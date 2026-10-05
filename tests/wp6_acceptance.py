"""The acceptance test of work package 6: views and exports (make_views.py, make_exports.py, the command export).

What it proves on the WP12a gold (examples/01 and 02 made into a project folder), as the blueprint's row for WP6 asks
(14.2), with the checks of step 11 and T8 (14.3):
- the plain part and the divider of every record file: code writes the plain part above the divider from the
  records (At a glance, one line per item, and for the scene "Why it's shot this way"), headings are # and ## only
  (G13), the records below the divider are left byte for byte, a second run changes nothing, sections code does not
  own (the log and word list of 00 Start here, "Lines to look at") stay, and the checker's own word rules (WORDS-02
  retired words, WORDS-04 abbreviations and codes) find nothing in any plain part; 02 Whole-film summary holds the
  records step 7 reads without the floor plan;
- the shot list: UTF-8 with the byte-order mark, exactly the columns of 5.9 in order (typed here from the blueprint),
  one row per shot in film order, the crew label only in its own column;
- SubRip and WebVTT: the format of each (checked by parsers written here, not the ones under test) and the timing of
  5.9, worked out again here from the gold's records and the story's speeches;
- the timeline: the structural check of OpenTimelineIO (and a real load when the opentimelineio library is
  installed) and a CMX 3600 check of the EDL;
- breakdown.json validates against breakdown.schema.json (a validator written here, and jsonschema when installed),
  the schema keeps to C5's portable subset, and nothing nests deeper than 3 levels;
- the command export: exit codes, the book (Markdown and HTML), the audio description script, the text to
  translate, the voice line script, the spotting sheet, the finishing jobs, and the private-study mark.

Usage: python tests/wp6_acceptance.py [--story "<The Catch, the whole story>"]
The scene 10 excerpt (tests/fixtures/The Catch - lines 397-489.txt) gives the speeches; without it the timing group
says "skipped: story not present". With --story, a fresh project made from the whole story by new and read is also
given its views and exports. Standard library only (opentimelineio and jsonschema are used only when installed).
"""

import argparse
import csv
import html.parser
import io
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

from stage_tools.record_format import DIVIDER_LINE, load_skill_data, parse_file, parse_text, split_item  # noqa: E402
from stage_tools.checks_craft_reasons_words import abbreviations_in_text, retired_words_in_text  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
FIXTURES = REPOSITORY / "tests" / "fixtures"
EXCERPT = FIXTURES / "The Catch - lines 397-489.txt"
GOLD_SCENE = SKILL / "examples" / "01 The Catch - scene 10.md"
GOLD_CONTEXT = SKILL / "examples" / "02 The Catch - scene 10 - context.md"
MACHINE = "For machines - do not edit"
SCENE_FILE = "11 Scenes/Scene 10 - Saye's kitchen.md"

# Blueprint 5.9, typed here from the blueprint so the test does not read the list it checks.
COLUMNS_5_9 = ["Scene", "Shot", "Crew label", "Size", "Angle", "Camera move", "Lens (mm)", "Subject (names)",
               "Description", "Dialogue", "Screen time (s)", "Location", "Look", "Grey preview level", "Storyboard",
               "Route", "Model", "Notes", "Shot ID", "Beats"]
ELEMENT_COLUMNS_5_9 = ["Kind", "ID", "Name", "Fixed description", "States", "Scenes"]
CHECKER_FILES = ("12 Whole-film check.md", "13 Health check.md")

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
                               env=environment, timeout=600)
    return completed.returncode, completed.stdout + completed.stderr


def make_gold_project(folder, story=None):
    """A project folder from the gold: each '## From <file>' part of the context file as its numbered file (a one-line
    title above the divider, as apply makes new files), the scene file in 11 Scenes, and, with a story, the story read
    in the way adopt reads it (numbered story, speeches.json, story map.json) without touching the records."""
    folder = Path(folder)
    folder.mkdir(parents=True)
    (folder / MACHINE).mkdir()
    context = GOLD_CONTEXT.read_text(encoding="utf-8").split(DIVIDER_LINE, 1)[1]
    sections = re.split(r"^## From (.+)$", context, flags=re.MULTILINE)[1:]
    for name, body in zip(sections[0::2], sections[1::2]):
        body = re.sub(r"\n+END OF FILE .*$", "", body.strip(), flags=re.DOTALL)
        count = len(re.findall(r"^### ", body, re.MULTILINE))
        (folder / f"{name.strip()}.md").write_text(
            f"# {name.strip()}\n\n{DIVIDER_LINE}\n\n{body}\n\nEND OF FILE | {name.strip()} | {count} records\n",
            encoding="utf-8")
    (folder / "11 Scenes").mkdir()
    shutil.copy(GOLD_SCENE, folder / SCENE_FILE)
    if story is not None:
        from stage_tools.project_files import Project
        from stage_tools.read_story import read_into_project
        (folder / "Original").mkdir()
        shutil.copy(story, folder / "Original" / story.name)

        class Context:
            constants = CONSTANTS
        read_into_project(Project(folder, SCHEMA, WORDS), Context(), folder / "Original" / story.name,
                          write_records=False)
    return folder


def record_file_names(folder):
    from stage_tools.project_files import Project
    return Project(folder, SCHEMA, WORDS).record_file_names()


def split_at_divider(text):
    """(plain part, the divider and everything after it), or (text, None) when there is no divider line."""
    lines = text.split("\n")
    for position, line in enumerate(lines):
        if line.strip() == DIVIDER_LINE:
            return "\n".join(lines[:position]), "\n".join(lines[position:])
    return text, None


def constant(name):
    entry = CONSTANTS["constants"].get(name) or CONSTANTS.get("from_blueprint_text", {}).get("constants", {}).get(name)
    return entry["value"]


def words_in(text):
    return len([word for word in text.split() if re.search(r"[A-Za-z0-9]", word)])


# ---------------------------------------------------------------- 1. plain parts and dividers

@group("the plain part and the divider of every record file (2.6): made by code, # and ## headings only, records "
       "untouched, the same on a second run")
def plain_parts(workspace, story):
    from stage_tools.make_views import build_views
    project = make_gold_project(workspace / "plain parts", story)
    # Things code must keep: a log entry and a word in 00 Start here, and WP3's "Lines to look at" in 04.
    from stage_tools.project_files import Project
    start = project / "00 Start here.md"
    start.write_text(start.read_text(encoding="utf-8").replace(
        DIVIDER_LINE, f"## Word list\n\n- beat: the smallest change in a scene.\n\n{DIVIDER_LINE}", 1), encoding="utf-8")
    Project(project, SCHEMA, WORDS).add_log_entry("Scene 10 designed: 11 beats, 20 shots.")
    scene_list = project / "04 Scene list.md"
    scene_list.write_text(scene_list.read_text(encoding="utf-8").replace(
        DIVIDER_LINE, f"## Lines to look at\n\n- line 486: a transition, read as the cut after shot 200.\n\n{DIVIDER_LINE}", 1),
        encoding="utf-8")
    names = record_file_names(project)
    before = {name: (project / name).read_text(encoding="utf-8") for name in names}
    result = build_views(project)
    assert not result.problems, result.problems
    after = {name: (project / name).read_text(encoding="utf-8") for name in names}
    problems = []
    for name in names:
        if name in CHECKER_FILES:
            continue
        plain, rest = split_at_divider(after[name])
        old_plain, old_rest = split_at_divider(before[name])
        if rest is None:
            problems.append(f"{name}: no divider")
            continue
        if rest != old_rest:
            problems.append(f"{name}: the records below the divider changed")
        if not plain.startswith("# "):
            problems.append(f"{name}: the plain part does not start with a # title")
        for line in plain.split("\n"):
            if line.startswith("#") and not re.match(r"^#{1,2} ", line):
                problems.append(f"{name}: the heading {line!r} is not # or ## (G13)")
        if name != "00 Start here.md" and "\n## At a glance\n" not in plain:
            problems.append(f"{name}: no At a glance section")
        parsed = parse_text(after[name], name, SCHEMA)
        if len(parsed.records) != len(parse_text(before[name], name, SCHEMA).records):
            problems.append(f"{name}: the number of records changed")
    assert not problems, "; ".join(problems)
    start_text = split_at_divider(after["00 Start here.md"])[0]
    for heading in ("## Where things stand", "## Next step", "## Big choices so far", "## Files in this folder",
                    "## Word list", "## Log"):
        assert heading in start_text, f"00 Start here has no {heading}"
    order = [start_text.index(heading) for heading in ("## Where things stand", "## Next step", "## Big choices so far",
                                                       "## Files in this folder", "## Word list", "## Log")]
    assert order == sorted(order), "00 Start here's sections are not in the order of 13.7"
    assert re.search(r"^\d{3} \d{4}-\d{2}-\d{2} Scene 10 designed", start_text, re.MULTILINE) and \
        "- beat: the smallest change" in start_text, \
        "00 Start here lost its log or its word list"
    assert "Checked by the checker: never." in start_text, "00 Start here does not say when the checker last ran"
    assert "## Lines to look at" in split_at_divider(after["04 Scene list.md"])[0], "04 lost its Lines to look at"
    scene_plain = split_at_divider(after[SCENE_FILE])[0]
    # since Project notes 38 a one-line entry says who acts when its moments do not, and the main turn is called so
    for expected in ("## At a glance", "## The shots, one line each", "## Why it's shot this way",
                     "## Small choices I made", "- shot 150, close-up, 15 seconds, the turn, on Iona: ",
                     "- shot 990, title card, 5 seconds", "11 beats, 20 shots and the title card",
                     "The main turn is beat 7", "in shot 150"):
        assert expected in scene_plain, f"the scene's plain part has no {expected!r}"
    shot_lines = [line for line in scene_plain.split("\n") if line.startswith("- shot ")]
    assert len(shot_lines) == 21, f"{len(shot_lines)} shot lines, not 21"
    second = build_views(project)
    assert not second.changed, f"a second run changed {second.changed}"
    return (f"{len(names) - len([name for name in names if name in CHECKER_FILES])} record files; 21 shot lines in the "
            f"scene's plain part; a second run changed nothing")


@group("plain words above every divider: the checker's WORDS-02 (retired words) and WORDS-04 (abbreviations and "
       "codes) find nothing in any plain part code wrote")
def plain_words(workspace, story):
    from stage_tools.make_views import build_views
    project = make_gold_project(workspace / "plain words", story)
    build_views(project)
    found = []
    for name in record_file_names(project):
        if name in CHECKER_FILES:
            continue
        plain = split_at_divider((project / name).read_text(encoding="utf-8"))[0]
        for number, line in enumerate(plain.split("\n"), start=1):
            for written, entry in retired_words_in_text(line, WORDS):
                found.append(f"{name} line {number}: retired word {written!r}")
            for written, kind in abbreviations_in_text(line, WORDS):
                found.append(f"{name} line {number}: {kind} {written!r}")
    assert not found, "; ".join(found[:12])
    return "no retired word, abbreviation or code in the plain parts"


@group("02 Whole-film summary: one line per record of files 04 to 09 with only the fields step 7 reads, without the "
       "floor plan, with its divider, a right END count and at most summary_words_max words (fix list C25)")
def whole_film_summary(workspace, story):
    from stage_tools.make_views import build_views
    project = make_gold_project(workspace / "summary", story)
    build_views(project)
    path = project / "02 Whole-film summary.md"
    assert path.is_file(), "02 Whole-film summary.md was not written"
    parsed = parse_file(path, path.name, SCHEMA)
    assert parsed.has_divider, "the summary has no divider"
    types = {record.type_name for record in parsed.records}
    for needed in ("SCENE", "PLAN", "SEQUENCE", "PLANT", "FACT", "CHARACTER", "VOICE", "LOCATION", "PROP", "STATE"):
        assert needed in types, f"the summary has no {needed} record"
    assert not types & {"CAMSYS", "CAMRULE", "LOOK", "SHOT", "BEAT", "CHOICE"}, f"the summary holds {types}"
    below = path.read_text(encoding="utf-8").split(DIVIDER_LINE, 1)[1]
    record_lines = [line for line in below.splitlines() if line.startswith("### ")]
    assert len(record_lines) == len(parsed.records), "a record takes more than one line"
    assert not any(record.fields for record in parsed.records), "a record has field lines under its one line"
    location = next(line for line in record_lines if line.startswith("### LOCATION "))
    assert not re.search(r"\| (object|mark|size|origin_corner|wild_walls): ", location), "the floor plan is in it"
    scene = next(line for line in record_lines if line.startswith("### SCENE "))
    assert "| event: " in scene and "| dial: " not in scene, "the scene line is not its list and plan fields"
    end = parsed.end_line
    assert end is not None and end.count == len(parsed.records), "the END line's count is wrong"
    words = words_in(path.read_text(encoding="utf-8"))
    constants = json.loads((SKILL / "rules" / "constants.json").read_text(encoding="utf-8"))
    limit = constants["from_blueprint_text"]["constants"]["summary_words_max"]["value"]
    assert words <= limit, f"{words} words, over {limit}"
    return f"{len(parsed.records)} records, one line each, {words} words (at most {limit}), no floor plan"


# ---------------------------------------------------------------- 2. the spreadsheets

@group("shot list: UTF-8 with the byte-order mark, exactly the columns of 5.9, one row per shot in film order; the "
       "people, places and things list with its columns")
def spreadsheets(project):
    path = project / "16 Spreadsheets" / "Shot list.csv"
    data = path.read_bytes()
    assert data.startswith(b"\xef\xbb\xbf"), "no byte-order mark"
    rows = list(csv.reader(io.StringIO(data.decode("utf-8-sig"))))
    assert rows[0] == COLUMNS_5_9, f"columns {rows[0]}"
    body = rows[1:]
    identifiers = [row[COLUMNS_5_9.index("Shot ID")] for row in body]
    gold = parse_file(GOLD_SCENE, GOLD_SCENE.name, SCHEMA)
    shots = sorted((record for record in gold.records if record.type_name == "SHOT"),
                   key=lambda record: int(record.identifier[-3:]))
    assert identifiers == [shot.identifier for shot in shots], f"rows {identifiers}"
    assert all(len(row) == len(COLUMNS_5_9) for row in body), "a row has the wrong width"
    row_150 = body[identifiers.index("SC10-SH150")]
    cell = dict(zip(COLUMNS_5_9, row_150))
    assert cell["Scene"] == "10" and cell["Shot"] == "150" and cell["Crew label"] == "10Q", cell
    assert cell["Size"] == "close-up" and cell["Lens (mm)"] == "50" and cell["Screen time (s)"] == "15", cell
    assert cell["Dialogue"].startswith("SC10-D10, SC10-D11, SC10-D12"), cell["Dialogue"]
    assert cell["Location"] == "Saye's kitchen" and cell["Storyboard"] == "yes" and cell["Beats"] == "SC10-B07, SC10-B08"
    for row in body:
        label = row[COLUMNS_5_9.index("Crew label")]
        others = [value for position, value in enumerate(row) if position != COLUMNS_5_9.index("Crew label")]
        assert not any(re.search(r"(?<![\w-])" + re.escape(label) + r"(?![\w-])", value) for value in others), \
            f"the crew label {label} appears outside its column"
    total = sum(float(row[COLUMNS_5_9.index("Screen time (s)")]) for row in body)
    assert abs(total - 111.5) < 1e-6, f"screen times add up to {total}"
    elements = project / "16 Spreadsheets" / "People, places and things.csv"
    element_data = elements.read_bytes()
    assert element_data.startswith(b"\xef\xbb\xbf"), "the elements list has no byte-order mark"
    element_rows = list(csv.reader(io.StringIO(element_data.decode("utf-8-sig"))))
    assert element_rows[0] == ELEMENT_COLUMNS_5_9, f"element columns {element_rows[0]}"
    iona = next(row for row in element_rows if row[1] == "CH-IONA")
    assert iona[0] == "person" and "CH-IONA.S02" in iona[4] and iona[5] == "10", iona
    return f"{len(body)} rows in film order, 111.5 seconds; {len(element_rows) - 1} people, places and things"


# ---------------------------------------------------------------- 3. captions

SRT_BLOCK = re.compile(r"^(\d+)\n(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})\n(.+)$", re.DOTALL)
VTT_TIMING = re.compile(r"^(\d{2}):(\d{2}):(\d{2})\.(\d{3}) --> (\d{2}):(\d{2}):(\d{2})\.(\d{3})$")


def seconds(parts):
    hours, minutes, whole, milliseconds = (int(part) for part in parts)
    return hours * 3600 + minutes * 60 + whole + milliseconds / 1000


def read_srt(text):
    """[(start, end, text)] from SubRip text, asserting its format as it goes (a parser written for this test)."""
    assert not text.startswith("\ufeff"), "the SubRip file starts with a byte-order mark"
    cues = []
    blocks = [block for block in text.strip("\n").split("\n\n")] if text.strip() else []
    for position, block in enumerate(blocks, start=1):
        match = SRT_BLOCK.match(block)
        assert match, f"SubRip block {position} is malformed: {block[:80]!r}"
        assert int(match.group(1)) == position, f"SubRip block {position} is numbered {match.group(1)}"
        start, end = seconds(match.groups()[1:5]), seconds(match.groups()[5:9])
        assert end > start, f"SubRip cue {position} ends before it starts"
        lines = match.group(10).split("\n")
        assert 1 <= len(lines) <= 2 and all(line.strip() for line in lines), f"SubRip cue {position} text {lines}"
        cues.append((start, end, " ".join(lines)))
    return cues


def read_vtt(text):
    assert text.startswith("WEBVTT\n") or text.startswith("WEBVTT \n") or text == "WEBVTT\n", "no WEBVTT header"
    blocks = text.strip("\n").split("\n\n")
    assert blocks[0].split("\n")[0].startswith("WEBVTT"), "the header block is wrong"
    cues = []
    for block in blocks[1:]:
        lines = block.split("\n")
        if lines[0].startswith("NOTE"):
            assert "-->" not in block, "a NOTE block holds -->"
            continue
        if "-->" not in lines[0]:
            lines = lines[1:]
        match = VTT_TIMING.match(lines[0])
        assert match, f"WebVTT timing line {lines[0]!r}"
        body = lines[1:]
        assert body and all(line.strip() and "-->" not in line for line in body), f"WebVTT cue text {body}"
        cues.append((seconds(match.groups()[:4]), seconds(match.groups()[4:]), " ".join(body)))
    return cues


def expected_cues(project):
    """The cues of 5.9 worked out here from the gold's records and speeches.json: shot starts are the running sum of
    screen times; a cue starts at its hear item's at, else caption_lead_s into the shot for the first speech, else where
    the speech before ends (and never before the cue before it ends); it lasts words / pace_wps, at least
    caption_min_s and at most caption_max_s; an off-screen speaker is named; a sound at emphasis 2 or more gets a tag."""
    lead, shortest, longest = constant("caption_lead_s"), constant("caption_min_s"), constant("caption_max_s")
    speeches = {entry["id"]: entry for entry in json.loads(
        (project / MACHINE / "speeches.json").read_text(encoding="utf-8"))["speeches"]}
    context = parse_file(GOLD_CONTEXT, GOLD_CONTEXT.name, SCHEMA)
    paces = {}
    for record in context.records:
        if record.type_name == "VOICE":
            paces[record.get("character")] = float(record.get("pace_wps"))
    gold = parse_file(GOLD_SCENE, GOLD_SCENE.name, SCHEMA)
    shots = sorted((record for record in gold.records if record.type_name == "SHOT"),
                   key=lambda record: int(record.identifier[-3:]))
    cues = []
    clock = 0.0
    last_speech_cue = None
    for shot in shots:
        shot_start = clock
        clock += float(shot.get("screen_time"))
        speech_end = None
        for value in shot.get_all("hear"):
            item = split_item(value, SCHEMA.field("SHOT", "hear"))
            if item.first == "none":
                continue
            speech = speeches[item.first]
            text = speech["text"]
            length = words_in(text) / paces.get(speech["speaker"], constant("speech_wps_default"))
            at = item.get("at")
            if at is not None:
                start = shot_start + float(at)
                if last_speech_cue is not None and last_speech_cue[1] > start:
                    last_speech_cue[1] = start
            else:
                start = shot_start + lead if speech_end is None else speech_end
                if last_speech_cue is not None and start < last_speech_cue[1]:
                    start = last_speech_cue[1]
            assert length <= longest + 1e-9, "a gold speech is longer than caption_max_s; this test does not split"
            label = speech["cue"] + ": " if item.get("speaker") == "off_screen" else ""
            cue = [start, start + min(max(length, shortest), longest), label + text]
            cues.append(cue)
            last_speech_cue = cue
            speech_end = start + length
        for value in shot.get_all("effect"):
            item = split_item(value, SCHEMA.field("SHOT", "effect"))
            if item.first != "none" and int(item.get("sound_emphasis") or 0) >= 2:
                start = shot_start + float(item.get("at") or lead)
                cues.append([start, start + shortest, f"[{item.first}]"])
    return sorted(cues, key=lambda cue: cue[0])


@group("captions: SubRip and WebVTT pass their format checks and follow the timing of 5.9 (worked out again here)")
def captions(project, story):
    if story is None:
        info("skipped: story not present (the caption timing needs the speeches of the scene 10 excerpt)")
        return "skip"
    folder = project / "17 Captions and audio description"
    srt = read_srt((folder / "The Catch.srt").read_text(encoding="utf-8"))
    vtt = read_vtt((folder / "The Catch.vtt").read_text(encoding="utf-8"))
    assert [(round(start, 3), round(end, 3), text) for start, end, text in srt] == \
        [(round(start, 3), round(end, 3), text) for start, end, text in vtt], "the SubRip and WebVTT cues differ"
    expected = expected_cues(project)
    assert len(srt) == len(expected), f"{len(srt)} cues, expected {len(expected)}"
    differences = []
    for (start, end, text), (want_start, want_end, want_text) in zip(srt, expected):
        if abs(start - want_start) > 0.0011 or abs(end - want_end) > 0.0011 or text != want_text:
            differences.append(f"{start:.3f}-{end:.3f} {text!r} expected {want_start:.3f}-{want_end:.3f} {want_text!r}")
    assert not differences, "; ".join(differences[:4])
    speech_cues = [cue for cue in srt if not cue[2].startswith("[")]
    for previous, following in zip(speech_cues, speech_cues[1:]):
        assert following[0] >= previous[1] - 0.0011, f"cues overlap: {previous} and {following}"
    first = srt[0]
    assert abs(first[0] - 6.5) < 0.001 and first[2] == "SAYE: Kitchen.", first
    assert any(text == "[the scissors set down on the counter]" for _, _, text in srt), "no sound tag"
    assert any(text == "Not mint." and abs(end - start - constant("caption_min_s")) < 0.001 for start, end, text in srt), \
        '"Not mint." is not held for caption_min_s'
    return f"{len(srt)} cues in both files, every start and end as 5.9 gives them; off-screen speakers named; 1 sound tag"


# ---------------------------------------------------------------- 4. the timeline

def assert_rational(node, where):
    assert isinstance(node, dict) and node.get("OTIO_SCHEMA") == "RationalTime.1", f"{where} is not a RationalTime.1"
    assert node["rate"] > 0 and node["value"] >= 0, f"{where} is out of range"


@group("timeline: the OpenTimelineIO file passes the structural check (and loads with opentimelineio when installed); "
       "the CMX 3600 EDL is well formed")
def timeline(project):
    path = project / MACHINE / "timeline.otio"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["OTIO_SCHEMA"] == "Timeline.1", data["OTIO_SCHEMA"]
    assert_rational(data["global_start_time"], "the global start")
    stack = data["tracks"]
    assert stack["OTIO_SCHEMA"] == "Stack.1" and len(stack["children"]) == 1, "not one track in a Stack.1"
    track = stack["children"][0]
    assert track["OTIO_SCHEMA"] == "Track.1" and track["kind"] == "Video", "the track is not a video Track.1"
    clips = track["children"]
    assert [clip["OTIO_SCHEMA"] for clip in clips] == ["Clip.2"] * 21, "not 21 Clip.2 items"
    frames = 0
    for clip in clips:
        source = clip["source_range"]
        assert source["OTIO_SCHEMA"] == "TimeRange.1", clip["name"]
        assert_rational(source["start_time"], clip["name"])
        assert_rational(source["duration"], clip["name"])
        assert clip["active_media_reference_key"] in clip["media_references"], clip["name"]
        for marker in clip["markers"]:
            assert marker["OTIO_SCHEMA"] in ("Marker.1", "Marker.2"), marker
            assert marker["marked_range"]["OTIO_SCHEMA"] == "TimeRange.1", marker
        frames += source["duration"]["value"]
    assert frames == 111.5 * 24, f"{frames} frames, not {111.5 * 24}"
    assert clips[14]["name"] == "SC10-SH150" and clips[14]["source_range"]["duration"]["value"] == 360, clips[14]["name"]
    joins = [marker["name"] for clip in clips for marker in clip["markers"] if marker["name"].startswith("JOIN")]
    assert joins == ["JOIN SC10-C200"], f"join markers {joins}"
    detail = "structural check passed"
    try:
        import opentimelineio
        loaded = opentimelineio.adapters.read_from_file(str(path))
        assert len(loaded.tracks[0]) == 21 and abs(loaded.duration().to_seconds() - 111.5) < 1e-6
        detail += f"; opentimelineio {opentimelineio.__version__} loads it (21 clips, 111.5 s)"
    except ImportError:
        detail += "; opentimelineio is not installed here, so the structural check stands in (T8)"
    edl = (project / MACHINE / "timeline.edl").read_text(encoding="utf-8").split("\n")
    assert edl[0] == "TITLE: The Catch" and edl[1] == "FCM: NON-DROP FRAME", edl[:2]
    events = [line for line in edl if re.match(r"^\d{3}  ", line)]
    assert len(events) == 21, f"{len(events)} EDL events"
    previous = "01:00:00:00"
    for number, line in enumerate(events, start=1):
        match = re.match(r"^(\d{3})  (\S{1,8})\s+V     C        (\d\d:\d\d:\d\d:\d\d) (\d\d:\d\d:\d\d:\d\d) "
                         r"(\d\d:\d\d:\d\d:\d\d) (\d\d:\d\d:\d\d:\d\d)$", line)
        assert match and int(match.group(1)) == number, f"EDL event line {line!r}"
        assert match.group(5) == previous, f"EDL event {number} does not start where the one before ends"
        previous = match.group(6)
    assert previous == "01:01:51:12", f"the EDL ends at {previous}, not 01:01:51:12 (111.5 seconds)"
    return detail + "; EDL: 21 events from 01:00:00:00 to 01:01:51:12"


# ---------------------------------------------------------------- 5. breakdown.json

def validate(value, schema, path, problems):
    """A validator for the keywords of the portable subset, written for this test."""
    kind = schema["type"]
    python_type = {"object": dict, "array": list, "string": str, "boolean": bool}.get(kind)
    if python_type and not isinstance(value, python_type):
        problems.append(f"{path} is not {kind}")
        return
    if "enum" in schema and value not in schema["enum"]:
        problems.append(f"{path} = {value!r} is not in its list")
    if kind == "object":
        for name in schema["required"]:
            if name not in value:
                problems.append(f"{path} lacks {name}")
        for name in value:
            if name not in schema["properties"]:
                problems.append(f"{path} has {name}, not in the schema")
            else:
                validate(value[name], schema["properties"][name], f"{path}.{name}", problems)
    if kind == "array":
        for position, item in enumerate(value):
            validate(item, schema["items"], f"{path}[{position}]", problems)


def depth(value):
    if isinstance(value, dict):
        return 1 + max((depth(item) for item in value.values()), default=0)
    if isinstance(value, list):
        return 1 + max((depth(item) for item in value), default=0)
    return 0


def subset_faults(schema, where="schema"):
    faults = []
    allowed = {"type", "properties", "required", "additionalProperties", "items", "enum", "description", "title",
               "$schema"}
    faults += [f"{where} uses {key}" for key in schema if key not in allowed]
    if schema.get("type") == "object":
        if schema.get("additionalProperties") is not False:
            faults.append(f"{where} allows other fields")
        if set(schema.get("required", [])) != set(schema.get("properties", {})):
            faults.append(f"{where} does not require every field")
        for name, child in schema.get("properties", {}).items():
            faults += subset_faults(child, f"{where}.{name}")
    if schema.get("type") == "array":
        faults += subset_faults(schema["items"], f"{where}[]")
    for word in schema.get("enum", []):
        if word != word.lower():
            faults.append(f"{where} has the list word {word}")
    return faults


@group("breakdown.json validates against breakdown.schema.json, in C5's portable subset, nesting at most 3 levels")
def breakdown_json(project):
    data = json.loads((project / MACHINE / "breakdown.json").read_text(encoding="utf-8"))
    schema = json.loads((project / MACHINE / "breakdown.schema.json").read_text(encoding="utf-8"))
    faults = subset_faults(schema)
    assert not faults, "; ".join(faults[:6])
    problems = []
    validate(data, schema, "breakdown", problems)
    assert not problems, "; ".join(problems[:6])
    assert depth(data) <= 3, f"breakdown.json nests {depth(data)} levels"
    shot = next(item for item in data["shot"] if item["record_id"] == "SC10-SH150")
    assert shot["size"] == "close_up" and shot["label"] == "10Q" and shot["min_screen_time_s"] == "13.8", shot["label"]
    assert shot["hear"].split("\n")[1].startswith("SC10-D11"), shot["hear"]
    assert len(data["shot"]) == 21 and len(data["beat"]) == 11 and len(data["character"]) == 4, "record counts"
    detail = f"{sum(len(value) for value in data.values() if isinstance(value, list))} records, nesting {depth(data)}"
    try:
        import jsonschema
        jsonschema.Draft202012Validator.check_schema(schema)
        errors = list(jsonschema.Draft202012Validator(schema).iter_errors(data))
        assert not errors, errors[0].message
        detail += "; jsonschema agrees"
    except ImportError:
        detail += "; jsonschema is not installed here, so this test's own validator stands in"
    return detail


# ---------------------------------------------------------------- 6. the command, the book and the other exports

class BookReader(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.details = 0
        self.ids = set()
        self.links = []
        self.text = []

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if tag == "details":
            self.details += 1
        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag == "a" and attributes.get("href", "").startswith("#"):
            self.links.append(attributes["href"][1:])

    def handle_data(self, data):
        self.text.append(data)


@group("the command export: exit 0 with every step-11 file; the book in Markdown and HTML (contents, how to read it on "
       "shot 150, full shots folded, no codes or abbreviations); the audio description and text to translate")
def export_command(project, output):
    for name in ("15 The breakdown/The breakdown.md", "15 The breakdown/The breakdown.html",
                 "16 Spreadsheets/Shot list.csv", "16 Spreadsheets/People, places and things.csv",
                 "17 Captions and audio description/The Catch.srt", "17 Captions and audio description/The Catch.vtt",
                 "17 Captions and audio description/Audio description script.md",
                 "17 Captions and audio description/Text to translate.md", f"{MACHINE}/timeline.otio",
                 f"{MACHINE}/timeline.edl", f"{MACHINE}/breakdown.json", f"{MACHINE}/breakdown.schema.json"):
        assert (project / name).is_file(), f"{name} was not written"
    assert "Format checks passed" in output, output[-400:]
    markdown = (project / "15 The breakdown" / "The breakdown.md").read_text(encoding="utf-8")
    for line in markdown.split("\n"):
        assert not re.match(r"^#{3,} ", line), f"the book has the heading {line!r} (G13)"
    for expected in ("## Contents", "## How to read this", "## The story plan", "## People, places and things",
                     "## The film rules in plain words", "## Scene 10 - Saye's kitchen", "## Word list",
                     "Take shot 150 of scene 10", "<details>"):
        assert expected in markdown, f"the book has no {expected!r}"
    reader = BookReader()
    reader.feed((project / "15 The breakdown" / "The breakdown.html").read_text(encoding="utf-8"))
    assert reader.details == 21, f"{reader.details} folded shots in the HTML book, not 21"
    missing = [link for link in reader.links if link not in reader.ids]
    assert not missing, f"contents links with no heading: {missing}"
    text = " ".join(reader.text)
    found = [f"{kind} {written!r}" for written, kind in abbreviations_in_text(text, WORDS)]
    found += [f"retired word {written!r}" for written, _ in retired_words_in_text(text, WORDS)]
    assert not found, "the book holds " + "; ".join(found[:8])
    description = (project / "17 Captions and audio description" / "Audio description script.md").read_text(encoding="utf-8")
    assert "shot 150" in description and "Iona chews slowly" in description, "no description for shot 150"
    assert "shot 990: left silent on purpose" in description, "the title card's true silence was filled"
    translate = (project / "17 Captions and audio description" / "Text to translate.md").read_text(encoding="utf-8")
    assert '"THE CATCH"' in translate, "the title card is not on the text list"
    return "12 files; the book: 21 folded shots, every contents link lands, WORDS clean; descriptions fit their gaps"


@group("export voices, spotting and finishing (add-ons C and D): the voice line script, the spotting sheet, and the "
       "finishing jobs code makes from the shots, made once")
def add_on_exports(project):
    code, output = stage(["export", "voices", "--project", project])
    assert code == 0, output[-600:]
    script = (project / "20 Prompts for AI video" / "Voice line script.md").read_text(encoding="utf-8")
    lines = [line for line in script.split("\n") if line.startswith("- SC10-D")]
    assert len(lines) == 16, f"{len(lines)} voice lines, not 16"
    line_11 = next(line for line in lines if line.startswith("- SC10-D11"))
    assert '"Not mint."' in line_11 and "not steady" in line_11 and "VO-IONA" in line_11, line_11
    code, output = stage(["export", "spotting", "--project", project])
    assert code == 0, output[-600:]
    spotting = (project / "21 Edit and finishing" / "Spotting sheet.md").read_text(encoding="utf-8")
    assert "the scissors set down on the counter" in spotting and "cut to black, 24 frames" in spotting, spotting[:400]
    assert "No music cues. The music policy is none" in spotting, "the music policy is not respected"
    code, output = stage(["export", "finishing", "--project", project])
    assert code == 0, output[-600:]
    path = project / "21 Edit and finishing" / "Finishing jobs.md"
    parsed = parse_file(path, "21 Edit and finishing/Finishing jobs.md", SCHEMA)
    jobs = {(record.get("shot"), record.get("operation")) for record in parsed.records if record.type_name == "FINISH"}
    assert ("SC10-SH990", "title") in jobs, "no title job for the title card"
    assert ("SC10-SH080", "composite") in jobs, "no composite job for shot 080 (the plate route)"
    assert ("SC10-SH150", "crop") in jobs, "no crop job to the 2.39 frame"
    assert parsed.has_divider and parsed.end_line.count == len(parsed.records), "the jobs file's form is wrong"
    for record in parsed.records:
        assert re.fullmatch(SCHEMA.data["record_types"]["FINISH"]["id_pattern"], record.identifier), record.identifier
        assert record.get("operation") in SCHEMA.field("FINISH", "operation")["values"], record.get("operation")
        assert record.get("status") == "draft" and record.get("locked") == "no", record.identifier
    count = len(parsed.records)
    code, output = stage(["export", "finishing", "--project", project])
    again = parse_file(path, path.name, SCHEMA)
    assert code == 0 and len(again.records) == count, f"a second run made {len(again.records) - count} more jobs"
    return f"16 voice lines; the spotting sheet; {count} finishing jobs, none made twice"


@group("private study: with rights study_only every export is marked 'Private study, not for publication' on its first "
       "page or first row, and the formats still pass")
def private_study(workspace, story):
    project = make_gold_project(workspace / "study only", story)
    start = project / "00 Start here.md"
    start.write_text(start.read_text(encoding="utf-8").replace("- rights: mine", "- rights: study_only"), encoding="utf-8")
    code, output = stage(["export", "all", "--project", project])
    assert code == 0, output[-800:]
    mark = "Private study, not for publication"
    rows = list(csv.reader(io.StringIO((project / "16 Spreadsheets" / "Shot list.csv").read_bytes().decode("utf-8-sig"))))
    assert rows[0] == [mark] and rows[1] == COLUMNS_5_9, rows[:2]
    assert mark in (project / "15 The breakdown" / "The breakdown.md").read_text(encoding="utf-8").split("\n## ")[0]
    assert mark in (project / "17 Captions and audio description" / "The Catch.vtt").read_text(encoding="utf-8")[:300]
    assert mark in (project / MACHINE / "timeline.edl").read_text(encoding="utf-8").split("\n")[0]
    assert json.loads((project / MACHINE / "breakdown.json").read_text(encoding="utf-8"))["notice"] == mark
    assert mark in (project / "17 Captions and audio description" / "Audio description script.md").read_text(encoding="utf-8")[:300]
    return "marked in the spreadsheets, the book, the WebVTT file, the EDL, breakdown.json and the scripts"


@group("exit codes of export (7.3): 2 with one plain line for no project or no scenes; 1 when a format check fails")
def exit_codes(workspace):
    code, output = stage(["export", "all", "--project", workspace / "no such folder"])
    assert code == 2, f"exit {code} for a missing project"
    empty = workspace / "empty project"
    empty.mkdir()
    (empty / MACHINE).mkdir()
    (empty / "00 Start here.md").write_text(
        f"# Empty\n\n{DIVIDER_LINE}\n\n### PROJECT EMPTY Empty\n- title: Empty\n- status: draft\n- locked: no\n\n"
        "END OF FILE | Start here | 1 records\n", encoding="utf-8")
    code, output = stage(["export", "timeline", "--project", empty])
    assert code == 2 and "no scenes to export" in output, f"exit {code}: {output[-300:]}"
    from stage_tools import make_exports
    broken = workspace / "broken.csv"
    broken.write_text("Scene,Shot\n10,150\n", encoding="utf-8")
    assert make_exports.check_csv(broken, COLUMNS_5_9), "a CSV without its mark and columns passes the check"
    bad_srt = workspace / "bad.srt"
    bad_srt.write_text("1\n00:00:01.000 --> 00:00:02,000\nWords\n", encoding="utf-8")
    assert make_exports.check_srt(bad_srt), "a SubRip file with a full stop before the milliseconds passes"
    bad_vtt = workspace / "bad.vtt"
    bad_vtt.write_text("1\n00:00:01.000 --> 00:00:02.000\nWords\n", encoding="utf-8")
    assert make_exports.check_vtt(bad_vtt), "a WebVTT file without its header passes"
    return "2 for a missing project and for a project with no scenes; the format checks refuse broken files"


@group("the whole story: views and exports on a fresh project made by new and read (30 scenes, no shots yet)")
def whole_story(workspace, whole):
    if whole is None:
        info("skipped: story not present (give --story <The Catch> for this group)")
        return "skip"
    repository = workspace / "repository"
    (repository / "My breakdowns").mkdir(parents=True)
    (repository / "CLAUDE.md").write_text("test\n", encoding="utf-8")
    code, output = stage(["new", whole], cwd=repository)
    assert code == 0, output[-600:]
    project = next((repository / "My breakdowns").iterdir())
    code, output = stage(["read", "--project", project])
    assert code == 0, output[-600:]
    code, output = stage(["build", "--project", project])
    assert code == 0, output[-600:]
    scene_list = split_at_divider((project / "04 Scene list.md").read_text(encoding="utf-8"))[0]
    lines = [line for line in scene_list.split("\n") if line.startswith("- scene ")]
    assert len(lines) == 30, f"{len(lines)} scene lines, not 30"
    found = []
    for name in record_file_names(project):
        if name in CHECKER_FILES:
            continue
        plain = split_at_divider((project / name).read_text(encoding="utf-8"))[0]
        found += [f"{name}: {written}" for written, _ in abbreviations_in_text(plain, WORDS)]
        found += [f"{name}: {written}" for written, _ in retired_words_in_text(plain, WORDS)]
    assert not found, "; ".join(found[:8])
    code, output = stage(["export", "all", "--project", project])
    assert code == 0, output[-800:]
    return "30 scene lines in 04, plain words everywhere, export all exits 0 with no shots yet"


@group("the storyboard page (blueprint 10): approved frames laid out as 18 Storyboard/Scene 10.html, with the labels "
       "the page adds; the frames file gets its plain part")
def storyboard_page(workspace, story):
    from stage_tools.make_views import build_views
    project = make_gold_project(workspace / "storyboard", story)
    frames = project / "18 Storyboard" / "Storyboard frames.md"
    frames.parent.mkdir()
    frames.write_text(
        f"# Storyboard frames\n\n{DIVIDER_LINE}\n\n"
        "### PIC PIC-SC10-SH150-STORYBOARD-01 Iona stops chewing\n- for: SC10-SH150\n- use: storyboard\n"
        "- moment: middle\n- file: 18 Storyboard/Scene 10 - shot 150 - frame 01.png\n- approved: yes\n"
        "- status: draft\n- locked: no\n\n"
        "### PIC PIC-SC10-SH080-STORYBOARD-01 The raised hands\n- for: SC10-SH080\n- use: storyboard\n"
        "- moment: middle\n- file: 18 Storyboard/Scene 10 - shot 080 - frame 01.png\n- approved: no\n"
        "- status: draft\n- locked: no\n\nEND OF FILE | Storyboard frames | 2 records\n", encoding="utf-8")
    result = build_views(project)
    assert not result.problems, result.problems
    page = project / "18 Storyboard" / "Scene 10.html"
    assert page.is_file(), "18 Storyboard/Scene 10.html was not made"
    text = page.read_text(encoding="utf-8")
    assert "../18%20Storyboard/Scene%2010%20-%20shot%20150%20-%20frame%2001.png" in text, "the approved frame is not shown"
    assert "shot%20080%20-%20frame" not in text, "a frame that is not approved is shown"
    slide = text.split('id="shot-150"')[1].split("</section>")[0]
    for expected in ("HOLD 15 SECONDS", "ROOM SOUND ONLY", "shot 150, 15 seconds", "Not mint."):
        assert expected in slide, f"the slide for shot 150 has no {expected!r}"
    assert "frame to come" in text, "a storyboard shot with no approved frame has no placeholder"
    reader = BookReader()
    reader.feed(text)
    plain = split_at_divider(frames.read_text(encoding="utf-8"))[0]
    assert "## At a glance" in plain and not abbreviations_in_text(plain, WORDS), plain
    slides = text.count('class="slide"')
    return f"{slides} slides (1 approved frame, the other storyboard shots waiting), labels added by the page"


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
    workspace = Path(tempfile.mkdtemp(prefix="wp6 "))
    try:
        plain_parts(workspace, story)
        plain_words(workspace, story)
        whole_film_summary(workspace, story)
        project = make_gold_project(workspace / "The Catch", story)
        code, output = stage(["export", "all", "--project", project])
        report(code == 0, "stage.py export all on the gold project exits 0", f"exit {code}; {output.strip().splitlines()[-1]}")
        spreadsheets(project)
        captions(project, story)
        timeline(project)
        breakdown_json(project)
        export_command(project, output)
        add_on_exports(project)
        private_study(workspace, story)
        exit_codes(workspace)
        storyboard_page(workspace, story)
        whole_story(workspace, whole)
    finally:
        shutil.rmtree(workspace, ignore_errors=True)
    failing = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({failing} failing groups)")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
