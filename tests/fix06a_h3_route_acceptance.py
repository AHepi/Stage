"""The acceptance test of work package A of Project notes 43: the route MiniMax H3 in ComfyUI, Reference to Video
(the clip book), and the prompt changes behind it (Project notes 42, W2 to W11).

What it proves, on a copy of the saved scene 10 project (tests/fixtures/chat saved scene 10, with the scene 10
excerpt for the spoken lines) and on small generic shots built in code:
- the route entry loads, carries a mark (V, U or J) with sources for its facts and a kit mark for each rule, and is
  never chosen automatically: scene 10's routing without --route is the same with and without the entry;
- every length on the route's grid from 124 to 362 frames has a one-decimal number of seconds to type that lands on
  it whichever way the template rounds;
- compile --route writes the six pages of the clip book and the scene's machine file; every clip holds one to three
  shots, has its frames on the grid, a tail of at least 1.3 seconds and a part to keep inside the clip; the shot map
  holds every video shot exactly once;
- every prompt has MiniMax's six sections in order, picture labels that match the pictures connected, <Subject 1> as
  the place, the descriptions word for word, speaker numbers in order, the story's lines word for word, and no word H3
  would show or say outside the spoken lines and the pasted descriptions;
- generic shots: two singles of people facing each other are a clip each, and share a clip after a two-shot; a contact
  pair stays in one clip (with the similar-framing warning) and a contact inside one shot is reported;
- every clip page names its master picture and its character pictures; the settings page names only boxes the
  adapter's settings name;
- TAKE rule lines turn a rule confirmed or wrong, which changes its check's level (an error, or not run);
- the hosted H3 prompts lose the stillness and absence words, no take question holds "stay still", stage.py check over
  the project raises no GEN line for a route clip, and no new file holds an email address.

Usage: python tests/fix06a_h3_route_acceptance.py
Standard library only.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parent.parent
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
TOOLS = SKILL / "tools"
STAGE = TOOLS / "stage.py"
sys.path.insert(0, str(TOOLS))

from stage_tools.record_format import load_skill_data, split_item  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
FIXTURES = REPOSITORY / "tests" / "fixtures"
CHAT_FOLDER = FIXTURES / "chat saved scene 10"
EXCERPT = FIXTURES / "The Catch - lines 397-489.txt"
MACHINE = "For machines - do not edit"
PROMPTS = f"{MACHINE}/prompts"
SYNTAX = f"{MACHINE}/prompts - syntax tests"
BOOK = "20 Prompts for AI video/MiniMax H3 in ComfyUI"
ROUTE = "minimax-h3-comfyui-r2v"
SECTIONS = ["subject_definitions", "summary", "retention_analysis", "detailed_description", "overall_soundscape",
            "non_diegetic_music"]
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}")
RESULTS = []


def report(passed, group, detail=""):
    RESULTS.append(bool(passed))
    print(f"{'PASS' if passed else 'FAIL'}  {group}" + (f": {detail}" if detail else ""), flush=True)


def group(title):
    """Run one group: an AssertionError or a fault fails that group only."""
    def decorator(function):
        def run(*arguments):
            try:
                detail = function(*arguments)
            except AssertionError as error:
                report(False, title, str(error)[:1500])
                return
            except Exception as error:  # a fault in the code under test fails the group, never the whole run
                report(False, title, f"{type(error).__name__}: {error}")
                return
            report(True, title, detail or "")
        return run
    return decorator


def stage(arguments):
    environment = dict(os.environ)
    environment["STAGE_LOCK_WAIT_SECONDS"] = "2"
    completed = subprocess.run([sys.executable, str(STAGE)] + [str(argument) for argument in arguments],
                               capture_output=True, text=True, encoding="utf-8", cwd=str(REPOSITORY),
                               env=environment, timeout=900)
    return completed.returncode, completed.stdout + completed.stderr


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def adapters_documents():
    return {name: load(SKILL / "adapters" / name) for name in
            ("video_models.json", "image_models.json", "audio_models.json", "routing.json", "phrasebook.json")}


def section_of(prompt, name):
    match = re.search(r"^" + re.escape(name) + r":\n(.*?)(?=\n\n(?:" + "|".join(SECTIONS) + r"):\n|\Z)", prompt,
                      re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def outside_lines(text):
    text = re.sub(r"<d>.*?</d>", " ", text, flags=re.DOTALL)
    return re.sub(r'"[^"]*"', " ", text)


# ---------------------------------------------------------------- generic shots built in code

class FakeRecord:
    """A record as the grouping reads it: get, get_all, identifier, title, type_name."""

    def __init__(self, identifier, fields, title="", type_name="SHOT"):
        self.identifier = identifier
        self.title = title
        self.type_name = type_name
        self.fields = {name: (value if isinstance(value, list) else [value]) for name, value in fields.items()}

    def get(self, name, default=None):
        values = self.fields.get(name) or []
        return values[0] if values else default

    def get_all(self, name):
        return list(self.fields.get(name) or [])

    def field_names(self):
        return list(self.fields)


class FakeBreakdown:
    def __init__(self, records):
        self.by_identifier = {record.identifier: record for record in records}
        self.constants = CONSTANTS

    def record(self, identifier, type_name=None):
        record = self.by_identifier.get(identifier)
        return record if record is not None and (type_name is None or record.type_name == type_name) else None

    def items(self, record, field_name):
        return [split_item(value) for value in record.get_all(field_name)]


class FakeCompiler:
    def __init__(self, breakdown):
        self.breakdown = breakdown
        self.words = WORDS


def fake_plan(identifier, people, seconds=3.0, size="medium", angle="eye_level", setup="SC01-SU01", moments=(),
              kind="live", held=False, end=""):
    """A ShotPlan of a generic shot: people as (reference, at, faces)."""
    from stage_tools.compile_prompts import Person, ShotPlan
    fields = {"size": size, "angle": angle, "setup": setup, "move": "static", "kind": kind, "screen_time": str(seconds)}
    if moments:
        fields["moment"] = list(moments)
    if end:
        fields["end"] = end
    shot = FakeRecord(identifier, fields, title=f"Generic shot {identifier[-3:]}")
    persons = []
    for reference, at, faces in people:
        element = reference.split(".")[0]
        item = split_item(f"{reference} | at: {at} | faces: {faces}")
        persons.append(Person(reference=reference, element=element, item=item, name=element[3:].title(), noun="person",
                              pronoun=("they", "their", "Their"), at=at, faces=faces))
    return ShotPlan(shot=shot, identifier=identifier, scene="SC01", kind=kind, video=True, route="auto",
                    route_note="", held=held, held_why="marked held: yes" if held else "", screen_time=seconds,
                    needed_s=seconds + 1.5, mirror=None, prompt_flipped_all=False, people=persons)


def generic_grouping(plans):
    from stage_tools.clip_book import Grouper, RouteFacts
    from stage_tools.compile_prompts import Adapters
    records = [FakeRecord("SC01", {"location": "LOC-ROOM"}, type_name="SCENE")]
    for number in range(1, 6):
        records.append(FakeRecord(f"SC01-SU0{number}", {"side": "a"}, type_name="SETUP"))
    compiler = FakeCompiler(FakeBreakdown(records))
    route = RouteFacts.from_adapters(Adapters(), ROUTE)
    return Grouper(compiler, route).group("SC01", plans), route


# ---------------------------------------------------------------- the groups

@group("the route entry loads, marks every fact V, U or J with sources, gives each rule a kit mark and a check, and "
       "is never chosen automatically")
def route_entry():
    from stage_tools.compile_prompts import Adapters, is_candidate, is_route
    documents = adapters_documents()
    facts = documents["video_models.json"]["models"][ROUTE]
    assert facts.get("kind") == "route" and facts.get("route_of") == "minimax-h3", facts.get("kind")
    assert facts.get("rewriting_step") is False and facts.get("negative_field") is None
    assert facts["frames"] == {"block": 17, "offset": 5, "min": 124, "max": 362}, facts["frames"]
    assert facts["tail_s_min"] == 1.3 and facts["fps"] == 24
    assert facts["sizes"]["2.39"] == {"full": [1536, 640], "test": [1152, 480]}, facts["sizes"]
    assert facts["sizes"]["16_9"]["full"] == [1344, 768], facts["sizes"]
    marks = facts["marks"]
    bad = [key for key, mark in marks.items() if str(mark).strip()[:1] not in ("V", "U", "J")]
    assert not bad and facts.get("sources"), bad
    for key in ("frames", "sizes", "settings", "inputs", "sections", "tail_s_min"):
        assert key in marks, f"the fact {key} has no mark"
    rules = facts["rules"]
    assert len(rules) >= 20, len(rules)
    for rule in rules:
        assert re.fullmatch(r"H3R-\d{2}", rule["id"]) and rule["kind"] in ("format", "judgement"), rule
        assert rule["mark"] in ("verified", "unclear") and re.fullmatch(r"ROUTE-\d{2}", rule["check"]), rule
        assert rule.get("source") and rule.get("says"), rule
        if rule["kind"] == "judgement":
            assert rule["mark"] == "unclear", f"{rule['id']} is a judgement marked {rule['mark']}"
    adapters = Adapters()
    assert is_route(adapters.video[ROUTE]) and not is_candidate(adapters.video[ROUTE])
    for alias in ("H3 in ComfyUI", "h3-comfyui", "H3 R2V", "h3_comfyui_r2v"):
        assert adapters.find(alias)[0] == ROUTE, alias
    assert adapters.find("H3")[0] == "minimax-h3", "the hosted H3 lost its own alias"
    hosted = documents["video_models.json"]["models"]["minimax-h3"]
    assert any("rewriting step" in entry for entry in hosted["access"]), hosted["access"]
    boxes = {setting["box"] for setting in facts["settings"]}
    for box in ("Boolean (Enable Lightning LoRA)", "Int (Full)", "Float (Duration)", "ref_image_size", "RandomNoise"):
        assert box in boxes, box
    return f"{len(rules)} rules ({sum(rule['mark'] == 'verified' for rule in rules)} verified), {len(boxes)} boxes"


@group("scene 10's routing without --route is the same with and without the route entry")
def routing_unchanged():
    from stage_tools.compile_prompts import Adapters, analyse_shot, choose_scene_model, route_shot
    from stage_tools.derive_fields import Breakdown
    breakdown = Breakdown.from_project(CHAT_FOLDER, SCHEMA, WORDS, CONSTANTS)
    documents = adapters_documents()
    without = json.loads(json.dumps(documents))
    del without["video_models.json"]["models"][ROUTE]
    results = []
    for docs in (documents, without):
        adapters = Adapters(docs)
        plans = [analyse_shot(breakdown, adapters, shot, {}) for shot in breakdown.shots_of("SC10")]
        scene_model, _ = choose_scene_model(adapters, plans)
        results.append((scene_model, {plan.identifier: route_shot(adapters, plan, scene_model).model
                                      for plan in plans if plan.video}))
    assert results[0] == results[1], f"{results[0]} != {results[1]}"
    assert ROUTE not in results[0][1].values() and results[0][0] != ROUTE
    return f"scene model {results[0][0]}; {len(results[0][1])} shots routed the same"


@group("every length on the grid from 124 to 362 frames has a one-decimal value to type that lands on it both ways")
def grid_lengths():
    from stage_tools.clip_book import RouteFacts, duration_to_type, frames_for, frames_from_duration_box
    from stage_tools.compile_prompts import Adapters
    route = RouteFacts.from_adapters(Adapters(), ROUTE)
    grid = route.grid()
    assert grid[0] == 124 and grid[-1] == 362 and all((frames - 5) % 17 == 0 for frames in grid), grid
    typed = {}
    for frames in grid:
        seconds = duration_to_type(frames)
        assert seconds is not None, f"no value lands on {frames}"
        assert round(seconds * 10) == seconds * 10 or abs(round(seconds, 1) - seconds) < 1e-9, seconds
        assert frames_from_duration_box(seconds, False) == frames == frames_from_duration_box(seconds, True), frames
        typed[frames] = seconds
    assert typed[277] == 11.5 and typed[209] == 8.7, typed
    assert frames_for(10.0, route) == (277, True), frames_for(10.0, route)
    assert frames_for(2.0, route) == (124, True), frames_for(2.0, route)
    assert frames_for(15.0, route) == (362, False), frames_for(15.0, route)
    return f"{len(grid)} lengths, from 124 (type {typed[124]}) to 362 (type {typed[362]})"


@group("compile --route writes the six pages and the machine file; every clip has one to three shots, frames on the "
       "grid, a tail of at least 1.3 seconds and a keep inside the clip; the shot map holds every video shot once")
def clip_book_written(project, output, code):
    from stage_tools.compile_prompts import Adapters, analyse_shot
    from stage_tools.derive_fields import Breakdown
    assert code in (0, 1), f"exit {code}\n{output[-1500:]}"
    pages = ["00 Settings and how to run a clip.md", "01 Pictures to make first.md", "Scene 10 - Saye's kitchen.md",
             "Shot map.md", "If a clip goes wrong.md", "Take log.md"]
    for name in pages:
        assert (project / BOOK / name).is_file(), f"{name} was not written\n{output[-800:]}"
    pack = load(project / PROMPTS / f"SC10 - {ROUTE}.json")
    assert pack["kind"] == "clip_book" and pack["route"] == "h3_comfyui_r2v", pack.get("kind")
    clips = pack["clips"]
    assert clips, "no clips"
    numbers = [clip["clip"] for clip in clips]
    assert numbers == [f"SC10-CL{index:02d}" for index in range(1, len(clips) + 1)], numbers
    for clip in clips:
        assert 1 <= len(clip["shots"]) <= 3, (clip["clip"], len(clip["shots"]))
        assert (clip["frames"] - 5) % 17 == 0 and 124 <= clip["frames"] <= 362, clip["frames"]
        assert clip["tail_s"] >= 1.3 - 1e-6, (clip["clip"], clip["tail_s"])
        assert 0 < clip["keep_s"] <= clip["frames"] / 24 - 1.3 + 1e-6, (clip["clip"], clip["keep_s"])
        assert clip["shots"][0]["clip_from_s"] == 0, clip["shots"][0]
        assert clip["title"], clip["clip"]
    breakdown = Breakdown.from_project(project, SCHEMA, WORDS, CONSTANTS)
    adapters = Adapters()
    video = [plan.identifier for plan in (analyse_shot(breakdown, adapters, shot, {})
                                          for shot in breakdown.shots_of("SC10")) if plan.video]
    mapped = [entry["shot"] for entry in pack["shot_map"] if entry.get("part", 1) == 1]
    assert sorted(mapped) == sorted(video), f"shot map {mapped} != video shots {video}"
    assert len(mapped) == len(set(mapped)), "a shot appears twice in the shot map"
    shot_map = (project / BOOK / "Shot map.md").read_text(encoding="utf-8")
    for identifier in video:
        assert f"shot {identifier[-3:]}" in shot_map, f"{identifier} is missing from the shot map page"
    groups = "; ".join(f"{clip['clip'][-4:]}: " + ", ".join(shot["shot"][-3:] for shot in clip["shots"]) for clip in clips)
    return f"{len(clips)} clips for {len(video)} video shots ({groups})"


@group("every prompt has the six sections in order, picture labels matching the wiring, <Subject 1> as the place, "
       "the descriptions word for word, speaker numbers in order and the story's lines word for word")
def prompts_in_format(project):
    from stage_tools.derive_fields import Breakdown
    from stage_tools.compile_prompts import raw_speeches_of
    pack = load(project / PROMPTS / f"SC10 - {ROUTE}.json")
    breakdown = Breakdown.from_project(project, SCHEMA, WORDS, CONSTANTS)
    speeches = raw_speeches_of(story_path=str(EXCERPT), constants=CONSTANTS)
    lines_seen = 0
    for clip in pack["clips"]:
        prompt = clip["prompt"]
        assert re.findall(r"^(\w+):$", prompt, flags=re.MULTILINE) == SECTIONS, clip["clip"]
        connections = clip["connections"]
        used = sorted({int(number) for number in re.findall(r"<Picture (\d+)>", prompt)})
        assert used == list(range(1, len(connections) + 1)), (clip["clip"], used, len(connections))
        for index, connection in enumerate(connections, start=1):
            assert connection["label"] == f"<Picture {index}>" and connection["input"] == f"ref_image_{index - 1}"
        definitions = section_of(prompt, "subject_definitions")
        assert definitions.startswith("<Subject 1> is Saye's kitchen shown in <Picture 1>"), definitions[:80]
        assert "<Picture 1> is the shot-planning reference for [Shot 1]" in definitions
        normalised = " ".join(prompt.split())
        for key in clip["keys"]:
            assert " ".join(key["text"].split()).rstrip(".") in normalised, (clip["clip"], key["record"])
        for person in clip["people"]:
            record = breakdown.record(person["person"])
            fixed = " ".join(str(record.get("fixed_description")).split()).rstrip(".")
            assert fixed in normalised, (clip["clip"], person["person"])
        order = []
        for number in re.findall(r"\((S\d+)\)", prompt):
            if number not in order:
                order.append(number)
        assert order == [f"S{index}" for index in range(1, len(order) + 1)], (clip["clip"], order)
        assert "(S" not in section_of(prompt, "retention_analysis")
        for speech in clip["speeches"]:
            story = speeches.get(speech["speech"]) or {}
            text = re.sub(r"\s*\([^)]*\)\s*", " ", str(story.get("text") or "")).strip()
            if text:
                assert speech["line"] in text, (speech["speech"], speech["line"], text)
                assert f"] {speech['line']}</d>" in prompt, speech["speech"]
                lines_seen += 1
        description = section_of(prompt, "detailed_description")
        assert description.startswith("The target video is"), description[:60]
        assert len(re.findall(r"From \d{2}:\d{2}\.\d{3} to the end", description)) == 1, clip["clip"]
        assert section_of(prompt, "non_diegetic_music").strip() == "N/A"
    assert lines_seen >= 5, f"only {lines_seen} spoken lines were checked against the story"
    return f"{len(pack['clips'])} prompts; {lines_seen} lines word for word"


@group("no word H3 would show or say (absence, stillness, talk about speaking, comparison) outside the spoken lines "
       "and the pasted descriptions")
def no_banned_words(project):
    from stage_tools.compile_prompts import Adapters, WordFixer
    fixer = WordFixer(Adapters(), WORDS, None)
    pack = load(project / PROMPTS / f"SC10 - {ROUTE}.json")
    found = []
    for clip in pack["clips"]:
        text = clip["prompt"]
        for key in clip["keys"]:
            for form in (key["text"], key["text"].rstrip(".")):
                text = text.replace(form, " ")
        text = text.replace(clip["style_sentence"], " ")
        word = fixer.kept_out_word(outside_lines(text), ("absence", "stillness", "talk", "comparison"))
        if word:
            found.append(f"{clip['clip']}: {word}")
    assert not found, found
    left_out = sum(len(clip["left_out"]) for clip in pack["clips"])
    return f"clean; {left_out} clauses left out and listed on the pages"


@group("generic shots: two singles of people facing each other are a clip each, and share a clip after a two-shot")
def facing_singles():
    first = fake_plan("SC01-SH010", [("CH-ANNA.S01", "left_third", "CH-BEN")], setup="SC01-SU01")
    second = fake_plan("SC01-SH020", [("CH-BEN.S01", "right_third", "CH-ANNA")], setup="SC01-SU02")
    clips, _ = generic_grouping([first, second])
    assert [[shot.identifier for shot in clip.shots] for clip in clips] == [["SC01-SH010"], ["SC01-SH020"]], \
        [[shot.identifier for shot in clip.shots] for clip in clips]
    both = fake_plan("SC01-SH005", [("CH-ANNA.S01", "left_third", "CH-BEN"), ("CH-BEN.S01", "right_third", "CH-ANNA")],
                     size="medium_wide", setup="SC01-SU03")
    first = fake_plan("SC01-SH010", [("CH-ANNA.S01", "left_third", "CH-BEN")], setup="SC01-SU01")
    second = fake_plan("SC01-SH020", [("CH-BEN.S01", "right_third", "CH-ANNA")], setup="SC01-SU02")
    clips, _ = generic_grouping([both, first, second])
    assert [[shot.identifier for shot in clip.shots] for clip in clips] == [["SC01-SH005", "SC01-SH010", "SC01-SH020"]], \
        [[shot.identifier for shot in clip.shots] for clip in clips]
    assert [shot.clip_start for shot in clips[0].shots] == [0.0, 3.0, 6.0]
    return "two clips without the two-shot; one clip of three after it"


@group("generic shots: a contact pair stays in one clip with its contact cut (and the similar-framing warning); a "
       "contact inside one shot is reported; a held take is a clip of its own")
def contact_pair():
    from stage_tools.checks_clip_book import check_contact, check_similar_framing
    from stage_tools.clip_book import clip_entry, contact_in_shot
    cause = fake_plan("SC01-SH010", [("CH-ANNA.S01", "left_third", "right")],
                      moments=["0-3 | shows: she lifts the bar and drives it into the panel"])
    result = fake_plan("SC01-SH020", [("CH-ANNA.S01", "left_third", "right")],
                       moments=["0-3 | shows: the panel cracks across and sags"])
    clips, route = generic_grouping([cause, result])
    assert len(clips) == 1 and len(clips[0].shots) == 2, [[shot.identifier for shot in clip.shots] for clip in clips]
    assert clips[0].contact_cuts == [1], clips[0].contact_cuts
    entry = clip_entry(clips[0], route, WORDS)
    assert check_similar_framing(None, {}, entry, route.facts), "two alike framings joined by a contact were not flagged"
    plain = fake_plan("SC01-SH010", [("CH-ANNA.S01", "left_third", "right")], moments=["0-3 | shows: she lifts the bar"])
    again = fake_plan("SC01-SH020", [("CH-ANNA.S01", "left_third", "right")], moments=["0-3 | shows: she looks down"])
    clips, _ = generic_grouping([plain, again])
    assert len(clips) == 2, "two alike framings with no contact shared a clip"
    inside = fake_plan("SC01-SH030", [("CH-BEN.S01", "centre", "camera")],
                       moments=["0-2 | shows: he kicks the crate", "2-4 | shows: the crate tips over"], seconds=4.0)
    assert contact_in_shot(inside.shot, WORDS) == ("kicks", "tips over"), contact_in_shot(inside.shot, WORDS)
    clips, route = generic_grouping([inside])
    found = check_contact(None, {}, clip_entry(clips[0], route, WORDS), route.facts)
    assert found and "contact inside one shot" in found[0][1], found
    held = fake_plan("SC01-SH040", [("CH-BEN.S01", "centre", "camera")], seconds=16.0, held=True)
    short = fake_plan("SC01-SH050", [("CH-BEN.S01", "centre", "camera")], size="close_up", setup="SC01-SU02")
    clips, _ = generic_grouping([held, short])
    assert [len(clip.shots) for clip in clips] == [1, 1] and clips[0].frames == 362 and clips[0].overflow_s > 0, \
        [(len(clip.shots), clip.frames, clip.overflow_s) for clip in clips]
    return "contact pair in one clip; contact on screen reported; held take alone at 362 frames"


@group("generic shots: a long shot that is not held splits at its planned cutaway, else into equal parts, each part a "
       "clip of its own")
def long_shot_split():
    long_shot = fake_plan("SC01-SH010", [("CH-ANNA.S01", "centre", "camera")], seconds=20.0,
                          moments=["0-9 | shows: she sorts the papers", "9-11 | shows: a cutaway to the door",
                                   "11-20 | shows: she sorts the papers again"])
    clips, _ = generic_grouping([long_shot])
    spans = [(shot.shot_start, shot.shot_end, shot.part, shot.parts) for clip in clips for shot in clip.shots]
    assert spans == [(0.0, 9.0, 1, 2), (9.0, 20.0, 2, 2)], spans
    plain = fake_plan("SC01-SH020", [("CH-ANNA.S01", "centre", "camera")], seconds=20.0,
                      moments=["0-20 | shows: she sorts the papers"])
    clips, route = generic_grouping([plain])
    spans = [(shot.shot_start, shot.shot_end) for clip in clips for shot in clip.shots]
    assert spans == [(0.0, 10.0), (10.0, 20.0)] and all(clip.frames <= 362 for clip in clips), spans
    assert all(clip.keep_s <= route.longest_kept_s + 1e-6 for clip in clips)
    return "split at the cutaway (0-9, 9-20); without one, two equal parts"


@group("the project's video_route h3_comfyui_r2v makes compile write the clip book without --route")
def project_route(project):
    start = project / "00 Start here.md"
    text = start.read_text(encoding="utf-8")
    text = text.replace("- rights: mine\n", "- rights: mine\n- video_route: h3_comfyui_r2v\n", 1)
    start.write_text(text, encoding="utf-8")
    book = project / PROMPTS / f"SC10 - {ROUTE}.json"
    if book.exists():
        book.unlink()
    code, output = stage(["compile", "--scene", "SC10", "--project", project, "--story", EXCERPT])
    assert book.is_file(), output[-800:]
    assert "clips for MiniMax H3 in ComfyUI" in output, output[-800:]
    code, output = stage(["compile", "--scene", "SC10", "--model", "kling-3.0-omni", "--project", project,
                          "--story", EXCERPT])
    assert "Kling 3.0 Omni" in output and "clips for MiniMax H3 in ComfyUI" not in output, output[-800:]
    # set through a CHOICE, as step 14's checkpoint asks: the user's field is backed by the answer (no FORM-10)
    choices = project / "01 Choices.md"
    text = choices.read_text(encoding="utf-8")
    count = int(re.search(r"END OF FILE \| Choices \| (\d+) records", text).group(1))
    choice = ("### CHOICE CHOICE-099 Way the video is made\n"
              "- question: Which way will you make the video?\n"
              "- why: The clip book for MiniMax H3 in ComfyUI is made only when asked.\n"
              "- option: a | text: Stage picks a model for each scene\n"
              "- option: b | text: MiniMax H3 in ComfyUI, Reference to Video\n"
              "- default: a | reason: Stage picks a model for each scene unless asked\n"
              "- answer: b\n- asked: yes\n- checkpoint: e\n- affects: PROJECT.video_route\n"
              "- sets: PROJECT.video_route | value: per_scene | when: a\n"
              "- sets: PROJECT.video_route | value: h3_comfyui_r2v | when: b\n"
              "- status: answered\n- date: 2026-10-10\n\n")
    text = re.sub(r"END OF FILE \| Choices \| \d+ records", f"END OF FILE | Choices | {count + 1} records", text)
    text = text.replace(f"END OF FILE | Choices | {count + 1} records", choice + f"END OF FILE | Choices | {count + 1} records")
    choices.write_text(text, encoding="utf-8")
    code, checked = stage(["check", "--project", project])
    wrong = [line for line in checked.splitlines() if ("video_route" in line or "CHOICE-099 sets" in line)
             and re.match(r"^E (FORM|ID)-", line)]
    assert not wrong, wrong
    return "video_route makes the clip book; asking for a model still makes the usual pack; a CHOICE sets it"


@group("every clip page names its master picture and character pictures; the settings page names only boxes the "
       "adapter's settings name")
def pages_name_pictures(project):
    pack = load(project / PROMPTS / f"SC10 - {ROUTE}.json")
    page = (project / BOOK / "Scene 10 - Saye's kitchen.md").read_text(encoding="utf-8")
    parts = re.split(r"(?m)^## Clip ", page)[1:]
    assert len(parts) == len(pack["clips"]), (len(parts), len(pack["clips"]))
    for part, clip in zip(parts, pack["clips"]):
        assert re.search(r"(?m)^Master picture: M\d+", part), part[:200]
        for person in clip["people"]:
            assert f"{person['name']} (Reference pictures/" in part, (clip["clip"], person["name"])
        assert "----- COPY FROM HERE -----" in part and "----- COPY TO HERE -----" in part
        assert re.search(r"Length: \d+ frames \(\d+\.\d\d seconds\)\. Type \d+(?:\.\d)? in Float \(Duration\)\.", part), \
            part[:300]
        assert "Connect nothing else." in part and "### Keep" in part and "### Check" in part
        assert clip["master_picture"].get("code") and len(clip["character_pictures"]) == len(clip["people"])
    facts = adapters_documents()["video_models.json"]["models"][ROUTE]
    boxes = {setting["box"] for setting in facts["settings"]}
    settings = (project / BOOK / "00 Settings and how to run a clip.md").read_text(encoding="utf-8")
    listed = re.findall(r"(?m)^- (.+?): .+ Why: ", settings)
    assert listed and set(listed) <= boxes, f"{set(listed) - boxes}"
    named = set(re.findall(r"\b(?:Boolean|Int|Float|Resolution Selector|Input Text) \([^)]+\)", settings + page))
    assert named <= boxes, named - boxes
    pictures = (project / BOOK / "01 Pictures to make first.md").read_text(encoding="utf-8")
    assert "### M1 - " in pictures and "deserted" in pictures and "Checklist before you use a picture" in pictures
    return f"{len(parts)} clip pages; settings name {len(listed)} boxes"


@group("TAKE rule lines turn a rule confirmed or wrong, and the check's level follows (an error, or not run)")
def take_log_marks(project):
    from stage_tools.check_records import CheckRun
    from stage_tools.checks_clip_book import route_problems, rule_marks
    from stage_tools.derive_fields import Breakdown
    takes = project / "20 Prompts for AI video" / "Takes.md"
    records = []
    for number in (1, 2):
        records.append(
            f"### TAKE TK-SC10-CL07-T0{number} Test take {number}\n"
            "- clip: SC10-CL07\n"
            f"- model: {ROUTE} (model facts 2026-09-27)\n"
            "- route: start picture and character pictures\n"
            "- inputs: Scene 10 - clip 07 - start picture.png\n"
            f"- seed: {1000 + number}\n"
            "- settings: 362 frames, 1152 x 480, Lightning off, 20 steps\n"
            "- cost_usd: 0\n"
            f"- file: Scene 10 - clip 07 - take 0{number}.mp4\n"
            "- review: Is each line said once, by the right mouth? | answer: yes | evidence: watched twice\n"
            "- rule: H3R-15 | verdict: confirmed | note: the words left out never showed up\n"
            "- rule: H3R-14 | verdict: wrong | note: a short prompt moved as well as a long one\n"
            "- refusals: 0\n- status: draft\n")
    takes.write_text("# Takes\n\nThe takes made so far.\n\nBelow this line: details for the AI and the checker. You never "
                     "need to read them.\n\n" + "\n".join(records) + "\nEND OF FILE | Takes | 2 records\n",
                     encoding="utf-8")
    breakdown = Breakdown.from_project(project, SCHEMA, WORDS, CONSTANTS)
    facts = adapters_documents()["video_models.json"]["models"][ROUTE]
    marks = rule_marks(breakdown, facts["rules"], facts)
    assert marks["H3R-15"]["mark"] == "confirmed", marks["H3R-15"]
    assert marks["H3R-14"]["mark"] == "wrong", marks["H3R-14"]
    assert marks["H3R-16"]["mark"] == "unclear" and marks["H3R-01"]["mark"] == "verified"
    assert marks["H3R-15"]["confirmed"] == ["TK-SC10-CL07-T01", "TK-SC10-CL07-T02"], marks["H3R-15"]
    entry = {"clip": "SC10-CL01", "scene": "SC10", "prompt": "detailed_description:\nnothing here\n", "keys": [],
             "style_sentence": "", "key_problems": [], "shots": []}
    run = CheckRun(breakdown.record_files, SCHEMA, WORDS, CONSTANTS)
    before = route_problems(run, [{"scene": "SC10", "clips": [entry]}], facts,
                            rule_marks(None, facts["rules"], facts))
    after = route_problems(run, [{"scene": "SC10", "clips": [entry]}], facts, marks)
    level = {problem.check_id: problem.level for problem in before}
    assert level.get("ROUTE-15") == "W" and level.get("ROUTE-14") == "W", level
    level_after = {problem.check_id: problem.level for problem in after}
    assert level_after.get("ROUTE-15") == "E", level_after
    assert "ROUTE-14" not in level_after, "a rule the takes showed wrong was still checked"
    code, output = stage(["compile", "--scene", "SC10", "--route", "h3-comfyui", "--project", project,
                          "--story", EXCERPT])
    log = (project / BOOK / "Take log.md").read_text(encoding="utf-8")
    assert "| H3R-15 |" in log and "confirmed" in log and "TK-SC10-CL07-T01" in log, log[:600]
    assert "wrong (dropped" in log, "the take log does not list the dropped rule"
    assert not re.search(r"(?m)^[EW] ROUTE-14\b", output), "ROUTE-14 still ran after the takes showed it wrong"
    code, checked = stage(["check", "--project", project])
    # the rule lines and the route clip IDs are read as the schema says (the user's own field `kept` is left out on
    # purpose: only the user writes it)
    form = [line for line in checked.splitlines()
            if re.match(r"^E (?:FORM-0[234]|FORM-12|ID-\d\d) .*TK-SC10-CL07", line)]
    assert not form, form
    return "H3R-15 confirmed (its check now an error), H3R-14 wrong (not run); the take log page lists both"


@group("the hosted H3 prompts lose the stillness and absence words; no take question holds 'stay still' on any "
       "route; stage.py check raises no GEN line for a route clip")
def hosted_h3_words(project):
    code, output = stage(["compile", "--scene", "SC10", "--force-model", "minimax-h3", "--project", project,
                          "--story", EXCERPT])
    assert code in (0, 1), output[-1000:]
    pack = load(project / SYNTAX / "SC10 - minimax-h3.json")
    found = []
    for clip in pack["clips"]:
        prompt = re.sub(r"<d>.*?</d>", " ", clip["prompt"]).replace("with no camera movement whatsoever", " ")
        for word in ("still", "The camera does not move", "nothing", "not", "none", "never", "contained",
                     "and nothing else"):
            if re.search(r"(?<![\w-])" + re.escape(word) + r"(?![\w-])", prompt, re.IGNORECASE):
                found.append(f"{clip['clip']}: {word}")
        assert prompt.count("The shot is static, on a tripod, with no camera movement whatsoever.") <= 1
        assert "non_diegetic_music: N/A" in clip["prompt"], clip["clip"]
    assert not found, found
    code, normal = stage(["compile", "--scene", "SC10", "--project", project, "--story", EXCERPT])
    assert code == 0, normal[-800:]
    questions = []
    for path in list((project / PROMPTS).glob("SC10 - *.json")) + list((project / SYNTAX).glob("SC10 - *.json")):
        data = load(path)
        for clip in data.get("clips") or []:
            questions += clip.get("questions") or []
    assert questions and not [question for question in questions if re.search(r"stays? still", question)], \
        [question for question in questions if re.search(r"stays? still", question)][:3]
    assert (project / PROMPTS / f"SC10 - {ROUTE}.json").is_file(), "a normal compile deleted the clip book"
    code, checked = stage(["check", "--project", project])
    gen_route = [line for line in checked.splitlines() if re.match(r"^[EWN] GEN-\d\d SC10-CL\d\d", line)]
    assert not gen_route, gen_route
    assert re.search(r"(?m)^[EW] ROUTE-\d\d SC10-CL\d\d", checked), "stage.py check ran no route check"
    return f"{len(pack['clips'])} hosted H3 prompts clean; {len(questions)} questions; check reads the clip book"


@group("no email address in any new or changed file of this work")
def no_email(project):
    files = [SKILL / "tools" / "stage_tools" / "clip_book.py", SKILL / "tools" / "stage_tools" / "checks_clip_book.py",
             Path(__file__), SKILL / "adapters" / "video_models.json", SKILL / "adapters" / "phrasebook.json",
             SKILL / "library" / "C3 Writing prompts for video models.md",
             SKILL / "cards" / "21 Making pictures and video with AI.md",
             SKILL / "steps" / "14 Add-on - generation packs.md"]
    files += sorted((project / BOOK).glob("*.md")) + [project / PROMPTS / f"SC10 - {ROUTE}.json"]
    found = []
    for path in files:
        found += [f"{path.name}: {match}" for match in EMAIL.findall(path.read_text(encoding="utf-8"))]
    assert not found, found
    return f"{len(files)} files"


def main():
    route_entry()
    routing_unchanged()
    grid_lengths()
    facing_singles()
    contact_pair()
    long_shot_split()
    with tempfile.TemporaryDirectory() as temporary:
        project = Path(temporary) / "scene 10"
        shutil.copytree(CHAT_FOLDER, project)
        code, output = stage(["compile", "--scene", "SC10", "--route", "h3-comfyui", "--project", project,
                              "--story", EXCERPT])
        clip_book_written(project, output, code)
        prompts_in_format(project)
        no_banned_words(project)
        pages_name_pictures(project)
        hosted_h3_words(project)
        take_log_marks(project)
        no_email(project)
        project_route(project)
    failing = len([passed for passed in RESULTS if not passed])
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({len(RESULTS) - failing} groups passed, {failing} failed)")
    return 0 if not failing else 1


if __name__ == "__main__":
    sys.exit(main())
