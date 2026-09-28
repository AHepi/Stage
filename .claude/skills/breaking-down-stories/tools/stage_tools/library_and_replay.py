"""library_and_replay.py: the commands lib, replay and import-json (blueprint 7.1; fix list C2).

In plain words:
- lib <code> <reference> prints one part of the research library: a section (B1 §10.2), a decision rule (B1 R14),
  a principle (B1 P5), a worked example (B1 Ex1) or any other labelled item (D10 TN2, D4 Recipe 3), with every
  erratum library/02 Errata.md holds for it. A resolved conflict (K03) comes from library/00 Resolved conflicts.md.
  When the full research file is not in this copy of the skill (the skill ZIP keeps only the digests), it prints the
  digest's entry instead, labelled as the digest's.
- replay [--story <path>] checks the gold examples against their expected outputs: it builds a project from the
  gold (examples/01 and 02), works out its derived fields and runs every check. With an expected-check file
  (examples/03 ... expected check.txt) the problem lines must be the same; without one the gold must give no error.
  The derived values blueprint 14.3 (T2) names are compared too. The story is the one at --story, else the scene 10
  excerpt in tests/fixtures, else none (the checks that compare story words then say "skipped: story not present").
- import-json is planned and not in this version: it says so plainly.

Standard library only.
"""

import re
import tempfile
from pathlib import Path

from .project_files import StageStop
from .record_format import SKILL_FOLDER

LIBRARY_FOLDER = "library"
DIGESTS_FOLDER = "digests"
ERRATA_FILE = "02 Errata.md"
CONFLICTS_FILE = "00 Resolved conflicts.md"
CODE_PATTERN = re.compile(r"^(?:[ABC]\d|D\d{1,2}|K\d{2})$")
EXCERPT_FIXTURE = "The Catch - lines 397-489.txt"
EXPECTED_CHECK_FILE = "examples/03 The Catch - scene 10 - expected check.txt"
# Derived values of the gold that blueprint 14.3 (T2) names: (shot, what, expected).
GOLD_DERIVED = [("SC10-SH150", "time floor in seconds", 13.8), ("SC10-SH080", "size from lens and distance", "medium"),
                ("SC10-SH080", "mirror route", "plate")]


# ---------------------------------------------------------------- lib

def library_file(code, skill_folder=SKILL_FOLDER, digest=False):
    """The research file (or its digest) whose name starts with the code, or None."""
    folder = Path(skill_folder) / LIBRARY_FOLDER
    if digest:
        folder = folder / DIGESTS_FOLDER
    if not folder.is_dir():
        return None
    for path in sorted(folder.glob(f"{code} *.md")):
        if digest == path.stem.endswith(" - digest"):
            return path
    return None


def heading_level(line):
    match = re.match(r"^(#{1,6}) ", line)
    return len(match.group(1)) if match else None


def block_from(lines, start):
    """The lines from a heading to the next heading of the same or a higher level."""
    level = heading_level(lines[start]) or 7
    end = start + 1
    while end < len(lines):
        other = heading_level(lines[end])
        if other is not None and other <= level:
            break
        end += 1
    return lines[start:end]


def section_block(lines, number):
    """§10.2: the heading numbered 10.2 (or 10) and what it holds."""
    wanted = re.compile(r"^#{1,6}\s+(?:§\s*)?" + re.escape(number) + r"(?:[.\s)]|$)")
    for index, line in enumerate(lines):
        if wanted.match(line):
            return block_from(lines, index)
    return None


def numbered_item(lines, heading_words, number):
    """Item <number> of the numbered list under the first heading holding one of the heading words (the decision
    rules, the core principles): the item's line and the lines that continue it."""
    for index, line in enumerate(lines):
        if heading_level(line) is None or not any(word in line.lower() for word in heading_words):
            continue
        section = block_from(lines, index)
        for position, text in enumerate(section):
            if re.match(rf"^\s*(?:- )?\**{number}\.\**\s", text):
                end = position + 1
                while end < len(section) and section[end].strip() and not re.match(r"^\s*(?:- )?\**\d+\.\**\s", section[end]) \
                        and heading_level(section[end]) is None and not section[end].startswith("**"):
                    end += 1
                return [line] + section[position:end]
    return None


def example_block(lines, number):
    """Worked example <number>: a heading 'Example N', else the Nth worked-example heading of the file."""
    for index, line in enumerate(lines):
        if heading_level(line) and re.search(rf"\bExample {number}\b", line, re.IGNORECASE):
            return block_from(lines, index)
    worked = [index for index, line in enumerate(lines)
              if heading_level(line) and re.search(r"worked example", line, re.IGNORECASE)]
    subheadings = []
    for index in worked:
        block = block_from(lines, index)
        inner = [index + offset for offset, text in enumerate(block[1:], start=1) if heading_level(text)]
        subheadings.extend(inner if inner else [index])
    if 1 <= number <= len(subheadings):
        return block_from(lines, subheadings[number - 1])
    return None


def labelled_item(lines, label):
    """Any other label (TN2, Recipe 3, S1, L02): a heading holding it, else the paragraph that starts with it."""
    pattern = re.compile(rf"(?<![\w-]){re.escape(label)}(?![\w-])")
    for index, line in enumerate(lines):
        if heading_level(line) and pattern.search(line):
            return block_from(lines, index)
    for index, line in enumerate(lines):
        stripped = line.lstrip("-* |").lstrip("*")
        if stripped.startswith(label) and pattern.match(stripped):
            end = index + 1
            while end < len(lines) and lines[end].strip() and heading_level(lines[end]) is None \
                    and not re.match(r"^\s*(?:[-*|]|\d+\.)\s", lines[end]):
                end += 1
            return lines[index:end]
    for index, line in enumerate(lines):
        if pattern.search(line):
            return [line]
    return None


def find_reference(lines, reference):
    """The lines a reference names in a research file, or None."""
    text = reference.strip()
    section = re.fullmatch(r"(?:§|section\s*)?\s*(\d+(?:\.\d+)*)", text, re.IGNORECASE)
    if section:
        return section_block(lines, section.group(1))
    rule = re.fullmatch(r"R(\d+)", text)
    if rule:
        return numbered_item(lines, ("decision rules", "rules"), int(rule.group(1)))
    principle = re.fullmatch(r"P(\d+)", text)
    if principle:
        return numbered_item(lines, ("principles",), int(principle.group(1)))
    example = re.fullmatch(r"(?:Ex|Example\s*)(\d+)", text, re.IGNORECASE)
    if example:
        return example_block(lines, int(example.group(1)))
    return labelled_item(lines, text)


def errata_for(code, reference, skill_folder=SKILL_FOLDER):
    """The lines of library/02 Errata.md about this code and reference (or about the whole file)."""
    path = Path(skill_folder) / LIBRARY_FOLDER / ERRATA_FILE
    if not path.is_file():
        return []
    found = []
    wanted = re.compile(rf"\b{re.escape(code)}\s+{re.escape(reference.strip())}(?![\w.])") if reference else None
    for line in path.read_text(encoding="utf-8").splitlines():
        if wanted is not None and wanted.search(line):
            found.append(line.strip())
    return found


def conflict_lines(code, skill_folder=SKILL_FOLDER):
    path = Path(skill_folder) / LIBRARY_FOLDER / CONFLICTS_FILE
    if not path.is_file():
        return None
    lines = path.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        if re.search(rf"(?<![\w-]){code}(?![\w-])", line) and (line.startswith("|") or heading_level(line)):
            return block_from(lines, index) if heading_level(line) else [line]
    return None


def library_text(code, reference, skill_folder=SKILL_FOLDER):
    """(header line, lines, errata lines) for lib, or StageStop with a plain line."""
    code = code.strip().upper()
    if not CODE_PATTERN.match(code):
        raise StageStop(f'"{code}" is not a library code. Codes look like B1, D10 or K03 (library/01 What the codes '
                        "mean.md lists them).")
    if code.startswith("K"):
        found = conflict_lines(code, skill_folder)
        if not found:
            raise StageStop(f"{code} is not in library/{CONFLICTS_FILE}.")
        return f"{code} (library/{CONFLICTS_FILE})", found, []
    full = library_file(code, skill_folder)
    reference = (reference or "").strip()
    if full is not None:
        lines = full.read_text(encoding="utf-8").splitlines()
        found = find_reference(lines, reference) if reference else lines[:40]
        if found:
            return (f"{code} {reference} (library/{full.name})".replace("  ", " "), found,
                    errata_for(code, reference, skill_folder))
    digest = library_file(code, skill_folder, digest=True)
    if digest is not None:
        lines = digest.read_text(encoding="utf-8").splitlines()
        found = find_reference(lines, reference) if reference else lines[:40]
        if found:
            why = "the full file is not in this copy of the skill" if full is None else \
                "the full file does not label it this way"
            return (f"{code} {reference}: from the digest (library/{DIGESTS_FOLDER}/{digest.name}), because {why}",
                    found, errata_for(code, reference, skill_folder))
    if full is None and digest is None:
        raise StageStop(f"No library file starts with {code} in this copy of the skill.")
    raise StageStop(f'"{reference}" was not found in {code}. References look like §10.2, R14, P5, Ex1 or a label '
                    "the file uses (TN2, Recipe 3).")


def add_lib_arguments(parser):
    parser.add_argument("code", help="the research code, for example B1, D10 or K03")
    parser.add_argument("reference", nargs="*", help="what to print: §10.2, R14, P5, Ex1 or a label such as TN2")


def run_lib(context):
    reference = " ".join(context.arguments.reference or [])
    header, lines, errata = library_text(context.arguments.code, reference, context.skill_folder)
    context.say(header + ":")
    for line in lines:
        context.say(line)
    if errata:
        context.say("Errata (library/02 Errata.md):")
        for line in errata:
            context.say(line)
    context.summary = f"lib {context.arguments.code} {reference}".strip()
    return 0


# ---------------------------------------------------------------- replay

def excerpt_fixture(skill_folder=SKILL_FOLDER):
    """tests/fixtures/The Catch - lines 397-489.txt next to the skill in the Stage folder, or None."""
    for folder in Path(skill_folder).resolve().parents:
        candidate = folder / "tests" / "fixtures" / EXCERPT_FIXTURE
        if candidate.is_file():
            return candidate
    return None


def expected_lines(skill_folder=SKILL_FOLDER):
    path = Path(skill_folder) / EXPECTED_CHECK_FILE
    if not path.is_file():
        return None
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines()
            if re.match(r"^[EW] [A-Z]+-\d{2} ", line.strip())]


def replay_gold(story_path=None, skill_folder=SKILL_FOLDER, say=print):
    """Replay the gold of The Catch, scene 10. Returns (passed, lines)."""
    from .build_kit import gold_project
    from .check_records import StorySource, run_checks
    from .derive_fields import Breakdown, mirror_route, size_check, time_floor
    from .project_files import Project
    from .record_format import load_skill_data
    schema, words, constants = load_skill_data()
    lines = []
    story = Path(story_path) if story_path else excerpt_fixture(skill_folder)
    with tempfile.TemporaryDirectory(prefix="stage-replay-") as temporary:
        folder, _ = gold_project(Path(temporary) / "The Catch", skill_folder)
        project = Project(folder, schema, words)
        record_files = project.load_record_files()
        source = StorySource.from_file(str(story), constants) if story else None
        result = run_checks(record_files, schema, words, constants, story=source)
        problems = [str(problem) for problem in result.problems if getattr(problem, "level", "") in ("E", "W")]
        errors = [line for line in problems if line.startswith("E ")]
        passed = True
        expected = expected_lines(skill_folder)
        if expected is not None:
            written = sorted(re.sub(r" \[[^\]]*\]$", "", line) for line in problems)
            wanted = sorted(re.sub(r" \[[^\]]*\]$", "", line) for line in expected)
            if written != wanted:
                passed = False
                lines.append(f"FAIL the check lines differ from {EXPECTED_CHECK_FILE}: "
                             f"{len(set(written) - set(wanted))} new, {len(set(wanted) - set(written))} missing.")
            else:
                lines.append(f"PASS the check lines match {EXPECTED_CHECK_FILE} ({len(written)} lines).")
        else:
            if errors:
                passed = False
                lines.append(f"FAIL the gold gives {len(errors)} error lines (it must give none); the first: {errors[0]}")
            else:
                lines.append(f"PASS the gold gives no error ({len(problems)} warnings).")
        skipped = [f"Skipped {check_id}: {why}" for check_id, why in result.skipped if "story not present" in why]
        if skipped:
            lines.append(f"{len(skipped)} checks skipped: story not present (give --story, or keep the scene 10 "
                         "excerpt in tests/fixtures).")
        breakdown = Breakdown.from_project(folder, schema, words, constants)
        if story:
            breakdown.attach_story_file(str(story))
        for shot_identifier, what, wanted in GOLD_DERIVED:
            shot = breakdown.record(shot_identifier, "SHOT")
            found = None
            if shot is not None:
                if what.startswith("time floor"):
                    floor = time_floor(breakdown, shot) if story else None
                    found = round(floor.floor, 1) if floor is not None and floor.floor is not None else None
                    if not story:
                        lines.append(f"Skipped {shot_identifier} {what}: story not present.")
                        continue
                elif what.startswith("size"):
                    check = size_check(breakdown, shot)
                    found = check.size if check is not None else None
                else:
                    found = mirror_route(breakdown, shot).route
            ok = found == wanted
            passed = passed and ok
            lines.append(f"{'PASS' if ok else 'FAIL'} {shot_identifier} {what}: {found} (expected {wanted}).")
    story_words = f"the story {story.name}" if story else "no story (story not present)"
    lines.insert(0, f"Replay of the gold (The Catch, scene 10) with {story_words}:")
    return passed, lines


def add_replay_arguments(parser):
    parser.add_argument("--story", help="the whole story or an excerpt (default: the scene 10 excerpt in tests/fixtures)")


def run_replay(context):
    story = getattr(context.arguments, "story", None)
    if story and not Path(story).is_file():
        raise StageStop(f'The story file "{Path(story).name}" was not found. Give its path, or leave --story out.')
    passed, lines = replay_gold(story, context.skill_folder)
    for line in lines:
        context.say(line)
    context.say("RESULT: PASS" if passed else "RESULT: FAIL")
    context.summary = f"replay {'passed' if passed else 'failed'}"
    return 0 if passed else 1


# ---------------------------------------------------------------- import-json (planned)

def add_import_json_arguments(parser):
    parser.add_argument("file", nargs="?", help="a JSON file of records from an API's structured output")


def run_import_json(context):
    raise StageStop("import-json is not in this version of the tools. Write the records as record text in an inbox "
                    "file and run stage.py apply on it.")


def register_commands(table):
    table.add("lib", "Print one part of the research library (B1 R14, B1 §10.2, B1 P5, B1 Ex1) with its errata",
              run_lib, add_lib_arguments, uses_project=False)
    table.add("replay", "Check the gold examples against their expected outputs (maintainers)", run_replay,
              add_replay_arguments, uses_project=False)
    table.add("import-json", "Not in this version: accept records as JSON from an API", run_import_json,
              add_import_json_arguments, uses_project=False)
