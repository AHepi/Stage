"""The tests of the "is it right" code review: one group per fix the review made in the checker, the derived fields,
the film pass and the generation layer (blueprint 5.6, 7.2, 8 and 9).

What it proves:
- a grey preview job code made at step 8 (PREVIS with status planned) does not switch add-on B on, and FORM-05 asks
  it only for what code writes; FORM-05 never asks the AI for PREVIS approved (code or the user writes it), so build
  can now write the stubs the checker accepts (derive_fields.checker_accepts_previs_stubs);
- on the plate route (8.5, route c) the start picture is two prompts, never one: the plate (the place and its
  mirrored people and things, described before the flip, with no one who is added later) and the edit that adds the
  people shown normally in the finished picture's sides; no research code or route instruction is inside a prompt;
- a mirrored person on the plate route is never turned in the video prompt, which is animated from the finished
  start picture (their travel keeps its side);
- reference pictures are attached flipped left to right where 8.5 says: on the flip routes (a, b) for every element
  shown normally, on the direct route (e) for every mirrored element, never on the plate route; a place's reference
  is compared with the orientation its set plan is stored in;
- FILM-02 lets a rhyme declare that its payoff reverses the plant's frame side on purpose (side: reversed, The
  Catch's scene 29 rings, B3 §8.2): silent when the payoff is on the other side, a warning when it is not;
- GEN-15 catches a mood phrase (words.json's mood-only phrases) and a departure's meaning_kept in a prompt, as 8.1
  rule 2 says reasons and mood words never travel;
- WORDS-01 does not report "hurt" or "tense" next to a body part ("his hurt arm"), which describe the body;
- TIME-01 skips a shot whose lines (or its beats' lines) are quotes not found in the story given, instead of
  passing it on a floor that leaves out the pause owed;
- refresh-models reads its age limit from rules/constants.json by name;
- a spoken line is taken out of a moment's words as whole words ("No" never cuts "Nothing" apart);
- the health check names the add-on records (pictures, grey previews, takes, voice takes, finishing jobs, music, the
  visual plan) in plain words, never by their codes;
- flip: never turns the plate route into direct too, so a sided insert (Saye's ring) is never flipped (K07);
- where a picture shows an element pre-reversed (a mirrored element made as it appears, or a normal one made before
  the clip's flip), its pasted words have left and right turned (B1 method 1) and GEN-04 accepts exactly that
  change; the reference sheets say frame-left and never "no people" (5.7, K18);
- a title card or caption reads normally in every era (D12 rule 17), so its reading time is never doubled;
- the inputs the crash search found stopping a tool (malformed shot and setup IDs) now run through the checks,
  build, compile and the plans.

Usage: python tests/review_is_it_right_acceptance.py
The scene 10 excerpt (tests/fixtures/The Catch - lines 397-489.txt) gives the story; without it the groups that need
it say "skipped: story not present". Standard library only.
"""

import re
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parent.parent
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
TOOLS = SKILL / "tools"
sys.path.insert(0, str(TOOLS))

from stage_tools import check_records  # noqa: E402
from stage_tools import compile_prompts as compiler_module  # noqa: E402
from stage_tools import checks_plan_generation_film as generation  # noqa: E402
from stage_tools.checks_form import FormContext, check_form_05  # noqa: E402
from stage_tools.derive_fields import Breakdown, MirrorRoute, checker_accepts_previs_stubs, load_video_models  # noqa: E402
from stage_tools.record_format import load_skill_data, parse_text  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
EXCERPT = REPOSITORY / "tests" / "fixtures" / "The Catch - lines 397-489.txt"
GOLD_SCENE = SKILL / "examples" / "01 The Catch - scene 10.md"
GOLD_CONTEXT = SKILL / "examples" / "02 The Catch - scene 10 - context.md"
SCENE_FILE = "11 Scenes/Scene 10 - Saye's kitchen.md"
CONTEXT_FILE = "05 Story plan and the other whole-film files.md"

RESULTS = []


def report(passed, group, detail=""):
    RESULTS.append(bool(passed))
    print(f"{'PASS' if passed else 'FAIL'}  {group}" + (f": {detail}" if detail else ""), flush=True)


def group(title):
    def decorator(function):
        def run(*arguments):
            try:
                detail = function(*arguments)
            except AssertionError as error:
                report(False, title, str(error) or "assertion failed")
                return
            except Exception as error:  # a crash is a failure of the group, with its message
                report(False, title, f"{type(error).__name__}: {error}")
                return
            if isinstance(detail, str) and detail.startswith("skipped:"):
                print(f"INFO  {title}: {detail}", flush=True)
                return
            report(True, title, detail or "")
        return run
    return decorator


def gold_texts():
    return {SCENE_FILE: GOLD_SCENE.read_text(encoding="utf-8"), CONTEXT_FILE: GOLD_CONTEXT.read_text(encoding="utf-8")}


def record_files(texts):
    return [parse_text(text, name, SCHEMA) for name, text in texts.items()]


def breakdown_of(texts, with_story=True):
    breakdown = Breakdown(record_files(texts), SCHEMA, WORDS, CONSTANTS)
    if with_story and EXCERPT.is_file():
        breakdown.attach_story_file(EXCERPT)
    breakdown.models = load_video_models()
    return breakdown


def replace_in_record(text, heading_start, old, new):
    """Replace one line inside the record whose heading starts with heading_start."""
    start = text.index(heading_start)
    end = text.find("\n### ", start + 1)
    end = len(text) if end < 0 else end
    block = text[start:end]
    assert old in block, f"{old!r} is not in {heading_start}"
    return text[:start] + block.replace(old, new, 1) + text[end:]


def add_record(text, record_text):
    """A record added before the END line of a record file (the END count is not checked here)."""
    position = text.rfind("\nEND OF FILE")
    position = len(text) if position < 0 else position
    return text[:position] + "\n\n" + record_text.strip() + "\n" + text[position:]


def compile_scene(breakdown):
    compiler = compiler_module.Compiler(breakdown, compiler_module.Adapters(), WORDS, {})
    scene = compiler.compile_scene("SC10")
    return compiler, scene


# ---------------------------------------------------------------- FORM-05 and the grey preview stubs

@group("FORM-05: a grey preview stub does not switch add-on B on; approved is never asked of the AI")
def previs_stubs():
    assert checker_accepts_previs_stubs(SCHEMA, WORDS), "FORM-05 still asks a planned stub for add-on B's fields"
    stub = ("### PREVIS PV-SC10-MASTER-V01 The master of the fall\n- for: SC10-MASTER\n- level: 3\n- status: planned\n"
            "- locked: no\n")
    files = record_files({"19 Grey previews/Grey preview jobs.md": "# Grey previews\n\n" + stub})
    context = FormContext.for_records(SCHEMA, WORDS, files, step=None)
    assert "B" not in (context.modules or set()), f"a planned stub switched add-ons on: {context.modules}"
    lines = [str(line) for line in check_form_05(files, context) if "PV-SC10-MASTER-V01" in str(line)]
    assert not lines, lines
    job = ("### PREVIS PV-SC10-SH080-V01 The reflection two-shot\n- for: SC10-SH080\n- level: 2\n- status: draft\n"
           "- locked: no\n")
    files = record_files({"19 Grey previews/Grey preview jobs.md": "# Grey previews\n\n" + job})
    context = FormContext.for_records(SCHEMA, WORDS, files, step=None)
    assert "B" in (context.modules or set()), "a real grey preview job no longer switches add-on B on"
    lines = [str(line) for line in check_form_05(files, context)]
    assert any(" standin_level " in line for line in lines), f"add-on B's own fields are no longer asked: {lines}"
    assert not any(" approved " in line for line in lines), f"FORM-05 asks the AI for approved: {lines}"
    return f"a planned stub is silent and leaves add-on B off; a draft job is asked {len(lines)} add-on fields, never approved"


# ---------------------------------------------------------------- the plate route (8.5, route c)

@group("plate route: the start picture is a plate prompt and a separate edit prompt, each in its own sides")
def plate_route_pictures():
    if not EXCERPT.is_file():
        return "skipped: story not present"
    breakdown = breakdown_of(gold_texts())
    compiler, scene = compile_scene(breakdown)
    jobs = {job["for"] + ":" + job["use"]: job for job in compiler_module.pictures_to_make(compiler, scene)
            if job.get("for")}
    job = jobs["SC10-SH080:start"]
    assert job.get("plate") and job.get("edit_prompt"), job
    plate, edit = job["prompt"], job["edit_prompt"]
    for prompt in (plate, edit):
        assert not re.search(r"\(\d\.\d|\bC2 R5\b|\bplate route\b|\bflip that picture\b", prompt), prompt
    # the plate is the place with Saye (mirrored), before the flip: she is described at the other third, facing the
    # other way; nobody who is added later is in it
    assert "Dr Saye is on the left third of the frame, facing right" in plate, plate
    for name in ("Iona", "Jude", "Eli"):
        assert not re.search(rf"\b{name}\b", plate), f"{name} is in the plate: {plate}"
    assert "the man off screen" not in edit, edit
    # the edit adds the others in the finished picture's sides, and never mirrors them
    assert edit.startswith("Add Iona, Jude and Eli to the attached picture."), edit[:80]
    assert "Iona is on the left third of the frame, facing right" in edit, edit
    assert "in Eli's hands" in edit, "a thing an added person holds is not added with them"
    assert "Do not mirror them. Keep the background exactly as given." in edit
    page = compiler_module.pictures_page(compiler, scene, list(jobs.values()))
    assert "Flip it left to right, then add the others" in page, page[:400]
    return "shot 080: Saye turned in the plate, Iona, Jude and Eli added in the finished sides; no codes in the prompts"


@group("plate route: a mirrored person's travel is not turned in the video prompt (the clip starts from the finished picture)")
def plate_route_travel():
    texts = gold_texts()
    texts[SCENE_FILE] = replace_in_record(texts[SCENE_FILE], "### SHOT SC10-SH080 ",
                                          "still: head, torso | travel: none\n- subject: CH-JUDE",
                                          "still: head, torso | travel: frame_left\n- subject: CH-JUDE")
    breakdown = breakdown_of(texts, with_story=EXCERPT.is_file())
    compiler, scene = compile_scene(breakdown)
    clip = next(clip for clip in scene.clips if clip.plan.identifier == "SC10-SH080")
    assert clip.plan.mirror.route == "plate", clip.plan.mirror.route
    saye = next(person for person in clip.plan.people if person.element == "CH-SAYE")
    assert saye.flipped, "Saye is not a mirrored person on the plate route"
    template = compiler_module.Adapters().phrase("travel", "frame_left", default="")
    assert template, "the phrasebook has no travel words for frame_left"
    wanted = template.replace("{who}", "").strip()
    assert wanted in clip.prompt, f"{wanted!r} is not in: {clip.prompt}"
    other = compiler_module.Adapters().phrase("travel", "frame_right", default="").replace("{who}", "").strip()
    assert other not in clip.prompt, f"the travel was turned: {clip.prompt}"
    return f"shot 080 with Saye travelling frame_left keeps '{wanted}'"


# ---------------------------------------------------------------- flipped reference pictures (8.5)

@group("reference pictures: flipped for elements shown normally on routes a and b, for mirrored ones on route e, never on the plate route")
def reference_pictures_turned():
    breakdown = breakdown_of(gold_texts(), with_story=EXCERPT.is_file())
    compiler = compiler_module.Compiler(breakdown, compiler_module.Adapters(), WORDS, {})
    shot = breakdown.record("SC10-SH050", "SHOT")
    plan = compiler_module.analyse_shot(breakdown, compiler.adapters, shot, {})
    if not EXCERPT.is_file():
        return "skipped: story not present"

    def turned(route, reference):
        changed = compiler_module.dataclass_replace(plan, mirror=MirrorRoute(route, route, False, []))
        return compiler_module.reference_turned(compiler, changed, reference)

    # scene 10, era b: Saye and the kitchen are mirrored, Iona is shown normally; the kitchen's set plan is stored as
    # the audience sees it there (reversed)
    assert turned("direct", "CH-SAYE.S01") and not turned("direct", "CH-IONA.S02")
    assert turned("flip_with_mirrored_references", "CH-IONA.S02") and not turned("flip_with_mirrored_references", "CH-SAYE.S01")
    assert turned("flip_with_mirrored_references", "LOC-SAYE-KITCHEN"), "the kitchen must be made unmirrored before the flip"
    assert not turned("direct", "LOC-SAYE-KITCHEN"), "the kitchen's stored plan already shows it as it appears"
    assert not any(turned("plate", reference) for reference in ("CH-SAYE.S01", "CH-IONA.S02", "LOC-SAYE-KITCHEN"))
    # an attached reference carries the flipped file name and its job says so
    compiler_obj, scene = compile_scene(breakdown)
    entries = [entry for clip in scene.clips for entry in clip.inputs.get("references") or []]
    for entry in entries:
        if entry.get("flipped"):
            assert entry["file"].endswith(" - flipped.png") and "flipped left to right" in entry["job"], entry
    job = {"picture": "PIC-CH-SAYE.S01-REFERENCE-01", "use": "reference", "file": "Reference pictures/Dr Saye.png",
           "model": "nano-banana-pro", "size": "size 2K", "prompt": "a reference sheet", "why": "reference pictures",
           "for": "CH-SAYE.S01", "flipped_file": compiler_module.turned_file("Reference pictures/Dr Saye.png"),
           "flipped_for": ["SC10-SH020", "SC10-SH040"]}
    page = compiler_module.pictures_page(compiler_obj, scene, [job])
    wanted = ("Then save a copy flipped left to right as: Reference pictures/Dr Saye - flipped.png. In the mirror world "
              "these shots attach the flipped copy: scene 10, shot 020; scene 10, shot 040.")
    assert wanted in page, page
    return "Saye flipped on the direct route, Iona and the kitchen on the flip route, nothing on the plate route"


# ---------------------------------------------------------------- FILM-02 and a side reversed on purpose

RHYME_RECORDS = """
### PLANT PL-90 The rings rhyme
- what: the two ringed hands
- rhyme: yes | framing: the reflection two-shot{side}

### SHOT SC10-SH910 Plant
- beats: SC10-B01
- size: medium
- angle: eye_level
- lens_mm: 85
- thing: MO-RINGS | emphasis: 1 | at: left_third | plant: PL-90

### SHOT SC10-SH920 Payoff
- beats: SC10-B01
- size: medium
- angle: eye_level
- lens_mm: 85
- thing: MO-RINGS | emphasis: 2 | at: {payoff_side} | payoff: PL-90
"""


def film_02_lines(side, payoff_side):
    text = "# Rhyme test\n" + RHYME_RECORDS.replace("{side}", side).replace("{payoff_side}", payoff_side)
    result = check_records.run_checks(record_files({"11 Scenes/Scene 10 - test.md": text}), SCHEMA, WORDS, CONSTANTS,
                                      check_ids=["FILM-02"])
    assert not result.crashed, result.crashed
    return [str(line) for line in result.problems if "FILM-02" in str(line)]


@group("FILM-02: a rhyme may declare its payoff's frame side reversed on purpose (side: reversed)")
def film_02_side_reversed():
    assert film_02_lines("", "right_third"), "a payoff on the other side with no declaration is silent"
    assert not film_02_lines(" | side: reversed", "right_third"), "a declared reversal still warns"
    lines = film_02_lines(" | side: reversed", "left_third")
    assert lines and "not the other side" in lines[0], lines
    assert not film_02_lines("", "left_third"), "a payoff on the same side warns"
    return "undeclared reversal warns; declared reversal is silent; declared but kept side warns"


# ---------------------------------------------------------------- GEN-15: reasons and mood words never travel

@group("GEN-15: a mood phrase or a departure's meaning_kept in a prompt is an error")
def gen_15_mood_and_meaning():
    texts = gold_texts()
    texts[SCENE_FILE] = replace_in_record(texts[SCENE_FILE], "### SHOT SC10-SH050 ", "- held: no\n",
                                          "- held: no\n- departure: move | from: push_in | to: static | because: "
                                          "feasibility | meaning_kept: the closest frame stays on the turn\n")
    files = record_files(texts)
    run = check_records.CheckRun(files, SCHEMA, WORDS, CONSTANTS)

    def lint(prompt):
        pack = {"scene": "SC10", "clips": [{"clip": "SC10-SH050.1", "shot": "SC10-SH050", "model": "kling-3.0-omni",
                                            "prompt": prompt, "length_s": 10}]}
        return [str(line) for line in generation.lint_gen_15(run, generation.clips_of(run, [pack]))]

    assert not lint("Medium close-up, at eye level. The woman looks down."), "a plain prompt is flagged"
    moody = lint("Medium close-up, a cinematic frame, at eye level. The woman looks down.")
    assert moody and "mood phrase" in moody[0], moody
    kept = lint("Medium close-up. The closest frame stays on the turn. The woman looks down.")
    assert kept and "meaning a departure keeps" in kept[0], kept
    return "'cinematic' and a meaning_kept sentence are caught; a plain prompt is silent"


# ---------------------------------------------------------------- WORDS-01: a body described is not a feeling

@group("WORDS-01: 'hurt' and 'tense' next to a body part describe the body and are not reported")
def words_01_body_words():
    from stage_tools.checks_craft_reasons_words import emotion_words_in
    for text in ("cradles his hurt arm", "her jaw tense, eyes down", "her shoulders go tense", "holds her hurt left hand"):
        assert not emotion_words_in(WORDS, text), f"{text!r} is reported as a feeling"
    for text, word in (("looks hurt", "hurt"), ("she is tense and angry", "tense"), ("sad and tired", "sad")):
        assert word in emotion_words_in(WORDS, text), f"{text!r} is no longer reported"
    return "body descriptions pass; feelings are still reported"


# ---------------------------------------------------------------- TIME-01: a floor whose pause is unknown

@group("TIME-01: a shot whose lines are quotes not found in the story given is skipped, never passed on a low floor")
def time_01_unresolved_lines():
    texts = gold_texts()
    texts[SCENE_FILE] = re.sub(r"(### SHOT SC10-SH150 [^\n]*\n(?:- [^\n]*\n)*?)- lines: [^\n]*\n",
                               lambda match: match.group(1) + '- lines: "words that are in no story here"\n',
                               texts[SCENE_FILE], count=1)
    breakdown = breakdown_of(texts, with_story=EXCERPT.is_file())
    from stage_tools.derive_fields import time_floor
    floor = time_floor(breakdown, breakdown.record("SC10-SH150", "SHOT"))
    assert not floor.complete and floor.unresolved_lines == ["SC10-SH150"], (floor.complete, floor.unresolved_lines)
    assert "lines not found for SC10-SH150" in floor.reasons(), floor.reasons()
    if not EXCERPT.is_file():
        return "skipped: story not present"
    story = check_records.StorySource.from_file(EXCERPT, CONSTANTS)
    result = check_records.run_checks(record_files(texts), SCHEMA, WORDS, CONSTANTS, story=story, check_ids=["TIME-01"])
    assert not result.crashed, result.crashed
    assert not [line for line in result.problems if "SC10-SH150" in str(line)], result.problems
    skipped = " ".join(why for check_id, why in result.skipped if check_id == "TIME-01")
    assert "SC10-SH150" in skipped and "pause they owe is not known" in skipped, skipped
    gold = time_floor(breakdown_of(gold_texts(), with_story=EXCERPT.is_file()),
                      breakdown_of(gold_texts(), with_story=EXCERPT.is_file()).record("SC10-SH150", "SHOT"))
    if EXCERPT.is_file():
        assert gold.complete and gold.floor == 13.8, (gold.complete, gold.floor)
    return "an unfound anchor makes the floor incomplete and TIME-01 says why; the gold's shot 150 is still 13.8 s"


# ---------------------------------------------------------------- refresh-models reads its age limit by name

@group("refresh-models: the age limit is read from rules/constants.json by name (model_facts_max_age_days)")
def refresh_age_limit():
    import copy
    import types
    from stage_tools import refresh_models
    constants = copy.deepcopy(CONSTANTS)
    constants["constants"]["model_facts_max_age_days"]["value"] = -1
    said = []
    context = types.SimpleNamespace(arguments=types.SimpleNamespace(propose=None, apply=False, check=True, adapters=None),
                                    constants=constants, say=said.append, summary="")
    refresh_models.run_refresh(context)
    dated = [line for line in said if "checked on" in line]
    assert dated and all("too old to spend money on" in line for line in dated), said[:3]
    context.constants, said[:] = CONSTANTS, []
    refresh_models.run_refresh(context)
    return f"a limit of -1 days marks all {len(dated)} dated files too old; the real limit is {CONSTANTS['constants']['model_facts_max_age_days']['value']} days"


# ---------------------------------------------------------------- a spoken line is taken out of a moment whole

@group("compile: a spoken line is taken out of a moment's words as whole words, never out of the middle of a word")
def spoken_line_whole_words():
    breakdown = breakdown_of(gold_texts(), with_story=EXCERPT.is_file())
    compiler, scene = compile_scene(breakdown)
    clip = next((clip for clip in scene.clips if clip.plan.on_screen), None)
    assert clip is not None, "no clip with a line spoken on screen"
    identifier, item, entry = clip.plan.on_screen[0]
    entry = dict(entry, text="No")
    clip.plan.on_screen = [(identifier, item, entry)] + list(clip.plan.on_screen[1:])
    shot = clip.plan.shot
    lines = shot.field_lines("moment")
    old = lines[0].value
    span = old.split("|", 1)[0].strip()
    lines[0].value = f"{span} | shows: Nothing moves; she says No and waits"
    try:
        cast = compiler_module.Cast(breakdown, compiler.adapters, clip.plan, clip.plan.start_picture)
        words = " ".join(entry_words for _, _, entry_words in compiler.writer.moments(clip, cast))
    finally:
        lines[0].value = old
    assert "Nothing moves" in words and " No " not in f" {words} ", words
    return f"'{words}'"


# ---------------------------------------------------------------- plain names in the health check

@group("health check: the add-on records are named in plain words, never by their codes (WORDS-04)")
def plain_names_of_add_on_records():
    expected = {"VS-SQ03": "the visual plan of group of scenes 3",
                "PIC-SC10-SH150-START-01": "the start picture of scene 10, shot 150",
                "PV-SC10-SH080-V01": "the grey preview of scene 10, shot 080, try 1",
                "PV-SC06-MASTER-V02": "the grey preview of scene 6, the master shot, try 2",
                "TK-SC10-SH150.1-T03": "take 3 of scene 10, shot 150, clip 1",
                "VT-SC10-D11-T01": "voice take 1 of scene 10, speech 11",
                "FX-SC10-SH080-01": "finishing job 1 of scene 10, shot 080",
                "MU-01": "music cue 1"}
    for label, words in expected.items():
        found = check_records.plain_name_of(label)
        assert found == words, f"{label}: {found!r}, wanted {words!r}"
        assert not re.search(r"\b(?:SC|SH|PV|PIC|TK|VT|FX|MU|VS|SQ)\d*\b", found, re.IGNORECASE), found
    return f"{len(expected)} add-on IDs read as plain words"


# ---------------------------------------------------------------- flip: never also stops the plate's flip

@group("mirror route: flip: never turns the plate route into direct, so a sided insert is never flipped (8.5, K07)")
def flip_never_on_the_plate_route():
    if not EXCERPT.is_file():
        return "skipped: story not present"
    from stage_tools.derive_fields import mirror_route
    breakdown = breakdown_of(gold_texts())
    ring = mirror_route(breakdown, breakdown.record("SC10-SH090", "SHOT"))
    assert ring.route == "direct" and "flip: never" in ring.reasons[-1], (ring.route, ring.reasons)
    texts = gold_texts()
    texts[SCENE_FILE] = re.sub(r"(### SHOT SC10-SH090 [^\n]*\n(?:- [^\n]*\n)*?)- flip: never\n",
                               lambda match: match.group(1) + "- flip: auto\n", texts[SCENE_FILE], count=1)
    auto = mirror_route(breakdown_of(texts), breakdown_of(texts).record("SC10-SH090", "SHOT"))
    assert auto.route == "plate", auto.route
    return "shot 090 (Saye's ring) is direct with flip: never and plate with flip: auto"


# ---------------------------------------------------------------- own sides pre-reversed where the picture is reversed

@group("pre-reversed sides: a mirrored element made as it appears has left and right turned in its pasted words; GEN-04 accepts only that change")
def pre_reversed_sides():
    if not EXCERPT.is_file():
        return "skipped: story not present"
    breakdown = breakdown_of(gold_texts())
    compiler, scene = compile_scene(breakdown)
    jobs = {job["for"] + ":" + job["use"]: job for job in compiler_module.pictures_to_make(compiler, scene)
            if job.get("for")}
    ring = jobs["SC10-SH090:start"]["prompt"]           # direct route: Saye as she appears in the mirror world
    assert "a plain gold ring on her right hand" in ring and "ring on her left hand" not in ring, ring
    plate = jobs["SC10-SH080:start"]["prompt"]          # the plate: Saye as her own world has her, flipped after
    assert "a plain gold ring on her left hand" in plate, plate
    edit = jobs["SC10-SH080:start"]["edit_prompt"]      # Iona is shown normally and made unflipped
    assert "her right palm raw" in edit, edit
    # reference sheets: the one word frame-left (5.7), and no "no people" in a picture prompt (K18)
    for job in jobs.values():
        if job["use"] == "reference":
            assert "image-left" not in job["prompt"] and not re.search(r"\bno (?:people|text|labels)\b",
                                                                      job["prompt"], re.IGNORECASE), job["prompt"]
    state = breakdown.record("CH-SAYE.S01", "STATE").get("state_line")
    files = record_files(gold_texts())
    run = check_records.CheckRun(files, SCHEMA, WORDS, CONSTANTS)

    def gen_04(prompt):
        pack = {"scene": "SC10", "clips": [{"clip": "SC10-SH050.1", "shot": "SC10-SH050", "model": "kling-3.0-omni",
                                            "prompt": prompt, "length_s": 10, "inputs": {},
                                            "subjects": ["CH-SAYE.S01"]}]}
        lines = generation.lint_gen_04(run, generation.clips_of(run, [pack]))
        return [str(line) for line in lines if "state line" in str(line)]

    fixed = breakdown.record("CH-SAYE", "CHARACTER").get("fixed_description")
    assert not gen_04(f"{fixed} {state}"), "the record's own words are refused"
    assert not gen_04(f"{fixed} {compiler_module.swap_own_sides(state)}"), "the pre-reversed words are refused"
    assert gen_04(f"{fixed} {state.replace('gold', 'silver')}"), "a changed state line is accepted"
    return "shot 090 (direct) says 'ring on her right hand'; shot 080's plate keeps 'left hand'; GEN-04 takes both forms, nothing else"


# ---------------------------------------------------------------- a title card never reads mirrored

@group("text orientation: a title card reads normally in a reversed frame even with no titles rule (D12 rule 17)")
def title_card_never_mirrored():
    from stage_tools import derive_fields
    texts = gold_texts()
    texts[CONTEXT_FILE] = texts[CONTEXT_FILE].replace("- governs: TX-TITLE-CATCH", "- governs: none")
    breakdown = breakdown_of(texts, with_story=EXCERPT.is_file())
    shot = breakdown.record("SC10-SH990", "SHOT")
    original = derive_fields.frame_at
    derive_fields.frame_at = lambda breakdown_here, line: "reversed"
    try:
        card = derive_fields.text_orientation(breakdown, "TX-TITLE-CATCH", shot)
        seconds, how = derive_fields.text_reading_seconds(breakdown, breakdown.record("TX-TITLE-CATCH", "TEXT"),
                                                          card == "mirrored")
    finally:
        derive_fields.frame_at = original
    assert card == "normal", card
    assert "mirrored" not in how, how
    return f"the title card reads {card} in a reversed frame; reading time {seconds:g} s ({how})"


# ---------------------------------------------------------------- the crash search

@group("crash search: unusual values in the gold do not stop the checks, compile or the grey preview plans")
def crash_search():
    from stage_tools import make_previs_plans
    from stage_tools.derive_fields import derive_all
    cases = review_crash_cases()
    for label, texts in cases:
        result = check_records.run_checks(record_files(texts), SCHEMA, WORDS, CONSTANTS)
        assert not result.crashed, f"{label}: {result.crashed}"
        breakdown = breakdown_of(texts, with_story=EXCERPT.is_file())
        derive_all(breakdown)
        compiler, scene = compile_scene(breakdown)
        compiler_module.pictures_to_make(compiler, scene)
        for shot in breakdown.shots_of("SC10"):
            make_previs_plans.compile_shot_plan(breakdown, shot.identifier)
    return f"{len(cases)} unusual inputs ran through the checks, build, compile and the plans"


def review_crash_cases():
    """The inputs the review's crash search found stopping a tool (each fixed; see the build log)."""
    cases = []
    base = gold_texts()
    for label, old, new in CRASH_EDITS:
        texts = dict(base)
        name = SCENE_FILE if old in texts[SCENE_FILE] else CONTEXT_FILE
        assert old in texts[name], f"{label}: the gold no longer holds {old!r}"
        texts[name] = texts[name].replace(old, new)
        cases.append((label, texts))
    return cases


# (label, text in the gold, replacement): the inputs the crash search found stopping a tool
CRASH_EDITS = [
    ("a shot ID with a letter after its number (ID-03, compile's file names)", "### SHOT SC10-SH010 ",
     "### SHOT SC10-SH010X "),
    ("a shot ID one digit short (ID-03)", "### SHOT SC10-SH020 ", "### SHOT SC10-SH02 "),
    ("a setup ID with a character outside the ID letters (CRAFT-07)", "### SETUP SC10-SU01 ", "### SETUP Zoë-SC10-SU01 "),
    ("a project with no frame shape (compile)", "- frame_shape: 2.39\n", ""),
    ("characters with no tier (compile)", "- tier: principal\n", ""),
]


def main():
    previs_stubs()
    plate_route_pictures()
    plate_route_travel()
    reference_pictures_turned()
    film_02_side_reversed()
    gen_15_mood_and_meaning()
    words_01_body_words()
    time_01_unresolved_lines()
    refresh_age_limit()
    spoken_line_whole_words()
    plain_names_of_add_on_records()
    title_card_never_mirrored()
    flip_never_on_the_plate_route()
    pre_reversed_sides()
    crash_search()
    failures = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failures else 'FAIL'} ({failures} failing groups)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
