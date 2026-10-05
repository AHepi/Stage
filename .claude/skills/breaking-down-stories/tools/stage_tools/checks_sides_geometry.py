"""checks_sides_geometry.py: the SIDE and GEOM checks of blueprint section 7.2.

In plain words:
- SIDE-01 to SIDE-05 check sides: every sided feature (a ring, a scar, a wound) has an own side; no state line or
  fixed description holds image-side words; an insert of a sided detail is never flipped; the side a viewer will
  see agrees with what the story says and with what the shot's words say; text in a mirrored scene has a rule
  saying which way it reads.
- GEOM-01 to GEOM-08 check geometry where the set plan and setups allow it: paired singles look to opposite
  sides; the cut between two shots of one person changes size or angle; the size written agrees with the size
  the lens and distance give; setups and marks sit where a camera and a person can be; what a shot says about
  where a person is and which way they face agrees with the set plan; a journey keeps its direction; paired
  singles in one part match.

Every check reads the derived fields of derive_fields.py (the Breakdown of the run) and never changes records.
Each is registered with check_records.register_check (see the note at the top of check_records.py).

Standard library only.

After the full run on The Catch (Project notes 31 and 32):
- a jump cut after a shot numbered below 100 is found (the CUT's number keeps its zeros); SIDE-01 skips a place's
  state; SIDE-04 matches a side word to the right hand;
- SIDE-03 counts the must_show and things that carry the feature; GEOM-05 knows when an object arrives in a later
  scene.

After the three-scene test of the fixed kit (Project notes 35 and 36):
- GEOM-02 measures the 3D angle between the cameras from the person's eyes.
"""

import math
import re

from .check_records import register_check
from .derive_fields import (FACING_ROUND, PLACEMENT_WORDS, SIZE_LADDER, apparent_side, breakdown_for_run, number_of,
                            camera_for, constant, element_name, element_of, eras, eras_unresolved, eyeline_sides,
                            feature_hidden,
                            feature_nouns, focus_subject, is_insert_or_card, is_single, mirror_state_at,
                            normalise_word, person_name, plan_for_shot, point_of, projected_placement,
                            scene_location, scene_mirror_states, scene_of, scene_staging, set_plan,
                            shot_first_line, sided_features, size_check, sort_key_for_identifier, split_list,
                            state_of_reference, subject_items, text_has_orientation_rule, vector, dot, length)

# Nouns that name a feature on one side of a body when a state line names them (SIDE-01). Judgement from K26 and
# B5 ("rings and wounds in state lines"): only features that exist on one side; features that come in pairs
# (sleeves, palms, shoes) need a side item only when the AI declares them. A candidate for rules/words.json.
ONE_SIDED_NOUNS = ("ring", "scar", "wound", "graze", "tattoo", "birthmark", "earring", "bracelet", "wristwatch",
                   "sling", "eyepatch", "parting", "mole")
SIDE_PHRASE = re.compile(r"\b(own\s+)?(left|right)(?:\s+(?:hand|arm|side|shoulder|palm|foot|leg|cheek|eye|ear|"
                         r"wrist|sleeve|temple|knee|hip|thigh))?\b", re.IGNORECASE)
TURNING_WORDS = re.compile(r"\b(turns?|turning|turned|comes back|goes back|back the way|the other way|round)\b",
                           re.IGNORECASE)
STORY_ACTION_TYPES = ("action", None)
# Words after "wound" or "sling" that show a verb ("a scarf wound round her neck"), not a one-sided feature.
NOUNS_THAT_ARE_ALSO_VERBS = ("wound", "sling")
NOT_A_NOUN_AFTER = r"(?:round|around|into|up|about|tight|tightly|through|over|across)\b"


# Body parts that come in pairs: a side word next to one of them may name the other of the pair, so a clause is
# about a sided feature on one of them only when it also names what marks it ("the dressed palm", "the scar").
PAIRED_BODY_NOUNS = {"hand", "hands", "palm", "palms", "arm", "arms", "wrist", "wrists", "eye", "eyes", "ear", "ears",
                     "cheek", "cheeks", "shoulder", "shoulders", "foot", "feet", "leg", "legs", "knee", "knees",
                     "temple", "temples", "hip", "hips", "thigh", "thighs", "sleeve", "sleeves", "finger", "fingers",
                     "thumb", "thumbs", "boot", "boots", "shoe", "shoes", "glove", "gloves"}


def clause_names_this_one(clause, feature):
    """True when a clause is about this sided feature: always for a one-of-a-kind feature (a ring, a scar); for one
    on a paired body part (a dressed palm), only when the clause also names what marks it (dressed)."""
    words = re.findall(r"[a-z]+", (feature or "").lower())
    if not words or words[-1] not in PAIRED_BODY_NOUNS:
        return True
    marks = [word for word in words[:-1] if word not in ("the", "a", "an", "her", "his", "their", "own", "left",
                                                          "right")]
    if not marks:
        return True
    lowered = clause.lower()
    return any(re.search(r"\b" + re.escape(mark), lowered) for mark in marks)


# ---------------------------------------------------------------- shared helpers

def breakdown_of(run):
    return breakdown_for_run(run)


def is_live_frame(shot):
    return not is_insert_or_card(shot)


def scene_parts(breakdown, scene_identifier):
    """{beat ID: part ID} for a scene, from each PART's beats range (first..last)."""
    beats = [beat.identifier for beat in breakdown.beats_of(scene_identifier)]
    found = {}
    for part in breakdown.of_scene("PART", scene_identifier):
        span = [piece.strip() for piece in (part.get("beats") or "").split("..")]
        if len(span) == 2:
            low, high = sort_key_for_identifier(span[0]), sort_key_for_identifier(span[1])
            for beat in beats:
                if low <= sort_key_for_identifier(beat) <= high:
                    found[beat] = part.identifier
        else:
            for beat in split_list(part.get("beats") or ""):
                found[beat] = part.identifier
    return found


def beat_order(breakdown, scene_identifier):
    return {beat.identifier: index for index, beat in enumerate(breakdown.beats_of(scene_identifier))}


def is_turn_beat(breakdown, beat_identifier):
    beat = breakdown.record(beat_identifier, "BEAT")
    return beat is not None and normalise_word(beat.get("turn") or "none") != "none"


def turn_between(breakdown, scene_identifier, earlier, later):
    """True when a turn beat lies after the earlier shot's last beat, up to and including the later shot's beats."""
    order = beat_order(breakdown, scene_identifier)
    earlier_beats = [order[beat] for beat in breakdown.id_list(earlier, "beats") if beat in order]
    later_beats = [order[beat] for beat in breakdown.id_list(later, "beats") if beat in order]
    if not earlier_beats or not later_beats:
        return False
    start, end = max(earlier_beats), max(later_beats)
    beats = breakdown.beats_of(scene_identifier)
    for index in range(start + 1, end + 1):
        if index < len(beats) and is_turn_beat(breakdown, beats[index].identifier):
            return True
    return any(is_turn_beat(breakdown, beat) for beat in breakdown.id_list(later, "beats")
               if beat not in breakdown.id_list(earlier, "beats"))


def shot_hears_speech(breakdown, shot):
    return bool(breakdown.items(shot, "hear"))


def singles_with_eyelines(breakdown, scene_identifier):
    """[(shot, looker, looked-at, side)] for every single whose subject looks at another person and whose eyeline
    side the set plan gives."""
    found = []
    for shot in breakdown.shots_of(scene_identifier):
        if not is_single(shot) or not is_live_frame(shot):
            continue
        item = focus_subject(breakdown, shot)
        if item is None or not item.get("eyeline"):
            continue
        looker = element_of(item.first)
        looked_at = element_of(item.get("eyeline"))
        if not looked_at.startswith("CH-") or looked_at == looker:
            continue
        side = eyeline_sides(breakdown, shot).get(looker)
        found.append((shot, looker, looked_at, side))
    return found


def paired_singles(breakdown, scene_identifier, same_part=False):
    """Pairs of singles (A looking at B, B looking at A) in a scene, optionally within one part."""
    singles = singles_with_eyelines(breakdown, scene_identifier)
    parts = scene_parts(breakdown, scene_identifier) if same_part else {}
    pairs = []
    for index, (first, looker, looked_at, side) in enumerate(singles):
        for second, other_looker, other_looked_at, other_side in singles[index + 1:]:
            if other_looker != looked_at or other_looked_at != looker:
                continue
            if same_part:
                first_parts = {parts.get(beat) for beat in breakdown.id_list(first, "beats")} - {None}
                second_parts = {parts.get(beat) for beat in breakdown.id_list(second, "beats")} - {None}
                if not first_parts & second_parts:
                    continue
            pairs.append(((first, looker, side), (second, other_looker, other_side)))
    return pairs


def shot_label(identifier):
    number = re.search(r"-SH(\d+)$", identifier or "")
    return f"shot {int(number.group(1)):03d}" if number else identifier


# ---------------------------------------------------------------- SIDE

@register_check("SIDE-01", level="E", build=1, title="A sided feature without an own side",
                plain="names a feature on one side of the body (a ring, a scar, a wound) without saying which side")
def check_side_01(run):
    breakdown = breakdown_of(run)
    problems = []
    for type_name in ("STATE", "PROP"):
        for record in run.records(type_name):
            items = breakdown.items(record, "side")
            for item in items:
                own = normalise_word(item.get("own") or "")
                if own not in ("left", "right"):
                    problems.append(run.problem(
                        "E", "SIDE-01", record, "side",
                        f'"{item.first}" has no own side' + (f' ("{item.get("own")}")' if item.get("own") else ""),
                        "Fix: add | own: left or | own: right, the side on the body or thing itself; the side the "
                        "picture shows is worked out per shot (5.4 rule 8)."))
            if type_name != "STATE":
                continue
            if (record.get("element") or record.identifier or "").startswith("LOC-"):
                continue  # a place has no body side: "bullet scars in the roof grid" is not a scar on someone
            state_line = (record.get("state_line") or "").lower()
            covered = set()
            for item in items:
                covered |= feature_nouns(item.first)
            for noun in ONE_SIDED_NOUNS:
                verb_guard = rf"(?!\s+{NOT_A_NOUN_AFTER})" if noun in NOUNS_THAT_ARE_ALSO_VERBS else ""
                if not re.search(rf"\b{noun}s?\b{verb_guard}", state_line):
                    continue
                if not re.search(rf"\bboth\s+(\w+\s+)?{noun}s\b", state_line):
                    if noun not in covered and noun + "s" not in covered:
                        problems.append(run.problem(
                            "E", "SIDE-01", record, "state_line",
                            f'names a {noun} but no side item gives its own side',
                            f"Fix: add - side: {noun} | own: left or right | plot: yes or no."))
    return problems


@register_check("SIDE-02", level="E", build=1, title="Image-side words in a state line or fixed description",
                plain="names a side of the picture where only the body's own side belongs")
def check_side_02(run):
    rule = (run.words or {}).get("image_side_words", {})
    phrases = sorted(rule.get("phrases", []), key=len, reverse=True)
    targets = rule.get("applies_to") or ["STATE.state_line", "CHARACTER.fixed_description", "PROP.fixed_description"]
    problems = []
    for target in targets:
        type_name, _, field_name = target.partition(".")
        for record in run.records(type_name):
            value = record.get(field_name) or ""
            lowered = value.lower()
            for phrase in phrases:
                if re.search(r"(?<![a-z])" + re.escape(phrase.lower()) + r"(?![a-z])", lowered):
                    problems.append(run.problem(
                        "E", "SIDE-02", record, field_name, f'holds the image-side words "{phrase}"',
                        "Fix: write the own side (her own right, the hand nearest the camera); code works out "
                        "the image side for each shot."))
                    break
    return problems


def sided_detail_of_insert(breakdown, shot):
    """The plot-sided detail an insert shows: a feature of the element it is about (focus_on, then must_show) that
    the shot does not keep out of sight. Returns (element, feature) or None."""
    line = shot_first_line(breakdown, shot)
    references = []
    focus = shot.get("focus_on")
    if focus and normalise_word(focus) != "none":
        references.append(focus)
    references += breakdown.id_list(shot, "must_show")
    for reference in references:
        if reference.startswith(("MO-", "TX-")):
            continue
        state_reference = reference
        for item in subject_items(breakdown, shot):
            if element_of(item.first) == element_of(reference):
                state_reference = item.first
        for feature, own, plot in sided_features(breakdown, state_reference, line):
            if plot and not feature_hidden(breakdown, shot, feature) and insert_words_name(breakdown, shot, feature):
                return element_of(reference), feature
    return None


def insert_words_name(breakdown, shot, feature):
    """True when an insert shows the sided feature: its own words (what it is for, its moments, what its people do,
    where its things are, its end) name it, or its must_show or things name a record that carries it (MO-RINGS for
    a wedding ring, read as feature_hidden reads must_not_show). An insert of Iona's boot on a rung does not show
    her ring."""
    nouns = feature_nouns(feature)
    texts = [shot.get("purpose") or "", shot.get("end") or ""]
    texts += [item.get("shows") or "" for item in breakdown.items(shot, "moment")]
    texts += [item.get("does") or "" for item in subject_items(breakdown, shot)]
    texts += [item.get("at") or "" for item in breakdown.items(shot, "thing")]
    joined = " ".join(texts).lower()
    if any(re.search(r"\b" + re.escape(noun) + r"\b", joined) for noun in nouns):
        return True
    shown = breakdown.id_list(shot, "must_show") + [item.first.strip() for item in breakdown.items(shot, "thing")
                                                     if item.first and normalise_word(item.first) != "none"]
    for identifier in shown:
        record = breakdown.record(identifier) or breakdown.record(element_of(identifier))
        words = set(re.findall(r"[a-z]+", identifier.lower()))
        if record is not None:
            words |= set(re.findall(r"[a-z]+", (record.title or "").lower()))
            words |= set(re.findall(r"[a-z]+", (record.get("names") or "").lower()))
        if nouns & words:
            return True
    return False


@register_check("SIDE-03", level="E", build=1, title="A sided insert with flip other than never",
                plain="is a close insert of a one-sided detail that could be flipped, which would put it on the wrong side")
def check_side_03(run):
    breakdown = breakdown_of(run)
    problems = []
    for shot in run.records("SHOT"):
        if normalise_word(shot.get("size") or "") != "insert" and normalise_word(shot.get("kind") or "") != "insert":
            continue
        detail = sided_detail_of_insert(breakdown, shot)
        flip = normalise_word(shot.get("flip") or "auto")
        if detail and flip != "never":
            element, feature = detail
            problems.append(run.problem(
                "E", "SIDE-03", shot, "flip",
                f"is {flip} on an insert of a sided detail ({element_name(breakdown, element)}'s {feature})",
                "Fix: set flip: never; the insert is made from an edited still at its final side (K07)."))
    return problems


def attributed_element(breakdown, text, position, candidates):
    """The candidate element whose name is written last before a position in a text (or None)."""
    best = None
    best_at = -1
    for element in candidates:
        record = breakdown.record(element, "CHARACTER")
        names = [person_name(element)]
        if record is not None:
            names += [name.strip() for name in split_list(record.get("names") or "")]
        for name in names:
            if not name:
                continue
            for match in re.finditer(r"\b" + re.escape(name) + r"\b", text, re.IGNORECASE):
                if match.start() < position and match.start() > best_at:
                    best, best_at = element, match.start()
    return best


def side_claims(text):
    """[(own or apparent, side, start, end)] for every side phrase in a text ('own left hand', 'right hand')."""
    found = []
    for match in SIDE_PHRASE.finditer(text):
        whole = match.group(0).lower()
        if whole in ("left", "right") and not re.search(r"\bon (the|his|her|their) (left|right)\b",
                                                       text[max(0, match.start() - 14):match.end()], re.IGNORECASE):
            continue
        found.append(("own" if match.group(1) else "apparent", match.group(2).lower(), match.start(), match.end()))
    return found


def story_side_statements(breakdown, scene_identifier):
    """[(line, element, feature, own or apparent, side)] for each action line of the scene that states a side of a
    sided feature of a person present ('Saye's wedding ring. On her right hand.')."""
    story = breakdown.story
    scope = breakdown.scene_range(scene_identifier)
    if story is None or scope is None:
        return []
    scene = breakdown.record(scene_identifier, "SCENE")
    people = breakdown.id_list(scene, "characters") if scene is not None else []
    found = []
    for number in range(scope[0], scope[1] + 1):
        kind = story.type_of(number)
        text = story.line(number)
        if not text.strip() or (kind not in STORY_ACTION_TYPES and kind != "action"):
            continue
        claims = side_claims(text)
        if not claims:
            continue
        for element in people:
            for feature, own, plot in sided_features(breakdown, element, number):
                for noun in feature_nouns(feature):
                    for match in re.finditer(r"\b" + re.escape(noun) + r"\b", text, re.IGNORECASE):
                        if attributed_element(breakdown, text, match.start(), people) != element:
                            continue
                        claim = min(claims, key=lambda entry: abs(entry[2] - match.start()))
                        found.append((number, element, feature, claim[0], claim[1]))
    unique = []
    for entry in found:
        if entry not in unique:
            unique.append(entry)
    return unique


@register_check("SIDE-04", level="W", build=1,
                title="A derived apparent side contradicts a side the story states, or one written in does or end",
                plain="shows a one-sided detail on the other side from the one the story or the shot's words give")
def check_side_04(run):
    breakdown = breakdown_of(run)
    problems = []
    if eras_unresolved(breakdown):
        run.skip("SIDE-04", "the mirror rule's era lines are not in the story given, so the sides a viewer sees are "
                            "not known yet")
        return problems
    if breakdown.story is None:
        run.skip("SIDE-04", "the story's own statements of sides need the story (the shots' words were checked)")
    for scene_identifier in breakdown.scene_identifiers():
        for line, element, feature, kind, side in story_side_statements(breakdown, scene_identifier):
            state = state_of_reference(breakdown, element, line)
            own = next((own for name, own, _ in sided_features(breakdown, element, line) if name == feature), None)
            if own is None or state is None:
                continue
            mirror = mirror_state_at(breakdown, element, line)
            derived = own if kind == "own" else apparent_side(own, mirror)
            if derived != side:
                what = (f'side "{feature}" is own {own}, so the picture shows it on {person_name(element)}\'s '
                        f"{apparent_side(own, mirror)} ({mirror}), but line {line} says "
                        f'{"own " if kind == "own" else ""}{side}')
                problems.append(run.problem(
                    "W", "SIDE-04", state, "side", what,
                    "Fix: a side the story states for a mirrored element is an apparent side (K03): record it as "
                    "the other own side, marked inferred."))
    for shot in run.records("SHOT"):
        line = shot_first_line(breakdown, shot)
        for item in subject_items(breakdown, shot):
            element = element_of(item.first)
            features = sided_features(breakdown, item.first, line)
            if not features:
                continue
            mirror = mirror_state_at(breakdown, item.first, line)
            texts = [("does", item.get("does") or "")]
            if len(subject_items(breakdown, shot)) == 1 or person_name(element).lower() in (shot.get("end") or "").lower():
                texts.append(("end", shot.get("end") or ""))
            for field_name, text in texts:
                for clause in re.split(r"[;.]", text):
                    claims = side_claims(clause)
                    if not claims:
                        continue
                    for feature, own, _ in features:
                        if own is None or not any(re.search(r"\b" + re.escape(noun) + r"\b", clause, re.IGNORECASE)
                                                  for noun in feature_nouns(feature)):
                            continue
                        if not clause_names_this_one(clause, feature):
                            continue  # "her left palm" is the other palm, not the dressed one
                        kind, side = claims[0][0], claims[0][1]
                        derived = own if kind == "own" else apparent_side(own, mirror)
                        if derived != side:
                            problems.append(run.problem(
                                "W", "SIDE-04", shot, field_name,
                                f'says {"own " if kind == "own" else ""}{side} for {person_name(element)}\'s '
                                f"{feature}, but it is own {own} and shows as {apparent_side(own, mirror)} here "
                                f"({mirror})",
                                "Fix: write the hand nearest the camera or the own side, or correct the state's "
                                "side."))
    return problems


@register_check("SIDE-05", level="E", build=1, title="A TEXT in a mirrored scene with no orientation rule",
                plain="shows readable words in a mirrored scene without a rule saying which way they read")
def check_side_05(run):
    breakdown = breakdown_of(run)
    problems = []
    if eras_unresolved(breakdown):
        run.skip("SIDE-05", "the mirror rule's era lines are not in the story given, so the mirrored scenes are not "
                            "known yet")
        return problems
    if not eras(breakdown):
        return problems
    mirrored_scenes = {}
    for shot in run.records("SHOT"):
        texts = breakdown.id_list(shot, "text")
        if not texts:
            continue
        scene_identifier = scene_of(shot.identifier)
        if scene_identifier not in mirrored_scenes:
            states = scene_mirror_states(breakdown, scene_identifier)
            era = breakdown.scene_era(scene_identifier)
            mirrored_scenes[scene_identifier] = ("mirrored" in states.values()
                                                 or (era is not None and "reversed" in (era.frame, era.next_frame)))
        if not mirrored_scenes[scene_identifier]:
            continue
        for text_identifier in texts:
            if not text_has_orientation_rule(breakdown, text_identifier):
                problems.append(run.problem(
                    "E", "SIDE-05", shot, "text",
                    f"{text_identifier} is in a mirrored scene but no rule says which way it reads",
                    "Fix: name it (or the thing it is on) in a text, titles or mirror RULE's governs, or give it an "
                    "exception with reads: normal or mirrored."))
    return problems


# ---------------------------------------------------------------- GEOM

@register_check("GEOM-01", level="E", build=1, title="Paired singles in dialogue without opposite eyeline sides",
                plain="has two people's singles looking to the same side of the frame, so they seem not to face each other")
def check_geom_01(run):
    breakdown = breakdown_of(run)
    problems = []
    for scene_identifier in breakdown.scene_identifiers():
        for (first, looker, side), (second, other, other_side) in paired_singles(breakdown, scene_identifier):
            if side is None or other_side is None or "centre" in (side, other_side):
                continue
            if not (breakdown.items(first, "hear") or breakdown.items(second, "hear")):
                continue
            if side == other_side:
                problems.append(run.problem(
                    "E", "GEOM-01", second, "subject",
                    f"{person_name(other)} looks {other_side} here and {person_name(looker)} looks {side} in "
                    f"{first.identifier}; paired singles need opposite eyelines",
                    "Fix: move one camera to the other side of the line, or change the setup so each looks "
                    "toward the other's side of the frame."))
    return problems


def same_person_consecutive(breakdown, scene_identifier):
    """(earlier, later, person) for consecutive shots about the same person (focus_on a person in frame)."""
    shots = [shot for shot in breakdown.shots_of(scene_identifier)
             if normalise_word(shot.get("kind") or "") not in ("card", "black")]
    pairs = []
    for earlier, later in zip(shots, shots[1:]):
        first = focus_subject(breakdown, earlier)
        second = focus_subject(breakdown, later)
        if first is None or second is None or is_insert_or_card(earlier) or is_insert_or_card(later):
            continue
        focus_first = element_of(earlier.get("focus_on") or "")
        focus_second = element_of(later.get("focus_on") or "")
        if element_of(first.first) != focus_first:
            continue
        if element_of(second.first) != focus_second or focus_first != focus_second:
            continue
        pairs.append((earlier, later, focus_first))
    return pairs


def cut_after(breakdown, shot):
    number = re.search(r"-SH(\d+)$", shot.identifier)
    if not number:
        return None
    # a CUT takes the three-digit number of the shot it follows: SC03-SH070 is followed by SC03-C070
    return breakdown.record(f"{scene_of(shot.identifier)}-C{int(number.group(1)):03d}", "CUT")


def angle_between_setups(breakdown, earlier, later, person):
    """The angle in degrees between two shots' cameras seen from the person, or None without geometry."""
    first_plan = plan_for_shot(breakdown, earlier)
    second_plan = plan_for_shot(breakdown, later)
    first_camera = camera_for(breakdown, earlier, first_plan)
    second_camera = camera_for(breakdown, later, second_plan)
    if first_camera is None or second_camera is None:
        if earlier.get("setup") and earlier.get("setup") == later.get("setup"):
            return 0.0
        return None
    placements = projected_placement(breakdown, earlier).get(person)
    if not placements:
        return None
    placement = placements[-1]
    point = placement.point
    if len(point) >= 3 and len(first_camera.position) >= 3 and len(second_camera.position) >= 3:
        # in 3D, from the person's eyes (the placement's point is the eye point, placed at her height on the set
        # plan): a camera much lower or higher is a new angle too
        eyes = point
        one = [first_camera.position[index] - eyes[index] for index in range(3)]
        two = [second_camera.position[index] - eyes[index] for index in range(3)]
    else:
        one = vector(point[:2], first_camera.position[:2])
        two = vector(point[:2], second_camera.position[:2])
    one_length = math.sqrt(sum(value * value for value in one))
    two_length = math.sqrt(sum(value * value for value in two))
    if one_length < 1e-9 or two_length < 1e-9:
        return None
    cosine = max(-1.0, min(1.0, sum(a * b for a, b in zip(one, two)) / (one_length * two_length)))
    return math.degrees(math.acos(cosine))


@register_check("GEOM-02", level="W", build=1,
                title="Consecutive shots of one subject change neither a size step nor 30 degrees",
                plain="cuts between two shots of the same person that are almost the same, which reads as a jump")
def check_geom_02(run):
    breakdown = breakdown_of(run)
    minimum = constant(breakdown.constants, "geometry_angle_change_min_deg", 30)
    problems = []
    for scene_identifier in breakdown.scene_identifiers():
        for earlier, later, person in same_person_consecutive(breakdown, scene_identifier):
            if normalise_word(earlier.get("size") or "") != normalise_word(later.get("size") or ""):
                continue
            cut = cut_after(breakdown, earlier)
            if cut is not None and normalise_word(cut.get("type") or "") == "jump_cut":
                continue
            angle = angle_between_setups(breakdown, earlier, later, person)
            if angle is None or angle >= minimum:
                continue
            problems.append(run.problem(
                "W", "GEOM-02", later, "size",
                f"follows {earlier.identifier} on {person_name(person)} at the same size and only "
                f"{angle:.0f} degrees round",
                f"Fix: change the size by a step or the angle by {minimum} degrees or more, or mark the join a "
                "jump cut with a CUT record."))
    return problems


@register_check("GEOM-03", level="W", build=2, title="The camera crosses the line inside a part without a declared crossing",
                plain="crosses the line between two people inside one part, which flips who is on which side")
def check_geom_03(run):
    run.skip("GEOM-03", "planned for the second build: the side of the line each camera stands on is worked out "
                        "by build, but crossings inside a part are not checked yet")
    return []


@register_check("GEOM-04", level="W", build=1, title="Authored size two or more steps from the computed size",
                plain="gives a shot size that the lens and the distance on the set plan do not give")
def check_geom_04(run):
    breakdown = breakdown_of(run)
    limit = constant(breakdown.constants, "size_step_difference_warning", 2)
    problems = []
    for shot in run.records("SHOT"):
        written = normalise_word(shot.get("size") or "")
        if written not in SIZE_LADDER:
            continue
        check = size_check(breakdown, shot)
        if check is None:
            continue
        steps = [abs(SIZE_LADDER.index(written) - SIZE_LADDER.index(size)) for size in check.sizes if size in SIZE_LADDER]
        if steps and min(steps) >= limit:
            problems.append(run.problem(
                "W", "GEOM-04", shot, "size",
                f"is {written}, but {shot.get('lens_mm') or 'the'} mm at {check.distance_m:.1f} m from "
                f"{person_name(check.subject)} frames {check.visible_height_m:.2f} m of height, "
                f"{'an' if check.size[:1] in 'aeiou' else 'a'} {check.size}",
                "Fix: change the size, or move the setup or the lens so the frame is the size written (the step 8 "
                "file, Camera, gives the sum)."))
    return problems


def wild_wall_names(text):
    return {word for word in ("north", "south", "east", "west") if re.search(rf"\b{word}\b", text or "", re.IGNORECASE)}


def outside_walls(plan, point):
    """The walls a point lies beyond (west when x < 0, and so on), in the plan's own compass."""
    walls = set()
    if point[0] < 0:
        walls.add("west")
    if point[0] > plan.width:
        walls.add("east")
    if point[1] < 0:
        walls.add("south")
    if point[1] > plan.depth:
        walls.add("north")
    return walls


@register_check("GEOM-05", level="E", build=2,
                title="A setup inside an object, a setup outside the room other than through a wild wall, or a mark "
                      "outside the room",
                plain="puts a camera or a mark where it cannot be: inside furniture or behind a wall")
def check_geom_05(run):
    breakdown = breakdown_of(run)
    problems = []
    for location in run.records("LOCATION"):
        plan = set_plan(breakdown, location.identifier)
        if plan is None:
            continue
        for name, point in plan.marks.items():
            if not plan.contains(point):
                problems.append(run.problem("E", "GEOM-05", location, "mark", f"{name} at {list(point)} is outside the room",
                                            "Fix: move the mark inside the plan's size, or place the person with a "
                                            "point in the scene's start or a move."))
    for setup in run.records("SETUP"):
        location = scene_location(breakdown, scene_of(setup.identifier))
        plan = set_plan(breakdown, location) if location else None
        position = point_of(setup.get("at"))
        if plan is None or not position or len(position) < 3:
            continue
        walls = outside_walls(plan, position)
        if walls and not walls <= wild_wall_names(plan.wild_walls):
            problems.append(run.problem(
                "E", "GEOM-05", setup, "at",
                f"{list(position)} is outside the room beyond the {', '.join(sorted(walls))} wall, which is not wild",
                "Fix: move the camera inside the room, or name that wall in the place's wild_walls."))
            continue
        for name, found in plan.objects.items():
            size = found.get("size") or ()
            if len(size) < 3:
                continue
            first = found.get("from_scene")
            if first and sort_key_for_identifier(scene_of(setup.identifier)) < sort_key_for_identifier(first):
                continue  # the object is not there yet in this scene (the tent comes in scene 29)
            centre = found["at"]
            inside = (abs(position[0] - centre[0]) < size[0] / 2 and abs(position[1] - centre[1]) < size[1] / 2
                      and found.get("base", 0.0) <= position[2] <= found.get("base", 0.0) + size[2])
            if inside:
                problems.append(run.problem("E", "GEOM-05", setup, "at",
                                            f"{list(position)} is inside the {name.lower().replace('_', ' ')}",
                                            "Fix: move the camera out of the object."))
    return problems


def placement_distance(first, second):
    if first not in PLACEMENT_WORDS or second not in PLACEMENT_WORDS:
        return None
    return abs(PLACEMENT_WORDS.index(first) - PLACEMENT_WORDS.index(second))


def opposite_facing(first, second):
    if first not in FACING_ROUND or second not in FACING_ROUND:
        return False
    return abs(FACING_ROUND.index(first) - FACING_ROUND.index(second)) == 2


@register_check("GEOM-06", level="W", build=1, title="An authored at or faces contradicts the set-plan projection",
                plain="places a person in the frame, or turns them, differently from the set plan")
def check_geom_06(run):
    breakdown = breakdown_of(run)
    problems = []
    for shot in run.records("SHOT"):
        if not is_live_frame(shot):
            continue
        placements = projected_placement(breakdown, shot)
        for item in subject_items(breakdown, shot):
            element = element_of(item.first)
            samples = placements.get(element)
            if not samples:
                continue
            written_at = normalise_word(item.get("at") or "")
            if written_at in PLACEMENT_WORDS:
                if not any(sample.in_frame for sample in samples):
                    problems.append(run.problem(
                        "W", "GEOM-06", shot, "subject",
                        f"{person_name(element)} is at {written_at}, but the set plan puts them outside this frame",
                        "Fix: move the setup or the person's mark, or take them out of the shot's subjects."))
                    continue
                distances = [placement_distance(written_at, sample.at) for sample in samples if sample.in_frame]
                distances = [value for value in distances if value is not None]
                if distances and min(distances) >= 2:
                    projected = ", ".join(sorted({sample.at for sample in samples if sample.in_frame}))
                    problems.append(run.problem(
                        "W", "GEOM-06", shot, "subject",
                        f"{person_name(element)} is at {written_at}, but the set plan and {shot.get('setup')} put "
                        f"them at {projected}",
                        "Fix: correct at (or leave it out: code projects it), or move the mark or the setup."))
            written_faces = normalise_word(item.get("faces") or "")
            facings = [sample.faces for sample in samples if sample.faces]
            if written_faces in FACING_ROUND and facings and all(opposite_facing(written_faces, faces) for faces in facings):
                problems.append(run.problem(
                    "W", "GEOM-06", shot, "subject",
                    f"{person_name(element)} faces {written_faces}, but the set plan turns them to "
                    f"{', '.join(sorted(set(facings)))}",
                    "Fix: correct faces (or leave it out: code projects it), or the start or move that turns them."))
    return problems


OPPOSITE_TRAVEL = {("frame_left", "frame_right"), ("up", "down"), ("toward_camera", "away")}


def travels_opposite(first, second):
    return (first, second) in OPPOSITE_TRAVEL or (second, first) in OPPOSITE_TRAVEL


def moves_in_shot(breakdown, shot, person):
    """The floor-plan moves of a person that happen during a shot (by the scene's timing)."""
    staging = scene_staging(breakdown, scene_of(shot.identifier))
    begin, end = staging.intervals.get(shot.identifier, (0.0, 0.0))
    return {move.identifier for move in staging.moves if move.who == person and move.start < end and move.end > begin}


@register_check("GEOM-07", level="W", build=1,
                title="travel reverses between shots of one journey without a turn beat or an on-screen change of direction",
                plain="has a person walking one way and then the other way across the cut of one journey")
def check_geom_07(run):
    breakdown = breakdown_of(run)
    problems = []
    for scene_identifier in breakdown.scene_identifiers():
        shots = breakdown.shots_of(scene_identifier)
        seen = {}
        for shot in shots:
            for item in subject_items(breakdown, shot):
                person = element_of(item.first)
                travel = normalise_word(item.get("travel") or "none")
                if travel == "none":
                    continue
                if person in seen:
                    earlier, earlier_item, earlier_travel = seen[person]
                    if travels_opposite(earlier_travel, travel):
                        first_moves = moves_in_shot(breakdown, earlier, person)
                        second_moves = moves_in_shot(breakdown, shot, person)
                        one_journey = bool(first_moves & second_moves) if (first_moves or second_moves) else (
                            shots.index(shot) == shots.index(earlier) + 1
                            and set(breakdown.id_list(earlier, "beats")) & set(breakdown.id_list(shot, "beats")))
                        turned = TURNING_WORDS.search(" ".join(filter(None, [earlier.get("end"), item.get("does"),
                                                                             earlier_item.get("does")])))
                        if one_journey and not turned and not turn_between(breakdown, scene_identifier, earlier, shot):
                            problems.append(run.problem(
                                "W", "GEOM-07", shot, "subject",
                                f"{person_name(person)} travels {travel} here and {earlier_travel} in "
                                f"{earlier.identifier}, in one journey",
                                "Fix: keep the direction, show the turn on screen, or cut on a turn beat."))
                seen[person] = (shot, item, travel)
    return problems


def matched_height(first_shot, second_shot, first_person, second_person):
    """True when two singles' heights match: each at its own subject's eye height, or the same value."""
    first = normalise_word(first_shot.get("height") or "")
    second = normalise_word(second_shot.get("height") or "")
    if first == second:
        return True
    return first == "eye:" + first_person.lower().replace("-", "_") and second == "eye:" + second_person.lower().replace("-", "_") \
        or (first == f"eye:{first_person}".lower() and second == f"eye:{second_person}".lower())


@register_check("GEOM-08", level="W", build=1,
                title="Paired singles within one part differ in size, lens or height with no turn beat between them "
                      "and no why",
                plain="gives one person a closer or different single than the other in the same part of the scene, with no reason")
def check_geom_08(run):
    breakdown = breakdown_of(run)
    problems = []
    for scene_identifier in breakdown.scene_identifiers():
        for (first, looker, _), (second, other, _) in paired_singles(breakdown, scene_identifier, same_part=True):
            differences = []
            if normalise_word(first.get("size") or "") != normalise_word(second.get("size") or ""):
                differences.append(f"size {first.get('size')} against {second.get('size')}")
            if number_of(first.get("lens_mm")) != number_of(second.get("lens_mm")):
                differences.append(f"lens {first.get('lens_mm')} against {second.get('lens_mm')} mm")
            if not matched_height(first, second, looker, other):
                differences.append(f"height {first.get('height')} against {second.get('height')}")
            if not differences:
                continue
            if first.get("why") or second.get("why"):
                continue
            ordered = sorted([first, second], key=lambda shot: sort_key_for_identifier(shot.identifier))
            if turn_between(breakdown, scene_identifier, ordered[0], ordered[1]):
                continue
            problems.append(run.problem(
                "W", "GEOM-08", ordered[1], "size",
                f"is paired with {ordered[0].identifier} in one part but differs ({'; '.join(differences)}) with "
                "no turn beat between them",
                "Fix: match the pair (B1 R7), or write a why naming the story reason for the difference."))
    return problems
