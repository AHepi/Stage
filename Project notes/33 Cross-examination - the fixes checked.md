# 33 Cross-examination - the fixes checked

Log entry 33. A fresh Opus 5.5 helper, which had not seen the fixes being made, tried to prove the fix pass (Project notes 32) wrong. Its report follows as it wrote it. The last section, added afterwards, says what was done about each finding.

A second look at the 18 fixes in the working folder (Project notes 32), done by someone who did not make them. The rule was to try to break each claim before believing it.

## In short, in plain words

**One example first.** In scene 1 of The Catch, the story says "Her light goes onto each rung before her hand does." Before the fixes, the checker asked for a light change there: the torch beam moves ahead of her hand. After the fixes it says nothing, because the scene's look has a main light, and any line that says "light", "bright", "dim" or "glow" now counts as already covered. The same thing happens if the story says "The lamp goes out." That is the pattern behind most of what I found. Some fixes do more than stop false alarms: they also stop the checker from seeing real faults.

**What holds.**
- Every test passes except the chat-kit size check. That check was already failing.
- The re-check numbers are the same as the helper's: no errors, 29 warnings, 40 prompt problems, and "Finished".
- The chat kit and the skill file were really rebuilt. A fresh build gives the same files.
- Starting a new project from The Catch still works.
- The Catch's own records were not touched.

**What is wrong, most serious first.**
1. **Locked choices can now be wiped.** Writing "none" on a field now clears it, even on a record the user approved and locked. I cleared two fields of the film's approved camera rules this way, and the kit said "Applied". Before the fixes, it refused.
2. **"Finished" can be said with no spreadsheets, captions or timeline.** The kit now decides the last step is done if the book is up to date. But step 10 already makes the book. In a clean run where nothing changes after that, the last step is skipped. I deleted the exports and made the book again, and "what's next" said "Finished: the book and the exports are made."
3. **The light check now misses real light changes**, as in the example above. On The Catch, three real light moments in scenes 1 and 6 lost their warnings.
4. **A way round two other checks.** A light change counts as "the story's own" as long as it quotes any line of its beat, even one that has nothing to do with light. A red strobe flash that quotes "Jude on the table." is no longer flagged. And a silence planned anywhere in a scene now excuses every silence in that scene.
5. **The ring check can be missed.** A close shot of Saye's ring hand no longer has to stay unflipped unless its words say "ring". That ring's side is the whole point of scene 10.
6. **Smaller things:**
   - Anyone can be marked "not human" to escape the suspense timing check, and nothing notices.
   - A scene can run three times its planned length without any warning.
   - The new test does not catch three of the fixes if they are undone.
   - Several instruction pages and cards still say the old rules.
   - Some sentences in note 32 are wrong: the reason given for the scene 14 and 30 warnings, the list of prompt problems left over, and "held hold" being a record fault.

**What I would do before this is committed:** fix items 1 to 5, add tests that would catch them, and correct note 32.

## How this was done

- I read notes 31 and 32, the whole diff (62 files) and the two new files. I also read parts of the raw notes from the run.
- I compared old and new code on the same faulty inputs. The old code was taken read-only from the last commit, with `git archive`. Each experiment ran on copies of the gold scene 10 (the kit's worked example) with the scene 10 excerpt of the story.
- I ran the whole test suite. I undid five fixes, one at a time, in copies of the repository, and ran the tests again.
- I re-checked "My breakdowns/The Catch" and ran the new code on a copy of the backup made before the fixes.
- I started a fresh project from The Catch in a scratch folder. It was never in "My breakdowns".
- I rebuilt the kit in a copy of the repository.
- No file in the repository was changed. The kit's own commands rewrote only code-made files in "My breakdowns/The Catch": the film check, the health check, the log and the manifest.

## Findings, in detail

### X01 (major, certain). "- field: none" bypasses the lock on approved records (problem 16)

`project_files.take_out_clearing_lines` takes the "none" lines out of the inbox before the inbox checks run, so FORM-11 (changes a locked record) never sees them. `put()` then removes the stored field.

- Gold project (every record `locked: yes`), inbox `U-06-CAMERA - fix 1.md` with `### CAMSYS` / `- normal_lens_mm: none` / `- camera_speed: none`:
  - new code: `exit 0`, "Cleared normal_lens_mm of CAMSYS. Cleared camera_speed of CAMSYS. Applied ..."; the stored CAMSYS has neither field and still says `locked: yes`;
  - old code: `exit 1`, "E FORM-11 CAMSYS normal_lens_mm changes a locked record (it was "50")", "Not applied".
- The same with `- plot_event: none` on the locked PLANT PL-07: cleared. A later `check --all` reports no lock problem, only a knock-on CRAFT-08 warning. For required fields it reports only "missing" (FORM-05).
- `- move: none` on the locked shot 150: cleared (the old code refused it with FORM-04 and FORM-11).
- The fix02 group P16 only clears a field of an unlocked CAMSYS in a fresh project.

Fix: run the lock check (FORM-11 against `locked records.json`) on clearing lines before taking them out. Refuse to clear a field of a locked record, the same way a changed value is refused. Add a test on a locked record.

### X02 (major, certain mechanism; likely in a clean run). "Finished" without the exports (problem 2)

`evidence_of` treats the step 11 unit (`export all`) as done when `file_is_fresh(BOOK_FILE)` is true. Since the fix, that means the book was made from the records as they are now. But step 10's own code unit runs `export book` first. The review answers and scores go to 13 Health check and 12 Whole-film check, which `records_signature` leaves out. So if nothing in a counted file changes after step 10, the book stays "fresh" and `export all` is never run.

- In a copy of The Catch, I deleted "16 Spreadsheets", "17 Captions and audio description", timeline.edl, timeline.otio and breakdown.json, then ran `export book` (as step 10 does) and `next --no-handout`:
  - new code: "Finished: the breakdown is done, the book and the exports are made." No export exists.
  - old code: "Next: step 10 of 12, the film pass ..." (the old bug from problem 2).
- The Catch run escaped this only because step 10 wrote choices and shot repairs into counted files. A clean run where the user answers "no changes" and no choice is open would not.

Fix: judge `export all` done only when its own outputs exist and were made from the current records. For example, `remember_made_from` for the shot list or `breakdown.json` in `run_export` when kind is all. Or record the step 11 run in the manifest. Add a test that goes from step 10's `export book` to `next`.

### X03 (major, certain). COVER-08 now passes real light changes (problem 9)

`light_word_carried_by_look` counts any brightness word ("light", "lit", "bright", "dim", "pale", "glow", "beam", "shine" and so on) as covered by any LOOK with a main light. Any named source ("lamp") counts as covered when the look names it. Only eight "change" words (dims, flicker(s), flash(es), flare, blaze, strobe, lightning, blinding) still need a cue.

Gold scene 10, with the look's cue at "Iona holds the lamp." removed and one sentence added to line 406 of the excerpt:

| Story line 406 | Old code | New code |
|---|---|---|
| "Iona holds the lamp." (the gold's own cue removed) | W COVER-08 (lamp) | nothing |
| "... The lamp goes out." | W COVER-08 (lamp) | nothing |
| "... The light dies." | W COVER-08 (lamp, light) | nothing |
| "... The kitchen goes dim." | W COVER-08 (dim, lamp) | nothing |
| "... Bright light floods the kitchen." | W COVER-08 (bright, lamp, light) | nothing |

- On The Catch, 19 warnings went away. Most were right to go (bright bolt holes, the fire door, a torch as an object). But these were real: line 73 "Her light goes onto each rung before her hand does.", line 83 "She brings the light up: one bracket sheared clean through." and line 212 "Light, brick, light, brick."
- The gold itself models "Iona holds the lamp." as needing a light cue ("the light moves when she moves"). The new rule says it does not.
- The wp4c fixture was changed by adding "It flickers." to the story, so its fault still fires (see weakened tests).
- Problem 9 asked that a quoted light cue satisfy both checks. It did not ask for a look's main light to cover every brightness word.

Fix: let the look cover only static description, the same source with no verb of change. Treat verbs of change or movement (goes out, dies, fades, sweeps, swings, comes on, brightens, "into the light") as needing a cue. Keep the gold's lamp cue as a test fault.

### X04 (major, certain). CRAFT-10 and CRAFT-19: any quote, and any planned silence in the scene, excuses an added change (problem 9)

- `reason_quotes_lines` is true when the value quotes *any* words of the beat's lines. So `shot_light_sound_changes` drops any light change that quotes any line. Gold, shot 030 (beat 2, which the script marks):
  - `- light: a hard red flash strobes across the table` gives W CRAFT-10 (new and old);
  - `- light: a hard red flash strobes across the table, as the story writes "Jude on the table."` gives **nothing** (new). The old code flagged it.
- The full run's helpers already found this trick by reading the code (all_findings line 259: "Only a light_cue whose why quotes the beat's lines satisfies both (read from CRAFT-10's code)"). The fix makes it general.
- `silence_planned` matches the word "silence" in any `rupture_plan` of the scene. I added `rupture_plan: SC10 | device: true silence under the title card`, and then a `silence: true_silence` added on beat 2 was no longer flagged. It was flagged without that line, and the old code flagged it either way.
- `rupture_planned(run, scene)` (read in code): if a scene has any rupture plan, every dial sound change in that scene stops counting, in both CRAFT-10 and CRAFT-19.

Fix: accept only a quote of a line the reader marked as light, whose light word is in the quote. Match a planned silence to the beat or shot the rupture names, not to the scene.

### X05 (major, certain). SIDE-03 no longer protects a ring insert whose words do not say "ring" (problem 13)

`insert_words_name` now has to find the feature's noun in the insert's purpose, end, moments, does or thing positions.

- Gold shot 090: I kept `must_show: MO-RINGS`, `thing: MO-RINGS` and Saye's state with the ring. I reworded purpose, does, moment and end without the word "ring", and set `flip: auto`. Old: "E SIDE-03 SC10-SH090 flip is auto on an insert of a sided detail (Saye's wedding ring)". New: nothing.
- A flipped insert puts the ring on the wrong hand, which is scene 10's plot point.
- Undoing this fix in a copy of the repository passes fix02 and the whole suite.

Fix: also count the shot's thing and must_show items: a motif or prop that carries the feature, such as MO-RINGS for the ring.

### X06 (minor, certain). TIME-09 "non-human" is an unguarded way out (problem 17)

- I set `tier: non_human` on Jude, a speaking principal with a voice, and ran every check on the gold. There were 0 new problems and 0 gone. Nothing ties `non_human` to `voice: none` or to no speeches.
- Undoing the TIME-09 skip (`or is_non_human(...)`) passes fix02 and the whole suite (only wp13's kit-freshness and size groups fail, as they must after any code change).

Fix: make it an error (FORM or ID) when a `non_human` character has a VOICE, speeches, or a voice other than none. Test TIME-09 itself, not only `is_non_human`.

### X07 (minor, certain). fix02 does not prove several fixes

- Undoing fixes in copies of the repository:
  - TIME-09's non-human skip: fix02 PASS (32 of 32), whole suite no new failure;
  - SIDE-03's insert-words gate: fix02 PASS, whole suite no new failure;
  - GEN-06 reading `kind` instead of `method` for model_drawn (the source text asserted by fix02 kept): fix02 PASS, whole suite no new failure;
  - CRAFT-10's silence rules: caught (P9);
  - COVER-08's look rule: caught (P9).
- "The same file run on the code from before the fixes fails all 32 groups": true, but 14 of the 32 fail only with ImportError or AttributeError, because the new helper names do not exist yet. That proves nothing about behaviour.
- P14 checks GEN-06 and GEN-15 by searching the source text (`'== "model_drawn"' in source`), not by running them.
- No group runs `next` to "Finished", or runs step 10 into step 11 (X02).
- No group clears a field of a locked record (X01).

### X08 (minor, certain). No check compares a scene with its planned length any more (problem 10)

- Gold: `target_duration_s: 110` changed to 40, with the shots at 112.5 s. Old: "W TIME-03 SC10 ... 181% over its target". New: no check says anything.
- TIME-03 now compares only the shots with the one-line list, and nothing compares the list with the target.
- This matches problem 10's wording, but note 32 does not list it as a risk. A step 7 design that triples a scene's length is no longer seen until the film total.

### X09 (minor, certain). GEN-06: "model_drawn" is not held to one mark, and capitals are matched too strictly (problem 14)

- A TEXT "NO ENTRY BEYOND THIS POINT" with `method: model_drawn` and the prompt "A steel door, NO ENTRY BEYOND THIS POINT painted across it in red." gives nothing (new). The old code gave "E GEN-06 ... asks the model to draw the words". The schema says model_drawn is "only a single large letter or mark", but no code enforces it.
- TEXT "THE CATCH" with the prompt "The words The Catch in white letters." gives nothing (new). The old code gave E GEN-06.

Fix: allow model_drawn only for one character or one short mark. Match all-capital words case-blind when the prompt holds them as a whole phrase in title case.

### X10 (minor, certain). Note 32's explanation of the scene 14 and 30 length warnings is wrong

Note 32 says the list times were written "under the old, lower promise, which left out reading time and the pause after a turn". The new floors do not support that:

- SC14: list 7.0 + 2.5 = 9.5 s; new provisional floors 2.0 and 0.5; shots 7.5 and 5.5.
- SC30: list 44.5 s, floors 15.1 s, shots 55.5 s. The overrun is shot 080, 21 s against a list time of 10. That is the film's longest hold, moved there in a step 10 repair (FIND-005's reason).

These are real overruns that the list was never updated for, not leftovers of the old rule.

### X11 (minor, certain). Note 32's numbers and leftovers overstate or misstate

- "Unaware character held too short 33 → 6": the 33 old lines were 8 scene-and-character pairs, printed once per fact. Now they are grouped. Six pairs remain, and two (CH-FIGURE in scenes 20 and 23) were dropped by the non-human rule. The real problems went from 8 to 6.
- "Light not covered 22 → 3" includes the real light moments of X03.
- "The other leftovers are real problems in the records: 13 prompts still ask for signs reading words; 5 ...; 3 ...". The 31 GEN-06 lines are 10 for the carriage F, 13 for "reading", and **8 more not mentioned**: STOP, PASSAGE FLOOR (twice), CHARGE, TURN, HULL CLEARANCE, UPWARD SPEED and RECEIVING, drawn by the model.
- "The ladder's hold value 'hold' prints as 'held hold' in the book (scene 30); the fault is in the record, not the code." The schema lists `hold` as a value of the rung's `hold` sub-part (short, medium, long, hold), so the book's wording code is at fault.
- "There is now one film length everywhere": "14 Time and cost.md" in My breakdowns/The Catch still says "the film runs about 43 minutes", because the estimate was not re-run. Re-run in a copy, it says "about 42 minutes of story, 43 minutes with titles and credits in about 514 shots", which reads badly.

### X12 (minor, certain). Words and rules that no longer agree

- reference/06 "Checks in words" (the chat route) still says FORM-08 flags "as before" anywhere (line 42). Its sample table still says "cards and black from 990" (line 21). Card 11 still says "Every light, colour and darkness word is binding", while the code now takes brightness words as covered by the look.
- Card 18, item 7, now offers only `stays_dark` or a quoting `light_cue`. The code still accepts a shot `light` too.
- `recorded` is in the schema for both `subject` and `thing`, and fix02 uses it on a subject. Step 8 mentions it only for things, and templates/11 Scene.md lists neither.
- Step 10, item 4 still places the estimate after the lint. The code, and a sentence added to item 2, run it before `check --all`.
- After `apply acceptance.md`, the message says "stage.py check --all, then stage.py next". Step 10 says "then run stage.py next --checkpoint-passed".
- SKILL.md says `status` "writes nothing", but it appends a line to `log.jsonl` (hash of log.jsonl changed after one `status`).

### X13 (minor, certain). The "as before" heuristic lets a real shortening through (problem 13)

A purpose of "the same framing, lens and light as before; ..." is no longer flagged (new), and was E FORM-08 (old). A value opening with "As before," is still flagged. The rule only looks at position and length: anything of six words or more with "as before" not at the start passes.

### X14 (minor, possible). CRAFT-03 loses the camera-rule cap when the ladder's rung names another beat (problem 8)

- Gold, rung moved to beat 2 (medium wide), and the main turn (shot 150) opened to medium. Old: "the main turn is at medium, but CR-IONA allows its subject up to close_up". New: that line is gone, because a rung for the scene sets `cap=None` even when it is not on the main turn.
- `size_allowed_by_saved_choices` reads `allowed_in` only as scene IDs. The gold's RC-02 says "main turns only; the first in scene 13", so it would not apply there. The Catch writes IDs, so it works on The Catch.

### X15 (minor, certain). INFO-01 now trusts keep_hidden completely, and the promised backstop does not exist (problem 11)

The skip is per fact and per shot. In the gold with a new fact about the flask, shot 020 hiding it was silenced, while shots 030 and 120 still warned. That part is right.

- A shot that lists the fact's element in `must_show` and also says `keep_hidden` is no longer warned. The old code warned (wp4d fault before its edit).
- The new code comment says "the review questions judge whether the hiding works". The question maker (`adopt_folder.QuestionMaker.shot_questions`) builds no question from `keep_hidden` or FACT, so nothing checks it.

### X16 (nit, certain). No file's plain header note was updated

All 17 changed code files keep their old header notes, including the new behaviour in project_files (made from.json, clearing with none), check_records (health check rule, quality scores) and make_handout (scene splits).

### X17 (nit, certain). User-facing wording

- In 13 Health check: "Scene 14, the shot list: runs longer or shorter than its own shot list planned." This reads as the list running over itself. "Scene 30, shot 090: has a shot number out of the usual steps of ten." But the problem is that an end black takes 990 to 999.
- Note 32 is meant for the user, but its plain parts use "the step loop", "units", "handouts", "records", "code_state" words and "the judging step's part units ... so their handouts are accepted". Its claim "A helper who follows the instructions can now finish a scene without warnings it cannot clear" was not tested: no fresh run was done, and note 32 says so later.
- ID-03 now also lets a title card at the start of a scene keep a low number. Problem 13 asked only about a black in the middle.

## Claims that held (tried to break, could not)

- The whole suite: `python tests/run_tests.py --story-catch "My stories/The Catch.txt"` gives 20 tests, 1 failing (wp13, chat-kit sizes 20,110 / 17,835 / 3,172 words), in 7.5 minutes. The repository was unchanged afterwards (file hashes compared).
- Re-check of The Catch with the new code:
  - `check --film`: 4 warnings.
  - `check --all`: 0 errors, 29 warnings, the same list by check as the helper's.
  - `compile --lint-only`: 40 errors (3 GEN-01, 1 GEN-05, 31 GEN-06, 5 GEN-07; GEN-12 from 54 to 0).
  - `next`: "Finished ...". `status`: "nothing: the breakdown is finished".
- The new code on a copy of the pre-fix backup: `check --film` rewrote FIND-005's fix to "reason: <why>', the why quoting the line where the story peaks.", and `check --all` gives 29 warnings and exit 0. The old code on the same backup gives 126 warnings and 1 error.
- The helper changed no record of The Catch. Records below the divider were compared with the backup: only FIND-005's code-written fix differs.
- Kit rebuilt: `build-kit` in a full copy gives byte-identical chat-kit files, AGENTS.md, field guide and example folder, and zip contents identical by entry.
- Start of the loop on a fresh project from The Catch (in a scratch folder): new, status, next, selftest --prepare, read, handouts U-00-START, U-01-ODDLINES, U-02-SC01..SC10, U-02-FILM, U-03-WORLD, check --step 1, check --unit, check --all and check --step 11 ("Not written ... because nothing was checked") all ran without a crash.
- Handout sizes (the kit's count; chars/4 agrees):

  | Handout | Tokens |
  |---|---|
  | U-10-SCORES | 24,520 (was 643,186 characters) |
  | U-08-SC06-B1 | 29,950 |
  | U-08-SC06-B2 | 29,947 |
  | U-08-SC23-B1 | 29,576 |
  | U-08-SC13-B1 | 28,761 |
  | U-08-SC26-B1 | 27,476 |
  | U-07-SC06 | 25,134 |
  | U-09-JUDGE | 27,538 |

  This is as note 32 says. Shot handouts are the same size as before: what changed is that 4 card parts are dropped instead of 9.
- INFO-01's skip applies only to the named fact in that shot.
- Apply accepts a STATE from a shot unit and a non-human CHARACTER from the things unit.
- The step 8 size sum and its thresholds match `size_ladder_thresholds`. "One per started 4 seconds" matches TIME-06.
- No `scene_duration_tolerance_share` is left in the skill, the chat kit, AGENTS.md or the reference pages. It survives only in the constant's history note, old project notes and The Catch's old code-made handouts.
- The health check's new "Quality scores" section is right. It names scene 15 among the best at 24, which note 31 missed.
- Privacy: the diff and the new files hold no email address, local path or whole story.
- Speed: `check --all` takes 21.3 to 22.0 s with the old code and 24.5 to 25.8 s with the new one, about 15% slower. That is acceptable.

## What was done about each finding (added after the review)

I repaired every finding myself, without new helpers. Each repair has a test that fails if the repair is undone.

**The five serious ones:**
- **X01, locked records.** "- field: none" on a record the user approved and locked is now refused, like any other change to a locked record. The reviewer's own case (clearing two fields of the approved camera rules) now stops with an error, and both fields stay.
- **X02, "Finished" too early.** The last step now counts as done only when "export all" itself ran, with its format checks passed, on the records as they are now. A book made alone does not count. Tested both ways: after the book alone, "what's next" says step 12; after export all, it says "Finished".
- **X03, the light check.** The scene's look now covers only light at rest (the lamp on its hook). A sentence where the light changes or moves still needs a light cue: it goes out, dies, floods in, is held up, carried or brought up, or repeats ("Light, brick, light, brick."). A light that something moves into ("comes into the light") and a bright surface ("the bright steel") count as light at rest. All five of the reviewer's light cases are caught again, and the original test fault (the lamp's cue taken away) is back as it was.
- **X04, the light and sound excuses.** A quote now excuses an added light change only if the quote itself holds a light word from the beat's lines, and the same for sound. A silence planned by the sound plan excuses only the moment the plan points at (it names the beat or shot, quotes its line, or names the black or card that the shot is). The reviewer's red flash quoting "Jude on the table." and the silence planned elsewhere in the scene are both warned again. A real excuse (a light that quotes "Iona holds the lamp.") still works.
- **X05, the ring close-up.** A close shot whose must-show list or things carry the ring is protected from flipping, whatever its words say. The reviewer's case is an error again.

**The smaller ones:**
- **X06:** a character counts as non-human only when it has no voice and no lines. Marking Jude "not human" changes nothing.
- **X07:** the test file now has 42 groups. New groups test each repair on data, not by searching the code. Two gaps remain: no small test case makes the suspense timing check fire, so its "non-human" skip is tested only through the rule that decides who is non-human; and the prompt check that leaves quoted script out is still tested only through the full prompt check.
- **X08:** a scene whose shot list is more than twice, or under half, its first planned length is warned again (the new number `scene_target_far_ratio`, 2). The reviewer's case (a scene planned at 40 seconds and designed at 112) is caught.
- **X09:** the "drawn by the video model" mark is allowed only for one short mark, such as a single letter. Words in capitals are found when a prompt writes them with a capital on every word ("The Catch"), but still not inside ordinary prose ("the end of the corridor").
- **X10 and X11:** note 32 is corrected: scenes 14 and 30 really run long; the suspense numbers; the prompt problems left over; "held hold" was the book's fault and now reads "held past the longest pause".
- **X12:** the reference page used in chat apps, cards 11, 14 and 18, the scene template, step 8, step 10 and the main instructions now say what the code does. Step 10's order is the same in the step file and in the kit's list of commands: book, estimate, full check, prompt check, questions. After the final answers are applied, the message names the same commands as step 10.
- **X13:** "as before" is a shortening again when its sentence points back ("the same framing, lens and light as before").
- **X14:** when the ladder's rung sits on another beat, the camera rule still applies to the turn, and the warning says where the rung is, so the fix can be to move the rung. Reading "scene 13" in words was not done: that field is free text ("the first in scene 13", "not in scenes 26 and 27"), and reading it as a list could turn its meaning round. The field's meaning now says the checker reads only scene IDs there.
- **X15:** every shot that says it keeps a secret now gets a review question: does the picture really keep it hidden?
- **X16:** the plain note at the top of each of the 18 changed code files now says what changed.
- **X17:** two health-check lines are reworded ("is longer or shorter than planned"; "has a shot number outside the usual pattern: tens for shots, 990 to 999 for an end card or black screen"). A card at the very start of a scene is still not asked to take 990 to 999, because those numbers sort last; the reference page now says "end cards and black from 990".

**Two false alarms of my own, found on The Catch and fixed:** my first light repair flagged "turns the tag to the light", "drags across the bright steel" and "comes into the light", and "a fire shutter" was read as light. All four are now read as light at rest or no light, with tests.

## The final numbers on The Catch

| What | Before the fixes | After the fix pass | After the review's repairs |
|---|---|---|---|
| Full check: errors | 1 | 0 | 0 |
| Full check: warnings | 126 | 29 | 37 |
| Light the story writes, not covered | 22 | 3 | 8 |
| Video-prompt problems | 133 | 40 | 40 |
| "What's next" at the end | back to the film pass | "Finished" | "Finished", only after every export |
| Tests | 19 files, 1 failing | 20 files, 1 failing | 20 files, 1 failing (the same old chat-kit size check) |

The warnings went up from 29 because the repaired checks catch real faults again. Of the 37: 8 are light moments the story writes with no light cue, such as "Her light goes onto each rung before her hand does." and "She brings the light up"; 2 say that the ladder's rung for scenes 5 and 9 sits on a different beat from the scene's turn; 1 is a light cue in scene 27 that does not quote the story's own "BLACK.". The other 26 are the ones note 32 lists. None can be cleared by code: the records change only through the kit's normal steps.

**Not tested:** a new scene written with the repaired kit; the chat apps; The Long Places; pictures and video. **Unsure:** the light rule reads words, so a change written in words it does not know would slip through.
