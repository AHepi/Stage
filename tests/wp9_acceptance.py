#!/usr/bin/env python3
"""WP9 acceptance test: grey previews (previs, add-on B; blueprint 9, 14.2 WP9, 14.3 T6).

What it checks, in plain words:
- the kit's five plans in tools/previs/plans/ are fixed as section 9 says: the key "beats" is now "moments", and
  plan_chest_opens.json follows K21 (static at (0.25, -2.4, 1.7) on 35 mm, the aim tilting from (0, 0, 1.9) to
  (0, -0.1, 1.55), no push-in and no lens change); previs_from_plan.py and check_blocking.py are unchanged;
- the plan of scene 10, shot 080 compiled from the WP12a gold matches tests/fixtures/previs/SC10-SH080 expected.json
  on boxes, figures (place, height, facing_deg within 1 degree) and camera keys, and follows section 9's rules
  (252 frames for 9 seconds at 24 frames a second, 1280 x 536, depth range from the subjects plus and minus 0.5 m,
  stills at the first frame, each moment's start and the last frame, the plan view over the room and the camera),
  with the values the blueprint's tested plan gives (camera A, Iona, Saye, Eli);
- the same shot with WP4a's staging patch applied, and shot 190's keys for Iona's step aside;
- the free-fall helper, a master with a time slice, a turned (mirrored) plan, seated, kneeling and lying
  stand-ins, a posture change, extras fragments, and PREVIS-01 on plans that cannot be compiled;
- stage.py previs on a project made from the gold (plans written, stand-in colours given once);
- with Blender's Python module (bpy): stage.py previs --shot SC10-SH080 --render prints BLOCKING OK with every
  facing within 20 degrees, writes the contact sheet, and the grey still shows Iona frame-left, Saye frame-right
  and Eli small in the middle (read from the PNG); small plans prove PREVIS-02, PREVIS-03 and the excused contact
  of a seated stand-in; the fixed chest-opens plan renders with BLOCKING OK; a shot that is not framing-critical
  is marked approved: auto. With --full it also renders shot 190 whole and the other four kit plans (T6's list,
  as far as the gold reaches: scenes 6, 13 and 25 need the whole breakdown of the test phase).

Usage: python tests/wp9_acceptance.py [--no-render] [--full] [--save-stills <folder>] [--write-expected]
  --write-expected  regenerate tests/fixtures/previs/SC10-SH080 expected.json from the gold (after WP12b changes it)
Without bpy the render groups report "skipped: Blender's Python module is not present". Standard library only
(the renders run bpy in separate processes).
"""

import argparse
import hashlib
import json
import math
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
TOOLS = SKILL / "tools"
KIT = TOOLS / "previs"
EXAMPLES = SKILL / "references" / "examples"
SCENE_FILE = "01 The Catch - scene 10.md"
CONTEXT_FILE = "02 The Catch - scene 10 - context.md"
EXPECTED = REPOSITORY / "tests" / "fixtures" / "previs" / "SC10-SH080 expected.json"
SIDES_FIXTURES = REPOSITORY / "tests" / "fixtures" / "sides and geometry"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(REPOSITORY / "tests"))

from stage_tools import derive_fields as derive  # noqa: E402
from stage_tools import make_previs_plans as previs  # noqa: E402
from stage_tools.record_format import load_skill_data, parse_file  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
RESULTS = []
# The kit scripts as the C4 research kit ships them (blueprint 9: "reused unchanged").
KIT_SCRIPT_SHA256 = {
    "previs_from_plan.py": "8c9f2cbef8f6a31ee0cef49170a83c18532321d93fa61849b97f3cdb877dc4fc",
    "check_blocking.py": "0c1b28c88c72c5934e93e2cc5a2d88f2893cce89aeed3f36f9a7adf2e8027f17",
}
# The blueprint's tested plan for this shot (section 9, "Tested here"; 14.2's gold content).
TESTED_CAMERA = ([-3.5, 1.8, 1.45], [2.8, 1.8, 1.4], 85)
TESTED_FIGURES = {"IONA": ([2.8, 2.55], 0.0, 1.68), "SAYE": ([2.8, 1.05], 180.0, 1.65), "ELI": ([5.1, 2.0], 292.4, 1.78)}


def report(level, name, detail=""):
    RESULTS.append(level)
    print(f"{level:<5} {name}" + (f": {detail}" if detail else ""), flush=True)


class Skip(Exception):
    pass


def group(name):
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


# ---------------------------------------------------------------- the gold and its variants

def gold_texts():
    return {"scene": (EXAMPLES / SCENE_FILE).read_text(encoding="utf-8"),
            "context": (EXAMPLES / CONTEXT_FILE).read_text(encoding="utf-8")}


def breakdown_of(texts, folder):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / CONTEXT_FILE).write_text(texts["context"], encoding="utf-8")
    (folder / SCENE_FILE).write_text(texts["scene"], encoding="utf-8")
    return derive.Breakdown.from_paths([folder / CONTEXT_FILE, folder / SCENE_FILE])


def edit_record(text, heading, find, replace):
    """Replace one line inside one record (fails when the line is not found once)."""
    from wp4a_derive_acceptance import replace_in_record
    return replace_in_record(text, heading, find, replace)


def add_lines(text, heading, lines):
    """Add field lines at the end of a record's fields (before its status line)."""
    from wp4a_derive_acceptance import record_block
    start, end = record_block(text, heading)
    block = text[start:end]
    marker = block.rfind("\n- status:")
    block = block[:marker] + "\n" + "\n".join(lines) + block[marker:]
    return text[:start] + block + text[end:]


def add_record(text, record_text, before):
    from wp4a_derive_acceptance import record_block, recount_end_line
    start, _ = record_block(text, before)
    return recount_end_line(text[:start] + record_text.rstrip("\n") + "\n\n" + text[start:])


def close(first, second, tolerance=1e-3):
    return all(abs(a - b) <= tolerance for a, b in zip(first, second)) and len(first) == len(second)


def angle_apart(first, second):
    difference = abs((first - second) % 360)
    return min(difference, 360 - difference)


def compare_plans(got, wanted):
    """Problems between two plans on boxes, figures and camera keys (the WP9 acceptance comparison)."""
    problems = []
    boxes_got = {box["name"]: box for box in got.get("boxes", [])}
    boxes_wanted = {box["name"]: box for box in wanted.get("boxes", [])}
    if set(boxes_got) != set(boxes_wanted):
        problems.append(f"boxes differ: extra {sorted(set(boxes_got) - set(boxes_wanted))}, "
                        f"missing {sorted(set(boxes_wanted) - set(boxes_got))}")
    for name in set(boxes_got) & set(boxes_wanted):
        for key in ("loc", "size"):
            if not close(boxes_got[name][key], boxes_wanted[name][key]):
                problems.append(f"box {name} {key} {boxes_got[name][key]} != {boxes_wanted[name][key]}")
    figures_got = {figure["name"]: figure for figure in got.get("figures", [])}
    figures_wanted = {figure["name"]: figure for figure in wanted.get("figures", [])}
    if set(figures_got) != set(figures_wanted):
        problems.append(f"figures differ: {sorted(figures_got)} != {sorted(figures_wanted)}")
    for name in set(figures_got) & set(figures_wanted):
        got_figure, wanted_figure = figures_got[name], figures_wanted[name]
        if not close(got_figure["loc"], wanted_figure["loc"]):
            problems.append(f"figure {name} location {got_figure['loc']} != {wanted_figure['loc']}")
        if abs(got_figure["height"] - wanted_figure["height"]) > 1e-3:
            problems.append(f"figure {name} height {got_figure['height']} != {wanted_figure['height']}")
        if angle_apart(got_figure["facing_deg"], wanted_figure["facing_deg"]) > 1.0:
            problems.append(f"figure {name} facing {got_figure['facing_deg']} != {wanted_figure['facing_deg']}")
    keys_got, keys_wanted = got["camera"]["keys"], wanted["camera"]["keys"]
    if len(keys_got) != len(keys_wanted):
        problems.append(f"camera keys: {len(keys_got)} != {len(keys_wanted)}")
    for first, second in zip(keys_got, keys_wanted):
        if first[0] != second[0] or not close(first[1], second[1]) or not close(first[2], second[2]) \
                or first[3:] != second[3:]:
            problems.append(f"camera key {first} != {second}")
    if abs(got["camera"]["lens_mm"] - wanted["camera"]["lens_mm"]) > 1e-6:
        problems.append(f"lens {got['camera']['lens_mm']} != {wanted['camera']['lens_mm']}")
    return problems


def with_staging_patch(texts):
    from wp4a_derive_acceptance import with_staging_patch as patch
    return patch(texts)


def make_project(folder, texts):
    from wp4a_derive_acceptance import make_project as make
    return make(folder, texts)


def stage(*arguments, timeout=3600):
    command = [sys.executable, str(TOOLS / "stage.py")] + [str(argument) for argument in arguments]
    finished = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    return finished.returncode, finished.stdout + finished.stderr


# ---------------------------------------------------------------- reading a PNG (standard library)

def read_png(path):
    """(width, height, rows of (r, g, b) tuples) for an 8-bit RGB or RGBA PNG without interlacing."""
    data = Path(path).read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", f"{path} is not a PNG"
    position = 8
    width = height = colour_type = None
    compressed = b""
    while position < len(data):
        size, kind = struct.unpack(">I4s", data[position:position + 8])
        body = data[position + 8:position + 8 + size]
        if kind == b"IHDR":
            width, height, depth, colour_type, _, _, interlace = struct.unpack(">IIBBBBB", body)
            assert depth == 8 and colour_type in (2, 6) and interlace == 0, "only 8-bit RGB or RGBA PNGs are read"
        elif kind == b"IDAT":
            compressed += body
        position += 12 + size
    raw = zlib.decompress(compressed)
    channels = 4 if colour_type == 6 else 3
    stride = width * channels
    rows = []
    previous = bytearray(stride)
    offset = 0
    for _ in range(height):
        method = raw[offset]
        line = bytearray(raw[offset + 1:offset + 1 + stride])
        offset += 1 + stride
        for index in range(stride):
            left = line[index - channels] if index >= channels else 0
            up = previous[index]
            corner = previous[index - channels] if index >= channels else 0
            if method == 1:
                line[index] = (line[index] + left) & 255
            elif method == 2:
                line[index] = (line[index] + up) & 255
            elif method == 3:
                line[index] = (line[index] + ((left + up) >> 1)) & 255
            elif method == 4:
                guess = left + up - corner
                distances = (abs(guess - left), abs(guess - up), abs(guess - corner))
                pick = left if distances[0] <= distances[1] and distances[0] <= distances[2] else (
                    up if distances[1] <= distances[2] else corner)
                line[index] = (line[index] + pick) & 255
        rows.append([tuple(line[index:index + 3]) for index in range(0, stride, channels)])
        previous = line
    return width, height, rows


def linear(value):
    """An sRGB byte as linear light (the renders use the Standard view, so pixels are sRGB)."""
    value = value / 255
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def colour_mass(rows, wanted, tolerance, top_share=0.45):
    """(count, mean x, mean y, widest run in the top share of the frame) of the pixels whose linear colour points
    the way a stand-in's flat colour does (shading changes the brightness, not the direction). The widest run near
    the top is the head's width, since the bodies start lower."""
    count = 0
    total_x = total_y = 0
    widest = 0
    norm = math.sqrt(sum(value * value for value in wanted))
    table = [linear(value) for value in range(256)]
    limit = int(len(rows) * top_share)
    for y, row in enumerate(rows):
        run = best = 0
        for x, pixel in enumerate(row):
            light = [table[value] for value in pixel]
            size = math.sqrt(sum(value * value for value in light))
            hit = size >= 0.02 and sum(a * b for a, b in zip(light, wanted)) / (size * norm) >= tolerance
            if hit:
                count += 1
                total_x += x
                total_y += y
                run += 1
                best = max(best, run)
            else:
                run = 0
        if y < limit:
            widest = max(widest, best)
    if not count:
        return 0, None, None, 0
    return count, total_x / count, total_y / count, widest


# ---------------------------------------------------------------- the tests

def main():
    parser = argparse.ArgumentParser(description="WP9 acceptance: grey preview plans and renders.")
    parser.add_argument("--no-render", action="store_true", help="skip every group that renders in Blender")
    parser.add_argument("--full", action="store_true", help="also render shot 190 whole and the other kit plans")
    parser.add_argument("--save-stills", help="copy shot 080's rendered stills and contact sheet into this folder")
    parser.add_argument("--write-expected", action="store_true", help="regenerate the expected SC10-SH080 plan")
    arguments = parser.parse_args()
    if not (EXAMPLES / SCENE_FILE).is_file() or not (EXAMPLES / CONTEXT_FILE).is_file():
        report("INFO", "the WP12a gold", "skipped: the gold example is not present")
        return finish()
    work = Path(tempfile.mkdtemp(prefix="wp9 "))
    texts = gold_texts()
    gold = breakdown_of(texts, work / "gold")
    compiled = previs.compile_shot_plan(gold, "SC10-SH080")
    if arguments.write_expected:
        EXPECTED.parent.mkdir(parents=True, exist_ok=True)
        plan = dict(compiled.plan)
        plan["about"] = ("The expected grey preview plan of scene 10, shot 080, compiled from the WP12a gold by "
                         "section 9's rules (make_previs_plans.py). tests/wp9_acceptance.py compares boxes, figures "
                         "(place, height, facing_deg within 1 degree) and camera keys. Regenerate it with "
                         "python tests/wp9_acceptance.py --write-expected after the gold changes, and read the "
                         "difference before keeping it.")
        EXPECTED.write_text(json.dumps(plan, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        report("INFO", "expected plan written", str(EXPECTED.relative_to(REPOSITORY)))

    @group("the kit's plans are fixed (moments; chest opens per K21) and its two scripts are unchanged")
    def kit_plans():
        names = sorted(path.name for path in (KIT / "plans").glob("plan_*.json"))
        assert names == ["plan_cage_fall.json", "plan_chest_opens.json", "plan_grid_pov.json",
                         "plan_inversion_reveal.json", "plan_push_sill.json"], names
        for name in names:
            plan = json.loads((KIT / "plans" / name).read_text(encoding="utf-8"))
            assert "beats" not in plan and plan.get("moments"), f"{name} still has beats, or no moments"
        chest = json.loads((KIT / "plans" / "plan_chest_opens.json").read_text(encoding="utf-8"))
        keys = chest["camera"]["keys"]
        assert all(close(key[1], [0.25, -2.4, 1.7]) for key in keys), f"the camera moves: {keys}"
        assert chest["camera"]["lens_mm"] == 35 and all(len(key) == 3 for key in keys), "a lens change is keyed"
        assert close(keys[0][2], [0.0, 0.0, 1.9]) and close(keys[-1][2], [0.0, -0.1, 1.55]), "the tilt is wrong"
        assert chest["shot"].startswith("SC25"), f"the chest opens in scene 25, not {chest['shot']}"
        changed = []
        for script, wanted in KIT_SCRIPT_SHA256.items():
            digest = hashlib.sha256((KIT / script).read_bytes()).hexdigest()
            if digest != wanted:
                changed.append(script)
        assert not changed, f"changed from the C4 kit: {changed}"
        return (f"5 plans with moments; chest opens static at (0.25, -2.4, 1.7) on 35 mm, aim (0, 0, 1.9) to "
                f"(0, -0.1, 1.55) over frames {keys[1][0]}-{keys[2][0]}, no lens key; kit scripts unchanged")

    @group("shot 080 compiled from the WP12a gold matches the expected file (boxes, figures, camera keys)")
    def matches_expected():
        assert not compiled.problems, [str(problem) for problem in compiled.problems]
        assert EXPECTED.is_file(), f"{EXPECTED} is missing; run with --write-expected"
        wanted = json.loads(EXPECTED.read_text(encoding="utf-8"))
        problems = compare_plans(compiled.plan, wanted)
        assert not problems, "; ".join(problems[:8])
        return (f"{len(wanted['boxes'])} boxes, {len(wanted['figures'])} figures, "
                f"{len(wanted['camera']['keys'])} camera key; facings within 1 degree")

    @group("shot 080 follows section 9's rules and the blueprint's tested values")
    def follows_rules():
        plan = compiled.plan
        assert plan["fps"] == 24 and plan["frames"] == round((9 + 2 * 0.75) * 24) == 252, plan["frames"]
        assert plan["resolution"] == [1280, 536], plan["resolution"]
        assert plan["stills"] == [1, 19, 67, 127, 252], plan["stills"]
        assert [moment[0] for moment in plan["moments"]] == [19, 67, 127], plan["moments"]
        assert all(moment[2] == "l.421-434" for moment in plan["moments"]), plan["moments"]
        position, aim, lens = TESTED_CAMERA
        key = plan["camera"]["keys"][0]
        assert len(plan["camera"]["keys"]) == 1 and key[0] == 1 and close(key[1], position) and close(key[2], aim), key
        assert plan["camera"]["lens_mm"] == lens and plan["camera"]["sensor_mm"] == 36, plan["camera"]
        figures = {figure["name"]: figure for figure in plan["figures"]}
        for name, (point, facing, height) in TESTED_FIGURES.items():
            figure = figures[name]
            assert close(figure["loc"], point + [0.0]), f"{name} at {figure['loc']}"
            assert angle_apart(figure["facing_deg"], facing) <= 1.0, f"{name} faces {figure['facing_deg']}"
            assert abs(figure["height"] - height) < 1e-6, f"{name} is {figure['height']} tall"
        boxes = {box["name"]: box for box in plan["boxes"]}
        jude, table = boxes["JUDE"], boxes["TABLE"]
        assert close(jude["size"], [1.85, 0.45, 0.25]) and close(jude["loc"], [2.6, 1.8, 0.75 + 0.125]), jude
        assert {"set": "TABLE", "stand_ins": ["JUDE"]} in plan["clash_exclusions"], plan["clash_exclusions"]
        assert close(table["loc"], [2.8, 1.8, 0.375]) and close(table["size"], [1.8, 0.9, 0.75]), table
        assert "wall_west" not in boxes and {"wall_north", "wall_east", "wall_south", "floor"} <= set(boxes)
        assert "BACK_DOOR" not in boxes, "the back door in the wild west wall would stand in front of camera A"
        # depth range from the subjects, recomputed here: camera A looks along +x (nearly level)
        forward = [aim[index] - position[index] for index in range(3)]
        size = math.sqrt(sum(value * value for value in forward))
        forward = [value / size for value in forward]
        def depth(point):
            return sum((point[index] - position[index]) * forward[index] for index in range(3))
        depths = [depth([2.8, 2.55, 1.68 / 2]), depth([2.8, 1.05, 1.65 / 2]), depth([5.1, 2.0, 1.78 / 2])]
        depths += [depth([x, y, z]) for x in (2.6 - 0.925, 2.6 + 0.925) for y in (1.575, 2.025) for z in (0.75, 1.0)]
        near, far = min(depths) - 0.5, max(depths) + 0.5
        got = plan["depth_range_m"]
        assert abs(got[0] - near) < 0.011 and abs(got[1] - far) < 0.011, f"depth range {got}, wanted {near:.2f}-{far:.2f}"
        view = plan["plan_view"]
        half = view["size_m"] / 2
        assert view["direction"] == "top" and view["center"][0] - half <= -3.5 and view["center"][0] + half >= 6.0, view
        colours = {figure["name"]: tuple(figure["rgb"]) for figure in plan["figures"]}
        colours["JUDE"] = tuple(jude["rgb"])
        assert len(set(colours.values())) == 4, f"stand-in colours are not distinct: {colours}"
        assert colours["IONA"] == (0.2, 0.4, 0.8), f"Iona's lineup colour is blue: {colours['IONA']}"
        derived_facings = plan["derived_facings"]
        assert set(derived_facings) == {"IONA", "SAYE", "ELI"} and all(
            [frame for frame, _ in values] == plan["stills"] for values in derived_facings.values()), derived_facings
        return (f"252 frames, 1280 x 536, stills {plan['stills']}, depth {got}, camera A at {position} to {aim} on "
                f"85 mm, Iona 0, Saye 180, Eli {figures['ELI']['facing_deg']} degrees, Jude a 1.85 x 0.45 x 0.25 box "
                f"on the table; plan view centre {view['center'][:2]} size {view['size_m']} m")

    @group("with WP4a's staging patch: shot 080 is the same; shot 190 keys Iona's step aside at frames 199-235")
    def staging_patch():
        patched, applied = with_staging_patch(texts)
        breakdown = breakdown_of(patched, work / "patched")
        plan = previs.compile_shot_plan(breakdown, "SC10-SH080").plan
        problems = compare_plans(plan, compiled.plan)
        assert not problems, "; ".join(problems[:6])
        for source, label in ((gold, "gold"), (breakdown, "patched")):
            wide = previs.compile_shot_plan(source, "SC10-SH190").plan
            keys = {entry["object"]: entry["keys"] for entry in wide.get("animate", [])}
            assert set(keys) == {"IONA"}, f"{label}: animated {sorted(keys)}"
            frames = [key[0] for key in keys["IONA"]]
            assert frames == [1, 7, 199, 235, 252], f"{label}: Iona's keys at {frames}"
            assert close(keys["IONA"][1][1], [4.15, 1.4, 0.0]) and close(keys["IONA"][3][1], [3.9, 1.95, 0.0])
            toward_jude = (math.degrees(math.atan2(1.8 - 1.95, 2.6 - 3.9)) + 90) % 360
            assert angle_apart(keys["IONA"][3][2][2], toward_jude) < 0.1, keys["IONA"][3]
        return (f"staging patch {'applied' if applied else 'already in the gold'}; shot 190: Iona moves from her "
                f"place between them to her place aside over frames 199-235 (7.5 to 9 seconds after the 18-frame "
                f"handle), turning to Jude ({toward_jude:.1f}); the end of her move into the line shows in frames 1-7")

    @group("the free-fall helper keys every frame from z = z0 - 4.9 t squared (C4 R10)")
    def free_fall():
        keys = previs.free_fall_keys([0.0, 0.0, 9.2], [0.0, 0.0, 0.0], 9.2, 2.53, 1, 24, 4.9)
        assert [key[0] for key in keys] == list(range(1, len(keys) + 1)), "not one key per frame"
        for key in keys[:-1]:
            seconds = (key[0] - 1) / 24
            assert abs(key[1][2] - (9.2 - 4.9 * seconds * seconds)) < 1e-3, key
        assert keys[-1][1][2] == 2.53 and len(keys) == 1 + math.ceil(math.sqrt((9.2 - 2.53) / 4.9) * 24), len(keys)
        text = add_lines(texts["scene"], "SHOT SC10-SH080",
                         ["- motion: free_fall | object: PR-LAMP | from_z: 2.2 | to_z: 0.925 | start_frame: 19"])
        breakdown = breakdown_of({"scene": text, "context": texts["context"]}, work / "fall")
        plan = previs.compile_shot_plan(breakdown, "SC10-SH080").plan
        lamp = next(entry for entry in plan["animate"] if entry["object"] == "LAMP")["keys"]
        assert [key[0] for key in lamp] == list(range(19, 19 + len(lamp))), [key[0] for key in lamp]
        assert close(lamp[0][1], [3.6, 1.8, 2.2]) and lamp[-1][1][2] == 0.925, (lamp[0], lamp[-1])
        return f"a 9.2 to 2.53 m fall keys {len(keys)} frames; the lamp dropped in shot 080 keys frames 19-{lamp[-1][0]}"

    @group("a master and a time slice: the master's frames 30-100 become the slice's frames 1-71")
    def master_and_slice():
        scene = add_lines(texts["scene"], "SHOT SC10-SH110",
                          ["- time_slice: PV-SC10-MASTER-V01 | frames: 30-100",
                           "- motion: free_fall | object: PR-LAMP | from_z: 2.2 | to_z: 0.925 | start_frame: 40"])
        scene = edit_record(scene, "SHOT SC10-SH110", "- previs_level: 0", "- previs_level: 3")
        scene = add_record(scene, "### PREVIS PV-SC10-MASTER-V01\n- for: SC10-MASTER\n- level: 3\n- status: planned\n"
                                  "- locked: no\n", "SHOT SC10-SH010")
        breakdown = breakdown_of({"scene": scene, "context": texts["context"]}, work / "slice")
        masters, shots, _ = previs.select_targets(breakdown)
        assert masters == ["PV-SC10-MASTER-V01"] and "SC10-SH110" in shots, (masters, shots)
        results = {item.identifier: item for item in previs.compile_all(breakdown, masters, shots, None)}
        master, piece = results["SC10-MASTER"], results["SC10-SH110"]
        assert master.ok and piece.ok, [str(problem) for problem in master.problems + piece.problems]
        master_keys = next(entry for entry in master.plan["animate"] if entry["object"] == "LAMP")["keys"]
        slice_keys = next(entry for entry in piece.plan["animate"] if entry["object"] == "LAMP")["keys"]
        assert master.plan["frames"] == 100 and piece.plan["frames"] == 71, (master.plan["frames"], piece.plan["frames"])
        assert master_keys[0][0] == 40 and slice_keys[0][0] == 11, (master_keys[0], slice_keys[0])
        assert close(piece.plan["camera"]["keys"][0][1], [-3.5, 1.8, 1.45]), piece.plan["camera"]
        assert {figure["name"] for figure in piece.plan["figures"]} == {"IONA", "SAYE", "ELI"}
        assert piece.plan["stills"][0] == 1 and piece.plan["stills"][-1] == 71, piece.plan["stills"]
        return ("the master holds the scene's set and stand-ins with the lamp's fall from frame 40; shot 110's slice "
                "starts it at frame 11 of 71, seen through its own camera A")

    @group("a turned plan: the kitchen stored as original is turned for scene 10 (x -> W - x, heading -> 180 - heading)")
    def turned():
        context = edit_record(texts["context"], "LOCATION LOC-SAYE-KITCHEN", "- plan_orientation: reversed",
                              "- plan_orientation: original")
        breakdown = breakdown_of({"scene": texts["scene"], "context": context}, work / "turned")
        plan = previs.compile_shot_plan(breakdown, "SC10-SH080").plan
        assert plan["orientation"].startswith("reversed (turned"), plan["orientation"]
        boxes = {box["name"]: box for box in plan["boxes"]}
        original = {box["name"]: box for box in compiled.plan["boxes"]}
        for name in ("TABLE", "FRIDGE", "COUNTER", "JUDE"):
            assert close(boxes[name]["loc"], [6.0 - original[name]["loc"][0]] + original[name]["loc"][1:]), name
        assert "wall_west" in boxes and "wall_east" not in boxes, "the wild wall must turn with the plan"
        figures = {figure["name"]: figure for figure in plan["figures"]}
        eli_heading = (292.44 - 90) % 360
        turned_facing = ((180 - eli_heading) + 90) % 360
        assert angle_apart(figures["ELI"]["facing_deg"], turned_facing) < 0.1, figures["ELI"]
        assert close(figures["ELI"]["loc"], [0.9, 2.0, 0.0]), figures["ELI"]
        key = plan["camera"]["keys"][0]
        assert close(key[1], [9.5, 1.8, 1.45]) and close(key[2], [3.2, 1.8, 1.4]), key
        return (f"table at {boxes['TABLE']['loc'][:2]}, Eli at {figures['ELI']['loc'][:2]} facing "
                f"{figures['ELI']['facing_deg']}, camera A at {key[1]}, the east wall wild")

    @group("stand-ins that are not standing: seated on a seat, kneeling, lying; a posture change swaps stand-ins")
    def postures():
        context = add_lines(texts["context"], "LOCATION LOC-SAYE-KITCHEN", [
            "- object: STOOL | at: [5.1, 2.0] | size: [0.4, 0.4, 0.45] | base: 0 | material: wood | meaning: a stool "
            "| furniture: seat"])
        # The gold starts the three at the back door and brings them to their marks with moves at beat 2
        # (SC10-M08 Iona, SC10-M09 Eli), so the postures are set on those moves.
        scene = edit_record(texts["scene"], "MOVE SC10-M09", "- posture: standing", "- posture: seated")
        scene = edit_record(scene, "MOVE SC10-M08", "- posture: standing", "- posture: kneeling")
        scene = edit_record(scene, "MOVE SC10-M06", "- posture: standing", "- posture: lying")
        breakdown = breakdown_of({"scene": scene, "context": context}, work / "postures")
        plan = previs.compile_shot_plan(breakdown, "SC10-SH080").plan
        figures = {figure["name"]: figure for figure in plan["figures"]}
        assert abs(figures["ELI"]["height"] - 1.78 * 0.55) < 1e-3 and abs(figures["ELI"]["loc"][2] - 0.45) < 1e-6, \
            figures["ELI"]
        assert {"set": "STOOL", "stand_ins": ["ELI"]} in plan["clash_exclusions"], plan["clash_exclusions"]
        assert abs(figures["IONA"]["height"] - 1.68 * 0.7) < 1e-3 and figures["IONA"]["loc"][2] == 0.0
        wide = previs.compile_shot_plan(breakdown, "SC10-SH190").plan
        keys = {entry["object"]: entry["keys"] for entry in wide["animate"]}
        assert set(keys) == {"IONA", "IONA_STANDING", "IONA_LYING"}, sorted(keys)
        assert any(box["name"] == "IONA_LYING" for box in wide["boxes"]), "the lying stand-in is not a box"

        def arrives(name):
            return next(key[0] for key in keys[name] if key[1][2] > -1 and key[0] > 1)

        def placed_at(name, frame):
            return next(key for key in keys[name] if key[0] == frame)[1][2] > -1

        # move 5 (kneeling to standing) ends at frame 7; move 6 (standing to lying) at frame 235
        assert placed_at("IONA", 6) and not placed_at("IONA", 7), keys["IONA"]
        assert arrives("IONA_STANDING") == 7 and placed_at("IONA_STANDING", 234), keys["IONA_STANDING"]
        assert not placed_at("IONA_STANDING", 235) and arrives("IONA_LYING") == 235, keys["IONA_LYING"]
        return ("Eli seated on the stool (0.55 of his height, at the seat's top, excused from clashing with it); Iona "
                "kneeling (0.7); in shot 190 her kneeling stand-in gives way to a standing one at frame 7 (move 5 ends "
                "standing) and that to a lying box at frame 235 (move 6 ends lying)")

    @group("extras fragments are merged by name; PREVIS-01 names what cannot be compiled")
    def extras_and_errors():
        project = make_project(work / "extras project", texts)
        extras = project / "19 Grey previews" / "extras"
        extras.mkdir(parents=True)
        (extras / "SC10-SH080.json").write_text(json.dumps({
            "pivots": [{"name": "LAMP_HINGE", "loc": [3.2, 1.8, 0.75]}],
            "boxes": [{"name": "LAMP_SHADE", "loc": [0, 0, 0.3], "size": [0.2, 0.2, 0.1], "rgb": [1, 0.9, 0.6],
                       "parent": "LAMP_HINGE"}],
            "remove": ["LAMP"]}), encoding="utf-8")
        jobs = project / "19 Grey previews" / "Grey preview jobs.md"
        jobs.write_text("# Grey previews\n\nBelow this line: details for the AI and the checker. You never need to read "
                        "them.\n\n### PREVIS PV-SC10-SH080-V01\n- for: SC10-SH080\n- level: 2\n- standin_level: 1\n"
                        "- route: 1\n- extras: 19 Grey previews/extras/SC10-SH080.json\n- stills: 1, 100\n"
                        "- status: draft\n- locked: no\n\n### PREVIS PV-SC10-SH190-V01\n- for: SC10-SH190\n"
                        "- level: 2\n- standin_level: 1\n- route: 1\n- extras: 19 Grey previews/extras/missing.json\n"
                        "- stills: 1\n- status: draft\n- locked: no\n\nEND OF FILE | Grey preview jobs | 2 records\n",
                        encoding="utf-8")
        breakdown = derive.Breakdown.from_project(project)
        first = previs.compile_shot_plan(breakdown, "SC10-SH080", project_folder=project)
        assert first.ok, [str(problem) for problem in first.problems]
        names = {box["name"] for box in first.plan["boxes"]}
        assert "LAMP" not in names and "LAMP_SHADE" in names and first.plan["pivots"][0]["name"] == "LAMP_HINGE"
        assert 100 in first.plan["stills"], first.plan["stills"]
        second = previs.compile_shot_plan(breakdown, "SC10-SH190", project_folder=project)
        lines = [str(problem) for problem in second.problems]
        assert any(line.startswith("E PREVIS-01 SC10-SH190 extras") for line in lines), lines
        no_setup = edit_record(texts["scene"], "SHOT SC10-SH080", "- setup: SC10-SU01", "- setup: SC10-SU99")
        broken = previs.compile_shot_plan(breakdown_of({"scene": no_setup, "context": texts["context"]},
                                                       work / "no setup"), "SC10-SH080")
        broken_lines = [str(problem) for problem in broken.problems]
        assert any(line.startswith("E PREVIS-01 SC10-SH080 setup") for line in broken_lines), broken_lines
        ghost = {"boxes": [], "animate": [{"object": "GHOST", "keys": []}], "camera": {"keys": [[1, [0, 0, 1], [1, 0, 1]]]}}
        found = []
        previs.finish_plan(ghost, found, "SC10-SH080")
        assert [problem.check_id for problem in found] == ["PREVIS-01"] and "GHOST" in str(found[0]), found
        return f"fragment merged (lamp replaced by a hinged shade, still 100 added); {lines[0]} | {broken_lines[0]}"

    @group("stage.py previs on a project made from the gold: plans written, stand-in colours given once")
    def command():
        project = make_project(work / "project", texts)
        code, output = stage("previs", "--project", project)
        assert code == 0, output
        written = project / previs.PLANS_FOLDER / "SC10-SH080.json"
        assert written.is_file() and (project / previs.PLANS_FOLDER / "SC10-SH190.json").is_file(), output
        plan = json.loads(written.read_text(encoding="utf-8"))
        problems = compare_plans(plan, compiled.plan)
        assert not problems, problems
        start = (project / "00 Start here.md").read_text(encoding="utf-8")
        assert start.count("- previs_colours: ") == 4 and "- previs_colours: CH-IONA | rgb: [0.20, 0.40, 0.80]" in start
        code, again = stage("previs", "--project", project, "--shot", "SC10-SH080")
        assert code == 0 and "Gave stand-in colours" not in again, again
        assert (project / "00 Start here.md").read_text(encoding="utf-8") == start, "the colours changed on a second run"
        code, checked = stage("check", "--all", "--project", project)
        assert code == 0, checked[-600:]
        return "; ".join(line for line in output.splitlines() if line.startswith(("Compiled", "Gave")))

    kit_plans()
    matches_expected()
    follows_rules()
    staging_patch()
    free_fall()
    master_and_slice()
    turned()
    postures()
    extras_and_errors()
    command()
    render_groups(arguments, texts, work)
    shutil.rmtree(work, ignore_errors=True)
    return finish()


def render_groups(arguments, texts, work):
    """The groups that render in Blender (bpy); skipped plainly when it is absent or --no-render is given."""
    renderer = previs.load_renderer()
    runner = renderer.find_blender()

    def needs_blender():
        if arguments.no_render:
            raise Skip("skipped: --no-render")
        if runner is None:
            raise Skip("skipped: Blender's Python module is not present (pip install bpy)")

    @group("T6: stage.py previs --shot SC10-SH080 --render: BLOCKING OK, facings within 20 degrees, contact sheet")
    def render_080():
        needs_blender()
        project = make_project(work / "render project", texts)
        code, output = stage("previs", "--project", project, "--shot", "SC10-SH080", "--render")
        assert code == 0, output[-1500:]
        assert "Shot 80: BLOCKING OK, every facing within 20 degrees of the records" in output, output[-800:]
        folder = project / "19 Grey previews" / "Scene 10 - shot 080"
        stills = sorted(path.name for path in folder.glob("clay_f*.png"))
        assert stills == ["clay_f0001.png", "clay_f0019.png", "clay_f0067.png", "clay_f0127.png", "clay_f0252.png"]
        sheet = project / "19 Grey previews" / "Scene 10 - contact sheet.html"
        page = sheet.read_text(encoding="utf-8")
        assert "Shot 80 (needs your answer)" in page and "Scene%2010%20-%20shot%20080/clay_f0067.png" in page
        assert "Reply with the numbers of any that look wrong, or &#x27;fine&#x27;." in page
        from stage_tools import checks_craft_reasons_words as words_checks
        visible = re.sub(r"<style>.*?</style>|<[^>]+>", " ", page, flags=re.S)
        visible = re.sub(r"\b[A-Z][A-Z_]+\b", " ", visible)          # set-plan names the user's records hold
        retired = words_checks.retired_words_in_text(visible, WORDS)
        short = words_checks.abbreviations_in_text(visible, WORDS)
        assert not retired and not short, f"WORDS-02 {retired[:3]} WORDS-04 {short[:3]} on the contact sheet"
        report_file = json.loads((project / previs.PLANS_FOLDER / previs.REPORT_FILE).read_text(encoding="utf-8"))
        result = report_file["plans"]["SC10-SH080"]
        worst = max(check["apart"] for check in result["facing_checks"])
        # the grey still: Iona (blue) frame-left, Saye (green) frame-right, Eli (orange) small in the middle
        width, height, rows = read_png(folder / "clay_f0067.png")
        plan = json.loads((project / previs.PLANS_FOLDER / "SC10-SH080.json").read_text(encoding="utf-8"))
        colours = {figure["name"]: figure["rgb"] for figure in plan["figures"]}
        masses = {name: colour_mass(rows, rgb, 0.995) for name, rgb in colours.items()}
        iona, saye, eli = masses["IONA"], masses["SAYE"], masses["ELI"]
        assert iona[0] and saye[0] and eli[0], f"a stand-in is not in the still: {masses}"
        assert iona[1] < width * 0.4 and saye[1] > width * 0.6, f"Iona at x {iona[1]:.0f}, Saye at {saye[1]:.0f}"
        assert abs(eli[1] - width / 2) < width * 0.12 and eli[3] < 0.85 * min(iona[3], saye[3]), f"Eli {eli}"
        if arguments.save_stills:
            target = Path(arguments.save_stills)
            target.mkdir(parents=True, exist_ok=True)
            for path in list(folder.glob("clay_f*.png")) + [folder / "plan_view.png"]:
                shutil.copy2(path, target / f"SC10-SH080 {path.name}")
            shutil.copy2(sheet, target / "Scene 10 - contact sheet.html")
        return (f"BLOCKING OK, largest facing difference {worst} degrees, render {result['render_seconds']} s + check "
                f"{result['check_seconds']} s; in the still Iona is at x {iona[1]:.0f} of {width}, Saye at "
                f"{saye[1]:.0f}, Eli at {eli[1]:.0f}; heads {iona[3]}, {saye[3]} and {eli[3]} pixels wide (Eli deeper, "
                f"so smaller)")

    @group("PREVIS-02, PREVIS-03 and an excused seat, on small plans rendered in Blender")
    def small_plans():
        needs_blender()
        base = {"fps": 24, "frames": 3, "resolution": [320, 134], "stills": [1, 3], "facing_tolerance_deg": 20,
                "boxes": [{"name": "floor", "loc": [0, 0, -0.05], "size": [6, 6, 0.1], "rgb": [0.5, 0.5, 0.5]},
                          {"name": "TABLE", "loc": [0, 0, 0.375], "size": [1.2, 0.8, 0.75], "rgb": [0.5, 0.4, 0.2]},
                          {"name": "SEAT", "loc": [2, 0, 0.3], "size": [0.6, 0.6, 0.6], "rgb": [0.5, 0.4, 0.2]}],
                "camera": {"lens_mm": 35, "sensor_mm": 36, "keys": [[1, [0, -6, 1.6], [0, 0, 0.8]]]},
                "plan_view": {"direction": "top", "center": [0, 0, 0], "size_m": 8}}
        cases = {
            "clash": dict(base, shot="clash", figures=[{"name": "A", "loc": [0, 0, 0], "height": 1.7, "facing_deg": 0,
                                                         "rgb": [0.2, 0.4, 0.8]}]),
            "facing": dict(base, shot="facing", figures=[{"name": "A", "loc": [-2, 0, 0], "height": 1.7,
                                                          "facing_deg": 0, "rgb": [0.2, 0.4, 0.8]}],
                           derived_facings={"A": [[1, 90.0], [3, 90.0]]}),
            "seat": dict(base, shot="seat", figures=[{"name": "B", "loc": [2, 0, 0.2], "height": 0.9, "facing_deg": 0,
                                                      "rgb": [0.9, 0.55, 0.2]}],
                         clash_exclusions=[{"set": "SEAT", "stand_ins": ["B"]}]),
        }
        results = {}
        for name, plan in cases.items():
            path = work / "small" / f"{name}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(plan), encoding="utf-8")
            results[name] = renderer.render_plan(path, work / "small" / name, runner)
        clash, facing, seat = results["clash"], results["facing"], results["seat"]
        assert not clash["blocking_ok"] and any(check == "PREVIS-02" for check, _ in clash["problems"]), clash
        assert facing["blocking_ok"] and [check for check, _ in facing["problems"]] == ["PREVIS-03"] * 2, facing
        assert abs(facing["facing_checks"][0]["rendered"] - 0.0) < 0.1, facing["facing_checks"]
        assert seat["blocking_ok"] and seat["excused_lines"] and not seat["problems"], seat
        return (f"{clash['problems'][0][0]} {clash['problems'][0][1]}; PREVIS-03 at 90 degrees apart; excused: "
                f"{seat['excused_lines'][0]}")

    @group("T6: the fixed chest-opens plan renders with BLOCKING OK")
    def chest():
        needs_blender()
        result = renderer.render_plan(KIT / "plans" / "plan_chest_opens.json", work / "chest", runner)
        assert result["blocking_ok"] and not result["problems"], result
        return f"BLOCKING OK, {result['frames']} frames in {result['render_seconds']} + {result['check_seconds']} s"

    @group("approved: auto on a shot that is not framing-critical once it passes both checks")
    def approval():
        needs_blender()
        scene = edit_record(texts["scene"], "SHOT SC10-SH190", "- framing_critical: yes", "- framing_critical: no")
        scene = edit_record(scene, "SHOT SC10-SH190", "- screen_time: 9", "- screen_time: 1")
        scene = edit_record(scene, "SHOTLIST SC10-LIST", "| time: 9 | shows: held from the high corner",
                            "| time: 1 | shows: held from the high corner")
        project = make_project(work / "approval project", {"scene": scene, "context": texts["context"]})
        jobs = project / "19 Grey previews" / "Grey preview jobs.md"
        jobs.parent.mkdir(parents=True)
        jobs.write_text("# Grey previews\n\nBelow this line: details for the AI and the checker. You never need to read "
                        "them.\n\n### PREVIS PV-SC10-SH190-V01\n- for: SC10-SH190\n- level: 2\n- standin_level: 1\n"
                        "- route: 1\n- extras: none\n- stills: 1\n- status: draft\n- locked: no\n\n"
                        "END OF FILE | Grey preview jobs | 1 records\n", encoding="utf-8")
        code, output = stage("previs", "--project", project, "--shot", "SC10-SH190", "--render")
        assert code == 0, output[-1500:]
        text = jobs.read_text(encoding="utf-8")
        assert "- approved: auto" in text, text
        divider = "Below this line: details for the AI and the checker. You never need to read them."
        plain = (project / "00 Start here.md").read_text(encoding="utf-8").split(divider)[0]
        assert "approved on their own: shot 190, try 1." in plain and "PV-" not in plain, plain
        code, checked = stage("check", "--all", "--project", project)
        about_previews = [line for line in checked.splitlines() if line.startswith("E ")
                          and ("PV-" in line or "previs" in line or "PREVIS" in line)]
        assert not about_previews, about_previews
        return ("PV-SC10-SH190-V01 approved: auto (approved: no until both checks passed), a plain numbered log entry "
                "in 00 Start here; check --all has no error about the grey previews or the stand-in colours (its "
                "TIME errors come from this test's one-second shot)")

    @group("T6 (--full): shot 190 whole and the other four kit plans render with BLOCKING OK")
    def full():
        needs_blender()
        if not arguments.full:
            raise Skip("skipped: give --full to render shot 190 whole and the four other kit plans (about 10 minutes)")
        project = make_project(work / "full project", texts)
        code, output = stage("previs", "--project", project, "--shot", "SC10-SH190", "--render")
        assert code == 0 and "Shot 190: BLOCKING OK" in output, output[-1500:]
        lines = [line for line in output.splitlines() if "BLOCKING OK" in line]
        for name in ("plan_cage_fall.json", "plan_grid_pov.json", "plan_inversion_reveal.json", "plan_push_sill.json"):
            result = renderer.render_plan(KIT / "plans" / name, work / "kit" / name, runner)
            assert result["blocking_ok"] and not result["problems"], (name, result["problems"])
            lines.append(f"{name}: BLOCKING OK ({result['render_seconds']} s)")
        return "; ".join(lines)

    render_080()
    small_plans()
    chest()
    approval()
    full()


def finish():
    failing = RESULTS.count("FAIL")
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({failing} failing groups)")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
