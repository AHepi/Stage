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
| ID-03 | shot numbers go in tens; cards and black from 990 | PASS |
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
| FORM-08 | No record holds "...", "…", "etc.", "and so on", "same as above", "as before", "remaining shots", "omitted for brevity" or a line starting `//`, except inside exact story quotes. |
| FORM-12 | Every sub-part after ` \| ` has a template key (`at: left_third`, never a bare `left_third`); no text value holds ` \| `. |
| ID-01 | No ID appears twice as a record heading or as the first part of a SCENE `value` or SHOTLIST `item`. |
| ID-03 | Shot numbers go in steps of `shot_number_step`; an insert takes a number between; cards and black use `end_card_numbers`. |
| ID-06 | Every new ID lies in the block the step file gives (`issued_blocks`: beats B01 to B30, shots SH010 to SH400 per scene). |
| ID-07 | Every SHOT is an item of its scene's SHOTLIST; at standard and detailed, every list item in the batch's range has its SHOT. |
| ID-08 | Each SHOT's `beats`, `role` and `size` equal its list item's. |
| COVER-01 | In order, the first beat starts on the scene's first line after the heading, each next beat on the line after the last one ends, and the last ends on the scene's last line. |
| COVER-02 | Every story line of the scene lies in some shot's `lines` (a list item's beats at step 7 and at quick) or in `lines_not_shown` with a reason. In a batch, only the batch's beats. |
| COVER-03 | Every speech whose cue lies in those beats is a `hear` item of some shot. |
| COVER-04 | Every beat in range is in some shot's (or list item's) `beats`. |

A check with nothing to look at is written `PASS (no beats or shots in this file)`. A failure is written `FAIL: <record>, <what is wrong>`; fix the records and send the whole box again before the user saves it. The reply prints one line: "Checked in words: 14 of 14 passed", or only the failures. `00 Start here` keeps "Checked by the checker: never" until part 3.

## Part 2: in a check chat (20 checks, then questions)

At the end of each group of scenes the resume line sends the user to a new chat in the same Gem or Project with that group's saved files, the story, `02 Whole-film summary`, `10 Film rules` and `05 Checks in words` (in two messages when they pass the app's file limit), and the message "Check my group of scenes." Quote this part's task first: "Check the attached group against the story and return 13 Health check." Without the story, ask for it.

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
| CRAFT-03 | No shot before the main turn is as tight as the scene's tightest size (inserts not counted). |
| CRAFT-04 | Each beat whose `turn` is not `none` has exactly one shot with `role: turn`. |
| CRAFT-06 | `move` holds one value and no `moment` describes a second camera move. |
| CRAFT-14 | Every thing in frame with `origin: invented` is listed in the scene's `additions`. |
| CRAFT-18 | The sign test: every beat whose `turn` is not `none` flips the sign of some value's `charge` or reaches its `close`. |
| REASON-01 | Every shot has a `purpose` and a `because` naming a story ID or line (`default` only when nothing departs from the defaults). |
| REASON-03 | Every `why` holds a quote from the scene's lines, an ID, or a named element of the scene. |
| REASON-04 | No `why` holds a mood-only phrase ("to build tension", "for drama", "cinematic", "moody", "dynamic", or "to emphasise" with no object). |
| WORDS-01 | No `does` or `task` holds an emotion adjective (angry, sad, afraid; `emotion_adjectives` in `rules/words.json`); write what the body does. |

**The time floor by hand.** Floor = the larger of the speech floor and the text floor, plus the pause owed. Speech floor: for each `hear` item, the speech's words ÷ the speaker's `pace_wps` (`speech_wps_default` if the voice has none), plus `speech_floor_extra_s`. Text floor: `text_floor` for each text in picture in frame, doubled when mirrored. Pause owed: for each beat whose last line lies inside the shot's lines, its `pause_after` seconds, or `turn_reaction_min_s` for a turn if that is larger. Scene 10, shot 150: Saye 19 words at 2.0 = 9.5 s, Iona 2 words at 2.5 = 0.8 s, three speeches add 1.5 s, so the speech floor is 11.8 s; the turn at beat 7 owes 2.0 s; the floor is 13.8 s, and 15 passes.

**Then the questions,** once the user reaches those steps. Step 9: with the sound off, does each turn picture tell its beat? Could a stranger say what each scene is about from its turn pictures and purposes? Is there a symbol not in the story, a scene with more than `plant_inserts_per_scene_max` plant inserts, music under an unsaid line, a light cue on the line that states the point, a rhyme the story does not support? Does any shot feel like a different film? Step 10: the questions and scores of `reference/05 Quality rubric.md`. Answer each yes or no against the story, quoting the record and the line (D7 R3).

**What the check chat returns:** `13 Health check.md` in one copy box, "Save as: 13 Health check.md" above it: the plain part ("In short: 2 things need you, 5 findings to fix", then what to fix first, one line each), the divider, one REVIEW per scene of the group (`RV-SC07` ...) with its answers (and its scores once the user has reached step 10), one FINDING per failed check or "no" answer (`record`, `rule`, `evidence`, `fix`, `source: review`, `status: open`), and the END line. The next working chat attaches it, fixes those findings first, and marks each `fixed`.

## Part 3: the real check

Words are weaker than code. At the end of each group, or at least before acceptance, the user attaches the folder as one ZIP and the story on the Claude website (the free plan is enough) and types "Check my breakdown."; `stage.py adopt` then `check --all` run every check (the house rules, "What the user may type").

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
