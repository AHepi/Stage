"""The acceptance test of work package 13: the user documents and the kit (blueprint 14.2, row WP13; 2.1, 2.3, 2.5, 13).

What it proves, from the files as they are in the repository:
- 07 Chat kit holds exactly the 13 files of blueprint 2.5, "00 Paste into instructions.txt" has at most 6,000
  characters (rules/limits.json), and each knowledge and step-group file is within a quarter of its 2.5 target, with
  the six knowledge files together about 60,000 words (these sizes are reported with their real numbers);
- the chat kit, AGENTS.md and reference/03 Field guide.md are up to date: build-kit run again into a scratch folder
  gives the same bytes, ZIPs included;
- 07 Tools.zip holds the tools and the skill's steps, cards, templates, examples, reference, schema, rules, adapters
  and library digests under breaking-down-stories/, no caches and none of the long research files; unzipped in a
  scratch folder, its stage.py lists build-kit and runs new, read and a handout on a small story;
- 08 Skill for Claude apps.zip has breaking-down-stories/SKILL.md at its top folder, SKILL.md's front matter names
  the skill, and its library is cut to the digests, the D files and the three notes;
- AGENTS.md is SKILL.md's body with every skill path written out, and every path it names exists;
- the field guide names every record type and every field of schema/schema.json;
- 09 Example - The Catch, scene 10 holds exactly the files blueprint 2.3 names, its scene file is the gold's, the
  book is there, and nothing in it holds a local path or an email address; its plain parts and book pass the
  checker's own word rules;
- the guides (README.md, CLAUDE.md, 01 to 06) are within the lengths of 2.3, pass the checker's own word rules
  (WORDS-02 retired words, WORDS-04 abbreviations and codes, the functions check_records uses), and every kit file
  they name exists;
- no file this package writes holds an email address, and, given --story, none holds more than a tenth of the story.

Usage: python tests/wp13_kit_acceptance.py [--story "<The Catch, the whole story>"]
Without --story the story group says "skipped: story not present". Standard library only.
"""

import argparse
import json
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

from stage_tools.checks_craft_reasons_words import abbreviations_in_text, retired_words_in_text  # noqa: E402
from stage_tools.record_format import DIVIDER_LINE  # noqa: E402

WORDS = json.loads((SKILL / "rules" / "words.json").read_text(encoding="utf-8"))
LIMITS = json.loads((SKILL / "rules" / "limits.json").read_text(encoding="utf-8"))
KIT = REPOSITORY / "07 Chat kit"
SKILL_ZIP = REPOSITORY / "08 Skill for Claude apps.zip"
EXAMPLE = REPOSITORY / "09 Example - The Catch, scene 10"
FIELD_GUIDE = SKILL / "reference" / "03 Field guide.md"
AGENTS = REPOSITORY / "AGENTS.md"
TOP = "breaking-down-stories/"

# Blueprint 2.5, typed here from the blueprint so the test does not read the list it checks: name, target words.
KIT_2_5 = [
    ("00 Paste into instructions.txt", None), ("01 House rules.md", 5500),
    ("02 Cards - story and scenes.md", 16000), ("03 Cards - picture, sound and making.md", 18000),
    ("04 Templates and word list.md", 12000), ("05 Checks in words.md", 2500),
    ("06 Example - The Catch, scene 10.md", 6000), ("07 Tools.zip", None),
    ("08 Steps 00-02 - start, reading, plan.md", 5000),
    ("09 Steps 03-06 - world, people, continuity, film rules.md", 7000),
    ("10 Steps 07-08 - scenes and shots.md", 3600),
    ("11 Steps 09-11 and 16 - film pass, check, book, resume.md", 7000),
    ("12 Steps for add-ons - storyboards, prompts, finishing.md", 5000),
]
KNOWLEDGE = [name for name, _ in KIT_2_5[1:7]]
KNOWLEDGE_TOTAL_ABOUT = 60000
TOLERANCE = 0.25
# Blueprint 2.3: the guides and their lengths in English words.
GUIDES = {
    "README.md": (150, 250), "CLAUDE.md": (1, 299), "01 Read me first.md": (700, 1000),
    "02 Using Claude.md": (900, 1300), "03 Using ChatGPT.md": (700, 1000),
    "04 Using Gemini or another chat app.md": (800, 1100), "05 How to read your breakdown.md": (1000, 1400),
    "06 Word list.md": (1200, 1600),
}
USER_GUIDES = [name for name in GUIDES if name != "CLAUDE.md"]
# Blueprint 2.3: 09 Example holds only these, plus the book made from them.
EXAMPLE_2_3 = {"00 Start here.md", "01 Choices.md", "04 Scene list.md", "07 Characters and voices.md",
               "08 Places and things.md", "09 Continuity.md", "10 Film rules.md",
               "11 Scenes/Scene 10 - Saye's kitchen.md", "15 The breakdown/The breakdown.md",
               "15 The breakdown/The breakdown.html"}
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}")

RESULTS = []


def report(passed, group, detail=""):
    RESULTS.append(bool(passed))
    print(f"{'PASS' if passed else 'FAIL'}  {group}" + (f": {detail}" if detail else ""), flush=True)


def info(line):
    print(f"INFO  {line}", flush=True)


def english_words(text):
    return len([token for token in text.split() if re.search(r"[A-Za-z0-9]", token)])


def read(path):
    return Path(path).read_text(encoding="utf-8")


def run_stage(arguments, cwd=None):
    completed = subprocess.run([sys.executable, str(STAGE)] + arguments, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", cwd=cwd, timeout=900)
    return completed.returncode, completed.stdout + completed.stderr


def words_problems(text):
    """The checker's own word rules on a user-facing text: [(what, kind)]."""
    found = [(written, "retired word") for written, _ in retired_words_in_text(text, WORDS)]
    found += abbreviations_in_text(text, WORDS)
    return found


def group(title):
    def decorator(function):
        def run(*arguments):
            try:
                detail = function(*arguments)
            except AssertionError as error:
                report(False, title, str(error))
                return
            except Exception as error:  # a fault fails this group only
                report(False, title, f"{type(error).__name__}: {error}")
                return
            if detail == "skip":
                return
            report(True, title, detail or "")
        return run
    return decorator


# ---------------------------------------------------------------- the chat kit

@group("07 Chat kit holds exactly the 13 files of blueprint 2.5")
def kit_files():
    names = sorted(path.name for path in KIT.iterdir())
    wanted = sorted(name for name, _ in KIT_2_5)
    extra = sorted(set(names) - set(wanted))
    missing = sorted(set(wanted) - set(names))
    assert not extra and not missing, f"extra {extra}, missing {missing}"
    return f"{len(names)} files"


@group("00 Paste into instructions.txt has at most the Project instruction limit of characters")
def instructions_length():
    limit = LIMITS["chat_kit"]["instructions_characters_max"]
    characters = len(read(KIT / "00 Paste into instructions.txt"))
    assert characters <= limit, f"{characters:,} characters, over {limit:,}"
    text = read(KIT / "00 Paste into instructions.txt")
    for needed in ("one-line task", "END OF FILE", "Checked in words", "Break down my story.",
                   "Continue my breakdown.", "Below this line: details for the AI and the checker.", "12 shots",
                   "private study", "email"):
        assert needed.lower() in text.lower(), f"it does not say {needed!r}"
    return f"{characters:,} of {limit:,} characters; names the one-line task, the END line, the report, the batch size and privacy"


@group("knowledge and step-group files within a quarter of their 2.5 targets; the six knowledge files about 60,000 words")
def kit_sizes():
    lines, outside = [], []
    total = 0
    for name, target in KIT_2_5:
        if target is None:
            continue
        words = english_words(read(KIT / name))
        if name in KNOWLEDGE:
            total += words
        ratio = (words - target) / target
        lines.append(f"{name[:2]} {words:,} ({ratio:+.0%})")
        if abs(ratio) > TOLERANCE:
            outside.append(f"{name} {words:,} words, target about {target:,} ({ratio:+.0%})")
    total_ratio = (total - KNOWLEDGE_TOTAL_ABOUT) / KNOWLEDGE_TOTAL_ABOUT
    info("sizes: " + "; ".join(lines) + f"; six knowledge files {total:,} ({total_ratio:+.0%})")
    if abs(total_ratio) > TOLERANCE:
        outside.append(f"the six knowledge files {total:,} words, target about {KNOWLEDGE_TOTAL_ABOUT:,}")
    assert not outside, "; ".join(outside)
    return f"six knowledge files {total:,} words"


@group("the chat kit, the skill ZIP, AGENTS.md and the field guide are up to date: build-kit again gives the same bytes")
def kit_up_to_date():
    with tempfile.TemporaryDirectory(prefix="wp13-rebuild-") as scratch:
        scratch = Path(scratch)
        guide_before = FIELD_GUIDE.read_bytes()
        code, output = run_stage(["build-kit", "--repository", str(scratch), "--skip-example"])
        assert code == 0, f"build-kit exit {code}: {output.strip().splitlines()[-1] if output.strip() else ''}"
        assert FIELD_GUIDE.read_bytes() == guide_before, "the field guide changed when built again: it was stale"
        different = []
        for name, _ in KIT_2_5:
            if (scratch / "07 Chat kit" / name).read_bytes() != (KIT / name).read_bytes():
                different.append(name)
        for name in ("08 Skill for Claude apps.zip", "AGENTS.md"):
            if (scratch / name).read_bytes() != (REPOSITORY / name).read_bytes():
                different.append(name)
        assert not different, "differs from a fresh build (run build-kit): " + ", ".join(different)
    return "13 kit files, the skill ZIP, AGENTS.md and the field guide"


# ---------------------------------------------------------------- the ZIPs

@group("07 Tools.zip: the tools and the skill's text under breaking-down-stories/, no caches, no long research files")
def tools_zip_layout():
    with zipfile.ZipFile(KIT / "07 Tools.zip") as archive:
        names = archive.namelist()
    assert all(name.startswith(TOP) for name in names), "a file outside breaking-down-stories/"
    tops = {name[len(TOP):].split("/")[0] for name in names}
    for needed in ("SKILL.md", "tools", "schema", "rules", "adapters", "steps", "cards", "templates", "examples",
                   "reference", "library"):
        assert needed in tops, f"no {needed}"
    for needed in ("tools/stage.py", "tools/stage_tools/record_format.py", "schema/schema.json",
                   "steps/08 Shot details.md", "reference/03 Field guide.md", "examples/01 The Catch - scene 10.md"):
        assert TOP + needed in names, f"no {needed}"
    assert not [name for name in names if "__pycache__" in name or name.endswith(".pyc")], "caches inside"
    library = [name[len(TOP):] for name in names if name.startswith(TOP + "library/")]
    long_files = [name for name in library if re.match(r"^library/[A-D]\d+ ", name)]
    assert not long_files, f"research files inside: {long_files[:2]}"
    assert any(name.startswith("library/digests/") for name in library), "no digests"
    return f"{len(names)} files; library: {len(library)} (digests and notes)"


@group("07 Tools.zip unzipped runs: help lists build-kit; new, read and a handout on a small story")
def tools_zip_runs():
    story = REPOSITORY / "tests" / "fixtures" / "reader" / "Night shift.fountain"
    if not story.is_file():
        info("skipped: the small reader fixture is not present")
        return "skip"
    with tempfile.TemporaryDirectory(prefix="wp13-tools-") as scratch:
        scratch = Path(scratch)
        with zipfile.ZipFile(KIT / "07 Tools.zip") as archive:
            archive.extractall(scratch)
        stage = scratch / "breaking-down-stories" / "tools" / "stage.py"
        shutil.copy(story, scratch / story.name)

        def run(arguments, cwd):
            completed = subprocess.run([sys.executable, str(stage)] + arguments, capture_output=True, text=True,
                                       encoding="utf-8", errors="replace", cwd=cwd, timeout=600)
            return completed.returncode, completed.stdout + completed.stderr

        code, output = run(["help"], scratch)
        assert code == 0 and "build-kit" in output, f"help exit {code}"
        code, output = run(["new", story.name], scratch)
        assert code == 0, f"new exit {code}: {output.strip()[-200:]}"
        project = next(path for path in scratch.iterdir() if (path / "00 Start here.md").is_file())
        code, output = run(["read"], project)
        assert code == 0 and (project / "03 Story - numbered.md").is_file(), f"read exit {code}"
        code, output = run(["handout", "U-01-ODDLINES"], project)
        assert code == 0, f"handout exit {code}: {output.strip()[-200:]}"
    return "help, new, read and handout U-01-ODDLINES ran from the unzipped copy"


@group("08 Skill for Claude apps.zip: breaking-down-stories/SKILL.md at its top folder; library cut to digests, D files and notes")
def skill_zip_layout():
    with zipfile.ZipFile(SKILL_ZIP) as archive:
        names = archive.namelist()
        skill_text = archive.read(TOP + "SKILL.md").decode("utf-8") if TOP + "SKILL.md" in names else ""
    assert TOP + "SKILL.md" in names, "no breaking-down-stories/SKILL.md"
    assert all(name.startswith(TOP) for name in names), "a file outside breaking-down-stories/"
    assert re.search(r"^name: breaking-down-stories$", skill_text, re.MULTILINE), "SKILL.md's front matter has no name"
    assert not [name for name in names if "__pycache__" in name or name.endswith(".pyc")], "caches inside"
    library = [name[len(TOP):] for name in names if name.startswith(TOP + "library/")]
    allowed = [name for name in library if name.startswith("library/digests/")
               or re.match(r"^library/(D\d+ |0\d )", name)]
    assert len(allowed) == len(library), f"other library files: {sorted(set(library) - set(allowed))[:3]}"
    for needed in ("steps/00 Start.md", "cards/14 Shot design.md", "tools/stage.py", "schema/schema.json",
                   "reference/03 Field guide.md", "templates/11 Scene.md"):
        assert TOP + needed in names, f"no {needed}"
    size = SKILL_ZIP.stat().st_size
    return f"{len(names)} files, {size // 1024:,} KB; library {len(library)} files"


# ---------------------------------------------------------------- AGENTS.md and the field guide

@group("AGENTS.md is SKILL.md's body with every skill path written out, and every path it names exists")
def agents_file():
    text = read(AGENTS)
    skill_body = read(SKILL / "SKILL.md").split("\n---", 1)[1]
    for heading in re.findall(r"^## (.+)$", skill_body, re.MULTILINE):
        assert f"## {heading}" in text, f"SKILL.md's section {heading!r} is missing"
    assert "<this skill's folder>" not in text, "a path is not written out"
    missing = []
    for path in re.findall(r"`(\.claude/skills/breaking-down-stories/[^`<>*]+?)`", text):
        clean = path.rstrip("/")
        clean = re.split(r" (?=part\b)|\s\|", clean)[0]
        target = REPOSITORY / clean
        if not target.exists() and not list(target.parent.glob(target.name + "*")):
            missing.append(clean)
    assert not missing, f"paths that do not exist: {missing[:4]}"
    return "every section of SKILL.md; every written-out path exists"


@group("reference/03 Field guide.md names every record type and every field of schema.json")
def field_guide():
    schema = json.loads(read(SKILL / "schema" / "schema.json"))
    text = read(FIELD_GUIDE)
    missing = []
    for type_name, record_type in schema["record_types"].items():
        section = re.search(rf"^## {re.escape(type_name)}: .*?(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
        if not section:
            missing.append(type_name)
            continue
        for field in record_type["fields"]:
            if f"| `{field['name']}` |" not in section.group(0):
                missing.append(f"{type_name}.{field['name']}")
    assert not missing, f"missing: {missing[:5]}"
    fields = sum(len(record_type["fields"]) for record_type in schema["record_types"].values())
    return f"{len(schema['record_types'])} record types, {fields} fields"


# ---------------------------------------------------------------- 09 Example

@group("09 Example holds exactly the files of blueprint 2.3; its scene file is the gold's; no local path or address")
def example_folder():
    files = {path.relative_to(EXAMPLE).as_posix() for path in EXAMPLE.rglob("*") if path.is_file()}
    assert files == EXAMPLE_2_3, f"extra {sorted(files - EXAMPLE_2_3)}, missing {sorted(EXAMPLE_2_3 - files)}"
    gold = SKILL / "examples" / "01 The Catch - scene 10.md"
    assert (EXAMPLE / "11 Scenes/Scene 10 - Saye's kitchen.md").read_bytes() == gold.read_bytes(), \
        "the scene file differs from the gold"
    scene_list = read(EXAMPLE / "04 Scene list.md").split(DIVIDER_LINE, 1)[1]
    assert re.findall(r"^### SCENE (\S+)", scene_list, re.MULTILINE) == ["SC10"], "04 holds more than scene 10"
    book = read(EXAMPLE / "15 The breakdown/The breakdown.md")
    assert "Scene 10" in book and "Not mint." in book, "the book has no page for scene 10"
    for path in sorted(EXAMPLE.rglob("*")):
        if path.is_file():
            text = path.read_text(encoding="utf-8", errors="replace")
            assert not EMAIL.search(text), f"{path.name} holds an email address"
            for local in ("/tmp/", "/home/", "/root/", str(REPOSITORY)):
                assert local not in text, f"{path.name} holds a local path"
    return f"{len(files)} files"


@group("09 Example: the plain parts and the book pass the checker's word rules")
def example_words():
    problems = []
    for path in sorted(EXAMPLE.rglob("*.md")):
        text = read(path)
        plain = text.split(DIVIDER_LINE, 1)[0]
        for line_number, line in enumerate(plain.split("\n"), 1):
            for written, kind in words_problems(line):
                problems.append(f"{path.relative_to(EXAMPLE)} line {line_number}: {kind} {written!r}")
    assert not problems, f"{len(problems)} found; first: {problems[:3]}"
    return "no retired words, abbreviations or codes"


# ---------------------------------------------------------------- the guides

@group("the guides are within the lengths of blueprint 2.3")
def guide_lengths():
    lines, outside = [], []
    for name, (low, high) in GUIDES.items():
        words = english_words(read(REPOSITORY / name))
        lines.append(f"{name.split(' ')[0]} {words:,}")
        if not low <= words <= high:
            outside.append(f"{name}: {words:,} words, not {low:,} to {high:,}")
    info("guide lengths: " + "; ".join(lines))
    assert not outside, "; ".join(outside)
    return f"{len(GUIDES)} files"


@group("the guides pass the checker's word rules (WORDS-02 retired words, WORDS-04 abbreviations and codes)")
def guide_words():
    problems = []
    for name in USER_GUIDES:
        for line_number, line in enumerate(read(REPOSITORY / name).split("\n"), 1):
            for written, kind in words_problems(line):
                problems.append(f"{name} line {line_number}: {kind} {written!r}")
    assert not problems, f"{len(problems)} found; first: {problems[:3]}"
    return f"{len(USER_GUIDES)} guides clean"


@group("the guides name only kit files and folders that exist, and CLAUDE.md says what blueprint 2.3 asks")
def guide_names():
    kit_names = {Path(name).stem for name, _ in KIT_2_5} | {name for name, _ in KIT_2_5}
    missing = []
    for name in GUIDES:
        text = read(REPOSITORY / name)
        for mentioned in re.findall(r"`((?:0\d|1[0-2]) [^`]+?)`", text):
            clean = mentioned.split("/")[0]
            if re.match(r"^(0[0-9]|1[0-2]) (Paste|House|Cards|Templates|Checks|Example|Tools|Steps)", clean):
                if clean not in kit_names and not (REPOSITORY / clean).exists():
                    missing.append(f"{name}: {mentioned}")
        for folder in ("07 Chat kit", "08 Skill for Claude apps.zip", "09 Example - The Catch, scene 10",
                       "My stories", "My breakdowns"):
            if folder in text:
                assert (REPOSITORY / folder).exists(), f"{name} names {folder}, which does not exist"
    assert not missing, f"names not in the kit: {missing[:3]}"
    claude = read(REPOSITORY / "CLAUDE.md")
    for needed in ("story-breakdown kit", "breaking-down-stories", "My stories/", "My breakdowns/",
                   "python .claude/skills/breaking-down-stories/tools/stage.py", "For machines - do not edit",
                   "Privacy"):
        assert needed in claude, f"CLAUDE.md does not say {needed!r}"
    readme = read(REPOSITORY / "README.md")
    assert "01 Read me first" in readme and "Not mint." in readme, "README.md lacks the example or the pointer"
    first = read(REPOSITORY / "01 Read me first.md")
    gold = read(SKILL / "examples" / "01 The Catch - scene 10.md")
    for line in re.findall(r"^shot \d{3}, .+$", first, re.MULTILINE):
        assert line.split(":")[0] in gold, f"{line[:30]} is not a line of the gold scene"
    return "kit names, folders, CLAUDE.md's required sentences, README's example and pointer, 01's gold lines"


# ---------------------------------------------------------------- privacy

@group("no file this package writes holds an email address")
def no_email():
    paths = [REPOSITORY / name for name in GUIDES] + [AGENTS, FIELD_GUIDE] + \
        [KIT / name for name, _ in KIT_2_5 if not name.endswith(".zip")] + \
        [TOOLS / "stage_tools" / "build_kit.py"]
    found = [path.name for path in paths if EMAIL.search(read(path))]
    for zip_path in (KIT / "07 Tools.zip", SKILL_ZIP):
        with zipfile.ZipFile(zip_path) as archive:
            for name in archive.namelist():
                if name.endswith((".md", ".txt", ".json", ".py")) and EMAIL.search(archive.read(name).decode("utf-8", "replace")):
                    found.append(f"{zip_path.name}:{name}")
    assert not found, f"email-like text in {found[:3]}"
    return f"{len(paths)} files and both ZIPs"


@group("no file this package writes holds more than a tenth of the story")
def no_whole_story(story):
    if not story:
        info("skipped: story not present (give --story to check that no kit file holds the story)")
        return "skip"
    story_lines = {line.strip() for line in read(story).splitlines() if len(line.strip()) >= 25}
    limit = len(story_lines) // 10
    texts = {name: read(REPOSITORY / name) for name in GUIDES}
    texts.update({f"07 Chat kit/{name}": read(KIT / name) for name, _ in KIT_2_5 if not name.endswith(".zip")})
    for path in EXAMPLE.rglob("*"):
        if path.is_file():
            texts[str(path.relative_to(REPOSITORY))] = path.read_text(encoding="utf-8", errors="replace")
    for zip_path in (KIT / "07 Tools.zip", SKILL_ZIP):
        with zipfile.ZipFile(zip_path) as archive:
            for name in archive.namelist():
                if name.endswith((".md", ".txt")):
                    texts[f"{zip_path.name}:{name}"] = archive.read(name).decode("utf-8", "replace")
    worst = max(((sum(1 for line in story_lines if line in text), name) for name, text in texts.items()))
    assert worst[0] <= limit, f"{worst[1]} holds {worst[0]} story lines (limit {limit})"
    return f"at most {worst[0]} of {len(story_lines)} long story lines in one file ({worst[1]})"


@group("build-kit is a stage.py command")
def command_registered():
    code, output = run_stage(["help"])
    assert code == 0 and re.search(r"^\s+build-kit\s", output, re.MULTILINE), "help does not list build-kit"
    return "listed by stage.py help"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--story", help="The Catch, the whole story (optional)")
    arguments = parser.parse_args()
    story = Path(arguments.story) if arguments.story else None
    if story is not None and not story.is_file():
        print(f"The story file {arguments.story} was not found.")
        return 2
    kit_files()
    instructions_length()
    kit_sizes()
    kit_up_to_date()
    tools_zip_layout()
    tools_zip_runs()
    skill_zip_layout()
    agents_file()
    field_guide()
    example_folder()
    example_words()
    guide_lengths()
    guide_words()
    guide_names()
    no_email()
    no_whole_story(story)
    command_registered()
    failing = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({RESULTS.count(True)} passed, {failing} failing groups)")
    return 0 if not failing else 1


if __name__ == "__main__":
    sys.exit(main())
