#!/usr/bin/env python3
"""wp3_reader_acceptance.py: the acceptance test of work package 3, the story reader (blueprint 14.2 WP3 and test T1
of 14.3). It checks stage_tools/read_story.py and the commands read, lines and selftest.

What it runs, in plain words:
1. The reader on every fixture in tests/fixtures/reader: a short invented screenplay in The Catch's layout, the
   same screenplay as Fountain and as Final Draft, a Word screenplay and a PDF made from it by this test, a prose
   story with chapters (Markdown), the same prose hard-wrapped as plain text, and as a Word file and an EPUB made
   by this test with zipfile, a stage play, and files the reader must refuse (empty, old Word, OpenDocument,
   copy-protected EPUB, a PDF with no text layer). Every expected number was worked out by hand (and word counts
   with the word-count command wc in its plain setting).
2. The scene 10 excerpt of The Catch (tests/fixtures), with the quote-anchor rule WP12a wrote down.
3. The commands on a project made from a fixture: new, read (again before the lock, refused after it), apply of
   the length answer, lines, selftest --prepare and --score, and the FORM checks on every file read writes.
4. Test T1 on the two real stories, when their paths are given: stage.py new and read in a temporary folder
   outside the repository, and every number T1 lists.

Usage:
    python tests/wp3_reader_acceptance.py [<The Catch story file> [<The Long Places story file>]] [--keep]
Without the story files the T1 groups say "skipped: story not present". Exit 0 when every group passes, else 1.
Standard library only (a PDF is read only when pdftotext or the pypdf package is present).
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
TOOLS = SKILL / "tools"
STAGE = TOOLS / "stage.py"
FIXTURES = REPOSITORY / "tests" / "fixtures" / "reader"
EXCERPT = REPOSITORY / "tests" / "fixtures" / "The Catch - lines 397-489.txt"
sys.path.insert(0, str(TOOLS))

from stage_tools.checks_form import FormContext, run_form_checks  # noqa: E402
from stage_tools.project_files import Project, StageStop  # noqa: E402
from stage_tools.read_story import (NumberedStory, load_story_file, normalise_quote, read_story_lines,  # noqa: E402
                                    story_map_of)
from stage_tools.record_format import load_skill_data, merge_copies, parse_file  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
RESULTS = []

# ---------------------------------------------------------------- expected values, worked out by hand

NIGHT_SHIFT_SPEECHES = [
    ("SC01-D01", "CH-MARA", "We're closed.", "direct"),
    ("SC01-D02", "CH-OSKAR", "It's me.", "off_screen"),
    ("SC01-D03", "CH-MARA", "Where did you find that?", "direct"),
    ("SC01-D04", "CH-OSKAR", "Under the shed. Where you said.", "direct"),
    ("SC02-D01", "CH-MARA", "Walk slowly. Keep to the wall.", "earpiece"),
    ("SC02-D02", "CH-OSKAR", "I am walking slowly.", "direct"),
    ("SC02-D03", "CH-MARA", "Now left.", "earpiece"),
    ("SC03-D01", "CH-MARA", "Keep it. Keep it safe.", "direct"),
]
NIGHT_SHIFT_HEADINGS = ["INT. BAKERY - BACK ROOM - NIGHT", "EXT. YARD - CONTINUOUS (ON THE MONITOR)",
                        "INT. BAKERY - FRONT ROOM - LATER"]
NIGHT_SHIFT_TOKENS = {"RINGS": "sound", "KEY": "prop", "NO ENTRY AFTER TEN": "text", "GUARD": "character",
                      "BARKS": "sound", "BLACK": "instruction", "MARA HOLT": "character", "OSKAR": "character"}
LAMP_KEEPER_CHAPTERS = [("CP01", "I. The Old Lamps", 5, 16, 62), ("CP02", "II. The Threshold", 17, 27, 51),
                        ("CP03", "Chapter 3: The Letter", 28, 34, 31)]
CATCH_HEADING_LINES = [10, 71, 116, 145, 181, 198, 300, 333, 343, 397, 490, 532, 672, 830, 838, 868, 912, 1000,
                       1098, 1112, 1211, 1259, 1265, 1376, 1428, 1502, 1555, 1599, 1713, 1814]
LONG_PLACES_CHAPTER_LINES = [5, 84, 163, 262, 385, 476, 541, 636, 777, 858, 943, 1048, 1155, 1287]


def report(ok, what, detail=""):
    level = "PASS" if ok is True else ("INFO" if ok is None else "FAIL")
    RESULTS.append(level)
    print(f"{level}  {what}" + (f": {detail}" if detail else ""), flush=True)


def shorten(problems, count=6):
    shown = "; ".join(str(problem) for problem in problems[:count])
    return shown + (f" ... and {len(problems) - count} more" if len(problems) > count else "")


def expect(problems, label, actual, wanted):
    if actual != wanted:
        problems.append(f"{label} is {actual!r}, expected {wanted!r}")


def reading_of(path):
    return read_story_lines(load_story_file(path), CONSTANTS)


def refused(path):
    """The plain message the reader stops with, or None when it read the file."""
    try:
        reading_of(path)
    except StageStop as stop:
        return stop.message
    return None


# ---------------------------------------------------------------- files this test makes with zipfile

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def docx_paragraph(text, style=None, inserted=None, deleted=None):
    style_xml = f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ""
    runs = f'<w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r>'
    if inserted:
        runs += f'<w:ins w:id="1" w:author="Writer"><w:r><w:t xml:space="preserve">{escape(inserted)}</w:t></w:r></w:ins>'
    if deleted:
        runs += f'<w:del w:id="2" w:author="Writer"><w:r><w:delText>{escape(deleted)}</w:delText></w:r></w:del>'
    return f"<w:p>{style_xml}{runs}</w:p>"


def escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def write_docx(path, paragraphs, styles, comments=0):
    """A minimal Word file: paragraphs are (text, style id or None, inserted, deleted)."""
    body = "".join(docx_paragraph(*paragraph) for paragraph in paragraphs)
    document = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="{W}"><w:body>{body}'
                "</w:body></w:document>")
    style_xml = "".join(f'<w:style w:type="paragraph" w:styleId="{identifier}"><w:name w:val="{name}"/></w:style>'
                        for identifier, name in styles.items())
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/'
                                                'package/2006/content-types"/>')
        archive.writestr("word/document.xml", document)
        archive.writestr("word/styles.xml", f'<?xml version="1.0"?><w:styles xmlns:w="{W}">{style_xml}</w:styles>')
        if comments:
            items = "".join(f'<w:comment w:id="{number}"><w:p><w:r><w:t>check</w:t></w:r></w:p></w:comment>'
                            for number in range(comments))
            archive.writestr("word/comments.xml", f'<?xml version="1.0"?><w:comments xmlns:w="{W}">{items}</w:comments>')


def markdown_blocks(path):
    """The paragraphs of a Markdown prose fixture as (kind, text): headings and plain paragraphs (markup removed)."""
    blocks = []
    current = []
    for line in Path(path).read_text(encoding="utf-8").splitlines() + [""]:
        if not line.strip():
            if current:
                blocks.append(("paragraph", " ".join(current)))
                current = []
            continue
        if line.startswith("#"):
            blocks.append(("heading", line.lstrip("#").strip()))
            continue
        current.append(re.sub(r"^>\s*", "", line).strip().strip("*"))
    return blocks


def write_prose_docx(path):
    blocks = markdown_blocks(FIXTURES / "The lamp keeper - chapters.md")
    paragraphs = []
    for index, (kind, text) in enumerate(blocks):
        if kind == "heading":
            paragraphs.append((text, "Title" if index == 0 else "Heading1", None, None))
        elif text.startswith("Nilay climbs"):
            paragraphs.append((text, None, " She counts them.", "an old sentence"))
        else:
            paragraphs.append((text, None, None, None))
    write_docx(path, paragraphs, {"Title": "Title", "Heading1": "heading 1"}, comments=2)


def write_screenplay_docx(path):
    """The Fountain fixture as a Word screenplay with screenplay styles (no title card paragraphs)."""
    reading = reading_of(FIXTURES / "Night shift.fountain")
    styles = {"heading": "SceneHeading", "cue": "Character", "dialogue": "Dialogue", "parenthetical": "Parenthetical",
              "transition": "Transition", "action": "Action"}
    paragraphs = [("NIGHT SHIFT", "Title", None, None)]
    for line, kind in zip(reading.lines, reading.types):
        if kind in styles:
            paragraphs.append((line.strip().lstrip(">").strip(), styles[kind], None, None))
    write_docx(path, paragraphs, {"Title": "Title", "SceneHeading": "Scene Heading", "Character": "Character",
                                  "Dialogue": "Dialogue", "Parenthetical": "Parenthetical",
                                  "Transition": "Transition", "Action": "Action"})


def write_epub(path, encrypted=False):
    blocks = markdown_blocks(FIXTURES / "The lamp keeper - chapters.md")
    pages = [[]]
    for kind, text in blocks:
        if kind == "heading" and re.match(r"^(II\.|Chapter)", text):
            pages.append([])
        pages[-1].append(f"<h1>{escape(text)}</h1>" if kind == "heading" else f"<p>{escape(text)}</p>")
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip")
        archive.writestr("META-INF/container.xml",
                         '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:'
                         'container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/'
                         'oebps-package+xml"/></rootfiles></container>')
        if encrypted:
            archive.writestr("META-INF/encryption.xml",
                             '<?xml version="1.0"?><encryption xmlns="urn:oasis:names:tc:opendocument:xmlns:container" '
                             'xmlns:enc="http://www.w3.org/2001/04/xmlenc#"><enc:EncryptedData><enc:EncryptionMethod '
                             'Algorithm="http://www.w3.org/2001/04/xmlenc#aes128-cbc"/></enc:EncryptedData></encryption>')
        items = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>']
        spine = ['<itemref idref="nav"/>']
        for number, page in enumerate(pages, 1):
            items.append(f'<item id="page{number}" href="page{number}.xhtml" media-type="application/xhtml+xml"/>')
            spine.append(f'<itemref idref="page{number}"/>')
            archive.writestr(f"OEBPS/page{number}.xhtml",
                             '<?xml version="1.0" encoding="UTF-8"?><html xmlns="http://www.w3.org/1999/xhtml"><head>'
                             f'<title>Page {number}</title></head><body>{"".join(page)}</body></html>')
        archive.writestr("OEBPS/nav.xhtml", '<?xml version="1.0"?><html xmlns="http://www.w3.org/1999/xhtml"><body>'
                                            '<h1>Contents</h1><p>I. The Old Lamps</p></body></html>')
        archive.writestr("OEBPS/content.opf",
                         '<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0"><metadata '
                         'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>The Lamp Keeper</dc:title></metadata>'
                         f'<manifest>{"".join(items)}</manifest><spine>{"".join(spine)}</spine></package>')


def write_pdf(path, lines):
    """A one-page PDF with a text layer (Courier, one text line per story line); lines=None makes a page with no text."""
    content = ["BT", "/F1 10 Tf", "12 TL", "54 760 Td"]
    for line in lines or []:
        escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        content.append(f"({escaped}) Tj T*")
    content.append("ET")
    stream = "\n".join(content if lines else ["0 0 m 10 10 l S"]).encode("latin-1")
    objects = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
               b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
               b"/Resources << /Font << /F1 5 0 R >> >> >>",
               b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
               b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>"]
    data = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, 1):
        offsets.append(len(data))
        data += f"{number} 0 obj\n".encode() + body + b"\nendobj\n"
    table = len(data)
    data += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    for offset in offsets:
        data += f"{offset:010d} 00000 n \n".encode()
    data += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{table}\n%%EOF\n".encode()
    Path(path).write_bytes(bytes(data))


def pdf_converter_present():
    if shutil.which("pdftotext"):
        return True
    try:
        import pypdf  # noqa: F401
        return True
    except ImportError:
        return False


# ---------------------------------------------------------------- group 1: the fixtures

def check_night_shift(reading, cards=True, exact=None):
    """The facts every version of the invented screenplay must give."""
    problems = []
    expect(problems, "kind", reading.source_kind, "screenplay")
    expect(problems, "scene count", len(reading.scenes), 3)
    expect(problems, "headings", [scene.heading for scene in reading.scenes], NIGHT_SHIFT_HEADINGS)
    expect(problems, "title", reading.title, "NIGHT SHIFT")
    if len(reading.scenes) == 3:
        first, second, third = reading.scenes
        expect(problems, "scene 1 join in", first.transition_in, "fade_in")
        expect(problems, "scene 1 join out", first.transition_out, "cut_to_black")
        expect(problems, "scene 2 join in", second.transition_in, "continuous")
        expect(problems, "scene 3 join out", third.transition_out, "fade_out")
        expect(problems, "scene 2 place and time", (second.int_ext, second.place_text, second.time_text),
               ("ext", "YARD", "CONTINUOUS"))
        expect(problems, "scene 2 presentation", (second.presentation, second.presentation_note),
               ("on_screen", "ON THE MONITOR"))
        expect(problems, "scene 1 speaking", first.speaking, [("CH-MARA", 2), ("CH-OSKAR", 2)])
        expect(problems, "scene 3 characters", third.characters, ["CH-MARA"])
        if cards:
            expect(problems, "cards", [(card["shot"], card["text"]) for scene in reading.scenes for card in scene.cards],
                   [("SC01-SH990", "NIGHT SHIFT"), ("SC03-SH990", "THE END")])
    speeches = [(speech.identifier, speech.speaker, normalise_quote(speech.text), speech.path)
                for speech in reading.speeches]
    expect(problems, "speeches", speeches, [(a, b, normalise_quote(c), d) for a, b, c, d in NIGHT_SHIFT_SPEECHES])
    expect(problems, "characters", [(character.identifier, character.names, character.cues)
                                    for character in sorted(reading.characters, key=lambda c: c.identifier)],
           [("CH-MARA", ["MARA", "MARA HOLT"], 5), ("CH-OSKAR", ["OSKAR"], 3)])
    for key, wanted in (("dialogue_words", 32), ("action_words", 76), ("beat_marks", 2), ("speeches", 8)):
        expect(problems, key, reading.counts.get(key), wanted)
    tokens = {token["text"]: token["class"] for scene in reading.scenes for token in scene.tokens}
    for text, kind in NIGHT_SHIFT_TOKENS.items():
        expect(problems, f'capitalised "{text}"', tokens.get(text), kind)
    expect(problems, "people who never speak", [person["name"] for person in reading.people_without_speeches],
           ["GUARD"])
    for label, (actual, wanted) in (exact or {}).items():
        expect(problems, label, actual, wanted)
    return problems


def group_fixtures(work):
    reading = reading_of(FIXTURES / "Night shift - Catch layout.txt")
    exact = {"format": (reading.source_format, "catch_dialect"), "lines": (len(reading.lines), 61),
             "words (wc -w)": (reading.words, 180),
             "scene lines": ([(scene.first, scene.last) for scene in reading.scenes], [(8, 32), (33, 48), (49, 61)]),
             "cue lines": ([speech.cue_line for speech in reading.speeches], [12, 15, 20, 24, 37, 41, 44, 53]),
             "card lines": ([card["line"] for scene in reading.scenes for card in scene.cards], [31, 61]),
             "spoken characters": (reading.counts.get("spoken_characters"), 156),
             "title page lines": ([(odd.first, odd.last) for odd in reading.odd_lines if odd.kind == "title_page"],
                                  [(1, 4)]),
             "join into scene 1 from line": (reading.scenes[0].transition_in_line if reading.scenes else None, 6),
             "odd-line kinds": (sorted({odd.kind for odd in reading.odd_lines}),
                                sorted({"title_page", "transition_in", "alias", "card", "presentation", "voice_path"}))}
    problems = check_night_shift(reading, exact=exact)
    report(not problems, "fixture: an invented screenplay in The Catch's layout (61 lines, 3 scenes, 8 speeches, "
           "2 cards, the title page, an alias, a presentation note, an inherited earpiece)", shorten(problems))

    reading = reading_of(FIXTURES / "Night shift.fountain")
    exact = {"format": (reading.source_format, "fountain"), "lines": (len(reading.lines), 66),
             "scene lines": ([(scene.first, scene.last) for scene in reading.scenes], [(7, 33), (34, 53), (54, 66)]),
             "note and set-aside lines": ([(odd.kind, odd.first, odd.last) for odd in reading.odd_lines
                                           if odd.kind in ("note", "boneyard")], [("note", 26, 26), ("boneyard", 50, 52)])}
    problems = check_night_shift(reading, exact=exact)
    report(not problems, "fixture: the same screenplay as Fountain (title page keys, forced and plain joins, centered "
           "cards, a note and set-aside text left out)", shorten(problems))

    reading = reading_of(FIXTURES / "Night shift.fdx")
    problems = check_night_shift(reading, exact={"format": (reading.source_format, "fdx"),
                                                  "extraction": (reading.extraction, "app_export")})
    report(not problems, "fixture: the same screenplay as Final Draft (paragraph types, centered cards, a title page, "
           "text runs joined)", shorten(problems))

    path = work / "Night shift.docx"
    write_screenplay_docx(path)
    reading = reading_of(path)
    problems = check_night_shift(reading, cards=False, exact={"format": (reading.source_format, "docx")})
    report(not problems, "made by this test: the same screenplay as a Word file with screenplay styles",
           shorten(problems))

    if pdf_converter_present():
        path = work / "Night shift.pdf"
        text_lines = (FIXTURES / "Night shift.fountain").read_text(encoding="utf-8").splitlines()
        write_pdf(path, text_lines)
        reading = reading_of(path)
        problems = check_night_shift(reading, exact={"format": (reading.source_format, "pdf_text")})
        if not any(odd.kind == "file" and "PDF" in odd.finding for odd in reading.odd_lines):
            problems.append("no line to look at says the story came from a PDF")
        report(not problems, "made by this test: the Fountain screenplay as a PDF with a text layer (read through the "
               "converter present here)", shorten(problems))
    else:
        report(None, "PDF with a text layer", "skipped: no PDF converter (pdftotext or pypdf) in this environment")

    reading = reading_of(FIXTURES / "The lamp keeper - chapters.md")
    problems = []
    expect(problems, "kind and format", (reading.source_kind, reading.source_format), ("prose", "markdown"))
    expect(problems, "lines", len(reading.lines), 34)
    expect(problems, "words (wc -w)", reading.words, 178)
    expect(problems, "chapters", [(chapter.identifier, chapter.title, chapter.first, chapter.last, chapter.words)
                                  for chapter in reading.chapters], LAMP_KEEPER_CHAPTERS)
    expect(problems, "title", (reading.title, reading.title_line), ("The Lamp Keeper - a draft for testing", 1))
    kinds = {odd.kind: (odd.first, odd.last) for odd in reading.odd_lines}
    expect(problems, "front matter", kinds.get("front_matter"), (3, 3))
    expect(problems, "quotation line", kinds.get("quotations"), (13, 13))
    expect(problems, "verse", kinds.get("verse"), (21, 24))
    expect(problems, "repeated passage", [(run["lines"], run["repeat_of"]) for run in reading.repeats],
           [([30, 32], [7, 9])])
    expect(problems, "speeches (prose has none from code)", len(reading.speeches), 0)
    report(not problems, "fixture: prose with a title, front matter and three chapters (roman numerals and the word "
           "Chapter), a quotation, verse and a repeated letter", shorten(problems))

    reading = reading_of(FIXTURES / "The lamp keeper - wrapped.txt")
    problems = []
    expect(problems, "kind and format", (reading.source_kind, reading.source_format), ("prose", "plain_text"))
    expect(problems, "lines after joining", len(reading.lines), 13)
    expect(problems, "words (wc -w)", reading.words, 96)
    expect(problems, "chapters", [(chapter.title, chapter.first, chapter.last) for chapter in reading.chapters],
           [("CHAPTER ONE", 3, 8), ("Chapter Two", 9, 13)])
    expect(problems, "title", (reading.title, reading.title_line), ("THE LAMP KEEPER", 1))
    if not any(odd.kind == "file" and "one paragraph per line" in odd.finding for odd in reading.odd_lines):
        problems.append("the joining of short lines is not reported")
    report(not problems, "fixture: hard-wrapped prose in plain text is numbered one paragraph per line", shorten(problems))

    path = work / "The lamp keeper.docx"
    write_prose_docx(path)
    reading = reading_of(path)
    problems = []
    expect(problems, "kind and format", (reading.source_kind, reading.source_format), ("prose", "docx"))
    expect(problems, "chapter titles", [chapter.title for chapter in reading.chapters],
           [title for _, title, _, _, _ in LAMP_KEEPER_CHAPTERS])
    expect(problems, "title", reading.title, "The Lamp Keeper - a draft for testing")
    notes = " ".join(odd.finding for odd in reading.odd_lines if odd.kind == "file")
    if "1 insertion and 1 deletion" not in notes:
        problems.append(f"tracked changes not counted: {notes!r}")
    if "2 comments" not in notes:
        problems.append(f"comments not counted: {notes!r}")
    text = " ".join(reading.lines)
    if "She counts them." not in text or "an old sentence" in text:
        problems.append("tracked changes were not read with every change accepted")
    report(not problems, "made by this test: the prose as a Word file (styles for title and chapters, one tracked "
           "insertion and deletion, two comments)", shorten(problems))

    path = work / "The lamp keeper.epub"
    write_epub(path)
    reading = reading_of(path)
    problems = []
    expect(problems, "kind and format", (reading.source_kind, reading.source_format), ("prose", "epub"))
    expect(problems, "chapter titles", [chapter.title for chapter in reading.chapters],
           [title for _, title, _, _, _ in LAMP_KEEPER_CHAPTERS])
    expect(problems, "title", reading.title, "The Lamp Keeper - a draft for testing")
    if "Contents" in reading.lines:
        problems.append("the table of contents page was read as story")
    report(not problems, "made by this test: the prose as an EPUB (three pages in spine order; the contents page left "
           "out)", shorten(problems))

    reading = reading_of(FIXTURES / "The yard - stage play.txt")
    problems = []
    expect(problems, "kind", reading.source_kind, "stage_play")
    expect(problems, "scenes", [(scene.identifier, scene.first, scene.last) for scene in reading.scenes],
           [("SC01", 5, 11), ("SC02", 12, 15)])
    expect(problems, "speeches", [(speech.identifier, speech.speaker, speech.text) for speech in reading.speeches],
           [("SC01-D01", "CH-MARA", "We're closed."), ("SC01-D02", "CH-OSKAR", "It's me."),
            ("SC01-D03", "CH-MARA", "Where did you find that?"), ("SC02-D01", "CH-OSKAR", "I found it under the shed."),
            ("SC02-D02", "CH-MARA", "Keep it safe.")])
    report(not problems, "fixture: a stage play (SCENE headings, speeches on the speaker's line, an act break)",
           shorten(problems))

    problems = []
    cases = {"an empty file": ("empty.txt", b"  \n"), "an old Word file": ("old.doc", b"\xd0\xcf\x11\xe0 old word"),
             "an OpenDocument file": ("story.odt", None)}
    for label, (name, data) in cases.items():
        path = work / name
        if data is None:
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("mimetype", "application/vnd.oasis.opendocument.text")
                archive.writestr("content.xml", "<office:document-content/>")
        else:
            path.write_bytes(data)
        message = refused(path)
        if not message:
            problems.append(f"{label} was read instead of refused")
    path = work / "protected.epub"
    write_epub(path, encrypted=True)
    message = refused(path)
    if not message or "copy-protected" not in message:
        problems.append(f"a copy-protected EPUB was not refused plainly: {message!r}")
    path = work / "scan.pdf"
    write_pdf(path, None)
    message = refused(path)
    if not message or "Google Docs" not in message:
        problems.append(f"a PDF with no text layer was not refused with the one-step fix: {message!r}")
    report(not problems, "files the reader refuses with one plain line (empty, old Word, OpenDocument, copy-protected "
           "EPUB, a PDF with no text layer)", shorten(problems))


def group_excerpt():
    if not EXCERPT.is_file():
        report(None, "the scene 10 excerpt", "skipped: story not present")
        return
    reading = reading_of(EXCERPT)
    problems = []
    expect(problems, "first line number", reading.first_line_number, 397)
    scene = reading.scenes[0] if reading.scenes else None
    expect(problems, "scene", (scene.identifier, scene.first, scene.last) if scene else None, ("SC10", 397, 489))
    speeches = [speech for speech in reading.speeches if speech.scene == "SC10"]
    expect(problems, "speeches", len(speeches), 16)
    if speeches:
        expect(problems, "first speech", (speeches[0].identifier, speeches[0].text), ("SC10-D01", "Kitchen."))
        expect(problems, "last speech", (speeches[-1].identifier, speeches[-1].text),
               ("SC10-D16", "Nobody leave this room."))
        expect(problems, "SC10-D11", (speeches[10].speaker, speeches[10].text, speeches[10].parentheticals,
                                      speeches[10].cue_line), ("CH-IONA", "Not mint.", [(462, "not steady")], 461))
    if scene:
        expect(problems, "speaking", scene.speaking, [("CH-SAYE", 10), ("CH-IONA", 4), ("CH-JUDE", 1), ("CH-ELI", 1)])
        expect(problems, "card", [(card["line"], card["shot"]) for card in scene.cards], [(488, "SC10-SH990")])
        expect(problems, "join out", (scene.transition_out, scene.transition_out_line), ("cut_to_black", 486))
    story = NumberedStory.from_story_map(story_map_of(reading))
    # The adopt rule's three worked examples (WP12a build log, contract 2) and a story point.
    expect(problems, "anchor 1", story.resolve_lines('"fully dressed at four in the morning"', 397, 489), (399, 402))
    expect(problems, "anchor 2", story.resolve_lines('"She goes to the windowsill" to "What does it taste of?"',
                                                     397, 489), (449, 463))
    expect(problems, "anchor 3", story.resolve_lines('"She waits until Iona steps aside." to "CUT TO BLACK."',
                                                     397, 489), (481, 488))
    expect(problems, "story point", story.resolve_story_point('SC10 "Nobody leave this room."'), 484)
    expect(problems, "single line", story.resolve_line("Saye's wedding ring. On her right hand."), 436)
    short = story.check_quote("Not mint.", 397, 489)
    twice = story.check_quote("Nothing has happened", 397, 489)
    if not short or "fewer than 3 words" not in short:
        problems.append(f"a two-word quote is not refused: {short!r}")
    if not twice or "found 2 times" not in twice:
        problems.append(f"a quote found twice in one line is not reported: {twice!r}")
    report(not problems, "the scene 10 excerpt: lines 397-489, 16 speeches, the card at line 488, and the quote-anchor "
           "rule (three worked examples, a story point, a single line, too short, found more than once)",
           shorten(problems))


def group_adopt_contract(work):
    """What adopt (work package 4) needs from the reader: the numbered story, speeches.json and story map.json for a
    folder saved by hand in a chat app, without touching the AI's scene list."""
    chat = REPOSITORY / "tests" / "fixtures" / "chat saved scene 10"
    if not EXCERPT.is_file() or not chat.is_dir():
        report(None, "reading for adopt", "skipped: story not present")
        return
    folder = work / "adopt" / "The Catch - breakdown"
    shutil.copytree(chat, folder)
    before = {path.name: path.read_bytes() for path in folder.rglob("*.md") if path.name != "00 Start here.md"}
    from stage_tools.read_story import read_into_project
    reading, written, _ = read_into_project(Project(folder, SCHEMA, WORDS), None, EXCERPT, write_records=False)
    problems = []
    after = {path.name: path.read_bytes() for path in folder.rglob("*.md") if path.name != "00 Start here.md"
             and path.name != "03 Story - numbered.md"}
    changed = [name for name, data in after.items() if before.get(name) != data]
    if changed:
        problems.append(f"record files changed: {changed}")
    speeches = json.loads((folder / "For machines - do not edit/speeches.json").read_text(encoding="utf-8"))
    expect(problems, "speeches", [speech["id"] for speech in speeches["speeches"]][::15], ["SC10-D01", "SC10-D16"])
    story = NumberedStory.from_project(folder)
    expect(problems, "scene scope", story.scope_of("SC10"), (397, 489))
    report(not problems, "reading for adopt: with write_records=False only the numbered story, speeches.json and "
           "story map.json are written; the chat-saved scene list is untouched", shorten(problems))


# ---------------------------------------------------------------- group 2: the commands on a project

def run_stage(arguments, folder):
    environment = dict(os.environ, STAGE_LOCK_WAIT_SECONDS="2")
    result = subprocess.run([sys.executable, str(STAGE)] + arguments, cwd=folder, capture_output=True, text=True,
                            env=environment, timeout=300)
    return result.returncode, result.stdout + result.stderr


def form_problems(project_folder, step):
    project = Project(project_folder, SCHEMA, WORDS)
    files = project.load_record_files()
    context = FormContext.for_records(SCHEMA, WORDS, files, step=step)
    return run_form_checks(files, context), files


def make_project(story, parent):
    code, output = run_stage(["new", str(story), "--into", str(parent)], parent)
    if code != 0:
        return None, f"new exited {code}: {output.strip()}"
    folder = next((path for path in sorted(parent.iterdir()) if (path / "00 Start here.md").is_file()), None)
    return folder, output


def selftest_shots(identifiers):
    """Twenty full SHOT records made from the gold turn shot, with the issued IDs and without code's fields."""
    gold = (SKILL / "references" / "examples" / "01 The Catch - scene 10.md").read_text(encoding="utf-8").splitlines()
    start = next(index for index, line in enumerate(gold) if line.startswith("### SHOT SC10-SH150"))
    end = start + 1
    while end < len(gold) and gold[end].strip():
        end += 1
    body = [line for line in gold[start + 1:end] if not line.startswith(("- status:", "- locked:"))]
    records = []
    for identifier in identifiers:
        records += [f"### SHOT {identifier} Test shot"] + body + [""]
    return records


def group_commands(work):
    parent = work / "project"
    parent.mkdir()
    folder, output = make_project(FIXTURES / "Night shift - Catch layout.txt", parent)
    if folder is None:
        report(False, "commands: new", output)
        return
    code, output = run_stage(["read"], folder)
    problems = []
    if code != 0:
        problems.append(f"read exited {code}: {output.strip()}")
    for name in ("03 Story - numbered.md", "04 Scene list.md", "07 Characters and voices.md", "01 Choices.md",
                 "For machines - do not edit/speeches.json", "For machines - do not edit/story map.json"):
        if not (folder / name).is_file():
            problems.append(f"{name} was not written")
    if problems:
        report(False, "commands: read on a fixture project", shorten(problems))
        return
    numbered = (folder / "03 Story - numbered.md").read_text(encoding="utf-8")
    if "31  = NIGHT SHIFT" not in numbered or "61  = THE END" not in numbered:
        problems.append("03 Story - numbered does not show the lines with their numbers")
    form, files = form_problems(folder, 1)
    if form:
        problems.append("FORM checks at step 1: " + shorten(form, 3))
    merged, _ = merge_copies(files, SCHEMA)
    scene = merged.get(("SCENE", "SC02"))
    if scene is None:
        problems.append("no SCENE SC02 record")
    else:
        for field, wanted in (("heading", "EXT. YARD - CONTINUOUS (ON THE MONITOR)"), ("lines", "33-48"),
                              ("presentation", "on_screen"), ("host", "open"), ("transition_in", "continuous"),
                              ("characters", "CH-MARA, CH-OSKAR"), ("origin", "story"), ("status", "draft"),
                              ("locked", "no")):
            expect(problems, f"SC02 {field}", scene.get(field), wanted)
        expect(problems, "SC02 speaking", scene.get_all("speaking"), ["CH-MARA | cues: 2", "CH-OSKAR | cues: 1"])
    first = merged.get(("SCENE", "SC01"))
    if first is not None and not any("SC01-SH990" in note for copy in first.copies for note in copy.notes):
        problems.append("SC01 has no note for its card, shot 990")
    mara = merged.get(("CHARACTER", "CH-MARA"))
    expect(problems, "CH-MARA names", mara.get("names") if mara else None, "MARA, MARA HOLT")
    project_record = next(record for key, record in merged.items() if key[0] == "PROJECT")
    for field, wanted in (("source_kind", "screenplay"), ("source_format", "catch_dialect"), ("language", "english"),
                          ("format", "short"), ("runtime_target_s", "open"), ("scene_id_digits", "2")):
        expect(problems, f"PROJECT {field}", project_record.get(field), wanted)
    format_choice = merged.get(("CHOICE", "CHOICE-004"))
    length_choice = merged.get(("CHOICE", "CHOICE-005"))
    expect(problems, "CHOICE-004 status and answer", (format_choice.get("status"), format_choice.get("answer"),
                                                      format_choice.get("asked")) if format_choice else None,
           ("defaulted", "a", "no"))
    expect(problems, "CHOICE-005 status and checkpoint", (length_choice.get("status"), length_choice.get("checkpoint"),
                                                          length_choice.get("asked")) if length_choice else None,
           ("open", "a", "yes"))
    scene_list = (folder / "04 Scene list.md").read_text(encoding="utf-8")
    plain = scene_list.split("Below this line:")[0]
    for wanted in ("## Lines to look at", "Line 31", "shot 990 of scene 1", "(ON THE MONITOR)", "earpiece"):
        if wanted not in plain:
            problems.append(f"the odd-lines report above the divider lacks {wanted!r}")
    for code_word in re.findall(r"\bSC\d{2}\b|\bCH-[A-Z]+\b|\bl\.", plain):
        problems.append(f"an internal code in the plain part: {code_word}")
        break
    speeches = json.loads((folder / "For machines - do not edit/speeches.json").read_text(encoding="utf-8"))
    expect(problems, "speeches.json", [(speech["id"], speech["speaker"], speech["line"], speech["path"])
                                       for speech in speeches["speeches"]],
           [(identifier, speaker, line, path) for (identifier, speaker, _, path), line in
            zip(NIGHT_SHIFT_SPEECHES, [12, 15, 20, 24, 37, 41, 44, 53])])
    manifest = json.loads((folder / "For machines - do not edit/manifest.json").read_text(encoding="utf-8"))
    expect(problems, "manifest story", {key: manifest.get("story", {}).get(key) for key in
                                        ("scenes", "speeches", "lines", "format_choice", "length_choice")},
           {"scenes": 3, "speeches": 8, "lines": 61, "format_choice": "CHOICE-004", "length_choice": "CHOICE-005"})
    if "Read the story: 3 scenes, 8 speeches, 61 numbered lines." not in (folder / "00 Start here.md").read_text(encoding="utf-8"):
        problems.append("no numbered log entry for the reading in 00 Start here")
    report(not problems, "commands: new and read on a fixture project (the numbered story, SCENE, CHARACTER, CHOICE "
           "and PROJECT records, the odd-lines report, speeches.json, the manifest and the log; FORM checks at step 1 "
           "find nothing)", shorten(problems))

    # Reading again before the lock gives the same records; after the length answer, read is refused (exit 2).
    problems = []
    before = (folder / "04 Scene list.md").read_text(encoding="utf-8")
    code, output = run_stage(["read"], folder)
    after = (folder / "04 Scene list.md").read_text(encoding="utf-8")
    if code != 0 or before != after:
        problems.append(f"a second read before the lock changed the scene list or failed ({code})")
    if not any((folder / "For machines - do not edit/history").rglob("04 Scene list.md")):
        problems.append("the old scene list was not kept in history")
    inbox = folder / "For machines - do not edit/inbox/U-01-ODDLINES.md"
    inbox.write_text("### CHOICE CHOICE-005\n- answer: defaults\n\nEND OF FILE | Answer | 1 records\n", encoding="utf-8")
    code, output = run_stage(["apply", "U-01-ODDLINES"], folder)
    if code != 0:
        problems.append(f"apply of the length answer exited {code}: {output.strip()}")
    merged, _ = merge_copies(Project(folder, SCHEMA, WORDS).load_record_files(), SCHEMA)
    project_record = next(record for key, record in merged.items() if key[0] == "PROJECT")
    expect(problems, "runtime and scope after the answer", (project_record.get("runtime_target_s"),
                                                            project_record.get("scope")), ("as_written", "all"))
    code, output = run_stage(["read"], folder)
    if code != 2 or "never numbered again" not in output:
        problems.append(f"read after the length answer was not refused with exit 2: {code} {output.strip()}")
    form, _ = form_problems(folder, 1)
    if form:
        problems.append("FORM checks at step 1 after the answer: " + shorten(form, 3))
    report(not problems, "commands: read again before the lock (same records, old copy in history), the length answer "
           "applied (runtime as written, scope all), read refused after it with exit 2", shorten(problems))

    # lines
    problems = []
    code, output = run_stage(["lines", "CH-MARA"], folder)
    listed = re.findall(r"^\s*(\d+)(?:  |$)", output, re.MULTILINE)
    if code != 0 or "10" not in listed or "12" in listed:
        problems.append(f"lines CH-MARA: exit {code}, lines {listed}")
    code, output = run_stage(["lines", "SC02"], folder)
    listed = [int(number) for number in re.findall(r"^\s*(\d+)(?:  |$)", output, re.MULTILINE)]
    if code != 0 or (listed[:1], listed[-1:]) != ([33], [48]):
        problems.append(f"lines SC02: exit {code}, first and last {listed[:1]} {listed[-1:]}")
    code, output = run_stage(["lines", "SC01-D03"], folder)
    listed = [int(number) for number in re.findall(r"^\s*(\d+)(?:  |$)", output, re.MULTILINE)]
    if code != 0 or listed != [20, 21, 22]:
        problems.append(f"lines SC01-D03: exit {code}, lines {listed}")
    code, output = run_stage(["lines", "oven"], folder)
    listed = [int(number) for number in re.findall(r"^\s*(\d+)(?:  |$)", output, re.MULTILINE)]
    if code != 0 or listed != [10, 51]:
        problems.append(f'lines "oven": exit {code}, lines {listed}')
    code, output = run_stage(["lines", "PR-NOTHING"], folder)
    if code != 2:
        problems.append(f"lines on a record that does not exist exited {code}, not 2")
    report(not problems, "commands: lines for a character (cue lines left out), a scene, a speech, plain words, and a "
           "missing record (exit 2)", shorten(problems))

    # selftest
    problems = []
    code, output = run_stage(["selftest", "--prepare"], folder)
    handout = folder / "For machines - do not edit/handouts/U-00-SELFTEST.md"
    if code != 0 or not handout.is_file():
        problems.append(f"selftest --prepare exited {code}: {output.strip()}")
    else:
        text = handout.read_text(encoding="utf-8")
        for wanted in ("SC99-SH010", "SC99-SH200", "### SHOT", "END OF FILE | Self-test shots | 20 records"):
            if wanted not in text:
                problems.append(f"the handout lacks {wanted!r}")
        if "61 lines" not in output or "works here" not in output:
            problems.append(f"prepare did not report the story's lines and the ZIP test: {output.strip()}")
    identifiers = [f"SC99-SH{number * 10:03d}" for number in range(1, 21)]
    inbox = folder / "For machines - do not edit/inbox/U-00-SELFTEST.md"
    inbox.write_text("\n".join(selftest_shots(identifiers) + ["END OF FILE | Self-test shots | 20 records", ""]),
                     encoding="utf-8")
    code, output = run_stage(["selftest", "--score", "--surface", "claude_code"], folder)
    record = next(record for record in parse_file(folder / "00 Start here.md", "00 Start here.md", SCHEMA).records
                  if record.type_name == "PROJECT")
    if code != 0 or record.get("batch_size") != "18" or record.get("surface") != "claude_code" or inbox.exists():
        problems.append(f"a full self-test did not give batches of 18: exit {code}, batch {record.get('batch_size')}, "
                        f"output {output.strip()[:300]}")
    run_stage(["selftest", "--prepare"], folder)
    lines = selftest_shots(identifiers)
    cut = lines[:len(lines) - 30]
    inbox.write_text("\n".join(cut) + "\n", encoding="utf-8")
    code, output = run_stage(["selftest", "--score"], folder)
    record = next(record for record in parse_file(folder / "00 Start here.md", "00 Start here.md", SCHEMA).records
                  if record.type_name == "PROJECT")
    if code != 0 or record.get("batch_size") != "12":
        problems.append(f"a cut-off self-test did not give batches of 12: exit {code}, batch {record.get('batch_size')}")
    form, _ = form_problems(folder, 1)
    if form:
        problems.append("FORM checks after the self-test: " + shorten(form, 3))
    report(not problems, "commands: selftest --prepare (issued IDs, handout with the SHOT template) and --score (20 "
           "complete shots give batches of 18; a cut-off reply gives 12; the test shots are deleted)", shorten(problems))

    # A prose project: chapter stubs; only the AI's first and last lines are missing at step 1.
    problems = []
    prose_parent = work / "prose"
    prose_parent.mkdir()
    folder, output = make_project(FIXTURES / "The lamp keeper - chapters.md", prose_parent)
    code, output = run_stage(["read"], folder) if folder else (1, output)
    if code != 0:
        problems.append(f"read exited {code}: {output.strip()}")
    else:
        form, files = form_problems(folder, 1)
        others = [problem for problem in form if not (problem.check_id == "FORM-05"
                                                      and problem.field_name in ("first_line", "last_line"))]
        if others or len(form) != 6:
            problems.append(f"FORM checks at step 1: {len(form)} lines, other than first and last lines: "
                            + shorten(others, 3))
        merged, _ = merge_copies(files, SCHEMA)
        chapter = merged.get(("CHAPTER", "CP02"))
        expect(problems, "CP02", (chapter.get("title"), chapter.get("lines"), chapter.get("words")) if chapter else None,
               ("II. The Threshold", "17-27", "51"))
        choice = merged.get(("CHOICE", "CHOICE-004"))
        expect(problems, "prose format choice checkpoint", choice.get("checkpoint") if choice else None, "p")
        if (folder / "For machines - do not edit/speeches.json").exists():
            problems.append("speeches.json was written for prose")
    report(not problems, "commands: read on a prose project (chapter stubs in 05 Story plan; at step 1 only the AI's "
           "quoted first and last lines are missing)", shorten(problems))


# ---------------------------------------------------------------- group 3: test T1 on the real stories

def outside_repository(path):
    return REPOSITORY not in Path(path).resolve().parents


def group_t1_catch(story, work):
    label = "T1 The Catch"
    if not story or not Path(story).is_file():
        report(None, label, "skipped: story not present")
        return
    parent = work / "t1 catch"
    parent.mkdir()
    folder, output = make_project(Path(story), parent)
    if folder is None:
        report(False, label, output)
        return
    code, output = run_stage(["read"], folder)
    print("      " + output.strip().replace("\n", "\n      "))
    problems = []
    if code != 0:
        report(False, f"{label}: stage.py read", output.strip())
        return
    if not outside_repository(folder):
        problems.append("the project was made inside the repository")
    story_map = json.loads((folder / "For machines - do not edit/story map.json").read_text(encoding="utf-8"))
    speeches = json.loads((folder / "For machines - do not edit/speeches.json").read_text(encoding="utf-8"))["speeches"]
    expect(problems, "lines", story_map["line_count"], 1852)
    expect(problems, "scene heading lines", [scene["heading_line"] for scene in story_map["scenes"]], CATCH_HEADING_LINES)
    expect(problems, "scene count", len(story_map["scenes"]), 30)
    expect(problems, "speeches", len(speeches), 221)
    scene = next((scene for scene in story_map["scenes"] if scene["id"] == "SC10"), None)
    expect(problems, "SC10 lines", scene["lines"] if scene else None, [397, 489])
    ten = [speech for speech in speeches if speech["scene"] == "SC10"]
    expect(problems, "SC10 speeches", len(ten), 16)
    if ten:
        expect(problems, "SC10 first speech", (ten[0]["id"], ten[0]["text"]), ("SC10-D01", "Kitchen."))
        expect(problems, "SC10 last speech", (ten[-1]["id"], ten[-1]["text"]), ("SC10-D16", "Nobody leave this room."))
    expect(problems, "the card at line 488", [(card["line"], card["text"], card["shot"]) for card in scene["cards"]]
           if scene else None, [(488, "THE CATCH", "SC10-SH990")])
    tablet = next((scene for scene in story_map["scenes"] if scene["heading_line"] == 838), None)
    expect(problems, "(ON THE TABLET)", (tablet["presentation_note"], tablet["presentation"]) if tablet else None,
           ("ON THE TABLET", "on_screen"))
    if not any(odd["kind"] == "presentation" and odd["lines"] == [838, 838] for odd in story_map["odd_lines"]):
        problems.append("(ON THE TABLET) is not in the odd-lines report")
    expect(problems, "the end card", [(card["line"], card["shot"]) for card in story_map["scenes"][-1]["cards"]],
           [(1852, "SC30-SH990")])
    records, _ = merge_copies(Project(folder, SCHEMA, WORDS).load_record_files(), SCHEMA)
    record = records.get(("SCENE", "SC10"))
    expect(problems, "SCENE SC10 record", (record.get("lines"), record.get("transition_out"),
                                           len(record.get_all("speaking")),
                                           any("SC10-SH990" in note for copy in record.copies for note in copy.notes))
           if record else None,
           ("397-489", "cut_to_black", 4, True))
    record = records.get(("SCENE", "SC15"))
    expect(problems, "SCENE SC15 presentation", (record.get("presentation"), record.get("host")) if record else None,
           ("on_screen", "open"))
    record = records.get(("CHARACTER", "CH-SAYE"))
    expect(problems, "CH-SAYE names", record.get("names") if record else None, "SAYE, DR SAYE")
    form, _ = form_problems(folder, 1)
    if form:
        problems.append("FORM checks at step 1: " + shorten(form, 3))
    report(not problems, f"{label}: 1,852 lines; 30 scenes at the listed heading lines; 221 speeches; SC10 = lines "
           "397-489 with 16 speeches (SC10-D01 \"Kitchen.\" to SC10-D16 \"Nobody leave this room.\"); \"= THE CATCH\" "
           "at line 488 becomes a card (SC10-SH990); \"(ON THE TABLET)\" noted as presentation; FORM checks at step 1 "
           "find nothing", shorten(problems))
    estimate = story_map.get("first_estimate") or {}
    central = estimate.get("central_s")
    within = central is not None and 1926 <= estimate.get("low_s", 0) and estimate.get("high_s", 0) <= 2309 \
        and 1926 <= central <= 2309
    report(within, f"{label}: the first estimate from the words lies between 1,926 and 2,309 s (the counts D13 §4.1 "
           "uses: 1,579 speech words, 7,091 action words, 221 speeches, 7 beats)",
           f"{estimate.get('low_s')} to {estimate.get('high_s')} s, central {central} s; counts "
           f"{story_map['counts'].get('dialogue_words')}, {story_map['counts'].get('action_words')}, "
           f"{story_map['counts'].get('speeches')}, {story_map['counts'].get('beat_marks')}. WP7's estimate.py writes "
           "the estimate file")


def group_t1_long_places(story, work):
    label = "T1 The Long Places"
    if not story or not Path(story).is_file():
        report(None, label, "skipped: story not present")
        return
    parent = work / "t1 long places"
    parent.mkdir()
    folder, output = make_project(Path(story), parent)
    if folder is None:
        report(False, label, output)
        return
    code, output = run_stage(["read"], folder)
    print("      " + output.strip().replace("\n", "\n      "))
    if code != 0:
        report(False, f"{label}: stage.py read", output.strip())
        return
    problems = []
    if not outside_repository(folder):
        problems.append("the project was made inside the repository")
    story_map = json.loads((folder / "For machines - do not edit/story map.json").read_text(encoding="utf-8"))
    expect(problems, "lines", story_map["line_count"], 1444)
    expect(problems, "words", story_map["words"], 49152)
    expect(problems, "chapter count", len(story_map["chapters"]), 14)
    expect(problems, "chapter heading lines", [chapter["heading_line"] for chapter in story_map["chapters"]],
           LONG_PLACES_CHAPTER_LINES)
    expect(problems, "title line", story_map["title"]["line"], 1)
    expect(problems, "clean title proposed", story_map["title"]["clean"], "The Long Places")
    if not any(odd["kind"] == "front_matter" and odd["lines"] == [3, 3] for odd in story_map["odd_lines"]):
        problems.append("line 3 is not listed as front matter")
    if not any(odd["kind"] == "repeat" and odd["lines"] == [1415, 1441] for odd in story_map["odd_lines"]):
        problems.append("the repeated letter (lines 1415 to 1441) is not listed")
    form, files = form_problems(folder, 1)
    others = [problem for problem in form if not (problem.check_id == "FORM-05"
                                                  and problem.field_name in ("first_line", "last_line"))]
    if others:
        problems.append("FORM checks at step 1 other than the AI's first and last lines: " + shorten(others, 3))
    merged, _ = merge_copies(files, SCHEMA)
    chapter = merged.get(("CHAPTER", "CP01"))
    expect(problems, "CHAPTER CP01", (chapter.get("title"), chapter.get("lines")) if chapter else None,
           ("I. The Lamps Are Old", "5-83"))
    report(not problems, f"{label}: 1,444 lines; 49,152 words; 14 chapters at lines 5, 84, 163, 262, 385, 476, 541, "
           "636, 777, 858, 943, 1048, 1155, 1287; the title and front matter placed; chapter stubs written",
           shorten(problems))


def main():
    parser = argparse.ArgumentParser(description="WP3 acceptance: the story reader and test T1.")
    parser.add_argument("catch", nargs="?", help="The Catch story file (for T1)")
    parser.add_argument("long_places", nargs="?", help="The Long Places story file (for T1)")
    parser.add_argument("--keep", action="store_true", help="keep the temporary folder and print its path")
    arguments = parser.parse_args()
    work = Path(tempfile.mkdtemp(prefix="stage-wp3-"))
    try:
        for group in (lambda: group_fixtures(work), group_excerpt, lambda: group_adopt_contract(work),
                      lambda: group_commands(work),
                      lambda: group_t1_catch(arguments.catch, work),
                      lambda: group_t1_long_places(arguments.long_places, work)):
            try:
                group()
            except Exception as error:  # a crash in one group is a failure, and the other groups still run
                report(False, "a test group stopped with an error", f"{type(error).__name__}: {error}")
    finally:
        if arguments.keep:
            print(f"INFO  kept the temporary folder: {work}")
        else:
            shutil.rmtree(work, ignore_errors=True)
    failures = RESULTS.count("FAIL")
    print(f"RESULT: {'PASS' if failures == 0 else 'FAIL'} ({failures} failing groups)")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
