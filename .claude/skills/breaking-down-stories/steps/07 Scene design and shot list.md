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
- Detailed adds: card 06, part "Display and stillness"; card 07, part "Emphasis"; card 11, part "Per-scene light".
- By the scene's tags, parts "Questions in order" and "Traps" of: card 15 (`action`); card 16 (`glass_and_reflection`, `handedness`); card 17 (`screens_and_text`, `in_story_footage`); card 18 (`suspense_and_reveal`, `darkness`); card 19 (`prose_interior`, `montage_and_time`); card 20 (`creature`, `violence`).
- Tag `prose_interior` also: card 02, part "Externalising inner life".

## Procedure

In this order; shots come last.

1. **Values.** Copy the event. Write each `value` with `open` and `close` charges (`SC10-V1 | name: ... | open: + | close: --- | turns_at: SC10-B07`). Sign test: every beat whose `turn` is not `none` changes the sign of a value's charge or reaches its close (CRAFT-18; card 03).
2. **Wants**, `driver`, `conflict`, `third_thing`.
3. **Beats.** `lines` (every source line in exactly one beat), `action` and `reaction` as -ing tactics, `task`, `beat_intensity` (at most `beat_intensity_5_per_part_max` fives per part), `turn`, `turn_kind`, `charge`, PART records; `flag` items naming their speech, flagged, never fixed; with tag `three_or_more`, each beat's `engaged_pair` and `silent_third`.
4. **Five steps** for each turn and each beat of intensity 4 or more.
5. **Dialogue pass** (Standard: turn beats, flagged lines, revealed facts, refusals, lines the plan names; Detailed: every line): `landing_face`, `unsaid` and `carrier`, `pause_after` by `pause_tiers` (at most `long_pauses_per_scene_max` long; a turn owes at least `turn_reaction_min_s`; a `hold` needs a saved choice).
6. **Staging.** A `staging` line, or MOVE records wherever a set plan exists (always at Detailed) with each character's `start`; SETUP records, a camera for every list item (one may serve several), placed so lens and distance give the item's size (the sum is in step 8, Camera; GEOM-04), never inside an object; without a set plan, `at_words` and `look_at_words`; the line of action per part. The configuration changes on every turn (`change`); between turns a body moves only for a want or task you can name, and distances change only with a value's charge (B3 P2-P3). Over `stations_needed_above_beats` beats, name `stations_per_scene` stations.
7. **Ideas.** `scene_idea`, and one `department_idea` each for camera, light, staging, sound and design, citing an ID; `holds_baseline` is a full answer. At most `departments_changing_at_main_turn_max` change at the main turn, named in `scene_idea` (B3 R7; B1 P11; CRAFT-19).
8. **Turn pictures**, one sentence each: `turn_picture: SC10-B07 | picture: Iona close, eyes on Saye just off the lens, her mouth stopped mid-chew`.
9. **The dial.** Per beat, `size`, `distance_m`, `height`, drawn toward the turn and away. Light stays `as_look` and sound `room_sound` unless a story source can change them (B2 R10) or at the rupture; a beat the script already marks gets nothing added (B4 R23; CRAFT-10), but its own light, when the look does not carry it, is a `light_cue` whose `why` quotes the line: that is the script's, not an addition (COVER-08).
10. **Rhythm.** `rhythm_shape`, `target_asl_s` (from the shape, the tone and card 13, never `rhythm_class`), one `rupture`. In suspense, hold on the one who does not know (A4 S2).
11. **Action** (tag `action`): `geography`, `cause_chain`, `escalation`, `reversal`, `action_score`, `time_treatment` (card 15).
12. **The one-line list**: turn shots first, then must-keep shots (plants, reveals, geography), then the rest, until every beat and line is covered; each `item` names beats, role, size, frame, subject, seconds and what we see (card 14). The main turn takes its LADDER rung's size, nothing earlier tighter (it may equal it) unless the rung plays the turn wide on purpose; with no rung, the tightest size its subject's camera rule and the saved choices allow (CRAFT-03); through one fixed in-story camera (The Catch, scene 15) the frame's action and the cuts carry the turn.
13. **Additions**, each with `changes_meaning` (yes for a new object or a new move at a turn); an invented record is named by its ID (CRAFT-14).
14. **Check**: `stage.py check --step 7 --scene SC10`; fix only what it prints, at most `repair_rounds_max` rounds. SHOTLIST `approved` is code's, set when the group passes; the check does not ask for it before.

## Record template

`templates/11 Scene.md` (SCENE design fields, PART, BEAT, SPEECH, MOVE, SETUP, SHOTLIST).

## IDs you will be given

Per scene (`issued_blocks`): beats `SC10-B01` to `SC10-B30`; parts `SC10-P1`, values `SC10-V1`, moves `SC10-M01`, setups `SC10-SU01` onward; shots `SC10-SH010` to `SC10-SH400` in steps of `shot_number_step` (end cards and black in `end_card_numbers`). A value and a list item declare their ID as their first part; speeches come with IDs and words (`SC10-D11`, "Not mint."). Use them in order (ID-06).

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

After each scene a short report (in chat ending with the list); after a sequence's last scene, checkpoint C's message (`reference/07`; your own counts):

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
2. Write the scene file in one copy box: plain part, divider, records, a `---` line, the checks-in-words table (`reference/06 Checks in words.md` part 1), the END line. Print "Checked in words: 14 of 14 passed" (or only the failures).
3. Write `status: approved`, `locked: yes` and SHOTLIST `approved: yes`; if the user changes the list, save the scene file again.
4. Step 8 follows the group message; the check chat follows the group's last batch. Mid-group:

```
Save as: 11 Scenes/Scene 11 - Treatment floor.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 02 Whole-film summary,
10 Film rules, 10 Steps 07-08 - scenes and shots, your story and Scene 11 - Treatment floor;
type: Continue my breakdown. Next is scene 12.
```

**One-line task, again:** Design one scene (its values, beats, wants, turns, moves, department ideas, turn pictures and dial) and end with a one-line shot list that fixes every shot's ID.
