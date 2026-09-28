"""make_previs_plans.py: compile the grey preview plans (previs, add-on B) from the records, and the command previs.

What this file does, in plain words (blueprint 9, K20, K23, K24; C4 section 5.2):
- for every shot at grey preview level previs_plan_level_min or more (SHOT previs_level), it writes one plan file in
  the C4 kit's format, "For machines - do not edit/previs plans/<shot>.json", built only from the records:
  - boxes: the floor and the walls from the place's set plan (LOCATION size; a wild wall is left out) and one box
    per set-plan object, centred from its at and base, in one flat colour per kind of material (C4 section 4.3);
  - figures: every character the scene starts (SCENE start), standing where the floor-plan moves (MOVE) of the
    beats before the shot's first beat left them, height_m tall, in the character's own stand-in colour (PROJECT
    previs_colours, given once by code), facing_deg = (heading + 90) mod 360 toward what they face. A seated
    stand-in is height x previs_seated_height_factor on its seat, a kneeling one x previs_kneeling_height_factor,
    a lying body a box (previs_lying_box) on its bed or the floor; seats and beds go into clash_exclusions;
  - animate: the floor-plan moves of the shot's own beats, keyed at start_s and start_s + dur_s (counted from the
    start of the first shot that shows the beat), with the posture changing at the end key;
  - camera: the shot's SETUP (at, look_at, lens_mm) on a previs_sensor_width_mm sensor; a push-in travels along
    the aim line to the next size step, a pan or tilt moves the aim point, handheld adds C4's small noise, and a
    mount on a moving thing parents the camera to it;
  - timing: frames = round((screen_time + 2 x handles_s) x fps); resolution previs_width_px wide, the height from
    PROJECT frame_shape (2.39 gives 1280 x 536); depth_range_m from the nearest and farthest subject, minus and
    plus previs_depth_margin_m; stills at the first frame, each moment's start and the last frame; moments with
    their story lines (for people; the kit ignores them); a plan view over the room and the camera;
  - a place stored in one mirror orientation is turned for a shot that needs the other (x -> W - x), never edited;
  - the free-fall helper turns SHOT motion items (free_fall | object | from_z | to_z | start_frame) into a key on
    every frame from z = z0 - free_fall_half_g x t squared (C4 R10);
  - what code cannot build (hinged rigs, riders keyed to a moving cage, arm poses, creatures) comes from the
    fragment PREVIS extras names ("19 Grey previews/extras/<shot>.json") and is merged by name;
  - a master (PV-SC06-MASTER-V01, for SC06-MASTER) is one plan of a physical event; each shot whose time_slice
    names it gets the master's set, stand-ins and keys, moved so the slice's first frame is frame 1, and its own
    camera. Shots joined by a CUT's shared_geometry take the master's set and stand-ins with their own timing.
- PREVIS-01 (E): a plan that cannot be compiled (no set plan, no setup, a missing extras fragment ...).
- the command previs [--shot] [--scene] [--render]: compiles the plans; with --render it renders them through
  tools/previs/render_previs.py (the kit's previs_from_plan.py and check_blocking.py, unchanged), reports
  PREVIS-02 (blocking not OK) and PREVIS-03 (a facing more than facing_tolerance_deg from the records), writes one
  contact sheet per scene and marks a passing shot that is not framing-critical approved: auto.

Numbers come from rules/constants.json by name. The few this file needs that constants.json does not hold yet
(stand-in palette, material colours, wall thickness, plan-view margin, handheld noise, parking depth) are named
in PREVIS_DEFAULTS below with their sources, and constants.json overrides them when it holds the same name.
Standard library only.
"""

import colorsys
import copy
import importlib.util
import json
import math
import random
import re
from dataclasses import dataclass, field as dataclass_field
from pathlib import Path

from .derive_fields import (MACHINE_FOLDER, SIZE_LADDER, Breakdown, along_path, blender_facing_deg, body_numbers,
                            camera_for, character_height, constant, element_of, frame_ratio, is_yes, length, number_of,
                            plan_for_shot, plan_heading_deg, point_of, scene_location, scene_of, scene_staging,
                            set_plan, shot_number, target_point, vector, via_share)
from .record_format import Problem, normalise_word, sort_key_for_identifier, split_list

PLANS_FOLDER = MACHINE_FOLDER + "/previs plans"
PREVIEWS_FOLDER = "19 Grey previews"
EXTRAS_FOLDER = PREVIEWS_FOLDER + "/extras"
REPORT_FILE = "render report.json"
MASTER_TARGET = re.compile(r"^(SC\d{2,3}[A-Z]?)-MASTER$")
PREVIS_ID = re.compile(r"^PV-(.+)-V(\d{2})$")
FRAMES_TEXT = re.compile(r"^\s*(\d+)\s*-\s*(\d+)\s*$")
SPAN_TEXT = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*$")
TOOLS_FOLDER = Path(__file__).resolve().parents[1]
KIT_FOLDER = TOOLS_FOLDER / "previs"

# Named values this module needs; rules/constants.json overrides any of them by the same name.
PREVIS_DEFAULTS = {
    # The stand-in colours, given once per character (PROJECT previs_colours). A character whose lineup colour word
    # names one of these gets it; the others take the next free one, in order. The first three are C4 section 12's
    # The Catch colours (Iona blue, Eli orange, Jude red), so the kit's plans and the compiled ones agree.
    "previs_stand_in_palette": [
        {"name": "blue", "rgb": [0.2, 0.4, 0.8]}, {"name": "orange", "rgb": [0.9, 0.55, 0.2]},
        {"name": "red", "rgb": [0.8, 0.2, 0.2]}, {"name": "green", "rgb": [0.25, 0.65, 0.3]},
        {"name": "purple", "rgb": [0.55, 0.35, 0.75]}, {"name": "yellow", "rgb": [0.9, 0.8, 0.2]},
        {"name": "teal", "rgb": [0.15, 0.6, 0.6]}, {"name": "pink", "rgb": [0.9, 0.45, 0.65]},
        {"name": "brown", "rgb": [0.5, 0.3, 0.15]}],
    # One flat colour per kind of material (C4 section 4.3: "brick brown, steel grey, sill white, band yellow"). The
    # first kind whose word appears in an object's material wins; walls and floor have their own.
    "previs_material_colours": [
        {"kind": "glass", "words": ["glass", "mirror", "window", "windows"], "rgb": [0.7, 0.85, 0.95]},
        {"kind": "living", "words": ["mint", "plant", "plants", "leaf", "leaves", "grass", "moss", "green"],
         "rgb": [0.2, 0.7, 0.3]},
        {"kind": "light", "words": ["lamp", "light", "bulb", "shade", "candle", "flame"], "rgb": [1.0, 0.85, 0.5]},
        {"kind": "dark", "words": ["black", "dark", "doorway", "opening", "hole", "shadow"], "rgb": [0.1, 0.1, 0.11]},
        {"kind": "metal", "words": ["steel", "metal", "iron", "chrome", "aluminium", "brass", "tin"],
         "rgb": [0.6, 0.62, 0.65]},
        {"kind": "wood", "words": ["wood", "wooden", "timber", "oak", "pine", "plywood"], "rgb": [0.55, 0.4, 0.25]},
        {"kind": "brick", "words": ["brick", "bricks", "terracotta", "clay"], "rgb": [0.6, 0.3, 0.2]},
        {"kind": "stone", "words": ["stone", "concrete", "tile", "tiles", "marble", "plaster"],
         "rgb": [0.5, 0.5, 0.5]},
        {"kind": "cloth", "words": ["cloth", "fabric", "leather", "blanket", "curtain", "cushion", "rug"],
         "rgb": [0.45, 0.3, 0.3]},
        {"kind": "white", "words": ["white", "pale", "paper"], "rgb": [0.95, 0.95, 0.95]},
        {"kind": "yellow", "words": ["yellow", "band", "stripe"], "rgb": [0.95, 0.8, 0.1]},
        {"kind": "painted", "words": ["painted", "paint"], "rgb": [0.8, 0.8, 0.76]},
        {"kind": "floor", "words": [], "rgb": [0.55, 0.55, 0.55]},
        {"kind": "wall", "words": [], "rgb": [0.8, 0.8, 0.76]},
        {"kind": "other", "words": [], "rgb": [0.65, 0.65, 0.65]}],
    # Walls and floor are this thick, outside the room (the kit's own sets use 0.1 to 0.2 metres).
    "previs_wall_thickness_m": 0.1,
    # A set-plan object this thin or thinner that touches a wild wall (a door or a window in it) is part of that
    # wall, so it is left out with the wall; otherwise it would stand in front of a camera looking through it.
    "previs_wall_object_depth_m": 0.2,
    # The plan view shows the room and every camera position, with this share of empty border.
    "previs_plan_view_margin": 0.1,
    # C4 section 4.2: handheld is a noise "under about 1 cm and 0.5 degrees"; keys every few frames.
    "previs_handheld_noise": {"position_m": 0.008, "angle_deg": 0.4, "every_frames": 6},
    # A stand-in for a posture a character is not in waits this far below the floor, out of every view.
    "previs_parking_depth_m": 20.0,
}
EPSILON = 1e-6


def setting(constants, name):
    """A named value: from rules/constants.json when it holds the name, else PREVIS_DEFAULTS."""
    return constant(constants, name, PREVIS_DEFAULTS.get(name))


def rounded(values, places=4):
    return [round(float(value) + 0.0, places) for value in values]


def stand_in_name(reference):
    """The plan name of a character's stand-in or a thing's box: CH-IONA -> IONA, PR-FLASK.S03 -> FLASK."""
    element = element_of(reference or "")
    return re.sub(r"^[A-Z]{2,4}-", "", element).replace("-", "_").upper()


def person_word(character):
    name = re.sub(r"^[A-Z]{2,4}-", "", element_of(character or ""))
    return " ".join(part.capitalize() for part in name.split("-"))


def shot_words(identifier):
    """A shot as the user reads it: SC10-SH080 -> 'shot 80'; SC06-MASTER -> 'the master of scene 6'."""
    master = MASTER_TARGET.match(identifier or "")
    if master:
        return f"the master of scene {scene_number_words(master.group(1))}"
    number = shot_number(identifier)
    return f"shot {number}" if number is not None else identifier


def scene_number_words(scene_identifier):
    match = re.match(r"^SC0*(\d+)([A-Z]?)$", scene_identifier or "")
    return (match.group(1) + match.group(2)) if match else scene_identifier


def scene_number_text(scene_identifier):
    """The scene's number as file names write it: SC10 -> 10, SC06A -> 06A."""
    match = re.match(r"^SC(\d{2,3}[A-Z]?)$", scene_identifier or "")
    return match.group(1) if match else scene_identifier


def render_folder_name(identifier):
    """'Scene 10 - shot 080' for a shot, 'Scene 06 - master' for a master (blueprint 2.6)."""
    master = MASTER_TARGET.match(identifier or "")
    if master:
        return f"Scene {scene_number_text(master.group(1))} - master"
    scene = scene_of(identifier)
    number = re.search(r"-SH(\d+)$", identifier or "")
    return f"Scene {scene_number_text(scene)} - shot {number.group(1) if number else identifier}"


def contact_sheet_name(scene_identifier):
    return f"Scene {scene_number_text(scene_identifier)} - contact sheet.html"


# ---------------------------------------------------------------- colours

def stored_colours(breakdown):
    """{CH id: [r, g, b]} from PROJECT previs_colours."""
    found = {}
    project = breakdown.project
    if project is None:
        return found
    for item in breakdown.items(project, "previs_colours"):
        point = point_of(item.get("rgb"))
        if item.first and point and len(point) == 3:
            found[item.first] = [round(value, 3) for value in point]
    return found


def lineup_colour_word(breakdown, character):
    record = breakdown.record(character, "CHARACTER")
    if record is None:
        return None
    item = breakdown.item(record, "lineup")
    word = item.get("colour") if item is not None else None
    return normalise_word(word) if word else None


def spare_colour(index):
    """A further distinct colour once the palette is used up (hues spread by the golden angle)."""
    hue = (0.61803398875 * (index + 1)) % 1.0
    return [round(value, 3) for value in colorsys.hsv_to_rgb(hue, 0.65, 0.85)]


def stand_in_colours(breakdown, constants=None):
    """({CH id: [r, g, b]} for every character, [the CH ids newly given a colour]). Colours already stored in
    PROJECT previs_colours never change; a new character whose lineup colour word names a free palette colour gets
    it; the rest take the next free palette colour in ID order (C4 Rec6: distinct stand-in colours)."""
    constants = constants if constants is not None else breakdown.constants
    palette = setting(constants, "previs_stand_in_palette") or []
    colours = dict(stored_colours(breakdown))
    taken = {tuple(value) for value in colours.values()}
    characters = [record.identifier for record in breakdown.records_of("CHARACTER") if record.identifier]
    new = [character for character in characters if character not in colours]
    by_name = {entry["name"]: entry["rgb"] for entry in palette}
    for character in list(new):
        word = lineup_colour_word(breakdown, character)
        rgb = by_name.get(word)
        if rgb is not None and tuple(rgb) not in taken:
            colours[character] = list(rgb)
            taken.add(tuple(rgb))
    spare_index = 0
    for character in new:
        if character in colours:
            continue
        free = next((entry["rgb"] for entry in palette if tuple(entry["rgb"]) not in taken), None)
        while free is None:
            candidate = spare_colour(spare_index)
            spare_index += 1
            if tuple(candidate) not in taken:
                free = candidate
        colours[character] = list(free)
        taken.add(tuple(free))
    return colours, new


def material_colour(material, constants, kind=None):
    """The flat colour of a set piece from its material words (C4 section 4.3)."""
    table = setting(constants, "previs_material_colours") or []
    if kind:
        for entry in table:
            if entry.get("kind") == kind:
                return list(entry["rgb"])
    text = (material or "").lower()
    for entry in table:
        for word in entry.get("words", []):
            if re.search(r"\b" + re.escape(word) + r"\b", text):
                return list(entry["rgb"])
    for entry in table:
        if entry.get("kind") == "other":
            return list(entry["rgb"])
    return [0.65, 0.65, 0.65]


# ---------------------------------------------------------------- the set

def wild_wall_sides(text):
    """The sides named wild in LOCATION wild_walls ('west wall' -> {'west'})."""
    words = set(re.findall(r"[a-z]+", (text or "").lower()))
    if "none" in words and len(words) <= 2:
        return set()
    return {side for side in ("north", "south", "east", "west") if side in words}


TURNED_WALL_NAMES = {"wall_east": "wall_west", "wall_west": "wall_east"}


def turn_box(box, plan):
    """A box written in the stored orientation, turned to the shot's (x -> W - x) when the plan is turned; the east
    and west walls change names with their sides."""
    if plan is not None and plan.turned:
        box = dict(box)
        box["loc"] = [round(plan.width - box["loc"][0], 4)] + box["loc"][1:]
        box["name"] = TURNED_WALL_NAMES.get(box["name"], box["name"])
    return box


def set_boxes(breakdown, plan, constants):
    """The floor, the walls (not the wild ones) and every set-plan object, as kit boxes in the shot's orientation."""
    thickness = setting(constants, "previs_wall_thickness_m")
    width, depth, height = plan.width, plan.depth, plan.height
    boxes = [{"name": "floor", "loc": rounded([width / 2, depth / 2, -thickness / 2]),
              "size": rounded([width, depth, thickness]), "rgb": material_colour("", constants, "floor")}]
    wall = material_colour("", constants, "wall")
    wild = wild_wall_sides(plan.wild_walls)
    walls = {
        "north": ([width / 2, depth + thickness / 2, height / 2], [width + 2 * thickness, thickness, height]),
        "south": ([width / 2, -thickness / 2, height / 2], [width + 2 * thickness, thickness, height]),
        "east": ([width + thickness / 2, depth / 2, height / 2], [thickness, depth, height]),
        "west": ([-thickness / 2, depth / 2, height / 2], [thickness, depth, height]),
    }
    for side in ("north", "east", "south", "west"):
        if side in wild:
            continue
        loc, size = walls[side]
        boxes.append({"name": f"wall_{side}", "loc": rounded(loc), "size": rounded(size), "rgb": list(wall)})
    location = breakdown.record(plan.location, "LOCATION")
    materials = {}
    if location is not None:
        for item in breakdown.items(location, "object"):
            materials[item.first] = item.get("material") or ""
    for name, found in plan.objects.items():
        size = found.get("size") or ()
        if len(size) < 3 or in_wild_wall(plan, found, wild, constants):
            continue
        x, y = found["at"][0], found["at"][1]
        base = found.get("base", 0.0) or 0.0
        boxes.append({"name": name, "loc": rounded([x, y, base + size[2] / 2]), "size": rounded(size[:3]),
                      "rgb": material_colour(materials.get(name, ""), constants)})
    return [turn_box(box, plan) for box in boxes]


def in_wild_wall(plan, found, wild, constants):
    """True for a thin object touching a wild wall (a door in it): it goes with the wall (stored orientation)."""
    if not wild:
        return False
    thin = setting(constants, "previs_wall_object_depth_m")
    size = found.get("size") or ()
    x, y = found["at"][0], found["at"][1]
    touch = setting(constants, "previs_wall_thickness_m") / 2
    sides = {"west": (x - size[0] / 2, size[0], 0.0), "east": (plan.width - (x + size[0] / 2), size[0], 0.0),
             "south": (y - size[1] / 2, size[1], 0.0), "north": (plan.depth - (y + size[1] / 2), size[1], 0.0)}
    for side in wild:
        gap, depth, _ = sides[side]
        if gap <= touch and depth <= thin:
            return True
    return False


def wild_wall_objects(plan, constants):
    """The names of set-plan objects left out with a wild wall."""
    wild = wild_wall_sides(plan.wild_walls)
    return [name for name, found in plan.objects.items()
            if len(found.get("size") or ()) >= 3 and in_wild_wall(plan, found, wild, constants)]


def resting_object(plan, stored_point, posture):
    """(name, top height) of the seat or bed a seated, lying or kneeling body rests on, else (None, 0.0)."""
    if posture == "standing" or stored_point is None:
        return None, 0.0
    wanted = {"seated": ("seat", "bed"), "lying": ("bed", "seat"), "kneeling": ("bed", "seat")}.get(posture, ())
    best = (None, 0.0)
    for kind in wanted:
        for name, found in plan.objects.items():
            size = found.get("size") or ()
            if len(size) < 3 or found.get("furniture") != kind:
                continue
            centre = found["at"]
            if (abs(stored_point[0] - centre[0]) <= size[0] / 2 + EPSILON
                    and abs(stored_point[1] - centre[1]) <= size[1] / 2 + EPSILON):
                top = (found.get("base", 0.0) or 0.0) + size[2]
                if best[0] is None or top > best[1]:
                    best = (name, top)
        if best[0] is not None:
            return best
    return best


# ---------------------------------------------------------------- time

@dataclass
class ShotTiming:
    """How a shot's seconds map onto plan frames: frame 1 is the start of the head handle (blueprint 9: frames =
    round((screen_time + 2 x handles_s) x fps)), so the plan lines up with the clip made from it (8.4)."""
    fps: int
    frames: int
    handle_s: float
    screen_time: float
    begin: float            # the scene-clock second the shot's screen time starts

    @property
    def handle_frames(self):
        return int(round(self.handle_s * self.fps))

    def frame_at(self, moment):
        """The plan frame of a scene-clock second."""
        return 1 + int(round((moment - self.begin + self.handle_s) * self.fps))

    def time_at(self, frame):
        return self.begin - self.handle_s + (frame - 1) / self.fps

    def frame_of_shot_second(self, seconds):
        """The plan frame of a second counted from the shot's screen-time start (a moment's start)."""
        return 1 + int(round((seconds + self.handle_s) * self.fps))

    @property
    def first_time(self):
        return self.time_at(1)

    @property
    def last_time(self):
        return self.time_at(self.frames)

    @property
    def screen_first_frame(self):
        return self.frame_of_shot_second(0.0)

    @property
    def screen_last_frame(self):
        return min(self.frames, self.frame_of_shot_second(self.screen_time))


def project_fps(breakdown):
    project = breakdown.project
    value = number_of(project.get("fps")) if project is not None else None
    return int(value) if value else 24


def shot_timing(breakdown, shot, staging, constants):
    fps = project_fps(breakdown)
    handle = constant(constants, "handles_s", 0.75)
    screen_time = number_of(shot.get("screen_time"), 0.0) or 0.0
    begin = staging.intervals.get(shot.identifier, (0.0, 0.0))[0]
    frames = int(round((screen_time + 2 * handle) * fps))
    return ShotTiming(fps, max(frames, 1), handle, screen_time, begin)


# ---------------------------------------------------------------- where the stand-ins are

@dataclass
class BodyState:
    point: tuple            # floor point in the shot's orientation
    stored_point: tuple     # the same in the stored plan
    heading: float          # facing direction on the plan (degrees from +x toward +y), or None
    posture: str
    resting: tuple          # (object name, top height)


class StagingForShot:
    """Where the scene's characters are during one shot: the scene's starts, every floor-plan move of the beats
    before the shot's first beat (their end), and the moves of the shot's own beats in time (blueprint 9)."""

    def __init__(self, breakdown, shot, plan, stored_plan, camera):
        self.breakdown = breakdown
        self.shot = shot
        self.plan = plan
        self.stored_plan = stored_plan
        self.camera = camera
        self.staging = scene_staging(breakdown, scene_of(shot.identifier))
        order = self.staging.beat_order
        beats = [beat for beat in breakdown.id_list(shot, "beats") if beat in order]
        self.shot_beats = set(beats)
        indexes = [order[beat] for beat in beats]
        self.first_index = min(indexes) if indexes else None
        self.last_index = max(indexes) if indexes else None

    def characters(self):
        return [character for character in self.staging.starts if self.staging.known(character)]

    def move_kind(self, move):
        """before (its end holds from frame 1), animated (keyed in time), or ignored (a later beat's move)."""
        index = self.staging.beat_order.get(move.beat)
        if index is None or self.first_index is None:
            return "animated"
        if move.beat in self.shot_beats:
            return "animated"
        if index < self.first_index:
            return "before"
        if index > self.last_index:
            return "ignored"
        return "animated"

    def animated_moves(self):
        return [move for move in self.staging.moves if move.path and self.move_kind(move) == "animated"]

    def raw_state(self, character, moment):
        """(stored floor point, faces reference, posture) of a character at a scene-clock second."""
        start = self.staging.starts[character]
        point, faces, posture = start["at"], start["faces"], start["posture"]
        for move in self.staging.moves:
            if move.who != character or not move.path:
                continue
            kind = self.move_kind(move)
            if kind == "ignored":
                continue
            if kind == "before" or move.end <= moment + EPSILON:
                point, faces, posture = move.path[-1], move.faces or faces, move.posture or posture
            elif move.start < moment - EPSILON:
                share = (moment - move.start) / (move.end - move.start) if move.end > move.start else 1.0
                point = along_path(move.path, share)
                faces = move.faces or faces
        return point, faces, posture

    def target_heading(self, point_here, faces, moment):
        """The heading from a point (shot orientation) toward what the character faces, or None."""
        word = normalise_word(faces or "")
        if word in ("camera", "away") and self.camera is not None:
            direction = vector(point_here, self.camera.position[:2])
            if word == "away":
                direction = (-direction[0], -direction[1])
        else:
            element = element_of(faces or "")
            if element in self.staging.starts and self.staging.known(element):
                target = self.raw_state(element, moment)[0]      # a person, where this shot's staging puts them
            else:
                target = target_point(self.breakdown, self.staging, self.stored_plan, faces, moment)
            if target is None:
                return None
            direction = vector(point_here, self.plan.place(target)[:2])
        if length(direction) < EPSILON:
            return None
        return plan_heading_deg(direction)

    def state(self, character, moment):
        stored_point, faces, posture = self.raw_state(character, moment)
        point = self.plan.place(stored_point)[:2]
        heading = self.target_heading(point, faces, moment)
        return BodyState(point, stored_point, heading, posture, resting_object(self.stored_plan, stored_point, posture))


def key_times(staging_for_shot, timing):
    """The scene-clock seconds to sample: the plan's first and last frame and every animated move's start, via
    point and end inside them."""
    first, last = timing.first_time, timing.last_time
    times = {first, last}
    for move in staging_for_shot.animated_moves():
        points = [move.start, move.end]
        if len(move.path) == 3 and move.end > move.start:
            points.append(move.start + (move.end - move.start) * via_share(move.path))
        for moment in points:
            if first < moment < last:
                times.add(moment)
    return sorted(times)


# ---------------------------------------------------------------- stand-ins

def unwrap(angles):
    """Angles made continuous, so a turn from 350 to 10 degrees keys as 350 to 370, never back through 180."""
    result = []
    for angle in angles:
        if not result:
            result.append(angle % 360)
            continue
        previous = result[-1]
        difference = ((angle - previous + 180) % 360) - 180
        result.append(previous + difference)
    return result


def drop_repeated_keys(keys):
    """Keys with the same place as both neighbours are left out; the ends of each still run are kept."""
    if len(keys) <= 2:
        return keys
    def same(first, second):
        return all(abs(a - b) < 1e-4 for a, b in zip(first[1] + first[2], second[1] + second[2]))
    kept = [keys[0]]
    for index in range(1, len(keys) - 1):
        if not (same(keys[index], keys[index - 1]) and same(keys[index], keys[index + 1])):
            kept.append(keys[index])
    kept.append(keys[-1])
    return kept


@dataclass
class StandIn:
    character: str
    name: str
    posture: str
    kind: str               # figure or box
    height: float
    entry: dict             # the figure or box entry of the plan
    keys: list = dataclass_field(default_factory=list)


class StandInBuilder:
    """Builds the figures, lying boxes and their keys for one shot from the StagingForShot."""

    def __init__(self, breakdown, constants, staging_for_shot, timing, colours):
        self.breakdown = breakdown
        self.constants = constants
        self.staging = staging_for_shot
        self.timing = timing
        self.colours = colours
        self.notes = []
        self.lying = constant(constants, "previs_lying_box", {}) or {}
        self.parking = setting(constants, "previs_parking_depth_m")

    def height_for(self, character, posture):
        height = character_height(self.breakdown, character)
        if posture == "seated":
            return height * constant(self.constants, "previs_seated_height_factor", 0.55)
        if posture == "kneeling":
            return height * constant(self.constants, "previs_kneeling_height_factor", 0.7)
        return height

    def lying_size(self, character):
        """A lying body's box: height_m long, previs_lying_box width and thickness (blueprint 9: 'a box of height_m x
        0.45 x 0.25 m'; the constant's width_factor is read as that width in metres)."""
        length_m = character_height(self.breakdown, character)
        width_m = self.lying.get("width_m", self.lying.get("width_factor", 0.45))
        thickness_m = self.lying.get("thickness_m", 0.25)
        return length_m, width_m, thickness_m

    def placement(self, character, posture, state):
        """(loc, rotation z) of a stand-in for a body state."""
        top = state.resting[1] if state.resting and state.resting[0] else 0.0
        if posture == "lying":
            _, _, thickness = self.lying_size(character)
            return [state.point[0], state.point[1], top + thickness / 2], (state.heading or 0.0)
        return [state.point[0], state.point[1], top], blender_facing_deg(state.heading or 0.0)

    def build(self, times):
        """[StandIn] for every character the scene starts, with keys when they move, turn or change posture."""
        stand_ins = []
        for character in self.staging.characters():
            samples = [(moment, self.staging.state(character, moment)) for moment in times]
            samples = self.with_switch_samples(character, samples)
            stand_ins.extend(self.stand_ins_for(character, samples))
        return stand_ins

    def with_switch_samples(self, character, samples):
        """Adds a sample one frame before each posture change, so the old stand-in stays until the change."""
        result = [samples[0]]
        for moment, state in samples[1:]:
            previous_moment, previous_state = result[-1]
            if state.posture != previous_state.posture:
                frame = self.timing.frame_at(moment)
                if frame - 1 > self.timing.frame_at(previous_moment):
                    before = self.timing.time_at(frame - 1)
                    result.append((before, self.staging.state(character, before)))
            result.append((moment, state))
        return result

    def stand_ins_for(self, character, samples):
        base = stand_in_name(character)
        colour = self.colours.get(character) or [0.8, 0.5, 0.3]
        postures = []
        for _, state in samples:
            if state.posture not in postures:
                postures.append(state.posture)
        headings = [state.heading for _, state in samples]
        known = next((heading for heading in headings if heading is not None), None)
        if known is None:
            self.notes.append(f"{person_word(character)} faces nothing the plan can place, so the stand-in faces "
                              "the default direction; give the start or the move a faces point")
        filled = []
        for heading in headings:
            known = heading if heading is not None else known
            filled.append(known if known is not None else 0.0)
        found = []
        for posture in postures:
            name = base if posture == postures[0] else f"{base}_{posture.upper()}"
            first_active = next(index for index, (_, state) in enumerate(samples) if state.posture == posture)
            active_state = samples[first_active][1]
            active_state.heading = filled[first_active]
            loc, rotation = self.placement(character, posture, active_state)
            keys = []
            rotations = []
            for index, (moment, state) in enumerate(samples):
                state_heading = filled[index]
                state.heading = state_heading
                if state.posture == posture:
                    place, turn = self.placement(character, posture, state)
                else:
                    place, turn = [loc[0], loc[1], -self.parking], rotation
                keys.append([self.timing.frame_at(moment), place, turn])
                rotations.append(turn)
            for key, turn in zip(keys, unwrap(rotations)):
                key[2] = [0.0, 0.0, round(turn, 2)]
                key[1] = rounded(key[1])
            keys = drop_repeated_keys(keys)
            moving = len(keys) > 1 and any(
                any(abs(a - b) > 1e-4 for a, b in zip(keys[0][1] + keys[0][2], other[1] + other[2]))
                for other in keys[1:])
            parked_at_start = samples[0][1].posture != posture
            if posture == "lying":
                stand_in = self.lying_box(character, name, colour, loc, rotation, moving or parked_at_start)
            else:
                height = self.height_for(character, posture)
                entry = {"name": name, "loc": rounded(keys[0][1] if parked_at_start else loc),
                         "height": round(height, 4), "facing_deg": round(rotation % 360, 2), "rgb": list(colour)}
                stand_in = StandIn(character, name, posture, "figure", height, entry)
            if moving or parked_at_start:
                stand_in.keys = keys
            found.append(stand_in)
        return found

    def lying_box(self, character, name, colour, loc, heading, keyed):
        length_m, width_m, thickness_m = self.lying_size(character)
        size = [length_m, width_m, thickness_m]
        turn = heading % 180
        entry = {"name": name, "loc": rounded(loc), "size": rounded(size), "rgb": list(colour)}
        stand_in = StandIn(character, name, "lying", "box", length_m, entry)
        if keyed:
            return stand_in
        if abs(turn - 90) < 0.5:
            entry["size"] = rounded([width_m, length_m, thickness_m])
        elif turn > 0.5 and abs(turn - 180) > 0.5:
            stand_in.keys = [[1, rounded(loc), [0.0, 0.0, round(heading, 2)]]]
        return stand_in


# ---------------------------------------------------------------- the camera

def size_ratio_for(constants, size):
    """The middle of a size's band on the size ladder (visible height / subject height)."""
    thresholds = constant(constants, "size_ladder_thresholds", {}) or {}
    band = thresholds.get(size)
    if isinstance(band, list) and len(band) == 2:
        return math.sqrt(band[0] * band[1])
    if isinstance(band, dict) and "at_least" in band:
        return band["at_least"] * 1.25
    if isinstance(band, dict) and "under" in band:
        return band["under"] * 0.75
    return None


def size_step(constants, ratio, steps):
    """The size one or more steps tighter (steps > 0) or wider (steps < 0) than a ratio's size."""
    thresholds = constant(constants, "size_ladder_thresholds", {}) or {}
    current = None
    for index, size in enumerate(SIZE_LADDER):
        band = thresholds.get(size)
        if isinstance(band, list) and band[0] <= ratio < band[1]:
            current = index
        elif isinstance(band, dict) and "at_least" in band and ratio >= band["at_least"]:
            current = index
        elif isinstance(band, dict) and "under" in band and ratio < band["under"]:
            current = index
    if current is None:
        return None
    wanted = max(0, min(len(SIZE_LADDER) - 1, current + steps))
    return SIZE_LADDER[wanted] if wanted != current else None


def focus_character(breakdown, shot, characters):
    focus = element_of(shot.get("focus_on") or "")
    if focus in characters:
        return focus
    for item in breakdown.items(shot, "subject"):
        element = element_of(item.first or "")
        if element in characters:
            return element
    return None


def eye_height(builder, character, state):
    if state.posture == "lying":
        top = state.resting[1] if state.resting and state.resting[0] else 0.0
        return top + builder.lying_size(character)[2]
    base = state.resting[1] if state.resting and state.resting[0] else 0.0
    return base + builder.height_for(character, state.posture) * body_numbers(builder.breakdown)["eye_height_share"]


def camera_keys(breakdown, shot, camera, staging_for_shot, builder, timing, constants, notes):
    """The kit camera's keys: [frame, position, aim point] (and lens where a zoom changes it)."""
    position = rounded(camera.position[:3])
    aim = rounded(camera.look_at[:3])
    keys = [[1, position, aim]]
    move = normalise_word(shot.get("move") or "static")
    if move in ("", "static", "none"):
        return keys
    characters = staging_for_shot.characters()
    subject = focus_character(breakdown, shot, characters)
    start_frame, end_frame = timing.screen_first_frame, timing.screen_last_frame
    start_time, end_time = timing.time_at(start_frame), timing.time_at(end_frame)
    if move in ("push_in", "pull_back", "zoom"):
        if subject is None:
            notes.append(f"the {move.replace('_', ' ')} has no person to size against; the camera holds still. "
                         "Name the subject in focus_on or write the move in the extras fragment")
            return keys
        state = staging_for_shot.state(subject, start_time)
        target = (state.point[0], state.point[1], eye_height(builder, subject, state))
        depth = sum((target[index] - camera.position[index]) * camera.forward[index] for index in range(3))
        body = builder.height_for(subject, state.posture) if state.posture != "lying" else builder.lying_size(subject)[0]
        if depth <= EPSILON or body <= EPSILON:
            notes.append(f"the {move.replace('_', ' ')} cannot be sized: the subject is not in front of the camera")
            return keys
        ratio = camera.visible_height_at(depth) / body
        wanted = size_step(constants, ratio, -1 if move == "pull_back" else 1)
        wanted_ratio = size_ratio_for(constants, wanted) if wanted else None
        if not wanted_ratio:
            notes.append(f"the {move.replace('_', ' ')} is already at the end of the size ladder; the camera holds still")
            return keys
        if move == "zoom":
            lens_end = camera.lens_mm * ratio / wanted_ratio
            keys = [[start_frame, position, aim, round(camera.lens_mm, 2)],
                    [end_frame, position, aim, round(lens_end, 2)]]
            return keys
        end_depth = wanted_ratio * body * camera.ratio * camera.lens_mm / camera.sensor_mm
        travel = depth - end_depth
        end_position = rounded([camera.position[index] + camera.forward[index] * travel for index in range(3)])
        end_aim = rounded([camera.look_at[index] + camera.forward[index] * travel for index in range(3)])
        return [[start_frame, position, aim], [end_frame, end_position, end_aim]]
    if move in ("pan", "tilt", "follow", "lead"):
        if subject is None:
            notes.append(f"the {move} has no person to follow; the camera holds still. Name the subject in focus_on "
                         "or write the move in the extras fragment")
            return keys
        result = []
        offset = None
        for moment in key_times(staging_for_shot, timing):
            state = staging_for_shot.state(subject, moment)
            eye = [state.point[0], state.point[1], eye_height(builder, subject, state)]
            frame = timing.frame_at(moment)
            if move in ("pan", "tilt"):
                new_aim = list(eye)
                if move == "pan":
                    new_aim[2] = aim[2]
                result.append([frame, position, rounded(new_aim)])
            else:
                if offset is None:
                    offset = [camera.position[index] - eye[index] for index in range(3)]
                result.append([frame, rounded([eye[index] + offset[index] for index in range(3)]), rounded(eye)])
        if len(result) < 2 or all(key[1] == result[0][1] and key[2] == result[0][2] for key in result):
            notes.append(f"the {move} has nothing to follow: {person_word(subject)} does not move in this shot; the "
                         "camera holds still. Write where it ends in the extras fragment")
            return keys
        return result
    if move == "handheld":
        noise = setting(constants, "previs_handheld_noise")
        seed = sum(ord(letter) for letter in shot.identifier)
        chance = random.Random(seed)
        distance = length(vector(camera.position, camera.look_at))
        aim_amount = distance * math.tan(math.radians(noise["angle_deg"]))
        result = []
        for frame in range(1, timing.frames + 1, max(1, int(noise["every_frames"]))):
            shake = [chance.uniform(-1, 1) * noise["position_m"] for _ in range(3)]
            sway = [chance.uniform(-1, 1) * aim_amount for _ in range(3)]
            result.append([frame, rounded([position[index] + shake[index] for index in range(3)]),
                           rounded([aim[index] + sway[index] for index in range(3)])])
        return result
    notes.append(f"the camera move {move.replace('_', ' ')} is not built by code; the plan holds the camera still. "
                 "Write the move in the extras fragment")
    return keys


# ---------------------------------------------------------------- the free-fall helper (C4 R10)

def free_fall_keys(loc, rotation, from_z, to_z, start_frame, fps, half_g):
    """A key on every frame from z = from_z - half_g x t squared until the object reaches to_z (C4 R10: eased keys
    float). loc and rotation are the object's own; only z changes."""
    keys = []
    frame = int(start_frame)
    while True:
        seconds = (frame - start_frame) / fps
        height = from_z - half_g * seconds * seconds
        if height <= to_z:
            keys.append([frame, rounded([loc[0], loc[1], to_z]), list(rotation)])
            break
        keys.append([frame, rounded([loc[0], loc[1], height]), list(rotation)])
        frame += 1
    return keys


def plan_object(plan, name):
    for key in ("pivots", "boxes", "figures"):
        for entry in plan.get(key, []):
            if entry.get("name") == name:
                return entry
    return None


def apply_motion(breakdown, shots, plan, fps, constants, problems, record_label):
    """Turns SHOT motion items into per-frame keys on the named objects of the plan."""
    half_g = constant(constants, "free_fall_half_g", 4.9)
    done = set()
    for shot in shots:
        for item in breakdown.items(shot, "motion"):
            if normalise_word(item.first or "") != "free_fall":
                continue
            name = stand_in_name(item.get("object") or "")
            key = (name, item.get("from_z"), item.get("to_z"), item.get("start_frame"))
            if key in done:
                continue
            done.add(key)
            from_z, to_z = number_of(item.get("from_z")), number_of(item.get("to_z"))
            start = int(number_of(item.get("start_frame"), 1) or 1)
            target = plan_object(plan, name)
            if target is None or from_z is None or to_z is None or from_z <= to_z:
                reason = (f"its object {item.get('object')} is not in the plan (a set-plan object, a stand-in, or a "
                          "box in the extras fragment)" if target is None else "from_z must be above to_z")
                problems.append(Problem("E", "PREVIS-01", record_label, "motion",
                                        f"the free fall cannot be keyed: {reason}",
                                        "Fix: correct the motion item or add the object to the extras fragment"))
                continue
            rotation = [0.0, 0.0, float(target.get("facing_deg", 0.0))] if "height" in target else [0.0, 0.0, 0.0]
            plan.setdefault("animate", [])
            plan["animate"] = [entry for entry in plan["animate"] if entry.get("object") != name]
            plan["animate"].append({"object": name, "keys": free_fall_keys(target["loc"], rotation, from_z, to_z,
                                                                           start, fps, half_g)})


# ---------------------------------------------------------------- extras fragments

LIST_KEYS = {"pivots": "name", "boxes": "name", "figures": "name", "animate": "object", "moments": None,
             "clash_exclusions": "set"}
KNOWN_KEYS = set(LIST_KEYS) | {"camera", "plan_view", "remove", "about", "note", "notes", "frames", "stills",
                               "depth_range_m", "fps", "resolution", "derived_facings"}


def merge_extras(plan, fragment):
    """Merges the AI's fragment into a compiled plan: items with the same name replace the compiled ones, new ones
    are added, names in remove are taken out, camera and plan_view keys are updated. Returns plain notes."""
    notes = []
    for name in fragment.get("remove", []) or []:
        for key in ("pivots", "boxes", "figures"):
            plan[key] = [entry for entry in plan.get(key, []) if entry.get("name") != name]
        plan["animate"] = [entry for entry in plan.get("animate", []) if entry.get("object") != name]
        plan.get("derived_facings", {}).pop(name, None)
    for key, value in fragment.items():
        if key in ("remove", "about", "note", "notes"):
            continue
        if key not in KNOWN_KEYS:
            notes.append(f'the extras fragment\'s key "{key}" is not a plan key the kit reads; it was copied as it is')
        if key in LIST_KEYS and isinstance(value, list):
            name_key = LIST_KEYS[key]
            existing = plan.setdefault(key, [])
            for item in value:
                if name_key and isinstance(item, dict) and item.get(name_key) is not None:
                    positions = [index for index, entry in enumerate(existing)
                                 if isinstance(entry, dict) and entry.get(name_key) == item[name_key]]
                    if positions:
                        existing[positions[0]] = item
                        if key == "figures":
                            plan.get("derived_facings", {}).pop(item[name_key], None)
                        continue
                existing.append(item)
        elif key in ("camera", "plan_view") and isinstance(value, dict):
            plan.setdefault(key, {}).update(value)
        else:
            plan[key] = value
    return notes


# ---------------------------------------------------------------- one shot

@dataclass
class CompiledPlan:
    identifier: str
    scene: str
    kind: str                           # shot, master or slice
    plan: dict = None
    problems: list = dataclass_field(default_factory=list)
    notes: list = dataclass_field(default_factory=list)
    framing_critical: bool = False
    previs_record: object = None
    master: str = None

    @property
    def ok(self):
        return self.plan is not None and not any(problem.level == "E" for problem in self.problems)


def previs_records_for(breakdown, target):
    """The PREVIS records whose for names a shot or master, oldest try first."""
    found = [record for record in breakdown.records_of("PREVIS") if (record.get("for") or "").strip() == target]
    return sorted(found, key=lambda record: sort_key_for_identifier(record.identifier))


def latest_previs(breakdown, target):
    found = [record for record in previs_records_for(breakdown, target)
             if normalise_word(record.get("status") or "") not in ("omitted",)]
    return found[-1] if found else None


def load_extras(project_folder, previs_record, problems, label):
    """The extras fragment a PREVIS record names, or None."""
    if previs_record is None:
        return None
    value = (previs_record.get("extras") or "").strip()
    if not value or normalise_word(value) == "none":
        return None
    if project_folder is None:
        problems.append(Problem("E", "PREVIS-01", label, "extras", f'the extras fragment "{value}" cannot be read '
                                "without the project folder"))
        return None
    path = Path(project_folder) / value
    if not path.is_file():
        problems.append(Problem("E", "PREVIS-01", label, "extras", f'names "{value}", which does not exist',
                                f"Fix: write the fragment at {value} or set extras: none on {previs_record.identifier}"))
        return None
    try:
        fragment = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        problems.append(Problem("E", "PREVIS-01", label, "extras", f'the fragment "{value}" is not valid JSON ({error})',
                                "Fix: correct the fragment"))
        return None
    if not isinstance(fragment, dict):
        problems.append(Problem("E", "PREVIS-01", label, "extras", f'the fragment "{value}" must be one JSON object'))
        return None
    return fragment


def moment_items(breakdown, shot):
    found = []
    for item in breakdown.items(shot, "moment"):
        match = SPAN_TEXT.match(item.first or "")
        if match:
            found.append((float(match.group(1)), float(match.group(2)), item.get("shows") or ""))
    return found


def lines_text(breakdown, shot):
    numbers = breakdown.lines_of(shot)
    if not numbers:
        value = shot.get("lines")
        return f"lines {value}" if value and normalise_word(value) != "none" else ""
    return f"l.{numbers[0]}" if numbers[0] == numbers[-1] else f"l.{numbers[0]}-{numbers[-1]}"


def shot_description(breakdown, shot):
    """The list item's one line (SHOTLIST item shows), else the shot's purpose."""
    for record in breakdown.of_scene("SHOTLIST", scene_of(shot.identifier)):
        for item in breakdown.items(record, "item"):
            if item.first == shot.identifier and item.get("shows"):
                return item.get("shows")
    return shot.get("purpose") or shot.title or ""


def subject_extent_points(builder, times_states):
    """Points whose depth bounds the shot's subjects: each figure's middle, each lying box's corners."""
    points = []
    for character, state in times_states:
        if state.posture == "lying":
            length_m, width_m, thickness_m = builder.lying_size(character)
            top = state.resting[1] if state.resting and state.resting[0] else 0.0
            heading = math.radians(state.heading or 0.0)
            along = (math.cos(heading) * length_m / 2, math.sin(heading) * length_m / 2)
            across = (-math.sin(heading) * width_m / 2, math.cos(heading) * width_m / 2)
            for first in (-1, 1):
                for second in (-1, 1):
                    for z in (top, top + thickness_m):
                        points.append((state.point[0] + first * along[0] + second * across[0],
                                       state.point[1] + first * along[1] + second * across[1], z))
        else:
            base = state.resting[1] if state.resting and state.resting[0] else 0.0
            points.append((state.point[0], state.point[1], base + builder.height_for(character, state.posture) / 2))
    return points


def depth_range(camera, points, margin):
    depths = [sum((point[index] - camera.position[index]) * camera.forward[index] for index in range(3))
              for point in points]
    depths = [depth for depth in depths if depth > EPSILON]
    if not depths:
        return None
    near = max(0.01, math.floor((min(depths) - margin) * 100) / 100)
    far = math.ceil((max(depths) + margin) * 100) / 100
    return [round(near, 2), round(far, 2)]


def plan_view(plan_record, camera_keys_list, ratio, constants, side=False):
    """The plan view: over the room and every camera position, in the frame's shape, with a small border."""
    margin = setting(constants, "previs_plan_view_margin")
    xs = [0.0, plan_record.width] + [key[1][0] for key in camera_keys_list]
    if side:
        zs = [0.0, plan_record.height] + [key[1][2] for key in camera_keys_list]
        width, height = max(xs) - min(xs), max(zs) - min(zs)
        size = max(width, height * ratio) * (1 + margin)
        return {"direction": "side", "center": rounded([(max(xs) + min(xs)) / 2, plan_record.depth / 2,
                                                        (max(zs) + min(zs)) / 2], 3),
                "size_m": round(size, 2), "hide": ["wall_south"]}
    ys = [0.0, plan_record.depth] + [key[1][1] for key in camera_keys_list]
    width, depth = max(xs) - min(xs), max(ys) - min(ys)
    size = max(width, depth * ratio) * (1 + margin)
    return {"direction": "top", "center": rounded([(max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, 0.0], 3),
            "size_m": round(size, 2)}


def is_shaft(plan_record):
    return plan_record.height > max(plan_record.width, plan_record.depth)


def overlap_notes(plan, stand_ins, lying_names):
    """Lying boxes that overlap a set object other than the bed they rest on: the kit's blocking check cannot see
    this (a lying body is a box of the set), so it is said plainly here."""
    notes = []
    boxes = {entry["name"]: entry for entry in plan.get("boxes", [])}
    for stand_in in stand_ins:
        if stand_in.kind != "box" or stand_in.keys:
            continue
        body = stand_in.entry
        resting = lying_names.get(stand_in.name)
        for name, entry in boxes.items():
            if name in (stand_in.name, resting, "floor") or name.startswith("wall_"):
                continue
            overlaps = []
            for axis in range(3):
                low = max(body["loc"][axis] - body["size"][axis] / 2, entry["loc"][axis] - entry["size"][axis] / 2)
                high = min(body["loc"][axis] + body["size"][axis] / 2, entry["loc"][axis] + entry["size"][axis] / 2)
                overlaps.append(high - low)
            if all(amount > 0.01 for amount in overlaps):
                notes.append(f"{person_word(stand_in.character)}'s lying stand-in overlaps the set-plan object {name} by "
                             f"{min(overlaps[:2]):.2f} metres; the blocking check cannot see it, because a lying body "
                             "is a box of the set. Move one of them in the records")
    return notes


def compile_shot_plan(breakdown, shot_identifier, colours=None, project_folder=None, constants=None, masters=None):
    """CompiledPlan for one shot: its plan dict in the kit's format, PREVIS-01 problems and plain notes."""
    constants = constants if constants is not None else breakdown.constants
    shot = breakdown.record(shot_identifier, "SHOT")
    scene = scene_of(shot_identifier)
    result = CompiledPlan(shot_identifier, scene, "shot")
    if shot is None:
        result.problems.append(Problem("E", "PREVIS-01", shot_identifier, None, "is not a shot in the records"))
        return result
    result.framing_critical = is_yes(shot.get("framing_critical"))
    slice_item = next(iter(breakdown.items(shot, "time_slice")), None)
    shared = shared_geometry_for(breakdown, shot_identifier)
    if slice_item is not None or shared:
        return compile_from_master(breakdown, shot, slice_item, shared, colours, project_folder, constants, masters)
    if colours is None:
        colours, _ = stand_in_colours(breakdown, constants)
    location = scene_location(breakdown, scene)
    stored = set_plan(breakdown, location) if location else None
    if stored is None:
        result.problems.append(Problem("E", "PREVIS-01", shot_identifier, None,
                                       f"cannot be compiled: its place ({location or 'none'}) has no set plan",
                                       "Fix: give the LOCATION a size, objects and marks (step 4's set plan)"))
        return result
    plan_record = plan_for_shot(breakdown, shot)
    camera = camera_for(breakdown, shot, plan_record)
    if camera is None:
        result.problems.append(Problem("E", "PREVIS-01", shot_identifier, "setup",
                                       "cannot be compiled: its setup has no complete camera (at, look_at, lens_mm)",
                                       "Fix: give the shot a setup with at, look_at and lens_mm"))
        return result
    staging = StagingForShot(breakdown, shot, plan_record, stored, camera)
    timing = shot_timing(breakdown, shot, staging.staging, constants)
    if timing.screen_time <= 0:
        result.problems.append(Problem("E", "PREVIS-01", shot_identifier, "screen_time",
                                       "cannot be compiled: the shot has no screen time"))
        return result
    missing = [person_word(character) for character in breakdown.id_list(breakdown.record(scene, "SCENE"), "characters")
               if character not in staging.staging.starts]
    if missing:
        result.notes.append("not placed, because the scene gives no start for them: " + ", ".join(missing))
    builder = StandInBuilder(breakdown, constants, staging, timing, colours)
    times = key_times(staging, timing)
    stand_ins = builder.build(times)
    result.notes.extend(builder.notes)
    previs_record = latest_previs(breakdown, shot_identifier)
    result.previs_record = previs_record
    plan = base_plan(breakdown, shot, plan_record, timing, constants)
    plan["boxes"] = set_boxes(breakdown, plan_record, constants)
    left_out = wild_wall_objects(plan_record, constants)
    if left_out:
        result.notes.append("left out with the wild wall they stand in: " + ", ".join(left_out))
    lying_names = {}
    for stand_in in stand_ins:
        if stand_in.kind == "box":
            plan["boxes"].append(stand_in.entry)
        else:
            plan["figures"].append(stand_in.entry)
        if stand_in.keys:
            plan["animate"].append({"object": stand_in.name, "keys": stand_in.keys})
    for stand_in in stand_ins:
        first_state = staging.state(stand_in.character, timing.first_time)
        if stand_in.posture == first_state.posture and first_state.resting[0] and stand_in.kind == "box":
            lying_names[stand_in.name] = first_state.resting[0]
    plan["clash_exclusions"] = clash_exclusions(stored, stand_ins, staging, times)
    notes = []
    keys = camera_keys(breakdown, shot, camera, staging, builder, timing, constants, notes)
    result.notes.extend(notes)
    plan["camera"] = camera_entry(breakdown, shot, camera, keys, stand_ins)
    subjects = subject_characters(breakdown, shot, staging.characters())
    samples = [(character, staging.state(character, moment)) for character in subjects for moment in times]
    points = subject_extent_points(builder, samples)
    if not points:
        points = [tuple(camera.look_at[:3])]
    margin = constant(constants, "previs_depth_margin_m", 0.5)
    plan["depth_range_m"] = depth_range(camera, points, margin) or [0.3, 15.0]
    moments = moment_items(breakdown, shot)
    story_lines = lines_text(breakdown, shot)
    plan["moments"] = [[timing.frame_of_shot_second(start), shows, story_lines] for start, _, shows in moments]
    stills = {1, timing.frames} | {min(timing.frames, max(1, frame)) for frame, _, _ in plan["moments"]}
    if previs_record is not None:
        for piece in split_list(previs_record.get("stills") or ""):
            frame = number_of(piece)
            if frame is not None and 1 <= frame <= timing.frames:
                stills.add(int(frame))
    plan["stills"] = sorted(stills)
    motion_used = any(normalise_word(item.first or "") == "free_fall" for item in breakdown.items(shot, "motion"))
    plan["plan_view"] = plan_view(plan_record, keys, camera.ratio, constants,
                                  side=motion_used or is_shaft(plan_record))
    plan["derived_facings"] = derived_facings(stand_ins, staging, timing, plan["stills"])
    plan["notes"] = []
    fragment = load_extras(project_folder, previs_record, result.problems, shot_identifier)
    if fragment is not None:
        result.notes.extend(merge_extras(plan, fragment))
    apply_motion(breakdown, [shot], plan, timing.fps, constants, result.problems, shot_identifier)
    result.notes.extend(mount_camera(breakdown, shot, plan, camera))
    result.notes.extend(overlap_notes(plan, stand_ins, lying_names))
    plan["notes"] = list(result.notes)
    finish_plan(plan, result.problems, result.identifier)
    result.plan = plan
    return result


def subject_characters(breakdown, shot, characters):
    found = []
    for item in breakdown.items(shot, "subject"):
        element = element_of(item.first or "")
        if element in characters and element not in found:
            found.append(element)
    return found


def base_plan(breakdown, shot, plan_record, timing, constants):
    ratio = frame_ratio(breakdown)
    width = int(constant(constants, "previs_width_px", 1280))
    orientation = plan_record.orientation + (" (turned from the stored plan)" if plan_record.turned else " (as stored)")
    return {
        "shot": shot.identifier,
        "about": ("Compiled by stage.py previs from the records (blueprint 9); never edit it. Change the records or "
                  "the extras fragment and compile again."),
        "scene": scene_of(shot.identifier),
        "label": shot_words(shot.identifier),
        "description": shot_description(breakdown, shot),
        "framing_critical": is_yes(shot.get("framing_critical")),
        "level": int(number_of(shot.get("previs_level"), 0) or 0),
        "location": plan_record.location,
        "orientation": orientation,
        "fps": timing.fps,
        "frames": timing.frames,
        "handle_frames": timing.handle_frames,
        "resolution": [width, int(round(width / ratio))],
        "facing_tolerance_deg": constant(constants, "facing_tolerance_deg", 20),
        "depth_range_m": None,
        "stills": [],
        "pivots": [],
        "boxes": [],
        "figures": [],
        "animate": [],
        "camera": {},
        "plan_view": {},
        "moments": [],
    }


def camera_entry(breakdown, shot, camera, keys, stand_ins):
    entry = {"lens_mm": round(camera.lens_mm, 2), "sensor_mm": round(camera.sensor_mm, 2)}
    focus = element_of(shot.get("focus_on") or "")
    names = {stand_in.character: stand_in.name for stand_in in stand_ins}
    if focus in names:
        entry["focus_on"] = names[focus]
    focus_word = normalise_word(shot.get("focus") or "")
    if focus_word and focus_word != "none":
        entry["focus"] = focus_word
    entry["setup"] = camera.setup
    entry["keys"] = keys
    return entry


def clash_exclusions(stored, stand_ins, staging, times):
    """Every seat and bed of the set plan, with the stand-ins that rest on it in this shot (blueprint 9)."""
    resting = {}
    for stand_in in stand_ins:
        for moment in times:
            state = staging.state(stand_in.character, moment)
            if state.posture == stand_in.posture and state.resting and state.resting[0]:
                resting.setdefault(state.resting[0], [])
                if stand_in.name not in resting[state.resting[0]]:
                    resting[state.resting[0]].append(stand_in.name)
    found = []
    for name, entry in stored.objects.items():
        if entry.get("furniture") in ("seat", "bed"):
            found.append({"set": name, "stand_ins": resting.get(name, [])})
    return found


def derived_facings(stand_ins, staging, timing, stills):
    """{figure: [[frame, facing_deg], ...]} at the stills, from the records, for PREVIS-03 (figures only)."""
    found = {}
    for stand_in in stand_ins:
        if stand_in.kind != "figure":
            continue
        values = []
        for frame in stills:
            state = staging.state(stand_in.character, timing.time_at(frame))
            if state.posture != stand_in.posture or state.heading is None:
                continue
            values.append([frame, round(blender_facing_deg(state.heading), 2)])
        if values:
            found[stand_in.name] = values
    return found


def mount_camera(breakdown, shot, plan, camera):
    """SETUP mount on a moving thing: parent the camera to it and write its keys relative to it."""
    setup = breakdown.record(shot.get("setup"), "SETUP") if shot.get("setup") else None
    mount = (setup.get("mount") or "world").strip() if setup is not None else "world"
    if normalise_word(mount) in ("world", "none", ""):
        return []
    name = stand_in_name(mount)
    target = plan_object(plan, name)
    if target is None:
        return [f"the camera's mount {mount} is not in the plan, so the camera stays fixed to the room; add {name} "
                "in the extras fragment to carry it"]
    origin = target.get("loc", [0, 0, 0])
    plan["camera"]["parent"] = name
    for key in plan["camera"]["keys"]:
        key[1] = rounded([key[1][index] - origin[index] for index in range(3)])
        key[2] = rounded([key[2][index] - origin[index] for index in range(3)])
    return [f"the camera rides {name}: its keys are measured from {name}'s place at frame 1"]


def unknown_names(plan):
    """Plain lines for every name the kit would not find (a key, parent or focus naming nothing): PREVIS-01."""
    names = {entry.get("name") for key in ("pivots", "boxes", "figures") for entry in plan.get(key, [])}
    found = []
    for entry in plan.get("animate", []):
        if entry.get("object") not in names:
            found.append(f"keys move {entry.get('object')}, which is not in the plan")
    for key in ("pivots", "boxes", "figures"):
        for entry in plan.get(key, []):
            if entry.get("parent") and entry["parent"] not in names:
                found.append(f"{entry.get('name')} hangs from {entry['parent']}, which is not in the plan")
    camera = plan.get("camera") or {}
    for key in ("parent", "focus_on"):
        if camera.get(key) and camera[key] not in names:
            found.append(f"the camera's {key.replace('_', ' ')} {camera[key]} is not in the plan")
    if not camera.get("keys"):
        found.append("the camera has no keys")
    return found


def finish_plan(plan, problems=None, label=None):
    """Leaves out empty lists the kit does not need; names the kit would not find become PREVIS-01 problems."""
    if problems is not None:
        for line in unknown_names(plan):
            problems.append(Problem("E", "PREVIS-01", label or plan.get("shot"), None, line,
                                    "Fix: correct the extras fragment or the records"))
    names = {entry.get("name") for key in ("pivots", "boxes", "figures") for entry in plan.get(key, [])}
    view = plan.get("plan_view") or {}
    if "hide" in view:                      # the kit stops on a name it does not know
        view["hide"] = [name for name in view["hide"] if name in names]
        if not view["hide"]:
            del view["hide"]
    for key in ("pivots", "animate", "clash_exclusions", "notes"):
        if key in plan and not plan[key]:
            del plan[key]
    if not plan.get("derived_facings"):
        plan.pop("derived_facings", None)


# ---------------------------------------------------------------- masters, time slices and shared geometry

def shared_geometry_for(breakdown, shot_identifier):
    """The PREVIS a CUT's shared_geometry names for this shot (the cut's own shot or its 'to' shot), or None."""
    for cut in breakdown.records_of("CUT"):
        value = (cut.get("shared_geometry") or "").strip()
        if not value or normalise_word(value) == "none":
            continue
        own = re.sub(r"-C(\d+)$", r"-SH\1", cut.identifier or "")
        if shot_identifier in (own, (cut.get("to") or "").strip()):
            return value
    return None


def master_target_of(previs_identifier, breakdown):
    record = breakdown.record(previs_identifier, "PREVIS")
    if record is not None and record.get("for"):
        return record.get("for").strip()
    match = PREVIS_ID.match(previs_identifier or "")
    return match.group(1) if match else None


def slices_of(breakdown, previs_identifier):
    """[(shot, first frame, last frame)] for every shot whose time_slice names this master."""
    found = []
    for shot in breakdown.records_of("SHOT"):
        for item in breakdown.items(shot, "time_slice"):
            if item.first == previs_identifier:
                match = FRAMES_TEXT.match(item.get("frames") or "")
                if match:
                    found.append((shot, int(match.group(1)), int(match.group(2))))
    return found


def compile_master_plan(breakdown, previs_identifier, colours=None, project_folder=None, constants=None):
    """CompiledPlan of a master (PV-SC06-MASTER-V01): one plan of the physical event, from the scene's set plan and
    starts, the slices' motion items and the master's extras fragment; its camera is the first slice's."""
    constants = constants if constants is not None else breakdown.constants
    target = master_target_of(previs_identifier, breakdown) or previs_identifier
    match = MASTER_TARGET.match(target)
    scene = match.group(1) if match else scene_of(target)
    result = CompiledPlan(target, scene, "master", master=previs_identifier)
    record = breakdown.record(previs_identifier, "PREVIS") or latest_previs(breakdown, target)
    result.previs_record = record
    slices = slices_of(breakdown, previs_identifier)
    shots = [shot for shot, _, _ in slices]
    first_shot = shots[0] if shots else next(iter(breakdown.shots_of(scene)), None)
    if colours is None:
        colours, _ = stand_in_colours(breakdown, constants)
    location = scene_location(breakdown, scene)
    stored = set_plan(breakdown, location) if location else None
    if stored is None or first_shot is None:
        result.problems.append(Problem("E", "PREVIS-01", previs_identifier, None,
                                       "the master cannot be compiled: its scene has no set plan or no shot"))
        return result
    plan_record = plan_for_shot(breakdown, first_shot)
    camera = camera_for(breakdown, first_shot, plan_record)
    staging = StagingForShot(breakdown, first_shot, plan_record, stored, camera)
    fps = project_fps(breakdown)
    frames = max([last for _, _, last in slices] or [0])
    timing = ShotTiming(fps, max(frames, 1), 0.0, max(frames, 1) / fps,
                        staging.staging.intervals.get(first_shot.identifier, (0.0, 0.0))[0])
    builder = StandInBuilder(breakdown, constants, staging, timing, colours)
    stand_ins = builder.build([timing.first_time])
    plan = base_plan(breakdown, first_shot, plan_record, timing, constants)
    plan.update({"shot": target, "label": shot_words(target), "master": previs_identifier,
                 "description": f"the master of scene {scene_number_words(scene)}: one physical event, cut into "
                                + ", ".join(shot_words(shot.identifier) for shot in shots) if shots else "",
                 "framing_critical": False, "level": int(number_of(record.get("level"), 3) or 3) if record else 3,
                 "handle_frames": 0})
    plan["boxes"] = set_boxes(breakdown, plan_record, constants)
    for stand_in in stand_ins:
        (plan["boxes"] if stand_in.kind == "box" else plan["figures"]).append(stand_in.entry)
        if stand_in.keys:
            plan["animate"].append({"object": stand_in.name, "keys": stand_in.keys})
    plan["clash_exclusions"] = clash_exclusions(stored, stand_ins, staging, [timing.first_time])
    if camera is not None:
        plan["camera"] = camera_entry(breakdown, first_shot, camera, [[1, rounded(camera.position[:3]),
                                                                     rounded(camera.look_at[:3])]], stand_ins)
    fragment = load_extras(project_folder, record, result.problems, previs_identifier)
    if fragment is not None:
        result.notes.extend(merge_extras(plan, fragment))
    if not plan.get("camera"):
        result.problems.append(Problem("E", "PREVIS-01", previs_identifier, None,
                                       "the master has no camera: its first slice has no setup and the extras "
                                       "fragment gives none"))
        return result
    if isinstance(fragment, dict) and fragment.get("frames"):
        plan["frames"] = max(int(fragment["frames"]), plan["frames"])
    apply_motion(breakdown, shots, plan, fps, constants, result.problems, previs_identifier)
    stills = {1, plan["frames"]}
    for _, first, last in slices:
        stills.update({first, last})
    plan["stills"] = sorted(frame for frame in stills if 1 <= frame <= plan["frames"])
    plan["moments"] = [[first, f"{shot_words(shot.identifier)} starts", lines_text(breakdown, shot)]
                       for shot, first, _ in slices]
    ratio = frame_ratio(breakdown)
    motion_used = any(normalise_word(item.first or "") == "free_fall"
                      for shot in shots for item in breakdown.items(shot, "motion"))
    plan["plan_view"] = plan.get("plan_view") or {}
    if not plan["plan_view"].get("size_m"):
        plan["plan_view"] = plan_view(plan_record, plan["camera"]["keys"], ratio, constants,
                                      side=motion_used or is_shaft(plan_record))
    points = [(entry["loc"][0], entry["loc"][1], entry["loc"][2] + entry.get("height", 0) / 2)
              for entry in plan["figures"]]
    if camera is not None and points:
        plan["depth_range_m"] = depth_range(camera, points, constant(constants, "previs_depth_margin_m", 0.5))
    plan["depth_range_m"] = plan.get("depth_range_m") or [0.3, 15.0]
    animated = {entry.get("object") for entry in plan.get("animate", [])}
    plan["derived_facings"] = {name: values for name, values in
                               derived_facings(stand_ins, staging, timing, [1]).items() if name not in animated}
    result.notes.extend(mount_camera(breakdown, first_shot, plan, camera) if camera is not None else [])
    plan["notes"] = list(result.notes)
    finish_plan(plan, result.problems, result.identifier)
    result.plan = plan
    return result


def shifted_keys(keys, offset):
    return [[key[0] - offset] + key[1:] for key in keys]


def compile_from_master(breakdown, shot, slice_item, shared, colours, project_folder, constants, masters):
    """A shot built from a master: a time slice (the master's frames first to last, moved to start at frame 1) or
    shared geometry (the master's set and stand-ins with the shot's own timing); the camera is the shot's own."""
    master_identifier = slice_item.first if slice_item is not None else shared
    result = CompiledPlan(shot.identifier, scene_of(shot.identifier), "slice", master=master_identifier)
    result.framing_critical = is_yes(shot.get("framing_critical"))
    masters = masters if masters is not None else {}
    if master_identifier not in masters:
        masters[master_identifier] = compile_master_plan(breakdown, master_identifier, colours, project_folder, constants)
    master = masters[master_identifier]
    if not master.ok:
        result.problems.append(Problem("E", "PREVIS-01", shot.identifier, "time_slice" if slice_item else None,
                                       f"cannot be compiled: its master {master_identifier} did not compile"))
        return result
    stored = set_plan(breakdown, scene_location(breakdown, scene_of(shot.identifier)))
    plan_record = plan_for_shot(breakdown, shot)
    camera = camera_for(breakdown, shot, plan_record)
    if camera is None:
        result.problems.append(Problem("E", "PREVIS-01", shot.identifier, "setup",
                                       "cannot be compiled: its setup has no complete camera (at, look_at, lens_mm)"))
        return result
    plan = copy.deepcopy(master.plan)
    fps = plan.get("fps", project_fps(breakdown))
    if slice_item is not None:
        match = FRAMES_TEXT.match(slice_item.get("frames") or "")
        if not match or int(match.group(2)) < int(match.group(1)):
            result.problems.append(Problem("E", "PREVIS-01", shot.identifier, "time_slice",
                                           "the frames must be first-last, for example 12-40"))
            return result
        first, last = int(match.group(1)), int(match.group(2))
        offset = first - 1
        frames = last - first + 1
        for entry in plan.get("animate", []):
            entry["keys"] = shifted_keys(entry["keys"], offset)
        timing = ShotTiming(fps, frames, 0.0, frames / fps, 0.0)
        result.notes.append(f"frames {first} to {last} of the master {master_identifier}, moved to start at frame 1")
    else:
        staging_scene = scene_staging(breakdown, scene_of(shot.identifier))
        timing = shot_timing(breakdown, shot, staging_scene, constants)
        frames = timing.frames
        result.notes.append(f"the set and stand-ins of {master_identifier}, shared by a match cut")
    staging = StagingForShot(breakdown, shot, plan_record, stored, camera)
    builder = StandInBuilder(breakdown, constants, staging, timing, colours or stand_in_colours(breakdown, constants)[0])
    notes = []
    keys = camera_keys(breakdown, shot, camera, staging, builder, timing, constants, notes)
    result.notes.extend(notes)
    plan.update({"shot": shot.identifier, "label": shot_words(shot.identifier),
                 "description": shot_description(breakdown, shot), "framing_critical": result.framing_critical,
                 "level": int(number_of(shot.get("previs_level"), 0) or 0), "frames": frames,
                 "handle_frames": timing.handle_frames, "master": master_identifier})
    plan["camera"] = camera_entry(breakdown, shot, camera, keys, [])
    moments = moment_items(breakdown, shot)
    plan["moments"] = [[timing.frame_of_shot_second(start), shows, lines_text(breakdown, shot)]
                       for start, _, shows in moments]
    stills = {1, frames} | {min(frames, max(1, frame)) for frame, _, _ in plan["moments"]}
    plan["stills"] = sorted(stills)
    plan["plan_view"] = plan_view(plan_record, keys, camera.ratio, constants,
                                  side=(master.plan.get("plan_view") or {}).get("direction") == "side")
    if isinstance(plan.get("derived_facings"), dict):
        plan["derived_facings"] = {name: [[1, values[0][1]]] for name, values in plan["derived_facings"].items()
                                   if values}
    previs_record = latest_previs(breakdown, shot.identifier)
    result.previs_record = previs_record
    fragment = load_extras(project_folder, previs_record, result.problems, shot.identifier)
    if fragment is not None:
        result.notes.extend(merge_extras(plan, fragment))
    result.notes.extend(mount_camera(breakdown, shot, plan, camera))
    plan["notes"] = list(result.notes)
    finish_plan(plan, result.problems, result.identifier)
    result.plan = plan
    return result


# ---------------------------------------------------------------- which plans

def scope_scenes(breakdown):
    """The scene IDs PROJECT scope names, or None for all (5.5 PROJECT scope)."""
    project = breakdown.project
    value = (project.get("scope") or "").strip() if project is not None else ""
    if not value or normalise_word(value) in ("all", "none", "open"):
        return None
    known = breakdown.scene_identifiers()
    found = set()
    for piece in split_list(value):
        piece = piece.strip()
        if ".." in piece:
            first, last = [part.strip() for part in piece.split("..", 1)]
            low, high = sort_key_for_identifier(first), sort_key_for_identifier(last)
            found.update(scene for scene in known if low <= sort_key_for_identifier(scene) <= high)
            found.update((first, last))
        elif piece:
            found.add(piece)
    return found


def select_targets(breakdown, shot=None, scene=None, constants=None):
    """(masters [PREVIS IDs], shots [SHOT IDs], notes) to compile."""
    constants = constants if constants is not None else breakdown.constants
    minimum = constant(constants, "previs_plan_level_min", 2)
    notes = []
    if shot:
        wanted = shot.strip()
        if PREVIS_ID.match(wanted):
            return [wanted], [], notes
        if MASTER_TARGET.match(wanted):
            records = previs_records_for(breakdown, wanted)
            names = {item.first for record in breakdown.records_of("SHOT")
                     for item in breakdown.items(record, "time_slice")}
            found = [record.identifier for record in records] or sorted(name for name in names
                                                                        if master_target_of(name, breakdown) == wanted)
            return (found[-1:] if found else []), [], notes
        record = breakdown.record(wanted, "SHOT")
        if record is None:
            return [], [], [f"{wanted} is not a shot in the records"]
        level = number_of(record.get("previs_level"), 0) or 0
        if level < minimum:
            notes.append(f"{shot_words(wanted)} is at grey preview level {level:g}, under {minimum:g}; compiled because "
                         "you asked for it")
        return [], [wanted], notes
    scopes = scope_scenes(breakdown)
    scenes = [identifier for identifier in breakdown.scene_identifiers()
              if (scopes is None or identifier in scopes) and (scene is None or identifier == scene)]
    shots = []
    for identifier in scenes:
        for record in breakdown.shots_of(identifier):
            if (number_of(record.get("previs_level"), 0) or 0) >= minimum:
                shots.append(record.identifier)
    masters = []
    for record in breakdown.records_of("PREVIS"):
        target = (record.get("for") or "").strip()
        match = MASTER_TARGET.match(target)
        if match and match.group(1) in scenes:
            latest = latest_previs(breakdown, target)
            if latest is not None and latest.identifier not in masters:
                masters.append(latest.identifier)
    for identifier in shots:
        for item in breakdown.items(breakdown.record(identifier, "SHOT"), "time_slice"):
            if item.first and item.first not in masters:
                masters.append(item.first)
    return masters, shots, notes


def compile_all(breakdown, masters, shots, colours, project_folder=None, constants=None):
    """[CompiledPlan] for the masters first, then the shots."""
    constants = constants if constants is not None else breakdown.constants
    compiled_masters = {}
    results = []
    for identifier in masters:
        compiled = compile_master_plan(breakdown, identifier, colours, project_folder, constants)
        compiled_masters[identifier] = compiled
        results.append(compiled)
    for identifier in shots:
        results.append(compile_shot_plan(breakdown, identifier, colours, project_folder, constants, compiled_masters))
    return results


# ---------------------------------------------------------------- writing

def plan_file_name(compiled):
    return f"{compiled.identifier}.json"


def write_plan(project_folder, compiled):
    folder = Path(project_folder) / PLANS_FOLDER
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / plan_file_name(compiled)
    temporary = path.with_suffix(".json.part")
    temporary.write_text(json.dumps(compiled.plan, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)
    return path


def store_colours(project_folder, breakdown, colours, new):
    """Writes the colours of newly coloured characters into PROJECT previs_colours (code_state), keeping the old
    file in history. Returns True when the file changed."""
    if not new:
        return False
    from .project_files import Project, history_run_folder, keep_in_history
    from .record_format import write_file
    project = Project(project_folder, breakdown.schema, breakdown.words)
    record_files = project.load_record_files()
    for record_file in record_files:
        for record in record_file.records:
            if record.type_name != "PROJECT":
                continue
            values = list(record.get_all("previs_colours"))
            present = {value.split("|", 1)[0].strip() for value in values}
            for character in sorted(colours, key=sort_key_for_identifier):
                if character not in present:
                    rgb = ", ".join(f"{value:.2f}" for value in colours[character])
                    values.append(f"{character} | rgb: [{rgb}]")
            record.set_items("previs_colours", values, breakdown.schema)
            path = Path(project_folder) / record_file.name
            keep_in_history(history_run_folder(project), path, record_file.name)
            write_file(record_file, path, breakdown.schema)
            return True
    return False


def set_approved(project_folder, breakdown, previs_identifiers, value, only_missing=False):
    """Writes approved (code_state) on PREVIS records, keeping the old files in history: auto once a shot that is
    not framing-critical passed both checks; no on a job that has no approved line yet (not approved so far), so
    the checker's FORM-05 finds the field without the AI ever writing it. Returns the IDs changed."""
    if not previs_identifiers:
        return []
    from .project_files import Project, history_run_folder, keep_in_history
    from .record_format import write_file
    project = Project(project_folder, breakdown.schema, breakdown.words)
    changed = []
    history = None
    for record_file in project.load_record_files():
        touched = False
        for record in record_file.records:
            if record.type_name != "PREVIS" or record.identifier not in previs_identifiers:
                continue
            current = normalise_word(record.get("approved") or "")
            if (only_missing and current) or current in ("auto", "yes") or current == value:
                continue
            record.set_field("approved", value, breakdown.schema)
            changed.append(record.identifier)
            touched = True
        if touched:
            history = history or history_run_folder(project)
            path = Path(project_folder) / record_file.name
            keep_in_history(history, path, record_file.name)
            write_file(record_file, path, breakdown.schema)
    return changed


def jobs_in_words(breakdown, previs_identifiers):
    """Grey preview jobs as the user reads them: 'shot 190, try 1' (for the log in 00 Start here)."""
    found = []
    for identifier in previs_identifiers:
        record = breakdown.record(identifier, "PREVIS")
        target = (record.get("for") or "").strip() if record is not None else ""
        match = PREVIS_ID.match(identifier)
        try_number = int(match.group(2)) if match else None
        words = shot_words(target) if target else "a grey preview"
        found.append(words + (f", try {try_number}" if try_number else ""))
    return "; ".join(found)


def mark_approved(project_folder, breakdown, previs_identifiers):
    """approved: auto on the jobs of shots that are not framing-critical and passed both checks."""
    return set_approved(project_folder, breakdown, previs_identifiers, "auto")


# ---------------------------------------------------------------- rendering (through tools/previs/render_previs.py)

def load_renderer():
    """The module tools/previs/render_previs.py."""
    spec = importlib.util.spec_from_file_location("render_previs", KIT_FOLDER / "render_previs.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def render_compiled(project_folder, compiled_plans, plan_paths, renderer, runner, say):
    """Renders every compiled plan; returns {identifier: result dict}."""
    results = {}
    for compiled in compiled_plans:
        if compiled.identifier not in plan_paths:
            continue
        folder = Path(project_folder) / PREVIEWS_FOLDER / render_folder_name(compiled.identifier)
        say(f"Rendering {shot_words(compiled.identifier)} ({compiled.plan.get('frames')} frames) ...")
        results[compiled.identifier] = renderer.render_plan(plan_paths[compiled.identifier], folder, runner)
    return results


def write_sheets(project_folder, compiled_plans, results, renderer):
    """One contact sheet per scene: framing-critical shots first (they need the user's answer)."""
    written = []
    by_scene = {}
    for compiled in compiled_plans:
        if compiled.identifier in results:
            by_scene.setdefault(compiled.scene, []).append(compiled)
    for scene, items in sorted(by_scene.items(), key=lambda pair: sort_key_for_identifier(pair[0])):
        items.sort(key=lambda compiled: (not compiled.framing_critical, compiled.kind != "master",
                                         sort_key_for_identifier(compiled.identifier)))
        entries = []
        for compiled in items:
            result = results[compiled.identifier]
            label = shot_words(compiled.identifier)
            label = label[0].upper() + label[1:]
            entries.append({"label": label, "description": compiled.plan.get("description", ""),
                            "folder": render_folder_name(compiled.identifier), "stills": compiled.plan.get("stills", []),
                            "moments": compiled.plan.get("moments", []), "fps": compiled.plan.get("fps", 24),
                            "handle_frames": compiled.plan.get("handle_frames", 0),
                            "frames": compiled.plan.get("frames"),
                            "result_lines": renderer.result_lines(result), "needs_answer": compiled.framing_critical,
                            "notes": [note[0].upper() + note[1:] + "." for note in compiled.notes]})
        path = Path(project_folder) / PREVIEWS_FOLDER / contact_sheet_name(scene)
        renderer.write_contact_sheet(path, f"Scene {scene_number_words(scene)}: grey previews", entries,
                                     "Here are the grey previews. Reply with the numbers of any that look wrong, "
                                     "or 'fine'.")
        written.append(path)
    return written


def write_render_report(project_folder, results):
    path = Path(project_folder) / PLANS_FOLDER / REPORT_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    report = {"about": "The last grey preview renders: times, blocking and facings (stage.py previs --render).",
              "plans": results}
    path.write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


# ---------------------------------------------------------------- the command

def add_previs_arguments(parser):
    parser.add_argument("--shot", help="one shot (SC10-SH080) or master (SC06-MASTER or PV-SC06-MASTER-V01)")
    parser.add_argument("--scene", help="only this scene's shots (for example SC10)")
    parser.add_argument("--render", action="store_true",
                        help="render the plans in Blender, run the blocking and facing checks, write contact sheets")


def run_previs(context):
    """stage.py previs: compile the grey preview plans; with --render, render and check them."""
    from .project_files import Project, StageStop
    project_folder = Path(context.project)
    arguments = context.arguments
    breakdown = Breakdown.from_project(project_folder, context.schema, context.words, context.constants)
    renderer = runner = None
    if getattr(arguments, "render", False):
        renderer = load_renderer()
        runner = renderer.find_blender()
    masters, shots, notes = select_targets(breakdown, getattr(arguments, "shot", None),
                                           getattr(arguments, "scene", None), context.constants)
    for note in notes:
        context.say(note[0].upper() + note[1:] + ".")
    if not masters and not shots:
        if getattr(arguments, "shot", None):
            raise StageStop(f"Nothing to compile: {notes[0] if notes else arguments.shot + ' was not found'}. "
                            "Give a shot ID such as SC10-SH080.")
        context.say("No shot in scope is at grey preview level "
                    f"{constant(context.constants, 'previs_plan_level_min', 2)} or more; nothing to compile.")
        context.summary = "previs: nothing to compile"
        return 0
    colours, new = stand_in_colours(breakdown, context.constants)
    if new and store_colours(project_folder, breakdown, colours, new):
        named = ", ".join(person_word(character) for character in new)
        Project(project_folder, context.schema, context.words).add_log_entry(
            f"Gave each character's grey stand-in its own colour ({named}).")
        context.say(f"Gave stand-in colours to {named} (00 Start here, stand-in colours).")
        breakdown = Breakdown.from_project(project_folder, context.schema, context.words, context.constants)
    compiled_plans = compile_all(breakdown, masters, shots, colours, project_folder, context.constants)
    errors = 0
    plan_paths = {}
    for compiled in compiled_plans:
        for problem in compiled.problems:
            context.say(str(problem))
            errors += problem.level == "E"
        if compiled.plan is None or not compiled.ok:
            continue
        path = write_plan(project_folder, compiled)
        plan_paths[compiled.identifier] = path
        for note in compiled.notes:
            context.say(f"Note on {shot_words(compiled.identifier)}: {note}.")
        if compiled.kind != "master" and compiled.previs_record is None:
            context.say(f"No grey preview job for {shot_words(compiled.identifier)} yet: write PREVIS "
                        f"PV-{compiled.identifier}-V01 (for, level, standin_level, route, extras, stills) in "
                        f"{PREVIEWS_FOLDER}/Grey preview jobs.md.")
    waiting = [compiled.previs_record.identifier for compiled in compiled_plans
               if compiled.previs_record is not None and compiled.kind != "master" and not compiled.framing_critical
               and not (compiled.previs_record.get("approved") or "").strip()]
    marked = set_approved(project_folder, breakdown, waiting, "no", only_missing=True)
    if marked:
        Project(project_folder, context.schema, context.words).add_log_entry(
            "Grey previews waiting for their checks: " + jobs_in_words(breakdown, marked) + ".")
        context.say("Marked not approved yet (approved: no, until both checks pass): " + ", ".join(marked) + ".")
    context.say(f"Compiled {len(plan_paths)} grey preview plan{'s' if len(plan_paths) != 1 else ''}: "
                + ", ".join(shot_words(identifier) for identifier in plan_paths) + f" (in {PLANS_FOLDER}).")
    if not getattr(arguments, "render", False):
        context.summary = f"previs: {len(plan_paths)} plans, {errors} errors"
        return 1 if errors else 0
    if runner is None:
        raise StageStop("The plans are written, but rendering needs Blender's Python module (pip install bpy) or "
                        "the Blender app on this computer, and neither was found. Grey previews need Claude Code on "
                        "a computer with Blender.")
    context.say(f"Rendering with {runner.describe()}; each shot takes seconds to a few minutes.")
    results = render_compiled(project_folder, compiled_plans, plan_paths, renderer, runner, context.say)
    approvals = []
    for compiled in compiled_plans:
        result = results.get(compiled.identifier)
        if result is None:
            continue
        label = shot_words(compiled.identifier)
        for check_id, text in result["problems"]:
            context.say(str(Problem("E", check_id, compiled.identifier, None, text,
                                    "Fix: change the marks, moves, setup or extras fragment, then render again")))
            errors += 1
        for line in result.get("excused_lines", []):
            context.say(f"Excused on {label}: {line} (a stand-in resting on its seat or bed).")
        if result["blocking_ok"] and not result["problems"]:
            facings = (f", every facing within {result['tolerance']:g} degrees of the records"
                       if result["facing_checks"] else "")
            seconds = (result.get("render_seconds") or 0) + (result.get("check_seconds") or 0)
            context.say(f"{label[0].upper() + label[1:]}: BLOCKING OK{facings} ({result['frames']} frames, "
                        f"{seconds:.0f} seconds).")
            if (compiled.kind != "master" and not compiled.framing_critical and compiled.previs_record is not None):
                approvals.append(compiled.previs_record.identifier)
            elif compiled.kind != "master" and not compiled.framing_critical:
                context.say(f"{label[0].upper() + label[1:]} passed, but has no grey preview job record yet; write "
                            f"PV-{compiled.identifier}-V01 (level, stand-in detail, route, extras, stills), then it "
                            "is approved on its own.")
    changed = mark_approved(project_folder, breakdown, approvals)
    if changed:
        Project(project_folder, context.schema, context.words).add_log_entry(
            "Grey previews that passed both checks and need no answer, approved on their own: "
            + jobs_in_words(breakdown, changed) + ".")
        context.say("Approved on their own (not framing-critical, both checks passed): " + ", ".join(changed) + ".")
    for path in write_sheets(project_folder, compiled_plans, results, renderer):
        context.say(f"Written: {path.relative_to(project_folder).as_posix()}")
    write_render_report(project_folder, results)
    critical = [shot_words(compiled.identifier) for compiled in compiled_plans
                if compiled.framing_critical and compiled.identifier in results]
    if critical:
        context.say("For the user (framing-critical: " + ", ".join(critical) + "): here are the grey previews. "
                    "Reply with the numbers of any that look wrong, or 'fine'.")
    context.summary = f"previs --render: {len(results)} rendered, {errors} errors"
    return 1 if errors else 0


def register_commands(table):
    if "previs" in getattr(table, "commands", {}):
        return
    table.add("previs", "Grey preview plans from the records; with --render, renders and blocking checks", run_previs,
              add_previs_arguments)
