# Card 14. Shot design

Step 7 reads only "The one-line shot list"; step 8 reads only "Full shots"; chat apps read it whole. "B1 R6" is rule 6 in B1 §11, "B1 P11" principle 11 in B1 §1; "A2 R4" is rule 4 in A2 §7, "D15 R6" in D15 §3.

## The job

Shot 150 of The Catch's scene 10 is its turn shot, a close-up held on Iona through "Not mint." and Saye's answer, because "Her face changes." (line 456) puts the turn inside her. Shots are the last thing written: from the turn pictures and the dial, turn shots first, then must-keep shots, then the rest (A2 Step 9). Step 7 hands on the one-line list fixing every shot's ID and count; step 8, one full SHOT per item, reasons before camera values.

## Questions in order

1. **Whose scene is this beat?** Put the lens at that person's eye height (B1 R6).
2. **Is this beat a turn?** Give it the scene's most extreme framing: closest if the turn happens inside a person, widest if it leaves them alone or waiting (B1 R1, A2 R4).
3. **Has the script already marked the beat** (a line, a look, a change of state)? Then the camera adds nothing (B1 P11, B4 R23).
4. **Is someone hiding a feeling?** Keep them one size wider than the progression would reach, except on a turn (B1 R5, R1).
5. **What must the audience get from this shot, and which records justify it?** (A2 Step 9; REASON-01)
6. **What does the body do, and what stays still?** (D15 P1, P4)
7. **How long must it stay up to be read?** (K08 to K10)

## The one-line shot list

Example: `SC10-SH150 | beats: SC10-B07, SC10-B08 | role: turn | size: close_up | frame: single | subject: CH-IONA | time: 15 | shows: Iona chews, stops, chews once more; "Not mint."; we stay on her through Saye's answer`.

The **one-line shot list** (SHOTLIST `item`) fixes each shot's ID, beats, role, size, frame, subject, seconds and one line of what we see, before any detail. IDs come from the handout's issued block, in steps of `shot_number_step`; an insert takes a number between (SH155); end cards and black use `end_card_numbers` (ID-03, ID-06). At Quick depth these items are the final shots.

Write them in this order (A2 Step 9):
1. **Turn shots** (`role: turn`), one per turn, from the **turn pictures**, the one-sentence frames each turn must show, written at step 7 before any shot (CRAFT-04). The main turn gets the scene's most extreme framing and nothing tighter comes before it (A2 R4; CRAFT-03); a later turn gets its part's tightest size or a deliberate wide.
2. **Must-keep shots** (`role: must_keep`): plants, reveals and the geography of a new place. A fact's reveal shot is a turn or must-keep shot (INFO-02); a new place gets who-is-where in its first one or two shots (A2 R29).
3. **The rest**, until every beat and every line is covered (COVER-02 to COVER-04). A new beat changes the image; a repeated tactic keeps one setup (camera position); a beat with no words still gets its shot, in full view (A2 R1 to R3).

**Coverage from the dial.** The **dial** gives each beat a planned size, distance and height, drawn toward the turn and away from it; list sizes stay within `size_step_difference_warning` steps of it (CRAFT-17). SCENE `coverage` is `designed` (each shot planned for its beat), `chained` (each starts where the last ended, for continuous physical action), `master_and_coverage` (a wide of the whole action plus closer shots; hardest for AI, since no performance repeats exactly) or `oner` (one shot) (A3 §5.6, R16).

Rules for the list:
- In dialogue, plan singles that need not match frame for frame, and keep the wide for the start and the turn (A3 §5.6); one staged wide can do the work of several singles (B3 §4.1).
- Several people reacting at once share one frame (A2 R7).
- Estimate seconds from the speech and pauses in the item's beats (A2 Step 9); a shot without dialogue starts from `non_dialogue_seconds_by_intensity` (A4 §6.1). Step 8 holds each full shot to its floor.
- The main turn's shot is the scene's longest or its shortest (A4 P5; TIME-10), and the scene's total stays within `scene_total_tolerance` of its target (TIME-03).

## Full shots

Example, from the turn shot: `purpose: Iona's body admits what her words denied; Saye's proof lands on her face.` `because: SC10-B07, SC10-V1, MO-MINT, CR-IONA`. `why: "Her face changes." puts the turn inside her mouth, so the scene's closest frame is spent here and held while Saye's proof lands off screen.`

Write each SHOT reason first: `purpose`, `because`, `role`, then the camera.
- `purpose`: one sentence saying what the audience must get; it names a change (A2 Step 9; REASON-01).
- `because`: the IDs that justify the shot (beat, value, motif, plant, fact, character, rule, saved choice, look, state) or a `line:`. `default` only on a normal shot with no departure (REASON-01). A turn shot cites its turn beat (REASON-05); a saved choice (a rationed choice, RESERVE) cites its RC (REASON-06).
- `why`: one sentence that quotes a line, names an object or action, or cites an ID, never a mood (REASON-03, REASON-04). Always on turn shots. Otherwise needed wherever a field departs from its default: `angle` eye_level; `height` the eye of the whose-scene character (the person whose point of view the scene holds) or of the subject; `lens_mm` the normal lens of CAMSYS; `move` static; `focus` moderate; `light` as_look; `room_sound` as_place; `silence` none; `music` none; `display` 1 in a close-up or tighter. `size` and `frame` never need one (REASON-02).
- **The camera slots**, in order: size, angle and height, lens, focus, camera move, and frame shape only for footage inside the story (B1 §0; card 10). One camera move per shot (CRAFT-06).
- **Behaviour, not emotion.** `does` holds visible behaviour, never emotion words (WORDS-01; A3 R2). A line that names a feeling ("Her face changes.") becomes two or three timed steps (D15 R1). **Display** is how openly a face shows: 1 contained, 2 visible, 3 open; the closer the shot, the lower the level, and `display: 3` at `display_3_needs_why_at_or_tighter` or tighter needs a `why` (D15 §2.2; CRAFT-25). `still` names what does not move, required on any hold of `hold_needs_still_s` or more (D15 R6; CRAFT-26). `eyeline` takes a `dwell_s`; `must_not` holds a look saved for a later beat (D15 R9, R10).
- `moment` items: timed visible changes inside the screen time, no more main actions than `main_actions_per_seconds` allows (TIME-02, TIME-06); `end` is the last picture.
- **Reading floors.** Code works out each shot's **time floor**: speech at the voice's pace (`speech_wps_default` unless the voice differs) plus `speech_floor_extra_s` a speech, or text by `text_floor`, whichever is longer, plus the pause owed, with `turn_reaction_min_s` after a turn. `screen_time` sits at or above it; never type the floor (TIME-01; K08 to K10).
- `held: yes` where meaning depends on not cutting; turn shots count as held (GEN-10).
- The film-level extreme close-up and push-in (the camera travelling toward the subject) are spent only where their RESERVE allows (FILM-08).
- At the main turn at most `departments_changing_at_main_turn_max` departments change, named in `scene_idea` (B3 R7; B1 P11; CRAFT-19). Holding the baseline is a full **department idea**, the scene's one idea for camera, light, staging, sound or design (`holds_baseline`).
- When rules disagree, the higher wins and the `why` names it: what the story states, readability, physical honesty, the film's systems and budgets, flaw handling, turn rules, emotion over continuity, conflict type, beat defaults, the baseline (A1 §6; B1 §11; B2 §7; reference/04).

## Translation menus with pitfalls

Pick at most one per beat; tie it to a line, object or action in this story (A2 §7):
- **A turn inside a person:** the closest size, held (B1 R1). Pitfall: a push-in plus music.
- **A turn about waiting:** a deliberate wide, held on the one waited on (A2 R4, R18).
- **A revelation:** an insert of the evidence, then a held close-up of the receiver (A2 R8).
- **An action turn:** one frame showing the action and its result (A2 R9).
- **A plant:** the same size and length as its neighbours, no push-in (A3 R22).

## Budgets and saved choices

Per scene: `push_in_per_scene_max`, `extreme_close_up_per_scene_max`, `long_pauses_per_scene_max`. Per beat: `signals_changing_per_beat_max`, `added_emphasis_per_beat_max`. Per clip: `acting_characters_per_clip_max`. Film: `extreme_close_up_film_max`, `push_in_scene_share_max`. Caps, never quotas (B1 P5; B4 R23).

## The baseline is a strong answer

"Static, the owner's eye height, a normal lens, room sound are choices, not failures. Depart only for a reason you can cite." A normal shot with no departure may give `because: default` and no `why` (REASON-01).

## Cliché traps

Tests: **any-film** (would this reason fit any film with this theme?), **mood-word** (does it name only a feeling?), **stacking** (more than one signal on one beat?), **sound-off** (does the frame tell the beat without sound?) (B3 R23, R26, §10.1; B1 P11):
- Push-in on every realisation; low angle from the first beat; Dutch tilt for tension; crane-up on every sad ending; shallow focus everywhere (B1 §14).
- God rays, lightning at a revelation, flickering hospital tubes, teal-and-orange (B2 §12).
- Rain on glass, ticking clocks, wilting plants, empty chairs (B3 R24; B4 R25).
- A sad cue under unspoken sadness; dissolves never written (A4 §7.6, §13, T5).
- Glowing eyes and chrome on a creature (B5 §6).
- **Default coverage**, the opposite failure: every scene wide, over-shoulders, singles, or one static frame repeated. Test: do all lists share one shape? Fix: design from the turn (B1 §14; FILM-06).
Fix: the baseline, or this story's own line, object or action.

## Reasons that fail and reasons that pass

- Fails: "Close-up to show her shock." Passes: "The scene's tightest size, spent on its main turn (SC10-B07): 'Her face changes.' puts the change inside her." (B1 R1)
- Fails: "Low angle to make Saye powerful." Passes: "Eye level on Saye (CR-SAYE: she holds power by stillness, not angle); she wins at SC10-B11 by waiting." (B1 R7)
- Fails: `does: horrified`. Passes: `does: chews slowly; stops chewing; a small frown; chews once more, slowly` (D15 R1).

## Two worked examples

### The Catch, scene 10 (tense, 20 shots and a title card)

SH080, the reflection two-shot, both women in one frame (`RC-01`); SH090 and SH100, the ring inserts, edited stills with `flip: never` (K07); SH110, Eli twisting the cap deep in camera A's frame, with no rack focus between planes (B1 R14); SH130, Saye's hand toward the flask, Eli heard off screen; SH150, the turn; SH160, Saye's one look afterwards (A1 R19); SH190, the held wide through the wait, the second turn; SH200, "Nobody leave this room." (line 484); the cut `SC10-C200`, `type: cut_to_black`; SH990, the title card.

### The Long Places, scene 5 (contemplative)

Three shots in about 110 seconds: the mouth at night, wide, static; a static medium through one out-breath of the shaft; the warmth shot, a static profile medium close-up, held, no reverse. "She did not turn her head." (line 79) gets the held frame, and the warmth stays behind her body (D10 §12.3; B1 Ex7, P7).

## Self-check

Yes or no (B1 §13; A2 §9; D15 §8).
1. Is every shot before the turn shot at its size or wider?
2. Is every beat and every line covered?
3. Is every `does` free of emotion words?
4. Is everything that must not move written in `still`?
5. Does every `why` fit only this film?
6. Is every screen time at or above its floor?

## Words for AI models

Works: one camera move and one action per clip, as timed steps with an end state (C3 §5); behaviour, not labels: "She stops chewing. Her eyes lose focus and drift down; her lips part slightly; she holds very still." (C3 §6); "The camera does not move." on a hold (D15 R6); "she listens; no dialogue" for a listener (A1 §11). Fails: emotion words; purposes and reasons in prompt text (GEN-15); parted lips in silence without "No dialogue." (D15 R7).

## Look up for more

`stage.py lib B1 §0`, `B1 §11`, `§13`; `A2 Step 9`, `A2 §7` (R1 to R31); `A3 §5.6`, `R16`, `R22`; `A4 §6.1`, `§6.2`; `D15 §2.2`, `§3`; `C3 §4` to `§6`; `reference/04 Rule order.md`; K05, K07, K08 to K10.
