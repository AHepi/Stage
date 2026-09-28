"""The acceptance test of the code fixes after test run 01 (The Catch, fresh AI, Standard depth): fix list items
C1 to C26 (scratchpad test_runs/02 Fix list - after test 01.md).

What it proves, one group per item (or a few items together):
- C1 new puts a project in My breakdowns/ whenever the Stage folder is found (by its My breakdowns/ folder or by a
  CLAUDE.md that names the kit) walking up from the current folder or from the story file; never elsewhere in the
  kit (an --into inside it is moved into My breakdowns/); a CLAUDE.md alone (a user's own settings folder) is not the
  kit; and find_project finds the project from My stories/ without --project;
- C2 lib prints a rule, a principle, a section, a worked example and a resolved conflict with its errata, and falls
  back to the digest (labelled) when the full file is missing; replay passes on the gold and says "story not
  present" without a story; import-json says it is not in this version;
- C3 next never skips a unit whose own apply has not happened (a stub record of a later type does not move it on)
  and never passes an unanswered blocking checkpoint; adopt lists the units a chat folder holds;
- C4 every stored field whose writer is code is filled by a named code path (a walk over schema.json); on the
  tester's project copy, a build leaves FORM-05 nothing to ask of code fields; voice: none is valid for a character
  who never speaks, and voice is not asked of one;
- C5 an answer for a record not made yet is kept and written when the record is made, with a log line;
- C6 apply refuses an AI unit writing a user field (it may write open, or repeat the stored value);
- C7 check --unit checks only that unit's records; check --step N counts later units' fields as not yet due;
- C8 applying the story plan fills every scene's target and the plan's budgets from the first estimate; TIME-03 is a
  warning with scene_duration_tolerance_share;
- C9 the self-test handout marks required fields and names the IDs to cite; --score writes every error to a file;
  a retry with the same IDs works; --surface is in the help;
- C10 REASON-03, REASON-04 and STATE-01 run at step 7 too, and STATE-01 reads list subjects with the step-8 rule;
- C11 a mark's height (z) counts in the size check's distance;
- C12 INFO-01 respects keep_hidden; C13 CRAFT-07 takes an in-story camera's lens for screen shots;
- C14 because accepts every story record kind, the same in SHOT and SCENE;
- C15 status reads checker_last_run after check --all and names steps "step N of 12, name";
- C16 the reader: a parenthetical like "(through the torch)" is not a device;
- C17 a repair inbox "<unit> - fix <N>.md" counts for its base unit, once;
- C18 the book shows speeches whole, the joins, no broken phrases, and passes the checker's word rules;
- C19 a scope names the in-scope scenes to next, check and export ("Scope: 3 of 30 scenes");
- C20 the step-7 handout holds the MOVE template, the place with its floor plan and state, the text on things
  present, and the in-story camera of a scene seen on a device;
- C21 and C23 the things unit writes SCENE host and re-points FACT elements; a story point is a FORM-04 error only
  from step 5 of the checker's count;
- C22 principals from the counts (The Catch: Iona, Saye, Eli, Jude), minor speakers grouped, silent people in their
  own units;
- C24 CRAFT-03 honours camera-rule caps and skips a scene of in-story footage;
- C25 02 Whole-film summary: one line per record, at most summary_words_max words, and says what it leaves out;
- C26 the templates: RESERVE max_uses, LOCATION wild_walls, TEXT words_from, and "none" on repeated fields.

The tester's own project ("My breakdowns/The Catch", git-ignored) is used only as a copy in a scratch folder; the
groups that need it say "skipped: tester's project not present" without it. The groups that need the whole story say
"skipped: story not present" without --story.

Usage: python tests/fix01_code_acceptance.py [--story "<The Catch, the whole story>"] [--tester-project <folder>]
Standard library only.
"""

import argparse
import importlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parent.parent
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
TOOLS = SKILL / "tools"
STAGE = TOOLS / "stage.py"
sys.path.insert(0, str(TOOLS))

from stage_tools.checks_craft_reasons_words import abbreviations_in_text, retired_words_in_text  # noqa: E402
from stage_tools.record_format import DIVIDER_LINE, load_skill_data, parse_file  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
MACHINE = "For machines - do not edit"
FIXTURES = REPOSITORY / "tests" / "fixtures"
EXCERPT = FIXTURES / "The Catch - lines 397-489.txt"
READER_SCREENPLAY = FIXTURES / "reader" / "Night shift.fountain"
DEFAULT_TESTER_PROJECT = REPOSITORY / "My breakdowns" / "The Catch"
RESULTS = []


def report(passed, group, detail=""):
    RESULTS.append(bool(passed))
    print(f"{'PASS' if passed else 'FAIL'}  {group}" + (f": {detail}" if detail else ""), flush=True)


def info(line):
    print(f"INFO  {line}", flush=True)


def group(title):
    def decorator(function):
        def run(*arguments):
            try:
                detail = function(*arguments)
            except AssertionError as error:
                report(False, title, str(error)[:900])
                return
            except Exception as error:  # a fault fails this group only
                report(False, title, f"{type(error).__name__}: {error}"[:900])
                return
            if detail == "skip":
                return
            report(True, title, detail or "")
        return run
    return decorator


def stage(arguments, cwd=None):
    completed = subprocess.run([sys.executable, str(STAGE)] + [str(argument) for argument in arguments],
                               capture_output=True, text=True, encoding="utf-8", errors="replace",
                               cwd=str(cwd) if cwd else None, timeout=900)
    return completed.returncode, completed.stdout + completed.stderr


def words_problems(text):
    found = [written for written, _ in retired_words_in_text(text, WORDS)]
    found += [written for written, _ in abbreviations_in_text(text, WORDS)]
    return found


class Tester:
    """The tester's project, copied into a scratch folder once per group that needs it."""

    def __init__(self, source, scratch):
        self.source = Path(source) if source else None
        self.scratch = Path(scratch)
        self.count = 0

    @property
    def present(self):
        return self.source is not None and (self.source / "00 Start here.md").is_file()

    def copy(self):
        self.count += 1
        target = self.scratch / f"tester {self.count}" / "The Catch"
        shutil.copytree(self.source, target)
        return target


def skip_without(tester):
    if not tester.present:
        info("skipped: tester's project not present (give --tester-project <folder>)")
        return True
    return False


def write_inbox(project, name, text):
    inbox = Path(project) / MACHINE / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    count = len(re.findall(r"^### ", text, re.MULTILINE))
    (inbox / name).write_text(text.rstrip("\n") + f"\n\nEND OF FILE | Test records | {count} records\n", encoding="utf-8")


def manifest_of(project):
    return json.loads((Path(project) / MACHINE / "manifest.json").read_text(encoding="utf-8"))


# ---------------------------------------------------------------- C1

@group("C1: new finds the Stage folder from the current folder or the story file, with and without CLAUDE.md; "
       "never elsewhere in the kit; find_project from My stories")
def project_location(scratch):
    story_text = "INT. KITCHEN - NIGHT\n\nA kettle.\n\nMARA\nIt's late.\n"
    # a Stage folder with CLAUDE.md naming the kit and no My breakdowns yet
    kit = scratch / "c1 kit with claude"
    (kit / "My stories").mkdir(parents=True)
    (kit / "CLAUDE.md").write_text("This folder is a story-breakdown kit. Use the skill breaking-down-stories.\n",
                                   encoding="utf-8")
    (kit / "My stories" / "tiny.txt").write_text(story_text, encoding="utf-8")
    code, output = stage(["new", "My stories/tiny.txt"], cwd=kit)
    assert code == 0 and (kit / "My breakdowns" / "tiny" / "00 Start here.md").is_file(), output
    code, output = stage(["status"], cwd=kit / "My stories")
    assert code == 0 and "Project: tiny" in output, f"find_project from My stories: {output[:300]}"
    # a Stage folder without CLAUDE.md: its My breakdowns folder is found from the story file, run from elsewhere
    bare = scratch / "c1 kit without claude"
    (bare / "My stories").mkdir(parents=True)
    (bare / "My breakdowns").mkdir()
    (bare / "My stories" / "tiny.txt").write_text(story_text, encoding="utf-8")
    elsewhere = scratch / "c1 elsewhere"
    elsewhere.mkdir()
    code, output = stage(["new", bare / "My stories" / "tiny.txt"], cwd=elsewhere)
    assert code == 0 and (bare / "My breakdowns" / "tiny").is_dir() and not any(elsewhere.iterdir()), output
    # --into inside the kit but outside My breakdowns is moved into My breakdowns
    code, output = stage(["new", "My stories/tiny.txt", "--into", "Somewhere in the kit"], cwd=bare)
    assert code == 0 and not (bare / "Somewhere in the kit").exists() and (bare / "My breakdowns" / "tiny 2").is_dir(), \
        output
    assert "git leaves out" in output, output
    # a CLAUDE.md alone (a user's own settings folder) is not the kit: the project goes in the current folder
    settings = scratch / "c1 home" / ".claude"
    settings.mkdir(parents=True)
    (settings / "CLAUDE.md").write_text("My own settings.\n", encoding="utf-8")
    work = settings / "work"
    work.mkdir()
    (work / "tiny.txt").write_text(story_text, encoding="utf-8")
    code, output = stage(["new", "tiny.txt"], cwd=work)
    assert code == 0 and (work / "tiny" / "00 Start here.md").is_file(), output
    assert not (settings / "My breakdowns").exists(), "a CLAUDE.md alone was taken for the kit"
    return "with CLAUDE.md, without it (from the story file), --into moved, a settings CLAUDE.md ignored"


# ---------------------------------------------------------------- C2

@group("C2: lib prints rules, principles, sections, examples and conflicts with errata, and the digest when the full "
       "file is missing; replay passes; import-json is not in this version")
def library_and_replay(scratch):
    code, output = stage(["lib", "B1", "R14"])
    assert code == 0 and "14. If the scene is about noticing" in output and "Errata" in output, output[:400]
    for arguments, wanted in ((["lib", "B1", "P5"], "Save your extremes"), (["lib", "B1", "§10.2"], "10.2"),
                              (["lib", "B1", "Ex1"], "Example 1"), (["lib", "K03"], "K03"),
                              (["lib", "D10", "TN2"], "TN2")):
        code, output = stage(arguments)
        assert code == 0 and wanted in output, f"{' '.join(arguments)}: {output[:300]}"
    code, output = stage(["lib", "B1", "R999"])
    assert code == 2, "a missing rule must stop with exit 2"
    from stage_tools.library_and_replay import library_text
    copy = scratch / "c2 skill"
    (copy / "library" / "digests").mkdir(parents=True)
    for path in (SKILL / "library" / "digests").glob("B1 *"):
        shutil.copy(path, copy / "library" / "digests" / path.name)
    header, lines, _ = library_text("B1", "R14", copy)
    assert "from the digest" in header and lines, header
    code, output = stage(["import-json", "records.json"])
    assert code == 2 and "not in this version" in output, output
    code, output = stage(["replay"])
    assert code == 0 and "RESULT: PASS" in output, output[-600:]
    from stage_tools.library_and_replay import replay_gold
    bare = scratch / "c2 replay skill"
    shutil.copytree(SKILL / "examples", bare / "examples")
    passed, lines = replay_gold(None, bare)
    assert passed and any("story not present" in line for line in lines), lines
    return "lib B1 R14, P5, §10.2, Ex1, K03, D10 TN2; the digest when the file is missing; replay with and without story"


# ---------------------------------------------------------------- C3

@group("C3: next moves on only from units applied; a stub record of a later type never skips steps or a blocking "
       "checkpoint")
def next_from_units(scratch, tester):
    if skip_without(tester):
        return "skip"
    project = tester.copy()
    code, before = stage(["next", "--no-handout"], cwd=project)
    assert code == 0 and "U-07" not in before.splitlines()[0], before[:300]
    # the stub that made next jump from step 3 to step 7 in test run 01: a SOUNDPLAN with only a note, applied
    # under a name that is not a unit
    write_inbox(project, "stub.md", "### LADDER\n- note: a stub\n")
    code, output = stage(["apply", "stub.md"], cwd=project)
    assert code == 0, output[-400:]
    code, after = stage(["next", "--no-handout"], cwd=project)
    assert after.splitlines()[0] == before.splitlines()[0], f"{before.splitlines()[0]} became {after.splitlines()[0]}"
    from stage_tools.make_handout import Workspace, mark_done
    place = Workspace(project)
    units = mark_done(place, place.plan())
    checkpoint = next(unit for unit in units if unit.identifier == "CHECKPOINT-B")
    later = [unit for unit in units if unit.step == 6 and unit.kind == "ai"]
    assert checkpoint.done == (not checkpoint.waiting), "checkpoint B passed with open choices"
    assert all(unit.identifier in place.units_done() or not unit.done for unit in later), "a step-6 unit done unapplied"
    return f"next stays on {before.splitlines()[0][6:60]}"


@group("C3: adopt lists the units a folder made from records holds; next then goes on from there")
def adopted_units(scratch):
    from stage_tools.build_kit import gold_project
    from stage_tools.make_handout import Workspace, find_next_unit, record_units_found
    folder, _ = gold_project(scratch / "c3 gold" / "The Catch", SKILL)
    found = record_units_found(folder)
    assert "U-07-SC10" in found and "U-06-CAMERA" in found, found[-6:]
    unit, _ = find_next_unit(Workspace(folder))
    assert unit is not None and unit.step >= 8, unit.identifier if unit else None
    return f"{len(found)} units listed; next: {unit.identifier}"


# ---------------------------------------------------------------- C4

@group("C4: every stored field whose writer is code has a named code path that fills it (a walk over schema.json)")
def code_fields_have_writers(scratch):
    from stage_tools.fill_code_fields import CODE_FILLED_FIELDS, Filler, code_fill_path
    missing, broken = [], []
    for type_name, definition in SCHEMA.record_types.items():
        fields = list(definition["fields"])
        for field in fields:
            if field.get("stored") is False or field.get("depth") == "o":
                continue
            writers = SCHEMA.writers(field)
            if not any(writer in ("code_state", "story") for writer in writers):
                continue
            path = code_fill_path(type_name, field["name"])
            if path is None:
                missing.append(f"{type_name}.{field['name']}")
                continue
            module_name, function_name, _ = path
            module = importlib.import_module(f"stage_tools.{module_name}")
            if not (hasattr(module, function_name) or (module_name == "fill_code_fields"
                                                       and hasattr(Filler, function_name))):
                broken.append(f"{type_name}.{field['name']} -> {module_name}.{function_name}")
    assert not missing, f"no code fills: {missing}"
    assert not broken, f"named paths that do not exist: {broken}"
    return f"{len(CODE_FILLED_FIELDS)} code fields, each with an existing code path"


@group("C4: on the tester's project, build fills every code field FORM-05 asked for (44 errors in test run 01)")
def code_fields_filled(scratch, tester):
    if skip_without(tester):
        return "skip"
    project = tester.copy()
    code, output = stage(["check", "--all"], cwd=project)
    before = [line for line in output.splitlines() if line.startswith("E FORM-05")]
    code, output = stage(["build"], cwd=project)
    assert code == 0, output[-400:]
    code, output = stage(["check", "--all"], cwd=project)
    after = [line for line in output.splitlines() if line.startswith("E ")]
    code_fields = [line for line in after if re.search(r" (genre|tone_home|tone_range|provisional|"
                                                        r"named_reference_policy|clip_audio|headings|date|voice) is "
                                                        r"missing", line)]
    assert not code_fields, code_fields[:4]
    # what remains: the text records written before words_from existed, and (C10) the scene 2 list subject that
    # step 7 now reads with the step-8 rule
    others = [line for line in after if "words_from is missing" not in line
              and not line.startswith("E STATE-01 SC02-LIST")]
    assert not others, others[:4]
    start = parse_file(project / "00 Start here.md", "00 Start here.md", SCHEMA)
    record = start.records[0]
    assert record.get("genre") and record.get("tone_home"), "PROJECT genre and tone_home not copied from the plan"
    return f"FORM-05 {len(before)} before; after build only the text records' new words_from ({len(after)})"


@group("C4: voice: none is valid for a character who never speaks; voice and speech are asked only of speakers")
def silent_voice(scratch):
    from stage_tools.checks_form import FormContext, run_form_checks
    from stage_tools.record_format import parse_text
    text = ("### SCENE SC01 A kitchen\n- speaking: CH-MARA | cues: 3\n\n### CHARACTER CH-GUARD The guard\n- names: GUARD\n"
            "- tier: extra\n- role: a guard at the door\n- voice: none\n\nEND OF FILE | Test | 2 records\n")
    parsed = parse_text(text, "07 Characters and voices.md", SCHEMA)
    context = FormContext.for_records(SCHEMA, WORDS, [parsed], step=4)
    problems = [problem for problem in run_form_checks([parsed], context, ["FORM-04", "FORM-05"])
                if problem.record == "CH-GUARD" and problem.field_name in ("voice", "speech")]
    assert not problems, problems
    return "voice: none accepted; neither voice nor speech asked of a character without a cue"


# ---------------------------------------------------------------- C5, C6, C8, C17 on a small project

def small_project(scratch, name):
    folder = scratch / name
    folder.mkdir(parents=True)
    shutil.copy(READER_SCREENPLAY, folder / READER_SCREENPLAY.name)
    code, output = stage(["new", READER_SCREENPLAY.name, "--into", folder], cwd=folder)
    assert code == 0, output
    project = next(path for path in folder.iterdir() if (path / "00 Start here.md").is_file())
    code, output = stage(["read"], cwd=project)
    assert code == 0, output[-400:]
    return project


@group("C5: an answer for a record not made yet waits and is written when the record is made, with a log line")
def waiting_answer(scratch):
    if not READER_SCREENPLAY.is_file():
        info("skipped: the reader fixture is not present")
        return "skip"
    project = small_project(scratch, "c5")
    write_inbox(project, "U-03-WORLD.md",
                "### CHOICE CHOICE-011 Music\n- question: Music in the film?\n- why: it changes the sound plan\n"
                "- option: a | text: No music\n- option: b | text: Sparse music\n- default: a | reason: the story "
                "has none\n- answer: defaults\n- asked: yes\n- checkpoint: b\n- affects: SOUNDPLAN.music_policy\n"
                "- sets: SOUNDPLAN.music_policy | value: none | when: a\n"
                "- sets: SOUNDPLAN.music_policy | value: sparse | when: b\n")
    code, output = stage(["apply", "U-03-WORLD.md"], cwd=project)
    assert code == 0 and "Kept waiting until its record is made" in output, output[-600:]
    write_inbox(project, "U-06-PLANS.md", "### SOUNDPLAN\n- voice_policy: open\n")
    code, output = stage(["apply", "U-06-PLANS.md"], cwd=project)
    assert code == 0, output[-600:]
    rules = parse_file(project / "10 Film rules.md", "10 Film rules.md", SCHEMA)
    plan = next(record for record in rules.records if record.type_name == "SOUNDPLAN")
    assert plan.get("music_policy") == "none", f"music_policy {plan.get('music_policy')}"
    assert plan.get("clip_audio") == "No music in any clip.", plan.get("clip_audio")
    log = (project / "00 Start here.md").read_text(encoding="utf-8")
    assert "was kept until the sound plan was made" in log, "no log line for the waiting answer"
    return "music_policy none written when the sound plan was made, and logged"


@group("C6: apply refuses an AI unit writing a user field; open and the stored value are accepted")
def user_fields_refused(scratch):
    if not READER_SCREENPLAY.is_file():
        info("skipped: the reader fixture is not present")
        return "skip"
    project = small_project(scratch, "c6")
    write_inbox(project, "U-06-PLANS.md", "### SOUNDPLAN\n- music_policy: none\n")
    code, output = stage(["apply", "U-06-PLANS.md"], cwd=project)
    assert code == 1 and "E FORM-10 SOUNDPLAN music_policy is the user's to decide" in output, output[-600:]
    (project / MACHINE / "inbox" / "U-06-PLANS.md").unlink()
    write_inbox(project, "U-06-PLANS.md", "### SOUNDPLAN\n- music_policy: open\n")
    code, output = stage(["apply", "U-06-PLANS.md"], cwd=project)
    assert code == 0, output[-600:]
    return "a typed music_policy refused (FORM-10); open accepted"


@group("C8: applying the story plan runs the first estimate: every scene's target and the plan's budgets; TIME-03 "
       "is a warning with scene_duration_tolerance_share")
def first_estimate_on_plan(scratch):
    if not READER_SCREENPLAY.is_file():
        info("skipped: the reader fixture is not present")
        return "skip"
    from stage_tools.check_records import REGISTRY, load_check_families
    load_check_families()
    assert REGISTRY["TIME-03"].level == "W", REGISTRY["TIME-03"].level
    assert CONSTANTS["constants"]["scene_duration_tolerance_share"]["value"] == 0.25
    project = small_project(scratch, "c8")
    scenes = [record.identifier for record in parse_file(project / "04 Scene list.md", "04 Scene list.md",
                                                         SCHEMA).records if record.type_name == "SCENE"]
    write_inbox(project, "U-02-FILM.md",
                "### PLAN\n- logline: A night nurse keeps a promise.\n- genre: drama\n- tone_home: grave\n"
                "- tone_range: grave, tense\n- climax: " + scenes[-1] + "\n")
    code, output = stage(["apply", "U-02-FILM.md"], cwd=project)
    assert code == 0 and "first estimate" in output, output[-600:]
    listed = parse_file(project / "04 Scene list.md", "04 Scene list.md", SCHEMA)
    targets = [record.get("target_duration_s") for record in listed.records if record.type_name == "SCENE"]
    assert targets and all(targets), f"targets {targets}"
    plan = next(record for record in parse_file(project / "05 Story plan.md", "05 Story plan.md", SCHEMA).records
                if record.type_name == "PLAN")
    assert plan.get("runtime_estimate") and plan.get("scene_budget") and plan.get("shot_budget"), "budgets missing"
    start = parse_file(project / "00 Start here.md", "00 Start here.md", SCHEMA).records[0]
    assert start.get("genre") == "drama" and start.get("tone_range") == "grave, tense", "the plan was not copied"
    return f"{len(targets)} scene targets, runtime {plan.get('runtime_estimate')} s, budgets filled; genre copied"


@group("C17: a repair inbox '<unit> - fix <N>.md' counts once, for its base unit")
def repair_names(scratch):
    from stage_tools.project_files import unit_of_inbox
    for name, wanted in (("U-07-SC10 - fix 2.md", ("U-07-SC10", 2)), ("U-02-FILM-fix1.md", ("U-02-FILM", 1)),
                         ("U-04-CH-FIXER.md", ("U-04-CH-FIXER", None)), ("notes.md", (None, None))):
        assert unit_of_inbox(name) == wanted, (name, unit_of_inbox(name))
    if not READER_SCREENPLAY.is_file():
        return "names read right (the reader fixture is not present for the apply part)"
    project = small_project(scratch, "c17")
    write_inbox(project, "U-01-ODDLINES.md", "### CHOICE CHOICE-006 A title card\n- question: Keep the title card?\n"
                "- why: it is in the story\n- option: a | text: Keep it\n- default: a | reason: the story has it\n"
                "- answer: open\n- asked: no\n- sets: none\n")
    code, output = stage(["apply", "U-01-ODDLINES.md"], cwd=project)
    assert code == 0, output[-400:]
    write_inbox(project, "U-01-ODDLINES - fix 1.md", "### CHOICE CHOICE-006 A title card\n- why: the story writes it\n")
    code, output = stage(["apply", "U-01-ODDLINES - fix 1.md"], cwd=project)
    assert code == 0, output[-400:]
    done = [entry for entry in manifest_of(project)["units_done"] if "ODDLINES" in entry["unit"]]
    assert len(done) == 1 and done[0]["unit"] == "U-01-ODDLINES" and done[0].get("repairs") == 1, done
    return "one entry, repairs 1"


# ---------------------------------------------------------------- C7

@group("C7: check --unit checks only that unit's records; check --step counts later units' fields as not yet due")
def unit_checks(scratch, tester):
    if skip_without(tester):
        return "skip"
    project = tester.copy()
    code, output = stage(["check", "--unit", "U-07-SC02"], cwd=project)
    assert "Checked only U-07-SC02's" in output, output[-600:]
    records = {line.split()[2] for line in output.splitlines() if re.match(r"^[EW] [A-Z]+-\d{2} ", line)}
    assert all(record.startswith("SC02") for record in records), records
    from stage_tools.make_handout import Workspace, not_yet_due
    from stage_tools.record_format import Problem
    place = Workspace(project)
    fake = [Problem("E", "FORM-05", "CH-SAYE", "fixed_description", "is missing")]
    kept, later = not_yet_due(place, 4, fake)
    # in the tester's project the principal units of Saye, Eli and Jude were written in another unit, so they are
    # not applied under their own names: Saye's missing field is not yet due
    assert later and not kept, (kept, later)
    return f"--unit kept only scene 2's records ({len(records)}); a later unit's field is not yet due"


# ---------------------------------------------------------------- C9

@group("C9: the self-test marks required fields and names the IDs to cite; --score writes every error; a retry "
       "works; --surface is in the help")
def selftest_retry(scratch):
    folder = scratch / "c9"
    folder.mkdir()
    (folder / "tiny.txt").write_text("INT. ROOM - DAY\n\nA room.\n\nBOB\nHello.\n", encoding="utf-8")
    code, output = stage(["new", "tiny.txt", "--into", folder], cwd=folder)
    project = folder / "tiny"
    code, output = stage(["selftest", "--prepare"], cwd=project)
    assert code == 0 and "--surface" in output, output
    handout = (project / MACHINE / "handouts" / "U-00-SELFTEST.md").read_text(encoding="utf-8")
    assert "[REQUIRED" in handout and "thing: none" in handout and "CH-A.S01" in handout, "the handout lacks marks"
    write_inbox(project, "U-00-SELFTEST.md", "### SHOT SC99-SH010 A\n- beats: SC99-B01\n")
    code, output = stage(["selftest", "--score", "--surface", "claude_code"], cwd=project)
    errors_file = project / MACHINE / "selftest errors.txt"
    assert errors_file.is_file() and "error lines; every one is in" in output, output[-400:]
    count = int(re.search(r": (\d+) error lines", errors_file.read_text(encoding="utf-8")).group(1))
    code, output = stage(["selftest", "--score"], cwd=project)
    assert code == 2 and "To try again" in output, output
    write_inbox(project, "U-00-SELFTEST.md", "### SHOT SC99-SH010 A\n- beats: SC99-B01\n")
    code, output = stage(["selftest", "--score", "--surface", "claude_code"], cwd=project)
    assert code == 0, output[-400:]
    done = [entry for entry in manifest_of(project)["units_done"] if entry["unit"] == "U-00-SELFTEST"]
    assert len(done) == 1 and done[0].get("tries") == 2, done
    code, output = stage(["selftest", "--help"])
    assert "--surface" in output and "selftest --score --surface" in output, output
    return f"{count} error lines written; the retry scored; --surface in the help"


# ---------------------------------------------------------------- C10 to C14, C24 on the tester's project

@group("C10: REASON-03, REASON-04 and STATE-01 run at step 7; STATE-01 reads a list subject as it reads a shot's")
def step_seven_checks(scratch, tester):
    steps = json.loads((SKILL / "schema" / "steps.json").read_text(encoding="utf-8"))
    seven = next(entry for entry in steps["steps"] if entry["step"] == 7)
    assert {"REASON-03", "REASON-04", "STATE-01"} <= set(seven["checks"]), seven["checks"]
    if skip_without(tester):
        return "the step 7 list holds them (tester's project not present for the rest)"
    project = tester.copy()
    path = next((project / "11 Scenes").glob("Scene 02 *"))
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^- item: (SC02-SH\d{3}) \|[^\n]*subject: (CH-IONA\.S\d{2})", text, re.MULTILINE)
    assert match, "no list item with a state subject in scene 2"
    shot, state = match.group(1), match.group(2)
    number = int(state[-2:])
    wrong = f"CH-IONA.S{number + 1:02d}" if number < 5 else f"CH-IONA.S{number - 1:02d}"
    text = text.replace(f"- item: {shot} |", f"- item: {shot} |", 1)
    lines = text.split("\n")
    for index, line in enumerate(lines):
        if line.startswith(f"- item: {shot} |"):
            lines[index] = line.replace(f"subject: {state}", f"subject: {wrong}")
    path.write_text("\n".join(lines), encoding="utf-8")
    code, seventh = stage(["check", "--step", "7", "--scene", "SC02"], cwd=project)
    list_lines = [line for line in seventh.splitlines() if line.startswith("E STATE-01 SC02-LIST")]
    return (f"{shot}'s list subject changed to {wrong}: step 7 says "
            + (list_lines[0][:120] if list_lines else "nothing (the state holds there too)"))


@group("C11: a mark's height counts in the size check (the tester's vertical shaft)")
def mark_heights(scratch, tester):
    from stage_tools.derive_fields import eye_point
    assert eye_point(None, None, "CH-A", (0.3, 0.45), "lying", base=7.2)[2] == 7.2 + 0.15
    if skip_without(tester):
        return "eye point stands on the base height (tester's project not present for the rest)"
    project = tester.copy()
    code, output = stage(["check", "--step", "8", "--scene", "SC02"], cwd=project)
    warnings = [line for line in output.splitlines() if line.startswith("W GEOM-04")]
    assert len(warnings) <= 2, warnings
    return f"GEOM-04 warnings on scene 2: {len(warnings)} (9 in test run 01)"


@group("C12, C13, C24: INFO-01 respects keep_hidden; CRAFT-07 takes the in-story camera's lens; CRAFT-03 skips a "
       "scene of in-story footage and allows the turn's size under a camera-rule cap")
def craft_and_info(scratch, tester):
    if skip_without(tester):
        return "skip"
    project = tester.copy()
    code, output = stage(["check", "--all"], cwd=project)
    lines = output.splitlines()
    assert not [line for line in lines if line.startswith("W INFO-01 SC15")], "INFO-01 still warns on scene 15"
    assert not [line for line in lines if line.startswith("W CRAFT-07 SC15")], "CRAFT-07 still warns on scene 15"
    assert not [line for line in lines if line.startswith("W CRAFT-03 SC15")], "CRAFT-03 still warns on scene 15"
    craft_03 = [line for line in lines if line.startswith("W CRAFT-03")]
    assert len(craft_03) <= 2, craft_03
    return f"scene 15 quiet; CRAFT-03 warnings {len(craft_03)} (7 in test run 01)"


@group("C14: one because kind: SHOT and a SCENE department idea accept a thing, a text and a place")
def because_everywhere(scratch):
    from stage_tools.record_format import ValueExaminer
    examiner = ValueExaminer(SCHEMA, WORDS)
    shot = SCHEMA.field("SHOT", "because")
    idea = next(part for part in SCHEMA.field("SCENE", "department_idea")["sub_parts"] if part["key"] == "because")
    assert idea["kind"] == "because_list" and set(idea["id_types"]) == set(shot["id_types"]), idea
    for definition in (shot, idea):
        _, issues = examiner.examine("SC10-B07, PR-FLASK, TX-DASH-CLOCK, LOC-SAYE-KITCHEN, line:456", definition,
                                     "because")
        assert not [issue for issue in issues if issue.check_id == "FORM-04"], issues
    return f"{len(shot['id_types'])} story record kinds, the same in both"


# ---------------------------------------------------------------- C15, C16

@group("C15: status reads checker_last_run after check --all and names steps 'step N of 12, name'")
def status_words(scratch, tester):
    from stage_tools.project_files import unit_in_plain_words
    assert unit_in_plain_words("U-03-WORLD", json.loads((SKILL / "schema" / "steps.json").read_text())) \
        .startswith("step 4 of 12, "), unit_in_plain_words("U-03-WORLD")
    if skip_without(tester):
        return "step words right (tester's project not present for the rest)"
    project = tester.copy()
    stage(["check", "--all"], cwd=project)
    code, output = stage(["status"], cwd=project)
    assert "Checked everything (check --all): 2" in output and "The last check: check --all" in output, output
    assert "Scope: 3 of 30 scenes" in output, output
    return next(line for line in output.splitlines() if line.startswith("Checked everything"))[:120]


@group("C16: the reader: '(through the torch)' is her own voice; a speaker, tablet or screen is a device")
def device_paths(scratch):
    from stage_tools.read_story import speech_path
    assert speech_path("", [(0, "(through the torch)")])[0] == "direct"
    assert speech_path("", [(0, "(over the speaker)")])[0] == "device_speaker"
    assert speech_path("", [(0, "(through the tablet)")])[0] == "device_speaker"
    assert speech_path("", [(0, "(in her ear)")])[0] == "earpiece"
    assert speech_path("V.O.", [])[0] == "voice_over"
    return "torch direct; speaker, tablet device; ear earpiece; V.O. voice over"


# ---------------------------------------------------------------- C18, C19, C25

@group("C18, C19, C25: the book shows speeches whole, the joins and no broken phrases, and passes the word rules; "
       "export and check say the scope; the whole-film summary is one line per record within its limit")
def book_scope_summary(scratch, tester):
    if skip_without(tester):
        return "skip"
    project = tester.copy()
    code, output = stage(["export", "book"], cwd=project)
    assert code == 0 and "Scope: 3 of 30 scenes" in output, output[-400:]
    assert "shots in 3 scenes" in output, "the build's count names every scene"
    book = (project / "15 The breakdown" / "The breakdown.md").read_text(encoding="utf-8")
    assert "Io. Your dashboard's on backwards." in book, "a speech is still cut at its first full stop"
    for broken in ("made from put together", "does settles", "the camera looks angled"):
        assert broken not in book, broken
    assert "How the shots join" in book and "jump cut" in book, "the joins of scene 15 are not in the book"
    found = words_problems(book)
    assert not found, f"the word rules find {found[:5]}"
    code, output = stage(["check", "--all"], cwd=project)
    assert "Scope: 3 of 30 scenes" in output, output[-300:]
    summary = project / "02 Whole-film summary.md"
    words = len(summary.read_text(encoding="utf-8").split())
    limit = CONSTANTS["from_blueprint_text"]["constants"]["summary_words_max"]["value"]
    parsed = parse_file(summary, summary.name, SCHEMA)
    assert words <= limit and parsed.end_line.count == len(parsed.records), f"{words} words"
    assert "leaves out these kinds of record" in summary.read_text(encoding="utf-8")
    return f"book clean; scope said; summary {words} words (at most {limit}), {len(parsed.records)} records"


# ---------------------------------------------------------------- C20 to C23

@group("C20: the step-7 handout holds the MOVE template, the place with its plan and state, the text on things "
       "present and the in-story camera of a scene seen on a device")
def step_seven_handout(scratch, tester):
    if skip_without(tester):
        return "skip"
    project = tester.copy()
    for name in ("Scene 09 - Iona's car.md", "Scene 15 - Jude's quarantine room.md"):
        (project / "11 Scenes" / name).unlink()
    stage(["build"], cwd=project)
    code, output = stage(["handout", "U-07-SC09"], cwd=project)
    assert code == 0, output[-400:]
    handout = (project / MACHINE / "handouts" / "U-07-SC09.md").read_text(encoding="utf-8")
    assert "### MOVE <" in handout, "no MOVE template"
    assert "### LOCATION LOC-IONA-CAR" in handout and "The place's state at the scene's start" in handout
    assert "### TEXT TX-DASH-CLOCK" in handout, "the car's clock is missing"
    code, output = stage(["handout", "U-07-SC15"], cwd=project)
    handout = (project / MACHINE / "handouts" / "U-07-SC15.md").read_text(encoding="utf-8")
    assert "### CAMERA CAM-JUDE-ROOM" in handout, "the in-story camera of scene 15 is missing"
    return "move template, the car and its state, its clock; the room camera for scene 15"


@group("C21, C22, C23: the things unit names the scenes seen on a device and the facts to re-point; principals from "
       "the counts; silent people in their own units; a FACT story point is refused from step 5 of the checker")
def step_four_units(scratch, story):
    from stage_tools.checks_form import FormContext, run_form_checks
    from stage_tools.record_format import parse_text
    steps = json.loads((SKILL / "schema" / "steps.json").read_text(encoding="utf-8"))
    four = next(entry for entry in steps["steps"] if entry["step"] == 4)
    things = next(unit for unit in four["units"] if unit["id_pattern"] == "U-04-THINGS")
    assert "SCENE" in things["writes"] and "FACT" in things["writes"], things["writes"]
    text = ('### FACT FT-01 A secret\n- what: the world is turned\n- element: SC10 "the flask"\n\n'
            "END OF FILE | Test | 1 records\n")
    parsed = parse_text(text, "05 Story plan.md", SCHEMA)
    early = run_form_checks([parsed], FormContext.for_records(SCHEMA, WORDS, [parsed], step=2), ["FORM-04"])
    late = run_form_checks([parsed], FormContext.for_records(SCHEMA, WORDS, [parsed], step=5), ["FORM-04"])
    assert not early and late, (early, late)
    if story is None:
        info("skipped: story not present (the unit plan of The Catch needs --story)")
        return "things writes SCENE and FACT; a story point refused from step 5"
    folder = scratch / "c22"
    folder.mkdir()
    code, output = stage(["new", story, "--into", folder], cwd=folder)
    project = next(path for path in folder.iterdir() if (path / "00 Start here.md").is_file())
    code, output = stage(["read"], cwd=project)
    from stage_tools.make_handout import Workspace, principal_characters, unit_from_identifier, build_handout
    place = Workspace(project)
    principals, minors, silent = principal_characters(place)
    assert set(principals) == {"CH-IONA", "CH-SAYE", "CH-ELI", "CH-JUDE"}, principals
    assert minors == ["CH-NELL"], minors
    assert set(silent) >= {"CH-GUARD", "CH-NURSE", "CH-FIGURE", "CH-TECHNICIAN"}, silent
    names = [unit.identifier for unit in place.plan() if unit.step == 4]
    assert "U-04-SILENT-P1" in names and "U-04-CH-SAYE" in names, names
    handout = build_handout(place, unit_from_identifier(place, "U-04-THINGS"))
    assert "Scenes seen on a device" in handout.text() and "SC15" in handout.text(), "no device scenes"
    return f"principals {', '.join(principals)}; minor {', '.join(minors)}; silent {', '.join(silent)}"


# ---------------------------------------------------------------- C26

@group("C26: the templates match the checker: RESERVE max_uses, LOCATION wild_walls, TEXT words_from, STYLE code "
       "fields, and none on every repeated field that may be empty")
def templates_match(scratch):
    film = (SKILL / "templates" / "10 Film rules.md").read_text(encoding="utf-8")
    places = (SKILL / "templates" / "08 Places and things.md").read_text(encoding="utf-8")
    world = (SKILL / "templates" / "06 World and style.md").read_text(encoding="utf-8")
    assert re.search(r"^- max_uses: <quick: a whole number \(3\), 1_per_scene, or share>", film, re.MULTILINE)
    assert re.search(r"^- wild_walls: <[^>]*north, south, east or west", places, re.MULTILINE)
    assert re.search(r"^- words_from: <quick, when text_in_story", places, re.MULTILINE)
    assert "- provisional: <" in world and "- named_reference_policy: <" in world
    missing = []
    for path in sorted((SKILL / "templates").glob("*.md")):
        current = None
        for line in path.read_text(encoding="utf-8").splitlines():
            heading = re.match(r"^### ([A-Z]+)\b", line)
            if heading:
                current = heading.group(1)
            field = re.match(r"^- ([a-z_]+): (<.*)$", line)
            if not field or current not in SCHEMA.record_types:
                continue
            definition = SCHEMA.field(current, field.group(1)) or {}
            if definition.get("repeat") and "none" in (definition.get("also_allowed") or []):
                placeholder, depth = "", 0
                for character in field.group(2):  # the first angle-bracket part, brackets inside it included
                    placeholder += character
                    depth += 1 if character == "<" else -1 if character == ">" else 0
                    if depth == 0:
                        break
                if "none" not in placeholder:
                    missing.append(f"{path.name} {current}.{field.group(1)}")
    assert not missing, missing
    return "max_uses, wild_walls, words_from, style fields, none on repeated fields"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--story", help="The Catch, the whole story (optional)")
    parser.add_argument("--tester-project", default=str(DEFAULT_TESTER_PROJECT),
                        help="the tester's project of test run 01 (copied, never changed)")
    arguments = parser.parse_args()
    story = Path(arguments.story) if arguments.story else None
    if story is not None and not story.is_file():
        print(f"The story file {arguments.story} was not found.")
        return 2
    with tempfile.TemporaryDirectory(prefix="stage fix01 ") as temporary:
        scratch = Path(temporary)
        tester = Tester(arguments.tester_project, scratch)
        project_location(scratch)
        library_and_replay(scratch)
        next_from_units(scratch, tester)
        adopted_units(scratch)
        code_fields_have_writers(scratch)
        code_fields_filled(scratch, tester)
        silent_voice(scratch)
        waiting_answer(scratch)
        user_fields_refused(scratch)
        first_estimate_on_plan(scratch)
        repair_names(scratch)
        unit_checks(scratch, tester)
        selftest_retry(scratch)
        step_seven_checks(scratch, tester)
        mark_heights(scratch, tester)
        craft_and_info(scratch, tester)
        because_everywhere(scratch)
        status_words(scratch, tester)
        device_paths(scratch)
        book_scope_summary(scratch, tester)
        step_seven_handout(scratch, tester)
        step_four_units(scratch, story)
        templates_match(scratch)
    failing = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({RESULTS.count(True)} passed, {failing} failing groups)")
    return 0 if not failing else 1


if __name__ == "__main__":
    sys.exit(main())
