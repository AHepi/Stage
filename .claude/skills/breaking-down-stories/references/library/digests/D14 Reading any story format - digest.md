# Digest D14: Intake of any story format, and of thin or non-English sources (27 Sept 2026)

Source: `research/D14_intake_any_format.md` (fact-checked 2026-09-27). Brackets: R# = the file's decision rule; P# = core principle (§1); T# = thin-source step (§7.3); I# = recipe; E# = worked example; M# = the file's own tests; S# = its sources. [V] verified, [V-sec] secondary source, [U] unverified, [J] judgment.

## 1. Scope

1. Stage 0 (intake), before C5 R1–R3: detect a source's container, kind, dialect, languages and density from its content, then convert it to `source.fountain` (anything performed) or `source_paragraphs.md` (prose), with `source_map.json` and `intake_log.json` beside it.
2. Covers Word, Google Docs, EPUB, text and scanned PDFs, screenwriting-app exports, stage plays, comic and game scripts, prose with letters and lists, and non-English or mixed-language sources.
3. For a thin source (treatment, outline, synopsis, logline), expands it to scenes under a user-chosen invention budget, every invention labelled, and stops at a new **checkpoint T** before D2's checkpoint M.

**Terms.** *Container* = file type; *kind* = sort of story text; *dialect* = markup convention; *fingerprint* = counts of telltale line patterns; *text layer* = a PDF's hidden selectable text (a scan has none); *OCR* = software reading letters from page images; *block* = one paragraph, speech, heading or document with an ID; *density* = source words per minute of planned film; *invention* = anything the source neither states nor implies; *French scene* = a theatre unit bounded by an entrance or exit; *BCP 47* = short language codes (`en`, `tr`).

## 2. Rules

**Principles** (§1)
1. [P1] If a file arrives, then detect its dialect from content, never its name, because *The Catch*'s markup is also valid Markdown.
2. [P2] If a source arrives, then keep the original untouched with its hash (C5 R2), because every later file cites it.
3. [P3] If text must be extracted, then a program extracts and the LLM only classifies and checks, because vision models show "overreliance on linguistic priors" [V, S27] and "correct" dialect or backwards text.
4. [P4, P5] If anything is converted, then count headings, cues, chapters and documents before and after and log every change, because conversion fails silently.
5. [P8] If the only copy is poor, then ask for the app export or original first, because repair loses more.

**Detect** (§2.2)
6. [R1] If any line starts `## INT` or `## EXT`, then use the *Catch* dialect (A3 §4.3), because Fountain deletes such headings as sections and Markdown makes them document headings.
7. [R2] If lines start `# ` and there are no scene headings, then treat them as chapter headings, because Fountain drops sections (*The Long Places* would lose 14 chapters).
8. [R3] If prose has lines starting `>`, then treat them as quotations, never transitions, because none of *The Long Places*'s 69 is a transition.
9. [R4] If one file mixes kinds, then split it into regions and ask which are the story, because notes are not story.
10. [R5] If the kind is still unclear, then show the first 40 lines with the proposed reading and ask, because every ID depends on it.
11. [R31] If there is no target runtime, then ask for a rough one and mark it `provisional` until D2 M0, because density needs minutes.
12. [R35] If the source is someone else's, an EPUB, or not written by the user, then run D4's rights intake before converting and stop at DRM, because conversion copies the work.

**Convert** (§3)
13. [R32] If the chat app runs code, then convert in its sandbox (Recipe I2); if not, then get an app export or plain-text save and have the LLM list lines, not count, because an LLM retyping a file is not an extraction.
14. [R36] If a Word or Google Docs file may hold revisions, then convert with `--track-changes=all`, count the marks and ask which version is the story, because pandoc's default silently accepts every change [V, S1].
15. [R6] If text came from a PDF, then compare first, middle and last pages as images and switch to OCR above about 1 wrong word in 50 [J], because extraction fails without errors (M1, M3, M4).
16. [R7] If a script or play arrives as PDF, then extract in layout mode or through an app, never plain mode, because indentation alone tells cue from dialogue from action (M1).
17. [R8] If the writer used a screenwriting app, then ask for Fountain, else .fdx, else "Text with Layout", else PDF, because each step down loses structure.
18. [R9] If text arrives, then store UTF-8, NFC, LF, no byte-order mark (NFKC only on PDF text), because one letter can be stored two ways and Fountain's own sample mixes CRLF and LF (M8).
19. [R10] If capitals do not round-trip (Turkish ı, İ), then store names as spelled and capitalize for display only, because "Kırk Oda" becomes "kirk oda" (M5).

**Normalize, plays, comics, games** (§4–6)
20. [R11] If an element must be forced (lower-case or non-Latin cue; non-English heading prefix), then use `@` or `.`, never rewrite words, because Fountain forcing "is helpful for names that require lower-case letters, and for non-Roman languages" [V, S3].
21. [R12] If Fountain has syntax for a convention, then use it (`^`, `~`, `>TEXT<`, `[[ ]]`), because home-made markers break tools.
22. [R13] If the source is a play, then decide soliloquy and aside handling once as series rules (D2 R14) and label moved locations and added scenes `invention`, because those conventions change most.
23. [R14] If one stage set stands for several places, then split only on the text's evidence, else ask, because a wrong split forks every reference image (A3 R6).
24. [R15] If the source branches, then the user chooses one path (`branch_path`), flattened to Fountain, because a film is one path.
25. [R16] If a game line is a "bark" with no scene, then drop it with a log line unless the user places it, because it has no event.

**Thin sources** (§7)
26. [R17] If density is `partial` or `thin`, then run T0–T6 and stop at checkpoint T before D2, because unapproved invention would become "source".
27. [R18] If a gap changes meaning (identity, motive, reveal, world rule, ending, tone, point of view, runtime, content limits), then ask; else decide and label, because meaning is the user's (A3 P10).
28. [R19] If the invented share exceeds the budget, then offer two or three independent expansions (C5 R14), because choosing between stories is the user's call.
29. [R20] If there are several thin documents, then merge them into one fact list citing each document, because contradictions must surface at T3.

**Languages** (§8)
30. [R21] If the language scores about 95% of English or better (Anthropic's table), then analyse in the original, prompt in English, keep dialogue original, because translation adds error and models follow English prompts best (C3 §7B).
31. [R22] If the language is lower-resource (Swahili 91.1%, Yoruba 79.7% [V, S41]), then analyse a line-by-line English translation, cite original IDs, and have a speaker check spoken lines, because errors multiply.
32. [R33] If the language is not in the table (Turkish), then run a ten-line round-trip test: 9–10 right means R21, else R22, because a missing score is not a low score [J].
33. [R23] If anything is translated, then keep `source_text` and `translation` in separate columns, because words must return to their original (A3 R11).
34. [R24] If the spoken language is not stable on the video model, then make the voice separately and feed the audio (C1 §6 rule 1), because a translating model changes the line.
35. [R25] If a line is marked "spoken in another language, subtitled", then set `spoken_language` and `subtitle: yes`, the written words being the subtitle, because that is what the page means; D18 reads these as forced narratives.
36. [R26] If names carry honorifics, then alias both forms, because *The Long Places* writes "Kaya Bey" 17 times and "Kaya" never alone.

**Embedded documents and breaks** (§9)
37. [R27] If a paragraph is set off (italics, quote block, style, list), then give it `block_type`, `document_kind`, `document_writer`, `in_world`, because italics alone do not say what it is.
38. [R28] If a block repeats earlier text, then compare character for character and set `repeat_of`, because refrains are staged identically and a changed word is information.
39. [R29] If a block is about the file, then exclude it as `front_matter` with a reason, because otherwise it becomes a scene.
40. [R30] If a document sits inside a paragraph, then record its exact words as inline, because an insert may need it "letter for letter".
41. [R34] If the source marks its own break (chapter, act, Intermission, Blackout, cut to black and card), then keep it with `break_kind`, because D16 R8 tests author breaks first.
42. [R37] If a block is verse or a song, then list it for D4's `underlying_works[]`, because a quoted song carries its own rights.

## 3. Breakdown fields

Enums lowercase `snake_case`; empty = `"none"`; each field carries C5's authority mark (`extracted`, `authored`, `derived`).

| level | field_name | meaning | allowed values / example |
|---|---|---|---|
| film | `source_container` | File type received | `docx` \| `odt` \| `rtf` \| `gdoc_export` \| `pdf_text` \| `pdf_scanned` \| `image` \| `epub` \| `fdx` \| `fountain` \| `txt` \| `md` \| `html` \| `app_export` \| `other` |
| film | `source_kind` | Kind (human confirms) | `screenplay` \| `stage_play` \| `prose` \| `treatment` \| `outline` \| `synopsis` \| `logline` \| `comic_script` \| `game_script` \| `mixed` |
| film | `source_dialect` | Markup convention | `fountain_strict` \| `catch_variant` \| `fdx_xml` \| `pdf_layout` \| `plain_screenplay` \| `markdown_prose` \| `plain_prose` \| `stage_standard` \| `comic_full_script` \| `ink` \| `yarn` \| `twee` \| `other` |
| film | `source_fingerprint` | Pattern counts | `{"catch_heading": 30, "at_cue": 221}` |
| film | `extraction_method` | How text was got | `native_text` \| `layout_text` \| `ocr_local` \| `ocr_cloud` \| `llm_vision` \| `app_export` \| `manual` |
| film | `conversion_chain[]` | One row per step | `{tool, version, command, input_hash, output_hash}` |
| film | `ocr_quality` | OCR checks | `{pages, mean_conf, low_conf_pages, checked_pages}` or `"none"` |
| film | `drm_status` | Protection found | `none` \| `protected_stopped` |
| film | `revisions_found` | Tracked changes and comments (R36) | `{insertions, deletions, comments, resolved_by}` or `"none"` |
| film | `source_language`, `working_language` | BCP 47 | `en`, `tr` |
| film | `working_language_basis` | Why this working language (R33) | `anthropic_table` \| `r33_test_pass` \| `r33_test_fail` \| `none` |
| film | `density_words_per_min`, `density_class`, `density_runtime_basis` | Thinness; where the minutes came from (R31) | `263`; `full` \| `partial` \| `thin`; `user_target` \| `provisional` \| `natural_runtime` |
| film | `invention_budget` | User's limit (human) | `minimal` \| `moderate` \| `free` |
| film | `facts[]` | Thin-source facts | `{id, quote, type}`; type `event` \| `character` \| `place` \| `rule` \| `tone` \| `ending` |
| film | `invention_report` | Counts by origin | `{scenes_total, scenes_invented, lines_total, lines_invented, share}` |
| film | `expansion_checkpoint` | Checkpoint T (human) | `{status: approved \| pending, version, date}` |
| film | `branch_path` | Chosen game path (human) | node IDs, or `[]` |
| film | `series_rules[]` (D2) | Device policies added here | `voice_over` \| `direct_address` \| `to_listener` \| `cut` |
| scene | `origin`, `serves_facts` | Where the scene came from | `source` \| `dramatized_summary` \| `invented`; `["F03","F07"]` |
| scene | `stage_unit`, `opened_up` | Play structure; moved off the play's set | `{act, scene, french_scenes}` or `"none"`; `yes` \| `no` |
| block | `block_id`, `original_ref` | Normalized ID and origin | `ch08.p027`; `file line 674` |
| block | `block_type` | What the block is | `heading` \| `narration` \| `dialogue` \| `action` \| `stage_direction` \| `embedded_document` \| `verse` \| `epigraph` \| `front_matter` \| `section_break` \| `panel` \| `caption` \| `sfx` \| `choice` |
| block | `break_kind` | Source-marked break (R34) | `chapter` \| `part` \| `act` \| `scene` \| `intermission` \| `curtain` \| `blackout` \| `card` \| `cut_to_black` \| `scene_break` \| `none` |
| block | `document_kind`, `document_writer`, `in_world` | Document typing | `letter` \| `statement` \| `report` \| `list` \| `protocol` \| `message` \| `label` \| `sign` \| `note` \| `none`; `CH-…` \| `unknown` \| `none`; `yes` \| `no` \| `unknown` |
| block | `repeat_of`, `provenance`, `language` | Repeat; how the words got here; language | block ID or `"none"`; `source_text` \| `converted` \| `ocr` \| `translated` \| `invented`; BCP 47 |
| dialogue line | `spoken_language`, `subtitle`, `translation_status` | Performed language | `vi`; `yes` \| `no`; `none` \| `machine` \| `native_checked` |
| dialogue line | `address`, `model_language_support` | To whom (plays); model support | `scene_partner` \| `audience` \| `self`; `stable` \| `partial` \| `none` |

**Validator checks.** D14-V1 every original block maps to one normalized block or a reasoned exclusion. V2 heading, cue, chapter and document counts match the fingerprint, apart from logged changes. V3 no Fountain cue in mixed case unless forced with `@`; no heading without a known prefix (any case) unless forced with `.`. V4 every OCR page above threshold or on the checked list. V5 every `invented` scene or block has `serves_facts`; invented share within budget; no `extracted` field cites an invented block. V6 every non-English spoken line has `translation_status` and `model_language_support`. V7 every set-off prose block has a `block_type`, every document a `document_kind`. V8 every `repeat_of` pair identical or the difference logged. V9 `partial`/`thin` sources have checkpoint T approved and `density_runtime_basis` set before stage 1. V10 every `verse` block listed for D4; every source-marked break has a `break_kind`.

## 4. Procedures

**Density classes** (§7.1; thresholds [J]): `full` 150+ words per minute with dialogue → extract (C5, A3); `partial` 30–150 → dramatize stated events, author dialogue and staging (D2 R6), checkpoint T for invented scenes; `thin` under 30 → interview, author, checkpoint T. *The Catch*: 9,217 words for about 35 minutes ≈ 260. Density is triage only, not a runtime estimate (D2 R3).

**Invention budget** (§7.2): `minimal` may invent connective action, unnamed places, wording of stated lines; not events, characters, reveals, endings. `moderate` adds scenes dramatizing stated events, functional minor characters, dialogue; not new cardinal events or changed outcomes. `free` adds new events and characters serving stated ones; never anything contradicting a stated fact.

**Recipe I1. Triage (5 minutes; no cost).** Say:
*"Run intake triage on this file. Tell me the container; whether it has a text layer; the kind and dialect, with fingerprint counts; the languages; the word count; and the density class for a film of [N] minutes (if I have not given N, ask me for a rough length and mark it provisional). Convert nothing yet. List what you are unsure of as questions."*
Check the counts against what you know (*The Catch*: 30 scenes), then say "go on" or correct it. If the app cannot run code, add: *"Do not count by eye. List every matching line with its line number instead, and I will check the list"*.

**Recipe I2. Convert inside the chat app (10–20 minutes; claude.ai with code execution on).** Upload the file, then say:
*"Stage 0 conversion. In your sandbox: install pypdf and pypandoc_binary (it includes pandoc). Keep my original file untouched and give me its SHA-256 hash. Convert it to plain text: Word or ODT with pandoc (`-f docx+styles --track-changes=all` for Word); EPUB with pandoc; a PDF with pypdf in layout mode. Then compute the intake fingerprint on both the original and the converted text, show the two tables side by side, list every difference, and give me the converted file to download. Do not retype, correct or summarize any of the text. If a step needs a program you cannot install, stop and tell me which one."*
Check the hash, the counts (*The Catch*: 30 headings, 221 cues) and the tracked-change count (R36). No Tesseract [U]: go to I5.

**Recipe I5. OCR a scanned script (30–90 minutes for 40–120 pages; free).** In Claude Code on your own computer (not Cowork, which runs on Anthropic's servers):
1. *"Count characters extracted per page; list pages under 50."* Mostly near zero means a scan.
2. *"Install OCRmyPDF and Tesseract with [language] data. OCR with deskew and rotation fix; write a sidecar text file and a TSV file per page."*
3. For a script or play: *"Rebuild each line's indentation from word positions, group left edges into columns, and label them from left to right."* (Layout order in M1: action, dialogue, parenthetical, cue; transitions pushed right.)
4. *"List pages with mean confidence below 85 and words below 60."*
5. *"Show me the first, middle and last pages as images beside your text."* Check names, numbers, dialect, backwards text.
6. Continue with C5 Recipe 2.

**Thin-source procedure T0–T6** (§7.3):
1. **T0. Classify** the density (Recipe I1).
2. **T1. Fact list.** *"List every statement in the source as a numbered fact (F01, F02 …), quoting the words. Mark each `event`, `character`, `place`, `rule`, `tone` or `ending`. Add nothing."*
3. **T2. Gap list.** *"List what a screenplay needs that the facts do not give. Sort each gap into ASK (it changes what the story means: identities, motives, reveals, world rules, ending, tone, point of view, runtime, content limits) or DECIDE (connective or textural)."*
4. **T3. Interview.** *"Ask me the ASK questions one at a time, most important first, twelve at most, each with two or three options and a default. Record my answers as facts F-U01 … with `decided_by: human`."*
5. **T4. Expand one level at a time** (logline → one-paragraph synopsis → treatment, present tense, a paragraph per sequence → step outline in D2's format): *"Expand to the next level only. Mark every sentence no fact states with ⟨INV⟩ and the fact IDs it serves."* Each step-outline line gets `origin`.
6. **T5. Checkpoint T.** A script counts scenes and events by origin and the invented share; the user answers "keep", "change" or "cut" per invented scene ("Revise only step 7").
7. **T6. Author** one sequence per call in strict Fountain, each scene opening `[[origin: invented; serves F03, F07]]`. Result: `source.fountain` with `source_type: authored_from_thin`; the thin original kept as `source_original` with its hash.

**Conversion routes** (§3.1): Word → `pandoc -f docx+styles -t markdown --track-changes=all in.docx -o out.md` (pandoc 3.11; no PDF input). EPUB → `pandoc -f epub -t markdown` or `ebook-convert book.epub book.txt --txt-output-formatting=markdown` (calibre 9.15.0). OCR → `tesseract page.png out -l eng+tur --psm 4 tsv` or `ocrmypdf -l eng --deskew --rotate-pages --sidecar out.txt in.pdf out.pdf`. Cloud OCR (Document AI $1.50 and Mistral OCR 4.1 $4 per 1,000 pages; Textract $0.0015 a page) sends the manuscript to another company.

**Mappings** (§5–6): French scene → beat boundary; soliloquy → voice-over, direct address, line to a listener, or cut; aside → glance to lens, voice-over, or quiet line plus reaction; Blackout/Curtain/Intermission → cut or act break. Comic panel → shot candidate (`[[PAGE 3 PANEL 2]]`); page turn → cut on the reveal; captions → one rule for the work; SFX → sound cues (D9). Ink `*` choices and `->` diverts; Yarn `title:` … `---` … `===`; Twee `:: Passage [tags] {metadata}`.

## 5. Checklists

- **Every source:** rights recorded and DRM checked (R35); original hashed; container, kind, dialect, languages, density and runtime basis recorded with fingerprint counts; extraction route logged; three pages compared as images (PDF, OCR); UTF-8, NFC, LF; tracked changes counted and resolved (R36); counts agree or differences logged; every block mapped or excluded with a reason; source-marked breaks kept with `break_kind`; questions listed; checkpoint A passed.
- **OCR:** Claude Code, not Cowork; 300 dpi, deskewed, languages set; low-confidence pages read by a person; names, numbers and deliberate oddities checked by eye.
- **Thin source:** density against a stated or provisional runtime; quoted fact list; ASK and DECIDE split; budget chosen by the user; `serves_facts` on every invention; invention report by script; checkpoint T answered; `source_original` kept.
- **Non-English:** working language by R21, R22 or R33's test; translation in its own column; cues forced where there are no capitals; heading prefixes mapped per language; every spoken line has a language and a model-support value.

## 6. Saying it to AI models

- **claude.ai uploads (page dated 23 Jul 2026)** [V, S17]: PDF, DOCX, CSV, TXT, HTML, ODT, RTF, EPUB, JSON, XLSX; chat files 500 MB, 20 per chat, PDFs to 1,000 pages; Project files 30 MB, text extraction only. PDFs over 100 pages are read as text only, so a scan over 100 pages yields nothing: split or OCR it. `.md` is not listed: rename to `.txt`.
- **Never ask a model to retype a source**; ask it to run a program, list numbered lines or classify blocks.
- **Language prompts** [V, S41]: state input and output languages explicitly, and submit text in its "native script rather than transliteration". Anthropic's scores cover Sonnet 4.5 and Haiku 4.5 on translated MMLU, not newer models or literary reading [J].
- **Spoken-language support**: MiniMax H3, 11 stable languages (Arabic, Chinese, English, French, German, Italian, Japanese, Korean, Portuguese, Russian, Spanish) [V, S42]; HappyHorse 1.1, 7; Kling 3.0, 5, translating others into English; Gemini Omni, only English fully (C1, C3 §7B); ElevenLabs Multilingual v2, 29 including Turkish; Eleven v3, "70+" [V, S43]. Prompts stay in English; dialogue stays original (R21).

## 7. The Catch

**Decisions made**
- Dialect `catch_variant` by R1: 30 lines start `## INT`/`## EXT`, 221 start `@`, 8 start `=`, 3 start `>` (all transitions), 18 standalone parentheticals, no bare `INT` line (E1, M6).
- Line 10 `## INT. MEDICAL FACTORY - LOADING TUNNEL - NIGHT` would vanish in Fountain and become a heading in Markdown; line 8 `> FADE IN:` would become a quotation, so the extension cannot decide.
- `NELL ROWAN. FLIGHT TEST.` (line 990) and `IONA VALE.` (line 1233) are on-screen text, not speakers: in this dialect only `@` makes a cue.
- `@JUDE (V.O.)` / `(in her ear)` / `Was that you?` (lines 93–95) → `voice_source` (A3 R15); `(ON THE TABLET)` (line 838) is a presentation note; `VISOR VIEW:` (line 1506) is a shot instruction; `= THE CATCH` (line 488) and `= THE END` (line 1852) are cards, and the first follows `> CUT TO BLACK.`, so it gets `break_kind: card` for D16 R8.
- Encoding: UTF-8, NFC, LF; the only non-ASCII characters are two em dashes on title-page lines 5–6.
- As a 160-word synopsis (E3): under 5 words per minute, `thin`; about half the 30 scenes carry a stated event; the broken rung, the car, the kitchen tests, the playback, Nell's room, the falling ship, the last two scenes and all 221 speeches would be invented. R17 and R19: interview, then two or three step outlines at checkpoint T.

**Flagged for the user** (E3's ASK list; the real script answers each in a way no model would guess)
- Who Jude is to Iona: implied only by "His wedding ring. On his right hand." (line 1779) and "The two rings sit directly across from each other, like a ring and its reflection." (line 1783).
- When Iona learns Eli fired the device: withheld until the scene-13 recording ("You could have moved us out of the shaft." / "We would still have been falling."); a synopsis that states it must flag F07 as a reveal.
- Whether anyone else is on the ship (Nell Rowan, missing nineteen years, cannot come from the synopsis); what the figure is; how the mirror world is shown ("Every letter is backwards.", "The wheel is on the other side.", "Not mint."); tone, runtime, limits on the gunshot and blood.
- Labels must survive: an invented cage scene would lose the writer's paid-off details ("Goods only. No persons.", the yellow stripe, "A hard metal CLACK.").

**The Long Places** (E2): `prose`, `markdown_prose`; lines 1 and 3 `front_matter`; the letter (lines 7–33) opens chapters I–XIII and returns identically at 1415–1441 (`repeat_of`); Statement 3's lower case kept; Melek's song (lines 987–997) is `verse`. Ask the user: show the letter-writer? keep Statement 3's lower case on screen? Turkish village dialogue (not among H3's 11 languages; separate voices)?

## 8. Conflicts and open questions

- **C5 §10.3** should list `source_map.json`, `intake_log.json` and `source_original` among stage-0 files.
- **Checkpoint order**: C5 A (rights and scene list, or paragraph numbering) → T (thin sources only) → D2 M.
- **"C5 P8"** is the C5 digest's intake-normalization procedure; the full C5 file has no P8, and C5 rules are numbered 1–33.
- **D1 §13** (Cowork is server-side): resolved; OCR goes to Claude Code.
- **D16 R8** assumes D14 maps source breaks; now true through R34 and `break_kind`. D14 records breaks; D16 decides act status.
- **D2 R3** rejects words per minute for prose runtime; D14 uses it for triage only.
- **D18** uses `lang`; D14 uses `source_language`, `working_language`, `language`, `spoken_language` (all BCP 47). Pick one stem at build time. R25's `subtitle: yes` lines should feed D18's forced narratives.
- **Provenance labels**: A3 `fact`/`inference`/`invention`, C5 `extracted`/`authored`/`derived`, D14 `origin` and `provenance`. Mapping [J]: `origin: invented` = A3 `invention`; `dramatized_summary` = a fact staged by invention; `provenance: invented` blocks yield only `authored` fields. Needs one published table (critic's shared-vocabulary list).
- **D4**: rights before conversion (R35); verse to `underlying_works[]` (R37).
- **Open [U]**: Mistral OCR 4.1 batch discount; whether claude.ai's sandbox can install Tesseract; which pandoc pypandoc_binary 1.17 bundles; whether a .docx uploaded straight into claude.ai keeps tracked changes or styles. Google Docs suggestions → Word tracked changes is only [V-sec] (2014 blog; user reports of failures), so R36 checks. Thresholds (150/30 words per minute; OCR 85/60; 1 in 50; R33's 9 in 10) are judgments to calibrate.

## 9. Section map

Header and fact-check note → 1; §0 terms → 1; §1 principles → 2; §2 fingerprint, R1–R5, R31, R35, Recipe I1 → 2, 4, 7; §3.1 routes, claude.ai limits, R32, R36, Recipe I2 → 2, 4, 6; §3.2 OCR, Recipe I5 → 4; §3.3 silent failures, R6, R7 → 2; §3.4 app exports, R8 → 2; §3.5 encoding, R9, R10 → 2; §4 canonical forms, R11, R12 → 1, 2; §5 plays, R13, R14 → 2, 4; §6 comics and games, R15, R16 → 2, 4; §7 density, budget, T0–T6, R17–R20 → 2, 4; §8 languages, R21–R26, R33 → 2, 6; §9 documents and breaks, R27–R30, R34, R37 → 2; §10 checklists → 5; §11 fields, D14-V1–V10 → 3; §12 failure modes → 2, 5; §13 E1–E3 → 7; §14 conflicts → 8; Sources S1–S48, own tests M1–M8.
