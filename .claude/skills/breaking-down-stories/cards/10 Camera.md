# Card 10. Camera

Step 6 reads only "Camera system"; step 8 reads only "Slots and moves"; chat apps read it whole. "B1 R6" is rule 6 in B1 §11 and "B1 P5" principle 5 in B1 §1; "B1 Ex3" is worked example 3 in B1 §12. Lenses are full-frame equivalents in millimetres (B1 §0.1).

## The job

In The Catch the camera kneels when Iona kneels, stays still while she is in control, and turns handheld only on three passages where she loses it (B1 §9.2). The camera is a narrator with a body: where it stands, how high, how far and through which lens each say something; if you cannot say what, choose again (B1 P1). Step 6 hands on CAMSYS, a CAMRULE per principal, RESERVE and LENS records; step 8, each SHOT's camera fields, every departure with a `why`.

## Questions in order

1. **Whose scene is this beat?** Put the lens at that person's eye height (B1 R6).
2. **Is this beat a turn?** Give it the scene's most extreme framing: closest if the turn happens inside a person, widest if it leaves them alone or waiting (B1 R1, A2 R4).
3. **Has the script already marked the beat** (a line, a look, a change of state)? Then the camera adds nothing (B1 P11, B4 R23).
4. **Is someone hiding a feeling?** One size wider than the progression would reach, except on a turn (B1 R5, R1).
5. **Is power shifting?** Change angle only on that beat, in both halves of the exchange (B1 R7).
6. **Where does the camera stand?** Position first, lens second (B1 P6).
7. **What causes the move?** Name it, or stay static and cut (B1 P8, R21).
8. **What does the story keep hidden?** Keep it out of frame; never tilt to find it (B1 P7, Ex2).

## Camera system

Example: The Catch frames `2.39` because pairs face each other across glass and tables; spherical lenses, 35 and 50 for people, 85 from scene 13, 24 only in the cage, the ship's wides and Iona's room; the lens at Iona's eye; `static`; dolly zoom, Dutch tilt, slow motion and orbit banned (B1 §9.2).

The **camera system** is the film's written rules for the camera, filled once before any shot, every line with its story reason (B1 §9.1). Its fields:
- `frame_shape_why`: decide once. Upright figures, confinement and faces favour a narrow frame; two or three people in rooms `1.85`; pairs at opposite edges, rows of rooms or a figure small in space `2.39`. A tool that makes only 16:9 serves a `2.39` film by keeping heads, hands and text in the central band (B1 §5; K24).
- `lens_type`: spherical for clinical, documentary honesty; anamorphic for romance, myth and epic width (B1 §4.4).
- `lens_family`: the **lens family** is the short list of lenses the film allows: wide up to about 35, normal about 40 to 58, long from about 75 (B1 §0.1, §4.3). The **normal lens** (`normal_lens_mm`) is the default for every shot's `lens_mm` (REASON-02).
- `step_change`: from a named scene the family shifts (B1 R15). A **lens exception** (LENS, `LX-`) allows one lens at named camera positions only (B1 §4.3; CRAFT-07).
- `default_height`: whose eye the lens sits at (B1 R6); `default_move`: `static`.
- `banned`: choices the film never makes, each with its why (B1 §9.2).
- `camera_speed: real_time`; `time_rule`: expanded action is built from overlapping real-time slices, never slow motion (K20, K30; CRAFT-16).
- `break`: **the break** is the one time the camera does the opposite of its rule, on the turn it serves (B1 P9, R24).

A **character camera rule** (CAMRULE, one per principal) says how the camera treats one person: `in_control`, `losing_control`, `never`, `closest` (a size at a story point), `limit_before` (nothing closer before `closest`), `eyeline`; a **story point** is a scene and a quote (B1 §9.2; FILM-03). Example `CR-ELI`: partial framings, eyes well off the lens, `never: push_in`, `limit_before: medium_close_up` until scene 13, his first near-lens look spent on "Now he looks at her." (line 811; B1 Ex3; K05).

A **saved choice** (RESERVE, `RC-`) names the choice, its `match` (how code recognises a use: `size = extreme_close_up`), most uses, where allowed and never on whom; card 09 adds the two film-level ones (B1 P5, §9.2). An in-story camera keeps its fixed position, lens, frame shape, frame rate and overlays in its CAMERA record (B1 R22).

## Slots and moves

Example: SC10-SH150 is `close_up`, `eye_level`, `height: eye:CH-IONA`, `lens_mm: 50`, `focus: moderate`, `move: static`: the scene's tightest frame on its main turn, with no push-in, because "Her face changes." (line 456) already marks the beat (B1 P11); the film's tightest size waits for scene 13 (K05).

Fill the six camera slots (fields) in B1's order, after `purpose` and `because` (B1 §0):
1. **Size** (`size`). Size equals importance now, and distance is emotional distance (B1 P2, P3). A scene's sizes approach, withdraw, hold or break (B1 §2.2). The turn gets the extreme its camera rules allow (B1 R1); equals get matched singles, same size, lens and height (B1 R3; GEOM-08); a breaking relationship moves from two-shots to singles, or from dirty to clean singles (B1 R4). A **single** holds one person, a **two-shot** two; an **over-shoulder** looks past one at the other; a **dirty single** keeps a soft sliver of the other person, a **clean single** none (B1 §2.1).
2. **Angle and height** (`angle`, `height`). Height is where the lens sits; angle is its tilt (B1 §0.1). `height: eye:CH-IONA` or `kneeling:CH-IONA`: the eye of the person whose point of view the scene holds (B1 R6). Low or high only on the beat power shifts: up at the winner, down at the loser (B1 R7); top-down for a machine's or institution's view (B1 R9); a Dutch tilt only while a perception is wrong, and only as a saved choice, a RESERVE record that rations it (B1 R8).
3. **Lens** (`lens_mm`). Stand first, then choose the lens: how near and far things compare in size depends only on where the camera stands (B1 P6, §4.1). A long lens from far away: closeness kept private (B1 R10); a wide lens close: a person pressed by the place (B1 R11); two people across a barrier: a long lens along the line between them, or the camera in the plane of the glass; a long lens shortens only distances toward the camera (B1 R13).
4. **Focus** (`focus`, `focus_on`). `moderate` for dialogue; `deep` when the audience must read something behind; `shallow` hides what the character ignores (B1 §4.5). A **rack focus** (sharpness moving from one plane to another) becomes two shots for AI video unless a test shows the tool can do it (B1 R14).
5. **Camera move** (`move`, `move_reason`). One per shot (B1 §13; CRAFT-06), with a named cause: a character moves or looks, or a sound draws attention (B1 P8). A **push-in** (the camera travels toward the subject) starts before the realisation and lands on the decision, at most `push_in_per_scene_max` a scene (B1 §6). A zoom is an observer's gaze, not approach (B1 §6). **Handheld** comes in on the exact beat control is lost (B1 R17). An impossible arrival happens in a static frame between cuts (B1 R20). If a cut does the move's job, cut (B1 R21). Orbit, zoom, whip pan, dolly zoom and drone only as saved choices; a crane above head height only for a view nobody in the scene has (B1 §6).
6. **Frame shape** changes only for footage inside the story, shown in its own shape (B1 R22).

A point-of-view shot (`frame: pov`, what one character sees from their eyes) comes in a short dose, then the face (B1 §3.2). A value that departs from its default needs a `why`: `angle` eye_level, `height` the owner's eye, `lens_mm` the normal lens, `move` static, `focus` moderate (REASON-02).

## Translation menus with pitfalls

Change one or two slots, leave the rest at the baseline, and tie the choice to a line, object or action (B1 §8):
- **In control:** medium clean singles, eye level, static. Pitfall: dull competence; show skill in inserts.
- **Losing control:** sizes jump tighter; handheld enters. Pitfall: shake before the loss.
- **Kept hidden:** partial framing. Pitfall: hiding so obviously the audience guesses.
- **Revelation:** an insert, then the face. Pitfall: insert, rack focus and push-in together.
- **Dread:** a static wide, deep focus; the threat never moves the camera (B1 §9.2; D10 §2.2).
- **Confession:** one size held, near the lens line. Pitfall: cutting the truth into pieces.

## Budgets and saved choices

`push_in_per_scene_max` and `extreme_close_up_per_scene_max`, on the main turn only: caps, not quotas (B1 P5; CRAFT-01 to CRAFT-03). Film-level: `extreme_close_up_film_max` and `push_in_scene_share_max` (FILM-08). A saved choice cites its RC in `because` (REASON-06; CRAFT-11). Consecutive shots of one subject change a size step or at least `geometry_angle_change_min_deg` (GEOM-02).

## The baseline is a strong answer

Static, the owner's eye height, a normal lens, room sound are choices, not failures. Depart only for a reason you can cite. The neutral fallback is never wrong and keeps the extremes available (B1 R25); a static frame can judge or trap (B1 §6).

## Cliché traps

Tests as in card 09.
- **Push-in on every realisation.** Fix: one, on the turn, starting before it (B1 §6, §14).
- **Low angle from the first beat; the monster from below.** Fix: eye level until power rises (B1 R7, §14).
- **Dutch tilt for tension.** Test: does the script say a perception is wrong? Fix: level it (B1 R8).
- **Crane-up on every sad ending.** Fix: a pull-back or crane-up ending on at most one scene ending in four (B1 R19).
- **Shallow focus everywhere; handheld as realism; slow motion for importance.** Fix: deep focus where the place matters; handheld only for lost control; real time, held longer (B1 §6.1, §14).

## Reasons that fail and reasons that pass

- Fails: "Low angle to make Saye powerful." Passes: "Eye level on Saye (CR-SAYE: she holds power by stillness, not angle); she wins at SC10-B11 by waiting." (B1 R7)
- Fails: "Push-in as she realises." Passes: "Static: 'Her face changes.' already marks the beat (B1 P11)."
- Fails: "85 for a cinematic look." Passes: "`LX-01`: camera A stands 6.3 metres back, through a wall removed for it, so both profiles in the reflection two-shot are the same size (B3 §6.3; K07)."

## Two worked examples

### The Catch, scene 10 (tense)

SH080, the reflection two-shot: camera A on the table's centre line, `lens_mm: 85` under `LX-01`, `frame_detail: symmetrical_profile`, one of `RC-01`'s two uses (K07, K22). SH150: the turn, above. SH190: the held wide from camera F through "She waits until Iona steps aside." (line 481): a turn about waiting takes a deliberate wide (A2 R4, R18).

### The Long Places, scene 5 (contemplative)

"She did not turn her head." (line 79): a static medium close-up in profile from her left, level, at her seated eye height, on a long lens; her right side, and whatever leans on it, hidden behind her own body. No push-in, pan or reverse: she refuses to look, so the camera refuses too (B1 Ex7; D10 §12.3).

## Self-check

Yes or no (B1 §13).
1. Does every camera-system line give a story reason?
2. Does every principal have a camera rule, kept?
3. Is the scene's most extreme framing the camera rules allow on its turn, nothing tighter before?
4. Is every lens in the family or a declared exception?
5. Does every move name its cause, one per shot?
6. Is what the story hides out of frame?

## Words for AI models

Works: "The camera holds completely still for the whole shot."; "The camera moves slowly closer to her face while she stays still." (B1 §15); one move per clip, saying where it ends; "over Iona's left shoulder toward Saye" (C3 §4). Fails: rack focus, dolly zoom, whip pan, zoom as distinct from push-in, "objective camera", a frame shape in the prompt (B1 §15; C3 §4). A lens number is a hint: write "compressed background, shallow focus" (C3 §4).

## Look up for more

`stage.py lib B1 §9`, `B1 §11` (R1 to R25), `B1 §2`, `§4`, `§6`, `§8`, `§12`, `§14`, `§15`; `C3 §4`; `D10 §2.2`; K05, K07, K20, K22, K24, K30.
