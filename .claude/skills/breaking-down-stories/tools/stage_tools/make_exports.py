"""make_exports.py: the files made from the records for other programs, and the command export (blueprint 2.6, 5.1,
5.9, 7.1, 8.6, 8.7, step 11, card 23).

What this file does, in plain words:
- lays the film out in time: every shot of the scenes in scope, in film order, starting where the one before ends
  (the running sum of screen times, 5.9), in seconds and in frames at the project's frame rate;
- writes the shot list and the list of people, places and things as spreadsheets (16 Spreadsheets/, UTF-8 with a
  byte-order mark, the columns of 5.9);
- writes the captions as SubRip and WebVTT files (17 Captions and audio description/), timed by 5.9: one cue per
  heard speech, a speech's length from its words and the speaker's pace, cues between caption_min_s and
  caption_max_s, long speeches split at a sentence end, an off-screen speaker named, italics for a voice from
  outside the scene, a tag for a sound at sound emphasis 2 or more;
- writes the audio description script (what each frame shows, fitted into the gaps between the speeches) and the
  list of text to translate;
- writes the timeline as OpenTimelineIO JSON (written directly, no library needed) and as a CMX 3600 EDL, with a
  marker wherever a join is not a plain cut and wherever a shot has no kept take yet (D8 R2, R8);
- writes For machines - do not edit/breakdown.json and its schema in C5's portable subset (every field required,
  "none" for empty, lowercase word lists, nesting at most 3 levels) and checks one against the other;
- writes the voice line script (8.6), the music and effects spotting sheet, and the finishing jobs (FINISH records
  code makes from the shots, 8.7);
- checks the formats of what it wrote (byte-order mark and columns, SubRip and WebVTT, the timeline's structure,
  the EDL, breakdown.json against its schema) and registers the command export.

Every export is marked "Private study, not for publication" on its first page or first row when the story's rights
are study_only (step 0). SubRip has no place for a note, so the mark goes in the other files only.

Other modules use: write_breakdown_json(project_folder) (called by stage.py build), film_timeline, caption_cues,
check_export_formats, SHOT_LIST_COLUMNS, ELEMENT_COLUMNS, nesting_depth, validate_portable.

Standard library only.
"""

import csv
import io
import json
import re
from dataclasses import dataclass
from pathlib import Path

from .record_format import (add_record, ensure_end_line, make_record, new_record_file, normalise_word,
                            parse_file, sort_key_for_identifier, split_item, split_list, write_file)
from .project_files import MACHINE_FOLDER, Project, StageStop, history_run_folder, keep_in_history, safe_file_name
from .make_views import (STUDY_ONLY_MARK, ProjectView, is_empty, join_words,
                         job_file_plain_part, number_text, plain_part_lines_of, plain_value, recent_view,
                         replace_plain_part, scene_number, scene_of, seconds_words, shot_number_text, write_book,
                         write_text_exactly)

SPREADSHEETS_FOLDER = "16 Spreadsheets"
CAPTIONS_FOLDER = "17 Captions and audio description"
SHOT_LIST_FILE = "Shot list.csv"
ELEMENTS_FILE = "People, places and things.csv"
DESCRIPTION_FILE = "Audio description script.md"
TRANSLATE_FILE = "Text to translate.md"
OTIO_FILE = "timeline.otio"
EDL_FILE = "timeline.edl"
JSON_FILE = "breakdown.json"
JSON_SCHEMA_FILE = "breakdown.schema.json"
VOICE_SCRIPT_FILE = "20 Prompts for AI video/Voice line script.md"
SPOTTING_FILE = "21 Edit and finishing/Spotting sheet.md"
FINISHING_FILE = "21 Edit and finishing/Finishing jobs.md"
DERIVED_FILE = "derived fields.json"

# 5.9, in this order. The column names are Stage's own (blueprint's critic note on T8).
SHOT_LIST_COLUMNS = ["Scene", "Shot", "Crew label", "Size", "Angle", "Camera move", "Lens (mm)", "Subject (names)",
                     "Description", "Dialogue", "Screen time (s)", "Location", "Look", "Grey preview level",
                     "Storyboard", "Route", "Model", "Notes", "Shot ID", "Beats"]
ELEMENT_COLUMNS = ["Kind", "ID", "Name", "Fixed description", "States", "Scenes"]
EXPORT_KINDS = ["all", "shotlist", "book", "timeline", "captions", "json", "voices", "spotting", "finishing"]
ALL_KINDS = ["shotlist", "book", "timeline", "captions", "json"]  # step 11's set; the add-on files are asked for by name

# Speech paths heard from outside the scene: italic in captions (D8 R52, card 23).
ITALIC_PATHS = ("voice_over", "thought", "phone", "radio", "earpiece", "intercom", "device_speaker", "recording")
# Speech paths laid in the edit through a saved treatment (8.6, D3 R24): each makes a voice_path finishing job.
RELAYED_PATHS = ("earpiece", "radio", "intercom", "phone", "device_speaker", "recording", "helmet_inside",
                 "helmet_outside", "through_glass")
CAPTION_LINE_CHARACTERS = 42  # D8 R49, Netflix's English limit per caption line
FRAME_SHAPES_NEEDING_CROP = ("2.39", "1.85")  # generation models make 16:9 or 21:9 frames (card 23, D8 R17)
TIMELINE_START_HOURS = 1  # editors start a timeline at 01:00:00:00; captions count from zero (D8 R55)
ELEMENT_KINDS = [("CHARACTER", "person"), ("LOCATION", "place"), ("PROP", "thing"), ("TEXT", "text in picture"),
                 ("CAMERA", "in-story camera")]
PORTABLE_KEYWORDS = {"type", "properties", "required", "additionalProperties", "items", "enum", "description",
                     "title", "$schema"}


# ---------------------------------------------------------------- small helpers

def constant(view, name, default):
    value = view.constant(name, default)
    return default if value is None else value


def number(value, default=None):
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return default


CSV_WORDS = {"close_up": "close-up", "medium_close_up": "medium close-up", "extreme_close_up": "extreme close-up",
             "frame_left": "frame-left", "frame_right": "frame-right", "two_shot": "two-shot", "three_shot": "three-shot",
             "j_cut": "J-cut", "l_cut": "L-cut"}


def csv_word(value):
    """A stored word as a spreadsheet cell: close_up -> close-up, eye_level -> eye level, auto stays auto."""
    if value is None or is_empty(value):
        return ""
    word = normalise_word(str(value))
    if word in CSV_WORDS:
        return CSV_WORDS[word]
    return word.replace("_", " ") if re.fullmatch(r"[a-z0-9_]+", word) else str(value).strip()


def fps_of(view):
    fps = number(view.project_value("fps"), 24.0)
    return fps if fps and fps > 0 else 24.0


def raw_speeches(view):
    """{speech ID: the speeches.json entry as read writes it} (with its cue, parenthetical and extension)."""
    cached = getattr(view, "_raw_speeches", None)
    if cached is None:
        cached = {}
        path = view.folder / MACHINE_FOLDER / "speeches.json"
        if path.is_file():
            try:
                with open(path, encoding="utf-8") as handle:
                    cached = {entry["id"]: entry for entry in json.load(handle).get("speeches", []) if "id" in entry}
            except (OSError, ValueError, KeyError):
                cached = {}
        view._raw_speeches = cached
    return cached


def speaker_label(view, character_identifier, speech_identifier=None):
    """The name a caption gives a speaker: the cue the story writes (SAYE), else the first of the character's names,
    else the character's title."""
    raw = raw_speeches(view).get(speech_identifier) if speech_identifier else None
    if raw and raw.get("cue"):
        return raw["cue"].upper()
    record = view.record(character_identifier, "CHARACTER")
    if record is not None:
        names = split_list(record.get("names") or "")
        if names:
            return names[0].upper()
        if record.title:
            return record.title.upper()
    return (character_identifier or "").replace("CH-", "")


def element_of(identifier):
    """CH-IONA.S02 -> CH-IONA."""
    return re.sub(r"\.S\d{2}$", "", identifier or "")


def mark_line(view):
    return STUDY_ONLY_MARK if view.study_only else None


def export_title(view):
    return safe_file_name(view.title)


# ---------------------------------------------------------------- the film in time

@dataclass
class TimelineEntry:
    """One shot of the film in time: where it starts and ends, in seconds and in frames."""
    identifier: str
    scene: str
    record: object
    item: object
    screen_time_s: float
    start_s: float
    end_s: float
    start_frame: int
    end_frame: int

    @property
    def frames(self):
        return self.end_frame - self.start_frame


def film_timeline(view):
    """Every shot of the scenes in scope in film order, each starting where the one before ends (5.9: the first
    assembly). A shot listed but not yet written counts with its list item's time (at quick depth the list items are
    the shots). A shot with no screen time at all is left out."""
    fps = fps_of(view)
    entries = []
    clock = 0.0
    for scene in view.film_scene_ids():
        items = dict(view.list_items(scene))
        written = {shot.identifier: shot for shot in view.shots(scene)}
        identifiers = sorted(set(items) | set(written), key=sort_key_for_identifier)
        for identifier in identifiers:
            record = written.get(identifier)
            if record is None and view.record(identifier, "SHOT") is not None:
                continue  # an omitted shot keeps its ID and is skipped by exports (5.4 rule 6)
            item = items.get(identifier)
            seconds = number(record.get("screen_time")) if record is not None else None
            if seconds is None and item is not None:
                seconds = number(item.get("time"))
            if not seconds or seconds <= 0:
                continue
            start = clock
            clock += seconds
            entries.append(TimelineEntry(identifier, scene, record, item, seconds, start, clock,
                                         int(round(start * fps)), int(round(clock * fps))))
    return entries


# ---------------------------------------------------------------- captions (5.9)

@dataclass
class Cue:
    start_s: float
    end_s: float
    text: str
    kind: str = "speech"
    shot: str = ""
    speech: str = ""
    italic: bool = False
    speaker: str = ""

    def lines(self):
        return wrap_caption(self.text)


def sentences_of(text):
    pieces = re.findall(r"[^.!?]+[.!?]+[\"'”)]*|[^.!?]+$", text.strip())
    return [piece.strip() for piece in pieces if piece.strip()]


def word_count(text):
    return len([word for word in re.split(r"\s+", text.strip()) if re.search(r"[A-Za-z0-9]", word)])


def split_speech(text, pace, most_seconds):
    """A speech as parts of at most most_seconds each, split at sentence ends (5.9); a single sentence that is still
    too long is split at a comma, a semicolon or a dash, and as a last resort between words."""
    total = word_count(text) / pace if pace else 0.0
    if total <= most_seconds + 1e-9:
        return [(text.strip(), total)]
    limit_words = max(1, int(most_seconds * pace))
    units = []
    for sentence in sentences_of(text):
        if word_count(sentence) <= limit_words:
            units.append(sentence)
            continue
        clauses = [piece.strip() for piece in re.split(r"(?<=[,;:—])\s+", sentence) if piece.strip()]
        for clause in clauses:
            words = clause.split()
            while len(words) > limit_words:
                units.append(" ".join(words[:limit_words]))
                words = words[limit_words:]
            if words:
                units.append(" ".join(words))
    parts = []
    current = []
    for unit in units:
        candidate = " ".join(current + [unit])
        if current and word_count(candidate) > limit_words:
            parts.append(" ".join(current))
            current = [unit]
        else:
            current.append(unit)
    if current:
        parts.append(" ".join(current))
    return [(part, word_count(part) / pace) for part in parts]


def wrap_caption(text, width=CAPTION_LINE_CHARACTERS):
    """One or two lines of at most about width characters, broken at the space nearest the middle (D8 R49)."""
    text = re.sub(r"\s+", " ", text.strip())
    if len(text) <= width:
        return [text]
    middle = len(text) // 2
    spaces = [position for position, character in enumerate(text) if character == " "]
    if not spaces:
        return [text]
    fitting = [position for position in spaces if position <= width and len(text) - position - 1 <= width] or spaces

    def score(position):
        before = text[position - 1] if position else ""
        bonus = 20 if before in ".!?" else 8 if before in ",;:" else 0
        return abs(position - middle) - bonus

    best = min(fitting, key=score)
    return [text[:best], text[best + 1:]]


def speech_words_for(view, item):
    """(text, speaker ID, path) of a heard speech: the speech record's words (the story's words, D8 R47), else the
    words a chat copy wrote in the hear item."""
    speech = view.speech(item.first) if item.first else None
    text = (speech.get("text") or "").strip() if speech else ""
    if not text and item.get("words"):
        text = item.get("words").strip().strip('"“”')
    speaker = speech.get("speaker") if speech else None
    path = normalise_word(item.get("path") or (speech.get("path") if speech else None) or "direct")
    return text, speaker, path


def caption_cues(view, timeline=None):
    """Every caption cue of the film (5.9). Returns (cues, notes): notes say what could not be captioned."""
    timeline = film_timeline(view) if timeline is None else timeline
    lead = float(constant(view, "caption_lead_s", 0.25))
    shortest = float(constant(view, "caption_min_s", 1.0))
    longest = float(constant(view, "caption_max_s", 7.0))
    cues = []
    notes = []
    for entry in timeline:
        shot = entry.record
        if shot is None:
            continue
        speech_end = None
        for item in view.items(shot, "hear"):
            if not item.first or is_empty(item.first):
                continue
            text, speaker, path = speech_words_for(view, item)
            if not text:
                notes.append(f"{view.names.name(entry.identifier)}: the words of {item.first} are not known "
                             "(the story is not present), so it has no caption.")
                continue
            pace = view.breakdown.pace_of(speaker) if speaker else float(constant(view, "speech_wps_default", 2.5))
            at = number(item.get("at"))
            if at is not None:
                start = entry.start_s + at
                if cues and cues[-1].kind == "speech" and cues[-1].end_s > start and cues[-1].shot == entry.identifier:
                    cues[-1].end_s = max(cues[-1].start_s + 0.001, start)
            elif speech_end is None:
                start = entry.start_s + lead
            else:
                start = speech_end
            if cues and cues[-1].kind == "speech" and start < cues[-1].end_s and at is None:
                start = cues[-1].end_s
            speaker_seen = normalise_word(item.get("speaker") or "on_screen")
            italic = path in ITALIC_PATHS
            prefix = f"{speaker_label(view, speaker, item.first)}: " if speaker and speaker_seen == "off_screen" else ""
            pointer = start
            for position, (part, seconds) in enumerate(split_speech(text, pace, longest)):
                if position:
                    pointer = max(pointer, cues[-1].end_s)
                length = min(max(seconds, shortest), longest)
                cues.append(Cue(pointer, pointer + length, (prefix if position == 0 else "") + part, "speech",
                                entry.identifier, item.first, italic, speaker or ""))
                pointer += seconds
            speech_end = pointer
        for item in view.items(shot, "effect"):
            emphasis = number(item.get("sound_emphasis"), 0)
            if emphasis is None or emphasis < 2 or not item.first or is_empty(item.first):
                continue
            at = number(item.get("at"))
            start = entry.start_s + (at if at is not None else lead)
            words = item.first.strip()
            words = words[:1].lower() + words[1:] if words[:1].isupper() and not words[:2].isupper() else words
            cues.append(Cue(start, start + shortest, f"[{words}]", "sound", entry.identifier))
    cues.sort(key=lambda cue: (cue.start_s, 0 if cue.kind == "speech" else 1))
    return cues, notes


def time_text(seconds, separator):
    total = int(round(max(seconds, 0.0) * 1000))
    hours, rest = divmod(total, 3_600_000)
    minutes, rest = divmod(rest, 60_000)
    whole, milliseconds = divmod(rest, 1000)
    return f"{hours:02d}:{minutes:02d}:{whole:02d}{separator}{milliseconds:03d}"


def cue_text_lines(cue):
    lines = cue.lines()
    if cue.italic:
        lines = [f"<i>{line}</i>" for line in lines]
    return lines


def srt_text(cues):
    blocks = []
    for number_of_cue, cue in enumerate(cues, start=1):
        blocks.append("\n".join([str(number_of_cue), f"{time_text(cue.start_s, ',')} --> {time_text(cue.end_s, ',')}"]
                                + cue_text_lines(cue)))
    return "\n\n".join(blocks) + ("\n" if blocks else "")


def vtt_text(view, cues):
    lines = ["WEBVTT", "", "NOTE", f"{view.title}: captions made from the breakdown's speech records. Times count "
             "from the first frame of the film."]
    if view.study_only:
        lines.append(STUDY_ONLY_MARK + ".")
    lines.append("")
    for number_of_cue, cue in enumerate(cues, start=1):
        lines += [str(number_of_cue), f"{time_text(cue.start_s, '.')} --> {time_text(cue.end_s, '.')}"]
        lines += cue_text_lines(cue)
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


# ---------------------------------------------------------------- the shot list and the elements (5.9)

def subject_names(view, shot, item):
    names = []
    for subject in (view.items(shot, "subject") if shot is not None else []):
        if subject.first and not is_empty(subject.first):
            name = view.names.name(element_of(subject.first), short=True)
            if name not in names:
                names.append(name)
    if not names and item is not None:
        for piece in split_list(item.get("subject") or ""):
            if not is_empty(piece):
                name = view.names.name(element_of(piece), short=True)
                if name not in names:
                    names.append(name)
    return names


def dialogue_cell(view, shot):
    """'SC10-D10, SC10-D11: SAYE: What does it taste of? / IONA: Not mint.' (speech IDs, then the words)."""
    if shot is None:
        return ""
    identifiers = []
    words = []
    for item in view.items(shot, "hear"):
        if not item.first or is_empty(item.first):
            continue
        identifiers.append(item.first)
        text, speaker, _ = speech_words_for(view, item)
        if text:
            words.append(f"{speaker_label(view, speaker, item.first)}: {text}" if speaker else text)
    if not identifiers:
        return ""
    return ", ".join(identifiers) + (": " + " / ".join(words) if words else "")


def routed_model(view, shot):
    """The model a shot is made with: its own override, else what the prompt compiler routes it to when that module
    can say; empty while nothing is chosen."""
    if shot is None:
        return ""
    override = shot.get("model")
    if override and not is_empty(override):
        return split_item(override).first or ""
    try:
        from . import compile_prompts
    except ImportError:
        return ""
    for name in ("routed_model", "route_shot", "model_for_shot"):
        finder = getattr(compile_prompts, name, None)
        if finder is None:
            continue
        try:
            found = finder(view.breakdown, shot)
        except Exception:  # routing is WP8's; a failure there leaves the cell empty rather than stopping the export
            return ""
        if isinstance(found, str):
            return found
        model = getattr(found, "model", None) or (found.get("model") if isinstance(found, dict) else None)
        return model or ""
    return ""


def shot_list_rows(view, timeline=None):
    timeline = film_timeline(view) if timeline is None else timeline
    rows = []
    for entry in timeline:
        shot, item = entry.record, entry.item
        scene = view.record(entry.scene, "SCENE")
        location = view.record(scene.get("location"), "LOCATION") if scene is not None and scene.get("location") else None
        look = view.record(scene.get("look"), "LOOK") if scene is not None and scene.get("look") else None
        get = (lambda name: shot.get(name)) if shot is not None else (lambda name: None)
        kind = normalise_word(get("kind") or "live")
        size = get("size") or (item.get("size") if item is not None else None)
        label = ""
        try:
            from .derive_fields import crew_label
            label = crew_label(entry.identifier)
        except (ImportError, ValueError):
            label = ""
        rows.append([
            scene_number(entry.scene),
            shot_number_text(entry.identifier),
            label,
            "title card" if kind == "card" else "black" if kind == "black" else csv_word(size),
            csv_word(get("angle")),
            csv_word(get("move")),
            number_text(get("lens_mm")) if get("lens_mm") and not is_empty(get("lens_mm")) else "",
            ", ".join(subject_names(view, shot, item)),
            (item.get("shows") if item is not None else None) or (get("purpose") or ""),
            dialogue_cell(view, shot),
            number_text(entry.screen_time_s),
            location.title if location is not None and location.title else "",
            look.title if look is not None and look.title else "",
            get("previs_level") or "",
            "yes" if normalise_word(get("storyboard") or "no") == "yes" else "no",
            csv_word(get("route")),
            routed_model(view, shot),
            get("why") or "",
            entry.identifier,
            get("beats") or (item.get("beats") if item is not None else "") or "",
        ])
    return rows


def element_scenes(view):
    """{element ID: set of scene IDs} from every scene record that names the element or one of its states."""
    found = {}
    pattern = re.compile(r"(?<![\w-])((?:CH|PR|LOC|TX|CAM)-[A-Z0-9]+(?:-[A-Z0-9]+)*)(?:\.S\d{2})?(?![\w-])")
    for scene in view.film_scene_ids():
        records = [view.record(scene, "SCENE")] + view.shots(scene)
        records += [record for type_name in ("BEAT", "MOVE", "SHOTLIST") for record in view.breakdown.of_scene(type_name, scene)]
        for record in records:
            if record is None:
                continue
            for line in record.fields:
                for match in pattern.finditer(line.value or ""):
                    found.setdefault(match.group(1), set()).add(scene)
    for state in view.records("STATE"):
        element = state.get("element")
        where = split_item(state.get("from") or "").first if state.get("from") else None
        if element and where and re.match(r"^SC\d", where) and view.in_scope(where):
            found.setdefault(element, set()).add(where)
    return found


def element_rows(view):
    scenes_of = element_scenes(view)
    rows = []
    for type_name, kind in ELEMENT_KINDS:
        for record in view.records(type_name):
            description = record.get("fixed_description") or ""
            if type_name == "LOCATION":
                description = record.get("dressing") or record.get("story_job") or ""
            elif type_name == "TEXT":
                description = f'reads "{record.get("words")}"' if record.get("words") else ""
            states = [f"{state.identifier}: {state.get('state_line') or state.title or ''}".strip()
                      for state in view.records("STATE") if state.get("element") == record.identifier]
            scenes = sorted(scenes_of.get(record.identifier, set()), key=sort_key_for_identifier)
            rows.append([kind, record.identifier, record.title or "", "" if is_empty(description) else description,
                         "; ".join(states), ", ".join(scene_number(scene) for scene in scenes)])
    return rows


def csv_text(view, columns, rows):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    mark = mark_line(view)
    if mark:
        writer.writerow([mark])
    writer.writerow(columns)
    for row in rows:
        writer.writerow(row)
    return buffer.getvalue()


def write_csv(path, text):
    """UTF-8 with a byte-order mark (5.9), so spreadsheet programs read the letters right."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".part")
    with open(temporary, "w", encoding="utf-8-sig", newline="") as handle:
        handle.write(text)
    temporary.replace(path)


def write_spreadsheets(view, timeline=None):
    folder = view.folder / SPREADSHEETS_FOLDER
    shot_path = folder / SHOT_LIST_FILE
    element_path = folder / ELEMENTS_FILE
    write_csv(shot_path, csv_text(view, SHOT_LIST_COLUMNS, shot_list_rows(view, timeline)))
    write_csv(element_path, csv_text(view, ELEMENT_COLUMNS, element_rows(view)))
    return [shot_path, element_path]


# ---------------------------------------------------------------- audio description and text to translate

def hidden_elements(view, shot):
    """Elements a shot must not give away: must_not_show and the elements of the facts it keeps hidden."""
    hidden = {element_of(piece) for piece in split_list(shot.get("must_not_show") or "") if not is_empty(piece)}
    for item in view.items(shot, "keep_hidden"):
        fact = view.record(item.first, "FACT") if item.first else None
        if fact is not None and fact.get("element"):
            hidden.add(element_of(fact.get("element")))
    return hidden


def description_words(view, shot):
    """What the frame shows, from each subject's does (never a feeling, D18 R10), as short sentences."""
    hidden = hidden_elements(view, shot)
    sentences = []
    for item in view.items(shot, "subject"):
        if not item.first or is_empty(item.first) or element_of(item.first) in hidden:
            continue
        does = (item.get("does") or "").strip()
        if not does or is_empty(does):
            continue
        name = view.names.name(element_of(item.first), short=True)
        does = view.names.text(does, scene_of(shot.identifier))
        clauses = [clause.strip() for clause in does.split(";") if clause.strip()]
        sentences.append((name, clauses))
    return sentences


def smaller_clauses(clause):
    """A long clause cut at its commas and at 'then', so its start can still fit a short gap."""
    pieces = [piece.strip() for piece in re.split(r",\s+|\s+then\s+", clause) if piece.strip()]
    return pieces or [clause]


def speech_gaps(entry, cues):
    """[(start, end)] of the stretches of a shot with no speech cue, longest first."""
    inside = sorted((cue for cue in cues if cue.kind == "speech" and cue.end_s > entry.start_s and cue.start_s < entry.end_s),
                    key=lambda cue: cue.start_s)
    gaps = []
    pointer = entry.start_s
    for cue in inside:
        if cue.start_s > pointer:
            gaps.append((pointer, cue.start_s))
        pointer = max(pointer, cue.end_s)
    if entry.end_s > pointer:
        gaps.append((pointer, entry.end_s))
    return sorted(gaps, key=lambda gap: gap[1] - gap[0], reverse=True)


def fitted_description(sentences, words_allowed):
    """As many whole clauses as fit the words allowed, the first person first (D18 R9, R11)."""
    parts = []
    used = 0
    for name, clauses in sentences:
        taken = []
        for clause in clauses:
            count = len(clause.split()) + (1 if not taken else 0)
            if used + count > words_allowed:
                if not taken and not parts:
                    first_piece = smaller_clauses(clause)[0]
                    if len(first_piece.split()) >= 3 and used + len(first_piece.split()) + 1 <= words_allowed:
                        taken.append(first_piece)
                        used += len(first_piece.split()) + 1
                break
            taken.append(clause)
            used += count
        if taken:
            joined = "; ".join(taken)
            first_word = joined.split()[0].lower() if joined.split() else ""
            parts.append(f"{name}: {joined}." if first_word in ("his", "her", "their", "its", "the", "a", "an")
                         else f"{name} {joined}.")
        if used >= words_allowed:
            break
    return " ".join(parts)


def description_script_text(view, timeline, cues):
    pace = float(constant(view, "speech_wps_default", 2.5))
    lines = ["# Audio description script", ""]
    if view.study_only:
        lines += [f"{STUDY_ONLY_MARK}.", ""]
    lines += ["A narrator reads these lines in the gaps between the speeches, for people who cannot see the picture. "
              "Each line says only what the frame shows, in the present tense, and fits its gap at about "
              f"{number_text(pace)} words a second. Times count from the first frame of the film.", ""]
    current_scene = None
    written = 0
    for entry in timeline:
        shot = entry.record
        if shot is None or normalise_word(shot.get("needs_description") or "no") != "yes":
            continue
        if entry.scene != current_scene:
            current_scene = entry.scene
            lines += [f"## {view.scene_heading_words(entry.scene)}", ""]
        where = f"{time_text(entry.start_s, '.')}, {view.names.name(entry.identifier, entry.scene)}"
        if normalise_word(shot.get("silence") or "none") == "true_silence":
            lines.append(f"- {where}: left silent on purpose; nothing is read here.")
            continue
        sentences = description_words(view, shot)
        if not sentences:
            lines.append(f"- {where}: nothing to read; the shot's people have no behaviour written.")
            continue
        gaps = speech_gaps(entry, cues)
        if not gaps:
            lines.append(f"- {where}: no gap between the speeches; nothing is read here.")
            continue
        start, end = gaps[0]
        allowed = int((end - start) * pace)
        text = fitted_description(sentences, allowed)
        if not text:
            lines.append(f"- {where}: the gap of {seconds_words(round(end - start, 1))} is too short for a line.")
            continue
        lines.append(f"- {time_text(start, '.')}, {view.names.name(entry.identifier, entry.scene)} "
                     f"(a gap of {seconds_words(round(end - start, 1))}): {text}")
        written += 1
    if written == 0 and len(lines) <= 6:
        lines.append("No shot is marked as needing a description yet.")
    return "\n".join(lines).rstrip("\n") + "\n"


def text_shots(view, text_identifier):
    shots = []
    for shot in view.film_shots():
        if text_identifier in split_list(shot.get("text") or ""):
            shots.append(shot.identifier)
        elif any(item.first == text_identifier for item in view.items(shot, "thing")):
            shots.append(shot.identifier)
    return shots


def translate_text(view):
    names = view.names
    lines = ["# Text to translate", ""]
    if view.study_only:
        lines += [f"{STUDY_ONLY_MARK}.", ""]
    lines += ["Every piece of text in the pictures, for translators: the exact words, what they are on, who reads "
              "them, and where they are seen. Work from these words, not from the captions (D18 R18). Text that reads "
              "backwards on screen gets no subtitle in any language (D8 R53).", ""]
    marked, others = [], []
    for record in view.records("TEXT"):
        (marked if normalise_word(record.get("translate") or "no") == "yes" else others).append(record)
    for heading, records in (("To translate", marked), ("Other text in the pictures", others)):
        lines += [f"## {heading}", ""]
        if not records:
            lines += ["None.", ""]
            continue
        for record in records:
            title = record.title or names.name(record.identifier, short=True)
            parts = [f'"{record.get("words")}"' if record.get("words") and not is_empty(record.get("words")) else "no words yet"]
            if record.get("kind"):
                parts.append(csv_word(record.get("kind")))
            on = record.get("on")
            parts.append(f"on {names.name(on, short=True)}" if on and not is_empty(on) else "laid over the picture")
            if record.get("reader") and not is_empty(record.get("reader")):
                parts.append(f"read by {names.name(record.get('reader'), short=True)}")
            if normalise_word(record.get("plot_critical") or "no") == "yes":
                parts.append("the audience must read it")
            shots = text_shots(view, record.identifier)
            if shots:
                parts.append("seen in " + join_words([names.name(shot) for shot in shots]))
            lines.append(f"- {title}: " + "; ".join(parts) + ".")
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def write_captions(view, timeline=None):
    timeline = film_timeline(view) if timeline is None else timeline
    cues, notes = caption_cues(view, timeline)
    folder = view.folder / CAPTIONS_FOLDER
    title = export_title(view)
    srt_path = folder / f"{title}.srt"
    vtt_path = folder / f"{title}.vtt"
    write_text_exactly(srt_path, srt_text(cues))
    write_text_exactly(vtt_path, vtt_text(view, cues))
    description_path = folder / DESCRIPTION_FILE
    write_text_exactly(description_path, description_script_text(view, timeline, cues))
    translate_path = folder / TRANSLATE_FILE
    write_text_exactly(translate_path, translate_text(view))
    return [srt_path, vtt_path, description_path, translate_path], notes


# ---------------------------------------------------------------- the timeline: OpenTimelineIO and CMX 3600

def rational_time(value, rate):
    return {"OTIO_SCHEMA": "RationalTime.1", "rate": float(rate), "value": float(value)}


def time_range(start, duration, rate):
    return {"OTIO_SCHEMA": "TimeRange.1", "duration": rational_time(duration, rate),
            "start_time": rational_time(start, rate)}


def kept_take(view, shot_identifier):
    """The file of the kept take of a shot (TAKE kept: yes), or None."""
    for take in view.records("TAKE"):
        identifier = take.identifier or ""
        if identifier.startswith(f"TK-{shot_identifier}.") and normalise_word(take.get("kept") or "no") == "yes":
            if take.get("file") and not is_empty(take.get("file")):
                return take.get("file")
    return None


def join_after(view, shot_identifier):
    """The CUT record after a shot, when its join is not a plain cut."""
    match = re.match(r"^(SC\d{2,3}[A-Z]?)-SH(\d{3})$", shot_identifier)
    if not match:
        return None
    return view.record(f"{match.group(1)}-C{match.group(2)}", "CUT")


def marker(name, start, duration, rate, comment, color="RED"):
    return {"OTIO_SCHEMA": "Marker.2", "metadata": {}, "name": name, "color": color,
            "marked_range": time_range(start, duration, rate), "comment": comment}


def otio_timeline(view, timeline):
    fps = fps_of(view)
    handles = int(round(float(constant(view, "handles_s", 0.75)) * fps))
    clips = []
    for entry in timeline:
        shot, item = entry.record, entry.item
        take = kept_take(view, entry.identifier)
        start = handles if take else 0
        if take:
            reference = {"OTIO_SCHEMA": "ExternalReference.1", "metadata": {}, "name": Path(take).name,
                         "available_range": None, "available_image_bounds": None, "target_url": take}
        else:
            reference = {"OTIO_SCHEMA": "MissingReference.1", "metadata": {}, "name": "",
                         "available_range": None, "available_image_bounds": None}
        markers = []
        if not take:
            markers.append(marker(f"MISSING {entry.identifier}", start, entry.frames, fps,
                                  "No kept take yet: the grey preview, a storyboard frame or black stands in.",
                                  "YELLOW"))
        cut = join_after(view, entry.identifier)
        if cut is not None and normalise_word(cut.get("type") or "") not in ("", "continue"):
            detail = plain_value(cut.get("type"))
            if cut.get("black_frames") and not is_empty(cut.get("black_frames")):
                detail += f", {cut.get('black_frames')} black frames"
            if cut.get("split_s") and not is_empty(cut.get("split_s")):
                detail += f", sound {cut.get('split_s')} seconds across"
            markers.append(marker(f"JOIN {cut.identifier}", start + max(entry.frames - 1, 0), 1, fps,
                                  f"Build this join in the editor: {detail} (D8 R8).", "RED"))
        metadata = {"stage": {
            "shot": entry.identifier, "scene": entry.scene,
            "size": (shot.get("size") if shot is not None else None) or (item.get("size") if item is not None else "") or "",
            "screen_time_s": entry.screen_time_s, "start_s": round(entry.start_s, 3),
            "description": (item.get("shows") if item is not None else None) or "",
        }}
        clips.append({"OTIO_SCHEMA": "Clip.2", "metadata": metadata, "name": entry.identifier,
                      "source_range": time_range(start, entry.frames, fps), "effects": [], "markers": markers,
                      "enabled": True, "media_references": {"DEFAULT_MEDIA": reference},
                      "active_media_reference_key": "DEFAULT_MEDIA"})
    track = {"OTIO_SCHEMA": "Track.1", "metadata": {}, "name": "V1", "source_range": None, "effects": [],
             "markers": [], "enabled": True, "children": clips, "kind": "Video"}
    stack = {"OTIO_SCHEMA": "Stack.1", "metadata": {}, "name": "tracks", "source_range": None, "effects": [],
             "markers": [], "enabled": True, "children": [track]}
    metadata = {"stage": {"title": view.title, "fps": fps, "first_assembly": True,
                          "notice": STUDY_ONLY_MARK if view.study_only else "none",
                          "about": "Made by stage.py export from the records: every shot of the scenes in scope in film "
                                   "order, cut to cut. Joins that are not plain cuts are markers to build in the editor."}}
    return {"OTIO_SCHEMA": "Timeline.1", "metadata": metadata, "name": view.title,
            "global_start_time": rational_time(TIMELINE_START_HOURS * 3600 * fps, fps), "tracks": stack}


def timecode(frame, fps):
    whole = int(round(fps))
    frames = int(frame)
    hours, rest = divmod(frames, 3600 * whole)
    minutes, rest = divmod(rest, 60 * whole)
    seconds, frames = divmod(rest, whole)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{frames:02d}"


def edl_text(view, timeline):
    fps = fps_of(view)
    whole = int(round(fps))
    offset = TIMELINE_START_HOURS * 3600 * whole
    handles = int(round(float(constant(view, "handles_s", 0.75)) * fps))
    title = f"{view.title} - {STUDY_ONLY_MARK}" if view.study_only else view.title
    lines = [f"TITLE: {title}", "FCM: NON-DROP FRAME", ""]
    for event, entry in enumerate(timeline, start=1):
        take = kept_take(view, entry.identifier)
        source_in = handles if take else 0
        source_out = source_in + entry.frames
        record_in = offset + entry.start_frame
        record_out = offset + entry.end_frame
        lines.append(f"{event:03d}  {'AX':<8} V     C        {timecode(source_in, fps)} {timecode(source_out, fps)} "
                     f"{timecode(record_in, fps)} {timecode(record_out, fps)}")
        lines.append(f"* FROM CLIP NAME: {Path(take).name if take else entry.identifier}")
        cut = join_after(view, entry.identifier)
        if cut is not None and normalise_word(cut.get("type") or "") not in ("", "continue"):
            detail = plain_value(cut.get("type"))
            if cut.get("black_frames") and not is_empty(cut.get("black_frames")):
                detail += f", {cut.get('black_frames')} black frames"
            lines.append(f"* COMMENT: then {detail}; build it in the editor")
        if not take:
            lines.append(f"* COMMENT: MISSING {entry.identifier}, no kept take yet")
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def write_timeline(view, timeline=None):
    timeline = film_timeline(view) if timeline is None else timeline
    machine = view.folder / MACHINE_FOLDER
    otio_path = machine / OTIO_FILE
    edl_path = machine / EDL_FILE
    write_text_exactly(otio_path, json.dumps(otio_timeline(view, timeline), indent=4, ensure_ascii=False) + "\n")
    write_text_exactly(edl_path, edl_text(view, timeline))
    return [otio_path, edl_path]


# ---------------------------------------------------------------- breakdown.json and its portable schema (5.1)

def record_key(type_name):
    return type_name.lower()


def stored_and_derived_fields(schema, type_name):
    """Every field of a record type in schema order, plus the common fields, as definitions."""
    definitions = list(schema.data["record_types"][type_name].get("fields", []))
    names = {definition["name"] for definition in definitions}
    for common in schema.data.get("common_fields", {}).get("fields", []):
        if common["name"] not in names:
            definitions.append(common)
    return definitions


def word_enum(definition, type_definition=None):
    """The allowed words of a single-value word field (lowercase, with G7's none, open and auto), or None. The common
    field status takes its record type's own list (CHOICE, FINDING) and PREVIS stubs add planned (schema note)."""
    if definition.get("kind") != "word" or definition.get("repeat") or definition.get("stored") is False:
        return None
    values = definition.get("values")
    if definition.get("name") == "status" and type_definition and type_definition.get("status_values"):
        values = list(type_definition["status_values"]) + ["planned"]
    if not isinstance(values, list) or not values:
        return None
    words = [str(value) for value in values]
    for extra in (definition.get("also_allowed") or []):
        if isinstance(extra, str) and not extra.startswith("<"):
            words.append(extra)
    for empty in ("none", "open", "auto"):
        if empty not in words:
            words.append(empty)
    return list(dict.fromkeys(words))


def breakdown_schema(schema):
    """The portable JSON schema of breakdown.json (C5 P4): objects with every field required and no other fields,
    strings and arrays only, lowercase word lists, nesting at most 3 levels (the file, a list of records, a record),
    no patterns, ranges, unions or references."""
    types = schema.data["record_types"]
    properties = {
        "about": {"type": "string", "description": "What this file is."},
        "made_by": {"type": "string", "description": "The command that made it."},
        "schema_version": {"type": "string", "description": "The version of schema/schema.json it follows."},
        "title": {"type": "string", "description": "The story's title."},
        "scope": {"type": "string", "description": "The scenes it covers: all, or a comma list of scene IDs."},
        "notice": {"type": "string", "description": "Private study, not for publication, or none."},
    }
    for type_name, definition in types.items():
        record_properties = {
            "record_type": {"type": "string", "enum": [record_key(type_name)],
                            "description": "The record type, in lowercase (SHOT is shot)."},
            "record_id": {"type": "string", "description": "The record's ID; none for a singleton."},
            "record_title": {"type": "string", "description": "The plain title after the ID."},
            "record_files": {"type": "string", "description": "The files that hold the record, joined by commas."},
        }
        for field_definition in stored_and_derived_fields(schema, type_name):
            name = field_definition["name"]
            if name in record_properties:
                raise ValueError(f"The field {type_name}.{name} clashes with a record key of breakdown.json.")
            description = (field_definition.get("label") or name) + ": " + (field_definition.get("meaning") or "")
            if field_definition.get("repeat"):
                description += " Repeatable: one item per line."
            if field_definition.get("stored") is False:
                description += " Worked out by code (open when not worked out in this build)."
            entry = {"type": "string", "description": description.strip()}
            enum = word_enum(field_definition, definition)
            if enum:
                entry["enum"] = enum
            record_properties[name] = entry
        properties[record_key(type_name)] = {
            "type": "array",
            "description": f"Every {definition.get('plain_name') or type_name} record.",
            "items": {"type": "object", "additionalProperties": False, "properties": record_properties,
                      "required": list(record_properties)},
        }
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": "Stage breakdown",
            "description": "The whole breakdown made from the record files by stage.py build, in C5's portable subset "
                           "of JSON Schema: every field required, none for empty, nesting at most 3 levels.",
            "type": "object", "additionalProperties": False, "properties": properties,
            "required": list(properties)}


def load_derived(view):
    """The derived values of stage.py build (derived fields.json), else worked out now; {} when that fails."""
    path = view.folder / MACHINE_FOLDER / DERIVED_FILE
    if path.is_file():
        try:
            with open(path, encoding="utf-8") as handle:
                return json.load(handle)
        except (OSError, ValueError):
            pass
    try:
        from .derive_fields import derive_all
        return derive_all(view.breakdown)
    except Exception:  # derived values are extra in breakdown.json; they read open when they cannot be worked out
        return {}


def mapping_text(mapping, inner=None):
    if not isinstance(mapping, dict) or not mapping:
        return "none"
    return ", ".join(f"{key} {inner(value) if inner else value}" for key, value in mapping.items())


def derived_shot_values(derived):
    """The SHOT fields code works out, as strings, from derive_shot's result."""
    if not derived:
        return {}
    clips = derived.get("clips") or {}
    lengths = clips.get("clip_lengths_s") or []
    clip_text = ", ".join(number_text(length) for length in lengths) if lengths else "open"
    if clips.get("held"):
        clip_text += " (held)"
    image_sides = []
    for entry in derived.get("image_sides") or []:
        hands = entry.get("hands") or {}
        sides = [f"{hand.get('own', key)} hand {hand.get('image')}" for key, hand in hands.items() if isinstance(hand, dict)]
        features = [f"{feature.get('feature')} {feature.get('image')}" for feature in entry.get("features") or []]
        image_sides.append(f"{entry.get('state') or entry.get('element')}: " + ", ".join(sides + features))
    placements = []
    for element, moments in (derived.get("projected_placement") or {}).items():
        if moments:
            first = moments[0]
            placements.append(f"{element} {first.get('at')} facing {first.get('faces')}")
    dominant = derived.get("dominant")
    return {
        "label": derived.get("label") or "open",
        "min_screen_time_s": number_text(derived.get("min_screen_time_s")) if derived.get("min_screen_time_s") is not None else "open",
        "clips": clip_text,
        "era": derived.get("era") or "open",
        "mirror_state": mapping_text(derived.get("mirror_state")),
        "mirror_route": derived.get("mirror_route") or "open",
        "post_ops": ", ".join(derived.get("post_ops") or []) or "none",
        "image_sides": "\n".join(image_sides) or "none",
        "main_light_side": derived.get("main_light_side") or "open",
        "eyeline_sides": mapping_text(derived.get("eyeline_sides")),
        "projected_placement": "\n".join(placements) or "none",
        "size_check": derived.get("size_check") or "open",
        "face_height": mapping_text(derived.get("face_height"), number_text),
        "lip_sync": derived.get("lip_sync") or "open",
        "dominant": (dominant.get("dominant") if isinstance(dominant, dict) else dominant) or "open",
    }


def derived_scene_values(derived):
    if not derived:
        return {}
    return {
        "era": derived.get("era") or "open",
        "frame_handedness": derived.get("frame_handedness") or "open",
        "switch_at": str(derived.get("switch_at")) if derived.get("switch_at") else "none",
        "states_in_play": ", ".join(derived.get("states_in_play") or []) or "none",
        "duration_est_s": number_text(derived.get("duration_est_s")) if derived.get("duration_est_s") is not None else "open",
        "label": derived.get("label") or "open",
        "eighths": str(derived.get("eighths")) if derived.get("eighths") is not None else "open",
    }


def field_text(definition, values, enum=None):
    """A field's value in breakdown.json: one string, repeat items one per line, a word value written the list's way
    (lowercase, underscores) when it is one of the list's words."""
    values = [value.strip() for value in values if value is not None and value.strip()]
    if not values:
        return "none"
    if definition is not None and definition.get("kind") == "word" and not definition.get("repeat"):
        word = normalise_word(values[0])
        return word if (enum is None or word in enum) else values[0]
    if definition is not None and definition.get("repeat"):
        return "\n".join(values)
    return values[0]


def record_object(view, record, record_schema_properties, derived_values=None, files=None):
    type_name = record.type_name
    item = {"record_type": record_key(type_name), "record_id": record.identifier or "none", "record_title": record.title or "",
            "record_files": ", ".join(files or []) or "none"}
    definitions = {definition["name"]: definition for definition in stored_and_derived_fields(view.schema, type_name)}
    for name in record_schema_properties:
        if name in item:
            continue
        definition = definitions.get(name)
        values = record.get_all(name) if definition is None or definition.get("repeat") else \
            ([record.get(name)] if record.get(name) is not None else [])
        if values:
            item[name] = field_text(definition, values, record_schema_properties.get(name, {}).get("enum"))
        elif derived_values and name in derived_values:
            item[name] = derived_values[name]
        elif definition is not None and definition.get("stored") is False:
            item[name] = "open"
        else:
            item[name] = "none"
    return item


def speech_objects(view, properties):
    """The speeches of speeches.json (screenplays) as SPEECH records of breakdown.json."""
    found = []
    seen = {record.identifier for record in view.records("SPEECH")}
    for identifier in sorted(view.breakdown.speeches, key=sort_key_for_identifier):
        if identifier in seen:
            continue
        entry = view.breakdown.speeches[identifier]
        item = {"record_type": record_key("SPEECH"), "record_id": identifier, "record_title": "",
                "record_files": f"{MACHINE_FOLDER}/speeches.json"}
        lines = entry.get("lines") or [entry.get("line"), entry.get("line")]
        line_text = (f"{lines[0]}-{lines[-1]}" if lines and lines[0] != lines[-1] else str(entry.get("line") or "none"))
        raw = raw_speeches(view).get(identifier) or {}
        values = {"speaker": entry.get("speaker"), "line": line_text, "text": entry.get("text"),
                  "parenthetical": raw.get("parenthetical"), "extension": raw.get("extension"),
                  "path": normalise_word(entry.get("path") or "direct"), "word_count": str(entry.get("words") or "open"),
                  "origin": raw.get("origin") or "story"}
        for name in properties:
            if name in item:
                continue
            value = values.get(name)
            item[name] = str(value) if value not in (None, "") else "none"
        found.append(item)
    return found


def breakdown_data(view, json_schema):
    derived = load_derived(view)
    shots_derived = derived.get("shots") or {}
    scenes_derived = derived.get("scenes") or {}
    files_of = {}
    for record_file in view.record_files:
        for record in record_file.records:
            files_of.setdefault(record.key, [])
            if record_file.name not in files_of[record.key]:
                files_of[record.key].append(record_file.name)
    scope = view.scope()
    data = {
        "about": "The whole breakdown, made from the numbered record files by stage.py build. Never edit it: it is "
                 "made again on every build. Repeatable fields hold one item per line.",
        "made_by": "stage.py build",
        "schema_version": str(view.schema.data.get("schema_version") or "none"),
        "title": view.title,
        "scope": "all" if scope is None else ", ".join(sorted(scope, key=sort_key_for_identifier)),
        "notice": STUDY_ONLY_MARK if view.study_only else "none",
    }
    type_properties = {type_name: json_schema["properties"][record_key(type_name)]["items"]["properties"]
                       for type_name in view.schema.data["record_types"]}
    grouped = {type_name: [] for type_name in view.schema.data["record_types"]}
    for key, record in view.index.items():
        type_name = record.type_name
        if type_name not in grouped or normalise_word(record.get("status") or "") == "omitted":
            continue  # omitted records keep their IDs and are skipped by exports (5.4 rule 6)
        derived_values = None
        if type_name == "SHOT":
            derived_values = derived_shot_values(shots_derived.get(record.identifier))
        elif type_name == "SCENE":
            derived_values = derived_scene_values(scenes_derived.get(record.identifier))
        elif type_name == "LOCATION":
            orientation = ((derived.get("locations") or {}).get(record.identifier) or {}).get("orientation")
            derived_values = {"orientation": orientation or "open"}
        elif type_name == "STATE":
            until = ((derived.get("states") or {}).get(record.identifier) or {}).get("until")
            derived_values = {"until": until or "none"}
        elif type_name == "BEAT":
            marked = (scenes_derived.get(scene_of(record.identifier)) or {}).get("script_marked_beats", {})
            value = marked.get(record.identifier)
            derived_values = {"script_marked": "yes" if value is True else "no" if value is False else "open"}
        grouped[type_name].append(record_object(view, record, type_properties[type_name], derived_values,
                                                files_of.get(key)))
    grouped["SPEECH"] += speech_objects(view, type_properties["SPEECH"])
    for type_name, records in grouped.items():
        data[record_key(type_name)] = sorted(records, key=lambda item: sort_key_for_identifier(
            item["record_id"] if item["record_id"] != "none" else ""))
    return data


def write_breakdown_json(project_folder, view=None):
    """Write For machines - do not edit/breakdown.json and breakdown.schema.json (5.1). Called by stage.py build.
    Returns (paths, problems): problems are the schema check's lines (empty when the file validates)."""
    view = view or recent_view(project_folder) or ProjectView(project_folder)
    json_schema = breakdown_schema(view.schema)
    data = breakdown_data(view, json_schema)
    machine = view.folder / MACHINE_FOLDER
    json_path = machine / JSON_FILE
    schema_path = machine / JSON_SCHEMA_FILE
    write_text_exactly(schema_path, json.dumps(json_schema, indent=1, ensure_ascii=False) + "\n")
    write_text_exactly(json_path, json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    return [json_path, schema_path], check_breakdown_json(json_path, schema_path)


def nesting_depth(value):
    """How deeply objects and lists nest: the file itself is level 1, each object or list inside adds one."""
    if isinstance(value, dict):
        return 1 + max((nesting_depth(item) for item in value.values()), default=0)
    if isinstance(value, list):
        return 1 + max((nesting_depth(item) for item in value), default=0)
    return 0


def schema_nesting_depth(schema_node):
    """The same count for a schema: each object or array schema adds one level."""
    if not isinstance(schema_node, dict):
        return 0
    kind = schema_node.get("type")
    if kind == "object":
        return 1 + max((schema_nesting_depth(child) for child in (schema_node.get("properties") or {}).values()), default=0)
    if kind == "array":
        return 1 + schema_nesting_depth(schema_node.get("items"))
    return 0


def portable_subset_problems(schema_node, where="the schema"):
    """Where a schema leaves C5's portable subset: other keywords, an object without every field required or with
    other fields allowed, a type that is not one of the simple ones."""
    problems = []
    if not isinstance(schema_node, dict):
        return [f"{where} is not an object"]
    for key in schema_node:
        if key not in PORTABLE_KEYWORDS:
            problems.append(f"{where} uses the keyword {key}, which the portable subset leaves out")
    kind = schema_node.get("type")
    if kind not in ("object", "array", "string", "integer", "number", "boolean"):
        problems.append(f"{where} has the type {kind!r}")
    if kind == "object":
        properties = schema_node.get("properties") or {}
        if schema_node.get("additionalProperties") is not False:
            problems.append(f"{where} allows fields it does not list")
        if sorted(schema_node.get("required") or []) != sorted(properties):
            problems.append(f"{where} does not require every field")
        for name, child in properties.items():
            problems += portable_subset_problems(child, f"{where} > {name}")
    if kind == "array":
        problems += portable_subset_problems(schema_node.get("items"), f"{where} > items")
    enum = schema_node.get("enum")
    if enum is not None:
        for word in enum:
            if not isinstance(word, str) or word != word.lower():
                problems.append(f"{where} has the list word {word!r}, which is not lowercase")
                break
    return problems


def validate_portable(instance, schema_node, where="breakdown.json", limit=40):
    """Validate a value against a portable-subset schema (type, properties, required, additionalProperties, items,
    enum). Returns plain problem lines (at most limit)."""
    problems = []

    def visit(value, node, path):
        if len(problems) >= limit:
            return
        kind = node.get("type")
        expected = {"object": dict, "array": list, "string": str, "boolean": bool}.get(kind)
        if kind in ("integer", "number"):
            if isinstance(value, bool) or not isinstance(value, (int, float)) or (kind == "integer" and not isinstance(value, int)):
                problems.append(f"{path} should be a {kind}")
                return
        elif expected is not None and not isinstance(value, expected):
            problems.append(f"{path} should be {'an' if kind in ('object', 'array') else 'a'} {kind}")
            return
        if "enum" in node and value not in node["enum"]:
            problems.append(f"{path} is {value!r}, which is not one of its allowed words")
        if kind == "object":
            properties = node.get("properties") or {}
            for name in node.get("required") or []:
                if name not in value:
                    problems.append(f"{path} lacks {name}")
            if node.get("additionalProperties") is False:
                for name in value:
                    if name not in properties:
                        problems.append(f"{path} has {name}, which the schema does not list")
            for name, child in properties.items():
                if name in value:
                    visit(value[name], child, f"{path} > {name}")
        elif kind == "array":
            for position, child in enumerate(value):
                label = child.get("record_id") if isinstance(child, dict) and child.get("record_id") else str(position + 1)
                visit(child, node.get("items") or {}, f"{path} > {label}")

    visit(instance, schema_node, where)
    return problems[:limit]


# ---------------------------------------------------------------- the format checks (step 11, T8)

def check_csv(path, columns):
    """Byte-order mark, exactly the columns (after the optional private-study row), the same width on every row."""
    problems = []
    data = Path(path).read_bytes()
    if not data.startswith(b"\xef\xbb\xbf"):
        problems.append(f"{Path(path).name} does not start with the byte-order mark")
    rows = list(csv.reader(io.StringIO(data.decode("utf-8-sig"))))
    if rows and rows[0] == [STUDY_ONLY_MARK]:
        rows = rows[1:]
    if not rows or rows[0] != columns:
        problems.append(f"{Path(path).name} does not have exactly the columns of 5.9 in order")
    for number_of_row, row in enumerate(rows[1:], start=2):
        if len(row) != len(columns):
            problems.append(f"{Path(path).name} row {number_of_row} has {len(row)} cells, not {len(columns)}")
            break
    return problems


SRT_TIME = re.compile(r"^(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})$")
VTT_TIME = re.compile(r"^(\d{2,}):(\d{2}):(\d{2})\.(\d{3}) --> (\d{2,}):(\d{2}):(\d{2})\.(\d{3})(?: .*)?$")


def seconds_of(groups):
    hours, minutes, seconds, milliseconds = (int(part) for part in groups)
    return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000


def parse_srt(text):
    """[(number, start, end, [lines])] of a SubRip file; raises ValueError naming the first fault."""
    text = text.replace("\r\n", "\n").lstrip("﻿")
    cues = []
    for block_number, block in enumerate(re.split(r"\n\s*\n", text.strip()), start=1):
        if not block.strip():
            continue
        lines = block.split("\n")
        if len(lines) < 3:
            raise ValueError(f"cue {block_number} has no number, time or text")
        if not lines[0].strip().isdigit():
            raise ValueError(f"cue {block_number} does not start with its number")
        match = SRT_TIME.match(lines[1].strip())
        if not match:
            raise ValueError(f"cue {block_number} has the time line {lines[1]!r}, not HH:MM:SS,mmm --> HH:MM:SS,mmm")
        cues.append((int(lines[0]), seconds_of(match.groups()[:4]), seconds_of(match.groups()[4:]), lines[2:]))
    return cues


def parse_vtt(text):
    """[(identifier, start, end, [lines])] of a WebVTT file; raises ValueError naming the first fault."""
    text = text.replace("\r\n", "\n").lstrip("﻿")
    blocks = re.split(r"\n\s*\n", text.strip("\n"))
    if not blocks or not re.match(r"^WEBVTT(?:[ \t].*)?$", blocks[0].split("\n")[0]):
        raise ValueError("the file does not start with WEBVTT")
    cues = []
    for block in blocks[1:]:
        lines = [line for line in block.split("\n")]
        if not lines or not lines[0].strip():
            continue
        if lines[0].startswith("NOTE") or lines[0].startswith("STYLE") or lines[0].startswith("REGION"):
            continue
        identifier = None
        if "-->" not in lines[0]:
            identifier = lines[0].strip()
            lines = lines[1:]
        if not lines:
            raise ValueError(f"cue {identifier} has no time line")
        match = VTT_TIME.match(lines[0].strip())
        if not match:
            raise ValueError(f"the time line {lines[0]!r} is not HH:MM:SS.mmm --> HH:MM:SS.mmm")
        body = lines[1:]
        if not body or any("-->" in line for line in body):
            raise ValueError(f"cue {identifier or lines[0]} has no text, or text holding -->")
        cues.append((identifier, seconds_of(match.groups()[:4]), seconds_of(match.groups()[4:8]), body))
    return cues


def cue_order_problems(name, cues):
    problems = []
    previous = -1.0
    for position, cue in enumerate(cues, start=1):
        start, end = cue[1], cue[2]
        if end <= start:
            problems.append(f"{name} cue {position} ends before it starts")
            break
        if start + 1e-9 < previous:
            problems.append(f"{name} cue {position} starts before the cue before it")
            break
        previous = start
    return problems


def check_srt(path):
    name = Path(path).name
    try:
        cues = parse_srt(Path(path).read_text(encoding="utf-8"))
    except ValueError as error:
        return [f"{name}: {error}"]
    problems = []
    if [cue[0] for cue in cues] != list(range(1, len(cues) + 1)):
        problems.append(f"{name}: the cues are not numbered 1, 2, 3 in order")
    return problems + cue_order_problems(name, cues)


def check_vtt(path):
    name = Path(path).name
    try:
        cues = parse_vtt(Path(path).read_text(encoding="utf-8"))
    except ValueError as error:
        return [f"{name}: {error}"]
    return cue_order_problems(name, cues)


def rational_problems(node, where):
    if not isinstance(node, dict) or node.get("OTIO_SCHEMA") != "RationalTime.1":
        return [f"{where} is not a RationalTime.1"]
    rate, value = node.get("rate"), node.get("value")
    if not isinstance(rate, (int, float)) or rate <= 0 or not isinstance(value, (int, float)) or value < 0:
        return [f"{where} has a rate or value out of range"]
    return []


def range_problems(node, where, require_length=True):
    if not isinstance(node, dict) or node.get("OTIO_SCHEMA") != "TimeRange.1":
        return [f"{where} is not a TimeRange.1"]
    problems = rational_problems(node.get("start_time"), f"{where} start") + \
        rational_problems(node.get("duration"), f"{where} duration")
    if not problems and require_length and node["duration"]["value"] <= 0:
        problems.append(f"{where} has no length")
    return problems


def check_otio(path):
    """The structural check of an OpenTimelineIO file (T8): a Timeline.1 over a Stack.1 of Track.1, whose items are
    clips, gaps or transitions with valid time ranges, and valid markers and media references."""
    name = Path(path).name
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return [f"{name} is not readable JSON: {error}"]
    problems = []
    if data.get("OTIO_SCHEMA") != "Timeline.1":
        return [f"{name} is not a Timeline.1"]
    if data.get("global_start_time") is not None:
        problems += rational_problems(data["global_start_time"], f"{name} global start")
    stack = data.get("tracks")
    if not isinstance(stack, dict) or stack.get("OTIO_SCHEMA") != "Stack.1" or not isinstance(stack.get("children"), list):
        return problems + [f"{name} has no Stack.1 of tracks"]
    for track_number, track in enumerate(stack["children"], start=1):
        where = f"{name} track {track_number}"
        if not isinstance(track, dict) or track.get("OTIO_SCHEMA") != "Track.1":
            problems.append(f"{where} is not a Track.1")
            continue
        if track.get("kind") not in ("Video", "Audio"):
            problems.append(f"{where} has the kind {track.get('kind')!r}")
        names = set()
        for position, child in enumerate(track.get("children") or [], start=1):
            label = f"{where} item {position}"
            schema_name = child.get("OTIO_SCHEMA") if isinstance(child, dict) else None
            if schema_name not in ("Clip.1", "Clip.2", "Gap.1", "Transition.1"):
                problems.append(f"{label} is {schema_name!r}, not a clip, gap or transition")
                continue
            if schema_name != "Transition.1":
                problems += range_problems(child.get("source_range"), f"{label} source range")
            if schema_name == "Clip.2":
                references = child.get("media_references")
                key = child.get("active_media_reference_key")
                if not isinstance(references, dict) or key not in references:
                    problems.append(f"{label} has no active media reference")
                elif (references[key] or {}).get("OTIO_SCHEMA") not in ("MissingReference.1", "ExternalReference.1",
                                                                       "GeneratorReference.1", "ImageSequenceReference.1"):
                    problems.append(f"{label} has an unknown media reference")
            if schema_name.startswith("Clip"):
                if child.get("name") in names:
                    problems.append(f"{label} repeats the clip name {child.get('name')}")
                names.add(child.get("name"))
            for marker_number, item in enumerate(child.get("markers") or [], start=1):
                if not isinstance(item, dict) or item.get("OTIO_SCHEMA") not in ("Marker.1", "Marker.2"):
                    problems.append(f"{label} marker {marker_number} is not a marker")
                else:
                    problems += range_problems(item.get("marked_range"), f"{label} marker {marker_number}", False)
    return problems


EDL_EVENT = re.compile(r"^(\d{3,4})\s+(\S{1,8})\s+(V|A|A2|AA|B|AA/V)\s+(C|D\s*\d+|W\d+)\s+"
                       r"(\d{2}:\d{2}:\d{2}:\d{2})\s+(\d{2}:\d{2}:\d{2}:\d{2})\s+(\d{2}:\d{2}:\d{2}:\d{2})\s+(\d{2}:\d{2}:\d{2}:\d{2})\s*$")


def frames_of_timecode(text, fps):
    hours, minutes, seconds, frames = (int(part) for part in text.split(":"))
    return ((hours * 60 + minutes) * 60 + seconds) * int(round(fps)) + frames


def check_edl(path, fps=24):
    """A CMX 3600 EDL: TITLE and FCM lines, numbered events in order, source and record lengths equal, record times
    running on without gaps."""
    name = Path(path).name
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    problems = []
    if not lines or not lines[0].startswith("TITLE:"):
        problems.append(f"{name} does not start with TITLE:")
    if not any(line.startswith("FCM:") for line in lines[:4]):
        problems.append(f"{name} has no FCM line")
    expected = 1
    previous_out = None
    for line in lines:
        if not line.strip() or line.startswith(("TITLE:", "FCM:", "*")):
            continue
        match = EDL_EVENT.match(line)
        if not match:
            problems.append(f"{name}: {line!r} is not an event line")
            break
        if int(match.group(1)) != expected:
            problems.append(f"{name}: event {match.group(1)} is out of order")
            break
        expected += 1
        source_in, source_out, record_in, record_out = (frames_of_timecode(match.group(index), fps) for index in range(5, 9))
        if source_out - source_in != record_out - record_in or record_out <= record_in:
            problems.append(f"{name}: event {match.group(1)} has different source and record lengths")
            break
        if previous_out is not None and record_in != previous_out:
            problems.append(f"{name}: event {match.group(1)} does not start where the one before ends")
            break
        previous_out = record_out
    return problems


def check_breakdown_json(json_path, schema_path):
    problems = []
    try:
        data = json.loads(Path(json_path).read_text(encoding="utf-8"))
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return [f"breakdown.json or its schema is not readable JSON: {error}"]
    problems += [f"breakdown.schema.json: {line}" for line in portable_subset_problems(schema)[:10]]
    problems += validate_portable(data, schema)
    depth = nesting_depth(data)
    if depth > 3:
        problems.append(f"breakdown.json nests {depth} levels; at most 3 are allowed")
    if schema_nesting_depth(schema) > 3:
        problems.append("breakdown.schema.json nests more than 3 levels")
    return problems


def check_export_formats(project_folder, view=None):
    """Every format check of step 11 on the files that exist. Returns plain problem lines (empty when all pass)."""
    folder = Path(project_folder)
    view = view or ProjectView(folder)
    problems = []
    spreadsheets = folder / SPREADSHEETS_FOLDER
    for name, columns in ((SHOT_LIST_FILE, SHOT_LIST_COLUMNS), (ELEMENTS_FILE, ELEMENT_COLUMNS)):
        if (spreadsheets / name).is_file():
            problems += check_csv(spreadsheets / name, columns)
    captions = folder / CAPTIONS_FOLDER
    title = export_title(view)
    if (captions / f"{title}.srt").is_file():
        problems += check_srt(captions / f"{title}.srt")
    if (captions / f"{title}.vtt").is_file():
        problems += check_vtt(captions / f"{title}.vtt")
    machine = folder / MACHINE_FOLDER
    if (machine / OTIO_FILE).is_file():
        problems += check_otio(machine / OTIO_FILE)
    if (machine / EDL_FILE).is_file():
        problems += check_edl(machine / EDL_FILE, fps_of(view))
    if (machine / JSON_FILE).is_file() and (machine / JSON_SCHEMA_FILE).is_file():
        problems += check_breakdown_json(machine / JSON_FILE, machine / JSON_SCHEMA_FILE)
    return problems


# ---------------------------------------------------------------- voices, spotting and finishing (add-ons C and D)

def delivery_words(view, entry, speech_identifier, speaker, most):
    """How a line is said, in at most most words: the parenthetical, then the speaker's tactic in the shot."""
    parts = []
    raw = raw_speeches(view).get(speech_identifier) or {}
    parenthetical = raw.get("parenthetical")
    if parenthetical and not is_empty(parenthetical):
        parts.append(parenthetical.strip("() "))
    shot = entry.record if entry is not None else None
    if shot is not None and speaker:
        for item in view.items(shot, "subject"):
            if element_of(item.first) == speaker and item.get("tactic"):
                parts.append(plain_value(item.get("tactic")))
                break
    words = " ".join("; ".join(parts).split()[:most])
    return words or "as written"


def voice_script_text(view, timeline):
    most = int(view.constant("voice_delivery_words_max", 8) or 8)
    heard_in = {}
    for entry in timeline:
        if entry.record is None:
            continue
        for item in view.items(entry.record, "hear"):
            if item.first and item.first not in heard_in:
                heard_in[item.first] = (entry, item)
    lines = ["# Voice line script", ""]
    if view.study_only:
        lines += [f"{STUDY_ONLY_MARK}.", ""]
    lines += ["Every line of speech in film order, for recording or making the voices (8.6): its ID, the exact words, "
              f"how it is said in at most {most} words, and how the voice reaches us. The words are the story's; "
              "keep them exactly, in every take.", ""]
    current = None
    count = 0
    for scene in view.film_scene_ids():
        speeches = view.breakdown.speeches_of_scene(scene)
        if not speeches:
            continue
        for speech in speeches:
            if speech is None:
                continue
            if scene != current:
                current = scene
                lines += [f"## {view.scene_heading_words(scene)}", ""]
            entry, item = heard_in.get(speech["id"], (None, None))
            speaker = speech.get("speaker")
            voice = next((record for record in view.records("VOICE") if record.get("character") == speaker), None)
            path = normalise_word((item.get("path") if item is not None else None) or speech.get("path") or "direct")
            where = f", in {view.names.name(entry.identifier, scene)}" if entry is not None else ", not heard in any shot yet"
            lines.append(f"- {speech['id']}, {view.names.name(speaker, short=True) if speaker else 'unknown speaker'}"
                         f" ({voice.identifier if voice is not None else 'no voice yet'}){where}: \"{speech.get('text') or ''}\" "
                         f"Delivery: {delivery_words(view, entry, speech['id'], speaker, most)}. Path: {plain_value(path)}.")
            count += 1
    if count == 0:
        lines.append("No speeches yet: the story has not been read, or no scene is in scope.")
    return "\n".join(lines).rstrip("\n") + "\n"


def spotting_text(view, timeline, cues):
    soundplan = view.singleton("SOUNDPLAN")
    policy = normalise_word((soundplan.get("music_policy") if soundplan is not None else None) or "open")
    lines = ["# Spotting sheet", ""]
    if view.study_only:
        lines += [f"{STUDY_ONLY_MARK}.", ""]
    lines += [f"Where music and sounds start and stop, in film time from the first frame. Music policy: "
              f"{plain_value(policy)}.", "", "## Music cues", ""]
    musics = view.records("MUSIC")
    if not musics:
        lines.append("No music cues." + (" The music policy is none, so none are written (D9 R1)." if policy == "none" else ""))
    for music in musics:
        lines.append(f"- {music.identifier}: from {view.names.name(music.get('in')) if music.get('in') else 'open'} "
                     f"to {view.names.name(music.get('out')) if music.get('out') else 'open'}; "
                     f"{music.get('function') or 'no function written'}; must not: {music.get('must_not') or 'open'}.")
    lines += ["", "## Sounds", ""]
    found = False
    for entry in timeline:
        if entry.record is None:
            continue
        for item in view.items(entry.record, "effect"):
            if not item.first or is_empty(item.first):
                continue
            at = number(item.get("at"), 0.0) or 0.0
            lines.append(f"- {time_text(entry.start_s + at, '.')}, {view.names.name(entry.identifier)}: {item.first}"
                         f" (sound emphasis {item.get('sound_emphasis') or 'open'}).")
            found = True
    if not found:
        lines.append("No sounds written in the shots yet.")
    lines += ["", "## Silences and cuts to black", ""]
    found = False
    for entry in timeline:
        if entry.record is None:
            continue
        silence = normalise_word(entry.record.get("silence") or "none")
        if silence != "none":
            lines.append(f"- {time_text(entry.start_s, '.')} to {time_text(entry.end_s, '.')}, "
                         f"{view.names.name(entry.identifier)}: {plain_value(silence)}.")
            found = True
        cut = join_after(view, entry.identifier)
        if cut is not None and normalise_word(cut.get("type") or "") in ("cut_to_black", "fade", "freeze"):
            frames = cut.get("black_frames") or "open"
            lines.append(f"- {time_text(entry.end_s, '.')}, after {view.names.name(entry.identifier)}: "
                         f"{plain_value(cut.get('type'))}, {frames} frames.")
            found = True
    if not found:
        lines.append("None.")
    return "\n".join(lines).rstrip("\n") + "\n"


def derived_operations(view, timeline):
    """{shot ID: [operations]} of the finishing jobs code makes from the shots (8.7)."""
    from .derive_fields import lip_sync, post_operations
    operations = {}
    frame_shape = normalise_word(view.project_value("frame_shape") or "2.39")
    first_of_sequence = set()
    seen_sequences = set()
    for entry in timeline:
        scene = view.record(entry.scene, "SCENE")
        sequence = scene.get("sequence") if scene is not None else None
        if sequence and sequence not in seen_sequences:
            seen_sequences.add(sequence)
            first_of_sequence.add(entry.identifier)
    for position, entry in enumerate(timeline):
        shot = entry.record
        if shot is None:
            continue
        found = []
        kind = normalise_word(shot.get("kind") or "live")
        try:
            found += [normalise_word(operation) for operation in post_operations(view.breakdown, shot)]
        except Exception:  # a shot whose mirror route cannot be worked out gets its other jobs
            pass
        if kind == "card":
            found.append("title")
        elif kind != "black" and frame_shape in FRAME_SHAPES_NEEDING_CROP:
            found.append("crop")
        if kind not in ("card", "black"):
            try:
                tight = lip_sync(view.breakdown, shot) == "tight"
            except Exception:  # no set plan or no speech: no lip-sync job
                tight = False
            on_screen = any(normalise_word(item.get("speaker") or "") == "on_screen" for item in view.items(shot, "hear"))
            if tight and on_screen:
                found.append("lip_sync")
        for item in view.items(shot, "hear"):
            _, _, path = speech_words_for(view, item)
            if path in RELAYED_PATHS:
                found.append("voice_path")
                break
        if entry.identifier in first_of_sequence and kind not in ("card", "black"):
            found.append("grade")
        if position == 0:
            found.append("grain")
        operations[entry.identifier] = list(dict.fromkeys(operation for operation in found if operation))
    return operations


def write_finishing_jobs(view, timeline):
    """Make a FINISH record for every operation a shot needs (8.7); keep the jobs already made (with what the AI
    wrote in them), and mark stale a job whose operation the shot no longer needs. Returns (path, made, marked)."""
    path = view.folder / FINISHING_FILE
    wanted = derived_operations(view, timeline)
    project = Project(view.folder, view.schema, view.words)
    if path.is_file():
        record_file = parse_file(path, FINISHING_FILE, view.schema)
    else:
        record_file = new_record_file(FINISHING_FILE, ["# Finishing jobs"], "Finishing jobs")
    existing = {}
    used_numbers = {}
    for record in record_file.records:
        if record.type_name != "FINISH":
            continue
        shot = record.get("shot") or ""
        operation = normalise_word(record.get("operation") or "")
        existing[(shot, operation)] = record
        match = re.search(r"-(\d{2})$", record.identifier or "")
        if match:
            used_numbers.setdefault(shot, set()).add(int(match.group(1)))
    made, marked = [], []
    for shot, operations in wanted.items():
        for operation in operations:
            if (shot, operation) in existing:
                continue
            numbers = used_numbers.setdefault(shot, set())
            number_free = 1
            while number_free in numbers:
                number_free += 1
            numbers.add(number_free)
            identifier = f"FX-{shot}-{number_free:02d}"
            record = make_record("FINISH", identifier, f"{plain_value(operation).capitalize()} for shot {shot_number_text(shot)}",
                                 [("shot", shot), ("operation", operation), ("status", "draft"), ("locked", "no")])
            add_record(record_file, record, view.schema, ["FINISH", "MUSIC"])
            made.append(identifier)
    for (shot, operation), record in existing.items():
        if operation not in wanted.get(shot, []) and normalise_word(record.get("status") or "") not in ("stale", "omitted"):
            record.set_field("status", "stale", view.schema)
            marked.append(record.identifier)
    if not made and not marked and path.is_file():
        return path, made, marked
    ensure_end_line(record_file, "Finishing jobs")
    if path.is_file():
        keep_in_history(history_run_folder(project), path, FINISHING_FILE)
    write_file(record_file, path, view.schema)
    # The file's plain part lists every job (make_views writes it from the records).
    fresh_view = ProjectView(view.folder, view.schema, view.words, view.constants)
    fresh = parse_file(path, FINISHING_FILE, view.schema)
    if replace_plain_part(fresh, job_file_plain_part(fresh_view, fresh, plain_part_lines_of(fresh))):
        write_file(fresh, path, view.schema)
    if made or marked:
        text = []
        if made:
            text.append(f"Made {len(made)} finishing job{'s' if len(made) != 1 else ''} to fill in")
        if marked:
            text.append(f"marked {len(marked)} out of date")
        try:
            project.add_log_entry("; ".join(text) + ", in 21 Edit and finishing.")
        except (OSError, ValueError):
            pass
    return path, made, marked


# ---------------------------------------------------------------- the command: export

def add_export_arguments(parser):
    parser.add_argument("what", nargs="?", default="all", choices=EXPORT_KINDS,
                        help="all (the book, spreadsheets, captions, timeline and machine files of step 11), or one "
                             "of shotlist, book, timeline, captions, json, voices, spotting, finishing")
    parser.add_argument("--story", help="a story file to read the lines and speeches from (default: the project's)")


def run_export(context):
    """stage.py export <what>: build first (derived fields, views, breakdown.json), then write the exports asked for
    and check their formats. Exit 1 when a format check fails."""
    from .derive_fields import run_build
    what = getattr(context.arguments, "what", "all") or "all"
    kinds = ALL_KINDS if what == "all" else [what]
    build_code = run_build(context)
    if build_code:
        return build_code
    view = None if getattr(context.arguments, "story", None) else recent_view(context.project)
    if view is None:
        view = ProjectView(context.project, context.schema, context.words, context.constants)
        if getattr(context.arguments, "story", None):
            view.breakdown.attach_story_file(context.arguments.story)
    if not view.film_scene_ids() and what not in ("json", "book"):
        if view.records("CHAPTER") and not view.records("SCENE"):
            raise StageStop("There are no scenes to export yet: a book's scenes are written with the story plan "
                            "(step 3 of 12), after its chapters are read. stage.py export book works now.")
        raise StageStop("There are no scenes to export yet: the scene list is empty or no scene is in the project's "
                        "scope. Run stage.py read first, or check PROJECT scope in 00 Start here.")
    timeline = film_timeline(view)
    written = []
    notes = []
    if "book" in kinds:
        written += write_book(view.folder, view=view)
    if "shotlist" in kinds:
        written += write_spreadsheets(view, timeline)
    if "captions" in kinds:
        paths, caption_notes = write_captions(view, timeline)
        written += paths
        notes += caption_notes
    if "timeline" in kinds:
        written += write_timeline(view, timeline)
    if "json" in kinds:
        written += [view.folder / MACHINE_FOLDER / JSON_FILE, view.folder / MACHINE_FOLDER / JSON_SCHEMA_FILE]
        if getattr(context.arguments, "story", None):
            paths, _ = write_breakdown_json(view.folder, view)
    if "voices" in kinds:
        path = view.folder / VOICE_SCRIPT_FILE
        write_text_exactly(path, voice_script_text(view, timeline))
        written.append(path)
    if "spotting" in kinds:
        cues, _ = caption_cues(view, timeline)
        path = view.folder / SPOTTING_FILE
        write_text_exactly(path, spotting_text(view, timeline, cues))
        written.append(path)
    if "finishing" in kinds:
        path, made, marked = write_finishing_jobs(view, timeline)
        written.append(path)
        context.say(f"Finishing jobs: {len(made)} made, {len(marked)} marked out of date, in {FINISHING_FILE}.")
    for path in written:
        context.say(f"Written: {Path(path).relative_to(view.folder).as_posix()}")
    for note in notes:
        context.say(f"Note: {note}")
    if view.study_only:
        context.say(f"Every export is marked {STUDY_ONLY_MARK} (the rights answer).")
    try:  # C19: the exports say when they cover only the scenes in scope
        from .project_files import scope_words
        scope_line = scope_words(view.breakdown.index)
        if scope_line:
            context.say(scope_line)
    except (ImportError, AttributeError):
        pass
    problems = check_export_formats(view.folder, view)
    if problems:
        for problem in problems:
            context.say(f"E Format check: {problem}")
        context.summary = f"export {what}: {len(written)} files, {len(problems)} format problems"
        return 1
    length = timeline[-1].end_s if timeline else 0
    context.say(f"Format checks passed: {len(timeline)} shots, {len(timeline)} timeline events, "
                f"about {round(length)} seconds of film.")
    context.summary = f"export {what}: {len(written)} files, formats checked"
    return 0


def register_commands(table):
    if "export" in getattr(table, "commands", {}):
        return
    table.add("export", "Make the book, spreadsheets, captions, timeline and machine files from the records",
              run_export, add_export_arguments)
