"""The acceptance test of work package 4c: the COVER, TIME and STATE checks of blueprint 7.2
(.claude/skills/breaking-down-stories/tools/stage_tools/checks_coverage_time_state.py).

What it proves (blueprint 7.2, 14.2 row WP4):
- every COVER, TIME and STATE check of 7.2 is registered with 7.2's level and build and a plain sentence;
- one faulty fixture per build-1 check (tests/fixtures/coverage time and state/faults.json: named edits to a temporary
  copy of the WP12a gold) fires with 7.2's message format (level, check ID, record, field, what is wrong, then the
  fix), naming the record and the field it should, placed in a file and line; TIME-01's line is exactly 7.2's
  example; the build-2 checks TIME-07 and TIME-10 fire on theirs, and STATE-04 is a stub that says why it skips;
- all these checks are silent on the WP12a gold fixture (examples/01 and 02 with the scene 10 excerpt, and with the
  whole story when --story is given), with no story at all (the story checks then say "story not present"), on the
  chat-saved copy of scene 10, and through the command stage.py check on a project made from the gold;
- before step 8 the coverage checks read the list items, and during step 8 they look only at the batches written
  so far, then at everything after the scene's last batch.

Usage: python tests/wp4c_acceptance.py [--story "<The Catch, the whole story>"]
Without the scene 10 excerpt the story groups say "skipped: story not present". Standard library only.
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

from stage_tools.check_records import REGISTRY, StorySource, load_check_families, run_checks  # noqa: E402
from stage_tools.record_format import DIVIDER_LINE, load_skill_data, parse_text  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
FIXTURES = REPOSITORY / "tests" / "fixtures"
FAULTS_FILE = FIXTURES / "coverage time and state" / "faults.json"
EXCERPT = FIXTURES / "The Catch - lines 397-489.txt"
CHAT_FOLDER = FIXTURES / "chat saved scene 10"
GOLD_FILES = {"scene": SKILL / "examples" / "01 The Catch - scene 10.md",
              "context": SKILL / "examples" / "02 The Catch - scene 10 - context.md"}

OWN_FAMILIES = ("COVER", "TIME", "STATE")
LEVELS_7_2 = {
    "COVER-01": "E", "COVER-02": "E", "COVER-03": "E", "COVER-04": "E", "COVER-05": "E", "COVER-06": "E",
    "COVER-07": "E", "COVER-08": "W",
    "TIME-01": "E", "TIME-02": "E", "TIME-03": "W", "TIME-04": "E", "TIME-05": "E", "TIME-06": "W", "TIME-07": "W",
    "TIME-08": "E", "TIME-09": "W", "TIME-10": "W",
    "STATE-01": "E", "STATE-02": "E", "STATE-03": "E", "STATE-04": "W",
}
BUILD_TWO = {"TIME-07", "TIME-10", "STATE-04"}
OWN_CHECKS = list(LEVELS_7_2)
# 7.2: "Every message is one line: level, check ID, record, field, what is wrong, the allowed values or the fix."
LINE_FORM = re.compile(r"^(?P<level>[EWN]) (?P<check>[A-Z]+-\d{2}) (?P<record>\S+) (?P<field>[a-z_]+) (?P<what>.+?)\. "
                       r"(?P<fix>(?:Fix|Allowed): .+?)(?: \[(?P<place>[^\]]+)\])?$")
PLACE = re.compile(r" \[[^\]]+\]$")

RESULTS = []


def report(passed, group, detail=""):
    RESULTS.append(passed)
    print(f"{'PASS' if passed else 'FAIL'}  {group}" + (f": {detail}" if detail else ""), flush=True)


def info(line):
    print(f"INFO  {line}", flush=True)


# ---------------------------------------------------------------- the gold, and faults made from it by named edits

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


def apply_edit(texts, edit):
    """One named edit to a copy of the gold (see the note at the top of faults.json)."""
    name = edit["file"]
    lines = texts[name].split("\n")
    if "add_after_record" in edit:
        _, end = record_block(lines, edit["add_after_record"])
        while end > 0 and not lines[end - 1].strip():
            end -= 1
        added = [""] + edit["text"].rstrip("\n").split("\n")
        lines[end:end] = added
    elif "remove_record" in edit:
        first, end = record_block(lines, edit["remove_record"])
        del lines[first:end]
    else:
        first, end = record_block(lines, edit["record"])
        block = "\n".join(lines[first:end]) + "\n"
        if edit["find"] not in block:
            raise AssertionError(f"{edit['record']} does not hold {edit['find']!r}")
        block = block.replace(edit["find"], edit["replace"], 1)
        lines[first:end] = block[:-1].split("\n") if block.endswith("\n") else block.split("\n")
    texts[name] = "\n".join(lines)
    return texts


def parse_texts(texts):
    return [parse_text(texts["scene"], GOLD_FILES["scene"].name, SCHEMA),
            parse_text(texts["context"], GOLD_FILES["context"].name, SCHEMA)]


def story_from(path, edits=(), folder=None):
    """The story for a run: the excerpt (or the file given), with story edits made in a temporary copy."""
    if path is None or not Path(path).is_file():
        return None
    if not edits:
        return StorySource.from_file(path, CONSTANTS)
    text = Path(path).read_text(encoding="utf-8")
    for edit in edits:
        if edit["find"] not in text:
            raise AssertionError(f"the story does not hold {edit['find']!r}")
        text = text.replace(edit["find"], edit["replace"], 1)
    changed = Path(folder) / Path(path).name
    changed.write_text(text, encoding="utf-8")
    return StorySource.from_file(changed, CONSTANTS)


def own_lines(result):
    return [problem for problem in result.problems if getattr(problem, "check_id", "").split("-")[0] in OWN_FAMILIES]


def check_ids_of(problems):
    return sorted({problem.check_id for problem in problems})


# ---------------------------------------------------------------- the groups

def check_registry():
    load_check_families()
    wrong = []
    for check_id, level in LEVELS_7_2.items():
        definition = REGISTRY.get(check_id)
        if definition is None:
            wrong.append(f"{check_id} not registered")
            continue
        build = 2 if check_id in BUILD_TWO else 1
        if definition.level != level or definition.build != build:
            wrong.append(f"{check_id} registered as {definition.level}, build {definition.build}")
        if not definition.plain or re.search(r"[A-Z]{2,}-\d|\bSC\d", definition.plain):
            wrong.append(f"{check_id} has no plain sentence, or one with a code in it")
        if not definition.module.endswith("checks_coverage_time_state"):
            wrong.append(f"{check_id} comes from {definition.module}")
    extra = [check_id for check_id, definition in REGISTRY.items()
             if definition.family in OWN_FAMILIES and check_id not in LEVELS_7_2]
    wrong += [f"{check_id} is not a check of 7.2" for check_id in extra]
    report(not wrong, "registry: COVER-01 to 08, TIME-01 to 10 and STATE-01 to 04 registered with 7.2's level and "
           "build, each with a plain sentence", "; ".join(wrong) or f"{len(LEVELS_7_2)} checks")
    module = TOOLS / "stage_tools" / "checks_coverage_time_state.py"
    first = module.read_text(encoding="utf-8").lstrip()
    report(first.startswith('"""checks_coverage_time_state.py:'), "the module starts with a plain note saying what it does")
    families = load_check_families()
    name = "stage_tools.checks_coverage_time_state"
    report(name not in families["missing"] and name not in families["broken"],
           "check_records loads this family module under its planned name",
           families["broken"].get(name, "loaded"))


def check_gold(whole_story):
    files = parse_texts(gold_texts())
    stories = [("the scene 10 excerpt", EXCERPT)]
    if whole_story:
        stories.append(("the whole story", Path(whole_story)))
    for story_name, path in stories:
        story = story_from(path)
        if story is None:
            info(f"gold with {story_name}: skipped: story not present")
            continue
        for step in (None, 7, 8):
            result = run_checks(files, SCHEMA, WORDS, CONSTANTS, story=story, step=step, check_ids=OWN_CHECKS)
            found = own_lines(result)
            where = "check --all" if step is None else f"check --step {step}"
            detail = "; ".join(str(problem) for problem in found[:3]) or \
                f"{len(result.checks_run)} checks run, no line, {len(result.skipped)} skip lines"
            if result.crashed:
                detail += f"; crashed: {result.crashed}"
            report(not found and not result.crashed and len(result.checks_run) == len(OWN_CHECKS),
                   f"gold (examples 01 and 02) with {story_name}, {where}: every COVER, TIME and STATE check is silent",
                   detail)
    result = run_checks(files, SCHEMA, WORDS, CONSTANTS, story=None, check_ids=OWN_CHECKS)
    missing = sorted({check_id for check_id, why in result.skipped if "story not present" in why})
    report(not own_lines(result) and not result.crashed and {"COVER-01", "COVER-02", "TIME-01", "STATE-02"} <= set(missing),
           "gold with no story at all: silent, and the checks that need the story say 'story not present'",
           f"skipped as story not present: {', '.join(missing)}")


def check_chat_copy():
    if not CHAT_FOLDER.is_dir():
        info("the chat-saved copy of scene 10 is missing: skipped")
        return
    files = [parse_text(path.read_text(encoding="utf-8"), str(path.relative_to(CHAT_FOLDER)).replace(os.sep, "/"),
                        SCHEMA) for path in sorted(CHAT_FOLDER.rglob("*.md"))]
    story = story_from(EXCERPT)
    if story is None:
        info("the chat-saved copy: skipped: story not present")
        return
    for step in (None, 8):
        result = run_checks(files, SCHEMA, WORDS, CONSTANTS, story=story, step=step, check_ids=OWN_CHECKS)
        found = own_lines(result)
        report(not found and not result.crashed,
               f"the chat-saved copy of scene 10 (quote anchors, two batch files) with the excerpt, "
               f"{'check --all' if step is None else 'check --step 8'}: silent",
               "; ".join(str(problem) for problem in found[:3]) or f"{len(result.checks_run)} checks run, no line")


def run_fault(fault, temporary):
    texts = gold_texts()
    for edit in fault.get("edits", []):
        texts = apply_edit(texts, edit)
    story = None if fault.get("story") == "none" else story_from(EXCERPT, fault.get("story_edits", ()), temporary)
    return run_checks(parse_texts(texts), SCHEMA, WORDS, CONSTANTS, story=story, step=fault.get("step"),
                      manifest=fault.get("manifest"), check_ids=OWN_CHECKS)


def check_faults():
    faults = json.loads(FAULTS_FILE.read_text(encoding="utf-8"))["faults"]
    temporary = Path(tempfile.mkdtemp(prefix="stage wp4c "))
    fired = {}
    try:
        for fault in faults:
            if fault.get("needs_story") and not EXCERPT.is_file():
                info(f"{fault['check']} ({fault['about']}): skipped: story not present")
                continue
            if fault.get("story_edits") and not EXCERPT.is_file():
                info(f"{fault['check']} ({fault['about']}): skipped: story not present")
                continue
            result = run_fault(fault, temporary)
            if result.crashed:
                report(False, f"{fault['check']} fires on its faulty fixture ({fault['about']})",
                       f"crashed: {result.crashed}")
                continue
            candidates = [problem for problem in result.problems if problem.check_id == fault["check"]]
            matching = [problem for problem in candidates
                        if problem.record == fault["record"] and problem.field_name == fault["field"]
                        and problem.level == fault["level"]
                        and fault.get("holds", "") in str(problem)]
            wrong = []
            if not matching:
                wrong.append("no matching line; got: " + ("; ".join(str(problem) for problem in candidates[:3])
                                                          or "no line of this check"))
            else:
                line = str(matching[0])
                form = LINE_FORM.match(line)
                if form is None or "\n" in line:
                    wrong.append(f"not in 7.2's form: {line}")
                if not (matching[0].file_name and matching[0].line_number):
                    wrong.append(f"not placed in a file and line: {line}")
                if fault.get("exact") and PLACE.sub("", line) != fault["exact"]:
                    wrong.append(f"not exactly 7.2's line: {PLACE.sub('', line)!r}")
            if not wrong:
                fired.setdefault(fault["check"], []).append(fault["about"])
            label = f"{fault['check']}{' (build 2)' if fault.get('build') == 2 else ''} fires on its faulty fixture " \
                    f"({fault['about']})"
            report(not wrong, label, "; ".join(wrong) or str(matching[0]))
    finally:
        shutil.rmtree(temporary, ignore_errors=True)
    build_one = [check_id for check_id in LEVELS_7_2 if check_id not in BUILD_TWO]
    missing = [check_id for check_id in build_one if check_id not in fired]
    if not EXCERPT.is_file():
        missing = [check_id for check_id in missing
                   if not all(fault.get("needs_story") for fault in faults if fault["check"] == check_id)]
    report(not missing, "every build-1 COVER, TIME and STATE check fires on at least one faulty fixture"
           + ("" if EXCERPT.is_file() else " that can be seen without the story"),
           f"missing: {', '.join(missing)}" if missing else
           f"{sum(len(found) for found in fired.values())} faulty fixtures fired for {len(fired)} checks")


def without_later_shots(texts, first_later):
    """The gold with every SHOT from first_later on (and the cut after shot 200) removed: only batch 1 written."""
    numbers = [int(match) for match in re.findall(r"^### SHOT SC10-SH(\d{3})", texts["scene"], re.MULTILINE)]
    for number in numbers:
        if number >= first_later:
            texts = apply_edit(texts, {"file": "scene", "remove_record": f"SHOT SC10-SH{number:03d}"})
    return apply_edit(texts, {"file": "scene", "remove_record": "CUT SC10-C200"})


def check_batches():
    story = story_from(EXCERPT)
    if story is None:
        info("batches: skipped: story not present")
        return
    texts = without_later_shots(gold_texts(), 130)
    files = parse_texts(texts)
    coverage = ["COVER-02", "COVER-03", "COVER-04", "TIME-03", "TIME-05"]
    batches = {"U-08-SC10-1": {"first": "SC10-SH010", "last": "SC10-SH120", "expected": 12, "received": 12},
               "U-08-SC10-2": {"first": "SC10-SH130", "last": "SC10-SH990", "expected": 9, "received": None}}
    manifest = {"batches": {"SC10": batches}}
    result = run_checks(files, SCHEMA, WORDS, CONSTANTS, story=story, step=8, manifest=manifest, check_ids=coverage)
    found = own_lines(result)
    waiting = [why for check_id, why in result.skipped if check_id == "TIME-03" and "last batch" in why]
    report(not found and bool(waiting),
           "step 8, batch 1 of 2 written (shots 010-120): the coverage checks look only at the batch's beats, and the "
           "scene total waits for the last batch",
           "; ".join(str(problem) for problem in found[:3]) or "no line; TIME-03 skipped: runs after the last batch")
    result = run_checks(files, SCHEMA, WORDS, CONSTANTS, story=story, step=8, check_ids=coverage)
    found = own_lines(result)
    report(not found, "step 8 with no batch data, shots 010-120 written: the list items up to the highest shot "
           "written count as the batch", "; ".join(str(problem) for problem in found[:3]) or "no line")
    complete = {"U-08-SC10-1": dict(batches["U-08-SC10-1"]),
                "U-08-SC10-2": dict(batches["U-08-SC10-2"], received=9)}
    result = run_checks(files, SCHEMA, WORDS, CONSTANTS, story=story, step=8, manifest={"batches": {"SC10": complete}},
                        check_ids=coverage)
    found = own_lines(result)
    beats = sorted({problem.record for problem in found if problem.check_id == "COVER-04"})
    expected_beats = [f"SC10-B{number:02d}" for number in range(6, 12)]
    report(beats == expected_beats and "COVER-02" in check_ids_of(found) and "COVER-03" in check_ids_of(found),
           "step 8 after the scene's last batch, with shots 130-990 missing: every beat, line and speech is checked",
           f"COVER-04 on {', '.join(beats)}; {len(found)} lines from {', '.join(check_ids_of(found))}")


def check_list_items():
    story = story_from(EXCERPT)
    if story is None:
        info("list items: skipped: story not present")
        return
    texts = without_later_shots(gold_texts(), 0)
    step_seven = ["COVER-01", "COVER-02", "COVER-03", "COVER-04", "TIME-04", "TIME-05", "TIME-08"]
    result = run_checks(parse_texts(texts), SCHEMA, WORDS, CONSTANTS, story=story, step=7, check_ids=step_seven)
    found = own_lines(result)
    report(not found and not result.crashed,
           "step 7, the shot list without shots: the coverage checks read the list items and are silent",
           "; ".join(str(problem) for problem in found[:3]) or f"{len(result.checks_run)} checks run, no line")
    edited = apply_edit(dict(texts), {"file": "scene", "record": "SHOTLIST SC10-LIST",
                                      "find": "- item: SC10-SH150 | beats: SC10-B07, SC10-B08 |",
                                      "replace": "- item: SC10-SH150 | beats: SC10-B07 |"})
    result = run_checks(parse_texts(edited), SCHEMA, WORDS, CONSTANTS, story=story, step=7, check_ids=step_seven)
    found = [problem for problem in own_lines(result) if problem.check_id == "COVER-04"]
    report(len(found) == 1 and found[0].record == "SC10-B08" and "list item" in str(found[0]),
           "step 7: a beat that no list item names is reported (COVER-04 on beat 8)",
           "; ".join(str(problem) for problem in found) or "no line")
    edited = apply_edit(dict(texts), {"file": "scene", "record": "SHOTLIST SC10-LIST",
                                      "find": "| role: turn | size: close_up | frame: single | subject: CH-IONA | time: 15 |",
                                      "replace": "| role: turn | size: close_up | frame: single | subject: CH-IONA | time: 10 |"})
    result = run_checks(parse_texts(edited), SCHEMA, WORDS, CONSTANTS, story=story, step=7, check_ids=step_seven)
    found = [problem for problem in own_lines(result) if problem.check_id == "TIME-05"]
    report(len(found) == 1 and found[0].record == "SC10-B07" and LINE_FORM.match(str(found[0])) is not None,
           "step 7: the list item that ends the main turn leaves no room for its reaction (TIME-05, from the "
           "provisional floor's least value)", "; ".join(str(problem) for problem in found) or "no line")
    quick = apply_edit(dict(edited), {"file": "context", "record": "PROJECT CATCH", "find": "- depth: standard",
                                      "replace": "- depth: quick"})
    result = run_checks(parse_texts(quick), SCHEMA, WORDS, CONSTANTS, story=story, check_ids=["TIME-01"])
    found = [problem for problem in own_lines(result) if problem.check_id == "TIME-01"]
    report(len(found) == 1 and found[0].record == "SC10-LIST" and found[0].field_name == "item"
           and "SC10-SH150 time 10" in str(found[0]),
           "Quick depth (the list items are the final shots): TIME-01 reads an item's time against its provisional "
           "floor", "; ".join(str(problem) for problem in found) or "no line")


def check_lines_left_out():
    """COVER-02 is silent for lines a scene leaves out on purpose (lines_not_shown with a why), and only for those."""
    story = story_from(EXCERPT)
    if story is None:
        info("lines left out on purpose: skipped: story not present")
        return
    texts = apply_edit(gold_texts(), {"file": "scene", "record": "SHOT SC10-SH990", "find": "- lines: 486-488",
                                      "replace": "- lines: 488"})
    result = run_checks(parse_texts(texts), SCHEMA, WORDS, CONSTANTS, story=story, check_ids=["COVER-02"])
    found = own_lines(result)
    fired = len(found) == 1 and "486 is in no shot" in str(found[0])
    reason = apply_edit(dict(texts), {"file": "scene", "record": "SCENE SC10", "find": "- flags: none",
                                      "replace": "- lines_not_shown: 486 | why: the story's cut to black is the cut "
                                                 "SC10-C200, not a shot\n- flags: none"})
    result = run_checks(parse_texts(reason), SCHEMA, WORDS, CONSTANTS, story=story, check_ids=["COVER-02"])
    silent = not own_lines(result)
    report(fired and silent, "COVER-02: line 486 in no shot is reported, and is silent once lines_not_shown gives it "
           "with a why", "; ".join(str(problem) for problem in found) or "no line before the reason")


def check_stub():
    result = run_checks(parse_texts(gold_texts()), SCHEMA, WORDS, CONSTANTS, story=None, check_ids=["STATE-04"])
    reasons = [why for check_id, why in result.skipped if check_id == "STATE-04"]
    report(bool(reasons) and not result.problems, "STATE-04 (build 2) is a stub that says why it skips",
           reasons[0] if reasons else "no skip line")


# ---------------------------------------------------------------- the command, on a project made from the gold

def stage(arguments, cwd):
    environment = dict(os.environ)
    environment["STAGE_LOCK_WAIT_SECONDS"] = "2"
    completed = subprocess.run([sys.executable, str(STAGE)] + arguments, capture_output=True, text=True,
                               encoding="utf-8", cwd=str(cwd), env=environment, timeout=300)
    return completed.returncode, completed.stdout + completed.stderr


def make_gold_project(folder, texts):
    """A project folder from the gold: the scene file as 11 Scenes/Scene 10 - Saye's kitchen.md and each '## From
    NN <name>' part of the context file as the numbered file it came from."""
    (folder / "11 Scenes").mkdir(parents=True)
    (folder / "11 Scenes" / "Scene 10 - Saye's kitchen.md").write_text(texts["scene"], encoding="utf-8")
    sections = {}
    current = None
    for line in texts["context"].splitlines():
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


def check_command():
    if not EXCERPT.is_file():
        info("stage.py check on a project made from the gold: skipped: story not present")
        return
    temporary = Path(tempfile.mkdtemp(prefix="stage wp4c "))
    try:
        project = temporary / "The Catch"
        make_gold_project(project, gold_texts())
        code, output = stage(["check", "--all", "--story", str(EXCERPT)], project)
        own = [line for line in output.splitlines() if re.match(r"^[EWN] (COVER|TIME|STATE)-\d\d ", line)]
        report(not own and code in (0, 1), "stage.py check --all --story <excerpt> on a project made from the gold: no "
               "COVER, TIME or STATE line", "; ".join(own[:3]) or f"exit {code}")
        faulty = temporary / "Faulty"
        texts = apply_edit(gold_texts(), {"file": "scene", "record": "SHOT SC10-SH150", "find": "- screen_time: 15",
                                          "replace": "- screen_time: 12"})
        make_gold_project(faulty, texts)
        code, output = stage(["check", "--step", "8", "--scene", "SC10", "--story", str(EXCERPT)], faulty)
        lines = [line for line in output.splitlines() if line.startswith("E TIME-01 SC10-SH150 screen_time 12")]
        report(code == 1 and bool(lines), "stage.py check --step 8 --scene SC10 on the gold with shot 150 at 12 "
               "seconds: E TIME-01, exit 1", lines[0] if lines else f"exit {code}: {output[-300:]}")
    finally:
        shutil.rmtree(temporary, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Acceptance test of work package 4c (the COVER, TIME and STATE checks).")
    parser.add_argument("--story", help="The Catch, the whole story (optional): the gold is also checked against it")
    arguments = parser.parse_args()
    if not EXCERPT.is_file():
        info("the scene 10 excerpt is missing: skipped: story not present (the story groups)")
    check_registry()
    check_gold(arguments.story)
    check_chat_copy()
    check_faults()
    check_batches()
    check_list_items()
    check_lines_left_out()
    check_stub()
    check_command()
    failures = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failures else 'FAIL'} ({failures} failing groups)")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
