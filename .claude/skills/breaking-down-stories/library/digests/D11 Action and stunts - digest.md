# Digest D11: Action, stunts and physical set pieces for AI (28 Sept 2026)

Source: `research/D11_action_stunts_design.md` (fact-checked 28 Sept 2026). Brackets: R# = the file's decision rule; P# = principle; WE# = worked example; § = section. "C4 rule 42" and "C5 rule 31" are rules in those files' digests. **[V]** primary or named page read 27-28 Sept 2026; **[U]** unverified; **[J]** judgment. The blueprint (7.2, card 15, K20) already uses this file under its own field names; the blueprint's names win (section 3 below). Re-check tool limits and prices after 28 Oct 2026.

## 1. Scope

1. Turns any physical passage (fall, strike, climb, push, carry, weightlessness, a "fast" move) into an action beat map and an action score: cause, effect, anchor, direction, camera mount, story time, screen time, clip, previs level, content risk.
2. Gives one method for stretching a moment without slow motion (overlapping real-time slices around clock shots) and settles the A4/B1/C4 conflict on *The Catch*'s SC06 fall (blueprint K20).
3. Says how to rehearse and capture choreography safely at home and how to cover action with short, chained AI clips; worked on SC02, SC05, SC06, SC23, SC26-27 and *The Long Places* ch. II.

## 2. Rules

**Principles** [§1]
1. [P1] If a passage is action, then treat it as a scene (physical goal, escalating obstacles, at least one reversal, a changed situation), because Chan's rules say the same: "Start with a **disadvantage**", "Use the **environment**", "Earn your **finish**" [V].
2. [P2] If a cut would leave the viewer unsure where the bodies are, then add a master or anchor shot, because Bordwell's first lesson is "go for clarity in every way" and the failure is "too many close views, too few master shots" [V].
3. [P6] If the audience can measure something (a wall streaming past, a growing stripe, a speed read-out), then it follows real physics; what nothing measures may be held [J].
4. [P7] If a clip carries action, then one acting body, one main action per 4-5 s, a simple camera, because in FilmBench action scenes cut camera-movement scores by 31.1 points [V].
5. [P8] If a stunt must be rehearsed, then mime it on a phone, never perform it, because even professional stuntvis is made in "a created space with pads and boxes" [V].

**Design** [§2]
6. [R1] If D10 `set_piece` is `chase` or `fight`, or the passage contains a fall, strike, climb, carry, push, throw, weightlessness or a "fast" move, then make a beat map before shot design, because models fail most here and durations cannot be guessed. SC02 and SC06 enter by the second clause [J].
7. [R2] If writing a beat, then state cause and effect as two visible events; if a take shows the effect first, then split them into two shots, because Runway says "effects sometimes precede causes" [V].
8. [R3] If a set piece has no reversal, then mark the one the text implies (a habit, a hope, a false relief), because action without reversal reads as a stunt reel [J].
9. [R4] If a beat must fail, then make the failure the described action, early, with a failed end state, because "actions disproportionately succeed" (Runway) [V; C3 R14].
10. [R5] If the danger comes from the place, then keep that anchor in frame at the cause, because the place is both obstacle and map.

**Geography** [§2]
11. [R6] If a set piece moves through space, then show its geography calmly first (A4 C6) and write one travel direction into every prompt (A4 C5), because it cannot be learned in a rush and models forget direction.
12. [R7] If cuts are under about 1.5 s [J], then keep the point of interest where the eye already is (centre by default), because *Fury Road* kept information "in one spot…the Center of the Frame" [V].
13. [R8] If a shot is wide, then hold it longer than a close one, because "More distant shots should be held longer than closer ones" (Bordwell) [V].

**Cutting** [§2]
14. [R9] If cutting away from a movement, then let it reach a point of rest "if only for a couple of frames"; if cutting to another angle of the same movement, then cut mid-movement with the whole movement in both clips (A4 R3).
15. [R10] If one impact must land harder, then use one axial overlap per set piece: cut straight in and repeat 2-4 frames, both shots at real speed, because Bordwell's axial cut works, but his example also slows the repeat ("slightly repeated and slowed"), which B1 bans in *The Catch* [V; J on the count].
16. [R11] If action and reaction can share a frame without touching, then keep them together (Chan's rule 4); if they touch, then split them (R20).
17. [R28] If a strike, shove or trip must look as if it lands, then build it from angle (the strike crossing toward or past camera), reaction (its own clip) and sound (the impact only in the mix), because "Angle + reaction + sound together make the missing punch land" [V, secondary] and it keeps one body per clip.

**Time** [§2, §3]
18. [R12] If summed reading minimums (A4 R8) exceed story time, then `overlapping_slices`; if the danger is a wait, then `held_real_time`; if the action is long and repetitive, then `elliptical`; otherwise `real_time_continuous`; `slow_motion` only where the camera system allows, because reading need against story time decides it [J].
19. [R13] If using overlapping slices, then play every shot at real speed, move every clock forward, hold only clockless shots, and let clock-shot slices cover the real duration about once; a shot showing a clock and a face together is a clock shot, because the audience can measure only clocks [J].
20. [§3.2 item 4] If two different clock objects overlap in story time, then keep the overlap at 0.3 s or less; the same object never goes backwards, because viewers cannot compare speeds across different views [J].
21. [R14] If screen time exceeds about 3× story time, then keep it for a turning point and, where possible, replay the event at true speed later, because a big stretch reads as subjective [J].
22. [R15] If a movement is fast, then prompt "in slow motion, half speed", generate twice the used length and speed it up 2× in the edit, because fast motion smears (C1 §9; B1 §6.1). Never write "slowly" when anything falls, pours or flaps in frame, because after 2× it looks like four times gravity [J].
23. [R16] If a clock is physical, then compute it: distance = 4.9 × t² m; speed = 9.8 × t m/s; time to fall h m = √(h ÷ 4.9) s [V], because eye-guesses run long [J] and eased keys float (C4 R10).

**Camera** [§2]
24. [R17] If physics is impossible or extreme, then the camera obeys the characters' physics (B1 R23) and changes mount only on a hidden cut or as B1's one "break", because a mount change is an event.
25. [R18] If a clip carries the action, then no camera move, or one move caused by the body (rule 4).

**AI coverage** [§2]
26. [R19] If a continuous action needs several angles, then design one shot or a chain (A3 R16); chain last frame to first only inside one continuous action and re-attach identity references each link, because last-frame chaining "degraded quality" (MovieDreamer, via C5) [V].
27. [R20] If bodies touch in one shot, then (a) one acting body per clip, first; (b) Route 2 depth per body and composite (C4 rule 42); or (c) Seedance 2.5 with a clay reference, budgeting double takes, because ByteDance names "the stability of scenes involving interactions among multiple subjects" as a weakness [V].
28. [R21] If hands carry the beat, then give them their own insert from a checked still, one grip, contact named (C3 §13C), and keep hands small in wides.
29. [R22] If more than about 3 s of an action clip is used, then it needs one main action and an end state, else split (C3 R2).
30. [R23] If a set piece has weapons, wounds or blood, then rate each beat's risk and apply C1 R9 (cause, reaction, aftermath separate; impact off-screen; flashes and blood composited; gunshots in the mix), because filters block injury; after two refusals, move the element to compositing or sound (C1 R10).

**Capture and previs** [§2]
31. [R24] If a performance matters (reach, pull, shove, flinch), then mime-capture it: phone locked off, whole body, plain background, one performer (C4 Rec7; D15 §5), because capture gives timing text cannot (C1 R12).
32. [R25] If a move involves height, speed, impact, falling, weightlessness or striking someone, then never perform it: hand-key, use Cascadeur, or mime a slow grounded version and retime, because home capture has no stunt safety [J].
33. [R26] If a reference video is a model input, then use footage you shot or have rights to, because the model copies it closely (D4) [J].
34. [R27] If choosing `previs_level`, then 0 for faces and inserts; 2 for exact geography or a withholding frame; 3 for falls, zero gravity and (this file's extension) three touching bodies; 4 for physical acting (C4 §9); record it per beat.

## 3. Breakdown fields

Blueprint names first (they win); D11's own proposals, not yet in the schema, after the line.

| level | field_name | meaning | allowed values / example |
|---|---|---|---|
| scene | `time_treatment` (D11: `time_design`) | how screen time relates to story time | `real_time_continuous` \| `held_real_time` \| `overlapping_slices` \| `elliptical` \| `slow_motion` (only where the camera system allows) |
| scene | `geography` (D11: `geography_anchors`, `travel_direction`) | where things are; the fixed direction | text: "control box NW; gate E; travel down; wall streams up in frame" |
| scene | `cause_chain` | the causes and effects in order | text: "shriek → cage falls → bodies lift → grip slips → CLACK" |
| scene | `escalation` | how danger grows | text |
| scene | `reversal` (D11: `reversals[]`) | beats that flip fortune | beat ids: `SC06-B12` |
| scene | `action_score` | the choreography table | text block, one row per count (section 4) |
| scene | `coverage` | how the scene is covered | `designed` \| `chained` \| `master_and_coverage` \| `oner` |
| shot | `time_slice` (D11: `story_time_s`) | master-previs frames a clock shot covers; frame = 12 + 24 × t | `PV-SC06-MASTER-V01 \| frames: 22-30` |
| shot | `motion` | a physical move the free-fall helper keys | `free_fall \| object: cage_floor \| from_z: 9.2 \| to_z: 2.53 \| start_frame: 1` |
| shot | `start` (D11: `join_in: chain_from_<id>`) | how it opens | text \| `from_end_of: SC06-SH150` |
| shot | `route` | how to make it | `start_picture` (D11 image_to_video) \| `start_end_pictures` (first_last_frame) \| `guide_video` (route_2/3) \| `performance_transfer` (mime_mocap) \| `composite_only` (route_5/edit_only) \| others |
| shot | `previs_level` | C4 rung | 0-5 (write C4's 1b as 1) |
| shot | `moment` (D11/D15: `behavior`) | timed visible steps | `0-0.5 \| shows: her fingers slide along the bar` |
| — | — | *D11 proposals below* | — |
| scene | `physical_goal` | the physical result wanted | "get three people out of the shaft" |
| scene | `story_duration_s`, `screen_duration_s`, `reading_budget_s` | physics time; watched time; reading need | 1.17; 11.57; the sum of A4 R8 minimums for the passage |
| scene | `clocks[]` | what measures time, and its law | `free_fall` \| `constant_speed` \| `text_given` \| `none` |
| scene | `device_budget` | axial overlaps and mount changes allowed | 0 or 1 each |
| beat | `beat_type` | the beat's job | `setup` \| `attempt` \| `obstacle` \| `escalation` \| `reversal` \| `near_miss` \| `release` \| `aftermath` |
| beat | `anchor`, `clock_shown` | orienting object; visible clock | anchor id \| `none`; clock id \| `none` |
| beat | `attention_in`, `attention_out` | where the eye is at first/last frame | `top_left` … `center` (default) … `bottom_right` |
| beat | `contact` | bodies touching | `none` \| `body_object` \| `two_bodies` \| `three_plus_bodies` |
| beat | `capture` | source of the motion | `none` \| `hand_keyed` \| `cascadeur` \| `mime_mocap` \| `motion_transfer` \| `own_reference_video` |
| beat | `speed_trick` | half-speed generation, doubled | `none` \| `generate_half_speed_x2` |
| beat | `join_in` | join to the previous shot | `cut` \| `match_on_action` \| `hidden_cut` \| `chain_from_<id>` \| `axial_overlap_<frames>` |
| beat | `content_risk`, `risk_method` | filter risk; handling | `none` \| `low` \| `medium` \| `high`; `split_cause_reaction_aftermath` \| `offscreen_impact` \| `composite` \| `sound_only` \| `neutral_wording` \| `none` |
| beat | `safety` | what the performer must not do | "mime only, no hanging" |

A proposal field enters only through the schema, with a reason (builder rule 2).

## 4. Procedures

**Procedure A: beat map from a passage (20-40 minutes per set piece)** [§6 Recipe A]
1. Give the LLM the scene text with line numbers, the B3 floor plan and anchors, and B1's camera system.
2. Say: *"List every physical beat in this passage as cause → effect, quoting the exact words. Mark each beat_type. Name the reversals. If there is no reversal, say which line implies one."*
3. Say: *"For each beat, name the anchor in frame, the screen direction and the camera mount from B1. Flag any beat where two or more bodies touch."*
4. Say: *"Compute the story duration from physics (distance = 4.9 × t²) or from the text. Sum A4 R8's reading minimums. Choose time_design by D11 R12 and explain in one line."*
5. Fill the beat map and write the action score (templates below).
6. Run the checklists (section 5).

Template, beat map (§4.1, exact):

```yaml
action_design:                  # only if R1 applies (set_piece chase or fight, or a physical passage)
  set_piece: <D10 value>
  physical_goal: "<who wants what physical result>"
  time_design: <see §5>
  story_duration_s: <from physics (R16) or the text>
  screen_duration_s: <sum of beat durations>
  reading_budget_s: <sum of A4 R8 minimums>
  clocks: [{id: clk_stripe, what: "the yellow stripe", law: free_fall}]
  geography_anchors: [<B3 anchor ids>]
  travel_direction: "up = frame top"
  reversals: [<beat ids>]
  device_budget: {axial_overlap: 0, mount_change: 1}
  beats:
    - id: SC06-AB15
      text: "<exact quote>"
      beat_type: <see §5>
      cause: "<visible event or beat id>"
      effect: "<visible change>"
      anchor: <anchor id | none>
      screen_direction: <A4 values>
      camera_mount: <B1 values: world | bolted_to_cage | bolted_to_ship | attached_to_iona | handheld>
      story_time_s: [<start>, <end>]
      clock_shown: <clock id | none>
      duration_s: <screen seconds used>
      attention_in: <grid cell>
      attention_out: <grid cell>
      contact: <see §5>
      capture: <see §5>
      previs_level: <C4: 0 | 1 | 1b | 2 | 3 | 4 | 5>
      route: <image_to_video | first_last_frame | route_1 | route_2 | route_3 | route_5 | edit_only>
      speed_trick: <see §5>
      join_in: <see §5>
      content_risk: <see §5>
      risk_method: <see §5>
      safety: "<capture limit, e.g. mime only, no hanging>"
```

Values are lowercase `snake_case` (C5 R29). A beat usually equals one shot. In the blueprint, write these into the fields of section 3 above.

Template, action score (§4.2, exact):

```
SCORE <scene>-<letter> "<name>"  time_design: <value>  story <s> s  screen ~<s> s
count | story_t   | <BODY 1>        | <BODY 2>        | <SET / WORLD>     | CAMERA
1     | <a>..<b>  | <+ / − / => what | <+ / − / => what | what the set does | mount, position, lens
```

Key: `+` this body pushes, pulls, strikes or grips; `−` it is pushed, pulled, struck or lifted; `=` it holds still; `(not seen)` it happens but no shot shows it; `(POV)` the camera's point of view. A count is an order, not a length of time (stage-combat notation: "Every actor therefore works from the same shared count" [V]). To make shots: each shot takes one slice, reads the columns inside it and writes them as `moment` steps. `+` and `−` on two bodies in the same count means contact: apply rules 17 and 27.

**Procedure B: overlapping slices (a fall, a crash, a snatch)** [§6 Recipe B]
1. Put t = 0 at the release; compute story duration (rule 23). SC06: 9.2 → 2.53 m = 6.67 m; √(6.67 ÷ 4.9) ≈ 1.17 s = 28 frames.
2. List clock objects and when each is visible. SC06: the sill passes the cage floor at √(0.15 ÷ 4.9) ≈ 0.18 s and leaves a 2.0 m gate's top at √(2.15 ÷ 4.9) ≈ 0.66 s [J on gate height; a 2.3 m gate gives 0.71 s].
3. Give each clock shot a slice in story order; its duration equals its slice.
4. Put clockless beats between them, held for their reading minimums or longer, framed on the interior, outside dark or soft.
5. Ask: *"Check that each clock object's slices only move forward, that different clocks overlap by 0.3 s at most, and that the last clock slice ends within 0.1 s of the event."*
6. Watch the animatic once without stopping; shorten clockless holds first.
7. Blueprint: one master previs (`PV-SC06-MASTER`, frames 12-40); each clock shot's `time_slice` = frames 12 + 24 × t; clockless shots are separate renders against a still cage (C4 R11).

**Procedure C: stuntvis at home, safely** [§6 Recipe C]
1. Clear floor space with a mattress or cushions; a second person present; no heights, ladders or real contact [J].
2. Tape the anchors on the floor; phone on books or a tripod, locked, whole body, plain background, good light (C4 Rec7; D15 §5).
3. Act each body separately: pull a towel tied to a door handle; push a closed door; for a hang, press hands down on a table edge while bending the knees; for a swing, a broom at empty air.
4. Act fast moves at half speed; never act falls, throws, weightlessness or hits (rule 32).
5. Name files by beat id (`SC02-AB08_hands.mp4`).

**Procedure D: from mime to motion** [§6 Recipe D; tools verified 27-28 Sept]
1. One body, ordinary movement: phone clip → Kling Motion Control (2.6: clip "3–30 seconds", no cuts or camera moves, moderate speed, largest person drives it; 3.0: 9 or 12 credits per second) or Runway Act-Two (D15).
2. One body in an exact set: phone clip → Rokoko Vision or DeepMotion (free tier 60 s a month, non-commercial) → stand-in in the C4 master set → Route 2 or 3.
3. Falls, throws, zero gravity: Cascadeur (Free non-commercial, own format only, 300 frames and 120 joints per scene; Indie $19/month or $8 yearly, revenue under $100k; Pro $49 or $33, adds environment interaction; Mocap (Alpha) .mp4, one actor) or Blender hand keys (C4 R10-R11) → Route 2.
4. Two people touching: capture separately, Route 2 depth per body (rule 27b), or Seedance 2.5 clay reference (up to 30 s).

**Procedure E: generate and assemble coverage** [§6 Recipe E]
1. One clip per beat at the model's shortest length plus handles; at most about 3 s used of any floating clip (A4 WE1).
2. Prompt: one main action and end state; failure as the action; screen direction; "The camera does not move." or one move; injury by look; for floating, visible floating, camera locked to the room, never the word "falling" (C3 R13).
3. Hands: separate insert from a checked still.
4. Joins: match on action with the whole movement in both clips; chain only inside one continuous action; hide mount changes in black or a body across the lens (A4 AI6).
5. Fast moves: half speed, then 2×; check cloth, hair and sound after.
6. Composite what must be exact: sparks, flashes, blood beads, floating screws, visor graphics (Route 5).
7. A person checks physics, contact and hands on every kept take: "83.3% of exocentric and 93.5% of egocentric generated videos exhibit at least one human-identifiable physical glitch" (Physion-Eval) [V]; LLM reviewers miss most (C3 R20).

## 5. Checklists

**Per set piece** [§7]
- A physical goal, at least one escalation, at least one reversal?
- Geography shown calmly first, with anchors, and re-shown after any rupture?
- Time treatment chosen by rule 18, story duration computed, reading budget summed?
- Every clock only moves forward; clock shots short, clockless shots the held ones; different-clock overlaps ≤0.3 s?
- At most one axial overlap and one mount change (outside B1's "break")?
- Every content-risk beat split and composited (C1 R9); every strike built from angle, reaction and sound (rule 17)?
- Fields under the blueprint's names?

**Per beat or shot** [§7]
- Cause and effect both visible (or the cause heard, A4 SND1)? Anchor in frame at the cause?
- Point of interest where the last shot left the eye?
- One main action, one or no camera move, an end state?
- If bodies touch, which rule 27 option? Movement reaches a point of rest before a cut away?
- A clock shot's duration equals its slice?
- Speed trick prompted "in slow motion"?
- `capture`, `safety`, `previs_level` filled?

**Failure signs** [§8]: fall floats → key 4.9 t² every frame; fall looks slow-motion → a clock shot held too long; stripe shrinks → re-slice; weightless bodies sink → hand keys, no "falling"; strike looks like a miss → rule 17; sped-up take has heavy gravity → it was prompted "slowly"; refusals → split, composite, stop after two.

## 6. Saying it to AI models

- One sentence per visible event, cause before effect: *"Her fingers slide along the bar and lose it; her hand swings free."* Failure is the action and the end state names it [R4].
- Direction every time: *"She moves toward frame left."* Camera: *"The camera does not move."* or one move tied to the body [R18].
- Floating: *"Her body drifts slowly away from the rail at a steady, constant speed; nothing pulls her down. The camera drifts with her at the same speed, level. End state: a metre of empty space between her and the hull."* (SC26 AB10 prompt core) [WE3].
- Fast moves: *"in slow motion, half speed"*, then 2× in the edit [R15].
- Injury by look, never by word: "a dark stain spreads" [C1 R9]; gunfire is a composited flicker plus sound.
- LLM (breakdown) prompts: use Procedure A's three instructions and Procedure B's check sentence verbatim.

## 7. The Catch

**Decisions made (for the user to confirm)**
- **SC06 fall (K20):** story 1.17 s by physics; screen about 11.6 s from overlapping slices. Clock shots at true speed: 15 wall (−0.3→0.45 s, 0.75 s), 18 opening (0.18→0.66, 0.5 s), 19 stripe small (0.42→0.75, master frames 22-30), 23 stripe large (0.75→1.08, frames 30-38). Clockless holds: 16 washing 2.2 s, 17 beads 2.0 s (composited over a blood-free plate), 20 Eli 2.5 s (longest, hand hidden), 21 slip 0.8 s, 22 "She hooks her fingers deeper into the grid." 0.7 s (new insert), 24 eyes 1.0 s; 25 CLACK plus 10 frames of black, hiding the mount change from cage to world. Sound roar may stretch. SC13 replays the 1.17 s at true speed.
- **SC06 whole (roof shot to black):** 25 shots, about 30.9 s, ASL about 1.23 s (inside D10's thriller peaks of 1-2 s). No gun or shooter seen, flicker composited, gunshots in the mix; the wound as "a dark stain spreads"; the haul at previs 3, Route 2 per body.
- **SC02 rung:** `real_time_continuous`, about 29 s, 14 beats; handheld only from "It rolls. Her foot goes." to "She gets a foot on the rung below." (B1); AB08 hands mimed on a table edge, `safety: no hanging`.
- **SC05 drip stand:** the strike split into swing (mimed with a broom at empty air) and fall (hand-keyed), joined by match on action, impact in sound; stairs frame left, shaft frame right [J].
- **SC23 fast move:** three 0.5 s bursts (shell, cell, lock), each ending on a point of rest, overlapped by a 1.0 s shot of Jude's hand; Jude in a separate clip.
- **SC26 push:** `held_real_time`, camera bolted to the ship and dead still until "She pushes gently away from the rail."; then the camera drifts with her (B1's "break"); SC27's first shot chained from AB10's last frame.
- **SC27 "Twelve. Six. Three.":** a 1.2 s free-fall clock, so a second `overlapping_slices` passage: three visor inserts in forward order with clockless holds between.

**Flagged for the user**
- Keep the addition: a stripe POV during the descent before the roof shot (not in the script)?
- Accept about 10× expansion, or test the fallback (shots 16 and 17 at 1.2 s each; about 9.8 s)?
- Keep "She hooks her fingers deeper into the grid." as its own shot?
- CLACK on the first black frame (A4) or over the last picture (B1 Example 2)?
- SC26 visor clock: true 4.9 t² (leaves the visor within seconds) or a rescaling display that holds until "Only an arrow points towards it." (suggested) [J]?
- The stripe and control box as SC06 anchors are additions to B3's list.

## 8. Conflicts and open questions

1. **A4 vs B1 vs C4 on the SC06 fall:** resolved by overlapping slices (rules 19-20); blueprint K20 adopted it. Proposed A4 WE1 edits: row 8 1.8 → 0.75 s; row 9 2.0 → 2.2; row 11 0.6 → 0.5; row 12 0.9 → 0.35; row 14 0.7 → 0.8; row 15 0.5 → 0.35; add the hook insert 0.7 s. C4 Example A needs a clockless variant (bodies relative to a still cage).
2. **Bordwell's axial cut vs B1's slow-motion ban:** repeat without slowing (rule 15).
3. **B1 Example 2 vs A4 WE1 row 17:** where the CLACK sits (one frame's difference); follows A4 [J]; user's choice.
4. **D10 CM1 (comic punch in a shared frame) vs rules 16-17:** share the frame only when bodies do not touch [J].
5. **C1 speed-up vs B1 no slow motion:** no conflict; screen speed stays real (rule 22).
6. **Field names:** D11's `time_design`, per-beat seconds and route names differ from the blueprint's `time_treatment`, `time_slice` and route values; the blueprint wins (section 3). C4's previs Level 1b has no place in the blueprint's 0-5.
7. **Beat density:** D11 and C3 say one main action per 4-5 s; blueprint TIME-06 uses 4 s. Use 4 s.
8. **D10 has no `fall` or `stunt` set-piece value;** R1's text trigger covers it. Open: add `physical` to D10's list?
9. **Unverified:** that *Film Art* itself uses *October* as its overlapping-editing example [U]; which Cascadeur plans include Mocap [U]; DeepMotion multi-person limits per plan [U]; the gate height in SC06 (2.0 m assumed; C4's cage is 2.3 m) [J].

## 9. Section map

| Section of D11 | Holds | Digest |
|---|---|---|
| §0 Terms | set piece, beat, anchor, clock, slice, count, selling a hit, stuntvis | 1 |
| §1 P1-P8 | principles | 2 (1-5) |
| §2 R1-R28 | decision rules | 2 (6-34) |
| §3.1 | the five time treatments table | 2 (18) |
| §3.2 | SC06 resolution, eight points | 2 (19-21), 4 B, 7 |
| §4.1-4.2 | beat map YAML; action score, SC06 example, blank template | 4 |
| §5 | field table; blueprint mapping | 3 |
| §6 Recipes A-E | procedures; tool table | 4 |
| §7-8 | checklists; failure modes | 5 |
| §9 WE1-WE6 | SC02, SC06, SC26-27, SC23, *Long Places* II, SC05 | 7 |
| §10 | conflicts; open questions | 8 |
| Sources | 20 sources, re-check notes | — |
