"""The grammar checks FORM-01 to FORM-13 of blueprint section 7.2, one function per check.

Each check_form_NN(record_files, context) takes parsed record files (record_format.RecordFile) and a
FormContext, and returns a list of problem lines (record_format.Problem, which is a str) in the format of
7.2: level, check ID, record, field, what is wrong, then the allowed values or the fix.

    E FORM-04 SC10-SH150 size "closeup shot" is not an allowed value. Did you mean close_up? ...

FORM_CHECKS maps each check ID to its function, so the checker (check_records.py) can register them;
run_form_checks runs several in order. apply_tidy_fixes makes the FORM-13 tidy fixes in the records.
condition_reader and ConditionReader answer the schema's named conditions (required_when, writer_when),
which other checks can reuse.

Standard library only.

After the full run on The Catch (Project notes 31 and 32):
- FORM-08 never judges text code wrote, and reads 'as before' as English unless it stands for the value or points
  back; FORM-05 does not ask for a shot list's approved mark before its group of shots has passed.

After the three-scene test of the fixed kit (Project notes 35 and 36):
- the big choices' fields wait for checkpoint B; the prices date is judged by GEN-11, not FORM-05; a missing user
  field is asked through a choice.
"""

import difflib
import re
from dataclasses import dataclass, field as dataclass_field

from .record_format import (DEPTH_RANK, DEPTH_WORD, FieldLine, Problem, ValueExaminer, closest, examine_field,
                            is_missing, merge_copies, normalise_name, normalise_word, parse_story_point,
                            quote_for_message, split_item, split_list, split_outside_quotes, value_for_comparison)

SCENE_PREFIX = re.compile(r"^(SC\d{2,3}[A-Z]?)(?:-|$)")
# Values code gives a new record itself; the AI writing the same value on a new record changes nothing (FORM-10).
CODE_DEFAULTS = {"status": ("draft", "open", "planned"), "locked": ("no",), "date": ("none",)}
ANSWERED = ("answered", "defaulted")


# ---------------------------------------------------------------- the context every check reads

@dataclass
class FormContext:
    """What the FORM checks need besides the records.

    depth: the project's depth (quick, standard, detailed); step: the step checked (None means --all);
    written_by_ai: True for an inbox the AI wrote (apply), which turns on the writer and lock checks against
    current_records (what is stored now, keyed by (TYPE, ID)); code_execution: yes or no (chat without code);
    index: every record of the project merged by ID, for conditions; modules: add-on letters switched on.
    """
    schema: object
    words: dict = None
    depth: str = "standard"
    step: object = None
    code_execution: str = "yes"
    written_by_ai: bool = False
    current_records: dict = None
    index: dict = None
    modules: set = None
    checkpoints: dict = None
    cache: dict = dataclass_field(default_factory=dict)

    @classmethod
    def for_records(cls, schema, words, record_files, other_record_files=(), step=None, written_by_ai=False,
                    current_records=None, depth=None, code_execution=None, modules=None):
        """Build a context from the files checked plus any others of the project (for conditions and choices)."""
        index, _ = merge_copies(list(other_record_files) + list(record_files), schema)
        project = next((record for key, record in index.items() if key[0] == "PROJECT"), None)
        if depth is None:
            depth = (project.get("depth") if project else None) or "standard"
            if depth == "open":
                depth = "standard"
        if code_execution is None:
            code_execution = (project.get("code_execution") if project else None) or "yes"
        if modules is None:
            modules = set()
            for type_name, letters in (("PIC", "AC"), ("PREVIS", "B"), ("TAKE", "C"), ("VOICETAKE", "C"),
                                       ("FINISH", "D"), ("MUSIC", "D")):
                # A grey preview job code made at step 8 (status planned) does not switch add-on B on: only the
                # add-on fills it (blueprint 9; WP4a's note).
                if any(key[0] == type_name and not is_previs_stub(key, record) for key, record in index.items()):
                    modules.update(letters)
        return cls(schema=schema, words=words or {}, depth=depth, step=step, code_execution=code_execution,
                   written_by_ai=written_by_ai, current_records=current_records or {}, index=index,
                   modules=modules)

    @property
    def examiner(self):
        if "examiner" not in self.cache:
            self.cache["examiner"] = ValueExaminer(self.schema, self.words)
        return self.cache["examiner"]

    @property
    def conditions(self):
        if "conditions" not in self.cache:
            self.cache["conditions"] = ConditionReader(self.schema, self.index or {}, self.depth)
        return self.cache["conditions"]


def make_problem(level, check_id, record_file, record, field_name, what, fix="", line_number=None):
    """A Problem located in a file (and a record, when there is one)."""
    label = record.label if record is not None else quote_for_message(record_file.name)
    line = line_number or (record.heading_line_number if record is not None else None)
    return Problem(level, check_id, label, field_name, what, fix, file_name=record_file.name, line_number=line)


# ---------------------------------------------------------------- conditions (required_when, writer_when)

class ConditionReader:
    """Answers the schema's named conditions for a record: True, False, or None when the records cannot tell."""

    def __init__(self, schema, index, depth):
        self.schema = schema
        self.index = index
        self.depth = depth
        self.project = next((record for key, record in index.items() if key[0] == "PROJECT"), None)

    def find(self, type_name, identifier):
        return self.index.get((type_name, identifier))

    def scene_of(self, record):
        if record is None or not record.identifier:
            return None
        match = SCENE_PREFIX.match(record.identifier)
        return self.find("SCENE", match.group(1)) if match else None

    def depth_rank_for(self, record):
        """The project's depth, or the scene's own depth when it is deeper ("Go deeper on scene 13")."""
        rank = DEPTH_RANK.get(self.depth, 2)
        scene = self.scene_of(record)
        if scene is not None and scene.get("depth") in DEPTH_RANK:
            rank = max(rank, DEPTH_RANK[scene.get("depth")])
        return rank

    def holds(self, condition, record, item=None):
        method = getattr(self, "condition_" + condition, None)
        if method is None:
            return None
        return method(record, item)

    # -- the conditions of schema.json, each answered where the records can tell
    def _source_kind(self):
        return self.project.get("source_kind") if self.project is not None else None

    def condition_source_is_screenplay(self, record, item):
        kind = self._source_kind()
        return None if kind in (None, "open") else kind == "screenplay"

    def condition_source_not_screenplay(self, record, item):
        kind = self._source_kind()
        return None if kind in (None, "open") else kind != "screenplay"

    def condition_compressing(self, record, item):
        if self.condition_source_not_screenplay(record, item):
            return True
        return None

    def condition_character_has_cue(self, record, item):
        speakers = set()
        for key, other in self.index.items():
            if key[0] == "SCENE":
                for value in other.get_all("speaking"):
                    speakers.add(split_item(value).first)
            if key[0] == "SPEECH" and other.get("speaker"):
                speakers.add(other.get("speaker"))
        if not speakers:
            return None
        return record.identifier in speakers

    def _location_has_plan(self, location):
        if location is None:
            return None
        return bool(location.get("size") or location.get_all("object") or location.get_all("mark"))

    def condition_set_plan_exists(self, record, item):
        if record.type_name == "LOCATION":
            return self._location_has_plan(record)
        scene = record if record.type_name == "SCENE" else self.scene_of(record)
        if scene is None or not scene.get("location"):
            return None
        return self._location_has_plan(self.find("LOCATION", scene.get("location")))

    def _scene_tags(self, record):
        scene = record if record.type_name == "SCENE" else self.scene_of(record)
        if scene is None or scene.get("tags") is None:
            return None
        return [normalise_word(tag) for tag in split_list(scene.get("tags"))]

    def condition_action_scene(self, record, item):
        tags = self._scene_tags(record)
        return None if tags is None else "action" in tags

    def condition_tag_three_or_more(self, record, item):
        tags = self._scene_tags(record)
        return None if tags is None else "three_or_more" in tags

    def condition_turn_beat(self, record, item):
        turn = record.get("turn")
        return None if turn is None else normalise_word(turn) != "none"

    def condition_turn_or_intense_beat(self, record, item):
        if self.condition_turn_beat(record, item):
            return True
        intensity = record.get("beat_intensity")
        if intensity and re.fullmatch(r"\d+", intensity):
            return int(intensity) >= 4
        return None if record.get("turn") is None else False

    def condition_dialogue_pass_beat(self, record, item):
        if self.depth_rank_for(record) >= 3:
            return True
        if self.condition_turn_beat(record, item) or record.get_all("flag") or record.get("fact"):
            return True
        return None

    def condition_principal(self, record, item):
        character = record if record.type_name == "CHARACTER" else self.find("CHARACTER", record.get("character") or "")
        if character is None or character.get("tier") is None:
            return None
        return normalise_word(character.get("tier")) == "principal"

    def condition_mirror_rule_exists(self, record, item):
        rules = [other for key, other in self.index.items() if key[0] == "RULE"]
        if not rules:
            return None
        return any(normalise_word(rule.get("kind") or "") == "mirror" for rule in rules)

    def condition_mirror_rule(self, record, item):
        kind = record.get("kind")
        return None if kind is None else normalise_word(kind) == "mirror"

    def condition_device_rule(self, record, item):
        kind = record.get("kind")
        return None if kind is None else normalise_word(kind) == "device"

    def condition_fact_mode_needs_record(self, record, item):
        mode = record.get("mode")
        return None if mode is None else normalise_word(mode) in ("suspense", "mystery", "dramatic_irony")

    def condition_eyeline_set(self, record, item):
        if item is None:
            return None
        return bool(item.get("eyeline")) and normalise_word(item.get("eyeline")) != "none"

    def condition_overlapping_slices(self, record, item):
        scene = record if record.type_name == "SCENE" else self.scene_of(record)
        if scene is None or scene.get("time_treatment") is None:
            return None
        return normalise_word(scene.get("time_treatment")) == "overlapping_slices"

    def _cut_type(self, record):
        value = record.get("type")
        return None if value is None else normalise_word(value)

    def condition_cut_is_split(self, record, item):
        cut = self._cut_type(record)
        return None if cut is None else cut in ("j_cut", "l_cut")

    def condition_cut_has_black(self, record, item):
        cut = self._cut_type(record)
        return None if cut is None else cut in ("cut_to_black", "fade", "freeze")

    def condition_cut_is_match(self, record, item):
        cut = self._cut_type(record)
        return None if cut is None else cut == "match_cut"

    def condition_presentation_on_device(self, record, item):
        presentation = record.get("presentation")
        return None if presentation is None else normalise_word(presentation) in ("on_screen", "recording")

    def condition_choice_answered(self, record, item):
        status = record.get("status")
        return None if status is None else normalise_word(status) == "answered"

    def condition_choice_settled(self, record, item):
        status = record.get("status")
        return None if status is None else normalise_word(status) in ("answered", "defaulted")

    def condition_rights_subject_source(self, record, item):
        subject = record.get("subject")
        return None if subject is None else normalise_word(subject) == "source"

    def condition_storyboard_frame(self, record, item):
        use = record.get("use")
        return None if use is None else normalise_word(use) == "storyboard"

    def condition_framing_critical(self, record, item):
        shot = self.find("SHOT", record.get("for") or "")
        if shot is None or shot.get("framing_critical") is None:
            return None
        return normalise_word(shot.get("framing_critical")) == "yes"

    def condition_previs_stub(self, record, item):
        status = record.get("status")
        return None if status is None else normalise_word(status) == "planned"

    def condition_checker_finding(self, record, item):
        source = record.get("source")
        return None if source is None else normalise_word(source) == "checker"

    def condition_text_in_story(self, record, item):
        origin = record.get("origin")
        return None if origin is None else normalise_word(origin) == "story"

    def condition_depth_detailed(self, record, item):
        return self.depth_rank_for(record) >= 3

    def condition_depth_below_detailed(self, record, item):
        return self.depth_rank_for(record) < 3

    def condition_when_used(self, record, item):
        return False

    def condition_music_policy_allows_cues(self, record, item):
        plan = next((other for key, other in self.index.items() if key[0] == "SOUNDPLAN"), None)
        if plan is None or plan.get("music_policy") is None:
            return None
        return normalise_word(plan.get("music_policy")) in ("sparse", "scored")

    # -- writers
    def writer_for(self, definition, record):
        """The one writer of a field for this record, or None when a condition cannot be decided."""
        if definition.get("writer"):
            return definition["writer"]
        for entry in definition.get("writer_when", []):
            if entry["when"] == "otherwise":
                return entry["writer"]
            answer = self.holds(entry["when"], record)
            if answer is True:
                return entry["writer"]
            if answer is None:
                return None
        return None


# ---------------------------------------------------------------- the shared analysis of field lines

def resolve_field(schema, words, record, field_name, index=None):
    """(definition, target name, how) for a field line: its own definition, a known synonym, or None.

    how is 'field', 'synonym' (a retired name read as its replacement, FORM-13) or None (unknown, FORM-03).
    SETVALUE accepts the fields of its target's record type.
    """
    type_name = record.type_name
    if type_name == "SETVALUE" and field_name != "target":
        target_type = setvalue_target_type(schema, record)
        if target_type is None:
            return None, field_name, None
        type_name = target_type
    definition = schema.field(type_name, field_name)
    if definition is not None:
        return definition, field_name, "field"
    synonyms = (words or {}).get("field_name_synonyms", {})
    scoped = synonyms.get("scoped", {}).get(type_name, {})
    target = scoped.get(field_name) or synonyms.get("names", {}).get(field_name)
    if target and schema.field(type_name, target) is not None:
        return schema.field(type_name, target), target, "synonym"
    return None, field_name, None


def setvalue_target_type(schema, record):
    """The record type a SETVALUE's target names (a record ID, or the type name of a singleton or PROJECT)."""
    target = (record.get("target") or "").strip()
    if not target:
        return None
    if target in schema.record_types:
        return target
    types = [name for name in schema.types_for_id(target) if name in schema.record_types]
    return types[0] if types else None


def field_suggestion(schema, words, type_name, field_name):
    synonyms = (words or {}).get("field_name_synonyms", {})
    target = synonyms.get("scoped", {}).get(type_name, {}).get(field_name) or synonyms.get("names", {}).get(field_name)
    if target and schema.field(type_name, target) is not None:
        return f"Did you mean {target}?"
    matches = [match for match in closest(field_name, schema.field_names(type_name))
               if difflib.SequenceMatcher(None, field_name, match).ratio() >= 0.75]
    if matches:
        return f"Did you mean {matches[0]}?"
    return "Fix: use a field of this record type (reference/03 Field guide lists them)"


def analyse(record_files, context):
    """One pass over every field line: FORM-02 (declared IDs), 03, 04, 12 and 13 problems, and the tidy plan.

    Cached in the context. Returns (problems, tidy plan); the plan lists (record, field line, name, value).
    """
    key = ("analysis",) + tuple(id(record_file) for record_file in record_files)
    if key in context.cache:
        return context.cache[key]
    schema = context.schema
    examiner = context.examiner
    problems = []
    plan = []
    for record_file in record_files:
        for record in record_file.records:
            for note in record.heading_tidy_notes:
                problems.append(make_problem("N", "FORM-13", record_file, record, None, note))
            if not record.known_type:
                continue
            seen_single = {}
            for line in record.fields:
                for note in line.tidy_notes:
                    problems.append(make_problem("N", "FORM-13", record_file, record, None, note, line_number=line.line_number))
                definition, name, how = resolve_field(schema, context.words, record, line.name)
                if definition is None:
                    written = line.written_name or line.name
                    type_for_message = record.type_name
                    if record.type_name == "SETVALUE" and line.name != "target":
                        target_type = setvalue_target_type(schema, record)
                        if target_type is None:
                            problems.append(make_problem("E", "FORM-03", record_file, record, written,
                                                         "cannot be checked: the SETVALUE has no target that names a record type",
                                                         "Fix: write - target: <record ID or singleton type> first",
                                                         line.line_number))
                            continue
                        type_for_message = target_type
                    problems.append(make_problem("E", "FORM-03", record_file, record, written,
                                                 f"is not a field of {type_for_message}",
                                                 field_suggestion(schema, context.words, type_for_message, line.name),
                                                 line.line_number))
                    continue
                if how == "synonym":
                    problems.append(make_problem("N", "FORM-13", record_file, record, line.written_name or line.name,
                                                 f"read as {name} (the one word for this field)", "",
                                                 line.line_number))
                if line.missing:
                    written_value = line.value if line.value else "blank"
                    problems.append(make_problem("N", "FORM-13", record_file, record, name,
                                                 f"{quote_for_message(written_value)} reads as missing (G7)",
                                                 "Write none for empty, or open for a question to the user",
                                                 line.line_number))
                    continue
                tidied, issues = examine_field(examiner, record.type_name, line, definition)
                context.cache[("tidied", id(line))] = tidied
                if not definition.get("repeat"):
                    previous = seen_single.get(name)
                    if previous is not None:
                        previous_value = context.cache.get(("tidied", id(previous)), previous.value)
                        if value_for_comparison(previous_value, definition) == value_for_comparison(tidied, definition):
                            problems.append(make_problem("N", "FORM-13", record_file, record, name,
                                                         "is written twice with the same value; the second line is a duplicate",
                                                         "", line.line_number))
                            plan.append((record, line, None, None))
                        continue
                    seen_single[name] = line
                for sub_part, issue in issues:
                    if sub_part == "first part":
                        prefix = "first part "
                    elif sub_part:
                        prefix = f"sub-part {sub_part} "
                    else:
                        prefix = ""
                    what = prefix + issue.what
                    problems.append(make_problem(issue.level, issue.check_id, record_file, record, name, what,
                                                 issue.fix, line.line_number))
                blocking = any(issue.check_id in ("FORM-04", "FORM-12", "FORM-02") for _, issue in issues)
                if not blocking and (tidied != line.value or name != line.name or line.tidy_notes):
                    plan.append((record, line, name, tidied))
    context.cache[key] = (problems, plan)
    return problems, plan


def apply_tidy_fixes(record_files, context):
    """Make the FORM-13 tidy fixes in the records (field names, known spellings, spacing, case, headings).

    Returns the FORM-13 problem lines for what was changed. Records keep their layout; only the tidied lines
    are rewritten.
    """
    problems, plan = analyse(record_files, context)
    for record, line, name, value in plan:
        if name is None:
            if line in record.body:
                record.body.remove(line)
                record.structure_changed = True
            continue
        line.name = name
        line.written_name = name
        line.value = value
        line.tidy_notes = []
        line.changed = True
    for record_file in record_files:
        for record in record_file.records:
            if record.heading_tidy_notes:
                record.heading_changed = True
                record.heading_tidy_notes = []
        for end_line in record_file.end_lines:
            if not end_line.strict and end_line.count >= 0:
                end_line.changed = True
    context.cache.clear()
    return [problem for problem in problems if problem.check_id == "FORM-13"]


# ---------------------------------------------------------------- FORM-01 to FORM-13

def check_form_01(record_files, context):
    """FORM-01 Unknown record type (G2, G13): a ### heading whose TYPE is not in schema.json."""
    problems = []
    type_names = list(context.schema.record_types)
    for record_file in record_files:
        for record in record_file.records:
            if record.known_type:
                continue
            heading = (record.heading_raw or "").strip()
            written = record.written_type or "(nothing)"
            second = record.written_identifier or ""
            looks_like_record = bool(re.search(r"[A-Z0-9]", second)) and (second.upper() == second)
            match = closest(written.upper(), type_names, count=1) if looks_like_record else []
            if match:
                fix = f"Did you mean {match[0]}?"
            else:
                fix = ("Fix: a free-text heading uses # or ## only (G13); a record heading names a record type, "
                       "as ### SHOT SC10-SH150")
            if written.startswith("#"):
                what = "starts with more than three #, so it is read as a record heading with no record type"
            else:
                what = f"names {written}, which is not a record type"
            problems.append(Problem("E", "FORM-01", quote_for_message(heading), None, what, fix,
                                    file_name=record_file.name, line_number=record.heading_line_number))
    return problems


def check_form_02(record_files, context):
    """FORM-02 ID does not match its type's pattern (5.3), for record headings and for IDs items declare."""
    problems = []
    schema = context.schema
    for record_file in record_files:
        for record in record_file.records:
            if not record.known_type or schema.is_singleton(record.type_name):
                continue
            syntax, example = schema.id_syntax(record.type_name)
            if not record.identifier:
                problems.append(Problem("E", "FORM-02", record.type_name, None, "has no ID",
                                        f"Fix: write ### {record.type_name} <ID>, the ID being {syntax} (for example {example})",
                                        file_name=record_file.name, line_number=record.heading_line_number))
                continue
            pattern = schema.id_pattern(record.type_name)
            if pattern and not pattern.fullmatch(record.identifier):
                problems.append(Problem("E", "FORM-02", record.identifier, None,
                                        f"is not a valid {record.type_name} ID",
                                        f"Fix: write {syntax} (for example {example})",
                                        file_name=record_file.name, line_number=record.heading_line_number))
    analysis, _ = analyse(record_files, context)
    problems.extend(problem for problem in analysis if problem.check_id == "FORM-02")
    return problems


def check_form_03(record_files, context):
    """FORM-03 Unknown field for this type, with 'did you mean'; also a list line inside a record that is not a field line."""
    analysis, _ = analyse(record_files, context)
    problems = [problem for problem in analysis if problem.check_id == "FORM-03"]
    for record_file in record_files:
        for record in record_file.records:
            for line in record.loose_lines:
                if re.match(r"^\s*[-*\u2022]\s*\S", line.raw) and not line.raw.strip().startswith("//"):
                    problems.append(make_problem("E", "FORM-03", record_file, record, None,
                                                 f"has the line {quote_for_message(line.raw.strip())}, which is not a field line",
                                                 "Fix: write - <field>: <value>, one field per line (G4)",
                                                 line.line_number))
    return problems


def check_form_04(record_files, context):
    """FORM-04 Value not allowed for the field's kind or list, with 'did you mean'. From step 5 on (and at --all), a
    FACT element may no longer be a story point: step 4's things unit re-points it to IDs (C23)."""
    analysis, _ = analyse(record_files, context)
    problems = [problem for problem in analysis if problem.check_id == "FORM-04"]
    step_rank = context.schema.step_rank(context.step) if context.step is not None else None
    if not context.written_by_ai and (step_rank is None or step_rank >= 5):
        for record_file in record_files:
            for record in record_file.records:
                if record.type_name != "FACT":
                    continue
                for line in record.field_lines("element"):
                    points = [piece for piece in split_list(line.value) if parse_story_point(piece)]
                    if points:
                        problems.append(make_problem(
                            "E", "FORM-04", record_file, record, "element",
                            f"still names a story point ({quote_for_message(points[0], 50)}) after step 5 of 12 "
                            "designed the things", "Fix: write the IDs of the things, places or people that would give "
                            "the fact away (step 5 of 12's things unit re-points these)", line.line_number))
    return problems


def step_in_words(step):
    """filled_by_step for a problem line: 'step 8', 'checkpoint B', 'add-on C'."""
    text = str(step)
    if text.isdigit():
        return f"step {text}"
    if text.startswith("add_on_"):
        return f"add-on {text[len('add_on_'):]}"
    return f"checkpoint {text}"


def field_is_required(record, definition, context, record_type):
    """(required, reason) for one field of one record at the context's depth and step (FORM-05)."""
    schema = context.schema
    conditions = context.conditions
    if definition.get("stored") is False:
        return False, ""
    writers = schema.writers(definition)
    if writers and all(writer == "code_derived" for writer in writers):
        return False, ""
    writer = conditions.writer_for(definition, record)
    if writer == "code_derived":
        return False, ""
    depth = definition.get("depth", "o")
    for entry in definition.get("depth_when", []) or []:
        if conditions.holds(entry["when"], record) is True:
            depth = entry["depth"]
    rank = conditions.depth_rank_for(record)
    if depth == "o":
        return False, ""
    if depth == "m":
        module = definition.get("module") or record_type.get("module") or ""
        if not any(letter in (context.modules or set()) for letter in module if letter.isalpha() and letter.isupper()):
            return False, ""
        depth_text = "when its add-on is on"
    else:
        if DEPTH_RANK.get(depth, 9) > rank:
            return False, ""
        depth_text = f"at {DEPTH_WORD.get(depth, depth)} depth"
    step_text = ""
    if context.step is not None:
        field_step = schema.step_rank(definition.get("filled_by_step", 0))
        if field_step is None or field_step > schema.step_rank(context.step):
            return False, ""
        step_text = " by " + step_in_words(definition.get("filled_by_step"))
    condition = definition.get("required_when")
    if condition:
        for_all = definition.get("required_for_all_at")
        if not (for_all and rank >= DEPTH_RANK.get(for_all, 9)):
            if conditions.holds(condition, record) is not True:
                return False, ""
    partner = definition.get("one_of")
    if partner and record.has(partner):
        return False, ""
    return True, f"required {depth_text}{step_text}"


def is_previs_stub(key, record):
    """True for a grey preview job code made as a stub at step 8 (PREVIS with status planned)."""
    return key[0] == "PREVIS" and normalise_word(record.get("status") or "") == "planned"


# The only fields of a grey preview stub: code writes them when it makes the stub (derive_fields.create_previs_stubs).
PREVIS_STUB_FIELDS = ("for", "level", "status", "locked")
# Fields FORM-05 never asks the AI for, because the AI never writes them: PREVIS approved is written by code
# (auto, or no until the checks pass) or by the user's answer at the grey previews checkpoint (schema writer_when).
NEVER_ASKED_OF_THE_AI = {("PREVIS", "approved")}
# Code fields FORM-05 never asks for, because another check judges them when they matter: the date of the video
# models' prices is written by the estimate from the shots (step 10) and judged by GEN-11 when prompts are made.
JUDGED_ELSEWHERE = {("PROJECT", "model_facts_date")}
SEQUENCE_OR_SCENE_RANGE = re.compile(r"^(SC\d{2,3}[A-Z]?)\.\.(SC\d{2,3}[A-Z]?)$")


def scenes_with_group_passed(context):
    """The scenes whose group of shots has passed (checkpoint C): named in the manifest's checkpoints
    (CHECKPOINT-C-<group or scene>), or with a written SHOT (step 8 starts only after its group passed)."""
    if "groups_passed" in context.cache:
        return context.cache["groups_passed"]
    passed = set()
    index = context.index or {}
    for key in index:
        if key[0] == "SHOT" and key[1]:
            match = SCENE_PREFIX.match(key[1])
            if match:
                passed.add(match.group(1))
    scenes = sorted((key[1] for key in index if key[0] == "SCENE" and key[1]), key=scene_sort_key)
    for name in (context.checkpoints or {}):
        if not str(name).startswith("CHECKPOINT-C-"):
            continue
        scope = str(name)[len("CHECKPOINT-C-"):]
        sequence = index.get(("SEQUENCE", scope))
        pieces = split_list(sequence.get("scenes") or "") if sequence is not None else [scope]
        for piece in pieces:
            match = SEQUENCE_OR_SCENE_RANGE.match(piece.strip())
            if match:
                low, high = scene_sort_key(match.group(1)), scene_sort_key(match.group(2))
                passed.update(scene for scene in scenes if low <= scene_sort_key(scene) <= high)
            elif piece.strip():
                passed.add(piece.strip())
    context.cache["groups_passed"] = passed
    return passed


def scene_sort_key(identifier):
    match = re.match(r"^SC(\d+)([A-Z]?)$", identifier or "")
    return (int(match.group(1)), match.group(2)) if match else (10 ** 6, identifier or "")


def checkpoint_not_yet_answered(definition, context):
    """True for a field the user's answers at a checkpoint fill (filled_by_step a checkpoint letter, such as B for
    the big choices) while that checkpoint's choices are not all answered or defaulted yet: it is not yet due."""
    letter = str(definition.get("filled_by_step", "")).strip()
    if not (len(letter) == 1 and letter.isalpha()):
        return False
    choices = [record for key, record in (context.index or {}).items() if key[0] == "CHOICE"
               and normalise_word(record.get("checkpoint") or "") == letter.lower()]
    return not choices or any(normalise_word(record.get("status") or "open") == "open" for record in choices)


def approval_not_yet_due(record, name, context):
    """SHOTLIST approved is code's mark that the user passed the scene's group of shots (checkpoint C). Until the
    group passes it is not yet due: FORM-05 never asks for it (in a chat without code the AI writes it, so it is
    asked as any field is)."""
    if record.type_name != "SHOTLIST" or name != "approved":
        return False
    if normalise_word(context.code_execution or "") == "no":
        return False
    scene = SCENE_PREFIX.match(record.identifier or "")
    return scene is not None and scene.group(1) not in scenes_with_group_passed(context)


def check_form_05(record_files, context):
    """FORM-05 Required field missing at the project's (or the scene's) depth, among fields filled by the step checked."""
    problems = []
    schema = context.schema
    merged, _ = merge_copies(record_files, schema)
    locations = {}
    for record_file in record_files:
        for record in record_file.records:
            locations.setdefault(record.key, (record_file, record))
    for key, record in merged.items():
        record_type = schema.record_types.get(key[0])
        if record_type is None:
            continue
        status = record.get("status")
        if status and normalise_word(status) == "omitted":
            continue
        record_file, first_copy = locations[key]
        fields = schema.field_map(key[0])
        if key[0] == "SETVALUE":
            fields = {"target": fields["target"]}
        stub = is_previs_stub(key, record)
        for name, definition in fields.items():
            if (key[0], name) in NEVER_ASKED_OF_THE_AI or (key[0], name) in JUDGED_ELSEWHERE or \
                    (stub and name not in PREVIS_STUB_FIELDS) or approval_not_yet_due(record, name, context):
                continue
            if context.conditions.writer_for(definition, record) == "user" and \
                    checkpoint_not_yet_answered(definition, context):
                continue
            required, reason = field_is_required(record, definition, context, record_type)
            if not required:
                continue
            if not record.field_lines(name) or all(line.missing for line in record.field_lines(name)):
                writer = context.conditions.writer_for(definition, record)
                if writer in ("code_state", "story"):
                    source = CODE_FIELD_SOURCES.get((key[0], name))
                    if source and not record.has(source):
                        continue  # code fills it from a field the AI writes, which FORM-05 asks for itself
                    problems.append(make_problem("E", "FORM-05", record_file, first_copy, name,
                                                 f"is missing ({reason})", code_field_fix(key[0], name)))
                    continue
                problems.append(make_problem("E", "FORM-05", record_file, first_copy, name, f"is missing ({reason})",
                                             user_field_fix(definition) if writer == "user" else
                                             missing_field_fix(name, definition)))
                continue
            if definition.get("kind") == "sub_parts":
                problems.extend(missing_sub_parts(record, name, definition, context, record_file, first_copy))
    return problems


# Code fields filled from a field the AI writes: while that field is missing, FORM-05 asks only for it.
CODE_FIELD_SOURCES = {("TEXT", "words"): "words_from"}


def code_field_fix(type_name, name):
    """The fix for a missing field that code keeps: the AI writes nothing; it says what code fills it from."""
    if (type_name, name) == ("SHOTLIST", "approved"):
        return ("Fix: nothing for the AI to write; code sets it when the group of shots passes: run stage.py next "
                "(after the user's \"next\" on a group that waits, stage.py next --checkpoint-passed)")
    try:
        from .fill_code_fields import FILL_COMMAND_WORDS, code_fill_path
    except ImportError:
        return "Fix: nothing for the AI to write; code fills it (stage.py build)"
    path = code_fill_path(type_name, name)
    how = f" ({path[2]})" if path else ""
    return f"Fix: nothing for the AI to write; {FILL_COMMAND_WORDS}{how}"


def user_field_fix(definition):
    """The fix for a missing field only the user's answer writes (apply refuses it from the AI, FORM-10)."""
    letter = str(definition.get("filled_by_step", "")).strip()
    where = (f"the user's answer at checkpoint {letter.upper()}" if len(letter) == 1 and letter.isalpha()
             else "the user's answer to a small choice")
    return (f"Fix: this is the user's field: never type it; it is written when {where} is applied (write or answer "
            "the CHOICE that sets it)")


def missing_field_fix(name, definition):
    """The fix for a missing field: the schema's own fix when it has one, a short example when the schema's example
    is short, else the field's label."""
    if definition.get("missing_fix"):
        return "Fix: " + definition["missing_fix"]
    example = str(definition.get("example", "")).strip()
    if example and len(example) <= 40 and "\n" not in example:
        return f'Fix: add a line such as "- {name}: {example}"'
    label = definition.get("label") or name
    if definition.get("repeat") or "none" in [str(value) for value in (definition.get("also_allowed") or [])]:
        return f'Fix: add "- {name}: <{label.lower()}>", or "- {name}: none" when there is nothing (reference/03 Field guide)'
    return f'Fix: add "- {name}: <{label.lower()}>" (reference/03 Field guide shows its form)'


def missing_sub_parts(record, name, definition, context, record_file, first_copy):
    """FORM-05 for sub-parts that carry their own depth (SHOT subject: at, faces, does, tactic ...)."""
    problems = []
    parts_with_depth = [entry for entry in definition.get("sub_parts") or [] if entry.get("depth")]
    if not parts_with_depth:
        return problems
    rank = context.conditions.depth_rank_for(record)
    for value in record.get_all(name):
        if value.strip().lower() in ("none", "open"):
            continue
        item = split_item(value, definition)
        for entry in parts_with_depth:
            if DEPTH_RANK.get(entry["depth"], 9) > rank:
                continue
            if entry.get("required_when") and context.conditions.holds(entry["required_when"], record, item) is not True:
                continue
            if entry.get("required_when_not") and context.conditions.holds(entry["required_when_not"], record, item) is True:
                continue
            if item.get(entry["key"]) is None:
                problems.append(make_problem("E", "FORM-05", record_file, first_copy, name,
                                             f"item {item.first or value[:20]} has no sub-part {entry['key']} "
                                             f"(required at {DEPTH_WORD.get(entry['depth'], entry['depth'])} depth)",
                                             f'Fix: add "| {entry["key"]}: <value>" to the item'))
    return problems


def check_form_06(record_files, context):
    """FORM-06 END line missing (G9): a cut-off reply. Also a malformed END line, several END lines, or text after it."""
    problems = []
    for record_file in record_files:
        ends = record_file.end_lines
        if not ends:
            records = record_file.records
            if records:
                last = records[-1]
                what = (f"END line missing: the reply may have been cut off; the last record, {last.label}, "
                        "may be incomplete")
                fix = (f"Fix: re-send from the start of {last.label} (### {last.type_name}"
                       f"{' ' + last.identifier if last.identifier else ''}) and end the file with "
                       '"END OF FILE | <what the file holds> | <n> records"')
            else:
                what = "END line missing: the file has no records and no END line"
                fix = 'Fix: end the file with "END OF FILE | <what the file holds> | <n> records"'
            problems.append(Problem("E", "FORM-06", quote_for_message(record_file.name), None, what, fix,
                                    file_name=record_file.name))
            continue
        for end_line in ends:
            if end_line.count < 0:
                problems.append(Problem("E", "FORM-06", quote_for_message(record_file.name), None,
                                        f"END line {quote_for_message(end_line.raw.strip())} has no record count",
                                        'Fix: write "END OF FILE | <what the file holds> | <n> records"',
                                        file_name=record_file.name, line_number=end_line.line_number))
        if len(ends) > 1:
            problems.append(Problem("E", "FORM-06", quote_for_message(record_file.name), None,
                                    f"has {len(ends)} END lines; a file ends with exactly one",
                                    "Fix: save each reply as its own file, or keep only the last END line with the total count",
                                    file_name=record_file.name, line_number=ends[1].line_number))
        else:
            after = record_file.lines_after_end()
            if after:
                problems.append(Problem("E", "FORM-06", quote_for_message(record_file.name), None,
                                        f"has {len(after)} line(s) after its END line, starting {quote_for_message(after[0][1].strip())}",
                                        "Fix: the END line is the file's last line; move the records above it and recount",
                                        file_name=record_file.name, line_number=after[0][0]))
    return problems


def check_form_07(record_files, context):
    """FORM-07 END count differs from the records in the file (G9): a dropped record."""
    problems = []
    for record_file in record_files:
        ends = record_file.end_lines
        if len(ends) != 1 or ends[0].count < 0:
            continue
        actual = len(record_file.records)
        if actual != ends[0].count:
            problems.append(Problem("E", "FORM-07", quote_for_message(record_file.name), None,
                                    f"END line counts {ends[0].count} records but the file holds {actual}",
                                    "Fix: send any record that was dropped, or correct the count to the ### records in the file",
                                    file_name=record_file.name, line_number=ends[0].line_number))
    return problems


def shortening_markers(words):
    table = (words or {}).get("shortening_markers", {})
    markers = table.get("markers") or ["...", "\u2026", "etc.", "and so on", "same as above", "as before",
                                       "remaining shots", "omitted for brevity"]
    starts = table.get("line_starts") or ["//"]
    return markers, starts


def remove_quoted(value):
    """The value with every double-quoted part removed (G11: markers inside story quotes are allowed)."""
    return re.sub(r'["\u201c][^"\u201c\u201d]*["\u201d]', '""', value)


# Markers that are also ordinary English inside a sentence ("the sound goes on as before"): they mark a shortening
# only when they stand for the value: at its start ("As before, the lamp on its hook."), in a value of at most this
# many words, or in a clause that points back to an earlier record ("the same framing, lens and light as before").
MARKERS_ALSO_ENGLISH = {"as before"}
MARKER_VALUE_WORDS_MAX = 5
POINTING_BACK_WORDS = {"same", "identical", "unchanged", "previous", "earlier", "above"}


def marker_clause_points_back(lowered, start):
    """True when the sentence part holding a marker (after the last ; . : or dash) holds a word that points back."""
    before = re.split(r"[;.:\u2014]|\s-\s", lowered[:start])[-1]
    return bool(set(re.findall(r"[a-z]+", before)) & POINTING_BACK_WORDS)


def find_marker(text, markers):
    lowered = text.lower()
    for marker in markers:
        if marker[0].isalpha():
            found = re.search(r"(?<![a-z])" + re.escape(marker.lower()) + r"(?![a-z])", lowered)
            if found:
                if marker.lower() in MARKERS_ALSO_ENGLISH and lowered[:found.start()].strip(" \t\"'(") and \
                        len(re.findall(r"[a-z']+", lowered)) > MARKER_VALUE_WORDS_MAX and \
                        not marker_clause_points_back(lowered, found.start()):
                    continue
                return marker
        elif marker in text:
            return marker
    return None


def written_by_code(context, record, field_name):
    """True when code wrote this field of this record (writer story or code_state): FORM-08 does not judge code's
    own text, which the AI may not change (FORM-10). A chat project's chat_writer ai fields are the AI's."""
    definition, _, how = resolve_field(context.schema, context.words, record, field_name)
    if definition is None or how is None:
        return False
    if definition.get("chat_writer") == "ai" and normalise_word(context.code_execution or "") == "no":
        return False
    return context.conditions.writer_for(definition, record) in ("story", "code_state")


def check_form_08(record_files, context):
    """FORM-08 Shortening marker inside a record (G11), unless inside double quotes, or in a field code wrote."""
    problems = []
    markers, starts = shortening_markers(context.words)
    for record_file in record_files:
        for record in record_file.records:
            for line in record.body:
                raw = line.raw if line.raw is not None else ""
                if isinstance(line, FieldLine):
                    if not context.written_by_ai and written_by_code(context, record, line.name):
                        continue
                    if raw.strip().startswith(tuple(starts)):
                        marker = raw.strip()[:2]
                    else:
                        marker = find_marker(remove_quoted(line.value), markers)
                        if marker is None and line.value.strip().startswith(tuple(starts)):
                            marker = line.value.strip()[:2]
                    if marker:
                        problems.append(make_problem("E", "FORM-08", record_file, record, line.name,
                                                     f'has the shortening marker "{marker}"',
                                                     "Fix: write the whole value; if the reply is getting long, stop "
                                                     "after a whole record and continue in the next batch",
                                                     line.line_number))
                elif line.kind == "loose":
                    stripped = raw.strip()
                    marker = stripped[:2] if stripped.startswith(tuple(starts)) else find_marker(remove_quoted(stripped), markers)
                    if marker:
                        problems.append(make_problem("E", "FORM-08", record_file, record, None,
                                                     f'has the shortening marker "{marker}" in the line {quote_for_message(stripped)}',
                                                     "Fix: write every record and field in full (G11)",
                                                     line.line_number))
    return problems


def check_form_09(record_files, context):
    """FORM-09 Same field with two different values across merged copies (G10), or twice in one record."""
    problems = []
    _, conflicts = merge_copies(record_files, context.schema)
    first_copy = {}
    for record_file in record_files:
        for record in record_file.records:
            first_copy.setdefault(record.key, (record_file, record))
    for conflict in conflicts:
        if len({copy_index for copy_index in conflict.copy_indexes}) < 2:
            continue
        record_file, record = first_copy[(conflict.type_name, conflict.identifier)]
        shown = []
        for value, file_name, line_number in conflict.values[:3]:
            shown.append(f"{quote_for_message(value, 40)} ({file_name}, line {line_number})")
        problems.append(make_problem("E", "FORM-09", record_file, record, conflict.field_name,
                                     "has different values in copies of this record: " + " and ".join(shown),
                                     "Fix: keep one value; copies of a record in several files must agree (G10)"))
    analyse(record_files, context)

    def tidied(line, definition):
        return value_for_comparison(context.cache.get(("tidied", id(line)), line.value), definition)

    for record_file in record_files:
        for record in record_file.records:
            if not record.known_type:
                continue
            seen = {}
            for line in record.fields:
                definition, name, _ = resolve_field(context.schema, context.words, record, line.name)
                if definition is None or definition.get("repeat") or line.missing:
                    continue
                if name in seen and tidied(seen[name], definition) != tidied(line, definition):
                    problems.append(make_problem("E", "FORM-09", record_file, record, name,
                                                 f"is written twice with different values: {quote_for_message(seen[name].value, 40)} "
                                                 f"(line {seen[name].line_number}) and {quote_for_message(line.value, 40)}",
                                                 "Fix: keep one line; this field takes one value", line.line_number))
                seen.setdefault(name, line)
    return problems


class ChoiceBook:
    """Which fields answered or defaulted choices set, for FORM-10's user fields and FORM-11's unlocks."""

    def __init__(self, records):
        self.choices = {}
        self.set_values = {}
        for record in records:
            if record.type_name == "CHOICE" and record.identifier:
                self.choices[record.identifier] = record
            elif record.type_name == "SETVALUE" and record.identifier:
                self.set_values[record.identifier] = record

    def status(self, choice):
        status = choice.get("status")
        return normalise_word(status) if status else None

    def chosen_letter(self, choice):
        """The option letter an answered or defaulted choice took, or None (free-text answer, open)."""
        status = self.status(choice)
        if status not in ANSWERED:
            return None
        answer = (choice.get("answer") or "").strip().lower()
        if re.fullmatch(r"[a-z]", answer):
            return answer
        if status == "defaulted":
            default = choice.get("default")
            if default:
                letter = split_item(default).first.strip().lower()
                if re.fullmatch(r"[a-z]", letter):
                    return letter
        return None

    def backing(self, record, field_name, schema):
        """(found, values): whether an answered or defaulted choice sets this field, and the values it sets."""
        paths = set()
        if record.identifier:
            paths.add(f"{record.identifier}.{field_name}")
        if record.type_name == "PROJECT" or schema.is_singleton(record.type_name):
            paths.add(f"{record.type_name}.{field_name}")
        definition = schema.field(record.type_name, field_name) or {}
        found = False
        values = []
        by_choice = definition.get("set_by_choice")
        if by_choice and by_choice in self.choices and self.status(self.choices[by_choice]) in ANSWERED:
            found = True
            letter = self.chosen_letter(self.choices[by_choice])
            for item_text in self.choices[by_choice].get_all("sets"):
                item = split_item(item_text)
                if item.first.strip() in paths and item.get("when") == letter and item.get("value") is not None:
                    values.append(item.get("value"))
        for identifier, choice in self.choices.items():
            if self.status(choice) not in ANSWERED:
                continue
            letter = self.chosen_letter(choice)
            for item_text in choice.get_all("sets"):
                item = split_item(item_text)
                first = item.first.strip()
                if first in paths:
                    found = True
                    if item.get("when") in (None, letter) and item.get("value") is not None:
                        values.append(item.get("value"))
                elif first in self.set_values:
                    set_value = self.set_values[first]
                    target = (set_value.get("target") or "").strip()
                    if target in (record.identifier, record.type_name) and set_value.field_lines(field_name):
                        found = True
                        if first.endswith("-" + (letter or "?").upper()):
                            values.extend(set_value.get_all(field_name))
            affects = choice.get("affects") or ""
            if any(path in [part.strip() for part in split_list(affects)] for path in paths):
                found = True
        for identifier, set_value in self.set_values.items():
            choice_identifier = identifier.rsplit("-", 1)[0]
            choice = self.choices.get(choice_identifier)
            if choice is None or self.status(choice) not in ANSWERED:
                continue
            target = (set_value.get("target") or "").strip()
            if target in (record.identifier, record.type_name) and set_value.field_lines(field_name):
                found = True
                letter = self.chosen_letter(choice)
                if letter and identifier.endswith("-" + letter.upper()):
                    values.extend(set_value.get_all(field_name))
        return found, values


def same_value(first, second):
    """Two values are the same when they differ only in spacing, case, or spaces and hyphens read as underscores."""
    return normalise_word(value_for_comparison(first)) == normalise_word(value_for_comparison(second))


def incoming_view(merged, incoming):
    """The record as it will be once an inbox copy is merged: the inbox's fields replace the stored ones they name."""
    if merged is incoming or merged is None:
        return incoming
    from .record_format import Record
    view = Record(type_name=incoming.type_name, identifier=incoming.identifier, title=incoming.title or merged.title,
                  known_type=True)
    named = {line.name for line in incoming.fields if not line.missing}
    view.body.extend(line for line in merged.fields if line.name not in named)
    view.body.extend(line for line in incoming.fields if not line.missing)
    return view


def check_form_10(record_files, context):
    """FORM-10 Wrong writer (5.2): a code_derived field typed (W, dropped); a code_state or story field changed by
    the AI (E), except a chat_writer ai field when code_execution is no; a user field set without an answered or
    defaulted CHOICE (E)."""
    problems = []
    schema = context.schema
    conditions = context.conditions
    all_records = list((context.index or {}).values())
    for record_file in record_files:
        all_records.extend(record_file.records)
    book = ChoiceBook(all_records)
    current = context.current_records or {}
    for record_file in record_files:
        for record in record_file.records:
            if not record.known_type:
                continue
            merged = (context.index or {}).get(record.key, record)
            if context.written_by_ai:
                # the writer of a conditional field follows what the inbox itself says (origin: inferred on a text
                # that was origin: story makes its words the AI's), not the stored copy it replaces
                merged = incoming_view(merged, record)
            stored = current.get(record.key)
            for line in record.fields:
                definition, name, _ = resolve_field(schema, context.words, record, line.name)
                if definition is None or line.missing:
                    continue
                if record.type_name == "SETVALUE" and name != "target":
                    continue
                if definition.get("stored") is False or definition.get("writer") == "code_derived":
                    problems.append(make_problem("W", "FORM-10", record_file, record, name,
                                                 "is worked out by code and never stored; the typed value is dropped",
                                                 "Fix: leave this field out; stage.py build computes it", line.line_number))
                    continue
                writer = conditions.writer_for(definition, merged)
                if writer == "code_derived":
                    problems.append(make_problem("W", "FORM-10", record_file, record, name,
                                                 "is worked out by code at this depth; the typed value is dropped",
                                                 "Fix: leave this field out", line.line_number))
                    continue
                if context.written_by_ai and writer in ("code_state", "story"):
                    stored_values = stored.get_all(name) if stored is not None else []
                    if stored_values and any(same_value(line.value, value) for value in stored_values):
                        continue
                    if stored is None and name in CODE_DEFAULTS and normalise_word(line.value) in CODE_DEFAULTS[name]:
                        continue
                    if definition.get("chat_writer") == "ai" and normalise_word(context.code_execution or "") == "no":
                        continue
                    who = "code copies it from the story" if writer == "story" else "code keeps it"
                    problems.append(make_problem("E", "FORM-10", record_file, record, name,
                                                 f"is written by code ({writer}); the AI may not change it",
                                                 f"Fix: remove the line; {who}", line.line_number))
                    continue
                if context.written_by_ai and definition.get("kind") in ("story_point", "story_point_list", "scene_or_story_point"):
                    for part in split_list(line.value):
                        point = parse_story_point(part)
                        if point and point[2]:
                            stored_values = stored.get_all(name) if stored is not None else []
                            if not any(part in split_list(value) for value in stored_values):
                                problems.append(make_problem("E", "FORM-10", record_file, record, name,
                                                             f"types the resolved beat after = in {quote_for_message(part)}; code writes that ending",
                                                             "Fix: write the scene ID and the quote only", line.line_number))
                if writer == "user" and context.written_by_ai and record.type_name not in ("CHOICE", "SETVALUE") \
                        and normalise_word(context.code_execution or "") != "no":
                    # C6: on a code surface the user's fields come only through a CHOICE (its sets lines) or a
                    # SETVALUE, which apply writes when the choice is answered or defaulted; the AI may repeat the
                    # stored value, or write open where nothing is decided yet, and nothing else. In a chat without
                    # code nobody applies the choice, so there the AI writes what the answered choice sets.
                    stored_values = [value for value in (stored.get_all(name) if stored is not None else [])
                                     if normalise_word(value) != "open"]
                    if stored_values and any(same_value(line.value, value) for value in stored_values):
                        continue
                    if normalise_word(line.value) == "open" and not stored_values:
                        continue
                    if normalise_word(line.value) == "open":
                        what = "is the user's decision, already made; writing open would erase it"
                    else:
                        what = "is the user's to decide; the AI may not write it"
                    problems.append(make_problem("E", "FORM-10", record_file, record, name, what,
                                                 "Fix: remove the line; the answer to a choice (its sets line or a "
                                                 "SETVALUE record) writes this field", line.line_number))
                    continue
                if writer == "user":
                    if normalise_word(line.value) == "open":
                        continue
                    if record.type_name == "CHOICE" and name == "answer":
                        if context.written_by_ai or book.status(merged) in ANSWERED or book.status(record) in ANSWERED:
                            continue
                        problems.append(make_problem("E", "FORM-10", record_file, record, name,
                                                     "holds an answer but the choice is still open",
                                                     "Fix: write open until the user answers", line.line_number))
                        continue
                    found, values = book.backing(merged, name, schema)
                    if not found:
                        problems.append(make_problem("E", "FORM-10", record_file, record, name,
                                                     "is the user's to decide, and no answered or defaulted choice sets it",
                                                     "Fix: write open and ask through a choice (or a small choice with a default)",
                                                     line.line_number))
                    elif values and not any(same_value(line.value, value) for value in values):
                        problems.append(make_problem("E", "FORM-10", record_file, record, name,
                                                     f"is {quote_for_message(line.value, 40)}, which differs from what the answered choice sets "
                                                     f"({quote_for_message(values[0], 40)})",
                                                     "Fix: write the value the choice sets, or ask the user again", line.line_number))
    return problems


def locked(record):
    value = record.get("locked") if record is not None else None
    return value is not None and normalise_word(value) == "yes"


def check_form_11(record_files, context):
    """FORM-11 Locked record changed (5.4 rule 5): a locked record may gain fields, but an existing value changes
    only when an answered or defaulted choice sets that value."""
    problems = []
    schema = context.schema
    current = context.current_records or {}
    all_records = list((context.index or {}).values())
    book = ChoiceBook(all_records + [record for record_file in record_files for record in record_file.records])
    for record_file in record_files:
        for record in record_file.records:
            stored = current.get(record.key)
            if not record.known_type or not locked(stored):
                continue
            for name in record.field_names():
                definition, target, _ = resolve_field(schema, context.words, record, name)
                if definition is None or name in ("status", "locked"):
                    continue
                writers = schema.writers(definition)
                if writers and all(writer in ("code_state", "code_derived") for writer in writers):
                    continue
                new_values = record.get_all(name)
                old_values = stored.get_all(target)
                if not old_values or not new_values:
                    continue
                if definition.get("repeat"):
                    old_set = {value_for_comparison(value) for value in old_values}
                    new_set = {value_for_comparison(value) for value in new_values}
                    if old_set == new_set or (target == "note" and old_set <= new_set):
                        continue
                elif same_value(new_values[0], old_values[0]):
                    continue
                found, values = book.backing(stored, target, schema)
                if found and values and all(any(same_value(new, value) for value in values) for new in new_values):
                    continue
                line = record.field_lines(name)[0]
                problems.append(make_problem("E", "FORM-11", record_file, record, target,
                                             f"changes a locked record (it was {quote_for_message(old_values[0], 40)})",
                                             "Fix: keep the locked value; changing it needs a choice the user answers, "
                                             "which unlocks it", line.line_number))
    return problems


def check_form_12(record_files, context):
    """FORM-12 Unknown sub-part key, positional (unnamed) sub-part, or " | " inside text (G6)."""
    analysis, _ = analyse(record_files, context)
    return [problem for problem in analysis if problem.check_id == "FORM-12"]


def check_form_13(record_files, context):
    """FORM-13 Tidy fixes (N): case, spacing, field-name and value synonyms from words.json, a tolerant END line."""
    analysis, _ = analyse(record_files, context)
    problems = [problem for problem in analysis if problem.check_id == "FORM-13"]
    for record_file in record_files:
        for end_line in record_file.end_lines:
            if not end_line.strict and end_line.count >= 0:
                problems.append(Problem("N", "FORM-13", quote_for_message(record_file.name), None,
                                        f"END line {quote_for_message(end_line.raw.strip())} read as "
                                        f'"END OF FILE | {end_line.what} | {end_line.count} records"',
                                        file_name=record_file.name, line_number=end_line.line_number))
    return problems


FORM_CHECKS = {
    "FORM-01": check_form_01,
    "FORM-02": check_form_02,
    "FORM-03": check_form_03,
    "FORM-04": check_form_04,
    "FORM-05": check_form_05,
    "FORM-06": check_form_06,
    "FORM-07": check_form_07,
    "FORM-08": check_form_08,
    "FORM-09": check_form_09,
    "FORM-10": check_form_10,
    "FORM-11": check_form_11,
    "FORM-12": check_form_12,
    "FORM-13": check_form_13,
}

# The checks that make sense on an inbox file the AI wrote (apply), before it is merged: FORM-05 runs on the
# merged project instead (check), because an inbox holds only one unit's fields.
INBOX_CHECKS = ["FORM-01", "FORM-02", "FORM-03", "FORM-04", "FORM-06", "FORM-07", "FORM-08", "FORM-09",
                "FORM-10", "FORM-11", "FORM-12", "FORM-13"]


def run_form_checks(record_files, context, check_ids=None):
    """Run the named FORM checks (all thirteen by default) and return their problem lines: in check order, and
    within one check in file order, then line order."""
    file_order = {record_file.name: index for index, record_file in enumerate(record_files)}
    problems = []
    for check_id in (check_ids or list(FORM_CHECKS)):
        found = FORM_CHECKS[check_id](record_files, context)
        found.sort(key=lambda problem: (file_order.get(getattr(problem, "file_name", None), len(file_order)),
                                        getattr(problem, "line_number", None) or 0))
        problems.extend(found)
    return problems
