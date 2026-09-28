"""checks_ids_citations.py: the ID and CITE checks of blueprint section 7.2 (ID-01 to ID-09, CITE-01 to CITE-07).

In plain words:
- the ID checks make sure every record has one ID of the right width, issued in the right block, never used
  twice and never brought back after it was cut; that every ID a record names exists; that the scene count
  matches the story; and that the shots and the shot list agree;
- the CITE checks make sure every line number points inside its scene (or the story), every quote anchor and
  story point holds at least 3 words found exactly once in its scope (5.1 G5, WP12a's adopt rule), every quoted
  string is the story's own words (G12), and every speech a shot hears matches the story.

Each check is one function registered with check_records.register_check; each takes a CheckRun and returns
problem lines (record_format.Problem). Three guards also run on an inbox before apply merges it (registered with
project_files.register_apply_check): ID-01 (one ID used twice), ID-04 (an omitted ID used again) and ID-06 (an
ID outside the unit's pre-issued block).

Scope of a quote (G5 and WP12a's adopt rule): the scene's lines for the records of a scene file, for story
points and for a STATE's starting line; the chapter's lines for CHAPTER first_line, last_line and candidate
scenes; the whole story otherwise. With only an excerpt of the story (the scene 10 fixture), a quote or a line
outside the excerpt is skipped as "not in the excerpt", never reported as a problem.

Pre-issued blocks (ID-06), written by make_handout.py into manifest.json:
    manifest["issued"]["U-07-SC10"] = {"BEAT": ["SC10-B01", "SC10-B30"], "SHOT": ["SC10-SH010", "SC10-SH400"]}
Each value is one [first, last] pair or a list of pairs. An ID is inside when it has the same letters before
its last number and that number lies between the pair's numbers (so an insert such as SH155 is inside). The
types are record types, plus VALUE for the values a SCENE declares.

Standard library only.
"""

import re
from pathlib import Path

from .check_records import register_check, same_scene, scene_of
from .checks_form import resolve_field, setvalue_target_type
from .project_files import register_apply_check
from .record_format import (FIELD_PATH, Problem, normalise_word, parse_line_numbers, parse_quote_anchor,
                            parse_story_point, quote_for_message, split_item, split_list, split_outside_quotes)

ID_KINDS = ("id", "id_list", "id_range", "because_list", "reference_list", "story_point", "story_point_list",
            "scene_or_story_point")
STORY_POINT_KINDS = ("story_point", "story_point_list", "scene_or_story_point")
ANCHOR_KINDS = ("lines",) + STORY_POINT_KINDS
EMPTY_WORDS = ("none", "open", "auto", "all", "default", "never", "as_written")
SCENE_FILE_TYPES = ("SCENE", "PART", "BEAT", "SPEECH", "MOVE", "SETUP", "SHOTLIST", "SHOT", "CUT")
NOT_STORY_TEXT_TYPES = ("FINDING", "REVIEW", "PIC", "PREVIS", "TAKE", "VOICETAKE", "FINISH", "MUSIC", "RIGHTS",
                        "PROJECT")
QUOTED = re.compile(r'["“]([^"“”]+)["”]')
SCENE_BEFORE_QUOTE = re.compile(r"\b(SC\d{2,3}[A-Z]?)\s+$")
SCENE_ID = re.compile(r"^SC(\d+)([A-Z]?)$")
CLIP_ID = re.compile(r"^(SC\d{2,3}[A-Z]?-SH\d{3})\.\d$")
NUMBER_AT_END = re.compile(r"^(.*?)(\d+)$")
WORD = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*")
DOUBLE_QUOTED_SPEECH = re.compile(r'["“]([^"“”]*)["”]')
LEFT_OUT_LISTED = 8


# ---------------------------------------------------------------- shared helpers

def text_of(record):
    return record.label


def effective_type(run, record):
    """The record type whose fields a record holds: a SETVALUE holds its target's fields."""
    if record.type_name == "SETVALUE":
        return setvalue_target_type(run.schema, record) or "SETVALUE"
    return record.type_name


def sub_part_definition(definition, key):
    for entry in definition.get("sub_parts") or []:
        if entry.get("key") == key:
            return entry
    return None


def field_values(run):
    """Every field line of every record copy, with its definition: (record_file, record, line, definition, name).

    Cached per run. Unknown fields (FORM-03) and missing values (G7) are left out."""
    key = "ids_citations_field_values"
    if key in run.cache:
        return run.cache[key]
    found = []
    for record_file in run.record_files:
        for record in record_file.records:
            if not record.known_type:
                continue
            for line in record.fields:
                if line.missing:
                    continue
                definition, name, _ = resolve_field(run.schema, run.words, record, line.name)
                if definition is None:
                    continue
                found.append((record_file, record, line, definition, name))
    run.cache[key] = found
    return found


def is_empty_word(value):
    return normalise_word(value) in EMPTY_WORDS


def plain_range(first, last):
    return f"{first}" if first == last else f"{first}-{last}"


def scene_words(scene_identifier):
    match = SCENE_ID.match(scene_identifier or "")
    return f"scene {int(match.group(1))}{match.group(2)}" if match else str(scene_identifier)


def left_out_skip(run, check_id, scenes):
    """One skip line naming the scenes a check could not see (no records here; outside the scope or excerpt)."""
    if not scenes:
        return
    ordered = sorted(scenes, key=lambda identifier: (len(identifier), identifier))
    shown = ", ".join(ordered[:LEFT_OUT_LISTED]) + (f" and {len(ordered) - LEFT_OUT_LISTED} more"
                                                    if len(ordered) > LEFT_OUT_LISTED else "")
    run.skip(check_id, f"references into {shown}: not in the excerpt (no records of those scenes here, and they "
                       "are outside the project's scope or the story given), so they were not checked")


# ---------------------------------------------------------------- IDs: what exists

def declared_identifiers(run):
    """{ID: (TYPE, declaring record)} for IDs declared by items (defines_id): SCENE values and shot-list items."""
    key = "ids_declared"
    if key in run.cache:
        return run.cache[key]
    declared = {}
    for record_type, field_name, declared_type in (("SCENE", "value", "VALUE"), ("SHOTLIST", "item", "SHOT")):
        definition = run.schema.field(record_type, field_name) or {}
        for record in run.records(record_type, include_omitted=True):
            for value in record.get_all(field_name):
                first = (split_item(value, definition).first or "").strip()
                if first and first not in declared:
                    declared[first] = (declared_type, record)
    run.cache[key] = declared
    return declared


def identifier_exists(run, identifier):
    """(exists, record or None): an ID exists as a record, a declared item, a speech, a clip or a singleton (5.4 rule 2)."""
    record = run.record(identifier)
    if record is not None:
        return True, record
    if identifier in declared_identifiers(run):
        return True, None
    if identifier in run.speeches:
        return True, None
    clip = CLIP_ID.match(identifier)
    if clip:
        shot = run.record(clip.group(1))
        return shot is not None, shot
    return False, None


def looks_like_identifier(run, text):
    if not text or " " in text:
        return False
    if run.schema.types_for_id(text):
        return True
    return text in run.schema.singleton_types or text == "PROJECT"


def setvalue_needed(run, choice, item):
    """A SETVALUE a choice's sets line names must exist only once that option is chosen: the AI writes it with the
    answer (WP3's length choice writes SETVALUE CHOICE-005-B only when the user gives a target)."""
    from .checks_form import ChoiceBook
    merged = run.index.get(choice.key, choice)
    book = run.cache.get("ids_choice_book")
    if book is None:
        book = run.cache["ids_choice_book"] = ChoiceBook(list(run.index.values()))
    letter = book.chosen_letter(merged)
    return letter is not None and (item.get("when") or "").strip().lower() == letter


def identifier_pieces(value, kind):
    """The IDs a value names, each with how it names it: ('id'), ('scene' of a story point), ('beat' after =)."""
    pieces = []
    text = value.strip()
    if kind == "id":
        return [(text, "id")]
    if kind in ("id_list", "id_range"):
        for piece in split_list(text):
            if ".." in piece:
                pieces.extend((end.strip(), "range end") for end in piece.split("..") if end.strip())
            else:
                pieces.append((piece, "id"))
        return pieces
    if kind == "because_list":
        return [(piece, "id") for piece in split_list(text)
                if not piece.lower().startswith("line:") and piece.lower() != "default"]
    if kind == "reference_list":
        for piece in split_list(text):
            match = FIELD_PATH.match(piece)
            pieces.append((match.group(1), "field path") if match and not piece[-1].isdigit() else (piece, "id"))
        return pieces
    if kind in STORY_POINT_KINDS:
        for piece in split_list(text):
            point = parse_story_point(piece)
            if point:
                pieces.append((point[0], "story point scene"))
                if point[2]:
                    pieces.append((point[2], "resolved beat"))
            else:
                pieces.append((piece, "id"))
        return pieces
    return pieces


def references(run):
    """Every ID a record names: (record_file, record, field name, line number, ID, how). Cached per run.

    Declarations (the first part of a defines_id field) are not references."""
    key = "ids_references"
    if key in run.cache:
        return run.cache[key]
    found = []
    for record_file, record, line, definition, name in field_values(run):
        value = line.value.strip()
        if is_empty_word(value):
            continue
        kind = definition.get("kind")
        pieces = []
        if kind in ID_KINDS:
            pieces = identifier_pieces(value, kind)
        elif kind == "sub_parts":
            item = split_item(value, definition)
            first_definition = definition.get("first_part")
            if first_definition and item.first and not definition.get("defines_id") and not is_empty_word(item.first):
                first_kind = first_definition.get("kind")
                if first_kind in ID_KINDS:
                    pieces.extend(identifier_pieces(item.first, first_kind))
                elif record.type_name == "CHOICE" and name == "sets":
                    target = item.first.strip()
                    match = FIELD_PATH.match(target)
                    if match:
                        pieces.append((match.group(1), "field path"))
                    elif setvalue_needed(run, record, item):
                        pieces.append((target, "id"))
            for sub_key, sub_value in item.parts:
                entry = sub_part_definition(definition, sub_key)
                if entry and entry.get("kind") in ID_KINDS and not is_empty_word(sub_value):
                    pieces.extend(identifier_pieces(sub_value, entry.get("kind")))
        for identifier, how in pieces:
            identifier = identifier.strip()
            if identifier and not is_empty_word(identifier):
                found.append((record_file, record, name, line.line_number, identifier, how))
    run.cache[key] = found
    return found


def scene_number_width(identifier):
    match = re.match(r"^SC(\d+)", identifier or "")
    return len(match.group(1)) if match else None


def project_digits(run):
    value = run.project_record.get("scene_id_digits") if run.project_record is not None else None
    if value and str(value).strip().isdigit():
        return int(value)
    if run.story is not None and run.story.story_map.get("scene_id_digits"):
        return int(run.story.story_map["scene_id_digits"])
    return None


def split_number(identifier):
    """('SC10-SH', 150) for SC10-SH150; None for an ID that does not end in a number (CH-IONA)."""
    match = NUMBER_AT_END.match(identifier or "")
    if not match or not match.group(1):
        return None
    return match.group(1), int(match.group(2))


# ---------------------------------------------------------------- ID-01 to ID-09

@register_check("ID-01", level="E", build=1, title="Duplicate ID, among record IDs and IDs declared in items",
                plain="uses a number or name that another record already has")
def check_id_01(run):
    problems = []
    types_by_identifier = {}
    for key in run.index:
        if key[1]:
            types_by_identifier.setdefault(key[1], []).append(key[0])
    for identifier, types in types_by_identifier.items():
        for type_name in types[1:]:
            problems.append(run.problem("E", "ID-01", (type_name, identifier), None,
                                        f"is also the ID of a {types[0]} record; one ID names one record",
                                        "Fix: give one of them another ID from its issued block"))
    for record_file in run.record_files:
        first_seen = {}
        for record in record_file.records:
            if not record.known_type:
                continue
            if record.key in first_seen:
                problems.append(run.problem("E", "ID-01", record, None,
                                            f"appears twice in this file (lines {first_seen[record.key]} and "
                                            f"{record.heading_line_number})",
                                            "Fix: keep one record and move any field it lacks into it (G10 merges "
                                            "copies only across files)", line_number=record.heading_line_number,
                                            file_name=record_file.name))
            else:
                first_seen[record.key] = record.heading_line_number
    for record_type, field_name, declared_type in (("SCENE", "value", "VALUE"), ("SHOTLIST", "item", "SHOT")):
        definition = run.schema.field(record_type, field_name) or {}
        for record in run.records(record_type, include_omitted=True):
            seen = {}
            for record_file, copy, line in run.field_lines(record.key, field_name):
                if line.missing:
                    continue
                first = (split_item(line.value, definition).first or "").strip()
                if not first:
                    continue
                comparison = re.sub(r"\s+", " ", line.value.strip())
                if first in seen and seen[first] != comparison:
                    problems.append(run.problem("E", "ID-01", copy, field_name,
                                                f"declares {first} twice with different content",
                                                "Fix: keep one item for each ID; give the other its own ID from the "
                                                "issued block", line_number=line.line_number, file_name=record_file.name))
                seen.setdefault(first, comparison)
                other = run.record(first)
                if other is not None and other.type_name != declared_type:
                    problems.append(run.problem("E", "ID-01", copy, field_name,
                                                f"declares {first}, which is already the ID of a {other.type_name} record",
                                                "Fix: use an ID from the issued block", line_number=line.line_number,
                                                file_name=record_file.name))
    return problems


@register_check("ID-02", level="E", build=1,
                title="Reference to an ID that does not exist, or to an omitted record",
                plain="points to something that does not exist or was cut")
def check_id_02(run):
    problems = []
    left_out = set()
    speeches_missing = False
    source_kind = run.project_record.get("source_kind") if run.project_record is not None else None
    for record_file, record, field_name, line_number, identifier, how in references(run):
        merged = run.index.get(record.key)
        if run.is_omitted(merged):
            continue
        if not looks_like_identifier(run, identifier):
            continue
        exists, target = identifier_exists(run, identifier)
        if exists:
            if target is not None and run.is_omitted(target) and target.key != record.key:
                problems.append(run.problem("E", "ID-02", record, field_name,
                                            f"names {identifier}, which was cut (status omitted); nothing may cite a "
                                            "cut record (5.4 rule 6)",
                                            "Fix: remove it, or name the record that replaced it",
                                            line_number=line_number, file_name=record_file.name))
            continue
        scene = scene_of(identifier)
        if scene is not None and run.scene_left_out(scene):
            left_out.add(scene)
            continue
        if re.fullmatch(r"SC\d{2,3}[A-Z]?-D\d{2,3}", identifier) and not run.speeches \
                and not run.records("SPEECH", include_omitted=True) and source_kind in (None, "screenplay"):
            speeches_missing = True
            continue
        what = f"names {identifier}, which does not exist"
        if how == "resolved beat":
            what = f"resolves its story point to {identifier}, which does not exist"
        elif how == "field path":
            what = f"names a field of {identifier}, which does not exist"
        problems.append(run.problem("E", "ID-02", record, field_name, what,
                                    "Fix: copy an ID that exists (reference/03 lists where each kind is issued), or "
                                    "write that record first", line_number=line_number, file_name=record_file.name))
    left_out_skip(run, "ID-02", left_out)
    if speeches_missing:
        run.skip("ID-02", "speech IDs: speeches.json is not present (run stage.py read, or give --story)")
    return problems


@register_check("ID-03", level="W", build=1,
                title="Shot numbers not in tens; an insert without a gap; cards and black below 990",
                plain="has a shot number out of the usual steps of ten")
def check_id_03(run):
    problems = []
    end_first = 990
    constants = (run.constants or {}).get("from_blueprint_text", {}).get("constants", {})
    if isinstance(constants.get("end_card_numbers"), dict):
        value = constants["end_card_numbers"].get("value")
        if isinstance(value, list) and value:
            end_first = int(value[0])
        elif isinstance(value, (int, float)):
            end_first = int(value)
    by_scene = {}
    for shot in run.records("SHOT"):
        by_scene.setdefault(scene_of(shot.identifier), {})[shot.identifier] = shot
    listed = {}
    for shot_list in run.records("SHOTLIST"):
        definition = run.schema.field("SHOTLIST", "item") or {}
        for value in shot_list.get_all("item"):
            first = (split_item(value, definition).first or "").strip()
            if re.fullmatch(r"SC\d{2,3}[A-Z]?-SH\d{3}", first):
                listed.setdefault(scene_of(first), {})[first] = shot_list
                by_scene.setdefault(scene_of(first), {})
    for scene, shots in by_scene.items():
        identifiers = set(shots) | set(listed.get(scene, {}))
        numbers = {identifier: int(identifier[-3:]) for identifier in identifiers}
        present = set(numbers.values())
        for identifier in sorted(identifiers):
            number = numbers[identifier]
            record = shots.get(identifier) or listed.get(scene, {}).get(identifier)
            field = None if identifier in shots else "item"
            kind = normalise_word(shots[identifier].get("kind") or "") if identifier in shots else ""
            if number == 0:
                problems.append(run.problem("W", "ID-03", record, field, f"{identifier} is numbered 000",
                                            "Fix: shots start at 010 and go in tens"))
                continue
            if number < end_first and number % 10:
                base = number - number % 10
                if base not in present:
                    problems.append(run.problem("W", "ID-03", record, field,
                                                f"{identifier} is not in tens and no shot {base:03d} comes before it, "
                                                "so it is not an insert between two shots",
                                                "Fix: use the next free number in tens from the issued block"))
            if kind in ("card", "black") and number < end_first:
                problems.append(run.problem("W", "ID-03", record, field,
                                            f"{identifier} is a {kind} shot numbered below {end_first}",
                                            f"Fix: number cards and black from {end_first} to 999"))
            if kind and kind not in ("card", "black") and number >= end_first:
                problems.append(run.problem("W", "ID-03", record, field,
                                            f"{identifier} is a {kind} shot numbered {end_first} or above; those "
                                            "numbers are for end cards and black",
                                            "Fix: give it a number in tens below 990"))
    return problems


@register_check("ID-04", level="E", build=1, title="An omitted ID reused",
                plain="brings back the number of something that was cut")
def check_id_04(run):
    problems = []
    for key in run.index:
        copies = run.copies(key)
        statuses = [(record_file, copy, normalise_word(copy.get("status") or "")) for record_file, copy in copies]
        if any(status == "omitted" for _, _, status in statuses):
            for record_file, copy, status in statuses:
                if status and status != "omitted":
                    problems.append(run.problem("E", "ID-04", copy, "status",
                                                f"is omitted in one file but {status} in {record_file.name}; a cut "
                                                "record keeps its ID and is never used again",
                                                "Fix: give the new record an ID of its own from the issued block",
                                                file_name=record_file.name))
    omitted_shots = {record.identifier for record in run.records("SHOT", include_omitted=True) if run.is_omitted(record)}
    omitted_values = set()
    definition = run.schema.field("SHOTLIST", "item") or {}
    for shot_list in run.records("SHOTLIST"):
        for record_file, copy, line in run.field_lines(shot_list.key, "item"):
            first = (split_item(line.value, definition).first or "").strip()
            if first in omitted_shots:
                problems.append(run.problem("E", "ID-04", copy, "item",
                                            f"lists {first}, which was cut (status omitted); its number is never "
                                            "used again", "Fix: take the item out of the list, or give a new shot "
                                            "the next free number", line_number=line.line_number,
                                            file_name=record_file.name))
    for identifier in (run.manifest.get("omitted_ids") or []):
        record = run.record(identifier)
        if record is not None and not run.is_omitted(record):
            problems.append(run.problem("E", "ID-04", record, None,
                                        f"was cut earlier (omitted), and its ID is used again",
                                        "Fix: give this record an ID of its own from the issued block"))
        elif record is None and identifier in declared_identifiers(run):
            declaring = declared_identifiers(run)[identifier][1]
            if declaring is not None and not run.is_omitted(declaring):
                omitted_values.add(identifier)
                problems.append(run.problem("E", "ID-04", declaring, None,
                                            f"declares {identifier}, which was cut earlier; its ID is never used again",
                                            "Fix: use the next free ID from the issued block"))
    return problems


@register_check("ID-05", level="E", build=1, title="Scene count differs from the story's headings (screenplay)",
                plain="has a different number of scenes from the story")
def check_id_05(run):
    kind = run.project_record.get("source_kind") if run.project_record is not None else None
    if kind is None and run.story is not None:
        kind = (run.story.story_map.get("source") or {}).get("kind")
    if normalise_word(kind or "") != "screenplay":
        return []
    if run.story_missing("ID-05"):
        return []
    story_scenes = list(run.story.numbered.scenes)
    records = [identifier for identifier in run.scene_ids() if re.fullmatch(r"SC\d{2,3}", identifier)]
    missing = [scene for scene in story_scenes if not any(same_scene(scene, record) for record in records)]
    extra = [record for record in records if not any(same_scene(scene, record) for scene in story_scenes)]
    if run.story.excerpt:
        extra = []
    if missing and run.scope_scenes is not None and records \
            and all(any(same_scene(record, scope) for scope in run.scope_scenes) for record in records) \
            and all(not any(same_scene(scene, scope) for scope in run.scope_scenes) for scene in missing):
        run.skip("ID-05", "the records hold only the scenes in the project's scope (a partial example), so the "
                          "count was not compared")
        return []
    if not missing and not extra:
        return []
    headings = len(story_scenes) if not run.story.excerpt else len(story_scenes)
    parts = []
    if missing:
        parts.append("no SCENE record for " + ", ".join(missing[:10]) + (" and more" if len(missing) > 10 else ""))
    if extra:
        parts.append("no heading in the story for " + ", ".join(extra[:10]) + (" and more" if len(extra) > 10 else ""))
    file_name = next((record_file.name for record_file in run.record_files
                      if any(record.type_name == "SCENE" for record in record_file.records)), "04 Scene list.md")
    return [Problem("E", "ID-05", quote_for_message(file_name), None,
                    f"holds {len(records)} scenes, but the story has {headings} scene headings: " + "; ".join(parts),
                    "Fix: run stage.py read again before the scene list is fixed, or mark a dropped scene omitted "
                    "(IDs never shift)", file_name=file_name)]


def issued_blocks(manifest, unit=None):
    """[(unit, TYPE, prefix, first number, last number)] from manifest["issued"] (see the note at the top)."""
    blocks = []
    issued = (manifest or {}).get("issued") or {}
    for unit_name, by_type in issued.items():
        if unit is not None and unit_name != unit:
            continue
        for type_name, pairs in (by_type or {}).items():
            if pairs and isinstance(pairs[0], str):
                pairs = [pairs]
            for pair in pairs or []:
                if not isinstance(pair, (list, tuple)) or len(pair) != 2:
                    continue
                first, last = split_number(str(pair[0])), split_number(str(pair[1]))
                if first and last and first[0] == last[0]:
                    blocks.append((unit_name, type_name, first[0], first[1], last[1]))
    return blocks


def outside_blocks(identifier, type_name, blocks):
    """The blocks of this type an ID should be inside (same scene), when it is inside none of them; else []."""
    parts = split_number(identifier)
    if parts is None:
        return []
    candidates = [block for block in blocks if block[1] == type_name
                  and (scene_of(block[2]) is None or same_scene(scene_of(block[2]), scene_of(identifier)))]
    if not candidates:
        return []
    if any(block[2] == parts[0] and block[3] <= parts[1] <= block[4] for block in candidates):
        return []
    return candidates


def block_words(blocks):
    shown = []
    for _, _, prefix, first, last in blocks[:3]:
        width = 3 if prefix.endswith("-SH") else 2 if re.search(r"-(B|M|SU|D)$", prefix) else 0
        shown.append(f"{prefix}{str(first).zfill(width)} to {prefix}{str(last).zfill(width)}")
    return "; ".join(shown)


@register_check("ID-06", level="E", build=1, title="ID outside the handout's pre-issued block",
                plain="uses a number outside the ones given for this step")
def check_id_06(run):
    blocks = issued_blocks(run.manifest)
    if not blocks:
        return []
    problems = []
    for key, record in run.index.items():
        if not key[1] or run.is_omitted(record):
            continue
        wanted = outside_blocks(key[1], key[0], blocks)
        if wanted:
            problems.append(run.problem("E", "ID-06", record, None,
                                        f"is outside the IDs issued for it ({block_words(wanted)})",
                                        "Fix: copy an ID from the issued block in the handout"))
    for identifier, (type_name, declaring) in declared_identifiers(run).items():
        wanted = outside_blocks(identifier, type_name, blocks)
        if wanted and declaring is not None and not run.is_omitted(declaring):
            problems.append(run.problem("E", "ID-06", declaring, None,
                                        f"declares {identifier}, outside the IDs issued for it ({block_words(wanted)})",
                                        "Fix: copy an ID from the issued block in the handout"))
    return problems


@register_check("ID-07", level="E", build=1,
                title="SHOT not in its scene's SHOTLIST; at Standard and Detailed, a list item without its SHOT",
                plain="has a shot missing from the shot list, or a listed shot not written yet")
def check_id_07(run):
    problems = []
    definition = run.schema.field("SHOTLIST", "item") or {}
    scenes = []
    for record in run.records("SHOT") + run.records("SHOTLIST"):
        scene = scene_of(record.identifier)
        if scene and scene not in scenes:
            scenes.append(scene)
    for scene in scenes:
        shot_list = run.record(f"{scene}-LIST")
        if shot_list is not None and run.is_omitted(shot_list):
            continue
        listed = []
        if shot_list is not None:
            listed = [(split_item(value, definition).first or "").strip() for value in shot_list.get_all("item")]
        for shot in run.records("SHOT"):
            if scene_of(shot.identifier) != scene or shot.identifier in listed:
                continue
            where = f"{scene}-LIST" if shot_list is not None else f"{scene}-LIST, which does not exist"
            problems.append(run.problem("E", "ID-07", shot, None, f"is not in its scene's shot list ({where})",
                                        "Fix: add its item to the shot list (the list fixes every shot's ID and "
                                        "count), or remove the shot"))
        if shot_list is None or (run.step is not None and run.step < 8):
            continue
        scene_record = run.record(scene)
        if run.depth_rank(scene_record if scene_record is not None else shot_list) < 2:
            continue
        written_so_far = run.batch_shots(scene)
        for identifier in listed:
            if not identifier or (written_so_far is not None and identifier not in written_so_far):
                continue
            shot = run.record(identifier)
            if shot is None or shot.type_name != "SHOT":
                line_number = next((line.line_number for _, _, line in run.field_lines(shot_list.key, "item")
                                    if (split_item(line.value, definition).first or "").strip() == identifier), None)
                problems.append(run.problem("E", "ID-07", shot_list, "item",
                                            f"lists {identifier}, which has no SHOT record",
                                            f"Fix: write the SHOT {identifier} (its batch), or take the item out of "
                                            "the list", line_number=line_number))
    return problems


@register_check("ID-08", level="E", build=1,
                title="SHOT's beats, role or size differ from its list item without a changed list",
                plain="has a shot that differs from its line in the shot list")
def check_id_08(run):
    problems = []
    definition = run.schema.field("SHOTLIST", "item") or {}
    for shot_list in run.records("SHOTLIST"):
        if normalise_word(shot_list.get("status") or "") == "stale":
            continue
        for value in shot_list.get_all("item"):
            item = split_item(value, definition)
            identifier = (item.first or "").strip()
            shot = run.record(identifier)
            if shot is None or shot.type_name != "SHOT" or run.is_omitted(shot):
                continue
            if normalise_word(shot.get("status") or "") == "stale":
                continue
            for field_name in ("beats", "role", "size"):
                listed_value = item.get(field_name)
                shot_value = shot.get(field_name)
                if not listed_value or not shot_value:
                    continue
                if field_name == "beats":
                    same = {normalise_word(piece) for piece in split_list(listed_value)} == \
                        {normalise_word(piece) for piece in split_list(shot_value)}
                else:
                    same = normalise_word(listed_value) == normalise_word(shot_value)
                if not same:
                    problems.append(run.problem("E", "ID-08", shot, field_name,
                                                f"is {quote_for_message(shot_value, 40)} but its list item says "
                                                f"{quote_for_message(listed_value, 40)}",
                                                "Fix: make the shot match its list item, or change the list item first "
                                                "(the shot then goes stale and is redone)"))
    return problems


@register_check("ID-09", level="E", build=1, title="Scene ID width differs from scene_id_digits",
                plain="has a scene number of the wrong width")
def check_id_09(run):
    digits = project_digits(run)
    if digits is None:
        return []
    problems = []
    for key, record in run.index.items():
        width = scene_number_width(key[1])
        if width is not None and width != digits:
            problems.append(run.problem("E", "ID-09", record, None,
                                        f"has a scene number of {width} digits; this project writes scene numbers "
                                        f"with {digits} (scene_id_digits)",
                                        f"Fix: write the scene as SC followed by {digits} digits, as "
                                        f"SC{'1'.zfill(digits)}"))
    for identifier, (_, declaring) in declared_identifiers(run).items():
        width = scene_number_width(identifier)
        if width is not None and width != digits and declaring is not None:
            problems.append(run.problem("E", "ID-09", declaring, None,
                                        f"declares {identifier}, whose scene number has {width} digits; this project "
                                        f"uses {digits}", f"Fix: write SC followed by {digits} digits"))
    return problems


# ---------------------------------------------------------------- the story lines each reference points to

class LineReference:
    """One place a record points into the story: line numbers, a quote anchor, or a story point.

    scope is ('scene', SCnn), ('chapter', CPnn), ('whole', None) or ('scene opened by start', None)."""

    def __init__(self, record_file, record, field_name, line_number, value, form, scope, single=False):
        self.record_file = record_file
        self.record = record
        self.field_name = field_name
        self.line_number = line_number
        self.value = value
        self.form = form
        self.scope = scope
        self.single = single


def record_scene(record):
    return scene_of(record.identifier) if record.type_name in SCENE_FILE_TYPES else None


def line_references(run):
    """Every line number, quote anchor and story point in the records (see LineReference). Cached per run."""
    key = "citations_line_references"
    if key in run.cache:
        return run.cache[key]
    found = []

    def add(record_file, record, name, line, value, scope, single=False):
        value = value.strip()
        if not value or is_empty_word(value):
            return
        if parse_line_numbers(value):
            found.append(LineReference(record_file, record, name, line.line_number, value, "numbers", scope, single))
        elif parse_quote_anchor(value):
            found.append(LineReference(record_file, record, name, line.line_number, value, "anchor", scope, single))

    for record_file, record, line, definition, name in field_values(run):
        type_name = effective_type(run, record)
        kind = definition.get("kind")
        value = line.value.strip()
        own_scene = record_scene(record)
        default_scope = ("scene", own_scene) if own_scene else ("whole", None)
        if kind == "lines":
            if type_name == "SCENE" and name == "lines":
                add(record_file, record, name, line, value, ("scene opened by start", record.identifier))
            elif type_name == "SCENE" and name == "from_lines":
                add(record_file, record, name, line, value, ("whole", None))
            else:
                single = type_name in ("SPEECH", "PROP") and name in ("line", "first_seen")
                add(record_file, record, name, line, value, default_scope, single)
        elif kind == "quote" and type_name == "CHAPTER":
            add(record_file, record, name, line, value, ("chapter", record.identifier), True)
        elif kind == "because_list":
            for piece in split_list(value):
                match = re.match(r"^line:\s*(.+)$", piece, re.IGNORECASE)
                if match:
                    add(record_file, record, name, line, match.group(1), default_scope, True)
        elif kind in STORY_POINT_KINDS:
            for piece in split_list(value):
                point = parse_story_point(piece)
                if point:
                    found.append(LineReference(record_file, record, name, line.line_number, piece, "story point",
                                               ("scene", point[0]), True))
        elif kind == "sub_parts":
            item = split_item(value, definition)
            first_definition = definition.get("first_part") or {}
            first_kind = first_definition.get("kind")
            if item.first and first_kind == "lines":
                scope = default_scope if own_scene else ("whole", None)
                add(record_file, record, name, line, item.first, scope, True)
            elif item.first and first_kind in STORY_POINT_KINDS:
                for piece in split_list(item.first):
                    point = parse_story_point(piece)
                    if point:
                        found.append(LineReference(record_file, record, name, line.line_number, piece, "story point",
                                                   ("scene", point[0]), True))
            for sub_key, sub_value in item.parts:
                entry = sub_part_definition(definition, sub_key) or {}
                sub_kind = entry.get("kind")
                label = f"{name} {sub_key}"
                if sub_kind == "lines":
                    if type_name == "STATE" and name == "from" and item.first:
                        scope = ("scene", item.first.strip())
                    elif type_name == "CHAPTER":
                        scope = ("chapter", record.identifier)
                    elif own_scene:
                        scope = default_scope
                    else:
                        scope = ("whole", None)
                    add(record_file, record, label, line, sub_value, scope, sub_key in ("line", "from"))
                elif sub_kind in STORY_POINT_KINDS:
                    for piece in split_list(sub_value):
                        point = parse_story_point(piece)
                        if point:
                            found.append(LineReference(record_file, record, label, line.line_number, piece,
                                                       "story point", ("scene", point[0]), True))
    run.cache[key] = found
    return found


def scope_lines(run, scope, check_id, left_out):
    """(first, last, complete) for a scope, or None when it cannot be known. complete is False when the story
    given does not hold every line of the scope (an excerpt), so 'not found' cannot be judged."""
    kind, identifier = scope
    story = run.story
    if kind == "scene":
        if identifier is None:
            return None
        lines = run.scene_range(identifier)
        if lines is None:
            if run.scene_left_out(identifier) or (story is not None and story.excerpt):
                left_out.add(identifier)
            return None
        return lines[0], lines[1], story is not None and story.holds(lines[0], lines[1])
    if kind == "chapter":
        lines = run.chapter_range(identifier)
        if lines is None:
            return None
        return lines[0], lines[1], story is not None and story.holds(lines[0], lines[1])
    if story is None:
        return None
    return story.first, story.last, not story.excerpt


def scope_words(scope, first, last):
    kind, identifier = scope
    if kind == "scene":
        return f"{scene_words(identifier)}'s lines ({plain_range(first, last)})"
    if kind == "chapter":
        return f"chapter {identifier}'s lines ({plain_range(first, last)})"
    return f"the story (lines {plain_range(first, last)})"


def scene_containing(run, number):
    for identifier, (first, last) in (run.story.numbered.scenes.items() if run.story is not None else []):
        if first <= number <= last:
            return first, last
    return None


# ---------------------------------------------------------------- CITE-01 to CITE-07

@register_check("CITE-01", level="E", build=1, title="Line reference outside the scene's lines",
                plain="points to story lines outside its scene")
def check_cite_01(run):
    problems = []
    left_out = set()
    not_in_excerpt = False
    for reference in line_references(run):
        if reference.form != "numbers" or run.is_omitted(run.index.get(reference.record.key)):
            continue
        ranges = parse_line_numbers(reference.value) or []
        kind, identifier = reference.scope
        if kind == "scene opened by start":
            kind = "whole"
        if kind in ("scene", "chapter"):
            lines = run.scene_range(identifier) if kind == "scene" else run.chapter_range(identifier)
            if lines is None:
                if kind == "scene" and (run.scene_left_out(identifier) or (run.story is not None and run.story.excerpt)):
                    left_out.add(identifier)
                continue
            first, last = lines
            outside = [pair for pair in ranges if pair[0] < first or pair[1] > last]
            if outside:
                shown = ", ".join(plain_range(*pair) for pair in outside)
                where = scene_words(identifier) if kind == "scene" else f"chapter {identifier}"
                problems.append(run.problem("E", "CITE-01", reference.record, reference.field_name,
                                            f"points to line {shown}, outside {where}'s lines ({plain_range(first, last)})",
                                            f"Fix: cite lines of {where} only (the numbered story shows them)",
                                            line_number=reference.line_number, file_name=reference.record_file.name))
            continue
        story = run.story
        if story is None:
            continue
        for pair in ranges:
            if story.holds(pair[0], pair[1]):
                continue
            if story.excerpt:
                not_in_excerpt = True
                continue
            problems.append(run.problem("E", "CITE-01", reference.record, reference.field_name,
                                        f"points to line {plain_range(*pair)}, outside the story's lines "
                                        f"({plain_range(story.first, story.last)})",
                                        "Fix: cite a line that exists in the numbered story",
                                        line_number=reference.line_number, file_name=reference.record_file.name))
    left_out_skip(run, "CITE-01", left_out)
    if not_in_excerpt:
        run.skip("CITE-01", "line numbers outside the excerpt of the story given: not in the excerpt, not checked")
    if run.story is None:
        run.skip("CITE-01", "lines outside any scene: story not present, so only lines inside scenes were checked")
    return problems


def quote_problem(run, story, quote, first, last):
    """CITE-02's wording for one quoted string in lines first..last, or None when it holds at least 3 words and is
    found exactly once. Returns ('skip', None) when it is not found but the story given is only part of the scope."""
    from .read_story import real_words
    if len(real_words(quote)) < story.numbered.minimum_words:
        return f"{quote_for_message(quote)} has fewer than {story.numbered.minimum_words} words"
    found = story.find(quote, first, last)
    if len(found) == 1:
        return None
    if not found:
        return "not found"
    shown = ", ".join(str(number) for number in sorted(set(found))[:5])
    return f"{quote_for_message(quote)} is found {len(found)} times (lines {shown})"


@register_check("CITE-02", level="E", build=1,
                title="A quote anchor or story point not found exactly once in its scope, or under 3 words",
                plain="quotes words that are not found exactly once where it points")
def check_cite_02(run):
    if run.story_missing("CITE-02"):
        return []
    problems = []
    left_out = set()
    partial = False
    story = run.story
    for reference in line_references(run):
        if reference.form not in ("anchor", "story point"):
            continue
        if run.is_omitted(run.index.get(reference.record.key)):
            continue
        if reference.form == "story point":
            point = parse_story_point(reference.value)
            quotes = [point[1]] if point else []
        else:
            quotes = parse_quote_anchor(reference.value) or []
        kind, identifier = reference.scope
        scopes = []
        if kind == "scene opened by start":
            whole = (story.first, story.last, not story.excerpt)
            scopes = [("whole", None, whole)]
            if len(quotes) > 1:
                start = story.find(quotes[0], story.first, story.last)
                opened = scene_containing(run, start[0]) if len(start) == 1 else None
                if opened is not None:
                    scopes.append(("scene", None, (opened[0], opened[1], story.holds(*opened))))
                else:
                    scopes.append(("whole", None, whole))
        else:
            lines = scope_lines(run, reference.scope, "CITE-02", left_out)
            if lines is None:
                continue
            scopes = [(kind, identifier, lines)] * len(quotes)
        for index, quote in enumerate(quotes):
            scope_kind, scope_identifier, (first, last, complete) = scopes[min(index, len(scopes) - 1)]
            wrong = quote_problem(run, story, quote, first, last)
            if wrong is None:
                continue
            if wrong == "not found":
                if not complete:
                    partial = True
                    continue
                wrong = f"{quote_for_message(quote)} is not found in {scope_words((scope_kind, scope_identifier), first, last)}"
            where = scope_words((scope_kind, scope_identifier), first, last)
            problems.append(run.problem("E", "CITE-02", reference.record, reference.field_name, wrong,
                                        f"Fix: quote at least 3 words that occur exactly once in {where}, copied "
                                        "exactly, or give line numbers", line_number=reference.line_number,
                                        file_name=reference.record_file.name))
    left_out_skip(run, "CITE-02", left_out)
    if partial:
        run.skip("CITE-02", "quotes whose scope reaches beyond the excerpt of the story given and that the excerpt "
                            "does not hold: not in the excerpt, not checked")
    return problems


def quote_search_scope(run, record, before_text, item_lines, left_out):
    """Where a quoted string of a field value must be found (G12): the item's own cited lines; else the scene
    named just before the quote; else the record's scene; else the whole story. None when it cannot be known."""
    story = run.story
    if item_lines is not None:
        return item_lines
    named = SCENE_BEFORE_QUOTE.search(before_text)
    if named:
        return scope_lines(run, ("scene", named.group(1)), "CITE-03", left_out)
    own_scene = record_scene(record)
    if own_scene:
        return scope_lines(run, ("scene", own_scene), "CITE-03", left_out)
    return story.first, story.last, not story.excerpt


def item_cited_lines(run, first_part):
    """(first, last, complete) of an evidence or cause item's own line (numbers or a single quote anchor)."""
    story = run.story
    numbers = parse_line_numbers(first_part.strip())
    if numbers:
        first, last = numbers[0][0], numbers[-1][1]
        return first, last, story.holds(first, last)
    quotes = parse_quote_anchor(first_part.strip())
    if quotes:
        found = story.find(quotes[0])
        if len(found) == 1:
            return found[0], found[0], True
    return None


@register_check("CITE-03", level="E", build=1, title="A quoted string not found in the cited or scene lines",
                plain="quotes words that are not in the story lines it cites")
def check_cite_03(run):
    if run.story_missing("CITE-03"):
        return []
    problems = []
    left_out = set()
    partial = False
    story = run.story

    def check_text(record_file, record, label, line, text, item_lines=None):
        nonlocal partial
        for match in QUOTED.finditer(text):
            quote = match.group(1).strip()
            if not quote:
                continue
            lines = quote_search_scope(run, record, text[:match.start()], item_lines, left_out)
            if lines is None:
                continue
            first, last, complete = lines
            if story.find(quote, first, last):
                continue
            if not complete:
                partial = True
                continue
            problems.append(run.problem("E", "CITE-03", record, label,
                                        f"quotes {quote_for_message(quote)}, which is not found in lines "
                                        f"{plain_range(first, last)}",
                                        "Fix: copy the story's words exactly, or drop the double quotes where the "
                                        "words are not the story's (G12)", line_number=line.line_number,
                                        file_name=record_file.name))

    for record_file, record, line, definition, name in field_values(run):
        type_name = effective_type(run, record)
        if type_name in NOT_STORY_TEXT_TYPES or record.type_name in NOT_STORY_TEXT_TYPES:
            continue
        if run.is_omitted(run.index.get(record.key)):
            continue
        kind = definition.get("kind")
        if kind in ANCHOR_KINDS or kind in ("because_list", "quote") or (type_name == "SPEECH" and name == "text"):
            continue
        value = line.value
        if '"' not in value and "“" not in value:
            continue
        if kind != "sub_parts":
            check_text(record_file, record, name, line, value)
            continue
        item = split_item(value, definition)
        first_definition = definition.get("first_part") or {}
        item_lines = None
        if item.first and first_definition.get("kind") == "lines":
            item_lines = item_cited_lines(run, item.first)
        elif item.first and first_definition.get("kind") not in ANCHOR_KINDS:
            check_text(record_file, record, name, line, item.first)
        for sub_key, sub_value in item.parts:
            entry = sub_part_definition(definition, sub_key) or {}
            sub_kind = entry.get("kind")
            if sub_kind in ANCHOR_KINDS or (sub_kind == "quote" and sub_key == "words"):
                continue
            if sub_kind == "quote":
                if item_lines is None and item.first and first_definition.get("kind") == "lines":
                    continue
                check_text(record_file, record, f"{name} {sub_key}", line, sub_value, item_lines)
            else:
                check_text(record_file, record, f"{name} {sub_key}", line, sub_value)
    left_out_skip(run, "CITE-03", left_out)
    if partial:
        run.skip("CITE-03", "quoted strings the excerpt of the story does not hold, whose lines lie outside it: not "
                            "in the excerpt, not checked")
    return problems


def comparable_words(text):
    """Speech words compared the way CITE-04 compares them: curly quotes straight, spaces collapsed."""
    from .read_story import normalise_quote
    return normalise_quote(text).strip()


def speech_text(run, identifier):
    """The story's text of a speech: speeches.json, else a prose SPEECH record's text; None when unknown."""
    entry = run.speeches.get(identifier)
    if entry is not None:
        return entry.get("text")
    record = run.record(identifier)
    if record is not None and record.type_name == "SPEECH":
        return record.get("text")
    return None


def hear_items(run):
    """(record_file, SHOT copy, line, item) for every hear item of every shot copy."""
    definition = run.schema.field("SHOT", "hear") or {}
    items = []
    for record_file, record, line, field_definition, name in field_values(run):
        if record.type_name != "SHOT" or name != "hear" or is_empty_word(line.value):
            continue
        items.append((record_file, record, line, split_item(line.value, definition)))
    return items


@register_check("CITE-04", level="E", build=1, title="words on a hear item differ from the speech's text",
                plain="gives words for a speech that differ from the story")
def check_cite_04(run):
    problems = []
    unknown = False
    for record_file, record, line, item in hear_items(run):
        words = item.get("words")
        if words is None or run.is_omitted(run.index.get(record.key)):
            continue
        identifier = (item.first or "").strip()
        text = speech_text(run, identifier)
        if text is None:
            unknown = True
            continue
        written = words.strip()
        if len(written) >= 2 and written[0] in '"“' and written[-1] in '"”':
            written = written[1:-1]
        if comparable_words(written) != comparable_words(text):
            problems.append(run.problem("E", "CITE-04", record, "hear words",
                                        f"of {identifier} are {quote_for_message(written, 50)}, but the speech is "
                                        f"{quote_for_message(text, 50)}",
                                        "Fix: copy the speech's words exactly (parentheticals left out), or leave "
                                        "words out: code shows the speech", line_number=line.line_number,
                                        file_name=record_file.name))
    if unknown:
        run.skip("CITE-04", "speeches whose text is not present here (speeches.json missing, or not in the "
                            "excerpt): not checked")
    return problems


def resolved_ranges(run, value, scene_identifier):
    """A lines value as [(first, last)]: numbers directly; a quote anchor resolved in the scene (adopt's rule)."""
    numbers = parse_line_numbers(value.strip())
    if numbers:
        return numbers
    if run.story is None or not parse_quote_anchor(value.strip()):
        return None
    lines = run.scene_range(scene_identifier) if scene_identifier else None
    first, last = lines if lines else (None, None)
    resolved = run.story.numbered.resolve_lines(value.strip(), first, last)
    return [resolved] if resolved else None


def cue_line(run, identifier):
    entry = run.speeches.get(identifier)
    if entry is not None:
        return entry.get("line")
    record = run.record(identifier)
    if record is None or record.type_name != "SPEECH" or not record.get("line"):
        return None
    ranges = resolved_ranges(run, record.get("line"), scene_of(identifier))
    return ranges[0][0] if ranges else None


@register_check("CITE-05", level="W", build=1, title="Heard speech whose cue lies outside the shot's lines",
                plain="hears a speech whose line is outside the shot's lines")
def check_cite_05(run):
    problems = []
    for shot in run.records("SHOT"):
        if not shot.get("lines") or not shot.get_all("hear"):
            continue
        ranges = resolved_ranges(run, shot.get("lines"), scene_of(shot.identifier))
        if not ranges:
            continue
        for record_file, copy, line in run.field_lines(shot.key, "hear"):
            if is_empty_word(line.value):
                continue
            identifier = (split_item(line.value).first or "").strip()
            cue = cue_line(run, identifier)
            if cue is None:
                continue
            if not any(first <= cue <= last for first, last in ranges):
                shown = ", ".join(plain_range(first, last) for first, last in ranges)
                problems.append(run.problem("W", "CITE-05", copy, "hear",
                                            f"hears {identifier}, whose cue (line {cue}) is outside the shot's lines "
                                            f"({shown})",
                                            "Fix: widen the shot's lines to the cue, or hear the speech in the shot "
                                            "that shows its lines (a pre-lap is fine: say so in why)",
                                            line_number=line.line_number, file_name=record_file.name))
    return problems


def spoken_words(text):
    """The words inside double quotes of a prose paragraph (all its words when it has none), lowercased."""
    from .read_story import normalise_quote
    text = normalise_quote(text)
    segments = DOUBLE_QUOTED_SPEECH.findall(text)
    source = " ".join(segments) if segments else text
    return [word.lower() for word in WORD.findall(source)]


def contains_run(haystack, needle):
    if not needle:
        return True
    size = len(needle)
    return any(haystack[index:index + size] == needle for index in range(len(haystack) - size + 1))


@register_check("CITE-06", level="E", build=1, title="Prose SPEECH with origin story not found word for word",
                plain="has a speech whose words are not found word for word in the story")
def check_cite_06(run):
    speeches = [record for record in run.records("SPEECH") if normalise_word(record.get("origin") or "") == "story"]
    if not speeches:
        return []
    if run.story_missing("CITE-06"):
        return []
    problems = []
    partial = False
    from .read_story import normalise_quote
    for speech in speeches:
        text = speech.get("text")
        if not text or not speech.get("line"):
            continue
        ranges = resolved_ranges(run, speech.get("line"), scene_of(speech.identifier))
        if not ranges:
            continue
        first, last = ranges[0][0], ranges[-1][1]
        if not run.story.holds(first, last):
            partial = True
            continue
        paragraph = " ".join(run.story.numbered.line(number) for number in range(first, last + 1))
        wanted = [word.lower() for word in WORD.findall(normalise_quote(text))]
        if contains_run(spoken_words(paragraph), wanted) or contains_run(
                [word.lower() for word in WORD.findall(normalise_quote(paragraph))], wanted):
            continue
        problems.append(run.problem("E", "CITE-06", speech, "text",
                                    f"{quote_for_message(text, 50)} is not found word for word in line "
                                    f"{plain_range(first, last)}",
                                    "Fix: copy the spoken words exactly from that line, or mark the speech origin "
                                    "adapted (or invented) if the words were changed"))
    if partial:
        run.skip("CITE-06", "speeches whose lines are not in the excerpt of the story given: not checked")
    return problems


def cue_name(text):
    name = re.sub(r"\(.*?\)", "", text or "")
    name = re.sub(r"\bCONT'?D\b\.?", "", name, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", name.replace("@", "")).strip().upper()


@register_check("CITE-07", level="E", build=2, title="A name in a story-derived field that matches no alias",
                plain="uses a name the story does not use for that character")
def check_cite_07(run):
    if not run.speeches:
        return []
    problems = []
    reported = set()
    for identifier, entry in run.speeches.items():
        speaker = entry.get("speaker")
        character = run.record(speaker) if speaker else None
        if character is None or character.type_name != "CHARACTER":
            continue
        name = cue_name(entry.get("cue"))
        aliases = {cue_name(alias) for alias in split_list(character.get("names") or "")}
        if not name or name in aliases or (speaker, name) in reported:
            continue
        reported.add((speaker, name))
        problems.append(run.problem("E", "CITE-07", character, "names",
                                    f"does not hold {quote_for_message(name)}, the cue of {identifier}",
                                    f"Fix: add {name} to names (every name the story uses for this character)"))
    return problems


# ---------------------------------------------------------------- guards on an inbox before apply merges it

def unit_of_inbox(inbox):
    return Path(inbox.name).stem


@register_apply_check
def check_identity_before_apply(project, inbox, current_files, context):
    """ID-01, ID-04 and ID-06 on an inbox the AI wrote, before apply merges it (apply refuses on any E line)."""
    problems = []
    stored = context.current_records or {}
    stored_types = {}
    for key in stored:
        if key[1]:
            stored_types.setdefault(key[1], key[0])
    seen = {}
    manifest = project.read_manifest() if project is not None else {}
    omitted_before = set(manifest.get("omitted_ids") or [])
    blocks = issued_blocks(manifest, unit_of_inbox(inbox))
    list_definition = context.schema.field("SHOTLIST", "item") or {}
    value_definition = context.schema.field("SCENE", "value") or {}
    for record in inbox.records:
        if not record.known_type:
            continue
        label_line = record.heading_line_number
        if record.key in seen:
            problems.append(Problem("E", "ID-01", record.label, None,
                                    f"appears twice in this inbox (lines {seen[record.key]} and {label_line})",
                                    "Fix: send each record once", file_name=inbox.name, line_number=label_line))
        seen.setdefault(record.key, label_line)
        if record.identifier and record.identifier in stored_types and stored_types[record.identifier] != record.type_name:
            problems.append(Problem("E", "ID-01", record.label, None,
                                    f"is already the ID of a {stored_types[record.identifier]} record",
                                    "Fix: use an ID from the issued block", file_name=inbox.name, line_number=label_line))
        stored_copy = stored.get(record.key)
        stored_status = normalise_word(stored_copy.get("status") or "") if stored_copy is not None else ""
        if stored_status == "omitted" or (stored_copy is None and record.identifier in omitted_before):
            problems.append(Problem("E", "ID-04", record.label, None,
                                    "was cut earlier (omitted); its ID is never used again",
                                    "Fix: use the next free ID from the issued block", file_name=inbox.name,
                                    line_number=label_line))
        if stored_copy is None and record.identifier:
            wanted = outside_blocks(record.identifier, record.type_name, blocks)
            if wanted:
                problems.append(Problem("E", "ID-06", record.label, None,
                                        f"is outside the IDs issued for this unit ({block_words(wanted)})",
                                        "Fix: copy an ID from the issued block in the handout", file_name=inbox.name,
                                        line_number=label_line))
        for field_name, declared_type, definition in (("item", "SHOT", list_definition),
                                                     ("value", "VALUE", value_definition)):
            if (record.type_name, field_name) not in (("SHOTLIST", "item"), ("SCENE", "value")):
                continue
            for line in record.field_lines(field_name):
                first = (split_item(line.value, definition).first or "").strip()
                if not first:
                    continue
                target = stored.get((declared_type, first)) if declared_type == "SHOT" else None
                if (target is not None and normalise_word(target.get("status") or "") == "omitted") \
                        or first in omitted_before:
                    problems.append(Problem("E", "ID-04", record.label, field_name,
                                            f"declares {first}, which was cut earlier; its ID is never used again",
                                            "Fix: use the next free ID from the issued block", file_name=inbox.name,
                                            line_number=line.line_number))
                wanted = outside_blocks(first, declared_type, blocks)
                if wanted:
                    problems.append(Problem("E", "ID-06", record.label, field_name,
                                            f"declares {first}, outside the IDs issued for this unit "
                                            f"({block_words(wanted)})",
                                            "Fix: copy an ID from the issued block in the handout",
                                            file_name=inbox.name, line_number=line.line_number))
    return problems
