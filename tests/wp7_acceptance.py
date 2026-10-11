"""wp7_acceptance.py: the acceptance test of work package 7, the estimate (blueprint 14.2 row "WP7 Estimate").

It checks, in plain groups:
- the dated price table _config/adapters/prices.json (date 2026-09-27, a page or a research file for every price, D13's shape);
- the estimator against D13's own worked figures (Recipe 0 and rule R25: scene 6 from its 36 shots gives 1,250
  generated seconds, $78 / $157 / $377 and 14.0 base hours; scene 6 from its words; the 15-minute plan's scene);
- the first estimate of The Catch through stage.py new, read and estimate: between 1,926 and 2,309 seconds of
  story with the central figure about 2,118 (test T1), its files, the planned figures it stores, and a clean step 1
  check (skipped when the story is not given);
- money kept out of every file and message when the prices are over 30 days old (a fake date), shown again at
  exactly 30 days, and never shown without a dated table;
- the estimate from the shots on the gold scene 10 and through the command on a project adopt made from the
  chat-saved scene 10 (check --all still exits 0 afterwards);
- the planned figures on a small invented screenplay (PLAN runtime_estimate, scene_budget, shot_budget; a locked
  record keeps its values; a shorter runtime target scales the scenes), a shot list, a partial scope and a model's
  allowed clip lengths;
- a prose project: a rough runtime only at step 1, then the macro plans side by side;
- plain words: the checker's own WORDS-02 and WORDS-04 helpers find nothing on any page made here.

Usage: python tests/wp7_acceptance.py [<The Catch>] [<The Long Places>] [--story <The Catch>] [--keep]
Standard library only. Temporary projects are made outside the repository and removed unless --keep is given.
"""

import contextlib
import datetime
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parent.parent
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
TOOLS = SKILL / "tools"
STAGE = TOOLS / "stage.py"
FIXTURES = REPOSITORY / "tests" / "fixtures"
EXCERPT = FIXTURES / "The Catch - lines 397-489.txt"
CHAT_SAVED = FIXTURES / "chat saved scene 10"
NIGHT_SHIFT = FIXTURES / "reader" / "Night shift - Catch layout.txt"
LAMP_KEEPER = FIXTURES / "reader" / "The lamp keeper - chapters.md"
GOLD = [SKILL / "references" / "examples" / "01 The Catch - scene 10.md", SKILL / "references" / "examples" / "02 The Catch - scene 10 - context.md"]

sys.path.insert(0, str(TOOLS))

from stage_tools import estimate  # noqa: E402
from stage_tools.derive_fields import Breakdown  # noqa: E402
from stage_tools.record_format import load_skill_data, parse_file, write_file  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
RESULTS = []
PAGES = {}


def report(passed, name, detail=""):
    """passed True (PASS), False (FAIL) or None (INFO, skipped)."""
    word = "PASS" if passed else ("INFO" if passed is None else "FAIL")
    RESULTS.append((word, name))
    line = f"{word}  {name}"
    if detail:
        line += f": {detail}"
    print(line, flush=True)


def expect(problems, what, found, wanted):
    if found != wanted:
        problems.append(f"{what}: found {found!r}, wanted {wanted!r}")


def near(problems, what, found, wanted, tolerance):
    if found is None or abs(found - wanted) > tolerance:
        problems.append(f"{what}: found {found!r}, wanted {wanted} within {tolerance}")


def shorten(problems, limit=6):
    text = "; ".join(problems[:limit])
    return text + (f"; and {len(problems) - limit} more" if len(problems) > limit else "")


def run_stage(arguments, folder, timeout=600):
    environment = dict(os.environ, STAGE_LOCK_WAIT_SECONDS="2")
    result = subprocess.run([sys.executable, str(STAGE)] + arguments, cwd=folder, capture_output=True, text=True,
                            env=environment, timeout=timeout)
    return result.returncode, result.stdout + result.stderr


def run_stage_in_process(arguments, on_date):
    """stage.py run in this process with a fake date for the estimate (the stale-prices tests)."""
    import stage
    estimate.use_today(on_date)
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            code = stage.main(list(arguments))
    finally:
        estimate.use_today(None)
    return code, output.getvalue()


def make_project(story, parent):
    parent.mkdir(parents=True, exist_ok=True)
    code, output = run_stage(["new", str(story), "--into", str(parent)], parent)
    if code != 0:
        return None, f"new exited {code}: {output.strip()}"
    folder = next((path for path in sorted(parent.iterdir()) if (path / "00 Start here.md").is_file()), None)
    return folder, output


def prices():
    table, reason = estimate.PriceTable.load()
    if table is None:
        raise RuntimeError(reason)
    return table


def estimate_json(folder):
    return json.loads((folder / "For machines - do not edit" / "estimate.json").read_text(encoding="utf-8"))


def money_found(text):
    return re.findall(r"\$\s?\d", text)


def json_money_keys(data):
    """Every key anywhere in the estimate JSON that holds money."""
    found = []

    def walk(value, path):
        if isinstance(value, dict):
            for key, inner in value.items():
                if key in ("money_usd", "by_price_level", "spent_usd", "subscriptions") or key.endswith("_usd"):
                    found.append(path + key)
                walk(inner, path + key + ".")
        elif isinstance(value, list):
            for index, inner in enumerate(value):
                walk(inner, f"{path}{index}.")
    walk(data, "")
    return found


def record_value(folder, file_name, type_name, identifier, field):
    record_file = parse_file(folder / file_name, file_name, SCHEMA)
    for record in record_file.records:
        if record.type_name == type_name and (identifier is None or record.identifier == identifier):
            return record.get(field)
    return None


def set_field(folder, file_name, type_name, identifier, field, value):
    path = folder / file_name
    record_file = parse_file(path, file_name, SCHEMA)
    for record in record_file.records:
        if record.type_name == type_name and (identifier is None or record.identifier == identifier):
            record.set_field(field, value, SCHEMA)
    write_file(record_file, path, SCHEMA)


# ---------------------------------------------------------------- group 1: the price table

def group_price_table():
    problems = []
    path = SKILL / "_config" / "adapters" / "prices.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    expect(problems, "price_date", data.get("price_date"), "2026-09-27")
    video = data.get("video", {})
    for level, wanted in (("draft", 0.05), ("budget", 0.07), ("mid", 0.17), ("premium", 0.45)):
        expect(problems, f"video {level} per second", video.get(level, {}).get("per_s"), wanted)
    expect(problems, "shortest clip", video.get("min_clip_s"), 5)
    image = data.get("image", {})
    expect(problems, "storyboard try", image.get("storyboard_try"), 0.0168)
    expect(problems, "start picture per shot", image.get("start_picture_per_shot"), 0.55)
    upscale = data.get("upscale", {})
    expect(problems, "upscale to 1080p", upscale.get("to_1080p_per_s"), 0.02)
    expect(problems, "upscale above 1080p", upscale.get("above_1080p_per_s"), 0.08)
    plans = data.get("plans", {})
    for name, wanted in (("claude_pro", 20), ("claude_max", 100), ("elevenlabs_starter", 6),
                         ("elevenlabs_creator", 22), ("elevenlabs_pro", 99), ("suno_pro", 8), ("suno_premier", 24)):
        expect(problems, f"plan {name}", plans.get(name, {}).get("per_month"), wanted)
    expect(problems, "Resolve Studio", plans.get("resolve_studio_once", {}).get("once"), 295)
    expect(problems, "ElevenLabs music", data.get("licence_flags", {}).get("elevenlabs_music"),
           "no_film_use_on_self_serve")
    classes = data.get("work_defaults", {}).get("cost_classes", {})
    for name, takes in (("graphic", (0, 0)), ("reuse", (0, 0)), ("still_move", (0, 0)), ("easy", (2, 3)),
                        ("dialogue", (2, 4)), ("hard", (4, 7))):
        expect(problems, f"takes of {name}", (classes.get(name, {}).get("draft_takes"),
                                              classes.get(name, {}).get("final_takes")), takes)
    # every price has a page or a research source
    for section in ("video", "plans"):
        for name, entry in data.get(section, {}).items():
            if isinstance(entry, dict) and ("per_s" in entry or "per_month" in entry or "once" in entry):
                if not (entry.get("url") or entry.get("source")):
                    problems.append(f"{section} {name} has no page or source")
    for section in ("image", "upscale", "credits"):
        entry = data.get(section, {})
        if not any(key in entry for key in ("url", "urls", "source", "storyboard_source")):
            problems.append(f"{section} has no page or source")
    text = path.read_text(encoding="utf-8")
    if re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text):
        problems.append("an email address in the price table")
    if re.search(r"keyframe|bible", text):
        problems.append("a retired word (keyframe, bible) in the price table's keys")
    report(not problems, "the price table _config/adapters/prices.json: dated 2026-09-27, D13's prices, plans, takes and "
           "licence flags, a page or source for every price", shorten(problems))


# ---------------------------------------------------------------- group 2: D13's worked figures (Recipe 0)

def scene_six_works():
    work = estimate.ShotWork
    works = [work("graphic", "graphic", 0.4, [5])] + [work(f"reuse {n}", "reuse", 1.4, [5]) for n in range(3)]
    works += [work(f"easy {n}", "easy", 1.4, [5]) for n in range(15)] + [work("final hold", "easy", 5.0, [7])]
    works += [work(f"dialogue {n}", "dialogue", 1.4, [5]) for n in range(2)]
    works += [work(f"hard {n}", "hard", 1.4, [5]) for n in range(14)]
    works[4].plates = 1
    works[5].plates = 1
    return works


def group_recipe_zero():
    table = prices()
    problems = []
    block = estimate.scene_block("SC06", "scene 6", scene_six_works(), (49.7, 49.7, 49.7), table,
                                 extra_previs_minutes=120)
    expect(problems, "shots", round(block.total_shots), 36)
    expect(problems, "draft seconds", round(block.draft_s), 464)
    expect(problems, "final seconds", round(block.final_s), 786)
    expect(problems, "generated seconds", round(block.generated_s), 1250)
    expect(problems, "money budget / mid / premium", tuple(round(block.video_money[level]) for level in
                                                          ("budget", "mid", "premium")), (78, 157, 377))
    expect(problems, "base hours", round(block.base_minutes / 60.0, 1), 14.0)
    expect(problems, "pictures", round(block.pictures_money), 19)
    report(not problems, "D13 Recipe 0 (rule R25): scene 6's fall from its 36 shots gives 1,250 generated seconds, "
           "$78 / $157 / $377 and 14.0 base hours", shorten(problems))

    problems = []
    counts = {"dialogue_words": 10, "speeches": 5, "beat_marks": 0, "action_words": 513}
    seconds = estimate.seconds_from_words(counts, CONSTANTS)
    expect(problems, "seconds low / central / high", tuple(round(value) for value in seconds), (92, 106, 119))
    scene = estimate.SceneInput("SC06", "scene 6", "action_peak", True, 1.0, True, False, counts=counts)
    block = estimate.scene_block_from_words(scene, CONSTANTS, table, 0.75, True)
    near(problems, "shots", block.total_shots, 53, 1)
    near(problems, "generated seconds", block.generated_s, 2512, 2512 * 0.01)
    for level, wanted in (("budget", 158), ("mid", 318), ("premium", 768)):
        near(problems, f"video money {level}", block.video_money[level], wanted, wanted * 0.01)
    near(problems, "base hours", block.base_minutes / 60.0, 36, 1)
    report(not problems, "D13 §15.1 scene 6 from its words: 92 to 119 seconds, about 53 shots, 2,512 generated "
           "seconds and $158 / $318 / $768 (within 1%; D13 rounded the seconds first)", shorten(problems))

    problems = []
    handles = float(estimate.constant(CONSTANTS, "handles_s", 0.75))
    clip = estimate.clip_length_for
    shots = [("easy", 7), ("easy", 6), ("graphic", 4), ("hard", 5), ("easy", 6), ("hard", 5), ("easy", 12),
             ("hard", 5), ("easy", 6), ("easy", 8), ("easy", 5), ("still_move", 11)]
    works = []
    for number, (cost_class, seconds) in enumerate(shots, 1):
        works.append(estimate.ShotWork(f"shot {number}", cost_class, seconds, [clip(seconds, table, handles)],
                                       plates=1 if cost_class == "graphic" else 0,
                                       previs_minutes=20 if number == 8 else 0))
    expect(problems, "easy clips", [work.clip_length_s for work in works if work.cost_class == "easy"],
           [9.0, 8.0, 8.0, 14.0, 8.0, 10.0, 7.0])
    expect(problems, "hard clips", [work.clip_length_s for work in works if work.cost_class == "hard"], [7.0] * 3)
    block = estimate.scene_block("plan C 03", "the mouth at night", works, (80, 80, 80), table)
    expect(problems, "generated seconds", (round(block.draft_s), round(block.final_s)), (212, 345))
    expect(problems, "money", tuple(round(block.video_money[level]) for level in ("budget", "mid", "premium")),
           (35, 69, 166))
    near(problems, "base hours", block.base_minutes / 60.0, 9.0, 0.1)
    report(not problems, "D13 §15.4 a 12-shot scene: clips by the rule of §6.2 (screen time plus the handles, "
           "rounded up, never under 5), 557 generated seconds, $35 / $69 / $166, 9 base hours", shorten(problems))


# ---------------------------------------------------------------- group 3: The Catch, the first estimate (T1)

def group_the_catch(story, work):
    if story is None:
        report(None, "T1 The Catch: the first estimate between 1,926 and 2,309 seconds", "skipped: story not present")
        return
    problems = []
    folder, output = make_project(story, work / "catch")
    if folder is None:
        report(False, "T1 The Catch: the first estimate", output)
        return
    code, output = run_stage(["read"], folder)
    expect(problems, "read exit", code, 0)
    if not (folder / "14 Time and cost.md").is_file():
        problems.append("read did not write 14 Time and cost.md")
    code, output = run_stage(["estimate", "--version", "v0"], folder)
    expect(problems, "estimate exit", code, 0)
    data = estimate_json(folder)["estimate"]
    story_seconds = data["story_runtime_s"]
    low, central, high = story_seconds["low"], story_seconds["central"], story_seconds["high"]
    if not (1926 <= round(low) and round(high) <= 2309 and round(low) == 1926 and round(high) == 2309):
        problems.append(f"story seconds {low} to {high}, wanted 1,926 to 2,309")
    near(problems, "central seconds", central, 2118, 1)
    expect(problems, "version", data["version"], "v0_words")
    expect(problems, "titles and credits of a short", data["titles_and_credits_s"], 60.0)
    near(problems, "runtime with titles", data["runtime_s"]["central"], 2178, 1)
    page = (folder / "14 Time and cost.md").read_text(encoding="utf-8")
    PAGES["The Catch, the first estimate"] = page
    # changed after the full run (Project notes 32, problem 18): one film length, the story's, then the same with
    # titles and credits added
    for wanted in ("1,926", "2,118", "2,309", "In short: the film runs about 35 minutes (32 to 38) of story, 36 minutes "
                   "(33 to 39) with titles and credits"):
        if wanted not in page:
            problems.append(f"14 Time and cost does not say {wanted!r}")
    if "first estimate" not in output:
        problems.append("the command's report does not name the first estimate")
    targets = [record_value(folder, "04 Scene list.md", "SCENE", f"SC{number:02d}", "target_duration_s")
               for number in range(1, 31)]
    if any(value is None for value in targets):
        problems.append(f"target_duration_s missing on {sum(value is None for value in targets)} scenes")
    else:
        near(problems, "the scenes' planned lengths added up", sum(float(value) for value in targets), 2118, 15)
        expect(problems, "scene 10's planned length", targets[9], "91")
    expect(problems, "PROJECT model_facts_date", record_value(folder, "00 Start here.md", "PROJECT", None,
                                                              "model_facts_date"), "2026-09-27")
    code, output = run_stage(["check", "--step", "1"], folder)
    expect(problems, "check --step 1 exit", code, 0)
    report(not problems, "T1 The Catch: new, read and estimate give the first estimate of 1,926 to 2,309 seconds of "
           "story, central 2,118 (2,178 with titles), written to 14 Time and cost and estimate.json; each scene's "
           "planned length stored; check --step 1 exits 0", shorten(problems))

    # the same project, prices over 30 days old
    problems = []
    price_date = prices().date
    code, output = run_stage_in_process(["estimate", "--version", "v0", "--project", str(folder)],
                                        price_date + datetime.timedelta(days=31))
    expect(problems, "exit", code, 0)
    page = (folder / "14 Time and cost.md").read_text(encoding="utf-8")
    PAGES["The Catch, stale prices"] = page
    data = estimate_json(folder)
    if money_found(page):
        problems.append(f"money on the page: {money_found(page)[:3]}")
    if money_found(output):
        problems.append(f"money in the report: {money_found(output)[:3]}")
    if json_money_keys(data):
        problems.append(f"money in estimate.json: {json_money_keys(data)[:3]}")
    expect(problems, "money_shown", data["estimate"]["money_shown"], False)
    if "31 days ago" not in page or "older than 30 days" not in page:
        problems.append("the page does not say why the money is not shown")
    near(problems, "runtime still shown", data["estimate"]["story_runtime_s"]["central"], 2118, 1)
    report(not problems, "The Catch with prices 31 days old (a fake date): no money on the page, in the report or in "
           "estimate.json, the reason given, runtime and hours still shown", shorten(problems))


# ---------------------------------------------------------------- group 4: stale prices, without the story

def excerpt_breakdown():
    return Breakdown.from_paths(GOLD, story_path=EXCERPT if EXCERPT.is_file() else None)


def group_stale_prices():
    table = prices()
    problems = []
    breakdown = excerpt_breakdown()
    days = int(estimate.constant(CONSTANTS, "model_facts_max_age_days", 30))
    for offset, shown in ((0, True), (days, True), (days + 1, False), (120, False)):
        film = estimate.film_estimate(breakdown, "v1", on=table.date + datetime.timedelta(days=offset), prices=table)
        page = estimate.render_time_and_cost(film, table)
        data = estimate.estimate_as_json(film)
        if film.money_shown != shown:
            problems.append(f"{offset} days old: money shown {film.money_shown}, wanted {shown}")
        if shown and not money_found(page):
            problems.append(f"{offset} days old: no money on the page")
        if not shown and (money_found(page) or json_money_keys(data)):
            problems.append(f"{offset} days old: money still on the page or in the file")
        if offset == days + 1:
            PAGES["the gold scene, stale prices"] = page
    undated = estimate.PriceTable({key: value for key, value in table.data.items()
                                   if key not in ("price_date", "checked_on")})
    film = estimate.film_estimate(breakdown, "v1", prices=undated)
    if film.money_shown or money_found(estimate.render_time_and_cost(film, undated)):
        problems.append("a price table with no date still shows money")
    estimate.use_today(table.date + datetime.timedelta(days=days + 1))
    try:
        film = estimate.film_estimate(breakdown, "v1", prices=table)
    finally:
        estimate.use_today(None)
    if film.money_shown:
        problems.append("use_today (the fake date) did not reach film_estimate")
    report(not problems, f"money is shown at 0 and {days} days and never after (D13 R7, E11), nor without a dated "
           "table; the fake date reaches the estimate", shorten(problems))


# ---------------------------------------------------------------- group 5: the estimate from the shots

def group_from_the_shots(work):
    table = prices()
    problems = []
    breakdown = excerpt_breakdown()
    film = estimate.film_estimate(breakdown, None, prices=table)
    expect(problems, "version chosen", film.version, "v1")
    shots = breakdown.shots_of("SC10")
    total = sum(float(shot.get("screen_time") or 0) for shot in shots)
    block = film.scenes[0] if film.scenes else None
    if block is None:
        problems.append("no scene block")
    else:
        expect(problems, "basis", block.basis, "shots")
        expect(problems, "shots", round(block.total_shots), len(shots))
        near(problems, "scene seconds", block.runtime_s[1], total, 0.01)
        classes = {}
        for shot in shots:
            classes[shot.get("cost_class")] = classes.get(shot.get("cost_class"), 0) + 1
        expect(problems, "shots by class", {name: round(value) for name, value in block.shots.items() if value},
               classes)
        if "mixed" not in (block.video_money or {}):
            problems.append("no mixed plan column")
    works, _, _ = estimate.works_from_shots(breakdown, estimate.scene_inputs(breakdown, table, {})[0], shots, table,
                                           0.75, 4.5, set())
    turn = next((item for item in works if item.identifier == "SC10-SH150"), None)
    expect(problems, "shot 150's clip", turn.clip_length_s if turn else None, 17.0)
    if "shot 150 of scene 10" not in film.example:
        problems.append(f"the example is not the turn shot: {film.example[:80]}")
    page = estimate.render_time_and_cost(film, table)
    PAGES["the gold scene, from the shots"] = page
    for wanted in ("the estimate from the shots", "Mixed plan", "scene 10, Saye's house - kitchen"):
        if wanted not in page:
            problems.append(f"the page does not say {wanted!r}")
    # a model's allowed lengths: 4, 6 or 8 seconds; a shot longer than the model holds
    breakdown.models = {"veo-3.1": {"aliases": ["Veo 3.1"], "length_s": {"allowed": [4, 6, 8]}},
                        "kling-3.0-omni": {"aliases": ["Kling O3"], "length_s": {"min": 3, "max": 15, "step": 1}}}
    for identifier, model, wanted in (("SC10-SH010", "Veo 3.1", None), ("SC10-SH150", "Kling O3", 17.0)):
        shot = breakdown.record(identifier, "SHOT")
        original = shot.get("model")
        shot.set_field("model", f"{model} | why: a test", SCHEMA)
        lengths, note = estimate.shot_clip_lengths(breakdown, shot, float(shot.get("screen_time")), table, 0.75)
        if wanted is None:
            needed = float(shot.get("screen_time")) + 1.5
            allowed = [value for value in (4, 6, 8) if value >= needed]
            expect(problems, f"{identifier} on Veo", lengths, [float(allowed[0])] if allowed else lengths)
            if allowed and note:
                problems.append(f"{identifier}: an unexpected note {note}")
        else:
            expect(problems, f"{identifier} on Kling, too long for it", lengths, [wanted])
            if "longer than" not in note:
                problems.append(f"{identifier}: no note that the model cannot hold it")
        if original is None:
            shot.remove_field("model")
        else:
            shot.set_field("model", original, SCHEMA)
    report(not problems, "the estimate from the shots on the gold scene 10: every shot's screen time and cost "
           "class, shot 150's 17-second clip, the mixed plan, a model's allowed lengths (4, 6 or 8 seconds) and a "
           "held shot too long for its model", shorten(problems))

    # through the command, on a project adopt made from the chat-saved scene 10
    if not EXCERPT.is_file() or not CHAT_SAVED.is_dir():
        report(None, "the estimate command on an adopted project", "skipped: story not present")
        return
    problems = []
    parent = work / "adopted"
    parent.mkdir(parents=True)
    folder = parent / "The Catch - breakdown"
    shutil.copytree(CHAT_SAVED, folder)
    code, output = run_stage(["adopt", str(folder), str(EXCERPT)], parent)
    if code != 0:
        problems.append(f"adopt exited {code}")
    if (folder / "14 Time and cost.md").is_file():
        problems.append("read wrote a first estimate into a folder that already holds scenes")
    code, output = run_stage(["estimate"], folder)
    expect(problems, "estimate exit", code, 0)
    if "The estimate from the shots" not in output:
        problems.append(f"the report does not name the estimate from the shots: {output[:120]}")
    data = estimate_json(folder)
    expect(problems, "version", data["estimate"]["version"], "v1_shot_list")
    expect(problems, "model_facts_date", record_value(folder, "00 Start here.md", "PROJECT", None,
                                                      "model_facts_date"), "2026-09-27")
    PAGES["the adopted scene, from the shots"] = (folder / "14 Time and cost.md").read_text(encoding="utf-8")
    code, output = run_stage(["check", "--all"], folder)
    expect(problems, "check --all exit after the estimate", code, 0)
    report(not problems, "stage.py estimate on a project adopt made from the chat-saved scene 10: the estimate from "
           "the shots, the model facts date stored, and check --all still exits 0", shorten(problems))


# ---------------------------------------------------------------- group 6: planned figures, lists, scope

PLAN_FILE = """# Story plan

## At a glance

The plan of a small invented film, for the estimate test.

Below this line: details for the AI and the checker. You never need to read them.

### PLAN
- logline: A baker and her nephew find a key and keep the night shift going.
- status: draft
- locked: no

END OF FILE | Story plan | 1 records
"""

SHOT_LIST = """# Scene 1 - Back room

## At a glance

A shot list for the estimate test.

Below this line: details for the AI and the checker. You never need to read them.

### SHOTLIST SC01-LIST
- item: SC01-SH010 | beats: SC01-B01 | role: normal | size: wide | frame: two_shot | subject: CH-MARA | time: 6 | shows: Mara at the oven
- item: SC01-SH020 | beats: SC01-B02 | role: turn | size: close_up | frame: single | subject: CH-OSKAR | time: 9 | shows: the key
- approved: no
- status: draft
- locked: no

END OF FILE | Scene 1 shot list | 1 records
"""


def group_planned_figures(work):
    problems = []
    folder, output = make_project(NIGHT_SHIFT, work / "night")
    if folder is None:
        report(False, "planned figures on an invented screenplay", output)
        return
    code, output = run_stage(["read"], folder)
    expect(problems, "read exit", code, 0)
    (folder / "05 Story plan.md").write_text(PLAN_FILE, encoding="utf-8")
    set_field(folder, "04 Scene list.md", "SCENE", "SC01", "rhythm_class", "dialogue")
    set_field(folder, "04 Scene list.md", "SCENE", "SC02", "rhythm_class", "suspense")
    code, output = run_stage(["estimate", "--version", "v0"], folder)
    expect(problems, "estimate exit", code, 0)
    data = estimate_json(folder)["estimate"]
    central = data["story_runtime_s"]["central"]
    near(problems, "PLAN runtime_estimate", float(record_value(folder, "05 Story plan.md", "PLAN", None,
                                                               "runtime_estimate") or 0),
         data["as_written_s"]["central"], 0.5)
    scenes = len(estimate_json(folder)["scenes"])
    expect(problems, "PLAN scene_budget", record_value(folder, "05 Story plan.md", "PLAN", None, "scene_budget"),
           str(scenes))
    expect(problems, "PLAN shot_budget", record_value(folder, "05 Story plan.md", "PLAN", None, "shot_budget"),
           str(int(round(data["shots"]["total"]))))
    blocks = {block["scene"]: block for block in estimate_json(folder)["scenes"]}
    expect(problems, "scene 1 pace", blocks.get("SC01", {}).get("rhythm_class"), "dialogue")
    near(problems, "scene 1 average shot", blocks.get("SC01", {}).get("average_shot_s"),
         float(estimate.constant(CONSTANTS, "rhythm_class_asl_s")["dialogue"]), 0.01)
    # a locked record keeps its values
    set_field(folder, "05 Story plan.md", "PLAN", None, "locked", "yes")
    before = record_value(folder, "05 Story plan.md", "PLAN", None, "shot_budget")
    set_field(folder, "04 Scene list.md", "SCENE", "SC01", "rhythm_class", "action_peak")
    code, output = run_stage(["estimate", "--version", "v0"], folder)
    expect(problems, "shot_budget on the locked PLAN", record_value(folder, "05 Story plan.md", "PLAN", None,
                                                                    "shot_budget"), before)
    if "unchanged" not in output:
        problems.append("the report does not say the locked values were kept")
    if estimate_json(folder)["estimate"]["shots"]["total"] == data["shots"]["total"]:
        problems.append("the estimate did not change with the pace class")
    # a shorter runtime target scales the kept scenes (titles and credits come on top)
    set_field(folder, "05 Story plan.md", "PLAN", None, "locked", "no")
    target = round(central * 0.5 + 60)
    set_field(folder, "00 Start here.md", "PROJECT", None, "runtime_target_s", str(target))
    code, output = run_stage(["estimate", "--version", "v0"], folder)
    data = estimate_json(folder)["estimate"]
    near(problems, "runtime at the target", data["runtime_s"]["central"], target, 1)
    stored = [record_value(folder, "04 Scene list.md", "SCENE", block["scene"], "target_duration_s")
              for block in estimate_json(folder)["scenes"]]
    near(problems, "planned lengths added up at the target", sum(float(value) for value in stored), target - 60,
         len(stored))
    near(problems, "as written kept", data["as_written_s"]["central"], central, 0.2)
    PAGES["an invented screenplay at a target"] = (folder / "14 Time and cost.md").read_text(encoding="utf-8")
    report(not problems, "the first estimate stores PLAN runtime_estimate, scene_budget and shot_budget and each "
           "scene's planned length; pace classes change the shots; a locked record keeps its values; a shorter "
           "target scales the kept scenes", shorten(problems))

    # a shot list and a partial scope
    problems = []
    set_field(folder, "00 Start here.md", "PROJECT", None, "runtime_target_s", "as_written")
    scenes_folder = folder / "11 Scenes"
    scenes_folder.mkdir(exist_ok=True)
    (scenes_folder / "Scene 01 - Back room.md").write_text(SHOT_LIST, encoding="utf-8")
    set_field(folder, "00 Start here.md", "PROJECT", None, "scope", "SC01")
    code, output = run_stage(["estimate"], folder)
    expect(problems, "estimate exit", code, 0)
    data = estimate_json(folder)
    expect(problems, "version", data["estimate"]["version"], "v1_shot_list")
    expect(problems, "scenes in scope", [block["scene"] for block in data["scenes"]], ["SC01"])
    block = data["scenes"][0] if data["scenes"] else {}
    expect(problems, "basis", block.get("basis"), "list")
    near(problems, "scene seconds from the list", block.get("runtime_s"), 15.0, 0.01)
    near(problems, "shots from the list", block.get("shots", {}).get("total"), 2, 0.01)
    expect(problems, "partial scope", data["estimate"]["partial_scope"], True)
    page = (folder / "14 Time and cost.md").read_text(encoding="utf-8")
    PAGES["an invented screenplay, a shot list in scope"] = page
    if "Scope: 1 of 3 scenes" not in page and "Scope: 1 of" not in page:
        problems.append("the page does not give the scope")
    report(not problems, "a scene with only its one-line shot list is counted from the list's times; a partial scope "
           "covers only its scenes and says so", shorten(problems))


# ---------------------------------------------------------------- group 7: prose

PLAN_OPTIONS = """# Story plan

## At a glance

Two plans for turning the book into a film, for the estimate test.

Below this line: details for the AI and the checker. You never need to read them.

### PLAN
- plan_option: A | format: feature | runtime_s: 6000 | scenes: 48 | shots: 1300 | keeps: both keepers | cuts: the letter | loses: the long winter
- plan_option: B | format: short | runtime_s: 900 | scenes: 8 | shots: 200 | keeps: the threshold | cuts: the stair | loses: the brother's fear
- status: draft
- locked: no

END OF FILE | Story plan | 1 records
"""


def merge_plan_options(folder):
    """Put the test's PLAN into 05 Story plan.md, keeping the chapter records read wrote there."""
    path = folder / "05 Story plan.md"
    text = path.read_text(encoding="utf-8")
    plan = PLAN_OPTIONS.split("Below this line: details for the AI and the checker. You never need to read them.")[1]
    plan = plan.split("END OF FILE")[0].strip()
    head, _, tail = text.rpartition("END OF FILE")
    count = int(re.search(r"(\d+) records", tail).group(1)) + 1
    path.write_text(head.rstrip() + "\n\n" + plan + "\n\n" + re.sub(r"\d+ records", f"{count} records",
                                                                      "END OF FILE" + tail), encoding="utf-8")


def group_prose(long_story, work):
    problems = []
    folder, output = make_project(LAMP_KEEPER, work / "lamp")
    if folder is None:
        report(False, "prose", output)
        return
    code, output = run_stage(["read"], folder)
    expect(problems, "read exit", code, 0)
    page = (folder / "14 Time and cost.md").read_text(encoding="utf-8") if (folder / "14 Time and cost.md").is_file() \
        else ""
    if not page:
        problems.append("read wrote no first estimate")
    PAGES["prose at step 1"] = page
    if money_found(page):
        problems.append("money shown for a book before its plans")
    if "rough" not in page:
        problems.append("the prose estimate is not labelled rough")
    merge_plan_options(folder)
    code, output = run_stage(["estimate", "--version", "v0"], folder)
    expect(problems, "estimate exit", code, 0)
    data = estimate_json(folder)
    plans = data.get("plans", [])
    expect(problems, "plans", [plan.get("plan") for plan in plans], ["A", "B"])
    if len(plans) == 2:
        near(problems, "plan A runtime", plans[0]["runtime_s"]["central"], 6000, 0.1)
        near(problems, "plan A shots at a mixed pace", plans[0]["shots"]["total"],
             (6000 - 180) / float(estimate.constant(CONSTANTS, "rhythm_class_asl_s")["mixed"]), 1)
        if not plans[0].get("by_price_level") or not plans[1].get("hours"):
            problems.append("a plan without money or hours")
        if plans[0]["by_price_level"]["mid"] <= plans[1]["by_price_level"]["mid"]:
            problems.append("the feature plan does not cost more than the short one")
    page = (folder / "14 Time and cost.md").read_text(encoding="utf-8")
    PAGES["prose, the plans side by side"] = page
    for wanted in ("The plans side by side", "Plan A", "Plan B"):
        if wanted not in page:
            problems.append(f"the page does not say {wanted!r}")
    if "Plan A:" not in output:
        problems.append("the report does not list the plans")
    report(not problems, "prose: a rough runtime only at step 1 (no money), then each macro plan estimated at its "
           "runtime, side by side", shorten(problems))

    if long_story is None:
        report(None, "The Long Places: the rough first estimate", "skipped: story not present")
        return
    problems = []
    folder, output = make_project(long_story, work / "long")
    code, output = run_stage(["read"], folder)
    expect(problems, "read exit", code, 0)
    page = (folder / "14 Time and cost.md").read_text(encoding="utf-8")
    PAGES["The Long Places at step 1"] = page
    data = estimate_json(folder)["estimate"]
    expect(problems, "rough", data["rough"], True)
    if money_found(page):
        problems.append("money shown before the plans")
    story_map = json.loads((folder / "For machines - do not edit" / "story map.json").read_text(encoding="utf-8"))
    near(problems, "rough runtime, as the reader counted it", data["story_runtime_s"]["central"],
         story_map["first_estimate"]["central_s"], 0.5)
    low_rate, high_rate = estimate.constant(CONSTANTS, "v0_action_seconds_per_word")
    if not (49152 * low_rate <= data["story_runtime_s"]["central"] <= 49152 * high_rate):
        problems.append("the rough runtime is not within the book's words at the action rates")
    report(not problems, "The Long Places at step 1: a rough runtime from its 49,152 words, labelled rough, no money",
           shorten(problems))


# ---------------------------------------------------------------- group 8: plain words

def group_plain_words():
    from stage_tools.checks_craft_reasons_words import abbreviations_in_text, retired_words_in_text
    problems = []
    for name, page in PAGES.items():
        if not page:
            continue
        retired = retired_words_in_text(page, WORDS)
        abbreviations = abbreviations_in_text(page, WORDS)
        if retired:
            problems.append(f"{name}: retired words {retired[:3]}")
        if abbreviations:
            problems.append(f"{name}: abbreviations {abbreviations[:3]}")
        if re.search(r"\bSC\d{2}|\bD13\b|\bv[01]\b|ASL", page):
            problems.append(f"{name}: an internal code in the page")
        if not page.startswith("# Time and cost\n\nIn short:"):
            problems.append(f"{name}: does not open with the In short line")
    report(not problems, f"plain words: WORDS-02 and WORDS-04 find nothing on the {len(PAGES)} pages made here, and "
           "each opens with its In short line", shorten(problems))


# ---------------------------------------------------------------- main

def main(argv):
    keep = "--keep" in argv
    arguments = [argument for argument in argv if argument != "--keep"]
    catch = long_story = None
    positional = []
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        if argument in ("--story", "--story-catch") and index + 1 < len(arguments):
            catch = Path(arguments[index + 1])
            index += 2
            continue
        if argument == "--story-long" and index + 1 < len(arguments):
            long_story = Path(arguments[index + 1])
            index += 2
            continue
        positional.append(Path(argument))
        index += 1
    if positional:
        catch = catch or positional[0]
    if len(positional) > 1:
        long_story = long_story or positional[1]
    catch = catch if catch and catch.is_file() else None
    long_story = long_story if long_story and long_story.is_file() else None
    work = Path(tempfile.mkdtemp(prefix="stage-wp7-"))
    groups = [("the price table", lambda: group_price_table()),
              ("D13's worked figures", lambda: group_recipe_zero()),
              ("The Catch", lambda: group_the_catch(catch, work)),
              ("stale prices", lambda: group_stale_prices()),
              ("the estimate from the shots", lambda: group_from_the_shots(work)),
              ("planned figures", lambda: group_planned_figures(work)),
              ("prose", lambda: group_prose(long_story, work)),
              ("plain words", lambda: group_plain_words())]
    for name, group in groups:
        try:
            group()
        except Exception as error:  # a group that crashes is a failure, and the others still run
            report(False, f"{name}: the group stopped", f"{type(error).__name__}: {error}")
            traceback.print_exc()
    if keep:
        print(f"Kept the test projects in {work}")
    else:
        shutil.rmtree(work, ignore_errors=True)
    failing = sum(1 for word, _ in RESULTS if word == "FAIL")
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({failing} failing groups)")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
