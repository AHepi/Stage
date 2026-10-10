# 32 Fixes - after the full run

The fixes for the problems found in the full run on The Catch (Project notes 31). Log entry 32.

**Read with note 33.** A second helper then tried to prove these fixes wrong (log entry 33). It found five fixes that went too far and let real faults through, and several wrong sentences in this note. All were repaired before anything was saved; the sentences below are corrected, and each correction says "(corrected after note 33)".

## What changed, in short

**One example from the story first.** At the climax (scene 26) Iona lets go of the rail, and the film's plan asks for a wide shot held long, the only time the camera floats free. Before, the checker asked for an extreme close-up there, which the film's own rules forbid in that scene, and the book printed "A break from CAMSYS" under the shot. Now the checker follows the film's plan and says nothing about that shot, and the book says "A break from the camera system".

**What was done:**
- 17 of the 18 problems are fixed, and one (the handout sizes) is fixed only in part. Problem 3 had already been fixed during the run.
- On The Catch, the full check went from 1 error and 126 warnings to no errors and 29 warnings. Every warning left is explained below. Most are real craft points; a few come from records written under the old rules.
- The video-prompt check went from 133 problems to 40.
- "What's next" now says "Finished" once the book and the exports are made.
- The book no longer shows the kit's internal names.
- A new test, with one part for each fix, passes. Every older test passes except the size check on three chat-kit files, which was already failing before and is no worse. Seven older tests had to change, because the rules they checked were changed on purpose. They are listed near the end.

**What it means for you:** the kit no longer argues with itself in the places the run found. A helper who follows the instructions should now be able to finish a scene without warnings it cannot clear. That is not yet tried: no new scene has been written with the fixed kit (corrected after note 33). The rule for switching to a format people can't read (JSON) now counts only real layout mistakes, and by that count the readable format stays.

## The numbers, before and after

| What | Before | After |
|---|---|---|
| Full check: errors | 1 | 0 |
| Full check: warnings | 126 | 29 |
| Closest shot at the turn (the ladder warning) | 40 | 0 |
| Unaware character held too short | 33 (8 people-in-scenes, each printed once per secret) | 6 |
| Light the story writes, not covered | 22 | 3 |
| Two shots too alike, no jump cut found | 3 | 0 |
| Light or sound added on a marked moment | 2 | 0 |
| Too many changes at once on a turn | 3 | 0 |
| Secret shown before its reveal | 2 | 0 |
| Black shot numbered below 990 | 2 | 1 |
| Video-prompt check: problems | 133 | 40 |
| Banned words in prompts ("cage", "flask") | 54 | 0 |
| Prompt describes what the picture already shows | 29 | 1 |
| Prompt asks the model to draw text | 42 | 31 |
| Kit names in the book (CAMSYS, SOUNDPLAN, LADDER, "PLAN peak", camera_break) | 14, 6, 35, 6, 1 | 0 in each |
| The scoring handout | 175,045 tokens | 24,520 tokens |
| "What's next" at the end | back to the film pass | "Finished" |
| Film length in the book | "42 minutes of film" | "42 minutes of story (43 with titles and credits)" |
| Chat-kit files that were too long (02, 04, 05 words) | 20,111, 17,840, 3,174 | 20,110, 17,835, 3,172 |
| Tests | 19 files, 1 failing (chat-kit size) | 20 files, 1 failing (the same) |

## Problem by problem

**1. Jump cuts after shots below 100. Fixed.** The checker now keeps the zero, so a jump cut after shot 070 is found. On The Catch the three false warnings about shots that look too alike are gone.
For maintainers: `checks_sides_geometry.cut_after` builds `{scene}-C{number:03d}`; test group P1.

**2. An error that could not be cleared, and no "finished". Fixed.** The checker no longer writes "..." into its own suggested fixes. The shortening check no longer judges text the checker wrote, which the AI may not edit anyway. The old stored wording is rewritten by the next film check. "What's next" now ends with "Finished: the breakdown is done, the book and the exports are made." It no longer looks at file dates, which every check changed. Instead the kit notes which records the film strip and the book were made from. They count as up to date until a record changes. Rewriting the plain top part of a file doesn't count.
For maintainers: FORM-08 skips code-written fields (`checks_form.written_by_code`); `film_pass.NEW_PEAK_WORDING`, `refresh_code_text` and the OLD to NEW migration; `project_files.records_signature`, `remember_made_from`, `made_from_current_records` ("made from.json"); `make_handout.file_is_fresh`, `newest_record_change` ignores report files; `run_next` "Finished"; groups P2.

**3. The kit wrote into its own example folder. Already fixed during the run** (entry 29); nothing new here. The example folder is now only remade by the maintainers' build command, and it comes out clean: "nothing needs you, no warnings".
For maintainers: no change in this pass.

**4. The approval mark nobody could fix. Fixed.** The checker no longer asks for a shot list's approval mark until that group of shots has been passed. When it does ask, the advice now says to run "what's next", which is what sets it. If "passing the checkpoint" is run when nothing is waiting, it now says so and carries on, instead of stopping with an error. The step file and the main instructions now say that only the first group of shots waits. Later groups are passed by a plain "what's next".
For maintainers: `checks_form.approval_not_yet_due` and `scenes_with_group_passed` (reads `manifest["checkpoints"]`, passed to FormContext in `check_records`); `code_field_fix` for SHOTLIST approved; `run_next --checkpoint-passed` exit 0; steps/07 and SKILL.md; groups P4.

**5. Long scenes planned twice. Fixed.** Whether a scene is written in parts is decided once, when its first handout is made, and kept. A scene already written whole is never planned again in parts. Step 7 now states the split rule with its number (more than 14 beats or 70 lines).
For maintainers: `make_handout.scene_is_big` reads `manifest["scene_splits"]`, then the units already applied; `write_handout` records the decision; group P5.

**6. Handouts too big. Partly fixed.**
- The scoring handout was 175,045 tokens. It now gives each review in brief (the counts, every "no" answer in full, the scores) and is 24,520 tokens.
- When a handout is too big, the kit now first leaves out the worked example. Next it shortens the records the unit only reads. Only after that does it drop card parts. The world step keeps the mirror rule; the camera step keeps its cards.
- Very long record lists become a short index of names.
- The judging step's part units, which the code already planned, are now listed in the steps file, so their handouts are accepted.
- The worked example is left out of scene 10's own handouts, because the example *is* scene 10 and would give the answer away.
- The advice for a handout still too big now names only a split that really exists.
- The handout's first line says to read it in parts when the file reader takes less at once.

What is not fixed: shot handouts for the biggest scenes are still 27,000 to 30,000 tokens. That is under the kit's limit of 30,000, but over what the file reader takes at once (about 25,000), so they still take two reads. In scenes 6 and 23 the lowest-listed card parts (suspense, and one more card) are still left out to fit.
For maintainers: `Handout.fit` order in `make_handout` (example, `records` sections to `trimmed_text` brief, cards, source); `INDEX_ONLY_ABOVE_RECORDS`; `review_summary`; `split_advice`; `example_section` leaves the gold out when the scene heading matches; `U-09-JUDGE-A<n>` in steps.json; `limits.json handout_over_ceiling_order`; groups P6.

**7. The health check page depended on the last check. Fixed.** Once a full check has run, only a full check rewrites the plain part you read. A narrower check (one step, one scene, the film) replaces only the checker's lines for the AI. A check that checks nothing writes nothing and says so. The page now shows the quality scores in plain words: how many scenes pass, the average, the best scene, and why a scene fails. It also names the three scenes to read.
For maintainers: `check_records.write_health_check` (returns None when no check ran; keeps a plain part that starts "Checked: everything, on"; still runs `REPORT_SECTIONS`); `quality_scores_plain_lines`, `scenes_to_read_plain_lines`, `review_scores`, `scene_passes`, `RUBRIC_PLAIN_NAMES`; `in_short_line`; group P7.

**8. How close the camera goes at the turn. Fixed.** The film's plan of closest shots (the ladder) now decides. Where the ladder sets a size for a scene's turn, the checker compares the turn with the ladder, not with the character's closest size.
- Earlier shots may equal the ladder's size, never go closer.
- A deliberately wide turn keeps its closer build-up shots.
- The character's closest size applies only where the ladder is silent. It then skips a size the film has saved for other scenes.

On The Catch this warning went from 40 to 0.
For maintainers: CRAFT-03 in `checks_craft_reasons_words` (`ladder_rung_of`, `rung_size_problems`, `size_allowed_by_saved_choices` against RESERVE `match: size = ...` and `allowed_in`); steps/07, reference/06; group P8.

**9. Light and sound. Fixed.**
- Light words are now read in their sentence. "Grey" in "grey and tidy" hair, and "fire" in "the fire door", are no longer light.
- A light the scene's look already describes, at rest (the kitchen lamp on its hook), needs no extra light change. A light the story changes or moves still does: it dims, goes out, floods in, or is held up (corrected after note 33: the first version let "The lamp goes out." through).
- A light change that quotes the story's own light words counts as the story's light, not an added one. Quoting a line with no light in it excuses nothing (corrected after note 33).
- A silence the sound plan plans for that very moment, or the beat's own pause, is not an added change, and neither is "room sound only". A silence planned elsewhere in the scene excuses nothing (corrected after note 33).
- One light cue counts once, not as both light and colour.

On The Catch: light not covered went from 22 to 3, added changes from 2 to 0, too many changes at once from 3 to 0.
For maintainers: `derive_fields.light_words_in_context` (used by COVER-08 and `script_marked`); COVER-08 `look_light_words`, `light_word_carried_by_look`; `shot_light_sound_changes`, `silence_planned`, `rupture_planned`, `beat_signals` (CRAFT-10, CRAFT-19); groups P9.

**10. Timing. Fixed.** A scene's length is now measured against its own shot list, with one tolerance (10%), not against the first word-count guess. A scene given room to breathe after an intense one is no longer flagged for being longer. The time the list promises for each shot now includes the time to read words the shot quotes, and the pause after a turn. The pause is owed once, by the last shot of the beat. Reading time counts only for words the audience must read (plot-critical or emphasised). It is never counted for a blurred background sign, and it now also counts for plot-critical text on a visor or wrist in the shot. Two scenes (14 and 30) still warn. Their shots really do run longer than their lists planned: scene 30 holds one shot for 21 seconds where its list planned 10 (corrected after note 33: the first version blamed the old promise, but the new promise is lower than the lists). A scene whose list is more than twice, or under half, its first planned length is warned again (added after note 33).
For maintainers: TIME-03 against the SHOTLIST `time` total with `scene_total_tolerance` (0.1); `scene_duration_tolerance_share` removed from constants.json; `derive_fields.time_floor` (`texts_shown_by`, `text_must_be_read`, `last_shot_naming_beat`), `provisional_floor` (`ListItemStandIn`, quoted text); rubric and step 10 wording; groups P10.

**11. Hiding a secret. Fixed.** A shot that says how it keeps a fact hidden (at the frame's edge, in the dark, out of focus, and so on) is no longer warned, and what is really on screen stays listed. Naming an idea such as "labels" no longer sets off a warning about every labelled object. On The Catch this warning went from 2 to 0.
For maintainers: INFO-01 in `checks_craft_reasons_words` skips a shot whose `keep_hidden` names the fact; a MOTIF in the shot no longer expands to its carriers (only `prop_motif(run, other) == element`); group P11.

**12. Things with no state yet. Fixed.** When continuity missed an early appearance, the shot step may now add the missing state as a marked addition, and the checker's advice says how. A recording of an earlier time can say which scene it shows ("recorded: scene 6"), and the checker then reads the state there.
For maintainers: STATE-01 `recorded_position` and its fix text; SHOT `thing` and `subject` sub-part `recorded` in schema.json; U-08 writes a STATE addition and SCENE additions (steps.json); steps/08 item 5; group P12.

**13. Wrong words flagged. Fixed.**
- "Movement" is flagged only as a camera movement, and "bed" only as a sound bed.
- "Her look" is not flagged at all, and "withhold" is allowed in the fields that describe a character's tactic.
- "As before" inside a sentence is ordinary English. It still counts as a shortening when it stands alone, opens a value, or points back ("the same framing as before") (the last case added after note 33).
- A place's "bullet scars" is not a body scar.
- "Left palm" is no longer matched to the other, dressed palm.
- A close shot of a boot no longer counts as showing the ring on the same person. A close shot that lists the ring among what it shows is still protected, whatever its words say (corrected after note 33).
- A black screen in the middle of a scene keeps its number. Only one at the end must be renumbered, and one such warning is left (scene 30).
For maintainers: words.json `pattern` for movement and bed, "her look" `flag: context`, withhold `exempt_field_names`; `checks_form.MARKERS_ALSO_ENGLISH`; SIDE-01 skips LOC states; SIDE-04 `clause_names_this_one`; SIDE-03 `insert_words_name`; ID-03 end-of-scene only; groups P13.

**14. The video-prompt check. Fixed in the code; some problems remain in The Catch's records.**
- The project's word swaps (a cage becomes an open steel freight elevator car) are now made everywhere a prompt is built, including the pasted place and look descriptions, and only once. Banned words went from 54 to 0.
- "THE END" is no longer flagged on shots that show no text, because words in capitals are matched as printed.
- A sound description is no longer read as describing the place again: 29 down to 1.
- Quoted story lines no longer count as reasons leaking into the prompt.
- A single large letter the shot is about, like the F on the toy carriage, can now be marked to be drawn by the video model. Only one short mark: a whole sign marked this way is still refused (added after note 33).

What is left in The Catch: the carriage's F still needs that mark (10 prompts), which only the kit's normal steps can write. The other leftovers are real problems in the records:
- 13 prompts still ask for signs "reading" words;
- 8 prompts name words shown on a display or sign (STOP, TURN, UPWARD SPEED and others) (added after note 33);
- 5 prompts negate something visible ("no warmth");
- 3 prompts are too long for the chosen model.
For maintainers: `derive_fields.project_prompt_swaps`, `swap_prompt_words`, `swap_sources_banned`; `compile_prompts.WordFixer`; GEN-04 accepts the swapped form; GEN-05 `prompt_without_sounds`; GEN-06 skips `method: model_drawn` for one short mark only (`is_single_mark`) and finds capitals written with a capital on every word (`words_asked_for`, after note 33); GEN-15 strips `QUOTED_WORDS`; TEXT `method` value `model_drawn`; groups P14.

**15. Rules that lived only in the code. Fixed.** Step 8 now says:
- one main action per started 4 seconds;
- the sum that turns lens and distance into shot size;
- that a camera never stands inside an object, and where it may stand beyond a missing wall;
- which fields show the beat's key moment;
- that a speech's words are on the lines after the speaker's name.

Step 7 says setups are placed by the same sum. The shot handout now lists each speech with its number, cue line and word lines. It gives the lenses in force for the scene, after the film rules' change from scene 11 (40, 75 and 100 mm).
For maintainers: steps/07 and 08; `make_handout.speech_lines`, `lens_family_in_force`, `batch_section`; schema SHOT `kind` meaning; group "P15, P17, P18".

**16. A wrong field could not be removed. Fixed.** Writing "none" on a field where "none" is not a value now clears the stored field, and the apply message says so. It never clears a field of a record the user approved and locked: that is refused, like any other change to a locked record (corrected after note 33: the first version let it through). A place without a floor plan can now say where the camera looks, in words. Notes sent on a record that already exists are kept (they used to be dropped). After an apply, the message names the next command as the handout does (build first at the scene steps).
For maintainers: `project_files.take_out_clearing_lines`, `none_allowed`, `put(keep_notes=...)`, `next_after_apply`; SETUP `look_at_words` (one_of with `look_at`); group P16.

**17. No record for the animal. Fixed.** A creature that acts in beats but never speaks and is not human is now a character of its own kind. Step 4 says so, and the things unit writes it when no other unit does. It is not held to a person's timing in suspense scenes, but only while it has no voice and no lines: marking a speaking character "not human" changes nothing (added after note 33).
For maintainers: CHARACTER `tier: non_human` (already in the schema) now in steps/04 and steps.json U-04-THINGS writes; TIME-09 `is_non_human`; group P17.

**18. The last steps were thin. Fixed.**
- Step 10 now says where your final answers go (one file, "acceptance.md", in the inbox).
- It says the film's own review answers are the four film-pass questions.
- It says one finding may be cited by several scores.
- A top score that can't be reached at this depth is scored 2, with the reason given.
- The estimate runs before the full check.
- Step 11 says the export checks its own file formats.
- There is now one film length everywhere: the story's, then the same "with titles and credits".
For maintainers: steps/10 and 11, reference/05; `estimate.in_short`; `make_views.titles_seconds`; groups "P15, P17, P18" and P18.

## The rule for switching the file format

The blueprint's switching rule now counts only real layout mistakes: the kinds that a stricter format (JSON) would prevent. Those are:
- a heading or ID the tools can't read;
- a field line in no known form;
- a missing or miscounted END line;
- a shortened record;
- a field given two values.

Missing fields and refused values no longer count, because JSON would not prevent them. The run's format errors were almost all of those two kinds. By the new rule the readable format stays.
For maintainers: "Project notes/13 Blueprint - how Stage is built.md" line 28 and section 14.3 (FORM-01, 02, 03, 06, 07, 08, 09 and 12 count; FORM-04, 05, 10 and 11 do not).

## Smaller items

**Fixed:**
- The book no longer prints kit names; the additions are labelled "changes the scene; keep or cut it" or "a small addition, kept".
- The book no longer adds "it cannot be shorter than 0.5 seconds" to every shot.
- The ladder's longest hold reads "held past the longest pause" in the book, not "held hold" (after note 33; the first version called this a fault in the record).
- The export now checks the book for codes.
- Shortened quotations in messages end at whole words ("she climbs on past the [shortened] will turn").
- "Status" says "0 of 9" instead of "None of 9". It lists a refused repair left in the inbox apart, as safe to remove, and says it writes nothing.
- The suspense warning gives one line per character, with the facts together, instead of one line per fact.
- The alias search finds "the figure" only as a name, not in "a small figure", and names are no longer printed twice.
- A scene heading is matched to the place whose own words fit best: "passage" outweighs "room", which many places share.
- A choice that sets a film rule not written yet is kept waiting, and is no longer an error.
- A quotation of a speech broken by a stage direction in brackets is accepted.
- A set-plan object that first appears in a later scene (the tent) no longer blocks cameras in earlier scenes.
- The message about the size a lens gives now reads "an extreme wide" and says where the sum is written.
- The check of a scene's last batch now includes the scene-wide checks.
- The beat's unsaid thing may be seen in where a thing stands, or in the shot's end.
- The audio description no longer says "no behaviour written" for a shot with no people.
- The step 7 example order of units matches what the kit really hands out.
- The shot kinds are explained.
- The rubric's film score takes the lower of the scenes' score and the film pass.

**Not fixed** (noted, left for later; none blocks a breakdown):
- The plain part of the choices file can contradict itself right after reading.
- A finding stays open after its problem goes away.
- The whole-film summary says it leaves out record types it has room for.
- The self-test handout does not print the allowed values.
- The start handout's "you write" list is wrong.
- Several template gaps: how to write a rule's or fact's element before it exists, where the frames of a time slice go, inserting a state between two others.
- "What's next" still builds the next handout as a side effect; "status" is the command that only looks.
- A place with no states can't be named as a thing, and the refusal doesn't say why.

## Warnings left on The Catch, and why

After the fixes, the full check gives 29 warnings and no errors:
- **Suspense held too short (6), in scenes 6, 20 and 23.** Real craft points: the character who does not know yet is cut shorter than the talk around them.
- **Rhymes that change their framing (3).** Real: a payoff is framed differently from its plant, at a different lens or size.
- **The size the lens gives (5).** Real: in scenes 3, 9 and 23 the camera's distance and lens give a wider frame than the size written. The setups were placed before the sum was written down.
- **Light not covered (3), in scenes 20, 23 and 26.** Real: "three green lights" on a wrist, "the pale strip dims" and "her lamplight" are light changes the story writes, with no light cue.
- **Scene length against its list (2), scenes 14 and 30.** Real: the shots hold longer than the lists planned, including scene 30's 21-second hold. The lists were never updated for it (corrected after note 33).
- **Talk with no line heard off screen (2), a silent third person missing from a turn (2), too many people acting in one shot (1), a turn held neither longest nor shortest (1), a scene that does not breathe after an intense one (1).** Real craft points.
- **A lens outside the film's family (2), scene 21.** Left over: the chest camera's own picture at 18 mm was written as seen by eye rather than as the camera's picture. The shot kinds are now explained, so a new run would write it as the camera's picture.
- **A black numbered below 990 (1), scene 30.** Real: that black comes at the end of the scene, so it takes the end numbers. A redo of that scene's list would renumber it.

None of these can be cleared by code without changing the records, and the records are changed only through the kit's normal steps (hand out, write, apply, check). These are the fix pass's numbers; the repairs after note 33 change a few of them, and note 33's last section gives the final count.

## Tests

- New: `tests/fix02_full_run_acceptance.py`, 32 groups, one or more for each fix. It uses only small fixtures: copies of the scene 10 example, the scene 10 excerpt, the small reader screenplay, and short texts. The same file run on the code from before the fixes fails all 32 groups, but 14 of those only because a name it imports did not exist yet, and three fixes could be undone without any group noticing (corrected after note 33). Groups for the repairs after note 33 were added; note 33's last section lists them.
- The full suite, `python tests/run_tests.py --story-catch "My stories/The Catch.txt"`: every test passes except the chat-kit size check. That one was already failing. Files 02, 04 and 05 were trimmed back to no longer than they were: 20,110, 17,835 and 3,172 words, against 20,111, 17,840 and 3,174 before.
- Older tests changed because a rule changed on purpose:
  - `wp5`: passing a checkpoint when none waits now carries on; the example is left out of scene 10's own handouts; records go in brief before card parts; the split advice wording.
  - `fix01`: the one scene-length tolerance.
  - `wp4b`: a film check keeps the full check's plain part.
  - `wp7`: one film length.
  - The fault fixture for hiding a secret (the fault also removes the "keep hidden" line). The light fault was also changed at first, which note 33 showed hid a real fault; it is back as it was (corrected after note 33).
  - The expected grammar results: whole-word shortening, and the new "recorded" sub-part.

## What was not tested, and what is uncertain

**Not tested:**
- A fresh run of The Catch with the fixed kit. The Catch was only re-checked, so the records written under the old rules stay as they were. The warnings a new run would give are not known.
- The chat-app route (ChatGPT, Gemini) and The Long Places.
- Whether a helper reading the new step text writes a missing state, a recording's scene or a model-drawn letter correctly.
- Grey previews, pictures and video.

**Uncertain:**
- Handouts for the biggest scenes still need two reads and still lose a few card parts; whether that hurts the shots is not known.
- A light the look describes, at rest, is taken as covered. A line that moves or changes it is caught by its words (goes, out, dies, floods, holds, brings up and about 60 more). A change written in other words would slip through.
- The chat-kit files are still 26% to 49% over their targets; that is older than this pass.
