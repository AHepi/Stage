"""The acceptance test of the routing files and the layout after the restructure's second cross-examination
(Project notes 43, round 2, findings R-F1 to R-F7): the folders-as-steps layout keeps its routing files true.

What it proves, in plain words:
- R-F1: every backticked path in the four routing files (the top CONTEXT.md, stages/CONTEXT.md, references/CONTEXT.md
  and _config/CONTEXT.md) leads somewhere: a file or folder of the repository or the kit, or a project file the
  schema or the steps name; stages/CONTEXT.md names, for every step, its folder, every record type it reads and every
  file it writes as _config/schema/steps.json lists them, and is exactly what build-kit makes from steps.json; each
  step file's Outputs and steps.json name the same numbered project files;
- R-F2: the user's part of the top CONTEXT.md names no kit folder path, no "stages" and no step 0 to 16 numbering
  (those stay in the maintainers' row), and says the project's files are numbered in reading order, not in the
  order they are made;
- R-F3: references/CONTEXT.md says what each ZIP carries of the library, as build-kit makes them;
- R-F4: no kit text names an old folder (library/, reference/, steps/, cards/, rules/, schema/, adapters/,
  templates/, examples/ on their own, or the old top-level names) outside 04 Project history, the tests and a few
  phrases quoted from research;
- R-F5: the chat kit's file map says where the three routing files are;
- R-F6: the guides for the Claude apps, ChatGPT and Gemini each say to replace the whole kit for a newer Stage;
- R-F7: a handout is grouped under two headings, the rules for this piece of work (the same for every story) and
  what you are working on (this story), with the one-line task first and last.

Fixtures: the gold example (references/examples/01 and 02, scene 10) made into a temporary project; nothing reads
a user's story or project.

Usage: python tests/fix07_routing_and_layout_acceptance.py
Standard library only.
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
TOOLS = SKILL / "tools"
STAGE = TOOLS / "stage.py"
sys.path.insert(0, str(TOOLS))

from stage_tools import build_kit  # noqa: E402
from stage_tools.record_format import DIVIDER_LINE  # noqa: E402

ROUTING_FILES = [REPOSITORY / "CONTEXT.md", SKILL / "stages" / "CONTEXT.md", SKILL / "references" / "CONTEXT.md",
                 SKILL / "_config" / "CONTEXT.md"]
STEPS = json.loads((SKILL / "_config" / "schema" / "steps.json").read_text(encoding="utf-8"))
SCHEMA = json.loads((SKILL / "_config" / "schema" / "schema.json").read_text(encoding="utf-8"))
CHAT_KIT = REPOSITORY / "03 Kits to upload" / "Chat kit"
PRIVATE_OR_COPIES = {".git", "My stories", "My breakdowns", "worktrees", "__pycache__"}
MACHINE = "For machines - do not edit"
RESULTS = []


def report(passed, group, detail=""):
    RESULTS.append(bool(passed))
    print(f"{'PASS' if passed else 'FAIL'}  {group}" + (f": {detail}" if detail else ""), flush=True)


def group(title):
    def decorator(function):
        try:
            detail = function()
        except AssertionError as error:
            report(False, title, str(error)[:900])
            return function
        except Exception as error:  # a fault fails this group only
            report(False, title, f"{type(error).__name__}: {error}"[:900])
            return function
        report(True, title, detail or "")
        return function
    return decorator


def read(path):
    return Path(path).read_text(encoding="utf-8")


def files_under(folder):
    """Every file under a folder, leaving out git, the user's own stories and projects, and worktree copies."""
    found = []
    for path in Path(folder).rglob("*"):
        parts = set(path.relative_to(folder).parts)
        if parts & PRIVATE_OR_COPIES or not path.is_file():
            continue
        found.append(path)
    return found


SEARCH_CACHE = {}


def names_under(folder):
    """{relative path (as text, with and without .md), name and stem} of every file and folder under a folder."""
    folder = Path(folder)
    if folder not in SEARCH_CACHE:
        names = set()
        for path in folder.rglob("*"):
            relative = path.relative_to(folder)
            if set(relative.parts) & PRIVATE_OR_COPIES:
                continue
            text = relative.as_posix()
            names.update({text, path.name, path.stem})
            if text.endswith(".md"):
                names.add(text[:-3])
        SEARCH_CACHE[folder] = names
    return SEARCH_CACHE[folder]


def project_file_names():
    """The project files the kit knows: every file a record type is stored in (schema.json) and every file a step
    writes (steps.json), with and without .md, and their first folder."""
    names = set()
    entries = [name for record_type in SCHEMA["record_types"].values() for name in record_type.get("files", [])]
    entries += [name for step in STEPS["steps"] for name in step["files_written"]]
    for entry in entries:
        name = entry.split(" (")[0].strip()
        first = name.split("/")[0]
        names.update({name, name.rstrip("/"), first, first[:-3] if first.endswith(".md") else first})
        if name.endswith(".md"):
            names.add(name[:-3])
    return names


def path_like(token):
    """True when a backticked text names a file or a folder (not a command, a field or a code)."""
    if re.match(r"^(stage\.py|python|--)", token) or " --" in token:
        return False
    return "/" in token or bool(re.search(r"\.(md|json|py|zip|html|txt|csv)$", token)) or \
        bool(re.match(r"^\d\d [A-Z]", token)) or token in ("My stories", "My breakdowns", MACHINE)


def resolves(token, routing_file, project_names):
    """True when a backticked path leads somewhere (see the note at the top of this file)."""
    pieces = []
    for piece in token.rstrip("/").split("/"):
        if "<" in piece or re.search(r"\bNN\b", piece) or piece == "...":
            break  # a placeholder: what comes before it must exist
        pieces.append(piece)
    if not pieces:
        return True
    wanted = "/".join(pieces)
    folder = routing_file.parent
    for base in (folder, REPOSITORY, SKILL):
        if (base / wanted).exists() or (base / (wanted + ".md")).exists():
            return True
    for root in (folder, CHAT_KIT, REPOSITORY / "01 Start here", REPOSITORY / "tests"):
        if root.is_dir() and wanted in names_under(root):
            return True
    return pieces[0] in project_names or wanted in project_names


def backticked(text):
    return re.findall(r"`([^`\n]+)`", text)


def table_cells(line):
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip()[1:-1])]


def step_rows():
    """{step number: cells} of the step rows of stages/CONTEXT.md."""
    rows = {}
    for line in read(SKILL / "stages" / "CONTEXT.md").splitlines():
        match = re.match(r"^\|\s*(\d+)\s*\|", line)
        if match:
            rows[int(match.group(1))] = table_cells(line)
    return rows


NUMBERED_FILE = re.compile(r"\b(\d\d) [A-Z][a-z]")
MACHINE_FILE = re.compile(r"(Original/|speeches\.json|breakdown\.json|timeline|previs plans)")


def project_files_named(text):
    """The numbered project files ('05' for 05 Story plan) and machine files a text names."""
    return set(NUMBERED_FILE.findall(text)) | set(MACHINE_FILE.findall(text))


def section_of(text, heading):
    match = re.search(r"(?ms)^## " + re.escape(heading) + r"\n(.*?)(?=^## |\Z)", text)
    return match.group(1) if match else ""


def make_gold_project(folder):
    """A project folder from the gold: the scene file in 11 Scenes and each '## From <file>' part of the context file
    as its numbered file (as tests/wp5_acceptance.py makes it)."""
    folder.mkdir(parents=True)
    (folder / MACHINE).mkdir()
    examples = SKILL / "references" / "examples"
    context = read(examples / "02 The Catch - scene 10 - context.md").split(DIVIDER_LINE, 1)[1]
    sections = re.split(r"^## From (.+)$", context, flags=re.MULTILINE)[1:]
    for name, body in zip(sections[0::2], sections[1::2]):
        body = re.sub(r"\n+END OF FILE .*$", "", body.strip(), flags=re.DOTALL)
        count = len(re.findall(r"^### ", body, re.MULTILINE))
        (folder / f"{name.strip()}.md").write_text(
            f"# {name.strip()}\n\n{DIVIDER_LINE}\n\n{body}\n\nEND OF FILE | {name.strip()} | {count} records\n",
            encoding="utf-8")
    (folder / "11 Scenes").mkdir()
    shutil.copy(examples / "01 The Catch - scene 10.md", folder / "11 Scenes" / "Scene 10 - Saye's kitchen.md")
    return folder


# ---------------------------------------------------------------- the groups

@group("R-F1: every backticked path in the four routing files leads to a file or folder of the repository or the kit, "
       "or to a project file the schema or the steps name")
def routing_paths_resolve():
    project_names = project_file_names()
    checked, broken = 0, []
    for routing_file in ROUTING_FILES:
        for token in backticked(read(routing_file)):
            if not path_like(token):
                continue
            checked += 1
            if not resolves(token, routing_file, project_names):
                broken.append(f"{routing_file.relative_to(REPOSITORY)}: `{token}`")
    assert checked > 50, f"only {checked} paths found"
    assert not broken, broken
    return f"{checked} paths in {len(ROUTING_FILES)} files lead somewhere"


@group("R-F1: stages/CONTEXT.md names, for every step, its folder, every record type it reads and every file it "
       "writes as _config/schema/steps.json lists them, and is exactly what build-kit makes from steps.json")
def steps_list_agrees():
    rows = step_rows()
    problems = []
    for step in STEPS["steps"]:
        cells = rows.get(step["step"])
        if cells is None:
            problems.append(f"step {step['step']} has no row")
            continue
        folder = step["step_file"].split("/")[1]
        if cells[1] != f"`{folder}/`":
            problems.append(f"step {step['step']}: folder {cells[1]}, not {folder}/")
        reads, writes = cells[-2], cells[-1]
        for entry in step["reads"]:
            if entry not in reads:
                problems.append(f"step {step['step']} reads {entry!r}, not in its Reads cell")
        for entry in step["files_written"]:
            name = entry.split(" (")[0].strip()
            if name not in writes:
                problems.append(f"step {step['step']} writes {name!r}, not in its Writes cell")
    assert not problems, problems
    current = read(SKILL / "stages" / "CONTEXT.md")
    assert build_kit.steps_list_text(current, STEPS) == current, \
        "stages/CONTEXT.md differs from what build-kit makes from steps.json: run stage.py build-kit"
    return f"{len(STEPS['steps'])} steps agree with steps.json, and the file is up to date with build-kit"


@group("R-F1: each step file's Outputs and steps.json's files_written name the same numbered project files")
def step_outputs_agree():
    problems = []
    for step in STEPS["steps"]:
        text = read(SKILL / step["step_file"])
        outputs = section_of(text, "Outputs")
        assert outputs, f"{step['step_file']} has no Outputs section"
        in_json = project_files_named(" ".join(step["files_written"]))
        in_file = project_files_named(outputs)
        if in_json != in_file:
            problems.append(f"step {step['step']}: steps.json only {sorted(in_json - in_file)}, "
                            f"the step file only {sorted(in_file - in_json)}")
    assert not problems, problems
    return f"{len(STEPS['steps'])} step files agree with steps.json"


@group("R-F2: the user's part of the top CONTEXT.md names no kit folder path, no 'stages' and no step 0 to 16 "
       "numbering, and says the project's files are numbered in reading order, not in the order they are made")
def top_context_in_users_words():
    text = read(REPOSITORY / "CONTEXT.md")
    maintainers = [line for line in text.splitlines() if "(for maintainers)" in line]
    assert len(maintainers) == 1, "no single maintainers' row"
    users_part = "\n".join(line for line in text.splitlines() if "(for maintainers)" not in line)
    problems = []
    for pattern, what in ((r"\.claude/", "a kit folder path"), (r"\bstages?\b", "the word 'stage' or 'stages'"),
                          (r"\bstep (?:0|16)\b|\b0 to 16\b", "the step 0 to 16 numbering"),
                          (r"`(?:references|_config|stages)/", "a kit folder")):
        found = re.findall(pattern, users_part)
        if found:
            problems.append(f"{what}: {found[:3]}")
    assert not problems, problems
    assert "in the order you read them" in users_part and "not in the order they are made" in users_part, \
        "the numbered files are not described as in reading order"
    assert ".claude/skills/breaking-down-stories/stages/CONTEXT.md" in maintainers[0], "the maintainers' row lacks the list of steps"
    return "the user's part is in plain words; the paths are in the maintainers' row"


@group("R-F3: references/CONTEXT.md says what each ZIP carries of the library, as build-kit makes them")
def library_claim_true():
    tools_names = [name for name, _ in build_kit.tools_zip_entries(SKILL)]
    skill_names = [name for name, _ in build_kit.skill_zip_entries(SKILL)]
    library = "references/library/"
    in_tools = [name for name in tools_names if library in name]
    in_skill = [name for name in skill_names if library in name]
    assert not any(re.search(r"/library/D\d+ ", name) for name in in_tools), "07 Tools.zip holds D files"
    assert any(re.search(r"/library/D\d+ ", name) for name in in_skill), "the skill ZIP holds no D files"
    assert any("/digests/" in name for name in in_tools) and any("/digests/" in name for name in in_skill)
    row = next(line for line in read(SKILL / "references" / "CONTEXT.md").splitlines() if line.startswith("| `library/`"))
    assert "07 Tools.zip only the digests and the three notes" in row, row[-200:]
    assert "The skill ZIP carries the digests, the D files and the three notes" in row, row[-200:]
    return f"07 Tools.zip: {len(in_tools)} library files, no D file; the skill ZIP: {len(in_skill)}, with the D files"


OLD_KIT_FOLDER = re.compile(r"(?<![\w/.-])(library|reference|steps|cards|rules|schema|adapters|templates|examples)/(?=\w)")
OLD_TOP_NAMES = re.compile(r"\b07 Chat kit\b|\b08 Skill for Claude apps\b|\b09 Example - The Catch\b|"
                           r"(?<![\w/])Project notes/")
# Phrases quoted from research that only look like old folder names.
QUOTED_RESEARCH = ("examples/catch-SC06.json", "examples/shots", "library/record", "Veo reference/frame")


@group("R-F4: no kit text names an old folder (library/, reference/, steps/, cards/, rules/ and the rest on their "
       "own, or the old top-level names) outside 04 Project history, the tests and phrases quoted from research")
def no_old_folder_names():
    stage_folders = [path.name for path in (SKILL / "stages").iterdir() if path.is_dir()]
    problems, read_count = [], 0
    for path in files_under(REPOSITORY):
        relative = path.relative_to(REPOSITORY)
        if relative.parts[0] in ("04 Project history", "tests") or path.suffix not in (".md", ".txt", ".json", ".py"):
            continue
        text = read(path)
        read_count += 1
        for name in stage_folders:
            text = text.replace(name + "/", "")
        for phrase in QUOTED_RESEARCH:
            text = text.replace(phrase, "")
        for line_number, line in enumerate(text.splitlines(), 1):
            for match in OLD_KIT_FOLDER.finditer(line):
                # a routing file may name a folder beside it ("cards/" in references/CONTEXT.md)
                if path.name == "CONTEXT.md" and (path.parent / match.group(1)).is_dir():
                    continue
                problems.append(f"{relative}:{line_number}: {line[max(0, match.start() - 30):match.end() + 20]!r}")
            for match in OLD_TOP_NAMES.finditer(line):
                problems.append(f"{relative}:{line_number}: {match.group(0)!r}")
    assert not problems, problems[:12]
    return f"{read_count} files read; no old folder name"


@group("R-F5: the chat kit's file map says where the three routing files are, in 07 Tools.zip only")
def kit_map_names_routing_files():
    table = build_kit.kit_map_table()
    row = next((line for line in table.splitlines() if "`stages/CONTEXT.md`" in line), "")
    assert row and "`references/CONTEXT.md`" in row and "`_config/CONTEXT.md`" in row, table
    assert "07 Tools.zip only" in row and "without code" in row, row
    entries = [name for name, _ in build_kit.tools_zip_entries(SKILL)]
    for name in ("stages/CONTEXT.md", "references/CONTEXT.md", "_config/CONTEXT.md"):
        assert f"breaking-down-stories/{name}" in entries, f"07 Tools.zip lacks {name}"
    assert row in build_kit.house_rules_text(SKILL), "01 House rules lacks the row"
    return "the map's row is in 01 House rules, and 07 Tools.zip holds the three files"


@group("R-F6: the guides for the Claude apps, ChatGPT and Gemini each say to replace the whole kit for a newer "
       "Stage, and that breakdowns keep working")
def guides_say_replace_the_kit():
    guides = ["02 Using Claude.md", "03 Using ChatGPT.md", "04 Using Gemini or another chat app.md"]
    missing = []
    for name in guides:
        text = read(REPOSITORY / "01 Start here" / name)
        sentence = next((line for line in text.splitlines() if "When you get a newer Stage" in line), "")
        if not sentence or "keep working" not in sentence or "replace" not in sentence:
            missing.append(name)
    assert not missing, missing
    return f"{len(guides)} guides"


@group("R-F7: a handout is grouped under two headings, the rules for this piece of work (the same for every story), "
       "then what you are working on (this story), with the one-line task first and last")
def handout_in_two_groups():
    from stage_tools.make_handout import RULES_HEADING, WORK_HEADING
    workspace = Path(tempfile.mkdtemp(prefix="fix07 "))
    try:
        project = make_gold_project(workspace / "gold")
        completed = subprocess.run([sys.executable, str(STAGE), "handout", "U-08-SC10-B1", "--project", str(project)],
                                   capture_output=True, text=True, encoding="utf-8", cwd=str(REPOSITORY), timeout=600,
                                   env={"STAGE_LOCK_WAIT_SECONDS": "5", "PATH": "/usr/bin:/bin"})
        assert completed.returncode == 0, (completed.stdout + completed.stderr)[:800]
        text = read(project / MACHINE / "handouts" / "U-08-SC10-B1.md")
    finally:
        shutil.rmtree(workspace, ignore_errors=True)
    lines = text.splitlines()
    assert lines[0].startswith("# Handout ") and lines[-1].startswith("**One-line task, again:**"), (lines[0], lines[-1])
    assert text.count(RULES_HEADING) == 1 and text.count(WORK_HEADING) == 1, "the two headings are not there once each"
    rules_at, work_at = text.index(RULES_HEADING), text.index(WORK_HEADING)
    assert rules_at < work_at, "the story's material comes before the rules"
    for heading in ("## The step file:", "## Card part:", "## The record template", "## One example from the gold"):
        at = text.find(heading)
        assert rules_at < at < work_at, f"{heading} is not under the rules"
    for heading in ("## This unit", "## This batch", "## Records you need"):
        at = text.find(heading)
        assert at > work_at, f"{heading} is not under what you are working on"
    assert text.index("**One-line task:**") < rules_at, "the one-line task does not open the handout"
    return "rules, then this story's material, inside the one-line task"


def main():
    failing = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({RESULTS.count(True)} passed, {failing} failing groups)")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
