"""The acceptance test of the fixes after the second three-scene test (Project notes 37; the fixes are written up in
Project notes 38).

What it proves, one group per problem, on small fixtures only (copies of the WP12a gold and the scene 10 excerpt; no
group reads a whole story). It borrows its helpers from fix02_full_run_acceptance.py.
- 1 a split scene's part 1 is not asked for references to beats a later part writes (ID-02 waits), and the later
  part and the list unit are shown what the earlier parts wrote;
- 2 the handouts: card 16 reaches a scene tagged handedness before the mirror rule is written; a character's unit is
  never shown its own character as the example; a saved choice "never in scenes 26 and 27" is not offered there;
- 3 the book: the beats, one line each; numbers said in words; who acts in a one-line entry; recordings and screens
  said; turns named in story order; a move named by who moves; an addition said once; an eyeline direction reads
  as one;
- 4 a scene heading goes to the place its most specific part names, and a word most places share is no match;
- 5 the length check runs when only some scenes are chosen but the whole film's scenes are there; a small choice
  shown at the big-choices checkpoint is listed as small;
- 6 the instructions say what the second test had to guess, and the template, the field guide and the check give a
  non-human's description one length.

Usage: python tests/fix04_second_three_scene_test_acceptance.py
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
                                       gold_texts, group, read_manifest, stage, write_manifest)


def split_scene_project(scratch, name):
    """A gold project whose scene 10 was split in two parts, with only part 1 applied."""
    project = gold_command_project(scratch, name)
    manifest = read_manifest(project)
    manifest["scene_splits"] = {"SC10": True}
    manifest["units_done"] = [entry for entry in manifest.get("units_done", [])
                              if not str(entry.get("unit", "")).startswith(("U-07-SC10", "U-08-SC10"))]
    manifest["units_done"].append({"unit": "U-07-SC10-P1", "applied": "2026-10-05T10:00:00"})
    write_manifest(project, manifest)
    return project


def project_file(project, name):
    return next(path for path in Path(project).rglob("*.md") if path.name == name)


def replace_in_file(path, find, replace):
    text = path.read_text(encoding="utf-8")
    assert find in text, f"{path.name} does not hold {find!r}"
    path.write_text(text.replace(find, replace, 1), encoding="utf-8")


# ---------------------------------------------------------------- 1: a split scene

@group("1: a split scene's part 1 is not asked for part 2's beats (ID-02 waits); the later part and the list unit "
       "see what the earlier parts wrote")
def split_scene(scratch):
    from stage_tools.make_handout import Workspace, not_yet_due
    project = split_scene_project(scratch, "n1 split")
    problem = SimpleNamespace(check_id="ID-02", record="SC10", field_name="turn_beat")
    kept, later = not_yet_due(Workspace(project), 7, [problem])
    assert later == [problem] and not kept, (kept, later)
    elsewhere = SimpleNamespace(check_id="ID-02", record="SC09", field_name="turn_beat")
    kept, later = not_yet_due(Workspace(project), 7, [elsewhere])
    assert kept == [elsewhere], "a missing reference in a scene with no part waiting was hidden"
    for unit, wanted in (("U-07-SC10-P2", ("### SCENE SC10", "BEAT SC10-B")),
                         ("U-07-SC10-LIST", ("### SCENE SC10", "BEAT SC10-B", "MOVE SC10-M", "SETUP SC10-SU"))):
        code, output = stage(["--project", project, "handout", unit])
        assert code == 0, output[-400:]
        handout = (project / MACHINE / "handouts" / f"{unit}.md").read_text(encoding="utf-8")
        section = handout.split("### What the earlier parts of this scene wrote", 1)
        assert len(section) == 2, f"{unit}: no section of what the earlier parts wrote"
        missing = [text for text in wanted if text not in section[1]]
        assert not missing and "re-send it whole" in section[1], (unit, missing)
    manifest = read_manifest(project)
    manifest["units_done"].append({"unit": "U-07-SC10-P2", "applied": "2026-10-05T10:05:00"})
    write_manifest(project, manifest)
    kept, later = not_yet_due(Workspace(project), 7, [problem])
    assert kept == [problem], "ID-02 still waited after the last part was applied"
    return "ID-02 waits for part 2 only; part 2 and the list unit see the earlier parts"


# ---------------------------------------------------------------- 2: handouts

class FakeRecord:
    def __init__(self, identifier, fields):
        self.identifier = identifier
        self.fields = fields

    def get(self, name):
        return self.fields.get(name)


class FakeWorkspace:
    def __init__(self, records):
        self.by_type = records

    def records(self, type_name):
        return self.by_type.get(type_name, [])


@group("2: card 16 reaches a scene tagged handedness before the mirror rule exists; a character's unit is never "
       "shown its own character; a saved choice kept out of a scene is not offered there")
def handouts(scratch):
    from stage_tools.film_pass import read_places
    from stage_tools.make_handout import Workspace, example_section, mirror_rule_exists, reserve_lines
    tagged = FakeWorkspace({"SCENE": [FakeRecord("SC10", {"tags": "handedness, glass"})]})
    untagged = FakeWorkspace({"SCENE": [FakeRecord("SC10", {"tags": "none"})]})
    ruled = FakeWorkspace({"RULE": [FakeRecord("RL-01", {"kind": "mirror"})]})
    assert mirror_rule_exists(tagged) and mirror_rule_exists(ruled) and not mirror_rule_exists(untagged)
    project = gold_command_project(scratch, "n2 handouts")
    workspace = Workspace(project)
    unit = next(unit for unit in workspace.plan() if unit.step == 4 and "CH-IONA" in (unit.characters or []))
    example = example_section(workspace, unit) or ""
    assert "### CHARACTER" in example and "### CHARACTER CH-IONA" not in example, example[:300]
    places = read_places("scenes 10 and 29; never in scenes 26 and 27")
    assert places.scenes == {"SC10", "SC29"} and places.excluded == {"SC26", "SC27"}, places
    assert read_places("not in SC26").excluded == {"SC26"}
    rules = project_file(project, "10 Film rules.md")
    replace_in_file(rules, "- allowed_in: main turns only; the first in scene 13",
                    "- allowed_in: main turns only; the first in scene 13; never in scenes 10 and 27")
    allowed, lines = reserve_lines(Workspace(project), "SC10", [])
    assert "RC-02" not in [record.identifier for record in allowed], [record.identifier for record in allowed]
    shown = re.search(r"### CHARACTER (\S+)", example).group(1)
    return f"card 16 by tags; the example is {shown}; RC-02 kept out of SC10"


@group("2: a saved choice 'never in scene 10' refuses a use there, and its size is reserved there")
def kept_out_uses(scratch):
    from stage_tools.checks_craft_reasons_words import reserve_places, size_allowed_by_saved_choices, use_is_allowed
    texts = edit(gold_texts(), "context", "RESERVE RC-01",
                 "- allowed_in: SC10-SU01, the raised hands; and scene 29, the rings at the glass",
                 "- allowed_in: scenes 10 and 29, the raised hands and the rings")
    run = helpers.check_run(texts)
    shot = run.record("SC10-SH050") or next(record for record in run.records("SHOT"))
    assert use_is_allowed(run, run.record("RC-01"), shot) is not False
    _, scenes, _, _ = reserve_places(run, run.record("RC-01"))
    assert scenes == {"SC10", "SC29"}, scenes
    texts = edit(texts, "context", "RESERVE RC-01", "- allowed_in: scenes 10 and 29, the raised hands and the rings",
                 "- allowed_in: scene 29; never in scene 10")
    run = helpers.check_run(texts)
    assert use_is_allowed(run, run.record("RC-01"), shot) is False
    _, scenes, _, _ = reserve_places(run, run.record("RC-01"))
    assert scenes == {"SC29"}, scenes
    texts = edit(gold_texts(), "context", "RESERVE RC-02", "- allowed_in: main turns only; the first in scene 13",
                 "- allowed_in: main turns only; never in scene 10")
    assert size_allowed_by_saved_choices(helpers.check_run(gold_texts()), "SC10", "extreme_close_up") == \
        "extreme_close_up"
    wider = size_allowed_by_saved_choices(helpers.check_run(texts), "SC10", "extreme_close_up")
    assert wider != "extreme_close_up", wider
    return "a use in a kept-out scene is refused; 'scenes 10 and 29' names both"


# ---------------------------------------------------------------- 3: the book

@group("3: the book lists the beats, says numbers in words, says who acts, names turns in story order and moves "
       "by who moves, says an addition once, and says a recording, a screen and an eyeline direction plainly")
def book(scratch):
    from stage_tools.make_views import (ProjectView, additions_of_scene, full_shot_rows, scene_at_a_glance,
                                        scene_beat_lines, shot_line)
    project = gold_command_project(scratch, "n3 book")
    code, output = stage(["export", "book", "--project", project])
    assert code == 0, output[-400:]
    text = (project / "15 The breakdown" / "The breakdown.md").read_text(encoding="utf-8")
    assert "The beats, one line each" in text
    for wrong in (r"\bemphasis \d", r"grey preview level \d", r"floor-plan move \d", r"\bThe turn is beat"):
        assert not re.search(wrong, text), re.search(r".{40}" + wrong + r".{20}", text).group(0)
    view = ProjectView(project)
    assert "- beat 7: Not mint (the main turn)" in scene_beat_lines(view, "SC10")
    glance = " ".join(scene_at_a_glance(view, "SC10"))
    assert "The main turn is beat 7" in glance and "Another turn is beat 11" in glance, glance[-200:]
    assert view.names.name("SC10-M01", "SC10", short=True).startswith("Dr Saye's move")
    additions = additions_of_scene(view, "SC10")
    assert len(additions) == 4 and all(where is None for where, _ in additions), additions
    assert ", on Eli: the flask" in shot_line(view, "SC10-SH020", "SC10")
    scenes = project_file(project, "Scene 10 - Saye's kitchen.md")
    replace_in_file(scenes, "- kind: insert\n- why: Saye's eyes go down to it", "- kind: screen\n- why: Saye's eyes go "
                    "down to it")
    replace_in_file(scenes, "| eyeline: CH-SAYE | dwell_s: 3.5", "| eyeline: down into the dark | dwell_s: 3.5 | "
                    "recorded: SC06")
    replace_in_file(scenes, "- thing: PR-FLASK.S03 | emphasis: 1 |", "- thing: PR-FLASK.S03 | emphasis: 2 | "
                    "recorded: SC06 |")
    view = ProjectView(project)
    rows = dict(full_shot_rows(view, view.record("SC10-SH020", "SHOT"), "SC10"))
    assert "eyes down into the dark" in rows["In the frame"] and "eyes on down" not in rows["In the frame"]
    assert "as recorded in scene 6" in rows["In the frame"], rows["In the frame"]
    assert "as recorded in scene 6" in rows["Thing"] and "pointed out" in rows["Thing"], rows["Thing"]
    assert "on a screen" in shot_line(view, "SC10-SH020", "SC10")
    return "beats listed; turns in order; move by who moves; 4 additions; recording, screen and eyeline in words"


# ---------------------------------------------------------------- 4: place headings

@group("4: a heading goes to the place its most specific part names; a word most places share is no match")
def place_headings(scratch):
    from stage_tools.fill_code_fields import best_location_for, specific_part
    places = [SimpleNamespace(identifier=identifier, title=title) for identifier, title in (
        ("LOC-QUARANTINE-WARD", "The quarantine ward"), ("LOC-IONA-ROOM", "Iona's room"),
        ("LOC-ELI-ROOM", "Eli's room"), ("LOC-RECEIVING-ROOM", "The receiving room"),
        ("LOC-SAYE-KITCHEN", "Saye's kitchen"))]

    def chosen(heading):
        found = best_location_for(heading, places)
        return found.identifier if found else None
    assert specific_part("QUARANTINE - IONA'S ROOM - CONTINUOUS") == "IONA'S ROOM"
    assert chosen("QUARANTINE - IONA'S ROOM") == "LOC-IONA-ROOM"
    assert chosen("RECEIVING ROOM - CONTINUOUS") == "LOC-RECEIVING-ROOM"
    assert chosen("QUARANTINE WARD - CORRIDOR") == "LOC-QUARANTINE-WARD"
    assert chosen("STORE ROOM") is None, "a heading sharing only 'room' was given a place"
    return "Iona's room, the receiving room and the ward found; 'store room' left unplaced"


# ---------------------------------------------------------------- 5: the length check and the choices

@group("5: PLAN-04 is skipped for an excerpt but runs when only some scenes are chosen; a small choice shown at "
       "checkpoint B is listed as small")
def length_and_choices(scratch):
    texts = gold_texts()  # its scope is scene 10, its only scene: an excerpt
    skipped = [why for check, why in helpers.checked(texts, ["PLAN-04"], story=False).skipped if check == "PLAN-04"]
    assert skipped and "not in the excerpt" in skipped[0], skipped
    others = "\n\n".join(f"### SCENE SC{number} Another scene\n- lines: {number * 40}-{number * 40 + 30}\n"
                           f"- target_duration_s: 60" for number in (11, 12))
    texts = edit(texts, "scene", "SCENE SC10", add_after=others)
    result = helpers.checked(texts, ["PLAN-04"], story=False)
    skipped = [why for check, why in result.skipped if check == "PLAN-04"]
    assert not any("excerpt" in why for why in skipped), skipped
    choices = (SKILL.parent.parent.parent / "09 Example - The Catch, scene 10" / "01 Choices.md").read_text(
        encoding="utf-8")
    small = choices.split("## Small choices I made", 1)[1].split("\n## ", 1)[0]
    assert "Faces: invented faces for everyone (choice 11)" in small, small[:400]
    return "skipped for one scene of one, run for one scene of three; choice 11 listed as small"


# ---------------------------------------------------------------- 6: the instructions

@group("6: the instructions say what the second test had to guess; a non-human's description has one length "
       "everywhere")
def instructions(scratch):
    from stage_tools.checks_craft_reasons_words import description_range
    phrases = {"steps/06 Film rules.md": "matched `pause_after = hold`",
               "steps/07 Scene design and shot list.md": "the staging always changes on a turn, so it is one of them",
               "steps/04 Characters, places and things.md": "the same at both ends",
               "steps/01 Read the story.md": "that `read` did not place",
               "templates/07 Characters and voices.md": "25-40 words for a principal or non-human"}
    missing = [name for name, phrase in phrases.items() if phrase not in (SKILL / name).read_text(encoding="utf-8")]
    assert not missing, missing
    definition = SCHEMA.field("PROJECT", "scope") or {}
    assert "checkpoint A" in definition.get("meaning", "") and "checkpoint P" in definition.get("meaning", "")
    meaning = (SCHEMA.field("CHARACTER", "fixed_description") or {}).get("meaning", "")
    assert "principals and non-humans" in meaning, meaning
    run = helpers.check_run(gold_texts())

    def words_for(tier):
        return description_range(run, FakeRecord("CH-X", {"tier": tier}))[1]
    assert words_for("non_human") == words_for("principal") == [25, 40], words_for("non_human")
    assert words_for("extra") == words_for("minor") == [20, 30], words_for("extra")
    return f"{len(phrases)} instructions written; one length for a non-human"


def main():
    with tempfile.TemporaryDirectory(prefix="stage fix04 ") as temporary:
        scratch = Path(temporary)
        split_scene(scratch)
        handouts(scratch)
        kept_out_uses(scratch)
        book(scratch)
        place_headings(scratch)
        length_and_choices(scratch)
        instructions(scratch)
    failing = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({RESULTS.count(True)} passed, {failing} failing groups)")
    return 0 if not failing else 1


if __name__ == "__main__":
    sys.exit(main())
