# Test 01: The Catch, "Break down my story." (Claude Code, Standard depth)

Tester: Claude Code, working in /home/user/Stage, using only the kit (SKILL.md, steps, cards, reference, templates, examples, schema, rules, tools/stage.py). No /tmp blueprint and no tests/ folder were opened. No kit file was edited. The user's answers were: "defaults" at every checkpoint, "next" at the group of shots.

## 1. What finished

- **Steps 0 to 6 (the user's steps 1 to 7), whole film:** all done.
  - Step 0: project, self-test and rights. The answer was "It's mine".
  - Step 1: reading. 30 scenes, 221 speeches, first estimate about 35 minutes (32 to 38).
  - Step 2: story plan. PLAN, 10 SEQUENCE, 16 PLANT, 5 FACT, and a climax choice.
  - Step 3: world and style. STYLE, WORLD, 7 RULE and 6 choices.
  - Step 4 records:
    - 9 CHARACTER and 5 VOICE
    - 22 LOCATION, 14 of them with set plans
    - 41 PROP, 21 TEXT, 8 MOTIF and 4 CAMERA
  - Step 5: 89 STATE and a sides choice. Checkpoint B was answered "defaults".
  - Step 6 records:
    - CAMSYS, 4 CAMRULE, 3 RESERVE and 2 LENS
    - 25 LOOK and 10 VISUAL
    - SOUNDPLAN and a LADDER of 30 rungs
- **Steps 7 and 8 (the user's steps 8 and 9), three scenes only:**
  - Scene 2, the freight shaft: 9 beats, 14 shots, about 64 s.
  - Scene 9, the car: 8 beats, 12 shots, about 54 s.
  - Scene 15, Jude's room on the tablet: 5 beats, 4 shots and 3 cuts, about 37 s.
- **Scene numbering note:** in the kit's numbering, Jude's room on the tablet is **scene 15**. The test brief says "scene 16", but scene 16 is Iona's room (continuous). I followed the description and used scene 15.
- **Were other scenes forced first?** Without a scope, `stage.py next` offered U-07-SC01 first. The unit order goes sequence by sequence:
  - SQ01 = scenes 1 to 3, so it forces scenes 1 and 3 around scene 2.
  - SQ03 = scenes 7 to 10, so it forces 7 and 8 before 9.
  - SQ05 = scenes 14 to 16, so it forces 14 before 15.

  I used the kit's own PROJECT.scope field, set through a new asked choice (CHOICE-041, "the user said so at the length question") after step 6. `next` then went straight to U-07-SC02 → U-08-SC02 → U-07-SC09 → U-08-SC09 → U-07-SC15 → U-08-SC15. No other scene was listed. The kit gives a screenplay user no documented route to do this (scope is only described for prose).
- **Then:** I ran `check --all` (scope-limited) and `export book`, and read scene 9's book page. Steps 9 to 11 were not run (out of test scope).

## 2. Units done and time taken

- **Wall time:** about 63 minutes, from copying the story to `export book`.
- **AI units: 40.**
  - Step 0: U-00-SELFTEST and U-00-START.
  - Step 1: U-01-ODDLINES.
  - Step 2: 3 event units and U-02-FILM.
  - Step 3: U-03-WORLD.
  - Step 4: MOTIFS, CH-IONA, MINOR-P1, 12 PLACES units and THINGS.
  - Step 5: 6 continuity units.
  - Step 6: CAMERA, LOOKS and PLANS.
  - Step 7: 3 scene-design units.
  - Step 8: 4 shot batches.
- **Also run:** 3 blocking checkpoints (A, B, C) and 1 scope choice. Code commands were `new`, `selftest`, `read`, `estimate`, `build` (many times), `check` (every unit) and `export book`.
- **Repair rounds:** the maximum reached was 3, in one unit (U-06-PLANS). The ceiling of `repair_rounds_max` was otherwise never hit, because most remaining errors could not be fixed at all (see section 5).

## 3. Errors before repair, by unit and check family

"In-unit" means errors on records the unit wrote, or errors that stop its apply. Errors the step-level check printed for later units (floods) are counted separately. W = warnings, which do not block.

| Unit | Errors before repair (family: count) | Rounds | What remained |
|---|---|---|---|
| U-00-SELFTEST (20 test shots) | FORM 52 (FORM-05 39: eyeline sub-part 14, effect 12, thing 10, subject 3; FORM-04 13: invented PR-/LOC-/speech IDs in `because`) | 0 (the score deletes the records; no retry) | batch_size stays 12 |
| U-00-START | 0 | 0 | 0 |
| U-01-ODDLINES, checkpoint A | 0 | 0 | 0 |
| U-02-SC01..SC10 | 0 in-unit (flood: 253 = FORM-05 223, COVER-06 30, all for later units or code) | 0 | 0 |
| U-02-SC11..SC20 | 0 in-unit (flood 173) | 0 | 0 |
| U-02-SC21..SC30 | 0 in-unit (flood 93) | 0 | 0 |
| U-02-FILM | FORM 67 (FORM-05: SCENE.sequence 30 (my miss); target_duration_s 30 and PLAN budgets 3, both filled only by `stage.py estimate`; CHOICE date 1; PROJECT genre/tone_home/tone_range 3) | 2 | FORM 4 (deadlock) |
| U-03-WORLD | FORM 12 (FORM-07 1 from my END count; FORM-05 11), ID 5 (ID-02: choice sets SOUNDPLAN, which does not exist yet) | 2 | FORM 11 plus ID 5 (the SOUNDPLAN stub workaround broke `next`, so I reverted it) |
| U-04-MOTIFS | CITE 1 (CITE-03, case of "No persons.") | 1 | 0 |
| U-04-CH-IONA | 0 | 0 | 0 |
| U-04-MINOR-P1 (4 speakers and 4 non-speakers) | FORM 29 (FORM-05 on extras and the figure); round 1 added FORM 4 (FORM-04 `voice: none` refused) | 2 | FORM 4 (deadlock: voice for non-speakers) |
| U-04-PLACES-P1 | FORM 2 (FORM-05 headings); round 1 added FORM 2 (FORM-10 refused) | 1 | FORM 2 (deadlock) |
| U-04-PLACES-P2..P12 (11 units) | FORM 20 (FORM-05 headings, 1 or 2 each) | 0 | FORM 20 (deadlock) |
| U-04-THINGS (66 records) | FORM 13 (FORM-10 1 stopped the apply; then FORM-05 TEXT words 12) | 1 | FORM 12 (deadlock) |
| U-05-SC01..05 | FORM 6 (FORM-05 `side` missing) | 1 | 0 |
| U-05-SC06..10 | 0 | 0 | 0 |
| U-05-SC11..15 | SIDE 1 (SIDE-01, sling) | 1 | 0 |
| U-05-SC16..20 | SIDE 1 (SIDE-01, "no sling") | 1 | 0 |
| U-05-SC21..25, U-05-SC26..30 | 0 | 0 | 0 |
| Checkpoint B | 0 (music answer silently lost, see section 5) | 0 | |
| U-06-CAMERA | FORM 3 (FORM-04 RESERVE max_uses stopped the apply) | 1 | 0 |
| U-06-LOOKS (25 LOOK) | 0 | 0 | 0 |
| U-06-PLANS | FORM 2 (FORM-05 music_policy, clip_audio); W: WORDS 2 (WORDS-02 "her look") | 3 | FORM 1 (clip_audio deadlock) |
| U-07-SC02 | FORM 6 (FORM-05 emphasis 5, SHOTLIST approved 1), TIME 3 (TIME-05 1, TIME-08 2), GEOM 3 (GEOM-05). REASON 3 (REASON-03 on MOVE `why`) only showed at the step-8 check. W: CRAFT-10 2 | 2 (+1 at step 8) | approval, set at checkpoint C |
| Checkpoint C (scene 2) | 0 | 0 | |
| U-08-SC02-B1 (7 shots) | FORM 3 (FORM-04 stopped the apply: LOCATION ID in `because`), REASON 1 (REASON-02). W: TIME-06 3, GEOM-04 2, CRAFT-03 1, CRAFT-08 2, CRAFT-10 3, COVER-08 4 | 2 | 0 E, 7 W |
| U-08-SC02-B2 (7 shots) | STATE 1 (STATE-01), REASON 1 (REASON-01). W: GEOM-04 7, CRAFT-03, COVER-08 | 1 | 0 E |
| U-07-SC09 | GEOM 4 (GEOM-05: cameras outside the car and one inside a seat), FORM 1 (approval) | 1 | 0 |
| U-08-SC09-B1 (12 shots) | FORM 5 (FORM-04 stopped the apply: PROP/TEXT IDs in `because`), then CITE 2, REASON 1, TIME 1, STATE 5, SIDE 3 (SIDE-05), CRAFT 2 (CRAFT-14). Round 1: FORM-07 1 (my END count), TIME 1, CRAFT 1. W: TIME-10, GEOM-02, CRAFT-03 4, CRAFT-19, CRAFT-24 | 2 | 0 E, 6 W |
| U-07-SC15 | TIME 1 (TIME-05), FORM 1 (approval) | 1 | 0 |
| U-08-SC15-B1 (4 shots, 3 cuts) | REASON 2 (REASON-08 carriers). W: CRAFT-07 5, CRAFT-03 2, INFO-01 1 | 1 | 0 E |
| `check --all` | GEOM 1 (GEOM-05: my mark outside Jude's room) | 1 | 0 |

**Totals before repair, in-unit errors only.**
- FORM 222. About 130 of these are code-owned fields that no code writes. The self-test contributes 52.
- ID 5 · CITE 3 · COVER 0 (4 W) · TIME 5 · STATE 6 · SIDE 5 · GEOM 8 · CRAFT 2 (about 25 W) · REASON 8 · INFO 0 (1 W) · WORDS 0 (2 W) · PLAN 0 · GEN 0 (skipped) · FILM 0 (the film pass was not run).

## 4. Final check output

`stage.py check --all` (scope SC02, SC09, SC15), last lines:

```
Skipped TIME-07: the film's average shot length needs the whole film, and the project's scope is only part of it
Skipped PLAN-04: needs the whole film's scenes, and the project's scope is part of the film (not in the excerpt)
Skipped GEN-01 .. GEN-06: no compiled prompts yet
And 13 more skipped, listed in 13 Health check.md.
In short: nothing needs you, no small fixes needed, 29 warnings, 44 problems still to fix.
[exit 1]
```

**The 44 errors are all FORM-05**, on fields the AI may not write and code never writes:

| Records | Field | Errors |
|---|---|---|
| 22 LOCATION | `headings` | 22 |
| 12 TEXT with origin: story | `words` | 12 |
| CH-FIGURE, CH-GUARD, CH-NURSE, CH-TECHNICIAN | `voice` | 4 |
| PROJECT | `genre`, `tone_home`, `tone_range` | 3 |
| STYLE | `provisional`, `named_reference_policy` | 2 |
| SOUNDPLAN | `clip_audio` | 1 |

**The 29 warnings:**
- GEOM-04 7, suspected wrong distances in a vertical set plan
- CRAFT-03 7
- CRAFT-07 5, the in-story camera's lens
- COVER-08 4, CRAFT-08 3
- GEOM-02 1, CRAFT-19 1, INFO-01 1

`stage.py export book` ran with exit 0: "Written: 15 The breakdown/The breakdown.md", ".html", "Format checks passed: 30 shots, 30 timeline events, about 154 seconds of film."

**The book page for scene 9** reads well: At a glance, one line per shot, collapsible full shots in plain words ("it cannot be shorter than 4.68 seconds"), "Why it's shot this way", and the small choices. Defects on the page:
- **Speech lines are cut at the first full stop:** "We hear: Jude's line "Io."" (should be "Io. Your dashboard's on backwards."), "Eli's line "Saye."" and "Iona's line "Eli.""
- **Broken wording from codes:** "made from put together in the edit" (route composite_only), "does settles behind the wheel" and "the camera looks angled".
- **Duplicated names:** "Because of: … the flask, state 2 and the flask" (a state and a motif render the same). The additions read "The night bus number, the night bus number N29", because CRAFT-14 forced me to name the TEXT in the addition.
- **Missing cuts:** CUT records are not in the book at all. Scene 15's written jump cuts, the heart of its design, are invisible to the user.
- **Wrong count message:** export/build print "Worked out 30 shots in 30 scenes". The 30 shots are in 3 scenes.

## 5. Tool bugs

Each bug gives the command and its output.

1. **No CLAUDE.md is shipped, so the project lands outside the git-ignored folder.** `python .claude/skills/breaking-down-stories/tools/stage.py new "My stories/The Catch.txt"` printed `Made the project "The Catch" in "Stage/The Catch".` The folder was /home/user/Stage/The Catch, not My breakdowns/. `repository_root()` looks for CLAUDE.md. That folder is **not in .gitignore**, so the user's story (Original/The Catch.txt) could be committed, against the kit's own privacy rule. Workaround: re-ran with `--into "My breakdowns"`. After that every command needs `--project`, because `find_project` also needs CLAUDE.md to look in My breakdowns.
2. **`stage.py lib` does not exist.** SKILL.md and every card say "`stage.py lib B1 R14` prints one rule". Running `stage.py lib K03` printed `stage.py: error: argument <command>: invalid choice: 'lib' (choose from 'help', 'new', ... 'build-kit')`. `replay` is missing too.
3. **`next` silently skips steps 4, 5 and 6 and the blocking checkpoint B.** This happens as soon as any SOUNDPLAN record exists. I had written a one-line `### SOUNDPLAN` stub to satisfy ID-02 for the step-3 music choice. `stage.py next` then printed `Next: U-07-SC01, step 8 of 12`. The cause is in make_handout.py `evidence_of`/`mark_done`: U-06-PLANS counts as done when a SOUNDPLAN exists, and any later work marks all earlier step-0-to-6 units done. Workaround: deleted the project's "10 Film rules.md", which held only the stub.
4. **Code-owned fields are never written, so FORM-05 errors can never be cleared.** FORM-05 demands them, and FORM-10 refuses the AI's copy. Examples:
   - `apply` → `E FORM-10 CATCH genre is written by code (code_state); the AI may not change it.`
   - The same happens for PROJECT tone_home/tone_range, CHOICE date on open choices (cleared only once answered), STYLE provisional/named_reference_policy, SOUNDPLAN clip_audio, LOCATION headings ("written by code (story)") and TEXT words when origin is story.
   - For CHARACTER.voice on non-speakers, `voice: none` gives `E FORM-04 CH-FIGURE voice is none, which is not allowed here.`
   - Only adopt_folder.py copies the PROJECT fields; nothing does on a code surface.
5. **An answered choice whose target does not yet exist is lost silently.** At checkpoint B, `apply "Checkpoint B.md"` printed `choice 11: the record it sets, SOUNDPLAN, does not exist yet.` and then `choice 11 is now defaulted; what it sets was written.` music_policy was never written. Re-sending `answer: a` later did nothing ("0 new and 1 changed" with no effect).
6. **`apply` lets the AI write a `user` field directly.** Writing `- music_policy: none` on SOUNDPLAN was accepted. FORM-10 only guards code-owned fields, not user fields.
7. **`check --step 2` cannot be scoped to a unit.** After the first event unit it printed 253 errors, all for later units or for code.
8. **Some code-owned fields are only filled by `estimate`.** target_duration_s, runtime_estimate, scene_budget and shot_budget are filled only by `stage.py estimate`, which no step, handout or `next` tells you to run.
9. **The self-test cannot be retried.** `selftest --score` deletes the test records, prints only the first 10 of 52 errors, and fails on rules the handout never states. A second `selftest --score --surface claude_code` gave `No test shots yet ... [exit 2]`. `next` tells you to pass `--surface <this app>`, but the step file does not.
10. **Step 7 and step 8 checks disagree.**
    - REASON-03 on step-7 MOVE `why` lines was not reported by `check --step 7 --scene SC02`; it first appeared under `check --step 8`.
    - STATE-01 accepted list subject CH-IONA.S01 at step 7, then rejected the same subject at step 8 because the state changes on the same line.
11. **GEOM-04 uses impossible distances in the vertical shaft plan.** It reports `50 mm at 4.0 m from Iona` for SU03 at [0.8, 0.6, 7.7], while her mark IONA_RUNG is at [0.3, 0.45, 7.2], about 0.7 m away. Other shots show 4.6 m and 1.2 m. The z axis or the move timing seems to be ignored.
12. **INFO-01 keeps warning after the fix.** `W INFO-01 SC15-SH020 thing shows PR-VESSEL ... before its reveal` still appears after `keep_hidden: FT-04 | how: sound_first` was added. The pump is only heard.
13. **CRAFT-07 ignores the in-story camera's lens.** For kind: screen shots it flags the 16 mm lens of CAM-JUDE-ROOM as outside the lens family.
14. **`because` accepts different kinds in different records.** SCENE department_idea `because` accepted TX-DASH-CLOCK. SHOT `because` refuses PROP, TEXT and LOCATION IDs (`E FORM-04 ... because "PR-FLASK" is neither an ID of a story record nor a line reference`), though they plainly are story records.
15. **`status` misreports progress.** It printed "Checked by the checker: never" after dozens of checks (checker_last_run is never updated). It also printed "the last was step 4 (world and style)", mixing internal and user step counts.
16. **The reader misread one speech.** It classified Iona's "(through the torch) No." as path `device_speaker`.
17. **Repair inbox names become unit names.** Names like U-02-FILM-fix1 and U-03-WORLD-fix2 are recorded in manifest units_done as if they were units.
18. **Book export defects,** as listed in section 4: truncated speeches, "made from put together in the edit", CUT records omitted, "30 shots in 30 scenes".

## 6. Unclear, contradictory or missing instructions

1. **CLAUDE.md is missing.** The task says CLAUDE.md is in /home/user/Stage, and SKILL.md says projects go to `My breakdowns/` in Claude Code. The file is not shipped and the tool puts the project elsewhere (bug 1).
2. **Step 0 contradicts the replace-all rule.** It says to send only the 4 PROJECT.rights `sets` lines and the 3 RT-001 lines "under the chosen option". The general rule "a field you send replaces all its stored lines" means that would silently delete the other options' RT-001 lines. I re-sent all 16.
3. **A screenplay user cannot limit steps 7 and 8 to some scenes.** Scope is only described for prose. I used PROJECT.scope through a new choice.
4. **Step 3 orders a choice that cannot be applied.** It says to write the music CHOICE setting SOUNDPLAN.music_policy, but SOUNDPLAN only exists at step 6. This leads to ID-02, then to bug 5, and to bug 3 if you work around it.
5. **Templates contradict the checker:**
   - RESERVE `max_uses` says "text", but the checker needs a number, `1_per_scene` or `share`.
   - LOCATION `wild_walls` says "text", but GEOM-05 needs compass wall names.
   - The STYLE template in the handout omits `provisional` and `named_reference_policy`, which FORM-05 requires.
   - Nowhere does it say that every repeated field (thing, effect, emphasis, side, subject) must be written as `none` when empty at Standard.
6. **Which kinds `because` accepts is only prose in card 14.** It differs between SCENE and SHOT (bug 14).
7. **Handouts leave things out:**
   - The step-7 handout omits the MOVE template (MOVE is listed under "You write").
   - It omits the scene's LOCATION set plan and the place's STATE, because `location` is written in the same unit.
   - It omits the in-story CAMERA (scene 15) and the scene's props and texts (the car's clock, sign and bus number).
8. **SCENE.host is never assigned.** The odd-lines report says the device "is named at step 5", but no unit or handout asks for it. It was still `open` at step 7.
9. **Character units are split badly.**
   - The code put Eli, Jude and Saye in a "minor characters" unit, though the card's worked example treats Saye as a principal.
   - No unit covers non-speaking characters (the figure, guard, nurse and technician).
   - The checker then demands the full principal-style field set, including a VOICE, from them.
10. **Some procedures have no unit or trigger:**
    - The step-4 name check has no unit and no instruction for when or how to record it.
    - FACT `element` at step 2 must name props that only exist after step 4, and nothing says to come back and re-point them. I had to trace back and fix them before step 7.
11. **Two kit-level notes are absent from SKILL.md:**
    - How to name a repair inbox.
    - The `next --checkpoint-passed` flag, which only `next`'s own output mentions.
12. **Two craft rules pull against each other, and the checker fires both:**
    - Eli's camera rule caps him at medium close-up before scene 13, while CRAFT-03 wants each scene's main turn to be its single tightest frame. In scene 9 that is impossible without breaking one rule.
    - In a fixed security-camera scene (scene 15), CRAFT-03 can never pass.
13. **The first estimate is tight for TIME-03.** Scene 9's target from the first estimate is 49 s against about 24 s of speech alone, so its shot list had to be trimmed to 53.8 s to stay inside the 10% tolerance.
14. **The whole-film summary is not short.** "02 Whole-film summary.md", described as "a short summary", is 23,717 words, which is heavy for any chat surface that attaches it.
15. **Scene numbering in the brief.** The brief's "scene 16 (Jude's room on the tablet)" is scene 15 in the kit's numbering.

## 7. Craft observations: would a director sign these shot plans?

**Scene 2, the freight shaft (14 shots, 64 s).** Mostly yes.
- **What works:**
  - The geography comes first: from just above the cage roof, the 24 mm looks up the ladder past the yellow band.
  - The climb is at her pace: the camera rises beside her at medium close-up.
  - Cause and effect are separate shots: the rung turns in her hand, then an insert of the sheared bracket as the anchor.
  - The turn is the scene's shortest shot (2.5 s, her weight dropping onto her hands). It is followed by the longest reaction beat, a small figure hanging over black on the 24 mm from below.
  - Two plants are laid honestly for scene 6: the bright sill (a 7 s shot) and the yellow band.
- **Changes a director would ask for:**
  - Open shot 030 to a medium close-up, so the turn's close-up is not equalled before it (CRAFT-03).
  - Consider whether the "It was my tooth" close-up plays a joke the tone rule says the camera must not play. A medium would keep it in her mouth.
- **Craft risk:** for AI video, three rising or climbing shots and a hang over depth are hard. The route and previs levels say so.

**Scene 9, the car (12 shots, 54 s).** Yes, after one fix.
- **What works:**
  - The camera rule does real work here: Eli only through side glass or in the rear-view mirror.
  - The 85 is spent once, on the mirror.
  - The story's red light is the only light change at the turn.
  - The refusal is the scene's longest shot, with Jude visible small in the mirror behind Eli, so the silent third is kept.
  - Inserts carry the wrong-side business: the hand hits the door, the palm opens on the rim, the backwards clock.
- **The fix:** shots 110 and 120 are the same setup and size on Eli (GEOM-02), effectively one shot split in two. A director would either merge them into one held mirror shot, or keep the mirror only for shot 120 and play Iona's question on her profile.
- **Open questions:**
  - Iona gets no clean single at all. Her reaction to "Drive." is only a soft edge, which is defensible (it lands on Eli) but worth a conscious sign-off.
  - Several nearly identical medium close-ups sit at the turn's own size (CRAFT-03), a consequence of the camera-rule cap.
- **Production caution:** left- and right-hand-drive errors and glass reflections are known AI failure points. The plan relies on the plate route and composited text, which is the right call.

**Scene 15, Jude's room on the tablet (4 shots, 37 s).** Yes, the strongest of the three.
- **What works:**
  - One fixed high-corner security frame for the whole scene (16 mm, 2.6 m), never zoomed.
  - Jump cuts only where the story writes the jump: the arrival "between one moment and the next", and "gone".
  - Sound before sight: the click, then the pump.
  - The care beat plays whole in the wide ("as carefully as a nurse").
  - The empty room and the chair are held longest.
- **Minor concerns:**
  - Nothing inside the scene says "on the tablet" except the presentation fields. A director might want the first frame to show the tablet's edge in Iona's hands, or a timestamp overlay, to anchor it.
  - 37 s of a static grainy wide is a bold hold. It suits the dread tone, but it relies entirely on the performance and the sound.
- **Book caveat:** the book hides the cut records, so a reader of the book would not see the jump-cut design at all.

**Overall.**
- Every shot gives a story reason, and most reasons quote the script.
- The checks caught real craft slips:
  - the plant emphasis
  - quote spans
  - carriers
  - turn reaction times
  - text reading floors
  - mirrored text governance
- Much of the checker's output, though, was noise from fields the AI is not allowed to write.
