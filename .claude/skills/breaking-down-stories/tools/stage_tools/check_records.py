"""check_records.py: the checker. It keeps the list of every check of blueprint section 7.2, runs the checks a
command asks for (check --step N, --scene SCnn, --film, --all, --story <path>), makes the tidy fixes and logs
them, writes the plain report "13 Health check.md" (its first line is "In short: ...") and exits as 7.3 says:
0 when no error line was printed, 1 when error lines were printed, 2 when the check could not run.

In plain words:
- every check lives in a family module and is registered here with its check ID, its level (E error, W warning,
  N note) and its build (1 in the first build, 2 later);
- run_checks runs the registered checks on a list of parsed record files and returns their problem lines, the
  checks it skipped and why, and the tidy fixes it made;
- the command check does the same on a project folder, writes the fixes back (the old files go to history),
  writes 13 Health check.md and prints the problem lines.

Standard library only.


HOW A FAMILY MODULE REGISTERS ITS CHECKS (for the builders of the other check families)
======================================================================================

1. Write the module in stage_tools/ under the name listed below, and add nothing anywhere else:
   CHECK_FAMILY_MODULES (below the imports) already lists every planned family module, and a module that is
   not there yet is skipped (its checks are reported as "not in this copy of the tools yet"). check_records
   imports each module when stage.py starts (and when run_checks runs), so importing it registers its checks.
   A family module that fails to import is reported as "Could not load ..." and every other family still runs.

       stage_tools.checks_form                  FORM-01 to FORM-13 (WP2; registered here by an adapter)
       stage_tools.checks_ids_citations         ID-01 to ID-09, CITE-01 to CITE-07 (WP4b)
       stage_tools.checks_coverage_time_state   COVER, TIME and STATE (WP4c)
       stage_tools.checks_sides_geometry        SIDE and GEOM (WP4a)
       stage_tools.checks_craft_reasons_words   CRAFT, INFO, REASON and WORDS (WP4d)
       stage_tools.checks_plan_generation_film  PLAN, GEN and FILM (WP4e)

2. In the module, register one function per check ID of 7.2 with the decorator register_check (import it with a
   relative import, so the module registers with this very registry):

       from .check_records import register_check, scene_of

       @register_check("TIME-01", level="E", build=1,
                       title="Screen time under the derived floor",
                       plain="has a shot shorter than the time its speech and pauses need")
       def check_time_01(run):
           problems = []
           for shot in run.records("SHOT"):
               ...
               problems.append(run.problem("E", "TIME-01", shot, "screen_time",
                                           "12 is under its floor 13.8 s (speech 11.8 s + pause 2.0 s)",
                                           "Fix: raise screen_time to 14 or move SC10-D12 to the next shot."))
           return problems

   - The ID is 7.2's ("FAMILY-NN"); registering an ID twice keeps the last function.
   - level is the level of 7.2 ("E", "W", "N", or "E/W" when the check can print either).
   - build is 1 or 2 (7.2's Build column). A build-2 check may be a stub that calls run.skip(...) and returns [].
   - title is 7.2's "Check" column, for maintainers.
   - plain says what is wrong in plain words for the plain part of 13 Health check. It follows a record's plain
     name ("Scene 10, shot 150: <plain>."), so it starts with a verb and never holds a code, an ID or an
     abbreviation (WORDS-04): "has a shot shorter than the time its speech and pauses need".
   - The function takes one CheckRun (below) and returns a list of record_format.Problem lines in 7.2's format
     (level, check ID, record, field, what is wrong, then the allowed values or the fix). Build each line with
     run.problem(...), which fills in the file and line of the record's first copy (pass line_number= and
     file_name= to point at one field line). A check may return plain strings too, but then the report cannot
     place them in a file or a scene.
   - When a check cannot run (no story, a scene not in the excerpt), call run.skip(check_id, "why") and return
     what it could check. A skip is not a problem line: it is listed separately ("Skipped ID: why"). Use the
     words "story not present" when the story is missing (run.story_missing does) and "not in the excerpt" for
     references outside the excerpt of the story given (the scene 10 fixture), as the tests look for them.
   - A check never changes records. Tidy fixes are made by the runner (FORM-13) before the checks run.
   - A check only reads; run.cache is a dict for sharing work between the checks of one run (for example
     derive_fields.breakdown_for_run(run) keeps its derived fields there).
   - A check that raises an exception is reported as "stopped with a fault in the tools" and the other checks
     still run, so one fault never hides every other problem.

3. What a check reads (CheckRun):

       run.schema, run.words, run.constants    schema.json (record_format.Schema), words.json, constants.json
       run.record_files                        the parsed record files (record_format.RecordFile), in file order
       run.index                               {(TYPE, ID): merged Record} over every file (G10); ID is None
                                               for singletons (PLAN, STYLE ...)
       run.records("SHOT")                     merged records of a type, in file order, omitted ones left out
                                               (include_omitted=True keeps them)
       run.record("SC10-SH150") / ("PLAN")     one merged record by ID, or a singleton or PROJECT by type
       run.copies(key)                         [(record_file, record copy)] for one (TYPE, ID)
       run.field_lines(key, "lines")           [(record_file, copy, FieldLine)] with the line numbers
       run.is_omitted(record)                  status omitted (5.4 rule 6)
       run.project_record                      the PROJECT record, or None
       run.depth, run.depth_rank(record)       the project's depth; 1 quick, 2 standard, 3 detailed, taking a
                                               scene's own deeper depth into account
       run.step                                the step checked (an int), or None for --all
       run.scene                               the scene given with --scene, or None
       run.film                                True with --film
       run.scope_scenes                        the scenes in PROJECT.scope, or None when the scope is all
       run.in_scope(ID or record)              True when it belongs to no scene or to a scene being checked
       run.scene_left_out("SC13")              True for a scene with no records here that lies outside the
                                               project's scope or the excerpt given: skip references into it
       run.scene_ids()                         the SCENE records' IDs, in file order
       run.scene_range("SC10")                 (first, last) lines of a scene: its SCENE record, else the story
       run.chapter_range("CP01")               (first, last) lines of a chapter
       run.story                               StorySource or None: .numbered (read_story.NumberedStory: line(n),
                                               find_quote, check_quote, resolve_lines, resolve_line, scenes),
                                               .speeches, .story_map (story map.json), .excerpt, .holds(a, b)
       run.story_missing("CITE-02")            True (and one skip line) when no story is present
       run.speeches                            {speech ID: speeches.json entry}, or {} when not present
       run.manifest                            the project's manifest.json, or {} (batches, issued blocks ...)
       run.batch_shots("SC10")                 during step 8: the set of listed shot IDs whose batches were
                                               written so far; None means "check every list item" (use it for
                                               ID-07 and COVER-02 to COVER-04, 7.2)
       run.form_context                        checks_form.FormContext for the same files (conditions, choices)
       run.locked_baseline                     {(TYPE, ID): Record} as the checker last saw each locked record
                                               ("For machines - do not edit/locked records.json")
       run.problem(level, check_id, record, field, what, fix="", line_number=None, file_name=None)
       run.skip(check_id, why)
       scene_of("SC10-SH150") -> "SC10"        (module function; same_scene("SC6", "SC06") is True)

   The runner removes exact duplicates, orders the lines by check (7.2's order), then file, then line, and
   leaves out the lines of records outside PROJECT.scope. With --scene it keeps only the lines of that scene's
   records and scene files; the other lines are counted ("left out") and shown by check --all.

4. Checks that must also run on an inbox before apply merges it: register them with
   project_files.register_apply_check(function(project, inbox, current_files, context)) at import time of the
   family module; the function returns Problem lines and apply refuses the whole inbox on any E line.
   check_records imports every family module when stage.py starts, so apply sees them. (checks_ids_citations
   registers ID-01, ID-04 and ID-06 this way.)

5. Other modules may add a section to the plain part of 13 Health check (quality scores, the three scenes to
   read) with register_report_section(function(project, result) -> list of plain lines, or []). The lines go
   after "Not checked this time" and before "Details by file"; start the section with a "## " heading.

6. To run checks from code (tests, adopt, replay): run_checks(record_files, schema, words, constants,
   story=StorySource.from_file(path) or StorySource.from_project(folder) or None, manifest=..., step=...,
   scene=..., film=..., check_ids=[...]) returns a CheckResult (problems, skipped, tidy_notes, checks_run,
   crashed, counts, errors).

WHAT THE CHECK COMMAND DOES
===========================
check [--step N] [--scene SCnn] [--film] [--all] [--story <path>]
- --step N runs the checks steps.json lists for step N (step 10 lists "all checks"); FORM-05 then asks only for
  fields filled by step N or earlier. --all (and no option at all) runs every registered check and asks for
  every field. --film runs the FILM checks and the rest of step 9's list. --scene keeps only the problems of that
  scene's records and scene files.
- --story <path> reads the story (or a Stage excerpt) from that file for the CITE checks, instead of the
  project's story map.json and speeches.json. Without any story the CITE checks say "skipped: story not present".
- Tidy fixes (FORM-13) are made in the record files and logged (a numbered entry in 00 Start here, a line in
  log.jsonl); the old files go to history/.
- 13 Health check.md gets a new plain part (first line "In short: ..."), its REVIEW and FINDING records are
  kept, and the checker's lines are written below the divider. --all also sets PROJECT.checker_last_run.
- manifest.json keeps the IDs of omitted records (omitted_ids, for ID-04), the last check (last_check) and fresh
  fingerprints; "For machines - do not edit/locked records.json" keeps each locked record as the checker last saw
  it (FORM-11 on stored files: a locked value changed by hand is an error on the next check).
- Exit (7.3): 0 when no error line was printed; 1 when error lines were printed (the AI fixes only those, at most
  3 rounds); 2 when the check could not run (a missing story file, a bad step or scene), with one plain line.

After the full run on The Catch (Project notes 31 and 32):
- a check that checks nothing leaves 13 Health check as it was; after a full check, a partial check keeps the plain
  part and replaces only its own lines;
- the plain part gives the quality scores in plain words and the three scenes to read, and its 'In short' line names
  the problems first;
- the check of a scene's last batch also runs the scene-wide checks.

After the three-scene test of the fixed kit (Project notes 35 and 36):
- check --unit drops what is not yet due, and says when the unit's inbox is still unapplied.

After the second three-scene test (Project notes 37 and 38):
- the scenes to read point to the guide "05 How to read your breakdown" and say where it is.
"""

import dataclasses
import datetime
import importlib
import json
import re
from dataclasses import dataclass, field as dataclass_field
from pathlib import Path

from .record_format import (DEPTH_RANK, DIVIDER_LINE, EndLine, Problem, Record, TextBlock, count_levels,
                            load_json, merge_copies, normalise_word, parse_file, parse_line_numbers,
                            parse_quote_anchor, parse_text, record_lines, render_file, sort_key_for_identifier,
                            split_item, split_list, write_file)
from .project_files import (MACHINE_FOLDER, START_HERE, Project, StageStop, history_run_folder, keep_in_history,
                            today)

HEALTH_CHECK_FILE = "13 Health check.md"
HEALTH_CHECK_TITLE = "Health check"
SCENE_PART = re.compile(r"^(SC\d{2,3}[A-Z]?)(?=-|\.|$)")
SCENE_FILE_NUMBER = re.compile(r"^11 Scenes/Scene (\d{2,3}[A-Z]?)\b")
SCENE_TYPES = ("SCENE", "PART", "BEAT", "SPEECH", "MOVE", "SETUP", "SHOTLIST", "SHOT", "CUT")
NOTE_LINES_PRINTED = 30
SKIP_LINES_PRINTED = 12
PLAIN_LINES_LISTED = 40

# Every planned family module (see the note at the top). A module that does not exist yet is skipped.
CHECK_FAMILY_MODULES = [
    "stage_tools.checks_form",
    "stage_tools.checks_ids_citations",
    "stage_tools.checks_coverage_time_state",
    "stage_tools.checks_sides_geometry",
    "stage_tools.checks_craft_reasons_words",
    "stage_tools.checks_plan_generation_film",
]

FAMILY_ORDER = ["FORM", "ID", "CITE", "COVER", "TIME", "STATE", "SIDE", "GEOM", "CRAFT", "INFO", "REASON", "WORDS",
                "PLAN", "GEN", "FILM"]
# The ending code writes after a story point once it is resolved to a beat: SC24 "She deletes the way home." = SC24-B03
RESOLVED_ENDING = re.compile(r'("[^"]*"|“[^”]*”)\s*=\s*SC\d{2,3}[A-Z]?-B\d{2,3}')
# Checks steps.json lists that another command runs (7.2: previs has its own checks in render_previs.py).
CHECKS_OF_OTHER_COMMANDS = {"PREVIS": "stage.py previs --render"}


# ---------------------------------------------------------------- the registry

@dataclass
class CheckDefinition:
    """One check of 7.2: its ID, level, build, 7.2's wording, a plain sentence and the function that runs it."""
    check_id: str
    level: str
    build: int
    title: str
    plain: str
    function: object
    family: str
    module: str = ""


REGISTRY = {}
REPORT_SECTIONS = []
_FAMILIES_LOADED = {"done": False, "missing": [], "broken": {}}


def register_check(check_id, level, build, title, plain="", family=None):
    """Decorator: register a check function under its 7.2 ID (see the note at the top of this file)."""
    def decorator(function):
        register_function(check_id, function, level, build, title, plain, family)
        return function
    return decorator


def register_function(check_id, function, level, build, title, plain="", family=None):
    """Register a check without the decorator. Registering an ID again replaces it and keeps its place."""
    if not re.fullmatch(r"[A-Z]+-\d{2}", check_id):
        raise ValueError(f"{check_id} is not a check ID of 7.2 (FAMILY-NN).")
    if level not in ("E", "W", "N", "E/W"):
        raise ValueError(f"{check_id}: the level must be E, W, N or E/W, not {level}.")
    definition = CheckDefinition(check_id=check_id, level=level, build=int(build), title=title,
                                 plain=plain or "has a problem the checker found", function=function,
                                 family=family or check_id.split("-")[0],
                                 module=getattr(function, "__module__", ""))
    REGISTRY[check_id] = definition
    return definition


def register_report_section(function):
    """Add a section to the plain part of 13 Health check: function(project, result) -> list of plain lines."""
    if function not in REPORT_SECTIONS:
        REPORT_SECTIONS.append(function)
    return function


def load_check_families():
    """Import every family module that exists, so that its checks (and apply checks) are registered.

    The modules are imported inside this package (whatever its name), so the checks register with this very
    registry. A missing module is listed in "missing"; one that fails to import is listed in "broken" with its
    error, and every other family still runs."""
    if _FAMILIES_LOADED["done"]:
        return _FAMILIES_LOADED
    package = __package__ or "stage_tools"
    for module_name in dict.fromkeys(CHECK_FAMILY_MODULES):
        short_name = module_name.rsplit(".", 1)[-1]
        full_name = f"{package}.{short_name}"
        try:
            importlib.import_module(full_name)
        except ModuleNotFoundError as error:
            if error.name in (full_name, module_name):
                _FAMILIES_LOADED["missing"].append(module_name)
                continue
            _FAMILIES_LOADED["broken"][module_name] = f"{type(error).__name__}: {error}"
        except Exception as error:  # a family with a fault must not stop the other checks
            _FAMILIES_LOADED["broken"][module_name] = f"{type(error).__name__}: {error}"
    _FAMILIES_LOADED["done"] = True
    return _FAMILIES_LOADED


def ordered_definitions():
    """Registered checks in 7.2's order: by family, then by number."""
    def order(definition):
        family = definition.family
        position = FAMILY_ORDER.index(family) if family in FAMILY_ORDER else len(FAMILY_ORDER)
        return position, definition.check_id
    return sorted(REGISTRY.values(), key=order)


# ---------------------------------------------------------------- the FORM checks of WP2, registered here

FORM_PLAIN = {
    "FORM-01": ("Unknown record type", "E", "has a heading with a kind of record the tools do not know"),
    "FORM-02": ("ID does not match its type's pattern", "E", "is numbered or named in a form the tools do not accept"),
    "FORM-03": ("Unknown field for this type", "E", "has a detail the tools do not know"),
    "FORM-04": ("Value not allowed for the field's kind or list", "E", "has a value that is not allowed"),
    "FORM-05": ("Required field missing at the depth and step", "E", "is missing a detail it needs at this depth"),
    "FORM-06": ("END line missing", "E", "has no end line, so it may have been cut off"),
    "FORM-07": ("END count differs from the records in the file", "E",
                "has an end line whose count does not match its records, so something may be missing"),
    "FORM-08": ("Shortening marker inside a record", "E", "was shortened instead of written in full"),
    "FORM-09": ("Same field with two different values across merged copies", "E",
                "says two different things in two places"),
    "FORM-10": ("Wrong writer", "E/W", "has a detail written by the wrong hand (one that code or you decide)"),
    "FORM-11": ("Locked record changed", "E", "changes something already approved"),
    "FORM-12": ("Unknown sub-part key, positional sub-part, or a bar inside text", "E",
                "has a detail written in the wrong shape"),
    "FORM-13": ("Tidy fixes applied", "N", "had a small slip of spelling, case or spacing, which I fixed"),
}


def register_form_checks():
    """Register WP2's FORM-01 to FORM-13 (stage_tools/checks_form.py) through a small adapter."""
    try:
        from . import checks_form
    except ModuleNotFoundError:
        return
    for check_id, function in checks_form.FORM_CHECKS.items():
        title, level, plain = FORM_PLAIN[check_id]

        def adapter(run, form_function=function, form_check_id=check_id):
            if form_check_id == "FORM-11" and run.locked_baseline:
                return form_11_against_baseline(run, form_function)
            return form_function(run.record_files, run.form_context)
        adapter.__module__ = checks_form.__name__
        register_function(check_id, adapter, level, 1, title, plain, "FORM")


def form_11_against_baseline(run, form_function):
    """FORM-11 on stored files: each locked record, merged across its files (G10), is compared with the copy the
    checker kept when it last saw it locked ("locked records.json"), so a hand edit of a locked value is caught.
    (apply compares an inbox with the stored files instead.) Each line is then placed at the file and line of the
    copy that holds the changed field."""
    from .record_format import FieldLine, RecordFile

    def comparable(record):
        # code adds the beat a story point resolves to (' = SC10-B07', code_state, 5.6); that is not a change
        copy = Record(type_name=record.type_name, identifier=record.identifier, title=record.title)
        copy.body = [FieldLine(name=line.name, value=RESOLVED_ENDING.sub(r"\1", line.value), written_name=line.name)
                     for line in record.fields]
        return copy

    merged_file = RecordFile(name="the merged records")
    merged_file.segments = [comparable(record) for key, record in run.index.items() if key in run.locked_baseline]
    baseline = {key: comparable(record) for key, record in run.locked_baseline.items()}
    context = dataclasses.replace(run.form_context, current_records=baseline)
    placed = []
    for problem in form_function([merged_file], context):
        record = run.record(getattr(problem, "record", None))
        field_name = getattr(problem, "field_name", None)
        found = run.field_lines(record.key, field_name) if record is not None and field_name else []
        if found:
            record_file, _, line = found[0]
            file_name, line_number = record_file.name, line.line_number
        else:
            file_name, line_number, _ = run.location(record if record is not None else problem.record)
        placed.append(Problem(problem.level, problem.check_id, problem.record, field_name, problem.what, problem.fix,
                              file_name=file_name, line_number=line_number))
    return placed


register_form_checks()


# ---------------------------------------------------------------- small helpers other checks use

def scene_of(identifier):
    """The scene an ID belongs to ("SC10-SH150" -> "SC10", "SC10" -> "SC10"), or None."""
    if not identifier:
        return None
    match = SCENE_PART.match(str(identifier).strip())
    return match.group(1) if match else None


def scene_of_problem(problem):
    """The scene a problem line is about: from its record, else from its scene file's name."""
    record = getattr(problem, "record", None) or ""
    scene = scene_of(record.strip('"'))
    if scene:
        return scene
    return scene_of_file_name(getattr(problem, "file_name", None))


def scene_of_file_name(file_name):
    """The scene a scene file belongs to ("11 Scenes/Scene 10 - Saye's kitchen.md" -> "SC10"), or None."""
    match = SCENE_FILE_NUMBER.match(file_name or "")
    return "SC" + match.group(1) if match else None


def same_scene(first, second):
    """SC10 and SC010 name the same scene (the width is ID-09's business)."""
    if first is None or second is None:
        return False
    return re.sub(r"^SC0*", "SC", first) == re.sub(r"^SC0*", "SC", second)


# ---------------------------------------------------------------- the story, for the CITE checks

class StorySource:
    """The numbered story the CITE checks read, and the speeches.

    numbered: read_story.NumberedStory (with quotes found through a cache); speeches: {ID: entry}; story_map:
    the reader's data; excerpt: True when only part of the story is present (a Stage excerpt such as the
    scene 10 fixture), so a line outside it is "not in the excerpt" rather than wrong; whole_lines: the whole
    story's line count when known.
    """

    def __init__(self, numbered, speeches=None, story_map=None, header=None, source_name=""):
        self.numbered = numbered
        self.speeches = {entry["id"]: entry for entry in (speeches or [])}
        self.story_map = story_map or {}
        self.header = header or {}
        self.source_name = source_name
        self.first = numbered.first
        self.last = numbered.last
        whole = self.header.get("whole_story_lines") or self.story_map.get("whole_story_lines")
        try:
            self.whole_lines = int(whole) if whole else None
        except ValueError:
            self.whole_lines = None
        self.excerpt = self.first > 1 or bool(self.whole_lines and self.whole_lines > self.last) \
            or bool(self.story_map.get("excerpt"))
        whole_scenes = self.header.get("whole_story_scenes")
        try:
            self.whole_scenes = int(whole_scenes) if whole_scenes else None
        except ValueError:
            self.whole_scenes = None

    @classmethod
    def from_file(cls, story_path, constants=None):
        """Read a story file (or a Stage excerpt) the way stage.py read does; stops with exit 2 if unreadable."""
        from .read_story import load_story_file, read_story_lines, speeches_json, story_map_of
        story = load_story_file(story_path)
        reading = read_story_lines(story, constants)
        story_map = story_map_of(reading)
        numbered = CachedNumberedStory.from_story_map(story_map)
        speeches = speeches_json(reading)["speeches"] if reading.speeches else []
        return cls(numbered, speeches, story_map, getattr(reading, "header", None) or getattr(story, "header", None),
                   Path(story_path).name)

    @classmethod
    def from_project(cls, project_folder):
        """The story the project's read wrote (story map.json and speeches.json), or None when not read yet."""
        from .read_story import SPEECHES_FILE, load_story_map
        story_map = load_story_map(project_folder)
        if not story_map:
            return None
        numbered = CachedNumberedStory.from_story_map(story_map)
        speeches = []
        path = Path(project_folder) / MACHINE_FOLDER / SPEECHES_FILE
        if path.is_file():
            with open(path, encoding="utf-8") as handle:
                speeches = json.load(handle).get("speeches", [])
        return cls(numbered, speeches, story_map, None, "story map.json")

    def holds(self, first, last=None):
        """True when every line first..last is present in this story."""
        last = first if last is None else last
        return self.first <= first and last <= self.last

    def scene_range(self, scene_identifier):
        for identifier, lines in self.numbered.scenes.items():
            if same_scene(identifier, scene_identifier):
                return tuple(lines)
        return None

    def chapter_range(self, chapter_identifier):
        return self.numbered.chapters.get(chapter_identifier)

    def find(self, quote, first=None, last=None):
        return self.numbered.find_quote(quote, first, last)

    def scene_count(self):
        return self.whole_scenes or len(self.numbered.scenes)


def make_cached_numbered_story():
    """NumberedStory with each line's comparison form worked out once (a whole film has thousands of quotes)."""
    from .read_story import NumberedStory, normalise_quote

    class CachedNumberedStoryClass(NumberedStory):
        def normalised(self, number):
            cache = self.__dict__.setdefault("_normalised", {})
            if number not in cache:
                cache[number] = normalise_quote(self.line(number))
            return cache[number]

        def find_quote(self, quote, first=None, last=None):
            first = self.first if first is None else first
            last = self.last if last is None else last
            wanted = normalise_quote(quote)
            found = []
            if not wanted:
                return found
            for number in range(max(first, self.first), min(last, self.last) + 1):
                count = self.normalised(number).count(wanted)
                if count:
                    found += [number] * count
            return found

    return CachedNumberedStoryClass


class _LazyClass:
    """Makes CachedNumberedStory on first use, so importing this module does not import the reader."""

    def __init__(self, maker):
        self.maker = maker
        self.made = None

    def __getattr__(self, name):
        if self.made is None:
            self.made = self.maker()
        return getattr(self.made, name)


CachedNumberedStory = _LazyClass(make_cached_numbered_story)


# ---------------------------------------------------------------- one run of the checks

class CheckRun:
    """Everything a check reads (see the note at the top of this file)."""

    def __init__(self, record_files, schema, words, constants, story=None, manifest=None, step=None, scene=None,
                 film=False, project=None, form_context=None, locked_baseline=None):
        self.record_files = list(record_files)
        self.locked_baseline = locked_baseline or {}
        self.schema = schema
        self.words = words or {}
        self.constants = constants or {}
        self.story = story
        self.manifest = manifest or {}
        self.step = step
        self.scene = scene
        self.film = film
        self.project = project
        self.cache = {}
        self.skipped = []
        self.index, _ = merge_copies(self.record_files, schema)
        self._copies = {}
        for record_file in self.record_files:
            for record in record_file.records:
                if record.known_type:
                    self._copies.setdefault(record.key, []).append((record_file, record))
        self._by_identifier = {}
        for key, record in self.index.items():
            self._by_identifier.setdefault(key[1] if key[1] else key[0], record)
        self.project_record = next((record for key, record in self.index.items() if key[0] == "PROJECT"), None)
        if form_context is None:
            from .checks_form import FormContext
            form_context = FormContext.for_records(schema, words, self.record_files, step=step)
            form_context.checkpoints = self.manifest.get("checkpoints") or {}
        self.form_context = form_context
        depth = (self.project_record.get("depth") if self.project_record else None) or "standard"
        self.depth = depth if depth in DEPTH_RANK else "standard"
        self.scope_scenes = self._scope()

    # -- records
    def records(self, type_name, include_omitted=False):
        return [record for key, record in self.index.items()
                if key[0] == type_name and (include_omitted or not self.is_omitted(record))]

    def record(self, reference):
        """A merged record by ID, or a singleton or PROJECT by its type name."""
        if reference in self._by_identifier:
            return self._by_identifier[reference]
        if reference == "PROJECT":
            return self.project_record
        return None

    def copies(self, key):
        return list(self._copies.get(key, []))

    def field_lines(self, key, name):
        return [(record_file, copy, line) for record_file, copy in self._copies.get(key, [])
                for line in copy.field_lines(name)]

    @staticmethod
    def is_omitted(record):
        status = record.get("status") if record is not None else None
        return bool(status) and normalise_word(status) == "omitted"

    def scene_ids(self):
        return [key[1] for key in self.index if key[0] == "SCENE" and key[1]]

    def depth_rank(self, record):
        rank = DEPTH_RANK.get(self.depth, 2)
        scene = self.record(scene_of(record.identifier)) if record is not None and record.identifier else None
        if scene is not None and scene.type_name == "SCENE" and scene.get("depth") in DEPTH_RANK:
            rank = max(rank, DEPTH_RANK[scene.get("depth")])
        return rank

    # -- scope
    def _scope(self):
        if self.project_record is None:
            return None
        value = (self.project_record.get("scope") or "").strip()
        if not value or normalise_word(value) in ("all", "open", "none"):
            return None
        scenes = set()
        for piece in split_list(value):
            if ".." in piece:
                first, last = [part.strip() for part in piece.split("..", 1)]
                known = self.scene_ids() or []
                inside = False
                for identifier in known:
                    if same_scene(identifier, first):
                        inside = True
                    if inside:
                        scenes.add(identifier)
                    if same_scene(identifier, last):
                        inside = False
                scenes.update((first, last))
            else:
                scenes.add(piece)
        return scenes or None

    def scene_checked(self, scene_identifier):
        """True when problems of this scene are reported: it is in the project's scope and matches --scene."""
        if scene_identifier is None:
            return True
        if self.scene is not None and not same_scene(scene_identifier, self.scene):
            return False
        if self.scope_scenes is not None and not any(same_scene(scene_identifier, other) for other in self.scope_scenes):
            return False
        return True

    def in_scope(self, thing):
        identifier = thing.identifier if isinstance(thing, Record) else thing
        return self.scene_checked(scene_of(identifier))

    def has_scene_record(self, scene_identifier):
        return any(same_scene(identifier, scene_identifier) for identifier in self.scene_ids())

    def scene_left_out(self, scene_identifier):
        """True for a scene this check cannot see: the project holds no SCENE record for it, and it lies outside
        the project's scope or outside the excerpt of the story given (a partial example such as the scene 10
        gold). References into such a scene are skipped ("not in the excerpt"), never reported as problems."""
        if scene_identifier is None or self.has_scene_record(scene_identifier):
            return False
        story_has_it = self.story is not None and self.story.scene_range(scene_identifier) is not None
        if self.story is not None and not self.story.excerpt and not story_has_it \
                and (self.story.story_map.get("source") or {}).get("kind") == "screenplay":
            return False
        if self.scope_scenes is not None and not any(same_scene(scene_identifier, other) for other in self.scope_scenes):
            return True
        if self.story is not None and self.story.excerpt and not story_has_it:
            return True
        return False

    # -- lines
    def scene_range(self, scene_identifier):
        """(first, last) story lines of a scene: its SCENE record's lines, else the story's scene, else None."""
        key = ("scene_range", scene_identifier)
        if key in self.cache:
            return self.cache[key]
        result = None
        scene = self.record(scene_identifier)
        is_scene = scene is not None and scene.type_name == "SCENE"
        value = scene.get("lines") if is_scene else None
        for written in (value, scene.get("from_lines") if is_scene else None):
            # a prose scene's lines are worked out from its source passage (from_lines) until code stores them
            numbers = parse_line_numbers(written) if written else None
            if numbers:
                result = (numbers[0][0], numbers[-1][1])
                break
        if result is None and self.story is not None:
            result = self.story.scene_range(scene_identifier)
        if result is None and value and self.story is not None and parse_quote_anchor(value):
            result = self.story.numbered.resolve_lines(value)
        self.cache[key] = result
        return result

    def chapter_range(self, chapter_identifier):
        chapter = self.record(chapter_identifier)
        value = chapter.get("lines") if chapter is not None else None
        if value:
            numbers = parse_line_numbers(value)
            if numbers:
                return numbers[0][0], numbers[-1][1]
        if self.story is not None:
            return self.story.chapter_range(chapter_identifier)
        return None

    @property
    def speeches(self):
        return self.story.speeches if self.story is not None else {}

    def story_missing(self, check_id):
        if self.story is None:
            self.skip(check_id, "story not present (give the story with --story <path>, or run stage.py read)")
            return True
        return False

    # -- batches (step 8)
    def batch_shots(self, scene_identifier):
        """During step 8, the listed shot IDs of the batches written so far; None means every list item.

        After the scene's last batch (every batch in the manifest received), and outside step 8, every item is
        checked. Without batch data, the items up to the highest shot written so far count as written.
        """
        if self.step is None or self.step != 8:
            return None
        batches = (self.manifest.get("batches") or {}).get(scene_identifier) or {}
        if batches and all(batch_complete(entry) for entry in batches.values()):
            return None
        listed = self._listed_shots(scene_identifier)
        ranges = [(entry.get("first"), entry.get("last")) for entry in batches.values()
                  if entry and entry.get("received") is not None and entry.get("first") and entry.get("last")]
        if ranges:
            return {shot for shot in listed
                    if any(shot_number(first) <= shot_number(shot) <= shot_number(last) for first, last in ranges)}
        written = [shot_number(record.identifier) for record in self.records("SHOT", include_omitted=True)
                   if same_scene(scene_of(record.identifier), scene_identifier)]
        if not written:
            return set()
        highest = max(written)
        return {shot for shot in listed if shot_number(shot) <= highest}

    def _listed_shots(self, scene_identifier):
        shots = []
        for record in self.records("SHOTLIST", include_omitted=True):
            if same_scene(scene_of(record.identifier), scene_identifier):
                for value in record.get_all("item"):
                    first = split_item(value).first
                    if first:
                        shots.append(first.strip())
        return shots

    # -- problem lines
    def location(self, reference):
        """(file name, line number, label) of a record's first copy, for a Record, a key or an ID."""
        if isinstance(reference, Record):
            key = reference.key
        elif isinstance(reference, tuple):
            key = reference
        else:
            record = self.record(reference)
            key = record.key if record is not None else None
        copies = self._copies.get(key) if key else None
        if copies:
            record_file, copy = copies[0]
            return record_file.name, copy.heading_line_number, copy.label
        label = reference.label if isinstance(reference, Record) else (key[1] or key[0]) if key else str(reference)
        return None, None, label

    def problem(self, level, check_id, record, field_name, what, fix="", line_number=None, file_name=None):
        """A problem line (7.2) about a record (a Record, a (TYPE, ID) key or an ID), placed in its file."""
        found_file, found_line, label = self.location(record)
        return Problem(level, check_id, label, field_name, what, fix, file_name=file_name or found_file,
                       line_number=line_number or found_line)

    def skip(self, check_id, why):
        entry = (check_id, why)
        if entry not in self.skipped:
            self.skipped.append(entry)


def batch_complete(entry):
    """True when a batch's expected and received shot counts are both known and every expected shot came in."""
    entry = entry or {}
    received, expected = entry.get("received"), entry.get("expected")
    return isinstance(received, int) and isinstance(expected, int) and received >= expected


def shot_number(identifier):
    match = re.search(r"-SH(\d+)$", identifier or "")
    return int(match.group(1)) if match else -1


# ---------------------------------------------------------------- choosing and running checks

def checks_for_step(step, skill_folder=None):
    """The check IDs steps.json lists for a step (step 10 means every check)."""
    steps = load_json("schema/steps.json", skill_folder)
    for entry in steps.get("steps", []):
        if entry.get("step") == step:
            listed = [item for item in entry.get("checks", []) if re.fullmatch(r"[A-Z]+-\d{2}", item)]
            if any("all checks" in item for item in entry.get("checks", [])):
                return None
            return listed
    return []


@dataclass
class CheckResult:
    """What run_checks found: problem lines, skipped checks (check ID, why), tidy notes, what ran and what is missing."""
    problems: list = dataclass_field(default_factory=list)
    skipped: list = dataclass_field(default_factory=list)
    tidy_notes: list = dataclass_field(default_factory=list)
    checks_run: list = dataclass_field(default_factory=list)
    checks_not_present: list = dataclass_field(default_factory=list)
    families_broken: dict = dataclass_field(default_factory=dict)
    crashed: dict = dataclass_field(default_factory=dict)
    changed_files: list = dataclass_field(default_factory=list)
    all_problems: list = dataclass_field(default_factory=list)
    left_out_by_scene: int = 0
    run: object = None

    @property
    def counts(self):
        return count_levels(self.problems)

    @property
    def errors(self):
        return [problem for problem in self.problems if getattr(problem, "level", str(problem)[:1]) == "E"]


def select_checks(step=None, film=False, check_ids=None):
    """(the registered checks to run, the listed check IDs that are not registered)."""
    load_check_families()
    wanted = None
    if check_ids is not None:
        wanted = list(check_ids)
    elif step is not None:
        listed = checks_for_step(step)
        wanted = None if listed is None else list(listed)
        if film:
            wanted = (wanted or []) + [definition.check_id for definition in REGISTRY.values()
                                       if definition.family == "FILM"] + (checks_for_step(9) or [])
    elif film:
        wanted = [definition.check_id for definition in REGISTRY.values() if definition.family == "FILM"]
        wanted += checks_for_step(9) or []
    definitions = ordered_definitions()
    if wanted is None:
        return definitions, []
    chosen = [definition for definition in definitions if definition.check_id in wanted]
    missing = sorted({check_id for check_id in wanted if check_id not in REGISTRY})
    return chosen, missing


def run_checks(record_files, schema, words, constants, story=None, manifest=None, step=None, scene=None,
               film=False, check_ids=None, tidy=False, project=None, locked_baseline=None):
    """Run the chosen checks on parsed record files and return a CheckResult.

    step: the step checked (FORM-05 asks only for fields filled by then; the checks steps.json lists for it run),
    or None for every check. film: add the whole-film checks. check_ids: run exactly these IDs instead.
    scene: report only the problems of that scene's records and scene files (the others are counted in
    left_out_by_scene). tidy=True makes the FORM-13 tidy fixes in the records first (the caller writes the
    changed files); the FORM-13 lines are the fixes made, and the other checks read the tidied records.
    locked_baseline: {(TYPE, ID): Record} as the checker last saw each locked record (FORM-11 on stored files).
    The problems of records outside PROJECT.scope are always left out.
    """
    from .checks_form import FORM_CHECKS, FormContext, apply_tidy_fixes
    result = CheckResult()
    families = load_check_families()
    result.families_broken = dict(families["broken"])
    definitions, missing = select_checks(step, film, check_ids)
    result.checks_not_present = missing
    form_context = FormContext.for_records(schema, words, record_files, step=step)
    form_context.checkpoints = (manifest or {}).get("checkpoints") or {}
    wanted_ids = {definition.check_id for definition in definitions}
    if "FORM-13" in wanted_ids or tidy:
        result.tidy_notes = FORM_CHECKS["FORM-13"](record_files, form_context)
    if tidy:
        before = {record_file.name: render_file(record_file, schema) for record_file in record_files}
        apply_tidy_fixes(record_files, form_context)
        result.changed_files = [record_file.name for record_file in record_files
                                if render_file(record_file, schema) != before[record_file.name]]
        form_context = FormContext.for_records(schema, words, record_files, step=step)
        form_context.checkpoints = (manifest or {}).get("checkpoints") or {}
    run = CheckRun(record_files, schema, words, constants, story=story, manifest=manifest, step=step, scene=scene,
                   film=film, project=project, form_context=form_context, locked_baseline=locked_baseline)
    result.run = run
    problems = []
    for definition in definitions:
        if definition.check_id == "FORM-13":
            found = list(result.tidy_notes)
        else:
            try:
                found = definition.function(run) or []
            except Exception as error:  # one broken check must not hide the others
                result.crashed[definition.check_id] = f"{type(error).__name__}: {error}"
                continue
        result.checks_run.append(definition.check_id)
        problems.extend(found)
    order = {definition.check_id: index for index, definition in enumerate(ordered_definitions())}
    file_order = {record_file.name: index for index, record_file in enumerate(record_files)}
    distinct = []
    seen = set()
    for problem in problems:
        line = str(problem)
        if line not in seen:
            seen.add(line)
            distinct.append(problem)
    distinct.sort(key=lambda problem: (order.get(getattr(problem, "check_id", ""), len(order)),
                                       file_order.get(getattr(problem, "file_name", None), len(file_order)),
                                       getattr(problem, "line_number", None) or 0))
    result.all_problems = distinct
    kept = []
    for problem in distinct:
        problem_scene = scene_of_problem(problem)
        if not run.scene_checked(problem_scene):
            continue
        if scene is not None and problem_scene is None:
            result.left_out_by_scene += 1
            continue
        kept.append(problem)
    result.problems = kept
    result.skipped = list(run.skipped)
    for check_id in missing:
        other_command = CHECKS_OF_OTHER_COMMANDS.get(check_id.split("-")[0])
        result.skipped.append((check_id, f"run by {other_command}, not by check" if other_command
                               else "not in this copy of the tools yet"))
    for check_id, reason in result.crashed.items():
        result.skipped.append((check_id, f"the check stopped with an error ({reason}); report this line"))
    return result


# ---------------------------------------------------------------- plain words for the report

TYPE_WORDS = {
    "PLAN": "the story plan", "STYLE": "the style", "WORLD": "the world", "CAMSYS": "the camera system",
    "SOUNDPLAN": "the sound plan", "LADDER": "the ladder of closest shots", "PROJECT": "the project",
}
NAMED_TYPE_WORDS = {
    "CHARACTER": "", "VOICE": "", "LOCATION": "", "PROP": "", "TEXT": "the text", "MOTIF": "the motif",
    "CAMERA": "the in-story camera", "RULE": "the rule", "LOOK": "the look", "CAMRULE": "the camera rule for",
    "VISUAL": "the visual plan", "SEQUENCE": "group of scenes", "CHAPTER": "chapter", "STRAND": "the strand",
    "CARDINAL": "the key event", "PLANT": "the plant", "FACT": "the fact", "RESERVE": "saved choice",
    "LENS": "lens exception", "CHOICE": "choice", "SETVALUE": "an answer of", "FINDING": "finding",
    "REVIEW": "the review", "RIGHTS": "the rights record",
}
SUFFIX_WORDS = {"SH": "shot", "B": "beat", "P": "part", "V": "value", "D": "speech", "M": "move", "C": "the cut after shot"}


def plain_number(text):
    return str(int(text)) if text.isdigit() else text


def plain_name_of(label, run=None):
    """A record's name in plain words for the report: "scene 10, shot 150", "choice 21", "Iona", "the story plan".

    Never an ID or a code (WORDS-04)."""
    label = (label or "").strip()
    if label.startswith('"') and label.endswith('"'):
        inner = label[1:-1]
        if inner.startswith("#"):
            return "a heading"
        return re.sub(r"\.md$", "", inner)
    if label in TYPE_WORDS:
        return TYPE_WORDS[label]
    if not label:
        return "a record"
    match = re.match(r"^SC0*(\d+[A-Z]?)(?:-(.+))?$", label)
    if match:
        scene_words = f"scene {match.group(1)}"
        rest = match.group(2)
        if not rest:
            return scene_words
        if rest == "LIST":
            return f"{scene_words}, the shot list"
        if rest == "MASTER":
            return f"{scene_words}, the master shot"
        inner = re.match(r"^(SH|SU|B|P|V|D|M|C)(\d+)(?:\.(\d+))?$", rest)
        if inner:
            kind, number, clip = inner.groups()
            if kind == "SU":
                index = int(number) - 1
                letter = chr(ord("A") + index) if 0 <= index < 26 else number
                return f"{scene_words}, camera {letter}"
            # shots keep their three digits ("shot 010", as every view and message says them, 5.3); the rest are
            # counted plainly ("beat 7", "speech 11")
            shown = number if kind in ("SH", "C") else plain_number(number)
            words = f"{scene_words}, {SUFFIX_WORDS[kind]} {shown}"
            if clip:
                words += f", clip {clip}"
            return words
        return f"{scene_words}, a record"
    record = run.record(label) if run is not None else None
    state = re.match(r"^(.+)\.S0*(\d+)$", label)
    if state:
        owner = run.record(state.group(1)) if run is not None else None
        owner_words = owner.title if owner is not None and owner.title else plain_words_from_code(state.group(1))
        return f"{owner_words}, state {state.group(2)}"
    numbered = re.match(r"^(CHOICE|FIND|RT|SQ|CP|RC|LX|PL|FT|ST|CF)-?0*(\d+)(?:-([A-Z]))?$", label)
    if numbered:
        prefix, number, letter = numbered.groups()
        words = {"CHOICE": "choice", "FIND": "finding", "RT": "rights record", "SQ": "group of scenes",
                 "CP": "chapter", "RC": "saved choice", "LX": "lens exception", "PL": "plant", "FT": "fact",
                 "ST": "strand", "CF": "key event"}[prefix]
        text = f"{words} {number}"
        if letter:
            text = f"answer {letter.lower()} of {text}"
        return text
    if label.startswith("RV-"):
        scene = plain_name_of(label[3:], run) if label[3:] != "FILM" else "the film"
        return f"the review of {scene}"
    # the add-on records name what they belong to: their words come from that record, never from the code
    made = MADE_FOR_PATTERNS.match(label)
    if made:
        return made_for_words(made, run)
    if record is not None and record.type_name in TYPE_WORDS:
        return TYPE_WORDS[record.type_name]
    if record is not None and record.title:
        prefix = NAMED_TYPE_WORDS.get(record.type_name, "")
        return f"{prefix} {record.title}".strip()
    return plain_words_from_code(label)


MADE_FOR_PATTERNS = re.compile(
    r"^(?:(?P<visual>VS)-(?P<visual_of>SQ\d+)"
    r"|(?P<picture>PIC)-(?P<picture_of>.+)-(?P<use>START|END|REFERENCE|STORYBOARD|STILL|LAYOUT|STYLE)-0*(?P<picture_number>\d+)"
    r"|(?P<previs>PV)-(?P<previs_of>.+)-V0*(?P<try>\d+)"
    r"|(?P<take>TK)-(?P<take_of>.+)-T0*(?P<take_number>\d+)"
    r"|(?P<voice>VT)-(?P<voice_of>.+)-T0*(?P<voice_number>\d+)"
    r"|(?P<finish>FX)-(?P<finish_of>.+)-0*(?P<finish_number>\d+)"
    r"|(?P<music>MU)-0*(?P<music_number>\d+))$")
PICTURE_USE_WORDS = {"START": "the start picture", "END": "the end picture", "REFERENCE": "the reference pictures",
                     "STORYBOARD": "the storyboard frame", "STILL": "the still", "LAYOUT": "the layout picture",
                     "STYLE": "the style picture"}


def made_for_words(match, run=None):
    """Plain words for an add-on record's ID from what it belongs to: PIC-SC10-SH150-START-01 -> "the start picture of
    scene 10, shot 150"; PV-SC10-SH080-V01 -> "the grey preview of scene 10, shot 080, try 1"."""
    if match.group("visual"):
        return f"the visual plan of {plain_name_of(match.group('visual_of'), run)}"
    if match.group("picture"):
        words = f"{PICTURE_USE_WORDS[match.group('use')]} of {plain_name_of(match.group('picture_of'), run)}"
        number = int(match.group("picture_number"))
        return words + (f", number {number}" if number > 1 else "")
    if match.group("previs"):
        return f"the grey preview of {plain_name_of(match.group('previs_of'), run)}, try {int(match.group('try'))}"
    if match.group("take"):
        return f"take {int(match.group('take_number'))} of {plain_name_of(match.group('take_of'), run)}"
    if match.group("voice"):
        return f"voice take {int(match.group('voice_number'))} of {plain_name_of(match.group('voice_of'), run)}"
    if match.group("finish"):
        return f"finishing job {int(match.group('finish_number'))} of {plain_name_of(match.group('finish_of'), run)}"
    return f"music cue {int(match.group('music_number'))}"


def plain_words_from_code(label):
    """CH-IONA -> Iona; LOC-SAYE-KITCHEN -> Saye kitchen: the words of a named ID without its prefix."""
    parts = label.split("-")
    if len(parts) > 1 and parts[0].isalpha() and parts[0].isupper():
        parts = parts[1:]
    words = " ".join(part.lower() for part in parts if part)
    words = re.sub(r"\d+", lambda match: plain_number(match.group(0)), words)
    return words[:1].upper() + words[1:] if words else "a record"


def plain_problem_line(problem, run):
    """One line of the plain part: where it is and what is wrong, in plain words."""
    definition = REGISTRY.get(getattr(problem, "check_id", ""))
    plain = definition.plain if definition else "has a problem the checker found"
    record = getattr(problem, "record", "") or ""
    file_name = re.sub(r"\.md$", "", getattr(problem, "file_name", None) or "")
    name = plain_name_of(record, run)
    if record.startswith('"') and not record.startswith('"#'):
        where = name  # a whole file ("04 Scene list")
    elif scene_of(record.strip('"')) or not file_name:
        where = name  # a scene's record says where it is: "Scene 10, shot 150"
    else:
        where = f"{name}, in {file_name}"
    where = where[:1].upper() + where[1:]
    return f"- {where}: {plain}."


def plain_problem_lines(problems, run):
    """The plain lines for a list of problems: the same plain line once, with how many times it was found, and at
    most PLAIN_LINES_LISTED lines; the rest are counted."""
    counted = {}
    for problem in problems:
        line = plain_problem_line(problem, run)
        counted[line] = counted.get(line, 0) + 1
    lines = []
    for line, count in list(counted.items())[:PLAIN_LINES_LISTED]:
        lines.append(line if count == 1 else f"{line[:-1]} ({count} times).")
    hidden = sum(list(counted.values())[PLAIN_LINES_LISTED:])
    if hidden:
        lines.append(f"- And {hidden} more, listed below the line for the AI.")
    return lines


def plural(count, word, plural_word=None):
    return f"{count} {word if count == 1 else (plural_word or word + 's')}"


def in_short_line(result, needs_you):
    """The report's first line (step 10): 'In short: 2 things need you, 14 small fixes I made, 3 warnings'. With
    problems still to fix it says them first, and says that no question waits for the user rather than "nothing
    needs you", which read as a contradiction next to them."""
    counts = result.counts
    errors = counts.get("E", 0)
    if needs_you:
        needs = f"{plural(needs_you, 'thing')} {'needs' if needs_you == 1 else 'need'} you"
    else:
        needs = "no question waits for you" if errors else "nothing needs you"
    fixes = len(result.tidy_notes)
    warnings = counts.get("W", 0)
    parts = [needs, f"{plural(fixes, 'small fix', 'small fixes')} I made" if fixes else "no small fixes needed",
             plural(warnings, "warning") if warnings else "no warnings"]
    if errors:
        parts.insert(0, f"{plural(errors, 'problem')} still to fix")
    return "In short: " + ", ".join(parts) + "."


def open_questions(run):
    """Choices waiting for the user: asked, still open (the things that need the user)."""
    count = 0
    for choice in run.records("CHOICE"):
        if normalise_word(choice.get("status") or "open") == "open" and normalise_word(choice.get("asked") or "no") == "yes":
            count += 1
    return count


ADD_ON_STEP_WORDS = {12: "the storyboards", 13: "the grey previews", 14: "the prompts for AI video",
                     15: "the edit and finishing", 16: "resuming after a problem"}


def scene_in_words(scene):
    """SC10 -> "scene 10"; SC06A -> "scene 6A"."""
    match = re.match(r"^SC0*(\d+)([A-Z]?)$", scene or "")
    return f"scene {match.group(1)}{match.group(2)}" if match else "one scene"


def what_was_checked(step, scene, film, all_checks):
    """What a check covered, in the user's words: 'the checks for step 8 of 12, scene 10 only'."""
    parts = []
    if step is not None:
        if isinstance(step, int) and step <= 11:
            parts.append(f"the checks for step {step + 1} of 12")
        else:
            parts.append(f"the checks for {ADD_ON_STEP_WORDS.get(step, 'this step')}")
    if film:
        parts.append("the whole film")
    if not parts:
        parts.append("everything")
    if scene:
        parts.append(f"{scene_in_words(scene)} only")
    return ", ".join(parts)


def health_check_plain_part(project, result, step, scene, film, all_checks, story):
    """The plain part of 13 Health check.md (step 10, 13.3). Its first line is 'In short: ...'; then At a glance
    (what was checked, the scope on a partial scope), what to fix first, warnings, the small fixes made, what could
    not be checked, the sections other modules add (quality scores, the three scenes to read) and the details by
    file. Plain words only: no check IDs, record IDs or abbreviations (WORDS-04)."""
    run = result.run
    lines = [in_short_line(result, open_questions(run)), "", f"# {HEALTH_CHECK_TITLE}", "", "## At a glance", ""]
    stamp = datetime.datetime.now()
    lines.append(f"Checked: {what_was_checked(step, scene, film, all_checks)}, on "
                 f"{stamp.day} {stamp.strftime('%B %Y')} at {stamp.strftime('%H:%M')}.")
    scene_ids = run.scene_ids()
    total = len(scene_ids)
    if story is not None and story.scene_count():
        total = max(total, story.scene_count())
    if run.scope_scenes is not None and total:
        in_scope = len([identifier for identifier in run.scope_scenes if re.fullmatch(r"SC\d{2,3}[A-Z]?", identifier)])
        if in_scope < total:
            lines.append(f"Scope: {in_scope} of {total} scenes.")
    if story is None:
        lines.append("The story's own words were not compared: the numbered story is not in this folder yet.")
    if result.left_out_by_scene:
        lines.append(f"{plural(result.left_out_by_scene, 'line')} about the whole-film files "
                     f"{'was' if result.left_out_by_scene == 1 else 'were'} left out, because this check looked at "
                     f"{scene_in_words(scene)} only.")
    lines.append("")
    errors = [problem for problem in result.problems if getattr(problem, "level", "") == "E"]
    warnings = [problem for problem in result.problems if getattr(problem, "level", "") == "W"]
    lines.append("## What to fix first")
    lines.append("")
    if errors:
        lines.extend(plain_problem_lines(errors, run))
    else:
        lines.append("Nothing: no problem was found.")
    lines.append("")
    lines.append("## Warnings")
    lines.append("")
    if warnings:
        lines.extend(plain_problem_lines(warnings, run))
    else:
        lines.append("None.")
    lines.append("")
    lines.append("## Small fixes I made")
    lines.append("")
    if result.tidy_notes:
        files = sorted({re.sub(r"\.md$", "", getattr(note, "file_name", "") or "") for note in result.tidy_notes} - {""})
        lines.append(f"{plural(len(result.tidy_notes), 'small fix', 'small fixes')} of spelling, case or spacing"
                     + (f", in {', '.join(files)}." if files else "."))
    else:
        lines.append("None were needed.")
    if result.skipped:
        lines.append("")
        lines.append("## Not checked this time")
        lines.append("")
        if result.crashed:
            lines.append(f"{plural(len(result.crashed), 'check')} stopped with a fault in the tools, so what "
                         f"{'it' if len(result.crashed) == 1 else 'they'} would find is not known; the lines for the "
                         "AI below say which.")
        lines.append(f"{plural(len(result.skipped), 'check')} could not run in full; the reasons are below the line "
                     "for the AI.")
    for section in [lambda project, result: quality_scores_plain_lines(result.run),
                    lambda project, result: scenes_to_read_plain_lines(result.run)] + list(REPORT_SECTIONS):
        try:
            extra = section(project, result) or []
        except Exception:  # a report section must never stop the report
            extra = []
        if extra:
            lines.append("")
            lines.extend(extra)
    lines.append("")
    lines.append("## Details by file")
    lines.append("")
    by_file = {}
    for problem in result.problems:
        name = re.sub(r"\.md$", "", getattr(problem, "file_name", None) or "") or "the project"
        counts = by_file.setdefault(name, {"E": 0, "W": 0, "N": 0})
        counts[getattr(problem, "level", "N")] = counts.get(getattr(problem, "level", "N"), 0) + 1
    checked_files = [re.sub(r"\.md$", "", record_file.name) for record_file in run.record_files]
    if scene is not None:
        checked_files = [name for name in checked_files
                         if name in by_file or same_scene(scene_of_file_name(name + ".md"), scene)]
    for name in checked_files + sorted(set(by_file) - set(checked_files)):
        counts = by_file.get(name)
        if not counts or not (counts["E"] or counts["W"]):
            lines.append(f"- {name}: nothing to fix.")
            continue
        parts = []
        if counts["E"]:
            parts.append(plural(counts["E"], "problem"))
        if counts["W"]:
            parts.append(plural(counts["W"], "warning"))
        lines.append(f"- {name}: {', '.join(parts)}.")
    lines.append("")
    return lines


# The ten scoring questions (reference/05 Quality rubric), in the user's words.
RUBRIC_PLAIN_NAMES = {1: "being faithful to the story", 2: "reading the story", 3: "shots that serve the beats",
                      4: "the reasons", 5: "restraint", 6: "continuity and sides", 7: "rhythm and time",
                      8: "the film's visual plan", 9: "being ready for AI video", 10: "being easy to read"}


def review_scores(run):
    """{scene or 'film': {criterion number: score}} from the REVIEW records' score items."""
    found = {}
    for review in run.records("REVIEW"):
        scope = (review.get("scope") or "").strip()
        scores = {}
        for value in review.get_all("score"):
            numbers = re.findall(r"\d+", value.split("| evidence", 1)[0])
            if len(numbers) >= 2:
                scores[int(numbers[0])] = int(numbers[1])
        if scores:
            found[scope or review.identifier] = scores
    return found


def scene_passes(scores):
    """The rubric's pass rule on one scene's scores (reference/05): no criterion at 0, criteria 1, 3 and 6 at 2 or
    more, and a total of 20 or more of 30. The 'no error' part is the checker's, said on its own line."""
    return (all(score > 0 for score in scores.values()) and all(scores.get(number, 0) >= 2 for number in (1, 3, 6))
            and sum(scores.values()) >= 20)


def quality_scores_plain_lines(run):
    """The plain section "Quality scores" of 13 Health check once the scores exist: how many scenes pass, the
    average, the scenes that do not pass and why, and whether the film passes. [] before any score is written."""
    found = review_scores(run)
    scenes = {scope: scores for scope, scores in found.items() if re.fullmatch(r"SC\d{2,3}[A-Z]?", scope)}
    if not scenes:
        return []
    lines = ["## Quality scores", ""]
    passing = [scope for scope, scores in scenes.items() if scene_passes(scores)]
    totals = {scope: sum(scores.values()) for scope, scores in scenes.items()}
    average = sum(totals.values()) / len(totals)
    best = max(totals.values())
    best_scenes = sorted((scope for scope, total in totals.items() if total == best), key=sort_key_for_identifier)
    lines.append(f"Each scene is scored on 10 questions, each from 0 to 3; 20 of 30 is a pass. "
                 f"{len(passing)} of {plural(len(scenes), 'scene')} pass; the average is {average:.0f} of 30; the best "
                 f"{'is' if len(best_scenes) == 1 else 'are'} {join_words([scene_in_words(scope) for scope in best_scenes])}, "
                 f"at {best}.")
    for scope in sorted(set(scenes) - set(passing), key=sort_key_for_identifier):
        scores = scenes[scope]
        low = [RUBRIC_PLAIN_NAMES.get(number, f"question {number}") for number, score in sorted(scores.items())
               if score < 2]
        lines.append(f"- {scene_in_words(scope).capitalize()} does not pass yet: {totals[scope]} of 30"
                     + (f"; it scores low on {join_words(low)}" if low else "") + ".")
    film_passes = len(passing) == len(scenes)
    lines.append("The whole film passes: every scene passes." if film_passes else
                 "The whole film does not pass yet: it passes when every scene passes.")
    return lines


def scenes_to_read_plain_lines(run):
    """The plain section "Three scenes to read": the climax, the scene with the most speeches and the biggest
    action scene (step 10), each once. [] before the scene designs exist."""
    scenes = [scene for scene in run.records("SCENE") if re.fullmatch(r"SC\d{2,3}[A-Z]?", scene.identifier or "")]
    if not scenes or not run.records("SHOT"):
        return []
    plan = next(iter(run.records("PLAN")), None)
    chosen = []
    climax = split_item((plan.get("climax") or "") if plan is not None else "").first
    climax = scene_of(climax) if climax else None
    if climax and any(scene.identifier == climax for scene in scenes):
        chosen.append((climax, "the climax"))
    speeches = {}
    for scene in scenes:
        count = 0
        for value in scene.get_all("speaking"):
            number = re.search(r"cues:\s*(\d+)", value)
            count += int(number.group(1)) if number else 0
        speeches[scene.identifier] = count
    shots = {}
    for shot in run.records("SHOT"):
        shots[scene_of(shot.identifier)] = shots.get(scene_of(shot.identifier), 0) + 1
    talk = max((scene for scene in scenes if scene.identifier not in dict(chosen)),
               key=lambda scene: speeches.get(scene.identifier, 0), default=None)
    if talk is not None and speeches.get(talk.identifier):
        chosen.append((talk.identifier, "the most talk"))
    action = [scene for scene in scenes if "action" in [normalise_word(tag) for tag in split_list(scene.get("tags") or "")]
              and scene.identifier not in dict(chosen)]
    if action:
        biggest = max(action, key=lambda scene: shots.get(scene.identifier, 0))
        chosen.append((biggest.identifier, "the most action"))
    if not chosen:
        return []
    return ["## Three scenes to read", "",
            "Read these in 15 The breakdown, with the 10 questions in the guide \"05 How to read your breakdown\" "
            "(in the Stage folder, beside 01 Read me first): "
            + join_words([f"{scene_in_words(scope)} ({why})" for scope, why in chosen]) + "."]


def join_words(items):
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def checker_lines_block(result, command_line):
    """The checker's own lines, below the divider: for the AI, with IDs and codes."""
    lines = ["## The checker's lines", "", f"Command: {command_line}"]
    counts = result.counts
    lines.append(f"Counts: {plural(counts.get('E', 0), 'error')}, {plural(counts.get('W', 0), 'warning')}, "
                 f"{plural(counts.get('N', 0), 'note')}; {plural(len(result.checks_run), 'check')} run.")
    if result.left_out_by_scene:
        lines.append(f"Left out: {plural(result.left_out_by_scene, 'line')} about records of no scene (whole-film "
                     "files); check --all shows them.")
    if result.problems:
        lines.append("")
        lines.extend(str(problem) for problem in result.problems)
    if result.skipped:
        lines.append("")
        lines.extend(f"Skipped {check_id}: {why}" for check_id, why in result.skipped)
    lines.append("")
    return lines


FULL_CHECK_MARK = re.compile(r"^Checked: everything, on ")


def plain_part_of(record_file):
    """The lines above the divider of a parsed file, or [] when it has no divider."""
    lines = []
    for segment in record_file.segments:
        if not isinstance(segment, TextBlock):
            break
        for line in segment.lines:
            if line.strip() == DIVIDER_LINE:
                return lines
            lines.append(line)
    return []


def write_health_check(project, result, step, scene, film, all_checks, story, command_line):
    """Write 13 Health check.md: its plain part, the checker's lines below the divider; its REVIEW and FINDING
    records are kept. Returns the path, or None when nothing was written.

    Only a full check (check --all) writes the plain part the user reads once a full check has run: a check of one
    step, one unit, one scene or the film keeps that plain part and replaces only the checker's lines for the AI,
    so what the user reads never depends on which check ran last. Before any full check, a partial check writes the
    plain part (there is nothing better to show). A check that ran no check at all writes nothing."""
    if not result.checks_run and not getattr(result, "checks_not_present", None):
        return None
    path = project.folder / HEALTH_CHECK_FILE
    existing = parse_file(path, HEALTH_CHECK_FILE, project.schema) if path.is_file() else None
    full = all_checks and step is None and scene is None and not film
    kept_plain = plain_part_of(existing) if existing is not None and not full else []
    if kept_plain and any(FULL_CHECK_MARK.match(line) for line in kept_plain):
        plain = list(kept_plain)
        # the report sections still run: the film pass's writes the film strip and 12 Whole-film check
        for section in REPORT_SECTIONS:
            try:
                section(project, result)
            except Exception:  # a report section must never stop the report
                pass
    else:
        plain = health_check_plain_part(project, result, step, scene, film, all_checks, story)
    block = TextBlock()
    for line in plain + [DIVIDER_LINE, ""] + checker_lines_block(result, command_line):
        block.lines.append(line)
        block.line_numbers.append(None)
    if existing is not None:
        record_file = existing
        kept = [segment for segment in record_file.segments if isinstance(segment, (Record, EndLine))]
        if not any(isinstance(segment, EndLine) for segment in kept):
            kept.append(EndLine(raw=None, what=HEALTH_CHECK_TITLE, count=0, changed=True))
        record_file.segments = [block] + kept
    else:
        from .record_format import RecordFile
        record_file = RecordFile(name=HEALTH_CHECK_FILE)
        record_file.segments = [block, EndLine(raw=None, what=HEALTH_CHECK_TITLE, count=0, changed=True)]
    end_line = record_file.end_line
    if end_line is not None and end_line.count != len(record_file.records):
        end_line.changed = True
    write_file(record_file, path, project.schema)
    return path


# ---------------------------------------------------------------- the locked records the checker last saw (FORM-11)

# "For machines - do not edit/locked records.json": {"TYPE ID": [the record's lines]} for every locked record, as the
# checker last saw it (the merged copy, one line per field). Kept apart from manifest.json, which every command
# reads, because it holds whole records; pack carries it, so a lock survives a move between apps.
LOCKED_RECORDS_FILE = "locked records.json"


def baseline_name(key):
    return f"{key[0]} {key[1]}" if key[1] else key[0]


def read_locked_records(project_folder):
    """The stored lines of each locked record ({"TYPE ID": [lines]}), or {} when the checker has not run yet."""
    path = Path(project_folder) / MACHINE_FOLDER / LOCKED_RECORDS_FILE
    if not path.is_file():
        return {}
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        return {}
    return data.get("records", {}) if isinstance(data, dict) else {}


def write_locked_records(project_folder, records):
    folder = Path(project_folder) / MACHINE_FOLDER
    folder.mkdir(parents=True, exist_ok=True)
    temporary = folder / (LOCKED_RECORDS_FILE + ".part")
    with open(temporary, "w", encoding="utf-8") as handle:
        json.dump({"about": "Each locked record as the checker last saw it (FORM-11). Written by stage.py check; "
                            "never edit.", "records": records}, handle, indent=0, ensure_ascii=False)
        handle.write("\n")
    temporary.replace(folder / LOCKED_RECORDS_FILE)


def forget_locked_records(project_folder):
    """Remove the checker's copies of the locked records, so the next check takes new ones. For code that rewrites
    locked values itself (adopt turns quote anchors into line numbers); nothing else should call it."""
    path = Path(project_folder) / MACHINE_FOLDER / LOCKED_RECORDS_FILE
    if path.is_file():
        path.unlink()


def locked_baseline_from_lines(stored, schema):
    """{(TYPE, ID): Record} from the stored lines of each locked record. {} when there is none yet."""
    blocks = ["\n".join(lines) for lines in (stored or {}).values() if isinstance(lines, list) and lines]
    if not blocks:
        return {}
    record_file = parse_text("\n\n".join(blocks) + "\n", "locked records", schema)
    return {record.key: record for record in record_file.records if record.known_type}


def next_locked_records(result, old, schema):
    """The locked records to keep after a check.

    A locked record the check found unchanged (no FORM-11 error) is kept as it is now; one with a FORM-11 error
    keeps its old copy, so the error stays until the value is put back or a choice changes it. When FORM-11 did
    not run (a step whose checks leave it out), the old copies stay and only newly locked records are added.
    Records no longer locked are dropped (unlocking goes through a choice the user answers)."""
    old = dict(old or {})
    form_11_ran = "FORM-11" in result.checks_run
    flagged = {getattr(problem, "record", None) for problem in result.all_problems
               if getattr(problem, "check_id", "") == "FORM-11" and getattr(problem, "level", "") == "E"}
    kept = {}
    for key, record in result.run.index.items():
        if normalise_word(record.get("locked") or "") != "yes":
            continue
        name = baseline_name(key)
        if name in old and (not form_11_ran or record.label in flagged):
            kept[name] = old[name]
        else:
            kept[name] = record_lines(record, schema, canonical=True)
    return kept


# ---------------------------------------------------------------- the command

def add_check_arguments(parser):
    parser.add_argument("--step", help="check as at the end of this step (0 to 16; step 8 is 'shot details'): only "
                                       "the checks of that step, and only fields filled by then")
    parser.add_argument("--scene", help="report only this scene's records, for example SC10")
    parser.add_argument("--film", action="store_true", help="run the whole-film checks (step 9)")
    parser.add_argument("--all", action="store_true", help="run every check and ask for every field (the default)")
    parser.add_argument("--story", help="read the story from this file for the checks that compare story words")
    parser.add_argument("--unit", help="check only the records this unit wrote (for example U-07-SC10), with its "
                                       "step's checks and only the fields its step fills")


def read_step(text):
    if text is None:
        return None
    value = str(text).strip()
    if not re.fullmatch(r"\d{1,2}", value) or int(value) > 16:
        raise StageStop(f'The step "{text}" is not a step number. Give a number from 0 to 16, as --step 8.')
    return int(value)


def read_scene(text):
    if text is None:
        return None
    value = str(text).strip().upper()
    if re.fullmatch(r"\d{1,3}[A-Z]?", value):
        value = "SC" + value.zfill(2) if not value[-1].isalpha() else "SC" + value[:-1].zfill(2) + value[-1]
    if not re.fullmatch(r"SC\d{2,3}[A-Z]?", value):
        raise StageStop(f'"{text}" is not a scene. Give a scene as SC10 (scene 10).')
    return value


def command_line_of(arguments):
    parts = ["check"]
    if getattr(arguments, "step", None) is not None:
        parts.append(f"--step {arguments.step}")
    if getattr(arguments, "scene", None):
        parts.append(f"--scene {arguments.scene}")
    if getattr(arguments, "film", False):
        parts.append("--film")
    if getattr(arguments, "all", False):
        parts.append("--all")
    if getattr(arguments, "story", None):
        parts.append(f"--story \"{Path(arguments.story).name}\"")
    if getattr(arguments, "unit", None):
        parts.append(f"--unit {arguments.unit}")
    return " ".join(parts)


def printable_lines(result):
    """The lines check prints: every error and warning, every check that stopped with a fault, the first notes and
    skips, then a count of the rest."""
    lines = [str(problem) for problem in result.problems if getattr(problem, "level", "") in ("E", "W")]
    notes = [str(problem) for problem in result.problems if getattr(problem, "level", "") == "N"]
    lines.extend(notes[:NOTE_LINES_PRINTED])
    if len(notes) > NOTE_LINES_PRINTED:
        lines.append(f"And {len(notes) - NOTE_LINES_PRINTED} more notes, listed in {HEALTH_CHECK_FILE}.")
    for check_id, reason in result.crashed.items():
        lines.append(f"The check {check_id} stopped with a fault in the tools ({reason}); its problems are not known. "
                     "Report this line.")
    skipped = [f"Skipped {check_id}: {why}" for check_id, why in result.skipped if check_id not in result.crashed]
    lines.extend(skipped[:SKIP_LINES_PRINTED])
    if len(skipped) > SKIP_LINES_PRINTED:
        lines.append(f"And {len(skipped) - SKIP_LINES_PRINTED} more skipped, listed in {HEALTH_CHECK_FILE}.")
    if result.left_out_by_scene:
        lines.append(f"Left out: {plural(result.left_out_by_scene, 'line')} about whole-film records (this check "
                     "covers one scene; check --all shows them).")
    return lines


def update_manifest_after_check(project, result, command_line, record_files):
    """The manifest after a check: the IDs of omitted records (ID-04), the last check and fresh fingerprints of the
    record files (the tidy fixes changed some); then the locked records as the checker saw them (FORM-11)."""
    manifest = project.read_manifest()
    omitted = list(manifest.get("omitted_ids") or [])
    for key, record in result.run.index.items():
        if key[1] and CheckRun.is_omitted(record) and key[1] not in omitted:
            omitted.append(key[1])
    manifest["omitted_ids"] = omitted
    counts = result.counts
    manifest["last_check"] = {"time": datetime.datetime.now().isoformat(timespec="seconds"), "command": command_line,
                              "errors": counts.get("E", 0), "warnings": counts.get("W", 0),
                              "notes": counts.get("N", 0), "tidy_fixes": len(result.tidy_notes)}
    project.refresh_manifest(manifest, record_files)
    project.write_manifest(manifest)
    write_locked_records(project.folder, next_locked_records(result, read_locked_records(project.folder),
                                                             project.schema))


def set_checker_last_run(project, keep_old_copy):
    """--all: PROJECT.checker_last_run gets today's date (00 Start here shows it). Returns True if it changed.
    keep_old_copy(path, name) keeps the file's old version in history/ first (once per run)."""
    path = project.folder / START_HERE
    if not path.is_file():
        return False
    record_file = parse_file(path, START_HERE, project.schema)
    record = next((record for record in record_file.records if record.type_name == "PROJECT"), None)
    if record is None or record.get("checker_last_run") == today():
        return False
    keep_old_copy(path, START_HERE)
    record.set_field("checker_last_run", today(), project.schema)
    write_file(record_file, path, project.schema)
    return True


class UnitView:
    """check --unit (C7): the records one unit wrote, and the records they cite."""

    def __init__(self, unit, labels, cited):
        self.unit = unit
        self.labels = labels
        self.cited = cited

    @classmethod
    def for_unit(cls, project_folder, identifier, context):
        from .make_handout import Workspace, unit_from_identifier, unit_records
        workspace = Workspace(project_folder, context.schema, context.words, context.constants)
        unit = unit_from_identifier(workspace, identifier)
        if unit.kind != "ai":
            raise StageStop(f"{identifier} is not a unit the AI writes, so it has no records to check; run stage.py "
                            "check --step N.")
        keys = unit_records(workspace, unit)
        labels = {key[1] or key[0] for key in keys}
        if unit.step == 8 and unit.scene:
            # the scene's last batch also answers for the checks of the whole scene (the light the story writes,
            # the time against the list, the suspense holds), which run once every batch is written
            from .make_handout import plan_batches
            batches = plan_batches(workspace, unit.scene)
            if batches and batches[-1][0] == unit.identifier:
                labels |= {unit.scene, f"{unit.scene}-LIST"}
        cited = set()
        known = {key[1] for key in workspace.index if key[1]}
        for key in keys:
            record = workspace.index.get(key)
            if record is None:
                continue
            for line in record.fields:
                for token in re.findall(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+(?:\.S\d{2})?", line.value or ""):
                    if token in known and token not in labels:
                        cited.add(token)
        return cls(unit, labels, cited)

    def split(self, problems):
        """(the unit's own problems, errors on the records it cites, how many other lines were left out)."""
        own, cited, others = [], [], 0
        for problem in problems:
            label = (getattr(problem, "record", "") or "").strip('"')
            if label in self.labels:
                own.append(problem)
            elif label in self.cited and getattr(problem, "level", "") == "E" and \
                    getattr(problem, "check_id", "") != "FORM-05":
                cited.append(problem)
            else:
                others += 1
        return own, cited, others


def scope_line_for(result):
    """"Scope: 3 of 30 scenes ..." when PROJECT.scope names some scenes (C19), else ""."""
    try:
        from .project_files import scope_words
        return scope_words(result.run.index)
    except (ImportError, AttributeError):
        return ""


def run_check(context):
    """check [--step N] [--scene SCnn] [--film] [--all] [--story <path>]: run the checks on the project.

    Exit (7.3): 0 when no error line was printed, 1 when error lines were printed; a missing story file, a bad
    step or scene stops with exit 2 (StageStop) before anything is written."""
    arguments = context.arguments
    step = read_step(getattr(arguments, "step", None))
    scene = read_scene(getattr(arguments, "scene", None))
    film = bool(getattr(arguments, "film", False))
    all_checks = bool(getattr(arguments, "all", False)) or (step is None and not film)
    if getattr(arguments, "all", False) and step is not None:
        raise StageStop("Give either --all or --step N, not both: --all runs every check, --step N the checks of "
                        "one step.")
    project = Project(context.project, context.schema, context.words)
    unit_view = None
    if getattr(arguments, "unit", None):
        if step is not None or film or getattr(arguments, "all", False):
            raise StageStop("Give --unit alone: it checks one unit's records with the checks of the unit's own step.")
        unit_view = UnitView.for_unit(project.folder, arguments.unit, context)
        step = unit_view.unit.step
        scene = scene or (unit_view.unit.scene if step in (7, 8) else None)
        all_checks = False
    story_path = getattr(arguments, "story", None)
    if story_path:
        if not Path(story_path).is_file():
            raise StageStop(f'The story file "{Path(story_path).name}" was not found. Give the path of the story file.')
        story = StorySource.from_file(story_path, context.constants)
    else:
        story = StorySource.from_project(project.folder)
    command_line = command_line_of(arguments)
    with project.lock():
        record_files = project.load_record_files()
        manifest = project.read_manifest()
        baseline = locked_baseline_from_lines(read_locked_records(project.folder), context.schema)
        result = run_checks(record_files, context.schema, context.words, context.constants, story=story,
                            manifest=manifest, step=step, scene=scene, film=film, tidy=True, project=project,
                            locked_baseline=baseline)
        not_due = []
        cited_lines = []
        left_to_others = 0
        if unit_view is not None:
            result.problems, cited_lines, left_to_others = unit_view.split(result.problems)
            try:  # what a later unit of this step will write is not yet due here either
                from .make_handout import Workspace, not_yet_due
                result.problems, not_due = not_yet_due(Workspace(project.folder, context.schema, context.words,
                                                                 context.constants), step, result.problems)
            except StageStop:
                not_due = []
        elif step is not None and not film:
            try:
                from .make_handout import Workspace, not_yet_due
                result.problems, not_due = not_yet_due(Workspace(project.folder, context.schema, context.words,
                                                                 context.constants), step, result.problems)
            except StageStop:
                not_due = []
        written = []
        history = []
        kept_names = set()

        def keep_old_copy(path, name):
            if name in kept_names:
                return
            if not history:
                history.append(history_run_folder(project))
            keep_in_history(history[0], path, name)
            kept_names.add(name)

        for record_file in record_files:
            if record_file.name not in result.changed_files:
                continue
            keep_old_copy(project.folder / record_file.name, record_file.name)
            write_file(record_file, project.folder / record_file.name, context.schema)
            written.append(record_file.name)
        changed_project = False
        if all_checks and step is None and scene is None and not film:
            changed_project = set_checker_last_run(project, keep_old_copy)
        health_written = write_health_check(project, result, step, scene, film, all_checks, story, command_line)
        counts = result.counts
        if written:
            names = ", ".join(re.sub(r"\.md$", "", name) for name in written)
            project.add_log_entry(f"Checked {what_was_checked(step, scene, film, all_checks)}: made "
                                  f"{plural(len(result.tidy_notes), 'small fix', 'small fixes')} of spelling, case or "
                                  f"spacing in {names}.")
        elif changed_project:
            project.add_log_entry(f"Checked everything: {plural(counts.get('E', 0), 'problem')}, "
                                  f"{plural(counts.get('W', 0), 'warning')}.")
        update_manifest_after_check(project, result, command_line, project.load_record_files())
    for line in printable_lines(result):
        context.say(line)
    if unit_view is not None:
        unit_name = unit_view.unit.identifier
        waiting_inbox = sorted(path.name for path in project.inbox_folder.glob("*.md")
                               if path.stem == unit_name or path.stem.startswith(f"{unit_name} - fix ")) \
            if project.inbox_folder.is_dir() else []
        if waiting_inbox:
            context.say(f"Note: {', '.join(waiting_inbox)} is still in the inbox, not applied (apply refused it, or "
                        "it was not run): this check read the records as they were before it. Fix it and apply it "
                        "first.")
        context.say(f"Checked only {unit_view.unit.identifier}'s {plural(len(unit_view.labels), 'record')}, with "
                    f"step {unit_view.unit.step + 1} of 12's checks and only the fields filled by then.")
        if cited_lines:
            context.say("About records it cites (fix them only if your records caused them; they do not count here):")
            for line in cited_lines[:NOTE_LINES_PRINTED]:
                context.say(str(line))
        if left_to_others:
            context.say(f"Left out: {plural(left_to_others, 'line')} about other units' records (check --all shows "
                        "them).")
    if not_due:
        context.say(f"Not yet due: {plural(len(not_due), 'line')} about what units of this step not yet written "
                    "will fill (never errors; they are listed in 13 Health check.md).")
    scope_line = scope_line_for(result)
    if scope_line:
        context.say(scope_line)
    if not result.checks_run and not result.checks_not_present:
        context.say("No check of the checker is listed for this step in steps.json, so nothing was checked.")
    for module_name, reason in result.families_broken.items():
        context.say(f"Could not load {module_name}: {reason}. Its checks did not run; report this line.")
    context.say(in_short_line(result, open_questions(result.run)))
    if health_written is None:
        context.say(f"Not written: {HEALTH_CHECK_FILE} is left as it was, because nothing was checked"
                    + (f"; tidied: {', '.join(written)}" if written else "") + ".")
    else:
        context.say(f"Written: {HEALTH_CHECK_FILE}" + (f"; tidied: {', '.join(written)}" if written else ""))
    context.summary = (f"{counts.get('E', 0)} errors, {counts.get('W', 0)} warnings, {counts.get('N', 0)} notes, "
                       f"{len(result.tidy_notes)} tidy fixes")
    return 1 if counts.get("E", 0) else 0


def register_commands(table):
    """stage.py's command table: check. (build is registered by derive_fields.py, and adopt, impact and
    questions by adopt_folder.py, each from its own module listed in stage.py's COMMAND_MODULES.)"""
    load_check_families()
    table.add("check", "Run the checks and write 13 Health check", run_check, add_check_arguments)
