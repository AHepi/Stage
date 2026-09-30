"""The acceptance test of work package 4b: the check framework (check_records.py), the command check, and the ID and
CITE check families (checks_ids_citations.py), with WP2's FORM checks registered through the framework.

What it proves (blueprint 7.2, 7.3, 14.2 row WP4):
- every check this package owns is registered with 7.2's level and build;
- one faulty fixture per check fires, naming the record it should (the faulty fixtures are the small invented
  projects in tests/fixtures/ids and citations/, each changed by one edit listed below; the FORM checks use WP2's
  grammar fixtures);
- the same checks are silent on the WP12a gold fixture (examples/01 and 02, with the scene 10 excerpt, and with
  the whole story when --story is given);
- the command check: the report 13 Health check.md with its first line "In short: ...", tidy fixes made and
  logged, a locked record changed by hand caught on the next check (FORM-11), --step, --scene, --film, --all and
  --story, and the exit codes of 7.3 (0, 1, 2);
- the guards apply runs on an inbox (ID-01, ID-04, ID-06) refuse it and change no file.

Usage: python tests/wp4b_checks_acceptance.py [--story "<The Catch, the whole story>"]
Without the scene 10 excerpt the gold's story groups say "skipped: story not present". Standard library only.
"""

import argparse
import json
import os
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

from stage_tools import check_records  # noqa: E402
from stage_tools.check_records import REGISTRY, StorySource, load_check_families, run_checks  # noqa: E402
from stage_tools.record_format import DIVIDER_LINE, load_skill_data, parse_file, parse_text  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
FIXTURES = REPOSITORY / "tests" / "fixtures"
OWN_FIXTURES = FIXTURES / "ids and citations"
KEY_PROJECT = OWN_FIXTURES / "base"
KEY_STORY = OWN_FIXTURES / "The key - story.txt"
LAMP_PROJECT = OWN_FIXTURES / "prose base"
LAMP_STORY = OWN_FIXTURES / "The lamp - prose story.md"
GRAMMAR = FIXTURES / "grammar"
EXCERPT = FIXTURES / "The Catch - lines 397-489.txt"
GOLD_SCENE = SKILL / "examples" / "01 The Catch - scene 10.md"
GOLD_CONTEXT = SKILL / "examples" / "02 The Catch - scene 10 - context.md"
SCENE_1 = "11 Scenes/Scene 01 - Mara's workshop.md"
SCENE_2 = "11 Scenes/Scene 02 - The shop door.md"
LAMP_SCENE = "11 Scenes/Scene 01 - The harbour wall.md"

OWN_FAMILIES = ("FORM", "ID", "CITE")
LEVELS_7_2 = {
    "FORM-01": "E", "FORM-02": "E", "FORM-03": "E", "FORM-04": "E", "FORM-05": "E", "FORM-06": "E", "FORM-07": "E",
    "FORM-08": "E", "FORM-09": "E", "FORM-10": "E/W", "FORM-11": "E", "FORM-12": "E", "FORM-13": "N",
    "ID-01": "E", "ID-02": "E", "ID-03": "W", "ID-04": "E", "ID-05": "E", "ID-06": "E", "ID-07": "E", "ID-08": "E",
    "ID-09": "E", "CITE-01": "E", "CITE-02": "E", "CITE-03": "E", "CITE-04": "E", "CITE-05": "W", "CITE-06": "E",
    "CITE-07": "E",
}
BUILD_TWO = {"CITE-07"}

RESULTS = []


def report(passed, group, detail=""):
    RESULTS.append(passed)
    print(f"{'PASS' if passed else 'FAIL'}  {group}" + (f": {detail}" if detail else ""), flush=True)


def info(line):
    print(f"INFO  {line}", flush=True)


# ---------------------------------------------------------------- fixtures made by one edit

def read_folder(folder):
    """{relative name: text} of every .md file in a project fixture folder."""
    return {str(path.relative_to(folder)).replace(os.sep, "/"): path.read_text(encoding="utf-8")
            for path in sorted(folder.rglob("*.md"))}


def apply_edits(texts, edits):
    """Each edit is (file, old, new): old must occur in the file and every occurrence is replaced. The edits are
    the faulty fixtures: one small, named change each to a project that is otherwise silent."""
    changed = dict(texts)
    for name, old, new in edits:
        if name not in changed:
            raise AssertionError(f"the fixture has no file {name}")
        if old not in changed[name]:
            raise AssertionError(f"{name} does not hold {old!r}")
        changed[name] = changed[name].replace(old, new)
    return changed


def parse_all(texts):
    return [parse_text(text, name, SCHEMA) for name, text in texts.items()]


def story_of(path):
    return StorySource.from_file(path, CONSTANTS) if path is not None and Path(path).is_file() else None


def lines_of(result, families=OWN_FAMILIES):
    return [problem for problem in result.problems if getattr(problem, "check_id", "").split("-")[0] in families]


SHOT_SC02_990 = """### SHOT SC02-SH990 Black
- beats: SC02-B01
- lines: 28
- purpose: The story cuts to black.
- because: SC02-B01, line:28
- role: normal
- kind: black
- size: wide
- subject: none
- status: draft
- locked: no

"""

# check ID, what is wrong, which fixture ("key" or "lamp"), the edits, the records that must be named, options
FAULTS = [
    ("ID-01", "a record written twice in one file", "key",
     [(SCENE_1, "### SHOTLIST SC01-LIST", "### BEAT SC01-B02 The red thread, again\n- lines: 14-17\n- status: draft\n"
                                          "- locked: no\n\n### SHOTLIST SC01-LIST")], ["SC01-B02"], {}),
    ("ID-01", "a shot list declaring one shot twice with different content", "key",
     [(SCENE_1, "- approved: yes", "- item: SC01-SH020 | beats: SC01-B02 | role: normal | size: wide | frame: single "
                                   "| subject: CH-MARA | time: 2 | shows: the tin again\n- approved: yes")],
     ["SC01-LIST"], {}),
    ("ID-02", "a reference to an ID that does not exist", "key",
     [(SCENE_1, "- because: SC01-B01, CH-MARA\n", "- because: SC01-B01, CH-MARTA\n")], ["SC01-SH020"], {}),
    ("ID-02", "a camera height at the eye of a character who does not exist", "key",
     [(SCENE_1, "- size: wide\n- subject: CH-MARA", "- size: wide\n- height: eye:CH-MARTA\n- subject: CH-MARA")],
     ["SC01-SH010"], {}),
    ("ID-02", "a reference to a record that was cut", "key",
     [("08 Places and things.md", "### LOCATION LOC-SHOP-DOOR The shop door\n- status: draft",
       "### LOCATION LOC-SHOP-DOOR The shop door\n- status: omitted")], ["SC02"], {}),
    ("ID-03", "a shot number out of the steps of ten with no shot before it", "key",
     [(SCENE_1, "SC01-SH030", "SC01-SH035")], ["SC01-SH035"], {}),
    ("ID-03", "black numbered below 990", "key",
     [(SCENE_2, "SC02-SH990", "SC02-SH020")], ["SC02-SH020"], {}),
    ("ID-04", "a listed shot that was cut (status omitted)", "key",
     [(SCENE_1, '- hear: SC01-D02 | speaker: on_screen | words: "I keep every key."\n- status: draft',
       '- hear: SC01-D02 | speaker: on_screen | words: "I keep every key."\n- status: omitted')], ["SC01-LIST"], {}),
    ("ID-04", "an ID cut earlier (in the manifest) used again", "key", [], ["SC01-SH020"],
     {"manifest": {"omitted_ids": ["SC01-SH020"]}}),
    ("ID-05", "a scene the story's headings do not have", "key",
     [("04 Scene list.md", "END OF FILE | Scene list | 2 records",
       "### SCENE SC03 The street\n- heading: EXT. THE STREET - NIGHT\n- int_ext: ext\n- lines: 27-28\n"
       "- status: draft\n- locked: no\n\nEND OF FILE | Scene list | 3 records")], ['"04 Scene list.md"'], {}),
    ("ID-06", "an ID outside the handout's pre-issued block", "key", [], ["SC01-SH030", "SC01-LIST"],
     {"manifest": {"issued": {"U-08-SC01-B1": {"SHOT": ["SC01-SH010", "SC01-SH020"]}}}}),
    ("ID-07", "a shot missing from its scene's shot list", "key",
     [(SCENE_1, "- item: SC01-SH020 | beats: SC01-B01 | role: normal | size: medium_close_up | frame: single | "
                "subject: CH-MARA | time: 3 | shows: she answers without looking up\n", "")], ["SC01-SH020"], {}),
    ("ID-07", "a listed shot with no SHOT record (after the scene's last batch)", "key",
     [(SCENE_2, SHOT_SC02_990, "")], ["SC02-LIST"], {}),
    ("ID-08", "a shot whose size differs from its list item", "key",
     [(SCENE_1, "- role: normal\n- kind: live\n- size: medium_close_up", "- role: normal\n- kind: live\n- size: close_up")],
     ["SC01-SH020"], {}),
    ("ID-09", "scene numbers of 2 digits in a project that writes 3", "key",
     [("00 Start here.md", "- scene_id_digits: 2", "- scene_id_digits: 3")], ["SC01", "SC01-SH010"], {}),
    ("CITE-01", "a line reference outside its scene's lines", "key",
     [(SCENE_1, "- lines: 5-12", "- lines: 5-20")], ["SC01-B01"], {}),
    ("CITE-02", "a quote anchor that is not found", "key",
     [(SCENE_1, 'line: "small brass key with the red thread"', 'line: "small silver key with the red thread"')],
     ["SC01-SH030"], {}),
    ("CITE-02", "a quote anchor found twice in its scope (the whole story)", "key",
     [("08 Places and things.md", "- first_seen: 14", '- first_seen: "the red thread"')], ["PR-KEY"], {}),
    ("CITE-02", "a story point of fewer than 3 words", "key",
     [("05 Story plan.md", '- crisis: SC02 "It turns the wrong way."', '- crisis: SC02 "It turns"')], ["PLAN"], {}),
    ("CITE-03", "a quoted string that is not in the scene's lines", "key",
     [(SCENE_1, '"under one bare bulb"', '"under a bare bulb"')], ["SC01-SH010"], {}),
    ("CITE-04", "hear words that differ from the speech", "key",
     [(SCENE_1, 'words: "I keep every key."', 'words: "I keep all the keys."')], ["SC01-SH020"], {}),
    ("CITE-05", "a heard speech whose cue lies outside the shot's lines", "key",
     [(SCENE_1, "- hear: SC01-D01 | speaker: off_screen", "- hear: SC01-D02 | speaker: off_screen")],
     ["SC01-SH010"], {}),
    ("CITE-06", "a prose speech with origin story not found word for word", "lamp",
     [(LAMP_SCENE, "- text: It is heavy.", "- text: It is too heavy.")], ["SC01-D02"], {}),
    ("CITE-07", "a cue name that is not among the character's names (build 2)", "key",
     [("07 Characters and voices.md", "- names: OSKAR", "- names: OSKAR KELL")], ["CH-OSKAR"], {}),
]


def fixture_for(which):
    if which == "lamp":
        return read_folder(LAMP_PROJECT), LAMP_STORY
    return read_folder(KEY_PROJECT), KEY_STORY


def check_registry():
    families = load_check_families()
    wrong = []
    for check_id, level in LEVELS_7_2.items():
        definition = REGISTRY.get(check_id)
        if definition is None:
            wrong.append(f"{check_id} not registered")
            continue
        build = 2 if check_id in BUILD_TWO else 1
        if definition.level != level or definition.build != build:
            wrong.append(f"{check_id} registered as {definition.level} build {definition.build}")
        if not definition.plain or re.search(r"\b[A-Z]+-\d{2}\b|\bSC\d", definition.plain):
            wrong.append(f"{check_id} has no plain sentence, or one with a code in it")
    broken = {name: reason for name, reason in families["broken"].items()}
    report(not wrong and not broken, "registry: FORM-01 to 13, ID-01 to 09 and CITE-01 to 07 registered with 7.2's "
           "level and build, each with a plain sentence; every family module present loads",
           "; ".join(wrong + [f"{name}: {reason}" for name, reason in broken.items()])
           or f"{len(LEVELS_7_2)} checks; {len(REGISTRY)} registered in all; missing family modules: "
              f"{', '.join(name.rsplit('.', 1)[-1] for name in families['missing']) or 'none'}")
    top = Path(check_records.__file__).read_text(encoding="utf-8")[:12000]
    needed = ["HOW A FAMILY MODULE REGISTERS ITS CHECKS", "@register_check(", "run.problem(", "run.skip(",
              "register_apply_check", "register_report_section", "checks_coverage_time_state",
              "checks_craft_reasons_words", "checks_plan_generation_film", "checks_sides_geometry"]
    missing = [text for text in needed if text not in top]
    report(not missing, "check_records.py says at its top how family modules register",
           ", ".join(missing) or "the registration note names the four other family modules and every hook")


def check_base_silent():
    for which, name in (("key", "the invented screenplay project"), ("lamp", "the invented prose project")):
        texts, story_path = fixture_for(which)
        result = run_checks(parse_all(texts), SCHEMA, WORDS, CONSTANTS, story=story_of(story_path),
                            check_ids=[check_id for check_id in LEVELS_7_2 if not check_id.startswith("FORM")])
        found = lines_of(result)
        report(not found and not result.crashed, f"faulty fixtures' base: {name} gives no ID or CITE line",
               "; ".join(str(problem) for problem in found[:3]) or f"{len(result.checks_run)} checks run, "
                                                                    f"{len(result.skipped)} skipped")


def check_faults():
    fired_by_check = {}
    for check_id, what, which, edits, must_name, options in FAULTS:
        texts, story_path = fixture_for(which)
        try:
            changed = apply_edits(texts, edits)
        except AssertionError as error:
            report(False, f"{check_id} faulty fixture: {what}", str(error))
            continue
        result = run_checks(parse_all(changed), SCHEMA, WORDS, CONSTANTS, story=story_of(story_path),
                            manifest=options.get("manifest"), step=options.get("step"), check_ids=[check_id])
        lines = [problem for problem in result.problems if problem.check_id == check_id]
        named = {problem.record for problem in lines}
        missing = [record for record in must_name if record not in named]
        level_ok = all(problem.level == LEVELS_7_2[check_id] or LEVELS_7_2[check_id] == "E/W" for problem in lines)
        passed = bool(lines) and not missing and level_ok and not result.crashed
        fired_by_check.setdefault(check_id, []).append(passed)
        detail = str(lines[0]) if lines else "nothing fired"
        if missing:
            detail = f"did not name {', '.join(missing)}; " + detail
        if result.crashed:
            detail = f"crashed: {result.crashed}"
        report(passed, f"{check_id} fires on its faulty fixture ({what})", detail)
    owned = [check_id for check_id in LEVELS_7_2 if not check_id.startswith("FORM")]
    without = [check_id for check_id in owned if check_id not in fired_by_check]
    report(not without, "every ID and CITE check has at least one faulty fixture", ", ".join(without) or
           f"{len(FAULTS)} faulty fixtures for {len(owned)} checks")


def check_batches():
    """ID-07 during step 8 looks only at the batches written so far, and in full after the scene's last batch
    (7.2); a batch whose expected count is not known yet (as apply first writes it) never stops the check."""
    texts = read_folder(KEY_PROJECT)
    scene_text = texts[SCENE_1]
    start = scene_text.index("### SHOT SC01-SH030")
    end = scene_text.index("END OF FILE")
    without_030 = apply_edits(texts, [(SCENE_1, scene_text[start:end], "")])
    first_batch = {"expected": 2, "received": 2, "first": "SC01-SH010", "last": "SC01-SH020"}
    cases = [
        ("the second batch not written yet", {"U-08-SC01-B1": first_batch,
                                              "U-08-SC01-B2": {"expected": 1, "first": "SC01-SH030",
                                                               "last": "SC01-SH030"}}, False),
        ("the second batch's count not known yet", {"U-08-SC01-B1": first_batch,
                                                    "U-08-SC01-B2": {"expected": None, "received": None}}, False),
        ("every batch received", {"U-08-SC01-B1": first_batch,
                                  "U-08-SC01-B2": {"expected": 1, "received": 1, "first": "SC01-SH030",
                                                   "last": "SC01-SH030"}}, True),
    ]
    wrong = []
    for what, batches, should_fire in cases:
        result = run_checks(parse_all(without_030), SCHEMA, WORDS, CONSTANTS, story=story_of(KEY_STORY), step=8,
                            manifest={"batches": {"SC01": batches}}, check_ids=["ID-07"])
        fired = [problem for problem in result.problems if problem.check_id == "ID-07"
                 and problem.record == "SC01-LIST" and "SC01-SH030" in problem]
        if bool(fired) != should_fire or result.crashed:
            wrong.append(f"{what}: {'fired' if fired else 'silent'}{' ' + str(result.crashed) if result.crashed else ''}")
    report(not wrong, "ID-07 during step 8: a listed shot of a batch not yet written is not reported; after the "
           "scene's last batch it is", "; ".join(wrong) or f"{len(cases)} cases")


def check_form_through_framework():
    """WP2's grammar fixtures, run through run_checks (so through the registry and its adapter)."""
    expected = json.loads((GRAMMAR / "expected results.json").read_text(encoding="utf-8"))
    fired = set()
    failures = []
    for entry in expected["runs"]:
        settings = entry.get("context") or {}
        if settings.get("written_by_ai") or not entry.get("must_fire"):
            continue  # inbox runs are apply's; FORM-11 on stored files is tested below with a baseline
        files = [parse_file(GRAMMAR / name, name, SCHEMA) for name in entry["files"]]
        wanted = sorted({check_id for check_id, _ in entry["must_fire"]})
        result = run_checks(files, SCHEMA, WORDS, CONSTANTS, step=settings.get("step"), check_ids=wanted)
        named = {(problem.check_id, problem.record) for problem in result.problems}
        named |= {(note.check_id, note.record) for note in result.tidy_notes}
        for check_id, record in entry["must_fire"]:
            if (check_id, record) in named:
                fired.add(check_id)
            else:
                failures.append(f"{entry['name']}: {check_id} {record}")
    # FORM-11 on stored files: a locked record changed since the checker last saw it
    texts = read_folder(KEY_PROJECT)
    locked_texts = apply_edits(texts, [("07 Characters and voices.md", "- gesture: sorts keys into a tin | line: 5\n"
                                        "- status: draft\n- locked: no",
                                        "- gesture: sorts keys into a tin | line: 5\n- status: draft\n- locked: yes")])
    baseline_files = parse_all(locked_texts)
    baseline_run = run_checks(baseline_files, SCHEMA, WORDS, CONSTANTS, check_ids=["FORM-11"])
    baseline = {key: record for key, record in baseline_run.run.index.items()
                if (record.get("locked") or "") == "yes"}
    changed = apply_edits(locked_texts, [("07 Characters and voices.md", "- gesture: sorts keys into a tin | line: 5",
                                          "- gesture: sorts keys into a box | line: 5")])
    unchanged_result = run_checks(parse_all(locked_texts), SCHEMA, WORDS, CONSTANTS, check_ids=["FORM-11"],
                                  locked_baseline=baseline)
    changed_result = run_checks(parse_all(changed), SCHEMA, WORDS, CONSTANTS, check_ids=["FORM-11"],
                                locked_baseline=baseline)
    form_11 = [problem for problem in changed_result.problems if problem.check_id == "FORM-11"]
    # code resolving a locked story point to its beat (' = SC02-B01', 5.6) is not a change
    plan_locked = apply_edits(locked_texts, [("05 Story plan.md", '- crisis: SC02 "It turns the wrong way."\n'
                                              "- status: draft\n- locked: no", '- crisis: SC02 "It turns the wrong '
                                              'way."\n- status: draft\n- locked: yes')])
    plan_run = run_checks(parse_all(plan_locked), SCHEMA, WORDS, CONSTANTS, check_ids=["FORM-11"])
    plan_baseline = {key: record for key, record in plan_run.run.index.items() if (record.get("locked") or "") == "yes"}
    resolved = apply_edits(plan_locked, [("05 Story plan.md", '- crisis: SC02 "It turns the wrong way."',
                                          '- crisis: SC02 "It turns the wrong way." = SC02-B01')])
    resolved_result = run_checks(parse_all(resolved), SCHEMA, WORDS, CONSTANTS, check_ids=["FORM-11"],
                                 locked_baseline=plan_baseline)
    if form_11 and form_11[0].record == "CH-MARA" and not unchanged_result.problems \
            and form_11[0].file_name == "07 Characters and voices.md" and form_11[0].line_number \
            and not resolved_result.problems:
        fired.add("FORM-11")
    else:
        failures.append(f"FORM-11 against the checker's copy: {[str(problem) for problem in form_11]}; a resolved "
                        f"story point: {[str(problem) for problem in resolved_result.problems]}")
    not_fired = [check_id for check_id in LEVELS_7_2 if check_id.startswith("FORM") and check_id not in fired]
    report(not failures and not not_fired, "FORM-01 to FORM-13 fire through the framework on WP2's grammar fixtures "
           "(FORM-11 on stored files against the checker's copy of a locked record, and not when code only adds the "
           "beat a story point resolves to)",
           "; ".join(failures + [f"{check_id} never fired" for check_id in not_fired])
           or f"all 13 fire; FORM-11 names {form_11[0].record} at {form_11[0].file_name}, line {form_11[0].line_number}")


def check_gold(whole_story):
    files = [parse_file(GOLD_SCENE, GOLD_SCENE.name, SCHEMA), parse_file(GOLD_CONTEXT, GOLD_CONTEXT.name, SCHEMA)]
    own = list(LEVELS_7_2)
    stories = [("the scene 10 excerpt", EXCERPT if EXCERPT.is_file() else None)]
    if whole_story:
        stories.append(("the whole story", Path(whole_story) if Path(whole_story).is_file() else None))
    for story_name, story_path in stories:
        if story_path is None:
            info(f"gold with {story_name}: skipped: story not present")
            story = None
        else:
            story = story_of(story_path)
        for step in (None, 7, 8):
            result = run_checks(files, SCHEMA, WORDS, CONSTANTS, story=story, step=step, check_ids=own)
            found = lines_of(result)
            where = "check --all" if step is None else f"check --step {step}"
            skipped_story = [why for check_id, why in result.skipped if "story not present" in why]
            detail = "; ".join(str(problem) for problem in found[:3])
            if not detail:
                detail = f"{len(result.checks_run)} checks run, no line"
                if story is None and skipped_story:
                    detail += "; the story checks say skipped: story not present"
            report(not found and not result.crashed,
                   f"gold (examples 01 and 02) with {story_name if story else 'no story'}, {where}: every FORM, ID "
                   "and CITE check is silent", detail)
            if story is None:
                break
        if story is not None:
            excerpt_skips = [why for check_id, why in result.skipped if "not in the excerpt" in why]
            if story.excerpt:
                report(bool(excerpt_skips), "gold with the excerpt: references into scenes outside the excerpt are "
                       "skipped as 'not in the excerpt', never reported", f"{len(excerpt_skips)} skip lines")
    # all families present, for information: other builders' checks on the gold
    story = story_of(EXCERPT) if EXCERPT.is_file() else None
    result = run_checks(files, SCHEMA, WORDS, CONSTANTS, story=story)
    others = [problem for problem in result.problems if problem.check_id.split("-")[0] not in OWN_FAMILIES]
    if others:
        info(f"gold: {len(others)} lines from other families (their builders' business), first: {others[0]}")


# ---------------------------------------------------------------- the command

def stage(arguments, cwd=None):
    environment = dict(os.environ)
    environment["STAGE_LOCK_WAIT_SECONDS"] = "2"
    completed = subprocess.run([sys.executable, str(STAGE)] + arguments, capture_output=True, text=True,
                               encoding="utf-8", cwd=cwd or str(REPOSITORY), env=environment, timeout=300)
    return completed.returncode, completed.stdout + completed.stderr


def make_gold_project(folder):
    """A project folder from the gold: the scene file as 11 Scenes/Scene 10 - Saye's kitchen.md and each '## From
    NN <name>' part of the context file as the numbered file it came from."""
    folder.mkdir(parents=True)
    (folder / "11 Scenes").mkdir()
    shutil.copy(GOLD_SCENE, folder / "11 Scenes" / "Scene 10 - Saye's kitchen.md")
    context_lines = GOLD_CONTEXT.read_text(encoding="utf-8").splitlines()
    sections = {}
    current = None
    for line in context_lines:
        match = re.match(r"^## From (\d\d .+)$", line)
        if match:
            current = match.group(1).strip()
            sections[current] = []
            continue
        if line.startswith("END OF FILE"):
            current = None
            continue
        if current is not None:
            sections[current].append(line)
    for name, lines in sections.items():
        count = sum(1 for line in lines if line.startswith("### "))
        text = "\n".join([f"# {name[3:]}", "", "The records scene 10 uses from this file (made from the gold example "
                          "for a test).", "", DIVIDER_LINE, ""] + lines).rstrip("\n")
        text += f"\n\nEND OF FILE | {name[3:]} | {count} records\n"
        (folder / f"{name}.md").write_text(text, encoding="utf-8")
    return folder


def above_divider(text):
    return text.split(DIVIDER_LINE, 1)[0]


def plain_part_problems(text):
    """Codes, IDs and abbreviations in the plain part of a report (WORDS-04's rule, checked simply)."""
    plain = above_divider(text)
    found = []
    for pattern, what in ((r"\b(FORM|ID|CITE|COVER|TIME|STATE|SIDE|GEOM|CRAFT|INFO|REASON|WORDS|PLAN|GEN|FILM)-\d\d\b",
                           "a check ID"), (r"\bSC\d{2,3}", "a scene ID"), (r"\b[A-Z]{2,5}-[A-Z0-9]", "a record ID")):
        match = re.search(pattern, plain)
        if match:
            found.append(f"{what} ({match.group(0)})")
    for word in WORDS.get("abbreviations", {}).get("words", []):
        if re.search(r"(?<![\w.])" + re.escape(word) + r"(?![\w])", plain):
            found.append(f"the abbreviation {word}")
    return found


def check_command(whole_story):
    temporary = Path(tempfile.mkdtemp(prefix="stage wp4b "))
    try:
        run_command_groups(temporary)
    finally:
        shutil.rmtree(temporary, ignore_errors=True)


def run_command_groups(temporary):
    project = make_gold_project(temporary / "The Catch")
    health = project / "13 Health check.md"
    story_arguments = ["--story", str(EXCERPT)] if EXCERPT.is_file() else []

    # 1. check --all on the gold project: no FORM, ID or CITE line; the report; the exit code follows the E lines
    code, output = stage(["check", "--all", "--project", str(project)] + story_arguments)
    own = [line for line in output.splitlines() if re.match(r"^[EWN] (FORM|ID|CITE)-\d\d ", line)]
    errors = [line for line in output.splitlines() if re.match(r"^E [A-Z]+-\d\d ", line)]
    text = health.read_text(encoding="utf-8") if health.is_file() else ""
    first_line = text.splitlines()[0] if text else ""
    plain_faults = plain_part_problems(text)
    records_after = parse_file(health, health.name, SCHEMA) if health.is_file() else None
    start_here = (project / "00 Start here.md").read_text(encoding="utf-8")
    machine = project / "For machines - do not edit"
    manifest = json.loads((machine / "manifest.json").read_text(encoding="utf-8")) \
        if (machine / "manifest.json").is_file() else {}
    locked = json.loads((machine / "locked records.json").read_text(encoding="utf-8")).get("records", {}) \
        if (machine / "locked records.json").is_file() else {}
    passed = (not own and code == (1 if errors else 0) and first_line.startswith("In short: ")
              and DIVIDER_LINE in text and not plain_faults and records_after is not None
              and records_after.end_line is not None and "checker_last_run: 20" in start_here
              and locked and manifest.get("last_check") and manifest.get("files"))
    report(passed, "check --all on a project made from the gold: no FORM, ID or CITE line; exit code 1 exactly when "
           "error lines are printed (7.3); 13 Health check.md starts 'In short:', has the divider and an END line, "
           "and its plain part holds no code, ID or abbreviation; checker_last_run set; the manifest records the "
           "check and the locked records are kept for FORM-11", f"exit {code}; first line: {first_line!r}; "
           f"{len(errors)} error lines from other families; {len(locked)} locked records kept"
           + (f"; own lines: {own[:2]}" if own else "") + (f"; plain part: {plain_faults}" if plain_faults else ""))
    if errors:
        info(f"other families' error lines on the gold project (not this package's): {errors[0]}")

    # 2. tidy fixes: made, written back, logged, kept in history
    scene_file = project / "11 Scenes" / "Scene 10 - Saye's kitchen.md"
    original = scene_file.read_text(encoding="utf-8")
    slipped = original.replace("- screen_time: 15\n", "- Screen time: 15\n", 1)
    scene_file.write_text(slipped, encoding="utf-8")
    code, output = stage(["check", "--all", "--project", str(project)] + story_arguments)
    after = scene_file.read_text(encoding="utf-8")
    history = list((project / "For machines - do not edit" / "history").rglob("Scene 10 - Saye's kitchen.md"))
    start_here = (project / "00 Start here.md").read_text(encoding="utf-8")
    text = health.read_text(encoding="utf-8")
    logged = re.search(r"^\d{3} \d{4}-\d\d-\d\d Checked everything: made 1 small fix", start_here, re.MULTILINE)
    log_lines = (project / "For machines - do not edit" / "log.jsonl").read_text(encoding="utf-8").splitlines()
    passed = (slipped != original and after == original and history
              and history[-1].read_text(encoding="utf-8") == slipped and logged
              and "1 small fix of spelling, case or spacing" in above_divider(text)
              and "tidied: 11 Scenes/Scene 10 - Saye's kitchen.md" in output
              and any('"command": "check"' in line for line in log_lines))
    report(passed, "tidy fixes: 'Screen time' becomes screen_time in the file, the old file is kept in history, a "
           "numbered entry is added to 00 Start here's log and a line to log.jsonl, and the report counts the fix",
           (logged.group(0) if logged else "no log entry") + f"; history copies: {len(history)}")

    # 3. a locked value changed by hand is caught on the next check (FORM-11), and the catch stays until fixed
    context_file = project / "08 Places and things.md"
    places = context_file.read_text(encoding="utf-8")
    lamp = re.search(r"### PROP PR-LAMP[^\n]*\n(?:- [^\n]*\n)*?- fixed_description: ([^\n]*)\n", places)
    changed_places = places.replace(lamp.group(1), lamp.group(1) + " A red stripe.", 1) if lamp else places
    context_file.write_text(changed_places, encoding="utf-8")
    code_changed, output_changed = stage(["check", "--all", "--project", str(project)] + story_arguments)
    code_again, output_again = stage(["check", "--all", "--project", str(project)] + story_arguments)
    context_file.write_text(places, encoding="utf-8")
    code_fixed, output_fixed = stage(["check", "--all", "--project", str(project)] + story_arguments)
    caught = [line for line in output_changed.splitlines() if line.startswith("E FORM-11 PR-LAMP fixed_description")]
    passed = (lamp and caught and code_changed == 1 and "E FORM-11 PR-LAMP" in output_again and code_again == 1
              and "FORM-11" not in output_fixed and "[08 Places and things.md, line" in caught[0])
    report(passed, "FORM-11 on stored files: a locked record's value changed by hand is an error on the next check "
           "(exit 1), stays one on the check after, and goes when the value is put back",
           caught[0] if caught else f"exit {code_changed}; nothing caught")

    # 4. --scene SC10 keeps only scene 10's lines: a whole-film fault is left out and counted
    context_file.write_text(changed_places, encoding="utf-8")
    code_scene, output_scene = stage(["check", "--scene", "SC10", "--project", str(project)] + story_arguments)
    context_file.write_text(places, encoding="utf-8")
    scene_errors = [line for line in output_scene.splitlines() if re.match(r"^E [A-Z]+-\d\d ", line)]
    outside = [line for line in output_scene.splitlines() if re.match(r"^[EWN] [A-Z]+-\d\d (?!SC10)", line)]
    passed = ("FORM-11" not in output_scene and "Left out:" in output_scene and not outside
              and code_scene == (1 if scene_errors else 0))
    report(passed, "check --scene SC10 reports only scene 10's records and files; the whole-film fault is left out "
           "and counted, and the exit code follows the lines printed",
           next((line for line in output_scene.splitlines() if line.startswith("Left out:")), "no 'Left out' line")
           + (f"; lines about other records: {outside[:2]}" if outside else ""))

    # 5. an ID fault in the scene gives exit 1 with --scene; --step 8 and --film run
    scene_file.write_text(original.replace("- size: close_up\n- angle: eye_level\n- height: eye:CH-IONA\n- lens_mm: 50",
                                           "- size: medium\n- angle: eye_level\n- height: eye:CH-IONA\n- lens_mm: 50", 1),
                          encoding="utf-8")
    code_fault, output_fault = stage(["check", "--step", "8", "--scene", "SC10", "--project", str(project)]
                                     + story_arguments)
    scene_file.write_text(original, encoding="utf-8")
    id_08 = [line for line in output_fault.splitlines() if line.startswith("E ID-08 SC10-SH150 size")]
    code_film, output_film = stage(["check", "--film", "--project", str(project)] + story_arguments)
    film_text = health.read_text(encoding="utf-8")
    # changed after the full run (Project notes 32, problem 7): once a full check has run, a partial check (here the
    # film pass) keeps the full check's plain part and replaces only the checker's lines below the divider
    passed = (id_08 and code_fault == 1 and code_film in (0, 1)
              and re.search(r"^Checked: everything, on ", above_divider(film_text), re.MULTILINE)
              and "check --film" in film_text.split(DIVIDER_LINE, 1)[1]
              and "In short:" in output_film)
    report(passed, "check --step 8 --scene SC10 with a shot whose size differs from its list item gives E ID-08 and "
           "exit 1; check --film runs and reports, keeping the full check's plain part",
           (id_08[0] if id_08 else f"exit {code_fault}") + f"; --film exit {code_film}")

    # 6. without any story the story checks are skipped, never failed
    code_none, output_none = stage(["check", "--all", "--project", str(project)])
    passed = "story not present" in output_none and not re.search(r"^E CITE-", output_none, re.MULTILINE)
    report(passed, "check with no story at all: the story checks say 'story not present' and no CITE error is printed",
           next((line for line in output_none.splitlines() if "story not present" in line), "no skip line")[:140])

    # 7. exit 2: could not run, one plain line, nothing written
    before = {path: path.read_bytes() for path in project.rglob("*.md")}
    cases = [(["check", "--story", str(temporary / "no such story.txt")], "was not found"),
             (["check", "--step", "42"], "is not a step number"),
             (["check", "--scene", "the kitchen"], "is not a scene"),
             (["check", "--all", "--step", "3"], "not both")]
    wrong = []
    for arguments, words in cases:
        code, output = stage(arguments + ["--project", str(project)])
        if code != 2 or words not in output:
            wrong.append(f"{' '.join(arguments[:3])}: exit {code}, {output.strip()[:100]}")
    empty = temporary / "an empty folder"
    empty.mkdir()
    code, output = stage(["check"], cwd=str(empty))
    if code != 2 or not output.strip():
        wrong.append(f"check outside any project: exit {code}, {output.strip()[:100]}")
    after = {path: path.read_bytes() for path in project.rglob("*.md")}
    if before != after:
        wrong.append("a file changed")
    report(not wrong, "exit 2 with one plain line and no file changed: a missing story file, a bad step, a bad scene, "
           "--all with --step, no project", "; ".join(wrong) or f"{len(cases) + 1} cases")

    # 8. the guards apply runs on an inbox: ID-01, ID-04, ID-06 refuse it and no numbered file changes
    key_project = temporary / "The key"
    shutil.copytree(KEY_PROJECT, key_project)
    machine = key_project / "For machines - do not edit"
    (machine / "inbox").mkdir(parents=True)
    (machine / "manifest.json").write_text(json.dumps({
        "manifest_version": 1, "files": {}, "locks": [], "units_done": [], "batches": {},
        "omitted_ids": ["SC01-SH040"],
        "issued": {"U-08-SC01-B2": {"SHOT": ["SC01-SH040", "SC01-SH060"]}}}, indent=1), encoding="utf-8")
    shot = ("### SHOT {identifier} {title}\n- beats: SC01-B02\n- lines: 14-17\n- purpose: The key again, closer.\n"
            "- because: SC01-B02\n- role: normal\n- kind: insert\n- size: close_up\n\n")
    inbox_text = ("# Scene 1, shots 040 to 060\n\n" + DIVIDER_LINE + "\n\n"
                  + shot.format(identifier="SC01-SH040", title="Cut before")
                  + shot.format(identifier="SC01-SH050", title="Inside the block")
                  + shot.format(identifier="SC01-SH050", title="Inside the block, twice")
                  + shot.format(identifier="SC01-SH070", title="Outside the block")
                  + "END OF FILE | Scene 1 shots 040-070 | 4 records\n")
    inbox = machine / "inbox" / "U-08-SC01-B2.md"
    inbox.write_text(inbox_text, encoding="utf-8")
    before = {path: path.read_bytes() for path in key_project.rglob("*.md") if "For machines" not in str(path)}
    code, output = stage(["apply", "U-08-SC01-B2.md", "--project", str(key_project)])
    after = {path: path.read_bytes() for path in key_project.rglob("*.md") if "For machines" not in str(path)}
    wanted = ["E ID-04 SC01-SH040", "E ID-01 SC01-SH050", "E ID-06 SC01-SH070"]
    missing = [text for text in wanted if text not in output]
    inside = "E ID-06 SC01-SH050" in output
    passed = code == 1 and not missing and not inside and before == after and inbox.is_file()
    report(passed, "apply refuses an inbox with a shot cut earlier (ID-04), a shot written twice (ID-01) and a shot "
           "outside the issued block (ID-06), and changes no numbered file",
           f"exit {code}; " + ("; ".join(f"missing {text}" for text in missing) or "all three named")
           + ("; SH050 wrongly outside" if inside else ""))

    # 9. the same guards let a good inbox through: a new shot inside the block, and a change to a stored shot
    inbox.write_text("# Scene 1, shot 050\n\n" + DIVIDER_LINE + "\n\n"
                     + shot.format(identifier="SC01-SH050", title="Inside the block")
                     + "### SHOT SC01-SH010 Mara at her tin\n- purpose: Mara at work, and the key Oskar asks about.\n\n"
                     + "END OF FILE | Scene 1 shot 050 | 2 records\n", encoding="utf-8")
    code, output = stage(["apply", "U-08-SC01-B2.md", "--project", str(key_project)])
    scene_text = (key_project / SCENE_1).read_text(encoding="utf-8")
    passed = code == 0 and "### SHOT SC01-SH050" in scene_text and not re.search(r"^E ID-0[146]", output, re.MULTILINE)
    report(passed, "apply accepts a good inbox: a new shot inside the issued block and a change to a stored shot "
           "outside it", f"exit {code}; " + (output.strip().splitlines()[-1][:120] if output.strip() else ""))


def main():
    parser = argparse.ArgumentParser(description="Acceptance test of work package 4b (the check framework, ID and CITE).")
    parser.add_argument("--story", help="The Catch, the whole story (optional): the gold is also checked against it")
    arguments = parser.parse_args()
    if not EXCERPT.is_file():
        info("the scene 10 excerpt is missing: skipped: story not present (the gold's story checks)")
    check_registry()
    check_base_silent()
    check_faults()
    check_batches()
    check_form_through_framework()
    check_gold(arguments.story)
    check_command(arguments.story)
    failures = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failures else 'FAIL'} ({failures} failing groups)")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
