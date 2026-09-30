"""film_pass.py: the film pass of step 9: the film strip and the FILM checks of blueprint section 7.2.

In plain words:
- the film strip is one line per shot, in film order: the shot, its beats, role, size, lens, camera move, the saved
  choices it spends, what it makes loud (emphasis), its screen time and its scene's intensity. Step 9's judgement
  unit reads it instead of the whole film ("For machines - do not edit/film strip.txt"; above
  film_strip_tokens_per_unit_max tokens it is also written act by act);
- FILM-01 to FILM-12 judge the whole film as one structure: the ladder (nothing before the climax spends the
  film's tightest size or longest hold unless a peak puts it there), rhymes (a payoff framed as its plant was),
  each character's camera rule, colour monotony across groups of scenes, stacking at a story peak, compliant
  sameness, a longer shot length after a high-intensity scene, the saved choices counted over the whole film,
  heavy-handedness counts, motif counts, loud sets, and each scene's tone against the film's tone range;
- check --film (and check --step 9) also writes what it finds into "12 Whole-film check.md": a plain audit report
  above the divider, then one FINDING record per problem (source: checker), numbered on from the highest finding
  number in the project. Findings already written keep their number, status and reason; only new problems get
  new numbers (steps/09 "How to redo").

How it plugs in: checks_plan_generation_film.py (the family module check_records loads) imports this file, which
registers FILM-01 to FILM-12 with check_records.register_check, and registers one report section with
check_records.register_report_section. That section is called while check writes 13 Health check.md; on a film
run (--film or --step 9) it also writes the film strip and 12 Whole-film check.md, and returns the lines of the
section "The whole film" for 13 Health check. It writes nothing on other runs, and nothing without a project.

Checks only read; every problem line has 7.2's form (level, check ID, record, field, what is wrong, then the fix).
Numbers come from rules/constants.json by name (colour_monotony_run, compliant_sameness_run,
high_intensity_scene_min, extreme_close_up_film_max, push_in_scene_share_max, motif_spines_max, sound_motif_max,
body_motif_max, loud_sets_max, plant_inserts_per_scene_max, undercurrent_scene_share_max,
departments_changing_at_main_turn_max, short_runtime_max_s) and rules/limits.json
(film_strip_tokens_per_unit_max, tokens_per_word_estimate). Readings of 7.2 that the blueprint leaves open are
written next to each check and in the WP4e build log.

Standard library only.

After the full run on The Catch (Project notes 31 and 32):
- the film pass writes no '...' into what it stores, rewrites the old stored wording, refreshes the evidence and fix
  of findings found again, and notes which records the film strip was made from.
"""

import datetime
import math
import re
from dataclasses import dataclass
from pathlib import Path

from .check_records import register_check, register_report_section, same_scene, scene_of
from .derive_fields import (SIZE_LADDER, breakdown_for_run, constant, element_of, focus_subject, is_insert_or_card,
                            number_of, resolve_story_point)
from .record_format import (DIVIDER_LINE, EndLine, Record, TextBlock, load_json, make_record, normalise_word,
                            parse_file, parse_story_point, sort_key_for_identifier, split_item, split_list,
                            write_file)

MACHINE_FOLDER = "For machines - do not edit"
FILM_STRIP_FILE = "film strip.txt"
WHOLE_FILM_FILE = "12 Whole-film check.md"
WHOLE_FILM_TITLE = "Whole-film check"
FILM_STRIP_COLUMNS = ["shot", "beats", "role", "size", "lens", "camera move", "saved choice used", "emphasis",
                      "screen time", "scene intensity"]

SCENE_IDENTIFIER = re.compile(r"^SC(\d{2,3})([A-Z]?)$")
SHOT_NUMBER = re.compile(r"-SH(\d+)$")
BEAT_NUMBER = re.compile(r"-B(\d+)$")
FINDING_NUMBER = re.compile(r"^FIND-(\d+)$")
RESERVE_MATCH = re.compile(r"^\s*([a-z_]+)\s*=\s*([a-z0-9_.]+)\s*$")
# IDs that name a place in a RESERVE's allowed_in: a scene, or a setup, beat, part or shot of one.
PLACE_IDENTIFIER = re.compile(r"\bSC\d{2,3}[A-Z]?(?:-(?:SU|B|SH|P)\d+)?\b")
SCENE_IN_WORDS = re.compile(r"\bscenes?\s+(\d{1,3}[A-Z]?)\b", re.IGNORECASE)
# "the first in scene 13" / "the first in SC13": a use before that scene is outside the saved choice's places.
FIRST_IN = re.compile(r"\bfirst\s+(?:one\s+|use\s+)?in\s+(?:scene\s+(\d{1,3}[A-Z]?)|(SC\d{2,3}[A-Z]?))\b",
                      re.IGNORECASE)
# SCENE keep values that take a scene out of the film (5.5).
NOT_KEPT = ("cut", "merge", "fold")
# PLAN peak components that are story events rather than film components raised at a peak (FILM-05 counts the
# rest: colour, contrast, tightest_size, longest_hold, loudest_sound, motif_payoff, camera_break, sound_rupture).
STORY_PEAKS = ("story", "crisis_choice")
# Frame side words for FILM-02 (5.5 SHOT subject and thing `at`).
LEFT_WORDS = ("left_edge", "left_third")
RIGHT_WORDS = ("right_edge", "right_third")
EMPTY_WORDS = ("none", "open", "auto", "")
DEFAULT_FORMAT = "feature"


# ---------------------------------------------------------------- small helpers shared with the PLAN and GEN checks

def breakdown_of(run):
    """The run's Breakdown (derived fields), made once per run by derive_fields and kept in run.cache."""
    return breakdown_for_run(run)


def is_empty(value):
    return value is None or normalise_word(value) in EMPTY_WORDS


def scene_key(identifier):
    """Story order of a scene ID: SC06 before SC06A before SC07."""
    match = SCENE_IDENTIFIER.match(identifier or "")
    if not match:
        return (10 ** 6, "")
    return (int(match.group(1)), match.group(2))


def shot_number(identifier):
    match = SHOT_NUMBER.search(identifier or "")
    return int(match.group(1)) if match else -1


def beat_number(identifier):
    match = BEAT_NUMBER.search(identifier or "")
    return int(match.group(1)) if match else None


def is_kept(scene):
    return normalise_word(scene.get("keep") or "keep") not in NOT_KEPT


def film_scenes(run):
    """The film's kept scenes (whatever --scene or the scope says), in story order."""
    scenes = [scene for scene in run.records("SCENE") if scene.identifier and is_kept(scene)]
    return sorted(scenes, key=lambda scene: scene_key(scene.identifier))


def scene_is_cut(run, scene_identifier):
    scene = run.record(scene_identifier)
    return scene is not None and scene.type_name == "SCENE" and not is_kept(scene)


def film_shots(run):
    """Every shot of the film's kept scenes, in film order (scene, then shot number); omitted shots left out."""
    shots = [shot for shot in run.records("SHOT") if shot.identifier and not scene_is_cut(run, scene_of(shot.identifier))]
    return sorted(shots, key=lambda shot: (scene_key(scene_of(shot.identifier)), shot_number(shot.identifier)))


def live_shots(run):
    """The film's shots of people and places: inserts, cards and black left out."""
    return [shot for shot in film_shots(run) if not is_insert_or_card(shot)]


def partial_film(run):
    """Why this run cannot see the whole film (a partial scope or an excerpt of the story), or None."""
    if run.scope_scenes is not None:
        return "the project's scope is part of the film"
    story = getattr(run, "story", None)
    if story is not None and getattr(story, "excerpt", False):
        return "the story given is an excerpt"
    return None


def needs_whole_film(run, check_id):
    """True (and one skip line) when the check needs every scene of the film and this run holds part of it."""
    reason = partial_film(run)
    if reason:
        run.skip(check_id, f"needs the whole film, and {reason} (not in the excerpt)")
        return True
    return False


def size_rank(size):
    """Place of a size on the ladder, widest first (insert is not on the ladder): None when not on it."""
    word = normalise_word(size or "")
    return SIZE_LADDER.index(word) if word in SIZE_LADDER else None


def film_format(run):
    """short or feature: PROJECT format (a limited series counts as a feature), else the first estimate's length
    against short_runtime_max_s, else feature."""
    project = run.project_record
    written = normalise_word(project.get("format") or "") if project is not None else ""
    if written == "short":
        return "short"
    if written in ("feature", "limited_series"):
        return "feature"
    plan = run.record("PLAN")
    estimate = number_of(plan.get("runtime_estimate")) if plan is not None else None
    limit = constant(run.constants, "short_runtime_max_s", None)
    if estimate is not None and limit is not None:
        return "short" if estimate < limit else "feature"
    return DEFAULT_FORMAT


def by_format(value, format_name):
    """A constant that has one value for a short and one for a feature."""
    if isinstance(value, dict):
        return value.get(format_name, value.get(DEFAULT_FORMAT))
    return value


def upper_bound(value):
    """The most a range constant allows: [3, 5] -> 5."""
    if isinstance(value, (list, tuple)):
        return value[-1]
    return value


def number_words(value):
    """A number as the records write it: 12, 13.8, 85."""
    if value is None:
        return "?"
    value = float(value)
    if value.is_integer():
        return str(int(value))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def ordinal(number):
    if 10 <= number % 100 <= 20:
        ending = "th"
    else:
        ending = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return f"{number}{ending}"


def place_of(run, record, field_name, first_part=None):
    """(file name, line number) of a record's field line (the item whose first part matches, when one is given);
    (None, None) when the field is not written, so the problem sits on the record's heading."""
    if record is None or not hasattr(record, "key"):
        return None, None
    for record_file, _, line in run.field_lines(record.key, field_name):
        if first_part is not None and (split_item(line.value).first or "").strip() != first_part:
            continue
        return record_file.name, line.line_number
    return None, None


def report(run, level, check_id, record, field_name, what, fix, place=(None, None)):
    """One problem line of 7.2's form, placed at the given (file, line) when known."""
    file_name, line_number = place
    return run.problem(level, check_id, record, field_name, what, fix, line_number=line_number, file_name=file_name)


def id_range_pairs(value):
    """The (first, last) scene pairs of an id_range value: 'SC26..SC27' -> [('SC26', 'SC27')]; 'SC10' ->
    [('SC10', 'SC10')]; a comma list gives one pair per piece."""
    pairs = []
    if is_empty(value):
        return pairs
    for piece in split_list(value):
        if ".." in piece:
            first, last = [part.strip() for part in piece.split("..", 1)]
        else:
            first = last = piece.strip()
        pairs.append((first, last))
    return pairs


def in_pairs(scene_identifier, pairs):
    key = scene_key(scene_identifier)
    return any(scene_key(first) <= key <= scene_key(last) for first, last in pairs)


def pairs_words(pairs):
    return ", ".join(first if first == last else f"{first}..{last}" for first, last in pairs)


# ---------------------------------------------------------------- positions in the story (for "before" and "after")

@dataclass
class Position:
    """Where something sits in the film: its scene (story order), and inside it the story lines and beats."""
    scene: tuple
    first_line: int = None
    last_line: int = None
    first_beat: int = None
    last_beat: int = None
    words: str = ""


def shot_position(breakdown, shot):
    lines = breakdown.lines_of(shot)
    beats = [beat_number(beat) for beat in breakdown.id_list(shot, "beats")]
    beats = [beat for beat in beats if beat is not None]
    return Position(scene_key(scene_of(shot.identifier)), min(lines) if lines else None, max(lines) if lines else None,
                    min(beats) if beats else None, max(beats) if beats else None, shot.identifier)


def story_point_position(breakdown, text):
    """The Position of a story point ('SC13 "Now he looks at her." = SC13-B05'), or None when it is not one."""
    parsed = parse_story_point(text or "")
    if parsed is None:
        if SCENE_IDENTIFIER.match((text or "").strip()):
            return Position(scene_key(text.strip()), words=text.strip())
        return None
    scene_identifier, _, stored = parsed
    point = resolve_story_point(breakdown, text)
    beat = beat_number(stored) if stored else beat_number(point.beat) if point.beat else None
    return Position(scene_key(scene_identifier), point.line, point.line, beat, beat, text.strip())


def ends_before(first, second):
    """True when `first` ends before `second` starts; False when not; None when it cannot be told."""
    if first is None or second is None:
        return None
    if first.scene != second.scene:
        return first.scene < second.scene
    if first.last_line is not None and second.first_line is not None:
        return first.last_line < second.first_line
    if first.last_beat is not None and second.first_beat is not None:
        return first.last_beat < second.first_beat
    return None


# ---------------------------------------------------------------- saved choices (RESERVE) and what a shot spends

def reserve_match(reserve):
    """(field, value) of a RESERVE's match ('frame_detail = symmetrical_profile'), or None for manual or unreadable."""
    written = reserve.get("match") or ""
    found = RESERVE_MATCH.match(normalise_word_spaces(written))
    if not found:
        return None
    return found.group(1), normalise_word(found.group(2))


def normalise_word_spaces(text):
    """'Frame detail = symmetrical profile' -> 'frame_detail = symmetrical_profile' (each side of '=' as a word)."""
    if "=" not in text:
        return text.strip()
    left, right = text.split("=", 1)
    return f"{normalise_word(left)} = {normalise_word(right)}"


def value_matches(record, field_name, value):
    """True when one of the record's values of the field (its first part, for an item) is the value."""
    for written in record.get_all(field_name):
        first = split_item(written).first or written
        word = normalise_word(first)
        if word == value:
            return True
        both_numbers = re.fullmatch(r"-?\d+(\.\d+)?", value) and re.fullmatch(r"-?\d+(\.\d+)?", first.strip())
        if both_numbers and float(first) == float(value):
            return True
    return False


def reserve_uses(run, reserve):
    """The records (shots, or beats for a beat field such as pause_after) that spend a saved choice, in film order."""
    matched = reserve_match(reserve)
    if matched is None:
        return None
    field_name, value = matched
    if run.schema.field("SHOT", field_name) is not None:
        return [shot for shot in film_shots(run) if value_matches(shot, field_name, value)]
    if run.schema.field("BEAT", field_name) is not None:
        beats = [beat for beat in run.records("BEAT") if beat.identifier
                 and not scene_is_cut(run, scene_of(beat.identifier))]
        beats.sort(key=lambda beat: (scene_key(scene_of(beat.identifier)), beat_number(beat.identifier) or 0))
        return [beat for beat in beats if value_matches(beat, field_name, value)]
    return None


def reserves_spent_by(run):
    """{shot ID: [RC IDs]}: the saved choices each shot spends (by the RESERVE's match, or cited in because)."""
    key = "film_pass.reserves_spent_by"
    if key in run.cache:
        return run.cache[key]
    spent = {}
    reserves = run.records("RESERVE")
    for reserve in reserves:
        for record in reserve_uses(run, reserve) or []:
            if record.type_name == "SHOT":
                spent.setdefault(record.identifier, []).append(reserve.identifier)
    known = {reserve.identifier for reserve in reserves}
    for shot in film_shots(run):
        for piece in split_list(shot.get("because") or ""):
            if piece in known and piece not in spent.get(shot.identifier, []):
                spent.setdefault(shot.identifier, []).append(piece)
    run.cache[key] = spent
    return spent


# ---------------------------------------------------------------- the film strip

def emphasis_words(shot):
    """The things a shot makes loud: 'MO-MINT 2' for each thing item with emphasis 1 or more, or 'none'."""
    found = []
    for written in shot.get_all("thing"):
        item = split_item(written)
        level = number_of(item.get("emphasis"))
        if item.first and not is_empty(item.first) and level is not None and level >= 1:
            found.append(f"{item.first} {number_words(level)}")
    return ", ".join(found) or "none"


def act_of_scene(run, scene_identifier):
    """The PLAN act whose scenes hold the scene, or None."""
    plan = run.record("PLAN")
    if plan is None or scene_identifier is None:
        return None
    for written in plan.get_all("act"):
        item = split_item(written)
        if in_pairs(scene_identifier, id_range_pairs(item.get("scenes") or "")):
            return item.first
    return None


def film_strip_rows(run):
    """[(act name or None, strip line)] for every shot of the film, in film order."""
    spent = reserves_spent_by(run)
    intensity = {scene.identifier: scene.get("scene_intensity") for scene in run.records("SCENE") if scene.identifier}
    rows = []
    for shot in film_shots(run):
        scene_identifier = scene_of(shot.identifier)
        beats = ", ".join(split_list(shot.get("beats") or "")) or "none"
        lens = number_of(shot.get("lens_mm"))
        screen_time = number_of(shot.get("screen_time"))
        cells = [shot.identifier, beats, shot.get("role") or "none", shot.get("size") or "none",
                 number_words(lens) if lens is not None else "none", shot.get("move") or "none",
                 ", ".join(spent.get(shot.identifier, [])) or "none", emphasis_words(shot),
                 number_words(screen_time) if screen_time is not None else "none",
                 intensity.get(scene_identifier) or "none"]
        rows.append((act_of_scene(run, scene_identifier), " | ".join(str(cell) for cell in cells)))
    return rows


def film_strip_text(rows, part_words=""):
    """The film strip as text: a note, the columns, then the lines under a heading for each act."""
    lines = [f"Film strip{part_words}: one line per shot, in film order. Written by stage.py check --film; never edit.",
             "Columns: " + " | ".join(FILM_STRIP_COLUMNS), ""]
    current = object()
    for act, row in rows:
        if act != current:
            if len(lines) > 3:
                lines.append("")
            lines.append(f"## {act}" if act else "## shots in no act")
            current = act
        lines.append(row)
    return "\n".join(lines) + "\n"


def strip_tokens(text):
    """An estimate of a text's tokens: words x tokens_per_word_estimate (rules/limits.json)."""
    per_word = 1.4
    try:
        limits = load_json("rules/limits.json")
        per_word = float(limits.get("tokens_per_word_estimate", {}).get("value", per_word))
    except (OSError, ValueError, AttributeError):
        pass
    return int(math.ceil(len(text.split()) * per_word))


def strip_token_limit(run):
    limit = constant(run.constants, "film_strip_tokens_per_unit_max", None)
    if limit is None:
        try:
            limit = load_json("rules/limits.json").get("film_strip_tokens_per_unit_max", {}).get("value")
        except (OSError, ValueError, AttributeError):
            limit = None
    return limit


def safe_part_name(text):
    return re.sub(r'[\\/:*?"<>|\x00-\x1f]', "", text or "no act").strip() or "no act"


def write_film_strip(run, project_folder):
    """Write 'film strip.txt' (and, above film_strip_tokens_per_unit_max tokens, one file per act) into the
    machine folder. Returns (number of shots, number of scenes, estimated tokens, [file names written])."""
    rows = film_strip_rows(run)
    folder = Path(project_folder) / MACHINE_FOLDER
    folder.mkdir(parents=True, exist_ok=True)
    text = film_strip_text(rows)
    (folder / FILM_STRIP_FILE).write_text(text, encoding="utf-8")
    written = [FILM_STRIP_FILE]
    tokens = strip_tokens(text)
    limit = strip_token_limit(run)
    if limit and tokens > limit:
        acts = []
        for act, _ in rows:
            if act not in acts:
                acts.append(act)
        for index, act in enumerate(acts, start=1):
            part_rows = [(row_act, row) for row_act, row in rows if row_act == act]
            name = f"film strip - part {index} - {safe_part_name(act)}.txt"
            (folder / name).write_text(film_strip_text(part_rows, f", part {index} of {len(acts)}"), encoding="utf-8")
            written.append(name)
    scenes = {scene_of(row.split(" | ", 1)[0]) for _, row in rows}
    from .project_files import remember_made_from
    remember_made_from(project_folder, FILM_STRIP_FILE)
    return len(rows), len(scenes), tokens, written


# ---------------------------------------------------------------- FILM-01 the ladder

def peak_places(run, component, scene_identifier):
    """True when a PLAN peak of this component names the scene and gives a reason."""
    plan = run.record("PLAN")
    if plan is None:
        return False
    for written in plan.get_all("peak"):
        item = split_item(written)
        if normalise_word(item.first or "") != component:
            continue
        if same_scene(item.get("scene"), scene_identifier) and not is_empty(item.get("reason")):
            return True
    return False


def climax_pairs(run):
    plan = run.record("PLAN")
    return id_range_pairs(plan.get("climax")) if plan is not None else []


@register_check("FILM-01", level="W", build=1,
                title="Ladder: a scene before the climax spends the film's tightest size or longest hold, unless "
                      "the peaks place it there",
                plain="spends the film's closest size or longest hold before the climax, and the story plan does "
                      "not place a peak there")
def check_film_01(run):
    """The film's tightest size is the tightest ladder size of any shot of a person or place (inserts, cards and black
    left out); its longest hold the longest screen time of such a shot. A scene before the climax's first scene that
    reaches either is reported once per measure, unless PLAN has a peak tightest_size or longest_hold on that scene
    with a reason (counterpoint, K12). It needs the whole film's shots."""
    if needs_whole_film(run, "FILM-01"):
        return []
    pairs = climax_pairs(run)
    if len(pairs) != 1:
        run.skip("FILM-01", "the story plan names no single climax yet (PLAN-01 reports it)")
        return []
    first_climax = scene_key(pairs[0][0])
    shots = live_shots(run)
    scenes_without_shots = [scene.identifier for scene in film_scenes(run)
                            if scene_key(scene.identifier) <= scene_key(pairs[0][1])
                            and not any(same_scene(scene_of(shot.identifier), scene.identifier) for shot in film_shots(run))]
    if not shots or scenes_without_shots:
        run.skip("FILM-01", "runs once every scene up to the climax has its shots"
                 + (f" ({', '.join(scenes_without_shots[:3])} not yet)" if scenes_without_shots else ""))
        return []
    ranks = [size_rank(shot.get("size")) for shot in shots]
    tightest = max((rank for rank in ranks if rank is not None), default=None)
    longest = max((number_of(shot.get("screen_time"), 0.0) for shot in shots), default=None)
    problems = []
    reported = set()
    for shot in shots:
        scene_identifier = scene_of(shot.identifier)
        if scene_key(scene_identifier) >= first_climax or not run.in_scope(shot.identifier):
            continue
        rank = size_rank(shot.get("size"))
        if tightest is not None and rank == tightest and (scene_identifier, "size") not in reported \
                and not peak_places(run, "tightest_size", scene_identifier):
            reported.add((scene_identifier, "size"))
            problems.append(report(
                run, "W", "FILM-01", shot, "size",
                f"{shot.get('size')} is the film's tightest size, spent in {scene_identifier} before the climax "
                f"{pairs_words(pairs)}, and no peak tightest_size places it there",
                f"Fix: keep {scene_identifier} wider than the film's tightest size, or add to the story plan "
                f"'peak: tightest_size | scene: {scene_identifier} | reason: <why>', the why quoting the line where the "
                "story peaks.",
                place_of(run, shot, "size")))
        seconds = number_of(shot.get("screen_time"), 0.0)
        if longest and seconds == longest and (scene_identifier, "hold") not in reported \
                and not peak_places(run, "longest_hold", scene_identifier):
            reported.add((scene_identifier, "hold"))
            problems.append(report(
                run, "W", "FILM-01", shot, "screen_time",
                f"{number_words(seconds)} s is the film's longest hold, spent in {scene_identifier} before the climax "
                f"{pairs_words(pairs)}, and no peak longest_hold places it there",
                f"Fix: shorten the hold below the film's longest, or add to the story plan 'peak: longest_hold | "
                f"scene: {scene_identifier} | reason: <why>', the why quoting the line where the story peaks.",
                place_of(run, shot, "screen_time")))
    return problems


# ---------------------------------------------------------------- FILM-02 rhymes

def frame_side(text):
    """left, right or centre from an `at` value (placement words or a short description), or None."""
    word = normalise_word(text or "")
    if word in LEFT_WORDS:
        return "left"
    if word in RIGHT_WORDS:
        return "right"
    if word == "centre":
        return "centre"
    lowered = (text or "").lower()
    has_left, has_right = bool(re.search(r"\bleft\b", lowered)), bool(re.search(r"\bright\b", lowered))
    if has_left and not has_right:
        return "left"
    if has_right and not has_left:
        return "right"
    if re.search(r"\b(centre|center|middle)\b", lowered):
        return "centre"
    return None


def thing_side(shot, element):
    """The frame side of the thing item that names this element (or its state) in a shot, or None."""
    for written in shot.get_all("thing"):
        item = split_item(written)
        if item.first and (item.first == element or element_of(item.first) == element_of(element)):
            return frame_side(item.get("at"))
    return None


def framing_of(shot, element):
    lens = number_of(shot.get("lens_mm"))
    return {"lens_mm": number_words(lens) if lens is not None else None,
            "angle": normalise_word(shot.get("angle") or "") or None,
            "size": normalise_word(shot.get("size") or "") or None,
            "frame side": thing_side(shot, element) if element else None}


OTHER_FRAME_SIDE = {"left": "right", "right": "left", "centre": "centre"}


def side_reversed_on_purpose(item):
    """True when a rhyme declares that its payoff mirrors the plant's frame side on purpose (a rhyme item's or a
    motif appearance's sub-part side: reversed), as The Catch's scene 29 rings reverse the kitchen's reflection
    two-shot (B3 §8.2)."""
    return item is not None and normalise_word(item.get("side") or "") == "reversed"


def framing_differences(plant_shot, payoff_shot, element, side_reversed=False):
    """[(what, plant's value, payoff's value)] where the payoff's framing differs from the plant's. With side_reversed
    the payoff's frame side is expected on the other side of the frame from the plant's."""
    planted, paid = framing_of(plant_shot, element), framing_of(payoff_shot, element)
    if side_reversed and planted["frame side"] is not None:
        planted["frame side"] = OTHER_FRAME_SIDE.get(planted["frame side"], planted["frame side"])
    return [(name, planted[name], paid[name]) for name in planted
            if planted[name] is not None and paid[name] is not None and planted[name] != paid[name]]


def shots_linking(run, key, plant_identifier):
    """(shot, thing element) for every shot whose thing item carries `plant:` or `payoff:` naming the plant."""
    found = []
    for shot in film_shots(run):
        for written in shot.get_all("thing"):
            item = split_item(written)
            if (item.get(key) or "").strip() == plant_identifier:
                found.append((shot, item.first))
    return found


def rhyme_line(run, plant_shot, payoff_shot, element, differences, about, side_reversed=False):
    field_name, planted, paid = differences[0]
    field_word = "lens_mm" if field_name == "lens_mm" else ("thing" if field_name == "frame side" else field_name)
    rest = "; ".join(f"{name} {new} against {old}" for name, old, new in differences[1:])
    if side_reversed and field_name == "frame side":
        what = (f"frame side {paid} is not the other side from the plant shot {plant_shot.identifier}'s, though "
                f"{about} rhymes with its side reversed")
    else:
        what = (f"{paid} differs from the plant shot {plant_shot.identifier}'s {planted}"
                + (f" (also {rest})" if rest else "") + f", though {about} rhymes")
    framing = framing_of(plant_shot, element)
    if side_reversed and framing["frame side"] is not None:
        framing["frame side"] = OTHER_FRAME_SIDE.get(framing["frame side"], framing["frame side"])
    wanted = ", ".join(f"{name} {value}" for name, value in framing.items() if value is not None)
    return report(run, "W", "FILM-02", payoff_shot, field_word, what,
                  f"Fix: frame the payoff as the plant was ({wanted}), or, when the story reverses the side on purpose, "
                  "write side: reversed on the rhyme.",
                  place_of(run, payoff_shot, field_word if field_word != "thing" else "thing"))


@register_check("FILM-02", level="W", build=1,
                title="Rhyme: the payoff shot's lens, angle, size or frame side differs from the plant shot's",
                plain="pays off a rhyme with a framing that differs from the shot that planted it")
def check_film_02(run):
    """For each PLANT with rhyme yes, the first shot that plants it (thing item `plant:`) against each shot that pays
    it off (thing item `payoff:`): lens, angle, size and the frame side of the thing. Also each MOTIF appearance
    written as a shot with `rhyme_with` a shot. A plant whose payoff shot is not written yet is left for later."""
    problems = []
    waiting = []
    for plant in run.records("PLANT"):
        rhyme_item = split_item(plant.get("rhyme") or "no")
        rhyme = rhyme_item.first or "no"
        if normalise_word(rhyme) != "yes":
            continue
        reversed_side = side_reversed_on_purpose(rhyme_item)
        planted = shots_linking(run, "plant", plant.identifier)
        paid = shots_linking(run, "payoff", plant.identifier)
        if not planted or not paid:
            waiting.append(plant.identifier)
            continue
        plant_shot, element = planted[0]
        for payoff_shot, _ in paid:
            if not run.in_scope(payoff_shot.identifier):
                continue
            differences = framing_differences(plant_shot, payoff_shot, element, reversed_side)
            if differences:
                problems.append(rhyme_line(run, plant_shot, payoff_shot, element, differences,
                                           f"plant {plant.identifier}", reversed_side))
    for motif in run.records("MOTIF"):
        for written in motif.get_all("appearance"):
            item = split_item(written)
            first, partner = (item.first or "").strip(), (item.get("rhyme_with") or "").strip()
            if not SHOT_NUMBER.search(first) or not SHOT_NUMBER.search(partner):
                continue
            later, earlier = run.record(first), run.record(partner)
            if later is None or earlier is None or later.type_name != "SHOT" or earlier.type_name != "SHOT":
                continue
            if not run.in_scope(later.identifier):
                continue
            reversed_side = side_reversed_on_purpose(item)
            differences = framing_differences(earlier, later, motif.identifier, reversed_side)
            if differences:
                problems.append(rhyme_line(run, earlier, later, motif.identifier, differences,
                                           f"motif {motif.identifier}'s appearance", reversed_side))
    if waiting:
        run.skip("FILM-02", f"{', '.join(waiting)}: the plant or payoff shot is not written yet, or is not in the excerpt")
    return problems


# ---------------------------------------------------------------- FILM-03 character camera rules

def shot_is_on(breakdown, shot, character):
    """True when the shot is about the character: its focus subject (focus_on, else the first person) is them."""
    subject = focus_subject(breakdown, shot)
    return subject is not None and element_of(subject.first) == character


NEVER_FIELDS = ("move", "angle", "size", "frame", "frame_detail", "focus", "mount", "stance")


def never_field(shot, written):
    """The shot's field that makes a choice a CAMRULE `never` item names ('push_in', 'low angle', 'dutch',
    'handheld'), or None."""
    wanted = normalise_word(written)
    if not wanted:
        return None
    for name in NEVER_FIELDS:
        value = normalise_word(shot.get(name) or "")
        if value and (value == wanted or (name == "angle" and f"{value}_angle" == wanted)):
            return name
    return None


@register_check("FILM-03", level="E", build=1,
                title="A character camera rule broken (closer than limit_before before closest; a never item used)",
                plain="breaks a character's camera rule: the camera comes closer than the rule allows, or makes a "
                      "choice the rule never makes for them")
def check_film_03(run):
    """For each CAMRULE, every shot about its character (the focus subject): no size on the ladder tighter than
    `closest` anywhere; none tighter than `limit_before` in a shot that ends before the `closest` story point; and
    none of the `never` items (camera move, angle, size, frame). Inserts are not on the ladder and are not sized
    against the rule."""
    breakdown = breakdown_of(run)
    problems = []
    shots = film_shots(run)
    for rule in run.records("CAMRULE"):
        character = (rule.get("character") or "").strip()
        if not character:
            continue
        limit = rule.get("limit_before")
        limit_rank = size_rank(limit)
        closest_item = split_item(rule.get("closest") or "", breakdown.definition("CAMRULE", "closest"))
        closest_size = closest_item.first if closest_item.first and not is_empty(closest_item.first) else None
        closest_rank = size_rank(closest_size)
        closest_at = closest_item.get("at")
        closest_position = story_point_position(breakdown, closest_at) if closest_at else None
        never = [piece for piece in split_list(rule.get("never") or "") if not is_empty(piece)]
        for shot in shots:
            if not run.in_scope(shot.identifier) or not shot_is_on(breakdown, shot, character):
                continue
            rank = size_rank(shot.get("size"))
            size_place = place_of(run, shot, "size")
            if rank is not None and closest_rank is not None and rank > closest_rank:
                problems.append(report(
                    run, "E", "FILM-03", shot, "size",
                    f"{shot.get('size')} on {character} is closer than {closest_size}, the closest camera rule "
                    f"{rule.identifier} ever allows",
                    f"Fix: take the shot back to {closest_size} or wider, or change the camera rule through a choice.",
                    size_place))
            elif rank is not None and limit_rank is not None and rank > limit_rank \
                    and ends_before(shot_position(breakdown, shot), closest_position) is True:
                problems.append(report(
                    run, "E", "FILM-03", shot, "size",
                    f"{shot.get('size')} on {character} is closer than {limit}, the limit camera rule "
                    f"{rule.identifier} sets before {closest_at}",
                    f"Fix: take the shot back to {limit} or wider, or move the closeness to the moment the rule "
                    "saves it for.", size_place))
            for written in never:
                field_name = never_field(shot, written)
                if field_name:
                    problems.append(report(
                        run, "E", "FILM-03", shot, field_name,
                        f"{shot.get(field_name)} on {character} is on the never list of camera rule {rule.identifier}",
                        f"Fix: choose another {field_name.replace('_', ' ')} for this shot, as the rule's in_control "
                        "or losing_control line says.", place_of(run, shot, field_name)))
    return problems


# ---------------------------------------------------------------- FILM-04 colour monotony

def sequences_in_order(run):
    """SEQUENCE records in film order (the first scene of each), else by ID."""
    sequences = [sequence for sequence in run.records("SEQUENCE") if sequence.identifier]

    def order(sequence):
        pairs = id_range_pairs(sequence.get("scenes"))
        return (scene_key(pairs[0][0]) if pairs else (10 ** 6, ""), sort_key_for_identifier(sequence.identifier))
    return sorted(sequences, key=order)


@register_check("FILM-04", level="W", build=1,
                title="Colour monotony: three consecutive sequences with the same frame value, saturation and "
                      "temperature",
                plain="repeats the same brightness, saturation and colour temperature across three groups of scenes "
                      "in a row")
def check_film_04(run):
    """VISUAL rows in the order of their sequences; colour_monotony_run adjacent sequences whose frame value,
    saturation and temperature are all the same give one warning, on the row that completes the run. A sequence with
    no VISUAL row breaks the run."""
    run_length = int(constant(run.constants, "colour_monotony_run", 3))
    visuals = {}
    for visual in run.records("VISUAL"):
        sequence = (visual.get("sequence") or "").strip()
        if sequence:
            visuals[sequence] = visual
    problems = []
    streak = []
    for sequence in sequences_in_order(run):
        visual = visuals.get(sequence.identifier)
        if visual is None:
            streak = []
            continue
        colour = (normalise_word(visual.get("frame_value") or ""), normalise_word(visual.get("saturation") or ""),
                  normalise_word(visual.get("temperature") or ""))
        if "" in colour:
            streak = []
            continue
        if streak and streak[-1][1] == colour:
            streak.append((visual, colour))
        else:
            streak = [(visual, colour)]
        if len(streak) == run_length:
            names = ", ".join(entry[0].get("sequence") for entry in streak)
            problems.append(report(
                run, "W", "FILM-04", visual, "frame_value",
                f"{colour[0]} with saturation {colour[1]} and temperature {colour[2]} repeats across "
                f"{run_length} groups of scenes in a row ({names})",
                "Fix: change one of these rows' frame value, saturation or temperature where the story changes "
                "(the colour script's progress or contrast), or give the plan's counterpoint.",
                place_of(run, visual, "frame_value")))
    return problems


# ---------------------------------------------------------------- FILM-05 stacking at a story peak (build 2)

@register_check("FILM-05", level="W", build=2,
                title="More than two components raised at one story peak (B3)",
                plain="raises more than two parts of the film (colour, contrast, size, hold, sound, camera) at "
                      "the same story peak")
def check_film_05(run):
    """PLAN peak items grouped by scene: the components (every peak but story and crisis_choice) that peak in one
    scene may number at most departments_changing_at_main_turn_max (B3 R7's two)."""
    plan = run.record("PLAN")
    if plan is None:
        return []
    most = int(constant(run.constants, "departments_changing_at_main_turn_max", 2))
    by_scene = {}
    for written in plan.get_all("peak"):
        item = split_item(written)
        component = normalise_word(item.first or "")
        scene_identifier = (item.get("scene") or "").strip()
        if not component or component in STORY_PEAKS or not scene_identifier:
            continue
        by_scene.setdefault(scene_identifier, []).append(component)
    problems = []
    for scene_identifier, components in sorted(by_scene.items(), key=lambda pair: scene_key(pair[0])):
        if len(components) > most:
            problems.append(report(
                run, "W", "FILM-05", plan, "peak",
                f"{scene_identifier} raises {len(components)} components at once ({', '.join(components)}); at most "
                f"{most} may peak at one story peak",
                "Fix: move the weaker components' peaks to another scene with a reason, so that at most "
                f"{most} rise together.", place_of(run, plan, "peak")))
    return problems


# ---------------------------------------------------------------- FILM-06 compliant sameness

@register_check("FILM-06", level="W", build=1,
                title="Three consecutive shots of the same subject from the same setup with the same size, angle and "
                      "a static camera and no why",
                plain="shows the same person three times in a row from the same camera, size and angle, with no "
                      "reason given")
def check_film_06(run):
    """Within a scene, consecutive shots (inserts, cards and black left out) about the same person from the same
    setup, at the same size and angle, with a static camera and no `why`: a run of compliant_sameness_run gives one
    warning on the shot that completes it. Matched singles alternate setups, so they never make a run."""
    breakdown = breakdown_of(run)
    run_length = int(constant(run.constants, "compliant_sameness_run", 3))
    problems = []
    streak = []
    previous_scene = None
    for shot in film_shots(run):
        scene_identifier = scene_of(shot.identifier)
        if scene_identifier != previous_scene:
            streak = []
            previous_scene = scene_identifier
        if is_insert_or_card(shot):
            streak = []
            continue
        subject = focus_subject(breakdown, shot)
        signature = (element_of(subject.first) if subject else None, (shot.get("setup") or "").strip(),
                     normalise_word(shot.get("size") or ""), normalise_word(shot.get("angle") or ""))
        static = normalise_word(shot.get("move") or "static") == "static"
        has_why = not is_empty(shot.get("why"))
        if not static or has_why or None in signature or "" in signature:
            streak = []
            continue
        if streak and streak[-1][1] == signature:
            streak.append((shot, signature))
        else:
            streak = [(shot, signature)]
        if len(streak) == run_length and run.in_scope(shot.identifier):
            names = ", ".join(entry[0].identifier for entry in streak)
            problems.append(report(
                run, "W", "FILM-06", shot, "setup",
                f"{signature[1]} repeats {signature[0]} at {signature[2]}, {signature[3]}, static, for {run_length} shots "
                f"in a row ({names}) with no why",
                "Fix: change the size, the setup or the angle where the beat changes, or give one of these shots a "
                "why that quotes the story.", place_of(run, shot, "setup")))
    return problems


# ---------------------------------------------------------------- FILM-07 relief after intensity (build 2)

@register_check("FILM-07", level="W", build=2,
                title="After a scene of intensity 8 or more, the next scene's target shot length is not longer",
                plain="follows a scene of high intensity with shots that are no longer on average")
def check_film_07(run):
    """Adjacent kept scenes in story order: after a scene of scene_intensity high_intensity_scene_min or more, the next
    scene's target_asl_s must be longer. It needs the whole film, so that adjacent records are adjacent scenes."""
    if needs_whole_film(run, "FILM-07"):
        return []
    least = number_of(constant(run.constants, "high_intensity_scene_min", 8), 8)
    scenes = film_scenes(run)
    problems = []
    for first, second in zip(scenes, scenes[1:]):
        intensity = number_of(first.get("scene_intensity"))
        before, after = number_of(first.get("target_asl_s")), number_of(second.get("target_asl_s"))
        if intensity is None or before is None or after is None or intensity < least:
            continue
        if after <= before and run.in_scope(second.identifier):
            problems.append(report(
                run, "W", "FILM-07", second, "target_asl_s",
                f"{number_words(after)} s is not longer than {first.identifier}'s {number_words(before)} s, though "
                f"{first.identifier} has scene intensity {number_words(intensity)}",
                f"Fix: give {second.identifier} a longer target average shot length, so the film breathes after "
                f"{first.identifier}.", place_of(run, second, "target_asl_s")))
    return problems


# ---------------------------------------------------------------- FILM-08 saved choices over the whole film

@dataclass
class Places:
    """Where a saved choice may be spent, read from its allowed_in text."""
    identifiers: set
    scenes: set
    turn: str = None          # 'main_turn' or 'turn' when only turn beats may spend it
    not_before: str = None    # 'the first in scene 13': nothing before that scene


def scene_identifier_from_number(number_text, digits=2):
    match = re.match(r"^(\d+)([A-Z]?)$", number_text.strip().upper())
    if not match:
        return None
    return f"SC{int(match.group(1)):0{digits}d}{match.group(2)}"


def read_places(text, digits=2):
    """Places from a RESERVE allowed_in: IDs (scenes, setups, beats, parts, shots), 'scene 29' words, 'main turns',
    'turns', and 'the first in scene 13' (read as: nothing before scene 13)."""
    text = text or ""
    not_before = None
    first = FIRST_IN.search(text)
    if first:
        not_before = scene_identifier_from_number(first.group(1), digits) if first.group(1) else first.group(2)
        text = text[:first.start()] + text[first.end():]
    identifiers = set(PLACE_IDENTIFIER.findall(text))
    scenes = {identifier for identifier in identifiers if SCENE_IDENTIFIER.match(identifier)}
    identifiers -= scenes
    for match in SCENE_IN_WORDS.finditer(text):
        found = scene_identifier_from_number(match.group(1), digits)
        if found:
            scenes.add(found)
    lowered = text.lower()
    turn = "main_turn" if re.search(r"\bmain turns?\b", lowered) else ("turn" if re.search(r"\bturns?\b", lowered) else None)
    return Places(identifiers, scenes, turn, not_before)


def turn_beats_of(run, record):
    """The turn words of the beats a shot (or a beat) names: {'main_turn', 'turn'}."""
    beats = [record.identifier] if record.type_name == "BEAT" else split_list(record.get("beats") or "")
    words = set()
    for identifier in beats:
        beat = run.record(identifier)
        if beat is not None and beat.type_name == "BEAT":
            words.add(normalise_word(beat.get("turn") or "none"))
    return words


def place_allows(run, places, record):
    """True when a use (a shot or a beat) lies in the saved choice's places."""
    scene_identifier = scene_of(record.identifier)
    if places.not_before and scene_key(scene_identifier) < scene_key(places.not_before):
        return False
    if places.turn == "main_turn" and "main_turn" not in turn_beats_of(run, record):
        return False
    if places.turn == "turn" and not ({"main_turn", "turn"} & turn_beats_of(run, record)):
        return False
    if not places.identifiers and not places.scenes:
        return True
    names = {record.identifier}
    if record.type_name == "SHOT":
        names.add((record.get("setup") or "").strip())
        names.update(split_list(record.get("beats") or ""))
    if names & places.identifiers:
        return True
    return any(same_scene(scene_identifier, scene) for scene in places.scenes)


def max_uses_of(reserve):
    """('number', n) | ('per_scene', 1) | ('share', fraction) | (None, None) from a RESERVE's max_uses."""
    item = split_item(reserve.get("max_uses") or "")
    first = normalise_word(item.first or "")
    if first in ("1_per_scene", "one_per_scene"):
        return "per_scene", 1
    if first == "share":
        fraction = number_of(item.get("fraction"))
        return ("share", fraction) if fraction is not None else (None, None)
    number = number_of(item.first)
    return ("number", int(number)) if number is not None else (None, None)


def film_scene_count(run):
    """How many scenes the film has: the whole story's scene count when known, else the kept SCENE records."""
    story = getattr(run, "story", None)
    count = story.scene_count() if story is not None else 0
    return max(count or 0, len(film_scenes(run)))


def over_count_lines(run, reserve, field_name, uses, allowed, what_counts):
    extra = uses[allowed:]
    problems = []
    listed = ", ".join(use.identifier for use in uses)
    for index, use in enumerate(extra, start=allowed + 1):
        if not run.in_scope(use.identifier):
            continue
        problems.append(report(
            run, "E", "FILM-08", use, field_name,
            f"{use.get(field_name)} is the {ordinal(index)} use of saved choice {reserve.identifier}, which allows "
            f"{allowed} {what_counts} ({listed})",
            f"Fix: go back to the camera system's default here, or spend saved choice {reserve.identifier} "
            "somewhere else through a choice.", place_of(run, use, field_name)))
    return problems


def film_level_default_lines(run, reserves):
    """The film-level extreme close-up and push-in budgets (extreme_close_up_film_max, push_in_scene_share_max) when
    no RESERVE record writes them."""
    matched = {reserve_match(reserve) for reserve in reserves}
    problems = []
    format_name = film_format(run)
    shots = film_shots(run)
    if ("size", "extreme_close_up") not in matched:
        most = by_format(constant(run.constants, "extreme_close_up_film_max", None), format_name)
        uses = [shot for shot in shots if normalise_word(shot.get("size") or "") == "extreme_close_up"
                and normalise_word(shot.get("kind") or "") != "insert"]
        if most is not None and len(uses) > int(most):
            listed = ", ".join(use.identifier for use in uses)
            for index, use in enumerate(uses[int(most):], start=int(most) + 1):
                if run.in_scope(use.identifier):
                    problems.append(report(
                        run, "E", "FILM-08", use, "size",
                        f"extreme_close_up is the {ordinal(index)} extreme close-up of the film; a {format_name} allows "
                        f"{int(most)} ({listed})",
                        "Fix: take this shot back to close_up, or write the film-level saved choice for extreme "
                        "close-ups in the film rules and spend it where the story peaks.",
                        place_of(run, use, "size")))
    if ("move", "push_in") not in matched:
        share = constant(run.constants, "push_in_scene_share_max", None)
        scenes = []
        for shot in shots:
            if normalise_word(shot.get("move") or "") == "push_in" and scene_of(shot.identifier) not in scenes:
                scenes.append(scene_of(shot.identifier))
        total = film_scene_count(run)
        if share is not None and total and len(scenes) > share * total:
            allowed = int(math.floor(share * total + 1e-9))
            for scene_identifier in scenes[allowed:]:
                use = next(shot for shot in shots if scene_of(shot.identifier) == scene_identifier
                           and normalise_word(shot.get("move") or "") == "push_in")
                if run.in_scope(use.identifier):
                    problems.append(report(
                        run, "E", "FILM-08", use, "move",
                        f"push_in makes {len(scenes)} scenes with a push-in out of {total}; the film allows push-ins "
                        f"in at most {number_words(share)} of its scenes ({allowed})",
                        "Fix: make this camera move static, or write the film-level saved choice for push-ins in the "
                        "film rules and spend it where the story turns inside a person.",
                        place_of(run, use, "move")))
    return problems


@register_check("FILM-08", level="E", build=1,
                title="Film-wide saved-choice counts and places, including the film-level extreme close-up and "
                      "push-in reserves",
                plain="spends a saved choice more often than the film allows, or in a place the film rules do not "
                      "allow")
def check_film_08(run):
    """Each RESERVE whose match is '<field> = <value>' is counted over the whole film: shots (or beats, for a beat
    field such as pause_after) whose field has that value. max_uses is a number, 1_per_scene, or 'share | fraction:'
    (scenes spending it, against the film's scene count). allowed_in is read for IDs, 'scene N', 'main turns' or
    'turns', and 'the first in scene N'; never_on names people the choice is never spent on (the shot's focus
    subject). With no RESERVE for them, the constants extreme_close_up_film_max and push_in_scene_share_max are the
    film-level budgets."""
    breakdown = breakdown_of(run)
    project = run.project_record
    digits = int(number_of(project.get("scene_id_digits"), 2)) if project is not None else 2
    reserves = run.records("RESERVE")
    problems = []
    manual = []
    for reserve in reserves:
        matched = reserve_match(reserve)
        uses = reserve_uses(run, reserve)
        if matched is None or uses is None:
            manual.append(reserve.identifier)
            continue
        field_name, value = matched
        kind, amount = max_uses_of(reserve)
        if kind == "number":
            if len(uses) > amount:
                problems += over_count_lines(run, reserve, field_name, uses, amount, "uses" if amount != 1 else "use")
        elif kind == "per_scene":
            seen = {}
            for use in uses:
                scene_identifier = scene_of(use.identifier)
                seen[scene_identifier] = seen.get(scene_identifier, 0) + 1
                if seen[scene_identifier] > 1 and run.in_scope(use.identifier):
                    problems.append(report(
                        run, "E", "FILM-08", use, field_name,
                        f"{use.get(field_name)} is the {ordinal(seen[scene_identifier])} use of saved choice "
                        f"{reserve.identifier} in {scene_identifier}, which allows one a scene",
                        f"Fix: keep one use of saved choice {reserve.identifier} in {scene_identifier} and go back to "
                        "the default in the others.", place_of(run, use, field_name)))
        elif kind == "share":
            total = film_scene_count(run)
            scenes = []
            for use in uses:
                if scene_of(use.identifier) not in scenes:
                    scenes.append(scene_of(use.identifier))
            allowed = int(math.floor(amount * total + 1e-9)) if total else None
            if allowed is not None and len(scenes) > allowed:
                for scene_identifier in scenes[allowed:]:
                    use = next(use for use in uses if scene_of(use.identifier) == scene_identifier)
                    if run.in_scope(use.identifier):
                        problems.append(report(
                            run, "E", "FILM-08", use, field_name,
                            f"{use.get(field_name)} makes {len(scenes)} scenes spending saved choice "
                            f"{reserve.identifier} out of {total}; it allows {number_words(amount)} of the scenes "
                            f"({allowed})",
                            f"Fix: go back to the default here, or spend saved choice {reserve.identifier} in fewer "
                            "scenes through a choice.", place_of(run, use, field_name)))
        places = read_places(reserve.get("allowed_in"), digits)
        never_on = [piece for piece in split_list(reserve.get("never_on") or "") if not is_empty(piece)]
        for use in uses:
            if not run.in_scope(use.identifier):
                continue
            if not place_allows(run, places, use):
                problems.append(report(
                    run, "E", "FILM-08", use, field_name,
                    f"{use.get(field_name)} spends saved choice {reserve.identifier} outside its places "
                    f"({reserve.get('allowed_in')})",
                    f"Fix: spend it only where saved choice {reserve.identifier} allows, or go back to the default "
                    "here.", place_of(run, use, field_name)))
            if use.type_name == "SHOT" and never_on:
                subject = focus_subject(breakdown, use)
                person = element_of(subject.first) if subject else None
                if person in never_on:
                    problems.append(report(
                        run, "E", "FILM-08", use, field_name,
                        f"{use.get(field_name)} spends saved choice {reserve.identifier} on {person}, whom it is never "
                        "spent on",
                        f"Fix: frame {person} another way here; saved choice {reserve.identifier} is never theirs.",
                        place_of(run, use, field_name)))
    if manual:
        run.skip("FILM-08", f"{', '.join(manual)}: matched by hand (match: manual), so its uses are not counted")
    problems += film_level_default_lines(run, reserves)
    return problems


# ---------------------------------------------------------------- FILM-09 heavy-handedness counts (build 2)

def plants_in(shot):
    return [split_item(written).get("plant") for written in shot.get_all("thing")
            if split_item(written).get("plant")]


def beat_flags(run, beat_identifier):
    beat = run.record(beat_identifier)
    if beat is None or beat.type_name != "BEAT":
        return set()
    return {normalise_word(split_item(written).first or "") for written in beat.get_all("flag")}


@register_check("FILM-09", level="W", build=2,
                title="Heavy-handedness counts: more than two plant inserts in a scene; music under a beat with an "
                      "unsaid; a light cue on the line that states the point",
                plain="points too hard at its meaning: too many inserts of planted things, music under what is left "
                      "unsaid, or a light change on the line that says the point")
def check_film_09(run):
    """Three counts (steps/09's heavy-handedness questions that code can count): inserts carrying a `plant:` thing
    item, more than plant_inserts_per_scene_max in a scene; a shot with music on a beat that has an `unsaid`; a light
    cue (LOOK light_cue resolved to a beat, or a shot's light_cue) on a beat flagged on_the_nose, the line that states
    the point."""
    breakdown = breakdown_of(run)
    most = int(constant(run.constants, "plant_inserts_per_scene_max", 2))
    problems = []
    inserts = {}
    for shot in film_shots(run):
        if normalise_word(shot.get("size") or "") == "insert" or normalise_word(shot.get("kind") or "") == "insert":
            if plants_in(shot):
                inserts.setdefault(scene_of(shot.identifier), []).append(shot)
    for scene_identifier, shots in inserts.items():
        if len(shots) > most and run.in_scope(shots[most].identifier):
            listed = ", ".join(shot.identifier for shot in shots)
            problems.append(report(
                run, "W", "FILM-09", shots[most], "thing",
                f"makes {len(shots)} inserts of planted things in {scene_identifier} ({listed}); at most {most} a scene",
                "Fix: plant the thing inside a wider frame instead of cutting to it, at emphasis 1.",
                place_of(run, shots[most], "thing")))
    for shot in film_shots(run):
        if not run.in_scope(shot.identifier) or is_empty(shot.get("music")):
            continue
        for beat_identifier in split_list(shot.get("beats") or ""):
            beat = run.record(beat_identifier)
            if beat is not None and beat.get_all("unsaid"):
                problems.append(report(
                    run, "W", "FILM-09", shot, "music",
                    f"{shot.get('music')} plays under {beat_identifier}, whose meaning is left unsaid",
                    "Fix: set music to none here and let the carrier of the unsaid do the work.",
                    place_of(run, shot, "music")))
                break
    for look in run.records("LOOK"):
        for written in look.get_all("light_cue"):
            item = split_item(written)
            point = story_point_position(breakdown, item.first) if item.first else None
            parsed = parse_story_point(item.first or "")
            if point is None or parsed is None:
                continue
            beat_identifier = parsed[2] or resolve_story_point(breakdown, item.first).beat
            if beat_identifier and "on_the_nose" in beat_flags(run, beat_identifier) and run.in_scope(beat_identifier):
                problems.append(report(
                    run, "W", "FILM-09", look, "light_cue",
                    f"{item.first} changes the light on {beat_identifier}, a line flagged on_the_nose that states the point",
                    "Fix: move the light change off the line that states the point, or drop it.",
                    place_of(run, look, "light_cue", item.first)))
    for shot in film_shots(run):
        if not run.in_scope(shot.identifier) or is_empty(shot.get("light_cue")):
            continue
        flagged = [beat for beat in split_list(shot.get("beats") or "") if "on_the_nose" in beat_flags(run, beat)]
        if flagged:
            problems.append(report(
                run, "W", "FILM-09", shot, "light_cue",
                f"changes the light on {flagged[0]}, a line flagged on_the_nose that states the point",
                "Fix: move the light change off the line that states the point, or drop it.",
                place_of(run, shot, "light_cue")))
    return problems


# ---------------------------------------------------------------- FILM-10 motif counts, FILM-11 loud sets

def count_lines(run, check_id, records, most, field_name, what_counts, fix):
    problems = []
    records = sorted(records, key=lambda record: sort_key_for_identifier(record.identifier))
    if most is None or len(records) <= int(most):
        return problems
    listed = ", ".join(record.identifier for record in records)
    for record in records[int(most):]:
        problems.append(report(
            run, "W", check_id, record, field_name,
            f"{record.get(field_name)} makes {len(records)} {what_counts}; the film allows {int(most)} ({listed})",
            fix, place_of(run, record, field_name)))
    return problems


@register_check("FILM-10", level="W", build=1,
                title="Motif counts over motif_spines_max, sound_motif_max or body_motif_max",
                plain="carries more returning motifs of one kind than a film of its length can hold")
def check_film_10(run):
    """MOTIF records: visual spines (rank spine, channel visual) at most the upper end of motif_spines_max for the
    film's format; sound motifs (channel sound) at most sound_motif_max; body motifs (channel body) at most
    body_motif_max (B4 rule 7). The motifs over the count are reported."""
    format_name = film_format(run)
    motifs = run.records("MOTIF")
    spines = [motif for motif in motifs if normalise_word(motif.get("rank") or "") == "spine"
              and normalise_word(motif.get("channel") or "visual") == "visual"]
    sounds = [motif for motif in motifs if normalise_word(motif.get("channel") or "") == "sound"]
    bodies = [motif for motif in motifs if normalise_word(motif.get("channel") or "") == "body"]
    problems = []
    problems += count_lines(run, "FILM-10", spines,
                            upper_bound(by_format(constant(run.constants, "motif_spines_max", None), format_name)),
                            "rank", f"visual spine motifs in a {format_name}",
                            "Fix: make this motif supporting or minor, or fold it into a spine that carries the same "
                            "meaning.")
    problems += count_lines(run, "FILM-10", sounds, constant(run.constants, "sound_motif_max", None), "channel",
                            "sound motifs", "Fix: keep one sound motif and make this one a sound effect of its scene.")
    problems += count_lines(run, "FILM-10", bodies, constant(run.constants, "body_motif_max", None), "channel",
                            "body motifs", "Fix: keep one body motif and make this one a gesture of its scene.")
    return problems


@register_check("FILM-11", level="W", build=1,
                title="More loud sets than loud_sets_max",
                plain="has more loud places than a film of its length can hold")
def check_film_11(run):
    """LOCATION records with loudness loud, at most loud_sets_max for the film's format (B4); the ones over are
    reported."""
    format_name = film_format(run)
    loud = [place for place in run.records("LOCATION") if normalise_word(place.get("loudness") or "") == "loud"]
    return count_lines(run, "FILM-11", loud, by_format(constant(run.constants, "loud_sets_max", None), format_name),
                       "loudness", f"loud places in a {format_name}",
                       "Fix: make this place quiet (plain, lived-in dressing), keeping loudness for the sets the story "
                       "needs most.")


# ---------------------------------------------------------------- FILM-12 tone

def tone_range_of(run):
    plan = run.record("PLAN")
    project = run.project_record
    for record in (plan, project):
        if record is not None and not is_empty(record.get("tone_range")):
            home = normalise_word(record.get("tone_home") or "")
            tones = {normalise_word(piece) for piece in split_list(record.get("tone_range"))}
            return record, tones | ({home} if home else set())
    return None, None


@register_check("FILM-12", level="W", build=1,
                title="A scene's tone outside PLAN tone_range, or over a third of scenes with an undercurrent",
                plain="is played in a tone outside the film's range; this is for you to decide, never fixed without "
                      "asking")
def check_film_12(run):
    """Each kept scene's tone must be the home tone or in PLAN tone_range (else PROJECT's); over
    undercurrent_scene_share_max of the film's kept scenes with a tone_undercurrent is flagged on the plan (D10 TN6),
    which needs the whole film. Both are flagged for the user and never fixed (D10 TN7)."""
    record, tones = tone_range_of(run)
    problems = []
    if tones:
        for scene in film_scenes(run):
            tone = normalise_word(scene.get("tone") or "")
            if tone and tone not in EMPTY_WORDS and tone not in tones and run.in_scope(scene.identifier):
                problems.append(report(
                    run, "W", "FILM-12", scene, "tone",
                    f"{tone} is outside the film's tone range ({', '.join(sorted(tones))})",
                    "Fix: ask the user whether to keep this tone (then add it to the range with a reason) or play the "
                    "scene in a tone of the range; never change it without asking.", place_of(run, scene, "tone")))
    if needs_whole_film(run, "FILM-12"):
        return problems
    scenes = film_scenes(run)
    with_undercurrent = [scene for scene in scenes if not is_empty(scene.get("tone_undercurrent"))]
    share = constant(run.constants, "undercurrent_scene_share_max", None)
    if scenes and share is not None and len(with_undercurrent) / len(scenes) > share:
        plan = run.record("PLAN") or record
        if plan is not None:
            problems.append(report(
                run, "W", "FILM-12", plan, "tone_home",
                f"{len(with_undercurrent)} of {len(scenes)} scenes carry an undercurrent, over a third of the film",
                "Fix: ask the user whether the home tone is right (the undercurrent may be the film's real tone), or "
                "keep undercurrents for the scenes that need them most.", place_of(run, plan, "tone_home")))
    return problems


# ---------------------------------------------------------------- check --film: the strip and 12 Whole-film check

def finding_problems(result):
    """The problems a film run writes as findings: every FILM line and TIME-07 (step 9's list), errors and warnings."""
    found = []
    for problem in result.problems:
        check_id = getattr(problem, "check_id", "")
        if (check_id.startswith("FILM-") or check_id == "TIME-07") and getattr(problem, "level", "") in ("E", "W"):
            found.append(problem)
    return found


def one_line(text):
    """A value that fits one field line: no ' | ' (G5), no line breaks, and single quotes for double (G12: double
    quotes in a value are story quotations, and a checker's evidence quotes records, not the story)."""
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    text = text.replace(" | ", " / ").replace('"', "'").replace("“", "'").replace("”", "'")
    return text or "none"


OLD_PEAK_WORDING = "reason: ...' quoting why the story peaks here."
NEW_PEAK_WORDING = "reason: <why>', the why quoting the line where the story peaks."


def refresh_code_text(record, fields):
    """Write code's own fields of an existing checker finding afresh, keeping the record's place and other lines."""
    for name, value in fields:
        if (record.get(name) or "") != value:
            record.set_field(name, value)


def all_finding_numbers(run):
    numbers = []
    for (type_name, identifier) in run.index:
        if type_name == "FINDING" and identifier:
            match = FINDING_NUMBER.match(identifier)
            if match:
                numbers.append(int(match.group(1)))
    return numbers


def whole_film_plain_part(run, problems, findings_counts, again, strip_facts, stamp):
    """The plain part of 12 Whole-film check.md: code's audit report, in plain words (no IDs or codes, WORDS-04)."""
    from .check_records import plain_problem_lines, plural
    errors = [problem for problem in problems if problem.level == "E"]
    warnings = [problem for problem in problems if problem.level == "W"]
    open_count = findings_counts.get("open", 0)
    found = "nothing to fix" if not errors else f"{plural(len(errors), 'thing')} to fix"
    found += " and no warnings" if not warnings else f" and {plural(len(warnings), 'warning')}"
    still = "no finding is open" if not open_count else \
        f"{plural(open_count, 'finding')} {'is' if open_count == 1 else 'are'} open"
    lines = [f"In short: the film pass found {found}; {still}.", "", f"# {WHOLE_FILM_TITLE}", "", "## At a glance", ""]
    shots, scenes = strip_facts[0], strip_facts[1]
    lines.append(f"Checked the film as one structure on {stamp.day} {stamp.strftime('%B %Y')} at "
                 f"{stamp.strftime('%H:%M')}: {plural(shots, 'shot')} in {plural(scenes, 'scene')}, one line each in the "
                 "film strip.")
    if run.scope_scenes is not None:
        in_scope = len([scene for scene in run.scope_scenes if SCENE_IDENTIFIER.match(scene)])
        lines.append(f"Scope: {in_scope} of {film_scene_count(run)} scenes, so the checks that need every scene of "
                     "the film waited.")
    elif partial_film(run):
        lines.append("Only an excerpt of the story is here, so the checks that need every scene of the film waited.")
    lines += ["", "## What the checker found", ""]
    if errors or warnings:
        lines += plain_problem_lines(errors + warnings, run)
    else:
        lines.append("Nothing: the ladder, the rhymes, the camera rules, the colour plan, the saved choices, the "
                     "motifs, the loud places and the tones hold.")
    lines += ["", "## Findings", ""]
    total = sum(findings_counts.values())
    lines.append(f"{plural(total, 'finding')} below the line: {findings_counts.get('open', 0)} open, "
                 f"{findings_counts.get('fixed', 0)} fixed, {findings_counts.get('accepted', 0)} accepted. Each names "
                 "the record, the rule, what shows the problem and the fix; the film pass questions add their own.")
    if again:
        lines.append(f"Found again although marked fixed: {plural(len(again), 'finding')}; look at "
                     f"{'it' if len(again) == 1 else 'them'} again.")
    lines.append("")
    return lines


def write_whole_film_check(project, run, problems, strip_facts):
    """Write 12 Whole-film check.md: a new plain part; the FINDING records kept; one new FINDING (source: checker)
    for each problem not yet written (same record and rule). Returns (new findings, findings found again although
    marked fixed, the counts by status)."""
    from .project_files import history_run_folder, keep_in_history
    path = project.folder / WHOLE_FILM_FILE
    schema = run.schema
    if path.is_file():
        record_file = parse_file(path, WHOLE_FILM_FILE, schema)
        old_text = path.read_text(encoding="utf-8")
    else:
        from .record_format import RecordFile
        record_file = RecordFile(name=WHOLE_FILM_FILE)
        old_text = None
    kept = [segment for segment in record_file.segments if isinstance(segment, (Record, EndLine))]
    written = {}
    for record in [segment for segment in kept if isinstance(segment, Record)]:
        if record.type_name == "FINDING" and normalise_word(record.get("source") or "") == "checker":
            written[((record.get("record") or "").strip(), (record.get("rule") or "").strip())] = record
    for record in written.values():
        # a wording the checker wrote before it stopped writing "..." (FORM-08 no longer judges code's text, but
        # the old text is written afresh so the record reads whole)
        for name in ("evidence", "fix"):
            value = record.get(name) or ""
            if OLD_PEAK_WORDING in value:
                record.set_field(name, value.replace(OLD_PEAK_WORDING, NEW_PEAK_WORDING))
    numbers = all_finding_numbers(run)
    next_number = (max(numbers) if numbers else 0) + 1
    new_records = []
    again = []
    for problem in problems:
        key = (problem.record, problem.check_id)
        fix = re.sub(r"^(Fix|Allowed):\s*", "", getattr(problem, "fix", "") or "").strip()
        evidence = one_line(f"{problem.field_name} {problem.what}" if problem.field_name else problem.what)
        if key in written:
            if normalise_word(written[key].get("status") or "") == "fixed":
                again.append(written[key].identifier)
            # the evidence and the fix are code's text (code_state): a check run again writes them afresh, so a
            # wording the checker has since changed never stays behind in the record
            refresh_code_text(written[key], (("evidence", evidence), ("fix", one_line(fix))))
            continue
        record = make_record("FINDING", f"FIND-{next_number:03d}", title=one_line(
            f"{problem.check_id} on {problem.record}")[:60], fields=[
            ("record", problem.record), ("rule", problem.check_id),
            ("evidence", evidence), ("fix", one_line(fix)), ("source", "checker"), ("status", "open"), ("reason", "none"),
            ("locked", "no")], file_name=WHOLE_FILM_FILE)
        written[key] = record
        new_records.append(record)
        next_number += 1
    end_lines = [segment for segment in kept if isinstance(segment, EndLine)]
    records = [segment for segment in kept if isinstance(segment, Record)] + new_records
    counts = {"open": 0, "fixed": 0, "accepted": 0}
    for record in records:
        if record.type_name == "FINDING":
            status = normalise_word(record.get("status") or "open")
            counts[status] = counts.get(status, 0) + 1
    stamp = datetime.datetime.now()
    plain = whole_film_plain_part(run, problems, counts, again, strip_facts, stamp)
    block = TextBlock()
    for line in plain + [DIVIDER_LINE, ""]:
        block.lines.append(line)
        block.line_numbers.append(None)
    segments = [block]
    for record in records:
        segments.append(record)
    end_line = end_lines[-1] if end_lines else EndLine(raw=None, what=WHOLE_FILM_TITLE, count=0, changed=True)
    if end_line.count != len(records):
        end_line.changed = True
    segments.append(end_line)
    record_file.segments = segments
    if old_text is not None:
        keep_in_history(history_run_folder(project), path, WHOLE_FILM_FILE)
    write_file(record_file, path, schema)
    if new_records:
        project.add_log_entry(f"Film pass: wrote {len(new_records)} new "
                              f"{'finding' if len(new_records) == 1 else 'findings'} in 12 Whole-film check.")
    return new_records, again, counts


def film_pass_report_section(project, result):
    """Report section for 13 Health check (check_records.register_report_section). On a film run (--film or
    --step 9) with a project, it writes the film strip and 12 Whole-film check.md, then returns the plain lines of
    the section "The whole film". On any other run it writes nothing and returns []."""
    run = getattr(result, "run", None)
    if project is None or run is None or not (getattr(run, "film", False) or getattr(run, "step", None) == 9):
        return []
    folder = getattr(project, "folder", None)
    if folder is None:
        return []
    lines = ["## The whole film", ""]
    try:
        strip_facts = write_film_strip(run, folder)
        new_records, again, counts = write_whole_film_check(project, run, finding_problems(result), strip_facts)
    except Exception as error:  # the report must still be written; say plainly what failed
        return lines + [f"The film strip or the whole-film check could not be written ({type(error).__name__}); "
                        "report this line.", ""]
    shots, scenes, _, files = strip_facts
    lines.append(f"The film strip lists {shots} {'shot' if shots == 1 else 'shots'} in {scenes} "
                 f"{'scene' if scenes == 1 else 'scenes'}" + (f", in {len(files) - 1} parts by act" if len(files) > 1 else "")
                 + ".")
    if new_records:
        lines.append(f"The film pass wrote {len(new_records)} new {'finding' if len(new_records) == 1 else 'findings'} "
                     "in 12 Whole-film check.")
    else:
        lines.append("The film pass found nothing new for 12 Whole-film check.")
    if counts.get("open"):
        lines.append(f"{counts['open']} {'finding is' if counts['open'] == 1 else 'findings are'} open there: each is "
                     "fixed, or accepted with a reason, before the film pass is done.")
    if again:
        lines.append(f"{len(again)} {'finding' if len(again) == 1 else 'findings'} marked fixed "
                     f"{'was' if len(again) == 1 else 'were'} found again.")
    lines.append("")
    return lines


register_report_section(film_pass_report_section)
