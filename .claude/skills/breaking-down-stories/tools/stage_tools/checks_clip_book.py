"""checks_clip_book.py: the ROUTE checks, which check a route's clip book (clip_book.py), and the marks of the route's
rules, worked out from the take log (Project notes 42, W5 and W11; Project notes 43, A8).

In plain words:
- the clip book of MiniMax H3 in ComfyUI is written by stage.py compile --route into "For machines - do not edit/
  prompts/SC10 - minimax-h3-comfyui-r2v.json" (one file per scene, marked "kind": "clip_book"); the GEN checks
  leave these files to the ROUTE checks here, which run in compile and in stage.py check;
- each check belongs to one rule of the route (adapters/video_models.json, the route's "rules"): its id (H3R-01
  ...), what it says, its kind (format or judgement), its source and its kit mark: verified (a format fact found in
  MiniMax's or ComfyUI's own documents) or unclear (a judgement from testers' notes or the clip file);
- the marks are worked out again from the project's take log every time code runs: a TAKE's rule lines (rule ID |
  verdict: confirmed, wrong or unclear | note) make a rule confirmed when at least takes_to_confirm takes say
  confirmed and none says wrong, and wrong when at least takes_to_drop say wrong and more say wrong than confirmed;
- a check's level comes from its rule's mark: verified or confirmed, an error; unclear, a warning shown as a
  suggestion; wrong, not run (the take log page lists it as dropped, with the takes that showed it).

The checks, each with its rule:
  ROUTE-01 (H3R-01) the six sections in MiniMax's order, each on its own line
  ROUTE-02 (H3R-02) one <Picture N> per picture connected, numbered in wiring order, at most 9; <Picture 1> defined
  ROUTE-03 (H3R-03) every <Subject N> used is defined; no placeholder left unfilled
  ROUTE-04 (H3R-04) every person whose picture is connected is placed in a shot
  ROUTE-05 (H3R-05) speaker numbers (S1), (S2) in order of first speaking; none in retention_analysis
  ROUTE-06 (H3R-06) every line inside <d>[Language] ...</d>, the tags balanced
  ROUTE-07 (H3R-07) the lines word for word from the story's speeches
  ROUTE-08 (H3R-08) [Shot 1] without a time; later shots "[Shot N] At MM:SS.mmm," with times rising from 0
  ROUTE-09 (H3R-09) one "From ... to the end" line, inside the last shot and before the keep point
  ROUTE-10 (H3R-10) a tail of at least the route's smallest tail, and nothing timed in it
  ROUTE-11 (H3R-11) the frames on the 17 x k + 5 grid, with a one-decimal value to type that lands on them
  ROUTE-12 (H3R-12) the frames between the route's shortest and longest lengths
  ROUTE-13 (H3R-13) a held take that is longer, with its tail, than H3's longest clip
  ROUTE-14 (H3R-14) detailed_description far from MiniMax's normal length (under 200 or over 700 words)
  ROUTE-15 (H3R-15) a word that names something absent, outside the spoken lines and printed words
  ROUTE-16 (H3R-16) a word that asks for stillness
  ROUTE-17 (H3R-17) talk about speaking
  ROUTE-18 (H3R-18) a comparison
  ROUTE-19 (H3R-19) a camera move written into a static clip
  ROUTE-20 (H3R-20) a fixed description or state line not word for word, or stale
  ROUTE-21 (H3R-21) the style sentence missing
  ROUTE-22 (H3R-22) a start picture brief that does not say who is in the picture
  ROUTE-23 (H3R-23) more shots in a clip than the route allows
  ROUTE-24 (H3R-24) two shots cut together with similar framing
  ROUTE-25 (H3R-25) two singles of people facing each other with no shot showing both first
  ROUTE-26 (H3R-26) a contact shown on screen inside one shot
  ROUTE-27 (H3R-27) a clip page that does not name its master picture and character pictures

Standard library only.
"""

import json
import re
from pathlib import Path

from .check_records import register_check
from .record_format import load_json, split_item

ROUTE_MODEL = "minimax-h3-comfyui-r2v"
ROUTE_FILE_KIND = "clip_book"
MACHINE_FOLDER = "For machines - do not edit"
PROMPTS_FOLDER = "prompts"
PAGES_FOLDER = "20 Prompts for AI video/MiniMax H3 in ComfyUI"
SECTIONS = ["subject_definitions", "summary", "retention_analysis", "detailed_description", "overall_soundscape",
            "non_diegetic_music"]
CAMERA_MOVE = re.compile(r"\bcamera (?:pans|pushes|pulls|tracks|tilts|zooms|moves|dollies|cranes|follows|slides|rises|"
                         r"lowers|makes a slow)\b", re.IGNORECASE)
TIMESTAMP = re.compile(r"\b(\d{2}):(\d{2}\.\d{3})\b")
SIZE_SCALE = ["extreme_wide", "wide", "medium_wide", "medium", "medium_close_up", "close_up", "extreme_close_up"]
NO_BOOK = ("no clip book yet: stage.py compile --route h3-comfyui writes it to 'For machines - do not edit/prompts/' "
           "(add-on C)")


# ---------------------------------------------------------------- the marks of the rules, from the take log

def rule_marks(breakdown, rules, facts=None):
    """{rule ID: {"mark", "kit_mark", "confirmed": [take IDs], "wrong": [...], "unclear": [...]}} from the project's
    TAKE records (their rule lines)."""
    counts = (facts or {}).get("rule_marks_from_takes") or {}
    to_confirm = int(counts.get("takes_to_confirm") or 2)
    to_drop = int(counts.get("takes_to_drop") or 2)
    marks = {rule["id"]: {"mark": rule.get("mark") or "unclear", "kit_mark": rule.get("mark") or "unclear",
                          "confirmed": [], "wrong": [], "unclear": []} for rule in rules}
    takes = breakdown.records_of("TAKE") if breakdown is not None else []
    for take in sorted(takes, key=lambda record: record.identifier or ""):
        for written in take.get_all("rule"):
            item = split_item(written)
            identifier = (item.first or "").strip().upper()
            verdict = (item.get("verdict") or "unclear").strip().lower()
            if identifier in marks and verdict in ("confirmed", "wrong", "unclear"):
                if take.identifier not in marks[identifier][verdict]:
                    marks[identifier][verdict].append(take.identifier)
    for entry in marks.values():
        confirmed, wrong = len(entry["confirmed"]), len(entry["wrong"])
        if confirmed >= to_confirm and wrong == 0:
            entry["mark"] = "confirmed"
        elif wrong >= to_drop and wrong > confirmed:
            entry["mark"] = "wrong"
    return marks


def level_of(mark):
    """E for a verified or confirmed rule, W for an unclear one, None for a rule the take log showed wrong."""
    if mark in ("verified", "confirmed"):
        return "E"
    if mark == "wrong":
        return None
    return "W"


# ---------------------------------------------------------------- reading a clip book

def read_route_packs_of(run):
    key = "clip_book.packs"
    if key in run.cache:
        return run.cache[key]
    packs = []
    project = getattr(run, "project", None)
    folder = Path(project.folder) / MACHINE_FOLDER / PROMPTS_FOLDER if project is not None else None
    if folder is not None and folder.is_dir():
        for path in sorted(folder.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if isinstance(data, dict) and data.get("kind") == ROUTE_FILE_KIND:
                packs.append(data)
    run.cache[key] = packs
    return packs


def route_facts_of(run, model=ROUTE_MODEL):
    key = "clip_book.facts"
    if key not in run.cache:
        try:
            run.cache[key] = (load_json("adapters/video_models.json").get("models") or {}).get(model) or {}
        except (OSError, ValueError):
            run.cache[key] = {}
    return run.cache[key]


def word_fixer_of(run):
    key = "clip_book.fixer"
    if key not in run.cache:
        from .compile_prompts import Adapters, WordFixer
        run.cache[key] = WordFixer(Adapters(), run.words or {}, getattr(run, "project_record", None))
    return run.cache[key]


def section_text(prompt, name):
    """The lines of one section of a prompt (between its 'name:' line and the next section's)."""
    match = re.search(r"^" + re.escape(name) + r":\n(.*?)(?=\n\n(?:" + "|".join(SECTIONS) + r"):\n|\Z)", prompt,
                      re.MULTILINE | re.DOTALL)
    return match.group(1) if match else ""


def outside_lines(text):
    """The text without spoken lines (<d>...</d>) and printed words in quotation marks."""
    text = re.sub(r"<d>.*?</d>", " ", text, flags=re.DOTALL)
    return re.sub(r'"[^"]*"', " ", text)


def seconds_of(stamp):
    minutes, seconds = stamp
    return int(minutes) * 60 + float(seconds)


def normalised(text):
    for curly, straight in {"“": '"', "”": '"', "‘": "'", "’": "'"}.items():
        text = str(text or "").replace(curly, straight)
    return re.sub(r"\s+", " ", text).strip().casefold()


# ---------------------------------------------------------------- the checks, one function each

def check_sections(run, pack, entry, facts):
    names = re.findall(r"^(\w+):$", entry["prompt"], flags=re.MULTILINE)
    if names != SECTIONS:
        return [("prompt", f"its sections are {', '.join(names) or 'missing'}, not MiniMax's six in order",
                 "Fix: compile again; the six sections are written by code.")]
    return []


def check_pictures(run, pack, entry, facts):
    found = []
    connections = entry.get("connections") or []
    most = int((facts.get("inputs") or {}).get("references_max") or 9)
    used = sorted({int(number) for number in re.findall(r"<Picture (\d+)>", entry["prompt"])})
    if used != list(range(1, len(connections) + 1)):
        found.append(("connections", f"the prompt uses pictures {used} but {len(connections)} are connected",
                      "Fix: compile again so the labels match the pictures connected, numbered in wiring order."))
    for index, connection in enumerate(connections, start=1):
        if connection.get("label") != f"<Picture {index}>" or connection.get("input") != f"ref_image_{index - 1}":
            found.append(("connections", f"connection {index} is {connection.get('input')} as {connection.get('label')}",
                          "Fix: wire the pictures in order: ref_image_0 is <Picture 1>, ref_image_1 is <Picture 2> ..."))
            break
    if len(connections) > most:
        found.append(("connections", f"{len(connections)} pictures are connected, over the route's {most}",
                      "Fix: split the clip so fewer people are seen in it."))
    definitions = section_text(entry["prompt"], "subject_definitions")
    if "<Picture 1> is the shot-planning reference for [Shot 1]" not in definitions:
        found.append(("prompt", "<Picture 1> is not defined as the shot-planning reference for [Shot 1]",
                      "Fix: compile again."))
    return found


def check_subjects(run, pack, entry, facts):
    found = []
    definitions = section_text(entry["prompt"], "subject_definitions")
    defined = set(re.findall(r"^(<Subject \d+>) is", definitions, flags=re.MULTILINE))
    used = set(re.findall(r"<Subject \d+>", entry["prompt"]))
    if used - defined:
        found.append(("prompt", f"uses {', '.join(sorted(used - defined))} without defining it",
                      "Fix: compile again; every subject is defined in subject_definitions."))
    if re.search(r"\{[A-Za-z_:]+\}", entry["prompt"]):
        found.append(("prompt", "holds a placeholder left unfilled", "Fix: compile again."))
    return found


def check_people_placed(run, pack, entry, facts):
    found = []
    description = section_text(entry["prompt"], "detailed_description")
    definitions = section_text(entry["prompt"], "subject_definitions")
    for person in entry.get("people") or []:
        match = re.search(r"^(<Subject \d+>) is " + re.escape(person["name"]), definitions, flags=re.MULTILINE)
        label = match.group(1) if match else None
        if label is None or f"{label}, {person['name']}" not in description:
            found.append(("people", f"{person['name']}'s picture is connected but {person['name']} is never placed in "
                          "a shot", "Fix: compile again, or take the person out of the clip's shots."))
    return found


def check_speakers(run, pack, entry, facts):
    found = []
    order = []
    for number in re.findall(r"\((S\d+)\)", entry["prompt"]):
        if number not in order:
            order.append(number)
    if order != [f"S{index}" for index in range(1, len(order) + 1)]:
        found.append(("speeches", f"speaker numbers come in the order {', '.join(order)}",
                      "Fix: compile again; speakers are numbered in the order they first speak."))
    if "(S" in section_text(entry["prompt"], "retention_analysis"):
        found.append(("prompt", "a speaker number is written in retention_analysis", "Fix: compile again."))
    return found


def check_dialogue_tags(run, pack, entry, facts):
    found = []
    prompt = entry["prompt"]
    if prompt.count("<d>") != prompt.count("</d>"):
        found.append(("prompt", "its <d> tags are unbalanced", "Fix: compile again."))
    for inner in re.findall(r"<d>(.*?)</d>", prompt, flags=re.DOTALL):
        if not re.match(r"^\[[A-Z][a-z]+\] ", inner):
            found.append(("prompt", f"a line has no language tag ('{inner[:30]}')", "Fix: compile again."))
            break
    return found


def check_lines(run, pack, entry, facts):
    from .derive_fields import speech_words_part
    from .film_pass import breakdown_of
    found = []
    breakdown = breakdown_of(run)
    spoken = [normalised(inner) for inner in re.findall(r"<d>\[[A-Za-z]+\] (.*?)</d>", entry["prompt"], flags=re.DOTALL)]
    listed = [normalised(speech.get("line")) for speech in entry.get("speeches") or []]
    if spoken != listed:
        found.append(("speeches", "the lines in the prompt are not the clip's lines in order",
                      "Fix: compile again."))
    for speech in entry.get("speeches") or []:
        story = breakdown.speech(speech.get("speech")) if breakdown is not None else None
        text = re.sub(r"\s*\([^)]*\)\s*", " ", str((story or {}).get("text") or "")).strip()
        line = str(speech.get("line") or "")
        if text and normalised(line) != normalised(text) and not speech_words_part(line, text):
            found.append(("speeches", f"{speech.get('speech')} is sent as '{line[:40]}', not the story's words",
                          "Fix: compile again from the story's speeches; lines are sent word for word."))
    return found


def check_shot_markers(run, pack, entry, facts):
    found = []
    description = section_text(entry["prompt"], "detailed_description")
    shots = entry.get("shots") or []
    starts = [shot["clip_from_s"] for shot in shots]
    if not starts or abs(starts[0]) > 1e-6 or any(later <= earlier for earlier, later in zip(starts, starts[1:])):
        found.append(("shots", f"the shot times {starts} do not rise from 0", "Fix: compile again."))
    for index, shot in enumerate(shots, start=1):
        if f"[Shot {index}]" not in description:
            found.append(("prompt", f"[Shot {index}] is missing", "Fix: compile again."))
            continue
        if index == 1 and re.search(r"\[Shot 1\] At \d", description):
            found.append(("prompt", "[Shot 1] is given a time; the opening shot has none", "Fix: compile again."))
        if index > 1:
            stamp = f"{int(shot['clip_from_s'] // 60):02d}:{shot['clip_from_s'] % 60:06.3f}"
            if f"[Shot {index}] At {stamp}," not in description:
                found.append(("prompt", f"[Shot {index}] does not open with its time ({stamp})", "Fix: compile again."))
    return found


def check_end_line(run, pack, entry, facts):
    description = section_text(entry["prompt"], "detailed_description")
    lines = TIMESTAMP_END.findall(description)
    if len(lines) != 1:
        return [("prompt", f"has {len(lines)} 'From ... to the end' lines; one is needed",
                 "Fix: compile again; the last shot ends with one line of small actions so the tail is never empty.")]
    moment = int(lines[0][0]) * 60 + float(lines[0][1])
    last = (entry.get("shots") or [{}])[-1].get("clip_from_s", 0)
    if not last < moment < entry["keep_s"]:
        return [("prompt", f"its 'From ... to the end' line starts at {moment:g} seconds, outside the last shot or after "
                 f"the keep point ({entry['keep_s']:g})", "Fix: compile again.")]
    return []


TIMESTAMP_END = re.compile(r"From (\d{2}):(\d{2}\.\d{3}) to the end")


def check_tail(run, pack, entry, facts):
    found = []
    smallest = float(facts.get("tail_s_min") or pack.get("tail_s_min") or 1.3)
    total = entry["frames"] / float(facts.get("fps") or pack.get("fps") or 24)
    if total - entry["keep_s"] < smallest - 1e-6:
        found.append(("keep_s", f"leaves a tail of {total - entry['keep_s']:.2f} seconds, under {smallest:g}",
                      "Fix: compile again; the clip is made long enough for its tail."))
    description = section_text(entry["prompt"], "detailed_description")
    filler = {int(minutes) * 60 + float(seconds) for minutes, seconds in TIMESTAMP_END.findall(description)}
    for stamp in TIMESTAMP.findall(description):
        moment = seconds_of(stamp)
        if moment >= total - smallest + 0.2 - 1e-6 and moment not in filler:
            found.append(("prompt", f"times something at {moment:g} seconds, inside the tail",
                          "Fix: compile again; nothing is planned in the last seconds, which are thrown away."))
            break
    if entry.get("shots") and entry["keep_s"] <= entry["shots"][-1]["clip_from_s"]:
        found.append(("keep_s", "the part to keep ends before the last shot starts", "Fix: compile again."))
    return found


def check_frames_grid(run, pack, entry, facts):
    from .clip_book import duration_to_type, frames_from_duration_box
    frames_facts = facts.get("frames") or {}
    block, offset = int(frames_facts.get("block") or 17), int(frames_facts.get("offset") or 5)
    fps = int(facts.get("fps") or 24)
    frames = int(entry["frames"])
    found = []
    if (frames - offset) % block != 0:
        found.append(("frames", f"{frames} frames is off the {block} x k + {offset} grid",
                      "Fix: compile again; lengths are snapped to the grid."))
    typed = entry.get("seconds_to_type")
    if typed is None or duration_to_type(frames, fps, block, offset) is None or \
            frames_from_duration_box(float(typed), False, fps, block, offset) != frames or \
            frames_from_duration_box(float(typed), True, fps, block, offset) != frames:
        found.append(("seconds_to_type", f"typing {typed} does not land on {frames} frames both ways",
                      "Fix: compile again."))
    return found


def check_frames_range(run, pack, entry, facts):
    frames_facts = facts.get("frames") or {}
    low, high = int(frames_facts.get("min") or 124), int(frames_facts.get("max") or 362)
    if not low <= int(entry["frames"]) <= high:
        return [("frames", f"{entry['frames']} frames is outside {low} to {high}", "Fix: compile again.")]
    return []


def check_held_too_long(run, pack, entry, facts):
    if float(entry.get("overflow_s") or 0) > 0:
        return [("held", f"is a held take {entry['overflow_s']:g} seconds longer, with its tail, than H3's longest clip; "
                 f"only seconds 0 to {entry['keep_s']:g} of the plan's hold can be made",
                 "Fix: make the rest in the edit, or redesign the shot with a motivated cut into shots each short "
                 "enough for one clip.")]
    return []


def check_length(run, pack, entry, facts):
    words = len(section_text(entry["prompt"], "detailed_description").split())
    if words < 200 or words > 700:
        return [("prompt", f"its detailed_description has {words} words; MiniMax's guide says normally 350 to 500",
                 "Fix: write more small timed actions in the shot's moments, or split a long clip; then compile again.")]
    return []


def kept_out_check(list_name, label):
    def check(run, pack, entry, facts):
        fixer = word_fixer_of(run)
        found = []
        text = entry["prompt"]
        for key in entry.get("keys") or []:
            for form in dict.fromkeys([key.get("text") or "", (key.get("text") or "").rstrip(".")]):
                if form:
                    text = text.replace(form, " ")
        if entry.get("style_sentence"):
            text = text.replace(entry["style_sentence"], " ")
        word = fixer.kept_out_word(outside_lines(text), (list_name,))
        if list_name == "talk" and word:
            # 'says' just before a line, and 'asks' or 'answers', are how a line is introduced
            word = fixer.kept_out_word(re.sub(r"\bsays,?\s[^<]*<d>", " ", outside_lines(text)), (list_name,))
        if word:
            found.append(("prompt", f"holds '{word}' ({label}) outside the spoken lines",
                          "Fix: write what happens instead in the record it comes from, then compile again."))
        for problem in entry.get("key_problems") or []:
            if fixer.kept_out_word(problem.get("word") or "", (list_name,)):
                found.append(("prompt", f"the {problem['what']} of {problem['record']} holds '{problem['word']}' "
                              f"({label}), pasted word for word",
                              f"Fix: reword {problem['record']}'s {problem['what']} to say what is there; keys are never "
                              "cut from a prompt."))
        return found
    return check


def check_camera_static(run, pack, entry, facts):
    if all(shot.get("static") for shot in entry.get("shots") or []):
        match = CAMERA_MOVE.search(entry["prompt"])
        if match:
            return [("prompt", f"writes a camera move ('{match.group(0)}') into a static clip",
                     "Fix: keep the one camera sentence; take the move out of the record, then compile again.")]
    return []


def check_keys(run, pack, entry, facts):
    from .film_pass import breakdown_of
    found = []
    prompt = normalised(entry["prompt"])
    breakdown = breakdown_of(run)
    fixer = word_fixer_of(run)
    for key in entry.get("keys") or []:
        text = key.get("text") or ""
        if normalised(text).rstrip(".") not in prompt:
            found.append(("keys", f"the {key['what']} of {key['record']} is not in the prompt word for word",
                          "Fix: compile again; descriptions are pasted, never reworded."))
            continue
        record = breakdown.record(key["record"]) if breakdown is not None else None
        field = {"fixed description": "fixed_description", "state line": "state_line",
                 "look block": "look_block"}.get(key["what"], "state_line")
        if record is not None and record.get(field):
            current = fixer.key_words(str(record.get(field)).strip())
            if normalised(current).rstrip(".") != normalised(text).rstrip("."):
                found.append(("keys", f"the {key['what']} of {key['record']} changed since this clip was compiled",
                              "Fix: compile again; the prompt is stale."))
    return found


def check_style_sentence(run, pack, entry, facts):
    sentence = entry.get("style_sentence") or ""
    description = section_text(entry["prompt"], "detailed_description")
    if not sentence or not description.startswith(sentence):
        return [("prompt", "detailed_description does not open with the style sentence", "Fix: compile again.")]
    return []


def check_start_picture(run, pack, entry, facts):
    picture = entry.get("start_picture") or {}
    prompt = str(picture.get("prompt") or "").lower()
    found = []
    if not any(word in prompt for word in ("only person", "only people", "deserted", "exactly")):
        found.append(("start_picture", "the start picture brief does not say who is in the picture",
                      "Fix: compile again; the brief ends by naming the people in it, or saying the place is deserted."))
    fixer = word_fixer_of(run)
    banned = fixer.banned_in(prompt)
    if banned:
        found.append(("start_picture", f"the start picture brief holds {', '.join(repr(word) for word in banned)}",
                      "Fix: use the project's word swaps in the record it comes from (torch becomes flashlight)."))
    return found


def check_shot_count(run, pack, entry, facts):
    most = int(facts.get("shots_per_clip_max") or 3)
    if len(entry.get("shots") or []) > most:
        return [("shots", f"holds {len(entry['shots'])} shots; a clip holds at most {most}", "Fix: compile again.")]
    return []


def similar(first, second):
    """True when two shots cut together are framed alike: same setup and angle, within one size step, no insert."""
    if second.get("insert"):
        return False
    if first.get("angle") != second.get("angle") or first.get("setup") != second.get("setup") or not first.get("setup"):
        return False
    sizes = [first.get("size"), second.get("size")]
    if all(size in SIZE_SCALE for size in sizes):
        return abs(SIZE_SCALE.index(sizes[0]) - SIZE_SCALE.index(sizes[1])) < 2
    return sizes[0] == sizes[1]


def check_similar_framing(run, pack, entry, facts):
    shots = entry.get("shots") or []
    for first, second in zip(shots, shots[1:]):
        if similar(first, second):
            return [("shots", f"cuts from shot {first['shot'][-3:]} to shot {second['shot'][-3:]} between similar "
                     "framings, which H3 can smooth into one continuous move",
                     "Fix: make the second shot clearly different in size (two steps or more) or angle.")]
    return []


def check_facing_singles(run, pack, entry, facts):
    shots = entry.get("shots") or []
    first_people = set(shots[0].get("people") or []) if shots else set()
    for index, first in enumerate(shots):
        for second in shots[index + 1:]:
            if not (first.get("single") and second.get("single")):
                continue
            one, other = (first.get("people") or [""])[0], (second.get("people") or [""])[0]
            if one == other:
                continue
            facing = other in (first.get("looks_at") or []) or one in (second.get("looks_at") or [])
            if facing and not {one, other} <= first_people:
                return [("shots", f"puts two singles of people facing each other (shots {first['shot'][-3:]} and "
                         f"{second['shot'][-3:]}) in one clip with no shot showing both first",
                         "Fix: start the clip on a shot showing both, or make each single a clip of its own.")]
    return []


def check_contact(run, pack, entry, facts):
    found = []
    for shot in entry.get("shots") or []:
        contact = shot.get("contact_on_screen")
        if contact:
            found.append(("shots", f"shot {shot['shot'][-3:]} shows a contact inside one shot ('{contact[0]}', then "
                          f"'{contact[1]}')", "Fix: end the shot at the contact and start the next shot with the result "
                          "already there, in a clearly different size or angle, with the sound on the cut."))
    return found


def check_pictures_named(run, pack, entry, facts):
    found = []
    if not (entry.get("master_picture") or {}).get("code"):
        found.append(("master_picture", "names no master picture",
                      "Fix: give the scene a place (SCENE location) so its master picture can be made, then compile."))
    named = {picture.get("person") for picture in entry.get("character_pictures") or [] if picture.get("file")}
    missing = [person["name"] for person in entry.get("people") or [] if person["person"] not in named]
    if missing:
        found.append(("character_pictures", f"names no character picture for {', '.join(missing)}",
                      "Fix: compile again."))
    return found


CHECKS = [
    ("ROUTE-01", "H3R-01", check_sections, "Sections not in MiniMax's order (reference mode)",
     "has an H3 prompt whose six parts are missing or out of MiniMax's order"),
    ("ROUTE-02", "H3R-02", check_pictures, "Picture labels that do not match the pictures connected",
     "names pictures in its H3 prompt that do not match the pictures connected, in order"),
    ("ROUTE-03", "H3R-03", check_subjects, "A subject label used but not defined",
     "uses a label for a person or place that its H3 prompt never defines"),
    ("ROUTE-04", "H3R-04", check_people_placed, "A connected person never placed in a shot",
     "connects a person's picture without placing that person in a shot"),
    ("ROUTE-05", "H3R-05", check_speakers, "Speaker numbers out of order",
     "numbers its speakers out of the order they first speak"),
    ("ROUTE-06", "H3R-06", check_dialogue_tags, "A line without its dialogue tags or language",
     "writes a spoken line without the dialogue marks H3 reads"),
    ("ROUTE-07", "H3R-07", check_lines, "A line not word for word from the story",
     "sends a spoken line that is not the story's words"),
    ("ROUTE-08", "H3R-08", check_shot_markers, "Shot markers or their times wrong",
     "marks its shots or their times in a form H3 does not read"),
    ("ROUTE-09", "H3R-09", check_end_line, "The tail's line of small actions missing or misplaced",
     "leaves the end of the clip without the line of small actions that keeps it alive"),
    ("ROUTE-10", "H3R-10", check_tail, "Tail too short, or something timed in the tail",
     "plans something in the last seconds of a clip, which are thrown away"),
    ("ROUTE-11", "H3R-11", check_frames_grid, "Clip length off H3's frame grid",
     "asks for a clip length H3 in ComfyUI does not make, or gives seconds that land elsewhere"),
    ("ROUTE-12", "H3R-12", check_frames_range, "Clip length outside the route's range",
     "asks for a clip shorter or longer than the route's tested lengths"),
    ("ROUTE-13", "H3R-13", check_held_too_long, "Held take longer than H3's longest clip",
     "plans a held take too long for H3 to make in one piece"),
    ("ROUTE-14", "H3R-14", check_length, "detailed_description far from MiniMax's normal length",
     "has an H3 prompt much shorter or longer than MiniMax's guide asks"),
    ("ROUTE-15", "H3R-15", kept_out_check("absence", "a word naming something absent"), "A word naming something absent",
     "names something that is not there, which H3 would show"),
    ("ROUTE-16", "H3R-16", kept_out_check("stillness", "a word asking for stillness"), "A word asking for stillness",
     "asks a person to stay still, which freezes faces in H3"),
    ("ROUTE-17", "H3R-17", kept_out_check("talk", "talk about speaking"), "Talk about speaking",
     "talks about speaking, which H3 may say aloud"),
    ("ROUTE-18", "H3R-18", kept_out_check("comparison", "a comparison"), "A comparison",
     "uses a comparison, which H3 may draw"),
    ("ROUTE-19", "H3R-19", check_camera_static, "A camera move written into a static clip",
     "writes a camera move into a clip whose camera stays on its tripod"),
    ("ROUTE-20", "H3R-20", check_keys, "A description not word for word, or stale",
     "describes a person in other words than the saved ones, which re-rolls the face"),
    ("ROUTE-21", "H3R-21", check_style_sentence, "The style sentence missing",
     "leaves out the sentence that gives the film's look"),
    ("ROUTE-22", "H3R-22", check_start_picture, "A start picture brief that does not say who is in it",
     "has a start picture brief that does not say who is in the picture"),
    ("ROUTE-23", "H3R-23", check_shot_count, "More shots in a clip than the route allows",
     "puts more shots in one clip than the route allows"),
    ("ROUTE-24", "H3R-24", check_similar_framing, "Two similar framings cut together in a clip",
     "cuts between two similar framings, which H3 may blend into one"),
    ("ROUTE-25", "H3R-25", check_facing_singles, "Facing singles with no shot showing both first",
     "cuts between two people facing each other without first showing both"),
    ("ROUTE-26", "H3R-26", check_contact, "A contact shown inside one shot",
     "shows one thing hitting another inside one shot, which H3 cannot do reliably"),
    ("ROUTE-27", "H3R-27", check_pictures_named, "A clip page without its master or character pictures",
     "has a clip page that does not name the pictures to make first"),
]
KIT_LEVELS = {"ROUTE-01": "E", "ROUTE-02": "E", "ROUTE-03": "E", "ROUTE-05": "E", "ROUTE-06": "E", "ROUTE-07": "E",
              "ROUTE-08": "E", "ROUTE-11": "E", "ROUTE-13": "E"}


def route_problems(run, packs, facts=None, marks=None):
    """[Problem] of every ROUTE check over these clip books, at the level each rule's mark gives."""
    from .film_pass import breakdown_of
    facts = facts if facts is not None else route_facts_of(run)
    rules = {rule["id"]: rule for rule in facts.get("rules") or [] if isinstance(rule, dict)}
    if marks is None:
        marks = rule_marks(breakdown_of(run), list(rules.values()), facts)
    problems = []
    for pack in packs:
        page = f"{PAGES_FOLDER}/{pack.get('scene_label') or pack.get('scene')}.md"
        for entry in pack.get("clips") or []:
            if hasattr(run, "in_scope") and not run.in_scope(entry.get("scene") or pack.get("scene") or ""):
                continue
            for check_id, rule_id, function, _, _ in CHECKS:
                mark = (marks.get(rule_id) or {}).get("mark") or (rules.get(rule_id) or {}).get("mark") or "unclear"
                level = level_of(mark)
                if level is None:
                    continue
                try:
                    found = function(run, pack, entry, facts)
                except (KeyError, TypeError, ValueError, IndexError) as error:  # an old or hand-edited machine file
                    if hasattr(run, "skip"):
                        run.skip(check_id, f"{entry.get('clip')} could not be read ({type(error).__name__}: {error}); "
                                           "compile the route again")
                    continue
                for field_name, what, fix in found:
                    if level == "W":
                        what = f"{what} (a suggestion: rule {rule_id} is unclear until the take log decides it)"
                    problem = run.problem(level, check_id, entry["clip"], field_name, what, fix, file_name=page)
                    problems.append(problem)
    return problems


def lint_route_packs(compiler, project, packs, route=None):
    """The ROUTE lines for clip books held in memory (stage.py compile --route)."""
    from .check_records import CheckRun
    run = CheckRun(compiler.breakdown.record_files, compiler.breakdown.schema, compiler.words,
                   compiler.breakdown.constants, project=project)
    facts = route.facts if route is not None else route_facts_of(run)
    return route_problems(run, packs, facts)


def all_route_problems(run, check_id):
    key = "clip_book.problems"
    if key not in run.cache:
        packs = read_route_packs_of(run)
        run.cache[key] = route_problems(run, packs) if packs else None
    found = run.cache[key]
    if found is None:
        run.skip(check_id, NO_BOOK)
        return []
    return [problem for problem in found if getattr(problem, "check_id", "") == check_id]


def make_check(check_id):
    def run_check(run):
        return all_route_problems(run, check_id)
    run_check.__name__ = f"check_{check_id.lower().replace('-', '_')}"
    return run_check


for _check_id, _rule_id, _function, _title, _plain in CHECKS:
    register_check(_check_id, level=KIT_LEVELS.get(_check_id, "W"), build=2, title=f"{_title} ({_rule_id})",
                   plain=_plain, family="ROUTE")(make_check(_check_id))
