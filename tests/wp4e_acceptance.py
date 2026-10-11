"""The acceptance test of work package 4e: the PLAN, GEN and FILM checks of blueprint 7.2 and the film pass
(.claude/skills/breaking-down-stories/tools/stage_tools/checks_plan_generation_film.py and film_pass.py).

What it proves (blueprint 7.2, 3 step 9, 14.2 row WP4):
- every PLAN, GEN and FILM check of 7.2 is registered with 7.2's level and build and a plain sentence;
- one faulty fixture or more per build-1 check (tests/fixtures/plan generation and film/faults.json: named edits to
  a temporary copy of the WP12a gold and of a clean compiled pack) fires with 7.2's message format (level, check
  ID, record, field, what is wrong, then the fix), naming the record and field it should, placed in a file and
  line; the build-2 checks FILM-05, FILM-07, FILM-09, GEN-16 and GEN-17 fire on theirs too;
- every one of these checks is silent on the WP12a gold fixture (references/examples/01 and 02 with the scene 10 excerpt, the
  whole story when --story is given, and no story at all), at check --all and at steps 2, 9 and 10, with and
  without the stand-in model facts; silent on the chat-saved copy; and the GEN checks are silent on a clean
  compiled pack of scene 10;
- while _config/adapters/*.json (work package 8) are missing, the GEN checks that need model facts skip and say so;
- stage.py check --film on a project made from the gold writes the film strip (one line per shot) and
  12 Whole-film check.md (plain part, divider, FINDING records, END line); a FILM problem becomes one FINDING with
  source checker, a second run adds no duplicate, and check --all finds nothing wrong with the file it wrote.

The GEN faults use STAND-IN model facts (tests/fixtures/plan generation and film/stand-in model facts.json, values
from blueprint 8.2 and C3 L02 and L28), given to the checks through use_model_facts, so that the faults do not move
when the dated adapter files change. The gold is also checked with the real _config/adapters/*.json, and the groups about
missing adapter files hide those files from the checks (without_adapter_files) rather than depend on their absence.

Usage: python tests/wp4e_acceptance.py [--story "<The Catch, the whole story>"]
Without the scene 10 excerpt the story groups say "skipped: story not present". Standard library only.
"""

import argparse
import copy
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

from stage_tools import checks_plan_generation_film as generation  # noqa: E402
from stage_tools.check_records import REGISTRY, StorySource, load_check_families, run_checks  # noqa: E402
from stage_tools.project_files import Project  # noqa: E402
from stage_tools.record_format import DIVIDER_LINE, load_skill_data, parse_file, parse_text  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
FIXTURES = REPOSITORY / "tests" / "fixtures"
OWN_FIXTURES = FIXTURES / "plan generation and film"
FAULTS_FILE = OWN_FIXTURES / "faults.json"
STAND_IN_FACTS = OWN_FIXTURES / "stand-in model facts.json"
CLEAN_PACK = OWN_FIXTURES / "compiled pack SC10.json"
EXCERPT = FIXTURES / "The Catch - lines 397-489.txt"
CHAT_FOLDER = FIXTURES / "chat saved scene 10"
GOLD_FILES = {"scene": SKILL / "references" / "examples" / "01 The Catch - scene 10.md",
              "context": SKILL / "references" / "examples" / "02 The Catch - scene 10 - context.md"}
MACHINE = "For machines - do not edit"

OWN_FAMILIES = ("PLAN", "GEN", "FILM")
LEVELS_7_2 = {
    "PLAN-01": "E", "PLAN-02": "E", "PLAN-03": "W", "PLAN-04": "W", "PLAN-05": "E",
    "GEN-01": "E", "GEN-02": "E", "GEN-03": "E", "GEN-04": "E", "GEN-05": "E", "GEN-06": "E", "GEN-07": "E",
    "GEN-08": "E", "GEN-09": "E", "GEN-10": "E", "GEN-11": "E", "GEN-12": "E", "GEN-13": "W", "GEN-14": "E",
    "GEN-15": "E", "GEN-16": "W", "GEN-17": "W",
    "FILM-01": "W", "FILM-02": "W", "FILM-03": "E", "FILM-04": "W", "FILM-05": "W", "FILM-06": "W", "FILM-07": "W",
    "FILM-08": "E", "FILM-09": "W", "FILM-10": "W", "FILM-11": "W", "FILM-12": "W",
}
BUILD_TWO = {"GEN-16", "GEN-17", "FILM-05", "FILM-07", "FILM-09"}
OWN_CHECKS = list(LEVELS_7_2)
NEEDS_FACTS = {"GEN-01", "GEN-02", "GEN-08", "GEN-09", "GEN-10"}
# 7.2: "Every message is one line: level, check ID, record, field, what is wrong, the allowed values or the fix."
LINE_FORM = re.compile(r"^(?P<level>[EWN]) (?P<check>[A-Z]+-\d{2}) (?P<record>\S+) (?P<field>[a-z_]+) (?P<what>.+?)\. "
                       r"(?P<fix>(?:Fix|Allowed): .+?)(?: \[(?P<place>[^\]]+)\])?$")
CODE_IN_PLAIN = re.compile(r"\b(?:[A-Z]{2,6}-\d{2}\b|SC\d{2,3}|FIND-\d|CH-[A-Z]|RC-\d|PL-\d)")

RESULTS = []


def without_adapter_files():
    """Make the GEN checks behave as if _config/adapters/video_models.json and image_models.json were missing (the files
    exist since work package 8, so their absence is simulated through the module's override)."""
    generation._MODEL_FACTS_OVERRIDE.update(facts=None, used=True)


def report(passed, group, detail=""):
    RESULTS.append(passed)
    print(f"{'PASS' if passed else 'FAIL'}  {group}" + (f": {detail}" if detail else ""), flush=True)


def info(line):
    print(f"INFO  {line}", flush=True)


# ---------------------------------------------------------------- the gold, the pack, and faults made from them

def gold_texts():
    return {name: path.read_text(encoding="utf-8") for name, path in GOLD_FILES.items()}


def record_block(lines, heading):
    """(first, end) line indexes of the record '### <heading> ...' (end is the first line after it)."""
    for index, line in enumerate(lines):
        if line == f"### {heading}" or line.startswith(f"### {heading} "):
            end = index + 1
            while end < len(lines) and not lines[end].startswith(("### ", "## ", "END OF FILE")) \
                    and lines[end] != DIVIDER_LINE:
                end += 1
            return index, end
    raise AssertionError(f"no record {heading}")


def apply_edit(texts, edit):
    """One named edit to a copy of the gold (see the note at the top of faults.json)."""
    name = edit["file"]
    lines = texts[name].split("\n")
    if "add_after_record" in edit:
        _, end = record_block(lines, edit["add_after_record"])
        while end > 0 and not lines[end - 1].strip():
            end -= 1
        lines[end:end] = [""] + edit["text"].rstrip("\n").split("\n")
    else:
        first, end = record_block(lines, edit["record"])
        block = "\n".join(lines[first:end]) + "\n"
        if edit["find"] not in block:
            raise AssertionError(f"{edit['record']} does not hold {edit['find']!r}")
        block = block.replace(edit["find"], edit["replace"], 1)
        lines[first:end] = block[:-1].split("\n")
    texts[name] = "\n".join(lines)
    return texts


def parse_texts(texts):
    return [parse_text(texts["scene"], GOLD_FILES["scene"].name, SCHEMA),
            parse_text(texts["context"], GOLD_FILES["context"].name, SCHEMA)]


def story_from(path):
    if path is None or not Path(path).is_file():
        return None
    return StorySource.from_file(path, CONSTANTS)


def clean_pack():
    return json.loads(CLEAN_PACK.read_text(encoding="utf-8"))


def stand_in_facts():
    return json.loads(STAND_IN_FACTS.read_text(encoding="utf-8"))


def apply_pack_edit(pack, edit):
    """One edit to a copy of the clean pack (see the note at the top of faults.json)."""
    clips = pack["clips"]
    if "pack_set" in edit:
        pack.update(edit["pack_set"])
        return pack
    if "add_clip" in edit:
        clips.append(copy.deepcopy(edit["add_clip"]))
        return pack
    if "split_clip" in edit:
        clip = next(clip for clip in clips if clip["clip"] == edit["split_clip"])
        second = copy.deepcopy(clip)
        second["clip"] = re.sub(r"\.\d+$", ".2", clip["clip"])
        clips.append(second)
        return pack
    clip = next(clip for clip in clips if clip["clip"] == edit["clip"])
    if "append" in edit:
        clip["prompt"] += edit["append"]
    if "replace" in edit:
        find, replace = edit["replace"]
        if find not in clip["prompt"]:
            raise AssertionError(f"{edit['clip']}'s prompt does not hold {find!r}")
        clip["prompt"] = clip["prompt"].replace(find, replace, 1)
    if "set" in edit:
        clip.update(edit["set"])
    return pack


def project_with_pack(folder, pack):
    """A folder that holds only the compiled pack, as stage.py compile writes it; enough for the GEN checks."""
    prompts = Path(folder) / MACHINE / "prompts"
    prompts.mkdir(parents=True, exist_ok=True)
    (prompts / "SC10 - compiled.json").write_text(json.dumps(pack, indent=1), encoding="utf-8")
    return Project(folder, SCHEMA, WORDS)


def own_lines(result):
    return [problem for problem in result.problems if getattr(problem, "check_id", "").split("-")[0] in OWN_FAMILIES]


def run_own(files, story, step=None, project=None, check_ids=None):
    return run_checks(files, SCHEMA, WORDS, CONSTANTS, story=story, step=step, project=project,
                      check_ids=OWN_CHECKS if check_ids is None and step is None else check_ids)


# ---------------------------------------------------------------- the groups

def check_registry():
    families = load_check_families()
    wrong = []
    for check_id, level in LEVELS_7_2.items():
        definition = REGISTRY.get(check_id)
        if definition is None:
            wrong.append(f"{check_id} not registered")
            continue
        build = 2 if check_id in BUILD_TWO else 1
        if definition.level != level or definition.build != build:
            wrong.append(f"{check_id} registered as {definition.level}, build {definition.build}")
        if not definition.plain or re.search(r"[A-Z]{2,}-\d|\bSC\d", definition.plain):
            wrong.append(f"{check_id} has no plain sentence, or one with a code in it")
        module = "film_pass" if check_id.startswith("FILM") else "checks_plan_generation_film"
        if not definition.module.endswith(module):
            wrong.append(f"{check_id} comes from {definition.module}")
    extra = [check_id for check_id, definition in REGISTRY.items()
             if definition.family in OWN_FAMILIES and check_id not in LEVELS_7_2]
    wrong += [f"{check_id} is not a check of 7.2" for check_id in extra]
    report(not wrong, "registry: PLAN-01 to 05, GEN-01 to 17 and FILM-01 to 12 registered with 7.2's level and build, "
           "each with a plain sentence", "; ".join(wrong) or f"{len(LEVELS_7_2)} checks")
    notes = []
    for name in ("checks_plan_generation_film.py", "film_pass.py"):
        text = (TOOLS / "stage_tools" / name).read_text(encoding="utf-8").lstrip()
        if not text.startswith(f'"""{name}:'):
            notes.append(name)
    report(not notes, "both modules start with a plain note saying what they do", ", ".join(notes) or "yes")
    name = "stage_tools.checks_plan_generation_film"
    report(name not in families["missing"] and name not in families["broken"],
           "check_records loads the family module under its planned name (and through it film_pass)",
           families["broken"].get(name, "loaded"))


def check_gold(whole_story):
    files = parse_texts(gold_texts())
    stories = [("the scene 10 excerpt", EXCERPT), ("no story", None)]
    if whole_story:
        stories.insert(1, ("the whole story", Path(whole_story)))
    for facts_name, facts in (("the stand-in model facts", stand_in_facts()), ("the adapter files", None),
                              ("no model facts", "hidden")):
        if facts == "hidden":
            without_adapter_files()
        else:
            generation.use_model_facts(facts)
        for story_name, path in stories:
            story = story_from(path)
            if path is not None and story is None:
                info(f"gold with {story_name}: skipped: story not present")
                continue
            for step in (None, 2, 9, 10):
                result = run_own(files, story, step=step)
                found = own_lines(result)
                where = "check --all" if step is None else f"check --step {step}"
                ran = [check_id for check_id in result.checks_run if check_id.split("-")[0] in OWN_FAMILIES]
                detail = "; ".join(str(problem) for problem in found[:3]) or f"{len(ran)} of these checks run, no line"
                crashed = {key: value for key, value in result.crashed.items() if key.split("-")[0] in OWN_FAMILIES}
                if crashed:
                    detail += f"; crashed: {crashed}"
                expected = len(OWN_CHECKS) if step in (None, 10) else (5 if step == 2 else 12)
                report(not found and not crashed and len(ran) == expected,
                       f"gold with {story_name} and {facts_name}, {where}: every PLAN, GEN and FILM check is silent",
                       detail)
    without_adapter_files()
    story = story_from(EXCERPT)
    result = run_own(files, story)
    generation.use_model_facts(None)
    skipped = dict(result.skipped)
    whole = [check_id for check_id in ("FILM-01", "FILM-12", "PLAN-04") if "not in the excerpt" in skipped.get(check_id, "")]
    facts = [check_id for check_id in ("GEN-10",) if "model facts" in skipped.get(check_id, "")]
    packs = [check_id for check_id in ("GEN-01", "GEN-04", "GEN-12") if "no compiled prompts" in skipped.get(check_id, "")]
    report(len(whole) == 3 and facts and len(packs) == 3,
           "gold: the whole-film checks skip as 'not in the excerpt'; with the adapter files hidden GEN-10 waits "
           "for the model facts; the prompt checks say no prompts are compiled yet",
           f"{whole}; {facts}; {packs}")


def check_chat_copy():
    if not CHAT_FOLDER.is_dir():
        info("the chat-saved copy of scene 10 is missing: skipped")
        return
    files = [parse_text(path.read_text(encoding="utf-8"), str(path.relative_to(CHAT_FOLDER)).replace(os.sep, "/"),
                        SCHEMA) for path in sorted(CHAT_FOLDER.rglob("*.md"))]
    generation.use_model_facts(stand_in_facts())
    try:
        for story_name, path in (("the excerpt", EXCERPT), ("no story", None)):
            story = story_from(path)
            if path is not None and story is None:
                info("the chat-saved copy with the excerpt: skipped: story not present")
                continue
            for step in (None, 9):
                result = run_own(files, story, step=step)
                found = own_lines(result)
                report(not found and not result.crashed,
                       f"the chat-saved copy of scene 10 (quote anchors, two batch files) with {story_name}, "
                       f"{'check --all' if step is None else 'check --step 9'}: silent",
                       "; ".join(str(problem) for problem in found[:3]) or f"{len(result.checks_run)} checks run, no line")
    finally:
        generation.use_model_facts(None)


def check_clean_pack():
    temporary = Path(tempfile.mkdtemp(prefix="stage wp4e "))
    try:
        project = project_with_pack(temporary / "pack", clean_pack())
        files = parse_texts(gold_texts())
        story = story_from(EXCERPT)
        generation.use_model_facts(stand_in_facts())
        gen = [check_id for check_id in OWN_CHECKS if check_id.startswith("GEN")]
        result = run_own(files, story, project=project, check_ids=gen)
        found = own_lines(result)
        not_run = sorted(check_id for check_id, why in result.skipped
                         if check_id in gen and "no compiled prompts" in why)
        report(not found and not result.crashed and not not_run,
               "a clean compiled pack of scene 10 (Seedance with a start picture, Kling and Veo speaker forms) with "
               "the stand-in model facts: every GEN check is silent",
               "; ".join(str(problem) for problem in found[:3]) or
               f"{len(result.checks_run)} checks read 3 clips, no line" + (f"; not run: {not_run}" if not_run else ""))
        without_adapter_files()
        result = run_own(files, story, project=project, check_ids=gen)
        generation.use_model_facts(None)
        waiting = sorted(check_id for check_id, why in result.skipped if "model facts" in why)
        report(waiting == sorted(NEEDS_FACTS) and not own_lines(result),
               "without _config/adapters/*.json the GEN checks that need model facts skip and say so; the others still read "
               "the pack", ", ".join(waiting))
        pack = apply_pack_edit(clean_pack(), {"clip": "SC10-SH170.1", "set": {"length_s": 17}})
        generation.use_model_facts(stand_in_facts())
        from stage_tools.check_records import CheckRun
        run = CheckRun(files, SCHEMA, WORDS, CONSTANTS, story=story)
        lines = [line for line in generation.lint_packs(run, [pack], forced=True) if line.check_id == "GEN-02"]
        report(len(lines) == 1 and lines[0].level == "N",
               "lint_packs, for stage.py compile --force-model: GEN-02 comes out as a note",
               str(lines[0]) if lines else "no line")
    finally:
        generation.use_model_facts(None)
        shutil.rmtree(temporary, ignore_errors=True)


def run_fault(fault, temporary):
    texts = gold_texts()
    for edit in fault.get("edits", []):
        texts = apply_edit(texts, edit)
    story = None if fault.get("story") == "none" else story_from(EXCERPT)
    project = None
    if fault.get("pack") != "none" and (fault.get("pack_edits") or fault["check"].startswith("GEN")):
        pack = clean_pack()
        for edit in fault.get("pack_edits", []):
            pack = apply_pack_edit(pack, edit)
        folder = Path(tempfile.mkdtemp(prefix="fault ", dir=temporary))
        project = project_with_pack(folder, pack)
    generation.use_model_facts(stand_in_facts())
    try:
        return run_own(parse_texts(texts), story, project=project)
    finally:
        generation.use_model_facts(None)


def check_faults():
    faults = json.loads(FAULTS_FILE.read_text(encoding="utf-8"))["faults"]
    temporary = Path(tempfile.mkdtemp(prefix="stage wp4e "))
    fired = {}
    try:
        for fault in faults:
            result = run_fault(fault, temporary)
            label = f"{fault['check']}{' (build 2)' if fault.get('build') == 2 else ''} fires on its faulty fixture " \
                    f"({fault['about']})"
            if result.crashed:
                report(False, label, f"crashed: {result.crashed}")
                continue
            candidates = [problem for problem in result.problems if problem.check_id == fault["check"]]
            matching = [problem for problem in candidates
                        if problem.record == fault["record"] and problem.field_name == fault["field"]
                        and problem.level == fault["level"] and fault.get("holds", "") in str(problem)]
            wrong = []
            if not matching:
                wrong.append("no matching line; got: " + ("; ".join(str(problem) for problem in candidates[:3])
                                                          or "no line of this check"))
            else:
                line = str(matching[0])
                if LINE_FORM.match(line) is None or "\n" in line:
                    wrong.append(f"not in 7.2's form: {line}")
                if not (matching[0].file_name and matching[0].line_number):
                    wrong.append(f"not placed in a file and line: {line}")
            if not wrong:
                fired.setdefault(fault["check"], []).append(fault["about"])
            report(not wrong, label, "; ".join(wrong) or str(matching[0]))
    finally:
        shutil.rmtree(temporary, ignore_errors=True)
    build_one = [check_id for check_id in LEVELS_7_2 if check_id not in BUILD_TWO]
    missing = [check_id for check_id in build_one if check_id not in fired]
    missing_two = [check_id for check_id in sorted(BUILD_TWO) if check_id not in fired]
    report(not missing and not missing_two,
           "every PLAN, GEN and FILM check (build 1, and the build-2 ones) fires on at least one faulty fixture",
           f"missing: {', '.join(missing + missing_two)}" if missing or missing_two else
           f"{sum(len(found) for found in fired.values())} faulty fixtures fired for {len(fired)} checks")


# ---------------------------------------------------------------- the command, on a project made from the gold

def stage(arguments, cwd):
    environment = dict(os.environ)
    environment["STAGE_LOCK_WAIT_SECONDS"] = "2"
    completed = subprocess.run([sys.executable, str(STAGE)] + arguments, capture_output=True, text=True,
                               encoding="utf-8", cwd=str(cwd), env=environment, timeout=300)
    return completed.returncode, completed.stdout + completed.stderr


def make_gold_project(folder, texts):
    """A project folder from the gold: the scene file as 11 Scenes/Scene 10 - Saye's kitchen.md and each '## From
    NN <name>' part of the context file as the numbered file it came from."""
    (folder / "11 Scenes").mkdir(parents=True)
    (folder / "11 Scenes" / "Scene 10 - Saye's kitchen.md").write_text(texts["scene"], encoding="utf-8")
    sections = {}
    current = None
    for line in texts["context"].splitlines():
        match = re.match(r"^## From (\d\d .+)$", line)
        if match:
            current = match.group(1).strip()
            sections[current] = []
            continue
        if line.startswith("END OF FILE"):
            current = None
            continue
        if current is not None:
            sections[current].append(line)
    for name, lines in sections.items():
        count = sum(1 for line in lines if line.startswith("### "))
        text = "\n".join([f"# {name[3:]}", "", "The records scene 10 uses from this file (made from the gold example "
                          "for a test).", "", DIVIDER_LINE, ""] + lines).rstrip("\n")
        text += f"\n\nEND OF FILE | {name[3:]} | {count} records\n"
        (folder / f"{name}.md").write_text(text, encoding="utf-8")


def plain_part(text):
    return text.split(DIVIDER_LINE, 1)[0]


def check_command():
    if not EXCERPT.is_file():
        info("stage.py check --film on a project made from the gold: skipped: story not present")
        return
    temporary = Path(tempfile.mkdtemp(prefix="stage wp4e "))
    try:
        project = temporary / "The Catch"
        make_gold_project(project, gold_texts())
        code, output = stage(["check", "--film", "--story", str(EXCERPT)], project)
        own = [line for line in output.splitlines() if re.match(r"^[EWN] (PLAN|GEN|FILM)-\d\d ", line)]
        strip = project / MACHINE / "film strip.txt"
        whole = project / "12 Whole-film check.md"
        strip_lines = [line for line in strip.read_text(encoding="utf-8").splitlines()
                       if re.match(r"^SC10-SH\d{3} \| ", line)] if strip.is_file() else []
        whole_text = whole.read_text(encoding="utf-8") if whole.is_file() else ""
        health = (project / "13 Health check.md").read_text(encoding="utf-8")
        wanted = "SC10-SH150 | SC10-B07, SC10-B08 | turn | close_up | 50 | static | none | MO-MINT 2 | 15 | 6"
        good = (code == 0 and not own and len(strip_lines) == 21 and wanted in strip_lines
                and "SC10-SH080 | SC10-B04 | must_keep | medium | 85 | static | RC-01" in strip.read_text(encoding="utf-8")
                and DIVIDER_LINE in whole_text and "END OF FILE | Whole-film check | 0 records" in whole_text
                and "## The whole film" in plain_part(health))
        report(good, "stage.py check --film on a project made from the gold: exit 0, no PLAN, GEN or FILM line, the "
               "film strip written with one line per shot (shot 150 as step 9's example), 12 Whole-film check with its "
               "plain part, divider and END line, and 'The whole film' in 13 Health check",
               f"exit {code}; {len(strip_lines)} strip lines; {own[:2]}")
        codes = CODE_IN_PLAIN.findall(plain_part(whole_text)) + CODE_IN_PLAIN.findall(plain_part(health))
        report(not codes, "the plain parts of 12 Whole-film check and 13 Health check hold no check ID or record ID",
               ", ".join(codes[:5]) or "none")

        faulty = temporary / "Faulty"
        texts = apply_edit(gold_texts(), {"file": "scene", "record": "SHOT SC10-SH200", "find": "- angle: eye_level",
                                          "replace": "- angle: low"})
        make_gold_project(faulty, texts)
        code, output = stage(["check", "--film", "--story", str(EXCERPT)], faulty)
        whole = faulty / "12 Whole-film check.md"
        record_file = parse_file(whole, whole.name, SCHEMA) if whole.is_file() else None
        findings = [record for record in (record_file.records if record_file else []) if record.type_name == "FINDING"]
        first = findings[0] if findings else None
        good = (code == 1 and len(findings) == 1 and first.identifier == "FIND-001" and first.get("rule") == "FILM-03"
                and first.get("record") == "SC10-SH200" and first.get("source") == "checker"
                and first.get("status") == "open" and "END OF FILE | Whole-film check | 1 records" in whole.read_text(encoding="utf-8"))
        report(good, "check --film with shot 200 at a low angle on Saye: exit 1 and one FINDING (FIND-001, FILM-03, "
               "source checker, open) in 12 Whole-film check", f"exit {code}; " + "; ".join(
                   f"{record.identifier} {record.get('rule')} {record.get('record')} {record.get('status')}"
                   for record in findings))
        code, output = stage(["check", "--film", "--story", str(EXCERPT)], faulty)
        again = [record for record in parse_file(whole, whole.name, SCHEMA).records if record.type_name == "FINDING"]
        start_here = (faulty / "00 Start here.md").read_text(encoding="utf-8")
        entries = start_here.count("Film pass: wrote 1 new finding")
        report(code == 1 and len(again) == 1 and entries == 1,
               "check --film again: the finding keeps its number and no duplicate is written; one log entry in "
               "00 Start here", f"exit {code}; {len(again)} findings; {entries} log entries")
        code, output = stage(["check", "--all", "--story", str(EXCERPT)], faulty)
        about = [line for line in output.splitlines() if "12 Whole-film check" in line and re.match(r"^[EW] ", line)]
        report(not about, "check --all finds nothing wrong with the 12 Whole-film check it wrote (grammar, IDs, "
               "writers, required fields)", "; ".join(about[:3]) or f"exit {code}")
    finally:
        shutil.rmtree(temporary, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Acceptance test of work package 4e (the PLAN, GEN and FILM checks).")
    parser.add_argument("--story", help="The Catch, the whole story (optional): the gold is also checked against it")
    arguments = parser.parse_args()
    if not EXCERPT.is_file():
        info("the scene 10 excerpt is missing: skipped: story not present (the story groups)")
    info("the GEN faults use STAND-IN model facts (tests/fixtures/plan generation and film/stand-in model facts.json), "
         "so they do not move when the dated adapter files change")
    check_registry()
    check_gold(arguments.story)
    check_chat_copy()
    check_clean_pack()
    check_faults()
    check_command()
    failures = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failures else 'FAIL'} ({failures} failing groups)")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
