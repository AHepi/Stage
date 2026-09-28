#!/usr/bin/env python3
"""WP4d acceptance test: the CRAFT, INFO, REASON and WORDS checks of blueprint 7.2
(tools/stage_tools/checks_craft_reasons_words.py).

What it checks, in plain words:
- every CRAFT, INFO, REASON and WORDS check of 7.2 is registered with 7.2's level and build, with a plain sentence
  for the health check that holds no code or abbreviation; the build-2 checks (CRAFT-17, REASON-09) are registered
  as build 2 and say plainly why they are skipped;
- every one of these checks is silent on the WP12a gold fixture (examples/01 The Catch - scene 10.md and its
  context file), with the scene 10 excerpt, without any story, at steps 7 and 8 and for check --all, and on the
  chat-saved copy of the same scene; stage.py check --all on a project made from the gold prints none of their lines;
- each build-1 check fires on its faulty fixture (tests/fixtures/craft reasons and words/faults.json), on the
  record and field it names, in 7.2's line format (level, check ID, record, field, what is wrong, then the fix);
- at step 7, before any shot is written, the checks that step lists read the shot list's items;
- reasons: mood-only reasons and reasons that would fit any film are rejected (REASON-03 and REASON-04, from the
  word lists in rules/words.json), and reasons that quote the scene, cite an ID or name an element pass;
- the text helpers other modules use (retired words, abbreviations) find what they should.

Usage: python tests/wp4d_acceptance.py [--story <the whole story or an excerpt>]
Without --story it reads tests/fixtures/The Catch - lines 397-489.txt; when no story is present the groups that
need one report "skipped: story not present". Standard library only.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
TOOLS = SKILL / "tools"
EXAMPLES = SKILL / "examples"
SCENE_FILE = "01 The Catch - scene 10.md"
CONTEXT_FILE = "02 The Catch - scene 10 - context.md"
EXCERPT = REPOSITORY / "tests" / "fixtures" / "The Catch - lines 397-489.txt"
CHAT_FOLDER = REPOSITORY / "tests" / "fixtures" / "chat saved scene 10"
FAULTS = REPOSITORY / "tests" / "fixtures" / "craft reasons and words" / "faults.json"
MODULE = TOOLS / "stage_tools" / "checks_craft_reasons_words.py"
sys.path.insert(0, str(TOOLS))

from stage_tools import check_records  # noqa: E402
from stage_tools import checks_craft_reasons_words as family  # noqa: E402
from stage_tools.record_format import load_skill_data, parse_file  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
FAMILIES = ("CRAFT", "INFO", "REASON", "WORDS")
DIVIDER = "Below this line: details for the AI and the checker. You never need to read them."
RESULTS = []

# Blueprint 7.2: level and build of every check this family owns.
EXPECTED = {
    "CRAFT-01": ("W", 1), "CRAFT-02": ("W", 1), "CRAFT-03": ("W", 1), "CRAFT-04": ("E", 1), "CRAFT-05": ("E", 1),
    "CRAFT-06": ("E", 1), "CRAFT-07": ("W", 1), "CRAFT-08": ("W", 1), "CRAFT-09": ("W", 1), "CRAFT-10": ("W", 1),
    "CRAFT-11": ("E", 1), "CRAFT-12": ("W", 1), "CRAFT-13": ("W", 1), "CRAFT-14": ("E", 1), "CRAFT-15": ("W", 1),
    "CRAFT-16": ("E", 1), "CRAFT-17": ("W", 2), "CRAFT-18": ("E", 1), "CRAFT-19": ("W", 1), "CRAFT-20": ("W", 1),
    "CRAFT-21": ("W", 1), "CRAFT-22": ("W", 1), "CRAFT-23": ("W", 1), "CRAFT-24": ("W", 1), "CRAFT-25": ("W", 1),
    "CRAFT-26": ("W", 1),
    "INFO-01": ("W", 1), "INFO-02": ("W", 1),
    "REASON-01": ("E", 1), "REASON-02": ("E", 1), "REASON-03": ("E", 1), "REASON-04": ("E", 1),
    "REASON-05": ("E", 1), "REASON-06": ("E", 1), "REASON-07": ("E", 1), "REASON-08": ("E", 1),
    "REASON-09": ("W", 2),
    "WORDS-01": ("E", 1), "WORDS-02": ("W", 1), "WORDS-03": ("E", 1), "WORDS-04": ("W", 1), "WORDS-05": ("E", 1),
}
# 7.2's line: level, check ID, record, field, what is wrong, then the fix; the checker adds [file, line n].
LINE_FORMAT = re.compile(r'^(E|W|N) ([A-Z]+-\d{2}) (\S+|"[^"]+")(?: ([a-z_]+(?: [a-z_]+)?))? \S.*?[.?!"]'
                         r' Fix: .+?[.?!"]( \[[^\]]+\])?$')


def report(level, name, detail=""):
    RESULTS.append(level)
    print(f"{level:<5} {name}" + (f": {detail}" if detail else ""))


class Skip(Exception):
    pass


def group(name):
    """Run a test group: it returns a detail line, or raises AssertionError (FAIL) or Skip (INFO)."""
    def wrap(function):
        try:
            detail = function()
        except Skip as skip:
            report("INFO", name, str(skip))
        except AssertionError as error:
            report("FAIL", name, str(error))
        except Exception as error:  # a crash is a failure, with its type
            report("FAIL", name, f"{type(error).__name__}: {error}")
        else:
            report("PASS", name, detail or "")
        return function
    return wrap


# ---------------------------------------------------------------- making the record files

def record_block(text, heading):
    """(start, end) of the record whose heading starts '### <heading>' (to the next '#' line, '---' or END)."""
    match = re.search(r"^### " + re.escape(heading) + r"(?=\s|$)", text, re.MULTILINE)
    if not match:
        raise AssertionError(f"record {heading} not found")
    end = re.search(r"^(#|---\s*$|END OF FILE)", text[match.end():], re.MULTILINE)
    return match.start(), match.end() + (end.start() if end else len(text) - match.end())


def replace_once(text, heading, find, replace):
    """Replace a text found exactly once inside a record (or, with no heading, in the plain part above the
    divider)."""
    if heading is None:
        start, end = 0, text.index(DIVIDER)
    else:
        start, end = record_block(text, heading)
    block = text[start:end]
    if block.count(find) != 1:
        raise AssertionError(f'"{find[:60]}" is found {block.count(find)} times in {heading or "the plain part"}, '
                             "not once")
    return text[:start] + block.replace(find, replace) + text[end:]


def gold_texts():
    return {"scene": (EXAMPLES / SCENE_FILE).read_text(encoding="utf-8"),
            "context": (EXAMPLES / CONTEXT_FILE).read_text(encoding="utf-8")}


def write_pair(folder, texts):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / SCENE_FILE).write_text(texts["scene"], encoding="utf-8")
    (folder / CONTEXT_FILE).write_text(texts["context"], encoding="utf-8")
    return [folder / CONTEXT_FILE, folder / SCENE_FILE]


def parsed(paths):
    return [parse_file(path, path.name, SCHEMA) for path in paths]


def family_ids(build=None):
    check_records.load_check_families()
    return sorted(check_id for check_id, definition in check_records.REGISTRY.items()
                  if check_id.split("-")[0] in FAMILIES and (build is None or definition.build == build))


def run_family(paths, story_path, check_ids=None, step=None):
    """Run this family's checks (or the named ones) on record files, with the story given (or none)."""
    check_records.load_check_families()
    wanted = check_ids if check_ids is not None else family_ids()
    source = check_records.StorySource.from_file(str(story_path), CONSTANTS) if story_path else None
    if step is not None:
        listed = check_records.checks_for_step(step)
        wanted = [check_id for check_id in wanted if listed is None or check_id in listed]
    return check_records.run_checks(parsed(paths), SCHEMA, WORDS, CONSTANTS, story=source, check_ids=wanted,
                                    step=step)


def family_lines(result):
    return [str(problem) for problem in result.problems
            if getattr(problem, "check_id", "").split("-")[0] in FAMILIES]


def make_project(folder, texts):
    """A project folder from the gold: the context's sections as the numbered files, the scene file in 11 Scenes."""
    folder.mkdir(parents=True)
    (folder / "For machines - do not edit").mkdir()
    context = texts["context"].split(DIVIDER, 1)[1]
    sections = re.split(r"^## From (.+)$", context, flags=re.MULTILINE)[1:]
    for name, body in zip(sections[0::2], sections[1::2]):
        body = re.sub(r"\n+END OF FILE .*$", "", body.strip(), flags=re.DOTALL)
        count = len(re.findall(r"^### ", body, re.MULTILINE))
        (folder / f"{name.strip()}.md").write_text(
            f"# {name.strip()}\n\n{DIVIDER}\n\n{body}\n\nEND OF FILE | {name.strip()} | {count} records\n",
            encoding="utf-8")
    scenes = folder / "11 Scenes"
    scenes.mkdir()
    (scenes / "Scene 10 - Saye's kitchen.md").write_text(texts["scene"], encoding="utf-8")
    return folder


def without_shots(scene_text):
    """The gold scene file as it stands at step 7: its SHOT and CUT records taken out (the shot list stays)."""
    pieces = re.split(r"(?=^### )", scene_text, flags=re.MULTILINE)
    kept = [piece for piece in pieces if not re.match(r"### (SHOT|CUT) ", piece)]
    text = "".join(kept)
    if not text.rstrip().splitlines()[-1].startswith("END OF FILE"):
        text = text.rstrip() + "\n\nEND OF FILE | Scene 10 - Saye's kitchen | 0 records\n"
    count = len(re.findall(r"^### ", text, re.MULTILINE))
    return re.sub(r"\| \d+ records?(\s*)$", f"| {count} records\\1", text)


# ---------------------------------------------------------------- the tests

def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--story", help="the whole story, or an excerpt (default: the scene 10 excerpt fixture)")
    arguments = parser.parse_args()
    story = Path(arguments.story) if arguments.story else EXCERPT
    if not story.is_file():
        story = None
    whole_story = story is not None and story != EXCERPT

    @group("registry: every CRAFT, INFO, REASON and WORDS check of 7.2 registered with its level, build and a plain "
           "sentence")
    def registry():
        found = family_ids()
        missing = sorted(set(EXPECTED) - set(found))
        extra = sorted(set(found) - set(EXPECTED))
        assert not missing and not extra, f"missing {missing}, not in 7.2 {extra}"
        wrong = []
        for check_id, (level, build) in EXPECTED.items():
            definition = check_records.REGISTRY[check_id]
            if definition.level != level or definition.build != build:
                wrong.append(f"{check_id} is {definition.level} build {definition.build}, 7.2 says {level} build "
                             f"{build}")
            if definition.module != family.__name__:
                wrong.append(f"{check_id} is registered by {definition.module}")
            codes = family.abbreviations_in_text(definition.plain, WORDS)
            if codes or not definition.plain or definition.plain[0].isupper():
                wrong.append(f"{check_id}'s plain sentence {definition.plain!r} ({codes})")
        assert not wrong, wrong
        top = MODULE.read_text(encoding="utf-8").split('"""')[1]
        assert "CRAFT" in top and "REASON" in top and "Standard library only" in top, "the module's top note"
        return f"{len(found)} checks ({len(family_ids(1))} build 1, {len(family_ids(2))} build 2), each with 7.2's " \
               "level and build and a plain sentence with no code"

    with tempfile.TemporaryDirectory(prefix="wp4d-") as temporary:
        temporary = Path(temporary)
        texts = gold_texts()
        gold_paths = write_pair(temporary / "gold", texts)

        @group("silent on the gold: every CRAFT, INFO, REASON and WORDS check, with the story given, at steps 7 and "
               "8 and for --all")
        def silent_with_story():
            if story is None:
                raise Skip("skipped: story not present")
            details = []
            for step in (None, 7, 8):
                result = run_family(gold_paths, story, step=step)
                assert not result.crashed and not result.families_broken, (result.crashed, result.families_broken)
                lines = family_lines(result)
                assert not lines, f"step {step or 'all'}: {lines}"
                details.append(f"{'--all' if step is None else f'--step {step}'} {len(result.checks_run)} checks")
            skipped = sorted({check_id for check_id, _ in result.skipped if check_id.split("-")[0] in FAMILIES})
            return f"no line ({'; '.join(details)}); skipped: {', '.join(skipped)} (build 2)" + (
                " (the whole story)" if whole_story else " (the scene 10 excerpt)")

        @group("silent on the gold without any story: the story checks say 'story not present'")
        def silent_without_story():
            result = run_family(gold_paths, None)
            assert not result.crashed, result.crashed
            lines = family_lines(result)
            assert not lines, lines
            reasons = {check_id: why for check_id, why in result.skipped}
            assert "story not present" in reasons.get("CRAFT-10", ""), reasons
            return f"no line; {len(result.checks_run)} checks ran; CRAFT-10 skipped its script marks: story not present"

        @group("silent on the chat-saved copy of scene 10 (quote anchors, hear words, two batch files)")
        def silent_on_chat_copy():
            if not CHAT_FOLDER.is_dir():
                raise Skip("skipped: the chat-saved fixture is not present")
            paths = sorted(CHAT_FOLDER.rglob("*.md"))
            result = run_family(paths, story)
            assert not result.crashed, result.crashed
            lines = family_lines(result)
            assert not lines, lines
            return f"no line on {len(paths)} files; {len(result.checks_run)} checks ran"

        @group("each build-1 check fires on its faulty fixture, on the named record and field, in 7.2's line format")
        def faults_fire():
            faults = json.loads(FAULTS.read_text(encoding="utf-8"))["faults"]
            fired, skipped, failures = [], [], []
            for index, fault in enumerate(faults):
                if fault.get("needs_story") and story is None:
                    skipped.append(fault["check"])
                    continue
                changed = dict(texts)
                for edit in fault["edits"]:
                    changed[edit["file"]] = replace_once(changed[edit["file"]], edit["record"], edit["find"],
                                                         edit["replace"])
                paths = write_pair(temporary / f"fault {index:02d}", changed)
                result = run_family(paths, story, [fault["check"]])
                assert not result.crashed, result.crashed
                level = EXPECTED[fault["check"]][0]
                hits = [problem for problem in result.problems
                        if problem.check_id == fault["check"] and problem.record == fault["record"]
                        and (problem.field_name or None) == fault.get("field")]
                if not hits:
                    failures.append(f"{fault['check']} did not fire on {fault['record']} {fault.get('field')} "
                                    f"({fault['about']}); got {[str(problem) for problem in result.problems]}")
                    continue
                line = str(hits[0])
                head = f"{level} {fault['check']} {fault['record']}" + (
                    f" {fault['field']}" if fault.get("field") else "") + " "
                if not line.startswith(head) or not LINE_FORMAT.match(line) or hits[0].level != level:
                    failures.append(f"{fault['check']}: not in 7.2's format: {line}")
                    continue
                if not hits[0].file_name or not hits[0].line_number:
                    failures.append(f"{fault['check']}: not placed in a file and line: {line}")
                    continue
                fired.append(f"{fault['check']} {fault['record']}")
            assert not failures, failures
            covered = {entry.split()[0] for entry in fired} | set(skipped)
            missing = sorted(set(family_ids(1)) - covered)
            assert not missing, f"build-1 checks with no faulty fixture: {missing}"
            example = str(hits[0]) if hits else ""
            return f"{len(fired)} faults for {len({entry.split()[0] for entry in fired})} checks, each caught; " \
                   f"for example: {example}" + (f"; skipped (story not present): {', '.join(skipped)}"
                                                 if skipped else "")

        @group("step 7: before the shots exist, CRAFT-04, 05, 10, 18 and 19 read the shot list and the beats")
        def step_seven():
            listed = check_records.checks_for_step(7) or []
            step_checks = [check_id for check_id in listed if check_id.split("-")[0] in FAMILIES]
            base = dict(texts)
            base["scene"] = without_shots(texts["scene"])
            result = run_family(write_pair(temporary / "step 7", base), story, step_checks, step=7)
            assert not result.crashed, result.crashed
            assert not family_lines(result), family_lines(result)
            broken = dict(base)
            broken["scene"] = replace_once(base["scene"], "SHOTLIST SC10-LIST",
                                           "SC10-SH150 | beats: SC10-B07, SC10-B08 | role: turn",
                                           "SC10-SH150 | beats: SC10-B07, SC10-B08 | role: must_keep")
            result = run_family(write_pair(temporary / "step 7 broken", broken), story, ["CRAFT-04"], step=7)
            lines = family_lines(result)
            assert any(line.startswith("E CRAFT-04 SC10-B07 turn ") for line in lines), lines
            return f"silent on the list-only scene ({', '.join(step_checks)}); a list whose turn item lost role: " \
                   f"turn gives: {lines[0]}"

        @group("reasons: mood-only reasons and reasons that fit any film are rejected (words.json); anchored "
               "reasons pass")
        def reasons():
            if story is None:
                raise Skip("skipped: story not present (quotes cannot be looked up)")
            source = check_records.StorySource.from_file(str(story), CONSTANTS)
            run = check_records.CheckRun(parsed(gold_paths), SCHEMA, WORDS, CONSTANTS, story=source)
            rejected_as_any_film = [
                "The camera holds so the moment can land.",
                "A wider lens makes the room feel bigger and emptier.",
                "It is more interesting this way.",
            ]
            rejected_as_mood = [
                "To build tension before the reveal.",
                "Moody, cinematic framing on Iona.",
                "The lamp is low to emphasise.",
                "For drama, the flask stays in frame.",
                "Dynamic angle on Saye.",
            ]
            mood_only_feeling = ["It feels lonely and tense."]
            passing = [
                '"Her face changes." puts the turn inside her mouth.',
                "The flask is what Saye looks at longest.",
                "Held for SC10-B07, where the value turns.",
                "The lamp on the table lights both women alike.",
                "The long lens is there to emphasise the distance between Iona and Saye.",
            ]
            wrong = []
            for text in rejected_as_any_film:
                if family.reason_is_anchored(run, text, "SC10"):
                    wrong.append(f"any-film reason accepted: {text}")
            for text in rejected_as_mood:
                if not family.mood_only_phrases_in_reason(text, WORDS):
                    wrong.append(f"mood-only reason not caught: {text}")
            for text in mood_only_feeling:
                if family.mood_only_phrases_in_reason(text, WORDS) or family.reason_is_anchored(run, text, "SC10") \
                        or not family.mood_words_in(WORDS, text):
                    wrong.append(f"feeling-only reason not caught by REASON-03 and REASON-04 together: {text}")
            for text in passing:
                if family.mood_only_phrases_in_reason(text, WORDS) or not family.reason_is_anchored(run, text, "SC10"):
                    wrong.append(f"good reason rejected: {text}")
            assert not family.reason_is_anchored(run, 'The frame "is not in this story at all" here.', "SC10"), \
                "a quote the scene does not hold was taken as an anchor"
            assert not wrong, wrong
            phrases = WORDS["mood_only_phrases"]["phrases"]
            return (f"{len(rejected_as_any_film)} any-film and {len(rejected_as_mood) + len(mood_only_feeling)} "
                    f"mood-only reasons rejected, {len(passing)} anchored reasons passed (words.json lists "
                    f"{len(phrases)} mood-only phrases)")

        @group("text helpers for other modules: retired words and abbreviations in user-facing text")
        def text_helpers():
            retired = [written for written, _ in family.retired_words_in_text(
                "The key shot uses a greybox and the stage.py tool; Stage is the product.", WORDS)]
            assert "key shot" in retired and "greybox" in retired, retired
            assert not any(word.lower() == "stage" for word in retired), retired
            quoted = family.retired_words_in_text('She says "the key shot" in the script.', WORDS)
            assert not quoted, quoted
            codes = [written for written, _ in family.abbreviations_in_text(
                "Shot 150 is a CU from checkpoint C, see SC10-SH150 and B1 R14; open Shot list.csv.", WORDS)]
            assert "CU" in codes and "SC10-SH150" in codes and "B1 R14" in codes, codes
            assert not family.abbreviations_in_text("Shot 150 is a close-up of the flask; the CAMERA holds.", WORDS)
            return f"retired: {retired}; codes: {codes}"

        @group("stage.py check --all on a project made from the gold prints no CRAFT, INFO, REASON or WORDS line")
        def whole_command():
            project = make_project(temporary / "project", texts)
            command = [sys.executable, str(TOOLS / "stage.py"), "check", "--all", "--project", str(project)]
            if story is not None:
                command += ["--story", str(story)]
            completed = subprocess.run(command, capture_output=True, text=True, timeout=300)
            assert completed.returncode in (0, 1), completed.stdout + completed.stderr
            lines = [line for line in completed.stdout.splitlines()
                     if re.match(r"^[EWN] (CRAFT|INFO|REASON|WORDS)-\d{2} ", line)]
            assert not lines, lines
            report_text = (project / "13 Health check.md").read_text(encoding="utf-8")
            assert report_text.startswith("In short:"), report_text[:80]
            return f"exit {completed.returncode}; no line from these families; 13 Health check.md written"

    failing = RESULTS.count("FAIL")
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({failing} failing groups)")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
