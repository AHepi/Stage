# Digest B1: Camera, lens and movement

Source: `research/B1_camera_lens_movement.md` (745 lines). Brackets: P# = principle (§1), R# = decision rule (§11), § = section, Ex# = worked example (§12). "Consider" = the default; depart only for a higher-priority rule or the film's camera system, and write the reason in the shot's WHY slot.

## 1. Scope

1. Per shot: shot size, angle and height, lens, depth of field/focus, movement, aspect ratio and camera speed, each with a story reason. The camera is a narrator with a point of view (how close, whose side, what we may know).
2. Adds a film-level **camera behavior system** written before any shot, a one-line six-slot shot spec, 25 rules, a checklist, AI phrasing and Blender settings.
3. Runs after beats/turning points (A1/A2), before prompts (C3) and previs (C4). Designs *The Catch*'s system and its impossible camera situations.

**Terms** (§0.1): *height* (lens above floor) is not *angle* (tilt). Focal lengths are **full-frame equivalents** (36 mm wide sensor, Blender's default, matched by frame width): *wide* 14–35 mm, *normal* 40–58, *long* 75+ (36–39 ≈ slightly wide normal; 60–70 ≈ mild long). *Push-in/pull-back*: body travels; *zoom*: focal length changes, camera stays; *truck*: sideways; *pedestal*: rise/sink without tilt ("vertical" in some AI tools); *leading*: following from ahead. *Motivated* move: caused by a character's movement, look or a sound. Stances (after Mascelli): *objective*; *subjective* (direct address, or through the eyes); *POV* (modern sense: what one character sees from their eye position); *near-POV* (camera just beside a character at their eye height). *Dirty/clean* single (blurred sliver of the other person / nobody else). *Emphasis device*: push-in, rack focus, ECU, angle change, lens change, slow motion, crane (outside camera: music sting, a line stating the point). *Lens family*: the film's allowed focal lengths; *step change*: it shifts from a scene on. *Handedness*: left/right-ness, like a glove. *Diegetic footage*: footage inside the story. *Master take*: one continuous recording all excerpts are cut from.

## 2. Rules

**Priority on conflict** [§11]: (1) in-story footage and impossible physics (R22, R23); (2) the film's camera system incl. banned/reserved choices; (3) turning-point rules (R1, R7, R17, R24); (4) the rest; (5) fallback (R25).

**Principles**
1. [P1] If you cannot say the sentence a camera choice makes ("we are below him"), then choose again, because every placement is a statement.
2. [P2, P3] If sizing a subject, then size it by its importance now and read size as social distance (CU intimate, medium personal/social, wide public), because audiences do (Hall, Giannetti).
3. [P4] If using any departure (long lens, low angle, handheld), then set a baseline first and spend departures on turning points, because change is the signal (Block: contrast raises intensity, affinity calms).
4. [P5] If using extremes, then default budgets: ≤1 ECU per scene, only on the turning point; ≤1 push-in per scene; dolly zoom, orbit, Dutch tilt, unmotivated overhead ≤1–2 per film each; crane-up/pull-back ending on ≤1 scene in 4 — because extremes work by rarity.
5. [P6, §4.1] If choosing a lens, then place the camera first, lens second, because perspective comes only from position; "compression" is distance and "wide-lens distortion" is closeness.
6. [P7] If the script withholds something (a hidden hand, an unseen presence), then keep it out of frame, because withholding is authored.
7. [P8, §6] If a camera moves, then name its motivation; unmotivated moves only when the narrator knows what characters do not.
8. [P9] If a rule has held most of the film, then break it once at the turning point it serves, because the break is an event.
9. [P11] If a beat already carries an emphasis device (face, dialogue or sound), then the camera adds nothing; if none, add one; never two, because stacking is the trailer version.

**Shot size**
10. [R1] If a beat is the turning point, then give it the scene's most extreme framing — closest if the turn is inside a person (realization, decision, confession, exposed lie), widest if it leaves them abandoned or small — because size is the loudest signal.
11. [R2] If the audience must read an object, then use an insert held to read twice: ≥2 s plus ~0.5 s per word, because unread information is not information.
12. [R3] If two characters are equals, then match their singles (size, lens, height), because a mismatch reads as power.
13. [R4] If a relationship is breaking, then move from two-shots to singles, or dirty to clean singles, because the cut becomes the separation (a return to the two-shot joins or traps them).
14. [R5] If a character hides a private emotion, then stay one size wider than the progression would reach, because the audience leans in.
15. [§2.1, §3.2] If tempted to default to close-ups or long POV, then ration them, because close-ups aid mind-reading only up to a point (Bálint et al. 2020) and POV loses the face (POV, then the face).

**Angle and height**
16. [R6] If the scene belongs to one person, then put the lens at their eye height, level (they kneel, it kneels), because height is where the audience stands.
17. [R7] If power shifts, then change angle only on that beat and in both halves (slightly up at the gainer, down at the loser, in matching reverses), because a low angle from beat one is decoration.
18. [R8] If you want a Dutch tilt, then only while the script says a perception or world is wrong, levelling when it rights, because "the scene is tense" is never enough.
19. [R9, §3.1] If a view belongs to a machine, institution or fate, then use a top-down or high fixed frame, because it removes the human horizon; a high angle also withholds a face honestly (read as geography).
20. [§14] If a threat appears, then low angle only where the viewer character is face to face and afraid, eye level elsewhere, so the angle can change when the truth does.

**Lens and focus**
21. [R10] If a face should feel close but private, then 85–135 mm from ~2–4 m, because it gives intimacy without intrusion.
22. [R11] If a character is pressed by surroundings, then 24–28 mm within ~1 m of the face, because the world stays large around them.
23. [R12] If someone runs and should not arrive, then ≥200 mm, subject ≥50 m away moving toward camera, because apparent size barely changes.
24. [R13] If two people must feel together across a barrier, then (a) a long lens from far away looking along the line between them at a shallow angle, or (b) a profile two-shot with the camera in the barrier's plane (glass edge-on = a thin line), because compression only shortens distances toward the camera, never across the frame.
25. [R14] If the scene is about noticing, then rack focus on the noticing beat; for AI video, split into two shots unless a test shows the tool can rack.
26. [R15, §4.3] If a turn should be felt below notice, then step-change the lens family from that scene (or use one single-exception lens), tied to a named story change.
27. [§4.5] If setting depth of field (full-frame, MCU distance), then: shallow f/1.4–2.8; moderate (dialogue default) f/4–5.6; deep f/8–16, usually on 24–35 mm. If anything behind the subject must be read, it cannot be shallow.
28. [§4.5, §4.4] If using a split diopter, then ≤1–2 per film (conspicuous). If the film is romantic/dreamlike/epic, consider anamorphic; if clean/clinical/documentary, spherical.
29. [§4.2] If copying a quoted focal length, then convert to full-frame first (Procedure 5).

**Movement**
30. [R16] If a character is in control, then static or smooth moves at their pace, because steadiness reads as competence.
31. [R17, §6] If control is lost, then handheld on the exact beat, not before, because early shake spoils the surprise. Choose handheld vs stabilizer per character and state of control, not genre.
32. [R18] If the narrator knows something characters do not, then one unmotivated move in that scene, no more.
33. [§6] If a character realizes, then push in (start before the realization, land on the decision); if an observer or machine watches, then zoom. If the performance already shows it, hold still. No push-in on a character whose rule forbids it.
34. [§6] If considering a dolly zoom, then at most once per film, on a perceptual shift only, because it reads as a *Vertigo* quotation.
35. [R19] If a scene ends on consequence or isolation, then pull back or cut to a wide landing on the last beat (≤1 scene ending in 4), because withdrawal is a full stop; mid-scene it deflates.
36. [R20] If something should appear impossibly, then a static frame where it is simply there after a cut or frame jump, because a move implies a path.
37. [R21] If a cut does the move's job, then cut, because moves cost attention and AI stability.
38. [§6] If using an orbit, a crane above head height or a drone, then only for a view no one in the scene could have (fate, institution, an ending), never as opener or "hero moment", because they are the narrator speaking; an orbit needs an axis reason and a quarter/half-circle duration.
39. [§6] If travelling with a character, then follow (shared path, face hidden), lead (face shown, destination hidden: suspense) or truck beside (companionship), because each sets what is hidden; slow reads inevitable, fast alarmed.
40. [§6] If placing cameras, then record the scene's axis first; a deliberate crossing is one of the scene's extremes; a flipped clip counts as a crossing (full rules: A4 §3, B3 §5.2).
41. [§6.1] If a moment should feel slowed, then hold longer in real time with less happening first; slow motion only when a character's time perception truly changes and is set up, budgeted as an extreme.

**Ratio and systems**
42. [§5] If a ratio change is proposed, then name the story fact it marks, or do not change.
43. [R22, §6.1] If footage exists in the story, then show it in its native ratio with fixed camera behavior (a 10–15 fps stutter marks a recording), because the shape says "recording".
44. [R23] If physics is impossible, then the camera obeys the characters' physics (falls with them, bolted to their vehicle), because honest camera behavior sells it.
45. [R24] If a character's inner state inverts at the climax, then invert their camera rule there.
46. [R25, §0] If unsure, or a slot has no story reason, then the system's default, else normal lens, eye height, static; never an invented flourish.
47. [§10.2] If a black or turn separates two shots, then repeat size, lens and position, so the world changes, not the camera.
48. [§13] If a clip is AI-generated, then at most one camera move; cut between clips.

## 3. Breakdown fields

The file names the slots SIZE, ANGLE/HEIGHT, LENS, FOCUS, MOVE, RATIO, WHY and the §9.1 labels; snake_case names are this digest's.

| Level | Field | Meaning | Values / example |
|---|---|---|---|
| film | `camera_system` | §9.1 template, filled once | Procedure 2 |
| film | `aspect_ratio`, `lens_type` | Frame shape; glass | 1.33/1.37 \| 1.66 \| 1.85 \| 1.78 \| 2.39 \| 9:16; spherical \| anamorphic |
| film | `lens_family`, `lens_step_changes[]` | Allowed mm and exceptions; shifts at turns | {default: [35, 50], exceptions: [{mm: 24, only_when}]}; {from_scene, add: 85, story_change} |
| film | `default_height`, `default_movement` | Baseline | "Iona's eye height"; static \| smooth \| handheld + motivation |
| film | `reserved_choices[]`, `banned_choices[]`, `extreme_budgets` | Rationed/forbidden choices; P5 overrides | {choice, max_uses}; {choice, reason} |
| film | `camera_speed`, `diegetic_footage[]`, `the_break` | Frame-rate policy; each in-story camera; the one inversion | {position, lens, ratio, movement, frame_rate, overlays, master_clip}; {beat, does, because} |
| film | `mirror_phases[]` (*Catch*) | Handedness phases | {id: A\|B\|C, from, to, mirrored[], not_mirrored[]} |
| scene | `turning_point_beat`, `size_progression` | From A2; the dial's shape | approach \| withdrawal \| hold \| break |
| scene | `axis_of_action`, `system_departures[]` | Line and crossings; departures with reasons | {line, crossing: none \| declared extreme} |
| beat | `emphasis_device`, `emphasis_already_present`, `power_shift` | One camera device; what performance/dialogue/sound carry; who gains | none \| push-in \| rack \| ECU \| angle change \| lens change \| slow motion \| crane |
| shot | `shot_size`, `framing` | Size; combination | EWS \| WS \| MWS \| MS \| MCU \| CU \| ECU \| insert; single \| two-shot \| OTS \| POV \| near-POV; dirty \| clean \| symmetrical profile |
| shot | `camera_stance` | Mascelli switch | objective \| subjective (direct address) \| near-POV \| POV |
| shot | `angle`, `camera_height` | Tilt; whose eye height | eye level \| low \| high \| top-down \| worm's-eye \| Dutch; "Iona kneeling" |
| shot | `lens_mm` | Full-frame equivalent in family | 24 \| 35 \| 50 \| 85 \| macro |
| shot | `depth_of_field`, `focus_target`, `rack` | Sharp zone | shallow \| moderate \| deep; {from, to, on_beat} |
| shot | `movement`, `move_motivation` | One move; its cause | static \| pan \| tilt \| push-in \| pull-back \| truck \| pedestal \| follow \| lead \| zoom \| handheld \| stabilized \| crane \| drone \| orbit \| whip pan; character move \| gaze \| sound \| narrator: <reason> |
| shot | `aspect_ratio`, `camera_speed` | Only if not default | "4:3 inside 2.39"; real time \| slow motion (<action>) \| 12–15 fps |
| shot | `eye_line`, `withheld`, `camera_mount` | Look; what is kept out and how; physics binding | off lens \| near lens line \| into lens; "arm exits bottom of frame"; bolted to cage \| ship \| attached to Iona \| world-vertical |
| shot | `why` | Story fact per slot | "she has found the proof and does not show it" |
| shot | `handedness_phase`, `flip` | *Catch* | A\|B\|C; unflipped \| method 1 \| 2 \| 3 |
| character | `camera_rule` | Per-character grammar | {in_control, losing_control_or_revealed, trigger_beats[], eye_line_rule} |
| location | `lens_allowance`, `mount` | Location camera rules | "ship spaces: 24 mm wides"; "ship: bolted, no roll" |
| prop | `mirror_treatment` | Asymmetric/text props | pre-reversed \| mirrored prop \| exception prop |
| motif | `reserved_framing` | Framing kept for rhymes | symmetrical profile two-shot for reflections; same insert for meal label and RECEIVING |
| generation job | `one_move`, `ratio_in_tool`, `safe_band`, `start_frame`/`end_frame`, `motion_guide`, `flip_plan` | AI constraints | 2.39 crop from 16:9: heads, hands, text out of top/bottom eighths; flip ref → generate → flip output |
| previs job | `blender_camera` | Exact camera | {focal_mm, sensor_width: 36, sensor_fit: Horizontal, focus_object \| distance, f_stop, parent, clear_parent_at} |

## 4. Procedures

**P1. Order of work** [§0]
1. Write the camera behavior system (P2).
2. Per scene, find beats and turning point; plan a size progression (P4) reaching its most extreme framing on the turn, not before.
3. Per shot, fill six slots in order — size; angle/height; lens; depth of field/focus; movement; ratio if it changes — each with a one-line story reason, on one line:
   `SIZE: medium close-up | ANGLE/HEIGHT: level, at Iona's kneeling eye height | LENS: 50 mm | FOCUS: shallow, on Iona's face | MOVE: static | RATIO: 2.39:1 (film default) | WHY: she has just found the proof and does not show it; the camera stays down with her and does not dramatize.`
   A slot with no reason takes the system default (or R25).
4. Run the §13 checklist on every shot; the §11 rules where a slot is uncertain.
5. Only then write prompts (§15).

**P2. Camera system template** [§9.1] (exact)
```
CAMERA SYSTEM: <film title>
Aspect ratio: <ratio>, because <story reason>
Lens family: default <mm>, <mm>; exception lens <mm> only when <condition>
Default height: <whose eye height>, because <reason>
Default movement: <static / smooth / handheld>, motivated by <what>
Per character:
  <Name> in control: <size, height, movement>
  <Name> losing control: <what changes>
Reserved choices (max 1-2 uses each): <ECU on X, overhead, dolly zoom...>
Banned choices: <moves or framings this film never uses, with the reason>
Camera speed: <real time everywhere / slow motion only when...>
Diegetic footage: <each in-story camera: position, lens, ratio, movement, frame rate, overlays>
The break: at <scene/beat>, the camera does <opposite of its rule>, because <turning point>
```
Derive every shot from it and log each departure with a reason; the recurring lens/height/movement words also keep AI shots consistent.

**P3. Aspect ratio, decided once** [§5]: upright figures, confinement, faces → 1.33–1.66; two or three people in rooms → 1.85; landscapes, pairs at opposite edges, rows of rooms, small figure in space → 2.39; phone feed → 9:16 with vertical action; tool outputs only 16:9 for a 2.39 film → compose for the central band, crop in the edit. Diegetic footage in its own shape is the cheap motivated ratio change.

**P4. Size progression** [§2.2]: *approach* (wide → close, closest on the turn; the default); *withdrawal* (close → wide as someone is abandoned); *hold* (one size while content changes; a trap, an undramatized confession); *break* (a sudden jump on the shock beat, only after gradual steps). Design from the turn, not from default coverage.

**P5. Convert a quoted focal length** [§4.2]: multiply by 36 ÷ image width. Full-frame / ALEXA LF / Mini LF / Blender ×1.0; Super 35 digital 16:9 ×1.5; 35 mm film Super 35 ×1.45; Academy 1.37 ×1.6; 2x anamorphic ×0.8 (field of view only); ALEXA 65 ×0.67; 65 mm 5-perf ×0.7; IMAX 15-perf ×0.5; phones ×1.0 (already equivalent).

**P6. In-story footage** [§10.4]: (1) fix one camera: position, lens, ratio, frame rate, overlays, exposure; it never moves or reframes (characters may pause, rewind, digitally enlarge). (2) Design it backwards from its reveal (what it must show that the story camera hid). (3) Build one continuous master clip; cut every excerpt from it. (4) Apply phase/mirror rules to the whole picture.

**P7. Mirror-world method** [§10.2]
| Shot contains | Use |
|---|---|
| Mostly world, turned characters small | **Method 1, flip and compensate**: pre-reverse turned things (ring, bandage, control box), generate normally, flip the clip. For AI: flip the character reference before generating, then flip the output. |
| A turned character's face large | **Method 2**: unflipped character composited over a flipped background. |
| World text to be read | **Method 3**: mirrored prop; or Method 1 with text generated normally and flipped with the clip. |
| A world-made screen, phase B | Flip its whole picture; a turned character live on it is pre-reversed inside it; a pre-turn recording flips entirely. |
| No asymmetric detail or text | No flip, unless cut with flipped shots of the same space. |
Phase C: flip only Eli's and Jude's singles (no readable text behind); in two-shots with Iona, put Jude's ring on his right hand directly.

**P8. Frames and previs** [§15]: a still shows the move's most important moment (usually its landing), with the move kept in the text. Where a tool takes start (and end) frames, generate storyboard frames first and let the model travel between them (most dependable for a specific push-in or reveal). When words fail, feed a Blender previs frame as the start image or a clip as a motion guide.

**P9. Blender** [§15; manual 5.2, checked 2026-09-27]: focal length in mm (default 50) on a 36 mm sensor; Sensor Fit = Horizontal, 36 mm (Auto uses the longer side, the height in 9:16); DoF by Focus Object/Distance and F-Stop (lower = shallower); Ratio simulates anamorphic blur; decreasing focal length while moving toward the object = dolly zoom; parent the camera to the cage to "bolt" it, and clear the parent at the black so post-turn shots stay world-vertical; flip mirror-phase clips in any editor.

**P10. Reserved-choice audit** [§14]: before approving a scene, search the shot list for each reserved choice (look into lens, first close-up, first handheld, first long lens, symmetric frame); move early uses back to baseline.

**P11. Translation menu** [§8] — pick the one or two columns the beat needs; leave the rest at baseline (P11 principle). Meaning → size / angle / lens-focus / move (pitfall):
- In control → medium clean singles / eye level / normal, moderate / static or pace-matched (boring competence: use inserts of skill).
- Losing control → sizes jump tighter / drifts off level / wider, closer / handheld enters (shake before the loss).
- Withheld information → partial framing / objective / shallow focus hiding it / static or stopping short (hiding too obviously).
- Revelation → insert or ECU, then face / level / rack object↔face / push-in landing on the beat (choose one of insert, rack, push-in).
- Power rising → their singles tighten / lower on them, higher on the other / longer lens on them / their frame steadies (low angles from beat one).
- Vulnerability → wider / higher / deep focus / pull-back (crane-up on every sad moment).
- Intimacy → two-shot or matched close singles / level / long lens along the line between them / slow, minimal.
- Separation → singles, or wide two-shot with a gap / mismatched heights / wide from close exaggerating a gap toward camera / static.
- Isolation → EWS or tight single on blank space / level or high / long with soft blank background, or wide with empty space / pull-back or static (lonely drone shot).
- Dread → static wide with empty areas / slightly high or corner / wide deep focus / static or very slow push to empty space.
- Being watched → wide off-axis / high corner / long lens, foreground obstruction / static or mechanical pan.
- Awe → EWS with a figure for scale / low or worm's-eye / wide / crane up or slow tilt.
- Confession → one held size / eye level near lens line / normal to long / static or one slow push-in (coverage chopping the truth).
- Grief → wide or held medium / level / normal / static long takes (ECU tears).
- Disorientation → unexpected sizes / Dutch or rolled / wide, close / handheld or rotating.
- Shared perception → POV then reaction / their eye height / normal / motivated by their head and eyes.

## 5. Checklists

**Scene** [§13] (a "no" needs a fix or written reason): system written and followed, or departure recorded? Turning point found, strongest framing there and not earlier? Extremes within budget and on beats that need them? At most one emphasis device per beat, counting performance, dialogue, sound? Dialogue singles matched unless power shifts?

**Shot** [§13]
- One sentence for what the size says about distance now?
- Lens at the experience owner's eye height; any angle tied to a named power/perception change?
- Position chosen before lens? Focal length full-frame, in family or declared exception?
- Depth of field hides only what the story hides, shows all that must be read? Focus shifts only on a noticing beat?
- Every move motivated or narrator-reasoned? At most one move (required for AI)?
- Withheld things kept out of frame? Impossible physics obeyed by the camera?
- In-story footage: same position, ratio, lens, overlays and content every viewing?
- *Catch*: phase A/B/C, every asymmetric detail (text, rings, wheel, smile, control box) on the right side? Flipped state matches all shots of that space in that phase?
- Axis recorded and respected, or crossing declared?
- Real time? Slow motion only if the system allows and perception changes?
- Symbols (glass, reflection, bars) present because the beat needs them, not the location?
- Would a cut do the move's job? Then cut.

**Mistake scan** [§14] (name → fix): default coverage → design from the turn; extremes early → move to the turn; floating camera → delete unjustified moves; tension by tilt → level it; reflex low angles → eye level until power rises; shallow everywhere → deep focus for establishing/relational shots; copied focal lengths → convert; lens before position → place first; handheld as realism → tie to loss of control; late/constant push-ins → start before, ration; endless POV → POV, face, POV; heavy symbolism → reserve one beat; showing the withheld → keep offscreen; dishonest physics → bind to body/vehicle; inconsistent footage → one master clip; stacked AI moves → one per clip; compression across frame → shoot along the line or barrier edge-on; slow motion for importance → real time held; monster low angle → only face to face and afraid; stacked emphasis → one device; payoff spent early → audit (P10).

## 6. Saying it to AI models

Model behavior changes with versions; generate and look [§15].
- **Documented (checked 2026-09-27):** Veo 3.1: order cinematography, subject, action, context, style/ambiance; its terms include medium shot, two-shot, low angle, dolly, tracking, crane, aerial, slow pan, POV, 180-degree arc, shallow depth of field, wide-angle, macro, deep focus. Sora 2: describe like a storyboard (framing, lens, depth of field), one camera move and one subject action; shorter clips follow better. Runway Gen-4: no negative phrasing (can do the opposite) — "camera holds completely static", not "no camera movement"; short verb-led motion. Kling: sliders (horizontal, vertical, zoom, pan, tilt, roll) beat words, but vary by version and labels differ ("vertical" = pedestal; check which of pan/tilt turns left-right); test one clip per control.
- **Usually works:** shot sizes, two-shot, OTS, low/high angle, top-down, eye level, POV, handheld, static, slow push-in/dolly in, tracking (= follow), pan, tilt, crane up, aerial, shallow depth of field, deep focus, wide-angle, macro. 24/35/50/85 mm act as style hints, not optics.
- **Often fails** (practice; test): rack focus, split diopter, dolly zoom/"Vertigo effect", "truck" (a vehicle), zoom vs push-in (same drift), "objective/subjective camera", ratios in the prompt (set in the tool), "anamorphic" (flares, no squeeze), anything relying on something staying out of frame, mirrored text (flip in the edit).
- **Rephrase:** rack focus → "Focus starts on the cloudy shape inside the clear container, then shifts to the reflection on its curved surface." Static → "The camera holds completely still for the whole shot." Truck left → "The camera slides sideways to the left, parallel to the wall." Push-in on realization → "The camera moves slowly closer to her face while she stays still." Hide his hand → "Close-up of his face and shoulder in three-quarter view, his eyes fixed on someone just out of frame to the left; his right arm runs down behind the other man's back, out of the bottom of the frame." Figure too tall → "Camera near the floor looking up; the tall black figure's head is cut off by the top of the frame." Zero-g → "Everyone floats slowly, in real time; the camera is perfectly steady; only the brick wall beyond the steel grid streaks upward, faster and faster." Slow motion: say which action ("in slow motion, the cup tips and falls") or the whole scene slows.
- **Example (Ex1 insert):** "Extreme close-up, macro lens, torchlight from the left: a woman's fingertip slides into a bright, empty bolt hole in greasy steel; the fresh, sharp thread glints. Shallow depth of field. The camera holds completely still. Cold, wet, dark brick tunnel."
- **Speed** [§6.1]: fixed frame rates; "slow motion" usually honored, shutter angle not controllable; fast action smears — generate slow, speed up in the edit (C1).

## 7. The Catch

B1 names scenes by content, not number (other digests: opening = sc1, CLACK = sc6 in A3; confession = sc13 in A2).

**System** [§9.2]
- **2.39:1** (pairs across glass/tables, rows of glass rooms, the figure "Taller than the door"). Insets: security camera 4:3; tablet and Saye's monitors 16:9.
- **Spherical lenses** (clinical register; flares would decorate). 35/50 mm for human scenes; **85 mm from the confession on** for dialogue singles and the final reflection two-shot (step change). **24 mm only**: inside the cage in the shaft; wides of ship spaces (service cavity, long chamber, collection room, ledge; ship faces stay 35/50); the figure in Iona's room. Macro for reserved inserts.
- **Height:** Iona's eye height; she kneels, it kneels.
- **Iona:** static/smooth at her pace; inserts follow her torch and fingers; under fire she is still acting, so no shake. Handheld, closer, wider (35 where the scene was 50; 24 only in her room) on exactly three passages: broken rung ("It rolls. Her foot goes." → "She gets a foot on the rung below."; at "the rung TURNS"/"She goes still", the camera stills), the car ("Hits the door." → end of drive), the figure in her room ("She turns." → "The figure is gone.").
- **Eli:** partial framings, profile/three-quarter, eyes well off lens, a hand often hidden, never a push-in. Confession: closest, most frontal on "You." with eyes on the monitor; first near-lens look on "Now he looks at her."
- **Saye:** through glass, centred, static, 50 mm from farther back than anyone; recorded Saye (lost "the voice she uses for answers") off-centre and closer on the wrist display.
- **Jude:** warm medium two-shots with Iona; static and patient when injured; never handheld.
- **The figure:** while a threat, it never causes a camera move (Iona's handheld shake may carry, but the frame never travels to it); it appears in static frames, between cuts/video frames. Looming frame (low, 24 mm, head cut off) once, in Iona's room; tablet: high corner; ship: Iona's eye height, 35 mm, whole head. Helping (air tank): frame at her height, levels as it bends. Chest: see Ex5.
- **Reserved:** top-down only for recordings and Iona's downward POVs (cage floor grid; ship's low window); symmetrical profile two-shot only for the two reflections (kitchen hands; final rings); handheld only on the three passages; Eli near lens once; looming low angle once.
- **Banned:** dolly zoom; Dutch tilt (the film's wrongness is handedness); slow motion (fall in real time; only the security camera's stutter alters frame rate); orbit.
- **The break:** stillness = control, shake = its loss. On the ship's ledge, at greatest danger, the camera is dead still (free fall has no sensation); on "She pushes gently away from the rail" it floats with her by her choice — floating now means control.

**Impossible situations** [§10]
- **Cage:** bolted inside, 24 mm; speed only through the grid. STOPS DEAD: frame stops, bodies lurch a hand's width, one few-frame shudder (the only shake). Fall: no shake, real time, drifting bodies, hanging "round red beads", only the shaft wall streaking and accelerating. "The opening flicks past. Going up." = level sideways POV through the gate (design the gate as open mesh); "The yellow stripe. Coming." = POV down through the floor grid, growing shot by shot as the fall's clock.
- **Mirror world:** the frame's handedness belongs to Iona. A: opening → the CLACK, nothing mirrored. B: "Her eyes open" → the black beside the ship; the world is mirrored (shaft, building, all text, city, her car, Saye, the nurse, Nell, world-made screens and suits); not Iona, Jude, Eli, cage, flask, their clothes, turned meals, ship interior. C: second turn → end; Jude, Eli and their meals mirrored; not Iona, the vessel, the animal. First cue is screen direction (the opening approaches from the other side going up). Post-turn shaft shots world-vertical (the camera stops following the upside-down cage). No readable shaft text (turn the red tag away). Shoot "RECEIVING" and the turned-meal label identically (same insert size/lens, same face framing, read twice). Axis rule: within a phase all shots of a space are flipped or all unflipped.
- **Ship:** grounded, level, bolted; no roll or float; dips show as stars shifting in the low window. Lurches: frame drops and catches with the deck, loose things move, ≤1 few-frame shudder. Falling: dead still; the screw rises, knees lift, the visor drawing goes "up and up the glass"; no exterior until she leaves; then the camera is attached to her and never corrects her orientation.
- **Surveillance:** above the top gate, straight down; wide, slight barrel distortion, 4:3, low-res, ~12–15 fps, timestamp, fixed exposure the cage lights flare; one master take; the puck is the darkest object and Eli's empty hand visible from above. Mirrored in phase B (backward overlay, control box swapped): do not fix; keep puck and hand readable.
- **Tablet:** establish on her knees; cut to the feed full screen (16:9 in 2.39): high corner, wide, static, desaturated, small overlay, mirrored. Figure appears by frame jump; cut to her face only after the room is empty. Her room then takes the feed's grammar (Ex4: same corner position; the needle insert matching earlier ones; pump sound offscreen first; the 24 mm handheld low-angle break whose frame never travels toward the figure and steadies on "The figure is gone.").
- **Other cameras:** camera sent across — 16:9 on Saye's monitor with corner diagram; tumbles, lies static, is carried (optional bob to the pump's "three strokes, not quite even"). VISOR VIEW — Iona's POV, full 2.39, graphics flat on the glass (no parallax). Wrist display — always an insert on her glove; one or two words or a number, held for R2's time; backwards in phase B (open). All vanishings/arrivals — between two frames of a static shot; no move, dissolve or glow; only the needle and sound. Suit camera/container — figure only in the reflection, rack from contents to reflection, no reverse until it "reaches past her shoulder". Carriage demo — objective, flat, side-on static frame at ramp height, even light; the same framing becomes the wrist recording ("Down. Turn. Up.").

**Examples** [§12]: Ex1 kneeling — camera already at kneeling height, 50 mm medium, macro bolt-hole insert, static hold on "One breath." (the turn), 35 mm with Jude's head cut off; no push-in. Ex2 fall — Eli 35 mm three-quarter close single, eyes on off-frame Iona, arm out the bottom of frame, never tilt to it; CLACK over picture, true black, phase B. Ex3 confession — wides with the monitor → OTS → first 85 mm singles; "Silence." held on Iona; palm insert after "Nothing in it." Ex5 chest — 35 mm looking up → motivated tilt down → macro animal from above then level; "A suit." static 50 mm on Iona. Ex6 rings — symmetrical profile two-shot, camera in the glass's plane, eye level, 85 mm from well back; the second and last symmetric two-shot.

**Also *The Long Places* (Ex7):** Ch. I warmth — static profile MCU from her left, level, seated height, 75 mm; the warmth stays hidden behind her body; no move or reverse (the camera refuses to look, as she does). Same rule for Yusuf's phone footage in Ch. VI ("the niches only").

**For the user** [§16]
- **Phase B screen text** (monitors, "NELL ROWAN. FLIGHT TEST.", visor, wrist): recommended keep backwards — few words, large, ~2× reading time, icons and color carry meaning; the visor snapping readable after the final turn becomes a cue. Alternative: the technician mirrored her display (legible, breaks the rule once).
- **The F carriage:** the rule says the world-made F looks backwards before any turn; the script says the opposite. Recommended: the two Fs as exception props, pre-reversed inside flipped shots so they read as scripted (correct → backwards → correct); applies also to the wrist recording ("Its F reverses"). Confirm.
- **Copied "IONA VALE" label:** assumed backwards to Iona, like the wristband. Confirm.
- **Delivery ratio:** 2.39 recommended; compose 16:9 generations for the crop, or choose 1.85.

## 8. Conflicts and open questions

- **Reading time vs A4:** B1 R2 = ≥2 s + ~0.5 s/word, read twice; A4 R8 = insert ~1 s, text ~1 s + ≤12–15 chars/s. Both double mirrored text. Pick one.
- **Mirror method** (flagged in the A3 digest): B1 mixes three methods by shot type; A3 prefers building mirrored; C1/C2/C3 prefer generate-and-flip with pre-reversal. Decide once.
- **Phase boundaries:** B1 ends phase A at the CLACK, starts B at "Her eyes open", ends it at the black beside the ship; A3's digest says CLACK (sc6) to her turn (sc27). Align to the exact shot.
- **Confession vs A2:** A2's digest has sc13 B15 as "a push-in to a big close-up played in singles"; B1 bans push-ins on Eli and plays static 85 mm singles with the eye-line payoff. "Big close-up" is not on B1's ladder.
- **ECU budget vs inserts (internal):** P5 allows one ECU per scene, only on the turn, but Ex1's evidence insert is prompted as "Extreme close-up, macro lens" before the turn. The ladder lists inserts separately; state whether they count.
- **R1 vs R5 (internal):** hidden emotion on a turning beat — by priority R1 wins.
- **Overlaps to assign:** shot-size defaults (A2 Step 6), axis/30° rules (A4 §3, B3 §5.2), in-frame symbolism (B4), replay setups (A3, consistent with master take), slow motion as a budgeted extreme (A4, consistent).
- **Unverified:** *The Graduate* "about 500 mm"; Deakins and Bradford Young figures, the Runway guide and *Mommy*'s widening read only through search results; "often fails" AI terms from practice; Kling varies by version; Hitchcock line is a paraphrase.
- **Tool dependence:** rack focus, out-of-frame withholding, mirrored text and free-fall physics are unreliable in models; C1/C3/C4 should confirm current start/end-frame, motion-guide and slider support. Check the Sensor Fit note against C4's previs kit.

## 9. Section map

- **§0** Order of work (5 steps), six-slot line, fallback; **§0.1** terms.
- **§1** Principles P1–P11 (budgets P5; one emphasis per beat P11).
- **§2** Shot size: 2.1 ladder table, combinations, Bálint study; 2.2 four progressions, shot pairs.
- **§3** Angle/height: 3.1 options table, Ozu/*E.T.* height, Lumet's height plan, *Kane*, Dutch warning, *Psycho* overhead; 3.2 camera stances.
- **§4** Lenses: 4.1 physics; 4.2 lens-range table, practitioner examples, conversion table; 4.3 families and changes; 4.4 spherical vs anamorphic; 4.5 depth-of-field numbers, rack, split diopter.
- **§5** Aspect ratio table, ratio changes, choice rules.
- **§6** Movement ideas (push vs zoom, dolly zoom, realization, pull-back, static, motivation, follow/lead, handheld, orbit/crane/drone, axis); 6.1 frame rate, shutter, in-story rates, AI speed.
- **§7** Full lens-and-movement table (33 rows: effect, use, risk).
- **§8** Translation table: 16 story meanings → size, angle, lens/focus, movement, pitfall ("menu, not recipe").
- **§9** Camera system: 9.1 template; 9.2 *The Catch*.
- **§10** Impossible situations: 10.1 cage; 10.2 mirror phases, methods, decision table, F conflict; 10.3 ship; 10.4 surveillance; 10.5 tablet; 10.6 other cameras.
- **§11** Priority order; R1–R25.
- **§12** Ex1–Ex6 (*The Catch*), Ex7 (*The Long Places*).
- **§13** Checklist; **§14** 21 common mistakes.
- **§15** AI guides, working/failing terms, rephrasings, example prompt, image models, Blender.
- **§16** Open questions. **Sources** with check dates and caveats.
