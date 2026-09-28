"""make_handout.py: the loop's two commands, next and handout (blueprint section 3's unit order, 6.1, 7.1).

What this file does, in plain words:
- works out the order of every unit of work in a project: steps 0 to 6 in order, once each; then steps 7 and 8
  sequence by sequence (step 7 designs and lists a sequence's scenes, the checkpoint shows that group of shots,
  step 8 writes their shots batch by batch); then steps 9 to 11. Between them sit the checkpoints that wait for
  the user (the rights question, the scene list, how the book becomes a film, the big choices, the first group of
  shots, the finished check);
- says which units are done: the manifest's list of units applied, or the records a unit writes already there
  (a folder adopted from a chat app has no list of units, only its records);
- next: names the next unit, the checkpoint that waits for the user, or the command code must run; for a unit
  it also builds the handout and says where the AI writes its records. With --checkpoint-passed it records the
  user's answer to a checkpoint that has no choice record of its own (the first group of shots, the finished
  check), and a group of shots passed (or reported) gets its shot lists marked approved;
- handout <unit>: builds one unit's handout, "For machines - do not edit/handouts/<unit>.md", the one file the AI
  reads for that unit: the one-line task first; what to write and where; the IDs issued to the unit (also written
  into the manifest, where the checker's ID-06 reads them); the step file; the card parts steps.json names for the
  step, the depth and the scene's tags; the records the unit needs and only those, with what code keeps (status,
  locks, the beats code gave story points) left out; the story's lines; at step 8 each list item's provisional
  time floor, the sizes, angles and moves the camera system allows here, the saved choices with their uses left
  and the fields that need a why with their defaults; the record template at the project's depth; one example
  from the gold; and the one-line task again at the end;
- keeps a handout within its surface's ceiling (rules/limits.json): card parts are capped at
  card_tokens_per_unit_max (the lowest-listed parts are left out first); over the ceiling it leaves out the
  example, then the lowest-listed card parts, then trims the story to the unit's own lines, and then says the unit
  must be split.

Other modules use: next_unit(project_folder) (stage.py status prints it), Workspace, plan_units, find_next_unit,
unit_from_identifier, build_handout, write_handout, estimate_tokens.

Standard library only.
"""

import json
import math
import re
from dataclasses import dataclass, field as dataclass_field
from pathlib import Path

from .project_files import (MACHINE_FOLDER, Project, StageStop, history_run_folder, keep_in_history, load_steps, now,
                            plural, unit_in_plain_words)
from .record_format import (DIVIDER_LINE, SKILL_FOLDER, load_skill_data, merge_copies, normalise_word, parse_file,
                            parse_line_numbers, sort_key_for_identifier, split_item, split_list, write_file)

HANDOUTS_FOLDER = "handouts"
INBOX_FOLDER = "inbox"
STORY_MAP_FILE = "story map.json"
QUESTIONS_FILE = "questions.json"
FILM_STRIP_FILE = "film strip.txt"
WHOLE_FILM_FILE = "12 Whole-film check.md"
HEALTH_CHECK_FILE = "13 Health check.md"
BOOK_FILE = "15 The breakdown/The breakdown.html"
GOLD_SCENE_FILE = "examples/01 The Catch - scene 10.md"
GOLD_CONTEXT_FILE = "examples/02 The Catch - scene 10 - context.md"

UNIT_IDENTIFIER = re.compile(r"^U-(\d{2})-(.+)$")
SCENE_IDENTIFIER = re.compile(r"^SC\d{2,3}[A-Z]?$")
SCENE_PREFIX = re.compile(r"^(SC\d{2,3}[A-Z]?)(?:-|$)")
SCENE_RANGE = re.compile(r"^(SC\d{2,3}[A-Z]?)\.\.(SC\d{2,3}[A-Z]?)$")
SHOT_NUMBER = re.compile(r"-SH(\d+)$")
STORY_POINT_ENDING = re.compile(r'(?<=["\u201d])\s*=\s*SC\d{2,3}[A-Z]?-B\d{2,3}\b')
SCENE_WORDS = re.compile(r"^SC0*(\d+)([A-Z]?)$")
DEPTH_RANK_OF = {"quick": 1, "standard": 2, "detailed": 3}
DEPTH_OF_HINT = {"quick": 1, "standard": 2, "detailed": 3}
CODE_KEPT_FIELDS = ("status", "locked", "approved")
STEP_OF_CHECKPOINT = {"rights": 0, "a": 1, "p": 2, "b": 5, "c": 7, "acceptance": 10}

# An estimate of tokens from characters, used beside rules/limits.json's tokens_per_word_estimate so that record
# text (IDs, numbers, punctuation) is not under-counted: the larger of the two estimates counts. [judgement]
CHARACTERS_PER_TOKEN = 4
# How many numbers a unit's block of choices (and of findings, outside the review questions) holds, so that units
# built side by side (helper agents taking scenes) never share a number. [judgement]
ISSUED_BLOCK_SIZE = 20

# The checkpoints as the user sees them (blueprint 13.3): named by what they are, never by letter.
CHECKPOINT_NAMES = {
    "rights": "the rights question",
    "a": "the scene list",
    "p": "how the book becomes a film",
    "b": "the big choices",
    "c": "each group of shots",
    "acceptance": "the finished check",
}

# The fields of each record type a handout shows when the whole record is not needed (inputs a unit reads).
BRIEF_FIELDS = {
    "SCENE": ["heading", "lines", "event", "sequence", "scene_intensity", "whose_scene", "tone", "tags", "keep"],
    "CHAPTER": ["title", "lines", "words"],
    "CHARACTER": ["names", "tier", "role", "fixed_description"],
    "VOICE": ["character", "pace_wps", "accent"],
    "LOCATION": ["headings", "story_job", "loudness", "room_sound"],
    "PROP": ["names", "category", "fixed_description", "side", "motif"],
    "TEXT": ["kind", "words", "on", "reader"],
    "MOTIF": ["meaning", "rank", "channel"],
    "STATE": ["element", "from", "state_line", "side", "handedness"],
    "CHOICE": ["question", "answer", "checkpoint"],
    "PLANT": ["what", "planted_at", "paid_off_at"],
    "FACT": ["what", "element", "audience_knows_from"],
    "SEQUENCE": ["title", "scenes", "act", "value_change"],
    "RULE": ["kind", "statement", "governs"],
    "LOOK": ["for", "time", "main_light", "contrast"],
}
# The fields of a character present in a scene that steps 7 and 8 read (blueprint 3, step 7's inputs).
CHARACTER_FIELDS_FOR_SCENES = ["names", "tier", "role", "fixed_description", "height_m", "movement", "gesture",
                               "status_play", "distance", "voice"]
VOICE_FIELDS_FOR_SCENES = ["character", "voice_description", "pitch", "pace_wps", "accent", "path_sound"]
PROP_FIELDS_FOR_SCENES = ["names", "category", "fixed_description", "real_size", "side", "text", "motif", "origin"]
TEXT_FIELDS_FOR_SCENES = ["kind", "words", "on", "origin", "reader", "plot_critical", "emphasis", "method"]
MOTIF_FIELDS_FOR_SCENES = ["meaning", "rank", "channel", "signature"]
RULE_FIELDS_FOR_SCENES = ["kind", "statement", "governs", "era", "exception", "policy"]
PLAN_FIELDS_FOR_SCENES = ["logline", "theme_question", "core_value", "core_opposition", "crisis", "climax",
                          "pov_plan", "genre", "tone_home", "tone_range", "tone_mix_rule"]
LOCATION_FIELDS_WITHOUT_PLAN = ["headings", "story_job", "loudness", "room_sound", "anchor", "exit", "dressing"]


# ---------------------------------------------------------------- small helpers

def read_json_file(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


def constant_value(constants, name, default=None):
    """The value of a named constant of rules/constants.json (either table), or default."""
    for section in ((constants or {}).get("constants", {}),
                    (constants or {}).get("from_blueprint_text", {}).get("constants", {})):
        if name in section:
            entry = section[name]
            return entry.get("value", default) if isinstance(entry, dict) else entry
    return default


def is_omitted(record):
    return normalise_word(record.get("status") or "") == "omitted"


def scene_of(identifier):
    match = SCENE_PREFIX.match(identifier or "")
    return match.group(1) if match else None


def shot_number(identifier):
    match = SHOT_NUMBER.search(identifier or "")
    return int(match.group(1)) if match else None


def scene_words(identifier):
    """'SC10' -> 'scene 10', 'SC06A' -> 'scene 6A'."""
    match = SCENE_WORDS.match(identifier or "")
    return f"scene {match.group(1)}{match.group(2)}" if match else (identifier or "")


def scene_number_text(identifier):
    match = SCENE_WORDS.match(identifier or "")
    return f"{match.group(1)}{match.group(2)}" if match else (identifier or "")


def words_of(text):
    return [piece for piece in (text or "").split() if piece.strip()]


def estimate_tokens(text, tokens_per_word=1.4):
    """An estimate of a text's tokens: the larger of words x tokens_per_word_estimate (rules/limits.json) and
    characters / CHARACTERS_PER_TOKEN, so dense record text is not under-counted."""
    text = text or ""
    by_words = len(text.split()) * float(tokens_per_word)
    by_characters = len(text) / CHARACTERS_PER_TOKEN
    return int(math.ceil(max(by_words, by_characters)))


def number_with_commas(value):
    return f"{int(value):,}"


def seconds_text(value):
    if value is None:
        return "?"
    text = f"{round(float(value), 2):.2f}".rstrip("0")
    return text + "0" if text.endswith(".") else text


def strip_story_point_endings(value):
    """A value without the ' = <beat>' endings code adds to story points (the AI never types them)."""
    return STORY_POINT_ENDING.sub("", value or "")


def demote_headings(text, levels=1):
    """Markdown headings made smaller by one level (## -> ###), except inside fenced code blocks, so a step file or
    a card sits under the handout's own headings."""
    output = []
    in_fence = False
    for line in (text or "").splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            output.append(line)
            continue
        if not in_fence and re.match(r"^#{1,5} ", line):
            output.append("#" * levels + line)
        else:
            output.append(line)
    return "\n".join(output)


def fenced(text, language="text"):
    return f"```{language}\n{text.rstrip()}\n```"


def expand_range(value, order):
    """The scene IDs an id_range or list names ('SC07..SC10', 'SC07, SC08'), in the order given."""
    found = []
    for piece in split_list(value or ""):
        match = SCENE_RANGE.match(piece.strip())
        if match and match.group(1) in order and match.group(2) in order:
            first, last = order.index(match.group(1)), order.index(match.group(2))
            found += order[min(first, last):max(first, last) + 1]
        elif match:
            first_key, last_key = sort_key_for_identifier(match.group(1)), sort_key_for_identifier(match.group(2))
            found += [scene for scene in order if first_key <= sort_key_for_identifier(scene) <= last_key]
        elif piece.strip():
            found.append(piece.strip())
    unique = []
    for scene in found:
        if scene not in unique:
            unique.append(scene)
    return unique


def balanced_chunks(items, most):
    """Items split into consecutive groups of at most `most`, the groups as even in size as possible."""
    items = list(items)
    if not items:
        return []
    most = max(1, int(most))
    count = int(math.ceil(len(items) / most))
    base, extra = divmod(len(items), count)
    chunks, start = [], 0
    for index in range(count):
        size = base + (1 if index < extra else 0)
        chunks.append(items[start:start + size])
        start += size
    return chunks


# ---------------------------------------------------------------- the project, as a plan and a handout read it

class Workspace:
    """One project with everything a plan or a handout reads: its records merged by ID, its story and speeches,
    its manifest, and the skill's steps, limits, cards and templates (from skill_folder, the skill by default)."""

    def __init__(self, project_folder, schema=None, words=None, constants=None, skill_folder=None, limits=None):
        self.skill_folder = Path(skill_folder).resolve() if skill_folder else SKILL_FOLDER
        if schema is None or words is None or constants is None:
            loaded_schema, loaded_words, loaded_constants = load_skill_data(skill_folder)
            schema = schema or loaded_schema
            words = words or loaded_words
            constants = constants or loaded_constants
        self.schema = schema
        self.words = words or {}
        self.constants = constants or {}
        self.folder = Path(project_folder).resolve()
        self.project = Project(self.folder, self.schema, self.words)
        self.steps = load_steps(skill_folder) or {}
        self.limits = limits if limits is not None else (read_json_file(self.skill_folder / "rules/limits.json") or {})
        self.record_files = self.project.load_record_files()
        self.index, _ = merge_copies(self.record_files, self.schema)
        self.by_identifier = {}
        for (type_name, identifier), record in self.index.items():
            self.by_identifier.setdefault(identifier or type_name, record)
        self.manifest = self.project.read_manifest()
        self.story_map = read_json_file(self.project.machine_folder / STORY_MAP_FILE)
        self.story = None
        if self.story_map:
            try:
                from .read_story import NumberedStory
                self.story = NumberedStory.from_story_map(self.story_map)
            except (ImportError, KeyError, ValueError):
                self.story = None
        self._breakdown = None
        self._check_run = None
        self._plan = None

    # -- records
    def records(self, type_name, include_omitted=False):
        found = [record for (kind, _), record in self.index.items() if kind == type_name]
        if not include_omitted:
            found = [record for record in found if not is_omitted(record)]
        return sorted(found, key=lambda record: sort_key_for_identifier(record.identifier or ""))

    def record(self, identifier, type_name=None):
        if identifier is None:
            return None
        if type_name:
            return self.index.get((type_name, identifier))
        return self.by_identifier.get(identifier)

    def singleton(self, type_name):
        return self.index.get((type_name, None))

    @property
    def project_record(self):
        found = self.records("PROJECT", include_omitted=True)
        return found[0] if found else None

    def project_value(self, name, default=None):
        record = self.project_record
        value = record.get(name) if record is not None else None
        return value if value not in (None, "") else default

    def constant(self, name, default=None):
        return constant_value(self.constants, name, default)

    def limit(self, name, default=None):
        entry = self.limits.get(name)
        if isinstance(entry, dict):
            return entry.get("value", default)
        return entry if entry is not None else default

    # -- the project's settings
    @property
    def depth(self):
        value = normalise_word(self.project_value("depth", "standard"))
        return value if value in DEPTH_RANK_OF else "standard"

    def scene_depth(self, scene_identifier):
        """The deeper of the project's depth and the scene's own ("go deeper on scene 13")."""
        scene = self.record(scene_identifier, "SCENE")
        own = normalise_word(scene.get("depth") or "") if scene is not None else ""
        if own in DEPTH_RANK_OF and DEPTH_RANK_OF[own] > DEPTH_RANK_OF[self.depth]:
            return own
        return self.depth

    @property
    def surface(self):
        return normalise_word(self.project_value("surface", "claude_code"))

    @property
    def code_execution(self):
        return normalise_word(self.project_value("code_execution", "yes")) != "no"

    def ceiling(self, surface=None):
        """The handout ceiling in tokens for a surface (rules/limits.json handout_tokens_max); chat surfaces, which
        read no handouts, take the Claude surfaces' ceiling."""
        table = self.limits.get("handout_tokens_max") or {}
        value = table.get(surface or self.surface)
        if not isinstance(value, (int, float)):
            value = table.get("claude_code")
        return int(value) if isinstance(value, (int, float)) else None

    @property
    def card_cap(self):
        return int(self.limit("card_tokens_per_unit_max", 9000))

    @property
    def tokens_per_word(self):
        return float(self.limit("tokens_per_word_estimate", 1.4))

    @property
    def batch_size(self):
        written = self.project_value("batch_size")
        try:
            return int(float(written))
        except (TypeError, ValueError):
            value = self.constant("batch_size", {"default": 12})
            return int(value.get("default", 12)) if isinstance(value, dict) else int(value)

    @property
    def source_kind(self):
        kind = normalise_word(self.project_value("source_kind", "") or "")
        if not kind and self.story_map:
            kind = "prose" if self.story_map.get("chapters") and not self.story_map.get("scenes") else "screenplay"
        return kind or "screenplay"

    @property
    def is_prose(self):
        return self.source_kind == "prose"

    # -- the story
    def scene_order(self):
        """Every kept scene in screen order: the SCENE records, else the scenes the reader found."""
        scenes = [record.identifier for record in self.records("SCENE") if record.identifier]
        if not scenes and self.story_map:
            scenes = [scene["id"] for scene in self.story_map.get("scenes", [])]
        return sorted(dict.fromkeys(scenes), key=sort_key_for_identifier)

    def kept_scene_order(self):
        """The scenes the compression plan keeps (SCENE keep is not cut or merged), in screen order."""
        kept = []
        for scene in self.scene_order():
            record = self.record(scene, "SCENE")
            keep = normalise_word((record.get("keep") if record is not None else None) or "keep")
            if keep not in ("cut", "merged"):
                kept.append(scene)
        return kept

    def story_scene(self, scene_identifier):
        for scene in (self.story_map or {}).get("scenes", []):
            if scene.get("id") == scene_identifier:
                return scene
        return None

    def chapter_order(self):
        chapters = [record.identifier for record in self.records("CHAPTER") if record.identifier]
        if not chapters and self.story_map:
            chapters = [chapter["id"] for chapter in self.story_map.get("chapters", [])]
        return sorted(dict.fromkeys(chapters), key=sort_key_for_identifier)

    def scene_lines(self, scene_identifier):
        """(first, last) story lines of a scene, from its SCENE lines, else the reader's scenes."""
        scene = self.record(scene_identifier, "SCENE")
        value = scene.get("lines") if scene is not None else None
        if value:
            ranges = parse_line_numbers(value)
            if ranges:
                return ranges[0][0], ranges[-1][1]
            if self.story is not None:
                resolved = self.story.resolve_lines(value)
                if resolved:
                    return resolved
        story_scene = self.story_scene(scene_identifier)
        if story_scene:
            return tuple(story_scene["lines"])
        return None

    def chapter_lines(self, chapter_identifier):
        chapter = self.record(chapter_identifier, "CHAPTER")
        value = chapter.get("lines") if chapter is not None else None
        ranges = parse_line_numbers(value) if value else None
        if ranges:
            return ranges[0][0], ranges[-1][1]
        for entry in (self.story_map or {}).get("chapters", []):
            if entry.get("id") == chapter_identifier:
                return tuple(entry["lines"])
        return None

    def non_blank_lines(self, scene_identifier):
        story_scene = self.story_scene(scene_identifier)
        if story_scene and story_scene.get("counts", {}).get("non_blank_lines") is not None:
            return int(story_scene["counts"]["non_blank_lines"])
        lines = self.scene_lines(scene_identifier)
        if lines and self.story is not None:
            return sum(1 for number in range(lines[0], lines[1] + 1) if self.story.line(number).strip())
        return None

    def scene_heading(self, scene_identifier):
        scene = self.record(scene_identifier, "SCENE")
        if scene is not None and scene.get("heading"):
            return scene.get("heading")
        story_scene = self.story_scene(scene_identifier)
        return story_scene.get("heading") if story_scene else None

    def story_read(self):
        return bool(self.story_map)

    # -- derived fields and checks, made once
    @property
    def breakdown(self):
        if self._breakdown is None:
            from .derive_fields import Breakdown, load_video_models, speeches_from_json
            speeches = {}
            data = read_json_file(self.project.machine_folder / "speeches.json")
            if data:
                speeches = speeches_from_json(data)
            self._breakdown = Breakdown(self.record_files, self.schema, self.words, self.constants, story=self.story,
                                        speeches=speeches, models=load_video_models(), project_folder=self.folder,
                                        story_map=self.story_map)
        return self._breakdown

    @property
    def check_run(self):
        """A check run over the project (the film pass's counters of saved choices read one)."""
        if self._check_run is None:
            from .check_records import CheckRun, StorySource
            story = None
            try:
                story = StorySource.from_project(self.folder)
            except Exception:  # the counters need no story; a story that cannot be read is left out
                story = None
            self._check_run = CheckRun(self.record_files, self.schema, self.words, self.constants, story=story,
                                       manifest=self.manifest, project=self.project)
        return self._check_run

    # -- the steps
    def step_entry(self, step):
        for entry in self.steps.get("steps", []):
            if entry.get("step") == step:
                return entry
        return {}

    def units_done(self):
        return {entry.get("unit") for entry in self.manifest.get("units_done", []) if entry.get("unit")}

    def plan(self):
        if self._plan is None:
            self._plan = plan_units(self)
        return self._plan


# ---------------------------------------------------------------- units and the order they run in (section 3)

@dataclass
class Unit:
    """One piece of work: an AI unit (one reply), a command code runs, or a checkpoint that waits for the user."""
    identifier: str
    step: int
    kind: str = "ai"                      # ai | code | checkpoint
    entry_of_unit: dict = None                     # the steps.json unit it comes from
    scenes: list = dataclass_field(default_factory=list)
    chapters: list = dataclass_field(default_factory=list)
    characters: list = dataclass_field(default_factory=list)
    places: list = dataclass_field(default_factory=list)
    sequence: str = None
    part: int = None                      # U-07-SCnn-P<n>
    list_unit: bool = False               # U-07-SCnn-LIST
    batch: int = None                     # U-08-SCnn-B<n>
    shots: list = dataclass_field(default_factory=list)
    lines: tuple = None                   # the unit's own story lines, when narrower than its scenes
    commands: list = dataclass_field(default_factory=list)
    checkpoint: str = None
    blocks: bool = True
    first_group: bool = False
    act: int = None
    strip_file: str = None
    note: str = ""

    @property
    def scene(self):
        return self.scenes[0] if self.scenes else None

    def plain(self, steps=None):
        if self.kind == "checkpoint":
            name = CHECKPOINT_NAMES.get(self.checkpoint, "a checkpoint")
            if self.checkpoint == "c" and self.scenes:
                return f"{name}: {scene_group_words(self.scenes)}"
            return name
        if self.kind == "code":
            step_name = step_user_name(steps, self.step)
            return f"step {self.step + 1} of 12 ({step_name}), work that code does"
        words = unit_in_plain_words(self.identifier, steps)
        if self.step <= 11:
            words = words.replace(f"step {self.step + 1} (", f"step {self.step + 1} of 12 (", 1)
        return words


def step_user_name(steps, step):
    for entry in (steps or {}).get("steps", []):
        if entry.get("step") == step:
            return entry.get("user_name") or entry.get("name") or f"step {step + 1}"
    return f"step {step + 1}"


def scene_group_words(scenes):
    if not scenes:
        return "no scenes"
    if len(scenes) == 1:
        return scene_words(scenes[0])
    return f"scenes {scene_number_text(scenes[0])} to {scene_number_text(scenes[-1])}"


def pattern_expression(pattern):
    """A steps.json id_pattern ('U-07-<scene>-P<n>') as a regular expression."""
    placeholders = {
        "<first scene>..<last scene>": r"SC\d{2,3}[A-Z]?\.\.SC\d{2,3}[A-Z]?",
        "<scene>": r"SC\d{2,3}[A-Z]?",
        "<chapter>": r"CP\d{2,3}",
        "<sequence>": r"SQ\d{2,3}",
        "<character>": r"CH-[A-Z0-9]+(?:-[A-Z0-9]+)*",
        "<n>": r"\d+",
    }
    pieces = re.split(r"(<first scene>\.\.<last scene>|<[a-z ]+>)", pattern)
    expression = ""
    for piece in pieces:
        expression += placeholders.get(piece, re.escape(piece))
    return re.compile("^" + expression + "$")


def unit_entry_for(workspace, step, identifier):
    """The steps.json unit whose id_pattern matches a unit ID, or None."""
    for entry_of_unit in workspace.step_entry(step).get("units", []):
        pattern = entry_of_unit.get("id_pattern", "")
        if pattern.startswith("code:"):
            continue
        if pattern_expression(pattern).match(identifier):
            return entry_of_unit
    return None


def code_unit_entry(workspace, step):
    for entry_of_unit in workspace.step_entry(step).get("units", []):
        if entry_of_unit.get("id_pattern", "").startswith("code:"):
            return entry_of_unit
    return None


def ai_unit(workspace, identifier, step, **values):
    return Unit(identifier=identifier, step=step, entry_of_unit=unit_entry_for(workspace, step, identifier), **values)


def code_unit(workspace, step, commands, identifier=None):
    return Unit(identifier=identifier or "code: " + ", ".join(commands), step=step, kind="code",
                entry_of_unit=code_unit_entry(workspace, step), commands=list(commands))


def checkpoint_unit(checkpoint, identifier=None, blocks=True, **values):
    return Unit(identifier=identifier or f"CHECKPOINT-{checkpoint.upper()}", step=STEP_OF_CHECKPOINT[checkpoint],
                kind="checkpoint", checkpoint=checkpoint, blocks=blocks, **values)


def principal_characters(workspace):
    """(principals, minor characters) for step 4's units: the tier written at step 4 when there is one; else a
    character is a principal when some scene belongs to them (whose_scene) or, with no whose_scene yet, when they
    speak in more than one scene."""
    characters = [record.identifier for record in workspace.records("CHARACTER") if record.identifier]
    if not characters and workspace.story_map:
        characters = [entry["id"] for entry in workspace.story_map.get("characters", []) if entry.get("id")]
    owners = {scene.get("whose_scene") for scene in workspace.records("SCENE") if scene.get("whose_scene")}
    speaking_scenes = {}
    for scene in workspace.records("SCENE"):
        for value in scene.get_all("speaking"):
            character = split_item(value).first
            if character:
                speaking_scenes[character] = speaking_scenes.get(character, 0) + 1
    principals, minors = [], []
    for character in characters:
        record = workspace.record(character, "CHARACTER")
        tier = normalise_word(record.get("tier") or "") if record is not None else ""
        if tier:
            (principals if tier == "principal" else minors).append(character)
        elif owners:
            (principals if character in owners else minors).append(character)
        else:
            (principals if speaking_scenes.get(character, 0) > 1 else minors).append(character)
    return principals, minors


def place_key(text):
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def places_of_scenes(workspace):
    """The distinct places of the story's scenes (their place words), in order of first appearance."""
    places = []
    for scene in workspace.scene_order():
        record = workspace.record(scene, "SCENE")
        text = record.get("place_text") if record is not None else None
        if not text:
            story_scene = workspace.story_scene(scene)
            text = story_scene.get("place_text") if story_scene else None
        if text and place_key(text) not in [place_key(place) for place in places]:
            places.append(text)
    return places


def sequence_groups(workspace):
    """[(sequence ID or None, [scene IDs in scope, in screen order])] in the order steps 7 and 8 take them."""
    order = workspace.kept_scene_order()
    scope = scope_scenes(workspace)
    groups = []
    placed = set()
    for sequence in workspace.records("SEQUENCE"):
        scenes = [scene for scene in expand_range(sequence.get("scenes"), order) if scene in order]
        for scene in order:
            record = workspace.record(scene, "SCENE")
            if record is not None and record.get("sequence") == sequence.identifier and scene not in scenes:
                scenes.append(scene)
        scenes = sorted(dict.fromkeys(scenes), key=order.index)
        scenes = [scene for scene in scenes if scene not in placed]
        placed.update(scenes)
        in_scope = [scene for scene in scenes if scope is None or scene in scope]
        if in_scope:
            groups.append((sequence.identifier, in_scope))
    rest = [scene for scene in order if scene not in placed and (scope is None or scene in scope)]
    if rest:
        groups.append((None, rest))
    groups.sort(key=lambda group: order.index(group[1][0]))
    return groups


def scope_scenes(workspace):
    """The scenes in PROJECT.scope, or None when the scope is all (or not set yet)."""
    value = workspace.project_value("scope")
    if not value or normalise_word(value) in ("all", "open", "none"):
        return None
    return set(expand_range(value, workspace.scene_order())) or None


def scene_is_big(workspace, scene_identifier):
    """A scene over scene_split_non_blank_lines non-blank lines (heading included) or scene_split_beats beats is
    designed in two units by part and listed in a third (blueprint 3, step 7)."""
    lines_most = int(workspace.constant("scene_split_non_blank_lines", 70))
    beats_most = int(workspace.constant("scene_split_beats", 14))
    count = workspace.non_blank_lines(scene_identifier)
    beats = len([beat for beat in workspace.records("BEAT") if scene_of(beat.identifier) == scene_identifier])
    return (count is not None and count > lines_most) or beats > beats_most


def part_line_split(workspace, scene_identifier):
    """The line where part 2 of a big scene starts: the blank line nearest the middle of its non-blank lines."""
    lines = workspace.scene_lines(scene_identifier)
    if not lines or workspace.story is None:
        return None
    first, last = lines
    non_blank = [number for number in range(first, last + 1) if workspace.story.line(number).strip()]
    if len(non_blank) < 2:
        return None
    middle = non_blank[len(non_blank) // 2]
    blanks = [number for number in range(first + 1, last) if not workspace.story.line(number).strip()]
    if not blanks:
        return middle
    nearest = min(blanks, key=lambda number: (abs(number - middle), number))
    return nearest + 1


def list_item_shots(workspace, scene_identifier):
    """The shot IDs a scene's one-line list declares, in ID order."""
    shot_list = workspace.record(f"{scene_identifier}-LIST", "SHOTLIST")
    if shot_list is None:
        return []
    definition = workspace.schema.field("SHOTLIST", "item")
    shots = []
    for value in shot_list.get_all("item"):
        first = (split_item(value, definition).first or "").strip()
        if first and first not in shots:
            shots.append(first)
    return sorted(shots, key=lambda shot: (shot_number(shot) is None, shot_number(shot) or 0, shot))


def batch_number(unit_identifier):
    match = re.search(r"-B(\d+)$", unit_identifier or "")
    return int(match.group(1)) if match else None


def plan_batches(workspace, scene_identifier):
    """[(unit ID, [shot IDs])] for a scene's step-8 batches: batch_size list items at most, split by ID range
    and as even in size as possible. A plan already in the manifest is kept while it covers the list; batches
    already written stay as they are and only the rest is planned again."""
    shots = list_item_shots(workspace, scene_identifier)
    if not shots:
        return []
    stored = (workspace.manifest.get("batches") or {}).get(scene_identifier) or {}
    planned = []
    for unit, entry in sorted(stored.items(), key=lambda pair: batch_number(pair[0]) or 0):
        first, last = (entry or {}).get("first"), (entry or {}).get("last")
        if not first or not last or shot_number(first) is None or shot_number(last) is None:
            continue
        inside = [shot for shot in shots if shot_number(first) <= (shot_number(shot) or -1) <= shot_number(last)]
        planned.append((unit, inside, entry))
    covered = [shot for _, inside, _ in planned for shot in inside]
    if planned and sorted(covered, key=shots.index) == shots and len(covered) == len(set(covered)) and all(
            entry.get("expected") in (None, len(inside)) or entry.get("received") is not None
            for _, inside, entry in planned):
        return [(unit, inside) for unit, inside, _ in planned if inside]
    kept = [(unit, inside) for unit, inside, entry in planned if entry.get("received") is not None and inside]
    taken = {shot for _, inside in kept for shot in inside}
    rest = [shot for shot in shots if shot not in taken]
    number = max([batch_number(unit) or 0 for unit, _ in kept] + [0])
    for chunk in balanced_chunks(rest, workspace.batch_size):
        number += 1
        kept.append((f"U-08-{scene_identifier}-B{number}", chunk))
    return sorted(kept, key=lambda pair: shot_number(pair[1][0]) or 0)


def film_strip_parts(workspace):
    folder = workspace.project.machine_folder
    parts = sorted(folder.glob("film strip - part *.txt"), key=lambda path: sort_key_for_identifier(path.name))
    return [path.name for path in parts]


def question_units(workspace):
    questions = workspace.manifest.get("questions") or {}
    units = list(questions.get("units") or [])
    if not units:
        data = read_json_file(workspace.project.machine_folder / QUESTIONS_FILE) or {}
        units = [batch.get("unit") for batch in data.get("batches", []) if batch.get("unit")]
    return units


def plan_units(workspace):
    """Every unit of steps 0 to 11 in the order they run (blueprint section 3), as far as the records say today:
    later units (batches, question units) are planned once the records they come from exist."""
    units = []
    order = workspace.kept_scene_order()
    prose = workspace.is_prose

    # Step 0: the hidden self-test, the welcome with its one question, and the rights answer.
    units.append(code_unit(workspace, 0, ["selftest --prepare", "selftest --score"], identifier="U-00-SELFTEST"))
    units[-1].entry_of_unit = unit_entry_for(workspace, 0, "U-00-SELFTEST")
    units.append(ai_unit(workspace, "U-00-START", 0, note=original_story_note(workspace)))
    units.append(checkpoint_unit("rights"))

    # Step 1: code reads the story; the AI reads the odd-lines report; checkpoint A.
    units.append(code_unit(workspace, 1, ["read"]))
    units.append(ai_unit(workspace, "U-01-ODDLINES", 1))
    units.append(checkpoint_unit("a", blocks=not prose))

    # Step 2: the story plan.
    if not prose:
        size = int(workspace.constant("event_unit_scenes", 10))
        for group in [order[index:index + size] for index in range(0, len(order), size)]:
            units.append(ai_unit(workspace, f"U-02-{group[0]}..{group[-1]}", 2, scenes=group))
        units.append(ai_unit(workspace, "U-02-FILM", 2, scenes=list(order)))
        if compressing(workspace):
            units.append(ai_unit(workspace, "U-02-COMPRESS", 2, scenes=list(order)))
    else:
        chapters = workspace.chapter_order()
        for chapter in chapters:
            units.append(ai_unit(workspace, f"U-02-{chapter}", 2, chapters=[chapter]))
        units.append(ai_unit(workspace, "U-02-BOOK", 2, chapters=list(chapters)))
        units.append(checkpoint_unit("p"))
        sizes = workspace.constant("outline_chapters_per_unit", [2, 3])
        most = max(sizes) if isinstance(sizes, list) else int(sizes)
        for number, group in enumerate(balanced_chunks(chapters, most), start=1):
            units.append(ai_unit(workspace, f"U-02-OUTLINE-P{number}", 2, chapters=group))

    # Step 3: world and style.
    units.append(ai_unit(workspace, "U-03-WORLD", 3))

    # Step 4: motifs first, then each principal, the minor characters, the places, the things.
    units.append(ai_unit(workspace, "U-04-MOTIFS", 4))
    principals, minors = principal_characters(workspace)
    for character in principals:
        units.append(ai_unit(workspace, f"U-04-{character}", 4, characters=[character]))
    for number, group in enumerate(balanced_chunks(minors, int(workspace.constant("minor_characters_per_unit", 4))),
                                   start=1):
        units.append(ai_unit(workspace, f"U-04-MINOR-P{number}", 4, characters=group))
    for number, group in enumerate(balanced_chunks(places_of_scenes(workspace),
                                                   int(workspace.constant("places_per_unit", 2))), start=1):
        units.append(ai_unit(workspace, f"U-04-PLACES-P{number}", 4, places=group))
    units.append(ai_unit(workspace, "U-04-THINGS", 4))

    # Step 5: continuity, then checkpoint B.
    if not prose:
        size = int(workspace.constant("continuity_unit_scenes", 5))
        for group in [order[index:index + size] for index in range(0, len(order), size)]:
            units.append(ai_unit(workspace, f"U-05-{group[0]}..{group[-1]}", 5, scenes=group))
    else:
        for sequence in workspace.records("SEQUENCE"):
            scenes = [scene for scene in expand_range(sequence.get("scenes"), order) if scene in order]
            units.append(ai_unit(workspace, f"U-05-{sequence.identifier}", 5, scenes=scenes,
                                 sequence=sequence.identifier))
    units.append(checkpoint_unit("b"))

    # Step 6: film rules, in three units.
    for name in ("CAMERA", "LOOKS", "PLANS"):
        units.append(ai_unit(workspace, f"U-06-{name}", 6))

    # Steps 7 and 8, sequence by sequence.
    stop_each = bool((workspace.manifest.get("checkpoints") or {}).get("stop_after_each_group"))
    for index, (sequence, scenes) in enumerate(sequence_groups(workspace)):
        for scene in scenes:
            if scene_is_big(workspace, scene):
                split = part_line_split(workspace, scene)
                lines = workspace.scene_lines(scene)
                part_lines = [(lines[0], split - 1), (split, lines[1])] if lines and split else [None, None]
                units.append(ai_unit(workspace, f"U-07-{scene}-P1", 7, scenes=[scene], sequence=sequence, part=1,
                                     lines=part_lines[0]))
                units.append(ai_unit(workspace, f"U-07-{scene}-P2", 7, scenes=[scene], sequence=sequence, part=2,
                                     lines=part_lines[1]))
                units.append(ai_unit(workspace, f"U-07-{scene}-LIST", 7, scenes=[scene], sequence=sequence,
                                     list_unit=True))
            else:
                units.append(ai_unit(workspace, f"U-07-{scene}", 7, scenes=[scene], sequence=sequence))
        units.append(checkpoint_unit("c", identifier=f"CHECKPOINT-C-{sequence or scenes[0]}",
                                     blocks=(index == 0 or stop_each), first_group=(index == 0), scenes=list(scenes),
                                     sequence=sequence))
        for scene in scenes:
            if DEPTH_RANK_OF[workspace.scene_depth(scene)] < DEPTH_RANK_OF["standard"]:
                continue
            batches = plan_batches(workspace, scene)
            if not batches:
                units.append(ai_unit(workspace, f"U-08-{scene}-B1", 8, scenes=[scene], sequence=sequence, batch=1,
                                     note="planned once the scene's one-line list exists"))
            for unit_identifier, shots in batches:
                units.append(ai_unit(workspace, unit_identifier, 8, scenes=[scene], sequence=sequence,
                                     batch=batch_number(unit_identifier), shots=shots))

    # Step 9: the film pass.
    scenes_in_scope = [scene for _, group in sequence_groups(workspace) for scene in group]
    units.append(code_unit(workspace, 9, ["check --film"]))
    if workspace.depth != "quick":
        parts = film_strip_parts(workspace)
        if parts:
            for number, name in enumerate(parts, start=1):
                units.append(ai_unit(workspace, f"U-09-JUDGE-A{number}", 9, scenes=scenes_in_scope, act=number,
                                     strip_file=name))
        else:
            units.append(ai_unit(workspace, "U-09-JUDGE", 9, scenes=scenes_in_scope, strip_file=FILM_STRIP_FILE))

    # Step 10: check and estimate, the review questions, the scores, the finished check.
    units.append(code_unit(workspace, 10, ["export book", "check --all", "compile --lint-only",
                                           "estimate --version v1", "questions --sample"]))
    for unit_identifier in question_units(workspace):
        units.append(ai_unit(workspace, unit_identifier, 10, scenes=scenes_in_scope))
    units.append(ai_unit(workspace, "U-10-SCORES", 10, scenes=scenes_in_scope))
    units.append(checkpoint_unit("acceptance"))

    # Step 11: the book and the exports.
    units.append(code_unit(workspace, 11, ["export all"]))
    return units


def original_story_note(workspace):
    """Where the story is for the welcome's one finished shot line (step 0 reads enough of it to find a strong turn)."""
    folder = workspace.folder / "Original"
    stories = [path.name for path in sorted(folder.glob("*")) if path.is_file() and "fingerprint" not in path.name] \
        if folder.is_dir() else []
    if stories:
        return f"read enough of the story (Original/{stories[0]}) to pick one strong turn for the welcome's example shot"
    return "read enough of the story to pick one strong turn for the welcome's example shot"


def compressing(workspace):
    """True when the user set a shorter target at checkpoint A (runtime_target_s is a number)."""
    value = workspace.project_value("runtime_target_s")
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


# ---------------------------------------------------------------- which units are done

def open_asked_choices(workspace, checkpoint):
    """The choices a checkpoint waits for: asked (not small choices), still open, shown at this checkpoint."""
    waiting = []
    for choice in workspace.records("CHOICE"):
        if normalise_word(choice.get("status") or "open") != "open":
            continue
        if normalise_word(choice.get("asked") or "no") != "yes":
            continue
        where = normalise_word(choice.get("checkpoint") or "none")
        if checkpoint == "rights":
            affects = [piece.strip() for piece in split_list(choice.get("affects") or "")]
            if "PROJECT.rights" in affects or choice.identifier == "CHOICE-001":
                waiting.append(choice)
        elif where == checkpoint:
            waiting.append(choice)
    return waiting


def newest_record_change(workspace):
    """The time the newest record file changed (a code unit done before it is done again)."""
    times = []
    for record_file in workspace.record_files:
        path = workspace.folder / record_file.name
        if path.is_file() and record_file.name != HEALTH_CHECK_FILE and record_file.name != WHOLE_FILM_FILE:
            times.append(path.stat().st_mtime)
    return max(times) if times else 0


def file_is_fresh(workspace, relative_path):
    path = workspace.folder / relative_path
    return path.is_file() and path.stat().st_mtime >= newest_record_change(workspace)


def evidence_of(workspace, unit):
    """True when the records (or the files code writes) show that a unit's work is there."""
    identifier = unit.identifier
    records = workspace.records
    if unit.kind == "code":
        if identifier == "U-00-SELFTEST":
            return False
        commands = unit.commands
        if commands == ["read"]:
            return workspace.story_read()
        if commands == ["check --film"]:
            return file_is_fresh(workspace, f"{MACHINE_FOLDER}/{FILM_STRIP_FILE}") and \
                (workspace.folder / WHOLE_FILM_FILE).is_file()
        if "questions --sample" in commands:
            return bool(workspace.manifest.get("questions")) or \
                (workspace.project.machine_folder / QUESTIONS_FILE).is_file()
        if commands == ["export all"]:
            return file_is_fresh(workspace, BOOK_FILE)
        return False
    if identifier == "U-00-START":
        return not open_asked_choices(workspace, "rights")
    if identifier.startswith("U-02-") and SCENE_RANGE.match(identifier[5:]):
        return all(workspace.record(scene, "SCENE") is not None and workspace.record(scene, "SCENE").get("event")
                   for scene in unit.scenes)
    if identifier == "U-02-FILM":
        plan = workspace.singleton("PLAN")
        return plan is not None and bool(plan.get("climax"))
    if identifier == "U-02-COMPRESS":
        return bool(records("CARDINAL"))
    if identifier.startswith("U-02-CP"):
        chapter = workspace.record(unit.chapters[0], "CHAPTER") if unit.chapters else None
        return chapter is not None and bool(chapter.get("digest"))
    if identifier == "U-02-BOOK":
        plan = workspace.singleton("PLAN")
        return bool(records("STRAND")) or (plan is not None and bool(plan.get("plan_option")))
    if identifier == "U-03-WORLD":
        return workspace.singleton("STYLE") is not None and workspace.singleton("WORLD") is not None
    if identifier == "U-04-MOTIFS":
        return bool(records("MOTIF"))
    if identifier.startswith("U-04-") and unit.characters:
        return all(workspace.record(character, "CHARACTER") is not None
                   and workspace.record(character, "CHARACTER").get("fixed_description")
                   for character in unit.characters)
    if identifier.startswith("U-04-PLACES"):
        known = set()
        for location in records("LOCATION"):
            for value in location.get_all("headings"):
                known.update(place_key(piece) for piece in split_list(value))
            known.add(place_key(location.title))
        return bool(unit.places) and all(place_key(place) in known or any(
            place_key(place) in name or name in place_key(place) for name in known if name) for place in unit.places)
    if identifier == "U-04-THINGS":
        return bool(records("PROP")) or bool(records("TEXT"))
    if identifier.startswith("U-05-"):
        scenes = set(unit.scenes)
        for state in records("STATE"):
            item = split_item(state.get("from") or "")
            if item.first in scenes:
                return True
        return False
    if identifier == "U-06-CAMERA":
        return workspace.singleton("CAMSYS") is not None
    if identifier == "U-06-LOOKS":
        return bool(records("LOOK"))
    if identifier == "U-06-PLANS":
        return workspace.singleton("LADDER") is not None or workspace.singleton("SOUNDPLAN") is not None
    if unit.step == 7:
        scene = unit.scene
        listed = workspace.record(f"{scene}-LIST", "SHOTLIST")
        if listed is not None and listed.get_all("item"):
            return True
        if unit.part:
            return workspace.record(f"{scene}-P{unit.part}", "PART") is not None
        return False
    if unit.step == 8:
        return bool(unit.shots) and all(workspace.record(shot, "SHOT") is not None for shot in unit.shots)
    return False


def checkpoint_passed(workspace, unit):
    """(passed, choices it waits for) for a checkpoint."""
    passed_before = (workspace.manifest.get("checkpoints") or {}).get(unit.identifier)
    if unit.checkpoint == "c":
        if passed_before:
            return True, []
        lists = [workspace.record(f"{scene}-LIST", "SHOTLIST") for scene in unit.scenes]
        if lists and all(record is not None and normalise_word(record.get("approved") or "") == "yes"
                         for record in lists):
            return True, []
        return False, []
    waiting = open_asked_choices(workspace, unit.checkpoint)
    if unit.checkpoint == "acceptance":
        return bool(passed_before) and not waiting, waiting
    return not waiting, waiting


def mark_done(workspace, units):
    """Set unit.done (and unit.waiting for checkpoints) on every planned unit.

    A unit is done when the manifest lists it among the units applied, or its records are there. Steps 0 to 6 run
    once each, in order: when any later unit's work is there, every earlier unit of steps 0 to 6 counts as done (a
    folder adopted from a chat app has records but no list of units). A checkpoint followed by work that is there
    counts as passed. Code units never make earlier units count as done.
    """
    applied = workspace.units_done()
    for unit in units:
        unit.waiting = []
        if unit.kind == "checkpoint":
            unit.done, unit.waiting = checkpoint_passed(workspace, unit)
        else:
            unit.done = unit.identifier in applied or evidence_of(workspace, unit)
        unit.own_evidence = unit.done and unit.kind == "ai"
    moved_past = False
    for unit in reversed(units):
        if unit.own_evidence or (unit.kind == "ai" and unit.identifier in applied):
            if unit.step >= 1:
                moved_past = True
            continue
        if moved_past and unit.step <= 6:
            # the self-test, the reading and the checkpoints of steps 0 to 6 lie behind work that is there
            unit.done = True
    # A checkpoint of steps 7 and later counts as passed when a unit after it in its own loop is done.
    for position, unit in enumerate(units):
        if unit.kind == "checkpoint" and unit.checkpoint == "c" and not unit.done:
            later = [other for other in units[position + 1:] if other.step == 8 and other.sequence == unit.sequence
                     and set(other.scenes) <= set(unit.scenes)]
            if any(other.done for other in later):
                unit.done = True
    return units


# ---------------------------------------------------------------- the next unit

def find_next_unit(workspace, pass_reported_checkpoints=False):
    """(the next unit or None, [checkpoints passed on the way that only report]).

    A checkpoint that does not wait (every group of shots after the first) is passed on the way; with
    pass_reported_checkpoints its shot lists are marked approved ("reported without changes")."""
    units = mark_done(workspace, workspace.plan())
    reported = []
    for unit in units:
        if unit.done:
            continue
        if unit.kind == "checkpoint" and not unit.blocks:
            reported.append(unit)
            if pass_reported_checkpoints:
                pass_checkpoint(workspace, unit, "reported without changes")
            continue
        return unit, reported
    return None, reported


def next_unit(project_folder):
    """One plain line naming the next unit, for stage.py status. Never writes anything."""
    try:
        workspace = Workspace(project_folder)
        unit, _ = find_next_unit(workspace)
    except StageStop as stop:
        return stop.message
    except Exception as error:  # status must still print; the command next says more
        return f"run stage.py next (the plan could not be worked out here: {type(error).__name__})."
    if unit is None:
        return "nothing left in the 12 steps; the add-ons run on request."
    if unit.kind == "checkpoint":
        return f"{unit.plain(workspace.steps)}, a checkpoint that waits for the user (run stage.py next)."
    if unit.kind == "code":
        return unit.plain(workspace.steps) + ": " + ", then ".join(f"stage.py {command}"
                                                                 for command in unit.commands) + "."
    return f"{unit.identifier}, {unit.plain(workspace.steps)} (stage.py next builds its handout)."


def pass_checkpoint(workspace, unit, how):
    """Record a checkpoint as passed; for a group of shots, mark its scenes' shot lists approved (code keeps
    SHOTLIST approved: the user passed the group, or it was reported without changes)."""
    changed = []
    if unit.checkpoint == "c":
        history = None
        for scene in unit.scenes:
            shot_list = workspace.record(f"{scene}-LIST", "SHOTLIST")
            if shot_list is None or normalise_word(shot_list.get("approved") or "") == "yes":
                continue
            for record_file in workspace.record_files:
                copy = record_file.find("SHOTLIST", f"{scene}-LIST")
                if copy is None:
                    continue
                path = workspace.folder / record_file.name
                history = history or history_run_folder(workspace.project)
                keep_in_history(history, path, record_file.name)
                copy.set_field("approved", "yes", workspace.schema)
                write_file(record_file, path, workspace.schema)
                changed.append(record_file.name)
                break
    with workspace.project.lock():
        manifest = workspace.project.read_manifest()
        manifest.setdefault("checkpoints", {})[unit.identifier] = {"passed": now(), "how": how}
        workspace.project.write_manifest(manifest)
        workspace.manifest = manifest
    if changed:
        workspace.project.add_log_entry(
            f"Passed {CHECKPOINT_NAMES.get(unit.checkpoint, 'a checkpoint')} for "
            f"{scene_group_words(unit.scenes)} ({how}): the shot lists are approved.")
        # the records changed: read them again
        refreshed = Workspace(workspace.folder, workspace.schema, workspace.words, workspace.constants,
                              workspace.skill_folder, workspace.limits)
        workspace.__dict__.update(refreshed.__dict__)
    return changed


# ---------------------------------------------------------------- finding a unit by its ID

def unit_from_identifier(workspace, identifier):
    """The unit with this ID: from the plan when it is there, else made from its steps.json pattern (a redo, an
    add-on, a scene outside the scope). Stops with a plain line when the ID is not a unit."""
    identifier = identifier.strip()
    for unit in workspace.plan():
        if unit.identifier == identifier:
            return unit
    match = UNIT_IDENTIFIER.match(identifier)
    if not match:
        raise StageStop(f'"{identifier}" is not a unit ID. Unit IDs look like U-07-SC10 or U-08-SC10-B2; '
                        "stage.py next names the next one.")
    step = int(match.group(1))
    scope = match.group(2)
    entry = workspace.step_entry(step)
    if not entry:
        raise StageStop(f"There is no step {step}: steps run from 0 to 16 (steps/ and schema/steps.json).")
    entry_of_unit = unit_entry_for(workspace, step, identifier)
    if entry_of_unit is None:
        patterns = [unit.get("id_pattern") for unit in entry.get("units", [])
                    if not unit.get("id_pattern", "").startswith("code:")]
        raise StageStop(f"{identifier} is not a unit of step {step}. Its units look like: "
                        + ", ".join(patterns) + ".")
    unit = Unit(identifier=identifier, step=step, entry_of_unit=entry_of_unit)
    order = workspace.scene_order()
    scene_match = SCENE_PREFIX.match(scope)
    range_match = SCENE_RANGE.match(scope)
    if range_match:
        unit.scenes = expand_range(scope, order) or [range_match.group(1), range_match.group(2)]
    elif scene_match:
        unit.scenes = [scene_match.group(1)]
        rest = scope[len(scene_match.group(1)):]
        if re.match(r"^-P(\d+)$", rest):
            unit.part = int(rest[2:])
        elif rest == "-LIST":
            unit.list_unit = True
        elif re.match(r"^-B(\d+)$", rest):
            unit.batch = int(rest[2:])
            for batch_identifier, shots in plan_batches(workspace, unit.scene):
                if batch_identifier == identifier:
                    unit.shots = shots
            if not unit.shots:
                raise StageStop(f"{identifier} is not one of the batches planned for {scene_words(unit.scene)}: "
                                + (", ".join(name for name, _ in plan_batches(workspace, unit.scene))
                                   or "the scene has no one-line shot list yet, so no batch is planned") + ".")
    elif re.match(r"^TAKES-(SC\d{2,3}[A-Z]?)$", scope):
        unit.scenes = [scope[len("TAKES-"):]]
    elif re.match(r"^CP\d{2,3}$", scope):
        unit.chapters = [scope]
    elif re.match(r"^SQ\d{2,3}$", scope):
        unit.sequence = scope
        sequence = workspace.record(scope, "SEQUENCE")
        unit.scenes = expand_range(sequence.get("scenes") if sequence else "", order)
    elif re.match(r"^CH-", scope):
        unit.characters = [scope]
    if unit.scenes:
        for scene in unit.scenes:
            if scene not in order and workspace.story_scene(scene) is None:
                raise StageStop(f"{scene_words(scene).capitalize()} is not in this project; its scenes are "
                                f"{scene_group_words(order)}.")
        if unit.step in (7, 8) and not unit.sequence:
            record = workspace.record(unit.scene, "SCENE")
            unit.sequence = record.get("sequence") if record is not None else None
    if unit.step == 7 and unit.part and unit.scene:
        split = part_line_split(workspace, unit.scene)
        lines = workspace.scene_lines(unit.scene)
        if lines and split:
            unit.lines = (lines[0], split - 1) if unit.part == 1 else (split, lines[1])
    return unit


# ---------------------------------------------------------------- the pieces of a handout

@dataclass
class Section:
    """One part of a handout: its text and what may happen to it when the handout is too big."""
    key: str
    text: str
    kind: str = "fixed"                   # fixed | card | example | source
    label: str = ""
    trimmed_text: str = None              # source: the unit's own lines only
    left_out: bool = False
    trimmed: bool = False

    def current_text(self):
        if self.left_out:
            return ""
        if self.trimmed and self.trimmed_text is not None:
            return self.trimmed_text
        return self.text


@dataclass
class Handout:
    """A unit's handout, section by section, with its size in tokens."""
    unit: Unit
    ceiling: int
    tokens_per_word: float
    card_cap: int
    sections: list = dataclass_field(default_factory=list)
    notes: list = dataclass_field(default_factory=list)
    left_out: list = dataclass_field(default_factory=list)
    card_parts_left_out: list = dataclass_field(default_factory=list)
    issued: dict = dataclass_field(default_factory=dict)
    batches: dict = dataclass_field(default_factory=dict)
    too_big: bool = False
    task: str = ""

    def add(self, key, text, kind="fixed", label="", trimmed_text=None):
        if text is None or not str(text).strip():
            return None
        section = Section(key=key, text=str(text).rstrip() + "\n", kind=kind, label=label or key,
                          trimmed_text=(trimmed_text.rstrip() + "\n") if trimmed_text else None)
        self.sections.append(section)
        return section

    def text(self):
        return "\n".join(section.current_text() for section in self.sections if section.current_text()).rstrip() + "\n"

    def tokens(self):
        return estimate_tokens(self.text(), self.tokens_per_word)

    def card_tokens(self):
        return sum(estimate_tokens(section.current_text(), self.tokens_per_word)
                   for section in self.sections if section.kind == "card")

    def fit(self):
        """Keep the card parts within card_tokens_per_unit_max and the handout within its ceiling (6.1): leave out
        the example, then the lowest-listed card parts, then trim the story to the unit's lines, then say the unit
        must be split."""
        cards = [section for section in self.sections if section.kind == "card"]
        while self.card_tokens() > self.card_cap and [section for section in cards if not section.left_out]:
            lowest = [section for section in cards if not section.left_out][-1]
            lowest.left_out = True
            self.card_parts_left_out.append(lowest.label)
            self.left_out.append(f"{lowest.label} (card parts are capped at {number_with_commas(self.card_cap)} "
                                 "tokens, card_tokens_per_unit_max)")
        if not self.ceiling:
            return self
        if self.tokens() > self.ceiling:
            for section in self.sections:
                if section.kind == "example" and not section.left_out:
                    section.left_out = True
                    self.left_out.append(f"{section.label} (to fit the ceiling)")
        while self.tokens() > self.ceiling and [section for section in cards if not section.left_out]:
            lowest = [section for section in cards if not section.left_out][-1]
            lowest.left_out = True
            self.card_parts_left_out.append(lowest.label)
            self.left_out.append(f"{lowest.label} (to fit the ceiling)")
        if self.tokens() > self.ceiling:
            for section in self.sections:
                if section.kind == "source" and section.trimmed_text is not None and not section.trimmed:
                    section.trimmed = True
                    self.left_out.append("the story's lines outside this unit's own (to fit the ceiling)")
        if self.tokens() > self.ceiling:
            self.too_big = True
        return self


# ---------------------------------------------------------------- step files, cards, templates, examples

def step_file_parts(workspace, step_entry, keep_chat_twin=False):
    """(one-line task, the step file without its title, task lines and, on a code surface, its chat twin)."""
    path = workspace.skill_folder / (step_entry.get("step_file") or "")
    if not step_entry.get("step_file") or not path.is_file():
        task = step_entry.get("purpose") or f"Do the work of step {step_entry.get('step')}."
        return task, (f"The step file {step_entry.get('step_file') or ''} is not in this copy of the skill; its "
                      f"purpose from schema/steps.json: {step_entry.get('purpose', '')}")
    text = path.read_text(encoding="utf-8")
    task = ""
    kept = []
    skipping = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("**One-line task:**"):
            task = task or stripped[len("**One-line task:**"):].strip()
            continue
        if stripped.startswith("**One-line task, again:**"):
            continue
        if stripped.startswith("Quote the one-line task back"):
            continue
        if re.match(r"^# ", line) and not kept:
            continue
        if re.match(r"^## ", line):
            skipping = (not keep_chat_twin) and stripped.lower().startswith("## if you cannot run code")
        if skipping:
            continue
        kept.append(line)
    excerpt = re.sub(r"\n{3,}", "\n\n", "\n".join(kept).strip())
    return task or step_entry.get("purpose", ""), demote_headings(excerpt, 1)


def card_file_path(workspace, card_code):
    entry = (workspace.steps.get("cards") or {}).get(card_code) or {}
    if entry.get("file"):
        return workspace.skill_folder / entry["file"], entry
    return None, entry


def card_part_text(workspace, card_code, part_name):
    """(label, text) of one card part: its ## heading and the lines to the next ## heading (headings inside
    fenced code blocks do not count), or the whole card; None when the card or the part is missing."""
    path, entry = card_file_path(workspace, card_code)
    if path is None or not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("# ") else path.stem
    if part_name == "whole":
        body = "\n".join(lines[1:] if lines and lines[0].startswith("# ") else lines).strip()
        return f"{title} (whole)", body
    heading = ((entry.get("parts") or {}).get(part_name) or {}).get("heading")
    if not heading:
        return None
    collected = None
    in_fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not in_fence and line.startswith("## "):
            if collected is not None:
                break
            if line[3:].strip().lower() == heading.lower():
                collected = []
                continue
        if collected is not None:
            collected.append(line)
    if collected is None:
        return None
    return f'{title}, part "{heading}"', "\n".join(collected).strip()


def scene_tags(workspace, scene_identifier):
    scene = workspace.record(scene_identifier, "SCENE") if scene_identifier else None
    if scene is None:
        return []
    return [normalise_word(tag) for tag in split_list(scene.get("tags") or "") if normalise_word(tag) != "none"]


def mirror_rule_exists(workspace):
    return any(normalise_word(rule.get("kind") or "") == "mirror" for rule in workspace.records("RULE"))


def card_list(workspace, unit, step_entry):
    """The card parts a unit reads, in merge order (steps.json card_part_rules): a unit's own list when it has
    one; else, at steps 7 and 8, the depth's base list, the parts for the scene's tags, then the standard and
    detailed additions; else the step's parts for every depth and those whose condition holds."""
    cards = step_entry.get("cards") or {}
    entry_of_unit = unit.entry_of_unit or {}
    chosen = []
    if entry_of_unit.get("cards"):
        chosen = list(entry_of_unit["cards"])
    elif unit.step in (7, 8):
        depth = DEPTH_RANK_OF[workspace.scene_depth(unit.scene)] if unit.scene else DEPTH_RANK_OF[workspace.depth]
        base = cards.get("quick", []) if unit.step == 7 else cards.get("standard", [])
        chosen = list(base)
        for tag in scene_tags(workspace, unit.scene):
            chosen += (cards.get("by_tag") or {}).get(tag, [])
        if unit.step == 7 and depth >= DEPTH_RANK_OF["standard"]:
            chosen += cards.get("standard_adds", [])
        if depth >= DEPTH_RANK_OF["detailed"]:
            chosen += cards.get("detailed_adds", [])
    else:
        chosen = list(cards.get("all_depths", []))
        if cards.get("when_source_not_screenplay") and workspace.source_kind != "screenplay":
            chosen += cards["when_source_not_screenplay"]
        if cards.get("when_mirror_rule") and mirror_rule_exists(workspace):
            chosen += cards["when_mirror_rule"]
    unique = []
    for entry in chosen:
        key = (entry.get("card"), entry.get("part"))
        if key not in unique:
            unique.append(key)
    return unique


def template_blocks(workspace):
    """{(template file name, record type): the template's record block with its note block}."""
    blocks = {}
    folder = workspace.skill_folder / "templates"
    if not folder.is_dir():
        return blocks
    for path in sorted(folder.glob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        current_type, current = None, []
        for line in lines:
            match = re.match(r"^### ([A-Z]+)\b", line)
            if match or line.startswith("END OF FILE"):
                if current_type:
                    blocks[(path.name, current_type)] = "\n".join(current).rstrip()
                current_type, current = (match.group(1), [line]) if match else (None, [])
                continue
            if current_type:
                current.append(line)
        if current_type:
            blocks[(path.name, current_type)] = "\n".join(current).rstrip()
    return blocks


def template_for(workspace, type_name, step):
    blocks = template_blocks(workspace)
    preferred = []
    if type_name in ("SCENE",):
        preferred = ["11 Scene.md"] if step in (7, 8) else ["04 Scene list.md"]
    for name in preferred:
        if (name, type_name) in blocks:
            return blocks[(name, type_name)]
    for (name, kind), text in blocks.items():
        if kind == type_name:
            return text
    return None


def filter_template(text, depth_rank, code_surface, add_on=False):
    """A template block at the project's depth: field lines marked for a deeper depth are left out, so are the
    add-on fields outside the add-on steps, and on a code surface the lines code writes (status, locked); notes and
    the 'code adds these' line stay."""
    kept = []
    for line in text.splitlines():
        if not add_on and re.match(r"^- [a-z_]+: <add-on\b", line):
            continue
        match = re.match(r"^- [a-z_]+: <(quick|standard|detailed|optional)\b(.*)$", line)
        if match:
            level = match.group(1)
            if level in DEPTH_OF_HINT and DEPTH_OF_HINT[level] > depth_rank:
                continue
            if code_surface and "code writes it" in match.group(2):
                continue
        kept.append(line)
    return "\n".join(kept).rstrip()


def written_types(unit, workspace):
    """The record types a unit writes (steps.json 'writes'), without prose-only types in a screenplay."""
    types = []
    for text in ((unit.entry_of_unit or {}).get("writes") or []):
        match = re.match(r"^([A-Z]+)\b", text)
        if not match or not workspace.schema.knows_type(match.group(1)):
            continue
        if "prose only" in text and not workspace.is_prose:
            continue
        if match.group(1) not in types:
            types.append(match.group(1))
    return types


def gold_records(workspace):
    """The gold example's records (scene 10 and its context), merged by ID, or {} when the files are absent."""
    files = []
    for relative in (GOLD_SCENE_FILE, GOLD_CONTEXT_FILE):
        path = workspace.skill_folder / relative
        if path.is_file():
            files.append(parse_file(path, Path(relative).name, workspace.schema))
    if not files:
        return {}
    merged, _ = merge_copies(files, workspace.schema)
    return merged


# ---------------------------------------------------------------- showing records

def record_heading(record):
    parts = ["###", record.type_name]
    if record.identifier:
        parts.append(record.identifier)
    if record.title:
        parts.append(record.title)
    return " ".join(parts)


def is_code_field(workspace, type_name, field_name):
    """True for what code keeps or works out and the AI never types: status, locks, approval, derived fields."""
    if field_name in CODE_KEPT_FIELDS:
        return True
    definition = workspace.schema.field(type_name, field_name) or {}
    if definition.get("stored") is False:
        return True
    return workspace.schema.writers(definition) == ["code_derived"] if definition else False


def record_text(workspace, record, fields=None, item_filter=None):
    """A record as record text for a handout: its heading and field lines, without what code keeps (status,
    locks, approval, derived fields) and without the ' = <beat>' endings code adds to story points. fields keeps
    only those fields (in the record's own order); item_filter(name, value) may leave out single items."""
    lines = [record_heading(record)]
    for line in record.fields:
        if fields is not None and line.name not in fields:
            continue
        if is_code_field(workspace, record.type_name, line.name):
            continue
        if line.missing:
            continue
        if item_filter is not None and not item_filter(line.name, line.value):
            continue
        lines.append(f"- {line.name}: {strip_story_point_endings(line.value.strip())}")
    return "\n".join(lines)


def records_block(workspace, records, fields=None, item_filter=None):
    texts = [record_text(workspace, record, fields, item_filter) for record in records if record is not None]
    return fenced("\n\n".join(texts)) if texts else ""


def brief_line(workspace, record):
    fields = BRIEF_FIELDS.get(record.type_name)
    if fields is None:
        fields = [line.name for line in record.fields
                  if not is_code_field(workspace, record.type_name, line.name)][:3]
    return record_text(workspace, record, fields)


# ---------------------------------------------------------------- IDs issued to a unit

def highest_number(workspace, prefix):
    """The highest number used by records (and IDs declared in items) whose ID is prefix + digits."""
    highest = 0
    expression = re.compile("^" + re.escape(prefix) + r"(\d+)$")
    for (_, identifier) in workspace.index:
        match = expression.match(identifier or "")
        if match:
            highest = max(highest, int(match.group(1)))
    return highest


def pending_block_end(workspace, type_name, prefix, own_unit):
    """The highest number in blocks of this type issued to units not yet applied (other than own_unit)."""
    applied = workspace.units_done()
    highest = 0
    for unit, blocks in (workspace.manifest.get("issued") or {}).items():
        if unit == own_unit or unit in applied:
            continue
        pairs = (blocks or {}).get(type_name) or []
        if pairs and isinstance(pairs[0], str):
            pairs = [pairs]
        for pair in pairs:
            if isinstance(pair, (list, tuple)) and len(pair) == 2:
                match = re.match("^" + re.escape(prefix) + r"(\d+)$", str(pair[1]))
                if match:
                    highest = max(highest, int(match.group(1)))
    return highest


def id_width(workspace, type_name, default=2):
    """How many digits an ID of this type ends with, from its pattern in schema.json."""
    record_type = workspace.schema.record_types.get(type_name) or {}
    pattern = record_type.get("id_pattern") or ""
    match = re.search(r"\\d\{(\d+)(?:,(\d+))?\}\$?$", pattern)
    if match:
        return int(match.group(1))
    if re.search(r"\\d\$?$", pattern):
        return 1
    return default


def numbered_block(workspace, unit, type_name, prefix, size=None, width=None):
    """[first, last] of the next free numbers of a numbered ID type (CHOICE-017 to CHOICE-036), after every
    number used and every number issued to a unit not yet applied."""
    width = width or id_width(workspace, type_name)
    start = max(highest_number(workspace, prefix),
                pending_block_end(workspace, type_name, prefix, unit.identifier)) + 1
    most = 10 ** width - 1
    last = most if size is None else min(most, start + size - 1)
    return [f"{prefix}{start:0{width}d}", f"{prefix}{last:0{width}d}"]


def scene_blocks(workspace, unit):
    """The blocks a step-7 unit is given for its scene (blueprint 3, step 7; constant issued_blocks)."""
    scene = unit.scene
    blocks = workspace.constant("issued_blocks", {"beats": [1, 30], "shots": [10, 400]})
    step_size = int(workspace.constant("shot_number_step", 10))
    end_cards = workspace.constant("end_card_numbers", [990, 999])
    beats = blocks.get("beats", [1, 30])
    shots = blocks.get("shots", [10, 400])
    beat_width = id_width(workspace, "BEAT")
    issued = {
        "BEAT": [f"{scene}-B{beats[0]:0{beat_width}d}", f"{scene}-B{beats[1]:0{beat_width}d}"],
        "PART": [f"{scene}-P1", f"{scene}-P{10 ** id_width(workspace, 'PART', 1) - 1}"],
        "VALUE": [f"{scene}-V1", f"{scene}-V9"],
        "MOVE": [f"{scene}-M{1:0{id_width(workspace, 'MOVE')}d}",
                 f"{scene}-M{10 ** id_width(workspace, 'MOVE') - 1}"],
        "SETUP": [f"{scene}-SU{1:0{id_width(workspace, 'SETUP')}d}",
                  f"{scene}-SU{10 ** id_width(workspace, 'SETUP') - 1}"],
        "SHOT": [[f"{scene}-SH{shots[0]:03d}", f"{scene}-SH{shots[1]:03d}"],
                 [f"{scene}-SH{end_cards[0]:03d}", f"{scene}-SH{end_cards[1]:03d}"]],
        # A cut takes the number of the shot it follows, so the scene's cuts share the shots' numbers.
        "CUT": [f"{scene}-C{shots[0]:03d}", f"{scene}-C{end_cards[1]:03d}"],
    }
    return issued, step_size, end_cards


def next_free_in_scene(workspace, scene, type_name, marker, width):
    highest = 0
    expression = re.compile("^" + re.escape(f"{scene}-{marker}") + r"(\d+)$")
    for (kind, identifier) in workspace.index:
        match = expression.match(identifier or "")
        if match and kind == type_name:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def issued_ids(workspace, unit):
    """({TYPE: [first, last] or [[first, last], ...]} for the manifest (ID-06), [plain lines for the handout])."""
    issued = {}
    lines = []
    step = unit.step
    choice_block = numbered_block(workspace, unit, "CHOICE", "CHOICE-", ISSUED_BLOCK_SIZE, 3)

    def add_choices():
        issued["CHOICE"] = choice_block
        lines.append(f"- Choices: {choice_block[0]} to {choice_block[1]}, in order; a set value takes its choice's "
                     "number and the option letter (CHOICE-017-A).")

    if step == 7 and unit.scene:
        scene = unit.scene
        blocks, step_size, end_cards = scene_blocks(workspace, unit)
        beat_width = id_width(workspace, "BEAT")
        if unit.part == 2:
            start = next_free_in_scene(workspace, scene, "BEAT", "B", beat_width)
            lines.append(f"- Beats: {scene}-B{start:0{beat_width}d} to {blocks['BEAT'][1]} (part 1 used the numbers "
                         "before), in story order.")
            lines.append(f"- Parts: {scene}-P2 for this part.")
        else:
            lines.append(f"- Beats: {blocks['BEAT'][0]} to {blocks['BEAT'][1]}, in story order; use as many as the "
                         "scene needs.")
            lines.append(f"- Parts: {blocks['PART'][0]} on, one per part with its own turn."
                         + (" This unit writes part 1 only." if unit.part == 1 else ""))
        if not unit.list_unit:
            lines.append(f"- Values (the first part of each SCENE value item): {blocks['VALUE'][0]} to "
                         f"{blocks['VALUE'][1]}.")
            move_start, setup_start = 1, 1
            if unit.part == 2:
                move_start = next_free_in_scene(workspace, scene, "MOVE", "M", id_width(workspace, "MOVE"))
                setup_start = next_free_in_scene(workspace, scene, "SETUP", "SU", id_width(workspace, "SETUP"))
            lines.append(f"- Floor-plan moves: {scene}-M{move_start:02d} on (to {blocks['MOVE'][1]}); setups "
                         f"(cameras, shown to the user as camera A, B, C ...): {scene}-SU{setup_start:02d} on (to "
                         f"{blocks['SETUP'][1]})" + ("; part 1 used the numbers before." if unit.part == 2 else "."))
        if unit.part is None or unit.list_unit:
            lines.append(f"- Shots (the first part of each SHOTLIST item): {blocks['SHOT'][0][0]} to "
                         f"{blocks['SHOT'][0][1]} in steps of {step_size} (shot_number_step; an insert added later "
                         f"takes a number between); end cards and black: {blocks['SHOT'][1][0]} to "
                         f"{blocks['SHOT'][1][1]} (end_card_numbers).")
            for card in (workspace.story_scene(scene) or {}).get("cards", []):
                lines.append(f"  - {card.get('shot')}: the card \"{card.get('text')}\" at line {card.get('line')} "
                             f"({card.get('kind', 'a card')}); list it as its own shot.")
        issued.update(blocks)
        add_choices()
    elif step == 8 and unit.scene:
        scene = unit.scene
        shots = unit.shots
        issued["SHOT"] = [shots[0], shots[-1]] if shots else []
        numbers = [shot_number(shot) for shot in shots if shot_number(shot) is not None]
        if numbers:
            issued["CUT"] = [f"{scene}-C{min(numbers):03d}", f"{scene}-C{max(numbers):03d}"]
        lines.append(f"- Shots: exactly these list items, one SHOT each, never added, dropped or renumbered: "
                     + ", ".join(shots) + ".")
        if numbers:
            lines.append(f"- Cuts: a CUT takes the number of the shot it follows ({scene}-C{min(numbers):03d} to "
                         f"{scene}-C{max(numbers):03d}); only where the join is not a plain cut.")
        lines.append("- Grey preview stubs (PREVIS) are named by code; name one only in time_slice or "
                     "shared_geometry.")
    elif step == 2:
        for type_name, prefix in (("SEQUENCE", "SQ"), ("PLANT", "PL-"), ("FACT", "FT-")):
            block = numbered_block(workspace, unit, type_name, prefix, None, 2)
            issued[type_name] = block
            lines.append(f"- {workspace.schema.record_types.get(type_name, {}).get('plain_name', type_name).capitalize()}"
                         f": {block[0]} onward.")
        if workspace.is_prose:
            for type_name, prefix in (("STRAND", "ST-"), ("CARDINAL", "CF-")):
                block = numbered_block(workspace, unit, type_name, prefix, None, 2)
                issued[type_name] = block
                lines.append(f"- {workspace.schema.record_types.get(type_name, {}).get('plain_name', type_name).capitalize()}"
                             f": {block[0]} onward.")
            if unit.identifier.startswith("U-02-OUTLINE"):
                digits = scene_id_digits_of(workspace)
                start = max([int(scene[2:2 + digits]) for scene in workspace.scene_order()
                             if re.match(r"^SC\d+$", scene)] + [0]) + 1
                first = f"SC{start:0{digits}d}"
                issued["SCENE"] = [first, f"SC{10 ** digits - 1}"]
                lines.append(f"- Scenes of the step outline: {first} onward, in screen order (3 digits when the plan "
                             "has more than scene_ids_three_digits_above scenes).")
        elif unit.identifier == "U-02-COMPRESS":
            block = numbered_block(workspace, unit, "CARDINAL", "CF-", None, 2)
            issued["CARDINAL"] = block
            lines.append(f"- Cardinal events: {block[0]} onward.")
        add_choices()
    elif step == 6:
        for type_name, prefix, words in (("RESERVE", "RC-", "Saved choices"), ("LENS", "LX-", "Lens exceptions")):
            block = numbered_block(workspace, unit, type_name, prefix, None, 2)
            issued[type_name] = block
            lines.append(f"- {words}: {block[0]} onward.")
        add_choices()
    elif step in (9, 10):
        size = int(workspace.constant("question_batch_size", 40)) if "QUESTIONS" in unit.identifier \
            else ISSUED_BLOCK_SIZE
        block = numbered_block(workspace, unit, "FINDING", "FIND-", size, 3)
        issued["FINDING"] = block
        lines.append(f"- Findings: {block[0]} to {block[1]}, in order (the checker's own findings come before "
                     "them).")
        if unit.identifier == "U-10-SCORES" or "QUESTIONS" in unit.identifier:
            lines.append("- Reviews are named by what they score: RV- and the scene (RV-SC10), and RV-FILM.")
        add_choices()
    elif step in (12, 13, 14, 15):
        if step in (14, 15):
            block = numbered_block(workspace, unit, "RIGHTS", "RT-", ISSUED_BLOCK_SIZE, 3)
            issued["RIGHTS"] = block
            lines.append(f"- Rights records: {block[0]} to {block[1]}.")
        if step == 15:
            block = numbered_block(workspace, unit, "MUSIC", "MU-", None, 2)
            issued["MUSIC"] = block
            lines.append(f"- Music cues: {block[0]} onward.")
        add_choices()
    elif step in (1, 3, 4, 5, 0):
        add_choices()
    return issued, lines


# ---------------------------------------------------------------- what a scene unit reads

def characters_present(workspace, scene_identifier):
    scene = workspace.record(scene_identifier, "SCENE")
    found = []
    if scene is not None:
        found += [piece for piece in split_list(scene.get("characters") or "") if piece.startswith("CH-")]
        if scene.get("whose_scene"):
            found.append(scene.get("whose_scene"))
    story_scene = workspace.story_scene(scene_identifier) or {}
    found += story_scene.get("characters", [])
    for state in workspace.records("STATE"):
        element = state.get("element") or state.identifier.split(".S")[0]
        item = split_item(state.get("from") or "")
        if item.first == scene_identifier and element.startswith("CH-"):
            found.append(element)
    return [character for character in dict.fromkeys(found) if character]


def scene_text(workspace, scene_identifier):
    lines = workspace.scene_lines(scene_identifier)
    if not lines or workspace.story is None:
        return ""
    return "\n".join(workspace.story.line(number) for number in range(lines[0], lines[1] + 1))


def name_in_text(name, text):
    name = (name or "").strip().strip('"')
    if len(name) < 2:
        return False
    return re.search(r"(?<![\w])" + re.escape(name) + r"(?![\w])", text, re.IGNORECASE) is not None


def elements_in_scene(workspace, scene_identifier):
    """Every element present in a scene: characters, its place, elements with states in play, things its shots
    show, and things, texts and cameras whose names its lines hold."""
    found = list(characters_present(workspace, scene_identifier))
    try:
        from .derive_fields import elements_present
        found += elements_present(workspace.breakdown, scene_identifier)
    except Exception:  # the derived list only adds; the story's words below still find things
        pass
    text = scene_text(workspace, scene_identifier)
    for type_name in ("PROP", "TEXT", "CAMERA"):
        for record in workspace.records(type_name):
            names = []
            for value in record.get_all("names"):
                names += split_list(value)
            if type_name == "TEXT" and record.get("words"):
                names.append(record.get("words"))
            if text and any(name_in_text(name, text) for name in names):
                found.append(record.identifier)
    for motif in workspace.records("MOTIF"):
        for value in motif.get_all("appearance"):
            if scene_of(split_item(value).first or "") == scene_identifier:
                found.append(motif.identifier)
                break
    return [element for element in dict.fromkeys(found) if element]


def states_in_play(workspace, scene_identifier):
    try:
        from .derive_fields import states_in_play as derived_states
        return [workspace.record(identifier, "STATE") for identifier in derived_states(workspace.breakdown,
                                                                                       scene_identifier)]
    except Exception:  # without the derived list: the states that start in this scene
        return [state for state in workspace.records("STATE")
                if split_item(state.get("from") or "").first == scene_identifier]


def story_point_in_scene(value, scene_identifier):
    first = (value or "").strip().split(" ", 1)[0]
    return scene_of(first) == scene_identifier or first == scene_identifier


def scene_id_digits_of(workspace):
    """PROJECT scene_id_digits as a number (2 or 3); a value that is not a whole number (FORM-04 reports it) reads
    as 2, so a handout is still made."""
    try:
        return int(float(str(workspace.project_value("scene_id_digits", 2) or 2).strip()))
    except (TypeError, ValueError):
        return 2


def reserve_lines(workspace, scene_identifier, own_shots):
    """(records allowed here, plain lines) for the saved choices (RESERVE): each with how it is matched, where it
    is allowed, how many uses the film allows and how many are left outside this unit's own shots."""
    try:
        from . import film_pass
    except ImportError:
        return workspace.records("RESERVE"), []
    run = workspace.check_run
    digits = scene_id_digits_of(workspace)
    allowed_records, lines = [], []
    for reserve in workspace.records("RESERVE"):
        places = film_pass.read_places(reserve.get("allowed_in") or "", digits)
        allowed = True
        if places.not_before and sort_key_for_identifier(scene_identifier) < sort_key_for_identifier(places.not_before):
            allowed = False
        if places.identifiers or places.scenes:
            here = any(scene_of(identifier) == scene_identifier for identifier in places.identifiers) or any(
                film_pass.same_scene(scene_identifier, scene) for scene in places.scenes)
            allowed = allowed and here
        matched = film_pass.reserve_match(reserve)
        what = f"{matched[0]} = {matched[1]}" if matched else "by hand"
        uses = [record for record in (film_pass.reserve_uses(run, reserve) or [])
                if record.identifier not in own_shots]
        kind, most = film_pass.max_uses_of(reserve)
        if kind == "number":
            left = max(0, most - len(uses))
            count = f"at most {most} in the film; used {len(uses)} times outside this unit, {left} left"
        elif kind == "share":
            total = film_pass.film_scene_count(run)
            allowed_scenes = int(math.floor(most * total + 1e-9)) if total else 0
            used_scenes = sorted({scene_of(record.identifier) for record in uses})
            left = max(0, allowed_scenes - len(used_scenes))
            count = (f"in at most {seconds_text(most)} of the film's scenes ({allowed_scenes} of {total}); used in "
                     f"{len(used_scenes)} scenes outside this unit, {left} left")
        elif kind == "per_scene":
            count = "at most once in a scene"
        else:
            count = "uses as its record says"
        where = "allowed in this scene" if allowed else "not allowed in this scene"
        turn = {"main_turn": ", only on a main turn", "turn": ", only on a turn"}.get(places.turn, "")
        never = reserve.get("never_on")
        never_text = f"; never on {never}" if never and normalise_word(never) != "none" else ""
        lines.append(f"- {reserve.identifier} {reserve.get('choice') or reserve.title} (matched by {what}): "
                     f"{where}{turn if allowed else ''}; {count}{never_text}.")
        if allowed:
            allowed_records.append(reserve)
    return allowed_records, lines


def lens_exceptions_here(workspace, scene_identifier):
    found = []
    for lens in workspace.records("LENS"):
        places = split_list(lens.get("only_in") or "")
        if not places or any(scene_of(place) == scene_identifier or place == scene_identifier for place in places):
            found.append(lens)
    return found


def looks_for_scene(workspace, scene_identifier):
    scene = workspace.record(scene_identifier, "SCENE")
    looks = []
    if scene is not None and scene.get("look"):
        looks.append(workspace.record(scene.get("look"), "LOOK"))
    location = scene.get("location") if scene is not None else None
    for look in workspace.records("LOOK"):
        if location and look.get("for") == location and look not in looks:
            looks.append(look)
        elif any(story_point_in_scene(value, scene_identifier) for value in look.get_all("light_cue")) \
                and look not in looks:
            looks.append(look)
    return [look for look in looks if look is not None]


def location_for_scene(workspace, scene_identifier):
    scene = workspace.record(scene_identifier, "SCENE")
    if scene is not None and scene.get("location"):
        return workspace.record(scene.get("location"), "LOCATION")
    heading = workspace.scene_heading(scene_identifier) or ""
    place = scene.get("place_text") if scene is not None else ""
    for location in workspace.records("LOCATION"):
        for value in location.get_all("headings"):
            if any(place_key(piece) and place_key(piece) in place_key(heading + " " + (place or ""))
                   for piece in split_list(value)):
                return location
    return None


def has_set_plan(location):
    return location is not None and (location.get("size") or location.get_all("object") or location.get_all("mark"))


def previous_and_next(workspace, unit):
    """Lines about the scene before (its last shot, or its last list item inside the same sequence) and the heading
    of the scene after."""
    scene = unit.scene
    order = workspace.scene_order()
    lines = []
    if scene not in order:
        return lines
    position = order.index(scene)
    if position > 0:
        previous = order[position - 1]
        record = workspace.record(previous, "SCENE")
        same_sequence = record is not None and unit.sequence and record.get("sequence") == unit.sequence
        shots = [shot for shot in workspace.records("SHOT") if scene_of(shot.identifier) == previous]
        shots.sort(key=lambda shot: shot_number(shot.identifier) or 0)
        filmed = [shot for shot in shots if normalise_word(shot.get("kind") or "live") not in ("card", "black")]
        items = []
        shot_list = workspace.record(f"{previous}-LIST", "SHOTLIST")
        if shot_list is not None:
            items = shot_list.get_all("item")
        if filmed and not same_sequence:
            text = record_text(workspace, filmed[-1])
            after = [shot.identifier for shot in shots if shot_number(shot.identifier) > shot_number(filmed[-1].identifier)]
            lines.append(f"The last shot of {scene_words(previous)}" + (f" (then {', '.join(after)})" if after else "")
                         + ":\n" + fenced(text))
        elif items:
            lines.append(f"The last item of {scene_words(previous)}'s one-line list:\n"
                         + fenced(f"- item: {strip_story_point_endings(items[-1])}"))
        elif filmed:
            lines.append(f"The last shot of {scene_words(previous)}:\n" + fenced(record_text(workspace, filmed[-1])))
        else:
            heading = workspace.scene_heading(previous)
            lines.append(f"{scene_words(previous).capitalize()} has no shots or list yet"
                         + (f"; its heading: {heading}" if heading else "") + ".")
    else:
        lines.append("This is the film's first scene.")
    if position + 1 < len(order):
        following = order[position + 1]
        heading = workspace.scene_heading(following)
        lines.append(f"The next scene, {scene_words(following)}: " + (heading or "its heading is not known yet") + ".")
    else:
        lines.append("This is the film's last scene.")
    return lines


def scene_design_fields(workspace):
    return [field["name"] for field in workspace.schema.record_types["SCENE"]["fields"]
            if field.get("part_of") == "design"]


def scene_list_fields(workspace):
    return [field["name"] for field in workspace.schema.record_types["SCENE"]["fields"]
            if field.get("part_of") in ("list", "plan")]


def scene_records_section(workspace, unit, own_shots):
    """The records a step-7 or step-8 unit reads (blueprint 3, step 7's inputs), as one Markdown section."""
    scene_identifier = unit.scene
    scene = workspace.record(scene_identifier, "SCENE")
    parts = ["## Records you need",
             "Read-only: these come from the numbered files. Cite their IDs; never copy them into your inbox file. "
             "What code keeps (status, locks, approval, the beats code gave story points) is left out."]
    if scene is not None:
        parts.append(f"### The scene's list and plan fields\n" + records_block(
            workspace, [scene], fields=scene_list_fields(workspace)))
    sequence = workspace.record(unit.sequence or (scene.get("sequence") if scene else None), "SEQUENCE")
    if sequence is not None:
        parts.append("### Its group of scenes\n" + records_block(workspace, [sequence]))
    plan = workspace.singleton("PLAN")
    if plan is not None:
        order = workspace.scene_order()

        def plan_items(name, value):
            item = split_item(value)
            if name == "act":
                return scene_identifier in expand_range(item.get("scenes") or "", order) or \
                    story_point_in_scene(item.get("turn") or "", scene_identifier)
            if name == "peak":
                return scene_identifier in expand_range(item.get("scene") or "", order)
            return True
        parts.append("### The story plan (the lines that concern this scene)\n" + records_block(
            workspace, [plan], fields=PLAN_FIELDS_FOR_SCENES + ["act", "peak"], item_filter=plan_items))
    rules = ["### Film rules this scene touches"]
    camera_system = workspace.singleton("CAMSYS")
    if camera_system is not None:
        rules.append(records_block(workspace, [camera_system]))
    present = characters_present(workspace, scene_identifier)
    camera_rules = [rule for rule in workspace.records("CAMRULE") if rule.get("character") in present]
    if camera_rules:
        rules.append("Camera rules of the people present:\n" + records_block(workspace, camera_rules))
    allowed, reserve_text = reserve_lines(workspace, scene_identifier, own_shots)
    if reserve_text:
        rules.append("Saved choices (RESERVE), with the uses left:\n" + "\n".join(reserve_text))
    if allowed:
        rules.append(records_block(workspace, allowed))
    lenses = lens_exceptions_here(workspace, scene_identifier)
    if lenses:
        rules.append("Lens exceptions allowed here:\n" + records_block(workspace, lenses))
    visual = [record for record in workspace.records("VISUAL")
              if sequence is not None and record.get("sequence") == sequence.identifier]
    if visual:
        rules.append("The visual plan of its group:\n" + records_block(
            workspace, visual, item_filter=lambda name, value: name != "sub_row" or
            split_item(value).first == scene_identifier))
    looks = looks_for_scene(workspace, scene_identifier)
    if looks:
        rules.append("The look:\n" + records_block(workspace, looks))
    sound_plan = workspace.singleton("SOUNDPLAN")
    if sound_plan is not None:
        rules.append(records_block(workspace, [sound_plan]))
    ladder = workspace.singleton("LADDER")
    if ladder is not None:
        rung = [value for value in ladder.get_all("rung") if story_point_in_scene(value, scene_identifier)]
        if rung:
            rules.append("Its rung of the ladder:\n" + records_block(
                workspace, [ladder], item_filter=lambda name, value: name != "rung" or
                story_point_in_scene(value, scene_identifier)))
    if len(rules) > 1:
        parts.append("\n\n".join(rules))
    people = [workspace.record(character, "CHARACTER") for character in present]
    people = [record for record in people if record is not None]
    if people:
        voices = []
        for record in people:
            voice = workspace.record(record.get("voice"), "VOICE") if record.get("voice") else None
            voice = voice or next((item for item in workspace.records("VOICE")
                                   if item.get("character") == record.identifier), None)
            if voice is not None and voice not in voices:
                voices.append(voice)
        parts.append("### The people present\n" + records_block(workspace, people, fields=CHARACTER_FIELDS_FOR_SCENES)
                     + ("\n\n" + records_block(workspace, voices, fields=VOICE_FIELDS_FOR_SCENES) if voices else ""))
    states = [state for state in states_in_play(workspace, scene_identifier) if state is not None]
    if states:
        parts.append("### States in play at the scene's start (each element's state, with its sides)\n"
                     + records_block(workspace, states))
    location = location_for_scene(workspace, scene_identifier)
    if location is not None:
        if has_set_plan(location):
            parts.append("### The place, with its set plan (metres, in plan_orientation)\n"
                         + records_block(workspace, [location]))
        else:
            parts.append("### The place (no set plan: write a staging line; subjects take at and faces)\n"
                         + records_block(workspace, [location], fields=LOCATION_FIELDS_WITHOUT_PLAN))
    elements = elements_in_scene(workspace, scene_identifier)
    things = [workspace.record(element) for element in elements]
    props = [record for record in things if record is not None and record.type_name == "PROP"]
    texts = [record for record in things if record is not None and record.type_name == "TEXT"]
    cameras = [record for record in things if record is not None and record.type_name == "CAMERA"]
    if props or texts or cameras:
        parts.append("### Things, text in picture and cameras in the story here\n"
                     + records_block(workspace, props, fields=PROP_FIELDS_FOR_SCENES)
                     + ("\n\n" + records_block(workspace, texts, fields=TEXT_FIELDS_FOR_SCENES) if texts else "")
                     + ("\n\n" + records_block(workspace, cameras) if cameras else ""))
    motifs = [motif for motif in workspace.records("MOTIF")
              if any(scene_of(split_item(value).first or "") == scene_identifier or
                     split_item(value).first == scene_identifier for value in motif.get_all("appearance"))]
    if motifs:
        parts.append("### Motifs with an appearance here\n" + records_block(
            workspace, motifs, fields=MOTIF_FIELDS_FOR_SCENES + ["appearance"],
            item_filter=lambda name, value: name != "appearance" or scene_of(split_item(value).first or "") ==
            scene_identifier or split_item(value).first == scene_identifier))
    plants = [plant for plant in workspace.records("PLANT")
              if story_point_in_scene(plant.get("planted_at"), scene_identifier)
              or story_point_in_scene(plant.get("paid_off_at"), scene_identifier)]
    facts = [fact for fact in workspace.records("FACT")
             if fact.get("element") in elements or story_point_in_scene(fact.get("audience_knows_from"),
                                                                        scene_identifier)
             or any(story_point_in_scene(split_item(value).get("from") or "", scene_identifier)
                    for value in fact.get_all("known_by"))]
    if plants or facts:
        parts.append("### Plants, payoffs and who knows what\n" + records_block(workspace, plants + facts))
    rules_here = [rule for rule in workspace.records("RULE")
                  if normalise_word(rule.get("kind") or "") in ("mirror", "text", "titles")
                  or any(piece in elements for piece in split_list(rule.get("governs") or ""))]
    if rules_here:
        parts.append("### Story-world rules that govern what is here\n"
                     + records_block(workspace, rules_here, fields=RULE_FIELDS_FOR_SCENES))
    around = previous_and_next(workspace, unit)
    if around:
        parts.append("### Before and after this scene\n" + "\n\n".join(around))
    return "\n\n".join(parts)


def speech_lines(workspace, scene_identifier):
    """The scene's speeches with their IDs, speakers, lines, words and the seconds they need at the speaker's pace."""
    lines = []
    try:
        breakdown = workspace.breakdown
        entries = breakdown.speeches_of_scene(scene_identifier)
    except Exception:  # no speeches read yet
        return lines
    extra = constant_value(workspace.constants, "speech_floor_extra_s", 0.5)
    for entry in entries:
        if entry is None:
            continue
        speaker = entry.get("speaker") or "?"
        pace = breakdown.pace_of(speaker) if speaker != "?" else None
        count = entry.get("words") or len(words_of(entry.get("text")))
        seconds = f", {seconds_text(count / pace + extra)} s with speech_floor_extra_s" if pace else ""
        path = entry.get("path") or "direct"
        path_text = f", heard by {path}" if path not in ("direct", None) else ""
        lines.append(f"  - {entry['id']} {speaker}, line {entry.get('line')}, {plural(count, 'word')} at "
                     f"{seconds_text(pace) if pace else '?'} words per second{seconds}{path_text}: "
                     f"\"{entry.get('text', '')}\"")
    return lines


def source_section(workspace, title, first, last, unit_lines=None, heading_note=""):
    """The story's numbered lines first..last (and a trimmed copy with only unit_lines, for the ceiling)."""
    if workspace.story is None or first is None:
        return None, None
    width = len(str(last))

    def numbered(start, end):
        return "\n".join(f"{number:>{width}}  {workspace.story.line(number)}".rstrip()
                         for number in range(start, end + 1))
    head = f"## {title}\n" + (heading_note + "\n" if heading_note else "")
    text = head + fenced(numbered(first, last))
    trimmed = None
    if unit_lines and (unit_lines[0] > first or unit_lines[1] < last):
        trimmed = (head + f"Trimmed to this unit's own lines, {unit_lines[0]} to {unit_lines[1]}, to fit the "
                   "handout ceiling; ask stage.py lines for the rest.\n" + fenced(numbered(*unit_lines)))
    return text, trimmed


# ---------------------------------------------------------------- step 8: the batch, the camera, the whys

def batch_section(workspace, unit):
    """This batch's list items with their provisional floors, the other items in brief, and the scene's design."""
    scene_identifier = unit.scene
    parts = ["## This batch", "One SHOT per list item below, in this order, at the project's depth. "
             "screen_time is at or above each item's provisional floor (TIME-01 checks the real floor from your hear "
             "items); a pause owed after a turn counts on the item that ends the turn."]
    shot_list = workspace.record(f"{scene_identifier}-LIST", "SHOTLIST")
    definition = workspace.schema.field("SHOTLIST", "item")
    items = {}
    if shot_list is not None:
        for value in shot_list.get_all("item"):
            items[(split_item(value, definition).first or "").strip()] = value
    try:
        from .derive_fields import provisional_floor
    except ImportError:
        provisional_floor = None
    lines = []
    for shot in unit.shots:
        lines.append(f"- item: {strip_story_point_endings(items.get(shot, shot))}")
        if provisional_floor is not None:
            try:
                floor = provisional_floor(workspace.breakdown, scene_identifier, shot)
            except Exception:  # a floor that cannot be worked out is shown as unknown
                floor = None
            if floor is not None:
                lines.append(f"  provisional {floor.reasons()}")
            else:
                lines.append("  provisional floor: not known (the speeches or beats are missing)")
    parts.append(fenced("\n".join(lines)))
    others = [value for shot, value in items.items() if shot not in unit.shots]
    if others:
        parts.append("The scene's other list items (other batches; for continuity only):\n"
                     + fenced("\n".join(f"- item: {strip_story_point_endings(value)}" for value in others)))
    earlier = [shot for shot in workspace.records("SHOT") if scene_of(shot.identifier) == scene_identifier
               and unit.shots and (shot_number(shot.identifier) or 0) < (shot_number(unit.shots[0]) or 0)]
    if earlier:
        earlier.sort(key=lambda shot: shot_number(shot.identifier) or 0)
        parts.append("The shot written just before this batch:\n" + fenced(record_text(workspace, earlier[-1])))
    return "\n\n".join(parts)


def scene_design_section(workspace, unit):
    """Step 8 reads the scene design step 7 wrote: SCENE design fields, parts, the batch's beats in full (the others
    in brief), the batch's floor-plan moves and every setup."""
    scene_identifier = unit.scene
    scene = workspace.record(scene_identifier, "SCENE")
    parts = ["## The scene design (step 7's records)"]
    if scene is not None:
        parts.append(records_block(workspace, [scene], fields=scene_design_fields(workspace)))
    part_records = [record for record in workspace.records("PART") if scene_of(record.identifier) == scene_identifier]
    if part_records:
        parts.append(records_block(workspace, part_records))
    shot_list = workspace.record(f"{scene_identifier}-LIST", "SHOTLIST")
    definition = workspace.schema.field("SHOTLIST", "item")
    batch_beats = []
    if shot_list is not None:
        for value in shot_list.get_all("item"):
            item = split_item(value, definition)
            if (item.first or "").strip() in unit.shots:
                batch_beats += split_list(item.get("beats") or "")
    batch_beats = list(dict.fromkeys(batch_beats))
    beats = [record for record in workspace.records("BEAT") if scene_of(record.identifier) == scene_identifier]
    full = [beat for beat in beats if beat.identifier in batch_beats]
    brief = [beat for beat in beats if beat.identifier not in batch_beats]
    if full:
        parts.append("The beats this batch covers:\n" + records_block(workspace, full))
    if brief:
        parts.append("The scene's other beats, in brief:\n" + records_block(
            workspace, brief, fields=["lines", "turn", "beat_intensity", "pause_after"]))
    moves = [record for record in workspace.records("MOVE") if scene_of(record.identifier) == scene_identifier
             and (not batch_beats or record.get("beat") in batch_beats)]
    if moves:
        parts.append("The floor-plan moves in these beats:\n" + records_block(workspace, moves))
    setups = [record for record in workspace.records("SETUP") if scene_of(record.identifier) == scene_identifier]
    if setups:
        parts.append("The setups (cameras):\n" + records_block(workspace, setups))
    return "\n\n".join(parts), batch_beats


def camera_choices_section(workspace, unit):
    """The sizes, angles and moves the camera system allows here (banned ones left out; saved ones with their RC
    ID and uses left), the per-person rules, the lenses, and the fields that need a why with their defaults."""
    scene_identifier = unit.scene
    camera_system = workspace.singleton("CAMSYS")
    banned = set()
    if camera_system is not None:
        for value in camera_system.get_all("banned"):
            banned.add(normalise_word(split_item(value).first or ""))
    allowed_reserves, reserve_text = reserve_lines(workspace, scene_identifier, set(unit.shots))
    try:
        from .film_pass import reserve_match
    except ImportError:
        reserve_match = None
    saved = {}
    for reserve in workspace.records("RESERVE"):
        matched = reserve_match(reserve) if reserve_match else None
        if matched:
            saved.setdefault(matched, []).append(reserve)
    lines = ["## What the camera may do here",
             "Only these values are open to this batch; banned choices are left out and saved choices need their "
             "saved choice (cite its RC ID in because)."]
    for field_name in ("size", "angle", "move"):
        definition = workspace.schema.field("SHOT", field_name) or {}
        reserved_values = set(definition.get("reserved_values") or [])
        open_values, saved_values = [], []
        for value in definition.get("values") or []:
            if value in banned:
                continue
            reserves = saved.get((field_name, value), [])
            if reserves:
                usable = [reserve for reserve in reserves if reserve in allowed_reserves]
                if usable:
                    saved_values.append(f"{value} (only as {', '.join(reserve.identifier for reserve in usable)})")
                continue
            if value in reserved_values:
                continue
            open_values.append(value)
        line = f"- {field_name}: " + ", ".join(open_values)
        if saved_values:
            line += "; saved: " + ", ".join(saved_values)
        lines.append(line)
    if banned:
        lines.append("- Banned in this film (never written): " + ", ".join(sorted(banned)) + ".")
    if reserve_text:
        lines.append("Saved choices and their uses:")
        lines += reserve_text
    present = characters_present(workspace, scene_identifier)
    person_lines = []
    for rule in workspace.records("CAMRULE"):
        if rule.get("character") not in present:
            continue
        pieces = []
        if rule.get("never"):
            pieces.append(f"never {rule.get('never')}")
        if rule.get("limit_before"):
            closest = split_item(rule.get("closest") or "")
            pieces.append(f"nothing tighter than {rule.get('limit_before')} before "
                          + strip_story_point_endings(closest.get("at") or "the closest point")
                          + (f" (closest there: {closest.first})" if closest.first else ""))
        if pieces:
            person_lines.append(f"- {rule.get('character')}: " + "; ".join(pieces) + f" ({rule.identifier}).")
    if person_lines:
        lines.append("Each person's camera rule (CAMRULE):")
        lines += person_lines
    normal_lens = camera_system.get("normal_lens_mm") if camera_system is not None else None
    if camera_system is not None:
        lines.append(f"- Lenses: the family {camera_system.get('lens_family') or '(not written)'}; the normal lens "
                     f"{normal_lens or '(not written)'} millimetres"
                     + "".join(f"; {lens.identifier} {lens.get('mm')} millimetres only in {lens.get('only_in')}"
                               for lens in lens_exceptions_here(workspace, scene_identifier)) + ".")
    why_defaults = (workspace.schema.record_types.get("SHOT") or {}).get("why_defaults") or {}
    lines.append("")
    lines.append("## Fields that need a why when they differ from their default (REASON-02)")
    lines.append("A turn shot always carries a why; size and frame never need one.")
    for field_name, default in why_defaults.items():
        if field_name == "lens_mm" and normal_lens:
            default = f"{normal_lens} (CAMSYS normal_lens_mm)"
        lines.append(f"- {field_name}: {default}")
    return "\n".join(lines)


# ---------------------------------------------------------------- other steps' records

def generic_records_section(workspace, unit, step_entry):
    """The records a unit of steps 0 to 6, 9 to 11 or an add-on reads, by the step's reads list: in full for the
    unit's own scenes, chapters, characters and places, in brief otherwise."""
    reads = []
    for text in step_entry.get("reads") or []:
        match = re.match(r"^([A-Z]+)\b", text)
        if match and workspace.schema.knows_type(match.group(1)) and match.group(1) not in reads:
            reads.append(match.group(1))
    parts = ["## Records you need",
             "Read-only: these come from the numbered files. Cite their IDs; never copy them into your inbox file."]
    own_scenes = set(unit.scenes)
    for type_name in reads:
        records = workspace.records(type_name)
        if type_name == "PROJECT":
            records = [workspace.project_record] if workspace.project_record is not None else []
        if not records:
            continue
        label = (workspace.schema.record_types.get(type_name) or {}).get("plain_name", type_name)
        if type_name == "SCENE":
            full = [record for record in records if record.identifier in own_scenes]
            rest = [record for record in records if record.identifier not in own_scenes]
            if full and len(full) <= int(workspace.constant("event_unit_scenes", 10)):
                parts.append(f"### Scenes of this unit\n" + records_block(workspace, full,
                                                                        fields=scene_list_fields(workspace)))
            else:
                rest = records
            if rest:
                parts.append("### Every scene, in brief\n" + fenced("\n\n".join(brief_line(workspace, record)
                                                                                for record in rest)))
            continue
        if type_name == "CHAPTER":
            full = [record for record in records if record.identifier in unit.chapters] if unit.chapters else records
            parts.append(f"### {label.capitalize()}s\n" + records_block(workspace, full))
            continue
        if type_name == "CHARACTER" and unit.characters:
            full = [workspace.record(character, "CHARACTER") for character in unit.characters]
            full = [record for record in full if record is not None]
            if full:
                parts.append("### The characters of this unit\n" + records_block(workspace, full))
            others = [record for record in records if record.identifier not in unit.characters]
            if others:
                parts.append("### The other characters, in brief\n"
                             + fenced("\n\n".join(brief_line(workspace, record) for record in others)))
            continue
        if type_name == "CHOICE":
            parts.append("### Choices so far, in brief\n" + fenced("\n\n".join(brief_line(workspace, record)
                                                                              for record in records)))
            continue
        if type_name == "STATE" and own_scenes:
            wanted = []
            for scene in unit.scenes:
                for state in states_in_play(workspace, scene):
                    if state is not None and state not in wanted:
                        wanted.append(state)
            if wanted:
                parts.append("### States in play in these scenes\n" + records_block(workspace, wanted))
            continue
        text = records_block(workspace, records)
        if estimate_tokens(text, workspace.tokens_per_word) > 3000 and type_name in BRIEF_FIELDS:
            parts.append(f"### {label.capitalize()} records, in brief\n"
                         + fenced("\n\n".join(brief_line(workspace, record) for record in records)))
        else:
            parts.append(f"### {label.capitalize()} records\n" + text)
    if len(parts) == 2:
        parts.append("None yet: this unit starts from the story.")
    return "\n\n".join(parts)


def element_mentions(workspace, names, limit_lines=None):
    """Numbered story lines that mention any of the names (cue lines left out), capped at alias_mentions_cap plus
    every later line naming something one can see."""
    if workspace.story is None or not names:
        return []
    try:
        from .read_story import CUE, PHYSICAL_NOUNS
    except ImportError:
        CUE, PHYSICAL_NOUNS = "cue", set()
    pattern = re.compile(r"(?<![\w])(" + "|".join(re.escape(name) for name in sorted(set(names), key=len,
                                                                                         reverse=True))
                         + r")(?![\w])", re.IGNORECASE)
    types = (workspace.story_map or {}).get("line_types") or []
    hits = []
    for offset, line in enumerate(workspace.story.lines):
        number = workspace.story.first + offset
        kind = types[offset] if offset < len(types) else None
        if kind == CUE or not pattern.search(line):
            continue
        hits.append(number)
    cap = int(limit_lines or workspace.constant("alias_mentions_cap", 400))
    shown = hits[:cap]
    shown += [number for number in hits[cap:]
              if any(word.lower() in PHYSICAL_NOUNS for word in re.findall(r"[A-Za-z]+", workspace.story.line(number)))]
    return sorted(set(shown)), len(hits)


def names_of(workspace, identifier):
    record = workspace.record(identifier)
    names = []
    if record is not None:
        for field_name in ("names", "headings"):
            for value in record.get_all(field_name):
                names += split_list(value)
        if not names and record.title:
            names.append(record.title)
    if not names:
        for entry in (workspace.story_map or {}).get("characters", []):
            if entry.get("id") == identifier:
                names = list(entry.get("names") or [])
    return [name for name in names if name and name.lower() not in ("none", "open")]


def mentions_section(workspace, unit):
    """Step 4: for each element of the unit, every source line that mentions its names (the code-built list)."""
    if workspace.story is None:
        return None, None
    blocks = []
    elements = list(unit.characters)
    names_by_element = {element: names_of(workspace, element) for element in elements}
    for place in unit.places:
        names_by_element[place] = [place, place.split(" - ")[-1]]
    if unit.identifier in ("U-04-THINGS", "U-04-MOTIFS"):
        tokens = {}
        for scene in (workspace.story_map or {}).get("scenes", []):
            for token in scene.get("capitalised_words", []):
                if token.get("class") in ("prop", "text", "sound", "emphasis"):
                    tokens.setdefault((token["class"], token["text"]), []).append(token["line"])
        if tokens:
            lines = [f"- {text} ({kind}): lines " + ", ".join(str(number) for number in sorted(set(numbers)))
                     for (kind, text), numbers in sorted(tokens.items(), key=lambda pair: (pair[0][0], pair[0][1]))]
            blocks.append("### Words the reader found in capitals (things, text in picture, sounds, emphasis)\n"
                          + "\n".join(lines))
    width = len(str(workspace.story.last))
    for element, names in names_by_element.items():
        if not names:
            continue
        found = element_mentions(workspace, names)
        if not found:
            continue
        numbers, total = found
        shown = "\n".join(f"{number:>{width}}  {workspace.story.line(number)}".rstrip() for number in numbers)
        more = f" (the first alias_mentions_cap, plus every later line naming something one can see; " \
               f"stage.py lines {element} --more gives all)" if len(numbers) < total else ""
        blocks.append(f"### Lines that mention {element} ({', '.join(names)}): {len(numbers)} of {total}{more}\n"
                      + fenced(shown))
    if not blocks:
        return None, None
    return "## The story's lines for this unit\n" + "\n\n".join(blocks), None


def characters_to_name_section(workspace):
    """Prose has no character records from the reader (no cues): the harvest names them, so that step 4's next units
    can design each principal and each group of minor characters."""
    candidates = (workspace.story_map or {}).get("name_candidates") or []
    listed = ", ".join(f"{entry.get('name')} ({entry.get('count')})" for entry in candidates if entry.get("name"))
    return ("## Characters to name (no character records yet)\n"
            "The reader made no CHARACTER records for this story (prose has no cues). As part of the harvest, write one "
            "CHARACTER record for each person or being the film shows more than once: its ID from the name in capitals "
            "and hyphens (CH-NILAY), names (every name the story uses for them, each found in the story) and tier "
            "(principal, minor, extra or non_human); leave every other field to the unit that designs the character. "
            "Choices come from the block above. The names the story uses most often (with how often; some are places): "
            + (listed or "none found") + ".")


def odd_lines_section(workspace):
    """Step 1's odd-lines unit: the reader's report of lines to look at, and every scene or chapter it found."""
    if not workspace.story_map:
        return "## Lines to look at\nThe story has not been read yet: run stage.py read first."
    parts = []
    try:
        from .read_story import odd_lines_report_from_map
        report = odd_lines_report_from_map(workspace.story_map)
    except (ImportError, KeyError, TypeError, ValueError):
        report = []
    parts.append("## Lines to look at (the reader's odd-lines report)\nConfirm or correct each: a CHOICE for anything "
                 "odd, SCENE presentation and host, CHAPTER first_line and last_line.\n"
                 + ("\n".join(report) if report else "Nothing odd was found."))
    scenes = [record for record in workspace.records("SCENE")]
    chapters = [record for record in workspace.records("CHAPTER")]
    if scenes:
        parts.append("## Every scene the reader found, in brief\n" + fenced("\n\n".join(
            record_text(workspace, record, ["heading", "lines", "characters", "presentation", "host",
                                            "transition_in", "transition_out", "origin"]) for record in scenes)))
    if chapters:
        parts.append("## Every chapter the reader found\n" + records_block(workspace, chapters))
    return "\n\n".join(parts)


def judgement_section(workspace, unit):
    """Step 9's judgement unit: the film strip (or its act), the turn pictures and the checker's film report."""
    parts = []
    folder = workspace.project.machine_folder
    strip = folder / (unit.strip_file or FILM_STRIP_FILE)
    if strip.is_file():
        parts.append(f"## The film strip ({strip.name}), one line per shot\n" + fenced(strip.read_text(encoding="utf-8")))
    else:
        parts.append("## The film strip\nNot made yet: run stage.py check --film first, then build this handout again.")
    pictures = []
    for scene in workspace.records("SCENE"):
        if unit.scenes and scene.identifier not in unit.scenes:
            continue
        for value in scene.get_all("turn_picture"):
            pictures.append(f"- {scene.identifier} {strip_story_point_endings(value)}")
    if pictures:
        parts.append("## Every turn picture\n" + "\n".join(pictures))
    report = workspace.folder / WHOLE_FILM_FILE
    if report.is_file():
        plain = report.read_text(encoding="utf-8").split(DIVIDER_LINE, 1)[0].strip()
        parts.append("## The checker's report on the whole film (12 Whole-film check)\n" + demote_headings(plain, 2))
    return "\n\n".join(parts)


def questions_section(workspace, unit):
    """A review-question unit: the batch's questions, only the records and story lines they cite (never the
    writer's context)."""
    data = read_json_file(workspace.project.machine_folder / QUESTIONS_FILE) or {}
    batch = next((entry for entry in data.get("batches", []) if entry.get("unit") == unit.identifier), None)
    if batch is None:
        return "## The questions\nNot made yet: run stage.py questions --sample first, then build this handout again."
    parts = [f"## The questions of {unit.identifier}",
             "Answer each yes or no against the story, reading only the records and lines it cites. Write one REVIEW "
             "per scene (### REVIEW RV-SC10, - scope: SC10) with one line per question: - answer: <the question, word "
             "for word> | answer: yes | evidence: <the story's words or the shot and moment>. Each no also becomes a "
             "FINDING with source: review, numbered from the block above. An answer without evidence is dropped."]
    cited, line_ranges = [], []
    lines = []
    for question in batch.get("questions", []):
        lines.append(f"{question.get('number')}. {question.get('question')} [{question.get('record')}]")
        for identifier in question.get("cites") or []:
            if identifier not in cited:
                cited.append(identifier)
        if question.get("lines"):
            line_ranges.append(tuple(question["lines"]))
    parts.append("\n".join(lines))
    records = [workspace.record(identifier) for identifier in cited]
    records = [record for record in records if record is not None]
    if records:
        parts.append("## The records these questions cite\n" + records_block(workspace, records))
    if line_ranges and workspace.story is not None:
        merged = []
        for first, last in sorted(line_ranges):
            if merged and first <= merged[-1][1] + 1:
                merged[-1] = (merged[-1][0], max(merged[-1][1], last))
            else:
                merged.append((first, last))
        width = len(str(workspace.story.last))
        blocks = ["\n".join(f"{number:>{width}}  {workspace.story.line(number)}".rstrip()
                            for number in range(first, last + 1)) for first, last in merged]
        parts.append("## The story's lines these questions cite\n" + fenced("\n...\n".join(blocks)))
    return "\n\n".join(parts)


def scores_section(workspace, unit):
    parts = []
    report = workspace.folder / HEALTH_CHECK_FILE
    if report.is_file():
        plain = report.read_text(encoding="utf-8").split(DIVIDER_LINE, 1)[0].strip()
        parts.append("## The checker's report (13 Health check)\n" + demote_headings(plain, 2))
    reviews = workspace.records("REVIEW")
    if reviews:
        parts.append("## The review answers so far\n" + records_block(workspace, reviews))
    return "\n\n".join(parts)


# ---------------------------------------------------------------- building the handout

def unit_section(workspace, unit, step_entry, issued_lines, check_command):
    """What this unit writes, where, and what to run after."""
    inbox = f"{MACHINE_FOLDER}/{INBOX_FOLDER}/{unit.identifier}.md"
    lines = ["## This unit"]
    scope = []
    if unit.scenes:
        if unit.step in (7, 8):
            lines_of_scene = workspace.scene_lines(unit.scene)
            heading = workspace.scene_heading(unit.scene)
            scope.append(f"{scene_words(unit.scene)}" + (f", lines {lines_of_scene[0]} to {lines_of_scene[1]}"
                                                         if lines_of_scene else "")
                         + (f" ({heading})" if heading else ""))
        else:
            scope.append(scene_group_words(unit.scenes))
    if unit.chapters:
        scope.append("chapters " + ", ".join(unit.chapters))
    if unit.characters:
        scope.append(", ".join(unit.characters))
    if unit.places:
        scope.append("places: " + "; ".join(unit.places))
    entry_of_unit = unit.entry_of_unit or {}
    lines.append(f"- Unit {unit.identifier}: {entry_of_unit.get('scope') or step_entry.get('name', '')}"
                 + (f"; {'; '.join(scope)}" if scope else "") + f". Depth: "
                 + (workspace.scene_depth(unit.scene) if unit.scene else workspace.depth) + ".")
    if unit.part:
        extent = f", lines {unit.lines[0]} to {unit.lines[1]}" if unit.lines else ""
        lines.append(f"- This is part {unit.part} of a big scene{extent}: write the scene fields"
                     + (" and" if unit.part == 1 else " you add,") + f" the part record, its beats, moves and setups; "
                     "end the part at a turn near that line. The one-line list comes in its own unit "
                     f"(U-07-{unit.scene}-LIST).")
    if unit.list_unit:
        lines.append("- This unit writes only the one-line shot list (SHOTLIST), from the parts and beats already "
                     "written.")
    writes = entry_of_unit.get("writes") or step_entry.get("writes") or []
    if writes:
        lines.append("- You write: " + ", ".join(writes) + ".")
    if entry_of_unit.get("batch_rule"):
        lines.append(f"- Batch rule: {entry_of_unit['batch_rule']}.")
    if workspace.code_execution:
        lines.append(f"- Write your records to: {inbox}, one reply, every record in full, ending with the END line "
                     "(END OF FILE | <what it holds> | <n> records).")
        after = f'stage.py apply "{unit.identifier}.md"'
        if unit.step in (7, 8):
            after += ", then stage.py build (code places the story points on their beats and works out the derived "\
                     "fields)"
        if check_command:
            after += f", then {check_command}"
        lines.append(f"- Then run: {after}. Fix only the lines the checker prints, at most repair_rounds_max rounds.")
        lines.append("- Never type what code writes: status, locked, approved, dates, the ' = <beat>' ending of a "
                     "story point, labels, time floors, clip lengths, image sides, prompts, prices.")
    else:
        lines.append("- In a chat without code: write the file in one copy box as the step file's last section says, "
                     "with every line reference as a quote anchor.")
    if unit.note:
        lines.append(f"- Note: {unit.note}.")
    lines.append("- Read this whole handout: the IDs issued to you, the step file, the card parts, the records, the "
                 "story's lines, the template and the example.")
    text = "\n".join(lines)
    if issued_lines:
        text += "\n\n## IDs issued to you\nCopy them; never make one up (ID-06 checks every new record against its " \
                "block).\n" + "\n".join(issued_lines)
    return text


def check_command_for(unit, step_entry):
    command = step_entry.get("check_command")
    if not command:
        return None
    if unit.step in (7, 8) and unit.scene:
        return f"stage.py {command} --scene {unit.scene}"
    return f"stage.py {command}"


def example_section(workspace, unit):
    """One example from the gold (scene 10 of The Catch): at step 7 its main turn's beat and its one-line list, at
    step 8 its turn shot, otherwise the first gold record of each type the unit writes."""
    gold = gold_records(workspace)
    if not gold:
        return None
    wanted = []
    if unit.step == 7:
        if not unit.list_unit:
            wanted.append(("BEAT", "SC10-B07"))
        if unit.part is None or unit.list_unit:
            wanted.append(("SHOTLIST", "SC10-LIST"))
    elif unit.step == 8:
        wanted.append(("SHOT", "SC10-SH150"))
    else:
        for type_name in [kind for kind in written_types(unit, workspace) if kind not in ("CHOICE", "SETVALUE")][:2]:
            first = next((key for key in gold if key[0] == type_name), None)
            if first:
                wanted.append(first)
    records = [gold[key] for key in wanted if key in gold]
    if not records:
        return None
    return ("## One example from the gold (The Catch, scene 10)\nThe form to follow, not words to copy.\n"
            + records_block(workspace, records))


def build_handout(workspace, unit, surface=None):
    """The handout of one unit (see the note at the top of this file)."""
    if unit.kind == "checkpoint":
        raise StageStop(f"{unit.plain(workspace.steps).capitalize()} is a checkpoint that waits for the user, not a "
                        "unit with a handout; stage.py next says what it waits for.")
    if unit.identifier == "U-00-SELFTEST":
        raise StageStop("The self-test's handout is written by: stage.py selftest --prepare")
    if unit.kind == "code":
        raise StageStop(f"{unit.plain(workspace.steps).capitalize()}: code does this work; there is no handout.")
    step_entry = workspace.step_entry(unit.step)
    task, excerpt = step_file_parts(workspace, step_entry, keep_chat_twin=not workspace.code_execution)
    handout = Handout(unit=unit, ceiling=workspace.ceiling(surface), tokens_per_word=workspace.tokens_per_word,
                      card_cap=workspace.card_cap, task=task)
    issued, issued_text = issued_ids(workspace, unit)
    handout.issued = issued
    user_number = step_entry.get("user_number")
    counted = f"step {user_number} of 12" if unit.step <= 11 and user_number else step_entry.get("name", "")
    plain = unit.plain(workspace.steps)
    handout.add("head", f"# Handout {unit.identifier}: {plain}\n\n"
                        f"**One-line task:** {task}\n\n"
                        "Quote the one-line task back, word for word, before you do anything else. "
                        f"This handout is the one file to read for this unit ({counted}).")
    handout.add("unit", unit_section(workspace, unit, step_entry, issued_text, check_command_for(unit, step_entry)))
    if unit.step == 7 and unit.scene:
        speeches = speech_lines(workspace, unit.scene)
        if speeches:
            handout.add("speeches", "- Speeches, numbered by code in cue order (cite their IDs; never renumber): the "
                                    "seconds are each speech's words at its speaker's pace plus speech_floor_extra_s, "
                                    "so a list item's seconds leave room for its speeches and for the pause owed after "
                                    "a turn (turn_reaction_min_s):\n" + "\n".join(speeches))
    handout.add("step", f"## The step file: {step_entry.get('step_file', '')}\n"
                        "Read it every time, never from memory.\n\n" + excerpt)
    for card_code, part_name in card_list(workspace, unit, step_entry):
        found = card_part_text(workspace, card_code, part_name)
        if found is None:
            handout.notes.append(f"card {card_code} part {part_name} is not in this copy of the skill")
            continue
        label, body = found
        handout.add(f"card {card_code} {part_name}", f"## Card part: {label}\n\n" + demote_headings(body, 1),
                    kind="card", label=f"card {card_code}, {label.split(', part ')[-1] if ', part ' in label else 'whole'}")
    source_note = ""
    if unit.step in (7, 8) and unit.scene:
        own_shots = set(unit.shots) if unit.step == 8 else {
            shot.identifier for shot in workspace.records("SHOT") if scene_of(shot.identifier) == unit.scene}
        if unit.step == 8:
            design, batch_beats = scene_design_section(workspace, unit)
            handout.add("batch", batch_section(workspace, unit))
            handout.add("camera", camera_choices_section(workspace, unit))
            handout.add("design", design)
        else:
            batch_beats = []
        handout.add("records", scene_records_section(workspace, unit, own_shots))
        lines = workspace.scene_lines(unit.scene)
        unit_lines = unit.lines
        if unit.step == 8 and batch_beats:
            numbers = []
            for beat in batch_beats:
                record = workspace.record(beat, "BEAT")
                ranges = parse_line_numbers(record.get("lines") or "") if record is not None else None
                for first, last in ranges or []:
                    numbers += [first, last]
            if numbers:
                unit_lines = (min(numbers), max(numbers))
        if lines:
            source, trimmed = source_section(workspace, f"The scene's lines ({scene_words(unit.scene)}, "
                                                        f"{lines[0]} to {lines[1]})", lines[0], lines[1], unit_lines)
            if source:
                handout.add("source", source, kind="source", label="the story's lines", trimmed_text=trimmed)
            else:
                source_note = "the story is not read into this project, so its lines are not shown"
    elif unit.step == 9:
        handout.add("records", judgement_section(workspace, unit))
        handout.add("records more", generic_records_section(workspace, unit, step_entry))
    elif unit.step == 10 and "QUESTIONS" in unit.identifier:
        handout.add("records", questions_section(workspace, unit))
    elif unit.step == 10:
        handout.add("records", scores_section(workspace, unit))
    else:
        handout.add("records", generic_records_section(workspace, unit, step_entry))
        if unit.identifier == "U-01-ODDLINES":
            handout.add("odd lines", odd_lines_section(workspace))
        if unit.identifier == "U-04-MOTIFS" and not workspace.records("CHARACTER"):
            handout.add("characters to name", characters_to_name_section(workspace))
        if unit.step == 4:
            text, _ = mentions_section(workspace, unit)
            if text:
                handout.add("source", text, kind="source", label="the story's lines")
        elif unit.chapters and workspace.story is not None and unit.step == 2 and unit.identifier != "U-02-BOOK":
            ranges = [workspace.chapter_lines(chapter) for chapter in unit.chapters]
            ranges = [pair for pair in ranges if pair]
            if ranges:
                source, trimmed = source_section(workspace, "The chapters' lines", ranges[0][0], ranges[-1][1])
                handout.add("source", source, kind="source", label="the story's lines")
        elif unit.scenes and workspace.story is not None and unit.step in (2, 5) and unit.identifier != "U-02-FILM":
            ranges = [workspace.scene_lines(scene) for scene in unit.scenes]
            ranges = [pair for pair in ranges if pair]
            if ranges:
                source, trimmed = source_section(workspace, f"The story's lines ({scene_group_words(unit.scenes)})",
                                                 ranges[0][0], ranges[-1][1])
                handout.add("source", source, kind="source", label="the story's lines")
    templates = []
    depth_rank = DEPTH_RANK_OF[workspace.scene_depth(unit.scene) if unit.scene else workspace.depth]
    for type_name in written_types(unit, workspace):
        if type_name == "MOVE" and unit.step == 7:
            location = location_for_scene(workspace, unit.scene) if unit.scene else None
            if not has_set_plan(location) and depth_rank < DEPTH_RANK_OF["detailed"]:
                continue
        block = template_for(workspace, type_name, unit.step)
        if block:
            templates.append(filter_template(block, depth_rank, workspace.code_execution, add_on=unit.step >= 12))
    if templates:
        handout.add("template", "## The record template, at this depth\nEvery field for this depth, in order; the "
                                "notes (> lines) give the allowed values and are not written.\n"
                    + fenced("\n\n".join(templates), "markdown"))
    example = example_section(workspace, unit)
    if example:
        handout.add("example", example, kind="example", label="the example from the gold")
    if source_note:
        handout.notes.append(source_note)
    handout.add("end", f"**One-line task, again:** {task}")
    unit_part = next(section for section in handout.sections if section.key == "unit")
    unit_text = unit_part.text
    for _ in range(4):
        # the notes about what was left out sit in the unit's own section, so fitting runs again with them in
        handout.fit()
        notes = []
        if handout.left_out:
            notes.append("Left out to fit: " + "; ".join(handout.left_out) + ".")
        if handout.too_big:
            notes.append(f"Still over the ceiling of {number_with_commas(handout.ceiling)} tokens: split this unit "
                         "(a smaller batch, or the scene in parts).")
        for note in handout.notes:
            notes.append(note[:1].upper() + note[1:] + ".")
        unit_part.text = unit_text.rstrip() + ("\n\n" + "\n".join(f"- {note}" for note in notes) if notes else "") + "\n"
        if not handout.ceiling or handout.too_big or handout.tokens() <= handout.ceiling:
            break
    if unit.step == 8 and unit.scene:
        handout.batches = {unit.scene: {unit.identifier: {"expected": len(unit.shots), "first": unit.shots[0],
                                                          "last": unit.shots[-1]}}} if unit.shots else {}
    return handout


def handout_path(workspace, unit):
    return workspace.project.machine_folder / HANDOUTS_FOLDER / f"{unit.identifier}.md"


def write_handout(workspace, unit, surface=None):
    """Build a unit's handout, write it and record its issued IDs (and a step-8 batch's range) in the manifest."""
    if unit.step == 8 and not unit.shots:
        raise StageStop(f"{unit.identifier} has no shots yet: its scene has no one-line shot list, so no batch is "
                        f"planned. Write the list first (U-07-{unit.scene}).")
    handout = build_handout(workspace, unit, surface)
    path = handout_path(workspace, unit)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = handout.text()
    path.write_text(text, encoding="utf-8")
    with workspace.project.lock():
        manifest = workspace.project.read_manifest()
        if handout.issued:
            manifest.setdefault("issued", {})[unit.identifier] = handout.issued
        if unit.step == 8 and unit.scene:
            # The checker compares a scene's stored records with every block issued for that scene: when no step-7
            # handout issued the scene's blocks (a folder adopted from a chat app), record them as step 7 does.
            issued = manifest.setdefault("issued", {})
            if not any(name == f"U-07-{unit.scene}" or name.startswith(f"U-07-{unit.scene}-") for name in issued):
                blocks, _, _ = scene_blocks(workspace, unit)
                issued[f"U-07-{unit.scene}"] = blocks
        for scene, batches in handout.batches.items():
            stored = manifest.setdefault("batches", {}).setdefault(scene, {})
            for batch_unit, entry in batches.items():
                current = stored.setdefault(batch_unit, {})
                received = current.get("received")
                current.update(entry)
                if received is not None:
                    current["received"] = received
        manifest.setdefault("handouts", {})[unit.identifier] = {
            "built": now(), "tokens": handout.tokens(), "ceiling": handout.ceiling,
            "card_tokens": handout.card_tokens(), "left_out": handout.left_out}
        workspace.project.write_manifest(manifest)
        workspace.manifest = manifest
    return handout, path


def record_batch_plan(workspace, units):
    """Write each planned step-8 batch's range (first, last, expected) into the manifest, so the checker knows which
    list items each batch holds (ID-07 and COVER-02 to COVER-04 during step 8)."""
    wanted = {}
    for unit in units:
        if unit.step == 8 and unit.shots:
            entry = {"expected": len(unit.shots), "first": unit.shots[0], "last": unit.shots[-1]}
            written = [shot for shot in unit.shots if workspace.record(shot, "SHOT") is not None]
            stored = ((workspace.manifest.get("batches") or {}).get(unit.scene) or {}).get(unit.identifier) or {}
            if len(written) == len(unit.shots) and stored.get("received") is None:
                # the batch's shots are already there (written before the plan was recorded, or adopted)
                entry["received"] = len(written)
            wanted.setdefault(unit.scene, {})[unit.identifier] = entry
    if not wanted:
        return
    with workspace.project.lock():
        manifest = workspace.project.read_manifest()
        changed = False
        for scene, batches in wanted.items():
            stored = manifest.setdefault("batches", {}).setdefault(scene, {})
            for unit_identifier, entry in batches.items():
                current = stored.setdefault(unit_identifier, {})
                for key, value in entry.items():
                    if current.get(key) != value and not (key == "expected" and current.get("received") is not None
                                                          and current.get(key) is not None):
                        current[key] = value
                        changed = True
        if changed:
            workspace.project.write_manifest(manifest)
            workspace.manifest = manifest


# ---------------------------------------------------------------- the commands

def add_next_arguments(parser):
    parser.add_argument("--checkpoint-passed", action="store_true",
                        help="the user answered the checkpoint next names (a group of shots, the finished check): "
                             "record it and go on")
    parser.add_argument("--stop-after-each-group", choices=["yes", "no"],
                        help="yes: every group of shots waits for the user (they said 'stop after each group'); "
                             "no: only the first group waits")
    parser.add_argument("--no-handout", action="store_true", help="name the next unit without building its handout")
    parser.add_argument("--surface", help="build the handout for this app's ceiling (default: PROJECT surface)")


def add_handout_arguments(parser):
    parser.add_argument("unit", help="the unit ID, for example U-07-SC10 or U-08-SC10-B1")
    parser.add_argument("--surface", help="build the handout for this app's ceiling (default: PROJECT surface)")


def say_checkpoint(context, workspace, unit):
    name = unit.plain(workspace.steps)
    reference = "reference/07 Report and message formats has its message"
    context.say(f"Next: {name}, a checkpoint that waits for the user ({reference}).")
    if unit.waiting:
        for choice in unit.waiting[:7]:
            default = split_item(choice.get("default") or "").first or ""
            number = int(choice.identifier.split("-")[1]) if re.match(r"^CHOICE-\d+$", choice.identifier) else None
            context.say(f"  Waiting for: choice {number if number is not None else choice.identifier} "
                        f"({choice.identifier}): {choice.get('question') or choice.title}"
                        + (f" [default {default}]" if default else ""))
        context.say('Pass the answers on: write "### CHOICE CHOICE-NNN" with "- answer: <letter>" (or "- answer: '
                    f'defaults") for each into {MACHINE_FOLDER}/{INBOX_FOLDER}/<a name>.md, run stage.py apply on it, '
                    "then stage.py next.")
    else:
        extra = ""
        if unit.checkpoint == "c" and unit.first_group:
            extra = (" The first group's message also states the film rules in five plain lines and says that later "
                     "groups are shown without waiting.")
        context.say(f"When the user replies \"next\" (after any change they ask for is made), run: stage.py next "
                    f"--checkpoint-passed.{extra}")


def run_next(context):
    arguments = context.arguments
    workspace = Workspace(context.project, context.schema, context.words, context.constants)
    if arguments.stop_after_each_group:
        with workspace.project.lock():
            manifest = workspace.project.read_manifest()
            manifest.setdefault("checkpoints", {})["stop_after_each_group"] = arguments.stop_after_each_group == "yes"
            workspace.project.write_manifest(manifest)
        workspace = Workspace(context.project, context.schema, context.words, context.constants)
        context.say("Every group of shots will wait for the user." if arguments.stop_after_each_group == "yes"
                    else "Only the first group of shots waits for the user; later groups are shown and the work "
                         "carries on.")
    if arguments.checkpoint_passed:
        unit, _ = find_next_unit(workspace, pass_reported_checkpoints=True)
        if unit is None or unit.kind != "checkpoint":
            raise StageStop("No checkpoint is waiting for the user now, so there is nothing to pass; run stage.py next.")
        if unit.waiting:
            raise StageStop(f"{unit.plain(workspace.steps).capitalize()} waits for choice records: pass the user's "
                            "answers through an inbox file and stage.py apply, then run stage.py next.")
        changed = pass_checkpoint(workspace, unit, "the user replied next")
        context.say(f"Passed: {unit.plain(workspace.steps)}"
                    + (f"; approved the shot lists in {', '.join(changed)}" if changed else "") + ".")
        workspace = Workspace(context.project, context.schema, context.words, context.constants)
    unit, reported = find_next_unit(workspace, pass_reported_checkpoints=True)
    if reported:
        for checkpoint in reported:
            context.say(f"Show the user {checkpoint.plain(workspace.steps)} (it does not wait; reference/07 has its "
                        "message); its shot lists are now approved.")
        workspace = Workspace(context.project, context.schema, context.words, context.constants)
        unit, _ = find_next_unit(workspace, pass_reported_checkpoints=True)
    record_batch_plan(workspace, workspace.plan())
    if unit is None:
        context.say("Nothing left in the 12 steps. The add-ons run when the user asks: storyboards (step 12), grey "
                    "previews (step 13, Claude Code only), prompts for AI video (step 14), edit and finishing "
                    "(step 15).")
        context.summary = "nothing left"
        return 0
    if unit.kind == "checkpoint":
        say_checkpoint(context, workspace, unit)
        context.summary = f"waiting: {CHECKPOINT_NAMES.get(unit.checkpoint)}"
        return 0
    if unit.kind == "code":
        if unit.identifier == "U-00-SELFTEST":
            context.say("Next: U-00-SELFTEST, step 1 of 12 (the hidden self-test, not shown to the user). Run stage.py "
                        f"selftest --prepare: it writes the handout {MACHINE_FOLDER}/{HANDOUTS_FOLDER}/U-00-SELFTEST.md. "
                        f"Write the test shots to {MACHINE_FOLDER}/{INBOX_FOLDER}/U-00-SELFTEST.md in one reply, then "
                        "run stage.py selftest --score --surface <this app>.")
        else:
            context.say(f"Next: {unit.plain(workspace.steps)}. Run " + ", then ".join(
                f"stage.py {command}" for command in unit.commands) + ", then stage.py next.")
        context.summary = f"next: {unit.identifier}"
        return 0
    context.say(f"Next: {unit.identifier}, {unit.plain(workspace.steps)}.")
    if unit.step == 8 and not unit.shots:
        context.say(f"Its scene has no one-line shot list yet; write U-07-{unit.scene} first.")
        return 0
    if arguments.no_handout:
        context.say(f"Build its handout with: stage.py handout {unit.identifier}")
        context.summary = f"next: {unit.identifier}"
        return 0
    handout, path = write_handout(workspace, unit, arguments.surface)
    say_handout(context, workspace, unit, handout, path)
    context.summary = f"next: {unit.identifier} ({handout.tokens()} tokens)"
    return 0


def say_handout(context, workspace, unit, handout, path):
    relative = path.relative_to(workspace.folder).as_posix()
    ceiling = f" of {number_with_commas(handout.ceiling)}" if handout.ceiling else ""
    context.say(f"Handout: {relative} (about {number_with_commas(handout.tokens())} tokens{ceiling}; card parts about "
                f"{number_with_commas(handout.card_tokens())} of {number_with_commas(handout.card_cap)}).")
    if handout.left_out:
        context.say("Left out to fit: " + "; ".join(handout.left_out) + ".")
    if handout.too_big:
        context.say(f"The handout is still over its ceiling: split {unit.identifier} (a smaller batch, or the scene "
                    "in parts).")
    step_entry = workspace.step_entry(unit.step)
    check = check_command_for(unit, step_entry)
    build = ", then stage.py build" if unit.step in (7, 8) else ""
    context.say(f"Then: write the records to {MACHINE_FOLDER}/{INBOX_FOLDER}/{unit.identifier}.md, run stage.py apply "
                f'"{unit.identifier}.md"{build}' + (f", then {check}" if check else "") + ".")


def run_handout(context):
    arguments = context.arguments
    workspace = Workspace(context.project, context.schema, context.words, context.constants)
    unit = unit_from_identifier(workspace, arguments.unit)
    mark_done(workspace, [unit])
    handout, path = write_handout(workspace, unit, arguments.surface)
    context.say(f"Wrote the handout for {unit.identifier}, {unit.plain(workspace.steps)}.")
    say_handout(context, workspace, unit, handout, path)
    if getattr(unit, "done", False):
        context.say(f"Its records are already there: redoing it replaces them (stage.py impact names what else goes "
                    "stale).")
    context.summary = f"handout {unit.identifier} ({handout.tokens()} tokens)"
    return 0


def register_commands(table):
    """stage.py's command table: next and handout (see the note at the top of stage.py)."""
    table.add("next", "The next unit, checkpoint or command, with the unit's handout", run_next, add_next_arguments)
    table.add("handout", "Build a unit's handout in For machines - do not edit/handouts/", run_handout,
              add_handout_arguments)
