"""adopt_folder.py: the commands adopt, impact and questions (blueprint 7.1, 5.2, 5.4 rule 5, 11.2).

In plain words:
- adopt "<folder>" "<story file>" turns a folder saved by hand in a chat app without code (Gemini, or any app
  whose self-test found no code) into a project the checker can read. It keeps the story in Original/ with its
  fingerprint and numbers it (03 Story - numbered, speeches.json, story map.json); merges the files the chat
  saved in parts ("07 Characters and voices - Saye.md", "Scene 10 - Saye's kitchen - shots 130-990.md") into
  their numbered files by ID (G10); turns every quote anchor into line numbers where the story given holds its
  scope, each found exactly once (CITE-02's rule); takes over every field code keeps that the AI had to write in
  chat (chat_writer: ai), working each one out again or confirming it, and logs each as a note (N), never as a
  warning or an error; stores the beat each story point resolves to; marks the project as one where code runs;
  and then runs check --all. The folder may also be given as the ZIP the user made of it.
- impact <ID> lists what depends on a record: every record that cites it and, following the work downstream only
  (records written at the same step or later), every record that goes stale when it changes, the units that
  would be redone and which of those records are locked (a locked record changes only through a choice the
  user answers). It changes nothing.
- questions [--sample] [--seed N] builds yes/no review questions from the records for every turn shot, turn beat
  and must-keep shot, every shot that needs mirror, text or violence handling, and a seeded share of the other
  shots (question_sample_share), each citing the story lines it can be checked against, in batches of
  question_batch_size for fresh units (U-10-QUESTIONS-B1 ...). It writes them to
  "For machines - do not edit/questions.json" and "questions.md".

Numbers come from rules/constants.json by name. Standard library only.

After the full run on The Catch (Project notes 31 and 32):
- every shot that keeps a fact hidden gets a review question about the hiding.
"""

import argparse
import json
import math
import random
import re
import shutil
import zipfile
from dataclasses import dataclass, field as dataclass_field
from pathlib import Path

from .check_records import (CheckRun, StorySource, forget_locked_records, load_check_families, plain_name_of,
                            read_scene, register_report_section, run_check, scene_of)
from .checks_form import ChoiceBook, ConditionReader, resolve_field, same_value, setvalue_target_type
from .checks_ids_citations import (declared_identifiers, effective_type, field_values, identifier_exists,
                                   references)
from .derive_fields import Breakdown, mirror_route, speeches_from_json, story_point_fields, with_story_point_beats
from .project_files import (MACHINE_FOLDER, ORIGINAL_FOLDER, SCENES_FOLDER, SCENE_FILE_TYPE_ORDER, START_HERE,
                            Project, StageStop, detect_surface, fingerprint_of_bytes, history_run_folder,
                            keep_in_history, now, safe_file_name, today, unique_folder)
from .record_format import (OtherLine, Problem, add_record, ensure_end_line, merge_copies, normalise_word, parse_file,
                            parse_line_numbers, parse_quote_anchor, render_file, sort_key_for_identifier, split_item,
                            split_list, split_outside_quotes, value_for_comparison)
from .read_story import NumberedStory, clean_title, read_into_project, real_words

# The check ID the notes about re-owned fields carry: FORM-10 is the writer check, and a chat_writer: ai field is
# exactly the case FORM-10 lets the AI write in chat and adopt takes over (5.2).
REOWN_CHECK_ID = "FORM-10"
# The check ID of the notes about merged records (G10's merge of copies across files).
MERGE_CHECK_ID = "FORM-09"
QUESTIONS_FILE = "questions.json"
QUESTIONS_TEXT_FILE = "questions.md"
QUESTION_UNIT = "U-10-QUESTIONS-B{number}"
SCENE_FILE_TYPES = ("SCENE", "PART", "BEAT", "SPEECH", "MOVE", "SETUP", "SHOTLIST", "SHOT", "CUT")
SCENE_FILE_NAME = re.compile(r"^Scene (?P<number>\d{2,3}[A-Z]?)(?: - (?P<rest>.+))?\.md$")
SCENE_IDENTIFIER = re.compile(r"^SC\d{2,3}[A-Z]?$")
STATE_IDENTIFIER = re.compile(r"^(?P<element>.+)\.S\d{2}$")
NUMBER_AT_END = re.compile(r"^(?P<prefix>.*?)(?P<number>\d+)$")
FINDING_IDENTIFIER = re.compile(r"^FIND-(\d{3})$")
RANGE_PIECE = re.compile(r"^\s*(\S+)\s*\.\.\s*(\S+)\s*$")
BECAUSE_LINE_PIECE = re.compile(r"^(\s*)line:\s*(.+?)\s*$", re.IGNORECASE)
SUB_PART_PIECE = re.compile(r"^(\s*)([A-Za-z][A-Za-z0-9 _-]*?)(\s*:\s?)(.*?)(\s*)$")
SENTENCE_END = re.compile(r"(?<=[.?!])\s+")
SIDE_WORDS = re.compile(r"\b(left|right)\b", re.IGNORECASE)
EMPTY_WORDS = ("none", "open", "auto", "all", "default", "never", "as_written")
ZIP_LEFT_OUT = ("__MACOSX", ".DS_Store", "Thumbs.db")
# Content flags that make a shot need violence handling (5.5 SHOT content_flags; 8.5's "violence and filters"): a
# little blood alone (blood_small) is a filter note, not violence to split into cause, reaction and aftermath.
VIOLENCE_FLAGS = ("violence_implied", "violence_onscreen", "weapon_visible", "gunfire", "gore", "self_harm")
# Mirror routes that make a shot need mirror handling a judge should look at (8.5; derive_fields.mirror_route): the
# routes where a person or a plot-sided detail differs from the place. A whole frame flipped (flip_all) or made as
# it appears (direct) is code's arithmetic, not a question for a judge.
MIRROR_ROUTES = ("plate", "flip_with_mirrored_references")
# Lines-kind places where one quote names exactly one line (WP12a's adopt rule): (record type, field or
# "field sub-part"). The only or last quote of every other lines value is a stretch that runs on through the rest
# of its speech and the short lines after it, and an era's "to" names that stretch's last line.
SINGLE_LINE_PLACES = {("SPEECH", "line"), ("PROP", "first_seen"), ("WORLD", "evidence"), ("CHARACTER", "evidence"),
                      ("STATE", "cause"), ("CHARACTER", "gesture line"), ("STATE", "from line"),
                      ("RULE", "era from")}
END_LINE_PLACES = {("RULE", "era to")}
# The unit that writes each record type (steps.json units), for impact's list of units to redo.
UNIT_OF_TYPE = {
    "PLAN": "U-02-FILM", "SEQUENCE": "U-02-FILM", "PLANT": "U-02-FILM", "FACT": "U-02-FILM",
    "CARDINAL": "U-02-COMPRESS", "STRAND": "U-02-BOOK", "STYLE": "U-03-WORLD", "WORLD": "U-03-WORLD",
    "RULE": "U-03-WORLD", "MOTIF": "U-04-MOTIFS", "LOCATION": "U-04-PLACES (the places unit that holds it)",
    "PROP": "U-04-THINGS",
    "TEXT": "U-04-THINGS", "CAMERA": "U-04-THINGS", "CAMSYS": "U-06-CAMERA", "CAMRULE": "U-06-CAMERA",
    "RESERVE": "U-06-CAMERA", "LENS": "U-06-CAMERA", "LOOK": "U-06-LOOKS", "VISUAL": "U-06-PLANS",
    "SOUNDPLAN": "U-06-PLANS", "LADDER": "U-06-PLANS", "FINDING": "U-09-JUDGE", "REVIEW": "U-10-QUESTIONS",
    "VOICETAKE": "U-14-VOICES", "FINISH": "U-15-FINISH", "MUSIC": "U-15-MUSIC",
}


# ---------------------------------------------------------------- small helpers

def constant(constants, name, default=None):
    """A named number of rules/constants.json (either of its tables), or default."""
    for table in ((constants or {}).get("constants") or {},
                  ((constants or {}).get("from_blueprint_text") or {}).get("constants") or {}):
        entry = table.get(name)
        if isinstance(entry, dict) and "value" in entry:
            return entry["value"]
    return default


def plural(count, word, plural_word=None):
    """'1 record', '2 records'; plural_word for words that do not just take an s."""
    return f"{count} {word}" if count == 1 else f"{count} {plural_word or word + 's'}"


def is_empty_word(value):
    return normalise_word(value or "") in EMPTY_WORDS


def range_text(first, last):
    return f"{first}" if first == last else f"{first}-{last}"


def lines_in_words(first, last):
    return f"line {first}" if first == last else f"lines {first} to {last}"


def shown_value(value, limit=70):
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[:limit - 1].rstrip() + "…"


def quoted_value(value, limit=70):
    """A value for a message, in double quotes unless it holds quotes itself (a quote anchor)."""
    text = shown_value(value, limit)
    return text if '"' in text or "“" in text else f'"{text}"'


def single_quoted(text):
    """Text for a question: double quotes become single ones and the sub-part bar a slash, so a REVIEW answer can
    carry the question word for word (a text value holds no ' | ', and double quotes would read as story quotes)."""
    text = str(text or "").replace("“", "'").replace("”", "'").replace('"', "'")
    return " ".join(text.replace(" | ", " / ").replace("|", "/").split())


def load_story_map(project_folder):
    path = Path(project_folder) / MACHINE_FOLDER / "story map.json"
    if not path.is_file():
        return None
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def id_in_range(identifier, first, last):
    """True when an ID lies in a range 'SC10-B01..SC10-B08': the same letters before the last number, and the
    number between the two ends."""
    wanted, low, high = (NUMBER_AT_END.match(text or "") for text in (identifier, first, last))
    if not (wanted and low and high):
        return False
    if not (wanted.group("prefix") == low.group("prefix") == high.group("prefix")):
        return False
    return int(low.group("number")) <= int(wanted.group("number")) <= int(high.group("number"))


def character_name(index, identifier):
    """The plain name of a character (or of the element a state belongs to): its record's title, else its ID's
    words ('CH-SAYE' gives 'Saye')."""
    element = STATE_IDENTIFIER.match(identifier or "")
    element_identifier = element.group("element") if element else identifier
    for type_name in ("CHARACTER", "PROP", "MOTIF", "TEXT", "LOCATION"):
        record = index.get((type_name, element_identifier))
        if record is not None and record.title:
            return record.title
    words = (element_identifier or "").split("-")[1:] or [element_identifier or "someone"]
    text = " ".join(word.lower() for word in words)
    return text[:1].upper() + text[1:]


# ---------------------------------------------------------------- adopt, part 1: the folder and the story

def unpack_zip(zip_path):
    """Unpack a ZIP of a project folder next to it, into a new folder named after the ZIP, refusing any name that
    would leave that folder. Returns the new folder."""
    target = unique_folder(zip_path.parent, safe_file_name(zip_path.stem))
    try:
        archive = zipfile.ZipFile(zip_path)
    except zipfile.BadZipFile:
        raise StageStop(f'"{zip_path.name}" is not a ZIP file that can be opened. Make the ZIP again (right-click '
                        "the folder, Compress) and attach it again.")
    with archive:
        members = []
        for member in archive.infolist():
            parts = Path(member.filename.replace("\\", "/")).parts
            if not parts or any(part in ZIP_LEFT_OUT for part in parts) or member.filename.endswith("/"):
                continue
            if member.filename.startswith(("/", "\\")) or ".." in parts or ":" in member.filename:
                raise StageStop(f'"{zip_path.name}" holds a file name that points outside its folder, so it was '
                                "not opened. Make the ZIP again from the project folder.")
            members.append((member, parts))
        target.mkdir(parents=True)
        for member, parts in members:
            destination = target.joinpath(*parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as source, open(destination, "wb") as handle:
                shutil.copyfileobj(source, handle)
    return target


def project_folder_in(folder):
    """The folder holding 00 Start here.md: the folder itself or one folder inside it (a ZIP usually holds the
    project folder). Stops with exit 2 otherwise."""
    folder = Path(folder)
    if (folder / START_HERE).is_file():
        return folder.resolve()
    inside = sorted(path for path in folder.rglob(START_HERE) if len(path.relative_to(folder).parts) <= 3)
    if len(inside) == 1:
        return inside[0].parent.resolve()
    if len(inside) > 1:
        names = ", ".join(f'"{path.parent.name}"' for path in inside)
        raise StageStop(f"Several projects found in \"{folder.name}\" ({names}). Give the folder of one of them.")
    raise StageStop(f'"{folder.name}" is not a breakdown folder: it has no "{START_HERE}". Give the folder saved '
                    "from the chat app (the one that holds 00 Start here.md).")


def resolve_input_folder(text):
    """The project folder adopt works on: a folder, or a ZIP of one (unpacked next to it)."""
    path = Path(text).expanduser()
    if not path.exists():
        raise StageStop(f'"{text}" was not found. Give the folder saved from the chat app, or its ZIP.')
    if path.is_file():
        if not zipfile.is_zipfile(path):
            raise StageStop(f'"{path.name}" is neither a folder nor a ZIP. Give the folder saved from the chat app, '
                            "or its ZIP.")
        path = unpack_zip(path)
    return project_folder_in(path)


def project_record_of(record_files):
    for record_file in record_files:
        for record in record_file.records:
            if record.type_name == "PROJECT":
                return record_file, record
    return None, None


def keep_story_in_original(project, story_path, history):
    """Put the story file in Original/ with fingerprint.txt (as stage.py new does); older files there go to
    history. Returns (the story's path in Original/, its fingerprint, whether Original/ changed)."""
    data = story_path.read_bytes()
    fingerprint = fingerprint_of_bytes(data)
    original = project.folder / ORIGINAL_FOLDER
    target = original / story_path.name
    fingerprint_line = f"SHA-256 {fingerprint}  {story_path.name}\n"
    present = [path for path in sorted(original.glob("*")) if path.is_file() and path.name != "fingerprint.txt"] \
        if original.is_dir() else []
    fingerprint_file = original / "fingerprint.txt"
    if [path.name for path in present] == [story_path.name] and fingerprint_of_bytes(target.read_bytes()) == fingerprint \
            and fingerprint_file.is_file() and fingerprint_file.read_text(encoding="utf-8") == fingerprint_line:
        return target, fingerprint, False
    original.mkdir(parents=True, exist_ok=True)
    for path in present + ([fingerprint_file] if fingerprint_file.is_file() else []):
        keep_in_history(history, path, f"{ORIGINAL_FOLDER}/{path.name}")
        if path.resolve() != story_path.resolve():
            path.unlink()
    if target.resolve() != story_path.resolve():
        shutil.copy2(story_path, target)
    fingerprint_file.write_text(fingerprint_line, encoding="utf-8")
    return target, fingerprint, True


# ---------------------------------------------------------------- adopt, part 2: merging the saved parts (G10)

def fixed_record_file_names(schema):
    """The numbered record files of 2.6 by their fixed names ("07 Characters and voices.md", "13 Health check.md",
    "20 Prompts for AI video/Takes.md")."""
    return [name for name in schema.data.get("files", {})
            if name.endswith(".md") and "<" not in name and not name.startswith(MACHINE_FOLDER)]


def saved_parts(project):
    """[(target file name, [part file names])]: the files a chat saved in parts, each with the numbered file its
    records belong in. A part is "<numbered file> - <what it holds>.md" beside its numbered file; in 11 Scenes it is
    any other file of the same scene ("Scene 10 - Saye's kitchen - shots 130-990.md"), whose numbered file is the
    scene's file with the shortest name."""
    found = []
    for name in fixed_record_file_names(project.schema):
        path = project.folder / name
        stem = path.name[:-3]
        parent = path.parent
        if not parent.is_dir():
            continue
        parts = sorted(candidate for candidate in parent.iterdir()
                       if candidate.is_file() and candidate.name.startswith(stem + " - ") and candidate.suffix == ".md")
        if parts:
            relative = [candidate.relative_to(project.folder).as_posix() for candidate in parts]
            found.append((name, relative))
    scenes = project.folder / SCENES_FOLDER
    if scenes.is_dir():
        by_scene = {}
        for path in sorted(scenes.glob("*.md")):
            match = SCENE_FILE_NAME.match(path.name)
            if match:
                by_scene.setdefault(match.group("number"), []).append(path.name)
        for number, names in sorted(by_scene.items(), key=lambda item: sort_key_for_identifier(item[0])):
            whole = [name for name in names if " - shots " not in name]
            if whole:
                main = sorted(whole, key=lambda name: (len(name), name))[0]
            else:
                # only batch files were saved: the scene's file is named as they are, without " - shots ..."
                main = re.sub(r" - shots .*$", "", sorted(names)[0][:-3]) + ".md"
            parts = [name for name in names if name != main]
            if parts:
                found.append((f"{SCENES_FOLDER}/{main}", [f"{SCENES_FOLDER}/{name}" for name in parts]))
    return found


def item_values(record, name):
    return [line.value.strip() for line in record.field_lines(name) if not line.missing]


def merge_record_into(existing, incoming, schema, notes, part_name, target_name):
    """Merge one record copy into the stored copy field by field (G10): a field the stored copy lacks is added;
    items of a repeatable field are combined without exact duplicates; a single field with two different values
    keeps the numbered file's value (the whole file is what the chat saved again after a change, 16's rule) and
    the part's value is named in a note. Returns True when the stored copy changed."""
    changed = False
    for name in incoming.field_names():
        values = [line.value.strip() for line in incoming.field_lines(name) if not line.missing]
        if not values:
            continue
        definition = schema.field(existing.type_name, name) or {}
        present = item_values(existing, name)
        if definition.get("repeat"):
            seen = {value_for_comparison(value) for value in present}
            added = [value for value in values if value_for_comparison(value) not in seen]
            if added:
                existing.set_items(name, present + added, schema)
                changed = True
            continue
        if not present:
            existing.set_field(name, values[0], schema)
            changed = True
        elif not same_value(present[0], values[0]):
            notes.append(Problem("N", MERGE_CHECK_ID, existing.label, name,
                                 f'is "{shown_value(present[0])}" in "{target_name}" but "{shown_value(values[0])}" '
                                 f'in the saved part "{part_name}"; the numbered file\'s value is kept',
                                 "Fix: if the part's value is the right one, write it in the numbered file (the part "
                                 "is kept in history)", file_name=target_name))
    for note in incoming.notes:
        if note not in existing.notes:
            existing.add_note(note[1:].strip() if note.startswith(">") else note)
            changed = True
    return changed


def next_finding_number(record_files):
    numbers = [int(match.group(1)) for record_file in record_files for record in record_file.records
               for match in [FINDING_IDENTIFIER.match(record.identifier or "")] if match]
    return (max(numbers) if numbers else 0) + 1


def comparable_record(record):
    return [(line.name, value_for_comparison(line.value)) for line in record.fields if not line.missing]


def cut_off_problem(part, part_name):
    """An error line when a saved part looks cut off (no END line, text after it, or a count that differs from its
    records, G9): such a part is not merged, so the record it may have lost is not hidden."""
    ends = part.end_lines
    if len(ends) != 1 or part.lines_after_end():
        return Problem("E", "FORM-06", f'"{part_name}"', None,
                       "was not merged: it has no single end line at its end, so the reply may have been cut off",
                       "Fix: save the part again from the chat, whole and ending with its END line, then run adopt "
                       "again", file_name=part_name)
    if ends[0].count != len(part.records):
        return Problem("E", "FORM-07", f'"{part_name}"', None,
                       f"was not merged: its end line counts {ends[0].count} records but it holds "
                       f"{len(part.records)}, so a record may be missing",
                       "Fix: save the part again from the chat, whole, then run adopt again", file_name=part_name,
                       line_number=ends[0].line_number)
    return None


def merge_saved_parts(project, files_by_name, notes, refused=None):
    """Merge every saved part into its numbered file (in memory). Returns [(part, target, records)]; the caller
    keeps the merged parts in history and takes them out of the folder. A part that looks cut off is left where it
    is, with an error line in refused."""
    schema = project.schema
    merged = []
    refused = refused if refused is not None else []
    for target_name, part_names in saved_parts(project):
        target = files_by_name.get(target_name)
        for part_name in part_names:
            part = files_by_name.get(part_name) or parse_file(project.folder / part_name, part_name, schema)
            problem = cut_off_problem(part, part_name)
            if problem is not None:
                refused.append(problem)
                continue
            # a scene's batch file is already loaded as a record file of its own: take it out of the list, so its
            # records are counted once, in the numbered file they move to
            files_by_name.pop(part_name, None)
            if target is None:
                # no numbered file yet: the first part becomes it, as the chat saved it
                target = part
                target.name = target_name
                target.path = project.folder / target_name
                target.became_numbered_file = True
                for record in target.records:
                    record.file_name = target_name
                files_by_name[target_name] = target
                merged.append((part_name, target_name, len(part.records)))
                continue
            moved = 0
            for record in part.records:
                if record.type_name == "FINDING" and record.identifier:
                    existing = target.find("FINDING", record.identifier) or next(
                        (other.find("FINDING", record.identifier) for other in files_by_name.values()
                         if other is not target and other.find("FINDING", record.identifier)), None)
                    if existing is not None and comparable_record(existing) != comparable_record(record):
                        new_identifier = f"FIND-{next_finding_number(list(files_by_name.values()) + [part]):03d}"
                        notes.append(Problem("N", "ID-01", record.identifier, None,
                                             f'is used by two different findings (one in "{part_name}"); that one is '
                                             f"now {new_identifier}", "Nothing to fix: findings are cited by nothing "
                                             "else", file_name=target_name))
                        record.identifier = new_identifier
                        record.heading_changed = True
                existing = target.find(record.type_name, record.identifier) if record.known_type else None
                if existing is not None:
                    merge_record_into(existing, record, schema, notes, part_name, target_name)
                    moved += 1
                    continue
                if record.body and not (isinstance(record.body[-1], OtherLine) and record.body[-1].kind == "blank"):
                    record.body.append(OtherLine(kind="blank", raw=""))
                add_record(target, record, schema, project.type_order_for(target_name)
                           if not target_name.startswith(SCENES_FOLDER + "/") else SCENE_FILE_TYPE_ORDER)
                moved += 1
            ensure_end_line(target, re.sub(r"^\d{2} ", "", Path(target_name).stem))
            target.end_line.changed = True
            target.records_moved_in = True
            merged.append((part_name, target_name, moved))
    return merged


# ---------------------------------------------------------------- adopt, part 3: quote anchors into line numbers

@dataclass
class AnchorReport:
    resolved: int = 0
    outside: int = 0
    unresolved: list = dataclass_field(default_factory=list)
    changes: list = dataclass_field(default_factory=list)


class AnchorResolver:
    """Turns quote anchors into line numbers by WP12a's adopt rule (G5, CITE-02). A quote is resolved only when its
    scope lies wholly in the story given and the quote holds at least quote_anchor_words_min words found exactly
    once there; an anchor whose scope reaches beyond the story given (an excerpt) stays a quote, and one that is
    not found once stays too, for CITE-02 to report."""

    def __init__(self, story, index, constants):
        self.story = story
        self.numbered = story.numbered
        self.index = index
        self.minimum = int(constant(constants, "quote_anchor_words_min", 3) or 3)
        self.numbered.minimum_words = self.minimum
        self.report = AnchorReport()

    def scene_scope(self, scene_identifier):
        if not scene_identifier:
            return None
        scope = self.story.scene_range(scene_identifier)
        if scope is not None:
            return tuple(scope)
        record = self.index.get(("SCENE", scene_identifier))
        if record is None:
            return None
        for name in ("lines", "from_lines"):
            value = record.get(name)
            numbers = parse_line_numbers(value) if value else None
            if numbers:
                return numbers[0][0], numbers[-1][1]
            if value and parse_quote_anchor(value) and not self.story.excerpt:
                found = self.numbered.resolve_lines(value)
                if found:
                    return found
        return None

    def scope_for(self, kind, identifier):
        """(first, last) of a scope when the story given holds all of it, else None."""
        if kind == "scene":
            scope = self.scene_scope(identifier)
        elif kind == "chapter":
            scope = self.numbered.chapters.get(identifier)
        else:
            scope = None if self.story.excerpt else (self.numbered.first, self.numbered.last)
        if scope is None or not self.story.holds(scope[0], scope[1]):
            return None
        return tuple(scope)

    def words_enough(self, quote):
        return len(real_words(quote)) >= self.minimum

    def convert(self, value, mode, scope, where):
        """The line numbers for one anchor value, or None (left as it is, counted in the report)."""
        text = value.strip()
        if not text or is_empty_word(text) or parse_line_numbers(text):
            return None
        quotes = parse_quote_anchor(text)
        if not quotes:
            return None
        if scope is None:
            self.report.outside += 1
            return None
        first, last = scope
        result = None
        if all(self.words_enough(quote) for quote in quotes):
            if mode == "single":
                number = self.numbered.resolve_line(quotes[0], first, last) if len(quotes) == 1 else None
                result = None if number is None else f"{number}"
            elif mode == "end":
                if len(quotes) == 1 and len(self.numbered.find_quote(quotes[0], first, last)) == 1:
                    number = self.numbered.resolve_end(quotes[0], first, last)
                    result = None if number is None else f"{number}"
            else:
                found = self.numbered.resolve_lines(text, first, last)
                result = None if found is None else range_text(*found)
        if result is None:
            self.report.unresolved.append(where + (text,))
            return None
        self.report.resolved += 1
        return result

    def resolve_record(self, record_file, record, schema, words):
        """Resolve every anchor in one record copy, in place."""
        type_name = record.type_name
        own_scene = scene_of(record.identifier) if type_name in SCENE_FILE_TYPES else None
        own_scope = ("scene", own_scene) if own_scene else ("whole", None)
        for line in record.fields:
            if line.missing:
                continue
            definition, name, _ = resolve_field(schema, words, record, line.name)
            if definition is None:
                continue
            effective = type_name
            if type_name == "SETVALUE":
                effective = setvalue_target_type(schema, record) or type_name
            kind = definition.get("kind")
            where = (record_file.name, record.label, name, line.line_number)
            new_value = None
            if kind == "lines":
                if effective == "SCENE" and name == "lines":
                    continue  # taken over from the story with the other chat fields
                scope = ("whole", None) if name == "from_lines" else own_scope
                mode = "single" if (effective, name) in SINGLE_LINE_PLACES else "range"
                new_value = self.convert(line.value, mode, self.scope_for(*scope), where)
            elif kind == "because_list":
                pieces = split_outside_quotes(line.value, ",")
                changed = False
                for position, piece in enumerate(pieces):
                    match = BECAUSE_LINE_PIECE.match(piece)
                    if not match or not parse_quote_anchor(match.group(2)):
                        continue
                    number = self.convert(match.group(2), "single", self.scope_for(*own_scope), where)
                    if number is not None:
                        pieces[position] = f"{match.group(1)}line:{number}"
                        changed = True
                if changed:
                    new_value = ",".join(pieces)
            elif kind == "sub_parts":
                new_value = self.resolve_items(line.value, definition, effective, name, own_scope, record, where)
            if new_value is not None and new_value != line.value:
                self.report.changes.append(where + (line.value, new_value))
                line.value = new_value
                line.changed = True

    def resolve_items(self, value, definition, type_name, name, own_scope, record, where):
        pieces = split_outside_quotes(value, " | ")
        changed = False
        first_definition = definition.get("first_part")
        start = 0
        if first_definition is not None:
            start = 1
            if first_definition.get("kind") == "lines" and pieces:
                mode = "range" if (type_name, name) == ("SCENE", "lines_not_shown") else "single"
                scope = own_scope if own_scope[0] == "scene" or mode == "range" else ("whole", None)
                number = self.convert(pieces[0], mode, self.scope_for(*scope), where)
                if number is not None:
                    leading = pieces[0][:len(pieces[0]) - len(pieces[0].lstrip())]
                    pieces[0] = leading + number
                    changed = True
        first_part = split_item(value, definition).first if first_definition is not None else None
        for position in range(start, len(pieces)):
            match = SUB_PART_PIECE.match(pieces[position])
            if not match:
                continue
            key = normalise_word(match.group(2))
            entry = next((sub for sub in definition.get("sub_parts") or [] if sub.get("key") == key), None)
            if entry is None or entry.get("kind") != "lines":
                continue
            place = (type_name, f"{name} {key}")
            mode = "end" if place in END_LINE_PLACES else ("single" if place in SINGLE_LINE_PLACES else "range")
            if type_name == "STATE" and name == "from" and first_part:
                scope = ("scene", first_part.strip())
            elif type_name == "CHAPTER":
                scope = ("chapter", record.identifier)
            else:
                scope = own_scope
            number = self.convert(match.group(4), mode, self.scope_for(*scope), where)
            if number is not None:
                pieces[position] = f"{match.group(1)}{match.group(2)}{match.group(3)}{number}{match.group(5)}"
                changed = True
        return " | ".join(pieces) if changed else None


# ---------------------------------------------------------------- adopt, part 4: taking over the chat's fields (5.2)

@dataclass
class Reowned:
    """One field code took over: where it is, the chat's value, code's value (None when confirmed) and how."""
    file_name: str
    record: str
    field_name: str
    line_number: int
    old: str
    new: object
    how: str
    type_name: str = ""

    @property
    def changed(self):
        return self.new is not None

    def note(self):
        if self.changed:
            new = self.new if isinstance(self.new, str) else "; ".join(self.new)
            if self.old is None:
                what = f"was missing (the chat app left it out); code wrote {quoted_value(new)} ({self.how})"
            else:
                what = (f"was {quoted_value(self.old)} as the chat app wrote it; code wrote {quoted_value(new)} "
                        f"({self.how})")
        else:
            what = f"{quoted_value(self.old)} as the chat app wrote it is confirmed ({self.how})"
        return Problem("N", REOWN_CHECK_ID, self.record, self.field_name, what,
                       "Nothing to fix: code keeps this field from now on", file_name=self.file_name,
                       line_number=self.line_number)


class FieldOwner:
    """Works out, for each field code keeps that the chat wrote (chat_writer: ai), the value code would write."""

    def __init__(self, schema, index, reading, surface, story_name, fingerprint, excerpt, constants=None):
        self.schema = schema
        self.constants = constants or {}
        self.index = index
        self.reading = reading
        self.surface = surface
        self.story_name = story_name
        self.fingerprint = fingerprint
        self.excerpt = excerpt
        project = next((record for key, record in index.items() if key[0] == "PROJECT"), None)
        self.conditions = ConditionReader(schema, index, (project.get("depth") if project else None) or "standard")
        self.book = ChoiceBook(list(index.values()))
        self.plan = index.get(("PLAN", None))
        self.scenes = {scene.identifier: scene for scene in (reading.scenes if reading else [])}
        self.chapters = {chapter.identifier: chapter for chapter in (reading.chapters if reading else [])}
        self.characters = {character.identifier: character for character in (reading.characters if reading else [])}
        self.headings = {" ".join(scene.heading.split()).upper(): scene.heading for scene in self.scenes.values()}
        self.locked_by_choices = self.records_choices_lock()

    def records_choices_lock(self):
        """IDs an answered or defaulted choice locks: its locks line, and the target of its chosen set value."""
        locked = {}
        for identifier, choice in self.book.choices.items():
            if self.book.status(choice) not in ("answered", "defaulted"):
                continue
            for target in split_list(choice.get("locks") or ""):
                if not is_empty_word(target):
                    locked[target] = identifier
            letter = self.book.chosen_letter(choice)
            set_value = self.book.set_values.get(f"{identifier}-{(letter or '').upper()}") if letter else None
            if set_value is not None and set_value.get("target"):
                locked[set_value.get("target").strip()] = identifier
        return locked

    def reowned_definition(self, record, name):
        """The field's definition when adopt takes it over: code keeps it (code_state or story for this record)
        and the chat wrote it (chat_writer: ai)."""
        if record.type_name == "SETVALUE":
            return None
        definition = self.schema.field(record.type_name, name)
        if not definition or definition.get("chat_writer") != "ai":
            return None
        if self.conditions.writer_for(definition, record) not in ("code_state", "story"):
            return None
        return definition

    # -- code's value for one field: (value or list of values, how) or (None, how) to confirm the chat's value
    def code_value(self, record, name, definition, values):
        type_name = record.type_name
        method = getattr(self, f"value_{type_name.lower()}_{name}", None) or getattr(self, f"value_any_{name}", None)
        if method is None:
            fixed = definition.get("fixed_value")
            if fixed is not None:
                return fixed, "a fixed value"
            allowed = definition.get("values") or []
            if definition.get("kind") == "word" and len(allowed) == 1:
                return allowed[0], "the only value allowed"
            return None, "code has no rule of its own for it, so the chat's value stands"
        return method(record, values)

    def value_project_title(self, record, values):
        if self.reading is None or not self.reading.title:
            return None, "the story given has no title line"
        return clean_title(self.reading.title), "from the story's title line"

    def value_project_source_file(self, record, values):
        return self.story_name, "the story file kept in Original"

    def value_project_source_fingerprint(self, record, values):
        return self.fingerprint, "worked out from the story file"

    def value_project_source_kind(self, record, values):
        return (self.reading.source_kind, "read from the story") if self.reading else (None, "no story read")

    def value_project_source_format(self, record, values):
        return (self.reading.source_format, "read from the story") if self.reading else (None, "no story read")

    def value_project_language(self, record, values):
        return (self.reading.language, "read from the story") if self.reading else (None, "no story read")

    def value_project_surface(self, record, values):
        return self.surface, "the app the tools run in now"

    def value_project_code_execution(self, record, values):
        return "yes", "the tools run on this app"

    def value_project_batch_size(self, record, values):
        if not values:
            default = (constant(self.constants, "batch_size", {}) or {}).get("default")
            return (str(default), "the batch size until the app self-test runs") if default else (None, "")
        return None, "kept until the app self-test runs on this app"

    def plan_value(self, name):
        if self.plan is None or not self.plan.get(name):
            return None, "no story plan to copy it from"
        return self.plan.get(name), "copied from the story plan"

    def value_project_genre(self, record, values):
        return self.plan_value("genre")

    def value_project_tone_home(self, record, values):
        return self.plan_value("tone_home")

    def value_project_tone_range(self, record, values):
        return self.plan_value("tone_range")

    def value_project_scene_id_digits(self, record, values):
        if self.reading is None or not self.reading.scenes or self.reading.source_kind != "screenplay":
            return None, "the scenes come from the plan, not from the story's headings"
        return str(self.reading.scene_id_digits), "from the story's scene count"

    def value_project_schema_version(self, record, values):
        return str(self.schema.data.get("schema_version", "1.0")), "the version of the tools' schema"

    def value_project_checker_last_run(self, record, values):
        return today(), "adopt runs the checker on everything now"

    def value_project_model_facts_date(self, record, values):
        return None, "set when the model facts are refreshed"

    def value_choice_status(self, record, values):
        answer = normalise_word(record.get("answer") or "")
        status = normalise_word(values[0]) if values else ""
        default = normalise_word(split_item(record.get("default") or "").first or "")
        if status in ("answered", "defaulted") and (answer and answer != "open" or status == "defaulted"):
            return None, "it agrees with the choice's answer"
        if answer and answer != "open" and re.fullmatch(r"[a-z]", answer):
            return ("defaulted" if answer == default else "answered"), "worked out from the choice's answer"
        if status in ("answered", "defaulted") and answer == "open":
            return "open", "the choice has no answer yet"
        return None, "it agrees with the choice's answer"

    def value_choice_date(self, record, values):
        status = normalise_word(record.get("status") or "")
        date = (values[0] if values else "").strip()
        if status in ("answered", "defaulted") and (not date or is_empty_word(date)):
            return today(), "the day code took the answer over"
        return None, "the date the chat app recorded"

    def scene_reading(self, record):
        for identifier, scene in self.scenes.items():
            if normalise_word(identifier) == normalise_word(record.identifier or ""):
                return scene
        return None

    def from_scene(self, record, attribute, how="from the story's scene heading"):
        scene = self.scene_reading(record)
        if scene is None:
            return None, "the scene is not in the story given"
        return getattr(scene, attribute), how

    def value_scene_heading(self, record, values):
        return self.from_scene(record, "heading")

    def value_scene_int_ext(self, record, values):
        return self.from_scene(record, "int_ext")

    def value_scene_place_text(self, record, values):
        return self.from_scene(record, "place_text")

    def value_scene_time_text(self, record, values):
        return self.from_scene(record, "time_text")

    def value_scene_transition_in(self, record, values):
        return self.from_scene(record, "transition_in", "from the story's joins")

    def value_scene_transition_out(self, record, values):
        return self.from_scene(record, "transition_out", "from the story's joins")

    def value_scene_lines(self, record, values):
        scene = self.scene_reading(record)
        if scene is not None:
            return range_text(scene.first, scene.last), "the scene's lines, from its heading to the next"
        merged = self.index.get(("SCENE", record.identifier)) or record
        numbers = parse_line_numbers(merged.get("from_lines") or "")
        if numbers and (self.reading is None or self.reading.source_kind != "screenplay"):
            return range_text(numbers[0][0], numbers[-1][1]), "the lines the scene is drawn from (from_lines)"
        return None, "the scene is not in the story given"

    def value_scene_characters(self, record, values):
        scene = self.scene_reading(record)
        if scene is None:
            return None, "the scene is not in the story given"
        return (", ".join(scene.characters) if scene.characters else "none"), "the people the scene's lines name"

    def value_scene_speaking(self, record, values):
        scene = self.scene_reading(record)
        if scene is None:
            return None, "the scene is not in the story given"
        items = [f"{speaker} | cues: {count}" for speaker, count in scene.speaking] or ["none"]
        return items, "counted from the scene's cues"

    def value_scene_target_duration_s(self, record, values):
        return None, "kept from the plan"

    def value_chapter_title(self, record, values):
        chapter = self.chapters.get(record.identifier)
        return (chapter.title, "from the chapter heading") if chapter else (None, "the chapter is not in the story given")

    def value_chapter_lines(self, record, values):
        chapter = self.chapters.get(record.identifier)
        return (range_text(chapter.first, chapter.last), "from the chapter headings") if chapter \
            else (None, "the chapter is not in the story given")

    def value_chapter_words(self, record, values):
        chapter = self.chapters.get(record.identifier)
        return (str(chapter.words), "counted from the chapter") if chapter \
            else (None, "the chapter is not in the story given")

    def value_character_names(self, record, values):
        character = self.characters.get(record.identifier)
        if character is None:
            return None, "the character's cues are not in the story given"
        present = [name.strip() for name in split_list(values[0] if values else "")]
        wanted = {normalise_word(name) for name in present}
        missing = [name for name in character.names if normalise_word(name) not in wanted]
        if not missing:
            return None, "every cue name is among the names"
        return ", ".join(present + missing), "the story's cue names added"

    def value_location_headings(self, record, values):
        present = [piece.strip() for piece in split_outside_quotes(values[0], ";")] if values else []
        if not self.headings:
            return None, "no scene heading of the story given to compare with"
        fixed = [self.headings.get(" ".join(piece.split()).upper(), piece) for piece in present]
        if fixed == present:
            return None, "the headings are written as the story writes them"
        return "; ".join(fixed), "written as the story writes them"

    def value_any_locked(self, record, values):
        lock = self.locked_by_choices.get(record.identifier) or (
            self.locked_by_choices.get(record.type_name) if self.schema.is_singleton(record.type_name) else None)
        if lock and normalise_word(values[0] if values else "") != "yes":
            return "yes", f"a choice the user answered locks it ({plain_name_of(lock)})"
        return None, "the user's approval as the chat app recorded it"

    def value_any_status(self, record, values):
        return None, "as the chat app recorded it"

    def value_shotlist_approved(self, record, values):
        return None, "the group of shots was passed in the chat"


def reown_fields(record_files, owner):
    """Take over every chat-written field code keeps, in place. Returns the list of Reowned."""
    taken = []
    for record_file in record_files:
        for record in record_file.records:
            if not record.known_type:
                continue
            for name in record.field_names():
                definition = owner.reowned_definition(record, name)
                if definition is None:
                    continue
                lines = [line for line in record.field_lines(name) if not line.missing]
                if not lines:
                    continue
                values = [line.value.strip() for line in lines]
                new, how = owner.code_value(record, name, definition, values)
                old_text = "; ".join(values) if definition.get("repeat") else values[0]
                if new is not None:
                    if isinstance(new, list):
                        same = [value_for_comparison(value) for value in values] == \
                               [value_for_comparison(value) for value in new]
                    else:
                        same = len(values) == 1 and same_value(values[0], str(new))
                    if same:
                        new = None
                if new is not None:
                    if isinstance(new, list):
                        record.set_items(name, new, owner.schema)
                    else:
                        record.set_field(name, str(new), owner.schema)
                taken.append(Reowned(record_file.name, record.label, name, lines[0].line_number, old_text, new, how,
                                     record.type_name))
    return taken


def add_missing_fields(record_files, owner):
    """The fields code keeps (chat_writer ai) that the chat left out of PROJECT and of the scene list, added with
    code's value wherever code can work it out (the story's kind and language, the fingerprint, a scene's heading
    and lines ...). A SCENE's list fields go in its 04 Scene list copy."""
    added = []
    copies = {}
    for record_file in record_files:
        for record in record_file.records:
            if record.type_name in ("PROJECT", "SCENE") and record.known_type:
                copies.setdefault(record.key, []).append((record_file, record))
    for key, found in copies.items():
        target_file, target = found[0]
        if key[0] == "SCENE":
            listed = [pair for pair in found if pair[0].name == "04 Scene list.md"]
            if not listed:
                continue
            target_file, target = listed[0]
        for definition in owner.schema.record_types.get(key[0], {}).get("fields", []):
            name = definition["name"]
            if definition.get("part_of") == "design" or any(record.field_lines(name) for _, record in found):
                continue
            if owner.reowned_definition(target, name) is None:
                continue
            value, how = owner.code_value(target, name, definition, [])
            if value is None:
                continue
            if isinstance(value, list):
                target.set_items(name, value, owner.schema)
            else:
                target.set_field(name, str(value), owner.schema)
            added.append(Reowned(target_file.name, target.label, name, None, None, value, how, key[0]))
    return added


# ---------------------------------------------------------------- adopt, part 5: the whole command

@dataclass
class AdoptReport:
    folder: Path = None
    story_file: str = ""
    fingerprint: str = ""
    original_changed: bool = False
    reading_summary: str = ""
    parts: list = dataclass_field(default_factory=list)
    merge_notes: list = dataclass_field(default_factory=list)
    refused: list = dataclass_field(default_factory=list)
    anchors: AnchorReport = None
    reowned: list = dataclass_field(default_factory=list)
    story_points: list = dataclass_field(default_factory=list)
    files_written: list = dataclass_field(default_factory=list)
    history: Path = None

    @property
    def notes(self):
        """Every note adopt logs (N): merged records, the fields taken over and the story points stored."""
        return list(self.merge_notes) + [entry.note() for entry in self.reowned] + list(self.story_points)


def store_story_point_beats_in(record_files, project, constants, story_map):
    """Store the beat each story point resolves to (code_state, 5.4 rule 12), in memory. Returns N notes."""
    if not story_map:
        return []
    speeches = {}
    speeches_path = project.machine_folder / "speeches.json"
    if speeches_path.is_file():
        with open(speeches_path, encoding="utf-8") as handle:
            speeches = speeches_from_json(json.load(handle))
    breakdown = Breakdown(record_files, project.schema, project.words, constants,
                          story=NumberedStory.from_story_map(story_map), speeches=speeches, story_map=story_map,
                          project_folder=project.folder)
    notes = []
    for record_file in record_files:
        for record in record_file.records:
            fields = story_point_fields(project.schema, record.type_name)
            for line in record.fields:
                if line.name not in fields or line.missing:
                    continue
                new_value = with_story_point_beats(breakdown, line.value, record.type_name, line.name)
                if new_value != line.value:
                    beats = ", ".join(re.findall(r"=\s*(SC\d{2,3}[A-Z]?-B\d{2,3})", new_value))
                    notes.append(Problem("N", REOWN_CHECK_ID, record.label, line.name,
                                         f"code stored the beat its story point resolves to ({beats})",
                                         "Nothing to fix: code keeps these beats", file_name=record_file.name,
                                         line_number=line.line_number))
                    line.value = new_value
                    line.changed = True
    return notes


def adopt_project(project, story_path, constants, surface):
    """Everything adopt does before its check: see the note at the top of this file. Returns an AdoptReport."""
    schema = project.schema
    report = AdoptReport(folder=project.folder, story_file=story_path.name)
    with project.lock():
        record_files = project.load_record_files()
        project_file, project_record = project_record_of(record_files)
        if project_record is None:
            raise StageStop(f'"{START_HERE}" holds no PROJECT record, so this is not a breakdown folder. Save '
                            "00 Start here again from the chat app, with its records below the line.")
        stored = (project_record.get("source_fingerprint") or "").strip().lower()
        data_fingerprint = fingerprint_of_bytes(story_path.read_bytes())
        if re.fullmatch(r"[0-9a-f]{64}", stored) and stored != data_fingerprint:
            raise StageStop("This story file is not the one the project was made from (its fingerprint differs from "
                            "the one in 00 Start here). Give the same story file, or start a new project for a "
                            "changed story.")
        history = history_run_folder(project)
        report.history = history
        original_path, report.fingerprint, report.original_changed = keep_story_in_original(project, story_path, history)
        manifest = project.read_manifest()
        manifest["source"] = {"file": f"{ORIGINAL_FOLDER}/{original_path.name}", "fingerprint": report.fingerprint}
        project.write_manifest(manifest)

        # the numbered story, speeches.json and story map.json (never the AI's scene list)
        reading, _, report.reading_summary = read_into_project(project, argparse.Namespace(constants=constants),
                                                               original_path, write_records=False)
        story = StorySource.from_project(project.folder)

        # every record file, and the parts saved beside them
        record_files = project.load_record_files()
        files_by_name = {record_file.name: record_file for record_file in record_files}
        originals = {record_file.name: render_file(record_file, schema) for record_file in record_files}
        report.parts = merge_saved_parts(project, files_by_name, report.merge_notes, report.refused)
        record_files = sorted(files_by_name.values(), key=lambda record_file: (record_file.name[:2], record_file.name))
        index, _ = merge_copies(record_files, schema)

        # quote anchors into line numbers
        resolver = AnchorResolver(story, index, constants)
        for record_file in record_files:
            for record in record_file.records:
                if record.known_type:
                    resolver.resolve_record(record_file, record, schema, project.words)
        report.anchors = resolver.report

        # the fields code keeps that the chat wrote
        index, _ = merge_copies(record_files, schema)
        owner = FieldOwner(schema, index, reading, surface, original_path.name, report.fingerprint, story.excerpt,
                           constants)
        report.reowned = reown_fields(record_files, owner) + add_missing_fields(record_files, owner)

        # the beat each story point resolves to
        report.story_points = store_story_point_beats_in(record_files, project, constants, load_story_map(project.folder))

        # write what changed; the parts go to history
        for record_file in record_files:
            text = render_file(record_file, schema)
            name = record_file.name
            if originals.get(name) == text:
                continue
            path = project.folder / name
            if path.is_file():
                keep_in_history(history, path, name)
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(text)
            report.files_written.append(name)
        for part_name, _, _ in report.parts:
            path = project.folder / part_name
            if path.is_file():
                keep_in_history(history, path, part_name)
                path.unlink()

        # the log and the manifest
        changed = [entry for entry in report.reowned if entry.changed]
        anchors = report.anchors
        summary = (f"Made this folder, saved by hand in a chat app, checkable: the story kept in Original and "
                   f"numbered; {plural(len(report.parts), 'saved part')} merged into the numbered files; "
                   f"{plural(anchors.resolved, 'quote')} turned into line numbers; "
                   f"{plural(len(report.reowned), 'value')} the chat app wrote taken over by the tools "
                   f"({len(changed)} changed).")
        project.add_log_entry(summary)
        manifest = project.read_manifest()
        manifest["source"] = {"file": f"{ORIGINAL_FOLDER}/{original_path.name}", "fingerprint": report.fingerprint}
        manifest["adopt"] = {
            "time": now(), "story": original_path.name, "surface": surface,
            "parts_merged": [{"part": part, "into": target, "records": count} for part, target, count in report.parts],
            "anchors": {"resolved": anchors.resolved, "outside_the_story_given": anchors.outside,
                        "not_found_once": len(anchors.unresolved)},
            "fields_taken_over": {"changed": len(changed), "confirmed": len(report.reowned) - len(changed)},
            "changed": [{"record": entry.record, "type": entry.type_name, "field": entry.field_name}
                        for entry in changed],
            "story_points_stored": len(report.story_points),
        }
        project.write_manifest(project.refresh_manifest(manifest))
        with open(project.log_path, "a", encoding="utf-8") as handle:
            handle.write(json.dumps({"time": now(), "command": "adopt", "notes": [str(note) for note in report.notes]},
                                    ensure_ascii=False) + "\n")
        forget_locked_records(project.folder)
    return report


def add_adopt_arguments(parser):
    parser.add_argument("folder", help="the folder saved from the chat app (the one holding 00 Start here.md), or "
                                       "its ZIP")
    parser.add_argument("story", help="the story file (the same one the chat worked from)")
    parser.add_argument("--surface", choices=["claude_code", "claude_cowork", "claude_web", "chatgpt", "gemini", "other"],
                        help="the app the tools run in now (default: found from the environment)")


def confirmed_summary(reowned):
    """'status on 130 records, locked on 130 records, ...' for the fields confirmed as the chat wrote them."""
    counts = {}
    for entry in reowned:
        if not entry.changed:
            counts[entry.field_name] = counts.get(entry.field_name, 0) + 1
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ", ".join(f"{name} on {plural(count, 'record')}" for name, count in ordered)


class CheckCommandContext:
    """What check's run function reads, for the check adopt runs at its end (check --all)."""

    def __init__(self, context, folder):
        self.arguments = argparse.Namespace(step=None, scene=None, film=False, all=True, story=None)
        self.project = folder
        self.project_folder = folder
        self.schema = context.schema
        self.words = context.words
        self.constants = context.constants
        self.skill_folder = getattr(context, "skill_folder", None)
        self.say = context.say
        self.summary = ""


def run_adopt(context):
    arguments = context.arguments
    story_path = Path(arguments.story).expanduser()
    if not story_path.is_file():
        raise StageStop(f'The story file "{story_path.name}" was not found. Give the path of the story file the chat '
                        "worked from.")
    folder = resolve_input_folder(arguments.folder)
    context.project_folder = folder
    project = Project(folder, context.schema, context.words)
    surface = arguments.surface or detect_surface()
    load_check_families()
    report = adopt_project(project, story_path.resolve(), context.constants, surface)
    say = context.say
    say(f'Adopted "{folder.name}" with the story "{story_path.name}".')
    say(f"- Kept the story in {ORIGINAL_FOLDER}/ with its fingerprint and numbered it: {report.reading_summary}.")
    if report.parts:
        say(f"- Merged {plural(len(report.parts), 'saved part')} into the numbered files by ID (each kept in history):")
        for part, target, count in report.parts:
            say(f'  "{part}" into "{target}" ({plural(count, "record")})')
    elif not report.refused:
        say("- No file was saved in parts.")
    for problem in report.refused:
        say(str(problem))
    anchors = report.anchors
    say(f"- Turned {plural(anchors.resolved, 'quote anchor')} into line numbers."
        + (f" {plural(anchors.outside, 'anchor')} point outside the story given (not in the excerpt) and stay quotes."
           if anchors.outside else "")
        + (f" {plural(len(anchors.unresolved), 'anchor')} could not be found exactly once; the check lists "
           f"{'it' if len(anchors.unresolved) == 1 else 'them'} (CITE-02)." if anchors.unresolved else ""))
    changed = [entry for entry in report.reowned if entry.changed]
    say(f"- Took over {plural(len(report.reowned), 'field')} the chat app wrote for code (chat writer ai): "
        f"{len(changed)} changed, {len(report.reowned) - len(changed)} confirmed. Each is a note:")
    for note in report.merge_notes:
        say(str(note))
    for entry in changed:
        say(str(entry.note()))
    confirmed = confirmed_summary(report.reowned)
    if confirmed:
        say(f"N {REOWN_CHECK_ID} confirmed as the chat app wrote them: {confirmed}. Every note is in "
            f"{MACHINE_FOLDER}/log.jsonl.")
    if report.story_points:
        say(f"- Stored the beat of {plural(len(report.story_points), 'story point')} (code keeps these).")
    try:  # next works only from the list of units applied (C3): the units this folder already holds go on it
        from .make_handout import record_units_found
        found = record_units_found(folder, context.schema, context.words, context.constants)
        if found:
            say(f"- Listed {plural(len(found), 'unit')} whose records the folder holds as done, so stage.py next goes "
                "on from there.")
    except Exception as error:  # the list is a convenience for next; adopting must not fail on it
        say(f"- The units done could not be listed ({type(error).__name__}: {error}); stage.py next may offer them again.")
    say("- The project is now marked as one where code runs. Checking everything (check --all):")
    check_context = CheckCommandContext(context, folder)
    exit_code = run_check(check_context)
    context.summary = (f"adopted: {len(report.parts)} parts merged, {anchors.resolved} anchors resolved, "
                       f"{len(report.reowned)} fields taken over ({len(changed)} changed); check: "
                       f"{check_context.summary}")
    if report.refused:
        say(f"{plural(len(report.refused), 'saved part')} could not be merged (the error lines above); save "
            f"{'it' if len(report.refused) == 1 else 'them'} again from the chat and run adopt again.")
        return 1
    return exit_code


def adopt_report_section(project, result):
    """13 Health check's plain section after an adopt: what the tools took over from the chat app. Shown by the
    check adopt runs, and not again once a later check has run. Plain words only (WORDS-04)."""
    try:
        manifest = project.read_manifest()
    except (OSError, ValueError):
        return []
    adopt = manifest.get("adopt")
    if not adopt:
        return []
    last = (manifest.get("last_check") or {}).get("time")
    if last and last >= adopt.get("time", ""):
        return []
    anchors = adopt.get("anchors", {})
    fields = adopt.get("fields_taken_over", {})
    lines = ["## Taken over from the chat app", ""]
    parts = adopt.get("parts_merged", [])
    if parts:
        lines.append(f"- {plural(len(parts), 'file')} saved in parts {'was' if len(parts) == 1 else 'were'} put "
                     "together with the files they belong to; the parts are kept in the history folder.")
    lines.append(f"- {plural(anchors.get('resolved', 0), 'quote')} that stood for story lines now "
                 f"{'points' if anchors.get('resolved', 0) == 1 else 'point'} to line numbers.")
    if anchors.get("outside_the_story_given"):
        lines.append(f"- {plural(anchors['outside_the_story_given'], 'quote')} stay as quotes, because they point "
                     "to parts of the story that were not given.")
    changed = adopt.get("changed", [])
    total = fields.get("changed", 0) + fields.get("confirmed", 0)
    lines.append(f"- The tools now keep {plural(total, 'detail')} the chat app had to write itself; "
                 f"{fields.get('changed', 0)} of them changed and the rest were kept as they were.")
    shown = []
    for entry in changed[:12]:
        if not isinstance(entry, dict):
            continue
        definition = project.schema.field(entry.get("type", ""), entry.get("field", "")) or {}
        words = (definition.get("label") or entry.get("field", "").replace("_", " ")).lower()
        owner = "the project" if entry.get("type") == "PROJECT" else plain_name_of(entry.get("record", ""))
        shown.append(f"{owner}: {words}")
    if shown:
        lines.append("- Changed: " + "; ".join(shown) + ("; and more." if len(changed) > 12 else "."))
    return lines


register_report_section(adopt_report_section)


# ---------------------------------------------------------------- impact <ID> (5.4 rule 5, principle 8)

@dataclass
class Edge:
    """One place a record cites an ID. citing is the citing record's (TYPE, ID), or ("item", shot ID) for a
    shot-list item; step is the rank of the step that fills the citing field; next_node is the ID the work carries
    on from when the citing record goes stale (None: it stops there); only_from_target marks a link followed only
    from the ID that changes (a scene's own records go stale when the scene changes, not when the scene record goes
    stale because one of its design fields cites a beat)."""
    citing: tuple
    field_name: str
    step: int
    detail: str
    next_node: str
    only_from_target: bool = False


@dataclass
class ImpactEntry:
    key: tuple
    fields: list = dataclass_field(default_factory=list)
    via: list = dataclass_field(default_factory=list)
    details: list = dataclass_field(default_factory=list)
    locked: bool = False
    unit: str = ""
    file_name: str = ""
    step: int = 0

    @property
    def identifier(self):
        return self.key[1] or self.key[0]

    def add(self, edge, node):
        if edge.field_name not in self.fields:
            self.fields.append(edge.field_name)
        if edge.detail and edge.detail != edge.field_name and edge.detail not in self.details:
            self.details.append(edge.detail)
        if node and not node.startswith("item:") and node not in self.via:
            self.via.append(node)
        self.step = max(self.step, edge.step)

    def as_dict(self):
        return {"id": self.identifier, "type": self.key[0], "fields": self.fields, "details": self.details,
                "via": self.via, "locked": self.locked, "unit": self.unit, "file": self.file_name}


@dataclass
class ImpactResult:
    identifier: str
    type_name: str
    file_name: str
    step: int
    unit: str = ""
    direct: list = dataclass_field(default_factory=list)
    stale: list = dataclass_field(default_factory=list)
    upstream: list = dataclass_field(default_factory=list)
    units: list = dataclass_field(default_factory=list)

    def shots_citing(self):
        """The shots that cite the ID themselves, or through their shot-list item."""
        found = []
        for entry in self.direct:
            if entry.key[0] == "SHOT":
                found.append(entry.identifier)
            for detail in entry.details:
                match = re.match(r"^the item for (\S+)$", detail)
                if match:
                    found.append(match.group(1))
        return sorted(set(found), key=sort_key_for_identifier)

    def as_dict(self):
        return {"id": self.identifier, "type": self.type_name, "file": self.file_name, "unit": self.unit,
                "cited_by": [entry.as_dict() for entry in self.direct], "shots_citing": self.shots_citing(),
                "stale": [entry.as_dict() for entry in self.stale],
                "earlier_in_the_work": [entry.as_dict() for entry in self.upstream], "units": self.units}


def field_step(schema, type_name, name):
    """The rank of the step that fills a field (filled_by_step; a checkpoint counts as the step it closes), or of
    the step that designs the record type when the field names none."""
    definition = schema.field(type_name, name) or {}
    step = definition.get("filled_by_step")
    if step is None:
        step = schema.record_types.get(type_name, {}).get("designed_by_step")
    rank = schema.step_rank(step)
    return 0 if rank is None else rank


def record_step(schema, type_name):
    rank = schema.step_rank(schema.record_types.get(type_name, {}).get("designed_by_step"))
    return 0 if rank is None else rank


def looks_like_identifier(schema, text):
    return bool(text) and " " not in text and bool(schema.types_for_id(text))


def impact_edges(run):
    """({cited ID: [Edge]}, [(first, last, Edge)] for ranges): every place a record cites an ID. A shot-list item
    leads to its list and to its shot; a state belongs to its element; a record of a scene file belongs to its
    scene; a range such as SC10-B01..SC10-B08 cites every ID in it."""
    schema = run.schema
    edges = {}
    ranges = []

    def add(cited, edge):
        edges.setdefault(cited, []).append(edge)

    for record_file, record, name, _, identifier, how in references(run):
        if (record.type_name == "SHOTLIST" and name == "item") or how == "range end":
            continue
        step = field_step(schema, effective_type(run, record), name)
        # a story point names a place in the story (its scene and quote) and the beat code resolved it to: the
        # record depends on the story's words there, not on that scene's or beat's records, so these links are
        # listed for the ID that changes but never followed further
        positional = how in ("story point scene", "resolved beat")
        detail = {"resolved beat": f"the beat its story point resolves to, in {name}",
                  "story point scene": f"a story point in it, in {name}"}.get(how, name)
        add(identifier, Edge(record.key, name, step, detail, record.key[1] or record.key[0],
                             only_from_target=positional))
    for record_file, record, line, definition, name in field_values(run):
        if record.type_name == "SHOTLIST" and name == "item":
            continue
        step = field_step(schema, effective_type(run, record), name)
        for piece in split_list(line.value):
            for part in split_outside_quotes(piece, " | "):
                text = part.split(":", 1)[1] if ":" in part else part
                match = RANGE_PIECE.match(text)
                if match and looks_like_identifier(schema, match.group(1)) and looks_like_identifier(schema, match.group(2)):
                    ranges.append((match.group(1), match.group(2),
                                   Edge(record.key, name, step, name, record.key[1] or record.key[0])))
    item_definition = schema.field("SHOTLIST", "item") or {}
    list_step = field_step(schema, "SHOTLIST", "item")
    for shotlist in run.records("SHOTLIST", include_omitted=True):
        for value in shotlist.get_all("item"):
            item = split_item(value, item_definition)
            shot = (item.first or "").strip()
            if not shot:
                continue
            node = f"item:{shot}"
            add(node, Edge(shotlist.key, "item", list_step, f"the item for {shot}", None))
            if run.index.get(("SHOT", shot)) is not None:
                add(node, Edge(("SHOT", shot), "its shot-list item", record_step(schema, "SHOT"),
                               "its shot-list item", shot))
            for sub_key in ("beats", "subject"):
                for piece in split_list(item.get(sub_key) or ""):
                    edge = Edge(("item", shot), f"item {sub_key}", list_step, f"the item for {shot}", node)
                    match = RANGE_PIECE.match(piece)
                    if match:
                        ranges.append((match.group(1), match.group(2), edge))
                    elif not is_empty_word(piece):
                        add(piece.strip(), edge)
    for key, record in run.index.items():
        identifier = key[1] or ""
        state = STATE_IDENTIFIER.match(identifier)
        if key[0] == "STATE" and state:
            add(state.group("element"), Edge(key, "a state of it", record_step(schema, "STATE"), "a state of it",
                                             identifier))
        scene = scene_of(identifier) if key[0] in SCENE_FILE_TYPES and key[0] != "SCENE" else None
        if scene:
            add(scene, Edge(key, "a record of the scene", record_step(schema, key[0]), "a record of the scene",
                            identifier, only_from_target=True))
    return edges, ranges


def unit_for(key, step, manifest, index):
    """The unit that writes a record (steps.json units), or a plain description when it cannot be named."""
    type_name, identifier = key
    scene = scene_of(identifier or "")
    if type_name in ("SHOT", "CUT"):
        batches = (manifest.get("batches") or {}).get(scene) or {}
        for unit, entry in batches.items():
            first, last = entry.get("first"), entry.get("last")
            if first and last and sort_key_for_identifier(first) <= sort_key_for_identifier(identifier) \
                    <= sort_key_for_identifier(last):
                return unit
        return f"U-08-{scene}-B?"
    if type_name in ("PART", "BEAT", "MOVE", "SETUP", "SHOTLIST", "SPEECH"):
        return f"U-07-{scene}"
    if type_name == "SCENE":
        if step >= 7:
            return f"U-07-{identifier}"
        for entry in manifest.get("units_done") or []:
            unit = entry.get("unit", "") if isinstance(entry, dict) else str(entry)
            match = re.match(r"^U-02-(SC\d{2,3}[A-Z]?)\.\.(SC\d{2,3}[A-Z]?)$", unit)
            if match and sort_key_for_identifier(match.group(1)) <= sort_key_for_identifier(identifier) \
                    <= sort_key_for_identifier(match.group(2)):
                return unit
        return f"U-02 (the event unit that holds {identifier})"
    if type_name == "CHAPTER":
        return f"U-02-{identifier}"
    if type_name in ("CHARACTER", "VOICE"):
        record = index.get(key)
        owner = identifier if type_name == "CHARACTER" else (record.get("character") if record is not None else None)
        return f"U-04-{owner}" if owner else "U-04 (the character's unit)"
    if type_name == "STATE":
        record = index.get(key)
        start = split_item(record.get("from") or "").first if record is not None and record.get("from") else ""
        return f"U-05 (the continuity unit that holds {(start or '').strip() or 'its first scene'})"
    for prefix, unit in (("PIC", "U-12-{scene} or U-14-{scene}"), ("PV", "U-13-{scene}"), ("TK", "U-14-TAKES-{scene}")):
        if type_name in ("PIC", "PREVIS", "TAKE") and (identifier or "").startswith(prefix + "-"):
            match = re.match(r"^[A-Z]+-(SC\d{2,3}[A-Z]?)", identifier)
            if match:
                return unit.format(scene=match.group(1))
    if type_name in ("CHOICE", "SETVALUE"):
        return "a choice for the user"
    return UNIT_OF_TYPE.get(type_name, "none (code keeps it)")


def impact_of(record_files, identifier, schema, words, constants, story=None, manifest=None):
    """What depends on an ID (see the note at the top of this file). Stops with exit 2 when no record or item has
    the ID. Changes nothing."""
    manifest = manifest or {}
    run = CheckRun(record_files, schema, words, constants, story=story, manifest=manifest)
    identifier = identifier.strip()
    exists, record = identifier_exists(run, identifier)
    if not exists and schema.knows_type(identifier.upper()) and run.record(identifier.upper()) is not None:
        identifier = identifier.upper()
        exists, record = True, run.record(identifier)
    if not exists:
        raise StageStop(f'No record or item has the ID "{identifier}". Give an ID as the records write it, for '
                        "example SC10-B07 or CH-IONA.")
    declared = declared_identifiers(run)
    if record is not None:
        type_name = record.type_name
        file_name = record.file_name or ""
        start_step = field_step(schema, "SCENE", "event") if type_name == "SCENE" else record_step(schema, type_name)
    elif identifier in declared:
        type_name, declaring = declared[identifier]
        file_name = declaring.file_name or ""
        start_step = field_step(schema, declaring.type_name, "value" if type_name == "VALUE" else "item")
    elif identifier in run.speeches:
        type_name, file_name, start_step = "SPEECH", f"{MACHINE_FOLDER}/speeches.json", 1
    else:
        type_name, file_name, start_step = "CLIP", "", record_step(schema, "SHOT")
    result = ImpactResult(identifier, type_name, file_name, start_step)
    edges, ranges = impact_edges(run)
    list_of_shot = {}
    for shotlist in run.records("SHOTLIST", include_omitted=True):
        for value in shotlist.get_all("item"):
            list_of_shot.setdefault((split_item(value).first or "").strip(), shotlist.key)

    def edges_citing(node):
        found = list(edges.get(node, []))
        for first, last, edge in ranges:
            if id_in_range(node, first, last):
                found.append(edge)
        return found

    target_keys = {record.key} if record is not None else set()
    direct, stale, upstream = {}, {}, {}
    seen = {identifier}
    queue = [identifier]
    # Downstream only: a record goes stale through a field filled at or after the step of the record it cites
    # (node_step), so the work never runs back up to an earlier step (a camera rule of step 6 does not make the
    # character of step 4 stale). Other records name a scene as a place in the story (a state's first scene, a
    # sequence's scenes, the project's scope), so a scene record that goes stale is not followed further.
    node_step = {identifier: start_step}
    while queue:
        node = queue.pop(0)
        if node != identifier and SCENE_IDENTIFIER.match(node):
            continue
        for edge in edges_citing(node):
            if edge.only_from_target and node != identifier:
                continue
            citing = edge.citing
            shown = list_of_shot.get(citing[1], citing) if citing[0] == "item" else citing
            if shown in target_keys:
                continue
            merged = run.index.get(shown)
            if merged is not None and run.is_omitted(merged):
                continue
            if node == identifier:
                direct.setdefault(shown, ImpactEntry(shown)).add(edge, node)
            if edge.step < node_step.get(node, start_step) or shown[0] in ("CHOICE", "SETVALUE"):
                # earlier in the work, or a choice: the user's answer stands until the user is asked again
                if node == identifier:
                    upstream.setdefault(shown, direct[shown])
                continue
            stale.setdefault(shown, ImpactEntry(shown)).add(edge, node)
            if edge.next_node and edge.next_node not in seen:
                seen.add(edge.next_node)
                next_type = shown[0] if shown[0] != "item" else "SHOTLIST"
                node_step[edge.next_node] = max(edge.step if edge.next_node.startswith("item:") else 0,
                                                record_step(schema, next_type))
                queue.append(edge.next_node)
    for entry in list(direct.values()) + list(stale.values()):
        merged = run.index.get(entry.key)
        entry.locked = merged is not None and normalise_word(merged.get("locked") or "") == "yes"
        entry.file_name = (merged.file_name if merged is not None else "") or ""
        entry.unit = unit_for(entry.key, entry.step, manifest, run.index)
    if record is not None:
        result.unit = unit_for(record.key, start_step, manifest, run.index)
    units = []
    unknown_batches = {}
    for entry in sorted(stale.values(), key=lambda item: (record_step(schema, item.key[0]),
                                                           sort_key_for_identifier(item.identifier))):
        if entry.unit.endswith("-B?"):
            unknown_batches.setdefault(entry.unit[:-3], []).append(entry.identifier)
            entry.unit = f"{entry.unit[:-3]} (the batch that holds {entry.identifier})"
            continue
        if entry.unit not in units and not entry.unit.startswith(("none", "a choice")):
            units.append(entry.unit)
    for unit, identifiers in unknown_batches.items():
        units.append(f"{unit} (the {'batch that holds' if len(identifiers) == 1 else 'batches that hold'} "
                     f"{', '.join(identifiers)})")
    for entry in direct.values():
        if entry.unit.endswith("-B?"):
            entry.unit = f"{entry.unit[:-3]} (the batch that holds {entry.identifier})"
    if result.unit.endswith("-B?"):
        result.unit = f"{result.unit[:-3]} (the batch that holds {identifier})"

    def order(entry):
        return (record_step(schema, entry.key[0]), sort_key_for_identifier(entry.identifier))
    result.direct = sorted(direct.values(), key=order)
    result.stale = sorted(stale.values(), key=order)
    result.upstream = sorted(upstream.values(), key=order)
    result.units = units
    return result


def add_impact_arguments(parser):
    parser.add_argument("identifier", help="the ID of the record or item that changes, for example SC10-B07")
    parser.add_argument("--json", action="store_true", help="print the result as JSON for other tools")


def run_impact(context):
    project = Project(context.project, context.schema, context.words)
    record_files = project.load_record_files()
    story = StorySource.from_project(project.folder)
    result = impact_of(record_files, context.arguments.identifier, context.schema, context.words, context.constants,
                       story=story, manifest=project.read_manifest())
    context.summary = (f"{result.identifier}: cited by {len(result.direct)}, {len(result.stale)} stale, "
                       f"{len(result.units)} units")
    if getattr(context.arguments, "json", False):
        context.say(json.dumps(result.as_dict(), ensure_ascii=False, indent=1))
        return 0
    say = context.say
    where = f", in {result.file_name}" if result.file_name else ""
    own_unit = f"; its own unit is {result.unit}" if result.unit else ""
    say(f"Impact of {plain_name_of(result.identifier)} ({result.identifier}, {result.type_name}{where}{own_unit}).")
    if not result.direct:
        say("No record cites it, so a change to it touches nothing else.")
        return 0
    earlier = {entry.key for entry in result.upstream}
    say(f"Cited directly by {plural(len(result.direct), 'record')}:")
    for entry in result.direct:
        extra = f" ({'; '.join(entry.details)})" if entry.details else ""
        note = ""
        if entry.key in earlier:
            note = (" - a choice the user answered; it stands unless the user is asked again"
                    if entry.key[0] in ("CHOICE", "SETVALUE") else " - earlier in the work, so it stays as it is")
        say(f"- {entry.identifier} ({entry.key[0]}{', locked' if entry.locked else ''}): "
            f"{', '.join(entry.fields)}{extra}{note}")
    shots = result.shots_citing()
    if shots:
        say(f"Shots that cite it: {', '.join(shots)}.")
    say(f"Go stale if it changes ({plural(len(result.stale), 'record')}, following the work downstream only):")
    for entry in result.stale:
        via = [item for item in entry.via if item != result.identifier]
        through = f" through {', '.join(via)}" if via else ""
        say(f"- {entry.identifier} ({entry.key[0]}{', locked' if entry.locked else ''}){through}; unit {entry.unit}")
    if result.units:
        say(f"Units to redo: {', '.join(result.units)}.")
    locked = [entry for entry in result.stale if entry.locked]
    if locked:
        say(f"{plural(len(locked), 'of these records is', 'of these records are')} locked: "
            f"{'it changes' if len(locked) == 1 else 'they change'} only through a choice the user answers, which "
            "then marks what cites it stale.")
    return 0


# ---------------------------------------------------------------- questions --sample [--seed N] (11.2)

@dataclass
class Question:
    number: int
    scene: str
    record: str
    asked_because: str
    text: str
    lines: list
    cites: list
    batch: int = 0

    def as_dict(self):
        return {"number": self.number, "scene": self.scene, "record": self.record,
                "asked_because": self.asked_because, "question": self.text, "lines": self.lines,
                "cites": self.cites, "unit": QUESTION_UNIT.format(number=self.batch)}


class QuestionMaker:
    """Builds the yes/no questions of 11.2 from the records, each citing the story lines it can be checked against."""

    def __init__(self, run, speeches, breakdown=None):
        self.run = run
        self.index = run.index
        self.speeches = speeches
        self.breakdown = breakdown
        self.story = run.story

    # -- words
    def lines_of(self, record, name="lines"):
        value = record.get(name) or ""
        numbers = parse_line_numbers(value)
        if numbers:
            return [numbers[0][0], numbers[-1][1]]
        return None

    def lines_words(self, record, name="lines"):
        numbers = self.lines_of(record, name)
        if numbers:
            return lines_in_words(*numbers)
        value = record.get(name)
        if value and parse_quote_anchor(value):
            return "the lines " + single_quoted(value)
        return "its lines"

    def shot_words(self, shot):
        match = re.search(r"-SH(\d+)$", shot.identifier or "")
        return f"shot {match.group(1)}" if match else plain_name_of(shot.identifier)

    def beat_words(self, beat):
        match = re.search(r"-B0*(\d+)$", beat.identifier or "")
        return f"beat {match.group(1)}" if match else plain_name_of(beat.identifier)

    def name(self, identifier):
        return character_name(self.index, identifier)

    def speech_opening(self, text):
        sentences = [piece for piece in SENTENCE_END.split(text.strip()) if piece]
        if len(sentences) > 1:
            return sentences[0].rstrip(".!?") + "..."
        return text.strip()

    def speech_lines(self, speech_identifier):
        entry = self.speeches.get(speech_identifier) or {}
        lines = entry.get("lines")
        if lines:
            return lines_in_words(lines[0], lines[-1])
        record = self.index.get(("SPEECH", speech_identifier))
        if record is not None:
            numbers = self.lines_of(record, "line")
            if numbers:
                return lines_in_words(*numbers)
        return "its lines"

    def speech_text(self, speech_identifier, words=None):
        entry = self.speeches.get(speech_identifier) or {}
        if entry.get("text"):
            return entry["text"]
        record = self.index.get(("SPEECH", speech_identifier))
        if record is not None and record.get("text"):
            return record.get("text").strip('"“”')
        return (words or "").strip('"“”')

    def speaker_of(self, speech_identifier):
        entry = self.speeches.get(speech_identifier) or {}
        if entry.get("speaker"):
            return entry["speaker"]
        record = self.index.get(("SPEECH", speech_identifier))
        return record.get("speaker") if record is not None else None

    # -- what each shot needs
    def needs(self, shot):
        """The handling needs of a shot: 'mirror', 'text', 'violence' (11.2)."""
        found = []
        route = None
        if self.breakdown is not None:
            try:
                route = mirror_route(self.breakdown, self.breakdown.record(shot.identifier, "SHOT") or shot).route
            except Exception:  # the derivation needs records a partial project may lack; the fields below still work
                route = None
        glass = [value for value in shot.get_all("glass") if not is_empty_word(value)]
        filmed = normalise_word(shot.get("kind") or "") not in ("card", "black")
        if filmed and (route in MIRROR_ROUTES or normalise_word(shot.get("flip") or "") == "never" or glass):
            found.append("mirror")
        texts = [piece for piece in split_list(shot.get("text") or "") if not is_empty_word(piece)]
        if texts or normalise_word(shot.get("kind") or "") in ("screen", "card"):
            found.append("text")
        flags = [normalise_word(piece) for piece in split_list(shot.get("content_flags") or "")]
        if any(flag in VIOLENCE_FLAGS for flag in flags):
            found.append("violence")
        return found

    # -- the questions
    def shot_questions(self, shot, reasons, turn_beats):
        where = self.shot_words(shot)
        lines = self.lines_words(shot)
        numbers = self.lines_of(shot)
        cites = [shot.identifier]
        questions = []

        def ask(text, extra_cites=(), extra_lines=None):
            questions.append((single_quoted(text), cites + [item for item in extra_cites if item not in cites],
                              extra_lines or numbers))

        purpose = shot.get("purpose")
        if purpose:
            ask(f"Shot {where[5:]} ({lines}): does the story support what the shot is for, '{purpose}'?")
        if "turn shot" in reasons:
            for beat_identifier in split_list(shot.get("beats") or ""):
                beat = self.index.get(("BEAT", beat_identifier))
                if beat is None or beat.key not in turn_beats:
                    continue
                ask(f"Shot {where[5:]} is the turn shot of {self.beat_words(beat)} ({self.lines_words(beat)}): does "
                    f"the scene turn inside this shot's {lines}, as the story writes the turn?", [beat.identifier],
                    self.lines_of(beat))
            why = shot.get("why")
            if why:
                ask(f"Shot {where[5:]} ({lines}): does the story support the reason it gives, '{why}'?")
        subjects = [item for item in shot.get_all("subject")]
        definition = self.run.schema.field("SHOT", "subject") or {}
        for value in subjects[:2]:
            item = split_item(value, definition)
            does = item.get("does")
            if not does or is_empty_word(does):
                continue
            ask(f"Shot {where[5:]} ({lines}): does the story have {self.name(item.first)} do what the shot shows, "
                f"'{does}', with nothing added that the story does not write or imply?", [item.first.strip()])
        hear_definition = self.run.schema.field("SHOT", "hear") or {}
        for value in shot.get_all("hear"):
            item = split_item(value, hear_definition)
            speech = (item.first or "").strip()
            if not speech or is_empty_word(speech):
                continue
            speaker = self.speaker_of(speech)
            text = self.speech_text(speech, item.get("words"))
            where_heard = normalise_word(item.get("speaker") or "")
            if speaker and text:
                who, said = self.name(speaker), f"'{self.speech_opening(text)}'"
                owner = f"{who}'s {said}"
            else:
                # the speeches are not known here (no story read): name the speech by its ID
                who, said = "the speaker", f"speech {speech}"
                owner = said
            if where_heard == "off_screen":
                ask(f"Shot {where[5:]}: is {owner} heard with {who} off screen, and does the story allow "
                    f"it ({self.speech_lines(speech)})?", [speech])
            elif where_heard == "on_screen":
                ask(f"Shot {where[5:]}: does the story let {who} be seen saying {said} "
                    f"({self.speech_lines(speech)})?", [speech])
            else:
                ask(f"Shot {where[5:]}: is {owner} heard the way the story has it "
                    f"({self.speech_lines(speech)})?", [speech])
        if "must-keep shot" in reasons:
            shows = self.list_item_shows(shot) or purpose
            if shows:
                ask(f"Shot {where[5:]} ({lines}): does the story need what it shows, '{shows}', so that the scene "
                    "would lose something the story writes without it?")
        if "keeps a fact hidden" in reasons:
            for value in shot.get_all("keep_hidden"):
                item = split_item(value)
                fact_identifier = (item.first or "").strip()
                if not fact_identifier or is_empty_word(fact_identifier):
                    continue
                fact = self.index.get(("FACT", fact_identifier))
                secret = (fact.title if fact is not None and fact.title else fact_identifier)
                how = item.get("how")
                ask(f"Shot {where[5:]} ({lines}) says it keeps a secret from the audience, '{secret}'"
                    + (f", by {how}" if how and not is_empty_word(how) else "") +
                    ": does the picture really keep it hidden until the story reveals it, even with what the shot "
                    "must show?", [fact_identifier])
        if "mirror" in reasons:
            side_line = self.side_line(numbers)
            if side_line:
                number, text = side_line
                ask(f"Shot {where[5:]}: does every side it shows agree with the story's '{text}' (line {number}), "
                    "counting sides as the person's own and as the audience sees them?", extra_lines=numbers)
            else:
                ask(f"Shot {where[5:]} ({lines}) shows sides the audience may see mirrored: does every hand, ring or "
                    "mark keep the side the story gives it?")
        if "text" in reasons:
            texts = [piece for piece in split_list(shot.get("text") or "") if not is_empty_word(piece)]
            for text_identifier in texts or [None]:
                record = self.index.get(("TEXT", text_identifier)) if text_identifier else None
                words = record.get("words") if record is not None else None
                if words:
                    ask(f"Shot {where[5:]} ({lines}): are the words it shows, '{words}', the story's own, and do they "
                        "read the way round the story needs on screen?", [text_identifier])
                else:
                    ask(f"Shot {where[5:]} ({lines}): is the text it shows written as the story writes it, and does "
                        "it read the right way round?")
        if "violence" in reasons:
            flags = [normalise_word(piece).replace("_", " ") for piece in split_list(shot.get("content_flags") or "")
                     if normalise_word(piece) in VIOLENCE_FLAGS]
            ask(f"Shot {where[5:]} ({lines}): does it show only the harm the story writes ({', '.join(flags)}), with "
                "the cause, the reaction and what follows where the story has them?")
        return questions

    def list_item_shows(self, shot):
        definition = self.run.schema.field("SHOTLIST", "item") or {}
        for shotlist in self.run.records("SHOTLIST"):
            for value in shotlist.get_all("item"):
                item = split_item(value, definition)
                if (item.first or "").strip() == shot.identifier:
                    return item.get("shows")
        return None

    def side_line(self, numbers):
        """(line, text) of the first story line in the shot's lines that names a side (left or right)."""
        if not numbers or self.story is None:
            return None
        for number in range(numbers[0], numbers[1] + 1):
            text = self.story.numbered.line(number).strip()
            if SIDE_WORDS.search(text):
                sentences = [piece for piece in SENTENCE_END.split(text) if piece]
                if len(text.split()) > 15:
                    text = next((piece for piece in sentences if SIDE_WORDS.search(piece)), text)
                return number, text.strip()
        return None

    def beat_questions(self, beat, scene):
        where = self.beat_words(beat)
        lines = self.lines_words(beat)
        numbers = self.lines_of(beat)
        cites = [beat.identifier]
        questions = []

        def ask(text, extra=()):
            questions.append((single_quoted(text), cites + list(extra), numbers))

        change = self.value_change(beat, scene)
        if change:
            value_name, before, after, value_identifier = change
            ask(f"{where[:1].upper()}{where[1:]} ({lines}): does the story turn here, so that '{value_name}' goes from "
                f"{before} to {after}?", [value_identifier])
        else:
            ask(f"{where[:1].upper()}{where[1:]} ({lines}): does the story turn here, as the beat says?")
        if scene is not None:
            definition = self.run.schema.field("SCENE", "turn_picture") or {}
            for value in scene.get_all("turn_picture"):
                item = split_item(value, definition)
                if (item.first or "").strip() == beat.identifier and item.get("picture"):
                    ask(f"{where[:1].upper()}{where[1:]} ({lines}): can the turn be seen in one frame, as its turn "
                        f"picture says, '{item.get('picture')}', and does the story allow that picture?", [scene.key[1]])
        five_definition = self.run.schema.field("BEAT", "five_steps") or {}
        for value in beat.get_all("five_steps"):
            item = split_item(value, five_definition)
            if normalise_word(item.first or "") == "expression" and item.get("shows"):
                ask(f"{where[:1].upper()}{where[1:]} ({lines}): does the story show this, '{item.get('shows')}'?")
        unsaid_definition = self.run.schema.field("BEAT", "unsaid") or {}
        for value in beat.get_all("unsaid"):
            item = split_item(value, unsaid_definition)
            if item.get("thought"):
                who = self.name(item.first)
                ask(f"{where[:1].upper()}{where[1:]} ({lines}): does the story leave unsaid what {who} thinks here, "
                    f"'{item.get('thought')}', so that no line speaks it?", [item.first.strip()])
        return questions

    def value_change(self, beat, scene):
        """(value name, charge before, charge after, value ID) for a value whose charge changes sign at the beat."""
        if scene is None:
            return None
        values = {}
        definition = self.run.schema.field("SCENE", "value") or {}
        for value in scene.get_all("value"):
            item = split_item(value, definition)
            values[(item.first or "").strip()] = item
        beats = sorted((record for record in self.run.records("BEAT") if scene_of(record.identifier) == scene.key[1]),
                       key=lambda record: sort_key_for_identifier(record.identifier))
        position = next((index for index, record in enumerate(beats) if record.identifier == beat.identifier), None)
        charge_definition = self.run.schema.field("BEAT", "charge") or {}

        def charges(record):
            found = {}
            for value in record.get_all("charge"):
                item = split_item(value, charge_definition)
                found[(item.first or "").strip()] = (item.get("charge") or "").strip()
            return found

        now_charges = charges(beat)
        before_charges = charges(beats[position - 1]) if position else {}

        def sign(text):
            return 1 if text.startswith("+") else (-1 if text.startswith("-") else 0)

        for value_identifier, after in now_charges.items():
            before = before_charges.get(value_identifier) or (values.get(value_identifier).get("open")
                                                             if value_identifier in values else None)
            if before is None or sign(before) == sign(after):
                continue
            item = values.get(value_identifier)
            name = item.get("name") if item is not None else value_identifier
            return name, before, after, value_identifier
        return None


def select_and_ask(run, speeches, breakdown, sample, seed, share, scene_filter=None):
    """[(scene, record, reason, [(text, cites, lines)])] for the records 11.2 names, then the seeded sample."""
    maker = QuestionMaker(run, speeches, breakdown)
    shots = [shot for shot in run.records("SHOT") if run.in_scope(shot)
             and (scene_filter is None or scene_of(shot.identifier) == scene_filter)]
    beats = [beat for beat in run.records("BEAT") if run.in_scope(beat)
             and (scene_filter is None or scene_of(beat.identifier) == scene_filter)]
    turn_beats = {beat.key for beat in beats if normalise_word(beat.get("turn") or "none") not in ("none", "")}
    groups = []
    chosen = []
    rest = []
    for shot in sorted(shots, key=lambda record: sort_key_for_identifier(record.identifier)):
        reasons = []
        role = normalise_word(shot.get("role") or "")
        if role == "turn":
            reasons.append("turn shot")
        if role == "must_keep":
            reasons.append("must-keep shot")
        if any(not is_empty_word(split_item(value).first or "none") for value in shot.get_all("keep_hidden")):
            reasons.append("keeps a fact hidden")  # INFO-01 trusts keep_hidden, so a reader checks the hiding
        reasons += maker.needs(shot)
        if reasons:
            chosen.append((shot, reasons))
        else:
            rest.append(shot)
    sampled = []
    if rest:
        if sample:
            # the seeded share: random.Random(seed).sample of the other shots in ID order, so a seed gives the same
            # sample again (count: question_sample_share of them, rounded up, at least one)
            count = min(len(rest), max(1, math.ceil(share * len(rest))))
            sampled = random.Random(seed).sample(rest, count)
        else:
            sampled = list(rest)
    sampled_keys = {shot.key for shot in sampled}
    for beat in sorted(beats, key=lambda record: sort_key_for_identifier(record.identifier)):
        if beat.key in turn_beats:
            scene = run.index.get(("SCENE", scene_of(beat.identifier)))
            groups.append((scene_of(beat.identifier), beat.identifier, "turn beat", maker.beat_questions(beat, scene)))
    for shot, reasons in chosen:
        groups.append((scene_of(shot.identifier), shot.identifier, ", ".join(reasons),
                       maker.shot_questions(shot, reasons, turn_beats)))
    for shot in rest:
        if shot.key in sampled_keys:
            groups.append((scene_of(shot.identifier), shot.identifier, "sampled" if sample else "every shot",
                           maker.shot_questions(shot, [], turn_beats)))
    groups.sort(key=lambda group: (sort_key_for_identifier(group[0] or ""),
                                   0 if "-B" in group[1] and "-SH" not in group[1] else 1,
                                   sort_key_for_identifier(group[1])))
    counts = {"turn shots": sum(1 for _, reasons in chosen if "turn shot" in reasons),
              "turn beats": len(turn_beats),
              "must-keep shots": sum(1 for _, reasons in chosen if "must-keep shot" in reasons),
              "shots keeping a fact hidden": sum(1 for _, reasons in chosen if "keeps a fact hidden" in reasons),
              "shots needing mirror, text or violence handling": sum(
                  1 for _, reasons in chosen if set(reasons) & {"mirror", "text", "violence"}),
              "other shots": len(rest), "other shots asked about": len(sampled),
              "other shot list": [shot.identifier for shot in rest]}
    return groups, counts


def batch_questions(groups, batch_size):
    """Number the questions and put them in batches of batch_size, keeping one record's questions together where
    they fit."""
    questions = []
    batch = 1
    in_batch = 0
    number = 0
    for scene, record, reason, asked in groups:
        if not asked:
            continue
        if in_batch and in_batch + len(asked) > batch_size:
            batch += 1
            in_batch = 0
        for text, cites, lines in asked:
            if in_batch >= batch_size:
                batch += 1
                in_batch = 0
            number += 1
            in_batch += 1
            questions.append(Question(number, scene, record, reason, text, lines, cites, batch))
    return questions


def questions_text(questions, seed, sample):
    """The questions as the fresh units read them, one part per batch (questions.md)."""
    lines = ["# Review questions", "",
             "Each batch is one fresh unit that wrote none of these records (U-10-QUESTIONS-B1 and on). Answer each "
             "question yes or no against the story, reading only the records and the lines it cites. Write one REVIEW "
             "per scene (### REVIEW RV-SC10, - scope: SC10) with one line per question: - answer: <the question, word "
             "for word> | answer: yes | evidence: <the story's words or the shot and moment>. Each no also becomes a "
             "FINDING with source: review. An answer without evidence is dropped.", "",
             f"Made {today()}; " + (f"a sample with seed {seed}." if sample else "every shot."), ""]
    batches = {}
    for question in questions:
        batches.setdefault(question.batch, []).append(question)
    for batch, items in batches.items():
        lines.append(f"## {QUESTION_UNIT.format(number=batch)} ({plural(len(items), 'question')})")
        lines.append("")
        for question in items:
            cited = f"; cites {', '.join(question.cites)}" if question.cites else ""
            lines.append(f"{question.number}. {question.text} [{question.record}, {question.asked_because}{cited}]")
        lines.append("")
    return "\n".join(lines)


def make_questions(project, constants, sample=True, seed=None, scene=None):
    """Build, number and batch the questions of a project. Returns (questions, counts, seed)."""
    record_files = project.load_record_files()
    story = StorySource.from_project(project.folder)
    run = CheckRun(record_files, project.schema, project.words, constants, story=story,
                   manifest=project.read_manifest())
    breakdown = None
    try:
        breakdown = Breakdown.from_project(project.folder, project.schema, project.words, constants)
    except Exception:  # questions do not need the derived fields; mirror needs fall back to the shot's own fields
        breakdown = None
    speeches = dict(run.speeches or {})
    share = float(constant(constants, "question_sample_share", 0.1))
    batch_size = int(constant(constants, "question_batch_size", 40))
    seed = 1 if seed is None else seed
    groups, counts = select_and_ask(run, speeches, breakdown, sample, seed, share, scene)
    return batch_questions(groups, batch_size), counts, seed


def add_questions_arguments(parser):
    parser.add_argument("--sample", action="store_true",
                        help="ask about every turn shot, turn beat and must-keep shot, every shot that needs mirror, "
                             "text or violence handling, and a seeded share of the other shots "
                             "(question_sample_share); without it every shot is asked about")
    parser.add_argument("--seed", type=int, help="the seed of the sample, so it can be made again (default: 1)")
    parser.add_argument("--scene", help="only this scene, for example SC10")


def run_questions(context):
    arguments = context.arguments
    project = Project(context.project, context.schema, context.words)
    scene = None
    if getattr(arguments, "scene", None):
        scene = read_scene(arguments.scene)
    questions, counts, seed = make_questions(project, context.constants, bool(arguments.sample), arguments.seed, scene)
    if not questions:
        raise StageStop("There are no shots or turn beats to ask about yet: the review questions come after the shot "
                        "details (step 9 of 12).")
    batches = sorted({question.batch for question in questions})
    other_shots = counts.pop("other shot list", [])
    data = {"made": now(), "seed": seed if arguments.sample else None, "sample": bool(arguments.sample),
            "scene": scene, "counts": counts, "other_shots": other_shots,
            "batches": [{"unit": QUESTION_UNIT.format(number=batch),
                         "questions": [question.as_dict() for question in questions if question.batch == batch]}
                        for batch in batches]}
    machine = project.machine_folder
    machine.mkdir(parents=True, exist_ok=True)
    history = None
    for name, text in ((QUESTIONS_FILE, json.dumps(data, ensure_ascii=False, indent=1) + "\n"),
                       (QUESTIONS_TEXT_FILE, questions_text(questions, seed, bool(arguments.sample)) + "\n")):
        path = machine / name
        if path.is_file():
            history = history or history_run_folder(project)
            keep_in_history(history, path, f"{MACHINE_FOLDER}/{name}")
        path.write_text(text, encoding="utf-8")
    manifest = project.read_manifest()
    manifest["questions"] = {"made": data["made"], "seed": data["seed"], "sample": data["sample"],
                             "count": len(questions), "units": [batch["unit"] for batch in data["batches"]],
                             "file": f"{MACHINE_FOLDER}/{QUESTIONS_FILE}"}
    project.write_manifest(manifest)
    say = context.say
    asked = ", ".join(f"{count} {name}" for name, count in counts.items() if not name.startswith("other shots"))
    others = (f"{counts['other shots asked about']} of the {counts['other shots']} other shots"
              + (f" (a seeded sample, seed {seed})" if arguments.sample else ""))
    say(f"Wrote {plural(len(questions), 'question')} in {plural(len(batches), 'batch', 'batches')} of at most "
        f"{int(constant(context.constants, 'question_batch_size', 40))}, about {asked}, and {others}.")
    say(f"Files: {MACHINE_FOLDER}/{QUESTIONS_FILE} and {QUESTIONS_TEXT_FILE}. Each batch is one fresh unit "
        f"({', '.join(QUESTION_UNIT.format(number=batch) for batch in batches)}), never the unit that wrote the shots.")
    for question in questions:
        if question.batch != batches[0]:
            say(f"The other batches are in {MACHINE_FOLDER}/{QUESTIONS_TEXT_FILE}.")
            break
        say(f"{question.number}. {question.text}")
    context.summary = f"{len(questions)} questions in {len(batches)} batches"
    return 0


# ---------------------------------------------------------------- stage.py

def register_commands(table):
    """stage.py's command table: adopt, impact and questions."""
    table.add("adopt", "Make a folder saved by hand in a chat app checkable, then check it", run_adopt,
              add_adopt_arguments, uses_project=False)
    table.add("impact", "What depends on a record: the records and units that go stale", run_impact,
              add_impact_arguments)
    table.add("questions", "Yes/no review questions from the records, in batches for fresh units", run_questions,
              add_questions_arguments)
