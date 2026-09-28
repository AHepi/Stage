"""fill_code_fields.py: fills, after every apply and on every build, the fields code keeps that no other command
fills (fix list C4, C5 and C8), and lists which code path fills every other field code keeps.

In plain words:
- PROJECT genre, tone_home and tone_range are copied from the story plan (PLAN) once it is written;
- a CHOICE that is answered or defaulted gets its date (an open choice needs none);
- STYLE provisional is yes until the style test sets the style picture, and STYLE named_reference_policy takes
  the one value the rules allow (describe_qualities_only);
- SOUNDPLAN clip_audio takes its fixed text: no clip carries music, whatever the music policy says, because music
  goes in at the edit;
- LOCATION headings (screenplays) are the scene headings of the scenes that use the place: the scenes whose
  location names it, else the scenes whose place words match the place best;
- TEXT words of a text written in the story (origin story) are copied from the story lines its words_from cites
  (the quoted words when a quote is given, else the whole line);
- an answer to a choice whose record did not exist yet (the music answer at step 3 sets the sound plan made at
  step 6) is kept waiting and written when the record is made, with a line in the log (C5);
- once the story plan is written, the first estimate (made from the words) fills each scene's
  target_duration_s and the plan's runtime_estimate, scene_budget and shot_budget (C8).

CODE_FILLED_FIELDS names, for every stored field whose writer is code (code_state, or story for some source),
the module and function that fill it; tests/fix_code_fields_acceptance.py walks schema.json against it, so a
field that FORM-05 can ask for and no code fills is caught before a user meets it.

Nothing here changes a value on a locked record; a locked record only gains a field it lacks. Old copies of every
file changed are kept in history/ (7.3). Standard library only.
"""

import re
from dataclasses import dataclass, field as dataclass_field
from pathlib import Path

from .record_format import merge_copies, normalise_word, parse_line_numbers, parse_quote_anchor, split_item, write_file

# Every stored field that code writes (code_state or story, or one of them under a condition), and what fills it:
# "TYPE.field": (module, function, how, in plain words). Fields that only an add-on fills name that add-on's code.
CODE_FILLED_FIELDS = {
    "PROJECT.title": ("read_story", "read_into_project", "the story's title line (stage.py new writes a first one)"),
    "PROJECT.source_file": ("project_files", "run_new", "the story file kept in Original/"),
    "PROJECT.source_fingerprint": ("project_files", "run_new", "the story file's fingerprint"),
    "PROJECT.source_kind": ("read_story", "read_into_project", "read from the story"),
    "PROJECT.source_format": ("read_story", "read_into_project", "read from the story"),
    "PROJECT.language": ("read_story", "read_into_project", "read from the story"),
    "PROJECT.surface": ("read_story", "score_selftest", "the app the self-test ran in (new writes a first guess)"),
    "PROJECT.code_execution": ("read_story", "score_selftest", "yes on every app that runs the tools"),
    "PROJECT.batch_size": ("read_story", "score_selftest", "from the self-test's score"),
    "PROJECT.genre": ("fill_code_fields", "plan_copies", "copied from the story plan"),
    "PROJECT.tone_home": ("fill_code_fields", "plan_copies", "copied from the story plan"),
    "PROJECT.tone_range": ("fill_code_fields", "plan_copies", "copied from the story plan"),
    "PROJECT.scene_id_digits": ("read_story", "read_into_project", "from the story's scene count"),
    "PROJECT.previs_colours": ("make_previs_plans", "run_previs", "add-on B: the grey preview colours"),
    "PROJECT.schema_version": ("project_files", "run_new", "the version of the tools' schema"),
    "PROJECT.checker_last_run": ("check_records", "set_checker_last_run", "the day check --all last ran"),
    "PROJECT.model_facts_date": ("estimate", "store_estimate_fields", "the date of the model facts the estimate used"),
    "CHOICE.status": ("project_files", "apply_choice_answers", "open, then answered or defaulted"),
    "CHOICE.date": ("fill_code_fields", "choice_dates", "the day a choice was answered or defaulted"),
    "SCENE.heading": ("read_story", "read_into_project", "copied from the story's scene heading"),
    "SCENE.int_ext": ("read_story", "read_into_project", "copied from the story's scene heading"),
    "SCENE.place_text": ("read_story", "read_into_project", "copied from the story's scene heading"),
    "SCENE.time_text": ("read_story", "read_into_project", "copied from the story's scene heading"),
    "SCENE.lines": ("read_story", "read_into_project", "the scene's lines, from its heading to the next"),
    "SCENE.characters": ("read_story", "read_into_project", "the people the scene's lines name"),
    "SCENE.speaking": ("read_story", "read_into_project", "counted from the scene's cues"),
    "SCENE.transition_in": ("read_story", "read_into_project", "from the story's joins"),
    "SCENE.transition_out": ("read_story", "read_into_project", "from the story's joins"),
    "SCENE.target_duration_s": ("fill_code_fields", "first_estimate_fields", "the first estimate, from the words"),
    "SPEECH.speaker": ("read_story", "speeches_json", "screenplays: speeches.json, read from the cues"),
    "SPEECH.line": ("read_story", "speeches_json", "screenplays: speeches.json, read from the cues"),
    "SPEECH.text": ("read_story", "speeches_json", "screenplays: speeches.json, read from the cues"),
    "SPEECH.parenthetical": ("read_story", "speeches_json", "screenplays: speeches.json, read from the cues"),
    "SPEECH.extension": ("read_story", "speeches_json", "screenplays: speeches.json, read from the cues"),
    "SPEECH.path": ("read_story", "speeches_json", "screenplays: speeches.json, read from the cues"),
    "SPEECH.origin": ("read_story", "speeches_json", "screenplays: speeches.json, read from the cues"),
    "SHOTLIST.approved": ("make_handout", "pass_checkpoint", "yes when the user passes the group of shots"),
    "PLAN.runtime_estimate": ("fill_code_fields", "first_estimate_fields", "the first estimate, from the words"),
    "PLAN.scene_budget": ("fill_code_fields", "first_estimate_fields", "the first estimate, from the words"),
    "PLAN.shot_budget": ("fill_code_fields", "first_estimate_fields", "the first estimate, from the words"),
    "CHAPTER.title": ("read_story", "read_into_project", "from the chapter heading"),
    "CHAPTER.lines": ("read_story", "read_into_project", "from the chapter headings"),
    "CHAPTER.words": ("read_story", "read_into_project", "counted from the chapter"),
    "STYLE.named_reference_policy": ("fill_code_fields", "style_fields", "the one value the rules allow"),
    "STYLE.provisional": ("fill_code_fields", "style_fields", "yes until the style test sets the style picture"),
    "CHARACTER.names": ("read_story", "read_into_project", "the story's cue names"),
    "LOCATION.headings": ("fill_code_fields", "location_headings", "the headings of the scenes that use the place"),
    "TEXT.words": ("fill_code_fields", "text_words", "copied from the story lines its words_from cites"),
    "SOUNDPLAN.clip_audio": ("fill_code_fields", "sound_plan_fields", "the fixed text: no music in any clip"),
    "FINDING.record": ("film_pass", "write_whole_film_check", "the checker's findings of the film pass"),
    "FINDING.rule": ("film_pass", "write_whole_film_check", "the checker's findings of the film pass"),
    "FINDING.evidence": ("film_pass", "write_whole_film_check", "the checker's findings of the film pass"),
    "FINDING.fix": ("film_pass", "write_whole_film_check", "the checker's findings of the film pass"),
    "FINDING.source": ("film_pass", "write_whole_film_check", "the checker's findings of the film pass"),
    "PREVIS.for": ("derive_fields", "create_previs_stubs", "the grey preview job code makes at step 8"),
    "PREVIS.level": ("derive_fields", "create_previs_stubs", "the grey preview job code makes at step 8"),
    "PREVIS.approved": ("make_previs_plans", "run_previs", "add-on B: auto, or the user's answer"),
    "FINISH.shot": ("make_exports", "run_export", "add-on D: the finishing job list"),
    "FINISH.operation": ("make_exports", "run_export", "add-on D: the finishing job list"),
    "status": ("project_files", "apply_inbox", "draft (open for a choice) when a record is first saved"),
    "locked": ("project_files", "apply_choice_answers", "yes when an answer or an approval locks the record"),
}

# How FORM-05 says who fills a code field that is still missing (used in its fix text).
FILL_COMMAND_WORDS = "code fills it after the next apply, or run stage.py build"

WORD_STOP_LIST = {"the", "a", "an", "of", "and", "in", "at", "on", "to", "int", "ext", "s"}
FIXED_NAMED_REFERENCE_POLICY = "describe_qualities_only"


@dataclass
class FillResult:
    """What one fill did: (record label, field, value, how) for each value written, the files changed, notes, and
    (record type's plain name, field's plain label, record's plain name) for the log the user reads."""
    written: list = dataclass_field(default_factory=list)
    files: list = dataclass_field(default_factory=list)
    notes: list = dataclass_field(default_factory=list)
    plain: list = dataclass_field(default_factory=list)

    def plain_summary(self):
        """One plain sentence for the numbered log (no IDs, no field names): 'Code filled what it keeps: the headings
        of 22 places; the words of 9 texts in pictures.'"""
        if not self.plain:
            return ""
        grouped = {}
        for type_words, label, record_words in self.plain:
            grouped.setdefault((label, type_words), []).append(record_words)
        parts = []
        for (label, type_words), names in grouped.items():
            if len(names) == 1:
                parts.append(f"the {label} of {names[0]}")
            else:
                parts.append(f"the {label} of {len(names)} {type_words}s")
        return "Code filled what it keeps: " + "; ".join(parts) + "."

    def summary(self):
        if not self.written:
            return ""
        by_field = {}
        for label, name, _, how in self.written:
            by_field.setdefault(name, []).append(label)
        parts = []
        for name, labels in by_field.items():
            shown = ", ".join(labels[:4]) + (f" and {len(labels) - 4} more" if len(labels) > 4 else "")
            parts.append(f"{name} on {shown}")
        return "Code filled " + "; ".join(parts) + "."


def place_words(text):
    """The words that name a place ("QUARANTINE - IONA'S ROOM" gives quarantine, iona, room), without little words."""
    words = set()
    lowered = (text or "").lower().replace("\u2019", "'").replace("'s", "")
    for word in re.findall(r"[a-z0-9]+", lowered):
        if word not in WORD_STOP_LIST:
            words.add(word)
    return words


def location_words(location):
    identifier = location.identifier or ""
    identifier = identifier[4:] if identifier.startswith("LOC-") else identifier
    return place_words(location.title) | place_words(identifier.replace("-", " "))


def best_location_for(place_text, locations):
    """The place whose name (title and ID) shares the most words with a scene's place words, the one with fewest
    other words on a tie; None when no place shares a word."""
    wanted = place_words(place_text)
    best = None
    best_score = (0, 0)
    for location in locations:
        if not location.identifier:
            continue
        words = location_words(location)
        shared = len(wanted & words)
        if not shared:
            continue
        score = (shared, -len(words - wanted))
        if score > best_score:
            best, best_score = location, score
    return best


def is_locked(record):
    return normalise_word(record.get("locked") or "") == "yes"


def is_empty_value(value):
    return value is None or normalise_word(str(value)) in ("", "open")


class Filler:
    """Works out and writes the code fields of one project's record files."""

    def __init__(self, record_files, schema, words=None, constants=None, story=None):
        self.record_files = record_files
        self.schema = schema
        self.words = words or {}
        self.constants = constants or {}
        self.story = story
        self.index, _ = merge_copies(record_files, schema)
        self.result = FillResult()
        self.changed_files = {}

    # -------------------------------------------------- finding and writing

    def records(self, type_name):
        return [record for (kind, _), record in self.index.items() if kind == type_name
                and normalise_word(record.get("status") or "") != "omitted"]

    def singleton(self, type_name):
        return self.index.get((type_name, None)) or next(iter(self.records(type_name)), None)

    def copies_of(self, record):
        """Every file copy of a record: (record file, record), the copy that already holds a field first."""
        found = []
        for record_file in self.record_files:
            for copy in record_file.records:
                if copy.key == record.key:
                    found.append((record_file, copy))
        return found

    def target_copy(self, record, name):
        copies = self.copies_of(record)
        if not copies:
            return None, None
        holding = [pair for pair in copies if pair[1].field_lines(name)]
        if holding:
            return holding[0]
        if record.type_name == "SCENE":
            listed = [pair for pair in copies if pair[0].name.startswith("04 ")]
            if listed:
                return listed[0]
        return copies[0]

    def write(self, record, name, value, how, repeat=False):
        """Set one field on the stored copy; a locked record only gains a field it lacks. Returns True if written."""
        values = value if isinstance(value, list) else [value]
        values = [str(item) for item in values]
        current = record.get_all(name)
        if [normalise_word(item) for item in current] == [normalise_word(item) for item in values]:
            return False
        if is_locked(record) and current and not all(is_empty_value(item) for item in current):
            return False
        record_file, copy = self.target_copy(record, name)
        if copy is None:
            return False
        if repeat:
            copy.set_items(name, values, self.schema)
        else:
            copy.set_field(name, values[0], self.schema)
        if copy is not record:
            if repeat:
                record.set_items(name, values, self.schema)
            else:
                record.set_field(name, values[0], self.schema)
        self.changed_files[record_file.name] = record_file
        shown = "; ".join(values)
        self.result.written.append((record.label, name, shown, how))
        definition = self.schema.field(record.type_name, name) or {}
        type_words = (self.schema.record_types.get(record.type_name) or {}).get("plain_name") or "record"
        type_words = re.sub(r"^the\s+", "", re.sub(r"\s*\(.*\)$", "", type_words))
        record_words = (f"the {type_words}" if not record.identifier or record.type_name == "PROJECT"
                        else (record.title or f"a {type_words}"))
        self.result.plain.append((type_words, (definition.get("label") or name.replace("_", " ")).lower(),
                                  record_words))
        return True

    # -------------------------------------------------- the fields

    def plan_copies(self):
        """PROJECT genre, tone_home and tone_range, copied from PLAN (tone_range falls back to the home tone at quick
        depth, where the plan has no range)."""
        project = self.singleton("PROJECT")
        plan = self.singleton("PLAN")
        if project is None or plan is None:
            return
        for name in ("genre", "tone_home", "tone_range"):
            value = plan.get(name)
            if is_empty_value(value) and name == "tone_range":
                value = plan.get("tone_home")
            if not is_empty_value(value):
                self.write(project, name, value, "copied from the story plan")

    def choice_dates(self, today_text):
        """An answered or defaulted choice without a date gets today's (an open choice needs none)."""
        for choice in self.records("CHOICE"):
            status = normalise_word(choice.get("status") or "open")
            if status in ("answered", "defaulted") and normalise_word(choice.get("date") or "none") in ("none", ""):
                self.write(choice, "date", today_text, "the day the choice was settled")

    def style_fields(self):
        style = self.singleton("STYLE")
        if style is None:
            return
        picture = style.get("style_picture")
        provisional = "no" if picture and normalise_word(picture) not in ("none", "open") else "yes"
        if not (is_locked(style) and style.get("provisional")):
            self.write(style, "provisional", provisional,
                       "yes until the style test chooses a style picture" if provisional == "yes"
                       else "the style test chose the style picture")
        self.write(style, "named_reference_policy", self.fixed_value("STYLE", "named_reference_policy"),
                   "the one value the rules allow")

    def fixed_value(self, type_name, name):
        definition = self.schema.field(type_name, name) or {}
        if definition.get("fixed_value"):
            return definition["fixed_value"]
        values = definition.get("values") or []
        return values[0] if len(values) == 1 else FIXED_NAMED_REFERENCE_POLICY

    def sound_plan_fields(self):
        plan = self.singleton("SOUNDPLAN")
        if plan is None:
            return
        definition = self.schema.field("SOUNDPLAN", "clip_audio") or {}
        fixed = definition.get("fixed_value") or "No music in any clip."
        self.write(plan, "clip_audio", fixed, "fixed: music goes in at the edit, never inside a clip")

    # -- LOCATION headings (screenplays)
    def best_location(self, scene, locations):
        return best_location_for(scene.get("place_text") or scene.get("heading") or "", locations)

    def location_headings(self):
        project = self.singleton("PROJECT")
        if project is None or normalise_word(project.get("source_kind") or "") != "screenplay":
            return
        locations = [location for location in self.records("LOCATION") if location.identifier]
        if not locations:
            return
        scenes = sorted(self.records("SCENE"), key=lambda record: record.identifier or "")
        chosen = {location.identifier: [] for location in locations}
        for scene in scenes:
            heading = scene.get("heading")
            if not heading:
                continue
            named = scene.get("location")
            target = self.index.get(("LOCATION", named)) if named else None
            if target is None:
                target = self.best_location(scene, locations)
            if target is not None and target.identifier in chosen:
                if heading not in chosen[target.identifier]:
                    chosen[target.identifier].append(heading)
        for location in locations:
            headings = chosen.get(location.identifier) or []
            value = "; ".join(headings) if headings else "none"
            self.write(location, "headings", value,
                       "the headings of the scenes that use the place" if headings
                       else "no scene heading names this place")

    # -- TEXT words (origin story)
    def text_words(self):
        for text in self.records("TEXT"):
            if normalise_word(text.get("origin") or "") != "story":
                continue
            sources = text.get_all("words_from")
            if not sources:
                continue
            pieces = []
            for source in sources:
                piece = self.words_of_source(source)
                if piece is None:
                    pieces = None
                    break
                pieces.append(piece)
            if pieces:
                self.write(text, "words", " ".join(pieces), "copied from the story lines words_from cites")

    def words_of_source(self, source):
        """The exact words one words_from item names: its quote (checked by CITE-03), else its whole line."""
        definition = self.schema.field("TEXT", "words_from")
        item = split_item(source, definition)
        quote = item.get("quote")
        if quote:
            quote = quote.strip()
            if len(quote) >= 2 and quote[0] in "\"“" and quote[-1] in "\"”":
                quote = quote[1:-1]
            return quote.strip() or None
        if self.story is None:
            return None
        first = (item.first or "").strip()
        numbers = parse_line_numbers(first)
        texts = []
        if numbers:
            for start, end in numbers:
                for number in range(start, end + 1):
                    texts.append(self.story.line(number).strip())
        elif parse_quote_anchor(first):
            texts = [part for part in parse_quote_anchor(first)]
        texts = [re.sub(r"^=\s*", "", line).strip() for line in texts if line and line.strip()]
        return " ".join(texts) or None

    # -- answers waiting for their record (C5)
    def waiting_answers(self):
        """Answered or defaulted choices whose chosen sets line (or set value) names a record that exists now but
        does not hold the answer yet: write it (only where the field is missing or open)."""
        from .checks_form import ChoiceBook
        book = ChoiceBook(list(self.index.values()))
        for choice in self.records("CHOICE"):
            letter = book.chosen_letter(choice)
            if letter is None:
                continue
            number = int(choice.identifier.split("-")[1]) if choice.identifier and "-" in choice.identifier else 0
            for item_text in choice.get_all("sets"):
                item = split_item(item_text)
                first = item.first.strip()
                if (item.get("when") or "").lower() not in ("", letter):
                    continue
                if first in book.set_values:
                    if not first.upper().endswith("-" + letter.upper()):
                        continue
                    set_value = book.set_values[first]
                    target = self.find_target(set_value.get("target") or "")
                    if target is None:
                        continue
                    for name in set_value.field_names():
                        if name in ("target", "status", "locked"):
                            continue
                        if all(is_empty_value(value) for value in target.get_all(name)):
                            definition = self.schema.field(target.type_name, name) or {}
                            self.write(target, name, set_value.get_all(name),
                                       f"the answer to choice {number}, kept until this record was made",
                                       repeat=bool(definition.get("repeat")))
                    continue
                match = re.match(r"^(.+)\.([a-z][a-z0-9_]*)$", first)
                if not match or item.get("value") is None:
                    continue
                target = self.find_target(match.group(1))
                if target is None:
                    continue
                if all(is_empty_value(value) for value in target.get_all(match.group(2))):
                    self.write(target, match.group(2), item.get("value"),
                               f"the answer to choice {number}, kept until this record was made")

    def find_target(self, reference):
        reference = reference.strip()
        for (kind, identifier), record in self.index.items():
            if identifier == reference:
                return record
        if reference == "PROJECT" or self.schema.is_singleton(reference):
            return self.singleton(reference)
        return None


def load_filler(project, story=None):
    """A Filler over a project's record files (and its numbered story, when it has been read)."""
    from .record_format import load_skill_data
    schema, words, constants = project.schema, project.words, None
    try:
        _, _, constants = load_skill_data()
    except (OSError, ValueError):
        constants = {}
    if story is None:
        try:
            from .read_story import NumberedStory
            story = NumberedStory.from_project(project.folder)
        except Exception:  # no story read yet: the TEXT words wait
            story = None
    return Filler(project.load_record_files(), schema, words, constants, story)


def fill_code_fields(project, today_text=None, log=True):
    """Fill every code field this module owns in a project, then the first estimate's fields when the story plan
    exists and they are missing. Writes the changed files (old copies in history/) and one log entry. Returns a
    FillResult."""
    from .project_files import history_run_folder, keep_in_history, today
    filler = load_filler(project)
    today_text = today_text or today()
    filler.waiting_answers()
    filler.plan_copies()
    filler.choice_dates(today_text)
    filler.style_fields()
    filler.sound_plan_fields()
    filler.location_headings()
    filler.text_words()
    result = filler.result
    if filler.changed_files:
        history = history_run_folder(project)
        for name, record_file in sorted(filler.changed_files.items()):
            path = project.folder / name
            if path.is_file():
                keep_in_history(history, path, name)
            write_file(record_file, path, project.schema)
            result.files.append(name)
    estimate_note = first_estimate_fields(project)
    if estimate_note:
        result.notes.append(estimate_note)
    waited = [(entry, plain) for entry, plain in zip(result.written, result.plain)
              if "kept until this record was made" in entry[3]]
    for (label, name, value, how), _ in waited:
        result.notes.append(f"Wrote {how.split(',')[0]} into {label}: {name} {value}.")
    if log and result.written:
        try:
            text = result.plain_summary()
            if waited:
                text += " " + " ".join(f"The {how.split(',')[0]} was kept until {plain[2]} was made, and is now "
                                       f"written there ({plain[1]}: {value})."
                                       for (label, name, value, how), plain in waited)
            project.add_log_entry(text)
        except (OSError, ValueError):
            pass
    return result


def first_estimate_fields(project):
    """C8: once the story plan exists, the first estimate (from the words) fills every scene's target_duration_s and
    the plan's runtime_estimate, scene_budget and shot_budget, when any of them is missing. Returns a plain note, or
    "" when nothing was needed."""
    record_files = project.load_record_files()
    index, _ = merge_copies(record_files, project.schema)
    plan = index.get(("PLAN", None))
    if plan is None:
        return ""
    scenes = [record for (kind, _), record in index.items() if kind == "SCENE"
              and normalise_word(record.get("status") or "") != "omitted"]
    missing_scene = [scene for scene in scenes if is_empty_value(scene.get("target_duration_s"))]
    missing_plan = [name for name in ("runtime_estimate", "scene_budget", "shot_budget")
                    if is_empty_value(plan.get(name))]
    if not missing_scene and not missing_plan:
        return ""
    try:
        from .estimate import (PriceTable, fields_to_store, film_estimate, load_breakdown, note_in_manifest,
                               nothing_to_estimate, write_estimate_files)
        breakdown = load_breakdown(project.folder)
        prices, _ = PriceTable.load()
        film = film_estimate(breakdown, "v0", prices=prices)
        if nothing_to_estimate(film):
            return ""
        write_estimate_files(project.folder, film, prices)
        changed, changed_files = store_missing_figures(project, fields_to_store(film, breakdown))
        note_in_manifest(project.folder, film, breakdown.schema, breakdown.words)
    except Exception as error:  # the estimate must never undo a saved unit; stage.py estimate tries again
        return f"The first estimate could not fill the scene targets ({type(error).__name__}: {error}); run stage.py estimate."
    if not changed:
        return ""
    try:
        project.add_log_entry(f"Made the first estimate from the words and stored {changed} planned figures "
                              f"(each scene's target length and the plan's budgets) in {', '.join(changed_files)}.")
    except (OSError, ValueError):
        pass
    return (f"The first estimate filled {changed} planned figures (each scene's target length and the plan's "
            "budgets); scene totals are compared with them as a warning only (TIME-03).")


def store_missing_figures(project, wanted):
    """Write the first estimate's figures [(type, ID or None, field, value)] only where the field is missing, so a
    target the plan or the user set later is never replaced. Returns (values written, file names)."""
    from .project_files import history_run_folder, keep_in_history
    record_files = project.load_record_files()
    changed = 0
    changed_files = {}
    for type_name, identifier, name, value in wanted:
        if name == "model_facts_date":
            continue
        ordered = sorted(record_files, key=lambda item: (0 if item.name.startswith("04 ") and type_name == "SCENE"
                                                         else 1, item.name))
        target = next(((record_file, record) for record_file in ordered for record in record_file.records
                       if record.type_name == type_name and (identifier is None or record.identifier == identifier)),
                      None)
        if target is None:
            continue
        record_file, record = target
        if not is_empty_value(record.get(name)):
            continue
        record.set_field(name, value, project.schema)
        changed += 1
        changed_files[record_file.name] = record_file
    if changed_files:
        history = history_run_folder(project)
        for name, record_file in changed_files.items():
            path = project.folder / name
            if path.is_file():
                keep_in_history(history, path, name)
            write_file(record_file, path, project.schema)
    return changed, sorted(changed_files)


def code_fill_path(type_name, field_name):
    """(module, function, how) that fills a code field, or None."""
    return CODE_FILLED_FIELDS.get(f"{type_name}.{field_name}") or CODE_FILLED_FIELDS.get(field_name)
