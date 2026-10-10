"""The acceptance test of the fixes after the second full run on The Catch (Project notes 39; the fix list is
"fix list.md" of that run, entries F01 to F63; the fixes are written up in Project notes 40).

What it proves, one group per problem (instruction-text fixes share one group), on small fixtures only: copies of the
WP12a gold (examples/01 and 02, scene 10), the scene 10 excerpt, and short texts written here. No group reads a whole
story. It borrows its helpers from fix02_full_run_acceptance.py.

Groups:
- F01 a side choice; F02 world text on nothing; F03 review answers across batches; F04 the scores wait for their
  unit; F05 a saved choice skips in-story footage; F06-F10 the handout's scene records; F11 the list unit in brief;
  F12 the handout's trimming order; F13 the prompt lint; F14 paired singles in one part; F15 scene-wide checks
  wait; F16 silent third none; F17 text none reads nothing; F18 00 Start here after the exports;
- F19 the first estimate and warnings kept on purpose; F20 a mounted camera; F21 the impact of a scene; F22 the
  film pass's check unit; F23 an invention in the list; F24 step 7's floors and beat states; F25 a rung's hold;
  F26 questions without "..."; F27 "as before the fire"; F28 lamplight and lamps; F29 side items, every word;
  F30 check --unit and cited coverage; F32 a mark inside an object; F33 the TEXT template's quote;
  F35 the self-test's note;
- F31, F34-F53 the instructions (one shared group); F37, F38, F40 a split speech, a move's via, a spoken plant;
  F51, F52 apply's report and a saved choice's beat uses;
- F53 what the book shows a reader; F54 the book never contradicts itself; F55 the health check's first line;
  F56 14 Time and cost; F57 01 Choices after read; F58 check --unit messages; F59 texts in a scene's handout;
  F61 three checks read words in any form; F62, F63 the add-ons' names and place headings.
F60 (scene file names) is left as designed; see the fix report.
- the cross-examination of these fixes ("cross-examination.md" of that run), one group per finding repaired: X01 only
  a state's sides merge; X02 "as before" and a joining word; X03 words added later keep their meaning; X04 text none
  keeps a featured text's floor; X05 a camera on the scene's own place; X06 a straight cut across parts; X07 silent
  third none with three present; X08 the only place of its kind; X09 an eyeline point in the book; X10 a speaking
  shot kept whole only when cut; X11 a seal ring; X12 the film pass's check after later changes; X13 a passed long
  list kept on purpose; X14 a move's marks; X15 the instruction wording; X16 "says it" in the frame's rows.

Usage: python tests/fix05_second_full_run_acceptance.py
Standard library only.
"""

import json
import re
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fix02_full_run_acceptance as helpers  # noqa: E402
from fix02_full_run_acceptance import (MACHINE, RESULTS, SCHEMA, SKILL, edit, gold_command_project,  # noqa: E402
                                       gold_texts, group, read_manifest, stage, write_inbox, write_manifest)


def project_file(project, name):
    return next(path for path in Path(project).rglob("*.md") if path.name == name)


def record_text(path, heading):
    """The lines of one record ('### TYPE ID ...') in a file, up to the next record."""
    text = Path(path).read_text(encoding="utf-8")
    assert f"### {heading}" in text, f"{Path(path).name} has no {heading}"
    return text.split(f"### {heading}", 1)[1].split("\n### ", 1)[0].split("\nEND OF FILE", 1)[0]


def field_values(block, name):
    return [line[len(f"- {name}: "):] for line in block.splitlines() if line.startswith(f"- {name}: ")]


def error_lines(output, check_id=None):
    return [line for line in output.splitlines() if line.startswith("E ")
            and (check_id is None or line.startswith(f"E {check_id} "))]


class GoldStoryWorkspace:
    """A stand-in for make_handout's Workspace: the gold records (with edits), the scene 10 excerpt's numbered lines
    and the derived breakdown, with no project folder."""

    def __init__(self, texts):
        self.run, self.breakdown = helpers.gold_breakdown(texts)
        self.story = self.run.story.numbered
        self.story_map = {}
        self.index = self.run.index

    def record(self, identifier, type_name=None):
        found = self.run.record(identifier) if identifier else None
        return found if found is not None and (type_name is None or found.type_name == type_name) else None

    def records(self, type_name):
        return self.run.records(type_name)

    def story_scene(self, scene_identifier):
        return None

    def scene_lines(self, scene_identifier):
        return self.breakdown.scene_range(scene_identifier)


class FakeLook:
    """A LOOK record stand-in: get() of its fields."""

    def __init__(self, fields):
        self.fields = fields

    def get(self, name):
        return self.fields.get(name)


# ---------------------------------------------------------------- F01: a side choice keeps the state's other sides

@group("F01: a side choice sets only the sides it names, keeps the others and locks the state; the same answer sent "
       "with a corrected SETVALUE is applied again, and FORM-11 stays quiet")
def side_choice(scratch):
    from stage_tools.project_files import items_by_first_part
    old = ["ring | own: left | plot: yes", "tooth | own: right | plot: no", "sleeve | own: right | plot: no",
           "palm | own: right | plot: yes"]
    merged = items_by_first_part(old, ["sleeve | own: left | plot: no", "palm | own: left | plot: yes"])
    assert merged == ["ring | own: left | plot: yes", "tooth | own: right | plot: no",
                      "sleeve | own: left | plot: no", "palm | own: left | plot: yes"], merged
    assert items_by_first_part(["none"], ["palm | own: left"]) == ["palm | own: left"]
    project = gold_command_project(scratch, "f01 sides")
    continuity = project / "09 Continuity.md"
    code, output = stage(["--project", project, "check", "--all"])  # the checker keeps its copy of locked records
    assert code == 0, error_lines(output)
    inbox = write_inbox(project, "U-05-CONT - fix 1.md", "### CHOICE CHOICE-014\n- answer: b\n")
    code, output = stage(["--project", project, "apply", inbox])
    assert code == 0, output[-600:]
    block = record_text(continuity, "STATE CH-IONA.S02")
    sides = field_values(block, "side")
    assert sides == ["sleeve torn away | own: left | plot: no", "skinned palm | own: left | plot: yes",
                     "wedding ring | own: left | plot: yes"], sides
    assert field_values(block, "locked") == ["yes"], block
    code, output = stage(["--project", project, "check", "--all"])
    assert code == 0 and not error_lines(output, "FORM-11"), error_lines(output)
    inbox = write_inbox(project, "U-05-CONT - fix 2.md", "### CHOICE CHOICE-014\n- answer: b\n\n"
                        "### SETVALUE CHOICE-014-B\n- target: CH-IONA.S02\n"
                        "- side: sleeve torn away | own: left | plot: yes\n- side: skinned palm | own: left | plot: yes\n")
    code, output = stage(["--project", project, "apply", inbox])
    assert code == 0, output[-600:]
    sides = field_values(record_text(continuity, "STATE CH-IONA.S02"), "side")
    assert sides[0] == "sleeve torn away | own: left | plot: yes" and len(sides) == 3, sides
    choice = record_text(project / "01 Choices.md", "CHOICE CHOICE-014")
    assert field_values(choice, "status") == ["answered"], choice
    code, output = stage(["--project", project, "check", "--all"])
    assert code == 0 and not error_lines(output, "FORM-11"), error_lines(output)
    phrase = "its SETVALUE names only the sides it decides"
    assert phrase in (SKILL / "steps" / "05 Continuity.md").read_text(encoding="utf-8")
    return "4 sides kept, 2 set; the corrected SETVALUE applied again; no FORM-11"


# ---------------------------------------------------------------- F02: world text on nothing follows the world

@group("F02: a sign on nothing that a text rule governs reads mirrored where the world is mirrored (the scene's "
       "place), with the mirrored reading floor; a title card stays normal; outside a text rule it follows the frame")
def world_text_on_nothing(scratch):
    from stage_tools.derive_fields import text_orientation, time_floor
    sign = ("### TEXT TX-NOTICE A notice on the wall\n- kind: sign\n- words: CLOSED\n- on: none\n- origin: invented\n"
            "- reader: CH-IONA\n- plot_critical: no\n- emphasis: 2\n- method: composite\n- animation: none\n")
    rule = ("### RULE WR-WORLD-TEXT Words printed in the world\n- kind: text\n- statement: Signs read backwards while "
            "the world is mirrored.\n- governs: TX-NOTICE\n- exception: none\n")
    texts = edit(gold_texts(), "context", "TEXT TX-TITLE-CATCH", add_after=sign)
    texts = edit(texts, "scene", "SHOT SC10-SH020", "- text: none", "- text: TX-NOTICE")
    run, breakdown = helpers.gold_breakdown(texts, story=False)
    shot = breakdown.record("SC10-SH020", "SHOT")
    assert text_orientation(breakdown, "TX-NOTICE", shot) == "normal", "no text rule: it should follow the frame"
    texts = edit(texts, "context", "RULE WR-TITLES", add_after=rule)
    run, breakdown = helpers.gold_breakdown(texts, story=False)
    shot = breakdown.record("SC10-SH020", "SHOT")
    assert text_orientation(breakdown, "TX-NOTICE", shot) == "mirrored", text_orientation(breakdown, "TX-NOTICE", shot)
    assert text_orientation(breakdown, "TX-TITLE-CATCH", shot) == "normal"
    parts = {name: how for name, _, how in time_floor(breakdown, shot).text_parts}
    assert "mirrored" in parts.get("TX-NOTICE", ""), parts
    phrase = "a sign in the world is on its place; only titles and captions are on none"
    assert phrase in (SKILL / "steps" / "04 Characters, places and things.md").read_text(encoding="utf-8")
    return f"the notice in the reversed kitchen reads mirrored ({parts['TX-NOTICE']}); the title stays normal"


# ---------------------------------------------------------------- F03: review answers across question batches

@group("F03: a scene's review answers sent in two question batches are all kept; a question answered again is "
       "replaced, not doubled")
def review_answers_across_batches(scratch):
    project = gold_command_project(scratch, "f03 reviews")
    first = ("### REVIEW RV-SC10 Scene 10's review\n- scope: SC10\n"
             "- answer: Does Iona chew the leaf? | answer: yes | evidence: shot 150\n"
             "- answer: Does Saye answer off screen? | answer: yes | evidence: shot 150, moment 2\n")
    second = ("### REVIEW RV-SC10 Scene 10's review\n- scope: SC10\n"
              "- answer: Is the flask on the table? | answer: no | evidence: shot 020\n"
              "- answer: Does Iona chew the leaf? | answer: yes | evidence: shot 150, moment 4\n")
    for name, text in (("U-10-Q01.md", first), ("U-10-Q02.md", second)):
        code, output = stage(["--project", project, "apply", write_inbox(project, name, text)])
        assert code == 0, output[-600:]
    answers = field_values(record_text(project / "13 Health check.md", "REVIEW RV-SC10"), "answer")
    assert len(answers) == 3, answers
    assert "Does Iona chew the leaf? | answer: yes | evidence: shot 150, moment 4" in answers, answers
    return "3 answers kept from 2 batches; the repeated question replaced"


# ---------------------------------------------------------------- F04: the scores wait for the scores unit

@group("F04: check --all before the scores unit counts a review's missing scores as not yet due, never errors; "
       "once the scores unit is done they are errors again")
def scores_wait_for_their_unit(scratch):
    project = gold_command_project(scratch, "f04 scores")
    review = ("### REVIEW RV-SC10 Scene 10's review\n- scope: SC10\n"
              "- answer: Does Iona chew the leaf? | answer: yes | evidence: shot 150\n")
    code, output = stage(["--project", project, "apply", write_inbox(project, "U-10-Q01.md", review)])
    assert code == 0, output[-600:]
    code, output = stage(["--project", project, "check", "--all"])
    assert code == 0 and not error_lines(output, "FORM-05"), error_lines(output)
    assert "Not yet due: 1 line about the scores" in output, output[-600:]
    manifest = read_manifest(project)
    manifest["units_done"].append({"unit": "U-10-SCORES", "applied": "2026-10-05T10:00:00"})
    write_manifest(project, manifest)
    code, output = stage(["--project", project, "check", "--all"])
    assert code == 1 and any("RV-SC10 score is missing" in line for line in error_lines(output, "FORM-05")), \
        output[-600:]
    return "a missing score waits for the scores unit, and is an error after it"


# ---------------------------------------------------------------- F05: in-story footage spends no saved choice

@group("F05: the film-level count of a saved choice (FILM-08, the handouts' uses left) skips in-story footage, as "
       "the scene-level count does; a film shot with the same angle still counts")
def saved_choice_skips_footage(scratch):
    from stage_tools.film_pass import reserve_uses
    reserve = ("### RESERVE RC-09 Straight down\n- choice: a camera looking straight down\n- match: angle = top_down\n"
               "- max_uses: 1\n- allowed_in: SC10\n- never_on: none\n- because: PLAN\n")
    texts = edit(gold_texts(), "context", "RESERVE RC-01", add_after=reserve)
    texts = edit(texts, "scene", "SHOT SC10-SH020", "- angle: high", "- angle: top_down")
    texts = edit(texts, "scene", "SHOT SC10-SH020", "- kind: insert", "- kind: screen")
    texts = edit(texts, "scene", "SHOT SC10-SH030", "- angle: high", "- angle: top_down")
    run = helpers.check_run(texts, story=False)
    uses = [record.identifier for record in reserve_uses(run, run.record("RC-09"))]
    assert uses == ["SC10-SH030"], uses
    return "the screen shot is not a use; the film shot is (1 use)"


# ---------------------------------------------------------------- F06 to F10: what the handouts leave out

@group("F06-F10: a handout's scene records hold a person who never speaks but is named, a fact about several "
       "elements, the look before the scene's place is written, every motif with a story-point appearance, and the "
       "state of a thing carried in or named")
def handout_scene_records(scratch):
    from stage_tools.derive_fields import states_in_play as derived_states
    from stage_tools.make_handout import (Workspace, appearance_in_scene, characters_present, elements_in_scene,
                                          facts_for_scene, looks_for_scene, states_in_play)
    silent = ("### CHARACTER CH-NEIGHBOUR The woman next door\n- names: WOMAN, the woman\n- tier: extra\n"
              "- origin: invented\n\n### CHARACTER CH-GUARD The guard\n- names: GUARD, the guard\n- tier: extra\n"
              "- origin: invented\n")
    fridge = ("### PROP PR-FRIDGE The fridge\n- names: fridge, the fridge\n- category: set_dressing\n"
              "- origin: invented\n")
    fridge_state = ("### STATE PR-FRIDGE.S01 Humming\n- element: PR-FRIDGE\n- from: SC07 | line: 310\n"
                    "- state_line: a white fridge, its door bare\n- origin: invented\n")
    fact = ("### FACT FT-09 Eli keeps the flask\n- element: CH-ELI, PR-FLASK\n- audience_knows_from: SC04\n")
    texts = edit(gold_texts(), "context", "CHARACTER CH-IONA", add_after=silent)
    texts = edit(texts, "context", "STATE PR-FLASK.S03", add_after=fridge_state + "\n" + fridge)
    texts = edit(texts, "context", "FACT FT-01", add_after=fact)
    workspace = GoldStoryWorkspace(texts)
    text = " ".join(workspace.story.line(number) for number in range(*workspace.scene_lines("SC10")))
    present = characters_present(workspace, "SC10")
    assert "CH-NEIGHBOUR" in present and "CH-GUARD" not in present, present
    elements = elements_in_scene(workspace, "SC10")
    assert {"MO-RINGS", "MO-MINT", "MO-FLASK"} <= set(elements), elements
    assert appearance_in_scene('SC12 "a toy carriage marked F" = SC12-B01 | role: plant', "SC12")
    assert not appearance_in_scene('SC12 "a toy carriage marked F" = SC12-B01', "SC13")
    assert "FT-09" in [record.identifier for record in facts_for_scene(workspace, ["CH-ELI"], "SC10")]
    assert "fridge" in text.lower(), "the excerpt's scene 10 no longer names the fridge"
    assert "PR-FRIDGE.S01" not in derived_states(workspace.breakdown, "SC10")
    assert "PR-FRIDGE.S01" in [state.identifier for state in states_in_play(workspace, "SC10")]
    project = gold_command_project(scratch, "f08 look")
    scene_file = next((project / "11 Scenes").glob("*.md"))
    scene_text = scene_file.read_text(encoding="utf-8")
    for line in ("- location: LOC-SAYE-KITCHEN\n", "- look: LK-SAYE-KITCHEN-NIGHT\n"):
        assert line in scene_text, line
        scene_text = scene_text.replace(line, "", 1)
    scene_file.write_text(scene_text, encoding="utf-8")
    looks = [look.identifier for look in looks_for_scene(Workspace(project), "SC10")]
    assert looks == ["LK-SAYE-KITCHEN-NIGHT"], looks
    return "the silent neighbour, 3 motifs, FT-09, the fridge's state and the look before the place is written"


# ---------------------------------------------------------------- F11: a trimmed list unit keeps its cameras

@group("F11: a split scene's list unit, in brief, still gets every setup (where, lens, use) and move (who, from, "
       "to) the earlier parts wrote")
def list_unit_in_brief(scratch):
    from stage_tools.make_handout import Workspace, earlier_parts_section
    project = gold_command_project(scratch, "f11 list unit")
    workspace = Workspace(project)
    unit = SimpleNamespace(list_unit=True, scene="SC10", step=7, part=None)
    section = earlier_parts_section(workspace, unit, workspace.record("SC10", "SCENE"), brief=True)
    setups = re.findall(r"### SETUP (SC10-SU\d+)", section)
    moves = re.findall(r"### MOVE (SC10-M\d+)", section)
    assert setups and moves and "SC10-SU01" in setups, (setups, moves)
    assert "- lens_mm:" in section and "- who:" in section and "- look_at_words:" not in section, section[-600:]
    return f"{len(setups)} setups and {len(moves)} moves kept in brief"


# ---------------------------------------------------------------- F12: trimming a handout keeps the tag cards

@group("F12: a handout over its ceiling trims the story to the unit's lines before leaving out any card part, and "
       "leaves out the scene's tag parts (glass, screens, creatures) last")
def handout_trimming_order(scratch):
    from stage_tools.make_handout import Handout

    def words(count):
        return " ".join(["w"] * count)  # one token a word
    handout = Handout(unit=None, ceiling=2000, tokens_per_word=1.0, card_cap=100000)
    handout.add("task", words(300))
    handout.add("source", words(1500), kind="source", trimmed_text=words(200))
    handout.add("card 14 a", words(400), kind="card", label="card 14, a")
    handout.add("card 16 a", words(400), kind="card", label="card 16, a", from_tag=True)
    handout.add("card 13 b", words(400), kind="card", label="card 13, b")
    handout.fit()
    assert handout.card_parts_left_out == [], handout.left_out
    assert any("story's lines" in note for note in handout.left_out), handout.left_out
    handout = Handout(unit=None, ceiling=1200, tokens_per_word=1.0, card_cap=100000)
    handout.add("task", words(300))
    handout.add("source", words(400), kind="source", trimmed_text=words(200))
    handout.add("card 14 a", words(300), kind="card", label="card 14, a")
    handout.add("card 16 a", words(300), kind="card", label="card 16, a", from_tag=True)
    handout.add("card 13 b", words(300), kind="card", label="card 13, b")
    handout.fit()
    assert handout.card_parts_left_out == ["card 13, b"], handout.card_parts_left_out
    assert "card 16, a" not in handout.card_parts_left_out
    return "the story trimmed first; the lowest standard part left out before the tag part"


# ---------------------------------------------------------------- F13: the prompt lint's tool faults

@group("F13: the compiler sends a split speech's own words, keeps a speaking shot whole on a model long enough, "
       "sends a start picture's action only, says composited words as added later and never pastes a speech twice; "
       "the lint counts a split speech's words, reads 'no longer than' as a size and knows pasted descriptions")
def prompt_lint(scratch):
    from stage_tools.checks_plan_generation_film import (ALLOWED_NEGATION_PHRASES, NEGATION, Clip, heard_words_text,
                                                         visible_texts)
    from stage_tools.compile_prompts import (Adapters, able, action_only, heard_line, leave_words_for_later,
                                             picture_clauses, without_quoted_speech)
    from stage_tools.record_format import split_item
    # (a) the words a shot hears of a speech split at a phrase, in the prompt and in GEN-03's count
    entry = {"text": "Bring the lamp. Then the case, from the shelf. Then wait."}
    assert heard_line({"words": '"Bring the lamp. Then the case, from the shelf."'}, entry) == \
        "Bring the lamp. Then the case, from the shelf."
    assert heard_line({}, entry) == entry["text"]
    assert heard_line({"words": "words the speech never says"}, entry) == entry["text"]
    run = helpers.check_run(gold_texts())
    whole = heard_words_text(run, "SC10-D12", None)
    part = " ".join(whole.split()[:5])
    assert heard_words_text(run, "SC10-D12", split_item(f"SC10-D12 | words: {part}")) == part
    adapters = Adapters()
    plan = SimpleNamespace(held=False, held_why="", whole_for_speech=True, needed_s=16.0, start_picture=False,
                           end_picture=False, guide_video=False, performance=False, sends_speech=True, recurring=False,
                           faces_to_reference=0)
    fifteen_seconds, thirty_seconds = adapters.video.get("kling-3.0-omni"), adapters.video.get("seedance-2.5")
    assert not able(adapters, "kling-3.0-omni", fifteen_seconds, plan)[0], "a 15 s model took a 16 s speaking shot"
    assert able(adapters, "seedance-2.5", thirty_seconds, plan)[0]
    plan.whole_for_speech = False
    assert able(adapters, "kling-3.0-omni", fifteen_seconds, plan)[0], "a shot without speech is still split as before"
    # (b) a start picture carries the look: the prompt keeps the action
    clauses = picture_clauses(["A bare yard under rain, puddles on every side, lit by one lamp."])
    assert action_only("The yard wall, puddles on every side; the man runs to the gate", clauses) == \
        "The yard wall; the man runs to the gate"
    # (c) composited words are said as added later, as the thing the title names, or a single mark as a letter
    # (changed by the cross-examination, X03: "the red label with words added later" lost the button)
    assert leave_words_for_later("a crate marked EXIT", [("EXIT", "label")]) == \
        "a crate marked with words added later"
    assert leave_words_for_later("her hand hits the red STOP.", [("STOP", "label", "button")]) == \
        "her hand hits the red button."
    assert leave_words_for_later("the K on its lid reads the right way", [("K", "label")]) == \
        "the letter on its lid reads the right way"
    assert leave_words_for_later("Kettles on the stove", [("K", "label")]) == "Kettles on the stove"
    # (d) a size is no negation
    for sentence, negates in (("A creature no longer than a hand.", False), ("No more than a glow.", False),
                              ("There is no door.", True)):
        assert bool(NEGATION.search(ALLOWED_NEGATION_PHRASES.sub(" ", sentence))) is negates, sentence
    # (e) the descriptions compile pastes are visible words
    shot = run.record("SC10-SH020")
    clip = Clip("SC10-SH020.1", "SC10-SH020", shot, "kling-3.0-omni", {})
    visible = visible_texts(clip, run)
    assert "a bare spring clip under its base" in visible and "small dented steel vacuum flask" in visible, visible[:300]
    assert "a bare spring clip" not in visible_texts(clip), "without the run nothing was meant to be added"
    # (f) a quoted part of a heard speech is not pasted again in the picture's words
    assert without_quoted_speech('He turns, through the door: "Bring the lamp."', [entry["text"]]) == \
        "He turns, through the door"
    return "split words sent and counted; 16 s speaking shot kept whole; action only; words added later; a size; " \
           "pasted descriptions; no doubled speech"


# ---------------------------------------------------------------- F14: GEOM-01 pairs singles within one part

@group("F14: GEOM-01 pairs singles only within one part of a scene (or on a straight cut between parts), read when "
       "the line is spoken: the gold passes; a camera moved across the line in part 2 fails there, never against "
       "part 1's other shots")
def paired_singles_in_one_part(scratch):
    found = helpers.lines_of(helpers.checked(gold_texts(), ["GEOM-01"], story=False), "GEOM-01")
    assert not found, found
    texts = edit(gold_texts(), "scene", "SETUP SC10-SU03", "- at: [2.5, 3.25, 1.55]", "- at: [3.1, 3.25, 1.55]")
    texts = edit(texts, "scene", "SETUP SC10-SU03", "- look_at: [2.9, 1.0, 1.5]", "- look_at: [2.7, 1.0, 1.5]")
    problems = helpers.lines_of(helpers.checked(texts, ["GEOM-01"], story=False), "GEOM-01")
    named = " ".join(str(problem) for problem in problems)
    assert problems and "SC10-SH170" in named, named
    # shot 150 (part 1) cuts straight to shot 160 (part 2), so that pair is read too (the cross-examination, X06)
    assert "SC10-SH070" not in named, named
    return f"{len(problems)} crossed pairs found in part 2 and on its first cut; none against the rest of part 1"


# ---------------------------------------------------------------- F15: scene-wide sound and light checks wait

@group("F15: COVER-07 and COVER-08 wait for a scene's last batch at step 8, and run once it is in")
def scene_wide_checks_wait(scratch):
    batches = {"U-08-SC10-B1": {"first": "SC10-SH010", "last": "SC10-SH120", "expected": 12, "received": 12},
               "U-08-SC10-B2": {"first": "SC10-SH130", "last": "SC10-SH990", "expected": 9, "received": None}}
    checks = ["COVER-07", "COVER-08"]
    result = helpers.checked(gold_texts(), checks, step=8, manifest={"batches": {"SC10": batches}})
    waiting = {check for check, why in result.skipped if "last batch" in why}
    assert waiting == set(checks), result.skipped
    assert not [problem for problem in result.problems if problem.check_id in checks], result.problems
    batches["U-08-SC10-B2"]["received"] = 9
    result = helpers.checked(gold_texts(), checks, step=8, manifest={"batches": {"SC10": batches}})
    assert not [why for check, why in result.skipped if "last batch" in why], result.skipped
    return "both wait while batch 2 is out, and run after it"


# ---------------------------------------------------------------- F16: nobody left to witness

@group("F16: 'silent_third: none' on a beat of a three-person scene is kept by apply (not read as clearing the "
       "field) and passes FORM-04 and FORM-05")
def silent_third_none(scratch):
    from stage_tools.project_files import none_allowed
    assert none_allowed(SCHEMA.field("BEAT", "silent_third")), "apply would still clear the field"
    texts = gold_texts()
    beat = next(line for line in texts["scene"].splitlines() if line.startswith("- silent_third: CH-"))
    heading = None
    for line in texts["scene"].splitlines():
        if line.startswith("### BEAT "):
            heading = line[4:].split(" ")[0] + " " + line[4:].split(" ")[1]
        if line == beat:
            break
    texts = edit(texts, "scene", heading, beat, "- silent_third: none")
    result = helpers.checked(texts, ["FORM-04", "FORM-05"], story=False)
    lines = [problem for problem in result.problems if "silent_third" in str(problem)]
    assert not lines, lines
    return f"{heading.split()[1]} keeps 'none' with no FORM-04 or FORM-05 line"


# ---------------------------------------------------------------- F17: text none has nothing to read

@group("F17: a shot that writes 'text: none' owes no reading time for plot-critical text on a thing it shows; a "
       "shot with no text line still does")
def text_none_reads_nothing(scratch):
    from stage_tools.derive_fields import time_floor
    label = ("### TEXT TX-FLASK-LABEL The flask's label\n- kind: label\n- words: KEEP FROZEN AT ALL TIMES\n"
             "- on: PR-FLASK\n- origin: invented\n- words_from: 400\n- reader: CH-SAYE\n- plot_critical: yes\n"
             "- emphasis: 2\n- method: composite\n- animation: none\n")
    texts = edit(gold_texts(), "context", "TEXT TX-TITLE-CATCH", add_after=label)
    run, breakdown = helpers.gold_breakdown(texts, story=False)
    floor = time_floor(breakdown, breakdown.record("SC10-SH020", "SHOT"))
    assert not floor.text_parts, floor.text_parts
    texts = edit(texts, "scene", "SHOT SC10-SH020", "- text: none\n", "")
    run, breakdown = helpers.gold_breakdown(texts, story=False)
    floor = time_floor(breakdown, breakdown.record("SC10-SH020", "SHOT"))
    assert [name for name, _, _ in floor.text_parts] == ["TX-FLASK-LABEL"], floor.text_parts
    return "no reading floor with text: none; the label's floor without a text line"


# ---------------------------------------------------------------- F18: 00 Start here after the book and exports

@group("F18: export all writes a log line in 00 Start here and remakes its plain part; once nothing is left, 00 says "
       "the breakdown is finished instead of naming step 12 as the next piece of work")
def start_here_after_exports(scratch):
    from stage_tools import make_views
    from stage_tools.make_views import FINISHED_LINE, ProjectView, plain_part_lines_of, start_here_plain_part
    project = gold_command_project(scratch, "f18 start here")
    code, output = stage(["--project", project, "export", "all"])
    assert code == 0, output[-600:]
    text = (project / "00 Start here.md").read_text(encoding="utf-8")
    assert re.search(r"^\d{3} \S+ Made the book and the exports\.$", text, re.MULTILINE), text[-600:]
    assert "Next piece of work: step 10 of 12" in text, "work is left: 00 must still name it"
    view = ProjectView(project)
    record_file = next(each for each in view.record_files if each.name == "00 Start here.md")
    kept = make_views.next_unit_words
    make_views.next_unit_words = lambda view: ("Nothing: the breakdown is finished (the book and the exports are "
                                               "made); the add-ons run on request.")
    try:
        lines = "\n".join(start_here_plain_part(view, plain_part_lines_of(record_file)))
    finally:
        make_views.next_unit_words = kept
    assert FINISHED_LINE in lines and "Next piece of work" not in lines, lines[:600]
    assert "Last saved: step 12 of 12, the book and exports." in lines, lines[:300]
    return "a log line; 'Finished' once nothing is left, the next step while work remains"


# ---------------------------------------------------------------- F19: advisory and accepted warnings

@group("F19: the list far from the first estimate is a warning until the list is approved, then a note; its plain "
       "line gives the size and the direction; a warning whose finding is accepted is listed as kept on purpose")
def advisory_and_accepted_warnings(scratch):
    from stage_tools.check_records import health_check_plain_part, in_short_line
    texts = edit(gold_texts(), "context", "SCENE SC10", "- target_duration_s: 110", "- target_duration_s: 40")
    result = helpers.checked(texts, ["TIME-03"], story=False)
    far = [problem for problem in helpers.lines_of(result, "TIME-03") if "first estimate" in str(problem)]
    assert far and far[0].level == "N", far
    texts = edit(texts, "scene", "SHOTLIST SC10-LIST", "- approved: yes", "- approved: no")
    result = helpers.checked(texts, ["TIME-03"], story=False)
    far = [problem for problem in helpers.lines_of(result, "TIME-03") if "first estimate" in str(problem)]
    assert far and far[0].level == "W", far
    lines = "\n".join(health_check_plain_part(None, result, None, None, False, True, None))
    assert re.search(r"runs \d+ seconds, [\d.]+ times the first estimate of 40 seconds", lines), lines[:900]
    finding = ("### FINDING FIND-001 The long scene\n- record: SC10-LIST\n- rule: TIME-03\n- evidence: 112 s\n"
               "- fix: none\n- source: checker\n- status: accepted\n- reason: the scene needs its length\n")
    texts = edit(texts, "context", "SCENE SC10", add_after=finding)
    result = helpers.checked(texts, ["TIME-03"], story=False)
    lines = "\n".join(health_check_plain_part(None, result, None, None, False, True, None))
    kept = lines.split("## Kept on purpose", 1)
    assert len(kept) == 2 and "finding 1 in 12 Whole-film check gives the reason" in kept[1], lines[:900]
    assert "first estimate" not in lines.split("## Warnings", 1)[1].split("## Kept on purpose", 1)[0], lines[:900]
    assert "1 warning kept on purpose" in in_short_line(result, 0), in_short_line(result, 0)
    return "a note once approved; 'runs N seconds, X times the first estimate'; the accepted one kept on purpose"


# ---------------------------------------------------------------- F20 (b): a mounted camera

@group("F20: GEOM-04 does not measure a camera mounted on a person from its fixed point (it is skipped with a "
       "reason); a camera on the world is still measured")
def mounted_camera(scratch):
    texts = edit(gold_texts(), "scene", "SHOT SC10-SH150", "- size: close_up", "- size: wide")
    found = helpers.lines_of(helpers.checked(texts, ["GEOM-04"], story=False), "GEOM-04", "SC10-SH150")
    assert found, "a wide written on a close framing was not found"
    texts = edit(texts, "scene", "SETUP SC10-SU02", "- mount: world", "- mount: CH-IONA")
    result = helpers.checked(texts, ["GEOM-04"], story=False)
    assert not helpers.lines_of(result, "GEOM-04", "SC10-SH150"), helpers.lines_of(result, "GEOM-04")
    assert any("SC10-SH150" in why and "mounted" in why for check, why in result.skipped if check == "GEOM-04")
    return "measured on the world; skipped with a reason when mounted on Iona"


# ---------------------------------------------------------------- F21: impact stops at records that name a place

@group("F21: impact of a scene lists the story plan, its group, the ladder, saved choices and motifs that name the "
       "scene as a place to read again by hand, and follows no work through them")
def impact_of_a_scene(scratch):
    project = gold_command_project(scratch, "f21 impact")
    code, output = stage(["--project", project, "impact", "SC10", "--json"])
    assert code == 0, output[-600:]
    result = json.loads(output[output.index("{"):])
    by_hand = {entry["id"] for entry in result["read_again_by_hand"]}
    assert {"PLAN", "SQ03", "LADDER", "MO-FLASK"} <= by_hand, by_hand
    through = [entry for entry in result["stale"]
               if set(entry.get("via") or []) & {"PLAN", "SQ03", "LADDER", "MO-FLASK", "MO-MINT", "MO-RINGS"}]
    assert not through, [entry["id"] for entry in through]
    stale = {entry["id"] for entry in result["stale"]}
    assert "SC10-SH150" in stale and "PLAN" not in stale, sorted(stale)[:20]
    return f"{len(by_hand)} records to read again by hand; {len(stale)} stale, none through them"


# ---------------------------------------------------------------- F22: next waits on the film pass's own check

@group("F22: after the film pass's judgement, next names check --step 9 and stays on it while a film error is open; "
       "once it passes, next goes on to step 11 of 12")
def film_pass_check_unit(scratch):
    import datetime
    project = gold_command_project(scratch, "f22 film check")
    code, output = stage(["--project", project, "check", "--film"])
    assert code in (0, 1), output[-400:]
    manifest = read_manifest(project)
    applied = (datetime.datetime.now() - datetime.timedelta(seconds=5)).isoformat(timespec="seconds")
    manifest["units_done"].append({"unit": "U-09-JUDGE", "applied": applied})
    write_manifest(project, manifest)
    code, output = stage(["--project", project, "next"])
    assert code == 0 and "check --step 9" in output.splitlines()[0], output[:300]
    rules = project / "10 Film rules.md"
    text = rules.read_text(encoding="utf-8")
    block = text.split("### RESERVE RC-01", 1)[1].split("\n### ", 1)[0]
    rules.write_text(text.replace(block, re.sub(r"- max_uses: \d+", "- max_uses: 0", block), 1), encoding="utf-8")
    code, output = stage(["--project", project, "check", "--step", "9"])
    assert code == 1 and error_lines(output, "FILM-08"), output[-600:]
    code, output = stage(["--project", project, "next"])
    assert "check --step 9" in output.splitlines()[0], output[:300]
    rules.write_text(text, encoding="utf-8")
    code, output = stage(["--project", project, "check", "--step", "9"])
    assert code == 0, error_lines(output)
    code, output = stage(["--project", project, "next"])
    assert "step 11 of 12" in output.splitlines()[0], output[:300]
    phrase = "`next` waits on it until it passes"
    assert phrase in (SKILL / "steps" / "09 Film pass.md").read_text(encoding="utf-8")
    return "next waits on check --step 9 while FILM-08 is open, then goes on"


# ---------------------------------------------------------------- F23: invented records in a step 7 list

@group("F23: at step 7, a list item that shows an invented record not in the scene's additions fails CRAFT-14; "
       "listed as an addition it passes")
def invented_in_list(scratch):
    texts = gold_texts()
    for identifier in re.findall(r"^### SHOT (SC10-SH\d+)", texts["scene"], re.MULTILINE):
        texts = edit(texts, "scene", f"SHOT {identifier}", remove=True)
    notice = ("### TEXT TX-NOTICE A notice on the wall\n- kind: sign\n- words: CLOSED\n- on: LOC-SAYE-KITCHEN\n"
              "- origin: invented\n- reader: CH-IONA\n- plot_critical: no\n- emphasis: 1\n- method: composite\n"
              "- animation: none\n")
    texts = edit(texts, "context", "TEXT TX-TITLE-CATCH", add_after=notice)
    texts = edit(texts, "scene", "SHOTLIST SC10-LIST", "| subject: CH-ELI | time: 3.5 |",
                 "| subject: CH-ELI, TX-NOTICE | time: 3.5 |")
    assert "CRAFT-14" in json.loads((SKILL / "schema" / "steps.json").read_text(encoding="utf-8"))["steps"][7][
        "checks"], "CRAFT-14 is not among step 7's checks"
    found = helpers.lines_of(helpers.checked(texts, ["CRAFT-14"], story=False, step=7), "CRAFT-14")
    assert found and found[0].record == "SC10-LIST" and "TX-NOTICE" in str(found[0]), found
    texts = edit(texts, "scene", "SCENE SC10", "- additions: the three arrive",
                 "- additions: TX-NOTICE, a closed sign on the wall | changes_meaning: no\n- additions: the three arrive")
    found = helpers.lines_of(helpers.checked(texts, ["CRAFT-14"], story=False, step=7), "CRAFT-14")
    assert not found, found
    phrase = "in every scene that shows it, even one invented at an earlier step"
    assert phrase in (SKILL / "steps" / "07 Scene design and shot list.md").read_text(encoding="utf-8")
    return "the unlisted invented sign fails at step 7; listed, it passes"


# ---------------------------------------------------------------- F24: step 7 checks list times and beat states

@group("F24: at standard depth, step 7 warns about a list item under its floor (an error only at quick depth), and "
       "STATE-01 reads a beat's emphasis")
def step_7_floors_and_beat_states(scratch):
    texts = gold_texts()
    for identifier in re.findall(r"^### SHOT (SC10-SH\d+)", texts["scene"], re.MULTILINE):
        texts = edit(texts, "scene", f"SHOT {identifier}", remove=True)
    assert not helpers.lines_of(helpers.checked(texts, ["TIME-01", "STATE-01"], step=7), "TIME-01")
    short = edit(texts, "scene", "SHOTLIST SC10-LIST", "| subject: CH-IONA | time: 15 |",
                 "| subject: CH-IONA | time: 5 |")
    found = helpers.lines_of(helpers.checked(short, ["TIME-01"], step=7), "TIME-01")
    if helpers.excerpt_story() is None:
        return "skip"
    assert found and found[0].level == "W" and "SC10-SH150" in str(found[0]), found
    assert "TIME-01" in json.loads((SKILL / "schema" / "steps.json").read_text(encoding="utf-8"))["steps"][7][
        "checks"], "TIME-01 is not among step 7's checks"
    later = ("### STATE PR-FLASK.S04 Set down for good\n- element: PR-FLASK\n- from: SC10 | line: 489\n"
             "- state_line: the flask on the counter, its cap off\n- origin: invented\n")
    texts = edit(texts, "context", "STATE PR-FLASK.S03", add_after=later)
    texts = edit(texts, "scene", "BEAT SC10-B01", "- emphasis: PR-FLASK.S03 | level: 1",
                 "- emphasis: PR-FLASK.S04 | level: 1")
    found = helpers.lines_of(helpers.checked(texts, ["STATE-01"], step=7), "STATE-01", "SC10-B01")
    assert found and "PR-FLASK.S04" in str(found[0]), found
    return "a 5 s item under its floor warns at step 7; a beat naming a later state fails STATE-01"


# ---------------------------------------------------------------- F25: a rung's hold

@group("F25: a ladder rung's hold: short is read as medium with a note (FORM-13), never an error, so a finished "
       "project keeps passing; medium passes; steps 6 and 7 say what a rung may ask and what a rung on another beat sets")
def rung_hold(scratch):
    ladder = next(line for line in gold_texts()["context"].splitlines() if line.startswith("- rung: SC10"))
    held = re.search(r"\| hold: (\w+)", ladder).group(1)
    texts = edit(gold_texts(), "context", "LADDER", ladder, ladder.replace(f"| hold: {held}", "| hold: short"))
    result = helpers.checked(texts, ["FORM-04", "FORM-13"], story=False, step=6)
    refused = [problem for problem in result.problems if problem.check_id == "FORM-04" and "hold" in str(problem)]
    assert not refused, [str(problem) for problem in refused]
    said = " ".join(str(item) for item in list(result.problems) + list(getattr(result, "tidy_notes", []) or []))
    assert "read as medium" in said, said[:600]
    texts = edit(gold_texts(), "context", "LADDER", ladder, ladder.replace(f"| hold: {held}", "| hold: medium"))
    found = [problem for problem in helpers.checked(texts, ["FORM-04"], story=False, step=6).problems
             if problem.check_id == "FORM-04" and "hold" in str(problem)]
    assert not found, found
    phrases = {"steps/06 Film rules.md": "never on black or a card",
               "steps/07 Scene design and shot list.md": "a rung on another beat sets that beat's shot"}
    missing = [name for name, phrase in phrases.items() if phrase not in (SKILL / name).read_text(encoding="utf-8")]
    assert not missing, missing
    return "short read as medium with a note, medium kept; the two sentences written"


# ---------------------------------------------------------------- F26: questions without a shortening marker

@group("F26: a review question names a long speech by 'the line that starts' its first sentence, never '...', so a "
       "batch that copies the question word for word applies")
def questions_without_markers(scratch):
    from stage_tools.adopt_folder import QuestionMaker
    from stage_tools.checks_form import FormContext, run_form_checks
    from stage_tools.record_format import parse_text
    maker = QuestionMaker(helpers.check_run(gold_texts()), {})
    said, owner = maker.speech_said("Goods only. No persons.", "Jude")
    assert said == "the line that starts 'Goods only.'" and owner == "Jude's line that starts 'Goods only.'", owner
    assert maker.speech_said("Kitchen.", "Saye") == ("'Kitchen.'", "Saye's 'Kitchen.'")
    question = f"Shot 020: does the story let Jude be seen saying {said} (lines 18 to 19)?"
    text = (f"### REVIEW RV-SC10 Scene 10's review\n- scope: SC10\n- answer: {question} | answer: yes | "
            "evidence: shot 020\n\nEND OF FILE | Test | 1 records\n")
    record_file = parse_text(text, "inbox/U-10-Q01.md", SCHEMA)
    context = FormContext.for_records(SCHEMA, helpers.WORDS, [record_file], written_by_ai=True)
    found = [str(problem) for problem in run_form_checks([record_file], context, ["FORM-08"])]
    assert not found, found
    return "'the line that starts' its first sentence; FORM-08 accepts the copied question"


# ---------------------------------------------------------------- F27: "as before the fire"

@group("F27: FORM-08 reads 'as before' followed by a word ('as before the fire') as a time phrase; 'As before.' "
       "alone or opening a value is still a shortening marker")
def as_before_the_fire(scratch):
    from stage_tools.checks_form import find_marker
    for text in ("the light on her visor the same as before the fire and after the black",
                 "exactly as before the fire"):
        assert find_marker(text, ["as before"]) is None, text
    for text in ("As before.", "as before", "As before, the lamp on its hook."):
        assert find_marker(text, ["as before"]) == "as before", text
    return "two time phrases pass; three markers still caught"


# ---------------------------------------------------------------- F28: lamplight and lamps

@group("F28: COVER-08 finds 'lamplight' carried by a look whose main light is 'her suit lamps'; a word the look does "
       "not carry is still not")
def lamplight_and_lamps(scratch):
    from stage_tools.checks_coverage_time_state import light_word_carried_by_look
    look = FakeLook({"main_light": "her suit lamps"})
    assert light_word_carried_by_look("lamplight", look, {"suit", "lamps"})
    assert light_word_carried_by_look("lamp", look, {"suit", "lamps"})
    assert not light_word_carried_by_look("moonlight", look, {"suit", "lamps"})
    return "lamplight is carried by lamps; moonlight is not"


# ---------------------------------------------------------------- F29: SIDE-01 reads every word of a side

@group("F29: SIDE-01 accepts a side item 'ring hand' for a ring, needs no side for a helmet ring at the neck, and "
       "still asks for a finger ring's side")
def side_items_every_word(scratch):
    state = ("### STATE CH-ELI.S09 Suited\n- element: CH-ELI\n- from: SC10 | line: 489\n"
             "- state_line: {line}\n- side: {side}\n- origin: invented\n")
    cases = (("a white suit, the helmet ring at his neck", "none", False),
             ("a white suit, a plain gold ring on one hand", "ring hand | own: left | plot: yes", False),
             ("a white suit, a plain gold ring on one hand", "none", True))
    for line, side, fails in cases:
        texts = edit(gold_texts(), "context", "STATE PR-FLASK.S03", add_after=state.format(line=line, side=side))
        found = helpers.lines_of(helpers.checked(texts, ["SIDE-01"], story=False), "SIDE-01", "CH-ELI.S09")
        assert bool(found) is fails, (line, side, found)
    return "a ring hand covers the ring; a helmet ring needs no side; a bare ring still does"


# ---------------------------------------------------------------- F30: check --unit and other units' coverage

@group("F30: check --unit on a split scene's part 2 lists no coverage error that only the list unit can clear "
       "(they wait); once the list unit is done they are shown")
def unit_check_cited_coverage(scratch):
    import fix04_second_three_scene_test_acceptance as fix04
    project = fix04.split_scene_project(scratch, "f30 part 2")
    manifest = read_manifest(project)
    manifest["units_done"] = [entry for entry in manifest["units_done"]
                              if not str(entry.get("unit", "")).startswith("U-08-SC10")]
    manifest["units_done"].append({"unit": "U-07-SC10-P2", "applied": "2026-10-06T05:00:00", "records_written": [
        "BEAT SC10-B09", "BEAT SC10-B10", "BEAT SC10-B11", "SCENE SC10"]})
    manifest["batches"] = {}
    write_manifest(project, manifest)
    scene_file = next((project / "11 Scenes").glob("*.md"))
    scene_file.write_text(re.sub(r"### (?:SHOTLIST|SHOT|CUT) SC10-[^\n]*\n(?:(?!### |END OF FILE)[^\n]*\n)*", "",
                                 scene_file.read_text(encoding="utf-8")), encoding="utf-8")
    code, output = stage(["--project", project, "check", "--unit", "U-07-SC10-P2", "--story", helpers.EXCERPT])
    assert code == 0 and not error_lines(output, "COVER-04"), error_lines(output)
    assert "About records it cites" not in output and "Not yet due" in output, output[-600:]
    manifest = read_manifest(project)
    manifest["units_done"].append({"unit": "U-07-SC10-LIST", "applied": "2026-10-06T05:10:00"})
    write_manifest(project, manifest)
    code, output = stage(["--project", project, "check", "--unit", "U-07-SC10-P2", "--story", helpers.EXCERPT])
    assert "About records it cites" in output and error_lines(output, "COVER-04"), output[-600:]
    return "8 cited coverage lines wait for the list unit, and show once it is done"


# ---------------------------------------------------------------- F32: a mark inside a table-high object

@group("F32: GEOM-05 warns about a mark inside a table-high object (the counter), not one on a bed people lie on, "
       "and the gold passes")
def mark_inside_object(scratch):
    assert not helpers.lines_of(helpers.checked(gold_texts(), ["GEOM-05"], story=False), "GEOM-05")
    texts = edit(gold_texts(), "context", "LOCATION LOC-SAYE-KITCHEN", "- mark: SAYE_COUNTER | at: [3.3, 0.85]",
                 "- mark: SAYE_COUNTER | at: [3.3, 0.4]")
    found = helpers.lines_of(helpers.checked(texts, ["GEOM-05"], story=False), "GEOM-05")
    assert found and found[0].level == "W" and "counter" in str(found[0]), found
    texts = edit(gold_texts(), "context", "LOCATION LOC-SAYE-KITCHEN", "- mark: SAYE_COUNTER | at: [3.3, 0.85]",
                 "- mark: SAYE_COUNTER | at: [2.8, 1.8]")
    assert not helpers.lines_of(helpers.checked(texts, ["GEOM-05"], story=False), "GEOM-05"), "the table is a bed"
    return "a mark in the counter warns; one on the table Jude lies on does not"


# ---------------------------------------------------------------- F33: the TEXT template's quote

@group("F33: the TEXT template shows quote in double quotes, and a line filled in as shown passes FORM-04")
def text_template_quote(scratch):
    from stage_tools.checks_form import FormContext, run_form_checks
    from stage_tools.record_format import parse_text
    template = (SKILL / "templates" / "08 Places and things.md").read_text(encoding="utf-8")
    assert '| quote: "<the exact words inside the line' in template
    text = ('### TEXT TX-STOP A stop sign\n- kind: sign\n- words_from: 400 | quote: "STOP"\n- on: none\n'
            "- origin: story\n\nEND OF FILE | Test | 1 records\n")
    record_file = parse_text(text, "inbox/U-04-THINGS.md", SCHEMA)
    context = FormContext.for_records(SCHEMA, helpers.WORDS, [record_file], written_by_ai=True)
    found = [str(problem) for problem in run_form_checks([record_file], context, ["FORM-04"]) if "quote" in str(problem)]
    assert not found, found
    return "the template asks for the double quotes; a filled-in line passes"


# ---------------------------------------------------------------- F31, F34 to F52: the instructions

@group("F31, F34-F52, F53: the instructions say what the second full run had to guess (one phrase per entry)")
def instructions(scratch):
    phrases = {
        "steps/04 Characters, places and things.md": [
            "writes \"from scene NN\" in its `material`",                                  # F31
            "sends only its END line (`0 records`)",                                        # F45 (20)
            "the things unit also sends the mirror RULE's `governs` again",                 # F45 (13, 23)
            "adding a text RULE for ordinary printed words in the world",                    # F45 (22)
            "(`sets: none`; step 5 reads the answer into the state's sides)"],              # F45 (16)
        "templates/08 Places and things.md": ["\"from scene NN\" when it arrives later"],   # F31
        "steps/07 Scene design and shot list.md": [
            "alone, or when the world acts, name the person for both",                      # F34
            "a speech too long for one item is split by quoting",                           # F37
            "a flaw in an action line goes in the beat's `note`",                           # F46 (107)
            "written even when nobody moves",                                               # F46 (128)
            "the list unit sends it again when the list's average shot length lands elsewhere",  # F46 (101)
            "a black inside the scene takes a normal number with `kind: black`"],           # F48
        "steps/08 Shot details.md": [
            "`at` and `faces` may be left out where a set plan exists",                      # F35
            "`origin: story` when the line states it, else `inferred`",                     # F39
            "numbers need not follow story order",                                          # F39
            "a fade-in before the first shot is `SC10-C000`",                               # F48
            "The book prints `why` and `note` for the user"],                               # F53 (d)
        "cards/05 Characters.md": ["tempo: slow` (the body's tempo", "`skin_light: open` until the casting choice"],  # F36
        "cards/08 World, style and genre.md": ["of any one scene's light"],                 # F36
        "cards/07 Places, things and motifs.md": ["On its own shot a plant's or payoff's emphasis wins"],  # F41
        "reference/07 Report and message formats.md": ["Left from group 2: 2 warnings, in 13 Health check"],  # F42
        "templates/22 Rights and credits.md": ["but step 0 already writes it: text"],    # F43, X15
        "templates/10 Film rules.md": ["code writes it from that choice, never type it on a code surface"],  # F44
        "steps/01 Read the story.md": ["(with none, only its END line, `0 records`)"],     # F45 (3)
        "cards/01 Reading the whole story.md": ["written in its `story_job`"],              # F45 (7)
        "cards/17 Screens, text and in-story cameras.md": ["joined by a `continue` CUT",
                                                          "the in-story camera's, in metres"],  # F47
        "cards/12 Staging and composition.md": ["one it implies is `origin: inferred`",    # F46 (143)
                                                "Two people side by side in a car"],        # F49
        "cards/10 Camera.md": ["in open space with no up or down"],                         # F49
        "steps/10 Check and estimate.md": ["a fault no question asked about goes in the unit's report",
                                           "a \"no\" settles only what the user read"],     # F50
        "SKILL.md": ["a refused apply fixed in place is no round"],                         # F51
        "steps/16 Resume and recovery.md": ["N is the number apply names"],                 # F51, X15
    }
    missing = [(name, phrase) for name, wanted in phrases.items() for phrase in wanted
               if phrase not in (SKILL / name).read_text(encoding="utf-8")]
    assert not missing, missing
    assert "a night takes the number of the day before it" in SCHEMA.field("SCENE", "story_day")["meaning"]  # F45 (5)
    words = next(part for part in SCHEMA.field("SHOT", "hear")["sub_parts"] if part["key"] == "words")
    assert "on any surface" in words["meaning"], words                                     # F37
    return f"{sum(len(wanted) for wanted in phrases.values())} phrases in {len(phrases)} files"


# ---------------------------------------------------------------- F35: the self-test's note

@group("F35: the self-test's note gives the allowed values of every sub-part a line may carry (the hear item's path), "
       "as step 8's handout does")
def selftest_note_values(scratch):
    from stage_tools.read_story import selftest_shot_template
    template = selftest_shot_template(SCHEMA, SKILL, "SC99")
    path_line = next((line for line in template.splitlines() if line.startswith("> - hear path: ")), "")
    assert "direct" in path_line and "through_glass" in path_line, template[-800:]
    return path_line[:60]


@group("F37, F38, F40: a list item that quotes part of a speech owes only that part; a move may pass through a "
       "mark; a spoken line can plant and pay off, and FILM-02 reads it")
def split_speech_via_and_spoken_plant(scratch):
    from stage_tools.derive_fields import list_items, provisional_floor
    from stage_tools.film_pass import shots_linking
    from stage_tools.record_format import split_list
    run, breakdown = helpers.gold_breakdown()
    entry = breakdown.speech("SC10-D12")

    def hears_it(item):
        beats = [breakdown.record(beat, "BEAT") for beat in split_list(item.get("beats") or "")]
        return any(beat is not None and entry["line"] in breakdown.lines_of(beat) for beat in beats)

    item_identifier = next(identifier for identifier, item in list_items(breakdown, "SC10") if hears_it(item))
    whole = provisional_floor(breakdown, "SC10", item_identifier)
    first_sentence = entry["text"].split(". ")[0] + "."
    texts = edit(gold_texts(), "scene", "SHOTLIST SC10-LIST", f"- item: {item_identifier} |",
                 f"- item: {item_identifier} |")
    lines = texts["scene"].split("\n")
    index = next(position for position, line in enumerate(lines) if line.startswith(f"- item: {item_identifier} |"))
    lines[index] = re.sub(r"\| shows: (.*)$", lambda match: f'| shows: "{first_sentence}"; ' + match.group(1)
                          .replace('"', ""), lines[index])
    texts["scene"] = "\n".join(lines)
    run, breakdown = helpers.gold_breakdown(texts)
    part = provisional_floor(breakdown, "SC10", item_identifier)
    words = {name: count for name, _, count, _, _ in part.speech_parts}
    assert words.get("SC10-D12") == len(first_sentence.split()), (words, first_sentence)
    assert part.floor <= whole.floor, (part.floor, whole.floor)
    via = SCHEMA.field("MOVE", "via")
    assert via["kind"] == "text" and "MARK_NAME" in via["syntax"], via
    hear = {part["key"] for part in SCHEMA.field("SHOT", "hear")["sub_parts"]}
    assert {"plant", "payoff"} <= hear, hear
    texts = edit(gold_texts(), "scene", "SHOT SC10-SH020", "- hear: SC10-D01 | speaker: off_screen | at: 2.5",
                 "- hear: SC10-D01 | speaker: off_screen | at: 2.5 | plant: PL-08")
    run, _ = helpers.gold_breakdown(texts)
    linking = [(shot.identifier, element) for shot, element in shots_linking(run, "plant", "PL-08")]
    assert ("SC10-SH020", None) in linking and ("SC10-SH030", "PR-MINT.S01") in linking, linking
    return f"{item_identifier} owes {words['SC10-D12']} words of SC10-D12; via takes a mark; a line plants PL-08"


@group("F51, F52: apply says where it kept the inbox; a saved choice matched on beats counts the unit's own scene's "
       "beats as its own")
def apply_report_and_beat_uses(scratch):
    from stage_tools.make_handout import Workspace, reserve_lines
    project = gold_command_project(scratch, "f51 apply")
    review = "### REVIEW RV-SC10 Scene 10's review\n- scope: SC10\n- answer: Is it so? | answer: yes | evidence: shot 150\n"
    code, output = stage(["--project", project, "apply", write_inbox(project, "U-10-Q01.md", review)])
    assert code == 0 and "The inbox file is kept in For machines - do not edit/history/" in output, output[-400:]
    rules = project / "10 Film rules.md"
    text = rules.read_text(encoding="utf-8")
    held = ("### RESERVE RC-09 The held pause\n- choice: a pause held past the longest pause\n- match: pause_after = "
            "medium\n- max_uses: 1\n- allowed_in: SC10\n- never_on: none\n- because: PLAN\n- status: draft\n"
            "- locked: no\n\n")
    rules.write_text(text.replace("### RESERVE RC-01", held + "### RESERVE RC-01", 1), encoding="utf-8")
    _, lines = reserve_lines(Workspace(project), "SC10", [])
    line = next(line for line in lines if line.startswith("- RC-09"))
    assert "used 0 times outside this unit, 1 left" in line, line
    return "the kept copy named; the scene's own medium pause is not a use outside the unit"



# ---------------------------------------------------------------- F53: what the book shows a reader

def with_field(text, heading, name, value):
    """A record file's text with one field of one record ('### TYPE ID') set to a new value."""
    head, rest = text.split(f"### {heading}", 1)
    block, separator, tail = rest.partition("\n### ")
    block = re.sub(rf"^- {name}: .*$", f"- {name}: {value}", block, count=1, flags=re.MULTILINE)
    return head + f"### {heading}" + block + separator + tail


def replace_in_file(path, find, replace):
    text = Path(path).read_text(encoding="utf-8")
    assert find in text, f"{Path(path).name} does not hold {find!r}"
    Path(path).write_text(text.replace(find, replace, 1), encoding="utf-8")


@group("F53: the book names an eyeline point by the place's nearest mark or object, never nests a bracket, lists "
       "value and the ladder in its word list and flags card numbers, capitals and coordinates; REASON-03 takes a "
       "set-plan object named in plain words, never in capitals")
def book_reader_words(scratch):
    from stage_tools.make_exports import BOOK_READER_FAULTS
    from stage_tools.make_views import BOOK_WORDS, ProjectView, full_shot_rows, point_in_words
    project = gold_command_project(scratch, "f53 book")
    view = ProjectView(project)
    assert point_in_words(view, "SC10", "[2.8, 1.8]") == "the table", point_in_words(view, "SC10", "[2.8, 1.8]")
    assert point_in_words(view, "SC10", "[5.7, 3.5]") == "a point near the fridge", point_in_words(view, "SC10", "[5.7, 3.5]")
    text = view.names.text("the far frame on the 85 exception (LX-01) with deep focus", "SC10")
    assert not re.search(r"\([^()]*\(", text) and "(the early 85, a lens exception)" in text, text
    replace_in_file(project_file(project, "Scene 10 - Saye's kitchen.md"), "| eyeline: CH-SAYE ",
                    "| eyeline: [2.8, 0.1] ")
    view = ProjectView(project)
    rows = [row for shot in view.shots("SC10") for label, row in full_shot_rows(view, shot, "SC10")
            if label == "In the frame"]
    assert any("eyes on the mint" in row for row in rows) and not any("[2.8" in row for row in rows), rows[:3]
    words = {word for word, _ in BOOK_WORDS}
    assert {"value", "ladder of closest shots"} <= words, words
    sample = "the CONTROL_BOX at [2.0, 4.0] (card 15: lock the camera)"
    assert all(pattern.search(sample) for pattern in BOOK_READER_FAULTS)
    why = "It holds {} bare and white, nothing of anybody on it."
    rack = ("- object: DRYING_RACK | at: [4.4, 0.3] | size: [0.4, 0.3, 0.4] | base: 0.9 | material: steel wire | "
            "meaning: nothing drying on it | furniture: none\n- object: TABLE |")
    texts = edit(gold_texts(), "context", "LOCATION LOC-SAYE-KITCHEN", "- object: TABLE |", rack)
    texts["scene"] = with_field(texts["scene"], "SHOT SC10-SH030", "why", why.format("the drying rack"))
    plain = helpers.lines_of(helpers.checked(texts, ["REASON-03"]), "REASON-03", "SC10-SH030")
    assert not plain, plain
    texts["scene"] = texts["scene"].replace(why.format("the drying rack"), why.format("the DRYING_RACK"))
    capitals = helpers.lines_of(helpers.checked(texts, ["REASON-03"]), "REASON-03", "SC10-SH030")
    assert capitals and "a line number alone does not anchor it" in capitals[0], capitals
    return "eyes on the mint; no nested bracket; 2 words added; 3 patterns flagged; the drying rack anchors, " \
        "DRYING_RACK not"


# ---------------------------------------------------------------- F54: the book never contradicts itself

@group("F54: a turn has one ordinal in At a glance and the one-line list; copied story plan lines start with a "
       "capital; moments join with one mark; 'says it' gets its words; a state's label shows where it first shows; "
       "an addition the scene lists is said once; the log never says 'The the'")
def book_says_it_once(scratch):
    from stage_tools.fill_code_fields import sentence_start
    from stage_tools.make_views import (ProjectView, additions_of_scene, full_shot_rows, says_it_with_words,
                                        scene_at_a_glance, shot_line, story_plan_plain_part, turn_words)
    project = gold_command_project(scratch, "f54 book")
    view = ProjectView(project)
    turn_shot = view.turn_shot_for("SC10-B11")
    turn_shot = turn_shot.identifier if hasattr(turn_shot, "identifier") else turn_shot
    assert turn_words(view, turn_shot) == "another turn", turn_words(view, turn_shot)
    assert "Another turn is beat 11" in " ".join(scene_at_a_glance(view, "SC10"))
    replace_in_file(next(project.glob("05 *.md")), "- what: Iona, Jude and Eli were turned",
                    "- what: the three of them were turned")
    scenes = project_file(project, "Scene 10 - Saye's kitchen.md")
    replace_in_file(scenes, "- additions: none", "- additions: Saye's phone on the counter by the flask (listed in "
                    "the scene's additions)")
    view = ProjectView(project)
    plan = "\n".join(story_plan_plain_part(view, []))
    assert "Group of scenes 3: The wrong world" in plan and "- The three of them were turned" in plan, plan[:600]
    assert len(additions_of_scene(view, "SC10")) == 4, additions_of_scene(view, "SC10")
    said = next(shot for shot in view.shots("SC10")
                if any("says it" in (moment.get("shows") or "") for moment in view.items(shot, "moment")))
    heard = view.items(said, "hear")
    speaking = SimpleNamespace(items=view.items, speech=lambda identifier: {"text": "I'm putting this down."})
    line = says_it_with_words(speaking, said, "she straightens and says it; her eyes stay on Saye")
    assert len(heard) == 1 and line == 'she straightens and says "I\'m putting this down."; her eyes stay on Saye', \
        line
    said = said.identifier
    first_moment = next(moment for moment in view.items(view.record("SC10-SH010", "SHOT"), "moment"))
    replace_in_file(scenes, first_moment.get("shows"), first_moment.get("shows").rstrip(".") + ".")
    view = ProjectView(project)
    assert ".;" not in shot_line(view, "SC10-SH010", "SC10"), shot_line(view, "SC10-SH010", "SC10")
    labelled = []
    for shot in view.shots("SC10"):
        for item in view.items(shot, "subject"):
            if item.first == "CH-IONA.S02":
                rows = [row for label, row in full_shot_rows(view, shot, "SC10") if label == "In the frame"]
                labelled.append(next(row for row in rows if row.startswith("Iona")))
    assert len(labelled) >= 2 and labelled[0].startswith("Iona (") and labelled[1].startswith("Iona;"), labelled[:2]
    assert sentence_start("the answer to choice 9") == "The answer to choice 9"
    return f"another turn in both places; a capital; one mark; {said} says its words; label once of {len(labelled)}"


# ---------------------------------------------------------------- F55: the health check's first line

@group("F55: 'In short' names what needs the user: the three scenes to read once the scores exist and the finished "
       "check waits, and each open choice; the skipped checks line asks nothing of the reader")
def in_short_names_what_waits(scratch):
    from stage_tools.check_records import in_short_line, what_needs_you
    scores = "".join(f"- score: {number} | score: 2 | evidence: shot 150\n" for number in range(1, 11))
    review = f"### REVIEW RV-SC10 Scene 10's scores\n- scope: SC10\n{scores}"
    texts = edit(gold_texts(), "scene", "SHOT SC10-SH010", add_after=review)
    run = helpers.check_run(texts)
    count, names = what_needs_you(run)
    assert count >= 1 and names[0] == "reading three scenes", (count, names)
    result = SimpleNamespace(counts={}, tidy_notes=[], run=None)
    line = in_short_line(result, count, names)
    assert line.startswith(f"In short: {count} thing") and "(reading three scenes" in line, line
    run.manifest = {"checkpoints": {"CHECKPOINT-ACCEPTANCE": {"passed": "2026-10-06T03:00:00"}}}
    assert "reading three scenes" not in what_needs_you(run)[1]
    texts = gold_texts()
    texts["context"] = with_field(with_field(texts["context"], "CHOICE CHOICE-004", "asked", "yes"),
                                  "CHOICE CHOICE-004", "status", "open")
    run = helpers.check_run(texts)
    count, names = what_needs_you(run)
    assert "choice 4" in names, names
    from stage_tools.check_records import health_check_plain_part
    result = helpers.checked(gold_texts(), ["PLAN-04", "CITE-02"])
    lines = health_check_plain_part(None, result, None, None, False, True, None)
    skipped = next((line for line in lines if "could not run in full" in line), "")
    assert skipped.endswith("nothing here needs you (the reasons are for the AI, below the line)."), skipped
    return line


# ---------------------------------------------------------------- F56: 14 Time and cost

@group("F56: 14 Time and cost rounds the weeks before comparing, names the first estimate, says 'first estimate' "
       "for a scene's planned length and warns when the film passes the short film the user chose")
def time_and_cost_words(scratch):
    from stage_tools.estimate import film_checks
    project = gold_command_project(scratch, "f56 estimate")
    code, output = stage(["--project", project, "estimate"])
    assert code == 0, output[-400:]
    page = (project / "14 Time and cost.md").read_text(encoding="utf-8")
    assert "(first estimate " in page and "(planned " not in page, [line for line in page.splitlines()
                                                                    if "scene 10" in line][:2]

    class Prices:
        def warning_band(self, name, default):
            return default

    def film(weeks, minutes):
        return SimpleNamespace(target_s=None, runtime_s=(minutes * 60 - 60, minutes * 60, minutes * 60 + 60),
                               partial=False, source_kind="prose", average_shot_s=None, generation_factor=None,
                               total_shots=0, format="short", hours_shown=True, weeks={"central": weeks},
                               hours_per_week=20, warnings=[], notes=[], scenes=[])
    breakdown = SimpleNamespace(project=FakeLook({"format": "short"}))
    near = film(26.4, 30)
    film_checks(near, breakdown, helpers.CONSTANTS, Prices())
    assert not near.warnings, near.warnings
    long = film(27, 50)
    film_checks(long, breakdown, helpers.CONSTANTS, Prices())
    assert any("longer than the short film you chose (40 minutes or less)" in line for line in long.warnings), \
        long.warnings
    assert any("about 27 weeks, longer than 26" in line for line in long.warnings), long.warnings
    return "first estimate named; 26.4 weeks no warning; a 50-minute short warned"


# ---------------------------------------------------------------- F57: 01 Choices after read

@group("F57: after read, 01 Choices is made again from its records: At a glance counts the choices that wait")
def choices_after_read(scratch):
    project = helpers.small_project(scratch, "f57 read")
    plain = (project / "01 Choices.md").read_text(encoding="utf-8").split(helpers.DIVIDER_LINE, 1)[0]
    counted = re.search(r"(\d+) waiting for you", plain)
    waiting = plain.split("## Waiting for you", 1)[1].split("\n## ", 1)[0]
    listed = len(re.findall(r"^\d+\. ", waiting, re.MULTILINE))
    assert counted and int(counted.group(1)) == listed and listed >= 1, plain[:600]
    assert "Nothing is waiting for you" not in waiting
    return f"{listed} waiting, counted and listed"


# ---------------------------------------------------------------- F58: check --unit messages

@group("F58: check --unit says how many records were sent and that the last batch adds the scene and its list, "
       "names the step both ways, counts left-out lines on the scene, and ends with 'not applied yet' when the "
       "unit's inbox file waits")
def unit_check_messages(scratch):
    from stage_tools.check_records import UnitView
    project = gold_command_project(scratch, "f58 unit")
    code, output = stage(["--project", project, "check", "--unit", "U-08-SC10-B2", "--story", helpers.EXCERPT])
    assert "plus the scene and its list" in output and "(check --step 8)" in output, output[-500:]
    code, output = stage(["--project", project, "check", "--unit", "U-08-SC10-B1", "--story", helpers.EXCERPT])
    assert "plus the scene and its list" not in output, output[-500:]
    write_inbox(project, "U-08-SC10-B1.md", "### SHOT SC10-SH010 Saye in her doorway\n- size: wide\n")
    code, output = stage(["--project", project, "check", "--unit", "U-08-SC10-B1", "--story", helpers.EXCERPT])
    last = output.strip().splitlines()[-1]
    assert last.startswith("Not applied yet: U-08-SC10-B1.md"), last
    view = UnitView(SimpleNamespace(scene="SC10"), {"SC10-SH010"}, set())
    problems = [SimpleNamespace(record=label, level="W", check_id="TIME-03") for label in
                ("SC10-SH010", "SC10-LIST", "SC10", "SC09-SH010")]
    own, cited, others = view.split(problems)
    assert len(own) == 1 and others == 3 and view.scene_wide_left_out == 2, (own, others, view.scene_wide_left_out)
    return "sent and added said apart; the step both ways; 2 scene-wide lines counted; not applied yet last"


# ---------------------------------------------------------------- F59: texts in a scene's handout

@group("F59: a text's printed words in capitals match only as written, and a text whose words_from or note line "
       "lies in the scene is in it")
def texts_in_scene(scratch):
    from stage_tools.make_handout import elements_in_scene
    texts_added = ("### TEXT TX-MINT-WORD The word on the pot\n- kind: label\n- words: MINT\n- on: none\n"
                   "- origin: invented\n\n### TEXT TX-STREET-SIGN The street sign\n- kind: sign\n- words: N25\n"
                   "- on: none\n- origin: invented\n- note: \"A pot of mint\" (line 410); the words are invented.\n")
    texts = edit(gold_texts(), "context", "TEXT TX-TITLE-CATCH", add_after=texts_added)
    workspace = GoldStoryWorkspace(texts)
    first, last = workspace.scene_lines("SC10")
    assert first <= 410 <= last, (first, last)
    found = elements_in_scene(workspace, "SC10")
    assert "TX-MINT-WORD" not in found and "TX-STREET-SIGN" in found, [item for item in found if item.startswith("TX")]
    return "MINT in capitals no match for 'mint'; a note's line 410 places the sign in scene 10"


# ---------------------------------------------------------------- F61: three checks read words in any form

@group("F61: WORDS-02 leaves 'the screen left blank' alone but still catches 'exits screen left'; CRAFT-19 takes "
       "'standing' or a MOVE ID for staging; plural words match their singular")
def words_in_any_form(scratch):
    from stage_tools.checks_craft_reasons_words import content_words, retired_words_in_text
    assert not retired_words_in_text("the screen left blank after the cut", helpers.WORDS)
    assert retired_words_in_text("Iona exits screen left.", helpers.WORDS)
    assert retired_words_in_text("she stands screen left of the door", helpers.WORDS)
    assert set(content_words("Iona stands by the tables")) == set(content_words("Iona stand by the table"))
    assert "glass" in content_words("the glass")
    texts = edit(gold_texts(), "scene", "SCENE SC10", "| holds_baseline: no | because: CR-IONA, RC-01, LX-01, SC10-B07",
                 "| holds_baseline: yes | because: CR-IONA, RC-01, LX-01, SC10-B07")
    texts = edit(texts, "scene", "SCENE SC10", "because: LOC-SAYE-KITCHEN, SC10-B04, SC10-B11",
                 "because: LOC-SAYE-KITCHEN, SC10-B04, SC10-B07, SC10-B11")
    old = "only the camera (the scene's one close-up, held) and the sound (room sound only) change."

    def idea_lines(words):
        changed = edit(dict(texts), "scene", "SCENE SC10", old, words)
        return [problem for problem in helpers.lines_of(helpers.checked(changed, ["CRAFT-19"]), "CRAFT-19", "SC10")
                if "does not name" in str(problem)]
    assert idea_lines("only Iona's place and the sound (room sound only) change."), "the check no longer catches"
    assert not idea_lines("only where Iona is standing and the sound (room sound only) change.")
    assert not idea_lines("only Iona's move SC10-M01 and the sound (room sound only) change.")
    return "screen left blank passes; standing and SC10-M01 name staging; stands = stand"


# ---------------------------------------------------------------- F62 and F63

@group("F62, F63: next names the add-ons without step numbers; a heading sharing one word with another place of the "
       "same kind waits for its own place")
def add_ons_and_headings(scratch):
    from stage_tools.fill_code_fields import best_location_for
    source = (SKILL / "tools/stage_tools/make_handout.py").read_text(encoding="utf-8")
    assert "storyboards (step 12)" not in source and "storyboards, grey previews (Claude Code only)" in source
    places = [SimpleNamespace(identifier=identifier, title=title) for identifier, title in (
        ("LOC-ELI-ROOM", "Eli's room"), ("LOC-PASSAGE", "The passage, later the receiving room"),
        ("LOC-TREATMENT-FLOOR", "The treatment floor"), ("LOC-FREIGHT-CAGE", "The freight cage"))]

    def chosen(heading):
        found = best_location_for(heading, places)
        return found.identifier if found else None
    assert chosen("QUARANTINE - IONA'S ROOM") is None and chosen("SHIP - COLLECTION ROOM") is None
    assert chosen("FREIGHT SHAFT") is None and chosen("FREIGHT CAGE") == "LOC-FREIGHT-CAGE"
    assert chosen("MAINTENANCE PASSAGE") == "LOC-PASSAGE" and chosen("ELI'S ROOM") == "LOC-ELI-ROOM"
    assert chosen("TREATMENT FLOOR - CORRIDOR") == "LOC-TREATMENT-FLOOR"
    return "add-ons by name; Iona's room waits for its own place, the passage still found"


# ================================================================ the cross-examination of this round's fixes
# One group per finding X01 to X16 of "cross-examination.md" that was repaired; each fails without its repair.

# ---------------------------------------------------------------- X01: only a state's sides are merged

@group("X01: only a state's sides merge by name (an era choice replaces the whole field); a side SETVALUE saying "
       "none is refused; a changed answer takes out the sides the earlier option named")
def side_merge_only_for_sides(scratch):
    from stage_tools.project_files import set_value_lines
    from stage_tools.record_format import make_record
    eras = [("era", "a | from: 10 | to: 261 | frame: original"), ("era", "b | from: 263 | to: 1563 | frame: original"),
            ("era", "c | from: 1565 | to: 1852 | frame: reversed")]
    rule = make_record("RULE", "WR-MIRROR", fields=eras)
    two_eras = make_record("SETVALUE", "CHOICE-010-A", fields=[
        ("target", "WR-MIRROR"), ("era", "a | from: 10 | to: 261 | frame: original"),
        ("era", "b | from: 263 | to: 1852 | frame: original")])
    assert set_value_lines(rule, "era", two_eras, SCHEMA) == two_eras.get_all("era"), \
        set_value_lines(rule, "era", two_eras, SCHEMA)
    project = gold_command_project(scratch, "x01 sides")
    continuity = project / "09 Continuity.md"
    inbox = write_inbox(project, "U-05-CONT - fix 1.md", "### CHOICE CHOICE-014\n- answer: b\n\n"
                        "### SETVALUE CHOICE-014-B\n- target: CH-IONA.S02\n- side: none\n")
    code, output = stage(["--project", project, "apply", inbox])
    assert code == 1 and error_lines(output, "FORM-04"), output[-600:]
    assert "- side: none" not in record_text(continuity, "STATE CH-IONA.S02")
    inbox = write_inbox(project, "U-05-CONT - fix 2.md", "### CHOICE CHOICE-014\n- answer: b\n\n"
                        "### SETVALUE CHOICE-014-B\n- target: CH-IONA.S02\n"
                        "- side: torn sleeve | own: left | plot: no\n- side: palm graze | own: left | plot: yes\n")
    code, output = stage(["--project", project, "apply", inbox])
    assert code == 0, output[-600:]
    sides = field_values(record_text(continuity, "STATE CH-IONA.S02"), "side")
    assert sorted(sides) == ["palm graze | own: left | plot: yes", "torn sleeve | own: left | plot: no",
                             "wedding ring | own: left | plot: yes"], sides
    return "eras replaced whole; side none refused; option a's two sides gone, b's two added, the ring kept"

# ---------------------------------------------------------------- X02: "as before" and a joining word

@group("X02: FORM-08 still finds 'as before' followed by a joining word ('but', 'and'); a time phrase after it "
       "('the fire', 'she wakes') still passes")
def as_before_then_joining_word(scratch):
    from stage_tools.checks_form import find_marker
    for text in ("As before but wetter.", "Same as before but with a scar on the cheek.",
                 "The same framing, lens and light as before and the lamp lit."):
        assert find_marker(text, ["as before"]) == "as before", text
    for text in ("exactly as before the fire", "the lamp as before she wakes", "the sound goes on as before"):
        assert find_marker(text, ["as before"]) is None, text
    return "three shortenings caught; two time phrases and a plain ending pass"


# ---------------------------------------------------------------- X03: composited words keep the sentence's meaning

@group("X03: words added later keep their sentence's meaning: words that stand for their thing become the thing the "
       "TEXT's title names, a single mark becomes a letter with the right article, and a quoted cue keeps its place")
def words_added_later_keep_meaning(scratch):
    from stage_tools.compile_prompts import (composited_texts, leave_words_for_later, thing_named_by_title,
                                             without_quoted_speech)
    _, breakdown = helpers.gold_breakdown(gold_texts(), story=False)
    assert composited_texts(breakdown, breakdown.record("SC10-SH990", "SHOT")) == \
        [("THE CATCH", "title_card", "title card")], composited_texts(breakdown, breakdown.record("SC10-SH990", "SHOT"))
    assert thing_named_by_title("The STOP button", "STOP") == "button"
    assert thing_named_by_title("The diagram's line label", "PASSAGE FLOOR") == "diagram's line label"
    assert thing_named_by_title("The carriage's F", "F") == "" and \
        thing_named_by_title("The name on Nell's file", "NELL ROWAN.") == ""
    floor = [("PASSAGE FLOOR", "screen", "diagram's line label")]
    cases = (
        ("her elbow hits the red STOP.", [("STOP", "label", "button")], "her elbow hits the red button."),
        ("a small figure drives her elbow into STOP.", [("STOP", "label", "button")],
         "a small figure drives her elbow into the button."),
        ("a second line, the ship's deck, level with PASSAGE FLOOR.", floor,
         "a second line, the ship's deck, level with the diagram's line label."),
        ("the second line dipped below PASSAGE FLOOR.", floor,
         "the second line dipped below the diagram's line label."),
        ("its two marks: TURN below, CROSS AT 0 beside RECEIVING.",
         [("TURN", "visor", "visor's mark"), ("CROSS AT 0", "visor", "visor's crossing mark"),
          ("RECEIVING", "visor", "visor's room label")],
         "its two marks: the visor's mark below, the visor's crossing mark beside the visor's room label."),
        ("her hand slides a paper F along the bench: it stays an F.", [("F", "label", "")],
         "her hand slides a paper letter along the bench: it stays a letter."),
        ("a horizontal line marked PASSAGE FLOOR.", floor, "a horizontal line marked with words added later."),
        ("the blanket with OSTREL stitched backwards", [("OSTREL", "label", "word on the blanket")],
         "the blanket with words added later stitched backwards"))
    for text, composited, expected in cases:
        assert leave_words_for_later(text, composited) == expected, (text, leave_words_for_later(text, composited))
    assert without_quoted_speech('at "Jude\'s blood" her eyes go down to her hands', ["Not his. Jude's blood."]) == \
        "at that line her eyes go down to her hands"
    return "the button, the line's label, the visor's marks, a paper letter, 'at that line'"


# ---------------------------------------------------------------- X04: text none keeps a featured text's floor

@group("X04: a shot that writes 'text: none' still owes reading time for a plot-critical text whose thing it shows "
       "at emphasis 2, or whose words its moments quote; at emphasis 1 and unquoted it owes none (F17)")
def text_none_keeps_featured_text(scratch):
    from stage_tools.derive_fields import time_floor
    label = ("### TEXT TX-FLASK-LABEL The flask's label\n- kind: label\n- words: KEEP FROZEN AT ALL TIMES\n"
             "- on: PR-FLASK\n- origin: invented\n- words_from: 400\n- reader: CH-SAYE\n- plot_critical: yes\n"
             "- emphasis: 2\n- method: composite\n- animation: none\n")
    texts = edit(gold_texts(), "context", "TEXT TX-TITLE-CATCH", add_after=label)

    def floor_texts(changed):
        _, breakdown = helpers.gold_breakdown(changed, story=False)
        return [name for name, _, _ in time_floor(breakdown, breakdown.record("SC10-SH020", "SHOT")).text_parts]
    assert floor_texts(texts) == [], "F17: at emphasis 1 and unquoted, text: none owes nothing"
    featured = edit(dict(texts), "scene", "SHOT SC10-SH020", "- thing: PR-FLASK.S03 | emphasis: 1 |",
                    "- thing: PR-FLASK.S03 | emphasis: 2 |")
    assert floor_texts(featured) == ["TX-FLASK-LABEL"], floor_texts(featured)
    quoted = edit(dict(texts), "scene", "SHOT SC10-SH020", "shows: the flask in his fist,",
                  "shows: the flask in his fist, KEEP FROZEN AT ALL TIMES on its side,")
    assert floor_texts(quoted) == ["TX-FLASK-LABEL"], floor_texts(quoted)
    return "unfeatured: no floor; at emphasis 2 or quoted in a moment: the label's floor"


# ---------------------------------------------------------------- X05: a camera on the scene's own place is measured

@group("X05: GEOM-04 measures a camera mounted on the scene's own place (it moves with the set plan) and still skips "
       "one mounted on a person")
def camera_on_own_place_measured(scratch):
    texts = edit(gold_texts(), "scene", "SHOT SC10-SH150", "- size: close_up", "- size: wide")
    own = edit(dict(texts), "scene", "SETUP SC10-SU02", "- mount: world", "- mount: LOC-SAYE-KITCHEN")
    result = helpers.checked(own, ["GEOM-04"], story=False)
    assert helpers.lines_of(result, "GEOM-04", "SC10-SH150"), "a camera on the kitchen itself was not measured"
    assert not any(check == "GEOM-04" for check, _ in result.skipped), result.skipped
    person = edit(dict(texts), "scene", "SETUP SC10-SU02", "- mount: world", "- mount: CH-IONA")
    result = helpers.checked(person, ["GEOM-04"], story=False)
    assert not helpers.lines_of(result, "GEOM-04", "SC10-SH150"), helpers.lines_of(result, "GEOM-04")
    return "on the kitchen: measured and warned; on Iona: skipped"


# ---------------------------------------------------------------- X06: a straight cut across a part boundary

@group("X06: GEOM-01 still pairs two singles in different parts when one cuts straight to the other: camera B "
       "moved across the line for shot 150 (part 1) fails against shot 160 (part 2)")
def straight_cut_across_parts(scratch):
    texts = edit(gold_texts(), "scene", "SETUP SC10-SU02", "- at: [2.55, 1.2, 1.57]", "- at: [3.35, 1.2, 1.57]")
    texts = edit(texts, "scene", "SETUP SC10-SU02", "- look_at: [2.95, 2.55, 1.57]", "- look_at: [2.75, 2.55, 1.57]")
    problems = helpers.lines_of(helpers.checked(texts, ["GEOM-01"], story=False), "GEOM-01")
    named = " ".join(str(problem) for problem in problems)
    assert len(problems) == 1 and "SC10-SH160" in named and "SC10-SH150" in named, named
    return "the crossed cut from shot 150 to shot 160 is found; nothing else"


# ---------------------------------------------------------------- X07: silent third none with three people present

@group("X07: CRAFT-24 warns when a turn's silent_third is none while three or more people are in its shots, and "
       "stays quiet on a turn with two people")
def silent_third_none_with_three(scratch):
    texts = edit(gold_texts(), "scene", "BEAT SC10-B07", "- silent_third: CH-ELI", "- silent_third: none")
    found = helpers.lines_of(helpers.checked(texts, ["CRAFT-24"], story=False), "CRAFT-24")
    assert len(found) == 1 and "SC10-B07" in str(found[0]) and "is none" in str(found[0]), found
    texts = edit(gold_texts(), "scene", "BEAT SC10-B09", "- turn: none", "- turn: turn")
    texts = edit(texts, "scene", "BEAT SC10-B09", "- silent_third: CH-ELI", "- silent_third: none")
    found = helpers.lines_of(helpers.checked(texts, ["CRAFT-24"], story=False), "CRAFT-24")
    assert not found, found
    return "none on the four-person turn warned; none on a two-person turn passes"


# ---------------------------------------------------------------- X08: the only place of its kind

@group("X08: a heading whose extra word only describes ('THE OLD KITCHEN', 'MOVING CAR') still finds the only place "
       "of its kind; a heading naming another kind ('FREIGHT SHAFT') still waits for its own place")
def heading_finds_only_place_of_its_kind(scratch):
    from stage_tools.fill_code_fields import best_location_for
    places = [SimpleNamespace(identifier=identifier, title=title) for identifier, title in (
        ("LOC-SAYE-KITCHEN", "Saye's kitchen"), ("LOC-IONA-BEDROOM", "Iona's bedroom"),
        ("LOC-FREIGHT-SHAFT", "The freight shaft"), ("LOC-CAR", "Iona's car"))]

    def chosen(heading, among=places):
        found = best_location_for(heading, among)
        return found.identifier if found else None
    assert chosen("INT. THE OLD KITCHEN - NIGHT") == "LOC-SAYE-KITCHEN"
    assert chosen("UPSTAIRS BEDROOM") == "LOC-IONA-BEDROOM"
    assert chosen("THE DEEP SHAFT") == "LOC-FREIGHT-SHAFT" and chosen("MOVING CAR") == "LOC-CAR"
    cage = [SimpleNamespace(identifier="LOC-FREIGHT-CAGE", title="The freight cage"),
            SimpleNamespace(identifier="LOC-ELI-ROOM", title="Eli's room")]
    assert chosen("FREIGHT SHAFT", cage) is None and chosen("DEMONSTRATION ROOM", cage) is None
    return "the old kitchen, the upstairs bedroom, the deep shaft and the moving car found; the freight shaft waits"


# ---------------------------------------------------------------- X09: an eyeline point in the book

@group("X09: the book never names an eyeline point after a mark named for a person ('IONA_BETWEEN'), and says 'a fixed "
       "point' when nothing on the plan is within 1.5 metres")
def eyeline_point_words(scratch):
    from stage_tools.make_views import ProjectView, point_in_words
    view = ProjectView(gold_command_project(scratch, "x09 points"))
    beside_mark = point_in_words(view, "SC10", "[4.2, 1.45]")
    assert "iona" not in beside_mark and beside_mark == "a point near the lamp", beside_mark
    assert point_in_words(view, "SC10", "[8.0, 6.0]") == "a fixed point", point_in_words(view, "SC10", "[8.0, 6.0]")
    assert point_in_words(view, "SC10", "[5.7, 3.5]") == "a point near the fridge"
    return "the lamp instead of Iona's mark; a far point is a fixed point; the fridge still named"


# ---------------------------------------------------------------- X10: a speaking shot kept whole only when needed

@group("X10: a speaking shot longer than the scene model's clip is kept whole only when chaining it would cut through "
       "its line: a 20-second shot whose 2-second line starts at 0 still chains on a 15-second model")
def speaking_shot_whole_only_when_cut(scratch):
    from stage_tools.compile_prompts import Adapters, able
    adapters = Adapters()
    fifteen_seconds = adapters.video.get("kling-3.0-omni")
    plan = SimpleNamespace(held=False, held_why="", whole_for_speech=True, needed_s=21.5, screen_time=20.0,
                           handles_s=0.75, speech_spans=[(0.0, 2.0)], start_picture=False, end_picture=False,
                           guide_video=False, performance=False, sends_speech=True, recurring=False,
                           faces_to_reference=0)
    assert able(adapters, "kling-3.0-omni", fifteen_seconds, plan)[0], "a line far from the cut kept the shot whole"
    plan.speech_spans = [(9.0, 11.0)]
    assert not able(adapters, "kling-3.0-omni", fifteen_seconds, plan)[0], "the chain's cut at 10 s splits the line"
    plan.speech_spans = None
    assert not able(adapters, "kling-3.0-omni", fifteen_seconds, plan)[0], "a line at an unknown time stays whole"
    return "line at 0-2 s: chained; line across the 10-second cut or at an unknown time: kept whole"


# ---------------------------------------------------------------- X11: a seal ring is a finger ring

@group("X11: SIDE-01 still asks for the side of a seal ring (a signet ring on a finger); a helmet ring needs none")
def seal_ring_needs_side(scratch):
    state = ("### STATE CH-ELI.S09 Suited\n- element: CH-ELI\n- from: SC10 | line: 489\n"
             "- state_line: {line}\n- side: none\n- origin: invented\n")
    for line, fails in (("a gold seal ring on his little finger", True), ("a white suit, the helmet ring at his neck",
                                                                           False)):
        texts = edit(gold_texts(), "context", "STATE PR-FLASK.S03", add_after=state.format(line=line))
        found = helpers.lines_of(helpers.checked(texts, ["SIDE-01"], story=False), "SIDE-01", "CH-ELI.S09")
        assert bool(found) is fails, (line, found)
    return "the seal ring needs its side; the helmet ring does not"


# ---------------------------------------------------------------- X12: the film pass's check after later changes

@group("X12: the film pass's check counts only when it passed after the judgement's last repair and after every fix "
       "applied since")
def film_pass_check_after_changes(scratch):
    from stage_tools.make_handout import film_pass_checked

    def checked(units, passed):
        return film_pass_checked(SimpleNamespace(manifest={"units_done": units, "checks_passed": {"step 9": passed}}))
    judged = {"unit": "U-09-JUDGE", "applied": "2026-10-06T01:39:58", "last_repair": "2026-10-06T01:45:07"}
    assert not checked([judged], "2026-10-06T01:42:00"), "a check before the judgement's repair counted"
    assert checked([judged], "2026-10-06T01:46:00")
    fixed = {"unit": "U-08-SC10-B1", "applied": "2026-10-05T18:30:55", "last_repair": "2026-10-06T02:15:29"}
    assert not checked([judged, fixed], "2026-10-06T01:46:00"), "a check before a later fix counted"
    assert checked([judged, fixed], "2026-10-06T02:16:00")
    return "a check before the judgement's repair or a later fix does not count; one after both does"


# ---------------------------------------------------------------- X13: a passed long list stays in the health check

@group("X13: a passed list far from the first estimate (a note) is listed in 13 Health check under 'Kept on purpose' "
       "with its size and direction")
def passed_list_kept_on_purpose(scratch):
    from stage_tools.check_records import health_check_plain_part
    texts = edit(gold_texts(), "context", "SCENE SC10", "- target_duration_s: 110", "- target_duration_s: 40")
    result = helpers.checked(texts, ["TIME-03"], story=False)
    lines = "\n".join(health_check_plain_part(None, result, None, None, False, True, None))
    kept = lines.split("## Kept on purpose", 1)
    assert len(kept) == 2, lines[:900]
    assert re.search(r"runs \d+ seconds, [\d.]+ times the first estimate of 40 seconds: kept on purpose; you passed "
                     r"this list\.", kept[1]), kept[1][:600]
    return "the passed list's length is kept on purpose, with its size and direction"


# ---------------------------------------------------------------- X14: a move's marks are checked

@group("X14: GEOM-05 warns when a move's from, via or to is no mark, object or point of the set plan (a misspelt "
       "mark was dropped without a word); the plan's own names pass")
def move_marks_checked(scratch):
    found = helpers.lines_of(helpers.checked(gold_texts(), ["GEOM-05"], story=False), "GEOM-05")
    assert not found, found
    texts = edit(gold_texts(), "scene", "MOVE SC10-M01", "- to: SAYE_COUNTER", "- to: SAYE_CUONTER")
    found = helpers.lines_of(helpers.checked(texts, ["GEOM-05"], story=False), "GEOM-05")
    assert len(found) == 1 and "SAYE_CUONTER" in str(found[0]) and found[0].level == "W", found
    texts = edit(gold_texts(), "scene", "MOVE SC10-M01", "- via: none", "- via: TABLE")
    assert not helpers.lines_of(helpers.checked(texts, ["GEOM-05"], story=False), "GEOM-05")
    return "a misspelt mark warned; an object as via passes"


# ---------------------------------------------------------------- X15: the instruction wording

@group("X15: apply names the next repair file's number; step 16 says N is that number; card 05 names one tempo per "
       "place; the rights template says step 0 writes evidence early; reference/01 names apply's two merges")
def instruction_wording_after_cross_examination(scratch):
    project = gold_command_project(scratch, "x15 fix numbers")
    review = ("### REVIEW RV-SC10 Scene 10's review\n- scope: SC10\n"
              "- answer: Is it so? | answer: yes | evidence: shot 150\n")
    code, output = stage(["--project", project, "apply", write_inbox(project, "U-10-Q01.md", review)])
    assert code == 0 and 'A repair of it goes in "U-10-Q01 - fix 1.md"' in output, output[-500:]
    code, output = stage(["--project", project, "apply", write_inbox(project, "U-10-Q01 - fix 1.md", review)])
    assert code == 0 and 'Another repair of it goes in "U-10-Q01 - fix 2.md"' in output, output[-500:]
    texts = {name: (SKILL / name).read_text(encoding="utf-8") for name in (
        "steps/16 Resume and recovery.md", "cards/05 Characters.md", "templates/22 Rights and credits.md",
        "reference/01 Record format.md")}
    assert "N is the number apply names" in texts["steps/16 Resume and recovery.md"]
    assert "her quick hands go in `tempo`" not in texts["cards/05 Characters.md"] and \
        'the field `tempo` says "fast hands, slow body"' in texts["cards/05 Characters.md"]
    assert "<quick, written at step 0" not in texts["templates/22 Rights and credits.md"]
    assert "except a review's answers and a side choice's sides" in texts["reference/01 Record format.md"]
    return "fix 1, then fix 2 named by apply; the four texts agree with the code and the schema"


# ---------------------------------------------------------------- X16 (c): "says it" in the frame's rows

@group("X16: the book's 'In the frame' row gives 'says it' its words when the shot hears one speech, as the one-line "
       "list does")
def says_it_in_the_frame(scratch):
    from stage_tools.make_views import ProjectView, full_shot_rows
    view = ProjectView(gold_command_project(scratch, "x16 says it"))
    view.speech = lambda identifier: {"text": "The police are on their way."}
    rows = [row for label, row in full_shot_rows(view, view.record("SC10-SH190", "SHOT"), "SC10")
            if label == "In the frame"]
    saye = next(row for row in rows if row.startswith("Dr Saye"))
    assert 'says "The police are on their way." once, level' in saye and "says it" not in saye, saye
    return "Dr Saye's row says the line's words"


# ---------------------------------------------------------------- after the update run: audio description

@group("Update run: an audio description line that starts with a body part or a count puts a colon after the name; "
       "a line that starts with what the person does keeps the plain form")
def description_after_name(scratch):
    from stage_tools.make_exports import fitted_description
    assert fitted_description([("Iona", ["one finger goes into a bright bolt hole"])], 20) == \
        "Iona: one finger goes into a bright bolt hole."
    assert fitted_description([("Iona", ["hand, foot, hand, foot", "her lips move round the torch"])], 20) == \
        "Iona: hand, foot, hand, foot; her lips move round the torch."
    assert fitted_description([("Iona", ["stands square to the window"])], 20) == "Iona stands square to the window."
    assert fitted_description([("Iona", ["in the foreground"])], 20) == "Iona in the foreground."
    return "a colon after the name only where the line names a part of the person or a count"


def main():
    with tempfile.TemporaryDirectory(prefix="stage fix05 ") as temporary:
        scratch = Path(temporary)
        side_choice(scratch)
        world_text_on_nothing(scratch)
        review_answers_across_batches(scratch)
        scores_wait_for_their_unit(scratch)
        saved_choice_skips_footage(scratch)
        handout_scene_records(scratch)
        list_unit_in_brief(scratch)
        handout_trimming_order(scratch)
        prompt_lint(scratch)
        paired_singles_in_one_part(scratch)
        scene_wide_checks_wait(scratch)
        silent_third_none(scratch)
        text_none_reads_nothing(scratch)
        start_here_after_exports(scratch)
        advisory_and_accepted_warnings(scratch)
        mounted_camera(scratch)
        impact_of_a_scene(scratch)
        film_pass_check_unit(scratch)
        invented_in_list(scratch)
        step_7_floors_and_beat_states(scratch)
        rung_hold(scratch)
        questions_without_markers(scratch)
        as_before_the_fire(scratch)
        lamplight_and_lamps(scratch)
        side_items_every_word(scratch)
        unit_check_cited_coverage(scratch)
        mark_inside_object(scratch)
        text_template_quote(scratch)
        instructions(scratch)
        selftest_note_values(scratch)
        split_speech_via_and_spoken_plant(scratch)
        apply_report_and_beat_uses(scratch)
        book_reader_words(scratch)
        book_says_it_once(scratch)
        in_short_names_what_waits(scratch)
        time_and_cost_words(scratch)
        choices_after_read(scratch)
        unit_check_messages(scratch)
        texts_in_scene(scratch)
        words_in_any_form(scratch)
        add_ons_and_headings(scratch)
        side_merge_only_for_sides(scratch)
        as_before_then_joining_word(scratch)
        words_added_later_keep_meaning(scratch)
        text_none_keeps_featured_text(scratch)
        camera_on_own_place_measured(scratch)
        straight_cut_across_parts(scratch)
        silent_third_none_with_three(scratch)
        heading_finds_only_place_of_its_kind(scratch)
        eyeline_point_words(scratch)
        speaking_shot_whole_only_when_cut(scratch)
        seal_ring_needs_side(scratch)
        film_pass_check_after_changes(scratch)
        passed_list_kept_on_purpose(scratch)
        move_marks_checked(scratch)
        instruction_wording_after_cross_examination(scratch)
        says_it_in_the_frame(scratch)
        description_after_name(scratch)
    failing = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({RESULTS.count(True)} passed, {failing} failing groups)")
    return 0 if not failing else 1


if __name__ == "__main__":
    sys.exit(main())
