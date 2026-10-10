"""Conformance test for work package 12a (templates and the gold example of The Catch, scene 10).

Reads _config/schema/schema.json and checks, with its own simple line parser:
1. the gold example (references/examples/01 and 02): every record type is known, every ID fits its type's pattern,
   every field name belongs to its record type (a SETVALUE's lines are checked against its target's type),
   every value fits its kind, allowed words, sub-part keys, number ranges and patterns, END counts match,
   the divider line is there, and every Standard field (depth quick or standard, conditions evaluated, the
   title card's camera fields exempt) is present for scene 10 and every record it cites;
2. the templates: plain part headings with # and ## only, the divider, every stored field of each record
   type in schema order, a note block after each record, and a correct END count (word counts reported);
3. the chat-saved copy under tests/fixtures/chat saved scene 10: the same form checks, plus chat facts
   (code_execution: no, quote anchors instead of line numbers, hear items with their words, two batch files);
4. with the story present (the excerpt tests/fixtures/The Catch - lines 397-489.txt, or --story <path>):
   the excerpt header, every double-quoted string of the scene file is exact story words from scene 10,
   scene 10's story points are found once and hold 3 or more words, every story line is in a beat and a
   shot, every speech is heard, every shot's screen time reaches its floor (shot 150: 13.8 seconds), and every
   quote anchor of the chat copy resolves, by the adopt rule, to the gold's line numbers. With the whole
   story (--story) the whole-film records' quotes and anchors are checked as well.
When the story is absent those checks report "skipped: story not present".

Run from anywhere:
    python tests/wp12a_gold_conformance.py [--story <path to the whole story or the excerpt>]
Standard library only.
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parent.parent
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
SCHEMA_FILE = SKILL / "_config" / "schema" / "schema.json"
CONSTANTS_FILE = SKILL / "_config" / "rules" / "constants.json"
GOLD = SKILL / "references" / "examples" / "01 The Catch - scene 10.md"
GOLD_CONTEXT = SKILL / "references" / "examples" / "02 The Catch - scene 10 - context.md"
TEMPLATES = SKILL / "references" / "templates"
FIXTURES = REPOSITORY / "tests" / "fixtures"
EXCERPT = FIXTURES / "The Catch - lines 397-489.txt"
CHAT_COPY = FIXTURES / "chat saved scene 10"
SCENE_FIRST_LINE, SCENE_LAST_LINE = 397, 489
TEMPLATE_NAMES = ["00 Start here.md", "01 Choices.md", "04 Scene list.md", "05 Story plan.md", "06 World and style.md",
                  "07 Characters and voices.md", "08 Places and things.md", "09 Continuity.md", "10 Film rules.md",
                  "11 Scene.md", "18 Add-on jobs.md"]
EXTRA_TEMPLATE_NAMES = ["13 Health check.md", "22 Rights and credits.md"]
TEMPLATE_TYPES = {
    "00 Start here.md": ["PROJECT"], "01 Choices.md": ["CHOICE", "SETVALUE"], "04 Scene list.md": ["SCENE"],
    "05 Story plan.md": ["PLAN", "SEQUENCE", "PLANT", "FACT", "CHAPTER", "STRAND", "CARDINAL"],
    "06 World and style.md": ["STYLE", "WORLD", "RULE"], "07 Characters and voices.md": ["CHARACTER", "VOICE"],
    "08 Places and things.md": ["LOCATION", "PROP", "TEXT", "MOTIF", "CAMERA"], "09 Continuity.md": ["STATE"],
    "10 Film rules.md": ["CAMSYS", "CAMRULE", "RESERVE", "LENS", "LOOK", "VISUAL", "SOUNDPLAN", "LADDER"],
    "11 Scene.md": ["SCENE", "PART", "BEAT", "SPEECH", "MOVE", "SETUP", "SHOTLIST", "SHOT", "CUT"],
    "13 Health check.md": ["REVIEW", "FINDING"],
    "18 Add-on jobs.md": ["PIC", "PREVIS", "TAKE", "VOICETAKE", "FINISH", "MUSIC"],
    "22 Rights and credits.md": ["RIGHTS"],
}
SCENE_PARTS = {"04 Scene list.md": {"list", "plan"}, "11 Scene.md": {"design"}}

RESULTS = []


def report(passed, group, detail=""):
    RESULTS.append((passed, group))
    print(("PASS  " if passed else "FAIL  ") + group + (f": {detail}" if detail else ""))


def info(line):
    print("INFO  " + line)


def shorten(problems, limit=6):
    return "; ".join(problems[:limit]) + (f" (and {len(problems) - limit} more)" if len(problems) > limit else "")


# ---------------------------------------------------------------- schema

SCHEMA = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
TYPES = SCHEMA["record_types"]
DIVIDER = SCHEMA["divider_line"]
HEADING_PATTERN = re.compile(SCHEMA["record_heading"]["pattern"])
FIELD_PATTERN = re.compile(SCHEMA["field_line"]["pattern"])
END_PATTERN = re.compile(SCHEMA["end_line"]["pattern"])
COMMON_FIELDS = {field["name"]: field for field in SCHEMA["common_fields"]["fields"]}
STEP_ORDER = SCHEMA["filled_by_step_order"]["values"]
ID_PATTERNS = {name: re.compile(record["id_pattern"]) for name, record in TYPES.items() if record.get("id_pattern")}
ID_PATTERNS.update({name: re.compile(other["pattern"]) for name, other in SCHEMA["other_ids"].items()})
SINGLETONS = {name for name, record in TYPES.items() if record.get("singleton")}
CHARGES = {"---", "--", "-", "0", "+", "++", "+++"}
NUMBER = re.compile(r"^-?\d+(\.\d+)?$")
QUOTED = re.compile(r'"([^"]*)"')


def field_definition(type_name, name):
    for field in TYPES[type_name]["fields"]:
        if field["name"] == name:
            return field
    return COMMON_FIELDS.get(name)


def type_of_identifier(identifier):
    for name, pattern in ID_PATTERNS.items():
        if name in TYPES and pattern.match(identifier):
            return name
    return None


# ---------------------------------------------------------------- the line parser

class Record:
    def __init__(self, type_name, identifier, title, file_name, line_number):
        self.type_name = type_name
        self.identifier = identifier
        self.title = title
        self.file_name = file_name
        self.line_number = line_number
        self.fields = []   # (name, value, line number)
        self.notes = []

    def values(self, name):
        return [value for field_name, value, _ in self.fields if field_name == name]

    def value(self, name):
        found = self.values(name)
        return found[0] if found else None

    @property
    def key(self):
        return (self.type_name, self.identifier)

    @property
    def label(self):
        return self.identifier or self.type_name


class RecordFile:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.text = path.read_text(encoding="utf-8")
        self.lines = self.text.split("\n")
        self.plain = []
        self.records = []
        self.end_lines = []
        self.problems = []
        self.divider_count = self.lines.count(DIVIDER)
        self.parse()

    def parse(self):
        below = False
        current = None
        after_check_table = False
        for number, line in enumerate(self.lines, start=1):
            if line == DIVIDER:
                below = True
                continue
            if not below:
                self.plain.append(line)
                continue
            end = END_PATTERN.match(line)
            if end:
                self.end_lines.append((end.group(1), int(end.group(2)), number))
                current = None
                continue
            if line.startswith("### "):
                heading = HEADING_PATTERN.match(line)
                after_check_table = False
                if not heading:
                    self.problems.append(f"{self.name}:{number} heading does not fit the grammar")
                    current = None
                    continue
                type_name, identifier, title = heading.group(1), heading.group(2), heading.group(3)
                if type_name in SINGLETONS and identifier is not None:
                    title = (identifier + " " + (title or "")).strip()
                    identifier = None
                current = Record(type_name, identifier, title, self.name, number)
                self.records.append(current)
                continue
            if line == "---":
                current = None
                after_check_table = True
                continue
            if line.startswith("## ") or line.startswith("# "):
                current = None
                continue
            if current is None:
                continue
            if line.startswith("> "):
                current.notes.append(line)
                continue
            if line.startswith("- "):
                field = FIELD_PATTERN.match(line)
                if not field:
                    self.problems.append(f"{self.name}:{number} field line does not fit the grammar")
                    continue
                current.fields.append((field.group(1), field.group(2), number))
                continue
            if line.strip() and not after_check_table:
                self.problems.append(f"{self.name}:{number} a line inside a record that is not a field or a note")


def split_outside_quotes(value, separator):
    pieces, current, inside, index = [], [], False, 0
    while index < len(value):
        character = value[index]
        if character in '"“”':
            inside = not inside
        if not inside and value.startswith(separator, index):
            pieces.append("".join(current))
            current = []
            index += len(separator)
            continue
        current.append(character)
        index += 1
    pieces.append("".join(current))
    return pieces


# ---------------------------------------------------------------- value checks

def normal_word(value):
    return re.sub(r"[ \-]", "_", value.strip()).lower()


def is_identifier_of(value, id_types, known_identifiers=None):
    value = value.strip()
    if "*" in id_types:
        return bool(type_of_identifier(value)) or value in SINGLETONS or value == "PROJECT" or any(
            pattern.match(value) for pattern in ID_PATTERNS.values())
    for type_name in id_types:
        if type_name in SINGLETONS and value == type_name:
            return True
        pattern = ID_PATTERNS.get(type_name)
        if pattern and pattern.match(value):
            return True
    return False


def check_quote_text(value):
    return bool(re.fullmatch(r'"[^"]+"', value.strip()))


def check_story_point(value):
    value = value.strip()
    if re.fullmatch(r'SC\d{2,3}[A-Z]? "[^"]+"( = SC\d{2,3}[A-Z]?-B\d{2})?', value):
        return True
    return bool(ID_PATTERNS["BEAT"].match(value))


def check_lines(value):
    value = value.strip()
    if re.fullmatch(r"\d+(-\d+)?(, ?\d+(-\d+)?)*", value):
        return True
    anchors = split_outside_quotes(value, ", ")
    return all(re.fullmatch(r'"[^"]+"( to "[^"]+")?', anchor.strip()) for anchor in anchors)


def check_value(definition, value, where, problems, writer=None, repeat=False):
    """Check one value (or first part, or sub-part value) against its definition."""
    kind = definition.get("kind")
    value = value.strip()
    values = [str(item) for item in (definition.get("values") or [])]
    also = [str(item) for item in (definition.get("also_allowed") or [])]
    if value == "":
        problems.append(f"{where}: empty value")
        return
    if value == "open" and writer in ("ai", "user", None):
        return
    if value == "none" and (kind in ("text", "id_list", "text_list", "because_list", "reference_list", "story_point_list",
                                     "element_list")
                            or repeat or "none" in values or "none" in also):
        return
    if value in also:
        return
    if "<ID>" in also and type_of_identifier(value):
        return
    if value == "auto" and "auto" in values:
        return
    pattern = definition.get("pattern")
    if kind == "word":
        if values and normal_word(value) not in [item.lower() for item in values]:
            problems.append(f"{where}: {value!r} is not one of {', '.join(values[:12])}")
        elif not values and pattern and not re.fullmatch(pattern, value):
            problems.append(f"{where}: {value!r} does not fit {pattern}")
        elif not values and not pattern and not re.fullmatch(r"[a-z0-9_]+", normal_word(value)):
            problems.append(f"{where}: {value!r} is not one lowercase word")
        return
    if kind == "word_list":
        for item in [piece.strip() for piece in value.split(",")]:
            if values and normal_word(item) not in [entry.lower() for entry in values]:
                problems.append(f"{where}: {item!r} is not one of {', '.join(values[:12])}")
        return
    if kind in ("number", "seconds", "metres", "millimetres", "dollars", "words_per_second"):
        if not NUMBER.match(value):
            problems.append(f"{where}: {value!r} is not a number")
            return
        if values and value not in values and str(float(value)) not in [str(float(item)) for item in values]:
            problems.append(f"{where}: {value} is not one of {', '.join(values)}")
        if definition.get("range"):
            low, high = definition["range"]
            if not low <= float(value) <= high:
                problems.append(f"{where}: {value} is outside {low}-{high}")
        return
    if kind == "number_list":
        if not all(NUMBER.match(piece.strip()) for piece in value.split(",")):
            problems.append(f"{where}: {value!r} is not a list of numbers")
        return
    if kind == "yes_no":
        if value not in ("yes", "no"):
            problems.append(f"{where}: {value!r} is not yes or no")
        return
    if kind == "id":
        if pattern and re.fullmatch(pattern, value):
            return
        if not is_identifier_of(value, definition.get("id_types") or ["*"]):
            problems.append(f"{where}: {value!r} is not an ID of {', '.join(definition.get('id_types') or ['*'])}")
        return
    if kind == "id_list":
        for item in split_outside_quotes(value, ","):
            if not is_identifier_of(item, definition.get("id_types") or ["*"]):
                problems.append(f"{where}: {item.strip()!r} is not an ID of {', '.join(definition.get('id_types') or ['*'])}")
        return
    if kind == "id_range":
        for item in value.split(","):
            for end in item.split(".."):
                if not type_of_identifier(end.strip()):
                    problems.append(f"{where}: {end.strip()!r} is not an ID")
        return
    if kind == "lines":
        if not check_lines(value):
            problems.append(f"{where}: {value!r} is neither line numbers nor quote anchors")
        return
    if kind == "quote":
        if not check_quote_text(value):
            problems.append(f"{where}: {value!r} is not one double-quoted string")
        return
    if kind == "story_point":
        if not check_story_point(value):
            problems.append(f"{where}: {value!r} is not a story point")
        return
    if kind == "story_point_list":
        for item in split_outside_quotes(value, ", "):
            if not check_story_point(item):
                problems.append(f"{where}: {item!r} is not a story point")
        return
    if kind == "scene_or_story_point":
        if not (ID_PATTERNS["SCENE"].match(value) or check_story_point(value)
                or is_identifier_of(value, definition.get("id_types") or [])):
            problems.append(f"{where}: {value!r} is neither a scene ID nor a story point")
        return
    if kind == "charge":
        if value not in CHARGES:
            problems.append(f"{where}: {value!r} is not a charge")
        return
    if kind == "point":
        if not re.fullmatch(r"\[-?\d+(\.\d+)?(, ?-?\d+(\.\d+)?){1,2}\]", value):
            problems.append(f"{where}: {value!r} is not a point")
        return
    if kind == "size":
        if not re.fullmatch(r"\[\d+(\.\d+)?(, ?\d+(\.\d+)?){2}\]", value):
            problems.append(f"{where}: {value!r} is not a size")
        return
    if kind == "span":
        match = re.fullmatch(r"(\d+(\.\d+)?)-(\d+(\.\d+)?)", value)
        if not match or float(match.group(1)) >= float(match.group(3)):
            problems.append(f"{where}: {value!r} is not a span t0-t1")
        return
    if kind == "date":
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            problems.append(f"{where}: {value!r} is not a date")
        return
    if kind == "because_list":
        items = split_outside_quotes(value, ",")
        for item in items:
            item = item.strip()
            if item == "default" and len(items) == 1:
                continue
            if re.fullmatch(r'line:\s*(\d+|"[^"]+")', item):
                continue
            if not is_identifier_of(item, definition.get("id_types") or ["*"]):
                problems.append(f"{where}: {item!r} is not an ID of {', '.join(definition.get('id_types') or ['*'])} or a line")
        return
    if kind == "element_list":
        # FACT element (fix list C23): IDs, or before step 4 a story point standing for an element with no record yet
        for item in split_outside_quotes(value, ","):
            item = item.strip()
            if not (is_identifier_of(item, definition.get("id_types") or ["*"]) or check_story_point(item)):
                problems.append(f"{where}: {item!r} is neither an ID of {', '.join(definition.get('id_types') or ['*'])} "
                                "nor a story point")
        return
    if kind == "reference_list":
        for item in split_outside_quotes(value, ","):
            item = item.strip()
            base = item.split(".")[0] if not re.match(r"^(CH|PR|LOC)-[A-Z0-9-]+\.S\d{2}", item) else ".".join(item.split(".")[:2])
            if not (type_of_identifier(base) or base in SINGLETONS or base == "PROJECT"):
                problems.append(f"{where}: {item!r} is not an ID or a field path")
        return
    if kind in ("text", "text_list", "file"):
        if pattern and not re.fullmatch(pattern, value):
            problems.append(f"{where}: {value!r} does not fit {pattern}")
        if " | " in value.replace('" | "', ""):
            problems.append(f"{where}: text holds a space, bar, space")
        return
    problems.append(f"{where}: kind {kind!r} is not known to this test")


def check_field(definition, value, where, problems):
    writer = definition.get("writer") or "ai"
    if definition.get("kind") != "sub_parts":
        check_value(definition, value, where, problems, writer, definition.get("repeat", False))
        return
    if value.strip() in ("none", "open") and ("none" in [str(item) for item in definition.get("also_allowed") or []]
                                             or definition.get("repeat") or value.strip() == "open"):
        return
    pieces = split_outside_quotes(value, " | ")
    first = definition.get("first_part")
    sub_parts = {part["key"]: part for part in definition.get("sub_parts") or []}
    start = 0
    if first:
        check_value(first, pieces[0], f"{where} (first part)", problems, writer)
        start = 1
    seen = set()
    for piece in pieces[start:]:
        key, separator, sub_value = piece.partition(": ")
        if not separator or key not in sub_parts:
            problems.append(f"{where}: unknown or unnamed sub-part {piece[:40]!r}")
            continue
        if key in seen:
            problems.append(f"{where}: sub-part {key} twice")
        seen.add(key)
        check_value(sub_parts[key], sub_value, f"{where} {key}", problems, writer)


def check_record_form(record, problems, target_type=None):
    """Type, ID and every field of one record."""
    if record.type_name not in TYPES:
        problems.append(f"{record.file_name}:{record.line_number} unknown record type {record.type_name}")
        return
    definition = TYPES[record.type_name]
    if definition.get("singleton"):
        if record.identifier:
            problems.append(f"{record.file_name}:{record.line_number} {record.type_name} is a singleton and takes no ID")
    elif not record.identifier or not ID_PATTERNS[record.type_name].match(record.identifier):
        problems.append(f"{record.file_name}:{record.line_number} ID {record.identifier!r} does not fit {record.type_name}")
    counts = {}
    for name, value, number in record.fields:
        where = f"{record.file_name}:{number} {record.label}.{name}"
        field = field_definition(record.type_name, name)
        if field is None and record.type_name == "SETVALUE" and target_type:
            field = field_definition(target_type, name)
        if field is None:
            problems.append(f"{where}: no such field")
            continue
        if field.get("stored") is False:
            problems.append(f"{where}: code derives this field; it is never stored")
        counts[name] = counts.get(name, 0) + 1
        if counts[name] == 2 and not field.get("repeat"):
            problems.append(f"{where}: written twice but does not repeat")
        check_field(field, value, where, problems)


def check_file_form(record_file, problems):
    problems.extend(record_file.problems)
    if record_file.divider_count != 1:
        problems.append(f"{record_file.name}: the divider line appears {record_file.divider_count} times")
    for line in record_file.plain:
        if line.startswith("#") and not (line.startswith("# ") or line.startswith("## ")):
            problems.append(f"{record_file.name}: plain part heading {line[:30]!r} is not # or ##")
    if len(record_file.end_lines) != 1:
        problems.append(f"{record_file.name}: {len(record_file.end_lines)} END lines")
    elif record_file.end_lines[0][1] != len(record_file.records):
        problems.append(f"{record_file.name}: END line says {record_file.end_lines[0][1]} records, the file has {len(record_file.records)}")
    identifiers = {}
    for record in record_file.records:
        target_type = None
        if record.type_name == "SETVALUE":
            target = record.value("target") or ""
            target_type = type_of_identifier(target) or (target if target in TYPES else None)
        check_record_form(record, problems, target_type)
        if record.identifier and record.type_name != "SCENE":
            if record.identifier in identifiers:
                problems.append(f"{record_file.name}: ID {record.identifier} twice")
            identifiers[record.identifier] = record


# ---------------------------------------------------------------- required fields (Standard depth)

class Project:
    """The merged records of a set of files, for evaluating conditions."""

    def __init__(self, record_files):
        self.records = []
        for record_file in record_files:
            self.records.extend(record_file.records)
        self.by_key = {}
        for record in self.records:
            self.by_key.setdefault(record.key, []).append(record)

    def merged_values(self, type_name, identifier, name):
        found = []
        for record in self.by_key.get((type_name, identifier), []):
            found.extend(record.values(name))
        return found

    def first(self, type_name, name, identifier=None):
        for record in self.records:
            if record.type_name == type_name and (identifier is None or record.identifier == identifier):
                value = record.value(name)
                if value is not None:
                    return value
        return None

    def scene_of(self, record):
        match = re.match(r"^(SC\d{2,3}[A-Z]?)", record.identifier or "")
        return match.group(1) if match else None

    def scene_tags(self, scene):
        tags = self.merged_values("SCENE", scene, "tags")
        return {tag.strip() for value in tags for tag in value.split(",")}

    def beat_order(self, beat):
        return int(beat.split("-B")[1])


def condition_holds(name, record, project, item=None):
    """True when the condition holds; False when it does not or cannot be told from the records."""
    scene = project.scene_of(record)
    if name == "source_is_screenplay":
        return project.first("PROJECT", "source_kind") == "screenplay"
    if name == "source_not_screenplay":
        return project.first("PROJECT", "source_kind") not in (None, "screenplay")
    if name == "compressing":
        return project.first("PROJECT", "runtime_target_s") not in (None, "as_written") or \
            project.first("PROJECT", "source_kind") == "prose"
    if name == "character_has_cue":
        speaking = [value.split(" | ")[0] for scene_record in project.records if scene_record.type_name == "SCENE"
                    for value in scene_record.values("speaking")]
        return record.identifier in speaking
    if name in ("set_plan_exists", "set_plan_needed"):
        if record.type_name == "LOCATION":
            location = record.identifier
        else:
            location = (project.merged_values("SCENE", scene, "location") or [None])[0]
        if name == "set_plan_needed":
            scenes = [key[1] for key, records in project.by_key.items() if key[0] == "SCENE"
                      and location in project.merged_values("SCENE", key[1], "location")]
            return any(project.scene_tags(one) & {"three_or_more", "glass_and_reflection", "action"} for one in scenes)
        return bool(location and project.merged_values("LOCATION", location, "size"))
    if name == "action_scene":
        return "action" in project.scene_tags(scene)
    if name == "tag_three_or_more":
        return "three_or_more" in project.scene_tags(scene)
    if name == "turn_beat":
        return (record.value("turn") or "none") != "none"
    if name == "turn_or_intense_beat":
        return (record.value("turn") or "none") != "none" or int(record.value("beat_intensity") or 0) >= 4
    if name == "dialogue_pass_beat":
        revealed = [value for fact in project.records if fact.type_name == "FACT"
                    for value in fact.values("audience_knows_from") if value.endswith("= " + record.identifier)]
        return (record.value("turn") or "none") != "none" or bool(record.values("flag")) or bool(revealed)
    if name == "principal":
        return record.value("tier") == "principal"
    if name == "mirror_rule_exists":
        return any(rule.type_name == "RULE" and rule.value("kind") == "mirror" for rule in project.records)
    if name == "mirror_rule":
        return record.value("kind") == "mirror"
    if name == "device_rule":
        return record.value("kind") == "device"
    if name == "fact_mode_needs_record":
        return record.value("mode") in ("suspense", "mystery", "dramatic_irony")
    if name == "fact_element_before_reveal":
        beats = [beat.strip() for beat in (record.value("beats") or "").split(",") if beat.strip()]
        for fact in project.records:
            if fact.type_name != "FACT":
                continue
            reveal = re.search(r"= (SC\d{2,3}[A-Z]?-B\d{2})$", fact.value("audience_knows_from") or "")
            if reveal and reveal.group(1).startswith(scene + "-") and beats and \
                    max(project.beat_order(beat) for beat in beats) < project.beat_order(reveal.group(1)):
                return True
        return False
    if name == "eyeline_set":
        return bool(item and item.get("eyeline") not in (None, "none"))
    if name == "overlapping_slices":
        return (project.merged_values("SCENE", scene, "time_treatment") or [""])[0] == "overlapping_slices"
    if name == "cut_is_split":
        return record.value("type") in ("j_cut", "l_cut")
    if name == "cut_has_black":
        return record.value("type") in ("cut_to_black", "fade", "freeze")
    if name == "cut_is_match":
        return record.value("type") == "match_cut"
    if name == "reserved_choice":
        return any(re.match(r"RC-\d{2}$", item.strip()) for item in (record.value("because") or "").split(","))
    if name == "presentation_on_device":
        return record.value("presentation") in ("on_screen", "recording")
    if name == "choice_answered":
        return record.value("status") == "answered"
    if name == "rights_subject_source":
        return record.value("subject") == "source"
    if name == "text_in_story":
        return record.value("origin") == "story"
    if name == "depth_detailed":
        return project.first("PROJECT", "depth") == "detailed"
    if name == "depth_below_detailed":
        return project.first("PROJECT", "depth") in ("quick", "standard", None)
    if name == "music_policy_allows_cues":
        return project.first("SOUNDPLAN", "music_policy") in ("sparse", "scored")
    if name == "filmed_shot":
        return record.value("kind") not in ("card", "black")
    # when_used, glass_in_frame, subject_moves, later_beat_saves_behaviour, match_cut_or_continuous_action,
    # casting_chosen, storyboard_frame, framing_critical, previs_stub, checker_finding: never demanded here
    return False


def required_at_standard(field, record, project, step_limit=10):
    if field.get("stored") is False or field.get("writer") == "code_derived":
        return False
    order = STEP_ORDER.get(str(field.get("filled_by_step")), 99)
    if order > step_limit:
        return False
    depth = field["depth"]
    for rule in field.get("depth_when") or []:
        if condition_holds(rule["when"], record, project):
            depth = rule["depth"]
    if depth not in ("q", "s"):
        return False
    if field.get("required_when") and not condition_holds(field["required_when"], record, project):
        return False
    return True


def check_required(project, records, problems):
    for record in records:
        if record.type_name not in TYPES:
            continue
        present = {name for name, _, _ in record.fields}
        for others in project.by_key.get(record.key, []):
            present |= {name for name, _, _ in others.fields}
        if record.type_name == "SETVALUE":
            continue
        own = {field["name"] for field in TYPES[record.type_name]["fields"]}
        fields = list(TYPES[record.type_name]["fields"]) + [field for name, field in COMMON_FIELDS.items() if name not in own]
        for field in fields:
            if record.type_name == "SCENE" and field.get("part_of") in ("design",) and record.file_name.startswith("02"):
                continue
            if record.type_name == "SCENE" and field.get("part_of") in ("list", "plan") and not record.file_name.startswith("02") \
                    and not record.file_name.startswith("04"):
                continue
            if field.get("one_of") and field["one_of"] in present:
                continue
            if required_at_standard(field, record, project) and field["name"] not in present:
                problems.append(f"{record.file_name} {record.label}: Standard field {field['name']} missing")
            if field.get("kind") == "sub_parts" and field["name"] in present:
                for value in record.values(field["name"]):
                    check_required_sub_parts(field, value, record, project, problems)


def check_required_sub_parts(field, value, record, project, problems):
    if value.strip() in ("none", "open"):
        return
    pieces = split_outside_quotes(value, " | ")
    item = {}
    for piece in pieces[1 if field.get("first_part") else 0:]:
        key, _, sub_value = piece.partition(": ")
        item[key] = sub_value
    for part in field.get("sub_parts") or []:
        depth = part.get("depth", field["depth"])
        if depth not in ("q", "s"):
            continue
        if part.get("required_when") and not condition_holds(part["required_when"], record, project, item):
            continue
        if part.get("required_when_not") and condition_holds(part["required_when_not"], record, project, item):
            continue
        if not part.get("depth"):
            continue   # sub-parts without their own depth are described by the field; only depth-marked ones are demanded
        if part["key"] not in item:
            problems.append(f"{record.file_name} {record.label}.{field['name']}: sub-part {part['key']} missing")


# ---------------------------------------------------------------- the story

def read_story(path):
    """Story lines by number, and the header when the file is a Stage excerpt."""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    header = {}
    if lines and lines[0] == "STAGE EXCERPT HEADER":
        end = lines.index("END OF STAGE EXCERPT HEADER")
        for line in lines[1:end]:
            key, _, value = line.partition(": ")
            header[key] = value
        body = lines[end + 1:]
        first = int(header["first_line_number"])
    else:
        body = lines
        first = 1
    numbered = {first + index: line for index, line in enumerate(body)}
    if body and body[-1] == "" and text.endswith("\n"):
        numbered.pop(first + len(body) - 1)
    return numbered, header


class Story:
    def __init__(self, numbered):
        self.lines = numbered
        self.first = min(numbered)
        self.last = max(numbered)
        while self.last > self.first and not self.lines[self.last].strip():
            self.last -= 1

    def line(self, number):
        return self.lines.get(number, "")

    def words(self, number):
        return [token for token in self.line(number).split() if re.search(r"[A-Za-z0-9]", token)]

    def is_cue(self, number):
        return self.line(number).startswith("@")

    def block(self, number):
        start = number
        while start > self.first and self.line(start).strip() and not self.is_cue(start):
            start -= 1
        if not self.line(start).strip() or not self.is_cue(start):
            return None
        end = start
        while end + 1 in self.lines and self.line(end + 1).strip():
            end += 1
        return (start, end) if start <= number <= end else None

    def speech_words(self, cue):
        _, end = self.block(cue)
        return sum(len(self.words(n)) for n in range(cue + 1, end + 1) if not self.line(n).startswith("("))

    def count(self, quote, low, high):
        return sum(self.line(n).count(quote) for n in range(low, high + 1))

    def find(self, quote, low, high):
        hits = [n for n in range(low, high + 1) if quote in self.line(n)]
        if len(hits) != 1 or self.line(hits[0]).count(quote) != 1:
            return None
        return hits[0]

    def resolve_end(self, quote, low, high):
        """The adopt rule: an anchor that ends a stretch runs on through the rest of its speech, then through
        blank lines, lines of fewer than 3 words and cues whose speech has fewer than 3 words."""
        end = self.find(quote, low, high)
        if end is None:
            return None
        block = self.block(end)
        if block:
            end = block[1]
        number = end + 1
        while number <= high:
            if not self.line(number).strip():
                number += 1
                continue
            if self.is_cue(number):
                _, block_end = self.block(number)
                if self.speech_words(number) < 3:
                    end = block_end
                    number = block_end + 1
                    continue
                break
            if len(self.words(number)) < 3:
                end = number
                number += 1
                continue
            break
        return end

    def resolve_range(self, value, low, high, end_low=None, end_high=None):
        """A lines value of quote anchors to (first, last) line numbers, or None."""
        match = re.fullmatch(r'"([^"]+)"(?: to "([^"]+)")?', value.strip())
        if not match:
            return None
        start = self.find(match.group(1), low, high)
        if start is None:
            return None
        block = self.block(start)
        if block and start != block[0]:
            start = block[0]
        if match.group(2):
            end = self.resolve_end(match.group(2), end_low or low, end_high or high)
        else:
            end = self.resolve_end(match.group(1), low, high)
        return None if end is None else (start, end)

    def scene_around(self, number):
        start = number
        while start > self.first and not self.line(start).startswith("## "):
            start -= 1
        end = number + 1
        while end <= self.last and not self.line(end).startswith("## "):
            end += 1
        return start, end - 1


def parse_line_numbers(value):
    result = []
    for piece in value.split(","):
        piece = piece.strip()
        if "-" in piece:
            first, last = piece.split("-")
            result.append((int(first), int(last)))
        elif piece:
            result.append((int(piece), int(piece)))
    return result


def line_set(value):
    return {number for first, last in parse_line_numbers(value) for number in range(first, last + 1)}


# ---------------------------------------------------------------- groups

def check_gold_form(gold_files):
    problems = []
    for record_file in gold_files:
        check_file_form(record_file, problems)
    counts = {record_file.name: len(record_file.records) for record_file in gold_files}
    report(not problems, "gold: record types, IDs, field names, values, sub-parts, END lines and divider",
           f"{counts}" if not problems else shorten(problems))


def check_gold_required(gold_files):
    project = Project(gold_files)
    problems = []
    check_required(project, project.records, problems)
    report(not problems, "gold: every Standard field present for scene 10 and the records it cites (conditions evaluated)",
           f"{len(project.records)} records at depth standard" if not problems else shorten(problems, 10))


def check_gold_content(gold_files):
    """Facts about the gold content that need no story text."""
    scene_file, context_file = gold_files
    problems = []
    types = {record.type_name for record in context_file.records}
    for wanted in ("PROJECT", "CHARACTER", "VOICE", "LOCATION", "PROP", "TEXT", "MOTIF", "STATE", "CAMSYS", "CAMRULE",
                   "RESERVE", "LENS", "LOOK", "VISUAL", "SOUNDPLAN", "RULE"):
        if wanted not in types:
            problems.append(f"the context file has no {wanted}")
    if not any(record.identifier == "WR-MIRROR" for record in context_file.records):
        problems.append("the context file has no WR-MIRROR")
    characters = {record.identifier for record in context_file.records if record.type_name == "CHARACTER"}
    voices = {record.value("character") for record in context_file.records if record.type_name == "VOICE"}
    if characters != {"CH-SAYE", "CH-IONA", "CH-JUDE", "CH-ELI"} or voices != characters:
        problems.append(f"characters {sorted(characters)} and voices {sorted(voices)} are not the four present")
    location = next((record for record in context_file.records if record.type_name == "LOCATION"), None)
    if location is None or not location.values("size") or len(location.values("object")) < 5 or len(location.values("mark")) < 4:
        problems.append("the location has no full set plan (size, objects, marks)")
    shots = [record for record in scene_file.records if record.type_name == "SHOT"]
    shot_list = next(record for record in scene_file.records if record.type_name == "SHOTLIST")
    items = [split_outside_quotes(value, " | ") for value in shot_list.values("item")]
    if [item[0] for item in items] != [shot.identifier for shot in shots]:
        problems.append("the shot list and the shots differ (ID-07)")
    for item in items:
        shot = next(shot for shot in shots if shot.identifier == item[0])
        parts = dict(piece.split(": ", 1) for piece in item[1:])
        for key in ("beats", "role", "size"):
            if parts.get(key) != shot.value(key):
                problems.append(f"{item[0]} list {key} {parts.get(key)!r} differs from the shot's {shot.value(key)!r} (ID-08)")
        if float(parts["time"]) != float(shot.value("screen_time")):
            problems.append(f"{item[0]} list time differs from screen_time")
    for shot in shots:
        number = int(shot.identifier[-3:])
        if shot.value("kind") in ("card", "black") and number < 990:
            problems.append(f"{shot.identifier}: a card below 990 (ID-03)")
        if shot.value("kind") not in ("card", "black") and number % 10:
            problems.append(f"{shot.identifier}: not in tens (ID-03)")
    sizes = ["extreme_wide", "wide", "medium_wide", "medium", "medium_close_up", "close_up", "extreme_close_up"]
    beats = {record.identifier: record for record in scene_file.records if record.type_name == "BEAT"}
    main_turns = [beat for beat, record in beats.items() if record.value("turn") == "main_turn"]
    live = [shot for shot in shots if shot.value("kind") not in ("insert", "card", "black")]
    tightest = max(sizes.index(shot.value("size")) for shot in live)
    for shot in live:
        if sizes.index(shot.value("size")) == tightest and not any(turn in shot.value("beats") for turn in main_turns):
            problems.append(f"{shot.identifier}: the tightest size outside the main turn (CRAFT-03)")
    for shot in shots:
        if shot.value("role") == "turn" and not shot.value("why"):
            problems.append(f"{shot.identifier}: a turn shot without why (REASON-02)")
        moments = []
        for value in shot.values("moment"):
            span = split_outside_quotes(value, " | ")[0]
            first, last = (float(piece) for piece in span.split("-"))
            moments.append((first, last))
        screen_time = float(shot.value("screen_time"))
        previous = 0.0
        for first, last in moments:
            if first < previous or last > screen_time:
                problems.append(f"{shot.identifier}: moment {first}-{last} overlaps or runs past {screen_time} (TIME-02)")
            previous = last
        if len(moments) > math.ceil(screen_time / 4):
            problems.append(f"{shot.identifier}: {len(moments)} moments in {screen_time} s (TIME-06)")
    total = sum(float(shot.value("screen_time")) for shot in shots)
    report(not problems, "gold: the content list (records present, shot list agreement, numbering, one close-up for the turn, moments)",
           f"{len(shots)} shots, {total:g} seconds" if not problems else shorten(problems))


def check_templates():
    problems = []
    notes = []
    for name in TEMPLATE_NAMES + EXTRA_TEMPLATE_NAMES:
        path = TEMPLATES / name
        if not path.is_file():
            problems.append(f"{name} missing")
            continue
        record_file = RecordFile(path, name)
        if record_file.divider_count != 1:
            problems.append(f"{name}: divider appears {record_file.divider_count} times")
        for line in record_file.plain:
            if line.startswith("#") and not (line.startswith("# ") or line.startswith("## ")):
                problems.append(f"{name}: plain part heading {line[:30]!r}")
        if not any(line.startswith("# ") for line in record_file.plain):
            problems.append(f"{name}: no # heading in the plain part")
        types = [record.type_name for record in record_file.records]
        if types != TEMPLATE_TYPES[name]:
            problems.append(f"{name}: record types {types}, expected {TEMPLATE_TYPES[name]}")
        if len(record_file.end_lines) != 1 or record_file.end_lines[0][1] != len(record_file.records):
            problems.append(f"{name}: END line missing or its count is wrong")
        for record in record_file.records:
            definition = TYPES.get(record.type_name)
            if definition is None:
                continue
            wanted = [field["name"] for field in definition["fields"] if field.get("stored") is not False
                      and field.get("writer") != "code_derived"
                      and (record.type_name != "SCENE" or field.get("part_of") in SCENE_PARTS[name])]
            own = {field["name"] for field in definition["fields"]}
            common = [field for field in COMMON_FIELDS if field not in own]
            if record.type_name == "SCENE" and name == "11 Scene.md":
                common = ["note"]   # the scene's status and locked live on its copy in 04 Scene list.md
            wanted += common
            written = [field_name for field_name, _, _ in record.fields]
            if written != wanted:
                missing = [field for field in wanted if field not in written]
                extra = [field for field in written if field not in wanted]
                problems.append(f"{name} {record.type_name}: fields not in schema order or incomplete"
                                f" (missing {missing[:4]}, extra {extra[:4]})")
            if not record.notes:
                problems.append(f"{name} {record.type_name}: no note block")
            for field_name, value, number in record.fields:
                if not re.search(r"<(quick|standard|detailed|optional|add-on)", value):
                    problems.append(f"{name}:{number} {field_name}: no depth word in its placeholder")
        words = len(record_file.text.split())
        notes.append(f"{name} {words}")
        if not 300 <= words <= 1500:
            info(f"template {name}: {words} words, outside the 300-1,500 target")
    report(not problems, f"templates: {len(TEMPLATE_NAMES)} of blueprint 2.2 plus {len(EXTRA_TEMPLATE_NAMES)} more; plain part, divider, "
           "every stored field in schema order with its depth, note blocks, END lines",
           ", ".join(notes) + " words" if not problems else shorten(problems))


def load_chat_copy():
    if not CHAT_COPY.is_dir():
        return None
    paths = sorted(CHAT_COPY.rglob("*.md"))
    return [RecordFile(path, str(path.relative_to(CHAT_COPY))) for path in paths]


def check_chat_form(chat_files):
    problems = []
    for record_file in chat_files:
        check_file_form(record_file, problems)
    names = [record_file.name for record_file in chat_files]
    batches = [name for name in names if re.search(r" - shots \d{3}-\d{3}\.md$", name)]
    if len(batches) != 2:
        problems.append(f"{len(batches)} batch files, expected 2")
    project_record = next((record for record_file in chat_files for record in record_file.records
                           if record.type_name == "PROJECT"), None)
    if project_record is None or project_record.value("code_execution") != "no":
        problems.append("the project does not say code_execution: no")
    for record_file in chat_files:
        if "---" not in record_file.lines:
            problems.append(f"{record_file.name}: no checks-in-words table after a --- line")
        for record in record_file.records:
            for name, value, number in record.fields:
                field = field_definition(record.type_name, name) or {}
                if field.get("kind") == "lines" and re.fullmatch(r"[\d ,\-]+", value.strip()):
                    problems.append(f"{record_file.name}:{number} {name} holds line numbers, not quote anchors")
                if re.search(r"\bline:\s*\d", value):
                    problems.append(f"{record_file.name}:{number} {name} holds a line number, not a quote anchor")
                if re.search(r'SC\d{2,3} "[^"]+" = ', value):
                    problems.append(f"{record_file.name}:{number} {name}: a story point with a code-resolved ending")
                if record.type_name == "SHOT" and name == "hear" and value != "none" and "| words: " not in value:
                    problems.append(f"{record_file.name}:{number} a hear item without its words")
    project = Project(chat_files)
    required = []
    check_required(project, project.records, required)
    problems.extend(required)
    counts = {record_file.name: len(record_file.records) for record_file in chat_files}
    report(not problems, "chat-saved copy: form, required fields, quote anchors, hear words, two batch files, code_execution: no",
           f"{sum(counts.values())} records in {len(counts)} files" if not problems else shorten(problems))


def gold_speeches(story):
    speeches = {}
    count = 0
    for number in range(SCENE_FIRST_LINE, SCENE_LAST_LINE + 1):
        if story.is_cue(number):
            count += 1
            _, end = story.block(number)
            text = " ".join(story.line(n) for n in range(number + 1, end + 1) if not story.line(n).startswith("("))
            words_line = next(n for n in range(number + 1, end + 1) if not story.line(n).startswith("("))
            speeches[f"SC10-D{count:02d}"] = {"cue": number, "line": words_line, "text": text,
                                              "speaker": "CH-" + story.line(number)[1:].strip()}
    return speeches


def check_with_story(gold_files, chat_files, story, header, whole_story):
    scene_file, context_file = gold_files
    # the excerpt header
    if header:
        problems = []
        if header.get("first_line_number") != str(SCENE_FIRST_LINE) or header.get("last_line_number") != str(SCENE_LAST_LINE):
            problems.append(f"header lines {header.get('first_line_number')}-{header.get('last_line_number')}")
        if header.get("first_scene_number") != "10":
            problems.append("header first_scene_number is not 10")
        if not story.line(SCENE_FIRST_LINE).startswith("## INT. SAYE'S HOUSE - KITCHEN"):
            problems.append(f"line {SCENE_FIRST_LINE} is not scene 10's heading")
        if max(story.lines) != SCENE_LAST_LINE:
            problems.append(f"the excerpt ends at line {max(story.lines)}")
        report(not problems, "excerpt fixture: header and line numbering (decision 16)",
               f"lines {SCENE_FIRST_LINE}-{SCENE_LAST_LINE} of {header.get('whole_story_lines')}" if not problems else shorten(problems))
    # quotes in the scene file
    problems = []
    for number, line in enumerate(scene_file.lines, start=1):
        if line == DIVIDER or line.startswith("END OF FILE"):
            continue
        for match in QUOTED.finditer(line):
            quote = match.group(1)
            before = line[:match.start()]
            point = re.search(r"\bSC(\d{2,3})\s+$", before)
            if point and point.group(1) != "10":
                continue
            if story.count(quote, SCENE_FIRST_LINE, SCENE_LAST_LINE) == 0:
                problems.append(f"{scene_file.name}:{number} \"{quote}\" is not in scene 10 (CITE-03)")
    report(not problems, "gold: every double-quoted string of the scene file is exact story words from scene 10 (G12)",
           "all found" if not problems else shorten(problems))
    # story points of scene 10 in both files
    problems = []
    points = 0
    for record_file in gold_files:
        for number, line in enumerate(record_file.lines, start=1):
            for match in re.finditer(r'\bSC10 "([^"]+)"(?: = (SC10-B\d{2}))?', line):
                points += 1
                quote = match.group(1)
                found = story.find(quote, SCENE_FIRST_LINE, SCENE_LAST_LINE)
                if found is None:
                    problems.append(f"{record_file.name}:{number} story point \"{quote}\" not found once in scene 10 (CITE-02)")
                    continue
                if len(story.words_in(quote) if hasattr(story, "words_in") else [t for t in quote.split() if re.search(r"[A-Za-z0-9]", t)]) < 3:
                    problems.append(f"{record_file.name}:{number} story point \"{quote}\" has fewer than 3 words")
                if match.group(2):
                    beat = next((record for record in scene_file.records if record.identifier == match.group(2)), None)
                    if beat is None or found not in line_set(beat.value("lines")):
                        problems.append(f"{record_file.name}:{number} \"{quote}\" resolves to {match.group(2)}, whose lines do not hold it")
    report(not problems, "gold: scene 10's story points are found once, hold 3 or more words and resolve to the right beat",
           f"{points} story points" if not problems else shorten(problems))
    # coverage, speeches and time floors
    speeches = gold_speeches(story)
    beats = [record for record in scene_file.records if record.type_name == "BEAT"]
    shots = [record for record in scene_file.records if record.type_name == "SHOT"]
    content = {n for n in range(SCENE_FIRST_LINE + 1, SCENE_LAST_LINE + 1) if story.line(n).strip()}
    problems = []
    in_beats = set().union(*(line_set(beat.value("lines")) for beat in beats))
    in_shots = set().union(*(line_set(shot.value("lines")) for shot in shots))
    if content - in_beats:
        problems.append(f"lines in no beat: {sorted(content - in_beats)} (COVER-01)")
    if content - in_shots:
        problems.append(f"lines in no shot: {sorted(content - in_shots)} (COVER-02)")
    heard = {}
    for shot in shots:
        for value in shot.values("hear"):
            speech = split_outside_quotes(value, " | ")[0]
            if speech == "none":
                continue
            heard.setdefault(speech, []).append(shot.identifier)
            if speech not in speeches:
                problems.append(f"{shot.identifier} hears {speech}, which is not a speech of scene 10")
            elif speeches[speech]["cue"] not in line_set(shot.value("lines")):
                problems.append(f"{shot.identifier} hears {speech}, whose cue is outside its lines (CITE-05)")
    for speech in speeches:
        if speech not in heard:
            problems.append(f"{speech} is heard in no shot (COVER-03)")
    for beat in beats:
        if not any(beat.identifier in (shot.value("beats") or "") for shot in shots):
            problems.append(f"{beat.identifier} has no shot (COVER-04)")
    report(not problems, "gold: every story line in a beat and a shot, every speech heard, every beat shot",
           f"{len(content)} story lines, {len(speeches)} speeches, {len(beats)} beats" if not problems else shorten(problems))
    constants = json.loads(CONSTANTS_FILE.read_text(encoding="utf-8"))["constants"]
    extra = constants["speech_floor_extra_s"]["value"]
    text_rule = constants["text_floor"]["value"]
    turn_minimum = constants.get("turn_reaction_min_s", {}).get("value", 2.0)
    paces = {record.value("character"): float(record.value("pace_wps")) for record in context_file.records
             if record.type_name == "VOICE"}
    texts = {record.identifier: record for record in context_file.records if record.type_name == "TEXT"}
    problems = []
    floors = {}
    for shot in shots:
        lines_here = line_set(shot.value("lines"))
        speech_floor = 0.0
        for value in shot.values("hear"):
            speech = split_outside_quotes(value, " | ")[0]
            if speech in speeches:
                speech_floor += len(speeches[speech]["text"].split()) / paces[speeches[speech]["speaker"]] + extra
        text_floor = 0.0
        for text_identifier in [item.strip() for item in (shot.value("text") or "none").split(",") if item.strip() != "none"]:
            words = texts[text_identifier].value("words")
            reading = max(text_rule["minimum_s"], text_rule["base_s"] + len(words) / text_rule["characters_per_second"])
            emphasis = int(texts[text_identifier].value("emphasis") or 0)
            if emphasis >= text_rule["plot_critical_emphasis_min"]:
                reading = max(reading, text_rule["plot_critical_base_s"] + text_rule["plot_critical_per_word_s"] * len(words.split()))
            text_floor += reading
        owed = 0.0
        for beat in beats:
            last = max(n for n in line_set(beat.value("lines")) if story.line(n).strip())
            if last in lines_here:
                pause = split_outside_quotes(beat.value("pause_after") or "none", " | ")
                seconds = 0.0
                if pause[0] != "none":
                    seconds = float(dict(piece.split(": ", 1) for piece in pause[1:]).get("seconds", 0))
                if (beat.value("turn") or "none") != "none":
                    seconds = max(seconds, turn_minimum)
                owed += seconds
        floor = round(max(speech_floor, text_floor) + owed, 2)
        floors[shot.identifier] = floor
        if float(shot.value("screen_time")) < floor:
            problems.append(f"{shot.identifier} screen_time {shot.value('screen_time')} is under its floor {floor} (TIME-01)")
    if floors.get("SC10-SH150") != 13.8:
        problems.append(f"shot 150's floor is {floors.get('SC10-SH150')}, not 13.8")
    report(not problems, "gold: every shot's screen time reaches its floor (5.6); shot 150's floor is 13.8 seconds",
           f"shot 150: floor {floors.get('SC10-SH150')}, screen time 15" if not problems else shorten(problems))
    # the chat copy's anchors against the gold
    if chat_files is None:
        info("skipped: the chat-saved copy is not present")
        return
    gold_by_key = {record.key: record for record in scene_file.records}
    problems = []
    checked = 0
    for record_file in chat_files:
        if not record_file.name.startswith("11 Scenes"):
            continue
        for record in record_file.records:
            gold = gold_by_key.get(record.key)
            if gold is None:
                problems.append(f"{record.label} is not in the gold")
                continue
            for name, value, number in record.fields:
                field = field_definition(record.type_name, name) or {}
                if field.get("kind") == "lines":
                    resolved = story.resolve_range(value, SCENE_FIRST_LINE, SCENE_LAST_LINE)
                    wanted = parse_line_numbers(gold.value(name))[0]
                    checked += 1
                    if resolved != wanted:
                        problems.append(f"{record.label}.{name} {value[:50]} resolves to {resolved}, the gold says {wanted}")
                if name == "because":
                    anchors = re.findall(r'line: "([^"]+)"', value)
                    numbers = [int(item) for item in re.findall(r"line:(\d+)", gold.value("because"))]
                    lines = [story.find(anchor, SCENE_FIRST_LINE, SCENE_LAST_LINE) for anchor in anchors]
                    checked += len(anchors)
                    if lines != numbers:
                        problems.append(f"{record.label}.because anchors resolve to {lines}, the gold says {numbers}")
                if name == "hear" and value != "none":
                    speech = split_outside_quotes(value, " | ")[0]
                    words = re.search(r'\| words: "([^"]*)"', value)
                    checked += 1
                    if not words or speech not in speeches or words.group(1) != speeches[speech]["text"]:
                        problems.append(f"{record.label} hear {speech}: words differ from the speech (CITE-04)")
            if record.type_name == "SHOT" and [(n, v) for n, v, _ in record.fields if n not in ("lines", "because", "hear")] != \
                    [(n, v) for n, v, _ in gold.fields if n not in ("lines", "because", "hear")]:
                problems.append(f"{record.label}: fields other than lines, because and hear differ from the gold")
    report(not problems, "chat-saved copy: every scene quote anchor resolves by the adopt rule to the gold's line numbers",
           f"{checked} anchors and hear items" if not problems else shorten(problems))
    if not whole_story:
        info("skipped: the whole-film records' quotes and anchors need the whole story (--story); the excerpt holds scene 10 only")
        return
    problems = []
    checked = 0
    for number, line in enumerate(context_file.lines, start=1):
        if line == DIVIDER or line.startswith("END OF FILE") or line.startswith("- source_file:"):
            continue
        for match in QUOTED.finditer(line):
            quote = match.group(1)
            checked += 1
            if story.count(quote, story.first, story.last) == 0:
                problems.append(f"{context_file.name}:{number} \"{quote}\" is not in the story (CITE-03)")
            point = re.search(r"\bSC(\d{2,3})\s+$", line[:match.start()])
            if point:
                scenes = [n for n in sorted(story.lines) if story.line(n).startswith("## ")]
                index = int(point.group(1)) - 1
                if index < len(scenes):
                    low = scenes[index]
                    high = scenes[index + 1] - 1 if index + 1 < len(scenes) else story.last
                    if story.find(quote, low, high) is None:
                        problems.append(f"{context_file.name}:{number} story point SC{point.group(1)} \"{quote}\" not found once in that scene")
    context_by_key = {record.key: record for record in context_file.records}
    for record_file in chat_files:
        if record_file.name.startswith("11 Scenes"):
            continue
        for record in record_file.records:
            gold = context_by_key.get(record.key)
            if gold is None:
                continue
            for (name, value, _), (gold_name, gold_value, _) in zip(record.fields, gold.fields):
                if name != gold_name:
                    problems.append(f"{record.label}: field order differs from the gold at {name}")
                    break
                field = field_definition(record.type_name, name) or field_definition("RULE", name) or {}
                if field.get("kind") == "lines":
                    wanted = parse_line_numbers(gold_value)[0]
                    end_scope = story.scene_around(wanted[0]) if record.type_name == "SCENE" else (story.first, story.last)
                    resolved = story.resolve_range(value, story.first, story.last, *end_scope)
                    checked += 1
                    if resolved != wanted:
                        info(f"chat {record.label}.{name} resolves to {resolved}, the gold says {wanted}"
                             + (" (adopt re-owns this field and logs the difference)" if record.type_name == "SCENE" else ""))
                        if record.type_name != "SCENE":
                            problems.append(f"{record.label}.{name} resolves to {resolved}, the gold says {wanted}")
                elif field.get("kind") == "sub_parts":
                    chat_pieces = split_outside_quotes(value, " | ")
                    gold_pieces = split_outside_quotes(gold_value, " | ")
                    for chat_piece, gold_piece in zip(chat_pieces, gold_pieces):
                        gold_number = gold_piece.split(": ")[-1].strip()
                        anchor = re.fullmatch(r'(?:\w+: )?"([^"]+)"', chat_piece.strip())
                        if re.fullmatch(r"\d+", gold_number) and anchor:
                            checked += 1
                            wanted = int(gold_number)
                            if gold_piece.startswith("to: "):
                                resolved = story.resolve_end(anchor.group(1), story.first, story.last)
                            else:
                                resolved = story.find(anchor.group(1), story.first, story.last)
                            if resolved != wanted:
                                problems.append(f"{record.label}.{name} {chat_piece[:40]} resolves to {resolved}, the gold says {wanted}")
    report(not problems, "whole story: the context file's quotes are story words, and the chat copy's whole-film anchors resolve to the gold",
           f"{checked} quotes and anchors" if not problems else shorten(problems))


def main():
    parser = argparse.ArgumentParser(description="Work package 12a conformance test.")
    parser.add_argument("--story", help="the whole story, or a Stage excerpt that holds scene 10 (default: the excerpt fixture)")
    arguments = parser.parse_args()
    if not GOLD.is_file() or not GOLD_CONTEXT.is_file():
        report(False, "gold example present", "references/examples/01 or 02 is missing")
        print("RESULT: FAIL")
        return 1
    gold_files = [RecordFile(GOLD, GOLD.name), RecordFile(GOLD_CONTEXT, GOLD_CONTEXT.name)]
    check_gold_form(gold_files)
    check_gold_required(gold_files)
    check_gold_content(gold_files)
    check_templates()
    chat_files = load_chat_copy()
    if chat_files is None:
        info("skipped: the chat-saved copy is not present")
    else:
        check_chat_form(chat_files)
    story_path = Path(arguments.story) if arguments.story else EXCERPT
    if not story_path.is_file():
        info("skipped: story not present")
    else:
        numbered, header = read_story(story_path)
        story = Story(numbered)
        whole_story = min(numbered) == 1
        if not all(n in numbered for n in range(SCENE_FIRST_LINE, SCENE_LAST_LINE + 1)):
            info("skipped: story not present (the file given does not hold lines 397-489)")
        else:
            check_with_story(gold_files, chat_files, story, header, whole_story)
    failed = [group for passed, group in RESULTS if not passed]
    print(f"RESULT: {'PASS' if not failed else 'FAIL'} ({len(failed)} failing groups)")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
