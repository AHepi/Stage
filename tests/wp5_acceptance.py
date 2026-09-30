"""The acceptance test of work package 5: handouts and the loop (the commands next and handout;
.claude/skills/breaking-down-stories/tools/stage_tools/make_handout.py; blueprint 3's unit order, 6.1, 7.1, 14.2).

What it proves (blueprint 14.2 row WP5):
- the handouts for U-07-SC10 and U-08-SC10-B1, built from the WP12a gold fixture, stay within the Claude ceiling of
  rules/limits.json, with their card parts within card_tokens_per_unit_max; their pre-issued ID blocks are in the
  handout and in the manifest (where ID-06 reads them, and the checker stays silent on the gold); the one-line task
  comes first and last; the records hold nothing code keeps (status, locks, approval, story-point endings); the
  step-8 handout prints each list item's provisional floor (shot 150: 13.8 s), leaves banned camera choices out and
  lists the fields that need a why with their defaults;
- the same holds with stub step files and stub card parts at their target lengths (steps.json target_words, the
  longest step file of 2.3), built in a temporary copy of the skill;
- over the ceiling, a handout leaves out the example first, then the lowest-listed card parts, then trims the story
  to the unit's own lines, and then says the unit must be split;
- next follows section 3's order: on the gold it goes on to the film pass; without the scene design it names
  U-07-SC10; with only the one-line list it waits at the first group of shots, and after --checkpoint-passed the
  list is approved and next names U-08-SC10-B1 (its batches recorded in the manifest); status prints the next unit;
- on a newly read story the plan runs step 0 to step 11 in order; with the whole of The Catch and its nine groups
  of scenes (K13) steps 7 and 8 run group by group, scenes 12 and 13 split into parts and a list unit, scene 10 not.

Usage: python tests/wp5_acceptance.py [--story "<The Catch, the whole story>"]
Without the scene 10 excerpt the handouts are built without the story's lines ("skipped: story not present" for the
checks that need them); without --story the whole-story group is skipped. Standard library only.
"""

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

REPOSITORY = Path(__file__).resolve().parent.parent
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
TOOLS = SKILL / "tools"
STAGE = TOOLS / "stage.py"
sys.path.insert(0, str(TOOLS))

from stage_tools.record_format import DIVIDER_LINE, load_skill_data  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
FIXTURES = REPOSITORY / "tests" / "fixtures"
EXCERPT = FIXTURES / "The Catch - lines 397-489.txt"
SCREENPLAY_FIXTURE = FIXTURES / "reader" / "Night shift - Catch layout.txt"
GOLD_SCENE = SKILL / "examples" / "01 The Catch - scene 10.md"
GOLD_CONTEXT = SKILL / "examples" / "02 The Catch - scene 10 - context.md"
MACHINE = "For machines - do not edit"
SCENE_FILE = "11 Scenes/Scene 10 - Saye's kitchen.md"
LIMITS = json.loads((SKILL / "rules" / "limits.json").read_text(encoding="utf-8"))
STEPS = json.loads((SKILL / "schema" / "steps.json").read_text(encoding="utf-8"))
CLAUDE_CEILING = int(LIMITS["handout_tokens_max"]["claude_code"])
CARD_CAP = int(LIMITS["card_tokens_per_unit_max"]["value"])
PER_WORD = float(LIMITS["tokens_per_word_estimate"]["value"])

RESULTS = []


def report(passed, title, detail=""):
    RESULTS.append(bool(passed))
    print(f"{'PASS' if passed else 'FAIL'}  {title}" + (f": {detail}" if detail else ""), flush=True)


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
            except Exception as error:  # a fault in the tools fails the group, never the whole test
                report(False, title, f"{type(error).__name__}: {error}")
                return
            if isinstance(detail, str) and detail.startswith("skipped"):
                info(f"{title}: {detail}")
                return
            report(True, title, detail or "")
        return run
    return decorator


# ---------------------------------------------------------------- helpers

def stage(arguments, cwd=None):
    completed = subprocess.run([sys.executable, str(STAGE)] + arguments, capture_output=True, text=True,
                               encoding="utf-8", cwd=cwd or str(REPOSITORY), timeout=600,
                               env={"STAGE_LOCK_WAIT_SECONDS": "5", "PATH": "/usr/bin:/bin"})
    return completed.returncode, completed.stdout + completed.stderr


def make_gold_project(folder, story=None):
    """A project folder from the gold: the scene file in 11 Scenes and each '## From <file>' part of the context file
    as its numbered file; with a story, the story read into it as adopt reads it (without touching the records)."""
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


def list_units_found(folder):
    """What adopt does for a folder made from records (fix list C3: next works only from the units applied): list the
    units whose records the folder holds as done."""
    from stage_tools.make_handout import record_units_found
    return record_units_found(folder, SCHEMA, WORDS, CONSTANTS)


def recount(text):
    count = len(re.findall(r"^### ", text, re.MULTILINE))
    return re.sub(r"\| \d+ records?(\s*)$", f"| {count} records\\1", text.rstrip("\n")) + "\n"


def without_shots(folder):
    """The gold scene file with its SHOT and CUT records cut and its list no longer approved (step 7 just done)."""
    path = Path(folder) / SCENE_FILE
    text = path.read_text(encoding="utf-8")
    start = text.index("### SHOT SC10-SH010")
    end = text.index("END OF FILE")
    text = text[:start] + text[end:]
    text = re.sub(r"^- approved: yes\n", "", text, flags=re.MULTILINE)
    path.write_text(recount(text), encoding="utf-8")


def gold_records(text, types, shot_range=None):
    """The gold scene file's records of these types as the AI would write them: without what code keeps (status,
    locked, approved) and without the ' = <beat>' endings of story points; shots and cuts within shot_range."""
    found = []
    body = text.split(DIVIDER_LINE, 1)[1]
    for block in re.split(r"(?m)^(?=### )", body):
        match = re.match(r"### (\w+) (\S+)", block)
        if not match or match.group(1) not in types:
            continue
        if shot_range and match.group(1) in ("SHOT", "CUT"):
            number = int(re.search(r"(\d+)$", match.group(2)).group(1))
            if not shot_range[0] <= number <= shot_range[1]:
                continue
        block = re.split(r"(?m)^END OF FILE", block)[0]
        lines = [line for line in block.rstrip().splitlines() if not re.match(r"^- (status|locked|approved):", line)]
        found.append("\n".join(re.sub(r'(?<=")\s*=\s*SC\d+-B\d+', "", line) for line in lines))
    return found


def write_inbox(folder, unit_identifier, records, what):
    inbox = Path(folder) / MACHINE / "inbox" / f"{unit_identifier}.md"
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("\n\n".join(records) + f"\n\nEND OF FILE | {what} | {len(records)} records\n", encoding="utf-8")


def manifest_of(folder):
    path = Path(folder) / MACHINE / "manifest.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def estimates(text):
    """(by words, by characters): the kit's tokens_per_word_estimate, and characters / 4 as a cross-check."""
    return int(math.ceil(len(text.split()) * PER_WORD)), int(math.ceil(len(text) / 4))


def sections_of(text):
    """{heading of each '## ' section: its text} (headings inside fenced blocks do not count)."""
    found, current, lines, fence = {}, None, [], False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
        if not fence and line.startswith("## "):
            if current is not None:
                found[current] = found.get(current, "") + "\n".join(lines)
            current, lines = line[3:].strip(), []
            continue
        lines.append(line)
    if current is not None:
        found[current] = found.get(current, "") + "\n".join(lines)
    return found


def step_task(step):
    entry = next(item for item in STEPS["steps"] if item["step"] == step)
    path = SKILL / entry["step_file"]
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("**One-line task:**"):
            return line.strip()[len("**One-line task:**"):].strip()
    return None


def first_and_last(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    task_line = next((line for line in lines[:4] if line.startswith("**One-line task:**")), None)
    return task_line, lines[-1]


def check_instruction_first_and_last(text, task):
    task_line, last = first_and_last(text)
    assert task_line == f"**One-line task:** {task}", f"the handout does not open with the one-line task: {task_line}"
    assert last == f"**One-line task, again:** {task}", f"the handout does not end with the one-line task: {last}"
    heading = text.splitlines()[0]
    assert heading.startswith("# Handout "), f"first line is {heading!r}"


def check_records_hold_no_code(text):
    records = sections_of(text).get("Records you need", "")
    assert records, "no 'Records you need' section"
    for field_name in ("status", "locked", "approved"):
        assert not re.search(rf"^- {field_name}:", records, re.MULTILINE), f"the records show '- {field_name}:'"
    assert not re.search(r'"\s*=\s*SC\d+-B\d+', records), "the records keep a story point's ' = <beat>' ending"


# ---------------------------------------------------------------- the groups

def run_groups(workspace, story_path):
    excerpt = EXCERPT if EXCERPT.is_file() else None
    gold = make_gold_project(workspace / "gold", excerpt)
    if excerpt is None:
        info("skipped: story not present (the scene 10 excerpt): handouts are built without the story's lines")
    task_7, task_8 = step_task(7), step_task(8)

    @group("U-07-SC10 from the gold: within the Claude ceiling, card parts within their cap, IDs issued, instruction "
           "first and last, no records of its own output and nothing code keeps")
    def handout_7():
        code, output = stage(["handout", "U-07-SC10", "--project", str(gold)])
        assert code == 0, f"exit {code}: {output[:800]}"
        text = (gold / MACHINE / "handouts" / "U-07-SC10.md").read_text(encoding="utf-8")
        words_estimate, character_estimate = estimates(text)
        assert max(words_estimate, character_estimate) <= CLAUDE_CEILING, \
            f"{words_estimate} / {character_estimate} tokens over {CLAUDE_CEILING}"
        cards = sum(max(estimates(body)) for heading, body in sections_of(text).items()
                    if heading.startswith("Card part:"))
        assert 0 < cards <= CARD_CAP, f"card parts {cards} tokens (cap {CARD_CAP})"
        check_instruction_first_and_last(text, task_7)
        for wanted in ("SC10-B01 to SC10-B30", "SC10-SH010 to SC10-SH400", "SC10-SH990 to SC10-SH999",
                       "SC10-P1", "SC10-V1 to SC10-V9", "SC10-M01", "SC10-SU01", "CHOICE-017 to CHOICE-036"):
            assert wanted in text, f"the issued IDs lack {wanted!r}"
        if excerpt is not None:
            speeches = re.findall(r"^  - (SC10-D\d\d) ", text, re.MULTILINE)
            assert speeches == [f"SC10-D{number:02d}" for number in range(1, 17)], f"speeches listed: {speeches}"
            assert '"Not mint."' in text and "SC10-SH990: the card \"THE CATCH\" at line 488" in text
        issued = manifest_of(gold)["issued"]["U-07-SC10"]
        assert issued["BEAT"] == ["SC10-B01", "SC10-B30"], issued
        assert ["SC10-SH010", "SC10-SH400"] in issued["SHOT"] and ["SC10-SH990", "SC10-SH999"] in issued["SHOT"]
        check_records_hold_no_code(text)
        records = sections_of(text)["Records you need"]
        assert "### BEAT SC10-B01" not in records and "### SHOTLIST SC10-LIST" not in records, \
            "the records hand the unit its own output"
        for wanted in ("### SCENE SC10", "### SEQUENCE SQ03", "### CAMSYS", "### CAMRULE CR-IONA", "### RESERVE RC-01",
                       "### LOOK LK-SAYE-KITCHEN-NIGHT", "### CHARACTER CH-SAYE", "### VOICE VO-SAYE",
                       "### STATE CH-IONA.S02", "### LOCATION LOC-SAYE-KITCHEN", "### PLANT PL-08", "### RULE WR-MIRROR"):
            assert wanted in records, f"the records lack {wanted}"
        assert "- rung: SC10" in records and "- rung: SC2" not in records, "the ladder shows other scenes' rungs"
        if excerpt is not None:
            source = sections_of(text).get("The scene's lines (scene 10, 397 to 489)", "")
            assert "397  ## INT. SAYE'S HOUSE - KITCHEN - BEFORE DAWN" in source and "489" in source
        # changed after the full run (Project notes 32, problem 6): the gold is this very scene, so its handout leaves
        # the gold out rather than hand the unit its answer; any other scene's handout gets the gold's beat and list
        example = sections_of(text).get("One example from the gold", "")
        assert "the gold example is this very scene" in example, f"the gold handed to its own scene: {example[:200]}"
        from stage_tools.make_handout import Workspace, example_section
        other_scene = SimpleNamespace(step=7, scene="SC11", part=None, list_unit=False)
        example = example_section(Workspace(gold), other_scene) or ""
        assert "### BEAT SC10-B07" in example and "### SHOTLIST SC10-LIST" in example, example[:300]
        return (f"about {max(words_estimate, character_estimate):,} tokens of {CLAUDE_CEILING:,} (words x {PER_WORD}: "
                f"{words_estimate:,}; characters / 4: {character_estimate:,}); card parts {cards:,} of {CARD_CAP:,}")
    handout_7()

    @group("U-08-SC10-B1 from the gold: within the Claude ceiling, provisional floors, the camera's open values, the "
           "fields that need a why, the batch recorded in the manifest")
    def handout_8():
        code, output = stage(["handout", "U-08-SC10-B1", "--project", str(gold)])
        assert code == 0, f"exit {code}: {output[:800]}"
        text = (gold / MACHINE / "handouts" / "U-08-SC10-B1.md").read_text(encoding="utf-8")
        words_estimate, character_estimate = estimates(text)
        assert max(words_estimate, character_estimate) <= CLAUDE_CEILING, \
            f"{words_estimate} / {character_estimate} tokens over {CLAUDE_CEILING}"
        cards = sum(max(estimates(body)) for heading, body in sections_of(text).items()
                    if heading.startswith("Card part:"))
        assert 0 < cards <= CARD_CAP, f"card parts {cards} tokens"
        check_instruction_first_and_last(text, task_8)
        check_records_hold_no_code(text)
        manifest = manifest_of(gold)
        batch = manifest["batches"]["SC10"]["U-08-SC10-B1"]
        shots = [f"SC10-SH{number:03d}" for number in range(10, 10 * batch["expected"] + 1, 10)]
        assert batch["first"] == "SC10-SH010" and batch["last"] == shots[-1], batch
        assert manifest["issued"]["U-08-SC10-B1"]["SHOT"] == [shots[0], shots[-1]]
        assert "Shots: exactly these list items, one SHOT each" in text and ", ".join(shots) in text
        this_batch = sections_of(text)["This batch"].split("The scene's other list items", 1)[0]
        items = re.findall(r"^- item: (SC10-SH\d{3})", this_batch, re.MULTILINE)
        floors = re.findall(r"^  provisional floor (\d+(?:\.\d+)?) s", this_batch, re.MULTILINE)
        assert items == shots and len(floors) == len(items), f"items {items}, floors {len(floors)}"
        camera = sections_of(text)["What the camera may do here"]
        open_values = " ".join(line for line in camera.splitlines() if re.match(r"^- (size|angle|move): ", line))
        for banned in ("dutch", "dolly_zoom", "orbit", "push_in", "extreme_close_up"):
            assert banned not in open_values, f"{banned} is offered although the film bans it or saves it elsewhere"
        assert "RC-02" in camera and "not allowed in this scene" in camera
        assert re.search(r"^- move: .*\bcrane\b", camera, re.MULTILINE), "crane is not offered on the gold"
        banned_copy = workspace / "crane banned"
        shutil.copytree(gold, banned_copy)
        rules = banned_copy / "10 Film rules.md"
        rules.write_text(rules.read_text(encoding="utf-8").replace(
            "- camera_speed: real_time", "- banned: crane | why: a test bans it\n- camera_speed: real_time"),
            encoding="utf-8")
        from stage_tools.make_handout import Workspace, build_handout, unit_from_identifier
        place = Workspace(banned_copy)
        banned_text = build_handout(place, unit_from_identifier(place, "U-08-SC10-B1"), "claude_code").text()
        banned_camera = sections_of(banned_text)["What the camera may do here"]
        assert not re.search(r"^- move: .*\bcrane\b", banned_camera, re.MULTILINE), "a banned move is offered"
        assert "crane" in banned_camera, "the banned move is not named as banned"
        whys = sections_of(text)["Fields that need a why when they differ from their default (REASON-02)"]
        assert "- lens_mm: 50 (CAMSYS normal_lens_mm)" in whys and "- move: static" in whys, whys
        design = sections_of(text)["The scene design (step 7's records)"]
        assert "### BEAT SC10-B04" in design and "- dial: SC10-B07" in design
        # shot 150's floor, in whichever batch holds it
        holder = next(name for name, entry in manifest["batches"]["SC10"].items()
                      if int(entry["first"][-3:]) <= 150 <= int(entry["last"][-3:])) \
            if any(int(entry["first"][-3:]) <= 150 <= int(entry["last"][-3:])
                   for entry in manifest["batches"]["SC10"].values()) else "U-08-SC10-B2"
        code, output = stage(["handout", holder, "--project", str(gold)])
        assert code == 0, output[:600]
        other = (gold / MACHINE / "handouts" / f"{holder}.md").read_text(encoding="utf-8")
        if excerpt is not None:
            match = re.search(r"^- item: SC10-SH150 .*\n  provisional floor (\S+) s \((.*)\)", other, re.MULTILINE)
            assert match and match.group(1) == "13.8", f"shot 150's floor: {match.group(0) if match else None}"
            assert "2.0 s after the turn at beat 7" in match.group(2)
        example = sections_of(other).get("One example from the gold", "")
        assert "the gold example is this very scene" in example, f"the gold handed to its own scene: {example[:200]}"
        from stage_tools.make_handout import Workspace, example_section
        other_scene = SimpleNamespace(step=8, scene="SC11", part=None, list_unit=False)
        assert "### SHOT SC10-SH150" in (example_section(Workspace(gold), other_scene) or "")
        return (f"about {max(words_estimate, character_estimate):,} tokens of {CLAUDE_CEILING:,}; card parts {cards:,}; "
                f"{len(items)} items, each with its floor; shot 150's floor 13.8 s in {holder}"
                + ("" if excerpt else " (floors skipped: story not present)"))
    handout_8()

    @group("the checker stays silent on the gold once the handouts wrote their ID blocks (ID-06), and check --step 8 "
           "reads the batch ranges")
    def silent_checker():
        code, output = stage(["check", "--step", "8", "--scene", "SC10", "--project", str(gold)])
        id_lines = [line for line in output.splitlines() if re.match(r"^[EW] ID-0[67] ", line)]
        assert not id_lines, "\n".join(id_lines[:5])
        errors = [line for line in output.splitlines() if line.startswith("E ")]
        assert code == 0 and not errors, f"exit {code}: {errors[:5]}"
        return "no ID-06 or ID-07 line; exit 0"
    silent_checker()

    @group("with stub step files and stub card parts at their target lengths (a temporary copy of the skill)")
    def stub_handouts():
        stub_skill = make_stub_skill(workspace / "stub skill")
        from stage_tools.make_handout import Workspace, build_handout, unit_from_identifier
        lines = []
        for unit_identifier, step in (("U-07-SC10", 7), ("U-08-SC10-B1", 8)):
            place = Workspace(gold, skill_folder=stub_skill)
            unit = unit_from_identifier(place, unit_identifier)
            handout = build_handout(place, unit, "claude_code")
            text = handout.text()
            words_estimate, character_estimate = estimates(text)
            assert max(words_estimate, character_estimate) <= CLAUDE_CEILING, \
                f"{unit_identifier}: {words_estimate} / {character_estimate} tokens"
            assert handout.card_tokens() <= CARD_CAP, f"{unit_identifier}: card parts {handout.card_tokens()}"
            task = f"Stub one-line task of step {step}."
            check_instruction_first_and_last(text, task)
            stub_words = sum(len(body.split()) for heading, body in sections_of(text).items()
                             if heading.startswith("Card part:"))
            lines.append(f"{unit_identifier} about {max(words_estimate, character_estimate):,} tokens, card parts "
                         f"{handout.card_tokens():,} ({stub_words:,} words"
                         + (f"; left out: {'; '.join(handout.left_out)}" if handout.left_out else "") + ")")
        return "; ".join(lines)
    stub_handouts()

    @group("over the ceiling: the example goes first, then the records the unit only reads are put in brief, then the "
           "lowest-listed card parts, then the story is trimmed to the unit's own lines, then the unit is marked for "
           "splitting")
    def drop_order():
        from stage_tools.make_handout import Workspace, build_handout, unit_from_identifier, estimate_tokens
        full = build_handout(Workspace(gold), unit_from_identifier(Workspace(gold), "U-08-SC10-B1"), "claude_code")
        total = full.tokens()
        example = next(section for section in full.sections if section.kind == "example")
        example_tokens = estimate_tokens(example.text, PER_WORD)
        cards = [section for section in full.sections if section.kind == "card"]

        def with_ceiling(ceiling):
            limits = json.loads(json.dumps(LIMITS))
            limits["handout_tokens_max"]["claude_code"] = ceiling
            place = Workspace(gold, limits=limits)
            return build_handout(place, unit_from_identifier(place, "U-08-SC10-B1"), "claude_code")

        first = with_ceiling(total - 10)
        assert first.left_out and "example" in first.left_out[0] and len(first.left_out) == 1, first.left_out
        assert first.tokens() <= total - 10
        # changed after the full run (Project notes 32, problem 6): the records a unit only reads are put in brief
        # before any card part is left out (the full run lost the mirror rule's card part to whole records)
        last_card = cards[-1]
        second = with_ceiling(total - example_tokens - 10)
        assert "example" in second.left_out[0] and "in brief" in second.left_out[1], second.left_out
        assert not any(card.label in entry for card in cards for entry in second.left_out), \
            f"a card part went before the records were put in brief: {second.left_out}"
        third = with_ceiling(3000)
        kinds = [entry for entry in third.left_out]
        assert kinds[0].startswith("the example") and "in brief" in kinds[1], kinds
        card_places = [index for index, entry in enumerate(kinds) if any(card.label in entry for card in cards)]
        assert card_places and min(card_places) > 1 and last_card.label in kinds[min(card_places)], kinds
        assert not any(cards[0].label in entry for entry in kinds[:min(card_places) + 1]) or len(cards) == 1, \
            "the highest-listed part went first"
        if excerpt is not None:
            assert any("the story's lines outside this unit's own" in entry for entry in kinds), kinds
            source = next(section for section in third.sections if section.kind == "source")
            assert source.trimmed and "Trimmed to this unit's own lines" in source.current_text()
        assert third.too_big, "a handout still over the ceiling is not marked for splitting"
        # changed after the full run (Project notes 32, problem 6): the advice names only a split that exists; for a
        # batch of shots that is two replies (a smaller batch is not a unit next can hand out)
        assert "Still over the ceiling" in third.text() and "two replies" in third.text()
        return (f"full {total:,} tokens; ceiling {total - 10:,}: {first.left_out[0]}; ceiling "
                f"{total - example_tokens - 10:,}: {len(second.left_out)} things left out; ceiling 3,000: "
                f"{len(third.left_out)} left out and the unit marked for splitting")
    drop_order()

    @group("next on the gold: past steps 0 to 8 it names the film pass; status prints the next unit")
    def next_on_gold():
        list_units_found(gold)
        code, output = stage(["next", "--project", str(gold)])
        assert code == 0 and "check --film" in output, f"exit {code}: {output[:600]}"
        code, status = stage(["status", "--project", str(gold)])
        assert code == 0 and re.search(r"^Next: .*check --film", status, re.MULTILINE), status[-600:]
        batches = manifest_of(gold)["batches"]["SC10"]
        assert all(entry.get("received") == entry.get("expected") for entry in batches.values()), batches
        return output.splitlines()[0]
    next_on_gold()

    @group("next without the scene design names U-07-SC10 and builds its handout")
    def next_design():
        folder = make_gold_project(workspace / "no design", excerpt)
        (folder / SCENE_FILE).unlink()
        list_units_found(folder)
        code, output = stage(["next", "--project", str(folder)])
        assert code == 0 and output.startswith("Next: U-07-SC10,"), f"exit {code}: {output[:600]}"
        assert (folder / MACHINE / "handouts" / "U-07-SC10.md").is_file()
        assert "U-07-SC10" in manifest_of(folder).get("issued", {})
        return output.splitlines()[0] + " " + output.splitlines()[1]
    next_design()

    @group("the first group of shots waits for the user; --checkpoint-passed approves the list and next names "
           "U-08-SC10-B1 with its batches in the manifest")
    def next_checkpoint():
        folder = make_gold_project(workspace / "list only", excerpt)
        without_shots(folder)
        list_units_found(folder)
        code, output = stage(["next", "--project", str(folder)])
        assert code == 0 and "each group of shots" in output and "waits for the user" in output \
            and "--checkpoint-passed" in output, f"exit {code}: {output[:600]}"
        assert "- approved: yes" not in (folder / SCENE_FILE).read_text(encoding="utf-8")
        code, passed = stage(["next", "--checkpoint-passed", "--project", str(folder)])
        assert code == 0 and "Passed: each group of shots" in passed and "Next: U-08-SC10-B1," in passed, passed[:800]
        assert re.search(r"^- approved: yes$", (folder / SCENE_FILE).read_text(encoding="utf-8"), re.MULTILINE)
        manifest = manifest_of(folder)
        batches = manifest["batches"]["SC10"]
        assert set(batches) >= {"U-08-SC10-B1"} and batches["U-08-SC10-B1"]["first"] == "SC10-SH010", batches
        assert sum(entry["expected"] for entry in batches.values()) == 21, batches
        assert manifest["checkpoints"]["CHECKPOINT-C-SQ03"]["how"] == "the user replied next"
        code, again = stage(["next", "--checkpoint-passed", "--project", str(folder)])
        # changed after the full run (Project notes 32, problem 4): with nothing waiting it goes on as next does
        assert code == 0 and "No checkpoint was waiting" in again and "Next: U-08-SC10-B1," in again, again[:600]
        code, check = stage(["check", "--step", "7", "--scene", "SC10", "--project", str(folder)])
        assert not [line for line in check.splitlines() if "approved is missing" in line], "approved still missing"
        shown = ", ".join(f"{name} ({entry['expected']})" for name, entry in batches.items())
        return f"waits, then approved; batches {shown}"
    next_checkpoint()

    @group("the loop on scene 10, with the gold's own records as the AI's replies: next, handout, apply, build, check, "
           "the first group of shots, each batch, then the film pass")
    def loop():
        folder = make_gold_project(workspace / "loop", excerpt)
        (folder / SCENE_FILE).unlink()
        list_units_found(folder)
        gold_text = GOLD_SCENE.read_text(encoding="utf-8")
        code, output = stage(["next", "--project", str(folder)])
        assert code == 0 and output.startswith("Next: U-07-SC10,"), output[:400]
        design = gold_records(gold_text, ("SCENE", "PART", "BEAT", "MOVE", "SETUP", "SHOTLIST"))
        write_inbox(folder, "U-07-SC10", design, "Scene 10 design and shot list")
        code, output = stage(["apply", "U-07-SC10.md", "--project", str(folder)])
        assert code == 0, f"apply refused the design: {output[:1500]}"
        code, output = stage(["build", "--project", str(folder)])
        assert code == 0, f"build after the design: {output[:800]}"
        code, output = stage(["check", "--step", "7", "--scene", "SC10", "--project", str(folder)])
        errors = [line for line in output.splitlines() if line.startswith("E ")]
        before = [line for line in errors if not re.match(r"^E FORM-05 SC10-LIST approved is missing", line)]
        assert not before, f"check --step 7 before the checkpoint: {before[:4]}"
        if errors:
            info("check --step 7 before the first group of shots is passed: 'E FORM-05 SC10-LIST approved is missing' "
                 "(code writes approved only when the group is passed; see the WP5 build log)")
        code, output = stage(["next", "--project", str(folder)])
        assert "each group of shots" in output and "waits for the user" in output, output[:400]
        code, output = stage(["next", "--checkpoint-passed", "--project", str(folder)])
        assert code == 0 and "Next: U-08-SC10-B1," in output, output[:600]
        code, output = stage(["check", "--step", "7", "--scene", "SC10", "--project", str(folder)])
        assert code == 0, f"check --step 7 after the checkpoint: {output[:800]}"
        batches = manifest_of(folder)["batches"]["SC10"]
        applied = []
        for unit_identifier in sorted(batches, key=lambda name: int(name.rsplit("B", 1)[1])):
            entry = batches[unit_identifier]
            first, last = int(entry["first"][-3:]), int(entry["last"][-3:])
            code, output = stage(["handout", unit_identifier, "--project", str(folder)])
            assert code == 0, output[:600]
            shots = gold_records(gold_text, ("SHOT", "CUT"), (first, last))
            write_inbox(folder, unit_identifier, shots, f"Scene 10 shots {first:03d}-{last:03d}")
            code, output = stage(["apply", f"{unit_identifier}.md", "--project", str(folder)])
            assert code == 0, f"apply refused {unit_identifier}: {output[:1500]}"
            code, output = stage(["build", "--project", str(folder)])
            assert code == 0, f"build after {unit_identifier}: {output[:800]}"
            code, output = stage(["check", "--step", "8", "--scene", "SC10", "--project", str(folder)])
            errors = [line for line in output.splitlines() if line.startswith("E ")]
            assert not errors, f"check --step 8 after {unit_identifier}: {errors[:4]}"
            applied.append(f"{unit_identifier} ({len(shots)} records)")
        received = manifest_of(folder)["batches"]["SC10"]
        assert all(entry.get("received") is not None for entry in received.values()), received
        code, output = stage(["next", "--project", str(folder)])
        assert "check --film" in output, output[:400]
        return "design applied and checked; " + ", ".join(applied) + " applied and checked; next: the film pass"
    loop()

    @group("a newly read story: the plan runs from step 0 to step 11 in section 3's order and next names the self-test")
    def fresh_plan():
        if not SCREENPLAY_FIXTURE.is_file():
            return "skipped: fixture not present"
        root = workspace / "fresh"
        root.mkdir()
        code, output = stage(["new", str(SCREENPLAY_FIXTURE), "--into", str(root)], cwd=str(root))
        assert code == 0, output[:600]
        project = next(path for path in root.iterdir() if path.is_dir())
        code, output = stage(["read", "--project", str(project)])
        assert code == 0, output[:600]
        from stage_tools.make_handout import Workspace, mark_done
        place = Workspace(project)
        units = mark_done(place, place.plan())
        steps = [unit.step for unit in units]
        assert steps == sorted(steps), f"steps out of order: {steps}"
        names = [unit.identifier for unit in units]
        assert names[:6] == ["U-00-SELFTEST", "U-00-START", "CHECKPOINT-RIGHTS", "code: read", "U-01-ODDLINES",
                             "CHECKPOINT-A"], names[:6]
        assert names.index("CHECKPOINT-B") < names.index("U-06-CAMERA") < names.index("U-07-SC01")
        code, output = stage(["next", "--project", str(project)])
        assert code == 0 and "U-00-SELFTEST" in output and "selftest --prepare" in output, output[:500]
        return f"{len(units)} units and checkpoints; next: the self-test"
    fresh_plan()

    @group("The Catch: steps 7 and 8 run group by group (K13's nine groups); scenes 12 and 13 in parts and a list "
           "unit, scene 10 in one unit")
    def catch_order():
        if story_path is None:
            return "skipped: story not present (give --story <The Catch>)"
        root = workspace / "catch"
        root.mkdir()
        code, output = stage(["new", str(story_path), "--into", str(root)], cwd=str(root))
        assert code == 0, output[:600]
        project = next(path for path in root.iterdir() if path.is_dir())
        code, output = stage(["read", "--project", str(project)])
        assert code == 0, output[:600]
        example = STEPS["unit_order"]["steps_7_and_8"]["example_the_catch"]
        records = []
        for sequence, scenes in example["sequences"].items():
            records += [f"### SEQUENCE {sequence}", f"- title: group {int(sequence[2:])}", f"- scenes: {scenes}",
                        "- status: draft", "- locked: no", ""]
        count = len(example["sequences"])
        (project / "05 Story plan.md").write_text(
            f"# Story plan\n\n{DIVIDER_LINE}\n\n" + "\n".join(records) + f"\nEND OF FILE | Story plan | {count} "
            "records\n", encoding="utf-8")
        from stage_tools.make_handout import Workspace
        place = Workspace(project)
        loop = [unit for unit in place.plan() if unit.step in (7, 8)]
        order = []
        for unit in loop:
            if unit.kind == "checkpoint":
                order.append("checkpoint C (blocks)" if unit.blocks else "checkpoint C (reports)")
            elif unit.step == 8:
                if not order or not order[-1].startswith(f"U-08-{unit.scene}"):
                    order.append(f"U-08-{unit.scene}")
            else:
                order.append(unit.identifier)
        expected_start = ["U-07-SC01", "U-07-SC02", "U-07-SC03", "U-07-SC04", "U-07-SC05", "checkpoint C (blocks)",
                          "U-08-SC01", "U-08-SC02", "U-08-SC03", "U-08-SC04", "U-08-SC05", "U-07-SC06",
                          "checkpoint C (reports)", "U-08-SC06", "U-07-SC07", "U-07-SC08", "U-07-SC09", "U-07-SC10",
                          "checkpoint C (reports)", "U-08-SC07", "U-08-SC08", "U-08-SC09", "U-08-SC10", "U-07-SC11",
                          "U-07-SC12-P1", "U-07-SC12-P2", "U-07-SC12-LIST", "U-07-SC13-P1", "U-07-SC13-P2",
                          "U-07-SC13-LIST", "checkpoint C (reports)", "U-08-SC11"]
        assert order[:len(expected_start)] == expected_start, f"order: {order[:36]}"
        assert order.count("checkpoint C (blocks)") == 1 and order.count("checkpoint C (reports)") == 8
        splits = sorted({unit.scene for unit in loop if unit.part})
        parts = {unit.identifier: unit.lines for unit in loop if unit.part}
        assert "SC12" in splits and "SC13" in splits and "SC10" not in splits, splits
        return f"{len(order)} entries; scenes split into parts: {', '.join(splits)}; part lines {parts}"
    catch_order()


def make_stub_skill(folder):
    """A copy of the skill's data (schema, rules, templates, examples) with stub step files at the longest length of
    2.3 (1,800 words, their chat twin included) and stub cards whose parts are at steps.json's target_words (a whole
    card at its type's longest length)."""
    folder = Path(folder)
    for name in ("schema", "rules", "templates", "examples"):
        shutil.copytree(SKILL / name, folder / name)
    filler = ("Stub words stand in for a real part of the kit at its target length so that the handout budget can be "
              "measured before the real file exists. ").split()

    def words(count):
        return " ".join(filler[index % len(filler)] for index in range(count))
    (folder / "steps").mkdir()
    for entry in STEPS["steps"]:
        step = entry["step"]
        sections = ["Purpose", "When it runs", "Inputs", "Outputs", "Card parts to open", "Procedure",
                    "Record template", "IDs you will be given", "Batch and chunk rules", "Self-check", "The report",
                    "Checkpoint", "How to redo", "If you cannot run code"]
        each = (1800 - 40) // len(sections)
        body = [f"# Step {step}. {entry['name']}", "", f"**One-line task:** Stub one-line task of step {step}.", "",
                "Quote the one-line task back, word for word, before you do anything else.", ""]
        for section in sections:
            body += [f"## {section}", "", words(each), ""]
        body += [f"**One-line task, again:** Stub one-line task of step {step}.", ""]
        path = folder / entry["step_file"]
        path.write_text("\n".join(body), encoding="utf-8")
    (folder / "cards").mkdir()
    (folder / "reference").mkdir()
    whole_words = {"department": 2000, "situation": 1000, "production": 1800, "reference": 1000}
    for code, card in STEPS["cards"].items():
        parts = [(part["heading"], part.get("target_words", 300)) for name, part in card["parts"].items()
                 if name != "whole" and part.get("heading")]
        total = whole_words.get(card.get("type"), 2000)
        rest = max(0, total - sum(count for _, count in parts))
        body = [f"# Card {code}. Stub", ""]
        for heading, count in parts:
            body += [f"## {heading}", "", words(count), ""]
        body += ["## The rest of the card", "", words(rest), ""]
        (folder / card["file"]).write_text("\n".join(body), encoding="utf-8")
    return folder


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--story", help="the whole story (The Catch), for the group that plans its steps 7 and 8")
    arguments = parser.parse_args()
    story_path = Path(arguments.story) if arguments.story else None
    if story_path is not None and not story_path.is_file():
        info(f"skipped: story not present ({story_path.name}); the whole-story group is skipped")
        story_path = None
    workspace = Path(tempfile.mkdtemp(prefix="wp5 "))
    try:
        run_groups(workspace, story_path)
    finally:
        shutil.rmtree(workspace, ignore_errors=True)
    failing = RESULTS.count(False)
    print(f"RESULT: {'PASS' if failing == 0 else 'FAIL'} ({failing} failing groups)")
    return 0 if failing == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
