"""The acceptance test of the plan-level fixes after the H3 handover (Project notes 42; the build plan is note 43,
work package B): stop asking for stillness, cut at contact, and check that the plan makes physical sense.

What it proves, on small fixtures only: copies of the WP12a gold (examples/01 and 02, scene 10) and a generic test
scene written here in neutral words (a climber in a 2.4 metre shaft, a patient, a guard). No group reads a whole
story; no group reads the clip file or its code.

Groups:
- B1 the constants: hold_action_every_s replaces hold_needs_still_s; the physical sense numbers are there, each with
  a meaning and a source and marked as a judgement;
- B1 CRAFT-26 turned round: a 7-second moment with one action is flagged, with four actions it is not; a pause held
  on picture needs its last moments filled;
- B1 the old still sub-part: a breakdown that still writes it, with enough actions, raises nothing about stillness,
  and no check asks for it;
- B1 CRAFT-27: stillness words in a moment, a does or an end are flagged; energy: still and quoted story words are
  not;
- B2 CRAFT-28: a contact and its result in one shot are flagged; the same pair split across a cut is not;
- B3 PHYS-01 to PHYS-11: each flags its generic slip (a 2.4 metre shaft round a 2 metre car; a heavy 30 centimetre
  flashlight held in the teeth; a line spoken round it; a strap cut with nothing; cover under an open grid roof; a
  rung that rolls; a weak man holding up a heavy man; a weak man running; a chair wedged under a door handle; a
  door kicked open; more than two things in one person's hands; a tiny thing given emphasis in a wide shot; a thing
  out of reach); each line is a warning that asks a question;
- the gold scene 10 (and its chat-saved copy) raises none of the new warnings, and none of the old checks either;
- the new checks are warnings, registered with a plain sentence, listed for steps 4, 7 and 8 in schema/steps.json,
  and their titles say they are judgements (J);
- no new or changed file holds an email address.

Usage: python tests/fix06b_plan_checks_acceptance.py
Standard library only.
"""

import json
import re
import sys
import tempfile
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
TOOLS = SKILL / "tools"
sys.path.insert(0, str(TOOLS))

from stage_tools import check_records  # noqa: E402
from stage_tools.record_format import DIVIDER_LINE, load_skill_data, parse_file  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
GOLD_FILES = {"context": SKILL / "examples" / "02 The Catch - scene 10 - context.md",
              "scene": SKILL / "examples" / "01 The Catch - scene 10.md"}
CHAT_FOLDER = REPOSITORY / "tests" / "fixtures" / "chat saved scene 10"
EXCERPT = REPOSITORY / "tests" / "fixtures" / "The Catch - lines 397-489.txt"
NEW_CHECKS = ["CRAFT-26", "CRAFT-27", "CRAFT-28"] + [f"PHYS-{number:02d}" for number in range(1, 12)]
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
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


# ---------------------------------------------------------------- fixtures

def gold_texts():
    return {name: path.read_text(encoding="utf-8") for name, path in GOLD_FILES.items()}


def edit(texts, name, heading, find, replace):
    """Replace a text found exactly once inside one record of a copy of the gold."""
    text = texts[name]
    start = text.index(f"### {heading}")
    end = text.find("\n### ", start + 4)
    end = len(text) if end < 0 else end
    block = text[start:end]
    assert block.count(find) == 1, f"{heading} holds {find!r} {block.count(find)} times"
    texts[name] = text[:start] + block.replace(find, replace) + text[end:]
    return texts


def record_file(text, title):
    count = len(re.findall(r"^### ", text, re.MULTILINE))
    return f"# {title}\n\n{DIVIDER_LINE}\n\n{text.strip()}\n\nEND OF FILE | {title} | {count} records\n"


# A generic test scene in neutral words: a climber in a narrow shaft, a weak patient, a heavy guard. Each shot holds
# one slip a physical sense check must catch.
GENERIC_WORLD = """
### CHARACTER CH-TEST-CLIMBER The climber
- names: CLIMBER, THE CLIMBER
- fixed_description: the climber, a lean woman in her thirties in grey overalls and a dark knitted cap
- height_m: 1.7
- build: lean and strong

### CHARACTER CH-TEST-PATIENT The patient
- names: PATIENT, THE PATIENT
- fixed_description: the patient, a thin man in his forties in a pale hospital gown
- height_m: 1.75
- build: thin, weak from the drug, his knees unsteady

### CHARACTER CH-TEST-GUARD The guard
- names: GUARD, THE GUARD
- fixed_description: the guard, a tall, heavy, broad man in a dark uniform
- height_m: 1.92
- build: tall, heavy and broad

### LOCATION LOC-TEST-SHAFT The shaft
- headings: INT. SHAFT - NIGHT
- dressing: a bare steel car whose roof is a grid of flat bars
- size: [2.4, 2.4, 20.0]
- object: CAR | at: [1.2, 1.2] | size: [2.0, 2.0, 2.4] | base: 0 | material: a bare steel car | meaning: the car | furniture: none
- object: LADDER | at: [0.05, 1.2] | size: [0.1, 0.6, 20.0] | base: 0 | material: steel rungs on the wall | meaning: the way up | furniture: none
- object: HATCH | at: [1.2, 2.35] | size: [0.4, 0.1, 0.8] | base: 0 | material: a small steel hatch | meaning: the way out | furniture: none
- object: ROPES | at: [2.3, 2.3] | size: [0.05, 0.05, 20.0] | base: 0 | material: steel cables | meaning: what the car hangs from | furniture: none
- mark: CLIMB | at: [0.15, 1.6]

### PROP PR-TEST-FLASHLIGHT The flashlight
- names: flashlight, the flashlight
- fixed_description: a heavy black metal flashlight about 30 centimetres long
- real_size: [0.05, 0.05, 0.3]

### PROP PR-TEST-STRAP The strap
- names: the strap
- fixed_description: a grey webbing strap with a steel buckle
- real_size: [0.04, 0.6, 0.01]

### PROP PR-TEST-BOLT The bolt
- names: the bolt
- fixed_description: a small steel bolt
- real_size: [0.02, 0.02, 0.05]

### PROP PR-TEST-ROPE The rope
- names: the rope
- fixed_description: a coil of blue rope
- real_size: [0.3, 0.3, 0.1]

### PROP PR-TEST-HOOK The hook
- names: the hook
- fixed_description: a steel hook on a short handle
- real_size: [0.05, 0.25, 0.02]

### PROP PR-TEST-BAG The bag
- names: the bag
- fixed_description: a canvas tool bag
- real_size: [0.4, 0.2, 0.25]

### SCENE SC90 The shaft
- location: LOC-TEST-SHAFT
- characters: CH-TEST-CLIMBER, CH-TEST-PATIENT, CH-TEST-GUARD
- start: CH-TEST-CLIMBER | at: CLIMB | faces: [1.0, 0.0] | posture: standing
- start: CH-TEST-PATIENT | at: [1.2, 1.2] | faces: [0.0, 1.0] | posture: standing
- start: CH-TEST-GUARD | at: [1.6, 1.2] | faces: [0.0, 1.0] | posture: standing

### SPEECH SC90-D01 Keep going
- speaker: CH-TEST-CLIMBER
- text: Keep going.
- parenthetical: round the flashlight

### SHOT SC90-SH010 Teeth
- size: medium
- subject: CH-TEST-CLIMBER | does: climbs the rungs with the flashlight in her teeth
- thing: PR-TEST-FLASHLIGHT | emphasis: 1
- hear: SC90-D01 | speaker: on_screen | at: 1
- screen_time: 3
- moment: 0-3 | shows: she climbs two rungs, breathing hard through her nose; her right hand closes on the next rung

### SHOT SC90-SH020 Strap
- size: medium_close_up
- subject: CH-TEST-CLIMBER | does: cuts the strap and pulls it free
- thing: PR-TEST-STRAP | emphasis: 1
- screen_time: 3
- moment: 0-3 | shows: she cuts the strap; it falls away

### SHOT SC90-SH030 Cover
- size: wide
- subject: CH-TEST-PATIENT | does: crouches in the corner of the car
- subject: CH-TEST-GUARD | does: crouches beside him
- screen_time: 3
- moment: 0-3 | shows: the two men take cover in the corner of the car from the shots coming down

### SHOT SC90-SH040 Rung
- size: close_up
- subject: CH-TEST-CLIMBER | does: grips the broken rung
- screen_time: 3
- moment: 0-3 | shows: the rung rolls under her hand like a rolling pin

### SHOT SC90-SH050 Holding up
- size: medium
- subject: CH-TEST-PATIENT | does: holds up the guard against the grid
- subject: CH-TEST-GUARD | does: hangs off his shoulder
- screen_time: 3
- moment: 0-3 | shows: the patient takes the guard's weight

### SHOT SC90-SH060 Running
- size: wide
- subject: CH-TEST-PATIENT | does: runs to the hatch
- screen_time: 3
- moment: 0-3 | shows: the patient runs the length of the car

### SHOT SC90-SH070 Brace
- size: medium
- subject: CH-TEST-GUARD | does: wedges a chair under the door handle
- screen_time: 3
- moment: 0-3 | shows: the guard wedges a chair under the door handle

### SHOT SC90-SH080 Kick
- size: medium
- subject: CH-TEST-GUARD | does: kicks the gate open
- screen_time: 3
- moment: 0-3 | shows: the guard kicks the gate open

### SHOT SC90-SH090 Hands
- size: medium
- subject: CH-TEST-CLIMBER | does: holds the rope, the hook and the bag
- thing: PR-TEST-ROPE | emphasis: 1
- thing: PR-TEST-HOOK | emphasis: 1
- thing: PR-TEST-BAG | emphasis: 1
- screen_time: 3
- moment: 0-3 | shows: she shifts her grip on all three

### SHOT SC90-SH100 Bolt
- size: wide
- subject: CH-TEST-CLIMBER | does: looks down the shaft
- thing: PR-TEST-BOLT | emphasis: 2 | at: on the car's roof
- screen_time: 3
- moment: 0-3 | shows: she looks down at the car below, breathing hard

### SHOT SC90-SH110 Reach
- size: medium
- subject: CH-TEST-CLIMBER | does: holds on with one hand
- screen_time: 3
- moment: 0-3 | shows: the climber takes hold of the ropes; she breathes out
"""

# Each physical sense check, the generic record it must flag, and the field.
PHYSICAL_SLIPS = [
    ("PHYS-01", "LOC-TEST-SHAFT", "mark", "a mark in the gap between a 2 metre car and a 2.4 metre shaft"),
    ("PHYS-01", "LOC-TEST-SHAFT", "object", "a ladder with 0.1 metres clear in front of it, a 0.4 metre hatch"),
    ("PHYS-02", "SC90-SH010", "subject", "a heavy 30 centimetre flashlight held in the teeth"),
    ("PHYS-03", "SC90-D01", "parenthetical", "a line spoken round the flashlight"),
    ("PHYS-03", "SC90-SH010", "subject", "the climber speaks on screen with the flashlight in her teeth"),
    ("PHYS-04", "SC90-SH110", "moment", "the ropes out of reach across the shaft"),
    ("PHYS-05", "SC90-SH020", "moment", "a strap cut with nothing to cut it"),
    ("PHYS-06", "SC90-SH030", "moment", "cover under an open grid roof"),
    ("PHYS-07", "SC90-SH040", "moment", "a rung that rolls"),
    ("PHYS-08", "SC90-SH050", "subject", "a weak man holding up a heavy man"),
    ("PHYS-08", "SC90-SH060", "moment", "a weak man running"),
    ("PHYS-09", "SC90-SH070", "moment", "a chair wedged under a door handle"),
    ("PHYS-09", "SC90-SH080", "moment", "a gate kicked open"),
    ("PHYS-10", "SC90-SH090", "subject", "three things in one person's hands"),
    ("PHYS-11", "SC90-SH100", "thing", "a 5 centimetre bolt given emphasis 2 in a wide shot"),
]


def write_files(folder, texts, extra=None):
    folder.mkdir(parents=True, exist_ok=True)
    paths = []
    for name in ("context", "scene"):
        path = folder / GOLD_FILES[name].name
        path.write_text(texts[name], encoding="utf-8")
        paths.append(path)
    if extra:
        path = folder / "Scene 90 - the shaft.md"
        path.write_text(record_file(extra, "Scene 90 - the shaft"), encoding="utf-8")
        paths.append(path)
    return paths


def run(paths, check_ids, story=True, step=None):
    check_records.load_check_families()
    source = check_records.StorySource.from_file(str(EXCERPT), CONSTANTS) if story and EXCERPT.is_file() else None
    files = [parse_file(path, path.name, SCHEMA) for path in paths]
    result = check_records.run_checks(files, SCHEMA, WORDS, CONSTANTS, story=source, check_ids=check_ids, step=step)
    assert not result.crashed and not result.families_broken, (result.crashed, result.families_broken)
    return result


def lines_of(result, check_id=None):
    """The problem lines of a run, the scene outside the gold project's scope (the generic scene 90) included."""
    return [problem for problem in result.all_problems if check_id is None or problem.check_id == check_id]


# ---------------------------------------------------------------- the groups

def main():
    temporary_folder = tempfile.TemporaryDirectory(prefix="fix06b-")
    temporary = Path(temporary_folder.name)
    counter = {"n": 0}

    def fresh(texts, extra=None):
        counter["n"] += 1
        return write_files(temporary / f"case {counter['n']:02d}", texts, extra)

    @group("B1: hold_action_every_s (2.0 s) replaces hold_needs_still_s; the physical sense numbers are in "
           "rules/constants.json with a meaning, a source and the judgement mark")
    def constants():
        table = CONSTANTS["constants"]
        assert "hold_needs_still_s" not in table, "the old constant is still there"
        entry = table["hold_action_every_s"]
        assert entry["value"] == 2.0 and entry.get("judgement") is True, entry
        wanted = {"body_pass_clearance_m": 0.5, "body_climb_clearance_m": 0.75, "teeth_hold_length_max_m": 0.2,
                  "reach_share_of_height": 0.6, "visible_thing_emphasis_min": 2, "tall_person_height_m": 1.85}
        wrong = [f"{name} {table.get(name, {}).get('value')!r}" for name, value in wanted.items()
                 if table.get(name, {}).get("value") != value]
        assert not wrong, wrong
        sizes = table["visible_thing_min_size_m_by_size"]["value"]
        assert sizes.get("wide") == 0.1, sizes
        for name in list(wanted) + ["visible_thing_min_size_m_by_size", "hold_action_every_s"]:
            for key in ("value", "unit", "meaning", "source"):
                assert table[name].get(key) not in (None, ""), f"{name}.{key}"
            assert table[name].get("judgement") is True, f"{name} is not marked a judgement"
        readers = [path.name for path in (TOOLS / "stage_tools").glob("*.py")
                   if "hold_needs_still_s" in path.read_text(encoding="utf-8")
                   and path.name not in ("compile_prompts.py",)]
        assert not readers, f"still reading the old constant: {readers}"
        return f"hold_action_every_s 2.0 s; {len(wanted) + 1} physical sense numbers, each a judgement with a source"

    @group("B1: CRAFT-26 turned round: a 7-second moment with one action is flagged, with four actions it is not")
    def held_moment():
        one = edit(gold_texts(), "scene", "SHOT SC10-SH150",
                   "- moment: 8-15 | shows: swallows once; breathes out slowly through her nose; blinks; her lips press "
                   "together; a slow breath in, her eyes on Saye; she blinks again",
                   "- moment: 8-15 | shows: listens; swallows once")
        lines = lines_of(run(fresh(one), ["CRAFT-26"]), "CRAFT-26")
        hits = [line for line in lines if line.record == "SC10-SH150" and line.field_name == "moment"
                and "8-15" in line.what]
        assert hits, [str(line) for line in lines]
        assert "1 small action" in hits[0].what and "at least 3" in hits[0].what, hits[0]
        assert hits[0].level == "W", hits[0]
        assert "stay still" in hits[0].fix and "never a list" in hits[0].fix, hits[0].fix
        four = edit(gold_texts(), "scene", "SHOT SC10-SH150",
                    "- moment: 8-15 | shows: swallows once; breathes out slowly through her nose; blinks; her lips "
                    "press together; a slow breath in, her eyes on Saye; she blinks again",
                    "- moment: 8-15 | shows: swallows once; breathes out through her nose; blinks; then her lips "
                    "press together")
        lines = lines_of(run(fresh(four), ["CRAFT-26"]), "CRAFT-26")
        assert not lines, [str(line) for line in lines]
        stillness = edit(gold_texts(), "scene", "SHOT SC10-SH150",
                         "- moment: 8-15 | shows: swallows once; breathes out slowly through her nose; blinks; her lips "
                         "press together; a slow breath in, her eyes on Saye; she blinks again",
                         "- moment: 8-15 | shows: swallows once; her head stays still; her hands do not move; she "
                         "waits")
        lines = lines_of(run(fresh(stillness), ["CRAFT-26"]), "CRAFT-26")
        assert lines and "1 small action" in lines[0].what, [str(line) for line in lines]
        return f"one action: {hits[0]}; four actions: silent; a list of still parts counts as no action"

    @group("B1: a pause held on picture needs the shot's last moments to carry small actions")
    def held_pause():
        texts = edit(gold_texts(), "scene", "SHOT SC10-SH190",
                     "- moment: 7.5-9 | shows: Iona's eyes go to Jude and she steps aside, toward him; Eli is in plain "
                     "sight again",
                     "- moment: 7.5-9 | shows: nobody moves")
        texts = edit(texts, "scene", "SHOT SC10-SH190",
                     "- moment: 4-7.5 | shows: Saye waits, her eyes on Iona; Iona swallows, her hands open at her "
                     "sides; Jude's chest rises and falls on the table",
                     "- moment: 4-7.5 | shows: Saye waits")
        lines = [line for line in lines_of(run(fresh(texts), ["CRAFT-26"]), "CRAFT-26")
                 if "pause of 3 s" in line.what]
        assert lines and lines[0].record == "SC10-SH190", [str(line) for line in lines]
        return str(lines[0])

    @group("B1: a breakdown that still writes the old still sub-part, with enough actions, raises nothing about "
           "stillness; FORM accepts it and no check asks for it")
    def old_still_sub_part():
        texts = edit(gold_texts(), "scene", "SHOT SC10-SH150", "| energy: held | display: 1 |",
                     "| energy: held | display: 1 | still: head, hands, torso |")
        texts = edit(texts, "scene", "SHOT SC10-SH010", "| tactic: hiding | energy: still | display: 1 |",
                     "| tactic: hiding | energy: still | display: 1 | still: whole_body |")
        form = [f"FORM-{number:02d}" for number in range(1, 14)]
        result = run(fresh(texts), ["CRAFT-15", "CRAFT-26", "CRAFT-27"] + form)
        lines = [str(line) for line in result.problems]
        assert not lines, lines
        definition = next(part for field in SCHEMA.record_types["SHOT"]["fields"] if field["name"] == "subject"
                          for part in field["sub_parts"] if part["key"] == "still")
        assert "depth" not in definition and "old field" in definition["meaning"].lower(), definition
        gold = run(fresh(gold_texts()), form)
        assert not [str(line) for line in gold.problems if "still" in line.what], [str(line) for line in gold.problems]
        return "silent with still written; the gold without it passes FORM-05 at standard depth"

    @group("B1: CRAFT-27 flags stillness words in a moment, a does and an end; energy: still and quoted story words "
           "are left alone")
    def stillness_words():
        texts = edit(gold_texts(), "scene", "SHOT SC10-SH110",
                     "- moment: 0-3.5 | shows: he twists the cap; it will not turn; he stops",
                     "- moment: 0-3.5 | shows: he twists the cap; it will not turn; he stays still")
        texts = edit(texts, "scene", "SHOT SC10-SH110", "does: lies on the table between them, his chest rising and "
                     "falling", "does: lies motionless on the table between them")
        texts = edit(texts, "scene", "SHOT SC10-SH110", "- end: Eli by the fridge, the open bottle in one hand, eyes "
                     "on Saye", "- end: Eli frozen by the fridge, nobody moves")
        lines = lines_of(run(fresh(texts), ["CRAFT-27"]), "CRAFT-27")
        fields = sorted({line.field_name for line in lines if line.record == "SC10-SH110"})
        assert fields == ["end", "moment", "subject"], [str(line) for line in lines]
        assert all(line.level == "W" for line in lines), lines
        quoted = edit(gold_texts(), "scene", "SHOT SC10-SH110",
                      "- moment: 0-3.5 | shows: he twists the cap; it will not turn; he stops",
                      '- moment: 0-3.5 | shows: he twists the cap; it will not turn; he stops; "Stay still."')
        quoted = edit(quoted, "scene", "SHOT SC10-SH110", "- end: Eli by the fridge, the open bottle in one hand",
                      "- end: Eli by the fridge, still holding the open bottle in one hand")
        lines = lines_of(run(fresh(quoted), ["CRAFT-27"]), "CRAFT-27")
        assert not lines, [str(line) for line in lines]
        return f"{len(lines_of(run(fresh(texts), ['CRAFT-27']), 'CRAFT-27'))} lines on moment, does and end; " \
               "energy: still, a quoted line and 'still holding' pass"

    @group("B2: CRAFT-28 flags a contact and its result in one shot; the pair split across a cut is the fix and "
           "passes")
    def contact_cut():
        together = edit(gold_texts(), "scene", "SHOT SC10-SH110",
                        "- moment: 3.5-6 | shows: he twists it the other way and it comes off; his eyes come up to "
                        "Saye",
                        "- moment: 3.5-6 | shows: he kicks the chair by the fridge; the chair topples")
        lines = lines_of(run(fresh(together), ["CRAFT-28"]), "CRAFT-28")
        assert lines and lines[0].record == "SC10-SH110" and lines[0].level == "W", [str(line) for line in lines]
        assert "different size or angle" in lines[0].fix and "sound" in lines[0].fix, lines[0].fix
        next_moment = edit(gold_texts(), "scene", "SHOT SC10-SH110",
                           "- moment: 0-3.5 | shows: he twists the cap; it will not turn; he stops",
                           "- moment: 0-3.5 | shows: he twists the cap; he kicks the chair by the fridge")
        next_moment = edit(next_moment, "scene", "SHOT SC10-SH110",
                           "- moment: 3.5-6 | shows: he twists it the other way and it comes off; his eyes come up "
                           "to Saye", "- moment: 3.5-6 | shows: the chair topples onto the floor")
        assert lines_of(run(fresh(next_moment), ["CRAFT-28"]), "CRAFT-28"), "cause and effect in two moments of one shot"
        split = edit(gold_texts(), "scene", "SHOT SC10-SH110",
                     "- moment: 3.5-6 | shows: he twists it the other way and it comes off; his eyes come up to Saye",
                     "- moment: 3.5-6 | shows: he twists it the other way; he kicks the chair by the fridge")
        split = edit(split, "scene", "SHOT SC10-SH120",
                     "- moment: 0-2.5 | shows: Saye holds Eli's look, then her head turns to the flask on the counter",
                     "- moment: 0-2.5 | shows: the chair topples onto the floor; Saye's head turns to the flask on "
                     "the counter")
        lines = lines_of(run(fresh(split), ["CRAFT-28"]), "CRAFT-28")
        assert not lines, [str(line) for line in lines]
        negated = edit(gold_texts(), "scene", "SHOT SC10-SH110",
                       "- moment: 3.5-6 | shows: he twists it the other way and it comes off; his eyes come up to Saye",
                       "- moment: 3.5-6 | shows: he kicks the chair; it does not fall")
        assert not lines_of(run(fresh(negated), ["CRAFT-28"]), "CRAFT-28"), "a negated effect was flagged"
        return f"together: {lines_of(run(fresh(together), ['CRAFT-28']), 'CRAFT-28')[0]}; split across the cut and " \
               "negated: silent"

    @group("B3: each physical sense check flags its generic slip, as a warning that asks a question")
    def physical_slips():
        result = run(fresh(gold_texts(), GENERIC_WORLD), [f"PHYS-{number:02d}" for number in range(1, 12)])
        found = lines_of(result)
        missing, wrong = [], []
        for check_id, record, field_name, about in PHYSICAL_SLIPS:
            hits = [line for line in found if line.check_id == check_id and line.record == record
                    and line.field_name == field_name]
            if not hits:
                missing.append(f"{check_id} {record} {field_name} ({about})")
                continue
            if hits[0].level != "W" or "?" not in hits[0].what or not hits[0].fix.startswith("Fix:"):
                wrong.append(str(hits[0]))
        assert not missing, f"not caught: {missing}; got {[str(line) for line in found]}"
        assert not wrong, wrong
        hatch = [line for line in found if line.check_id == "PHYS-01" and "hatch" in line.what]
        ladder = [line for line in found if line.check_id == "PHYS-01" and "climb" in line.what]
        assert hatch and ladder, [str(line) for line in found if line.check_id == "PHYS-01"]
        teeth = next(line for line in found if line.check_id == "PHYS-02")
        assert "0.3 metres" in teeth.what and "heavy" in teeth.what, teeth
        return f"{len(PHYSICAL_SLIPS)} slips caught by {len({entry[0] for entry in PHYSICAL_SLIPS})} checks; " \
               f"for example: {teeth}"

    @group("B3: other ways of writing the same slips are caught too, and near misses are not")
    def physical_phrasings():
        variants = [
            ("- subject: CH-TEST-PATIENT | does: holds up the guard against the grid",
             "- subject: CH-TEST-PATIENT | does: holds the guard up against the grid", "PHYS-08", "SC90-SH050"),
            ("does: climbs the rungs with the flashlight in her teeth",
             "does: climbs the rungs with the flashlight clamped in her jaws", "PHYS-02", "SC90-SH010"),
            ("- moment: 0-3 | shows: the two men take cover in the corner of the car from the shots coming down",
             "- moment: 0-3 | shows: the guard drags the patient into the corner for cover from the shots fired down "
             "through the roof grid", "PHYS-06", "SC90-SH030"),
            ("- moment: 0-3 | shows: the guard kicks the gate open", "- moment: 0-3 | shows: the gate is kicked open",
             "PHYS-09", "SC90-SH080"),
            ("- moment: 0-3 | shows: the patient runs the length of the car",
             "- moment: 0-3 | shows: the patient sprints for the hatch", "PHYS-08", "SC90-SH060"),
        ]
        world = GENERIC_WORLD.replace("- dressing: a bare steel car whose roof is a grid of flat bars",
                                      "- dressing: a bare steel car")
        missed = []
        for old, new, check_id, record in variants:
            assert world.count(old) == 1, old
            changed = world.replace(old, new)
            found = [line for line in lines_of(run(fresh(gold_texts(), changed), [check_id]), check_id)
                     if line.record == record]
            if not found:
                missed.append(f"{check_id} {record}: {new}")
        assert not missed, missed
        near = world.replace("- subject: CH-TEST-PATIENT | does: holds up the guard against the grid",
                             "- subject: CH-TEST-PATIENT | does: holds her hand up against the grid")
        near = near.replace("- moment: 0-3 | shows: the patient takes the guard's weight",
                            "- moment: 0-3 | shows: the patient raises one hand")
        near = near.replace("- subject: CH-TEST-PATIENT | does: runs to the hatch",
                            "- subject: CH-TEST-PATIENT | does: runs his hand along the grid")
        near = near.replace("- moment: 0-3 | shows: the patient runs the length of the car",
                            "- moment: 0-3 | shows: his fingers find the hatch")
        found = [str(line) for line in lines_of(run(fresh(gold_texts(), near), ["PHYS-08"]), "PHYS-08")]
        assert not found, found
        return f"{len(variants)} other phrasings caught; 'holds her hand up' and 'runs his hand along' pass"

    @group("B3: the same generic scene with the slips mended raises no physical sense line")
    def physical_mended():
        mended = GENERIC_WORLD
        replacements = [
            ("- size: [2.4, 2.4, 20.0]", "- size: [4.0, 4.0, 20.0]"),
            ("- object: CAR | at: [1.2, 1.2]", "- object: CAR | at: [2.6, 2.0]"),
            ("- mark: CLIMB | at: [0.15, 1.6]", "- mark: CLIMB | at: [0.6, 1.6]"),
            ("size: [0.4, 0.1, 0.8]", "size: [0.8, 0.1, 1.8]"),
            ("- object: ROPES | at: [2.3, 2.3]", "- object: ROPES | at: [0.3, 2.3]"),
            ("a heavy black metal flashlight about 30 centimetres long", "a pen light the length of a finger"),
            ("- real_size: [0.05, 0.05, 0.3]", "- real_size: [0.02, 0.02, 0.09]"),
            ("- parenthetical: round the flashlight", "- parenthetical: none"),
            ("- hear: SC90-D01 | speaker: on_screen | at: 1", "- hear: none"),
            ("does: cuts the strap and pulls it free", "does: cuts the strap with a utility knife and pulls it free"),
            ("a dark knitted cap", "a dark knitted cap, a utility knife clipped to her belt"),
            ("a grid of flat bars", "a grid of flat bars, with a wooden deck over one end"),
            ("the rung rolls under her hand like a rolling pin", "the rung bends a little under her hand"),
            ("does: holds up the guard against the grid", "does: leans on the grid beside the guard"),
            ("does: runs to the hatch", "does: limps to the hatch"),
            ("the patient runs the length of the car", "the patient limps the length of the car"),
            ("- dressing: a bare steel car", "- exit: GATE | leads_to: the corridor; the gate opens away from the car\n"
                                             "- dressing: a bare steel car"),
            ("does: holds the rope, the hook and the bag", "does: holds the rope and the hook; the bag hangs on her back"),
            ("- thing: PR-TEST-BOLT | emphasis: 2", "- thing: PR-TEST-BOLT | emphasis: 1"),
        ]
        for old, new in replacements:
            assert mended.count(old) == 1, old
            mended = mended.replace(old, new)
        result = run(fresh(gold_texts(), mended), [f"PHYS-{number:02d}" for number in range(1, 12)])
        lines = [str(line) for line in lines_of(result)]
        assert not lines, lines
        return f"{len(replacements)} mends; no line"

    @group("the gold scene 10 and its chat-saved copy raise none of the new warnings, and the new rules break no "
           "other check there")
    def gold_clean():
        result = run(fresh(gold_texts()), None)
        new = [str(line) for line in result.problems if line.check_id in NEW_CHECKS]
        assert not new, new
        craft = [str(line) for line in result.problems if line.check_id.split("-")[0] in ("CRAFT", "PHYS")]
        assert not craft, craft
        detail = f"gold: {len(result.checks_run)} checks, none of the new ones fires"
        if CHAT_FOLDER.is_dir():
            chat = run(sorted(CHAT_FOLDER.rglob("*.md")), NEW_CHECKS + ["CRAFT-15"])
            lines = [str(line) for line in chat.problems]
            assert not lines, lines
            detail += f"; chat copy: silent on {len(NEW_CHECKS) + 1} checks"
        stills = [line for line in GOLD_FILES["scene"].read_text(encoding="utf-8").splitlines()
                  if line.startswith("- subject:") and "| still:" in line]
        assert not stills, stills[:2]
        return detail

    @group("the new checks are warnings with a plain sentence and a J title, listed for steps 4, 7 and 8")
    def registration():
        check_records.load_check_families()
        problems = []
        for check_id in NEW_CHECKS:
            definition = check_records.REGISTRY.get(check_id)
            if definition is None:
                problems.append(f"{check_id} not registered")
                continue
            if definition.level != "W" or definition.build != 1:
                problems.append(f"{check_id} is {definition.level} build {definition.build}")
            if "J" not in re.findall(r"\bJ\b", definition.title):
                problems.append(f"{check_id}'s title does not say J")
            plain = definition.plain
            if not plain or plain[0].isupper() or re.search(r"[A-Z]{2,}-\d\d|\bJ\b", plain):
                problems.append(f"{check_id}'s plain sentence {plain!r}")
        steps = json.loads((SKILL / "schema" / "steps.json").read_text(encoding="utf-8"))["steps"]
        listed = {entry["step"]: entry["checks"] for entry in steps}
        if "PHYS-01" not in listed[4]:
            problems.append("step 4 does not list PHYS-01")
        if "PHYS-03" not in listed[7]:
            problems.append("step 7 does not list PHYS-03")
        for check_id in NEW_CHECKS:
            if check_id not in listed[8]:
                problems.append(f"step 8 does not list {check_id}")
        assert not problems, problems
        return f"{len(NEW_CHECKS)} warnings; step 4 lists PHYS-01, step 7 PHYS-03, step 8 all of them"

    @group("no new or changed file of this work holds an email address")
    def no_email():
        files = [Path(__file__), TOOLS / "stage_tools" / "checks_physical_sense.py",
                 TOOLS / "stage_tools" / "checks_craft_reasons_words.py", SKILL / "rules" / "constants.json",
                 GOLD_FILES["scene"]]
        found = [f"{path.name}: {match}" for path in files
                 for match in EMAIL.findall(path.read_text(encoding="utf-8"))]
        assert not found, found
        return f"{len(files)} files read"

    temporary_folder.cleanup()
    failing = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({RESULTS.count(True)} passed, {failing} failing groups)")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
