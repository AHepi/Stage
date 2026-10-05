"""checks_coverage_time_state.py: the COVER, TIME and STATE checks of blueprint section 7.2.

In plain words:
- COVER-01 to COVER-08 check that nothing the story writes is lost on the way to the screen: every story line of a
  scene is in a beat and in a shot (a list item before step 8 and at Quick depth), every speech is heard, every
  beat is shown, every key event stays in a scene the film keeps, every scene is in exactly one group of scenes,
  every sound the story writes in capitals is carried by an effect, the room sound or a motif, and every light,
  colour or darkness line the story writes is carried by a light cue, what stays dark, a shot's light or (for the
  colour of a thing, B2 P2) a description that keeps that colour;
- TIME-01 to TIME-10 check time: each shot at least as long as its time floor (worked out by derive_fields.py);
  timed moments inside the shot and never overlapping; each scene's total near its target; at most the allowed
  long pauses a scene; the reaction a turn owes; not more main actions than a shot's length allows; the film's
  average shot length for its home tone; pause lengths inside their tier, and a hold only with a saved choice;
  longer holds on the person who does not know, in a suspense scene; the main turn's shot the longest or the
  shortest of its scene;
- STATE-01 to STATE-04 check continuity: every person and thing in a shot is named in the state valid at that
  point of the story; every state has a cause line found in the story; a scene that runs straight on from the
  one before starts everyone in the state they left it in, unless a cause says otherwise.

Each check is registered with check_records.register_check (see the note at the top of check_records.py), reads
the records and the story through the CheckRun, takes derived values (time floors, lines of a record, states)
from derive_fields.py, and never changes a record. Every problem line has 7.2's form: level, check ID, record,
field, what is wrong, then the fix.

Readings of 7.2 that the blueprint leaves open are written next to each check and in the WP4c build log. Numbers
come from rules/constants.json by name (pause_tiers, long_pauses_per_scene_max, turn_reaction_min_s,
scene_total_tolerance, main_actions_per_seconds, film_asl_range_s) and rules/tone_defaults.json.

Standard library only.

After the full run on The Catch (Project notes 31 and 32):
- COVER-08: the look covers a light at rest; a light that changes or moves still needs a light cue;
- TIME-01 counts text the audience must read and owes a beat's pause once; TIME-03 measures the shots against the
  list (scene_total_tolerance) and warns a list far from its planned length (scene_target_far_ratio);
- TIME-09 prints one line per character and leaves out a silent non-human character; STATE-01 reads a recording's
  state where it was recorded.

After the three-scene test of the fixed kit (Project notes 35 and 36):
- footage recorded in a scene may show any state that held during that scene.

After the second three-scene test (Project notes 37 and 38):
- TIME-09's fix says to report a fact whose known_by is wrong, since the shots cannot correct it.
"""

import math
import re
from dataclasses import dataclass

from .check_records import register_check, same_scene, scene_of
from .derive_fields import (breakdown_for_run, constant, element_of, elements_present, focus_subject,
                            light_words_in_context, LIGHT_BRIGHTNESS_WORDS, LIGHT_CHANGE_WORDS, LIGHT_MOVING_WORDS,
                            light_moves_in,
                            is_insert_or_card, list_items, number_of, provisional_floor, resolve_story_point,
                            seconds_text, state_from, states_in_play, time_floor)
from .record_format import (load_json, normalise_word, parse_line_numbers, parse_quote_anchor, parse_story_point,
                            sort_key_for_identifier, split_item, split_list)

# Seconds are compared as written: a screen time of 13.8 against a floor of 13.8 is not under it.
TIME_TOLERANCE_S = 0.001
SCENE_IDENTIFIER = re.compile(r"^SC(\d{2,3})([A-Z]?)$")
SCENE_OR_BEAT_IN_TEXT = re.compile(r"\bSC\d{2,3}[A-Z]?(?:-B\d{2,3})?\b")
STATE_REFERENCE = re.compile(r"^(?:CH|PR|LOC)-[A-Z0-9]+(?:-[A-Z0-9]+)*\.S\d{2}$")
ELEMENT_REFERENCE = re.compile(r"^(?:CH|PR|LOC)-[A-Z0-9]+(?:-[A-Z0-9]+)*$")
BEAT_NUMBER = re.compile(r"-B(\d{2,3})$")
SPAN = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*[-–]\s*(-?\d+(?:\.\d+)?)\s*$")
RESERVE_MATCH = re.compile(r"^\s*([a-z_]+)\s*=\s*([a-z0-9_.]+)\s*$")
# Story lines that coverage does not ask for (7.2: "blank lines and the heading excluded"); the other kinds of
# heading, and a script's notes and hidden text, are not story either (read_story's line types).
NOT_STORY_LINE_TYPES = {"blank", "heading", "chapter_heading", "other_heading", "note", "boneyard", "section",
                        "synopsis", "page_break", "title", "front_matter"}
# SCENE keep values that take a scene out of the film (5.5); merge and fold hand its content to merged_into.
NOT_KEPT = ("cut", "merge", "fold")
# B2 P2 sorts the light words read_story finds: a darkness word means something stays dark; a colour word names a
# thing's colour, which "holds under every light", so a description that keeps the colour carries it; every
# other light word (a source, a brightness, a change) needs a light cue or a shot's light. Judgement, from B2 P2.
DARKNESS_WORDS = {"dark", "darker", "darkness", "shadow", "shadows", "gloom", "black", "unlit"}
COLOUR_WORDS = {"red", "green", "blue", "yellow", "orange", "white", "black", "grey", "gray", "gold", "golden",
                "silver", "amber", "purple", "violet", "pink", "brown", "pale"}
# Word endings taken off a sound word before it is looked for in the records ("TICKS" is found in "ticking").
SOUND_WORD_ENDINGS = ("ing", "es", "ed", "s")
SOUND_STEM_LENGTH_MIN = 3
# The LOOK fields whose words can keep a thing's colour (COVER-08).
LOOK_COLOUR_FIELDS = ("look_block", "palette", "accent_allowed", "main_light", "neutral_white", "stays_dark")


# ---------------------------------------------------------------- shared helpers

def breakdown_of(run):
    """The run's Breakdown (derived fields), made once per run by derive_fields and kept in run.cache."""
    return breakdown_for_run(run)


def seconds_words(value):
    """A number of seconds as the records write it: 12, 13.8, 2.5."""
    if value is None:
        return "?"
    if float(value).is_integer():
        return str(int(value))
    return seconds_text(value)


def scene_key(identifier):
    """Story order of a scene ID: SC06 before SC06A before SC07."""
    match = SCENE_IDENTIFIER.match(identifier or "")
    if not match:
        return (10 ** 6, "")
    return (int(match.group(1)), match.group(2))


def beat_order_number(identifier):
    match = BEAT_NUMBER.search(identifier or "")
    return int(match.group(1)) if match else None


def is_kept(scene):
    return normalise_word(scene.get("keep") or "keep") not in NOT_KEPT


def kept_scenes(run):
    """The scenes whose problems this run reports (scope and --scene), leaving out omitted and cut scenes."""
    scenes = [scene for scene in run.records("SCENE") if scene.identifier and is_kept(scene)
              and run.scene_checked(scene.identifier)]
    return sorted(scenes, key=lambda scene: scene_key(scene.identifier))


def place_of(run, record, field_name, first_part=None):
    """(file name, line number) of a record's field line (the item whose first part matches, when one is given);
    (None, None) when the field is not written, so the problem sits on the record's heading."""
    if record is None or not hasattr(record, "key"):
        return None, None
    found = run.field_lines(record.key, field_name)
    for record_file, _, line in found:
        if first_part is not None and (split_item(line.value).first or "").strip() != first_part:
            continue
        return record_file.name, line.line_number
    return None, None


def scene_file_place(run, scene_identifier):
    """(file name, line number) of a scene's heading in its scene file (11 Scenes/...), else its first copy."""
    scene = run.record(scene_identifier)
    if scene is None:
        return None, None
    copies = run.copies(scene.key)
    for record_file, copy in copies:
        if record_file.name.startswith("11 Scenes/"):
            return record_file.name, copy.heading_line_number
    if copies:
        return copies[0][0].name, copies[0][1].heading_line_number
    return None, None


def report(run, level, check_id, record, field_name, what, fix, place=(None, None)):
    """One problem line of 7.2's form, placed at the given (file, line) when known."""
    file_name, line_number = place
    return run.problem(level, check_id, record, field_name, what, fix, line_number=line_number, file_name=file_name)


def numbers_text(numbers):
    """(first, last) pairs of line numbers as words: '413-414, 420'."""
    return ", ".join(f"{first}-{last}" if first != last else str(first) for first, last in numbers)


def story_line_groups(wanted, counted):
    """The wanted story lines grouped into runs that no counted, unwanted line interrupts (blank lines between two
    wanted lines do not break a run)."""
    groups = []
    current = None
    for number in counted:
        if number in wanted:
            if current is None:
                current = [number, number]
            else:
                current[1] = number
        elif current is not None:
            groups.append(tuple(current))
            current = None
    if current is not None:
        groups.append(tuple(current))
    return groups


def is_story_line(numbered, number):
    """True for a line coverage asks for: not blank, not a heading, not a note."""
    if not numbered.line(number).strip():
        return False
    return (numbered.type_of(number) or "") not in NOT_STORY_LINE_TYPES


def first_words(numbered, number, count=7):
    """The start of a story line for a problem line; a cue line gives its name and the first words of its speech
    ("JUDE: They didn't let me watch.")."""
    text = numbered.line(number).strip()
    if (numbered.type_of(number) or "").startswith("cue") or text.startswith("@"):
        name = text.lstrip("@").strip()
        spoken = []
        following = number + 1
        while following <= numbered.last and numbered.line(following).strip() \
                and (numbered.type_of(following) or "") in ("dialogue", "parenthetical", "lyric"):
            if (numbered.type_of(following) or "") != "parenthetical":
                spoken.append(numbered.line(following).strip())
            following += 1
        text = f"{name}: {' '.join(spoken)}" if spoken else name
    words = text.split()
    return " ".join(words[:count]) + (" ..." if len(words) > count else "")


def sentence_holding(text, words):
    """The sentence of a story line that holds one of the words (for a story point the AI can copy), else None."""
    for sentence in re.split(r"(?<=[.!?])\s+", (text or "").strip()):
        found = {word.lower() for word in re.findall(r"[A-Za-z]+", sentence)}
        if found & set(words) and len(sentence.split()) >= 3:
            return sentence.strip()
    return None


def scene_span(run, breakdown, scene_identifier, check_id):
    """(first, last) story lines of a scene when the story holds them; otherwise a skip line and None."""
    if run.story_missing(check_id):
        return None
    span = run.scene_range(scene_identifier) or breakdown.scene_range(scene_identifier)
    if span is None:
        run.skip(check_id, f"{scene_identifier}: its lines are not known yet")
        return None
    if not run.story.holds(span[0], span[1]):
        run.skip(check_id, f"{scene_identifier}: not in the excerpt of the story given")
        return None
    return span


def counted_lines(run, span):
    numbered = run.story.numbered
    return [number for number in range(span[0], span[1] + 1) if is_story_line(numbered, number)]


def record_lines(breakdown, record, field_name="lines"):
    """(set of line numbers, readable): readable is False when a lines value is written but cannot be read (an
    anchor not found: CITE-02 reports that, so coverage does not report its lines again)."""
    value = record.get(field_name) if record is not None else None
    numbers = set(breakdown.lines_of(record, field_name)) if record is not None else set()
    readable = bool(numbers) or not value or normalise_word(value) == "none"
    return numbers, readable


def lines_left_out(breakdown, scene):
    """Lines a scene leaves out on purpose (SCENE lines_not_shown with a why): COVER-02 is silent for them."""
    numbers = set()
    if scene is None:
        return numbers
    span = breakdown.scene_range(scene.identifier)
    for item in breakdown.items(scene, "lines_not_shown"):
        if not (item.get("why") or "").strip():
            continue
        ranges = parse_line_numbers(item.first or "")
        if ranges:
            for first, last in ranges:
                numbers.update(range(first, last + 1))
        elif breakdown.story is not None and parse_quote_anchor(item.first or ""):
            resolved = breakdown.story.resolve_lines(item.first, span[0] if span else None, span[1] if span else None)
            if resolved:
                numbers.update(range(resolved[0], resolved[1] + 1))
    return numbers


def scene_speeches(breakdown, scene_identifier):
    """The scene's speeches (screenplay speeches from speeches.json, prose SPEECH records), each a dict with its
    ID, speaker, cue line and lines."""
    found = []
    for entry in breakdown.speeches_of_scene(scene_identifier):
        if not entry or entry.get("line") is None:
            continue
        lines = entry.get("lines") or [entry["line"], entry["line"]]
        if isinstance(lines, (list, tuple)) and len(lines) == 2 and all(isinstance(part, int) for part in lines):
            numbers = set(range(lines[0], lines[1] + 1))
        else:
            numbers = {entry["line"]}
        found.append({"id": entry["id"], "speaker": entry.get("speaker"), "line": entry["line"], "lines": numbers,
                      "text": entry.get("text") or ""})
    return found


def story_map_scene(breakdown, scene_identifier):
    for entry in (breakdown.story_map or {}).get("scenes") or []:
        if same_scene(entry.get("id"), scene_identifier):
            return entry
    return None


def shot_is_card_or_black(shot):
    return normalise_word(shot.get("kind") or "") in ("card", "black")


# ---------------------------------------------------------------- what covers a scene (COVER-02 to COVER-04)

@dataclass
class CoverUnit:
    """One shot, or one list item before step 8 and at Quick depth: its beats, its lines and the speeches heard."""
    identifier: str
    record: object
    beats: set
    lines: set
    heard: set
    readable: bool = True


def uses_list_items(run, breakdown, scene):
    """True when a scene's coverage is read from its list items: before step 8 (steps.json's note on step 7), and at
    Quick depth or with no SHOT records outside step 8 (at Quick the list items are the final shots)."""
    if run.step is not None and run.step <= 7:
        return True
    shots = breakdown.shots_of(scene.identifier)
    if shots:
        return False
    return run.step != 8


def coverage_units(run, breakdown, scene):
    """(units, from_list): what covers a scene's lines, beats and speeches."""
    key = ("wp4c coverage units", scene.identifier, run.step)
    if key in run.cache:
        return run.cache[key]
    units = []
    from_list = uses_list_items(run, breakdown, scene)
    if not from_list:
        for shot in breakdown.shots_of(scene.identifier):
            lines, readable = record_lines(breakdown, shot)
            heard = {item.first.strip() for item in breakdown.items(shot, "hear") if item.first}
            units.append(CoverUnit(shot.identifier, shot, set(breakdown.id_list(shot, "beats")), lines, heard,
                                   readable))
    else:
        speeches = scene_speeches(breakdown, scene.identifier)
        for identifier, item in list_items(breakdown, scene.identifier):
            shot = breakdown.record(identifier, "SHOT")
            if shot is not None and normalise_word(shot.get("status") or "") == "omitted":
                continue
            beats = set(split_list(item.get("beats") or ""))
            lines = set()
            readable = True
            for beat_identifier in beats:
                beat = breakdown.record(beat_identifier, "BEAT")
                if beat is None:
                    continue
                beat_lines, beat_readable = record_lines(breakdown, beat)
                lines |= beat_lines
                readable = readable and beat_readable
            heard = {speech["id"] for speech in speeches if speech["line"] in lines}
            units.append(CoverUnit(identifier, None, beats, lines, heard, readable))
    run.cache[key] = (units, from_list)
    return units, from_list


def batch_beats(run, breakdown, scene_identifier):
    """During step 8, the beats that only the batches written so far name (7.2: "only the batch's beats"); None
    means every beat is checked (outside step 8, or once the scene's last batch is in)."""
    written = run.batch_shots(scene_identifier)
    if written is None:
        return None
    items = list_items(breakdown, scene_identifier)
    if items and all(identifier in written for identifier, _ in items):
        return None
    naming = {}
    for identifier, item in items:
        for beat_identifier in split_list(item.get("beats") or ""):
            naming.setdefault(beat_identifier, []).append(identifier)
    return {beat for beat, identifiers in naming.items() if all(identifier in written for identifier in identifiers)}


def beat_lines_of(breakdown, beat_identifiers):
    numbers = set()
    for beat_identifier in beat_identifiers:
        beat = breakdown.record(beat_identifier, "BEAT")
        if beat is not None:
            numbers |= set(breakdown.lines_of(beat))
    return numbers


def what_covers(from_list):
    return "list item" if from_list else "shot"


# ---------------------------------------------------------------- COVER-01 to COVER-04

@register_check("COVER-01", level="E", build=1,
                title="A story line of the scene in no beat (blank lines and the heading excluded)",
                plain="has story lines that no beat covers")
def check_cover_01(run):
    breakdown = breakdown_of(run)
    problems = []
    for scene in kept_scenes(run):
        beats = breakdown.beats_of(scene.identifier)
        if not beats:
            if run.step is None or run.step >= 9:
                span = scene_span(run, breakdown, scene.identifier, "COVER-01")
                if span is not None and counted_lines(run, span):
                    problems.append(report(run, "E", "COVER-01", scene, "lines",
                                           f"{span[0]}-{span[1]} are in no beat: the scene has no beats yet",
                                           "Fix: design the scene (step 7) and give every story line to a beat.",
                                           scene_file_place(run, scene.identifier)))
            continue
        span = scene_span(run, breakdown, scene.identifier, "COVER-01")
        if span is None:
            continue
        covered = set()
        unreadable = []
        endings = []
        for beat in beats:
            numbers, readable = record_lines(breakdown, beat)
            if not readable:
                unreadable.append(beat.identifier)
            covered |= numbers
            if numbers:
                endings.append((max(numbers), beat.identifier))
        if unreadable:
            run.skip("COVER-01", f"{scene.identifier}: the lines of {', '.join(unreadable)} could not be read "
                                 "(a quote anchor not found once; see CITE-02)")
            continue
        counted = counted_lines(run, span)
        missing = {number for number in counted if number not in covered}
        for first, last in story_line_groups(missing, counted):
            before = [beat for end, beat in sorted(endings) if end < first]
            neighbour = f" ({before[-1]} ends before {'it' if first == last else 'them'})" if before else ""
            problems.append(report(
                run, "E", "COVER-01", scene, "lines",
                f"{numbers_text([(first, last)])} {'is' if first == last else 'are'} in no beat (line {first}: "
                f"\"{first_words(run.story.numbered, first)}\")",
                (f"Fix: add them to the lines of the beat they belong to{neighbour}, or give them a beat of their own."
                 if first != last else
                 f"Fix: add it to the lines of the beat it belongs to{neighbour}, or give it a beat of its own."),
                scene_file_place(run, scene.identifier)))
    return problems


@register_check("COVER-02", level="E", build=1,
                title="A story line of the scene in no shot (list item at Quick) unless omitted with a reason",
                plain="has story lines that no shot shows")
def check_cover_02(run):
    breakdown = breakdown_of(run)
    problems = []
    for scene in kept_scenes(run):
        if not breakdown.beats_of(scene.identifier) and not list_items(breakdown, scene.identifier) \
                and not breakdown.shots_of(scene.identifier):
            continue  # not designed yet: COVER-01 says so from step 9
        span = scene_span(run, breakdown, scene.identifier, "COVER-02")
        if span is None:
            continue
        units, from_list = coverage_units(run, breakdown, scene)
        unreadable = [unit.identifier for unit in units if not unit.readable]
        if unreadable:
            run.skip("COVER-02", f"{scene.identifier}: the lines of {', '.join(unreadable)} could not be read "
                                 "(a quote anchor not found once; see CITE-02)")
            continue
        counted = counted_lines(run, span)
        required = set(counted) - lines_left_out(breakdown, scene)
        limit = batch_beats(run, breakdown, scene.identifier)
        if limit is not None:
            required &= beat_lines_of(breakdown, limit)
        covered = set()
        for unit in units:
            covered |= unit.lines
        missing = required - covered
        kind = what_covers(from_list)
        for first, last in story_line_groups(missing, counted):
            showing_before = [unit.identifier for unit in units if unit.lines and max(unit.lines) < first]
            neighbour = (f" ({showing_before[-1]} shows the lines before {'it' if first == last else 'them'})"
                         if showing_before and not from_list else "")
            if from_list:
                fix = "Fix: add the beat that holds them to a list item's beats, or add a list item for it."
            else:
                them = "it" if first == last else "them"
                fix = (f"Fix: add {them} to the lines of a shot{neighbour}, or list {them} under the scene's "
                       "lines_not_shown with a why.")
            problems.append(report(
                run, "E", "COVER-02", scene, "lines",
                f"{numbers_text([(first, last)])} {'is' if first == last else 'are'} in no {kind} (line {first}: "
                f"\"{first_words(run.story.numbered, first)}\")",
                fix, scene_file_place(run, scene.identifier)))
    return problems


@register_check("COVER-03", level="E", build=1, title="A speech heard in no shot",
                plain="has a spoken line that no shot lets us hear")
def check_cover_03(run):
    breakdown = breakdown_of(run)
    problems = []
    for scene in kept_scenes(run):
        if not list_items(breakdown, scene.identifier) and not breakdown.shots_of(scene.identifier):
            continue
        speeches = scene_speeches(breakdown, scene.identifier)
        if not speeches:
            if run.story is None and not breakdown.of_scene("SPEECH", scene.identifier):
                run.story_missing("COVER-03")
            continue
        units, from_list = coverage_units(run, breakdown, scene)
        heard = set()
        for unit in units:
            heard |= unit.heard
        limit = batch_beats(run, breakdown, scene.identifier)
        limit_lines = beat_lines_of(breakdown, limit) if limit is not None else None
        left_out = lines_left_out(breakdown, scene)
        for speech in speeches:
            if speech["id"] in heard:
                continue
            if limit_lines is not None and speech["line"] not in limit_lines:
                continue
            if speech["lines"] and speech["lines"] <= left_out:
                continue
            speaker = element_of(speech.get("speaker") or "") or "the speaker"
            words = " ".join((speech["text"] or "").split()[:8])
            about = f"{speech['id']} ({speaker}, line {speech['line']}" + (f": \"{words}\")" if words else ")")
            if from_list:
                problems.append(report(
                    run, "E", "COVER-03", scene, "lines",
                    f"the speech {about} is in no list item's beats",
                    "Fix: add the beat that holds its line to a list item's beats.",
                    scene_file_place(run, scene.identifier)))
                continue
            showing = [unit for unit in units if speech["line"] in unit.lines]
            if showing:
                shot = showing[0].record
                problems.append(report(
                    run, "E", "COVER-03", shot, "hear",
                    f"{about} is heard in no shot, and this shot shows its line",
                    f"Fix: add - hear: {speech['id']} | speaker: on_screen (or off_screen) to this shot, or to the "
                    "shot where it is heard.", place_of(run, shot, "hear")))
            else:
                problems.append(report(
                    run, "E", "COVER-03", scene, "lines",
                    f"the speech {about} is heard in no shot, and no shot shows its line",
                    f"Fix: add its line to a shot's lines and a hear item for {speech['id']} to that shot.",
                    scene_file_place(run, scene.identifier)))
    return problems


@register_check("COVER-04", level="E", build=1, title="A beat with no shot", plain="is in no shot")
def check_cover_04(run):
    breakdown = breakdown_of(run)
    problems = []
    for scene in kept_scenes(run):
        beats = breakdown.beats_of(scene.identifier)
        if not beats:
            continue
        if not list_items(breakdown, scene.identifier) and not breakdown.shots_of(scene.identifier) \
                and run.step is not None and run.step < 7:
            continue
        units, from_list = coverage_units(run, breakdown, scene)
        shown = set()
        for unit in units:
            shown |= unit.beats
        limit = batch_beats(run, breakdown, scene.identifier)
        kind = what_covers(from_list)
        for beat in beats:
            if beat.identifier in shown:
                continue
            if limit is not None and beat.identifier not in limit:
                continue
            numbers = sorted(breakdown.lines_of(beat))
            span_words = numbers_text([(numbers[0], numbers[-1])]) if numbers else (beat.get("lines") or "")
            showing = [unit.identifier for unit in units if numbers and unit.lines & set(numbers)]
            if from_list:
                fix = f"Fix: add {beat.identifier} to the beats of a list item, or add a list item for it."
            elif showing:
                fix = (f"Fix: add {beat.identifier} to the beats of {showing[0]}, which shows its lines, or give the "
                       "beat a shot of its own.")
            else:
                fix = f"Fix: give {beat.identifier} a shot, or add it to the beats of the shot that shows its lines."
            problems.append(report(run, "E", "COVER-04", beat, "lines",
                                   f"{span_words}: the beat is in no {kind}, since no {kind} names it in its beats",
                                   fix, place_of(run, beat, "lines")))
    return problems


# ---------------------------------------------------------------- COVER-05 and COVER-06 (whole film)

def follow_merges(run, scene):
    """The scene a scene's content ends up in (merge and fold hand it to merged_into), or None when it is cut."""
    seen = set()
    while scene is not None and scene.identifier not in seen:
        seen.add(scene.identifier)
        keep = normalise_word(scene.get("keep") or "keep")
        if keep in ("keep", "trim"):
            return scene
        if keep in ("merge", "fold") and scene.get("merged_into"):
            target = run.record(scene.get("merged_into"))
            scene = target if target is not None and target.type_name == "SCENE" else None
            continue
        return None
    return None


@register_check("COVER-05", level="E", build=1, title="A cardinal event in no kept scene",
                plain="happens in no scene the film keeps")
def check_cover_05(run):
    breakdown = breakdown_of(run)
    problems = []
    scenes = [scene for scene in run.records("SCENE") if scene.identifier]
    for cardinal in run.records("CARDINAL"):
        carriers = [scene for scene in scenes if cardinal.identifier in breakdown.id_list(scene, "cardinal")]
        numbers = sorted(breakdown.lines_of(cardinal)) if cardinal.get("lines") else []
        if not carriers and numbers:
            for scene in scenes:
                span = breakdown.scene_range(scene.identifier)
                if span and span[0] <= numbers[0] <= span[1]:
                    carriers.append(scene)
        if not carriers:
            value = cardinal.get("lines")
            if value and not numbers and run.story is None:
                run.story_missing("COVER-05")
                continue
            if numbers and run.story is not None and run.story.excerpt and not run.story.holds(numbers[0]):
                run.skip("COVER-05", f"{cardinal.identifier}: its lines are not in the excerpt of the story given")
                continue
            if numbers and scene_of_line_left_out(run, numbers[0]):
                run.skip("COVER-05", f"{cardinal.identifier}: its scene has no record here (not in the excerpt)")
                continue
            where = f"its lines {numbers[0]}-{numbers[-1]} lie" if numbers else "it lies"
            problems.append(report(
                run, "E", "COVER-05", cardinal, "lines",
                f"{where} in no scene of the scene list, and no scene lists it in its cardinal events",
                f"Fix: add {cardinal.identifier} to the cardinal list of the kept scene that carries it.",
                place_of(run, cardinal, "lines")))
            continue
        if any(follow_merges(run, scene) is not None for scene in carriers):
            continue
        names = ", ".join(f"{scene.identifier} (keep: {normalise_word(scene.get('keep') or 'keep')})"
                          for scene in carriers)
        problems.append(report(
            run, "E", "COVER-05", cardinal, "lines",
            f"the key event is carried only by scenes the film does not keep: {names}",
            f"Fix: keep or trim one of them, merge it into a kept scene (merged_into), or move {cardinal.identifier} "
            "into a kept scene's cardinal list.", place_of(run, cardinal, "lines")))
    return problems


def scene_of_line_left_out(run, line):
    """True when a line lies in a story scene that has no SCENE record and lies outside the project's scope."""
    if run.story is None:
        return False
    for identifier, span in run.story.numbered.scenes.items():
        if span[0] <= line <= span[1]:
            return run.scene_left_out(identifier)
    return False


def sequence_scenes(value, known_scenes):
    """The scene IDs a SEQUENCE's scenes value holds: ranges first..last (by story order) and single IDs."""
    held = set()
    for piece in split_list(value or ""):
        if ".." in piece:
            first, last = [part.strip() for part in piece.split("..", 1)]
            low, high = scene_key(first), scene_key(last)
            held.update(identifier for identifier in known_scenes if low <= scene_key(identifier) <= high)
            held.update((first, last))
        elif piece:
            held.add(piece.strip())
    return held


@register_check("COVER-06", level="E", build=1, title="A scene in no sequence, or in two",
                plain="belongs to no group of scenes, or to two")
def check_cover_06(run):
    problems = []
    scenes = kept_scenes(run)
    if not scenes:
        return problems
    sequences = run.records("SEQUENCE")
    known = [scene.identifier for scene in run.records("SCENE") if scene.identifier]
    holding = {}
    for sequence in sequences:
        for identifier in sequence_scenes(sequence.get("scenes"), known):
            holding.setdefault(identifier, []).append(sequence)
    for scene in scenes:
        holders = [sequence for identifier, found in holding.items() if same_scene(identifier, scene.identifier)
                   for sequence in found]
        holders = list({sequence.identifier: sequence for sequence in holders}.values())
        declared = (scene.get("sequence") or "").strip()
        declared = "" if normalise_word(declared or "none") in ("none", "open") else declared
        place = place_of(run, scene, "sequence")
        if len(holders) >= 2:
            names = " and ".join(f"{sequence.identifier} ({sequence.get('scenes')})" for sequence in holders)
            problems.append(report(run, "E", "COVER-06", scene, "sequence",
                                   f"is in two groups of scenes: {names}",
                                   "Fix: make the groups' scenes ranges meet without overlapping, so each scene is "
                                   "in exactly one.", place))
        elif not holders and not declared:
            fix = ("Fix: set sequence to the group this scene belongs to and include it in that group's scenes range."
                   if sequences else "Fix: write the groups of scenes (SEQUENCE records, step 2) and set sequence.")
            problems.append(report(run, "E", "COVER-06", scene, "sequence",
                                   "is in no group of scenes: no SEQUENCE's scenes hold it and its sequence is empty",
                                   fix, place))
        elif not holders:
            named = run.record(declared)
            range_words = f" ({named.get('scenes')})" if named is not None and named.type_name == "SEQUENCE" else ""
            problems.append(report(run, "E", "COVER-06", scene, "sequence",
                                   f"says {declared}, but {declared}'s scenes{range_words} leave it out, so it is in "
                                   "no group of scenes",
                                   f"Fix: widen {declared}'s scenes range to hold {scene.identifier}, or set sequence "
                                   "to the group that holds it.", place))
        elif declared and not any(sequence.identifier == declared for sequence in holders):
            problems.append(report(run, "E", "COVER-06", scene, "sequence",
                                   f"says {declared}, but {holders[0].identifier}'s scenes "
                                   f"({holders[0].get('scenes')}) hold it: it is in two groups of scenes",
                                   f"Fix: set sequence to {holders[0].identifier}, or move {scene.identifier} out of "
                                   f"{holders[0].identifier}'s scenes range and into {declared}'s.", place))
    return problems


# ---------------------------------------------------------------- COVER-07 and COVER-08 (what the story writes)

def sound_stems(token_text):
    """The stems of a scripted sound token's sound words: 'A clock TICKS' gives {'tick'}."""
    try:
        from .read_story import SOUND_WORDS
    except ImportError:  # the reader is part of this package; this only guards a broken copy
        SOUND_WORDS = set()
    words = re.findall(r"[A-Za-z]+", token_text or "")
    chosen = [word for word in words if word.upper() in SOUND_WORDS] or words
    stems = set()
    for word in chosen:
        lowered = word.lower()
        for ending in SOUND_WORD_ENDINGS:
            if lowered.endswith(ending) and len(lowered) - len(ending) >= SOUND_STEM_LENGTH_MIN:
                lowered = lowered[:-len(ending)]
                break
        stems.add(lowered)
    return stems


def mentions_any(text, stems):
    lowered = (text or "").lower()
    return any(re.search(r"\b" + re.escape(stem), lowered) for stem in stems)


def scene_sound_texts(run, breakdown, scene, from_list):
    """Every place in a scene's records that can carry a written sound: effects, room sounds (shot, scene and
    place), and at Quick depth the list items' words. Each is (text, record, field)."""
    texts = []
    location = breakdown.record(scene.get("location"), "LOCATION") if scene.get("location") else None
    place_sound = location.get("room_sound") if location is not None else None
    scene_sound = scene.get("room_sound")
    for value in (scene_sound, place_sound):
        if value and normalise_word(value) not in ("as_place", "none"):
            texts.append((value, scene, "room_sound"))
    for shot in breakdown.shots_of(scene.identifier):
        for item in breakdown.items(shot, "effect"):
            texts.append((item.first or "", shot, "effect"))
        value = shot.get("room_sound")
        if value and normalise_word(value) not in ("as_place", "none"):
            texts.append((value, shot, "room_sound"))
    if from_list:
        for identifier, item in list_items(breakdown, scene.identifier):
            texts.append((item.get("shows") or "", identifier, "item"))
    return texts


def motif_appears_in_scene(breakdown, motif, scene_identifier):
    """True when a MOTIF has an appearance in the scene (a scene ID, a story point in it, or one of its shots)."""
    for item in breakdown.items(motif, "appearance"):
        first = (item.first or "").strip()
        point = parse_story_point(first)
        where = point[0] if point else scene_of(first)
        if where and same_scene(where, scene_identifier):
            return True
    return False


@register_check("COVER-07", level="E", build=1,
                title="A scripted sound (a capitalised sound token, A4 §4.2) with no effect, room_sound or MOTIF "
                      "appearance in its scene",
                plain="leaves out a sound the story writes")
def check_cover_07(run):
    breakdown = breakdown_of(run)
    problems = []
    for scene in kept_scenes(run):
        if not breakdown.shots_of(scene.identifier) and not list_items(breakdown, scene.identifier):
            continue
        if run.story_missing("COVER-07"):
            return problems
        entry = story_map_scene(breakdown, scene.identifier)
        if entry is None:
            run.skip("COVER-07", f"{scene.identifier}: not in the excerpt of the story given (no capitalised words "
                                 "read for it)")
            continue
        tokens = [token for token in entry.get("capitalised_words") or [] if token.get("class") == "sound"]
        if not tokens:
            continue
        units, from_list = coverage_units(run, breakdown, scene)
        texts = scene_sound_texts(run, breakdown, scene, from_list)
        motifs = [motif for motif in breakdown.records_of("MOTIF")
                  if motif_appears_in_scene(breakdown, motif, scene.identifier)]
        for token in tokens:
            stems = sound_stems(token.get("text"))
            if any(mentions_any(text, stems) for text, _, _ in texts):
                continue
            if any(mentions_any(" ".join([motif.title or "", motif.get("meaning") or "", motif.get("signature") or ""]),
                                stems) for motif in motifs):
                continue
            line = token.get("line")
            showing = [unit for unit in units if line in unit.lines and unit.record is not None]
            what = (f"the sound the story writes in capitals, {token.get('text')} (line {line}), has no effect, room "
                    f"sound or motif in {scene.identifier}")
            if showing:
                shot = showing[0].record
                problems.append(report(run, "E", "COVER-07", shot, "effect", what + ", and this shot shows its line",
                                       "Fix: add - effect: <what is heard> | at: <seconds> to this shot, naming the "
                                       "sound.", place_of(run, shot, "effect")))
            else:
                problems.append(report(run, "E", "COVER-07", scene, "room_sound", what,
                                       f"Fix: add an effect naming it to the shot that shows line {line}, or carry it "
                                       "in the room sound or a sound motif.", place_of(run, scene, "room_sound")))
    return problems


def scene_look(breakdown, scene):
    look = breakdown.record(scene.get("look"), "LOOK") if scene.get("look") else None
    if look is not None:
        return look
    location = scene.get("location")
    for candidate in breakdown.records_of("LOOK"):
        if location and candidate.get("for") == location:
            return candidate
    return None


def light_cue_lines(run, breakdown, scene_identifier):
    """{line: LOOK ID} for every line a LOOK light_cue at a story point in this scene covers: the quote's line and
    the lines of the beat it resolves to."""
    covered = {}
    span = breakdown.scene_range(scene_identifier)
    for look in breakdown.records_of("LOOK"):
        for item in breakdown.items(look, "light_cue"):
            point = parse_story_point((item.first or "").strip())
            if not point or not same_scene(point[0], scene_identifier):
                continue
            beat_identifier = point[2]
            if breakdown.story is not None and span:
                line = breakdown.story.resolve_line(f'"{point[1]}"', span[0], span[1])
                if line is not None:
                    covered.setdefault(line, look.identifier)
                if beat_identifier is None:
                    beat_identifier = resolve_story_point(breakdown, (item.first or "").strip()).beat
            beat = breakdown.record(beat_identifier, "BEAT") if beat_identifier else None
            if beat is not None:
                for number in breakdown.lines_of(beat):
                    covered.setdefault(number, look.identifier)
    return covered


def colours_kept(breakdown, scene, look):
    """The words of every description that keeps a thing's colour in this scene (B2 P2: an object's colour holds
    under every light): the look's text, and the fixed descriptions and state lines of what is present."""
    texts = []
    if look is not None:
        texts += [look.get(name) or "" for name in LOOK_COLOUR_FIELDS]
    for element in elements_present(breakdown, scene.identifier):
        record = breakdown.record(element)
        if record is not None:
            texts.append(record.get("fixed_description") or "")
    for state_identifier in states_in_play(breakdown, scene.identifier):
        state = breakdown.record(state_identifier, "STATE")
        if state is not None:
            texts.append(state.get("state_line") or "")
    return set(re.findall(r"[a-z]+", " ".join(texts).lower()))


# COVER-08 reads light words in their sentence: a light the scene's LOOK already carries, described as it is, is
# covered by the look. Brightness words are covered by any look with a main light; a named source (torch, lamp) by a
# look whose text names it, a word built on it (torchlight) or the project's word swap for it (torch becomes
# flashlight). A sentence where the light changes or moves is never covered by the look alone: it needs a light cue.
# That is a word of change (the light dims, flickers, dies, goes out, floods in), a person moving the light (holds,
# lifts, brings it up, points it) or a beat of light repeated ("Light, brick, light, brick.").
def look_light_words(breakdown, look):
    """The words of a LOOK's light text, with the project's word swaps read both ways (torch and flashlight)."""
    if look is None:
        return set()
    text = " ".join(look.get(name) or "" for name in LOOK_COLOUR_FIELDS)
    words = set(re.findall(r"[a-z]+", text.lower()))
    project = next(iter(breakdown.records_of("PROJECT")), None)
    for written in (project.get_all("prompt_words") if project is not None else []):
        parts = [piece.strip().lower() for piece in re.split(r"\|\s*use:", written)]
        if len(parts) == 2:
            original, swapped = parts
            swapped_words = set(re.findall(r"[a-z]+", swapped))
            if original in words or (swapped_words and swapped_words <= words | {"a", "the", "of"}):
                words.add(original)
                words |= swapped_words
    return words


def light_word_carried_by_look(word, look, look_words):
    """True when the LOOK already carries a light word of the story (the word lists are in derive_fields)."""
    if look is None or word in LIGHT_CHANGE_WORDS:
        return False
    if word in LIGHT_BRIGHTNESS_WORDS:
        return bool(look.get("main_light")) and normalise_word(look.get("main_light") or "none") != "none"
    if word in look_words:
        return True
    return any(word.startswith(stem) and len(stem) >= 4 for stem in look_words) or \
        any(stem.startswith(word) and len(word) >= 4 for stem in look_words)


@register_check("COVER-08", level="W", build=1,
                title="A scripted light, colour or darkness line (B2 P2) with no LOOK light_cue, no stays_dark and "
                      "no shot light covering it",
                plain="leaves out light, colour or darkness the story writes")
def check_cover_08(run):
    breakdown = breakdown_of(run)
    problems = []
    for scene in kept_scenes(run):
        if not breakdown.shots_of(scene.identifier) and not list_items(breakdown, scene.identifier):
            continue
        if run.story_missing("COVER-08"):
            return problems
        entry = story_map_scene(breakdown, scene.identifier)
        if entry is None:
            run.skip("COVER-08", f"{scene.identifier}: not in the excerpt of the story given (no light lines read "
                                 "for it)")
            continue
        light_lines = entry.get("light_lines") or []
        if not light_lines:
            continue
        look = scene_look(breakdown, scene)
        stays_dark = look is not None and normalise_word(look.get("stays_dark") or "none") not in ("none", "")
        look_words = look_light_words(breakdown, look)
        cue_lines = light_cue_lines(run, breakdown, scene.identifier)
        kept_words = colours_kept(breakdown, scene, look)
        units, _ = coverage_units(run, breakdown, scene)
        shot_units = [unit for unit in units if unit.record is not None]
        for entry_line in light_lines:
            line = entry_line.get("line")
            words = [word.lower() for word in entry_line.get("words") or []]
            if line in cue_lines:
                continue
            showing = [unit.record for unit in shot_units if line in unit.lines]
            if any(normalise_word(shot.get("light") or "as_look") not in ("as_look", "none")
                   or normalise_word(shot.get("light_cue") or "none") != "none" for shot in showing):
                continue
            open_words = []
            line_text = run.story.numbered.line(line)
            for word in light_words_in_context(line_text, words):
                if word in DARKNESS_WORDS and stays_dark:
                    continue
                if word in COLOUR_WORDS and word in kept_words:
                    continue
                if word not in COLOUR_WORDS and word not in DARKNESS_WORDS and \
                        not light_moves_in(sentence_holding(line_text, [word]) or line_text, word) and \
                        light_word_carried_by_look(word, look, look_words):
                    continue
                open_words.append(word)
            if not open_words:
                continue
            look_name = look.identifier if look is not None else "a LOOK for this place and time (none yet)"
            reasons = [f"no light_cue of {look.identifier} at it" if look is not None else "the scene has no LOOK"]
            if any(word in DARKNESS_WORDS for word in open_words):
                reasons.append("no stays_dark")
            if any(word in COLOUR_WORDS for word in open_words):
                reasons.append("no description here keeps the colour")
            if showing:
                reasons.append(f"{showing[0].identifier}, which shows it, has light as_look and no light_cue")
            sentence = sentence_holding(run.story.numbered.line(line), open_words)
            where = f"{scene.identifier} \"{sentence}\"" if sentence else f"line {line}"
            problems.append(report(
                run, "W", "COVER-08", scene, "look",
                f"line {line} writes light, colour or darkness ({', '.join(open_words)}) that nothing covers: "
                + "; ".join(reasons),
                f"Fix: add a light_cue at {where} to {look_name}, or write the light on the shot that shows it (light "
                "or light_cue).", place_of(run, scene, "look")))
    return problems


# ---------------------------------------------------------------- TIME-01 to TIME-03

def provisional_least(floor):
    """(least seconds, words) a list item surely needs: its provisional floor, less the speeches of a shared beat
    that another item may hear instead (derive_fields gives those to every sharing item, so the floor is then only
    an upper bound)."""
    shared = {speech for speech, _ in floor.shared_speeches}
    if not shared:
        return floor.floor, f"its provisional floor is {seconds_text(floor.floor)} s: {floor.short_reason()}"
    least = floor.floor - sum(part[4] for part in floor.speech_parts if part[0] in shared)
    return round(least, 2), (f"its provisional floor is {seconds_text(floor.floor)} s ({floor.short_reason()}), and "
                             f"at least {seconds_text(round(least, 2))} s even if {', '.join(sorted(shared))} is heard "
                             "in another item")


def suggested_seconds(floor):
    """The next half second at or above a floor: 13.8 gives 14."""
    return seconds_words(math.ceil(floor * 2 - TIME_TOLERANCE_S) / 2)


@register_check("TIME-01", level="E", build=1,
                title="Screen time under the derived floor, max(speech_floor, text_floor) + pause_owed (5.6)",
                plain="is shorter than the time its speech and pauses need")
def check_time_01(run):
    breakdown = breakdown_of(run)
    problems = []
    words_unknown = []
    lines_unknown = []
    for scene in kept_scenes(run):
        shots = breakdown.shots_of(scene.identifier)
        if shots:
            for shot in shots:
                screen_time = number_of(shot.get("screen_time"))
                if screen_time is None:
                    continue
                floor = time_floor(breakdown, shot)
                if not floor.complete:
                    (lines_unknown if floor.unresolved_lines and not floor.unknown_speeches
                     else words_unknown).append(shot.identifier)
                    continue
                if screen_time + TIME_TOLERANCE_S >= floor.floor:
                    continue
                spoken = [item.first for item in breakdown.items(shot, "hear") if item.first]
                fix = f"Fix: raise screen_time to {suggested_seconds(floor.floor)}"
                if spoken:
                    fix += f" or move {spoken[-1]} to the next shot"
                problems.append(report(run, "E", "TIME-01", shot, "screen_time",
                                       f"{seconds_words(screen_time)} is under its floor {seconds_text(floor.floor)} s "
                                       f"({floor.short_reason()})", fix + ".",
                                       place_of(run, shot, "screen_time")))
        elif run.depth_rank(scene) <= 1:
            shot_list = breakdown.record(f"{scene.identifier}-LIST", "SHOTLIST")
            for identifier, item in list_items(breakdown, scene.identifier):
                time = number_of(item.get("time"))
                if time is None:
                    continue
                floor = provisional_floor(breakdown, scene.identifier, identifier)
                if floor is None or not floor.complete:
                    continue
                least, words = provisional_least(floor)
                if time + TIME_TOLERANCE_S >= least:
                    continue
                problems.append(report(run, "E", "TIME-01", shot_list, "item",
                                       f"{identifier} time {seconds_words(time)} is under its floor: {words}",
                                       f"Fix: raise its time to {suggested_seconds(least)}, or give part of its "
                                       "beats to the next item.", place_of(run, shot_list, "item", identifier)))
    if words_unknown:
        run.skip("TIME-01", f"story not present: the words heard in {len(words_unknown)} shots are not known (and "
                            f"their hear items give no words), so their floors are not worked out "
                            f"({', '.join(words_unknown[:6])}{' ...' if len(words_unknown) > 6 else ''})")
    if lines_unknown:
        run.skip("TIME-01", f"{'story not present' if run.story is None else 'not in the excerpt'}: the lines of "
                            f"{len(lines_unknown)} shots or their beats are quotes not found in the story given, so the "
                            f"pause they owe is not known ({', '.join(lines_unknown[:6])}"
                            f"{' ...' if len(lines_unknown) > 6 else ''})")
    return problems


def moment_spans(run, shot):
    """[(start, end, written first part, (file, line))] for every moment of a shot whose span can be read."""
    spans = []
    seen = set()
    for record_file, _, line in run.field_lines(shot.key, "moment"):
        if line.missing:
            continue
        item = split_item(line.value)
        written = (item.first or "").strip()
        match = SPAN.match(written)
        if not match or (written, line.value) in seen:
            continue
        seen.add((written, line.value))
        spans.append((float(match.group(1)), float(match.group(2)), written, (record_file.name, line.line_number)))
    return spans


@register_check("TIME-02", level="E", build=1, title="A moment outside the screen time, or moments overlapping",
                plain="has a timed moment outside its length, or two moments that overlap")
def check_time_02(run):
    breakdown = breakdown_of(run)
    problems = []
    for scene in kept_scenes(run):
        for shot in breakdown.shots_of(scene.identifier):
            spans = moment_spans(run, shot)
            if not spans:
                continue
            screen_time = number_of(shot.get("screen_time"))
            for start, end, written, place in spans:
                if start < 0 or end <= start:
                    problems.append(report(run, "E", "TIME-02", shot, "moment",
                                           f"{written} does not run forward from 0 or later",
                                           "Fix: write the moment as start-end in seconds from the shot's start, with "
                                           "end after start.", place))
                elif screen_time is not None and end > screen_time + TIME_TOLERANCE_S:
                    problems.append(report(run, "E", "TIME-02", shot, "moment",
                                           f"{written} runs past the screen time {seconds_words(screen_time)} s",
                                           f"Fix: end it by {seconds_words(screen_time)}, or raise screen_time.",
                                           place))
            ordered = sorted((span for span in spans if span[1] > span[0] >= 0), key=lambda span: (span[0], span[1]))
            for earlier, later in zip(ordered, ordered[1:]):
                if later[0] < earlier[1] - TIME_TOLERANCE_S:
                    problems.append(report(run, "E", "TIME-02", shot, "moment",
                                           f"{later[2]} overlaps {earlier[2]}",
                                           f"Fix: start it at {seconds_words(earlier[1])} or later, or end the moment "
                                           "before it sooner.", later[3]))
    return problems


def scene_total(run, breakdown, scene):
    """(total seconds, what was counted) of a scene: its shots' screen time plus black frames on its cuts, or its
    list items' times before step 8 and at Quick; None when nothing is timed."""
    units, from_list = coverage_units(run, breakdown, scene)
    if from_list:
        times = [number_of(item.get("time")) for _, item in list_items(breakdown, scene.identifier)]
        times = [time for time in times if time is not None]
        return (sum(times), "list items") if times else (None, "")
    shots = breakdown.shots_of(scene.identifier)
    times = [number_of(shot.get("screen_time")) for shot in shots]
    times = [time for time in times if time is not None]
    if not times:
        return None, ""
    project = breakdown.project
    frames_per_second = number_of(project.get("fps") if project is not None else None) or 24.0
    black = sum(number_of(cut.get("black_frames"), 0.0) or 0.0 for cut in breakdown.of_scene("CUT", scene.identifier))
    return sum(times) + black / frames_per_second, "shots"


@register_check("TIME-03", level="W", build=1,
                title="Scene total outside its design (the approved list's total) by more than scene_total_tolerance "
                      "(a warning; run after the scene's last batch); a design more than scene_target_far_ratio "
                      "times its planned length, or under its inverse",
                plain="is longer or shorter than planned")
def check_time_03(run):
    """A warning only. The full run (Project notes 31, problem 10): a scene is measured against its own design, the
    total of its one-line list's times, which step 7 set with room for speech, text reading and the pauses owed; the
    target from the first estimate (word counts) is a guess and is not judged, so a scene given room to breathe
    after an intense one (FILM-07) is never flagged for it. Before the shots are written, and at Quick depth, the
    list is the design and there is nothing to compare. One tolerance, scene_total_tolerance, everywhere."""
    breakdown = breakdown_of(run)
    problems = []
    tolerance = constant(run.constants, "scene_total_tolerance", None)
    if tolerance is None:
        run.skip("TIME-03", "scene_total_tolerance is missing from rules/constants.json")
        return problems
    far = constant(run.constants, "scene_target_far_ratio", None)
    for scene in kept_scenes(run):
        problems += design_far_from_target(run, breakdown, scene, far)
        if batch_beats(run, breakdown, scene.identifier) is not None:
            run.skip("TIME-03", f"{scene.identifier}: runs after the scene's last batch")
            continue
        total, counted = scene_total(run, breakdown, scene)
        if total is None or counted != "shots":
            continue
        times = [number_of(item.get("time")) for _, item in list_items(breakdown, scene.identifier)]
        times = [time for time in times if time is not None]
        design = sum(times) if times else None
        if not design:
            continue
        share = (total - design) / design
        if abs(share) <= tolerance + TIME_TOLERANCE_S:
            continue
        direction = "over" if share > 0 else "under"
        record = breakdown.record(f"{scene.identifier}-LIST", "SHOTLIST") or scene
        problems.append(report(run, "W", "TIME-03", record, "item",
                               f"the scene's shots run {seconds_text(round(total, 2))} s, {round(abs(share) * 100)}% "
                               f"{direction} its one-line list's {seconds_text(round(design, 2))} s (at most "
                               f"{round(tolerance * 100)}% either way, scene_total_tolerance)",
                               "Fix: " + ("shorten the shots that hold longer than the list planned" if share > 0 else
                                          "hold the shots that need it longer") +
                               ", or change the list's times (and say why) when the shots found time the list missed.",
                               place_of(run, record, "item")))
    return problems


def design_far_from_target(run, breakdown, scene, far):
    """TIME-03's wide warning, from step 7: the scene's one-line list totals more than scene_target_far_ratio times
    its planned target_duration_s, or under its inverse. The target is the first estimate's guess and is not kept to,
    but a scene twice or half its plan changes the film's length, and the user should hear of it."""
    target = number_of(scene.get("target_duration_s"))
    if not far or not target:
        return []
    times = [number_of(item.get("time")) for _, item in list_items(breakdown, scene.identifier)]
    times = [time for time in times if time is not None]
    design = sum(times) if times else None
    if not design or 1 / far <= design / target <= far:
        return []
    record = breakdown.record(f"{scene.identifier}-LIST", "SHOTLIST") or scene
    how = f"{design / target:.1f} times" if design > target else f"{round(design / target * 100)}% of"
    return [report(run, "W", "TIME-03", record, "item",
                   f"the scene's one-line list totals {seconds_text(round(design, 2))} s, {how} its planned "
                   f"{round(target, 2):g} s (target_duration_s; more than {far:g} times or under "
                   f"1/{far:g} of it is warned, scene_target_far_ratio)",
                   "Fix: check the list's times against the scene's lines; when the scene really needs this length, "
                   "keep it and say so in the report to the user, since it changes the film's length.",
                   place_of(run, record, "item"))]


# ---------------------------------------------------------------- pauses (TIME-04, TIME-05, TIME-08)

def pause_tier_ranges(run):
    """{tier: (from, to, includes_end)} from the constant pause_tiers, and the hold's lower bound."""
    tiers = constant(run.constants, "pause_tiers", {}) or {}
    ranges = {}
    for name in ("short", "medium", "long"):
        entry = tiers.get(name)
        if isinstance(entry, dict) and "from_s" in entry and "to_s" in entry:
            ranges[name] = (float(entry["from_s"]), float(entry["to_s"]), bool(entry.get("includes_end")))
    hold = tiers.get("hold") or {}
    hold_above = float(hold.get("above_s")) if isinstance(hold, dict) and "above_s" in hold else None
    return ranges, hold_above


def written_pause(breakdown, beat):
    """(tier, seconds or None, item) of a beat's pause_after as written; ('none', None, None) when absent."""
    item = breakdown.item(beat, "pause_after")
    if item is None:
        return "none", None, None
    tier = normalise_word(item.first or "none") or "none"
    return tier, number_of(item.get("seconds")), item


def tier_holds(ranges, tier, seconds):
    low, high, includes_end = ranges[tier]
    return low <= seconds < high or (includes_end and abs(seconds - high) <= TIME_TOLERANCE_S)


def tier_of_seconds(ranges, hold_above, seconds):
    for name, _ in ranges.items():
        if tier_holds(ranges, name, seconds):
            return name
    if hold_above is not None and seconds > hold_above:
        return "hold"
    return None


def range_words(ranges, tier):
    low, high, includes_end = ranges[tier]
    return f"[{seconds_text(low)}, {seconds_text(high)}{']' if includes_end else ')'}"


def is_long_pause(ranges, tier, seconds):
    if "long" not in ranges:
        return tier == "long"
    if seconds is not None:
        return tier != "hold" and tier_holds(ranges, "long", seconds)
    return tier == "long"


@register_check("TIME-04", level="E", build=1, title="More than two long pauses in a scene",
                plain="has one long pause too many for its scene")
def check_time_04(run):
    breakdown = breakdown_of(run)
    problems = []
    most = constant(run.constants, "long_pauses_per_scene_max", None)
    if most is None:
        run.skip("TIME-04", "long_pauses_per_scene_max is missing from rules/constants.json")
        return problems
    ranges, _ = pause_tier_ranges(run)
    for scene in kept_scenes(run):
        long_beats = []
        for beat in breakdown.beats_of(scene.identifier):
            tier, seconds, _ = written_pause(breakdown, beat)
            if is_long_pause(ranges, tier, seconds):
                long_beats.append(beat)
        if len(long_beats) <= most:
            continue
        over = long_beats[int(most)]
        problems.append(report(run, "E", "TIME-04", over, "pause_after",
                               f"is long pause {int(most) + 1} of {len(long_beats)} in {scene.identifier} "
                               f"({', '.join(beat.identifier for beat in long_beats)}); a scene holds at most "
                               f"{int(most)} (long_pauses_per_scene_max)",
                               f"Fix: make {len(long_beats) - int(most)} of them medium (under "
                               f"{seconds_text(ranges['long'][0]) if 'long' in ranges else 'the long tier'} s) "
                               "or short.", place_of(run, over, "pause_after")))
    return problems


def is_turn(beat):
    return normalise_word(beat.get("turn") or "none") != "none"


@register_check("TIME-05", level="E", build=1,
                title="The pause owed by a turn beat (5.6) is under turn_reaction_min_s (2.0 s)",
                plain="gives a turn less time to land than a turn needs")
def check_time_05(run):
    """Two readings of 7.2 (the formula in 5.6 always owes at least turn_reaction_min_s):
    - the pause a turn beat writes is under the minimum: explicit seconds under it, or the short tier, whose whole
      range is under it (a pause written 'none' is read as not written: the reaction is owed all the same);
    - the reaction is owed by no shot: the turn beat's last story line is in no shot's lines, so no floor holds it;
      before step 8 (list items), the last list item naming the turn beat has a time under its provisional floor,
      which holds the reaction (card 03: leave room for it in the list item)."""
    breakdown = breakdown_of(run)
    problems = []
    minimum = constant(run.constants, "turn_reaction_min_s", None)
    if minimum is None:
        run.skip("TIME-05", "turn_reaction_min_s is missing from rules/constants.json")
        return problems
    ranges, _ = pause_tier_ranges(run)
    for scene in kept_scenes(run):
        units, from_list = coverage_units(run, breakdown, scene)
        items = list_items(breakdown, scene.identifier)
        limit = batch_beats(run, breakdown, scene.identifier)
        for beat in breakdown.beats_of(scene.identifier):
            if not is_turn(beat):
                continue
            tier, seconds, _ = written_pause(breakdown, beat)
            place = place_of(run, beat, "pause_after")
            written_short = (seconds is not None and seconds + TIME_TOLERANCE_S < minimum) or \
                (seconds is None and tier == "short" and "short" in ranges and ranges["short"][1] <= minimum)
            if written_short:
                written = f"{tier} | seconds: {seconds_words(seconds)}" if seconds is not None else tier
                problems.append(report(run, "E", "TIME-05", beat, "pause_after",
                                       f"{written} gives the turn less than the {seconds_text(minimum)} s of reaction "
                                       "a turn owes (turn_reaction_min_s)",
                                       f"Fix: give it at least {seconds_text(minimum)} s (medium | seconds: "
                                       f"{seconds_text(minimum)}, or long), held on the one who receives the turn.",
                                       place))
                continue
            if from_list:
                naming = [(identifier, item) for identifier, item in items
                          if beat.identifier in split_list(item.get("beats") or "")]
                if not naming:
                    continue  # COVER-04 reports a beat in no list item
                identifier, item = naming[-1]
                time = number_of(item.get("time"))
                floor = provisional_floor(breakdown, scene.identifier, identifier)
                if time is None or floor is None or not floor.complete:
                    continue
                least, words = provisional_least(floor)
                if time + TIME_TOLERANCE_S < least:
                    problems.append(report(run, "E", "TIME-05", beat, "pause_after",
                                           f"the list item that ends this turn, {identifier}, has time "
                                           f"{seconds_words(time)}, which leaves no room for the reaction the turn "
                                           f"owes ({words})",
                                           f"Fix: raise {identifier}'s time to {suggested_seconds(least)}, or move "
                                           "part of its beats to another item.", place))
                continue
            if limit is not None and beat.identifier not in limit:
                continue
            if run.story is None:
                run.story_missing("TIME-05")
                continue
            numbers = breakdown.lines_of(beat)
            if not numbers or not run.story.holds(min(numbers), max(numbers)):
                continue
            last = breakdown.last_story_line(numbers)
            if any(last in unit.lines for unit in units):
                continue
            problems.append(report(run, "E", "TIME-05", beat, "pause_after",
                                   f"no shot owes the turn's reaction of at least {seconds_text(minimum)} s: its last "
                                   f"line, {last}, is in no shot's lines, so no shot's floor holds the pause",
                                   f"Fix: add line {last} to the lines of the shot that ends the turn, so that shot "
                                   "holds the reaction.", place))
    return problems


def hold_reserves(breakdown):
    """The saved choices (RESERVE records) that allow a pause held above the long tier: match pause_after = hold."""
    found = []
    for reserve in breakdown.records_of("RESERVE"):
        match = RESERVE_MATCH.match(reserve.get("match") or "")
        if match and match.group(1) == "pause_after" and match.group(2) == "hold":
            found.append(reserve)
    return found


def reserve_allows(reserve, beat_identifier, scene_identifier):
    """True when a saved choice's allowed_in names this beat or scene, or names no scene or beat at all."""
    named = SCENE_OR_BEAT_IN_TEXT.findall(reserve.get("allowed_in") or "")
    if not named:
        return True
    return any(name == beat_identifier or (("-" not in name) and same_scene(name, scene_identifier)) for name in named)


def hold_is_saved(breakdown, beat, scene_identifier):
    reserves = hold_reserves(breakdown)
    if any(reserve_allows(reserve, beat.identifier, scene_identifier) for reserve in reserves):
        return True
    names = {reserve.identifier for reserve in reserves}
    for shot in breakdown.shots_of(scene_identifier):
        if beat.identifier in breakdown.id_list(shot, "beats") and names & set(breakdown.id_list(shot, "because")):
            return True
    return False


@register_check("TIME-08", level="E", build=1,
                title="Pause seconds outside their tier (half-open ranges, 5.8); a hold above 4.0 s without a saved "
                      "choice",
                plain="has a pause whose length does not fit its kind, or a hold with no saved choice")
def check_time_08(run):
    breakdown = breakdown_of(run)
    problems = []
    ranges, hold_above = pause_tier_ranges(run)
    if not ranges:
        run.skip("TIME-08", "pause_tiers is missing from rules/constants.json")
        return problems
    for scene in kept_scenes(run):
        for beat in breakdown.beats_of(scene.identifier):
            tier, seconds, item = written_pause(breakdown, beat)
            if item is None:
                continue
            place = place_of(run, beat, "pause_after")
            written = f"{tier} | seconds: {seconds_words(seconds)}" if seconds is not None else tier
            if seconds is not None:
                fitting = tier_of_seconds(ranges, hold_above, seconds)
                if tier in ranges and not tier_holds(ranges, tier, seconds):
                    problems.append(report(run, "E", "TIME-08", beat, "pause_after",
                                           f"{written}: {seconds_words(seconds)} s is outside the {tier} tier "
                                           f"{range_words(ranges, tier)} s (pause_tiers)",
                                           f"Fix: write the tier its seconds fall in ({fitting or 'none'}), or change "
                                           f"the seconds to fit {tier}.", place))
                    continue
                if tier == "none" and seconds > TIME_TOLERANCE_S:
                    problems.append(report(run, "E", "TIME-08", beat, "pause_after",
                                           f"{written}: a pause of none has no seconds",
                                           f"Fix: write the tier its seconds fall in ({fitting or 'none'}), or remove "
                                           "the seconds.", place))
                    continue
                if tier == "hold" and hold_above is not None and seconds <= hold_above + TIME_TOLERANCE_S:
                    problems.append(report(run, "E", "TIME-08", beat, "pause_after",
                                           f"{written}: a hold is above {seconds_text(hold_above)} s (pause_tiers)",
                                           f"Fix: write the tier its seconds fall in ({fitting or 'long'}), or make "
                                           f"the hold longer than {seconds_text(hold_above)} s.", place))
                    continue
            if tier == "hold" and not hold_is_saved(breakdown, beat, scene.identifier):
                above = f" above {seconds_text(hold_above)} s" if hold_above is not None else ""
                problems.append(report(run, "E", "TIME-08", beat, "pause_after",
                                       f"{written}: a hold{above} needs a saved choice, and no RESERVE with match: "
                                       f"pause_after = hold allows it here",
                                       "Fix: shorten it to long, or add the saved choice (a RESERVE with match: "
                                       "pause_after = hold whose allowed_in names this scene) and cite it in the "
                                       "shot's because.", place))
    return problems


# ---------------------------------------------------------------- TIME-06, TIME-07, TIME-09, TIME-10

@register_check("TIME-06", level="W", build=1, title="More than one main action per 4 s of moments",
                plain="packs in more actions than its length allows")
def check_time_06(run):
    """A moment is one main action (C3 R2 and L05: about one main action per 4 seconds of clip); a shot's moments
    may hold one per started stretch of main_actions_per_seconds' seconds, so 4 moments fit 15 seconds (WP12a's
    reading, which the gold's shot 150 follows). A shot marked compound: yes is exempt."""
    breakdown = breakdown_of(run)
    problems = []
    rule = constant(run.constants, "main_actions_per_seconds", None)
    if not isinstance(rule, dict) or not rule.get("per_s"):
        run.skip("TIME-06", "main_actions_per_seconds is missing from rules/constants.json")
        return problems
    actions, per_seconds = float(rule.get("actions", 1)), float(rule["per_s"])
    for scene in kept_scenes(run):
        for shot in breakdown.shots_of(scene.identifier):
            if normalise_word(shot.get("compound") or "no") == "yes":
                continue
            spans = [span for span in moment_spans(run, shot) if span[1] > span[0] >= 0]
            if not spans:
                continue
            covered = 0.0
            reach = None
            for start, end, _, _ in sorted(spans):
                if reach is None or start >= reach:
                    covered += end - start
                    reach = end
                elif end > reach:
                    covered += end - reach
                    reach = end
            allowed = max(actions, actions * math.ceil(covered / per_seconds - TIME_TOLERANCE_S))
            if len(spans) <= allowed:
                continue
            problems.append(report(run, "W", "TIME-06", shot, "moment",
                                   f"{len(spans)} moments in {seconds_words(covered)} s of moments: at most "
                                   f"{int(allowed)} main actions fit (one per {seconds_words(per_seconds)} s, "
                                   "main_actions_per_seconds)",
                                   "Fix: join moments that are one action, split the shot, or mark it compound: yes "
                                   "if the actions truly happen together.", place_of(run, shot, "moment")))
    return problems


@register_check("TIME-07", level="W", build=2,
                title="Film average shot length outside film_asl_range_s scaled by the home tone",
                plain="has an average shot length outside the range for the film's home tone")
def check_time_07(run):
    breakdown = breakdown_of(run)
    problems = []
    if run.scope_scenes is not None:
        run.skip("TIME-07", "the film's average shot length needs the whole film, and the project's scope is only "
                            "part of it")
        return problems
    if run.story is not None and run.story.excerpt:
        run.skip("TIME-07", "the film's average shot length needs the whole film: the other scenes are not in the "
                            "excerpt of the story given")
        return problems
    plan = run.record("PLAN")
    tone = normalise_word((plan.get("tone_home") if plan is not None else None)
                          or (run.project_record.get("tone_home") if run.project_record is not None else None) or "")
    band = constant(run.constants, "film_asl_range_s", None)
    if not tone or not isinstance(band, dict):
        run.skip("TIME-07", "no home tone yet (PLAN tone_home), or film_asl_range_s is missing")
        return problems
    if tone in band and isinstance(band[tone], list):
        low, high = band[tone]
        how = f"the {tone} range"
    else:
        base = next((value for value in band.values() if isinstance(value, list)), None)
        try:
            tones = load_json("rules/tone_defaults.json").get("tones", {})
        except (OSError, ValueError):
            tones = {}
        factor = (tones.get(tone) or {}).get("shot_length_factor")
        if base is None or factor is None:
            run.skip("TIME-07", f"no shot_length_factor for the home tone {tone} in rules/tone_defaults.json")
            return problems
        low, high = base[0] * factor, base[1] * factor
        how = f"{seconds_words(base[0])}-{seconds_words(base[1])} s scaled by {tone}'s shot_length_factor {factor}"
    times = []
    for scene in run.records("SCENE"):
        if not scene.identifier or not is_kept(scene):
            continue
        shots = breakdown.shots_of(scene.identifier)
        if not shots:
            run.skip("TIME-07", f"{scene.identifier} has no shots yet")
            return problems
        times += [number_of(shot.get("screen_time")) for shot in shots
                  if not shot_is_card_or_black(shot) and number_of(shot.get("screen_time")) is not None]
    if not times:
        return problems
    average = sum(times) / len(times)
    if low - TIME_TOLERANCE_S <= average <= high + TIME_TOLERANCE_S:
        return problems
    record = plan if plan is not None else run.project_record
    problems.append(report(run, "W", "TIME-07", record, "tone_home",
                           f"{tone}: the film's average shot length is {seconds_text(round(average, 2))} s over "
                           f"{len(times)} shots, outside {seconds_words(round(low, 2))}-{seconds_words(round(high, 2))} s "
                           f"({how}, film_asl_range_s)",
                           "Fix: bring the scenes' target_asl_s toward the range, or confirm the home tone with the "
                           "user.", place_of(run, record, "tone_home")))
    return problems


def point_position(breakdown, text):
    """(scene key, beat number or None) of a story point or a scene ID; None when it cannot be read."""
    text = (text or "").strip()
    point = parse_story_point(text)
    if point is None:
        return (scene_key(text), None) if SCENE_IDENTIFIER.match(text) else None
    scene_identifier, _, stored = point
    beat = stored
    if beat is None and breakdown.story is not None:
        beat = resolve_story_point(breakdown, text).beat
    return scene_key(scene_identifier), beat_order_number(beat)


def known_at(position, at):
    """True, False, or None when unknown: whether something known from position is known at position at."""
    if position is None or at is None:
        return None
    if position[0] != at[0]:
        return position[0] < at[0]
    if position[1] is None or at[1] is None:
        return None
    return position[1] <= at[1]


def shot_position(breakdown, shot):
    numbers = [beat_order_number(beat) for beat in breakdown.id_list(shot, "beats")]
    numbers = [number for number in numbers if number is not None]
    return scene_key(scene_of(shot.identifier)), (min(numbers) if numbers else None)


def average(values):
    return sum(values) / len(values) if values else None


@register_check("TIME-09", level="W", build=1,
                title="In a suspense_and_reveal scene, shots on the character who does not know the fact average "
                      "shorter than the scene's dialogue shots, with no why (A4 S2)",
                plain="cuts faster on the person who does not know what the audience knows than on the talk")
def check_time_09(run):
    """A shot is on a character when its focus subject is that character (inserts, cards and black left out). The
    character does not know the fact at that shot when the FACT's known_by has no entry for them, or one from a
    later beat, while the audience already knows it (audience_knows_from at or before the shot). Shots with a why
    are explained and left out of the average; the others are compared with the scene's dialogue shots (shots
    with a hear item)."""
    breakdown = breakdown_of(run)
    problems = []
    facts = run.records("FACT")
    if not facts:
        return problems
    for scene in kept_scenes(run):
        tags = {normalise_word(tag) for tag in split_list(scene.get("tags") or "")}
        if "suspense_and_reveal" not in tags:
            continue
        shots = breakdown.shots_of(scene.identifier)
        dialogue = [number_of(shot.get("screen_time")) for shot in shots
                    if breakdown.items(shot, "hear") and number_of(shot.get("screen_time")) is not None]
        dialogue_average = average(dialogue)
        if dialogue_average is None:
            continue
        # one line per character and cause: the facts they do not know are named together (the full run printed
        # the same short shots once per fact)
        by_character = {}
        for fact in facts:
            audience = point_position(breakdown, fact.get("audience_knows_from"))
            knowers = {}
            for item in breakdown.items(fact, "known_by"):
                knowers[element_of(item.first or "")] = point_position(breakdown, item.get("from"))
            unaware = {}
            for shot in shots:
                if is_insert_or_card(shot):
                    continue
                subject = focus_subject(breakdown, shot)
                if subject is None:
                    continue
                character = element_of(subject.first or "")
                if not character.startswith("CH-") or is_non_human(breakdown, character):
                    continue  # a creature is not the one the audience waits for to learn a fact
                at = shot_position(breakdown, shot)
                if known_at(audience, at) is not True:
                    continue
                knows = known_at(knowers[character], at) if character in knowers else False
                if knows is not False:
                    continue
                unaware.setdefault(character, []).append(shot)
            for character, found in unaware.items():
                unexplained = [shot for shot in found if not (shot.get("why") or "").strip()
                               and number_of(shot.get("screen_time")) is not None]
                if not unexplained:
                    continue
                unaware_average = average([number_of(shot.get("screen_time")) for shot in unexplained])
                if unaware_average + TIME_TOLERANCE_S >= dialogue_average:
                    continue
                key = (character, tuple(shot.identifier for shot in unexplained))
                entry = by_character.setdefault(key, {"facts": [], "average": unaware_average})
                entry["facts"].append(fact.identifier)
        for (character, shot_names), entry in by_character.items():
            facts_named = entry["facts"]
            problems.append(report(run, "W", "TIME-09", scene, "tags",
                                   f"suspense_and_reveal: the shots on {character}, who does not know "
                                   f"{' or '.join(facts_named) if len(facts_named) <= 2 else ', '.join(facts_named)} "
                                   f"yet, average {seconds_text(round(entry['average'], 2))} s ({', '.join(shot_names)}),"
                                   f" shorter than the scene's dialogue shots ({seconds_text(round(dialogue_average, 2))}"
                                   " s), and none gives a why (A4 S2)",
                                   f"Fix: hold longer on {character} while the audience knows and they do not, or "
                                   "give those shots a why; if the fact's known_by is wrong (they do know it), say so "
                                   "in the report: the story plan's facts are corrected there, not in the shots.",
                                   place_of(run, scene, "tags")))
    return problems


def is_non_human(breakdown, character):
    """True for a character of tier non_human that has no voice and says nothing (the animal in The Catch). Marking
    a speaking character non_human does not take it out of the checks: its voice or its speeches keep it a person."""
    record = breakdown.record(character, "CHARACTER")
    if record is None or normalise_word(record.get("tier") or "") != "non_human":
        return False
    if normalise_word(record.get("voice") or "none") not in ("none", ""):
        return False
    if any(voice.get("character") == character for voice in breakdown.records_of("VOICE")):
        return False
    speeches = getattr(breakdown, "speeches", None) or {}
    return not any(isinstance(entry, dict) and entry.get("speaker") == character for entry in speeches.values())


@register_check("TIME-10", level="W", build=2,
                title="The main turn's shot is neither the longest nor the shortest shot of its scene (A4 R4)",
                plain="is the main turn's shot but neither the longest nor the shortest in its scene")
def check_time_10(run):
    breakdown = breakdown_of(run)
    problems = []
    for scene in kept_scenes(run):
        main_turns = [beat.identifier for beat in breakdown.beats_of(scene.identifier)
                      if normalise_word(beat.get("turn") or "") == "main_turn"]
        if not main_turns:
            continue
        shots = [shot for shot in breakdown.shots_of(scene.identifier)
                 if not shot_is_card_or_black(shot) and number_of(shot.get("screen_time")) is not None]
        if len(shots) < 3:
            continue
        times = [number_of(shot.get("screen_time")) for shot in shots]
        shortest, longest = min(times), max(times)
        for shot in shots:
            if normalise_word(shot.get("role") or "") != "turn":
                continue
            if not set(main_turns) & set(breakdown.id_list(shot, "beats")):
                continue
            time = number_of(shot.get("screen_time"))
            if shortest + TIME_TOLERANCE_S < time < longest - TIME_TOLERANCE_S:
                problems.append(report(run, "W", "TIME-10", shot, "screen_time",
                                       f"{seconds_words(time)} is neither the scene's longest shot "
                                       f"({seconds_words(longest)} s) nor its shortest ({seconds_words(shortest)} s): "
                                       "a peak must be an extreme (A4 R4)",
                                       "Fix: hold it longest for a realisation, a decision or a refusal, or make it "
                                       "shortest for a physical event.", place_of(run, shot, "screen_time")))
    return problems


# ---------------------------------------------------------------- states (STATE-01 to STATE-04)

def compare_positions(first, second):
    """-1, 0 or 1 comparing two (scene key, line) positions, or None when the order cannot be known."""
    if first is None or second is None:
        return None
    if first[0] != second[0]:
        return -1 if first[0] < second[0] else 1
    if first[1] is None or second[1] is None:
        return None
    return (first[1] > second[1]) - (first[1] < second[1])


def state_start(breakdown, state):
    scene_identifier, line = state_from(breakdown, state)
    if not scene_identifier:
        return None
    return scene_key(scene_identifier), line


def element_states(breakdown, element):
    """An element's STATE records in story order (scene, then line, then ID)."""
    key = ("wp4c element states", element)
    if key in breakdown._cache:
        return breakdown._cache[key]

    def order(state):
        start = state_start(breakdown, state)
        if start is None:
            return (10 ** 6, ""), -1, sort_key_for_identifier(state.identifier)
        return start[0], start[1] if start[1] is not None else -1, sort_key_for_identifier(state.identifier)

    found = sorted((state for state in breakdown.records_of("STATE")
                    if (state.get("element") or element_of(state.identifier)) == element), key=order)
    breakdown._cache[key] = found
    return found


def state_interval(breakdown, element, state):
    """(start, end, following state): the state holds from start until the next state of its element starts."""
    states = element_states(breakdown, element)
    start = state_start(breakdown, state)
    for index, other in enumerate(states):
        if other.identifier == state.identifier and index + 1 < len(states):
            following = states[index + 1]
            return start, state_start(breakdown, following), following
    return start, None, None


def state_at(breakdown, element, position):
    """The element's state that surely holds at a position, or None."""
    chosen = None
    for state in element_states(breakdown, element):
        order = compare_positions(state_start(breakdown, state), position)
        if order in (-1, 0):
            chosen = state
        elif order is None and chosen is None:
            return None
    return chosen


def shot_span(breakdown, shot):
    numbers = breakdown.lines_of(shot)
    key = scene_key(scene_of(shot.identifier))
    if numbers:
        return (key, min(numbers)), (key, max(numbers))
    return (key, None), (key, None)


def state_start_words(breakdown, state):
    """Where a state starts, in words: 'SC10 line 408', or 'the start of SC10' when no line is known."""
    scene_identifier, line = state_from(breakdown, state)
    return f"{scene_identifier} line {line}" if line is not None else f"the start of {scene_identifier}"


def shot_lines_words(first, last):
    if first[1] is None:
        return "its lines"
    return f"lines {first[1]}-{last[1]}" if last[1] != first[1] else f"line {first[1]}"


@register_check("STATE-01", level="E", build=1, title="A subject or thing without a state valid for this scene",
                plain="shows a person or thing in a state they are not in at that point")
def check_state_01(run):
    """5.4 rule 4: subject and thing items name a state ID when the element has states, and the state must be
    valid there (its from at or before the shot, its until after). A shot is read as its lines: a state that holds
    during any of them fits, so a shot that shows a change may name either state; a state replaced on the shot's
    first line no longer holds there. An element with no states at all is named directly (rule 4), and motifs and
    text are not elements. The same rule reads the one-line list's subjects at step 7 (a list item may name the
    character instead of its state), so a list subject step 7 accepts is one step 8 accepts too (C10)."""
    breakdown = breakdown_of(run)
    problems = []
    for scene in kept_scenes(run):
        for shot in breakdown.shots_of(scene.identifier):
            first, last = shot_span(breakdown, shot)
            for field_name in ("subject", "thing"):
                for item in breakdown.items(shot, field_name):
                    item_first, item_last = first, last
                    recorded = recorded_position(run, breakdown, item.get("recorded"))
                    if recorded is not None:
                        # footage from an earlier time: the state that held when it was recorded
                        item_first, item_last = recorded
                    problems.extend(state_reference_problems(run, breakdown, scene, shot, field_name,
                                                             (item.first or "").strip(), item_first, item_last))
        shot_list = run.record(f"{scene.identifier}-LIST")
        if shot_list is None or shot_list.type_name != "SHOTLIST":
            continue
        definition = run.schema.field("SHOTLIST", "item")
        for value in shot_list.get_all("item"):
            item = split_item(value, definition)
            first, last = list_item_span(run, breakdown, scene, item)
            if first[1] is None:
                continue
            for reference in split_list(item.get("subject") or ""):
                reference = reference.strip()
                if not STATE_REFERENCE.match(reference):
                    continue  # a list item may name the character; its shot names the state
                problems.extend(state_reference_problems(run, breakdown, scene, shot_list, "item",
                                                         reference, first, last, item_label=item.first))
    return problems


def recorded_position(run, breakdown, value):
    """((scene key, line), (scene key, line)) of a subject's or thing's `recorded` sub-part (footage from an earlier
    time): a story point ('SC06 "The cage drops."') gives its line; a scene ID alone gives the whole scene (footage
    from some time in it: any state that held during the scene fits, as for a shot's own lines). None when there is
    no such sub-part or it names no scene."""
    value = (value or "").strip()
    if not value or normalise_word(value) in ("none", "no"):
        return None
    parsed = parse_story_point(value)
    if parsed:
        scene_identifier = parsed[0]
        line = None
        if run.story is not None:
            line = resolve_story_point(breakdown, value).line
        position = (scene_key(scene_identifier), line)
        return position, position
    match = re.search(r"\bSC\d{2,3}[A-Z]?\b", value)
    if not match:
        return None
    span = breakdown.scene_range(match.group(0))
    key = scene_key(match.group(0))
    if not span:
        return (key, None), (key, None)
    return (key, span[0]), (key, span[1])


def list_item_span(run, breakdown, scene, item):
    """(first, last) positions of a one-line list item: the lines of the beats it covers."""
    numbers = []
    for beat_identifier in split_list(item.get("beats") or ""):
        beat = breakdown.record(beat_identifier.strip(), "BEAT")
        if beat is not None:
            numbers.extend(breakdown.lines_of(beat))
    key = scene_key(scene.identifier)
    if not numbers:
        return (key, None), (key, None)
    return (key, min(numbers)), (key, max(numbers))


def state_reference_problems(run, breakdown, scene, record, field_name, reference, first, last, item_label=None):
    """STATE-01's lines for one subject or thing reference of a shot (or of a list item) covering first..last."""
    problems = []
    where = f" (list item {item_label})" if item_label else ""
    place = place_of(run, record, field_name, first_part=item_label or reference)
    if STATE_REFERENCE.match(reference):
        state = breakdown.record(reference, "STATE")
        if state is None:
            return problems  # ID-02 reports a state that does not exist
        element = state.get("element") or element_of(reference)
        start, end, following = state_interval(breakdown, element, state)
        valid = state_at(breakdown, element, first)
        fix = f"Fix: name {valid.identifier}." if valid is not None and valid is not state else \
            f"Fix: name the state of {element} that holds here, or correct the states' from lines."
        if compare_positions(start, last) == 1:
            problems.append(report(run, "E", "STATE-01", record, field_name,
                                   f"{reference}{where} is not valid here: it starts at "
                                   f"{state_start_words(breakdown, state)}, after this shot "
                                   f"({shot_lines_words(first, last)})", fix, place))
        elif end is not None and compare_positions(end, first) in (-1, 0):
            problems.append(report(run, "E", "STATE-01", record, field_name,
                                   f"{reference}{where} is not valid here: {following.identifier} replaces "
                                   f"it from {state_start_words(breakdown, following)}, at or before the start of "
                                   f"this shot ({shot_lines_words(first, last)})", fix, place))
    elif ELEMENT_REFERENCE.match(reference) and item_label is None:
        states = element_states(breakdown, reference)
        if not states:
            return problems
        valid = state_at(breakdown, reference, first)
        if valid is not None:
            problems.append(report(run, "E", "STATE-01", record, field_name,
                                   f"{reference} names the element, but it has states: the one valid "
                                   f"here ({shot_lines_words(first, last)}) is {valid.identifier}",
                                   f"Fix: write {valid.identifier}.", place))
        elif compare_positions(state_start(breakdown, states[0]), first) == 1:
            problems.append(report(run, "E", "STATE-01", record, field_name,
                                   f"{reference} has no state valid here: its first state, "
                                   f"{states[0].identifier}, starts at "
                                   f"{state_start_words(breakdown, states[0])}, after this shot",
                                   f"Fix: write a STATE of {reference} from {scene.identifier} with this unit (an "
                                   f"addition: its next free state number, origin: invented, listed in the scene's "
                                   f"additions), or, for footage of an earlier time, add '| recorded: <scene>'.",
                                   place))
    return problems


def cause_line(run, cause_first):
    """(line number or None, why not found or None) of a cause's first part: a line number, or a quote anchor
    found once in the whole story (WP12a's adopt rule for single-line references)."""
    ranges = parse_line_numbers(cause_first or "")
    if ranges:
        return ranges[0][0], None
    if parse_quote_anchor(cause_first or ""):
        found = run.story.numbered.resolve_line(cause_first)
        if found is None:
            return None, "its quote anchor is not found exactly once in the story"
        return found, None
    return None, "it is neither a line number nor a quote anchor"


@register_check("STATE-02", level="E", build=1, title="A state without a cause line found in the story",
                plain="has no story line that causes it")
def check_state_02(run):
    """The cause is required from Standard depth (5.5), and an invented state is exempt from having one. A cause's
    line must be a story line (not blank), and its quote, when written, must be on that line."""
    problems = []
    for state in run.records("STATE"):
        cause = state.get("cause")
        origin = normalise_word(state.get("origin") or "story")
        place = place_of(run, state, "cause")
        if not cause or normalise_word(cause) == "none":
            if origin != "invented" and run.depth_rank(state) >= 2:
                problems.append(report(run, "E", "STATE-02", state, "cause",
                                       "is missing: a state needs the story line that causes it",
                                       "Fix: write cause: <line> | quote: \"<the words on that line>\" (or mark the "
                                       "state origin: invented).", place_of(run, state, "from")))
            continue
        if run.story_missing("STATE-02"):
            continue  # a missing cause is still reported for the other states
        item = split_item(cause)
        line, why_not = cause_line(run, item.first)
        if line is None:
            if why_not and "not found" in why_not and run.story.excerpt:
                run.skip("STATE-02", f"{state.identifier}: its cause is not in the excerpt of the story given")
                continue
            problems.append(report(run, "E", "STATE-02", state, "cause",
                                   f"{cause}: the cause line cannot be found: {why_not}",
                                   "Fix: write the cause's line number, or a quote of 3 or more words found once in "
                                   "the story.", place))
            continue
        if not run.story.holds(line):
            run.skip("STATE-02", f"{state.identifier}: its cause line {line} is not in the excerpt of the story given")
            continue
        numbered = run.story.numbered
        if not numbered.line(line).strip():
            problems.append(report(run, "E", "STATE-02", state, "cause",
                                   f"{cause}: line {line} is blank",
                                   "Fix: point the cause at the story line that causes the state.", place))
            continue
        quote = (item.get("quote") or "").strip().strip('"“”')
        if quote and not numbered.find_quote(quote, line, line):
            elsewhere = numbered.find_quote(quote)
            hint = f" (it is on line {elsewhere[0]})" if len(elsewhere) == 1 else ""
            problems.append(report(run, "E", "STATE-02", state, "cause",
                                   f"{cause}: the quote is not on line {line}{hint}",
                                   "Fix: correct the cause's line, or quote the words that line holds.", place))
    return problems


def is_continuous(scene):
    words = " ".join([scene.get("time_text") or "", scene.get("heading") or ""]).upper()
    return "CONTINUOUS" in words or normalise_word(scene.get("transition_in") or "") == "continuous"


@register_check("STATE-03", level="E", build=1,
                title="A CONTINUOUS scene whose entry state differs from the previous exit with no cause",
                plain="follows straight on from the scene before, but someone starts it changed with no cause")
def check_state_03(run):
    breakdown = breakdown_of(run)
    problems = []
    all_scenes = sorted((scene for scene in run.records("SCENE") if scene.identifier),
                        key=lambda scene: scene_key(scene.identifier))
    for scene in kept_scenes(run):
        if not is_continuous(scene):
            continue
        earlier = [other for other in all_scenes if scene_key(other.identifier) < scene_key(scene.identifier)]
        if not earlier:
            continue
        previous = earlier[-1]
        if run.story is not None and not run.story.excerpt:
            story_scenes = sorted(run.story.numbered.scenes, key=scene_key)
            before = [identifier for identifier in story_scenes if scene_key(identifier) < scene_key(scene.identifier)]
            if before and not same_scene(before[-1], previous.identifier):
                run.skip("STATE-03", f"{scene.identifier}: the scene before it, {before[-1]}, has no record here")
                continue
        this_span = breakdown.scene_range(scene.identifier)
        previous_span = breakdown.scene_range(previous.identifier)
        entry = (scene_key(scene.identifier), this_span[0] if this_span else None)
        exit_position = (scene_key(previous.identifier), previous_span[1] if previous_span else None)
        shared = [element for element in elements_present(breakdown, scene.identifier)
                  if element in elements_present(breakdown, previous.identifier)]
        for element in shared:
            entering = state_at(breakdown, element, entry)
            leaving = state_at(breakdown, element, exit_position)
            if entering is None or leaving is None or entering is leaving:
                continue
            cause = entering.get("cause")
            if cause and normalise_word(cause) != "none":
                continue
            problems.append(report(run, "E", "STATE-03", scene, "time_text",
                                   f"{scene.identifier} runs straight on from {previous.identifier}, but {element} "
                                   f"enters in {entering.identifier} and left {previous.identifier} in "
                                   f"{leaving.identifier}, and {entering.identifier} has no cause",
                                   f"Fix: give {entering.identifier} a cause (the story line that changes {element}), "
                                   f"or start {element} in {leaving.identifier}.", place_of(run, scene, "time_text")))
    return problems


@register_check("STATE-04", level="W", build=2, title="Consecutive shots of one subject disagree on end and start",
                plain="ends differently from how the next shot of the same person starts")
def check_state_04(run):
    run.skip("STATE-04", "build 2: comparing a shot's end with the next shot's start needs a reading of free text; "
                         "it is added when the test runs show this error happens")
    return []
