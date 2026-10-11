"""Acceptance test for work package 1 (schema and rules).

Checks that every JSON file of the skill's _config/schema/ and _config/rules/ folders loads; that every record type
and field of blueprint section 5.5 is in _config/schema/schema.json with a depth, exactly one writer (or a
writer_when list) and a filled_by_step; that the depth and writer of every field agree with the d and
w columns of 5.5 (documented deviations listed below with their reasons); that the filled_by_step
values and chat writers the blueprint names hold; that every example ID of 5.3 matches its record
type's pattern and malformed IDs do not; that the turn shot of 5.1 is valid under the schema; that
every retired word of section 5.7 is in _config/rules/words.json; that every constant the blueprint names is
in _config/rules/constants.json with the value of 5.8; that _config/schema/steps.json names only known checks, record
types, card parts and files; that limits.json and tone_defaults.json hold their blueprint rows; and
that every field's example is valid under its own definition.

Run from anywhere:
    python tests/wp1_schema_acceptance.py [--blueprint <path to blueprint.md>] [--self-test]

The blueprint is not part of the repository. When it is given (or found through the environment
variable STAGE_BLUEPRINT) the lists are read from it; otherwise the test uses the snapshot of those
lists stored at the end of this file, taken from the blueprint of 27 Sep 2026. --self-test breaks
copies of the files in memory, one fault at a time, and checks that each fault makes its check fail.
Standard library only.
"""

import argparse
import copy
import json
import os
import re
import sys

REPOSITORY_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_FOLDER = os.path.join(REPOSITORY_FOLDER, ".claude", "skills", "breaking-down-stories")
JSON_FILES = ["_config/schema/schema.json", "_config/schema/steps.json", "_config/rules/constants.json",
              "_config/rules/words.json", "_config/rules/limits.json", "_config/rules/tone_defaults.json"]
DEPTHS = {"q", "s", "f", "m", "o"}
WRITERS = {"story", "ai", "user", "code_state", "code_derived"}
WRITER_PATTERN = r"story|ai|user|code_state|code_derived|code"
COMMON_FIELD_NAMES = ["status", "locked", "note"]
ID_KINDS = ("id", "id_list", "id_range", "reference_list", "because_list")

# Names in backticks that the blueprint uses but that are not constants, each with its reason.
NOT_CONSTANTS = {
    "chat_writer": "a schema key (5.2)",
    "defines_id": "a schema key (5.3)",
    "filled_by_step": "a schema key (5.2)",
    "writer_when": "a schema key (5.2)",
    "depth_range_m": "a key of the previs plan file (section 9)",
    "facing_deg": "a key of the previs plan file (section 9)",
    "plan_view": "a key of the previs plan file (section 9)",
    "licensed_data": "a flag in the adapter files (8.4)",
    "audio_max": "a key in the adapter files (8.2)",
    "negative_default": "a key in the adapter files (8.2)",
    "price_usd_per_s": "a key in the adapter files (8.2)",
    "references_max": "a key in the adapter files (8.2)",
    "videos_max": "a key in the adapter files (8.2)",
    "references_max_with_video": "a key in the adapter files (8.2)",
    "from_end_of": "the prefix form of SHOT.start (5.5)",
    "pause_owed": "a term of the derived time floor formula (5.6)",
    "speech_floor": "a term of the derived time floor formula (5.6)",
    "remove_empty_rows": "the blueprint's example of a plain function name (7.1)",
}
CONSTANT_LIKE = re.compile(
    r"\b[a-z][a-z0-9]*(?:_[a-z0-9]+)*_(?:max|min|default|rule|rules|tolerance|thresholds|tiers|by_size|by_intensity|"
    r"per_[a-z_]+|age_days|extra_s|range_s|asl_s|lead_s|needs_still_s|face_height|words)\b")

# Where schema.json knowingly differs from the d or w column of 5.5, with the reason (build log WP1, "Deviations").
KNOWN_DEVIATIONS = {
    "PROP.names": "writer ai: code cannot know which things the story names before step 4's harvest (WP1 deviation 1)",
}
# Fields whose writer_when is allowed although the w column names one writer (5.2 conditional writers and the WP1 log).
CONDITIONAL_WRITERS_ALLOWED = {
    "CHARACTER.names": "story for a character with a cue, ai otherwise (WP1 deviation 2)",
    "LOCATION.headings": "story for screenplays, ai otherwise, as SCENE heading (WP1 deviation 3)",
    "SHOT.dominant": "ai at detailed; code derives it below (5.5 d column; WP1 deviation 4)",
    "TEXT.words": "story when the words are in the script, ai with origin invented otherwise (5.2)",
    "PIC.approved": "the AI approves storyboard frames, the user every other picture (5.5 w column note)",
    "PREVIS.for": "code_state for stubs, ai otherwise (5.5 w column note)",
    "PREVIS.level": "code_state for stubs, ai otherwise (5.5 w column note)",
    "PREVIS.approved": "the user for framing-critical shots, code (auto) for the rest (add-on B done test; review note)",
}
# Depth cells the parser cannot read field by field.
DEPTH_OVERRIDES = {("LOOK", "style_picture"): "m"}

# filled_by_step values the blueprint names (5.2, the 5.5 introduction and the outputs of section 3).
EXPECTED_FILLED_BY_STEP = {
    "PROJECT.format": 1, "PROJECT.frame_shape": "B", "PROJECT.runtime_target_s": "A", "PROJECT.fps": 6,
    "PROJECT.genre": 2, "PROJECT.scope": "P", "PROJECT.rights": 0, "PROJECT.depth": 0, "PROJECT.training_off": 0,
    "PROJECT.surface": 0, "PROJECT.code_execution": 0, "PROJECT.batch_size": 0, "PROJECT.title": 1,
    "SCENE.heading": 1, "SCENE.lines": 1, "SCENE.characters": 1, "SCENE.speaking": 1, "SCENE.event": 2,
    "SCENE.sequence": 2, "SCENE.scene_intensity": 2, "SCENE.whose_scene": 2, "SCENE.story_day": 2,
    "SCENE.rhythm_class": 2, "SCENE.tone": 2, "SCENE.tone_undercurrent": 2, "SCENE.tags": 2,
    "SCENE.target_duration_s": 2, "SCENE.turn_picture": 7, "SCENE.dial": 7, "SHOTLIST.item": 7, "SHOTLIST.approved": "C",
    "CHAPTER.title": 1, "CHAPTER.first_line": 1, "CHAPTER.last_line": 1, "CHAPTER.digest": 2,
    "CHARACTER.names": 1, "CHARACTER.fixed_description": 4, "CHARACTER.likeness_basis": 4,
    "STYLE.medium": "B", "WORLD.place": "B", "WORLD.period": "B", "RULE.era": "B", "VOICE.source": 4,
    "SOUNDPLAN.music_policy": "B", "SOUNDPLAN.voice_policy": 6, "STATE.state_line": 5,
    "SHOT.screen_time": 8, "SHOT.purpose": 8, "CUT.type": 8, "FINDING.record": 9, "REVIEW.score": 10,
}
# chat_writer: ai named by 5.2 (a field whose writer is already ai also satisfies it).
EXPECTED_CHAT_WRITERS = ["common.status", "common.locked", "PROJECT.surface", "PROJECT.code_execution", "PROJECT.batch_size",
                         "SCENE.characters", "SCENE.heading", "SCENE.lines", "CHAPTER.first_line", "CHAPTER.last_line"]
# The record type each example ID of 5.3 belongs to.
ID_EXAMPLE_TYPES = {
    "CATCH": "PROJECT", "LONG": "PROJECT", "SC10": "SCENE", "SC06A": "SCENE", "SC104": "SCENE", "SC10-P2": "PART",
    "SC10-V1": "VALUE", "SC10-B07": "BEAT", "SC10-D11": "SPEECH", "SC10-M04": "MOVE", "SC10-SU02": "SETUP",
    "SC10-LIST": "SHOTLIST", "SC10-SH150": "SHOT", "SC10-SH150.1": "CLIP", "SC10-C200": "CUT", "SQ03": "SEQUENCE",
    "CP01": "CHAPTER", "ST-01": "STRAND", "CF-05": "CARDINAL", "PL-07": "PLANT", "FT-03": "FACT", "CH-IONA": "CHARACTER",
    "LOC-SAYE-KITCHEN": "LOCATION", "WR-MIRROR": "RULE", "CR-ELI": "CAMRULE", "VS-SQ03": "VISUAL", "RC-01": "RESERVE",
    "LX-01": "LENS", "CH-IONA.S02": "STATE", "PR-FLASK.S02": "STATE", "CHOICE-021": "CHOICE", "FIND-004": "FINDING",
    "RV-SC10": "REVIEW", "CHOICE-014-A": "SETVALUE", "PIC-SC10-SH150-START-01": "PIC", "PV-SC10-SH080-V01": "PREVIS",
    "TK-SC10-SH150.1-T03": "TAKE", "VT-SC10-D11-T01": "VOICETAKE", "FX-SC10-SH080-01": "FINISH",
    "PV-SC06-MASTER-V01": "PREVIS", "RT-001": "RIGHTS", "MU-01": "MUSIC", "U-08-SC10-B2": "UNIT",
}
# Malformed IDs (5.3, and references/formats/01 mistake 8) that must match no pattern of the named type.
BAD_IDS = {"SC10-SH15": "SHOT", "SC10-B7": "BEAT", "SC1": "SCENE", "SC10-P12": "PART", "CHOICE-21": "CHOICE",
           "RC-1": "RESERVE", "CH-iona": "CHARACTER", "CH-IONA.S2": "STATE", "SQ3": "SEQUENCE", "VS-03": "VISUAL",
           "SC10-SH1500": "SHOT", "RV-10": "REVIEW"}
# The values of the 5.8 table (read by hand from the blueprint of 27 Sep 2026); the test also checks that each
# scalar still appears in its blueprint row when the blueprint is given.
EXPECTED_CONSTANT_VALUES = {
    "speech_wps_default": 2.5, "speech_floor_extra_s": 0.5, "long_pauses_per_scene_max": 2, "turn_reaction_min_s": 2.0,
    "handles_s": 0.75, "scene_total_tolerance": 0.1, "acting_characters_per_clip_max": 3, "push_in_per_scene_max": 1,
    "extreme_close_up_per_scene_max": 1, "push_in_scene_share_max": 0.25, "departments_changing_at_main_turn_max": 2,
    "display_3_needs_why_at_or_tighter": "close_up", "hold_action_every_s": 2.0, "head_height_m": 0.23,
    "sound_motif_max": 1, "body_motif_max": 1, "look_block_words_max": 60, "repair_rounds_max": 3,
    "plate_route_face_height": 0.1, "lip_sync_tight_face_height": 0.15, "model_facts_max_age_days": 30,
    "takes_stop_per_route": 4, "takes_stop_per_shot": 10, "cheap_test_above_usd_per_take": 2, "caption_lead_s": 0.25,
    "caption_min_s": 1.0, "caption_max_s": 7.0,
    "extreme_close_up_film_max": {"short": 3, "feature": 6}, "loud_sets_max": {"short": 2, "feature": 3},
    "motif_spines_max": {"short": [3, 5], "feature": [5, 8]}, "batch_size": {"default": 12, "after_selftest": 18},
    "fixed_description_words": {"principal": [25, 40], "minor": [20, 30]},
    "face_height_by_size": {"extreme_close_up": 0.6, "close_up": 0.4, "medium_close_up": 0.25, "medium": 0.15,
                            "medium_wide": 0.1, "wide": 0.05, "extreme_wide": 0.02},
    "rhythm_class_asl_s": {"action_peak": 2.0, "suspense": 3.5, "mixed": 4.0, "dialogue": 4.5, "contemplative": 6.0},
    "v0_action_seconds_per_word": [0.166, 0.22],
    "plant_emphasis_max": {"plant": 1, "plot_event_plant": 2},
    "added_emphasis_per_beat_max": {"max": 1, "where_script_marks_the_beat": 0},
    "device_budget_short": {"cut_to_black": 2, "true_silence": 2, "freeze": 2},
    "main_actions_per_seconds": {"actions": 1, "per_s": 4},
    "non_dialogue_seconds_by_intensity": {"1": [5, 8], "2": [3.5, 6], "3": [2.5, 4], "4": [1, 3], "5": "under 1, or 6 and over"},
}
# Each scalar or pair of pause_tiers, text_floor and the size ladder, as (path in the value, expected).
EXPECTED_CONSTANT_PARTS = [
    ("pause_tiers", ("short", "to_s"), 1.0), ("pause_tiers", ("medium", "from_s"), 1.0), ("pause_tiers", ("medium", "to_s"), 2.5),
    ("pause_tiers", ("long", "from_s"), 2.5), ("pause_tiers", ("long", "to_s"), 4.0), ("pause_tiers", ("long", "includes_end"), True),
    ("pause_tiers", ("short", "includes_end"), False), ("pause_tiers", ("hold", "above_s"), 4.0),
    ("pause_tiers", ("script_words", "(beat)"), 1.0),
    ("text_floor", ("minimum_s",), 2.0), ("text_floor", ("base_s",), 1.0), ("text_floor", ("characters_per_second",), 13),
    ("text_floor", ("plot_critical_base_s",), 2.0), ("text_floor", ("plot_critical_per_word_s",), 0.5),
    ("text_floor", ("mirrored_factor",), 2), ("text_floor", ("plot_critical_emphasis_min",), 2),
    ("clip_speech_rule", ("margin_s",), 1.0), ("signals_changing_per_beat_max", ("max",), 2),
    ("emphasis_3_rules", ("per_motif_in_film_max",), 1), ("emphasis_3_rules", ("per_scene_max",), 2),
    ("size_ladder_thresholds", ("extreme_wide", "at_least"), 2.0), ("size_ladder_thresholds", ("wide",), [1.1, 2.0]),
    ("size_ladder_thresholds", ("medium_wide",), [0.75, 1.1]), ("size_ladder_thresholds", ("medium",), [0.45, 0.75]),
    ("size_ladder_thresholds", ("medium_close_up",), [0.3, 0.45]), ("size_ladder_thresholds", ("close_up",), [0.15, 0.3]),
    ("size_ladder_thresholds", ("extreme_close_up", "under"), 0.15), ("film_asl_range_s", ("grave",), [3, 7]),
    ("film_asl_range_s", ("tense",), [3, 7]),
]


def split_table_row(line):
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [cell.strip() for cell in cells]


def split_outside_parentheses(text):
    """Split on ', ' and '; ' but not inside parentheses."""
    items, current, depth = [], "", 0
    index = 0
    while index < len(text):
        character = text[index]
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        if depth == 0 and text[index:index + 2] in (", ", "; "):
            items.append(current.strip())
            current = ""
            index += 2
            continue
        current += character
        index += 1
    if current.strip():
        items.append(current.strip())
    return items


def read_blueprint_lists(text):
    """Read from the blueprint everything the test compares: 5.5's rows, 5.1's example, 5.3's IDs, 5.7, 5.8 and 7.2."""
    start = text.index("### 5.5 Record types and fields")
    end = text.index("### 5.6 ")
    section = text[start:end]
    heading_types = {"Continuity": "STATE"}
    record_fields = {}
    field_rows = []
    heading_type = None
    header = None
    for line in section.splitlines():
        if line.startswith("#### "):
            heading = line[5:].strip()
            match = re.match(r"([A-Z]{2,})\b", heading)
            heading_type = match.group(1) if match else None
            for word, type_name in heading_types.items():
                if heading.startswith(word):
                    heading_type = type_name
            header = None
            continue
        if not line.startswith("| "):
            continue
        cells = split_table_row(line)
        if header is None:
            header = cells
            continue
        if set(cells[0]) <= set("-: "):
            continue
        if header[0] == "type":
            type_name, field_cell = cells[0], cells[1]
        elif header[0] == "group":
            type_name, field_cell = heading_type, cells[1]
        else:
            type_name, field_cell = heading_type, cells[0]
        names = []
        for name in re.split(r", | or ", field_cell):
            name = name.strip().strip("`")
            if name:
                names.append(name)
                record_fields.setdefault(type_name, [])
                if name not in record_fields[type_name]:
                    record_fields[type_name].append(name)
        field_rows.append([type_name, names, cells[header.index("d")], cells[header.index("w")]])
    if "- target:" in section:
        record_fields.setdefault("SETVALUE", ["target"])
    derived = {}
    for line in section.splitlines():
        match = re.match(r"Code derives (?:on )?([A-Z]+)?", line)
        if match:
            type_name = match.group(1) or "STATE"
            names = re.findall(r"`([a-z_]+)`", line)
            derived[type_name] = [name for name in names if name not in ("none", "loose", "tight")]
    start = text.index("### SHOT SC10-SH150 Not mint")
    shot_example = text[start:text.index("```", start)].strip().splitlines()
    chat_forms = re.findall(r"\(`(- (?:hear|lines): [^`]+)`\)", text[text.index("```", start):text.index("### 5.2 ")])
    start = text.index("### 5.3 IDs")
    end = text.index("**Who issues IDs.**", start)
    id_examples = []
    for line in text[start:end].splitlines():
        if line.startswith("| ") and not line.startswith("| Record"):
            cells = split_table_row(line)
            if len(cells) >= 3:
                for identifier in re.findall(r"`([A-Z][A-Z0-9.\-]*)`", cells[2]):
                    if identifier not in id_examples:
                        id_examples.append(identifier)
    start = text.index("### 5.7 The word list")
    end = text.index("### 5.8 Constants")
    retired = []
    for line in text[start:end].splitlines():
        if not line.startswith("| ") or line.startswith("| Thing"):
            continue
        cells = split_table_row(line)
        if len(cells) < 3 or set(cells[0]) <= set("-: "):
            continue
        for item in split_outside_parentheses(cells[2]):
            if item and item not in retired:
                retired.append(item)
    start = text.index("### 5.8 Constants")
    end = text.index("### 5.9 ")
    table_constants = []
    constant_rows = {}
    for line in text[start:end].splitlines():
        if line.startswith("| `"):
            cells = split_table_row(line)
            for name in re.findall(r"`([a-z0-9_]+)`", cells[0]):
                if name not in table_constants:
                    table_constants.append(name)
                constant_rows[name] = cells[1]
    start = text.index("### 7.2 Every check")
    end = text.index("### 7.3 ")
    check_ids = sorted(set(re.findall(r"\b(?:FORM|ID|CITE|COVER|TIME|STATE|SIDE|GEOM|CRAFT|INFO|REASON|WORDS|PLAN|GEN|FILM|PREVIS)-\d{2}\b",
                                      text[start:end])))
    backticked = sorted(set(re.findall(r"`([a-z][a-z0-9]*(?:_[a-z0-9]+)+)`", text)))
    constant_like = sorted(set(CONSTANT_LIKE.findall(text)))
    return {"record_fields": record_fields, "derived": derived, "retired": retired, "table_constants": table_constants,
            "backticked_names": backticked, "constant_like_names": constant_like, "check_ids": check_ids,
            "field_rows": field_rows, "shot_example": shot_example, "shot_example_chat_forms": chat_forms,
            "id_examples": id_examples, "constant_rows": constant_rows}


def field_by_name(record_types, type_name, field_name):
    for field in record_types[type_name]["fields"]:
        if field["name"] == field_name:
            return field
    raise KeyError(f"{type_name}.{field_name}")


def find_field(record_types, type_name, field_name):
    """The field with this name, or the field renamed from it, or None."""
    for field in record_types.get(type_name, {}).get("fields", []):
        if field["name"] == field_name or field.get("renamed_from") == field_name:
            return field
    return None


def normalise_retired(text):
    return text.replace("\"", "").replace("`", "").strip().lower()


def collect_schema_names(schema):
    """Every field name, sub-part key, value and schema key, for telling constants apart."""
    names = set(COMMON_FIELD_NAMES)

    def walk(value):
        if isinstance(value, dict):
            for key, inner in value.items():
                names.add(key)
                walk(inner)
        elif isinstance(value, list):
            for inner in value:
                if isinstance(inner, str):
                    names.add(inner)
                walk(inner)

    for record in schema["record_types"].values():
        for field in record["fields"]:
            names.add(field["name"])
            if field.get("renamed_from"):
                names.add(field["renamed_from"])
            walk(field.get("values"))
            walk(field.get("also_allowed"))
            if field.get("first_part"):
                walk(field["first_part"].get("values"))
            for sub_part in field.get("sub_parts", []):
                names.add(sub_part["key"])
                walk(sub_part.get("values"))
    walk({key: None for key in schema})
    for record in schema["record_types"].values():
        for field in record["fields"]:
            names.update(field.keys())
    names.update(schema["kinds"])
    names.update(schema["writers"])
    names.update(schema["conditions"])
    return names


def id_patterns(schema):
    """Every ID pattern by type name: record types and other_ids."""
    patterns = {}
    for type_name, record in schema["record_types"].items():
        if record.get("id_pattern"):
            patterns[type_name] = re.compile(record["id_pattern"])
    for type_name, other in schema["other_ids"].items():
        patterns[type_name] = re.compile(other["pattern"])
    return patterns


# ---------------------------------------------------------------- reading 5.5's d and w columns

def parenthesised_groups(cell):
    """Pairs (word before the brackets, text inside) for 'word (inside)' in a cell."""
    return re.findall(r"([a-z_]+)\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)", cell)


def expected_depths(names, cell):
    """The base depth letter 5.5's d cell gives each field of a row."""
    parts = [part.strip() for part in cell.split(";")]
    if len(names) > 1 and len(parts) == len(names) and not any(part.startswith("f all") for part in parts):
        return {name: part[0] for name, part in zip(names, parts)}
    result = {}
    rest_depth = None
    for value, inside in parenthesised_groups(cell):
        items = [item.strip().strip("`").split(" ")[0] for item in re.split(r"[,;]", inside)]
        if inside.strip() == "rest":
            rest_depth = value[0]
            continue
        for item in items:
            if item in names:
                result[item] = value[0]
    base = cell.strip()[0]
    return {name: result.get(name, rest_depth or base) for name in names}


def expected_writers(names, cell):
    """The writer 5.5's w cell gives each field of a row: a writer, 'code', or 'WHEN' for a conditional writer."""
    if cell.startswith("`writer_when`"):
        return {name: ("ai" if name in ("status", "reason") else "WHEN") for name in names}
    parts = [part.strip() for part in cell.split(";")]
    if len(names) > 1 and len(parts) == len(names) and all(re.match(WRITER_PATTERN, part) for part in parts):
        return {name: re.match(WRITER_PATTERN, part).group(0) for name, part in zip(names, parts)}
    if re.search(r"\(screenplay\)|for screenplays", cell):
        return {name: "WHEN" for name in names}
    result = {}
    for value, inside in parenthesised_groups(cell):
        for item in re.split(r"[,;]", inside):
            item = item.strip().strip("`")
            pair = re.match(r"([a-z_]+): (" + WRITER_PATTERN + r")$", item)
            if pair and pair.group(1) in names:
                result[pair.group(1)] = pair.group(2)
            elif item.split(" ")[0] in names and value in WRITERS | {"code"}:
                result[item.split(" ")[0]] = value
    remaining = re.sub(r"\([^()]*(?:\([^()]*\)[^()]*)*\)", "", cell)
    remaining_writers = re.findall(r"\b(" + WRITER_PATTERN + r")\b", remaining)
    plain = re.fullmatch(r"(" + WRITER_PATTERN + r"), (" + WRITER_PATTERN + r")", cell.strip())
    if plain and not result:
        return {name: (plain.group(1) if index == 0 else plain.group(2)) for index, name in enumerate(names)}
    unused = [writer for writer in remaining_writers if writer not in result.values()]
    default = unused[0] if unused else (remaining_writers[-1] if remaining_writers else None)
    return {name: result.get(name, default) for name in names}


def expected_chat_writer(names, cell):
    """Names whose w cell marks '(AI in chat)'."""
    marked = set()
    for value, inside in parenthesised_groups(cell):
        if "AI in chat" in inside:
            items = [item.strip().split(" ")[0] for item in re.split(r"[,;]", inside)]
            listed = [item for item in items if item in names]
            marked.update(listed or names)
    return marked


# ---------------------------------------------------------------- checking one value

NUMBER_KINDS = ("number", "seconds", "metres", "millimetres", "dollars", "words_per_second")
QUOTE = r'"[^"]+"'
LINES_VALUE = re.compile(r"(\d+(-\d+)?)(, \d+(-\d+)?)*|" + QUOTE + r"( to " + QUOTE + r")?")


def id_problem(identifier, id_types, patterns, where):
    """A problem when an ID fits none of its accepted types."""
    candidates = patterns.values() if (not id_types or "*" in id_types) else [patterns[t] for t in id_types if t in patterns]
    if any(pattern.fullmatch(identifier) for pattern in candidates):
        return []
    if id_types and ("*" in id_types or any(t in ("PLAN", "STYLE", "WORLD", "CAMSYS", "SOUNDPLAN", "LADDER", "PROJECT")
                                            for t in id_types)) and identifier.isupper() and identifier.isalpha():
        return []
    return [f"{where}: {identifier!r} is not an ID of {id_types or 'any type'}"]


def story_point_problem(value):
    return not re.fullmatch(r'SC\d{2,3}[A-Z]? "[^"]+"( = \S+)?|SC\d{2,3}[A-Z]?-B\d{2}', value)


def example_problems(value, definition, where, patterns):
    """Problems with one example value under its own field or sub-part definition."""
    problems = []
    kind = definition["kind"]
    if value in (definition.get("also_allowed") or []) or value in ("none", "open"):
        return problems
    if definition.get("pattern") and not re.fullmatch(definition["pattern"], value):
        problems.append(f"{where}: {value!r} does not match its pattern")

    def word_problem(word):
        allowed = [str(item).lower() for item in (definition.get("values") or []) + (definition.get("also_allowed") or [])]
        tidied = word.strip().lower().replace(" ", "_").replace("-", "_")
        if definition.get("values") is not None and tidied not in allowed + ["none", "open"]:
            problems.append(f"{where}: {word!r} is not an allowed value")

    if kind == "word":
        if "<ID>" in (definition.get("also_allowed") or []) and re.fullmatch(r"[A-Z][A-Z0-9.\-]+", value):
            return problems
        word_problem(value)
    elif kind == "word_list":
        for word in value.split(", "):
            word_problem(word)
    elif kind in NUMBER_KINDS:
        if not re.fullmatch(r"-?\d+(\.\d+)?", value):
            problems.append(f"{where}: {value!r} is not a number")
        else:
            if definition.get("values") and float(value) not in [float(item) for item in definition["values"]]:
                problems.append(f"{where}: {value} is not an allowed value")
            if definition.get("range") and not definition["range"][0] <= float(value) <= definition["range"][1]:
                problems.append(f"{where}: {value} is outside its range")
    elif kind == "yes_no" and value not in ("yes", "no"):
        problems.append(f"{where}: {value!r} is not yes or no")
    elif kind == "charge" and value not in ("---", "--", "-", "0", "+", "++", "+++"):
        problems.append(f"{where}: {value!r} is not a charge")
    elif kind == "span" and not re.fullmatch(r"\d+(\.\d+)?-\d+(\.\d+)?", value):
        problems.append(f"{where}: {value!r} is not a span")
    elif kind in ("point", "size") and not re.fullmatch(r"\[-?\d+(\.\d+)?(, -?\d+(\.\d+)?){1,2}\]", value):
        problems.append(f"{where}: {value!r} is not a point or size")
    elif kind == "story_point" and story_point_problem(value):
        problems.append(f"{where}: {value!r} is not a story point")
    elif kind == "scene_or_story_point":
        if not re.fullmatch(r"SC\d{2,3}[A-Z]?", value) and story_point_problem(value):
            if not any(p.fullmatch(value) for t, p in patterns.items() if t in (definition.get("id_types") or [])):
                problems.append(f"{where}: {value!r} is neither a scene ID nor a story point")
    elif kind == "quote" and not re.fullmatch(QUOTE, value):
        problems.append(f"{where}: {value!r} is not a quote")
    elif kind == "lines" and not LINES_VALUE.fullmatch(value):
        problems.append(f"{where}: {value!r} is not line numbers or a quote anchor")
    elif kind == "id":
        problems += id_problem(value, definition.get("id_types"), patterns, where)
    elif kind in ("id_list", "because_list", "reference_list"):
        for item in re.split(r", (?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", value):
            if kind == "because_list" and (re.fullmatch(r"line: ?(\d+(-\d+)?|" + QUOTE + r")", item) or item == "default"):
                continue
            if kind == "reference_list" and "." in item and not re.fullmatch(r".*\.S\d{2}", item):
                owner, _, field_name = item.rpartition(".")
                problems += id_problem(owner, ["*"], patterns, where)
                continue
            problems += id_problem(item, definition.get("id_types"), patterns, where)
    elif kind == "id_range":
        for item in re.split(r"\.\.|, ", value):
            problems += id_problem(item, definition.get("id_types"), patterns, where)
    return problems


def field_example_problems(type_name, field, patterns, value=None):
    """Check a field's value (its example by default), splitting items into first part and named sub-parts (G6)."""
    where = f"{type_name}.{field['name']}"
    example = str(field["example"] if value is None else value)
    if field["kind"] != "sub_parts":
        return example_problems(example, field, where, patterns)
    if example == "none" or example in (field.get("also_allowed") or []):
        return []
    problems = []
    pieces = example.split(" | ")
    sub_parts = {sub_part["key"]: sub_part for sub_part in field["sub_parts"]}
    if field.get("first_part") is not None:
        problems += example_problems(pieces[0], field["first_part"], where + " first part", patterns)
        pieces = pieces[1:]
    for piece in pieces:
        match = re.match(r"([a-z_]+): (.*)$", piece)
        if not match:
            problems.append(f"{where}: unnamed sub-part {piece!r}")
        elif match.group(1) not in sub_parts:
            problems.append(f"{where}: unknown sub-part {match.group(1)}")
        else:
            problems += example_problems(match.group(2), sub_parts[match.group(1)], f"{where}.{match.group(1)}", patterns)
    return problems


def value_at(value, path):
    for key in path:
        value = value[key]
    return value


# ---------------------------------------------------------------- the checks, one function per group

def check_coverage(loaded, expected):
    schema = loaded["_config/schema/schema.json"]
    record_types = schema["record_types"]
    missing_types = [name for name in expected["record_fields"] if name not in record_types]
    missing_fields = []
    field_total = 0
    for type_name, names in expected["record_fields"].items():
        if type_name not in record_types:
            continue
        for name in names:
            field_total += 1
            if find_field(record_types, type_name, name) is None:
                missing_fields.append(f"{type_name}.{name}")
    common = {field["name"] for field in schema["common_fields"]["fields"]}
    missing_common = [name for name in COMMON_FIELD_NAMES if name not in common]
    for type_name, names in expected["derived"].items():
        present = {field["name"] for field in record_types.get(type_name, {}).get("fields", [])}
        for name in names:
            field_total += 1
            if name not in present:
                missing_fields.append(f"{type_name}.{name} (code derives it)")
    if missing_types or missing_fields or missing_common:
        return [f"missing record types {missing_types}, fields {missing_fields}, common fields {missing_common}"], ""
    return [], (f"all {len(expected['record_fields'])} record types and {field_total} named fields "
                f"(plus the common fields {', '.join(COMMON_FIELD_NAMES)}) are in schema.json")


def all_fields_of(schema):
    fields = [(type_name, field) for type_name, record in schema["record_types"].items() for field in record["fields"]]
    return fields + [("common", field) for field in schema["common_fields"]["fields"]]


def check_field_attributes(loaded, expected):
    schema = loaded["_config/schema/schema.json"]
    step_values = set(schema["filled_by_step_order"]["values"])
    problems = []
    all_fields = all_fields_of(schema)
    for type_name, field in all_fields:
        where = f"{type_name}.{field['name']}"
        if field.get("depth") not in DEPTHS:
            problems.append(f"{where}: depth {field.get('depth')!r}")
        has_writer = "writer" in field
        has_writer_when = "writer_when" in field
        if has_writer == has_writer_when:
            problems.append(f"{where}: needs exactly one of writer and writer_when")
        if has_writer and field["writer"] not in WRITERS:
            problems.append(f"{where}: writer {field['writer']!r}")
        if has_writer_when:
            conditions = [pair["when"] for pair in field["writer_when"]]
            if len(conditions) < 2 or len(set(conditions)) != len(conditions):
                problems.append(f"{where}: writer_when needs two or more different conditions")
            for pair in field["writer_when"]:
                if pair["writer"] not in WRITERS or pair["when"] not in schema["conditions"]:
                    problems.append(f"{where}: writer_when entry {pair}")
        if field.get("chat_writer") not in (None, "ai"):
            problems.append(f"{where}: chat_writer {field.get('chat_writer')!r}")
        if str(field.get("filled_by_step")) not in step_values:
            problems.append(f"{where}: filled_by_step {field.get('filled_by_step')!r}")
        if not field.get("kind") in schema["kinds"]:
            problems.append(f"{where}: kind {field.get('kind')!r}")
        if not field.get("label") or not field.get("meaning") or field.get("example") in (None, ""):
            problems.append(f"{where}: label, meaning or example missing")
        if (field.get("writer") == "code_derived") != (field.get("stored") is False):
            problems.append(f"{where}: code_derived fields, and only they, are stored: false")
    if problems:
        return problems, ""
    return [], (f"all {len(all_fields)} fields have a depth, exactly one writer or writer_when, a filled_by_step, a kind, "
                f"a label, a meaning and an example; stored: false exactly on code_derived fields")


def check_depth_and_writer(loaded, expected):
    """Every field's depth and writer agree with 5.5's d and w columns, apart from the documented deviations."""
    schema = loaded["_config/schema/schema.json"]
    record_types = schema["record_types"]
    problems = []
    compared = 0
    for type_name, names, depth_cell, writer_cell in expected["field_rows"]:
        depths = expected_depths(names, depth_cell)
        writers = expected_writers(names, writer_cell)
        chat_names = expected_chat_writer(names, writer_cell)
        for name in names:
            field = find_field(record_types, type_name, name)
            if field is None:
                continue
            compared += 1
            where = f"{type_name}.{field['name']}"
            want_depth = DEPTH_OVERRIDES.get((type_name, name), depths[name])
            have_depth = field["depth"]
            equivalent = want_depth == "f" and have_depth == "s" and field.get("required_for_all_at") == "f"
            if have_depth != want_depth and not equivalent and where not in KNOWN_DEVIATIONS:
                problems.append(f"{where}: depth {have_depth}, 5.5 says {want_depth} ({depth_cell})")
            want_writer = writers[name]
            if "writer_when" in field:
                if want_writer != "WHEN" and where not in CONDITIONAL_WRITERS_ALLOWED and where not in KNOWN_DEVIATIONS:
                    problems.append(f"{where}: writer_when, 5.5 names one writer {want_writer} ({writer_cell})")
                have_writers = {pair["writer"] for pair in field["writer_when"]}
                if want_writer not in ("WHEN", None, "code") and want_writer not in have_writers:
                    problems.append(f"{where}: writer_when {sorted(have_writers)} lacks 5.5's writer {want_writer}")
            else:
                have_writer = field["writer"]
                matches = (have_writer == want_writer or
                           (want_writer == "code" and have_writer in ("code_state", "code_derived")))
                if not matches and where not in KNOWN_DEVIATIONS:
                    problems.append(f"{where}: writer {have_writer}, 5.5 says {want_writer} ({writer_cell})")
            if name in chat_names and field.get("chat_writer") != "ai" and field.get("writer") != "ai":
                problems.append(f"{where}: 5.5 marks it (AI in chat) but chat_writer is not ai")
    if problems:
        return problems, ""
    return [], (f"the depth and writer of all {compared} fields named in 5.5 agree with its d and w columns "
                f"({len(KNOWN_DEVIATIONS)} documented deviation, {len(CONDITIONAL_WRITERS_ALLOWED)} documented conditional writers)")


def check_named_steps_and_chat_writers(loaded, expected):
    schema = loaded["_config/schema/schema.json"]
    record_types = schema["record_types"]
    common = {field["name"]: field for field in schema["common_fields"]["fields"]}
    problems = []
    for path, step in EXPECTED_FILLED_BY_STEP.items():
        type_name, field_name = path.split(".")
        field = find_field(record_types, type_name, field_name)
        if field is None:
            problems.append(f"{path}: missing")
        elif str(field["filled_by_step"]) != str(step):
            problems.append(f"{path}: filled_by_step {field['filled_by_step']!r}, the blueprint says {step!r}")
    for path in EXPECTED_CHAT_WRITERS:
        type_name, field_name = path.split(".")
        field = common.get(field_name) if type_name == "common" else find_field(record_types, type_name, field_name)
        if field is None or (field.get("chat_writer") != "ai" and field.get("writer") != "ai"):
            problems.append(f"{path}: 5.2 names it a chat writer field, but the AI may not write it in chat")
    for type_name, record in record_types.items():
        default_step = str(record["designed_by_step"])
        if default_step not in schema["filled_by_step_order"]["values"]:
            problems.append(f"{type_name}: designed_by_step {default_step!r}")
    if problems:
        return problems, ""
    return [], (f"the {len(EXPECTED_FILLED_BY_STEP)} filled_by_step values and the {len(EXPECTED_CHAT_WRITERS)} chat writers "
                f"the blueprint names (5.2, 5.5, section 3) hold")


def check_id_patterns(loaded, expected):
    schema = loaded["_config/schema/schema.json"]
    record_types = schema["record_types"]
    patterns = id_patterns(schema)
    problems = []
    for type_name, record in record_types.items():
        if not record.get("files"):
            problems.append(f"{type_name}: no file")
        for file_name in record.get("files", []):
            if type_name not in schema["files"].get(file_name, []):
                problems.append(f"{type_name}: file {file_name!r} does not list the type in schema files")
        if record["singleton"]:
            continue
        try:
            pattern = re.compile(record["id_pattern"])
        except (re.error, TypeError) as error:
            problems.append(f"{type_name}: bad id_pattern ({error})")
            continue
        if not pattern.fullmatch(record["id_example"] or ""):
            problems.append(f"{type_name}: id_example {record['id_example']!r} does not match its pattern")
    for file_name, type_names in schema["files"].items():
        for type_name in type_names:
            if file_name not in record_types[type_name]["files"]:
                problems.append(f"schema files {file_name!r} lists {type_name}, whose files do not name it")
    for identifier in expected["id_examples"]:
        type_name = ID_EXAMPLE_TYPES.get(identifier)
        if type_name is None:
            problems.append(f"5.3 example {identifier} has no expected record type in this test")
            continue
        if not patterns[type_name].fullmatch(identifier):
            problems.append(f"5.3 example {identifier} does not match the {type_name} pattern")
    for identifier, type_name in ID_EXAMPLE_TYPES.items():
        if not patterns[type_name].fullmatch(identifier):
            problems.append(f"{identifier} does not match the {type_name} pattern")
    for identifier, type_name in BAD_IDS.items():
        if patterns[type_name].fullmatch(identifier):
            problems.append(f"the malformed ID {identifier} matches the {type_name} pattern")
    if problems:
        return problems, ""
    return [], (f"every type names its files and the file map agrees; every ID pattern compiles and matches its example; "
                f"all {len(expected['id_examples'])} example IDs of 5.3 match their types and {len(BAD_IDS)} malformed IDs do not")


def check_turn_shot_example(loaded, expected):
    """The turn shot of 5.1 (and its chat forms) is valid under the schema, and every Standard field is in it or has a reason."""
    schema = loaded["_config/schema/schema.json"]
    patterns = id_patterns(schema)
    fields = {field["name"]: field for field in schema["record_types"]["SHOT"]["fields"]}
    problems = []
    heading = expected["shot_example"][0]
    if not re.fullmatch(schema["record_heading"]["pattern"], heading):
        problems.append(f"heading {heading!r} does not match record_heading")
    lines = expected["shot_example"][1:] + expected["shot_example_chat_forms"]
    for line in lines:
        match = re.fullmatch(schema["field_line"]["pattern"], line)
        if not match:
            problems.append(f"{line!r} is not a field line")
            continue
        name, value = match.group(1), match.group(2)
        if name not in fields:
            problems.append(f"SHOT has no field {name}")
            continue
        if fields[name].get("stored") is False:
            problems.append(f"SHOT.{name} is code_derived but the example types it")
        problems += field_example_problems("SHOT", fields[name], patterns, value)
    rule_era = field_by_name(schema["record_types"], "RULE", "era")
    problems += field_example_problems("RULE", rule_era, patterns, "b | from: 263 | to: 1563 | frame: original")
    if problems:
        return problems, ""
    return [], (f"the turn shot of 5.1 ({len(lines)} field lines, with its chat forms) and SETVALUE's era item are valid "
                f"under the schema")


def check_retired_words(loaded, expected):
    words = loaded["_config/rules/words.json"]
    written = {normalise_retired(entry["as_written"]) for entry in words["retired"]}
    missing = [item for item in expected["retired"] if normalise_retired(item) not in written]
    if missing:
        return [f"missing from words.json: {missing}"], ""
    return [], f"all {len(expected['retired'])} retired words of 5.7 are in words.json"


def check_constants(loaded, expected):
    schema = loaded["_config/schema/schema.json"]
    constants = loaded["_config/rules/constants.json"]
    constant_names = set(constants["constants"]) | set(constants["from_blueprint_text"]["constants"])
    missing_table = [name for name in expected["table_constants"] if name not in constants["constants"]]
    schema_names = collect_schema_names(schema)
    candidates = sorted(set(expected["backticked_names"]) | set(expected["constant_like_names"]))
    unexplained = [name for name in candidates
                   if name not in constant_names and name not in schema_names and name not in NOT_CONSTANTS]
    problems = []
    for name, entry in list(constants["constants"].items()) + list(constants["from_blueprint_text"]["constants"].items()):
        for key in ("value", "unit", "meaning", "source"):
            if key not in entry or entry[key] in (None, ""):
                problems.append(f"{name}.{key} missing")
    for name, value in EXPECTED_CONSTANT_VALUES.items():
        entry = constants["constants"].get(name)
        if entry is None or entry["value"] != value:
            problems.append(f"{name}: {entry and entry['value']!r}, 5.8 says {value!r}")
        row = expected["constant_rows"].get(name, "")
        if isinstance(value, (int, float)) and not isinstance(value, bool) and row:
            numbers = [float(number) / (100 if percent else 1)
                       for number, percent in re.findall(r"(\d+(?:\.\d+)?)(%?)", row.replace(",", ""))]
            if float(value) not in numbers:
                problems.append(f"{name}: {value} no longer appears in its 5.8 row ({row})")
    for name, path, value in EXPECTED_CONSTANT_PARTS:
        try:
            have = value_at(constants["constants"][name]["value"], path)
        except (KeyError, TypeError):
            have = None
        if have != value:
            problems.append(f"{name} {'.'.join(path)}: {have!r}, 5.8 says {value!r}")
    if missing_table or unexplained or problems:
        return [f"missing 5.8 names {missing_table}; names in the blueprint that are neither constants nor schema names "
                f"{unexplained}; {problems}"], ""
    return [], (f"all {len(expected['table_constants'])} names of the 5.8 table are in constants.json with 5.8's values "
                f"({len(EXPECTED_CONSTANT_VALUES)} values and {len(EXPECTED_CONSTANT_PARTS)} parts compared); all "
                f"{len(candidates)} snake_case names in the blueprint are constants ({len(constant_names)} in the file), schema "
                f"names, or listed non-constants ({len(NOT_CONSTANTS)})")


def check_steps(loaded, expected):
    schema = loaded["_config/schema/schema.json"]
    record_types = schema["record_types"]
    steps = loaded["_config/schema/steps.json"]
    problems = []
    numbers = [step["step"] for step in steps["steps"]]
    if numbers != list(range(17)):
        problems.append(f"steps are {numbers}, not 0-16")
    check_ids = set(expected["check_ids"])
    unit_pattern = re.compile(schema["other_ids"]["UNIT"]["pattern"])
    for step in steps["steps"]:
        for check in step["checks"]:
            if re.fullmatch(r"[A-Z]+-\d{2}", check) and check not in check_ids:
                problems.append(f"step {step['step']}: unknown check {check}")
        files_written = [name.split(" (")[0] for name in step["files_written"]]
        for record in step["reads"] + step["writes"]:
            first_word = record.split(" ")[0]
            if first_word.isupper() and first_word not in record_types:
                problems.append(f"step {step['step']}: unknown record type {first_word}")
        for record in step["writes"]:
            first_word = record.split(" ")[0]
            if first_word in record_types:
                type_files = [name.split(" (")[0] for name in record_types[first_word]["files"]]
                folders = {name.split("/")[0] + "/" for name in type_files if "/" in name}
                if not (set(type_files) & set(files_written)) and not (folders & set(files_written)):
                    problems.append(f"step {step['step']}: writes {first_word} but names none of its files {type_files}")
        card_lists = []
        for key, value in step["cards"].items():
            if key == "by_tag":
                for parts in value.values():
                    card_lists.extend(parts)
            elif isinstance(value, list):
                card_lists.extend(value)
        units_only = "each unit loads only" in str(step["cards"].get("note", ""))
        for unit in step["units"]:
            card_lists.extend(unit.get("cards", []))
            if units_only and unit.get("surfaces") != "code" and not unit.get("cards"):
                problems.append(f"step {step['step']}: unit {unit['id_pattern']} loads no card part, and units here load "
                                f"only their own")
            if unit.get("example") and not unit_pattern.fullmatch(unit["example"]):
                problems.append(f"step {step['step']}: unit example {unit['example']} does not match the UNIT pattern")
        for part in card_lists:
            card = steps["cards"].get(part["card"])
            if card is None or part["part"] not in card["parts"]:
                problems.append(f"step {step['step']}: unknown card part {part}")
        if not step["units"]:
            problems.append(f"step {step['step']}: no units")
    for group in steps["chat_checks"].values():
        for check in group["checks"]:
            if check not in check_ids:
                problems.append(f"chat check {check} unknown")
    if len(steps["chat_checks"]["in_reply"]["checks"]) != 14 or len(steps["chat_checks"]["check_chat"]["checks"]) != 20:
        problems.append("chat checks are not 14 in the reply and 20 in the check chat (7.4)")
    tags = set(field_by_name(record_types, "SCENE", "tags")["values"])
    by_tag = steps["steps"][7]["cards"]["by_tag"]
    if set(by_tag) != tags:
        problems.append(f"step 7 by_tag covers {sorted(by_tag)}, SCENE.tags allows {sorted(tags)}")
    if problems:
        return problems, ""
    return [], ("steps 0-16 present; every check ID is in blueprint 7.2; every record type exists and every written type "
                "names one of its files; every card part is in the card list and every AI unit that loads only its own "
                "parts has some; unit examples match the UNIT pattern; 14 + 20 chat checks; step 7 covers every scene tag")


def check_limits_and_tones(loaded, expected):
    record_types = loaded["_config/schema/schema.json"]["record_types"]
    limits = loaded["_config/rules/limits.json"]
    tones = loaded["_config/rules/tone_defaults.json"]["tones"]
    problems = []
    if limits["handout_tokens_max"].get("claude_code") != 30000 or limits["handout_tokens_max"].get("chatgpt") != 20000:
        problems.append("handout ceilings are not 30,000 and 20,000")
    if limits["card_tokens_per_unit_max"]["value"] != 9000:
        problems.append("card tokens per unit is not 9,000")
    uploads = limits["files_per_upload"]
    if (uploads["gemini"]["value"], uploads["claude_web"]["value"], uploads["chatgpt"]["value"]) != (10, 20, 25):
        problems.append("files per upload are not 10, 20 and 25")
    if (limits["batch_size"]["default"], limits["batch_size"]["after_selftest"]) != (12, 18):
        problems.append("batch size is not 12 and 18")
    tone_values = set(field_by_name(record_types, "SCENE", "tone")["values"])
    if set(tones) != tone_values:
        problems.append(f"tone_defaults tones {sorted(tones)} differ from SCENE.tone {sorted(tone_values)}")
    needed = ["shot_length_factor", "size_and_lens", "camera_move", "contrast_band", "music_default", "display_level", "opener"]
    music_words = set(field_by_name(record_types, "SOUNDPLAN", "music_policy")["values"])
    contrast_words = set(field_by_name(record_types, "LOOK", "contrast")["values"])
    for tone_name, row in tones.items():
        for key in needed:
            if key not in row:
                problems.append(f"{tone_name} lacks {key}")
        if not isinstance(row.get("shot_length_factor"), (int, float)):
            problems.append(f"{tone_name} shot_length_factor is not a number")
        if row.get("music_default") not in music_words:
            problems.append(f"{tone_name} music_default {row.get('music_default')!r} is not a music_policy word")
        for band in row.get("contrast_band") or []:
            if band not in contrast_words:
                problems.append(f"{tone_name} contrast band {band!r} is not a LOOK contrast value")
    if problems:
        return problems, ""
    return [], (f"limits.json holds the 2.3 row (30,000 / 20,000 tokens, 9,000 card tokens, batch 12 / 18, 10 / 20 / 25 files); "
                f"tone_defaults.json has all {len(tones)} tones with every column, in the schema's own words")


def check_kinds_and_references(loaded, expected):
    """Every kind, first part, sub-part, id_types entry and condition refers to something the schema defines."""
    schema = loaded["_config/schema/schema.json"]
    kinds = set(schema["kinds"])
    types = set(schema["record_types"]) | set(schema["other_ids"]) | {"*"}
    conditions = set(schema["conditions"])
    problems = []
    for type_name, field in all_fields_of(schema):
        definitions = [("", field)]
        if field.get("first_part"):
            definitions.append((" first part", field["first_part"]))
        for sub_part in field.get("sub_parts", []):
            definitions.append((f" {sub_part['key']}", sub_part))
        if field["kind"] == "sub_parts" and "sub_parts" not in field:
            problems.append(f"{type_name}.{field['name']}: kind sub_parts without sub_parts")
        for suffix, definition in definitions:
            where = f"{type_name}.{field['name']}{suffix}"
            if definition.get("kind") not in kinds:
                problems.append(f"{where}: kind {definition.get('kind')!r}")
            for id_type in definition.get("id_types") or []:
                if id_type not in types:
                    problems.append(f"{where}: id_types entry {id_type!r}")
            if definition.get("kind") in ID_KINDS and not definition.get("id_types"):
                problems.append(f"{where}: kind {definition['kind']} without id_types")
            for key in ("required_when", "required_when_not"):
                if definition.get(key) and definition[key] not in conditions:
                    problems.append(f"{where}: {key} {definition[key]!r} is not a condition")
            for entry in definition.get("depth_when") or []:
                if entry["when"] not in conditions:
                    problems.append(f"{where}: depth_when {entry['when']!r} is not a condition")
    for type_name, record in schema["record_types"].items():
        if record.get("required_when") and record["required_when"] not in conditions:
            problems.append(f"{type_name}: required_when {record['required_when']!r} is not a condition")
    if problems:
        return problems, ""
    return [], "every kind, id_types entry and condition in every field, first part and sub-part is defined in the schema"


def check_examples(loaded, expected):
    schema = loaded["_config/schema/schema.json"]
    patterns = id_patterns(schema)
    problems = []
    for type_name, field in all_fields_of(schema):
        problems += field_example_problems(type_name, field, patterns)
    for kind_name, kind in schema["kinds"].items():
        if not kind.get("example"):
            problems.append(f"kind {kind_name} has no example")
    if problems:
        return problems, ""
    return [], ("every field's example is valid under its own kind, values, pattern, sub-parts and ID patterns")


CHECKS = [
    ("5.5 coverage", check_coverage),
    ("field attributes", check_field_attributes),
    ("5.5 depth and writer", check_depth_and_writer),
    ("named steps and chat writers", check_named_steps_and_chat_writers),
    ("record types and IDs", check_id_patterns),
    ("the turn shot of 5.1", check_turn_shot_example),
    ("retired words", check_retired_words),
    ("constants", check_constants),
    ("steps.json", check_steps),
    ("limits and tone defaults", check_limits_and_tones),
    ("kinds, ID types and conditions", check_kinds_and_references),
    ("examples", check_examples),
]


def run_checks(loaded, expected):
    """Run every check group; return the report lines and the names of the groups that failed."""
    lines, failures = [], []
    for name, check in CHECKS:
        problems, summary = check(loaded, expected)
        if problems:
            failures.append(name)
            shown = "; ".join(problems[:20]) + (f"; and {len(problems) - 20} more" if len(problems) > 20 else "")
            lines.append(f"FAIL  {name}: {len(problems)} problems: {shown}")
        else:
            lines.append(f"PASS  {name}: {summary}")
    return lines, failures


# ---------------------------------------------------------------- the self-test

def break_field(schema, type_name, field_name, **changes):
    field = field_by_name(schema["record_types"], type_name, field_name)
    for key, value in changes.items():
        if value is None:
            field.pop(key, None)
        else:
            field[key] = value


def remove_field(schema, type_name, field_name):
    fields = schema["record_types"][type_name]["fields"]
    fields[:] = [field for field in fields if field["name"] != field_name]


SELF_TEST_FAULTS = [
    ("remove SHOT.held", "5.5 coverage", lambda data: remove_field(data["_config/schema/schema.json"], "SHOT", "held")),
    ("give BEAT.turn two writers", "field attributes",
     lambda data: break_field(data["_config/schema/schema.json"], "BEAT", "turn", writer_when=[{"when": "turn_beat", "writer": "ai"}])),
    ("make SHOT.screen_time standard", "5.5 depth and writer",
     lambda data: break_field(data["_config/schema/schema.json"], "SHOT", "screen_time", depth="s")),
    ("make CHOICE.question a user field", "5.5 depth and writer",
     lambda data: break_field(data["_config/schema/schema.json"], "CHOICE", "question", writer="user")),
    ("fill PROJECT.frame_shape at step 3", "named steps and chat writers",
     lambda data: break_field(data["_config/schema/schema.json"], "PROJECT", "frame_shape", filled_by_step=3)),
    ("let shots have 2 digits", "record types and IDs",
     lambda data: data["_config/schema/schema.json"]["record_types"]["SHOT"].update(id_pattern=r"^SC\d{2,3}[A-Z]?-SH\d{2,3}$")),
    ("drop the value turn from SHOT.role", "the turn shot of 5.1",
     lambda data: break_field(data["_config/schema/schema.json"], "SHOT", "role", values=["must_keep", "normal"])),
    ("drop the retired word greybox", "retired words",
     lambda data: data["_config/rules/words.json"].update(
         retired=[entry for entry in data["_config/rules/words.json"]["retired"] if entry["word"] != "greybox"])),
    ("set handles_s to 0.5", "constants",
     lambda data: data["_config/rules/constants.json"]["constants"]["handles_s"].update(value=0.5)),
    ("remove loud_sets_max", "constants", lambda data: data["_config/rules/constants.json"]["constants"].pop("loud_sets_max")),
    ("take card 07 off the motif unit", "steps.json",
     lambda data: data["_config/schema/steps.json"]["steps"][4]["units"][0].pop("cards", None)),
    ("forget step 2's RULE file", "steps.json",
     lambda data: data["_config/schema/steps.json"]["steps"][2].update(
         files_written=[name for name in data["_config/schema/steps.json"]["steps"][2]["files_written"] if "06 World" not in name])),
    ("give ChatGPT 30,000 handout tokens", "limits and tone defaults",
     lambda data: data["_config/rules/limits.json"]["handout_tokens_max"].update(chatgpt=30000)),
    ("point SHOT.setup at an unknown type", "kinds, ID types and conditions",
     lambda data: break_field(data["_config/schema/schema.json"], "SHOT", "setup", id_types=["CAMERA_POSITION"])),
    ("write a bad SHOT.because example", "examples",
     lambda data: break_field(data["_config/schema/schema.json"], "SHOT", "because", example="SC10-B7, MO-MINT")),
]


def self_test(loaded, expected):
    """Break a copy of the files one fault at a time; each fault must fail its group and only make groups fail."""
    lines, broken = [], 0
    for description, group, apply_fault in SELF_TEST_FAULTS:
        data = copy.deepcopy(loaded)
        apply_fault(data)
        _, failures = run_checks(data, expected)
        if group in failures:
            lines.append(f"PASS  self-test: '{description}' fails '{group}'")
        else:
            broken += 1
            lines.append(f"FAIL  self-test: '{description}' should fail '{group}' but failed {failures or 'nothing'}")
    return lines, broken


def main():
    parser = argparse.ArgumentParser(description="Acceptance test for work package 1 (schema and rules).")
    parser.add_argument("--blueprint", help="path to the build blueprint (blueprint.md)")
    parser.add_argument("--self-test", action="store_true", help="also check that each check fails on a broken copy")
    options = parser.parse_args()
    lines = []
    loaded = {}
    load_failures = 0
    for relative_path in JSON_FILES:
        path = os.path.join(SKILL_FOLDER, relative_path)
        try:
            with open(path, encoding="utf-8") as handle:
                loaded[relative_path] = json.load(handle)
            lines.append(f"PASS  loads: {relative_path}")
        except (OSError, ValueError) as error:
            load_failures += 1
            lines.append(f"FAIL  loads: {relative_path}: {error}")
    if load_failures:
        print("\n".join(lines))
        print(f"\nRESULT: FAIL ({load_failures} files do not load)")
        return 1

    blueprint_path = options.blueprint or os.environ.get("STAGE_BLUEPRINT")
    if blueprint_path and os.path.exists(blueprint_path):
        with open(blueprint_path, encoding="utf-8") as handle:
            expected = read_blueprint_lists(handle.read())
        lines.append(f"INFO  lists read from the blueprint: {blueprint_path}")
        if expected != BLUEPRINT_SNAPSHOT:
            lines.append("INFO  the blueprint's lists differ from the stored snapshot (the blueprint has changed since 27 Sep 2026)")
        else:
            lines.append("INFO  the blueprint's lists equal the stored snapshot")
    else:
        expected = BLUEPRINT_SNAPSHOT
        lines.append("INFO  blueprint not given: using the stored snapshot of its lists (27 Sep 2026)")

    check_lines, failures = run_checks(loaded, expected)
    lines += check_lines
    broken = 0
    if options.self_test:
        self_lines, broken = self_test(loaded, expected)
        lines += self_lines
    print("\n".join(lines))
    groups = len(failures) + broken
    print(f"\nRESULT: {'PASS' if not groups else 'FAIL'} ({len(failures)} failing groups"
          + (f", {broken} self-test faults not caught)" if options.self_test else ")"))
    return 0 if not groups else 1


# SNAPSHOT START (generated from blueprint.md of 27 Sep 2026 by this file's read_blueprint_lists)
BLUEPRINT_SNAPSHOT = json.loads(r'''
{
 "record_fields": {
  "PROJECT": [
   "title",
   "source_file",
   "source_fingerprint",
   "source_kind",
   "source_format",
   "language",
   "depth",
   "surface",
   "code_execution",
   "batch_size",
   "training_off",
   "rights",
   "intended_use",
   "licensed_data_only",
   "format",
   "runtime_target_s",
   "scope",
   "frame_shape",
   "fps",
   "genre",
   "tone_home",
   "tone_range",
   "scene_id_digits",
   "prompt_words",
   "previs_colours",
   "spend_cap_usd",
   "hours_per_week",
   "schema_version",
   "checker_last_run",
   "model_facts_date"
  ],
  "CHOICE": [
   "question",
   "why",
   "option",
   "default",
   "answer",
   "asked",
   "checkpoint",
   "affects",
   "sets",
   "locks",
   "based_on",
   "status",
   "date"
  ],
  "SCENE": [
   "heading",
   "int_ext",
   "place_text",
   "time_text",
   "lines",
   "characters",
   "speaking",
   "transition_in",
   "transition_out",
   "presentation",
   "host",
   "event",
   "sequence",
   "scene_intensity",
   "whose_scene",
   "story_day",
   "rhythm_class",
   "tone",
   "tone_undercurrent",
   "tags",
   "depth",
   "target_duration_s",
   "keep",
   "merged_into",
   "from_lines",
   "five_test",
   "cardinal",
   "strands",
   "origin",
   "location",
   "sub_area",
   "look",
   "value",
   "want",
   "driver",
   "conflict",
   "third_thing",
   "staging",
   "start",
   "scene_idea",
   "department_idea",
   "turn_picture",
   "dial",
   "coverage",
   "rhythm_shape",
   "target_asl_s",
   "rupture",
   "tone_shift",
   "room_sound",
   "geography",
   "cause_chain",
   "escalation",
   "reversal",
   "action_score",
   "time_treatment",
   "departure",
   "additions",
   "flags"
  ],
  "PART": [
   "beats",
   "turn",
   "starts"
  ],
  "BEAT": [
   "lines",
   "action",
   "reaction",
   "task",
   "beat_intensity",
   "turn",
   "turn_kind",
   "charge",
   "flag",
   "engaged_pair",
   "silent_third",
   "five_steps",
   "landing_face",
   "unsaid",
   "carrier",
   "pause_after",
   "emphasis",
   "added_emphasis",
   "change",
   "distance",
   "core_word",
   "cut_rule",
   "fact"
  ],
  "SPEECH": [
   "speaker",
   "line",
   "text",
   "parenthetical",
   "extension",
   "path",
   "origin"
  ],
  "MOVE": [
   "beat",
   "who",
   "from",
   "to",
   "via",
   "start_s",
   "dur_s",
   "faces",
   "posture",
   "why",
   "origin"
  ],
  "SETUP": [
   "at",
   "at_words",
   "look_at",
   "lens_mm",
   "use",
   "side",
   "mount"
  ],
  "SHOTLIST": [
   "item",
   "approved"
  ],
  "SHOT": [
   "beats",
   "lines",
   "purpose",
   "because",
   "role",
   "kind",
   "why",
   "origin",
   "additions",
   "pov_break",
   "setup",
   "frame",
   "frame_detail",
   "size",
   "angle",
   "height",
   "lens_mm",
   "focus",
   "focus_on",
   "move",
   "move_reason",
   "mount",
   "stance",
   "dominant",
   "placement",
   "layers",
   "frame_in_frame",
   "device",
   "glass",
   "subject",
   "thing",
   "text",
   "keep_hidden",
   "must_show",
   "must_not_show",
   "physics_note",
   "motion",
   "light",
   "light_cue",
   "dark",
   "eye_light",
   "hear",
   "effect",
   "room_sound",
   "silence",
   "music",
   "needs_description",
   "screen_time",
   "moment",
   "start",
   "end",
   "cut_in_on",
   "cut_out_on",
   "time_slice",
   "held",
   "previs_level",
   "storyboard",
   "framing_critical",
   "pose_critical",
   "route",
   "model",
   "flip",
   "content_flags",
   "policy_route",
   "cost_class",
   "reuse_of",
   "departure",
   "gen_note"
  ],
  "CUT": [
   "to",
   "type",
   "split_s",
   "black_frames",
   "sound_across",
   "shared_geometry",
   "why"
  ],
  "PLAN": [
   "logline",
   "theme_question",
   "core_value",
   "core_opposition",
   "crisis",
   "climax",
   "act",
   "peak",
   "pov_plan",
   "genre",
   "tone_home",
   "tone_range",
   "tone_mix_rule",
   "plan_option",
   "loses",
   "op",
   "runtime_estimate",
   "scene_budget",
   "shot_budget"
  ],
  "SEQUENCE": [
   "title",
   "scenes",
   "story_job",
   "value_change",
   "act",
   "scene_intensity",
   "travel"
  ],
  "PLANT": [
   "what",
   "planted_at",
   "paid_off_at",
   "plant_emphasis",
   "payoff_emphasis",
   "rhyme",
   "motif"
  ],
  "FACT": [
   "what",
   "element",
   "audience_knows_from",
   "known_by",
   "mode"
  ],
  "CHAPTER": [
   "title",
   "lines",
   "words",
   "first_line",
   "last_line",
   "digest",
   "people",
   "places",
   "time_markers",
   "pov",
   "candidate"
  ],
  "STRAND": [
   "name",
   "chapters",
   "carries",
   "feeds",
   "decision",
   "reason",
   "seconds"
  ],
  "CARDINAL": [
   "event",
   "lines",
   "depends"
  ],
  "STYLE": [
   "medium",
   "style_words",
   "texture",
   "named_reference_policy",
   "words_to_avoid",
   "style_picture",
   "provisional"
  ],
  "WORLD": [
   "place",
   "period",
   "drives_on",
   "language",
   "accents",
   "signage",
   "emergency_lights",
   "institutions",
   "money",
   "evidence",
   "origin"
  ],
  "RULE": [
   "kind",
   "statement",
   "governs",
   "era",
   "exception",
   "occurrences",
   "policy",
   "template_setup",
   "varies"
  ],
  "CHARACTER": [
   "names",
   "tier",
   "role",
   "life_want",
   "arc",
   "thesis",
   "evidence",
   "fixed_description",
   "height_m",
   "build",
   "colour_identity",
   "tempo",
   "speech",
   "lineup",
   "face",
   "movement",
   "gesture",
   "status",
   "distance",
   "one_image",
   "expression",
   "skin_light",
   "voice",
   "likeness_basis",
   "consent"
  ],
  "VOICE": [
   "character",
   "voice_description",
   "pitch",
   "pace_wps",
   "accent",
   "path_sound",
   "source",
   "consent",
   "tool",
   "provider_voice",
   "texture",
   "habits"
  ],
  "LOCATION": [
   "headings",
   "story_job",
   "loudness",
   "room_sound",
   "anchor",
   "exit",
   "dressing",
   "plan_orientation",
   "size",
   "origin_corner",
   "axes",
   "wild_walls",
   "object",
   "mark"
  ],
  "PROP": [
   "names",
   "category",
   "kind",
   "fixed_description",
   "real_size",
   "surface",
   "side",
   "text",
   "first_seen",
   "motif"
  ],
  "TEXT": [
   "kind",
   "words",
   "on",
   "reader",
   "plot_critical",
   "emphasis",
   "method",
   "look",
   "animation",
   "translate"
  ],
  "MOTIF": [
   "meaning",
   "rank",
   "channel",
   "appearance",
   "signature",
   "direction",
   "pole",
   "test_score",
   "rule",
   "largest_payoff"
  ],
  "CAMERA": [
   "at",
   "lens_mm",
   "ratio",
   "fps",
   "overlays",
   "moves",
   "master_clip"
  ],
  "STATE": [
   "element",
   "from",
   "cause",
   "state_line",
   "changes",
   "side",
   "handedness",
   "pictures_needed",
   "origin"
  ],
  "CAMSYS": [
   "frame_shape_why",
   "lens_type",
   "lens_family",
   "normal_lens_mm",
   "step_change",
   "default_height",
   "default_move",
   "banned",
   "camera_speed",
   "break",
   "time_rule"
  ],
  "CAMRULE": [
   "character",
   "in_control",
   "losing_control",
   "never",
   "closest",
   "limit_before",
   "eyeline",
   "because"
  ],
  "RESERVE": [
   "choice",
   "match",
   "max_uses",
   "allowed_in",
   "never_on",
   "because"
  ],
  "LENS": [
   "mm",
   "only_in",
   "why",
   "because"
  ],
  "LOOK": [
   "for",
   "time",
   "look_block",
   "main_light",
   "neutral_white",
   "contrast",
   "fill",
   "stays_dark",
   "palette",
   "accent_allowed",
   "light_cue",
   "style_picture"
  ],
  "VISUAL": [
   "sequence",
   "frame_value",
   "saturation",
   "temperature",
   "dominant",
   "accent",
   "main_light",
   "contrast",
   "exit",
   "sub_row",
   "space",
   "component",
   "counterpoint"
  ],
  "SOUNDPLAN": [
   "music_policy",
   "clip_audio",
   "voice_policy",
   "device_budget",
   "rupture_plan",
   "loudness_target"
  ],
  "LADDER": [
   "rung"
  ],
  "FINDING": [
   "record",
   "rule",
   "evidence",
   "fix",
   "source",
   "status",
   "reason"
  ],
  "REVIEW": [
   "scope",
   "answer",
   "score"
  ],
  "PIC": [
   "for",
   "use",
   "moment",
   "model",
   "references",
   "file",
   "checks",
   "approved",
   "cost_usd"
  ],
  "PREVIS": [
   "for",
   "level",
   "standin_level",
   "route",
   "extras",
   "stills",
   "approved"
  ],
  "TAKE": [
   "clip",
   "model",
   "route",
   "inputs",
   "seed",
   "settings",
   "cost_usd",
   "file",
   "review",
   "kept",
   "refusals"
  ],
  "VOICETAKE": [
   "speech",
   "voice",
   "delivery",
   "tts_text",
   "tool",
   "file",
   "verdict",
   "cost_usd"
  ],
  "FINISH": [
   "shot",
   "operation",
   "tool",
   "inputs",
   "output",
   "done"
  ],
  "MUSIC": [
   "in",
   "out",
   "function",
   "must_not",
   "source",
   "licence"
  ],
  "RIGHTS": [
   "subject",
   "status",
   "holder",
   "licence",
   "evidence",
   "commercial_ok",
   "attribution",
   "disclosure"
  ],
  "SETVALUE": [
   "target"
  ]
 },
 "derived": {
  "SCENE": [
   "era",
   "frame_handedness",
   "switch_at",
   "duration_est_s"
  ],
  "SHOT": [
   "label",
   "min_screen_time_s",
   "clips",
   "era",
   "mirror_state",
   "mirror_route",
   "post_ops",
   "size_check",
   "face_height",
   "lip_sync",
   "dominant",
   "needs",
   "scene_model",
   "suggested_model"
  ],
  "STATE": [
   "until"
  ]
 },
 "retired": [
  "phase",
  "frame reversed",
  "turned (as a mirror state)",
  "handedness_phase",
  "mirror true",
  "MIRRORED",
  "mirror_state capitals",
  "mirror_flip",
  "identity key",
  "look line",
  "look ID",
  "costume phase C1-C6",
  "states S1-S6",
  "look key",
  "lighting block",
  "global look key",
  "look (for either)",
  "style key",
  "\"the film's look\"",
  "\"her look\"",
  "key light",
  "key shot",
  "key frame (as a written frame)",
  "keyframe",
  "first frame",
  "start frame",
  "structure image",
  "layout guide",
  "control video",
  "clay render",
  "greybox",
  "motion guide",
  "reference pack",
  "asset sheet",
  "stack",
  "model sheet",
  "style frame",
  "bit",
  "BEATS (in prompts)",
  "timeline events",
  "C4 beats",
  "beat",
  "movement",
  "part (for replies)",
  "stretch",
  "colour-script sequence",
  "journey unit",
  "\"move\" alone in user text",
  "POV for both",
  "objective",
  "intention",
  "super-intention",
  "spine",
  "scene desire",
  "action gerund",
  "playable action",
  "infinitives",
  "activity",
  "physical task",
  "emotion words",
  "behaviour as a plan field",
  "performance scale",
  "intensity (for display)",
  "screen direction (as a field name)",
  "beat reference (before step 7)",
  "mood (as a field)",
  "genre (for tone)",
  "continuity bible",
  "ledger",
  "state table",
  "damage ledger",
  "carrier log",
  "thread",
  "emblem",
  "hinge",
  "reserved framing",
  "reserved choice",
  "withhold",
  "withheld",
  "on-screen text",
  "insert graphic",
  "text spec",
  "sound key",
  "voice key",
  "room tone key",
  "bed",
  "ambience",
  "channel",
  "voice_source",
  "perspective",
  "camera position S1-S8",
  "screen left",
  "image-left",
  "camera left",
  "axis",
  "180° line",
  "big close-up",
  "EWS",
  "WS",
  "MCU",
  "CU",
  "ECU",
  "OTS and every abbreviation",
  "angle_height",
  "fact",
  "extracted",
  "authored",
  "added",
  "[design choice]",
  "derived",
  "human",
  "duration_s",
  "clip_s",
  "PURPOSE",
  "purpose (as picture job kind)",
  "purpose",
  "override:",
  "WHY slot",
  "story_reason",
  "L0-L3",
  "S0-S3",
  "emphasis device",
  "added signal",
  "intensity",
  "story intensity",
  "bible",
  "visual bible",
  "asset bible",
  "register",
  "core facts",
  "decision card",
  "question record",
  "small call",
  "decision (for a choice)",
  "question (for a choice)",
  "checkpoint letters in user text",
  "full (as a depth)",
  "issue",
  "stage (except \"Stage\", capitalised, the product's name, and `stage.py`, which WORDS-02 exempts)",
  "task",
  "call",
  "context pack",
  "clay preview",
  "greybox (for the user)",
  "v0",
  "v1 in user text",
  "generation job",
  "torch in prompts",
  "informal names"
 ],
 "table_constants": [
  "speech_wps_default",
  "clip_speech_rule",
  "speech_floor_extra_s",
  "text_floor",
  "pause_tiers",
  "long_pauses_per_scene_max",
  "turn_reaction_min_s",
  "handles_s",
  "non_dialogue_seconds_by_intensity",
  "scene_total_tolerance",
  "main_actions_per_seconds",
  "acting_characters_per_clip_max",
  "push_in_per_scene_max",
  "extreme_close_up_per_scene_max",
  "extreme_close_up_film_max",
  "push_in_scene_share_max",
  "departments_changing_at_main_turn_max",
  "signals_changing_per_beat_max",
  "display_3_needs_why_at_or_tighter",
  "hold_action_every_s",
  "head_height_m",
  "face_height_by_size",
  "motif_spines_max",
  "sound_motif_max",
  "body_motif_max",
  "loud_sets_max",
  "emphasis_3_rules",
  "added_emphasis_per_beat_max",
  "plant_emphasis_max",
  "device_budget_short",
  "fixed_description_words",
  "look_block_words_max",
  "batch_size",
  "repair_rounds_max",
  "plate_route_face_height",
  "lip_sync_tight_face_height",
  "model_facts_max_age_days",
  "takes_stop_per_route",
  "takes_stop_per_shot",
  "cheap_test_above_usd_per_take",
  "film_asl_range_s",
  "rhythm_class_asl_s",
  "v0_action_seconds_per_word",
  "size_ladder_thresholds",
  "caption_lead_s",
  "caption_min_s",
  "caption_max_s"
 ],
 "backticked_names": [
  "acting_characters_per_clip_max",
  "added_emphasis",
  "added_emphasis_per_beat_max",
  "as_look",
  "audience_knows_from",
  "batch_size",
  "beat_intensity",
  "body_motif_max",
  "caption_lead_s",
  "caption_max_s",
  "caption_min_s",
  "chat_writer",
  "cheap_test_above_usd_per_take",
  "checker_last_run",
  "clip_speech_rule",
  "close_up",
  "code_derived",
  "code_execution",
  "code_state",
  "content_flags",
  "cost_class",
  "cut_to_black",
  "defines_id",
  "departments_changing_at_main_turn_max",
  "depth_range_m",
  "designed_only",
  "device_budget_short",
  "display_3_needs_why_at_or_tighter",
  "duration_est_s",
  "dwell_s",
  "emphasis_3_rules",
  "extreme_close_up",
  "extreme_close_up_film_max",
  "extreme_close_up_per_scene_max",
  "face_height",
  "face_height_by_size",
  "facing_deg",
  "filled_by_step",
  "film_asl_range_s",
  "first_line",
  "fixed_description",
  "fixed_description_words",
  "focus_on",
  "frame_handedness",
  "frame_left",
  "frame_right",
  "frame_shape",
  "frame_value",
  "from_end_of",
  "from_lines",
  "glass_and_reflection",
  "handles_s",
  "head_height_m",
  "height_m",
  "hold_action_every_s",
  "holds_baseline",
  "in_story_footage",
  "int_ext",
  "intended_use",
  "known_by",
  "last_line",
  "lens_mm",
  "licensed_data",
  "light_cue",
  "likeness_basis",
  "limit_before",
  "lip_sync",
  "lip_sync_tight_face_height",
  "long_pauses_per_scene_max",
  "longest_hold",
  "look_at",
  "look_block_words_max",
  "loud_sets_max",
  "main_actions_per_seconds",
  "main_turn",
  "meaning_kept",
  "medium_close_up",
  "medium_high",
  "merged_into",
  "min_screen_time_s",
  "mirror_route",
  "mirror_state",
  "model_facts_max_age_days",
  "montage_and_time",
  "motif_spines_max",
  "music_policy",
  "must_keep",
  "must_not",
  "must_not_show",
  "must_show",
  "needs_description",
  "non_dialogue_seconds_by_intensity",
  "normal_lens_mm",
  "not_confirmed",
  "open_and_close",
  "overlapping_slices",
  "pace_wps",
  "pause_owed",
  "pause_tiers",
  "physics_note",
  "place_text",
  "plan_orientation",
  "plan_view",
  "plant_emphasis_max",
  "plate_route_face_height",
  "policy_route",
  "post_ops",
  "pov_break",
  "previs_colours",
  "previs_level",
  "prompt_words",
  "prose_interior",
  "push_in_per_scene_max",
  "push_in_scene_share_max",
  "remove_empty_rows",
  "repair_rounds_max",
  "rhythm_class",
  "rhythm_class_asl_s",
  "room_sound",
  "runtime_estimate",
  "runtime_target_s",
  "scene_id_digits",
  "scene_idea",
  "scene_intensity",
  "scene_model",
  "scene_total_tolerance",
  "screen_time",
  "screens_and_text",
  "shared_geometry",
  "signals_changing_per_beat_max",
  "silent_third",
  "size_check",
  "size_ladder_thresholds",
  "skin_light",
  "sound_emphasis",
  "sound_motif_max",
  "source_fingerprint",
  "source_kind",
  "speech_floor",
  "speech_floor_extra_s",
  "speech_wps_default",
  "spend_cap_usd",
  "standin_level",
  "start_s",
  "stays_dark",
  "story_day",
  "study_only",
  "sub_row",
  "suggested_model",
  "suspense_and_reveal",
  "switch_at",
  "takes_stop_per_route",
  "takes_stop_per_shot",
  "target_duration_s",
  "text_floor",
  "three_or_more",
  "tightest_size",
  "time_slice",
  "time_text",
  "tone_home",
  "tone_range",
  "tone_shift",
  "tone_undercurrent",
  "training_off",
  "transition_in",
  "tts_text",
  "turn_reaction_min_s",
  "v0_action_seconds_per_word",
  "voice_path",
  "voice_policy",
  "whose_scene",
  "words_match",
  "writer_when"
 ],
 "constant_like_names": [
  "acting_characters_per_clip_max",
  "added_emphasis_per_beat_max",
  "at_words",
  "audio_max",
  "body_motif_max",
  "caption_lead_s",
  "cheap_test_above_usd_per_take",
  "clip_speech_rule",
  "cut_rule",
  "departments_changing_at_main_turn_max",
  "emphasis_3_rules",
  "extreme_close_up_film_max",
  "extreme_close_up_per_scene_max",
  "face_height_by_size",
  "film_asl_range_s",
  "fixed_description_words",
  "hold_action_every_s",
  "hours_per_week",
  "lip_sync_tight_face_height",
  "long_pauses_per_scene_max",
  "look_block_words_max",
  "loud_sets_max",
  "main_actions_per_seconds",
  "model_facts_max_age_days",
  "motif_spines_max",
  "negative_default",
  "non_dialogue_seconds_by_intensity",
  "pause_tiers",
  "plant_emphasis_max",
  "plate_route_face_height",
  "price_usd_per_s",
  "prompt_words",
  "push_in_per_scene_max",
  "push_in_scene_share_max",
  "references_max",
  "repair_rounds_max",
  "rhythm_class_asl_s",
  "scene_total_tolerance",
  "signals_changing_per_beat_max",
  "size_ladder_thresholds",
  "sound_motif_max",
  "speech_floor_extra_s",
  "speech_wps_default",
  "style_words",
  "takes_stop_per_route",
  "takes_stop_per_shot",
  "target_asl_s",
  "time_rule",
  "tone_mix_rule",
  "v0_action_seconds_per_word",
  "videos_max"
 ],
 "check_ids": [
  "CITE-01",
  "CITE-02",
  "CITE-03",
  "CITE-04",
  "CITE-05",
  "CITE-06",
  "CITE-07",
  "COVER-01",
  "COVER-02",
  "COVER-03",
  "COVER-04",
  "COVER-05",
  "COVER-06",
  "COVER-07",
  "COVER-08",
  "CRAFT-01",
  "CRAFT-02",
  "CRAFT-03",
  "CRAFT-04",
  "CRAFT-05",
  "CRAFT-06",
  "CRAFT-07",
  "CRAFT-08",
  "CRAFT-09",
  "CRAFT-10",
  "CRAFT-11",
  "CRAFT-12",
  "CRAFT-13",
  "CRAFT-14",
  "CRAFT-15",
  "CRAFT-16",
  "CRAFT-17",
  "CRAFT-18",
  "CRAFT-19",
  "CRAFT-20",
  "CRAFT-21",
  "CRAFT-22",
  "CRAFT-23",
  "CRAFT-24",
  "CRAFT-25",
  "CRAFT-26",
  "CRAFT-27",
  "CRAFT-28",
  "PHYS-01",
  "PHYS-02",
  "PHYS-03",
  "PHYS-04",
  "PHYS-05",
  "PHYS-06",
  "PHYS-07",
  "PHYS-08",
  "PHYS-09",
  "PHYS-10",
  "PHYS-11",
  "ROUTE-01",
  "ROUTE-02",
  "ROUTE-03",
  "ROUTE-04",
  "ROUTE-05",
  "ROUTE-06",
  "ROUTE-07",
  "ROUTE-08",
  "ROUTE-09",
  "ROUTE-10",
  "ROUTE-11",
  "ROUTE-12",
  "ROUTE-13",
  "ROUTE-14",
  "ROUTE-15",
  "ROUTE-16",
  "ROUTE-17",
  "ROUTE-18",
  "ROUTE-19",
  "ROUTE-20",
  "ROUTE-21",
  "ROUTE-22",
  "ROUTE-23",
  "ROUTE-24",
  "ROUTE-25",
  "ROUTE-26",
  "ROUTE-27",
  "FILM-01",
  "FILM-02",
  "FILM-03",
  "FILM-04",
  "FILM-05",
  "FILM-06",
  "FILM-07",
  "FILM-08",
  "FILM-09",
  "FILM-10",
  "FILM-11",
  "FILM-12",
  "FORM-01",
  "FORM-02",
  "FORM-03",
  "FORM-04",
  "FORM-05",
  "FORM-06",
  "FORM-07",
  "FORM-08",
  "FORM-09",
  "FORM-10",
  "FORM-11",
  "FORM-12",
  "FORM-13",
  "GEN-01",
  "GEN-02",
  "GEN-03",
  "GEN-04",
  "GEN-05",
  "GEN-06",
  "GEN-07",
  "GEN-08",
  "GEN-09",
  "GEN-10",
  "GEN-11",
  "GEN-12",
  "GEN-13",
  "GEN-14",
  "GEN-15",
  "GEN-16",
  "GEN-17",
  "GEOM-01",
  "GEOM-02",
  "GEOM-03",
  "GEOM-04",
  "GEOM-05",
  "GEOM-06",
  "GEOM-07",
  "GEOM-08",
  "ID-01",
  "ID-02",
  "ID-03",
  "ID-04",
  "ID-05",
  "ID-06",
  "ID-07",
  "ID-08",
  "ID-09",
  "INFO-01",
  "INFO-02",
  "PLAN-01",
  "PLAN-02",
  "PLAN-03",
  "PLAN-04",
  "PLAN-05",
  "PREVIS-01",
  "PREVIS-02",
  "PREVIS-03",
  "REASON-01",
  "REASON-02",
  "REASON-03",
  "REASON-04",
  "REASON-05",
  "REASON-06",
  "REASON-07",
  "REASON-08",
  "REASON-09",
  "SIDE-01",
  "SIDE-02",
  "SIDE-03",
  "SIDE-04",
  "SIDE-05",
  "STATE-01",
  "STATE-02",
  "STATE-03",
  "STATE-04",
  "TIME-01",
  "TIME-02",
  "TIME-03",
  "TIME-04",
  "TIME-05",
  "TIME-06",
  "TIME-07",
  "TIME-08",
  "TIME-09",
  "TIME-10",
  "WORDS-01",
  "WORDS-02",
  "WORDS-03",
  "WORDS-04",
  "WORDS-05"
 ],
 "field_rows": [
  [
   "PROJECT",
   [
    "title"
   ],
   "q",
   "story (from the first title-page line or title heading; the AI may propose a clean title as a small choice)"
  ],
  [
   "PROJECT",
   [
    "source_file",
    "source_fingerprint"
   ],
   "q",
   "code_state"
  ],
  [
   "PROJECT",
   [
    "source_kind"
   ],
   "q",
   "code (AI confirms)"
  ],
  [
   "PROJECT",
   [
    "source_format"
   ],
   "q",
   "code"
  ],
  [
   "PROJECT",
   [
    "language"
   ],
   "q",
   "code"
  ],
  [
   "PROJECT",
   [
    "depth"
   ],
   "q",
   "user"
  ],
  [
   "PROJECT",
   [
    "surface",
    "code_execution",
    "batch_size"
   ],
   "q",
   "code_state (AI in chat)"
  ],
  [
   "PROJECT",
   [
    "training_off"
   ],
   "q",
   "user (CHOICE-003)"
  ],
  [
   "PROJECT",
   [
    "rights"
   ],
   "q",
   "user"
  ],
  [
   "PROJECT",
   [
    "intended_use"
   ],
   "m",
   "user"
  ],
  [
   "PROJECT",
   [
    "licensed_data_only"
   ],
   "m",
   "user"
  ],
  [
   "PROJECT",
   [
    "format"
   ],
   "q",
   "user (CHOICE-004, step 1)"
  ],
  [
   "PROJECT",
   [
    "runtime_target_s"
   ],
   "q",
   "user"
  ],
  [
   "PROJECT",
   [
    "scope"
   ],
   "q",
   "user (the length choice at A sets `all` for a screenplay; checkpoint P sets it for prose)"
  ],
  [
   "PROJECT",
   [
    "frame_shape"
   ],
   "q",
   "user"
  ],
  [
   "PROJECT",
   [
    "fps"
   ],
   "q",
   "ai"
  ],
  [
   "PROJECT",
   [
    "genre",
    "tone_home",
    "tone_range"
   ],
   "q",
   "code_state (copied from PLAN)"
  ],
  [
   "PROJECT",
   [
    "scene_id_digits"
   ],
   "q",
   "code_state"
  ],
  [
   "PROJECT",
   [
    "prompt_words"
   ],
   "s",
   "ai"
  ],
  [
   "PROJECT",
   [
    "previs_colours"
   ],
   "m",
   "code_state"
  ],
  [
   "PROJECT",
   [
    "spend_cap_usd",
    "hours_per_week"
   ],
   "m",
   "user"
  ],
  [
   "PROJECT",
   [
    "schema_version",
    "checker_last_run",
    "model_facts_date"
   ],
   "q",
   "code_state"
  ],
  [
   "CHOICE",
   [
    "question"
   ],
   "q",
   "ai"
  ],
  [
   "CHOICE",
   [
    "why"
   ],
   "q",
   "ai"
  ],
  [
   "CHOICE",
   [
    "option"
   ],
   "q",
   "ai"
  ],
  [
   "CHOICE",
   [
    "default"
   ],
   "q",
   "ai"
  ],
  [
   "CHOICE",
   [
    "answer"
   ],
   "q",
   "user"
  ],
  [
   "CHOICE",
   [
    "asked"
   ],
   "q",
   "ai"
  ],
  [
   "CHOICE",
   [
    "checkpoint"
   ],
   "q",
   "ai"
  ],
  [
   "CHOICE",
   [
    "affects"
   ],
   "q",
   "ai"
  ],
  [
   "CHOICE",
   [
    "sets"
   ],
   "q",
   "ai"
  ],
  [
   "CHOICE",
   [
    "locks"
   ],
   "o",
   "ai"
  ],
  [
   "CHOICE",
   [
    "based_on"
   ],
   "s",
   "ai"
  ],
  [
   "CHOICE",
   [
    "status",
    "date"
   ],
   "q",
   "code_state (AI in chat)"
  ],
  [
   "SCENE",
   [
    "heading",
    "int_ext",
    "place_text",
    "time_text"
   ],
   "q",
   "story for screenplays (AI in chat); ai when `source_kind` is not screenplay"
  ],
  [
   "SCENE",
   [
    "lines"
   ],
   "q",
   "story for screenplays (AI in chat, as an anchor pair); code_state derived from `from_lines` otherwise"
  ],
  [
   "SCENE",
   [
    "characters",
    "speaking"
   ],
   "q",
   "code_state (AI in chat)"
  ],
  [
   "SCENE",
   [
    "transition_in",
    "transition_out"
   ],
   "q",
   "story"
  ],
  [
   "SCENE",
   [
    "presentation",
    "host"
   ],
   "q",
   "ai"
  ],
  [
   "SCENE",
   [
    "event"
   ],
   "q",
   "ai"
  ],
  [
   "SCENE",
   [
    "sequence"
   ],
   "q",
   "ai"
  ],
  [
   "SCENE",
   [
    "scene_intensity"
   ],
   "q",
   "ai"
  ],
  [
   "SCENE",
   [
    "whose_scene"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "story_day"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "rhythm_class"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "tone",
    "tone_undercurrent"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "tags"
   ],
   "q",
   "ai"
  ],
  [
   "SCENE",
   [
    "depth"
   ],
   "o",
   "user (through the request, logged as a CHOICE)"
  ],
  [
   "SCENE",
   [
    "target_duration_s"
   ],
   "s",
   "code_state"
  ],
  [
   "SCENE",
   [
    "keep",
    "merged_into"
   ],
   "s* when compressing",
   "ai"
  ],
  [
   "SCENE",
   [
    "from_lines",
    "five_test",
    "cardinal",
    "strands"
   ],
   "q (prose)",
   "ai"
  ],
  [
   "SCENE",
   [
    "origin"
   ],
   "q",
   "ai"
  ],
  [
   "SCENE",
   [
    "location",
    "sub_area"
   ],
   "q; f",
   "ai"
  ],
  [
   "SCENE",
   [
    "look"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "value"
   ],
   "q (core), s (others)",
   "ai"
  ],
  [
   "SCENE",
   [
    "want"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "driver",
    "conflict",
    "third_thing"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "staging"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "start"
   ],
   "s* set plan exists",
   "ai"
  ],
  [
   "SCENE",
   [
    "scene_idea"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "department_idea"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "turn_picture"
   ],
   "q",
   "ai"
  ],
  [
   "SCENE",
   [
    "dial"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "coverage"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "rhythm_shape",
    "target_asl_s"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "rupture"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "tone_shift"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "room_sound"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "geography",
    "cause_chain",
    "escalation",
    "reversal",
    "action_score",
    "time_treatment"
   ],
   "s* action",
   "ai"
  ],
  [
   "SCENE",
   [
    "departure"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "additions"
   ],
   "s",
   "ai"
  ],
  [
   "SCENE",
   [
    "flags"
   ],
   "s",
   "ai"
  ],
  [
   "PART",
   [
    "beats",
    "turn",
    "starts"
   ],
   "s",
   "ai"
  ],
  [
   "BEAT",
   [
    "lines"
   ],
   "q",
   "ai"
  ],
  [
   "BEAT",
   [
    "action",
    "reaction"
   ],
   "s",
   "ai"
  ],
  [
   "BEAT",
   [
    "task"
   ],
   "s",
   "ai"
  ],
  [
   "BEAT",
   [
    "beat_intensity"
   ],
   "s",
   "ai"
  ],
  [
   "BEAT",
   [
    "turn",
    "turn_kind"
   ],
   "q",
   "ai"
  ],
  [
   "BEAT",
   [
    "charge"
   ],
   "s",
   "ai"
  ],
  [
   "BEAT",
   [
    "flag"
   ],
   "s (when found)",
   "ai"
  ],
  [
   "BEAT",
   [
    "engaged_pair",
    "silent_third"
   ],
   "s* tag `three_or_more`",
   "ai"
  ],
  [
   "BEAT",
   [
    "five_steps"
   ],
   "s* turns and intensity 4+",
   "ai"
  ],
  [
   "BEAT",
   [
    "landing_face"
   ],
   "s* turns, flagged lines, revealed facts, refusals; f all",
   "ai"
  ],
  [
   "BEAT",
   [
    "unsaid",
    "carrier"
   ],
   "s* turns; f all",
   "ai"
  ],
  [
   "BEAT",
   [
    "pause_after"
   ],
   "s",
   "ai"
  ],
  [
   "BEAT",
   [
    "emphasis",
    "added_emphasis"
   ],
   "s",
   "ai"
  ],
  [
   "BEAT",
   [
    "change"
   ],
   "s* turns",
   "ai"
  ],
  [
   "BEAT",
   [
    "distance",
    "core_word",
    "cut_rule",
    "fact"
   ],
   "f",
   "ai"
  ],
  [
   "SPEECH",
   [
    "speaker",
    "line",
    "text",
    "parenthetical",
    "extension",
    "path",
    "origin"
   ],
   "q",
   "story (screenplay), ai (prose)"
  ],
  [
   "MOVE",
   [
    "beat",
    "who",
    "from",
    "to",
    "via",
    "start_s",
    "dur_s",
    "faces",
    "posture",
    "why",
    "origin"
   ],
   "s* set plan; f",
   "ai"
  ],
  [
   "SETUP",
   [
    "at",
    "at_words",
    "look_at",
    "lens_mm",
    "use",
    "side",
    "mount"
   ],
   "s",
   "ai"
  ],
  [
   "SHOTLIST",
   [
    "item"
   ],
   "q",
   "ai"
  ],
  [
   "SHOTLIST",
   [
    "approved"
   ],
   "q",
   "code_state (AI in chat)"
  ],
  [
   "SHOT",
   [
    "beats",
    "lines"
   ],
   "q",
   "ai"
  ],
  [
   "SHOT",
   [
    "purpose"
   ],
   "q",
   "ai"
  ],
  [
   "SHOT",
   [
    "because"
   ],
   "q",
   "ai"
  ],
  [
   "SHOT",
   [
    "role"
   ],
   "q",
   "ai"
  ],
  [
   "SHOT",
   [
    "kind"
   ],
   "q",
   "ai"
  ],
  [
   "SHOT",
   [
    "why"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "origin",
    "additions"
   ],
   "q; s",
   "ai"
  ],
  [
   "SHOT",
   [
    "pov_break"
   ],
   "s* when used",
   "ai"
  ],
  [
   "SHOT",
   [
    "setup"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "frame"
   ],
   "q",
   "ai"
  ],
  [
   "SHOT",
   [
    "frame_detail"
   ],
   "f (s when reserved)",
   "ai"
  ],
  [
   "SHOT",
   [
    "size"
   ],
   "q",
   "ai"
  ],
  [
   "SHOT",
   [
    "angle"
   ],
   "q",
   "ai"
  ],
  [
   "SHOT",
   [
    "height"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "lens_mm",
    "focus",
    "focus_on"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "move",
    "move_reason"
   ],
   "q; s",
   "ai"
  ],
  [
   "SHOT",
   [
    "mount",
    "stance"
   ],
   "f",
   "ai"
  ],
  [
   "SHOT",
   [
    "dominant",
    "placement",
    "layers",
    "frame_in_frame",
    "device"
   ],
   "f (at Standard code derives `dominant` from `focus_on`, `role` and the first `subject`)",
   "ai"
  ],
  [
   "SHOT",
   [
    "glass"
   ],
   "s* glass in frame",
   "ai"
  ],
  [
   "SHOT",
   [
    "subject"
   ],
   "q",
   "ai"
  ],
  [
   "SHOT",
   [
    "thing"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "text"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "keep_hidden"
   ],
   "s* when a FACT's element is in the scene before its reveal",
   "ai"
  ],
  [
   "SHOT",
   [
    "must_show",
    "must_not_show"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "physics_note",
    "motion"
   ],
   "s* when used",
   "ai"
  ],
  [
   "SHOT",
   [
    "light",
    "light_cue"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "dark",
    "eye_light"
   ],
   "f",
   "ai"
  ],
  [
   "SHOT",
   [
    "hear"
   ],
   "q",
   "ai"
  ],
  [
   "SHOT",
   [
    "effect"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "room_sound",
    "silence",
    "music"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "needs_description"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "screen_time"
   ],
   "q",
   "ai"
  ],
  [
   "SHOT",
   [
    "moment"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "start",
    "end"
   ],
   "f (s for `from_end_of` when the join is a match cut or the scene is continuous action); s",
   "ai"
  ],
  [
   "SHOT",
   [
    "cut_in_on",
    "cut_out_on"
   ],
   "f; s",
   "ai"
  ],
  [
   "SHOT",
   [
    "time_slice"
   ],
   "s* overlapping slices",
   "ai"
  ],
  [
   "SHOT",
   [
    "held"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "previs_level",
    "storyboard"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "framing_critical",
    "pose_critical"
   ],
   "s; f",
   "ai"
  ],
  [
   "SHOT",
   [
    "route"
   ],
   "s (default auto)",
   "ai"
  ],
  [
   "SHOT",
   [
    "model"
   ],
   "o",
   "ai"
  ],
  [
   "SHOT",
   [
    "flip"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "content_flags",
    "policy_route"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "cost_class",
    "reuse_of"
   ],
   "s",
   "ai"
  ],
  [
   "SHOT",
   [
    "departure"
   ],
   "s* when used",
   "ai"
  ],
  [
   "SHOT",
   [
    "gen_note"
   ],
   "o",
   "ai"
  ],
  [
   "CUT",
   [
    "to"
   ],
   "s",
   "ai"
  ],
  [
   "CUT",
   [
    "type"
   ],
   "s",
   "ai"
  ],
  [
   "CUT",
   [
    "split_s",
    "black_frames"
   ],
   "s*",
   "ai"
  ],
  [
   "CUT",
   [
    "sound_across"
   ],
   "s*",
   "ai"
  ],
  [
   "CUT",
   [
    "shared_geometry"
   ],
   "s* match_cut",
   "ai"
  ],
  [
   "CUT",
   [
    "why"
   ],
   "s",
   "ai"
  ],
  [
   "PLAN",
   [
    "logline",
    "theme_question"
   ],
   "q",
   "ai"
  ],
  [
   "PLAN",
   [
    "core_value",
    "core_opposition"
   ],
   "q; s",
   "ai"
  ],
  [
   "PLAN",
   [
    "crisis"
   ],
   "q",
   "ai"
  ],
  [
   "PLAN",
   [
    "climax"
   ],
   "q",
   "ai"
  ],
  [
   "PLAN",
   [
    "act"
   ],
   "s",
   "ai"
  ],
  [
   "PLAN",
   [
    "peak"
   ],
   "s",
   "ai"
  ],
  [
   "PLAN",
   [
    "pov_plan"
   ],
   "s",
   "ai"
  ],
  [
   "PLAN",
   [
    "genre",
    "tone_home",
    "tone_range",
    "tone_mix_rule"
   ],
   "q (genre, tone_home), s (rest)",
   "ai"
  ],
  [
   "PLAN",
   [
    "plan_option"
   ],
   "q (prose)",
   "ai"
  ],
  [
   "PLAN",
   [
    "loses",
    "op"
   ],
   "s* compressing or prose",
   "ai"
  ],
  [
   "PLAN",
   [
    "runtime_estimate",
    "scene_budget",
    "shot_budget"
   ],
   "q",
   "code_state"
  ],
  [
   "SEQUENCE",
   [
    "title",
    "scenes",
    "story_job",
    "value_change",
    "act",
    "scene_intensity",
    "travel"
   ],
   "q (title, scenes, value_change), s (rest)",
   "ai"
  ],
  [
   "PLANT",
   [
    "what",
    "planted_at",
    "paid_off_at",
    "plant_emphasis",
    "payoff_emphasis",
    "rhyme",
    "motif"
   ],
   "s",
   "ai"
  ],
  [
   "FACT",
   [
    "what",
    "element",
    "audience_knows_from",
    "known_by",
    "mode"
   ],
   "s* mode suspense, mystery or dramatic_irony (about 5-15 in a film); f all",
   "ai"
  ],
  [
   "CHAPTER",
   [
    "title",
    "lines",
    "words",
    "first_line",
    "last_line"
   ],
   "q",
   "story (title, lines, words; AI in chat as anchors), ai (first_line, last_line)"
  ],
  [
   "CHAPTER",
   [
    "digest",
    "people",
    "places",
    "time_markers",
    "pov"
   ],
   "q",
   "ai"
  ],
  [
   "CHAPTER",
   [
    "candidate"
   ],
   "q",
   "ai"
  ],
  [
   "STRAND",
   [
    "name",
    "chapters",
    "carries",
    "feeds",
    "decision",
    "reason",
    "seconds"
   ],
   "q (prose)",
   "ai"
  ],
  [
   "CARDINAL",
   [
    "event",
    "lines",
    "depends"
   ],
   "q (prose, compression)",
   "ai"
  ],
  [
   "STYLE",
   [
    "medium"
   ],
   "q",
   "user"
  ],
  [
   "STYLE",
   [
    "style_words"
   ],
   "q",
   "ai"
  ],
  [
   "STYLE",
   [
    "texture"
   ],
   "s",
   "ai"
  ],
  [
   "STYLE",
   [
    "named_reference_policy",
    "words_to_avoid"
   ],
   "q",
   "code_state; ai"
  ],
  [
   "STYLE",
   [
    "style_picture"
   ],
   "m",
   "ai"
  ],
  [
   "STYLE",
   [
    "provisional"
   ],
   "q",
   "code_state"
  ],
  [
   "WORLD",
   [
    "place",
    "period",
    "drives_on",
    "language"
   ],
   "q",
   "user (place, period via CHOICE), ai (drives_on, language)"
  ],
  [
   "WORLD",
   [
    "accents",
    "signage",
    "emergency_lights",
    "institutions",
    "money"
   ],
   "s",
   "ai"
  ],
  [
   "WORLD",
   [
    "evidence",
    "origin"
   ],
   "s",
   "ai"
  ],
  [
   "RULE",
   [
    "kind",
    "statement",
    "governs"
   ],
   "q",
   "ai"
  ],
  [
   "RULE",
   [
    "era"
   ],
   "q (mirror rules)",
   "user (via a CHOICE and its SETVALUE records)"
  ],
  [
   "RULE",
   [
    "exception"
   ],
   "s",
   "ai"
  ],
  [
   "RULE",
   [
    "occurrences",
    "policy",
    "template_setup",
    "varies"
   ],
   "q (device rules)",
   "ai"
  ],
  [
   "CHARACTER",
   [
    "names"
   ],
   "q",
   "story"
  ],
  [
   "CHARACTER",
   [
    "tier",
    "role"
   ],
   "q",
   "ai"
  ],
  [
   "CHARACTER",
   [
    "life_want",
    "arc",
    "thesis"
   ],
   "s",
   "ai"
  ],
  [
   "CHARACTER",
   [
    "evidence"
   ],
   "s",
   "ai"
  ],
  [
   "CHARACTER",
   [
    "fixed_description"
   ],
   "q",
   "ai (then locked)"
  ],
  [
   "CHARACTER",
   [
    "height_m",
    "build",
    "colour_identity",
    "tempo",
    "speech"
   ],
   "s",
   "ai"
  ],
  [
   "CHARACTER",
   [
    "lineup"
   ],
   "s (principals)",
   "ai"
  ],
  [
   "CHARACTER",
   [
    "face",
    "movement",
    "gesture",
    "status",
    "distance"
   ],
   "s (principals); f all",
   "ai"
  ],
  [
   "CHARACTER",
   [
    "one_image",
    "expression"
   ],
   "f",
   "ai"
  ],
  [
   "CHARACTER",
   [
    "skin_light"
   ],
   "m (add-on C, once casting is chosen)",
   "ai"
  ],
  [
   "CHARACTER",
   [
    "voice",
    "likeness_basis",
    "consent"
   ],
   "s; q; m",
   "ai; user; user"
  ],
  [
   "VOICE",
   [
    "character",
    "voice_description"
   ],
   "s",
   "ai"
  ],
  [
   "VOICE",
   [
    "pitch",
    "pace_wps",
    "accent"
   ],
   "s",
   "ai"
  ],
  [
   "VOICE",
   [
    "path_sound"
   ],
   "s",
   "ai"
  ],
  [
   "VOICE",
   [
    "source"
   ],
   "s",
   "user"
  ],
  [
   "VOICE",
   [
    "consent",
    "tool",
    "provider_voice",
    "texture",
    "habits"
   ],
   "m",
   "ai"
  ],
  [
   "LOCATION",
   [
    "headings",
    "story_job",
    "loudness",
    "room_sound",
    "anchor",
    "exit",
    "dressing"
   ],
   "s",
   "story (headings), ai"
  ],
  [
   "LOCATION",
   [
    "plan_orientation"
   ],
   "s* set plan",
   "ai"
  ],
  [
   "LOCATION",
   [
    "size",
    "origin_corner",
    "axes",
    "wild_walls",
    "object",
    "mark"
   ],
   "s* (4, step 4 rule); f all",
   "ai"
  ],
  [
   "PROP",
   [
    "names",
    "category",
    "kind",
    "fixed_description",
    "real_size",
    "surface",
    "side",
    "text",
    "first_seen",
    "motif"
   ],
   "q (names, category), s (rest), f (kind, surface)",
   "story, ai"
  ],
  [
   "TEXT",
   [
    "kind",
    "words",
    "on",
    "reader",
    "plot_critical",
    "emphasis",
    "method",
    "look",
    "animation",
    "translate"
   ],
   "q (kind, words, on), s (rest), f (look, translate)",
   "story (words in the script), ai"
  ],
  [
   "MOTIF",
   [
    "meaning",
    "rank",
    "channel",
    "appearance",
    "signature"
   ],
   "s",
   "ai"
  ],
  [
   "MOTIF",
   [
    "direction",
    "pole",
    "test_score",
    "rule",
    "largest_payoff"
   ],
   "f",
   "ai"
  ],
  [
   "CAMERA",
   [
    "at",
    "lens_mm",
    "ratio",
    "fps",
    "overlays",
    "moves",
    "master_clip"
   ],
   "s",
   "ai"
  ],
  [
   "STATE",
   [
    "element"
   ],
   "q",
   "ai"
  ],
  [
   "STATE",
   [
    "from"
   ],
   "q",
   "ai"
  ],
  [
   "STATE",
   [
    "cause"
   ],
   "s",
   "ai"
  ],
  [
   "STATE",
   [
    "state_line"
   ],
   "q",
   "ai"
  ],
  [
   "STATE",
   [
    "changes"
   ],
   "s",
   "ai"
  ],
  [
   "STATE",
   [
    "side"
   ],
   "s",
   "ai"
  ],
  [
   "STATE",
   [
    "handedness"
   ],
   "s* mirror rule",
   "ai (user confirms at B)"
  ],
  [
   "STATE",
   [
    "pictures_needed"
   ],
   "m",
   "ai"
  ],
  [
   "STATE",
   [
    "origin"
   ],
   "q",
   "ai"
  ],
  [
   "CAMSYS",
   [
    "frame_shape_why"
   ],
   "s",
   "ai"
  ],
  [
   "CAMSYS",
   [
    "lens_type",
    "lens_family",
    "normal_lens_mm",
    "step_change"
   ],
   "s",
   "ai"
  ],
  [
   "CAMSYS",
   [
    "default_height",
    "default_move"
   ],
   "q",
   "ai"
  ],
  [
   "CAMSYS",
   [
    "banned"
   ],
   "q",
   "ai"
  ],
  [
   "CAMSYS",
   [
    "camera_speed",
    "break",
    "time_rule"
   ],
   "q; s; s",
   "ai"
  ],
  [
   "CAMRULE",
   [
    "character",
    "in_control",
    "losing_control",
    "never",
    "closest",
    "limit_before",
    "eyeline",
    "because"
   ],
   "s",
   "ai"
  ],
  [
   "RESERVE",
   [
    "choice",
    "match",
    "max_uses",
    "allowed_in",
    "never_on",
    "because"
   ],
   "q",
   "ai"
  ],
  [
   "LENS",
   [
    "mm",
    "only_in",
    "why",
    "because"
   ],
   "s",
   "ai"
  ],
  [
   "LOOK",
   [
    "for",
    "time",
    "look_block"
   ],
   "s",
   "ai"
  ],
  [
   "LOOK",
   [
    "main_light"
   ],
   "s",
   "ai"
  ],
  [
   "LOOK",
   [
    "neutral_white",
    "contrast",
    "fill",
    "stays_dark",
    "palette",
    "accent_allowed",
    "light_cue",
    "style_picture"
   ],
   "s (m for picture)",
   "ai"
  ],
  [
   "VISUAL",
   [
    "sequence",
    "frame_value",
    "saturation",
    "temperature",
    "dominant",
    "accent",
    "main_light",
    "contrast",
    "exit"
   ],
   "s",
   "ai"
  ],
  [
   "VISUAL",
   [
    "sub_row"
   ],
   "f",
   "ai"
  ],
  [
   "VISUAL",
   [
    "space",
    "component",
    "counterpoint"
   ],
   "s",
   "ai"
  ],
  [
   "SOUNDPLAN",
   [
    "music_policy"
   ],
   "q",
   "user"
  ],
  [
   "SOUNDPLAN",
   [
    "clip_audio",
    "voice_policy"
   ],
   "q",
   "code_state; user"
  ],
  [
   "SOUNDPLAN",
   [
    "device_budget",
    "rupture_plan",
    "loudness_target"
   ],
   "s; s; f",
   "ai"
  ],
  [
   "LADDER",
   [
    "rung"
   ],
   "s",
   "ai"
  ],
  [
   "FINDING",
   [
    "record",
    "rule",
    "evidence",
    "fix",
    "source",
    "status",
    "reason"
   ],
   "q",
   "`writer_when`: code_state when `source: checker` (except `status` and `reason`, ai), ai otherwise"
  ],
  [
   "REVIEW",
   [
    "scope",
    "answer",
    "score"
   ],
   "s",
   "ai"
  ],
  [
   "PIC",
   [
    "for",
    "use",
    "moment",
    "model",
    "references",
    "file",
    "checks",
    "approved",
    "cost_usd"
   ],
   "m",
   "ai / user (approved); the AI sets storyboard frames approved when every check passes, and the user names only frames to redo"
  ],
  [
   "PREVIS",
   [
    "for",
    "level",
    "standin_level",
    "route",
    "extras",
    "stills",
    "approved"
   ],
   "m",
   "ai / user (approved); code_state for stubs (`status: planned`); code_derived plan_file, blocking"
  ],
  [
   "TAKE",
   [
    "clip",
    "model",
    "route",
    "inputs",
    "seed",
    "settings",
    "cost_usd",
    "file",
    "review",
    "kept",
    "refusals"
   ],
   "m",
   "ai / user (kept)"
  ],
  [
   "VOICETAKE",
   [
    "speech",
    "voice",
    "delivery",
    "tts_text",
    "tool",
    "file",
    "verdict",
    "cost_usd"
   ],
   "m",
   "ai (verdict: user); code_derived `words_match`"
  ],
  [
   "FINISH",
   [
    "shot",
    "operation",
    "tool",
    "inputs",
    "output",
    "done"
   ],
   "m",
   "code_state (shot, operation); ai (tool, inputs, output, done)"
  ],
  [
   "MUSIC",
   [
    "in",
    "out",
    "function",
    "must_not",
    "source",
    "licence"
   ],
   "m",
   "ai"
  ],
  [
   "RIGHTS",
   [
    "subject",
    "status",
    "holder",
    "licence",
    "evidence",
    "commercial_ok",
    "attribution",
    "disclosure"
   ],
   "q (source), m (rest)",
   "user (subject, status, holder, licence, commercial_ok); ai (evidence, attribution, disclosure)"
  ]
 ],
 "shot_example": [
  "### SHOT SC10-SH150 Not mint",
  "- beats: SC10-B07, SC10-B08",
  "- lines: 454-466",
  "- purpose: Iona's body admits what her words denied; Saye's proof lands on her face.",
  "- because: SC10-B07, SC10-V1, MO-MINT, CR-IONA",
  "- role: turn",
  "- kind: live",
  "- setup: SC10-SU02",
  "- frame: single",
  "- size: close_up",
  "- angle: eye_level",
  "- height: eye:CH-IONA",
  "- lens_mm: 50",
  "- focus: moderate",
  "- focus_on: CH-IONA",
  "- move: static",
  "- subject: CH-IONA.S02 | at: left_third | faces: camera | eyeline: CH-SAYE | dwell_s: 15 | does: chews slowly; stops chewing; a small frown; chews once more, slowly; then listens | tactic: discovering | energy: held | display: 1 | still: head, hands, torso | travel: none",
  "- hear: SC10-D10 | speaker: off_screen",
  "- hear: SC10-D11 | speaker: on_screen",
  "- hear: SC10-D12 | speaker: off_screen",
  "- thing: MO-MINT | emphasis: 2",
  "- screen_time: 15",
  "- moment: 0-4 | shows: chews slowly, eyes on Saye just right of the lens",
  "- moment: 4-6 | shows: stops chewing; a small frown; chews once more, slowly",
  "- moment: 6-8 | shows: says two words, unsteady",
  "- moment: 8-15 | shows: listens, does not speak; swallows once; eyes stay on Saye",
  "- end: still, mouth closed, eyes on Saye",
  "- silence: room_sound_only",
  "- music: none",
  "- needs_description: yes",
  "- cut_out_on: thought_complete",
  "- why: \"Her face changes.\" puts the turn inside her mouth, so the scene's closest frame is spent here and held while Saye's proof lands off screen, on its target.",
  "- previs_level: 0",
  "- storyboard: yes",
  "- cost_class: dialogue",
  "- origin: story"
 ],
 "shot_example_chat_forms": [
  "- hear: SC10-D11 | speaker: on_screen | words: \"Not mint.\"",
  "- lines: \"Iona chews it.\" to \"street signs either.\""
 ],
 "id_examples": [
  "CATCH",
  "LONG",
  "SC10",
  "SC06A",
  "SC104",
  "SC10-P2",
  "SC10-V1",
  "SC10-B07",
  "SC10-D11",
  "SC10-M04",
  "SC10-SU02",
  "SC10-LIST",
  "SC10-SH150",
  "SC10-SH150.1",
  "SC10-C200",
  "SQ03",
  "CP01",
  "ST-01",
  "CF-05",
  "PL-07",
  "FT-03",
  "CH-IONA",
  "LOC-SAYE-KITCHEN",
  "WR-MIRROR",
  "CR-ELI",
  "VS-SQ03",
  "RC-01",
  "LX-01",
  "CH-IONA.S02",
  "PR-FLASK.S02",
  "CHOICE-021",
  "FIND-004",
  "RV-SC10",
  "CHOICE-014-A",
  "PIC-SC10-SH150-START-01",
  "PV-SC10-SH080-V01",
  "TK-SC10-SH150.1-T03",
  "VT-SC10-D11-T01",
  "FX-SC10-SH080-01"
 ],
 "constant_rows": {
  "speech_wps_default": "2.5 words per second (per-voice `pace_wps` overrides; Saye 2.0)",
  "clip_speech_rule": "Σ(words ÷ pace) ≤ clip length − 1.0 s (17 words in 8 s at 2.5)",
  "speech_floor_extra_s": "0.5 s per speech",
  "text_floor": "max(2.0, 1.0 + characters ÷ 13); emphasis ≥ 2: at least 2.0 + 0.5 × words; mirrored × 2",
  "pause_tiers": "half-open ranges: short [0, 1.0) s; medium [1.0, 2.5) s (\"(beat)\" = 1.0 s); long [2.5, 4.0] s (\"Silence.\" and \"She waits.\" 2.5-3 s; \"A long moment\" 3-4 s); above 4.0 s a `hold`, which needs a saved choice (RC)",
  "long_pauses_per_scene_max": "2",
  "turn_reaction_min_s": "2.0",
  "handles_s": "0.75 each end",
  "non_dialogue_seconds_by_intensity": "1: 5-8; 2: 3.5-6; 3: 2.5-4; 4: 1-3; 5: under 1 or 6 and over",
  "scene_total_tolerance": "±10% of `target_duration_s`",
  "main_actions_per_seconds": "at most 1 per 4 s unless the shot is marked compound",
  "acting_characters_per_clip_max": "3",
  "push_in_per_scene_max": "1, 1 (on the main turn); caps, never quotas",
  "extreme_close_up_per_scene_max": "1, 1 (on the main turn); caps, never quotas",
  "extreme_close_up_film_max": "non-insert extreme close-ups: 3 in a short, 6 in a feature [judgement]; push-ins in at most 0.25 of scenes; both written as film-level RESERVE records at step 6",
  "push_in_scene_share_max": "non-insert extreme close-ups: 3 in a short, 6 in a feature [judgement]; push-ins in at most 0.25 of scenes; both written as film-level RESERVE records at step 6",
  "departments_changing_at_main_turn_max": "2",
  "signals_changing_per_beat_max": "2 of size, light, sound, camera move and colour",
  "display_3_needs_why_at_or_tighter": "close_up",
  "hold_action_every_s": "2.0 (a held moment needs at least one small timed action every 2.0 s; it replaced hold_needs_still_s, Project notes 43)",
  "head_height_m": "0.23",
  "face_height_by_size": "extreme_close_up 0.6; close_up 0.4; medium_close_up 0.25; medium 0.15; medium_wide 0.1; wide 0.05; extreme_wide 0.02 (used when no set plan exists)",
  "motif_spines_max": "visual spines 3-5 in a short, 5-8 in a feature; 1 sound motif; 1 body motif",
  "sound_motif_max": "visual spines 3-5 in a short, 5-8 in a feature; 1 sound motif; 1 body motif",
  "body_motif_max": "visual spines 3-5 in a short, 5-8 in a feature; 1 sound motif; 1 body motif",
  "loud_sets_max": "2 in a short; 3 in a feature",
  "emphasis_3_rules": "at most 1 per motif in the film; at most 2 per scene, on different turns, never in consecutive shots",
  "added_emphasis_per_beat_max": "1; 0 where the script marks the beat",
  "plant_emphasis_max": "1; 2 for a plot-event plant",
  "device_budget_short": "at most 2 each of editor-made cut to black, true silence, freeze",
  "fixed_description_words": "principal 25-40; minor 20-30",
  "look_block_words_max": "60",
  "batch_size": "12 default; 18 after the self-test passes",
  "repair_rounds_max": "3",
  "plate_route_face_height": "0.10 of frame height",
  "lip_sync_tight_face_height": "0.15 of frame height [judgement, tune in test]",
  "model_facts_max_age_days": "30",
  "takes_stop_per_route": "4, 10",
  "takes_stop_per_shot": "4, 10",
  "cheap_test_above_usd_per_take": "2",
  "film_asl_range_s": "3-7 for the home tones grave and tense; other home tones scale it by their shot-length factor in `tone_defaults.json`",
  "rhythm_class_asl_s": "action_peak 2.0; suspense 3.5; mixed 4.0; dialogue 4.5; contemplative 6.0; read only by `estimate.py`, never a design target",
  "v0_action_seconds_per_word": "0.166-0.220",
  "size_ladder_thresholds": "section 5.6",
  "caption_lead_s": "0.25; 1.0; 7.0 (5.9)",
  "caption_min_s": "0.25; 1.0; 7.0 (5.9)",
  "caption_max_s": "0.25; 1.0; 7.0 (5.9)"
 }
}
''')
# SNAPSHOT END

if __name__ == "__main__":
    sys.exit(main())
