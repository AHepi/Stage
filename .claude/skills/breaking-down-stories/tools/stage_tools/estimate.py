"""estimate.py: how long the film runs, how many shots it has, and what making it with AI video costs in money and in
the user's own hours (blueprint 7.1 and 5.6 "Estimates"; research file D13, formulas E1 to E11).

What this file does, in plain words:
- the first estimate (D13 version v0, "the first estimate" to the user), from the words of the story: each scene's
  seconds are its spoken words at the speaking pace, half a second for each speech, a second for each "(beat)",
  plus its action words at v0_action_seconds_per_word (low and high); its shots are its seconds divided by the
  average shot length of its pace class (SCENE rhythm_class, rhythm_class_asl_s) times its tone's shot-length
  factor (_config/rules/tone_defaults.json); its takes, pictures and minutes follow D13's class shares;
- the estimate from the shots (D13 version v1, "the estimate from the shots"): each SHOT's screen time, cost class,
  clip length (screen time plus handles_s at each end, rounded up to a length the model allows and never under the
  shortest clip), plates for text in picture and screens, storyboard frames and grey preview work. A scene whose
  shots are not written yet uses its one-line shot list, and a scene with neither keeps the first estimate (D13 R2);
- for a prose project at the story plan, each macro plan (PLAN plan_option) is estimated at its runtime;
- money by price level (budget, mid, premium; the mixed plan once shot sizes exist): video takes (E7), pictures,
  upscaling, voices and sound effects, music (by the music policy, D13 R24), the AI assistant's months, editing
  software and contingency (E8); the user's hours, base, central and high (E9), and weeks at their hours a week
  (E10); warnings for the page check (E3), the average shot length (E4), the generation factor (E6), the runtime
  target (E1, E2) and a long calendar (D13 R17);
- prices come from _config/adapters/prices.json with their date. When they are older than model_facts_max_age_days, no money
  is printed, written or stored anywhere until the prices are refreshed (D13 R7, E11);
- writes "14 Time and cost.md" (plain words for the user) and "For machines - do not edit/estimate.json" (the D13
  estimate blocks, film and scene). The command also stores the code-owned fields the estimate fills: SCENE
  target_duration_s, PLAN runtime_estimate, scene_budget and shot_budget (first estimate only) and PROJECT
  model_facts_date. A locked record only gains a field it lacks; its values are never changed;
- registers the command estimate, and offers write_first_estimate(project_folder), which stage.py read calls
  after reading the story (it writes the two estimate files and never touches a record file).

Other modules may use: film_estimate(breakdown, version, on=None, prices=None), PriceTable, ShotWork, scene_block,
seconds_from_words, render_time_and_cost, estimate_as_json, write_first_estimate, use_today.

Every number comes from _config/rules/constants.json (speech_wps_default, speech_floor_extra_s, pause_tiers, handles_s,
v0_action_seconds_per_word, rhythm_class_asl_s, model_facts_max_age_days, film_asl_range_s, short_runtime_max_s,
page_eighths_line_model, scene_total_tolerance) or from _config/adapters/prices.json (prices and D13's work defaults).

Standard library only.

After the full run on The Catch (Project notes 31 and 32):
- one film length: the story's, then with titles and credits.

After the second full run (Project notes 39 and 40):
- the weeks are rounded before they are compared; the page check names the estimate from the story's words; a scene's
  planned length is called its first estimate; a film longer than the short film the user chose is warned about.
"""

import datetime
import json
import math
import os
import re
from dataclasses import dataclass, field as dataclass_field
from pathlib import Path

from .record_format import TONE_DEFAULTS_FILE, adapter_file, load_json, normalise_word, split_item, split_list

PRICES_FILE = adapter_file("prices.json")
TIME_AND_COST_FILE = "14 Time and cost.md"
MACHINE_FOLDER = "For machines - do not edit"
ESTIMATE_JSON_FILE = "estimate.json"
START_HERE = "00 Start here.md"
SCENES_FOLDER = "11 Scenes"

COST_CLASSES = ("graphic", "reuse", "still_move", "easy", "dialogue", "hard")
SHARE_CLASSES = ("still_move", "easy", "dialogue", "hard")
PRICE_LEVELS = ("budget", "mid", "premium")
RHYTHM_CLASSES = ("action_peak", "suspense", "mixed", "dialogue", "contemplative")
CLOSE_SIZES = ("medium_close_up", "close_up", "extreme_close_up")
NOT_KEPT = ("merge", "fold", "cut")
CARD_KINDS = ("card", "black")
RECORDED_VOICE_SOURCES = ("user_recorded", "actor_recorded")
VERSION_NAMES = {"v0": "v0_words", "v1": "v1_shot_list"}

CLASS_WORDS = {"graphic": ("graphic or card", "graphics or cards"), "reuse": ("reused shot", "reused shots"),
               "still_move": ("still with a slow move", "stills with a slow move"),
               "easy": ("easy shot", "easy shots"), "dialogue": ("dialogue shot", "dialogue shots"),
               "hard": ("hard shot", "hard shots")}
PACE_WORDS = {"action_peak": "an action peak", "suspense": "a suspense", "mixed": "a mixed", "dialogue": "a dialogue",
              "contemplative": "a contemplative"}
LEVEL_WORDS = {"budget": "Budget", "mid": "Mid", "premium": "Premium", "mixed": "Mixed plan"}
MONEY_LINES = (("video", "Video takes"),
               ("pictures", "Pictures (reference pictures, storyboard frames, start pictures)"),
               ("upscale", "Upscaling"),
               ("voices_and_effects", "Voices and sound effects"),
               ("music", "Music"),
               ("assistant", "AI assistant plan"),
               ("software", "Editing software"),
               ("contingency", "Contingency"),
               ("total", "Total"))

SCENE_IDENTIFIER = re.compile(r"^SC(\d{2,3})([A-Z]?)$")
SCENE_OF = re.compile(r"^(SC\d{2,3}[A-Z]?)(?:-|$)")
SHOT_NUMBER = re.compile(r"-SH(\d+)$")
NUMBER_IN_TEXT = re.compile(r"-?\d+(?:\.\d+)?")

_TODAY = {"date": None}


# ---------------------------------------------------------------- small helpers

def today():
    """Today's date; tests may set another with use_today(date)."""
    return _TODAY["date"] or datetime.date.today()


def use_today(date):
    """Use this date as today (a datetime.date, an ISO text, or None to go back to the clock). For tests only."""
    if isinstance(date, str):
        date = datetime.date.fromisoformat(date)
    _TODAY["date"] = date


def read_date(text):
    try:
        return datetime.date.fromisoformat(str(text).strip()[:10])
    except (TypeError, ValueError):
        return None


def constant(constants, name, default=None):
    """The value of a named constant of _config/rules/constants.json (either table), or default."""
    if not constants:
        return default
    for section in (constants.get("constants", {}), constants.get("from_blueprint_text", {}).get("constants", {})):
        if name in section:
            entry = section[name]
            return entry.get("value", default) if isinstance(entry, dict) else entry
    return default


def number_of(text, default=None):
    """The first number in a value ('15', '15 s', '2.0'), or default."""
    if text is None:
        return default
    if isinstance(text, (int, float)):
        return float(text)
    match = NUMBER_IN_TEXT.search(str(text))
    return float(match.group(0)) if match else default


def is_none_word(value):
    return value is None or normalise_word(str(value)) in ("", "none", "open", "auto", "null", "n_a")


def scene_of(identifier):
    match = SCENE_OF.match(identifier or "")
    return match.group(1) if match else None


def scene_key(identifier):
    match = SCENE_IDENTIFIER.match(identifier or "")
    return (int(match.group(1)), match.group(2)) if match else (10 ** 6, identifier or "")


def shot_key(identifier):
    match = SHOT_NUMBER.search(identifier or "")
    return (scene_key(scene_of(identifier)), int(match.group(1)) if match else 0)


def scene_words(identifier):
    """SC10 -> 'scene 10', SC06A -> 'scene 6A', SC104 -> 'scene 104'."""
    match = SCENE_IDENTIFIER.match(identifier or "")
    if not match:
        return identifier or "a scene"
    return f"scene {int(match.group(1))}{match.group(2)}"


def shot_words(identifier):
    match = SHOT_NUMBER.search(identifier or "")
    number = f"shot {int(match.group(1)):03d}" if match else "a shot"
    return f"{number} of {scene_words(scene_of(identifier))}"


def whole(value):
    """12345.6 -> '12,346'."""
    return f"{int(round(value)):,}"


def dollars(value):
    return f"${int(round(value)):,}"


def one_place(value):
    text = f"{value:.1f}"
    return text[:-2] if text.endswith(".0") else text


def plural(count, word, many=None):
    rounded = int(round(count))
    return f"{whole(count)} {word if rounded == 1 else (many or word + 's')}"


def sentence_case(text):
    text = (text or "").strip()
    if not text:
        return ""
    lowered = text.lower()
    return lowered[0].upper() + lowered[1:]


def full_stop(text):
    """A note as a sentence: capital first letter, full stop at the end."""
    text = (text or "").strip()
    if not text:
        return text
    text = text[0].upper() + text[1:]
    return text if text[-1] in ".!?:" else text + "."


def weeks_text(value):
    return one_place(value) if value < 10 else whole(value)


# ---------------------------------------------------------------- the price table

class PriceTable:
    """_config/adapters/prices.json: prices with their date and page, and D13's work defaults (takes, minutes, shares)."""

    def __init__(self, data, path=None):
        self.data = data or {}
        self.path = path

    @classmethod
    def load(cls, skill_folder=None):
        """(PriceTable, None), or (None, a plain reason) when the file is missing or unreadable."""
        try:
            return cls(load_json(PRICES_FILE, skill_folder), PRICES_FILE), None
        except FileNotFoundError:
            return None, f"the price table ({PRICES_FILE}) is not in this copy of the tools"
        except (OSError, ValueError) as error:
            return None, f"the price table ({PRICES_FILE}) could not be read ({type(error).__name__})"

    @property
    def date(self):
        return read_date(self.data.get("price_date") or self.data.get("checked_on"))

    def age_days(self, on):
        return None if self.date is None else (on - self.date).days

    def section(self, name):
        return self.data.get(name) or {}

    @property
    def work(self):
        return self.section("work_defaults")

    def minutes(self, name, default=0.0):
        value = self.work.get("minutes", {}).get(name, default)
        return value

    def class_work(self, cost_class):
        return self.work.get("cost_classes", {}).get(cost_class) or {}

    def class_shares(self, rhythm_class):
        shares = self.work.get("first_estimate_class_shares", {})
        return shares.get(rhythm_class) or shares.get(self.default_rhythm_class) or {}

    @property
    def default_rhythm_class(self):
        return self.work.get("default_rhythm_class", "mixed")

    def video_price(self, level):
        return float(self.section("video").get(level, {}).get("per_s", 0.0))

    @property
    def draft_price(self):
        return self.video_price("draft")

    @property
    def min_clip_s(self):
        return float(self.section("video").get("min_clip_s", 0) or 0)

    @property
    def hard_action_peak_clip_s(self):
        return float(self.section("video").get("hard_action_peak_clip_s", 0) or 0)

    def image(self, name, default=0.0):
        return float(self.section("image").get(name, default) or 0)

    def upscale(self, name, default=0.0):
        return float(self.section("upscale").get(name, default) or 0)

    def plan(self, name):
        return self.section("plans").get(name) or {}

    def credits(self, name, default=0.0):
        return float(self.section("credits").get(name, default) or 0)

    def level(self, level):
        return self.section("price_levels").get(level) or {}

    def warning_band(self, name, default=None):
        return self.work.get("warning_bands", {}).get(name, default)


def load_tone_factors(skill_folder=None):
    """{tone: shot_length_factor} from _config/rules/tone_defaults.json (D10 §2.2), or {} when the file is missing."""
    try:
        tones = load_json(TONE_DEFAULTS_FILE, skill_folder).get("tones", {})
    except (OSError, ValueError):
        return {}
    return {name: float(row.get("shot_length_factor", 1.0) or 1.0) for name, row in tones.items()
            if isinstance(row, dict)}


# ---------------------------------------------------------------- one shot's work, one scene's block

@dataclass
class ShotWork:
    """The work one shot needs for the estimate (or a share of one: weight under 1 in the first estimate, or when a
    shot has no cost class yet and takes its scene's class shares)."""
    identifier: str
    cost_class: str
    screen_time_s: float
    clip_lengths_s: list
    plates: float = 0.0
    plate_clip_s: float = None
    weight: float = 1.0
    storyboard: bool = True
    previs_minutes: float = 0.0
    dialogue_close: bool = False
    note: str = ""

    @property
    def clip_length_s(self):
        """Seconds one take bills: the clip, or the clips added up when the shot is split."""
        return float(sum(self.clip_lengths_s))

    @property
    def plate_length_s(self):
        return float(self.plate_clip_s if self.plate_clip_s is not None else self.clip_length_s)


def clip_length_for(screen_time_s, prices, handles_s, lengths=None, minimum=None):
    """D13 §6.2 and E5: the larger of the shortest clip and screen time plus a handle at each end, rounded up to a
    length the model allows (whole seconds when no model is chosen)."""
    needed = screen_time_s + 2 * handles_s
    if lengths:
        for value in sorted(lengths):
            if value + 1e-9 >= needed:
                return float(value)
        return float(math.ceil(needed - 1e-9))
    shortest = prices.min_clip_s if minimum is None else minimum
    return float(max(shortest, math.ceil(needed - 1e-9)))


@dataclass
class SceneBlock:
    """One scene's estimate (D13 §11.2's scene block): runtime, shots by class, generated seconds, the scene's share of
    money (video takes and its pictures) and of hours."""
    identifier: str
    label: str
    basis: str                      # words, shots, list, planned_length, plan, none
    rhythm_class: str
    average_shot_s: float
    runtime_s: tuple                # (low, central, high)
    shots: dict = dataclass_field(default_factory=dict)
    plates: float = 0.0
    draft_s: float = 0.0
    final_s: float = 0.0
    video_money: dict = None        # {budget, mid, premium, mixed}
    pictures_money: float = 0.0
    storyboards: float = 0.0
    start_pictures: float = 0.0
    minutes: dict = dataclass_field(default_factory=dict)
    upscale_whole_takes_s: float = 0.0
    target_s: float = None
    notes: list = dataclass_field(default_factory=list)
    example: str = ""
    counts: dict = None

    @property
    def total_shots(self):
        return sum(self.shots.values())

    @property
    def generated_s(self):
        return self.draft_s + self.final_s

    @property
    def base_minutes(self):
        return sum(self.minutes.values())


def scene_block(identifier, label, works, runtime_s, prices, basis="shots", rhythm_class="", average_shot_s=0.0,
                money_shown=True, extra_previs_minutes=0.0):
    """E5 to E7 and the scene's hours (D13 §11.1, §15.1): shots by class, draft and final generated seconds, video
    money at each price level, the scene's pictures and its minutes."""
    block = SceneBlock(identifier, label, basis, rhythm_class, average_shot_s, tuple(runtime_s))
    for name in COST_CLASSES:
        block.shots[name] = 0.0
    draft_price = prices.draft_price
    levels = {level: prices.video_price(level) for level in PRICE_LEVELS}
    finals_by_level = {level: 0.0 for level in PRICE_LEVELS}
    mixed_finals_money = 0.0
    storyboard_price = prices.image("storyboard_try") * prices.image("storyboard_tries_per_shot", 1)
    start_picture_price = prices.image("start_picture_per_shot")
    minutes = {"storyboard frames": 0.0, "start pictures": 0.0, "grey previews": float(extra_previs_minutes),
               "preparing jobs": 0.0, "watching takes": 0.0, "making graphics": 0.0, "compositing": 0.0,
               "editing, sound and grade": 0.0}
    for work in works:
        cost_class = work.cost_class if work.cost_class in COST_CLASSES else "easy"
        rules = prices.class_work(cost_class)
        weight = work.weight
        block.shots[cost_class] += weight
        plates = weight * work.plates
        block.plates += plates
        draft = weight * work.clip_length_s * rules.get("draft_takes", 0)
        final_takes_s = weight * work.clip_length_s * rules.get("final_takes", 0)
        plate_s = plates * work.plate_length_s
        block.draft_s += draft
        block.final_s += final_takes_s + plate_s
        for level in PRICE_LEVELS:
            finals_by_level[level] += (final_takes_s + plate_s) * levels[level]
        mixed_level = "premium" if (cost_class == "dialogue" and work.dialogue_close) else "mid"
        mixed_finals_money += (final_takes_s + plate_s) * levels[mixed_level]
        if rules.get("video"):
            block.upscale_whole_takes_s += weight * work.clip_length_s
        block.upscale_whole_takes_s += plate_s
        storyboard = weight if (work.storyboard and cost_class not in ("graphic", "reuse")) else 0.0
        block.storyboards += storyboard
        start_pictures = weight * rules.get("start_pictures", 0)
        block.start_pictures += start_pictures
        minutes["storyboard frames"] += storyboard * prices.minutes("storyboard_pick")
        minutes["start pictures"] += start_pictures * prices.minutes("start_picture")
        minutes["grey previews"] += weight * work.previs_minutes
        minutes["preparing jobs"] += weight * (prices.minutes("job_preparation") if rules.get("video") else 0.0)
        minutes["watching takes"] += weight * rules.get("review_minutes", 0)
        minutes["making graphics"] += weight * rules.get("make_minutes", 0)
        minutes["compositing"] += plates * prices.minutes("compositing_plate")
    post = prices.minutes("post_per_finished_minute", {})
    post_per_minute = sum(post.values()) if isinstance(post, dict) else float(post or 0)
    minutes["editing, sound and grade"] = post_per_minute * block.runtime_s[1] / 60.0
    block.minutes = minutes
    block.pictures_money = block.storyboards * storyboard_price + block.start_pictures * start_picture_price
    if money_shown:
        draft_money = block.draft_s * draft_price
        block.video_money = {level: draft_money + finals_by_level[level] for level in PRICE_LEVELS}
        block.video_money["mixed"] = draft_money + mixed_finals_money
    return block


# ---------------------------------------------------------------- the first estimate from words (D13 §4.1)

def seconds_from_words(counts, constants):
    """(low, central, high) seconds of one scene from its word counts: speech words at speech_wps_default, plus
    speech_floor_extra_s a speech and the "(beat)" pause a beat mark, plus action words at v0_action_seconds_per_word."""
    pace = float(constant(constants, "speech_wps_default", 2.5))
    per_speech = float(constant(constants, "speech_floor_extra_s", 0.5))
    pause = (constant(constants, "pause_tiers", {}) or {}).get("script_words", {}).get("(beat)", 1.0)
    low_rate, high_rate = constant(constants, "v0_action_seconds_per_word", [0.166, 0.22])
    speech = (counts.get("dialogue_words", 0) / pace + per_speech * counts.get("speeches", 0)
              + float(pause) * counts.get("beat_marks", 0))
    action = counts.get("action_words", 0)
    low = speech + action * float(low_rate)
    high = speech + action * float(high_rate)
    return (low, (low + high) / 2, high)


def works_from_shares(identifier, shots, rhythm_class, average_shot_s, prices, handles_s, first_estimate=True):
    """The first estimate's shots of one scene as class shares (D13 §6.1): still, easy, dialogue and hard shots of
    average length, each with its clip (D13 §6.2: the pace's clip, and 7 seconds for a hard shot in an action peak),
    plates spread evenly (billed at the pace's clip) and grey previews for every hard shot."""
    shares = prices.class_shares(rhythm_class)
    clip = clip_length_for(average_shot_s, prices, handles_s)
    works = []
    for cost_class in SHARE_CLASSES:
        share = float(shares.get(cost_class, 0.0))
        if share <= 0 or shots <= 0:
            continue
        own_clip = clip
        if first_estimate and cost_class == "hard" and rhythm_class == "action_peak" and prices.hard_action_peak_clip_s:
            own_clip = max(clip, prices.hard_action_peak_clip_s)
        previs = prices.minutes("previs_shot") if (first_estimate and cost_class == "hard") else 0.0
        works.append(ShotWork(f"{identifier} {cost_class} share", cost_class, average_shot_s, [own_clip],
                              plates=float(shares.get("plates", 0.0)), plate_clip_s=clip, weight=shots * share,
                              storyboard=True, previs_minutes=previs))
    return works


# ---------------------------------------------------------------- reading the project

@dataclass
class SceneInput:
    identifier: str
    label: str
    rhythm_class: str
    rhythm_class_given: bool
    tone_factor: float
    kept: bool
    locked: bool
    target_s: float = None
    counts: dict = None
    location: str = None
    record: object = None


def scene_label(identifier, title):
    title = (title or "").strip()
    return f"{scene_words(identifier)}, {title}" if title else scene_words(identifier)


def story_scenes(breakdown):
    """{scene ID: the story map's scene entry} for a screenplay (empty for prose or with no story map)."""
    story_map = breakdown.story_map or {}
    return {entry.get("id"): entry for entry in story_map.get("scenes", []) or [] if entry.get("id")}


def project_value(breakdown, name):
    project = breakdown.project
    return project.get(name) if project is not None else None


def scope_identifiers(breakdown):
    """The scene IDs PROJECT scope names, or None for all."""
    value = project_value(breakdown, "scope")
    if value is None or normalise_word(value) in ("all", "", "none", "open"):
        return None
    found = []
    for piece in split_list(value):
        piece = piece.strip()
        if ".." in piece:
            first, last = [part.strip() for part in piece.split("..", 1)]
            found.append((first, last))
        elif piece:
            found.append((piece, piece))
    return found


def in_scope(identifier, scope):
    if scope is None:
        return True
    key = scene_key(identifier)
    return any(scene_key(first) <= key <= scene_key(last) for first, last in scope)


def scene_inputs(breakdown, prices, tone_factors):
    """Every scene the estimate knows, in story order: SCENE records merged with the story map's scenes."""
    from_story = story_scenes(breakdown)
    records = {record.identifier: record for record in breakdown.records_of("SCENE", include_omitted=True)
               if record.identifier}
    identifiers = sorted(set(from_story) | set(records), key=scene_key)
    found = []
    for identifier in identifiers:
        record = records.get(identifier)
        entry = from_story.get(identifier) or {}
        if record is not None and normalise_word(record.get("status") or "") == "omitted":
            continue
        rhythm = normalise_word(record.get("rhythm_class") or "") if record is not None else ""
        given = rhythm in RHYTHM_CLASSES
        tone = normalise_word(record.get("tone") or "") if record is not None else ""
        keep = normalise_word(record.get("keep") or "keep") if record is not None else "keep"
        title = entry.get("title") or ""
        if not title and record is not None:
            place = record.get("place_text") or ""
            title = sentence_case(place.split(" - ")[-1]) if place else ""
        found.append(SceneInput(
            identifier=identifier, label=scene_label(identifier, title),
            rhythm_class=rhythm if given else prices.default_rhythm_class, rhythm_class_given=given,
            tone_factor=tone_factors.get(tone, 1.0) if tone else 1.0, kept=keep not in NOT_KEPT,
            locked=record is not None and normalise_word(record.get("locked") or "") == "yes",
            target_s=number_of(record.get("target_duration_s")) if record is not None else None,
            counts=entry.get("counts"), location=(record.get("location") if record is not None else None),
            record=record))
    return found


def average_shot_for(scene, constants):
    table = constant(constants, "rhythm_class_asl_s", {}) or {}
    base = float(table.get(scene.rhythm_class, table.get("mixed", 4.0)))
    return base * (scene.tone_factor or 1.0)


def canonical_model(models, name):
    """A model's name as video_models.json keys it (aliases resolved), or None."""
    if not models or not name:
        return None
    wanted = normalise_word(name)
    for key, facts in models.items():
        if normalise_word(key) == wanted:
            return key
        for alias in (facts or {}).get("aliases", []) or []:
            if normalise_word(alias) == wanted:
                return key
    return None


def shot_model(breakdown, shot):
    value = shot.get("model")
    if is_none_word(value):
        return None
    return canonical_model(breakdown.models, split_item(value).first)


def shot_clip_lengths(breakdown, shot, screen_time_s, prices, handles_s):
    """The clips one take of this shot bills (E5): with a model chosen on the shot, the lengths it allows (through
    derive_fields.clip_plan, which also splits a long shot that is not held at its planned cutaway); otherwise whole
    seconds and never under the shortest clip. Returns (lengths, note)."""
    model = shot_model(breakdown, shot)
    if model:
        try:
            from .derive_fields import clip_plan
            plan = clip_plan(breakdown, shot, model)
            if plan.fits and plan.clip_lengths:
                return [float(value) for value in plan.clip_lengths], ""
            return ([clip_length_for(screen_time_s, prices, handles_s)],
                    f"{shot_words(shot.identifier)} is longer than {model} allows; priced as one clip on a model "
                    "that can hold it")
        except Exception:  # the derivation must never stop an estimate
            pass
    return [clip_length_for(screen_time_s, prices, handles_s)], ""


def has_value(record, name):
    value = record.get(name)
    return value is not None and not is_none_word(value)


def works_from_shots(breakdown, scene, shots, prices, handles_s, average_shot_s, counted_locations):
    """ShotWork for each SHOT of a scene (D13 E5, R6, R20; §6.1 and §7.1 for previs), plus plain notes."""
    works = []
    notes = []
    missing_class = []
    missing_time = []
    previs_found = False
    for shot in shots:
        kind = normalise_word(shot.get("kind") or "")
        cost_class = normalise_word(shot.get("cost_class") or "")
        if has_value(shot, "reuse_of"):
            cost_class = "reuse"
        screen_time = number_of(shot.get("screen_time"))
        if screen_time is None:
            missing_time.append(shot.identifier)
            screen_time = average_shot_s
        lengths, note = shot_clip_lengths(breakdown, shot, screen_time, prices, handles_s)
        if note:
            notes.append(note)
        plates = 0.0
        if kind not in CARD_KINDS and cost_class not in ("reuse", "still_move"):
            if has_value(shot, "text"):
                plates += 1
            if kind == "screen":
                plates += 1
        storyboard_value = normalise_word(shot.get("storyboard") or "")
        storyboard = storyboard_value != "no"
        level = number_of(shot.get("previs_level"), 0.0)
        previs = 0.0
        if 2 <= level <= 3:
            previs = prices.minutes("previs_shot")
            previs_found = True
        elif level == 4:
            previs = prices.minutes("phone_performance")
        size = normalise_word(shot.get("size") or "")
        if cost_class not in COST_CLASSES:
            missing_class.append(shot.identifier)
            for share_work in works_from_shares(shot.identifier, 1.0, scene.rhythm_class, screen_time, prices,
                                                handles_s, first_estimate=False):
                share_work.clip_lengths_s = list(lengths)
                share_work.plate_clip_s = None
                share_work.plates = plates
                share_work.storyboard = storyboard
                share_work.previs_minutes = previs
                works.append(share_work)
            continue
        works.append(ShotWork(shot.identifier, cost_class, screen_time, lengths, plates=plates, storyboard=storyboard,
                              previs_minutes=previs, dialogue_close=size in CLOSE_SIZES))
    extra_previs = 0.0
    if previs_found and scene.location and scene.location not in counted_locations:
        counted_locations.add(scene.location)
        extra_previs = prices.minutes("previs_location_master")
    if missing_class:
        notes.append(f"{scene_words(scene.identifier)}: {plural(len(missing_class), 'shot')} without a cost class, "
                     f"counted by the shares of {PACE_WORDS.get(scene.rhythm_class, 'a mixed')} pace")
    if missing_time:
        notes.append(f"{scene_words(scene.identifier)}: {plural(len(missing_time), 'shot')} without a screen time, "
                     f"counted at {one_place(average_shot_s)} seconds")
    return works, notes, extra_previs


def list_design_seconds(breakdown, scene_identifier):
    """The total of a scene's one-line list times (its design), or None without a timed list."""
    listing = breakdown.record(f"{scene_identifier}-LIST", "SHOTLIST")
    if listing is None:
        return None
    times = [number_of(item.get("time")) for item in breakdown.items(listing, "item")]
    times = [time for time in times if time is not None]
    return sum(times) if times else None


def works_from_list(breakdown, scene, prices, handles_s):
    """ShotWork for the one-line shot list of a scene whose shots are not written yet: each item's time, with the
    classes of its scene's pace shares."""
    listing = breakdown.record(f"{scene.identifier}-LIST", "SHOTLIST")
    if listing is None:
        return [], 0.0
    works = []
    total = 0.0
    for item in breakdown.items(listing, "item"):
        seconds = number_of(item.get("time"))
        if seconds is None:
            continue
        total += seconds
        identifier = item.first or scene.identifier
        number = SHOT_NUMBER.search(identifier)
        if number and 990 <= int(number.group(1)) <= 999:
            works.append(ShotWork(identifier, "graphic", seconds, [clip_length_for(seconds, prices, handles_s)]))
            continue
        clip = clip_length_for(seconds, prices, handles_s)
        for work in works_from_shares(identifier, 1.0, scene.rhythm_class, seconds, prices, handles_s,
                                      first_estimate=False):
            work.clip_lengths_s = [clip]
            work.plate_clip_s = clip
            works.append(work)
    return works, total


# ---------------------------------------------------------------- the whole film

@dataclass
class FilmEstimate:
    version: str
    made_on: datetime.date
    title: str = ""
    source_kind: str = "screenplay"
    price_date: datetime.date = None
    price_age_days: int = None
    money_shown: bool = False
    money_note: str = ""
    hours_shown: bool = True
    scope_text: str = ""
    partial: bool = False
    format: str = "short"
    titles_s: float = 0.0
    scenes: list = dataclass_field(default_factory=list)
    story_runtime_s: tuple = (0.0, 0.0, 0.0)
    runtime_s: tuple = (0.0, 0.0, 0.0)
    as_written_s: tuple = None
    target_s: float = None
    shots: dict = dataclass_field(default_factory=dict)
    plates: float = 0.0
    draft_s: float = 0.0
    final_s: float = 0.0
    money: dict = None
    subscriptions: dict = dataclass_field(default_factory=dict)
    hours: dict = dataclass_field(default_factory=dict)
    hour_parts: dict = dataclass_field(default_factory=dict)
    hours_per_week: float = 20.0
    weeks: dict = dataclass_field(default_factory=dict)
    warnings: list = dataclass_field(default_factory=list)
    notes: list = dataclass_field(default_factory=list)
    plans: list = dataclass_field(default_factory=list)
    counts: dict = dataclass_field(default_factory=dict)
    example: str = ""
    rough: bool = False
    spent: dict = None
    runtime_only_reason: str = ""
    rules: dict = dataclass_field(default_factory=dict)

    @property
    def total_shots(self):
        return sum(self.shots.values())

    @property
    def generated_s(self):
        return self.draft_s + self.final_s

    @property
    def average_shot_s(self):
        shots = self.total_shots
        return (self.runtime_s[1] - self.titles_s) / shots if shots else None

    @property
    def generation_factor(self):
        return self.generated_s / self.runtime_s[1] if self.runtime_s[1] else None


def film_format(breakdown, constants, story_seconds):
    written = normalise_word(project_value(breakdown, "format") or "")
    if written == "short":
        return "short"
    if written in ("feature", "limited_series"):
        return "feature"
    limit = constant(constants, "short_runtime_max_s", 2400)
    return "short" if story_seconds < float(limit) else "feature"


def page_count(breakdown, constants):
    """Pages of a screenplay by A3's line model (page_eighths_line_model), or None without the whole story."""
    model = constant(constants, "page_eighths_line_model", None)
    story = getattr(breakdown, "story", None)
    story_map = breakdown.story_map or {}
    if not model or story is None or story_map.get("first_line_number", 1) != 1:
        return None
    try:
        from .derive_fields import DIALOGUE_WIDTH_TYPES
    except ImportError:
        DIALOGUE_WIDTH_TYPES = ("cue", "dialogue", "parenthetical")
    page_lines = 0
    for number in range(story.first, story.last + 1):
        text = story.line(number).strip()
        if not text:
            page_lines += 1
            continue
        text = text.lstrip("#>= ").strip()
        width = (model["dialogue_characters_per_line"] if story.type_of(number) in DIALOGUE_WIDTH_TYPES
                 else model["action_characters_per_line"])
        page_lines += max(1, math.ceil(len(text) / width))
    return page_lines / float(model["lines_per_page"])


def speech_counts(breakdown, scene_identifiers, characters_per_word=4.9):
    """(speeches, spoken characters, speakers, characters voiced by the user or an actor) for these scenes."""
    wanted = set(scene_identifiers)
    recorded = set()
    for voice in breakdown.records_of("VOICE"):
        if normalise_word(voice.get("source") or "") in RECORDED_VOICE_SOURCES and voice.get("character"):
            recorded.add(voice.get("character").strip())
    for character in breakdown.records_of("CHARACTER"):
        voice_identifier = character.get("voice")
        voice = breakdown.record(voice_identifier, "VOICE") if voice_identifier else None
        if voice is not None and normalise_word(voice.get("source") or "") in RECORDED_VOICE_SOURCES:
            recorded.add(character.identifier)
    speeches = 0
    characters = 0.0
    synthetic_characters = 0.0
    speakers = set()
    for identifier, entry in (breakdown.speeches or {}).items():
        if scene_of(identifier) not in wanted:
            continue
        speeches += 1
        speaker = (entry.get("speaker") or "").strip()
        if speaker:
            speakers.add(speaker)
        text = entry.get("text") or ""
        count = len(text) if text else float(entry.get("words") or 0) * characters_per_word
        characters += count
        if speaker not in recorded:
            synthetic_characters += count
    for record in breakdown.records_of("SPEECH"):
        if scene_of(record.identifier) not in wanted or record.identifier in (breakdown.speeches or {}):
            continue
        speeches += 1
        speaker = (record.get("speaker") or "").strip()
        if speaker:
            speakers.add(speaker)
        count = len(record.get("text") or "")
        characters += count
        if speaker not in recorded:
            synthetic_characters += count
    return speeches, characters, synthetic_characters, speakers


def reference_counts(breakdown, prices, version):
    """(characters, places, things) that need reference pictures: records, or D13's counts before step 4 in the
    first estimate when fewer records exist yet."""
    characters = [record for record in breakdown.records_of("CHARACTER")
                  if normalise_word(record.get("tier") or "") != "extra"]
    places = breakdown.records_of("LOCATION")
    things = breakdown.records_of("PROP")
    defaults = prices.work.get("reference_counts_before_step_4", {})
    counts = [len(characters), len(places), len(things)]
    if version == "v0":
        counts = [max(counts[0], defaults.get("characters", 0)), max(counts[1], defaults.get("locations", 0)),
                  max(counts[2], defaults.get("props", 0))]
    else:
        counts = [counts[0] or defaults.get("characters", 0), counts[1] or defaults.get("locations", 0),
                  counts[2] or defaults.get("props", 0)]
    return tuple(counts)


def music_cues(breakdown, prices, runtime_s):
    """(cues, the policy used, a plain note) by the music policy (D13 R24; D9)."""
    music = prices.work.get("music", {})
    plan = breakdown.singleton("SOUNDPLAN") if hasattr(breakdown, "singleton") else None
    policy = normalise_word(plan.get("music_policy") or "") if plan is not None else ""
    cues_on_record = len(breakdown.records_of("MUSIC"))
    note = ""
    if policy in ("", "open"):
        policy = music.get("policy_before_the_big_choices", "scored")
        note = ("music is counted as a full score until the music choice is made; with no music its money and "
                "minutes drop out")
    if policy == "none":
        return 0, policy, note
    if cues_on_record:
        return cues_on_record, policy, note
    if policy == "scored":
        return max(1, int(round(runtime_s / float(music.get("seconds_per_cue_when_scored", 120))))), policy, note
    if policy == "sparse":
        return int(music.get("sparse_cues", 3)), policy, note
    if policy == "source_only":
        return int(music.get("source_only_cues", 1)), policy, note
    if policy == "end_credits_only":
        return int(music.get("end_credits_only_cues", 1)), policy, note
    return int(music.get("sparse_cues", 3)), policy, note


def voice_plan_for(prices, credits_needed):
    """The smallest voice plan whose monthly credits cover what is needed (D13 §6.5, R19), with the months it takes."""
    order = prices.data.get("voice_plans_in_order", [])
    for name in order:
        per_month = float(prices.plan(name).get("credits_per_month", 0) or 0)
        if per_month >= credits_needed:
            return name, 1
    if not order:
        return None, 0
    largest = order[-1]
    per_month = float(prices.plan(largest).get("credits_per_month", 1) or 1)
    return largest, max(1, math.ceil(credits_needed / per_month))


def finish_film(film, breakdown, prices, constants, scene_identifiers, speech_scene_identifiers=None,
                scene_count=None, group_count=None, story_kind="screenplay", reference=None):
    """Film-level totals, other money (E8), hours (E9) and calendar (E10) from the scene blocks already on film."""
    work = prices.work
    minutes = work.get("minutes", {})
    film.shots = {name: sum(block.shots.get(name, 0.0) for block in film.scenes) for name in COST_CLASSES}
    film.plates = sum(block.plates for block in film.scenes)
    film.draft_s = sum(block.draft_s for block in film.scenes)
    film.final_s = sum(block.final_s for block in film.scenes)
    scene_count = scene_count if scene_count is not None else len(film.scenes)
    runtime_central = film.runtime_s[1]
    total_shots = film.total_shots

    # the user's minutes (D13 §7.1)
    speeches, characters, synthetic_characters, speakers = speech_counts(
        breakdown, speech_scene_identifiers if speech_scene_identifiers is not None else scene_identifiers,
        prices.credits("characters_per_word", 4.9))
    counts_from_story = sum((block.counts or {}).get("spoken_characters", 0) for block in film.scenes)
    if not characters and counts_from_story:
        characters = synthetic_characters = float(counts_from_story)
    if not speeches:
        speeches = int(sum((block.counts or {}).get("speeches", 0) for block in film.scenes))
    references = reference or reference_counts(breakdown, prices, film.version)
    cues, policy, music_note = music_cues(breakdown, prices, runtime_central)
    if music_note:
        film.notes.append(music_note)
    groups = group_count
    if groups is None:
        groups = len(breakdown.records_of("SEQUENCE")) or math.ceil(scene_count / float(minutes.get("scenes_per_group", 6) or 6))
    first_plan = minutes.get("first_plan", {})
    parts = {
        "setting up accounts and the price table": float(minutes.get("setup_once", 0)),
        "planning the film": float(first_plan.get("prose" if story_kind != "screenplay" else "screenplay", 0))
        + float(minutes.get("scene_list_and_big_choices", 0)) + scene_count * float(minutes.get("per_scene", 0))
        + groups * float(minutes.get("group_check", 0)),
        "reference pictures": references[0] * float(minutes.get("reference_pictures_character", 0))
        + references[1] * float(minutes.get("reference_pictures_location", 0))
        + references[2] * float(minutes.get("reference_pictures_prop", 0)),
        "voices": len(speakers or ()) * float(minutes.get("voice_character", 0))
        + speeches * float(minutes.get("voice_line", 0)),
        "music": cues * float(minutes.get("music_cue", 0)),
        "delivery": float(minutes.get("delivery_once", 0)),
    }
    for block in film.scenes:
        for name, value in block.minutes.items():
            parts[name] = parts.get(name, 0.0) + value
    film.hour_parts = {name: value / 60.0 for name, value in parts.items()}
    base = sum(parts.values()) / 60.0
    factors = work.get("hours_factors", {})
    film.hours = {"base": base, "central": base * float(factors.get("central", 1.3)),
                  "high": base * float(factors.get("high", 2.0))}
    hours_per_week = number_of(project_value(breakdown, "hours_per_week"))
    film.hours_per_week = hours_per_week if hours_per_week and hours_per_week > 0 else float(
        work.get("hours_per_week_default", 20))
    film.weeks = {name: value / film.hours_per_week for name, value in film.hours.items()}
    weeks_per_month = float(work.get("weeks_per_month", 4.333))
    months = max(1, math.ceil(film.weeks["central"] / weeks_per_month - 1e-9))
    film.counts.update({"speeches": speeches, "spoken_characters": characters, "speakers": len(speakers or ()),
                        "characters": references[0], "places": references[1], "things": references[2],
                        "music_cues": cues, "music_policy": policy, "groups": groups, "scenes": scene_count,
                        "assistant_months": months})

    # other money (E8)
    if film.money_shown:
        credits = prices.section("credits")
        effect_credits = (total_shots * float(credits.get("effect_share_of_shots", 0.3))
                          * float(credits.get("effect_seconds", 3)) * float(credits.get("effect_per_second", 40))
                          * float(credits.get("effect_tries", 2)))
        speech_credits = (synthetic_characters * float(credits.get("speech_per_character", 1))
                          * float(credits.get("speech_tries", 5)))
        credits_needed = speech_credits + effect_credits
        smallest, smallest_months = voice_plan_for(prices, credits_needed)
        downloads = cues * float(work.get("music", {}).get("downloads_per_cue", 1.5))
        base_pictures = prices.image("reference_pictures_base")
        extra_characters = max(0, references[0] - int(prices.image("reference_pictures_characters_in_base", 7)))
        extra_places = max(0, references[1] - int(prices.image("reference_pictures_locations_in_base", 3)))
        reference_money = (base_pictures + extra_characters * prices.image("reference_pictures_per_character_above")
                           + extra_places * prices.image("reference_pictures_per_location_above"))
        pictures = reference_money + sum(block.pictures_money for block in film.scenes)
        whole_takes_s = sum(block.upscale_whole_takes_s for block in film.scenes)
        if film.version == "v0" or not whole_takes_s:
            whole_takes_s = runtime_central * prices.upscale("whole_take_factor_first_estimate", 1.5)
        film.money = {}
        film.subscriptions = {}
        film.counts.update({"voice_credits": credits_needed, "speech_credits": speech_credits,
                            "effect_credits": effect_credits, "music_downloads": downloads})
        for level in PRICE_LEVELS + ("mixed",):
            rules = prices.level(level)
            if level == "mixed":
                rules = prices.level(rules.get("like", "mid")) if rules.get("like") else prices.level("mid")
            video = sum((block.video_money or {}).get(level, 0.0) for block in film.scenes)
            if rules.get("upscale_to") == "4k":
                upscale = runtime_central * prices.upscale("handles_factor", 1.3) * prices.upscale("above_1080p_per_s")
            else:
                upscale = whole_takes_s * prices.upscale("to_1080p_per_s")
            voice_name = smallest if rules.get("voice_plan") == "smallest" else rules.get("voice_plan")
            voice_months = max(int(rules.get("voice_months", 1)), smallest_months if voice_name == smallest else 1)
            voice_money = float(prices.plan(voice_name).get("per_month", 0) or 0) * voice_months if voice_name else 0.0
            music_money = 0.0
            music_name = rules.get("music_plan")
            music_months = 0
            if cues and music_name:
                per_month_downloads = float(prices.plan(music_name).get("downloads_per_month", 1) or 1)
                music_months = max(int(rules.get("music_months", 1)), math.ceil(downloads / per_month_downloads - 1e-9))
                music_money = float(prices.plan(music_name).get("per_month", 0) or 0) * music_months
            assistant_name = rules.get("assistant_plan", "claude_pro")
            assistant = float(prices.plan(assistant_name).get("per_month", 0) or 0) * months
            software = sum(float(prices.plan(name).get("once", prices.plan(name).get("per_month", 0)) or 0)
                           for name in rules.get("software", []) or [])
            subtotal = video + pictures + upscale + voice_money + music_money + assistant + software
            contingency = subtotal * float(work.get("contingency_share", 0.2))
            film.money[level] = {"video": video, "pictures": pictures, "upscale": upscale,
                                 "voices_and_effects": voice_money, "music": music_money, "assistant": assistant,
                                 "software": software, "contingency": contingency, "total": subtotal + contingency}
            film.subscriptions[level] = [entry for entry in (
                {"plan": voice_name, "months": voice_months} if voice_name else None,
                {"plan": music_name, "months": music_months} if music_money else None,
                {"plan": assistant_name, "months": months},
                *({"plan": name, "months": 0} for name in rules.get("software", []) or [])) if entry]
    return film


def film_checks(film, breakdown, constants, prices, pages=None):
    """Warnings in plain words: runtime target (E2), page check (E3, D13 R22), average shot length (E4, R23),
    generation factor (E6), a long calendar (R17)."""
    tolerance = float(constant(constants, "scene_total_tolerance", 0.1))
    if film.target_s:
        central = film.runtime_s[1]
        if abs(central - film.target_s) > tolerance * film.target_s:
            film.warnings.append(
                f"The film runs about {whole(central / 60)} minutes, more than {whole(tolerance * 100)}% away from "
                f"your target of {whole(film.target_s / 60)} minutes.")
    short_max = float(constant(constants, "short_runtime_max_s", 2400))
    chose_short = normalise_word(project_value(breakdown, "format") or "") == "short"
    if chose_short and film.runtime_s and not film.partial and round(film.runtime_s[1] / 60) > round(short_max / 60):
        # the format choice and the estimate disagree: say so (the second full run: a 50-minute film stood against
        # "A short film (40 minutes or less)" and nothing said it)
        film.warnings.append(
            f"The film runs about {whole(film.runtime_s[1] / 60)} minutes, longer than the short film you chose "
            f"({whole(short_max / 60)} minutes or less): choose a feature, or cut scenes, before trusting the "
            "short film's budgets.")
    if pages and film.source_kind == "screenplay" and not film.partial:
        per_minute = float(prices.warning_band("pages_per_minute", 1.1))
        short_rate = float(prices.warning_band("pages_per_minute_short_script", 0.8))
        page_seconds = pages / per_minute * 60.0
        share = float(prices.warning_band("page_check_share", 0.25))
        central = film.as_written_s[1] if film.as_written_s else film.story_runtime_s[1]
        difference = (central - page_seconds) / page_seconds
        line = (f"The page check: the script is about {one_place(pages)} pages; at {one_place(per_minute)} pages a "
                f"minute it plays about {whole(page_seconds / 60)} minutes, {whole(abs(difference) * 100)}% "
                f"{'more' if difference < 0 else 'less'} than the estimate from the story's words "
                f"({whole(central / 60)} minutes)")
        if abs(difference) > share:
            film.warnings.append(line + f", more than the {whole(share * 100)}% the check allows: look for missing "
                                 "scenes, speech counted twice or wrong pace classes before trusting either.")
        else:
            film.notes.append(line + f", within the {whole(share * 100)}% the check allows.")
        if pages < float(prices.warning_band("short_script_pages_below", 90)):
            high_seconds = pages / short_rate * 60.0
            extrapolated = pages < float(prices.warning_band("extrapolated_below_pages", 60))
            film.notes.append(
                f"Scripts under {whole(prices.warning_band('short_script_pages_below', 90))} pages often play slower: "
                f"at {one_place(short_rate)} pages a minute this one would run about {whole(high_seconds / 60)} "
                "minutes. That is only a high reference" + (", taken beyond the published figures, which start at "
                f"{whole(prices.warning_band('extrapolated_below_pages', 60))} pages" if extrapolated else "")
                + "; measure the timed storyboard before trusting either figure.")
    average = film.average_shot_s
    if average:
        band = prices.warning_band("average_shot_length_s", [3, 7])
        weights = [(block.runtime_s[1], block.average_shot_s / max(float((constant(constants, "rhythm_class_asl_s", {})
                    or {}).get(block.rhythm_class, block.average_shot_s) or 1.0), 1e-9))
                   for block in film.scenes if block.average_shot_s]
        total_weight = sum(weight for weight, _ in weights)
        factor = (sum(weight * value for weight, value in weights) / total_weight) if total_weight else 1.0
        low, high = band[0] * factor, band[1] * factor
        if not (low - 1e-9 <= average <= high + 1e-9):
            film.warnings.append(
                f"The average shot lasts {one_place(average)} seconds, outside {one_place(low)} to {one_place(high)} "
                "seconds for this film's tones: check the pace classes of the scenes before trusting the shot count.")
    factor = film.generation_factor
    band = prices.warning_band("generation_factor", [5, 15])
    if factor and film.total_shots and not (band[0] <= factor <= band[1]):
        film.warnings.append(
            f"About {one_place(factor)} seconds are generated for every second on screen, outside the usual "
            f"{whole(band[0])} to {whole(band[1])}" + (": fast cutting pays for whole clips, as expected in action."
                                                       if factor > band[1] else ": check the takes per shot."))
    limits = prices.warning_band("weeks_central_max", {"short": 26, "other": 52})
    limit = limits.get("short" if film.format == "short" else "other", 52)
    # rounded before comparing, so it never says "about 26 weeks, longer than 26" (the second full run)
    if film.hours_shown and round(film.weeks.get("central", 0)) > limit:
        film.warnings.append(
            f"At {whole(film.hours_per_week)} hours a week this takes about {whole(film.weeks['central'])} weeks, "
            f"longer than {whole(limit)}: a shorter film, or a first part made to the end before the rest, is worth "
            "considering.")


def scene_block_from_words(scene, constants, prices, handles_s, money_shown, scale=1.0):
    seconds = seconds_from_words(scene.counts, constants)
    seconds = tuple(value * scale for value in seconds)
    average = average_shot_for(scene, constants)
    shots = seconds[1] / average if average else 0.0
    works = works_from_shares(scene.identifier, shots, scene.rhythm_class, average, prices, handles_s)
    block = scene_block(scene.identifier, scene.label, works, seconds, prices, basis="words",
                        rhythm_class=scene.rhythm_class, average_shot_s=average, money_shown=money_shown)
    block.counts = dict(scene.counts or {})
    block.target_s = scene.target_s
    return block


def scene_block_from_seconds(scene, seconds, constants, prices, handles_s, money_shown, basis):
    average = average_shot_for(scene, constants)
    shots = seconds[1] / average if average else 0.0
    works = works_from_shares(scene.identifier, shots, scene.rhythm_class, average, prices, handles_s)
    block = scene_block(scene.identifier, scene.label, works, seconds, prices, basis=basis,
                        rhythm_class=scene.rhythm_class, average_shot_s=average, money_shown=money_shown)
    block.target_s = scene.target_s
    return block


def words_example(block, constants):
    counts = block.counts or {}
    if not counts:
        return ""
    pace = float(constant(constants, "speech_wps_default", 2.5))
    per_speech = float(constant(constants, "speech_floor_extra_s", 0.5))
    low_rate, high_rate = constant(constants, "v0_action_seconds_per_word", [0.166, 0.22])
    pause = float((constant(constants, "pause_tiers", {}) or {}).get("script_words", {}).get("(beat)", 1.0))
    pauses = counts.get("beat_marks", 0)
    speech = counts.get("dialogue_words", 0) / pace + per_speech * counts.get("speeches", 0) + pause * pauses
    action = counts.get("action_words", 0)
    pause_text = f" and {plural(pauses, 'pause')} marked in the script" if pauses else ""
    pause_rule = f" and {seconds_words(pause)} for each pause" if pauses else ""
    return (f"Example: {block.label}. Its {whole(counts.get('dialogue_words', 0))} spoken words in "
            f"{plural(counts.get('speeches', 0), 'speech', 'speeches')}{pause_text} take about {whole(speech)} "
            f"seconds ({one_place(pace)} words a second, plus {seconds_words(per_speech)} for each speech"
            f"{pause_rule}); its "
            f"{whole(action)} words of action add {whole(action * float(low_rate))} to {whole(action * float(high_rate))}"
            f" seconds. So it runs about {whole(block.runtime_s[1])} seconds ({whole(block.runtime_s[0])} to "
            f"{whole(block.runtime_s[2])}): about {plural(block.total_shots, 'shot')} at {PACE_WORDS.get(block.rhythm_class, 'a mixed')} "
            f"pace, whose average shot lasts {one_place(block.average_shot_s)} seconds.")


def shots_example(breakdown, block, works, prices, handles_s):
    """One worked shot for the plain part: the turn shot if there is one, else the first shot with takes."""
    candidates = [work for work in works if work.weight == 1.0 and prices.class_work(work.cost_class).get("video")]
    if not candidates:
        return ""
    chosen = candidates[0]
    for work in candidates:
        shot = breakdown.record(work.identifier, "SHOT")
        if shot is not None and normalise_word(shot.get("role") or "") == "turn":
            chosen = work
            break
    rules = prices.class_work(chosen.cost_class)
    takes = rules.get("draft_takes", 0) + rules.get("final_takes", 0)
    generated = chosen.clip_length_s * takes
    single = CLASS_WORDS[chosen.cost_class][0]
    article = "an" if single[0] in "aeiou" else "a"
    return (f"Example: {shot_words(chosen.identifier)} is {one_place(chosen.screen_time_s)} seconds on screen. Each "
            f"take is a {one_place(chosen.clip_length_s)}-second clip (the screen time plus a spare "
            f"{seconds_words(handles_s)} at each end, rounded up to a length the model makes). As {article} {single} it "
            f"takes {rules.get('draft_takes', 0)} cheap draft takes and {rules.get('final_takes', 0)} final takes: "
            f"{whole(generated)} generated seconds for {one_place(chosen.screen_time_s)} seconds of film.")


def page_rules(constants, prices):
    """The figures the plain page names, taken from the constants and the price table so the page never disagrees
    with the arithmetic."""
    low_rate, high_rate = constant(constants, "v0_action_seconds_per_word", [0.166, 0.22])
    per_speech = float(constant(constants, "speech_floor_extra_s", 0.5))
    rules = {"pace": float(constant(constants, "speech_wps_default", 2.5)), "per_speech": per_speech,
             "pause": float((constant(constants, "pause_tiers", {}) or {}).get("script_words", {}).get("(beat)", 1.0)),
             "action_rates": (float(low_rate), float(high_rate)), "handles": float(constant(constants, "handles_s", 0.75)),
             "takes": {}, "central_factor": 1.3, "high_factor": 2.0, "contingency": 0.2, "shortest_clip": 5.0}
    if prices is not None:
        rules["takes"] = {name: (prices.class_work(name).get("draft_takes", 0), prices.class_work(name).get(
            "final_takes", 0)) for name in COST_CLASSES}
        factors = prices.work.get("hours_factors", {})
        rules["central_factor"] = float(factors.get("central", 1.3))
        rules["high_factor"] = float(factors.get("high", 2.0))
        rules["contingency"] = float(prices.work.get("contingency_share", 0.2))
        rules["shortest_clip"] = prices.min_clip_s
    return rules


def seconds_words(value):
    """0.5 -> 'half a second', 1 -> 'a second', 0.75 -> '0.75 seconds'."""
    if abs(value - 0.5) < 1e-9:
        return "half a second"
    if abs(value - 1.0) < 1e-9:
        return "a second"
    return f"{seconds_text_short(value)} seconds"


def seconds_text_short(value):
    text = f"{value:.3f}".rstrip("0").rstrip(".")
    return text or "0"


def prices_state(prices, reason, constants, on):
    """(money shown, plain note, price date, age in days)."""
    if prices is None:
        return False, f"Money is not shown: {reason}.", None, None
    most = int(number_of(constant(constants, "model_facts_max_age_days", 30), 30))
    date = prices.date
    if date is None:
        return False, "Money is not shown: the price table has no date, so its prices cannot be trusted.", None, None
    age = prices.age_days(on)
    if age > most:
        return (False, f"Money is not shown: the prices were checked on {date.isoformat()}, {plural(age, 'day')} ago, "
                f"and prices older than {whole(most)} days are never used. The money comes back once the prices are "
                "refreshed: the AI reads the makers' pages again and you approve any change.", date, age)
    if age < 0:
        return True, f"Prices checked on {date.isoformat()}.", date, age
    return True, f"Prices checked on {date.isoformat()} ({plural(age, 'day')} old).", date, age


def film_estimate(breakdown, version=None, on=None, prices=None, skill_folder=None):
    """The whole estimate of a project (a derive_fields.Breakdown): version 'v0' (the first estimate, from words and
    plans) or 'v1' (from the shots; scenes without shots keep the first estimate). version None picks v1 when any
    shot or shot list exists, else v0."""
    constants = breakdown.constants
    on = on or today()
    reason = ""
    if prices is None:
        prices, reason = PriceTable.load(skill_folder)
    if version is None:
        version = "v1" if (breakdown.records_of("SHOT") or breakdown.records_of("SHOTLIST")) else "v0"
    money_shown, money_note, price_date, age = prices_state(prices, reason, constants, on)
    film = FilmEstimate(version=version, made_on=on, price_date=price_date, price_age_days=age,
                        money_shown=money_shown, money_note=money_note)
    film.rules = page_rules(constants, prices)
    project = breakdown.project
    film.title = (project.get("title") if project is not None else "") or ""
    story_map = breakdown.story_map or {}
    film.source_kind = normalise_word((project.get("source_kind") if project is not None else "")
                                      or (story_map.get("source", {}) or {}).get("kind") or "screenplay")
    if prices is None:
        film.hours_shown = False
        film.runtime_only_reason = reason
        return runtime_only_estimate(film, breakdown, constants)
    handles_s = float(constant(constants, "handles_s", 0.75))
    tone_factors = load_tone_factors(skill_folder)
    scenes = scene_inputs(breakdown, prices, tone_factors)
    screenplay = film.source_kind == "screenplay"
    plan = breakdown.singleton("PLAN")
    options = breakdown.items(plan, "plan_option") if plan is not None else []
    if not screenplay and not any(scene.counts for scene in scenes) and options and version == "v0":
        return plans_estimate(film, breakdown, constants, prices, options, handles_s)
    if not scenes:
        film.rough = True
        return runtime_only_estimate(film, breakdown, constants)
    if not screenplay and version == "v0" and not options and not any(
            scene.target_s for scene in scenes) and not breakdown.records_of("SCENE"):
        film.rough = True
        return runtime_only_estimate(film, breakdown, constants)

    scope = scope_identifiers(breakdown) if version == "v1" else None
    kept = [scene for scene in scenes if scene.kept]
    chosen = [scene for scene in kept if in_scope(scene.identifier, scope)]
    film.partial = scope is not None and len(chosen) < len(kept)
    film.scope_text = (f"Scope: {whole(len(chosen))} of {plural(len(kept), 'scene')}; the figures cover these scenes "
                       "only, and the one-off work (setting up, reference pictures, delivery) is counted in full."
                       if film.partial else f"Scope: all {plural(len(chosen), 'scene')}." if len(chosen) > 1
                       else "Scope: the one scene there is.")

    # the first estimate as written (screenplays), for runtime and the page check
    as_written = [scene_block_from_words(scene, constants, prices, handles_s, money_shown) for scene in scenes
                  if scene.counts]
    story_as_written = tuple(sum(block.runtime_s[index] for block in as_written) for index in range(3))
    film.format = film_format(breakdown, constants, story_as_written[1] if as_written else 0.0)
    film.titles_s = float(prices.work.get("titles_and_credits_s", {}).get(film.format, 0))
    target = number_of(project_value(breakdown, "runtime_target_s"))
    film.target_s = target
    if as_written:
        film.as_written_s = story_as_written

    scale = 1.0
    if version == "v0" and target and as_written:
        kept_written = sum(block.runtime_s[1] for block in as_written
                           if any(scene.identifier == block.identifier for scene in kept))
        if kept_written > 0:
            scale = max(0.0, (target - film.titles_s)) / kept_written
            film.notes.append(
                f"Your target is {whole(target / 60)} minutes with titles and credits, so every kept scene is "
                f"counted at {whole(scale * 100)}% of its length as written.")

    counted_locations = set()
    first_words = []
    no_pace = []
    for scene in chosen:
        block = None
        if version == "v1":
            shots = sorted(breakdown.shots_of(scene.identifier), key=lambda record: shot_key(record.identifier))
            if shots:
                average = average_shot_for(scene, constants)
                works, notes, extra_previs = works_from_shots(breakdown, scene, shots, prices, handles_s, average,
                                                              counted_locations)
                total = sum(number_of(shot.get("screen_time"), average) for shot in shots)
                block = scene_block(scene.identifier, scene.label, works, (total, total, total), prices,
                                    basis="shots", rhythm_class=scene.rhythm_class,
                                    average_shot_s=(total / len(shots)) if shots else average,
                                    money_shown=money_shown, extra_previs_minutes=extra_previs)
                block.notes.extend(notes)
                if not film.example:
                    film.example = shots_example(breakdown, block, works, prices, handles_s)
            else:
                works, total = works_from_list(breakdown, scene, prices, handles_s)
                if works:
                    count = len({work.identifier for work in works})
                    block = scene_block(scene.identifier, scene.label, works, (total, total, total), prices,
                                        basis="list", rhythm_class=scene.rhythm_class,
                                        average_shot_s=total / count if count else 0.0, money_shown=money_shown)
        if block is None and scene.counts:
            block = scene_block_from_words(scene, constants, prices, handles_s, money_shown, scale)
            first_words.append(scene.identifier)
        if block is None and scene.target_s:
            block = scene_block_from_seconds(scene, (scene.target_s,) * 3, constants, prices, handles_s, money_shown,
                                             "planned_length")
        if block is None and not screenplay:
            low, high = prices.work.get("prose_candidate_scene_s", [120, 150])
            block = scene_block_from_seconds(scene, (float(low), (low + high) / 2.0, float(high)), constants, prices,
                                             handles_s, money_shown, "plan")
        if block is None:
            continue
        block.target_s = scene.target_s
        if not scene.rhythm_class_given and block.basis in ("words", "list", "planned_length", "plan"):
            no_pace.append(scene.identifier)
        film.scenes.append(block)
    if not film.scenes:
        film.rough = True
        return runtime_only_estimate(film, breakdown, constants)
    if version == "v0" and not film.example:
        biggest = max(film.scenes, key=lambda block: (block.counts or {}).get("speeches", 0))
        film.example = words_example(biggest, constants)
    story = tuple(sum(block.runtime_s[index] for block in film.scenes) for index in range(3))
    film.story_runtime_s = story
    film.runtime_s = tuple(value + film.titles_s for value in story)
    if version == "v1" and first_words:
        film.notes.append(f"{plural(len(first_words), 'scene')} with no shots yet keep the first estimate from "
                          "their words.")
    if no_pace and len(no_pace) == len(film.scenes):
        film.notes.append("No scene has a pace class yet (the story plan gives each scene one), so every scene is "
                          "counted at a mixed pace; the shot count changes then.")
    elif no_pace:
        film.notes.append(", ".join(scene_words(identifier) for identifier in no_pace)
                          + (" has" if len(no_pace) == 1 else " have") + " no pace class yet: counted at a mixed pace.")
    finish_film(film, breakdown, prices, constants, [block.identifier for block in film.scenes],
                story_kind="screenplay" if screenplay else "prose")
    for block in film.scenes:
        film.notes.extend(block.notes)
        # a scene's shots are measured against its own design, the one-line list's total (the same rule and the same
        # tolerance as TIME-03); the first estimate's target is a guess from the words and is not judged
        design = list_design_seconds(breakdown, block.identifier) if block.basis == "shots" else None
        if version == "v1" and design:
            tolerance = float(constant(constants, "scene_total_tolerance", 0.1))
            if abs(block.runtime_s[1] - design) > tolerance * design:
                film.warnings.append(
                    f"{sentence_case(block.label)} runs {whole(block.runtime_s[1])} seconds against the "
                    f"{whole(design)} its shot list planned, more than {whole(tolerance * 100)}% away.")
    pages = page_count(breakdown, constants) if screenplay and not film.partial else None
    film.counts["pages"] = pages
    film_checks(film, breakdown, constants, prices, pages)
    film.spent = spent_so_far(breakdown) if money_shown else None
    return film


def runtime_only_estimate(film, breakdown, constants):
    """When no scene can be estimated (prose before its plan) or the price table is missing: the story's rough
    runtime from its words, the reader's first estimate."""
    story_map = breakdown.story_map or {}
    first = story_map.get("first_estimate") or {}
    if first:
        low, central, high = (float(first.get("low_s", 0)), float(first.get("central_s", 0)),
                              float(first.get("high_s", 0)))
        film.story_runtime_s = (low, central, high)
        film.format = film_format(breakdown, constants, central)
        film.runtime_s = film.story_runtime_s
        film.rough = film.rough or bool(first.get("rough"))
    film.money_shown = False
    film.hours_shown = False
    if film.runtime_only_reason:
        film.money_note = f"Only the runtime is shown: {film.runtime_only_reason}."
    elif film.source_kind != "screenplay":
        film.money_note = "Shots, money and hours come with the plans for turning the book into a film."
    return film


def plans_estimate(film, breakdown, constants, prices, options, handles_s):
    """Prose at the story plan: each macro plan (PLAN plan_option) estimated at its runtime, at the pace mix of the
    scenes that exist (mixed when none has a pace class yet)."""
    story_map = breakdown.story_map or {}
    first = story_map.get("first_estimate") or {}
    if first:
        film.story_runtime_s = (float(first.get("low_s", 0)), float(first.get("central_s", 0)),
                                float(first.get("high_s", 0)))
        film.runtime_s = film.story_runtime_s
    film.rough = True
    classes = [normalise_word(record.get("rhythm_class") or "") for record in breakdown.records_of("SCENE")]
    classes = [name for name in classes if name in RHYTHM_CLASSES]
    mix = {name: classes.count(name) / len(classes) for name in set(classes)} if classes else {
        prices.default_rhythm_class: 1.0}
    if not classes:
        film.notes.append("No scene has a pace class yet, so each plan is counted at a mixed pace.")
    for option in options:
        runtime = number_of(option.get("runtime_s"))
        if not runtime:
            continue
        option_format = normalise_word(option.get("format") or "feature")
        option_format = "short" if option_format == "short" else "feature"
        titles = float(prices.work.get("titles_and_credits_s", {}).get(option_format, 0))
        story_seconds = max(0.0, runtime - titles)
        scene_total = number_of(option.get("scenes"))
        plan_film = FilmEstimate(version="v0", made_on=film.made_on, price_date=film.price_date,
                                 price_age_days=film.price_age_days, money_shown=film.money_shown,
                                 money_note=film.money_note, source_kind=film.source_kind, format=option_format,
                                 titles_s=titles)
        for rhythm_class, share in sorted(mix.items()):
            seconds = story_seconds * share
            scene = SceneInput(f"plan {option.first} {rhythm_class}", f"plan {option.first}", rhythm_class, True, 1.0,
                               True, False)
            block = scene_block_from_seconds(scene, (seconds, seconds, seconds), constants, prices, handles_s,
                                             film.money_shown, "plan")
            plan_film.scenes.append(block)
        plan_film.story_runtime_s = (story_seconds,) * 3
        plan_film.runtime_s = (runtime,) * 3
        low, high = prices.work.get("prose_candidate_scene_s", [120, 150])
        finish_film(plan_film, breakdown, prices, constants, [], speech_scene_identifiers=[],
                    scene_count=int(scene_total) if scene_total else max(1, round(story_seconds / ((low + high) / 2.0))),
                    story_kind="prose")
        plan_film.counts["plan"] = option.first
        film.plans.append(plan_film)
    film.hours_shown = bool(film.plans)
    if not film.plans:
        return runtime_only_estimate(film, breakdown, constants)
    return film


def spent_so_far(breakdown):
    """Money spent on takes so far (TAKE cost_usd) and shots with a kept take, or None when no take is logged."""
    takes = breakdown.records_of("TAKE")
    if not takes:
        return None
    spent = sum(number_of(take.get("cost_usd"), 0.0) for take in takes)
    kept = set()
    for take in takes:
        if normalise_word(take.get("kept") or "") == "yes":
            clip = take.get("clip") or take.identifier or ""
            match = re.match(r"^(?:TK-)?(SC\d{2,3}[A-Z]?-SH\d+)", clip)
            if match:
                kept.add(match.group(1))
    return {"spent": spent, "takes": len(takes), "shots_kept": len(kept),
            "shots": len(breakdown.records_of("SHOT"))}


# ---------------------------------------------------------------- the plain page (14 Time and cost.md)

def version_words(film):
    return "the first estimate" if film.version == "v0" else "the estimate from the shots"


def minutes_range(runtime):
    """'about 36 minutes (33 to 39)'; under two minutes in seconds ('about 75 seconds')."""
    if runtime[1] < 120:
        low, central, high = (int(round(value)) for value in runtime)
        unit = "seconds"
    else:
        low, central, high = (int(round(value / 60)) for value in runtime)
        unit = "minutes"
    if low == high:
        return f"about {whole(central)} {unit}"
    return f"about {whole(central)} {unit} ({whole(low)} to {whole(high)})"


def in_short(film):
    if film.rough and not film.total_shots and film.source_kind != "screenplay":
        return (f"In short: the book as written would run {minutes_range(film.runtime_s)}, counting every word as "
                f"action. {film.money_note}")
    if film.story_runtime_s and film.titles_s:
        # one film length everywhere: the story's, then the same with titles and credits added (the book says so too)
        parts = [f"In short: the film runs {minutes_range(film.story_runtime_s)} of story, "
                 f"{minutes_range(film.runtime_s).replace('about ', '')} with titles and credits"]
    else:
        parts = [f"In short: the film runs {minutes_range(film.runtime_s)}"]
    if film.total_shots:
        parts.append(f" in about {plural(film.total_shots, 'shot')}")
    if film.money_shown and film.money:
        levels = ", ".join(f"{dollars(film.money[level]['total'])} ({LEVEL_WORDS[level].lower()})"
                           for level in PRICE_LEVELS)
        parts.append(f". Making it with AI video would cost about {levels}")
        if film.hours_shown:
            parts.append(f", and about {whole(film.hours['central'])} hours of your time "
                         f"({whole(film.hours['base'])} to {whole(film.hours['high'])})")
        parts.append(".")
    elif film.hours_shown and film.hours:
        parts.append(f", and making it would take about {whole(film.hours['central'])} hours of your time "
                     f"({whole(film.hours['base'])} to {whole(film.hours['high'])}). {film.money_note}")
    else:
        parts.append(f". {film.money_note}" if film.money_note else ".")
    return "".join(parts)


def plan_name(prices, key):
    name = prices.plan(key).get("name") if prices is not None else None
    return name or key.replace("_", " ")


def money_table(film, levels):
    lines = ["| | " + " | ".join(LEVEL_WORDS[level] for level in levels) + " |",
             "|---|" + "---:|" * len(levels)]
    share = int(round(100 * film.rules.get("contingency", 0.2)))
    for key, words in MONEY_LINES:
        if key == "contingency":
            words = f"Contingency ({share}%)"
        values = [dollars(film.money[level][key]) for level in levels]
        if key == "total":
            lines.append(f"| **{words}** | " + " | ".join(f"**{value}**" for value in values) + " |")
        else:
            lines.append(f"| {words} | " + " | ".join(values) + " |")
    return lines


def render_plans(film, prices, lines):
    lines.append("## The plans side by side")
    lines.append("")
    header = "| | " + " | ".join(f"Plan {plan.counts.get('plan', '')}" for plan in film.plans) + " |"
    lines.append(header)
    lines.append("|---|" + "---:|" * len(film.plans))
    lines.append("| Runtime (minutes) | " + " | ".join(whole(plan.runtime_s[1] / 60) for plan in film.plans) + " |")
    lines.append("| Shots | " + " | ".join(whole(plan.total_shots) for plan in film.plans) + " |")
    lines.append("| Generated seconds | " + " | ".join(whole(plan.generated_s) for plan in film.plans) + " |")
    if film.money_shown:
        for level in PRICE_LEVELS:
            lines.append(f"| Money, {LEVEL_WORDS[level].lower()} | "
                         + " | ".join(dollars(plan.money[level]["total"]) for plan in film.plans) + " |")
    lines.append("| Your hours (central) | " + " | ".join(whole(plan.hours["central"]) for plan in film.plans) + " |")
    lines.append(f"| Weeks at {whole(film.plans[0].hours_per_week)} hours a week | "
                 + " | ".join(whole(plan.weeks["central"]) for plan in film.plans) + " |")
    lines.append("")


def render_time_and_cost(film, prices=None):
    """The plain page "14 Time and cost.md": example first, the four figures, then the detail."""
    lines = ["# Time and cost", ""]
    if film.plans:
        lines.append(f"In short: the plans below run from {whole(min(plan.runtime_s[1] for plan in film.plans) / 60)} "
                     f"to {whole(max(plan.runtime_s[1] for plan in film.plans) / 60)} minutes; the book as written "
                     f"would run {minutes_range(film.runtime_s)}, counting every word as action."
                     + ("" if film.money_shown else f" {film.money_note}"))
    else:
        lines.append(in_short(film))
    lines.append("")
    made = (f"This is {version_words(film)}, worked out by code on {film.made_on.isoformat()}"
            + (" from the words of the story, before any shot is planned." if film.version == "v0" and not film.plans
               else " from each plan's length." if film.plans else " from the shots written so far."))
    lines.append(made)
    if film.money_shown:
        lines.append(film.money_note)
    if film.scope_text:
        lines.append(film.scope_text)
    if film.rough:
        lines.append("It is rough: treat every figure as a range.")
    lines.append("")
    if film.example:
        lines.append(film.example)
        lines.append("")
    if film.plans:
        render_plans(film, prices, lines)
    if film.total_shots:
        lines.append("## Runtime and shots")
        lines.append("")
        lines.append("| | Low | Central | High |")
        lines.append("|---|---:|---:|---:|")
        lines.append("| Story, in seconds | " + " | ".join(whole(value) for value in film.story_runtime_s) + " |")
        lines.append(f"| With {whole(film.titles_s)} seconds of titles and credits | "
                     + " | ".join(whole(value) for value in film.runtime_s) + " |")
        lines.append("| In minutes | " + " | ".join(whole(value / 60) for value in film.runtime_s) + " |")
        lines.append("")
        if film.as_written_s and film.version == "v0" and film.target_s:
            lines.append(f"As written, the story runs about {whole(film.as_written_s[1])} seconds "
                         f"({whole(film.as_written_s[0])} to {whole(film.as_written_s[2])}).")
            lines.append("")
        by_class = ", ".join(plural(film.shots[name], *CLASS_WORDS[name]) for name in COST_CLASSES
                             if round(film.shots.get(name, 0)))
        lines.append(f"Shots: about {whole(film.total_shots)}; the average shot lasts "
                     f"{one_place(film.average_shot_s or 0)} seconds. By the work they need: {by_class}"
                     + (f"; plus {plural(film.plates, 'extra plate')} for compositing (a background or an element "
                        "made separately and laid over)." if round(film.plates) else "."))
        lines.append("")
        factor = film.generation_factor
        lines.append(f"Generated seconds: about {whole(film.draft_s)} in cheap draft takes and {whole(film.final_s)} "
                     f"in final takes, {whole(film.generated_s)} in all: about {one_place(factor or 0)} seconds made "
                     "for every second on screen, because every take is paid for whole, kept or not.")
        lines.append("")
    elif not film.plans and film.runtime_s[1]:
        lines.append("## Runtime")
        lines.append("")
        lines.append(f"About {whole(film.runtime_s[1])} seconds ({whole(film.runtime_s[0])} to "
                     f"{whole(film.runtime_s[2])}).")
        lines.append("")
    if film.money_shown and film.money and not film.plans:
        lines.append("## Money by price level")
        lines.append("")
        levels = list(PRICE_LEVELS)
        if film.version == "v1" and abs(film.money["mixed"]["total"] - film.money["mid"]["total"]) >= 0.5:
            levels.append("mixed")
        lines.extend(money_table(film, levels))
        lines.append("")
        if prices is not None:
            lines.append(f"Final takes cost about ${prices.video_price('budget'):.2f} a generated second at the budget "
                         f"level, ${prices.video_price('mid'):.2f} at mid and ${prices.video_price('premium'):.2f} at "
                         f"premium; draft takes cost ${prices.draft_price:.2f} at every level."
                         + (" The mixed plan makes drafts cheaply, finals at mid, and dialogue close-ups at premium."
                            if "mixed" in levels else ""))
        subscriptions = []
        for level in PRICE_LEVELS:
            entries = [f"{plan_name(prices, entry['plan'])} for {plural(entry['months'], 'month')}"
                       if entry.get("months") else f"{plan_name(prices, entry['plan'])}, bought once"
                       for entry in film.subscriptions.get(level, [])]
            if entries:
                subscriptions.append(f"- {LEVEL_WORDS[level]}: " + "; ".join(entries) + ".")
        if subscriptions:
            lines.append("")
            lines.append("Monthly plans and software in each column:")
            lines.extend(subscriptions)
        lines.append("")
        lines.append("Not counted: lip sync made in the edit, a reference sheet for every setting, other languages, "
                     "festival fees and legal advice.")
        lines.append("")
        if film.spent:
            lines.append(f"Spent so far on takes: {dollars(film.spent['spent'])} on {plural(film.spent['takes'], 'take')}; "
                         f"{whole(film.spent['shots_kept'])} of {plural(film.spent['shots'], 'shot')} have a kept take.")
            lines.append("")
    elif not film.money_shown and not film.plans and film.total_shots:
        lines.append("## Money")
        lines.append("")
        lines.append(film.money_note)
        lines.append("")
    if film.hours_shown and film.hours and not film.plans:
        lines.append("## Your time")
        lines.append("")
        lines.append("| | Base | Central | High |")
        lines.append("|---|---:|---:|---:|")
        lines.append("| Hours | " + " | ".join(whole(film.hours[name]) for name in ("base", "central", "high")) + " |")
        lines.append(f"| Weeks at {whole(film.hours_per_week)} hours a week | "
                     + " | ".join(weeks_text(film.weeks[name]) for name in ("base", "central", "high")) + " |")
        lines.append("")
        ranked = sorted(((value, name) for name, value in film.hour_parts.items() if value >= 0.5), reverse=True)
        lines.append("Where the base hours go: " + "; ".join(f"{name} {whole(value)}" for value, name in ranked) + ".")
        central_share = whole((film.rules.get("central_factor", 1.3) - 1) * 100)
        high = film.rules.get("high_factor", 2.0)
        high_words = "doubles the base" if abs(high - 2.0) < 1e-9 else f"is {one_place(high)} times the base"
        lines.append(f"The central figure adds {central_share}% for a first film and the high figure {high_words}, "
                     "until the first finished group of scenes gives your own times.")
        lines.append("")
    if film.scenes and not film.plans:
        lines.append("## Scene by scene")
        lines.append("")
        for block in film.scenes:
            lines.append("- " + scene_line(film, block))
        lines.append("")
    if film.warnings:
        lines.append("## Things to look at")
        lines.append("")
        lines.extend(f"- {warning}" for warning in film.warnings)
        lines.append("")
    notes = [note for note in film.notes if note]
    lines.append("## How this was worked out")
    lines.append("")
    lines.append("- Code works out every figure on this page from the records and the dated price table; nobody "
                 "types a total, and the page is made again each time the estimate runs.")
    if film.plans:
        lines.append("- Each plan's shots come from its length, less the titles and credits, at the pace of its "
                     "scenes; the kinds of work (stills, easy, dialogue, hard) come from the usual shares for that "
                     "pace.")
    elif film.version == "v0" and not film.total_shots:
        low_rate, high_rate = film.rules.get("action_rates", (0.166, 0.22))
        lines.append(f"- Every word of the book counts as action here, at {seconds_text_short(low_rate)} to "
                     f"{seconds_text_short(high_rate)} seconds a word, so the figure only says roughly how long the "
                     "book is on screen.")
    elif film.version == "v0":
        low_rate, high_rate = film.rules.get("action_rates", (0.166, 0.22))
        lines.append(f"- Spoken words play at {one_place(film.rules.get('pace', 2.5))} words a second, plus "
                     f"{seconds_words(film.rules.get('per_speech', 0.5))} for each speech and "
                     f"{seconds_words(film.rules.get('pause', 1.0))} for each pause the script marks; action plays at "
                     f"{seconds_text_short(low_rate)} to {seconds_text_short(high_rate)} seconds a word.")
        lines.append("- Shots come from each scene's pace (action peak, suspense, mixed, dialogue or contemplative) "
                     "and its tone; the kinds of work (stills, easy, dialogue, hard) come from the usual shares for "
                     "that pace until the shots are written.")
    else:
        takes = film.rules.get("takes", {})
        lines.append(f"- Each shot's clip is its screen time plus a spare {seconds_words(film.rules.get('handles', 0.75))}"
                     " at each end, rounded up to a length the model makes, and never shorter than "
                     f"{one_place(film.rules.get('shortest_clip', 5.0))} seconds while no model is chosen.")
        if takes:
            lines.append(f"- Takes follow each shot's cost class: easy {takes['easy'][0]} draft and {takes['easy'][1]} "
                         f"final takes, dialogue {takes['dialogue'][0]} and {takes['dialogue'][1]}, hard "
                         f"{takes['hard'][0]} and {takes['hard'][1]}; stills, graphics and reused shots need none; "
                         "text in picture or a screen adds a plate.")
    lines.extend(f"- {full_stop(note)}" for note in dict.fromkeys(notes))
    lines.append("")
    return "\n".join(lines)


def scene_line(film, block):
    label = block.label
    if block.basis == "shots":
        text = (f"{label}: {whole(block.runtime_s[1])} seconds in {plural(block.total_shots, 'shot')}"
                + (f" (first estimate {whole(block.target_s)})" if block.target_s else ""))
    elif block.basis == "list":
        text = (f"{label}: {whole(block.runtime_s[1])} seconds in {plural(block.total_shots, 'listed shot')}, "
                "counted by the pace's shares until the shots are written")
    else:
        spread = (f" ({whole(block.runtime_s[0])} to {whole(block.runtime_s[2])})"
                  if round(block.runtime_s[0]) != round(block.runtime_s[2]) else "")
        text = (f"{label}: about {whole(block.runtime_s[1])} seconds{spread}, about "
                f"{plural(block.total_shots, 'shot')} at {PACE_WORDS.get(block.rhythm_class, 'a mixed')} pace")
    text += f"; {whole(block.generated_s)} generated seconds"
    if film.money_shown and block.video_money:
        text += f"; video takes about {dollars(block.video_money['mid'])} at mid"
    return text + "."


# ---------------------------------------------------------------- the machine file (D13 §11.2's blocks)

def rounded(value, places=1):
    return None if value is None else round(float(value), places)


def block_as_json(block, film):
    data = {
        "scene": block.identifier,
        "version": VERSION_NAMES.get(film.version, film.version),
        "basis": block.basis,
        "price_date": film.price_date.isoformat() if film.price_date else None,
        "rhythm_class": block.rhythm_class,
        "runtime_s": ({"low": rounded(block.runtime_s[0]), "central": rounded(block.runtime_s[1]),
                       "high": rounded(block.runtime_s[2])}
                      if round(block.runtime_s[0], 1) != round(block.runtime_s[2], 1) else rounded(block.runtime_s[1])),
        "target_duration_s": rounded(block.target_s),
        "shots": {"total": rounded(block.total_shots), **{name: rounded(block.shots.get(name, 0.0))
                                                          for name in COST_CLASSES},
                  "composite_plates": rounded(block.plates)},
        "average_shot_s": rounded(block.average_shot_s, 2),
        "generated_s": {"draft": rounded(block.draft_s), "final": rounded(block.final_s),
                        "factor": rounded(block.generated_s / block.runtime_s[1]) if block.runtime_s[1] else None},
        "hours": {"base": rounded(block.base_minutes / 60.0, 2)},
        "writer": "code_derived",
    }
    if film.money_shown and block.video_money is not None:
        data["money_usd"] = {"video": {level: rounded(value, 2) for level, value in block.video_money.items()},
                             "pictures": rounded(block.pictures_money, 2), "other": "film level"}
    if block.notes:
        data["notes"] = list(block.notes)
    return data


def film_as_json(film):
    data = {
        "version": VERSION_NAMES.get(film.version, film.version),
        "made_on": film.made_on.isoformat(),
        "price_date": film.price_date.isoformat() if film.price_date else None,
        "price_age_days": film.price_age_days,
        "money_shown": film.money_shown,
        "money_note": "" if film.money_shown else film.money_note,
        "format": film.format,
        "rough": film.rough,
        "partial_scope": film.partial,
        "titles_and_credits_s": rounded(film.titles_s),
        "story_runtime_s": {"low": rounded(film.story_runtime_s[0]), "central": rounded(film.story_runtime_s[1]),
                            "high": rounded(film.story_runtime_s[2])},
        "runtime_s": {"low": rounded(film.runtime_s[0]), "central": rounded(film.runtime_s[1]),
                      "high": rounded(film.runtime_s[2]), "target": rounded(film.target_s)},
        "writer": "code_derived",
    }
    if film.as_written_s:
        data["as_written_s"] = {"low": rounded(film.as_written_s[0]), "central": rounded(film.as_written_s[1]),
                                "high": rounded(film.as_written_s[2])}
    if film.total_shots:
        data["shots"] = {"total": rounded(film.total_shots), **{name: rounded(film.shots.get(name, 0.0))
                                                                for name in COST_CLASSES},
                         "composite_plates": rounded(film.plates)}
        data["average_shot_s"] = rounded(film.average_shot_s, 2)
        data["generated_s"] = {"draft": rounded(film.draft_s), "final": rounded(film.final_s),
                               "factor": rounded(film.generation_factor)}
    if film.money_shown and film.money:
        data["money_usd"] = {level: {key: rounded(value, 2) for key, value in lines.items()}
                             for level, lines in film.money.items()}
        data["by_price_level"] = {level: rounded(lines["total"], 2) for level, lines in film.money.items()}
        data["subscriptions"] = film.subscriptions
        if film.spent:
            data["spent_usd"] = {key: rounded(value, 2) for key, value in film.spent.items()}
    if film.hours_shown and film.hours:
        data["hours"] = {name: rounded(value) for name, value in film.hours.items()}
        data["hour_parts"] = {name: rounded(value, 2) for name, value in film.hour_parts.items()}
        data["calendar"] = {"hours_per_week": rounded(film.hours_per_week),
                            "weeks_central": rounded(film.weeks.get("central")),
                            "weeks_high": rounded(film.weeks.get("high"))}
    counts = {key: (rounded(value, 2) if isinstance(value, float) else value) for key, value in film.counts.items()
              if value is not None and (film.money_shown or "credit" not in key)}
    data["counts"] = counts
    data["warnings"] = list(film.warnings)
    data["notes"] = list(dict.fromkeys(note for note in film.notes if note))
    return data


def estimate_as_json(film):
    """The machine file: the film block, one block per scene and one per plan (D13 §11.2)."""
    data = {"estimate": film_as_json(film), "scenes": [block_as_json(block, film) for block in film.scenes]}
    if film.plans:
        data["plans"] = [{"plan": plan.counts.get("plan"), **film_as_json(plan)} for plan in film.plans]
    return data


# ---------------------------------------------------------------- writing the files and the code-owned fields

def write_estimate_files(project_folder, film, prices=None):
    """Write "14 Time and cost.md" and "For machines - do not edit/estimate.json". Returns the names written."""
    folder = Path(project_folder)
    text = render_time_and_cost(film, prices)
    (folder / TIME_AND_COST_FILE).write_text(text, encoding="utf-8")
    machine = folder / MACHINE_FOLDER
    machine.mkdir(parents=True, exist_ok=True)
    temporary = machine / (ESTIMATE_JSON_FILE + ".part")
    with open(temporary, "w", encoding="utf-8") as handle:
        json.dump(estimate_as_json(film), handle, indent=1, ensure_ascii=False)
        handle.write("\n")
    os.replace(temporary, machine / ESTIMATE_JSON_FILE)
    return [TIME_AND_COST_FILE, f"{MACHINE_FOLDER}/{ESTIMATE_JSON_FILE}"]


def read_estimate_json(project_folder):
    path = Path(project_folder) / MACHINE_FOLDER / ESTIMATE_JSON_FILE
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


def fields_to_store(film, breakdown):
    """[(type, ID or None, field, value)] of the code-owned fields this estimate fills."""
    wanted = []
    if film.price_date:
        wanted.append(("PROJECT", None, "model_facts_date", film.price_date.isoformat()))
    if film.version == "v0" and film.scenes and not film.plans:
        for block in film.scenes:
            if block.basis == "words":
                wanted.append(("SCENE", block.identifier, "target_duration_s", str(int(round(block.runtime_s[1])))))
        if breakdown.singleton("PLAN") is not None:
            if film.as_written_s:
                wanted.append(("PLAN", None, "runtime_estimate", str(int(round(film.as_written_s[1])))))
            wanted.append(("PLAN", None, "scene_budget", str(len(film.scenes))))
            wanted.append(("PLAN", None, "shot_budget", str(int(round(film.total_shots)))))
    elif film.version == "v1":
        for block in film.scenes:
            if block.basis == "words" and block.target_s is None:
                wanted.append(("SCENE", block.identifier, "target_duration_s", str(int(round(block.runtime_s[1])))))
    return wanted


def store_estimate_fields(project_folder, film, breakdown):
    """Write the code-owned fields of fields_to_store into the record files, keeping old copies in history. A locked
    record only gains a field it lacks. Returns (values changed, file names changed, values kept on locked records)."""
    from .project_files import Project, history_run_folder, keep_in_history
    from .record_format import write_file
    wanted = fields_to_store(film, breakdown)
    if not wanted:
        return 0, [], 0
    project = Project(project_folder, breakdown.schema, breakdown.words)
    record_files = project.load_record_files()
    changed_files = {}
    changed = 0
    kept_locked = 0
    for type_name, identifier, name, value in wanted:
        target = None
        for record_file in sorted(record_files, key=lambda item: (0 if item.name.startswith("04 ") and type_name == "SCENE"
                                                                   else 1, item.name)):
            for record in record_file.records:
                if record.type_name == type_name and (identifier is None or record.identifier == identifier):
                    target = (record_file, record)
                    break
            if target:
                break
        if target is None:
            continue
        record_file, record = target
        present = record.get(name)
        if present is not None and str(present).strip() == value:
            continue
        locked = normalise_word(record.get("locked") or "") == "yes"
        if locked and present is not None and not is_none_word(present):
            kept_locked += 1
            continue
        if locked and present is not None and name != "model_facts_date":
            kept_locked += 1
            continue
        record.set_field(name, value, breakdown.schema)
        changed += 1
        changed_files[record_file.name] = record_file
    if changed_files:
        history = history_run_folder(project)
        for name, record_file in changed_files.items():
            path = Path(project_folder) / name
            if path.is_file():
                keep_in_history(history, path, name)
            write_file(record_file, path, breakdown.schema)
        try:
            project.write_manifest(project.refresh_manifest(project.read_manifest()))
        except (OSError, ValueError):
            pass
    return changed, sorted(changed_files), kept_locked


def note_in_manifest(project_folder, film, schema=None, words=None):
    try:
        from .project_files import Project
        project = Project(project_folder, schema, words)
        manifest = project.read_manifest()
        manifest["estimate"] = {"version": VERSION_NAMES.get(film.version, film.version),
                                "made": film.made_on.isoformat(),
                                "price_date": film.price_date.isoformat() if film.price_date else None,
                                "money_shown": film.money_shown, "file": TIME_AND_COST_FILE}
        project.write_manifest(manifest)
    except (OSError, ValueError, ImportError):
        pass


def nothing_to_estimate(film):
    return not film.scenes and not film.plans and not film.runtime_s[1]


def load_breakdown(project_folder):
    from .derive_fields import Breakdown
    return Breakdown.from_project(project_folder)


def write_first_estimate(project_folder):
    """Called by stage.py read: write the first estimate's two files (never a record file). The first estimate
    belongs to step 1, so nothing is written once the project holds scene files (a folder saved in a chat app that
    adopt reads, for example) or an estimate from the shots; stage.py estimate makes those. Returns the names
    written."""
    scenes_folder = Path(project_folder) / SCENES_FOLDER
    if scenes_folder.is_dir() and any(path.suffix == ".md" for path in scenes_folder.iterdir()):
        return []
    existing = read_estimate_json(project_folder)
    if existing and (existing.get("estimate") or {}).get("version") == VERSION_NAMES["v1"]:
        return []
    breakdown = load_breakdown(project_folder)
    prices, _ = PriceTable.load()
    film = film_estimate(breakdown, "v0", prices=prices)
    if nothing_to_estimate(film):
        return []
    written = write_estimate_files(project_folder, film, prices)
    note_in_manifest(project_folder, film, breakdown.schema, breakdown.words)
    return written


# ---------------------------------------------------------------- the command

def summary_lines(film):
    """The command's plain report: what it found, then what it made."""
    lines = []
    name = version_words(film)
    name = name[0].upper() + name[1:]
    if film.plans:
        for plan in film.plans:
            money = (", " + " / ".join(dollars(plan.money[level]["total"]) for level in PRICE_LEVELS)
                     + " (budget / mid / premium)") if film.money_shown else ""
            lines.append(f"Plan {plan.counts.get('plan')}: {minutes_range(plan.runtime_s)}, about "
                         f"{plural(plan.total_shots, 'shot')}{money}, about {whole(plan.hours['central'])} hours of the "
                         "user's time.")
    else:
        text = f"{name}: the film runs {minutes_range(film.runtime_s)}"
        if film.story_runtime_s and film.titles_s:
            low, central, high = (whole(value) for value in film.story_runtime_s)
            spread = f", {low} to {high}" if low != high else ""
            text += (f" ({central} seconds of story{spread}, plus {whole(film.titles_s)} of titles and credits)")
        if film.total_shots:
            text += f", about {plural(film.total_shots, 'shot')}"
        lines.append(text + ".")
        if film.money_shown and film.money:
            lines.append("Money: " + ", ".join(f"{LEVEL_WORDS[level].lower()} {dollars(film.money[level]['total'])}"
                                               for level in PRICE_LEVELS) + f". {film.money_note}")
        if film.hours_shown and film.hours:
            lines.append(f"The user's time: about {whole(film.hours['central'])} hours ({whole(film.hours['base'])} "
                         f"to {whole(film.hours['high'])}), about {whole(film.weeks['central'])} weeks at "
                         f"{whole(film.hours_per_week)} hours a week.")
    if not film.money_shown and film.money_note:
        lines.append(film.money_note)
    for warning in film.warnings:
        lines.append(f"To look at: {warning}")
    return lines


def run_estimate(context):
    project_folder = context.project
    breakdown = load_breakdown(project_folder)
    version = getattr(context.arguments, "version", None)
    if version == "v1" and not (breakdown.records_of("SHOT") or breakdown.records_of("SHOTLIST")):
        # The estimate from the shots needs shots; before any is written it would be the first estimate under
        # the wrong name, so the first estimate is made and called by its own name.
        context.say("No shot or shot list is written yet, so this is the first estimate, made from the words.")
        version = "v0"
    prices, _ = PriceTable.load()
    film = film_estimate(breakdown, version, prices=prices)
    if nothing_to_estimate(film):
        from .project_files import StageStop
        raise StageStop("There is nothing to estimate yet: read the story first (stage.py read).")
    for line in summary_lines(film):
        context.say(line)
    written = write_estimate_files(project_folder, film, prices)
    changed, changed_files, kept_locked = store_estimate_fields(project_folder, film, breakdown)
    note_in_manifest(project_folder, film, breakdown.schema, breakdown.words)
    if changed:
        try:
            from .project_files import Project
            Project(project_folder, breakdown.schema, breakdown.words).add_log_entry(
                f"Made {version_words(film)} and stored {plural(changed, 'planned figure')} it fills "
                f"({', '.join(changed_files)}).")
        except (OSError, ValueError):
            pass
    if kept_locked:
        context.say(f"Kept {plural(kept_locked, 'value')} on approved records unchanged.")
    context.say("Made: " + ", ".join(written) + (", and the planned figures in " + ", ".join(changed_files)
                                                   if changed_files else "") + ".")
    context.summary = (f"{VERSION_NAMES.get(film.version)}: {whole(film.runtime_s[1])} s, "
                       f"{whole(film.total_shots)} shots, money {'shown' if film.money_shown else 'not shown'}")
    return 0


def add_estimate_arguments(parser):
    parser.add_argument("--version", choices=["v0", "v1"], default=None,
                        help="v0 is the first estimate (from the words), v1 the estimate from the shots "
                             "(default: v1 once any shot or shot list exists)")


def register_commands(table):
    table.add("estimate", "Time and cost: the first estimate, or the estimate from the shots", run_estimate,
              add_estimate_arguments)
