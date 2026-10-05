"""make_views.py: the parts of a project that people read, made from the records (blueprint 2.6, 5.6 Views, 7.1,
11.3 criterion 10, 13.7, step 11).

What this file does, in plain words:
- writes the plain part of every record file (the part above the divider line) from the file's own records:
  "At a glance", the items one plain line each and, for a scene, "Why it's shot this way" and "Small choices I
  made"; everything below the divider (the records and the END line) is left exactly as it was;
- rewrites the status part of 00 Start here (where things stand, the next step, the big choices so far and the
  files in this folder) and keeps its word list and its log as they are;
- writes 02 Whole-film summary: the records step 7 reads from files 04 to 09, without the floor plans;
- writes the book, 15 The breakdown/The breakdown.md and The breakdown.html: contents, how to read it (shown on a
  shot of the user's own story), the story plan, people, places and things, the film rules in plain words, every
  scene (At a glance, the shots one line each, then the full shots folded underneath) and the word list;
- lays approved storyboard frames out as 18 Storyboard/Scene NN.html, a slideshow to watch with the sound off
  (blueprint 10): the frame inside the film's frame shape, the shot's number, its line, its words, its seconds and
  the labels the page adds (a hold, room sound only, where the eyes go);
- gives other modules plain names for records ("shot 150", "Iona, state 2") and plain words for values
  ("medium close-up"), so that nothing a person reads holds a code or an abbreviation (WORDS-02, WORDS-04).

It never touches the plain parts the checker writes (12 Whole-film check, 13 Health check), and it keeps any
section of a plain part it does not own (the word list and log of 00 Start here, "Lines to look at" in the scene
list) where it was.

Other modules use: build_views(project_folder), write_book(project_folder), write_storyboard_pages(view),
ProjectView, PlainNames, plain_value,
seconds_words, duration_words, scene_number, shot_number_text.

Standard library only.

After the full run on The Catch (Project notes 31 and 32):
- the one-of-a-kind records are named in plain words (the camera system, the sound plan, the ladder); a rung 'held
  past the longest pause'; one film length.

After the three-scene test of the fixed kit (Project notes 35 and 36):
- the one-line list follows the written shot; states and saved choices are named by what they are; the floor is
  rounded up to one decimal; seated and kneeling eye heights in words.

After the second three-scene test (Project notes 37 and 38):
- the book lists the beats, one line each; emphasis and grey preview levels in words; a one-line entry says who
  acts; recordings and screens are said; turns are named in story order and moves by who moves; an addition
  the scene already lists is said once; small choices shown at checkpoint B are listed as small.
"""

import datetime
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

from .record_format import (DIVIDER_LINE, FieldLine, Record, TextBlock, load_skill_data, normalise_word,
                            parse_file, parse_line_numbers, parse_story_point, record_lines, render_file,
                            sort_key_for_identifier, split_item, split_list)
from .project_files import (CHOICES_FILE, FILES_IN_THIS_FOLDER, SCENE_LIST_FILE, SCENES_FOLDER, START_HERE, Project,
                            load_steps, unit_in_plain_words)
from .derive_fields import Breakdown, element_of, scene_duration, time_floor

SUMMARY_FILE = "02 Whole-film summary.md"
BOOK_FOLDER = "15 The breakdown"
BOOK_MARKDOWN = "The breakdown.md"
BOOK_HTML = "The breakdown.html"
CHECKER_FILES = ("12 Whole-film check.md", "13 Health check.md")
STUDY_ONLY_MARK = "Private study, not for publication"
FILES_LINE = "Each file's number is its place in the list Files in this folder; the log below records every change."

# The record types step 7 reads from files 04 to 09 (6.1), in the order the summary lists them.
SUMMARY_TYPES = ["SCENE", "PLAN", "SEQUENCE", "PLANT", "FACT", "CHAPTER", "STRAND", "CARDINAL", "WORLD", "RULE",
                 "CHARACTER", "VOICE", "LOCATION", "PROP", "TEXT", "MOTIF", "CAMERA", "STATE"]
# A scene's design fields live in its scene file; the summary keeps only its list and plan fields (5.5).
SCENE_LIST_FIELDS = ["heading", "int_ext", "place_text", "time_text", "lines", "characters", "speaking",
                     "transition_in", "transition_out", "presentation", "host", "event", "sequence",
                     "scene_intensity", "whose_scene", "story_day", "rhythm_class", "tone", "tone_undercurrent", "tags",
                     "depth", "target_duration_s", "keep", "merged_into", "from_lines", "five_test", "cardinal",
                     "strands", "origin", "location", "status"]
# The floor plan of a place (5.5 LOCATION): never in the summary.
SET_PLAN_FIELDS = ("plan_orientation", "size", "origin_corner", "axes", "wild_walls", "object", "mark")
# Plain words for stored values, where the value's own words are not plain enough (5.7).
PLAIN_WORDS = {
    "close_up": "close-up", "medium_close_up": "medium close-up", "extreme_close_up": "extreme close-up",
    "medium_wide": "medium wide", "extreme_wide": "extreme wide", "eye_level": "eye level", "worms_eye": "worm's-eye",
    "top_down": "straight down", "frame_left": "frame-left", "frame_right": "frame-right",
    "left_edge": "the left edge", "left_third": "the left third", "centre": "the centre",
    "right_third": "the right third", "right_edge": "the right edge", "two_shot": "two-shot",
    "three_shot": "three-shot", "over_shoulder": "over the shoulder", "near_pov": "near point of view",
    "pov": "point of view", "j_cut": "J-cut", "l_cut": "L-cut", "cut_to_black": "cut to black",
    "match_cut": "match cut", "jump_cut": "jump cut", "smash_cut": "smash cut", "16_9": "16:9", "4_3": "4:3",
    "9_16": "9:16", "2.39": "2.39 to 1", "1.85": "1.85 to 1", "as_look": "as the look", "as_place": "as the place",
    "room_sound_only": "room sound only", "true_silence": "true silence", "drop_out": "the sound drops out",
    "must_keep": "must keep", "main_turn": "the main turn", "start_picture": "a start picture",
    "start_end_pictures": "start and end pictures", "references": "reference pictures", "guide_video": "a guide video",
    "performance_transfer": "a performance copied from a recording", "still_with_move": "a still with a camera move",
    "composite_only": "put together in the edit", "text": "text first", "auto": "chosen by the tools",
    "open": "not decided yet", "none": "none", "yes": "yes", "no": "no", "live_action": "live action",
    "3d_animation": "animation made in 3D", "2d_animation": "drawn animation", "stop_motion_look": "stop-motion style",
    "on_screen": "on screen", "off_screen": "off screen", "hidden": "not seen", "voice_over": "a voice over the picture",
    "device_speaker": "a device's speaker", "helmet_inside": "inside a helmet", "helmet_outside": "outside a helmet",
    "through_glass": "through glass", "thought": "a thought heard aloud", "study_only": "private study only",
    "public_domain": "in the public domain", "mine": "the author's own", "permission": "with permission",
    "not_confirmed": "not confirmed yet", "thought_complete": "the thought is complete",
    "action_midpoint": "the middle of an action", "line_end": "the end of a line", "sound_hit": "a sound",
    "keep_hidden": "keeping something hidden for later", "flip": "flip", "lip_sync": "lip sync", "voice_path": "voice path",
}
# How a shot is made (SHOT route), as whole phrases for the book's "Making it" line (C18).
ROUTE_WORDS = {
    "auto": "made the way the tools choose", "text": "made from a written description first",
    "start_picture": "made from a start picture", "start_end_pictures": "made from start and end pictures",
    "references": "made from reference pictures", "guide_video": "made from a guide video",
    "performance_transfer": "made from a performance copied from a recording",
    "still_with_move": "made from a still with a camera move", "composite_only": "put together in the edit",
}
# How the camera sees a glass surface (SHOT glass camera), in plain words.
GLASS_CAMERA_WORDS = {"through": "seen straight through", "along": "seen along its surface",
                      "angled": "seen at an angle"}
# Plain words for sub-part keys and for field names that have no plain label.
KEY_WORDS = {
    "at": "at", "faces": "facing", "eyeline": "eyes on", "dwell_s": "eyes stay (seconds)", "does": "does",
    "tactic": "tactic", "energy": "energy", "display": "display", "still": "still", "travel": "travel",
    "emphasis": "emphasis", "sound_emphasis": "sound emphasis", "speaker": "speaker", "path": "path",
    "words": "words", "shows": "shows", "why": "why", "when": "when", "state": "state", "camera": "camera",
    "how": "how", "plant": "plants", "payoff": "pays off", "from": "from", "to": "to", "because": "because",
    "meaning_kept": "meaning kept", "posture": "posture", "treatment": "sound", "value": "value",
}
WHOLE_WORD_UNITS = {"mm": "millimetre"}
# Numbers in the records said in words in the book (the second three-scene test: "emphasis 2" meant nothing).
EMPHASIS_WORDS = {"0": "in the background", "1": "seen plainly", "2": "pointed out", "3": "what the shot is about"}
SOUND_EMPHASIS_WORDS = {"0": "under everything", "1": "heard plainly", "2": "brought forward",
                        "3": "what the sound is about"}
# The grey preview ladder of card 22: 0 no 3D at all, 2 a layout check, 3 a guide video, 4 a captured performance.
PREVIS_LEVEL_WORDS = {"0": "no grey preview", "1": "posed grey stills", "2": "a grey layout check in 3D",
                      "3": "a grey guide video the model copies", "4": "a performance filmed on a phone",
                      "5": "a grey preview from open models"}
# An eyeline that is a direction reads "eyes down ...", not "eyes on down ...".
EYELINE_DIRECTION_WORDS = {"up", "down", "away", "ahead", "forward", "back", "left", "right", "out", "off", "frame",
                           "sideways", "inward", "nowhere"}

TYPE_WORDS = {
    "MOTIF": "motif", "PLANT": "plant", "FACT": "fact the audience learns", "RULE": "story-world rule",
    "CAMRULE": "camera rule", "LOOK": "look", "VISUAL": "visual plan", "TEXT": "text in picture",
    "CAMERA": "in-story camera", "STRAND": "strand", "CARDINAL": "event the story needs",
}
SHOT_KIND_WORDS = {"card": "title card", "black": "black", "insert": "insert", "screen": "screen", "pov": "point of view"}

ID_IN_TEXT = re.compile(
    r"(?<![\w-])(?:"
    r"SC\d{2,3}[A-Z]?-(?:SH\d{3}(?:\.\d)?|B\d{2}|D\d{2,3}|V\d+|SU\d{2}|M\d{2}|P\d|C\d{3}|LIST)"
    r"|(?:CH|PR|LOC)-[A-Z0-9]+(?:-[A-Z0-9]+)*\.S\d{2}"
    r"|(?:CHOICE-\d{3}(?:-[A-Z])?)"
    r"|(?:FIND-\d{3}|RT-\d{3}|MU-\d{2}|RV-[A-Z0-9]+)"
    r"|(?:FX|PV|PIC|TK|VT)-[A-Z0-9.]+(?:-[A-Z0-9.]+)*"
    r"|(?:CH|VO|LOC|PR|TX|MO|CAM|WR|LK|CR|VS|RC|LX|PL|FT|ST|CF)-[A-Z0-9]+(?:-[A-Z0-9]+)*"
    r"|SQ\d{2}|CP\d{2}|SC\d{2,3}[A-Z]?"
    r")(?![\w-])")
QUOTED_TEXT = re.compile(r'"[^"\n]*"|“[^”\n]*”')
# The one-of-a-kind film records (no ID but their type), in the user's words, in lists and in free text.
SINGLETON_WORDS = {"PLAN": "the story plan", "STYLE": "the style", "WORLD": "the world",
                   "CAMSYS": "the camera system", "SOUNDPLAN": "the sound plan", "LADDER": "the ladder of closest shots"}
SINGLETON_IN_TEXT = re.compile(r"(?<![\w-])(?:" + "|".join(SINGLETON_WORDS) + r")(?![\w-])")
SINGLETON_FIELDS_IN_TEXT = "peak|break|rung|crisis|climax|step_change|rupture_plan|music_policy|default_height"
SINGLETON_PEAK_IN_TEXT = re.compile(r"(?<![\w-])(" + "|".join(SINGLETON_WORDS) + r")\s+(" + SINGLETON_FIELDS_IN_TEXT
                                    + r")(?:\s+([a-z]+(?:_[a-z]+)+))?(?![\w-])")
# A field or value name written into a free text (tightest_size, whose_scene, push_in): read as plain words.
FIELD_WORD_IN_TEXT = re.compile(r"(?<![\w-])[a-z]+(?:_[a-z]+)+(?![\w-])")
# A unit ID in a text: U-08-SC10-B2, U-07-SC13-P1, U-02-SC01..SC10 (a range of scenes), U-02-CP01.
UNIT_IN_TEXT = re.compile(r"\bU-\d{2}-[A-Z0-9]+(?:\.\.[A-Z0-9]+)?(?:-[A-Z0-9]+)*")
SCENE_ID = re.compile(r"^SC(\d{2,3})([A-Z]?)$")
SHOT_ID = re.compile(r"^(SC\d{2,3}[A-Z]?)-SH(\d{3})$")


# ---------------------------------------------------------------- small plain-word helpers

def is_empty(value):
    return value is None or normalise_word(str(value)) in ("", "none", "null", "n/a")


def plain_value(value):
    """A stored word value in plain words: close_up -> close-up, eye_level -> eye level (5.7)."""
    if value is None:
        return ""
    text = str(value).strip()
    key = normalise_word(text)
    if key in PLAIN_WORDS:
        return PLAIN_WORDS[key]
    if key.startswith("named:"):
        return " ".join(part.capitalize() for part in key[len("named:"):].split("_"))
    if re.fullmatch(r"[a-z0-9_]+", key) and "_" in key:
        return key.replace("_", " ")
    return text


def plain_words_list(value):
    """A word_list value in plain words, joined with commas and 'and'."""
    return join_words([plain_value(piece) for piece in split_list(value or "") if not is_empty(piece)])


def join_words(items):
    items = [item for item in items if item]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def number_text(value):
    """15.0 -> '15', 3.5 -> '3.5'."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.2f}".rstrip("0").rstrip(".")


def seconds_words(value):
    """4 -> '4 seconds', 1 -> '1 second', 3.5 -> '3.5 seconds'."""
    text = number_text(value)
    return f"{text} second" if text == "1" else f"{text} seconds"


def duration_words(seconds):
    """112.5 -> 'about 1 minute 53 seconds'; 2118 -> 'about 35 minutes'."""
    if seconds is None:
        return "not known yet"
    total = int(float(seconds) + 0.5)
    if total < 60:
        return f"about {seconds_words(total)}"
    minutes, rest = divmod(total, 60)
    if minutes >= 10:
        minutes = int(float(seconds) / 60 + 0.5)
        hours, minutes = divmod(minutes, 60)
        if hours:
            return f"about {hours} hour{'s' if hours != 1 else ''}" + (
                f" {minutes} minute{'s' if minutes != 1 else ''}" if minutes else "")
        return f"about {minutes} minutes"
    text = f"about {minutes} minute{'s' if minutes != 1 else ''}"
    if rest:
        text += f" {rest} second{'s' if rest != 1 else ''}"
    return text


def scene_number(scene_identifier):
    """'SC10' -> '10', 'SC06A' -> '6A', 'SC005' -> '5'."""
    match = SCENE_ID.match(scene_identifier or "")
    if not match:
        return scene_identifier or ""
    return f"{int(match.group(1))}{match.group(2)}"


def shot_number_text(shot_identifier):
    """'SC10-SH150' -> '150', 'SC10-SH010' -> '010' (shots keep their three digits, 5.3)."""
    match = SHOT_ID.match(shot_identifier or "")
    return match.group(2) if match else (shot_identifier or "")


def scene_of(identifier):
    match = re.match(r"^(SC\d{2,3}[A-Z]?)(?:-|$)", identifier or "")
    return match.group(1) if match else None


def mid_sentence(title):
    """'The flask' -> 'the flask' for use inside a sentence; names are kept."""
    if not title:
        return title
    for article in ("The ", "A ", "An "):
        if title.startswith(article):
            return article.lower() + title[len(article):]
    return title


def sentence_start(text):
    return text[:1].upper() + text[1:] if text else text


def end_sentence(text):
    text = (text or "").strip()
    if not text:
        return text
    # A closing bracket ends a sentence only after a full stop inside it ("(see 01 Choices.)"), never after
    # "(starting)".
    if text[-1] in ".!?\"”" or (text[-1] == ")" and text[-2:-1] in (".", "!", "?")):
        return text
    return text + "."


def lines_words(value):
    """'397-489' -> 'lines 397 to 489'; '402, 449-463' -> 'lines 402 and 449 to 463'."""
    ranges = parse_line_numbers(value or "")
    if not ranges:
        return ""
    parts = []
    for first, last in ranges:
        parts.append(str(first) if first == last else f"{first} to {last}")
    word = "line" if len(ranges) == 1 and ranges[0][0] == ranges[0][1] else "lines"
    return f"{word} {join_words(parts)}"


def line_numbers_words(value):
    """'454-466' -> '454 to 466'; '402, 449-463' -> '402 and 449 to 463'; '' when the value is not line numbers."""
    ranges = parse_line_numbers(value or "")
    if not ranges:
        return ""
    return join_words([str(first) if first == last else f"{first} to {last}" for first, last in ranges])


def first_sentence(text, words_max=14):
    text = (text or "").strip()
    match = re.match(r"^(.+?[.!?])(\s|$)", text)
    sentence = match.group(1) if match else text
    return sentence if len(sentence.split()) <= words_max else ""


# ---------------------------------------------------------------- the project as it is read for views

class ProjectView:
    """A project's records, merged, with the numbered story and speeches when present, and plain names."""

    def __init__(self, project_folder, schema=None, words=None, constants=None, breakdown=None):
        self.folder = Path(project_folder)
        if schema is None or words is None or constants is None:
            loaded_schema, loaded_words, loaded_constants = load_skill_data()
            schema = schema or loaded_schema
            words = words or loaded_words
            constants = constants or loaded_constants
        self.schema = schema
        self.words = words
        self.constants = constants
        self.project = Project(self.folder, schema, words)
        self.breakdown = breakdown or Breakdown.from_project(self.folder, schema, words, constants)
        self.record_files = self.breakdown.record_files
        self.index = self.breakdown.index
        self.names = PlainNames(self)
        self._steps = None
        self._scope = "unset"
        self._shots = {}
        self._records = {}
        self._beats = {}
        self._turn_beats = {}
        self._list_items = {}

    # -- the project
    @property
    def project_record(self):
        return self.breakdown.project

    def project_value(self, name, default=None):
        record = self.project_record
        value = record.get(name) if record is not None else None
        return default if is_empty(value) else value

    @property
    def title(self):
        return self.project_value("title") or self.folder.name

    @property
    def study_only(self):
        return normalise_word(self.project_value("rights", "") or "") == "study_only"

    @property
    def steps(self):
        if self._steps is None:
            self._steps = load_steps()
        return self._steps

    def constant(self, name, default=None):
        entry = (self.constants or {}).get("constants", {}).get(name)
        if entry is None:
            entry = (self.constants or {}).get("from_blueprint_text", {}).get("constants", {}).get(name)
        if isinstance(entry, dict) and "value" in entry:
            return entry["value"]
        return default if entry is None else entry

    # -- records
    def record(self, identifier, type_name=None):
        return self.breakdown.record(identifier, type_name)

    def records(self, type_name, include_omitted=False):
        key = (type_name, include_omitted)
        if key not in self._records:
            self._records[key] = self.breakdown.records_of(type_name, include_omitted)
        return list(self._records[key])

    def beats(self, scene_identifier):
        if scene_identifier not in self._beats:
            self._beats[scene_identifier] = [beat for beat in self.records("BEAT")
                                              if scene_of(beat.identifier) == scene_identifier]
        return self._beats[scene_identifier]

    def singleton(self, type_name):
        return self.index.get((type_name, None))

    def items(self, record, field_name):
        if record is None:
            return []
        return self.breakdown.items(record, field_name)

    # -- scenes and shots in film order
    def all_scene_ids(self):
        if "all_scene_ids" not in self._records:
            found = {record.identifier for record in self.records("SCENE")}
            for type_name in ("SHOT", "BEAT", "SHOTLIST"):
                found.update(scene_of(record.identifier) for record in self.records(type_name))
            found.discard(None)
            self._records["all_scene_ids"] = sorted(found, key=sort_key_for_identifier)
        return list(self._records["all_scene_ids"])

    def scope(self):
        """The scenes in PROJECT scope, or None for all (7.1 scope; ranges written SC07..SC10 are allowed)."""
        if self._scope != "unset":
            return self._scope
        value = (self.project_value("scope") or "").strip()
        if not value or normalise_word(value) in ("all", "open", "none"):
            self._scope = None
            return None
        known = self.all_scene_ids()
        found = set()
        for piece in split_list(value):
            if ".." in piece:
                first, last = [part.strip() for part in piece.split("..", 1)]
                inside = False
                for identifier in known:
                    if identifier == first:
                        inside = True
                    if inside:
                        found.add(identifier)
                    if identifier == last:
                        inside = False
                found.update((first, last))
            else:
                found.add(piece)
        self._scope = found or None
        return self._scope

    def in_scope(self, scene_identifier):
        scope = self.scope()
        return scope is None or scene_identifier in scope

    def scene_kept(self, scene_identifier):
        scene = self.record(scene_identifier, "SCENE")
        if scene is None:
            return True
        return normalise_word(scene.get("keep") or "keep") not in ("cut", "merge", "fold")

    def film_scene_ids(self):
        """The scenes of the film in story order: in scope, kept, not omitted."""
        if "film_scene_ids" not in self._records:
            self._records["film_scene_ids"] = [
                identifier for identifier in self.all_scene_ids()
                if self.in_scope(identifier) and self.scene_kept(identifier)
                and (self.record(identifier, "SCENE") is not None or self.shots(identifier))]
        return list(self._records["film_scene_ids"])

    def shots(self, scene_identifier):
        if not self._shots:
            for shot in self.records("SHOT"):
                self._shots.setdefault(scene_of(shot.identifier), []).append(shot)
            for shots in self._shots.values():
                shots.sort(key=lambda shot: sort_key_for_identifier(shot.identifier))
            self._shots.setdefault(None, [])
        return self._shots.get(scene_identifier, [])

    def film_shots(self):
        return [shot for scene in self.film_scene_ids() for shot in self.shots(scene)]

    def list_items(self, scene_identifier):
        """[(shot ID, Item)] of the scene's one-line shot list, in list order."""
        if scene_identifier not in self._list_items:
            shot_list = self.record(f"{scene_identifier}-LIST", "SHOTLIST")
            self._list_items[scene_identifier] = [(item.first, item) for item in self.items(shot_list, "item")
                                                  if item.first]
        return self._list_items[scene_identifier]

    def list_item(self, shot_identifier):
        for identifier, item in self.list_items(scene_of(shot_identifier)):
            if identifier == shot_identifier:
                return item
        return None

    def scene_title(self, scene_identifier):
        scene = self.record(scene_identifier, "SCENE")
        if scene is not None and scene.title:
            return scene.title
        location = self.record(scene.get("location"), "LOCATION") if scene is not None else None
        if location is not None and location.title:
            return location.title
        place = scene.get("place_text") if scene is not None else None
        if place:
            words = place.split(" - ")[-1].strip()
            return words[:1].upper() + words[1:].lower() if words.upper() == words else words
        return ""

    def scene_heading_words(self, scene_identifier):
        title = self.scene_title(scene_identifier)
        return f"Scene {scene_number(scene_identifier)}" + (f" - {title}" if title else "")

    def speech(self, identifier):
        return self.breakdown.speech(identifier)

    def is_turn_shot(self, shot):
        return normalise_word(shot.get("role") or "") == "turn"

    def turn_beats(self, scene_identifier):
        """[(beat, 'main' or 'other')] of the scene's turning beats, in beat order."""
        if scene_identifier in self._turn_beats:
            return self._turn_beats[scene_identifier]
        found = []
        for beat in self.beats(scene_identifier):
            turn = normalise_word(beat.get("turn") or "none")
            if turn == "main_turn":
                found.append((beat, "main"))
            elif turn == "turn":
                found.append((beat, "other"))
        self._turn_beats[scene_identifier] = found
        return found

    def turn_shot_for(self, beat_identifier):
        scene = scene_of(beat_identifier)
        for shot in self.shots(scene):
            if self.is_turn_shot(shot) and beat_identifier in split_list(shot.get("beats") or ""):
                return shot
        for identifier, item in self.list_items(scene):
            if normalise_word(item.get("role") or "") == "turn" and beat_identifier in split_list(item.get("beats") or ""):
                return identifier
        return None


# ---------------------------------------------------------------- plain names for records

# A state's title is printed after its element's name in short lists ("Because of", "In the frame") when it has at
# most this many words; a longer one is left to the full lines.
STATE_TITLE_WORDS_SHORT = 6


class PlainNames:
    """Plain names for IDs ("shot 150", "Iona, state 2", "saved choice 1: the reflection two-shot") and a way to
    replace every ID inside a text with its plain name, leaving double-quoted story words alone."""

    def __init__(self, view):
        self.view = view

    def title_of(self, identifier, type_name=None):
        record = self.view.record(identifier, type_name)
        return record.title if record is not None and record.title else None

    def name(self, identifier, scene=None, short=False):
        """The plain name of one ID; scene is the scene the reader is in (so 'beat 7' needs no scene)."""
        identifier = (identifier or "").strip()
        if not identifier:
            return ""
        view = self.view
        own_scene = scene_of(identifier)
        prefix = "" if (scene and own_scene == scene) else (f"scene {scene_number(own_scene)}, " if own_scene else "")
        match = re.match(r"^(SC\d{2,3}[A-Z]?)-(SH|B|D|V|SU|M|P|C)(\d+)(?:\.(\d))?$", identifier)
        if match:
            kind, number = match.group(2), match.group(3)
            if kind == "SH":
                text = f"shot {number}"
                if match.group(4):
                    text += f", clip {match.group(4)}"
                return prefix + text
            if kind == "B":
                return prefix + f"beat {int(number)}"
            if kind == "P":
                title = self.title_of(identifier, "PART")
                return prefix + f"part {int(number)}" + (f" ({mid_sentence(title)})" if title and not short else "")
            if kind == "C":
                return prefix + f"the cut after shot {number}"
            if kind == "M":
                title = self.title_of(identifier, "MOVE")
                if title and not short:
                    return prefix + f"the move where {mid_sentence(title)}"
                move = view.record(identifier, "MOVE")
                mover = self.name(move.get("who"), scene, short=True) if move is not None and move.get("who") else ""
                return prefix + (f"{mover}'s move" + (f" ({mid_sentence(title)})" if title else "") if mover
                                 else "a move of the scene" + (f" ({mid_sentence(title)})" if title else ""))
            if kind == "SU":
                title = self.title_of(identifier, "SETUP")
                if title:
                    head, _, rest = title.partition(":")
                    head = head.strip()
                    head = head[:1].lower() + head[1:] if head.lower().startswith("camera") else head
                    return prefix + (head if short or not rest.strip() else f"{head} ({rest.strip()})")
                return prefix + f"camera setup {int(number)}"
            if kind == "V":
                scene_record = view.record(own_scene, "SCENE")
                for item in view.items(scene_record, "value"):
                    if item.first == identifier and item.get("name"):
                        value_name = item.get("name")
                        if short:
                            value_name = value_name.split(",")[0]
                        return prefix + f"the value {value_name}"
                return prefix + f"value {int(number)}"
            if kind == "D":
                speech = view.speech(identifier)
                if speech:
                    speaker = self.name(speech.get("speaker"), short=True) if speech.get("speaker") else ""
                    words = " ".join((speech.get("text") or "").split())  # the whole speech (C18)
                    if speaker and words:
                        return f'{speaker}\'s line "{words}"'
                    if speaker:
                        return prefix + f"{speaker}'s line"
                return prefix + f"line {int(number)} of the speeches"
        if re.match(r"^SC\d{2,3}[A-Z]?-LIST$", identifier):
            return prefix + "the shot list"
        if SCENE_ID.match(identifier):
            return f"scene {scene_number(identifier)}"
        state = re.match(r"^((?:CH|PR|LOC)-[A-Z0-9-]+)\.S(\d{2})$", identifier)
        if state:
            # a state is named by what it is ("Iona, her palm bandaged"), never by a number a reader cannot use
            element = self.name(state.group(1), short=True)
            title = self.title_of(identifier, "STATE")
            if title and normalise_word(title) != normalise_word(element) and \
                    (not short or len(title.split()) <= STATE_TITLE_WORDS_SHORT):
                return f"{element} ({title[:1].lower() + title[1:]})"
            return element  # a state titled as its thing says nothing more ("Jude's water (jude's water)")
        choice = re.match(r"^CHOICE-(\d{3})(?:-([A-Z]))?$", identifier)
        if choice:
            text = f"choice {int(choice.group(1))}"
            return text + (f", option {choice.group(2).lower()}" if choice.group(2) else "")
        numbered = [(r"^RC-(\d{2})$", "saved choice", "RESERVE"), (r"^LX-(\d{2})$", "lens exception", "LENS"),
                    (r"^FIND-(\d{3})$", "finding", "FINDING"), (r"^RT-(\d{3})$", "rights record", "RIGHTS"),
                    (r"^MU-(\d{2})$", "music cue", "MUSIC"), (r"^CP(\d{2})$", "chapter", "CHAPTER")]
        for pattern, word, type_name in numbered:
            found = re.match(pattern, identifier)
            if found:
                title = self.title_of(identifier, type_name)
                if type_name == "CHAPTER":
                    number_words = roman(int(found.group(1)))
                    return f"chapter {number_words}" + (f" ({title})" if title and not short else "")
                if short and title and type_name in ("RESERVE", "LENS"):
                    return f"{mid_sentence(title)} (a {word})"  # a name a reader can use, not "saved choice 4"
                text = f"{word} {int(found.group(1))}"
                return text + (f": {mid_sentence(title)}" if title and not short else "")
        sequence = re.match(r"^SQ(\d{2})$", identifier)
        if sequence:
            title = self.title_of(identifier, "SEQUENCE")
            text = f"group of scenes {int(sequence.group(1))}"
            return text + (f": {mid_sentence(title)}" if title and not short else "")
        review = re.match(r"^RV-(.+)$", identifier)
        if review:
            target = review.group(1)
            return "the review of the whole film" if target == "FILM" else f"the review of {self.name(target)}"
        job = re.match(r"^(FX|PV|PIC|TK|VT)-(.+)$", identifier)
        if job:
            return self.job_name(job.group(1), job.group(2))
        if identifier in SINGLETON_WORDS:
            # the one-of-a-kind film records have no ID but their type: never print CAMSYS or LADDER to the user
            return SINGLETON_WORDS[identifier]
        record = view.record(identifier)
        if record is not None:
            title = record.title or ""
            if record.type_name in ("CHARACTER", "LOCATION", "PROP"):
                return mid_sentence(title) if title else identifier
            if record.type_name == "VOICE":
                return mid_sentence(title) if title else "a voice"
            if record.type_name == "PROJECT":
                return view.title
            if record.type_name == "VISUAL":
                group = self.name(record.get("sequence") or identifier[3:], short=True) if record.get("sequence") \
                    else self.name(identifier[3:], short=True)
                return f"the visual plan for {group}"
            word = TYPE_WORDS.get(record.type_name)
            if title:
                return f"{mid_sentence(title)} ({word})" if word and not short else mid_sentence(title)
            return word or identifier
        if identifier in ("PROJECT",):
            return view.title
        return identifier

    def job_name(self, kind, rest):
        shot = re.match(r"^(SC\d{2,3}[A-Z]?-SH\d{3})", rest)
        shot_words = self.name(shot.group(1)) if shot else ""
        number = re.search(r"-(?:T|V)?(\d{2})$", rest)
        count = int(number.group(1)) if number else None
        if kind == "FX":
            return f"finishing job {count} for {shot_words}" if shot_words else "a finishing job"
        if kind == "PV":
            return f"grey preview try {count} for {shot_words or 'a scene'}"
        if kind == "TK":
            return f"take {count} of {shot_words}" if shot_words else "a take"
        if kind == "VT":
            speech = re.match(r"^(SC\d{2,3}[A-Z]?-D\d{2,3})", rest)
            return f"voice take {count} of {self.name(speech.group(1))}" if speech else "a voice take"
        return f"a picture for {shot_words}" if shot_words else "a picture"

    def names(self, value, scene=None, short=False):
        return [self.name(piece, scene, short) for piece in split_list(value or "") if not is_empty(piece)]

    def list_words(self, value, scene=None, short=False):
        return join_words(self.names(value, scene, short))

    def text(self, text, scene=None):
        """A free text with every ID replaced by its plain name and every unit by its plain words; double-quoted
        story words and 'mm' after a number are handled so no code or abbreviation is left (WORDS-04)."""
        if not text:
            return text or ""
        pieces = []
        last = 0
        for match in QUOTED_TEXT.finditer(text):
            pieces.append(self._plain_piece(text[last:match.start()], scene))
            pieces.append(match.group(0))
            last = match.end()
        pieces.append(self._plain_piece(text[last:], scene))
        return "".join(pieces)

    def _plain_piece(self, text, scene):
        text = UNIT_IN_TEXT.sub(lambda match: unit_in_plain_words(match.group(0), self.view.steps), text)
        text = ID_IN_TEXT.sub(lambda match: self.name(match.group(0), scene, short=True), text)
        # the one-of-a-kind film records, named by their type in a why ("(PLAN peak tightest_size, Iona)",
        # "(CAMSYS break)", "A break from LADDER"), in the user's words
        text = SINGLETON_PEAK_IN_TEXT.sub(
            lambda match: f"{SINGLETON_WORDS[match.group(1)]}'s {plain_value(match.group(2).lower())}"
                          + (f" for the {plain_value(match.group(3))}" if match.group(3) else ""), text)
        text = SINGLETON_IN_TEXT.sub(lambda match: SINGLETON_WORDS[match.group(0)], text)
        text = FIELD_WORD_IN_TEXT.sub(lambda match: plain_value(match.group(0)), text)
        text = re.sub(r"(\d)\s?mm\b", r"\1 millimetre", text)
        text = re.sub(r"\bline:\s*(\d+)", r"story line \1", text)
        # a cited ID that names what the sentence just said: "stays with Iona (CR-IONA)" reads "stays with Iona"
        text = NAME_REPEATED_IN_BRACKETS.sub(r"\1", text)
        return text

    def story_point(self, value, scene=None):
        """'SC24 "She deletes the way home." = SC24-B05' -> 'scene 24, "She deletes the way home."'."""
        if is_empty(value):
            return ""
        point = parse_story_point(value)
        if point:
            where = self.name(point[0], scene)
            return f'{where}, "{point[1]}"' if where else f'"{point[1]}"'
        value = re.sub(r"\s*=\s*SC\d{2,3}[A-Z]?-B\d{2}\s*$", "", value)
        if ".." in value:
            return self.range_words(value)
        return self.text(value, scene)

    def range_words(self, value):
        """'SC26..SC27' -> 'scenes 26 to 27'; 'SC10-B01..SC10-B08' -> 'beats 1 to 8'."""
        first, _, last = value.partition("..")
        first, last = first.strip(), last.strip()
        if SCENE_ID.match(first) and SCENE_ID.match(last):
            return f"scenes {scene_number(first)} to {scene_number(last)}"
        beat_first = re.match(r"^(SC\d{2,3}[A-Z]?)-B(\d{2})$", first)
        beat_last = re.match(r"^(SC\d{2,3}[A-Z]?)-B(\d{2})$", last)
        if beat_first and beat_last:
            return f"beats {int(beat_first.group(2))} to {int(beat_last.group(2))}"
        return f"{self.name(first)} to {self.name(last)}"

    def because_words(self, value, scene=None):
        """A because list in plain names ('beat 7, the mint (motif), story line 454')."""
        parts = []
        for piece in split_list(value or ""):
            piece = piece.strip()
            if is_empty(piece):
                continue
            if normalise_word(piece) == "default":
                parts.append("the film's defaults")
            elif piece.startswith("line:"):
                reference = piece[5:].strip()
                parts.append(f'story line {reference}' if re.match(r"^\d", reference) else f"the story at {reference}")
            else:
                name = self.name(piece, scene, short=True)
                if any(part.lower() == name.lower() for part in parts):
                    continue  # a plant and its motif of the same name are said once
                if piece.startswith("MO-") and any(name.lower() in part.lower() for part in parts):
                    name = f"{name} as a motif"
                parts.append(name)
        return join_words(parts)


def roman(number):
    values = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
              (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    text = ""
    for value, letters in values:
        while number >= value:
            text += letters
            number -= value
    return text


# ---------------------------------------------------------------- sections of a plain part

class PlainPart:
    """A plain part as a title and sections: [(heading, [lines])]. Sections are '## ' headings (G13)."""

    def __init__(self, title_lines=None, sections=None):
        self.title_lines = title_lines or []
        self.sections = sections or []

    @classmethod
    def from_lines(cls, lines):
        title_lines = []
        sections = []
        current = None
        for line in lines:
            if line.startswith("## "):
                current = (line[3:].strip(), [])
                sections.append(current)
            elif current is None:
                title_lines.append(line)
            else:
                current[1].append(line)
        return cls(title_lines, sections)

    def section(self, heading):
        wanted = heading_key(heading)
        for name, lines in self.sections:
            if heading_key(name) == wanted:
                return lines
        return None

    def to_lines(self):
        lines = list(self.title_lines)
        while lines and not lines[-1].strip():
            lines.pop()
        for heading, body in self.sections:
            body = list(body)
            while body and not body[0].strip():
                body.pop(0)
            while body and not body[-1].strip():
                body.pop()
            lines += ["", f"## {heading}", ""] + body
        return lines


def heading_key(heading):
    return re.sub(r"[^a-z0-9 ]", "", heading.lower()).strip()


def merged_plain_part(title, owned, existing_lines):
    """The new plain part: the title, the owned sections (in order), then every section of the old plain part that
    is not owned, where it was relative to the others."""
    existing = PlainPart.from_lines(existing_lines or [])
    owned_keys = {heading_key(heading) for heading, _ in owned}
    kept = [(heading, lines) for heading, lines in existing.sections if heading_key(heading) not in owned_keys]
    part = PlainPart([f"# {title}"], [(heading, lines) for heading, lines in owned if lines is not None] + kept)
    return part.to_lines()


def plain_part_lines_of(record_file):
    """The lines above the divider of a parsed record file ([] when it has no divider at its top)."""
    for segment in record_file.segments:
        if isinstance(segment, TextBlock):
            for position, line in enumerate(segment.lines):
                if line.strip() == DIVIDER_LINE:
                    return list(segment.lines[:position])
            return list(segment.lines) if not record_file.has_divider else []
        return []
    return []


def replace_plain_part(record_file, lines):
    """Put new plain-part lines above the divider. The records and the END line are not touched; a file without a
    divider at its top gets one. Returns True when the file's text changed."""
    before = render_file(record_file, recount=False)
    new_lines = list(lines)
    while new_lines and not new_lines[-1].strip():
        new_lines.pop()
    first = record_file.segments[0] if record_file.segments else None
    divider_at = None
    if isinstance(first, TextBlock):
        divider_at = next((position for position, line in enumerate(first.lines) if line.strip() == DIVIDER_LINE), None)
    if divider_at is not None:
        rest_lines = first.lines[divider_at:]
        rest_numbers = first.line_numbers[divider_at:]
        first.lines = new_lines + [""] + rest_lines
        first.line_numbers = [None] * (len(new_lines) + 1) + rest_numbers
    elif isinstance(first, TextBlock) and not record_file.has_divider:
        # Free text but no divider: the old text was the plain part.
        first.lines = new_lines + ["", DIVIDER_LINE, ""]
        first.line_numbers = [None] * len(first.lines)
    else:
        block = TextBlock(lines=new_lines + ["", DIVIDER_LINE, ""], line_numbers=[None] * (len(new_lines) + 3))
        record_file.segments.insert(0, block)
    return render_file(record_file, recount=False) != before


# ---------------------------------------------------------------- one line per record, per file

def shot_line(view, shot_identifier, scene=None):
    """'shot 150, close-up, 15 seconds, the turn: Iona chews, stops ...' from the written shot (its moments), else its
    list item."""
    shot = view.record(shot_identifier, "SHOT")
    item = view.list_item(shot_identifier)
    kind = normalise_word((shot.get("kind") if shot is not None else None) or "live")
    size = (shot.get("size") if shot is not None else None) or (item.get("size") if item is not None else None)
    seconds = (shot.get("screen_time") if shot is not None else None) or (item.get("time") if item is not None else None)
    role = normalise_word((shot.get("role") if shot is not None else None) or (item.get("role") if item else "") or "")
    parts = [view.names.name(shot_identifier, scene)]
    if kind in ("card", "black"):
        parts.append(SHOT_KIND_WORDS[kind])
    elif size:
        parts.append(plain_value(size))
    if seconds:
        parts.append(seconds_words(seconds))
    if role == "turn":
        parts.append(turn_words(view, shot_identifier))
    if kind == "screen":
        parts.append("on a screen")
    # a written shot speaks for itself: its moments, in order, are what the picture shows (the shot step may have
    # changed what the approved list said); before it is written, the list's line
    moments = [moment.get("shows") for moment in view.items(shot, "moment") if moment.get("shows")] \
        if shot is not None else []
    shows = "; ".join(moments) if moments else (item.get("shows") if item is not None else None)
    if not shows and shot is not None:
        shows = shot.get("purpose")
    if moments and shot is not None:
        # moments lean on the shot's subject ("her finger draws ..."): say who, when the words do not
        who = next((view.names.name(element_of(subject.first), scene, short=True)
                    for subject in view.items(shot, "subject")
                    if subject.first and element_of(subject.first).startswith("CH-")), None)
        if who and who.lower() not in view.names.text(shows, scene).lower():
            parts.append(f"on {who}")
    head = ", ".join(part for part in parts if part)
    return f"{head}: {view.names.text(shows, scene)}" if shows else head


def turn_words(view, shot_identifier):
    """'the turn' for the main turn's shot, 'the second turn' for a later turn, 'a turn' otherwise."""
    scene = scene_of(shot_identifier)
    shot = view.record(shot_identifier, "SHOT")
    item = view.list_item(shot_identifier)
    beats = split_list((shot.get("beats") if shot is not None else None) or (item.get("beats") if item else "") or "")
    turns = view.turn_beats(scene)
    for position, (beat, kind) in enumerate(turns):
        if beat.identifier in beats:
            if kind == "main":
                return "the turn"
            return "the second turn" if position == 1 else "a turn"
    return "the turn"


def scene_at_a_glance(view, scene_identifier):
    """The At a glance lines of a scene page: the event, then counts, length and where it turns."""
    scene = view.record(scene_identifier, "SCENE")
    names = view.names
    lines = []
    event = scene.get("event") if scene is not None else None
    idea = scene.get("scene_idea") if scene is not None else None
    first = end_sentence(names.text(event, scene_identifier)) if event else ""
    if idea:
        first = (first + " " if first else "") + "The idea: " + end_sentence(names.text(idea, scene_identifier))
    if first:
        lines += [first, ""]
    beats = view.beats(scene_identifier)
    shots = view.shots(scene_identifier)
    items = view.list_items(scene_identifier)
    counts = []
    if beats:
        counts.append(f"{len(beats)} beat{'s' if len(beats) != 1 else ''}")
    kinds = {}
    for shot_identifier, item in ([(shot.identifier, None) for shot in shots] or items):
        record = view.record(shot_identifier, "SHOT")
        kind = normalise_word((record.get("kind") if record is not None else "") or "live")
        kinds[kind] = kinds.get(kind, 0) + 1
    filmed = sum(count for kind, count in kinds.items() if kind not in ("card", "black"))
    if filmed or kinds:
        shot_words = f"{filmed} shot{'s' if filmed != 1 else ''}"
        extras = []
        if kinds.get("card"):
            extras.append("the title card" if kinds["card"] == 1 else f"{kinds['card']} title cards")
        if kinds.get("black"):
            extras.append("a black" if kinds["black"] == 1 else f"{kinds['black']} blacks")
        counts.append(shot_words + (" and " + join_words(extras) if extras else ""))
    length = scene_duration(view.breakdown, scene_identifier) if shots else None
    if not length and items:
        try:
            length = sum(float(item.get("time") or 0) for _, item in items)
        except ValueError:
            length = None
    sentence = ", ".join(counts)
    if length:
        sentence = (sentence + ", " if sentence else "") + duration_words(length)
    if sentence:
        sentence = sentence[:1].upper() + sentence[1:] + "."
    turn_sentences = []
    turns = view.turn_beats(scene_identifier)
    turns = sorted(turns, key=lambda pair: sort_key_for_identifier(pair[0].identifier))
    others = [beat for beat, kind in turns if kind != "main"]
    for beat, kind in turns:
        shot = view.turn_shot_for(beat.identifier)
        shot_identifier = shot.identifier if isinstance(shot, Record) else shot
        if kind == "main":
            label = "The main turn"
        else:
            # earlier turns in story order: "A first turn", "A second turn" (the second test read them backwards)
            label = f"A {ORDINAL_WORDS[min(others.index(beat), len(ORDINAL_WORDS) - 1)]} turn" if len(others) > 1 \
                else "Another turn"
        quote = turn_quote(view, beat, shot_identifier)
        text = f"{label} is beat {int(beat.identifier.rsplit('-B', 1)[1])}"
        if quote:
            text += f", \"{quote}\""
        if shot_identifier:
            text += f", in {names.name(shot_identifier, scene_identifier)}"
        turn_sentences.append(text + ".")
    closing = " ".join([sentence] + turn_sentences).strip()
    if closing:
        lines.append(closing)
    if not lines:
        lines.append("Nothing designed yet for this scene.")
    return lines


ORDINAL_WORDS = ["first", "second", "third", "fourth", "fifth", "later"]


def turn_quote(view, beat, shot_identifier):
    """The words of the first on-screen speech in the turn shot whose cue lies in the turn beat (8 words or fewer)."""
    shot = view.record(shot_identifier, "SHOT") if shot_identifier else None
    if shot is None:
        return ""
    beat_lines = set()
    for first, last in parse_line_numbers(beat.get("lines") or "") or []:
        beat_lines.update(range(first, last + 1))
    for item in view.items(shot, "hear"):
        if normalise_word(item.get("speaker") or "") != "on_screen":
            continue
        speech = view.speech(item.first)
        if not speech:
            continue
        line = speech.get("line")
        if beat_lines and line not in beat_lines:
            continue
        words = (speech.get("text") or "").strip()
        if words and len(words.split()) <= 8:
            return words
    return ""


def scene_shot_lines(view, scene_identifier, shot_identifiers=None):
    if shot_identifiers is None:
        listed = [identifier for identifier, _ in view.list_items(scene_identifier)]
        written = [shot.identifier for shot in view.shots(scene_identifier)]
        shot_identifiers = listed + [identifier for identifier in written if identifier not in listed]
        shot_identifiers = sorted(set(shot_identifiers), key=sort_key_for_identifier)
    lines = [f"- {shot_line(view, identifier, scene_identifier)}" for identifier in shot_identifiers
             if not is_omitted(view.record(identifier, "SHOT"))]
    return lines or ["No shots listed yet."]


def is_omitted(record):
    return record is not None and normalise_word(record.get("status") or "") == "omitted"


def scene_why_lines(view, scene_identifier):
    """'Why it's shot this way': the turn shots' reasons, the scene's idea, saved choices spent, departures from the
    film rules and the departments that change."""
    names = view.names
    scene = view.record(scene_identifier, "SCENE")
    lines = []
    for shot in view.shots(scene_identifier):
        if view.is_turn_shot(shot) and shot.get("why"):
            label = sentence_start(f"{names.name(shot.identifier, scene_identifier)}, {turn_words(view, shot.identifier)}")
            lines.append(f"- {label}: {end_sentence(names.text(shot.get('why'), scene_identifier))}")
    for shot in view.shots(scene_identifier):
        reserves = [piece for piece in split_list(shot.get("because") or "") if piece.startswith("RC-")]
        if reserves and shot.get("why") and not view.is_turn_shot(shot):
            spent = join_words([reserve_label(view, piece) for piece in reserves])
            lines.append(f"- {sentence_start(names.name(shot.identifier, scene_identifier))} spends {spent}: "
                         f"{end_sentence(names.text(shot.get('why'), scene_identifier))}")
    for item in view.items(scene, "departure"):
        what = item.get("what")
        why = item.get("why")
        if what:
            lines.append(f"- A break from {names.name(item.first, short=True)}: {names.text(what, scene_identifier)}"
                         + (f"; {end_sentence(names.text(why, scene_identifier))}" if why else "."))
    for item in view.items(scene, "department_idea"):
        if normalise_word(item.get("holds_baseline") or "no") == "yes":
            continue
        department = sentence_start(plain_value(item.first))
        idea = item.get("idea")
        if idea:
            lines.append(f"- {department}: {end_sentence(names.text(idea, scene_identifier))}")
    if not lines:
        if scene is not None and scene.get("scene_idea"):
            lines.append(f"- {end_sentence(names.text(scene.get('scene_idea'), scene_identifier))}")
        else:
            lines.append("- The reasons are written with each shot once the shots are written.")
    return lines


def choice_mentions_scene(choice, scene_identifier):
    targets = []
    for field_name in ("affects", "locks"):
        targets += split_list(choice.get(field_name) or "")
    for value in choice.get_all("sets"):
        targets.append(split_item(value).first or "")
    for target in targets:
        target = target.strip()
        if target == scene_identifier or target.startswith(scene_identifier + "-") or target.startswith(scene_identifier + "."):
            return True
    return False


def option_text(choice, letter):
    for value in choice.get_all("option"):
        item = split_item(value)
        if normalise_word(item.first or "") == normalise_word(letter or ""):
            return item.get("text") or ""
    return ""


def choice_answer(choice):
    """(letter, text, how) of a choice's answer: how is 'your answer', 'the default' or None when open."""
    status = normalise_word(choice.get("status") or "open")
    answer = choice.get("answer")
    default = split_item(choice.get("default") or "").first if choice.get("default") else None
    if status == "answered" and answer and normalise_word(answer) not in ("open", "defaults"):
        return answer, option_text(choice, answer), "your answer"
    if status in ("answered", "defaulted"):
        letter = answer if answer and normalise_word(answer) not in ("open", "defaults") else default
        return letter, option_text(choice, letter), "the default" if status == "defaulted" else "your answer"
    return None, "", None


def choice_title(choice):
    return choice.title or choice.get("question") or "a choice"


def is_asked(choice):
    return normalise_word(choice.get("asked") or "no") == "yes"


def choice_status(choice):
    return normalise_word(choice.get("status") or "open")


def waiting_line(view, choice, number=None):
    names = view.names
    question = names.text(choice.get("question") or choice_title(choice))
    default_letter = split_item(choice.get("default") or "").first if choice.get("default") else None
    default = option_text(choice, default_letter) if default_letter else ""
    text = end_sentence(question)
    if default:
        text += f" If you say nothing: {names.text(default)}"
    text = text.rstrip(".") + f" ({names.name(choice.identifier)})."
    return f"{number}. {text}" if number is not None else f"- {text}"


def additions_of_scene(view, scene_identifier, with_meaning=False):
    """[(where, what)] of the additions to the story in a scene: SCENE additions and shots' additions. With
    with_meaning, [(where, what, changes meaning: True or False)] (only additions that change what the scene means
    go to the user to keep or cut; the rest are kept and counted)."""
    from .checks_craft_reasons_words import content_words
    names = view.names
    found = []
    cited = set()
    said = []
    scene = view.record(scene_identifier, "SCENE")
    for item in view.items(scene, "additions"):
        if item.first and not is_empty(item.first):
            changes = normalise_word(item.get("changes_meaning") or "yes") != "no"
            found.append((None, names.text(item.first, scene_identifier), changes))
            cited |= set(ID_IN_TEXT.findall(item.first))
            said.append(set(content_words(item.first)))
    for shot in view.shots(scene_identifier):
        value = shot.get("additions")
        if value and not is_empty(value):
            words = set(content_words(value))
            if set(ID_IN_TEXT.findall(value)) & cited or (words and any(
                    len(words & scene_words) >= ADDITION_SAME_SHARE * len(words) for scene_words in said)):
                continue  # the scene's own additions already say it (the second test listed it twice)
            found.append((shot.identifier, names.text(value, scene_identifier), True))
    return found if with_meaning else [(where, what) for where, what, _ in found]


# "Iona (Iona)": a name followed by itself in brackets, once an ID has been put into plain words.
NAME_REPEATED_IN_BRACKETS = re.compile(r"\b([A-Z][\w'’]*(?: [\w'’]+){0,3}) \(\1\)", re.IGNORECASE)
# A shot's addition that shares this much of its main words with one of the scene's additions is the same addition.
ADDITION_SAME_SHARE = 0.8


def scene_beat_lines(view, scene_identifier):
    """'beat 7: Iona chews the leaf; she cannot taste the mint (the main turn)', one line for each beat, so that
    "beat 7" elsewhere in the book leads somewhere."""
    names = view.names
    turns = {beat.identifier: kind for beat, kind in view.turn_beats(scene_identifier)}
    lines = []
    for beat in sorted(view.breakdown.beats_of(scene_identifier), key=lambda record: sort_key_for_identifier(
            record.identifier)):
        words = beat.title or "; ".join(part for part in (beat.get("action"), beat.get("reaction")) if part)
        turn = {"main": " (the main turn)"}.get(turns.get(beat.identifier), " (a turn)" if beat.identifier in turns
                                                 else "")
        lines.append(f"- {names.name(beat.identifier, scene_identifier)}: {names.text(words, scene_identifier)}{turn}")
    return lines


def scene_small_choice_lines(view, scene_identifier):
    names = view.names
    lines = []
    for where, what, changes in additions_of_scene(view, scene_identifier, with_meaning=True):
        place = sentence_start(names.name(where, scene_identifier)) + ": " if where else ""
        what = end_sentence(what).rstrip(".")
        label = "an addition that changes the scene; keep or cut it" if changes else "a small addition, kept"
        lines.append(f"- {place}{what if place else sentence_start(what)} ({label}).")
    for choice in view.records("CHOICE"):
        if not choice_mentions_scene(choice, scene_identifier) or is_asked(choice):
            continue
        letter, text, how = choice_answer(choice)
        if how is None:
            continue
        lines.append(f"- {names.text(choice_title(choice))}: {names.text(text) or 'as the default'} "
                     f"({names.name(choice.identifier)}).")
    return lines or ["- None: everything in this scene comes from the story and the film rules."]


def scene_waiting_lines(view, scene_identifier):
    lines = []
    for choice in view.records("CHOICE"):
        if choice_mentions_scene(choice, scene_identifier) and is_asked(choice) and choice_status(choice) == "open":
            lines.append(waiting_line(view, choice))
    return lines


def scene_file_plain_part(view, record_file, existing):
    stem = Path(record_file.name).stem
    scene_identifier = scene_from_file_name(view, record_file)
    if scene_identifier is None:
        return None
    if " - shots " in stem:
        shot_identifiers = [record.identifier for record in record_file.records if record.type_name == "SHOT"]
        owned = [("At a glance", [f"A batch of shots for {view.names.name(scene_identifier)}, saved as its own file. "
                                  f"The scene's own file has its At a glance and the reasons for its shots."]),
                 ("The shots, one line each", scene_shot_lines(view, scene_identifier, shot_identifiers))]
        return merged_plain_part(stem, owned, existing)
    owned = [("At a glance", scene_at_a_glance(view, scene_identifier)),
             ("The shots, one line each", scene_shot_lines(view, scene_identifier)),
             ("Why it's shot this way", scene_why_lines(view, scene_identifier)),
             ("Small choices I made", scene_small_choice_lines(view, scene_identifier))]
    waiting = scene_waiting_lines(view, scene_identifier)
    owned.append(("Waiting for you", waiting if waiting else None))
    return merged_plain_part(stem, owned, existing)


def scene_from_file_name(view, record_file):
    match = re.match(r"^Scene (\d+)([A-Z]?)\b", Path(record_file.name).name)
    if match:
        digits = int(match.group(1))
        for identifier in view.all_scene_ids():
            found = SCENE_ID.match(identifier)
            if found and int(found.group(1)) == digits and found.group(2) == match.group(2):
                return identifier
    for record in record_file.records:
        scene = scene_of(record.identifier)
        if scene:
            return scene
    return None


def start_here_plain_part(view, existing):
    names = view.names
    manifest = view.project.read_manifest()
    units = manifest.get("units_done", []) or []
    where = []
    if units:
        last = units[-1]
        applied = (last.get("applied") or "")[:10]
        where.append(f"Last saved: {unit_in_plain_words(last.get('unit'), view.steps)}"
                     + (f", on {applied}" if applied else "") + ".")
    elif view.records("SCENE") or view.records("CHAPTER"):
        speeches = len(view.breakdown.speeches)
        read_words = f"{len(view.records('SCENE'))} scene{'s' if len(view.records('SCENE')) != 1 else ''}" \
            if view.records("SCENE") else f"{len(view.records('CHAPTER'))} chapters"
        where.append(f"Step 2 of 12, reading the story: the story is numbered, {read_words}"
                     + (f", {speeches} speeches" if speeches else "") + ".")
    else:
        where.append("Step 1 of 12, starting: the project folder is made and your story is kept safe in Original.")
    scene_records = view.records("SCENE")
    film_scenes = view.film_scene_ids()
    designed = [scene for scene in film_scenes if view.beats(scene)]
    with_shots = [scene for scene in film_scenes if view.shots(scene)]
    shots = sum(len(view.shots(scene)) for scene in film_scenes)
    if scene_records:
        total = len(scene_records)
        scope_words = (f"all {total} scenes" if total != 1 else "its 1 scene") if view.scope() is None else \
            f"{len(film_scenes)} of {total} scene{'s' if total != 1 else ''}"
        where.append(f"This breakdown covers {scope_words}: {len(designed)} designed, "
                     f"{len(with_shots)} with their shots written ({shots} shot{'s' if shots != 1 else ''}).")
    last_run = view.project_value("checker_last_run") or "never"
    where.append(f"Checked by the checker: {last_run}.")
    additions = sum(len(additions_of_scene(view, scene)) for scene in film_scenes)
    if additions:
        where.append(f"{additions} small addition{'s' if additions != 1 else ''} to the story kept; "
                     f"the list is in 01 Choices.")
    stale = [record for record in view.index.values() if normalise_word(record.get("status") or "") == "stale"]
    if stale:
        where.append(f"Out of date and waiting to be redone: {len(stale)} record{'s' if len(stale) != 1 else ''}.")
    waiting = [choice for choice in view.records("CHOICE") if is_asked(choice) and choice_status(choice) == "open"]
    if waiting:
        where.append(f"Waiting for you: {len(waiting)} choice{'s' if len(waiting) != 1 else ''} "
                     f"({join_words([names.name(choice.identifier) for choice in waiting])}), "
                     f"at the top of 01 Choices.")
    else:
        where.append("Waiting for you: nothing.")
    next_lines = []
    if waiting:
        choice = waiting[0]
        next_lines.append(f"Answer {names.name(choice.identifier)}: {end_sentence(names.text(choice.get('question') or choice_title(choice)))} "
                          "Or type: defaults.")
    else:
        found = next_unit_words(view)
        if found:
            next_lines.append(f"Next piece of work: {found}")
    next_lines += [
        "In Claude Code or Claude desktop with this folder, type: Continue my breakdown.",
        "On the Claude website or in ChatGPT: start a new chat in this project, attach the newest save file, and "
        "type: Continue my breakdown.",
        "In Gemini or another chat app: start a new chat, attach the files the last reply named, and type: "
        "Continue my breakdown.",
    ]
    big = []
    for choice in view.records("CHOICE"):
        if choice_status(choice) not in ("answered", "defaulted"):
            continue
        checkpoint = normalise_word(choice.get("checkpoint") or "none")
        if not (is_asked(choice) or checkpoint == "b" or choice.identifier == "CHOICE-002"):
            continue
        letter, text, how = choice_answer(choice)
        big.append(f"{len(big) + 1}. {names.text(choice_title(choice))}: {names.text(text) or 'as the default'} "
                   f"({names.name(choice.identifier)}, {how}).")
    files = [FILES_LINE] + [f"- {name}: {meaning}." for name, meaning in FILES_IN_THIS_FOLDER]
    owned = [("Where things stand", where), ("Next step", next_lines), ("Big choices so far", big or ["None yet."]),
             ("Files in this folder", files)]
    lines = merged_plain_part(view.title, owned, existing)
    part = PlainPart.from_lines(lines)
    if part.section("Word list") is None:
        part.sections.append(("Word list", ["- step: one of the 12 steps of the work, counted from 1.",
                                            "- choice: a question for you with a default answer; the word defaults "
                                            "accepts every default."]))
    if part.section("Log") is None:
        part.sections.append(("Log", []))
    return keep_log_last(part)


def keep_log_last(part):
    """00 Start here keeps its sections in the order of 13.7: the log is the last section above the divider."""
    log = [(heading, lines) for heading, lines in part.sections if heading_key(heading) == "log"]
    others = [(heading, lines) for heading, lines in part.sections if heading_key(heading) != "log"]
    part.sections = others + log
    lines = part.to_lines()
    if log and not log[0][1]:
        lines.append("")
    return lines


def next_unit_words(view):
    """The next unit in plain words, from make_handout when that module can say it."""
    try:
        from . import make_handout
    except ImportError:
        return ""
    finder = getattr(make_handout, "next_unit", None)
    if finder is None:
        return ""
    try:
        found = finder(view.folder)
    except Exception:  # the next unit is a convenience here; the status line stays correct without it
        return ""
    if not found:
        return ""
    # make_handout speaks to the AI (unit IDs and commands); the user never types a command, so only the plain
    # description of the work is kept.
    text = str(found)
    text = re.sub(r"\s*\([^)]*stage\.py[^)]*\)", "", text)
    text = re.sub(r",?\s*(?:work that code does)?:\s*stage\.py.*$", "", text)
    text = re.sub(UNIT_IN_TEXT.pattern + r",\s*", "", text)
    if "stage.py" in text or not text.strip():
        return ""
    text = view.names.text(text)
    text = re.sub(r"\s+", " ", text).strip().rstrip(".")
    return end_sentence(text)


def choices_plain_part(view, existing):
    names = view.names
    waiting, big, small = [], [], []
    for choice in view.records("CHOICE"):
        status = choice_status(choice)
        if status == "open":
            if is_asked(choice):
                waiting.append(waiting_line(view, choice, len(waiting) + 1))
            else:
                small.append(f"- {names.text(choice_title(choice))}: not decided yet ({names.name(choice.identifier)}).")
            continue
        letter, text, how = choice_answer(choice)
        line = f"- {names.text(choice_title(choice))}: {names.text(text) or 'as the default'} ({names.name(choice.identifier)}"
        if is_asked(choice):  # a small choice shown at checkpoint B (asked: no) is still a small choice (SKILL.md)
            big.append(line + f", {how}).")
        else:
            small.append(line + ").")
    additions = []
    for scene in view.film_scene_ids():
        for where, what in additions_of_scene(view, scene):
            place = names.name(where) if where else names.name(scene)
            additions.append(f"- {sentence_start(place)}: {end_sentence(what)}")
    total = len(view.records("CHOICE"))
    glance = [f"{total} choice{'s' if total != 1 else ''}: {len(waiting)} waiting for you, {len(big)} big "
              f"choice{'s' if len(big) != 1 else ''} made and {len(small)} small "
              f"choice{'s' if len(small) != 1 else ''}. Type defaults to accept every default."
              if total else "No choices yet."]
    if additions:
        glance.append(f"{len(additions)} addition{'s' if len(additions) != 1 else ''} to the story, listed at the end: "
                      "keep or cut each one.")
    owned = [("At a glance", glance),
             ("Waiting for you", waiting or ["Nothing is waiting for you."]),
             ("Big choices", big or ["None yet."]),
             ("Small choices I made", small or ["None yet."]),
             ("Additions to the story", additions or None)]
    return merged_plain_part("Choices", owned, existing)


def scene_list_plain_part(view, existing):
    names = view.names
    scenes = sorted(view.records("SCENE", include_omitted=True), key=lambda record: sort_key_for_identifier(record.identifier))
    glance = []
    lines_all = []
    for scene in scenes:
        for first, last in parse_line_numbers(scene.get("lines") or "") or []:
            lines_all += [first, last]
    if scenes:
        sentence = f"{len(scenes)} scene{'s' if len(scenes) != 1 else ''}"
        if all(scene.get("heading") for scene in scenes):
            sentence += ", one for each heading in the story"
        if lines_all:
            sentence += f", from line {min(lines_all)} to line {max(lines_all)}"
        speeches = len(view.breakdown.speeches)
        if speeches:
            sentence += f", with {speeches:,} speech{'es' if speeches != 1 else ''}"
        glance.append(sentence + ".")
        estimate = (view.breakdown.story_map or {}).get("first_estimate") or {}
        minutes = estimate.get("minutes") if isinstance(estimate, dict) else None
        if isinstance(minutes, list) and len(minutes) == 3:
            glance.append(f"As written it runs about {minutes[1]} minutes ({minutes[0]} to {minutes[2]}), by the "
                          "first estimate from the words.")
    scope = view.scope()
    if scope is not None and scenes:
        inside = [scene.identifier for scene in scenes if scene.identifier in scope]
        glance.append(f"This breakdown covers {len(inside)} of them: {join_words([names.name(scene) for scene in inside])}.")
    sequences = view.records("SEQUENCE")
    if sequences:
        glance.append(f"They fall into {len(sequences)} group{'s' if len(sequences) != 1 else ''} of scenes.")
    plan = view.singleton("PLAN")
    if plan is not None and plan.get("climax"):
        glance.append(f"The climax: {names.story_point(plan.get('climax'))}.")
    listing = []
    for scene in scenes:
        parts = [names.name(scene.identifier)]
        title = view.scene_title(scene.identifier)
        if title:
            parts.append(title)
        where = lines_words(scene.get("lines") or scene.get("from_lines") or "")
        if where:
            parts.append(where)
        if scene.get("sequence") and not is_empty(scene.get("sequence")):
            parts.append(names.name(scene.get("sequence"), short=True).replace("group of scenes", "group"))
        if scene.get("scene_intensity") and not is_empty(scene.get("scene_intensity")):
            parts.append(f"scene intensity {scene.get('scene_intensity')}")
        line = "- " + ", ".join(parts)
        event = scene.get("event")
        if event and not is_empty(event):
            line += f": {end_sentence(names.text(event, scene.identifier))}"
        else:
            line += f": {speaking_words(view, scene)}."
        notes = []
        keep = normalise_word(scene.get("keep") or "keep")
        if is_omitted(scene) or keep == "cut":
            notes.append("cut from the film")
        elif keep in ("merge", "fold") and scene.get("merged_into") and not is_empty(scene.get("merged_into")):
            notes.append(f"joined to {names.name(scene.get('merged_into'))}")
        if scope is not None and scene.identifier not in scope:
            notes.append("not in this breakdown yet")
        if notes:
            line += f" ({'; '.join(notes)})"
        listing.append(line)
    owned = [("At a glance", glance or ["No scenes yet."]), ("The scenes, one line each", listing or ["No scenes yet."])]
    return merged_plain_part("Scene list", owned, existing)


def story_plan_plain_part(view, existing):
    names = view.names
    plan = view.singleton("PLAN")
    glance = []
    if plan is not None:
        if plan.get("logline"):
            glance.append(end_sentence(names.text(plan.get("logline"))))
        if plan.get("theme_question"):
            glance.append(f"The question underneath: {end_sentence(names.text(plan.get('theme_question')))}")
        parts = []
        if plan.get("crisis") and not is_empty(plan.get("crisis")):
            parts.append(f"the crisis is {names.story_point(plan.get('crisis'))}")
        if plan.get("climax") and not is_empty(plan.get("climax")):
            parts.append(f"the climax is {names.story_point(plan.get('climax'))}")
        if parts:
            glance.append(sentence_start("; ".join(parts)) + ".")
        for value in plan.get_all("act"):
            item = split_item(value, view.schema.field("PLAN", "act"))
            text = sentence_start(item.first or "an act")
            if item.get("scenes"):
                text += f": {names.story_point(item.get('scenes'))}"
            if item.get("turn"):
                text += f", turning at {names.story_point(item.get('turn'))}"
            glance.append(f"- {end_sentence(text)}")
    if not glance:
        chapters = view.records("CHAPTER")
        words = sum(int(chapter.get("words")) for chapter in chapters
                    if chapter.get("words") and re.fullmatch(r"\d+", chapter.get("words").strip()))
        if chapters:
            glance.append(f"The book has {len(chapters)} chapter{'s' if len(chapters) != 1 else ''}"
                          + (f" and {words:,} words" if words else "") + ". The plan of the whole book comes next: how "
                          "it becomes a film.")
        else:
            glance.append("The story plan is not written yet; it comes at step 3 of 12.")
    owned = [("At a glance", glance)]
    groups = []
    for sequence in view.records("SEQUENCE"):
        text = sentence_start(names.name(sequence.identifier))
        if sequence.get("scenes"):
            text += f", {names.story_point(sequence.get('scenes'))}"
        if sequence.get("story_job"):
            text += f": {end_sentence(names.text(sequence.get('story_job')))}"
        groups.append(f"- {text}")
    owned.append(("Groups of scenes", groups or None))
    plants = []
    for plant in view.records("PLANT"):
        text = sentence_start(mid_sentence(plant.title) if plant.title else names.name(plant.identifier, short=True))
        where = []
        if plant.get("planted_at"):
            where.append(f"planted at {names.story_point(plant.get('planted_at'))}")
        if plant.get("paid_off_at"):
            where.append(f"paid off at {names.story_point(plant.get('paid_off_at'))}")
        if where:
            text += ": " + "; ".join(where)
        plants.append(f"- {end_sentence(text)}")
    owned.append(("Plants and payoffs", plants or None))
    facts = [f"- {end_sentence(names.text(fact.get('what') or fact.title))}" for fact in view.records("FACT")]
    owned.append(("What the audience knows", facts or None))
    chapters = []
    for chapter in view.records("CHAPTER"):
        text = sentence_start(names.name(chapter.identifier, short=True))
        title = re.sub(r"^[IVXLC]+\.\s*", "", chapter.get("title") or chapter.title or "").strip()
        if title:
            text += f", {title}"
        details = []
        where = lines_words(chapter.get("lines") or "")
        if where:
            details.append(where)
        words = chapter.get("words")
        if words and re.fullmatch(r"\d+", words.strip()):
            details.append(f"{int(words):,} words")
        if details:
            text += ": " + ", ".join(details)
        digest = first_sentence(chapter.get("digest") or "", 40)
        if digest:
            text += f". {sentence_start(names.text(digest))}"
        chapters.append(f"- {end_sentence(text)}")
    owned.append(("The chapters, one line each", chapters or None))
    strands = [f"- {sentence_start(names.text(strand.get('name') or strand.title or ''))}: "
               f"{end_sentence(names.text(strand.get('carries') or ''))}" for strand in view.records("STRAND")]
    owned.append(("Strands", strands or None))
    cardinals = [f"- {end_sentence(names.text(cardinal.get('event') or cardinal.title or ''))}"
                 for cardinal in view.records("CARDINAL")]
    owned.append(("Events the story needs", cardinals or None))
    return merged_plain_part("Story plan", owned, existing)


def world_plain_part(view, existing):
    names = view.names
    glance = []
    style = view.singleton("STYLE")
    if style is not None:
        medium = plain_value(style.get("medium")) if style.get("medium") else ""
        words = names.text(style.get("style_words") or "")
        text = "The style: " + ", ".join(part for part in (medium, words) if part)
        glance.append(end_sentence(text))
    world = view.singleton("WORLD")
    if world is not None:
        where = [plain_value(world.get(name)) for name in ("place", "period") if world.get(name) and not is_empty(world.get(name))]
        if where:
            glance.append(f"Where and when: {end_sentence(join_words(where))}")
        for name, label in (("language", "Language"), ("accents", "Accents"), ("signage", "Signs"),
                            ("institutions", "Institutions")):
            value = world.get(name)
            if value and not is_empty(value):
                if name == "language" and re.fullmatch(r"[a-z_]+", value):
                    value = " ".join(part.capitalize() for part in value.split("_"))
                glance.append(f"- {label}: {end_sentence(names.text(plain_value(value) if '_' in value and ' ' not in value else value))}")
    rules = []
    for rule in view.records("RULE"):
        title = sentence_start(mid_sentence(rule.title)) if rule.title else sentence_start(names.name(rule.identifier))
        statement = rule.get("statement")
        rules.append(f"- {title}: {end_sentence(names.text(statement))}" if statement else f"- {title}.")
    owned = [("At a glance", glance or ["The style and the world are not written yet."]),
             ("Rules of the story world", rules or None)]
    return merged_plain_part("World and style", owned, existing)


def speaking_words(view, scene):
    """'Saye speaks 10 times, Iona 4 times, Jude once and Eli once' from SCENE speaking (code_state, step 1)."""
    parts = []
    for value in scene.get_all("speaking"):
        item = split_item(value, view.schema.field("SCENE", "speaking"))
        count = item.get("cues")
        if not item.first or not count or not re.fullmatch(r"\d+", count.strip()):
            continue
        number = int(count)
        times = "once" if number == 1 else "twice" if number == 2 else f"{number} times"
        parts.append(f"{view.names.name(item.first, short=True)} {times}")
    if not parts:
        return "nobody speaks"
    first_name, _, first_times = parts[0].partition(" ")
    parts[0] = f"{first_name} speaks {first_times}" if " " in parts[0] else parts[0]
    return join_words(parts)


def strip_leading_name(description, name):
    if description and name and description.lower().startswith(name.lower() + ","):
        return description[len(name) + 1:].strip()
    return description


def characters_plain_part(view, existing):
    names = view.names
    characters = view.records("CHARACTER")
    glance = []
    spoken = {}
    for entry in view.breakdown.speeches.values():
        speaker = entry.get("speaker")
        if speaker:
            count, first = spoken.get(speaker, (0, None))
            line = entry.get("line")
            spoken[speaker] = (count + 1, line if first is None or (line is not None and line < first) else first)
    if characters:
        glance.append(f"{len(characters)} character{'s' if len(characters) != 1 else ''}: "
                      f"{join_words([names.name(record.identifier) for record in characters])}.")
        if not any(character.get("fixed_description") for character in characters):
            glance.append("Their descriptions and voices come at step 5 of 12 (characters, places and things).")
    listing = []
    for character in characters:
        name = names.name(character.identifier)
        tier = plain_value(character.get("tier")) if character.get("tier") else ""
        head = f"{name}, {tier}" if tier else name
        description = strip_leading_name(character.get("fixed_description") or character.get("role") or "", name)
        count, first = spoken.get(character.identifier, (0, None))
        speaks = ""
        if count:
            speaks = f"speaks {count if count != 1 else 'once'}{' times' if count > 1 else ''}" + \
                (f", first at line {first}" if first else "")
            aliases = split_list(character.get("names") or "")[1:]
            if aliases:
                speaks += "; also called " + join_words([f'"{alias}"' for alias in aliases])
        if description:
            listing.append(f"- {head}: {end_sentence(names.text(description))}" + (f" {sentence_start(speaks)}." if speaks else ""))
        else:
            listing.append(f"- {head}: {speaks}." if speaks else f"- {head}.")
    voices = []
    for voice in view.records("VOICE"):
        text = sentence_start(names.name(voice.identifier))
        description = voice.get("voice_description")
        pace = voice.get("pace_wps")
        line = f"- {text}: {end_sentence(names.text(description))}" if description else f"- {text}."
        if pace and not is_empty(pace):
            line += f" About {number_text(pace)} words a second."
        voices.append(line)
    owned = [("At a glance", glance or ["No characters yet."]),
             ("The characters, one line each", listing or None), ("Voices", voices or None),
             ("The people, one line each", None)]
    return merged_plain_part("Characters and voices", owned, existing)


def places_plain_part(view, existing):
    names = view.names
    locations, props, texts, motifs, cameras = (view.records(type_name) for type_name in
                                                ("LOCATION", "PROP", "TEXT", "MOTIF", "CAMERA"))
    counts = []
    for records, one, many in ((locations, "place", "places"), (props, "thing", "things"),
                               (texts, "piece of text in pictures", "pieces of text in pictures"),
                               (motifs, "motif", "motifs")):
        if records:
            counts.append(f"{len(records)} {one if len(records) == 1 else many}")
    glance = [sentence_start(join_words(counts)) + "."] if counts else ["Nothing yet."]
    places = []
    for location in locations:
        text = f"- {sentence_start(names.name(location.identifier))}"
        job = location.get("story_job") or location.get("dressing")
        if job:
            text += f": {end_sentence(names.text(job))}"
        else:
            text += "."
        if location.get("object") or location.get("mark"):
            text += " It has a floor plan."
        places.append(text)
    things = []
    for prop in props:
        description = prop.get("fixed_description")
        things.append(f"- {sentence_start(names.name(prop.identifier))}: {end_sentence(names.text(description))}"
                      if description else f"- {sentence_start(names.name(prop.identifier))}.")
    text_lines = []
    for text_record in texts:
        words = text_record.get("words")
        label = sentence_start(mid_sentence(text_record.title) if text_record.title else "Text")
        text_lines.append(f'- {label}: reads "{words}".' if words and not is_empty(words) else f"- {label}.")
    motif_lines = []
    for motif in motifs:
        meaning = motif.get("meaning")
        label = sentence_start(mid_sentence(motif.title) if motif.title else names.name(motif.identifier, short=True))
        motif_lines.append(f"- {label}: {end_sentence(names.text(meaning))}" if meaning else f"- {label}.")
    camera_lines = [f"- {sentence_start(mid_sentence(camera.title) if camera.title else 'An in-story camera')}."
                    for camera in cameras]
    owned = [("At a glance", glance), ("Places", places or None), ("Things", things or None),
             ("Text in pictures", text_lines or None), ("Motifs", motif_lines or None),
             ("In-story cameras", camera_lines or None)]
    return merged_plain_part("Places and things", owned, existing)


def state_from_words(view, state):
    value = state.get("from")
    if not value or is_empty(value):
        return ""
    item = split_item(value, view.schema.field("STATE", "from"))
    first = item.first or ""
    if SCENE_ID.match(first):
        return f"from {view.names.name(first)}"
    return ""


def continuity_plain_part(view, existing):
    names = view.names
    states = view.records("STATE")
    elements = {state.get("element") for state in states if state.get("element")}
    glance = [f"{len(states)} state{'s' if len(states) != 1 else ''} for {len(elements)} "
              f"{'person, place or thing' if len(elements) == 1 else 'people, places and things'}."] if states \
        else ["No states yet."]
    listing = []
    for state in states:
        head = sentence_start(names.name(state.identifier, short=True))
        since = state_from_words(view, state)
        if since:
            head += f", {since}"
        line = state.get("state_line")
        listing.append(f"- {head}: {end_sentence(names.text(line))}" if line else f"- {head}.")
    owned = [("At a glance", glance), ("States, one line each", listing or None)]
    return merged_plain_part("Continuity", owned, existing)


def film_rules_plain_part(view, existing):
    names = view.names
    glance = []
    camsys = view.singleton("CAMSYS")
    frame = view.project_value("frame_shape")
    if frame:
        glance.append(f"The frame: {plain_value(frame)}.")
    if camsys is not None:
        parts = []
        if camsys.get("default_move"):
            parts.append(plain_value(camsys.get("default_move")))
        if camsys.get("default_height"):
            parts.append(f"at {names.text(plain_value(camsys.get('default_height')))}")
        if camsys.get("normal_lens_mm"):
            parts.append(f"on the normal lens of {number_text(camsys.get('normal_lens_mm'))} millimetres")
        if parts:
            glance.append("The camera: " + end_sentence(", ".join(parts)))
    soundplan = view.singleton("SOUNDPLAN")
    if soundplan is not None and soundplan.get("music_policy"):
        glance.append(f"Music: {plain_value(soundplan.get('music_policy'))}.")
    owned = [("At a glance", glance or ["The film rules are not written yet."])]
    camera_rules = []
    for rule in view.records("CAMRULE"):
        who = names.name(rule.get("character"), short=True) if rule.get("character") else mid_sentence(rule.title or "")
        parts = []
        for name, label in (("in_control", "in control"), ("losing_control", "losing control"), ("never", "never"),
                            ("closest", "closest")):
            value = rule.get(name)
            if value and not is_empty(value):
                parts.append(f"{label}: {value_words(view, value)}")
        camera_rules.append(f"- {sentence_start(who)}: {end_sentence('; '.join(parts))}" if parts else f"- {sentence_start(who)}.")
    owned.append(("Camera rules for each person", camera_rules or None))
    saved = []
    for reserve in view.records("RESERVE"):
        text = sentence_start(reserve_label(view, reserve.identifier))
        choice = reserve.get("choice")
        if choice:
            text += f": {value_words(view, choice)}"
        uses = reserve.get("max_uses")
        if uses and not is_empty(uses):
            text += f"; {uses_words(uses)}"
        saved.append(f"- {end_sentence(text)}")
    owned.append(("Saved choices", saved or None))
    lenses = []
    for lens in view.records("LENS"):
        text = sentence_start(re.sub(r": .*$", "", names.name(lens.identifier, short=True)))
        if lens.get("mm"):
            text += f": the {number_text(lens.get('mm'))} millimetre lens"
        if lens.get("only_in"):
            text += f", only in {names.list_words(lens.get('only_in'), short=True)}"
        if lens.get("why"):
            text += f"; {names.text(lens.get('why'))}"
        lenses.append(f"- {end_sentence(text)}")
    owned.append(("Lens exceptions", lenses or None))
    looks = []
    for look in view.records("LOOK"):
        label = sentence_start(mid_sentence(look.title) if look.title else "A look")
        block = look.get("look_block")
        looks.append(f"- {label}: {end_sentence(names.text(block))}" if block else f"- {label}.")
    owned.append(("Looks", looks or None))
    visuals = []
    for visual in view.records("VISUAL"):
        label = sentence_start(names.name(visual.identifier))
        parts = []
        for name in ("dominant", "accent", "contrast", "space"):
            value = visual.get(name)
            if value and not is_empty(value):
                parts.append(f"{name}: {names.text(plain_value(value) if re.fullmatch(r'[a-z_]+', value) else value)}")
        visuals.append(f"- {label}" + (f": {end_sentence('; '.join(parts))}" if parts else "."))
    owned.append(("Visual plan by group of scenes", visuals or None))
    sound = []
    if soundplan is not None:
        for name, label in (("music_policy", "Music"), ("voice_policy", "Voices"), ("loudness_target", "Loudness")):
            value = soundplan.get(name)
            if value and not is_empty(value):
                sound.append(f"- {label}: {end_sentence(names.text(plain_value(value) if re.fullmatch(r'[a-z_]+', value) else value))}")
    owned.append(("Sound", sound or None))
    ladder = view.singleton("LADDER")
    rungs = [f"- {end_sentence(rung_words(view, value))}" for value in (ladder.get_all("rung") if ladder is not None else [])]
    owned.append(("The ladder", rungs or None))
    return merged_plain_part("Film rules", owned, existing)


def rights_plain_part(view, existing):
    names = view.names
    rights = view.records("RIGHTS")
    listing = []
    for record in rights:
        label = sentence_start(mid_sentence(record.title) if record.title else names.name(record.identifier))
        parts = []
        if record.get("clearance"):
            parts.append(names.text(plain_value(record.get("clearance"))))
        if record.get("holder") and not is_empty(record.get("holder")):
            parts.append(f"held by {names.text(record.get('holder'))}")
        if record.get("disclosure") and not is_empty(record.get("disclosure")):
            parts.append(f"the credit line: {names.text(record.get('disclosure'))}")
        listing.append(f"- {label}: {end_sentence('; '.join(parts))}" if parts else f"- {label}.")
    glance = [f"{len(rights)} rights record{'s' if len(rights) != 1 else ''}."]
    if view.study_only:
        glance.append(f"{STUDY_ONLY_MARK}: this story is not yours to publish, so every export says so.")
    owned = [("At a glance", glance), ("Rights, one line each", listing or None)]
    return merged_plain_part("Rights and credits", owned, existing)


def job_file_plain_part(view, record_file, existing):
    """The add-on files (storyboard frames, grey preview jobs, pictures, takes, voices, finishing jobs)."""
    names = view.names
    title = Path(record_file.name).stem
    listing = []
    for record in record_file.records:
        label = sentence_start(names.name(record.identifier or record.type_name))
        parts = []
        if record.type_name == "FINISH":
            label = sentence_start(names.name(record.get("shot"))) if record.get("shot") else label
            parts.append(plain_value(record.get("operation") or ""))
            if record.get("tool") and not is_empty(record.get("tool")):
                parts.append(f"with {record.get('tool')}")
            parts.append("done" if normalise_word(record.get("done") or "no") == "yes" else "not done yet")
        elif record.type_name == "MUSIC":
            if record.get("in"):
                parts.append(f"from {names.name(record.get('in'))}")
            if record.get("out"):
                parts.append(f"to {names.name(record.get('out'))}")
            if record.get("function"):
                parts.append(names.text(record.get("function")))
        elif record.type_name == "PREVIS":
            if record.get("level"):
                parts.append(f"level {record.get('level')}")
            if record.get("approved"):
                parts.append(f"approved: {plain_value(record.get('approved'))}")
        elif record.type_name == "PIC":
            if record.get("use"):
                parts.append(plain_value(record.get("use")))
            if record.get("moment"):
                parts.append(names.text(record.get("moment")))
        elif record.type_name == "TAKE":
            if record.get("model"):
                parts.append(record.get("model"))
            if record.get("kept"):
                parts.append(f"kept: {plain_value(record.get('kept'))}")
        elif record.type_name == "VOICETAKE":
            if record.get("verdict"):
                parts.append(f"verdict: {plain_value(record.get('verdict'))}")
        listing.append(f"- {label}: {end_sentence(', '.join(part for part in parts if part))}" if any(parts) else f"- {label}.")
    glance = [f"{len(record_file.records)} job{'s' if len(record_file.records) != 1 else ''} in this file."]
    owned = [("At a glance", glance), ("One line each", listing or None)]
    return merged_plain_part(title, owned, existing)


def generic_plain_part(view, record_file, existing):
    names = view.names
    title = Path(record_file.name).stem
    title = re.sub(r"^\d\d ", "", title)
    listing = [f"- {sentence_start(names.name(record.identifier or record.type_name))}"
               + (f": {mid_sentence(record.title)}" if record.title and record.identifier and record.type_name
                  not in ("CHARACTER", "LOCATION", "PROP") else "") + "."
               for record in record_file.records]
    owned = [("At a glance", [f"{len(record_file.records)} record{'s' if len(record_file.records) != 1 else ''}."]),
             ("One line each", listing or None)]
    return merged_plain_part(title, owned, existing)


def reserve_label(view, identifier):
    """'saved choice 1, the reflection two-shot' (one comma, so it can sit before a colon)."""
    record = view.record(identifier, "RESERVE")
    number = re.match(r"^RC-(\d+)$", identifier or "")
    label = f"saved choice {int(number.group(1))}" if number else view.names.name(identifier, short=True)
    if record is not None and record.title:
        label += f", {mid_sentence(record.title)}"
    return label


def uses_words(value):
    """RESERVE max_uses in words: '2' -> 'used at most 2 times'; 'share | fraction: 0.25' -> 'used in at most a
    quarter of the scenes'."""
    item = split_item(value)
    first = normalise_word(item.first or "")
    if re.fullmatch(r"\d+", first):
        return f"used at most {first} time{'s' if first != '1' else ''}"
    if first == "share":
        fraction = item.get("fraction")
        try:
            share = float(fraction)
            words = {0.25: "a quarter", 0.5: "half", 0.33: "a third", 0.2: "a fifth", 0.1: "a tenth"}.get(round(share, 2))
            return f"used in at most {words or f'{round(share * 100)} in every 100'} of the scenes"
        except (TypeError, ValueError):
            return "used in a share of the scenes"
    if first in ("1_per_scene", "once_per_scene"):
        return "used at most once a scene"
    return f"used {plain_value(item.first)}"


def value_words(view, value, scene=None):
    """Any stored value in plain words: a word or word list in plain words, an item as its first part with its
    sub-parts, a story point as a scene and a quote, free text with its IDs named."""
    names = view.names
    text = (value or "").strip()
    if not text or is_empty(text):
        return "none"
    if " | " in text:
        item = split_item(text)
        head = value_words(view, item.first or "", scene)
        parts = []
        for key, part in item.parts:
            words = value_words(view, part, scene)
            parts.append(words if key in ("at",) and words.startswith("scene") else f"{KEY_WORDS.get(key, key.replace('_', ' '))} {words}")
        return head + (", " + ", ".join(parts) if parts else "")
    if parse_story_point(text):
        return names.story_point(text, scene)
    pieces = [piece.strip() for piece in text.split(",")]
    if len(pieces) > 1 and all(re.fullmatch(r"[a-z0-9_ ]+", piece) for piece in pieces):
        return join_words([plain_value(normalise_word(piece)) for piece in pieces])
    if re.fullmatch(r"[a-z0-9_.:]+", text):
        return plain_value(text)
    if ID_IN_TEXT.fullmatch(text):
        return names.name(text, scene, short=True)
    return names.text(text, scene)


def rung_words(view, value):
    """A LADDER rung: 'scene 10, "Her face changes.": close-up, held long; the turn happens inside her mouth ...'."""
    item = split_item(value)
    where = view.names.story_point(item.first or "") if item.first else ""
    parts = []
    if item.get("size"):
        parts.append(plain_value(item.get("size")))
    if item.get("hold"):
        hold = normalise_word(item.get("hold"))
        # the rung's hold values are short, medium, long and hold (held past the longest pause)
        parts.append("held past the longest pause" if hold == "hold" else f"held {plain_value(item.get('hold'))}")
    text = where + (": " + ", ".join(parts) if parts else "")
    if item.get("why"):
        text += f"; {view.names.text(item.get('why'))}"
    return sentence_start(text)


FILE_VIEWS = {
    START_HERE: start_here_plain_part, CHOICES_FILE: choices_plain_part, SCENE_LIST_FILE: scene_list_plain_part,
    "05 Story plan.md": story_plan_plain_part, "06 World and style.md": world_plain_part,
    "07 Characters and voices.md": characters_plain_part, "08 Places and things.md": places_plain_part,
    "09 Continuity.md": continuity_plain_part, "10 Film rules.md": film_rules_plain_part,
    "22 Rights and credits.md": rights_plain_part,
}
JOB_FILES = ("18 Storyboard/", "19 Grey previews/", "20 Prompts for AI video/", "21 Edit and finishing/")


def plain_part_for(view, record_file):
    """The new plain part of one record file, or None when code does not write it (12, 13)."""
    name = record_file.name
    if name in CHECKER_FILES:
        return None
    existing = plain_part_lines_of(record_file)
    if name in FILE_VIEWS:
        return FILE_VIEWS[name](view, existing)
    if name.startswith(SCENES_FOLDER + "/"):
        return scene_file_plain_part(view, record_file, existing)
    if name.startswith(JOB_FILES):
        return job_file_plain_part(view, record_file, existing)
    return generic_plain_part(view, record_file, existing)


# ---------------------------------------------------------------- 02 Whole-film summary

# C25: the summary holds one line per record with only the fields step 7 reads, in this order per type.
SUMMARY_FIELDS = {
    "SCENE": ["lines", "characters", "presentation", "host", "event", "sequence", "scene_intensity", "whose_scene",
              "tone", "tags", "target_duration_s", "keep", "merged_into", "from_lines"],
    "PLAN": ["logline", "theme_question", "core_value", "crisis", "climax", "pov_plan", "genre", "tone_home",
             "tone_range", "tone_mix_rule"],
    "SEQUENCE": ["title", "scenes", "value_change", "act"],
    "PLANT": ["what", "planted_at", "paid_off_at", "plot_event", "motif"],
    "FACT": ["what", "element", "audience_knows_from", "mode"],
    "CHAPTER": ["title", "lines", "digest"],
    "STRAND": ["title", "chapters"],
    "CARDINAL": ["what", "chapter"],
    "WORLD": ["place", "period", "drives_on", "language"],
    "RULE": ["kind", "statement", "governs", "era", "exception"],
    "CHARACTER": ["names", "tier", "role", "fixed_description", "height_m", "voice"],
    "VOICE": ["character", "pitch", "pace_wps", "accent"],
    "LOCATION": ["story_job", "room_sound", "anchor"],
    "PROP": ["names", "fixed_description", "side", "motif"],
    "TEXT": ["kind", "words", "on", "origin", "plot_critical"],
    "MOTIF": ["meaning", "rank", "channel", "signature"],
    "CAMERA": ["at", "lens_mm", "ratio", "moves"],
    "STATE": ["from", "state_line", "handedness"],
}
# Values the summary leaves out because they say the usual thing (a normal scene, a state not mirrored).
SUMMARY_USUAL_VALUES = {("SCENE", "presentation"): "normal", ("STATE", "handedness"): "original"}
# Fields whose sub-parts the summary leaves out, keeping the first part (a state's from: its scene).
SUMMARY_FIRST_PART_ONLY = {("STATE", "from"), ("PROP", "side"), ("SCENE", "speaking")}
# When the summary is over summary_words_max, record types are left out in this order (the lowest priority first):
# code surfaces give each step-7 handout the records it needs anyway, so only chat surfaces miss these.
# The continuity states stay longest: in a chat, 09 Continuity is not attached to a scene's chat, while 08 Places and
# things is (when the place has a floor plan).
SUMMARY_DROP_ORDER = ["CARDINAL", "STRAND", "CAMERA", "VOICE", "WORLD", "TEXT", "PROP", "MOTIF", "LOCATION",
                      "PLANT", "STATE"]
SUMMARY_TEXT_WORDS_MAX = 30
SUMMARY_TEXT_WORDS_SHORT = 12


def shortened(value, most):
    """A long text value cut to its first most words, with ' ...' when cut."""
    words = value.split()
    return value if len(words) <= most else " ".join(words[:most]) + " ..."


def summary_record_line(view, record, most_words=SUMMARY_TEXT_WORDS_MAX):
    """One line for a record, its heading carrying only the fields step 7 reads:
    '### SCENE SC10 Saye's kitchen | event: ... | sequence: SQ04'. The file stays a record file (one record per line,
    no field lines), so its END line counts them."""
    fields = SUMMARY_FIELDS.get(record.type_name, [])
    pieces = []
    for name in fields:
        values = record.get_all(name)
        values = [value for value in values if value and not is_empty(value)]
        usual = SUMMARY_USUAL_VALUES.get((record.type_name, name))
        if usual is not None:
            values = [value for value in values if normalise_word(value) != usual]
        if (record.type_name, name) in SUMMARY_FIRST_PART_ONLY:
            values = [split_item(value).first or value for value in values]
        if not values:
            continue
        value = "; ".join(values)
        pieces.append(f"{name}: {shortened(value, most_words)}")
    head = " ".join(piece for piece in (record.type_name, record.identifier, record.title) if piece)
    return "### " + " | ".join([head] + [piece.replace("\n", " ") for piece in pieces])


def summary_words_limit(view):
    """summary_words_max from rules/constants.json (else limits.json's whole_film_summary_words_max, else 6,000)."""
    try:
        value = view.constant("summary_words_max", None)
        if value:
            return int(value)
    except (TypeError, ValueError, AttributeError):
        pass
    try:
        from .record_format import load_json
        return int(load_json("rules/limits.json").get("whole_film_summary_words_max", {}).get("value", 6000))
    except (OSError, ValueError, TypeError):
        return 6000


def whole_film_summary_text(view):
    """The text of 02 Whole-film summary (6.1, C25): plain part, divider, one line per record with only the fields
    step 7 reads, and the END line; the whole file within summary_words_max words: long texts are first cut to their
    first words, then the lowest-priority record types are left out, and the plain part says so."""
    limit = summary_words_limit(view)
    records = []
    for type_name in SUMMARY_TYPES:
        records += view.records(type_name)
    dropped_types = []
    most_words = SUMMARY_TEXT_WORDS_MAX
    while True:
        kept = [record for record in records if record.type_name not in dropped_types]
        body = [summary_record_line(view, record, most_words) for record in kept]
        text = summary_file_text(view, kept, body, most_words, dropped_types, limit)
        if len(text.split()) <= limit:
            return text
        if most_words > SUMMARY_TEXT_WORDS_SHORT:
            most_words = SUMMARY_TEXT_WORDS_SHORT  # first shorten every long text to its first words
            continue
        remaining = [type_name for type_name in SUMMARY_DROP_ORDER if type_name not in dropped_types
                     and any(record.type_name == type_name for record in records)]
        if not remaining:
            return summary_file_text(view, kept, body, most_words, dropped_types, limit, still_over=True)
        dropped_types.append(remaining[0])


def summary_file_text(view, kept, body, most_words, dropped_types, limit, still_over=False):
    """The whole summary file for one choice of what it keeps."""
    counts = {}
    for record in kept:
        counts[record.type_name] = counts.get(record.type_name, 0) + 1
    words = sum(len(line.split()) for line in body)
    held = join_words([f"{counts[type_name]} {word}{'s' if counts[type_name] != 1 else ''}"
                       for type_name, word in (("SCENE", "scene"), ("CHARACTER", "character"), ("LOCATION", "place"),
                                               ("PROP", "thing"), ("STATE", "state")) if counts.get(type_name)])
    glance = [
        "Made by the tools from files 04 to 09 for the scene work: one line for each record, with only what the "
        "scene design reads: the scene list with its events, the story plan, the characters and their voices, the "
        "places and things without their floor plans, and the continuity states. The film rules are in 10 Film "
        "rules, whole. Never edit this file: it is made again after every change to those files.",
        "",
        f"It holds {held or 'no records yet'}, in about {words:,} words (the whole file stays under {limit:,}).",
    ]
    if most_words < SUMMARY_TEXT_WORDS_MAX:
        glance += ["", f"To stay short, long descriptions are cut to their first {most_words} words (the full text is in "
                       "files 04 to 09)."]
    if dropped_types:
        left_out = join_words([view.schema.data["record_types"][type_name].get("plain_name", type_name.lower())
                               for type_name in dropped_types])
        glance += ["", f"To stay within about {limit:,} words it leaves out these kinds of record: {left_out}. Files "
                       "04 to 09 hold them whole; on a code surface each scene's handout brings the ones it "
                       "needs."]
    if still_over:
        glance += ["", f"It is still longer than about {limit:,} words; attach only the part a chat needs, or work on "
                       "a code surface."]
    lines = ["# Whole-film summary", "", "## At a glance", ""] + glance + ["", DIVIDER_LINE, ""] + body
    lines += ["", f"END OF FILE | Whole-film summary | {len(kept)} records"]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- building every view

class ViewsResult:
    def __init__(self):
        self.changed = []
        self.unchanged = []
        self.skipped = []
        self.problems = []

    def summary(self):
        return (f"remade the plain part of {len(self.changed)} file{'s' if len(self.changed) != 1 else ''}"
                + (f"; {len(self.problems)} could not be remade" if self.problems else ""))


_RECENT_VIEWS = {}


def record_files_signature(folder, names):
    signature = []
    for name in names:
        path = Path(folder) / name
        try:
            stat = path.stat()
            signature.append((name, stat.st_mtime_ns, stat.st_size))
        except OSError:
            signature.append((name, None, None))
    return tuple(signature)


def recent_view(project_folder):
    """The ProjectView build_views just used for this folder, when no record file changed since (stage.py build
    calls build_views and then make_exports.write_breakdown_json on the same records); else None."""
    folder = str(Path(project_folder).resolve())
    kept = _RECENT_VIEWS.get(folder)
    if kept is None:
        return None
    view, names, signature = kept
    return view if record_files_signature(folder, names) == signature else None


def build_views(project_folder, schema=None, words=None, constants=None, include_summary=True, view=None):
    """Remake the plain part of every record file (except 12 and 13, which the checker writes), the status part of
    00 Start here, and 02 Whole-film summary. Records are never changed. Returns a ViewsResult; a file that cannot
    be remade is listed in its problems and the others are still made."""
    view = view or ProjectView(project_folder, schema, words, constants)
    result = ViewsResult()
    for record_file in view.record_files:
        try:
            lines = plain_part_for(view, record_file)
            if lines is None:
                result.skipped.append(record_file.name)
                continue
            path = view.folder / record_file.name
            fresh = parse_file(path, record_file.name, view.schema)
            if replace_plain_part(fresh, lines):
                write_text_exactly(path, render_file(fresh, recount=False))
                result.changed.append(record_file.name)
            else:
                result.unchanged.append(record_file.name)
        except Exception as error:  # one file's view must never stop build; the problem is reported instead
            result.problems.append(f"The plain part of {record_file.name} could not be remade: "
                                   f"{type(error).__name__}: {error}")
    try:
        result.changed += write_storyboard_pages(view)
    except Exception as error:  # reported, never fatal (see above)
        result.problems.append(f"The storyboard pages could not be made: {type(error).__name__}: {error}")
    if include_summary and any(view.records(type_name) for type_name in ("SCENE", "CHARACTER", "LOCATION", "STATE")):
        try:
            text = whole_film_summary_text(view)
            path = view.folder / SUMMARY_FILE
            old = path.read_text(encoding="utf-8") if path.is_file() else None
            if old != text:
                write_text_exactly(path, text)
                result.changed.append(SUMMARY_FILE)
        except Exception as error:  # reported, never fatal (see above)
            result.problems.append(f"{SUMMARY_FILE} could not be made: {type(error).__name__}: {error}")
    names = [record_file.name for record_file in view.record_files]
    folder = str(view.folder.resolve())
    _RECENT_VIEWS.pop(folder, None)
    while len(_RECENT_VIEWS) >= 4:  # a long-running caller (a test) keeps only the last few
        _RECENT_VIEWS.pop(next(iter(_RECENT_VIEWS)))
    _RECENT_VIEWS[folder] = (view, names, record_files_signature(folder, names))
    return result


def write_text_exactly(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".part")
    with open(temporary, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    temporary.replace(path)


# ---------------------------------------------------------------- the storyboard page (blueprint 10)

STORYBOARD_FOLDER = "18 Storyboard"
FRAME_RATIOS = {"2.39": "2.39 / 1", "1.85": "1.85 / 1", "16_9": "16 / 9", "4_3": "4 / 3", "9_16": "9 / 16"}


def storyboard_frames(view):
    """{shot ID: the approved storyboard PIC record} (the first approved one, by ID)."""
    frames = {}
    for record in view.records("PIC"):
        if normalise_word(record.get("use") or "") != "storyboard":
            continue
        if normalise_word(record.get("approved") or "no") != "yes":
            continue
        target = record.get("for") or ""
        if SHOT_ID.match(target) and target not in frames:
            frames[target] = record
    return frames


def storyboard_labels(view, shot):
    """The labels the page adds (never drawn into the frame, C2 R3): a hold, the sound, where the eyes go."""
    labels = []
    held = normalise_word(shot.get("held") or "no") == "yes" or view.is_turn_shot(shot)
    if held and shot.get("screen_time"):
        labels.append(f"HOLD {number_text(shot.get('screen_time'))} SECONDS")
    silence = normalise_word(shot.get("silence") or "none")
    if silence in ("room_sound_only", "true_silence", "drop_out"):
        labels.append({"room_sound_only": "ROOM SOUND ONLY", "true_silence": "SILENCE",
                       "drop_out": "THE SOUND DROPS OUT"}[silence])
    try:
        from .derive_fields import eyeline_sides
        for character, side in (eyeline_sides(view.breakdown, shot) or {}).items():
            if side in ("frame_left", "frame_right"):
                arrow = "\u2190" if side == "frame_left" else "\u2192"
                labels.append(f"{view.names.name(character, short=True).upper()} LOOKS {arrow}")
    except Exception:  # an eyeline the plan cannot give is simply not labelled
        pass
    return labels


def storyboard_page(view, scene_identifier, frames):
    names = view.names
    shots = [shot for shot in view.shots(scene_identifier) if shot.identifier in frames
             or normalise_word(shot.get("storyboard") or "no") == "yes"]
    ratio = FRAME_RATIOS.get(normalise_word(view.project_value("frame_shape") or "2.39"), "2.39 / 1")
    slides = []
    for position, shot in enumerate(shots, start=1):
        frame = frames.get(shot.identifier)
        heard = []
        for item in view.items(shot, "hear"):
            speech = view.speech(item.first) if item.first else None
            if speech and speech.get("text"):
                speaker = names.name(speech.get("speaker"), short=True) if speech.get("speaker") else ""
                heard.append(f"{speaker}: \u201c{speech['text']}\u201d" if speaker else f"\u201c{speech['text']}\u201d")
        if frame is not None and frame.get("file") and not is_empty(frame.get("file")):
            source = "../" + quote(frame.get("file").replace("\\", "/"))
            picture = f'<img src="{html.escape(source)}" alt="{html.escape(shot_line(view, shot.identifier, scene_identifier))}">'
        else:
            picture = '<div class="missing">frame to come</div>'
        labels = "".join(f'<span class="label">{html.escape(label)}</span>' for label in storyboard_labels(view, shot))
        item = view.list_item(shot.identifier)
        line = item.get("shows") if item is not None and item.get("shows") else shot.get("purpose") or ""
        slides.append(
            f'<section class="slide" id="shot-{shot_number_text(shot.identifier)}">'
            f'<div class="frame">{picture}<div class="labels">{labels}</div></div>'
            f'<p class="shot">{html.escape(names.name(shot.identifier, scene_identifier))}, '
            f'{html.escape(seconds_words(shot.get("screen_time")) if shot.get("screen_time") else "")}'
            f'<span class="count">{position} of {len(shots)}</span></p>'
            f'<p>{html.escape(names.text(line, scene_identifier))}</p>'
            + "".join(f'<p class="words">{html.escape(words)}</p>' for words in heard) + "</section>")
    title = view.scene_heading_words(scene_identifier)
    return STORYBOARD_PAGE.format(title=html.escape(f"{title}: storyboard"), heading=html.escape(title),
                                  ratio=ratio, slides="\n".join(slides),
                                  mark=f"<p>{STUDY_ONLY_MARK}.</p>" if view.study_only else "")


def write_storyboard_pages(view):
    """Write 18 Storyboard/Scene NN.html for every scene with an approved storyboard frame. Returns the names."""
    frames = storyboard_frames(view)
    written = []
    for scene in sorted({scene_of(target) for target in frames}, key=sort_key_for_identifier):
        name = f"{STORYBOARD_FOLDER}/Scene {scene_number(scene)}.html"
        path = view.folder / name
        text = storyboard_page(view, scene, frames)
        if not path.is_file() or path.read_text(encoding="utf-8") != text:
            write_text_exactly(path, text)
            written.append(name)
    return written


STORYBOARD_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
body {{ margin: 0; background: #111; color: #eee; font: 17px/1.5 Georgia, serif; }}
main {{ max-width: 60rem; margin: 0 auto; padding: 1rem; }}
h1 {{ font-size: 1.3rem; font-weight: normal; }}
.slide {{ display: none; }}
.slide.shown {{ display: block; }}
.frame {{ position: relative; aspect-ratio: {ratio}; background: #000; overflow: hidden; }}
.frame img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
.missing {{ display: flex; align-items: center; justify-content: center; height: 100%; color: #888; }}
.labels {{ position: absolute; left: 0; right: 0; bottom: 0; padding: 0.4rem; }}
.label {{ background: rgba(0,0,0,0.7); color: #fff; font: 13px/1.4 sans-serif; padding: 0.1rem 0.4rem; margin-right: 0.4rem; }}
.shot {{ font-weight: bold; }}
.count {{ float: right; font-weight: normal; color: #aaa; }}
.words {{ color: #ccc; font-style: italic; }}
nav button {{ font: inherit; margin-right: 0.5rem; }}
@media print {{ body {{ background: #fff; color: #000; }} .slide {{ display: block; break-inside: avoid; }} nav {{ display: none; }} }}
</style>
</head>
<body>
<main>
<h1>{heading}: storyboard. Watch it with the sound off; name only the frames to redo.</h1>
{mark}
<nav><button id="back">Back</button><button id="next">Next</button> (or the arrow keys)</nav>
{slides}
</main>
<script>
var slides = document.querySelectorAll(".slide"), at = 0;
function show(n) {{ if (!slides.length) return; at = Math.max(0, Math.min(slides.length - 1, n));
  slides.forEach(function (s, i) {{ s.classList.toggle("shown", i === at); }}); }}
document.getElementById("back").onclick = function () {{ show(at - 1); }};
document.getElementById("next").onclick = function () {{ show(at + 1); }};
document.addEventListener("keydown", function (e) {{ if (e.key === "ArrowRight") show(at + 1); if (e.key === "ArrowLeft") show(at - 1); }});
show(0);
</script>
</body>
</html>
"""


# ---------------------------------------------------------------- the book

class Book:
    """The book as blocks, written out both as Markdown and as one printable HTML page."""

    def __init__(self, title):
        self.title = title
        self.blocks = []

    def heading(self, text, level=2, anchor=None):
        self.blocks.append(("heading", level, text, anchor or slug(text)))

    def paragraph(self, text):
        if text:
            self.blocks.append(("paragraph", text))

    def label(self, text):
        self.blocks.append(("label", text))

    def bullets(self, items):
        items = [item for item in items if item]
        if items:
            self.blocks.append(("bullets", items))

    def numbered(self, items):
        items = [item for item in items if item]
        if items:
            self.blocks.append(("numbered", items))

    def details(self, summary, rows):
        self.blocks.append(("details", summary, rows))

    def contents(self, entries):
        self.blocks.append(("contents", entries))

    def to_markdown(self):
        lines = []
        for block in self.blocks:
            kind = block[0]
            if kind == "heading":
                level = min(block[1], 2)
                lines += ["#" * level + " " + block[2], ""]
            elif kind == "paragraph":
                lines += [block[1], ""]
            elif kind == "label":
                lines += [f"**{block[1]}**", ""]
            elif kind == "bullets":
                lines += [f"- {item}" for item in block[1]] + [""]
            elif kind == "numbered":
                lines += [f"{number}. {item}" for number, item in enumerate(block[1], start=1)] + [""]
            elif kind == "contents":
                lines += [f"{number}. [{text}](#{anchor})" for number, (text, anchor) in enumerate(block[1], start=1)]
                lines.append("")
            elif kind == "details":
                lines.append("<details>")
                lines.append(f"<summary>{html.escape(block[1], quote=False)}</summary>")
                lines.append("")
                lines += [f"- **{label}:** {value}" for label, value in block[2]]
                lines += ["", "</details>", ""]
        while lines and not lines[-1].strip():
            lines.pop()
        return "\n".join(lines) + "\n"

    def to_html(self):
        escape = lambda text: html.escape(text, quote=False)  # noqa: E731
        body = []
        for block in self.blocks:
            kind = block[0]
            if kind == "heading":
                level = min(block[1], 2)
                body.append(f'<h{level} id="{html.escape(block[3])}">{escape(block[2])}</h{level}>')
            elif kind == "paragraph":
                body.append(f"<p>{escape(block[1])}</p>")
            elif kind == "label":
                body.append(f'<p class="label">{escape(block[1])}</p>')
            elif kind == "bullets":
                body.append("<ul>" + "".join(f"<li>{escape(item)}</li>" for item in block[1]) + "</ul>")
            elif kind == "numbered":
                body.append("<ol>" + "".join(f"<li>{escape(item)}</li>" for item in block[1]) + "</ol>")
            elif kind == "contents":
                body.append('<ol class="contents">' + "".join(
                    f'<li><a href="#{html.escape(anchor)}">{escape(text)}</a></li>' for text, anchor in block[1]) + "</ol>")
            elif kind == "details":
                rows = "".join(f"<dt>{escape(label)}</dt><dd>{escape(value)}</dd>" for label, value in block[2])
                body.append(f"<details><summary>{escape(block[1])}</summary><dl>{rows}</dl></details>")
        return BOOK_PAGE.format(title=escape(self.title), body="\n".join(body))


BOOK_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{ --ink: #1d1d1b; --soft: #5b5b57; --line: #d8d6cf; --paper: #fbfaf6; --mark: #7a4b12; }}
body {{ margin: 0; background: var(--paper); color: var(--ink); font: 17px/1.55 Georgia, "Times New Roman", serif; }}
main {{ max-width: 46rem; margin: 0 auto; padding: 2rem 1rem 4rem; }}
h1 {{ font-size: 2rem; line-height: 1.2; margin: 0 0 1rem; }}
h2 {{ font-size: 1.35rem; margin: 2.5rem 0 0.75rem; padding-top: 0.75rem; border-top: 1px solid var(--line); }}
p.label {{ font-weight: bold; margin: 1.25rem 0 0.25rem; }}
ul, ol {{ padding-left: 1.4rem; }}
li {{ margin: 0.2rem 0; }}
details {{ border: 1px solid var(--line); border-radius: 4px; margin: 0.4rem 0; padding: 0.3rem 0.6rem; background: #fff; }}
summary {{ cursor: pointer; }}
dl {{ display: grid; grid-template-columns: max-content 1fr; gap: 0.2rem 0.8rem; margin: 0.6rem 0; }}
dt {{ color: var(--soft); }}
dd {{ margin: 0; }}
.contents a {{ color: var(--mark); }}
@media print {{
  body {{ background: #fff; font-size: 11pt; }}
  main {{ max-width: none; padding: 0; }}
  h2 {{ break-before: page; border-top: none; }}
  details {{ border: none; padding: 0; }}
  summary {{ list-style: none; }}
}}
</style>
</head>
<body>
<main>
{body}
</main>
<script>
window.addEventListener("beforeprint", function () {{
  document.querySelectorAll("details").forEach(function (item) {{ item.open = true; }});
}});
</script>
</body>
</html>
"""


def slug(text):
    """The anchor GitHub gives a Markdown heading: lowercase, spaces as hyphens, punctuation removed."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


# Words the book uses, in plain words (5.7); the word list of 00 Start here is added after them.
BOOK_WORDS = [
    ("beat", "the smallest change inside a scene: one person acts and another reacts."),
    ("turn", "the moment a scene changes for good; its shot is the turn shot."),
    ("screen time", "how long a shot stays on the screen, in seconds."),
    ("close-up, medium, wide", "how much of a person the frame shows, from the face alone to the whole room."),
    ("insert", "a close shot of a thing or a hand, cut into the scene."),
    ("frame-left and frame-right", "the left and right of the picture as you watch it."),
    ("own left and own right", "a person's own left and right hands, whichever side of the picture they are on."),
    ("saved choice", "a strong picture kept for a few moments only, so it still means something when it comes."),
    ("look", "the light, colour and texture of a place at a time."),
    ("state", "how a person or thing looks at a point in the story: clothes, wounds, condition."),
    ("grey preview", "a grey 3D picture that fixes where the camera and the people are."),
    ("addition", "something the story does not say, added to make a shot work; you may keep or cut it."),
]


def full_shot_rows(view, shot, scene_identifier):
    """[(label, value)] of one shot for its folded page in the book: every written field in plain words."""
    names = view.names
    rows = []

    def add(label, value):
        if value is not None and str(value).strip() and not is_empty(value):
            rows.append((label, str(value).strip()))

    add("What it is for", names.text(shot.get("purpose"), scene_identifier))
    add("Why", names.text(shot.get("why"), scene_identifier))
    add("Because of", names.because_words(shot.get("because"), scene_identifier))
    add("Beats", names.list_words(shot.get("beats"), scene_identifier))
    add("Story lines", line_numbers_words(shot.get("lines")) or names.text(shot.get("lines"), scene_identifier))
    camera = []
    if shot.get("setup") and not is_empty(shot.get("setup")):
        camera.append(names.name(shot.get("setup"), scene_identifier))
    for name in ("size", "frame", "angle"):
        if shot.get(name) and not is_empty(shot.get(name)):
            camera.append(plain_value(shot.get(name)))
    if shot.get("height") and not is_empty(shot.get("height")):
        height = shot.get("height")
        eye = re.match(r"^(eye|seated|kneeling):(.+)$", height)
        posture = {"eye": "", "seated": "seated ", "kneeling": "kneeling "}
        camera.append(f"at {names.name(eye.group(2).strip(), short=True)}'s {posture[eye.group(1)]}eye height" if eye
                      else f"{number_text(height)} metres high" if re.fullmatch(r"[\d.]+", height) else names.text(height))
    if shot.get("lens_mm") and not is_empty(shot.get("lens_mm")):
        camera.append(f"{number_text(shot.get('lens_mm'))} millimetre lens")
    if shot.get("move") and not is_empty(shot.get("move")):
        camera.append(plain_value(shot.get("move")))
    add("Camera", ", ".join(camera))
    focus = []
    if shot.get("focus") and not is_empty(shot.get("focus")):
        focus.append(f"{plain_value(shot.get('focus'))} focus")
    if shot.get("focus_on") and not is_empty(shot.get("focus_on")):
        focus.append(f"sharp on {names.name(shot.get('focus_on'), scene_identifier, short=True)}")
    add("Focus", ", ".join(focus))
    add("Why the camera moves", names.text(shot.get("move_reason"), scene_identifier))
    for item in view.items(shot, "subject"):
        parts = [names.name(item.first, scene_identifier, short=True)]
        for key in ("at", "faces", "eyeline", "does", "still", "travel"):
            value = item.get(key)
            if value and not is_empty(value):
                if key == "faces" and normalise_word(value) == "camera":
                    value = "the camera"
                elif key in ("at", "faces", "travel"):
                    value = names.name(value, scene_identifier, short=True) if ID_IN_TEXT.fullmatch(value) else plain_value(value)
                elif key == "eyeline":
                    value = names.name(value, scene_identifier, short=True) if ID_IN_TEXT.fullmatch(value) else plain_value(value)
                    first_word = (re.findall(r"[a-z]+", value.lower()) or [""])[0]
                    if first_word in EYELINE_DIRECTION_WORDS:
                        parts.append(f"eyes {value}")  # "eyes down into the dark", not "eyes on down ..."
                        continue
                elif key == "still":
                    value = plain_words_list(value)
                else:
                    value = names.text(value, scene_identifier)
                if key == "does":
                    parts.append(value)  # a verb phrase of its own: "settles behind the wheel" (C18)
                else:
                    parts.append(f"{KEY_WORDS.get(key, key)} {value}")
        if item.get("recorded") and not is_empty(item.get("recorded")):
            parts.append(f"as recorded in {names.text(item.get('recorded'), scene_identifier)}")
        add("In the frame", "; ".join(parts))
    for item in view.items(shot, "thing"):
        text = names.name(item.first, scene_identifier, short=True)
        if item.get("recorded") and not is_empty(item.get("recorded")):
            text += f", as recorded in {names.text(item.get('recorded'), scene_identifier)}"
        if item.get("emphasis"):
            emphasis = str(item.get("emphasis")).strip()
            text += f", {EMPHASIS_WORDS.get(emphasis, 'emphasis ' + emphasis)}"
        if item.get("at"):
            text += f", {names.text(item.get('at'), scene_identifier)}"
        add("Thing", text)
    add("Text in the picture", names.list_words(shot.get("text"), scene_identifier, short=True))
    add("Must show", names.list_words(shot.get("must_show"), scene_identifier, short=True))
    add("Must not show", names.list_words(shot.get("must_not_show"), scene_identifier, short=True))
    for item in view.items(shot, "glass"):
        add("Glass", f"{item.first}" + (f", {plain_value(item.get('state'))}" if item.get("state") else "")
            + (f", {GLASS_CAMERA_WORDS.get(normalise_word(item.get('camera')), 'seen ' + plain_value(item.get('camera')))}"
               if item.get("camera") else ""))
    light = shot.get("light")
    add("Light", plain_value(light) if light and re.fullmatch(r"[a-z_]+", light) else names.text(light, scene_identifier))
    for item in view.items(shot, "light_cue"):
        add("Light change", names.text(item.first, scene_identifier)
            + (f", at {seconds_words(item.get('when'))}" if item.get("when") else ""))
    for item in view.items(shot, "hear"):
        speech = names.name(item.first, scene_identifier)
        where = plain_value(item.get("speaker")) if item.get("speaker") else ""
        add("We hear", speech + (f" ({where})" if where else ""))
    for item in view.items(shot, "effect"):
        loudness = str(item.get("sound_emphasis") or "").strip()
        add("Sound", names.text(item.first, scene_identifier)
            + (f", {SOUND_EMPHASIS_WORDS.get(loudness, 'sound emphasis ' + loudness)}" if loudness else ""))
    room = shot.get("room_sound")
    add("Room sound", plain_value(room) if room and re.fullmatch(r"[a-z_]+", room) else names.text(room, scene_identifier))
    if shot.get("silence") and normalise_word(shot.get("silence")) != "none":
        add("Silence", plain_value(shot.get("silence")))
    if shot.get("music") and not is_empty(shot.get("music")):
        add("Music", names.text(shot.get("music"), scene_identifier))
    if shot.get("screen_time"):
        text = seconds_words(shot.get("screen_time"))
        try:
            floor = time_floor(view.breakdown, shot)
            if floor.floor and floor.complete:
                text += f" (it cannot be shorter than {seconds_words(round(floor.floor + 0.049, 1))})"
        except Exception:  # the floor is a courtesy on the page; the checker reports floors properly
            pass
        add("Screen time", text)
    for item in view.items(shot, "moment"):
        span = (item.first or "").replace("-", " to ")
        add("Moment", f"{span} seconds: {names.text(item.get('shows'), scene_identifier)}")
    add("Last picture", names.text(shot.get("end"), scene_identifier))
    if shot.get("cut_out_on") and not is_empty(shot.get("cut_out_on")):
        add("Cut out on", plain_value(shot.get("cut_out_on")))
    making = []
    if shot.get("storyboard"):
        making.append(f"storyboard: {plain_value(shot.get('storyboard'))}")
    if shot.get("previs_level") and not is_empty(shot.get("previs_level")):
        level = str(shot.get("previs_level")).strip()
        making.append(PREVIS_LEVEL_WORDS.get(level, f"grey preview level {level}"))
    if shot.get("route") and not is_empty(shot.get("route")):
        making.append(ROUTE_WORDS.get(normalise_word(shot.get("route")), f"made from {plain_value(shot.get('route'))}"))
    if normalise_word(shot.get("held") or "no") == "yes":
        making.append("one unbroken take")
    add("Making it", ", ".join(making))
    add("Additions", names.text(shot.get("additions"), scene_identifier))
    for note in shot.get_all("note"):
        add("Note", names.text(note, scene_identifier))
    return rows


def plain_part_sections(lines):
    """The owned sections of a plain part made by one of the views above, as {heading: [lines]}."""
    part = PlainPart.from_lines(lines)
    return {heading_key(heading): body for heading, body in part.sections}


def section_items(lines):
    """Bullet and numbered lines of a section as items, other lines as paragraphs."""
    paragraphs, items = [], []
    for line in lines:
        text = line.strip()
        if not text:
            continue
        bullet = re.match(r"^(?:- |\d+\. )(.*)$", text)
        if bullet:
            items.append(bullet.group(1))
        else:
            paragraphs.append(text)
    return paragraphs, items


def add_section_to_book(book, lines, heading_text):
    paragraphs, items = section_items(lines)
    if not paragraphs and not items:
        return
    book.label(heading_text)
    for paragraph in paragraphs:
        book.paragraph(paragraph)
    book.bullets(items)


def example_shot(view):
    """The shot 'How to read this' explains: the first main-turn shot, else the first turn shot, else the first shot."""
    shots = view.film_shots()
    for shot in shots:
        if view.is_turn_shot(shot) and turn_words(view, shot.identifier) == "the turn":
            return shot
    for shot in shots:
        if view.is_turn_shot(shot):
            return shot
    return shots[0] if shots else None


def how_to_read_lines(view):
    names = view.names
    lines = []
    shot = example_shot(view)
    if shot is not None:
        scene = scene_of(shot.identifier)
        item = view.list_item(shot.identifier)
        shows = names.text(item.get("shows"), scene) if item is not None and item.get("shows") else \
            names.text(shot.get("purpose"), scene)
        size = plain_value(shot.get("size")) if shot.get("size") else "shot"
        what = f"Take {names.name(shot.identifier, scene)} of {names.name(scene)}"
        if view.is_turn_shot(shot):
            what += f", {turn_words(view, shot.identifier)} of the scene"
        what += f": a {size} held for {seconds_words(shot.get('screen_time'))}." if shot.get("screen_time") \
            else f": a {size}."
        lines.append(what)
        if shows:
            lines.append(f"Its line in the shot list says what we see: {end_sentence(shows)}")
        if shot.get("why"):
            lines.append(f"Its reason is written next to it: {end_sentence(names.text(shot.get('why'), scene))}")
    else:
        scene_ids = view.film_scene_ids()
        if scene_ids:
            event = (view.record(scene_ids[0], "SCENE") or Record("SCENE")).get("event")
            if event:
                lines.append(f"Take {names.name(scene_ids[0])}: {end_sentence(names.text(event, scene_ids[0]))}")
    lines += [
        "Each scene starts with At a glance: what happens, how many shots, how long it runs and where it turns.",
        "Then come its shots, one line each: the shot's number, how close the camera is, how many seconds it runs "
        "and what we see. Open a shot to read all of it: what it is for, why, where the camera stands, who is in "
        "the frame, what we hear.",
        "Shots are numbered in tens so that a shot added later fits between them (shot 155).",
        "Words in double quotes are your story's own words.",
    ]
    return lines


def scene_join_lines(view, scene_identifier):
    """One line per CUT record of a scene (a join that is not a plain cut): 'After shot 010: a jump cut, why ...'
    (C18). Every other join is a plain cut."""
    names = view.names
    lines = []
    for cut in view.records("CUT"):
        if scene_of(cut.identifier) != scene_identifier:
            continue
        number = re.search(r"-C(\d+)$", cut.identifier or "")
        kind = normalise_word(cut.get("type") or "")
        what = "the shot carries straight on" if kind == "continue" else f"a {plain_value(kind)}"
        text = f"After shot {int(number.group(1)):03d}: {what}" if number else f"{cut.identifier}: {what}"
        if cut.get("to") and not is_empty(cut.get("to")):
            text += f", into {names.name(cut.get('to'), scene_identifier, short=True)}"
        if cut.get("split_s") and not is_empty(cut.get("split_s")):
            text += f", the sound leads by {seconds_words(cut.get('split_s'))}"
        if cut.get("black_frames") and not is_empty(cut.get("black_frames")):
            text += f", {cut.get('black_frames')} frames of black"
        if cut.get("sound_across") and not is_empty(cut.get("sound_across")):
            text += f"; heard across it: {names.text(cut.get('sound_across'), scene_identifier)}"
        if cut.get("why") and not is_empty(cut.get("why")):
            text += f". Why: {names.text(cut.get('why'), scene_identifier)}"
        lines.append("- " + text.rstrip(".") + ".")
    if lines:
        lines.append("- Every other join is a plain cut.")
    return lines


def titles_seconds(view):
    """The seconds of titles and credits the estimate from the shots adds (estimate.json), or 0: the book and the
    time and cost page then give one film length, the story's, 'plus titles' when there are any."""
    path = view.folder / "For machines - do not edit" / "estimate.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return float((data.get("estimate") or {}).get("titles_and_credits_s") or 0)
    except (OSError, ValueError, TypeError, AttributeError):
        return 0.0


def write_book(project_folder, schema=None, words=None, constants=None, view=None):
    """Write 15 The breakdown/The breakdown.md and The breakdown.html from the records. Returns their paths."""
    view = view or ProjectView(project_folder, schema, words, constants)
    names = view.names
    book = Book(f"{view.title}: the breakdown")
    book.heading(f"{view.title}: the breakdown", level=1)
    if view.study_only:
        book.paragraph(f"{STUDY_ONLY_MARK}.")
    film_scenes = view.film_scene_ids()
    all_scenes = view.records("SCENE", include_omitted=True)
    if view.scope() is not None and all_scenes:
        book.paragraph(f"Scope: {len(film_scenes)} of {len(all_scenes)} scene{'s' if len(all_scenes) != 1 else ''} "
                       f"({join_words([names.name(scene) for scene in film_scenes])}).")
    length = sum(scene_duration(view.breakdown, scene) or 0 for scene in film_scenes)
    shot_count = sum(len(view.shots(scene)) for scene in film_scenes)
    if shot_count:
        titles = titles_seconds(view)
        with_titles = f" ({duration_words(length + titles)} with titles and credits)" if titles else ""
        book.paragraph(f"{len(film_scenes)} scene{'s' if len(film_scenes) != 1 else ''}, {shot_count} "
                       f"shot{'s' if shot_count != 1 else ''}, {duration_words(length)} of story{with_titles}. "
                       f"Made from the records on {datetime.date.today().isoformat()}; if it looks wrong, the record "
                       "is fixed and the book is made again.")
    sections = [("How to read this", "how-to-read-this"), ("The story plan", "the-story-plan"),
                ("People, places and things", "people-places-and-things"),
                ("The film rules in plain words", "the-film-rules-in-plain-words")]
    sections += [(view.scene_heading_words(scene), slug(view.scene_heading_words(scene))) for scene in film_scenes]
    sections.append(("Word list", "word-list"))
    book.heading("Contents")
    book.contents(sections)

    book.heading("How to read this")
    for line in how_to_read_lines(view):
        book.paragraph(line)

    book.heading("The story plan")
    plan_part = plain_part_sections(story_plan_plain_part(view, []))
    for key, label in (("at a glance", "At a glance"), ("groups of scenes", "Groups of scenes"),
                       ("plants and payoffs", "Plants and payoffs"), ("what the audience knows", "What the audience knows"),
                       ("the chapters one line each", "The chapters"), ("strands", "Strands"),
                       ("events the story needs", "Events the story needs")):
        if key in plan_part:
            add_section_to_book(book, plan_part[key], label)
    scene_part = plain_part_sections(scene_list_plain_part(view, []))
    add_section_to_book(book, scene_part.get("the scenes one line each", []), "The scenes, one line each")

    book.heading("People, places and things")
    for builder, keys in ((characters_plain_part, (("the characters one line each", "The characters"), ("voices", "Voices"))),
                          (places_plain_part, (("places", "Places"), ("things", "Things"),
                                               ("text in pictures", "Text in pictures"), ("motifs", "Motifs"),
                                               ("instory cameras", "In-story cameras"))),
                          (continuity_plain_part, (("states one line each", "How people and things change"),))):
        part = plain_part_sections(builder(view, []))
        for key, label in keys:
            if key in part:
                add_section_to_book(book, part[key], label)
    world_part = plain_part_sections(world_plain_part(view, []))
    add_section_to_book(book, world_part.get("at a glance", []), "Style and world")
    add_section_to_book(book, world_part.get("rules of the story world", []), "Rules of the story world")

    book.heading("The film rules in plain words")
    rules_part = plain_part_sections(film_rules_plain_part(view, []))
    for key, label in (("at a glance", "At a glance"), ("camera rules for each person", "Camera rules for each person"),
                       ("saved choices", "Saved choices"), ("lens exceptions", "Lens exceptions"), ("looks", "Looks"),
                       ("visual plan by group of scenes", "Visual plan by group of scenes"), ("sound", "Sound"),
                       ("the ladder", "The ladder")):
        if key in rules_part:
            add_section_to_book(book, rules_part[key], label)

    for scene in film_scenes:
        heading = view.scene_heading_words(scene)
        book.heading(heading)
        add_section_to_book(book, scene_at_a_glance(view, scene), "At a glance")
        add_section_to_book(book, scene_beat_lines(view, scene), "The beats, one line each")
        add_section_to_book(book, scene_shot_lines(view, scene), "The shots, one line each")
        shots = view.shots(scene)
        if shots:
            book.label("The full shots (open one to read it)")
            for shot in shots:
                book.details(shot_line(view, shot.identifier, scene), full_shot_rows(view, shot, scene))
        add_section_to_book(book, scene_join_lines(view, scene), "How the shots join")
        add_section_to_book(book, scene_why_lines(view, scene), "Why it's shot this way")
        add_section_to_book(book, scene_small_choice_lines(view, scene), "Small choices I made")
        waiting = scene_waiting_lines(view, scene)
        if waiting:
            add_section_to_book(book, waiting, "Waiting for you")

    book.heading("Word list")
    word_lines = [f"{word}: {meaning}" for word, meaning in BOOK_WORDS]
    start_here = view.folder / START_HERE
    if start_here.is_file():
        part = PlainPart.from_lines(plain_part_lines_of(parse_file(start_here, START_HERE, view.schema)))
        known = {word for word, _ in BOOK_WORDS}
        for line in part.section("Word list") or []:
            text = line.strip()
            if text.startswith("- ") and text[2:].split(":")[0] not in known:
                word_lines.append(names.text(text[2:]))
    book.bullets(word_lines)

    folder = view.folder / BOOK_FOLDER
    folder.mkdir(parents=True, exist_ok=True)
    markdown_path = folder / BOOK_MARKDOWN
    html_path = folder / BOOK_HTML
    write_text_exactly(markdown_path, book.to_markdown())
    write_text_exactly(html_path, book.to_html())
    from .project_files import remember_made_from
    remember_made_from(view.folder, f"{BOOK_FOLDER}/{BOOK_HTML}")
    return [markdown_path, html_path]
