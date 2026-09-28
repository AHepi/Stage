#!/usr/bin/env python3
"""WP4a acceptance test: the fields code derives (blueprint 5.6), the SIDE and GEOM checks (7.2) and the build
command, on the WP12a gold fixture (examples/01 The Catch - scene 10.md with its context file).

What it checks, in plain words:
- test T2's derived numbers (blueprint 14.3): shot 150's time floor of 13.8 seconds (speech 11.8 + pause 2.0),
  its 17-second clip as a held take, shot 080's size check (medium) and mirror route (plate), the sides of Iona's
  and Saye's raised hands and of Saye's ring, the opposite eyelines of Iona and Saye, and scene 10's era b with
  the elements K03 lists as mirrored and normal;
- the other derivations of 5.6 on the same scene: crew labels, provisional floors, speaking counts, eighths,
  story points resolved to beats, states in play, face heights, the facing Blender needs;
- that SIDE and GEOM are silent on the gold (with the staging patch while the gold still needs it; see
  tests/fixtures/sides and geometry/staging patch.json) and that each check fires on its faulty fixture
  (tests/fixtures/sides and geometry/faults.json);
- that stage.py build works on a project made from the gold: it writes derived fields.json and stores the
  story points' beats.

Usage: python tests/wp4a_derive_acceptance.py [--story <the story or an excerpt>]
Without --story it reads tests/fixtures/The Catch - lines 397-489.txt; when no story is present the groups that
need one report "skipped: story not present". Standard library only.
"""

import argparse
import json
import re
import shutil
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
SIDES_FIXTURES = REPOSITORY / "tests" / "fixtures" / "sides and geometry"
sys.path.insert(0, str(TOOLS))

from stage_tools import check_records  # noqa: E402
from stage_tools import derive_fields as derive  # noqa: E402
from stage_tools.record_format import load_skill_data, parse_file  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
RESULTS = []


def report(level, name, detail=""):
    RESULTS.append(level)
    print(f"{level:<5} {name}" + (f": {detail}" if detail else ""))


def group(name):
    """Run a test group: it returns a detail line, or raises AssertionError (FAIL) or Skip (INFO)."""
    def wrap(function):
        def run(*arguments):
            try:
                detail = function(*arguments)
            except Skip as skip:
                report("INFO", name, str(skip))
            except AssertionError as error:
                report("FAIL", name, str(error))
            except Exception as error:  # a crash is a failure, with its type
                report("FAIL", name, f"{type(error).__name__}: {error}")
            else:
                report("PASS", name, detail or "")
        return run
    return wrap


class Skip(Exception):
    pass


# ---------------------------------------------------------------- making the record files

def record_block(text, heading):
    """(start, end) of the record whose heading starts '### <heading>' (to the next '#' line, '---' or END)."""
    match = re.search(r"^### " + re.escape(heading) + r"(?=\s|$)", text, re.MULTILINE)
    if not match:
        raise AssertionError(f"record {heading} not found")
    end = re.search(r"^(#|---\s*$|END OF FILE)", text[match.end():], re.MULTILINE)
    return match.start(), match.end() + (end.start() if end else len(text) - match.end())


def replace_in_record(text, heading, find, replace):
    start, end = record_block(text, heading)
    block = text[start:end]
    if block.count(find) != 1:
        raise AssertionError(f'"{find}" is found {block.count(find)} times in {heading}, not once')
    return text[:start] + block.replace(find, replace) + text[end:]


def recount_end_line(text):
    count = len(re.findall(r"^### ", text, re.MULTILINE))
    return re.sub(r"\| \d+ records?(\s*)$", f"| {count} records\\1", text)


def gold_texts():
    return {"scene": (EXAMPLES / SCENE_FILE).read_text(encoding="utf-8"),
            "context": (EXAMPLES / CONTEXT_FILE).read_text(encoding="utf-8")}


def staging_patch_needed(texts):
    patch = json.loads((SIDES_FIXTURES / "staging patch.json").read_text(encoding="utf-8"))
    return all(edit["find"] in texts["scene"] for edit in patch["replace_in_record"]), patch


def with_staging_patch(texts):
    """The gold with the proposed staging fix (start at the back door, four moves in), while it needs one."""
    needed, patch = staging_patch_needed(texts)
    if not needed:
        return dict(texts), False
    scene = texts["scene"]
    for edit in patch["replace_in_record"]:
        scene = replace_in_record(scene, edit["record"], edit["find"], edit["replace"])
    start, _ = record_block(scene, patch["insert_before"])
    scene = scene[:start] + "\n".join(patch["records"]) + "\n" + scene[start:]
    return {"scene": recount_end_line(scene), "context": texts["context"]}, True


def write_pair(folder, texts):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / SCENE_FILE).write_text(texts["scene"], encoding="utf-8")
    (folder / CONTEXT_FILE).write_text(texts["context"], encoding="utf-8")
    return [folder / CONTEXT_FILE, folder / SCENE_FILE]


def parsed(paths):
    return [parse_file(path, path.name, SCHEMA) for path in paths]


def run_family_checks(paths, story, check_ids=None):
    check_records.load_check_families()
    wanted = check_ids or [check_id for check_id in check_records.REGISTRY
                           if check_id.split("-")[0] in ("SIDE", "GEOM")]
    source = check_records.StorySource.from_file(str(story), CONSTANTS) if story else None
    return check_records.run_checks(parsed(paths), SCHEMA, WORDS, CONSTANTS, story=source, check_ids=wanted)


# ---------------------------------------------------------------- the tests

def main():
    parser = argparse.ArgumentParser(description="WP4a acceptance: derived fields, SIDE and GEOM checks, build.")
    parser.add_argument("--story", help="the story file or an excerpt (default: the scene 10 fixture)")
    arguments = parser.parse_args()
    story = Path(arguments.story) if arguments.story else EXCERPT
    if not story.is_file():
        story = None
    if not (EXAMPLES / SCENE_FILE).is_file() or not (EXAMPLES / CONTEXT_FILE).is_file():
        report("INFO", "the WP12a gold", "skipped: the gold example is not present")
        return finish()
    breakdown = derive.Breakdown.from_paths([EXAMPLES / CONTEXT_FILE, EXAMPLES / SCENE_FILE],
                                            story_path=str(story) if story else None)
    whole_story = bool(story and breakdown.story and breakdown.story.first == 1)

    def shot(identifier):
        record = breakdown.record(identifier, "SHOT")
        assert record is not None, f"{identifier} is missing from the gold"
        return record

    def needs_story():
        if story is None:
            raise Skip("skipped: story not present")

    @group("T2: shot 150's time floor is 13.8 s = speech floor 11.8 s + pause owed 2.0 s after the turn at beat 7")
    def floor_of_150():
        needs_story()
        floor = derive.time_floor(breakdown, shot("SC10-SH150"))
        assert (floor.floor, floor.speech_floor, floor.text_floor, floor.pause_owed) == (13.8, 11.8, 0.0, 2.0), \
            f"got floor {floor.floor}, speech {floor.speech_floor}, text {floor.text_floor}, pause {floor.pause_owed}"
        line = floor.reasons()
        for piece in ("Saye 19 words at 2.0 = 9.5 s", "Iona 2 words at 2.5 = 0.8 s", "3 speeches x 0.5 s",
                      "2.0 s after the turn at beat 7"):
            assert piece in line, f'"{piece}" missing from the reasons: {line}'
        assert not floor.unknown_speeches, f"words unknown for {floor.unknown_speeches}"
        provisional = derive.provisional_floor(breakdown, "SC10", "SC10-SH150")
        assert provisional.floor == 13.8, f"the list item's provisional floor is {provisional.floor}, not 13.8"
        card = derive.time_floor(breakdown, shot("SC10-SH990"))
        assert (card.floor, card.text_floor, card.pause_owed) == (5.0, 3.0, 2.0), card.reasons()
        assert "2.0 s after the turn at beat 11" in card.reasons(), card.reasons()
        low = [f"{record.identifier} {derive.time_floor(breakdown, record).floor} > {record.get('screen_time')}"
               for record in breakdown.shots_of("SC10")
               if derive.time_floor(breakdown, record).floor > derive.number_of(record.get("screen_time"), 0) + 1e-9]
        assert not low, f"shots under their floor: {low}"
        return (f"{line}; the list item's provisional floor is also 13.8; the title card's floor is 5.0 (reading "
                f"3.0 s + the 2.0 s a turn is owed though beat 11 writes no pause); all 21 shots reach their floors")

    @group("T2: shot 150's clip is 17 s (15 s + 0.75 s handles each end, rounded up), a held take (turn), never split")
    def clip_of_150():
        plan = derive.clip_plan(breakdown, shot("SC10-SH150"))
        assert plan.clip_lengths == [17.0] and plan.held and plan.held_reason == "a turn shot" and not plan.split_at, \
            f"got {plan.as_dict()}"
        # Model facts are WP8's (adapters/video_models.json); these stand-ins have only the lengths clip_plan reads.
        stand_ins = {"kling-3.0-omni": {"length_s": {"min": 3, "max": 15, "step": 1}},
                     "seedance-2.5": {"length_s": {"min": 4, "max": 30, "step": 1}},
                     "wan-3.0": {"length_s": {"min": 2, "max": 30, "step": 1}}}
        original = breakdown.models
        breakdown.models = stand_ins
        try:
            on_kling = derive.clip_plan(breakdown, shot("SC10-SH150"), "kling-3.0-omni")
            assert not on_kling.fits and not on_kling.split_at and not on_kling.chained, \
                f"a held take on a 15-second model must not be split: {on_kling.as_dict()}"
            assert "seedance-2.5" in on_kling.models_allowing, f"models allowing 17 s: {on_kling.models_allowing}"
            on_seedance = derive.clip_plan(breakdown, shot("SC10-SH150"), "seedance-2.5")
            assert on_seedance.clip_lengths == [17.0] and on_seedance.fits, on_seedance.as_dict()
            fixture = fixture_shot(breakdown)
            split = derive.clip_plan(breakdown, fixture, "kling-3.0-omni")
            assert not split.held and split.fits and split.split_at == [8.0] and not split.chained, split.as_dict()
            assert all(length <= 15 for length in split.clip_lengths), split.as_dict()
        finally:
            breakdown.models = original
        real = "WP8's adapter file not present yet: model lengths from stand-ins"
        if original:
            real_plan = derive.clip_plan(breakdown, shot("SC10-SH150"), "kling-3.0-omni")
            real = f"with adapters/video_models.json on kling-3.0-omni: {real_plan.as_dict()}"
        return (f"17 s, held (a turn shot); on a 15-second model it is not split and goes whole to "
                f"{', '.join(on_kling.models_allowing)}; a normal 18 s shot with a cutaway at 8 s splits there into "
                f"{split.clip_lengths} s on the same model; {real}")

    @group("T2: shot 080's size check is medium (85 mm at about 6.3 m frames about 1.12 m) and its route is plate")
    def size_and_route_of_080():
        check = derive.size_check(breakdown, shot("SC10-SH080"))
        assert check is not None and check.size == "medium", f"size check {check}"
        assert abs(check.distance_m - 6.3) < 0.1 and abs(check.visible_height_m - 1.12) < 0.02, check.as_dict()
        route = derive.mirror_route(breakdown, shot("SC10-SH080"))
        assert route.route == "plate" and route.letter == "c", route.as_dict()
        assert "composite" in derive.post_operations(breakdown, shot("SC10-SH080")), "the plate needs a composite"
        return (f"{check.size}: {check.visible_height_m:.2f} m of height at {check.distance_m:.2f} m on Iona; "
                f"route plate: {'; '.join(route.reasons)}")

    @group("T2: sides in shot 080 (Iona's raised hand, Saye's raised hand, Saye's ring)")
    def sides_in_080():
        sides = {entry["element"]: entry for entry in derive.image_sides(breakdown, shot("SC10-SH080"))}
        iona, saye = sides["CH-IONA"], sides["CH-SAYE"]
        assert iona["mirror_state"] == "normal" and iona["hand_nearest_the_camera"] == "right", iona
        assert iona["hands"]["own_right"]["image"] == "nearest the camera", iona["hands"]
        assert saye["mirror_state"] == "mirrored", saye
        right = saye["hands"]["own_right"]
        assert right["appears_as"] == "left" and right["image"] == "nearest the camera", right
        ring = next(feature for feature in saye["features"] if feature["feature"] == "wedding ring")
        assert ring["own"] == "left" and ring["appears_as"] == "right" and ring["on_hand"] == "the far hand", ring
        assert right["prompt"] == "nearest the camera", right
        # Facing the camera, an own right side shows on frame-left (5.6): Iona in her close-up, shot 150.
        close = {entry["element"]: entry for entry in derive.image_sides(breakdown, shot("SC10-SH150"))}["CH-IONA"]
        palm = next(feature for feature in close["features"] if feature["feature"] == "skinned palm")
        assert close["facing"] == "camera" and palm["image"] == "frame_left", (close["facing"], palm)
        return ("Iona's raised hand is her own right, the hand nearest the camera; Saye's raised own right appears as "
                "her left, nearest the camera; Saye's ring (own left) appears on her right, the far hand; in shot 150 "
                "Iona faces the camera and her skinned palm (own right) shows on frame-left")

    @group("T2: Iona's and Saye's eyelines go to opposite sides of the frame")
    def eyelines():
        iona_sides, saye_sides = set(), set()
        for record in breakdown.shots_of("SC10"):
            if not derive.is_single(record):
                continue
            item = derive.focus_subject(breakdown, record)
            if item is None or not item.get("eyeline"):
                continue
            looker, looked_at = derive.element_of(item.first), derive.element_of(item.get("eyeline"))
            side = derive.eyeline_sides(breakdown, record).get(looker)
            if (looker, looked_at) == ("CH-IONA", "CH-SAYE"):
                iona_sides.add((record.identifier, side))
            elif (looker, looked_at) == ("CH-SAYE", "CH-IONA"):
                saye_sides.add((record.identifier, side))
        assert iona_sides and saye_sides, f"singles found: Iona {iona_sides}, Saye {saye_sides}"
        iona_set, saye_set = {side for _, side in iona_sides}, {side for _, side in saye_sides}
        assert len(iona_set) == 1 and len(saye_set) == 1 and iona_set != saye_set and None not in iona_set | saye_set, \
            f"Iona {sorted(iona_sides)}, Saye {sorted(saye_sides)}"
        two_shot = derive.eyeline_sides(breakdown, shot("SC10-SH080"))
        assert two_shot.get("CH-IONA") == iona_set.pop() and two_shot.get("CH-SAYE") == saye_set.pop(), two_shot
        # T6 (14.3): in shot 080 Iona is frame-left looking right, Saye frame-right looking left.
        assert (two_shot.get("CH-IONA"), two_shot.get("CH-SAYE")) == ("frame_right", "frame_left"), two_shot
        return (f"Iona's singles {sorted(iona_sides)} and Saye's {sorted(saye_sides)}; in the reflection two-shot "
                f"Iona looks {two_shot['CH-IONA']} and Saye {two_shot['CH-SAYE']}")

    @group("T2: scene 10 is era b, frame original; Saye, the kitchen and the mint mirrored; Iona, Jude and Eli normal")
    def era_of_scene_10():
        era = derive.scene_era(breakdown, "SC10")
        assert era is not None and era.era == "b" and era.frame == "original" and era.switch_at is None, era
        states = derive.scene_mirror_states(breakdown, "SC10")
        expected = {"CH-SAYE": "mirrored", "LOC-SAYE-KITCHEN": "mirrored", "PR-MINT": "mirrored",
                    "CH-IONA": "normal", "CH-JUDE": "normal", "CH-ELI": "normal"}
        wrong = {element: states.get(element) for element, state in expected.items() if states.get(element) != state}
        assert not wrong, f"wrong mirror states: {wrong}"
        in_150 = derive.shot_mirror_states(breakdown, shot("SC10-SH150"))
        assert in_150["CH-IONA"]["mirror_state"] == "normal" and in_150["LOC-SAYE-KITCHEN"]["mirror_state"] == "mirrored", \
            f"shot 150's mirror states: {in_150}"
        other_world = sorted(element for element, state in states.items() if state == "mirrored"
                             and element not in expected)
        assert derive.location_orientation(breakdown, "LOC-SAYE-KITCHEN") == "single", "the kitchen is seen both ways"
        # K03's other eras from the same WR-MIRROR lines: a to line 261, b from 263, c from 1565 with the frame
        # reversed, where the world (still reversed) shows normal and Jude and Eli (original) show mirrored.
        eras = {line: derive.era_at(breakdown, line) for line in (200, 263, 1563, 1565, 1600)}
        assert [eras[line].name for line in (200, 263, 1563, 1565)] == ["a", "b", "b", "c"], eras
        assert eras[1600].frame == "reversed" and eras[263].frame == "original", eras
        in_c = {element: derive.mirror_state_at(breakdown, element, 1600)
                for element in ("CH-JUDE", "CH-ELI", "LOC-SAYE-KITCHEN", "CH-SAYE")}
        assert in_c == {"CH-JUDE": "mirrored", "CH-ELI": "mirrored", "LOC-SAYE-KITCHEN": "normal",
                        "CH-SAYE": "normal"}, in_c
        from stage_tools.record_format import parse_text
        switching = parse_text("### SCENE SC27 The crossing\n- lines: 1555-1598\n", "scene 27.md", SCHEMA)
        with_27 = derive.Breakdown(breakdown.record_files + [switching], SCHEMA, WORDS, CONSTANTS)
        era_27 = derive.scene_era(with_27, "SC27")
        assert (era_27.era, era_27.frame, era_27.switch_at, era_27.next_era, era_27.next_frame) == \
            ("b", "original", 1565, "c", "reversed"), era_27
        return (f"era b, frame original; in era c (from line 1565, frame reversed) Jude and Eli show mirrored and the "
                f"world normal; a scene at lines 1555-1598 switches from b to c at 1565; in scene 10 mirrored: Saye, the "
                f"kitchen, the mint and {', '.join(other_world)}; normal: "
                f"Iona, Jude, Eli and {', '.join(sorted(e for e, s in states.items() if s == 'normal' and e not in expected))}")

    @group("5.6: labels, counts, eighths, provisional floors, states in play and the facing Blender needs")
    def labels_and_counts():
        labels = {identifier: derive.crew_label(identifier) for identifier in
                  ("SC10-SH010", "SC10-SH080", "SC10-SH090", "SC10-SH150", "SC10-SH155", "SC10-SH990")}
        assert labels == {"SC10-SH010": "10A", "SC10-SH080": "10H", "SC10-SH090": "10J", "SC10-SH150": "10Q",
                          "SC10-SH155": "10Q5", "SC10-SH990": "10 card 1"}, labels
        detail = [f"labels {labels['SC10-SH150']}, {labels['SC10-SH090']} (I and O skipped)"]
        if story is not None:
            speaking = derive.speaking_counts(breakdown, "SC10")
            counts = {person: entry["speeches"] for person, entry in speaking.items()}
            assert counts == {"CH-SAYE": 10, "CH-IONA": 4, "CH-JUDE": 1, "CH-ELI": 1}, counts
            eighths, how = derive.scene_eighths(breakdown, "SC10")
            assert eighths == 16, (eighths, how)
            detail.append(f"speeches Saye 10, Iona 4, Jude 1, Eli 1; eighths {eighths} ({how})")
        states = derive.states_in_play(breakdown, "SC10")
        for state in ("CH-IONA.S02", "CH-SAYE.S01", "CH-JUDE.S03", "CH-ELI.S03", "PR-MINT.S01"):
            assert state in states, f"{state} not in play: {states}"
        samples = derive.projected_placement(breakdown, shot("SC10-SH080"))
        iona, saye = samples["CH-IONA"][0], samples["CH-SAYE"][0]
        assert (iona.at, iona.faces, saye.at, saye.faces) == ("left_third", "frame_right", "right_third", "frame_left"), \
            (iona, saye)
        assert iona.facing_deg == 0.0 and saye.facing_deg == 180.0, (iona.facing_deg, saye.facing_deg)
        heights = derive.face_heights(breakdown, shot("SC10-SH150"))
        tight = CONSTANTS["constants"]["lip_sync_tight_face_height"]["value"]
        assert heights.get("CH-IONA", 0) >= tight, f"Iona's face height in shot 150: {heights}"
        detail.append("in shot 080 Iona is projected at the left third facing right (Blender facing 0) and Saye at "
                      f"the right third facing left (180); Iona's face is {heights['CH-IONA']:.2f} of the frame in "
                      "shot 150")
        if story is not None:
            assert derive.lip_sync(breakdown, shot("SC10-SH150")) == "tight", "shot 150's lip sync is not tight"
            detail.append("its lip sync is tight (the speakers come from the story's speeches)")
        return "; ".join(detail)

    @group("5.6 and step 7: every story point of scene 10 resolves to the beat the gold stores")
    def story_points():
        needs_story()
        points = derive.story_points(breakdown)
        in_scene = [point for point in points if point.scene == "SC10"]
        wrong = [f"{point.record}.{point.field} {point.quote}: {point.beat} (stored {point.stored_beat})"
                 for point in in_scene if point.beat is None or point.beat != point.stored_beat]
        assert len(in_scene) == 19 and not wrong, f"{len(in_scene)} points; wrong: {wrong}"
        outside = [point for point in points if point.scene != "SC10"]
        if not whole_story:
            assert all(point.problem == "skipped: not in the excerpt" for point in outside), \
                [point.as_dict() for point in outside if point.problem != "skipped: not in the excerpt"]
        return (f"19 story points on their stored beats; {len(outside)} in other scenes "
                + ("checked against the whole story" if whole_story else "skipped: not in the excerpt"))

    @group("A3 §5.2: eighths from the line-count model match A3's worked scenes (needs the whole story)")
    def eighths_whole_story():
        if not whole_story:
            raise Skip("skipped: needs the whole story (--story); the excerpt holds scene 10 only")
        found = {}
        for scene_identifier, expected in (("SC06", 18), ("SC08", 2), ("SC13", 29)):
            found[scene_identifier] = derive.scene_eighths(breakdown, scene_identifier)
            assert found[scene_identifier][0] == expected, (scene_identifier, found[scene_identifier])
        return "; ".join(f"{scene} {how}" for scene, (_, how) in found.items()) + " (A3: 2 2/8, 2/8, 3 5/8)"

    with tempfile.TemporaryDirectory(prefix="wp4a-") as temporary:
        temporary = Path(temporary)
        texts = gold_texts()
        base_texts, patched = with_staging_patch(texts)

        @group("SIDE and GEOM are silent on the gold (with the proposed staging patch while it needs one)")
        def silent_on_gold():
            gold_paths = write_pair(temporary / "gold", texts)
            result = run_family_checks(gold_paths, story)
            assert not result.crashed and not result.families_broken, (result.crashed, result.families_broken)
            lines = [str(problem) for problem in result.problems]
            if not patched:
                assert not lines, lines
                return f"no line on the gold; {len(result.checks_run)} checks ran"
            staging = [line for line in lines if re.match(r"W GEOM-0[46] SC10-SH010 ", line)]
            other = [line for line in lines if line not in staging]
            assert not other, other
            patched_result = run_family_checks(write_pair(temporary / "base", base_texts), story)
            assert not patched_result.problems, [str(problem) for problem in patched_result.problems]
            report("INFO", "the gold still places everyone at the table from the scene's start, but beat 1 is at "
                   "the back door, so shot 010 gives these warnings until WP12b adds the arrival (staging patch.json)",
                   " | ".join(staging))
            return (f"only the {len(staging)} shot 010 staging warnings on the gold; none with the staging patch; "
                    f"{len(result.checks_run)} checks ran")

        @group("each SIDE and GEOM check fires on its faulty fixture")
        def faults_fire():
            faults = json.loads((SIDES_FIXTURES / "faults.json").read_text(encoding="utf-8"))["faults"]
            fired, skipped = [], []
            for index, fault in enumerate(faults):
                if fault.get("needs_story") and story is None:
                    skipped.append(fault["check"])
                    continue
                changed = dict(base_texts)
                for edit in fault["edits"]:
                    changed[edit["file"]] = replace_in_record(changed[edit["file"]], edit["record"], edit["find"],
                                                              edit["replace"])
                paths = write_pair(temporary / f"fault {index:02d}", changed)
                result = run_family_checks(paths, story, [fault["check"]])
                assert not result.crashed, result.crashed
                hits = [problem for problem in result.problems
                        if getattr(problem, "check_id", "") == fault["check"] and problem.record == fault["record"]]
                assert hits, (f"{fault['check']} did not fire on {fault['record']} ({fault['about']}); got "
                              f"{[str(problem) for problem in result.problems]}")
                fired.append(f"{fault['check']} {fault['record']}")
            check_records.load_check_families()
            families = sorted(check_id for check_id, definition in check_records.REGISTRY.items()
                              if check_id.split("-")[0] in ("SIDE", "GEOM") and definition.build == 1)
            missing = sorted(set(families) - {entry.split()[0] for entry in fired} - set(skipped))
            assert not missing, f"build-1 checks with no faulty fixture: {missing}"
            return f"{len(fired)} faults, each caught: {', '.join(fired)}" + (
                f"; skipped (story not present): {', '.join(skipped)}" if skipped else "")

        @group("stage.py build on a project made from the gold: derived fields.json, story points stored")
        def build_command():
            project = make_project(temporary / "project", base_texts)
            command = [sys.executable, str(TOOLS / "stage.py"), "build", "--project", str(project)]
            if story:
                command += ["--story", str(story)]
            completed = subprocess.run(command, capture_output=True, text=True, timeout=300)
            assert completed.returncode == 0, completed.stdout + completed.stderr
            derived = json.loads((project / derive.MACHINE_FOLDER / derive.DERIVED_FILE).read_text(encoding="utf-8"))
            shot_150 = derived["shots"]["SC10-SH150"]
            assert shot_150["label"] == "10Q" and shot_150["clips"]["clip_lengths_s"] == [17.0], shot_150["clips"]
            assert derived["shots"]["SC10-SH080"]["size_check"] == "medium"
            assert derived["shots"]["SC10-SH080"]["mirror_route"] == "plate"
            assert derived["scenes"]["SC10"]["era"] == "b"
            detail = f"exit 0; {completed.stdout.strip().splitlines()[0]}"
            if story:
                assert shot_150["min_screen_time_s"] == 13.8, shot_150["min_screen_time_reasons"]
                scene_file = (project / "11 Scenes" / "Scene 10 - Saye's kitchen.md").read_text(encoding="utf-8")
                list_file = (project / "05 Story plan.md").read_text(encoding="utf-8")
                looks = (project / "10 Film rules.md").read_text(encoding="utf-8")
                assert "= SC10-B07" in looks and "= SC10-B02" in list_file, "story-point beats not stored"
                history = list((project / derive.MACHINE_FOLDER / "history").rglob("*.md"))
                assert history, "the old files were not kept in history"
                assert "SCENE SC10" in scene_file
                detail += f"; {len(history)} old files kept in history; story-point beats written back"
            return detail

        @group("step 8: a time slice's grey preview job is listed, and made as a planned stub once the checker accepts stubs")
        def previs_stubs():
            changed = dict(base_texts)
            changed["scene"] = replace_in_record(changed["scene"], "SHOT SC10-SH080", "- screen_time: 9",
                                                 "- screen_time: 9\n- time_slice: PV-SC10-MASTER-V01 | frames: 1-216")
            project = make_project(temporary / "stubs", changed)
            command = [sys.executable, str(TOOLS / "stage.py"), "build", "--project", str(project)]
            completed = subprocess.run(command, capture_output=True, text=True, timeout=300)
            assert completed.returncode == 0, completed.stdout + completed.stderr
            derived = json.loads((project / derive.MACHINE_FOLDER / derive.DERIVED_FILE).read_text(encoding="utf-8"))
            assert derived["previs_stubs_needed"] == [{"previs": "PV-SC10-MASTER-V01", "for": "SC10-MASTER",
                                                       "named_by": "SC10-SH080"}], derived["previs_stubs_needed"]
            stub_file = project / derive.PREVIS_FILE
            accepted = derive.checker_accepts_previs_stubs(SCHEMA, WORDS)
            assert stub_file.is_file() == accepted, f"stub file present: {stub_file.is_file()}, accepted: {accepted}"
            original = derive.checker_accepts_previs_stubs
            derive.checker_accepts_previs_stubs = lambda schema, words: True
            try:
                breakdown_here = derive.Breakdown.from_project(project, SCHEMA, WORDS, CONSTANTS)
                made = derive.create_previs_stubs(breakdown_here, project)
            finally:
                derive.checker_accepts_previs_stubs = original
            text = stub_file.read_text(encoding="utf-8")
            assert made == ["PV-SC10-MASTER-V01"] or accepted, made
            for line in ("### PREVIS PV-SC10-MASTER-V01", "- for: SC10-MASTER", "- level: 3", "- status: planned"):
                assert line in text, f'"{line}" missing from {derive.PREVIS_FILE}'
            again = derive.previs_stubs_needed(derive.Breakdown.from_project(project, SCHEMA, WORDS, CONSTANTS))
            assert again == [], again
            return ("listed in derived fields.json; " + ("made by build" if accepted else
                    "build leaves it unwritten while FORM-05 would ask the AI for its add-on fields (see WP4a's build "
                    "log); written correctly when allowed") + " as PREVIS PV-SC10-MASTER-V01, level 3, status planned")

        silent_on_gold()
        faults_fire()
        build_command()
        previs_stubs()

    floor_of_150()
    clip_of_150()
    size_and_route_of_080()
    sides_in_080()
    eyelines()
    era_of_scene_10()
    labels_and_counts()
    story_points()
    eighths_whole_story()
    return finish()


def fixture_shot(breakdown):
    """A normal (not held) 18-second shot with a planned cutaway at 8 seconds (T2's fixture shot)."""
    from stage_tools.record_format import parse_text
    text = ("### SHOT SC10-SH185 The fixture shot\n- role: normal\n- kind: live\n- held: no\n- screen_time: 18\n"
            "- moment: 0-8 | shows: Saye speaks\n- moment: 8-10 | shows: cutaway to Eli's hands\n"
            "- moment: 10-18 | shows: Saye goes on\n")
    return parse_text(text, "fixture shot.md", SCHEMA).records[0]


def make_project(folder, texts):
    """A project folder from the gold: the context's sections as the numbered files, the scene file in 11 Scenes,
    with every stored story-point beat taken off so that build must write it back."""
    folder.mkdir(parents=True)
    (folder / derive.MACHINE_FOLDER).mkdir()
    divider = "Below this line: details for the AI and the checker. You never need to read them."
    context = texts["context"].split(divider, 1)[1]
    sections = re.split(r"^## From (.+)$", context, flags=re.MULTILINE)[1:]
    for name, body in zip(sections[0::2], sections[1::2]):
        body = re.sub(r"\n+END OF FILE .*$", "", body.strip(), flags=re.DOTALL)
        body = re.sub(r'( "[^"]+") = SC\d{2,3}[A-Z]?-B\d{2,3}', r"\1", body)
        count = len(re.findall(r"^### ", body, re.MULTILINE))
        (folder / f"{name.strip()}.md").write_text(
            f"# {name.strip()}\n\n{divider}\n\n{body}\n\nEND OF FILE | {name.strip()} | {count} records\n", encoding="utf-8")
    scenes = folder / "11 Scenes"
    scenes.mkdir()
    (scenes / "Scene 10 - Saye's kitchen.md").write_text(texts["scene"], encoding="utf-8")
    return folder


def finish():
    failing = RESULTS.count("FAIL")
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({failing} failing groups)")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
