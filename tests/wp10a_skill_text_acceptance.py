"""Acceptance test for work package 10a: SKILL.md and reference/05, 06 and 07 (the skill's house rules,
the quality rubric, the checks in words, and the report and message formats).

What it checks, in plain words:
1. SKILL.md: front matter with name breaking-down-stories and a third-person description under 1,024
   characters; under 500 lines and under 4,500 words (counted both as English words and as every
   whitespace-separated token); the required sections of blueprint 2.3; the ten principles; the run command
   sentence; the loop; a step table that names all 17 step files with the user's step numbers from
   schema/steps.json; every command of blueprint 7.1, in order, each with its "if you cannot run code" twin;
   every stage.py command named anywhere in the four files exists; the privacy rules.
2. reference/05: the ten criteria of blueprint 11.3 with their names, how each is measured and what 2 and 3
   mean; the four anchors; the pass rule.
3. reference/06: part 1 lists exactly the 14 in-reply checks of schema/steps.json (in the template table and
   in the how-to table), part 2 exactly the 20 check-chat checks; the numbers table matches
   rules/constants.json; the shot 150 worked floor adds up.
4. reference/07: WORDS-02 (retired words) and WORDS-04 (abbreviations and internal codes) clean on the whole
   file, as blueprint 7.2 requires; every checkpoint shape named by what it is; the four-part ending; the
   welcome's rights question; the command list of blueprint 13.4.
5. All four files: every check ID exists in blueprint 7.2; every backticked constant-like name exists in
   rules/constants.json, rules/limits.json or schema/schema.json; every research citation (B3 R26, D7 §5.2)
   points to a real rule or section of the library's full file; no email address.

Run from anywhere:
    python tests/wp10a_skill_text_acceptance.py [--blueprint <path to blueprint.md>]
Without the blueprint it uses the lists stored at the end of this file. Standard library only.
"""

import argparse
import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
LIBRARY = SKILL / "library"
FILES = {
    "skill": SKILL / "SKILL.md",
    "rubric": SKILL / "reference" / "05 Quality rubric.md",
    "checks": SKILL / "reference" / "06 Checks in words.md",
    "messages": SKILL / "reference" / "07 Report and message formats.md",
}

results = []


def report(passed, group, detail):
    results.append((passed, group, detail))
    print(("PASS  " if passed else "FAIL  ") + group + (": " + detail if detail else ""))


def info(line):
    print("INFO  " + line)


def english_words(text):
    return [token for token in re.findall(r"\S+", text) if re.search(r"[A-Za-z0-9]", token)]


def section(text, heading):
    """The text of one '## ' section, up to the next '## ' heading."""
    match = re.search(r"(?m)^## " + re.escape(heading) + r".*$", text)
    if not match:
        return None
    rest = text[match.end():]
    following = re.search(r"(?m)^## ", rest)
    return rest[: following.start()] if following else rest


def table_rows(text):
    rows = []
    for line in text.splitlines():
        if line.startswith("|") and not re.match(r"^\|[-| ]+\|$", line):
            cells = re.split(r"(?<!\\)\|", line.strip()[1:-1])
            rows.append([cell.strip() for cell in cells])
    return rows


# ---------------------------------------------------------------- lists from the blueprint (or the snapshot)

def lists_from_blueprint(path):
    text = Path(path).read_text(encoding="utf-8")
    commands_part = text[text.index("**Commands**"): text.index("### 7.2")]
    commands = []
    for line in commands_part.splitlines():
        if line.startswith("| `"):
            first_cell = line.split("|")[1]
            commands.extend(re.findall(r"`([a-z][a-z-]*)", first_cell))
    checks_part = text[text.index("### 7.2"): text.index("### 7.3")]
    check_ids = re.findall(r"(?m)^\| \**([A-Z]+-\d\d)\**", checks_part)
    rubric_part = text[text.index("### 11.3"): text.index("### 11.4")]
    criteria = []
    for line in rubric_part.splitlines():
        if re.match(r"^\| \d+ \|", line):
            cells = [cell.strip() for cell in line.strip()[1:-1].split("|")]
            criteria.append(cells)
    return {"commands": commands, "check_ids": check_ids, "criteria": criteria}


def load_lists(blueprint):
    snapshot = SNAPSHOT
    if blueprint and Path(blueprint).exists():
        live = lists_from_blueprint(blueprint)
        info("lists read from the blueprint: " + str(blueprint))
        same = all(live[key] == snapshot[key] for key in snapshot)
        info("the blueprint's lists " + ("equal" if same else "DIFFER from") + " the stored snapshot")
        return live
    info("blueprint not given or not found: using the stored snapshot")
    return snapshot


# ---------------------------------------------------------------- shared data

def load_json(relative):
    return json.loads((SKILL / relative).read_text(encoding="utf-8"))


def all_constant_names():
    constants = load_json("rules/constants.json")
    names = set(constants["constants"]) | set(constants["from_blueprint_text"]["constants"])
    limits = load_json("rules/limits.json")
    names |= set(limits)
    schema = load_json("schema/schema.json")
    for record_type in schema["record_types"].values():
        for field in record_type["fields"]:
            names.add(field["name"])
            for sub_part in field.get("sub_parts", []) or []:
                names.add(sub_part["key"])
            for value in field.get("values", []) or []:
                if isinstance(value, str):
                    names.add(value)
    for field in schema.get("common_fields", []) or []:
        if isinstance(field, dict):
            names.add(field.get("name", ""))
    words = load_json("rules/words.json")
    names |= set(words)
    for record_type in schema["record_types"].values():
        for field in record_type["fields"]:
            names |= set(re.findall(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)+", str(field.get("example", ""))))
    return names


def constant_values():
    constants = load_json("rules/constants.json")
    values = {name: entry.get("value") for name, entry in constants["constants"].items()}
    values.update({name: entry.get("value") for name, entry in constants["from_blueprint_text"]["constants"].items()})
    return values


# ---------------------------------------------------------------- research citations

CODE = r"(?:A[1-4]|B[1-5]|C[1-5]|D1[0-8]|D[1-9])"
CITATION = re.compile(r"\b(" + CODE + r") (R\d+|§\d+(?:\.\d+)?|P\d+|Ex\d+)")
FOLLOW_ON = re.compile(r"\b(" + CODE + r") R\d+((?:, R\d+)+)")


def library_lines(code):
    matches = sorted(LIBRARY.glob(code + " *.md"))
    matches = [path for path in matches if not path.name.endswith("digest.md")]
    return matches[0].read_text(encoding="utf-8").split("\n") if matches else None


def resolve(code, token):
    lines = library_lines(code)
    if lines is None:
        return False
    if token.startswith("§"):
        number = token[1:]
        return any(re.match(r"^#+\s*(?:Section\s+)?" + re.escape(number) + r"(?:[.\s)]|$)", line) for line in lines)
    match = re.fullmatch(r"R(\d+)", token)
    if match:
        number = match.group(1)
        if any(re.search(r"^\s*[-*]?\s*\*\*R" + number + r"\.?\*\*|^R" + number + r"\. ", line) for line in lines):
            return True
        start = next((i for i, line in enumerate(lines) if re.match(r"^#{2,3} .*[Dd]ecision rules", line)), None)
        if start is None:
            return False
        end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
        return any(re.match(r"^\s*(?:[-*]\s*)?(?:\*\*)?" + number + r"\.\s", lines[i]) for i in range(start, end))
    match = re.fullmatch(r"(?:Ex)(\d+)", token)
    if match:
        return any(re.match(r"^#+ .*(?:Example|Ex\.?|Worked example)\s*" + match.group(1) + r"\b", line) for line in lines)
    return any(re.search(r"\*\*" + re.escape(token) + r"[.:]?\*\*|^#+ .*\b" + re.escape(token) + r"\b", line) for line in lines)


# ---------------------------------------------------------------- WORDS-02 and WORDS-04

def retired_word_hits(text, modes):
    words = load_json("rules/words.json")
    hits = []
    for entry in words["retired"]:
        if entry.get("flag") not in modes:
            continue
        word = entry["word"]
        if word in ("checkpoint letters",):
            pattern, flags = entry.get("pattern"), 0
        elif entry.get("pattern"):
            pattern = entry["pattern"]
            flags = 0 if entry.get("case_sensitive") else re.I
        else:
            pattern = r"(?<![A-Za-z_])" + re.escape(word) + r"(?![A-Za-z_])"
            flags = 0 if (entry.get("case_sensitive") or word != word.lower()) else re.I
        if word == "stage":
            pattern, flags = r"(?<![A-Za-z_])stage(?![A-Za-z_.])|(?<![A-Za-z_])stages(?![A-Za-z_])", 0
        for match in re.finditer(pattern, text, flags):
            hits.append((word, text[max(0, match.start() - 30): match.end() + 30].replace("\n", " ")))
    return hits


def words_04_hits(text):
    words = load_json("rules/words.json")
    abbreviations = words["abbreviations"]
    hits = []
    for word in abbreviations["words"]:
        pattern = r"(?<![A-Za-z0-9_.])" + re.escape(word) + (r"(?![A-Za-z0-9_])" if not word.endswith(".") else r"")
        for match in re.finditer(pattern, text):
            hits.append(("abbreviation " + word, text[max(0, match.start() - 30): match.end() + 30].replace("\n", " ")))
    for name, pattern in abbreviations["internal_code_patterns"].items():
        for match in re.finditer(pattern, text):
            hits.append((name, text[max(0, match.start() - 30): match.end() + 30].replace("\n", " ")))
    return hits


# ---------------------------------------------------------------- the checks

def check_skill(lists, steps):
    text = FILES["skill"].read_text(encoding="utf-8")
    lines = text.split("\n")
    front = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    ok = bool(front)
    detail = []
    if front:
        header = front.group(1)
        name = re.search(r"(?m)^name: (.+)$", header)
        description = re.search(r"(?m)^description: (.+)$", header)
        ok = bool(name and description and name.group(1).strip() == "breaking-down-stories")
        if description:
            value = description.group(1).strip()
            length = len(value)
            unquoted = re.sub(r'"[^"]*"', " ", value)
            first_person = re.findall(r"\b(I|I'm|I'll|me|my|you|your|we|our)\b", unquoted)
            yaml_safe = ": " not in value and " #" not in value and value[0] not in "\"'[{&*!|>%@`"
            ok = ok and length < 1024 and not first_person and value.startswith("Breaks down") and yaml_safe
            ok = ok and all(word in value for word in ("screenplays", "prose", "scene-by-scene", "shot plans", "AI"))
            detail.append(f"description {length} characters, third person: {not first_person}")
    report(ok, "SKILL.md front matter: name breaking-down-stories, third-person description under 1,024 characters", "; ".join(detail))

    body = text[front.end():] if front else text
    english = len(english_words(text))
    tokens = len(re.findall(r"\S+", text))
    report(len(lines) < 500 and english < 4500 and tokens < 4500, "SKILL.md size: under 500 lines and 4,500 words",
           f"{len(lines)} lines, {english} English words, {tokens} whitespace tokens")

    required = ["The ten principles", "How to talk to the user", "The loop", "The steps", "What the user may type",
                "Tools: one command", "Where things are", "Privacy"]
    missing = [heading for heading in required if section(body, heading) is None]
    report(not missing, "SKILL.md sections of blueprint 2.3", "missing: " + ", ".join(missing) if missing else "all 8 present")

    principles = section(body, "The ten principles") or ""
    numbers = re.findall(r"(?m)^(\d+)\. \*\*", principles)
    report(numbers == [str(n) for n in range(1, 11)], "SKILL.md: the ten principles, numbered, as instructions", f"{len(numbers)} found")

    run_sentence = "Run every tool as `python <this skill's folder>/tools/stage.py <command>`"
    report(run_sentence in body, "SKILL.md: the run command sentence", "")

    loop = section(body, "The loop") or ""
    loop_words = ["stage.py next", "stage.py handout", "one-line task back", "inbox", "stage.py apply", "stage.py check",
                  "repair_rounds_max", "Report", "chat without code", "copy box", "Checked in words", "check chat"]
    absent = [word for word in loop_words if word not in loop]
    report(not absent, "SKILL.md: the loop (next, handout, quote the task, write, apply, check, fix, report; and in chat)",
           "missing: " + ", ".join(absent) if absent else "")

    step_rows = table_rows(section(body, "The steps") or "")[1:]
    problems = []
    by_file = {row[2].strip("`"): row for row in step_rows if len(row) >= 5}
    for step in steps["steps"]:
        row = by_file.get(step["step_file"])
        if row is None:
            problems.append("no row for " + step["step_file"])
            continue
        if step["user_number"] is not None and not row[1].startswith(f"step {step['user_number']} of 12"):
            problems.append(f"{step['step_file']} user count '{row[1]}'")
        if not row[3] or not row[4]:
            problems.append(step["step_file"] + " has an empty cell")
    report(not problems and len(step_rows) == 17, "SKILL.md: step table names all 17 step files with the user's count",
           "; ".join(problems) if problems else f"{len(step_rows)} rows")

    tools_rows = table_rows(section(body, "Tools: one command") or "")[1:]
    table_commands = []
    empty_twins = []
    for row in tools_rows:
        names = re.findall(r"`([a-z][a-z-]*)", row[0])
        table_commands.extend(names)
        if len(row) < 3 or not row[2]:
            empty_twins.append(row[0])
    report(table_commands == lists["commands"] and not empty_twins,
           "SKILL.md: every command of blueprint 7.1, in order, with its 'if you cannot run code' twin",
           f"{len(table_commands)} commands" + ("; no twin: " + ", ".join(empty_twins) if empty_twins else ""))
    check_commands_against_stage_py(tools_rows)

    privacy = section(body, "Privacy") or ""
    needed = ["training", "personal information", "email", "commit it to a repository", "memory", "study_only"]
    absent = [word for word in needed if word not in privacy]
    report(not absent, "SKILL.md: privacy rules", "missing: " + ", ".join(absent) if absent else "")

    quote = re.findall(r"(?m)^> (.*)$", body)
    hits = retired_word_hits("\n".join(quote), ("always", "user_text")) + words_04_hits("\n".join(quote))
    report(not hits, "SKILL.md: the example message is WORDS-02 and WORDS-04 clean", "; ".join(f"{a}: {b}" for a, b in hits))


def check_commands_against_stage_py(tools_rows):
    """Every command in the table is one stage.py knows (built, or planned in its PLANNED_COMMANDS list); for the
    commands already built, every --option the table names is one the command accepts (its --help)."""
    stage_py = SKILL / "tools" / "stage.py"
    tree = ast.parse(stage_py.read_text(encoding="utf-8"))
    planned = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(getattr(target, "id", "") == "PLANNED_COMMANDS" for target in node.targets):
            planned = set(ast.literal_eval(node.value))
    listing = subprocess.run([sys.executable, str(stage_py), "help"], capture_output=True, text=True).stdout
    built = set(re.findall(r"(?m)^  ([a-z][a-z-]*)\s", listing))
    unknown, bad_options = [], []
    for row in tools_rows:
        for name in re.findall(r"`([a-z][a-z-]*)", row[0]):
            if name not in planned and name not in built:
                unknown.append(name)
            if name in built:
                accepted = subprocess.run([sys.executable, str(stage_py), name, "--help"], capture_output=True, text=True).stdout
                for option in re.findall(r"(--[a-z][a-z-]*)", row[0]):
                    if option not in accepted:
                        bad_options.append(f"{name} {option}")
    report(not unknown and not bad_options, "SKILL.md: every command is one stage.py knows; built commands accept the options named",
           "; ".join(unknown + bad_options) or f"{len(built)} built now ({', '.join(sorted(built))}), the rest planned in stage.py")


def check_commands_named(lists):
    known = set(lists["commands"])
    unknown = []
    for key, path in FILES.items():
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"stage\.py ([a-z][a-z-]*)", text):
            if match.group(1) not in known:
                unknown.append(f"{path.name}: {match.group(1)}")
    report(not unknown, "every stage.py command named in the four files exists in blueprint 7.1", "; ".join(unknown))


def check_rubric(lists):
    text = FILES["rubric"].read_text(encoding="utf-8")
    rows = [row for row in table_rows(section(text, "The ten criteria") or "") if row and row[0].isdigit()]
    substitutions = [("80-94%", "80 to 94%"), ("budgets and reserve kept", "budgets and saved choices kept"),
                     ("within ±10%", "within `scene_total_tolerance`"), ("(film pass clean)", "(the film pass is clean)"),
                     ("`compile --lint-only` at step 10 reports", "`stage.py compile --lint-only` reports"),
                     ("a fresh AI unit", "a fresh unit"), (" (the user's part stays the 10-question review sheet)", "")]
    problems = []
    if len(rows) != 10:
        problems.append(f"{len(rows)} criteria rows")
    for expected, row in zip(lists["criteria"], rows):
        wanted = list(expected)
        for index in (3, 4):
            for old, new in substitutions:
                wanted[index] = wanted[index].replace(old, new)
        if row[:5] != wanted[:5]:
            problems.append(f"criterion {expected[0]}: {row[:5]} differs from {wanted[:5]}")
    report(not problems, "reference/05: the ten criteria of blueprint 11.3 (name, how, 2 means, 3 means)", "; ".join(problems))
    anchors = [row[0] for row in table_rows(section(text, "The anchors") or "")[1:]]
    report(anchors == ["0", "1", "2", "3"], "reference/05: the four anchors 0 to 3", "")
    rule = section(text, "The pass rule") or ""
    needed = ["no ERROR", "no criterion scores 0", "criteria 1, 3 and 6 score 2 or more", "20 or more of 30",
              "one line of evidence and a fix"]
    absent = [phrase for phrase in needed if phrase not in rule]
    report(not absent, "reference/05: the pass rule of 11.3", "missing: " + ", ".join(absent) if absent else "")


def check_checks_in_words(steps):
    text = FILES["checks"].read_text(encoding="utf-8")
    in_reply = steps["chat_checks"]["in_reply"]["checks"]
    check_chat = steps["chat_checks"]["check_chat"]["checks"]
    template = re.search(r"```\n(.*?)```", text, re.S).group(1)
    template_ids = re.findall(r"(?m)^\| ([A-Z]+-\d\d) \|", template)
    part1 = [row[0] for row in table_rows(section(text, "Part 1") or "")[1:]]
    part2 = [row[0] for row in table_rows(section(text, "Part 2") or "")[1:]]
    report(template_ids == in_reply and part1 == in_reply, "reference/06 part 1: exactly the 14 in-reply checks of steps.json",
           f"template {len(template_ids)}, how-to {len(part1)}")
    report(part2 == check_chat, "reference/06 part 2: exactly the 20 check-chat checks of steps.json", f"{len(part2)} rows")
    report("END OF FILE | " in template and "\n---\n" in template and "Checked in words: 14 of 14 passed." in template,
           "reference/06: the template has the --- line, the one line and the END line", "")

    values = constant_values()
    numbers_table = {row[0]: row[1] for row in table_rows(section(text, "Numbers this page uses") or "")[1:]}
    problems = []
    expectations = {
        "`speech_wps_default`": [values["speech_wps_default"]],
        "`speech_floor_extra_s`": [values["speech_floor_extra_s"]],
        "`text_floor`": [values["text_floor"]["minimum_s"], values["text_floor"]["base_s"],
                         values["text_floor"]["characters_per_second"], values["text_floor"]["plot_critical_emphasis_min"],
                         values["text_floor"]["plot_critical_base_s"], values["text_floor"]["plot_critical_per_word_s"],
                         values["text_floor"]["mirrored_factor"]],
        "`turn_reaction_min_s`": [values["turn_reaction_min_s"]],
        "`pause_tiers`": [values["pause_tiers"]["short"]["to_s"], values["pause_tiers"]["medium"]["to_s"],
                          values["pause_tiers"]["long"]["to_s"], values["pause_tiers"]["script_words"]["(beat)"]],
        "`long_pauses_per_scene_max`": [values["long_pauses_per_scene_max"]],
        "`push_in_per_scene_max`, `extreme_close_up_per_scene_max`": [values["push_in_per_scene_max"],
                                                                      values["extreme_close_up_per_scene_max"]],
        "`quote_anchor_words_min`": [values["quote_anchor_words_min"]],
        "`plant_inserts_per_scene_max`": [values["plant_inserts_per_scene_max"]],
        "`shot_number_step`, `end_card_numbers`": [values["shot_number_step"]] + list(values["end_card_numbers"]),
        "`issued_blocks`": list(values["issued_blocks"]["beats"]) + list(values["issued_blocks"]["shots"]),
    }
    for name, numbers in expectations.items():
        cell = numbers_table.get(name)
        if cell is None:
            problems.append("no row " + name)
            continue
        found = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", cell)]
        for number in numbers:
            if float(number) not in found:
                problems.append(f"{name} lacks {number}")
    extra = [name for name in numbers_table if name not in expectations]
    report(not problems and not extra, "reference/06: the numbers table matches rules/constants.json",
           "; ".join(problems + ["unexpected row " + e for e in extra]) or f"{len(numbers_table)} rows")

    speech = 19 / 2.0 + 2 / values["speech_wps_default"] + 3 * values["speech_floor_extra_s"]
    floor = speech + values["turn_reaction_min_s"]
    report(abs(speech - 11.8) < 0.05 and abs(floor - 13.8) < 0.05 and "the floor is 13.8 s" in text,
           "reference/06: the shot 150 floor adds up (11.8 s + 2.0 s = 13.8 s)", f"{speech:.1f} + {values['turn_reaction_min_s']}")


def check_messages(steps):
    text = FILES["messages"].read_text(encoding="utf-8")
    retired = retired_word_hits(text, ("always", "user_text"))
    report(not retired, "reference/07: WORDS-02 clean (retired words)", "; ".join(f"{a}: {b}" for a, b in retired))
    codes = words_04_hits(text)
    report(not codes, "reference/07: WORDS-04 clean (abbreviations and internal codes)", "; ".join(f"{a}: {b}" for a, b in codes))

    names = []
    for step in steps["steps"]:
        checkpoint = step.get("checkpoint") or {}
        if checkpoint.get("user_name"):
            names.append(checkpoint["user_name"])
    absent = [name for name in names if name.lower() not in text.lower()]
    report(not absent, "reference/07: every checkpoint named by what it is", "missing: " + ", ".join(absent) if absent else f"{len(names)} names")
    headings = ["Every reply's ending", "The welcome", "The scene list", "How the book becomes a film", "The big choices",
                "Each group of shots", "The finished check", "Add-ons", "Resuming", "When something goes wrong",
                "What the user can type", "00 Start here"]
    missing = [heading for heading in headings if section(text, heading) is None]
    report(not missing, "reference/07: sections for 13.2 to 13.7", "missing: " + ", ".join(missing) if missing else "")
    ending = section(text, "Every reply's ending") or ""
    order = [ending.find(part) for part in ("Done:", "Example from your story:", "Made:", "Needs you:", "Next:")]
    report(all(position >= 0 for position in order) and order == sorted(order) and "Save as:" in ending and "To continue later:" in ending,
           "reference/07: the four-part ending in order, then Next, and the chat lines", "")
    rights = steps["steps"][0]["checkpoint"]["question"]
    report(rights in text, "reference/07: the welcome asks the rights question with its default", "")
    typed = ["Break down my story.", "Continue my breakdown.", "Where are we?", "Why shot 150?", "Change ...",
             "Go deeper on scene 13", "Quick / Standard / Detailed", "Redo step 6", "Stop here", "Check", "continue", "next",
             "defaults", "Make storyboards", "Make grey previews", "Get it ready for AI video", "Plan the edit"]
    command_list = section(text, "What the user can type") or ""
    absent = [item for item in typed if item not in command_list]
    report(not absent, "reference/07: the plain-word command list of 13.4", "missing: " + ", ".join(absent) if absent else "")


def check_all_files(lists):
    known_checks = set(lists["check_ids"])
    known_names = all_constant_names()
    unknown_checks, unknown_names, bad_citations, emails = [], [], [], []
    citation_count = 0
    for path in FILES.values():
        text = path.read_text(encoding="utf-8")
        for check_id in re.findall(r"\b(?:FORM|ID|CITE|COVER|TIME|STATE|SIDE|GEOM|CRAFT|INFO|REASON|WORDS|PLAN|GEN|FILM)-\d\d\b", text):
            if check_id not in known_checks:
                unknown_checks.append(f"{path.name}: {check_id}")
        for name in re.findall(r"`([a-z][a-z0-9]*(?:_[a-z0-9]+)+)`", text):
            if name not in known_names:
                unknown_names.append(f"{path.name}: {name}")
        for code, token in CITATION.findall(text):
            citation_count += 1
            if not resolve(code, token):
                bad_citations.append(f"{path.name}: {code} {token}")
        for code, rest in FOLLOW_ON.findall(text):
            for token in re.findall(r"R\d+", rest):
                citation_count += 1
                if not resolve(code, token):
                    bad_citations.append(f"{path.name}: {code} {token}")
        emails += [f"{path.name}: {m}" for m in re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)]
    report(not unknown_checks, "every check ID in the four files exists in blueprint 7.2", "; ".join(unknown_checks))
    report(not unknown_names, "every backticked constant or field name exists in rules/ or the schema", "; ".join(sorted(set(unknown_names))))
    report(not bad_citations, "every research citation points to a real rule or section of the library",
           "; ".join(bad_citations) if bad_citations else f"{citation_count} citations")
    report(not emails, "no email address in the four files", "; ".join(emails))
    for key, path in FILES.items():
        text = path.read_text(encoding="utf-8")
        info(f"{path.name}: {len(english_words(text))} English words, {len(re.findall(chr(92) + 'S+', text))} tokens, {len(text.splitlines())} lines")


def main():
    parser = argparse.ArgumentParser(description="Acceptance test for SKILL.md and reference/05, 06, 07.")
    parser.add_argument("--blueprint", default=os.environ.get("STAGE_BLUEPRINT"))
    arguments = parser.parse_args()
    missing = [str(path) for path in FILES.values() if not path.exists()]
    if missing:
        print("FAIL  files missing: " + ", ".join(missing))
        return 1
    lists = load_lists(arguments.blueprint)
    steps = load_json("schema/steps.json")
    check_skill(lists, steps)
    check_commands_named(lists)
    check_rubric(lists)
    check_checks_in_words(steps)
    check_messages(steps)
    check_all_files(lists)
    failing = [group for passed, group, _ in results if not passed]
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({len(failing)} failing groups)")
    return 0 if not failing else 1


SNAPSHOT = {
    "commands": ["new", "selftest", "read", "adopt", "status", "next", "handout", "apply", "check", "build", "impact",
                 "questions", "estimate", "compile", "graphics", "previs", "export", "pack", "unpack", "lines", "lib",
                 "refresh-models", "import-json", "build-kit", "replay"],
    "check_ids": (["FORM-%02d" % n for n in range(1, 14)] + ["ID-%02d" % n for n in range(1, 10)]
                  + ["CITE-%02d" % n for n in range(1, 8)] + ["COVER-%02d" % n for n in range(1, 9)]
                  + ["TIME-%02d" % n for n in range(1, 11)] + ["STATE-%02d" % n for n in range(1, 5)]
                  + ["SIDE-%02d" % n for n in range(1, 6)] + ["GEOM-%02d" % n for n in range(1, 9)]
                  + ["CRAFT-%02d" % n for n in range(1, 27)] + ["INFO-%02d" % n for n in range(1, 3)]
                  + ["REASON-%02d" % n for n in range(1, 10)] + ["WORDS-%02d" % n for n in range(1, 6)]
                  + ["PLAN-%02d" % n for n in range(1, 6)] + ["GEN-%02d" % n for n in range(1, 18)]
                  + ["FILM-%02d" % n for n in range(1, 13)]),
    "criteria": [
        ["1", "Faithful to the story", "M", "every line covered; quotes exact; inventions labelled", "and every addition approved"],
        ["2", "Story reading (events, values, turns, climax)", "J, U", "80-94% of judge questions pass", "95% or more, and the user agrees on the sample"],
        ["3", "Shots serve beats", "M, J", "every purpose names a change; one turn shot per turn", "and turn shots are the scene's extremes and match their turn pictures"],
        ["4", "Reasons", "M, J", "every `why` anchored; no mood-only reason", "and no sampled reason fails the any-film test"],
        ["5", "Restraint and economy", "M", "budgets and reserve kept; plants quiet", "and no shot a cut could replace; no stacked signals"],
        ["6", "Continuity and sides", "M", "no state or side errors", "and every state has its reference plan"],
        ["7", "Rhythm and time", "M, J", "floors met; holds within budget; scene totals within ±10%", "and each scene's rhythm shape shows in its durations"],
        ["8", "Visual system", "M", "film rules followed; departures carry reasons", "and the ladder escalates and rhymes land (film pass clean)"],
        ["9", "Ready for generation", "M", "`compile --lint-only` at step 10 reports 0 GEN errors on the scene model", "and every hard case has its references and guide inputs listed"],
        ["10", "Readable for the user", "J, U", "plain part above the divider; no abbreviations; At a glance per scene", "and a fresh AI unit given only the scene's plain page answers 5 questions about the scene correctly (the user's part stays the 10-question review sheet)"],
    ],
}

if __name__ == "__main__":
    sys.exit(main())
