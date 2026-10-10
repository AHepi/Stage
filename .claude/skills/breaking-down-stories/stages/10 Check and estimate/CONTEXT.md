# Step 10. Check and estimate

This is step 10 of the pipeline; the user counts it as step 11 of 12, "the health check". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Prove the breakdown complete and consistent, have fresh units answer its yes/no review questions and score it on the rubric, estimate its time and cost from the shots, and ask the user to read three scenes.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Prove the breakdown is complete and consistent, score its quality, and say what it will cost. Example: the finished check for The Catch opens "In short: one thing needs you (reading three scenes); 14 small fixes I made; 3 warnings", and then says the film runs about 36 minutes in 468 shots (illustrative numbers: the step prints the computed ones). Code checks what can be counted, fresh units answer what needs judgement, the user reads three scenes (principle 9).

## When it runs

Once, after the film pass. At quick depth it runs without the questions and scores, which start at standard depth. "Check again" runs it at any time. With a partial scope it covers the scenes in scope, and the health check says so first: "Scope: 5 of 48 scenes".

## Inputs

All records; the checker's report; `12 Whole-film check.md`; the adapter files and `_config/adapters/prices.json` for the lint and the money; the story, read only in the lines each question cites.

## Outputs

- `13 Health check.md`. Its plain part, in this order: the first line ("In short: 2 things need you, 14 small fixes I made, 3 warnings"); on a partial scope the scope line; the quality scores; "3 scenes to read"; then the details by file. Below the divider: one REVIEW per scene in scope (`RV-SC10`) and one for the film (`RV-FILM`), and a FINDING for each problem.
- `14 Time and cost.md`: the estimate from the shots (runtime, shots, generated seconds, money by tier, hours, calendar).
- `For machines - do not edit/breakdown.json`, and a first `15 The breakdown/` on code surfaces.

## Card parts to open

At every depth: `references/formats/05 Quality rubric.md`, whole; card 21, part "Cost".

## Procedure

1. **The book first.** Run `stage.py export book`. It is cheap, can be remade any time, and gives the user the three scenes as pages.
2. **The estimate from the shots.** Run `stage.py estimate --version v1`. It works out runtime, shots, generated seconds, money at all three tiers and hours of review; never type a total (card 21, "Cost"). If the model facts are older than `model_facts_max_age_days`, it prints no money (GEN-11; D13 R7): with web access, run the refresh (`stage.py refresh-models --propose`, the user approves any price change, then `--apply`); without it, the report says the money waits for fresh prices. It also writes the date of the model facts that `check --all` asks for, so it runs first.
3. **The whole check.** Run `stage.py check --all`: every field at the project's depth, every check. Tidy fixes are applied and logged (FORM-13); real problems are fixed, only the lines printed, at most `repair_rounds_max` rounds (C5 R13); then a trace to the earliest wrong record, or one plain question for the user. TIME-03 only warns, past `scene_total_tolerance` of the scene's own list; the first estimate's target is a guess and is not judged.
4. **The lint.** Run `stage.py compile --lint-only`: it routes every shot to its scene model and lints the prompt without writing any pack. Its GEN error count scores rubric criterion 9; a GEN error is fixed in the shot record, never in a prompt.
5. **The questions.** Run `stage.py questions --sample`. It writes yes/no questions for every turn shot, turn beat and must-keep shot, every shot that needs mirror, text or violence handling, and a seeded share (`question_sample_share`) of the rest, each citing the lines it can be checked against (C5 R11; D7 R3, R5): "Does Iona's face change before she says 'Not mint.' (lines 454 to 463)?"
6. **Fresh answers.** Units U-10-QUESTIONS-B1, B2 and on, each a fresh unit that wrote none of the records (C5 R12), answer one batch against the story, reading only the records and lines its questions cite. Each answer is an `answer` item on its scene's REVIEW, with its evidence. Each "no" also becomes a FINDING (`source: review`); a fault no question asked about goes in the unit's report, not in a finding. A finding without quoted evidence is dropped (D7 R4); a sampled shot with a blocking finding widens the sample (D7 R6).
7. **Fix, then check again.** Fix the findings as in item 3 above, then run `stage.py check --all` once more.
8. **Scores** (U-10-SCORES). Only once `check --all` reports no error, because scores on a broken file measure the break (D7 R1). A fresh unit scores the ten criteria of `references/formats/05 Quality rubric.md`, 0 to 3, with one line of evidence each, per scene in scope and for the film. The film passes by the pass rule in `references/formats/05`; a score under 2 carries a FINDING with its fix, and one FINDING may be cited by several scores. RV-FILM's `answer` items are step 9's four film-pass questions (sound-off, stranger, heavy-handedness, different-film), answered from the film strip and `12 Whole-film check`. Scores are advice: judges agree with people only weakly (D7 §8), so the user reads three scenes.
9. **The three scenes to read** (`scenes_to_read`): the climax scene, the scene with the most dialogue, and the biggest action scene. The Catch: scene 26, scene 13, scene 06.
10. **Check.** Run `stage.py check --step 10`, then give the report below.

## Record template

`references/templates/13 Health check.md` (REVIEW, FINDING).

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

The finished check's message (`references/formats/07 Report and message formats.md`), filled with the computed numbers:

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

The finished check. It waits for the answer; "defaults" accepts [no]. At most `acceptance_items_max` things to check, each with a default and often none (a film pass choice still open is one of them), and the three scenes with the 10-question review sheet of `05 How to read your breakdown`. A change the user asks for: `stage.py impact` on what it touches, say what it redoes in plain words, redo only that, then check again. Nothing else runs until it is answered or defaulted. The user's answers go in `For machines - do not edit/inbox/acceptance.md`: each open choice as `### CHOICE CHOICE-NNN` with `- answer:`, and each finding the answer settles marked `fixed` or `accepted` with its reason (a "no" settles only what the user read; other open findings stay open and are named in the report); apply it, run `stage.py check --all`, then `stage.py next --checkpoint-passed`. A question that quotes a count says it was counted at the check.

## How to redo

"Check again" runs this step again at any time: the checker, the lint, the estimate, fresh questions and fresh scores. New answers and scores replace the old; findings keep their numbers and states.

## If you cannot run code

Every line reference is a quote anchor: each question and each evidence line quotes the story or the record, at least `quote_anchor_words_min` words, never a line number.

1. The health check runs in check chats, never in the chat that wrote the files: one per group of scenes, attaching the group's scene files, `02 Whole-film summary`, `10 Film rules`, your story, `11 Steps 09-11 and 16 - film pass, check, book, resume`, `05 Checks in words`, and the previous group's health-check file so the finding numbers go on from it. The user types "Check my group of scenes."
2. That chat runs `references/formats/06 Checks in words.md` part 2, then writes the review questions by hand: every turn shot, turn beat and must-keep shot, every shot with mirror, text or violence handling, and one remaining shot in every ten, in shot order. It answers them against the story, scores the rubric for each scene, and saves `13 Health check - group 3.md`: the group's REVIEW and FINDING records, the checks-in-words table, the END line.
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
