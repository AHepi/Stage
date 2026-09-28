# D14. Intake of Any Story Format, and of Thin or Non-English Sources

*Library file D14. Written 2026-09-27. Test sources: "The Catch" (screenplay in a variant markup, workshop revision of 25 September 2026) and "The Long Places" (a 14-chapter novella in Markdown).*

> **What this file is for**
> 1. It tells the pipeline what kind of file and what kind of story it has been given, from the content, before anything else runs.
> 2. It turns every file type into one of the two forms the pipeline reads (strict Fountain, or numbered prose paragraphs), with checks that catch silent damage.
> 3. It maps stage plays, comic scripts and game scripts onto screen units, and types the letters, lists and reports inside prose.
> 4. It expands a treatment, outline, synopsis or logline into scenes under an invention budget, every invention labelled and approved at a new checkpoint T.
> 5. It sets how to work with non-English or mixed-language sources, and checks each spoken language against what voice and video models can say.

**Evidence labels.** [V] verified at the named source on 2026-09-27, or by my own test (M1–M8, listed in Sources); [V-sec] secondary source only; [U] unverified; [J] my judgment. Tool versions and prices go stale; re-check any over a month old (C5 R22).

**Fact-check pass, 2026-09-27.** A second reader re-opened more than 30 of the cited pages and re-ran the own tests. Corrected: the "Brick & Steel" fingerprint (8 headings, 6 `>` lines, 26 capital lines, not 6, 1 and 17); the FDX paragraph counts (23 Action, not 20); the FDX case rule (Fountain headings are case-insensitive, so only cues need capitals); Recipe I5 (Cowork runs on Anthropic's servers, so local Tesseract needs Claude Code, per D1). Added: claude.ai project-file limits; the chat-app conversion route (Recipe I2); rules R31–R37 (no target runtime, no code execution, a language outside Anthropic's table, source-marked breaks, rights before conversion, unresolved revisions, quoted songs); resolved two open questions as [V-sec] (Tesseract 5.5.3; Google Docs suggestions). Every quoted line from *The Catch* and *The Long Places* was re-checked against the files and is verbatim. Pages that refused automated fetching (Final Draft and Celtx help centres, HTTP 403) were checked through search-result extracts or left as the first writer's [V].

**Place in the pipeline.** This file widens C5's stage 0 (intake) and hands C5 R1–R3 a clean file. It does not repeat what exists: C5 R1–R3, P8 and §3 (Fountain, FDX and PDF screenplays; prose segmentation); A3 §4.1–4.3 (parsing Fountain and *The Catch*'s markup); A3 §7 (adapting prose); D2 (whole-work plan and step outline). For a thin source, checkpoint T comes before D2's checkpoint M.

---

## 0. Words this file uses (one word per concept)

| Word | Plain meaning |
|---|---|
| **Source** | The story the user hands over, in whatever form. |
| **Container** | The file type holding the source (.docx, .pdf, .epub, .fdx, .md and so on). |
| **Kind** | What sort of story text it is: screenplay, stage play, prose, treatment, outline, synopsis, logline, comic script, game script. |
| **Dialect** | The markup convention inside the text (strict Fountain, *The Catch*'s variant, Markdown, standard play layout). |
| **Fingerprint** | A count of telltale line patterns, used to detect kind and dialect from the content rather than the file name. |
| **Extraction** | Getting plain text out of a container. |
| **Text layer** | The hidden, selectable text inside a PDF; a scanned PDF has none. |
| **OCR** | Optical character recognition: software that reads letters from a picture of a page. |
| **Normalized source** | The one clean file the pipeline reads: `source.fountain` or `source_paragraphs.md`. |
| **Block** | One paragraph, speech, heading or embedded document in the normalized source, with an ID. |
| **Source map** | A file saying, for every block, where it came from in the original. |
| **Embedded document** | A letter, list, report, message, sign or song quoted inside the story. |
| **Density** | Source words per minute of planned film. |
| **Thin source** | A source too low in density to extract scenes from; the pipeline must author them. |
| **Invention** | Anything the pipeline adds that the source neither states nor implies (A3 P2). |
| **Invention budget** | The user's limit on how much, and what kind of thing, may be invented. |
| **Checkpoint T** | The user's approval of an expanded thin source, inventions highlighted. |
| **French scene** | In theatre, a unit that begins and ends when a character enters or leaves. |
| **Working language** | The language the pipeline analyses in. **Spoken language** is the language a line is performed in. |

---

## 1. Core principles

1. **Detect from content, never from the file name** [J]. *The Catch*'s markup is also valid Markdown: `## INT.` renders as a heading and `>` as a quotation, so a `.md` extension or a chat window would change its meaning without warning.
2. **Keep the original untouched, with its hash** (C5 R2). Every later file cites back to it through the source map.
3. **Programs extract; the LLM classifies and checks** [J]. A program copies letters; the LLM decides what each block is and flags doubts. A vision model reading a degraded page tends toward "overreliance on linguistic priors" [V, S27]: it may "correct" a dialect, a meaningful misspelling or backwards text.
4. **Count before and after** [J, extends A3 §4.3 step 10]. Headings, cues, chapters and documents are counted in the original and the normalized file; every difference is a logged change.
5. **Nothing silent** [J]. Every conversion step, dropped block and forced element is logged with its reason.
6. **Invention is labelled and budgeted** (A3 P2 and R24, C5 V12); the user approves each invented scene.
7. **Keep the original words; translate beside them** [J].
8. **Ask for a better file before repairing a bad one** [J]: an app export or the original document beats OCR.

---

## 2. Detect: the triage

Three questions, in order: **container** (can a program read its text? Section 3); **kind and dialect** (the fingerprint, 2.1); **density** (Section 7.1), which decides whether the pipeline extracts scenes or authors them.

### 2.1 The fingerprint

A short script counts line patterns (a **fingerprint**: how many lines of each telltale shape the file has). My run on both test sources and on Fountain's sample script "Brick & Steel" [V, own tests M6 and M8]:

| Pattern | Suggests | *The Catch* | *The Long Places* | "Brick & Steel" |
|---|---|---|---|---|
| Line starts `## INT` / `## EXT` | *Catch* dialect heading (A3 §4.3) | 30 | 0 | 0 |
| Line starts `INT`, `EXT`, `EST`, `I/E` (or forced `.`) | Fountain or plain screenplay heading | 0 | 0 | 8 (6 with a prefix, 2 forced with `.`) |
| Line starts `@` | Forced character cue | 221 | 0 | 0 |
| Line starts `=` | Fountain synopsis; in *The Catch*, title page and cards | 8 | 0 | 0 |
| Line starts `>` | Fountain transition or centred text (`>…<`); Markdown quotation | 3 (all transitions) | 69 | 6 (5 centred, 1 transition) |
| Line starts `# ` | Markdown chapter; Fountain section | 0 | 15 | 0 |
| Whole paragraph in `*…*` | Markdown italic block | 0 | 180 | 0 |
| Line `---` | Markdown section break | 0 | 15 | 0 |
| All-capital line with no marker (`@`, `>`, `.`, `=`) and no heading prefix, after the title page | Cue, transition or on-screen text | 2 | 0 | 26 (20 cues, 6 transitions) |
| Parenthetical on its own line | Delivery note | 18 | 0 | 6 |

Read the last-but-one row with care: in strict Fountain an unmarked capital line *is* how cues and transitions are written, so a high count means ordinary Fountain; in *The Catch* every cue carries `@`, so its two unmarked capital lines are something else (E1).

Other telltales [J]: `ACT I`, `Scene 1`, `At Rise:` (stage play, Section 5); `PAGE ONE`, `Panel 1.`, `CAP:`, `SFX:` (comic script); `:: Name` (Twine), `title:` … `---` … `===` (Yarn), `=== knot ===` with lines starting `*` (Ink) (game scripts, Section 6); present-tense prose without dialogue, with phrases such as "we meet" or "in act two" (treatment or outline, Section 7).

### 2.2 Decision rules for detection

- **R1.** If any line starts `## INT` or `## EXT`, then use the *Catch* dialect (A3 §4.3) whatever the file is called, because read as Fountain every scene heading vanishes, and read as Markdown each becomes a document heading [V, S3; own test M6].
- **R2.** If lines start `# ` and there are no scene headings, then treat them as chapter or part headings of prose, because Fountain drops sections from output [V, S3] and *The Long Places* would lose its 14 chapter titles.
- **R3.** If prose has lines starting `>`, then treat them as quotations (embedded documents, Section 9), never as transitions, because *The Long Places* has 69 such lines and none is a transition [V, own test M6].
- **R4.** If one file mixes kinds (a screenplay pasted into a Word file with notes around it), then split it into regions, detect each, and ask which regions are the story, because notes and drafts are not story.
- **R5.** If the kind is still unclear, then show the user the first 40 lines with the proposed reading and ask, because every later ID depends on it (C5 R1).
- **R31.** If the user has not yet chosen a target runtime, then ask for a rough one (a short under 40 minutes, or a feature of 90–120), record it as `density_runtime_basis: provisional`, and let D2's M0 confirm it later, because density (Section 7.1) cannot be computed without minutes, and a guess that is labelled can be corrected while an unlabelled one silently decides whether the pipeline invents [J].
- **R35.** If the source is someone else's work, or an EPUB, or a file the user did not write, then run D4's rights intake (D4 Recipe 1, `rights_status`) before any conversion, and stop at DRM (Section 3.1), because conversion copies the work, and D4 makes rights a condition of checkpoint A [J; D4 §7.1].

**Recipe I1. Triage (5 minutes; no cost).** Say: *"Run intake triage on this file. Tell me the container; whether it has a text layer; the kind and dialect, with fingerprint counts; the languages; the word count; and the density class for a film of [N] minutes (if I have not given N, ask me for a rough length and mark it provisional). Convert nothing yet. List what you are unsure of as questions."* Check the counts against what you know (*The Catch*: 30 scenes), then say "go on" or correct it. If the app cannot run code, add: *"Do not count by eye. List every matching line with its line number instead, and I will check the list"*, because an LLM reading a long file miscounts, while a list can be checked [J].

---

## 3. Convert: from any container to text

### 3.1 Conversion routes

| Container | Best route | What gets lost, and the check |
|---|---|---|
| Word (.docx), .odt, .rtf | pandoc 3.11 (29 Aug 2026) [V, S2]: `pandoc -f docx+styles -t markdown --track-changes=all in.docx -o out.md`; pandoc reads docx, odt, rtf, epub, html and Markdown, not PDF (PDF is absent from its input list) [V, S1] | Indentation is dropped [J], but the `styles` extension adds "custom-styles attributes for all docx styles" [V, S1], so a script typed with named styles (Character, Dialogue) keeps them. The default `accept` silently applies tracked changes; `accept` and `reject` both "ignore comments"; `all` keeps insertions, deletions and comments, marked, with author and time [V, S1]. `--track-changes` "only affects the docx reader" [V, S1]: for .odt, ask the writer which version is final. |
| Google Docs | File > Download > Markdown (.md) or .docx [V, S16] | Suggestions: use .docx with `--track-changes=all`. Google's suggestions are reported to arrive in Word as tracked changes [V-sec, S45, a 2014 blog], with some user reports of failures [V-sec]; check by counting the `insertion` and `deletion` marks pandoc writes (R36). |
| EPUB | `pandoc -f epub -t markdown` [V, S1], or calibre 9.15.0 `ebook-convert book.epub book.txt --txt-output-formatting=markdown` [V, S29] | An EPUB is "a ZIP-based archive" whose spine gives "the default reading order" [V, S28]; tag front and back matter (Section 9). **DRM:** "Most purchased EPUB books have DRM. This prevents calibre from opening them" [V, S30]. Stop and ask for a DRM-free copy; in the US "No person shall circumvent a technological measure…" (17 U.S.C. §1201) [V, S31]. |
| PDF with text layer, prose | Plain extraction (pypdf, pdftotext) | Broken or spaced words (3.3). |
| PDF with text layer, script or play | **Layout** extraction (pypdf `extraction_mode="layout"`, `pdftotext -layout`) [V, own test M1], or an app: Final Draft 12/13 imports PDF "with a high degree of accuracy, including the title page" [V, S9]; Highland Pro "melts" script PDFs [V, S14] | Plain mode loses the indentation that says what each line is (M1). |
| Scanned PDF, photos | OCR (3.2) | Check every page. |
| Final Draft (.fdx) | A short Python script reads each `<Paragraph Type="…">` (Scene Heading, Action, Character, Dialogue, Parenthetical, Transition, General), including those nested inside a `<DualDialogue>` block [V, own test M2] | **Case:** text is stored as typed (`Ext. Brick's patio - day`; cue `Steel`) and only displayed in capitals [V, M2]. Headings survive, because Fountain reads heading prefixes "case insensitive" [V, S3]; cues do not, because a Fountain cue must be "entirely in uppercase" [V, S3], so upper-case every Character paragraph or force it with `@`. screenplain writes FDX, HTML and PDF from Fountain; its documentation shows no FDX input [V, S5]. |
| Other screenwriting apps | Their Fountain export (3.4) | App notes: keep as `[[notes]]` or drop with a log line. |
| HTML, Markdown, text | Read directly; HTML via pandoc | Encoding (3.5). |

**What claude.ai accepts** [V, S17, page dated 23 Jul 2026]: PDF, DOCX, CSV, TXT, HTML, ODT, RTF, EPUB, JSON, XLSX (XLSX only with code execution on); images JPEG, PNG, GIF, WebP up to 8000×8000 pixels. In a chat: 500 MB a file, 20 files a chat, PDFs up to 1,000 pages. In a Project's files: 30 MB a file, "Text extraction only (except for multimodal PDFs)". For non-PDF documents "Claude extracts text only", so embedded images in a Word file are not read. PDFs "of 100 pages or fewer" have text and images read; "For PDFs from 101 to 1000 pages, Claude processes text only". [J] So a scanned script over 100 pages yields nothing past what its text layer holds (for a pure scan, nothing); split it into parts of 100 pages or fewer, or OCR it first. `.md` is not in the list; rename it `.txt` (R1 then still decides how it is read). A Word file uploaded straight into the chat loses its style names and tracked-change marks [U: not documented either way]; convert it with pandoc (Recipe I2) when styles or revisions matter.

**R32.** If the chat app can run code (claude.ai with "Code execution and file creation" on; D1 §3.1), then do conversions in its sandbox with Recipe I2; if it cannot, then ask the writer for an app export or a plain-text save (Word: File > Save As > Plain Text; Google Docs: File > Download > Markdown), have the LLM list rather than count (Recipe I1), and run the real conversion and validator at the next chance, because an LLM retyping a file is not an extraction and may "fix" it (principle 3) [J; D1 R3].

**R36.** If a Word or Google Docs file might hold unresolved revisions, then convert with `--track-changes=all`, count the insertion, deletion and comment marks, and, if any exist, ask the writer which version is the story before normalizing, because the default silently accepts every change [V, S1] and a rejected draft line would otherwise become source [J].

**Recipe I2. Convert inside the chat app (10–20 minutes; no extra cost; claude.ai with code execution on).** Upload the file, then say:
*"Stage 0 conversion. In your sandbox: install pypdf and pypandoc_binary (it includes pandoc). Keep my original file untouched and give me its SHA-256 hash. Convert it to plain text: Word or ODT with pandoc (`-f docx+styles --track-changes=all` for Word); EPUB with pandoc; a PDF with pypdf in layout mode. Then compute the intake fingerprint on both the original and the converted text, show the two tables side by side, list every difference, and give me the converted file to download. Do not retype, correct or summarize any of the text. If a step needs a program you cannot install, stop and tell me which one."*
Check: the hash is given; the counts match what you know (for *The Catch*: 30 headings, 221 cues); the tracked-change count is zero or you have answered R36. pypandoc_binary ships Linux wheels [V, S46]; whether the sandbox can install Tesseract (a system program, not a Python package) is [U]; if it cannot, OCR goes to Recipe I5.

### 3.2 OCR: reading scanned pages

| Tool | Cost | Use |
|---|---|---|
| Tesseract 5 ("more than 100 languages" "out of the box" [V, S18]; latest 5.5.3, 24 Jul 2026 [V-sec, S48]) | Free | `tesseract page.png out -l eng+tur --psm 4 tsv` (`-l eng+tur` reads English and Turkish together). Works best at "at least 300 dpi"; `--psm 4` means "Assume a single column of text of variable sizes" [V, S19]; `tsv` gives each word's `left`, `top`, `width`, `height`, `conf` (confidence, 0–100) and `text` [V, S20], which recovers indentation and flags doubtful words. |
| OCRmyPDF 17.12.1 (16 Sep 2026) [V, S21] | Free | Adds a text layer: `ocrmypdf -l eng --deskew --rotate-pages --sidecar out.txt in.pdf out.pdf` [V, S22]. Pages already holding text: `--skip-text` skips them, `--force-ocr` rasterizes and re-reads everything, `--redo-ocr` removes old OCR and redoes it [V, S23]; `--redo-ocr` cannot be combined with `--deskew` or other image cleaning [V, S22]. |
| Google Document AI (Enterprise Document OCR) | $1.50 per 1,000 pages from 1,000 to 5 million a month, $0.60 above; the first tier is listed at $0.00 (the page counts in "count", unit not stated) [V, S24] | Cloud. |
| Amazon Textract (Detect Document Text) | $0.0015 a page for the first million a month (price shown for US West, Oregon); new AWS customers get 1,000 pages a month free for three months [V, S25] | Cloud. |
| Mistral OCR 4.1 (16 Jul 2026) | "$4 /1000 Pages"; $5 per 1,000 annotated pages; a batch endpoint exists, discount not stated on the model page [V, S26] | Cloud. |
| An LLM reading page images | Plan cost | Good at telling a cue from action, but may "fix" text [V, S27]; use it to classify and compare, not as the only reader [J]. |

**Privacy** [J, D1 §8]: cloud OCR sends the manuscript to another company; for an unpublished script prefer Tesseract on your own computer.

**Recipe I5. OCR a scanned script (30–90 minutes for 40–120 pages; free).** In Claude Code on your own computer (D1 §3.2), which can install and run Tesseract there. Cowork is not the tool for this step: its work "runs on Anthropic's servers, in an isolated environment" and it only reads and writes your local files (D1 §3.2 and §13, [V] there). Try Recipe I2's sandbox first only if it reports Tesseract installed.
1. *"Count characters extracted per page; list pages under 50."* Mostly near zero means a scan.
2. *"Install OCRmyPDF and Tesseract with [language] data. OCR with deskew and rotation fix; write a sidecar text file and a TSV file per page."*
3. For a script or play: *"Rebuild each line's indentation from word positions, group left edges into columns, and label them from left to right."* In my layout test the order was action, dialogue, parenthetical, cue, with transitions pushed right [V, own test M1].
4. *"List pages with mean confidence below 85 and words below 60."* (Thresholds [J].)
5. *"Show me the first, middle and last pages as images beside your text."* Check names, numbers and deliberate oddities (dialect, backwards text).
6. Continue with C5 Recipe 2.

### 3.3 Three silent extraction failures, measured

- **M1, plain extraction erases what a line is** [V, own test M1]. Fountain's "Brick & Steel" PDF through pypdf 6.19.0 in plain mode gave `STEEL` / `Beer's ready!` with no blank lines or indents, so dialogue and action look alike, and two simultaneous speeches became one line pair. Layout mode kept `STEEL` at column 25, its dialogue at column 12, and the simultaneous speeches side by side.
- **M3, wrong character mapping** [V, own test M3]. Dark Horse's script guide extracts as `PanelWnkWNumberWyourWpanelsk`: spaces became `W`, full stops `k`, digits other letters. No error is raised.
- **M4, split and spaced words** [V, own test M4]. Samuel French's guide extracts with "cont ain", "Th is" and "Y o u r  N a m e".

All three were re-run on 2026-09-27 with pypdf 6.19.0 and reproduced exactly (M3 also turns `(five panels)` into `efiveWpanelsf`).

**R6.** If text came from a PDF, then compare three sample pages (first, middle, last) as images against the text before normalizing, and switch to OCR if more than about 1 word in 50 is wrong [J], because extraction fails without errors (M1, M3, M4).

**R7.** If a screenplay or play arrives as PDF, then extract in layout mode or through an app that rebuilds elements, never in plain mode, because indentation alone tells a cue from dialogue from action [V, own test M1].

### 3.4 Screenwriting app exports

| App | Exports | Imports / notes |
|---|---|---|
| Final Draft 13 | File > Export > Script: .fdx, .fdxt, .fcf, HTML, RTF, Plain Text, "Text with Layout (.txt)" (white space imitates the indents), Scheduling Export (.sex), Avid, "Tab-Delimited Dialogue" (every speech with character and scene number, for a spreadsheet) [V, S7]; PDF | Imports PDF (FD 12 and 13 only; earlier versions cannot), .txt, .rtf, .fcf [V, S6, S9]; "cannot open or import .fountain or .spmd files" [V, S8], but a Fountain-style text saved as .txt imports "formatted correctly" [V-sec, S8 extract]. Ask for .fdx, else "Text with Layout". |
| Celtx (web) | ".txt or .fountain"; PDF via Print/Download PDF [V, S11, S13] | Imports text-based PDF, Fountain, .celtx, .fdx, .docx, .rtf, .txt, .html; "Scanned PDFs will not work without Optical Character Recognition" [V, S12; first writer's check; the help centre refused automated re-fetching on 2026-09-27]. |
| WriterDuet | .wdz, PDF, .fdx (with or without notes), .fountain, .celtx, .docx, .rtf, .txt, .html, .csv, .json [V, S10] | "We cannot guarantee the formatting for some file types (e.g. Microsoft Word) will be one-to-one upon export" [V, S10]. |
| Highland Pro (Mac, iPhone, iPad, Apple Vision Pro) | Fountain, .fdx, PDF, .docx [V, S14, S15] | "PDF Melting" turns Final Draft and Fountain PDFs back into editable scripts; $9.99 a month or $59.99 a year after a 30-day trial [V, S14]. |

**R8.** If the user wrote in a screenwriting app, then ask for its Fountain export first, then .fdx, then "Text with Layout", then PDF, because each step down loses more structure [J].

### 3.5 Encoding and letters

**R9.** If text arrives, then store it as UTF-8, NFC (one code point per accented letter), line feeds, no byte-order mark, and log any change, because one letter can be stored two ways and names then fail to match [J]. Both test sources already comply [V, own test M5]; Fountain's own sample "Brick & Steel" does not: it mixes Windows (CRLF) and Unix (LF) line endings, 144 of its lines ending CRLF [V, own test M8], so a line-count check that ignores endings would disagree with itself. Apply NFKC only to PDF-derived text, where it turns ligatures such as "ﬁ" back into "fi" [V, own test M5], never to a whole source (it also rewrites characters such as "₂").

**R10.** If names contain letters whose capitals do not round-trip, then store the canonical name as spelled and generate capitals for display only, because in Python "Kırk Oda".upper() is "KIRK ODA", which lower-cases to "kirk oda", and "İstanbul".lower() gains a combining dot [V, own test M5]. *The Long Places* has 51 dotless ı characters [V, own test M5]; A3 Ex5's heading `KIRK ODA` is a display label, while `LOC-KIRKODA` keeps "Kırk Oda".

---

## 4. Normalize: two canonical forms and a source map

Every source ends as **`source.fountain`** (anything performed, including expanded thin sources) or **`source_paragraphs.md`** (prose, one block per line with an ID), as C5 §3 requires. Beside it the intake writes **`source_map.json`** (per block: `block_id`, such as `L0674` or D2's `ch08.p027`; `block_type`; `original_ref`; `provenance`; Section 11) and **`intake_log.json`** (per step: tool, version, command, input and output hashes, counts before and after, each forced or dropped element with its reason).

**R11.** If an element must be forced to parse (a cue with lower-case or non-Latin letters, a heading with a non-English prefix), then force it with Fountain's markers (`@` for a character, `.` for a heading) rather than rewriting its words, because Fountain provides exactly this: forcing a character "is helpful for names that require lower-case letters, and for non-Roman languages" [V, S3].

**R12.** If the source uses a convention Fountain has syntax for, then use that syntax: simultaneous speech with `^` after the second cue, lyrics with `~`, centred text `>TEXT<`, notes `[[ ]]` [V, S3], because each maps to a breakdown field and a home-made marker breaks other tools.

---

## 5. Stage plays to screen

**Detecting a play.** Samuel French's guide [V, S33]: `ACT II` / `Scene 6`; "Setting" and "At Rise" describe the stage and opening action; the speaker's name "centered or set 3.5" from the Left Edge of the Paper in ALL CAPS"; longer directions "on the following line in parentheses, three indents in"; simultaneous dialogue "side-by-side"; scenes end with "Blackout," "Curtain," etc. There is no INT/EXT, and one set often stands for many places.

| Stage element | Screen unit | Breakdown handling |
|---|---|---|
| Act, scene | Sequence; scene candidate | `stage_unit {act, scene}` on each scene; IDs per C5 §10.1. |
| French scene ("a scene in which the beginning and end are marked by a change in the presence of characters onstage" [V, S32]) | Beat boundary; a new screen scene only if the film moves the action | List in `stage_unit.french_scenes`; strong beat candidates (A2). |
| Setting / At Rise | Heading and establishing action | Place `fact` if named; INT/EXT usually `inference`. |
| Stage direction | Action | `fact`; a stage-only device (a light change to show a thought) is translated by the A3 §7.2 ladder, not copied. |
| Offstage event reported in dialogue | Candidate dramatized scene | Opening it up is `invention`, logged. |
| Soliloquy (thoughts spoken aloud, alone or to the audience; A1 §2) | Voice-over over behaviour; direct address to the lens; a line to a present listener; cut | One series rule for the play (D2 R14); A1 R44: a look into the lens is direct address, never an accident. |
| Aside (a remark others on stage do not hear; A1 §2) | Glance to lens; voice-over; quiet line plus reaction shot | `address` on the line (Section 11). |
| Blackout, Curtain, Intermission | Scene end; cut to black; act break | Cut record (C5). |

Direct address can carry a whole adaptation: *Fleabag* is "based on her one-woman show first performed in 2013 at the Edinburgh Festival Fringe", and its protagonist "frequently breaks the fourth wall, providing exposition, internal monologues, and running commentary" [V, S34]. Opening up is invention even when the playwright does it: in *Glengarry Glen Ross* (1992), "Baldwin's character Blake was specifically written for the actor and the film, and is not in the play" [V, S35].

**R13.** If the source is a stage play, then decide once, as series rules, how soliloquies and asides play, and label every moved location and added scene `invention`, because a play's conventions are what an adaptation most visibly changes [J; D2 R14].

**R14.** If one stage set stands for several places, then split it into screen locations only on the text's evidence, else keep one and ask, because a wrong split forks every reference image (A3 R6).

---

## 6. Comic scripts and game scripts

**Comic scripts.** Dark Horse's format [V, S37]: `PAGE ONE (five panels)`; `Panel 1.` and a description; the speaker in capitals above the dialogue; `SFX:` and `CAP:` (caption) lines "listed in the order in which they should be read"; `CHARACTER (thought):` and `CHARACTER (OP):` (off-panel); "approximately 25 words per balloon, and about 50 words per panel, max". Mapping [J]: a panel is a shot candidate and a ready storyboard frame (C2), noted `[[PAGE 3 PANEL 2]]`; a page turn usually hides a reveal, so cut on it; captions become voice-over, on-screen text or nothing, decided once per work; SFX become sound cues (D9); thought balloons go down A3's externalization ladder. For finished comic art, ask for the script; the art becomes style reference (D5).

**Game scripts.** Ink marks a choice with `*` and moves between sections ("knots", headed `=== knot ===`) with a "divert arrow" `->` [V, S38]. A Yarn Spinner node runs from `title:` through `---` to `===`, and "a set of characters without spaces before a colon" at a line's start is the speaker [V, S39]. Twine's Twee 3 heads each passage `:: Passage Name [tags] {metadata}` [V, S40].

**R15.** If the source branches, then ask the user to choose one path (or the canonical ending), store it as `branch_path`, and flatten that path to Fountain, because a film is one path and the choice of ending is the user's [J].

**R16.** If a game line is a reusable remark with no scene (a "bark"), then drop it with a log line unless the user places it, because it has no event (A3 R1) [J].

---

## 7. Thin sources: treatments, outlines, synopses and loglines

### 7.1 Measuring thinness

The WGA's agreement defines a **screenplay** as "the final script with individual scenes, full dialogue and camera setups" and a **treatment** as material "in a form suitable for use as the basis of a screenplay" [V, S36]. Only the first gives the pipeline scenes to extract.

*The Catch* has 9,217 words [V, own count] for a natural runtime of about 35 minutes (D2 §6: 32–38): about 260 words per minute.

Density is a triage number only: it decides extract-or-author. It is not a runtime estimate; D2 R3 rejects words per minute for prose runtime "because words per minute vary too much with style", and D2 §6 and R3 stay the method for minutes [J].

| Density class | Words per minute [J] | Typical kind | Pipeline action |
|---|---|---|---|
| `full` | 150 or more, with dialogue | Screenplay, play, dense prose | Extract (C5, A3). |
| `partial` | 30–150 | Treatment, detailed outline, short story for a long film | Dramatize stated events; author dialogue and staging (D2 R6); checkpoint T for invented scenes. |
| `thin` | under 30 | Synopsis, logline, beat list | Interview the user, author the scenes, checkpoint T. |

### 7.2 The invention budget

The user picks one level before expansion:

| Level | May invent | May not invent |
|---|---|---|
| `minimal` | Connective action; unnamed places; wording of lines whose content is stated | New events, characters, reveals or endings |
| `moderate` | Scenes dramatizing stated events; minor characters with a function; dialogue | New cardinal events (D2); changed outcomes |
| `free` | New events and characters serving the stated ones | Anything contradicting a stated fact |

Every invention carries `serves_facts`, the stated facts it serves (A3 R24: "label it `invention` in the adaptation log with the source lines it serves").

### 7.3 Procedure T0–T6

**T0. Classify** the density (Recipe I1).

**T1. Fact list.** *"List every statement in the source as a numbered fact (F01, F02 …), quoting the words. Mark each `event`, `character`, `place`, `rule`, `tone` or `ending`. Add nothing."*

**T2. Gap list.** *"List what a screenplay needs that the facts do not give. Sort each gap into ASK (it changes what the story means: identities, motives, reveals, world rules, ending, tone, point of view, runtime, content limits) or DECIDE (connective or textural)."*

**T3. Interview.** *"Ask me the ASK questions one at a time, most important first, twelve at most, each with two or three options and a default. Record my answers as facts F-U01 … with `decided_by: human`."*

**T4. Expand one level at a time.** Logline → one-paragraph synopsis → treatment (present tense, a paragraph per sequence) → step outline in D2's format. *"Expand to the next level only. Mark every sentence no fact states with ⟨INV⟩ and the fact IDs it serves."* Each step-outline line gets `origin`: `source`, `dramatized_summary` or `invented`.

**T5. Checkpoint T.** A script counts scenes and events by origin and computes the invented share. The user sees the step outline with ⟨INV⟩ lines highlighted and answers "keep", "change" or "cut" for each invented scene ("Revise only step 7").

**T6. Author the screenplay.** One sequence per call, strict Fountain, each scene opening with a note such as `[[origin: invented; serves F03, F07]]`. The approved result becomes `source.fountain` with `source_type: authored_from_thin`; the thin original is kept as `source_original` with its hash. C5 stage 0 onward then runs as usual, but every block keeps its provenance, so a line the pipeline wrote is never later cited as the user's (D14-V5).

**R17.** If density is `partial` or `thin`, then run T0–T6 and stop at checkpoint T before D2's macro pass, because unapproved invention would become "source" for every later stage.

**R18.** If a gap changes what the story means, then ask; if it only connects or textures, then decide and label it, because meaning belongs to the user and a question costs less than a regenerated sequence (A3 P10).

**R19.** If the invented share exceeds the budget, then offer two or three independent expansions (C5 R14) instead of trimming one, because choosing between stories is the user's call.

**R20.** If the user supplies several thin documents (logline, character list, mood notes), then merge them into one fact list, each fact citing its document, because contradictions between them must surface as questions at T3.

---

## 8. Non-English and mixed-language sources

### 8.1 Working language

Anthropic scores Claude Sonnet 4.5 (extended thinking) on MMLU, a general-knowledge test professionally translated into 14 languages, relative to English: Spanish 98.2%, Italian 97.9%, Portuguese (Brazil) 97.8%, French 97.5%, Indonesian 97.3%, Arabic 97.2%, German 97.0%, Chinese (Simplified) 96.9%, Japanese 96.8%, Korean 96.7%, Hindi 96.7%, Bengali 95.4%, Swahili 91.1%, Yoruba 79.7% (Haiku 4.5 runs 1–27 points lower; Yoruba 52.7%). "Claude is capable in many languages beyond those benchmarked in the following table. Test with any languages relevant to your specific use cases." It advises stating input and output languages and submitting text in its "native script rather than transliteration" [V, S41]. Two limits [J]: the table covers only those two models, not newer ones, and it measures knowledge questions, not reading dialect, verse or subtext. Turkish, the second language of *The Long Places*, is not in it.

**R21.** If the source's language scores about 95% of English or better, then analyse in the original, write breakdown descriptions and prompts in English, and keep dialogue in the original, because translation adds error and English prompts are the most reliable for image and video models [J; C3 §7B: Omni fully supports only English].

**R22.** If the language is lower-resource for the model (Swahili, Yoruba and similar [V, S41]), then make a line-by-line English working translation beside the original, analyse the translation, cite original block IDs, and have a speaker check every line that will be spoken, because errors multiply downstream.

**R23.** If anything is translated, then keep `source_text` and `translation` as separate columns of one block and never overwrite the original, because dialogue, names and on-screen text must return to their original wording (A3 R11).

**R33.** If the source's language is not in Anthropic's table, then run a 10-minute test before choosing R21 or R22: have the model translate ten varied lines (one with dialect, one with an idiom, one verse line) into English and back, and have a speaker, or a second model in a fresh chat, mark each line right or wrong; 9 or 10 right means R21, fewer means R22, because a missing score is not a low score, and the test costs less than a wrong working language [J]. Record the result in `working_language_basis` (Section 11).

### 8.2 Parsing other languages' screenplays

- **Case.** Fountain finds cues by capitals; Chinese, Japanese, Korean, Arabic and Hebrew have none, so every cue is forced with `@` (R11) [V, S3].
- **Heading prefixes.** Fountain knows only its English prefix list [V, S3]; a German `INNEN`/`AUSSEN` heading must be forced with `.` [J]. An Italian guide uses `EST.` for *esterno* (exterior) [V-sec, S44], which is also one of Fountain's prefixes [V, S3]: map `int_ext` from the script's language, not from the prefix list.
- **Right-to-left scripts** (Arabic, Hebrew): keep logical order in files; check rendered signs in images, not prompts [J].

### 8.3 Spoken language against model support

MiniMax H3 has "Stable support for 11 languages: Arabic, Chinese, English, French, German, Italian, Japanese, Korean, Portuguese, Russian, and Spanish", others "to varying degrees" [V, S42]. HappyHorse 1.1 has 7; Kling 3.0 speaks 5 and translates others into English; Gemini Omni fully supports only English (C1 §3A, C3 §7B). ElevenLabs Multilingual v2 covers 29 languages including Turkish; Eleven v3 "70+" [V, S43].

**R24.** If a line's spoken language is not stable on the chosen video model, then make the voice separately (a speech model that supports it, or a speaker) and give the video model the audio (C1 §6 rule 1), because a model that translates into English changes the line.

**R25.** If a script marks a line as spoken in another language and subtitled, then set `spoken_language`, `subtitle: yes`, and treat the written words as the subtitle; the spoken words are a translation to make and check. Fountain's own sample does this: `JACK` / `(in Vietnamese, subtitled)` / `*Did you know Brick and Steel are retired?*` [V, S3, S4]. D18 later turns each such subtitle into a forced-narrative (FN) event, D18's term for "a subtitle every viewer of a language gets, translating plot-pertinent on-screen text or foreign speech" (D18 §1) [J].

**R26.** If names carry honorifics from another language, then list both the bare name and the honorific form as aliases, because *The Long Places* writes "Kaya Bey" 17 times and "Kaya" never alone [V, own count], and the alias list must resolve both (C5 §6.5).

---

## 9. Prose with embedded documents

A3 §7.7 decides how a letter plays on screen. This section finds and types embedded documents so that A3 has something to decide on.

**R27.** If a whole paragraph is set off (italics, quotation block, a distinct Word style, a list), then give it `block_type` (`embedded_document` or `verse`), a `document_kind`, a `document_writer` (character ID, `unknown` or `none`) and `in_world` (`yes` if it exists as an object in the story, `no` if it is a narrating device, `unknown`), because italics alone do not say what a block is (E2).

**R28.** If a block repeats earlier text, then compare it character for character and set `repeat_of`, because a refrain must be staged identically (A3 R23; D2 R15) and one changed word is information.

**R29.** If a block is about the file rather than the story (editor's note, version history, contents list), then exclude it as `front_matter` with a logged reason, because otherwise it becomes a scene or a voice-over.

**R30.** If a list or document sits inside a prose paragraph, then keep it in that paragraph's block but record it as an inline document with its exact words, because an insert may need it "letter for letter" (A3 §7.7).

**R34.** If the source marks its own break (a chapter or part heading, `---`, an act or scene line, "Intermission", "Blackout", "Curtain", a cut to black followed by a card such as *The Catch*'s `> CUT TO BLACK.` then `= THE CATCH`), then keep it as a `section_break` or `heading` block with a `break_kind`, never drop it, because D16 R8 tests the author's own breaks first as act boundaries and can only test what intake kept [J; D16 R8].

**R37.** If a block is verse, a song or a quoted poem (Melek's song; a hymn; lyrics), then also list it for D4's `underlying_works[]` check with "source: this work" or the named original, because a quoted real song carries its own rights even inside a story the user owns [J; D4 §6].

---

## 10. Checklists

- **Every source:** rights recorded (D4 `rights_status`, R35) and DRM checked; original hashed; container, kind, dialect, languages and density recorded with fingerprint counts, and the runtime basis (`user_target` or `provisional`, R31); extraction route logged; three pages compared as images (PDF, OCR); UTF-8 and NFC; line endings made LF; tracked changes counted and resolved (R36); counts agree or differences logged; every block mapped or excluded with a reason; source-marked breaks kept with `break_kind` (R34); questions listed; checkpoint A (C5) passed.
- **OCR:** run in Claude Code, not Cowork (Recipe I5); 300 dpi, deskewed, languages set; low-confidence pages read by a person; names, numbers and deliberate oddities checked by eye.
- **Thin source:** density computed against a stated or provisional runtime; quoted fact list; ASK and DECIDE gaps split; budget chosen by the user; `serves_facts` on every invention; invention report by script; checkpoint T answered; `source_original` kept.
- **Non-English:** working language by R21 or R22 (R33's test if the language is not in Anthropic's table); translation in its own column; cues forced where there are no capitals; heading prefixes mapped per language; every spoken line has a language and a model-support value.

---

## 11. Fields this subject adds to the breakdown

Enums lowercase `snake_case`; empty is `"none"`; each field carries C5's authority mark.

| Level | Field | Meaning | Allowed values / example |
|---|---|---|---|
| film | `source_container` | File type received (extracted) | `docx` \| `odt` \| `rtf` \| `gdoc_export` \| `pdf_text` \| `pdf_scanned` \| `image` \| `epub` \| `fdx` \| `fountain` \| `txt` \| `md` \| `html` \| `app_export` \| `other` |
| film | `source_kind` | Kind (extracted; human confirms) | `screenplay` \| `stage_play` \| `prose` \| `treatment` \| `outline` \| `synopsis` \| `logline` \| `comic_script` \| `game_script` \| `mixed` |
| film | `source_dialect` | Markup convention (derived) | `fountain_strict` \| `catch_variant` \| `fdx_xml` \| `pdf_layout` \| `plain_screenplay` \| `markdown_prose` \| `plain_prose` \| `stage_standard` \| `comic_full_script` \| `ink` \| `yarn` \| `twee` \| `other` |
| film | `source_fingerprint` | Pattern counts (derived) | `{"catch_heading": 30, "at_cue": 221}` |
| film | `extraction_method` | How text was got (derived) | `native_text` \| `layout_text` \| `ocr_local` \| `ocr_cloud` \| `llm_vision` \| `app_export` \| `manual` |
| film | `conversion_chain[]` | One row per step (derived) | `{tool, version, command, input_hash, output_hash}` |
| film | `ocr_quality` | OCR checks (derived) | `{pages, mean_conf, low_conf_pages, checked_pages}` or `"none"` |
| film | `drm_status` | Protection found (derived) | `none` \| `protected_stopped` |
| film | `source_language`, `working_language` | BCP 47 tags, the standard short language codes (extracted; working language authored) | `en`, `tr` |
| film | `density_words_per_min`, `density_class`, `density_runtime_basis` | Thinness (derived); what the minutes came from (authored, human) | `263`; `full` \| `partial` \| `thin`; `user_target` \| `provisional` \| `natural_runtime` |
| film | `working_language_basis` | Why this working language (derived) | `anthropic_table` \| `r33_test_pass` \| `r33_test_fail` \| `none` |
| film | `revisions_found` | Tracked changes and comments in the original (derived) | `{insertions, deletions, comments, resolved_by}` or `"none"` |
| film | `invention_budget` | User's limit (authored, human) | `minimal` \| `moderate` \| `free` |
| film | `facts[]` | Thin-source facts (extracted) | `{id, quote, type}`; type `event` \| `character` \| `place` \| `rule` \| `tone` \| `ending` |
| film | `invention_report` | Counts by origin (derived) | `{scenes_total, scenes_invented, lines_total, lines_invented, share}` |
| film | `expansion_checkpoint` | Checkpoint T (authored, human) | `{status: approved \| pending, version, date}` |
| film | `branch_path` | Chosen game path (authored, human) | node IDs, or `[]` |
| film | `series_rules[]` (D2) | New device policies for soliloquy, aside, caption | adds `voice_over` \| `direct_address` \| `to_listener` \| `cut` |
| scene | `origin`, `serves_facts` | Where the scene came from (authored) | `source` \| `dramatized_summary` \| `invented`; `["F03","F07"]` |
| scene | `stage_unit`, `opened_up` | Play structure; moved off the play's set | `{act, scene, french_scenes}` or `"none"`; `yes` \| `no` |
| block | `block_id`, `original_ref` | Normalized ID and origin (derived) | `ch08.p027`; `file line 674` |
| block | `break_kind` | For a `heading` or `section_break`: which break the source marks (extracted; R34, for D16 R8) | `chapter` \| `part` \| `act` \| `scene` \| `intermission` \| `curtain` \| `blackout` \| `card` \| `cut_to_black` \| `scene_break` \| `none` |
| block | `block_type` | What the block is (extracted) | `heading` \| `narration` \| `dialogue` \| `action` \| `stage_direction` \| `embedded_document` \| `verse` \| `epigraph` \| `front_matter` \| `section_break` \| `panel` \| `caption` \| `sfx` \| `choice` |
| block | `document_kind`, `document_writer`, `in_world` | Document typing (extracted or inference) | `letter` \| `statement` \| `report` \| `list` \| `protocol` \| `message` \| `label` \| `sign` \| `note` \| `none`; `CH-…` \| `unknown` \| `none`; `yes` \| `no` \| `unknown` |
| block | `repeat_of`, `provenance`, `language` | Repeat; origin of the words; language (derived/extracted) | block ID or `"none"`; `source_text` \| `converted` \| `ocr` \| `translated` \| `invented`; BCP 47 |
| dialogue line | `spoken_language`, `subtitle`, `translation_status` | Performed language | `vi`; `yes` \| `no`; `none` \| `machine` \| `native_checked` |
| dialogue line | `address`, `model_language_support` | To whom (plays); model support (derived) | `scene_partner` \| `audience` \| `self`; `stable` \| `partial` \| `none` |

**Validator checks** (prefixed to avoid C5's V1–V13 and D1's V14–V16):
- **D14-V1** every original block maps to one normalized block or a reasoned exclusion.
- **D14-V2** heading, cue, chapter and document counts match the original's fingerprint, apart from logged changes.
- **D14-V3** no Fountain cue in mixed case unless forced with `@`; no heading without a known prefix (`INT`, `EXT`, `EST`, `INT./EXT`, `INT/EXT`, `I/E`, any case) unless forced with `.`.
- **D14-V4** every OCR page is above the confidence threshold or on the checked list.
- **D14-V5** every `invented` scene or block has non-empty `serves_facts`; the invented share is within budget; no `extracted` field cites an invented block as evidence.
- **D14-V6** every non-English spoken line has `translation_status` and `model_language_support`.
- **D14-V7** every italic, quoted or distinctly styled prose block has a `block_type`; every document has a `document_kind`.
- **D14-V8** every `repeat_of` pair is identical, or the difference is logged.
- **D14-V9** if `density_class` is `partial` or `thin`, `expansion_checkpoint.status` is `approved` before any stage after 0 runs, and `density_runtime_basis` is set.
- **D14-V10** every `verse` block appears in D4's `underlying_works[]` (R37), and every source-marked break has a `break_kind` (R34).

---

## 12. Failure modes

| Failure | Sign | Fix |
|---|---|---|
| Variant markup read as Fountain or Markdown | Zero scenes; cards gone | R1; C5 P8 |
| Markdown chapters or quotations misread | Chapters vanish; "transitions" in prose | R2, R3 |
| Plain PDF extraction | Dialogue looks like action | R7 (M1) |
| Bad PDF font mapping; split words | Stray letters; "cont ain" | R6; OCR (M3, M4) |
| FDX text in mixed case | Cues missed (headings survive: prefixes are case-insensitive) | Upper-case cues or force with `@` (M2; D14-V3) |
| Tracked changes silently applied | Deleted lines back; comments lost | `--track-changes=all`; ask which version |
| Scanned PDF over 100 pages in claude.ai | Nothing read at all: PDFs of 101–1,000 pages are read as text only, and a scan has no text | Split into parts of 100 pages or fewer, or OCR first (S17) |
| OCR attempted in Cowork | Tesseract missing; or the model "reads" the images itself | Claude Code (Recipe I5; D1 §13) |
| Mixed line endings | Line counts or line references disagree between tools | R9: store LF only (M8) |
| Unresolved revisions | Two versions of a line; rejected text in the scene | R36 |
| Density against an invented runtime | A full script treated as thin, or the reverse | R31; `density_runtime_basis` |
| LLM "corrects" the text | Dialect or backwards text regularized | Principle 3; compare with Tesseract |
| Front matter or italics misread | Editor's note becomes a scene; a song staged as a letter | R27, R29 |
| Unapproved expansion | Invented scenes cited as the user's | R17; D14-V5 |
| Translation overwrote the original | Lines untraceable | R23 |
| Unsupported spoken language | Line translated or garbled | R24 |
| Names round-tripped through capitals | "Kırk" becomes "kirk" | R10 |

---

## 13. Worked examples

### E1. *The Catch*: detecting a dialect from its marks

**Fingerprint** [V, own test M6]: 30 lines start `## INT` or `## EXT`; 221 start `@`; 8 start `=`; 3 start `>`; 18 standalone parentheticals; no bare `INT` line. By R1 the dialect is `catch_variant`. A3 §4.3 gives the reading and C5 P8 the normalization, so only detection and its traps are shown.

**Why the extension cannot decide.** Line 10, `## INT. MEDICAL FACTORY - LOADING TUNNEL - NIGHT`, is a vanishing section in Fountain [V, S3] and a heading in Markdown, where line 8, `> FADE IN:`, is a quotation. Saved as `.md`, the file previews well and parses wrongly.

**Lines the fingerprint hands to the LLM to classify** (A3 §4.3 step 5):
- The two standalone capital lines, `NELL ROWAN. FLIGHT TEST.` (line 990) and `IONA VALE.` (line 1233), each with a blank line after. Strict Fountain reads them as action (a cue must have no blank line after it [V, S3]); a looser reader that takes any capital line as a cue would invent two speakers. In this dialect only `@` makes a cue, so both are on-screen text.
- `@JUDE (V.O.)` / `(in her ear)` / `Was that you?` (lines 93–95): extension plus device parenthetical, which A3 R15 turns into `voice_source`.
- `## INT. QUARANTINE - JUDE'S ROOM - CONTINUOUS (ON THE TABLET)` (line 838): a modifier after the time, so a presentation note, not part of the place.
- `VISOR VIEW: a wire-frame room marked RECEIVING hangs beyond the ledge.` (line 1506): a colon line inside action, a shot instruction, not a title-page key.
- `= THE CATCH` (line 488) and `= THE END` (line 1852): after the title page, so cards.

**Encoding** [V, own test M5]: UTF-8, NFC, line feeds; the only non-ASCII characters are two em dashes on title-page lines 5–6.

**Check before checkpoint A**: 30 scene records; 221 cues resolving to IONA, JUDE, ELI, SAYE and NELL (A3 §4.3); every later `=` line a card; the dialect decision logged with its evidence lines.

### E2. *The Long Places*: Markdown prose with embedded documents

**Fingerprint** [V, own test M6]: 15 lines start `# ` (file title plus 14 chapters); 180 whole-paragraph italic lines; 15 `---` breaks; 69 lines start `>`; no scene headings. Kind `prose`, dialect `markdown_prose`. A Fountain parser would drop the chapters as sections and turn the 69 quotation lines into transitions (R2, R3).

| Lines | Text (exact) | Typing |
|---|---|---|
| 1 | `# 19 The Long Places - revised by Claude, final` | `front_matter` (file title), excluded. |
| 3 | `*GLM 5.3's novella (file 10), revised by three Claude agents …` `What changed, and why, is in 17's change logs.*` | `front_matter`, excluded (R29): italic like the letters, but about the file. |
| 7–33 | `*To the one who keeps the lamps after me:*` … `*To the one who keeps the lamps after me: begin.*` | `embedded_document`, `letter`, writer `unknown`, `in_world: unknown`; ends at `---` (line 35). Chapters I–XIII open this way (A3 §7.7). |
| 67 | Inside a paragraph: `*47. Stair, rock-cut, seven treads, worn.` … `51. Hand print, right, red ochre, above the first marks, lower wall.` … `53. Lamp, ceramic, handle broken.*` | Inline `list` (R30); exact words kept for the insert A3 Ex5 plans. |
| 120 | `*Enclosures: gendarmerie summary, 1 leaf; correspondence, Valletta, 7.ix.1999, 1 leaf — not reproduced.*` | `note`, `in_world: yes` (part of a registered letter). |
| 674–726 | `> **Statement 1 — Dr. M. Kállai, geophysics. 9.ix.**` and three more; Statement 3's body is all lower case: `> went down 10:05 with everyone. gave my name at the mouth like always.` | Four `statement` documents; writers from their headers (Kállai, Arat, Demir, Yılmaz; linking "Y. Demir, assistant" and "M. Yılmaz, keeper" to named characters is `inference`). The lower case is the writer's voice and must survive, which is why an LLM must not re-type it (principle 3). |
| 987–997 | `*Wake, house, the day is spent,*` … `*and the lamps are kept.*` | `verse`: Melek's song, recorded in the scene; Fountain lyrics `~` (R12), not a letter. |
| 1092 | `*you asked for the wick hour. it isn't coming back from me. …*` | `message`: a post a character types into his channel's drafts, answering a follower's comments (lines 1086–1090); on screen, so `on_screen_text` with exact lower case (A3 R11). |
| 1205–1209; 1237–1242 | `> *Newgrange — no lamp after 1974.*` …; `> *The Vigil of the Sealed Hour (the founder's manner, 1924).*` and numbered steps | `list`; `protocol`. |
| 1415–1441 | The opening letter again | `repeat_of` lines 7–33: all 14 paragraphs identical [V, own test M7] (R28). |

**Language.** English narrative with Turkish names and address terms ("Kırk Oda", "Kaya Bey", "Melek Hanım", Melek's "Record it, kızım." at line 985): `source_language: en`, working language English (R21), honorific aliases (R26), dotless ı kept (R10). If the user wants village scenes spoken in Turkish with subtitles, those lines get `spoken_language: tr`; Turkish is not among H3's 11 stable languages [V, S42], so R24 routes them to separate voices (ElevenLabs Multilingual v2 lists Turkish [V, S43], or an actor).

**Output.** `source_paragraphs.md` (IDs such as `ch08.p027`); `source_map.json` with two exclusions, every italic and quoted block typed, one `repeat_of` run. Questions for the user: should the film show the letter-writer (A3 Ex5 shows hands only)? Should Statement 3's lower case be visible on screen?

### E3. *The Catch* as a one-paragraph synopsis

Suppose the user had sent only this (my synopsis of the screenplay, about 160 words, written for this test):

> **THE CATCH.** Iona breaks her brother Eli out of a medical factory where he is held for a drug trial the company says does not exist, with help from Jude. They escape in an old freight cage whose brakes are gone; they are shot at, the cage falls, and Eli fires a device he has stolen. They survive, but now the world is mirror-reversed: they have been "turned". Ordinary food no longer feeds them, and a germ that crossed with them could spread unstoppably. Dr Saye, who inspects the company's trials, quarantines them. A tall figure from a ship hanging beside the factory in another world takes Jude and Eli. Iona crosses to the ship in a pressure suit, finds it has been collecting everything that turned, and gets the others sent home. To destroy the dangerous culture she gives up her own way back, then brings home the small creature that lived inside the figure's suit, turned with her.

**T0.** About 160 words for about 35 minutes is under 5 words per minute: `thin` (the screenplay runs about 260).

**T1. Facts.** F01 Iona breaks Eli out of a medical factory. F02 He is held for a trial the company denies. F03 Jude helps. F04 They escape in an old freight cage without brakes. F05 They are shot at. F06 The cage falls. F07 Eli fires a stolen device. F08 They survive, mirror-reversed ("turned"). F09 Ordinary food no longer feeds them. F10 A germ that crossed could spread unstoppably. F11 Dr Saye, an inspector of trials, quarantines them. F12 A tall figure from a ship beside the factory, in another world, takes Jude and Eli. F13 Iona crosses in a pressure suit. F14 The figure has been collecting everything that turned. F15 The others are sent home. F16 She gives up her way back to destroy the culture. F17 She brings home the creature from inside the figure's suit, turned with her.

**T2. ASK: questions whose answers change the story.** The screenplay answers each in a way no LLM would guess:
1. Who is Jude to Iona? The script never says; its last image implies it: "His wedding ring. On his right hand." and "She lifts her own left hand and lays it against his, through the glass. The two rings sit directly across from each other, like a ring and its reflection." (lines 1779, 1783).
2. When does Iona learn that Eli fired the device? The script withholds it until a recording in scene 13, and A3 Ex2 forbids scene 6's synopsis to say it; this synopsis gives it away, so the fact list must flag F07 as a reveal.
3. Did Eli choose for all three, and could they have got out another way? That argument is the heart of scene 13: "You could have moved us out of the shaft." / "We would still have been falling."
4. What is the figure, and is it hostile?
5. Is anyone else on the ship? (The script has Nell Rowan, missing nineteen years; no expansion of this synopsis can produce her.)
6. How is the mirror world discovered and shown? (The script uses details: "Every letter is backwards.", "The wheel is on the other side.", a mint leaf that tastes of "Not mint.")
7. What does the ending leave open between Iona and Eli? Tone? Runtime (D2 M0)? Limits on the gunshot and blood (D1 §6.5)?

**T2. DECIDE (labelled `invention`, with `serves_facts`).** Factory layout; how the guard is passed; the quarantine rooms; the suit; the ship's rooms; how the others are sent home.

**The gap, measured against the real script** [J, from the scene list]. Roughly half of the screenplay's 30 scenes contain an event the synopsis states (the break-out, the fall, quarantine, the food and germ, the two abductions, the crossing, the collection room, the sending home, the fire, the creature, the return). The rest have no basis in it: the climb and broken rung (scene 2), the car (9), the kitchen tests (10), the playback (13), Nell's room (20), the falling ship (26), the last two scenes (29–30). All 221 speeches would be invented. At `minimal` there is no film; at `moderate` about half the scenes are dramatized summaries and all dialogue is invented. So R17 and R19 apply: interview (T3), then two or three independent step outlines for the user to choose between at checkpoint T.

The test also shows why labels must survive. An invented cage scene could be vivid and still miss the writer's details that later scenes pay off (the red tag "Goods only. No persons.", the yellow stripe, "A hard metal CLACK."). Unlabelled, the invented version would be taken for the writer's.

---

## 14. Conflicts with other files, and open questions

- **Stage 0 files.** C5 names `source.fountain` or numbered paragraphs; this file adds `source_map.json`, `intake_log.json` and, for thin sources, `source_original`. C5 §10.3 should list them.
- **Checkpoint order.** Checkpoint T precedes D2's checkpoint M, and is skipped for `full` sources.
- **Labels.** A3 labels items `fact` / `inference` / `invention`; C5 marks fields `extracted` / `authored` / `derived` and flags additions (V12). This file's `origin` and `provenance` join them: an `invented` block yields `authored` fields, never `extracted` ones.
- **Prompt language.** R21 keeps prompts in English; D18 may set a different rule for on-screen text.
- **Language field names.** D18 names a version's language `lang`; this file uses `source_language`, `working_language`, `language` (block) and `spoken_language` (line). All take BCP 47 codes; the build should pick one stem (suggest `lang` with a prefix: `source_lang`, `spoken_lang`) [J].
- **Subtitled foreign speech.** R25's `subtitle: yes` lines are D18's forced-narrative events; D18 should read them from this field rather than re-detect them.
- **C5 "P8".** "C5 P8" in this file (and in the brief) is the C5 *digest's* procedure P8 (intake normalization, built from C5 §9 E1 and Recipe 2); the full C5 file has no P8. C5's rules are numbered 1–33 without an R; "C5 R1" means C5 §5 rule 1.
- **D1 on Cowork (resolved).** D1 §13 corrected the first version of Recipe I5, which called Cowork an agent that runs code on your computer; I5 now sends OCR to Claude Code.
- **D16 R8** says "D14 already maps these to act breaks". The first version kept only a play's Blackout, Curtain and Intermission; R34 and `break_kind` now keep every source-marked break (chapter, part, card, cut to black), so D16 can test them. D14 records breaks; D16 decides whether they are act breaks.
- **D2 R3** rejects words per minute for estimating prose runtime; this file uses words per minute only for density triage (Section 7.1). No conflict if each file keeps to its use.
- **D4 rights.** D4 makes `rights_status` a condition of checkpoint A; this file's triage now asks for it first (R35), and quoted songs feed D4's `underlying_works[]` (R37).
- **Provenance labels multiply.** A3's `fact`/`inference`/`invention` (claims), C5's `extracted`/`authored`/`derived` (field authority), and this file's scene `origin` (`source`/`dramatized_summary`/`invented`) and block `provenance` (`source_text`/`converted`/`ocr`/`translated`/`invented`: how the words got here) answer different questions. Mapping [J]: `origin: invented` ⇔ A3 `invention`; `dramatized_summary` ⇔ the event is A3 `fact`, its staging A3 `invention`; `provenance: invented` blocks yield only `authored` fields. The critic's shared-vocabulary list already flags this family; the build should publish one table.
- **Resolved on re-check** [V-sec]: Tesseract's latest release is 5.5.3 (24 Jul 2026, S48; GitHub itself refused automated fetching); Google Docs suggestions are reported to export to Word as tracked changes (S45, 2014, with later user reports of failures), so R36 checks rather than trusts.
- **Open** [U]: Mistral OCR 4.1's batch discount; whether claude.ai's sandbox can install Tesseract (test in Recipe I2: "Run `tesseract --version`"); which pandoc version pypandoc_binary 1.17 bundles (test: "Run `pandoc --version`"); whether a .docx uploaded straight into claude.ai keeps tracked changes or style names. The density thresholds (150 and 30 words per minute), OCR confidence thresholds (85, 60), the 1-in-50 error trigger and R33's 9-in-10 pass mark are judgments to calibrate on real sources.

---

## Sources

All checked 2026-09-27. Re-opened by the fact-check pass the same day: S1, S2, S3, S4, S5 (PyPI data), S10, S14, S16, S17, S18–S26, S27, S28, S29, S30, S31, S32, S33, S34, S35, S36, S37, S38, S39, S40, S41, S42, S43; S6–S9 through search-result extracts (the Final Draft help centre returns HTTP 403 to automated fetches); S11–S13 not re-opened (same 403).

- S1 Pandoc User's Guide: https://pandoc.org/MANUAL.html
- S2 Pandoc releases (3.11, 29 Aug 2026): https://github.com/jgm/pandoc/releases
- S3 Fountain syntax: https://fountain.io/syntax
- S4 Fountain sample "Brick & Steel": https://fountain.io/_downloads/Brick-&-Steel.fountain (also `.fdx`, `.pdf`)
- S5 screenplain 0.12.0 (28 Apr 2026): https://pypi.org/project/screenplain/
- S6 Final Draft, import formats (updated 12 Sep 2026): https://kb.finaldraft.com/hc/en-us/articles/15575252515988
- S7 Final Draft, export formats: https://kb.finaldraft.com/hc/en-us/articles/27525594609684
- S8 Final Draft, Fountain files: https://kb.finaldraft.com/hc/en-us/articles/15575076862228
- S9 Final Draft, PDF import (updated 13 Sep 2026): https://kb.finaldraft.com/hc/en-us/articles/15575271457556
- S10 WriterDuet, export: https://www.writerduet.com/article/261-export-a-document
- S11 Celtx, script editor (updated 2 Sep 2026): https://support.celtx.com/hc/en-us/articles/360009310173
- S12 Celtx, import: https://support.celtx.com/hc/en-us/articles/215946588
- S13 Celtx, PDFs: https://support.celtx.com/hc/en-us/articles/207127828
- S14 Highland Pro, App Store: https://apps.apple.com/us/app/highland-pro/id6612007609
- S15 Highland 2 vs Highland Pro: https://blog.quoteunquoteapps.com/highland-2-highland-pro-what-changed-what-stayed-the-same-and-where-to-get-it/
- S16 Google Docs, Markdown: https://support.google.com/docs/answer/12014036
- S17 Claude Help Center, uploads: https://support.claude.com/en/articles/8241126-upload-files-to-claude
- S18 Tesseract README: https://github.com/tesseract-ocr/tesseract
- S19 Tesseract, output quality: https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html
- S20 Tesseract, command line: https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html
- S21 OCRmyPDF 17.12.1: https://pypi.org/project/ocrmypdf/
- S22 OCRmyPDF cookbook: https://ocrmypdf.readthedocs.io/en/latest/cookbook.html
- S23 OCRmyPDF errors: https://ocrmypdf.readthedocs.io/en/latest/errors.html
- S24 Google Document AI pricing: https://cloud.google.com/document-ai/pricing
- S25 Amazon Textract pricing: https://aws.amazon.com/textract/pricing/
- S26 Mistral OCR 4.1: https://docs.mistral.ai/models/ocr-4-1
- S27 "Seeing is Believing? Mitigating OCR Hallucinations in Multimodal Large Language Models": https://arxiv.org/abs/2506.20168
- S28 W3C EPUB 3.3: https://www.w3.org/TR/epub-33/
- S29 calibre 9.15.0 `ebook-convert`: https://manual.calibre-ebook.com/generated/en/ebook-convert.html
- S30 calibre FAQ: https://manual.calibre-ebook.com/faq.html
- S31 17 U.S.C. §1201: https://www.law.cornell.edu/uscode/text/17/1201
- S32 Wikipedia, "Scene (performing arts)": https://en.wikipedia.org/wiki/Scene_(performing_arts)
- S33 Samuel French formatting guidelines: https://www.readmyplay.com/Samuel-French-Formatting-Guide.pdf
- S34 Wikipedia, "Fleabag": https://en.wikipedia.org/wiki/Fleabag
- S35 Wikipedia, "Glengarry Glen Ross (film)": https://en.wikipedia.org/wiki/Glengarry_Glen_Ross_(film)
- S36 WGA 2023 Theatrical and Television Basic Agreement, Article 1.B: https://www.wga.org/uploadedfiles/contracts/mba23.pdf
- S37 Dark Horse, script format: https://images.darkhorse.com/darkhorse08/company/submissions/scriptguide.pdf
- S38 inkle, "Writing with ink": https://github.com/inkle/ink/blob/master/Documentation/WritingWithInk.md
- S39 Yarn Spinner, lines, nodes and options: https://docs.yarnspinner.dev/write-yarn-scripts/scripting-fundamentals/lines-nodes-and-options
- S40 Twee 3 specification: https://github.com/iftechfoundation/twine-specs/blob/master/twee-3-specification.md
- S41 Anthropic, multilingual support: https://platform.claude.com/docs/en/build-with-claude/multilingual-support
- S42 MiniMax H3 model card: https://huggingface.co/MiniMaxAI/MiniMax-H3
- S43 ElevenLabs, text to speech: https://elevenlabs.io/docs/overview/capabilities/text-to-speech
- S44 Scrivere sceneggiatura, "Intestazioni": http://scriveresceneggiatura.blogspot.com/2015/07/intestazioni.html
- S45 UpCurve Cloud, "Google Docs Has Full 'Track Changes' Word Integration" (4 Dec 2014): https://upcurvecloud.com/blog/google-docs-has-full-track-changes-word-integration/
- S46 pypandoc_binary 1.17 (14 Mar 2026; "including pandoc out of the box"; wheels for Linux, macOS, Windows): https://pypi.org/project/pypandoc-binary/
- S47 D18 §1 (forced narrative), D16 R8, D4 §6–7, D1 §3.1–3.2 and §13, D2 R3 and §6: library files in scratchpad/research/
- S48 Tesseract releases (5.5.3, 24 Jul 2026, via search result): https://github.com/tesseract-ocr/tesseract/releases

**Own tests** (2026-09-27; Python 3, pypdf 6.19.0): M1 plain and layout extraction of S4's PDF; M2 paragraph types and letter case in S4's FDX (8 Scene Heading, 23 Action, 20 Character, 22 Dialogue, 6 Parenthetical, 7 Transition, 1 General, counting the two Character and two Dialogue paragraphs nested in one `DualDialogue` block; text stored in mixed case; recounted in the fact-check pass); M3 extraction of S37; M4 extraction of S33; M5 Unicode checks on both test sources and Python case mapping; M6 fingerprint counts on both test sources and S4; M7 comparison of *The Long Places* lines 7–33 with 1415–1441 (identical); M8 fact-check recount of S4's `.fountain` fingerprint (8 headings, 6 `>` lines, 26 unmarked capital lines, 6 parentheticals) and line endings (144 CRLF lines among LF lines), and re-runs of M1, M3 and M4.

**Library files built on:** A1, A2, A3, C1, C2, C3, C5, D1, D2, D4, D5, D9, D16, D18.
