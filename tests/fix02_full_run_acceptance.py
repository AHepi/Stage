"""The acceptance test of the fixes after the full run on The Catch (Project notes 31, problems 1 to 18, and the
smaller items; the fixes are written up in Project notes 32).

What it proves, one group per problem (or a few problems together), on small fixtures only: copies of the WP12a gold
(examples/01 and 02, scene 10), the scene 10 excerpt (tests/fixtures), the reader fixture, and short texts written
here. No group reads a whole story.
- P1 a jump cut after a shot numbered 010 to 090 is found (the CUT's number keeps its zeros);
- P2 FORM-08 never judges code's own text (a checker finding's fix), and "as before" in a sentence is English; the
  film pass writes no "..." into what it stores, and rewrites the old wording; an output code made (the book) stays
  fresh when only plain parts are rewritten, and goes stale when a record changes, so next can say finished;
- P4 a shot list's approved mark is not asked for before its group of shots passes; --checkpoint-passed with nothing
  waiting carries on as next does;
- P5 a scene's split into parts is decided once;
- P6 a handout over its ceiling leaves out the example, then puts read-only records in brief, before any card part;
  the scoring handout gives each review in brief; a shot handout lists the speeches with their cue and word lines,
  the lens family in force and leaves out the gold when the unit is the gold's own scene;
- P7 a check that checks nothing leaves 13 Health check as it was; a partial check keeps the full check's plain
  part; the scores are said in plain words;
- P8 CRAFT-03 follows the film's ladder: a deliberate wide rung is kept, earlier shots are held to the rung;
- P9 light words are read in their sentence; a light the scene's look carries, at rest, needs no cue, a light
  that changes or moves does; a planned silence, a room-sound silence and light that quotes the script's light
  are not added changes, while a rupture planned elsewhere in the scene or a quote without a light word excuse
  nothing;
- P10 the time floor counts text to read and owes a beat's pause once; TIME-03 measures the shots against the list;
- P11 INFO-01 accepts a shot that says how it keeps the fact hidden;
- P12 STATE-01 reads a recording's state where it was recorded, and its fix names the missing state as an addition;
- P13 retired words only in their retired senses; a place's "bullet scars" is no body scar; "left palm" is not the
  dressed palm; an insert shows a sided feature only when its words name it; a black in the middle of a scene keeps
  its number;
- P14 word swaps made everywhere, once; sounds are not re-described places; model_drawn text is allowed;
- P15 the step files say the rules the checker enforces;
- P16 "- field: none" clears a stored field, notes sent on an existing record are kept, and apply names the next
  command as the handout does (build first at steps 7 and 8);
- P17 a non-human character is recognised and not held to a person's timing;
- P18 the last steps are written down; one film length, "with titles and credits";
- the blueprint's kill rule counts only real layout mistakes; the book names the one-of-a-kind records in plain
  words; ID-02 waits for a choice's record; CITE-03 reads a speech across a stage direction; GEOM-05 knows when an
  object arrives; status says "0 of" and lists a left-over repair apart; quote_for_message cuts between words; a
  place's own word outweighs a shared one; a common-word name is found only as a name.

Usage: python tests/fix02_full_run_acceptance.py
Standard library only.
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace

REPOSITORY = Path(__file__).resolve().parent.parent
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
TOOLS = SKILL / "tools"
STAGE = TOOLS / "stage.py"
sys.path.insert(0, str(TOOLS))

from stage_tools.check_records import CheckRun, StorySource, load_check_families, run_checks  # noqa: E402
from stage_tools.derive_fields import breakdown_for_run  # noqa: E402
from stage_tools.record_format import DIVIDER_LINE, load_skill_data, parse_file, parse_text  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
MACHINE = "For machines - do not edit"
FIXTURES = REPOSITORY / "tests" / "fixtures"
EXCERPT = FIXTURES / "The Catch - lines 397-489.txt"
READER_SCREENPLAY = FIXTURES / "reader" / "Night shift.fountain"
GOLD_FILES = {"scene": SKILL / "examples" / "01 The Catch - scene 10.md",
              "context": SKILL / "examples" / "02 The Catch - scene 10 - context.md"}
BLUEPRINT = REPOSITORY / "Project notes" / "13 Blueprint - how Stage is built.md"
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


# ---------------------------------------------------------------- the gold, and named edits to a copy of it

def gold_texts():
    return {name: path.read_text(encoding="utf-8") for name, path in GOLD_FILES.items()}


def record_block(lines, heading):
    """(first, end) line indexes of the record '### <heading> ...' (end is the first line after it)."""
    for index, line in enumerate(lines):
        if line == f"### {heading}" or line.startswith(f"### {heading} "):
            end = index + 1
            while end < len(lines) and not lines[end].startswith(("### ", "## ", "END OF FILE")) \
                    and lines[end] != DIVIDER_LINE:
                end += 1
            return index, end
    raise AssertionError(f"no record {heading}")


def edit(texts, name, record, find=None, replace=None, add_after=None, remove=False):
    """One edit to a copy of the gold: replace text inside a record, add a record after it, or remove it."""
    lines = texts[name].split("\n")
    first, end = record_block(lines, record)
    if remove:
        del lines[first:end]
    elif add_after is not None:
        while end > 0 and not lines[end - 1].strip():
            end -= 1
        lines[end:end] = [""] + add_after.rstrip("\n").split("\n")
    else:
        block = "\n".join(lines[first:end])
        assert find in block, f"{record} does not hold {find!r}"
        lines[first:end] = block.replace(find, replace, 1).split("\n")
    texts[name] = "\n".join(lines)
    return texts


def parsed(texts):
    return [parse_text(texts["scene"], GOLD_FILES["scene"].name, SCHEMA),
            parse_text(texts["context"], GOLD_FILES["context"].name, SCHEMA)]


def excerpt_story():
    return StorySource.from_file(EXCERPT, CONSTANTS) if EXCERPT.is_file() else None


def checked(texts, check_ids, story=True, step=None, manifest=None):
    result = run_checks(parsed(texts), SCHEMA, WORDS, CONSTANTS, story=excerpt_story() if story else None,
                        step=step, manifest=manifest, check_ids=check_ids)
    assert not result.crashed, f"crashed: {result.crashed}"
    return result


def lines_of(result, check_id, record=None):
    return [problem for problem in result.problems if problem.check_id == check_id
            and (record is None or problem.record == record)]


def check_run(texts, story=True):
    return CheckRun(parsed(texts), SCHEMA, WORDS, CONSTANTS, story=excerpt_story() if story else None)


def gold_breakdown(texts=None, story=True):
    run = check_run(texts or gold_texts(), story)
    return run, breakdown_for_run(run)


def gold_command_project(scratch, name):
    """A project made from the gold, with the units its records hold listed (as build-kit makes the example)."""
    from stage_tools.build_kit import gold_project
    from stage_tools.make_handout import record_units_found
    folder, _ = gold_project(scratch / name / "The Catch", SKILL)
    record_units_found(folder)
    return folder


def manifest_path(project):
    return Path(project) / MACHINE / "manifest.json"


def read_manifest(project):
    return json.loads(manifest_path(project).read_text(encoding="utf-8"))


def write_manifest(project, data):
    manifest_path(project).write_text(json.dumps(data, indent=1) + "\n", encoding="utf-8")


def write_inbox(project, name, text):
    inbox = Path(project) / MACHINE / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    count = len(re.findall(r"^### ", text, re.MULTILINE))
    path = inbox / name
    path.write_text(text.rstrip("\n") + f"\n\nEND OF FILE | Test records | {count} records\n", encoding="utf-8")
    return path


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


def above_divider(text):
    return text.split(DIVIDER_LINE, 1)[0]


# ---------------------------------------------------------------- P1

@group("P1: a jump cut after a shot numbered below 100 is found (SC10-SH070 is followed by SC10-C070)")
def jump_cut_numbers(scratch):
    from stage_tools.checks_sides_geometry import cut_after
    texts = edit(gold_texts(), "scene", "SHOT SC10-SH070", add_after=(
        "### CUT SC10-C070 A jump cut\n- to: SC10-SH080\n- type: jump_cut\n- why: The story jumps.\n"))
    run, breakdown = gold_breakdown(texts, story=False)
    shot = run.record("SC10-SH070")
    found = cut_after(breakdown, shot)
    assert found is not None and found.identifier == "SC10-C070", f"cut after SH070: {found}"
    last = cut_after(breakdown, run.record("SC10-SH200"))
    assert last is not None and last.identifier == "SC10-C200", f"cut after SH200: {last}"
    assert cut_after(breakdown, run.record("SC10-SH060")) is None
    return "SC10-C070 after shot 070, SC10-C200 after shot 200, none after shot 060"


# ---------------------------------------------------------------- P2

@group("P2: FORM-08 leaves a checker finding's own text alone and still judges the AI's; 'as before' inside a "
       "sentence is English, alone or opening a value it is a shortening")
def shortening_markers(scratch):
    from stage_tools.checks_form import FormContext, run_form_checks

    def form_08(text, name):
        record_file = parse_text(text, name, SCHEMA)
        context = FormContext.for_records(SCHEMA, WORDS, [record_file])
        return [problem for problem in run_form_checks([record_file], context, ["FORM-08"])]
    finding = ("### FINDING FIND-005 The ladder\n- record: SC06-SH120\n- rule: FILM-01\n- evidence: size close_up\n"
               "- fix: add to the story plan 'peak: tightest_size | reason: ...' quoting why the story peaks here.\n"
               "- source: {source}\n- status: open\n\nEND OF FILE | Test | 1 records\n")
    by_code = form_08(finding.format(source="checker"), "12 Whole-film check.md")
    assert not by_code, f"code's own text judged: {by_code}"
    by_ai = form_08(finding.format(source="review"), "12 Whole-film check.md")
    assert by_ai and by_ai[0].field_name == "fix", f"the AI's '...' was not found: {by_ai}"
    sentence = ("### SHOT SC01-SH010 A shot\n- room_sound: the ship's hum goes on as before under the whole scene\n\n"
                "END OF FILE | Test | 1 records\n")
    alone = "### SHOT SC01-SH010 A shot\n- room_sound: as before\n\nEND OF FILE | Test | 1 records\n"
    opening = "### SHOT SC01-SH010 A shot\n- purpose: As before, the lamp on its hook.\n\nEND OF FILE | Test | 1 records\n"
    assert not form_08(sentence, "11 Scenes/SC01 A room.md"), "'as before' in a sentence was taken for a marker"
    assert form_08(alone, "11 Scenes/SC01 A room.md"), "'as before' alone was not taken for a marker"
    assert form_08(opening, "11 Scenes/SC01 A room.md"), "'As before, ...' opening a value was not taken for a marker"
    return "checker text skipped, review text judged; 'as before' in a sentence allowed, alone refused"


@group("P2: the film pass stores no '...' in its fixes, and a stored old wording is written afresh by check --film")
def film_pass_wording(scratch):
    from stage_tools import film_pass
    source = (TOOLS / "stage_tools" / "film_pass.py").read_text(encoding="utf-8")
    fixes = re.findall(r'f?"Fix: [^\n]*(?:\n\s+f?"[^\n]*)*', source)
    with_dots = [fix[:80] for fix in fixes if "..." in fix]
    assert fixes and not with_dots, f"fix texts with '...': {with_dots}"
    assert "..." not in film_pass.NEW_PEAK_WORDING and "..." in film_pass.OLD_PEAK_WORDING
    project = gold_command_project(scratch, "p2 film")
    whole = project / "12 Whole-film check.md"
    whole.write_text("# 12 Whole-film check\n\n" + DIVIDER_LINE + "\n\n### FINDING FIND-001 The ladder\n"
                     "- record: SC10-SH150\n- rule: FILM-01\n- evidence: size close_up is the film's tightest\n"
                     f"- fix: keep SC10 wider, or add to the story plan 'peak: tightest_size | scene: SC10 | "
                     f"{film_pass.OLD_PEAK_WORDING}\n- source: checker\n- status: open\n\n"
                     "END OF FILE | 12 Whole-film check | 1 records\n", encoding="utf-8")
    code, output = stage(["check", "--film", "--project", project])
    assert code in (0, 1), output[-600:]
    text = whole.read_text(encoding="utf-8")
    assert film_pass.OLD_PEAK_WORDING not in text and film_pass.NEW_PEAK_WORDING in text, text[-900:]
    assert not re.search(r"^E FORM-08", output, re.MULTILINE), output[-600:]
    return f"{len(fixes)} fix texts without '...'; the stored old wording rewritten"


@group("P2: an output code made stays fresh when only plain parts change and goes stale when a record changes; "
       "report files never make the work look older")
def made_from_records(scratch):
    from stage_tools.make_handout import Workspace, newest_record_change
    from stage_tools.project_files import made_from_current_records
    project = gold_command_project(scratch, "p2 fresh")
    code, output = stage(["build", "--project", project])
    assert code == 0, output[-400:]
    code, output = stage(["export", "book", "--project", project])
    assert code == 0, output[-400:]
    book = "15 The breakdown/The breakdown.html"
    assert made_from_current_records(project, book) is True, "the book is not fresh just after export"
    rules = project / "10 Film rules.md"
    text = rules.read_text(encoding="utf-8")
    top, bottom = text.split(DIVIDER_LINE, 1)
    rules.write_text(top + "A plain line a build rewrote.\n\n" + DIVIDER_LINE + bottom, encoding="utf-8")
    assert made_from_current_records(project, book) is True, "a plain part made the book stale"
    before = newest_record_change(Workspace(project))
    time.sleep(1.1)
    health = project / "13 Health check.md"
    health.write_text(health.read_text(encoding="utf-8") if health.is_file() else "# 13 Health check\n",
                      encoding="utf-8")
    assert newest_record_change(Workspace(project)) == before, "a report file counted as a record change"
    rules.write_text(top + DIVIDER_LINE + bottom.replace("- default_move: static", "- default_move: static\n"
                                                         "- note: a changed record", 1), encoding="utf-8")
    assert made_from_current_records(project, book) is False, "a changed record left the book fresh"
    return "fresh after export and after a plain-part rewrite; stale after a record change; reports ignored"


# ---------------------------------------------------------------- P4

@group("P4: a shot list's approved mark is not asked for before its group passes, and is asked after; the advice "
       "names stage.py next")
def approval_not_due(scratch):
    from stage_tools.checks_form import FormContext, run_form_checks
    text = ("### SCENE SC01 A kitchen\n- lines: 1-20\n\n### SHOTLIST SC01-LIST The shot list\n"
            "- item: SC01-SH010 | beats: SC01-B01 | role: must_keep | size: medium | frame: single | subject: CH-MARA "
            "| time: 4 | shows: Mara at the kettle\n- status: draft\n\nEND OF FILE | Test | 2 records\n")

    def approved_lines(checkpoints):
        record_file = parse_text(text, "11 Scenes/SC01 A kitchen.md", SCHEMA)
        context = FormContext.for_records(SCHEMA, WORDS, [record_file], step=7)
        context.checkpoints = checkpoints
        return [problem for problem in run_form_checks([record_file], context, ["FORM-05"])
                if problem.record == "SC01-LIST" and problem.field_name == "approved"]
    assert not approved_lines({}), "approved asked for before the group passed"
    after = approved_lines({"CHECKPOINT-C-SC01": {"passed": "2026-09-30"}})
    assert after, "approved not asked for after the group passed"
    assert "stage.py next" in str(after[0]) and "build" not in str(after[0]).split("Fix:", 1)[1].split("(")[0], \
        str(after[0])
    return "not due before checkpoint C; due after, with advice to run stage.py next"


@group("P4: --checkpoint-passed with nothing waiting says so and carries on as next")
def checkpoint_nothing_waiting(scratch):
    project = gold_command_project(scratch, "p4 next")
    code, output = stage(["next", "--checkpoint-passed", "--no-handout", "--project", project])
    assert code == 0 and "No checkpoint was waiting" in output, output[-600:]
    return output.strip().splitlines()[0][:100]


# ---------------------------------------------------------------- P5

@group("P5: a scene's split into parts is decided once (the manifest's scene_splits, then the units applied)")
def split_once(scratch):
    from stage_tools.make_handout import Workspace, scene_is_big
    project = gold_command_project(scratch, "p5 split")
    manifest = read_manifest(project)
    manifest["scene_splits"] = {"SC10": True}
    write_manifest(project, manifest)
    assert scene_is_big(Workspace(project), "SC10") is True, "a split decided as parts was planned whole"
    manifest["scene_splits"] = {"SC10": False}
    write_manifest(project, manifest)
    assert scene_is_big(Workspace(project), "SC10") is False, "a scene decided whole was planned in parts"
    manifest.pop("scene_splits")
    manifest["units_done"] = [entry for entry in manifest.get("units_done", [])
                              if not str(entry.get("unit", "")).startswith("U-07-SC10")]
    manifest["units_done"].append({"unit": "U-07-SC10", "applied": "2026-09-30T10:00:00"})
    write_manifest(project, manifest)
    workspace = Workspace(project)
    workspace.constants = json.loads(json.dumps(workspace.constants))
    assert scene_is_big(workspace, "SC10") is False, "a scene designed whole was planned again in parts"
    return "kept as decided; a scene designed whole stays whole"


# ---------------------------------------------------------------- P6

@group("P6: over the ceiling a handout leaves out the example, then puts read-only records in brief, before any "
       "card part; the advice names only real splits")
def handout_fit_order(scratch):
    from stage_tools.make_handout import Handout, split_advice
    handout = Handout(unit=None, ceiling=1000, tokens_per_word=1.0, card_cap=100000)
    word = "word "
    handout.add("task", word * 200)
    handout.add("example", word * 400, kind="example", label="the example")
    handout.add("records", word * 800, kind="records", label="the records", trimmed_text=word * 100)
    handout.add("card", word * 300, kind="card", label="card 14 Questions in order")
    handout.fit()
    assert any("the example" in note for note in handout.left_out), handout.left_out
    assert any("in brief" in note for note in handout.left_out), handout.left_out
    assert not handout.card_parts_left_out, f"a card part left out first: {handout.card_parts_left_out}"
    assert handout.tokens() <= 1000 and not handout.too_big, handout.tokens()
    seven = SimpleNamespace(step=7, part=None, list_unit=False, scene="SC06")
    eight = SimpleNamespace(step=8, part=None, list_unit=False, scene="SC06")
    ten = SimpleNamespace(step=10, part=None, list_unit=False, scene=None)
    assert "U-07-SC06-P1" in split_advice(seven)
    assert "two replies" in split_advice(eight)
    assert "no smaller unit" in split_advice(ten)
    return f"example out, records in brief, card kept ({handout.tokens()} of 1000)"


@group("P6: the scoring handout gives each review in brief: its counts, every no answer, its scores")
def review_in_brief(scratch):
    from stage_tools.make_handout import review_summary
    text = ("### REVIEW RV-SC10 Scene 10\n- scope: SC10\n- answer: Q1 | answer: yes | evidence: SC10-SH150\n"
            "- answer: Q2 | answer: yes | evidence: SC10-SH190\n- answer: Q3 | answer: no | evidence: SC10-SH070 "
            "adds the lamp\n- score: 1 | score: 3 | evidence: every line covered\n\nEND OF FILE | Test | 1 records\n")
    review = parse_text(text, "13 Health check.md", SCHEMA).records[0]
    summary = review_summary(review)
    assert summary.startswith("RV-SC10 (scope SC10): 2 yes, 1 no"), summary
    assert "- no: Q3 | answer: no" in summary and "- score: 1 | score: 3" in summary, summary
    assert "Q1" not in summary, "a yes answer was given whole"
    return summary.splitlines()[0]


@group("P6: a shot handout lists the batch's speeches with cue and word lines and the lens family in force, and "
       "leaves out the gold for the gold's own scene")
def shot_handout(scratch):
    from stage_tools.make_handout import lens_family_in_force
    run, _ = gold_breakdown(story=False)
    camsys = run.record("CAMSYS")
    assert lens_family_in_force(camsys, "SC10") == ("35, 50", None), lens_family_in_force(camsys, "SC10")
    assert lens_family_in_force(camsys, "SC13") == ("35, 50, 85", "SC13"), lens_family_in_force(camsys, "SC13")
    if not EXCERPT.is_file():
        info("the handout part: skipped: story not present")
        return "the lens family after a step change"
    project = gold_command_project(scratch, "p6 handout")
    from stage_tools.project_files import Project
    from stage_tools.read_story import read_into_project
    read_into_project(Project(project, SCHEMA, WORDS), None, EXCERPT, write_records=False)
    manifest = read_manifest(project)
    manifest["units_done"] = [entry for entry in manifest.get("units_done", [])
                              if not str(entry.get("unit", "")).startswith("U-08-SC10")]
    write_manifest(project, manifest)
    code, output = stage(["handout", "U-08-SC10-B1", "--project", project])
    assert code == 0, output[-600:]
    path = project / MACHINE / "handouts" / "U-08-SC10-B1.md"
    if not path.is_file():
        found = sorted((project / MACHINE).rglob("U-08-SC10-B1*.md"))
        assert found, f"no handout written: {output[-400:]}"
        path = found[0]
    text = path.read_text(encoding="utf-8")
    assert re.search(r"SC10-D\d{2} \S+, cue line \d+", text), "no speech with its cue line"
    assert "35, 50" in text, "the lens family is not in the handout"
    assert "One example from the gold (The Catch, scene 10)" not in text, "the gold was given to the gold's own scene"
    from stage_tools.make_handout import Workspace, example_section
    unit = SimpleNamespace(step=8, scene="SC10", part=None, list_unit=False)
    assert "gold example is this very scene" in example_section(Workspace(project), unit)
    return f"speeches with cue lines, lens family 35, 50, no gold ({len(text.split())} words)"


# ---------------------------------------------------------------- P7

@group("P7: a check that checks nothing leaves 13 Health check as it was; a partial check keeps the full check's "
       "plain part")
def health_check_page(scratch):
    project = gold_command_project(scratch, "p7 health")
    code, output = stage(["check", "--all", "--project", project])
    assert code in (0, 1), output[-600:]
    health = project / "13 Health check.md"
    full = health.read_text(encoding="utf-8")
    assert re.search(r"^Checked: everything, on ", above_divider(full), re.MULTILINE), above_divider(full)[:600]
    code, output = stage(["check", "--step", "8", "--project", project])
    assert code in (0, 1), output[-600:]
    partial = health.read_text(encoding="utf-8")
    assert above_divider(partial) == above_divider(full), "a partial check rewrote the plain part"
    assert "check --step 8" in partial.split(DIVIDER_LINE, 1)[1], "the checker's lines were not replaced"
    from stage_tools.check_records import write_health_check
    empty = SimpleNamespace(checks_run=[], checks_not_present=[])
    assert write_health_check(SimpleNamespace(folder=project), empty, 11, None, False, False, None, "check") is None
    assert health.read_text(encoding="utf-8") == partial, "a check of nothing wrote the page"
    return "the full check's plain part kept; nothing written when nothing ran"


@group("P7: the quality scores are said in plain words: how many scenes pass, why one does not")
def scores_in_words(scratch):
    from stage_tools.check_records import quality_scores_plain_lines
    reviews = ("### REVIEW RV-SC10 Scene 10\n- scope: SC10\n" + "".join(
        f"- score: {number} | score: 3 | evidence: FIND-00{number}\n" for number in range(1, 11)) +
        "\n### REVIEW RV-SC11 Scene 11\n- scope: SC11\n" + "".join(
        f"- score: {number} | score: {1 if number == 3 else 2} | evidence: FIND-01{number}\n"
        for number in range(1, 11)) + "\nEND OF FILE | Test | 2 records\n")
    run = CheckRun([parse_text(reviews, "13 Health check.md", SCHEMA)], SCHEMA, WORDS, CONSTANTS)
    lines = quality_scores_plain_lines(run)
    text = "\n".join(lines)
    assert lines and lines[0] == "## Quality scores", lines[:2]
    assert "1 of 2 scenes pass" in text, text
    assert "scene 11 does not pass yet" in text.lower() and "shots that serve the beats" in text, text
    assert "RV-" not in text and "FIND-" not in text, "codes in the plain part"
    return lines[2][:110]


# ---------------------------------------------------------------- P8

@group("P8: CRAFT-03 follows the ladder: a deliberate wide rung is kept; a turn shot off its rung and an earlier "
       "shot tighter than the rung are warned")
def ladder_decides(scratch):
    load_check_families()
    base = lines_of(checked(gold_texts(), ["CRAFT-03"]), "CRAFT-03")
    assert not base, f"the gold warned: {base}"
    wide = edit(gold_texts(), "context", "LADDER", "size: close_up", "size: medium_wide")
    wide = edit(wide, "scene", "SHOT SC10-SH150", "- size: close_up", "- size: medium_wide")
    wide = edit(wide, "scene", "SHOTLIST SC10-LIST", "role: turn | size: close_up", "role: turn | size: medium_wide")
    found = lines_of(checked(wide, ["CRAFT-03"]), "CRAFT-03")
    assert not found, f"a deliberate wide turn was warned: {[str(problem) for problem in found]}"
    off = edit(gold_texts(), "context", "LADDER", "size: close_up", "size: medium_wide")
    found = lines_of(checked(off, ["CRAFT-03"]), "CRAFT-03", "SC10-SH150")
    assert found and "ladder" in str(found[0]), f"a turn off its rung: {[str(problem) for problem in found]}"
    tight = edit(gold_texts(), "scene", "SHOT SC10-SH120", "- size: medium_close_up", "- size: extreme_close_up")
    found = lines_of(checked(tight, ["CRAFT-03"]), "CRAFT-03", "SC10-SH120")
    assert found and "tighter than" in str(found[0]), f"an earlier shot tighter than the rung: {found}"
    return "wide rung kept; off-rung turn and tighter earlier shot warned"


# ---------------------------------------------------------------- P9

@group("P9: light words are read in their sentence: a person's colour and a fire door are not light")
def light_in_context(scratch):
    from stage_tools.derive_fields import light_words_in_context
    assert light_words_in_context("DR SAYE, fifties, grey and tidy, opens the door.", ["grey"]) == []
    assert light_words_in_context("Her grey hair falls loose.", ["grey"]) == []
    assert light_words_in_context("He shoulders through the fire door.", ["fire"]) == []
    assert light_words_in_context("She slams a fire shutter behind them.", ["fire"]) == []
    assert light_words_in_context("The sky outside goes grey.", ["grey"]) == ["grey"]
    assert light_words_in_context("The fire spreads along the ceiling.", ["fire"]) == ["fire"]
    return "person's colour and fire door left out; sky and fire kept"


@group("P9: a planned silence, a room-sound silence and light that quotes the script's light are not added changes; a "
       "rupture elsewhere in the scene and a quote without a light word excuse nothing")
def added_changes(scratch):
    from stage_tools.checks_craft_reasons_words import shot_light_sound_changes
    run = check_run(gold_texts())
    title = run.record("SC10-SH990")
    assert ("silence" in [field for field, _ in shot_light_sound_changes(run, title)]), \
        "an unplanned true silence was not counted"
    planned = edit(gold_texts(), "context", "SOUNDPLAN", "- rupture_plan: SC26 | device: drop_out, the ship's hum",
                   "- rupture_plan: SC26 | device: drop_out, the ship's hum\n"
                   "- rupture_plan: SC10 | device: true silence under the title")
    run = check_run(planned)
    assert "silence" not in [field for field, _ in shot_light_sound_changes(run, run.record("SC10-SH990"))], \
        "a silence the sound plan plans was counted"
    room = edit(gold_texts(), "scene", "SHOT SC10-SH990", "- silence: true_silence", "- silence: room_sound_only")
    run = check_run(room)
    assert "silence" not in [field for field, _ in shot_light_sound_changes(run, run.record("SC10-SH990"))], \
        "room_sound_only was counted"
    elsewhere = edit(gold_texts(), "context", "SOUNDPLAN", "- rupture_plan: SC26 | device: drop_out, the ship's hum",
                     "- rupture_plan: SC26 | device: drop_out, the ship's hum\n"
                     "- rupture_plan: SC10 | device: true silence under the title")
    elsewhere = edit(elsewhere, "scene", "SHOT SC10-SH030", "- silence: none", "- silence: true_silence")
    run = check_run(elsewhere)
    assert "silence" in [field for field, _ in shot_light_sound_changes(run, run.record("SC10-SH030"))], \
        "a rupture planned for the title excused a silence on another beat of the scene"
    if EXCERPT.is_file():
        lit = edit(gold_texts(), "scene", "SHOT SC10-SH030", "- light: as_look",
                   '- light: the lamp swings over the table, as the story writes "Iona holds the lamp."')
        run = check_run(lit)
        changes = shot_light_sound_changes(run, run.record("SC10-SH030"))
        assert "light" not in [field for field, _ in changes], f"light quoting the script's light was counted: {changes}"
        other = edit(gold_texts(), "scene", "SHOT SC10-SH030", "- light: as_look",
                     '- light: a hard red flash strobes across the table, as the story writes "Jude on the table."')
        run = check_run(other)
        assert "light" in [field for field, _ in shot_light_sound_changes(run, run.record("SC10-SH030"))], \
            "a quote with no light word in it excused an added light"
        own = edit(gold_texts(), "scene", "SHOT SC10-SH150", "- light: as_look", "- light: the lamp dims")
        run = check_run(own)
        assert "light" in [field for field, _ in shot_light_sound_changes(run, run.record("SC10-SH150"))]
    return ("planned and room-sound silences and quoted light not counted; a rupture elsewhere in the scene, a quote "
            "with no light word, own light and silence counted")


@group("P9: COVER-08 takes a light the scene's look already carries, described as it is, as covered; a light that "
       "changes or moves (held, goes out, dies, floods in) still needs a light cue")
def light_the_look_carries(scratch):
    if not EXCERPT.is_file():
        info("skipped: story not present")
        return "skip"
    no_cue = edit(gold_texts(), "context", "LOOK LK-SAYE-KITCHEN-NIGHT",
                  '- light_cue: SC10 "Iona holds the lamp." = SC10-B02 | change: the lamp is in Iona\'s hand over '
                  'Jude, so the light moves when she moves | why: the story puts the only light in her hand\n', "")
    story_text = EXCERPT.read_text(encoding="utf-8")
    assert "Iona holds the lamp." in story_text

    def cover_08_with(sentence, folder):
        changed = scratch / folder / EXCERPT.name
        changed.parent.mkdir(parents=True, exist_ok=True)
        changed.write_text(story_text.replace("Iona holds the lamp.", sentence, 1), encoding="utf-8")
        result = run_checks(parsed(no_cue), SCHEMA, WORDS, CONSTANTS,
                            story=StorySource.from_file(changed, CONSTANTS), check_ids=["COVER-08"])
        return [str(problem) for problem in lines_of(result, "COVER-08")]
    assert not cover_08_with("The lamp stands on the table.", "p9 still"), "a lamp at rest, the look's own, was asked a cue"
    for sentence in ("Iona holds the lamp.", "The lamp goes out.", "The light dies.", "Bright light floods the kitchen.",
                     "Light, table, light, table.", "Iona holds the lamp. It flickers."):
        found = cover_08_with(sentence, f"p9 {len(sentence)}")
        assert found, f"a light that changes or moves was taken as covered by the look: {sentence!r}"
    return "a lamp at rest covered by the look; held, going out, dying, flooding, repeated or flickering light asks a cue"


# ---------------------------------------------------------------- P10

@group("P10: the time floor counts text to read (never blurred background) and owes a beat's pause once, on the "
       "last shot naming it")
def time_floors(scratch):
    from stage_tools.derive_fields import provisional_floor, text_must_be_read, time_floor
    run, breakdown = gold_breakdown()
    title = run.record("TX-TITLE-CATCH")
    assert text_must_be_read(title), "an emphasised title is not read"
    blurred = parse_text("### TEXT TX-SIGN A sign\n- words: EXIT\n- method: background_blur\n- plot_critical: yes\n\n"
                         "END OF FILE | Test | 1 records\n", "08 Places and things.md", SCHEMA).records[0]
    passing = parse_text("### TEXT TX-SHOP A shop sign\n- words: BAKERY\n- plot_critical: no\n- emphasis: 0\n\n"
                         "END OF FILE | Test | 1 records\n", "08 Places and things.md", SCHEMA).records[0]
    assert not text_must_be_read(blurred) and not text_must_be_read(passing)
    floor = time_floor(breakdown, run.record("SC10-SH990"))
    assert floor.text_floor > 0 and floor.text_parts, f"the title's reading time is not in the floor: {floor}"
    owed_180 = time_floor(breakdown, run.record("SC10-SH180"))
    owed_190 = time_floor(breakdown, run.record("SC10-SH190"))
    beats_180 = [part[0] for part in owed_180.pause_parts]
    beats_190 = [part[0] for part in owed_190.pause_parts]
    assert "SC10-B10" not in beats_180 and "SC10-B10" in beats_190, (beats_180, beats_190)
    quoted = edit(gold_texts(), "scene", "SHOTLIST SC10-LIST", "white on black: THE CATCH",
                  'white on black: "THE CATCH"')
    run, breakdown = gold_breakdown(quoted)
    item = provisional_floor(breakdown, "SC10", "SC10-SH990")
    assert item is not None and item.text_parts, f"the list item's quoted title was not read: {item}"
    return f"title read, blur and passing sign not; pause of beat 10 owed by shot 190 only"


@group("P10: TIME-03 measures the scene's shots against its own list: a small overrun is kept, a large one warned")
def time_against_list(scratch):
    small = edit(gold_texts(), "scene", "SHOT SC10-SH150", "- screen_time: 15", "- screen_time: 17")
    assert not lines_of(checked(small, ["TIME-03"]), "TIME-03"), "two seconds over a list of 113 was warned"
    large = edit(gold_texts(), "scene", "SHOT SC10-SH150", "- screen_time: 15", "- screen_time: 45")
    found = lines_of(checked(large, ["TIME-03"]), "TIME-03")
    assert found, "thirty seconds over the list was not warned"
    assert found[0].record == "SC10-LIST" and "one-line list" in str(found[0]), str(found[0])
    assert "scene_duration_tolerance_share" not in str(found[0]) and "target" not in str(found[0]).split(".")[0]
    return str(found[0])[:140]


# ---------------------------------------------------------------- P11, P12

@group("P11: INFO-01 accepts a shot that says how it keeps the fact hidden, without deleting what is on screen")
def keep_hidden_clears(scratch):
    fact = ('### FACT FT-09 The flask\n- what: the flask holds the clip\n- element: PR-FLASK\n'
            '- audience_knows_from: SC10 "Don\'t open the flask." = SC10-B06\n- known_by: CH-ELI | from: SC07\n'
            '- mode: mystery\n')
    texts = edit(gold_texts(), "context", "FACT FT-01", add_after=fact)
    found = lines_of(checked(texts, ["INFO-01"], story=False), "INFO-01", "SC10-SH020")
    assert found, "the flask before its reveal was not warned"
    hidden = edit(texts, "scene", "SHOT SC10-SH020", "- keep_hidden: FT-01 | how: frame_edge",
                  "- keep_hidden: FT-01 | how: frame_edge\n- keep_hidden: FT-09 | how: dark")
    found = lines_of(checked(hidden, ["INFO-01"], story=False), "INFO-01", "SC10-SH020")
    assert not found, f"keep_hidden did not clear it: {found}"
    shot = parse_text(hidden["scene"], GOLD_FILES["scene"].name, SCHEMA)
    kept = [record for record in shot.records if record.identifier == "SC10-SH020"][0]
    assert "PR-FLASK.S03" in (kept.get("must_show") or ""), "must_show lost the flask"
    return "warned without keep_hidden; cleared with it; the flask stays in must_show"


@group("P12: STATE-01 reads a recording's state where it was recorded; its fix names the missing state as an "
       "addition")
def recorded_state(scratch):
    if not EXCERPT.is_file():
        info("skipped: story not present")
        return "skip"
    early = edit(gold_texts(), "scene", "SHOT SC10-SH010", "- subject: CH-JUDE.S02 |", "- subject: CH-JUDE.S03 |")
    found = lines_of(checked(early, ["STATE-01"]), "STATE-01", "SC10-SH010")
    assert found, "a state used before its line was not found"
    recorded = edit(gold_texts(), "scene", "SHOT SC10-SH010", "- subject: CH-JUDE.S02 |",
                    "- subject: CH-JUDE.S03 | recorded: SC10 |")
    after = lines_of(checked(recorded, ["STATE-01"]), "STATE-01", "SC10-SH010")
    assert not after, f"a recorded state was read at the shot: {[str(problem) for problem in after]}"
    missing = edit(gold_texts(), "context", "STATE PR-LAMP.S01", "- from: SC10 | line: 399", "- from: SC10 | line: 480")
    missing = edit(missing, "scene", "SHOT SC10-SH010", "- thing: PR-LAMP.S01 |", "- thing: PR-LAMP |")
    lines = lines_of(checked(missing, ["STATE-01"]), "STATE-01", "SC10-SH010")
    assert lines and "addition" in str(lines[0]), f"the fix names no addition: {[str(line) for line in lines]}"
    return "S03 before line 408 warned; recorded at SC10 accepted; a missing state is added as an addition"


# ---------------------------------------------------------------- P13

@group("P13: retired words only in their retired senses (movement, bed, her look, withhold as a tactic)")
def retired_senses(scratch):
    from stage_tools.checks_craft_reasons_words import retired_words_in_text

    def found(text, field_path=None):
        return [written.lower() for written, _ in retired_words_in_text(text, WORDS, field_path=field_path)]
    assert not found("His movement is slow and careful."), found("His movement is slow and careful.")
    assert found("The camera movement follows her."), "a camera movement was not flagged"
    assert not found("the hospital bed creaks under him", "SHOT.room_sound"), "a hospital bed was flagged"
    assert found("a low room-tone bed under the scene", "SHOT.room_sound"), "a sound bed was not flagged"
    assert not found("Her look goes to the door."), found("Her look goes to the door.")
    assert not found("she tries to withhold the answer", "BEAT.action"), "a tactic was flagged"
    assert not found("CH-ELI.S03 | tactic: withhold", "SHOT.subject"), "a tactic was flagged"
    assert found("we withhold the hand until beat 7", "SHOT.why"), "withhold outside a tactic field"
    return "ordinary English kept, retired senses flagged"


@group("P13: a place's 'bullet scars' is no body scar; 'left palm' is not the dressed palm; an insert shows a "
       "sided feature only when its words name it")
def sides_in_words(scratch):
    from stage_tools.checks_sides_geometry import clause_names_this_one, insert_words_name
    load_check_families()
    place = edit(gold_texts(), "context", "STATE LOC-SAYE-KITCHEN.S01", "- state_line: ",
                 "- state_line: old bullet scars in the plaster by the door; ")
    assert not lines_of(checked(place, ["SIDE-01"], story=False), "SIDE-01", "LOC-SAYE-KITCHEN.S01")
    assert clause_names_this_one("she lays her left palm flat on the glass", "dressed palm") is False
    assert clause_names_this_one("the dressed palm bleeds through", "dressed palm") is True
    assert clause_names_this_one("the ring catches the lamp", "wedding ring") is True
    run, breakdown = gold_breakdown(story=False)
    assert insert_words_name(breakdown, run.record("SC10-SH090"), "wedding ring") is True
    assert insert_words_name(breakdown, run.record("SC10-SH020"), "wedding ring") is False
    return "place scars skipped; the other palm; ring insert names the ring, flask insert does not"


@group("P13: a black in the middle of a scene keeps its number; an end black below 990 is warned")
def black_mid_scene(scratch):
    middle = edit(gold_texts(), "scene", "SHOT SC10-SH140", "- kind: live", "- kind: black")
    assert not lines_of(checked(middle, ["ID-03"], story=False), "ID-03", "SC10-SH140")
    end = edit(gold_texts(), "scene", "SHOT SC10-SH200", "- kind: live", "- kind: black")
    found = lines_of(checked(end, ["ID-03"], story=False), "ID-03", "SC10-SH200")
    assert found and "end of the scene" in str(found[0]), [str(problem) for problem in found]
    return "shot 140 black kept; shot 200 black warned"


# ---------------------------------------------------------------- P14

@group("P14: word swaps are made once and everywhere; a swap whose target holds its source is not banned")
def word_swaps(scratch):
    from stage_tools.derive_fields import project_prompt_swaps, swap_prompt_words, swap_sources_banned
    swaps = [("cage", "open steel freight elevator car"), ("flask", "small steel vacuum flask")]
    assert swap_prompt_words("The cage drops.", swaps) == "The open steel freight elevator car drops."
    assert swap_prompt_words("a small steel vacuum flask and a flask", swaps) == \
        "a small steel vacuum flask and a small steel vacuum flask"
    assert swap_sources_banned(swaps) == ["cage"], swap_sources_banned(swaps)
    project = parse_text("### PROJECT CATCH The Catch\n- prompt_words: torch | use: flashlight\n"
                         "- prompt_words: cage | use: open steel freight elevator car\n\nEND OF FILE | Test | 1 "
                         "records\n", "00 Start here.md", SCHEMA).records[0]
    pairs = project_prompt_swaps(WORDS, project)
    assert ("cage", "open steel freight elevator car") in pairs and ("torch", "flashlight") in pairs, pairs
    return f"{len(pairs)} swaps; made once; the flask's own words allowed"


@group("P14: GEN-05 does not read a room sound as the place described again; GEN-06 leaves model-drawn text and "
       "matches capitals as printed; GEN-15 leaves quoted script alone")
def prompt_checks(scratch):
    from stage_tools import checks_plan_generation_film as generation
    clip = SimpleNamespace(prompt="Iona kneels by the rail. Room sound: a small sealed room at dawn: the air handling.",
                           data={"sounds": ["room sound: a small sealed room at dawn: the air handling"]})
    assert "sealed room" not in generation.prompt_without_sounds(clip)
    source = (TOOLS / "stage_tools" / "checks_plan_generation_film.py").read_text(encoding="utf-8")
    assert '== "model_drawn"' in source and "words != words.upper()" in source
    assert "QUOTED_WORDS.sub" in source
    assert "model_drawn" in SCHEMA.field("TEXT", "method").get("values", [])
    project = gold_command_project(scratch, "p14 lint")
    start = project / "00 Start here.md"
    start.write_text(start.read_text(encoding="utf-8").replace(
        "- prompt_words: torch | use: flashlight", "- prompt_words: torch | use: flashlight\n"
        "- prompt_words: fridge | use: refrigerator"), encoding="utf-8")
    code, output = stage(["build", "--project", project])
    assert code == 0, output[-400:]
    code, output = stage(["compile", "--lint-only", "--project", project])
    assert code in (0, 1), output[-600:]
    fridge = [line for line in output.splitlines() if "fridge" in line.lower() and re.match(r"^[EW] GEN-", line)]
    assert not fridge, f"the place's words were not swapped: {fridge[:2]}"
    return "room sound left out of GEN-05; model_drawn and capitals; a place's fridge swapped in prompts"


# ---------------------------------------------------------------- P16

@group("P16: '- field: none' clears a stored field where none is no value; a note sent on an existing record is "
       "kept; apply names the next command as the handout does")
def none_clears(scratch):
    from stage_tools.project_files import next_after_apply
    if not READER_SCREENPLAY.is_file():
        info("skipped: the reader fixture is not present")
        return "skip"
    project = small_project(scratch, "p16")
    write_inbox(project, "U-06-CAMERA.md", "### CAMSYS\n- lens_type: spherical\n- lens_family: 28, 40, 75\n"
                "- normal_lens_mm: 40\n- default_move: static\n")
    code, output = stage(["apply", "U-06-CAMERA.md"], cwd=project)
    assert code == 0, output[-600:]
    write_inbox(project, "U-06-CAMERA - fix 1.md", "### CAMSYS\n> the normal lens is left to the film rules\n"
                "- normal_lens_mm: none\n")
    code, output = stage(["apply", "U-06-CAMERA - fix 1.md"], cwd=project)
    assert code == 0 and "Cleared normal_lens_mm of CAMSYS" in output, output[-600:]
    rules = parse_file(project / "10 Film rules.md", "10 Film rules.md", SCHEMA)
    camera = next(record for record in rules.records if record.type_name == "CAMSYS")
    assert camera.get("normal_lens_mm") is None and camera.get("lens_type") == "spherical", camera.get("lens_type")
    assert "the normal lens is left to the film rules" in (project / "10 Film rules.md").read_text(encoding="utf-8")
    steps = json.loads((SKILL / "schema" / "steps.json").read_text(encoding="utf-8"))
    assert next_after_apply("U-07-SC10", steps) == "stage.py build, then stage.py check --unit U-07-SC10"
    assert next_after_apply("U-08-SC10-B1", steps).startswith("stage.py build, then")
    assert next_after_apply("U-06-CAMERA", steps) == "stage.py check --unit U-06-CAMERA"
    assert next_after_apply("acceptance", steps) == "stage.py check --all, then stage.py next --checkpoint-passed"
    assert next_after_apply("notes from the user", steps) == "stage.py next"
    assert next_after_apply("U-01-SCENELIST-ANSWERS", steps) == "stage.py check --step 1, then stage.py next"
    return "normal_lens_mm cleared, the note kept; build before check at steps 7 and 8"


# ---------------------------------------------------------------- P15, P17, P18 and the blueprint

@group("P15, P17, P18: the step files say the rules the checker enforces, the non-human character and the last "
       "steps; the blueprint's kill rule counts only real layout mistakes")
def written_rules(scratch):
    step_7 = (SKILL / "steps" / "07 Scene design and shot list.md").read_text(encoding="utf-8")
    step_8 = (SKILL / "steps" / "08 Shot details.md").read_text(encoding="utf-8")
    step_4 = (SKILL / "steps" / "04 Characters, places and things.md").read_text(encoding="utf-8")
    step_10 = (SKILL / "steps" / "10 Check and estimate.md").read_text(encoding="utf-8")
    wanted = {"a speech's words": ("words are on the lines after its speaker's name", step_8),
              "size from lens and distance": ("36 ÷ lens × distance", step_8),
              "one main action per 4 seconds": ("one per started 4 seconds", step_8),
              "no camera inside an object": ("never stands inside an object", step_8),
              "the lens family in force": ("the family in force here", step_8),
              "a recording's state": ("| recorded: SC06", step_8),
              "a missing state as an addition": ("as an addition", step_8),
              "the pause owed once": ("owed once", step_8),
              "setups never inside an object": ("never inside an object", step_7),
              "the non-human character": ("tier: non_human", step_4),
              "where the user's answers go": ("inbox/acceptance.md", step_10),
              "RV-FILM's answers": ("RV-FILM's `answer` items", step_10),
              "one finding for several scores": ("one FINDING may be cited by several scores", step_10)}
    missing = [name for name, (phrase, text) in wanted.items() if phrase not in text]
    assert not missing, f"not written: {missing}"
    blueprint = BLUEPRINT.read_text(encoding="utf-8") if BLUEPRINT.is_file() else ""
    if blueprint:
        assert "more real layout mistakes than craft errors" in blueprint
        assert "missing fields and refused values do not" in blueprint
        assert "the grammar errors (FORM family) before repair outnumber" not in blueprint
    steps = json.loads((SKILL / "schema" / "steps.json").read_text(encoding="utf-8"))
    things = next(unit for step in steps["steps"] if step["step"] == 4 for unit in step.get("units", [])
                  if unit.get("id_pattern") == "U-04-THINGS")
    assert any("CHARACTER" in str(entry) and "non_human" in str(entry) for entry in things.get("writes", [])), things
    return f"{len(wanted)} rules written; the kill rule counts layout mistakes only"


@group("P17: a non-human character is recognised, and TIME-09 does not hold it to a person's timing")
def non_human(scratch):
    from stage_tools.checks_coverage_time_state import is_non_human
    texts = edit(gold_texts(), "context", "CHARACTER CH-ELI", add_after=(
        "### CHARACTER CH-CREATURE The animal\n- names: the animal, it\n- tier: non_human\n"
        "- role: the creature inside the figure\n- voice: none\n"))
    run, breakdown = gold_breakdown(texts, story=False)
    assert is_non_human(breakdown, "CH-CREATURE") is True
    assert is_non_human(breakdown, "CH-IONA") is False
    from stage_tools.checks_form import FormContext, run_form_checks
    files = parsed(texts)
    context = FormContext.for_records(SCHEMA, WORDS, files, step=4)
    problems = [problem for problem in run_form_checks(files, context, ["FORM-04"])
                if problem.record == "CH-CREATURE"]
    assert not problems, [str(problem) for problem in problems]
    return "tier non_human with voice none is valid and recognised"


@group("P18: one film length: the book says the story's length, then 'with titles and credits' when titles exist")
def one_length(scratch):
    project = gold_command_project(scratch, "p18 length")
    code, output = stage(["build", "--project", project])
    assert code == 0, output[-400:]
    (project / MACHINE / "estimate.json").write_text(json.dumps({"estimate": {"titles_and_credits_s": 60}}),
                                                     encoding="utf-8")
    code, output = stage(["export", "book", "--project", project])
    assert code == 0, output[-400:]
    book = (project / "15 The breakdown" / "The breakdown.md").read_text(encoding="utf-8")
    line = next((line for line in book.splitlines() if "of story" in line), "")
    assert re.search(r"of story \(.+ with titles and credits\)\.", line), line or book[:400]
    assert "of film" not in line, line
    return line[:110]


# ---------------------------------------------------------------- the book, ID-02, CITE-03, GEOM-05

@group("The book names the one-of-a-kind records in plain words (no LADDER, CAMSYS, SOUNDPLAN or 'PLAN peak')")
def book_plain_names(scratch):
    project = gold_command_project(scratch, "book names")
    scene_file = next((project / "11 Scenes").glob("*.md"))
    text = scene_file.read_text(encoding="utf-8")
    first, end = record_block(text.split("\n"), "SHOT SC10-SH150")
    lines = text.split("\n")
    for index in range(first, end):
        if lines[index].startswith("- why: "):
            lines[index] += " (PLAN peak tightest_size; LADDER; CAMSYS break; SOUNDPLAN rupture_plan)"
            break
    scene_file.write_text("\n".join(lines), encoding="utf-8")
    code, output = stage(["build", "--project", project])
    assert code == 0, output[-400:]
    code, output = stage(["export", "book", "--project", project])
    assert code == 0, output[-400:]
    book = (project / "15 The breakdown" / "The breakdown.md").read_text(encoding="utf-8")
    leaks = [word for word in ("LADDER", "CAMSYS", "SOUNDPLAN", "PLAN peak", "tightest_size", "rupture_plan")
             if word in book]
    assert not leaks, f"in the book: {leaks}"
    assert "the ladder of closest shots" in book and "the camera system" in book, "plain names missing"
    return "the ladder of closest shots, the camera system, the sound plan, the story plan's peak"


@group("ID-02 waits for a choice's record; CITE-03 reads a speech across a stage direction; GEOM-05 knows when an "
       "object arrives")
def waiting_and_arriving(scratch):
    from stage_tools.checks_ids_citations import quote_in_a_speech
    from stage_tools.derive_fields import object_from_scene
    texts = edit(gold_texts(), "context", "SOUNDPLAN", remove=True)
    result = checked(texts, ["ID-02"], story=False)
    about = [str(problem) for problem in lines_of(result, "ID-02") if "SOUNDPLAN" in str(problem)]
    assert not about, about
    assert any("waiting" in why for check_id, why in result.skipped if check_id == "ID-02"), result.skipped
    run = SimpleNamespace(speeches={"SC06-D04": {"line": 250, "text": "I know. Not that one."}})
    assert quote_in_a_speech(run, "I know. Not that one.", 248, 256)
    assert not quote_in_a_speech(run, "I know. Not this one.", 248, 256)
    assert object_from_scene({"material": "grey canvas", "meaning": "the tent, from scene 29"}) == "SC29"
    assert object_from_scene({"material": "canvas, from SC29"}) == "SC29"
    assert object_from_scene({"material": "pale wood"}) is None
    return "the sound plan's choices wait; a speech quoted whole; the tent from scene 29"


# ---------------------------------------------------------------- smaller items

@group("Smaller items: status says '0 of' and lists a left-over repair apart; quote_for_message cuts between words; "
       "a place's own word outweighs a shared one; a common-word name is found only as a name")
def smaller_items(scratch):
    from stage_tools.fill_code_fields import best_location_for
    from stage_tools.make_handout import name_pattern
    from stage_tools.record_format import quote_for_message
    project = gold_command_project(scratch, "smaller")
    manifest = read_manifest(project)
    manifest["batches"] = {"SC10": {"U-08-SC10-B3": {"expected": 5}}}
    stamp = datetime.datetime.now().replace(microsecond=0).isoformat()
    for entry in manifest.get("units_done", []):
        if entry.get("unit") == "U-07-SC10":
            entry["applied"] = stamp
    if not any(entry.get("unit") == "U-07-SC10" for entry in manifest.get("units_done", [])):
        manifest.setdefault("units_done", []).append({"unit": "U-07-SC10", "applied": stamp})
    write_manifest(project, manifest)
    left = write_inbox(project, "U-07-SC10 - fix 1.md", "### SCENE SC10 Saye's kitchen\n- note: a refused repair\n")
    old = time.time() - 3 * 86400
    os.utime(left, (old, old))
    code, output = stage(["status", "--project", project])
    assert code == 0, output[-400:]
    assert "U-08-SC10-B3 (0 of 5)" in output, output[-800:]
    assert "Left in the inbox after a refused apply" in output and "U-07-SC10 - fix 1.md" in output, output[-800:]
    assert "In the inbox, not yet applied: U-07-SC10 - fix 1.md" not in output
    value = "she climbs on past the landing and the stairwell turns and turns until the door at the top will turn"
    quoted = quote_for_message(value)
    head, tail = quoted.strip('"').split(" [shortened] ")
    assert value.startswith(head) and value.endswith(tail), quoted
    assert value[len(head)] == " " and value[-len(tail) - 1] == " ", f"half a word: {quoted}"
    places = [SimpleNamespace(identifier="LOC-NURSES-ROOM", title="The nurses' room"),
              SimpleNamespace(identifier="LOC-STORE-ROOM", title="The store room"),
              SimpleNamespace(identifier="LOC-WARD-ROOM", title="The ward room"),
              SimpleNamespace(identifier="LOC-BACK-PASSAGE", title="The back passage")]
    # one word shared with each place: "passage" is the passage's own, "room" is shared by three places
    best = best_location_for("INT. HOSPITAL - PASSAGE, ROOM END - NIGHT", places)
    assert best is not None and best.identifier == "LOC-BACK-PASSAGE", best
    best = best_location_for("INT. HOSPITAL - STORE ROOM - NIGHT", places)
    assert best is not None and best.identifier == "LOC-STORE-ROOM", best
    story = "A small figure in the corner. THE FIGURE rises. The figure walks."
    pattern = re.compile(name_pattern("FIGURE", story))
    assert not pattern.search("A small figure in the corner.")
    assert pattern.search("THE FIGURE rises.") and pattern.search("The figure walks.")
    assert re.compile(name_pattern("Iona", story)).search("iona waits")
    return "0 of 5; left-over repair apart; whole words; the passage; the figure as a name"


# ---------------------------------------------------------------- the cross-examination of the fixes (X01 to X15)

@group("X01: '- field: none' never clears a field of a locked record; it is refused as FORM-11")
def locked_not_cleared(scratch):
    project = gold_command_project(scratch, "x01 locked")
    write_inbox(project, "U-06-CAMERA - fix 1.md", "### CAMSYS\n- normal_lens_mm: none\n- camera_speed: none\n")
    code, output = stage(["apply", "U-06-CAMERA - fix 1.md", "--project", project])
    assert code == 1 and "E FORM-11 CAMSYS normal_lens_mm clears a field of a locked record" in output, output[-600:]
    rules = parse_file(project / "10 Film rules.md", "10 Film rules.md", SCHEMA)
    camera = next(record for record in rules.records if record.type_name == "CAMSYS")
    assert camera.get("normal_lens_mm") and camera.get("camera_speed"), "a locked field was cleared"
    return "refused with FORM-11; the locked camera system keeps both fields"


@group("X02: step 12 counts as done only when export all ran on the current records, not after a book alone")
def export_all_done(scratch):
    from stage_tools.make_handout import Workspace, exports_are_fresh
    project = gold_command_project(scratch, "x02 exports")
    code, output = stage(["export", "book", "--project", project])
    assert code == 0, output[-400:]
    assert exports_are_fresh(Workspace(project)) is False, "a book made alone counted as every export"
    code, output = stage(["export", "all", "--project", project])
    assert code == 0, output[-400:]
    assert exports_are_fresh(Workspace(project)) is True, "export all did not count"
    rules = project / "10 Film rules.md"
    text = rules.read_text(encoding="utf-8")
    rules.write_text(text.replace("- default_move: static", "- default_move: static\n- note: a changed record", 1),
                     encoding="utf-8")
    assert exports_are_fresh(Workspace(project)) is False, "a changed record left the exports counted as done"
    return "book alone: not done; export all: done; a record changed: not done"


@group("X05: a ring insert is protected from flipping when its must_show or things carry the ring, even if its "
       "words do not say 'ring'")
def ring_insert_by_record(scratch):
    texts = gold_texts()
    for find, replace in [
            ("- purpose: The proof in plain sight: Saye's wedding ring is on the hand that looks like her right.",
             "- purpose: The proof in plain sight: Saye's hand lies on the table, the one that looks like her right."),
            ("a plain gold ring on it", "fingers spread"),
            ("the ring catches the lamp", "the hand catches the lamp"),
            ("- end: the ringed hand flat on the table's edge", "- end: the hand flat on the table's edge"),
            ("- flip: never", "- flip: auto")]:
        texts = edit(texts, "scene", "SHOT SC10-SH090", find, replace)
    found = lines_of(checked(texts, ["SIDE-03"]), "SIDE-03", "SC10-SH090")
    assert found and "wedding ring" in str(found[0]), [str(problem) for problem in found]
    return "SIDE-03 still asks flip: never on the ring insert"


@group("X06: a character marked non_human that has a voice is still held to a person's timing")
def non_human_needs_silence(scratch):
    from stage_tools.checks_coverage_time_state import is_non_human
    texts = edit(gold_texts(), "context", "CHARACTER CH-JUDE", "- tier: principal", "- tier: non_human")
    run, breakdown = gold_breakdown(texts, story=False)
    assert breakdown.record("CH-JUDE", "CHARACTER").get("tier") == "non_human"
    assert is_non_human(breakdown, "CH-JUDE") is False, "a speaking principal marked non_human was taken as an animal"
    return "Jude, with a voice, stays a person"


@group("X08: TIME-03 warns when a scene's list is more than twice, or under half, its planned length")
def design_against_target(scratch):
    far = edit(gold_texts(), "context", "SCENE SC10", "- target_duration_s: 110", "- target_duration_s: 40")
    # changed after the second full run (Project notes 39, F19): the first estimate is named as such, and the far
    # list is a warning until the user approves the list, then a note
    found = lines_of(checked(far, ["TIME-03"]), "TIME-03")
    assert any("times the first estimate's 40 s" in str(problem) and problem.level == "N" for problem in found), \
        [str(problem) for problem in found]
    draft = edit(far, "scene", "SHOTLIST SC10-LIST", "- approved: yes", "- approved: no")
    found = lines_of(checked(draft, ["TIME-03"]), "TIME-03")
    assert any("times the first estimate's 40 s" in str(problem) and problem.level == "W" for problem in found), \
        [str(problem) for problem in found]
    near = lines_of(checked(gold_texts(), ["TIME-03"]), "TIME-03")
    assert not any("first estimate" in str(problem) for problem in near), [str(problem) for problem in near]
    return "a list 2.8 times its first estimate warned, then a note once approved; the gold's own estimate silent"


@group("X09: GEN-06 allows model_drawn only for one short mark, and finds capitals written with a capital on every "
       "word, never inside lower-case prose")
def drawn_text_limits(scratch):
    from stage_tools.checks_plan_generation_film import is_single_mark, words_asked_for
    assert is_single_mark("F") and is_single_mark("12") and not is_single_mark("NO ENTRY BEYOND THIS POINT")
    assert words_asked_for("THE CATCH", "The words The Catch in white letters.")
    assert words_asked_for("THE END", "A black card: THE END.")
    assert not words_asked_for("THE END", "She walks to the end of the corridor.")
    assert not words_asked_for("THE END", "The end of the corridor is dark.")
    assert words_asked_for("Exit", "a green sign that says exit")
    return "one mark allowed; 'The Catch' found; 'the end of the corridor' not"


@group("X13: 'as before' is a shortening when its sentence points back ('the same ... as before'), English otherwise")
def as_before_points_back(scratch):
    from stage_tools.checks_form import find_marker
    markers = ["as before"]
    assert find_marker("the same framing, lens and light as before; the lamp lower", markers) == "as before"
    assert find_marker("As before, the lamp on its hook.", markers) == "as before"
    assert find_marker("while the torch and the tunnel's sound go on as before.", markers) is None
    assert find_marker("She keeps the lamp low and warm as before, while Iona speaks.", markers) is None
    return "pointing back flagged; plain English kept"


@group("X14: the camera rule's cap still holds for the turn when the ladder's rung is on another beat")
def rung_on_another_beat(scratch):
    texts = edit(gold_texts(), "context", "LADDER", "= SC10-B07", "= SC10-B02") \
        if "= SC10-B07" in gold_texts()["context"] else None
    if texts is None:
        info("skipped: the gold's ladder names no resolved beat for scene 10")
        return "skip"
    texts = edit(texts, "scene", "SHOT SC10-SH150", "- size: close_up", "- size: medium")
    found = lines_of(checked(texts, ["CRAFT-03"]), "CRAFT-03", "SC10-SH150")
    assert any("allows its subject up to" in str(problem) for problem in found), [str(problem) for problem in found]
    return "the turn at medium is asked for the camera rule's close-up"


@group("X15: a shot that keeps a fact hidden gets a review question about the hiding")
def hidden_fact_question(scratch):
    from stage_tools.adopt_folder import select_and_ask
    run, breakdown = gold_breakdown()
    groups, counts = select_and_ask(run, {}, breakdown, sample=False, seed=1, share=1.0)
    asked = [question for _, record, _, questions in groups for question in questions
             if "keeps a secret from the audience" in str(question)]
    assert asked and counts.get("shots keeping a fact hidden", 0) >= 1, (counts, len(asked))
    return f"{len(asked)} questions on {counts['shots keeping a fact hidden']} shots that hide a fact"


@group("X03: a light moves or changes in its sentence; a light things move into, or a bright surface, is at rest")
def light_moves_in_sentence(scratch):
    from stage_tools.checks_coverage_time_state import light_moves_in
    cases = [("He turns the card to the light and reads it.", "light", False),
             ("A shape comes into the light at the far end.", "light", False),
             ("His hand slides across the bright rail.", "bright", False),
             ("The lamp stands on the shelf.", "lamp", False),
             ("She carries the torch round the corner.", "torch", True),
             ("She comes round the truck with the torch.", "torch", True),
             ("His light goes onto each step before his foot does.", "light", True),
             ("He brings the light up: the bolt is gone.", "light", True),
             ("Light, wall, light, wall.", "light", True),
             ("The green strip dims.", "green", True),
             ("The lamp goes out.", "lamp", True)]
    wrong = [(sentence, expected) for sentence, word, expected in cases if light_moves_in(sentence, word) != expected]
    assert not wrong, wrong
    return f"{len(cases)} sentences read right"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="stage fix02 ") as temporary:
        scratch = Path(temporary)
        jump_cut_numbers(scratch)
        shortening_markers(scratch)
        film_pass_wording(scratch)
        made_from_records(scratch)
        approval_not_due(scratch)
        checkpoint_nothing_waiting(scratch)
        split_once(scratch)
        handout_fit_order(scratch)
        review_in_brief(scratch)
        shot_handout(scratch)
        health_check_page(scratch)
        scores_in_words(scratch)
        ladder_decides(scratch)
        light_in_context(scratch)
        added_changes(scratch)
        light_the_look_carries(scratch)
        time_floors(scratch)
        time_against_list(scratch)
        keep_hidden_clears(scratch)
        recorded_state(scratch)
        retired_senses(scratch)
        sides_in_words(scratch)
        black_mid_scene(scratch)
        word_swaps(scratch)
        prompt_checks(scratch)
        none_clears(scratch)
        written_rules(scratch)
        non_human(scratch)
        one_length(scratch)
        book_plain_names(scratch)
        waiting_and_arriving(scratch)
        smaller_items(scratch)
        locked_not_cleared(scratch)
        export_all_done(scratch)
        ring_insert_by_record(scratch)
        non_human_needs_silence(scratch)
        design_against_target(scratch)
        drawn_text_limits(scratch)
        as_before_points_back(scratch)
        rung_on_another_beat(scratch)
        hidden_fact_question(scratch)
        light_moves_in_sentence(scratch)
    failing = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({RESULTS.count(True)} passed, {failing} failing groups)")
    return 0 if not failing else 1


if __name__ == "__main__":
    sys.exit(main())
