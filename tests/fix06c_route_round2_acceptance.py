"""The acceptance test of the route repairs of the second review (Project notes 43, round 2: N1 to N6, N9, N10 and
N12 to N15), for the route MiniMax H3 in ComfyUI (clip_book.py, checks_clip_book.py) and the hosted H3 gate
(compile_prompts.py).

What it proves, each group named after its finding, on copies of the saved scene 10 project (tests/fixtures/chat
saved scene 10, with the scene 10 excerpt for the spoken lines) and of the gold example, changed with invented words:
- N1: no spoken line vanishes: a crowded shot, moments that name the lines in another order than the shot's hear
  lines, and a line with a late time of its own all keep every line, in the hear order, inside the shot; a line
  written to start after its shot ends stops the clip with a ROUTE-07 error and a page note;
- N2: a cut never leaves a fragment ('unsteady', 'either side of the scar', 'then looks away', 'level, from the
  counter'), on the route and in the hosted H3 gate, which no longer leaves 'A bare.';
- N3: a person seen only in an insert is not wired, not counted in the people cap, and defined by the parts seen;
- N4: the plate route's start pictures carry no absence words and no 'Do not mirror them', and a plate-route clip
  with nobody mirrored in its first shot gets the ordinary brief from the master picture as it is;
- N5: the mirror-world warnings say what can be done (answer the side questions, keep or run the take again), never
  'a clip of its own';
- N6: a long shot's parts split a moment only at ';' and 'then', carry an action on into a part with none of its own,
  and never settle in a part that goes on;
- N9: the clip pages and the health check speak plain words: no command, no record to edit, the clip and the shot
  named, each route fault its own sentence, 'verified' explained on the take log page;
- N10: the stills made in the edit get their picture prompts in 01 Pictures to make first;
- N12: 'voice' is talk about speaking outside the code's own speaker phrase;
- N13: a mirror state that cannot be worked out is reported, never taken for 'not mirrored';
- N14: the closing line starts after the last timed action or line, and a moving camera gets its own question;
- N15: a clip's questions open with its own actions and its end, ask about everyone once, and keep the tips under
  'If it goes wrong'.

Usage: python tests/fix06c_route_round2_acceptance.py
Standard library only.
"""

import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

TESTS = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS))

from fix06a_h3_route_acceptance import (BOOK, CHAT_FOLDER, CONSTANTS, EXCERPT, PROMPTS, ROUTE, SCHEMA, SKILL,  # noqa: E402
                                        WORDS, load, route_lines, scene_file, section_of, set_field, set_moments, stage)

RESULTS = []
PAGE = "Scene 10 - Saye's kitchen.md"


def report(passed, group_title, detail=""):
    RESULTS.append(bool(passed))
    print(f"{'PASS' if passed else 'FAIL'}  {group_title}" + (f": {detail}" if detail else ""), flush=True)


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


def compiled_copy(scratch, name, edit=None, extra=()):
    """A copy of the chat fixture, changed by edit(project), compiled on the route with the story: (project, output,
    exit code, machine file)."""
    project = scratch / name
    shutil.copytree(CHAT_FOLDER, project)
    if edit is not None:
        edit(project)
    code, output = stage(["compile", "--scene", "SC10", "--route", "h3-comfyui", "--project", project, "--story", EXCERPT,
                          *extra])
    pack_path = project / PROMPTS / f"SC10 - {ROUTE}.json"
    return project, output, code, (load(pack_path) if pack_path.is_file() else None)


def clip_with(pack, shot):
    return next(clip for clip in pack["clips"] if any(entry["shot"] == shot for entry in clip["shots"]))


def replace_in_shot(project, shot, old, new):
    path = scene_file(project, shot)
    text = path.read_text(encoding="utf-8")
    start = text.index(f"### SHOT {shot} ")
    end = text.find("\n### ", start + 1)
    end = len(text) if end < 0 else end
    block = text[start:end]
    assert old in block, (shot, old)
    path.write_text(text[:start] + block.replace(old, new, 1) + text[end:], encoding="utf-8")


def set_hear_time(project, shot, speech, at):
    path = scene_file(project, shot)
    text = path.read_text(encoding="utf-8")
    changed, count = re.subn(rf"(?m)^(- hear: {re.escape(speech)} \| speaker: on_screen) \|", rf"\1 | at: {at} |", text)
    assert count == 1, speech
    path.write_text(changed, encoding="utf-8")


# ---------------------------------------------------------------- N1

@group("N1: no spoken line vanishes: a crowded shot, moments in another order than the hear lines and a late time of "
       "one's own keep every line, in order and inside the shot; a line written after its shot ends stops the clip")
def lines_never_vanish(scratch):
    lines = ["Hold up your right hand.", "That is your left.", "It's my right."]

    def crowded(project):
        set_moments(scene_file(project, "SC10-SH080"), "### SHOT SC10-SH080 ", [
            "0-2 | shows: Saye looks up from Jude to Iona and speaks",
            "2-5 | shows: Iona raises the hand nearest the camera; the two short lines pass between them"])
        set_field(scene_file(project, "SC10-SH080"), "### SHOT SC10-SH080 ", "screen_time", "5")
        path = scene_file(project, "SC10-SH080")
        path.write_text(path.read_text(encoding="utf-8").replace("dwell_s: 9", "dwell_s: 5"), encoding="utf-8")

    def reordered(project):
        set_moments(scene_file(project, "SC10-SH080"), "### SHOT SC10-SH080 ", [
            "0-2 | shows: Saye looks up from Jude to Iona",
            "2-4.5 | shows: Iona says it's my right; both hold",
            "4.5-9 | shows: Saye says hold up your right hand, then that is your left"])

    def late_time(project):
        set_hear_time(project, "SC10-SH080", "SC10-D05", 7)

    found = []
    for name, edit in (("crowded", crowded), ("reordered", reordered), ("late time", late_time)):
        project, output, code, pack = compiled_copy(scratch, f"N1 {name}", edit)
        clip = clip_with(pack, "SC10-SH080")
        speeches = [speech["speech"] for speech in clip["speeches"]]
        assert speeches == ["SC10-D05", "SC10-D06", "SC10-D07"], (name, speeches)
        for line in lines:
            assert line in clip["prompt"], (name, line)
        assert all(speech["at"] < clip["keep_s"] for speech in clip["speeches"]), (name, clip["speeches"])
        assert not [line for line in route_lines(output, "ROUTE-07") if "SC10-CL04" in line], (name, output[-600:])
        found.append(f"{name}: " + ", ".join(f"{speech['at']:g}" for speech in clip["speeches"]))
    # a time written after the shot's end: an error and a note, never silence
    project, output, code, pack = compiled_copy(scratch, "N1 outside", lambda project: set_hear_time(
        project, "SC10-SH080", "SC10-D07", 10))
    lost = [line for line in route_lines(output, "ROUTE-07") if line.startswith("E ") and "SC10-D07" in line]
    assert code == 1 and lost, output[-800:]
    page = (project / BOOK / PAGE).read_text(encoding="utf-8")
    assert "is written to start at 10 seconds, outside shot 080" in page, "no page note for the line outside its shot"
    return "; ".join(found) + "; a line after its shot: ROUTE-07 error"


# ---------------------------------------------------------------- N2

@group("N2: a cut never leaves a fragment: the reviewer's wordings go whole, a clause that stands keeps its words, "
       "and the hosted H3 gate no longer leaves 'A bare.' or 'It ends: either side of the scar.'")
def cuts_leave_no_fragment(scratch):
    sys.path.insert(0, str(SKILL / "tools"))
    from stage_tools.clip_book import KEPT_OUT_LISTS, trim_kept_out
    from stage_tools.compile_prompts import Adapters, WordFixer
    fixer = WordFixer(Adapters(), WORDS, None)
    fixer.word_lists.setdefault("held", ["stays", "stay", "remains", "remain"])
    lists = KEPT_OUT_LISTS + ("held",)
    for wording in ("her hands still and flat, either side of the scar", "the disc still, on his own left side",
                    "she says nothing, then looks away", "Dr Saye still, eyes down on something below the frame",
                    "says two words, unsteady"):
        for action in (False, True):
            kept, _, cut = trim_kept_out(fixer, wording, lists, action)
            assert kept == "" and cut == [wording], (wording, action, kept, cut)
    kept, _, cut = trim_kept_out(fixer, "Saye speaks, level, from the counter; Iona breathes in, her eyes on Saye", lists,
                                 True)
    assert kept == "Iona breathes in, her eyes on Saye", kept
    kept, _, _ = trim_kept_out(fixer, "a bare, clean kitchen with nothing on the walls or the fridge door", lists)
    assert kept == "a bare, clean kitchen", kept
    kept, _, _ = trim_kept_out(fixer, "Anna looks up and speaks", lists, True)
    assert kept == "Anna looks up", kept
    dropped = []
    assert fixer.drop_kept_out("a bare, clean kitchen with nothing on the walls", ("absence",), dropped) == \
        "a bare, clean kitchen" and dropped == ["with nothing on the walls"], dropped
    # the route: the chat fixture's own fragments are gone
    project, output, code, pack = compiled_copy(scratch, "N2 route")
    text = json.dumps([clip["prompt"] + clip["start_picture"]["prompt"] for clip in pack["clips"]])
    for fragment in (", unsteady.", "seconds, level", ": level", "instant this begins: level"):
        assert fragment not in text, fragment
    # the hosted H3 gate, on a copy with the old kitchen wording and an end that leaves a lone place
    project = scratch / "N2 hosted"
    shutil.copytree(CHAT_FOLDER, project)
    continuity = project / "09 Continuity.md"
    set_field(continuity, "### STATE LOC-SAYE-KITCHEN.S01 ", "state_line",
              "a bare, clean kitchen with nothing on the walls or the fridge door")
    set_field(scene_file(project, "SC10-SH080"), "### SHOT SC10-SH080 ", "end",
              "her hands still and flat, either side of the scar")
    code, output = stage(["compile", "--scene", "SC10", "--force-model", "minimax-h3", "--project", project, "--story",
                          EXCERPT])
    assert code in (0, 1), output[-800:]
    hosted = "".join(path.read_text(encoding="utf-8") for path in (project / "For machines - do not edit").rglob(
        "*minimax-h3*.json"))
    assert hosted, "no hosted H3 pack written"
    assert "A bare." not in hosted and "It ends: either" not in hosted, "a fragment in the hosted H3 prompts"
    assert "a bare, clean kitchen" in hosted.lower(), "the kitchen's own words were lost"
    return "five wordings go whole; standing clauses kept; route and hosted prompts hold no fragment"


# ---------------------------------------------------------------- N3

@group("N3: a person seen only in an insert is not wired, not counted against the cap, defined by the parts seen and "
       "kept fully_preserved for them; the start picture still gets their picture")
def insert_people_not_wired(project):
    pack = load(project / PROMPTS / f"SC10 - {ROUTE}.json")
    clip = clip_with(pack, "SC10-SH040")
    jude = next(person for person in clip["people"] if person["person"] == "CH-JUDE")
    assert jude["wired"] is False, jude
    assert not [picture for picture in clip["character_pictures"] if picture["person"] == "CH-JUDE"]
    assert not [connection for connection in clip["connections"] if "Jude" in connection["picture"]]
    definitions = section_of(clip["prompt"], "subject_definitions")
    line = next(line for line in definitions.splitlines() if " is Jude" in line)
    assert "of whom only his chest is seen" in line and "face, hair and build" not in line, line
    retention = section_of(clip["prompt"], "retention_analysis")
    assert re.search(r"fully_preserved - only Jude's chest is seen", retention), retention
    assert "Jude's face" not in clip["prompt"], "Jude's face is still described"
    assert "Do Jude's chest and clothes match your Jude picture?" in clip["questions"]
    assert "your Jude picture (Reference pictures/" in ", ".join(clip["start_picture"]["attach"])
    assert "two people's pictures in all" in " ".join(clip["joins"]), clip["joins"]
    return f"{clip['clip']}: Jude defined by his chest, {len(clip['connections']) - 1} pictures wired"


# ---------------------------------------------------------------- N4, N5 (the gold scene, in the mirror world)

@group("N4, N5: the plate start pictures carry no absence words and no 'Do not mirror them'; a plate clip with nobody "
       "mirrored in its first shot gets the ordinary brief; the mirror warnings say what can be done")
def mirror_briefs_and_warnings(scratch):
    from stage_tools.build_kit import gold_project
    from stage_tools.compile_prompts import Adapters, WordFixer
    folder, _ = gold_project(scratch / "gold" / "The Catch", SKILL)
    code, output = stage(["compile", "--scene", "SC10", "--route", "h3-comfyui", "--project", folder, "--story", EXCERPT])
    assert code in (0, 1), output[-1200:]
    pack = load(folder / PROMPTS / f"SC10 - {ROUTE}.json")
    fixer = WordFixer(Adapters(), WORDS, None)
    plates = [clip for clip in pack["clips"] if clip["start_picture"].get("plate")]
    assert plates, "no plate brief"
    for clip in pack["clips"]:
        brief = clip["start_picture"]["prompt"]
        assert "Do not mirror them" not in brief and " does not " not in brief, (clip["clip"], brief[-400:])
        assert not fixer.kept_out_word(brief, ("absence",)), (clip["clip"], fixer.kept_out_word(brief, ("absence",)))
    lone = clip_with(pack, "SC10-SH150")
    assert lone["mirror"]["routes"] == ["plate"] and not lone["start_picture"].get("plate"), lone["mirror"]
    assert "Step 1, the plate" not in lone["start_picture"]["prompt"] and "flipped" not in lone["start_picture"]["prompt"]
    later = [line for line in route_lines(output, "ROUTE-27") if "later shot" in line]
    assert later, route_lines(output, "ROUTE-27")
    page = (folder / BOOK / PAGE).read_text(encoding="utf-8")
    assert "a clip of its own" not in " ".join(later) and "clips of their own" not in page.split("## Clip 01")[1]
    assert all("run it again with another seed" in line for line in later), later[0]
    for clip in pack["clips"]:
        for problem in clip["mirror"]["problems"]:
            number = re.search(r"shot (\d{3}) is in the mirror world", problem)
            if number:
                assert any(question.startswith(f"Shot {number.group(1)}:") for question in clip["questions"]), \
                    (clip["clip"], number.group(1))
    return f"{len(plates)} plate briefs clean; shot 150 ordinary; {len(later)} warnings say what to do"


# ---------------------------------------------------------------- N6

@group("N6: a long shot's parts split a moment only at ';' and 'then', carry an action on into a part with none of its "
       "own, and never settle in a part that goes on")
def long_shot_moments(scratch):
    def one_moment(project):
        path = scene_file(project, "SC10-SH140")
        set_field(path, "### SHOT SC10-SH140 ", "screen_time", "30")
        set_moments(path, "### SHOT SC10-SH140 ", ["0-30 | shows: she crosses to the sill and back, slowly"])

    def two_actions(project):
        path = scene_file(project, "SC10-SH140")
        set_field(path, "### SHOT SC10-SH140 ", "screen_time", "30")
        set_moments(path, "### SHOT SC10-SH140 ", ["0-30 | shows: she crosses to the sill, slowly; she comes back to "
                                                   "the table"])

    project, output, code, pack = compiled_copy(scratch, "N6 one", one_moment)
    parts = [clip for clip in pack["clips"] if clip["shots"][0]["shot"] == "SC10-SH140"]
    assert len(parts) >= 2, len(parts)
    for clip in parts:
        description = section_of(clip["prompt"], "detailed_description")
        assert "crosses to the sill and back, slowly" in description, (clip["clip"], description[-500:])
        assert re.search(r"seconds, slowly\.", description) is None
    for clip in parts[:-1]:
        closing = re.search(r"From \d{2}:\d{2}\.\d{3} to the end, [^.]*\.", section_of(clip["prompt"],
                                                                                       "detailed_description")).group(0)
        assert "settles" not in closing and "go on with what" in closing, closing
    project, output, code, pack = compiled_copy(scratch, "N6 two", two_actions)
    parts = [clip for clip in pack["clips"] if clip["shots"][0]["shot"] == "SC10-SH140"]
    texts = [section_of(clip["prompt"], "detailed_description") for clip in parts]
    assert all("comes back to the table" in text or "crosses to the sill, slowly" in text for text in texts), texts
    assert any("the same action carries on" in text for text in texts) or len(parts) == 2, texts
    return f"{len(parts)} parts; every part has an action; no settling before the cut"


# ---------------------------------------------------------------- N9

@group("N9: plain words: no command or record to edit on the clip pages, the health check names the clip and the "
       "shot and gives each route fault its own sentence, and the take log explains 'verified'")
def plain_words(project):
    page = (project / BOOK / PAGE).read_text(encoding="utf-8")
    settings = (project / BOOK / "00 Settings and how to run a clip.md").read_text(encoding="utf-8")
    for text in (page, settings):
        for words in ("--story", "stage.py", "compile again", "Write what happens instead", "Reword it",
                      "Change the shot in the breakdown"):
            assert words not in text, words
    assert "Ask Claude to read the whole story again" in page and "Tell Claude what happens instead" in page
    take_log = (project / BOOK / "Take log.md").read_text(encoding="utf-8")
    assert "Verified means the rule is stated in the makers' own documents" in take_log
    code, output = stage(["check", "--all", "--project", project])
    health = (project / "13 Health check.md").read_text(encoding="utf-8").split("Below this line")[0]
    route_plain = [line for line in health.splitlines() if re.match(r"^- Scene 10, clip \d{2} \(shot \d{3}\): ", line)]
    assert route_plain, health[:1500]
    assert "Scene 10, a record" not in health and " or times two lines over each other" not in health
    assert "the pictures to make first, or a mirror-world part" not in health
    assert any("does not know yet who is mirrored" in line for line in route_plain), route_plain
    assert re.search(r"- Scene 10, clip 07 \(shot 150\): plans a held take too long", health), health[:1200]
    assert "11 Scenes/Scene 10 - Saye's kitchen - shots 130-990: 1 problem" in health, health[-1500:]
    return f"{len(route_plain)} route lines name their clip and shot"


# ---------------------------------------------------------------- N10, N12, N14, N15 (the compiled chat fixture)

@group("N10: the stills made in the edit get their picture prompts in 01 Pictures to make first")
def stills_for_the_edit(project):
    pack = load(project / PROMPTS / f"SC10 - {ROUTE}.json")
    stills = pack.get("stills") or []
    assert {still["shot"] for still in stills} == {"SC10-SH090", "SC10-SH100"}, [still["shot"] for still in stills]
    pictures = (project / BOOK / "01 Pictures to make first.md").read_text(encoding="utf-8")
    assert "## Stills for the edit" in pictures
    for number in ("090", "100"):
        part = pictures.split(f"### Scene 10, shot {number}")[1].split("###")[0]
        assert "```text" in part and f"Stills/Scene 10 - shot {number} - still.png" in part, part[:300]
    page = (project / BOOK / PAGE).read_text(encoding="utf-8")
    assert "under Stills for the edit" in page
    return "shots 090 and 100 have picture prompts"


@group("N12: 'voice' is talk about speaking, cut from the moments and caught by ROUTE-17, except in the code's own "
       "speaker phrase right before a line")
def voice_is_talk(project):
    from types import SimpleNamespace
    from stage_tools.checks_clip_book import kept_out_check
    pack = load(project / PROMPTS / f"SC10 - {ROUTE}.json")
    for clip in pack["clips"]:
        assert "Eli's voice;" not in clip["prompt"] and "a voice also comes" not in clip["prompt"], clip["clip"]
    assert any("'Eli's voice'" in note for clip in pack["clips"] for note in clip["left_out"])
    check = kept_out_check("talk", "talk about speaking")
    run = SimpleNamespace(cache={}, words=WORDS, project_record=None)
    base = {"keys": [], "style_sentence": "", "key_problems": [], "clip": "SC01-CL01"}
    entry = dict(base, prompt="detailed_description:\n[Shot 1] The hand stops; Ben's voice. <Subject 2> (S1) says: "
                              "<d>[English] Go.</d>\n")
    assert check(run, {"clips": [entry]}, entry, {}), "'Ben's voice' was not caught"
    entry = dict(base, prompt="detailed_description:\n[Shot 1] From off screen, a man's voice (S2), a low voice, warm, "
                              "says, quietly: <d>[English] No.</d>\n")
    assert not check(run, {"clips": [entry]}, entry, {}), check(run, {"clips": [entry]}, entry, {})
    return "'voice' cut and caught; the speaker phrase passes"


@group("N14, N15: the closing line starts after the last timed action or line; a clip's questions open with its own "
       "actions and end, ask about everyone once, and keep the tips under 'If it goes wrong'")
def closing_and_questions(project):
    pack = load(project / PROMPTS / f"SC10 - {ROUTE}.json")
    for clip in pack["clips"]:
        description = section_of(clip["prompt"], "detailed_description")
        last = description.splitlines()[-1]
        before = last.split("From ")[0]
        stamps = [int(minutes) * 60 + float(seconds) for minutes, seconds in
                  re.findall(r"At (?:about )?(\d{2}):(\d{2}\.\d{3})", before)]
        if stamps:
            assert clip["filler_s"] > max(stamps), (clip["clip"], clip["filler_s"], max(stamps))
        questions = clip["questions"]
        assert questions[0].startswith(("Do these happen, in this order: ", "Does this happen: ", "Does it end on this: ")), \
            (clip["clip"], questions[:2])
        assert len([question for question in questions if "keep moving" in question or " move between" in question]) <= 1
        assert len([question for question in questions if "same face" in question or "faces the same" in question]) <= 1
    clip = clip_with(pack, "SC10-SH080")
    assert any(question.startswith("Does it end on this: both hands raised") for question in clip["questions"]), \
        clip["questions"]
    page = (project / BOOK / PAGE).read_text(encoding="utf-8")
    check_part = page.split("## Clip 05")[1].split("### Keep")[0].split("### Check")[1]
    questions_part, tips = check_part.split("If it goes wrong:")
    assert questions_part.count("\n- ") <= 10 and "run another seed" in tips, check_part
    return f"clip 05 asks {questions_part.count(chr(10) + '- ')} questions, then the tips"


@group("N14: a moving camera gets its own question")
def moving_camera_question(scratch):
    project, output, code, pack = compiled_copy(scratch, "N14 moving", lambda project: replace_in_shot(
        project, "SC10-SH120", "- move: static\n", "- move: push_in\n"))
    clip = clip_with(pack, "SC10-SH120")
    assert any("make its one move (push in)" in question for question in clip["questions"]), clip["questions"]
    assert not any("hold its framing" in question for question in clip["questions"])
    return clip["clip"] + ": " + next(question for question in clip["questions"] if "one move" in question)


# ---------------------------------------------------------------- N13

@group("N13: a mirror state that cannot be worked out is reported in the clip's mirror problems, never taken for "
       "'not mirrored' in silence")
def mirror_gaps_reported():
    from stage_tools import compile_prompts
    from stage_tools.clip_book import RouteFacts, compile_scene, master_pictures
    from stage_tools.compile_prompts import Adapters, Compiler, raw_speeches_of
    from stage_tools.derive_fields import Breakdown
    breakdown = Breakdown.from_project(CHAT_FOLDER, SCHEMA, WORDS, CONSTANTS)
    breakdown.attach_story_file(str(EXCERPT))
    adapters = Adapters()
    compiler = Compiler(breakdown, adapters, WORDS, raw_speeches_of(story_path=str(EXCERPT), constants=CONSTANTS))
    route = RouteFacts.from_adapters(adapters)
    original = compile_prompts.reference_turned

    def broken(*arguments):
        raise KeyError("an era with no set plan")
    compile_prompts.reference_turned = broken
    try:
        plans, clips = compile_scene(compiler, route, "SC10", master_pictures(compiler, route))
    finally:
        compile_prompts.reference_turned = original
    gaps = [problem for clip in clips for problem in clip.mirror["problems"] if "could not be worked out" in problem]
    assert gaps and len(gaps) >= len(clips) - 1, (len(gaps), len(clips))
    assert "tell Claude" in gaps[0], gaps[0]
    return f"{len(gaps)} clips report the gap"


def main():
    with tempfile.TemporaryDirectory() as temporary:
        scratch = Path(temporary)
        project, output, code, pack = compiled_copy(scratch, "scene 10")
        insert_people_not_wired(project)
        stills_for_the_edit(project)
        voice_is_talk(project)
        closing_and_questions(project)
        plain_words(project)
        lines_never_vanish(scratch)
        cuts_leave_no_fragment(scratch)
        long_shot_moments(scratch)
        moving_camera_question(scratch)
        mirror_briefs_and_warnings(scratch)
        mirror_gaps_reported()
    failing = len([passed for passed in RESULTS if not passed])
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({len(RESULTS) - failing} groups passed, {failing} failed)")
    return 0 if not failing else 1


if __name__ == "__main__":
    sys.exit(main())
