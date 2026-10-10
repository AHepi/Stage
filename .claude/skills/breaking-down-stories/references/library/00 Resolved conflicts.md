# Resolved conflicts (K01 to K31)

**Example first.** C3 calls the dialogue-through-glass shot "13-04", but the story's thirteenth heading is the glass partition, and the shot C3 describes happens in the eleventh (the treatment floor, morning). Conflict K01 settles it: this pipeline counts scenes in heading order, so the shot belongs to SC11, and `references/library/01 What the codes mean.md` translates every old number. Every row below works the same way: it names the research files that disagreed, says what this pipeline does instead, and says whether the user is asked.

**How to read a row.**

- **Research**: the files and places that disagreed. "B1 R14" is rule 14 of B1's decision rules; "B1 §10.2" is a section; "B1 Ex1" is a worked example; "B1 P11" is a principle. `references/library/01 What the codes mean.md` explains every label, and `references/library/02 Errata.md` lists the research sentences these decisions overrule.
- **Decision**: what the pipeline does. Numbers live in `_config/rules/constants.json` and are named here, never retyped as rules.
- **Asked**: "no" means the decision is fixed. "B item 5" means the user sees it at the big choices (checkpoint B), item 5, with the default shown. A "small choice" is a CHOICE with `asked: no`, listed at checkpoint B under "small choices I made".
- **Where it lives**: the files, fields and checks that carry the decision now.

Worked story values (The Catch) are defaults for that story, not rules for every story. The checks named are those of the checker's list (FORM, ID, CITE and so on).

---

## K01 IDs

- **Research**: C5 §10.1 (ID rules) and C5 E3 (`SC06-SH140`, crew label "6P"); A2, A3, A4, B3, B4, C2 and C5 count the thirty headings in order; A1 §7 writes the recording scene as `scene_id: 07` with a beat `7.4`; B1 and C1 name scenes by what happens in them; B2 §8.5 numbers twenty-three colour-script rows; B3 §2.7 has nine stretches; C3 §22 numbers shots on other scene numbers ("13-04", "09-22"); A2 §8 and §11 write `sc10.B1.a`; A3 §5.9 labels a setup `6C`, A3 §1 a look `IONA-L2`; C1 Recipe 10 writes `S07_03`; C2 §6.6 writes `SC014_SH03` and §5 rule 29 `SC012_SH03_start.png`; C4's previs kit writes `CATCH_SC06_SH14`.
- **Decision**: C5 §10.1. Scenes SC01-SC30 in heading order; beats `SC10-B07`; shots `SC10-SH150` in tens, an added shot between two (`SH155`); the crew letter labels are derived by code and appear only in the shot-list spreadsheet. Code issues or pre-issues every ID. Every research example is mapped once: C3's 13-04 is SC11; 09-22 and 09-15 are SC06; 11-07A, 11-07B and 11-08 are SC07; 14-05A and 14-05B are SC15; 18-31 to 18-33 are SC25; A1's 07 and 7.4 are SC13; C4's `CATCH_SC06_SH14` is `SC06-SH140`. B2's rows become `sub_row` items of the visual plans VS-SQ01 to VS-SQ09.
- **Asked**: no.
- **Where it lives**: ID patterns in `_config/schema/schema.json`; checks ID-01 to ID-09; the full map of old numbers in `references/library/01 What the codes mean.md`.

## K02 How mirrored shots are made

- **Research**: A3 Ex4 (build the world mirrored, "safer for AI"); B1 §10.2 (three methods: flip and compensate, flip the background only, mirror the props, with a decision table); C1 Recipe 8 and C4 §7 (generate normally, flip in the edit); C2 §7.3 and §8 R5 (generate the place empty, flip the plate, add the people unflipped, lettering last); C3 §12 (flip shots with no character; never flip a shot whose left and right carry the plot); B3 R22 and §5.4 (derive the mirrored plan: every x becomes room width minus x, every facing angle θ becomes 180° minus θ).
- **Decision**: one route table, worked out per shot by code: readable text is always a text graphic; the plate route for sided plot details or a large face that must not flip (`plate_route_face_height`); the direct route when every mirrored element is seen in one orientation only; flip with mirrored reference pictures; or flip everything. A3's "build it mirrored" is dropped for generation. B3's coordinate rule stays for previs plans.
- **Later research**: D6 rule 14b follows this table, including the direct route.
- **Asked**: no.
- **Where it lives**: SHOT `route` (derived); card 16; checks SIDE-03 and SIDE-05.

## K03 Era boundaries and frame values (The Catch)

- **Research**: A3 Ex4 (mirrored from the CLACK in scene 6 to Iona's turn in scene 27, a per-scene `frame` flag); B1 §10.2 (phases A, B and C, the third from her second turn); C2 §7.3, followed by B4 and B5 (era C from "RECEIVING ... Reads it again." in scene 28, which leaves the lines between her turn and scene 28 unassigned); C5 §9 E2 and §10 (`frame_handedness` per scene set by a person, handedness per element); C1 Recipe 8 (a mirror column per shot); B2 R21 (flip one lighting convention once, at the first reversal).
- **Decision**: boundaries anchored to story lines in the rule `WR-MIRROR`, whose `era` items are set through SETVALUE records. Era a runs from line 10 to line 261 ("A hard metal CLACK." at line 259; "BLACK." at line 261): `frame: original`, every element `original`. Era b runs from line 263 ("Her eyes open.") to line 1563 ("She fires."): `frame: original`; every world element (places, things, Saye and everyone met there) `reversed` from line 263; Iona, Jude and Eli `original`. Era c runs from line 1565 ("The ship is gone. The stars are gone.") to the end: `frame: reversed`; Iona `reversed` from line 1563 (a STATE change caused by that line); Jude and Eli `original`; world elements still `reversed`. SC06 switches from a to b at line 263; SC27 switches from b to c at line 1565. An element is mirrored on screen when its STATE handedness differs from its scene's frame, so in era b the world is mirrored around the three, and in era c only Jude and Eli are. An earlier design's `frame_handedness: turned` for SC10 is superseded. A side the story states for a mirrored element is an apparent side: "Saye's wedding ring. On her right hand." (line 436) is recorded as her own left, `origin: inferred`, and so is Jude's ring in era c ("His wedding ring. On his right hand.", line 1779). B2 R21's one-time flip is dropped: the main light is written in room terms, and its frame side is worked out per era, so it flips lawfully with the picture at both boundaries.
- **Asked**: B item 5 (as proposed).
- **Where it lives**: `WR-MIRROR` in `06 World and style.md`; STATE `handedness`; SHOT `mirror_state` (derived); check SIDE-04; card 16.

**Worked values for SC10** (era b, frame `original`):

| Element | Handedness (STATE) | Mirror state (derived) | What the picture shows |
|---|---|---|---|
| Iona, Jude, Eli | original | normal | as in era a; Iona's raised hand is her own right, the hand nearest the camera |
| Saye | reversed | mirrored | her own right appears as her left; her ring, on her own left, appears on her right hand, the far hand in the reflection two-shot |
| The kitchen, the mint and the other things of Saye's world | reversed | mirrored | the room is shown reversed; its readable text follows `WR-WORLD-SCREENS` and the text-graphic route |

## K04 Open mirror questions (The Catch)

- **Research**: B1 §10.2 and §16 (recommendations: the Fs as exception props, world screens mirrored, the copied name backwards, world screen text backwards with longer reading time, the scene 6 recording flipped when shown in era b); C2 §7.4 (leaves the F, world screens and the copied name open); A3 Ex4 (asks whether the visor reads backwards); B5 §4.4 (the suit's lettering: "Every word printed on it reads backwards to her"); C3 §13B (visor graphics as edit graphics, orientation not stated).
- **Decision**: B1's recommendations, each a RULE record listing what it governs: `WR-F-EXCEPTION` (the toy carriage's Fs read as scripted), `WR-WORLD-SCREENS` (world screens mirrored in era b), `WR-COPIED-NAME` (the copied "IONA VALE" label backwards), `WR-SCREEN-TEXT-B` (visor, wrist and monitor text backwards in era b, with reading time doubled), `WR-REPLAY` (the SC06 recording flipped when shown in era b), `WR-TITLES` (title cards always read normally).
- **Later research**: D12 §12 and D6 §12 keep the suit's words backwards after her final turn too, because the suit turns with her (B1 §16's "snap readable" is not followed); see `references/library/02 Errata.md`.
- **Asked**: B item 5, grouped (accept).
- **Where it lives**: RULE records in `06 World and style.md`; check SIDE-05; card 17.

## K05 The turn in SC13

- **Research**: A1 Ex3 ("You." is the turning line; stay on Iona, Eli off screen); A2 §12 ("You." inside beat 10; the main turn at beat 15 with a push-in to a "big close-up"); A2 R4 (the tightest size on the main turn); B1 Ex3 (Eli's closest, most frontal framing on "You."; his first glance near the lens on "Now he looks at her."; no push-ins on Eli); B3 §2.7 (the plan tightens toward "You.").
- **Decision**: A2's value analysis. The main turn SC13-B15 carries the scene's one push-in, on Iona, landing at `extreme_close_up`: one use each of the film-level saved choices for the extreme close-up and the push-in, and the film's tightest size, which K12 places in SC13. On "You." the cut lands on Iona, where A1 and A2 agree. Eli's closest single so far is `close_up`, one step wider; his glance near the lens (a saved choice) is spent on "Now he looks at her."; `CR-ELI` forbids push-ins on him and sets `limit_before: medium_close_up` until SC13.
- **Later research**: D7 §14 item 1 reaches the same reading ("You." is a reveal inside beat 10). D16 §12 item 2 proposed stopping SC13 at a close-up; the declared peak in K12 answers it instead.
- **Asked**: no.
- **Where it lives**: `CR-ELI`, RESERVE records and PLAN `peak` in the film rules; checks CRAFT-01 to CRAFT-03, FILM-01, FILM-03, FILM-08.

## K06 Where everyone stands in SC13

- **Research**: A1 R39 and Ex3 (Iona on the left looking right, Eli on the right looking left, the monitor behind Eli); A2 §12 (an assumed row, left to right Iona, Jude, Eli); A3 Ex3 (Iona's single faces frame-left); B1 Ex3 (the monitor on Saye's side of the glass, turned to face it); B3 §8.6 and Ex2 (a floor plan built and checked in Blender: Jude in bed as the pivot, the row facing the monitor).
- **Decision**: B3's tested floor plan is the place's set plan. Every eyeline is worked out from it by code, and that replaces the text of A1, A2 and A3 in the cards. The scene keeps its note "staging assumed".
- **Later research**: D7 §14 item 3 follows B3's row order.
- **Asked**: no.
- **Where it lives**: LOCATION set plan in `08 Places and things.md`; check GEOM-01; card 12.

## K07 Reflection two-shots and rings (SC10, SC29)

- **Research**: B1 Ex6 and B3 §8.2 (camera along the glass, level, 85 millimetres from well back, profiles at the frame edges, ringed hands nearest the camera); B3 §8.3 and §8.8 (a separate hands-on-glass ladder for SC29, which keeps SC10's raised hands out of it); A2 §11 (SC10's ring inserts should match the SC29 hands "in lens and angle"); C1 §11 Example 8 (the SC29 rings from a checked still, little motion); C3 §12 and §19 (never flip a shot whose left and right carry the plot); B5 §10.2 (Jude's era c state line written in image sides); B1 §9.2 (the lens family holds 85 millimetres back until the confession).
- **Decision**: B1's and B3's geometry for both reflection two-shots, as the saved choice `RC-01` (at most two uses: SC10 camera A and SC29); SC10's 85 millimetre lens is the lens exception `LX-01`. The SC29 hands insert follows B3's ladder; A2's rhyme moves to the two reflection two-shots (PLANT `rhyme`). State lines use own sides; "hand nearest the camera" goes in behaviour text; image sides are worked out by code; ring inserts are edited stills with `flip: never`.
- **Asked**: small choice.
- **Where it lives**: `RC-01`, `LX-01` in `10 Film rules.md`; checks SIDE-01 to SIDE-03, FILM-02, CRAFT-07, CRAFT-11.

## K08 Words per clip

- **Research**: A1 §11 (McKee's 2 to 3 words a second, so 16 to 24 words in 8 seconds); A2 Step 9 and §15 (words divided by 2.5, plus half a second; slower for weighted speakers such as Saye); A4 AI5 (split past about 15 to 17 words in 8 seconds); C3 R8 (at most 2.5 words a second, one speaker change per 3 seconds); C5 §6.6 check 5 (at most 2.5 words a second).
- **Decision**: the sum over a clip's speeches of words divided by pace stays within the clip length less a margin (`clip_speech_rule`); the default pace is `speech_wps_default`, and each VOICE may set `pace_wps` (Saye speaks slower). A1's 16 to 24 words is retired.
- **Asked**: no.
- **Where it lives**: `_config/rules/constants.json`; checks GEN-03, TIME-01.

## K09 Reading time for text and inserts

- **Research**: A1 R20 (a planted fact gets a clear shot held about 1 to 2 seconds); A3 R22 (a buried plant matches its neighbours); A4 R8 and §6.1 (an insert about a second, a face about 1.5, text read at no more than 12 to 15 characters a second, doubled when mirrored); B1 R2 (at least 2 seconds plus about half a second a word, long enough to read twice). For the tag "Goods only. No persons." they give from about 2 to about 4 seconds.
- **Decision**: one formula, `text_floor`: the larger of its minimum and a base plus characters divided by the reading rate; plot-critical text (emphasis 2 or more) gets B1's read-twice floor; mirrored text doubles. "Goods only. No persons." needs 4.0 seconds, 8.0 mirrored. Inserts without text follow their emphasis.
- **Later research**: D12 §12 compares its design targets with this floor; the floor is the enforced minimum.
- **Asked**: no.
- **Where it lives**: `text_floor` in `_config/rules/constants.json`; check TIME-01.

## K10 Pauses, holds and handles

- **Research**: A1 R15 (pauses short, medium or long, at most two long ones per scene); A2 Step 9 ("(beat)" about a second; "Silence." or "She waits." 2 to 3 seconds; "a long moment" 3 to 4; a turning point's reaction at least 2); A4 §6.1 (shot length by beat intensity) and §10 (handles of 0.75 seconds); C5 R15 (handles of half a second to a second).
- **Decision**: A2's dialogue length is a floor for each speech; A4's table sets shots without dialogue and where cuts fall. Pause tiers are half-open ranges with no gaps (`pause_tiers`): short, medium and long, and anything longer is a `hold` that needs a saved choice. The long tier starts where A2's "Silence." starts, not at A1's 3 seconds, so no length is left unnamed. At most `long_pauses_per_scene_max` long pauses per scene; a turn's reaction lasts at least `turn_reaction_min_s`; handles are `handles_s`.
- **Asked**: no.
- **Where it lives**: `_config/rules/constants.json`; checks TIME-01, TIME-04, TIME-05, TIME-08.

## K11 How loud a plant may be

- **Research**: A1 R20 (one clear, unemphatic insert or single); A3 R22 (a buried plant matches its neighbours' size, length and framing); A4 S5 (one clear, calm shot); B4 R6 (plants at emphasis 0 or 1, in context).
- **Decision**: B4's emphasis ladder is the only scale. Quiet plants (emphasis 0 or 1) match their neighbours, as A3 R22 says; a plant that is itself a plot event may reach 2, with nothing pointing forward (A1's clear insert). PLANT `plot_event` marks which plants those are.
- **Asked**: no.
- **Where it lives**: `plant_emphasis_max`; check CRAFT-08; card 07.

## K12 Climax and peaks (The Catch)

- **Research**: B3 §2.7 (SC26 and SC27, the ledge and the crossing, the film's only intensity 10, played in counterpoint); B1 §9.2 (the camera's break on the ship's ledge); B4 §15 question 9 (the largest payoff is the figure's chest opening, SC25); B5 §10.1 (Iona's arc turns when she deletes the way home, SC24); B2 §8.5 (saturation and red-green contrast peak at the fire, row 18, SC24); A2 R31 and A4 §6.9 (the tightest size and longest hold kept for "the climax" without naming it).
- **Decision**: PLAN names `crisis` and `climax` separately. Default: crisis SC24 ("She deletes the way home.", line 1412); climax SC26-SC27 (the crossing; the film's one scene intensity 10, played in counterpoint). Peaks: colour saturation and red-green contrast at the SC24 fire; the largest motif payoff at SC25 (the chest opens); the camera's break at SC26 ("She pushes gently away from the rail."); the sound rupture at SC26 (the ship's hum drops out); the longest hold and the only sound emphasis 3 on SC30's last shot (the pump over black); the tightest size in SC13, declared as `peak: tightest_size | scene: SC13 | reason: the confession's turn lands inside Iona; the climax is played wide and still, in counterpoint`. The ladder rises by size and hold together. The SC24 and SC25 readings are shown beside the default.
- **Later research**: D16 §8 and §12 recommend the same climax and relabel B2's "climax" wording as the crisis peak.
- **Asked**: B item 1 (SC26 to SC27).
- **Where it lives**: PLAN in `05 Story plan.md`; LADDER; checks PLAN-01, PLAN-03, FILM-01.

## K13 Sequences

- **Research**: B2 §8.5 (twenty-three colour-script rows); B3 §2.7 (nine stretches); A3 §1 (a sequence is scenes playing as one action, with one direction of travel); C5 §6.9 (the one-line shot list approved per sequence).
- **Decision**: one list, made at step 2. Default for The Catch: B3's nine stretches as SQ01 to SQ09 (SC01-SC05, SC06, SC07-SC10, SC11-SC13, SC14-SC17, SC18-SC22, SC23-SC25, SC26-SC27, SC28-SC30). B2's rows are `sub_row` items of the VISUAL records.
- **Later research**: D16 §12 item 5 notes A3's "scenes 1 to 7 are one rescue" differs from SQ01; the direction of travel stays a rule over those scenes.
- **Asked**: no.
- **Where it lives**: SEQUENCE and VISUAL records; check COVER-06.

## K14 Scales

- **Research**: A2 §6 Step 6 (beat intensity 1 to 5 within a scene); B3 §0.1 and §2.7 (story intensity 1 to 10 across the film, one 10, never converted); B2 §8 (frame value and saturation 1 to 5); B4 §3.4 (emphasis L0 to L3 for things, S0 to S3 for sounds); B1 P11 (one "emphasis device" per beat) against B4 R23 (one "added signal"); C4 §9 and §4.4 (previs levels 0 to 5, with a 1b; stand-in detail 1 to 5).
- **Decision**: separate names and ranges, never converted: `beat_intensity`, `scene_intensity`, `emphasis`, `sound_emphasis`, `frame_value`, `saturation`, `previs_level`, `standin_level` (ranges in `scales`). B1's device and B4's added signal merge into `added_emphasis`, 0 or 1 per beat.
- **Asked**: no.
- **Where it lives**: `scales` and `added_emphasis_per_beat_max` in `_config/rules/constants.json`; checks CRAFT-05, CRAFT-09, CRAFT-10.

## K15 Speech syntax for Veo

- **Research**: A1 §11 (Google's October 2025 guide: speech in quotation marks); A4 §7.8 (a sound line with quoted speech); C3 §2B, §7A and §16 (September 2026 documents: Veo and Omni in colon form without quotes, because quotes can be drawn as text; Kling, Wan and LTX quoted).
- **Decision**: speaker syntax per model adapter: Veo and Omni colon form without quotes; Kling, Wan and LTX quoted. The freshness rule forces a re-check before a paid batch.
- **Asked**: no.
- **Where it lives**: `_config/adapters/video_models.json`; checks GEN-09, GEN-11.

## K16 Voices

- **Research**: C1 R1 (voice first: record or make every line with a fixed voice, then use models that take audio); C3 §7B and §19 (a pasted voice description in every clip; a separate voice and lip sync only if voices drift); A4 §7.8 (native audio, or a voice model plus lip sync); A1 R1 and A2 R27 (lines the listener carries play off screen).
- **Decision**: voices first for every recurring speaker, one locked voice each; voices generated inside a clip only for drafts and one-line parts; off-screen delivery wherever A1 and A2 choose the listener.
- **Later research**: D3 (voice design, paths, consent, lip-sync routes) builds on this.
- **Asked**: no.
- **Where it lives**: VOICE records; `_config/adapters/audio_models.json`; card 06.

## K17 Readable text

- **Research**: C2 P4, §5 rule 9 and §7.1, C1 R6, C4 §6 Route 5 and B4 §14.2 (exact text is always a composited graphic); A3 R11 (composite unless too small to read); C3 R11 and Ex3 (a sign of three words or fewer may be generated forwards, then flipped).
- **Decision**: all readable text is composited from text graphics; models draw only illegible background text. A quoted sign in a prompt is an error.
- **Later research**: D12 (text graphics made by script) and D6 (composites).
- **Asked**: no.
- **Where it lives**: TEXT records; `make_text_graphics.py`; check GEN-06; card 17.

## K18 Negation and glass wording

- **Research**: C2 §6.3 (location prompts with "No people, no text"); B2 §8.2 (write swatch prompts in positive terms, because models add what a prompt names); C3 §21 linter item L14 (no negation of a visible thing except documented "No ..." lines); B3 R29 (clear glass has no reflections, keep the camera's side darker); C1 §9 and C2 §9 ("faint reflections").
- **Decision**: exclusions go to a negative field where the model has one, otherwise only the documented "No ..." lines; never "no people" in picture prompts. Glass wording follows the glass state: clear glass is "seen through perfectly clear glass; the room on the camera's side is dark"; reflecting glass uses B3's reflection phrase.
- **Asked**: no.
- **Where it lives**: `_config/adapters/phrasebook.json`; check GEN-07.

## K19 "Torch" and the light side in the SC01 bolt-hole insert

- **Research**: B2 Ex1 (the flashlight enters from frame-right; B2 §0.1 writes "flashlight" in prompts, because "torch" draws a flame); B1 §15 (Example 1's prompt: "torchlight from the left"); C1's test prompt and C3 §22.0's look block for the cage both say "torch".
- **Decision**: `prompt_words` swaps "torch" for "flashlight" in every compiled prompt; quotes of the script keep "torch". The insert takes B2's main-light side (frame-right). B1's example is corrected in `references/library/02 Errata.md`.
- **Asked**: no.
- **Where it lives**: PROJECT `prompt_words`; `_config/rules/words.json`; check GEN-12; card 11.

## K20 The SC06 fall

- **Research**: A4 Worked examples 1 and 2 (about 12 seconds of expanded screen time from "The cage falls." to the CLACK, against "the long second" in real time on the SC13 recording); B1 §10.1 and Ex2 (no slow motion; the fall in real time; the yellow stripe grows shot by shot as the clock); C4 §12 Example A and the kit's cage-fall plan (the physical fall keyed from 4.9 t², about 1.2 seconds).
- **Decision**: expanded screen time built from overlapping real-time slices, never slow motion. One master previs `PV-SC06-MASTER` of the physical fall (height falls as `free_fall_half_g` times t²); each shot's `time_slice` names its frames; overlaps are allowed; the yellow stripe never shrinks in frame across the fall shots (a review question on SC06). Stated in the camera system (`CAMSYS.time_rule`).
- **Later research**: D11 §3.2 and §10 item 1 work out the slices and propose timings for A4's rows.
- **Asked**: small choice (named in B item 7).
- **Where it lives**: CAMSYS `time_rule`; SHOT `time_slice`; card 15.

## K21 The camera when the chest opens (SC25)

- **Research**: C4 §12 Example C and `plan_chest_opens.json` (over Iona's right shoulder at 35 millimetres, a slow push to 50); B1 Ex5 (35 millimetres looking up, a motivated tilt down, a macro of the animal, then a static 50 on Iona); B4 §9 M17, §14 and R23 (medium close, camera still, no added signal because the script already marks the beat); C3 Ex4 (start and end pictures).
- **Decision**: B1 and B4: static 35 millimetres looking up, a motivated tilt down, the vessel by a macro insert, then static 50 on Iona; no push-in. `plan_chest_opens.json` is fixed to match.
- **Asked**: no.
- **Where it lives**: the scene's shots; `tools/previs/plans/plan_chest_opens.json`; check CRAFT-10.

## K22 SC10 staging

- **Research**: B3 Ex1 and §6.3 (camera A at 85 millimetres from about 6.3 metres on the table's axis; Iona sets the lamp down before the raised hands; Eli deep in the same frame); A2 §11 (beat 5 with Saye in the foreground); B1 §9.2 (no 85 before SC13).
- **Decision**: default is B3's tested version: camera A 6.3 metres back on the table's axis at 85 millimetres under `LX-01`; Iona sets the lamp down before the raised hands, an invention listed for keep or cut; Eli small and deep in the centre. Option b is A2's version with Saye in the foreground. Shown again at checkpoint C for SQ03.
- **Asked**: small choice.
- **Where it lives**: LOCATION `LOC-SAYE-KITCHEN` set plan; the gold scene in `references/examples/`.

## K23 Previs formats

- **Research**: B3 §6.3 and §6.4 (a scene-level plan and `plan_to_blender.py`, tested on bpy 5.0.1); C4 §5 and §8 (per-shot plans, `facing_deg`, animated cameras, bpy 5.2.2 on Blender's long-term release).
- **Decision**: C4's per-shot schema is canonical. B3's scene plan becomes the LOCATION set plan, compiled per shot by `make_previs_plans.py` (tested on bpy 5.0.1 here; C4's 5.2.2 long-term release is the target). B3's `plan_to_blender.py` is retired. The render size follows the frame shape.
- **Asked**: no.
- **Where it lives**: `tools/stage_tools/make_previs_plans.py`; `tools/previs/`; card 22.

## K24 Frame shape

- **Research**: B1 §5 and §16 (2.39:1; from 16:9, keep heads, hands and text out of the top and bottom eighths); B3 and C5 examples at 2.39; C1 §5 (Seedance at 21:9); C2 §2.3 and §5 rule 25 (GPT Image at 2560 × 1072, bars drawn on storyboards); C3 §22 examples at 16:9; C4 §5 (renders at 1280 × 720).
- **Decision**: chosen once; default 2.39:1. Worked out from it: storyboard bars; the generation size per tool (Seedance 21:9; GPT Image 2560 × 1072; other 16:9 sources with heads, hands and text kept out of the top and bottom eighths); previs at `previs_width_px` wide with the matching height.
- **Asked**: B item 2 (2.39).
- **Where it lives**: PROJECT `frame_shape`; the adapters; card 21.

## K25 Runtime (The Catch)

- **Research**: A3 §5.2 (about 42 to 44 pages, 40 minutes or more at a page a minute); C1 §10 (costs for a 20-minute short); C2 §3.7 (about 300 shots, 120 of them to video); A2 §11 and §12, A4 §11 (19 to 36 shots in single scenes).
- **Decision**: the first estimate at checkpoint A: 1,926 to 2,309 seconds (D2 §6, D13 §4.1), told to the user as "about 35 minutes (32 to 38; the page count suggests up to 44)"; the 44 is A3's page count, not the estimate. C1's 20-minute costs scale by about 1.75. The estimate from the shots follows at step 10. The user keeps the full length or gives a target (a compression plan at step 2; lines never rewritten).
- **Asked**: checkpoint A, its one question (keep everything).
- **Where it lives**: PROJECT `runtime_target_s`; `estimate.py`; `v0_action_seconds_per_word`.

## K26 States, sides and fixed descriptions (The Catch)

- **Research**: A3 §5.4 (looks `IONA-L1` to `L5`); B5 §10 (costume phases C1 to C6, state lines, and sides); C2 §6.1 and §8 R2 (states S1 to S6; a look line of 25 to 40 words, whose example carries the ring); C5 §5 R6 and §9 E2, E3 (state IDs such as `CH-IONA.S03`); B4 §15 question 1 and B5 §10.1 (Iona's torn sleeve and palm on her right); C2 §8 R4, §9 and §10 W2 (a left sleeve and a left-shoulder wound in example phrases); B5 §10.2 (Jude's wound on his right, from the ringed "good hand"); C3 §22.0 (the figure about 2.5 metres, Saye "late fifties", a grey blanket).
- **Decision**: C5's state IDs, with boundaries from continuity; B5 is the source of fixed descriptions; rings and wounds go in state lines, never in fixed descriptions; C3's example descriptions are replaced. Defaults: Iona's torn sleeve and skinned palm on her own right; Jude's wound on his own right shoulder (inferred from the ringed "good hand"); Eli's half-smile and parting on his own left, his one shoe on the right foot; the figure 2.4 metres; Saye "fifties" (story); the blanket "OSTREL, stitched on it in blue" (story), made dark navy (design choice). Casting types stay `open` until pictures exist. Lengths: `fixed_description_words`.
- **Asked**: small choices.
- **Where it lives**: CHARACTER, PROP and STATE records; checks STATE-01, SIDE-01, SIDE-02, WORDS-05; card 05.

## K27 Place and time (The Catch)

- **Research**: C3 §22.0 (British accents for every voice); B2 R19 (British blue emergency lights as the example); B3 §8.5 (the car layout depends on the driving side); A3 §10 (the period written `unstated` when the story does not fix it).
- **Decision**: a WORLD record: an unnamed British city, present day, driving on the left, British English voices, each marked `inferred` (from "torch", "night bus" and "I know how a lift works"). Voices stay `draft` until answered.
- **Later research**: D17 (options, primary sources, and the near-future question for the user).
- **Asked**: B item 3.
- **Where it lives**: WORLD in `06 World and style.md`; VOICE `status`; card 08.

## K28 Data conventions

- **Research**: A1 to A4 fill-in templates in YAML; C5 R29 (lowercase snake_case values, compared ignoring case) and C5 §10 (JSON, `none` for empty); C1 Recipe 10 and C2 §6.6 use null; C2 §7.3 and B3 §8 write values in capitals (NORMAL, MIRRORED, CLEAR); A2 and A4 values contain spaces and hyphens; A1 and A2 write actions as -ing words, A3 as infinitives.
- **Decision**: the record text of the pipeline; lowercase snake_case values compared ignoring case; `none`, never null; `yes` and `no`; one -ing field named `tactic`; A3's infinitives converted.
- **Asked**: no.
- **Where it lives**: `references/formats/01 Record format.md`; `_config/schema/schema.json`; checks FORM-04, FORM-13.

## K29 Model routing

- **Research**: C1 §9 (the same model for every shot of one scene, against character drift), against C1 §5 and C3 §22, which choose a model shot by shot; C1 §3C and C3 §0's fact-check note on which LTX versions have camera add-ons; C4 R14 (render the previs at 16 frames a second for Wan, or retime afterwards).
- **Decision**: one scene model by default; overrides for single shots are logged with their reason and followed by drift questions; control of open models is tested once, and the working route is written into the adapter.
- **Later research**: D8 §10 item 3 settles the frame-rate question by frame count.
- **Asked**: no.
- **Where it lives**: SHOT `scene_model` and `model`; `_config/adapters/routing.json`.

## K30 Slow motion

- **Research**: B1 §9.2 and §10.1 (slow motion banned in The Catch; the fall plays in real time); C1 §9 (generate fast action slowly, then speed it up); A4 P10 (slow motion is a strong device with a budget).
- **Decision**: slow generation only as a technique whose playback is real time, logged as a `speed` finishing job; slow playback is banned in The Catch's camera system.
- **Later research**: D11 R15 and §10 item 2 agree; D10 lists slow motion among the budgeted devices.
- **Asked**: no.
- **Where it lives**: CAMSYS; FINISH jobs; check CRAFT-16.

## K31 Music (The Catch)

- **Research**: A4 §7.6 and §15 (no music or very sparse, the user decides); C3 R10 (music kept out of every clip, score added in the edit); A1 §9 (save score for transitions or counterpoint); B4 §9 M10 (the pump over black at the end of SC30 is "the only S3 of the film").
- **Decision**: every clip is music-free. The film's policy is the user's: default `none` for The Catch, so the pump is the only sound to reach sound emphasis 3.
- **Later research**: D9 §4.1 and §10 (the same default, and the options `sparse` and end credits only).
- **Asked**: B item 4 (none).
- **Where it lives**: SOUNDPLAN `music_policy`; MUSIC records; card 13.
