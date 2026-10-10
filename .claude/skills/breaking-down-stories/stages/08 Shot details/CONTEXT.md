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
