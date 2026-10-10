# Step 11. Book and exports

This is step 11 of the pipeline; the user counts it as step 12 of 12, "the book and exports". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Make the book, the spreadsheets, the captions, the audio description and the timeline from the records with one command, check each file's format, and tell the user which files are for reading and which are for other programs.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Hand the user the deliverable. Example: `15 The breakdown/The breakdown.html` opens with "How to read this", explained on shot 150 of their own scene 10, and each scene page starts with its "At a glance", then the one-line shot list, with the full shots folded underneath. Everything this step makes is generated from the records and never edited (principle 1): a file that is wrong is fixed in its record and made again.

## When it runs

Once, after the finished check is answered or defaulted. "Make the book again" runs it at any time; it takes minutes. After any later change the exports go stale and are made again at the end of that change. With a partial scope (The Long Places, chapter I as a trial) the exports hold the scenes in scope, and the book says so on its first page.

## Inputs

All records, turned into `For machines - do not edit/breakdown.json` by `stage.py build`; `13 Health check.md` and `14 Time and cost.md`; PROJECT `rights`, `frame_shape` and `fps`; the voices' `pace_wps` for caption timing.

## Outputs

- `15 The breakdown/The breakdown.html` and `The breakdown.md`: contents; "How to read this", with examples from the user's own story; the story plan; people, places and things; the film rules in plain words; each scene with its "At a glance", the one-line list first and the full shots folded underneath; the word list. It prints cleanly.
- `16 Spreadsheets/Shot list.csv` (one row per shot in film order, UTF-8 with a byte-order mark, the fixed columns; the crew label, "10Q" for shot 150, appears only here) and `People, places and things.csv`.
- `17 Captions and audio description/`: `The Catch.srt`, `The Catch.vtt`, `Audio description script.md`, `Text to translate.md`.
- `For machines - do not edit/`: `timeline.otio`, `timeline.edl`, `breakdown.json`, `breakdown.schema.json`.

## Card parts to open

At every depth: card 23, whole; `references/formats/07 Report and message formats.md`, whole.

## Procedure

1. **Make everything.** Run `stage.py export all`. It builds, then writes the four folders above. With `rights: study_only`, every export is marked "Private study, not for publication" on its first page or first row.
2. **Check the formats.** `export all` checks them itself and prints "Format checks passed": the shot list opens with its byte-order mark and has exactly its columns; the timeline passes the structural check; the captions pass the SubRip and WebVTT format checks; `breakdown.json` validates against its schema, nested at most three levels. A failure is a fault in the code or a record: fix the record (or report the code fault plainly), never the file. Then `stage.py next` says "Finished".
3. **Read the captions against card 23.** Code times them from the records: each shot starts where the one before ends, one cue per heard speech, the first starting `caption_lead_s` after the shot starts, each lasting its words at the speaker's pace, never under `caption_min_s` or over `caption_max_s`. The words come from the speech records, never from recognition (D8 R47). An off-screen speaker's cue starts with the name ("SAYE:"); a sound at sound emphasis 2 or more gets a tag, and a motif always the same tag (D8 R51; D18 R7).
4. **Read the audio description script** (a narrator's voice in the gaps telling a blind viewer what to see). It covers every shot with `needs_description: yes`, from `does`: what the frame shows, never a feeling and never anything kept hidden (D18 R3, R10). Scene 10, shot 150: "She chews, then stops. Her eyes drift down. One more slow chew." A line that interprets is fixed in the shot's `does` or `keep_hidden`, then the export is made again.
5. **Read the book's first page and one scene page** as the user will: plain words, no codes or abbreviations above any divider (WORDS-04 runs on the book). A slip goes back to its record or to the view code as a fault, and the book is made again.
6. **Choose one next step for this project**, never a list: storyboards when the user wants to see the film first; grey previews in Claude Code when framing-critical shots are waiting (The Catch: about 26); prompts for AI video when they want to make it. At quick depth say once: "Quick plans can't be turned into AI video prompts until a scene is made standard. Say 'go deeper on scene N' for the scenes you want to make."
7. **Report** with the message below. It names the three files to open first and says which files are for reading and which are for other programs.

## Record template

None: this step writes no records. The book's layout and the spreadsheet columns are fixed by code; nothing here is typed by hand on a code surface.

## IDs you will be given

None. Every file is named by the project: captions and the timeline carry the story's title (`The Catch.srt`); shots appear as "shot 150" everywhere but the shot list's crew-label column.

## Batch and chunk rules

Code, one command, any length: the whole film in one run. Nothing here is split into units, and no unit reads the whole story. In chat without code this step is one reply (U-11-CONTENTS).

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Was every export made: the book in both forms, both spreadsheets, both caption files, the description script, the translation list, the timeline in both forms and the machine files?
2. Does the shot list open with its byte-order mark and hold exactly its columns?
3. Do the timeline and both caption files pass their format checks?
4. Are the captions' words the speech records' words, with off-screen speakers named?
5. Does the description script say only what each frame shows?
6. Is the book free of codes and abbreviations above every divider, and marked private study where the rights say so?
7. Does the last message name the three files to open first and exactly one next step?

## The report

The book step's last message (`references/formats/07 Report and message formats.md`), for The Catch:

```
Done: step 12 of 12, the book and exports. Your breakdown is finished.
Example: the book explains how to read it on shot 150 of scene 10: Iona's
  close-up, held 15 seconds, from the first chew through Saye's answer.
Made: for reading, 15 The breakdown (open The breakdown.html in your browser,
  or print it). For other programs: 16 Spreadsheets (the shot list, and the
  people, places and things), 17 Captions and audio description, and a
  timeline for your editing program in For machines - do not edit.
  Open these three first: 15 The breakdown, 13 Health check, 14 Time and cost.
Needs you: nothing.
Next, if you want to see it: say "make storyboards" (about $10 and an hour).
```

## Checkpoint

None. The report says which files are for reading and which are for other programs, and offers one next step; nothing waits.

## How to redo

"Make the book again": run `stage.py export all` again; it takes minutes. Exports are never edited by hand, only made again from the records. A change after this step ("Change shot 150 to ...") goes through `stage.py impact`, redoes only the units it touches, and ends by running this step again.

## If you cannot run code

Every line reference is a quote anchor, but this step writes no records: only the book's contents page.

1. Unit U-11-CONTENTS: write `15 The breakdown/The breakdown.md` as a contents page in one copy box. First "How to read this", in five plain lines with one example from the story (shot 150 of scene 10 and its reason); then each numbered file of the folder with one line on what it is for; then every scene file by its name, with its event sentence from `02 Whole-film summary`. The user opens the scene files themselves; their plain parts are the book's pages.
2. End the box with `END OF FILE | The breakdown contents | 0 records`, so a cut-off reply shows.
3. The spreadsheets, captions, audio description, timeline and machine files need code. They are made at the real check: "Open the Claude website (the free plan is enough), attach the folder as one ZIP and your story, and type: Check my breakdown." The Claude website runs `adopt`, `check --all`, `build` and `export all` and hands the files back. Say so once in the report, in place of the files you cannot make.
4. Report, then:

```
Save as: 15 The breakdown/The breakdown.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 02 Whole-film summary,
10 Film rules, your story and 12 Steps for add-ons - storyboards, prompts, finishing;
type: Make storyboards.
```

**One-line task, again:** Make the book, the spreadsheets, the captions, the audio description and the timeline from the records with one command, check each file's format, and tell the user which files are for reading and which are for other programs.
