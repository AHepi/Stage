"""checks_physical_sense.py: the PHYS checks: does the plan ask for something a real body could do in a real place?

In plain words (Project notes 42, work item W8, and 43, part B3):
- PHYS-01 room for a body: in a set plan, a mark in a gap narrower than body_pass_clearance_m, a ladder or rungs
  with less than body_climb_clearance_m clear in front of them, or a door or opening too narrow to pass through;
- PHYS-02 held in the teeth: a thing held in the teeth or mouth that is longer than teeth_hold_length_max_m, or
  whose description says heavy, large or long;
- PHYS-03 a line spoken round a thing held in the teeth (a speech's parenthetical "round the ...", or a person who
  speaks on screen in a shot that has them holding something in their teeth and never taking it out);
- PHYS-04 reach: a person who touches, takes or grips a thing of the set plan from further away than they can reach
  (reach_share_of_height of their height; the positions come from the scene's starts and moves);
- PHYS-05 cutting with nothing: someone cuts, slices or saws, and no knife, blade, scissors, razor, shears, saw or
  glass shard is in the words, the shot's things, the person's description and state, or the scene's props;
- PHYS-06 cover from above under something open: people take cover where the roof is a grid, mesh, wire, slats or
  open, and nothing solid is said to be above them;
- PHYS-07 a fixed bar said to roll: a rung, bar, rail or pipe that rolls, with nothing saying it is loose;
- PHYS-08 a person written as weak (weak, frail, drugged; or thin, hurt or exhausted in their build or state) who
  runs or sprints, or who carries, lifts or holds up a person written as heavy, big, broad or tall;
- PHYS-09 doors: a brace against a door (a chair under the handle, a wedge), or a door or gate kicked open, when
  nothing says which way the door opens;
- PHYS-10 one thing per hand: a person holding more than two things at once in one shot;
- PHYS-11 a thing given emphasis that is too small to see at the shot's size (visible_thing_min_size_m_by_size,
  from visible_thing_emphasis_min).

Every one is a warning marked J: a judgement from the plan slips the handover lists (Project notes 42, work item
W8), not a fact from a maker's document, so it stays a suggestion. Each asks a plain question a writer
can answer. Code measures where the plan has numbers (set plans, real sizes, heights); elsewhere the checks read
words, with narrow triggers and quoted story words left out, so that a clean scene (the gold scene 10) raises none.

What these checks cannot see: story logic (a thing sent toward the people about to arrive), what can be seen from
where (a corridor seen from inside a shaft), and speeds (how many floors pass in one shot). Those stay for the
review questions.

Every check reads the records and the derived fields of derive_fields.py and never changes them; each is
registered with check_records.register_check (see the note at the top of check_records.py). Numbers come from
rules/constants.json by name. The word lists below are this module's own; they are candidates for
rules/words.json.

Standard library only.
"""

import math
import re

from .check_records import register_check, scene_of
from .checks_craft_reasons_words import (QUOTED, constant_of, items, people_in, problem_at, quote_for_message,
                                         records_of, size_words, speaker_of, word_of)
from .derive_fields import (breakdown_for_run, character_height, element_of, elements_present, number_of, point_of,
                            scene_location, scene_staging, set_plan)
from .record_format import split_list

# ---------------------------------------------------------------- words (candidates for rules/words.json)

TEETH_HOLD = re.compile(
    r"\b(?:in|between)\s+(?:her|his|their|its|the|my|your)?\s*(?:own\s+)?teeth\b"
    r"|\bteeth\s+(?:clamped|clenched|closed|locked|tight)\s+(?:on|round|around|over)\b"
    r"|\b(?:clamped|clenched|gripped|held)\s+(?:in|between)\s+(?:her|his|their)\s+jaws\b|\bbites?\s+down\s+on\b"
    r"|\b(?:holds?|holding|carries|carrying|grips?|gripping|clamps?|clamping|clenche?s?|clenching)\b"
    r"[^.;]{0,40}\bin\s+(?:her|his|their)\s+mouth\b", re.I)
TAKEN_OUT_OF_TEETH = re.compile(
    r"\b(?:takes?|took|taking|pulls?|pulling|spits?|spitting|drops?|dropping|removes?|removing|lets? go of)\b"
    r"[^.;]{0,30}\b(?:out of|from)\s+(?:her|his|their)\s+(?:teeth|mouth|jaws?)\b|\bspits?\b", re.I)
BIG_WORDS = ("heavy", "large", "long", "big", "bulky", "hefty")
SIZE_IN_WORDS = re.compile(r"\b(\d+(?:\.\d+)?)\s*(centimetres|centimeters|centimetre|centimeter|cm|millimetres|"
                           r"millimeters|mm|metres|meters|metre|meter|m)\b", re.I)
ROUND_THE_THING = re.compile(r"\b(round|around|through)\s+(?:the|her|his|their|a|an)\s+"
                             r"([a-z][a-z-]*(?:\s+[a-z][a-z-]*)?)", re.I)
REACH_VERB = re.compile(
    r"\b(?:touch(?:es)?|takes? hold of|takes?|picks? up|grabs?|grips?|seizes?|clutch(?:es)?|"
    r"reach(?:es)?\s+(?:for|out to|up to|to)|holds? on to|hangs? on to|"
    r"(?:lays?|puts?|rests?|presses?)\s+(?:her|his|their|a|one|both)\s+(?:\w+\s+)?(?:hand|hands|palm|palms)\s+on)\b",
    re.I)
CUT_VERB = re.compile(r"\b(cuts?|cutting|slices?|slicing|saws|sawing|sawed|slits?|slitting|severs?|severing|snips?|"
                      r"snipping|hacks? through)\b", re.I)
NOT_A_CUT_AFTER = re.compile(r"\s+(?:to|away|back|in to|into black|from|between|on the|across to)\b", re.I)
NOT_A_CUT_BEFORE = re.compile(r"\b(?:the|a|an|camera|we|picture|shot|sound|edit|hard|jump|smash|match)\s+$", re.I)
CUTTING_THINGS = ("knife", "knives", "penknife", "blade", "blades", "scissors", "razor", "shears", "saw", "scalpel",
                  "cutter", "machete", "axe", "hatchet", "sword", "bayonet", "clippers", "secateurs", "sickle",
                  "cleaver", "shard", "dagger", "box cutter")
COVER_WORDS = re.compile(r"\b(?:takes?|taking|took)\s+cover\b|\bfor cover\b|\bcover from\b|\bunder cover\b|"
                         r"\bshelters?\s+from\b|\bsheltering\s+from\b|"
                         r"\bhides?\s+from\s+(?:the\s+)?(?:shots|fire|gunfire|bullets|shooting)\b", re.I)
OPEN_ABOVE = re.compile(r"\b(?:open|grid|grille|mesh|wire|slatted|slats|grating|lattice|netting|barred)\s+"
                        r"(?:[a-z-]+\s+)?(?:roof|ceiling|top|overhead)\b|"
                        r"\b(?:roof|ceiling)\s+(?:of\s+)?(?:[a-z-]+\s+){0,2}"
                        r"(?:grid|grille|mesh|grating|slats|lattice|netting|bars|wire)\b|"
                        r"\broofless\b|\bopen to the sky\b|\bopen top\b", re.I)
SOLID_ABOVE = re.compile(r"\b(?:solid|steel|metal|iron|concrete|wooden|wood)\s+(?:[a-z-]+\s+)?"
                         r"(?:plate|sheet|slab|panel|lid|deck|cover)\b|"
                         r"\b(?:plate|sheet|slab|panel|lid|deck)\s+(?:[a-z-]+\s+){0,3}(?:over|above|covers?)\b", re.I)
ROLLING_BAR = re.compile(r"\b(rung|rungs|bar|bars|crossbar|rail|rails|handrail|railing|pipe|pipes)\b[^.;]{0,40}?"
                         r"\b(rolls|roll|rolling|rolled)\b(?!\s+pin)", re.I)
LOOSE_WORDS = re.compile(r"\b(loose|free|falls|fallen|falling|dropped|drops|on the floor|across the floor|along the "
                         r"floor|off the|down the)\b", re.I)
# Weak words: the strong ones count wherever they describe the person; the soft ones (thin is also said of cloth)
# only in their build, state line or the state's changes.
WEAK_ALWAYS = ("weak", "weakened", "frail", "feeble", "emaciated", "starved", "drugged", "sedated", "half-conscious",
               "barely conscious")
WEAK_IN_BODY_ONLY = ("thin", "hurt", "injured", "wounded", "exhausted")
HEAVY_WORDS = ("heavy", "heavyset", "big", "broad", "broad-shouldered", "burly", "bulky", "hulking", "large",
               "muscular", "stocky", "tall")
RUN_VERB = re.compile(r"\b(runs|run|running|ran|sprints?|sprinting|races|racing|dashes|dashing|bolts)\b", re.I)
NOT_A_RUN_AFTER = re.compile(r"\s+(?:\w+\s+)?(?:\w+\s+)?(?:hand|hands|finger|fingers|thumb|thumbs|eyes|tongue|palm|"
                             r"palms|a hand|out of|dry|cold|through her mind|through his mind)\b", re.I)
CARRY_VERB = re.compile(r"\b(carries|carrying|carried|lifts|lifting|lifted|hauls|hauling|drags|dragging|supports|"
                        r"supporting|takes the weight of|bears the weight of)\b|"
                        r"\b(?:holds?|holding|held|props?|propping|propped|keeps?|keeping)\s+(?:[A-Za-z'-]+\s+){0,2}up\b",
                        re.I)
BRACE = re.compile(r"\b(?:wedges?|wedged|wedging|jams?|jammed|jamming|braces?|braced|bracing|props?|propped)\b"
                   r"[^.;]{0,50}\b(?:under|against|beneath)\s+(?:the\s+)?(?:door\s+)?(?:handle|knob|doorknob|lever|door)\b"
                   r"|\b(?:chair|wedge|table|plank|bar)\b[^.;]{0,30}\bunder\s+(?:the\s+)?(?:door\s+)?"
                   r"(?:handle|knob|doorknob|lever)\b", re.I)
KICKED_OPEN = re.compile(r"\b(?:kicks?|kicked|kicking|boots?|booted)\b[^.;]{0,25}\b(?:door|gate|hatch)\b[^.;]{0,25}"
                         r"\bopen\b|\b(?:door|gate|hatch)\b[^.;]{0,15}\b(?:kicked|booted)\s+open\b", re.I)
OPENS_WHICH_WAY = re.compile(r"\bopens?\s+(?:in|inward|inwards|out|outward|outwards|toward|towards|away|into|onto|"
                             r"on to)\b|\bswings?\s+(?:in|inward|inwards|out|outward|outwards|toward|towards|away|"
                             r"into|open toward)\b", re.I)
HOLD_VERB = re.compile(r"\b(holds?|holding|carries|carrying|clutch(?:es|ing)?|grips?|gripping|clasps?|clasping|"
                       r"cradles?|cradling)\b|"
                       r"\bin\s+(?:her|his|their)\s+(?:\w+\s+)?(?:hand|hands|fist|fists|arms|grip)\b", re.I)
HAND_PLACE = re.compile(r"\bin\s+(?:([A-Z][A-Za-z]+)(?:'s|’s)|her|his|their)\s+(?:\w+\s+)?"
                        r"(?:hand|hands|fist|fists|grip|arms|fingers|palm)\b")
# "him" or "her" as the one carried, never "her hand" ("holds her hand up").
CARRIED_PRONOUN = re.compile(r"\b(him|her|them)\b(?!\s+(?:own\s+)?(?:hand|hands|arm|arms|head|chin|face|eyes|palm|"
                             r"palms|finger|fingers|leg|legs|foot|feet)\b)", re.I)
LADDER_WORDS = re.compile(r"\b(ladder|ladders|rung|rungs|step irons|climbing irons)\b", re.I)
OPENING_WORDS = re.compile(r"\b(door|doors|doorway|gate|hatch|trapdoor|opening|gap|manhole)\b", re.I)
ARTICLES = re.compile(r"^(?:the|a|an|her|his|their|its|one|some)\s+|^[a-z]+(?:'s|’s)\s+", re.I)

J_NOTE = "a judgement from the plan slips of Project notes 42"


# ---------------------------------------------------------------- small helpers

def breakdown_of(run):
    return breakdown_for_run(run)


def plain_text(text):
    """A text with its quoted story words blanked out, and curly apostrophes made straight."""
    return QUOTED.sub(" ", (text or "").replace("’", "'"))


def clauses_of(text):
    """The clauses of a text, split at ';' and '.' and at 'then'."""
    return [piece.strip(" ,:") for piece in re.split(r"[;.]|\bthen\b", text or "") if piece.strip(" ,:")]


def whole_word(word):
    return re.compile(r"(?<![A-Za-z'-])" + re.escape(word) + r"(?![A-Za-z'-])", re.I)


def any_word_in(words, text):
    for word in words:
        if whole_word(word).search(text or ""):
            return word
    return None


def shot_texts(run, shot):
    """[(field name, item's first part or None, text, the person the text belongs to or None)] of what a shot says
    happens: its moments, each subject's does, its start and its end."""
    found = [("moment", item.first, item.get("shows"), None) for item in items(run, shot, "moment")]
    found += [("subject", item.first, item.get("does"), element_of((item.first or "").strip()))
              for item in items(run, shot, "subject") if item.first]
    found += [(name, None, shot.get(name), None) for name in ("start", "end")]
    return [entry for entry in found if entry[2]]


def person_names(run, element):
    """The lower-case names a person goes by: their CHARACTER names (with and without a title) and the ID's tail."""
    record = run.record(element)
    names = []
    if record is not None and record.get("names"):
        for name in split_list(record.get("names")):
            name = name.strip().lower()
            if name:
                names.append(name)
                if " " in name:
                    names.append(name.split()[-1])
    if element and "-" in element:
        names.append(element.split("-", 1)[1].replace("-", " ").lower())
    return list(dict.fromkeys(names))


def inside_a_sentence(title):
    """A record title as it reads inside a sentence: a leading article in lower case ("the climber")."""
    first, _, rest = (title or "").partition(" ")
    return f"{first.lower()} {rest}" if first in ("The", "A", "An") and rest else title


def plain_name(run, element):
    record = run.record(element)
    if record is not None and record.title:
        return inside_a_sentence(record.title)
    return element.split("-", 1)[-1].replace("-", " ").title() if element else "someone"


def thing_name(prop):
    return inside_a_sentence(prop.title or prop.identifier)


# The plain form of the verbs PHYS-08 quotes ("Can the patient run?").
PLAIN_VERBS = {"runs": "run", "running": "run", "ran": "run", "sprints": "sprint", "sprint": "sprint",
               "sprinting": "sprint", "races": "race", "racing": "race", "dashes": "dash", "dashing": "dash",
               "bolts": "bolt"}


def plain_verb(verb):
    return PLAIN_VERBS.get(verb.lower(), verb.lower())


def person_in_clause(run, shot, clause, owner=None):
    """Who a clause is about: the text's owner (a subject's does), else the person named first in the clause, else
    the only person in the shot."""
    if owner:
        return owner
    people = [element_of(item.first.strip()) for item in people_in(run, shot)]
    best = None
    for element in people:
        for name in person_names(run, element):
            match = whole_word(name).search(clause)
            if match and (best is None or match.start() < best[0]):
                best = (match.start(), element)
    if best:
        return best[1]
    return people[0] if len(people) == 1 else None


def prop_of(run, reference):
    record = run.record(element_of((reference or "").strip()))
    return record if record is not None and record.type_name == "PROP" else None


def prop_names(run, prop):
    """The lower-case names a thing goes by: its names without articles or owners, their last words, the ID's tail."""
    names = []
    for name in split_list(prop.get("names") or ""):
        name = ARTICLES.sub("", name.strip().lower())
        if name:
            names.append(name)
    if prop.identifier and "-" in prop.identifier:
        names.append(prop.identifier.split("-", 1)[1].replace("-", " ").lower())
    return [name for name in dict.fromkeys(names) if len(name) >= 3]


def prop_length(prop):
    """The longest real size of a thing in metres: its real_size, else a size its description gives, else None."""
    size = point_of(prop.get("real_size"))
    if size:
        return max(size)
    return longest_size_in_words(prop.get("fixed_description"))


def longest_size_in_words(text):
    found = []
    for number, unit in SIZE_IN_WORDS.findall(text or ""):
        unit = unit.lower()
        scale = 0.01 if unit.startswith("cent") or unit == "cm" else 0.001 if unit.startswith("milli") or unit == "mm" \
            else 1.0
        found.append(float(number) * scale)
    return max(found) if found else None


def scene_props(run, scene):
    """The PROP records present in a scene (things its shots show and states that start there)."""
    breakdown = breakdown_of(run)
    found = []
    for element in elements_present(breakdown, scene):
        record = prop_of(run, element)
        if record is not None and record not in found:
            found.append(record)
    return found


def shot_props(run, shot):
    found = []
    for item in items(run, shot, "thing"):
        record = prop_of(run, item.first)
        if record is not None and record not in found:
            found.append(record)
    return found


def all_props(run):
    return list(records_of(run, "PROP"))


def props_named(run, text, props):
    """The things of a list named in a text, each once."""
    found = []
    for prop in props:
        if any(whole_word(name).search(text) for name in prop_names(run, prop)) and prop not in found:
            found.append(prop)
    return found


def state_lines(run, element, shot):
    """The state line and changes of the state a shot names for a person."""
    texts = []
    for item in items(run, shot, "subject"):
        if element_of((item.first or "").strip()) == element:
            state = run.record(item.first.strip())
            if state is not None and state.type_name == "STATE":
                texts += [state.get("state_line") or "", state.get("changes") or ""]
    return texts


def state_texts(run, element, shot):
    """The words describing a person in a shot: their CHARACTER fixed description and build, and their state."""
    record = run.record(element)
    own = [record.get("fixed_description") or "", record.get("build") or ""] if record is not None else []
    return own + state_lines(run, element, shot)


def body_texts(run, element, shot):
    """The words about a person's body only: their build and their state."""
    record = run.record(element)
    return ([record.get("build") or ""] if record is not None else []) + state_lines(run, element, shot)


# ---------------------------------------------------------------- PHYS-01 room for a body

def footprint(found):
    """(x0, y0, x1, y1) of a set-plan object on the floor plan, or None when it has no size."""
    size = found.get("size") or ()
    if len(size) < 2:
        return None
    x, y = found["at"][0], found["at"][1]
    return (x - size[0] / 2, y - size[1] / 2, x + size[0] / 2, y + size[1] / 2)


def blocks_a_body(found):
    """True for an object a body cannot stand in: it starts below 1.5 m and reaches above 0.3 m."""
    size = found.get("size") or ()
    height = size[2] if len(size) > 2 else 1.0
    base = found.get("base", 0.0) or 0.0
    return base < 1.5 and base + height > 0.3


def free_run(plan, boxes, point, axis, sign):
    """How far a body can go from a point along one axis before an object or a wall stops it."""
    other = 1 - axis
    limit = (plan.width if axis == 0 else plan.depth) if sign > 0 else 0.0
    best = abs(limit - point[axis])
    for box in boxes:
        low, high = (box[other], box[other + 2])
        if not low < point[other] < high:
            continue
        near = box[axis] if sign > 0 else box[axis + 2]
        distance = (near - point[axis]) * sign
        if distance >= -1e-9:
            best = min(best, max(distance, 0.0))
    return best


def inside(box, point):
    return box[0] < point[0] < box[2] and box[1] < point[1] < box[3]


@register_check("PHYS-01", level="W", build=1,
                title="Room for a body: a mark in a gap under body_pass_clearance_m, a ladder with under "
                      "body_climb_clearance_m in front, or a door narrower than body_pass_clearance_m (J: Project "
                      "notes 42 W8)",
                plain="leaves no room for a person to stand, pass or climb where the plan puts them")
def check_phys_01(run):
    problems = []
    breakdown = breakdown_of(run)
    passing = float(constant_of(run, "body_pass_clearance_m", 0.5))
    climbing = float(constant_of(run, "body_climb_clearance_m", 0.75))
    for location in records_of(run, "LOCATION"):
        plan = set_plan(breakdown, location.identifier)
        if plan is None:
            continue
        objects = {name: found for name, found in plan.objects.items() if footprint(found)}
        blocking = {name: footprint(found) for name, found in objects.items() if blocks_a_body(found)}
        for name, point in plan.marks.items():
            if not plan.contains(point) or any(inside(box, point) for box in blocking.values()):
                continue
            across_x = free_run(plan, blocking.values(), point, 0, 1) + free_run(plan, blocking.values(), point, 0, -1)
            across_y = free_run(plan, blocking.values(), point, 1, 1) + free_run(plan, blocking.values(), point, 1, -1)
            narrowest = min(across_x, across_y)
            if narrowest < passing - 1e-9:
                problems.append(problem_at(
                    run, "W", "PHYS-01", location, "mark",
                    f"Is there room for a person at {name}? The gap there is {narrowest:.2f} metres across, and a "
                    f"person needs at least {passing:g}",
                    f"Fix: widen the place or move the objects or the mark in the set plan ({J_NOTE}).",
                    containing=name))
        for name, found in objects.items():
            words = " ".join([name.replace("_", " "), str(found.get("furniture") or "")])
            record_words = " ".join(value for value in location.get_all("object") if value.startswith(name + " "))
            box = footprint(found)
            if LADDER_WORDS.search(words) or LADDER_WORDS.search(record_words):
                gaps = {"west": box[0], "east": plan.width - box[2], "south": box[1], "north": plan.depth - box[3]}
                wall = min(gaps, key=gaps.get)
                middle = ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
                others = [other for key, other in blocking.items() if key != name]
                if wall == "west":
                    clear = free_run(plan, others, (box[2], middle[1]), 0, 1)
                elif wall == "east":
                    clear = free_run(plan, others, (box[0], middle[1]), 0, -1)
                elif wall == "south":
                    clear = free_run(plan, others, (middle[0], box[3]), 1, 1)
                else:
                    clear = free_run(plan, others, (middle[0], box[1]), 1, -1)
                if clear < climbing - 1e-9:
                    problems.append(problem_at(
                        run, "W", "PHYS-01", location, "object",
                        f"Can a person climb the {name.replace('_', ' ').lower()}? There are {clear:.2f} metres "
                        f"clear in front of it, and a climber needs about {climbing:g}",
                        f"Fix: give the ladder about {climbing:g} metres clear in front of its rungs in the set plan, "
                        f"or move what stands in front of it ({J_NOTE}).", containing=name))
            elif OPENING_WORDS.search(words) or OPENING_WORDS.search(record_words.split("|")[0]):
                size = found.get("size") or ()
                across = (max(size[0], size[1]) if min(size[0], size[1]) < 0.2 else min(size[0], size[1]))
                if across < passing - 1e-9:
                    problems.append(problem_at(
                        run, "W", "PHYS-01", location, "object",
                        f"Can a person pass through the {name.replace('_', ' ').lower()}? It is {across:.2f} metres "
                        f"wide, and a person needs at least {passing:g}",
                        f"Fix: widen it in the set plan, or let nobody pass through it ({J_NOTE}).", containing=name))
    return problems


# ---------------------------------------------------------------- PHYS-02 and PHYS-03 the teeth

def texts_with_owners(run):
    """[(record, field name, item first, text, owner element, shot or None)] of every shot text and every state line
    that may hold a thing in a person's teeth."""
    found = []
    for shot in records_of(run, "SHOT"):
        for field_name, first, text, owner in shot_texts(run, shot):
            found.append((shot, field_name, first, text, owner, shot))
    for state in records_of(run, "STATE"):
        if state.get("state_line") and element_of(state.identifier).startswith("CH-"):
            found.append((state, "state_line", None, state.get("state_line"), element_of(state.identifier), None))
    return found


def teeth_holds(run):
    """[(record, field, item first, clause, owner, shot, props named in the clause)] of every thing held in the
    teeth, from shots and state lines; worked out once per run."""
    key = ("phys_teeth_holds",)
    if key in run.cache:
        return run.cache[key]
    found = []
    candidates = all_props(run)
    for record, field_name, first, text, owner, shot in texts_with_owners(run):
        for clause in clauses_of(plain_text(text)):
            if TEETH_HOLD.search(clause):
                found.append((record, field_name, first, clause, owner, shot, props_named(run, clause, candidates)))
    run.cache[key] = found
    return found


@register_check("PHYS-02", level="W", build=1,
                title="A thing held in the teeth or mouth that is longer than teeth_hold_length_max_m or described as "
                      "heavy, large or long (J: Project notes 42 W8)",
                plain="has someone hold in their teeth a thing too big or heavy to hold there")
def check_phys_02(run):
    problems = []
    longest = float(constant_of(run, "teeth_hold_length_max_m", 0.2))
    for record, field_name, first, clause, owner, shot, props in teeth_holds(run):
        reasons = []
        if props:
            for prop in props:
                length = prop_length(prop)
                big = any_word_in(BIG_WORDS, prop.get("fixed_description") or "")
                why = []
                if length is not None and length > longest + 1e-9:
                    why.append(f"it is {length:g} metres long")
                if big:
                    why.append(f"its description says {big}")
                if why:
                    reasons.append((thing_name(prop), why))
        else:
            length = longest_size_in_words(clause)
            big = any_word_in(BIG_WORDS, clause)
            why = ([f"it is {length:g} metres long"] if length is not None and length > longest + 1e-9 else []) + (
                [f"the words say {big}"] if big else [])
            if why:
                reasons.append(("this thing", why))
        for name, why in reasons:
            who = f"{plain_name(run, owner)} " if owner else "a person "
            problems.append(problem_at(
                run, "W", "PHYS-02", record, field_name,
                f"Can {who}hold {name} in their teeth? "
                f"{' and '.join(why).capitalize()}",
                f"Fix: make it short and light (at most {longest:g} metres), or let them carry it another way, on a "
                f"strap, in a pocket or on a belt ({J_NOTE}).", containing=(first or "").strip() or None))
    return problems


@register_check("PHYS-03", level="W", build=1,
                title="A line spoken round a thing held in the teeth (J: Project notes 42 W8)",
                plain="has someone speak while a thing is held in their teeth, so the line cannot be understood")
def check_phys_03(run):
    problems = []
    fix = ("Fix: have them take the thing out of their teeth before the line (and put it back after), or move the "
           f"line ({J_NOTE}).")
    holds = teeth_holds(run)
    held_props = {prop.identifier for hold in holds for prop in hold[6]}
    for speech in records_of(run, "SPEECH"):
        text = speech.get("parenthetical") or ""
        if not text or word_of(text) in ("none", ""):
            continue
        plain = text.replace("’", "'")
        hit = None
        if TEETH_HOLD.search(plain):
            hit = "with a thing held in the teeth"
        for preposition, noun in ROUND_THE_THING.findall(plain):
            for prop in all_props(run):
                names = prop_names(run, prop)
                if not any(whole_word(name).search(noun) for name in names):
                    continue
                if preposition.lower() in ("round", "around") or prop.identifier in held_props:
                    hit = f"{preposition.lower()} the {noun.lower()}"
        if hit:
            who = speaker_of(run, speech.identifier)
            problems.append(problem_at(
                run, "W", "PHYS-03", speech, "parenthetical",
                f"Can anyone understand {plain_name(run, who) if who else 'this person'}'s line, said {hit}? A line "
                f"said round something held in the teeth comes out as a mumble", fix))
    for shot in records_of(run, "SHOT"):
        holders = {}
        for record, field_name, first, clause, owner, hold_shot, props in holds:
            if hold_shot is not shot:
                continue
            person = person_in_clause(run, shot, clause, owner)
            if person:
                holders.setdefault(person, (field_name, first))
        if not holders:
            continue
        taken_out = any(TAKEN_OUT_OF_TEETH.search(plain_text(text)) for _, _, text, _ in shot_texts(run, shot))
        if taken_out:
            continue
        for item in items(run, shot, "hear"):
            if word_of(item.get("speaker")) != "on_screen":
                continue
            speaker = speaker_of(run, (item.first or "").strip())
            if speaker in holders:
                field_name, first = holders[speaker]
                problems.append(problem_at(
                    run, "W", "PHYS-03", shot, field_name,
                    f"Can anyone understand {plain_name(run, speaker)}'s line ({item.first.strip()}) while a thing is "
                    f"held in their teeth? Nothing in the shot takes it out", fix,
                    containing=(first or "").strip() or None))
    return problems


# ---------------------------------------------------------------- PHYS-04 reach

def object_names(plan):
    """{plain name: object key} of a set plan's objects; a last word stands for its object only when no other object
    shares it."""
    names = {}
    last_words = {}
    for key in plan.objects:
        plain = key.replace("_", " ").lower()
        names[plain] = key
        last_words.setdefault(plain.split()[-1], []).append(key)
    for word, keys in last_words.items():
        if len(keys) == 1 and len(word) >= 4 and word not in names:
            names[word] = keys[0]
    return names


def distance_to_box(point, box):
    dx = max(box[0] - point[0], 0.0, point[0] - box[2])
    dy = max(box[1] - point[1], 0.0, point[1] - box[3])
    return math.hypot(dx, dy)


@register_check("PHYS-04", level="W", build=1,
                title="A person touches, takes or grips a set-plan object further away than reach_share_of_height of "
                      "their height (J: Project notes 42 W8)",
                plain="has someone touch or take a thing that is out of their reach from where they stand")
def check_phys_04(run):
    problems = []
    breakdown = breakdown_of(run)
    share = float(constant_of(run, "reach_share_of_height", 0.6))
    for shot in records_of(run, "SHOT"):
        scene = scene_of(shot.identifier)
        staging = scene_staging(breakdown, scene)
        plan = staging.plan
        if plan is None or shot.identifier not in staging.intervals:
            continue
        names = object_names(plan)
        begin, end = staging.intervals[shot.identifier]
        moment_spans = {}
        for item in items(run, shot, "moment"):
            match = re.match(r"^(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)$", (item.first or "").strip())
            if match:
                moment_spans[item.first] = (begin + float(match.group(1)), begin + float(match.group(2)))
        reported = set()
        for field_name, first, text, owner in shot_texts(run, shot):
            if field_name not in ("moment", "subject"):
                continue
            span = moment_spans.get(first, (begin, end)) if field_name == "moment" else (begin, end)
            for clause in clauses_of(plain_text(text)):
                verb = REACH_VERB.search(clause)
                if not verb:
                    continue
                person = person_in_clause(run, shot, clause, owner)
                if not person or not staging.known(person):
                    continue
                after = clause[verb.end():]
                for name, key in names.items():
                    if not whole_word(name).search(after) or (person, key) in reported:
                        continue
                    box = footprint(plan.objects[key]) or (plan.objects[key]["at"][0], plan.objects[key]["at"][1],
                                                           plan.objects[key]["at"][0], plan.objects[key]["at"][1])
                    times = sorted({span[0], max(span[0], span[1] - 1e-6)} | {
                        moment for move in staging.moves for moment in (move.start, move.end)
                        if span[0] <= moment <= span[1]})
                    distances = []
                    for moment in times:
                        state = staging.state_at(person, moment)
                        if state is None or state[2] == "lying":
                            distances = []
                            break
                        distances.append(distance_to_box(state[0], box))
                    if not distances:
                        continue
                    reach = share * character_height(breakdown, person)
                    nearest = min(distances)
                    if nearest > reach + 1e-9:
                        reported.add((person, key))
                        problems.append(problem_at(
                            run, "W", "PHYS-04", shot, field_name,
                            f"Can {plain_name(run, person)} reach the {name} from where they stand? They are "
                            f"{nearest:.1f} metres from it, and reach about {reach:.1f} metres",
                            f"Fix: bring them or the thing closer with a move or in the set plan, so the thing is in "
                            f"reach ({J_NOTE}; reach is {share:g} of the person's height).",
                            containing=(first or "").strip() or None))
    return problems


# ---------------------------------------------------------------- PHYS-05 cutting with nothing

def cut_words_in(clause):
    """The cutting verbs of a clause that mean cutting something (never 'the cut', 'cuts to', 'a cut')."""
    found = []
    for match in CUT_VERB.finditer(clause):
        if NOT_A_CUT_BEFORE.search(clause[:match.start()]) or NOT_A_CUT_AFTER.match(clause[match.end():]):
            continue
        found.append(match.group(0))
    return found


@register_check("PHYS-05", level="W", build=1,
                title="Someone cuts, slices or saws and no cutting thing is in the words, the shot's things, the "
                      "person's description and state, or the scene's props (J: Project notes 42 W8)",
                plain="has someone cut something with nothing to cut it with")
def check_phys_05(run):
    problems = []
    for shot in records_of(run, "SHOT"):
        scene = scene_of(shot.identifier)
        tool_texts = None
        reported = False
        for field_name, first, text, owner in shot_texts(run, shot):
            if reported:
                break
            for clause in clauses_of(plain_text(text)):
                verbs = cut_words_in(clause)
                if not verbs:
                    continue
                if any_word_in(CUTTING_THINGS, clause):
                    continue
                if tool_texts is None:
                    tool_texts = []
                    for prop in shot_props(run, shot) + scene_props(run, scene):
                        tool_texts += prop_names(run, prop) + [prop.get("fixed_description") or ""]
                    for item in people_in(run, shot):
                        tool_texts += state_texts(run, element_of(item.first.strip()), shot)
                if any(any_word_in(CUTTING_THINGS, value) for value in tool_texts):
                    continue
                person = person_in_clause(run, shot, clause, owner)
                who = plain_name(run, person) if person else "the person"
                problems.append(problem_at(
                    run, "W", "PHYS-05", shot, field_name,
                    f"What does {who} cut with? The shot says {quote_for_message(verbs[0])}, but nothing in the shot, "
                    f"the person's state or the scene's things can cut (a knife, a blade, scissors, a razor, shears, "
                    f"a saw or a glass shard)",
                    f"Fix: add the cutting thing as a thing in the scene (listed in the additions if the story does "
                    f"not give it) and show it, or change the action ({J_NOTE}).",
                    containing=(first or "").strip() or None))
                reported = True
                break
    return problems


# ---------------------------------------------------------------- PHYS-06 cover from above

@register_check("PHYS-06", level="W", build=1,
                title="People take cover where the roof is a grid, mesh, wire, slats or open, and nothing solid is "
                      "above them (J: Project notes 42 W8)",
                plain="has people take cover under something open, which stops nothing from above")
def check_phys_06(run):
    problems = []
    for shot in records_of(run, "SHOT"):
        scene = scene_of(shot.identifier)
        place_words = None
        for field_name, first, text, owner in shot_texts(run, shot):
            plain = plain_text(text)
            if not COVER_WORDS.search(plain):
                continue
            if place_words is None:
                place_words = " ; ".join(location_record_values(run, scene))
            open_found = OPEN_ABOVE.search(plain) or OPEN_ABOVE.search(place_words)
            if not open_found or SOLID_ABOVE.search(plain) or SOLID_ABOVE.search(place_words):
                continue
            problems.append(problem_at(
                run, "W", "PHYS-06", shot, field_name,
                f"What covers them from above here? The place has {quote_for_message(open_found.group(0))}, and an "
                f"open roof (a grid, mesh, wire or slats) stops nothing",
                f"Fix: put something solid above the place they hide (a slab, a deck, a solid roof) in the set plan "
                f"and the words, or move them under it ({J_NOTE}).", containing=(first or "").strip() or None))
            break
    return problems


def location_record_values(run, scene):
    """The words of a scene's place: every value of its LOCATION record and the state lines of its states."""
    location = scene_location(breakdown_of(run), scene)
    record = run.record(location) if location else None
    if record is None:
        return []
    values = []
    for name in ("headings", "story_job", "anchor", "dressing", "room_sound", "exit", "object", "note"):
        values += [plain_text(value) for value in record.get_all(name)]
    for state in records_of(run, "STATE"):
        if element_of(state.identifier) == location and state.get("state_line"):
            values.append(plain_text(state.get("state_line")))
    return values


# ---------------------------------------------------------------- PHYS-07 a fixed bar that rolls

@register_check("PHYS-07", level="W", build=1,
                title="A rung, bar, rail or pipe said to roll, with nothing saying it is loose (J: Project notes 42 "
                      "W8)",
                plain="has a fixed bar or rung roll, which a bar held at both ends cannot do")
def check_phys_07(run):
    problems = []
    for shot in records_of(run, "SHOT"):
        for field_name, first, text, owner in shot_texts(run, shot):
            for clause in clauses_of(plain_text(text)):
                found = ROLLING_BAR.search(clause)
                if not found or LOOSE_WORDS.search(clause):
                    continue
                problems.append(problem_at(
                    run, "W", "PHYS-07", shot, field_name,
                    f"Is this {found.group(1).lower()} fixed at both ends? A bar held at both ends can turn in a "
                    f"broken bracket, bend or give way, but it cannot roll",
                    f"Fix: write what a fixed bar can do: it bends, cracks, comes away from one end, or holds "
                    f"({J_NOTE}).", containing=(first or "").strip() or None))
                break
    return problems


# ---------------------------------------------------------------- PHYS-08 the weak doing what the strong do

def weak_word(run, element, shot):
    for text in state_texts(run, element, shot):
        found = any_word_in(WEAK_ALWAYS, plain_text(text))
        if found:
            return found
    for text in body_texts(run, element, shot):
        found = any_word_in(WEAK_IN_BODY_ONLY, plain_text(text))
        if found:
            return found
    return None


def heavy_word(run, element, shot):
    record = run.record(element)
    if record is None:
        return None
    for text in (record.get("build") or "", record.get("fixed_description") or ""):
        found = any_word_in(HEAVY_WORDS, plain_text(text))
        if found:
            return found
    lineup = record.get("lineup") or ""
    if re.search(r"\bmass:\s*heavy\b", lineup):
        return "heavy"
    height = number_of(record.get("height_m"))
    if height is not None and height >= float(constant_of(run, "tall_person_height_m", 1.85)) - 1e-9:
        return f"{height:g} metres tall"
    return None


def runs_in(clause):
    for match in RUN_VERB.finditer(clause):
        if NOT_A_RUN_AFTER.match(clause[match.end():]):
            continue
        return match.group(0)
    return None


@register_check("PHYS-08", level="W", build=1,
                title="A person written as weak (weak, frail, drugged; thin, hurt or exhausted in body) who runs or "
                      "sprints, or carries, lifts or holds up a person written as heavy, big, broad or tall (J: "
                      "Project notes 42 W8)",
                plain="has someone written as weak run, or hold up someone heavy")
def check_phys_08(run):
    problems = []
    for shot in records_of(run, "SHOT"):
        people = [element_of(item.first.strip()) for item in people_in(run, shot)]
        reported = False
        for field_name, first, text, owner in shot_texts(run, shot):
            if reported:
                break
            for clause in clauses_of(plain_text(text)):
                run_verb = runs_in(clause)
                carry = CARRY_VERB.search(clause)
                if not run_verb and not carry:
                    continue
                person = person_in_clause(run, shot, clause, owner)
                if not person:
                    continue
                if owner is None:
                    verb_at = (RUN_VERB.search(clause) or carry).start()
                    named = [whole_word(name).search(clause) for name in person_names(run, person)]
                    if not any(match and match.start() < verb_at for match in named) and len(people) != 1:
                        continue
                weak = weak_word(run, person, shot)
                if not weak:
                    continue
                if run_verb:
                    problems.append(problem_at(
                        run, "W", "PHYS-08", shot, field_name,
                        f"Can {plain_name(run, person)}, written as {weak}, {plain_verb(run_verb)}?",
                        f"Fix: let them walk slowly, limp or lean on someone, or say what gives them the strength "
                        f"({J_NOTE}).", containing=(first or "").strip() or None))
                    reported = True
                    break
                after = clause[carry.start():]
                carried = None
                for other in people:
                    if other == person:
                        continue
                    if any(whole_word(name).search(after) for name in person_names(run, other)):
                        carried = other
                        break
                if carried is None and CARRIED_PRONOUN.search(after):
                    others = [other for other in people if other != person]
                    carried = others[0] if len(others) == 1 else None
                heavy = heavy_word(run, carried, shot) if carried else None
                if heavy:
                    problems.append(problem_at(
                        run, "W", "PHYS-08", shot, field_name,
                        f"Can {plain_name(run, person)}, written as {weak}, carry or hold up "
                        f"{plain_name(run, carried)}, written as {heavy}?",
                        f"Fix: let someone else take the weight, let them drag instead of lift, or let both sink to "
                        f"the floor ({J_NOTE}).", containing=(first or "").strip() or None))
                    reported = True
                    break
    return problems


# ---------------------------------------------------------------- PHYS-09 doors

@register_check("PHYS-09", level="W", build=1,
                title="A brace against a door, or a door or gate kicked open, when nothing says which way it opens "
                      "(J: Project notes 42 W8)",
                plain="braces or kicks a door without saying which way it opens")
def check_phys_09(run):
    problems = []
    for shot in records_of(run, "SHOT"):
        scene = scene_of(shot.identifier)
        place_words = None
        for field_name, first, text, owner in shot_texts(run, shot):
            plain = plain_text(text)
            brace, kick = BRACE.search(plain), KICKED_OPEN.search(plain)
            if not brace and not kick:
                continue
            if place_words is None:
                place_words = " ; ".join(location_record_values(run, scene))
            if OPENS_WHICH_WAY.search(plain) or OPENS_WHICH_WAY.search(place_words):
                continue
            if brace:
                what = "Which way does this door open? A brace only holds a door that opens toward it"
            else:
                what = ("Does this door open away from the person kicking it? A door that opens toward them is "
                        "pulled, not kicked")
            problems.append(problem_at(
                run, "W", "PHYS-09", shot, field_name, what,
                f"Fix: say which way the door opens (in the place's exits or objects, or in the shot) and make the "
                f"action fit it ({J_NOTE}).", containing=(first or "").strip() or None))
            break
    return problems


# ---------------------------------------------------------------- PHYS-10 one thing per hand

@register_check("PHYS-10", level="W", build=1,
                title="A person holding more than two things at once in one shot (J: Project notes 42 W8)",
                plain="has someone hold more things at once than two hands can")
def check_phys_10(run):
    problems = []
    for shot in records_of(run, "SHOT"):
        people = [element_of(item.first.strip()) for item in people_in(run, shot)]
        if not people:
            continue
        scene = scene_of(shot.identifier)
        in_shot = shot_props(run, shot)
        candidates = in_shot + [prop for prop in scene_props(run, scene) if prop not in in_shot]
        held = {person: [] for person in people}
        for item in items(run, shot, "thing"):
            prop = prop_of(run, item.first)
            place = item.get("at") or ""
            match = HAND_PLACE.search(place)
            if prop is None or not match:
                continue
            owner = None
            if match.group(1):
                owner = next((person for person in people if match.group(1).lower() in person_names(run, person)),
                             None)
            elif len(people) == 1:
                owner = people[0]
            if owner and prop not in held[owner]:
                held[owner].append(prop)
        for item in people_in(run, shot):
            person = element_of(item.first.strip())
            for clause in clauses_of(plain_text(item.get("does"))):
                if not HOLD_VERB.search(clause) or TEETH_HOLD.search(clause):
                    continue
                for prop in props_named(run, clause, candidates):
                    if prop not in held[person]:
                        held[person].append(prop)
        for person, things in held.items():
            if len(things) > 2:
                problems.append(problem_at(
                    run, "W", "PHYS-10", shot, "subject",
                    f"Can {plain_name(run, person)} hold all of these at once: "
                    f"{', '.join(thing_name(prop) for prop in things)}? A person has two hands",
                    f"Fix: let them put one thing down, pocket it or hand it over first ({J_NOTE}).",
                    containing=person))
    return problems


# ---------------------------------------------------------------- PHYS-11 too small to see

@register_check("PHYS-11", level="W", build=1,
                title="A thing with emphasis visible_thing_emphasis_min or more that is smaller than "
                      "visible_thing_min_size_m_by_size at a wide shot size (J: Project notes 42 W8)",
                plain="gives weight to a thing too small to see at the shot's size")
def check_phys_11(run):
    problems = []
    smallest = constant_of(run, "visible_thing_min_size_m_by_size", {}) or {}
    loudest = float(constant_of(run, "visible_thing_emphasis_min", 2))
    for shot in records_of(run, "SHOT"):
        size = word_of(shot.get("size"))
        if size not in smallest:
            continue
        for item in items(run, shot, "thing"):
            emphasis = number_of(item.get("emphasis"))
            prop = prop_of(run, item.first)
            if emphasis is None or emphasis < loudest - 1e-9 or prop is None:
                continue
            length = prop_length(prop)
            if length is None or length >= float(smallest[size]) - 1e-9:
                continue
            problems.append(problem_at(
                run, "W", "PHYS-11", shot, "thing",
                f"Can the audience see {thing_name(prop)} in a {size_words(size)} shot? It is "
                f"{length:g} metres across and has emphasis {emphasis:g}",
                f"Fix: show it in a closer shot (an insert), make it bigger, or lower its emphasis ({J_NOTE}).",
                containing=(item.first or "").strip()))
    return problems
