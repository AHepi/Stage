"""checks_plan_generation_film.py: the PLAN and GEN checks of blueprint section 7.2, and the door to the FILM checks.

In plain words:
- PLAN-01 to PLAN-05 check the story plan (step 2): exactly one climax, with the one scene intensity 10 on it;
  every plant paid off, and no payoff without a plant or before it; a reason for every peak away from the climax;
  the scenes' planned lengths within step_outline_tolerance of the runtime target; no kept scene carrying a strand
  the plan cut;
- GEN-01 to GEN-17 lint the prompts that stage.py compile writes (add-on C, and step 10's compile --lint-only):
  the prompt within the model's limit; a clip length and resolution the model allows; no more speech than a clip
  holds; fixed descriptions, state lines and the look block pasted word for word, and not repeated when a start
  picture is attached; no readable text asked of the model; no negation of a visible thing outside the documented
  "No ..." lines; no dialogue sent to a silent model; the model's own speaker form; a held take never split; fresh
  model facts on a paid pack; no banned word; one on-screen speaker a clip; no public release while the rights are
  study_only; no reasons in a prompt; a cheap test before a dear take; relayed voices with their path and at most
  three named sounds;
- importing this module also imports film_pass.py, which registers FILM-01 to FILM-12 and the film strip
  (check_records loads this module under its planned name, so nothing else needs to list film_pass).

Where the GEN checks read the prompts. stage.py compile (work package 8) writes each scene's compiled prompts as
JSON files in "For machines - do not edit/prompts/". Each file holds one pack:

    {"scene": "SC10", "compiled_on": "2026-09-28", "model_facts_date": "2026-09-27",
     "paid": false, "release": "private",
     "clips": [{"clip": "SC10-SH150.1", "shot": "SC10-SH150", "model": "seedance-2.5",
                "length_s": 17, "resolution": "720p", "shape": "21:9",
                "prompt": "...", "negative": null,
                "inputs": {"start_picture": "PIC-SC10-SH150-START-01", "end_picture": null,
                           "references": [], "guide_video": null},
                "speeches": ["SC10-D10", "SC10-D11", "SC10-D12"],
                "sounds": ["chewing", "the room's low hum"]}]}

Only "clip", "shot", "model" and "prompt" are needed. Without "speeches", a speech counts as sent when its words
are in the prompt; without "subjects" (optional, state IDs), the shot's subject items are the people in frame;
"paid" (true only on a pack compile marks paid) is read by GEN-11 and "release" ("public" or "private") by GEN-14.
compile can also call lint_packs(run, packs, forced=True) on packs it holds in memory: with forced (compile
--force-model), GEN-02 and GEN-10 come out as notes.

Model facts come from adapters/video_models.json and adapters/image_models.json (work package 8), in the shape
of blueprint 8.2. While those files are missing, the checks that need them skip with a plain reason (tests give
stand-in facts through use_model_facts). Checks only read; every problem line has 7.2's form (level, check ID,
record, field, what is wrong, then the fix). Numbers come from rules/constants.json by name
(step_outline_tolerance, clip_speech_rule, handles_s, model_facts_max_age_days, on_screen_speakers_per_clip_max,
cheap_test_above_usd_per_take, named_sounds_per_prompt_max) and rules/limits.json (tokens_per_word_estimate);
word lists from rules/words.json (banned_prompt_words, allowed_negations).

Standard library only.

After the full run on The Catch (Project notes 31 and 32):
- GEN-05 leaves the room sound out; GEN-06 lets the model draw only one short mark (model_drawn) and finds capitals
  written with a capital on every word; GEN-15 leaves quoted script lines out.
"""

import datetime
import json
import math
import re
from dataclasses import dataclass, field as dataclass_field
from pathlib import Path

from . import film_pass  # noqa: F401  (registers FILM-01 to FILM-12 and the film pass report section)
from .check_records import register_check, same_scene, scene_of
from .derive_fields import (allowed_lengths, constant, element_of, held_take, number_of, project_prompt_swaps,
                            round_up_to, swap_prompt_words, swap_sources_banned)
from .film_pass import (MACHINE_FOLDER, breakdown_of, ends_before, film_scenes, id_range_pairs, in_pairs,
                        is_empty, is_kept, number_words, pairs_words, place_of, report, story_point_position)
from .record_format import load_json, normalise_word, split_item, split_list

PROMPTS_FOLDER = "prompts"
MODEL_FACTS_FILES = ("adapters/video_models.json", "adapters/image_models.json")
NO_PACKS = ("no compiled prompts yet: stage.py compile writes them to 'For machines - do not edit/prompts/' "
            "(add-on C, or step 10's compile --lint-only)")
NO_FACTS = ("the model facts files (adapters/video_models.json, adapters/image_models.json) are missing from this copy of "
            "the tools, so this check waits for them")
# 5.5 PROJECT intended_use values that release the film to other people (GEN-14; D4).
PUBLIC_USES = ("festival", "online_free", "online_monetised", "commercial")
# SPEECH path values that relay a voice through something, so the prompt must name the path (GEN-17; C3 L11, 7F).
RELAYED_PATHS = {
    "earpiece": ("earpiece",), "radio": ("radio",), "intercom": ("intercom",), "phone": ("phone",),
    "device_speaker": ("speaker",), "recording": ("recording", "recorded"), "helmet_inside": ("helmet",),
    "helmet_outside": ("helmet",), "through_glass": ("glass",),
}
# A start picture fixes appearance, so the prompt must not re-describe it (GEN-05, C3 L18): a clause of this many
# words or more taken from a fixed description, a state line or the look block counts as re-describing.
# [judgement: long enough that "on the left" or "the woman" never counts]
REDESCRIBED_CLAUSE_WORDS_MIN = 4
# A double-quoted quotation of the script inside a record's words.
QUOTED_WORDS = re.compile(r'["\u201c][^"\u201c\u201d]+["\u201d]')
# A reason (why, purpose, motif meaning) counts as travelling into the prompt when a clause of this many words or
# more from it is there (GEN-15). [judgement, as above]
REASON_CLAUSE_WORDS_MIN = 4
# GEN-06 (C3 L21, K17): the ways a prompt asks the model to write words. [judgement, from C3 §13A]
WRITING_REQUESTS = [
    # a surface's words: "a sign on the fridge reads ...", "letters that spell ...", "a label which says ..." ("says"
    # alone is left out: it is how every spoken line is written)
    re.compile(r"\b(?:text|letters|lettering|writing|signs?|labels?|captions?|subtitles?|title card)\b"
               r"[^.]{0,40}?\b(?:reads?|reading|spells?|spelling|(?:that|which) says?)\b", re.IGNORECASE),
    re.compile(r"\b(?:backwards?|reversed|mirror(?:ed)?)\s+(?:text|writing|letters|lettering|words)\b", re.IGNORECASE),
    re.compile(r"\b(?:text|writing|letters|lettering|words)\s+(?:backwards?|reversed|in reverse)\b", re.IGNORECASE),
]
# GEN-07 (C3 L14): negation words, and the negations compile itself writes that are allowed: a behaviour held back
# (8.1 rule 9, D15 rule 6: "He does not look at her.", "The camera does not move.") and the off-screen voice
# (C3 §7F: "he is not visible").
NEGATION = re.compile(r"\b(?:no|not|without)\b|\b\w+n't\b", re.IGNORECASE)
ALLOWED_NEGATION_PHRASES = re.compile(r"\b(?:does|do|did)\s+not\s+\w+|\b(?:is|are)\s+not\s+visible\b", re.IGNORECASE)
# GEN-15: the records' own IDs, which never belong in a prompt (the reasons' because list).
STAGE_IDENTIFIER = re.compile(r"\b(?:SC\d{2,3}[A-Z]?(?:-[A-Z]+\d+)?|(?:CH|VO|LOC|PR|TX|MO|CAM|WR|LK|CR|VS|RC|LX|PL|FT|"
                              r"ST|CF|SQ|CP|FIND|CHOICE|RT|PIC|PV|TK|VT|FX|MU)-[A-Z0-9][A-Z0-9-]*)\b")
QUOTES = {"“": '"', "”": '"', "‘": "'", "’": "'"}

_MODEL_FACTS_OVERRIDE = {"facts": None, "used": False}


# ---------------------------------------------------------------- small helpers

def normalised(text):
    """Text for comparing prompts with records: straight quotes, one space, no case."""
    text = str(text or "")
    for curly, straight in QUOTES.items():
        text = text.replace(curly, straight)
    return re.sub(r"\s+", " ", text).strip().casefold()


def word_count(text):
    return len([piece for piece in (text or "").split() if re.search(r"\w", piece)])


def clauses(text, least):
    """The clauses of a text (split at . ; , : and dashes) with at least `least` words, normalised."""
    pieces = re.split(r"[.;,:!?]\s*|\s+[-–—]\s+|\(|\)", str(text or ""))
    return [normalised(piece) for piece in pieces if word_count(piece) >= least]


def tokens_per_word():
    try:
        return float(load_json("rules/limits.json").get("tokens_per_word_estimate", {}).get("value", 1.4))
    except (OSError, ValueError, AttributeError):
        return 1.4


def today():
    return datetime.date.today()


def read_date(text):
    try:
        return datetime.date.fromisoformat(str(text).strip()[:10])
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- PLAN-01 one climax, intensity 10 on it

@register_check("PLAN-01", level="E", build=1,
                title="Not exactly one climax; scene intensity 10 not on it",
                plain="does not have exactly one climax carrying the film's one highest scene intensity")
def check_plan_01(run):
    """PLAN climax names one scene or one range of scenes. Every kept scene with scene_intensity 10 lies inside it;
    and when the climax's scenes are here with their intensities, at least one of them is 10. Scenes of the climax
    left out of a partial example are skipped (not in the excerpt)."""
    plan = run.record("PLAN")
    if plan is None or is_empty(plan.get("climax")):
        return []
    place = place_of(run, plan, "climax")
    pairs = id_range_pairs(plan.get("climax"))
    problems = []
    if len(pairs) != 1:
        problems.append(report(
            run, "E", "PLAN-01", plan, "climax",
            f"{plan.get('climax')} names {len(pairs)} climaxes; a film has exactly one (one scene or one range)",
            "Fix: name the one scene or range where the core value turns for the last time, and put the other "
            "readings to the user as a choice.", place))
        return problems
    tens = [scene for scene in film_scenes(run) if number_of(scene.get("scene_intensity")) == 10]
    for scene in tens:
        if not in_pairs(scene.identifier, pairs):
            problems.append(report(
                run, "E", "PLAN-01", scene, "scene_intensity",
                f"10 is outside the climax {pairs_words(pairs)}; the film's one scene intensity 10 (or one 10 range) "
                "belongs on the climax",
                f"Fix: lower {scene.identifier}'s scene intensity below 10, or make it the climax.",
                place_of(run, scene, "scene_intensity")))
    if not tens:
        first, last = pairs[0]
        present = [scene for scene in film_scenes(run) if in_pairs(scene.identifier, pairs)]
        left_out = [identifier for identifier in (first, last) if not any(same_scene(identifier, scene.identifier)
                                                                          for scene in present)]
        if left_out or not present:
            reason = "not in the excerpt" if any(run.scene_left_out(identifier) for identifier in (left_out or [first])) \
                else "the climax's scenes have no records yet"
            run.skip("PLAN-01", f"the climax {pairs_words(pairs)} is not here to read its scene intensity ({reason})")
        elif all(number_of(scene.get("scene_intensity")) is not None for scene in present):
            written = ", ".join(f"{scene.identifier} {scene.get('scene_intensity')}" for scene in present)
            problems.append(report(
                run, "E", "PLAN-01", plan, "climax",
                f"{pairs_words(pairs)} holds no scene of intensity 10 ({written})",
                "Fix: give the climax the film's one scene intensity 10, or name the climax where the 10 is.",
                place))
    return problems


# ---------------------------------------------------------------- PLAN-02 plants and payoffs

@register_check("PLAN-02", level="E", build=1,
                title="A plant without a payoff, or a payoff without a plant",
                plain="has a plant that is never paid off, or a payoff with no plant before it")
def check_plan_02(run):
    """Every PLANT has planted_at and paid_off_at (an `open` or `none` value counts as missing), and its payoff does
    not come before its plant in the story (scene order, then lines or beats when the story or the stored beats
    tell)."""
    breakdown = breakdown_of(run)
    problems = []
    for plant in run.records("PLANT"):
        planted, paid = plant.get("planted_at"), plant.get("paid_off_at")
        if is_empty(planted):
            problems.append(report(
                run, "E", "PLAN-02", plant, "planted_at",
                "is missing, so this payoff has no plant" if not is_empty(paid) else
                "and paid_off_at are both missing",
                "Fix: write where the story plants it, as a story point (a scene and a quote), or cut the record.",
                place_of(run, plant, "planted_at")))
            continue
        if is_empty(paid):
            problems.append(report(
                run, "E", "PLAN-02", plant, "paid_off_at",
                "is missing, so this plant is never paid off",
                "Fix: write where the story pays it off, as a story point, or cut the plant (and its emphasis).",
                place_of(run, plant, "paid_off_at")))
            continue
        plant_position = story_point_position(breakdown, planted)
        payoff_position = story_point_position(breakdown, paid)
        if ends_before(payoff_position, plant_position) is True:
            problems.append(report(
                run, "E", "PLAN-02", plant, "paid_off_at",
                f"{paid} comes before its plant {planted}, so the payoff has no plant before it",
                "Fix: swap the two story points if they were written the wrong way round, or find the plant that "
                "comes earlier in the story.", place_of(run, plant, "paid_off_at")))
    return problems


# ---------------------------------------------------------------- PLAN-03 peaks away from the climax

@register_check("PLAN-03", level="W", build=1,
                title="A peak away from the climax without a reason",
                plain="places a peak away from the climax without saying why")
def check_plan_03(run):
    """Each PLAN peak whose scene lies outside the climax needs a reason (K12: counterpoint is a reason)."""
    plan = run.record("PLAN")
    if plan is None:
        return []
    pairs = id_range_pairs(plan.get("climax"))
    if not pairs:
        run.skip("PLAN-03", "the story plan names no climax yet")
        return []
    problems = []
    for written in plan.get_all("peak"):
        item = split_item(written, run.schema.field("PLAN", "peak"))
        scene_identifier = (item.get("scene") or "").strip()
        if not scene_identifier or in_pairs(scene_identifier, pairs):
            continue
        if is_empty(item.get("reason")):
            problems.append(report(
                run, "W", "PLAN-03", plan, "peak",
                f"{item.first} peaks in {scene_identifier}, away from the climax {pairs_words(pairs)}, with no reason",
                f"Fix: add '| reason: ...' naming what in the story peaks in {scene_identifier}, or move the peak to "
                "the climax.", place_of(run, plan, "peak", item.first)))
    return problems


# ---------------------------------------------------------------- PLAN-04 step outline against the runtime target

@register_check("PLAN-04", level="W", build=1,
                title="Step-outline targets outside ±10% of the runtime target",
                plain="plans scene lengths that add up to more or less than the film's target length allows")
def check_plan_04(run):
    """The kept scenes' target_duration_s added up, against PROJECT runtime_target_s (with as_written, the first
    estimate, PLAN runtime_estimate), within step_outline_tolerance. It needs every scene of the film, each with its
    target."""
    project = run.project_record
    plan = run.record("PLAN")
    if project is None:
        return []
    written = project.get("runtime_target_s")
    target, what = number_of(written), "the runtime target"
    if target is None and plan is not None and normalise_word(written or "") in ("as_written", ""):
        target, what = number_of(plan.get("runtime_estimate")), "the first estimate (the target is as written)"
    if target is None or target <= 0:
        run.skip("PLAN-04", "no runtime target or first estimate to compare with yet")
        return []
    if run.scope_scenes is not None:
        run.skip("PLAN-04", "needs the whole film's scenes, and the project's scope is part of the film "
                            "(not in the excerpt)")
        return []
    scenes = film_scenes(run)
    missing = [scene.identifier for scene in scenes if number_of(scene.get("target_duration_s")) is None]
    if not scenes or missing:
        run.skip("PLAN-04", "runs once every kept scene has its planned length (target_duration_s)"
                 + (f"; not yet: {', '.join(missing[:3])}" if missing else ""))
        return []
    total = sum(number_of(scene.get("target_duration_s")) for scene in scenes)
    tolerance = number_of(constant(run.constants, "step_outline_tolerance", 0.1), 0.1)
    if abs(total - target) > tolerance * target + 1e-9:
        share = (total - target) / target
        return [report(
            run, "W", "PLAN-04", project, "runtime_target_s",
            f"the {len(scenes)} kept scenes' targets add up to {number_words(total)} s, {abs(share):.0%} "
            f"{'over' if share > 0 else 'under'} {what} of {number_words(target)} s (allowed within "
            f"{tolerance:.0%})",
            "Fix: " + ("trim, merge or fold scenes in the step outline" if share > 0 else
                       "keep more of the story in the step outline")
            + ", or change the runtime target through a choice.", place_of(run, project, "runtime_target_s"))]
    return []


# ---------------------------------------------------------------- PLAN-05 cut strands

@register_check("PLAN-05", level="E", build=1,
                title="A kept scene citing a cut strand",
                plain="keeps a scene that carries a line of events the plan cut")
def check_plan_05(run):
    """A kept scene's strands must not name a STRAND whose decision is cut."""
    cut = {strand.identifier for strand in run.records("STRAND")
           if normalise_word(strand.get("decision") or "") == "cut"}
    problems = []
    if not cut:
        return problems
    for scene in film_scenes(run):
        for strand in split_list(scene.get("strands") or ""):
            if strand in cut and run.in_scope(scene.identifier):
                problems.append(report(
                    run, "E", "PLAN-05", scene, "strands",
                    f"{strand} is a strand the plan cuts, yet this kept scene carries it",
                    f"Fix: cut, fold or merge {scene.identifier} with the strand, or keep the strand through a choice.",
                    place_of(run, scene, "strands")))
    return problems


# ---------------------------------------------------------------- the model facts (adapters) and the compiled packs

class ModelFacts:
    """The dated model facts of adapters/*.json: models by name, their aliases, the date they were checked."""

    def __init__(self, documents):
        self.models = {}
        self.aliases = {}
        self.retired = {}
        dates = []
        self.stand_in = False
        for document in documents:
            if not isinstance(document, dict):
                continue
            self.stand_in = self.stand_in or bool(document.get("stand_in"))
            date = read_date(document.get("checked_on"))
            if date:
                dates.append(date)
            for name, facts in (document.get("models") or {}).items():
                if not isinstance(facts, dict):
                    continue
                self.models[name] = facts
                self.aliases[normalised(name)] = name
                for alias in facts.get("aliases") or []:
                    self.aliases[normalised(alias)] = name
            self.retired.update(document.get("retired") or {})
        self.checked_on = min(dates) if dates else None

    def find(self, name):
        canonical = self.aliases.get(normalised(name))
        return (canonical, self.models[canonical]) if canonical else (None, None)


def use_model_facts(document):
    """Use these model facts (one dict shaped like adapters/video_models.json, or a list of them) instead of the
    adapter files, for tests and dry runs; None goes back to the files."""
    if document is None:
        _MODEL_FACTS_OVERRIDE.update(facts=None, used=False)
    else:
        documents = document if isinstance(document, list) else [document]
        _MODEL_FACTS_OVERRIDE.update(facts=ModelFacts(documents), used=True)


def model_facts(run):
    """The model facts for this run, or None while no adapter file exists."""
    if _MODEL_FACTS_OVERRIDE["used"]:
        return _MODEL_FACTS_OVERRIDE["facts"]
    key = "plan_generation_film.model_facts"
    if key in run.cache:
        return run.cache[key]
    documents = []
    for relative in MODEL_FACTS_FILES:
        try:
            documents.append(load_json(relative))
        except (OSError, ValueError):
            continue
    facts = ModelFacts(documents) if documents else None
    run.cache[key] = facts
    return facts


@dataclass
class Clip:
    """One compiled clip: its data from the pack, its shot record and its pack."""
    identifier: str
    shot_identifier: str
    shot: object
    model: str
    data: dict
    pack: dict = dataclass_field(default_factory=dict)

    @property
    def prompt(self):
        return str(self.data.get("prompt") or "")

    @property
    def inputs(self):
        return self.data.get("inputs") or {}


def read_packs(run):
    """The packs stage.py compile wrote ('For machines - do not edit/prompts/*.json'), each a dict with 'clips'."""
    key = "plan_generation_film.packs"
    if key in run.cache:
        return run.cache[key]
    packs = []
    project = getattr(run, "project", None)
    folder = Path(project.folder) / MACHINE_FOLDER / PROMPTS_FOLDER if project is not None else None
    if folder is not None and folder.is_dir():
        for path in sorted(folder.glob("*.json")):
            try:
                with open(path, encoding="utf-8") as handle:
                    data = json.load(handle)
            except (OSError, ValueError):
                run.skip("GEN-01", f"'{path.name}' in the prompts folder could not be read as JSON; compile it again")
                continue
            if isinstance(data, dict) and isinstance(data.get("clips"), list):
                data = dict(data, _file=path.name)
                packs.append(data)
    run.cache[key] = packs
    return packs


def clips_of(run, packs):
    clips = []
    for pack in packs:
        for data in pack.get("clips") or []:
            if not isinstance(data, dict):
                continue
            shot_identifier = str(data.get("shot") or re.sub(r"\.\d+$", "", str(data.get("clip") or ""))).strip()
            identifier = str(data.get("clip") or f"{shot_identifier}.1").strip()
            if not run.in_scope(shot_identifier):
                continue
            shot = run.record(shot_identifier)
            clips.append(Clip(identifier, shot_identifier, shot if shot is not None and shot.type_name == "SHOT" else None,
                              str(data.get("model") or "").strip(), data, pack))
    return clips


def compiled_clips(run, check_id):
    """The clips of the compiled packs whose shots this run checks; with none, one skip line."""
    key = "plan_generation_film.clips"
    if key not in run.cache:
        run.cache[key] = clips_of(run, read_packs(run))
    clips = run.cache[key]
    if not clips:
        run.skip(check_id, NO_PACKS)
    return clips


def clip_problem(run, level, check_id, clip, field_name, what, fix):
    """A problem line about a clip, named by its clip ID and placed at its shot's heading."""
    file_name, line_number = None, None
    if clip.shot is not None:
        file_name, line_number, _ = run.location(clip.shot)
    return run.problem(level, check_id, clip.identifier, field_name, what, fix, line_number=line_number,
                       file_name=file_name)


def facts_for_clip(run, facts, clip, check_id):
    canonical, found = facts.find(clip.model)
    if found is None:
        run.skip(check_id, f"model '{clip.model}' of {clip.identifier} is not in the model facts")
    return canonical, found


# ---------------------------------------------------------------- speeches in a clip

def speech_entry(run, identifier):
    breakdown = breakdown_of(run)
    return breakdown.speech(identifier)


def speech_words_text(entry):
    text = (entry or {}).get("text") or ""
    return re.sub(r"\([^)]*\)", " ", text).strip()


def heard(clip):
    """[(speech ID, hear item)] of the clip's shot."""
    if clip.shot is None:
        return []
    found = []
    for written in clip.shot.get_all("hear"):
        item = split_item(written)
        if item.first and not is_empty(item.first):
            found.append((item.first.strip(), item))
    return found


def clip_speeches(run, clip):
    """The speech IDs whose words the clip sends: its 'speeches' list, else the shot's heard speeches whose words are
    in the prompt."""
    listed = clip.data.get("speeches")
    if isinstance(listed, list):
        return [str(identifier) for identifier in listed]
    prompt = normalised(clip.prompt)
    sent = []
    for identifier, _ in heard(clip):
        words = normalised(speech_words_text(speech_entry(run, identifier)))
        if words and words in prompt:
            sent.append(identifier)
    return sent


def prompt_without_speeches(run, clip):
    """The prompt with the words of every heard speech taken out (dialogue is quoted exactly and never linted as
    picture words)."""
    prompt = clip.prompt
    for identifier, _ in heard(clip):
        words = speech_words_text(speech_entry(run, identifier))
        if words:
            prompt = re.sub(re.escape(words), " ", prompt, flags=re.IGNORECASE)
    return prompt


def level_for(check_id, forced):
    """compile --force-model tests one adapter's syntax: its GEN-02 and GEN-10 lines are notes (7.1)."""
    return "N" if forced and check_id in ("GEN-02", "GEN-10") else None


# ---------------------------------------------------------------- the GEN checks, one function each over clips

def lint_gen_01(run, clips, facts, forced=False):
    problems = []
    per_word = tokens_per_word()
    for clip in clips:
        canonical, found = facts_for_clip(run, facts, clip, "GEN-01")
        if found is None:
            continue
        limit = found.get("prompt_limit") or {}
        prompt = clip.prompt
        measures = [("characters", len(prompt)), ("tokens", int(math.ceil(word_count(prompt) * per_word))),
                    ("words", word_count(prompt))]
        for unit, amount in measures:
            most = number_of(limit.get(unit))
            if most is not None and amount > most:
                estimate = " (words x the tokens-per-word estimate)" if unit == "tokens" else ""
                problems.append(clip_problem(
                    run, "E", "GEN-01", clip, "prompt",
                    f"has {amount} {unit}{estimate}, over {canonical}'s limit of {number_words(most)}",
                    "Fix: shorten the records the prompt is built from (moments, does, the look block's extra words) "
                    "or route the shot to a model with a longer limit, then compile again."))
                break
    return problems


def forced_length(facts_model, clip):
    """The length a model forces for this clip (Veo's 8 s for 1080p, 4K or references), or None."""
    spec = facts_model.get("length_s") or {}
    for key, conditions in spec.items():
        match = re.fullmatch(r"forced_(\d+(?:\.\d+)?)_when", key)
        if not match or not isinstance(conditions, list):
            continue
        wanted = {normalised(condition) for condition in conditions}
        resolution = normalised(clip.data.get("resolution"))
        references = clip.inputs.get("references")
        if resolution in wanted or ("references" in wanted and references):
            return float(match.group(1))
    return None


def lint_gen_02(run, clips, facts, forced=False):
    problems = []
    level = level_for("GEN-02", forced) or "E"
    for clip in clips:
        canonical, found = facts_for_clip(run, facts, clip, "GEN-02")
        if found is None:
            continue
        length = number_of(clip.data.get("length_s"))
        lengths = allowed_lengths(found)
        if length is not None and lengths and not any(abs(length - allowed) < 1e-6 for allowed in lengths):
            shown = ", ".join(number_words(value) for value in lengths) if len(lengths) <= 8 else \
                f"{number_words(lengths[0])} to {number_words(lengths[-1])}"
            problems.append(clip_problem(
                run, level, "GEN-02", clip, "length_s",
                f"{number_words(length)} s is not a clip length {canonical} allows ({shown} s)",
                "Fix: compile again so the clip is rounded up to an allowed length, or route the shot to another "
                "model."))
            continue
        must = forced_length(found, clip)
        if length is not None and must is not None and abs(length - must) > 1e-6:
            problems.append(clip_problem(
                run, level, "GEN-02", clip, "length_s",
                f"{number_words(length)} s is not the {number_words(must)} s {canonical} forces for this resolution "
                "or for references",
                f"Fix: make the clip {number_words(must)} s, or drop the resolution or references that force it."))
            continue
        for key, facts_key in (("resolution", "resolution"), ("shape", "shapes")):
            written = clip.data.get(key)
            allowed = found.get(facts_key)
            if written and isinstance(allowed, list) and normalised(written) not in {normalised(value) for value in allowed}:
                problems.append(clip_problem(
                    run, level, "GEN-02", clip, key,
                    f"{written} is not a {key} {canonical} allows ({', '.join(str(value) for value in allowed)})",
                    f"Fix: compile at an allowed {key} (and crop or upscale in finishing), or route the shot to "
                    "another model."))
                break
    return problems


def lint_gen_03(run, clips, facts=None, forced=False):
    breakdown = breakdown_of(run)
    rule = constant(run.constants, "clip_speech_rule", {}) or {}
    margin = number_of(rule.get("margin_s") if isinstance(rule, dict) else None, 1.0)
    problems = []
    for clip in clips:
        length = number_of(clip.data.get("length_s"))
        speeches = clip_speeches(run, clip)
        if length is None or not speeches:
            continue
        need = 0.0
        parts = []
        for identifier in speeches:
            entry = speech_entry(run, identifier) or {}
            words = entry.get("words")
            if words is None:
                words = word_count(speech_words_text(entry))
            pace = breakdown.pace_of(entry.get("speaker") or "")
            need += words / pace
            parts.append(f"{identifier} {words} words at {number_words(pace)}")
        if need > length - margin + 1e-9:
            problems.append(clip_problem(
                run, "E", "GEN-03", clip, "hear",
                f"its speech needs {number_words(round(need, 1))} s ({'; '.join(parts)}), more than the "
                f"{number_words(length)} s clip holds after the {number_words(margin)} s margin",
                "Fix: give the shot more screen time, split the speech at a planned cut, or route the shot to a model "
                "whose clip is long enough."))
    return problems


def subject_references(clip):
    """The state IDs (or element IDs) of the people in the clip: its 'subjects' list, else the shot's subjects."""
    listed = clip.data.get("subjects")
    if isinstance(listed, list):
        return [str(reference) for reference in listed]
    if clip.shot is None:
        return []
    return [split_item(written).first.strip() for written in clip.shot.get_all("subject")
            if split_item(written).first and not is_empty(split_item(written).first)]


def appearance_texts(run, clip):
    """[(field, what it is, text)] of the fixed descriptions, state lines and look block the clip's picture uses."""
    texts = []
    for reference in subject_references(clip):
        element = run.record(element_of(reference))
        if element is not None and not is_empty(element.get("fixed_description")):
            texts.append(("subject", f"{element.identifier}'s fixed description", element.get("fixed_description")))
        state = run.record(reference)
        if state is not None and state.type_name == "STATE" and not is_empty(state.get("state_line")):
            texts.append(("subject", f"{state.identifier}'s state line", state.get("state_line")))
    look_identifier = clip.data.get("look")
    if not look_identifier:
        scene = run.record(scene_of(clip.shot_identifier))
        look_identifier = scene.get("look") if scene is not None and scene.type_name == "SCENE" else None
    look = run.record(look_identifier) if look_identifier else None
    if look is not None and not is_empty(look.get("look_block")):
        texts.append(("look", f"{look.identifier}'s look block", look.get("look_block")))
    return texts


def turned_sides(text):
    """A record's words with every left and right turned (the form compile pastes for an element shown pre-reversed)."""
    return re.sub(r"\b(?:left|right)\b", lambda match: {"left": "right", "right": "left"}[match.group(0).lower()],
                  str(text or ""), flags=re.IGNORECASE)


def lint_gen_04(run, clips, facts=None, forced=False):
    problems = []
    for clip in clips:
        if clip.inputs.get("start_picture"):
            continue
        prompt = normalised(clip.prompt)
        for field_name, what, text in appearance_texts(run, clip):
            # the one change allowed: left and right turned, where the picture shows the element pre-reversed
            # (a mirrored element made as it appears, or a normal one made before the clip's flip; 8.5, B1 method 1)
            # the one change allowed: left and right turned, and the project's word swaps made on every word
            swapped = swap_prompt_words(text, prompt_swaps(run))
            if normalised(text) not in prompt and normalised(turned_sides(text)) not in prompt and \
                    normalised(swapped) not in prompt and normalised(turned_sides(swapped)) not in prompt:
                problems.append(clip_problem(
                    run, "E", "GEN-04", clip, field_name,
                    f"the prompt does not hold {what} word for word",
                    "Fix: compile again from the record (the words are pasted, never paraphrased); if the record "
                    "changed, the prompt is stale."))
    return problems


def prompt_without_sounds(clip):
    """The prompt with its sound sentences taken out (the effects and the room sound): a room sound that begins with
    the place's words ("a small sealed room at dawn: the air handling") describes what is heard, not what is seen,
    so it never counts as re-describing the place for GEN-05."""
    prompt = str(clip.prompt or "")
    for sound in clip.data.get("sounds") or []:
        text = re.sub(r"^room sound:\s*", "", str(sound or ""), flags=re.IGNORECASE).strip().rstrip(".")
        if text:
            prompt = re.sub(re.escape(text), " ", prompt, flags=re.IGNORECASE)
    return prompt


def lint_gen_05(run, clips, facts=None, forced=False):
    problems = []
    for clip in clips:
        if not clip.inputs.get("start_picture"):
            continue
        prompt = normalised(prompt_without_sounds(clip))
        for _, what, text in appearance_texts(run, clip):
            found = normalised(text) in prompt or any(piece in prompt
                                                     for piece in clauses(text, REDESCRIBED_CLAUSE_WORDS_MIN))
            if found:
                problems.append(clip_problem(
                    run, "E", "GEN-05", clip, "prompt",
                    f"has a start picture attached and still re-describes {what}",
                    "Fix: with a start picture the prompt is motion only; call the people 'the woman', 'the man' and "
                    "leave appearance, costume and set to the picture."))
                break
    return problems


def texts_in_frame(run, clip):
    """TEXT records in the clip's frame: the shot's text field, and TEXT whose `on` is a thing in the shot."""
    if clip.shot is None:
        return []
    found = []
    for identifier in split_list(clip.shot.get("text") or ""):
        record = run.record(identifier)
        if record is not None and record.type_name == "TEXT" and record not in found:
            found.append(record)
    things = {element_of(split_item(written).first or "") for written in clip.shot.get_all("thing")}
    things = {thing for thing in things if thing and not is_empty(thing)}
    for record in run.records("TEXT"):
        on = element_of(record.get("on") or "")
        # a title card is on nothing: "on: none" never matches a shot's "thing: none"
        if on and not is_empty(on) and on in things and record not in found:
            found.append(record)
    return found


def is_single_mark(words):
    """True for one short mark a model may draw itself (a single letter, digit or sign of up to 3 characters)."""
    return len(words.split()) == 1 and len(words) <= 3


def words_asked_for(words, prompt):
    """True when a prompt asks for a text's words. Words printed in capitals are found as printed ("THE END") or
    with a capital on every word ("The End", "The Catch"), never inside lower-case prose ("the end of the corridor");
    other words are found without regard to case."""
    pattern = r"(?<!\w)" + re.escape(words) + r"(?!\w)"
    if words != words.upper() or not re.search(r"[A-Z]", words):
        return bool(re.search(pattern, prompt, re.IGNORECASE))
    if len(words.split()) < 2:
        return bool(re.search(pattern, prompt))
    return any(all(piece[:1].isupper() for piece in match.group(0).split() if piece[:1].isalpha())
               for match in re.finditer(pattern, prompt, re.IGNORECASE))


def lint_gen_06(run, clips, facts=None, forced=False):
    problems = []
    for clip in clips:
        prompt = prompt_without_speeches(run, clip)
        reported = False
        for text in texts_in_frame(run, clip):
            words = (text.get("words") or "").strip().strip('"')
            if not words or is_empty(words):
                continue
            drawn = normalise_word(text.get("method") or "") == "model_drawn"
            if drawn and is_single_mark(words):
                continue  # a single mark the shot is about, drawn by the model and checked in the take
            if words_asked_for(words, prompt):
                problems.append(clip_problem(
                    run, "E", "GEN-06", clip, "text",
                    f"asks the model to draw the words of {text.identifier} ('{words}')" +
                    ("; model_drawn is only for one short mark, such as a single letter" if drawn else ""),
                    "Fix: ask for a plain, unmarked surface; the words are drawn as a text graphic and composited "
                    "after any flip."))
                reported = True
                break
        if reported:
            continue
        for pattern in WRITING_REQUESTS:
            match = pattern.search(prompt)
            if match:
                problems.append(clip_problem(
                    run, "E", "GEN-06", clip, "prompt",
                    f"asks the model for readable or backwards text ('{match.group(0)}')",
                    "Fix: ask for a plain, unmarked surface; readable text is a text graphic composited in finishing."))
                break
    return problems


def sentences(text):
    return [piece.strip() for piece in re.split(r"(?<=[.!?])\s+|\n+", text or "") if piece.strip()]


def lint_gen_07(run, clips, facts=None, forced=False):
    allowed_lines = {normalised(line) for line in (run.words.get("allowed_negations") or {}).get("lines", [])}
    problems = []
    for clip in clips:
        for sentence in sentences(prompt_without_speeches(run, clip)):
            if normalised(sentence) in allowed_lines:
                continue
            rest = ALLOWED_NEGATION_PHRASES.sub(" ", sentence)
            match = NEGATION.search(rest)
            if match:
                shown = sentence if len(sentence) <= 80 else sentence[:77] + "..."
                problems.append(clip_problem(
                    run, "E", "GEN-07", clip, "prompt",
                    f"negates a visible thing ('{shown}'); only the documented 'No ...' lines may negate",
                    "Fix: describe what is there instead (plain bare walls, an empty table), put the thing in the "
                    "model's negative field when it has one, or write a behaviour held back as 'does not'."))
                break
    return problems


def is_silent_model(found):
    audio = found.get("audio")
    if audio is False:
        return True
    return isinstance(audio, str) and normalised(audio).split(",")[0].strip() in ("none", "silent", "no")


def lint_gen_08(run, clips, facts, forced=False):
    problems = []
    for clip in clips:
        canonical, found = facts_for_clip(run, facts, clip, "GEN-08")
        if found is None or not is_silent_model(found):
            continue
        speeches = clip_speeches(run, clip)
        sounds = clip.data.get("sounds") or []
        audio_text = clip.data.get("audio")
        if speeches or sounds or audio_text:
            sent = "dialogue" if speeches else "sound"
            problems.append(clip_problem(
                run, "E", "GEN-08", clip, "prompt",
                f"sends {sent} to {canonical}, a model that makes no sound",
                "Fix: take the dialogue and sound out of this prompt (write 'she speaks' only as visible behaviour) "
                "and make the voice and sound separately, or route the shot to a model with sound."))
    return problems


def speaker_form(found):
    """(template, quoted, colon) of a model's speaker form, or None."""
    template = found.get("speaker")
    if not template:
        return None
    quoted = bool(re.search(r"[\"“]\{line\}", template))
    if found.get("speaker_quotes") is False:
        quoted = False
    colon = bool(re.search(r":\s*[\"“]?\{line\}", template))
    return template, quoted, colon


def lint_gen_09(run, clips, facts, forced=False):
    problems = []
    for clip in clips:
        canonical, found = facts_for_clip(run, facts, clip, "GEN-09")
        if found is None:
            continue
        form = speaker_form(found)
        if form is None:
            continue
        template, quoted, colon = form
        prompt = clip.prompt
        for curly, straight in QUOTES.items():
            prompt = prompt.replace(curly, straight)
        for identifier in clip_speeches(run, clip):
            words = speech_words_text(speech_entry(run, identifier))
            if not words:
                continue
            match = re.search(re.escape(words), prompt, re.IGNORECASE)
            if not match:
                continue
            before = prompt[:match.start()].rstrip()
            after = prompt[match.end():].lstrip()
            is_quoted = before.endswith('"') and after.startswith('"')
            lead = before[:-1].rstrip() if is_quoted else before
            wrong = []
            if quoted != is_quoted:
                wrong.append("with quotation marks" if is_quoted else "without quotation marks")
            if colon and not lead.endswith(":"):
                wrong.append("without the colon before the line")
            if wrong:
                problems.append(clip_problem(
                    run, "E", "GEN-09", clip, "hear",
                    f"{identifier} is written {' and '.join(wrong)}; {canonical}'s speaker form is {template}",
                    f"Fix: compile again with {canonical}'s own speaker form."))
    return problems


def lint_gen_10_packs(run, clips, forced=False):
    """A held take compiled as more than one clip."""
    level = level_for("GEN-10", forced) or "E"
    breakdown = breakdown_of(run)
    by_shot = {}
    for clip in clips:
        by_shot.setdefault(clip.shot_identifier, []).append(clip)
    problems = []
    for shot_identifier, shot_clips in by_shot.items():
        shot = shot_clips[0].shot
        if shot is None or len(shot_clips) < 2:
            continue
        held, why = held_take(breakdown, shot)
        if held:
            problems.append(clip_problem(
                run, level, "GEN-10", shot_clips[1], "held",
                f"splits {shot_identifier}, a held take ({why}), into {len(shot_clips)} chained clips",
                "Fix: route the shot whole to a model that allows its length, or redesign it with a motivated cut; "
                "a held take is never chained."))
    return problems


def lint_gen_10_records(run, facts, forced=False):
    """A held take longer, with its handles, than any model in the model facts allows."""
    level = level_for("GEN-10", forced) or "E"
    breakdown = breakdown_of(run)
    handles = number_of(constant(run.constants, "handles_s", 0.75), 0.75)
    problems = []
    for shot in run.records("SHOT"):
        if not shot.identifier or not run.in_scope(shot.identifier):
            continue
        scene = run.record(scene_of(shot.identifier))
        if scene is not None and scene.type_name == "SCENE" and not is_kept(scene):
            continue
        held, why = held_take(breakdown, shot)
        seconds = number_of(shot.get("screen_time"))
        if not held or seconds is None:
            continue
        needed = seconds + 2 * handles
        allowing = [name for name, found in facts.models.items()
                    if round_up_to(needed, allowed_lengths(found) or []) is not None]
        if not allowing:
            longest = max((max(allowed_lengths(found) or [0]) for found in facts.models.values()), default=0)
            problems.append(report(
                run, level, "GEN-10", shot, "screen_time",
                f"{number_words(seconds)} s makes a held take ({why}) of {number_words(needed)} s with handles, longer "
                f"than any model allows (the longest is {number_words(longest)} s), and a held take is never split",
                "Fix: redesign the shot with a motivated cut into shots each short enough for one clip, or shorten "
                "it.", place_of(run, shot, "screen_time")))
    return problems


def pack_scene(pack, clips):
    if pack.get("scene"):
        return str(pack["scene"])
    for clip in clips:
        if clip.pack is pack:
            return scene_of(clip.shot_identifier)
    return None


def lint_gen_11(run, packs, clips, facts, forced=False):
    most = number_of(constant(run.constants, "model_facts_max_age_days", 30), 30)
    problems = []
    for pack in packs:
        if pack.get("paid") is not True:
            continue
        scene_identifier = pack_scene(pack, clips)
        if scene_identifier and not run.in_scope(scene_identifier):
            continue
        date = read_date(pack.get("model_facts_date")) or (facts.checked_on if facts is not None else None)
        record = run.record(scene_identifier) if scene_identifier else None
        label = scene_identifier or pack.get("_file") or "a pack"
        place = run.location(record)[:2] if record is not None else (None, None)
        if date is None:
            problems.append(run.problem(
                "E", "GEN-11", label, "model_facts_date",
                "the paid pack has no model facts date, so its prices cannot be trusted",
                "Fix: refresh the model facts (stage.py refresh-models --propose, then --apply) and compile again.",
                file_name=place[0], line_number=place[1]))
            continue
        age = (today() - date).days
        if age > most:
            problems.append(run.problem(
                "E", "GEN-11", label, "model_facts_date",
                f"{date.isoformat()} is {age} days old on a paid pack; model facts older than {number_words(most)} days "
                "cannot price a paid pack",
                "Fix: refresh the model facts (stage.py refresh-models --propose; the user approves any price change; "
                "then --apply) and compile again before spending.", file_name=place[0], line_number=place[1]))
    return problems


def banned_words(run):
    """The words banned from prompts: words.json's groups, and each word swap's source except one whose own target
    holds it ("flask" becomes "small steel vacuum flask")."""
    groups = (run.words.get("banned_prompt_words") or {}).get("groups") or {}
    words = []
    for group in groups.values():
        words.extend(group)
    words += swap_sources_banned(prompt_swaps(run))
    return sorted(set(words), key=lambda word: (-len(word), word))


def prompt_swaps(run):
    """The prompt word swaps (words.json's and the project's own), as the compiler makes them."""
    return project_prompt_swaps(run.words, run.project_record)


def lint_gen_12(run, clips, facts=None, forced=False):
    words = banned_words(run)
    problems = []
    for clip in clips:
        prompt = prompt_without_speeches(run, clip)
        found = [word for word in words if re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", prompt, re.IGNORECASE)]
        if found:
            problems.append(clip_problem(
                run, "E", "GEN-12", clip, "prompt",
                f"holds {', '.join(repr(word) for word in found)}, banned from prompts",
                "Fix: describe the visible quality instead, and use the project's word swaps (torch becomes "
                "flashlight); compile again."))
    return problems


def lint_gen_13(run, clips, facts=None, forced=False):
    most = int(number_of(constant(run.constants, "on_screen_speakers_per_clip_max", 1), 1))
    breakdown = breakdown_of(run)
    problems = []
    for clip in clips:
        listed = clip.data.get("on_screen_speakers")
        if isinstance(listed, list):
            speakers = sorted({str(speaker) for speaker in listed})
        else:
            items = dict(heard(clip))
            speakers = set()
            for identifier in clip_speeches(run, clip):
                item = items.get(identifier)
                if item is not None and normalise_word(item.get("speaker") or "") == "on_screen":
                    speaker = (breakdown.speech(identifier) or {}).get("speaker")
                    if speaker:
                        speakers.add(element_of(speaker))
            speakers = sorted(speakers)
        if len(speakers) > most:
            problems.append(clip_problem(
                run, "W", "GEN-13", clip, "hear",
                f"has {len(speakers)} speakers talking on screen ({', '.join(speakers)}); one clip holds {most}",
                "Fix: keep one speaker's mouth on screen per clip (the listener's clip is silent), split at a planned "
                "cut, or plan lip sync as a finishing job."))
    return problems


def lint_gen_14(run, packs, clips, forced=False):
    project = run.project_record
    if project is None or normalise_word(project.get("rights") or "") != "study_only":
        return []
    use = normalise_word(project.get("intended_use") or "")
    if use in PUBLIC_USES:
        return [report(
            run, "E", "GEN-14", project, "intended_use",
            f"{use} releases the film, but the rights are study_only",
            "Fix: keep the intended use personal, or settle the rights (permission, or the user's own story) through "
            "a choice before any pack is made for release.", place_of(run, project, "intended_use"))]
    problems = []
    for pack in packs:
        if normalise_word(pack.get("release") or "") == "public":
            scene_identifier = pack_scene(pack, clips)
            if scene_identifier and not run.in_scope(scene_identifier):
                continue
            problems.append(report(
                run, "E", "GEN-14", project, "rights",
                f"study_only forbids the public release pack {pack.get('_file') or scene_identifier}",
                "Fix: compile the pack for private study only, or settle the rights through a choice first.",
                place_of(run, project, "rights")))
    return problems


def reason_texts(run, clip):
    """[(what, text)]: the reasons that must never travel into a prompt (8.1 rule 2)."""
    texts = []
    shot = clip.shot
    if shot is not None:
        for name in ("purpose", "why", "move_reason", "pov_break"):
            if not is_empty(shot.get(name)):
                texts.append((f"the shot's {name}", shot.get(name)))
        for written in shot.get_all("departure"):
            kept = split_item(written).get("meaning_kept")
            if not is_empty(kept):
                texts.append(("the meaning a departure keeps", kept))
        for written in shot.get_all("thing"):
            motif = run.record(element_of(split_item(written).first or ""))
            if motif is not None and motif.type_name == "MOTIF" and not is_empty(motif.get("meaning")):
                texts.append((f"{motif.identifier}'s meaning", motif.get("meaning")))
    return texts


def visible_texts(clip):
    """The shot's visible words (does, shows, end, task-like fields), which a prompt may legitimately hold."""
    shot = clip.shot
    if shot is None:
        return ""
    parts = []
    for written in shot.get_all("subject"):
        item = split_item(written)
        parts += [item.get("does") or "", item.get("must_not") or ""]
    for written in shot.get_all("moment"):
        parts.append(split_item(written).get("shows") or "")
    parts += [shot.get("end") or "", shot.get("physics_note") or "", shot.get("gen_note") or ""]
    return normalised(" ".join(parts))


def lint_gen_15(run, clips, facts=None, forced=False):
    problems = []
    mood_phrases = [normalised(phrase) for phrase in
                    ((run.words or {}).get("mood_only_phrases") or {}).get("phrases") or [] if phrase]
    for clip in clips:
        prompt = normalised(clip.prompt)
        visible = visible_texts(clip)
        found = None
        for what, text in reason_texts(run, clip):
            # a quotation of the script inside a reason is the story's own words (a spoken line the prompt sends,
            # text the shot shows), never the reason travelling into the prompt
            for piece in clauses(QUOTED_WORDS.sub(" ; ", text or ""), REASON_CLAUSE_WORDS_MIN):
                if piece in prompt and piece not in visible:
                    found = (what, piece)
                    break
            if found:
                break
        if found is None:
            identifier = STAGE_IDENTIFIER.search(clip.prompt)
            if identifier:
                found = ("a record ID from the reasons", identifier.group(0))
        if found is None:
            # 8.1 rule 2: mood words never travel either (words.json's mood-only phrases, REASON-04's list)
            for phrase in mood_phrases:
                if re.search(r"(?<![a-z])" + re.escape(phrase) + r"(?![a-z])", prompt) and phrase not in visible:
                    found = ("a mood phrase", phrase)
                    break
        if found:
            shown = found[1] if len(found[1]) <= 60 else found[1][:57] + "..."
            problems.append(clip_problem(
                run, "E", "GEN-15", clip, "prompt",
                f"carries {found[0]} into the prompt ('{shown}')",
                "Fix: prompts carry only what is seen and heard; keep why, because, purpose, motif meanings and mood "
                "words in the records (take a mood word out of the record the prompt pastes), and compile again."))
    return problems


def lint_gen_17(run, clips, facts=None, forced=False):
    most = int(number_of(constant(run.constants, "named_sounds_per_prompt_max", 3), 3))
    breakdown = breakdown_of(run)
    problems = []
    for clip in clips:
        prompt = normalised(clip.prompt)
        items = dict(heard(clip))
        for identifier in clip_speeches(run, clip):
            item = items.get(identifier)
            path = normalise_word((item.get("path") if item is not None else None)
                                  or (breakdown.speech(identifier) or {}).get("path") or "direct")
            words = RELAYED_PATHS.get(path)
            if words and not any(re.search(r"\b" + re.escape(word), prompt) for word in words):
                problems.append(clip_problem(
                    run, "W", "GEN-17", clip, "hear",
                    f"{identifier} comes through a {path.replace('_', ' ')}, but the prompt never names that path",
                    "Fix: name the path in the same sentence as the line ('through a small intercom speaker, slightly "
                    "thin'), from the voice's path sound."))
                break
        sounds = clip.data.get("sounds")
        if isinstance(sounds, list) and len(sounds) > most:
            problems.append(clip_problem(
                run, "W", "GEN-17", clip, "effect",
                f"names {len(sounds)} sounds ({', '.join(str(sound) for sound in sounds)}); models drop sounds beyond "
                f"{most}",
                f"Fix: keep the {most} sounds the beat needs and add the rest in the sound edit."))
    return problems


def lint_packs(run, packs, forced=False):
    """Lint packs held in memory (stage.py compile): every GEN check that reads compiled clips, as one list of
    problem lines. forced (compile --force-model) makes GEN-02 and GEN-10 notes."""
    clips = clips_of(run, packs)
    facts = model_facts(run)
    problems = []
    for function in (lint_gen_03, lint_gen_04, lint_gen_05, lint_gen_06, lint_gen_07, lint_gen_12, lint_gen_13,
                     lint_gen_15, lint_gen_17):
        problems += function(run, clips, facts, forced)
    if facts is not None:
        for function in (lint_gen_01, lint_gen_02, lint_gen_08, lint_gen_09):
            problems += function(run, clips, facts, forced)
        problems += lint_gen_10_records(run, facts, forced)
    problems += lint_gen_10_packs(run, clips, forced)
    problems += lint_gen_11(run, packs, clips, facts, forced)
    problems += lint_gen_14(run, packs, clips, forced)
    return problems


# ---------------------------------------------------------------- registering the GEN checks

def packs_check(check_id, function, needs_facts):
    def run_check(run):
        clips = compiled_clips(run, check_id)
        if not clips:
            return []
        facts = model_facts(run)
        if needs_facts and facts is None:
            run.skip(check_id, NO_FACTS)
            return []
        return function(run, clips, facts)
    run_check.__name__ = f"check_{check_id.lower().replace('-', '_')}"
    run_check.__doc__ = function.__doc__
    return run_check


GEN_ON_PACKS = [
    ("GEN-01", lint_gen_01, True, "Prompt over the model's limit (C3 L01)",
     "has a prompt longer than its video model accepts"),
    ("GEN-02", lint_gen_02, True, "Clip length or resolution not allowed by the model (L02)",
     "asks its video model for a clip length or picture size it does not make"),
    ("GEN-03", lint_gen_03, False, "Speech over the clip rule (L08, K08)",
     "puts more speech in a clip than the clip can hold"),
    ("GEN-04", lint_gen_04, False, "Fixed description, state line or look block differs from its record (L16, L17)",
     "has a prompt whose description of a person or of the place's light is not the saved wording"),
    ("GEN-05", lint_gen_05, False, "Start picture attached and appearance re-described (L18)",
     "describes people or the set again although a start picture already shows them"),
    ("GEN-06", lint_gen_06, False, "Readable or backwards text asked of the model (L21)",
     "asks the video model to draw readable words, which are added afterwards instead"),
    ("GEN-07", lint_gen_07, False, "Negation of a visible thing outside the documented 'No ...' lines (L14)",
     "tells the video model what not to show, which often makes it show it"),
    ("GEN-08", lint_gen_08, True, "Dialogue or audio sent to a silent model (L28)",
     "sends speech or sound to a video model that makes no sound"),
    ("GEN-09", lint_gen_09, True, "Speaker format wrong for the model (L09)",
     "writes a spoken line in a form its video model does not follow"),
    ("GEN-12", lint_gen_12, False, "'torch' or another banned word in a prompt",
     "uses a word that video models misread or that adds nothing to the picture"),
    ("GEN-13", lint_gen_13, False, "Two on-screen speakers in one clip",
     "has two people talking on screen in one clip"),
    ("GEN-15", lint_gen_15, False, "Reasons (why, because, purpose, motif meaning) in prompt text",
     "puts the reasons for a shot into its prompt, where only what is seen and heard belongs"),
]
GEN_LEVELS = {"GEN-13": "W"}

for _check_id, _function, _needs_facts, _title, _plain in GEN_ON_PACKS:
    register_check(_check_id, level=GEN_LEVELS.get(_check_id, "E"), build=1, title=_title, plain=_plain)(
        packs_check(_check_id, _function, _needs_facts))


@register_check("GEN-10", level="E", build=1,
                title="A held take (a turn shot, a shot in a oner scene, or held: yes) split into chained clips",
                plain="splits a shot whose meaning depends on not cutting, or is too long for any video model to "
                      "make in one piece")
def check_gen_10(run):
    """From the records (with the model facts): a held take whose screen time plus handles no model allows, which
    would have to be split. From the compiled packs: a held take compiled as more than one clip."""
    problems = []
    facts = model_facts(run)
    if facts is None:
        run.skip("GEN-10", NO_FACTS)
    else:
        problems += lint_gen_10_records(run, facts)
    problems += lint_gen_10_packs(run, clips_of(run, read_packs(run)))
    return problems


@register_check("GEN-11", level="E", build=1,
                title="Model facts older than 30 days on a paid pack",
                plain="prices a paid pack from model facts older than the tools allow")
def check_gen_11(run):
    """A pack marked paid whose model facts date (the pack's own, else the adapters' checked_on) is older than
    model_facts_max_age_days, or has no date at all."""
    packs = read_packs(run)
    if not packs:
        run.skip("GEN-11", NO_PACKS)
        return []
    return lint_gen_11(run, packs, compiled_clips(run, "GEN-11"), model_facts(run))


@register_check("GEN-14", level="E", build=1,
                title="A public-release pack while rights are study_only",
                plain="makes material for release while the story's rights allow study only")
def check_gen_14(run):
    """PROJECT rights study_only with an intended use that releases the film (festival, online or commercial), or a
    compiled pack marked for public release."""
    packs = read_packs(run)
    return lint_gen_14(run, packs, clips_of(run, packs))


@register_check("GEN-16", level="W", build=2,
                title="A take over $2 with no cheaper test first (L30)",
                plain="spends on a dear take before trying a cheap test")
def check_gen_16(run):
    """TAKE records: a take costing more than cheap_test_above_usd_per_take with no earlier take of the same clip at
    or below it."""
    most = number_of(constant(run.constants, "cheap_test_above_usd_per_take", 2), 2)
    by_clip = {}
    for take in run.records("TAKE"):
        clip = (take.get("clip") or "").strip()
        if clip:
            by_clip.setdefault(clip, []).append(take)
    problems = []
    for clip, takes in by_clip.items():
        takes.sort(key=lambda take: take.identifier or "")
        cheap_seen = False
        for take in takes:
            cost = number_of(take.get("cost_usd"))
            if cost is None:
                continue
            if cost <= most:
                cheap_seen = True
            elif not cheap_seen and run.in_scope(clip):
                problems.append(report(
                    run, "W", "GEN-16", take, "cost_usd",
                    f"{number_words(cost)} dollars is spent on {clip} with no cheaper test take first (above "
                    f"{number_words(most)} dollars a take needs one)",
                    "Fix: make a draft take on the cheapest tier first, and spend on the dear route only once the "
                    "draft shows the prompt works.", place_of(run, take, "cost_usd")))
    return problems


@register_check("GEN-17", level="W", build=2,
                title="Relayed voice without its path; more than 3 named sounds (L11, L13)",
                plain="plays a voice heard through a radio, phone or glass without saying so, or names more sounds "
                      "than a video model keeps")
def check_gen_17(run):
    """Compiled clips: a speech whose path relays it (earpiece, radio, intercom, phone, speaker, recording, helmet,
    glass) with no word for that path in the prompt; more named sounds than named_sounds_per_prompt_max."""
    clips = compiled_clips(run, "GEN-17")
    return lint_gen_17(run, clips) if clips else []
