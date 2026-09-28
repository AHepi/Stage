"""The acceptance test of work package 8: generation (the adapter files, compile_prompts.py, make_text_graphics.py,
refresh_models.py and the commands compile, graphics and refresh-models).

What it proves, as the blueprint's row for WP8 asks (14.2), on the WP12a gold (examples/01 and 02 made into a
project folder):
- the dated model facts: every adapter file loads, carries its checked_on date and a mark (V, U or J) with a source
  for its facts; the facts compile and the GEN checks read are there (clip lengths, sizes, speaker forms), and the
  shape check of refresh-models finds nothing;
- compile --scene SC10 exits 0 with 0 GEN errors, and the checker run afterwards over the written packs prints no GEN
  error either; the packs have the shape the GEN checks read, are dated and (while the facts are fresh) priced;
- shot 150, a held turn shot of 15 seconds, is one clip on Seedance 2.5 and never split;
- compile --force-model veo-3.1 writes the colon speaker form with no quotation marks ("... says: Who are you
  calling?"), into the syntax-test folders only;
- a non-held 18-second copy of shot 140 with a planned cutaway at 8 seconds splits there on Kling: two clips of 10
  and 12 seconds, each with its own start picture, and no word about the cutaway in the prompts;
- the prompts never carry reasons, record IDs, banned words or quoted signs; with a start picture they are motion
  only; without one they paste the fixed descriptions word for word;
- --lint-only writes nothing, --model writes only that model's pack, --storyboard writes the frame prompts;
- graphics draws the title card (never mirrored, D12 Recipe 7's numbers) and a sign, normal and mirrored with the
  translate-and-scale wrapper, and gives the sign's reading time from the text_floor constant;
- refresh-models checks, proposes and applies a refresh on a copy of the adapters, and holds back a price change
  until the user approves it;
- no email address in any adapter file or written page, and the refresh tool makes no web request.

Usage: python tests/wp8_acceptance.py [--story "<The Catch, the whole story>"]
The scene 10 excerpt (tests/fixtures/The Catch - lines 397-489.txt) gives the speeches; without it the groups that
need the spoken lines say "skipped: story not present". With --story, compile is also run with --story on it.
Standard library only.
"""

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ElementTree
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parent.parent
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
TOOLS = SKILL / "tools"
STAGE = TOOLS / "stage.py"
ADAPTERS = SKILL / "adapters"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(REPOSITORY / "tests"))

from stage_tools.derive_fields import constant  # noqa: E402
from stage_tools.record_format import load_skill_data  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
FIXTURES = REPOSITORY / "tests" / "fixtures"
EXCERPT = FIXTURES / "The Catch - lines 397-489.txt"
MACHINE = "For machines - do not edit"
PROMPTS = f"{MACHINE}/prompts"
SYNTAX = f"{MACHINE}/prompts - syntax tests"
PAGES = "20 Prompts for AI video"
SCENE_FILE = "11 Scenes/Scene 10 - Saye's kitchen.md"
FACTS_DATE = "2026-09-27"
ADAPTER_FILES = ("video_models.json", "image_models.json", "audio_models.json", "routing.json", "phrasebook.json")
PACK_KEYS = ("clip", "shot", "model", "prompt", "length_s", "resolution", "shape", "inputs", "speeches", "sounds")
IDENTIFIER = re.compile(r"\b(?:SC\d{2,3}|CH|PR|LOC|TX|MO|PIC|VT|PV|STY|LK)-[A-Z0-9]")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}")

RESULTS = []


def report(passed, group, detail=""):
    RESULTS.append(bool(passed))
    print(f"{'PASS' if passed else 'FAIL'}  {group}" + (f": {detail}" if detail else ""), flush=True)


def info(line):
    print(f"INFO  {line}", flush=True)


def group(title):
    """Run one group: an AssertionError or a fault fails that group only; 'skip' reports nothing."""
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
            if detail == "skip":
                return
            report(True, title, detail or "")
        return run
    return decorator


def stage(arguments, cwd=None):
    environment = dict(os.environ)
    environment["STAGE_LOCK_WAIT_SECONDS"] = "2"
    completed = subprocess.run([sys.executable, str(STAGE)] + [str(argument) for argument in arguments],
                               capture_output=True, text=True, encoding="utf-8", cwd=str(cwd or REPOSITORY),
                               env=environment, timeout=900)
    return completed.returncode, completed.stdout + completed.stderr


def make_gold(folder, story):
    """The gold as a project folder (the same helper work package 6's test uses)."""
    from wp6_acceptance import make_gold_project
    return make_gold_project(folder, story)


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def packs_in(folder):
    return {path.name: load(path) for path in sorted(Path(folder).glob("SC10 - *.json")) if "pictures" not in path.name}


def clips_of(packs):
    return [clip for pack in packs.values() for clip in pack["clips"]]


def facts_age():
    checked = datetime.date.fromisoformat(FACTS_DATE)
    return (datetime.date.today() - checked).days


def fresh():
    limit = constant(CONSTANTS, "model_facts_max_age_days", 30)
    return facts_age() <= limit


def lint_lines(output, level=None):
    lines = [line for line in output.splitlines() if re.match(r"^[EWN] GEN-\d{2}\b", line)]
    return [line for line in lines if level is None or line.startswith(level + " ")]


# ---------------------------------------------------------------- the adapter files

@group("the adapter files load, are dated 2026-09-27 and mark every fact V, U or J with its sources")
def adapter_files():
    documents = {name: load(ADAPTERS / name) for name in ADAPTER_FILES}
    for name, document in documents.items():
        assert document.get("checked_on") == FACTS_DATE, f"{name} is dated {document.get('checked_on')}"
    video = documents["video_models.json"]["models"]
    image = documents["image_models.json"]["models"]
    for kind, models in (("video", video), ("image", image)):
        for name, facts in models.items():
            marks = facts.get("marks") or {}
            assert marks, f"the {kind} model {name} has no marks"
            bad = [key for key, mark in marks.items() if str(mark).strip()[:1] not in ("V", "U", "J")]
            assert not bad, f"{name}: marks without V, U or J: {bad}"
            assert facts.get("sources"), f"the {kind} model {name} names no source page"
    for name in ("veo-3.1", "kling-3.0", "kling-3.0-omni", "seedance-2.5", "wan-3.0", "minimax-h3"):
        assert name in video, f"{name} is missing from video_models.json"
    veo = video["veo-3.1"]
    assert veo["length_s"].get("allowed") == [4, 6, 8], veo["length_s"]
    assert ": {line}" in veo["speaker"] and veo.get("speaker_quotes") is False, veo["speaker"]
    kling = video["kling-3.0-omni"]
    assert '"{line}"' in kling["speaker"] and kling["length_s"]["max"] == 15, (kling["speaker"], kling["length_s"])
    seedance = video["seedance-2.5"]
    assert seedance["length_s"]["max"] >= 17, seedance["length_s"]
    routing = documents["routing.json"]
    for need, row in routing["needs"].items():
        for model in (row.get("first") or []) + (row.get("backup") or []):
            assert model in video, f"routing need {need} names {model}, which has no facts"
    assert routing["needs"]["long_take"]["first"] == ["seedance-2.5"], routing["needs"]["long_take"]
    phrasebook = documents["phrasebook.json"]
    assert phrasebook["move"]["static"].endswith("The camera does not move."), phrasebook["move"]["static"]
    from stage_tools.refresh_models import read_documents, shape_problems
    problems = shape_problems(read_documents(ADAPTERS))
    assert not problems, problems
    for name in list(ADAPTER_FILES) + ["prices.json"]:
        text = (ADAPTERS / name).read_text(encoding="utf-8")
        found = EMAIL.findall(text)
        assert not found, f"{name} holds something shaped like an email address: {found[:3]}"
    return (f"{len(video)} video and {len(image)} image models, {len(routing['needs'])} routing needs; "
            "the shape check finds nothing")


# ---------------------------------------------------------------- compile on the gold

@group("compile --scene SC10 on the gold exits 0 with 0 GEN errors; the packs are dated and in the GEN checks' shape")
def compile_gold(project, output, code):
    assert code == 0, f"exit {code}\n{output}"
    assert "Lint: 0 errors" in output, output
    assert not lint_lines(output, "E"), lint_lines(output, "E")
    packs = packs_in(project / PROMPTS)
    assert set(packs) == {"SC10 - kling-3.0-omni.json", "SC10 - seedance-2.5.json"}, sorted(packs)
    for name, pack in packs.items():
        assert pack["model_facts_date"] == FACTS_DATE, (name, pack["model_facts_date"])
        assert pack["compiled_on"] == datetime.date.today().isoformat(), pack["compiled_on"]
        assert pack["paid"] is False, "a pack is paid although the gold sets no spending cap"
        assert any("spending cap" in reason for reason in pack["not_paid_because"]), pack["not_paid_because"]
        assert pack["release"] in ("public", "private"), pack["release"]
        for clip in pack["clips"]:
            missing = [key for key in PACK_KEYS if key not in clip]
            assert not missing, f"{clip.get('clip')} lacks {missing}"
            assert "start_picture" in clip["inputs"], clip["inputs"]
            if fresh():
                assert isinstance(clip.get("cost_usd"), (int, float)) and clip["cost_usd"] > 0, (clip["clip"], clip.get("cost_usd"))
            else:
                assert clip.get("cost_usd") is None, "a price is shown on stale model facts"
    clips = clips_of(packs)
    scene_model = {pack["scene_model"] for pack in packs.values()}
    assert scene_model == {"kling-3.0-omni"}, scene_model
    pages = sorted(path.name for path in (project / PAGES).glob("*.md"))
    assert "Scene 10 - Saye's kitchen - Kling 3.0 Omni.md" in pages and \
        "Scene 10 - Saye's kitchen - pictures to make first.md" in pages, pages
    money = "priced" if fresh() else f"not priced (model facts {facts_age()} days old)"
    return f"{len(clips)} clips in 2 packs, scene model Kling 3.0 Omni, {money}"


@group("the checker over the written packs, and lint_packs on them, find no GEN error")
def checker_after_compile(project):
    code, output = stage(["check", "--project", project])
    errors = [line for line in output.splitlines() if re.match(r"^E GEN-", line)]
    assert not errors, errors
    from stage_tools.check_records import CheckRun, StorySource
    from stage_tools.checks_plan_generation_film import lint_packs
    from stage_tools.derive_fields import Breakdown
    from stage_tools.project_files import Project
    breakdown = Breakdown.from_project(project, SCHEMA, WORDS, CONSTANTS)
    run = CheckRun(breakdown.record_files, SCHEMA, WORDS, CONSTANTS, story=StorySource.from_project(project),
                   project=Project(project, SCHEMA, WORDS))
    problems = lint_packs(run, list(packs_in(project / PROMPTS).values()))
    errors = [problem for problem in problems if getattr(problem, "level", "") == "E"]
    assert not errors, [str(problem) for problem in errors]
    return f"check exit {code}, no GEN line at level E; lint_packs: {len(problems)} lines, none an error"


@group("shot 150 (a held turn shot) is one clip on Seedance 2.5, never split")
def shot_150(project, output):
    clips = [clip for clip in clips_of(packs_in(project / PROMPTS)) if clip["shot"] == "SC10-SH150"]
    assert len(clips) == 1, [clip["clip"] for clip in clips]
    clip = clips[0]
    assert clip["model"] == "seedance-2.5", clip["model"]
    assert clip["held"] is True and clip["chained"] is False, (clip["held"], clip["chained"])
    handles = constant(CONSTANTS, "handles_s", 0.75)
    assert clip["length_s"] >= 15 + 2 * handles, clip["length_s"]
    assert clip["override"], "the move off the scene model has no logged reason"
    assert "Shot 150 goes to Seedance 2.5 as one" in output, output
    assert clip["inputs"]["start_picture"] == "PIC-SC10-SH150-START-01", clip["inputs"]
    from stage_tools.compile_prompts import routed_model
    from stage_tools.derive_fields import Breakdown
    breakdown = Breakdown.from_project(project, SCHEMA, WORDS, CONSTANTS)
    routed = {shot.identifier: routed_model(breakdown, shot) for shot in breakdown.shots_of("SC10")}
    assert routed["SC10-SH150"] == "seedance-2.5" and routed["SC10-SH010"] == "kling-3.0-omni", routed
    return (f"{clip['clip']}: {clip['length_s']:g} seconds at {clip['resolution']}, {clip['shape']}; routed_model "
            "(the shot list's Model column) agrees")


@group("the prompts carry no reasons, record IDs, banned words or quoted signs; start pictures give motion-only prompts")
def prompt_contents(project):
    from stage_tools.derive_fields import Breakdown
    breakdown = Breakdown.from_project(project, SCHEMA, WORDS, CONSTANTS)
    clips = clips_of(packs_in(project / PROMPTS))
    banned = [word.lower() for words in ((WORDS.get("banned_prompt_words") or {}).get("groups") or {}).values()
              for word in words]
    assert "torch" in banned, banned
    fixed = {record.identifier: (record.get("fixed_description") or "").strip()
             for record in breakdown.records_of("CHARACTER")}
    motion_only = with_keys = 0
    for clip in clips:
        prompt = clip["prompt"]
        shot = breakdown.record(clip["shot"], "SHOT")
        found = IDENTIFIER.findall(prompt)
        assert not found, f"{clip['clip']} carries record IDs {found}"
        for word in banned:
            assert not re.search(rf"(?<!\w){re.escape(word)}(?!\w)", prompt, re.IGNORECASE), f"{clip['clip']}: {word!r}"
        for field in ("purpose", "why"):
            reason = (shot.get(field) or "").strip()
            assert not reason or reason[:40] not in prompt, f"{clip['clip']} carries its {field}"
        assert "because" not in prompt.lower(), f"{clip['clip']} gives a reason"
        people = [identifier for identifier, text in fixed.items() if text]
        if clip["inputs"].get("start_picture"):
            motion_only += 1
            for identifier in people:
                assert fixed[identifier][:50] not in prompt, f"{clip['clip']} repeats a fixed description beside a start picture"
        else:
            in_frame = [subject.split(".")[0] for subject in clip.get("subjects") or []]
            for identifier in in_frame:
                if fixed.get(identifier):
                    assert fixed[identifier].rstrip(".") in prompt, f"{clip['clip']} does not paste {identifier}'s fixed description"
                    with_keys += 1
        assert "The camera does not move." in prompt or "Static" not in prompt, clip["clip"]
    assert motion_only and with_keys, (motion_only, with_keys)
    return f"{len(clips)} prompts: {motion_only} motion only, {with_keys} fixed descriptions pasted word for word"


@group("compile --force-model veo-3.1 gives the colon speaker form without quotation marks, in the syntax-test folders")
def forced_veo(project, story):
    if story is None:
        info("skipped: story not present (the scene 10 excerpt fixture is missing); the spoken lines are unknown")
        return "skip"
    before = sorted(path.name for path in (project / PROMPTS).glob("*.json"))
    code, output = stage(["compile", "--scene", "SC10", "--force-model", "veo-3.1", "--project", project])
    assert code == 0, f"exit {code}\n{output}"
    assert not lint_lines(output, "E"), lint_lines(output, "E")
    notes = lint_lines(output, "N")
    assert all(re.match(r"^N GEN-(02|10)\b", line) for line in notes), notes
    after = sorted(path.name for path in (project / PROMPTS).glob("*.json"))
    assert before == after, f"the syntax test changed the real packs: {before} -> {after}"
    pack = load(project / SYNTAX / "SC10 - veo-3.1.json")
    assert pack["forced"] is True and pack["paid"] is False, (pack["forced"], pack["paid"])
    assert (project / PAGES / "Syntax tests" / "Scene 10 - Saye's kitchen - Veo 3.1.md").is_file()
    shot_170 = next(clip for clip in pack["clips"] if clip["shot"] == "SC10-SH170")
    assert "says: Who are you calling?" in shot_170["prompt"], shot_170["prompt"]
    assert '"Who are you calling?"' not in shot_170["prompt"], shot_170["prompt"]
    spoken = 0
    for clip in pack["clips"]:
        for line in re.findall(r"says: ([^\n]+?[.?!])(?= [A-Z]|$)", clip["prompt"]):
            assert not line.startswith('"'), f"{clip['clip']}: a quoted line after the colon: {line}"
            spoken += 1
    assert spoken >= 5, spoken
    return f"{len(pack['clips'])} Veo clips, {spoken} lines in the colon form; notes only GEN-02 and GEN-10"


@group("a non-held 18-second copy of shot 140 splits on Kling at its planned cutaway")
def split_at_cutaway(workspace, story):
    project = make_gold(workspace / "Split", story)
    path = project / SCENE_FILE
    text = path.read_text(encoding="utf-8")
    start, end = text.index("### SHOT SC10-SH140"), text.index("### SHOT SC10-SH150")
    block = text[start:end]
    changed = block.replace("- screen_time: 7\n", "- screen_time: 18\n")
    changed = re.sub(r"- moment: 3-7 \| shows: ([^\n]+)\n",
                     lambda match: f"- moment: 3-8 | shows: {match.group(1)}\n- moment: 8-18 | shows: after the cutaway "
                                   "to Iona's hands, Saye waits with the leaf held out; Iona takes it\n", changed)
    assert changed != block and "held: no" in changed, "the fixture shot could not be made"
    path.write_text(text[:start] + changed + text[end:], encoding="utf-8")
    code, output = stage(["compile", "--scene", "SC10", "--project", project])
    assert code == 0, f"exit {code}\n{output}"
    assert not lint_lines(output, "E"), lint_lines(output, "E")
    clips = [clip for clip in clips_of(packs_in(project / PROMPTS)) if clip["shot"] == "SC10-SH140"]
    assert [clip["clip"] for clip in clips] == ["SC10-SH140.1", "SC10-SH140.2"], [clip["clip"] for clip in clips]
    assert all(clip["model"] == "kling-3.0-omni" for clip in clips), [clip["model"] for clip in clips]
    assert [clip["covers_s"] for clip in clips] == [[0.0, 8.0], [8.0, 18.0]], [clip["covers_s"] for clip in clips]
    assert [clip["length_s"] for clip in clips] == [10.0, 12.0], [clip["length_s"] for clip in clips]
    assert not any(clip["held"] or clip["chained"] for clip in clips), "the split is chained or held"
    assert clips[1]["inputs"]["start_picture"] == "PIC-SC10-SH140-START-02", clips[1]["inputs"]
    assert not any(re.search(r"cut ?away", clip["prompt"], re.IGNORECASE) for clip in clips), "a cutaway word reached a prompt"
    pictures = load(project / PROMPTS / "SC10 - pictures.json")["pictures"]
    assert any(job["picture"] == "PIC-SC10-SH140-START-02" for job in pictures), "no picture job for clip 2's start"
    assert "split into 2 clips on Kling 3.0 Omni" in output, output
    return "clips of 10 and 12 seconds covering 0-8 and 8-18 seconds, clip 2 from its own start picture"


@group("--lint-only writes nothing; --model writes one model's pack; --storyboard writes the frame prompts")
def options(workspace, story):
    project = make_gold(workspace / "Options", story)
    code, output = stage(["compile", "--scene", "SC10", "--lint-only", "--project", project])
    assert code == 0 and "Lint: 0 errors" in output, f"exit {code}\n{output}"
    assert not (project / PROMPTS).exists() and not (project / PAGES).exists(), "--lint-only wrote files"
    code, output = stage(["compile", "--scene", "SC10", "--model", "seedance-2.5", "--project", project])
    assert code == 0, f"exit {code}\n{output}"
    written = sorted(path.name for path in (project / PROMPTS).glob("*.json"))
    assert written == ["SC10 - pictures.json", "SC10 - seedance-2.5.json"], written
    code, output = stage(["compile", "--scene", "SC10", "--storyboard", "--project", project])
    assert code == 0, f"exit {code}\n{output}"
    page = (project / "18 Storyboard" / "Scene 10 - frame prompts.md").read_text(encoding="utf-8")
    frames = page.count("\n## Shot ")
    assert frames >= 1 and "at at " not in page, page[:500]
    assert not IDENTIFIER.findall(page.split("## For the records")[0]), "a record ID in the frame prompts"
    code, output = stage(["compile", "--scene", "SC10", "--force-model", "no-such-model", "--project", project])
    assert code == 2 and "not in the model facts" in output, f"exit {code}\n{output}"
    return f"lint only: nothing written; one pack for Seedance 2.5; {frames} storyboard frames; an unknown model stops with exit 2"


@group("the pages the user reads carry no research codes or email addresses")
def plain_pages(project):
    codes = re.compile(r"\((?:[A-D]\d{1,2}|K\d{1,2})\b|\bC\d §|\bRule \d+\)|\b(?:GEN|WORDS)-\d{2}\b")
    for page in sorted((project / PAGES).rglob("*.md")):
        text = page.read_text(encoding="utf-8")
        outside = re.sub(r"```text\n.*?```", "", text, flags=re.DOTALL)
        found = codes.findall(outside)
        assert not found, f"{page.name}: {found[:5]}"
        assert not EMAIL.findall(text), f"{page.name} holds an email address"
    return "every page in 20 Prompts for AI video is in plain words"


# ---------------------------------------------------------------- graphics

@group("graphics draws the title card (never mirrored) and a sign, normal and mirrored")
def graphics(workspace, story):
    project = make_gold(workspace / "Graphics", story)
    things = project / "08 Places and things.md"
    text = things.read_text(encoding="utf-8")
    record = ("### TEXT TX-GOODS-ONLY The goods sign\n- kind: sign\n- words: Goods only. No persons.\n- on: none\n"
              "- origin: story\n- reader: CH-IONA\n- plot_critical: yes\n- emphasis: 2\n- method: composite\n"
              "- animation: none\n- status: approved\n\n")
    match = re.search(r"END OF FILE \| (.+?) \| (\d+) records", text)
    assert match, "the places and things file has no end line"
    text = text[:match.start()] + record + f"END OF FILE | {match.group(1)} | {int(match.group(2)) + 1} records" + text[match.end():]
    things.write_text(text, encoding="utf-8")
    scene = project / SCENE_FILE
    scene_text = scene.read_text(encoding="utf-8")
    start = scene_text.index("### SHOT SC10-SH110")
    scene_text = scene_text[:start] + scene_text[start:].replace("- text: none\n", "- text: TX-GOODS-ONLY\n", 1)
    scene.write_text(scene_text, encoding="utf-8")
    code, output = stage(["graphics", "--project", project, "--no-png"])
    assert code in (0, 1), f"exit {code}\n{output}"
    folder = project / PAGES / "Text graphics"
    names = sorted(path.name for path in folder.glob("*.svg"))
    assert names == ["The goods sign - mirrored.svg", "The goods sign.svg", "The title card.svg"], names
    title = ElementTree.parse(folder / "The title card.svg").getroot()
    namespace = "{http://www.w3.org/2000/svg}"
    assert title.get("width") == "1920" and title.get("height") == "804", (title.get("width"), title.get("height"))
    rect = title.find(f"{namespace}rect")
    words = title.find(f"{namespace}text")
    assert rect is not None and rect.get("fill") == "#000000", "the title card is not on black"
    assert words.text == "THE CATCH" and words.get("font-size") == "69" and words.get("fill") == "#EDEBE6", \
        (words.text, words.get("font-size"), words.get("fill"))
    assert words.get("font-family") == "IBM Plex Sans" and words.get("font-weight") == "500"
    assert abs(float(words.get("y")) - 410) <= 1 and abs(float(words.get("letter-spacing")) - 5.5) <= 0.1, \
        (words.get("y"), words.get("letter-spacing"))
    mirrored = ElementTree.parse(folder / "The goods sign - mirrored.svg").getroot()
    wrapper = mirrored.find(f"{namespace}g")
    assert wrapper is not None and wrapper.get("transform") == "translate(1920,0) scale(-1,1)", \
        wrapper.get("transform") if wrapper is not None else "no wrapper"
    normal = ElementTree.parse(folder / "The goods sign.svg").getroot()
    assert normal.find(f"{namespace}g") is None and normal.find(f"{namespace}rect") is None, "the sign is not transparent"
    sign = normal.find(f"{namespace}text")
    cap = round(0.05 * 804)
    assert int(sign.get("font-size")) == round(cap / 0.698), sign.get("font-size")
    page = (folder / "Text graphics.md").read_text(encoding="utf-8")
    assert "Reading time: 4 seconds; 8 seconds when it reads mirrored." in page, page
    assert "shot 110" in page and "Never mirrored" in page, page
    too_short = "too short" in page
    assert (code == 1) == too_short, f"exit {code} while the page says too short: {too_short}"
    return f"3 SVG files, the title card at 69 pixels on black, the sign {'too short in shot 110' if too_short else 'readable in shot 110'} (exit {code})"


# ---------------------------------------------------------------- refresh-models

@group("refresh-models checks, proposes and applies on a copy, and waits for the user's approval of a price change")
def refresh(workspace):
    folder = workspace / "adapters"
    shutil.copytree(ADAPTERS, folder)
    code, output = stage(["refresh-models", "--check", "--adapters", folder])
    assert code == 0 and "the model facts are in order" in output, f"exit {code}\n{output}"
    today = datetime.date.today().isoformat()
    findings = workspace / "findings.json"
    findings.write_text(json.dumps({"checked_on": today, "changes": [
        {"file": "video_models.json", "path": "models/kling-3.0/price_usd_per_s/audio", "value": 0.18, "mark": "V",
         "source": "https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video"},
        {"file": "video_models.json", "path": "models/wan-3.0/status", "value": "current", "mark": "V",
         "source": "https://fal.ai/wan-3"},
        {"file": "video_models.json", "path": "models/seedance-2.5/length_s/max", "value": 20, "mark": "V",
         "source": "https://example.org/seedance-2.5"}]}), encoding="utf-8")
    before = (folder / "video_models.json").read_bytes()
    code, output = stage(["refresh-models", "--propose", findings, "--adapters", folder])
    assert code == 0 and "1 of them change a price" in output, f"exit {code}\n{output}"
    proposal = load(folder / "proposal" / "proposal.json")
    assert len(proposal["price_changes"]) == 1 and proposal["shape_ok"], proposal["price_changes"]
    assert (folder / "video_models.json").read_bytes() == before, "--propose changed the model facts"
    code, output = stage(["refresh-models", "--apply", "--adapters", folder])
    assert code == 1 and "waits for the user's approval" in output, f"exit {code}\n{output}"
    assert (folder / "video_models.json").read_bytes() == before, "a price change was applied without approval"
    code, output = stage(["refresh-models", "--apply", "--prices-approved", "--adapters", folder])
    assert code == 0, f"exit {code}\n{output}"
    video = load(folder / "video_models.json")
    assert video["checked_on"] == today, video["checked_on"]
    assert video["models"]["kling-3.0"]["price_usd_per_s"]["audio"] == 0.18
    assert video["models"]["kling-3.0"]["marks"]["price_usd_per_s"].startswith("V https://fal.ai"), \
        video["models"]["kling-3.0"]["marks"]["price_usd_per_s"]
    assert video["models"]["seedance-2.5"]["length_s"]["max"] == 20
    assert (folder / "previous" / FACTS_DATE / "video_models.json").read_bytes() == before, "the old file was not kept"
    assert not (folder / "proposal").exists(), "the applied proposal was left behind"
    bad = workspace / "bad findings.json"
    bad.write_text(json.dumps({"checked_on": today, "changes": [
        {"file": "video_models.json", "path": "models/veo-3.1/price_usd_per_s/1080p", "value": -1, "mark": "V",
         "source": "https://ai.google.dev/gemini-api/docs/pricing"},
        {"file": "video_models.json", "path": "models/veo-3.1/speaker", "value": "{who} says", "mark": "V"}]}),
        encoding="utf-8")
    code, output = stage(["refresh-models", "--propose", bad, "--adapters", folder])
    assert code == 1 and "below zero" in output and "has no {line}" in output and "needs the page" in output, output
    code, output = stage(["refresh-models", "--apply", "--prices-approved", "--adapters", folder])
    assert code == 1 and "has problems" in output, f"exit {code}\n{output}"
    source = (TOOLS / "stage_tools" / "refresh_models.py").read_text(encoding="utf-8")
    assert not re.search(r"^\s*(?:import|from)\s+(?:urllib|http|socket|ssl)\b", source, re.MULTILINE), \
        "refresh_models.py imports a web library"
    return "check, propose, apply held back by a price change, apply with approval, old files kept, bad findings refused"


# ---------------------------------------------------------------- the whole story, when given

@group("compile with --story on the whole story")
def whole_story(workspace, whole):
    if whole is None:
        return "skip"
    project = make_gold(workspace / "Whole", EXCERPT if EXCERPT.is_file() else None)
    code, output = stage(["compile", "--scene", "SC10", "--story", whole, "--project", project])
    assert code == 0 and "Lint: 0 errors" in output, f"exit {code}\n{output}"
    return "exit 0, 0 GEN errors"


# ---------------------------------------------------------------- running it

def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--story", help="the whole story (The Catch); the scene 10 excerpt fixture is used when present")
    arguments = parser.parse_args()
    whole = Path(arguments.story) if arguments.story else None
    if whole is not None and not whole.is_file():
        info(f"skipped: story not present ({whole.name}); the whole-story group is skipped")
        whole = None
    story = EXCERPT if EXCERPT.is_file() else None
    if story is None:
        info("skipped: story not present (the scene 10 excerpt fixture is missing); speech-dependent checks are skipped")
    if not fresh():
        info(f"the model facts are {facts_age()} days old, over the limit: prices are expected to be missing")
    workspace = Path(tempfile.mkdtemp(prefix="wp8 "))
    try:
        adapter_files()
        project = make_gold(workspace / "The Catch", story)
        code, output = stage(["compile", "--scene", "SC10", "--project", project])
        compile_gold(project, output, code)
        checker_after_compile(project)
        shot_150(project, output)
        prompt_contents(project)
        plain_pages(project)
        forced_veo(project, story)
        split_at_cutaway(workspace, story)
        options(workspace, story)
        graphics(workspace, story)
        refresh(workspace)
        whole_story(workspace, whole)
    finally:
        shutil.rmtree(workspace, ignore_errors=True)
    failing = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({failing} failing groups)")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
