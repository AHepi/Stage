"""derive_fields.py: everything code works out from the records and never lets the AI type (blueprint 5.6).

What this file does, in plain words:
- loads a project's records (or any set of record files, such as the gold example) into one Breakdown,
  with the numbered story and the speeches when they are there;
- works out every shot's time floor, max(speech floor, text floor) + pause owed, with its reasons in words
  ("speech floor 11.8 s: Saye 19 words at 2.0 = 9.5 s, ..."), and the provisional floor of each list item
  that step 8's handout prints;
- works out clip lengths (screen time plus handles, rounded up to a length the model allows), whether a shot
  is a held take, and where a shot that is not held may be split;
- works out labels and counts: the crew label ("10Q"), words per speech and per character, speaking counts,
  the coverage map, the scene's label, its length from its shots and on the page (eighths, A3's line-count
  model), whether the script already marks each beat, and what a shot shows first (dominant, at Standard);
- works out the mirror world: each scene's era and frame handedness (with the line where it switches), each
  element's mirror state (mirrored when its state's handedness differs from the frame's; open while the era
  lines are not in the story given), each place's orientation, each shot's mirror route (8.5) and its
  finishing operations;
- works out sides: the image side and the prompt side of every sided feature in frame, and which own hand is
  the hand nearest the camera;
- works out geometry where a set plan exists: frame placement and facing of every person, projected from the
  marks, the scene's start, the floor-plan moves and the setup (with the facing Blender uses); the eyeline side
  of every single; the size check from lens and distance; the face height; the frame side of the look's main
  light; the side of the line each setup stands on;
- resolves every story point to the beat whose lines hold its quote, and can store that beat (code_state);
- lists the grey preview jobs (PREVIS stubs, status planned) that time slices and shared geometry name;
- registers the command build, which works all of this out, stores the story points' beats, makes the stubs
  the checker accepts, and writes "For machines - do not edit/derived fields.json".

Other modules use: Breakdown (from_project, from_paths, breakdown_for_run for a check run), time_floor,
provisional_floor, clip_plan, held_take, scene_era, era_at, mirror_state_at, shot_mirror_states, mirror_route,
image_sides, eyeline_sides, projected_placement, size_check, face_heights, lip_sync, main_light_side,
story_points, scene_eighths, script_marked, dominant_of, derive_shot, derive_scene, derive_all.

Numbers come from _config/rules/constants.json by name. The few layout numbers that are judgement (where a third of
the frame ends) are named below with a note.

Standard library only.

After the full run on The Catch (Project notes 31 and 32):
- word swaps are made once and everywhere; the time floor counts text to read and owes a beat's pause on the last
  shot naming it; light words are read in their sentence.

After the three-scene test of the fixed kit (Project notes 35 and 36):
- a light at rest marks no beat (light_moves_in, here now, with LIGHT_MOVING_NEAR); a speech split at a phrase is
  timed for the words a shot hears; one or two letters match a text only when its thing is in the scene.

After the second full run (Project notes 39 and 40):
- printed words on nothing that a text rule governs follow the scene's place; the states in play take the things a
  handout names; eyeline sides are read when the line is spoken; a shot that writes "text: none" owes no reading time;
  a list item that quotes part of a speech owes only that part.
- after its cross-examination: "text: none" still owes reading time for a text whose thing the shot shows at
  emphasis 2 or whose words it quotes.
"""

import json
import math
import re
from dataclasses import dataclass, field as dataclass_field
from pathlib import Path

from .record_format import (adapter_file, load_json, load_skill_data, merge_copies, normalise_word, parse_file,
                            parse_line_numbers,
                            parse_story_point, sort_key_for_identifier, split_item, split_list, split_outside_quotes)

MACHINE_FOLDER = "For machines - do not edit"
DERIVED_FILE = "derived fields.json"
SPEECHES_FILE = "speeches.json"

SCENE_OF = re.compile(r"^(SC\d{2,3}[A-Z]?)(?:-|$)")
SHOT_NUMBER = re.compile(r"-SH(\d+)$")
BEAT_NUMBER = re.compile(r"-B(\d+)$")
STATE_ID = re.compile(r"^(.+)\.S\d{2}$")
NUMBER_IN_TEXT = re.compile(r"-?\d+(?:\.\d+)?")
POINT_TEXT = re.compile(r"^\[\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*(?:,\s*(-?\d+(?:\.\d+)?)\s*)?\]$")
STORY_POINT_KINDS = ("story_point", "story_point_list", "scene_or_story_point")

# The shot-size ladder, widest first (5.5 SHOT size; insert is not on the ladder).
SIZE_LADDER = ["extreme_wide", "wide", "medium_wide", "medium", "medium_close_up", "close_up", "extreme_close_up"]
# Where a subject sits across the frame, from left to right (5.5 SHOT subject at).
PLACEMENT_WORDS = ["left_edge", "left_third", "centre", "right_third", "right_edge"]
# The frame runs from -1 (left edge) to +1 (right edge). Where the centre, the thirds and the edges fall, and where a
# subject is out of frame, come from the constant frame_placement_bands; these are its values when it is missing.
FRAME_PLACEMENT_BANDS = {"centre_half_width": 0.2, "third_outer": 0.6, "out_of_frame": 1.1}
# A person's eye point is at this share of their height, and a person with no height_m counts this tall: the constant
# projection_body; these are its values when it is missing.
PROJECTION_BODY = {"eye_height_share": 0.93, "height_fallback_m": 1.7}
# Crew labels use capital letters from A, skipping I and O (5.3).
LABEL_LETTERS = [letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if letter not in "IO"]
# The facing words a subject can have in a frame, in the order they go round the subject.
FACING_ROUND = ["camera", "frame_right", "away", "frame_left"]
FRAME_RATIOS = {"2.39": 2.39, "1.85": 1.85, "16_9": 16 / 9, "4_3": 4 / 3, "9_16": 9 / 16}
HELD_ROLES = ("turn",)


# ---------------------------------------------------------------- small helpers

def constant(constants, name, default=None):
    """The value of a named constant of _config/rules/constants.json (either table), or default."""
    if not constants:
        return default
    for section in (constants.get("constants", {}), constants.get("from_blueprint_text", {}).get("constants", {})):
        if name in section:
            entry = section[name]
            return entry.get("value", default) if isinstance(entry, dict) else entry
    return default


def number_of(text, default=None):
    """The first number in a value ('15', '15 s', '2.0'), or default."""
    if text is None:
        return default
    match = NUMBER_IN_TEXT.search(str(text))
    return float(match.group(0)) if match else default


def point_of(text):
    """A point value '[2.8, 2.55]' or '[-3.5, 1.8, 1.45]' as a tuple of floats, or None."""
    if not text:
        return None
    match = POINT_TEXT.match(str(text).strip())
    if not match:
        return None
    return tuple(float(part) for part in match.groups() if part is not None)


def is_yes(value):
    return normalise_word(value or "") == "yes"


def element_of(reference):
    """The element a reference names: CH-IONA for CH-IONA.S02, the reference itself otherwise."""
    if not reference:
        return reference
    match = STATE_ID.match(reference)
    return match.group(1) if match else reference


def scene_of(identifier):
    match = SCENE_OF.match(identifier or "")
    return match.group(1) if match else None


def shot_number(identifier):
    match = SHOT_NUMBER.search(identifier or "")
    return int(match.group(1)) if match else None


def beat_number(identifier):
    match = BEAT_NUMBER.search(identifier or "")
    return int(match.group(1)) if match else None


def person_name(identifier):
    """A plain name for a character ID: CH-SAYE -> Saye, CH-DR-SAYE -> Dr Saye."""
    if not identifier:
        return ""
    name = element_of(identifier)
    name = re.sub(r"^[A-Z]{2,4}-", "", name)
    return " ".join(part.capitalize() for part in name.split("-"))


def seconds_text(value):
    """A number of seconds for a reason line: 9.5, 0.8, 13.8, 2.0 (one decimal, more only when needed)."""
    if value is None:
        return "?"
    rounded = round(value, 2)
    text = f"{rounded:.2f}".rstrip("0")
    if text.endswith("."):
        text += "0"
    return text


def round_seconds(value):
    return None if value is None else round(value + 0.0, 2)


def item_of(value, definition=None):
    return split_item(value, definition)


def count_words(text):
    """Words counted the way read_story counts them (wc -w in its plain setting)."""
    try:
        from .read_story import count_words as reader_count
        return reader_count(text)
    except Exception:  # the reader is part of the same package; this is only a fallback
        return len([piece for piece in (text or "").split() if re.search(r"[A-Za-z0-9]", piece)])


def ranges_to_set(ranges):
    numbers = set()
    for first, last in ranges or ():
        numbers.update(range(first, last + 1))
    return numbers


# ---------------------------------------------------------------- the records, the story and the speeches

class Breakdown:
    """Every record of a project merged by ID (G10), with the numbered story and the speeches when present.

    Build one with Breakdown.from_project(folder), Breakdown.from_paths([...], story_path=...) or
    Breakdown(record_files, ...). All derivations are methods, cached per Breakdown.
    """

    def __init__(self, record_files, schema=None, words=None, constants=None, story=None, speeches=None,
                 models=None, project_folder=None, story_map=None):
        if schema is None or words is None or constants is None:
            loaded_schema, loaded_words, loaded_constants = load_skill_data()
            schema = schema or loaded_schema
            words = words or loaded_words
            constants = constants or loaded_constants
        self.schema = schema
        self.words = words or {}
        self.constants = constants or {}
        self.record_files = list(record_files)
        self.index, self.conflicts = merge_copies(self.record_files, schema)
        self.by_identifier = {}
        for (type_name, identifier), record in self.index.items():
            self.by_identifier.setdefault(identifier or type_name, record)
        self.story = story
        self.story_map = story_map or {}
        self.speeches = dict(speeches or {})
        self.models = models
        self.project_folder = Path(project_folder) if project_folder else None
        self._cache = {}

    # -------------------------------------------------- making one

    @classmethod
    def from_project(cls, project_folder, schema=None, words=None, constants=None):
        """The project's record files, its story map (numbered story) and speeches.json, when they exist."""
        from .project_files import Project
        if schema is None or words is None or constants is None:
            schema, words, constants = load_skill_data()
        project = Project(project_folder, schema, words)
        record_files = project.load_record_files()
        story = None
        story_map = None
        speeches = {}
        machine = Path(project_folder) / MACHINE_FOLDER
        try:
            from .read_story import NumberedStory, load_story_map
            story_map = load_story_map(project_folder)
            if story_map:
                story = NumberedStory.from_story_map(story_map)
        except (ImportError, OSError, ValueError, KeyError):
            story, story_map = None, None
        speeches_path = machine / SPEECHES_FILE
        if speeches_path.is_file():
            with open(speeches_path, encoding="utf-8") as handle:
                speeches = speeches_from_json(json.load(handle))
        return cls(record_files, schema, words, constants, story=story, speeches=speeches,
                   models=load_video_models(), project_folder=project_folder, story_map=story_map)

    @classmethod
    def from_paths(cls, paths, story_path=None, schema=None, words=None, constants=None, models=None):
        """Record files given by path (the gold example and its context file, for example), and optionally a
        story file (the whole story or a test excerpt), read the way stage.py read reads it."""
        if schema is None or words is None or constants is None:
            schema, words, constants = load_skill_data()
        record_files = [parse_file(Path(path), Path(path).name, schema) for path in paths]
        breakdown = cls(record_files, schema, words, constants, models=models)
        if story_path:
            breakdown.attach_story_file(story_path)
        return breakdown

    def attach_story_file(self, story_path):
        """Read a story file (or a test excerpt with its header) and use its numbered lines and speeches."""
        from .read_story import NumberedStory, load_story_file, read_story_lines, story_map_of
        reading = read_story_lines(load_story_file(story_path), self.constants)
        self.story_map = story_map_of(reading)
        self.story = NumberedStory.from_story_map(self.story_map)
        self.speeches = {}
        for speech in reading.speeches:
            self.speeches[speech.identifier] = speech_entry(speech.to_json())
        self._cache.clear()
        return self

    # -------------------------------------------------- finding records

    def record(self, identifier, type_name=None):
        if identifier is None:
            return None
        if type_name:
            return self.index.get((type_name, identifier))
        return self.by_identifier.get(identifier)

    def records_of(self, type_name, include_omitted=False):
        found = [record for (kind, _), record in self.index.items() if kind == type_name]
        if not include_omitted:
            found = [record for record in found if normalise_word(record.get("status") or "") != "omitted"]
        return sorted(found, key=lambda record: sort_key_for_identifier(record.identifier or ""))

    def singleton(self, type_name):
        return self.index.get((type_name, None))

    @property
    def project(self):
        found = self.records_of("PROJECT", include_omitted=True)
        return found[0] if found else None

    def of_scene(self, type_name, scene_identifier):
        return [record for record in self.records_of(type_name) if scene_of(record.identifier) == scene_identifier]

    def scene_identifiers(self):
        found = {record.identifier for record in self.records_of("SCENE")}
        for type_name in ("SHOT", "BEAT", "SHOTLIST"):
            found.update(scene_of(record.identifier) for record in self.records_of(type_name))
        found.discard(None)
        return sorted(found, key=sort_key_for_identifier)

    def shots_of(self, scene_identifier):
        return self.of_scene("SHOT", scene_identifier)

    def beats_of(self, scene_identifier):
        return self.of_scene("BEAT", scene_identifier)

    def definition(self, type_name, field_name):
        return self.schema.field(type_name, field_name)

    def items(self, record, field_name):
        """Every item of a repeatable field as record_format.Item (first part and named sub-parts)."""
        definition = self.definition(record.type_name, field_name)
        found = []
        for value in record.get_all(field_name):
            if normalise_word(value) == "none":
                continue
            found.append(split_item(value, definition))
        return found

    def item(self, record, field_name):
        found = self.items(record, field_name)
        return found[0] if found else None

    def id_list(self, record, field_name):
        value = record.get(field_name) if record is not None else None
        if not value or normalise_word(value) == "none":
            return []
        return [piece for piece in split_list(value) if normalise_word(piece) != "none"]

    # -------------------------------------------------- lines

    def scene_range(self, scene_identifier):
        """(first, last) line of a scene: from its SCENE lines, else the story's scene, else None."""
        key = ("scene_range", scene_identifier)
        if key in self._cache:
            return self._cache[key]
        found = None
        scene = self.record(scene_identifier, "SCENE")
        value = scene.get("lines") if scene else None
        if value:
            ranges = parse_line_numbers(value)
            if ranges:
                found = (ranges[0][0], ranges[-1][1])
            elif self.story is not None:
                found = self.story.resolve_lines(value)
        if found is None and self.story is not None:
            found = self.story.scope_of(scene_identifier)
        self._cache[key] = found
        return found

    def lines_of(self, record, field_name="lines"):
        """The line numbers a lines value names, as a sorted list; quote anchors are resolved in the scene."""
        value = record.get(field_name) if record is not None else None
        if not value or normalise_word(value) == "none":
            return []
        ranges = parse_line_numbers(value)
        if ranges:
            return sorted(ranges_to_set(ranges))
        if self.story is None:
            return []
        scope = self.scene_range(scene_of(record.identifier)) or (None, None)
        resolved = self.story.resolve_lines(value, scope[0], scope[1])
        return list(range(resolved[0], resolved[1] + 1)) if resolved else []

    def last_story_line(self, numbers):
        """The last line of a set that holds words (blank lines at the end do not count)."""
        if not numbers:
            return None
        if self.story is None:
            return max(numbers)
        for number in sorted(numbers, reverse=True):
            if self.story.line(number).strip():
                return number
        return max(numbers)

    def line_reference(self, value, scene_identifier=None):
        """A single-line reference (a number or a quote) as a line number, or None."""
        if value is None:
            return None
        ranges = parse_line_numbers(value)
        if ranges:
            return ranges[0][0]
        if self.story is None:
            return None
        scope = self.scene_range(scene_identifier) if scene_identifier else None
        if scope:
            found = self.story.resolve_line(value, scope[0], scope[1])
            if found:
                return found
        return self.story.resolve_line(value)

    # -------------------------------------------------- speeches

    def speech(self, identifier):
        """A speech as a dict (speaker, words, cue line, text, path), from speeches.json, the story, or a prose
        SPEECH record; None when unknown."""
        if identifier in self.speeches:
            return self.speeches[identifier]
        record = self.record(identifier, "SPEECH")
        if record is not None:
            text = record.get("text") or ""
            entry = {"id": identifier, "speaker": record.get("speaker"), "words": count_words(text),
                     "line": self.line_reference(record.get("line"), scene_of(identifier)), "text": text,
                     "path": record.get("path") or "direct"}
            self.speeches[identifier] = entry
            return entry
        return None

    def speeches_of_scene(self, scene_identifier):
        found = [entry for identifier, entry in self.speeches.items() if scene_of(identifier) == scene_identifier]
        for record in self.of_scene("SPEECH", scene_identifier):
            if record.identifier not in self.speeches:
                found.append(self.speech(record.identifier))
        return sorted(found, key=lambda entry: sort_key_for_identifier(entry["id"]))

    def pace_of(self, character):
        """Words per second for a character: its VOICE pace_wps, else speech_wps_default (K08)."""
        default = constant(self.constants, "speech_wps_default", 2.5)
        character = element_of(character)
        record = self.record(character, "CHARACTER")
        voice_identifier = record.get("voice") if record else None
        voices = [self.record(voice_identifier, "VOICE")] if voice_identifier else []
        voices += [voice for voice in self.records_of("VOICE") if voice.get("character") == character]
        for voice in voices:
            if voice is not None and number_of(voice.get("pace_wps")):
                return number_of(voice.get("pace_wps"))
        return default


def breakdown_for_run(run):
    """The Breakdown of one check run (check_records.CheckRun), made once and kept in run.cache: the same record
    files, and the run's story and speeches when it has them."""
    cache = getattr(run, "cache", None)
    if isinstance(cache, dict) and "derive_fields.breakdown" in cache:
        return cache["derive_fields.breakdown"]
    source = getattr(run, "story", None)
    numbered = getattr(source, "numbered", None) if source is not None else None
    raw_speeches = getattr(source, "speeches", None) or {}
    speeches = {identifier: speech_entry(entry) for identifier, entry in raw_speeches.items()}
    project = getattr(run, "project", None)
    folder = getattr(project, "folder", None) if project is not None else None
    breakdown = Breakdown(run.record_files, run.schema, run.words, run.constants, story=numbered,
                          speeches=speeches, models=load_video_models(), project_folder=folder,
                          story_map=getattr(source, "story_map", None) if source is not None else None)
    if isinstance(cache, dict):
        cache["derive_fields.breakdown"] = breakdown
    return breakdown


def speech_entry(data):
    """One speeches.json entry as the dict Breakdown.speech returns."""
    lines = data.get("lines") or [data.get("line"), data.get("line")]
    return {"id": data["id"], "speaker": data.get("speaker"), "words": data.get("word_count"),
            "line": data.get("line"), "lines": lines, "text": data.get("text", ""), "path": data.get("path", "direct")}


def speeches_from_json(data):
    return {entry["id"]: speech_entry(entry) for entry in data.get("speeches", [])}


def load_video_models(skill_folder=None):
    """The dated video model facts of _config/adapters/video_models.json, or None while that file does not exist."""
    try:
        return load_json(adapter_file("video_models.json"), skill_folder).get("models")
    except (OSError, ValueError):
        return None


# ---------------------------------------------------------------- time floors (5.6, TIME-01)

@dataclass
class TimeFloor:
    """A shot's time floor, max(speech floor, text floor) + pause owed, with every part that makes it."""
    shot: str
    floor: float
    speech_floor: float
    text_floor: float
    pause_owed: float
    speech_parts: list = dataclass_field(default_factory=list)   # (speech ID, speaker, words, pace, seconds)
    text_parts: list = dataclass_field(default_factory=list)     # (text ID, seconds, how)
    pause_parts: list = dataclass_field(default_factory=list)    # (beat ID, seconds, why)
    unknown_speeches: list = dataclass_field(default_factory=list)
    provisional: bool = False
    extra_per_speech_s: float = 0.5
    shared_speeches: list = dataclass_field(default_factory=list)  # (speech ID, other list items sharing its beat)
    unresolved_lines: list = dataclass_field(default_factory=list)  # records whose lines (quote anchors) are not found

    @property
    def complete(self):
        """False when some speech's words are unknown (no story and no words on the hear item), or when the lines of
        the shot or of one of its beats are quote anchors not found in the story given, so the pause owed is not
        known."""
        return not self.unknown_speeches and not self.unresolved_lines

    def speech_reason(self):
        if not self.speech_parts:
            return "no speech"
        by_speaker = {}
        order = []
        for _, speaker, words, pace, _ in self.speech_parts:
            if speaker not in by_speaker:
                by_speaker[speaker] = [0, pace]
                order.append(speaker)
            by_speaker[speaker][0] += words
        pieces = []
        for speaker in order:
            words, pace = by_speaker[speaker]
            pieces.append(f"{person_name(speaker)} {words} words at {seconds_text(pace)} = "
                          f"{seconds_text(words / pace)} s")
        count = len(self.speech_parts)
        pieces.append(f"{count} {'speech' if count == 1 else 'speeches'} x {seconds_text(self.extra_per_speech_s)} s")
        return f"speech floor {seconds_text(self.speech_floor)} s: " + ", ".join(pieces)

    def text_reason(self):
        if not self.text_parts:
            return ""
        return f"text floor {seconds_text(self.text_floor)} s: " + ", ".join(
            f"{identifier} {seconds_text(seconds)} s ({how})" for identifier, seconds, how in self.text_parts)

    def pause_reason(self):
        if not self.pause_parts:
            return "no pause owed"
        pieces = [f"{seconds_text(seconds)} s {why}" for _, seconds, why in self.pause_parts if seconds > 0]
        if not pieces:
            return "no pause owed"
        return f"pause owed {seconds_text(self.pause_owed)} s: " + ", ".join(pieces)

    def reasons(self):
        """The floor with its reasons in one line, as 5.6 prints it."""
        parts = [self.speech_reason()]
        text = self.text_reason()
        if text:
            parts.append(text)
        parts.append(self.pause_reason())
        line = f"floor {seconds_text(self.floor)} s ({'; '.join(parts)})"
        if self.unknown_speeches:
            line += "; words unknown for " + ", ".join(self.unknown_speeches)
        if self.unresolved_lines:
            line += "; lines not found for " + ", ".join(self.unresolved_lines) + ", so the pause owed may be more"
        if self.shared_speeches:
            line += "; " + "; ".join(
                f"{speech} may be heard in {', '.join(others)} instead (a shared beat), which lowers this floor"
                for speech, others in self.shared_speeches)
        return line

    def short_reason(self):
        """The TIME-01 wording: '(speech 11.8 s + pause owed after the turn at beat 7, 2.0 s)'."""
        pieces = []
        if self.text_floor > self.speech_floor:
            pieces.append(f"text {seconds_text(self.text_floor)} s")
        else:
            pieces.append(f"speech {seconds_text(self.speech_floor)} s")
        owed = [(beat, seconds, why) for beat, seconds, why in self.pause_parts if seconds > 0]
        if owed:
            pieces.append(" + ".join(f"pause owed {why}, {seconds_text(seconds)} s" for _, seconds, why in owed))
        return " + ".join(pieces)


def pause_seconds(breakdown, beat):
    """(seconds, tier, why) of the pause a beat owes after it: its pause_after seconds (the tier's lower end when
    no seconds are written), and at least turn_reaction_min_s after a turn (5.6, TIME-05)."""
    item = breakdown.item(beat, "pause_after")
    tier = normalise_word(item.first) if item and item.first else "none"
    seconds = number_of(item.get("seconds")) if item else None
    if seconds is None:
        tiers = constant(breakdown.constants, "pause_tiers", {}) or {}
        if tier in tiers and isinstance(tiers[tier], dict):
            seconds = tiers[tier].get("from_s", tiers[tier].get("above_s", 0.0))
        else:
            seconds = 0.0
    turn = normalise_word(beat.get("turn") or "none")
    number = beat_number(beat.identifier)
    if turn != "none":
        minimum = constant(breakdown.constants, "turn_reaction_min_s", 2.0)
        if minimum > seconds:
            return minimum, tier, f"after the turn at beat {number}"
        return seconds, tier, f"after the turn at beat {number}"
    return seconds, tier, f"after beat {number}"


def text_reading_seconds(breakdown, text_record, mirrored=False):
    """(seconds, how) to read one TEXT in picture: max(2.0, 1.0 + characters / 13); with emphasis 2 or more at
    least 2.0 + 0.5 x words; doubled when mirrored (K09, text_floor)."""
    rule = constant(breakdown.constants, "text_floor", {}) or {}
    words = (text_record.get("words") or "").strip().strip('"')
    characters = len(words)
    seconds = max(rule.get("minimum_s", 2.0), rule.get("base_s", 1.0) + characters / rule.get("characters_per_second", 13))
    how = f"{characters} characters"
    emphasis = number_of(text_record.get("emphasis"), 0)
    if emphasis >= rule.get("plot_critical_emphasis_min", 2):
        word_count = len(words.split())
        critical = rule.get("plot_critical_base_s", 2.0) + rule.get("plot_critical_per_word_s", 0.5) * word_count
        if critical > seconds:
            seconds = critical
            how = f"emphasis {int(emphasis)}, {word_count} words"
    if mirrored:
        seconds *= rule.get("mirrored_factor", 2)
        how += ", mirrored"
    return seconds, how


# ---------------------------------------------------------------- word swaps for prompts (8.1 rule 5)

def project_prompt_swaps(words, project_record):
    """[(from, to)] of the prompt word swaps: words.json's prompt_substitutions that are plain words, and the project's
    own PROJECT prompt_words (torch becomes flashlight, cage becomes open steel freight elevator car)."""
    swaps = []
    for swap in ((words or {}).get("prompt_substitutions") or {}).get("swaps") or []:
        source, target = swap.get("from", ""), swap.get("to", "")
        if source and target and "<" not in source and "(" not in target and "visible evidence" not in target:
            swaps.append((source, target))
    if project_record is not None:
        for written in project_record.get_all("prompt_words"):
            item = split_item(written)
            if item.first and normalise_word(item.first) != "none" and item.get("use"):
                swaps.append((item.first.strip(), item.get("use").strip()))
    return swaps


def swap_prompt_words(text, swaps):
    """The text with every swap made once: a swap's target already in the text is kept as it is, so "a small steel
    vacuum flask" never becomes "a small steel vacuum small steel vacuum flask"."""
    text = str(text or "")
    kept = {}
    for number, (_, target) in enumerate(swaps):
        marker = f"\u0000{number}\u0000"
        pattern = re.compile(r"(?<!\w)" + re.escape(target) + r"(?!\w)", re.IGNORECASE)
        if pattern.search(text):
            text = pattern.sub(lambda match, key=marker: kept.setdefault(key, [])
                               .append(match.group(0)) or key, text)
    for source, target in swaps:
        text = re.sub(r"(?<!\w)" + re.escape(source) + r"(?!\w)", target, text, flags=re.IGNORECASE)
    for marker, originals in kept.items():
        for original in originals:
            text = text.replace(marker, original, 1)
    return text


def swap_sources_banned(swaps):
    """The swap sources a prompt may not hold: not one whose own target holds it ("flask" becomes "small steel
    vacuum flask", so "flask" inside the target is the user's own choice of words)."""
    return [source for source, target in swaps
            if not re.search(r"(?<!\w)" + re.escape(source) + r"(?!\w)", target, re.IGNORECASE)]


def object_from_scene(item):
    """The scene a set-plan object first stands in, when its material or meaning says so ("a tent ..., from scene
    29", "from SC29"), else None (there from the start)."""
    text = " ".join(str(item.get(key) or "") for key in ("material", "meaning"))
    match = re.search(r"\bfrom\s+(?:scene\s+(\d{1,3})([A-Z]?)\b|(SC\d{2,3}[A-Z]?)\b)", text, re.IGNORECASE)
    if not match:
        return None
    if match.group(3):
        return match.group(3).upper()
    return f"SC{int(match.group(1)):02d}{match.group(2) or ''}"


def text_must_be_read(text_record):
    """True when the audience must read a TEXT in picture, so its reading time counts in a floor: not when it is
    blurred into the background (method background_blur), and not when it is neither plot-critical nor given any
    emphasis (a shop sign seen in passing)."""
    if normalise_word(text_record.get("method") or "") == "background_blur":
        return False
    critical = normalise_word(text_record.get("plot_critical") or "") == "yes"
    return critical or (number_of(text_record.get("emphasis"), 0) or 0) > 0


def texts_shown_by(breakdown, shot, shot_lines):
    """[(TEXT ID, how it is shown)]: the texts a shot lists in `text` that the audience must read, and the
    plot-critical texts it shows without listing them (their thing is in the shot's thing, must_show or subject
    items, and the story line that writes their words is one of the shot's lines), so a reading floor is never
    missed on a visor or a wrist display. A shot that writes text: none says nothing in it is read (a monitor too
    small to read; the second full run, Project notes 39): it owes no time for such a text when the text's thing is
    at emphasis 0 or 1 and the shot's moments, purpose and why do not quote its words (its cross-examination: the
    F the scene is about, quoted in the shot, lost its floor)."""
    found = [(identifier, "listed") for identifier in breakdown.id_list(shot, "text")
             if breakdown.record(identifier, "TEXT") is not None
             and text_must_be_read(breakdown.record(identifier, "TEXT"))]
    text_none = shot.get("text") is not None and normalise_word(shot.get("text") or "") == "none"
    shown = set()
    for field_name in ("thing", "must_show", "subject"):
        for item in breakdown.items(shot, field_name):
            for piece in split_list(item.first or ""):
                shown.add(element_of(piece.strip()))
    if not shown or not shot_lines:
        return found
    for text_record in breakdown.records_of("TEXT"):
        identifier = text_record.identifier
        if any(identifier == listed for listed, _ in found) or identifier in breakdown.id_list(shot, "text"):
            continue
        if normalise_word(text_record.get("plot_critical") or "") != "yes" or not text_must_be_read(text_record):
            continue
        on = (text_record.get("on") or "").strip()
        if not on or (on not in shown and identifier not in shown):
            continue
        source = breakdown.item(text_record, "words_from")
        numbers = parse_line_numbers(source.first) if source is not None and source.first else None
        if not numbers or not any(first <= line <= last for first, last in numbers for line in shot_lines):
            continue
        if text_none and not text_featured_in_shot(breakdown, shot, text_record, on):
            continue
        found.append((identifier, f"shown on {on}"))
    return found


def text_featured_in_shot(breakdown, shot, text_record, on):
    """True when a shot that writes text: none still features an unlisted text: its thing is at emphasis 2 or more
    in the shot, or the shot's moments, purpose or why quote its words (capitals matched as written)."""
    for item in breakdown.items(shot, "thing"):
        if any(element_of(piece.strip()) in (on, text_record.identifier) for piece in split_list(item.first or "")) \
                and (number_of(item.get("emphasis"), 0) or 0) >= 2:
            return True
    words = (text_record.get("words") or "").strip().strip('"').strip()
    if not words or normalise_word(words) == "none":
        return False
    written = " ".join([shot.get("purpose") or "", shot.get("why") or ""]
                       + [item.get("shows") or "" for item in breakdown.items(shot, "moment")])
    capitals = words == words.upper() and re.search(r"[A-Z]", words)
    return bool(re.search(r"(?<!\w)" + re.escape(words) + r"(?!\w)", written, 0 if capitals else re.IGNORECASE))


def speech_word_list(text):
    """A speech's words for comparing parts of it: lower case, curly quotes straight, punctuation left out."""
    return re.findall(r"[a-z0-9']+", (text or "").lower().replace("\u2019", "'"))


def speech_words_part(part, whole):
    """True when part is a run of whole's words, in order, shorter than the whole (a speech split at a phrase)."""
    wanted, every = speech_word_list(part), speech_word_list(whole)
    if not wanted or len(wanted) >= len(every):
        return False
    return any(every[start:start + len(wanted)] == wanted for start in range(len(every) - len(wanted) + 1))


def speech_part(breakdown, speech_identifier, hear_words=None):
    """(speech ID, speaker, words, pace, seconds) for one heard speech, or None when its words are unknown."""
    extra = constant(breakdown.constants, "speech_floor_extra_s", 0.5)
    entry = breakdown.speech(speech_identifier)
    words = entry.get("words") if entry else None
    speaker = entry.get("speaker") if entry else None
    if words is None and hear_words:
        words = count_words(hear_words)
    elif hear_words and entry and speech_words_part(hear_words, entry.get("text") or ""):
        words = count_words(hear_words)  # a speech split at a phrase: this shot hears only these words
    if words is None or speaker is None:
        return None
    pace = breakdown.pace_of(speaker)
    return speech_identifier, speaker, int(words), pace, words / pace + extra


def time_floor(breakdown, shot):
    """The shot's time floor (5.6): max(speech_floor, text_floor) + pause_owed, from its real hear items."""
    key = ("time_floor", shot.identifier)
    if key in breakdown._cache:
        return breakdown._cache[key]
    extra = constant(breakdown.constants, "speech_floor_extra_s", 0.5)
    speech_parts = []
    unknown = []
    for item in breakdown.items(shot, "hear"):
        words = item.get("words")
        part = speech_part(breakdown, item.first, words.strip('"“”') if words else None)
        if part is None:
            unknown.append(item.first)
        else:
            speech_parts.append(part)
    speech_floor = sum(part[4] for part in speech_parts)
    shot_lines = set(breakdown.lines_of(shot))
    text_parts = []
    for text_identifier, shown_how in texts_shown_by(breakdown, shot, shot_lines):
        text_record = breakdown.record(text_identifier, "TEXT")
        mirrored = text_orientation(breakdown, text_identifier, shot) == "mirrored"
        seconds, how = text_reading_seconds(breakdown, text_record, mirrored)
        text_parts.append((text_identifier, seconds, how if shown_how == "listed" else f"{how}, {shown_how}"))
    text_floor = max((part[1] for part in text_parts), default=0.0)
    unresolved = [shot.identifier] if not shot_lines and lines_written(shot) else []
    pause_parts = []
    for beat_identifier in breakdown.id_list(shot, "beats"):
        beat = breakdown.record(beat_identifier, "BEAT")
        if beat is None:
            continue
        beat_numbers = breakdown.lines_of(beat)
        if not beat_numbers and lines_written(beat):
            unresolved.append(beat_identifier)
            continue
        # the pause after a beat is owed once, by the last shot that names the beat (the same rule as the
        # provisional floor of step 8's handout), never by every shot whose lines reach the beat's last line
        if last_shot_naming_beat(breakdown, beat_identifier) != shot.identifier:
            continue
        seconds, _, why = pause_seconds(breakdown, beat)
        pause_parts.append((beat_identifier, seconds, why))
    pause_owed = sum(part[1] for part in pause_parts)
    result = TimeFloor(shot.identifier, round_seconds(max(speech_floor, text_floor) + pause_owed),
                       round_seconds(speech_floor), round_seconds(text_floor), round_seconds(pause_owed),
                       speech_parts, text_parts, pause_parts, unknown)
    result.extra_per_speech_s = extra
    result.unresolved_lines = unresolved
    breakdown._cache[key] = result
    return result


def last_shot_naming_beat(breakdown, beat_identifier):
    """The last shot (in shot order) whose beats name this beat: written shots and list items together."""
    key = ("last_shot_naming_beat", beat_identifier)
    if key in breakdown._cache:
        return breakdown._cache[key]
    scene_identifier = scene_of(beat_identifier)
    naming = {shot.identifier for shot in breakdown.shots_of(scene_identifier)
              if beat_identifier in breakdown.id_list(shot, "beats")}
    for identifier, item in list_items(breakdown, scene_identifier):
        if identifier and beat_identifier in split_list(item.get("beats") or ""):
            naming.add(identifier.strip())
    found = max(naming, key=sort_key_for_identifier) if naming else None
    breakdown._cache[key] = found
    return found


class ListItemStandIn:
    """A list item read as a shot for text_orientation: its ID, and the lines of its first beat."""

    def __init__(self, identifier, lines):
        self.identifier = identifier
        self._lines = lines

    def get(self, name, default=None):
        return self._lines if name == "lines" else default


def lines_written(record):
    """True when a record writes lines (numbers or quote anchors), not none."""
    value = (record.get("lines") or "").strip() if record is not None else ""
    return bool(value) and normalise_word(value) != "none"


def list_items(breakdown, scene_identifier):
    """The scene's SHOTLIST items as (shot ID, Item), in list order."""
    shot_list = breakdown.record(f"{scene_identifier}-LIST", "SHOTLIST")
    if shot_list is None:
        return []
    return [(item.first, item) for item in breakdown.items(shot_list, "item")]


def quoted_strings(text):
    return [match.strip() for match in re.findall(r'["“]([^"“”]+)["”]', text or "")]


def provisional_floor(breakdown, scene_identifier, shot_identifier):
    """The provisional floor of one list item, printed in step 8's handout (5.6).

    Speeches: every speech whose cue lies in the item's beats. A speech in a beat that several list items share
    goes to the items whose one line quotes its words; when none quotes it, to every item sharing the beat (the
    floor is then an upper bound). Pause owed: each beat's pause counts on the last list item that names it,
    because the pause comes after the beat's last line.
    """
    items = list_items(breakdown, scene_identifier)
    by_shot = {identifier: item for identifier, item in items}
    item = by_shot.get(shot_identifier)
    if item is None:
        return None
    items_of_beat = {}
    for identifier, other in items:
        for beat_identifier in split_list(other.get("beats") or ""):
            items_of_beat.setdefault(beat_identifier, []).append(identifier)
    speech_parts = []
    unknown = []
    pause_parts = []
    shared = []
    beats_here = split_list(item.get("beats") or "")
    for beat_identifier in beats_here:
        beat = breakdown.record(beat_identifier, "BEAT")
        if beat is None:
            continue
        beat_lines = set(breakdown.lines_of(beat))
        sharing = items_of_beat.get(beat_identifier, [shot_identifier])
        for entry in breakdown.speeches_of_scene(scene_identifier):
            if entry is None or entry.get("line") not in beat_lines:
                continue
            if any(part[0] == entry["id"] for part in speech_parts):
                continue
            if len(sharing) > 1:
                quoting = [identifier for identifier in sharing
                           if any(quote and quote in (entry.get("text") or "")
                                  for quote in quoted_strings(by_shot[identifier].get("shows")))]
                if quoting and shot_identifier not in quoting:
                    continue
                if not quoting:
                    shared.append((entry["id"], [identifier for identifier in sharing if identifier != shot_identifier]))
            # an item that quotes part of the speech hears that part only, as its shot's hear words will say (the
            # second full run, Project notes 39: it was given the whole speech's floor)
            quoted = [quote for quote in quoted_strings(item.get("shows"))
                      if quote and speech_words_part(quote, entry.get("text") or "")]
            part = speech_part(breakdown, entry["id"], " ".join(quoted) if len(quoted) == 1 else None)
            if part is not None and len(quoted) > 1:
                words = sum(count_words(quote) for quote in quoted)
                part = (part[0], part[1], words, part[3],
                        words / part[3] + constant(breakdown.constants, "speech_floor_extra_s", 0.5))
            if part is None:
                unknown.append(entry["id"])
            else:
                speech_parts.append(part)
        if sharing and sharing[-1] == shot_identifier:
            seconds, _, why = pause_seconds(breakdown, beat)
            pause_parts.append((beat_identifier, seconds, why))
    speech_floor = sum(part[4] for part in speech_parts)
    pause_owed = sum(part[1] for part in pause_parts)
    text_parts = []
    shows = " ".join([item.get("shows") or "", item.get("subject") or ""])
    first_beat = breakdown.record(beats_here[0], "BEAT") if beats_here else None
    stand_in = ListItemStandIn(shot_identifier, first_beat.get("lines") if first_beat is not None else None)
    present = None
    for text_record in breakdown.records_of("TEXT"):
        if not text_must_be_read(text_record):
            continue
        words = (text_record.get("words") or "").strip().strip('"')
        named = text_record.identifier in shows or (words and any(
            quote and (re.search(r"(?<!\w)" + re.escape(words) + r"(?!\w)", quote) or quote in words)
            and len(quote) >= min(len(words), 4)
            for quote in quoted_strings(shows)))
        if named and text_record.identifier not in shows and len(words) <= 2:
            # one or two letters match many quotes: only a text on a thing that is in this scene counts
            if present is None:
                present = set(elements_present(breakdown, scene_identifier))
            named = element_of(text_record.get("on") or "") in present
        if not named:
            continue
        mirrored = text_orientation(breakdown, text_record.identifier, stand_in) == "mirrored"
        seconds, how = text_reading_seconds(breakdown, text_record, mirrored)
        text_parts.append((text_record.identifier, seconds, how))
    text_floor = max((part[1] for part in text_parts), default=0.0)
    result = TimeFloor(shot_identifier, round_seconds(max(speech_floor, text_floor) + pause_owed),
                       round_seconds(speech_floor), round_seconds(text_floor), round_seconds(pause_owed), speech_parts,
                       text_parts, pause_parts, unknown, provisional=True)
    result.extra_per_speech_s = constant(breakdown.constants, "speech_floor_extra_s", 0.5)
    result.shared_speeches = shared
    return result


# ---------------------------------------------------------------- clips and held takes (8.4)

@dataclass
class ClipPlan:
    """How a shot becomes generated clips on one model: lengths with handles, held or not, and any split."""
    shot: str
    screen_time: float
    needed_s: float
    held: bool
    held_reason: str
    model: str = None
    clip_lengths: list = dataclass_field(default_factory=list)
    fits: bool = True
    split_at: list = dataclass_field(default_factory=list)
    chained: bool = False
    models_allowing: list = dataclass_field(default_factory=list)
    note: str = ""

    @property
    def clip_s(self):
        return self.clip_lengths[0] if len(self.clip_lengths) == 1 else None

    def as_dict(self):
        return {"model": self.model, "screen_time_s": self.screen_time, "needed_s": self.needed_s,
                "held": self.held, "held_reason": self.held_reason, "clip_lengths_s": self.clip_lengths,
                "fits": self.fits, "split_at_s": self.split_at, "chained": self.chained,
                "models_allowing": self.models_allowing, "note": self.note}


def held_take(breakdown, shot):
    """(True, why) when the shot is a held take (8.4): a turn shot, a shot in a oner scene, or held: yes."""
    if normalise_word(shot.get("role") or "") in HELD_ROLES:
        return True, "a turn shot"
    scene = breakdown.record(scene_of(shot.identifier), "SCENE")
    if scene is not None and normalise_word(scene.get("coverage") or "") == "oner":
        return True, "a shot in a scene played in one take"
    if is_yes(shot.get("held")):
        return True, "marked held: yes"
    return False, ""


def allowed_lengths(model_facts):
    """The clip lengths a model allows, as a sorted list of seconds (from its length_s facts), or None."""
    if not model_facts:
        return None
    spec = model_facts.get("length_s") or {}
    if "allowed" in spec:
        return sorted(float(value) for value in spec["allowed"])
    if "min" in spec and "max" in spec:
        step = float(spec.get("step", 1) or 1)
        values = []
        value = float(spec["min"])
        while value <= float(spec["max"]) + 1e-9:
            values.append(round(value, 3))
            value += step
        return values
    return None


def round_up_to(needed, lengths):
    """The shortest allowed length at or above what is needed, or None."""
    for value in lengths:
        if value + 1e-9 >= needed:
            return value
    return None


def cut_points(breakdown, shot):
    """Planned cutaways inside a shot, in seconds: the start of every moment whose words name a cutaway."""
    points = []
    for item in breakdown.items(shot, "moment"):
        span = re.match(r"^\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*$", item.first or "")
        if span and re.search(r"\bcut ?away\b|\bcuts away\b", item.get("shows") or "", re.IGNORECASE):
            if float(span.group(1)) > 0:
                points.append(float(span.group(1)))
    return sorted(points)


def clip_plan(breakdown, shot, model=None, planned_cuts=None):
    """The shot's clips on one model (8.4): screen time + handles_s at each end, rounded up to a length the model
    allows. A held take is never split: when the model cannot hold it, the plan names the models that can. A shot
    that is not held is split only at planned cutaways (planned_cuts, else moments that name a cutaway); with none
    that fit, it is chained as a flagged last resort. With no model, lengths are whole seconds."""
    handles = constant(breakdown.constants, "handles_s", 0.75)
    screen_time = number_of(shot.get("screen_time"), 0.0)
    needed = round(screen_time + 2 * handles, 3)
    held, why_held = held_take(breakdown, shot)
    plan = ClipPlan(shot.identifier, screen_time, needed, held, why_held, model=model)
    longest_allowed = constant(breakdown.constants, "shot_screen_time_max_s", 600)
    if screen_time > longest_allowed:
        plan.fits = False
        plan.clip_lengths = []
        plan.note = (f"screen time {seconds_text(screen_time)} s is over the most one shot may last "
                     f"({seconds_text(longest_allowed)} s), so no clips were planned; check the value")
        return plan
    models = breakdown.models or {}
    lengths = allowed_lengths(models.get(model)) if model else None
    if lengths is None:
        plan.clip_lengths = [float(math.ceil(needed - 1e-9))]
        plan.note = "no model facts: whole seconds" if model else "no model chosen: whole seconds"
        return plan
    one = round_up_to(needed, lengths)
    if one is not None:
        plan.clip_lengths = [one]
        return plan
    plan.fits = False
    plan.models_allowing = sorted(name for name, facts in models.items()
                                  if round_up_to(needed, allowed_lengths(facts) or []) is not None)
    if held:
        plan.note = (f"a held take ({why_held}) of {seconds_text(needed)} s with handles is longer than {model} "
                     f"allows; route it whole to a model that allows it, never split (8.4)")
        return plan
    longest = max(lengths)
    points = sorted(planned_cuts if planned_cuts is not None else cut_points(breakdown, shot))
    pieces = []
    start = 0.0
    for point in points + [screen_time]:
        if point <= start:
            continue
        if point - start + 2 * handles <= longest + 1e-9:
            if pieces and pieces[-1][1] == start and (point - pieces[-1][0]) + 2 * handles <= longest + 1e-9:
                pieces[-1] = (pieces[-1][0], point)
            else:
                pieces.append((start, point))
            start = point
    if start >= screen_time - 1e-9 and pieces:
        plan.fits = True
        plan.split_at = [piece[1] for piece in pieces[:-1]]
        plan.clip_lengths = [round_up_to(piece[1] - piece[0] + 2 * handles, lengths) for piece in pieces]
        plan.note = "split at the planned cutaway" + ("s" if len(plan.split_at) > 1 else "")
        return plan
    count = math.ceil(screen_time / (longest - 2 * handles))
    share = screen_time / count
    plan.fits = True
    plan.chained = True
    plan.split_at = [round(share * index, 3) for index in range(1, count)]
    plan.clip_lengths = [round_up_to(share + 2 * handles, lengths)] * count
    plan.note = "no planned cutaway fits: chained from the last frame of the clip before, a flagged last resort"
    return plan


# ---------------------------------------------------------------- labels and counts

def label_letters(index):
    """1 -> A, 2 -> B, ... skipping I and O; after the 24th letter, AA, BB and so on."""
    count = len(LABEL_LETTERS)
    letter = LABEL_LETTERS[(index - 1) % count]
    return letter * ((index - 1) // count + 1)


def crew_label(identifier):
    """The crew label of a shot, used only in the shot-list spreadsheet: SC10-SH150 -> 10Q (5.3)."""
    scene = scene_of(identifier) or ""
    scene_number = re.sub(r"^SC0*", "", scene) or "0"
    number = shot_number(identifier)
    if number is None:
        return None
    if number >= 990:
        return f"{scene_number} card {number - 989}"
    base, rest = divmod(number, 10)
    label = f"{scene_number}{label_letters(base)}" if base > 0 else f"{scene_number}0"
    return label + (str(rest) if rest else "")


def scene_label(breakdown, scene_identifier):
    """The scene's plain name in views: 'Scene 10 - Saye's kitchen' (from its place's title)."""
    scene = breakdown.record(scene_identifier, "SCENE")
    number = re.sub(r"^SC0*", "", scene_identifier or "") or "0"
    place = ""
    location = breakdown.record(scene.get("location"), "LOCATION") if scene is not None else None
    if location is not None and location.title:
        place = location.title
    elif scene is not None and scene.get("place_text"):
        text = scene.get("place_text").split(" - ")[-1].strip().lower()
        place = text[:1].upper() + text[1:]
    return f"Scene {number} - {place}" if place else f"Scene {number}"


def scene_duration(breakdown, scene_identifier):
    """The scene's length from its shots (screen time, plus black frames written on cuts), else its list items."""
    shots = breakdown.shots_of(scene_identifier)
    fps = number_of(breakdown.project.get("fps") if breakdown.project else None, 24.0) or 24.0
    if shots:
        total = sum(number_of(shot.get("screen_time"), 0.0) for shot in shots)
        total += sum(number_of(cut.get("black_frames"), 0.0) / fps for cut in breakdown.of_scene("CUT", scene_identifier))
        return round_seconds(total)
    items = list_items(breakdown, scene_identifier)
    if items:
        return round_seconds(sum(number_of(item.get("time"), 0.0) for _, item in items))
    return None


def speaking_counts(breakdown, scene_identifier):
    """{character: {"speeches": n, "words": n}} for the scene, from its speeches."""
    counts = {}
    for entry in breakdown.speeches_of_scene(scene_identifier):
        if not entry:
            continue
        speaker = entry.get("speaker")
        slot = counts.setdefault(speaker, {"speeches": 0, "words": 0})
        slot["speeches"] += 1
        slot["words"] += int(entry.get("words") or 0)
    return counts


def coverage_map(breakdown, scene_identifier):
    """Which shots cover each story line, beat and speech of the scene (list items when there are no shots)."""
    lines = {}
    beats = {}
    speeches = {}
    shots = breakdown.shots_of(scene_identifier)
    for shot in shots:
        for number in breakdown.lines_of(shot):
            lines.setdefault(number, []).append(shot.identifier)
        for beat_identifier in breakdown.id_list(shot, "beats"):
            beats.setdefault(beat_identifier, []).append(shot.identifier)
        for item in breakdown.items(shot, "hear"):
            speeches.setdefault(item.first, []).append(shot.identifier)
    if not shots:
        for identifier, item in list_items(breakdown, scene_identifier):
            for beat_identifier in split_list(item.get("beats") or ""):
                beats.setdefault(beat_identifier, []).append(identifier)
    return {"lines": lines, "beats": beats, "speeches": speeches}


def speech_word_counts(breakdown, scene_identifier):
    """{speech ID: words} for every speech of the scene (derived SPEECH word_count; screenplay speeches too)."""
    return {entry["id"]: int(entry.get("words") or 0) for entry in breakdown.speeches_of_scene(scene_identifier)
            if entry}


# Line types of the numbered story that a formatted page sets at the narrow dialogue width.
DIALOGUE_WIDTH_TYPES = ("cue", "dialogue", "parenthetical")


def scene_eighths(breakdown, scene_identifier):
    """(eighths, how) of a scene's length on the page, by A3 §5.2's line-count model (page_eighths_line_model):
    each line of the numbered story wrapped at the action or dialogue width, blank lines kept, pages of
    lines_per_page lines, rounded up to the next eighth and never under minimum_eighths. Only a formatted page gives
    true eighths, so this is an estimate. (None, why) when the story's lines are not present."""
    model = constant(breakdown.constants, "page_eighths_line_model", None)
    scope = breakdown.scene_range(scene_identifier)
    story = breakdown.story
    if not model or scope is None or story is None or not (story.first <= scope[0] and scope[1] <= story.last):
        return None, "needs the scene's story lines and the page line model"
    page_lines = 0
    for number in range(scope[0], scope[1] + 1):
        text = story.line(number).strip()
        if not text:
            page_lines += 1
            continue
        text = text.lstrip("#>= ").strip()
        width = (model["dialogue_characters_per_line"] if story.type_of(number) in DIALOGUE_WIDTH_TYPES
                 else model["action_characters_per_line"])
        page_lines += max(1, math.ceil(len(text) / width))
    eighths = math.ceil(page_lines * model["eighths_per_page"] / model["lines_per_page"] - 1e-9)
    eighths = max(model.get("minimum_eighths", 1), eighths)
    per_page = model["eighths_per_page"]
    pages, rest = divmod(eighths, per_page)
    if not pages:
        plain = f"{rest}/{per_page} of a page"
    elif not rest:
        plain = f"{pages} page{'s' if pages != 1 else ''}"
    else:
        plain = f"{pages} {rest}/{per_page} pages"
    return eighths, f"{plain} ({page_lines} page lines, an estimate from the line count)"


# The light, colour and darkness words stage.py read finds (read_story.LIGHT_WORDS) are read in their sentence
# before they count: a colour that describes a person ("DR SAYE, fifties, grey and tidy", "grey hair") and a word
# inside a name for something that gives no light ("the fire door", "open fire") are not light (B2 P2 is about
# light). COVER-08 and the beats the script marks (CRAFT-10, CRAFT-19) both read them through light_words_in_context.
COLOUR_WORDS_OF_LIGHT = {"red", "green", "blue", "yellow", "orange", "white", "black", "grey", "gray", "gold",
                         "golden", "silver", "amber", "purple", "violet", "pink", "brown", "pale"}
PERSON_WORDS = {"hair", "hairs", "beard", "moustache", "eyes", "eye", "skin", "face", "lips", "cheeks", "brows",
                "eyebrows", "suit", "coat", "coats", "uniform", "scrubs", "gown", "dress", "shirt", "jacket",
                "overalls", "tie", "shoes", "boots", "gloves", "hat", "cap", "teeth", "temples", "stubble"}
NOT_LIGHT_PHRASES = re.compile(
    r"\bfire[- ](?:door|doors|shutter|shutters|curtain|wall|walls|stairs|stair|exit|exits|escape|alarm|alarms|"
    r"extinguisher|hose|brigade|station|drill)\b|"
    r"\b(?:open|opens|opened|opening|return|returns|returned|cease|hold|holds|held|under|crossfire|gun)\s+fire\b|"
    r"\bgunfire\b", re.IGNORECASE)
PERSON_INTRODUCTION = re.compile(r"(?:^|[.!?]\s+)((?:[A-Z][A-Z'.-]*\s?){1,4}),([^.!?]*)")


# How a light word reads in its sentence: at rest, or changing or moving (COVER-08 asks a light cue for the
# second; script_marked counts only the second as the script marking a beat with light).
LIGHT_BRIGHTNESS_WORDS = {"light", "lit", "bright", "brightness", "dim", "pale", "glow", "glows",
                          "glowing", "beam", "beams", "shine", "shines", "shining", "glint", "gleam", "glare"}
LIGHT_CHANGE_WORDS = {"dims", "flicker", "flickers", "flash", "flashes", "flare", "blaze", "strobe", "lightning",
                      "blinding"}
LIGHT_MOVING_WORDS = {"goes", "go", "going", "went", "gone", "out", "off", "dies", "died", "dying", "fades", "fade",
                      "fading", "faded", "dimmed", "dimming", "brightens", "brightened", "floods", "flood", "flooded",
                      "sweeps", "sweep", "swept", "swings", "swing", "swinging", "swung", "comes", "came", "onto",
                      "across", "up", "brings", "bring", "brought", "raises", "raise", "raised", "lifts", "lift",
                      "lifted", "holds", "hold", "held", "points", "pointed", "turns", "turned", "moves", "moved",
                      "passes", "passed", "falls", "fell", "spills", "spilled", "catches", "caught", "snaps",
                      "switches", "switched", "clicks", "blinks", "sparks", "rises", "rose", "drops", "dropped",
                      "returns", "returned", "kills", "killed", "blows", "cuts", "cut", "stutters", "pulses",
                      "carries", "carried", "carrying", "shifts", "shifted", "slides", "slid", "trails"}


# A word that moves a light counts only this near it, in words: "comes round the cage with the torch" moves the
# torch; "a screw rises off the deck beside her boot and hangs in her lamplight" does not move the lamplight.
LIGHT_MOVING_NEAR = 6
LIGHT_AS_PLACE = re.compile(r"\b(?:to|into|towards?|in|under)\s+(?:the|her|his|their|its)\s+$")


def light_moves_in(sentence, word=None):
    """True when a sentence of the story changes or moves its light (see the note above COVER-08's words). A light
    that things move into or towards ("turns the tag to the light", "comes into the light") and a brightness word
    that describes a surface ("the bright steel") are light at rest, unless a word of change is there too."""
    lowered = (sentence or "").lower()
    words = re.findall(r"[a-z]+", lowered)
    if any(found in LIGHT_CHANGE_WORDS for found in words):
        return True
    light_words = [found for found in words if found in LIGHT_BRIGHTNESS_WORDS]
    if len(light_words) != len(set(light_words)):
        return True
    if word:
        match = re.search(r"\b" + re.escape(word) + r"\b", lowered)
        if match:
            after = re.findall(r"[a-z]+", lowered[match.end():])
            if LIGHT_AS_PLACE.search(lowered[:match.start()]):
                return False
            if word in LIGHT_BRIGHTNESS_WORDS and word not in ("light", "glow", "beam", "beams") and after and \
                    after[0] not in LIGHT_BRIGHTNESS_WORDS and after[0] not in LIGHT_MOVING_WORDS:
                return False  # "the bright steel": the word describes a thing's surface
    if word:
        positions = [number for number, found in enumerate(words) if found == word]
        return any(found in LIGHT_MOVING_WORDS and any(abs(number - at) <= LIGHT_MOVING_NEAR for at in positions)
                   for number, found in enumerate(words))
    return any(found in LIGHT_MOVING_WORDS for found in words)



def light_words_in_context(text, words):
    """The words of a story line's light words that are light in this line: colours describing a person and words
    inside a name for something that gives no light are left out."""
    text = text or ""
    lowered = text.lower()
    blocked = set()
    for match in NOT_LIGHT_PHRASES.finditer(text):
        blocked.update(word.lower() for word in re.findall(r"[A-Za-z]+", match.group(0)))
    introductions = [match.span(2) for match in PERSON_INTRODUCTION.finditer(text)
                     if len(re.sub(r"[^A-Z]", "", match.group(1))) >= 2]
    tokens = [(match.group(0).lower(), match.start()) for match in re.finditer(r"[A-Za-z]+", text)]
    kept = []
    for word in words or []:
        word = word.lower()
        if word in blocked and word in ("fire", "gunfire"):
            continue
        if word in COLOUR_WORDS_OF_LIGHT:
            places = [position for position, (token, _) in enumerate(tokens) if token == word]
            about_person = False
            for position in places:
                near = [token for token, _ in tokens[position + 1:position + 3]] + \
                       [token for token, _ in tokens[max(0, position - 2):position]]
                start = tokens[position][1]
                if any(token in PERSON_WORDS for token in near) or \
                        any(first <= start < last for first, last in introductions):
                    about_person = True
            if about_person:
                continue
        kept.append(word)
    return kept


def sentence_with_word(text, word):
    """The sentence of a story line that holds a word (the whole line when none does)."""
    for sentence in re.split(r"(?<=[.!?])\s+", (text or "").strip()):
        if word.lower() in {found.lower() for found in re.findall(r"[A-Za-z]+", sentence)}:
            return sentence
    return text or ""


def script_marked(breakdown, beat):
    """(yes or no, what marks it): a beat is marked by the script when its lines hold a capitalised sound, emphasis
    or text token, or a light, colour or darkness word that stage.py read found and that is light in its sentence
    (light_words_in_context; derived BEAT script_marked; CRAFT-10 and added_emphasis_per_beat_max read it). None when
    the story map is not present."""
    scenes = (breakdown.story_map or {}).get("scenes") or []
    scene_identifier = scene_of(beat.identifier)
    scene = next((entry for entry in scenes if entry.get("id") == scene_identifier), None)
    if scene is None:
        return None, "needs the story map that stage.py read writes"
    lines = set(breakdown.lines_of(beat))
    marks = []
    for token in scene.get("capitalised_words") or []:
        if token.get("line") in lines and token.get("class") in ("sound", "emphasis", "text"):
            marks.append(f'{token["class"]} "{token["text"]}" (line {token["line"]})')
    for entry in scene.get("light_lines") or []:
        if entry.get("line") in lines:
            words = entry.get("words") or []
            if breakdown.story is not None:
                line_text = breakdown.story.line(entry["line"])
                # a light at rest ("hangs in her lamplight") marks nothing; a light that changes or moves does
                words = [word for word in light_words_in_context(line_text, words)
                         if light_moves_in(sentence_with_word(line_text, word), word)]
            if words:
                marks.append(f'light words {", ".join(words)} (line {entry["line"]})')
    return ("yes" if marks else "no"), "; ".join(marks)


# ---------------------------------------------------------------- the mirror world: eras and frames (5.6, K03)

@dataclass
class Era:
    """A stretch of the film under one frame handedness, from the mirror RULE's era lines."""
    name: str
    first: int
    last: int
    frame: str

    def holds(self, line):
        return line is not None and self.first <= line <= self.last


@dataclass
class SceneEra:
    """A scene's era and frame handedness, and the line where it switches to the next era, if it does."""
    scene: str
    era: str
    frame: str
    switch_at: int = None
    next_era: str = None
    next_frame: str = None

    def as_dict(self):
        found = {"era": self.era, "frame_handedness": self.frame}
        if self.switch_at is not None:
            found.update({"switch_at": self.switch_at, "era_after_switch": self.next_era,
                          "frame_after_switch": self.next_frame})
        return found


def mirror_rule(breakdown):
    """The story's mirror RULE (kind mirror), or None."""
    for rule in breakdown.records_of("RULE"):
        if normalise_word(rule.get("kind") or "") == "mirror":
            return rule
    return None


def eras(breakdown):
    """The eras of the mirror rule, in line order. Era lines may be numbers or quote anchors (an era's from names
    its line; its to runs to the end of the quote's speech, as the adopt rule says)."""
    key = ("eras",)
    if key in breakdown._cache:
        return breakdown._cache[key]
    found = []
    unresolved = []
    rule = mirror_rule(breakdown)
    for item in breakdown.items(rule, "era") if rule is not None else []:
        first = breakdown.line_reference(item.get("from"))
        last_value = item.get("to")
        last = None
        if last_value:
            ranges = parse_line_numbers(last_value)
            if ranges:
                last = ranges[-1][1]
            elif breakdown.story is not None:
                resolved = breakdown.story.resolve_lines(last_value)
                last = resolved[1] if resolved else None
        if first is None or last is None:
            unresolved.append(normalise_word(item.first or "") or "?")
            continue
        found.append(Era(normalise_word(item.first or ""), first, last,
                         normalise_word(item.get("frame") or "original")))
    found.sort(key=lambda era: era.first)
    breakdown._cache[key] = found
    breakdown._cache[("eras_unresolved",)] = unresolved
    return found


def eras_unresolved(breakdown):
    """The mirror rule's eras whose lines could not be found (quote anchors outside the story given, or no story).
    While any is unresolved, mirror states are 'open': code does not guess which elements are mirrored."""
    eras(breakdown)
    return breakdown._cache.get(("eras_unresolved",), [])


def era_at(breakdown, line):
    """The era that holds a line (the one before it when the line falls in a gap between eras), or None."""
    if line is None:
        return None
    before = None
    for era in eras(breakdown):
        if era.holds(line):
            return era
        if era.first <= line:
            before = era
    return before


def frame_at(breakdown, line):
    era = era_at(breakdown, line)
    return era.frame if era else "original"


def scene_era(breakdown, scene_identifier):
    """The scene's era and frame (from its first line), and switch_at when another era starts inside it."""
    key = ("scene_era", scene_identifier)
    if key in breakdown._cache:
        return breakdown._cache[key]
    scope = breakdown.scene_range(scene_identifier)
    result = None
    if scope and eras(breakdown):
        first_era = era_at(breakdown, scope[0])
        result = SceneEra(scene_identifier, first_era.name if first_era else None,
                          first_era.frame if first_era else "original")
        for era in eras(breakdown):
            if scope[0] < era.first <= scope[1] and (first_era is None or era.name != first_era.name):
                result.switch_at = era.first
                result.next_era = era.name
                result.next_frame = era.frame
                break
    elif eras(breakdown) == []:
        result = SceneEra(scene_identifier, None, "original")
    breakdown._cache[key] = result
    return result


def shot_first_line(breakdown, shot):
    numbers = breakdown.lines_of(shot)
    if numbers:
        return numbers[0]
    scope = breakdown.scene_range(scene_of(shot.identifier))
    return scope[0] if scope else None


def shot_era(breakdown, shot):
    """The era a shot is in: the era of its first line (after a mid-scene switch, the new era)."""
    line = shot_first_line(breakdown, shot)
    era = era_at(breakdown, line)
    return era


# ---------------------------------------------------------------- states, handedness and mirror states

def state_from(breakdown, state):
    """(scene, line) where a STATE starts: its from item's scene and line (a number or a quote in that scene)."""
    item = breakdown.item(state, "from")
    if item is None:
        return None, None
    scene_identifier = item.first
    line = breakdown.line_reference(item.get("line"), scene_identifier) if item.get("line") else None
    if line is None and scene_identifier:
        scope = breakdown.scene_range(scene_identifier)
        line = scope[0] if scope else None
    return scene_identifier, line


def states_of(breakdown, element):
    """The STATE records of one element, in the order they start."""
    key = ("states_of", element)
    if key not in breakdown._cache:
        found = [state for state in breakdown.records_of("STATE") if (state.get("element") or element_of(state.identifier)) == element]
        found.sort(key=lambda state: (state_from(breakdown, state)[1] is None, state_from(breakdown, state)[1] or 0,
                                      sort_key_for_identifier(state.identifier)))
        breakdown._cache[key] = found
    return breakdown._cache[key]


def state_until(breakdown, state):
    """(scene, line) where the next state of the same element starts (derived STATE until), or (None, None)."""
    element = state.get("element") or element_of(state.identifier)
    found = states_of(breakdown, element)
    for index, other in enumerate(found):
        if other.identifier == state.identifier and index + 1 < len(found):
            return state_from(breakdown, found[index + 1])
    return None, None


def state_valid_at(breakdown, element, line):
    """The state of an element valid at a line: the last one starting at or before it (else the first)."""
    found = states_of(breakdown, element)
    if not found:
        return None
    chosen = None
    for state in found:
        start = state_from(breakdown, state)[1]
        if start is not None and line is not None and start <= line:
            chosen = state
    return chosen or found[0]


def state_of_reference(breakdown, reference, line=None):
    """The STATE a subject or thing item names: the state itself, or the element's state valid at the line."""
    if not reference:
        return None
    record = breakdown.record(reference, "STATE")
    if record is not None:
        return record
    return state_valid_at(breakdown, element_of(reference), line)


def handedness_of(state):
    """original or reversed (a state that does not say is original)."""
    value = normalise_word(state.get("handedness") or "") if state is not None else ""
    return value if value in ("original", "reversed") else "original"


def mirror_state_at(breakdown, reference, line):
    """mirrored when the element's state handedness differs from the frame's at that line, else normal (5.6);
    open while the mirror rule's era lines cannot be found."""
    if eras_unresolved(breakdown):
        return "open"
    if not eras(breakdown):
        return "normal"
    state = state_of_reference(breakdown, reference, line)
    return "mirrored" if handedness_of(state) != frame_at(breakdown, line) else "normal"


def scene_location(breakdown, scene_identifier):
    scene = breakdown.record(scene_identifier, "SCENE")
    return scene.get("location") if scene is not None else None


def elements_in_shot(breakdown, shot):
    """The elements a shot shows: its subjects and things (element states and elements; not motifs or text)."""
    found = []
    for field_name in ("subject", "thing"):
        for item in breakdown.items(shot, field_name):
            reference = item.first
            if not reference or reference.startswith(("MO-", "TX-")):
                continue
            if reference not in found:
                found.append(reference)
    return found


def shot_mirror_states(breakdown, shot):
    """{element: {"state", "handedness", "mirror_state"}} for every element in frame and the scene's place."""
    key = ("shot_mirror_states", shot.identifier)
    if key in breakdown._cache:
        return breakdown._cache[key]
    line = shot_first_line(breakdown, shot)
    result = {}
    references = elements_in_shot(breakdown, shot)
    location = scene_location(breakdown, scene_of(shot.identifier))
    if location and normalise_word(shot.get("kind") or "") not in ("card", "black"):
        references.append(location)
    for reference in references:
        state = state_of_reference(breakdown, reference, line)
        result[element_of(reference)] = {"state": state.identifier if state is not None else None,
                                         "handedness": handedness_of(state),
                                         "mirror_state": mirror_state_at(breakdown, reference, line)}
    breakdown._cache[key] = result
    return result


def elements_present(breakdown, scene_identifier):
    """Every element present in a scene: its characters and place, and every element its shots show."""
    key = ("elements_present", scene_identifier)
    if key in breakdown._cache:
        return breakdown._cache[key]
    found = []
    scene = breakdown.record(scene_identifier, "SCENE")
    if scene is not None:
        found += breakdown.id_list(scene, "characters")
        if scene.get("location"):
            found.append(scene.get("location"))
    for shot in breakdown.shots_of(scene_identifier):
        found += [element_of(reference) for reference in elements_in_shot(breakdown, shot)]
    for state in breakdown.records_of("STATE"):
        if state_from(breakdown, state)[0] == scene_identifier:
            found.append(state.get("element") or element_of(state.identifier))
    unique = []
    for element in found:
        if element and element not in unique:
            unique.append(element)
    breakdown._cache[key] = unique
    return unique


def states_in_play(breakdown, scene_identifier, more_elements=()):
    """The states valid in a scene for the elements present in it (derived SCENE states_in_play); more_elements adds
    elements a handout found by name in the scene's lines."""
    scope = breakdown.scene_range(scene_identifier)
    if scope is None:
        return []
    found = []
    elements = list(elements_present(breakdown, scene_identifier))
    elements += [element for element in more_elements if element not in elements]
    for element in elements:
        for state in states_of(breakdown, element):
            start = state_from(breakdown, state)[1]
            end = state_until(breakdown, state)[1]
            if start is not None and start > scope[1]:
                continue
            if end is not None and end <= scope[0]:
                continue
            found.append(state.identifier)
    return found


def scene_mirror_states(breakdown, scene_identifier):
    """{element: mirror state} at the scene's first line for every element present (and after a switch)."""
    scope = breakdown.scene_range(scene_identifier)
    if scope is None:
        return {}
    era = scene_era(breakdown, scene_identifier)
    result = {}
    for element in elements_present(breakdown, scene_identifier):
        result[element] = mirror_state_at(breakdown, element, scope[0])
        if era is not None and era.switch_at is not None:
            result[element + " after the switch"] = mirror_state_at(breakdown, element, era.switch_at)
    return result


def element_orientations(breakdown, element):
    """The mirror states an element is seen in across the film: from every scene where it is present, or, when the
    records place it in no scene, from each of its states against each era it overlaps."""
    key = ("orientations", element)
    if key in breakdown._cache:
        return breakdown._cache[key]
    seen = set()
    for scene_identifier in breakdown.scene_identifiers():
        if element not in elements_present(breakdown, scene_identifier):
            continue
        scope = breakdown.scene_range(scene_identifier)
        if scope is None:
            continue
        seen.add(mirror_state_at(breakdown, element, scope[0]))
        era = scene_era(breakdown, scene_identifier)
        if era is not None and era.switch_at is not None:
            seen.add(mirror_state_at(breakdown, element, era.switch_at))
    if not seen:
        for state in states_of(breakdown, element):
            start = state_from(breakdown, state)[1] or 0
            end = state_until(breakdown, state)[1]
            for era in eras(breakdown):
                if era.last >= start and (end is None or era.first < end):
                    seen.add("mirrored" if handedness_of(state) != era.frame else "normal")
    if not eras(breakdown):
        seen = {"normal"}
    breakdown._cache[key] = seen
    return seen


def location_orientation(breakdown, location):
    """single when the place is seen in one mirror state only, both otherwise (derived LOCATION orientation)."""
    if eras_unresolved(breakdown):
        return "open"
    seen = element_orientations(breakdown, location)
    return "single" if len(seen) <= 1 else "both"


def rules_governing(breakdown, identifiers):
    found = []
    for rule in breakdown.records_of("RULE"):
        governed = set(breakdown.id_list(rule, "governs"))
        exceptions = {item.first for item in breakdown.items(rule, "exception")}
        if governed & set(identifiers) or exceptions & set(identifiers):
            found.append(rule)
    return found


# Title cards and captions are laid over the finished film and never mirrored (D12 rule 17), in every era; the text
# graphics tool draws them the same way (make_text_graphics.NEVER_MIRRORED_DEFAULT).
NEVER_MIRRORED_TEXT_KINDS = ("title_card", "caption")


def text_orientation(breakdown, text_identifier, shot):
    """normal or mirrored for one TEXT in a shot: a title card or caption always reads normally; a rule exception
    that names it decides; a titles rule reads it normally; otherwise it follows the thing it is on. Text on nothing
    that a text rule governs (a street sign) follows the world, the scene's place; other text on nothing follows the
    frame."""
    text_record = breakdown.record(text_identifier, "TEXT")
    if text_record is None:
        return None
    if normalise_word(text_record.get("kind") or "") in NEVER_MIRRORED_TEXT_KINDS:
        return "normal"
    on = text_record.get("on")
    on = None if not on or normalise_word(on) == "none" else on
    world_text = False
    for rule in rules_governing(breakdown, [text_identifier] + ([on] if on else [])):
        for item in breakdown.items(rule, "exception"):
            if item.first == text_identifier and item.get("reads"):
                return normalise_word(item.get("reads"))
        if normalise_word(rule.get("kind") or "") == "titles" and text_identifier in breakdown.id_list(rule, "governs"):
            return "normal"
        if normalise_word(rule.get("kind") or "") == "text" and text_identifier in breakdown.id_list(rule, "governs"):
            world_text = True
    line = shot_first_line(breakdown, shot)
    if on:
        return mirror_state_at(breakdown, on, line)
    place = scene_location(breakdown, scene_of(getattr(shot, "identifier", None))) if world_text else None
    if place:
        # The second full run (Project notes 39): a bus number on nothing read normally in the mirrored era.
        return mirror_state_at(breakdown, place, line)
    return "mirrored" if frame_at(breakdown, line) == "reversed" else "normal"


def text_has_orientation_rule(breakdown, text_identifier):
    """True when a RULE names the text (or the thing it is on) in governs or as an exception (SIDE-05)."""
    text_record = breakdown.record(text_identifier, "TEXT")
    on = text_record.get("on") if text_record is not None else None
    references = [text_identifier] + ([on] if on and normalise_word(on) != "none" else [])
    return bool(rules_governing(breakdown, references))


# ---------------------------------------------------------------- geometry: set plans and cameras (5.6)

@dataclass
class SetPlan:
    """A place's set plan in metres (5.5 LOCATION), as stored or turned to the other orientation (x -> W - x)."""
    location: str
    width: float
    depth: float
    height: float
    orientation: str
    marks: dict
    objects: dict
    wild_walls: str = ""
    turned: bool = False
    mark_heights: dict = dataclass_field(default_factory=dict)

    def x(self, value):
        return self.width - value if self.turned else value

    def place(self, point):
        """A stored point (2D or 3D) in this plan's orientation."""
        if point is None:
            return None
        return (self.x(point[0]),) + tuple(point[1:])

    def object_point(self, name, top=False):
        found = self.objects.get(name)
        if not found:
            return None
        x, y = found["at"][0], found["at"][1]
        height = found["size"][2] if found.get("size") and len(found["size"]) > 2 else 0.0
        z = found.get("base", 0.0) + (height if top else height / 2)
        return (x, y, z)

    def contains(self, point):
        return (point is not None and -1e-9 <= point[0] <= self.width + 1e-9
                and -1e-9 <= point[1] <= self.depth + 1e-9)

    def surface_under(self, point):
        """The top of the object under a floor point (a table a person lies on), or None."""
        best = None
        for found in self.objects.values():
            size = found.get("size") or ()
            if len(size) < 3:
                continue
            centre = found["at"]
            if abs(point[0] - centre[0]) <= size[0] / 2 + 1e-9 and abs(point[1] - centre[1]) <= size[1] / 2 + 1e-9:
                top = found.get("base", 0.0) + size[2]
                best = top if best is None else max(best, top)
        return best


def set_plan(breakdown, location_identifier):
    """The LOCATION's set plan (size and marks or objects), in its stored orientation, or None."""
    key = ("set_plan", location_identifier)
    if key in breakdown._cache:
        return breakdown._cache[key]
    location = breakdown.record(location_identifier, "LOCATION")
    result = None
    size = point_of(location.get("size")) if location is not None else None
    if location is not None and size and len(size) >= 2:
        marks = {}
        heights = {}
        for item in breakdown.items(location, "mark"):
            point = point_of(item.get("at"))
            if point:
                marks[item.first] = point[:2]
                if len(point) > 2:
                    heights[item.first] = point[2]  # a vertical plan: the height the person stands at (C11)
        objects = {}
        for item in breakdown.items(location, "object"):
            point = point_of(item.get("at"))
            if point:
                objects[item.first] = {"at": point[:2], "size": point_of(item.get("size")) or (),
                                       "base": number_of(item.get("base"), 0.0),
                                       "furniture": normalise_word(item.get("furniture") or "none"),
                                       "from_scene": object_from_scene(item)}
        if marks or objects:
            orientation = normalise_word(location.get("plan_orientation") or "original")
            result = SetPlan(location_identifier, size[0], size[1], size[2] if len(size) > 2 else 2.5,
                             orientation if orientation in ("original", "reversed") else "original",
                             marks, objects, location.get("wild_walls") or "", mark_heights=heights)
    breakdown._cache[key] = result
    return result


def plan_for_shot(breakdown, shot):
    """The set plan of the shot's place in the orientation the shot needs: the place as it appears on screen
    (reversed when its mirror state is mirrored, original when normal), turned from the stored orientation by
    x -> W - x when the two differ (5.4 rule 7, 5.6)."""
    location = scene_location(breakdown, scene_of(shot.identifier))
    stored = set_plan(breakdown, location) if location else None
    if stored is None:
        return None
    line = shot_first_line(breakdown, shot)
    state = mirror_state_at(breakdown, location, line)
    needed = stored.orientation if state == "open" else ("reversed" if state == "mirrored" else "original")
    if needed == stored.orientation:
        return stored
    return SetPlan(stored.location, stored.width, stored.depth, stored.height, needed, stored.marks,
                   stored.objects, stored.wild_walls, turned=True, mark_heights=stored.mark_heights)


def vector(a, b):
    return tuple(b[index] - a[index] for index in range(len(a)))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def length(a):
    return math.sqrt(dot(a, a))


def unit(a):
    size = length(a)
    return tuple(value / size for value in a) if size > 1e-12 else a


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


@dataclass
class Camera:
    """One setup's camera: position, the point it looks at, the lens, and the frame's shape."""
    setup: str
    position: tuple
    look_at: tuple
    lens_mm: float
    ratio: float
    sensor_mm: float = 36.0

    def __post_init__(self):
        self.forward = unit(vector(self.position, self.look_at))
        right = cross(self.forward, (0.0, 0.0, 1.0))
        if length(right) < 1e-9:
            right = (1.0, 0.0, 0.0)
        self.right = unit(right)
        self.up = cross(self.right, self.forward)
        self.half_width = (self.sensor_mm / 2) / self.lens_mm
        self.half_height = self.half_width / self.ratio

    def project(self, point):
        """(u, v, depth): u from -1 (left edge) to +1 (right edge), v from -1 (bottom) to +1 (top)."""
        offset = vector(self.position, point if len(point) == 3 else (point[0], point[1], self.position[2]))
        depth = dot(offset, self.forward)
        if depth <= 1e-9:
            return None, None, depth
        return (dot(offset, self.right) / depth / self.half_width,
                dot(offset, self.up) / depth / self.half_height, depth)

    def side_of_direction(self, direction):
        """Which way a floor direction points in the picture: + toward frame right, - toward frame left."""
        flat = (direction[0], direction[1], 0.0)
        return dot(flat, self.right)

    def toward_camera(self, direction):
        flat = (direction[0], direction[1], 0.0)
        return -dot(flat, self.forward)

    def visible_height_at(self, depth):
        """Visible height of the frame at a depth: (36 / lens_mm x distance) / frame ratio (5.6)."""
        return (self.sensor_mm / self.lens_mm * depth) / self.ratio


def frame_ratio(breakdown):
    value = breakdown.project.get("frame_shape") if breakdown.project else None
    word = normalise_word(value or "2.39").replace(":", "_")
    if word in FRAME_RATIOS:
        return FRAME_RATIOS[word]
    parts = re.split(r"[_:x]", word)
    if len(parts) == 2 and all(part.replace(".", "").isdigit() for part in parts):
        return float(parts[0]) / float(parts[1])
    return number_of(word, 2.39) or 2.39


def camera_for(breakdown, shot, plan=None):
    """The shot's camera from its setup (turned with the plan when the shot needs the other orientation)."""
    setup = breakdown.record(shot.get("setup"), "SETUP") if shot.get("setup") else None
    if setup is None:
        return None
    position = point_of(setup.get("at"))
    look_at = point_of(setup.get("look_at"))
    if not position or not look_at or len(position) < 3 or len(look_at) < 2:
        return None
    if len(look_at) == 2:
        look_at = (look_at[0], look_at[1], position[2])
    if plan is not None and plan.turned:
        position = plan.place(position)
        look_at = plan.place(look_at)
    lens = number_of(shot.get("lens_mm")) or number_of(setup.get("lens_mm"))
    if not lens:
        return None
    sensor = constant(breakdown.constants, "previs_sensor_width_mm", 36) or 36
    return Camera(setup.identifier, position, look_at, lens, frame_ratio(breakdown), float(sensor))


def placement_bands(breakdown):
    bands = dict(FRAME_PLACEMENT_BANDS)
    bands.update(constant(breakdown.constants, "frame_placement_bands", {}) or {})
    return bands


def body_numbers(breakdown):
    numbers = dict(PROJECTION_BODY)
    numbers.update(constant(breakdown.constants, "projection_body", {}) or {})
    return numbers


def placement_word(u, bands=None):
    """left_edge, left_third, centre, right_third or right_edge for a place across the frame (-1 to +1)."""
    if u is None:
        return None
    bands = bands or FRAME_PLACEMENT_BANDS
    if u < -bands["third_outer"]:
        return "left_edge"
    if u < -bands["centre_half_width"]:
        return "left_third"
    if u <= bands["centre_half_width"]:
        return "centre"
    if u <= bands["third_outer"]:
        return "right_third"
    return "right_edge"


def facing_word(camera, direction):
    """frame_left, frame_right, camera or away for a floor direction seen from a camera."""
    if direction is None or length((direction[0], direction[1])) < 1e-9:
        return None
    side = camera.side_of_direction(direction)
    toward = camera.toward_camera(direction)
    if abs(side) >= abs(toward):
        return "frame_right" if side > 0 else "frame_left"
    return "camera" if toward > 0 else "away"


def plan_heading_deg(direction):
    """The heading of a floor direction on the plan, in degrees from +x toward +y."""
    return math.degrees(math.atan2(direction[1], direction[0])) % 360


def blender_facing_deg(heading_deg):
    """Blender's facing for a plan heading: facing_deg = (heading + 90) mod 360 (5.6)."""
    return (heading_deg + 90) % 360


# ---------------------------------------------------------------- where people are over a scene's time

@dataclass
class TimedMove:
    identifier: str
    who: str
    beat: str
    start: float
    end: float
    path: list
    faces: str
    posture: str


class SceneStaging:
    """Where each person is at each moment of a scene: their start (SCENE start), then their floor-plan moves
    (MOVE), timed from the start of the first shot that shows each move's beat (5.5 MOVE start_s)."""

    def __init__(self, breakdown, scene_identifier):
        self.breakdown = breakdown
        self.scene = scene_identifier
        self.plan = set_plan(breakdown, scene_location(breakdown, scene_identifier) or "")
        self.shots = breakdown.shots_of(scene_identifier)
        self.beat_order = {beat.identifier: index for index, beat in enumerate(breakdown.beats_of(scene_identifier))}
        self.intervals = {}
        clock = 0.0
        for shot in self.shots:
            seconds = number_of(shot.get("screen_time"), 0.0)
            self.intervals[shot.identifier] = (clock, clock + seconds)
            clock += seconds
        self.total = clock
        self.starts = {}
        self.move_heights = {}
        scene = breakdown.record(scene_identifier, "SCENE")
        for item in breakdown.items(scene, "start") if scene is not None else []:
            self.starts[item.first] = {"at": self.point(item.get("at")), "faces": item.get("faces"),
                                       "posture": normalise_word(item.get("posture") or "standing"),
                                       "height": self.point_height(item.get("at"))}
        self.moves = []
        for move in breakdown.of_scene("MOVE", scene_identifier):
            beat = move.get("beat")
            anchor = self.beat_start(beat)
            begin = anchor + number_of(move.get("start_s"), 0.0)
            end = begin + number_of(move.get("dur_s"), 0.0)
            ends = [move.get("from"), move.get("via"), move.get("to")]
            path = [self.point(value) for value in ends]
            heights = [self.point_height(value) for value, point in zip(ends, path) if point is not None]
            path = [point for point in path if point is not None]
            timed = TimedMove(move.identifier, move.get("who"), beat, begin, end, path, move.get("faces"),
                              normalise_word(move.get("posture") or "standing"))
            self.move_heights[move.identifier] = heights
            self.moves.append(timed)
        self.moves.sort(key=lambda move: (move.start, sort_key_for_identifier(move.identifier)))

    def point(self, value):
        """A mark name or a point, as a floor point in the stored plan, or None."""
        if not value or normalise_word(value) == "none":
            return None
        found = point_of(value)
        if found:
            return found[:2]
        if self.plan is not None:
            if value in self.plan.marks:
                return self.plan.marks[value]
            if value in self.plan.objects:
                return self.plan.objects[value]["at"]
        return None

    def point_height(self, value):
        """The height a mark or an [x, y, z] point stands at (a vertical set plan), or None for the floor (C11)."""
        if not value or normalise_word(value) == "none":
            return None
        found = point_of(value)
        if found:
            return found[2] if len(found) > 2 else None
        if self.plan is not None:
            return self.plan.mark_heights.get(value)
        return None

    def height_at(self, character, moment):
        """The height a person stands at, at a moment: their mark's or point's z, followed along their moves (the
        floor, None, when the plan gives no height)."""
        if not self.known(character):
            return None
        height = self.starts[character].get("height")
        for move in self.moves:
            if move.who != character or not move.path:
                continue
            heights = self.move_heights.get(move.identifier) or []
            if move.end <= moment + 1e-9:
                height = heights[-1] if heights and heights[-1] is not None else height
            elif move.start < moment:
                known = [value for value in heights if value is not None]
                if len(heights) >= 2 and heights[0] is not None and heights[-1] is not None and move.end > move.start:
                    share = (moment - move.start) / (move.end - move.start)
                    height = heights[0] + (heights[-1] - heights[0]) * share
                elif known:
                    height = known[0]
            else:
                break
        return height

    def beat_start(self, beat):
        """When a beat starts on screen: the start of the first shot that shows it (or the next beat's shot)."""
        for shot in self.shots:
            if beat in self.breakdown.id_list(shot, "beats"):
                return self.intervals[shot.identifier][0]
        order = self.beat_order.get(beat)
        if order is not None:
            for shot in self.shots:
                orders = [self.beat_order.get(identifier) for identifier in self.breakdown.id_list(shot, "beats")]
                orders = [value for value in orders if value is not None]
                if orders and min(orders) > order:
                    return self.intervals[shot.identifier][0]
        return self.total

    def known(self, character):
        return character in self.starts and self.starts[character]["at"] is not None

    def state_at(self, character, moment):
        """(floor point, faces reference, posture, moving) of a person at a moment, or None when not placed."""
        if not self.known(character):
            return None
        start = self.starts[character]
        point, faces, posture, moving = start["at"], start["faces"], start["posture"], False
        for move in self.moves:
            if move.who != character or not move.path:
                continue
            if move.end <= moment + 1e-9:
                point, faces, posture = move.path[-1], move.faces or faces, move.posture or posture
            elif move.start < moment:
                share = (moment - move.start) / (move.end - move.start) if move.end > move.start else 1.0
                point = along_path(move.path, share)
                faces, moving = move.faces or faces, True
            else:
                break
        return point, faces, posture, moving

    def moments(self, shot_identifier):
        """The moments sampled in a shot: its start, every move's start, turn and end inside it, and the instant
        before its cut (a move that starts on the next shot's first frame does not count here)."""
        begin, end = self.intervals.get(shot_identifier, (0.0, 0.0))
        last = max(begin, end - 1e-6)
        found = {begin, last}
        for move in self.moves:
            for moment in (move.start, move.end):
                if begin <= moment < end:
                    found.add(moment)
            if len(move.path) == 3 and move.end > move.start:
                middle = move.start + (move.end - move.start) * via_share(move.path)
                if begin <= middle < end:
                    found.add(middle)
        return sorted(found)


def along_path(path, share):
    """The point a share of the way along a path of floor points."""
    if len(path) == 1:
        return path[0]
    lengths = [length(vector(path[index], path[index + 1])) for index in range(len(path) - 1)]
    total = sum(lengths) or 1.0
    wanted = max(0.0, min(1.0, share)) * total
    for index, piece in enumerate(lengths):
        if wanted <= piece or index == len(lengths) - 1:
            fraction = wanted / piece if piece else 1.0
            a, b = path[index], path[index + 1]
            return (a[0] + (b[0] - a[0]) * fraction, a[1] + (b[1] - a[1]) * fraction)
        wanted -= piece
    return path[-1]


def via_share(path):
    first = length(vector(path[0], path[1]))
    total = first + length(vector(path[1], path[2]))
    return first / total if total else 0.5


def scene_staging(breakdown, scene_identifier):
    key = ("staging", scene_identifier)
    if key not in breakdown._cache:
        breakdown._cache[key] = SceneStaging(breakdown, scene_identifier)
    return breakdown._cache[key]


def character_height(breakdown, character):
    record = breakdown.record(element_of(character), "CHARACTER")
    if record is not None and number_of(record.get("height_m")):
        return number_of(record.get("height_m"))
    return body_numbers(breakdown)["height_fallback_m"]


def body_height(breakdown, character, posture):
    """The height a person stands (or sits, or kneels) for the size check."""
    height = character_height(breakdown, character)
    if posture == "seated":
        return height * constant(breakdown.constants, "previs_seated_height_factor", 0.55)
    if posture == "kneeling":
        return height * constant(breakdown.constants, "previs_kneeling_height_factor", 0.7)
    return height


def eye_point(breakdown, plan, character, point, posture, base=None):
    """A person's eye point in 3D for projection. base is the height the person stands at (a mark's z on a
    vertical set plan, C11); without it they stand on the floor, or lie on what is under them."""
    if posture == "lying":
        surface = plan.surface_under(point) if plan is not None else None
        return (point[0], point[1], (base if base is not None else (surface or 0.0)) + 0.15)
    eye = body_height(breakdown, character, posture) * body_numbers(breakdown)["eye_height_share"]
    return (point[0], point[1], (base or 0.0) + eye)


def target_point(breakdown, staging, plan, reference, moment):
    """Where a faces or eyeline target is at a moment (a person, a thing on the set plan, a mark, a point)."""
    if not reference or normalise_word(reference) in ("none", "camera", "away", "up", "down", "frame_left",
                                                      "frame_right"):
        return None
    found = point_of(reference)
    if found:
        return found[:2]
    element = element_of(reference)
    if element.startswith("CH-"):
        state = staging.state_at(element, moment)
        return state[0] if state else None
    if plan is not None:
        if reference in plan.marks:
            return plan.marks[reference]
        name = re.sub(r"^[A-Z]{2,4}-", "", element).replace("-", "_")
        if name in plan.objects:
            return plan.objects[name]["at"]
        if reference in plan.objects:
            return plan.objects[reference]["at"]
    return None


@dataclass
class Placement:
    """One person's projected place in a shot at one moment."""
    moment: float
    point: tuple
    at: str
    faces: str
    depth: float
    u: float
    in_frame: bool
    posture: str
    moving: bool
    heading_deg: float = None     # the facing direction on the plan, in the orientation this shot needs
    facing_deg: float = None      # the same as Blender's facing: (heading + 90) mod 360 (5.6)


def subject_items(breakdown, shot):
    return [item for item in breakdown.items(shot, "subject") if item.first]


def projected_placement(breakdown, shot):
    """{element: [Placement, ...]} for every person in the shot the set plan places, sampled over the shot."""
    key = ("placement", shot.identifier)
    if key in breakdown._cache:
        return breakdown._cache[key]
    result = {}
    plan = plan_for_shot(breakdown, shot)
    camera = camera_for(breakdown, shot, plan)
    if plan is None or camera is None:
        breakdown._cache[key] = result
        return result
    staging = scene_staging(breakdown, scene_of(shot.identifier))
    for item in subject_items(breakdown, shot):
        element = element_of(item.first)
        if not element.startswith("CH-") or not staging.known(element):
            continue
        samples = []
        for moment in staging.moments(shot.identifier):
            state = staging.state_at(element, moment)
            if state is None:
                continue
            point, faces, posture, moving = state
            base = staging.height_at(element, moment)
            seen_point = plan.place(eye_point(breakdown, plan, element, point, posture, base))
            u, _, depth = camera.project(seen_point)
            target = target_point(breakdown, staging, plan, faces, moment)
            facing = heading = None
            if target is not None:
                direction = vector(plan.place(point)[:2], plan.place(target)[:2])
                if length(direction) > 1e-9:
                    heading = round(plan_heading_deg(direction), 1)
                if posture != "lying":
                    facing = facing_word(camera, direction)
            bands = placement_bands(breakdown)
            samples.append(Placement(moment, seen_point, placement_word(u, bands), facing, depth, u,
                                     u is not None and abs(u) <= bands["out_of_frame"], posture, moving, heading,
                                     round(blender_facing_deg(heading), 1) if heading is not None else None))
        if samples:
            result[element] = samples
    breakdown._cache[key] = result
    return result


def facing_in_shot(breakdown, shot, item):
    """A subject's facing word in a shot: projected from the set plan when one exists, else as written."""
    placements = projected_placement(breakdown, shot).get(element_of(item.first))
    if placements and placements[0].faces:
        return placements[0].faces
    written = normalise_word(item.get("faces") or "")
    return written if written in FACING_ROUND + ["up", "down"] else None


def eyeline_sides(breakdown, shot, share=0.0):
    """{element: side} for every subject whose eyeline names someone or something the set plan places: the side of
    the frame the look goes to (frame_left or frame_right), from the shot's first moment (5.6), or from the share of
    the shot given (0.5: its middle; GEOM-01 reads it when the line is spoken)."""
    key = ("eyelines", shot.identifier, round(share, 3))
    if key in breakdown._cache:
        return breakdown._cache[key]
    result = {}
    plan = plan_for_shot(breakdown, shot)
    camera = camera_for(breakdown, shot, plan)
    if plan is not None and camera is not None:
        staging = scene_staging(breakdown, scene_of(shot.identifier))
        start, end = staging.intervals.get(shot.identifier, (0.0, 0.0))
        begin = start + (end - start) * min(max(share, 0.0), 1.0)
        for item in subject_items(breakdown, shot):
            element = element_of(item.first)
            eyeline = item.get("eyeline")
            state = staging.state_at(element, begin) if element.startswith("CH-") else None
            target = target_point(breakdown, staging, plan, eyeline, begin) if eyeline else None
            if state is None or target is None:
                continue
            side = camera.side_of_direction(vector(plan.place(state[0]), plan.place(target)))
            if abs(side) < 1e-6:
                result[element] = "centre"
            else:
                result[element] = "frame_right" if side > 0 else "frame_left"
    breakdown._cache[key] = result
    return result


def is_insert_or_card(shot):
    """True for an insert (a detail, not a person's frame), a card or black."""
    return (normalise_word(shot.get("size") or "") == "insert"
            or normalise_word(shot.get("kind") or "") in ("insert", "card", "black"))


def is_single(shot):
    return normalise_word(shot.get("frame") or "") in ("single", "over_shoulder")


def focus_subject(breakdown, shot):
    """The person a shot is about: focus_on when it names someone in frame, else the first person subject."""
    items = subject_items(breakdown, shot)
    focus = element_of(shot.get("focus_on") or "")
    for item in items:
        if element_of(item.first) == focus:
            return item
    for item in items:
        if element_of(item.first).startswith("CH-"):
            return item
    return None


def dominant_of(breakdown, shot):
    """What is seen first in the shot (SHOT dominant): the AI's own words at Detailed depth; at Standard, derived from
    focus_on (the sharp subject), then the first subject, then the first thing; a turn shot's dominant is the face
    of that subject (5.5 picture group)."""
    written = shot.get("dominant")
    if written and normalise_word(written) not in ("none", "auto"):
        return {"dominant": written, "from": "written"}
    role = normalise_word(shot.get("role") or "")
    focus = shot.get("focus_on")
    chosen, source = None, None
    if focus and normalise_word(focus) != "none":
        chosen, source = element_of(focus), "focus_on"
    elif subject_items(breakdown, shot):
        chosen, source = element_of(subject_items(breakdown, shot)[0].first), "the first subject"
    else:
        things = [item.first for item in breakdown.items(shot, "thing") if item.first]
        if things:
            chosen, source = element_of(things[0]), "the first thing"
    if chosen is None:
        return {"dominant": None, "from": "nothing in frame to name"}
    name = element_name(breakdown, chosen)
    words = f"{name}'s face" if role == "turn" and chosen.startswith("CH-") else name
    return {"dominant": chosen, "words": words, "from": source + (" (a turn shot: the face)" if role == "turn" else "")}


@dataclass
class SizeCheck:
    """The size computed from lens and distance for a shot's subject (5.6, GEOM-04)."""
    subject: str
    size: str
    sizes: list
    ratio: float
    visible_height_m: float
    distance_m: float

    def as_dict(self):
        return {"subject": self.subject, "size": self.size, "sizes_over_the_shot": self.sizes,
                "ratio": round(self.ratio, 3), "visible_height_m": round(self.visible_height_m, 3),
                "distance_m": round(self.distance_m, 3)}


def size_for_ratio(breakdown, ratio):
    """The size word for visible height / subject height, from size_ladder_thresholds (half-open ranges)."""
    table = constant(breakdown.constants, "size_ladder_thresholds", {}) or {}
    for size in SIZE_LADDER:
        rule = table.get(size)
        if isinstance(rule, dict) and "at_least" in rule and ratio >= rule["at_least"]:
            return size
        if isinstance(rule, dict) and "under" in rule and ratio < rule["under"]:
            return size
        if isinstance(rule, list) and rule[0] <= ratio < rule[1]:
            return size
    return None


def size_check(breakdown, shot):
    """The shot's size computed from its lens and the distance to its subject, or None without a set plan."""
    key = ("size_check", shot.identifier)
    if key in breakdown._cache:
        return breakdown._cache[key]
    result = None
    item = None if is_insert_or_card(shot) else focus_subject(breakdown, shot)
    focus = element_of(shot.get("focus_on") or "")
    if item is not None and focus and not focus.startswith("CH-") and normalise_word(focus) != "none":
        item = None
    plan = plan_for_shot(breakdown, shot)
    camera = camera_for(breakdown, shot, plan)
    if item is not None and camera is not None:
        element = element_of(item.first)
        placements = projected_placement(breakdown, shot).get(element) or []
        sizes = []
        first = None
        for placement in placements:
            if placement.depth is None or placement.depth <= 0:
                continue
            visible = camera.visible_height_at(placement.depth)
            ratio = visible / body_height(breakdown, element, placement.posture)
            size = size_for_ratio(breakdown, ratio)
            sizes.append(size)
            if first is None:
                first = (size, ratio, visible, placement.depth)
        if first is not None:
            result = SizeCheck(element, first[0], sizes, first[1], first[2], first[3])
    breakdown._cache[key] = result
    return result


def face_heights(breakdown, shot):
    """{element: face height as a share of frame height} for every person subject: head_height_m / visible height at
    the person with a set plan, else face_height_by_size for the shot's size (5.6)."""
    head = constant(breakdown.constants, "head_height_m", 0.23)
    by_size = constant(breakdown.constants, "face_height_by_size", {}) or {}
    plan = plan_for_shot(breakdown, shot)
    camera = camera_for(breakdown, shot, plan)
    placements = projected_placement(breakdown, shot)
    result = {}
    size = normalise_word(shot.get("size") or "")
    for item in subject_items(breakdown, shot):
        element = element_of(item.first)
        if not element.startswith("CH-"):
            continue
        if is_insert_or_card(shot):
            result[element] = 0.0
            continue
        faces = normalise_word(item.get("faces") or "")
        found = placements.get(element)
        if camera is not None and found and found[0].depth and found[0].depth > 0:
            result[element] = head / camera.visible_height_at(found[0].depth)
        elif size in by_size:
            result[element] = by_size[size]
        if faces == "away" and element in result:
            result[element] = 0.0
    return result


def lip_sync(breakdown, shot):
    """none, loose or tight: tight when a speaker is seen with a face at least lip_sync_tight_face_height tall."""
    speakers = []
    for item in breakdown.items(shot, "hear"):
        if normalise_word(item.get("speaker") or "") == "on_screen":
            entry = breakdown.speech(item.first)
            if entry and entry.get("speaker"):
                speakers.append(element_of(entry["speaker"]))
    if not speakers:
        return "none"
    tight = constant(breakdown.constants, "lip_sync_tight_face_height", 0.15)
    heights = face_heights(breakdown, shot)
    if any(heights.get(speaker, 0.0) >= tight for speaker in speakers):
        return "tight"
    return "loose"


def compass_point(plan, word):
    word = normalise_word(word or "")
    centre_height = plan.height / 2
    points = {"north_wall": (plan.width / 2, plan.depth, centre_height),
              "south_wall": (plan.width / 2, 0.0, centre_height),
              "east_wall": (plan.width, plan.depth / 2, centre_height),
              "west_wall": (0.0, plan.depth / 2, centre_height),
              "ceiling": (plan.width / 2, plan.depth / 2, plan.height)}
    return points.get(word)


def scene_look(breakdown, scene_identifier):
    scene = breakdown.record(scene_identifier, "SCENE")
    look = breakdown.record(scene.get("look"), "LOOK") if scene is not None and scene.get("look") else None
    if look is None:
        location = scene_location(breakdown, scene_identifier)
        look = next((record for record in breakdown.records_of("LOOK") if record.get("for") == location), None)
    return look


def main_light_side(breakdown, shot):
    """The frame side of the look's main light for the shot's setup and era: frame_left, centre, frame_right, or
    behind the camera on one side; open when the look names no set-plan object or wall (5.6)."""
    look = scene_look(breakdown, scene_of(shot.identifier))
    item = breakdown.item(look, "main_light") if look is not None else None
    source = item.get("from") if item is not None else None
    plan = plan_for_shot(breakdown, shot)
    camera = camera_for(breakdown, shot, plan)
    if not source or plan is None or camera is None:
        return "open"
    point = plan.object_point(source) or compass_point(plan, source)
    if point is None:
        return "open"
    u, _, depth = camera.project(plan.place(point))
    if u is None:
        side = camera.side_of_direction(vector(camera.position, plan.place(point)))
        return "behind the camera, " + ("frame_right" if side > 0 else "frame_left")
    if abs(u) <= placement_bands(breakdown)["centre_half_width"]:
        return "centre"
    return "frame_right" if u > 0 else "frame_left"


def axis_sides(breakdown, scene_identifier):
    """{part: {setup: 'left of the line' | 'right of the line'}}: which side of the line of action each setup used in
    the part stands, the line running from the first to the second person of the part's first engaged pair."""
    staging = scene_staging(breakdown, scene_identifier)
    plan = staging.plan
    result = {}
    if plan is None:
        return result
    for part in breakdown.of_scene("PART", scene_identifier):
        span = (part.get("beats") or "").split("..")
        beats = [beat for beat in breakdown.beats_of(scene_identifier)
                 if len(span) == 2 and sort_key_for_identifier(span[0]) <= sort_key_for_identifier(beat.identifier)
                 <= sort_key_for_identifier(span[1])]
        pair = []
        for beat in beats:
            pair = split_list(beat.get("engaged_pair") or "")
            if len(pair) == 2:
                break
        if len(pair) != 2:
            continue
        moment = staging.beat_start(beats[0].identifier) if beats else 0.0
        first, second = staging.state_at(pair[0], moment), staging.state_at(pair[1], moment)
        if first is None or second is None:
            continue
        line = vector(first[0], second[0])
        sides = {}
        for shot in breakdown.shots_of(scene_identifier):
            if not set(breakdown.id_list(shot, "beats")) & {beat.identifier for beat in beats}:
                continue
            setup = breakdown.record(shot.get("setup"), "SETUP") if shot.get("setup") else None
            position = point_of(setup.get("at")) if setup is not None else None
            if not position:
                continue
            offset = vector(first[0], position[:2])
            turn = line[0] * offset[1] - line[1] * offset[0]
            sides[setup.identifier] = "left of the line" if turn > 0 else "right of the line"
        result[part.identifier] = sides
    return result


# ---------------------------------------------------------------- sides (5.4 rule 8, 5.6, K03, K07)

def other_side(side):
    return {"left": "right", "right": "left"}.get(side, side)


def apparent_side(own, mirror_state):
    """The side a viewer reads on the picture: the own side, swapped when the element is mirrored (5.6); open while
    the element's mirror state is open."""
    if mirror_state == "open":
        return "open"
    return other_side(own) if mirror_state == "mirrored" else own


def image_position(apparent, facing):
    """Where an apparent side falls in the picture for a facing: facing the camera, apparent right is frame-left;
    facing frame-right, apparent right is the hand nearest the camera; and so on (5.6)."""
    if apparent not in ("left", "right"):
        return "open"
    if facing == "camera":
        return "frame_left" if apparent == "right" else "frame_right"
    if facing == "away":
        return "frame_right" if apparent == "right" else "frame_left"
    if facing == "frame_right":
        return "nearest the camera" if apparent == "right" else "far from the camera"
    if facing == "frame_left":
        return "nearest the camera" if apparent == "left" else "far from the camera"
    return "open"


def turned_facing(facing):
    return {"frame_left": "frame_right", "frame_right": "frame_left"}.get(facing, facing)


def sided_features(breakdown, reference, line=None):
    """[(feature, own side, plot)] of an element state (STATE side) or a thing (PROP side); a feature both name is
    listed once, as the state gives it."""
    found = []
    state = state_of_reference(breakdown, reference, line) if reference else None
    records = [state] if state is not None else []
    prop = breakdown.record(element_of(reference), "PROP") if reference else None
    if prop is not None:
        records.append(prop)
    for record in records:
        for item in breakdown.items(record, "side"):
            own = normalise_word(item.get("own") or "")
            if any(normalise_word(feature) == normalise_word(item.first or "") for feature, _, _ in found):
                continue
            found.append((item.first, own if own in ("left", "right") else None, is_yes(item.get("plot"))))
    return found


def element_name(breakdown, element):
    """A plain name for an element: a person's name, else its record's title in lower case ('the water bottle')."""
    element = element_of(element)
    if element and element.startswith("CH-"):
        return person_name(element)
    record = breakdown.record(element)
    if record is not None and record.title:
        title = record.title.strip()
        return title[:1].lower() + title[1:] if title[:4].lower() == "the " else title
    return element


def flipped_after(route):
    """True when the route flips the generated picture afterwards, so prompts describe the unflipped picture."""
    return route in ("flip_all", "flip_with_mirrored_references")


def prompt_is_flipped(route, mirror_state):
    """True when an element's prompt describes a picture that is flipped later: every element on routes a and b;
    on the plate route (c) the mirrored elements, generated in world orientation in the plate that is then flipped,
    while the normal people are added to it unflipped (8.5)."""
    return flipped_after(route) or (route == "plate" and mirror_state == "mirrored")


def subject_sides(breakdown, shot, item, route=None):
    """For one subject: its facing, mirror state, both hands (apparent side, place in the picture, place in the
    prompt) and every sided feature in the same terms; also which own hand is nearest the camera."""
    element = element_of(item.first)
    line = shot_first_line(breakdown, shot)
    mirror = mirror_state_at(breakdown, item.first, line)
    facing = facing_in_shot(breakdown, shot, item)
    route = route if route is not None else mirror_route(breakdown, shot).route
    flipped = prompt_is_flipped(route, mirror)
    prompt_facing = turned_facing(facing) if flipped else facing
    prompt_mirror = ("normal" if mirror == "mirrored" else "mirrored") if flipped else mirror

    def describe(own):
        apparent = apparent_side(own, mirror)
        return {"own": own, "appears_as": apparent, "image": image_position(apparent, facing),
                "prompt": image_position(apparent_side(own, prompt_mirror), prompt_facing)}

    hands = {"own_right": describe("right"), "own_left": describe("left")}
    nearest = next((own for own in ("right", "left") if hands["own_" + own]["image"] == "nearest the camera"), None)
    features = []
    for feature, own, plot in sided_features(breakdown, item.first, line):
        entry = {"feature": feature, "own": own, "plot": plot}
        if own:
            entry.update(describe(own))
            entry["on_hand"] = "the hand nearest the camera" if entry["image"] == "nearest the camera" else (
                "the far hand" if entry["image"] == "far from the camera" else entry["image"])
        features.append(entry)
    written = " ".join(filter(None, [item.get("does"), shot.get("end")])).lower()
    return {"element": element, "state": item.first, "mirror_state": mirror, "facing": facing,
            "hands": hands, "hand_nearest_the_camera": nearest,
            "does_names_hand_nearest_the_camera": "hand nearest the camera" in written,
            "features": features}


def image_sides(breakdown, shot):
    """Every person and thing in frame with its sided features: image side and prompt side (5.6)."""
    key = ("image_sides", shot.identifier)
    if key in breakdown._cache:
        return breakdown._cache[key]
    route = mirror_route(breakdown, shot).route
    result = [subject_sides(breakdown, shot, item, route) for item in subject_items(breakdown, shot)
              if item.first and not item.first.startswith(("MO-", "TX-"))]
    line = shot_first_line(breakdown, shot)
    for item in breakdown.items(shot, "thing"):
        if not item.first or item.first.startswith(("MO-", "TX-")):
            continue
        features = sided_features(breakdown, item.first, line)
        if not features:
            continue
        mirror = mirror_state_at(breakdown, item.first, line)
        result.append({"element": element_of(item.first), "state": item.first, "mirror_state": mirror,
                       "features": [{"feature": feature, "own": own, "plot": plot,
                                     "appears_as": apparent_side(own, mirror) if own else None}
                                    for feature, own, plot in features]})
    breakdown._cache[key] = result
    return result


def feature_nouns(feature):
    """The nouns a sided feature's name is known by: 'wedding ring' -> ring, rings; 'skinned palm' -> palm."""
    words = re.findall(r"[a-z]+", (feature or "").lower())
    found = set()
    for word in words[-1:]:
        found.add(word)
        found.add(word[:-1] if word.endswith("s") else word + "s")
    return found


def feature_hidden(breakdown, shot, feature):
    """True when the shot keeps the feature out of sight: must_not_show names a record whose ID, title or names
    hold the feature's noun (MO-RINGS for a wedding ring)."""
    nouns = feature_nouns(feature)
    for identifier in breakdown.id_list(shot, "must_not_show"):
        record = breakdown.record(identifier) or breakdown.record(element_of(identifier))
        words = set(re.findall(r"[a-z]+", identifier.lower()))
        if record is not None:
            words |= set(re.findall(r"[a-z]+", (record.title or "").lower()))
            words |= set(re.findall(r"[a-z]+", (record.get("names") or "").lower()))
        if nouns & words:
            return True
    return False


# ---------------------------------------------------------------- the mirror route (8.5, K02)

@dataclass
class MirrorRoute:
    route: str
    letter: str
    text_graphic: bool
    reasons: list = dataclass_field(default_factory=list)

    def as_dict(self):
        return {"route": self.route, "letter": self.letter, "text_graphic": self.text_graphic,
                "reasons": self.reasons}


ROUTE_LETTERS = {"plate": "c", "direct": "e", "flip_with_mirrored_references": "b", "flip_all": "a", "none": "none",
                 "open": "open"}


def mirror_route(breakdown, shot):
    """The shot's mirror route, in the order of 8.5: text graphic always when text is in frame; then plate, direct,
    flip with mirrored references, flip all, or none. flip: never turns a route that flips anything (a, b, or the
    plate of c) into direct."""
    key = ("mirror_route", shot.identifier)
    if key in breakdown._cache:
        return breakdown._cache[key]
    text_graphic = bool(breakdown.id_list(shot, "text"))
    reasons = ["readable text in frame: drawn as a text graphic and composited after any flip"] if text_graphic else []
    kind = normalise_word(shot.get("kind") or "")
    line = shot_first_line(breakdown, shot)
    states = shot_mirror_states(breakdown, shot)
    location = scene_location(breakdown, scene_of(shot.identifier)) if kind not in ("card", "black") else None
    location_state = states.get(location, {}).get("mirror_state") if location else None
    route = None
    if kind in ("card", "black"):
        route = "none"
        reasons.append("a card or black: no place in frame")
    elif eras_unresolved(breakdown):
        route = "open"
        reasons.append("the mirror rule's era lines were not found in the story given ("
                       + ", ".join(eras_unresolved(breakdown)) + "), so which elements are mirrored is not known yet")
    elif not eras(breakdown):
        route = "none"
        reasons.append("nothing in frame is mirrored")
    else:
        mirrored = [element for element, entry in states.items() if entry["mirror_state"] == "mirrored"]
        people = [element for element in states if element.startswith("CH-")]
        differing = [element for element in people
                     if location_state is not None and states[element]["mirror_state"] != location_state]
        plate_limit = constant(breakdown.constants, "plate_route_face_height", 0.1)
        heights = face_heights(breakdown, shot)
        visible_plot = []
        for reference in elements_in_shot(breakdown, shot):
            if mirror_state_at(breakdown, reference, line) != "mirrored":
                continue
            for feature, own, plot in sided_features(breakdown, reference, line):
                if plot and not feature_hidden(breakdown, shot, feature):
                    detail = f"{element_name(breakdown, reference)}'s {feature}"
                    if detail not in visible_plot:
                        visible_plot.append(detail)
        large = [element for element in differing if heights.get(element, 0.0) >= plate_limit]
        if visible_plot or large:
            route = "plate"
            if visible_plot:
                reasons.append("a plot-sided detail of a mirrored element is visible: " + ", ".join(visible_plot))
            if large:
                reasons.append("a face whose mirror state differs from the place's covers at least "
                               f"{seconds_text(plate_limit)} of the frame height: " + ", ".join(
                                   f"{person_name(element)} {heights[element]:.2f}" for element in large))
        elif mirrored and all(element_orientations(breakdown, element) == {"mirrored"} for element in mirrored):
            route = "direct"
            reasons.append("every mirrored element in frame is seen in one orientation only in the whole film")
        elif differing:
            route = "flip_with_mirrored_references"
            reasons.append("people whose mirror state differs from the place's are small in frame, with no "
                           "plot-sided detail: " + ", ".join(person_name(element) for element in differing))
        elif location_state == "mirrored":
            route = "flip_all"
            reasons.append("the place is mirrored and nobody differs from it")
        elif mirrored:
            route = "flip_with_mirrored_references"
            reasons.append("mirrored elements in a place shown normally: " + ", ".join(mirrored))
        else:
            route = "none"
            reasons.append("nothing in frame is mirrored")
    # flip: never means nothing of this shot is ever flipped: not the clip (routes a and b) and not the plate picture
    # (route c); a sided insert is made from edited stills at their final side (8.5, SIDE-03, K07)
    if normalise_word(shot.get("flip") or "auto") == "never" and (flipped_after(route) or route == "plate"):
        reasons.append(f"flip: never, so the {route.replace('_', ' ')} route becomes direct (the final picture is "
                       "made as it appears, from edited stills at their final side)")
        route = "direct"
    result = MirrorRoute(route, ROUTE_LETTERS[route], text_graphic, reasons)
    breakdown._cache[key] = result
    return result


def post_operations(breakdown, shot):
    """Finishing operations the shot needs from its mirror route (8.5, 8.7): flip after routes a and b; composite
    for a text graphic, and for the plate route, whose normal people are added to the flipped plate."""
    route = mirror_route(breakdown, shot)
    found = []
    if flipped_after(route.route):
        found.append("flip")
    if route.text_graphic or route.route == "plate":
        found.append("composite")
    return found


# ---------------------------------------------------------------- story points (5.4 rule 12, step 7)

STORY_POINT_IN_TEXT = re.compile(r'(SC\d{2,3}[A-Z]?)\s+(["“][^"“”]+["”])(\s*=\s*(SC\d{2,3}[A-Z]?-B\d{2,3}))?')


@dataclass
class StoryPoint:
    """One story point and the beat it resolves to."""
    record: str
    field: str
    value: str
    scene: str
    quote: str
    stored_beat: str
    line: int = None
    beat: str = None
    status: str = "resolved"
    problem: str = ""

    def as_dict(self):
        return {"record": self.record, "field": self.field, "scene": self.scene, "quote": self.quote,
                "line": self.line, "beat": self.beat, "stored_beat": self.stored_beat, "status": self.status,
                "problem": self.problem}


def story_point_fields(schema, type_name):
    """{field name: where story points sit in it} for a record type: 'value', 'first' or sub-part keys."""
    found = {}
    record_type = schema.record_types.get(type_name, {})
    for definition in record_type.get("fields", []):
        places = []
        if definition.get("kind") in STORY_POINT_KINDS:
            places.append("value")
        first = definition.get("first_part")
        if isinstance(first, dict) and first.get("kind") in STORY_POINT_KINDS:
            places.append("first")
        for sub_part in definition.get("sub_parts") or []:
            if isinstance(sub_part, dict) and sub_part.get("kind") in STORY_POINT_KINDS:
                places.append(sub_part.get("key"))
        if places:
            found[definition["name"]] = places
    return found


def story_point_texts(breakdown, record, field_name, places, value):
    """The story-point strings inside one field value."""
    texts = []
    if "value" in places:
        texts += split_list(value) if "," in value and value.count('"') >= 4 else [value]
    definition = breakdown.definition(record.type_name, field_name)
    if any(place not in ("value",) for place in places):
        item = split_item(value, definition)
        if "first" in places and item.first:
            texts.append(item.first)
        for key in places:
            if key in ("value", "first"):
                continue
            part = item.get(key)
            if part:
                texts += [piece for piece in split_outside_quotes(part, ",") if piece.strip()]
    return [text.strip() for text in texts if text and parse_story_point(text.strip())]


def beat_holding_line(breakdown, scene_identifier, line):
    for beat in breakdown.beats_of(scene_identifier):
        if line in breakdown.lines_of(beat):
            return beat.identifier
    return None


def resolve_story_point(breakdown, text, record=None, field_name=None):
    """Resolve one story point ('SC10 "Her face changes."') to its line and to the beat whose lines hold it."""
    scene_identifier, quote, stored = parse_story_point(text)
    point = StoryPoint(record.identifier or record.type_name if record else None, field_name, text, scene_identifier,
                       quote, stored)
    if breakdown.story is None:
        point.status, point.problem = "no_story", "skipped: story not present"
        return point
    scope = breakdown.story.scope_of(scene_identifier)
    if scope is None:
        point.status, point.problem = "not_in_story", "skipped: not in the excerpt"
        return point
    problem = breakdown.story.check_quote(quote, scope[0], scope[1])
    if problem:
        point.status, point.problem = "not_found", problem
        return point
    point.line = breakdown.story.resolve_line(quote, scope[0], scope[1])
    if not breakdown.beats_of(scene_identifier):
        point.status, point.problem = "no_beats", "the scene has no beats yet"
        return point
    point.beat = beat_holding_line(breakdown, scene_identifier, point.line)
    if point.beat is None:
        point.status, point.problem = "no_beat", f"line {point.line} is in no beat of {scene_identifier}"
    return point


def story_points(breakdown):
    """Every story point in the records with the beat it resolves to (and the beat stored with it, if any)."""
    key = ("story_points",)
    if key in breakdown._cache:
        return breakdown._cache[key]
    found = []
    for (type_name, _), record in sorted(breakdown.index.items(), key=lambda pair: (pair[0][0], sort_key_for_identifier(pair[0][1] or ""))):
        fields = story_point_fields(breakdown.schema, type_name)
        for field_name, places in fields.items():
            for value in record.get_all(field_name):
                for text in story_point_texts(breakdown, record, field_name, places, value):
                    found.append(resolve_story_point(breakdown, text, record, field_name))
    breakdown._cache[key] = found
    return found


def with_story_point_beats(breakdown, value, type_name, field_name):
    """A field value with every resolvable story point ending in ' = <beat>' (5.2, WP1's stored form)."""
    if not story_point_fields(breakdown.schema, type_name).get(field_name):
        return value

    def replace(match):
        text = f"{match.group(1)} {match.group(2)}"
        point = resolve_story_point(breakdown, text)
        if point.beat:
            return f"{text} = {point.beat}"
        return match.group(0)

    return STORY_POINT_IN_TEXT.sub(replace, value)


def store_story_point_beats(breakdown, project_folder=None, schema=None):
    """Write each resolved story point's beat into the record files (code_state), keeping old copies in history.
    Returns (number of values changed, names of files changed)."""
    changed_values = 0
    changed_files = []
    for record_file in breakdown.record_files:
        file_changed = False
        for record in record_file.records:
            fields = story_point_fields(breakdown.schema, record.type_name)
            for line in record.fields:
                if line.name not in fields or line.missing:
                    continue
                new_value = with_story_point_beats(breakdown, line.value, record.type_name, line.name)
                if new_value != line.value:
                    line.value = new_value
                    line.changed = True
                    changed_values += 1
                    file_changed = True
        if file_changed:
            changed_files.append(record_file)
    if project_folder and changed_files:
        from .project_files import history_run_folder, keep_in_history, Project
        from .record_format import write_file
        project = Project(project_folder, breakdown.schema, breakdown.words)
        history = history_run_folder(project)
        for record_file in changed_files:
            path = Path(project_folder) / record_file.name
            if path.is_file():
                keep_in_history(history, path, record_file.name)
            write_file(record_file, path, breakdown.schema)
    return changed_values, [record_file.name for record_file in changed_files]


# ---------------------------------------------------------------- previs stubs (step 8, 5.4 rule 2)

PREVIS_IDENTIFIER = re.compile(r"^PV-(.+)-V\d{2}$")
PREVIS_FILE = "19 Grey previews/Grey preview jobs.md"


def previs_stubs_needed(breakdown):
    """[(previs ID, what it is for, the record that names it)] for every PREVIS a SHOT time_slice or a CUT
    shared_geometry names that no PREVIS record holds yet: code creates these as stubs with status planned (step 8)."""
    existing = {record.identifier for record in breakdown.records_of("PREVIS", include_omitted=True)}
    found = []
    named = []
    for shot in breakdown.records_of("SHOT"):
        for item in breakdown.items(shot, "time_slice"):
            named.append((item.first, shot.identifier))
    for cut in breakdown.records_of("CUT"):
        value = cut.get("shared_geometry")
        if value and normalise_word(value) != "none":
            named.append((value.strip(), cut.identifier))
    for identifier, source in named:
        match = PREVIS_IDENTIFIER.match(identifier or "")
        if not match or identifier in existing or any(entry[0] == identifier for entry in found):
            continue
        found.append((identifier, match.group(1), source))
    return found


def checker_accepts_previs_stubs(schema, words):
    """True when FORM-05 leaves a PREVIS stub (status planned) alone. Until it does, a stub would switch the grey
    preview add-on on and the checker would ask the AI for fields only add-on B fills, so build lists the stubs in
    derived fields.json instead of writing them (ID-02 already accepts the names they would hold)."""
    try:
        from .checks_form import FormContext, check_form_05
        from .record_format import add_record, make_record, new_record_file
    except ImportError:
        return False
    record_file = new_record_file(PREVIS_FILE, ["# Grey previews"], "Grey preview jobs")
    add_record(record_file, make_record("PREVIS", "PV-SC01-MASTER-V01", fields=[
        ("for", "SC01-MASTER"), ("level", 3), ("status", "planned"), ("locked", "no")]), schema)
    context = FormContext.for_records(schema, words, [record_file], step=None)
    return not any("PV-SC01-MASTER-V01" in str(problem) for problem in check_form_05([record_file], context))


def create_previs_stubs(breakdown, project_folder):
    """Add the PREVIS stubs a project needs to its grey preview jobs file (keeping the old file in history).
    Returns the IDs created (none while the checker would still ask for their add-on fields)."""
    needed = previs_stubs_needed(breakdown)
    if not needed or not checker_accepts_previs_stubs(breakdown.schema, breakdown.words):
        return []
    from .project_files import Project, history_run_folder, keep_in_history
    from .record_format import add_record, ensure_end_line, make_record, new_record_file, write_file
    project = Project(project_folder, breakdown.schema, breakdown.words)
    record_files = project.load_record_files()
    file_name = next((name for name in [project.target_file_for(make_record("PREVIS", needed[0][0]), record_files)]
                      if name), PREVIS_FILE)
    path = Path(project_folder) / file_name
    record_file = next((existing for existing in record_files if existing.name == file_name), None)
    if record_file is None:
        record_file = new_record_file(file_name, ["# Grey previews", "",
                                                  "The grey preview jobs: one for each shot, master or place "
                                                  "that gets a grey 3D preview."], "Grey preview jobs")
    else:
        keep_in_history(history_run_folder(project), path, file_name)
    level = constant(breakdown.constants, "previs_stub_level", 3)
    for identifier, target, _ in needed:
        add_record(record_file, make_record("PREVIS", identifier, fields=[
            ("for", target), ("level", level), ("status", "planned"), ("locked", "no")]),
            breakdown.schema, project.type_order_for(file_name))
    ensure_end_line(record_file, "Grey preview jobs")
    write_file(record_file, path, breakdown.schema)
    return [identifier for identifier, _, _ in needed]


# ---------------------------------------------------------------- everything for one shot, scene, project

def shot_mirror_state_text(breakdown, shot):
    return {entry["state"] or element: entry["mirror_state"] for element, entry in shot_mirror_states(breakdown, shot).items()}


def derive_shot(breakdown, shot, model=None):
    """Every code-derived field of one SHOT (5.5 'Code derives on SHOT'), as plain data."""
    floor = time_floor(breakdown, shot)
    era = shot_era(breakdown, shot)
    route = mirror_route(breakdown, shot)
    check = size_check(breakdown, shot)
    placements = projected_placement(breakdown, shot)
    heights = face_heights(breakdown, shot)
    plan = plan_for_shot(breakdown, shot)
    return {
        "label": crew_label(shot.identifier),
        "min_screen_time_s": floor.floor,
        "min_screen_time_reasons": floor.reasons(),
        "floor_parts": {"speech_floor_s": floor.speech_floor, "text_floor_s": floor.text_floor,
                        "pause_owed_s": floor.pause_owed, "words_unknown_for": floor.unknown_speeches},
        "clips": clip_plan(breakdown, shot, model).as_dict(),
        "era": era.name if era else None,
        "frame_handedness": era.frame if era else "original",
        "mirror_state": shot_mirror_state_text(breakdown, shot),
        "mirror_route": route.route,
        "mirror_route_detail": route.as_dict(),
        "post_ops": post_operations(breakdown, shot),
        "image_sides": image_sides(breakdown, shot),
        "main_light_side": main_light_side(breakdown, shot),
        "eyeline_sides": eyeline_sides(breakdown, shot),
        "projected_placement": {element: [{"moment_s": round(sample.moment, 2), "at": sample.at,
                                           "faces": sample.faces, "depth_m": round(sample.depth, 3) if sample.depth else None,
                                           "in_frame": sample.in_frame, "posture": sample.posture,
                                           "plan_point": [round(value, 3) for value in sample.point],
                                           "facing_deg": sample.facing_deg} for sample in samples]
                                for element, samples in placements.items()},
        "plan_orientation": plan.orientation if plan is not None else None,
        "dominant": dominant_of(breakdown, shot),
        "size_check": check.size if check else None,
        "size_check_detail": check.as_dict() if check else None,
        "face_height": {element: round(value, 3) for element, value in heights.items()},
        "lip_sync": lip_sync(breakdown, shot),
        "text_orientation": {text: text_orientation(breakdown, text, shot) for text in breakdown.id_list(shot, "text")},
    }


def derive_scene(breakdown, scene_identifier):
    """Every code-derived field of one SCENE, and its list items' provisional floors."""
    era = scene_era(breakdown, scene_identifier)
    items = list_items(breakdown, scene_identifier)
    eighths, eighths_how = scene_eighths(breakdown, scene_identifier)
    provisional = {identifier: provisional_floor(breakdown, scene_identifier, identifier) for identifier, _ in items}
    return {
        "label": scene_label(breakdown, scene_identifier),
        "era": era.era if era else None,
        "frame_handedness": era.frame if era else "original",
        "switch_at": era.switch_at if era else None,
        "era_after_switch": era.next_era if era else None,
        "states_in_play": states_in_play(breakdown, scene_identifier),
        "mirror_states": scene_mirror_states(breakdown, scene_identifier),
        "duration_est_s": scene_duration(breakdown, scene_identifier),
        "eighths": eighths,
        "eighths_how": eighths_how,
        "speaking": speaking_counts(breakdown, scene_identifier),
        "speech_words": speech_word_counts(breakdown, scene_identifier),
        "coverage": coverage_map(breakdown, scene_identifier),
        "axis_sides": axis_sides(breakdown, scene_identifier),
        "script_marked_beats": {beat.identifier: script_marked(breakdown, beat)[0]
                                for beat in breakdown.beats_of(scene_identifier)},
        "provisional_floors": {identifier: floor.floor for identifier, floor in provisional.items()},
        "provisional_floor_reasons": {identifier: floor.reasons() for identifier, floor in provisional.items()},
    }


def derive_all(breakdown, scenes=None):
    """Everything code derives, for the whole project (or the scenes named)."""
    scene_identifiers = scenes or breakdown.scene_identifiers()
    result = {"scenes": {}, "shots": {}, "locations": {}, "states": {}, "story_points": []}
    for scene_identifier in scene_identifiers:
        result["scenes"][scene_identifier] = derive_scene(breakdown, scene_identifier)
        for shot in breakdown.shots_of(scene_identifier):
            result["shots"][shot.identifier] = derive_shot(breakdown, shot)
    for location in breakdown.records_of("LOCATION"):
        result["locations"][location.identifier] = {"orientation": location_orientation(breakdown, location.identifier)}
    for state in breakdown.records_of("STATE"):
        until = state_until(breakdown, state)
        result["states"][state.identifier] = {"until": f"{until[0]} | line: {until[1]}" if until[0] else None}
    result["story_points"] = [point.as_dict() for point in story_points(breakdown)]
    result["previs_stubs_needed"] = [{"previs": identifier, "for": target, "named_by": source}
                                     for identifier, target, source in previs_stubs_needed(breakdown)]
    return result


# ---------------------------------------------------------------- the command: build

def add_build_arguments(parser):
    parser.add_argument("--scene", help="work out only this scene (for example SC10)")
    parser.add_argument("--story", help="a story file to read the lines and speeches from (default: the project's)")


def run_build(context):
    """stage.py build: work out every derived field, store each story point's beat, write derived fields.json."""
    project_folder = Path(context.project)
    try:  # the fields code keeps that no other command fills (fix list C4, C5, C8)
        from .fill_code_fields import fill_code_fields
        from .project_files import Project
        filled = fill_code_fields(Project(project_folder, context.schema, context.words))
        if filled.summary():
            context.say(filled.summary())
        for note in filled.notes:
            context.say(note)
    except (OSError, ValueError, ImportError) as error:
        context.say(f"The fields code keeps were not filled ({type(error).__name__}: {error}).")
    breakdown = Breakdown.from_project(project_folder, context.schema, context.words, context.constants)
    if getattr(context.arguments, "story", None):
        breakdown.attach_story_file(context.arguments.story)
    changed_values, changed_files = store_story_point_beats(breakdown, project_folder)
    stubs = create_previs_stubs(breakdown, project_folder)
    if stubs:
        context.say(f"Made {len(stubs)} grey preview job{'s' if len(stubs) != 1 else ''} to fill in later: "
                    + ", ".join(stubs) + ".")
    if changed_values or stubs:
        breakdown = Breakdown.from_project(project_folder, context.schema, context.words, context.constants)
        if getattr(context.arguments, "story", None):
            breakdown.attach_story_file(context.arguments.story)
        from .project_files import Project
        entry = []
        if changed_values:
            entry.append(f"Worked out the beat of {changed_values} story point{'s' if changed_values != 1 else ''}")
        if stubs:
            entry.append(f"made {len(stubs)} grey preview job{'s' if len(stubs) != 1 else ''} to fill in later")
        try:
            Project(project_folder, context.schema, context.words).add_log_entry("; ".join(entry).capitalize() + ".")
        except (OSError, ValueError) as error:
            context.say(f"The log in 00 Start here could not be written ({error}); the story points were saved.")
    scenes = [context.arguments.scene] if getattr(context.arguments, "scene", None) else None
    data = derive_all(breakdown, scenes)
    data["about"] = ("Worked out by stage.py build from the record files; never edit it. It is made again on "
                     "every build.")
    machine = project_folder / MACHINE_FOLDER
    machine.mkdir(parents=True, exist_ok=True)
    target = machine / DERIVED_FILE
    temporary = target.with_suffix(".json.part")
    with open(temporary, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=1, ensure_ascii=False)
        handle.write("\n")
    temporary.replace(target)
    for module_name, function_name in (("make_views", "build_views"), ("make_exports", "write_breakdown_json")):
        try:
            module = __import__(f"{__package__}.{module_name}", fromlist=[function_name])
        except ImportError:
            continue
        function = getattr(module, function_name, None)
        if function is not None:
            function(project_folder)
    shots = len(data["shots"])
    resolved = sum(1 for point in data["story_points"] if point["status"] == "resolved")
    waiting = sum(1 for point in data["story_points"] if point["status"] in ("no_beats",))
    scenes_with_shots = len({scene_of(identifier) for identifier in data["shots"]} - {None})
    context.say(f"Worked out {shots} shot{'s' if shots != 1 else ''} in {scenes_with_shots} "
                f"scene{'s' if scenes_with_shots != 1 else ''} (of {len(data['scenes'])}): time floors, clips, "
                "mirror routes, sides and sizes.")
    context.say(f"Story points: {resolved} placed on their beats"
                + (f", {waiting} waiting for their scene's beats" if waiting else "")
                + (f"; {changed_values} beats written into {', '.join(changed_files)}" if changed_values else "") + ".")
    context.say(f"Written: {MACHINE_FOLDER}/{DERIVED_FILE}")
    context.summary = f"build: {shots} shots, {resolved} story points placed"
    return 0


def register_commands(table):
    if "build" in getattr(table, "commands", {}):
        return
    table.add("build", "Work out every derived field (time floors, clips, sides, mirror routes, sizes)", run_build,
              add_build_arguments)


# Methods, so other modules can write breakdown.time_floor(shot) as well as time_floor(breakdown, shot).
for _function in (time_floor, provisional_floor, clip_plan, held_take, scene_era, shot_era, eras, mirror_state_at,
                  shot_mirror_states, scene_mirror_states, states_in_play, state_until, state_valid_at,
                  location_orientation, element_orientations, text_orientation, projected_placement, eyeline_sides,
                  size_check, face_heights, lip_sync, main_light_side, image_sides, mirror_route, post_operations,
                  story_points, derive_shot, derive_scene, derive_all, scene_duration, scene_label, coverage_map,
                  speaking_counts, focus_subject, facing_in_shot, plan_for_shot, camera_for, scene_staging,
                  axis_sides, scene_eighths, script_marked, speech_word_counts, dominant_of, eras_unresolved):
    setattr(Breakdown, _function.__name__, _function)
del _function
