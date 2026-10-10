# 10 Steps 07-08 - scenes and shots

Part of the Stage chat kit: a step-group file, attached to the chat that runs one of these steps (not knowledge). It joins the step files 07 Scene design and shot list, 08 Shot details, each whole. Read the one for this unit every time, quote its one-line task back before any work, and follow its section "If you cannot run code" when this chat has no code. 01 House rules (in the knowledge) says where every other skill file is.

---

From the skill file `stages/07 Scene design and shot list/CONTEXT.md`:

# Step 7. Scene design and shot list

This is step 7 of the pipeline; the user counts it as step 8 of 12, "designing the scenes and listing their shots". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Design one scene (its values, beats, wants, turns, moves, department ideas, turn pictures and dial) and end with a one-line shot list that fixes every shot's ID.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Design each scene, then fix its shot IDs and count in a one-line list before any detail (principle 6).

## When it runs

Sequence by sequence: design and list a sequence's scenes, checkpoint C, step 8 writes their shots, then the next sequence (a first group of scenes 1 to 3: U-07-SC01 to U-07-SC03, checkpoint C, U-08-SC01-B1 on, then U-07-SC04; `next` follows the groups of the story plan). At Quick depth step 8 never runs; the list is the final shot plan.

Only scenes in `scope` run. "Only do scenes 2, 9 and 16 for now" is an asked CHOICE (numbered from your handout's block) with `sets: PROJECT.scope | value: SC02, SC09, SC16 | when: a` and `answer: a`; once applied, `next` offers only those scenes. "Do the rest" sets `all`.

## Inputs

The handout (in chat, the attached files): the scene's lines and plan fields; the film rules it touches (camera rules of those present, saved choices allowed here, VISUAL row, LOOK, SOUNDPLAN, LADDER rung); present characters' fixed descriptions, states, voices, `movement`, `gesture`, `status_play`; FACT and PLANT records with story points here; its LOCATION, set plan and start state; any in-story CAMERA; the PROP and TEXT records its lines name; the previous scene's last shot; the templates (MOVE too), a gold excerpt, the IDs below.

## Outputs

`11 Scenes/Scene NN - <place>.md`: the plain part (code writes it; you in chat), the divider, then SCENE design fields, PART, BEAT, SPEECH (prose only), MOVE, SETUP, SHOTLIST; small choices go to `01 Choices.md`. After `apply`, code resolves each story point here to a beat.

## Card parts to open

At most `card_tokens_per_unit_max` card tokens.
- Quick: card 03, whole; card 14, part "The one-line shot list".
- Standard adds: card 04, parts "Landing face", "Flaws" and "Pauses"; card 12, part "Stations and configuration"; card 13, part "Scene rhythm".
- Detailed adds: card 06, part "Display and timed actions"; card 07, part "Emphasis"; card 11, part "Per-scene light".
- By the scene's tags, parts "Questions in order" and "Traps" of: card 15 (`action`); card 16 (`glass_and_reflection`, `handedness`); card 17 (`screens_and_text`, `in_story_footage`); card 18 (`suspense_and_reveal`, `darkness`); card 19 (`prose_interior`, `montage_and_time`); card 20 (`creature`, `violence`).
- Tag `prose_interior` also: card 02, part "Externalising inner life".

## Procedure

In this order; shots come last.

1. **Values.** Copy the event. Write each `value` with `open` and `close` charges (`SC10-V1 | name: ... | open: + | close: --- | turns_at: SC10-B07`). Sign test: every beat whose `turn` is not `none` changes the sign of a value's charge or reaches its close (CRAFT-18; card 03).
2. **Wants**, `driver`, `conflict`, `third_thing`.
3. **Beats.** `lines` (every source line in exactly one beat), `action` and `reaction` as -ing tactics (alone, or when the world acts, name the person for both, the reaction theirs; a group with no record acts through the nearest recorded character, with a note), `task`, `beat_intensity` (at most `beat_intensity_5_per_part_max` fives per part), `turn`, `turn_kind`, `charge`, PART records; `flag` items naming their speech, flagged, never fixed (a flaw in an action line goes in the beat's `note`); with tag `three_or_more`, each beat's `engaged_pair` and `silent_third`.
4. **Five steps** for each turn and each beat of intensity 4 or more.
5. **Dialogue pass** (Standard: turn beats, flagged lines, revealed facts, refusals, lines the plan names; Detailed: every line): `landing_face`, `unsaid` and `carrier`, `pause_after` by `pause_tiers` (at most `long_pauses_per_scene_max` long; a turn owes at least `turn_reaction_min_s`; a `hold` needs a saved choice).
6. **Staging.** A `staging` line, or MOVE records wherever a set plan exists (always at Detailed) with each character's `start` (written even when nobody moves); SETUP records, a camera for every list item (one may serve several), placed so lens and distance give the item's size (the sum is in step 8, Camera; GEOM-04), never inside an object; without a set plan, `at_words` and `look_at_words`; the line of action per part. The configuration changes on every turn (`change`); between turns a body moves only for a want or task you can name, and distances change only with a value's charge (B3 P2-P3). Over `stations_needed_above_beats` beats, name `stations_per_scene` stations.
7. **Ideas.** `scene_idea`, and one `department_idea` each for camera, light, staging, sound and design, citing an ID; `holds_baseline` is a full answer. At most `departments_changing_at_main_turn_max` change at the main turn, named in `scene_idea` (B3 R7; B1 P11; CRAFT-19); the staging always changes on a turn, so it is one of them.
8. **Turn pictures**, one sentence each: `turn_picture: SC10-B07 | picture: Iona close, eyes on Saye just off the lens, her mouth stopped mid-chew`.
9. **The dial.** Per beat, `size`, `distance_m`, `height`, drawn toward the turn and away. Light stays `as_look` and sound `room_sound` unless a story source can change them (B2 R10) or at the rupture; a beat the script already marks gets nothing added (B4 R23; CRAFT-10), but its own light, when the look does not carry it, is a `light_cue` whose `why` quotes the line: that is the script's, not an addition (COVER-08).
10. **Rhythm.** `rhythm_shape`, `target_asl_s` (from the shape, the tone and card 13, never `rhythm_class`; the list unit sends it again when the list's average shot length lands elsewhere), one `rupture`. In suspense, hold on the one who does not know (A4 S2).
11. **Action** (tag `action`): `geography`, `cause_chain`, `escalation`, `reversal`, `action_score`, `time_treatment` (card 15).
12. **The one-line list**: turn shots first, then must-keep shots (plants, reveals, geography), then the rest, until every beat and line is covered; each `item` names beats, role, size, frame, subject, seconds and what we see (card 14). The main turn takes its LADDER rung's size, nothing earlier tighter (it may equal it) unless the rung plays the turn wide on purpose; with no rung, the tightest size its subject's camera rule and the saved choices allow (CRAFT-03); a rung on another beat sets that beat's shot, and the main turn follows its subject's camera rule; a speech too long for one item is split by quoting, in each item, the part it hears (its shot's `hear` then gives those `words`); a hit and its result are two items, cut at the contact, the second opening on the result in a clearly different size or angle (CRAFT-28; card 15); through one fixed in-story camera (The Catch, scene 15) the frame's action and the cuts carry the turn.
13. **Additions**, each with `changes_meaning` (yes for a new object or a new move at a turn); an invented record is named by its ID (CRAFT-14), in every scene that shows it, even one invented at an earlier step.
14. **Check**: `stage.py check --step 7 --scene SC10`; fix only what it prints, at most `repair_rounds_max` rounds. SHOTLIST `approved` is code's, set when the group passes; the check does not ask for it before.

## Record template

`references/templates/11 Scene.md` (SCENE design fields, PART, BEAT, SPEECH, MOVE, SETUP, SHOTLIST).

## IDs you will be given

Per scene (`issued_blocks`): beats `SC10-B01` to `SC10-B30`; parts `SC10-P1`, values `SC10-V1`, moves `SC10-M01`, setups `SC10-SU01` onward; shots `SC10-SH010` to `SC10-SH400` in steps of `shot_number_step` (end cards and a closing black in `end_card_numbers`; a black inside the scene takes a normal number with `kind: black`). A value and a list item declare their ID as their first part; speeches come with IDs and words (`SC10-D11`, "Not mint."). Use them in order (ID-06).

## Batch and chunk rules

One scene per unit; a scene over `scene_split_non_blank_lines` non-blank lines (70, heading included) is designed in two units by part and listed in a third: The Catch's scene 13 runs as U-07-SC13-P1, -P2, -LIST. The split is decided once, at the scene's first handout; a scene designed whole stays whole, even past `scene_split_beats` (14) beats. In part 1, forward references to part 2's beats and lines not yet covered are expected; write the scene-level fields (`turns_at`, `turn_picture`, `rupture`, dial) in the part that holds their beats.

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Is every source line and every speech in a beat?
2. Does every turn have a turn picture, visible in one frame, and a list item with `role: turn`?
3. Does the configuration change on every turn, and every move between turns have a want or task you can name?
4. Do the dial and the list cover every beat, with every list ID in the issued block and in tens?
5. Is every story point in this scene resolved to a beat?
6. Which list item's reason would fit any film?
7. Does `check --step 7 --scene SC10` exit 0?

## The report

After each scene a short report (in chat ending with the list); after a sequence's last scene, checkpoint C's message (`references/formats/07`; your own counts):

```
Done: group 3, scenes 7 to 10 (step 8 of 12). 58 shots, about 4 minutes.
Example: shot 150 is the turn of scene 10: Iona's close-up held 15 seconds, from
  the first chew through Saye's "Nothing has happened to the mint...".
Made: 11 Scenes/Scene 07 to Scene 10 (designs and one-line shot lists).
  Checked: no problems. One added detail changes a scene, to keep or cut: Iona sets
  the lamp down before she raises her hand (scene 10). 6 small additions kept
  (listed in 01 Choices).

Scene 10 - Saye's kitchen - 20 shots and a title card - about 1 minute 53 seconds
 shot 150, 15 seconds: the turn: close-up, Iona chews, stops, chews once more; "Not mint."
                       We stay on her through Saye's answer
 (the other 19 shots are listed in the scene file)
Needs you: nothing. I'm carrying on; tell me anything you want changed.
Next: writing the shots of scenes 7 to 10 in full, then group 4.
```

## Checkpoint

Checkpoint C, "each group of shots": each scene's "At a glance" and list in plain words, total screen time, additions that change meaning (the rest counted in `00 Start here`), anything flagged, small choices. One ask, default [next]. After a group's last list, run `stage.py next`. Only the first group waits (every group, after "stop after each group": `stage.py next --stop-after-each-group yes`): show the message, and when the user replies "next", run `stage.py next --checkpoint-passed`, which approves the lists. A later group does not wait: `next` approves its lists and says so; show the message and carry on. The first message adds:

```
The film's rules, in five lines (a change here costs little now):
  1. The camera stays still, at the eye height of the person the scene belongs to.
  2. It breaks that rule once, in scene 26, when she pushes away from the rail.
  3. Eli is never pushed in on; his closest shots are saved for scene 13.
  4. The film's tightest shot is saved for scene 13; the crossing is played wide and still.
  5. No slow motion and no music: the pump and the engine click do music's job.
Needs you: reply "next", or tell me what to change.
After this group I'll carry on and show you each group; say "stop after each group"
if you prefer.
```

## How to redo

"Redo scene 10" redoes the design and the list; "Change shot 150 to ..." changes one list item, and its written shot goes stale (`stage.py impact`).

## If you cannot run code

Every line reference is a quote anchor: beat `lines`, `because` lines and story points quote the scene exactly, at least `quote_anchor_words_min` words, found once in it (`- lines: "Iona chews it." to "street signs either."`). Never add a ` = <beat>` ending.

1. Number the speeches in cue order yourself (`SC10-D01` is the first cue); prose gets SPEECH records with the exact words.
2. Write the scene file in one copy box: plain part, divider, records, a `---` line, the checks-in-words table (`references/formats/06 Checks in words.md` part 1), the END line. Print "Checked in words: 14 of 14 passed" (or only the failures).
3. Write `status: approved`, `locked: yes` and SHOTLIST `approved: yes`; if the user changes the list, save the scene file again.
4. Step 8 follows the group message; the check chat follows the group's last batch. Mid-group:

```
Save as: 11 Scenes/Scene 11 - Treatment floor.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 02 Whole-film summary,
10 Film rules, 10 Steps 07-08 - scenes and shots, your story and Scene 11 - Treatment floor;
type: Continue my breakdown. Next is scene 12.
```

**One-line task, again:** Design one scene (its values, beats, wants, turns, moves, department ideas, turn pictures and dial) and end with a one-line shot list that fixes every shot's ID.

---

From the skill file `stages/08 Shot details/CONTEXT.md`:

# Step 8. Shot details

This is step 8 of the pipeline; the user counts it as step 9 of 12, "writing the shots". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Expand one batch of the approved one-line list into full shot records, reasons before camera values, one record per list item, with a cut record only where the join is not a plain cut.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Expand the approved one-line list into full SHOT and CUT records, batch by batch. The list fixed each shot's ID, beats, role and size; this step writes why the shot exists, what we see and hear, how long it holds and how it will be made.

## When it runs

Sequence by sequence, after checkpoint C: every scene of the sequence, in screen order, its batches in ID order; then the next sequence starts with step 7. Standard and Detailed only: at Quick the list is the final shot plan.

## Inputs

The handout (in chat, the attached files): everything step 7 had, the scene design just written, and the batch's approved list items, each with its **provisional time floor** (every speech whose cue lies in the item's beats, or the text to read that its `shows` quotes, whichever is longer, plus the pause owed by the beats it ends). It lists only the sizes, angles and moves the camera system allows here (banned choices are left out; saved ones appear with their RC ID and uses left), and every field that needs a `why` when it departs from its default, with the default.

## Outputs

SHOT and CUT records, appended to `11 Scenes/Scene NN - <place>.md` on code surfaces, or saved in chat as `11 Scenes/Scene 10 - Saye's kitchen - shots 130-200.md` (merged by ID, G10). `stage.py build` then works out the derived fields. When a shot writes a `time_slice` or a CUT writes `shared_geometry`, code creates the named PREVIS stub (`PV-SC06-MASTER-V01`, `status: planned`).

## Card parts to open

At most `card_tokens_per_unit_max` card tokens.
- Standard: card 14, part "Full shots"; card 10, part "Slots and moves"; card 12, part "Frame rules"; card 13, part "Cut points and sound"; card 04, parts "Landing face" and "Pauses"; card 06, part "Display and timed actions".
- Detailed adds: card 11, part "Per-shot light".
- By the scene's tags, parts "Questions in order" and "Traps" of: card 15 (`action`); card 16 (`glass_and_reflection`, `handedness`); card 17 (`screens_and_text`, `in_story_footage`); card 18 (`suspense_and_reveal`, `darkness`); card 19 (`prose_interior`, `montage_and_time`); card 20 (`creature`, `violence`).
- Tag `prose_interior` also: card 02, part "Externalising inner life".

## Procedure

For each list item in order, write one SHOT at the project's depth, in reason-first order: why before how (card 14, "Full shots"). A field the depth asks for with nothing to hold is written `none` (`- effect: none`); left out, it is an error (FORM-05).

1. **Copy** the item's shot ID, `beats` and `role`, and keep its `size` (ID-08); add `lines`: a speech's words are on the lines after its speaker's name, so `lines` covers both (the handout gives each speech's cue line and word lines).
2. **Reasons.** `purpose`: one sentence naming the change the audience must get. `because`: what justifies it, as the ID of any story record (scene, beat, value, character, state, place, prop, text, motif, rule, plan, camera rule, saved choice, look, fact, plant) or a line reference, the same set SCENE takes; a turn shot cites its turn beat (REASON-05), a saved choice its RC (REASON-06); `default` only on a normal shot with no departure.
3. **Camera.** `kind` (`screen` is the picture an in-story camera makes, at its own lens), `setup`, `frame`, `size`, `angle`, `height`, `lens_mm` (the family in force here, as the handout gives it), `focus`, `focus_on`, one `move` (CRAFT-06) with its `move_reason`. With a set plan, size must fit lens and distance (GEOM-04): the height the frame shows at the subject is 36 ÷ lens × distance ÷ the frame ratio; divided by the subject's height (seated: 0.55 of it) it reads 2.0 or more extreme wide, 1.1 wide, 0.75 medium wide, 0.45 medium, 0.3 medium close-up, 0.15 close-up, less extreme close-up; two steps off warns; inserts and a focus on a thing are not measured. A camera never stands inside an object of the set plan, and beyond a wild wall only within the room's other extent (GEOM-05).
4. **People.** One `subject` item per person in frame: `at` and `faces` may be left out where a set plan exists (code projects them, and checks any you write, GEOM-06); `does` as visible behaviour, never emotion words (WORDS-01); `tactic`, `energy`, `display`, `eyeline` with `dwell_s`, `travel`, and `must_not` for a glance saved for a later beat. Leave out the old `still` part: a list of parts that stay still reads to a video model as an order to freeze.
5. **Sound and things.** `hear` items (each speech heard, `speaker: on_screen` or `off_screen`); `thing` items (a thing with states is named by the state valid here, `PR-FLASK.S02`; STATE-01; footage of an earlier time names the state it shows with `| recorded: SC06` (any time in scene 6) or `| recorded: SC06 "The cage falls."` (that moment), on a `thing` or a `subject`; a thing continuity gave no state here gets one from you, as an addition: its next free state number (code orders states by `from`, so numbers need not follow story order), `from` this line, `origin: story` when the line states it, else `inferred`, listed in the scene's `additions`) with `emphasis`, and `plant:` or `payoff:` on the item that plants or pays off a PLANT; `text`; `keep_hidden` (the FACT it protects and how: this clears INFO-01, so what is really on screen stays in `must_show`), `must_show`, `must_not_show`; `light` only when it differs from the look (light the story writes and the look does not carry: a `light_cue` whose `why` quotes the line, which counts as the script's, never as an addition; COVER-08, CRAFT-10); `effect`, `room_sound`, `silence` (`room_sound_only` and a silence the sound plan or the beat's pause already plans add nothing), `music`, `needs_description`.
6. **Time.** `screen_time` at or above the provisional floor (TIME-01): shot 150's floor is 13.8 seconds (Saye's and Iona's speech, 11.8, plus 2.0 owed after the turn at beat 7), so it runs 15. The floor holds the longer of speech and text to read (text the audience must read: plot-critical or given emphasis, never blurred background), plus each beat's pause, owed once, on the last shot naming the beat. Timed `moment` items inside it, each a main action: one per started 4 seconds (a 4-second shot holds one, 4.5 seconds two; TIME-06); `end`; `cut_out_on`. A held moment of `hold_action_every_s` or more carries a small timed action at least every `hold_action_every_s`, joined by ";" or "then" (shot 150, seconds 8 to 15: "swallows once; breathes out slowly through her nose; blinks; her lips press together; ..."; CRAFT-26), and no moment, `does`, `start` or `end` asks for stillness ("stays still", "does not move"; CRAFT-27). A hit and its result never share a shot: end on the contact and open the next shot on the result (CRAFT-28). Make it physically possible: room to stand, a reach the person can make, one thing per hand, nothing heavy in the teeth, something to cut with (PHYS-01 to PHYS-11; suggestions, answered in words). A beat's unsaid carrier is seen in a `thing` (with its `at`), a `does`, a `moment`, the `end`, an `effect` or a heard speech of that beat's shots (REASON-08).
7. **Making.** `held: yes` where the meaning depends on not cutting (turn shots count as held); `previs_level`, `storyboard`, `framing_critical`, `route`, `flip` (`never` on a sided insert such as a ring; SIDE-03), `content_flags`, `policy_route`, `cost_class`, `reuse_of`; `pov_break` when the shot leaves the whose-scene character's place or knowledge.
8. **`why`**, one sentence that quotes a line, names an object or action, or cites an ID, never a mood (REASON-03, REASON-04). Always on turn shots; otherwise wherever a value departs from its default or the camera system (REASON-02): `angle` eye_level; `height` the eye of the whose-scene character, or of the subject; `lens_mm` the normal lens; `move` static; `focus` moderate; `light` as_look; `room_sound` as_place; `silence` none; `music` none; `display` 1 in a close-up or tighter. `size` and `frame` never need one. The book prints `why` and `note` for the user: no card numbers, set-plan names in capitals or coordinates (name the fire door in plain words), and name a lens as the 40 millimetre lens; a line number alone does not anchor a `why`.
9. **Cuts.** A CUT record only where the join is not a plain cut (`to`, `type`, `split_s`, `black_frames`, `sound_across`, `shared_geometry`, `why`). A dissolve, fade, cut to black, freeze or smash cut only where the story writes it (CRAFT-13): scene 10's `SC10-C200` is the script's "CUT TO BLACK.".
10. **Never type what code works out**: labels, time floors, clip lengths, image sides, eyeline sides, mirror states, prompts, prices (FORM-10).
11. **Check**: `stage.py check --step 8 --scene SC10`. During the scene, ID-07 and COVER-02 to COVER-04 cover only the batch's range; after its last batch they run in full, with TIME-03 (a warning: the shots against the list's total) and the scene-wide checks (COVER-08, TIME-09). Fix only what it prints, at most `repair_rounds_max` rounds: errors always, and a warning when its fix is in your own records. A warning you leave (a real choice, or a record this step may not write, such as a fact's `known_by`) goes in the report and waits for the next checkpoint.

The turn shot's reasons, from `references/examples/01 The Catch - scene 10.md`:

```
- purpose: Iona's body admits what her words denied; Saye's proof lands on her face.
- because: SC10-B07, SC10-V1, MO-MINT, CR-IONA
- why: "Her face changes." puts the turn inside her mouth, so the scene's closest frame is spent here and held while Saye's proof lands off screen, on its target.
```

## Record template

`references/templates/11 Scene.md` (SHOT, CUT).

## IDs you will be given

The batch's shot IDs, copied from the approved list (`SC10-SH130` to `SC10-SH200`); never add, drop or renumber one. A CUT takes the scene and the number of the shot it follows (`SC10-C200`); a fade-in before the first shot is `SC10-C000`. PREVIS stubs are named by code.

## Batch and chunk rules

`batch_size` shots per unit (the default until the self-test passes, then the larger value), split by ID range from the list; the manifest records each scene's expected ranges. A record is never split across replies. The Catch at Standard: 300 to 580 shots, 25 to 50 batches.

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Does every list item in the batch have exactly one SHOT with the same beats, role and size?
2. Name the turn shot: is any earlier shot closer?
3. Is there an emotion word in any `does`?
4. Does every held moment carry small timed actions (a breath, a blink, a swallow, a glance), with no word asking for stillness, and could a real body do everything written?
5. Which `why` would fit any film? Rewrite it from this story.
6. Which invented items could go, and is every one kept listed in the scene's `additions`?
7. Does the END count match the batch's records, and does `check --step 8 --scene SC10` exit 0?

## The report

After each batch, a short report; after the scene's last batch:

```
Done: scene 10 of 30, step 9 of 12, writing the shots. 20 shots and a title card.
Example: shot 150 holds Iona's face for 15 seconds, from the first chew through
  Saye's answer, because "Her face changes." puts the turn inside her mouth.
Made: 11 Scenes/Scene 10 - Saye's kitchen (every shot written in full).
  Checked: no errors; 2 warnings to show you with the next group (in 13 Health check).
Needs you: nothing.
Next: scene 11, the treatment floor, which starts group 4 (in a chat app,
  first the check of group 3).
```

## Checkpoint

None: the one-line list was the checkpoint. Warnings are shown at the next group of shots.

## How to redo

"Redo the shots for scene 10" keeps the list and rewrites its shots. "Make shot 150 tighter" edits one list item and its shot; `stage.py impact SC10-SH150` names what else goes stale.

## If you cannot run code

Every line reference is a quote anchor: `lines` is an anchor pair (`- lines: "Iona chews it." to "street signs either."`), and `because` lines read `line: "<exact quote>"`, each at least `quote_anchor_words_min` words, found once in the scene.

1. Each `hear` item also carries the speech's exact words: `- hear: SC10-D11 | speaker: on_screen | words: "Not mint."` (CITE-04).
2. Work out each floor in words to set `screen_time`: each speech's words divided by its voice's `pace_wps`, plus `speech_floor_extra_s` per speech, plus the pause owed (at least `turn_reaction_min_s` after a turn). Never write the floor into a record.
3. Save each batch in one copy box, `11 Scenes/Scene 10 - Saye's kitchen - shots 130-200.md`: the records, a `---` line, the checks-in-words table (`references/formats/06 Checks in words.md` part 1), the END line counting this file's records (`END OF FILE | Scene 10 shots 130-200 | 8 records`). Print "Checked in words: 14 of 14 passed" (or only the failures).
4. A box with no END line is never saved. When the user types **continue**, send its complete records again as their own file (`... - shots 130-160.md`), then, in the next reply, the rest from the start of the cut record (`... - shots 170-200.md`), each with its END line. A box short of the list's IDs: send only the missing records, then the END line (step 16).
5. Report, then the resume line. After a group's last batch it names the check chat first: "Next: a check. New chat in this project; attach the files of scenes 7 to 10, your story, 02 Whole-film summary, 10 Film rules, 05 Checks in words and your last 13 Health check file; type: Check my group of scenes." Otherwise:

```
Save as: 11 Scenes/Scene 10 - Saye's kitchen - shots 010-120.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 02 Whole-film summary,
10 Film rules, 10 Steps 07-08 - scenes and shots, your story, Scene 10 - Saye's kitchen
and its shot files; type: Continue my breakdown. Next is scene 10, shots 130 to 200.
```

**One-line task, again:** Expand one batch of the approved one-line list into full shot records, reasons before camera values, one record per list item, with a cut record only where the join is not a plain cut.
