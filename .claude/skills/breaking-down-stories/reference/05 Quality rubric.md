# Quality rubric

A breakdown is scored on ten criteria, each from 0 to 3, one REVIEW record per scene in scope and one for the film. Example first, from The Catch scene 10:

```
### REVIEW RV-SC10 Scene 10 scores
- scope: SC10
- answer: Does Iona's face change before she says "Not mint." (lines 454 to 463)? | answer: yes | evidence: SC10-SH150 moments 4-6 and 6-8
- score: 3 | score: 3 | evidence: SC10-SH150 is the scene's one close-up, spent on the main turn SC10-B07, as its turn picture says
- score: 4 | score: 3 | evidence: every why quotes the scene or cites an ID; SC10-SH130 lands Eli's line on the flask it protects (CR-ELI)
```

In `score` items the first part is the criterion's number and the `score` sub-part its score. Every score carries one line of evidence that names a record, a field or a story line. A finding without evidence is dropped (D7 R4).

## When, and who scores

- **When.** At step 10, on every scene in scope and on the film, after `stage.py check --all` reports no ERROR: scores on a broken file measure the break (D7 R1). In chat apps without code, the check chat scores each group's scenes once the user has reached step 10 (`reference/06 Checks in words.md` part 2); what only the checker can measure is scored at the real check on a code surface.
- **Who.** A fresh unit that did not write the records (in chat apps, the check chat), never the writer (D7 §2; C5 R12). Scores are advice: AI judges agree only weakly with people (D7 §8), so the user also reads three scenes with the review sheet in `05 How to read your breakdown.md`.
- **How**, in the table's second column. **M**: measured by the checker; read the check IDs named for it from `13 Health check`. **J**: yes/no questions answered by the fresh unit against the story. On a code surface `stage.py questions --sample` builds them for every turn shot, turn beat and must-keep shot, every shot needing mirror, text or violence handling, and a seeded share (`question_sample_share`) of the rest, in batches of `question_batch_size` (C5 R11; D7 R3, R5). Without code, write the same questions by hand, taking one remaining shot in every ten (`question_sample_share`), in shot order. Each answer is a REVIEW `answer` item; each "no" also becomes a FINDING. **U**: the user's reading of the three scenes. Coverage and counts are scored from the checker's report, never from a judge's impression (C5 R25).

## The anchors

| Score | Meaning |
|---|---|
| 0 | Wrong or missing. |
| 1 | Correct but generic: default coverage, reasons that would fit any film. |
| 2 | Specific to this story and following the film rules. |
| 3 | A head of department would sign it: the choice shows what the story implies without saying it, with restraint. |

Where a row below gives a measure for 2 and 3, a result under the measure for 2 scores 1, and a missing or wrong result scores 0.

## The ten criteria

| # | Criterion | How | 2 means | 3 means | Read it from |
|---|---|---|---|---|---|
| 1 | Faithful to the story | M | every line covered; quotes exact; inventions labelled | and every addition approved | COVER-01 to COVER-05; CITE-01 to CITE-06; CRAFT-14; additions that change meaning answered at each group of shots |
| 2 | Story reading (events, values, turns, climax) | J, U | 80 to 94% of judge questions pass | 95% or more, and the user agrees on the sample | questions on turn beats, the sign test (CRAFT-18) and PLAN's crisis and climax; the user's answer at acceptance |
| 3 | Shots serve beats | M, J | every purpose names a change; one turn shot per turn | and turn shots are the scene's extremes and match their turn pictures | REASON-01, CRAFT-04, REASON-05; CRAFT-03 and TIME-10; a question per turn picture |
| 4 | Reasons | M, J | every `why` anchored; no mood-only reason | and no sampled reason fails the any-film test | REASON-02 to REASON-04; the any-film test on sampled reasons (card 09; B3 R26) |
| 5 | Restraint and economy | M | budgets and saved choices kept; plants quiet | and no shot a cut could replace; no stacked signals | CRAFT-01, CRAFT-02, CRAFT-08 to CRAFT-12, CRAFT-19, FILM-08, FILM-09 |
| 6 | Continuity and sides | M | no state or side errors | and every state has its reference plan | STATE-01 to STATE-04; SIDE-01 to SIDE-05; `pictures_needed` on every STATE |
| 7 | Rhythm and time | M, J | floors met; holds within budget; scene totals within `scene_total_tolerance` | and each scene's rhythm shape shows in its durations | TIME-01 to TIME-05, TIME-08; a question on the scene's `rhythm_shape` |
| 8 | Visual system | M | film rules followed; departures carry reasons | and the ladder escalates and rhymes land (the film pass is clean) | CRAFT-07, CRAFT-11, CRAFT-16, FILM-01 to FILM-12, REASON-02; `12 Whole-film check` |
| 9 | Ready for generation | M | `stage.py compile --lint-only` reports 0 GEN errors on the scene model | and every hard case has its references and guide inputs listed | GEN-01 to GEN-17; the picture and previs jobs of mirror, text and action shots |
| 10 | Readable for the user | J, U | plain part above the divider; no abbreviations; At a glance per scene | and a fresh unit given only the scene's plain page answers 5 questions about the scene correctly | WORDS-02, WORDS-04; five questions to a fresh unit; the user's review sheet |

## The pass rule

A scene passes when there is no ERROR, no criterion scores 0, criteria 1, 3 and 6 score 2 or more, and the total is 20 or more of 30. The film passes when every scene in scope passes (D7 §5.2); RV-FILM gives each criterion the lowest score of any scene, with that scene named in its evidence, and scores criterion 8 from the film pass.

Every score below 2 carries one line of evidence and a fix. Write the fix as a FINDING (`rule: rubric criterion 4`, `source: review`, `status: open`) and cite its ID in the score's evidence. Fix only the findings named, run the checks again and score only the criteria they touch, at most `repair_rounds_max` rounds (C5 R13; D7 R8). A finding that survives them, or needs a story choice, becomes one plain question for the user.

## What a 3 looks like, and a 1

- **Criterion 3, a 3.** Scene 10's main turn, "Her face changes.", gets the scene's only close-up (shot 150), held 15 seconds through Saye's answer off screen, exactly as the turn picture describes. **A 1.** Every speaker gets a close-up in turn; the turn shot is one of many at the same size.
- **Criterion 4, a 3.** "Eye level on Saye (CR-SAYE: she holds power by stillness, not angle); she wins at SC10-B11 by waiting." **A 1.** "Low angle to make Saye powerful": true of any film, and a mood, not this story.
- **Criterion 5, a 3.** The mint is planted at emphasis 1, a pot at the edge of the kitchen's one wide (shot 30), and pays off on Iona's face in the close-up, not on an insert. **A 1.** Push-in, music sting and a light change all on the same beat.

No criterion is improved by a "review and improve" pass (C5 R12; C5 §6.7): the fixes come from findings, the checker and the fresh unit's answers.
