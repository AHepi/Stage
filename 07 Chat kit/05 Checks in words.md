# 05 Checks in words

Part of the Stage chat kit: knowledge, and attached to every check chat. It joins `reference/06 Checks in words.md` (part 1: the checks every reply runs on its own file; part 2: the checks a separate check chat runs on a group of scenes; part 3: the real check on the Claude website) and `reference/05 Quality rubric.md` (the ten criteria the finished check scores).

---

From the skill file `reference/06 Checks in words.md`:

# Checks in words

Without code, checking is split: counting and matching in the reply that wrote the records (part 1), judgement and arithmetic in a separate check chat (part 2), the real checker later on a code surface (part 3). No reply judges its own work (C5 R12; D1 R3). Example first, and the template for part 1: the end of a saved batch file of scene 10.

```
- status: approved
- locked: yes

---

Checked in words: 14 of 14 passed.

| Check | What it checks | Result |
|---|---|---|
| FORM-05 | every field needed at this depth is present | PASS |
| FORM-06 | the file ends with its END line | PASS |
| FORM-07 | the END line's count matches the records | PASS |
| FORM-08 | no shortening marker inside a record | PASS |
| FORM-12 | sub-parts are named, and no text holds a space, bar, space | PASS |
| ID-01 | no ID is used twice | PASS |
| ID-03 | shot numbers go in tens; end cards and black from 990 | PASS |
| ID-06 | every new ID is inside the numbers given for this step | PASS |
| ID-07 | every shot is in the scene's shot list | PASS |
| ID-08 | each shot's beats, role and size match its list item | PASS |
| COVER-01 | every story line of the scene is in a beat | PASS |
| COVER-02 | every story line of the scene is in a shot | PASS |
| COVER-03 | every speech is heard in a shot | PASS |
| COVER-04 | every beat has a shot | PASS |

END OF FILE | Scene 10 - Saye's kitchen - shots 010-120 | 12 records
```

## Part 1: in the reply that writes the records (14 checks)

Count and match only. The `---` line ends the last record (G3), so the table is free text (G1) and the END line counts only the `###` records.

| Check | How to check it by hand |
|---|---|
| FORM-05 | Every field of the template at the project's depth (or the scene's deeper one) whose step is this one or earlier is present; empty is `none`, undecided `open`. |
| FORM-06 | Exactly one line `END OF FILE \| <what the file holds> \| <n> records` ends the file. |
| FORM-07 | `n` equals the number of lines starting `### ` below the divider. |
| FORM-08 | No record holds "...", "…", "etc.", "and so on", "same as above", "remaining shots", "omitted for brevity", "as before" standing for a value, or a line starting `//`, except inside exact story quotes. |
| FORM-12 | Every sub-part after ` \| ` has a template key (`at: left_third`, never a bare `left_third`); no text value holds ` \| `. |
| ID-01 | No ID appears twice as a record heading or as the first part of a SCENE `value` or SHOTLIST `item`. |
| ID-03 | Shot numbers go in steps of `shot_number_step`; an insert takes a number between; end cards and black use `end_card_numbers`. |
| ID-06 | Every new ID lies in the block the step file gives (`issued_blocks`: beats B01 to B30, shots SH010 to SH400 per scene). |
| ID-07 | Every SHOT is an item of its scene's SHOTLIST; at standard and detailed, every list item in the batch's range has its SHOT. |
| ID-08 | Each SHOT's `beats`, `role` and `size` equal its list item's. |
| COVER-01 | In order, the first beat starts on the scene's first line after the heading, each next beat on the line after the last one ends, and the last ends on the scene's last line. |
| COVER-02 | Every story line of the scene lies in some shot's `lines` (a list item's beats at step 7 and at quick) or in `lines_not_shown` with a reason. In a batch, only the batch's beats. |
| COVER-03 | Every speech whose cue lies in those beats is a `hear` item of some shot. |
| COVER-04 | Every beat in range is in some shot's (or list item's) `beats`. |

A check with nothing to look at is written `PASS (no beats or shots in this file)`. A failure is written `FAIL: <record>, <what is wrong>`; fix the records and send the whole box again before the user saves it. The reply prints one line: "Checked in words: 14 of 14 passed", or only the failures. `00 Start here` keeps "Checked by the checker: never" until part 3.

## Part 2: in a check chat (20 checks, then questions)

At the end of each group of scenes the resume line sends the user to a new chat in the same Gem or Project with that group's saved files, the story, `02 Whole-film summary`, `10 Film rules`, `05 Checks in words` and the last saved `13 Health check` file, if any (two messages past the app's file limit), and the message "Check my group of scenes." Quote this part's task first: "Check the attached group against the story and return 13 Health check." Without the story, ask for it.

| Check | How to check it in words |
|---|---|
| CITE-01 | Every line reference in a scene record (`lines`, `line:` in `because`, story points) lies inside the scene's lines. |
| CITE-02 | Each quoted string of a quote anchor or story point has at least `quote_anchor_words_min` words and occurs exactly once in its scope (the scene for story points and scene fields, else the whole story). |
| TIME-01 | Each shot's `screen_time` reaches its floor (below). |
| TIME-04 | At most `long_pauses_per_scene_max` beats of a scene have `pause_after: long`. |
| TIME-05 | Every beat whose `turn` is not `none` owes at least `turn_reaction_min_s`. |
| TIME-08 | Every `pause_after` has seconds inside its tier (`pause_tiers`); a hold above the long tier needs a saved choice (an RC ID) in the shot's `because`. |
| SIDE-01 | Every `side` item has `own: left` or `own: right`. |
| SIDE-02 | No state line or fixed description holds image-side words ("frame-left", "left of the image"). |
| SIDE-03 | A sided insert (a ring, a palm, a scar) has `flip: never`. |
| CRAFT-01 | At most `push_in_per_scene_max` shots of a scene have `move: push_in`. |
| CRAFT-02 | At most `extreme_close_up_per_scene_max` extreme close-ups, only on the main turn. |
| CRAFT-03 | The main turn is at its ladder rung's size, nothing before it tighter unless the rung is wide (inserts not counted). |
| CRAFT-04 | Each beat whose `turn` is not `none` has exactly one shot with `role: turn`. |
| CRAFT-06 | `move` holds one value and no `moment` describes a second camera move. |
| CRAFT-14 | Every thing in frame with `origin: invented` is listed in the scene's `additions`. |
| CRAFT-18 | The sign test: every beat whose `turn` is not `none` flips the sign of some value's `charge` or reaches its `close`. |
| REASON-01 | Every shot has a `purpose` and a `because` naming a story ID or line (`default` only when nothing departs from the defaults). |
| REASON-03 | Every `why` holds a quote from the scene's lines, an ID, or a named element of the scene. |
| REASON-04 | No `why` holds a mood-only phrase ("to build tension", "for drama", "cinematic", "moody", "dynamic", or "to emphasise" with no object). |
| WORDS-01 | No `does` or `task` holds an emotion adjective (angry, sad, afraid; `emotion_adjectives` in `rules/words.json`); write what the body does. |

**The time floor by hand.** Floor = the larger of the speech floor and the text floor, plus the pause owed. Speech floor: for each `hear` item, the speech's words ÷ the speaker's `pace_wps` (`speech_wps_default` if the voice has none), plus `speech_floor_extra_s`. Text floor: `text_floor` for each text to read (plot-critical or with emphasis), doubled when mirrored. Pause owed: for each beat this shot ends (the last shot naming it), its `pause_after` seconds, or `turn_reaction_min_s` for a turn if that is larger. Scene 10, shot 150: Saye 19 words at 2.0 = 9.5 s, Iona 2 words at 2.5 = 0.8 s, three speeches add 1.5 s, so the speech floor is 11.8 s; the turn at beat 7 owes 2.0 s; the floor is 13.8 s, and 15 passes.

**Then the questions,** once the user reaches those steps. Step 9: with the sound off, does each turn picture tell its beat? Could a stranger say what each scene is about from its turn pictures and purposes? Is there a symbol not in the story, a scene with more than `plant_inserts_per_scene_max` plant inserts, music under an unsaid line, a light cue on the line that states the point, a rhyme the story does not support? Does any shot feel like a different film? Step 10: the questions and scores of `reference/05 Quality rubric.md`. Answer each yes or no against the story, quoting the record and the line (D7 R3).

**What the check chat returns:** one copy box with "Save as: 13 Health check - group 3.md" (the group's number) above it: the plain part ("In short: 2 things need you, 5 findings to fix", then what to fix first, one line each), the divider, one REVIEW per scene of the group (`RV-SC07` ...) with its answers (and its scores once the user has reached step 10), one FINDING per failed check or "no" answer (`record`, `rule`, `evidence`, `fix`, `source: review`, `status: open`), numbered on from the attached health-check file, and the END line. `adopt` merges the group files by ID. The next working chat attaches it, fixes those findings first, and marks each `fixed`.

## Part 3: the real check

Words are weaker than code. At the end of each group, or at least before acceptance, the user attaches the folder as one ZIP and the story on the Claude website (the free plan is enough) and types "Check my breakdown."; `stage.py adopt` then `check --all` run every check.

## Numbers this page uses

Copied from `rules/constants.json`, which wins if they ever differ.

| Name | Value |
|---|---|
| `speech_wps_default` | 2.5 words per second |
| `speech_floor_extra_s` | 0.5 s per speech |
| `text_floor` | the larger of 2.0 s and 1.0 s + characters ÷ 13; with emphasis 2 or more, at least 2.0 s + 0.5 s per word; mirrored × 2 |
| `turn_reaction_min_s` | 2.0 s |
| `pause_tiers` | short from 0 to under 1.0 s; medium from 1.0 to under 2.5 s ("(beat)" is 1.0 s); long from 2.5 to 4.0 s; above 4.0 s a hold |
| `long_pauses_per_scene_max` | 2 |
| `push_in_per_scene_max`, `extreme_close_up_per_scene_max` | 1 and 1 |
| `quote_anchor_words_min` | 3 words |
| `plant_inserts_per_scene_max` | 2 |
| `shot_number_step`, `end_card_numbers` | 10; 990 to 999 |
| `issued_blocks` | beats 1 to 30, shots 10 to 400, per scene |

## Numbers the step files name

Without code there is no `rules/constants.json`; the step files name these numbers, and their values are here. Copied from `rules/constants.json` and `rules/limits.json`, which win if they ever differ.

| Name | Value |
|---|---|
| `batch_size` | 12 shots a reply; 18 once the code self-test passes (in chat: 12) |
| `repair_rounds_max` | 3 rounds |
| `event_unit_scenes`, `continuity_unit_scenes` | 10 scenes; 5 scenes |
| `chapter_digest_words_max`, `outline_chapters_per_unit` | 350 words; 2 to 3 chapters |
| `step_outline_tolerance`, `fact_records_typical` | a tenth of the runtime target; about 5 to 15 facts |
| `short_runtime_max_s` | 2400 s (40 minutes): under it `short`, otherwise `feature` |
| `scene_ids_three_digits_above`, `speech_ids_three_digits_above` | 99 scenes; 99 speeches in a scene |
| `style_words_count` | 8 to 15 style words |
| `minor_characters_per_unit`, `places_per_unit` | 4; 2 |
| `lineup_columns_differ_min` | 3 of the six lineup columns |
| `fixed_description_words` | principals 25 to 40 words; minor characters 20 to 30 |
| `voice_description_words` | 30 to 50 words |
| `motif_spines_max`, `sound_motif_max`, `body_motif_max` | a short 3 to 5, a feature 5 to 8 spine motifs; 1 sound motif; 1 body motif |
| `loud_sets_max` | a short 2, a feature 3 |
| `previs_plan_level_min` | 2 |
| `checkpoint_b_items_max`, `checkpoint_b_marked_items` | 7 items; 3 marked |
| `whole_film_summary_words_max` | 6000 words |
| `extreme_close_up_film_max`, `push_in_scene_share_max` | a short 3, a feature 6; push-ins in at most a quarter of the scenes |
| `look_block_sentences`, `look_block_words_max` | 2 to 3 sentences; 60 words |
| `colour_monotony_run`, `device_budget_short` | 3 groups of scenes; in a short at most 2 each of cut to black, true silence and freeze |
| `beat_intensity_5_per_part_max`, `departments_changing_at_main_turn_max` | 2; 2 |
| `scene_split_non_blank_lines`, `scene_split_beats` | 70 lines; 14 beats |
| `stations_needed_above_beats`, `stations_per_scene` | 8 beats; 2 to 4 stations |
| `hold_needs_still_s`, `main_actions_per_seconds` | 2.0 s; one main action per 4 s |
| `film_strip_tokens_per_unit_max` | 20000 tokens |
| `question_batch_size`, `question_sample_share`, `scenes_to_read`, `acceptance_items_max` | 40 questions; a tenth; 3 scenes; 3 things |
| `model_facts_max_age_days`, `handles_s` | 30 days; 0.75 s at each end |
| `cheap_test_above_usd_per_take`, `takes_stop_per_route`, `takes_stop_per_shot`, `spend_check_share` | 2 dollars; 4 failed takes; 10 failed takes; half |
| `chat_usage_handover_share` | 0.8 of the chat's usage |

---

From the skill file `reference/05 Quality rubric.md`:

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

- **When.** At step 10, on every scene in scope and on the film, after `stage.py check --all` reports no ERROR: scores on a broken file measure the break (D7 R1). In chat apps without code, the check chat scores each group's scenes once the user has reached step 10 (`reference/06` part 2); what only the checker measures waits for the real check.
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

A scene passes when there is no ERROR, no criterion scores 0, criteria 1, 3 and 6 score 2 or more, and the total is 20 or more of 30. The film passes when every scene in scope passes (D7 §5.2); RV-FILM gives each criterion the lowest score of any scene, with that scene named in its evidence; criterion 8 takes the lower of that and the film pass. A 3 out of reach here (the user's agreement before acceptance, `pictures_needed`, the five-question test) scores 2, saying so.

Every score below 2 carries one line of evidence and a fix. Write the fix as a FINDING (`rule: rubric criterion 4`, `source: review`, `status: open`) and cite its ID in the score's evidence. Fix only the findings named, run the checks again and score only the criteria they touch, at most `repair_rounds_max` rounds (C5 R13; D7 R8). A finding that survives them, or needs a story choice, becomes one plain question for the user.

## What a 3 looks like, and a 1

- **Criterion 3, a 3.** Scene 10's main turn, "Her face changes.", gets the scene's only close-up (shot 150), held 15 seconds through Saye's answer off screen, exactly as the turn picture describes. **A 1.** Every speaker gets a close-up in turn; the turn shot is one of many at the same size.
- **Criterion 4, a 3.** "Eye level on Saye (CR-SAYE: she holds power by stillness, not angle); she wins at SC10-B11 by waiting." **A 1.** "Low angle to make Saye powerful": true of any film, and a mood, not this story.
- **Criterion 5, a 3.** The mint is planted at emphasis 1, a pot at the edge of the kitchen's one wide (shot 30), and pays off on Iona's face in the close-up, not on an insert. **A 1.** Push-in, music sting and a light change all on the same beat.

No criterion is improved by a "review and improve" pass (C5 R12; C5 §6.7): the fixes come from findings, the checker and the fresh unit's answers.
