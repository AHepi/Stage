# 11 Steps 09-11 and 16 - film pass, check, book, resume

Part of the Stage chat kit: a step-group file, attached to the chat that runs one of these steps (not knowledge). It joins the step files 09 Film pass, 10 Check and estimate, 11 Book and exports, 16 Resume and recovery, each whole. Read the one for this unit every time, quote its one-line task back before any work, and follow its section "If you cannot run code" when this chat has no code. 01 House rules (in the knowledge) says where every other skill file is.

---

From the skill file `steps/09 Film pass.md`:

# Step 9. Film pass

This is step 9 of the pipeline; the user counts it as step 10 of 12, "the film pass". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Judge the whole film as one structure before any picture is made: run the film checks, answer the film pass questions in a fresh unit, and turn every "no" into a finding with its fix.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Scenes were designed one at a time; this step reads them as one. The Catch: scene 29's reflection shot must repeat scene 10's framing (the same long lens, level, along the glass) for the rhyme to land, and no scene before scene 13 may spend the film's tightest size. No single scene can see either. Structure beats single frames (B3 P4): a film whose every scene spends its strongest choice has nowhere to go. It finds where the film repeats itself or spends too early, and sends each fix to the scene that needs it.

## When it runs

Once, after the last sequence's shots are written, before the health check. At quick depth only the code audits run: there are no full shots to judge. With a partial scope (The Long Places, chapter I as a trial) it covers the scenes in scope only. "Run the film pass again" runs it again at any time.

## Inputs

- The **film strip**, made by code: one line per shot with its ID, beats, role, size, lens, camera move, saved choice used, emphasis, screen time and the scene's intensity. For example: `SC10-SH150 | SC10-B07, SC10-B08 | turn | close_up | 50 | static | none | MO-MINT 2 | 15 | 6`.
- The film rules: CAMSYS, CAMRULE, RESERVE, LENS, LOOK, VISUAL, SOUNDPLAN, LADDER.
- PLAN (`crisis`, `climax`, each `peak` and its reason), MOTIF appearances, and the SCENE records (plan fields, turn pictures).
- The checker's film-level report.

Judgement works from these, never the story whole.

## Outputs

- `12 Whole-film check.md`: the plain part (code's audit report: what was checked, found and fixed), the divider, one FINDING per problem, the END line. Code writes the checker's findings (`source: checker`); the judgement unit writes its own (`source: film_pass`).
- CHOICE records in `01 Choices.md` for findings that change a creative choice, usually none to three.
- Fixes, routed back to steps 7 and 8 for the named scenes only.

## Card parts to open

At every depth: card 09, part "Film pass".

## Procedure

1. **Code audits.** Run `stage.py check --film`. It builds the film strip and runs FILM-01 to FILM-12 and TIME-07; card 09, "Film pass", says what each one catches. Two are errors: FILM-03 (a character camera rule broken: Eli closer than `medium_close_up` before scene 13) and FILM-08 (a saved choice over its uses or outside its places, including the film-level extreme close-up and push-in). The rest are warnings. Code writes one FINDING per problem.
2. **Fix what the checker found.** Every error is fixed. Every warning is fixed or accepted with a `reason` that quotes the story or cites a record: FILM-02's warning on scene 29 is accepted because the sides are reversed on purpose, Iona being turned back (B3 P8). `stage.py impact <ID>` names what a fix touches; redo only those units of steps 7 and 8. Fix only the lines printed, at most `repair_rounds_max` rounds (C5 R13), then trace the fault to its earliest wrong record or ask one plain question.
3. **Judgement unit** (U-09-JUDGE). A fresh unit that wrote none of the shots answers these questions, one scene or turn at a time, each naming and quoting its record (C5 R12; D7 R3):
   - **Sound-off test:** with the sound off, does each turn picture tell its beat (B3 §10.1)? "Does shot 150's picture (Iona chews, stops, frowns) tell beat 7, 'Her face changes.', without her line?"
   - **Stranger test:** could someone who has not read the story say what changes in each scene from its turn pictures and purposes alone (D7 §7)?
   - **Heavy-handedness:** a symbol the story does not hold (B3 R24; B4 R25)? More than `plant_inserts_per_scene_max` inserts of plants in one scene? Music under a beat whose meaning is unsaid (A4 §7.6)? A light cue timed to the line that states the point (B2 §12)? A rhyme the story does not support (B3 P8)?
   - **Different film:** does any shot feel as if it belongs to a different film (B3 R26)?
4. **Write the findings.** Each "no" becomes a FINDING: `record` (the shot, scene or film rule), `rule` (the check ID, or the question as asked), `evidence` (the record's words and the story line they rest on), `fix`, `source: film_pass`, `status: open`. A finding with no quoted evidence is dropped (D7 R4).
5. **Sort the findings.** A fix that only brings a shot back inside the film rules is made and logged, and its FINDING set `fixed`. A finding that changes a creative choice (a peak moved, a saved choice spent somewhere else, a rhyme dropped, a scene played in a different tone) becomes a CHOICE with a default and its reason, `asked: yes`, `checkpoint: acceptance`, and the FINDING stays `open` until it is answered.
6. **Check.** Run `stage.py check --step 9`: every FILM error fixed, every FINDING `fixed` or `accepted` with a reason, or `open` behind an open CHOICE.

## Record template

`templates/13 Health check.md`, its FINDING part (the same record in `12 Whole-film check.md`); `templates/01 Choices.md` (CHOICE).

## IDs you will be given

Code numbers the checker's findings. The handout gives the judgement unit a block of finding numbers that follows them (for example FIND-021 onward) and the next free choice number (CHOICE-031 onward). Copy them in order; never reuse a number, even for a finding later accepted.

## Batch and chunk rules

The judgement unit reads the whole strip at once when it is under `film_strip_tokens_per_unit_max` tokens (The Catch at about 300 shots: about 12,000); above that, one unit per act (U-09-JUDGE-A1, U-09-JUDGE-A2 ...), each with the film rules and PLAN, and the last asks one more question: do the acts' ladders join into one climb?

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Would the film's turn pictures tell the story with the sound off?
2. Does no shot feel like a different film?
3. Is every FILM error fixed, and every warning fixed or accepted with a reason that quotes a line or cites a record?
4. Was the judgement unit fresh, and did every question quote its record?
5. Does every finding name its record, rule, evidence and fix?
6. Did each fix redo only the scenes it names?
7. Does each choice put to the user change a creative choice, and have a default?

## The report

Fill it from the project; these are illustrative counts for The Catch (message shapes: `reference/07 Report and message formats.md`):

```
Done: step 10 of 12, the film pass.
Example: nothing before scene 13 is as close as its shot of Iona on "You.", and the
  crossing in scenes 26 and 27 is played wide and still, as the film's rules say.
Made: 12 Whole-film check: 7 problems found and fixed in 4 scenes (the details are
  in the file), 1 for you to choose.
Needs you: one choice, with an answer ready.
  1. Scene 24 already spends the film's strongest colour and contrast on the
     fire. A push-in on "She deletes the way home." would add a third. Keep the
     camera still there?                                                      [yes]
  I'm carrying on with the health check; your answer changes only scene 24.
Next: the health check, with three scenes for you to read.
```

## Checkpoint

None that waits. Only findings that change a creative choice reach the user, as choices with defaults, in this step's report; the work carries on. A choice not answered by the finished check is shown there again, among its things to check, and then defaulted.

## How to redo

"Run the film pass again": `stage.py check --film` runs again and a fresh judgement unit answers the questions again. Fixed findings stay fixed, accepted ones keep their reasons, and only new problems get new numbers. A later change to one scene ("Redo scene 10") marks the film pass stale; it runs again before the health check.

## If you cannot run code

Every line reference is a quote anchor: each finding's `evidence` quotes the record and the story line exactly, at least `quote_anchor_words_min` words, never a line number.

1. There is no film strip. The film pass runs in check chats, one per group of scenes, after the last group's own check. Each chat attaches that group's scene files (in two messages when they pass the app's file limit), `02 Whole-film summary`, `10 Film rules`, `05 Checks in words`, `11 Steps 09-11 and 16 - film pass, check, book, resume`, and the last saved `12 Whole-film check` (for the first group, the last `13 Health check` instead), and the user types "Run the film pass on these scenes."
2. In that chat, quote this step's one-line task, then answer step 9's questions of `reference/06 Checks in words.md` part 2 for the group, and check by hand the two errors you can count: each character camera rule (nothing closer than its `limit_before` before its `closest` story point; nothing on its `never` list) and each saved choice's uses against `max_uses` and `allowed_in`.
3. Save the findings as `12 Whole-film check.md`, the whole file each time: the earlier groups' findings carried forward, then this group's, numbered on from the highest FIND number in the attached files, the checks-in-words table, the END line. Choices go in `01 Choices - film pass.md`.
4. The other film checks (the ladder, rhymes, colour, sameness, counts) need code: they run at the real check on a code surface, where `adopt` is followed by `check --film`. Say so once in the report.
5. Report, then the resume line; after the last group it names step 10's first health-check chat:

```
Save as: 12 Whole-film check.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach the files of scenes 11 to 13,
02 Whole-film summary, 10 Film rules, 05 Checks in words, 12 Whole-film check and
11 Steps 09-11 and 16 - film pass, check, book, resume; type: Run the film pass
on these scenes.
```

**One-line task, again:** Judge the whole film as one structure before any picture is made: run the film checks, answer the film pass questions in a fresh unit, and turn every "no" into a finding with its fix.

---

From the skill file `steps/10 Check and estimate.md`:

# Step 10. Check and estimate

This is step 10 of the pipeline; the user counts it as step 11 of 12, "the health check". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Prove the breakdown complete and consistent, have fresh units answer its yes/no review questions and score it on the rubric, estimate its time and cost from the shots, and ask the user to read three scenes.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Prove the breakdown is complete and consistent, score its quality, and say what it will cost. Example: the finished check for The Catch opens "In short: one thing needs you (reading three scenes); 14 small fixes I made; 3 warnings", and then says the film runs about 36 minutes in 468 shots (illustrative numbers: the step prints the computed ones). Code checks what can be counted, fresh units answer what needs judgement, the user reads three scenes (principle 9).

## When it runs

Once, after the film pass. At quick depth it runs without the questions and scores, which start at standard depth. "Check again" runs it at any time. With a partial scope it covers the scenes in scope, and the health check says so first: "Scope: 5 of 48 scenes".

## Inputs

All records; the checker's report; `12 Whole-film check.md`; the adapter files and `adapters/prices.json` for the lint and the money; the story, read only in the lines each question cites.

## Outputs

- `13 Health check.md`. Its plain part, in this order: the first line ("In short: 2 things need you, 14 small fixes I made, 3 warnings"); on a partial scope the scope line; the quality scores; "3 scenes to read"; then the details by file. Below the divider: one REVIEW per scene in scope (`RV-SC10`) and one for the film (`RV-FILM`), and a FINDING for each problem.
- `14 Time and cost.md`: the estimate from the shots (runtime, shots, generated seconds, money by tier, hours, calendar).
- `For machines - do not edit/breakdown.json`, and a first `15 The breakdown/` on code surfaces.

## Card parts to open

At every depth: `reference/05 Quality rubric.md`, whole; card 21, part "Cost".

## Procedure

1. **The book first.** Run `stage.py export book`. It is cheap, can be remade any time, and gives the user the three scenes as pages.
2. **The whole check.** Run `stage.py check --all`: every field at the project's depth, every check. Tidy fixes are applied and logged (FORM-13); real problems are fixed, only the lines printed, at most `repair_rounds_max` rounds (C5 R13); then a trace to the earliest wrong record, or one plain question for the user.
3. **The lint.** Run `stage.py compile --lint-only`: it routes every shot to its scene model and lints the prompt without writing any pack. Its GEN error count scores rubric criterion 9; a GEN error is fixed in the shot record, never in a prompt.
4. **The estimate from the shots.** Run `stage.py estimate --version v1`. It works out runtime, shots, generated seconds, money at all three tiers and hours of review; never type a total (card 21, "Cost"). If the model facts are older than `model_facts_max_age_days`, it prints no money (GEN-11; D13 R7): with web access, run the refresh (`stage.py refresh-models --propose`, the user approves any price change, then `--apply`); without it, the report says the money waits for fresh prices.
5. **The questions.** Run `stage.py questions --sample`. It writes yes/no questions for every turn shot, turn beat and must-keep shot, every shot that needs mirror, text or violence handling, and a seeded share (`question_sample_share`) of the rest, each citing the lines it can be checked against (C5 R11; D7 R3, R5): "Does Iona's face change before she says 'Not mint.' (lines 454 to 463)?"
6. **Fresh answers.** Units U-10-QUESTIONS-B1, B2 and on, each a fresh unit that wrote none of the records (C5 R12), answer one batch against the story, reading only the records and lines its questions cite. Each answer is an `answer` item on its scene's REVIEW, with its evidence. Each "no" also becomes a FINDING (`source: review`). A finding without quoted evidence is dropped (D7 R4); a sampled shot with a blocking finding widens the sample (D7 R6).
7. **Fix, then check again.** Fix the findings as in item 2 above, then run `stage.py check --all` once more.
8. **Scores** (U-10-SCORES). Only once `check --all` reports no error, because scores on a broken file measure the break (D7 R1). A fresh unit scores the ten criteria of `reference/05 Quality rubric.md`, 0 to 3, with one line of evidence each, per scene in scope and for the film. The film passes by the pass rule in `reference/05`; a score under 2 carries a FINDING with its fix. Scores are advice: judges agree with people only weakly (D7 §8), so the user reads three scenes.
9. **The three scenes to read** (`scenes_to_read`): the climax scene, the scene with the most dialogue, and the biggest action scene. The Catch: scene 26, scene 13, scene 06.
10. **Check.** Run `stage.py check --step 10`, then give the report below.

## Record template

`templates/13 Health check.md` (REVIEW, FINDING).

## IDs you will be given

REVIEW records are named by what they score: `RV-` and the scene (`RV-SC10`), and `RV-FILM`. Code numbers the checker's findings; the handout gives each question unit a block of finding numbers that follows them (FIND-041 onward). Copy them in order; never reuse one.

## Batch and chunk rules

Questions come in batches of `question_batch_size`, one fresh unit per batch, each reading only the records and lines its questions cite, never the story whole. The scores are one fresh unit (U-10-SCORES).

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Were the review questions answered by a fresh unit (in chat, a check chat), not the writer?
2. Does `check --all` report no error?
3. Does every score carry one line of evidence that names a record, a field or a story line?
4. Is the rubric's pass rule met, and does every score under 2 have a finding with its fix?
5. Did the lint find 0 GEN errors on the scene models, or is every one listed as a finding?
6. Is every money figure from the estimate and dated, with none printed on stale prices?
7. Are the three scenes the climax, the most dialogue and the most action?

## The report

The finished check's message (`reference/07 Report and message formats.md`), filled with the computed numbers:

```
Done: step 11 of 12, the health check. In short: one thing needs you (reading three
  scenes); 14 small fixes I made; 3 warnings (listed in 13 Health check).
Example: the film runs about 36 minutes in 468 shots; making it with AI would cost
  about $2,900 to $7,600 and 45 to 90 hours of watching takes (14 Time and cost).
Made: 13 Health check, 14 Time and cost, and a first version of 15 The breakdown.
Needs you: please read three scenes in 15 The breakdown (about 20 minutes): 26 (the
  climax), 13 (the most talk), 06 (the most action), with the 10 questions in
  05 How to read your breakdown.
  Anything you want changed in these three scenes?                            [no]
Next: I'll finish the book, the spreadsheets, the captions and the timeline.
```

## Checkpoint

The finished check. It waits for the answer; "defaults" accepts [no]. At most `acceptance_items_max` things to check, each with a default and often none (a film pass choice still open is one of them), and the three scenes with the 10-question review sheet of `05 How to read your breakdown`. A change the user asks for: `stage.py impact` on what it touches, say what it redoes in plain words, redo only that, then check again. Nothing else runs until it is answered or defaulted.

## How to redo

"Check again" runs this step again at any time: the checker, the lint, the estimate, fresh questions and fresh scores. New answers and scores replace the old; findings keep their numbers and states.

## If you cannot run code

Every line reference is a quote anchor: each question and each evidence line quotes the story or the record, at least `quote_anchor_words_min` words, never a line number.

1. The health check runs in check chats, never in the chat that wrote the files: one per group of scenes, attaching the group's scene files, `02 Whole-film summary`, `10 Film rules`, your story, `11 Steps 09-11 and 16 - film pass, check, book, resume`, `05 Checks in words`, and the previous group's health-check file so the finding numbers go on from it. The user types "Check my group of scenes."
2. That chat runs `reference/06 Checks in words.md` part 2, then writes the review questions by hand: every turn shot, turn beat and must-keep shot, every shot with mirror, text or violence handling, and one remaining shot in every ten, in shot order. It answers them against the story, scores the rubric for each scene, and saves `13 Health check - group 3.md`: the group's REVIEW and FINDING records, the checks-in-words table, the END line.
3. Criteria scored only by measuring (1, 5, 6, 8 and 9) are scored from the checks in words, labelled "checked in words", and scored again at the real check.
4. The estimate is rough and labelled rough: screen time added up from the scene files; no money is printed without the checker and fresh prices.
5. After the last group, one short chat attaching the group files, `12 Whole-film check` and `00 Start here` writes `13 Health check.md`: its plain part, `RV-FILM`, the END line. The three scenes are read as the plain parts of their scene files.
6. Before the finished check, the real check: "Open the Claude website (the free plan is enough), attach the folder as one ZIP and your story, and type: Check my breakdown." It runs `adopt`, `check --all`, `build` and `export all`.

```
Save as: 13 Health check - group 3.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach the files of scenes 11 to 13,
02 Whole-film summary, 10 Film rules, 05 Checks in words, 13 Health check - group 3,
11 Steps 09-11 and 16 - film pass, check, book, resume and your story;
type: Check my group of scenes.
```

**One-line task, again:** Prove the breakdown complete and consistent, have fresh units answer its yes/no review questions and score it on the rubric, estimate its time and cost from the shots, and ask the user to read three scenes.

---

From the skill file `steps/11 Book and exports.md`:

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

At every depth: card 23, whole; `reference/07 Report and message formats.md`, whole.

## Procedure

1. **Make everything.** Run `stage.py export all`. It builds, then writes the four folders above. With `rights: study_only`, every export is marked "Private study, not for publication" on its first page or first row.
2. **Check the formats.** Run `stage.py check --step 11`: the shot list opens with its byte-order mark and has exactly its columns; the timeline passes the structural check; the captions pass the SubRip and WebVTT format checks; `breakdown.json` validates against its schema, nested at most three levels. A failure is a fault in the code or a record: fix the record (or report the code fault plainly), never the file.
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

The book step's last message (`reference/07 Report and message formats.md`), for The Catch:

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

---

From the skill file `steps/16 Resume and recovery.md`:

# Step 16. Resume and recovery

This file is "carrying on": it is not one of the 12 steps the user counts. Use it whenever the user types "Continue my breakdown." or "continue", and whenever something goes wrong. Read it each time, never from memory.

**One-line task:** Pick up where the work stopped, say in one line where things stand, and carry on with the next unit, or recover from a cut-off reply, skipped records, a full chat, a lost file, an unreadable attachment or a refusal, using the files and never memory.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Files are the only memory. Example: in Claude Code the user types "Continue my breakdown." the next day; you run `stage.py status` and answer "Yesterday we finished scenes 1 to 12. Next: scene 13. Nothing is waiting for you.", then read step 7's file and design scene 13. App memory features are turned off or ignored, because remembered facts from older versions can contradict the files (D1 R10). A reply that fails is never repaired by hand: it is sent again, in whole records (D1 §6.2).

## When it runs

- The user resumes, in any app, in a new chat or the same one.
- A reply was cut off or skipped records, the chat is full, a file is lost, an attachment cannot be read to its end, a step is refused, or you cannot quote a choice you need.
- The app compacted the conversation: run `status` again and re-read the current step file.

## Inputs

PROJECT and `00 Start here.md` (where things stand, the next step, the big choices, the log); the manifest in `For machines - do not edit/` (units done, each batch's expected and received counts, locks; code surfaces); the newest save ZIP on the Claude website and ChatGPT; in chat, the files the resume line named.

## Outputs

None, or the missing records sent again; on the Claude website and ChatGPT a save ZIP when a chat ends; in chat without code, `00 Start here` and `02 Whole-film summary` rewritten at a stop point.

## Card parts to open

At every depth: `reference/07 Report and message formats.md`, whole.

## Procedure

1. **Where are we?** On a code surface run `stage.py status`; without code read `00 Start here`. Say one line: what is done, what is next, what waits for the user. Never answer from memory: if you cannot quote a choice from `01 Choices` or `00 Start here`, ask for that file.
2. **By surface.**
   - Claude desktop with a folder, and Claude Code: `status`, then `stage.py next`, then the next unit's step file, read fresh, its one-line task quoted.
   - The Claude website and ChatGPT: the user attaches the newest save ZIP; run `stage.py unpack <zip>`, read `00 Start here`, then as above. One group of scenes per chat (`units_per_chat`), and earlier if the app says it is summarising or usage passes `chat_usage_handover_share` (D1 R5, R6): finish the unit, run `stage.py pack` (`023 Save - The Catch - after scene 10.zip`), and give the message below. On ChatGPT the download link expires: say so (D1 R7).
3. **A reply cut off** (no END line, or a count short of the approved list; D1 R4). The user types **continue**: send again from the start of the record that was cut (shot 170, when the reply stopped inside it), then the END line. A record is never split across replies.
4. **Records skipped** (IDs missing from the approved list, or a shortening marker such as "same as above"). The user types **continue**: send only the missing records, complete, then an END line counting them (D1 §6.2).
5. **A format slip** ("medium closeup", an unknown field): the checker makes tidy fixes itself and logs them (FORM-13); real problems come back as "Fix only these". Fix only those lines, at most `repair_rounds_max` rounds (C5 R13), then one plain question with a default, or a trace to the earliest wrong record.
6. **An early choice changed** ("make it 16:9"): run `stage.py impact` on what it changes, say in plain words what it touches and how long it takes, ask once if it is costly, then redo only those units. Locked records change only through an answered choice.
7. **A file lost.** `00 Start here` lists what should exist. On Claude surfaces restore it from git or the last save ZIP; `apply` keeps earlier versions in `For machines - do not edit/history/`. In chat apps redo that scene from the story.
8. **An attachment not read to the end**: if you cannot quote its first and last lines, ask the user to paste the missing part.
9. **A fact not in the story** (the CITE checks): mark it "not found in the story"; fix it, or keep it labelled `invented` and listed.
10. **A refusal** of the story's content (scene 6's gunshot and blood): say once that this is planning for the user's own film and you need only camera, staging and continuity fields; use production words ("gunshot sound effect", "wound make-up"). If refused again, log it and suggest another model or app for that scene. Never disguise the content (D1 §6.5, R12).
11. **Then carry on** with the next unit of its own step, as that step's file says.

## Record template

None of its own. Records sent again follow the template of the step that was interrupted (for shots, the SHOT part of `templates/11 Scene.md`).

## IDs you will be given

None new. Copy every ID from the approved list, the manifest or the saved file; a record sent again keeps its ID. Never renumber to close a gap; an omitted record keeps its number.

## Batch and chunk rules

The resume is one line, then the next unit under its own step's batch rule. A re-sent part is the missing records only, in ID order, within the step's batch size.

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Did the one line of where things stand come from the files, not from memory?
2. Did you read the next unit's step file afresh and quote its one-line task?
3. After a cut-off, does the re-sent part start at the record that was cut and end with the END line?
4. After skipped records, did you send only the missing IDs?
5. Did a change redo only what `impact` named, leaving locked records alone?
6. After a refusal, did you use production words once and never disguise the content?

## The report

The resume line, then the next unit's own report (`reference/07 Report and message formats.md`):

```
Yesterday we finished scenes 1 to 12. Next: scene 13. Nothing is waiting for you.
```

When the chat is long (the Claude website, ChatGPT):

```
This chat is getting long. Start a new chat in this project, attach the save file,
and type: Continue my breakdown.
```

When something went wrong (the user types only the word in bold, **continue**):

```
My reply was cut off inside shot 170. Type continue and I'll send it again from shot 170.
```

## Checkpoint

None. A recovery that needs the user asks one plain question with a default; "continue" answers every cut-off.

## How to redo

"continue" sends again. A record is never split across replies, and a saved file that failed its checks is sent whole again before the user saves it.

## If you cannot run code

Every line reference is a quote anchor, here as in every step; a re-sent record keeps its quote anchors word for word.

1. The user starts a new chat in the Gem or Project, attaches the files the resume line named (the step-group file, the story, `00 Start here`, `02 Whole-film summary`, `10 Film rules`, `08 Places and things` when needed, the previous scene file) and types "Continue my breakdown." Quote the step file's one-line task, then carry on from "Next step".
2. One group of scenes (3 to 5 scenes) per chat. At the budget, rewrite `00 Start here` and `02 Whole-film summary` in copy boxes and give the exact message for the new chat. At a group's end the resume line names the check chat.
3. File names: a reply that only adds records to a saved file saves them as `<numbered file> - <what they hold>.md` (`09 Continuity - scenes 06-10.md`, `Scene 10 - Saye's kitchen - shots 130-200.md`), each with its own END line; `adopt` merges them by ID. A reply that changes a saved record saves the whole file again and names the extra files to delete.
4. A box with no END line is never saved. After **continue**, send the file again in parts that each end with an END line: first the records that were complete, as `Scene 10 - Saye's kitchen - shots 130-160.md`, then, in the next reply, the rest from the start of the cut record, as `Scene 10 - Saye's kitchen - shots 170-200.md`.
5. `00 Start here` shows "Checked by the checker: never" until the real check. Report, then:

```
Save as: nothing new in this reply.
To continue later: new chat in this project; attach 00 Start here, 02 Whole-film summary,
10 Film rules, 10 Steps 07-08 - scenes and shots, your story and Scene 12 - Demonstration
room; type: Continue my breakdown. Next is scene 13.
```

**One-line task, again:** Pick up where the work stopped, say in one line where things stand, and carry on with the next unit, or recover from a cut-off reply, skipped records, a full chat, a lost file, an unreadable attachment or a refusal, using the files and never memory.
