#!/usr/bin/env python3
"""run_tests.py: runs every acceptance test of the Stage kit and prints one plain line for each (blueprint 14.3, T0).

What it does:
- finds every test file in this folder (wp*_*.py, *_acceptance.py, *_conformance.py; not this file);
- runs each one in its own Python process, a few at a time, and reads its last "RESULT:" line;
- prints one line per test, in a fixed order: PASS or FAIL, the file, how many groups passed and failed, how many
  groups said "skipped", the seconds it took, and for a failing test its first FAIL line;
- ends with one RESULT line and exits 0 when every test passed, 1 when one failed, 2 when it could not run.

Stories. The whole stories are never in the repository (builder rule 5). Every test runs without them: the groups
that need a story say "skipped: story not present" inside the test, and the scene 10 excerpt in tests/fixtures
is used where a test can use it. Give the stories to run those groups as well:
    --story-catch "<The Catch, the whole story>"      passed as --story (or as the first story) to the tests that
                                                       take The Catch
    --story-long "<The Long Places, the whole story>"  passed to the tests that take The Long Places (the reader
                                                       test and the estimate test)

Usage:
    python tests/run_tests.py
    python tests/run_tests.py --story-catch "My stories/The Catch.txt" --story-long "My stories/The Long Places.md"
    python tests/run_tests.py --only wp2 wp4b     (only tests whose file names start with these words)
    python tests/run_tests.py --no-render          (grey preview test without Blender renders, which take minutes)
    python tests/run_tests.py --jobs 1             (one test at a time; the default runs 4 at once)
    python tests/run_tests.py --blueprint <blueprint.md>   (for the two tests that can also read the blueprint)
    python tests/run_tests.py --verbose            (also print each test's whole output after its line)

Standard library only.
"""

import argparse
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

TESTS_FOLDER = Path(__file__).resolve().parent
REPOSITORY = TESTS_FOLDER.parent
THIS_FILE = Path(__file__).resolve().name
TEST_FILE_PATTERNS = ("wp*_*.py", "*_acceptance.py", "*_conformance.py")
TIMEOUT_SECONDS = int(os.environ.get("STAGE_TEST_TIMEOUT_SECONDS", "2400"))

# How each test takes the stories, when it does not simply take --story <The Catch> (found in its source).
# "positional": [<The Catch>] [<The Long Places>] as its first arguments.
POSITIONAL_STORIES = {"wp3_reader_acceptance.py", "wp7_acceptance.py"}
# Tests that can also read the blueprint (--blueprint), which lives outside the repository.
BLUEPRINT_TESTS = {"wp1_schema_acceptance.py", "wp10a_skill_text_acceptance.py"}
# The grey preview test renders in Blender unless it is told not to.
RENDER_TEST = "wp9_acceptance.py"

RESULT_LINE = re.compile(r"^RESULT:\s*(PASS|FAIL)\b(.*)$")
GROUP_LINE = re.compile(r"^(PASS|FAIL)\b")


def find_tests(only=None):
    """The test files in a fixed order: the work packages by number, then the others by name."""
    found = set()
    for pattern in TEST_FILE_PATTERNS:
        found.update(path for path in TESTS_FOLDER.glob(pattern) if path.name != THIS_FILE)
    tests = sorted(found, key=order_key)
    if only:
        tests = [path for path in tests if any(path.name.startswith(word) for word in only)]
    return tests


def order_key(path):
    """wp1 before wp2 before wp10a; files that are not a work package's come last, by name."""
    match = re.match(r"^wp(\d+)([a-z]?)_", path.name)
    if match:
        return (0, int(match.group(1)), match.group(2), path.name)
    return (1, 0, "", path.name)


def takes_story_option(path):
    """True when the test's own command line has --story."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    return bool(re.search(r"""add_argument\(\s*["']--story["']""", text))


def command_for(path, options):
    """The command line that runs one test with the stories and options it can use."""
    command = [sys.executable, str(path)]
    if path.name in POSITIONAL_STORIES:
        if options.story_catch:
            command.append(options.story_catch)
            if options.story_long:
                command.append(options.story_long)
        if path.name == "wp7_acceptance.py" and options.story_catch:
            command += ["--story", options.story_catch]
    elif options.story_catch and takes_story_option(path):
        command += ["--story", options.story_catch]
    if path.name in BLUEPRINT_TESTS and options.blueprint:
        command += ["--blueprint", options.blueprint]
    if path.name == RENDER_TEST and options.no_render:
        command.append("--no-render")
    return command


class TestRun:
    """One test's outcome."""

    def __init__(self, path):
        self.path = path
        self.passed = False
        self.groups_passed = 0
        self.groups_failed = 0
        self.skipped = 0
        self.seconds = 0.0
        self.first_failure = ""
        self.result_text = ""
        self.output = ""
        self.exit_code = None
        self.problem = ""

    def line(self):
        """The one plain summary line for this test."""
        word = "PASS" if self.passed else "FAIL"
        name = self.path.name
        took = f"{self.seconds:.1f} s" if self.seconds < 10 else f"{self.seconds:.0f} s"
        if self.problem:
            return f"{word}  {name}: {self.problem} ({took})"
        groups = f"{self.groups_passed} group{'s' if self.groups_passed != 1 else ''} passed"
        if self.groups_failed:
            groups += f", {self.groups_failed} failed"
        if self.skipped:
            groups += f", {self.skipped} said skipped"
        text = f"{word}  {name}: {groups} ({took})"
        if not self.passed and self.first_failure:
            text += f"; first failure: {shorten(self.first_failure, 220)}"
        return text


def shorten(text, limit):
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit - 3].rstrip() + "..."


def run_one(path, options):
    """Run one test file and read its result."""
    outcome = TestRun(path)
    command = command_for(path, options)
    started = time.monotonic()
    environment = dict(os.environ)
    environment.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    try:
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace",
                                   cwd=str(REPOSITORY), env=environment, timeout=TIMEOUT_SECONDS)
        outcome.output = completed.stdout + completed.stderr
        outcome.exit_code = completed.returncode
    except subprocess.TimeoutExpired as stopped:
        outcome.output = (stopped.stdout or "") if isinstance(stopped.stdout, str) else ""
        outcome.problem = f"stopped after {TIMEOUT_SECONDS} seconds without finishing"
        outcome.seconds = time.monotonic() - started
        return outcome
    outcome.seconds = time.monotonic() - started
    lines = outcome.output.splitlines()
    result = None
    for line in lines:
        match = RESULT_LINE.match(line.strip())
        if match:
            result = match
        group = GROUP_LINE.match(line)
        if group:
            if group.group(1) == "PASS":
                outcome.groups_passed += 1
            else:
                outcome.groups_failed += 1
                if not outcome.first_failure:
                    outcome.first_failure = line[4:].strip()
        if "skipped" in line.lower() and not line.startswith(("PASS", "FAIL", "RESULT")):
            outcome.skipped += 1
    if result is None:
        tail = next((line for line in reversed(lines) if line.strip()), "no output")
        outcome.problem = f"it printed no RESULT line (exit {outcome.exit_code}); its last line: {shorten(tail, 200)}"
        return outcome
    outcome.result_text = result.group(0)
    outcome.passed = result.group(1) == "PASS" and outcome.exit_code == 0
    if result.group(1) == "PASS" and outcome.exit_code != 0:
        outcome.problem = f"it printed RESULT: PASS but exited {outcome.exit_code}"
    return outcome


def check_story(path_text, which):
    if path_text and not Path(path_text).expanduser().is_file():
        print(f'The story file for {which} was not found: "{path_text}". Give its full path, or leave the option out '
              "(the groups that need it then say skipped).")
        return False
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run every acceptance test of the Stage kit, one line each.")
    parser.add_argument("--story-catch", help="The Catch, the whole story (optional)")
    parser.add_argument("--story-long", help="The Long Places, the whole story (optional)")
    parser.add_argument("--blueprint", default=os.environ.get("STAGE_BLUEPRINT"),
                        help="the build blueprint, for the tests that can read it (optional)")
    parser.add_argument("--only", nargs="+", help="run only the tests whose file names start with these words")
    parser.add_argument("--no-render", action="store_true", help="skip the Blender renders of the grey preview test")
    parser.add_argument("--jobs", type=int, default=4, help="how many tests run at once (default 4)")
    parser.add_argument("--verbose", action="store_true", help="print each test's whole output after its line")
    options = parser.parse_args(argv)
    for attribute in ("story_catch", "story_long", "blueprint"):
        value = getattr(options, attribute)
        if value:
            setattr(options, attribute, str(Path(value).expanduser().resolve()))
    if not (check_story(options.story_catch, "The Catch") and check_story(options.story_long, "The Long Places")):
        return 2
    if options.blueprint and not Path(options.blueprint).is_file():
        print(f'The blueprint was not found: "{options.blueprint}". Leave --blueprint out to run without it.')
        return 2
    if options.story_long and not options.story_catch:
        print("--story-long is used only together with --story-catch (the tests take The Catch first).")
        return 2
    tests = find_tests(options.only)
    if not tests:
        print("No test file was found" + (f" starting with {', '.join(options.only)}." if options.only else "."))
        return 2
    stories = []
    if options.story_catch:
        stories.append("The Catch")
    if options.story_long:
        stories.append("The Long Places")
    print(f"Running {len(tests)} tests, {max(1, options.jobs)} at a time, "
          + (f"with {' and '.join(stories)}." if stories else
             "without the whole stories (their groups say skipped; give --story-catch and --story-long)."))
    started = time.monotonic()
    outcomes = []
    with ThreadPoolExecutor(max_workers=max(1, options.jobs)) as pool:
        futures = [pool.submit(run_one, path, options) for path in tests]
        for future in futures:  # printed in the fixed order, each as soon as it and those before it are done
            outcome = future.result()
            outcomes.append(outcome)
            print(outcome.line(), flush=True)
            if options.verbose:
                print(outcome.output.rstrip())
                print()
    failing = [outcome for outcome in outcomes if not outcome.passed]
    minutes = (time.monotonic() - started) / 60
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({len(outcomes)} tests, {len(failing)} failing, "
          f"{minutes:.1f} minutes)")
    return 0 if not failing else 1


if __name__ == "__main__":
    sys.exit(main())
