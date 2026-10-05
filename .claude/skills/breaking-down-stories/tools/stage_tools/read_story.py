"""read_story.py: read a story file of any common kind, number its lines, split it into scenes or chapters, find
the speeches, cues, transitions, title lines, cards, capitalised words and light words, propose aliases, write the
odd-lines report, count what the first estimate needs, and turn quote anchors into line numbers (blueprint section
3 step 1 and 7.1; A3 §4.3; D14). It also runs the commands read, lines and selftest.

In plain words:
- load_story_file turns a file into lines: The Catch's own layout, Fountain, plain screenplay text, Final Draft
  (.fdx), Word (.docx), EPUB, Markdown or plain prose, and a PDF with a text layer when a converter is present.
  Where the file itself says what a line is (Final Draft paragraph types, Word styles, EPUB headings) the line
  keeps that as a hint;
- read_story_lines finds the kind of story and its parts: scenes, speeches and characters for a screenplay; the
  title, front matter and chapters for prose; the capitalised words and light words of each scene; and every
  line code could not place (the odd-lines report the AI confirms or corrects);
- NumberedStory answers later questions about the numbered lines: a scene's lines, a speech's block, and where
  a quote anchor or a story point is (the adopt rule of blueprint 5.1 G5, used by CITE-02 and adopt);
- read_into_project writes 03 Story - numbered, 04 Scene list, 05 Story plan (chapters), 07 Characters and
  voices, the PROJECT fields, the format choice, the length choice, speeches.json and story map.json.

Words are counted the way the common word-count command counts them in its plain setting (wc -w): pieces between
spaces that hold at least one plain keyboard character, so a dash standing alone between spaces is punctuation.
This gives The Long Places' 49,152 words and The Catch's 1,579 words of speech and 7,091 words of action.

Standard library only. A PDF is read only when a converter (the pdftotext program or the pypdf package) exists.

After the three-scene test of the fixed kit (Project notes 35 and 36):
- the self-test handout prints the allowed values of the fields it asks for.
"""

import codecs
import html.parser
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import unicodedata
import zipfile
import xml.etree.ElementTree as ElementTree
from dataclasses import dataclass, field as dataclass_field
from pathlib import Path

from .project_files import (CHOICES_FILE, MACHINE_FOLDER, ORIGINAL_FOLDER, SCENE_LIST_FILE, START_HERE, Project,
                            StageStop, detect_surface, fingerprint_of_file, history_run_folder, keep_in_history,
                            now, today)
from .record_format import (DIVIDER_LINE, Record, TextBlock, add_record, ensure_end_line, make_record,
                            merge_copies, new_record_file, normalise_word, parse_file, parse_line_numbers,
                            parse_quote_anchor, parse_story_point, split_list, write_file)

NUMBERED_STORY_FILE = "03 Story - numbered.md"
STORY_PLAN_FILE = "05 Story plan.md"
CHARACTERS_FILE = "07 Characters and voices.md"
SPEECHES_FILE = "speeches.json"
STORY_MAP_FILE = "story map.json"
SELFTEST_UNIT = "U-00-SELFTEST"
STORY_MAP_VERSION = 1

EXCERPT_START = "STAGE EXCERPT HEADER"
EXCERPT_END = "END OF STAGE EXCERPT HEADER"

# D14 Recipe I5: a page with fewer characters than this has no text layer (a scan).
SCANNED_PAGE_CHARACTERS = 50

# Line types (what each numbered line is).
BLANK, TITLE, HEADING, CUE, PARENTHETICAL, DIALOGUE, TRANSITION, ACTION = (
    "blank", "title", "heading", "cue", "parenthetical", "dialogue", "transition", "action")
CARD, NOTE, SECTION, SYNOPSIS, PAGE_BREAK, BONEYARD, LYRIC, CUE_WITH_SPEECH = (
    "card", "note", "section", "synopsis", "page_break", "boneyard", "lyric", "cue_with_speech")
CHAPTER_HEADING, OTHER_HEADING, PARAGRAPH, QUOTATION, FRONT_MATTER = (
    "chapter_heading", "other_heading", "paragraph", "quotation", "front_matter")
SPEECH_TYPES = (PARENTHETICAL, DIALOGUE, LYRIC)
STORY_ELEMENT_TYPES = (ACTION, CUE, DIALOGUE, PARENTHETICAL, LYRIC, CUE_WITH_SPEECH)

# ---------------------------------------------------------------- word lists the reader uses (code data)

# A3 §4.3 step 5 test 3: capitalised words that are sounds, and common sound words.
SOUND_WORDS = {
    "GUNSHOT", "GUNSHOTS", "SHOT", "SHOTS", "BANG", "BANGS", "CLACK", "CLACKS", "CLICK", "CLICKS", "CLANG", "CLANGS",
    "CLANK", "CLANKS", "THUD", "THUDS", "THUMP", "THUMPS", "CRASH", "CRASHES", "BOOM", "BOOMS", "SHRIEK", "SHRIEKS",
    "SCREAM", "SCREAMS", "HUM", "HUMS", "BUZZ", "BUZZES", "BEEP", "BEEPS", "ALARM", "ALARMS", "SIREN", "SIRENS",
    "RING", "RINGS", "RINGING", "KNOCK", "KNOCKS", "SLAM", "SLAMS", "CREAK", "CREAKS", "HISS", "HISSES", "PUMP",
    "FIRES", "WHIRR", "WHIR", "RUMBLE", "RUMBLES", "ROAR", "ROARS", "SNAP", "SNAPS", "CRACK", "CRACKS", "POP",
    "POPS", "SPLASH", "RATTLE", "RATTLES", "TICK", "TICKS", "WAIL", "WAILS", "HOWL", "HOWLS", "WHISTLE", "BLAST",
    "EXPLOSION", "EXPLODES", "THUNDER", "CLATTER", "SCREECH", "SQUEAL", "CHIME", "CHIMES", "BARK", "BARKS", "GROWL",
    "HONK", "SMASH", "SHATTERS", "BUZZER", "WHOOSH", "THWACK", "DING", "DRIP", "DRIPS", "SIZZLE", "STATIC",
}
# A3 §4.3 step 5 test 1: role words that introduce a person who may never speak.
ROLE_WORDS = {
    "FIGURE", "GUARD", "GUARDS", "NURSE", "NURSES", "TECHNICIAN", "TECHNICIANS", "DOCTOR", "OFFICER", "OFFICERS",
    "SOLDIER", "SOLDIERS", "DRIVER", "MAN", "MEN", "WOMAN", "WOMEN", "BOY", "GIRL", "CHILD", "CHILDREN", "STRANGER",
    "WAITER", "WAITRESS", "CLERK", "PRIEST", "PILOT", "WORKER", "WORKERS", "CROWD", "POLICEMAN", "POLICE",
    "NEIGHBOUR", "NEIGHBOR", "SECRETARY", "RECEPTIONIST", "TEACHER", "STUDENT", "PATIENT", "ORDERLY", "PARAMEDIC",
    "CREW", "ENGINEER", "PASSENGER", "PASSENGERS", "VISITOR", "COURIER", "BARMAN", "BARTENDER", "MOTHER",
    "FATHER", "OLD MAN", "OLD WOMAN", "YOUNG MAN", "YOUNG WOMAN", "GUEST", "GUESTS", "SURGEON", "SCIENTIST",
}
# A3 §4.3 step 5 test 2: words near a capitalised word that show it is printed, displayed or read.
TEXT_SIGNALS = {
    "labelled", "labeled", "marked", "reads", "read", "says", "stitched", "stamped", "printed", "written",
    "painted", "sign", "signs", "screen", "monitor", "display", "displays", "visor", "label", "tag", "button",
    "readout", "caption", "title", "hits", "presses", "pushes", "punches", "taps", "spells", "lettered",
    "engraved", "headline", "banner", "plate", "flashes",
}
DISPLAY_WORDS = {"visor", "screen", "monitor", "display", "readout", "dashboard", "tablet", "hud", "diagram", "chart",
                 "gauge", "dial", "map"}
FOLLOWING_TEXT_SIGNALS = {"stitched", "stamped", "printed", "written", "painted", "engraved", "lettered"}
DESCRIBING_WORDS = {
    "small", "flat", "black", "white", "grey", "gray", "steel", "glass", "thin", "thick", "heavy", "old", "big",
    "large", "little", "open", "dark", "red", "green", "blue", "yellow", "brass", "metal", "wooden", "plastic",
    "paper", "long", "short", "tiny", "huge", "second", "first", "single", "broken", "empty", "full", "clear",
    "bright", "pale", "cold", "hot", "wet", "dry", "sealed", "locked", "new", "battered", "rusted", "rusty",
    "silver", "gold", "leather", "rubber", "iron", "stone", "narrow", "wide", "round", "square",
}
DETERMINERS = {"a", "an", "the", "one", "two", "three", "four", "five", "six", "her", "his", "its", "their", "my",
               "your", "our", "this", "that", "these", "those", "some", "another", "each", "every", "no"}
AGE_OR_DESCRIPTION = re.compile(
    r"^,\s*(?:(?:early|mid|late|mid-)\s*)?(?:teens|twenties|thirties|forties|fifties|sixties|seventies|eighties|"
    r"nineties|\d+|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|young|old|elderly|middle|a man|a woman|"
    r"a boy|a girl|a child|his|her|tall|short|thin|small|big)\b", re.IGNORECASE)
# B2 P2: light sources, colours, brightness and darkness words, and light changes.
LIGHT_WORDS = {
    "light", "lights", "lit", "lamp", "lamps", "lamplight", "torch", "torches", "torchlight", "flashlight",
    "candle", "candles", "candlelight", "fire", "firelight", "flame", "flames", "sun", "sunlight", "sunrise",
    "sunset", "moon", "moonlight", "dawn", "dusk", "twilight", "neon", "bulb", "lantern", "glow", "glows",
    "glowing", "headlamp", "headlight", "headlights", "spotlight", "floodlight", "strobe", "flare", "beam",
    "beams", "lightning", "red", "green", "blue", "yellow", "orange", "white", "black", "grey", "gray", "gold",
    "golden", "silver", "amber", "purple", "violet", "pink", "brown", "bright", "brightness", "dim", "dims",
    "pale", "glare", "dark", "darker", "darkness", "shadow", "shadows", "gloom", "glint", "gleam", "shine",
    "shines", "shining", "flicker", "flickers", "flash", "flashes", "blaze", "blinding", "unlit",
}
STOPWORDS = {
    "english": {"the", "and", "of", "to", "a", "in", "is", "it", "that", "was", "he", "she", "for", "on", "with",
                "as", "his", "her", "at", "you", "not", "but", "they", "this", "have"},
    "french": {"le", "la", "les", "et", "de", "des", "un", "une", "est", "que", "qui", "dans", "pas", "il", "elle",
               "je", "vous", "nous", "sur", "pour", "avec", "au", "du"},
    "german": {"der", "die", "das", "und", "ist", "nicht", "ein", "eine", "ich", "sie", "er", "es", "mit", "auf",
               "zu", "den", "dem", "von", "wir", "auch", "sich"},
    "spanish": {"el", "la", "los", "las", "y", "de", "que", "en", "un", "una", "es", "no", "se", "por", "con",
                "para", "su", "lo", "al", "del", "pero"},
    "italian": {"il", "lo", "la", "gli", "le", "e", "di", "che", "un", "una", "non", "per", "con", "sono", "del",
                "della", "mi", "si", "ma", "come"},
    "portuguese": {"o", "a", "os", "as", "e", "de", "que", "em", "um", "uma", "não", "do", "da", "para", "com",
                   "se", "por", "mais", "seu", "sua"},
    "dutch": {"de", "het", "een", "en", "van", "is", "niet", "dat", "ik", "je", "hij", "zij", "op", "met", "voor",
              "maar", "ook", "te"},
    "turkish": {"ve", "bir", "bu", "da", "de", "ne", "için", "ile", "çok", "ama", "gibi", "daha", "o", "ben",
                "sen", "değil", "var", "yok", "mi"},
}
# The blueprint's step 4: lines past the cap are still listed when they name something one can see.
PHYSICAL_NOUNS = {
    "hand", "hands", "face", "eyes", "eye", "hair", "head", "arm", "arms", "shoulder", "shoulders", "finger",
    "fingers", "palm", "leg", "legs", "foot", "feet", "mouth", "lips", "neck", "back", "skin", "scar", "beard",
    "coat", "jacket", "shirt", "sleeve", "sleeves", "boots", "boot", "shoes", "gloves", "glove", "helmet", "suit",
    "cardigan", "trousers", "dress", "hat", "cap", "ring", "watch", "collar", "belt", "bag", "blood", "wound",
    "steel", "glass", "wood", "metal", "paper", "leather", "brass", "stone",
}
PROSE_NAME_STOPWORDS = {
    "The", "A", "An", "I", "It", "He", "She", "They", "We", "You", "This", "That", "These", "Those", "But", "And",
    "Or", "If", "When", "Then", "There", "Here", "What", "Who", "Why", "How", "Where", "In", "On", "At", "Of",
    "For", "To", "From", "With", "By", "As", "So", "No", "Yes", "Not", "Now", "One", "Two", "My", "Her", "His",
    "Their", "Our", "Your", "Its", "Is", "Was", "Be", "Do", "Did", "All", "Some", "Every", "After", "Before",
    "Once", "Only", "Even", "Still", "Just", "Our", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
    "Saturday", "Sunday", "January", "February", "March", "April", "May", "June", "July", "August", "September",
    "October", "November", "December", "Chapter",
}

# ---------------------------------------------------------------- patterns

PLAIN_CHARACTER = re.compile(r"[!-~]")
PLAIN_SPACE = re.compile(r"[ \t\n\r\f\v]+")
LETTER_OR_DIGIT = re.compile(r"[^\W_]")
CATCH_HEADING = re.compile(r"^## (INT|EXT)")
SCREENPLAY_HEADING = re.compile(r"^(?:(\d+[A-Z]?)[.\s]\s*)?(INT\.?/EXT|EXT\.?/INT|INT/EXT|I/E|INT|EXT|EST)[.\s]")
HEADING_PREFIX = re.compile(r"^(INT\.?\s*/\s*EXT|EXT\.?\s*/\s*INT|INT/EXT|I/E|INT|EXT|EST)\.?\s*", re.IGNORECASE)
FOUNTAIN_SCENE_NUMBER = re.compile(r"\s*#([\w.\-]+)#\s*$")
LEADING_SCENE_NUMBER = re.compile(r"^(\d+[A-Z]?)[.\s]\s*(?=(?:INT|EXT|EST|I/E))")
PAREN_LINE = re.compile(r"^\(.*\)$")
TITLE_KEY = re.compile(r"^(title|credit|author|authors|source|draft date|date|contact|copyright|notes|revision)\s*:",
                       re.IGNORECASE)
TIME_WORDS = re.compile(
    r"\b(DAY|NIGHT|MORNING|EVENING|AFTERNOON|DAWN|DUSK|SUNSET|SUNRISE|MIDNIGHT|NOON|LATER|CONTINUOUS|SAME|"
    r"MOMENTS LATER|BEFORE DAWN|EARLY|LATE|MAGIC HOUR|TWILIGHT)\b")
PRESENTATION_WORDS = [
    (re.compile(r"\b(FLASHBACK|FLASH BACK|EARLIER|YEARS AGO|THE PAST)\b"), "flashback"),
    (re.compile(r"\b(DREAM|NIGHTMARE|FANTASY|IMAGINED|VISION)\b"), "dream"),
    (re.compile(r"\b(MONTAGE|SERIES OF SHOTS)\b"), "montage"),
    (re.compile(r"\b(RECORDING|RECORDED|FOOTAGE|PLAYBACK|VIDEO|ON TAPE)\b"), "recording"),
    (re.compile(r"\b(ON THE|ON A|SCREEN|MONITOR|TABLET|TV|TELEVISION|PHONE|CAMERA|FEED|LIVE|WEBCAM)\b"), "on_screen"),
    (re.compile(r"\b(LETTER)\b"), "letter"),
]
TRANSITION_WORDS = [
    (re.compile(r"^FADE\s*IN\b"), "fade_in"),
    (re.compile(r"^(FADE\s*OUT|FADE\s*TO\s*BLACK|FADE\s*TO\s*WHITE)\b"), "fade_out"),
    (re.compile(r"^(CUT\s*TO\s*BLACK|SMASH\s*TO\s*BLACK|BLACKOUT|BLACK\s*OUT)\b"), "cut_to_black"),
    (re.compile(r"^((LAP|CROSS|SLOW)\s*)?DISSOLVE\b"), "dissolve"),
    (re.compile(r"^SMASH\s*CUT\b"), "smash_cut"),
    (re.compile(r"^MATCH\s*CUT\b"), "match_cut"),
    (re.compile(r"^((HARD|JUMP|QUICK)\s*)?CUT(\s*TO)?\b"), "cut"),
]
PLAIN_TRANSITION_LINES = {"FADE IN:", "FADE IN.", "FADE OUT.", "FADE OUT:", "FADE OUT", "FADE TO BLACK.",
                          "CUT TO BLACK.", "CUT TO BLACK", "FADE TO BLACK", "BLACKOUT."}
EXTENSION = re.compile(r"\s*\(([^()]*)\)\s*$")
CAPITALS = re.compile(r"(?<![\w'’])[A-Z][A-Z0-9'’\-]*[A-Z0-9](?:\s[A-Z][A-Z0-9'’\-]*[A-Z0-9])*(?![\w'’])")
ROMAN_OR_NUMBER_HEADING = re.compile(r"^(?:[IVXLCDM]+|\d+)\.(?:\s|$)")
CHAPTER_WORD_HEADING = re.compile(r"^chapter\b", re.IGNORECASE)
PLAIN_CHAPTER_LINE = re.compile(r"^(?:CHAPTER|Chapter)\s+[\w-]+[.:]?(?:\s.*)?$|^[IVXLC]+\.?$")
STAGE_HEADING = re.compile(r"^(SCENE|Scene)\s+([IVXLC]+|\d+|[A-Z][a-z]+)\b")
ACT_HEADING = re.compile(r"^(ACT|Act)\s+([IVXLC]+|\d+|[A-Z][a-z]+)\b")
INLINE_CUE = re.compile(r"^([A-Z][A-Z0-9 .'’\-]{0,30}[A-Z])(\s*\([^)]*\))?\s*[.:]\s+(\S.*)$")
COMIC_PAGE = re.compile(r"^PAGE\s+(\w+)", re.IGNORECASE)
COMIC_PANEL = re.compile(r"^PANEL\s+\d+", re.IGNORECASE)
GAME_MARKERS = [re.compile(r"^\s*->\s*\w"), re.compile(r"^===\s*\w+\s*===\s*$"), re.compile(r"^::\s*\S"),
                re.compile(r"^title:\s*\S")]


# ---------------------------------------------------------------- small helpers

def constant(constants, name, default=None):
    """The value of a named constant in rules/constants.json (the 5.8 table or the blueprint's other numbers)."""
    constants = constants or {}
    entry = constants.get("constants", {}).get(name)
    if entry is None:
        entry = constants.get("from_blueprint_text", {}).get("constants", {}).get(name)
    return entry.get("value", default) if isinstance(entry, dict) else default


def count_words(text):
    """Words as wc -w counts them in its plain setting: pieces between spaces with a plain keyboard character."""
    return sum(1 for piece in PLAIN_SPACE.split(text) if piece and PLAIN_CHARACTER.search(piece))


def real_words(text):
    """Pieces with a letter or digit (the quote-anchor rule: at least 3 of these, G5)."""
    return [piece for piece in text.split() if LETTER_OR_DIGIT.search(piece)]


def normalise_quote(text):
    """Text as quotes are compared: curly quotes and apostrophes read as straight ones, spaces collapsed."""
    text = (text or "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip()


def number_text(number):
    return f"{number:,}"


PLURAL_WORDS = {"speech": "speeches", "person": "people", "passage": "passages", "match": "matches"}


def counted(count, word):
    """'1 speech', '221 speeches', '1,852 lines': a count with its word in the right form."""
    return f"{number_text(count)} {word if count == 1 else PLURAL_WORDS.get(word, word + 's')}"


def name_for_people(cue_name):
    """'SAYE' becomes 'Saye', 'DR SAYE' becomes 'Dr Saye' (for messages and titles)."""
    words = []
    for word in cue_name.split():
        if word.upper() == word:
            words.append("-".join(part[:1].upper() + part[1:].lower() for part in word.split("-")))
        else:
            words.append(word)
    return " ".join(words)


def clean_title(raw):
    """A clean title from a title line: capitals made plain, a leading number and anything after ' - ' left out."""
    text = (raw or "").strip().strip("*_").strip()
    text = re.sub(r"^\d+\s+", "", text)
    text = text.split(" - ")[0].strip() or text
    if text.upper() == text:
        text = name_for_people(text)
    return text


def fallback_title_from_file_name(path):
    """The title stage.py new uses when it finds no title in the file (its file-name fallback)."""
    stem = Path(path).stem
    stem = re.sub(r"^[0-9a-f]{6,}-\d+_", "", stem)
    return re.sub(r"[_]+", " ", stem).strip() or "Untitled"


def character_identifier(name, taken):
    """CH- and the cue name in capitals and hyphens ('DR SAYE' becomes CH-DR-SAYE)."""
    plain = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    core = re.sub(r"[^A-Z0-9]+", "-", plain.upper()).strip("-")
    if not core:
        core = f"PERSON-{len(taken) + 1:02d}"
    return "CH-" + core


def shorten_for_quote(text, words=10):
    """The first words of a line, exactly as written (a quote that stays story words, with no shortening mark)."""
    pieces = text.strip().split()
    return " ".join(pieces[:words])


def speaking_summary(counts):
    """'Saye speaks 10 times, Iona 4, Jude and Eli once each' from [(name, count)] sorted by count."""
    if not counts:
        return "nobody speaks"
    groups = []
    for name, count in counts:
        if groups and groups[-1][1] == count:
            groups[-1][0].append(name)
        else:
            groups.append(([name], count))

    def names_text(names):
        return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]

    def times(count):
        return {1: "once", 2: "twice"}.get(count, f"{count} times")

    parts = []
    for index, (names, count) in enumerate(groups):
        each = " each" if len(names) > 1 and count <= 2 else ""
        if index == 0:
            verb = "speaks" if len(names) == 1 else "speak"
            parts.append(f"{names_text(names)} {verb} {times(count)}" + (" each" if len(names) > 1 else ""))
        elif count <= 2:
            parts.append(f"{names_text(names)} {times(count)}{each}")
        else:
            parts.append(f"{names_text(names)} {count}" + (" each" if len(names) > 1 else ""))
    return ", ".join(parts)


# ---------------------------------------------------------------- reading files into lines

@dataclass
class ExtractedStory:
    """A story file turned into lines, before its parts are found."""
    lines: list
    file_name: str = ""
    suffix: str = ""
    file_kind: str = "text"                 # text, fdx, docx, epub, pdf
    extraction: str = "native_text"         # D14's extraction_method
    hints: list = None                      # per line: what the file says it is, or None
    title: str = None                       # a title the file's own data gives (Final Draft title page, EPUB title)
    notes: list = dataclass_field(default_factory=list)   # (line number or None, plain finding) for the report
    first_line_number: int = 1
    first_scene_number: int = 1
    header: dict = None


def decode_text(data):
    """Text from bytes: UTF-8 (with or without a byte-order mark), UTF-16, else Windows text, noting the guess."""
    if data.startswith(codecs.BOM_UTF16_LE) or data.startswith(codecs.BOM_UTF16_BE):
        return data.decode("utf-16"), None
    try:
        return data.decode("utf-8-sig"), None
    except UnicodeDecodeError:
        pass
    note = ("The file was not saved as UTF-8 text, so it was read as Windows text; check that accented letters "
            "look right in the numbered story.")
    try:
        return data.decode("cp1252"), note
    except UnicodeDecodeError:
        return data.decode("latin-1"), note


def normalise_text_lines(text):
    """Lines of a text as D14 R9 stores them: NFC, LF line ends, no byte-order mark, no trailing spaces."""
    text = unicodedata.normalize("NFC", text.lstrip("﻿"))
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return [re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", line).rstrip() for line in lines]


def split_excerpt_header(lines):
    """A test fixture may start with a STAGE EXCERPT HEADER block (WP12a): its keys and the story lines after it."""
    if not lines or lines[0].strip() != EXCERPT_START:
        return None, lines
    header = {}
    for index in range(1, len(lines)):
        if lines[index].strip() == EXCERPT_END:
            return header, lines[index + 1:]
        if ":" in lines[index]:
            key, value = lines[index].split(":", 1)
            header[key.strip()] = value.strip()
    return None, lines


def load_story_file(path):
    """Read a story file into an ExtractedStory, or stop with one plain line (exit 2) when it cannot be read."""
    path = Path(path)
    if not path.is_file():
        raise StageStop(f'The story file "{path.name}" was not found.')
    data = path.read_bytes()
    suffix = path.suffix.lower()
    if not data.strip():
        raise StageStop(f'The story file "{path.name}" is empty. Give me the file with the story in it.')
    if data[:4] == b"PK\x03\x04":
        return read_zip_story(path, data)
    if data[:5] == b"%PDF-":
        return read_pdf_story(path)
    if data[:4] == b"\xd0\xcf\x11\xe0" or suffix in (".doc", ".rtf", ".pages", ".wpd", ".odt"):
        raise StageStop(f'"{path.name}" is in a word-processor format these tools cannot read. Save it as a Word file '
                        '(.docx) or as plain text (.txt) and give me that file.')
    text, note = decode_text(data)
    if suffix == ".fdx" or "<FinalDraft" in text[:4000]:
        return read_fdx_story(path, data)
    lines = normalise_text_lines(text)
    header, lines = split_excerpt_header(lines)
    story = ExtractedStory(lines=lines, file_name=path.name, suffix=suffix)
    if header:
        story.header = header
        story.first_line_number = int(header.get("first_line_number", 1))
        story.first_scene_number = int(header.get("first_scene_number", 1))
    if note:
        story.notes.append((None, note))
    return story


def read_zip_story(path, data):
    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile:
        raise StageStop(f'"{path.name}" looks like a ZIP file but cannot be opened. Save the story again and give me '
                        'the new file.')
    with archive:
        names = set(archive.namelist())
        mimetype = archive.read("mimetype").decode("ascii", "ignore").strip() if "mimetype" in names else ""
        if "word/document.xml" in names:
            return read_docx_story(path, archive, names)
        if mimetype == "application/epub+zip" or "META-INF/container.xml" in names:
            return read_epub_story(path, archive, names)
        if "opendocument" in mimetype:
            raise StageStop(f'"{path.name}" is an OpenDocument text file. Save it as a Word file (.docx) or as plain '
                            'text (.txt) and give me that file.')
    raise StageStop(f'"{path.name}" is a ZIP file, not a story file. Give me the story itself: text, Fountain, '
                    'Final Draft, Word or EPUB.')


# -- Final Draft (.fdx)

FDX_TYPES = {"scene heading": "heading", "action": "action", "general": "action", "shot": "action",
             "cast list": "action", "character": "cue", "parenthetical": "parenthetical", "dialogue": "dialogue",
             "transition": "transition", "new act": "section", "end of act": "section", "outline": "note",
             "outline body": "note", "lyrics": "lyric"}


def fdx_paragraphs(element):
    """The Paragraph elements of an FDX Content element in order, looking inside dual dialogue."""
    for paragraph in element.findall("Paragraph"):
        dual = paragraph.find("DualDialogue")
        if dual is not None:
            yield from fdx_paragraphs(dual)
            continue
        yield paragraph


def fdx_text(paragraph):
    return "".join("".join(text.itertext()) for text in paragraph.findall("Text")).replace("\t", " ")


def read_fdx_story(path, data):
    try:
        root = ElementTree.fromstring(data)
    except ElementTree.ParseError:
        raise StageStop(f'The Final Draft file "{path.name}" could not be read (it is not complete). Export it again, '
                        'or save it as Fountain or plain text.')
    lines, hints = [], []
    title = None
    title_page = root.find("TitlePage")
    if title_page is not None and title_page.find("Content") is not None:
        for paragraph in fdx_paragraphs(title_page.find("Content")):
            text = fdx_text(paragraph).strip()
            if not text:
                continue
            title = title or text
            lines += [text, ""]
            hints += ["title", None]
    content = root.find("Content")
    if content is None:
        raise StageStop(f'The Final Draft file "{path.name}" has no script in it.')
    previous = None
    for paragraph in fdx_paragraphs(content):
        kind = FDX_TYPES.get((paragraph.get("Type") or "Action").strip().lower(), "action")
        if kind == "action" and (paragraph.get("Alignment") or "").lower() == "center":
            kind = "card"
        text = fdx_text(paragraph).strip()
        if not text:
            continue
        joined_to_speech = kind in ("parenthetical", "dialogue", "lyric") and previous in ("cue", "parenthetical",
                                                                                            "dialogue", "lyric")
        if lines and not joined_to_speech and lines[-1] != "":
            lines.append("")
            hints.append(None)
        for piece in text.split("\n"):
            lines.append(piece.strip())
            hints.append(kind)
        previous = kind
    story = ExtractedStory(lines=[unicodedata.normalize("NFC", line) for line in lines], file_name=path.name,
                           suffix=path.suffix.lower(), file_kind="fdx", extraction="app_export", hints=hints,
                           title=title)
    return story


# -- Word (.docx)

W_NAMESPACE = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
DOCX_STYLE_HINTS = {"title": "title", "sceneheading": "heading", "slugline": "heading", "character": "cue",
                    "dialogue": "dialogue", "parenthetical": "parenthetical", "transition": "transition",
                    "action": "action", "general": "action", "shot": "action"}


def read_docx_story(path, archive, names):
    try:
        root = ElementTree.fromstring(archive.read("word/document.xml"))
    except ElementTree.ParseError:
        raise StageStop(f'The Word file "{path.name}" could not be read. Save it again, or save it as plain text.')
    style_names = {}
    if "word/styles.xml" in names:
        for style in ElementTree.fromstring(archive.read("word/styles.xml")).iter(W_NAMESPACE + "style"):
            name = style.find(W_NAMESPACE + "name")
            style_names[style.get(W_NAMESPACE + "styleId")] = name.get(W_NAMESPACE + "val") if name is not None else ""
    counts = {"insertions": 0, "deletions": 0}

    def walk(element, pieces):
        for child in element:
            tag = child.tag
            if tag in (W_NAMESPACE + "del", W_NAMESPACE + "moveFrom"):
                counts["deletions"] += 1
                continue
            if tag in (W_NAMESPACE + "ins", W_NAMESPACE + "moveTo"):
                counts["insertions"] += 1
                walk(child, pieces)
            elif tag == W_NAMESPACE + "t":
                pieces[-1] += child.text or ""
            elif tag == W_NAMESPACE + "tab":
                pieces[-1] += " "
            elif tag in (W_NAMESPACE + "br", W_NAMESPACE + "cr"):
                pieces.append("")
            elif tag in (W_NAMESPACE + "pPr", W_NAMESPACE + "delText", W_NAMESPACE + "instrText"):
                continue
            elif tag.endswith("}Fallback"):
                continue
            else:
                walk(child, pieces)

    paragraphs = []
    body = root.find(W_NAMESPACE + "body")
    for paragraph in (body.iter(W_NAMESPACE + "p") if body is not None else []):
        style_id = None
        properties = paragraph.find(W_NAMESPACE + "pPr")
        if properties is not None and properties.find(W_NAMESPACE + "pStyle") is not None:
            style_id = properties.find(W_NAMESPACE + "pStyle").get(W_NAMESPACE + "val")
        style = re.sub(r"[\s_-]+", "", (style_names.get(style_id) or style_id or "")).lower()
        pieces = [""]
        walk(paragraph, pieces)
        pieces = [unicodedata.normalize("NFC", piece).strip() for piece in pieces]
        if not any(pieces):
            continue
        hint = DOCX_STYLE_HINTS.get(style)
        if hint is None and re.fullmatch(r"heading\d", style):
            hint = "heading_prose"
        paragraphs.append((hint, [piece for piece in pieces if piece]))
    screenplay = any(hint in ("heading", "cue") for hint, _ in paragraphs)
    lines, hints = [], []
    previous = None
    title = None
    for hint, pieces in paragraphs:
        if hint == "title":
            title = title or " ".join(pieces)
        if not screenplay and hint not in ("heading_prose", "title"):
            hint = None
        if screenplay and hint in (None, "heading_prose"):
            hint = "action"
        if screenplay and hint == "title":
            hint = "title"
        joined = screenplay and hint in ("parenthetical", "dialogue") and previous in ("cue", "parenthetical", "dialogue")
        if lines and not joined:
            lines.append("")
            hints.append(None)
        for piece in pieces:
            lines.append(piece)
            hints.append("heading" if hint in ("heading_prose",) or (hint == "title" and not screenplay) else hint)
        previous = hint
    if title is None and "docProps/core.xml" in names:
        core = ElementTree.fromstring(archive.read("docProps/core.xml"))
        for element in core.iter():
            if element.tag.endswith("}title") and (element.text or "").strip():
                title = element.text.strip()
                break
    story = ExtractedStory(lines=lines, file_name=path.name, suffix=path.suffix.lower(), file_kind="docx",
                           extraction="native_text", hints=hints, title=title)
    if counts["insertions"] or counts["deletions"]:
        story.notes.append((None, f"The Word file holds tracked changes ({counted(counts['insertions'], 'insertion')} and "
                                  f"{counted(counts['deletions'], 'deletion')}). It was read with every change accepted; "
                                  "say if the story is the version before the changes."))
    if "word/comments.xml" in names:
        comments = len(ElementTree.fromstring(archive.read("word/comments.xml")).findall(W_NAMESPACE + "comment"))
        if comments:
            story.notes.append((None, f"The Word file holds {counted(comments, 'comment')}; comments are not part of the "
                                      "story and were left out."))
    return story


# -- EPUB

class BlockTextParser(html.parser.HTMLParser):
    """The text blocks of an XHTML page: headings and paragraphs, each a list of lines, in order."""
    BLOCKS = {"p", "div", "li", "blockquote", "pre", "section", "article", "tr", "dd", "dt", "figcaption", "td"}
    HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
    SKIP = {"head", "script", "style", "title", "nav"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = []
        self.pieces = [""]
        self.kind = None
        self.skip_depth = 0

    def flush(self):
        pieces = [re.sub(r"\s+", " ", piece).strip() for piece in self.pieces]
        pieces = [piece for piece in pieces if piece]
        if pieces:
            self.blocks.append((self.kind, pieces))
        self.pieces = [""]
        self.kind = None

    def handle_starttag(self, tag, attributes):
        if tag in self.SKIP:
            self.skip_depth += 1
            return
        if tag in self.HEADINGS or tag in self.BLOCKS:
            self.flush()
            self.kind = "heading" if tag in self.HEADINGS else None
        elif tag == "br":
            self.pieces.append("")

    def handle_startendtag(self, tag, attributes):
        if tag == "br":
            self.pieces.append("")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if tag in self.HEADINGS or tag in self.BLOCKS:
            self.flush()

    def handle_data(self, data):
        if not self.skip_depth:
            self.pieces[-1] += data


def read_epub_story(path, archive, names):
    if "META-INF/rights.xml" in names:
        raise StageStop(copy_protected_message(path))
    if "META-INF/encryption.xml" in names:
        encryption = ElementTree.fromstring(archive.read("META-INF/encryption.xml"))
        for element in encryption.iter():
            if element.tag.endswith("EncryptionMethod"):
                algorithm = element.get("Algorithm") or ""
                if algorithm not in ("http://www.idpf.org/2008/embedding", "http://ns.adobe.com/pdf/enc#RC"):
                    raise StageStop(copy_protected_message(path))
    try:
        container = ElementTree.fromstring(archive.read("META-INF/container.xml"))
        rootfile = next(element.get("full-path") for element in container.iter() if element.tag.endswith("rootfile"))
        package = ElementTree.fromstring(archive.read(rootfile))
    except (KeyError, StopIteration, ElementTree.ParseError):
        raise StageStop(f'The e-book "{path.name}" could not be read (its table of contents is missing or broken).')
    base = rootfile.rsplit("/", 1)[0] + "/" if "/" in rootfile else ""
    manifest = {}
    title = None
    spine = []
    for element in package.iter():
        tag = element.tag.split("}")[-1]
        if tag == "item":
            manifest[element.get("id")] = (element.get("href"), element.get("media-type") or "",
                                           element.get("properties") or "")
        elif tag == "itemref":
            spine.append(element.get("idref"))
        elif tag == "title" and title is None and (element.text or "").strip():
            title = element.text.strip()
    lines, hints = [], []
    for identifier in spine:
        href, media_type, properties = manifest.get(identifier, (None, "", ""))
        if not href or "nav" in properties.split() or "html" not in media_type:
            continue
        document = base + href.split("#")[0]
        try:
            text = archive.read(document).decode("utf-8", "replace")
        except KeyError:
            continue
        parser = BlockTextParser()
        parser.feed(text)
        parser.flush()
        for kind, pieces in parser.blocks:
            if lines:
                lines.append("")
                hints.append(None)
            for piece in pieces:
                lines.append(unicodedata.normalize("NFC", piece))
                hints.append("heading" if kind == "heading" else None)
    if not lines:
        raise StageStop(f'The e-book "{path.name}" holds no text these tools can read.')
    return ExtractedStory(lines=lines, file_name=path.name, suffix=path.suffix.lower(), file_kind="epub",
                          extraction="native_text", hints=hints, title=title)


def copy_protected_message(path):
    return (f'The e-book "{path.name}" is copy-protected, so the tools cannot read it. Use a copy without protection '
            'that you have the right to adapt, or save the text as a plain text file.')


# -- PDF

PDF_FIX = ("This copy of the tools cannot read PDF files here. Open the PDF in Google Docs, choose File, Download, "
           "Plain text, and give me that file.")
SCANNED_FIX = ("This PDF is a scan: it has no text layer to read. Open it in Google Docs, choose File, Download, "
               "Plain text, and give me that file.")


def read_pdf_story(path):
    text = None
    extraction = "layout_text"
    converter = shutil.which("pdftotext")
    if converter:
        try:
            result = subprocess.run([converter, "-layout", "-enc", "UTF-8", str(path), "-"], capture_output=True,
                                    timeout=300)
            if result.returncode == 0:
                text = result.stdout.decode("utf-8", "replace")
        except (OSError, subprocess.TimeoutExpired):
            text = None
    if text is None:
        try:
            import pypdf  # optional: only used when it is installed
            reader = pypdf.PdfReader(str(path))
            pages = []
            for page in reader.pages:
                try:
                    pages.append(page.extract_text(extraction_mode="layout") or "")
                except TypeError:
                    pages.append(page.extract_text() or "")
            text = "\f".join(pages)
        except ImportError:
            raise StageStop(PDF_FIX)
        except Exception:
            raise StageStop(PDF_FIX)
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    printable = [len(re.sub(r"\s", "", page)) for page in pages] or [0]
    if sum(printable) / max(1, len(printable)) < SCANNED_PAGE_CHARACTERS:
        raise StageStop(SCANNED_FIX)
    lines = normalise_text_lines("\n".join(pages))
    story = ExtractedStory(lines=lines, file_name=path.name, suffix=".pdf", file_kind="pdf", extraction=extraction)
    story.notes.append((None, f"This story came from a PDF of {counted(len(pages), 'page')}. Compare its first, middle and "
                              "last pages with the numbered story before going on; a PDF can lose or reorder words "
                              "without any warning."))
    return story


# ---------------------------------------------------------------- the kind of story and what each line is

def looks_like_cue(text):
    """A Fountain character cue: a name in capitals (extensions and a dual-dialogue mark allowed)."""
    name = text.strip()
    if name.endswith("^"):
        name = name[:-1].strip()
    while EXTENSION.search(name):
        name = EXTENSION.sub("", name).strip()
    if not name or not re.search(r"[^\W\d_]", name) or name != name.upper():
        return False
    if len(name) > 40 or name.endswith((".", ":", "!", "?", ",", ";")) or name.startswith(("(", "[")):
        return False
    if is_transition_text(name) or SCREENPLAY_HEADING.match(name):
        return False
    return True


def is_transition_text(text):
    stripped = text.strip()
    if stripped != stripped.upper() or not re.search(r"[A-Z]", stripped):
        return False
    return stripped.endswith("TO:") or stripped in PLAIN_TRANSITION_LINES


def transition_value(text):
    """The schema word for a transition line ('> CUT TO BLACK.' is cut_to_black), and whether the list knows it."""
    words = re.sub(r"^[>\s]+", "", text).strip().rstrip(":.").strip().upper()
    for pattern, value in TRANSITION_WORDS:
        if pattern.match(words):
            return value, True
    return "cut", False


def detect_kind(story):
    """(source_kind, dialect): the kind of story from its content, never from its file name (D14 principle 1)."""
    lines = story.lines
    hints = story.hints or []
    if any(CATCH_HEADING.match(line) for line in lines):
        return "screenplay", "catch"
    if any(hint in ("heading", "cue") for hint in hints) and story.file_kind in ("fdx", "docx") and \
            any(hint == "cue" for hint in hints):
        return "screenplay", "hinted"
    if story.file_kind == "fdx":
        return ("screenplay" if any(hint == "cue" for hint in hints) else "treatment"), "hinted"
    stripped = [line.strip() for line in lines]
    if sum(1 for line in stripped if any(marker.match(line) for marker in GAME_MARKERS)) >= 2 and \
            (any(line.startswith("->") or line.startswith("::") for line in stripped)
             or any(line.lower().startswith("title:") for line in stripped) and "===" in stripped):
        return "game_script", "game"
    headings = cues = 0
    for index, line in enumerate(stripped):
        before_blank = index == 0 or not stripped[index - 1]
        after_filled = index + 1 < len(stripped) and stripped[index + 1]
        if before_blank and (SCREENPLAY_HEADING.match(line) or (line.startswith(".") and len(line) > 1
                                                                 and not line.startswith(".."))):
            headings += 1
        elif (line.startswith("@") or (before_blank and after_filled and looks_like_cue(line))) and after_filled:
            cues += 1
    pages = sum(1 for line in stripped if COMIC_PAGE.match(line))
    panels = sum(1 for line in stripped if COMIC_PANEL.match(line))
    if pages and panels and not headings:
        return "comic_script", "comic"
    stage_headings = sum(1 for line in stripped if STAGE_HEADING.match(line) or ACT_HEADING.match(line))
    inline_cues = sum(1 for line in stripped if INLINE_CUE.match(line))
    if stage_headings and inline_cues >= 2 and not headings:
        return "stage_play", "stage"
    if headings and cues:
        return "screenplay", "fountain"
    if headings:
        return "treatment", "fountain"
    return "prose", "prose"


def source_format_for(story, kind, dialect):
    if dialect == "catch":
        return "catch_dialect"
    if story.file_kind in ("fdx", "docx", "epub"):
        return story.file_kind
    if story.file_kind == "pdf":
        return "pdf_text"
    if dialect == "fountain":
        fountain_marks = any(line.startswith(("[[", "/*", "@", "~", ".", "!")) or (line.startswith(">") and line.endswith("<"))
                             or re.fullmatch(r"={3,}", line.strip() or "x") for line in story.lines)
        first = next((line for line in story.lines if line.strip()), "")
        if story.suffix in (".fountain", ".spmd") or TITLE_KEY.match(first) or fountain_marks:
            return "fountain"
        return "plain_text"
    if story.suffix in (".md", ".markdown", ".mdown") or any(line.startswith("# ") for line in story.lines):
        return "markdown"
    return "plain_text"


def classify_catch(lines):
    """The Catch's layout (A3 §4.3 step 1): '## ' headings, '@' cues, '> ' transitions, '= ' title lines."""
    types = []
    in_speech = False
    seen_heading = False
    for line in lines:
        text = line.strip()
        if not text:
            types.append(BLANK)
            in_speech = False
        elif text.startswith("##"):
            types.append(HEADING)
            seen_heading = True
            in_speech = False
        elif text.startswith("@"):
            types.append(CUE)
            in_speech = True
        elif in_speech:
            types.append(PARENTHETICAL if PAREN_LINE.match(text) else DIALOGUE)
        elif text.startswith(">"):
            types.append(TRANSITION)
        elif text.startswith("="):
            types.append(CARD if seen_heading else TITLE)
        else:
            types.append(ACTION)
    return types


HINT_TYPES = {"heading": HEADING, "cue": CUE, "dialogue": DIALOGUE, "parenthetical": PARENTHETICAL,
              "transition": TRANSITION, "action": ACTION, "title": TITLE, "section": SECTION, "note": NOTE,
              "lyric": LYRIC, "card": CARD}


def classify_hinted(lines, hints):
    types = []
    for line, hint in zip(lines, hints):
        if not line.strip():
            types.append(BLANK)
        else:
            types.append(HINT_TYPES.get(hint, ACTION))
    return types


def classify_fountain(lines):
    """Fountain and plain screenplay text (A3 §4.1-4.2): headings, cues, speeches, transitions and the rest."""
    count = len(lines)
    stripped = [line.strip() for line in lines]
    types = [None] * count

    def blank(index):
        return index < 0 or index >= count or not stripped[index]

    index = 0
    while index < count:
        if stripped[index].startswith("/*"):
            while index < count:
                types[index] = BONEYARD if stripped[index] else BLANK
                if "*/" in stripped[index]:
                    break
                index += 1
        index += 1
    first = next((index for index in range(count) if stripped[index]), None)
    if first is not None and TITLE_KEY.match(stripped[first]):
        index = first
        while index < count and stripped[index]:
            types[index] = TITLE
            index += 1
    in_speech = False
    for index in range(count):
        text = stripped[index]
        if types[index] is not None:
            in_speech = False
            continue
        if not text:
            types[index] = BLANK
            in_speech = False
        elif in_speech:
            if PAREN_LINE.match(text):
                types[index] = PARENTHETICAL
            elif text.startswith("~"):
                types[index] = LYRIC
            else:
                types[index] = DIALOGUE
        elif text.startswith("[[") and text.endswith("]]"):
            types[index] = NOTE
        elif re.fullmatch(r"={3,}", text):
            types[index] = PAGE_BREAK
        elif text.startswith("#"):
            types[index] = SECTION
        elif text.startswith("="):
            types[index] = SYNOPSIS
        elif text.startswith(">") and text.endswith("<"):
            types[index] = CARD
        elif text.startswith(">"):
            types[index] = TRANSITION
        elif text.startswith("!"):
            types[index] = ACTION
        elif text.startswith("~"):
            types[index] = LYRIC
        elif blank(index - 1) and ((text.startswith(".") and len(text) > 1 and not text.startswith(".."))
                                   or SCREENPLAY_HEADING.match(text)):
            types[index] = HEADING
        elif text.startswith("@") and not blank(index + 1):
            types[index] = CUE
            in_speech = True
        elif blank(index - 1) and is_transition_text(text) and blank(index + 1):
            types[index] = TRANSITION
        elif blank(index - 1) and not blank(index + 1) and looks_like_cue(text):
            types[index] = CUE
            in_speech = True
        else:
            types[index] = ACTION
    return types


def classify_stage_play(lines):
    """A stage play: SCENE headings split scenes, ACT lines are breaks, 'NAME. words' lines are cues with speech."""
    types = []
    in_speech = False
    for line in lines:
        text = line.strip()
        if not text:
            types.append(BLANK)
            in_speech = False
        elif STAGE_HEADING.match(text):
            types.append(HEADING)
            in_speech = False
        elif ACT_HEADING.match(text):
            types.append(SECTION)
            in_speech = False
        elif INLINE_CUE.match(text) and not text.startswith(("(", "[")):
            types.append(CUE_WITH_SPEECH)
            in_speech = True
        elif in_speech and not text.startswith(("(", "[")):
            types.append(DIALOGUE)
        else:
            types.append(ACTION)
            in_speech = False
    return types


def classify_comic(lines):
    """A comic script: PAGE lines split scenes, PANEL lines are breaks, 'NAME: words' balloons are cues with speech."""
    types = []
    for line in lines:
        text = line.strip()
        if not text:
            types.append(BLANK)
        elif COMIC_PAGE.match(text):
            types.append(HEADING)
        elif COMIC_PANEL.match(text):
            types.append(SECTION)
        elif re.match(r"^(CAPTION|SFX|SOUND)\b", text, re.IGNORECASE):
            types.append(ACTION)
        elif INLINE_CUE.match(re.sub(r"^\d+\.?\s*", "", text)) and ":" in text:
            types.append(CUE_WITH_SPEECH)
        else:
            types.append(ACTION)
    return types


def heading_text_of(line, dialect):
    """The heading as the story writes it, without the layout marks ('## ', a forcing '.', Fountain's #12#)."""
    text = line.strip()
    if dialect == "catch" and text.startswith("##"):
        text = text[2:].strip()
    elif text.startswith(".") and not text.startswith(".."):
        text = text[1:].strip()
    return FOUNTAIN_SCENE_NUMBER.sub("", text).strip()


def split_heading(heading):
    """(int_ext, place_text, time_text, presentation note or None) of a scene heading (A3 §4.3 step 3)."""
    text = LEADING_SCENE_NUMBER.sub("", heading.strip())
    match = HEADING_PREFIX.match(text)
    int_ext = "int"
    if match:
        prefix = match.group(1).upper().replace(" ", "")
        if "/" in prefix:
            int_ext = "int_ext"
        elif prefix.startswith("EXT") or prefix.startswith("EST"):
            int_ext = "ext"
        text = text[match.end():].strip()
    note = None
    trailing = re.search(r"\s*\(([^()]*)\)\s*$", text)
    if trailing:
        before = text[:trailing.start()].strip()
        inside = trailing.group(1).strip()
        last_part = before.rsplit(" - ", 1)[-1] if " - " in before else ""
        if any(pattern.search(inside.upper()) for pattern, _ in PRESENTATION_WORDS) or \
                (last_part and TIME_WORDS.search(last_part.upper())):
            note = inside
            text = before
    if " - " in text:
        place, time = text.rsplit(" - ", 1)
        if not TIME_WORDS.search(time.upper()) and len(time.split()) > 3:
            place, time = text, "none"
    else:
        place, time = text, "none"
    return int_ext, place.strip() or "none", time.strip() or "none", note


def presentation_for(note):
    if not note:
        return "normal"
    upper = note.upper()
    for pattern, value in PRESENTATION_WORDS:
        if pattern.search(upper):
            return value
    return "normal"


def scene_number_of(heading_line, dialect):
    """A scene number the source already carries (Fountain #12#, or '12 INT.'), or None (A3 §4.3 step 2)."""
    text = heading_line.strip()
    if dialect == "catch" and text.startswith("##"):
        text = text[2:].strip()
    fountain = FOUNTAIN_SCENE_NUMBER.search(text)
    if fountain and re.fullmatch(r"\d+[A-Z]?", fountain.group(1)):
        return fountain.group(1)
    leading = LEADING_SCENE_NUMBER.match(text)
    if leading:
        return leading.group(1)
    return None


# ---------------------------------------------------------------- the parts of a story

@dataclass
class OddLine:
    """One entry of the odd-lines report: where, the story's words, and what code made of them."""
    first: int
    last: int
    text: str
    finding: str
    kind: str


@dataclass
class Speech:
    identifier: str
    scene: str
    speaker: str
    cue_name: str
    cue_line: int
    first: int
    last: int
    text: str
    text_lines: list
    parentheticals: list
    extension: str
    path: str
    path_reason: str
    word_count: int
    beat_marks: int
    spoken_characters: int

    def to_json(self):
        return {"id": self.identifier, "scene": self.scene, "speaker": self.speaker, "cue": self.cue_name,
                "line": self.cue_line, "lines": [self.first, self.last], "text_lines": self.text_lines,
                "text": self.text,
                "parenthetical": "; ".join(text for _, text in self.parentheticals) if self.parentheticals else "none",
                "parentheticals": [{"line": line, "text": text} for line, text in self.parentheticals],
                "extension": self.extension or "none", "path": self.path, "path_from": self.path_reason,
                "origin": "story", "word_count": self.word_count, "beat_marks": self.beat_marks,
                "spoken_characters": self.spoken_characters}


@dataclass
class Character:
    identifier: str
    cue_name: str
    names: list
    cues: int = 0
    first_line: int = None
    alias_lines: dict = dataclass_field(default_factory=dict)


@dataclass
class Scene:
    identifier: str
    heading: str
    heading_line: int
    first: int
    last: int
    int_ext: str
    place_text: str
    time_text: str
    presentation_note: str = None
    presentation: str = "normal"
    transition_in: str = "cut"
    transition_in_line: int = None
    transition_out: str = "cut"
    transition_out_line: int = None
    speeches: list = dataclass_field(default_factory=list)
    characters: list = dataclass_field(default_factory=list)
    speaking: list = dataclass_field(default_factory=list)
    cards: list = dataclass_field(default_factory=list)
    instructions: list = dataclass_field(default_factory=list)
    tokens: list = dataclass_field(default_factory=list)
    light_lines: list = dataclass_field(default_factory=list)
    counts: dict = dataclass_field(default_factory=dict)
    notes: list = dataclass_field(default_factory=list)
    title: str = ""


@dataclass
class Chapter:
    identifier: str
    title: str
    heading_line: int
    first: int
    last: int
    words: int


@dataclass
class StoryReading:
    """Everything read_story_lines found in one story."""
    lines: list
    types: list
    first_line_number: int
    file_name: str
    source_kind: str
    source_format: str
    dialect: str
    extraction: str
    language: str
    title: str = None
    title_line: int = None
    scenes: list = dataclass_field(default_factory=list)
    speeches: list = dataclass_field(default_factory=list)
    characters: list = dataclass_field(default_factory=list)
    chapters: list = dataclass_field(default_factory=list)
    people_without_speeches: list = dataclass_field(default_factory=list)
    odd_lines: list = dataclass_field(default_factory=list)
    extraction_notes: list = dataclass_field(default_factory=list)
    counts: dict = dataclass_field(default_factory=dict)
    first_estimate: dict = None
    repeats: list = dataclass_field(default_factory=list)
    verse: list = dataclass_field(default_factory=list)
    set_off_blocks: list = dataclass_field(default_factory=list)
    name_candidates: list = dataclass_field(default_factory=list)
    scene_id_digits: int = 2
    header: dict = None

    @property
    def last_line_number(self):
        return self.first_line_number + len(self.lines) - 1

    def line(self, number):
        index = number - self.first_line_number
        return self.lines[index] if 0 <= index < len(self.lines) else ""

    def type_of(self, number):
        index = number - self.first_line_number
        return self.types[index] if 0 <= index < len(self.types) else None

    @property
    def words(self):
        return count_words("\n".join(self.lines))


# ---------------------------------------------------------------- reading a story's parts

def detect_language(lines):
    """The story's language from its commonest small words, or 'unknown'."""
    tokens = [token.lower().strip(".,;:!?\"'()*_") for line in lines for token in line.split()][:20000]
    if not tokens:
        return "unknown"
    scores = {language: sum(1 for token in tokens if token in words) for language, words in STOPWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] * 20 >= len(tokens) else "unknown"


def join_hard_wrapped_prose(story):
    """Prose is numbered one paragraph per line: a hard-wrapped text (most lines continue the line before) is
    joined, and the original line numbers are kept in a note. Returns True when it joined anything."""
    lines = story.lines
    filled = [index for index, line in enumerate(lines) if line.strip()]
    if len(filled) < 4:
        return False
    continuing = sum(1 for index in filled if index > 0 and lines[index - 1].strip()
                     and not lines[index].lstrip().startswith(("#", ">", "-", "*", "|")))
    if continuing * 2 <= len(filled):
        return False
    joined = []
    for line in lines:
        if line.strip() and joined and joined[-1].strip() and not line.lstrip().startswith(("#", ">", "|")) \
                and not joined[-1].lstrip().startswith("#"):
            joined[-1] = joined[-1].rstrip() + " " + line.strip()
        else:
            joined.append(line)
    story.notes.append((None, f"The prose was broken into short lines ({number_text(len(lines))} lines); it is "
                              f"numbered one paragraph per line ({number_text(len(joined))} lines)."))
    story.lines = joined
    story.hints = None
    return True


def read_story_lines(story, constants=None):
    """Find the parts of an extracted story. Returns a StoryReading."""
    kind, dialect = detect_kind(story)
    if kind == "prose" and story.file_kind == "text":
        join_hard_wrapped_prose(story)
    source_format = source_format_for(story, kind, dialect)
    reading = StoryReading(lines=list(story.lines), types=[], first_line_number=story.first_line_number,
                           file_name=story.file_name, source_kind=kind, source_format=source_format, dialect=dialect,
                           extraction=story.extraction, language=detect_language(story.lines), header=story.header)
    reading.extraction_notes = list(story.notes)
    if kind in ("screenplay", "treatment", "stage_play", "comic_script"):
        if dialect == "catch":
            reading.types = classify_catch(story.lines)
        elif dialect == "hinted":
            reading.types = classify_hinted(story.lines, story.hints)
        elif dialect == "stage":
            reading.types = classify_stage_play(story.lines)
        elif dialect == "comic":
            reading.types = classify_comic(story.lines)
        else:
            reading.types = classify_fountain(story.lines)
        read_screenplay(reading, story, constants)
    elif kind == "game_script":
        reading.types = [BLANK if not line.strip() else PARAGRAPH for line in story.lines]
        reading.odd_lines.append(OddLine(reading.first_line_number, reading.last_line_number, "",
                                         "This is a game script with branches. A film follows one path, so the user "
                                         "picks the path first; the scenes are then written from it.", "game_script"))
    else:
        read_prose(reading, story, constants)
    reading.odd_lines.sort(key=lambda odd: (odd.first, odd.last))
    for line_number, note in reversed(story.notes):
        reading.odd_lines.insert(0, OddLine(line_number or reading.first_line_number, line_number
                                            or reading.first_line_number, "", note, "file"))
    reading.first_estimate = first_estimate(reading, constants)
    return reading


# -- screenplays

def read_screenplay(reading, story, constants):
    types = reading.types
    lines = reading.lines
    first_number = reading.first_line_number
    heading_indexes = [index for index, kind in enumerate(types) if kind == HEADING]
    dialect = reading.dialect

    # Placement rules for lines before the first heading (step 1): title-page lines, the join into scene 1,
    # and anything else (front matter, listed as odd).
    end_of_front = heading_indexes[0] if heading_indexes else len(lines)
    title_indexes = [index for index in range(end_of_front) if types[index] == TITLE]
    title_text = None
    for index in title_indexes:
        text = lines[index].strip()
        value = text[1:].strip() if text.startswith("=") else text
        key = TITLE_KEY.match(value)
        if key:
            if key.group(1).lower() != "title":
                continue
            value = value[key.end():].strip()
            if not value:
                follow = index + 1
                while follow < end_of_front and types[follow] == TITLE and not TITLE_KEY.match(lines[follow].strip()):
                    if lines[follow].strip():
                        value = lines[follow].strip()
                        break
                    follow += 1
        value = re.sub(r"[_*]+", "", value).strip()
        if value:
            title_text = value
            reading.title_line = first_number + index
            break
    if title_text is None and story.title:
        title_text = story.title
    reading.title = title_text
    if title_indexes:
        first, last = first_number + title_indexes[0], first_number + title_indexes[-1]
        reading.odd_lines.append(OddLine(first, last, lines[title_indexes[0]].strip(),
                                         "the title page, outside every scene"
                                         + (f'; its first line gives the title, "{title_text}"' if title_text else ""),
                                         "title_page"))
    pending_in = None
    for index in range(end_of_front):
        kind = types[index]
        number = first_number + index
        text = lines[index].strip()
        if kind == TRANSITION:
            value, known = transition_value(text)
            pending_in = (value, number)
            reading.odd_lines.append(OddLine(number, number, text, f"the join into the first scene ({value.replace('_', ' ')})",
                                             "transition_in"))
        elif kind in (CARD,):
            reading.odd_lines.append(OddLine(number, number, text, "a card before the first scene: it belongs to the "
                                             "title page", "title_page"))
        elif kind == SECTION:
            reading.odd_lines.append(OddLine(number, number, text, "a break the story marks before the first scene "
                                             "(an act or a part): kept as a break, not a scene", "section"))
        elif kind in (ACTION, CUE, DIALOGUE, PARENTHETICAL, SYNOPSIS, NOTE, BONEYARD, LYRIC, CUE_WITH_SPEECH):
            reading.odd_lines.append(OddLine(number, number, text, "before the first scene heading and not a title "
                                             "line: front matter, outside every scene", "front_matter"))

    # Scene numbers: the source's own when every heading carries one (A3 §4.3 step 2), else counted in order.
    carried = [scene_number_of(lines[index], dialect) for index in heading_indexes]
    use_carried = heading_indexes and all(carried) and len(set(carried)) == len(carried)
    base = int((reading.header or {}).get("first_scene_number", 1))
    numbers = [carried[position] if use_carried else str(base + position) for position in range(len(heading_indexes))]
    widest = max([int(re.match(r"\d+", number).group(0)) for number in numbers] or [0])
    digits_above = constant(constants, "scene_ids_three_digits_above", 99)
    reading.scene_id_digits = 3 if (len(numbers) > digits_above or widest > digits_above) else 2

    cue_names = collect_cue_names(reading)
    characters = {}
    for position, index in enumerate(heading_indexes):
        last_index = (heading_indexes[position + 1] - 1) if position + 1 < len(heading_indexes) else len(lines) - 1
        match = re.match(r"(\d+)([A-Z]?)", numbers[position])
        identifier = f"SC{int(match.group(1)):0{reading.scene_id_digits}d}{match.group(2)}"
        heading = heading_text_of(lines[index], dialect)
        int_ext, place, time, note = split_heading(heading)
        scene = Scene(identifier=identifier, heading=heading, heading_line=first_number + index,
                      first=first_number + index, last=first_number + last_index, int_ext=int_ext, place_text=place,
                      time_text=time, presentation_note=note, presentation=presentation_for(note))
        if reading.dialect in ("stage", "comic"):
            scene.int_ext, scene.place_text, scene.time_text = "int", heading, "none"
        reading.scenes.append(scene)
        read_scene(reading, scene, index, last_index, cue_names, characters, constants,
                   is_last=position == len(heading_indexes) - 1)
    if heading_indexes and pending_in:
        reading.scenes[0].transition_in, reading.scenes[0].transition_in_line = pending_in
    for position, scene in enumerate(reading.scenes):
        if position and scene.transition_in_line is None:
            previous = reading.scenes[position - 1]
            carried_in = getattr(previous, "join_into_next", None)
            if carried_in:
                scene.transition_in, scene.transition_in_line = carried_in
            elif previous.transition_out in ("dissolve", "match_cut", "smash_cut"):
                scene.transition_in = previous.transition_out
                scene.transition_in_line = previous.transition_out_line
            elif "CONTINUOUS" in scene.time_text.upper():
                scene.transition_in = "continuous"
    if not heading_indexes:
        reading.odd_lines.append(OddLine(first_number, reading.last_line_number, "",
                                         "no scene headings were found, so there are no scenes yet", "no_scenes"))
    if reading.source_kind == "treatment":
        reading.odd_lines.append(OddLine(first_number, reading.last_line_number, "",
                                         "a thin source: scene headings but no speeches. Later steps write scenes and "
                                         "speeches as inventions, each shown to the user", "thin_source"))
    finish_characters(reading, characters, cue_names)
    settle_repeated_capitals(reading)
    reading.counts = {
        "scenes": len(reading.scenes), "headings": len(heading_indexes), "speeches": len(reading.speeches),
        "dialogue_words": sum(scene.counts.get("dialogue_words", 0) for scene in reading.scenes),
        "action_words": sum(scene.counts.get("action_words", 0) for scene in reading.scenes),
        "spoken_characters": sum(scene.counts.get("spoken_characters", 0) for scene in reading.scenes),
        "beat_marks": sum(scene.counts.get("beat_marks", 0) for scene in reading.scenes),
        "cues": sum(1 for kind in types if kind in (CUE, CUE_WITH_SPEECH)),
        "transitions": sum(1 for kind in types if kind == TRANSITION),
        "parentheticals": sum(1 for kind in types if kind == PARENTHETICAL),
        "title_lines": sum(1 for kind in types if kind == TITLE),
        "cards": sum(len(scene.cards) for scene in reading.scenes),
        "lines": len(lines), "words": reading.words,
    }


def cue_name_of(text):
    """(name, extension) of a cue line: '@SAYE (RECORDED)' gives ('SAYE', 'RECORDED')."""
    name = text.strip().lstrip("@").strip()
    if name.endswith("^"):
        name = name[:-1].strip()
    extensions = []
    while True:
        match = EXTENSION.search(name)
        if not match:
            break
        extensions.insert(0, match.group(1).strip())
        name = name[:match.start()].strip()
    extensions = [extension for extension in extensions
                  if normalise_word(extension).replace("_", "") not in ("contd", "cont", "continued", "continuing")]
    name = re.sub(r"\.(?=\s|$)", "", name)
    name = re.sub(r"\s+", " ", name).strip().upper()
    return name, "; ".join(extensions)


def inline_cue_parts(text):
    """(name, extension, speech) of a 'NAME. words' or 'NAME: words' line (stage plays, comic balloons)."""
    match = INLINE_CUE.match(re.sub(r"^\d+\.?\s*", "", text.strip()))
    if not match:
        return None
    name, extension = cue_name_of(match.group(1) + (match.group(2) or ""))
    return name, extension, match.group(3).strip()


def collect_cue_names(reading):
    names = []
    for index, kind in enumerate(reading.types):
        if kind == CUE:
            name, _ = cue_name_of(reading.lines[index])
        elif kind == CUE_WITH_SPEECH:
            parts = inline_cue_parts(reading.lines[index])
            name = parts[0] if parts else None
        else:
            continue
        if name and name not in names:
            names.append(name)
    return names


# C16: a voice comes through a device only when the parenthetical names one of these (or radio, phone, intercom,
# recording, an earpiece or "in her ear", matched below, and the cue extensions V.O., O.S. and RECORDED). Anything
# else a character speaks "through" (a torch held in the teeth, a mask, a door) stays her own direct voice.
DEVICE_SPEAKER_WORDS = ("speaker", "loudspeaker", "tannoy", "tablet", "screen")

PATH_BY_WORDS = [
    (re.compile(r"\bhelmet\b", re.IGNORECASE), "helmet_inside", "the parenthetical names a helmet"),
    (re.compile(r"\b(in (her|his|their|my|your|its) ears?|earpiece|ear piece|in-ear)\b", re.IGNORECASE), "earpiece",
     "the parenthetical says the voice is in an ear"),
    (re.compile(r"\b(radio|walkie|two-way)\b", re.IGNORECASE), "radio", "the parenthetical names a radio"),
    (re.compile(r"\bintercom\b", re.IGNORECASE), "intercom", "the parenthetical names an intercom"),
    (re.compile(r"\b(phone|filtered|on the line)\b", re.IGNORECASE), "phone", "the parenthetical names a phone"),
    (re.compile(r"\b(recorded|recording|on tape|playback|tape|video)\b", re.IGNORECASE), "recording",
     "the parenthetical names a recording"),
    (re.compile(r"\bthrough (the )?glass\b", re.IGNORECASE), "through_glass", "the parenthetical names glass"),
    (re.compile(r"\b(through|over|from|on) (the |a |her |his |their )?(" + "|".join(DEVICE_SPEAKER_WORDS) + r")\b"
                r"|\b(loud)?speaker\b", re.IGNORECASE), "device_speaker",
     "the parenthetical names a device that plays the voice"),
    (re.compile(r"\b(thought|thinking|inner voice|in (her|his) head)\b", re.IGNORECASE), "thought",
     "the parenthetical says it is a thought"),
]
PATH_BY_EXTENSION = [
    (re.compile(r"^(V\.?\s?O\.?|VOICE ?OVER|NARRATOR|NARRATING)$", re.IGNORECASE), "voice_over"),
    (re.compile(r"^(O\.?\s?S\.?|O\.?\s?C\.?|OFF|OFF-?SCREEN|OFF CAMERA)$", re.IGNORECASE), "off_screen"),
    (re.compile(r"^(RECORDED|RECORDING|ON TAPE|ON RECORDING|PLAYBACK|VIDEO|ON VIDEO|ON SCREEN)$", re.IGNORECASE),
     "recording"),
    (re.compile(r"^(FILTERED|ON PHONE|PHONE|ON THE PHONE)$", re.IGNORECASE), "phone"),
    (re.compile(r"^(RADIO|OVER RADIO|ON RADIO)$", re.IGNORECASE), "radio"),
    (re.compile(r"^(INTERCOM)$", re.IGNORECASE), "intercom"),
    (re.compile(r"^(THOUGHT|THINKING|THOUGHTS)$", re.IGNORECASE), "thought"),
]


def speech_path(extension, parentheticals):
    """(path, reason) of a speech: the parenthetical under the cue names a device first, then the cue extension."""
    for _, text in parentheticals[:1] + parentheticals[1:]:
        for pattern, path, reason in PATH_BY_WORDS:
            if pattern.search(text):
                return path, reason, True
    for piece in [part.strip() for part in (extension or "").split(";") if part.strip()]:
        for pattern, path in PATH_BY_EXTENSION:
            if pattern.match(piece):
                return path, f"the cue says ({piece})", False
    return "direct", "no extension or device named", False


def read_scene(reading, scene, first_index, last_index, cue_names, characters, constants, is_last=False):
    types = reading.types
    lines = reading.lines
    first_number = reading.first_line_number
    speech_number = 0
    dialogue_words = action_words = spoken = beats = 0
    # Joins after the scene's last speech close the scene (placement rules); action after a cut to black plays
    # over the black, and cards after it are title or end cards.
    last_story = max([index for index in range(first_index + 1, last_index + 1)
                      if types[index] in (CUE, CUE_WITH_SPEECH, DIALOGUE, PARENTHETICAL, LYRIC)] or [first_index])
    closing = None
    cue_indexes = [index for index in range(first_index, last_index + 1) if types[index] in (CUE, CUE_WITH_SPEECH)]
    widths = 3 if len(cue_indexes) > constant(constants, "speech_ids_three_digits_above", 99) else 2
    black_before = False
    for index in range(first_index + 1, last_index + 1):
        kind = types[index]
        number = first_number + index
        text = lines[index].strip()
        if kind == TRANSITION:
            value, known = transition_value(text)
            if index > last_story:
                if value == "fade_in":
                    scene.join_into_next = (value, number)
                else:
                    scene.transition_out, scene.transition_out_line = value, number
                    closing = index
                    if value in ("cut_to_black", "fade_out"):
                        black_before = True
            else:
                reading.odd_lines.append(OddLine(number, number, text, f"a join written inside {scene_words(scene)}, "
                                                 "with story lines after it; it is not the scene's last join",
                                                 "transition_inside"))
            if not known:
                reading.odd_lines.append(OddLine(number, number, text, "a join the list of joins does not name; read "
                                                 "as a plain cut", "transition_unknown"))
        elif kind == CARD:
            card_text = text.lstrip("=>").rstrip("<").strip()
            if not card_text:
                continue
            numbers = constant(constants, "end_card_numbers", [990, 999])
            shot_number = numbers[0] + len(scene.cards)
            shot = f"{scene.identifier}-SH{shot_number:03d}"
            last_scene_end = is_last and closing is not None
            what = ("an end card after the last scene's final join" if last_scene_end and black_before
                    else "a title card after the black" if black_before else "a card inside the film")
            scene.cards.append({"line": number, "text": card_text, "shot": shot, "kind": what})
            scene.notes.append(f'Line {number}, "{text}": {what}; it becomes shot {shot_number} of this scene '
                               f"({shot}).")
            reading.odd_lines.append(OddLine(number, number, text, f"{what}: it becomes its own shot, shot "
                                             f"{shot_number} of {scene_words(scene)}", "card"))
        elif kind in (CUE, CUE_WITH_SPEECH):
            speech_number += 1
            speech = read_speech(reading, scene, index, last_index, speech_number, widths)
            reading.speeches.append(speech)
            scene.speeches.append(speech.identifier)
            dialogue_words += speech.word_count
            spoken += speech.spoken_characters
            beats += speech.beat_marks
            character = characters.get(speech.cue_name)
            if character is None:
                character = Character(identifier=character_identifier(speech.cue_name, characters),
                                      cue_name=speech.cue_name, names=[speech.cue_name], first_line=speech.cue_line)
                characters[speech.cue_name] = character
            character.cues += 1
            speech.speaker = character.identifier
        elif kind == ACTION:
            action_words += count_words(text)
            read_action_line(reading, scene, number, lines[index], cue_names, characters)
            if closing is not None:
                joined = scene.transition_out.replace("_", " ")
                where = "over the black" if black_before else "after the join"
                reading.odd_lines.append(OddLine(number, number, text, f"comes after the {joined} at line "
                                                 f"{first_number + closing} in {scene_words(scene)}: it plays {where}",
                                                 "after_join"))
        elif kind in (SECTION, NOTE, SYNOPSIS, BONEYARD):
            previous = reading.odd_lines[-1] if reading.odd_lines else None
            if previous is not None and previous.kind == kind and number - previous.last <= 2:
                previous.last = number
                continue
            what = {"section": "a section line", "note": "a note for the writer", "synopsis": "a synopsis line",
                    "boneyard": "text the writer set aside"}[kind]
            reading.odd_lines.append(OddLine(number, number, text, f"{what} inside {scene_words(scene)}: not story, "
                                             "left out of the shots", kind))
    if scene.presentation_note:
        what = scene.presentation.replace("_", " ")
        host_words = ("; the device it is seen on is named at step 5 of 12, where the cameras inside the story are "
                      "designed") if scene.presentation in ("on_screen", "recording") else ""
        scene.notes.append(f'The heading ends "({scene.presentation_note})": a presentation note, so presentation '
                           f"is {scene.presentation}{host_words} (A3 §4.3 step 3).")
        reading.odd_lines.append(OddLine(scene.heading_line, scene.heading_line, f"({scene.presentation_note})",
                                         f"a note at the end of the heading of {scene_words(scene)}: how the scene is "
                                         f"shown ({what}), not the name of the place{host_words}", "presentation"))
    scene.counts = {"dialogue_words": dialogue_words, "action_words": action_words, "speeches": len(scene.speeches),
                    "beat_marks": beats, "spoken_characters": spoken,
                    "lines": scene.last - scene.first + 1,
                    "non_blank_lines": sum(1 for index in range(first_index, last_index + 1) if lines[index].strip())}


def scene_words(scene):
    return scene_words_of(scene.identifier)


def scene_words_of(identifier):
    """'SC10' becomes 'scene 10', 'SC06A' becomes 'scene 6A' (for plain messages)."""
    match = re.match(r"SC0*(\d+)([A-Z]?)$", identifier)
    return f"scene {match.group(1)}{match.group(2)}" if match else identifier


def read_speech(reading, scene, cue_index, last_index, number, width):
    types = reading.types
    lines = reading.lines
    first_number = reading.first_line_number
    cue_text = lines[cue_index].strip()
    text_lines = []
    parentheticals = []
    pieces = []
    spoken = 0
    beats = 0
    if types[cue_index] == CUE_WITH_SPEECH:
        name, extension, first_words = inline_cue_parts(cue_text) or (cue_text, "", "")
        pieces.append(first_words)
        spoken += len(first_words)
        text_lines.append(first_number + cue_index)
    else:
        name, extension = cue_name_of(cue_text)
    end = cue_index
    index = cue_index + 1
    while index <= last_index and types[index] in SPEECH_TYPES + ((DIALOGUE,) if types[cue_index] == CUE_WITH_SPEECH else ()):
        text = lines[index].strip()
        if types[index] == PARENTHETICAL:
            inner = text[1:-1].strip() if text.startswith("(") and text.endswith(")") else text
            parentheticals.append((first_number + index, inner))
            if f"({inner.lower()})" == "(beat)":
                beats += 1
        else:
            pieces.append(text.lstrip("~").strip())
            spoken += len(text)
            text_lines.append(first_number + index)
        end = index
        index += 1
    words = " ".join(piece for piece in pieces if piece)
    path, reason, from_parenthetical = speech_path(extension, parentheticals)
    identifier = f"{scene.identifier}-D{number:0{width}d}"
    speech = Speech(identifier=identifier, scene=scene.identifier, speaker="", cue_name=name,
                    cue_line=first_number + cue_index, first=first_number + cue_index, last=first_number + end,
                    text=words, text_lines=text_lines, parentheticals=parentheticals, extension=extension, path=path,
                    path_reason=reason, word_count=count_words(words), beat_marks=beats, spoken_characters=spoken)
    speech.path_from_parenthetical = from_parenthetical
    return speech


# -- capitalised words and light words (A3 §4.3 steps 5 and 6; B2 P2)

def classify_capitals(token, line, start, end, cue_names):
    """(class, why) of a capitalised word in an action line, by A3 §4.3 step 5's tests in order."""
    words = token.split()
    before = line[:start]
    after = line[end:]
    previous_words = re.findall(r"[\w'’-]+", before.lower())[-6:]
    letters = re.sub(r"[^A-Za-z]", "", line)
    standalone = letters and letters.upper() == letters
    sentence_start = not before.strip() or before.rstrip().endswith((".", "!", "?", ":"))
    # Picture instructions inside action (A3 §4.3 step 6): 'VISOR VIEW:' and 'BLACK.' on their own.
    if not before.strip() and after.startswith(":") and not any(word in SOUND_WORDS for word in words):
        return "instruction", "a capitalised instruction ending in a colon at the start of the line"
    if token == "BLACK" and sentence_start:
        return "instruction", "BLACK at the start of a sentence: a black frame inside the scene"
    # Test 1: a person introduced.
    if not standalone:
        if AGE_OR_DESCRIPTION.match(after):
            return "character", "a name followed by a description"
        if any(word in cue_names for word in (words[0], words[-1])) or token in cue_names:
            return "character", "the name of a speaking character"
        role = " ".join(words[1:]) if words[0] == "THE" and len(words) > 1 else token
        if role in ROLE_WORDS or words[-1] in ROLE_WORDS:
            if (previous_words and previous_words[-1] in DETERMINERS) or words[0] == "THE":
                return "character", "a role's first appearance"
    # Test 2: printed, displayed or read.
    if standalone:
        if len(words) == 1 and words[0] in SOUND_WORDS:
            return "sound", "a sound word on its own line"
        return "text", "a whole line in capitals: text in picture"
    if ":" in before and not re.search(r"[a-z]", before.rsplit(":", 1)[1]):
        return "text", "straight after a colon: text in picture"
    if any(word in TEXT_SIGNALS for word in previous_words[-3:]):
        if not (previous_words[-1:] == ["into"] and not after.lstrip().startswith((".", ","))):
            return "text", "a word near it says it is printed, shown or pressed"
    following = re.findall(r"[\w'’-]+", after.lower())[:2]
    if following and following[0] in FOLLOWING_TEXT_SIGNALS:
        return "text", "the next word says it is printed or stitched"
    if previous_words[-1:] == ["into"] and after.lstrip().startswith("."):
        return "text", "pressed or driven into: a label"
    if any(word in DISPLAY_WORDS for word in re.findall(r"[a-z]+", line.lower())) and not any(word in SOUND_WORDS for word in words):
        return "text", "the line is about a screen or display"
    # Test 3: a sound.
    if any(word in SOUND_WORDS for word in words):
        return "sound", "a sound word"
    # Test 4: an object's first mention.
    position = len(previous_words)
    while position > 0 and previous_words[position - 1] in DESCRIBING_WORDS:
        position -= 1
    if position > 0 and previous_words[position - 1] in DETERMINERS:
        return "prop", "a thing named after a, the or a number"
    # Test 5: anything else.
    return "emphasis", "none of the other tests fits"


def read_action_line(reading, scene, number, line, cue_names, characters):
    for match in CAPITALS.finditer(line):
        token = match.group(0).strip()
        if len(re.sub(r"[^A-Z]", "", token)) < 2:
            continue
        kind, why = classify_capitals(token, line, match.start(), match.end(), cue_names)
        scene.tokens.append({"text": token, "line": number, "class": kind, "why": why})
        if kind == "instruction":
            scene.instructions.append({"line": number, "text": token})
        if kind == "character":
            words = token.split()
            owner = next((name for name in cue_names if name in (token, words[0], words[-1])), None)
            if owner and token != owner:
                scene.alias_candidates = getattr(scene, "alias_candidates", [])
                scene.alias_candidates.append((owner, token, number))
            elif not owner:
                reading.people_without_speeches.append({"name": token, "line": number, "scene": scene.identifier})
    found = sorted({word.lower() for word in re.findall(r"[A-Za-z]+", line) if word.lower() in LIGHT_WORDS})
    if found:
        scene.light_lines.append({"line": number, "words": found})


def finish_characters(reading, characters, cue_names):
    """Aliases from introductions, who is present in each scene, and the odd cues (A3 §4.3 step 7)."""
    for scene in reading.scenes:
        for owner, alias, number in getattr(scene, "alias_candidates", []):
            character = characters.get(owner)
            if character is not None and alias not in character.names:
                character.names.append(alias)
                character.alias_lines[alias] = number
                reading.odd_lines.append(OddLine(number, number, alias, f"taken as another name for "
                                                 f"{name_for_people(owner)} (introduced in {scene_words(scene)})",
                                                 "alias"))
    ordered = sorted(characters.values(), key=lambda character: character.first_line or 0)
    reading.characters = ordered
    by_name = {character.cue_name: character for character in ordered}
    # V.O. speeches with no device named take the device of the same speaker's latest earlier V.O. (A3 §4.3 step 4).
    last_device = {}
    for speech in reading.speeches:
        if getattr(speech, "path_from_parenthetical", False):
            if "V" in (speech.extension or "").upper():
                last_device[speech.cue_name] = (speech.path, speech.cue_line)
        elif speech.path == "voice_over" and speech.cue_name in last_device:
            path, line = last_device[speech.cue_name]
            speech.path = path
            speech.path_reason = f"the same speaker's earlier voice over at line {line} named the device"
            reading.odd_lines.append(OddLine(speech.cue_line, speech.cue_line, reading.line(speech.cue_line).strip(),
                                             f"a voice over with no device named: read as the same {path.replace('_', ' ')} "
                                             f"as line {line}", "voice_path"))
    # Presence: speakers first (most speeches first), then characters named in the action lines.
    patterns = {}
    for character in ordered:
        forms = []
        for name in character.names:
            forms += [name, name_for_people(name)]
        patterns[character.identifier] = re.compile(r"(?<![\w])(" + "|".join(re.escape(form) for form in sorted(set(forms), key=len, reverse=True)) + r")(?![\w])")
    speech_by_id = {speech.identifier: speech for speech in reading.speeches}
    for scene in reading.scenes:
        counts = {}
        first_cue = {}
        for identifier in scene.speeches:
            speech = speech_by_id[identifier]
            counts[speech.speaker] = counts.get(speech.speaker, 0) + 1
            first_cue.setdefault(speech.speaker, speech.cue_line)
        speaking = sorted(counts, key=lambda speaker: (-counts[speaker], first_cue[speaker]))
        scene.speaking = [(speaker, counts[speaker]) for speaker in speaking]
        mentioned = []
        for index in range(scene.first - reading.first_line_number, scene.last - reading.first_line_number + 1):
            if reading.types[index] != ACTION:
                continue
            for character in ordered:
                if character.identifier in speaking or character.identifier in mentioned:
                    continue
                if patterns[character.identifier].search(reading.lines[index]):
                    mentioned.append(character.identifier)
        scene.characters = speaking + mentioned
        scene.title = plain_place(scene.place_text, cue_names) if scene.place_text != "none" else scene.heading
    # Cue names that look like one person under two names (never merged by code).
    names = [character.cue_name for character in ordered]
    for name in names:
        for other in names:
            if name != other and set(name.split()) < set(other.split()):
                character = by_name[other]
                reading.odd_lines.append(OddLine(character.first_line, character.first_line, other,
                                                 f'the cue "{other}" may be the same person as "{name}"; they are kept as '
                                                 "two characters until you say they are one", "cue_names"))
    seen = set()
    unique = []
    for person in reading.people_without_speeches:
        key = person["name"]
        if key in seen:
            continue
        seen.add(key)
        unique.append(person)
    reading.people_without_speeches = unique


def settle_repeated_capitals(reading):
    """The same capitalised words read the same way everywhere: a word left as emphasis or a thing takes the class
    its words have elsewhere as a sound or as words seen on screen."""
    known = {}
    for scene in reading.scenes:
        for token in scene.tokens:
            if token["class"] in ("sound", "text"):
                known.setdefault(token["text"], (token["class"], token["line"]))
    for scene in reading.scenes:
        for token in scene.tokens:
            if token["class"] in ("emphasis", "prop") and token["text"] in known:
                kind, line = known[token["text"]]
                token["class"] = kind
                token["why"] = f"the same words are read as {'a sound' if kind == 'sound' else 'text in picture'} at line {line}"


def plain_place(place_text, cue_names):
    """'SAYE'S HOUSE - KITCHEN' becomes "Saye's house - kitchen" (names of characters keep their capitals)."""
    text = place_text.strip()
    if text.upper() != text:
        return text
    result = text.lower()
    result = result[:1].upper() + result[1:]
    for name in cue_names:
        for word in name.split():
            if len(word) > 1:
                result = re.sub(r"(?<![\w])" + re.escape(word.lower()) + r"(?![\w])", name_for_people(word), result)
    return result


# -- prose

def is_chapter_heading(text):
    text = text.lstrip("#").strip()
    return bool(ROMAN_OR_NUMBER_HEADING.match(text) or CHAPTER_WORD_HEADING.match(text))


def read_prose(reading, story, constants):
    lines = reading.lines
    hints = story.hints or [None] * len(lines)
    first_number = reading.first_line_number
    types = []
    for index, line in enumerate(lines):
        text = line.strip()
        before_blank = index == 0 or not lines[index - 1].strip()
        after_blank = index + 1 >= len(lines) or not lines[index + 1].strip()
        if not text:
            types.append(BLANK)
        elif hints[index] == "heading" or text.startswith("#"):
            types.append(CHAPTER_HEADING if is_chapter_heading(text) else OTHER_HEADING)
        elif story.file_kind == "text" and before_blank and after_blank and PLAIN_CHAPTER_LINE.match(text) \
                and len(text.split()) <= 8:
            types.append(CHAPTER_HEADING)
        elif text.startswith(">"):
            types.append(QUOTATION)
        else:
            types.append(PARAGRAPH)
    reading.types = types
    chapter_indexes = [index for index, kind in enumerate(types) if kind == CHAPTER_HEADING]
    heading_indexes = [index for index, kind in enumerate(types) if kind in (CHAPTER_HEADING, OTHER_HEADING)]
    title_index = None
    if heading_indexes and types[heading_indexes[0]] == OTHER_HEADING and len(heading_indexes) > 1 \
            and types[heading_indexes[1]] == CHAPTER_HEADING:
        title_index = heading_indexes[0]
    elif heading_indexes and types[heading_indexes[0]] == OTHER_HEADING and not chapter_indexes:
        title_index = heading_indexes[0]
    elif chapter_indexes:
        first_filled = next((index for index, kind in enumerate(types) if kind != BLANK), None)
        if first_filled is not None and first_filled < chapter_indexes[0] and types[first_filled] == PARAGRAPH \
                and len(lines[first_filled].split()) <= 8 and not re.search(r"[.!?,;]$", lines[first_filled].strip()) \
                and all(types[index] == BLANK for index in range(first_filled + 1, chapter_indexes[0])):
            title_index = first_filled
    if title_index is not None:
        reading.title = lines[title_index].lstrip("#").strip()
        reading.title_line = first_number + title_index
        types[title_index] = TITLE
        reading.odd_lines.append(OddLine(first_number + title_index, first_number + title_index,
                                         lines[title_index].strip(), f'the title of the book; the clean title is '
                                         f'probably "{clean_title(reading.title)}"', "title"))
    elif story.title:
        reading.title = story.title
    start = (title_index + 1) if title_index is not None else 0
    front_end = chapter_indexes[0] if chapter_indexes else start
    for index in range(start, front_end):
        if types[index] in (PARAGRAPH, QUOTATION, OTHER_HEADING):
            types[index] = FRONT_MATTER
            reading.odd_lines.append(OddLine(first_number + index, first_number + index, lines[index].strip(),
                                             "between the title and the first chapter: front matter, about the file "
                                             "or the book, outside every chapter", "front_matter"))
    for index in range(0, title_index or 0):
        if types[index] in (PARAGRAPH, QUOTATION, OTHER_HEADING):
            types[index] = FRONT_MATTER
            reading.odd_lines.append(OddLine(first_number + index, first_number + index, lines[index].strip(),
                                             "before the title: front matter, outside every chapter", "front_matter"))
    if chapter_indexes:
        for position, index in enumerate(chapter_indexes):
            last_index = (chapter_indexes[position + 1] - 1) if position + 1 < len(chapter_indexes) else len(lines) - 1
            body = "\n".join(lines[index + 1:last_index + 1])
            reading.chapters.append(Chapter(identifier=f"CP{position + 1:02d}", title=lines[index].lstrip("#").strip(),
                                            heading_line=first_number + index, first=first_number + index,
                                            last=first_number + last_index, words=count_words(body)))
    elif lines:
        first_story = next((index for index in range(start, len(lines)) if types[index] in (PARAGRAPH, QUOTATION)), None)
        if first_story is not None:
            reading.chapters.append(Chapter(identifier="CP01", title=reading.title or "The whole story",
                                            heading_line=None, first=first_number + first_story,
                                            last=first_number + len(lines) - 1,
                                            words=count_words("\n".join(lines[first_story:]))))
            reading.odd_lines.append(OddLine(first_number + first_story, first_number + len(lines) - 1, "",
                                             "no chapter headings were found, so the whole story is one chapter",
                                             "no_chapters"))
    quotations = [first_number + index for index, kind in enumerate(types) if kind == QUOTATION]
    if quotations:
        verb = "starts" if len(quotations) == 1 else "start"
        reading.odd_lines.append(OddLine(quotations[0], quotations[-1], lines[quotations[0] - first_number].strip()[:1],
                                         f'{counted(len(quotations), "line")} {verb} with ">": quotations or set-off '
                                         "passages inside the story, not joins between scenes", "quotations"))
    find_prose_blocks(reading)
    reading.name_candidates = prose_name_candidates(reading)
    reading.counts = {"chapters": len(reading.chapters), "lines": len(lines), "words": reading.words,
                      "quotation_lines": len(quotations),
                      "action_words": sum(chapter.words for chapter in reading.chapters),
                      "dialogue_words": 0, "speeches": 0, "beat_marks": 0}


def find_prose_blocks(reading):
    """Set-off passages in italics, verse, and passages repeated word for word (D14 R27, R28, R37)."""
    lines = reading.lines
    first_number = reading.first_line_number
    minimum = 3
    italic = [index for index, line in enumerate(lines)
              if re.fullmatch(r">?\s*\*[^*].*\*", line.strip()) or re.fullmatch(r">?\s*_[^_].*_", line.strip())]
    blocks = []
    for index in italic:
        if blocks and all(not lines[between].strip() or between in italic for between in range(blocks[-1][1] + 1, index)):
            blocks[-1][1] = index
        else:
            blocks.append([index, index])
    reading.set_off_blocks = [{"lines": [first_number + a, first_number + b]} for a, b in blocks]
    if blocks:
        shown = ", ".join(f"{first_number + a} to {first_number + b}" if a != b else f"{first_number + a}"
                          for a, b in blocks[:6])
        more = f" and {len(blocks) - 6} more" if len(blocks) > 6 else ""
        reading.odd_lines.append(OddLine(first_number + blocks[0][0], first_number + blocks[-1][1], "",
                                         f"{counted(len(blocks), 'passage')} set off in italics (lines {shown}{more}): "
                                         "letters, notes, songs or documents inside the story; say what each one is "
                                         "and who wrote it", "set_off"))
    verse = []
    run = []
    for index, line in enumerate(lines + [""]):
        text = line.strip()
        if text and 0 < len(real_words(text)) <= 12 and not text.startswith("#"):
            run.append(index)
            continue
        if len(run) >= minimum and all(run[position] + 1 == run[position + 1] for position in range(len(run) - 1)):
            verse.append([run[0], run[-1]])
        run = []
    merged = []
    for a, b in verse:
        if merged and a - merged[-1][1] <= 3:
            merged[-1][1] = b
        else:
            merged.append([a, b])
    reading.verse = [{"lines": [first_number + a, first_number + b]} for a, b in merged]
    for a, b in merged:
        reading.odd_lines.append(OddLine(first_number + a, first_number + b, lines[a].strip(),
                                         "short lines one after another: verse, a song or a list; a song quoted in "
                                         "the story may carry its own rights", "verse"))
    paragraphs = {}
    for index, line in enumerate(lines):
        key = normalise_quote(line)
        if len(real_words(key)) >= minimum and not key.startswith("#"):
            paragraphs.setdefault(key, []).append(index)
    repeated = sorted((indexes[0], later) for indexes in paragraphs.values() if len(indexes) > 1 for later in indexes[1:])
    runs = []
    for original, later in repeated:
        if runs and later > runs[-1]["later"][1] and later - runs[-1]["later"][1] <= 2 and \
                original - runs[-1]["original"][1] <= 2 and original > runs[-1]["original"][1]:
            runs[-1]["later"][1] = later
            runs[-1]["original"][1] = original
            runs[-1]["paragraphs"] += 1
        else:
            runs.append({"original": [original, original], "later": [later, later], "paragraphs": 1})
    reading.repeats = [{"lines": [first_number + run["later"][0], first_number + run["later"][1]],
                        "repeat_of": [first_number + run["original"][0], first_number + run["original"][1]],
                        "paragraphs": run["paragraphs"]} for run in runs]
    for run in reading.repeats:
        if run["paragraphs"] < 2:
            continue
        a, b = run["lines"]
        c, d = run["repeat_of"]
        reading.odd_lines.append(OddLine(a, b, reading.line(a).strip(),
                                         f"repeats lines {c} to {d} word for word ({run['paragraphs']} paragraphs); a quote "
                                         "from them is found twice, so cite it inside its chapter", "repeat"))


def prose_name_candidates(reading):
    counts = {}
    for index, line in enumerate(reading.lines):
        if reading.types[index] not in (PARAGRAPH, QUOTATION):
            continue
        for match in re.finditer(r"(?<![\w'’])([A-Z][^\W\d_]+(?:\s[A-Z][^\W\d_]+)?)", line):
            before = line[:match.start()].rstrip()
            if not before or before.endswith((".", "!", "?", ":", '"', "“", "*", ">", "—")):
                continue
            name = match.group(1)
            if name.split()[0] in PROSE_NAME_STOPWORDS:
                continue
            counts[name] = counts.get(name, 0) + 1
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [{"name": name, "count": count} for name, count in ranked[:20] if count > 1]


# -- the first estimate (D13 §4.1 v0, from word counts)

def first_estimate(reading, constants):
    """Low, central and high seconds from the words: speech words at the speaking pace plus a little per speech and
    per (beat), and action words at v0_action_seconds_per_word (D13 §4.1). For prose every word counts as action,
    so the figure is rough and only sets the default format."""
    counts = reading.counts
    if not counts:
        return None
    pace = constant(constants, "speech_wps_default", 2.5)
    per_speech = constant(constants, "speech_floor_extra_s", 0.5)
    pause = (constant(constants, "pause_tiers", {}) or {}).get("script_words", {}).get("(beat)", 1.0)
    low_rate, high_rate = constant(constants, "v0_action_seconds_per_word", [0.166, 0.22])
    speech_seconds = counts.get("dialogue_words", 0) / pace + per_speech * counts.get("speeches", 0) \
        + pause * counts.get("beat_marks", 0)
    action = counts.get("action_words", 0)
    low = speech_seconds + action * low_rate
    high = speech_seconds + action * high_rate
    central = (low + high) / 2
    return {"low_s": round(low), "central_s": round(central), "high_s": round(high),
            "speech_s": round(speech_seconds, 1), "basis": "D13 §4.1 v0 from word counts",
            "rough": reading.source_kind != "screenplay",
            "minutes": [round(low / 60), round(central / 60), round(high / 60)]}


# ---------------------------------------------------------------- the story map (what later tools read)

def story_map_of(reading, source_file=None, fingerprint=None):
    """The reader's results as JSON data (For machines - do not edit/story map.json)."""
    return {
        "story_map_version": STORY_MAP_VERSION,
        "made": now(),
        "source": {"file": source_file or reading.file_name, "fingerprint": fingerprint,
                   "format": reading.source_format, "kind": reading.source_kind, "dialect": reading.dialect,
                   "extraction": reading.extraction, "language": reading.language},
        "first_line_number": reading.first_line_number,
        "line_count": len(reading.lines),
        "words": reading.words,
        "title": {"text": reading.title, "line": reading.title_line,
                  "clean": clean_title(reading.title) if reading.title else None},
        "scene_id_digits": reading.scene_id_digits,
        "counts": reading.counts,
        "first_estimate": reading.first_estimate,
        "scenes": [{
            "id": scene.identifier, "title": scene.title, "heading": scene.heading, "heading_line": scene.heading_line,
            "lines": [scene.first, scene.last], "int_ext": scene.int_ext, "place_text": scene.place_text,
            "time_text": scene.time_text, "presentation_note": scene.presentation_note,
            "presentation": scene.presentation, "transition_in": scene.transition_in,
            "transition_in_line": scene.transition_in_line, "transition_out": scene.transition_out,
            "transition_out_line": scene.transition_out_line, "characters": scene.characters,
            "speaking": [{"character": speaker, "cues": count} for speaker, count in scene.speaking],
            "speeches": scene.speeches, "cards": scene.cards, "instructions": scene.instructions,
            "capitalised_words": scene.tokens, "light_lines": scene.light_lines, "counts": scene.counts,
        } for scene in reading.scenes],
        "chapters": [{"id": chapter.identifier, "title": chapter.title, "heading_line": chapter.heading_line,
                      "lines": [chapter.first, chapter.last], "words": chapter.words} for chapter in reading.chapters],
        "characters": [{"id": character.identifier, "cue": character.cue_name, "names": character.names,
                        "cues": character.cues, "first_line": character.first_line,
                        "alias_lines": character.alias_lines} for character in reading.characters],
        "people_without_speeches": reading.people_without_speeches,
        "odd_lines": [{"lines": [odd.first, odd.last], "text": odd.text, "finding": odd.finding, "kind": odd.kind}
                      for odd in reading.odd_lines],
        "set_off_blocks": reading.set_off_blocks, "verse": reading.verse, "repeats": reading.repeats,
        "name_candidates": reading.name_candidates,
        "line_types": reading.types,
        "lines": reading.lines,
    }


def speeches_json(reading):
    return {"speeches_version": 1, "source": reading.file_name, "count": len(reading.speeches),
            "speeches": [speech.to_json() for speech in reading.speeches]}


# ---------------------------------------------------------------- the numbered story, for later questions

class NumberedStory:
    """The numbered lines of a story and their types, with the quote-anchor rules of G5 and WP12a's adopt rule:
    an anchor must hold at least 3 words and be found exactly once in its scope (the scene or chapter for scene
    fields and story points, the whole story otherwise); a range starts at the cue of the speech its first quote
    is in, and runs on through the rest of its last quote's speech, then through blank lines, lines of fewer than
    3 words and cues whose speech has fewer than 3 words."""

    def __init__(self, lines, first_line_number=1, types=None, scenes=None, chapters=None):
        self.lines = list(lines)
        self.first = first_line_number
        self.last = first_line_number + len(self.lines) - 1
        self.types = list(types) if types else None
        self.scenes = {scene["id"]: tuple(scene["lines"]) for scene in (scenes or [])}
        self.chapters = {chapter["id"]: tuple(chapter["lines"]) for chapter in (chapters or [])}
        self.minimum_words = 3

    @classmethod
    def from_story_map(cls, data):
        return cls(data["lines"], data.get("first_line_number", 1), data.get("line_types"), data.get("scenes"),
                   data.get("chapters"))

    @classmethod
    def from_project(cls, project_folder):
        path = Path(project_folder) / MACHINE_FOLDER / STORY_MAP_FILE
        if not path.is_file():
            raise StageStop("The story has not been read yet. Run: stage.py read")
        with open(path, encoding="utf-8") as handle:
            return cls.from_story_map(json.load(handle))

    @classmethod
    def from_file(cls, story_path, constants=None):
        reading = read_story_lines(load_story_file(story_path), constants)
        data = story_map_of(reading)
        return cls.from_story_map(data)

    def line(self, number):
        index = number - self.first
        return self.lines[index] if 0 <= index < len(self.lines) else ""

    def type_of(self, number):
        index = number - self.first
        if self.types and 0 <= index < len(self.types):
            return self.types[index]
        text = self.line(number).strip()
        if not text:
            return BLANK
        return CUE if text.startswith("@") else None

    def scope_of(self, identifier):
        """(first, last) lines of a scene or chapter, or of the whole story when identifier is None."""
        if identifier is None:
            return self.first, self.last
        if identifier in self.scenes:
            return self.scenes[identifier]
        if identifier in self.chapters:
            return self.chapters[identifier]
        return None

    def words(self, number):
        return real_words(self.line(number))

    def speech_block(self, number):
        """(cue line, last line) of the speech that holds this line, or None."""
        kind = self.type_of(number)
        if kind not in (CUE, CUE_WITH_SPEECH, DIALOGUE, PARENTHETICAL, LYRIC):
            return None
        start = number
        while start > self.first and self.type_of(start) not in (CUE, CUE_WITH_SPEECH):
            if self.type_of(start - 1) in (BLANK, None, ACTION, HEADING):
                return None
            start -= 1
        if self.type_of(start) not in (CUE, CUE_WITH_SPEECH):
            return None
        end = start
        while end + 1 <= self.last and self.type_of(end + 1) in (DIALOGUE, PARENTHETICAL, LYRIC):
            end += 1
        return start, end

    def speech_words(self, cue):
        block = self.speech_block(cue)
        if block is None:
            return 0
        start, end = block
        total = len(real_words(re.sub(r"^\S+[.:]\s*", "", self.line(start)))) if self.type_of(start) == CUE_WITH_SPEECH else 0
        return total + sum(len(self.words(number)) for number in range(start + 1, end + 1)
                           if self.type_of(number) != PARENTHETICAL)

    def find_quote(self, quote, first=None, last=None):
        """Every line in the scope that holds the quote, once per time it holds it."""
        first = self.first if first is None else first
        last = self.last if last is None else last
        wanted = normalise_quote(quote)
        found = []
        if not wanted:
            return found
        for number in range(max(first, self.first), min(last, self.last) + 1):
            found += [number] * normalise_quote(self.line(number)).count(wanted)
        return found

    def check_quote(self, quote, first=None, last=None):
        """A plain problem with one quoted string of an anchor (CITE-02), or None when it is found exactly once."""
        if len(real_words(quote)) < self.minimum_words:
            return f'"{quote}" has fewer than {self.minimum_words} words'
        found = self.find_quote(quote, first, last)
        if not found:
            return f'"{quote}" is not found in lines {first or self.first}-{last or self.last}'
        if len(found) > 1:
            shown = ", ".join(str(number) for number in sorted(set(found))[:5])
            return f'"{quote}" is found {len(found)} times (lines {shown})'
        return None

    def resolve_end(self, quote, first, last):
        found = self.find_quote(quote, first, last)
        if len(found) != 1:
            return None
        end = found[0]
        block = self.speech_block(end)
        if block:
            end = block[1]
        number = end + 1
        while number <= last:
            kind = self.type_of(number)
            if not self.line(number).strip():
                number += 1
                continue
            if kind in (CUE, CUE_WITH_SPEECH):
                block = self.speech_block(number)
                if block and self.speech_words(number) < self.minimum_words:
                    end = block[1]
                    number = block[1] + 1
                    continue
                break
            if len(self.words(number)) < self.minimum_words:
                end = number
                number += 1
                continue
            break
        return end

    def resolve_lines(self, value, first=None, last=None, end_first=None, end_last=None):
        """A lines value that is a quote anchor ("..." or "..." to "...") as (first, last) line numbers, or None."""
        quotes = parse_quote_anchor(value)
        if not quotes:
            numbers = parse_line_numbers(value) if value else None
            if numbers:
                return numbers[0][0], numbers[-1][1]
            return None
        first = self.first if first is None else first
        last = self.last if last is None else last
        found = self.find_quote(quotes[0], first, last)
        if len(found) != 1 or len(real_words(quotes[0])) < self.minimum_words:
            return None
        start = found[0]
        block = self.speech_block(start)
        if block and start != block[0]:
            start = block[0]
        closing = quotes[1] if len(quotes) > 1 else quotes[0]
        if len(quotes) > 1 and len(real_words(closing)) < self.minimum_words:
            return None
        end = self.resolve_end(closing, end_first or first, end_last or last)
        return None if end is None else (start, end)

    def resolve_line(self, quote, first=None, last=None):
        """A single-line reference: exactly the line that holds the quote, or None."""
        quotes = parse_quote_anchor(quote) or [quote]
        found = self.find_quote(quotes[0], first, last)
        return found[0] if len(found) == 1 and len(real_words(quotes[0])) >= self.minimum_words else None

    def resolve_story_point(self, value):
        """The line of a story point ('SC24 "She deletes the way home."') inside its scene, or None."""
        point = parse_story_point(value)
        if not point:
            return None
        scope = self.scope_of(point[0])
        if scope is None:
            return None
        return self.resolve_line(point[1], scope[0], scope[1])


def load_story_map(project_folder):
    path = Path(project_folder) / MACHINE_FOLDER / STORY_MAP_FILE
    if not path.is_file():
        return None
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


# ---------------------------------------------------------------- writing into a project

def original_story_path(project):
    """The story file stage.py new kept in Original/."""
    manifest = project.read_manifest()
    source = (manifest.get("source") or {}).get("file")
    if source and (project.folder / source).is_file():
        return project.folder / source
    folder = project.folder / ORIGINAL_FOLDER
    candidates = [path for path in sorted(folder.glob("*")) if path.is_file() and path.name != "fingerprint.txt"] \
        if folder.is_dir() else []
    if len(candidates) == 1:
        return candidates[0]
    if not candidates:
        raise StageStop('The project has no story in Original/. Start the project with: stage.py new "<story file>"')
    raise StageStop("Original/ holds more than one file, so the story is not clear. Leave only the story and "
                    "fingerprint.txt there.")


def numbered_story_text(reading, title):
    width = len(str(reading.last_line_number))
    fence_length = max([3] + [len(run) + 1 for line in reading.lines for run in re.findall(r"`{3,}", line)])
    fence = "`" * fence_length
    kind_words = {"catch_dialect": "a screenplay in The Catch's own layout", "fountain": "a Fountain screenplay",
                  "fdx": "a Final Draft screenplay", "docx": "a Word file", "epub": "an e-book",
                  "pdf_text": "a PDF", "markdown": "a Markdown file", "plain_text": "a plain text file"}
    lines = [f"# {title}: the story with line numbers", "",
             f'Made by the tools from "{reading.file_name}" ({kind_words.get(reading.source_format, "a text file")}), '
             "which is kept unchanged in Original. Every line has its number in front; the scene list, the speeches "
             "and the shots cite these numbers. This file is made again whenever the story is read, so do not "
             "change it.", "", fence + "text"]
    for offset, line in enumerate(reading.lines):
        number = reading.first_line_number + offset
        lines.append(f"{number:>{width}}  {line}".rstrip())
    lines += [fence, ""]
    return "\n".join(lines)


def replace_plain_part(record_file, new_lines):
    """Put new plain-part lines above the divider of a parsed record file (records stay byte for byte)."""
    for segment in record_file.segments:
        if isinstance(segment, TextBlock):
            for position, line in enumerate(segment.lines):
                if line.strip() == DIVIDER_LINE:
                    segment.lines[:position] = list(new_lines) + [""]
                    segment.line_numbers[:position] = [None] * (len(new_lines) + 1)
                    return True
    return False


def remove_records(record_file, type_name):
    before = len(record_file.segments)
    record_file.segments = [segment for segment in record_file.segments
                            if not (isinstance(segment, Record) and segment.type_name == type_name)]
    if len(record_file.segments) != before:
        record_file.records_removed = True


def open_or_new(project, name, plain_lines, what):
    path = project.folder / name
    if path.is_file():
        record_file = parse_file(path, name, project.schema)
        if not replace_plain_part(record_file, plain_lines):
            record_file.segments.insert(0, TextBlock(lines=list(plain_lines) + ["", DIVIDER_LINE, ""],
                                                     line_numbers=[None] * (len(plain_lines) + 3)))
        return record_file, True
    record_file = new_record_file(name, plain_lines, what)
    record_file.path = path
    return record_file, False


def scene_list_plain_part(reading):
    lines = ["# Scene list", "", "## At a glance", ""]
    estimate = reading.first_estimate or {}
    minutes = estimate.get("minutes") or [0, 0, 0]
    if reading.scenes:
        lines.append(f"{counted(len(reading.scenes), 'scene')}, one for each heading in the story, in "
                     f"{number_text(len(reading.lines))} numbered lines, with {counted(len(reading.speeches), 'speech')}. "
                     f"As written it runs about {minutes[1]} minutes ({minutes[0]} to {minutes[2]}), by the first "
                     "estimate from the words.")
    elif reading.source_kind == "prose":
        lines.append(f"No scenes yet: the book is planned first, and its scenes are listed here after that. The book "
                     f"has {counted(len(reading.chapters), 'chapter')} and {number_text(reading.words)} words in "
                     f"{number_text(len(reading.lines))} numbered lines.")
    else:
        lines.append(f"No scenes were found in {number_text(len(reading.lines))} numbered lines; see Lines to look at.")
    if reading.scenes:
        lines += ["", "## The scenes, one line each", ""]
        names = {character.identifier: name_for_people(character.cue_name) for character in reading.characters}
        for scene in reading.scenes:
            summary = speaking_summary([(names.get(speaker, speaker), count) for speaker, count in scene.speaking])
            endings = []
            if scene.transition_out != "cut":
                endings.append(f"ends with a {scene.transition_out.replace('_', ' ')}")
            for card in scene.cards:
                endings.append(f'the card "{card["text"]}", which becomes its own shot')
            ending = ("; " + " and ".join(endings)) if endings else ""
            lines.append(f'- {scene_words(scene)}, lines {scene.first} to {scene.last}, "{scene.heading}": '
                         f"{summary}{ending}.")
    lines += ["", "## Lines to look at", "",
              "The tools read these lines as shown. Confirm each one, or say what it really is."]
    report = odd_lines_report(reading)
    lines += report if report else ["Nothing odd: every line has its place."]
    return lines


def odd_lines_report(reading):
    return odd_lines_report_from_map(story_map_of(reading))


def odd_lines_report_from_map(story_map):
    """The odd-lines report as plain lines, from story map.json (so a view builder can write it again)."""
    entries = []
    for number, odd in enumerate(story_map.get("odd_lines", []), 1):
        first, last = odd["lines"]
        where = f"Line {first}" if first == last else f"Lines {first} to {last}"
        quoted = f', "{shorten_for_quote(odd["text"])}"' if odd.get("text") and odd["text"] not in (">",) else ""
        entries.append(f"{number}. {where}{quoted}: {odd['finding']}.")
    tokens = {}
    for scene in story_map.get("scenes", []):
        for token in scene.get("capitalised_words", []):
            tokens.setdefault(token["class"], {}).setdefault(token["text"], []).append(token["line"])
    labels = [("sound", "Sounds"), ("prop", "Things"), ("text", "Text in picture"),
              ("character", "People"), ("instruction", "Picture instructions"), ("emphasis", "Emphasis")]
    if tokens:
        entries += ["", "Words in capitals in the action, sorted by what the tools think they are:"]
        for key, label in labels:
            found = tokens.get(key)
            if not found:
                continue
            shown = ", ".join(f'"{text}" ({", ".join(str(line) for line in found_lines[:3])})'
                              for text, found_lines in found.items())
            entries.append(f"- {label}: {shown}.")
    people = story_map.get("people_without_speeches") or []
    if people:
        shown = ", ".join(f'"{person["name"]}" (line {person["line"]})' for person in people)
        entries += ["", f"People who never speak, named in capitals: {shown}. They are named as characters at step 5."]
    candidates = story_map.get("name_candidates") or []
    if candidates:
        shown = ", ".join(f'{candidate["name"]} ({candidate["count"]})' for candidate in candidates[:15])
        entries += ["", f"Names that appear most often, with how many times: {shown}. The characters are named at "
                        "step 5."]
    return entries


def story_plan_plain_part(reading):
    lines = ["# Story plan", "", "## At a glance", "",
             f"The book has {counted(len(reading.chapters), 'chapter')} and {number_text(reading.words)} words. The plan "
             "of the whole book comes next: how it becomes a film.", "", "## The chapters, one line each", ""]
    for chapter in reading.chapters:
        lines.append(f'- chapter {chapter.identifier[2:].lstrip("0")}, "{chapter.title}": lines {chapter.first} to '
                     f"{chapter.last}, {number_text(chapter.words)} words.")
    return lines


def characters_plain_part(reading):
    lines = ["# Characters and voices", "", "## At a glance", ""]
    speaking = [character for character in reading.characters]
    lines.append(f"{counted(len(speaking), 'person')} speak in the story. Their descriptions and voices come at step 5 "
                 "of 12 (characters, places and things).")
    lines += ["", "## The people, one line each", ""]
    for character in sorted(speaking, key=lambda character: -character.cues):
        other = [name for name in character.names if name != character.cue_name]
        also = f'; also called "{", ".join(other)}"' if other else ""
        lines.append(f"- {name_for_people(character.cue_name)}: speaks {character.cues} times, first at line "
                     f"{character.first_line}{also}.")
    return lines


def next_choice_number(records):
    numbers = [int(record.identifier.split("-")[1]) for record in records
               if record.type_name == "CHOICE" and record.identifier and re.fullmatch(r"CHOICE-\d{3}", record.identifier)]
    return (max(numbers) if numbers else 0) + 1


def format_choice_record(identifier, reading, constants):
    short_max = constant(constants, "short_runtime_max_s", 2400)
    minutes = short_max // 60
    estimate = reading.first_estimate or {}
    central = estimate.get("central_s", 0)
    short = central < short_max
    if not estimate.get("rough"):
        low, middle, high = estimate.get("minutes", [0, 0, 0])
        reason = (f"the first estimate from the words is about {middle} minutes ({low} to {high}), "
                  + (f"under {minutes} minutes" if short else f"over {minutes} minutes"))
        checkpoint = "a"
    else:
        reason = (f"the book has {number_text(reading.words)} words; the plan of the whole book may change this"
                  if not short else f"the story is short ({number_text(reading.words)} words)")
        checkpoint = "a" if reading.scenes else "p"
    letter = "a" if short else "b"
    fields = [
        ("question", "What kind of film is this: a short film or a feature?"),
        ("why", "The kind of film sets the budgets that differ for short films and features, such as how often the "
                "film may use its saved choices."),
        ("option", f"a | text: A short film ({minutes} minutes or less)"),
        ("option", f"b | text: A feature film (over {minutes} minutes)"),
        ("option", "c | text: A limited series of episodes"),
        ("default", f"{letter} | reason: {reason}"),
        ("answer", letter), ("asked", "no"), ("checkpoint", checkpoint), ("affects", "PROJECT.format"),
        ("sets", "PROJECT.format | value: short | when: a"), ("sets", "PROJECT.format | value: feature | when: b"),
        ("sets", "PROJECT.format | value: limited_series | when: c"), ("based_on", "D2 §3.3; D13 §4.1"),
        ("status", "defaulted"), ("date", today()), ("locked", "no"),
    ]
    return make_record("CHOICE", identifier, "Format", fields), ("short" if short else "feature")


def length_choice_record(identifier, reading):
    low, middle, high = (reading.first_estimate or {}).get("minutes", [0, 0, 0])
    fields = [
        ("question", f"Length: as written it runs about {middle} minutes ({low} to {high}). Keep everything, or give "
                     "me a target?"),
        ("why", "A shorter target means the plan trims, merges or cuts scenes; the story's lines are never rewritten."),
        ("option", f"a | text: Keep everything, about {middle} minutes as written"),
        ("option", "b | text: A shorter film: tell me the target in minutes"),
        ("default", "a | reason: nothing is lost, and a shorter film can still be asked for later"),
        ("answer", "open"), ("asked", "yes"), ("checkpoint", "a"),
        ("affects", "PROJECT.runtime_target_s, PROJECT.scope"),
        ("sets", "PROJECT.runtime_target_s | value: as_written | when: a"),
        ("sets", "PROJECT.scope | value: all | when: a"),
        ("sets", f"{identifier}-B | when: b"),
        ("sets", "PROJECT.scope | value: all | when: b"),
        ("based_on", "K25; D13 §4.1"), ("status", "open"), ("date", "none"), ("locked", "no"),
    ]
    record = make_record("CHOICE", identifier, "Length", fields)
    record.add_note(f"For b, write SETVALUE {identifier}-B with - target: PROJECT and - runtime_target_s: <the target "
                    "in seconds> in the same inbox as the answer. Once this choice is answered or defaulted the scene "
                    "numbers are fixed: stage.py read will not number the scenes again.")
    return record


def scene_record(scene, reading):
    fields = [("heading", scene.heading), ("int_ext", scene.int_ext), ("place_text", scene.place_text),
              ("time_text", scene.time_text), ("lines", f"{scene.first}-{scene.last}"),
              ("characters", ", ".join(scene.characters) if scene.characters else "none")]
    fields += [("speaking", f"{speaker} | cues: {count}") for speaker, count in scene.speaking]
    if not scene.speaking:
        fields.append(("speaking", "none"))
    fields += [("transition_in", scene.transition_in), ("transition_out", scene.transition_out),
               ("presentation", scene.presentation)]
    if scene.presentation in ("on_screen", "recording"):
        fields.append(("host", "open"))
    fields += [("origin", "story"), ("status", "draft"), ("locked", "no")]
    record = make_record("SCENE", scene.identifier, scene.title, fields)
    for note in scene.notes:
        record.add_note(note)
    return record


def chapter_record(chapter):
    fields = [("title", chapter.title), ("lines", f"{chapter.first}-{chapter.last}"), ("words", chapter.words),
              ("status", "draft"), ("locked", "no")]
    return make_record("CHAPTER", chapter.identifier, chapter.title, fields)


def character_record(character):
    return make_record("CHARACTER", character.identifier, name_for_people(character.cue_name),
                       [("names", ", ".join(character.names)), ("status", "draft"), ("locked", "no")])


def ids_are_fixed(project, record_files, manifest):
    """Why the scene or chapter numbers may no longer change, or None (step 1's redo rule)."""
    merged, _ = merge_copies(record_files, project.schema)
    length_choice = (manifest.get("story") or {}).get("length_choice")
    if length_choice:
        choice = merged.get(("CHOICE", length_choice))
        if choice is not None and normalise_word(choice.get("status") or "open") in ("answered", "defaulted"):
            return "the length choice at the scene list has been answered, which fixed the scene numbers"
    written_by_read = {"SCENE": {"heading", "int_ext", "place_text", "time_text", "lines", "characters", "speaking",
                                 "transition_in", "transition_out", "presentation", "host", "origin", "status",
                                 "locked", "note"},
                       "CHAPTER": {"title", "lines", "words", "status", "locked", "note", "first_line", "last_line"}}
    for key, record in merged.items():
        if key[0] not in written_by_read:
            continue
        if normalise_word(record.get("locked") or "no") == "yes":
            return f"{key[1]} is locked"
        extra = [name for name in record.field_names() if name not in written_by_read[key[0]]]
        if extra:
            return f"{key[1]} already has later work in it ({', '.join(extra[:3])})"
    return None


def read_into_project(project, context=None, story_path=None, write_records=True):
    """Read the project's story and write what step 1 makes (blueprint 3 step 1). Returns (reading, files written,
    summary). With write_records=False (for adopt, whose folder already holds the AI's scene list) only the numbered
    story, speeches.json and story map.json are written, and the scene numbers are not checked against a lock."""
    schema = project.schema
    constants = context.constants if context is not None else None
    if constants is None:
        from .record_format import load_skill_data
        _, _, constants = load_skill_data()
    story_path = Path(story_path) if story_path else original_story_path(project)
    record_files = project.load_record_files()
    manifest = project.read_manifest()
    project_file = next((record_file for record_file in record_files if record_file.name == START_HERE), None)
    project_record = next((record for record in (project_file.records if project_file else [])
                           if record.type_name == "PROJECT"), None)
    if project_record is None:
        raise StageStop(f'The project has no PROJECT record in "{START_HERE}". Start it with: stage.py new "<story file>"')
    fingerprint = fingerprint_of_file(story_path)
    stored_fingerprint = project_record.get("source_fingerprint")
    if write_records and stored_fingerprint and stored_fingerprint not in ("none", "open") \
            and stored_fingerprint != fingerprint:
        raise StageStop("The story in Original is not the one this project started from (its fingerprint differs). "
                        "Start a new project for a changed story.")
    fixed = ids_are_fixed(project, record_files, manifest) if write_records else None
    if fixed:
        raise StageStop(f"The story was already read and {fixed}. Scenes are never numbered again after that: an "
                        "inserted scene takes a letter (scene 6A) and a removed one is marked omitted.")
    reading = read_story_lines(load_story_file(story_path), constants)
    history = history_run_folder(project)
    written = []

    def keep(name):
        path = project.folder / name
        if path.is_file():
            keep_in_history(history, path, name)

    title = project_record.get("title") or project.folder.name
    # 03 Story - numbered
    keep(NUMBERED_STORY_FILE)
    (project.folder / NUMBERED_STORY_FILE).write_text(numbered_story_text(reading, title), encoding="utf-8")
    written.append(NUMBERED_STORY_FILE)

    format_identifier = length_identifier = None
    story_state = manifest.get("story") or {}
    if write_records:
        # 04 Scene list: the scene records (screenplays) and the odd-lines report above the divider
        scene_file, _ = open_or_new(project, SCENE_LIST_FILE, scene_list_plain_part(reading), "Scene list")
        earlier = {record.identifier: record for record in scene_file.records if record.type_name == "SCENE"}
        remove_records(scene_file, "SCENE")
        for scene in reading.scenes:
            record = scene_record(scene, reading)
            carry_ai_fields(earlier.get(scene.identifier), record, ("presentation", "host", "origin"), schema)
            add_record(scene_file, record, schema, project.type_order_for(SCENE_LIST_FILE))
        ensure_end_line(scene_file, "Scene list")
        scene_file.records_removed = True
        keep(SCENE_LIST_FILE)
        write_file(scene_file, project.folder / SCENE_LIST_FILE, schema)
        written.append(SCENE_LIST_FILE)

        # 05 Story plan: chapter stubs (prose)
        if reading.chapters:
            plan_file, _ = open_or_new(project, STORY_PLAN_FILE, story_plan_plain_part(reading), "Story plan")
            earlier = {record.identifier: record for record in plan_file.records if record.type_name == "CHAPTER"}
            remove_records(plan_file, "CHAPTER")
            for chapter in reading.chapters:
                record = chapter_record(chapter)
                carry_ai_fields(earlier.get(chapter.identifier), record, ("first_line", "last_line"), schema)
                add_record(plan_file, record, schema, project.type_order_for(STORY_PLAN_FILE))
            ensure_end_line(plan_file, "Story plan")
            plan_file.records_removed = True
            keep(STORY_PLAN_FILE)
            write_file(plan_file, project.folder / STORY_PLAN_FILE, schema)
            written.append(STORY_PLAN_FILE)

        # 07 Characters and voices: character stubs (ID and names) for every cue
        if reading.characters:
            character_file, _ = open_or_new(project, CHARACTERS_FILE, characters_plain_part(reading), "Characters and voices")
            for character in reading.characters:
                existing = character_file.find("CHARACTER", character.identifier)
                if existing is None:
                    add_record(character_file, character_record(character), schema, project.type_order_for(CHARACTERS_FILE))
                elif normalise_word(existing.get("locked") or "no") != "yes":
                    existing.set_field("names", ", ".join(character.names), schema)
            ensure_end_line(character_file, "Characters and voices")
            keep(CHARACTERS_FILE)
            write_file(character_file, project.folder / CHARACTERS_FILE, schema)
            written.append(CHARACTERS_FILE)

        # 01 Choices: the format choice (asked: no, defaulted) and, for a screenplay, the length question
        choices_path = project.folder / CHOICES_FILE
        if choices_path.is_file():
            choices_file = parse_file(choices_path, CHOICES_FILE, schema)
        else:
            choices_file = new_record_file(CHOICES_FILE, ["# Choices"], "Choices")
        format_identifier = story_state.get("format_choice")
        if not format_identifier or choices_file.find("CHOICE", format_identifier) is None:
            number = next_choice_number(choices_file.records)
            format_identifier = "CHOICE-004" if number <= 4 else f"CHOICE-{number:03d}"
        format_record, format_value = format_choice_record(format_identifier, reading, constants)
        existing_format = choices_file.find("CHOICE", format_identifier)
        if existing_format is not None and normalise_word(existing_format.get("status") or "") == "answered":
            format_value = None
        else:
            remove_record(choices_file, "CHOICE", format_identifier)
            add_record(choices_file, format_record, schema, project.type_order_for(CHOICES_FILE))
        length_identifier = None
        if reading.source_kind in ("screenplay", "treatment", "stage_play", "comic_script") and reading.scenes:
            length_identifier = story_state.get("length_choice")
            if not length_identifier or choices_file.find("CHOICE", length_identifier) is None:
                length_identifier = f"CHOICE-{next_choice_number(choices_file.records):03d}"
            remove_record(choices_file, "CHOICE", length_identifier)
            add_record(choices_file, length_choice_record(length_identifier, reading), schema,
                       project.type_order_for(CHOICES_FILE))
        ensure_end_line(choices_file, "Choices")
        format_number = int(format_identifier.split("-")[1])
        kind_words = {"short": "a short film", "feature": "a feature film", None: "as you answered"}
        small_line = (f"- The kind of film: {kind_words.get(format_value, format_value)}, from the first estimate "
                      f"(choice {format_number}).")
        waiting_line = None
        if length_identifier:
            low, middle, high = (reading.first_estimate or {}).get("minutes", [0, 0, 0])
            waiting_line = (f"Length: as written it runs about {middle} minutes ({low} to {high}). Keep everything, or "
                            f"give me a target? If you say nothing: keep everything (choice {int(length_identifier.split('-')[1])}).")
        note_choices_in_plain_part(choices_file, waiting_line, small_line,
                                   [format_number] + ([int(length_identifier.split("-")[1])] if length_identifier else []))
        keep(CHOICES_FILE)
        write_file(choices_file, choices_path, schema)
        written.append(CHOICES_FILE)

        # 00 Start here: the PROJECT fields step 1 fills
        story_title = reading.title
        if story_title and title == fallback_title_from_file_name(story_path):
            project_record.set_field("title", clean_title(story_title), schema)
        project_record.set_field("source_kind", reading.source_kind, schema)
        project_record.set_field("source_format", reading.source_format, schema)
        project_record.set_field("language", reading.language, schema)
        if format_value:
            project_record.set_field("format", format_value, schema)
        if not project_record.get("runtime_target_s"):
            project_record.set_field("runtime_target_s", "open", schema)
        project_record.set_field("scene_id_digits", str(reading.scene_id_digits), schema)
        keep(START_HERE)
        write_file(project_file, project.folder / START_HERE, schema)
        written.append(START_HERE)

    # For machines: speeches.json and story map.json
    machine = project.machine_folder
    machine.mkdir(parents=True, exist_ok=True)
    relative_source = story_path.relative_to(project.folder).as_posix() if project.folder in story_path.parents else story_path.name
    outputs = [(STORY_MAP_FILE, story_map_of(reading, relative_source, fingerprint))]
    if reading.scenes or reading.speeches:
        outputs.insert(0, (SPEECHES_FILE, speeches_json(reading)))
    for name, data in outputs:
        path = machine / name
        if path.is_file():
            keep_in_history(history, path, f"{MACHINE_FOLDER}/{name}")
        temporary = path.with_suffix(".part")
        with open(temporary, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=1, ensure_ascii=False)
            handle.write("\n")
        os.replace(temporary, path)
        written.append(f"{MACHINE_FOLDER}/{name}")

    # The manifest and the log
    manifest = project.read_manifest()
    manifest["story"] = {**story_state, "read": now(), "file": relative_source, "fingerprint": fingerprint,
                         "format": reading.source_format, "kind": reading.source_kind, "lines": len(reading.lines),
                         "words": reading.words, "scenes": len(reading.scenes), "chapters": len(reading.chapters),
                         "speeches": len(reading.speeches), "story_map": f"{MACHINE_FOLDER}/{STORY_MAP_FILE}",
                         "speeches_file": f"{MACHINE_FOLDER}/{SPEECHES_FILE}",
                         "format_choice": format_identifier or story_state.get("format_choice"),
                         "length_choice": length_identifier or story_state.get("length_choice"),
                         "first_estimate": reading.first_estimate}
    project.write_manifest(project.refresh_manifest(manifest))
    if reading.scenes:
        summary = (f"{counted(len(reading.scenes), 'scene')}, {counted(len(reading.speeches), 'speech')}, "
                   f"{number_text(len(reading.lines))} numbered lines")
    elif reading.chapters:
        summary = (f"{counted(len(reading.chapters), 'chapter')}, {number_text(reading.words)} words, "
                   f"{number_text(len(reading.lines))} numbered lines")
    else:
        summary = f"{number_text(len(reading.lines))} numbered lines"
    project.add_log_entry(f"Read the story: {summary}." if write_records else
                          f"Numbered the story again from the story file: {summary}.")
    written += write_first_estimate_file(project)
    return reading, written, summary


def write_first_estimate_file(project):
    """14 Time and cost holds the first estimate (step 1). estimate.py (work package 7) writes it: when that module
    offers write_first_estimate(project_folder), it is called here; otherwise the estimate stays in story map.json."""
    try:
        from . import estimate
    except ImportError:
        return []
    writer = getattr(estimate, "write_first_estimate", None)
    if writer is None:
        return []
    writer(project.folder)
    return ["14 Time and cost.md"]


def note_choices_in_plain_part(record_file, waiting_line, small_line, numbers):
    """Name the new choices in the plain part of 01 Choices (under Waiting for you and Small choices I made), so the
    user sees them before the views are built again. Lines from an earlier reading are replaced."""
    block = next((segment for segment in record_file.segments if isinstance(segment, TextBlock)
                  and any(line.strip() == DIVIDER_LINE for line in segment.lines)), None)
    if block is None:
        return
    marks = tuple(f"(choice {number})." for number in numbers)
    kept = [(line, number) for line, number in zip(block.lines, block.line_numbers) if not line.rstrip().endswith(marks)]
    block.lines = [line for line, _ in kept]
    block.line_numbers = [number for _, number in kept]

    def insert_after_heading(heading, text, numbered):
        position = next((index for index, line in enumerate(block.lines) if line.strip() == heading), None)
        if position is None:
            return
        end = position + 1
        while end < len(block.lines) and block.lines[end].strip() and not block.lines[end].startswith("#") \
                and block.lines[end].strip() != DIVIDER_LINE:
            end += 1
        if numbered:
            count = sum(1 for line in block.lines[position + 1:end] if re.match(r"^\d+\.", line))
            text = f"{count + 1}. {text}"
        block.lines.insert(end, text)
        block.line_numbers.insert(end, None)

    if waiting_line:
        insert_after_heading("## Waiting for you", waiting_line, True)
    if small_line:
        insert_after_heading("## Small choices I made", small_line, False)


def carry_ai_fields(earlier, record, names, schema):
    """On a second reading, keep what the AI already wrote on a scene or chapter whose lines did not change."""
    if earlier is None or earlier.get("lines") != record.get("lines"):
        return
    for name in names:
        values = earlier.get_all(name)
        if values:
            record.set_items(name, values, schema)


def remove_record(record_file, type_name, identifier):
    before = len(record_file.segments)
    record_file.segments = [segment for segment in record_file.segments
                            if not (isinstance(segment, Record) and segment.type_name == type_name
                                    and segment.identifier == identifier)]
    if len(record_file.segments) != before:
        record_file.records_removed = True


# ---------------------------------------------------------------- the commands

def add_read_arguments(parser):
    pass


def run_read(context):
    project = Project(context.project, context.schema, context.words)
    with project.lock():
        reading, written, summary = read_into_project(project, context)
    kind_words = {"catch_dialect": "a screenplay in The Catch's own layout", "fountain": "a Fountain screenplay",
                  "fdx": "a Final Draft file", "docx": "a Word file", "epub": "an e-book", "pdf_text": "a PDF",
                  "markdown": "a Markdown file", "plain_text": "a plain text file"}
    context.say(f"Read {kind_words.get(reading.source_format, 'the story')} ({reading.source_kind.replace('_', ' ')}): "
                f"{summary}" + ("" if reading.chapters else f", {number_text(reading.words)} words") + ".")
    if reading.scenes:
        names = {character.identifier: name_for_people(character.cue_name) for character in reading.characters}
        example = max(reading.scenes, key=lambda scene: (len(scene.cards), len(scene.speeches)))
        context.say(f"Found {counted(len(reading.scenes), 'scene')}, one for each heading, and "
                    f"{counted(len(reading.speeches), 'speech')} by {counted(len(reading.characters), 'character')}. "
                    f"Example: {scene_words(example)} is lines {example.first} to {example.last}; "
                    + speaking_summary([(names.get(s, s), c) for s, c in example.speaking]) + ".")
        estimate = reading.first_estimate or {}
        low, middle, high = estimate.get("minutes", [0, 0, 0])
        context.say(f"First estimate: about {middle} minutes as written ({low} to {high}).")
    elif reading.chapters:
        context.say(f"Found {counted(len(reading.chapters), 'chapter')} and {number_text(reading.words)} words; the "
                    "plan of the whole book comes next.")
    context.say(f"Lines to look at: {len(reading.odd_lines)}, listed in {SCENE_LIST_FILE[:-3]} under Lines to look at.")
    context.say("Made: " + ", ".join(name[:-3] if name.endswith(".md") else name for name in written) + ".")
    context.say("Next: the AI reads the lines to look at and confirms or corrects them (unit U-01-ODDLINES), then "
                "stage.py check --step 1.")
    context.summary = f"read: {summary}"
    return 0


def add_lines_arguments(parser):
    parser.add_argument("element", help="an ID (CH-IONA, PR-FLASK, SC10, SC10-D11) or words in quotes")
    parser.add_argument("--more", action="store_true", help="list every line, with no cap")


def names_for_element(project, identifier, story_map):
    """The names to look for: a record's names (or TEXT words), or the words given."""
    record_files = project.load_record_files()
    merged, _ = merge_copies(record_files, project.schema)
    record = next((record for key, record in merged.items() if key[1] == identifier), None)
    if record is None:
        for character in story_map.get("characters", []):
            if character["id"] == identifier:
                return character["names"], name_for_people(character["cue"])
        return None, None
    names = []
    for field_name in ("names", "headings"):
        for value in record.get_all(field_name):
            names += split_list(value)
    if record.type_name == "TEXT" and record.get("words"):
        names.append(record.get("words").strip('"'))
    if not names and record.title:
        names.append(record.title)
    return [name for name in names if name and name.lower() not in ("none", "open")], record.title or identifier


def run_lines(context):
    project = Project(context.project, context.schema, context.words)
    story_map = load_story_map(project.folder)
    if story_map is None:
        raise StageStop("The story has not been read yet. Run: stage.py read")
    story = NumberedStory.from_story_map(story_map)
    element = context.arguments.element.strip()
    speeches = []
    if re.fullmatch(r"SC\d{2,3}[A-Z]?", element) and story.scope_of(element):
        first, last = story.scope_of(element)
        for number in range(first, last + 1):
            context.say(f"{number:>5}  {story.line(number)}".rstrip())
        context.summary = f"lines of {element}"
        return 0
    if re.fullmatch(r"CP\d{2}", element) and story.scope_of(element):
        first, last = story.scope_of(element)
        for number in range(first, last + 1):
            context.say(f"{number:>5}  {story.line(number)}".rstrip())
        context.summary = f"lines of {element}"
        return 0
    if re.fullmatch(r"SC\d{2,3}[A-Z]?-D\d{2,3}", element):
        path = project.machine_folder / SPEECHES_FILE
        if path.is_file():
            with open(path, encoding="utf-8") as handle:
                speeches = json.load(handle).get("speeches", [])
        speech = next((speech for speech in speeches if speech["id"] == element), None)
        if speech is None:
            raise StageStop(f"No speech {element} in this story. Speeches are numbered in cue order in each scene.")
        for number in range(speech["lines"][0], speech["lines"][1] + 1):
            context.say(f"{number:>5}  {story.line(number)}".rstrip())
        return 0
    if re.fullmatch(r"[A-Z]{2,4}-[A-Z0-9-]+|[A-Z]+-\d+", element):
        names, label = names_for_element(project, element, story_map)
        if names is None:
            raise StageStop(f"No record {element} in this project, so there are no names to look for. Give the ID of "
                            "a character, place, thing or text, or the words to look for in quotes.")
    else:
        names, label = [element], element
    if not names:
        raise StageStop(f"{element} has no names to look for yet (its names field is empty).")
    pattern = re.compile(r"(?<![\w])(" + "|".join(re.escape(name) for name in sorted(set(names), key=len, reverse=True))
                         + r")(?![\w])", re.IGNORECASE)
    types = story_map.get("line_types") or []
    scenes = story_map.get("scenes") or story_map.get("chapters") or []
    cap = constant(context.constants, "alias_mentions_cap", 400)
    hits = []
    cue_count = 0
    for offset, line in enumerate(story.lines):
        number = story.first + offset
        kind = types[offset] if offset < len(types) else None
        if not pattern.search(line):
            continue
        if kind in (CUE,):
            cue_count += 1
            continue
        hits.append(number)
    shown = hits if context.arguments.more else hits[:cap]
    extra = []
    if not context.arguments.more and len(hits) > cap:
        extra = [number for number in hits[cap:]
                 if any(word.lower() in PHYSICAL_NOUNS for word in re.findall(r"[A-Za-z]+", story.line(number)))]
    listed = sorted(set(shown + extra))
    context.say(f'Lines that mention {label} (names: {", ".join(names)}): {counted(len(hits), "line")}'
                + (f"; its {counted(cue_count, 'speech')} are in speeches.json and not listed" if cue_count else "") + ".")
    current = None
    for number in listed:
        part = next((entry for entry in scenes if entry["lines"][0] <= number <= entry["lines"][1]), None)
        label_part = part["id"] if part else None
        if label_part != current:
            current = label_part
            if part:
                words = scene_words_of(part["id"]) if part["id"].startswith("SC") else f'chapter "{part.get("title")}"'
                context.say(f"{words[:1].upper() + words[1:]} (lines {part['lines'][0]} to {part['lines'][1]}):")
        context.say(f"{number:>5}  {story.line(number)}".rstrip())
    if len(listed) < len(hits):
        context.say(f"Shown: {len(listed)} of {len(hits)} lines (the first {cap}, plus every later line that names "
                    "something one can see). Add --more to see every line.")
    context.summary = f"lines for {element}: {len(hits)}"
    return 0


def add_selftest_arguments(parser):
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prepare", action="store_true", help="issue the test shot IDs and write the handout")
    group.add_argument("--score", action="store_true", help="score the AI's test shots and set the batch size")
    parser.add_argument("--surface", choices=["claude_code", "claude_cowork", "claude_web", "chatgpt", "gemini", "other"],
                        help="with --score: the app this runs in, which the project records (default: found from the "
                             "environment); for example selftest --score --surface claude_code")


def plural_words(count, word):
    return f"{count} {word}" if count == 1 else f"{count} {word}s"


def zip_round_trip():
    """Whether code can make a ZIP here and read it back unchanged (the self-test, step 0)."""
    try:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.zip"
            content = "Kitchen.\nNot mint.\n" * 20
            with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("test/story.txt", content)
            with zipfile.ZipFile(path) as archive:
                return archive.read("test/story.txt").decode("utf-8") == content
    except (OSError, zipfile.BadZipFile, RuntimeError):
        return False


def selftest_identifiers(project_record, story_map, constants):
    scenes = {scene["id"] for scene in (story_map or {}).get("scenes", [])}
    digits = int(project_record.get("scene_id_digits") or (story_map or {}).get("scene_id_digits") or 2)
    names = constant(constants, "selftest_scene", {"two_digit_ids": "SC99", "three_digit_ids": "SC999"})
    scene = names["three_digit_ids"] if digits == 3 else names["two_digit_ids"]
    number = int(scene[2:])
    while scene in scenes and number > 1:
        number -= 1
        scene = f"SC{number:0{digits}d}"
    count = constant(constants, "selftest_records", 20)
    step = constant(constants, "shot_number_step", 10)
    return scene, [f"{scene}-SH{step * position:03d}" for position in range(1, count + 1)]


def shot_template(skill_folder):
    path = Path(skill_folder) / "templates" / "11 Scene.md"
    if not path.is_file():
        return "### SHOT <ID> <a short plain title>\n(the SHOT template is missing from this copy of the skill)"
    lines = path.read_text(encoding="utf-8").splitlines()
    start = next((index for index, line in enumerate(lines) if line.startswith("### SHOT ")), None)
    if start is None:
        return ""
    end = start + 1
    while end < len(lines) and not lines[end].startswith("### ") and not lines[end].startswith("END OF FILE"):
        end += 1
    return "\n".join(lines[start:end]).rstrip()


SELFTEST_ERRORS_FILE = "selftest errors.txt"
# Conditions of SHOT fields as the self-test's invented scene meets them: a live, filmed shot in a room with no floor
# plan, no glass, no fact to hide and no saved choice.
SELFTEST_CONDITIONS = {"filmed_shot": True}
SELFTEST_CONDITION_WORDS = {
    "glass_in_frame": "a glass surface is in frame", "fact_element_before_reveal": "a secret's element is in frame "
    "before its reveal", "reserved_choice": "a saved choice is used", "overlapping_slices": "the scene overlaps time "
    "slices", "when_used": "the thing it records happens", "eyeline_set": "the item has an eyeline",
    "subject_moves": "the person moves in the frame", "later_beat_saves_behaviour": "a later beat saves a behaviour",
    "set_plan_exists": "the place has a floor plan",
}


def selftest_issued_ids(scene):
    """The IDs a test shot may cite (C9): they need not exist, but each has the right form."""
    return {"beats": [f"{scene}-B0{number}" for number in range(1, 6)],
            "setups": [f"{scene}-SU0{number}" for number in range(1, 4)],
            "speeches": [f"{scene}-D0{number}" for number in range(1, 5)],
            "characters": ["CH-A", "CH-B"], "states": ["CH-A.S01", "CH-B.S01", "PR-CUP.S01"],
            "things": ["PR-CUP", "PR-LAMP"], "lines": ["line:1", "line:2"]}


def selftest_shot_template(schema, skill_folder, scene):
    """The SHOT template of the self-test's handout (C9): every field in order, each marked required, required only
    when something holds, or left out, for a live shot at standard depth in the invented scene."""
    placeholders = {}
    for line in shot_template(skill_folder).splitlines():
        match = re.match(r"^- ([a-z_]+): (.*)$", line)
        if match:
            placeholders[match.group(1)] = match.group(2)
    lines = [f"### SHOT {scene}-SH010 <a short plain title>"]
    allowed = []
    for definition in schema.record_types["SHOT"]["fields"]:
        name = definition["name"]
        writers = schema.writers(definition)
        if definition.get("stored") is False or not writers or any(writer != "ai" for writer in writers):
            continue
        depth = definition.get("depth", "o")
        if depth not in ("q", "s"):
            continue
        condition = definition.get("required_when")
        placeholder = placeholders.get(name, "<value>")
        if not condition or SELFTEST_CONDITIONS.get(condition):
            mark = "REQUIRED"
            if definition.get("repeat") or "none" in (definition.get("also_allowed") or []):
                mark += "; write none when there is nothing"
            if definition.get("repeat"):
                mark += "; one line for each"
        else:
            mark = f"only when {SELFTEST_CONDITION_WORDS.get(condition, condition.replace('_', ' '))}; else leave it out"
        parts = [entry for entry in definition.get("sub_parts") or [] if entry.get("depth") in ("q", "s")]
        if parts:
            needed = []
            for entry in parts:
                when = entry.get("required_when") or entry.get("required_when_not")
                if not when:
                    needed.append(entry["key"])
                elif entry.get("required_when_not") == "set_plan_exists":
                    needed.append(entry["key"])  # the invented room has no floor plan
                else:
                    needed.append(f"{entry['key']} (only when {SELFTEST_CONDITION_WORDS.get(when, when)})")
            mark += "; every item needs these parts: " + ", ".join(needed)
        lines.append(f"- {name}: {placeholder}   [{mark}]")
        values = [str(value) for value in (definition.get("values") or [])]
        first_values = [str(value) for value in ((definition.get("first_part") or {}).get("values") or [])]
        if values or first_values:
            allowed.append(f"> - {name}: {', '.join(values or first_values)}")
        for entry in parts:
            if entry.get("values"):
                allowed.append(f"> - {name} {entry['key']}: {', '.join(str(value) for value in entry['values'])}")
    if allowed:
        lines += ["", "> Allowed values (\"one word from the note\" means one of these):"] + allowed
    return "\n".join(lines)


def run_selftest(context):
    project = Project(context.project, context.schema, context.words)
    record_file = parse_file(project.folder / START_HERE, START_HERE, project.schema)
    project_record = next((record for record in record_file.records if record.type_name == "PROJECT"), None)
    if project_record is None:
        raise StageStop(f'The project has no PROJECT record in "{START_HERE}".')
    story_map = load_story_map(project.folder)
    scene, identifiers = selftest_identifiers(project_record, story_map, context.constants)
    inbox = project.inbox_folder / f"{SELFTEST_UNIT}.md"
    if context.arguments.prepare:
        return prepare_selftest(context, project, story_map, scene, identifiers, inbox)
    return score_selftest(context, project, record_file, project_record, identifiers, inbox)


def prepare_selftest(context, project, story_map, scene, identifiers, inbox):
    if story_map is not None:
        story_lines = story_map["line_count"]
    else:
        story_lines = len(load_story_file(original_story_path(project)).lines)
    zip_ok = zip_round_trip()
    handout = project.machine_folder / "handouts" / f"{SELFTEST_UNIT}.md"
    handout.parent.mkdir(parents=True, exist_ok=True)
    task = (f"Write {len(identifiers)} full SHOT records, {identifiers[0]} to {identifiers[-1]}, and the END line, "
            f"in one reply, to {MACHINE_FOLDER}/inbox/{SELFTEST_UNIT}.md.")
    issued = selftest_issued_ids(scene)
    example = ""
    example_path = Path(context.skill_folder) / "examples" / "01 The Catch - scene 10.md"
    if example_path.is_file():
        text = example_path.read_text(encoding="utf-8").splitlines()
        start = next((index for index, line in enumerate(text) if line.startswith("### SHOT SC10-SH150")), None)
        if start is not None:
            end = start + 1
            while end < len(text) and not text[end].startswith("###") and text[end].strip() != "---":
                end += 1
            example = "\n".join(text[start:end]).rstrip()
    body = [f"# Handout {SELFTEST_UNIT}: the app self-test", "", f"Your one-line task: {task}", "",
            "This test is not shown to the user. It checks that this app can write a full batch of shots in one reply.",
            "", "## Rules", "",
            f"1. Invent one simple scene: two people at a kitchen table at night. It is scene {scene[2:]}, which the "
            "story does not use.",
            f"2. Write exactly {len(identifiers)} SHOT records with these IDs, in this order: {', '.join(identifiers)}.",
            "3. Fill every field the template below marks REQUIRED, with every part it names; write none in a "
            "repeated field when there is nothing (no thing in frame: thing: none). Leave out the fields it marks "
            "\"only when\" unless that holds.",
            "4. Cite only these IDs (they need not exist, but copy them exactly): "
            + "; ".join(f"{kind} {', '.join(values)}" for kind, values in issued.items()) + ".",
            "5. Leave out status, locked and every field code works out.",
            f"6. End the file with exactly this line: END OF FILE | Self-test shots | {len(identifiers)} records",
            "7. Never shorten: no \"...\", no \"same as above\", no \"etc.\".", "",
            "## The SHOT template, marked for this test", "",
            selftest_shot_template(context.schema, context.skill_folder, scene), ""]
    if example:
        body += ["## A finished shot, for its form only", "", example, ""]
    body += [f"Your one-line task, again: {task}", ""]
    handout.write_text("\n".join(body), encoding="utf-8")
    manifest = project.read_manifest()
    manifest["selftest"] = {"prepared": now(), "scene": scene, "shots": [identifiers[0], identifiers[-1]],
                            "count": len(identifiers), "story_lines": story_lines, "zip_round_trip": zip_ok,
                            "handout": f"{MACHINE_FOLDER}/handouts/{SELFTEST_UNIT}.md"}
    project.write_manifest(manifest)
    context.say(f"Self-test ready. The story has {number_text(story_lines)} lines. Saving the project as one ZIP "
                + ("works here." if zip_ok else "does NOT work here: save files one by one."))
    context.say(f"Issued {len(identifiers)} test shots, {identifiers[0]} to {identifiers[-1]}. Handout: "
                f"{MACHINE_FOLDER}/handouts/{SELFTEST_UNIT}.md")
    context.say(f"Next: write the test shots to {MACHINE_FOLDER}/inbox/{SELFTEST_UNIT}.md in one reply, then run "
                "stage.py selftest --score --surface <this app: claude_code, claude_cowork, claude_web, chatgpt, gemini "
                "or other>.")
    context.summary = f"self-test prepared: {identifiers[0]} to {identifiers[-1]}"
    return 0


def score_selftest(context, project, record_file, project_record, identifiers, inbox):
    from .checks_form import INBOX_CHECKS, FormContext, run_form_checks
    if not inbox.is_file():
        earlier = (project.read_manifest().get("selftest") or {})
        if earlier.get("scored"):
            raise StageStop(f"The test shots were scored on {earlier['scored'][:10]} ({earlier.get('records_complete', 0)} "
                            f"of {earlier.get('records_expected', len(identifiers))} complete, batches of "
                            f"{earlier.get('batch_size')}) and moved to history. To try again, write them again with the "
                            f"same IDs, {identifiers[0]} to {identifiers[-1]}, to {MACHINE_FOLDER}/inbox/{SELFTEST_UNIT}.md "
                            f"and run stage.py selftest --score --surface <this app>; the errors of the last try are in "
                            f"{MACHINE_FOLDER}/{SELFTEST_ERRORS_FILE}.")
        raise StageStop(f"No test shots yet. Run stage.py selftest --prepare, write the test shots to "
                        f"{MACHINE_FOLDER}/inbox/{SELFTEST_UNIT}.md, then score them.")
    constants = context.constants
    batch = constant(constants, "batch_size", {"default": 12, "after_selftest": 18})
    parsed = parse_file(inbox, f"inbox/{inbox.name}", project.schema)
    current_files = project.load_record_files()
    current_index, _ = merge_copies(current_files, project.schema)
    form_context = FormContext.for_records(project.schema, project.words, [parsed], other_record_files=current_files,
                                           written_by_ai=True, current_records=current_index, step=8)
    problems = run_form_checks([parsed], form_context, INBOX_CHECKS + ["FORM-05"])
    # Fields code writes (status, locked) are never the AI's to write, so their absence is no fault here.
    problems = [problem for problem in problems
                if not (problem.check_id == "FORM-05" and code_writes(project.schema, problem.record, problem.field_name))]
    errors = [problem for problem in problems if problem.is_error]
    shots = [record for record in parsed.records if record.type_name == "SHOT"]
    written = [record.identifier for record in shots]
    missing = [identifier for identifier in identifiers if identifier not in written]
    unexpected = [identifier for identifier in written if identifier not in identifiers]
    others = [record.label for record in parsed.records if record.type_name != "SHOT"]
    end = parsed.end_line
    end_ok = end is not None and end.count == len(parsed.records) and len(parsed.end_lines) == 1
    faulty = {problem.record for problem in errors}
    good = [identifier for identifier in written if identifier not in faulty and identifier in identifiers]
    passed = not errors and not missing and not unexpected and not others and end_ok
    size = batch["after_selftest"] if passed else batch["default"]
    surface = context.arguments.surface or detect_surface()
    project_record.set_field("surface", surface, project.schema)
    project_record.set_field("code_execution", "yes", project.schema)
    project_record.set_field("batch_size", str(size), project.schema)
    history = history_run_folder(project)
    keep_in_history(history, project.folder / START_HERE, START_HERE)
    write_file(record_file, project.folder / START_HERE, project.schema)
    keep_in_history(history, inbox, f"inbox/{inbox.name}")
    inbox.unlink()
    manifest = project.read_manifest()
    manifest.setdefault("selftest", {}).update({"scored": now(), "records_complete": len(good),
                                                "records_expected": len(identifiers), "end_line": end_ok,
                                                "errors": len(errors), "batch_size": size, "surface": surface})
    done = manifest.setdefault("units_done", [])
    earlier_entry = next((entry for entry in done if isinstance(entry, dict) and entry.get("unit") == SELFTEST_UNIT),
                         None)
    if earlier_entry is None:
        done.append({"unit": SELFTEST_UNIT, "applied": now(), "records": len(parsed.records), "files": [START_HERE]})
    else:  # a retry with the same issued IDs (C9): the unit stays done once, the new score counts
        earlier_entry["applied_again"] = now()
        earlier_entry["tries"] = int(earlier_entry.get("tries") or 1) + 1
    manifest["selftest"]["errors_file"] = f"{MACHINE_FOLDER}/{SELFTEST_ERRORS_FILE}"
    project.write_manifest(project.refresh_manifest(manifest))
    errors_path = project.machine_folder / SELFTEST_ERRORS_FILE
    errors_path.write_text(f"Self-test scored {now()}: {len(errors)} error lines.\n" +
                           "".join(str(problem) + "\n" for problem in errors), encoding="utf-8")
    project.add_log_entry(f"Checked this app: {len(good)} of {len(identifiers)} test shots came back complete, so "
                          f"shots are written {size} at a time.")
    context.say(f"Self-test: {len(good)} of {len(identifiers)} test shots complete; END line "
                + ("right." if end_ok else "missing or wrong.")
                + (f" Missing: {', '.join(missing[:5])}." if missing else "")
                + (f" Not issued: {', '.join(unexpected[:5])}." if unexpected else ""))
    context.say(f"{plural_words(len(errors), 'error line')}; every one is in {MACHINE_FOLDER}/{SELFTEST_ERRORS_FILE}.")
    for problem in errors[:10]:
        context.say(str(problem))
    if len(errors) > 10:
        context.say(f"... and {len(errors) - 10} more error lines in {MACHINE_FOLDER}/{SELFTEST_ERRORS_FILE}.")
    if not passed:
        context.say(f"To try again with the same IDs, write the test shots again to {MACHINE_FOLDER}/inbox/"
                    f"{SELFTEST_UNIT}.md and run stage.py selftest --score --surface <this app>.")
    context.say(f"Set on the project: surface {surface}, code runs here, batches of {size} shots. The test shots "
                "were deleted (a copy is in history).")
    rights_choice = next((record for record_file in project.load_record_files() for record in record_file.records
                          if record.type_name == "CHOICE" and record.identifier == "CHOICE-001"), None)
    rights_status = normalise_word((rights_choice.get("status") if rights_choice is not None else None) or "open")
    if rights_status in ("answered", "defaulted"):
        context.say("Next: stage.py next (the rights question is already answered).")
    else:
        context.say("Next: the welcome message with the rights question (choice 1).")
    context.summary = f"self-test scored: batch {size}"
    return 0


def code_writes(schema, identifier, field_name):
    """True when code, not the AI, writes this field of a SHOT (status and locked, and every code field)."""
    definition = schema.field("SHOT", field_name) or {}
    writers = schema.writers(definition) if definition else []
    return field_name in ("status", "locked") or (writers and all(writer in ("code_state", "code_derived", "story")
                                                                  for writer in writers))


def register_commands(table):
    """The commands of this module (stage.py calls this; see the note at the top of stage.py)."""
    table.add("read", "Read and number the story: scenes or chapters, speeches, the odd-lines report", run_read,
              add_read_arguments)
    table.add("lines", "Every story line that mentions an element (a character, place, thing or words)", run_lines,
              add_lines_arguments)
    table.add("selftest", "Test this app: --prepare issues the test shots; --score --surface <this app> scores them "
              "and sets the batch size", run_selftest, add_selftest_arguments)
