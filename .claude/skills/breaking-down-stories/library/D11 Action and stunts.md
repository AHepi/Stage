# D11 — Action, stunts and physical set pieces for AI: beat maps, geography, time, coverage (as of 27 September 2026)

> **What this file is for**
> 1. It turns any physical passage (a fall, a fight, a climb, a push, a fast move) into an **action beat map**: one row per cause and effect, with place, direction, camera mount, story time, screen time, clip, previs level and content risk.
> 2. It gives one method for **expanding a moment without slow motion**, and settles the A4/B1/C4 disagreement about *The Catch*'s fall (SC06).
> 3. It says how to **write and capture choreography** safely at home (action score, mime, phone, mocap, Cascadeur), and how to **cover** action with short, chained AI clips.
> 4. It runs after A2/A3 (beats, floor plan), B1 (camera system) and B3 (geography), and before C3 prompts, C4 previs and A4's final durations.
> 5. It builds on these and does not repeat them: A3 R16; A4 C1–C7, WE1, AI6; B1 R23, §10; C1 R9; C3 R2, R14, §13C; C4 §9, R10–R12, Rec7, digest rule 42; C5 digest rule 31; D10 `set_piece`; D15 driving clips.

Evidence labels: **[V]** verified at a primary or named source (URL in Sources, checked 2026-09-27; re-checked in an adversarial pass on 2026-09-28); **[U]** unverified; **[J]** my judgment. Scene numbers follow A2 (SC02 freight shaft, SC05 corridor, SC06 freight cage, SC13 glass partition, SC23 ship human rooms, SC26 ledge, SC27 beside the ship). "Frame" means 1/24 s. Cross-references: "R#", "Rec#", "Ex#", "WE#" and "§" are the cited file's own labels; "C4 rule 42" and "C5 rule 31" mean the numbered rules in those files' **digests** (C5's full-file R31 is a different rule, about lip sync). The blueprint (section 7.2, card 15, K20) has already adopted this file under some different field names; §5 gives the mapping, and the blueprint's names win.

**Fact-check pass, 2026-09-28 (what changed).** Bordwell's axial-cut quote was cut short: his example repeats the action *and slows it* (R10 now says how to use it without slow motion). Runway's failure wording is now quoted exactly (R2, R4). B3's anchor list does not include the control box (§0). The *October* example had the wrong source (§3.2). The Kling Motion Control quotes are now exact (Recipe D). The SC06 slices were re-timed to the C4 kit's frame numbers (WE2, §4.2, §10), which also brought every overlap between different clocks under 0.3 s. R15 now says "in slow motion", not "slowly". Added: R1's trigger from D10's `set_piece` values; R28 (strikes: angle, reaction and sound); WE6 (SC05, the drip stand); the blueprint field mapping (§5); four conflict notes (§10, items 3–6).

---

## 0. Terms (one plain sentence each)

- **Set piece**: a scene built around one big physical event (D10's `set_piece` field).
- **Action beat**: one cause and its visible effect ("the rung TURNS"). It is the smallest unit of an action scene.
- **Geography**: where people and things are in relation to each other, so the viewer can predict what could happen next.
- **Anchor**: a fixed, easily seen object that keeps the viewer oriented. B3 lists *The Catch*'s anchors for these scenes as "the red tag on the cage gate (sc1–6); the bright sill (shaft)". This file adds the control box (in the cage's north-west corner in C4's floor plan) and the yellow stripe as anchors for SC06 [J].
- **Escalation**: each beat makes the danger or the effort bigger.
- **Reversal**: a beat that flips fortune, from safe to in danger or back.
- **Story time**: how long an event takes in the story world. **Screen time**: how long the audience watches it.
- **Clock**: anything in picture or sound that lets the viewer measure story time (the yellow stripe growing, a speed read-out).
- **Clock shot / clockless shot**: a shot that shows a clock / a shot that shows nothing that measures time.
- **Slice**: the stretch of story time that one shot shows.
- **Overlapping editing**: "Cuts that repeat part or all of an action, thus expanding its viewing time and plot duration" (Bordwell and Thompson's *Film Art* glossary) [V].
- **Elliptical editing**: "Shot transitions that omit parts of an event, causing an ellipsis in plot duration" [V, same glossary]. In plain words: cuts that leave out parts of an event, so screen time is shorter than story time.
- **Point of rest**: the few frames where a movement finishes before a cut away. Bordwell: "Let the arc of movement, itself perhaps stretched over several shots, come to a point of rest, if only for a couple of frames" [V].
- **Count**: one step of a fight or stunt, numbered so every performer works from the same sequence (stage-combat practice, §4.2). A count is an order, not a length of time.
- **Selling a hit**: making a blow that never touches read as a hit, by the angle, the victim's reaction and the impact sound (R28).
- **Axial cut**: a cut straight in or out along the camera's line of sight.
- **Action score**: this file's choreography notation: one row per count, one column per moving body, the set and the camera.
- **Stuntvis**: video rehearsal of a stunt, made before filming, used as a blueprint [V, VFX Voice].
- **Mime capture**: acting a movement for the phone without its real force, height or contact.
- **Motion capture (mocap)**: turning filmed movement into a 3D skeleton's animation. **Motion transfer**: copying a filmed person's movement onto a character image inside a video model.
- **Chain**: a clip generated from the previous clip's last frame. **Hidden cut**: a cut placed where the frame is filled by something (a body, dark, blur), so the join cannot be seen.
- **Camera mount**: what the camera is fixed to (B1): the world, a vehicle, or a character.
- **Borrowed terms**: *previs* is a rough grey 3D version of a shot (C4); *hand-keying* is animating by setting positions by hand; *routes 1–5* are C4 §6's ways into video (1 keyframe images, 2 depth or pose control video, 3 clay render as reference, 5 compositing); *first_last_frame* makes a clip between two given pictures; *compositing* lays an element over a clip in the editor; an *insert* is a close shot of a detail; *POV* is what a character sees; a *J-cut* starts the next shot's sound early; *ASL* is average shot length.

---

## 1. Core principles

- **P1. An action scene is a scene.** Someone wants a physical result, obstacles escalate, fortune reverses at least once, and it ends in a changed situation (A2's beat logic). Jackie Chan's rules, as summarised from *Every Frame a Painting*, say the same: "Start with a **disadvantage**", "Use the **environment**", "Earn your **finish**" [V].
- **P2. Legibility first.** At every cut the viewer must know where the bodies are, what each wants and what just changed. Bordwell: "go for clarity in every way"; the failure he names is "too many close views, too few master shots" [V]. Stork's *Chaos Cinema* essays name the opposite style [V].
- **P3. Geography is story.** Murch ranks 3D continuity last of his six cut criteria (A4). In action, though, who is where decides what can happen, so a cut that loses geography loses story (Murch's second criterion), not only space [J].
- **P4. Cause, then effect, then reaction, each seen** (A4 R7). Models reverse or skip causes (C1 §9), so the map names both.
- **P5. Time is designed, not left to the model.** Choose one time design per passage (§3). Slow motion is not the default way to stretch a moment (B1).
- **P6. Physics is honest wherever the audience can measure it.** Clocks follow real numbers. What nothing measures may be held [J; this file's main addition].
- **P7. One acting body per clip where possible, one main action per 4–5 s, a simple camera** (C3 R2 and its beat-density check L05; B3 R21). Action is every model's weakest skill. In FilmBench (July 2026), action scenes lowered every model's score, and "the drop is dominated by camera-work sub-metrics—camera movement (−31.1), focus (−28.6), shot scale (−26.6)"; physical plausibility fell 16.9 points [V, arXiv 2607.24241, full text].
- **P8. Design and rehearse before generating; the body at home never does the stunt.** Stuntvis is "some kind of video reference undertaken as part of the design of a project's stunts by a stunt coordinator or action choreographer prior to anything being filmed on set"; fights are worked out "in a gymnasium or a created space with pads and boxes", and "It's not uncommon for the final sequence to be nearly identical to the stuntvis" [V, VFX Voice]. Your version: an action score plus a mimed phone rehearsal.

---

## 2. Decision rules

**Design**
- **R1.** If D10's `set_piece` is `chase` or `fight`, or a passage contains a fall, a strike, a climb, a carry, a push, a throw, weightlessness or a move the text calls fast, then make an action beat map (§4) before shot design, because models fail most here and durations cannot be guessed (C5). D10 has no `fall` or `stunt` value, so SC02 and SC06 (`task` or `none` in D10's list) enter through the second half of this rule [J].
- **R2.** If writing a beat, then state cause and effect as two visible events; if a take shows the effect first, then split cause and effect into two shots, because Runway's own limitations list for Gen-4.5 says "effects sometimes precede causes (e.g., a door opening before the handle is pressed)" [V; C1 §9; C3 R15].
- **R3.** If a set piece has no reversal, then find the one the text implies (a habit, a hope, a false relief) and mark it, because action without reversal reads as a stunt reel [J]. *The Catch*: the foot's habit in SC02; the sill's false relief in SC06.
- **R4.** If a beat must fail (a grip slips, a rung rolls, a stone will not move), then make the failure the described action, early, with a failed end state, because models favour success: Runway's list says "actions disproportionately succeed (e.g., a poorly aimed kick still scoring a goal)" [V; C3 R14].
- **R5.** If the danger comes from the place (grid, sill, rail, stone), then name that anchor in each beat and keep it in frame at the cause, because the place is both obstacle and map (P1).

**Geography and direction**
- **R6.** If a set piece moves through space, then show its geography calmly before the pressure (A4 C6), write one `travel_direction` for the sequence (A3) and put it in every prompt (A4 C5), because it cannot be learned in a rush and models forget direction.
- **R7.** If cuts are fast (under about 1.5 s [J on the threshold]), then keep the point of interest where the eye already is (the centre by default, else where the last shot ended) and record `attention_in`/`attention_out`, because *Mad Max: Fury Road* (2,700 shots in 120 minutes) used "Eye Trace" and "Crosshair Framing" so the important information stayed "in one spot…the Center of the Frame"; George Miller's instruction on set was "Put the cross hairs on her nose!" [V, Nedomansky].
- **R8.** If a shot is wide, then hold it longer than a close shot, because "More distant shots should be held longer than closer ones" (Bordwell) [V].

**Cutting**
- **R9.** If cutting away from a movement to something else, then let the movement reach its point of rest ("if only for a couple of frames", Bordwell). If cutting to another angle of the same movement, then cut mid-movement with the whole movement in both clips (A4 R3). The first gives rhythm; the second hides the join.
- **R10.** If one impact must land harder, then consider one axial overlap: cut straight in and repeat 2–4 frames of the impact, **both shots at real speed**. Bordwell's full sentence is "The force of the action is multiplied by the simplest cut possible: an axial enlargement, with the action slightly repeated and slowed"; in his example "The first shot of Salina's swing lasts seventeen frames, the second exactly twice as long" [V]. Chan: "In editing, **two** good hits = **one** great hit" [V]. In a film that bans slow motion (*The Catch*, B1), keep only the repeat, not the slowing. Use it at most once per set piece, because repeats wear out like A4 P10's devices [J on the count].
- **R11.** If action and reaction can share one frame without the two bodies touching, then keep them together (Chan's rule 4, "Action and Reaction in the **same** frame"). If they touch, then split them (R20), because the models' multi-subject weakness outweighs the gain [J].
- **R28.** If a strike, shove or trip must look as if it lands, then build it from angle, reaction and sound: the strike crossing toward or past the camera in one clip, the victim's reaction in its own clip, and the impact only in the sound mix, because screen fighting never needs contact ("Shoot punches and kicks from an angle where the strike crosses toward or past camera, so the gap between fist and face is hidden"; "Angle + reaction + sound together make the missing punch land" [V, Roberts, Filmmaker Genius]), and this also keeps one acting body per clip (R20a) and keeps the impact off-screen (C1 R9). *The Catch*: SC05's "Iona puts the drip stand across his shins." (WE6).

**Time** (details in §3)
- **R12.** If the reading time a passage needs (A4 R8's minimums, summed) is longer than its story time, then use `overlapping_slices`; if the danger is a wait, `held_real_time`; if the passage is long and repetitive, `elliptical`; otherwise `real_time_continuous`; `slow_motion` only where B1's camera system allows, because reading time against story time decides it [J].
- **R13.** If using overlapping slices, then play every shot at real speed, move every clock forward from shot to shot, hold only clockless shots, and make the clock shots' slices cover about the real duration once, because the audience can measure only clocks [J]. If a shot shows a clock and a face together (the wall streaming behind Iona), then it counts as a clock shot: its screen duration equals its slice.
- **R14.** If screen time exceeds about 3× story time, then keep the expansion for a turning point and, where the story allows, show the event again at true speed later (SC13 does), because a large stretch reads as subjective time [J].
- **R15.** If a movement is fast (a slip, a snatch, a swing), then generate it at half speed (write "in slow motion, half speed"), generate twice the used length, and speed it up 2× in the editor, because models smear fast motion (C1 §9; B1 §6.1: "a common fix is to generate it in slow motion and speed it up in the edit"). The screen speed is still real, so B1's no-slow-motion rule holds [J]. Write "in slow motion", not "slowly": "slowly" slows only the performer, so anything falling, pouring or flapping in the same frame moves at normal speed and, after the 2× speed-up, looks as if gravity were four times stronger [J]. If nothing but the one fast move is in frame, either word works.
- **R16.** If a clock is physical (a fall, a rising cage, a thrown object), then compute it: distance fallen = 4.9 × t² m; speed = 9.8 × t m/s; time to fall h metres = √(h ÷ 4.9) s (from d = ½ g t², g = 9.807 m/s²) [V]. Eye-guesses of falls tend to come out too long [J], and eased keys read as floating (C4 R10). Worked number: a 10 m fall takes √(10 ÷ 4.9) ≈ 1.43 s, and ends at about 14 m/s.

**Camera**
- **R17.** If physics is impossible or extreme, then the camera obeys the characters' physics (B1 R23), and it changes mount only on a hidden cut (black, a body across the lens) or as the film's one "break" (B1), because a mount change is itself an event.
- **R18.** If a clip carries the action, then give it no camera move, or one simple move caused by the body, because models handle one move per clip (C3 R2, B3 R21) and camera work is weakest in action (P7).

**AI coverage**
- **R19.** If a continuous action needs several angles, then design one shot or a chain (A3 R16). Chain last frame to first frame only inside one continuous action, and re-attach the identity references on every link, because chaining drifts: MovieDreamer found "chaining from each clip's last frame degraded quality", and CineCrew uses "last-frame-to-first-frame chaining only where clips form one continuous take" (C5 §1; C5 digest rule 31 refines A4 AI6).
- **R20.** If two or more bodies touch in one shot, then (a) cut so only one body acts per clip, (b) use Route 2 depth per body and composite (C4 digest rule 42; D6 Rec8), or (c) use Seedance 2.5 with a clay reference and distinct stand-in colours, budgeting double takes, because ByteDance says Seedance 2.5 has "room for improvement, particularly regarding the physical plausibility of complex motions and the stability of scenes involving interactions among multiple subjects" [V]. Try (a) first; use (b) or (c) only when the touch itself is the beat (a pull, a carry, a catch).
- **R21.** If hands carry the beat (grip, slip, latch, button), then give them their own insert from a checked start frame, with one simple grip and the contact named (C3 §13C), and keep hands small or hidden in wides, because hands melt.
- **R22.** If more than about 3 s of an action clip is used, then it needs one main action and an end state, else split it (C3 R2), because chained events come out muddled.
- **R23.** If a set piece contains weapons, wounds or blood, then rate each beat's content risk and apply C1 R9: cause, reaction and aftermath as separate shots; impact off-screen; muzzle flashes, sparks and blood composited; gunshots in the sound mix. After two refusals, move the element to compositing or sound (C1 R10).

**Capture and previs**
- **R24.** If a performance matters (a reach, a pull, a shove, a flinch), then mime-capture it: phone locked off, whole body in frame, plain background, one performer per clip (C4 Rec7; D15 §5 for the filming set-up), because capture gives timing that text cannot (C1 R12).
- **R25.** If a move involves height, speed, impact, falling, weightlessness or striking someone, then do not perform it for reference: hand-key it (C4 R11), use Cascadeur, or mime a slow, grounded version and retime it, because home capture has no stunt safety and mocap assumes gravity anyway [J].
- **R26.** If a reference video goes into a model as input, then use footage you shot or have rights to; watch film clips only to study timing, because the model copies its input closely (D4) [J].
- **R27.** If choosing `previs_level` for an action beat, then use Level 0 for faces and inserts; Level 2 for exact geography or a framing that withholds; Level 3 for falls and zero gravity (C4 §9) and, by this file's extension, three touching bodies [J]; Level 4 for physical acting (C4 §9). Record it per beat, because one set piece mixes levels. C4's ladder also has a Level 1b (a browser 3D try-out); the blueprint's `previs_level` field allows only 0–5, so write 1b as 1 there.

---

## 3. Time: stretching a moment without slow motion

### 3.1 The five time designs

| `time_design` | Screen vs story | Use when | *The Catch* |
|---|---|---|---|
| `real_time_continuous` | equal; each shot continues the last | most action; the audience needs no extra reading time | SC02 rung; SC06 up to the fall |
| `held_real_time` | equal; few long shots, little happening | the danger is a wait; B1 §6.1: "first try holding the shot longer in real time with less happening in it" | SC26 ledge |
| `overlapping_slices` | screen longer; shots repeat parts of the same seconds, each at real speed | the event is shorter than its reading time | SC06 fall; SC27's last metre ("Twelve. Six. Three.") |
| `elliptical` | screen shorter; parts left out | long repetitive action (a climb, a rise) | SC27's rise ("At last…") |
| `slow_motion` | screen longer by frame rate | only if the camera system allows | banned in *The Catch* (B1) |

### 3.2 The SC06 conflict and its resolution

**What the library says.**
- A4: the fall "runs about 12 seconds of screen time (subjective, expanded)" (WE2); WE1's shots 8–17 sum to 12.4 s.
- B1 §10.1 and its banned list: no slow motion; "the fall is played in real time", because slowing the picture would make the beads "decorative".
- C4 Example A: free fall from 9.2 to 2.53 m in 28 frames (master previs frames 12–40, CLACK on frame 40), about 1.17 s, keyed from 4.9 t² [V, C4 kit `plan_cage_fall.json`]. So story time t (seconds after release) = (frame − 12) ÷ 24.
- The script agrees with C4: SC13 calls it "the long second of the fall".
- B1 §10.1 says the stripe "grows shot by shot and becomes the fall's clock"; C4 quotes it.

**The resolution: two clocks and overlapping slices [J].**
1. **The story clock is physics and stays 1.17 s.** Every clock shot obeys it exactly. A clock shot is anything that sees the shaft: the streaming wall, the opening, the yellow stripe.
2. **Inside a freely falling cage, nothing moves because of gravity.** Bodies and beads drift at whatever speed the release and the air rushing up through the grid give them (B1 §10.1: "everything falling together, camera included, feels weightless"; B1's "the break": "free fall has no sensation"). So a shot that sees only the cage's interior (faces, hands, beads, the control box) contains no clock, and can be held 2–3 s at real speed without slowing anything. Physics sets the wall's speed, not a drifting body's.
3. **Screen time is built from slices.** Clock shots are short and move forward: each clock object only ever shows later states. Clockless shots are the held ones; they overlap in story time. The classic film case of stretching one moment by overlapping shots is the raising of the bridge in Eisenstein's *October* (1928), where "Eisenstein draws out the sequence to remarkable effect" [V, Cox, *Screening the Past*]; that *Film Art* uses it as its own textbook example is [U] (the glossary page gives only the definition).
4. **Tolerance.** Two *different* clock objects may overlap by up to about 0.3 s, because a viewer cannot compare speeds across different views [J]. The same object never goes backwards.
5. **Sound may stretch.** The air roar rising in pitch (A4) follows screen time. It has no scale the viewer can measure, so it is the one clock allowed to be subjective [J].
6. **Payoff.** SC13 replays the same 1.17 s at true speed. The audience then learns how short the fall was and how little time Eli had (A4 WE2 already plans this).
7. **Budget.** The fall comes to about 11.6 s of screen time from 1.17 s of story time (about 10×), which R14 allows only because this is the film's central turn and SC13 pays it off. If the animatic reads as dreamy, cut the washing and beads holds (shots 16 and 17 in WE2) to 1.2 s each, for about 9.8 s; keep Eli's 2.5 s hold, which SC13 needs.
8. **How it goes into the blueprint.** One master previs of the physical fall (`PV-SC06-MASTER`, frames 12–40); each clock shot's `time_slice` names its frame range, frame = 12 + 24 × t (blueprint K20). Clockless shots have no `time_slice`; they are separate renders relative to a still cage (C4 R11).

Proposed edits to A4 WE1 and C4 Example A are listed in §10.

---

## 4. The action beat map and the action score

### 4.1 Beat map (scene level; copy into the breakdown)

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

Values are lowercase `snake_case` (C5 R29). A beat usually equals one shot. When a shot holds two beats, list both and give the duration once.

### 4.2 The action score (choreography notation)

Stage-combat notation records "the order of the moves, the line of each action" and "whether the actor attacks or defends"; "Every actor therefore works from the same shared count", so that "+4 on one actor's diagram will be answered by −4" on the partner's [V, Weapons of Choice]. In that system `+` means attacking and `−` defending, marked on a stick-figure target diagram. The action score adapts this to a table. There is one row per **count** (a count is a beat, not a second). Each body reads its own column. `+` marks the body applying force, `−` the body receiving it, `=` a body holding still. The set and the camera get columns too, because in *The Catch* the cage and the ship act.

```
SCORE SC06-C "the fall"  time_design: overlapping_slices  story 1.17 s  screen ~11.6 s
count | story_t     | IONA                     | ELI                     | JUDE            | CAGE / WORLD                 | CAMERA
1     | -0.3..0.0   | = flat, hand to latch    | = arm round Jude        | = slumped       | + shriek ends, lets go       | bolted_to_cage, low SE, 24 mm
2     | 0.0..0.4    | − boots leave floor      | − lifts with Jude       | − lifts         | + free fall 4.9 t²; wall streams up | same, level, no shake
3     | 0.1..0.6    | + fingers into grid; legs drift up | = eyes on Iona | − drifts        | (not seen)                   | same
4     | 0.18..0.66  | (POV)                    |                         |                 | opening slides up, out of gate top | her POV, sideways, level
5     | 0.42..1.08  | − grip slips; + hooks deeper | = "Io."; hand hidden | = across Eli    | stripe grows (small → frame-filling) | POV down / close
6     | 1.17        | eyes closed              |                         |                 | + CLACK                      | cut to black, 10 frames
```

To turn a score into shots: each shot takes one slice, reads the columns inside it, and writes them as D15 `behavior` steps (`t0-t1: what happens`; in the blueprint, the SHOT `moment` items `0-1.5 | shows: ...`). Two bodies with `+` and `−` on the same count means contact (apply R20 and R28). Story times in the score use t = 0 at the release; for the master previs, frame = 12 + 24 × t.

**Blank action score (copy this).**

```
SCORE <scene>-<letter> "<name>"  time_design: <value>  story <s> s  screen ~<s> s
count | story_t   | <BODY 1>        | <BODY 2>        | <SET / WORLD>     | CAMERA
1     | <a>..<b>  | <+ / − / => what | <+ / − / => what | what the set does | mount, position, lens
```

Plain-word key: `+` this body pushes, pulls, strikes or grips; `−` this body is pushed, pulled, struck or lifted; `=` this body holds still; `(not seen)` the thing happens but no shot shows it; `(POV)` this column is the camera's point of view.

---

## 5. Fields this file adds

| Level | Field | Meaning | Allowed values |
|---|---|---|---|
| scene | `action_design` | Container for this file's fields | present only for physical set pieces |
| scene | `physical_goal` | The physical result someone wants | one line |
| scene | `time_design` | How screen time relates to story time | `real_time_continuous`, `held_real_time`, `overlapping_slices`, `elliptical`, `slow_motion` |
| scene | `story_duration_s`, `screen_duration_s`, `reading_budget_s` | Physics or text time; watched time; reading need | numbers |
| scene | `clocks[]` | What lets the viewer measure time, and its law | `free_fall`, `constant_speed`, `text_given`, `none` |
| scene | `reversals[]`, `device_budget` | Beats that flip fortune; overlaps and mount changes allowed | beat ids; 0 or 1 each |
| beat | `beat_type` | The beat's job | `setup`, `attempt`, `obstacle`, `escalation`, `reversal`, `near_miss`, `release`, `aftermath` |
| beat | `cause`, `effect` | Two visible events | text or beat id |
| beat | `anchor` | Orienting object in frame | anchor id, `none` |
| beat | `story_time_s`, `clock_shown` | The slice; which clock is visible | [start, end]; clock id, `none` |
| beat | `attention_in`, `attention_out` | Where the eye is at the first and last frame | `top_left`, `top`, `top_right`, `left`, `center` (default), `right`, `bottom_left`, `bottom`, `bottom_right` |
| beat | `contact` | Bodies touching | `none`, `body_object`, `two_bodies`, `three_plus_bodies` |
| beat | `capture` | Source of the motion | `none`, `hand_keyed`, `cascadeur`, `mime_mocap`, `motion_transfer`, `own_reference_video` |
| beat | `speed_trick` | Half-speed generation, doubled in the edit | `none`, `generate_half_speed_x2` |
| beat | `join_in` | How the shot joins the previous one | `cut`, `match_on_action`, `hidden_cut`, `chain_from_<id>`, `axial_overlap_<frames>` |
| beat | `content_risk` | Chance a hosted filter refuses (C1 R9) | `none`, `low`, `medium`, `high` |
| beat | `risk_method` | How the risk is handled | `none`, `split_cause_reaction_aftermath`, `offscreen_impact`, `composite`, `sound_only`, `neutral_wording` |
| beat | `safety` | What the performer must not do | text |

Reused from other files, not redefined here: `screen_direction`, `axis`, `overlap_action`, `start_frame_from` (A4); `camera_mount` (B1); `previs_level`, `plan_file` (C4); `route` numbers (C4 §6); `behavior` (D15); `set_piece` (D10); `composite_elements[]` (C1).

**Mapping to the blueprint (section 7.2; the blueprint's names win).** The blueprint adopted this file as card 15 and conflict K20, under these names:

| This file | Blueprint | Note |
|---|---|---|
| `time_design` | scene `time_treatment` | same five values |
| `beats[].cause` / `effect` chain | scene `cause_chain` (text) | one text block, not per-beat fields |
| `beat_type: escalation` beats | scene `escalation` (text) | |
| `reversals[]` | scene `reversal` (beat ids) | |
| §4.2 action score | scene `action_score` (text block) | "one row per count, one column per body, the set and the camera" |
| `geography_anchors`, `travel_direction` | scene `geography` (text) | |
| `story_time_s` of a clock shot | shot `time_slice` | `PV-SC06-MASTER-V01 \| frames: 12-40`; frame = 12 + 24 × t |
| R16 physics clock | SHOT `motion` item | `free_fall \| object: <id> \| from_z: 9.2 \| to_z: 2.53 \| start_frame: 1`, read by the free-fall helper |
| `join_in: chain_from_<id>` | shot `start: from_end_of: <shot>`; scene `coverage: chained` | |
| `route` (`image_to_video`, `first_last_frame`, `route_2`, …) | shot `route` (`start_picture`, `start_end_pictures`, `guide_video`, `performance_transfer`, `composite_only`, …) | translate: image_to_video → start_picture; first_last_frame → start_end_pictures; route_2 / route_3 → guide_video; mime_mocap or motion transfer → performance_transfer; route_5 or edit_only → composite_only [J on the mapping] |
| `previs_level` 0, 1, 1b, 2–5 | `previs_level` 0–5 | write 1b as 1 |
| `behavior` steps | SHOT `moment` items (`0-1.5 \| shows: ...`) | the blueprint's check TIME-06 warns at more than one main action per 4 s |

Not yet in the blueprint (proposals, not facts): `physical_goal`, `clocks[]`, `reading_budget_s`, `device_budget`, `beat_type`, `anchor`, `clock_shown`, `attention_in/out`, `contact`, `capture`, `speed_trick`, `content_risk`, `risk_method`, `safety`. A builder who needs one must add it to the schema and record why (builder rule 2).

---

## 6. Recipes (the LLM does the work)

### Recipe A: an action beat map from a passage (20–40 minutes per set piece)
1. Give the LLM the scene text with line numbers, the B3 floor plan and anchors, and B1's camera system.
2. Say: *"List every physical beat in this passage as cause → effect, quoting the exact words. Mark each beat_type. Name the reversals. If there is no reversal, say which line implies one."*
3. Say: *"For each beat, name the anchor in frame, the screen direction and the camera mount from B1. Flag any beat where two or more bodies touch."*
4. Say: *"Compute the story duration from physics (distance = 4.9 × t²) or from the text. Sum A4 R8's reading minimums. Choose time_design by D11 R12 and explain in one line."*
5. Fill the §4.1 template and write the action score (§4.2).
6. Run the §7 checklist.

### Recipe B: overlapping slices (for a fall, a crash, a snatch)
1. Put t = 0 at the release. Compute the story duration (R16). For SC06: 9.2 m to 2.53 m is 6.67 m, and √(6.67 ÷ 4.9) ≈ 1.17 s, matching C4's 28 frames.
2. List the clock objects and when each is visible. Example: in C4's kit the sill's top is at 9.05 m, 0.15 m below the stopped cage floor (9.2 m), and the opening's top is at 11.2 m. The sill passes the cage floor after a drop of 0.15 m, at √(0.15 ÷ 4.9) ≈ 0.18 s. With a gate about 2.0 m tall, the sill leaves the gate's top after a drop of about 2.15 m, at √(2.15 ÷ 4.9) ≈ 0.66 s [J; gate height assumed; C4's cage is 2.3 m tall, and a 2.3 m gate gives 0.71 s]. So the opening's slice is 0.18–0.66 s.
3. Give each clock shot a slice in story order. Its duration equals its slice (real speed).
4. Insert the clockless beats between them, held for their reading minimums or longer, framed against the moving object's interior, with the outside dark or out of focus.
5. Ask the LLM: *"Check that each clock object's slices only move forward, that different clocks overlap by 0.3 s at most, and that the last clock slice ends within 0.1 s of the event."*
6. Watch the animatic once without stopping (A4); shorten clockless holds first.

### Recipe C: stuntvis at home (mime capture), safely
1. Clear a floor space with a mattress or cushions. Have a second person present. Use no heights, no ladders and no real contact [J].
2. Tape the anchors on the floor (the gate line, the control box corner). Put the phone on books or a tripod, locked, whole body in frame, plain background, good light (C4 Rec7; D15 §5).
3. Act each body separately: pull a towel tied to a door handle; push a closed door; for a hang, press your hands down on a table edge while bending your knees.
4. Act fast moves at about half speed (R15). Never act falls, throws, weightlessness or hits (R25).
5. Name the files by beat id (`SC02-AB08_hands.mp4`) so the LLM can place them.

### Recipe D: from mime to motion (tools checked 2026-09-27)

| Tool | What it does for action | Limits and price | Label |
|---|---|---|---|
| **Kling Motion Control** (VIDEO 3.0 and 2.6; guide dated 5 Mar 2026) | Copies a filmed person's body movement onto a character image | For 2.6: "The supported duration for uploaded action videos is 3–30 seconds"; "avoid overly fast motions; steady, moderate movements yield the best results"; "Please avoid cuts, shot changes, or camera movements; otherwise, the video may be truncated"; "For motion reference with two or more characters, the motion of the character occupying the largest portion of the frame will be used". The guide states no reference length for 3.0. Price: 3.0 costs 9 (Standard) or 12 (Professional) credits per second; 2.6 costs 5 or 8 | [V] |
| **Cascadeur** | Keyframe animation with physics help (AutoPhysics) and AI posing; Mocap (Alpha) from video | Free: "Only non-commercial use"; "Export to .casc format only. .fbx and .dae are not available"; export "limited to: 300 frames per scene, 120 joints per scene" (300 frames is 12.5 s at 24 fps). Indie $19/month, or $8/month billed annually; adds .fbx and .dae export; "The revenue must be less than $100k per year". Pro $49/month, or $33/month billed annually; "Commercial use with no limits", animation retargeting, "Interaction with environment in AutoPhysics" ("allows characters to interact with other objects in AutoPhysics (e.g. interaction with vertical walls)"). Mocap (Alpha): "Currently, only .mp4 files are supported"; it "can currently capture the movement of a single actor from the reference video" | [V] |
| **DeepMotion Animate 3D** | Video to 3D animation, incl. several people (C4) | Freemium: "Create up to 60 seconds of animations every month", "available for personal, non-commercial use"; paid-plan prices were not shown on the page; multi-person limits per plan not stated ("multi-person labeling is not available on mobile") | [V]; limits [U] |
| **Seedance 2.5** | Clay renders set "spatial structure, character poses, motion paths, and camera angles"; "Up to 30 seconds per generation, with multi-round extensions" (released 31 Jul 2026) | ByteDance: "room for improvement, particularly regarding the physical plausibility of complex motions and the stability of scenes involving interactions among multiple subjects" | [V] |

Rokoko Vision (one performer), QuickMagic, Runway Act-Two and Wan-Animate-2 are covered in C4 §3D and D15.

**Path.** (1) One body, ordinary movement: phone clip → Kling Motion Control or Act-Two (D15). (2) One body in an exact set or camera: phone clip → Rokoko Vision or DeepMotion → stand-in in the C4 master set → Route 2 or 3. (3) Falls, throws, zero gravity: Cascadeur or Blender hand keys (C4 R10–R11) → Route 2. (4) Two people touching: capture each separately, render Route 2 depth per body (C4 digest rule 42; D6 Rec8).

### Recipe E: generate and assemble action coverage
1. One clip per beat: the model's shortest length plus handles, trimmed (A4); at most about 3 s used of any floating clip (A4 WE1).
2. Prompts: one main action with its end state; the failure written as the action (R4); screen direction stated; camera "does not move" or one move (R18); injury described by look (C1 R9); for weightless bodies, describe visible floating, lock the camera to the room and avoid the word "falling" (C3 R13).
3. Hands: a separate insert from a checked still (R21).
4. Joins: match on action where both clips hold the whole movement (A4 R3); chain only inside one continuous action (R19); hide mount changes in black or a body crossing the lens (A4 §5, AI6).
5. Fast moves: half speed, then 2× (R15). Check that the cloth, hair and sound still read right after the speed-up.
6. Composite what must be exact: sparks, flashes, blood beads, screws floating, visor graphics (C4 Route 5).
7. A person checks physics, contact and hands on every take: in Physion-Eval (March 2026), "83.3% of exocentric and 93.5% of egocentric generated videos exhibit at least one human-identifiable physical glitch" across five late-2025 models (C1), and LLM reviewers miss most (C3 R20; C1 rule 18).

---

## 7. Checklists

**Per set piece**
- Is there a physical goal, at least one escalation and at least one reversal?
- Was the geography shown calmly first, with anchors, and re-shown after any rupture?
- Is `time_design` chosen by R12, with story duration computed and reading budget summed?
- Does every clock object move forward? Are clock shots short and clockless shots the held ones?
- Is at most one axial overlap used, and at most one mount change (outside B1's "break")?
- Is every content-risk beat split and composited per C1 R9?
- Is every strike or shove built from angle, reaction and sound in separate clips (R28)?
- Do the scene's fields use the blueprint's names (`time_treatment`, `cause_chain`, `reversal`, `action_score`, `geography`; shot `time_slice`, `route`, `moment`) (§5)?

**Per beat or shot**
- Are cause and effect both visible (or the cause heard, A4 SND1)?
- Is the anchor in frame at the cause?
- Is the point of interest where the last shot left the eye?
- Is there one main action, one or no camera move, and an end state?
- If bodies touch: which R20 option applies?
- Does the movement reach a point of rest before a cut away?
- Are `capture`, `safety` and `previs_level` filled?
- If the shot is a clock shot, does its duration equal its slice, and does its clock only move forward (R13)?
- If the speed trick is used, was the prompt "in slow motion" (R15)?

---

## 8. Failure modes (sign → fix)

- **Nobody can say where the people are** → a master or anchor shot before the pressure; fewer close views (P2).
- **The effect arrives before the cause** → split into two shots (R2).
- **The rung holds, the grip succeeds** → write the failure as the action, early (R4).
- **A fall looks like floating** → key from 4.9 t² every frame, or Cascadeur (C4 R10).
- **A fall looks like slow motion** → a clock shot was held too long; shorten it, or remove the clock from the frame (§3.2).
- **The stripe gets smaller between two fall shots** → reorder or re-slice (R13).
- **Weightless bodies sink** → models add gravity back: Route 2 depth from hand keys (C4 R11); in the prompt, describe visible floating, lock the camera to the room and avoid the word "falling" (C3 R13); reject takes where drift accelerates downward.
- **A strike looks like a miss, or two bodies merge at the hit** → rebuild it as angle, reaction and sound in separate clips (R28).
- **A sped-up take looks as if gravity is too strong** (hair, cloth or debris snaps down) → it was generated "slowly", not "in slow motion"; regenerate (R15).
- **Fast motion smears** → half speed, then 2× (R15).
- **Two people merge or swap; hands melt** → R20; R21.
- **The camera floats, shakes or orbits** → "The camera does not move" (R18).
- **Cutting before the boot clears the gate** → let the movement finish (R9; A4 WE1 row 33).
- **Refusals on the gunfire shot** → split and composite (R23); stop after two refusals.
- **A mimed capture hurts someone** → R25; no heights, falls or contact.

---

## 9. Worked examples

### WE1. SC02: the rung turns

**Goal:** reach the top gate. **Time design:** `real_time_continuous`, with one held beat (the hang). **Anchors:** the ladder "bolted to the brick"; the broken rung (its bright sheared bracket); the torch in her teeth (the light moves with her head). **Direction:** up = frame top. **Mount:** static; handheld from "It rolls." to "She gets a foot on the rung below." (B1); the camera stills at "She goes still." **Reversals:** AB05 (safe again), AB07 (habit bites). **Content risk:** none.

| # | Exact text | Type | Cause → effect | s | Route / previs | Notes |
|---|---|---|---|---|---|---|
| AB01 | "Hand. Foot. Hand. Foot." | setup | climbing rhythm | 3.0 | image_to_video / 0 | the pattern the beat breaks |
| AB02 | "Her hand closes on a rung and the rung TURNS." | obstacle | grip → rung rotates | 1.5 | first_last_frame / 0 | C1 Ex1; silent, creak in the mix |
| AB03 | "She goes still. The rung rolls in its brackets like a rolling pin." | escalation | her weight off → rung rolls | 2.0 | image_to_video / 0 | camera stills with her (B1) |
| AB04 | "She brings the light up: one bracket sheared clean through." | setup (plant) | torch up → bracket seen | 1.2 | still insert / 0 | the anchor, readable |
| AB05 | "She takes her hand off it. Reaches past. Finds the next one solid. Pulls." | reversal | reach → safe grip | 3.0 | image_to_video / 0 | one main action in 3 s (C3 R2) |
| AB06 | "…and sets itself on the broken rung." | escalation | habit → foot on danger | 1.5 | insert / 0 | suspense hold (A4 S2); bracket in frame (R5) |
| AB07 | "It rolls. Her foot goes." | reversal | rung rolls → foot off | 0.7 | first_last_frame / 0; `generate_half_speed_x2` | failure as the action (R4); handheld starts |
| AB08 | "Her whole weight drops onto her hands. Her jaw shuts on the torch." | escalation | drop → arms straighten, beam jerks | 1.0 | insert / 4 (mime: hands pressing a table edge) | `safety: no hanging`; one grip, named contact (R21) |
| AB09 | "She hangs." | near_miss | — | 2.5 | image_to_video / 1 (posed still) | held; legs over the dark shaft |
| AB10 | "Was that you?" / "No." | aftermath | V.O. → answer through torch | 3.0 | image_to_video / 0 | dialogue per A1/D3 |
| AB11 | "She gets a foot on the rung below." | release | foot finds rung | 1.5 | insert / 0 | handheld ends; camera settles |
| AB12 | "Spits into the dark. Does not hear it land." | aftermath (plant) | spit → no sound | 2.5 | image_to_video / 0 | no impact sound (SC06 payoff) |
| AB13 | "Runs her tongue over a front tooth…" / "It was my tooth." | aftermath | — | 2.5 | image_to_video / 0 | small, open expression (AI faces over-act) |
| AB14 | "Now each foot goes only where a hand has already been." | aftermath (change) | new rule → hand touches, foot follows | 3.0 | image_to_video / 0 | the changed situation (P1) |

Total about 29 s. The danger is shown once calmly (AB02–AB04); then her own habit makes it bite (AB06–AB07), and AB14 shows what it changed.

### WE2. SC06: from the roof shot to the CLACK

**Goal:** get three people out of the shaft. **Time design:** segments A and B `real_time_continuous` (about 19.3 s); segment C `overlapping_slices` (story 1.17 s, screen about 11.6 s). **Anchors:** control box (NW), gate, bright sill, grid, yellow stripe. **Direction:** travel down; shaft wall streams up in frame. **Mount:** `bolted_to_cage`, level, 24 mm, low SE corner (B1, C4); one shudder on the stop; no shake in the fall. **Reversals:** 12 (the way out) and 14–15 (the fall). **Clocks:** `clk_wall`, `clk_opening`, `clk_stripe` (all free fall); the roar (subjective). **Device budget:** mount change 1 (at the black, hidden); axial overlap 0.

Routes use C4 §6 numbers; models per C1. "PL" is `previs_level`.

**Segment A: the roof shot (real time)**

| # | Exact text | Type / cause → effect | s | Contact / risk | PL / route |
|---|---|---|---|---|---|
| 01 | "Far above, the stair door gives with a crash." | obstacle; crash → faces turn up | 1.2 | none / none | 0 / image_to_video; crash in the mix, source unseen (A4 T6) |
| 02 | "Someone KICKS the top gate open and FIRES down through the roof." | escalation; POV straight up through the roof grid: a tiny flicker far above, centred | 0.8 | none / **high** → `composite`, `sound_only` | 0 / still + composited flicker; no gun or shooter (C1 Ex7) |
| 03 | "Oh." | effect; voice first | 1.0 | none / low | 0 / Kling or H3 face (C1 Ex7 B) |
| 04 | "He sits down into Eli with a hole through his shoulder." | effect; Jude sits heavily into Eli's arms, shoulder turned away | 1.6 | `two_bodies` / medium → `neutral_wording` ("a dark stain spreads") | 2 / route_3; if merged, split (R20a) |
| 05 | "Iona hauls them both behind the control box." | attempt; her pull → both slide | 1.8 | `three_plus_bodies` / none | 3 / route_2 per body (R20b); Iona's pull `mime_mocap` |
| 06 | "Eli gets one arm round Jude's chest. His other hand goes underneath. Behind Jude's back. Out of sight." | setup (plant) | 2.0 | `two_bodies` / none | 2 / route_1; framing withholds (B1 Ex2); shown once, calmly (A4 S5) |
| 07 | "Another shot sparks off the grid beside her boot." | escalation | 0.8 | none / low → `composite` | 0 / insert + composited spark; shot in the mix |

**Segment B: the stop and the false relief (real time; A4 WE1 rows 1–7 unchanged, 10.1 s).** 08 "The opening reaches them." 1.5 s, PL 2. 09 "Iona hits STOP with her elbow." 0.6 s insert, `match_on_action` with 10. 10 "The cage STOPS DEAD." 1.2 s, PL 3, the only shudder. 11 "Iona is thrown flat on the grid." 0.8 s, `hand_keyed` or Cascadeur, never self-captured (R25). 12 "A passage. A way out." 3.0 s, the false-relief reversal, PL 1, route_1. 13 "She reaches for the latch." 1.5 s, shriek as a J-cut. 14 the METAL SHRIEK, 1.5 s, three faces up, source never shown.

**Segment C: the fall (overlapping slices; t = 0 at release; CLACK at 1.17 s)**

| # | Exact text | Story t (s) | Clock | s | PL / route | Notes |
|---|---|---|---|---|---|---|
| 15 | "The cage falls." | −0.3 → 0.45 | wall | 0.75 | 3 / route_2 or route_3 (`plan_cage_fall.json` frames 5–23) | was 1.8 s in A4; a longer hold would show more fall than exists; the wall is behind Iona, so this is a clock shot (R13) |
| 16 | "Her boots leave the floor. She gets her fingers into the grid. Her body floats out behind her like washing." | ~0.0 → 1.1 | none | 2.2 | 3 / route_2 from hand keys relative to a static cage | framed against the grid and control box; shaft below dark |
| 17 | "Jude's blood lifts off the steel in round red beads and hangs in the air between them, turning." | any | none | 2.0 | 3 / route_5 beads over a blood-free plate | `content_risk: medium`, `composite` (C1 Ex2) |
| 18 | "Through the grid, the opening flicks past. Going up." | 0.18 → 0.66 | opening | 0.5 | 2 / copy of `plan_grid_pov.json` aimed east (C4; master frames 16–28) | sill streaks up out of the gate top (Recipe B step 2); overlaps 15 by 0.27 s: different clock, allowed |
| 19 | "Through the grid, the yellow stripe. Coming." | 0.42 → 0.75 | stripe (small) | 0.35 | 3 / route_2 (`plan_grid_pov.json` frames 11–19, = master frames 22–30) | overlaps 18 by 0.24 s: different clock, allowed |
| 20 | "Io." / "He has one hand she cannot see." | any | none | 2.5 | 0 / image_to_video | longest shot of the fall; arm leaves frame bottom (B1 Ex2) |
| 21 | "Her grip begins to slip." | any | none | 0.8 | 0 / first_last_frame; `generate_half_speed_x2` | failure as the action (R4) |
| 22 | "She hooks her fingers deeper into the grid." | any | none | 0.7 | 0 / first_last_frame | **new insert**; the script's counter-move (a reversal inside the fall) |
| 23 | (the stripe) | 0.75 → 1.08 | stripe (large) | 0.35 | 3 / route_2 (grid-POV frames 19–27, = master frames 30–38) | stripe fills the frame edges (C4: full frame by grid-POV frame 22) |
| 24 | "Closes her eyes." | ends 1.17 | none | 1.0 | 0 / image_to_video | cut on the eyelids closing |
| 25 | "A hard metal CLACK." / "BLACK. A dark with nothing in it. One instant." | 1.17 | — | 0.42 | edit_only | 10 frames of black, CLACK on the first, true silence (A4); hides the mount change to `world` |

**Totals.** 25 shots, about 30.9 s from the crash to the black (A 9.2 s, B 10.1 s, C 11.57 s), average shot length about 1.23 s (D10 puts thriller peaks at 1–2 s, so this sits inside the genre range). The stripe's slices (0.42–0.75, 0.75–1.08) move forward and end two frames before the CLACK; the eyes shot (24) covers the last two frames. Every overlap between different clocks is under 0.3 s (15/18: 0.27; 18/19: 0.24). Every held shot (16, 17, 20, 24) is clockless.

**Check by arithmetic (the validator can do this).** Segment C: 0.75 + 2.2 + 2.0 + 0.5 + 0.35 + 2.5 + 0.8 + 0.7 + 0.35 + 1.0 + 0.42 = 11.57 s. Clock-shot screen time: 0.75 + 0.5 + 0.35 + 0.35 = 1.95 s, which equals the sum of their slices (0.75 + 0.48 + 0.33 + 0.33 = 1.89 s) within one frame per shot.

**Addition to flag (C5 V12).** During the descent before the roof shot, one POV down through the grid could show the stripe tiny and far below. Its growth in 19 and 23 would then read as approach at once. The script names the ladder, the rung and the opening there, not the stripe, so mark it `addition: keep | cut` for the user [J].

**After the black.** A4 WE1 rows 18–36 and C4 Example B stand. The push is `three_plus_bodies`: Seedance 2.5 with the clay reference first, R20b if bodies merge; Iona's reach and pull mime-captured, floating bodies hand-keyed.

### WE3. SC26: "She pushes gently away from the rail"

**Goal:** leave the falling ship on a path that will turn and rise to the receiving room. **Time design:** `held_real_time`: the danger is a wait while she works out the path. B1: "No exterior shot of the falling ship exists until she leaves it". **Clocks:** the visor drawing of the room (`free_fall`: it must slide up faster and faster, by 4.9 t² at the visor's scale) and the reserve bar; both are composited (Route 5). **Mount:** `bolted_to_ship`, dead still, until the last beat; then `attached_to_iona`, which is B1's "the break" (floating now means control). **Anchors:** rail, hatch, the hull's last projection (needed later for "HULL CLEARANCE"). **Content risk:** none.

| # | Exact text | Type / cause → effect | s | Capture / PL / route |
|---|---|---|---|---|
| AB01 | "Her boots on the deck. The sick motor through them." | setup | 2.0 | none / 0 / insert; motor as low sound through the feet |
| AB02 | "Then not." | reversal; the motor stops, nothing moves | 1.5 | none / 0 / same framing held; free fall starts with no jolt, so sound is the first sign |
| AB03 | "A loose screw rises off the deck beside her boot and hangs in her lamplight." | effect | 2.5 | none / 3 / route_5 screw drifting at constant slow speed (models add gravity back) |
| AB04 | "Her knees lift. Her feet leave the floor." | effect | 2.5 | `hand_keyed` / 3 / route_2; camera dead still |
| AB05 | "On the visor, the drawing of the room slides upwards. Goes on sliding." | escalation; the clock starts | 3.0 | none / 0 / route_5 graphic, accelerating |
| AB06 | "Nothing moves. There is no feeling of speed at all." | held danger | 4.0 | none / 0 / image_to_video; the held real time |
| — | (visor, carriage, path and animal beats: B1, C2, A4) | — | ~45 | — |
| AB07 | "Iona checks the strap. Pulls it once, hard." | attempt | 1.5 | `mime_mocap` optional / 0 / insert, one grip |
| AB08 | "The receiving room is far above the edge of her visor now. Only an arrow points towards it." | escalation; the clock leaves the visor | 2.0 | none / 0 / route_5 |
| AB09 | "She sets the engine to wait for her signal." | setup | 2.5 | none / 0 / wrist insert |
| AB10 | "She pushes gently away from the rail." | release (the break) | 5.0 (6 s clip) | arm: `mime_mocap` (a slow push off a door frame); body: `hand_keyed` / 3 / route_2 |

**AB10 in detail.**
- **Physics.** One short push (about half a second), then a constant slow drift that never speeds up: "Very slowly apart, as gently as two boats" (SC27). Reject takes where she drops away or speeds up: that is gravity added back [J].
- **Camera.** One move: the camera drifts with her at her speed, so she keeps her size in frame while the rail and hull slide away. Nothing like it appears earlier in the film (B1 reserves it).
- **Join.** Chain SC27's first shot ("She drifts out from the ship's side.") from AB10's last frame. This is one continuous action, so R19 allows the chain. Re-attach Iona's identity references.
- **Prompt core.** *"Medium shot. A woman in a white pressure suit floats beside a dark ship's hull, one gloved hand on a rail. She straightens her arm once, gently, and lets go. Her body drifts slowly away from the rail at a steady, constant speed; nothing pulls her down. The camera drifts with her at the same speed, level. End state: a metre of empty space between her and the hull."*

**The same method in SC27.** The rise ("At last the drawing of the room comes down to meet her") is `elliptical`. "UPWARD SPEED, in metres per second. Twelve. Six. Three." is a free-fall clock: from 12 m/s to nought takes 12 ÷ 9.8 ≈ 1.2 s [J from R16]. That is too short to read three numbers (A4 R8), so it is a second `overlapping_slices` passage. Three short visor inserts (12, 6, 3) in forward order, with clockless holds on her face and the vessel between them, then "Nought."

### WE4. SC23: the figure's one fast move

"Then it moves, and it is fast. / It closes a clear shell round Jude's bed. Pulls a black cell from the rack. Locks it under the shell. Jude has time to raise one hand."

- **Speed reads only against slowness** (Bordwell's pause/burst/pause). The figure has been careful ("As carefully as a nurse.", SC15), and the text plants its reflex calmly first: "It catches the cup without looking." Keep that insert clear and unhurried (A4 S5).
- **The clock is Jude's hand.** Three burst shots of about 0.5 s each in real time (shell, cell, lock) each end on a 2–4 frame point of rest (R9). Then one 1.0 s shot of Jude's hand rising, which overlaps the burst: mild `overlapping_slices`, about 2.5 s of screen for about 1.6 s of story [J].
- **Generation.** Each burst shot is a state change, so use `first_last_frame` (shell open → shut; cell in rack → in hand; cell under shell) with `generate_half_speed_x2` (R15). The figure is non-human (C4 Example C routes). Jude is in a separate clip, so no two acting bodies share a clip (R20a). `contact: body_object`. `content_risk: none`.

### WE5. *The Long Places*, chapter II: the stone will not open

"Going back, the stone had come home in its socket. She pushed with the flat of her hand, the heel of her hand, her shoulder; the pivot gritted and kept its opinion." Then "the third time it lay down she pinched it out with her nails".

- **Prose to beats (A3).** One sentence holds a three-step **escalation**: more of her body each time. Map it as AB01 flat of the hand (1.5 s), AB02 heel (1.5 s), AB03 shoulder (2.5 s, with the pivot's grit as `sync_fx`). The **reversal** is the flame lying down three times, the clock of bad air: the threat changes from being shut in to having no air, and she chooses the dark (the text: "The flame lay down and would not stand") [J reading].
- **Time.** `real_time_continuous` for the pushes. The three lyings-down are `elliptical` (time cuts between them).
- **Capture.** The cheapest Level 4 in either text: push a real closed door, film it locked off, send the 3–5 s clip to Kling Motion Control. The flame is a Level 0 insert.

### WE6. SC05: the drip stand (a strike built from angle, reaction and sound)

"A GUARD comes out of a side room, pistol half drawn, eyes on the stairs. / Iona puts the drip stand across his shins. The pistol skids away. She kicks it hard back down the corridor. / Eli drops to his knees beside the guard and pulls the card off his lanyard."

**Goal:** get past the guard to the cabinet and the cage. **Time design:** `real_time_continuous`. **Geography:** the stair door (the gunfire) at one end of the corridor, the shaft at the other; fix "stairs = frame left, shaft = frame right" for the whole scene and write it into every prompt (A4 C5) [J on the side]. **Mount:** `world`, steady: B1 keeps Iona's steady grammar under fire ("the shots show as sound, sparks and cuts, not shake"). **Reversal:** AB02 (armed guard → disarmed). **Content risk:** low (a pistol is seen, never fired here).

| # | Exact text | Type / cause → effect | s | Contact / risk | Capture / PL / route |
|---|---|---|---|---|---|
| AB01 | "A GUARD comes out of a side room, pistol half drawn, eyes on the stairs." | obstacle | 1.5 | none / low | none / 0 / image_to_video; his eyes toward frame left |
| AB02a | "Iona puts the drip stand across his shins." | attempt; the stand's base swings low, crossing toward the camera (R28) | 0.6 | `body_object`, split / none | Iona's swing: `mime_mocap` with a broom swung at empty air, at half speed (R15, R25) / 4 / first_last_frame |
| AB02b | (the same line) | effect; his legs go out, he drops out of frame bottom | 0.7 | none in this clip / low | `hand_keyed` or Cascadeur, never performed (R25) / 3 / route_2; the hit is a sound only |
| AB03 | "The pistol skids away." | effect | 0.8 | none / low | none / 0 / insert, first_last_frame (pistol at hand → on the floor, sliding) |
| AB04 | "She kicks it hard back down the corridor." | attempt → effect; the pistol slides away toward frame left, into the dark | 1.0 | `body_object` / low | none / 0 / insert of her boot and the pistol; `generate_half_speed_x2` |
| AB05 | "Eli drops to his knees beside the guard and pulls the card off his lanyard." | release | 1.8 | the guard is still, so only one body acts (R20a) / none | none / 0 / hands insert from a checked still (R21): Eli's fingers, the card, the lanyard; the guard's body soft behind |

Total about 6.4 s. The strike is never one clip with two bodies in it: the swing (AB02a) and the fall (AB02b) are separate clips joined by `match_on_action` on the moment of impact, with the impact sound on the cut (R28). If a model refuses AB01 or AB03 for the pistol, move the pistol into compositing after the second refusal (C1 R10).

---

## 10. Checks on the rest of the library (conflicts resolved)

1. **A4/B1/C4 on SC06's fall:** resolved in §3.2 (the blueprint adopted the resolution as K20). Proposed A4 WE1 edits, row by row against WE2 segment C: row 8 1.8 → 0.75 s; row 9 2.0 → 2.2 s; row 11 0.6 → 0.5 s; row 12 0.9 → 0.35 s; row 14 0.7 → 0.8 s; row 15 0.5 → 0.35 s; add "She hooks her fingers deeper into the grid." 0.7 s after row 14; rows 10, 13, 16 and 17 unchanged (row 17's 0.4 s and this file's 0.42 s are both 10 frames). C4 Example A gains a clockless variant: bodies drifting 2–3 s relative to a stationary cage, the shaft unseen.
2. **A4 AI6 vs C5 digest rule 31 (chaining):** R19. **C1's speed-up vs B1's ban on slow motion:** no conflict (R15). **Bordwell's point of rest vs A4 R3:** R9. **Chan's same-frame rule vs C4 digest rule 42:** R11.
3. **B1 Example 2 vs A4 WE1 row 17 (where the CLACK sits):** B1 says "The CLACK is sound over the frame; then true black"; A4 puts "the CLACK on the first black frame". This file follows A4 (the cut and the sound become one event, A4's synchresis argument) [J]; the difference is at most one frame, and the user may choose.
4. **Bordwell's axial cut vs B1's ban on slow motion:** Bordwell's example repeats *and* slows the action (17 frames, then 34). R10 keeps the repeat and drops the slowing.
5. **D10 CM1 (comedy: the punch lands inside a frame holding both cause and victim) vs R11 and R28 (split touching bodies):** for a comic hit, keep D10's shared frame only when the bodies do not touch in it (a pie thrown across the frame); for a touching hit, R28's angle-reaction-sound build in separate clips wins, because the models' multi-subject weakness is the same in comedy [J].
6. **Field names vs the blueprint:** see §5's mapping; the blueprint wins (`time_treatment`, not `time_design`; `route` values; `previs_level` without 1b).

**Open questions for the user**
- Keep the flagged stripe-in-the-descent addition in SC06?
- Accept about 10× expansion for the fall, or test the 9.8 s fallback first?
- Keep the new insert "She hooks her fingers deeper into the grid." as its own 0.7 s shot (it is in the script, but A4 WE1 has no row for it)?
- SC06 CLACK: on the first black frame (A4) or over the last picture frame (B1 Example 2)?
- For SC26's visor clock: should the drawing of the room follow true 4.9 t² at a fixed scale (it leaves the visor within seconds), or a rescaling display that keeps it visible until "Only an arrow points towards it."? The second is my suggestion [J].

---

## Sources

All checked 2026-09-27; the ones marked "re-checked" were opened again on 2026-09-28 in the adversarial pass.

- Bordwell, D., "Bond vs. Chan: Jackie shows how it's done" (15 Sep 2010): https://www.davidbordwell.net/blog/?p=10077 [V, re-checked; his four lessons are clarity, precision, rhythm and amplification; the axial-cut sentence ends "slightly repeated and slowed"].
- Bordwell, D., *Planet Hong Kong* (2000), pause/burst/pause, as quoted in Offscreen, "Action Aesthetics, Part 2": https://offscreen.com/view/action-aesthetics-pt2 (Kyle Barrowman, October 2014; quotes *Planet Hong Kong* p. 221) [V, secondary, re-checked].
- Bordwell and Thompson, *Film Art* 10th ed. glossary (overlapping, elliptical editing; axis of action), University of West Georgia: https://www.westga.edu/academics/university-college/writing/glossary_of_film_terms.php [V, re-checked]. The Filmmakers Academy glossary page formerly cited here for *October* does not mention *October* (re-checked) and is withdrawn as a source for it; *October*'s bridge sequence: Cox, D., "October and the Question of Cinematic Thinking", *Screening the Past* 38: https://www.screeningthepast.com/issue-38-cinematic-thinking/october-and-the-question-of-cinematic-thinking/ [V, secondary].
- No Film School, "Jackie Chan's 9 Principles of Action Comedy" (summarising Tony Zhou, *Every Frame a Painting*, 2014): https://nofilmschool.com/2014/12/jackie-chans-9-principles-action-comedy (3 Dec 2014) [V, re-checked].
- Nedomansky, V., "The Editing of Mad Max: Fury Road": https://vashivisuals.com/the-editing-of-mad-max-fury-road/ [V, re-checked].
- Stork, M., "Chaos Cinema" (Press Play, 2011): https://pressplayredux.com/2011/08/22/video-essay-chaos-cinema-the-decline-and-fall-of-action-filmmaking/ and https://scalar.usc.edu/works/film-studies-in-motion/chaos-cinema-part-1-by-matthias-stork [V].
- Failes, I., "Stuntvis Amps Up the Action", VFX Voice (27 Sep 2018): https://vfxvoice.com/stuntvis-amps-up-the-action/ (quotes Dan Glass and Chris Clements) [V, re-checked].
- Weapons of Choice, "Choreographic Notation for Stage Combat": https://weaponsofchoice.com/the-textbook-of-stage-combat/staging-violence/fighting/choreographic-notation/ [V, re-checked].
- Wikipedia, "Equations for a falling body" (d = ½ g t², g = 9.807 m/s²): https://en.wikipedia.org/wiki/Equations_for_a_falling_body [V, re-checked].
- Kling AI, "Kling Motion Control User Guide" (5 Mar 2026): https://kling.ai/quickstart/motion-control-user-guide [V, re-checked; the 3–30 s limit and the fast-motion and camera advice are stated for VIDEO 2.6].
- Cascadeur plans: https://cascadeur.com/plans [V, re-checked]; Cascadeur help, "Mocap (Alpha)": https://cascadeur.com/help/category/203 [V, re-checked; the page does not say which plans include Mocap: U].
- DeepMotion, Animate 3D pricing and FAQ: https://www.deepmotion.com/pricing-animate3d [V, re-checked; plan prices not shown, multi-person limits U].
- ByteDance Seed, "Introducing Seedance 2.5": https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5 (31 Jul 2026) [V, re-checked].
- Wang et al., "FilmBench: A Film-Grade Benchmark for Cinematic Video Generation" (27–29 Jul 2026), via C5 [S22]: https://arxiv.org/abs/2607.24241; the −31.1 camera-movement figure is in the full text, https://arxiv.org/html/2607.24241 [V, re-checked].
- "Physion-Eval: Evaluating Physical Realism in Generated Video via Human Reasoning" (20 Mar 2026), via C1 [S65]: https://arxiv.org/abs/2603.19607 [V, re-checked].
- Runway, "Introducing Runway Gen-4.5" (limitations: causal reasoning, object permanence, success bias): https://runway.com/research/introducing-runway-gen-4.5 [V, re-checked].
- Roberts, W., "How to Film a Fight Scene: Camera, Angles & Cutting", Filmmaker Genius (updated 14 Aug 2026): https://filmmakergenius.com/academy/how-to-film-action-scenes/how-to-film-a-fight-scene [V, secondary; a teaching site, used only for the long-standing angle-reaction-sound practice].
- Library files A3, A4, B1, B3, C1, C3, C4 (kit plans `plan_cage_fall.json`, `plan_grid_pov.json`), C5 (and its digest), D6, D10, D15; the blueprint (section 7.2, card 15, K20).
- Texts: *The Catch* (workshop revision, 25 Sep 2026); *The Long Places* (revised final), chapter II.
