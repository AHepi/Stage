"""Acceptance test for work package 2 (records and project files).

What it checks, in plain words:
1. every grammar fixture in tests/fixtures/grammar/ parses to exactly the records, fields, items, END lines
   and merged records stored in "expected results.json", and the FORM checks print exactly the stored lines;
2. each of FORM-01 to FORM-13 fires on its own fixture (the check IDs listed by hand under must_fire);
3. every grammar rule G1 to G13 has a fixture, and so do a cut-off reply and a file with shortening markers;
4. a write-read round trip leaves every fixture unchanged, byte for byte; a canonical rewrite reads back to the
   same records and is stable; editing one field changes only that field's line;
   every stored field's example in schema.json passes the value checks (no false alarms);
5. the commands new, status, apply, pack and unpack work on a small invented story in a temporary folder
   (apply refuses a faulty inbox and changes nothing; answered choices set their fields; the lock file holds a
   second helper back; a save ZIP opens to identical files);
6. if the WP12a gold example ("references/examples/01 The Catch - scene 10.md") exists, it parses with no FORM error
   (FORM-05 and FORM-10, which depend on records in other files, are reported as information); if it does not
   exist yet the group says so.

Run from anywhere:
    python tests/wp2_acceptance.py
    python tests/wp2_acceptance.py --write-expected    (maintainers: rewrite the computed parts of
                                                        "expected results.json" after reviewing a change)
Standard library only.
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
TOOLS = SKILL / "tools"
STAGE = TOOLS / "stage.py"
FIXTURES = REPOSITORY / "tests" / "fixtures" / "grammar"
EXPECTED = FIXTURES / "expected results.json"
GOLD = SKILL / "references" / "examples" / "01 The Catch - scene 10.md"
GOLD_CONTEXT = SKILL / "references" / "examples" / "02 The Catch - scene 10 - context.md"

sys.path.insert(0, str(TOOLS))
from stage_tools.checks_form import FORM_CHECKS, FormContext, apply_tidy_fixes, run_form_checks  # noqa: E402
from stage_tools.record_format import (Record, count_levels, load_skill_data, merge_copies, parse_file,  # noqa: E402
                                       parse_text, render_file, split_item, split_list)

SCHEMA, WORDS, CONSTANTS = load_skill_data()
LIST_KINDS = ("id_list", "because_list", "reference_list", "story_point_list", "word_list", "text_list",
              "number_list")
FILE_CHECKS = ["FORM-01", "FORM-02", "FORM-03", "FORM-04", "FORM-06", "FORM-07", "FORM-08", "FORM-09",
               "FORM-12", "FORM-13"]
RESULTS = []


def report(passed, group, detail=""):
    RESULTS.append((passed, group))
    print(("PASS  " if passed else "FAIL  ") + group + (f": {detail}" if detail else ""))


def info(line):
    print("INFO  " + line)


# ---------------------------------------------------------------- summaries of parse results

def summarise_record(record):
    summary = {"type": record.type_name, "id": record.identifier, "title": record.title,
               "known": record.known_type, "line": record.heading_line_number,
               "fields": [[line.name, line.value] for line in record.fields]}
    if record.notes:
        summary["notes"] = record.notes
    loose = [line.raw for line in record.loose_lines]
    if loose:
        summary["loose"] = loose
    items = {}
    lists = {}
    if record.known_type:
        for line in record.fields:
            definition = SCHEMA.field(record.type_name, line.name)
            if definition is None or line.missing:
                continue
            if definition.get("kind") == "sub_parts" and line.value.strip().lower() not in ("none", "open"):
                item = split_item(line.value, definition)
                items.setdefault(line.name, []).append({"first": item.first, "parts": [list(part) for part in item.parts],
                                                        "unnamed": item.unnamed})
            elif definition.get("kind") in LIST_KINDS:
                lists.setdefault(line.name, []).append(split_list(line.value))
            if definition.get("kind") == "sub_parts" and line.value.strip().lower() not in ("none", "open"):
                kinds = {entry["key"]: entry["kind"] for entry in definition.get("sub_parts") or []}
                for key, value in split_item(line.value, definition).parts:
                    if kinds.get(key) in LIST_KINDS:
                        lists.setdefault(f"{line.name}.{key}", []).append(split_list(value))
    if items:
        summary["items"] = items
    if lists:
        summary["lists"] = lists
    return summary


def summarise_file(record_file):
    return {"file": record_file.name,
            "records": [summarise_record(record) for record in record_file.records],
            "end_lines": [{"what": end.what, "count": end.count, "strict": end.strict, "line": end.line_number}
                          for end in record_file.end_lines],
            "has_divider": record_file.has_divider,
            "free_text_lines": len(record_file.text_lines)}


def load_fixture(name):
    return parse_file(FIXTURES / name, name, SCHEMA)


def compute_run(run):
    """Parse a run's files, run its checks with its context, and return what the expected file stores."""
    files = [load_fixture(name) for name in run["files"]]
    others = [load_fixture(name) for name in run.get("other_files", [])]
    settings = run.get("context", {})
    current = {}
    if settings.get("current_files"):
        current_files = [load_fixture(name) for name in settings["current_files"]]
        current, _ = merge_copies(current_files, SCHEMA)
        others = others + current_files
    context = FormContext.for_records(SCHEMA, WORDS, files, other_record_files=others,
                                      step=settings.get("step"), written_by_ai=settings.get("written_by_ai", False),
                                      current_records=current, depth=settings.get("depth"),
                                      code_execution=settings.get("code_execution"))
    problems = run_form_checks(files, context, run.get("checks") or FILE_CHECKS)
    computed = {"parsed": [summarise_file(record_file) for record_file in files],
                "problems": [str(problem) for problem in problems]}
    if len(files) > 1:
        merged, _ = merge_copies(files, SCHEMA)
        computed["merged"] = [{"type": key[0], "id": key[1], "fields": [[line.name, line.value] for line in record.fields]}
                              for key, record in merged.items()]
    if run.get("tidied_file"):
        tidy_context = FormContext.for_records(SCHEMA, WORDS, files, step=settings.get("step"))
        apply_tidy_fixes(files, tidy_context)
        computed["tidied_text"] = render_file(files[0], SCHEMA)
    return computed, problems


# ---------------------------------------------------------------- group 1-3: fixtures

def check_fixtures(write_expected):
    data = json.loads(EXPECTED.read_text(encoding="utf-8"))
    mismatches = []
    missing_fires = []
    fired = {}
    for run in data["runs"]:
        computed, problems = compute_run(run)
        if write_expected:
            run["expected"] = computed
            if run.get("tidied_file"):
                (FIXTURES / run["tidied_file"]).write_text(computed.pop("tidied_text"), encoding="utf-8")
            continue
        expected = run.get("expected", {})
        if run.get("tidied_file"):
            expected = dict(expected)
            expected["tidied_text"] = (FIXTURES / run["tidied_file"]).read_text(encoding="utf-8")
        for key in ("parsed", "problems", "merged", "tidied_text"):
            if key in computed or key in expected:
                if computed.get(key) != expected.get(key):
                    mismatches.append(f"{run['name']}: {key} differs")
                    if key == "problems":
                        extra = [line for line in computed.get(key, []) if line not in expected.get(key, [])]
                        lost = [line for line in expected.get(key, []) if line not in computed.get(key, [])]
                        for line in extra[:5]:
                            print("      new:  " + line)
                        for line in lost[:5]:
                            print("      gone: " + line)
        produced = {(problem.check_id, problem.record) for problem in problems}
        produced_ids = {problem.check_id for problem in problems}
        for wanted in run.get("must_fire", []):
            check_id, record = (wanted + [None])[:2] if isinstance(wanted, list) else (wanted, None)
            ok = (check_id, record) in produced if record else check_id in produced_ids
            if not ok:
                missing_fires.append(f"{run['name']}: {check_id} {record or ''}".strip())
            fired.setdefault(check_id, []).append(run["name"])
        for level in run.get("no_levels", []):
            if any(problem.level == level for problem in problems):
                missing_fires.append(f"{run['name']}: has {level} lines but should have none")
    if write_expected:
        EXPECTED.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        info(f"rewrote the computed parts of {EXPECTED.name}; review the change before keeping it")
        return data
    report(not mismatches, "fixture parse results and problem lines equal the expected results",
           f"{len(data['runs'])} runs" if not mismatches else "; ".join(mismatches[:8]))
    not_fired = [check_id for check_id in FORM_CHECKS if check_id not in fired]
    report(not missing_fires and not not_fired, "FORM-01 to FORM-13 each fire on their fixtures",
           "all 13 fire where expected" if not (missing_fires or not_fired)
           else "; ".join(missing_fires[:8] + [f"{check_id} has no fixture" for check_id in not_fired]))
    rules = {run.get("rule") for run in data["runs"]}
    wanted_rules = {f"G{number}" for number in range(1, 14)}
    lacking = sorted(wanted_rules - rules, key=lambda rule: int(rule[1:]))
    names = {name for run in data["runs"] for name in run["files"]}
    special = [name for name in ("G09 cut off reply.md", "G11 shortening markers.md") if name not in names]
    report(not lacking and not special, "every grammar rule G1-G13 has a fixture, plus a cut-off reply and shortening markers",
           "all present" if not (lacking or special) else f"missing: {lacking + special}")
    return data


def check_schema_examples():
    """No false alarms: every field's own example in schema.json passes FORM-04 and FORM-12 (fields code works out
    and never stores are left out: they are never written)."""
    from stage_tools.record_format import FieldLine, ValueExaminer, examine_field
    examiner = ValueExaminer(SCHEMA, WORDS)
    problems = []
    total = 0
    for type_name, record_type in SCHEMA.record_types.items():
        for definition in record_type["fields"]:
            if definition.get("stored") is False:
                continue
            total += 1
            line = FieldLine(name=definition["name"], value=str(definition["example"]))
            _, issues = examine_field(examiner, type_name, line, definition)
            problems.extend(f"{type_name}.{definition['name']}: {issue.check_id} {issue.what}"
                            for _, issue in issues if issue.level == "E")
    report(not problems, "every stored field's example in schema.json passes the value checks (no false alarms)",
           f"{total} examples" if not problems else "; ".join(problems[:6]))


# ---------------------------------------------------------------- group 4: round trips

def comparable_records(record_file):
    return [(record.type_name, record.identifier, record.title,
             [(line.name, line.value) for line in record.fields]) for record in record_file.records]


def check_round_trips(extra_files=()):
    failures = []
    paths = sorted(FIXTURES.glob("*.md")) + [Path(path) for path in extra_files if Path(path).is_file()]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        with open(path, encoding="utf-8", newline="") as handle:
            exact = handle.read()
        record_file = parse_text(exact, path.name, SCHEMA)
        if render_file(record_file, SCHEMA) != exact:
            failures.append(f"{path.name}: write after read differs")
            continue
        canonical_file = parse_text(exact, path.name, SCHEMA)
        for record in canonical_file.records:
            record.is_new = True
        canonical_text = render_file(canonical_file, SCHEMA, recount=False)
        reread = parse_text(canonical_text, path.name, SCHEMA)
        before = sorted(comparable_records(record_file), key=lambda item: (item[0], item[1] or ""))
        after = sorted([(type_name, identifier, title, sorted(fields)) for type_name, identifier, title, fields
                        in comparable_records(reread)], key=lambda item: (item[0], item[1] or ""))
        before_sorted = [(type_name, identifier, title, sorted(fields)) for type_name, identifier, title, fields in before]
        if before_sorted != after:
            failures.append(f"{path.name}: the canonical rewrite reads back to different records")
        again = parse_text(canonical_text, path.name, SCHEMA)
        for record in again.records:
            record.is_new = True
        if render_file(again, SCHEMA, recount=False) != canonical_text:
            failures.append(f"{path.name}: the canonical rewrite is not stable")
        del text
    edit_failures = check_one_edit()
    report(not failures and not edit_failures, "a write-read round trip leaves files unchanged",
           f"{len(paths)} files byte for byte; canonical rewrites stable; one edit changes one line"
           if not (failures or edit_failures) else "; ".join((failures + edit_failures)[:6]))


def check_one_edit():
    """Change one field of one record and add one: only those lines change, and they read back."""
    failures = []
    path = FIXTURES / "G01 free text.md"
    original = path.read_text(encoding="utf-8")
    record_file = parse_text(original, path.name, SCHEMA)
    record = record_file.find("BEAT", "SC03-B02")
    record.set_field("beat_intensity", "5", SCHEMA)
    record.set_field("change", "the lamp is lit and she stops winding", SCHEMA)
    new_text = render_file(record_file, SCHEMA)
    old_lines = original.splitlines()
    new_lines = new_text.splitlines()
    removed = [line for line in old_lines if line not in new_lines]
    added = [line for line in new_lines if line not in old_lines]
    if removed != ["- beat_intensity: 4"] or sorted(added) != sorted(["- beat_intensity: 5",
                                                                      "- change: the lamp is lit and she stops winding"]):
        failures.append(f"editing changed other lines (removed {removed}, added {added})")
    reread = parse_text(new_text, path.name, SCHEMA).find("BEAT", "SC03-B02")
    if reread.get("beat_intensity") != "5" or reread.get("change") != "the lamp is lit and she stops winding":
        failures.append("the edited values do not read back")
    return failures


# ---------------------------------------------------------------- group 5: the commands

TINY_STORY = """= THE LANTERN
= An invented test story

> FADE IN:

## INT. SHED - NIGHT

A lamp hangs from a hook. MARA winds the key three turns.

@MARA
It never stays lit.

The wick takes the flame at last. It holds.

> CUT TO:
"""

GOOD_INBOX = """# Scene 1

Below this line: details for the AI and the checker. You never need to read them.

### SCENE SC01
- event: Mara made the lamp hold for the first time.
- location: LOC-SHED
- turn_picture: SC01-B01 | picture: Mara close, the lamp steady in her hands
- scene_idea: the lamp holds only when she stops watching it

### BEAT SC01-B01 The lamp holds
- lines: 8-13
- turn: main_turn
- turn_kind: action

### SHOTLIST SC01-LIST
- item: SC01-SH010 | beats: SC01-B01 | role: turn | size: close_up | frame: single | subject: CH-MARA | time: 6 | shows: Mara winds the key; the flame holds

END OF FILE | Scene 1 | 3 records
"""

LOCATION_INBOX = """### LOCATION LOC-SHED The shed
- story_job: the only warm room left
- loudness: quiet

END OF FILE | Places | 1 records
"""

BAD_INBOX = """### SHOT SC01-SH010 The flame holds
- beats: SC01-B01
- size: closeup shot
- status: approved
- because: SC01-B01, etc.

END OF FILE | Scene 1 shots 010-010 | 2 records
"""

ANSWER_INBOX = """### CHOICE CHOICE-001 Rights
- answer: a

END OF FILE | Start | 1 records
"""

CUT_OFF_INBOX = """### SHOT SC01-SH010 The flame holds
- beats: SC01-B01
- purpose: Mara sees the flame hold and"""


def stage(arguments, working_folder, environment=None):
    completed = subprocess.run([sys.executable, str(STAGE)] + arguments, cwd=working_folder,
                               capture_output=True, text=True, encoding="utf-8",
                               env=dict(os.environ, **(environment or {})))
    return completed.returncode, completed.stdout + completed.stderr


def file_fingerprints(folder, leave_out=()):
    prints = {}
    for path in sorted(Path(folder).rglob("*")):
        if path.is_file():
            relative = path.relative_to(folder).as_posix()
            if any(part in relative for part in leave_out):
                continue
            prints[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return prints


def check_commands():
    failures = []
    temporary = Path(tempfile.mkdtemp(prefix="stage wp2 "))
    try:
        root = temporary / "Stage"
        (root / "My stories").mkdir(parents=True)
        (root / "My breakdowns").mkdir()
        (root / "CLAUDE.md").write_text("A test copy of the kit.\n", encoding="utf-8")
        story = root / "My stories" / "the lantern.txt"
        story.write_text(TINY_STORY, encoding="utf-8")

        code, output = stage(["new", "My stories/the lantern.txt"], root)
        project = root / "My breakdowns" / "The Lantern"
        if code != 0 or not (project / "00 Start here.md").is_file() or not (project / "01 Choices.md").is_file():
            failures.append(f"new: exit {code}: {output.strip()[:200]}")
            return failures
        fingerprint = hashlib.sha256(story.read_bytes()).hexdigest()
        if fingerprint not in (project / "Original" / "fingerprint.txt").read_text(encoding="utf-8"):
            failures.append("new: the story's fingerprint is not in Original/fingerprint.txt")
        if (project / "Original" / "the lantern.txt").read_bytes() != story.read_bytes():
            failures.append("new: Original/ does not hold the story exactly")

        project_files = [parse_file(path, path.relative_to(project).as_posix(), SCHEMA)
                         for path in sorted(project.glob("*.md"))]
        context = FormContext.for_records(SCHEMA, WORDS, project_files, step=0)
        problems = run_form_checks(project_files, context)
        if problems:
            failures.append("new: the new project has FORM problems at step 0: " + "; ".join(problems[:3]))
        for path in project.glob("*.md"):
            with open(path, encoding="utf-8", newline="") as handle:
                text = handle.read()
            if render_file(parse_text(text, path.name, SCHEMA), SCHEMA) != text:
                failures.append(f"new: {path.name} does not survive a round trip")

        code, output = stage(["status"], root)
        if code != 0 or "Waiting for the user: 1 open choice" not in output:
            failures.append(f"status: exit {code}: {output.strip()[:200]}")

        inbox = project / "For machines - do not edit" / "inbox"
        (inbox / "U-04-PLACES.md").write_text(LOCATION_INBOX, encoding="utf-8")
        code, output = stage(["apply", "U-04-PLACES"], project)
        if code != 0:
            failures.append(f"apply (a place): exit {code}: {output.strip()[:200]}")
        (inbox / "U-07-SC01.md").write_text(GOOD_INBOX, encoding="utf-8")
        code, output = stage(["apply", "U-07-SC01.md"], project)
        scene_file = project / "11 Scenes" / "Scene 01 - The shed.md"
        if code != 0 or not scene_file.is_file() or not (project / "04 Scene list.md").is_file():
            failures.append(f"apply (a scene): exit {code}; scene file made: {scene_file.is_file()}: {output.strip()[:300]}")
        else:
            scene = parse_file(scene_file, scene_file.name, SCHEMA)
            if [record.key for record in scene.records] != [("SCENE", "SC01"), ("BEAT", "SC01-B01"), ("SHOTLIST", "SC01-LIST")]:
                failures.append(f"apply: the scene file holds {[record.key for record in scene.records]}")
            if scene.end_line is None or scene.end_line.count != 3:
                failures.append("apply: the scene file's END line does not count 3 records")
            listing = parse_file(project / "04 Scene list.md", "04 Scene list.md", SCHEMA).find("SCENE", "SC01")
            if listing is None or listing.get("event") is None or listing.get("status") != "draft" or listing.get("scene_idea"):
                failures.append("apply: the scene's list and design fields were not split between 04 and its scene file")
            if inbox.joinpath("U-07-SC01.md").exists() or not list((project / "For machines - do not edit" / "history").rglob("U-07-SC01.md")):
                failures.append("apply: the applied inbox file was not moved into history")
            manifest = json.loads((project / "For machines - do not edit" / "manifest.json").read_text(encoding="utf-8"))
            if "U-07-SC01" not in [unit["unit"] for unit in manifest.get("units_done", [])]:
                failures.append("apply: the manifest does not list the unit as done")
            start_here = (project / "00 Start here.md").read_text(encoding="utf-8")
            if "003 " not in start_here or "scene 1" not in start_here:
                failures.append("apply: no numbered log entry in 00 Start here")
        (inbox / "U-07-SC01.md").write_text(GOOD_INBOX, encoding="utf-8")
        before = file_fingerprints(project, ("For machines",))
        code, output = stage(["apply", "U-07-SC01.md"], project)
        if code != 0 or "0 new and 0 changed" not in output:
            failures.append(f"apply again: expected no change, got exit {code}: {output.strip()[:200]}")
        if file_fingerprints(project, ("For machines", "00 Start here")) != {key: value for key, value in before.items() if "00 Start here" not in key}:
            failures.append("apply again: files changed although the records were the same")

        (inbox / "U-08-SC01-B1.md").write_text(BAD_INBOX, encoding="utf-8")
        before = file_fingerprints(project, ("For machines",))
        code, output = stage(["apply", "U-08-SC01-B1.md"], project)
        if code != 1 or "FORM-07" not in output or "FORM-08" not in output or "FORM-10" not in output or "FORM-04" not in output:
            failures.append(f"apply (faulty inbox): expected exit 1 with FORM-04, 07, 08, 10; got {code}: {output.strip()[:300]}")
        if file_fingerprints(project, ("For machines",)) != before or not (inbox / "U-08-SC01-B1.md").is_file():
            failures.append("apply (faulty inbox): files changed although it was refused")

        (inbox / "U-08-SC01-B2.md").write_text(CUT_OFF_INBOX, encoding="utf-8")
        code, output = stage(["apply", "U-08-SC01-B2.md"], project)
        if code != 1 or "FORM-06" not in output:
            failures.append(f"apply (cut-off inbox): expected exit 1 with FORM-06; got {code}: {output.strip()[:200]}")
        (inbox / "U-08-SC01-B2.md").unlink()

        (inbox / "U-00-START.md").write_text(ANSWER_INBOX, encoding="utf-8")
        code, output = stage(["apply", "U-00-START.md"], project)
        start = parse_file(project / "00 Start here.md", "00 Start here.md", SCHEMA)
        choices = parse_file(project / "01 Choices.md", "01 Choices.md", SCHEMA)
        rights = start.records[0].get("rights")
        choice = choices.find("CHOICE", "CHOICE-001")
        if code != 0 or rights != "mine" or choice.get("status") != "answered" or choice.get("date") in (None, "none"):
            failures.append(f"apply (an answer): exit {code}, rights {rights}, choice status {choice.get('status')}")
        project_files = [parse_file(path, path.relative_to(project).as_posix(), SCHEMA)
                         for path in sorted(list(project.glob("*.md")) + list((project / "11 Scenes").glob("*.md")))]
        context = FormContext.for_records(SCHEMA, WORDS, project_files, step=0)
        grammar = [problem for problem in run_form_checks(project_files, context, FILE_CHECKS + ["FORM-10"])
                   if problem.level != "N"]
        if grammar:
            failures.append("after apply: the project has FORM problems: " + "; ".join(grammar[:3]))
        for record_file in project_files:
            path = project / record_file.name
            with open(path, encoding="utf-8", newline="") as handle:
                text = handle.read()
            if render_file(parse_text(text, record_file.name, SCHEMA), SCHEMA) != text:
                failures.append(f"after apply: {record_file.name} does not survive a round trip")

        lock = project / "For machines - do not edit" / "apply.lock"
        lock.write_text("another helper\n", encoding="utf-8")
        code, output = stage(["apply", "U-08-SC01-B1.md"], project, {"STAGE_LOCK_WAIT_SECONDS": "1"})
        if code != 2 or "Another helper" not in output:
            failures.append(f"lock: a second helper was not held back (exit {code}: {output.strip()[:120]})")
        lock.unlink()

        code, output = stage(["pack"], root)
        zips = sorted((root / "My breakdowns").glob("* Save - The Lantern - after *.zip"))
        if code != 0 or len(zips) != 1:
            failures.append(f"pack: exit {code}, ZIPs {[path.name for path in zips]}: {output.strip()[:200]}")
        else:
            if not zips[0].name[:3].isdigit():
                failures.append(f"pack: the ZIP name does not start with the log entry number ({zips[0].name})")
            elsewhere = temporary / "Elsewhere"
            code, output = stage(["unpack", str(zips[0]), "--into", str(elsewhere)], temporary)
            opened = elsewhere / "The Lantern"
            left_out = ("For machines - do not edit/history", "For machines - do not edit/handouts",
                        "For machines - do not edit/log.jsonl")
            if code != 0 or file_fingerprints(project, left_out) != file_fingerprints(opened, left_out):
                failures.append(f"unpack: exit {code}; the opened files differ from the project: {output.strip()[:200]}")
            if not (opened / "For machines - do not edit" / "inbox").is_dir():
                failures.append("unpack: the inbox folder is missing")
            code, output = stage(["unpack", str(zips[0]), "--into", str(elsewhere)], temporary)
            if code != 2:
                failures.append(f"unpack over an existing folder: expected exit 2, got {code}")
            unsafe = temporary / "unsafe.zip"
            with zipfile.ZipFile(unsafe, "w") as archive:
                archive.writestr("The Lantern/00 Start here.md", "x")
                archive.writestr("The Lantern/../../escape.txt", "x")
            code, output = stage(["unpack", str(unsafe), "--into", str(temporary / "Unsafe")], temporary)
            if code != 2 or (temporary / "escape.txt").exists():
                failures.append(f"unpack of an unsafe ZIP: expected exit 2, got {code}")

        code, output = stage(["status", "--project", str(temporary / "Elsewhere")], temporary)
        if code != 2:
            failures.append(f"--project on a folder that is not a project: expected exit 2, got {code}")
        code, output = stage(["frobnicate"], root)
        if code != 2:
            failures.append(f"an unknown command: expected exit 2, got {code}")
        log_lines = (project / "For machines - do not edit" / "log.jsonl").read_text(encoding="utf-8").splitlines()
        commands = [json.loads(line)["command"] for line in log_lines]
        for wanted in ("new", "status", "apply", "pack"):
            if wanted not in commands:
                failures.append(f"log.jsonl has no line for {wanted}")
        if any(str(temporary) in line for line in log_lines):
            failures.append("log.jsonl holds full paths (it should hold file names only)")
    finally:
        shutil.rmtree(temporary, ignore_errors=True)
    return failures


# ---------------------------------------------------------------- group 6: the WP12a gold example

def check_gold():
    if not GOLD.is_file():
        info(f'skipped: "{GOLD.relative_to(REPOSITORY)}" does not exist yet (WP12a writes it)')
        return
    files = [parse_file(GOLD, GOLD.name, SCHEMA)]
    if GOLD_CONTEXT.is_file():
        files.append(parse_file(GOLD_CONTEXT, GOLD_CONTEXT.name, SCHEMA))
    context = FormContext.for_records(SCHEMA, WORDS, files, step=None)
    grammar = [problem for problem in run_form_checks(files, context, FILE_CHECKS) if problem.level == "E"]
    counts = {record_file.name: len(record_file.records) for record_file in files}
    report(not grammar, "the WP12a gold example parses with no FORM error",
           f"{counts}; FORM-01 to 04, 06 to 09, 12: no error" if not grammar
           else f"{len(grammar)} errors, first: " + "; ".join(grammar[:5]))
    for check_ids, step in ((["FORM-05"], 8), (["FORM-10"], None)):
        context = FormContext.for_records(SCHEMA, WORDS, files, step=step)
        found = [problem for problem in run_form_checks(files, context, check_ids) if problem.level == "E"]
        info(f"gold, {check_ids[0]} (depends on records in other files; not a failure): {len(found)} error lines"
             + (": " + "; ".join(found[:4]) if found else ""))
    with open(GOLD, encoding="utf-8", newline="") as handle:
        text = handle.read()
    report(render_file(parse_text(text, GOLD.name, SCHEMA), SCHEMA) == text, "the gold example survives a write-read round trip")


def main():
    parser = argparse.ArgumentParser(description="Work package 2 acceptance test.")
    parser.add_argument("--write-expected", action="store_true",
                        help="rewrite the computed parts of the expected results (review the change first)")
    arguments = parser.parse_args()
    check_fixtures(arguments.write_expected)
    if arguments.write_expected:
        return 0
    check_schema_examples()
    check_round_trips([GOLD, GOLD_CONTEXT])
    failures = check_commands()
    report(not failures, "the commands new, status, apply, pack and unpack",
           "new, status, apply (good, again, faulty, cut off, an answer), lock, pack, unpack, logs"
           if not failures else "; ".join(failures[:8]))
    check_gold()
    failed = [group for passed, group in RESULTS if not passed]
    print(f"RESULT: {'PASS' if not failed else 'FAIL'} ({len(failed)} failing groups)")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
