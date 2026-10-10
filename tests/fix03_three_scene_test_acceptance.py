"""The acceptance test of the fixes after the three-scene test of the fixed kit (Project notes 35; the fixes are
written up in Project notes 36).

What it proves, one group per problem, on small fixtures only (copies of the WP12a gold, the scene 10 excerpt and the
small reader screenplay; no group reads a whole story). It borrows its helpers from fix02_full_run_acceptance.py.
- 1 a unit's own check counts what a later unit of its step writes as not yet due: the event units' sequences and
  scene lengths; the big choices' fields wait for checkpoint B; the prices date waits for the estimate; a missing
  user field is asked through a choice;
- 3 a light at rest marks no beat, and a silence on the beat the scene's own rupture names is planned;
- 4 two shots of one person differ by the 3D angle between the cameras, height included;
- 5 the book's one-line list follows the written shot, names states and saved choices by what they are, rounds the
  floor and says a seated eye height in words;
- 6 "pause_after: none" is a value;
- 7 footage recorded "in SC06" may show any state that held during scene 6;
- 8 a speech split at a phrase over two shots: each hears a run of its words, and is timed for those words;
- 9 apply finds an inbox path written from the project folder, names an empty record, and a unit's check says when
  its inbox is not applied yet; the self-test handout prints the allowed values; the steps' "You write" lists and
  the planning instructions say what the test had to guess.

Usage: python tests/fix03_three_scene_test_acceptance.py
Standard library only.
"""

import json
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fix02_full_run_acceptance as helpers  # noqa: E402
from fix02_full_run_acceptance import (MACHINE, READER_SCREENPLAY, RESULTS, SCHEMA, SKILL, WORDS, checked,  # noqa: E402
                                       edit, gold_breakdown, gold_command_project, gold_texts, group, info, lines_of,
                                       small_project, stage, write_inbox)


# ---------------------------------------------------------------- 1: not yet due

@group("1: a scene-plan unit's own check counts the sequences and scene lengths the film unit brings as not yet due")
def event_unit_not_due(scratch):
    if not READER_SCREENPLAY.is_file():
        info("skipped: the reader fixture is not present")
        return "skip"
    project = small_project(scratch, "n1")
    code, output = stage(["handout", "U-02-SC01..SC03"], cwd=project)
    assert code == 0, output[-400:]
    handout = (project / MACHINE / "handouts" / "U-02-SC01..SC03.md").read_text(encoding="utf-8")
    assert "You write: SCENE (event, scene_intensity" in handout and "sequence, scene_intensity" not in handout
    records = "\n".join(
        f"### SCENE SC0{number}\n- event: Mara opened the back room and found scene {number}'s work undone.\n"
        f"- scene_intensity: {3 + number}\n- whose_scene: CH-MARA\n- story_day: D1\n- rhythm_class: dialogue\n"
        "- tone: tense\n- tone_undercurrent: none\n- tags: none\n" for number in (1, 2, 3))
    write_inbox(project, "U-02-SC01..SC03.md", records)
    code, output = stage(["apply", "U-02-SC01..SC03.md"], cwd=project)
    assert code == 0, output[-600:]
    code, output = stage(["check", "--unit", "U-02-SC01..SC03"], cwd=project)
    assert code == 0 and "Not yet due:" in output and " E " not in output, output[-900:]
    return "exit 0; " + next(line for line in output.splitlines() if line.startswith("Not yet due"))[:80]


@group("1: the big choices' fields wait for checkpoint B; the prices date is never asked of the AI; a user field is "
       "asked through a choice")
def checkpoint_fields_wait(scratch):
    from stage_tools.checks_form import FormContext, run_form_checks, user_field_fix
    texts = gold_texts()
    project_block = re.search(r"### PROJECT\b.*?(?=\n### )", texts["context"], re.S)
    assert project_block, "the gold has no PROJECT record"
    if "- model_facts_date:" in project_block.group(0):
        line = next(line for line in project_block.group(0).split("\n") if line.startswith("- model_facts_date:"))
        texts = edit(texts, "context", "PROJECT", line + "\n", "")
    files = helpers.parsed(texts)
    context = FormContext.for_records(SCHEMA, WORDS, files)
    problems = run_form_checks(files, context, ["FORM-05"])
    assert not any(problem.field_name == "model_facts_date" for problem in problems), [str(p) for p in problems]
    definition = SCHEMA.field("PROJECT", "frame_shape") or {}
    assert "checkpoint B" in user_field_fix(definition) and "never type it" in user_field_fix(definition)
    from stage_tools.checks_form import checkpoint_not_yet_answered
    open_choice = SimpleContext({("CHOICE", "CHOICE-009"): FakeRecord({"checkpoint": "b", "status": "open"})})
    answered = SimpleContext({("CHOICE", "CHOICE-009"): FakeRecord({"checkpoint": "b", "status": "defaulted"})})
    assert checkpoint_not_yet_answered(definition, open_choice) is True
    assert checkpoint_not_yet_answered(definition, answered) is False
    return "prices date not asked; frame_shape waits while a big choice is open; the fix says to answer the choice"


class FakeRecord:
    def __init__(self, fields):
        self.fields_by_name = fields

    def get(self, name):
        return self.fields_by_name.get(name)


class SimpleContext:
    def __init__(self, index):
        self.index = index


# ---------------------------------------------------------------- 3: light at rest, the scene's own rupture

@group("3: a light at rest marks no beat; a silence on the beat the scene's own rupture names is planned")
def rest_and_rupture(scratch):
    from stage_tools.checks_craft_reasons_words import shot_light_sound_changes
    from stage_tools.derive_fields import light_moves_in
    assert light_moves_in("A loose screw rises off the deck beside her boot and hangs in her lamplight.",
                          "lamplight") is False
    assert light_moves_in("She comes round the cage with the torch.", "torch") is True
    texts = edit(gold_texts(), "scene", "SHOT SC10-SH030", "- silence: none", "- silence: true_silence")
    run = helpers.check_run(texts)
    assert "silence" in [field for field, _ in shot_light_sound_changes(run, run.record("SC10-SH030"))]
    scene_block = re.search(r"### SCENE SC10\b.*?(?=\n### )", texts["scene"] + "\n### ", re.S).group(0)
    rupture = next(line for line in scene_block.split("\n") if line.startswith("- rupture:"))
    planned = edit(texts, "scene", "SCENE SC10", rupture,
                   "- rupture: SC10-B02 | device: true silence while she holds the lamp | breaks: the room sound")
    run = helpers.check_run(planned)
    assert "silence" not in [field for field, _ in shot_light_sound_changes(run, run.record("SC10-SH030"))]
    return "lamplight at rest; the scene's rupture plans the silence on its beat"


# ---------------------------------------------------------------- 5: the book

@group("5: the book's one-line list follows the written shot; states and saved choices are named by what they are; "
       "the floor is rounded; a seated eye height is in words")
def book_reads_plainly(scratch):
    project = gold_command_project(scratch, "n5 book")
    code, output = stage(["export", "book", "--project", project])
    assert code == 0, output[-400:]
    book = (project / "15 The breakdown" / "The breakdown.md").read_text(encoding="utf-8")
    assert not re.search(r", state \d+\b", book), re.search(r".{40}, state \d+.{20}", book).group(0)
    assert not re.search(r"cannot be shorter than \d+\.\d\d", book)
    assert not re.search(r"\b(?:seated|kneeling|eye):[A-Z]", book)
    run, breakdown = gold_breakdown(story=False)
    shot = run.record("SC10-SH150")
    moment = next(item for item in breakdown.items(shot, "moment") if item.get("shows"))
    line = next(line for line in book.splitlines() if line.startswith("- shot 150,"))
    assert moment.get("shows")[:25] in line, (line[:200], moment.get("shows")[:60])
    return line[:100]


# ---------------------------------------------------------------- 6 to 8: values, footage, split speeches

@group("6, 7, 8: 'pause_after: none' is a value; footage 'recorded: SC10' may show any state of scene 10; a speech "
       "split at a phrase is heard and timed in parts")
def values_footage_speech(scratch):
    from stage_tools.checks_coverage_time_state import recorded_position
    from stage_tools.derive_fields import speech_words_part
    pause = re.search(r"### BEAT SC10-B01\b.*?(?=\n### )", gold_texts()["scene"], re.S).group(0)
    line = next(line for line in pause.split("\n") if line.startswith("- pause_after:"))
    texts = edit(gold_texts(), "scene", "BEAT SC10-B01", line, "- pause_after: none")
    found = [str(problem) for problem in checked(texts, ["FORM-04", "FORM-05"], story=False).problems
             if "pause_after" in str(problem) and "SC10-B01" in str(problem)]
    assert not found, found
    run, breakdown = gold_breakdown()
    span = breakdown.scene_range("SC10")
    first, last = recorded_position(run, breakdown, "SC10")
    assert span and first[1] == span[0] and last[1] == span[1], (first, last, span)
    assert speech_words_part("I knew what the cage weighed.",
                             "I'd been looking at the drawings. I knew what the cage weighed. Us, I guessed.")
    assert not speech_words_part("the cage I knew", "I knew what the cage weighed.")
    assert not speech_words_part("I knew what the cage weighed.", "I knew what the cage weighed.")
    return "none accepted; recorded SC10 spans the scene; parts of a speech accepted in order only"


# ---------------------------------------------------------------- 9: apply, handouts, instructions

@group("9: apply finds an inbox path written from the project folder and names an empty record; a unit's check "
       "says when its inbox is not applied yet")
def apply_paths(scratch):
    project = gold_command_project(scratch, "n9 apply")
    write_inbox(project, "U-06-LOOKS - fix 1.md", "### LOOK LK-SAYE-KITCHEN-NIGHT\n")
    code, output = stage(["--project", project, "apply", f"{MACHINE}/inbox/U-06-LOOKS - fix 1.md"],
                         cwd=SKILL)
    assert code == 0 and "had a heading and no fields" in output, output[-600:]
    write_inbox(project, "U-06-LOOKS - fix 2.md", "### LOOK LK-SAYE-KITCHEN-NIGHT\n- stays_dark: oops\n")
    stage(["--project", project, "apply", "U-06-LOOKS - fix 2.md"])
    code, output = stage(["--project", project, "check", "--unit", "U-06-LOOKS"])
    assert "is still in the inbox, not applied" in output, output[-600:]
    return "path from the project folder found; empty record named; unapplied inbox named"


@group("9: the self-test handout prints the allowed values; the steps' 'You write' lists and the planning "
       "instructions say what the three-scene test had to guess")
def handouts_and_instructions(scratch):
    from stage_tools.read_story import selftest_shot_template
    template = selftest_shot_template(SCHEMA, SKILL, "SC99")
    assert "Allowed values" in template and "- size:" in template.split("Allowed values", 1)[1]
    steps = json.loads((SKILL / "_config" / "schema" / "steps.json").read_text(encoding="utf-8"))

    def writes(pattern):
        return next(unit for step in steps["steps"] for unit in step.get("units", [])
                    if unit.get("id_pattern") == pattern)["writes"]
    assert not any("sequence" in entry for entry in writes("U-02-<first scene>..<last scene>"))
    assert "SCENE (sequence)" in writes("U-02-FILM")
    assert "PROJECT" not in writes("U-00-START") and any(entry.startswith("RIGHTS") for entry in writes("U-00-START"))
    assert "PROJECT.fps" in writes("U-06-PLANS")
    assert "FILM-11" in next(step for step in steps["steps"] if step["step"] == 4)["checks"]
    phrases = {"stages/01 Read the story/CONTEXT.md": "Only do scenes 2, 13 and 26 for now",
               "stages/06 Film rules/CONTEXT.md": "quoting the story's words at its moment",
               "stages/04 Characters, places and things/CONTEXT.md": "the same at both ends",
               "stages/05 Continuity/CONTEXT.md": "gets a state even if nothing else changes",
               "stages/08 Shot details/CONTEXT.md": "(any time in scene 6)",
               "references/cards/13 Cutting, rhythm and sound.md": "each shot's `words:` the run it hears"}
    missing = [name for name, phrase in phrases.items() if phrase not in (SKILL / name).read_text(encoding="utf-8")]
    assert not missing, missing
    return f"allowed values printed; {len(phrases)} instructions written; the writes lists corrected"


def main():
    with tempfile.TemporaryDirectory(prefix="stage fix03 ") as temporary:
        scratch = Path(temporary)
        event_unit_not_due(scratch)
        checkpoint_fields_wait(scratch)
        rest_and_rupture(scratch)
        book_reads_plainly(scratch)
        values_footage_speech(scratch)
        apply_paths(scratch)
        handouts_and_instructions(scratch)
    failing = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({RESULTS.count(True)} passed, {failing} failing groups)")
    return 0 if not failing else 1


if __name__ == "__main__":
    sys.exit(main())
