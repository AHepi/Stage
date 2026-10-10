"""Read and write record files: the line grammar G1-G13 of blueprint section 5.1.

What this file does, in plain words:
- reads a record file into its parts (the free text people read, the records with their field lines and
  notes, and the END line), keeping every line exactly as it was written;
- writes a file back: records nobody changed come out exactly as they were read, changed and new records
  come out in the canonical form (fields in the schema's order), the plain part and divider are untouched
  and the END line is counted again;
- splits values into their parts (list items, sub-parts, line numbers, story points) and examines each
  value against its kind in _config/schema/schema.json, returning tidy fixes and problems;
- merges the copies of one record found in several files (G10);
- defines Problem, the one-line message every check prints (blueprint 7.2).

Other modules use: load_skill_data, Schema, parse_text, parse_file, render_file, write_file, make_record,
Record.get / get_all / set_field / set_items / remove_field, add_record, split_item, split_list,
examine_value, examine_field, merge_copies, Problem.

Standard library only.

After the full run on The Catch (Project notes 31 and 32):
- quote_for_message cuts between whole words.

After the three-scene test of the fixed kit (Project notes 35 and 36):
- a bare none is a value of a field whose first part may be none (pause_after).
"""

import datetime
import difflib
import json
import re
from dataclasses import dataclass, field as dataclass_field
from pathlib import Path

SKILL_FOLDER = Path(__file__).resolve().parents[2]

# Where things are inside the skill folder (Project notes 43: the folders are the steps). Each is a path relative to
# the skill folder, written with "/", so a caller joins it to whichever copy of the skill it reads
# (skill_folder / CARDS_FOLDER, or load_json(LIMITS_FILE, skill_folder)). Change a folder here and nowhere else.
STAGES_FOLDER = "stages"                                  # one folder per step: "00 Start/CONTEXT.md" and so on
STAGE_CONTRACT_NAME = "CONTEXT.md"                        # the step file inside each step's folder
REFERENCES_FOLDER = "references"                          # what the AI reads, the same every run
CARDS_FOLDER = REFERENCES_FOLDER + "/cards"               # the craft cards 01 to 24
LIBRARY_FOLDER = REFERENCES_FOLDER + "/library"           # the research files, their digests and three notes
FORMATS_FOLDER = REFERENCES_FOLDER + "/formats"           # record format, word list, field guide, rule order, ...
TEMPLATES_FOLDER = REFERENCES_FOLDER + "/templates"       # the empty record files
EXAMPLES_FOLDER = REFERENCES_FOLDER + "/examples"         # the gold scene 10 and its context
CONFIG_FOLDER = "_config"                                 # the settings the code reads, the same every run
SCHEMA_FOLDER = CONFIG_FOLDER + "/schema"                 # schema.json and steps.json
RULES_FOLDER = CONFIG_FOLDER + "/rules"                   # constants, words, limits, tone defaults
ADAPTERS_FOLDER = CONFIG_FOLDER + "/adapters"             # dated model facts and prices
SCHEMA_FILE = SCHEMA_FOLDER + "/schema.json"
STEPS_FILE = SCHEMA_FOLDER + "/steps.json"
CONSTANTS_FILE = RULES_FOLDER + "/constants.json"
WORDS_FILE = RULES_FOLDER + "/words.json"
LIMITS_FILE = RULES_FOLDER + "/limits.json"
TONE_DEFAULTS_FILE = RULES_FOLDER + "/tone_defaults.json"
GOLD_SCENE_FILE = EXAMPLES_FOLDER + "/01 The Catch - scene 10.md"
GOLD_CONTEXT_FILE = EXAMPLES_FOLDER + "/02 The Catch - scene 10 - context.md"
MESSAGE_FORMATS_FILE = FORMATS_FOLDER + "/07 Report and message formats.md"


def stage_contract_file(step_folder_name):
    """The step file of one step, relative to the skill folder: stage_contract_file("08 Shot details") is
    "stages/08 Shot details/CONTEXT.md"."""
    return f"{STAGES_FOLDER}/{step_folder_name}/{STAGE_CONTRACT_NAME}"


def adapter_file(file_name):
    """One file of the dated model facts, relative to the skill folder: adapter_file("prices.json")."""
    return f"{ADAPTERS_FOLDER}/{file_name}"


DIVIDER_LINE = "Below this line: details for the AI and the checker. You never need to read them."
SUB_PART_SEPARATOR = " | "
MISSING_WORDS = ("null", "n/a", "-", "")
CHARGES = ("---", "--", "-", "0", "+", "++", "+++")
DEPTH_RANK = {"q": 1, "s": 2, "f": 3, "quick": 1, "standard": 2, "detailed": 3}
DEPTH_WORD = {"q": "quick", "s": "standard", "f": "detailed"}
NUMBER_KINDS = ("number", "seconds", "metres", "millimetres", "dollars", "words_per_second")
UNIT_SUFFIXES = {
    "seconds": r"s|sec|secs|second|seconds",
    "metres": r"m|metre|metres|meter|meters",
    "millimetres": r"mm|millimetre|millimetres|millimeter|millimeters",
    "dollars": r"usd|dollars?",
    "words_per_second": r"wps|words per second|words/s",
}
OPENING_QUOTES = '"\u201c'
CLOSING_QUOTES = '"\u201d'

HEADING_START = re.compile(r"^###")
HEADING_PARTS = re.compile(r"^###\s*(\S*)(?:\s+(\S+))?(?:\s+(.*?))?\s*$")
FIELD_LINE = re.compile(r"^(\s*)([-*\u2022])(\s*)([A-Za-z][A-Za-z0-9 _-]*?)\s*:(?:\s?(.*))?$")
LIST_LIKE_LINE = re.compile(r"^\s*[-*\u2022]\s*\S")
NOTE_LINE = re.compile(r"^\s*>")
END_LINE_LOOSE = re.compile(r"^\s*end\s+of\s+file\b", re.IGNORECASE)
END_LINE_STRICT = re.compile(r"^END OF FILE \| (.+) \| (\d+) records?$")
END_LINE_TOLERANT = re.compile(r"^\s*end\s+of\s+file\s*\|\s*(.+?)\s*\|\s*(\d+)\s*records?\s*\.?\s*$", re.IGNORECASE)
SUB_PART_PIECE = re.compile(r"^([A-Za-z][A-Za-z0-9 _-]*?)\s*:\s?(.*)$")
NUMBER_VALUE = re.compile(r"^-?\d+(?:\.\d+)?$")
QUOTED_STRING = r'["\u201c][^"\u201c\u201d]+["\u201d]'
QUOTE_ANCHOR = re.compile(r"^(" + QUOTED_STRING + r")(?:\s+to\s+(" + QUOTED_STRING + r"))?$")
LINE_NUMBERS = re.compile(r"^\d+(?:\s*-\s*\d+)?(?:\s*,\s*\d+(?:\s*-\s*\d+)?)*$")
STORY_POINT = re.compile(r"^(\S+)\s+(" + QUOTED_STRING + r")(?:\s*=\s*(\S+))?$")
POINT_VALUE = re.compile(r"^\[\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*(?:,\s*(-?\d+(?:\.\d+)?)\s*)?\]$")
SPAN_VALUE = re.compile(r"^(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)$")
DATE_VALUE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BECAUSE_LINE_ITEM = re.compile(r"^line:\s*(\d+(?:\s*-\s*\d+)?|" + QUOTED_STRING + r"(?:\s+to\s+" + QUOTED_STRING + r")?)$")
FIELD_PATH = re.compile(r"^(.+)\.([a-z][a-z0-9_]*)$")

# Plain words for the patterns schema.json uses without a written syntax, for problem lines.
PATTERN_WORDS = {
    "^[a-z]$": "one lowercase letter, as a",
    "^[A-Z]$": "one capital letter, as A",
    "^[A-Z0-9_]+$": "capitals, digits and underscores, as TABLE",
    "^[a-z_]+ing$": "one -ing word, as proving",
    "^[DN]\\d+$": "D or N and a number, as D1 or N2",
    "^[01] [01] [01] [01] [01]$": "five digits 0 or 1 separated by spaces, as 1 1 0 1 1",
    "^\\d{1,2}(-\\d{1,2})?$": "a number or a range, as 4-6",
    "^\\d+-\\d+$": "first-last frame numbers, as 1-48",
    "^(\\d+|1_per_scene|share)$": "a number, 1_per_scene, or share",
}


# ---------------------------------------------------------------- the skill's data files

_data_cache = {}


def load_json(relative_path, skill_folder=None):
    """Load one JSON file of the skill folder (for example SCHEMA_FILE, '_config/schema/schema.json'), cached."""
    folder = Path(skill_folder) if skill_folder else SKILL_FOLDER
    path = folder / relative_path
    key = str(path)
    if key not in _data_cache:
        with open(path, encoding="utf-8") as handle:
            _data_cache[key] = json.load(handle)
    return _data_cache[key]


def load_skill_data(skill_folder=None):
    """The schema (as a Schema), the word lists and the constants of the skill folder."""
    schema = Schema(load_json(SCHEMA_FILE, skill_folder))
    words = load_json(WORDS_FILE, skill_folder)
    constants = load_json(CONSTANTS_FILE, skill_folder)
    return schema, words, constants


# ---------------------------------------------------------------- names and words

def normalise_name(written):
    """A field name or sub-part key as the schema writes it: lowercase, spaces and hyphens as underscores (G4).
    A missing name (None) reads as ""."""
    if written is None:
        return ""
    name = str(written).strip().lower()
    name = re.sub(r"[\s\-]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")


def normalise_word(written):
    """A word value compared the G5 way: lowercase, spaces and hyphens read as underscores. A field that is not
    there (record.get gives None) reads as "", so callers never crash on a record that lacks the field."""
    if written is None:
        return ""
    word = str(written).strip().lower()
    word = re.sub(r"[\s\-]+", "_", word)
    word = re.sub(r"_+", "_", word)
    return word


def is_missing(value):
    """True for the words that read as missing (G7): null, N/A, - and blank."""
    return value is None or value.strip().lower() in MISSING_WORDS


def closest(word, choices, count=3):
    """Up to three choices that look like the word, for 'did you mean'."""
    choices = [str(choice) for choice in choices]
    return difflib.get_close_matches(word, choices, n=count, cutoff=0.6)


def quote_for_message(value, limit=60):
    """A value in double quotes for a problem line, shortened in the middle only if very long, and only between
    whole words ("she climbs on past the [shortened] will turn", never half a word)."""
    if len(value) <= limit:
        return '"' + value + '"'
    head = value[: limit - 20]
    if " " in head and not value[len(head)].isspace():
        head = head.rsplit(" ", 1)[0]
    tail = value[-12:]
    if " " in tail and not value[-13].isspace():
        tail = tail.split(" ", 1)[1]
    return '"' + head.rstrip() + " [shortened] " + tail.lstrip() + '"'


# ---------------------------------------------------------------- the schema

class Schema:
    """_config/schema/schema.json with the lookups the grammar and the checks need."""

    def __init__(self, data):
        self.data = data
        self.record_types = data["record_types"]
        self.divider_line = data.get("divider_line", DIVIDER_LINE)
        self.step_order = data["filled_by_step_order"]["values"]
        self.common_fields = {entry["name"]: entry for entry in data["common_fields"]["fields"]}
        self._field_maps = {}
        self._field_orders = {}
        self.id_patterns = {}
        for type_name, record_type in self.record_types.items():
            if record_type.get("id_pattern"):
                self.id_patterns[type_name] = re.compile(record_type["id_pattern"])
        for type_name, other in data.get("other_ids", {}).items():
            self.id_patterns.setdefault(type_name, re.compile(other["pattern"]))
        self.singleton_types = [name for name, record_type in self.record_types.items() if record_type.get("singleton")]

    def knows_type(self, type_name):
        return type_name in self.record_types

    def is_singleton(self, type_name):
        return bool(self.record_types.get(type_name, {}).get("singleton"))

    def field_map(self, type_name):
        """Field name to definition for one record type, including the common fields status, locked and note."""
        if type_name not in self._field_maps:
            fields = {}
            order = {}
            record_type = self.record_types.get(type_name, {})
            for position, definition in enumerate(record_type.get("fields", [])):
                fields[definition["name"]] = definition
                order[definition["name"]] = position
            base = len(order)
            for position, (name, definition) in enumerate(self.common_fields.items()):
                if name not in fields:
                    common = dict(definition)
                    if name == "status" and record_type.get("status_values"):
                        common["values"] = list(record_type["status_values"])
                    fields[name] = common
                    order[name] = base + position
            self._field_maps[type_name] = fields
            self._field_orders[type_name] = order
        return self._field_maps[type_name]

    def field(self, type_name, field_name):
        return self.field_map(type_name).get(field_name)

    def field_names(self, type_name):
        return list(self.field_map(type_name).keys())

    def field_position(self, type_name, field_name):
        """The field's place in the schema's order (unknown fields go last)."""
        self.field_map(type_name)
        return self._field_orders[type_name].get(field_name, 10_000)

    def id_pattern(self, type_name):
        return self.id_patterns.get(type_name)

    def types_for_id(self, identifier):
        """The record types (and other ID kinds) whose pattern the identifier matches."""
        return [name for name, pattern in self.id_patterns.items() if pattern.fullmatch(identifier)]

    def id_matches(self, identifier, id_types):
        """True when the identifier fits one of the accepted types ('*' accepts any ID or a singleton's type name)."""
        if not id_types or "*" in id_types:
            if any(pattern.fullmatch(identifier) for pattern in self.id_patterns.values()):
                return True
            return identifier in self.singleton_types or identifier == "PROJECT"
        for type_name in id_types:
            pattern = self.id_patterns.get(type_name)
            if pattern and pattern.fullmatch(identifier):
                return True
            if (type_name in self.singleton_types or type_name == "PROJECT") and identifier == type_name:
                return True
        return False

    def step_rank(self, step):
        """A filled_by_step value (0-11, a checkpoint letter or an add-on) as a number to compare."""
        if step is None:
            return None
        key = str(step)
        if key in self.step_order:
            return self.step_order[key]
        if key.isdigit():
            return int(key)
        return 99

    def writers(self, definition):
        """Every writer a field can have: its writer, or each writer of its writer_when list."""
        if definition.get("writer"):
            return [definition["writer"]]
        return [entry["writer"] for entry in definition.get("writer_when", [])]

    def id_syntax(self, type_name):
        record_type = self.record_types.get(type_name, {})
        return record_type.get("id_syntax") or "", record_type.get("id_example") or ""


# ---------------------------------------------------------------- problem lines (blueprint 7.2)

class Problem(str):
    """One problem line: level, check ID, record, field, what is wrong, then the allowed values or the fix.

    A Problem is a str (the line itself) that also keeps its parts, so checks can return plain lines and
    the checker can still count errors, warnings and notes.
    Example: E FORM-04 SC10-SH150 size "closeup shot" is not an allowed value. Did you mean close_up?
    """

    def __new__(cls, level, check_id, record, field_name, what, fix="", file_name=None, line_number=None):
        head = f"{level} {check_id} {record}"
        if field_name:
            head += f" {field_name}"
        text = f"{head} {what}".rstrip()
        if not text.endswith((".", "?", "!")):
            text += "."
        if fix:
            text += " " + fix.strip()
            if not text.endswith((".", "?", "!", '"')):
                text += "."
        location = []
        if file_name:
            location.append(str(file_name))
        if line_number:
            location.append(f"line {line_number}")
        if location:
            text += " [" + ", ".join(location) + "]"
        instance = super().__new__(cls, text)
        instance.level = level
        instance.check_id = check_id
        instance.record = record
        instance.field_name = field_name
        instance.what = what
        instance.fix = fix
        instance.file_name = file_name
        instance.line_number = line_number
        return instance

    @property
    def is_error(self):
        return self.level == "E"


def count_levels(problems):
    """How many errors (E), warnings (W) and notes (N) a list of problem lines holds."""
    counts = {"E": 0, "W": 0, "N": 0}
    for problem in problems:
        level = getattr(problem, "level", str(problem)[:1])
        counts[level] = counts.get(level, 0) + 1
    return counts


# ---------------------------------------------------------------- the parts of a file

@dataclass
class FieldLine:
    """One field line `- <field>: <value>` (G4)."""
    name: str
    value: str
    raw: str = None
    line_number: int = None
    written_name: str = None
    tidy_notes: list = dataclass_field(default_factory=list)
    changed: bool = False

    @property
    def missing(self):
        return is_missing(self.value)

    def canonical(self):
        return f"- {self.name}: {self.value}".rstrip()


@dataclass
class OtherLine:
    """A line inside a record that is not a field: a note (G8), a blank line or loose free text (G1)."""
    kind: str
    raw: str
    line_number: int = None


@dataclass
class EndLine:
    """The END line (G9): END OF FILE | <what the file holds> | <n> records."""
    raw: str
    what: str
    count: int
    line_number: int = None
    strict: bool = True
    changed: bool = False

    def canonical(self):
        return f"END OF FILE | {self.what} | {self.count} records"


@dataclass
class Record:
    """One record: `### <TYPE> <ID> <title>` and the lines under it (G2, G3)."""
    type_name: str
    identifier: str = None
    title: str = ""
    heading_raw: str = None
    heading_line_number: int = None
    body: list = dataclass_field(default_factory=list)
    file_name: str = None
    known_type: bool = True
    written_type: str = None
    written_identifier: str = None
    heading_tidy_notes: list = dataclass_field(default_factory=list)
    heading_changed: bool = False
    is_new: bool = False
    structure_changed: bool = False
    copies: list = None

    @property
    def key(self):
        return (self.type_name, self.identifier)

    @property
    def label(self):
        """How problem lines name the record: its ID, or its type for a singleton."""
        return self.identifier or self.type_name

    @property
    def fields(self):
        return [line for line in self.body if isinstance(line, FieldLine)]

    @property
    def notes(self):
        return [line.raw for line in self.body if isinstance(line, OtherLine) and line.kind == "note"]

    @property
    def loose_lines(self):
        return [line for line in self.body if isinstance(line, OtherLine) and line.kind == "loose"]

    @property
    def changed(self):
        return (self.is_new or self.heading_changed or self.structure_changed
                or any(line.changed for line in self.fields))

    def field_lines(self, name):
        return [line for line in self.fields if line.name == name]

    def has(self, name):
        return any(not line.missing for line in self.field_lines(name))

    def get(self, name, default=None):
        """The value of a field (its first line), or default when absent or missing (G7)."""
        for line in self.field_lines(name):
            if not line.missing:
                return line.value.strip()
        return default

    def get_all(self, name):
        """Every value of a repeatable field, in order, leaving out missing ones."""
        return [line.value.strip() for line in self.field_lines(name) if not line.missing]

    def field_names(self):
        names = []
        for line in self.fields:
            if line.name not in names:
                names.append(line.name)
        return names

    def heading_canonical(self):
        parts = ["###", self.type_name]
        if self.identifier:
            parts.append(self.identifier)
        if self.title:
            parts.append(self.title)
        return " ".join(parts)

    # -------------------------------------------------- editing (used by apply and by code that writes records)

    def _insert_position(self, name, schema):
        """Where a new field line goes: after the last field that comes before it in the schema's order."""
        own = schema.field_position(self.type_name, name) if schema else 10_000
        position = None
        for index, line in enumerate(self.body):
            if isinstance(line, FieldLine):
                other = schema.field_position(self.type_name, line.name) if schema else 0
                if other <= own:
                    position = index + 1
        if position is not None:
            return position
        for index, line in enumerate(self.body):
            if isinstance(line, FieldLine):
                return index
        position = 0
        for index, line in enumerate(self.body):
            if not (isinstance(line, OtherLine) and line.kind == "blank"):
                position = index + 1
        return position

    def set_field(self, name, value, schema=None):
        """Give a single-value field one value: replace the first line, drop other lines of that name."""
        self.set_items(name, [value], schema)

    def set_items(self, name, values, schema=None):
        """Replace every line of a field by one line per value, at the place of the first old line."""
        values = [str(value) for value in values]
        old_indexes = [index for index, line in enumerate(self.body)
                       if isinstance(line, FieldLine) and line.name == name]
        old_values = [self.body[index].value for index in old_indexes]
        if old_values == values and all(not self.body[index].changed for index in old_indexes):
            return
        if old_indexes:
            first = old_indexes[0]
            reuse = [self.body[index] for index in old_indexes]
            for index in reversed(old_indexes):
                del self.body[index]
            new_lines = []
            for position, value in enumerate(values):
                if position < len(reuse) and reuse[position].value == value and not reuse[position].changed:
                    new_lines.append(reuse[position])
                else:
                    new_lines.append(FieldLine(name=name, value=value, written_name=name, changed=True))
            self.body[first:first] = new_lines
        else:
            position = self._insert_position(name, schema)
            new_lines = [FieldLine(name=name, value=value, written_name=name, changed=True) for value in values]
            self.body[position:position] = new_lines
        self.structure_changed = True

    def remove_field(self, name):
        before = len(self.body)
        self.body = [line for line in self.body if not (isinstance(line, FieldLine) and line.name == name)]
        if len(self.body) != before:
            self.structure_changed = True

    def add_note(self, text):
        position = len(self.body)
        while position > 0 and isinstance(self.body[position - 1], OtherLine) and self.body[position - 1].kind == "blank":
            position -= 1
        self.body.insert(position, OtherLine(kind="note", raw="> " + text))
        self.structure_changed = True


@dataclass
class RecordFile:
    """A parsed record file: an ordered list of segments, each free text, a record or the END line."""
    name: str
    segments: list = dataclass_field(default_factory=list)
    newline: str = "\n"
    byte_order_mark: bool = False
    final_newline: bool = True
    path: object = None

    @property
    def records(self):
        return [segment for segment in self.segments if isinstance(segment, Record)]

    @property
    def end_lines(self):
        return [segment for segment in self.segments if isinstance(segment, EndLine)]

    @property
    def end_line(self):
        ends = self.end_lines
        return ends[-1] if ends else None

    @property
    def text_lines(self):
        """Every line of free text (G1), with its line number."""
        lines = []
        for segment in self.segments:
            if isinstance(segment, TextBlock):
                lines.extend(zip(segment.line_numbers, segment.lines))
        return lines

    @property
    def has_divider(self):
        return any(line.strip() == DIVIDER_LINE for _, line in self.text_lines)

    def lines_after_end(self):
        """Non-blank lines after the first END line (a file ends with its END line, G9)."""
        seen_end = False
        after = []
        for segment in self.segments:
            if isinstance(segment, EndLine):
                if seen_end:
                    after.append((segment.line_number, segment.raw))
                seen_end = True
            elif seen_end:
                if isinstance(segment, TextBlock):
                    after.extend((number, line) for number, line in zip(segment.line_numbers, segment.lines)
                                 if line.strip())
                elif isinstance(segment, Record):
                    after.append((segment.heading_line_number, segment.heading_raw or segment.heading_canonical()))
        return after

    def find(self, type_name, identifier):
        for record in self.records:
            if record.type_name == type_name and record.identifier == identifier:
                return record
        return None


@dataclass
class TextBlock:
    """Free text between records (G1): kept exactly and ignored by the parser."""
    lines: list = dataclass_field(default_factory=list)
    line_numbers: list = dataclass_field(default_factory=list)


# ---------------------------------------------------------------- reading

def split_text_lines(text):
    """The lines of a text, with its newline style, byte-order mark and final newline remembered."""
    byte_order_mark = text.startswith("\ufeff")
    if byte_order_mark:
        text = text[1:]
    newline = "\r\n" if "\r\n" in text else "\n"
    if newline == "\r\n":
        text = text.replace("\r\n", "\n")
    final_newline = text.endswith("\n")
    lines = text.split("\n")
    if final_newline:
        lines = lines[:-1]
    return lines, newline, byte_order_mark, final_newline


def read_heading(line, schema):
    """TYPE, ID and title of a record heading, with tidy notes (case, stray punctuation)."""
    match = HEADING_PARTS.match(line)
    written_type = match.group(1) if match else ""
    second = (match.group(2) or "") if match else ""
    rest = (match.group(3) or "") if match else ""
    notes = []
    type_name = written_type.rstrip(":.").upper() if written_type else ""
    known = schema.knows_type(type_name) if schema else bool(type_name)
    if known and type_name != written_type:
        notes.append(f'record type "{written_type}" read as {type_name}')
    identifier = None
    title = ""
    written_identifier = None
    if known and schema and schema.is_singleton(type_name):
        title = " ".join(part for part in (second, rest) if part)
    else:
        written_identifier = second or None
        identifier = second or None
        title = rest
        if identifier and known and schema:
            pattern = schema.id_pattern(type_name)
            if pattern and not pattern.fullmatch(identifier):
                candidate = identifier.rstrip(".,:;").upper()
                if pattern.fullmatch(candidate):
                    notes.append(f'ID "{identifier}" read as {candidate}')
                    identifier = candidate
    return type_name, identifier, title, known, written_type, written_identifier, notes


def read_field_line(line, line_number):
    """A FieldLine when the line is a field line (G4), else None."""
    match = FIELD_LINE.match(line)
    if not match:
        return None
    indent, bullet, space, written_name, value = match.groups()
    name = normalise_name(written_name)
    notes = []
    if indent or bullet != "-" or space != " ":
        notes.append(f'the line "{line.strip()[:40]}" read as a field line; a field line starts with "- " (a dash and a space)')
    if written_name != name:
        notes.append(f'field name "{written_name}" read as {name}')
    return FieldLine(name=name, value=(value or "").strip(), raw=line, line_number=line_number,
                     written_name=written_name, tidy_notes=notes)


def parse_text(text, file_name="record file", schema=None):
    """Parse a record file's text into a RecordFile (G1-G3, G8, G9), keeping every line."""
    lines, newline, byte_order_mark, final_newline = split_text_lines(text)
    record_file = RecordFile(name=file_name, newline=newline, byte_order_mark=byte_order_mark,
                             final_newline=final_newline)
    current = None

    def close_record():
        nonlocal current
        if current is not None:
            record_file.segments.append(current)
            current = None

    def add_text(line, line_number):
        if not record_file.segments or not isinstance(record_file.segments[-1], TextBlock):
            record_file.segments.append(TextBlock())
        record_file.segments[-1].lines.append(line)
        record_file.segments[-1].line_numbers.append(line_number)

    for line_number, line in enumerate(lines, start=1):
        if END_LINE_LOOSE.match(line):
            close_record()
            strict = END_LINE_STRICT.match(line)
            tolerant = strict or END_LINE_TOLERANT.match(line)
            if tolerant:
                record_file.segments.append(EndLine(raw=line, what=tolerant.group(1).strip(),
                                                    count=int(tolerant.group(2)), line_number=line_number,
                                                    strict=bool(strict)))
            else:
                record_file.segments.append(EndLine(raw=line, what="", count=-1, line_number=line_number,
                                                    strict=False))
            continue
        if HEADING_START.match(line):
            close_record()
            type_name, identifier, title, known, written_type, written_identifier, notes = read_heading(line, schema)
            current = Record(type_name=type_name, identifier=identifier, title=title, heading_raw=line,
                             heading_line_number=line_number, file_name=file_name, known_type=known,
                             written_type=written_type, written_identifier=written_identifier,
                             heading_tidy_notes=notes)
            continue
        if line.startswith("#") or line.strip() == "---":
            close_record()
            add_text(line, line_number)
            continue
        if current is None:
            add_text(line, line_number)
            continue
        field_line = read_field_line(line, line_number)
        if field_line is not None:
            current.body.append(field_line)
        elif NOTE_LINE.match(line):
            current.body.append(OtherLine(kind="note", raw=line, line_number=line_number))
        elif not line.strip():
            current.body.append(OtherLine(kind="blank", raw=line, line_number=line_number))
        else:
            current.body.append(OtherLine(kind="loose", raw=line, line_number=line_number))
    close_record()
    return record_file


def parse_file(path, name=None, schema=None):
    """Parse a record file on disk. name is how messages name it (default: the file name)."""
    path = Path(path)
    with open(path, encoding="utf-8", newline="") as handle:
        text = handle.read()
    record_file = parse_text(text, name or path.name, schema)
    record_file.path = path
    return record_file


# ---------------------------------------------------------------- writing

def record_lines(record, schema=None, canonical=False):
    """The lines of one record: exactly as read when unchanged, canonical where changed or new."""
    if canonical or record.is_new:
        lines = [record.heading_canonical()]
        field_lines = [line for line in record.body if isinstance(line, FieldLine)]
        if schema is not None:
            field_lines = sorted(field_lines, key=lambda line: schema.field_position(record.type_name, line.name))
        lines.extend(line.canonical() for line in field_lines)
        lines.extend(line.raw for line in record.body if isinstance(line, OtherLine) and line.kind in ("note", "loose"))
        return lines
    lines = [record.heading_canonical() if (record.heading_changed or record.heading_raw is None)
             else record.heading_raw]
    for line in record.body:
        if isinstance(line, FieldLine):
            lines.append(line.canonical() if (line.changed or line.raw is None) else line.raw)
        else:
            lines.append(line.raw)
    return lines


def count_records(record_file):
    """n of the END line: every ### record in the file (G9)."""
    return len(record_file.records)


def render_file(record_file, schema=None, recount=True):
    """The whole text of a record file: unchanged parts exactly as read, changed and new records in canonical form.

    With recount, the END line is counted again when records were added or changed (a file nobody changed keeps
    its END line exactly as it was, even a wrong one, so a write after a read never hides a problem).
    """
    output = []
    records_changed = any(record.changed for record in record_file.records) or getattr(record_file, "records_removed", False)
    segments = record_file.segments
    for index, segment in enumerate(segments):
        if isinstance(segment, TextBlock):
            output.extend(segment.lines)
        elif isinstance(segment, Record):
            canonical = segment.is_new or segment.heading_raw is None
            if canonical and output and output[-1].strip():
                output.append("")
            output.extend(record_lines(segment, schema))
            if canonical and index + 1 < len(segments):
                following = segments[index + 1]
                first_line = following.lines[0] if isinstance(following, TextBlock) and following.lines else None
                if not isinstance(following, TextBlock) or (first_line is not None and first_line.strip()):
                    output.append("")
        elif isinstance(segment, EndLine):
            count = count_records(record_file)
            if segment.changed or segment.raw is None or (recount and records_changed and count != segment.count):
                segment.count = count
                output.append(segment.canonical())
            else:
                output.append(segment.raw)
    text = record_file.newline.join(output)
    if record_file.final_newline:
        text += record_file.newline
    if record_file.byte_order_mark:
        text = "\ufeff" + text
    return text


def write_file(record_file, path=None, schema=None):
    """Write a record file to disk (its own path by default) and return the path."""
    target = Path(path or record_file.path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(render_file(record_file, schema))
    record_file.path = target
    return target


def ensure_end_line(record_file, what):
    """Give a file its END line (at the end) if it has none; the count is filled in when it is written."""
    if not record_file.end_lines:
        if record_file.segments and isinstance(record_file.segments[-1], Record):
            last = record_file.segments[-1]
            if not (last.body and isinstance(last.body[-1], OtherLine) and last.body[-1].kind == "blank") and not last.is_new:
                last.body.append(OtherLine(kind="blank", raw=""))
                last.structure_changed = True
        record_file.segments.append(EndLine(raw=None, what=what, count=0, changed=True))
    return record_file


def make_record(type_name, identifier=None, title="", fields=(), file_name=None):
    """A new record built by code: fields is a list of (name, value) pairs, repeated names for items."""
    record = Record(type_name=type_name, identifier=identifier, title=title or "", file_name=file_name,
                    is_new=True, heading_raw=None)
    for name, value in fields:
        record.body.append(FieldLine(name=name, value=str(value), written_name=name, changed=True))
    return record


def sort_key_for_identifier(identifier):
    """Natural order for IDs: SC10-SH150 before SC10-SH1000, SC06 before SC06A before SC07."""
    if identifier is None:
        return ()
    return tuple(int(part) if part.isdigit() else part for part in re.split(r"(\d+)", identifier))


def add_record(record_file, record, schema=None, type_order=None):
    """Put a new record into a file in canonical order: among its type, by ID; types in type_order."""
    record.file_name = record_file.name
    type_order = type_order or []

    def order_of(item):
        type_position = type_order.index(item.type_name) if item.type_name in type_order else len(type_order)
        return (type_position, sort_key_for_identifier(item.identifier))

    new_order = order_of(record)
    insert_at = None
    last_record_index = None
    for index, segment in enumerate(record_file.segments):
        if isinstance(segment, Record):
            last_record_index = index
            if insert_at is None and order_of(segment) > new_order:
                insert_at = index
    if insert_at is None:
        if last_record_index is not None:
            insert_at = last_record_index + 1
        else:
            end_indexes = [index for index, segment in enumerate(record_file.segments) if isinstance(segment, EndLine)]
            insert_at = end_indexes[0] if end_indexes else len(record_file.segments)
    previous = record_file.segments[insert_at - 1] if insert_at > 0 else None
    if isinstance(previous, Record) and not previous.is_new:
        if not (previous.body and isinstance(previous.body[-1], OtherLine) and previous.body[-1].kind == "blank"):
            previous.body.append(OtherLine(kind="blank", raw=""))
            previous.structure_changed = True
    record_file.segments.insert(insert_at, record)
    return record


def new_record_file(name, title_lines, what, newline="\n"):
    """An empty record file: the plain part (title_lines), the divider line, and an END line (G9)."""
    record_file = RecordFile(name=name, newline=newline)
    block = TextBlock()
    for line in list(title_lines) + ["", DIVIDER_LINE, ""]:
        block.lines.append(line)
        block.line_numbers.append(None)
    record_file.segments.append(block)
    record_file.segments.append(EndLine(raw=None, what=what, count=0, changed=True))
    return record_file


# ---------------------------------------------------------------- splitting values

def split_outside_quotes(value, separator):
    """Split on a separator that is not inside double quotes (straight or curly)."""
    pieces = []
    current = []
    inside = False
    index = 0
    length = len(separator)
    while index < len(value):
        character = value[index]
        if character in OPENING_QUOTES and not inside:
            inside = True
        elif character in CLOSING_QUOTES and inside:
            inside = False
        if not inside and value.startswith(separator, index):
            pieces.append("".join(current))
            current = []
            index += length
            continue
        current.append(character)
        index += 1
    pieces.append("".join(current))
    return pieces


def split_list(value):
    """The items of a comma list (id_list, word_list ...); a comma inside double quotes does not split (G5)."""
    return [piece.strip() for piece in split_outside_quotes(value, ",") if piece.strip()]


@dataclass
class Item:
    """One item of a repeatable field (G6): a first part and named sub-parts."""
    first: str = None
    parts: list = dataclass_field(default_factory=list)
    unnamed: list = dataclass_field(default_factory=list)

    def get(self, key, default=None):
        for name, value in self.parts:
            if name == key:
                return value
        return default

    def keys(self):
        return [name for name, _ in self.parts]


def split_item(value, definition=None):
    """Split an item into its first part and named sub-parts. definition decides whether a first part exists."""
    pieces = [piece.strip() for piece in split_outside_quotes(value, SUB_PART_SEPARATOR)]
    item = Item()
    has_first_part = definition is None or definition.get("first_part", {}) is not None
    if has_first_part:
        item.first = pieces[0] if pieces else ""
        pieces = pieces[1:]
    for piece in pieces:
        match = SUB_PART_PIECE.match(piece)
        if match:
            item.parts.append((normalise_name(match.group(1)), match.group(2).strip()))
        else:
            item.unnamed.append(piece)
    return item


def parse_line_numbers(value):
    """Line numbers and ranges as (first, last) pairs, or None when the value is not in that form."""
    if not LINE_NUMBERS.match(value.strip()):
        return None
    ranges = []
    for piece in value.split(","):
        piece = piece.strip()
        if "-" in piece:
            first, last = [int(part) for part in piece.split("-")]
        else:
            first = last = int(piece)
        ranges.append((first, last))
    return ranges


def parse_quote_anchor(value):
    """The quoted strings of a quote anchor (one, or a pair joined by 'to'), or None."""
    match = QUOTE_ANCHOR.match(value.strip())
    if not match:
        return None
    return [part[1:-1] for part in match.groups() if part]


def parse_story_point(value):
    """(scene ID, quoted words, resolved beat or None) of a story point, or None when it is not one."""
    match = STORY_POINT.match(value.strip())
    if not match:
        return None
    return match.group(1), match.group(2)[1:-1], match.group(3)


# ---------------------------------------------------------------- examining values against their kinds

@dataclass
class ValueIssue:
    """A finding about one value: FORM-04 (not allowed), FORM-12 (sub-parts, bars) or FORM-13 (tidied)."""
    check_id: str
    what: str
    fix: str = ""
    level: str = "E"


class ValueExaminer:
    """Examines field values against their kinds (G5-G7) and returns the tidied value and any issues."""

    def __init__(self, schema, words=None):
        self.schema = schema
        self.words = words or {}
        synonyms = (self.words.get("value_synonyms") or {}).get("fields", {})
        self.value_synonyms = {name: {normalise_word(key): target for key, target in table.items()}
                               for name, table in synonyms.items()}

    # -- helpers
    def allowed_words(self, definition):
        return [str(value) for value in (definition.get("values") or [])]

    def also_allowed(self, definition):
        return [str(value) for value in (definition.get("also_allowed") or [])]

    def empty_word_issue(self, word, definition, field_definition, repeat):
        """None when the empty word (none, open, auto) is allowed here, else a FORM-04 issue (G7)."""
        allowed = [value.lower() for value in self.allowed_words(definition) + self.also_allowed(definition)]
        first_part = definition.get("first_part") or {}
        allowed += [str(value).lower() for value in (first_part.get("values") or [])]
        if word == "none":
            if (definition.get("kind") in ("text", "id_list", "text_list", "file") or repeat or "none" in allowed
                    or definition.get("kind") == "sub_parts" and repeat):
                return None
            return ValueIssue("FORM-04", "is none, which is not allowed here",
                              "Fix: write a value" + self.allowed_text(definition))
        if word == "open":
            writers = self.schema.writers(field_definition or definition)
            if any(writer in ("ai", "user") for writer in writers) or "open" in allowed:
                return None
            return ValueIssue("FORM-04", "is open, but only fields the AI or the user write may be open",
                              "Fix: write the value")
        if word == "auto":
            if "auto" in allowed:
                return None
            return ValueIssue("FORM-04", "is auto, which is allowed only where code decides this field",
                              "Fix: write the value" + self.allowed_text(definition))
        return None

    def allowed_text(self, definition, limit=14):
        values = self.allowed_words(definition) + [value for value in self.also_allowed(definition)
                                                   if not value.startswith("<")]
        if not values:
            return ""
        shown = values[:limit]
        more = "" if len(values) <= limit else f" and {len(values) - limit} more"
        return ". Allowed: " + ", ".join(shown) + more

    def did_you_mean(self, word, choices):
        matches = closest(word, choices)
        return f"Did you mean {matches[0]}?" if matches else ""

    # -- the kinds
    def examine(self, value, definition, key, field_definition=None, repeat=False):
        """Examine one value (a field value, a first part or a sub-part value).

        Returns (tidied value, list of ValueIssue). key is the field name or sub-part key, for value synonyms.
        """
        issues = []
        kind = definition.get("kind", "text")
        stripped = value.strip()
        if stripped != value:
            value = stripped
        lowered = value.lower()
        if lowered in ("none", "open", "auto"):
            issue = self.empty_word_issue(lowered, definition, field_definition, repeat)
            if issue:
                return value, [issue]
            if value != lowered:
                issues.append(ValueIssue("FORM-13", f"{quote_for_message(value)} read as {lowered}", level="N"))
            return lowered, issues
        extra_words = [item.lower() for item in self.also_allowed(definition) if not item.startswith("<")]
        if extra_words and normalise_word(value) in extra_words:
            word = normalise_word(value)
            if word != value:
                issues.append(ValueIssue("FORM-13", f"{quote_for_message(value)} read as {word}", level="N"))
            return word, issues
        if kind != "sub_parts" and SUB_PART_SEPARATOR in value:
            return value, [ValueIssue("FORM-12", f'has " | " inside a value of kind {kind}',
                                      "Fix: use a semicolon or a comma instead; a bar separates named sub-parts only")]
        pattern = definition.get("pattern")
        if pattern:
            if re.fullmatch(pattern, value):
                return value, issues
            if kind in ("word", "id") and re.fullmatch(pattern, normalise_word(value)):
                tidied = normalise_word(value)
                return tidied, issues + [ValueIssue("FORM-13", f"{quote_for_message(value)} read as {tidied}", level="N")]
            if kind == "id" and re.fullmatch(pattern, value.upper()):
                return value.upper(), issues + [ValueIssue("FORM-13", f"{quote_for_message(value)} read as {value.upper()}", level="N")]
            if kind == "id":
                return value, issues + [ValueIssue("FORM-04", f"{quote_for_message(value)} is not the ID of {' or '.join(definition.get('id_types') or ['a record'])}",
                                                   "Fix: copy the ID exactly as issued (for example " + self.example_id(definition.get("id_types")) + ")")]
            syntax = definition.get("syntax") or PATTERN_WORDS.get(pattern) or f"a value of the form {pattern}"
            return value, issues + [ValueIssue("FORM-04", f"{quote_for_message(value)} does not have the right form",
                                               f"Fix: write {syntax}")]
        method = getattr(self, "examine_" + kind, None)
        if method is None:
            method = self.examine_text
        tidied, found = method(value, definition, key)
        if definition.get("fixed_value") and tidied != definition["fixed_value"]:
            found.append(ValueIssue("FORM-04", f"{quote_for_message(tidied)} differs from the only value this field takes",
                                    f'Fix: write "{definition["fixed_value"]}"'))
        return tidied, issues + found

    def examine_text(self, value, definition, key):
        return value, []

    examine_file = examine_text

    def examine_text_list(self, value, definition, key):
        items = split_list(value)
        if not items:
            return value, [ValueIssue("FORM-04", "is empty", "Fix: write the names separated by commas")]
        return value, []

    def examine_quote(self, value, definition, key):
        if re.fullmatch(QUOTED_STRING, value):
            return value, []
        return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} is not one quotation in double quotes",
                                  'Fix: write the exact story words in double quotes, as "Not mint."')]

    def examine_word(self, value, definition, key):
        allowed = self.allowed_words(definition)
        extra = self.also_allowed(definition)
        if "<ID>" in extra and self.schema.types_for_id(value):
            return value, []
        word = normalise_word(value)
        synonyms = self.value_synonyms.get(key, {})
        if allowed:
            choices = [item.lower() for item in allowed] + [item for item in extra if not item.startswith("<")]
            if value in choices:
                return value, []
            if word in choices:
                return word, [ValueIssue("FORM-13", f"{quote_for_message(value)} read as {word}", level="N")]
            if word in synonyms and synonyms[word] in choices:
                target = synonyms[word]
                return target, [ValueIssue("FORM-13", f"{quote_for_message(value)} read as {target} (a known spelling)", level="N")]
            spoken = value.strip().lower()
            if spoken in synonyms and synonyms[spoken] in choices:
                target = synonyms[spoken]
                return target, [ValueIssue("FORM-13", f"{quote_for_message(value)} read as {target} (a known spelling)", level="N")]
            hint = self.did_you_mean(word, choices)
            if "<ID>" in extra:
                hint = (hint + " " if hint else "") + "An ID is also allowed."
            return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} is not an allowed value",
                                      (hint + " " if hint else "") + self.allowed_text(definition).lstrip(". "))]
        if re.fullmatch(r"[a-z0-9_.]+", value):
            return value, []
        if re.fullmatch(r"[a-z0-9_.]+", word):
            return word, [ValueIssue("FORM-13", f"{quote_for_message(value)} read as {word}", level="N")]
        return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} is not one lowercase word",
                                  "Fix: write one word in lowercase, with underscores between words")]

    def examine_word_list(self, value, definition, key):
        items = split_list(value)
        if not items:
            return value, [ValueIssue("FORM-04", "is empty", "Fix: write the words separated by commas")]
        tidied = []
        issues = []
        for item in items:
            word, found = self.examine_word(item, definition, key)
            tidied.append(word)
            issues.extend(found)
        joined = ", ".join(tidied)
        if joined != value and not any(issue.check_id == "FORM-04" for issue in issues):
            if not issues:
                issues.append(ValueIssue("FORM-13", f"{quote_for_message(value)} read as {joined}", level="N"))
        return joined, issues

    def number_issues(self, number_text, definition):
        number = float(number_text)
        issues = []
        values = definition.get("values")
        if values and number not in [float(item) for item in values]:
            issues.append(ValueIssue("FORM-04", f"{number_text} is not an allowed value",
                                     "Allowed: " + ", ".join(str(item) for item in values)))
        value_range = definition.get("range")
        if value_range and not value_range[0] <= number <= value_range[1]:
            issues.append(ValueIssue("FORM-04", f"{number_text} is outside {value_range[0]} to {value_range[1]}",
                                     f"Fix: write a number from {value_range[0]} to {value_range[1]}"))
        return issues

    def examine_number(self, value, definition, key, kind="number"):
        text = value.strip()
        issues = []
        if not NUMBER_VALUE.match(text):
            suffixes = UNIT_SUFFIXES.get(kind)
            match = None
            if suffixes:
                match = re.fullmatch(r"\$?\s*(-?\d+(?:\.\d+)?)\s*(?:" + suffixes + r")?", text, re.IGNORECASE)
            if match and match.group(1) != text:
                issues.append(ValueIssue("FORM-13", f"{quote_for_message(value)} read as {match.group(1)} (the unit is in the field name)", level="N"))
                text = match.group(1)
            else:
                return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} is not a number",
                                          "Fix: write digits only, with a full stop for decimals; the unit is in the field name")]
        if definition.get("whole") and "." in text:
            if re.fullmatch(r"-?\d+\.0+", text):
                whole = text.split(".")[0]
                issues.append(ValueIssue("FORM-13", f"{text} read as {whole}", level="N"))
                text = whole
            else:
                return value, [ValueIssue("FORM-04", f"{text} is not a whole number", "Fix: write a whole number")]
        found = self.number_issues(text, definition)
        if found:
            return value, found
        return text, issues

    def examine_seconds(self, value, definition, key):
        return self.examine_number(value, definition, key, "seconds")

    def examine_metres(self, value, definition, key):
        return self.examine_number(value, definition, key, "metres")

    def examine_millimetres(self, value, definition, key):
        return self.examine_number(value, definition, key, "millimetres")

    def examine_dollars(self, value, definition, key):
        return self.examine_number(value, definition, key, "dollars")

    def examine_words_per_second(self, value, definition, key):
        return self.examine_number(value, definition, key, "words_per_second")

    def examine_number_list(self, value, definition, key):
        items = split_list(value)
        if not items:
            return value, [ValueIssue("FORM-04", "is empty", "Fix: write numbers separated by commas")]
        tidied = []
        for item in items:
            number, found = self.examine_number(item, definition, key)
            if any(issue.check_id == "FORM-04" for issue in found):
                return value, found
            tidied.append(number)
        joined = ", ".join(tidied)
        if joined != value:
            return joined, [ValueIssue("FORM-13", f"{quote_for_message(value)} read as {joined}", level="N")]
        return value, []

    def examine_yes_no(self, value, definition, key):
        if value in ("yes", "no"):
            return value, []
        word = value.strip().lower().rstrip(".")
        if word in ("yes", "no"):
            return word, [ValueIssue("FORM-13", f"{quote_for_message(value)} read as {word}", level="N")]
        also = self.also_allowed(definition)
        if word in also:
            return word, []
        return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} is not yes or no", "Allowed: yes, no")]

    def examine_charge(self, value, definition, key):
        text = value.strip().replace("\u2212", "-").replace("\u2013", "-")
        if text in CHARGES:
            if text != value:
                return text, [ValueIssue("FORM-13", f"{quote_for_message(value)} read as {text}", level="N")]
            return value, []
        return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} is not a charge",
                                  "Allowed: ---, --, -, 0, +, ++, +++")]

    def examine_point(self, value, definition, key, size=False):
        match = POINT_VALUE.match(value.strip())
        if not match or (size and match.group(3) is None):
            form = "[w, d, h] in metres" if size else "[x, y] or [x, y, z] in metres"
            return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} is not a {'size' if size else 'point'}",
                                      f"Fix: write {form}")]
        numbers = [part for part in match.groups() if part is not None]
        if size and any(float(number) <= 0 for number in numbers):
            return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} has a size that is not above 0",
                                      "Fix: write width, depth and height in metres, each above 0")]
        tidied = "[" + ", ".join(numbers) + "]"
        if tidied != value:
            return tidied, [ValueIssue("FORM-13", f"{quote_for_message(value)} read as {tidied}", level="N")]
        return value, []

    def examine_size(self, value, definition, key):
        return self.examine_point(value, definition, key, size=True)

    def examine_span(self, value, definition, key):
        match = SPAN_VALUE.match(value.strip())
        if not match:
            return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} is not a span",
                                      "Fix: write start-end in seconds from the shot's start, as 4-6")]
        start, end = match.groups()
        if float(start) >= float(end):
            return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} ends before it starts",
                                      "Fix: write start-end with the end later than the start")]
        tidied = f"{start}-{end}"
        if tidied != value:
            return tidied, [ValueIssue("FORM-13", f"{quote_for_message(value)} read as {tidied}", level="N")]
        return value, []

    def examine_date(self, value, definition, key):
        if DATE_VALUE.match(value):
            try:
                datetime.date.fromisoformat(value)
                return value, []
            except ValueError:
                pass
        return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} is not a date",
                                  "Fix: write year-month-day, as 2026-10-02")]

    def examine_lines(self, value, definition, key):
        text = value.strip()
        ranges = parse_line_numbers(text)
        if ranges is not None:
            for first, last in ranges:
                if first > last or first < 1:
                    return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} has the range {first}-{last}, which runs backwards or starts below 1",
                                              "Fix: write first-last with the first line first")]
            tidied = ", ".join(str(first) if first == last else f"{first}-{last}" for first, last in ranges)
            if tidied != value:
                return tidied, [ValueIssue("FORM-13", f"{quote_for_message(value)} read as {tidied}", level="N")]
            return value, []
        if parse_quote_anchor(text) is not None:
            return value, []
        return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} is neither line numbers nor a quote anchor",
                                  'Fix: write line numbers (402, 449-463) or a quote anchor ("Iona chews it." to "street signs either.")')]

    def examine_id(self, value, definition, key, id_types=None):
        id_types = id_types if id_types is not None else definition.get("id_types")
        text = value.strip()
        if self.schema.id_matches(text, id_types):
            return text, []
        extra = self.also_allowed(definition)
        if text in extra:
            return text, []
        if "<scene>-MASTER" in extra and re.fullmatch(r"SC\d{2,3}[A-Z]?-MASTER", text):
            return text, []
        candidate = text.rstrip(".,;:").upper()
        if candidate != text and self.schema.id_matches(candidate, id_types):
            return candidate, [ValueIssue("FORM-13", f"{quote_for_message(value)} read as {candidate}", level="N")]
        wanted = "any record" if (not id_types or "*" in id_types) else " or ".join(id_types)
        return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} is not the ID of {wanted}",
                                  "Fix: copy the ID exactly as issued (for example " + self.example_id(id_types) + ")")]

    def example_id(self, id_types):
        for type_name in (id_types or []):
            if type_name in self.schema.record_types and self.schema.record_types[type_name].get("id_example"):
                return self.schema.record_types[type_name]["id_example"]
            other = self.schema.data.get("other_ids", {}).get(type_name)
            if other:
                return other["example"]
        return "SC10-SH150"

    def examine_id_list(self, value, definition, key):
        items = split_list(value)
        if not items:
            return value, [ValueIssue("FORM-04", "is empty", "Fix: write IDs separated by commas, or none")]
        tidied = []
        for item in items:
            identifier, found = self.examine_id(item, definition, key)
            if any(issue.check_id == "FORM-04" for issue in found):
                return value, found
            tidied.append(identifier)
        joined = ", ".join(tidied)
        if joined != value:
            return joined, [ValueIssue("FORM-13", f"{quote_for_message(value)} read as {joined}", level="N")]
        return value, []

    def examine_id_range(self, value, definition, key):
        text = value.strip()
        if ".." in text and "," not in text:
            pieces = [piece.strip() for piece in text.split("..")]
            if len(pieces) != 2:
                return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} is not an ID range",
                                          "Fix: write first..last, as SC07..SC10")]
            for piece in pieces:
                _, found = self.examine_id(piece, definition, key)
                if found:
                    return value, found
            return value, []
        return self.examine_id_list(value, definition, key)

    def examine_story_point(self, value, definition, key, extra_types=None):
        text = value.strip()
        point = parse_story_point(text)
        if point:
            scene, _, resolved = point
            if not self.schema.id_matches(scene, ["SCENE"]):
                return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} does not start with a scene ID",
                                          'Fix: write the scene ID, a space and a quote anchor, as SC24 "She deletes the way home."')]
            if resolved and not self.schema.id_matches(resolved, ["BEAT"]):
                return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} ends in {resolved}, which is not a beat ID",
                                          "Fix: leave the ending after = to code")]
            return value, []
        if self.schema.id_matches(text, ["BEAT"] + list(extra_types or [])):
            return value, []
        return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} is not a story point",
                                  'Fix: write the scene ID and a quote anchor, as SC24 "She deletes the way home.", or a beat ID from step 7')]

    def examine_story_point_list(self, value, definition, key):
        for item in split_list(value):
            _, found = self.examine_story_point(item, definition, key)
            if found:
                return value, found
        return value, []

    def examine_element_list(self, value, definition, key):
        """IDs, or (until step 4 designs the things) a story point standing for an element with no record yet (C23)."""
        items = split_list(value)
        if not items:
            return value, [ValueIssue("FORM-04", "is empty", "Fix: write IDs separated by commas, or none")]
        for item in items:
            if parse_story_point(item):
                _, found = self.examine_story_point(item, definition, key)
                if found:
                    return value, found
                continue
            _, found = self.examine_id(item, definition, key)
            if any(issue.check_id == "FORM-04" for issue in found):
                return value, [ValueIssue("FORM-04", f"{quote_for_message(item)} is neither an ID of "
                                          f"{' or '.join(definition.get('id_types') or ['a record'])} nor a story point",
                                          'Fix: write IDs (PR-RING, MO-MINT), or before step 4 a story point, as '
                                          'SC10 "the flask"')]
        return value, []

    def examine_scene_or_story_point(self, value, definition, key):
        text = value.strip()
        if self.schema.id_matches(text, ["SCENE"]):
            return value, []
        _, found = self.examine_story_point(text, definition, key, extra_types=definition.get("id_types"))
        if not found:
            return value, []
        return value, [ValueIssue("FORM-04", f"{quote_for_message(value)} is neither a scene ID nor a story point",
                                  'Fix: write a scene ID (SC26) or a story point (SC26 "She pushes gently away from the rail.")')]

    def examine_because_list(self, value, definition, key):
        items = split_list(value)
        if not items:
            return value, [ValueIssue("FORM-04", "is empty", "Fix: write the IDs that justify the shot")]
        if [item.lower() for item in items] == ["default"]:
            return "default", []
        for item in items:
            if item.lower() == "default":
                return value, [ValueIssue("FORM-04", "mixes default with other reasons",
                                          "Fix: write default alone, or only IDs and line references")]
            if BECAUSE_LINE_ITEM.match(item):
                continue
            # one because kind everywhere (fix list C14): the kind's own list of story record types, whatever the
            # field (SHOT because, a SCENE department idea's because ...)
            kind_types = ((self.schema.data.get("kinds") or {}).get("because_list") or {}).get("id_types")
            _, found = self.examine_id(item, definition, key, id_types=kind_types or definition.get("id_types"))
            if found:
                if any(issue.check_id == "FORM-04" for issue in found):
                    return value, [ValueIssue("FORM-04", f"{quote_for_message(item)} is neither an ID of a story record nor a line reference",
                                              'Fix: write IDs (SC10-B07, MO-MINT), line:NNN or line: "<quote anchor>"')]
        return value, []

    def examine_reference_list(self, value, definition, key):
        items = split_list(value)
        if not items:
            return value, [ValueIssue("FORM-04", "is empty", "Fix: write IDs or field paths separated by commas")]
        for item in items:
            if self.schema.id_matches(item, ["*"]):
                continue
            match = FIELD_PATH.match(item)
            if match and self.schema.id_matches(match.group(1), ["*"]):
                owner = match.group(1)
                types = [owner] if owner in self.schema.record_types else [
                    name for name in self.schema.types_for_id(owner) if name in self.schema.record_types]
                if types and not any(self.schema.field(type_name, match.group(2)) for type_name in types):
                    return value, [ValueIssue("FORM-04", f"{quote_for_message(item)} names {match.group(2)}, which is not a field of {types[0]}",
                                              "Fix: write <ID>.<field> with a field of that record")]
                continue
            return value, [ValueIssue("FORM-04", f"{quote_for_message(item)} is neither an ID nor a field path",
                                      "Fix: write an ID or <ID>.<field>, as PROJECT.frame_shape or SC10-SU01.lens_mm")]
        return value, []


def examine_field(examiner, record_type_name, field_line, definition):
    """Examine one field line's value; returns (tidied value, list of (sub-part key or None, ValueIssue))."""
    value = field_line.value.strip()
    repeat = bool(definition.get("repeat"))
    if definition.get("kind") != "sub_parts":
        tidied, issues = examiner.examine(value, definition, field_line.name, definition, repeat)
        return tidied, [(None, issue) for issue in issues]
    lowered = value.lower()
    if lowered in ("none", "open", "auto"):
        issue = examiner.empty_word_issue(lowered, definition, definition, repeat)
        if issue:
            return value, [(None, issue)]
        tidy = [] if value == lowered else [(None, ValueIssue("FORM-13", f"{quote_for_message(value)} read as {lowered}", level="N"))]
        return lowered, tidy
    return examine_item(examiner, value, definition)


def examine_item(examiner, value, definition):
    """Examine an item of a sub_parts field (G6): its first part, then each named sub-part."""
    results = []
    pieces = [piece.strip() for piece in split_outside_quotes(value, SUB_PART_SEPARATOR)]
    first_definition = definition.get("first_part")
    sub_parts = {entry["key"]: entry for entry in definition.get("sub_parts") or []}
    tidied_pieces = []
    if first_definition is not None:
        first = pieces[0] if pieces else ""
        pieces = pieces[1:]
        if not first or SUB_PART_PIECE.match(first) and normalise_name(SUB_PART_PIECE.match(first).group(1)) in sub_parts \
                and first_definition.get("kind") not in ("text",):
            results.append((None, ValueIssue("FORM-12", f"has no first part before its named sub-parts ({quote_for_message(value)})",
                                                     "Fix: start the item with its main value (usually an ID), then the named sub-parts")))
            tidied_pieces.append(first)
        else:
            tidied, issues = examiner.examine(first, first_definition, definition.get("name", ""), definition,
                                              repeat=False)
            if definition.get("defines_id"):
                issues = [ValueIssue("FORM-02", issue.what, issue.fix) if issue.check_id == "FORM-04" else issue
                          for issue in issues]
            results.extend(("first part", issue) for issue in issues)
            tidied_pieces.append(tidied)
    seen = []
    for piece in pieces:
        match = SUB_PART_PIECE.match(piece)
        if not match:
            example_key = next(iter(sub_parts), "key")
            results.append((None, ValueIssue("FORM-12", f"has an unnamed sub-part {quote_for_message(piece)}",
                                             f"Fix: name it, as \"{example_key}: {piece}\"; sub-parts are always key: value")))
            tidied_pieces.append(piece)
            continue
        written_key, sub_value = match.group(1), match.group(2).strip()
        key = normalise_name(written_key)
        if key not in sub_parts:
            hint = closest(key, list(sub_parts))
            fix = (f"Did you mean {hint[0]}? " if hint else "") + "Allowed: " + ", ".join(sub_parts)
            results.append((None, ValueIssue("FORM-12", f"has the unknown sub-part key {written_key}", fix)))
            tidied_pieces.append(piece)
            continue
        if key != written_key:
            results.append((None, ValueIssue("FORM-13", f'has the sub-part key "{written_key}", read as {key}', level="N")))
        if key in seen:
            results.append((None, ValueIssue("FORM-12", f"has the sub-part {key} twice in one item",
                                             "Fix: keep one; a repeatable field takes one line per item")))
        seen.append(key)
        tidied, issues = examiner.examine(sub_value, sub_parts[key], key, definition, repeat=False)
        results.extend((key, issue) for issue in issues)
        tidied_pieces.append(f"{key}: {tidied}")
    return SUB_PART_SEPARATOR.join(tidied_pieces), results


# ---------------------------------------------------------------- merging copies (G10)

@dataclass
class Conflict:
    """The same single-value field with different values in two copies of one record (FORM-09)."""
    type_name: str
    identifier: str
    field_name: str
    values: list
    copy_indexes: list = dataclass_field(default_factory=list)


WORD_LIKE_KINDS = ("word", "word_list", "yes_no", "id", "id_list", "id_range", "charge", "point", "size", "span",
                   "lines", "number_list") + NUMBER_KINDS


def value_for_comparison(value, definition=None):
    """Values compared the tolerant way: spaces around commas and bars ignored; for words, IDs and numbers also
    case, spaces and hyphens (G5), so 'Dialogue duel' and 'dialogue_duel' are the same value."""
    text = re.sub(r"\s*,\s*", ", ", value.strip())
    text = re.sub(r"\s*\|\s*", " | ", text)
    if definition is not None and definition.get("kind") in WORD_LIKE_KINDS:
        text = ", ".join(normalise_word(item) for item in split_list(text))
    return text


def merge_copies(record_files, schema):
    """Merge the records of several files by TYPE and ID (G10).

    Returns (merged records keyed by (type, ID), list of Conflict). A merged record is a new Record whose
    single-value fields hold the first value found and whose repeatable fields hold every distinct item,
    in file order. merged.copies lists the original records.
    """
    groups = {}
    order = []
    for record_file in record_files:
        for record in record_file.records:
            if not record.known_type:
                continue
            key = record.key
            if key not in groups:
                groups[key] = []
                order.append(key)
            groups[key].append(record)
    merged = {}
    conflicts = []
    for key in order:
        copies = groups[key]
        result = Record(type_name=key[0], identifier=key[1], title=copies[0].title, file_name=copies[0].file_name,
                        known_type=True, heading_raw=copies[0].heading_raw)
        result.copies = copies
        values_by_field = {}
        field_order = []
        for copy_index, copy in enumerate(copies):
            for line in copy.fields:
                if line.missing:
                    continue
                if line.name not in values_by_field:
                    values_by_field[line.name] = []
                    field_order.append(line.name)
                values_by_field[line.name].append((line.value.strip(), copy.file_name, line.line_number, copy_index))
        for name in field_order:
            definition = schema.field(key[0], name) if schema else None
            repeat = bool(definition and definition.get("repeat"))
            entries = values_by_field[name]
            if repeat or definition is None:
                seen = set()
                for value, _, _, _ in entries:
                    comparison = value_for_comparison(value, definition if definition and definition.get("kind") != "sub_parts" else None)
                    if comparison in seen:
                        continue
                    seen.add(comparison)
                    result.body.append(FieldLine(name=name, value=value, written_name=name))
            else:
                distinct = []
                for value, file_name, line_number, copy_index in entries:
                    comparison = value_for_comparison(value, definition)
                    if comparison not in [item[0] for item in distinct]:
                        distinct.append((comparison, value, file_name, line_number, copy_index))
                result.body.append(FieldLine(name=name, value=entries[0][0], written_name=name))
                if len(distinct) > 1:
                    conflicts.append(Conflict(key[0], key[1], name,
                                              [(value, file_name, line_number) for _, value, file_name, line_number, _ in distinct],
                                              [copy_index for _, _, _, _, copy_index in distinct]))
        merged[key] = result
    return merged, conflicts
