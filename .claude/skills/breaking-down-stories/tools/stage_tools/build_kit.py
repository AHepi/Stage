"""build_kit.py: builds, from the skill folder, every file the Stage repository hands out, and runs the command
build-kit (blueprint 7.1, 2.1, 2.3, 2.5). It is a maintainers' tool: the AI never runs it for a user.

In plain words, `python .claude/skills/breaking-down-stories/tools/stage.py build-kit` writes:
- reference/03 Field guide.md in the skill: every record type and field of schema/schema.json in plain words;
- AGENTS.md at the top of the repository: SKILL.md's rules with every path written out, for coding agents
  other than Claude Code;
- 07 Chat kit/: exactly the 13 files of blueprint 2.5 for a ChatGPT Project or a Gemini Gem: the text to paste
  into the instruction box, six knowledge files joined from the skill's own files, the tools as one ZIP, and
  five step-group files that each chat attaches;
- 08 Skill for Claude apps.zip: the skill folder, with breaking-down-stories/SKILL.md at the top of the ZIP, for
  Customize > Skills on the Claude website and in Claude desktop (the research library cut to its digests, its
  D files and its three notes, to keep the ZIP small);
- 09 Example - The Catch, scene 10/: a small finished project folder made from the gold example (the records of
  examples/01 and 02, built, checked and made into a book by stage.py itself), holding only the files blueprint
  2.3 names.

Everything is made from the skill folder, so there is one source: edit the skill, then run build-kit again.
Files it made before are replaced; nothing else in the repository is touched. ZIPs are written with fixed dates
and a fixed file order, so building twice from the same skill gives the same bytes.

Command: build-kit [--repository <folder>] [--story <story file>] [--skip-example]
Exit 0: built (size notes may be printed); 1: built, but a hard limit failed (the instruction text is too long,
a source file is missing, a ZIP is laid out wrongly); 2: could not run.
Standard library only.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from .project_files import Project, StageStop, today
from .record_format import DIVIDER_LINE, SKILL_FOLDER

SKILL_NAME = "breaking-down-stories"
CHAT_KIT_FOLDER = "07 Chat kit"
SKILL_ZIP_NAME = "08 Skill for Claude apps.zip"
EXAMPLE_FOLDER = "09 Example - The Catch, scene 10"
AGENTS_FILE = "AGENTS.md"
FIELD_GUIDE = "reference/03 Field guide.md"
TOOLS_ZIP_NAME = "07 Tools.zip"
INSTRUCTIONS_NAME = "00 Paste into instructions.txt"
GOLD_SCENE = "examples/01 The Catch - scene 10.md"
GOLD_CONTEXT = "examples/02 The Catch - scene 10 - context.md"
STORY_EXCERPT = "tests/fixtures/The Catch - lines 397-489.txt"
MACHINE_FOLDER = "For machines - do not edit"
ZIP_DATE = (2026, 1, 1, 0, 0, 0)  # one fixed date for every entry, so the same skill gives the same ZIP
LEAVE_OUT_NAMES = {"__pycache__", ".DS_Store", "proposal", "previous", ".git"}
LEAVE_OUT_ENDINGS = (".pyc", ".pyo", ".part", "~")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9.-]+")

# The knowledge and step-group files of blueprint 2.5: name, the skill files joined in order, the target length in
# English words ("about"), and how it is used. Cards and steps are named by their two-digit number.
CARD_GROUPS = {
    "02 Cards - story and scenes.md": ["01", "02", "03", "04", "05", "06", "07", "15", "16", "17", "18", "19", "20"],
    "03 Cards - picture, sound and making.md": ["08", "09", "10", "11", "12", "13", "14", "21", "22", "23", "24"],
}
STEP_GROUPS = {
    "08 Steps 00-02 - start, reading, plan.md": ["00", "01", "02"],
    "09 Steps 03-06 - world, people, continuity, film rules.md": ["03", "04", "05", "06"],
    "10 Steps 07-08 - scenes and shots.md": ["07", "08"],
    "11 Steps 09-11 and 16 - film pass, check, book, resume.md": ["09", "10", "11", "16"],
    "12 Steps for add-ons - storyboards, prompts, finishing.md": ["12", "14", "15"],
}
KIT_FILES = [
    # (file name, kind, target words, what it is for)
    (INSTRUCTIONS_NAME, "instructions", None, "the Project or Gem instruction box"),
    ("01 House rules.md", "knowledge", 5500, "knowledge"),
    ("02 Cards - story and scenes.md", "knowledge", 16000, "knowledge"),
    ("03 Cards - picture, sound and making.md", "knowledge", 18000, "knowledge"),
    ("04 Templates and word list.md", "knowledge", 12000, "knowledge"),
    ("05 Checks in words.md", "knowledge", 2500, "knowledge, and attached to every check chat"),
    ("06 Example - The Catch, scene 10.md", "knowledge", 6000, "knowledge"),
    (TOOLS_ZIP_NAME, "tools", None, "ChatGPT only (not uploaded to Gemini)"),
    ("08 Steps 00-02 - start, reading, plan.md", "steps", 5000, "attached to the chats of steps 1 to 3"),
    ("09 Steps 03-06 - world, people, continuity, film rules.md", "steps", 7000,
     "attached to the chats of steps 4 to 7"),
    ("10 Steps 07-08 - scenes and shots.md", "steps", 3600, "attached to every scene chat"),
    ("11 Steps 09-11 and 16 - film pass, check, book, resume.md", "steps", 7000,
     "attached to the chats of steps 10 to 12 and to a chat that resumes after a problem"),
    ("12 Steps for add-ons - storyboards, prompts, finishing.md", "steps", 5000,
     "attached when the user asks for storyboards, prompts for AI video or the edit plan"),
]
SIZE_TOLERANCE = 0.25  # "about" in blueprint 2.5: within a quarter of the target
KNOWLEDGE_TOTAL_ABOUT = 60000  # blueprint 2.5 and rules/limits.json chat_kit.knowledge_words_total_about

# The records of the gold scene kept in the chat kit's example (06): its plain part whole, the scene's design, the
# two turns and the beats around them, a floor-plan move, three setups, the one-line shot list, and six shots of
# different kinds (the first shot, the saved reflection frame, a line heard over a thing, the turn, the held wide,
# the last line) with the cut to black and the title card. The whole file is in 07 Tools.zip and in 09 Example.
EXAMPLE_EXCERPT_RECORDS = [
    "SC10", "SC10-P1", "SC10-P2", "SC10-B01", "SC10-B06", "SC10-B07", "SC10-B11", "SC10-M01", "SC10-M05",
    "SC10-SU01", "SC10-SU02", "SC10-SU06", "SC10-LIST", "SC10-SH010", "SC10-SH080", "SC10-SH130", "SC10-SH150",
    "SC10-SH190", "SC10-SH200", "SC10-C200", "SC10-SH990",
]

# The folder 09 Example holds only these (blueprint 2.3), plus the book made from them.
EXAMPLE_FILES = ["00 Start here.md", "01 Choices.md", "04 Scene list.md", "07 Characters and voices.md",
                 "08 Places and things.md", "09 Continuity.md", "10 Film rules.md"]
EXAMPLE_BOOK_FILES = ["15 The breakdown/The breakdown.md", "15 The breakdown/The breakdown.html"]
EXAMPLE_LAST_UNIT = "U-08-SC10-B2"  # the gold's 21 shots are two batches of the chat batch size (12)

# The text for the instruction box of a ChatGPT Project or a Gemini Gem (blueprint 2.5): the house rules
# condensed. It must stay within rules/limits.json chat_kit.instructions_characters_max (6,000 characters).
INSTRUCTIONS_TEXT = """\
You are Stage, a story-breakdown helper. You turn the user's story (a screenplay, a novel, a short story, a play) into a scene-by-scene plan for making it as a film, including with AI picture and video tools. You do the work; the user decides only what matters.

FILES ARE THE MEMORY
- Knowledge: 01 House rules (the full rules and every message shape), 02 and 03 (craft cards), 04 (templates, record format, word list, rule order), 05 Checks in words, 06 (a finished example scene). Look things up there.
- Each working chat attaches one step file (08 to 12). Read it whole, every time; the resume line names it.
- The user's saved files are the project: 00 Start here, 02 Whole-film summary, 10 Film rules, the previous scene file. Trust them over memory and over earlier chats; app memory is ignored.

WHICH APP YOU ARE IN
First try to run Python. If you can and 07 Tools.zip is in this project or attached, unzip it: its folder breaking-down-stories is the skill's folder. Run every tool as python breaking-down-stories/tools/stage.py <command> and follow the code loop in 01 House rules. Otherwise you are in a chat without code: follow the loop below.

EVERY UNIT (one piece of work that fits one reply)
1. Quote the step file's one-line task back as your first line, before any work.
2. Read the attached files: the story, 00 Start here, 02 Whole-film summary, 10 Film rules, 08 Places and things when the place has a floor plan, the previous scene file.
3. Write the whole file in one copy box with "Save as: <file name>" above it: the plain part for the user, the divider line "Below this line: details for the AI and the checker. You never need to read them.", the records, a --- line, the checks-in-words table, then the END line: END OF FILE | <what the file holds> | <n> records
4. Never shorten: no "...", "etc." or "same as above" inside a record, and never split a record across replies. When writing shots without code, 12 shots a reply.
5. Line references are quote anchors: a short exact quotation from the story. Quote the story word for word, never fix it, and label every addition invented.
6. Run the checks of 05 Checks in words, part 1, and print one line: "Checked in words: 14 of 14 passed", or only the failures. Fix a failing box before the user saves it.
7. End with the report.

THE REPORT, AT THE END OF EVERY REPLY
Done: <what, with progress, like "scene 11 of 30, step 9 of 12">
Example from your story: <one concrete line>
Made: <files>
Needs you: nothing, or one question with its default in [square brackets]
Next: <one step>
Without code, two more lines:
Save as: <file names> (save only boxes that end with the END line)
To continue later: new chat in this project; attach <the files>; type: Continue my breakdown.
Without code, after a group of scenes Next is a check: a new chat with that group's files, the story, 02 Whole-film summary, 10 Film rules, 05 Checks in words and the last health check file; type: Check my group of scenes. Never judge your own work in the reply that wrote it. Before acceptance, the user takes the folder to the Claude website (the free plan is enough) and types: Check my breakdown.
With code, at every stop make the save file (stage.py pack) and tell the user: "Download it now: the link expires."

HOW TO TALK
- Plain words, one word for each thing (the word list in 04); no abbreviations and no codes. Say "scene 10, shot 150", "group 3", "the big choices", "grey previews". Count steps from 1: "step 8 of 12".
- Start every report with an example from the user's story. Explain a new craft word once, in one sentence.
- Ask only about what the user wants and what is risky, costly or hard to undo. Every question has a default, and "defaults" accepts them all.
- Plan short, then expand: the one-line shot list fixes the shots and their count before any detail.
- Every shot has a purpose and a because. A choice that leaves the baseline (camera still, at the eye height of the person the scene belongs to, the normal lens, room sound) has a why that quotes a line, names an object or action, or cites a record. Never a reason that is only a mood.

SAVING, WITHOUT CODE
- The user keeps one folder, named like "The Catch - breakdown", with 11 Scenes inside. A reply that only adds records to a saved file saves them as "<file> - <what they hold>.md" (09 Continuity - scenes 06-10.md), each with its own END line. A reply that changes a saved record gives the whole file again and names the older files to delete.
- After every answer to a question and at every stop, save 00 Start here again, whole.
- If the user types continue, send again from the start of the record that was cut, or only the missing records, then the END line. If you cannot read an attached file to its end, ask the user to paste the missing part.

PRIVACY AND RIGHTS
- Before an unpublished story is uploaded, the user turns model training off in this app. Record their answer; never assume it.
- No personal information in any file: no email addresses, no account details.
- If the story is not theirs and they have no permission, plan it for private study only: every file says "Private study, not for publication".

The first message is "Break down my story." with the story attached (in Gemini, with 08 Steps 00-02 too). The resume message is "Continue my breakdown."
"""


# ---------------------------------------------------------------- small helpers

def english_words(text):
    """The number of English words: whitespace-separated tokens holding a letter or a digit (the count the step
    and card builders used)."""
    return len([token for token in text.split() if re.search(r"[A-Za-z0-9]", token)])


def read_text(path):
    return Path(path).read_text(encoding="utf-8")


def write_text(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".part")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def without_front_matter(text):
    """SKILL.md's body: everything after the front matter between the two --- lines."""
    if text.startswith("---"):
        parts = text.split("\n---", 1)
        if len(parts) == 2:
            return parts[1].split("\n", 1)[1].lstrip("\n") if "\n" in parts[1] else ""
    return text


def numbered_files(folder, numbers):
    """The files of a folder whose names start with each two-digit number, in the order given."""
    found = []
    for number in numbers:
        matches = sorted(path for path in Path(folder).glob(f"{number} *.md") if path.is_file())
        if not matches:
            raise StageStop(f'The skill has no file starting "{number} " in {Path(folder).name}/. '
                            "Restore it, then run build-kit again.")
        found.append(matches[0])
    return found


def repository_of(skill_folder, explicit=None):
    """The Stage repository: --repository, else the folder that holds .claude/skills/<the skill>."""
    if explicit:
        folder = Path(explicit).expanduser().resolve()
        if not folder.is_dir():
            raise StageStop(f'The folder "{explicit}" does not exist. Give the Stage repository with --repository.')
        return folder
    skill_folder = Path(skill_folder).resolve()
    if skill_folder.parent.name == "skills" and skill_folder.parent.parent.name == ".claude":
        return skill_folder.parent.parent.parent
    raise StageStop("This copy of the skill is not inside a Stage repository (.claude/skills/" + SKILL_NAME + "/). "
                    "Give the repository with --repository \"<folder>\".")


def skill_relative(path, skill_folder):
    return Path(path).resolve().relative_to(Path(skill_folder).resolve()).as_posix()


def kept_in_zip(relative):
    """Whether a file of the skill belongs in a ZIP at all (no caches, no half-written files, no proposals)."""
    parts = relative.split("/")
    if any(part in LEAVE_OUT_NAMES or part.startswith(".") for part in parts):
        return False
    return not relative.endswith(LEAVE_OUT_ENDINGS)


def library_file_kept(relative):
    """The library in a ZIP: its digests, its D research files and its three notes (00, 01, 02); the long A, B and C
    research files stay out (blueprint 2.3: 'library limited to digests and D files to keep it small')."""
    parts = relative.split("/")
    if parts[0] != "library":
        return True
    if len(parts) >= 3 and parts[1] == "digests":
        return True
    if len(parts) == 2:
        return bool(re.match(r"^(D\d+ |0\d )", parts[1]))
    return False


def write_zip(zip_path, entries):
    """A ZIP of [(name inside the ZIP, source path)], in the given order, every entry with ZIP_DATE."""
    zip_path = Path(zip_path)
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = zip_path.with_name(zip_path.name + ".part")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, source in entries:
            info = zipfile.ZipInfo(name, date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o644 & 0xFFFF) << 16
            archive.writestr(info, Path(source).read_bytes())
    os.replace(temporary, zip_path)


def skill_files(skill_folder):
    """Every file of the skill folder that may go into a ZIP, as sorted paths relative to the skill folder."""
    skill_folder = Path(skill_folder)
    found = []
    for path in skill_folder.rglob("*"):
        if path.is_file():
            relative = path.relative_to(skill_folder).as_posix()
            if kept_in_zip(relative):
                found.append(relative)
    return sorted(found)


# ---------------------------------------------------------------- reference/03 Field guide.md

def table_cell(text):
    text = " ".join(str(text).split())
    return text.replace("|", "\\|")


def depth_words(depth):
    return {"q": "quick", "s": "standard", "f": "detailed", "m": "add-on", "o": "optional"}.get(depth, depth or "")


def step_words(step):
    step = str(step)
    if step.isdigit():
        return f"step {step}"
    if step.startswith("add_on_"):
        return {"add_on_A": "add-on A (storyboards)", "add_on_B": "add-on B (grey previews)",
                "add_on_C": "add-on C (prompts for AI video)", "add_on_D": "add-on D (edit and finishing)"}.get(step, step)
    if step == "acceptance":
        return "the finished check (step 10)"
    return f"checkpoint {step}"


def writer_words(field):
    if field.get("writer_when"):
        parts = [f"{rule.get('writer')} (when {rule.get('when')})" for rule in field["writer_when"]]
        words = "; ".join(parts)
    else:
        words = field.get("writer", "")
    if field.get("chat_writer"):
        words += f"; in a chat without code: {field['chat_writer']}"
    return words


def values_words(field):
    """Allowed values, sub-parts and the other limits of a field, in one cell."""
    pieces = []
    kind = field.get("kind", "")
    if field.get("values"):
        pieces.append(", ".join(str(value) for value in field["values"]))
    if field.get("range"):
        low, high = (field["range"] + [None, None])[:2]
        pieces.append(f"from {low} to {high}")
    if field.get("pattern"):
        pieces.append(f"pattern `{field['pattern']}`")
    if field.get("id_types"):
        pieces.append("IDs of " + ", ".join(field["id_types"]))
    first_part = field.get("first_part")
    if first_part:
        first = f"first part: {first_part.get('kind', '')}"
        if first_part.get("values"):
            first += " (" + ", ".join(str(value) for value in first_part["values"]) + ")"
        elif first_part.get("id_types"):
            first += " (" + ", ".join(first_part["id_types"]) + ")"
        pieces.append(first)
    for part in field.get("sub_parts") or []:
        entry = f"{part.get('key')}: {part.get('kind', '')}"
        if part.get("values"):
            entry += " (" + ", ".join(str(value) for value in part["values"]) + ")"
        pieces.append(entry)
    if field.get("also_allowed"):
        pieces.append("also " + ", ".join(str(value) for value in field["also_allowed"]))
    if field.get("default") is not None:
        pieces.append(f"default {field['default']}")
    if field.get("repeat"):
        pieces.append("one line each")
    if not pieces:
        pieces.append(kind)
    elif kind and kind not in ("word",):
        pieces.insert(0, kind)
    return "; ".join(pieces)


def field_row(field):
    depth = depth_words(field.get("depth"))
    if field.get("module"):
        depth += f" ({field['module']})"
    if field.get("stored") is False:
        depth += ", worked out by code"
    example = field.get("example", "")
    example_cell = f"`{table_cell(example)}`" if example not in ("", None) else ""
    return (f"| `{field.get('name')}` | {table_cell(field.get('meaning', ''))} | {table_cell(values_words(field))} "
            f"| {depth} | {table_cell(writer_words(field))} | {step_words(field.get('filled_by_step'))} "
            f"| {example_cell} |")


def field_guide_text(schema_data):
    """reference/03 Field guide.md, made from schema.json."""
    record_types = schema_data["record_types"]
    shot = record_types.get("SHOT", {})
    size = next((field for field in shot.get("fields", []) if field.get("name") == "size"), None)
    lines = [
        "# Field guide",
        "",
        "Every record type and every field of `schema/schema.json`, in plain words. This file is made by "
        "`stage.py build-kit` from the schema (version "
        f"{schema_data.get('schema_version', '')}); edit the schema, never this file. Record grammar: "
        "`reference/01 Record format.md`. Words: `reference/02 Word list.md`.",
        "",
    ]
    if size:
        lines += [
            "Example first. The SHOT field `size` reads, in the table for SHOT:",
            "",
            "| Field | Meaning | Values | Depth | Writer | Filled at | Example |",
            "|---|---|---|---|---|---|---|",
            field_row(size),
            "",
            "So a shot record carries the line `- size: close_up`: the AI writes it at step 8 (the user's step 9 of 12), "
            "from quick depth, choosing one of the eight sizes.",
            "",
        ]
    lines += [
        "## How to read the tables",
        "",
        "- **Depth**: " + "; ".join(f"{depth_words(letter)} ({letter}): {text.rstrip('.')}"
                                     for letter, text in schema_data.get("depths", {}).items()) + ".",
        "- **Writer**: " + "; ".join(f"`{name}`: {text.rstrip('.')}"
                                      for name, text in schema_data.get("writers", {}).items()) + ".",
        "- **Filled at**: the step that fills the field, counted from 0 as in the step files (step 8 is the user's "
        "step 9 of 12); a letter is a checkpoint; add-ons come after step 11.",
        "- **Values**: the kind first when it is not a single word, then the allowed values, the sub-parts "
        "(`key: kind (values)`), other values allowed, the default, and \"one line each\" for a field written once "
        "per item. Syntax of every kind is in the table below.",
        "",
        "## Kinds of value",
        "",
        "| Kind | Syntax | Example |",
        "|---|---|---|",
    ]
    for name, kind in schema_data.get("kinds", {}).items():
        lines.append(f"| `{name}` | {table_cell(kind.get('syntax', ''))} | `{table_cell(kind.get('example', ''))}` |")
    common = schema_data.get("common_fields", {})
    lines += ["", "## Fields every record takes", "", table_cell(common.get("about", "")), "",
              "| Field | Meaning | Values | Depth | Writer | Filled at | Example |", "|---|---|---|---|---|---|---|"]
    lines += [field_row(field) for field in common.get("fields", [])]
    for type_name, record_type in record_types.items():
        files = ", ".join(record_type.get("files", []))
        lines += [
            "",
            f"## {type_name}: {record_type.get('plain_name', '')}",
            "",
            f"{record_type.get('meaning', '')} ID: {record_type.get('id_syntax', '')} (`{record_type.get('id_example', '')}`); "
            f"the user sees it as {record_type.get('shown_to_user_as', '')}. Lives in: {files}. "
            f"Designed at {step_words(record_type.get('designed_by_step'))}; needed from "
            f"{depth_words(record_type.get('depth'))} depth.",
            "",
            "| Field | Meaning | Values | Depth | Writer | Filled at | Example |",
            "|---|---|---|---|---|---|---|",
        ]
        lines += [field_row(field) for field in record_type.get("fields", [])]
        if record_type.get("status_values"):
            lines += ["", "Status values: " + ", ".join(record_type["status_values"]) + "."]
    conditions = schema_data.get("conditions", {})
    if conditions:
        lines += ["", "## Conditions", "", "The names used in \"when\" above.", "", "| Condition | Meaning |", "|---|---|"]
        lines += [f"| `{name}` | {table_cell(text)} |" for name, text in conditions.items()]
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------- AGENTS.md

EXPLICIT_PREFIXES = ("steps/", "cards/", "reference/", "schema/", "rules/", "adapters/", "templates/", "examples/",
                     "tools/", "library/")


def with_explicit_paths(text):
    """SKILL.md's text with every skill path written out from the repository's top folder."""
    skill_path = f".claude/skills/{SKILL_NAME}/"
    text = text.replace("<this skill's folder>/", skill_path)

    def explicit(match):
        inner = match.group(1)
        if inner.startswith(EXPLICIT_PREFIXES):
            return f"`{skill_path}{inner}`"
        if inner.startswith("python tools/"):
            return f"`python {skill_path}{inner[len('python '):]}`"
        return match.group(0)

    return re.sub(r"`([^`\n]+)`", explicit, text)


def agents_text(skill_folder):
    body = without_front_matter(read_text(Path(skill_folder) / "SKILL.md"))
    body = with_explicit_paths(body)
    # The body's own title becomes a second-level heading under this file's title.
    body = re.sub(r"^# ", "## ", body, count=1, flags=re.MULTILINE)
    header = [
        "# AGENTS.md: the Stage story-breakdown kit",
        "",
        "This folder is a story-breakdown kit. It turns a story (a screenplay, a novel, a short story, a play) into a "
        "scene-by-scene plan for making it as a film, including with AI picture and video tools. Follow the rules "
        f"below, which are the skill `{SKILL_NAME}` with every path written out from this folder.",
        "",
        "- Stories are in `My stories/`; projects are made in `My breakdowns/`.",
        f"- Run every tool as `python .claude/skills/{SKILL_NAME}/tools/stage.py <command>`.",
        "- Never edit the files in a project's `For machines - do not edit/` folder, and never edit files code makes "
        "(`breakdown.json`, the book, spreadsheets, prompts): change the records and build again.",
        "- Privacy: no personal information in any file, prompt or web request; never commit a user's story; never "
        "paste a story into a web request.",
        "",
        f"This file is made by `stage.py build-kit` from `.claude/skills/{SKILL_NAME}/SKILL.md`: edit that file, then "
        "build again.",
        "",
    ]
    return "\n".join(header) + "\n" + body.rstrip("\n") + "\n"


# ---------------------------------------------------------------- the chat kit

def kit_map_table():
    """Where each skill file is in the chat kit, for the joined files' headers."""
    return "\n".join([
        "| The skill's file | In this chat kit |",
        "|---|---|",
        "| `SKILL.md`, `reference/07 Report and message formats.md` | 01 House rules (this file) |",
        "| `cards/01` to `07`, `15` to `20` | 02 Cards - story and scenes |",
        "| `cards/08` to `14`, `21` to `24` | 03 Cards - picture, sound and making |",
        "| `templates/`, `reference/01 Record format.md`, `02 Word list.md`, `04 Rule order.md` | "
        "04 Templates and word list |",
        "| `reference/05 Quality rubric.md`, `reference/06 Checks in words.md` | 05 Checks in words |",
        "| `examples/01 The Catch - scene 10.md` | 06 Example - The Catch, scene 10 (an excerpt; the whole file is in "
        "07 Tools.zip) |",
        "| `tools/`, `schema/`, `rules/`, `adapters/`, `reference/03 Field guide.md`, library digests | "
        "07 Tools.zip (ChatGPT only; unzip it and its folder breaking-down-stories is the skill's folder) |",
        "| `steps/00` to `02` | 08 Steps 00-02 - start, reading, plan |",
        "| `steps/03` to `06` | 09 Steps 03-06 - world, people, continuity, film rules |",
        "| `steps/07`, `08` | 10 Steps 07-08 - scenes and shots |",
        "| `steps/09`, `10`, `11`, `16` | 11 Steps 09-11 and 16 - film pass, check, book, resume |",
        "| `steps/12`, `14`, `15` | 12 Steps for add-ons - storyboards, prompts, finishing (step 13, grey previews, "
        "needs Claude Code on the user's computer and is not in the chat kit) |",
    ])


def joined_file(title, lead, parts, skill_folder):
    """One knowledge or step-group file: a short header, then each skill file whole, each introduced by the line
    naming where it comes from. parts: [(path, text)] or [(path, text, True)]; True wraps that part in a ~~~~ block
    (a template, to be copied as it is)."""
    lines = [f"# {title}", "", lead, ""]
    for part in parts:
        path, text = part[0], part[1]
        fence = len(part) > 2 and part[2]
        relative = skill_relative(path, skill_folder)
        lines += ["---", "", f"From the skill file `{relative}`:", ""]
        if fence:
            lines += ["~~~~markdown", text.rstrip("\n"), "~~~~", ""]
        else:
            lines += [text.rstrip("\n"), ""]
    return "\n".join(lines).rstrip("\n") + "\n"


def house_rules_text(skill_folder):
    skill_folder = Path(skill_folder)
    lead = ("Part of the Stage chat kit, for a ChatGPT Project or a Gemini Gem. It joins the skill's house rules "
            "(`SKILL.md`, without its front matter) and `reference/07 Report and message formats.md`. Where they "
            "name another skill file, it is in this kit here:\n\n" + kit_map_table() +
            "\n\nOn ChatGPT with 07 Tools.zip unzipped you are on a code surface: the paths below are inside the "
            "folder breaking-down-stories. In a chat without code, the step file attached to the chat says what to do.")
    parts = [(skill_folder / "SKILL.md", without_front_matter(read_text(skill_folder / "SKILL.md"))),
             (skill_folder / "reference/07 Report and message formats.md",
              read_text(skill_folder / "reference/07 Report and message formats.md"))]
    return joined_file("01 House rules", lead, parts, skill_folder)


def cards_text(file_name, numbers, skill_folder):
    skill_folder = Path(skill_folder)
    paths = numbered_files(skill_folder / "cards", numbers)
    listing = ", ".join(path.stem for path in paths)
    lead = (f"Part of the Stage chat kit (knowledge). It joins these craft cards, each whole: {listing}. A step file "
            "names the card parts to read for each unit; read only those parts. 01 House rules says where every "
            "other skill file is in this kit.")
    return joined_file(Path(file_name).stem, lead, [(path, read_text(path)) for path in paths], skill_folder)


def templates_text(skill_folder):
    skill_folder = Path(skill_folder)
    templates = sorted(path for path in (skill_folder / "templates").glob("*.md") if path.is_file())
    references = [skill_folder / "reference" / name for name in
                  ("01 Record format.md", "02 Word list.md", "04 Rule order.md")]
    for path in references:
        if not path.is_file():
            raise StageStop(f"The skill has no {skill_relative(path, skill_folder)}. Restore it, then run build-kit again.")
    listing = ", ".join(path.stem for path in templates)
    lead = ("Part of the Stage chat kit (knowledge). It holds every empty record file of the skill (" + listing +
            "), each between two ~~~~ lines to copy as it is, then the record format, the word list and the rule "
            "order. Fill a template's angle brackets; the note block after each record lists the allowed values, "
            "and you need not copy it. 01 House rules says where every other skill file is in this kit.")
    parts = [(path, read_text(path), True) for path in templates] + [(path, read_text(path)) for path in references]
    return joined_file("04 Templates and word list", lead, parts, skill_folder)


def checks_text(skill_folder):
    skill_folder = Path(skill_folder)
    paths = [skill_folder / "reference/06 Checks in words.md", skill_folder / "reference/05 Quality rubric.md"]
    lead = ("Part of the Stage chat kit: knowledge, and attached to every check chat. It joins "
            "`reference/06 Checks in words.md` (part 1: the checks every reply runs on its own file; part 2: the "
            "checks a separate check chat runs on a group of scenes; part 3: the real check on the Claude website) and "
            "`reference/05 Quality rubric.md` (the ten criteria the finished check scores).")
    return joined_file("05 Checks in words", lead, [(path, read_text(path)) for path in paths], skill_folder)


def split_records(text):
    """(the text above the first record, [(ID, record text)], the END line) of a record file."""
    body, _, end = text.rstrip("\n").rpartition("\nEND OF FILE")
    end = "END OF FILE" + end if _ else ""
    if not _:
        body = text
    pieces = re.split(r"(?m)^(?=### )", body)
    head = pieces[0]
    records = []
    for piece in pieces[1:]:
        heading = piece.split("\n", 1)[0]
        words = heading.split()
        identifier = words[2] if len(words) > 2 else (words[1] if len(words) > 1 else "")
        records.append((identifier, piece))
    return head, records, end


def example_excerpt_text(skill_folder):
    """06 Example: the gold scene's plain part whole and the records of EXAMPLE_EXCERPT_RECORDS, with a counted END
    line of its own."""
    skill_folder = Path(skill_folder)
    gold_path = skill_folder / GOLD_SCENE
    text = read_text(gold_path)
    head, records, end = split_records(text)
    by_id = {identifier: piece for identifier, piece in records}
    missing = [identifier for identifier in EXAMPLE_EXCERPT_RECORDS if identifier not in by_id]
    if missing:
        raise StageStop("The gold scene no longer holds " + ", ".join(missing) + ". Update EXAMPLE_EXCERPT_RECORDS in "
                        "build_kit.py, then run build-kit again.")
    kept = [identifier for identifier, _ in records if identifier in EXAMPLE_EXCERPT_RECORDS]
    left_out = [identifier for identifier, _ in records if identifier not in EXAMPLE_EXCERPT_RECORDS]
    shots_left = [identifier.split("-SH")[1] for identifier in left_out if "-SH" in identifier]
    what = re.search(r"END OF FILE \| (.+?) \|", end)
    what = what.group(1) if what else "Scene 10"
    lead = [
        "# 06 Example - The Catch, scene 10",
        "",
        "Part of the Stage chat kit (knowledge). This is the finished example of a scene file: scene 10 of The Catch, "
        "Saye's kitchen, at standard depth. It is an excerpt: the plain part is whole, and below the divider it keeps "
        f"{len(kept)} of the file's {len(records)} records: the scene's design, its two parts, the beats of its two "
        "turns and a few around them, two floor-plan moves, three camera setups, the one-line shot list, and six "
        "shots of different kinds with the cut to black and the title card. The shots left out (shots "
        + ", ".join(shots_left) + ") follow the same form. A real scene file holds "
        "every beat and every shot, and its END line counts them all; the END line below counts this excerpt. The "
        "whole file is `examples/01 The Catch - scene 10.md` in 07 Tools.zip (and in the Stage folder's "
        "\"09 Example - The Catch, scene 10\"), and the whole-film records it cites (characters, places, "
        "continuity, film rules) are in `examples/02` there.",
        "",
        "",
    ]
    kept_text = "".join(by_id[identifier] if by_id[identifier].endswith("\n") else by_id[identifier] + "\n"
                        for identifier in kept)
    end_line = f"END OF FILE | {what}, excerpt | {len(kept)} records"
    return "\n".join(lead) + head + kept_text.rstrip("\n") + "\n\n" + end_line + "\n"


def steps_text(file_name, numbers, skill_folder):
    skill_folder = Path(skill_folder)
    paths = numbered_files(skill_folder / "steps", numbers)
    listing = ", ".join(path.stem for path in paths)
    lead = (f"Part of the Stage chat kit: a step-group file, attached to the chat that runs one of these steps "
            f"(not knowledge). It joins the step files {listing}, each whole. Read the one for this unit every time, "
            "quote its one-line task back before any work, and follow its section \"If you cannot run code\" when "
            "this chat has no code. 01 House rules (in the knowledge) says where every other skill file is.")
    return joined_file(Path(file_name).stem, lead, [(path, read_text(path)) for path in paths], skill_folder)


def tools_zip_entries(skill_folder):
    """07 Tools.zip (blueprint 2.5): stage.py and stage_tools plus schema, rules, adapters, steps, cards, templates,
    examples and the library digests, so every command runs in ChatGPT's sandbox. SKILL.md, reference/ (the handouts
    read it) and the library's three notes (lib prints the errata) go in too. The previs scripts stay out: grey
    previews need Claude Code and Blender."""
    entries = []
    for relative in skill_files(skill_folder):
        top = relative.split("/")[0]
        if relative == "SKILL.md" or top in ("schema", "rules", "adapters", "steps", "cards", "templates", "examples",
                                             "reference"):
            pass
        elif relative == "tools/stage.py" or relative.startswith("tools/stage_tools/"):
            pass
        elif top == "library" and library_file_kept(relative) and not re.match(r"^library/D\d+ ", relative):
            pass  # digests and the three notes; the D research files stay in the skill ZIP only
        else:
            continue
        entries.append((f"{SKILL_NAME}/{relative}", Path(skill_folder) / relative))
    return entries


def skill_zip_entries(skill_folder):
    """08 Skill for Claude apps.zip: the whole skill folder under breaking-down-stories/, library cut down."""
    return [(f"{SKILL_NAME}/{relative}", Path(skill_folder) / relative)
            for relative in skill_files(skill_folder) if library_file_kept(relative)]


def check_zip_layout(zip_path, must_hold):
    """Problems with a ZIP: every entry under breaking-down-stories/, and the named entries present."""
    problems = []
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
    outside = [name for name in names if not name.startswith(f"{SKILL_NAME}/")]
    if outside:
        problems.append(f"{Path(zip_path).name} holds {len(outside)} files outside {SKILL_NAME}/ (first: {outside[0]}).")
    for name in must_hold:
        if name not in names:
            problems.append(f"{Path(zip_path).name} has no {name}.")
    return problems, names


# ---------------------------------------------------------------- 09 Example - The Catch, scene 10

def gold_project(folder, skill_folder):
    """A project folder from the gold: each '## From <file>' part of the context file as its numbered file (a
    one-line title above the divider, as apply makes new files) and the scene file in 11 Scenes."""
    skill_folder = Path(skill_folder)
    folder = Path(folder)
    (folder / MACHINE_FOLDER).mkdir(parents=True)
    context = read_text(skill_folder / GOLD_CONTEXT)
    if DIVIDER_LINE not in context:
        raise StageStop(f"{GOLD_CONTEXT} has no divider line. Restore it, then run build-kit again.")
    context = context.split(DIVIDER_LINE, 1)[1]
    sections = re.split(r"^## From (.+)$", context, flags=re.MULTILINE)[1:]
    for name, body in zip(sections[0::2], sections[1::2]):
        name = name.strip()
        body = re.sub(r"\n+END OF FILE .*$", "", body.strip(), flags=re.DOTALL)
        count = len(re.findall(r"^### ", body, re.MULTILINE))
        write_text(folder / f"{name}.md",
                   f"# {name}\n\n{DIVIDER_LINE}\n\n{body}\n\nEND OF FILE | {name} | {count} records\n")
    scene_text = read_text(skill_folder / GOLD_SCENE)
    title = scene_text.split("\n", 1)[0].lstrip("# ").strip()
    write_text(folder / "11 Scenes" / f"{title}.md", scene_text)
    return folder, f"11 Scenes/{title}.md"


def run_stage(arguments, project, stage_script):
    """Run one stage.py command on the example project; (exit code, output lines)."""
    completed = subprocess.run([sys.executable, str(stage_script)] + arguments + ["--project", str(project)],
                               capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    return completed.returncode, (completed.stdout + completed.stderr).splitlines()


def leaks_in(text, name, local_paths):
    """Problem lines when a file build-kit copies out holds a local folder path or an email address."""
    problems = []
    for local in local_paths + ["/tmp/"]:
        if local and len(local) > 1 and local in text:
            problems.append(f"{name} holds the local path {local!r}; files handed out must hold no local path.")
    if EMAIL.search(text):
        problems.append(f"{name} holds an email address; files handed out must hold none.")
    return problems


def build_example(repository, skill_folder, story=None, say=print):
    """09 Example - The Catch, scene 10/: files 00, 01, 04, 07, 08, 09, 10 with the plain parts code writes, the
    gold scene file as it is, and the book made from them. Returns problem lines."""
    problems = []
    skill_folder = Path(skill_folder)
    stage_script = skill_folder / "tools" / "stage.py"
    target = Path(repository) / EXAMPLE_FOLDER
    with tempfile.TemporaryDirectory(prefix="stage-example-") as temporary:
        project, scene_name = gold_project(Path(temporary) / "The Catch", skill_folder)
        record = Project(project)
        # next works only from the units applied (fix list C3): the units the gold's records hold are listed as adopt
        # lists them, so the example's next step is the film pass; its last saved unit stays the last batch
        from .make_handout import record_units_found
        record_units_found(project)
        manifest = record.read_manifest()
        manifest["units_done"] = [entry for entry in manifest.get("units_done", [])
                                  if entry.get("unit") != EXAMPLE_LAST_UNIT]
        manifest["units_done"].append({"unit": EXAMPLE_LAST_UNIT, "applied": today()})
        record.write_manifest(manifest)
        code, lines = run_stage(["build"], project, stage_script)
        if code != 0:
            return [f"The example's build stopped with exit {code}: " + (lines[-1] if lines else "no output")]
        record.add_log_entry("Scene 10 designed and its shots written: 11 beats, 20 shots and the title card; "
                             "one added detail to keep or cut (Iona sets the lamp down).")
        check = ["check", "--all"] + (["--story", str(story)] if story else [])
        code, lines = run_stage(check, project, stage_script)  # check writes its own log entry
        errors = [line for line in lines if line.startswith("E ")]
        warnings = [line for line in lines if line.startswith("W ")]
        if code == 2:
            return ["The example's check could not run: " + (lines[-1] if lines else "no output")]
        in_short = next((line for line in lines if line.startswith("In short:")), f"{len(errors)} errors, "
                        f"{len(warnings)} warnings")
        code, lines = run_stage(["export", "book"], project, stage_script)
        if code != 0:
            return [f"The example's book stopped with exit {code}: " + (lines[-1] if lines else "no output")]
        record.add_log_entry("The book made: 15 The breakdown.")
        for name in EXAMPLE_FILES + EXAMPLE_BOOK_FILES:
            if not (project / name).is_file():
                problems.append(f"The example project has no {name} after build and export.")
        if problems:
            return problems
        if target.exists():
            if not (target / "00 Start here.md").is_file() and any(target.iterdir()):
                return [f'"{EXAMPLE_FOLDER}" holds files build-kit did not make; move them, then build again.']
            shutil.rmtree(target)
        for name in EXAMPLE_FILES + EXAMPLE_BOOK_FILES:
            destination = target / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(project / name, destination)
        # The scene file keeps the gold's own plain part, written by hand as the model for every scene page.
        destination = target / scene_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(skill_folder / GOLD_SCENE, destination)
        temporary_path = str(Path(temporary).resolve())
    for path in sorted(target.rglob("*")):
        if path.is_file():
            problems += leaks_in(path.read_text(encoding="utf-8", errors="replace"), path.relative_to(target),
                                 [temporary_path, str(Path.home()), str(Path(repository).resolve())])
    say(f"Example: {EXAMPLE_FOLDER}/ with {sum(1 for path in target.rglob('*') if path.is_file())} files "
        f"(the checker: {in_short.replace('In short:', '').strip().rstrip('.')}).")
    return problems


# ---------------------------------------------------------------- the whole build

def build_chat_kit(repository, skill_folder, say=print):
    """07 Chat kit/ with exactly the 13 files of blueprint 2.5. Returns (problem lines, size notes, sizes)."""
    skill_folder = Path(skill_folder)
    kit = Path(repository) / CHAT_KIT_FOLDER
    kit.mkdir(parents=True, exist_ok=True)
    problems, notes, sizes = [], [], {}
    limits = json.loads(read_text(skill_folder / "rules" / "limits.json")).get("chat_kit", {})
    characters_max = int(limits.get("instructions_characters_max", 6000))
    texts = {
        INSTRUCTIONS_NAME: INSTRUCTIONS_TEXT,
        "01 House rules.md": house_rules_text(skill_folder),
        "04 Templates and word list.md": templates_text(skill_folder),
        "05 Checks in words.md": checks_text(skill_folder),
        "06 Example - The Catch, scene 10.md": example_excerpt_text(skill_folder),
    }
    for name, numbers in CARD_GROUPS.items():
        texts[name] = cards_text(name, numbers, skill_folder)
    for name, numbers in STEP_GROUPS.items():
        texts[name] = steps_text(name, numbers, skill_folder)
    for name, text in texts.items():
        write_text(kit / name, text)
    tools_zip = kit / TOOLS_ZIP_NAME
    write_zip(tools_zip, tools_zip_entries(skill_folder))
    zip_problems, names = check_zip_layout(tools_zip, [f"{SKILL_NAME}/tools/stage.py", f"{SKILL_NAME}/schema/schema.json",
                                                       f"{SKILL_NAME}/steps/00 Start.md"])
    problems += zip_problems
    wanted = [name for name, _, _, _ in KIT_FILES]
    for path in sorted(kit.iterdir()):
        if path.name not in wanted:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            notes.append(f"Removed {path.name} from {CHAT_KIT_FOLDER}: it is not one of the 13 files.")
    characters = len(INSTRUCTIONS_TEXT)
    sizes[INSTRUCTIONS_NAME] = characters
    if characters > characters_max:
        problems.append(f"{INSTRUCTIONS_NAME} has {characters:,} characters, over {characters_max:,}. Shorten "
                        "INSTRUCTIONS_TEXT in build_kit.py.")
    knowledge_total = 0
    for name, kind, target, _ in KIT_FILES:
        if kind in ("knowledge", "steps"):
            words = english_words(read_text(kit / name))
            sizes[name] = words
            if kind == "knowledge":
                knowledge_total += words
            if target and abs(words - target) > SIZE_TOLERANCE * target:
                notes.append(f"{name}: {words:,} words, target about {target:,} "
                             f"({(words - target) / target:+.0%}).")
    sizes["knowledge total"] = knowledge_total
    if abs(knowledge_total - KNOWLEDGE_TOTAL_ABOUT) > SIZE_TOLERANCE * KNOWLEDGE_TOTAL_ABOUT:
        notes.append(f"The six knowledge files: {knowledge_total:,} words, target about {KNOWLEDGE_TOTAL_ABOUT:,}.")
    sizes[TOOLS_ZIP_NAME] = tools_zip.stat().st_size
    say(f"Chat kit: {CHAT_KIT_FOLDER}/ with {len(list(kit.iterdir()))} files; {INSTRUCTIONS_NAME} {characters:,} "
        f"characters; the six knowledge files {knowledge_total:,} words; {TOOLS_ZIP_NAME} {len(names)} files, "
        f"{sizes[TOOLS_ZIP_NAME] // 1024:,} KB.")
    return problems, notes, sizes


def build_all(repository, skill_folder, story=None, with_example=True, say=print):
    """Every output of build-kit. Returns (problem lines, notes)."""
    skill_folder = Path(skill_folder)
    repository = Path(repository)
    problems, notes = [], []
    schema_data = json.loads(read_text(skill_folder / "schema" / "schema.json"))
    write_text(skill_folder / FIELD_GUIDE, field_guide_text(schema_data))
    say(f"Field guide: {FIELD_GUIDE} ({english_words(read_text(skill_folder / FIELD_GUIDE)):,} words, "
        f"{len(schema_data['record_types'])} record types).")
    write_text(repository / AGENTS_FILE, agents_text(skill_folder))
    say(f"{AGENTS_FILE}: SKILL.md's rules with every path written out.")
    kit_problems, kit_notes, _ = build_chat_kit(repository, skill_folder, say)
    problems += kit_problems
    notes += kit_notes
    skill_zip = repository / SKILL_ZIP_NAME
    write_zip(skill_zip, skill_zip_entries(skill_folder))
    zip_problems, names = check_zip_layout(skill_zip, [f"{SKILL_NAME}/SKILL.md"])
    problems += zip_problems
    say(f"Skill ZIP: {SKILL_ZIP_NAME} with {len(names)} files, {skill_zip.stat().st_size // 1024:,} KB, "
        f"{SKILL_NAME}/SKILL.md at its top folder.")
    if with_example:
        problems += build_example(repository, skill_folder, story, say)
    return problems, notes


def add_build_kit_arguments(parser):
    parser.add_argument("--repository", help="the Stage repository (default: the folder that holds .claude/skills)")
    parser.add_argument("--story", help="the story file, or the story excerpt, for the example's check (default: "
                                        f"{STORY_EXCERPT} when it is there)")
    parser.add_argument("--skip-example", action="store_true", help=f'do not rebuild "{EXAMPLE_FOLDER}"')


def run_build_kit(context):
    arguments = context.arguments
    skill_folder = Path(getattr(context, "skill_folder", None) or SKILL_FOLDER)
    repository = repository_of(skill_folder, getattr(arguments, "repository", None))
    story = getattr(arguments, "story", None)
    if story:
        story = Path(story).expanduser().resolve()
        if not story.is_file():
            raise StageStop(f'The story file "{arguments.story}" was not found.')
    elif (repository / STORY_EXCERPT).is_file():
        story = repository / STORY_EXCERPT
    problems, notes = build_all(repository, skill_folder, story, not getattr(arguments, "skip_example", False),
                                context.say)
    for note in notes:
        context.say(f"N {note}")
    for problem in problems:
        context.say(f"E {problem}")
    context.summary = f"kit built, {len(problems)} problems, {len(notes)} notes"
    return 1 if problems else 0


def register_commands(table):
    table.add("build-kit", "Maintainers: build the chat kit, the skill ZIP, AGENTS.md, the field guide and the example",
              run_build_kit, add_build_kit_arguments, uses_project=False)
