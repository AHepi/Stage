"""checks_craft_reasons_words.py: the CRAFT, INFO, REASON and WORDS checks of blueprint section 7.2.

In plain words:
- CRAFT-01 to CRAFT-28 count the craft rules that can be counted: caps on push-ins and extreme close-ups, the
  scene's closest size kept for its turn, exactly one turn shot for each turn beat, at most two beats of intensity 5
  in a part, one camera move per shot, lenses inside the family or a lens exception, quiet plants, the emphasis-3
  budget, no added emphasis where the script already marks a beat, saved choices and banned choices, the editor's
  device budget, joins the story does not write, inventions listed as additions, at most three acting people in a
  shot, no slow playback where the camera system bans it, the sign test for turns, no stacked signals on one beat,
  principals that look alike, melodrama and monologue flags, off-screen speakers, the silent third, display 3,
  held moments filled with small timed actions, no words asking for stillness, and no contact shown with its
  result inside one shot (CRAFT-17 is planned for the second build).
- INFO-01 and INFO-02 check who knows what: nothing gives a fact away before its reveal, and the reveal shot
  matters (turn or must_keep).
- REASON-01 to REASON-08 check that every shot says why it exists: a purpose and a because that names this story;
  a why wherever a value leaves its default; a why that is anchored in this story (a quote from the scene, an ID or
  a named element) and never mood-only or a reason that would fit any film (the word lists of rules/words.json);
  turn shots citing their turn beat; saved choices citing their RC; tool-forced changes keeping their meaning; every
  unsaid thought carried by something seen or heard (REASON-09 is planned for the second build).
- WORDS-01 to WORDS-05 check the words: no emotion adjectives in what bodies do; no retired words; no real people,
  living artists, film titles or brands in anything pasted into prompts; no abbreviations or internal codes in the
  plain part above a file's divider; fixed descriptions within their length and free of expression words.

Every check reads the records (and the derived fields of derive_fields.py where it needs them), never changes them,
and is registered with check_records.register_check (see the note at the top of check_records.py). Numbers come from
rules/constants.json and words from rules/words.json, by name.

Other modules may use the text helpers at the end of this file (retired_words_in_text, abbreviations_in_text,
mood_only_phrases_in_reason, reason_is_anchored) to check text that is not a record file, such as step files,
checkpoint templates and guides.

Standard library only.

After the full run on The Catch (Project notes 31 and 32):
- CRAFT-03 follows the ladder's rung on the main turn, else the camera rule's cap;
- CRAFT-10 and CRAFT-19: a change is not added when a quote of the beat's own light or sound words backs it, or the
  sound plan's rupture points at the beat;
- INFO-01 accepts a shot whose keep_hidden names the fact; retired words are found only in their retired senses;
  REASON-08 reads a thing's 'at' and the shot's end.

After the three-scene test of the fixed kit (Project notes 35 and 36):
- a silence on the beat the scene's own rupture names is planned; an in-story camera's own angle, move or lens spends
  no saved choice.

After the second three-scene test (Project notes 37 and 38):
- a saved choice's "never in scenes 26 and 27" keeps those scenes out, and "scenes 10 and 29" names both.

After the second full run (Project notes 39 and 40):
- CRAFT-14 reads list items in a scene with no shots yet; REASON-03 takes a set-plan mark or object named in plain
  words, never in capitals, and says a line number alone anchors nothing; CRAFT-19 takes any form of stand or move, or
  a MOVE ID, for staging; WORDS-02 leaves "the screen left blank" alone; a plural word matches its singular.
- after its cross-examination: CRAFT-24 warns about silent_third none on a turn with three or more people in its
  shots.

After the H3 handover (Project notes 42 and 43, 10 October 2026); all three are warnings marked J, judgements from
testers' notes that the take log has not yet confirmed:
- CRAFT-26 is turned round: a moment of hold_action_every_s or more needs at least one small timed action every
  hold_action_every_s (its shows split at ";" and "then"; a clause holding a stillness word or a not_an_action word
  of rules/words.json is no action), and a pause held on picture needs the shot's last moments to carry it the same
  way. It never asks for the subject's still sub-part, which is kept only so that older breakdowns load.
- CRAFT-27: a stillness word or phrase (stillness_words) in a moment, a does, a start or an end.
- CRAFT-28: a contact_words cause followed by its effect in one shot (the same moment or the next one); a shot that
  ends on the cause, followed by one that opens on the result, is the fix and is never flagged.
- CRAFT-15 counts a person as acting unless they are in the background: energy: still and no line on screen in
  the shot (or an older breakdown's still: whole_body).
"""

import math
import re
from dataclasses import dataclass

from .check_records import register_check, same_scene, scene_of
from .derive_fields import (SIZE_LADDER, breakdown_for_run, constant, count_words, element_of,
                            last_shot_naming_beat, number_of, script_marked)
from .record_format import (DIVIDER_LINE, TextBlock, normalise_word, parse_line_numbers, parse_story_point,
                            quote_for_message, sort_key_for_identifier, split_item, split_list)

# ---------------------------------------------------------------- words and patterns

QUOTED = re.compile(r'["“]([^"“”]+)["”]')
ID_TOKEN = re.compile(r"(?<![A-Za-z0-9_-])((?:SC\d{2,3}[A-Z]?(?:-[A-Z]+\d+(?:\.\d+)?)?)|"
                      r"(?:[A-Z]{2,6}-[A-Z0-9]+(?:-[A-Z0-9]+)*(?:\.S\d{2})?))(?![A-Za-z0-9_])")
WORD_PIECE = re.compile(r"[A-Za-z][A-Za-z'’-]*")
TITLE_WORD = re.compile(r"^[A-Z][A-Za-z'’-]*[a-z][A-Za-z'’-]*$")
EMPTY_WORDS = ("none", "open", "auto", "", "default")
CAMERA_MOVE_WORDS = ("pan", "tilt", "push_in", "pull_back", "sideways", "rise", "lower", "follow", "lead", "handheld",
                     "crane", "orbit", "zoom", "whip_pan", "dolly_zoom", "drone")
# Camera moves 5.5 allows only when a saved choice covers them (SHOT move and angle).
MOVES_ONLY_WHEN_SAVED = ("orbit", "zoom", "whip_pan", "dolly_zoom", "drone")
ANGLES_ONLY_WHEN_SAVED = ("dutch",)
# Words in a moment that name a camera move ("the camera pans", "we push in"), each read as the move it names. Only
# the camera (or "we", or the lens) as the one who moves counts, so "a frying pan" or "she pulls back" never does.
CAMERA_SUBJECT = r"\b(?:the\s+)?(?:camera|we|lens)\s+(?:slowly\s+|then\s+|now\s+|gently\s+)?"
CAMERA_MOVE_PHRASES = [
    (re.compile(CAMERA_SUBJECT + r"pans?\b", re.I), "pan"),
    (re.compile(CAMERA_SUBJECT + r"tilts?\b", re.I), "tilt"),
    (re.compile(CAMERA_SUBJECT + r"push(?:es)?\s+in\b", re.I), "push_in"),
    (re.compile(CAMERA_SUBJECT + r"(?:pulls?|pull)\s+back\b", re.I), "pull_back"),
    (re.compile(CAMERA_SUBJECT + r"(?:cranes?|booms?)\b", re.I), "crane"),
    (re.compile(CAMERA_SUBJECT + r"(?:follows|follow|tracks|track|trucks|dollies)\b", re.I), "follow"),
    (re.compile(CAMERA_SUBJECT + r"(?:rises|rise|lifts)\b", re.I), "rise"),
    (re.compile(CAMERA_SUBJECT + r"(?:lowers|drops|sinks)\b", re.I), "lower"),
    (re.compile(CAMERA_SUBJECT + r"(?:orbits|circles)\b", re.I), "orbit"),
    (re.compile(CAMERA_SUBJECT + r"zooms?\s+(?:in|out)\b", re.I), "zoom"),
    (re.compile(r"\bwhip[\s-]?pans?\b", re.I), "whip_pan"),
]
SLOW_PLAYBACK = re.compile(r"\b(slow[\s-]?motion|slow[\s-]?mo|half[\s-]speed|over[\s-]?cranked|high\s+frame\s+rate)"
                           r"\b", re.I)
NEGATION_BEFORE = re.compile(r"\b(no|never|not|without|nor|instead\s+of|rather\s+than)\b[^.;]{0,24}$", re.I)
# Devices whose words, quoted from the story, show that the story writes the join (CRAFT-12, CRAFT-13).
DEVICE_WORDS = {
    "cut_to_black": ("cut to black", "black"),
    "fade": ("fade",),
    "dissolve": ("dissolve",),
    "freeze": ("freeze",),
    "smash_cut": ("smash cut",),
}
JOINS_THE_STORY_MUST_WRITE = ("dissolve", "fade", "cut_to_black", "freeze", "smash_cut")
# What a match cut's why must name (CRAFT-13): a shared shape, motion or sound (A4 T5).
SHARED_SHAPE_MOTION_SOUND = re.compile(
    r"\b(shape|shapes|form|outline|silhouette|circle|circles|circular|round|square|line|lines|curve|arc|spiral|"
    r"motion|moving|movement|gesture|swing|swings|fall|falls|falling|spin|spins|spinning|turn|turns|turning|"
    r"rise|rises|sound|sounds|noise|hum|ring|ringing|bang|echo|echoes|rhythm|beat of|shared|matches|matching|"
    r"rhymes?)\b", re.I)
# Departments of SCENE department_idea and the words scene_idea may name them by (CRAFT-19).
DEPARTMENT_WORDS = {
    "camera": ("camera", "lens", "close-up", "close up", "frame", "shot"),
    "light": ("light", "lighting", "lamp", "dark", "darkness"),
    "staging": ("staging", "blocking", "stands", "moves", "position"),
    "sound": ("sound", "silence", "silent", "music", "hum", "room sound"),
    "design": ("design", "set", "dressing", "props", "costume"),
}
# Signals that must not stack on one beat (CRAFT-19; signals_changing_per_beat_max names them).
COLOUR_WORDS = re.compile(r"\b(colou?r|colou?rs|hue|tint|saturat\w*|red|green|blue|amber|orange|yellow|violet|"
                          r"purple|teal)\b", re.I)
# Capitalised words that are not names of real people, works or brands (WORDS-03). Judgement: nationalities,
# languages, compass words, days and months are written with a capital in plain English.
COMMON_CAPITALISED = {
    "english", "british", "american", "scottish", "irish", "welsh", "french", "german", "spanish", "italian",
    "indian", "chinese", "japanese", "african", "european", "asian", "australian", "canadian", "mexican", "russian",
    "arabic", "latin", "dutch", "polish", "greek", "turkish", "portuguese", "brazilian", "korean", "nordic",
    "northern", "southern", "eastern", "western", "north", "south", "east", "west", "monday", "tuesday", "wednesday",
    "thursday", "friday", "saturday", "sunday", "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december", "christmas", "easter", "god", "i", "dr", "mr", "mrs",
    "ms", "the", "a", "an",
}
# Words that may open the object of "to emphasise" without being it ("to emphasise her isolation" has no object
# beyond a feeling word; "to emphasise the distance" has one).
OBJECT_DETERMINERS = {"the", "a", "an", "her", "his", "their", "its", "this", "that", "these", "those", "our", "my",
                      "your", "how", "just", "further", "more", "even"}
BRAND_SYMBOLS = re.compile("[™®©]")
DETERMINERS = re.compile(r"^(the|a|an|her|his|their|its|our|my|your|one|some)\s+", re.I)
POSSESSIVE_START = re.compile(r"^[A-Z][A-Za-z]*(?:'s|’s)\s+")
STOP_WORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "at", "by", "for", "with", "from", "into", "onto", "over",
    "her", "his", "their", "its", "them", "they", "she", "he", "it", "is", "are", "was", "be", "as", "so", "that",
    "this", "then", "back", "up", "down", "out", "off", "before", "after", "between", "while",
}
# Prompt-compiled fields (WORDS-03): what code pastes into picture, video and voice prompts (8.1, words.json's
# banned_prompt_words applies_to, plus the voice description and a shot's visible words).
PROMPT_FIELDS = {
    "STYLE": ("style_words", "texture"),
    "LOOK": ("look_block",),
    "CHARACTER": ("fixed_description", "skin_light"),
    "PROP": ("fixed_description",),
    "STATE": ("state_line",),
    "VOICE": ("voice_description",),
    "LOCATION": ("dressing", "room_sound"),
    "SHOT": ("subject", "moment", "gen_note", "physics_note", "light", "light_cue", "effect", "end", "start"),
}
# Records whose values the checker writes (a FINDING from source checker) or that only people read: WORDS-02 leaves
# their values alone so that a quoted slip is not reported twice.
WORDS_02_SKIPPED_TYPES = ("FINDING", "REVIEW")


# ---------------------------------------------------------------- small helpers

def breakdown_of(run):
    return breakdown_for_run(run)


def constant_of(run, name, default=None):
    return constant(run.constants, name, default)


def word_of(value):
    return normalise_word(value or "")


def is_empty(value):
    """True for a missing value and for none, open, auto and default (G7), in any case."""
    return value is None or value.strip().lower() in EMPTY_WORDS


def by_identifier(records):
    return sorted(records, key=lambda record: sort_key_for_identifier(record.identifier or ""))


def definition_of(run, type_name, field_name):
    return run.schema.field(type_name, field_name) or {}


def items(run, record, field_name):
    """Every item of a repeatable field (or one sub-parts value) as record_format.Item, leaving out none; worked out
    once per record and field in a run."""
    if record is None:
        return []
    key = ("craft_items", id(record), field_name)
    cached = run.cache.get(key)
    if cached is not None and cached[0] is record:
        return cached[1]
    definition = definition_of(run, record.type_name, field_name)
    found = []
    for value in record.get_all(field_name):
        if normalise_word(value) in ("none", ""):
            continue
        found.append(split_item(value, definition))
    run.cache[key] = (record, found)
    return found


def named_parts(value):
    """{key: value} of every named piece of an item, the first piece too ("from: SC13 | family: 35, 50, 85"), for
    fields written with named sub-parts only (WP1: first_part null)."""
    found = {}
    for piece in split_item(value or "", {"first_part": None}).parts:
        found.setdefault(piece[0], piece[1].strip())
    return found


def id_list(record, field_name):
    value = record.get(field_name) if record is not None else None
    if not value or is_empty(value):
        return []
    return [piece.strip() for piece in split_list(value) if not is_empty(piece)]


def field_line_of(run, record, field_name, containing=None):
    """(file name, line number) of a record's field line (the first one, or the one whose value holds a text)."""
    if record is None:
        return None, None
    for record_file, _, line in run.field_lines(record.key, field_name):
        if containing is None or containing in (line.value or ""):
            return record_file.name, line.line_number
    for record_file, _, line in run.field_lines(record.key, field_name):
        return record_file.name, line.line_number
    return None, None


def problem_at(run, level, check_id, record, field_name, what, fix, containing=None):
    """A problem line placed at the field line it is about (or at the record's heading)."""
    file_name, line_number = field_line_of(run, record, field_name.split(" ")[0] if field_name else None,
                                          containing) if field_name else (None, None)
    return run.problem(level, check_id, record, field_name, what, fix, line_number=line_number, file_name=file_name)


def records_of(run, type_name):
    """The merged records of a type (omitted ones left out), in ID order; worked out once per run."""
    key = ("craft_records", type_name)
    if key not in run.cache:
        run.cache[key] = by_identifier(run.records(type_name))
    return run.cache[key]


def scene_key(scene):
    """SC10 and SC010 name the same scene (the width is ID-09's business)."""
    return re.sub(r"^SC0*", "SC", scene or "")


def scene_identifiers(run):
    """Every scene with records here, in story order."""
    key = "craft_scene_identifiers"
    if key not in run.cache:
        found = set(run.scene_ids())
        for type_name in ("SHOT", "BEAT", "SHOTLIST", "PART"):
            for record in records_of(run, type_name):
                scene = scene_of(record.identifier)
                if scene:
                    found.add(scene)
        run.cache[key] = sorted(found, key=sort_key_for_identifier)
    return run.cache[key]


def of_scene(run, type_name, scene):
    """The records of one type that belong to a scene, in ID order."""
    key = ("craft_of_scene", type_name)
    groups = run.cache.get(key)
    if groups is None:
        groups = {}
        for record in records_of(run, type_name):
            owner = scene_of(record.identifier)
            if owner:
                groups.setdefault(scene_key(owner), []).append(record)
        run.cache[key] = groups
    return groups.get(scene_key(scene), [])


def beats_of(run, scene):
    return of_scene(run, "BEAT", scene)


def beat_positions(run, scene):
    return {beat.identifier: index for index, beat in enumerate(beats_of(run, scene))}


def turn_of(beat):
    return word_of(beat.get("turn") or "none") if beat is not None else "none"


def is_turn_beat(beat):
    return turn_of(beat) not in ("none", "")


def main_turn_of(run, scene):
    for beat in beats_of(run, scene):
        if turn_of(beat) == "main_turn":
            return beat
    return None


def size_rank(size):
    size = word_of(size)
    return SIZE_LADDER.index(size) if size in SIZE_LADDER else None


def size_words(size):
    return (size or "").replace("_", " ")


def scene_record(run, scene):
    record = run.record(scene)
    return record if record is not None and record.type_name == "SCENE" else None


def whole_number(value, default=None):
    number = number_of(value, None)
    return default if number is None else number


def names_list(identifiers):
    return ", ".join(identifiers)


# ---------------------------------------------------------------- one view of a shot: a SHOT record or a list item

@dataclass
class ShotView:
    """A shot as the checks see it: its SHOT record when written, else its shot-list item (step 7, Quick depth, and
    the shots of later batches during step 8)."""
    identifier: str
    scene: str
    beats: list
    role: str
    size: str
    frame: str
    kind: str
    subjects: list
    record: object = None
    list_record: object = None

    @property
    def written(self):
        return self.record is not None

    @property
    def is_card(self):
        return self.kind in ("card", "black") or self.frame == "empty" and not self.subjects and self.size != "insert"

    @property
    def is_insert(self):
        return self.size == "insert" or self.kind == "insert"

    @property
    def is_live(self):
        return not self.is_insert and self.kind not in ("card", "black")

    @property
    def problem_record(self):
        return self.record if self.record is not None else self.list_record


def list_items_of(run, scene):
    """[(shot ID, Item, SHOTLIST record)] of a scene's shot list."""
    found = []
    definition = definition_of(run, "SHOTLIST", "item")
    for record in of_scene(run, "SHOTLIST", scene):
        for value in record.get_all("item"):
            item = split_item(value, definition)
            if item.first and not is_empty(item.first):
                found.append((item.first.strip(), item, record))
    return found


def subject_elements_of_shot(run, shot):
    return [element_of(item.first.strip()) for item in items(run, shot, "subject") if item.first]


def shot_views(run, scene):
    """Every shot of a scene in shot order: the SHOT record when it exists, else the list item."""
    key = ("craft_shot_views", scene)
    if key in run.cache:
        return run.cache[key]
    views = {}
    for shot_identifier, item, list_record in list_items_of(run, scene):
        subjects = [] if is_empty(item.get("subject")) else [element_of(piece) for piece in
                                                              split_list(item.get("subject") or "")]
        views[shot_identifier] = ShotView(
            identifier=shot_identifier, scene=scene,
            beats=[piece for piece in split_list(item.get("beats") or "") if not is_empty(piece)],
            role=word_of(item.get("role") or "normal"), size=word_of(item.get("size")),
            frame=word_of(item.get("frame")), kind="card" if word_of(item.get("frame")) == "empty" and
            not subjects else "", subjects=subjects, list_record=list_record)
    for shot in of_scene(run, "SHOT", scene):
        listed = views.get(shot.identifier)
        views[shot.identifier] = ShotView(
            identifier=shot.identifier, scene=scene, beats=id_list(shot, "beats"),
            role=word_of(shot.get("role") or "normal"), size=word_of(shot.get("size")),
            frame=word_of(shot.get("frame")), kind=word_of(shot.get("kind")),
            subjects=subject_elements_of_shot(run, shot), record=shot,
            list_record=listed.list_record if listed else None)
    ordered = sorted(views.values(), key=lambda view: sort_key_for_identifier(view.identifier))
    run.cache[key] = ordered
    return ordered


def shots_of(run, scene):
    """The written SHOT records of a scene, in shot order."""
    return of_scene(run, "SHOT", scene)


def shots_on_beat(run, scene, beat_identifier, written_only=False):
    return [view for view in shot_views(run, scene) if beat_identifier in view.beats
            and (view.written or not written_only)]


def last_beat_position(view, positions):
    known = [positions[beat] for beat in view.beats if beat in positions]
    return max(known) if known else None


# ---------------------------------------------------------------- what is in a shot

def thing_items(run, shot):
    return [item for item in items(run, shot, "thing") if item.first]


def prop_motif(run, element):
    record = run.record(element)
    if record is not None and record.type_name == "PROP":
        motif = record.get("motif")
        if motif and not is_empty(motif):
            return motif.strip()
    return None


def elements_in_frame(run, shot, include_must_show=True):
    """{element: where it was named} for everything a shot puts in frame (subjects, things, must_show)."""
    found = {}
    for item in items(run, shot, "subject"):
        if item.first:
            found.setdefault(element_of(item.first.strip()), "subject")
    for item in thing_items(run, shot):
        found.setdefault(element_of(item.first.strip()), "thing")
    if include_must_show:
        for reference in id_list(shot, "must_show"):
            found.setdefault(element_of(reference), "must_show")
    for reference in id_list(shot, "text"):
        found.setdefault(element_of(reference), "text")
    return found


def element_matches(run, wanted, present):
    """True when an element (or its motif) is among the present elements (a PROP whose motif is wanted counts)."""
    wanted = element_of(wanted)
    if wanted in present:
        return True
    for element in present:
        if prop_motif(run, element) == wanted or prop_motif(run, wanted) == element:
            return True
    return False


def thing_emphasis(item):
    return whole_number(item.get("emphasis"), None)


def motif_of_thing(run, reference):
    element = element_of(reference.strip())
    if element.startswith("MO-"):
        return element
    return prop_motif(run, element)


# ---------------------------------------------------------------- names, IDs and quotes (REASON-03, REASON-04)

def identifier_exists(run, identifier):
    """True when an ID names a record, an item a field declares (a scene value, a shot-list item) or a speech."""
    if run.record(identifier) is not None:
        return True
    key = "craft_declared_identifiers"
    if key not in run.cache:
        declared = set()
        for type_name, field_name in (("SCENE", "value"), ("SHOTLIST", "item")):
            definition = definition_of(run, type_name, field_name)
            for record in run.records(type_name, include_omitted=True):
                for value in record.get_all(field_name):
                    first = split_item(value, definition).first
                    if first:
                        declared.add(first.strip())
        run.cache[key] = declared
    if identifier in run.cache[key] or identifier in run.speeches:
        return True
    clip = re.match(r"^(SC\d{2,3}[A-Z]?-SH\d{3})\.\d$", identifier)
    return bool(clip and run.record(clip.group(1)) is not None)


def identifier_counts(run, identifier):
    """An ID counts as an anchor when it exists, or when it points into a scene this check cannot see."""
    if identifier_exists(run, identifier):
        return True
    scene = scene_of(identifier)
    return bool(scene and run.scene_left_out(scene))


def plain_name(text):
    """A name as it can be looked for in prose: no leading article or possessive, lowercase."""
    text = (text or "").strip().strip(".")
    text = POSSESSIVE_START.sub("", text)
    previous = None
    while previous != text:
        previous = text
        text = DETERMINERS.sub("", text)
    return text.strip().lower()


def element_name_list(run, element):
    """Every name an element may be called by in prose: its names (aliases), its title and, for a place, the names
    of its set-plan objects."""
    record = run.record(element)
    if record is None:
        return []
    names = []
    if record.get("names"):
        names += split_list(record.get("names"))
    if record.title:
        names.append(record.title)
    if record.type_name == "LOCATION":
        for item in items(run, record, "object"):
            if item.first:
                names.append(item.first.replace("_", " "))
    found = []
    for name in names:
        cleaned = plain_name(name)
        if len(cleaned) >= 3 and cleaned not in found:
            found.append(cleaned)
    return found


def scene_elements(run, scene):
    """The elements a scene's records name (people, things, places, motifs, texts), with its place."""
    key = ("craft_scene_elements", scene)
    if key in run.cache:
        return run.cache[key]
    found = set()
    scene_types = ("SCENE", "PART", "BEAT", "SHOTLIST", "SHOT", "MOVE", "SETUP", "CUT", "SPEECH")
    for type_name in scene_types:
        records = [scene_record(run, scene)] if type_name == "SCENE" else of_scene(run, type_name, scene)
        for record in records:
            if record is None:
                continue
            for line in record.fields:
                for match in ID_TOKEN.finditer(line.value or ""):
                    element = element_of(match.group(1))
                    if run.record(element) is not None and run.record(element).type_name in (
                            "CHARACTER", "PROP", "LOCATION", "MOTIF", "TEXT", "CAMERA"):
                        found.add(element)
    record = scene_record(run, scene)
    if record is not None:
        for piece in id_list(record, "characters"):
            found.add(element_of(piece))
    run.cache[key] = found
    return found


def names_of_elements(run, elements):
    names = {}
    for element in elements:
        for name in element_name_list(run, element):
            names.setdefault(name, element)
    return names


def scene_element_names(run, scene):
    key = ("craft_scene_element_names", scene)
    if key not in run.cache:
        run.cache[key] = names_of_elements(run, scene_elements(run, scene))
    return run.cache[key]


def all_element_names(run):
    key = "craft_all_element_names"
    if key not in run.cache:
        elements = []
        for type_name in ("CHARACTER", "PROP", "LOCATION", "MOTIF", "TEXT", "CAMERA"):
            elements += [record.identifier for record in records_of(run, type_name) if record.identifier]
        run.cache[key] = names_of_elements(run, elements)
    return run.cache[key]


def scene_plan_names(run, scene):
    """The marks and objects of the scene's set plan in plain words ("fire door" for FIRE_DOOR): a why that names one
    in plain words is anchored in the scene; the capitals themselves never count (the second full run, Project
    notes 39)."""
    key = ("craft_scene_plan_names", scene)
    if key not in run.cache:
        from .derive_fields import scene_location, set_plan
        breakdown = breakdown_of(run)
        location = scene_location(breakdown, scene)
        plan = set_plan(breakdown, location) if location else None
        found = set()
        for name in (list(plan.marks) + list(plan.objects)) if plan is not None else []:
            words = " ".join(name.lower().replace("_", " ").split())
            if len(words) >= 3:
                found.add(words)
        run.cache[key] = found
    return run.cache[key]


def plan_name_in(text, names):
    """The first set-plan name the text holds in plain words ("the fridge", "the fire door"), never in capitals
    ("FRIDGE", "FIRE_DOOR"), or None."""
    for name in sorted(names, key=len, reverse=True):
        for match in re.finditer(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?:s|es)?(?![A-Za-z0-9_])", text or "",
                                 re.IGNORECASE):
            if match.group(0) != match.group(0).upper():
                return name
    return None


def named_element_in(text, names):
    """The first element name the text holds (whole words, any case, a plain plural allowed), or None."""
    lowered = (text or "").lower()
    for name in sorted(names, key=len, reverse=True):
        if re.search(r"(?<![a-z0-9])" + re.escape(name) + r"(?:s|es)?(?![a-z0-9])", lowered):
            return name
    return None


def quote_found(run, quote, scope):
    """True when a quote is found in the story lines of a scope (first, last); None when that cannot be known."""
    if run.story is None or scope is None:
        return None
    first, last = scope
    if not run.story.holds(first, last):
        return None
    if run.story.find(quote, first, last):
        return True
    from .read_story import normalise_quote
    wanted = normalise_quote(quote)
    joined = " ".join(normalise_quote(run.story.numbered.line(number)) for number in range(first, last + 1))
    return bool(wanted) and wanted in joined


@dataclass
class Anchor:
    """How a reason names this story: a quote found in the scene's lines, an ID, or a named element."""
    anchored: bool
    how: str = ""
    unknown_quotes: bool = False


def reason_anchor(run, text, scene=None):
    """Whether a why (or an idea) is anchored in this story (REASON-03): a quote from the scene's lines (the whole
    story for whole-film records), an ID that exists, or the name of an element of the scene (of the film for
    whole-film records). A quote that cannot be looked up (no story, or a scene outside the excerpt) counts."""
    text = text or ""
    scope = run.scene_range(scene) if scene else (
        (run.story.first, run.story.last) if run.story is not None else None)
    unknown = False
    for match in QUOTED.finditer(text):
        found = quote_found(run, match.group(1), scope)
        if found:
            return Anchor(True, f'the quote "{match.group(1)}"')
        if found is None:
            unknown = True
    for match in ID_TOKEN.finditer(text):
        if identifier_counts(run, match.group(1)):
            return Anchor(True, f"the ID {match.group(1)}")
    names = scene_element_names(run, scene) if scene else all_element_names(run)
    name = named_element_in(QUOTED.sub(" ", text), names)
    if name:
        return Anchor(True, f'the name "{name}"')
    name = plan_name_in(QUOTED.sub(" ", text), scene_plan_names(run, scene)) if scene else None
    if name:
        return Anchor(True, f'the set plan\'s "{name}"')
    if unknown:
        return Anchor(True, "a quote that could not be looked up here", unknown_quotes=True)
    return Anchor(False)


def mood_phrases_in(words, text):
    """The mood-only phrases of words.json a reason holds (REASON-04): every listed phrase, and 'to emphasise' only
    with no object after it (at the end, or followed only by a feeling word)."""
    rule = (words or {}).get("mood_only_phrases", {})
    conditional = {entry.get("phrase", "").lower() for entry in rule.get("conditional", [])}
    feeling_words = [word.lower() for word in rule.get("mood_words_flag_if_alone", [])]
    lowered = QUOTED.sub(" ", text or "").lower()
    found = []
    for phrase in rule.get("phrases", []):
        lowered_phrase = phrase.lower()
        for match in re.finditer(r"(?<![a-z])" + re.escape(lowered_phrase) + r"(?![a-z])", lowered):
            if lowered_phrase in conditional:
                clause = re.split(r"[.;:,!?()]", lowered[match.end():], maxsplit=1)[0]
                after = [word for word in re.findall(r"[a-z']+", clause) if word not in OBJECT_DETERMINERS]
                if after and after[0] not in feeling_words:
                    continue
            if phrase not in found:
                found.append(phrase)
            break
    return found


def mood_words_in(words, text):
    rule = (words or {}).get("mood_only_phrases", {})
    lowered = QUOTED.sub(" ", text or "").lower()
    return [word for word in rule.get("mood_words_flag_if_alone", [])
            if re.search(r"(?<![a-z])" + re.escape(word.lower()) + r"(?![a-z])", lowered)]


# ---------------------------------------------------------------- CRAFT

def push_in_shots(run, scene):
    found = [shot for shot in shots_of(run, scene) if word_of(shot.get("move")) == "push_in"]
    positions = beat_positions(run, scene)
    for beat in beats_of(run, scene):
        for item in items(run, beat, "pause_after"):
            if word_of(item.get("picture")) != "push_in":
                continue
            covering = [view for view in shot_views(run, scene) if view.written and view.beats
                        and last_beat_position(view, positions) == positions.get(beat.identifier)]
            if not any(word_of(view.record.get("move")) == "push_in" for view in covering):
                found.append(beat)
    return found


@register_check("CRAFT-01", level="W", build=1, title="More than one push-in in a scene (a cap, not a quota)",
                plain="pushes in more than once in one scene; the push-in is kept for the main turn")
def check_craft_01(run):
    problems = []
    most = int(constant_of(run, "push_in_per_scene_max", 1))
    for scene in scene_identifiers(run):
        found = push_in_shots(run, scene)
        if len(found) <= most:
            continue
        main = main_turn_of(run, scene)
        for extra in found[most:]:
            field_name = "move" if extra.type_name == "SHOT" else "pause_after"
            problems.append(problem_at(
                run, "W", "CRAFT-01", extra, field_name,
                f"push_in is push-in {found.index(extra) + 1} of {len(found)} in {scene} "
                f"({names_list([record.identifier for record in found])}); the cap is {most} per scene",
                "Fix: keep one push-in, on the main turn" + (f" ({main.identifier})" if main else "") +
                ", and make the others static (B1 P5)."))
    return problems


@register_check("CRAFT-02", level="W", build=1,
                title="More than one extreme close-up in a scene, or one not on the main turn (a cap, not a quota)",
                plain="uses more than one extreme close-up in a scene, or one away from the main turn")
def check_craft_02(run):
    problems = []
    most = int(constant_of(run, "extreme_close_up_per_scene_max", 1))
    for scene in scene_identifiers(run):
        main = main_turn_of(run, scene)
        closest = [view for view in shot_views(run, scene)
                   if view.size == "extreme_close_up" and view.kind != "insert"]
        for index, view in enumerate(closest):
            record = view.problem_record
            if index >= most:
                problems.append(problem_at(
                    run, "W", "CRAFT-02", record, "size",
                    f"extreme_close_up is extreme close-up {index + 1} of {len(closest)} in {scene} "
                    f"({names_list([other.identifier for other in closest])}); the cap is {most} per scene",
                    "Fix: keep one extreme close-up, on the main turn, and open the others to close_up or wider "
                    "(B1 P5).", containing=None))
            elif main is not None and main.identifier not in view.beats:
                problems.append(problem_at(
                    run, "W", "CRAFT-02", record, "size",
                    f"extreme_close_up is not on the main turn {main.identifier} (beats {names_list(view.beats)})",
                    f"Fix: spend the extreme close-up on {main.identifier}, or open this shot to close_up (B1 P5)."))
    return problems


@register_check("CRAFT-03", level="W", build=1, title="The main turn's size against the film's ladder, or the scene's "
                                                   "tightest size spent before the turn",
                plain="does not give the main turn the size the film's plan sets for it, or spends a closer shot "
                      "before the turn")
def check_craft_03(run):
    """C24, and the full run (Project notes 31, problem 8): the film's ladder decides the turn shot's size.

    Where a LADDER rung names a beat of this scene, a shot of that beat (its turn shot first) is at the rung's size,
    and the main turn, when it is the rung's beat, is compared with the rung, never with the camera rule's closest
    size. Earlier shots are then held to the rung as to a cap (they may equal it, never be tighter), unless the
    rung plays the turn wide on purpose (wider than medium), when the turn is marked by opening out and earlier
    closer shots are the build to it. A rung on an insert leaves people's sizes alone.

    Without a rung, as before: the main turn is at least as tight as every earlier shot; where a camera rule caps the
    turn's subject (limit_before before the scene where its closest size is spent, the closest size from then on,
    stepped down past a size a saved choice keeps out of this scene), the turn should be at that cap, and earlier
    shots may equal it. A scene whose every shot is in-story footage from a fixed camera is skipped."""
    problems = []
    for scene in scene_identifiers(run):
        main = main_turn_of(run, scene)
        rung_beat, rung_size, _ = ladder_rung_of(run, scene)
        positions = beat_positions(run, scene)
        written = [view for view in shot_views(run, scene) if view.record is not None]
        if written and all(view.kind == "screen" for view in written):
            run.skip("CRAFT-03", f"{scene}: every shot is in-story footage from a fixed camera, so size cannot mark "
                                 "the turn")
            continue
        if rung_size and rung_beat:
            problems.extend(rung_size_problems(run, scene, rung_beat, rung_size))
        if main is None:
            continue
        turn_position = positions.get(main.identifier)
        views = [view for view in shot_views(run, scene) if view.is_live and size_rank(view.size) is not None]
        if not views or turn_position is None:
            continue
        ladder_decides = bool(rung_size) and rung_beat == main.identifier
        if ladder_decides and (size_rank(rung_size) is None or size_rank(rung_size) < SIZE_LADDER.index("medium")):
            continue  # an insert turn, or a deliberate wide: the ladder chose it, and earlier sizes are the build
        turn_views = [view for view in views if view.role == "turn" and main.identifier in view.beats]
        if not turn_views:
            if rung_size:
                continue  # the turn is carried by an insert or a card; the ladder set this scene's size elsewhere
            tightest = max(size_rank(view.size) for view in views)
            for view in views:
                last = last_beat_position(view, positions)
                if size_rank(view.size) == tightest and last is not None and last < turn_position:
                    problems.append(problem_at(
                        run, "W", "CRAFT-03", view.problem_record, "size",
                        f"{view.size} is the scene's tightest size and comes before the main turn {main.identifier} "
                        f"(beats {names_list(view.beats)})",
                        f"Fix: open this shot to a wider size, so that the scene's closest frame is spent on "
                        f"{main.identifier} (A2 R4)."))
            continue
        turn_view = max(turn_views, key=lambda view: size_rank(view.size))
        turn_rank = size_rank(turn_view.size)
        if ladder_decides:
            cap, cap_rule = rung_size, None
        else:  # no rung, or a rung on another beat of the scene: the camera rule's cap still holds for the turn
            cap, cap_rule = size_cap_for(run, scene, turn_view)
        for view in views:
            if view in turn_views:
                continue
            last = last_beat_position(view, positions)
            if last is None or last >= turn_position:
                continue
            rank = size_rank(view.size)
            if rank > turn_rank or (rank == turn_rank and cap is None and not ladder_decides):
                problems.append(problem_at(
                    run, "W", "CRAFT-03", view.problem_record, "size",
                    f"{view.size} comes before the main turn {main.identifier} and is "
                    f"{'tighter than' if rank > turn_rank else 'as tight as'} its turn shot {turn_view.identifier} "
                    f"({turn_view.size})",
                    f"Fix: open this shot to a wider size, so that the scene's closest frame is spent on "
                    f"{main.identifier} (A2 R4)."))
        if cap_rule is not None and cap is not None and turn_rank < SIZE_LADDER.index(cap):
            problems.append(problem_at(
                run, "W", "CRAFT-03", turn_view.problem_record, "size",
                f"the main turn is at {turn_view.size}, but {cap_rule.identifier} allows its subject up to {cap} in "
                f"{scene}, and the film's ladder sets no size for this turn" +
                (f" (its rung for {scene} is on {rung_beat}, not on the main turn {main.identifier})"
                 if rung_size and rung_beat else ""),
                (f"Fix: when the rung was meant for this turn, move it to {main.identifier} (a film rule, so it asks "
                 f"the user); otherwise take the turn to {cap}" if rung_size and rung_beat else
                 f"Fix: take the turn to {cap}") +
                ", the tightest size the camera rule and the saved choices allow here (A2 R4)."))
    return problems


def ladder_rung_of(run, scene):
    """(the beat the LADDER's rung for this scene names, the rung's size, the rung's value), or (None, None, None).
    The rung's beat is the one code resolved its story point to (' = SC06-B17'), else the beat holding its line."""
    for ladder in records_of(run, "LADDER"):
        for value in ladder.get_all("rung"):
            item = split_item(value)
            point = item.first or ""
            scene_identifier, _, stored = parse_story_point(point)
            if scene_identifier != scene:
                continue
            beat = stored
            if not beat:
                try:
                    from .derive_fields import resolve_story_point
                    beat = resolve_story_point(breakdown_for_run(run), point).beat
                except Exception:  # an unresolved rung is simply not used here
                    beat = None
            size = word_of(item.get("size") or "")
            return beat, (size if size and size not in EMPTY_WORDS else None), value
    return None, None, None


def rung_size_problems(run, scene, rung_beat, rung_size):
    """A rung's beat must have a shot at the rung's size: its turn shot when it has one, else any of its shots."""
    views = [view for view in shot_views(run, scene) if rung_beat in view.beats and view.kind not in ("card", "black")]
    if not views:
        return []
    turn_views = [view for view in views if view.role == "turn"]
    wanted = turn_views or views

    def size_of(view):
        return "insert" if view.is_insert else word_of(view.size)
    if any(size_of(view) == rung_size for view in wanted):
        return []
    view = wanted[0]
    return [problem_at(
        run, "W", "CRAFT-03", view.problem_record, "size",
        f"{size_of(view)} is not the size the film's ladder gives beat {rung_beat} ({rung_size})",
        f"Fix: take the {'turn ' if turn_views else ''}shot of {rung_beat} to {rung_size}, as the ladder says, or "
        f"change the ladder rung for {scene} first (a film rule, so it asks the user).")]


def size_cap_for(run, scene, view):
    """(the tightest size a camera rule allows the turn's subject in this scene, the CAMRULE) or (None, None):
    limit_before in scenes before the one where the rule's closest size is spent, the closest size from there,
    each stepped down past a size a saved choice keeps out of this scene."""
    for subject in view.subjects or []:
        character = element_of(subject)
        if not character.startswith("CH-"):
            continue
        for rule in records_of(run, "CAMRULE"):
            if (rule.get("character") or "").strip() != character:
                continue
            closest = split_item(rule.get("closest") or "")
            closest_size = word_of(closest.first or "")
            spent_at = parse_story_point(closest.get("at") or "") if closest.get("at") else None
            spent_scene = spent_at[0] if spent_at else scene_of(closest.get("at") or "")
            limit = word_of(rule.get("limit_before") or "")
            if spent_scene and sort_key_for_identifier(scene) < sort_key_for_identifier(spent_scene) \
                    and limit in SIZE_LADDER:
                return size_allowed_by_saved_choices(run, scene, limit), rule
            if closest_size in SIZE_LADDER:
                return size_allowed_by_saved_choices(run, scene, closest_size), rule
    return None, None


def size_allowed_by_saved_choices(run, scene, size):
    """The size itself, or the next wider one while a saved choice (a RESERVE matched on 'size = <size>') keeps that
    size out of this scene: an extreme close-up saved for scenes 13 and 25 is never asked of scene 26. The scene IDs
    in allowed_in (SC13) and the scenes it keeps out ("never in scenes 26 and 27") are read; other words there ("the
    first in scene 13") are for people, since reading them as a list could turn their meaning round."""
    while size in SIZE_LADDER:
        reserved = False
        for reserve in records_of(run, "RESERVE"):
            match = re.match(r"^\s*size\s*=\s*([a-z_]+)\s*$", reserve.get("match") or "")
            if not match or match.group(1) != size:
                continue
            allowed = set(re.findall(r"\bSC\d{2,3}[A-Z]?\b", reserve.get("allowed_in") or ""))
            from .film_pass import read_places
            excluded = read_places(reserve.get("allowed_in") or "").excluded or set()
            if (allowed - excluded and scene not in allowed) or scene in excluded:
                reserved = True
        position = SIZE_LADDER.index(size)
        if not reserved or position == 0:
            return size
        size = SIZE_LADDER[position - 1]
    return size


@register_check("CRAFT-04", level="E", build=1, title="A turn beat without exactly one turn shot",
                plain="has a turn that no single turn shot shows")
def check_craft_04(run):
    problems = []
    for scene in scene_identifiers(run):
        views = shot_views(run, scene)
        if not views:
            continue
        for beat in beats_of(run, scene):
            if not is_turn_beat(beat):
                continue
            turn_shots = [view.identifier for view in views if view.role == "turn" and beat.identifier in view.beats]
            if len(turn_shots) == 1:
                continue
            if not turn_shots:
                what = f"{turn_of(beat)} has no turn shot (no shot of this beat has role: turn)"
            else:
                what = f"{turn_of(beat)} has {len(turn_shots)} turn shots ({names_list(turn_shots)})"
            problems.append(problem_at(
                run, "E", "CRAFT-04", beat, "turn", what,
                "Fix: give exactly one shot of this beat role: turn, the shot that shows its turn picture; make the "
                "others must_keep or normal."))
    return problems


def parts_of(run, scene):
    """{part ID: [beat IDs]} of a scene, from each PART's beats (a range first..last or a list); with no PART records
    the whole scene is one part (None)."""
    beats = [beat.identifier for beat in beats_of(run, scene)]
    parts = {}
    for part in of_scene(run, "PART", scene):
        written = part.get("beats") or ""
        if ".." in written:
            first, last = [piece.strip() for piece in written.split("..", 1)]
            low, high = sort_key_for_identifier(first), sort_key_for_identifier(last)
            parts[part.identifier] = [beat for beat in beats
                                      if low <= sort_key_for_identifier(beat) <= high]
        else:
            parts[part.identifier] = [piece for piece in split_list(written) if piece in beats]
    if not parts:
        parts[None] = beats
    return parts


@register_check("CRAFT-05", level="E", build=1, title="More than two beat-intensity 5s in a part",
                plain="has more beats at the highest pressure in one part than the part can carry")
def check_craft_05(run):
    problems = []
    most = int(constant_of(run, "beat_intensity_5_per_part_max", 2))
    for scene in scene_identifiers(run):
        for part_identifier, beat_identifiers in parts_of(run, scene).items():
            fives = [beat for beat in beat_identifiers
                     if run.record(beat) is not None and whole_number(run.record(beat).get("beat_intensity")) == 5]
            if len(fives) <= most:
                continue
            record = run.record(part_identifier) if part_identifier else run.record(fives[most])
            field_name = "beats" if part_identifier else "beat_intensity"
            where = f"part {part_identifier}" if part_identifier else f"scene {scene}"
            problems.append(problem_at(
                run, "E", "CRAFT-05", record, field_name,
                f"{where} has {len(fives)} beats of intensity 5 ({names_list(fives)}); the most is {most} per part",
                "Fix: lower the extra beats to 4, keeping the 5s for the part's turn and its peak (A2 R10)."))
    return problems


def moves_named_in(shot, run):
    """The camera moves a shot names: its move field (each word of it) and the moves its moments describe."""
    found = []
    for line in shot.field_lines("move"):
        written = line.value or ""
        for piece in re.split(r"\s*(?:,|/|\+|\band\b|\bthen\b)\s*", written):
            word = word_of(piece)
            if word in CAMERA_MOVE_WORDS and word not in found:
                found.append(word)
    for item in items(run, shot, "moment"):
        text = QUOTED.sub(" ", item.get("shows") or "")
        for pattern, move in CAMERA_MOVE_PHRASES:
            if pattern.search(text) and move not in found:
                found.append(move)
    return found


@register_check("CRAFT-06", level="E", build=1, title="More than one camera move in a shot",
                plain="moves the camera in more than one way in one shot")
def check_craft_06(run):
    problems = []
    for shot in records_of(run, "SHOT"):
        moves = moves_named_in(shot, run)
        scene = scene_of(shot.identifier)
        positions = beat_positions(run, scene)
        for beat_identifier in id_list(shot, "beats"):
            beat = run.record(beat_identifier)
            if beat is None or beat.type_name != "BEAT":
                continue
            for item in items(run, beat, "pause_after"):
                if word_of(item.get("picture")) == "push_in" and "push_in" not in moves and moves:
                    view_last = max((positions.get(other, -1) for other in id_list(shot, "beats")), default=-1)
                    if positions.get(beat_identifier) == view_last:
                        moves.append("push_in")
        if len(moves) <= 1:
            continue
        problems.append(problem_at(
            run, "E", "CRAFT-06", shot, "move",
            f"the shot makes {len(moves)} camera moves ({', '.join(moves)}); one shot holds one camera move",
            "Fix: keep the one move the beat needs and split the other into its own shot (B1 section 13, C3 R2)."))
    return problems


def lens_family_for(run, scene):
    """The lens family (mm list) in force for a scene: CAMSYS lens_family, changed from a scene by step_change."""
    camsys = run.record("CAMSYS")
    if camsys is None:
        return None
    family = [number_of(piece) for piece in split_list(camsys.get("lens_family") or "") if number_of(piece)]
    changes = []
    for value in camsys.get_all("step_change"):
        parts = named_parts(value)
        start = parts.get("from")
        mms = [number_of(piece) for piece in split_list(parts.get("family") or "") if number_of(piece)]
        if start and mms:
            changes.append((sort_key_for_identifier(start.strip()), mms))
    for start, mms in sorted(changes):
        if scene and sort_key_for_identifier(scene) >= start:
            family = mms
    return family or None


def lens_exception_covers(run, lens, targets):
    for exception in records_of(run, "LENS"):
        if number_of(exception.get("mm")) != lens:
            continue
        places = set(id_list(exception, "only_in"))
        if not places or places & set(targets):
            return exception
    return None


def in_story_camera_for(run, shot):
    """The in-story CAMERA a screen shot is seen through: its scene's host when that is a camera, else the first
    CAMERA its fields name (C13)."""
    scene = run.record(scene_of(shot.identifier) or "")
    host = scene.get("host") if scene is not None else None
    if host:
        camera = run.record(host.strip())
        if camera is not None and camera.type_name == "CAMERA":
            return camera
    for line in shot.fields:
        for token in re.findall(r"\bCAM-[A-Z0-9]+(?:-[A-Z0-9]+)*", line.value or ""):
            camera = run.record(token)
            if camera is not None and camera.type_name == "CAMERA":
                return camera
    return None


def screen_camera_of(run, record):
    """For a screen shot, or a setup used only by screen shots: the in-story CAMERA whose lens it takes, else None."""
    if record.type_name == "SHOT":
        return in_story_camera_for(run, record) if word_of(record.get("kind")) == "screen" else None
    users = [shot for shot in records_of(run, "SHOT") if (shot.get("setup") or "").strip() == record.identifier]
    if users and all(word_of(shot.get("kind")) == "screen" for shot in users):
        return in_story_camera_for(run, users[0])
    return None


@register_check("CRAFT-07", level="W", build=1, title="A lens outside the family without a lens exception that covers it",
                plain="uses a lens outside the film's lenses with no lens exception for it")
def check_craft_07(run):
    problems = []
    for type_name in ("SETUP", "SHOT"):
        for record in records_of(run, type_name):
            lens = number_of(record.get("lens_mm"))
            if lens is None:
                continue
            camera = screen_camera_of(run, record)
            if camera is not None:
                # in-story footage takes the lens of the camera in the story, not the film's lens family (C13)
                own = number_of(camera.get("lens_mm"))
                if own is not None and abs(own - lens) > 1e-6:
                    problems.append(problem_at(
                        run, "W", "CRAFT-07", record, "lens_mm",
                        f"{lens:g} differs from the lens of the in-story camera {camera.identifier} ({own:g}), "
                        "which this footage is seen through",
                        f"Fix: write lens_mm: {own:g}, the in-story camera's own lens (card 17)."))
                continue
            scene = scene_of(record.identifier)
            family = lens_family_for(run, scene)
            if not family or lens in family:
                continue
            targets = [target for target in (record.identifier, scene) if target]
            if type_name == "SHOT" and record.get("setup"):
                targets.append(record.get("setup").strip())
            if lens_exception_covers(run, lens, targets):
                continue
            family_words = ", ".join(f"{mm:g}" for mm in family)
            problems.append(problem_at(
                run, "W", "CRAFT-07", record, "lens_mm",
                f"{lens:g} is outside the lens family ({family_words}) and no lens exception covers "
                f"{names_list(targets)}",
                f"Fix: use a lens of the family, or add a LENS exception for {lens:g} whose only_in names this setup "
                "or scene, with its story reason (B1 R15)."))
    return problems


def plant_limit(run, plant):
    limits = constant_of(run, "plant_emphasis_max", {"plant": 1, "plot_event_plant": 2}) or {}
    plot_event = plant is not None and word_of(plant.get("plot_event")) == "yes"
    return int(limits.get("plot_event_plant" if plot_event else "plant", 1)), plot_event


@register_check("CRAFT-08", level="W", build=1,
                title="A plant louder than emphasis 1 (2 for a plot-event plant), read from thing items with plant:",
                plain="makes a plant louder than a plant may be, which gives the payoff away")
def check_craft_08(run):
    problems = []
    for shot in records_of(run, "SHOT"):
        for item in thing_items(run, shot):
            plant_identifier = item.get("plant")
            emphasis = thing_emphasis(item)
            if not plant_identifier or is_empty(plant_identifier) or emphasis is None:
                continue
            plant = run.record(plant_identifier.strip())
            limit, plot_event = plant_limit(run, plant)
            if emphasis > limit:
                problems.append(problem_at(
                    run, "W", "CRAFT-08", shot, "thing",
                    f"{item.first.strip()} plants {plant_identifier.strip()} at emphasis {emphasis:g}; a "
                    f"{'plot-event ' if plot_event else ''}plant is at most emphasis {limit}",
                    f"Fix: lower the plant to emphasis {limit}; the payoff is where it gets loud (K11, B4 R6).",
                    containing=plant_identifier.strip()))
    for plant in records_of(run, "PLANT"):
        emphasis = number_of(plant.get("plant_emphasis"))
        limit, plot_event = plant_limit(run, plant)
        if emphasis is not None and emphasis > limit:
            problems.append(problem_at(
                run, "W", "CRAFT-08", plant, "plant_emphasis",
                f"{emphasis:g} is louder than a {'plot-event ' if plot_event else ''}plant may be (at most {limit})",
                f"Fix: lower plant_emphasis to {limit}" + ("" if plot_event else
                                                           ", or mark the plant plot_event: yes if the plot turns on it")
                + " (K11)."))
    return problems


@register_check("CRAFT-09", level="W", build=1, title="Emphasis-3 budgets broken",
                plain="spends the loudest emphasis more often than its budget allows")
def check_craft_09(run):
    problems = []
    rules = constant_of(run, "emphasis_3_rules", {}) or {}
    per_motif = int(rules.get("per_motif_in_film_max", 1))
    per_scene = int(rules.get("per_scene_max", 2))
    loud_by_motif = {}
    for scene in scene_identifiers(run):
        loud = []
        for shot in shots_of(run, scene):
            loud_items = [item for item in thing_items(run, shot) if (thing_emphasis(item) or 0) >= 3]
            if not loud_items:
                continue
            loud.append((shot, loud_items))
            for item in loud_items:
                motif = motif_of_thing(run, item.first)
                if motif:
                    loud_by_motif.setdefault(motif, []).append(shot)
        if len(loud) > per_scene:
            for shot, _ in loud[per_scene:]:
                problems.append(problem_at(
                    run, "W", "CRAFT-09", shot, "thing",
                    f"is emphasis-3 use {[entry[0] for entry in loud].index(shot) + 1} of {len(loud)} in {scene}; "
                    f"the most is {per_scene} per scene",
                    "Fix: lower this thing to emphasis 2 (B4)."))
        elif len(loud) == per_scene and per_scene > 1 and rules.get("on_different_turns", True):
            turns = set()
            for shot, _ in loud:
                turns.update(beat for beat in id_list(shot, "beats")
                             if run.record(beat) is not None and is_turn_beat(run.record(beat)))
            if len(turns) < len(loud):
                shot = loud[-1][0]
                problems.append(problem_at(
                    run, "W", "CRAFT-09", shot, "thing",
                    f"the scene's {len(loud)} emphasis-3 uses ({names_list([entry[0].identifier for entry in loud])}) "
                    "are not on different turns",
                    "Fix: keep emphasis 3 for one turn each, and lower the other to 2 (B4)."))
        if not rules.get("in_consecutive_shots", False):
            ordered = [view.identifier for view in shot_views(run, scene) if not view.is_card]
            loud_identifiers = [shot.identifier for shot, _ in loud]
            for first, second in zip(ordered, ordered[1:]):
                if first in loud_identifiers and second in loud_identifiers:
                    problems.append(problem_at(
                        run, "W", "CRAFT-09", run.record(second), "thing",
                        f"emphasis 3 follows emphasis 3 in the shot before ({first})",
                        "Fix: never put emphasis 3 in two shots in a row; lower one of them to 2 (B4)."))
    for motif, shots in loud_by_motif.items():
        distinct = []
        for shot in shots:
            if shot not in distinct:
                distinct.append(shot)
        if len(distinct) > per_motif:
            for shot in distinct[per_motif:]:
                problems.append(problem_at(
                    run, "W", "CRAFT-09", shot, "thing",
                    f"{motif} reaches emphasis 3 again ({names_list([other.identifier for other in distinct])}); a "
                    f"motif reaches emphasis 3 at most {per_motif} time in the film",
                    "Fix: keep emphasis 3 for the motif's one payoff and lower this use to 2 (B4).",
                    containing=motif))
    for motif in records_of(run, "MOTIF"):
        loud = [item for item in items(run, motif, "appearance") if (whole_number(item.get("emphasis"), 0) or 0) >= 3]
        if len(loud) > per_motif:
            problems.append(problem_at(
                run, "W", "CRAFT-09", motif, "appearance",
                f"has {len(loud)} appearances at emphasis 3; a motif reaches emphasis 3 at most {per_motif} time",
                "Fix: keep emphasis 3 for its payoff and lower the others (B4)."))
    return problems


def dial_items(run, scene):
    """{beat ID: Item} of a scene's dial."""
    record = scene_record(run, scene)
    return {item.first.strip(): item for item in items(run, record, "dial") if item.first}


def added_emphasis_of(run, beat):
    found = items(run, beat, "added_emphasis")
    if not found:
        value = beat.get("added_emphasis")
        return number_of(value), None
    return number_of(found[0].first), found[0]


# Words of sound or its absence that a script writes in lower case (the reader's SOUND_WORDS are effects in capitals).
QUIET_WORDS = {"silence", "silent", "quiet", "quieter", "hush", "hushed", "noise", "sound", "sounds", "soundless",
               "deaf", "deafening", "loud", "louder"}


def reason_quotes_lines(run, text, lines, kind=None):
    """True when a reason quotes words found in the given lines (the script's own words). With kind "light" or
    "sound", the quote must also hold a light or sound word of the story (read_story's word lists): quoting any line
    of the beat does not excuse a light or sound the line does not write."""
    if not lines or run.story is None:
        return False
    from .read_story import LIGHT_WORDS, SOUND_WORDS
    wanted = {"light": {word.lower() for word in LIGHT_WORDS},
              "sound": {word.lower() for word in SOUND_WORDS} | QUIET_WORDS}.get(kind)
    first, last = min(lines), max(lines)
    for match in QUOTED.finditer(text or ""):
        quote = match.group(1)
        if wanted is not None and not ({word.lower() for word in re.findall(r"[A-Za-z]+", quote)} & wanted):
            continue
        if quote_found(run, quote, (first, last)):
            return True
    return False


def rupture_points_at(run, item, lines, identifiers):
    """True when a rupture_plan line of the sound plan points at this moment: it names one of the given beat or shot
    IDs, or it quotes words found in the given lines."""
    text = " ".join(part for part in (item.first or "", item.get("device") or "") if part)
    if any(identifier and re.search(rf"\b{re.escape(identifier)}\b", text) for identifier in identifiers):
        return True
    if not lines or run.story is None:
        return False
    first, last = min(lines), max(lines)
    return any(quote_found(run, match.group(1), (first, last)) for match in QUOTED.finditer(text))


def beat_lines(run, beat):
    numbers = parse_line_numbers(beat.get("lines") or "") if beat.get("lines") else None
    if numbers:
        found = set()
        for first, last in numbers:
            found.update(range(first, last + 1))
        return sorted(found)
    breakdown = breakdown_of(run)
    return breakdown.lines_of(beat)


def shot_light_sound_changes(run, shot, beat=None):
    """[(field, what)] of the light and sound changes a shot adds (CRAFT-10, CRAFT-19). Not added, so not counted:
    light (or a light cue) that quotes the lines of the shot's beats, the script's own light (the same cue then
    covers COVER-08); silence room_sound_only, which keeps the room's sound; and a silence the film's sound plan
    or the beat's own pause already plans (a rupture_plan of this scene naming it, or the pause's sound)."""
    changes = []
    lines = []
    for beat_identifier in ([beat.identifier] if beat is not None else id_list(shot, "beats")):
        record = run.record(beat_identifier)
        if record is not None and record.type_name == "BEAT":
            lines += beat_lines(run, record)
    lines += [number for first, last in (parse_line_numbers(shot.get("lines") or "") or []) for number in
              range(first, last + 1)]
    light = shot.get("light")
    if light and not is_empty(light) and word_of(light) != "as_look" and \
            not reason_quotes_lines(run, light, lines, "light"):
        changes.append(("light", f"light {light}"))
    for item in items(run, shot, "light_cue"):
        if item.first and not is_empty(item.first):
            if reason_quotes_lines(run, item.get("why"), lines, "light") or \
                    reason_quotes_lines(run, item.first, lines, "light"):
                continue
            changes.append(("light_cue", f"light cue: {item.first}"))
    silence = shot.get("silence")
    if silence and not is_empty(silence) and word_of(silence) != "room_sound_only" and \
            not silence_planned(run, shot, word_of(silence), beat, lines):
        changes.append(("silence", f"silence {word_of(silence)}"))
    music = shot.get("music")
    if music and not is_empty(music):
        changes.append(("music", f"music {music}"))
    return changes


def silence_planned(run, shot, silence, beat=None, lines=None):
    """True when the film's sound plan or the beat's own pause plans this silence: a SOUNDPLAN rupture_plan for the
    shot's scene whose device names it and points at this moment (it names the shot or one of its beats, quotes the
    shot's lines, or names the black or card that this shot is), or a pause_after of one of the shot's beats whose
    sound names it. A rupture planned somewhere in the scene does not excuse every silence in it."""
    words = silence.replace("_", " ")
    stems = {words, words.replace("true ", ""), words.replace(" ", "-"), words.replace(" ", "")}
    scene = scene_of(shot.identifier)
    beats = [beat] if beat is not None else [run.record(identifier) for identifier in id_list(shot, "beats")]
    identifiers = [shot.identifier] + [record.identifier for record in beats if record is not None]
    kind = word_of(shot.get("kind"))

    def names_it(text):
        lowered = (text or "").lower()
        return any(stem and stem in lowered for stem in stems)
    for plan in records_of(run, "SOUNDPLAN"):
        for item in items(run, plan, "rupture_plan"):
            if not (item.first and same_scene(item.first.strip(), scene) and names_it(item.get("device"))):
                continue
            device = (item.get("device") or "").lower()
            if rupture_points_at(run, item, lines or [], identifiers) or \
                    (kind in ("black", "card") and re.search(r"\b(black|blacks|card|cards|title)\b", device)):
                return True
    if scene_rupture_on(run, scene, identifiers, names_it):
        return True
    for record in beats:
        if record is None or record.type_name != "BEAT":
            continue
        for pause in items(run, record, "pause_after"):
            if names_it(pause.get("sound")):
                return True
    return False


def scene_rupture_on(run, scene, identifiers, device_test=None):
    """True when the scene's own rupture (SCENE rupture: the beat | device: ...) sits on one of these beats, and,
    with device_test, its device passes it (names the silence)."""
    record = scene_record(run, scene)
    for item in items(run, record, "rupture") if record is not None else []:
        if (item.first or "").strip() in identifiers and (device_test is None or device_test(item.get("device"))):
            return True
    return False


@register_check("CRAFT-10", level="W", build=1,
                title="Added emphasis above 1 on a beat, or above 0 where the script marks the beat; an added light "
                      "or sound change on a beat the script already marks",
                plain="adds its own signal to a moment the script already marks, which says it twice")
def check_craft_10(run):
    problems = []
    breakdown = breakdown_of(run)
    limits = constant_of(run, "added_emphasis_per_beat_max", {"max": 1, "where_script_marks_the_beat": 0}) or {}
    most = limits.get("max", 1)
    most_marked = limits.get("where_script_marks_the_beat", 0)
    story_missing = False
    for scene in scene_identifiers(run):
        dial = dial_items(run, scene)
        for beat in beats_of(run, scene):
            added, _ = added_emphasis_of(run, beat)
            if added is not None and added > most:
                problems.append(problem_at(
                    run, "W", "CRAFT-10", beat, "added_emphasis",
                    f"{added:g} is above the most a beat may add ({most})",
                    f"Fix: set added_emphasis to {most} or 0 (B4 R23)."))
                continue
            if run.story is None:
                story_missing = True
                continue
            marked, how = script_marked(breakdown, beat)
            if marked is None:
                story_missing = True
                continue
            if marked != "yes":
                continue
            if added is not None and added > most_marked:
                problems.append(problem_at(
                    run, "W", "CRAFT-10", beat, "added_emphasis",
                    f"{added:g} adds a signal where the script already marks the beat ({how})",
                    f"Fix: set added_emphasis to {most_marked}; the script's own mark is enough (B4 R23, B1 P11)."))
            item = dial.get(beat.identifier)
            if item is not None:
                light, sound = item.get("light"), item.get("sound")
                changed = []
                lines = beat_lines(run, beat)
                if light and not is_empty(light) and word_of(light) != "as_look" and \
                        not reason_quotes_lines(run, light, lines, "light"):
                    changed.append(f"light {light}")
                if sound and not is_empty(sound) and word_of(sound) != "room_sound" and \
                        not reason_quotes_lines(run, sound, lines, "sound") and \
                        not rupture_planned(run, scene, beat, lines):
                    changed.append(f"sound {sound}")
                if changed:
                    problems.append(problem_at(
                        run, "W", "CRAFT-10", scene_record(run, scene), "dial",
                        f"the dial for {beat.identifier} adds {' and '.join(changed)} where the script already "
                        f"marks the beat ({how})",
                        "Fix: keep light: as_look and sound: room_sound on this beat (B2 R10).",
                        containing=beat.identifier))
            for view in shots_on_beat(run, scene, beat.identifier, written_only=True):
                if view.is_card or any(other != beat.identifier and not script_marked_yes(breakdown, run, other)
                                       for other in view.beats):
                    continue
                for field_name, what in shot_light_sound_changes(run, view.record, beat):
                    problems.append(problem_at(
                        run, "W", "CRAFT-10", view.record, field_name,
                        f"adds a change ({what}) on {beat.identifier}, which the script already marks ({how})",
                        f"Fix: take the added change out; the script's own mark is enough (B4 R23, B1 P11)."))
    if story_missing:
        run.skip("CRAFT-10", "story not present, so the beats the script already marks are not known (added emphasis "
                             "above the most was still checked)")
    return problems


def rupture_planned(run, scene, beat=None, lines=None):
    """True when the film's sound plan has a rupture_plan for this scene that points at this beat (it names the beat
    or quotes its lines): the dial's sound change there is planned. Without a beat, any rupture of the scene."""
    for plan in records_of(run, "SOUNDPLAN"):
        for item in items(run, plan, "rupture_plan"):
            if not (item.first and same_scene(item.first.strip(), scene)):
                continue
            if beat is None or rupture_points_at(run, item, lines or [], [beat.identifier]):
                return True
    return beat is not None and scene_rupture_on(run, scene, [beat.identifier])


def script_marked_yes(breakdown, run, beat_identifier):
    beat = run.record(beat_identifier)
    if beat is None or beat.type_name != "BEAT":
        return False
    marked, _ = script_marked(breakdown, beat)
    return marked == "yes"


def reserve_match(run, reserve):
    """(field, value) a RESERVE's match names ('frame_detail = symmetrical_profile'), or None for manual."""
    written = reserve.get("match") or ""
    if "=" not in written:
        return None
    field_name, _, value = written.partition("=")
    return normalise_word(field_name).strip("_"), word_of(value)


# The camera fields an in-story camera decides in a shot that is its own picture (kind screen).
IN_STORY_CAMERA_FIELDS = {"angle", "move", "lens_mm", "travel"}


def shots_using(run, reserve):
    matched = reserve_match(run, reserve)
    if matched is None:
        return []
    field_name, value = matched
    found = []
    for shot in records_of(run, "SHOT"):
        if field_name in IN_STORY_CAMERA_FIELDS and word_of(shot.get("kind")) == "screen":
            continue  # the in-story camera's own angle, move or lens, not the film's choice
        if field_name == "subject" or field_name == "display":
            values = [word_of(item.get(field_name)) for item in items(run, shot, "subject")]
        else:
            values = [word_of(shot.get(field_name))]
        if value in values:
            found.append(shot)
    return found


def reserve_places(run, reserve):
    """What a RESERVE's allowed_in names: IDs, scene numbers ('scene 29') and whether main turns are allowed."""
    text = reserve.get("allowed_in") or ""
    identifiers = {match.group(1) for match in ID_TOKEN.finditer(text)}
    from .film_pass import NOT_IN
    text = NOT_IN.sub(" ", text)  # scenes a choice keeps out are not places it is allowed
    scenes = {f"SC{int(number):02d}" for listed in re.findall(r"\bscenes?\s+(\d{1,3}(?:\s*(?:,|and|or)\s*\d{1,3})*)",
                                                            text, re.I) for number in re.findall(r"\d{1,3}", listed)}
    main_turns = bool(re.search(r"\bmain\s+turns?\b", text, re.I))
    turns = bool(re.search(r"(?<!main )\bturns?\b", text, re.I)) and not main_turns
    return identifiers, scenes, main_turns, turns


def use_is_allowed(run, reserve, shot):
    identifiers, scenes, main_turns, turns = reserve_places(run, reserve)
    if not (identifiers or scenes or main_turns or turns):
        return None
    scene = scene_of(shot.identifier)
    from .film_pass import read_places
    if any(same_scene(scene, other) for other in (read_places(reserve.get("allowed_in") or "").excluded or ())):
        return False  # "never in scenes 26 and 27"
    beats = id_list(shot, "beats")
    places = {shot.identifier, scene, (shot.get("setup") or "").strip()} | set(beats)
    if places & identifiers:
        return True
    if any(same_scene(scene, other) for other in scenes):
        return True
    for beat_identifier in beats:
        beat = run.record(beat_identifier)
        if beat is None or beat.type_name != "BEAT":
            continue
        if main_turns and turn_of(beat) == "main_turn":
            return True
        if turns and is_turn_beat(beat):
            return True
    return False


def shot_is_on(run, shot):
    """The person a shot is on: its focus_on when that names a person, else its first person subject."""
    focus = element_of((shot.get("focus_on") or "").strip())
    if focus.startswith("CH-"):
        return {focus}
    for element in subject_elements_of_shot(run, shot):
        if element.startswith("CH-"):
            return {element}
    return set()


def scene_count(run):
    counted = len(run.scene_ids())
    if run.story is not None:
        counted = max(counted, run.story.scene_count() or 0)
    return counted


def banned_choices(run):
    camsys = run.record("CAMSYS")
    if camsys is None:
        return []
    return [word_of(item.first) for item in items(run, camsys, "banned") if item.first]


def banned_uses(run, banned):
    """[(record, field, value)] of every place a banned choice is used: a SHOT's word fields, a CUT's type, a
    SCENE's time treatment (a banned 'low angle' also matches angle: low)."""
    found = []
    for shot in records_of(run, "SHOT"):
        for field_name in ("move", "angle", "size", "frame", "frame_detail", "focus", "silence"):
            value = word_of(shot.get(field_name))
            if value and (value == banned or f"{value}_{field_name}" == banned):
                found.append((shot, field_name, value))
    for cut in records_of(run, "CUT"):
        value = word_of(cut.get("type"))
        if value and value == banned:
            found.append((cut, "type", value))
    for scene in records_of(run, "SCENE"):
        value = word_of(scene.get("time_treatment"))
        if value and value == banned:
            found.append((scene, "time_treatment", value))
    return found


@register_check("CRAFT-11", level="E", build=1,
                title="A reserved choice beyond its uses or outside its allowed places; a banned choice used",
                plain="spends a saved choice more often or somewhere other than planned, or uses a choice the film bans")
def check_craft_11(run):
    problems = []
    covered_moves = set()
    for reserve in records_of(run, "RESERVE"):
        matched = reserve_match(run, reserve)
        if matched is None:
            continue
        covered_moves.add(matched)
        uses = shots_using(run, reserve)
        limit_text = (reserve.get("max_uses") or "").strip()
        limit_word = word_of(limit_text.split("|")[0])
        if limit_word == "1_per_scene":
            by_scene = {}
            for shot in uses:
                by_scene.setdefault(scene_of(shot.identifier), []).append(shot)
            for scene, shots in by_scene.items():
                for shot in shots[1:]:
                    problems.append(problem_at(
                        run, "E", "CRAFT-11", shot, matched[0],
                        f"{matched[1]} spends {reserve.identifier} a second time in {scene} "
                        f"({names_list([other.identifier for other in shots])}); it allows 1 per scene",
                        f"Fix: keep one use in the scene and change the other (saved choice {reserve.identifier})."))
        elif limit_word == "share":
            item = split_item(limit_text, definition_of(run, "RESERVE", "max_uses"))
            fraction = number_of(item.get("fraction"))
            total = scene_count(run)
            scenes = sorted({scene_of(shot.identifier) for shot in uses}, key=sort_key_for_identifier)
            if fraction is not None and total and len(scenes) > fraction * total:
                allowed = int(fraction * total)
                for scene in scenes[allowed:]:
                    shot = next(shot for shot in uses if scene_of(shot.identifier) == scene)
                    problems.append(problem_at(
                        run, "E", "CRAFT-11", shot, matched[0],
                        f"{matched[1]} brings {reserve.identifier} to {len(scenes)} of {total} scenes; it allows "
                        f"{fraction:g} of scenes ({allowed})",
                        f"Fix: keep {reserve.identifier} for the scenes that need it most and change this use."))
        else:
            limit = number_of(limit_text)
            if limit is not None and len(uses) > limit:
                for shot in uses[int(limit):]:
                    problems.append(problem_at(
                        run, "E", "CRAFT-11", shot, matched[0],
                        f"{matched[1]} is use {uses.index(shot) + 1} of {reserve.identifier}, which allows "
                        f"{limit:g} ({names_list([other.identifier for other in uses])})",
                        f"Fix: change this shot, or answer a choice that raises {reserve.identifier}'s max_uses."))
        never_on = set(element_of(piece) for piece in id_list(reserve, "never_on"))
        for shot in uses:
            on = shot_is_on(run, shot)
            allowed = use_is_allowed(run, reserve, shot)
            if allowed is False:
                problems.append(problem_at(
                    run, "E", "CRAFT-11", shot, matched[0],
                    f"{matched[1]} spends {reserve.identifier} outside its allowed places "
                    f"({reserve.get('allowed_in')})",
                    f"Fix: keep {reserve.identifier} for the places it names, or change this shot."))
            if never_on & on:
                problems.append(problem_at(
                    run, "E", "CRAFT-11", shot, matched[0],
                    f"{matched[1]} spends {reserve.identifier} on {names_list(sorted(never_on & on))}, which it is "
                    "never used on",
                    f"Fix: change this shot; {reserve.identifier} is never_on {names_list(sorted(never_on))}."))
    for shot in records_of(run, "SHOT"):
        move = word_of(shot.get("move"))
        if move in MOVES_ONLY_WHEN_SAVED and ("move", move) not in covered_moves:
            problems.append(problem_at(
                run, "E", "CRAFT-11", shot, "move",
                f"{move} is a camera move used only as a saved choice, and no RESERVE covers it",
                "Fix: use one of the ordinary camera moves, or save it as a choice in 10 Film rules first (5.5)."))
        angle = word_of(shot.get("angle"))
        if angle in ANGLES_ONLY_WHEN_SAVED and ("angle", angle) not in covered_moves:
            problems.append(problem_at(
                run, "E", "CRAFT-11", shot, "angle",
                f"{angle} is an angle used only as a saved choice, and no RESERVE covers it",
                "Fix: use eye_level, low, high, top_down or worms_eye, or save the angle as a choice first (5.5)."))
    for banned in banned_choices(run):
        for record, field_name, value in banned_uses(run, banned):
            problems.append(problem_at(
                run, "E", "CRAFT-11", record, field_name,
                f"{value} is a choice the camera system bans ({banned})",
                "Fix: choose another value; CAMSYS banned lists what this film never does."))
    return problems


def film_is_short(run):
    project = run.project_record
    if project is not None and word_of(project.get("format")):
        return word_of(project.get("format")) == "short"
    return True


def device_budget(run):
    """{device: most uses} for the editor-made devices: SOUNDPLAN device_budget, else device_budget_short in a short."""
    budget = {}
    soundplan = run.record("SOUNDPLAN")
    if soundplan is not None:
        for item in items(run, soundplan, "device_budget"):
            most = number_of(item.get("max"))
            if item.first and most is not None:
                budget[word_of(item.first)] = most
    if not budget and film_is_short(run):
        budget = dict(constant_of(run, "device_budget_short", {}) or {})
    return budget


def same_join(device, written):
    written = word_of(written or "")
    return bool(written) and (written == device or (device == "fade" and written in ("fade_in", "fade_out")))


def scene_transitions(run, scene):
    """(transition_in, transition_out) a scene's story writes: its SCENE record, else the story map."""
    record = scene_record(run, scene)
    found = [record.get("transition_in") if record else None, record.get("transition_out") if record else None]
    if run.story is not None:
        for entry in (run.story.story_map or {}).get("scenes") or []:
            if same_scene(entry.get("id"), scene):
                found = [found[0] or entry.get("transition_in"), found[1] or entry.get("transition_out")]
    return found


def cut_ends_scene(run, cut):
    """True when a CUT is the scene's way out: its next shot is in another scene, or only cards and black follow."""
    scene = scene_of(cut.identifier)
    target = (cut.get("to") or "").strip()
    if target and not same_scene(scene_of(target), scene):
        return True
    views = shot_views(run, scene)
    after = [view for view in views if sort_key_for_identifier(view.identifier) >= sort_key_for_identifier(target)] \
        if target else []
    return bool(after) and all(view.is_card for view in after)


def story_writes_device(run, record, device):
    """True when the story writes a join or device: the scene's written transition out (for the cut that ends the
    scene), the next scene's transition in, the story map's instructions, or a quote in the record's why that holds
    the device's words and is found in the scene."""
    scene = scene_of(record.identifier)
    words = DEVICE_WORDS.get(device, (device.replace("_", " "),))
    if record.type_name == "CUT" and cut_ends_scene(run, record):
        transition_in, transition_out = scene_transitions(run, scene)
        if same_join(device, transition_out):
            return True
        target_scene = scene_of((record.get("to") or "").strip())
        if target_scene and not same_scene(target_scene, scene):
            if same_join(device, scene_transitions(run, target_scene)[0]):
                return True
    if run.story is not None:
        for entry in (run.story.story_map or {}).get("scenes") or []:
            if not same_scene(entry.get("id"), scene):
                continue
            for instruction in entry.get("instructions") or []:
                text = str(instruction.get("text") if isinstance(instruction, dict) else instruction).lower()
                if any(word in text for word in words):
                    return True
    why = record.get("why") or ""
    scope = run.scene_range(scene) if scene else None
    for match in QUOTED.finditer(why):
        quote = match.group(1)
        if any(word in quote.lower() for word in words) and quote_found(run, quote, scope) is not False:
            return True
    return False


def editor_made_uses(run):
    """[(device, record, field)] of the editor-made cuts to black, true silences and freezes, in film order."""
    found = []
    for scene in scene_identifiers(run):
        for cut in of_scene(run, "CUT", scene):
            device = word_of(cut.get("type"))
            if device in ("cut_to_black", "freeze") and not story_writes_device(run, cut, device):
                found.append((device, cut, "type"))
        for view in shot_views(run, scene):
            if not view.written or view.is_card:
                continue
            if word_of(view.record.get("silence")) == "true_silence":
                why = view.record.get("why") or ""
                if any("silen" in match.group(1).lower() for match in QUOTED.finditer(why)):
                    continue
                found.append(("true_silence", view.record, "silence"))
    return found


@register_check("CRAFT-12", level="W", build=1, title="Editor-made device budgets exceeded (film)",
                plain="uses more cuts to black, true silences or freezes of its own than the film allows")
def check_craft_12(run):
    problems = []
    budget = device_budget(run)
    counts = {}
    for device, record, field_name in editor_made_uses(run):
        counts.setdefault(device, []).append(record)
        most = budget.get(device)
        if most is None or len(counts[device]) <= most:
            continue
        problems.append(problem_at(
            run, "W", "CRAFT-12", record, field_name,
            f"{device} is editor-made use {len(counts[device])} in the film; the budget is {most:g} "
            f"({names_list([other.identifier for other in counts[device]])})",
            "Fix: keep the uses on the film's strongest moments and take this one out, or raise the budget in "
            "SOUNDPLAN device_budget through a choice (A4 P10)."))
    return problems


@register_check("CRAFT-13", level="W", build=1,
                title="A dissolve, fade, cut to black, freeze or smash cut that the story does not write; a match cut "
                      "whose why names no shared shape, motion or sound",
                plain="joins two shots in a way the story does not write, or matches two shots with no shared shape, "
                      "motion or sound")
def check_craft_13(run):
    problems = []
    for cut in records_of(run, "CUT"):
        device = word_of(cut.get("type"))
        if device in JOINS_THE_STORY_MUST_WRITE and not story_writes_device(run, cut, device):
            problems.append(problem_at(
                run, "W", "CRAFT-13", cut, "type",
                f"{device} is a join the story does not write",
                "Fix: make it a cut (J-cuts, L-cuts and jump cuts are free), or quote the story's own words for "
                "this join in why (A4 T5)."))
        elif device == "match_cut":
            why = cut.get("why") or ""
            shared = cut.get("shared_geometry")
            if (shared and not is_empty(shared)) or SHARED_SHAPE_MOTION_SOUND.search(QUOTED.sub(" ", why)):
                continue
            problems.append(problem_at(
                run, "W", "CRAFT-13", cut, "why",
                "names no shape, motion or sound the two shots share" if why else
                "is missing, so the match cut names no shape, motion or sound the two shots share",
                "Fix: say in why what the shots share (the same round shape, the same fall, the same sound), or "
                "make it a cut (A4 T5)."))
    return problems


def addition_texts(run, scene):
    record = scene_record(run, scene)
    return [item.first.strip() for item in items(run, record, "additions") if item.first]


def content_words(text):
    """The main words of a text, lower case, with a plain final "s" taken off ("stands" and "stand" match; the second
    full run, Project notes 39); "glass" keeps its "ss"."""
    return [without_plain_s(word) for word in (piece.lower().strip("'’-") for piece in WORD_PIECE.findall(text or ""))
            if word and word not in STOP_WORDS and len(word) > 1]


def without_plain_s(word):
    return word[:-1] if len(word) > 3 and word.endswith("s") and not word.endswith("ss") else word


def addition_listed(run, scene, element=None, text=None):
    listed = addition_texts(run, scene)
    if element is not None:
        for entry in listed:
            if element in {element_of(match.group(1)) for match in ID_TOKEN.finditer(entry)}:
                return True
        names = element_name_list(run, element)
        return any(named_element_in(entry, names) for entry in listed)
    words = set(content_words(text))
    if not words:
        return True
    for entry in listed:
        entry_words = set(content_words(entry))
        if entry_words and len(words & entry_words) >= max(1, round(0.6 * len(words))):
            return True
    return False


def invented(run, reference):
    """True when a thing in frame is invented: the element's own record (a person, thing, place or text) has
    origin: invented. A state's origin says where its costume or condition comes from, not the thing itself."""
    element = run.record(element_of(reference))
    return element is not None and word_of(element.get("origin")) == "invented"


@register_check("CRAFT-14", level="E", build=1, title="An invented thing in frame not listed in the scene's additions",
                plain="puts something invented in the picture without listing it as an addition for you to keep or cut")
def check_craft_14(run):
    problems = []
    for scene in scene_identifiers(run):
        if not shots_of(run, scene):
            # step 7: the one-line list's subjects (the second full run, Project notes 39: an invented record shown
            # in a scene was found only at step 8, a repair round later)
            reported = set()
            for view in shot_views(run, scene):
                for element in view.subjects:
                    if element in reported or not invented(run, element) or \
                            addition_listed(run, scene, element=element):
                        continue
                    reported.add(element)
                    problems.append(problem_at(
                        run, "E", "CRAFT-14", view.list_record, "item",
                        f"{element} is invented (origin: invented) and is not in {scene}'s additions "
                        f"(list item {view.identifier})",
                        f"Fix: add it to SCENE {scene} additions with changes_meaning: yes or no, or take it out of the "
                        "item (B3 R24, C5 R27).", containing=element))
            continue
        for shot in shots_of(run, scene):
            reported = set()
            references = [(item.first.strip(), "thing") for item in thing_items(run, shot)]
            references += [(item.first.strip(), "subject") for item in items(run, shot, "subject") if item.first]
            references += [(reference, "must_show") for reference in id_list(shot, "must_show")]
            for reference, field_name in references:
                element = element_of(reference)
                if element in reported or not invented(run, reference):
                    continue
                if addition_listed(run, scene, element=element):
                    continue
                reported.add(element)
                problems.append(problem_at(
                    run, "E", "CRAFT-14", shot, field_name,
                    f"{reference} is invented (origin: invented) and is not in {scene}'s additions",
                    f"Fix: add it to SCENE {scene} additions with changes_meaning: yes or no, or take it out of the "
                    "shot (B3 R24, C5 R27).", containing=reference))
            additions = shot.get("additions")
            if additions and not is_empty(additions) and not addition_listed(run, scene, text=additions):
                problems.append(problem_at(
                    run, "E", "CRAFT-14", shot, "additions",
                    f"{quote_for_message(additions)} is not in {scene}'s additions",
                    f"Fix: add it to SCENE {scene} additions with changes_meaning: yes or no, or take it out of the "
                    "shot."))
    return problems


def speaks_on_screen(run, shot, element):
    """True when a person speaks in the shot with their mouth seen (a hear item with speaker: on_screen)."""
    for item in items(run, shot, "hear"):
        if word_of(item.get("speaker")) == "on_screen" and speaker_of(run, (item.first or "").strip()) == element:
            return True
    return False


def acting_characters(run, shot):
    """The people in a shot who act: every person subject, apart from those in the background: energy: still and
    no line spoken on screen in this shot. An older breakdown's still: whole_body counts as background too (the
    subject's still sub-part is kept only so that those breakdowns load; Project notes 43)."""
    found = []
    for item in items(run, shot, "subject"):
        if not item.first:
            continue
        element = element_of(item.first.strip())
        record = run.record(element)
        if not element.startswith("CH-") and not (record is not None and record.type_name == "CHARACTER"):
            continue
        old_still = [word_of(piece) for piece in split_list(item.get("still") or "")]
        if "whole_body" in old_still:
            continue
        if word_of(item.get("energy")) == "still" and not speaks_on_screen(run, shot, element):
            continue
        if element not in found:
            found.append(element)
    return found


@register_check("CRAFT-15", level="W", build=1, title="More than three acting characters in a shot",
                plain="asks too many people to act at once in one shot")
def check_craft_15(run):
    problems = []
    most = int(constant_of(run, "acting_characters_per_clip_max", 3))
    for shot in records_of(run, "SHOT"):
        acting = acting_characters(run, shot)
        if len(acting) > most:
            problems.append(problem_at(
                run, "W", "CRAFT-15", shot, "subject",
                f"{len(acting)} people act in the shot ({names_list(acting)}); the most is {most}",
                "Fix: keep the others in the background (energy: still, with no line on screen in this shot), or "
                "split the shot (C3 L22)."))
    return problems


def slow_playback_banned(run):
    camsys = run.record("CAMSYS")
    if camsys is None:
        return None
    if word_of(camsys.get("camera_speed")) == "real_time":
        return "camera_speed real_time"
    for banned in banned_choices(run):
        if banned in ("slow_motion", "slow_playback", "slowmo", "slow_mo"):
            return f"banned {banned}"
    return None


def slow_playback_in(text):
    for match in SLOW_PLAYBACK.finditer(text or ""):
        if NEGATION_BEFORE.search(text[:match.start()]):
            continue
        return match.group(1)
    return None


@register_check("CRAFT-16", level="E", build=1, title="Slow playback where the camera system bans it",
                plain="slows the picture down in a film whose camera system plays everything in real time")
def check_craft_16(run):
    reason = slow_playback_banned(run)
    if reason is None:
        return []
    problems = []
    for scene in records_of(run, "SCENE"):
        if word_of(scene.get("time_treatment")) == "slow_motion":
            problems.append(problem_at(
                run, "E", "CRAFT-16", scene, "time_treatment",
                f"slow_motion is banned by the camera system ({reason})",
                "Fix: use overlapping_slices or held_real_time, built from real-time pieces (K30)."))
    for shot in records_of(run, "SHOT"):
        texts = [("moment", item.get("shows") or "") for item in items(run, shot, "moment")]
        texts += [(name, shot.get(name) or "") for name in ("gen_note", "physics_note")]
        texts += [("subject", item.get("does") or "") for item in items(run, shot, "subject")]
        for field_name, text in texts:
            found = slow_playback_in(QUOTED.sub(" ", text))
            if found:
                problems.append(problem_at(
                    run, "E", "CRAFT-16", shot, field_name,
                    f'asks for slow playback ("{found}"), which the camera system bans ({reason})',
                    "Fix: play it in real time; build expanded time from overlapping real-time slices (K30).",
                    containing=found))
                break
    return problems


@register_check("CRAFT-17", level="W", build=2, title="A shot's size two or more steps from the dial for its beat",
                plain="frames a beat much closer or wider than the scene's dial planned")
def check_craft_17(run):
    run.skip("CRAFT-17", "planned for the second build: a shot's size is compared with its beat's dial once the test "
                         "runs show how often a scene's cutting leaves its dial")
    return []


CHARGE_SIGNS = {"---": -1, "--": -1, "-": -1, "0": 0, "+": 1, "++": 1, "+++": 1}


def value_items(run, scene):
    record = scene_record(run, scene)
    return [item for item in items(run, record, "value") if item.first]


def charges_of(run, beat):
    return {item.first.strip(): (item.get("charge") or "").strip() for item in items(run, beat, "charge") if item.first}


@register_check("CRAFT-18", level="E", build=1,
                title="A turn beat that changes the sign of no value's charge and reaches no value's close (the sign "
                      "test)",
                plain="is marked as a turn, but no value changes from positive to negative or reaches its end")
def check_craft_18(run):
    problems = []
    for scene in scene_identifiers(run):
        values = {item.first.strip(): item for item in value_items(run, scene)}
        current = {name: (item.get("open") or "").strip() for name, item in values.items()}
        for beat in beats_of(run, scene):
            charges = charges_of(run, beat)
            if is_turn_beat(beat) and charges:
                changed, reached = [], []
                for name, charge in charges.items():
                    before = current.get(name)
                    if before in CHARGE_SIGNS and charge in CHARGE_SIGNS and \
                            CHARGE_SIGNS[before] != CHARGE_SIGNS[charge]:
                        changed.append(f"{name} {before} to {charge}")
                    close = (values[name].get("close") or "").strip() if name in values else None
                    if close and charge == close and before != close:
                        reached.append(f"{name} reaches its close {close}")
                if not changed and not reached:
                    before_words = ", ".join(f"{name} {current.get(name) or '?'} to {charge}"
                                             for name, charge in charges.items())
                    problems.append(problem_at(
                        run, "E", "CRAFT-18", beat, "charge",
                        f"the {turn_of(beat).replace('_', ' ')} changes no value's sign and reaches no value's close "
                        f"({before_words})",
                        "Fix: show the change of charge this turn makes (a sign change or a value reaching its "
                        "close), or set turn: none (McKee's sign test, A2)."))
            for name, charge in charges.items():
                current[name] = charge
    return problems


def beat_signals(run, scene, beat, previous_dial, dial, views):
    """{signal: evidence} of the signals that change on a beat: size, light, sound, camera move and colour."""
    signals = {}
    item = dial.get(beat.identifier)
    previous_item = dial.get(previous_dial) if previous_dial else None
    if item is not None and previous_item is not None:
        size, before = word_of(item.get("size")), word_of(previous_item.get("size"))
        if size and before and size != before:
            signals["size"] = f"{size_words(before)} to {size_words(size)}"
    lines = beat_lines(run, beat)
    if item is not None:
        light, sound = item.get("light"), item.get("sound")
        # one change counts once: a light change that names a colour is the light's change, not light and colour
        if light and not is_empty(light) and word_of(light) != "as_look" and \
                not reason_quotes_lines(run, light, lines, "light"):
            signals["colour" if COLOUR_WORDS.search(light) and "light" in signals else "light"] = f"dial light {light}"
        if sound and not is_empty(sound) and word_of(sound) != "room_sound" and \
                not reason_quotes_lines(run, sound, lines, "sound") and not rupture_planned(run, scene, beat, lines):
            signals["sound"] = f"dial sound {sound}"
    for view in views:
        # a shot's own changes count on the beat it starts on, so a shot over two beats is not counted twice
        if not view.written or view.is_card or (view.beats and view.beats[0] != beat.identifier):
            continue
        shot = view.record
        for field_name, what in shot_light_sound_changes(run, shot, beat):
            key = "light" if field_name in ("light", "light_cue") else "sound"
            if key == "light" and "light" in signals and COLOUR_WORDS.search(what):
                key = "colour"  # a second, coloured light change; one change never counts as both
            signals.setdefault(key, f"{shot.identifier} {what}")
        move = word_of(shot.get("move"))
        if move and move != "static":
            signals.setdefault("camera move", f"{shot.identifier} move {move}")
    for pause in items(run, beat, "pause_after"):
        if word_of(pause.get("picture")) == "push_in":
            signals.setdefault("camera move", f"{beat.identifier} pause push_in")
    return signals


DEPARTMENT_SYNONYMS = {"lighting": "light", "blocking": "staging", "art": "design", "set": "design"}
# Staging named in a scene idea in any form of stand or move, or by a MOVE ID (the second full run: only the fixed
# words "stands" and "moves" counted).
STAGING_IN_IDEA = re.compile(r"(?<![a-z])(?:stand|stands|standing|stood|move|moves|moving|moved|movement)(?![a-z])|"
                             r"(?<![A-Za-z0-9])SC\d{2,3}[A-Z]?-M\d{2}(?![0-9])", re.IGNORECASE)


@register_check("CRAFT-19", level="W", build=1,
                title="Stacking: more than two of size, light, sound, camera move and colour change on the same beat; "
                      "more than two departments change at the main turn, or scene_idea does not name them",
                plain="changes too many things at once on one beat, so none of them reads")
def check_craft_19(run):
    problems = []
    rule = constant_of(run, "signals_changing_per_beat_max", {"max": 2}) or {}
    most = int(rule.get("max", 2)) if isinstance(rule, dict) else int(rule)
    most_departments = int(constant_of(run, "departments_changing_at_main_turn_max", 2))
    for scene in scene_identifiers(run):
        dial = dial_items(run, scene)
        previous = None
        record = scene_record(run, scene)
        for beat in beats_of(run, scene):
            views = shots_on_beat(run, scene, beat.identifier)
            signals = beat_signals(run, scene, beat, previous, dial, views)
            previous = beat.identifier if beat.identifier in dial else previous
            if len(signals) > most:
                evidence = "; ".join(f"{name}: {what}" for name, what in signals.items())
                target = record if record is not None else beat
                problems.append(problem_at(
                    run, "W", "CRAFT-19", target, "dial" if record is not None else None,
                    f"{beat.identifier} changes {len(signals)} of size, light, sound, camera move and colour at once "
                    f"({evidence}); the most is {most}",
                    "Fix: keep the one or two changes the beat needs and hold the rest (B3 R7).",
                    containing=beat.identifier))
        main = main_turn_of(run, scene)
        if record is None or main is None:
            continue
        changing = []
        for item in items(run, record, "department_idea"):
            department = word_of(item.first)
            department = DEPARTMENT_SYNONYMS.get(department, department)
            holds = word_of(item.get("holds_baseline"))
            if holds == "yes" or item.first is None:
                continue
            because = [piece.strip() for piece in split_list(item.get("because") or "")]
            if main.identifier in because and department not in changing:
                changing.append(department)
        if len(changing) > most_departments:
            problems.append(problem_at(
                run, "W", "CRAFT-19", record, "department_idea",
                f"{len(changing)} departments change at the main turn {main.identifier} ({', '.join(changing)}); the "
                f"most is {most_departments}",
                "Fix: let at most two departments change at the main turn and hold the others at their baseline "
                "(B3 R7, B1 P11)."))
        idea = record.get("scene_idea")
        if changing and not idea:
            problems.append(problem_at(
                run, "W", "CRAFT-19", record, "department_idea",
                f"the departments that change at the main turn ({', '.join(changing)}) are named in no scene_idea",
                "Fix: write scene_idea, naming the departments that change at the main turn."))
        elif changing:
            lowered = (idea or "").lower()
            missing = [department for department in changing
                       if not any(re.search(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", lowered)
                                  for word in DEPARTMENT_WORDS.get(department, (department,)))
                       and not (department == "staging" and STAGING_IN_IDEA.search(idea or ""))]
            if missing:
                problems.append(problem_at(
                    run, "W", "CRAFT-19", record, "scene_idea",
                    f"does not name {' or '.join(missing)}, which {'changes' if len(missing) == 1 else 'change'} at "
                    f"the main turn {main.identifier}",
                    "Fix: name in scene_idea every department that changes at the main turn."))
    return problems


LINEUP_COLUMNS = ("height", "mass", "shape", "value", "colour", "tempo")


def lineup_of(run, character):
    value = character.get("lineup")
    if not value or is_empty(value):
        return None
    parts = named_parts(value)
    return {key: word_of(parts[key]) for key in LINEUP_COLUMNS if parts.get(key)}


@register_check("CRAFT-20", level="W", build=1, title="Two principals share four or more lineup columns (B5 R3)",
                plain="makes two main characters look too much alike to tell apart at a glance")
def check_craft_20(run):
    problems = []
    differ = int(constant_of(run, "lineup_columns_differ_min", 3))
    share_limit = len(LINEUP_COLUMNS) - differ + 1
    # file order: the character written second is the one reported
    principals = [record for record in run.records("CHARACTER") if word_of(record.get("tier")) == "principal"]
    lineups = [(record, lineup_of(run, record)) for record in principals]
    lineups = [(record, lineup) for record, lineup in lineups if lineup]
    for index, (first, first_lineup) in enumerate(lineups):
        for second, second_lineup in lineups[index + 1:]:
            shared = [key for key in LINEUP_COLUMNS
                      if first_lineup.get(key) and first_lineup.get(key) == second_lineup.get(key)]
            if len(shared) >= share_limit:
                problems.append(problem_at(
                    run, "W", "CRAFT-20", second, "lineup",
                    f"shares {len(shared)} of the {len(LINEUP_COLUMNS)} lineup columns with {first.identifier} "
                    f"({', '.join(shared)}); principals differ in at least {differ}",
                    "Fix: change the columns that matter most for this character (height, mass, shape, value), so "
                    "the two read apart at a glance (B5 R3)."))
    return problems


def flagged_speeches(run, scene, flag):
    """[(beat, speech ID or None)] for every BEAT flag of a kind (melodrama, monologue); None when the flag names no
    line."""
    found = []
    for beat in beats_of(run, scene):
        for item in items(run, beat, "flag"):
            if word_of(item.first) == flag:
                found.append((beat, (item.get("line") or "").strip() or None))
    return found


def median_rank(views):
    ranks = sorted(size_rank(view.size) for view in views if view.is_live and size_rank(view.size) is not None)
    if not ranks:
        return None
    middle = len(ranks) // 2
    return ranks[middle] if len(ranks) % 2 else (ranks[middle - 1] + ranks[middle]) / 2


@register_check("CRAFT-21", level="W", build=1,
                title="A shot that hears a line flagged melodrama is tighter than the scene's median size, moves, or "
                      "has music (A1 R36)",
                plain="pushes a line the story flags as over-played with a close frame, a camera move or music")
def check_craft_21(run):
    problems = []
    for scene in scene_identifiers(run):
        flags = flagged_speeches(run, scene, "melodrama")
        if not flags:
            continue
        median = median_rank(shot_views(run, scene))
        for shot in shots_of(run, scene):
            heard = [item.first.strip() for item in items(run, shot, "hear") if item.first]
            beats = id_list(shot, "beats")
            hits = [speech for beat, speech in flags if (speech and speech in heard) or
                    (speech is None and beat.identifier in beats and heard)]
            if not hits:
                continue
            reasons = []
            rank = size_rank(shot.get("size"))
            if median is not None and rank is not None and rank > median:
                reasons.append(f"size {shot.get('size')} is tighter than the scene's median")
            move = word_of(shot.get("move"))
            if move and move != "static":
                reasons.append(f"move {move}")
            if shot.get("music") and not is_empty(shot.get("music")):
                reasons.append(f"music {shot.get('music')}")
            if reasons:
                problems.append(problem_at(
                    run, "W", "CRAFT-21", shot, "size" if reasons[0].startswith("size") else
                    ("move" if reasons[0].startswith("move") else "music"),
                    f"hears {names_list([speech for speech in hits if speech]) or 'a line'} flagged melodrama, and "
                    f"{'; '.join(reasons)}",
                    "Fix: play the flagged line plainly: the scene's median size or wider, a static camera, no music "
                    "(A1 R36)."))
    return problems


def speaker_of(run, speech_identifier):
    if not speech_identifier:
        return None
    entry = run.speeches.get(speech_identifier)
    if entry and entry.get("speaker"):
        return element_of(entry.get("speaker"))
    record = run.record(speech_identifier)
    if record is not None and record.get("speaker"):
        return element_of(record.get("speaker").strip())
    breakdown = breakdown_of(run)
    found = breakdown.speech(speech_identifier)
    return element_of(found.get("speaker")) if found and found.get("speaker") else None


@register_check("CRAFT-22", level="W", build=1,
                title="A beat flagged monologue has no listener in frame and no listener shot (A1 R31)",
                plain="plays a long speech with no one listening in the picture")
def check_craft_22(run):
    problems = []
    for scene in scene_identifiers(run):
        for beat, speech in flagged_speeches(run, scene, "monologue"):
            speaker = speaker_of(run, speech)
            if speaker is None:
                actions = items(run, beat, "action")
                speaker = element_of(actions[0].first.strip()) if actions and actions[0].first else None
            views = shots_on_beat(run, scene, beat.identifier)
            if not views:
                continue
            listeners = sorted({subject for view in views for subject in view.subjects
                                if subject.startswith("CH-") and subject != speaker})
            if listeners:
                continue
            problems.append(problem_at(
                run, "W", "CRAFT-22", beat, "flag",
                f"the monologue{f' ({speech})' if speech else ''} has no listener in frame in any of its shots "
                f"({names_list([view.identifier for view in views])})",
                "Fix: put the listener in frame, or give the beat a listener shot, so the speech lands on someone "
                "(A1 R31)."))
    return problems


def speakers_in_scene(run, scene):
    record = scene_record(run, scene)
    speakers = set()
    if record is not None:
        for item in items(run, record, "speaking"):
            if item.first and (number_of(item.get("cues")) or 0) > 0:
                speakers.add(element_of(item.first.strip()))
    if len(speakers) < 2:
        for shot in shots_of(run, scene):
            for item in items(run, shot, "hear"):
                speaker = speaker_of(run, item.first.strip()) if item.first else None
                if speaker:
                    speakers.add(speaker)
    return speakers


@register_check("CRAFT-23", level="W", build=1,
                title="A dialogue scene with no hear item whose speaker is off screen (A1 R2)",
                plain="never lets a line land on the listener: every line is heard only on the speaker's face")
def check_craft_23(run):
    problems = []
    for scene in scene_identifiers(run):
        shots = shots_of(run, scene)
        heard = [item for shot in shots for item in items(run, shot, "hear") if item.first]
        if not heard or len(speakers_in_scene(run, scene)) < 2:
            continue
        if any(word_of(item.get("speaker")) in ("off_screen", "hidden") for item in heard):
            continue
        record = scene_record(run, scene)
        speakers = speakers_in_scene(run, scene)
        problems.append(problem_at(
            run, "W", "CRAFT-23", record if record is not None else shots[0],
            "speaking" if record is not None else "hear",
            f"makes it a dialogue scene ({len(speakers)} speakers), and none of its {len(heard)} heard speeches is "
            "heard off screen",
            "Fix: land at least one line on the listener (speaker: off_screen), where the reaction is the story "
            "(A1 R1, A1 R2)."))
    return problems


@register_check("CRAFT-24", level="W", build=1,
                title="A turn beat whose silent_third appears in no shot of that beat (A1 R5)",
                plain="leaves the silent witness of a turn out of every shot of that turn")
def check_craft_24(run):
    problems = []
    for scene in scene_identifiers(run):
        for beat in beats_of(run, scene):
            third = beat.get("silent_third")
            if not is_turn_beat(beat) or not third:
                continue
            views = shots_on_beat(run, scene, beat.identifier)
            if not views:
                continue
            if is_empty(third):
                # "none" is for a turn where nobody is left to witness (the second full run); three people in the
                # turn's shots mean someone is (its cross-examination)
                people = sorted({subject for view in views for subject in view.subjects if subject.startswith("CH-")})
                if len(people) >= 3:
                    problems.append(problem_at(
                        run, "W", "CRAFT-24", beat, "silent_third",
                        f"is none, but {len(people)} people are in this turn's shots ({names_list(people)})",
                        "Fix: name the one who watches without speaking as silent_third; none is only for a turn "
                        "with nobody left to witness."))
                continue
            third = element_of(third.strip())
            seen = any(third in view.subjects or (view.written and third in {
                element_of(reference) for reference in id_list(view.record, "must_show")}) for view in views)
            if not seen:
                problems.append(problem_at(
                    run, "W", "CRAFT-24", beat, "silent_third",
                    f"{third} appears in no shot of this turn ({names_list([view.identifier for view in views])})",
                    "Fix: keep the silent third in frame at least once on the turn, in the background or the edge "
                    "(A1 R5)."))
    return problems


def at_or_tighter(size, limit):
    rank, limit_rank = size_rank(size), size_rank(limit)
    return rank is not None and limit_rank is not None and rank >= limit_rank


@register_check("CRAFT-25", level="W", build=1, title="display: 3 at close-up or tighter without a why (D15)",
                plain="shows a face fully open in a close frame without a reason")
def check_craft_25(run):
    problems = []
    limit = constant_of(run, "display_3_needs_why_at_or_tighter", "close_up")
    for shot in records_of(run, "SHOT"):
        if not at_or_tighter(shot.get("size"), limit) or shot.get("why"):
            continue
        for item in items(run, shot, "subject"):
            if whole_number(item.get("display"), None) == 3:
                problems.append(problem_at(
                    run, "W", "CRAFT-25", shot, "subject",
                    f"{item.first.strip()} has display 3 at {shot.get('size')} with no why",
                    "Fix: lower display to 1 or 2, or write a why quoting the line that opens the face (D15).",
                    containing=item.first.strip()))
    return problems


def moment_seconds(item):
    span = (item.first or "").strip()
    match = re.match(r"^(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)$", span)
    if not match:
        return None
    return float(match.group(2)) - float(match.group(1))


def moment_span(item):
    """(start, end) seconds of a moment item ('8-15'), or None."""
    match = re.match(r"^(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)$", (item.first or "").strip())
    return (float(match.group(1)), float(match.group(2))) if match else None


def without_quotes(text):
    """A text with its quoted parts (story lines, printed words) blanked out, so their words are never judged."""
    return QUOTED.sub(" ", (text or "").replace("’", "'"))


def word_pattern(word):
    """A pattern that finds a word or phrase as whole words, in any case."""
    return re.compile(r"(?<![A-Za-z'-])" + re.escape(word) + r"(?![A-Za-z'-])", re.I)


def stillness_lists(run):
    """(words, phrases, not-an-action words) of rules/words.json's stillness_words."""
    entry = run.words.get("stillness_words") or {}
    return (list(entry.get("words") or []), list(entry.get("phrases") or []),
            list(entry.get("not_an_action") or []))


# "still" that means "even now" ("still refusing", "still talking") asks for no stillness, so it is not counted
# when the next word is an -ing word (Project notes 43: narrow triggers).
STILL_AS_EVEN_NOW = re.compile(r"\bstill\s+[a-z]+ing\b", re.I)


def stillness_in(run, text):
    """The stillness words and phrases of rules/words.json in a text, outside quotation marks, in the order of
    the lists; a word inside a phrase found is reported as the phrase only."""
    words, phrases, _ = stillness_lists(run)
    plain = without_quotes(text)
    found = [phrase for phrase in phrases if word_pattern(phrase).search(plain)]
    for word in words:
        for match in word_pattern(word).finditer(plain):
            if word.lower() == "still" and STILL_AS_EVEN_NOW.match(plain, match.start()):
                continue
            if any(word_pattern(word).search(phrase) for phrase in found):
                break
            found.append(word)
            break
    return found


def action_clauses(run, text):
    """The clauses of a moment's shows (split at ';' and at 'then') that are actions: those holding no stillness
    word or phrase and no not_an_action word (stays, waits, listens ...) of rules/words.json."""
    _, _, not_actions = stillness_lists(run)
    clauses = [piece.strip(" ,.:") for piece in re.split(r";|\bthen\b", text or "")]
    found = []
    for clause in clauses:
        if not clause:
            continue
        plain = without_quotes(clause)
        if stillness_in(run, clause) or any(word_pattern(word).search(plain) for word in not_actions):
            continue
        found.append(clause)
    return found


def people_in(run, shot):
    return [item for item in items(run, shot, "subject")
            if item.first and element_of(item.first.strip()).startswith("CH-")]


def held_pause_seconds(run, shot):
    """The longest pause held on picture (BEAT pause_after with picture: hold) that this shot carries: the pause
    of a beat whose last shot is this one, read from its seconds, else from the low end of its tier."""
    breakdown = breakdown_of(run)
    longest = None
    tiers = constant_of(run, "pause_tiers", {}) or {}
    for beat_identifier in id_list(shot, "beats"):
        beat = run.record(beat_identifier)
        if beat is None or beat.type_name != "BEAT":
            continue
        if last_shot_naming_beat(breakdown, beat_identifier) not in (None, shot.identifier):
            continue
        for item in items(run, beat, "pause_after"):
            if word_of(item.get("picture")) != "hold":
                continue
            seconds = number_of(item.get("seconds"))
            if seconds is None:
                tier = tiers.get(word_of(item.first)) if isinstance(tiers, dict) else None
                seconds = (tier or {}).get("from_s", 0.0) if isinstance(tier, dict) else 0.0
            longest = seconds if longest is None else max(longest, seconds)
    return longest


SMALL_ACTIONS_FIX = ("Fix: write small timed actions instead (a breath, a blink, a swallow, a glance, a hand that "
                     "adjusts something), about one every {every:g} s, never a list of parts that stay still (D15 R6; "
                     "a judgement from testers' notes, Project notes 42).")


@register_check("CRAFT-26", level="W", build=1,
                title="A held moment (hold_action_every_s or more, or a pause held on picture) with fewer than one "
                      "small timed action every hold_action_every_s (D15 R6, rewritten; J: testers' notes, Project "
                      "notes 42 and 43)",
                plain="holds on a person with too little happening, so a video model may freeze the picture or "
                      "squeeze the time out")
def check_craft_26(run):
    problems = []
    every = float(constant_of(run, "hold_action_every_s", 2.0) or 2.0)
    fix = SMALL_ACTIONS_FIX.format(every=every)
    for shot in records_of(run, "SHOT"):
        if not people_in(run, shot):
            continue
        moments = items(run, shot, "moment")
        for item in moments:
            seconds = moment_seconds(item)
            if seconds is None or seconds + 1e-9 < every:
                continue
            needed = int(math.floor(seconds / every + 1e-9))
            found = action_clauses(run, item.get("shows") or "")
            if len(found) < needed:
                span = (item.first or "").strip()
                problems.append(problem_at(
                    run, "W", "CRAFT-26", shot, "moment",
                    f"the moment {span} holds {seconds:g} s with {len(found)} small "
                    f"{'action' if len(found) == 1 else 'actions'}; it needs at least {needed}, one every {every:g} s",
                    fix, containing=span))
        pause = held_pause_seconds(run, shot)
        if pause is None:
            continue
        needed = max(1, int(math.floor(pause / every + 1e-9)))
        screen_time = number_of(shot.get("screen_time"))
        tail = [item for item in moments if moment_span(item) and (
            screen_time is None or moment_span(item)[1] >= screen_time - pause - 1e-9)]
        found = sum(len(action_clauses(run, item.get("shows") or "")) for item in tail)
        if found < needed:
            last = (moments[-1].first or "").strip() if moments else None
            problems.append(problem_at(
                run, "W", "CRAFT-26", shot, "moment" if moments else "beats",
                f"the shot holds a pause of {pause:g} s on picture with {found} small "
                f"{'action' if found == 1 else 'actions'} in its last moments; it needs at least {needed}",
                fix, containing=last))
    return problems


@register_check("CRAFT-27", level="W", build=1,
                title="A stillness word or phrase (stillness_words) in a moment's shows, a subject's does, or a "
                      "shot's start or end (J: testers' notes, Project notes 42 and 43)",
                plain="asks a person or a thing to stay still, which a video model reads as an order to freeze")
def check_craft_27(run):
    problems = []
    # energy: still is a value, not text, so it is never read here (Project notes 43).
    fix = ("Fix: write what happens instead, as small timed actions (a breath, a blink, a swallow, a glance, a hand "
           "that adjusts something) (D15 R6; a judgement from testers' notes, Project notes 42).")
    for shot in records_of(run, "SHOT"):
        places = [("moment", item.first, item.get("shows")) for item in items(run, shot, "moment")]
        places += [("subject", item.first, item.get("does")) for item in items(run, shot, "subject")]
        places += [(name, None, shot.get(name)) for name in ("start", "end")]
        for field_name, first, text in places:
            found = stillness_in(run, text or "")
            if not found:
                continue
            where = {"moment": f"the moment {(first or '').strip()}", "subject": f"{(first or '').strip()}'s does",
                     "start": "the start", "end": "the end"}[field_name]
            problems.append(problem_at(
                run, "W", "CRAFT-27", shot, field_name,
                f"{', '.join(quote_for_message(word) for word in found)} in {where} asks for stillness", fix,
                containing=(first or "").strip() or None))
    return problems


def contact_lists(run):
    entry = run.words.get("contact_words") or {}
    return list(entry.get("cause") or []), list(entry.get("effect") or [])


def phrase_positions(plain, phrases):
    """[(position, phrase)] of every phrase found in a text as whole words and not negated just before it."""
    found = []
    for phrase in phrases:
        for match in word_pattern(phrase).finditer(plain):
            if NEGATION_BEFORE.search(plain[:match.start()]):
                continue
            found.append((match.start(), phrase))
    return sorted(found)


@register_check("CRAFT-28", level="W", build=1,
                title="A shot whose moments, in order, hold a contact_words cause and then its effect: a contact "
                      "shown on screen (J: testers' notes, Project notes 42 W9)",
                plain="shows one thing hitting another and the result in the same shot, which video models cannot "
                      "do; cut at the moment of contact")
def check_craft_28(run):
    problems = []
    causes, effects = contact_lists(run)
    fix = ("Fix: end the shot at the contact and open the next shot on the result already there, in a clearly "
           "different size or angle, with the sound of the hit on the cut (a judgement from testers' notes: video "
           "models cannot make one thing break or push another at the moment of contact; Project notes 42).")
    for shot in records_of(run, "SHOT"):
        moments = items(run, shot, "moment")
        timed = sorted(moments, key=lambda item: (moment_span(item) or (0.0, 0.0)))
        texts = [("moment", item.first, without_quotes(item.get("shows"))) for item in timed]
        texts += [("subject", item.first, without_quotes(item.get("does"))) for item in items(run, shot, "subject")]
        for index, (field_name, first, plain) in enumerate(texts):
            hit = None
            for position, cause in phrase_positions(plain, causes):
                later = [(field_name, first, effect) for spot, effect in phrase_positions(plain, effects)
                         if spot > position]
                if not later and field_name == "moment" and index + 1 < len(texts) and texts[index + 1][0] == "moment":
                    following = texts[index + 1]
                    later = [(following[0], following[1], effect)
                             for _, effect in phrase_positions(following[2], effects)]
                if later:
                    hit = (cause, later[0])
                    break
            if hit is None:
                continue
            cause, (where_field, where_first, effect) = hit
            problems.append(problem_at(
                run, "W", "CRAFT-28", shot, where_field,
                f"{quote_for_message(cause)} and then {quote_for_message(effect)} in one shot show a contact and its "
                f"result on screen", fix, containing=(where_first or "").strip() or None))
            break
    return problems


# ---------------------------------------------------------------- INFO

def fact_reveal(run, fact):
    """(scene, beat ID or None, quote, line or None) of a FACT's audience_knows_from story point: the beat code
    stored with it (' = SC10-B04'), else the beat it resolves to in the story given."""
    value = (fact.get("audience_knows_from") or "").strip()
    if not value or is_empty(value):
        return None
    parsed = parse_story_point(value)
    if not parsed:
        scene = scene_of(value)
        return (scene, None, None, None) if scene else None
    scene, quote, beat = parsed
    line = None
    if run.story is not None:
        from .derive_fields import resolve_story_point
        resolved = resolve_story_point(breakdown_of(run), value, fact, "audience_knows_from")
        line = resolved.line
        beat = beat or resolved.beat
    return scene, beat, quote, line


# The ways keep_hidden hides a fact's element from sight (SHOT keep_hidden how); an item without a how is read as
# hidden too, since keep_hidden means "stays out of view".
HIDDEN_FROM_SIGHT = ("frame_edge", "focus", "dark", "obstruction", "timing", "sound_first", "off_frame", "")


@register_check("INFO-01", level="W", build=1,
                title="A shot before a FACT's reveal whose subject, thing or must_show includes the fact's element "
                      "(A4 S1-S3)",
                plain="shows the thing that gives a secret away before the story reveals it")
def check_info_01(run):
    problems = []
    for fact in records_of(run, "FACT"):
        reveal = fact_reveal(run, fact)
        elements = [element_of(piece) for piece in id_list(fact, "element")]
        if reveal is None or not elements:
            continue
        reveal_scene, reveal_beat = reveal[0], reveal[1]
        for scene in scene_identifiers(run):
            if sort_key_for_identifier(scene) > sort_key_for_identifier(reveal_scene):
                continue
            positions = beat_positions(run, scene)
            same = same_scene(scene, reveal_scene)
            if same and (reveal_beat is None or reveal_beat not in positions):
                continue
            for shot in shots_of(run, scene):
                if same:
                    view = next(view for view in shot_views(run, scene) if view.identifier == shot.identifier)
                    last = last_beat_position(view, positions)
                    if last is None or last >= positions[reveal_beat]:
                        continue
                hidden_facts = {item.first.strip() for item in items(run, shot, "keep_hidden")
                                if item.first and normalise_word(item.get("how") or "") in HIDDEN_FROM_SIGHT}
                # C12 and the full run (Project notes 31, problem 11): a shot that says how it keeps this fact
                # hidden (heard first, at the frame's edge, out of focus, in the dark, behind something, or timed
                # out of view) is not warned, whatever it lists as seen: the thing stays in must_show when it is
                # really on screen, and the review questions judge whether the hiding works
                if fact.identifier in hidden_facts:
                    continue
                present = {}
                for item in items(run, shot, "subject"):
                    if item.first:
                        present.setdefault(element_of(item.first.strip()), "subject")
                for item in thing_items(run, shot):
                    present.setdefault(element_of(item.first.strip()), "thing")
                for reference in id_list(shot, "must_show"):
                    present.setdefault(element_of(reference), "must_show")
                for element in elements:
                    where = present.get(element)
                    if where is None:
                        # a thing that carries the secret's motif shows it; a motif named in the shot is not
                        # read as every thing that carries it (the labels motif is not the sleeve container)
                        for other, other_where in present.items():
                            if prop_motif(run, other) == element:
                                where = other_where
                                break
                    if where is None:
                        continue
                    problems.append(problem_at(
                        run, "W", "INFO-01", shot, where,
                        f"shows {element}, the element of {fact.identifier}, before its reveal at "
                        f"{reveal_beat or reveal_scene}",
                        f"Fix: keep {element} out of frame until {reveal_beat or reveal_scene} (keep_hidden: "
                        f"{fact.identifier} | how: frame_edge, focus, dark, obstruction, timing or sound_first) "
                        "(A4 S1-S3).", containing=element))
                    break
    return problems


def reveal_shot(run, fact, reveal):
    """The shot where the audience learns a fact: the shot of the reveal beat whose lines hold the reveal's quote;
    else the first shot of that beat that shows the fact's element; else the beat's first shot."""
    scene, beat, _, line = reveal
    if beat is None:
        return None
    views = shots_on_beat(run, scene, beat)
    if not views:
        return None
    if line is not None:
        breakdown = breakdown_of(run)
        for view in views:
            if view.written and line in breakdown.lines_of(view.record):
                return view
    elements = [element_of(piece) for piece in id_list(fact, "element")]
    for view in views:
        if view.written and any(element_matches(run, element, set(elements_in_frame(run, view.record)))
                                for element in elements):
            return view
    return views[0]


@register_check("INFO-02", level="W", build=1, title="A FACT's reveal shot whose role is neither turn nor must_keep",
                plain="reveals a secret in a shot the scene does not treat as one it depends on")
def check_info_02(run):
    problems = []
    for fact in records_of(run, "FACT"):
        reveal = fact_reveal(run, fact)
        if reveal is None:
            continue
        view = reveal_shot(run, fact, reveal)
        if view is None or view.role in ("turn", "must_keep"):
            continue
        problems.append(problem_at(
            run, "W", "INFO-02", view.problem_record, "role",
            f"{view.role} is the role of {fact.identifier}'s reveal shot (at {reveal[1]})",
            "Fix: make the reveal shot must_keep (or the turn shot, if the reveal is the turn) (A4 S1-S3)."))
    return problems


# ---------------------------------------------------------------- REASON

def because_items(shot):
    value = shot.get("because") or ""
    return [piece.strip() for piece in split_list(value) if piece.strip()]


def because_identifiers(shot):
    return [piece for piece in because_items(shot)
            if not piece.lower().startswith("line") and normalise_word(piece) != "default"]


def departures(run, shot):
    """[(field, value, default)] of the values on 5.4 rule 11's list that leave their default (REASON-02)."""
    found = []
    card = word_of(shot.get("kind")) in ("card", "black")
    scene = scene_record(run, scene_of(shot.identifier))
    camsys = run.record("CAMSYS")
    if not card:
        angle = word_of(shot.get("angle"))
        if angle and angle != "eye_level":
            found.append(("angle", angle, "eye_level"))
        height = (shot.get("height") or "").strip()
        if height and not is_empty(height):
            people = set(subject_elements_of_shot(run, shot))
            if shot.get("focus_on") and not is_empty(shot.get("focus_on")):
                people.add(element_of(shot.get("focus_on").strip()))
            whose = scene.get("whose_scene") if scene is not None else None
            if whose and not is_empty(whose):
                people.add(element_of(whose.strip()))
            match = re.match(r"^(eye|seated|kneeling)\s*:\s*(\S+)$", height)
            if not match or element_of(match.group(2)) not in people:
                default = f"eye:{element_of(whose.strip())}" if whose and not is_empty(whose) else "the subject's eye"
                found.append(("height", height, default))
        lens = number_of(shot.get("lens_mm"))
        normal = number_of(camsys.get("normal_lens_mm")) if camsys is not None else None
        if lens is not None and normal is not None and lens != normal:
            found.append(("lens_mm", f"{lens:g}", f"{normal:g}"))
        move = word_of(shot.get("move"))
        if move and move != "static":
            found.append(("move", move, "static"))
        focus = word_of(shot.get("focus"))
        if focus and focus != "moderate":
            found.append(("focus", focus, "moderate"))
        light = shot.get("light")
        if light and not is_empty(light) and word_of(light) != "as_look":
            found.append(("light", light, "as_look"))
        room_sound = shot.get("room_sound")
        if room_sound and not is_empty(room_sound) and word_of(room_sound) != "as_place":
            found.append(("room_sound", room_sound, "as_place"))
    silence = word_of(shot.get("silence"))
    if silence and silence != "none":
        found.append(("silence", silence, "none"))
    music = shot.get("music")
    if music and not is_empty(music):
        found.append(("music", music, "none"))
    if at_or_tighter(shot.get("size"), "close_up"):
        for item in items(run, shot, "subject"):
            display = whole_number(item.get("display"), None)
            if display is not None and display != 1:
                found.append(("display", f"{display:g}", "1 in a close-up or tighter"))
                break
    return found


@register_check("REASON-01", level="E", build=1,
                title="Purpose missing, or because without a resolvable story ID",
                plain="does not say what the shot is for, or which part of the story it serves")
def check_reason_01(run):
    problems = []
    for shot in records_of(run, "SHOT"):
        purpose = shot.get("purpose")
        if not purpose or is_empty(purpose):
            problems.append(problem_at(
                run, "E", "REASON-01", shot, "purpose", "is missing",
                "Fix: write one sentence saying what the audience must get from this shot."))
        pieces = because_items(shot)
        if not pieces:
            problems.append(run.problem(
                "E", "REASON-01", shot, "because", "is missing",
                "Fix: cite the story records that justify the shot, at least its beat (5.4 rule 3)."))
            continue
        identifiers = because_identifiers(shot)
        if any(identifier_counts(run, identifier) for identifier in identifiers):
            continue
        if any(normalise_word(piece) == "default" for piece in pieces) and not departures(run, shot) and \
                word_of(shot.get("role")) != "turn":
            continue
        if identifiers:
            what = f"cites no story ID that exists ({names_list(identifiers)})"
        elif any(normalise_word(piece) == "default" for piece in pieces):
            what = "is default, but the shot leaves its defaults" + (" (a turn shot)" if word_of(
                shot.get("role")) == "turn" else "")
        else:
            what = "cites only story lines and no story ID"
        problems.append(problem_at(
            run, "E", "REASON-01", shot, "because", what,
            "Fix: cite the records that justify the shot: its beat, and the value, motif, plant, fact, character, "
            "camera rule, saved choice or look it serves (5.4 rule 3)."))
    return problems


@register_check("REASON-02", level="E", build=1,
                title="A field on the list in 5.4 rule 11 that differs from its default, or a departure from the camera "
                      "system, without why; a turn shot without why",
                plain="leaves the film's baseline (angle, height, lens, move, focus, light or sound) without saying why")
def check_reason_02(run):
    problems = []
    for shot in records_of(run, "SHOT"):
        if shot.get("why") and not is_empty(shot.get("why")):
            continue
        found = departures(run, shot)
        turn = word_of(shot.get("role")) == "turn"
        if not found and not turn:
            continue
        parts = [f"{field_name} {value} (default {default})" for field_name, value, default in found]
        if turn:
            parts.insert(0, "the shot is a turn shot")
        problems.append(run.problem(
            "E", "REASON-02", shot, "why", f"is missing, and {'; '.join(parts)}",
            "Fix: write a why that quotes a line, names an object or action, or cites an ID for each departure, or "
            "go back to the default (5.4 rule 11)."))
    return problems


def reason_texts(run, field_filter=None):
    """[(record, field label, text, scene or None, field line)] of every reason written in the records: every field
    named why, every sub-part why, SCENE department_idea idea and scene_idea (worked out once per run)."""
    key = "craft_reason_texts"
    if key not in run.cache:
        run.cache[key] = all_reason_texts(run)
    found = run.cache[key]
    if field_filter:
        found = [entry for entry in found if field_filter(entry)]
    return found


def all_reason_texts(run):
    found = []
    for record_file in run.record_files:
        for record in record_file.records:
            if not record.known_type:
                continue
            merged = run.index.get(record.key)
            if merged is not None and run.is_omitted(merged):
                continue
            scene = scene_of(record.identifier) if record.identifier else None
            for line in record.fields:
                if not line.value or is_empty(line.value):
                    continue
                definition = run.schema.field(record.type_name, line.name) or {}
                if line.name == "why":
                    found.append((record, "why", line.value, scene, line))
                elif record.type_name == "SCENE" and line.name == "scene_idea":
                    found.append((record, "scene_idea", line.value, scene, line))
                elif ("why:" in line.value or "idea:" in line.value) and (
                        definition.get("kind") == "sub_parts" or definition.get("sub_parts")):
                    item = split_item(line.value, definition)
                    for key, value in item.parts:
                        if key == "why" or (record.type_name == "SCENE" and line.name == "department_idea"
                                            and key == "idea"):
                            if value and not is_empty(value):
                                found.append((record, f"{line.name} {key}", value, scene, line))
    return found


REASON_03_FIELDS = {("SHOT", "why"), ("SHOT", "light_cue why"), ("CUT", "why"), ("MOVE", "why"),
                    ("SCENE", "departure why")}


@register_check("REASON-03", level="E", build=1,
                title="why not anchored: no quote found in the scene's lines, no ID, no named element of the scene",
                plain="gives a reason that could belong to any film: it quotes nothing, cites nothing and names "
                      "nothing in this story")
def check_reason_03(run):
    problems = []
    seen = set()
    for record, label, text, scene, line in reason_texts(
            run, lambda entry: (entry[0].type_name, entry[1]) in REASON_03_FIELDS):
        key = (record.key, label, text)
        if key in seen:
            continue
        seen.add(key)
        anchor = reason_anchor(run, text, scene)
        if anchor.anchored:
            continue
        problems.append(run.problem(
            "E", "REASON-03", record, label,
            f"{quote_for_message(text)} is not anchored: it quotes no line of {scene or 'the story'}, cites no ID and "
            "names no element of the scene",
            "Fix: quote the line that justifies the choice, name the object or person it serves (a set plan's "
            "mark or object counts in plain words, not in capitals), or cite its ID; a line number alone does not "
            "anchor it (the any-film test: would this reason fit any film?).", line_number=line.line_number,
            file_name=record.file_name))
    return problems


@register_check("REASON-04", level="E", build=1,
                title="why contains a mood-only phrase from words.json",
                plain="gives a mood instead of a reason (to build tension, for drama, cinematic)")
def check_reason_04(run):
    problems = []
    seen = set()
    for record, label, text, scene, line in reason_texts(run):
        key = (record.key, label, text)
        if key in seen:
            continue
        seen.add(key)
        phrases = mood_phrases_in(run.words, text)
        if not phrases:
            feelings = mood_words_in(run.words, text) if record.type_name not in ("CHOICE", "SETVALUE") else []
            if feelings and not reason_anchor(run, text, scene if record.type_name in (
                    "SHOT", "CUT", "MOVE", "SCENE", "BEAT") else None).anchored:
                phrases = feelings
                what = (f"names only a feeling ({', '.join(quote_for_message(word) for word in feelings)}) and "
                        "nothing in this story")
            else:
                continue
        else:
            what = f"holds the mood-only {'phrase' if len(phrases) == 1 else 'phrases'} " + \
                   ", ".join(quote_for_message(phrase) for phrase in phrases)
        problems.append(run.problem(
            "E", "REASON-04", record, label, what,
            "Fix: replace the mood with the story reason: quote the line, name the object or action, or cite the ID "
            "the choice serves (B3 R23).", line_number=line.line_number, file_name=record.file_name))
    return problems


@register_check("REASON-05", level="E", build=1, title="A turn shot whose because cites no turn beat",
                plain="is the turn shot but does not name the turn it shows")
def check_reason_05(run):
    problems = []
    for shot in records_of(run, "SHOT"):
        if word_of(shot.get("role")) != "turn":
            continue
        turns = [identifier for identifier in because_identifiers(shot)
                 if run.record(identifier) is not None and run.record(identifier).type_name == "BEAT"
                 and is_turn_beat(run.record(identifier))]
        if turns:
            continue
        beats = [identifier for identifier in id_list(shot, "beats")
                 if run.record(identifier) is not None and is_turn_beat(run.record(identifier))]
        problems.append(problem_at(
            run, "E", "REASON-05", shot, "because",
            "cites no beat whose turn is not none", "Fix: add the turn beat this shot shows" +
            (f" ({names_list(beats)})" if beats else "") + " to because (5.4 rule 3)."))
    return problems


@register_check("REASON-06", level="E", build=1, title="A reserved choice used without its RC in because",
                plain="spends a saved choice without naming it")
def check_reason_06(run):
    problems = []
    for reserve in records_of(run, "RESERVE"):
        for shot in shots_using(run, reserve):
            if reserve.identifier in because_identifiers(shot):
                continue
            field_name, value = reserve_match(run, reserve)
            problems.append(problem_at(
                run, "E", "REASON-06", shot, "because",
                f"does not cite {reserve.identifier}, the saved choice the shot spends ({field_name} {value})",
                f"Fix: add {reserve.identifier} to because, or change {field_name}."))
    return problems


@register_check("REASON-07", level="E", build=1, title="A tool-forced departure without meaning_kept",
                plain="changes a planned choice to suit a tool without saying what meaning it keeps")
def check_reason_07(run):
    problems = []
    for shot in records_of(run, "SHOT"):
        for item in items(run, shot, "departure"):
            kept = item.get("meaning_kept")
            if kept and not is_empty(kept):
                continue
            problems.append(problem_at(
                run, "E", "REASON-07", shot, "departure",
                f"{(item.first or '').strip()} changes from {item.get('from') or '?'} to {item.get('to') or '?'} "
                f"({item.get('because') or 'feasibility'}) with no meaning_kept",
                "Fix: add | meaning_kept: what the change still shows, in one line.",
                containing=(item.first or "").strip() or None))
    return problems


def carrier_seen(run, carrier, views):
    """True when a carrier (an ID, or words) is seen or heard in the shots: things and where they are (at), subjects
    and what they do, moments, the end picture, effects and heard speeches."""
    identifiers = [match.group(1) for match in ID_TOKEN.finditer(carrier)]
    texts = []
    present = set()
    for view in views:
        shot = view.record
        for item in thing_items(run, shot):
            present.add(element_of(item.first.strip()))
            texts.append(item.get("at") or "")
        texts.append(shot.get("end") or "")
        for item in items(run, shot, "subject"):
            if item.first:
                present.add(element_of(item.first.strip()))
            texts.append(item.get("does") or "")
        for item in items(run, shot, "effect"):
            texts.append(item.first or "")
        for item in items(run, shot, "hear"):
            if item.first:
                present.add(item.first.strip())
        for item in items(run, shot, "moment"):
            texts.append(item.get("shows") or "")
    for identifier in identifiers:
        if identifier in present or element_matches(run, identifier, present):
            return True
        names = element_name_list(run, element_of(identifier))
        if any(named_element_in(text, names) for text in texts):
            return True
    if identifiers:
        return False
    words = set(content_words(carrier))
    joined = set(content_words(" ".join(texts)))
    return bool(words) and len(words & joined) >= max(1, round(0.5 * len(words)))


@register_check("REASON-08", level="E", build=1,
                title="An unsaid with no carrier seen or heard in any shot of its beat (things, does, sound)",
                plain="gives a character an unspoken thought that nothing in the shots lets us see or hear")
def check_reason_08(run):
    problems = []
    for scene in scene_identifiers(run):
        for beat in beats_of(run, scene):
            unsaid = items(run, beat, "unsaid")
            if not unsaid:
                continue
            views = shots_on_beat(run, scene, beat.identifier)
            if not views or any(not view.written for view in views):
                continue
            carrier = beat.get("carrier")
            if not carrier or is_empty(carrier):
                problems.append(problem_at(
                    run, "E", "REASON-08", beat, "unsaid",
                    f"{(unsaid[0].first or '').strip()}'s unsaid thought has no carrier",
                    "Fix: add a carrier: the thing, action or sound that makes the thought seen or heard."))
                continue
            if carrier_seen(run, carrier, views):
                continue
            problems.append(problem_at(
                run, "E", "REASON-08", beat, "carrier",
                f"{carrier} is seen or heard in no shot of this beat ({names_list([view.identifier for view in views])})",
                "Fix: put the carrier in a shot of the beat (a thing item, what a body does, or a sound), or choose a "
                "carrier the shots show."))
    return problems


@register_check("REASON-09", level="W", build=2,
                title="In a scene with whose_scene, a shot outside that character's place or knowledge without "
                      "pov_break (A3 rule 37)",
                plain="leaves the point of view the scene holds without saying why")
def check_reason_09(run):
    run.skip("REASON-09", "planned for the second build: leaving the whose-scene character's place or knowledge is "
                          "checked once the test runs show how scenes mark their point of view")
    return []


# ---------------------------------------------------------------- WORDS

# Emotion words that also name what a body visibly is ("his hurt arm", "her jaw tense", "tense shoulders"): next to a
# body part they describe the body, not a feeling, so WORDS-01 does not report them there (WP4d's note; D15 R1 asks
# for exactly such visible descriptions).
BODY_STATE_WORDS = ("hurt", "tense")
BODY_PARTS = ("arm", "arms", "hand", "hands", "shoulder", "shoulders", "leg", "legs", "foot", "feet", "knee", "knees",
              "back", "neck", "jaw", "jaws", "wrist", "wrists", "ankle", "ankles", "hip", "hips", "palm", "palms",
              "finger", "fingers", "fist", "fists", "head", "face", "mouth", "lips", "chest", "ribs", "body",
              "muscles", "brow", "side", "throat")
BODY_PART_PATTERN = "(?:" + "|".join(BODY_PARTS) + ")"


def names_a_body(word, lowered, position):
    """True when an emotion word that can describe a body stands next to a body part: 'hurt arm', 'the arm is
    hurt', 'jaw tense', 'shoulders go tense'."""
    if word not in BODY_STATE_WORDS:
        return False
    after = lowered[position + len(word):position + len(word) + 20]
    before = lowered[max(0, position - 30):position]
    return bool(re.match(r"\s+(?:left\s+|right\s+)?" + BODY_PART_PATTERN + r"\b", after)
                or re.search(r"\b" + BODY_PART_PATTERN + r"(?:\s+(?:is|are|go|goes|went|gone|stay|stays|still))?\s+$",
                             before))


def emotion_words_in(words, text):
    rule = (words or {}).get("emotion_adjectives", {})
    lowered = QUOTED.sub(" ", text or "").lower()
    found = []
    for word in rule.get("words", []):
        word = word.lower()
        for match in re.finditer(r"(?<![a-z-])" + re.escape(word) + r"(?![a-z-])", lowered):
            if not names_a_body(word, lowered, match.start()):
                found.append(word)
                break
    if re.search(r"\b(feels|feeling)\s+(like|as if|as though|that|of)\b", lowered):
        found.append(re.search(r"\b(feels|feeling)\s+(like|as if|as though|that|of)\b", lowered).group(0))
    return found


@register_check("WORDS-01", level="E", build=1, title="Emotion adjectives in does or task",
                plain="names a feeling where it should describe what the body visibly does")
def check_words_01(run):
    problems = []
    for type_name, field_name in (("SHOT", "subject"), ("BEAT", "task")):
        for record in records_of(run, type_name):
            for item in items(run, record, field_name):
                found = emotion_words_in(run.words, item.get("does") or "")
                if found:
                    problems.append(problem_at(
                        run, "E", "WORDS-01", record, f"{field_name} does",
                        f"{(item.first or '').strip()} {', '.join(quote_for_message(word) for word in found)} names a "
                        "feeling, not a visible behaviour",
                        "Fix: write two or three things the body does that show it (A3 R2, C3 section 6).",
                        containing=(item.first or "").strip() or None))
    return problems


_RETIRED_CACHE = {}


def retired_entries(words, modes=("always",)):
    """The retired entries of words.json with the given flag modes (cached per word list)."""
    key = ("entries", id(words), tuple(modes))
    cached = _RETIRED_CACHE.get(key)
    if cached is None or cached[0] is not words:
        cached = (words, [entry for entry in (words or {}).get("retired", []) if entry.get("flag") in modes])
        _RETIRED_CACHE[key] = cached
    return list(cached[1])


def retired_pattern(entry):
    """The compiled pattern of one retired entry: its pattern, or its word and extra words as whole words."""
    key = ("pattern", id(entry))
    cached = _RETIRED_CACHE.get(key)
    if cached is not None and cached[0] is entry:
        return cached[1]
    flags = 0 if entry.get("case_sensitive") else re.IGNORECASE
    if entry.get("pattern"):
        pattern = re.compile(entry["pattern"], flags)
    else:
        words = [entry.get("word", "")] + list(entry.get("extra_words") or [])
        alternatives = "|".join(re.escape(word) for word in words if word)
        pattern = re.compile(r"(?<![A-Za-z0-9_])(?:" + alternatives + r")(?![A-Za-z0-9_])", flags)
    _RETIRED_CACHE[key] = (entry, pattern)
    return pattern


class RetiredQuickLook:
    """A quick first look for retired words: an entry is looked at closely only when the text holds the longest word
    of one of its phrases, or matches its pattern (the few entries written as patterns)."""

    def __init__(self, entries):
        self.by_word = {}
        self.patterned = []
        for entry in entries:
            if entry.get("pattern") or entry.get("extra_pattern"):
                self.patterned.append((entry, re.compile("|".join(
                    f"(?:{pattern})" for pattern in (entry.get("pattern"), entry.get("extra_pattern")) if pattern),
                    re.IGNORECASE)))
            if not entry.get("pattern"):
                for phrase in [entry.get("word", "")] + list(entry.get("extra_words") or []):
                    pieces = RETIRED_WORD_PIECE.findall(phrase.lower())
                    if pieces:
                        self.by_word.setdefault(max(pieces, key=len), []).append(entry)

    def candidates(self, text):
        """The entries worth looking at closely for this text, in words.json's order."""
        tokens = set(RETIRED_WORD_PIECE.findall((text or "").lower()))
        found = []
        for token in tokens & self.by_word.keys():
            found += self.by_word[token]
        found += [entry for entry, pattern in self.patterned if pattern.search(text or "")]
        unique = []
        for entry in found:
            if not any(entry is other for other in unique):
                unique.append(entry)
        return unique

    def search(self, text):
        return bool(self.candidates(text))


RETIRED_WORD_PIECE = re.compile(r"[a-z0-9\u00b0']+")


def any_retired_word(words, modes):
    """The quick first look for the retired words of the given modes (cached per word list)."""
    key = ("any", id(words), tuple(modes))
    cached = _RETIRED_CACHE.get(key)
    if cached is None or cached[0] is not words:
        cached = (words, RetiredQuickLook(retired_entries(words, modes)))
        _RETIRED_CACHE[key] = cached
    return cached[1]


def screen_is_a_thing(text, match):
    """True for "the screen left blank": a screen named as a thing, with "left" a verb and a word after it, which is
    no direction (the second full run, Project notes 39); "exits screen left" and "screen left of the door" are still
    the retired direction."""
    before = text[max(0, match.start() - 8):match.start()]
    after = text[match.end():match.end() + 12]
    return bool(re.search(r"(?<![a-z])(?:the|a|its|his|her|their|this|that|your|our)\s+$", before, re.IGNORECASE)) \
        and bool(re.match(r"\s+(?!of\b|to\b|toward)[a-z]", after))


def retired_words_in_text(text, words, modes=("always", "user_text"), field_path=None):
    """[(word as found, entry)] of the retired words (rules/words.json) a text holds, outside double-quoted story
    words. modes chooses the flag modes to look for; field_path ("SHOT.why") also brings in the in_fields entries
    that name that field. Other modules may call this on any user-facing text."""
    text = QUOTED.sub(" ", text or "")
    found = []
    entries = any_retired_word(words, tuple(modes)).candidates(text)
    if field_path:
        type_name, _, field_name = field_path.partition(".")
        base_field = field_name.split(" ")[0]
        for entry in any_retired_word(words, ("in_fields",)).candidates(text):
            targets = entry.get("in_fields") or []
            if any(target in (f"{type_name}.{base_field}", f"*.{base_field}", type_name) for target in targets):
                entries.append(entry)
    seen = set()
    for entry in entries:
        if field_path and field_path.split(" ")[0] in (entry.get("exempt_field_names") or []):
            continue
        for match in retired_pattern(entry).finditer(text):
            written = match.group(0)
            if entry.get("word") == "stage" and text[match.end():match.end() + 3] == ".py":
                continue
            if entry.get("word") == "screen left" and screen_is_a_thing(text, match):
                continue
            if written in (entry.get("exempt") or []):
                continue
            if written.lower() not in seen:
                seen.add(written.lower())
                found.append((written, entry))
            break
        if field_path and entry.get("extra_pattern"):
            if field_path.split(" ")[0] in (entry.get("extra_pattern_in_fields") or []):
                match = re.search(entry["extra_pattern"], text)
                if match and match.group(0).lower() not in seen:
                    seen.add(match.group(0).lower())
                    found.append((match.group(0), entry))
    return found


def use_instead(words, entry, written):
    """The word to write instead of a retired one: for words retired only in user text (checkpoint letters, v0,
    greybox), the user's word from ai_word_and_user_word; otherwise the entry's own replacement."""
    if entry.get("flag") == "user_text":
        for pair in (words or {}).get("ai_word_and_user_word", []):
            if (pair.get("ai") or "").lower() == written.lower():
                return pair.get("user") or entry.get("use_instead") or ""
        if written.lower() == "greybox":
            return "grey previews"
    return entry.get("use_instead") or ""


def story_written_field(run, type_name, field_name):
    definition = definition_of(run, type_name, field_name)
    if definition.get("writer") == "story":
        return True
    condition = definition.get("writer_when")
    if condition and "story" in str(condition):
        return True
    return field_name in ("names",) and type_name == "CHARACTER"


def plain_part_lines(record_file):
    """[(line number, text)] of a file's plain part: the free text above its divider (or above its first record when
    it has no divider)."""
    lines = []
    has_divider = record_file.has_divider
    for segment in record_file.segments:
        if isinstance(segment, TextBlock):
            for number, text in zip(segment.line_numbers, segment.lines):
                if text.strip() == DIVIDER_LINE:
                    return lines
                lines.append((number, text))
        elif not has_divider:
            return lines
    return lines


def file_record_label(record_file):
    return quote_for_message(record_file.name)


@register_check("WORDS-02", level="W", build=1,
                title="A retired word in a field value or in user-facing text",
                plain="uses a word the word list has retired, where one plain word is used for each thing")
def check_words_02(run):
    problems = []
    quick_look = any_retired_word(run.words, ("always", "in_fields"))
    # Above the divider WORDS-04 reports the abbreviations (MCU, CU, POV ...), so they are not reported twice here.
    abbreviations = set((run.words or {}).get("abbreviations", {}).get("words", []))
    for record_file in run.record_files:
        for number, text in plain_part_lines(record_file):
            for written, entry in retired_words_in_text(text, run.words, ("always", "user_text")):
                if written in abbreviations:
                    continue
                problems.append(run.problem(
                    "W", "WORDS-02", file_record_label(record_file), None,
                    f"holds the retired word {quote_for_message(written)} above the divider",
                    f"Fix: write the plain word instead: {use_instead(run.words, entry, written)} (5.7).",
                    line_number=number, file_name=record_file.name))
        for record in record_file.records:
            if not record.known_type or record.type_name in WORDS_02_SKIPPED_TYPES:
                continue
            for line in record.fields:
                if not line.value or not quick_look.search(line.value) or \
                        story_written_field(run, record.type_name, line.name):
                    continue
                for written, entry in retired_words_in_text(line.value, run.words, ("always",),
                                                            f"{record.type_name}.{line.name}"):
                    problems.append(run.problem(
                        "W", "WORDS-02", record, line.name,
                        f"holds the retired word {quote_for_message(written)}",
                        f"Fix: write the plain word instead: {use_instead(run.words, entry, written)} (5.7).",
                        line_number=line.line_number, file_name=record_file.name))
    return problems


def known_capitalised_words(run):
    """Lowercase words that are names this project or its story already uses (WORDS-03)."""
    key = "craft_known_capitalised"
    if key in run.cache:
        return run.cache[key]
    known = set(COMMON_CAPITALISED)
    for record in run.index.values():
        texts = [record.title or ""]
        if record.type_name in ("CHARACTER", "PROP", "LOCATION", "MOTIF", "TEXT", "CAMERA", "WORLD", "PROJECT",
                                "PLAN", "RULE", "SEQUENCE", "CHAPTER"):
            texts += [line.value or "" for line in record.fields]
        for text in texts:
            known.update(piece.lower().strip("'’-") for piece in WORD_PIECE.findall(text))
    if run.story is not None:
        for number in range(run.story.first, run.story.last + 1):
            for piece in WORD_PIECE.findall(run.story.numbered.line(number) or ""):
                if piece[:1].isupper():
                    known.add(piece.lower().strip("'’-"))
    run.cache[key] = known
    return known


def unknown_name_runs(text, known):
    """Runs of two or more capitalised words (not at a sentence's start) that are no name this project knows."""
    found = []
    tokens = list(re.finditer(r"[A-Za-z][A-Za-z'’-]*|[.!?;:]", text))
    run_words = []
    sentence_start = True
    for token in tokens + [None]:
        word = token.group(0) if token else "."
        if word in ".!?;:":
            if len(run_words) >= 2:
                found.append(" ".join(run_words))
            run_words = []
            sentence_start = True
            continue
        titled = bool(TITLE_WORD.match(word))
        if titled and not sentence_start and word.lower().strip("'’-") not in known:
            run_words.append(word)
        else:
            if len(run_words) >= 2:
                found.append(" ".join(run_words))
            run_words = []
        sentence_start = False
    return found


def named_references_in(run, text):
    """What in a prompt-compiled text names a real person, living artist, film title or brand (WORDS-03): the marker
    phrases of words.json, trade mark signs, and runs of capitalised names this project and its story do not use."""
    text = QUOTED.sub(" ", text or "")
    lowered = text.lower()
    found = []
    for phrase in (run.words or {}).get("named_reference_markers", {}).get("phrases", []):
        if re.search(r"(?<![a-z])" + re.escape(phrase.lower()) + r"(?![a-z])", lowered):
            found.append(phrase)
    symbol = BRAND_SYMBOLS.search(text)
    if symbol:
        found.append(symbol.group(0))
    found += unknown_name_runs(text, known_capitalised_words(run))
    return found


@register_check("WORDS-03", level="E", build=1,
                title="A real person, living artist, film title or brand in any field compiled into prompts",
                plain="names a real person, an artist, a film or a brand in words that go into the picture prompts")
def check_words_03(run):
    problems = []
    for type_name, field_names in PROMPT_FIELDS.items():
        for record in records_of(run, type_name):
            for field_name in field_names:
                definition = definition_of(run, type_name, field_name)
                for line_value in record.get_all(field_name):
                    if is_empty(line_value):
                        continue
                    texts = []
                    if definition.get("kind") == "sub_parts" or definition.get("sub_parts"):
                        item = split_item(line_value, definition)
                        first_kind = (definition.get("first_part") or {}).get("kind")
                        if item.first and first_kind == "text":
                            texts.append((field_name, item.first))
                        for key, value in item.parts:
                            entry = next((part for part in definition.get("sub_parts") or []
                                          if part.get("key") == key), {})
                            if entry.get("kind") == "text" and key not in ("why",):
                                texts.append((f"{field_name} {key}", value))
                    else:
                        texts.append((field_name, line_value))
                    for label, text in texts:
                        found = named_references_in(run, text)
                        if found:
                            problems.append(problem_at(
                                run, "E", "WORDS-03", record, label,
                                f"names {', '.join(quote_for_message(piece) for piece in found)}, which reads as a "
                                "real person, artist, film title or brand",
                                "Fix: describe the visible qualities instead of naming anyone or anything real "
                                "(STYLE named_reference_policy: describe_qualities_only).",
                                containing=found[0] if found[0] in line_value else None))
    return problems


def abbreviation_patterns(words):
    """[(word, compiled pattern)] of words.json's abbreviations, matched as written (cached per word list)."""
    key = ("abbreviations", id(words))
    cached = _RETIRED_CACHE.get(key)
    if cached is not None and cached[0] is words:
        return cached[1]
    rule = (words or {}).get("abbreviations", {})
    patterns = []
    for word in rule.get("words", []):
        if word.endswith("."):
            pattern = r"(?<![A-Za-z.])" + re.escape(word)
        else:
            pattern = r"(?<![A-Za-z0-9_.])" + re.escape(word) + r"(?![A-Za-z0-9_])"
        patterns.append((word, re.compile(pattern)))
    _RETIRED_CACHE[key] = (words, patterns)
    return patterns


def abbreviations_in_text(text, words):
    """[(what, kind)] of the abbreviations and internal codes (rules/words.json) a user-facing text holds, outside
    double-quoted story words and file names. Other modules may call this on guides, steps and templates."""
    text = QUOTED.sub(" ", text or "")
    text = re.sub(r"\S+\.(?:csv|srt|vtt|json|otio|edl|md|html|zip|pdf|txt|py)\b", " ", text, flags=re.I)
    found = []
    for word, pattern in abbreviation_patterns(words):
        if pattern.search(text):
            found.append((word, "abbreviation"))
    codes = (words or {}).get("abbreviations", {}).get("internal_code_patterns", {})
    for kind, pattern in codes.items():
        for match in re.finditer(pattern, text):
            written = match.group(0)
            if kind == "named record ID" and not re.search(r"[-\d]", written):
                continue
            found.append((written.strip(), kind))
            break
    return found


@register_check("WORDS-04", level="W", build=1,
                title="An abbreviation or internal code in user-facing text",
                plain="uses an abbreviation or an internal code in the part of a file written for you")
def check_words_04(run):
    problems = []
    for record_file in run.record_files:
        for number, text in plain_part_lines(record_file):
            for written, kind in abbreviations_in_text(text, run.words):
                problems.append(run.problem(
                    "W", "WORDS-04", file_record_label(record_file), None,
                    f"holds the {kind} {quote_for_message(written)} above the divider",
                    "Fix: write the full plain words (principle 7).", line_number=number,
                    file_name=record_file.name))
    return problems


def description_range(run, character):
    ranges = constant_of(run, "fixed_description_words", {"principal": [25, 40], "minor": [20, 30]}) or {}
    tier = word_of(character.get("tier"))
    key = "minor" if tier in ("minor", "extra") else "principal"
    return tier or key, ranges.get(key)


def expression_words_in(words, text):
    rule = (words or {}).get("expression_words", {})
    lowered = QUOTED.sub(" ", text or "").lower()
    return [word for word in rule.get("words", [])
            if re.search(r"(?<![a-z-])" + re.escape(word.lower()) + r"(?:s|es)?(?![a-z-])", lowered)]


@register_check("WORDS-05", level="E", build=1,
                title="A fixed description outside its length, or with expression words",
                plain="has a fixed description of the wrong length, or one that fixes an expression on the face")
def check_words_05(run):
    problems = []
    for character in records_of(run, "CHARACTER"):
        text = character.get("fixed_description")
        if not text or is_empty(text):
            continue
        tier, allowed = description_range(run, character)
        count = count_words(text)
        if allowed and not (allowed[0] <= count <= allowed[1]):
            problems.append(problem_at(
                run, "E", "WORDS-05", character, "fixed_description",
                f"has {count} words; a {tier} character's fixed description has {allowed[0]}-{allowed[1]}",
                "Fix: " + ("add visible nouns (face, hair, build, clothes)" if count < allowed[0] else
                           "cut to the visible nouns a stranger needs to recognise them") + " (B5, C2, C5)."))
    for type_name in ("CHARACTER", "PROP"):
        for record in records_of(run, type_name):
            text = record.get("fixed_description")
            found = expression_words_in(run.words, text) if text else []
            if found:
                problems.append(problem_at(
                    run, "E", "WORDS-05", record, "fixed_description",
                    f"holds the expression {'word' if len(found) == 1 else 'words'} "
                    f"{', '.join(quote_for_message(word) for word in found)}",
                    "Fix: keep only visible nouns; the expression belongs in each shot's does and display (B5, C2)."))
    return problems


# ---------------------------------------------------------------- helpers for other modules (text outside records)

def mood_only_phrases_in_reason(text, words):
    """The mood-only phrases of words.json a reason holds (REASON-04's rule), for text outside record files."""
    return mood_phrases_in(words, text)


def reason_is_anchored(run, text, scene=None):
    """True when a reason quotes the scene, cites an existing ID or names an element (REASON-03's rule)."""
    return reason_anchor(run, text, scene).anchored
