"""Project folders: make them, find their files, keep the manifest and the log, make and open save ZIPs,
and run the commands new, status, apply, pack and unpack (blueprint 2.6, 7.1, 7.3, 13.5, 13.7).

In plain words:
- find_project finds the project folder a command works on (7.1's rule), or stops with exit 2;
- Project knows the fixed file names per record type, loads every record file, and says which file a
  record belongs in (a scene's list fields in 04 Scene list.md, its design fields in its scene file);
- the manifest (For machines - do not edit/manifest.json) keeps fingerprints, locks, units done and the
  batches with their expected and received counts; log.jsonl gets one line per command; changes to
  records get a numbered entry in the log of 00 Start here.md;
- apply checks an inbox file the AI wrote (the FORM checks), tidies it, merges its records into the
  numbered files (keeping the old versions in history/), applies answered choices, and logs it;
- pack and unpack carry the whole project as one ZIP named "NNN Save - <title> - after <what>.zip";
- a lock file lets helper agents apply one unit at a time.

Standard library only.
"""

import datetime
import hashlib
import json
import os
import re
import shutil
import time
import zipfile
from pathlib import Path

from .checks_form import INBOX_CHECKS, ChoiceBook, FormContext, apply_tidy_fixes, resolve_field, run_form_checks
from .record_format import (DIVIDER_LINE, FieldLine, OtherLine, Record, TextBlock, add_record, ensure_end_line,
                            load_json, load_skill_data, merge_copies, new_record_file, normalise_word, parse_file,
                            split_item, split_list, write_file)

MACHINE_FOLDER = "For machines - do not edit"
START_HERE = "00 Start here.md"
CHOICES_FILE = "01 Choices.md"
SCENE_LIST_FILE = "04 Scene list.md"
SCENES_FOLDER = "11 Scenes"
ORIGINAL_FOLDER = "Original"
BREAKDOWNS_FOLDER = "My breakdowns"
LOCK_FILE = "apply.lock"
LOCK_WAIT_SECONDS = float(os.environ.get("STAGE_LOCK_WAIT_SECONDS", "60"))
LOCK_STALE_SECONDS = 600
PACK_LEFT_OUT = ("history", "handouts")
SCENE_TYPES = ("SCENE", "PART", "BEAT", "SPEECH", "MOVE", "SETUP", "SHOTLIST", "SHOT", "CUT")
SCENE_FILE_TYPE_ORDER = ["SCENE", "PART", "BEAT", "SPEECH", "MOVE", "SETUP", "SHOTLIST", "SHOT", "CUT"]
UNIT_PATTERN = re.compile(r"^U-(\d{2})-(.+)$")
SCENE_ID = re.compile(r"^(SC(\d{2,3})([A-Z]?))(?:-|$)")
UNSAFE_NAME_CHARACTERS = re.compile(r'[\\/:*?"<>|\x00-\x1f]')

# The files a new project lists in "Files in this folder" (2.6), each with one plain line.
FILES_IN_THIS_FOLDER = [
    ("00 Start here", "this file: where things stand, the next step, the big choices and the log"),
    ("01 Choices", "every question for you, each with its default; open ones first"),
    ("02 Whole-film summary", "a short summary of files 04 to 10 that later steps read"),
    ("03 Story - numbered", "your story with a number on every line"),
    ("04 Scene list", "one entry for each scene"),
    ("05 Story plan", "what changes in each scene, the groups of scenes, the climax, plants and payoffs"),
    ("06 World and style", "where and when the story happens and how the film looks"),
    ("07 Characters and voices", "each character's appearance and voice"),
    ("08 Places and things", "places with their floor plans, things, text in pictures, motifs"),
    ("09 Continuity", "what each person, thing and place looks like from scene to scene"),
    ("10 Film rules", "the camera, light, colour and sound rules for the whole film"),
    ("11 Scenes", "one file for each scene: how it turns and every shot"),
    ("12 Whole-film check", "the check of the film as a whole"),
    ("13 Health check", "the checker's report and the three scenes to read"),
    ("14 Time and cost", "how long the film runs and what making it costs"),
    ("15 The breakdown", "the readable book of the whole breakdown"),
    ("16 Spreadsheets", "the shot list and the list of people, places and things"),
    ("17 Captions and audio description", "captions and a script that describes the pictures"),
    ("18 Storyboard", "storyboard frames, if you ask for them"),
    ("19 Grey previews", "grey previews of hard shots, if you ask for them"),
    ("20 Prompts for AI video", "prompts for picture and video tools, if you ask for them"),
    ("21 Edit and finishing", "the edit plan and finishing jobs, if you ask for them"),
    ("22 Rights and credits", "rights, licences and the credit text"),
    ("Original", "your story exactly as you gave it, and its fingerprint"),
    (MACHINE_FOLDER, "files for the tools; you never need to open them"),
]


class StageStop(Exception):
    """A command cannot run (exit 2). The message is one plain line that says what to do."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


def today():
    return datetime.date.today().isoformat()


def now():
    return datetime.datetime.now().replace(microsecond=0).isoformat()


def fingerprint_of_bytes(data):
    return hashlib.sha256(data).hexdigest()


def fingerprint_of_file(path):
    with open(path, "rb") as handle:
        return fingerprint_of_bytes(handle.read())


def safe_file_name(name):
    """A file or folder name without characters file systems refuse."""
    cleaned = UNSAFE_NAME_CHARACTERS.sub("", name).strip().strip(".")
    return re.sub(r"\s+", " ", cleaned) or "Untitled"


def sentence_case(text):
    """'LOADING TUNNEL' becomes 'Loading tunnel'; text already in mixed case is kept."""
    text = text.strip()
    if text.upper() != text:
        return text
    lowered = text.lower()
    return lowered[:1].upper() + lowered[1:]


def title_case(text):
    """'THE CATCH' becomes 'The Catch' (apostrophes kept: SAYE'S becomes Saye's)."""
    words = []
    for word in text.split():
        words.append(word[:1].upper() + word[1:].lower() if word.upper() == word else word)
    return " ".join(words)


def scene_number_words(scene_identifier):
    """'SC10' becomes 'scene 10' for messages; 'SC06A' becomes 'scene 6A'."""
    match = SCENE_ID.match(scene_identifier or "")
    if not match:
        return scene_identifier
    return f"scene {int(match.group(2))}{match.group(3)}"


# ---------------------------------------------------------------- finding the project (7.1)

def repository_root(start):
    """The nearest folder at or above start that holds CLAUDE.md (the Stage repository), or None."""
    folder = Path(start).resolve()
    for candidate in [folder] + list(folder.parents):
        if (candidate / "CLAUDE.md").is_file():
            return candidate
    return None


def default_breakdowns_folder(start):
    """My breakdowns/ in the repository when there is one, else the start folder."""
    root = repository_root(start)
    if root is not None and (root / BREAKDOWNS_FOLDER).is_dir():
        return root / BREAKDOWNS_FOLDER
    return Path(start).resolve()


def is_project(folder):
    return (Path(folder) / START_HERE).is_file()


def find_project(explicit=None, start=None):
    """The project folder: --project; else the current folder; else its single project subfolder; else the single
    project in My breakdowns/ (found by walking up to the folder that holds CLAUDE.md). Stops with exit 2 otherwise."""
    start = Path(start or os.getcwd()).resolve()
    if explicit:
        folder = Path(explicit)
        if not folder.is_absolute():
            folder = start / folder
        if is_project(folder):
            return folder.resolve()
        raise StageStop(f'The folder "{explicit}" is not a project: it has no "{START_HERE}". '
                        "Give the folder of a project made with stage.py new.")
    if is_project(start):
        return start
    subfolders = sorted(child for child in start.iterdir() if child.is_dir() and is_project(child)) if start.is_dir() else []
    if len(subfolders) == 1:
        return subfolders[0]
    candidates = list(subfolders)
    if not subfolders:
        root = repository_root(start)
        if root is not None and (root / BREAKDOWNS_FOLDER).is_dir():
            candidates = sorted(child for child in (root / BREAKDOWNS_FOLDER).iterdir()
                                if child.is_dir() and is_project(child))
            if len(candidates) == 1:
                return candidates[0]
    if not candidates:
        raise StageStop("No project found here. Start one with: stage.py new \"<story file>\", "
                        "or give the project folder with --project \"<folder>\".")
    names = ", ".join(f'"{candidate.name}"' for candidate in candidates)
    raise StageStop(f"Several projects found ({names}). Choose one with --project \"<folder>\".")


# ---------------------------------------------------------------- a project and its files

class Project:
    """One project folder: its record files, manifest and log."""

    def __init__(self, folder, schema=None, words=None, skill_folder=None):
        self.folder = Path(folder).resolve()
        if schema is None or words is None:
            schema, words, _ = load_skill_data(skill_folder)
        self.schema = schema
        self.words = words
        self.skill_folder = skill_folder
        self.machine_folder = self.folder / MACHINE_FOLDER
        self._type_files = None

    # -- paths
    @property
    def manifest_path(self):
        return self.machine_folder / "manifest.json"

    @property
    def log_path(self):
        return self.machine_folder / "log.jsonl"

    @property
    def inbox_folder(self):
        return self.machine_folder / "inbox"

    @property
    def history_folder(self):
        return self.machine_folder / "history"

    def path_of(self, name):
        return self.folder / name

    # -- which file holds which record type (2.6, schema.json "files")
    def type_files(self):
        if self._type_files is None:
            mapping = {}
            for file_name, type_names in self.schema.data.get("files", {}).items():
                for type_name in type_names:
                    mapping.setdefault(type_name, []).append(file_name)
            self._type_files = mapping
        return self._type_files

    def record_file_names(self):
        """Every record file present in the project, as names relative to the project folder."""
        names = []
        for file_name in self.schema.data.get("files", {}):
            if "<" in file_name or file_name.startswith(MACHINE_FOLDER) or file_name.endswith(".json"):
                continue
            if (self.folder / file_name).is_file() and file_name not in names:
                names.append(file_name)
        scenes = self.folder / SCENES_FOLDER
        if scenes.is_dir():
            scene_files = sorted((path for path in scenes.glob("*.md") if path.is_file()),
                                 key=lambda path: [int(part) if part.isdigit() else part
                                                   for part in re.split(r"(\d+)", path.name)])
            names.extend(f"{SCENES_FOLDER}/{path.name}" for path in scene_files)
        return sorted(set(names), key=lambda name: (name[:2], name))

    def load_record_files(self):
        return [parse_file(self.folder / name, name, self.schema) for name in self.record_file_names()]

    def scene_file_name(self, scene_identifier, record_files, incoming=None):
        """The scene's file: the one already there, else 'Scene NN - <place>.md' named from its place (the title of
        its LOCATION record, else the last part of its heading's place words). incoming is a SCENE record not yet
        merged (apply), read when the stored records do not name the place."""
        match = SCENE_ID.match(scene_identifier)
        number = (match.group(2) + match.group(3)) if match else scene_identifier
        prefix = f"{SCENES_FOLDER}/Scene {number}"
        for record_file in record_files:
            if record_file.name.startswith(prefix + " - ") or record_file.name == prefix + ".md":
                if " - shots " not in record_file.name:
                    return record_file.name
        merged, _ = merge_copies(record_files, self.schema)
        scene = merged.get(("SCENE", scene_identifier))
        sources = [record for record in (scene, incoming) if record is not None]
        location_identifier = next((record.get("location") for record in sources if record.get("location")), "")
        place_text = next((record.get("place_text") for record in sources if record.get("place_text")), "")
        place = ""
        location = merged.get(("LOCATION", location_identifier))
        if location is not None and location.title:
            place = location.title
        elif place_text:
            place = sentence_case(place_text.split(" - ")[-1])
        place = safe_file_name(place) if place else ""
        return f"{prefix} - {place}.md" if place else f"{prefix}.md"

    def target_file_for(self, record, record_files):
        """The numbered file a new record of this type goes into."""
        type_name = record.type_name
        if type_name in SCENE_TYPES and type_name != "SCENE":
            match = SCENE_ID.match(record.identifier or "")
            if match:
                return self.scene_file_name(match.group(1), record_files)
        if type_name == "PIC":
            use = normalise_word(record.get("use") or "")
            return "18 Storyboard/Storyboard frames.md" if use == "storyboard" else "20 Prompts for AI video/Pictures.md"
        files = [name for name in self.type_files().get(type_name, []) if "<" not in name and not name.endswith(".json")]
        return files[0] if files else None

    def type_order_for(self, file_name):
        if file_name.startswith(SCENES_FOLDER + "/"):
            return SCENE_FILE_TYPE_ORDER
        return list(self.schema.data.get("files", {}).get(file_name, []))

    # -- the manifest
    def read_manifest(self):
        if self.manifest_path.is_file():
            with open(self.manifest_path, encoding="utf-8") as handle:
                return json.load(handle)
        return {"manifest_version": 1, "files": {}, "locks": [], "units_done": [], "batches": {}}

    def write_manifest(self, manifest):
        self.machine_folder.mkdir(parents=True, exist_ok=True)
        temporary = self.manifest_path.with_suffix(".json.part")
        with open(temporary, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle, indent=1, ensure_ascii=False)
            handle.write("\n")
        os.replace(temporary, self.manifest_path)

    def refresh_manifest(self, manifest, record_files=None):
        """Fingerprints and record counts of every record file, and the IDs of locked records."""
        record_files = record_files if record_files is not None else self.load_record_files()
        files = {}
        locks = []
        for record_file in record_files:
            path = self.folder / record_file.name
            if path.is_file():
                files[record_file.name] = {"fingerprint": fingerprint_of_file(path),
                                           "records": len(record_file.records)}
            for record in record_file.records:
                if normalise_word(record.get("locked") or "") == "yes":
                    label = record.identifier or record.type_name
                    if label not in locks:
                        locks.append(label)
        manifest["files"] = files
        manifest["locks"] = locks
        return manifest

    # -- the logs
    def log_command(self, command, arguments, exit_code, summary=""):
        """One line in log.jsonl for every command (7.3). Paths are logged by file name only (privacy)."""
        self.machine_folder.mkdir(parents=True, exist_ok=True)
        entry = {"time": now(), "command": command, "arguments": arguments, "exit_code": exit_code}
        if summary:
            entry["summary"] = summary
        with open(self.log_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def log_entry_numbers(self):
        path = self.folder / START_HERE
        if not path.is_file():
            return []
        record_file = parse_file(path, START_HERE, self.schema)
        numbers = []
        in_log = False
        for _, line in record_file.text_lines:
            if line.strip().lower().startswith("## log"):
                in_log = True
                continue
            if in_log and line.startswith("#"):
                in_log = False
            if in_log:
                match = re.match(r"^(\d{3,})\s", line)
                if match:
                    numbers.append(int(match.group(1)))
        return numbers

    def add_log_entry(self, text):
        """A numbered, dated entry at the end of the Log section of 00 Start here (13.7). Returns its number."""
        path = self.folder / START_HERE
        record_file = parse_file(path, START_HERE, self.schema)
        numbers = self.log_entry_numbers()
        number = (max(numbers) if numbers else 0) + 1
        entry = f"{number:03d} {today()} {text}"
        blocks = [segment for segment in record_file.segments if isinstance(segment, TextBlock)]
        for block in blocks:
            lines = block.lines
            heading = next((index for index, line in enumerate(lines) if line.strip().lower().startswith("## log")), None)
            if heading is None:
                continue
            insert_at = heading + 1
            scan = heading + 1
            while scan < len(lines) and not lines[scan].startswith("#") and lines[scan].strip() != DIVIDER_LINE:
                if re.match(r"^\d{3,}\s", lines[scan]):
                    insert_at = scan + 1
                scan += 1
            lines.insert(insert_at, entry)
            block.line_numbers.insert(insert_at, None)
            break
        else:
            for block in blocks:
                divider = next((index for index, line in enumerate(block.lines) if line.strip() == DIVIDER_LINE), None)
                if divider is not None:
                    block.lines[divider:divider] = ["## Log", entry, ""]
                    block.line_numbers[divider:divider] = [None, None, None]
                    break
        write_file(record_file, path, self.schema)
        return number

    # -- the lock for helpers working in parallel
    def lock(self):
        return ProjectLock(self.machine_folder / LOCK_FILE)


class ProjectLock:
    """A lock file so that helper agents apply one unit at a time (7.1). Waits, then stops with exit 2."""

    def __init__(self, path):
        self.path = Path(path)

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        waited = 0.0
        while True:
            try:
                handle = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                with os.fdopen(handle, "w") as file:
                    file.write(f"{os.getpid()} {now()}\n")
                return self
            except FileExistsError:
                try:
                    age = time.time() - self.path.stat().st_mtime
                except FileNotFoundError:
                    continue
                if age > LOCK_STALE_SECONDS:
                    try:
                        self.path.unlink()
                    except FileNotFoundError:
                        pass
                    continue
                if waited >= LOCK_WAIT_SECONDS:
                    raise StageStop("Another helper is applying records to this project. Try again in a minute.")
                time.sleep(0.5)
                waited += 0.5

    def __exit__(self, *exception):
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass
        return False


# ---------------------------------------------------------------- the files a new project starts with

def guess_title(story_path, text):
    """A title for the project: the first '= ' title-page line, else the first '# ' heading, else the file name."""
    for line in text.splitlines()[:40]:
        stripped = line.strip()
        if stripped.startswith("= ") and stripped[2:].strip():
            return title_case(stripped[2:].strip())
        if stripped.startswith("# ") and stripped[2:].strip():
            heading = re.sub(r"^\d+\s+", "", stripped[2:].strip())
            return heading.split(" - ")[0].strip() or heading
    stem = Path(story_path).stem
    stem = re.sub(r"^[0-9a-f]{6,}-\d+_", "", stem)
    return re.sub(r"[_]+", " ", stem).strip() or "Untitled"


def project_identifier(title):
    """The project ID (5.3: 3 to 8 capitals) from the title's first word that is not an article."""
    words = [re.sub(r"[^A-Za-z]", "", word).upper() for word in title.split()]
    words = [word for word in words if word]
    meaningful = [word for word in words if word not in ("THE", "A", "AN")] or words or ["STORY"]
    identifier = meaningful[0][:8]
    if len(identifier) < 3:
        identifier = ("".join(meaningful))[:8]
    if len(identifier) < 3:
        identifier = (identifier + "PRJ")[:3]
    return identifier


def detect_surface():
    """Which app the code runs in, as far as the environment shows; the self-test records it properly later."""
    if os.environ.get("CLAUDECODE") or os.environ.get("CLAUDE_CODE_ENTRYPOINT"):
        return "claude_code"
    if Path("/mnt/data").is_dir():
        return "chatgpt"
    if Path("/mnt/user-data").is_dir() or Path("/mnt/skills").is_dir():
        return "claude_web"
    return "other"


def start_here_text(title, identifier, story_name, fingerprint, depth, surface, schema_version, depth_answered):
    depth_line = (f"1. How deep the breakdown goes: {depth} (choice 2, your answer)." if depth_answered
                  else f"1. How deep the breakdown goes: {depth} (choice 2, the default; say quick or detailed to change it).")
    lines = [
        f"# {title}",
        "",
        "## Where things stand",
        "Step 1 of 12, starting: the project folder is made and your story is kept safe in Original.",
        "Checked by the checker: never.",
        "Waiting for you: one choice, whether the story is yours to adapt (choice 1).",
        "",
        "## Next step",
        "Tell me whether the story is yours to adapt, for example: It's mine.",
        "",
        "## Big choices so far",
        depth_line,
        "",
        "## Files in this folder",
        "Each file's number is its place in the list Files in this folder; the log below records every change.",
    ]
    lines.extend(f"- {name}: {meaning}." for name, meaning in FILES_IN_THIS_FOLDER)
    lines += [
        "",
        "## Word list",
        "- step: one of the 12 steps of the work, counted from 1.",
        "- choice: a question for you with a default answer; the word defaults accepts every default.",
        "- depth: how deep the breakdown goes: quick, standard or detailed.",
        "",
        "## Log",
        "",
        DIVIDER_LINE,
        "",
        f"### PROJECT {identifier} {title}",
        f"- title: {title}",
        f"- source_file: {story_name}",
        f"- source_fingerprint: {fingerprint}",
        f"- depth: {depth}",
        f"- surface: {surface}",
        "- code_execution: yes",
        "- batch_size: 12",
        "- training_off: not_confirmed",
        "- rights: open",
        f"- schema_version: {schema_version}",
        "- checker_last_run: never",
        "- status: draft",
        "- locked: no",
        "",
        "END OF FILE | Start here | 1 records",
    ]
    return "\n".join(lines) + "\n"


def choices_text(depth, depth_answered):
    depth_letter = {"standard": "a", "quick": "b", "detailed": "c"}[depth]
    date = today()
    depth_status = "answered" if depth_answered else "defaulted"
    lines = [
        "# Choices",
        "",
        "## Waiting for you",
        "1. Is this story yours, or do you have permission to adapt it? If you say nothing: it's yours (choice 1).",
        "",
        "## Small choices I made",
        f"- How deep the breakdown goes: {depth} (choice 2).",
        "- The setting that lets the app learn from your chats: not confirmed off yet; tell me once it is off (choice 3).",
        "",
        DIVIDER_LINE,
        "",
        "### CHOICE CHOICE-001 Rights",
        "- question: Is this story yours, or do you have permission to adapt it?",
        "- why: What you may do with the finished work depends on it: private study, or sharing and publishing.",
        "- option: a | text: It's mine",
        "- option: b | text: Someone else's, and I have their permission",
        "- option: c | text: It is in the public domain",
        "- option: d | text: Not mine and no permission: private study only",
        "- default: a | reason: most people adapt their own work",
        "- answer: open",
        "- asked: yes",
        "- checkpoint: none",
        "- affects: PROJECT.rights",
        "- sets: PROJECT.rights | value: mine | when: a",
        "- sets: PROJECT.rights | value: permission | when: b",
        "- sets: PROJECT.rights | value: public_domain | when: c",
        "- sets: PROJECT.rights | value: study_only | when: d",
        "- based_on: D4 R1",
        "- status: open",
        "- date: none",
        "- locked: no",
        "",
        "### CHOICE CHOICE-002 Depth",
        "- question: How deep should the breakdown go?",
        "- why: Depth sets how many details each scene and shot gets, and how long the work takes.",
        "- option: a | text: Standard: every shot planned in full",
        "- option: b | text: Quick: a one-line shot list for every scene",
        "- option: c | text: Detailed: every field, for the hardest scenes",
        "- default: a | reason: standard is enough to make pictures and video from",
        f"- answer: {depth_letter}",
        "- asked: no",
        "- checkpoint: none",
        "- affects: PROJECT.depth",
        "- sets: PROJECT.depth | value: standard | when: a",
        "- sets: PROJECT.depth | value: quick | when: b",
        "- sets: PROJECT.depth | value: detailed | when: c",
        "- based_on: none",
        f"- status: {depth_status}",
        f"- date: {date}",
        "- locked: no",
        "",
        "### CHOICE CHOICE-003 Privacy setting",
        "- question: Have you turned off the setting that lets the app learn from your chats?",
        "- why: An unpublished story should not be used to train anyone's models.",
        "- option: a | text: Not confirmed yet",
        "- option: b | text: Yes, it is off",
        "- default: a | reason: nothing is assumed until you say it is off",
        "- answer: a",
        "- asked: no",
        "- checkpoint: none",
        "- affects: PROJECT.training_off",
        "- sets: PROJECT.training_off | value: not_confirmed | when: a",
        "- sets: PROJECT.training_off | value: confirmed | when: b",
        "- based_on: D1 §4.9",
        "- status: defaulted",
        f"- date: {date}",
        "- locked: no",
        "",
        "END OF FILE | Choices | 3 records",
    ]
    return "\n".join(lines) + "\n"


def unique_folder(parent, name):
    """A folder name not yet used: 'The Catch', then 'The Catch 2' ('Start again' keeps the old project)."""
    candidate = parent / name
    number = 2
    while candidate.exists():
        candidate = parent / f"{name} {number}"
        number += 1
    return candidate


# ---------------------------------------------------------------- plain words for units

def unit_in_plain_words(unit, steps=None):
    """'U-08-SC10-B2' becomes 'writing the shots, scene 10, batch 2' (the step's name from steps.json)."""
    match = UNIT_PATTERN.match(unit or "")
    if not match:
        return "records"
    step = int(match.group(1))
    scope = match.group(2)
    name = f"step {step + 1}"
    for entry in (steps or {}).get("steps", []):
        if entry.get("step") == step:
            name = entry.get("user_name") or entry.get("name") or name
            break
    if scope == "SELFTEST":
        return "checking this app"
    parts = [f"step {step + 1} ({name})" if step <= 11 else name]
    scene = SCENE_ID.match(scope)
    range_match = re.match(r"^(SC\d+[A-Z]?)\.\.(SC\d+[A-Z]?)$", scope)
    if range_match:
        parts.append(f"scenes {scene_number_words(range_match.group(1))[6:]} to {scene_number_words(range_match.group(2))[6:]}")
    elif scene:
        parts.append(scene_number_words(scene.group(1)))
        rest = scope[len(scene.group(1)):]
        batch = re.match(r"^-B(\d+)$", rest)
        part = re.match(r"^-P(\d+)$", rest)
        if batch:
            parts.append(f"batch {int(batch.group(1))}")
        elif part:
            parts.append(f"part {int(part.group(1))}")
        elif rest == "-LIST":
            parts.append("shot list")
    return ", ".join(parts)


def unit_in_few_words(unit, steps=None):
    """A short name for what a unit made, for save ZIP names: 'scene 10', 'scene 10 batch 2', 'world and style'."""
    match = UNIT_PATTERN.match(unit or "")
    if not match:
        return "the start"
    scope = match.group(2)
    scene = SCENE_ID.match(scope)
    if scene and ".." not in scope:
        words = scene_number_words(scene.group(1))
        batch = re.match(r"^-B(\d+)$", scope[len(scene.group(1)):])
        return f"{words} batch {int(batch.group(1))}" if batch else words
    step = int(match.group(1))
    for entry in (steps or {}).get("steps", []):
        if entry.get("step") == step:
            return entry.get("user_name") or entry.get("name") or f"step {step + 1}"
    return f"step {step + 1}"


def plural(count, word):
    """'1 record', '2 records'."""
    return f"{count} {word}" if count == 1 else f"{count} {word}s"


def load_steps(skill_folder=None):
    try:
        return load_json("schema/steps.json", skill_folder)
    except (OSError, ValueError):
        return {}


# ---------------------------------------------------------------- apply: merging an inbox file

def split_scene_record(record, schema):
    """A SCENE record's fields split by where they live: list and plan fields (04 Scene list) and design fields
    (its scene file). status, locked and notes stay with the list copy, so the two copies never disagree."""
    list_fields = []
    design_fields = []
    for line in record.fields:
        definition = schema.field("SCENE", line.name) or {}
        if definition.get("part_of") == "design":
            design_fields.append(line)
        else:
            list_fields.append(line)
    return list_fields, design_fields


def copy_record_with(record, field_lines):
    copy = Record(type_name=record.type_name, identifier=record.identifier, title=record.title,
                  known_type=True, is_new=True, heading_raw=None)
    for line in field_lines:
        copy.body.append(FieldLine(name=line.name, value=line.value, written_name=line.name, changed=True))
    for note in record.notes:
        copy.body.append(OtherLine(kind="note", raw=note))
    return copy


def default_status(type_name):
    if type_name in ("CHOICE", "FINDING"):
        return "open"
    return "draft"


class ApplyResult:
    """What apply did: its problem lines, counts, the files written, notes and the history folder used."""

    def __init__(self):
        self.history_folder = None
        self.answered = []
        self.problems = []
        self.new_records = 0
        self.changed_records = 0
        self.files_written = []
        self.notes = []


def merge_fields_into(existing, incoming_lines, schema):
    """Set each field the incoming record names: its lines replace the existing lines of that field (a redo
    replaces the whole field). Fields the incoming record does not name are kept."""
    names = []
    for line in incoming_lines:
        if line.name not in names:
            names.append(line.name)
    for name in names:
        values = [line.value for line in incoming_lines if line.name == name and not line.missing]
        if not values:
            continue
        definition = schema.field(existing.type_name, name) or {}
        if not definition.get("repeat"):
            values = values[:1]
        existing.set_items(name, values, schema)


def apply_inbox(project, inbox_path, steps=None):
    """Check an inbox file, then merge its records into the numbered files. Returns (exit code, ApplyResult)."""
    schema = project.schema
    result = ApplyResult()
    inbox = parse_file(inbox_path, f"inbox/{Path(inbox_path).name}", schema)
    current_files = project.load_record_files()
    current_index, _ = merge_copies(current_files, schema)
    context = FormContext.for_records(schema, project.words, [inbox], other_record_files=current_files,
                                      written_by_ai=True, current_records=current_index)
    problems = run_form_checks([inbox], context, INBOX_CHECKS)
    for extra_check in APPLY_CHECKS:
        problems.extend(extra_check(project, inbox, current_files, context))
    result.problems = problems
    if any(problem.is_error for problem in problems):
        return 1, result
    apply_tidy_fixes([inbox], context)
    drop_code_written_fields(inbox, context)

    files_by_name = {record_file.name: record_file for record_file in current_files}
    changed_files = set()
    locations = {}
    for record_file in current_files:
        for record in record_file.records:
            locations.setdefault(record.key, []).append(record_file)

    def file_for(name):
        if name not in files_by_name:
            title = Path(name).stem
            title = re.sub(r"^\d{2} ", "", title)
            new_file = new_record_file(name, [f"# {title}", "",
                                              "The plain summary of this file is written when the tools next build the views."],
                                       title)
            new_file.path = project.folder / name
            new_file.is_new_file = True
            files_by_name[name] = new_file
        return files_by_name[name]

    def keep_copies_in_step(record, field_lines, target_name):
        """A field that another file's copy of the record already holds is updated there too, so the copies
        never disagree (G10, FORM-09)."""
        for other_file in locations.get(record.key, []):
            if other_file.name == target_name:
                continue
            copy = other_file.find(record.type_name, record.identifier)
            if copy is None:
                continue
            shared = [line for line in field_lines if copy.field_lines(line.name)]
            if shared:
                before = copy.changed
                merge_fields_into(copy, shared, schema)
                if copy.changed:
                    changed_files.add(other_file.name)
                    if not before:
                        result.changed_records += 1

    def put(record, field_lines, target_name, add_code_defaults):
        keep_copies_in_step(record, field_lines, target_name)
        record_file = file_for(target_name)
        existing = record_file.find(record.type_name, record.identifier)
        if existing is not None:
            before = existing.changed
            merge_fields_into(existing, field_lines, schema)
            if record.title and record.title != existing.title:
                existing.title = record.title
                existing.heading_changed = True
            if existing.changed and not before:
                result.changed_records += 1
            if existing.changed:
                changed_files.add(target_name)
            return existing
        fresh = copy_record_with(record, field_lines)
        if add_code_defaults:
            if not fresh.field_lines("status"):
                fresh.body.append(FieldLine(name="status", value=default_status(record.type_name), written_name="status", changed=True))
            if not fresh.field_lines("locked"):
                fresh.body.append(FieldLine(name="locked", value="no", written_name="locked", changed=True))
        add_record(record_file, fresh, schema, project.type_order_for(target_name))
        result.new_records += 1
        changed_files.add(target_name)
        return fresh

    all_files = lambda: list(files_by_name.values())
    for record in inbox.records:
        if record.type_name == "SCENE":
            list_fields, design_fields = split_scene_record(record, schema)
            if list_fields or not design_fields:
                put(record, list_fields, SCENE_LIST_FILE, add_code_defaults=True)
            if design_fields:
                put(record, design_fields, project.scene_file_name(record.identifier, all_files(), record),
                    add_code_defaults=False)
            continue
        where = locations.get(record.key)
        target = where[0].name if where else project.target_file_for(record, all_files())
        if target is None:
            result.notes.append(f"No file holds {record.type_name} records; {record.label} was not applied.")
            continue
        put(record, record.fields, target, add_code_defaults=True)

    answered = apply_choice_answers(project, inbox, files_by_name, changed_files, result)
    result.history_folder = history_run_folder(project)
    for name in sorted(changed_files):
        record_file = files_by_name[name]
        ensure_end_line(record_file, re.sub(r"^\d{2} ", "", Path(name).stem))
        path = project.folder / name
        if path.is_file():
            keep_in_history(result.history_folder, path, name)
        write_file(record_file, path, schema)
        result.files_written.append(name)
    result.notes.extend(answered)
    return 0, result


def drop_code_written_fields(inbox, context):
    """Remove the fields code works out (FORM-10 warned about them): they are never stored."""
    for record in inbox.records:
        for line in list(record.fields):
            definition, name, _ = resolve_field(context.schema, context.words, record, line.name)
            if definition is None:
                continue
            if definition.get("stored") is False or context.conditions.writer_for(definition, record) == "code_derived":
                record.body.remove(line)


def history_run_folder(project):
    """A new folder in history/ for one command's old versions, named by date and time ('2026-10-02 141503')."""
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")
    folder = project.history_folder / stamp
    number = 2
    while folder.exists():
        folder = project.history_folder / f"{stamp} {number}"
        number += 1
    folder.mkdir(parents=True)
    return folder


def keep_in_history(history_folder, path, name):
    """Copy a file into history/ before it changes (7.3: no command deletes a record file)."""
    target = Path(history_folder) / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)
    return target


def apply_choice_answers(project, inbox, files_by_name, changed_files, result):
    """When the AI passes on a user's answer to a choice: code sets its status and date, writes what the answer
    sets (sets lines and SETVALUE records) and locks what it names. Returns plain notes for the report."""
    schema = project.schema
    notes = []
    all_records = [record for record_file in files_by_name.values() for record in record_file.records]
    book = ChoiceBook(all_records)
    for incoming in inbox.records:
        if incoming.type_name != "CHOICE" or not incoming.identifier:
            continue
        answer = (incoming.get("answer") or "").strip()
        if not answer or answer.lower() == "open":
            continue
        stored = next((record for record in all_records if record.key == incoming.key), None)
        if stored is None:
            continue
        status = normalise_word(stored.get("status") or "open")
        if status in ("answered", "defaulted"):
            continue
        choice_label = f"choice {int(stored.identifier.split('-')[1])}"
        default_letter = split_item(stored.get("default") or "").first.strip().lower()
        if answer.lower() in ("default", "defaults"):
            if not re.fullmatch(r"[a-z]", default_letter):
                notes.append(f"{choice_label} has no default, so the answer 'defaults' was not applied; ask the user.")
                continue
            letter = default_letter
            stored.set_field("answer", letter, schema)
            stored.set_field("status", "defaulted", schema)
        else:
            letter = answer.lower() if re.fullmatch(r"[a-zA-Z]", answer) else None
            stored.set_field("status", "answered", schema)
        stored.set_field("date", today(), schema)
        changed_files.add(stored.file_name)
        for item_text in stored.get_all("sets"):
            item = split_item(item_text)
            if letter is None or (item.get("when") or "").lower() != letter:
                continue
            target_text = item.first.strip()
            if target_text in book.set_values:
                set_value = book.set_values[target_text]
                target = find_record(all_records, set_value.get("target") or "", schema)
                if target is None:
                    notes.append(f"{choice_label}: the record it sets, {set_value.get('target')}, does not exist yet.")
                    continue
                for name in set_value.field_names():
                    if name == "target" or name in ("status", "locked"):
                        continue
                    target.set_items(name, set_value.get_all(name), schema)
                target.set_field("locked", "yes", schema)
                changed_files.add(target.file_name)
                continue
            match = re.match(r"^(.+)\.([a-z][a-z0-9_]*)$", target_text)
            if not match or item.get("value") is None:
                continue
            target = find_record(all_records, match.group(1), schema)
            if target is None:
                notes.append(f"{choice_label}: the record it sets, {match.group(1)}, does not exist yet.")
                continue
            target.set_field(match.group(2), item.get("value"), schema)
            changed_files.add(target.file_name)
        for identifier in split_list(stored.get("locks") or ""):
            target = find_record(all_records, identifier, schema)
            if target is not None:
                target.set_field("locked", "yes", schema)
                changed_files.add(target.file_name)
        notes.append(f"{choice_label} is now {normalise_word(stored.get('status'))}; what it sets was written.")
        result.answered.append(f"{choice_label} {normalise_word(stored.get('status'))}")
    return notes


def find_record(records, reference, schema):
    """A record by ID, or by type name for PROJECT and singletons."""
    reference = reference.strip()
    for record in records:
        if record.identifier == reference:
            return record
    if reference == "PROJECT" or schema.is_singleton(reference):
        for record in records:
            if record.type_name == reference:
                return record
    return None


# Other modules may add checks that run on an inbox before it is merged (for example the ID checks):
# each is a function (project, inbox record file, current record files, FormContext) -> list of Problem.
APPLY_CHECKS = []


def register_apply_check(function):
    APPLY_CHECKS.append(function)
    return function


@register_apply_check
def check_one_project_record(project, inbox, current_files, context):
    """A project has one PROJECT record: an inbox may change it, never add a second one under another ID."""
    from .record_format import Problem
    stored = [record.identifier for record_file in current_files for record in record_file.records
              if record.type_name == "PROJECT"]
    problems = []
    for record in inbox.records:
        if record.type_name == "PROJECT" and stored and record.identifier not in stored:
            problems.append(Problem("E", "FORM-02", record.identifier or "PROJECT", None,
                                    f"is not this project's ID ({stored[0]}); a project has one PROJECT record",
                                    f"Fix: write ### PROJECT {stored[0]}", file_name=inbox.name,
                                    line_number=record.heading_line_number))
    return problems


# ---------------------------------------------------------------- the commands

def add_new_arguments(parser):
    parser.add_argument("story", help="the story file")
    parser.add_argument("--title", help="the project's title (default: from the story)")
    parser.add_argument("--depth", choices=["quick", "standard", "detailed"],
                        help="how deep, when the user asked for one (default: standard)")
    parser.add_argument("--into", help="the folder to make the project in (default: My breakdowns, or here)")
    parser.add_argument("--surface", choices=["claude_code", "claude_cowork", "claude_web", "chatgpt", "gemini", "other"],
                        help="the app (default: found from the environment; the self-test records it)")


def run_new(context):
    arguments = context.arguments
    story = Path(arguments.story).expanduser()
    if not story.is_absolute():
        story = Path(os.getcwd()) / story
    if not story.is_file():
        raise StageStop(f'The story file "{arguments.story}" was not found. Put it in My stories/ or give its full path.')
    data = story.read_bytes()
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = data.decode("latin-1")
    title = (arguments.title or guess_title(story, text)).strip()
    identifier = project_identifier(title)
    parent = Path(arguments.into).expanduser() if arguments.into else default_breakdowns_folder(os.getcwd())
    if not parent.is_absolute():
        parent = Path(os.getcwd()) / parent
    parent.mkdir(parents=True, exist_ok=True)
    folder = unique_folder(parent, safe_file_name(title))
    folder.mkdir(parents=True)
    machine = folder / MACHINE_FOLDER
    for sub_folder in ("inbox", "history", "handouts"):
        (machine / sub_folder).mkdir(parents=True, exist_ok=True)
    original = folder / ORIGINAL_FOLDER
    original.mkdir()
    shutil.copy2(story, original / story.name)
    fingerprint = fingerprint_of_bytes(data)
    (original / "fingerprint.txt").write_text(f"SHA-256 {fingerprint}  {story.name}\n", encoding="utf-8")
    depth = arguments.depth or "standard"
    surface = arguments.surface or detect_surface()
    schema_version = context.schema.data.get("schema_version", "1.0")
    (folder / START_HERE).write_text(start_here_text(title, identifier, story.name, fingerprint, depth, surface,
                                                     schema_version, bool(arguments.depth)), encoding="utf-8")
    (folder / CHOICES_FILE).write_text(choices_text(depth, bool(arguments.depth)), encoding="utf-8")
    project = Project(folder, context.schema, context.words)
    context.project_folder = folder
    project.add_log_entry(f'Project started from the story file "{story.name}".')
    manifest = project.read_manifest()
    manifest.update({"created": now(), "schema_version": schema_version, "project": identifier, "title": title,
                     "source": {"file": f"{ORIGINAL_FOLDER}/{story.name}", "fingerprint": fingerprint}})
    project.write_manifest(project.refresh_manifest(manifest))
    shown = folder.relative_to(parent.parent) if parent.parent in folder.parents else folder.name
    context.say(f'Made the project "{title}" in "{shown}".')
    context.say(f"Kept your story in {ORIGINAL_FOLDER}/ with its fingerprint. Depth: {depth}. App: {surface}.")
    context.say("Next: the app self-test (selftest --prepare), then ask the user the rights question (choice 1).")
    context.summary = f"project {identifier} made"
    return 0


def add_status_arguments(parser):
    pass


def run_status(context):
    project = Project(context.project, context.schema, context.words)
    record_files = project.load_record_files()
    merged, _ = merge_copies(record_files, context.schema)
    manifest = project.read_manifest()
    steps = load_steps(context.skill_folder)
    project_record = next((record for key, record in merged.items() if key[0] == "PROJECT"), None)
    title = (project_record.get("title") if project_record else None) or project.folder.name
    depth = (project_record.get("depth") if project_record else None) or "standard"
    surface = (project_record.get("surface") if project_record else None) or "unknown"
    context.say(f"Project: {title} ({depth} depth; app: {surface}).")
    units = manifest.get("units_done", [])
    if units:
        last = units[-1]
        context.say(f"Done: {plural(len(units), 'unit')}; the last was {unit_in_plain_words(last.get('unit'), steps)} "
                    f"({plural(last.get('records', 0), 'record')}, {last.get('applied', '')[:10]}).")
    else:
        context.say("Done: no units yet.")
    counts = {}
    for key in merged:
        counts[key[0]] = counts.get(key[0], 0) + 1
    if counts:
        shown = ", ".join(f"{count} {type_name}" for type_name, count in counts.items())
        context.say(f"Records: {shown}.")
    stale = [record.label for record in merged.values() if normalise_word(record.get("status") or "") == "stale"]
    context.say("Stale: none." if not stale else f"Stale: {len(stale)} records ({', '.join(stale[:12])}"
                + (" and more" if len(stale) > 12 else "") + ").")
    waiting = [record for key, record in merged.items()
               if key[0] == "CHOICE" and normalise_word(record.get("status") or "open") == "open"]
    if waiting:
        context.say(f"Waiting for the user: {plural(len(waiting), 'open choice')}.")
        for record in waiting[:7]:
            default = split_item(record.get("default") or "").first or ""
            asked = "asked" if normalise_word(record.get("asked") or "") == "yes" else "small choice"
            context.say(f"  {record.identifier} ({asked}): {record.get('question') or record.title}"
                        + (f" [default {default}]" if default else ""))
    else:
        context.say("Waiting for the user: nothing.")
    last_run = (project_record.get("checker_last_run") if project_record else None) or "never"
    context.say(f"Checked by the checker: {last_run}.")
    batches = manifest.get("batches", {})
    short = [f"{unit} ({batch.get('received')} of {batch.get('expected')})"
             for scene, scene_batches in batches.items() for unit, batch in scene_batches.items()
             if batch.get("expected") not in (None, batch.get("received"))]
    if short:
        context.say("Batches not complete: " + ", ".join(short) + ".")
    pending = sorted(path.name for path in project.inbox_folder.glob("*.md")) if project.inbox_folder.is_dir() else []
    if pending:
        context.say("In the inbox, not yet applied: " + ", ".join(pending) + ".")
    context.say("Next: " + next_step_line(project, context))
    return 0


def next_step_line(project, context):
    """The next unit, from make_handout when that module exists; else the command that finds it."""
    try:
        from . import make_handout
        finder = getattr(make_handout, "next_unit", None)
        if finder is not None:
            found = finder(project.folder)
            if found:
                return str(found)
    except ImportError:
        pass
    return "run stage.py next to get the next unit."


def add_apply_arguments(parser):
    parser.add_argument("inbox_file", help="the inbox file the AI wrote (a path, or its name in the inbox folder)")


def resolve_inbox_path(project, written):
    path = Path(written).expanduser()
    candidates = [path if path.is_absolute() else Path(os.getcwd()) / path,
                  project.inbox_folder / written, project.inbox_folder / (written + ".md")]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise StageStop(f'The inbox file "{written}" was not found. Write the records to '
                    f'"{MACHINE_FOLDER}/inbox/<unit>.md" and apply that file.')


def run_apply(context):
    project = Project(context.project, context.schema, context.words)
    steps = load_steps(context.skill_folder)
    with project.lock():
        inbox_path = resolve_inbox_path(project, context.arguments.inbox_file)
        exit_code, result = apply_inbox(project, inbox_path, steps)
        for problem in result.problems:
            context.say(str(problem))
        unit = inbox_path.stem if UNIT_PATTERN.match(inbox_path.stem) else None
        if exit_code != 0:
            errors = sum(1 for problem in result.problems if problem.is_error)
            context.say(f"Not applied: {errors} error(s) above. Fix only those lines in {inbox_path.name} and apply it again.")
            context.summary = f"{inbox_path.name} refused, {errors} errors"
            return 1
        inbox_records = parse_file(inbox_path, inbox_path.name, project.schema).records
        applied_copy = result.history_folder / "inbox" / inbox_path.name
        applied_copy.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(inbox_path), applied_copy)
        manifest = project.read_manifest()
        if unit:
            manifest.setdefault("units_done", []).append({"unit": unit, "applied": now(),
                                                          "records": len(inbox_records),
                                                          "files": result.files_written})
            batch = re.match(r"^U-08-(SC\d{2,3}[A-Z]?)-B(\d+)$", unit)
            if batch:
                scene_batches = manifest.setdefault("batches", {}).setdefault(batch.group(1), {})
                entry = scene_batches.setdefault(unit, {"expected": None})
                entry["received"] = sum(1 for record in inbox_records if record.type_name == "SHOT")
        project.write_manifest(project.refresh_manifest(manifest))
        described = unit_in_plain_words(unit, steps) if unit else f'the file "{inbox_path.name}"'
        if result.files_written:
            files = ", ".join(name[:-3] if name.endswith(".md") else name for name in result.files_written)
            answered = f" Choices: {', '.join(result.answered)}." if result.answered else ""
            project.add_log_entry(f"Saved {described}: {plural(len(inbox_records), 'record')}, in {files}.{answered}")
        for note in result.notes:
            context.say(note)
        context.say(f"Applied {inbox_path.name}: {result.new_records} new and {result.changed_records} changed "
                    f"records in {', '.join(result.files_written) or 'no file'}. Next: stage.py check.")
        context.summary = f"{inbox_path.name} applied"
    return 0


def add_pack_arguments(parser):
    parser.add_argument("--after", help='what the save comes after, in plain words (default: the last unit), '
                                        'as in "scene 10"')
    parser.add_argument("--into", help="the folder for the ZIP (default: the folder that holds the project)")


def run_pack(context):
    project = Project(context.project, context.schema, context.words)
    steps = load_steps(context.skill_folder)
    with project.lock():
        manifest = project.read_manifest()
        numbers = project.log_entry_numbers()
        number = max(numbers) if numbers else 0
        record_files = [parse_file(project.folder / START_HERE, START_HERE, project.schema)] if (project.folder / START_HERE).is_file() else []
        project_record = next((record for record_file in record_files for record in record_file.records
                               if record.type_name == "PROJECT"), None)
        title = (project_record.get("title") if project_record else None) or project.folder.name
        after = context.arguments.after
        if not after:
            units = manifest.get("units_done", [])
            after = unit_in_few_words(units[-1]["unit"], steps) if units else "the start"
        name = safe_file_name(f"{number:03d} Save - {title} - after {after}") + ".zip"
        destination_folder = Path(context.arguments.into).expanduser() if context.arguments.into else project.folder.parent
        destination_folder.mkdir(parents=True, exist_ok=True)
        destination = destination_folder / name
        counter = 2
        while destination.exists():
            destination = destination_folder / (name[:-4] + f" ({counter}).zip")
            counter += 1
        count = 0
        with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(project.folder.rglob("*")):
                if not path.is_file():
                    continue
                relative = path.relative_to(project.folder)
                parts = relative.parts
                if parts[0] == MACHINE_FOLDER and len(parts) > 1 and parts[1] in PACK_LEFT_OUT:
                    continue
                if parts[0] == MACHINE_FOLDER and parts[-1] == LOCK_FILE:
                    continue
                archive.write(path, (Path(project.folder.name) / relative).as_posix())
                count += 1
        context.say(f'Saved the project as one file: "{destination.name}" ({count} files), in "{destination_folder.name}".')
        context.say("To continue in a new chat: attach this save file and type: Continue my breakdown.")
        context.summary = f"saved {destination.name}"
    return 0


def add_unpack_arguments(parser):
    parser.add_argument("zip_file", help="the save ZIP")
    parser.add_argument("--into", help="the folder to open it in (default: My breakdowns, or here)")


def run_unpack(context):
    zip_path = Path(context.arguments.zip_file).expanduser()
    if not zip_path.is_absolute():
        zip_path = Path(os.getcwd()) / zip_path
    if not zip_path.is_file():
        raise StageStop(f'The save file "{context.arguments.zip_file}" was not found.')
    into = Path(context.arguments.into).expanduser() if context.arguments.into else default_breakdowns_folder(os.getcwd())
    if not into.is_absolute():
        into = Path(os.getcwd()) / into
    try:
        archive = zipfile.ZipFile(zip_path)
    except zipfile.BadZipFile:
        raise StageStop(f'"{zip_path.name}" is not a ZIP file. Attach the save file the tools made.')
    with archive:
        names = [name for name in archive.namelist() if not name.endswith("/")]
        if not names:
            raise StageStop(f'"{zip_path.name}" is empty.')
        tops = set()
        for name in names:
            parts = Path(name).parts
            if name.startswith(("/", "\\")) or ".." in parts or (parts and ":" in parts[0]):
                raise StageStop(f'"{zip_path.name}" holds a file outside its folder ("{name}"); it was not opened.')
            tops.add(parts[0])
        if len(tops) != 1:
            raise StageStop(f'"{zip_path.name}" does not hold one project folder. Attach a save file made by stage.py pack.')
        top = tops.pop()
        if f"{top}/{START_HERE}" not in names:
            raise StageStop(f'"{zip_path.name}" has no "{START_HERE}", so it is not a saved project.')
        destination = into / top
        if destination.exists():
            raise StageStop(f'A folder "{top}" already exists in "{into.name}". Open the save somewhere else with '
                            '--into "<folder>", or move the old folder first.')
        into.mkdir(parents=True, exist_ok=True)
        archive.extractall(into)
    for sub_folder in ("inbox", "history", "handouts"):
        (destination / MACHINE_FOLDER / sub_folder).mkdir(parents=True, exist_ok=True)
    context.project_folder = destination
    context.say(f'Opened the save "{zip_path.name}" as the project folder "{top}" in "{into.name}".')
    context.say("Next: stage.py status, then carry on with the next unit.")
    context.summary = f"opened {zip_path.name}"
    return 0


def register_commands(table):
    """The commands of this module (stage.py calls this; see the note at the top of stage.py)."""
    table.add("new", "Start a project from a story file", run_new, add_new_arguments, uses_project=False)
    table.add("status", "Where things stand: done, stale, waiting for the user, next", run_status, add_status_arguments)
    table.add("apply", "Accept the AI's records from an inbox file into the numbered files", run_apply, add_apply_arguments)
    table.add("pack", "Save the project as one ZIP", run_pack, add_pack_arguments)
    table.add("unpack", "Open a saved project ZIP", run_unpack, add_unpack_arguments, uses_project=False)
