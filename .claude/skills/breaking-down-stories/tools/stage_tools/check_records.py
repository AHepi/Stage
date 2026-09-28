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

1. Write the module in stage_tools/, for example stage_tools/checks_coverage_time_state.py, and add nothing
   anywhere else: CHECK_FAMILY_MODULES below already lists every planned family module, and a module that is
   not there yet is skipped (its checks are reported as "not in this copy of the tools").

       stage_tools.checks_form                  FORM-01 to FORM-13 (WP2; registered here by an adapter)
       stage_tools.checks_ids_citations         ID-01 to ID-09, CITE-01 to CITE-07 (WP4b)
       stage_tools.checks_coverage_time_state   COVER, TIME and STATE
       stage_tools.checks_sides_geometry        SIDE and GEOM (WP4a)
       stage_tools.checks_craft_reasons_words   CRAFT, INFO, REASON and WORDS
       stage_tools.checks_plan_generation_film  PLAN, GEN and FILM

2. In the module, register one function per check ID with the decorator register_check:

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

   - level is the level of 7.2 ("E", "W", "N", or "E/W" when the check can print either).
   - build is 1 or 2 (7.2's Build column).
   - title is 7.2's "Check" column, for maintainers.
   - plain says what is wrong in plain words for the plain part of 13 Health check. It follows a record's plain
     name ("Scene 10, shot 150 <plain>."), so it starts with a verb and never holds a code, an ID or an
     abbreviation (WORDS-04): "has a shot shorter than the time its speech and pauses need".
   - The function takes one CheckRun (below) and returns a list of record_format.Problem lines. Build each line
     with run.problem(...), which fills in the file and line of the record's first copy. A check may return
     plain strings too, but then the report cannot place them in a file.
   - When a check cannot run (no story, a scene not in the excerpt), call run.skip(check_id, "why") and
     return what it could check. A skip is not a problem line: it is listed separately ("Skipped: ...").
   - A check must never change records. Tidy fixes are made by the runner (FORM-13) before the checks run.
   - A check only reads; run.cache is a dict for sharing work between checks of one run.

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
       run.scope_scenes                        the scenes in PROJECT.scope, or None when the scope is all
       run.in_scope(ID or record)              True when it belongs to no scene or to a scene being checked
       run.scene_ids()                         the SCENE records' IDs, in file order
       run.scene_range("SC10")                 (first, last) lines of a scene: its SCENE record, else the story
       run.chapter_range("CP01")               (first, last) lines of a chapter
       run.story                               StorySource or None (the numbered story; see the class)
       run.story_missing("CITE-02")            True (and one skip line) when no story is present
       run.speeches                            {speech ID: speeches.json entry}, or {} when not present
       run.manifest                            the project's manifest.json, or {} (for example the batches)
       run.batch_shots("SC10")                 during step 8: the set of listed shot IDs whose batches were
                                               written so far; None means "check every list item" (use it for
                                               ID-07 and COVER-02 to COVER-04, 7.2)
       run.form_context                        checks_form.FormContext for the same files (conditions, choices)
       run.problem(level, check_id, record, field, what, fix="", line_number=None)
       run.skip(check_id, why)
       scene_of("SC10-SH150") -> "SC10"        (module function)

   The runner drops problem lines of records outside the checked scenes (PROJECT.scope and --scene), removes
   exact duplicates, and orders them by check, then file, then line.

4. Checks that must also run on an inbox before apply merges it: register them with
   project_files.register_apply_check(function(project, inbox, current_files, context)) at import time of the
   family module. check_records imports every family module when stage.py starts, so apply sees them.

5. Other modules may add a section to the plain part of 13 Health check (quality scores, the three scenes to
   read) with register_report_section(function(project, result) -> list of plain lines, or []).

WHAT THE CHECK COMMAND DOES
===========================
check [--step N] [--scene SCnn] [--film] [--all] [--story <path>]
- --step N runs the checks steps.json lists for step N; FORM-05 then asks only for fields filled by step N or
  earlier. --all (and no option at all) runs every registered check and asks for every field. --film runs the
  FILM checks and TIME-07 (step 9). --scene keeps only the problems of that scene's records and files.
- --story <path> reads the story (or a Stage excerpt) from that file for the CITE checks, instead of the
  project's story map.json and speeches.json. Without any story the CITE checks say "skipped: story not present".
- Tidy fixes (FORM-13) are made in the record files and logged; the old files go to history/.
- 13 Health check.md gets a new plain part (first line "In short: ..."), its REVIEW and FINDING records are
  kept, and the checker's lines are written below the divider. --all also sets PROJECT.checker_last_run.
- manifest.json keeps the IDs of omitted records (omitted_ids, for ID-04) and the last check (last_check).
"""

import datetime
import importlib
import json
import re
from dataclasses import dataclass, field as dataclass_field
from pathlib import Path

from .record_format import (DEPTH_RANK, DIVIDER_LINE, EndLine, Problem, Record, TextBlock, count_levels,
                            load_json, merge_copies, normalise_word, parse_file, parse_line_numbers,
                            parse_quote_anchor, render_file, split_item, split_list, write_file)
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
    """Import every family module that exists, so that its checks (and apply checks) are registered."""
    if _FAMILIES_LOADED["done"]:
        return _FAMILIES_LOADED
    for module_name in CHECK_FAMILY_MODULES:
        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError as error:
            if error.name == module_name:
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

        def adapter(run, form_function=function):
            return form_function(run.record_files, run.form_context)
        adapter.__module__ = checks_form.__name__
        register_function(check_id, adapter, level, 1, title, plain, "FORM")


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
    file_name = getattr(problem, "file_name", None) or ""
    match = SCENE_FILE_NUMBER.match(file_name)
    if match:
        return "SC" + match.group(1)
    return None


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
                 film=False, project=None, form_context=None):
        self.record_files = list(record_files)
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
        value = scene.get("lines") if scene is not None and scene.type_name == "SCENE" else None
        if value:
            numbers = parse_line_numbers(value)
            if numbers:
                result = (numbers[0][0], numbers[-1][1])
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
        if batches and all((entry or {}).get("received") is not None
                           and (entry or {}).get("received", 0) >= (entry or {}).get("expected", 0)
                           for entry in batches.values()):
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
               film=False, check_ids=None, tidy=False, project=None):
    """Run the chosen checks on parsed record files and return a CheckResult.

    tidy=True makes the FORM-13 tidy fixes in the records first (the caller writes the changed files); the
    FORM-13 lines are the fixes made. The other checks then read the tidied records.
    """
    from .checks_form import FORM_CHECKS, FormContext, apply_tidy_fixes
    result = CheckResult()
    families = load_check_families()
    result.families_broken = dict(families["broken"])
    definitions, missing = select_checks(step, film, check_ids)
    result.checks_not_present = missing
    form_context = FormContext.for_records(schema, words, record_files, step=step)
    wanted_ids = {definition.check_id for definition in definitions}
    if "FORM-13" in wanted_ids or tidy:
        result.tidy_notes = FORM_CHECKS["FORM-13"](record_files, form_context)
    if tidy:
        before = {record_file.name: render_file(record_file, schema) for record_file in record_files}
        apply_tidy_fixes(record_files, form_context)
        result.changed_files = [record_file.name for record_file in record_files
                                if render_file(record_file, schema) != before[record_file.name]]
        form_context = FormContext.for_records(schema, words, record_files, step=step)
    run = CheckRun(record_files, schema, words, constants, story=story, manifest=manifest, step=step, scene=scene,
                   film=film, project=project, form_context=form_context)
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
    kept = []
    seen = set()
    for problem in problems:
        text = str(problem)
        if text in seen:
            continue
        seen.add(text)
        if not run.scene_checked(scene_of_problem(problem)):
            continue
        kept.append(problem)
    kept.sort(key=lambda problem: (order.get(getattr(problem, "check_id", ""), len(order)),
                                   file_order.get(getattr(problem, "file_name", None), len(file_order)),
                                   getattr(problem, "line_number", None) or 0))
    result.problems = kept
    result.skipped = list(run.skipped)
    for check_id in missing:
        result.skipped.append((check_id, "not in this copy of the tools yet"))
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
        inner = re.match(r"^(SH|SU|B|P|V|D|M|C)(\d+)(?:\.(\d+))?$", rest)
        if inner:
            kind, number, clip = inner.groups()
            if kind == "SU":
                index = int(number) - 1
                letter = chr(ord("A") + index) if 0 <= index < 26 else number
                return f"{scene_words}, camera {letter}"
            words = f"{scene_words}, {SUFFIX_WORDS[kind]} {plain_number(number)}"
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
    if record is not None and record.type_name in TYPE_WORDS:
        return TYPE_WORDS[record.type_name]
    if record is not None and record.title:
        prefix = NAMED_TYPE_WORDS.get(record.type_name, "")
        return f"{prefix} {record.title}".strip()
    return plain_words_from_code(label)


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
        where = name
    elif file_name:
        where = f"{file_name}, {name}"
    else:
        where = name
    where = where[:1].upper() + where[1:]
    return f"- {where}: {plain}."


def plural(count, word, plural_word=None):
    return f"{count} {word if count == 1 else (plural_word or word + 's')}"


def in_short_line(result, needs_you):
    """The report's first line (step 10): 'In short: 2 things need you, 14 small fixes I made, 3 warnings'."""
    counts = result.counts
    needs = "nothing needs you" if needs_you == 0 else \
        (f"{plural(needs_you, 'thing')} {'needs' if needs_you == 1 else 'need'} you")
    fixes = len(result.tidy_notes)
    warnings = counts.get("W", 0)
    parts = [needs, f"{plural(fixes, 'small fix', 'small fixes')} I made" if fixes else "no small fixes needed",
             plural(warnings, "warning") if warnings else "no warnings"]
    if counts.get("E", 0):
        parts.append(f"{plural(counts['E'], 'problem')} still to fix")
    return "In short: " + ", ".join(parts) + "."


def open_questions(run):
    """Choices waiting for the user: asked, still open (the things that need the user)."""
    count = 0
    for choice in run.records("CHOICE"):
        if normalise_word(choice.get("status") or "open") == "open" and normalise_word(choice.get("asked") or "no") == "yes":
            count += 1
    return count


def what_was_checked(step, scene, film, all_checks):
    parts = []
    if step is not None:
        parts.append(f"the checks for step {step + 1} of 12" if isinstance(step, int) and step <= 11 else f"step {step}")
    if film:
        parts.append("the whole film")
    if not parts:
        parts.append("everything")
    if scene:
        parts.append(f"scene {plain_number(scene[2:]) if scene[2:].isdigit() else scene[2:]} only")
    return ", ".join(parts)


def health_check_plain_part(project, result, step, scene, film, all_checks, story):
    """The plain part of 13 Health check.md, first line 'In short: ...' (step 10, 13.3). Plain words only."""
    run = result.run
    lines = [in_short_line(result, open_questions(run)), "", f"# {HEALTH_CHECK_TITLE}", ""]
    stamp = datetime.datetime.now()
    lines.append(f"Checked: {what_was_checked(step, scene, film, all_checks)}, on "
                 f"{stamp.day} {stamp.strftime('%B %Y')} at {stamp.strftime('%H:%M')}.")
    scene_ids = [identifier for identifier in run.scene_ids()]
    total = len(scene_ids)
    if story is not None and story.scene_count():
        total = max(total, story.scene_count())
    if run.scope_scenes is not None and total:
        in_scope = len([identifier for identifier in run.scope_scenes if re.fullmatch(r"SC\d{2,3}[A-Z]?", identifier)])
        if in_scope < total:
            lines.append(f"Scope: {in_scope} of {total} scenes.")
    if story is None:
        lines.append("The story's own words were not compared: the numbered story is not in this folder yet.")
    lines.append("")
    errors = [problem for problem in result.problems if getattr(problem, "level", "") == "E"]
    warnings = [problem for problem in result.problems if getattr(problem, "level", "") == "W"]
    lines.append("## What to fix first")
    lines.append("")
    if errors:
        for problem in errors[:PLAIN_LINES_LISTED]:
            lines.append(plain_problem_line(problem, run))
        if len(errors) > PLAIN_LINES_LISTED:
            lines.append(f"- And {len(errors) - PLAIN_LINES_LISTED} more, listed below the line for the AI.")
    else:
        lines.append("Nothing: no problem was found.")
    lines.append("")
    lines.append("## Warnings")
    lines.append("")
    if warnings:
        for problem in warnings[:PLAIN_LINES_LISTED]:
            lines.append(plain_problem_line(problem, run))
        if len(warnings) > PLAIN_LINES_LISTED:
            lines.append(f"- And {len(warnings) - PLAIN_LINES_LISTED} more, listed below the line for the AI.")
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
        lines.append(f"{plural(len(result.skipped), 'check')} could not run in full; the reasons are below the line "
                     "for the AI. Nothing is wrong because of this.")
    for section in REPORT_SECTIONS:
        try:
            extra = section(project, result) or []
        except Exception:
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


def checker_lines_block(result, command_line):
    """The checker's own lines, below the divider: for the AI, with IDs and codes."""
    lines = ["## The checker's lines", "", f"Command: {command_line}"]
    counts = result.counts
    lines.append(f"Counts: {counts.get('E', 0)} errors, {counts.get('W', 0)} warnings, {counts.get('N', 0)} notes; "
                 f"{len(result.checks_run)} checks run.")
    if result.problems:
        lines.append("")
        lines.extend(str(problem) for problem in result.problems)
    if result.skipped:
        lines.append("")
        lines.extend(f"Skipped {check_id}: {why}" for check_id, why in result.skipped)
    lines.append("")
    return lines


def write_health_check(project, result, step, scene, film, all_checks, story, command_line):
    """Write 13 Health check.md: a new plain part and checker lines; its REVIEW and FINDING records are kept."""
    path = project.folder / HEALTH_CHECK_FILE
    plain = health_check_plain_part(project, result, step, scene, film, all_checks, story)
    block = TextBlock()
    for line in plain + [DIVIDER_LINE, ""] + checker_lines_block(result, command_line):
        block.lines.append(line)
        block.line_numbers.append(None)
    if path.is_file():
        record_file = parse_file(path, HEALTH_CHECK_FILE, project.schema)
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


# ---------------------------------------------------------------- the command

def add_check_arguments(parser):
    parser.add_argument("--step", help="check as at the end of this step (0 to 11): only fields filled by then")
    parser.add_argument("--scene", help="report only this scene's records, for example SC10")
    parser.add_argument("--film", action="store_true", help="run the whole-film checks (step 9)")
    parser.add_argument("--all", action="store_true", help="run every check and ask for every field (the default)")
    parser.add_argument("--story", help="read the story from this file for the checks that compare story words")


def read_step(text):
    if text is None:
        return None
    value = str(text).strip()
    if not re.fullmatch(r"\d{1,2}", value) or int(value) > 16:
        raise StageStop(f'The step "{text}" is not a step number. Give a number from 0 to 11, as --step 8.')
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
    return " ".join(parts)


def printable_lines(result):
    """The lines check prints: every error and warning, the first notes and skips, then a count of the rest."""
    lines = [str(problem) for problem in result.problems if getattr(problem, "level", "") in ("E", "W")]
    notes = [str(problem) for problem in result.problems if getattr(problem, "level", "") == "N"]
    lines.extend(notes[:NOTE_LINES_PRINTED])
    if len(notes) > NOTE_LINES_PRINTED:
        lines.append(f"And {len(notes) - NOTE_LINES_PRINTED} more notes, listed in {HEALTH_CHECK_FILE}.")
    skipped = [f"Skipped {check_id}: {why}" for check_id, why in result.skipped]
    lines.extend(skipped[:SKIP_LINES_PRINTED])
    if len(skipped) > SKIP_LINES_PRINTED:
        lines.append(f"And {len(skipped) - SKIP_LINES_PRINTED} more skipped, listed in {HEALTH_CHECK_FILE}.")
    return lines


def update_manifest_after_check(project, result, command_line):
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
    project.write_manifest(manifest)


def set_checker_last_run(project, history_folder):
    """--all: PROJECT.checker_last_run gets today's date (00 Start here shows it). Returns True if it changed.
    history_folder() gives the history folder for this run; the old file is kept there first."""
    path = project.folder / START_HERE
    if not path.is_file():
        return False
    record_file = parse_file(path, START_HERE, project.schema)
    record = next((record for record in record_file.records if record.type_name == "PROJECT"), None)
    if record is None or record.get("checker_last_run") == today():
        return False
    keep_in_history(history_folder(), path, START_HERE)
    record.set_field("checker_last_run", today(), project.schema)
    write_file(record_file, path, project.schema)
    return True


def run_check(context):
    """check [--step N] [--scene SCnn] [--film] [--all] [--story <path>]: run the checks on the project."""
    arguments = context.arguments
    step = read_step(getattr(arguments, "step", None))
    scene = read_scene(getattr(arguments, "scene", None))
    film = bool(getattr(arguments, "film", False))
    all_checks = bool(getattr(arguments, "all", False)) or (step is None and not film)
    project = Project(context.project, context.schema, context.words)
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
        result = run_checks(record_files, context.schema, context.words, context.constants, story=story,
                            manifest=manifest, step=step, scene=scene, film=film, tidy=True, project=project)
        written = []
        history = []

        def history_folder():
            if not history:
                history.append(history_run_folder(project))
            return history[0]

        for record_file in record_files:
            if record_file.name not in result.changed_files:
                continue
            keep_in_history(history_folder(), project.folder / record_file.name, record_file.name)
            write_file(record_file, project.folder / record_file.name, context.schema)
            written.append(record_file.name)
        changed_project = False
        if all_checks and step is None and scene is None and not film:
            changed_project = set_checker_last_run(project, history_folder)
        write_health_check(project, result, step, scene, film, all_checks, story, command_line)
        update_manifest_after_check(project, result, command_line)
        counts = result.counts
        if written:
            names = ", ".join(re.sub(r"\.md$", "", name) for name in written)
            project.add_log_entry(f"Checked {what_was_checked(step, scene, film, all_checks)}: made "
                                  f"{plural(len(result.tidy_notes), 'small fix', 'small fixes')} of spelling, case or "
                                  f"spacing in {names}.")
        elif changed_project:
            project.add_log_entry(f"Checked everything: {plural(counts.get('E', 0), 'problem')}, "
                                  f"{plural(counts.get('W', 0), 'warning')}.")
    for line in printable_lines(result):
        context.say(line)
    for module_name, reason in result.families_broken.items():
        context.say(f"Could not load {module_name}: {reason}")
    context.say(in_short_line(result, open_questions(result.run)))
    context.say(f"Written: {HEALTH_CHECK_FILE}" + (f"; tidied: {', '.join(written)}" if written else ""))
    context.summary = (f"{counts.get('E', 0)} errors, {counts.get('W', 0)} warnings, {counts.get('N', 0)} notes, "
                       f"{len(result.tidy_notes)} tidy fixes")
    return 1 if counts.get("E", 0) else 0


def register_commands(table):
    """stage.py's command table: check. (build, impact and questions are planned for this slot; a builder who
    writes them registers them from their own module, listed in stage.py's COMMAND_MODULES.)"""
    load_check_families()
    table.add("check", "Run the checks and write 13 Health check", run_check, add_check_arguments)
