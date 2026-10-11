"""The acceptance test of work package 4f: the commands adopt, impact and questions
(.claude/skills/breaking-down-stories/tools/stage_tools/adopt_folder.py; blueprint 7.1, 5.2, 5.4 rule 5, 11.2).

What it proves (blueprint 14.2 row WP4, and the WP4f brief):
- adopt turns the chat-saved scene 10 fixture (tests/fixtures/chat saved scene 10, from WP12a) plus the story into a
  project on which check --all exits 0: the story kept in Original with its fingerprint and numbered, the two batch
  files merged into the scene file by ID, every quote anchor whose scope the story given holds turned into the
  gold's line numbers, every story point given the gold's beat, code_execution set to yes;
- each field adopt takes over (chat_writer: ai) is logged as a note (N), never a warning or an error, and every
  value that changed has its own note;
- adopt again on the adopted folder changes no record; saved parts of whole-film files merge by ID (a colliding
  finding number is renumbered); a part that looks cut off is not merged (exit 1); a ZIP of the folder works; a
  missing story, a folder that is not a breakdown and a story whose fingerprint differs stop with exit 2 and change
  nothing;
- impact SC10-B07 lists the shots that cite it, and what goes stale downstream only; impact changes nothing;
- questions --sample --seed 1 produces yes/no questions for every turn shot of the gold (and every turn beat and
  must-keep shot), each citing its lines, in batches of question_batch_size; the same seed gives the same questions.

Usage: python tests/wp4f_acceptance.py [--story "<The Catch, the whole story>"]
Without the scene 10 excerpt (or the chat-saved fixture) the groups that need them say "skipped: story not present"
(or "skipped: fixture not present"). With --story the whole story is used as well, and every anchor of every file
must resolve to the gold's numbers. Standard library only.
"""

import argparse
import hashlib
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parent.parent
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
TOOLS = SKILL / "tools"
STAGE = TOOLS / "stage.py"
sys.path.insert(0, str(TOOLS))

from stage_tools.record_format import (DIVIDER_LINE, load_skill_data, merge_copies, parse_file,  # noqa: E402
                                       parse_line_numbers, parse_quote_anchor, split_item, split_list)

SCHEMA, WORDS, CONSTANTS = load_skill_data()
FIXTURES = REPOSITORY / "tests" / "fixtures"
EXCERPT = FIXTURES / "The Catch - lines 397-489.txt"
CHAT_FOLDER = FIXTURES / "chat saved scene 10"
GOLD_SCENE = SKILL / "references" / "examples" / "01 The Catch - scene 10.md"
GOLD_CONTEXT = SKILL / "references" / "examples" / "02 The Catch - scene 10 - context.md"
MODULE = TOOLS / "stage_tools" / "adopt_folder.py"
MACHINE = "For machines - do not edit"
SCENE_FILE = "11 Scenes/Scene 10 - Saye's kitchen.md"
BATCH_FILES = ["11 Scenes/Scene 10 - Saye's kitchen - shots 010-120.md",
               "11 Scenes/Scene 10 - Saye's kitchen - shots 130-990.md"]
# PROJECT fields the gold holds as the code project it is, which a chat folder adopted elsewhere holds differently
# (the story file's name and fingerprint when a different story file is given, the app, the batch size the app
# self-test sets, the date the checker last ran).
PROJECT_FIELDS_OF_THE_APP = {"source_file", "source_fingerprint", "surface", "batch_size", "checker_last_run"}
NOTE_LINE = re.compile(r"^N (?P<check>[A-Z]+-\d{2}) (?P<record>\S+) (?P<field>[a-z_]+) (?P<what>.+)$")

RESULTS = []


def report(passed, group, detail=""):
    RESULTS.append(bool(passed))
    print(f"{'PASS' if passed else 'FAIL'}  {group}" + (f": {detail}" if detail else ""), flush=True)


def info(line):
    print(f"INFO  {line}", flush=True)


def group(title):
    """Run a test group: an AssertionError fails it with its message, any other error fails it with its type."""
    def decorator(function):
        def run(*arguments):
            try:
                detail = function(*arguments)
            except AssertionError as error:
                report(False, title, str(error)[:1500])
                return
            except Exception as error:  # a fault in the code under test fails the group, never the whole run
                report(False, title, f"{type(error).__name__}: {error}")
                return
            if detail == "skip":
                return
            report(True, title, detail or "")
        return run
    return decorator


def stage(arguments, cwd):
    environment = dict(os.environ)
    environment["STAGE_LOCK_WAIT_SECONDS"] = "2"
    completed = subprocess.run([sys.executable, str(STAGE)] + [str(argument) for argument in arguments],
                               capture_output=True, text=True, encoding="utf-8", cwd=str(cwd), env=environment,
                               timeout=600)
    return completed.returncode, completed.stdout + completed.stderr


def shorten(items, count=4):
    items = list(items)
    return "; ".join(str(item) for item in items[:count]) + (f"; and {len(items) - count} more" if len(items) > count else "")


# ---------------------------------------------------------------- reading records

def record_files_of(folder, leave_out=("03 ", "13 ")):
    folder = Path(folder)
    files = []
    for path in sorted(folder.rglob("*.md")):
        relative = path.relative_to(folder).as_posix()
        if relative.startswith((MACHINE, "Original")) or path.name.startswith(leave_out):
            continue
        files.append(parse_file(path, relative, SCHEMA))
    return files


def merged_index(files):
    index, conflicts = merge_copies(files, SCHEMA)
    return index, conflicts


def gold_index():
    files = [parse_file(GOLD_SCENE, GOLD_SCENE.name, SCHEMA), parse_file(GOLD_CONTEXT, GOLD_CONTEXT.name, SCHEMA)]
    return merged_index(files)[0]


def values_of(record, name):
    return [line.value.strip() for line in record.field_lines(name) if not line.missing]


def definition_of(record, name):
    if record.type_name == "SETVALUE":
        target = (record.get("target") or "").strip()
        types = [target] if SCHEMA.knows_type(target) else [kind for kind in SCHEMA.types_for_id(target)
                                                                if SCHEMA.knows_type(kind)]
        return SCHEMA.field(types[0], name) if types else None
    return SCHEMA.field(record.type_name, name)


def holds_line_reference(record, name, value):
    """True when a value carries a line reference: a lines-kind field, a line: piece of a because, or a lines-kind
    first part or sub-part."""
    definition = definition_of(record, name) or {}
    kind = definition.get("kind")
    if kind == "lines":
        return True
    if kind == "because_list":
        return any(piece.lower().startswith("line:") for piece in split_list(value))
    if kind == "sub_parts":
        first = definition.get("first_part") or {}
        if first.get("kind") == "lines":
            return True
        return any(sub.get("kind") == "lines" and f"{sub.get('key')}:" in value for sub in definition.get("sub_parts") or [])
    return False


def reowned_fields(files):
    """{(record label, field)} the schema says adopt takes over: fields with chat_writer ai whose writer (or one of
    whose conditional writers) is code_state or story, as the chat wrote them (SETVALUE records hold a target's
    fields and are not the record itself)."""
    found = set()
    for record_file in files:
        for record in record_file.records:
            if record.type_name == "SETVALUE" or not record.known_type:
                continue
            for name in record.field_names():
                definition = SCHEMA.field(record.type_name, name) or {}
                if definition.get("chat_writer") != "ai":
                    continue
                writers = [definition.get("writer")] + [entry["writer"] for entry in definition.get("writer_when", [])]
                if any(writer in ("code_state", "story") for writer in writers):
                    found.add((record.label, name))
    return found


def adopt_notes(folder):
    """The notes adopt logged in log.jsonl (its own line with "notes")."""
    notes = []
    for line in (Path(folder) / MACHINE / "log.jsonl").read_text(encoding="utf-8").splitlines():
        entry = json.loads(line)
        if entry.get("command") == "adopt" and "notes" in entry:
            notes = entry["notes"]
    return notes


# ---------------------------------------------------------------- projects made for the tests

def make_gold_project(folder, story=None):
    """A project folder from the gold: the scene file in 11 Scenes and each '## From <file>' part of the context
    file as its numbered file; with a story, the story read into it as stage.py adopt reads it (numbered story,
    speeches.json, story map.json), without touching the records."""
    folder = Path(folder)
    folder.mkdir(parents=True)
    (folder / MACHINE).mkdir()
    context = GOLD_CONTEXT.read_text(encoding="utf-8").split(DIVIDER_LINE, 1)[1]
    sections = re.split(r"^## From (.+)$", context, flags=re.MULTILINE)[1:]
    for name, body in zip(sections[0::2], sections[1::2]):
        body = re.sub(r"\n+END OF FILE .*$", "", body.strip(), flags=re.DOTALL)
        count = len(re.findall(r"^### ", body, re.MULTILINE))
        (folder / f"{name.strip()}.md").write_text(
            f"# {name.strip()}\n\n{DIVIDER_LINE}\n\n{body}\n\nEND OF FILE | {name.strip()} | {count} records\n",
            encoding="utf-8")
    (folder / "11 Scenes").mkdir()
    shutil.copy(GOLD_SCENE, folder / SCENE_FILE)
    if story is not None:
        from stage_tools.project_files import Project
        from stage_tools.read_story import read_into_project
        (folder / "Original").mkdir()
        shutil.copy(story, folder / "Original" / story.name)

        class Context:
            constants = CONSTANTS
        read_into_project(Project(folder, SCHEMA, WORDS), Context(), folder / "Original" / story.name,
                          write_records=False)
    return folder


def snapshot(folder):
    """{relative path: bytes} of every file under a folder."""
    folder = Path(folder)
    return {path.relative_to(folder).as_posix(): path.read_bytes() for path in folder.rglob("*") if path.is_file()}


def cut_record(text, heading):
    """(text without the record '### <heading>...', the record's text)."""
    pattern = re.compile(r"^### " + re.escape(heading) + r"\b.*?(?=^### |^---$|^END OF FILE)", re.MULTILINE | re.DOTALL)
    match = pattern.search(text)
    assert match, f"no record {heading}"
    return text[:match.start()] + text[match.end():], match.group(0)


def recount(text):
    count = len(re.findall(r"^### ", text, re.MULTILINE))
    return re.sub(r"\| \d+ records?(\s*)$", f"| {count} records\\1", text.rstrip("\n")) + "\n"


# ---------------------------------------------------------------- the tests

def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--story", help="the whole story (The Catch); the scene 10 excerpt fixture is always used when present")
    arguments = parser.parse_args()
    whole_story = Path(arguments.story) if arguments.story else None
    if whole_story is not None and not whole_story.is_file():
        info(f"skipped: story not present ({whole_story.name}); the whole-story groups are skipped")
        whole_story = None
    excerpt = EXCERPT if EXCERPT.is_file() else None
    chat_present = (CHAT_FOLDER / "00 Start here.md").is_file()
    workspace = Path(tempfile.mkdtemp(prefix="wp4f "))
    try:
        run_groups(workspace, excerpt, whole_story, chat_present)
    finally:
        shutil.rmtree(workspace, ignore_errors=True)
    failing = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({failing} failing groups)")
    return 1 if failing else 0


def run_groups(workspace, excerpt, whole_story, chat_present):
    state = {}

    @group("the module: a plain note at its top, and stage.py lists adopt, impact and questions")
    def module_and_commands():
        text = MODULE.read_text(encoding="utf-8")
        assert text.startswith('"""adopt_folder.py: '), "the module does not start with its plain note"
        code, output = stage(["help"], workspace)
        assert code == 0, f"help exit {code}"
        for command in ("adopt", "impact", "questions"):
            assert re.search(rf"^\s+{command}\s", output, re.MULTILINE), f"{command} is not listed: {output[:500]}"
        assert "Not in this copy of the tools yet" not in output or not re.search(
            r"yet: .*\b(adopt|impact|questions)\b", output), "a WP4f command is reported missing"
        return "adopt, impact and questions registered"
    module_and_commands()

    if not chat_present or excerpt is None:
        info("skipped: fixture not present (the chat-saved scene 10 folder)" if not chat_present
             else "skipped: story not present (the scene 10 excerpt): the adopt groups need a story")
    else:
        adopt_groups(workspace, excerpt, whole_story, state)
    if excerpt is None:
        info("skipped: story not present (the scene 10 excerpt): impact and questions run on the gold without speeches")
    impact_groups(workspace, excerpt)
    question_groups(workspace, excerpt, state)


def adopt_groups(workspace, excerpt, whole_story, state):
    folder = workspace / "chat" / "The Catch - breakdown"
    shutil.copytree(CHAT_FOLDER, folder)
    before_files = record_files_of(folder)
    before_index = merged_index(before_files)[0]
    code, output = stage(["adopt", folder, excerpt, "--surface", "claude_web"], workspace)
    state["adopt_output"] = output
    state["adopted"] = folder

    @group("adopt: the chat-saved scene 10 fixture plus the story becomes a project on which check --all exits 0")
    def adopt_exit():
        assert code == 0, f"adopt exit {code}: {output[-2500:]}"
        health = (folder / "13 Health check.md").read_text(encoding="utf-8")
        assert health.startswith("In short:"), "13 Health check.md does not start with 'In short:'"
        assert "Command: check --all" in health, "the health check was not made by check --all"
        counts = re.search(r"Counts: (\d+) errors?", health)
        assert counts and counts.group(1) == "0", f"the check found errors: {counts.group(0) if counts else health[:300]}"
        errors = [line for line in output.splitlines() if line.startswith("E ")]
        assert not errors, f"error lines: {shorten(errors)}"
        story_copy = folder / "Original" / excerpt.name
        assert story_copy.is_file() and story_copy.read_bytes() == excerpt.read_bytes(), "the story is not in Original"
        fingerprint = hashlib.sha256(excerpt.read_bytes()).hexdigest()
        assert fingerprint in (folder / "Original" / "fingerprint.txt").read_text(encoding="utf-8"), "fingerprint.txt"
        for name in ("03 Story - numbered.md", f"{MACHINE}/speeches.json", f"{MACHINE}/story map.json"):
            assert (folder / name).is_file(), f"{name} was not made"
        speeches = json.loads((folder / MACHINE / "speeches.json").read_text(encoding="utf-8"))["speeches"]
        assert len(speeches) == 16, f"{len(speeches)} speeches, not 16"
        project = merged_index(record_files_of(folder))[0]
        project_record = next(record for key, record in project.items() if key[0] == "PROJECT")
        assert project_record.get("code_execution") == "yes", "code_execution is not yes"
        assert project_record.get("surface") == "claude_web", "surface is not the new app"
        assert project_record.get("source_fingerprint") == fingerprint, "source_fingerprint is not the story's"
        return (f"exit 0; 13 Health check: 0 errors; story in Original with its fingerprint; 16 speeches; "
                f"code_execution yes, surface claude_web")
    adopt_exit()

    @group("adopt: the two batch files are merged into the scene file by ID (G10), and kept in history")
    def adopt_batches():
        for name in BATCH_FILES:
            assert not (folder / name).exists(), f"{name} is still in the folder"
            kept = list((folder / MACHINE / "history").rglob(Path(name).name))
            assert kept, f"{name} is not kept in history"
        scene = parse_file(folder / SCENE_FILE, SCENE_FILE, SCHEMA)
        shots = [record.identifier for record in scene.records if record.type_name == "SHOT"]
        assert len(shots) == 21 and len(set(shots)) == 21, f"{len(shots)} shots in the scene file"
        assert scene.end_line is not None and scene.end_line.count == len(scene.records), "the END line was not recounted"
        before_keys = {key for key in before_index if key[0] in ("SHOT", "CUT")}
        after_keys = {record.key for record in scene.records if record.type_name in ("SHOT", "CUT")}
        assert before_keys == after_keys, f"shots or cuts lost or added: {sorted(before_keys ^ after_keys)[:5]}"
        return f"{len(scene.records)} records in the scene file (END line counts {scene.end_line.count}); both parts in history"
    adopt_batches()

    @group("adopt: every quote anchor whose scope the story given holds becomes the gold's line numbers")
    def adopt_anchors():
        gold = gold_index()
        after = merged_index(record_files_of(folder))[0]
        wrong = []
        checked = 0
        left = 0
        for key, record in after.items():
            gold_record = gold.get(key)
            if gold_record is None:
                continue
            for name in record.field_names():
                for value, gold_value in zip(values_of(record, name), values_of(gold_record, name)):
                    if not holds_line_reference(record, name, value):
                        continue
                    if '"' in re.sub(r'\| (?:quote|words): "[^"]*"', "", value):
                        left += 1
                        scene = key[1] if key[0] in ("SCENE", "SHOT", "BEAT", "PART", "MOVE", "SETUP", "SHOTLIST",
                                                        "CUT") else None
                        if scene and scene.startswith("SC10"):
                            wrong.append(f"{key[1]} {name} still a quote: {value[:60]}")
                        continue
                    checked += 1
                    if value != gold_value:
                        wrong.append(f"{key[1] or key[0]} {name}: {value[:60]} (gold: {gold_value[:60]})")
        assert not wrong, shorten(wrong)
        assert checked >= 40, f"only {checked} line references compared"
        return (f"{checked} line references equal the gold's; {left} whole-film anchors outside the excerpt stay "
                "quotes (not in the excerpt)")
    adopt_anchors()

    @group("adopt: every story point stores the beat the gold stores for it (5.4 rule 12)")
    def adopt_story_points():
        gold = gold_index()
        after = merged_index(record_files_of(folder))[0]
        wrong = []
        checked = 0
        for key, gold_record in gold.items():
            record = after.get(key)
            if record is None:
                continue
            for name in gold_record.field_names():
                for value, gold_value in zip(values_of(record, name), values_of(gold_record, name)):
                    gold_beats = re.findall(r"=\s*(SC10-B\d{2})", gold_value)
                    if not gold_beats:
                        continue
                    checked += len(gold_beats)
                    if re.findall(r"=\s*(SC10-B\d{2})", value) != gold_beats:
                        wrong.append(f"{key[1] or key[0]} {name}: {value[:70]}")
        assert checked >= 15 and not wrong, f"{checked} checked; {shorten(wrong)}"
        return f"{checked} story points end with the gold's beat"
    adopt_story_points()

    @group("adopt: each field it takes over (chat_writer ai) is logged as a note (N), and each change has its own note")
    def adopt_notes_group():
        expected = reowned_fields(before_files)
        notes = adopt_notes(folder)
        assert notes, "no notes in log.jsonl"
        levels = {note[:1] for note in notes}
        assert levels == {"N"}, f"adopt logged lines that are not notes: {sorted(levels)}"
        logged = set()
        for note in notes:
            match = NOTE_LINE.match(note)
            assert match, f"a note is not in 7.2's form: {note[:120]}"
            logged.add((match.group("record"), match.group("field")))
        missing = sorted(expected - logged)
        assert not missing, f"re-owned fields not logged: {shorten(missing)}"
        after = merged_index(record_files_of(folder))[0]
        changed = []
        for key, record in before_index.items():
            if key[0] == "SETVALUE":
                continue
            for name in record.field_names():
                if (record.label, name) not in expected:
                    continue
                new = after.get(key)
                if new is not None and values_of(record, name) != values_of(new, name):
                    changed.append((record.label, name))
        for label, name in changed:
            assert any(note.startswith(f"N FORM-10 {label} {name} was ") and "code wrote" in note for note in notes), \
                f"no note says how {label} {name} changed"
        printed = [line for line in state["adopt_output"].split("Checking everything")[0].splitlines()
                   if re.match(r"^[EW] ", line)]
        assert not printed, f"adopt printed warnings or errors of its own: {shorten(printed)}"
        wanted_changes = {("CATCH", "source_fingerprint"), ("CATCH", "code_execution"), ("CATCH", "surface"),
                          ("SC10", "lines")}
        assert wanted_changes <= set(changed), f"expected changes missing: {sorted(wanted_changes - set(changed))}"
        scene_lines = next(note for note in notes if note.startswith("N FORM-10 SC10 lines was "))
        assert "397-489" in scene_lines, f"scene 10's lines note: {scene_lines[:160]}"
        return (f"{len(expected)} re-owned fields, all logged as N (of {len(notes)} notes); {len(changed)} changed, "
                f"each with its note: {', '.join(f'{label} {name}' for label, name in changed)}")
    adopt_notes_group()

    @group("adopt: 13 Health check says in plain words what the tools took over from the chat app")
    def adopt_report():
        health = (folder / "13 Health check.md").read_text(encoding="utf-8")
        plain = health.split(DIVIDER_LINE, 1)[0]
        assert "## Taken over from the chat app" in plain, "no section on what was taken over"
        section = plain.split("## Taken over from the chat app", 1)[1].split("\n## ", 1)[0]
        codes = re.findall(r"\b(?:SC\d{2}|CH-[A-Z]+|FORM-\d{2}|[A-Z]{2,}-\d{2,3})\b", section)
        assert not codes, f"codes or IDs in the plain section: {codes[:5]}"
        abbreviations = [word for word in (WORDS.get("abbreviations") or {}) if isinstance(word, str) and
                         re.search(rf"\b{re.escape(word)}\b", section)] if isinstance(WORDS.get("abbreviations"), dict) else []
        assert not abbreviations, f"abbreviations: {abbreviations[:5]}"
        return section.strip().splitlines()[0][:120]
    adopt_report()

    @group("adopt again on the adopted folder: no record changes, still exit 0")
    def adopt_again():
        before = {name: data for name, data in snapshot(folder).items()
                  if not name.startswith((MACHINE, "00 Start here", "13 Health check", "03 Story"))}
        code_again, output_again = stage(["adopt", folder, excerpt, "--surface", "claude_web"], workspace)
        assert code_again == 0, f"exit {code_again}: {output_again[-1500:]}"
        after = {name: data for name, data in snapshot(folder).items()
                 if not name.startswith((MACHINE, "00 Start here", "13 Health check", "03 Story"))}
        changed = sorted(name for name in set(before) | set(after) if before.get(name) != after.get(name))
        assert not changed, f"files changed: {changed}"
        project_file = parse_file(folder / "00 Start here.md", "00 Start here.md", SCHEMA)
        project_before = parse_file(Path(CHAT_FOLDER) / "00 Start here.md", "00", SCHEMA)
        assert project_file.records and project_before.records
        assert "0 changed" in output_again and "Turned 0 quote anchors" in output_again, output_again[:800]
        return "no record file changed; 0 anchors, 0 changed fields"
    adopt_again()

    if whole_story is not None:
        @group("adopt with the whole story: every anchor of every file becomes the gold's line numbers")
        def adopt_whole():
            whole = workspace / "whole" / "The Catch - breakdown"
            shutil.copytree(CHAT_FOLDER, whole)
            code_whole, output_whole = stage(["adopt", whole, whole_story, "--surface", "claude_code"], workspace)
            assert code_whole == 0, f"exit {code_whole}: {output_whole[-1500:]}"
            gold = gold_index()
            after = merged_index(record_files_of(whole))[0]
            differences = []
            for key, gold_record in gold.items():
                record = after.get(key)
                if record is None:
                    differences.append(f"{key} missing")
                    continue
                for name in gold_record.field_names():
                    if key[0] == "PROJECT" and name in PROJECT_FIELDS_OF_THE_APP:
                        continue
                    ours = [re.sub(r' \| words: "[^"]*"', "", value) for value in values_of(record, name)]
                    if ours != values_of(gold_record, name):
                        differences.append(f"{key[1] or key[0]} {name}: {ours[:1]} (gold {values_of(gold_record, name)[:1]})")
            assert not differences, shorten(differences)
            fingerprint = after[("PROJECT", "CATCH")].get("source_fingerprint")
            assert fingerprint == gold[("PROJECT", "CATCH")].get("source_fingerprint"), "the fingerprint is not the gold's"
            return "the adopted folder equals the gold field for field (apart from the app's own PROJECT fields and hear words)"
        adopt_whole()
    else:
        info("skipped: story not present (the whole story): adopt with --story compares every file with the gold")

    @group("adopt: saved parts of whole-film files and group health checks merge by ID; a colliding finding number "
           "is renumbered")
    def adopt_parts():
        folder_parts = workspace / "parts" / "The Catch - breakdown"
        shutil.copytree(CHAT_FOLDER, folder_parts)
        characters = folder_parts / "07 Characters and voices.md"
        text = characters.read_text(encoding="utf-8")
        text, eli = cut_record(text, "CHARACTER CH-ELI")
        text, eli_voice = cut_record(text, "VOICE VO-ELI")
        characters.write_text(recount(text), encoding="utf-8")
        (folder_parts / "07 Characters and voices - Eli.md").write_text(
            f"# Characters and voices: Eli\n\n{DIVIDER_LINE}\n\n{eli.rstrip()}\n\n{eli_voice.rstrip()}\n\n"
            "END OF FILE | Characters and voices - Eli | 2 records\n", encoding="utf-8")
        finding = ("### FINDING FIND-001 {title}\n- record: SC10-SH{shot}\n- rule: CRAFT-19\n- evidence: {evidence}\n"
                   "- fix: keep the light as it is\n- source: review\n- status: fixed\n- reason: fixed in the chat\n"
                   "- locked: no\n")
        for number, shot, evidence in ((3, "150", "size and sound change on the turn"),
                                       (4, "190", "the wait is cut too soon")):
            (folder_parts / f"13 Health check - group {number}.md").write_text(
                f"# Health check, group {number}\n\n{DIVIDER_LINE}\n\n"
                + finding.format(title=f"Group {number}", shot=shot, evidence=evidence)
                + f"\nEND OF FILE | Health check - group {number} | 1 records\n", encoding="utf-8")
        code_parts, output_parts = stage(["adopt", folder_parts, excerpt], workspace)
        leftovers = [path.name for path in folder_parts.glob("* - *.md")
                     if path.name.startswith(("07 ", "13 ")) and " - " in path.name[3:]]
        assert not leftovers, f"parts left in the folder: {leftovers}"
        merged = parse_file(characters, "07", SCHEMA)
        assert merged.find("CHARACTER", "CH-ELI") is not None and merged.find("VOICE", "VO-ELI") is not None, \
            "Eli's records were not merged into 07 Characters and voices"
        original = {record.key: [(line.name, line.value) for line in record.fields]
                    for record in parse_file(CHAT_FOLDER / "07 Characters and voices.md", "07", SCHEMA).records}
        now = {record.key: [(line.name, line.value) for line in record.fields] for record in merged.records}
        assert set(original) == set(now), f"records differ: {sorted(set(original) ^ set(now))}"
        health = parse_file(folder_parts / "13 Health check.md", "13", SCHEMA)
        findings = sorted(record.identifier for record in health.records if record.type_name == "FINDING")
        assert findings == ["FIND-001", "FIND-002"], f"findings after the merge: {findings}"
        assert re.search(r"N ID-01 FIND-001 is used by two different findings", output_parts), \
            "no note about the renumbered finding"
        assert code_parts in (0, 1), f"exit {code_parts}"
        form = [line for line in output_parts.splitlines() if re.match(r"^E (FORM-0[1-9]|FORM-1[0-2]|ID-01)", line)]
        assert not form, f"form or ID errors after the merge: {shorten(form)}"
        return f"07's part and two group health checks merged; FIND-001 and FIND-002; check exit {code_parts}"
    adopt_parts()

    @group("adopt: a saved part that looks cut off (no END line) is not merged, with an error line and exit 1")
    def adopt_cut_off():
        folder_cut = workspace / "cut" / "The Catch - breakdown"
        shutil.copytree(CHAT_FOLDER, folder_cut)
        batch = folder_cut / BATCH_FILES[1]
        text = batch.read_text(encoding="utf-8")
        batch.write_text(re.sub(r"\nEND OF FILE .*\n?$", "\n", text), encoding="utf-8")
        code_cut, output_cut = stage(["adopt", folder_cut, excerpt], workspace)
        assert code_cut == 1, f"exit {code_cut}"
        assert re.search(r'^E FORM-06 "11 Scenes/Scene 10 - Saye\'s kitchen - shots 130-990.md" was not merged',
                         output_cut, re.MULTILINE), output_cut[:1500]
        assert batch.is_file(), "the cut-off part was taken out of the folder"
        assert not (folder_cut / BATCH_FILES[0]).exists(), "the whole part was not merged"
        return "E FORM-06 on the part, left in place, exit 1"
    adopt_cut_off()

    @group("adopt: a ZIP of the folder (as the user makes it) is unpacked next to it and adopted")
    def adopt_zip():
        zip_folder = workspace / "zip"
        zip_folder.mkdir()
        archive = zip_folder / "The Catch - breakdown.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            for path in sorted(CHAT_FOLDER.rglob("*")):
                if path.is_file():
                    handle.write(path, f"The Catch - breakdown/{path.relative_to(CHAT_FOLDER).as_posix()}")
            handle.writestr("__MACOSX/._00 Start here.md", b"left out")
        code_zip, output_zip = stage(["adopt", archive, excerpt], workspace)
        assert code_zip == 0, f"exit {code_zip}: {output_zip[-1200:]}"
        unpacked = zip_folder / "The Catch - breakdown" / "The Catch - breakdown"
        assert (unpacked / "13 Health check.md").is_file(), f"not adopted where expected: {output_zip[:300]}"
        assert not list(zip_folder.rglob("__MACOSX")), "the __MACOSX folder was unpacked"
        bad = zip_folder / "bad.zip"
        with zipfile.ZipFile(bad, "w") as handle:
            handle.writestr("../outside.md", "no")
        code_bad, output_bad = stage(["adopt", bad, excerpt], workspace)
        assert code_bad == 2 and not (workspace / "outside.md").exists(), f"unsafe ZIP: exit {code_bad}"
        return "the ZIP is unpacked beside it and adopted (exit 0); a ZIP with ../ stops with exit 2"
    adopt_zip()

    @group("adopt stops with exit 2 and one plain line, changing nothing: no story, not a breakdown, another story")
    def adopt_stops():
        folder_stop = workspace / "stop" / "The Catch - breakdown"
        shutil.copytree(CHAT_FOLDER, folder_stop)
        before = snapshot(folder_stop)
        cases = []
        code_missing, output_missing = stage(["adopt", folder_stop, workspace / "no story.txt"], workspace)
        cases.append(("missing story", code_missing, output_missing))
        empty = workspace / "stop" / "empty"
        empty.mkdir()
        code_empty, output_empty = stage(["adopt", empty, excerpt], workspace)
        cases.append(("not a breakdown", code_empty, output_empty))
        start = folder_stop / "00 Start here.md"
        start_text = start.read_text(encoding="utf-8")
        start.write_text(start_text.replace("- source_fingerprint: none", "- source_fingerprint: " + "a" * 64),
                         encoding="utf-8")
        before = snapshot(folder_stop)
        code_other, output_other = stage(["adopt", folder_stop, excerpt], workspace)
        cases.append(("another story", code_other, output_other))
        wrong = [f"{name}: exit {code}, {output.strip()[:120]}" for name, code, output in cases
                 if code != 2 or len(output.strip().splitlines()) != 1]
        assert not wrong, "; ".join(wrong)
        # every command writes its line in log.jsonl, a refused one too (7.3); nothing else may change
        after = {name: data for name, data in snapshot(folder_stop).items() if name != f"{MACHINE}/log.jsonl"}
        assert after == before, f"files changed: {sorted(set(after) ^ set(before)) or 'contents'}"
        return "; ".join(f"{name}: {output.strip()[:70]}" for name, _, output in cases)
    adopt_stops()


def impact_groups(workspace, excerpt):
    folder = make_gold_project(workspace / "gold impact" / "The Catch", excerpt)
    gold_files = record_files_of(folder)
    index = merged_index(gold_files)[0]

    def citing(identifier, type_name):
        found = set()
        for key, record in index.items():
            if key[0] != type_name:
                continue
            for line in record.fields:
                if re.search(rf"(?<![\w-]){re.escape(identifier)}(?![\w.-]|\d)", line.value):
                    found.add(key[1])
        return found

    expected_shots = citing("SC10-B07", "SHOT")
    for value in index[("SHOTLIST", "SC10-LIST")].get_all("item"):
        item = split_item(value, SCHEMA.field("SHOTLIST", "item"))
        if "SC10-B07" in split_list(item.get("beats") or ""):
            expected_shots.add(item.first.strip())

    @group("impact SC10-B07 lists the shots that cite it, and what goes stale downstream only")
    def impact_beat():
        before = snapshot(folder)
        code, output = stage(["impact", "SC10-B07", "--json"], folder)
        assert code == 0, f"exit {code}: {output[:600]}"
        data = json.loads(output)
        shots = set(data["shots_citing"])
        assert shots == expected_shots, f"shots {sorted(shots)}, the records say {sorted(expected_shots)}"
        stale = {entry["id"] for entry in data["stale"]}
        wanted = expected_shots | {"SC10", "SC10-LIST", "SC10-P1"} | citing("SC10-B07", "MOVE")
        assert wanted <= stale, f"not stale: {sorted(wanted - stale)}"
        not_citing = {key[1] for key in index if key[0] == "SHOT"} - expected_shots
        wrongly = sorted(stale & not_citing)
        assert not wrongly, f"shots that do not cite beat 7 marked stale: {wrongly}"
        assert not any(entry["type"] in ("CHARACTER", "PLAN", "CAMSYS", "LOOK") for entry in data["stale"]), \
            "an earlier step's record went stale"
        earlier = {entry["id"] for entry in data["earlier_in_the_work"]}
        assert "PL-08" in earlier, f"the plant whose story point resolves to beat 7 is not listed as earlier: {sorted(earlier)}"
        assert any(unit.startswith("U-07-SC10") for unit in data["units"]) and \
            any(unit.startswith("U-08-SC10") for unit in data["units"]), f"units: {data['units']}"
        code_text, text = stage(["impact", "SC10-B07"], folder)
        assert code_text == 0 and f"Shots that cite it: {', '.join(sorted(expected_shots))}." in text, text[:1500]
        after = {name: data_bytes for name, data_bytes in snapshot(folder).items() if not name.endswith("log.jsonl")}
        assert after == {name: data_bytes for name, data_bytes in before.items() if not name.endswith("log.jsonl")}, \
            "impact changed a file"
        return (f"shots {', '.join(sorted(shots))}; stale {len(stale)} records ({', '.join(sorted(stale))}); "
                f"units {', '.join(data['units'])}; no file changed")
    impact_beat()

    @group("impact on a speech, a state and a camera: the shots that hear, show or use them; an unknown ID stops with "
           "exit 2")
    def impact_others():
        results = []
        cases = [("SC10-SU02", citing("SC10-SU02", "SHOT")), ("CH-IONA.S02", citing("CH-IONA.S02", "SHOT"))]
        if excerpt is not None:
            cases.append(("SC10-D11", citing("SC10-D11", "SHOT")))
        for identifier, wanted in cases:
            code, output = stage(["impact", identifier, "--json"], folder)
            assert code == 0, f"{identifier}: exit {code}: {output[:300]}"
            shots = set(json.loads(output)["shots_citing"])
            assert shots == wanted and wanted, f"{identifier}: {sorted(shots)}, the records say {sorted(wanted)}"
            results.append(f"{identifier}: {len(shots)} shots")
        code, output = stage(["impact", "SC10-B99"], folder)
        assert code == 2 and len(output.strip().splitlines()) == 1, f"unknown ID: exit {code}, {output[:200]}"
        return "; ".join(results) + "; SC10-B99: exit 2"
    impact_others()


def question_groups(workspace, excerpt, state):
    folder = make_gold_project(workspace / "gold questions" / "The Catch", excerpt)
    index = merged_index(record_files_of(folder))[0]
    turn_shots = sorted(key[1] for key, record in index.items()
                        if key[0] == "SHOT" and (record.get("role") or "") == "turn")
    must_keep = sorted(key[1] for key, record in index.items()
                       if key[0] == "SHOT" and (record.get("role") or "") == "must_keep")
    turn_beats = sorted(key[1] for key, record in index.items()
                        if key[0] == "BEAT" and (record.get("turn") or "none") != "none")
    batch_size = CONSTANTS["from_blueprint_text"]["constants"]["question_batch_size"]["value"]
    share = CONSTANTS["from_blueprint_text"]["constants"]["question_sample_share"]["value"]

    @group("questions --sample --seed 1: yes/no questions for every turn shot of the gold, every turn beat and "
           "must-keep shot, each citing its lines, in batches")
    def questions_gold():
        code, output = stage(["questions", "--sample", "--seed", "1"], folder)
        assert code == 0, f"exit {code}: {output[:800]}"
        data = json.loads((folder / MACHINE / "questions.json").read_text(encoding="utf-8"))
        questions = [question for batch in data["batches"] for question in batch["questions"]]
        assert questions, "no questions"
        by_record = {}
        for question in questions:
            by_record.setdefault(question["record"], []).append(question)
        assert turn_shots == ["SC10-SH150", "SC10-SH190"], f"the gold's turn shots: {turn_shots}"
        for shot in turn_shots:
            asked = by_record.get(shot, [])
            assert asked and all("turn shot" in question["asked_because"] for question in asked), \
                f"{shot}: {len(asked)} questions"
            assert any("turn shot of beat" in question["question"] for question in asked), f"{shot}: no turn question"
        missing = [record for record in must_keep + turn_beats if record not in by_record]
        assert not missing, f"no questions for {missing}"
        wrong = []
        for question in questions:
            text = question["question"]
            if not text.endswith("?") or " | " in text or '"' in text:
                wrong.append(f"not a clean yes/no question: {text[:80]}")
            if not re.search(r"\blines? \d+", text) and not question["lines"]:
                wrong.append(f"cites no lines: {text[:80]}")
        assert not wrong, shorten(wrong)
        sizes = [len(batch["questions"]) for batch in data["batches"]]
        assert max(sizes) <= batch_size, f"a batch holds {max(sizes)}"
        assert [batch["unit"] for batch in data["batches"]] == [f"U-10-QUESTIONS-B{number}"
                                                                for number in range(1, len(sizes) + 1)]
        heard = [question["question"] for question in by_record["SC10-SH150"] if "off screen" in question["question"]]
        if excerpt is not None:
            # changed after the second full run (Project notes 39, F26): a long speech is named by the line it
            # starts with, never with "...", which apply refuses when the answer copies the question
            example = [question for question in heard
                       if "line that starts 'Nothing has happened to the mint.'" in question]
            assert example, "no question on Saye's line that starts 'Nothing has happened to the mint.' heard off " \
                            "screen (11.2's example)"
            assert not any("..." in question["question"] for question in questions), "a question holds '...'"
        else:
            example = [question for question in heard if "speech SC10-D12" in question]
            assert example, "no question on speech SC10-D12 heard off screen (the speeches are not known without a story)"
        assert (folder / MACHINE / "questions.md").is_file(), "questions.md was not written"
        first = json.dumps(data["batches"], sort_keys=True)
        code_again, _ = stage(["questions", "--sample", "--seed", "1"], folder)
        again = json.loads((folder / MACHINE / "questions.json").read_text(encoding="utf-8"))
        assert code_again == 0 and json.dumps(again["batches"], sort_keys=True) == first, "seed 1 gave other questions"
        return (f"{len(questions)} questions in {len(sizes)} batches ({', '.join(map(str, sizes))}); turn shots "
                f"{', '.join(turn_shots)}: {len(by_record['SC10-SH150'])} and {len(by_record['SC10-SH190'])} questions; "
                f"e.g. \"{example[0]}\"")
    questions_gold()

    @group("questions: the seeded share of the other shots (question_sample_share), the same for the same seed")
    def questions_sample():
        # a gold variant with many other shots: no mirror rule, no must-keep roles, no flip overrides, no glass
        sample_folder = make_gold_project(workspace / "gold sample" / "The Catch", excerpt)
        scene_path = sample_folder / SCENE_FILE
        scene_text = scene_path.read_text(encoding="utf-8")
        scene_text = scene_text.replace("- role: must_keep", "- role: normal").replace("- flip: never", "- flip: auto")
        scene_text = re.sub(r"^- glass: .*$", "- glass: none", scene_text, flags=re.MULTILINE)
        scene_text = scene_text.replace("| role: must_keep |", "| role: normal |")
        scene_path.write_text(scene_text, encoding="utf-8")
        world = sample_folder / "06 World and style.md"
        world.write_text(recount(cut_record(world.read_text(encoding="utf-8"), "RULE WR-MIRROR")[0]), encoding="utf-8")
        results = {}
        for seed in (1, 1, 7, 12):
            code, output = stage(["questions", "--sample", "--seed", seed], sample_folder)
            assert code == 0, f"exit {code}: {output[:600]}"
            data = json.loads((sample_folder / MACHINE / "questions.json").read_text(encoding="utf-8"))
            sampled = sorted({question["record"] for batch in data["batches"] for question in batch["questions"]
                              if question["asked_because"] == "sampled"})
            results.setdefault(seed, []).append(sampled)
            others = data["counts"]["other shots"]
            assert others >= 10, f"only {others} other shots in the variant"
            wanted = min(others, max(1, math.ceil(share * others)))
            assert len(sampled) == wanted, f"seed {seed}: {len(sampled)} sampled of {others}, not {wanted}"
            # the seeded rule: random.Random(seed).sample of the other shots in ID order
            other_shots = data.get("other_shots", [])
            assert len(other_shots) == others, "questions.json does not list the other shots"
            expected = sorted(random.Random(seed).sample(other_shots, wanted))
            assert sampled == expected, f"seed {seed} sampled {sampled}, the seeded rule gives {expected}"
            asked = {question["record"] for batch in data["batches"] for question in batch["questions"]}
            assert set(turn_shots) <= asked, "a turn shot was left out of the sample run"
        assert results[1][0] == results[1][1], "the same seed sampled other shots"
        code_all, _ = stage(["questions"], sample_folder)
        data_all = json.loads((sample_folder / MACHINE / "questions.json").read_text(encoding="utf-8"))
        every = {question["record"] for batch in data_all["batches"] for question in batch["questions"]}
        shots = {key[1] for key in merged_index(record_files_of(sample_folder))[0] if key[0] == "SHOT"}
        assert code_all == 0 and shots <= every, f"without --sample not every shot is asked about: {sorted(shots - every)}"
        return (f"{others} other shots, {wanted} sampled: seed 1 gives {results[1][0]} twice, seed 7 {results[7][0]}, "
                f"seed 12 {results[12][0]}, each as random.Random(seed) gives; without --sample every shot is asked about")
    questions_sample()


if __name__ == "__main__":
    sys.exit(main())
