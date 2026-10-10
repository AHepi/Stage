# Digest B3: Composition, visual structure and staging

Source: `research/B3_composition_visual_structure_staging.md` (1,055 lines). Brackets: P# = principle (§1), R# = decision rule (§7.2), § = section, Ex# = worked example (§9). R1–R22 are "consider" defaults. R23–R29 are firm.

## 1. Scope

1. **Frame and film:** what goes where in one frame and where the eye lands first; across the film, Bruce Block's visual structure (visual intensity planned to track story intensity).
2. **Scene:** staging and blocking (marks, moves, distances, who moves and why), geography and screen direction, a text floor plan (readable and JSON), and a tested Blender script that turns the plan into a grey blocking scene.
3. **Order:** runs after beats and turning points (A-series), alongside B1 (camera) and B2 (light). It designs *The Catch*'s glass-and-mirror system and gives three worked floor plans.

**Terms** (§0.1). *Frame-left/right*: as the audience sees it. *Visual components* (Block): space, line, shape, tone, colour, movement, rhythm. *Contrast / affinity*: difference / similarity within a component; contrast raises visual intensity and affinity lowers it. *Space types*: **deep** (many depth cues), **flat** (cues suppressed), **limited** (flat frontal planes stacked in depth), **ambiguous** (size, spatial relations or camera position unreadable). *Surface division*: a line (glass edge, door edge) that splits the frame. *Point of attention*: where the audience looks now. *Dominant*: the element seen first. *Eye-trace*: the path of attention across a cut. *Lead room*: space in front of a face or a moving body. *Short-siding*: the character faces the near edge, empty space behind them. *Planimetric*: camera square to a back wall, people strung across it. *Closed form*: everything important is inside the frame; *open form*: edges cut people and the world continues. *Staging*: the strategy for placing bodies relative to camera; *blocking*: exact marks and moves per beat. *Line of action*: the line through the two people (or person and thing) at the centre of a moment. *Anchor*: a fixed recognizable object that keeps geography clear. *Dirty single*: includes a soft edge of the other person. *Start frame*: first-frame still for a video model (C2: keyframe). *Wild wall*: a removable wall (all walls in Blender/AI). *Stations*: 2–4 marks a long scene moves through, each tied to one of its movements. *Glass state*: how visible a transparent surface is (§8.1). *Mirror state*: NORMAL / MIRRORED (C2 §7.3; phases in B1 §10.2). *Mirror twin*: a person's position reflected through the glass plane.

## 2. Rules

**Using the translation table** [§7.1] (it closes this section): at most one composition choice and one staging choice per moment. Prefer staging, because it comes from what the characters want. Tie the choice to a script object, line or action, never to a mood word.

**Principles and structure**
1. [P1] If the frame's ranking of importance does not match the beat (who wants, who wins), then reframe, because the frame is an argument about importance.
2. [P2, R2] If a scene's value is closeness or distance, then write the distance in metres at every beat and change it only when the value changes, because drift reads as meaning the scene does not intend.
3. [P3, §4.7] If a person moves, then write the desire (the move's "why") or cut the move, because a move without desire is noise. If a scene runs more than a few beats, then give it 2–4 **stations**; the route carries meaning (toward the door = escape, the window = longing, the other person = appeal, an object = the stake).
4. [P4, P5] If planning intensity, then plan across the whole film and hold most components constant, because maximum contrast everywhere leaves nowhere to go, and the one component that changes is loud.
5. [P6, P7] Unless the story wants the audience lost, then keep people and exits mappable, and decide per beat when each barrier is visible, because accidental disorientation kills tension and barriers carry separation without words.
6. [P8, R9, R20, R27] If a place, configuration, gesture or image returns, then repeat the earlier framing exactly (position, lens, marks) and change one thing. Never add an occurrence the script lacks, because the one change is the meaning and extra emphasis is cliché.
7. [P9] If you break a rule (short-siding, crossing the line, dead centre), then break it once, on purpose, and record the reason, because a break registers only against kept rules.
8. [P10, R19] If the source is prose, then turn each spatial phrase into a named mark in metres, keep the phrase as the reason, and reuse the number whenever the phrase returns, because a named mark becomes a repeatable motif.
9. [§2.2, §2.5] If planning a component (space, line, shape, movement, rhythm), then score contrast at three levels (in the shot, shot to shot, sequence to sequence) and choose per stretch: **hold**, **progress** or **contrast**, because a film needs both contrast and affinity. The default is **parallel** (visual intensity climbs to the climax); **counterpoint** (visual calm under a story peak) is a justified pipeline choice, not Block's rule.
10. [R7, R25] If at a story peak, then raise contrast in **≤2 components** and hold the rest. Firm, per frame: if one expressive device is working (barrier, reflection, frame within frame, short-siding, tilted horizon), then keep all else neutral, because stacked devices read as the film pointing at itself (unless the script stacks them, as in sc17).
11. [R8] If a scene follows a high-contrast sequence, then consider strong affinity (flat space, stillness, horizontals), because contrast needs a quiet side.
12. [§2.3] If a space must stay ambiguous for more than a few seconds, then remove known-size objects and hold the camera still, because movement and known sizes are depth cues. One known-size object ends it on purpose.
13. [§2.4] If ranking line and shape, then diagonal > vertical > horizontal, and circle vs triangle is the strongest shape contrast (meaning is taught by the film). If the dominant is a still object, then keep everything else still, because movement beats brightness for attention.

**Single frame**
14. [§3.1] If framing any shot, then name the dominant, with **≥3** attention cues agreeing and none of the four strongest (movement, brightest area, sharpest focus, a face) pointing elsewhere, because conflicting cues confuse. For split attention, give each target exactly one strong cue.
15. [§3.2–3.4, R12] If there is no story reason, then use thirds as the baseline and asymmetrical balance. Reserve centre and symmetry for ritual, confrontation, control, mirroring or entrapment, and imbalance for waiting for or dreading someone off-frame, because used everywhere they stop meaning anything.
16. [§3.5] If framing a single (medium to close-up), then eyes go on or just above the **upper third line**; the face sits on the third line opposite the look (**~2/3 width** of lead room); the listener looks just past the lens on the other person's side (into lens is reserved); eyeline heights match the bodies; faces are cheated **20–30°** toward camera except in reserved true profiles (true facing in the plan, cheat in the shot line), because this keeps singles matched. Excess headroom reads as defeat.
17. [§3.5, R10] If a character hides something, then short-side them or crop a hand or half the face (one character at a time), and give them their first open, centred frame when the truth comes out, because the composition then pays off the secret.
18. [§3.6–3.9, R13] If adding negative space, a frame within a frame, leading lines or foreground objects, then: negative space must be motivated (an empty chair) and its side chosen; **one** frame within a frame per shot (two only if the script names both), its meaning stated (observation, containment, exclusion); lines land on the dominant; each foreground object frames, blocks or comments, or is removed, because decoration competes with the dominant.
19. [§3.10] If a scene is about being trapped, controlled or observed, then default to closed form; if about escape, chaos or a larger world, then open form; switch on the turn where control changes.
20. [R14, §3.11] If a shot is under **2 s**, then place its dominant where the previous shot's was, because the eye has no time to search. Jump only for a deliberate jolt.

**Staging**
21. [§4.1] If tempted by static singles, then prefer one staged wide (a walk-and-talk, or a short "oner": in AI, one move turning a wide into a two-shot), because singles are cheap but carry no relationship. For long takes and AI clips, steer attention by **blocking and revealing** (small moves that hide, then uncover, a key figure) instead of cutting.
22. [§4.2] If writing distances, then use Hall's zones: **intimate ≤45 cm, personal 45 cm–1.2 m, social 1.2–3.6 m, public >3.6 m** (the story's own distances override), because social→personal is an event and intimate is a claim. Power cues, clearest first: who moves or holds still; who closes the gap; body height; territory; facing; interposition; objects handed over.
23. [R1, §4.9] If a scene has a turning point, then change the configuration **on** that beat (stand, sit, turn, step in/between/aside, cross a threshold, touch, let go) and reset coverage, because bodies are read before words. Identical blocking before and after means no turn or a missed one; stillness counts only after movement.
24. [R3, R4] If one character holds the power, then keep them still while the other moves; if someone steps between two others, then play it in one wide showing all three, because stillness reads as control and interposition needs both people it separates.
25. [R5, §4.4] If there are three people, then the one physically between is the **pivot**; write the **engaged pair** and **silent third** per beat; when the pair changes, show the pivot's head turn in a held wide or re-establish all three before new singles; keep the silent third visible when their reaction matters, because clean singles lose the third person.
26. [R6] If a scene is mostly talk, then give it one shared "third thing" (screen, document, window) and stage laterally toward it, because the turn becomes a turn away from it.
27. [§4.3, §4.5] If two people, then use Arijon's triangle (all cameras one side of the line). Face to face = negotiation (social) or love/threat (intimate); side by side = alliance or avoidance (only a mirror gives eye contact); one behind the other = watching or protecting; L-shape = withdrawal; a barrier = choose the camera's side per beat. If four or more, then subgroups, one dominant subgroup per beat, ranked by depth; a crossing between subgroups is a beat.
28. [R17, R18, §4.6] If someone enters, then choose a frame edge (arrives from somewhere) or a background door (arrives into this place; the door gains power). Appearing without entering is reserved for the uncanny. An exit clearing frame ends presence; an open door leaves the question open; passing between two people separates them.

**Geography and AI**
29. [R15, §5.1] If a location is new, then give a master or establishing view, a named anchor and the exits before the first important move, because a move means nothing without a map (a piecemeal introduction must add up before that move).
30. [R16, §5.2] If you must cross the line, then do it inside a shot (camera move or a character move that redraws it), via an on-axis shot, insert or cutaway, or on a beat that reverses the relationship, because unmotivated crossing reads as confusion. Same-subject cuts need ~**30°** or a clear size change. Exit frame-right means enter frame-left; show direction changes inside a shot; re-establish after marks change; people approaching each other move in opposite screen directions.
31. [§5.3] If using direction as meaning, then keep the film's own directions consistent, because "left-to-right = forward" is weak; vertical (up = effort or hope, down = danger) travels better, but the story decides.
32. [R22, §5.4] If a location is mirrored in one phase, then write directions and plans for the **final picture** and derive phase B from phase A by **x → room width − x, θ → 180° − θ**, never by hand-editing, because a later flip would silently reverse the plan.
33. [R21] If a shot is AI-generated, then use **one move per clip** and fix the start composition with a start frame (a generated still or Blender render), because models handle one action far better than choreography.

**Restraint (firm)**
34. [R23] If a shot's reason names only a mood, then rewrite it to name this script's object, line or action, because mood-only reasons produce stock images.
35. [R24] If a symbol is not in the source (rain on glass, wilting plant, ticking clock, caged bird, blind shadows), then do not add it, because the source's recurring objects already carry the meaning.
36. [R26] If a composition would fit any film (the **any-film test**), then add the detail only this script has, or simplify to plain coverage.

**Glass physics (firm)**
37. [R28] If A's reflection must lie over B beyond the pane, then place A's mirror twin (as far behind the glass as A is in front), draw twin–B, extend it to A's side and put the camera there; light A and darken B's side, because reflections sit at the twin and glass reflects only a few per cent. A and B directly opposite at equal distances works from any camera on A's side; twin and B side by side at the same depth works from none, so move one.
38. [R29] If the glass must be CLEAR, then keep the camera side darker than the far side (black cloth; prompt "no reflections on the glass"), because reflections come from camera-side light. A polarizer works only near **56°** off square.
39. [§8.1] If planning any glass shot, then use: ~**4% per surface** square on, <10% to 60°, ~25% at 75°, total at grazing. A square-on THROUGH shot reflects the camera (cheat a few degrees). ALONG mirrors both people (a faint double on the dividing line is fine, never over a face). A small convex surface shows a shrunken, bent view just behind it: focus on the container, and the reflected thing must be close.

**Translation table** [§7.1] (meaning: composition / staging). Control: centre, symmetry, planimetric, closed / lateral, fixed marks, no one crosses centre. System about to break: symmetry with one element wrong / one still while others move. Isolation: negative space, excess headroom / >3.6 m from all, back turned. Unseen threat: short-siding, empty side behind / facing a wall, threat enters behind. Watched: frame within frame, camera outside barrier / watched lit in a box, watcher in a darker space. United: shared lead room, one plane / side by side, closing to personal. Divided: surface division, clean singles / barrier or third body, distances held. Power held: height, centrality, tone / holds still, holds the doorway, stands. Power shifting: weight tilts / the weaker one stands, steps in, takes the object. Protection: one body before another in depth / interposition. Secrets: partial framing / turned away, hands hidden, behind the deceived. Revelation: blocking and revealing / step aside, door opens, turn to camera. Longing: leading line to a small far figure / a gap that does not close. Reconciliation: symmetry returns / gap closed by **both**. Unreal: ambiguous space, reflections, no anchor / disconnected entrances, appearing without entering. World turned over: a frame repeated with one element reversed / earlier marks reversed or swapped. Grief: flat, horizontal, still / sitting or lying, the empty mark.

## 3. Breakdown fields

| Level | Field | Meaning | Values / example |
|---|---|---|---|
| film | visual_structure_plan | Per-sequence table | columns: sequence, story_intensity, space_type, line_and_shape, movement_and_rhythm |
| film | reserved_choices | Used only in named slots | "perfect symmetry: two reflection two-shots" |
| film | camera_side_default | Side of recurring barriers | "Iona's side of the glass" |
| sequence | space_type | Block's type | deep / flat / limited / ambiguous |
| sequence | component_behaviour | Per component | hold / progress / contrast + one sentence |
| scene | story_intensity | Whole-film score | 1–10 (§2.6 list); exactly one 10 |
| scene | counterpoint | Visual calm under a peak | bool + reason |
| scene | floor_plan | Readable + JSON plan | §4 P3 |
| scene | stations | 2–4 marks | "drawer, Nell's room, tank" |
| scene | lines_of_action | Per movement: pair + camera side | "IONA–ELI; south side" |
| scene | pov_character | Dominant in master and turn shot | IONA |
| scene | pivot | Person between two others | JUDE (sc13) |
| scene | barriers | Barrier, visibility, camera side | "partition CLEAR; family side" |
| scene | rhyme_with | Earlier configuration + one change | "sc13 master, observer now in frame" |
| scene | staging_additions | Moves the script does not write | "sc23 step to glass" |
| beat | engaged_pair / silent_third | 3+ people | IONA–ELI / JUDE |
| beat | configuration_change | Physical change on the turn | stand / step between / step aside |
| beat | distance_m, hall_zone | Key-pair distance | 1.8, social |
| beat | move | who, to, via, start_s, dur_s, faces, why | §6.3 |
| shot | dominant, attention_cues | First-look element, ≥3 cues | "Eli: focus, centre line" |
| shot | placement | thirds / centre / edge (+reason) | centre (reserved) |
| shot | balance | symmetrical / asymmetrical / imbalance | — |
| shot | headroom, lead_room, eyeline, cheat_deg, short_sided | Single slots | eyes upper third; 2/3; 20–30° |
| shot | negative_space_side | Side + motivation | "left, empty chair" |
| shot | frame_within_frame | ≤1 + meaning | doorway / observation |
| shot | layers | FG / MG / BG, each justified | "FG Jude soft, MG Iona" |
| shot | form | open / closed | closed |
| shot | glass_state | Every transparent surface in frame | CLEAR / MARKED / REFLECTING / SCREEN / BROKEN-OPEN |
| shot | camera_to_glass | Relation to pane | THROUGH / ALONG / ANGLED |
| shot | mirror_state | Asset orientation | NORMAL / MIRRORED |
| shot | screen_direction | In final (flipped) picture | "exits frame-right" |
| shot | eye_trace | From previous shot | smooth / jump(reason) |
| shot | anchor_visible | Named anchor | MONITOR |
| shot | reserved_slot | Which reserved composition | reflection_two_shot |
| shot | expressive_device | ≤1 | reflection |
| shot | story_reason | Names a script object, line or action | "the needle climbing" |
| location | anchor, exits, wild_walls | Orientation fixtures | "RACK; WEST HATCH" |
| location | phase_orientation, derived_from | Final-picture orientation; derived phase-B plan | "phase B, from phase-A plan" |
| character | eye_height_m, start_mark, faces | Plan entries | IONA 1.60, [2.8, 2.55], SAYE |
| prop | id, centre, size, z, story_meaning | Fixed objects | MINT [2.8, 0.1], z 1.0 |
| motif | ladder_step, crossing_insert, named_mark | Repeated gesture framing | hand-on-glass step 4; GOOD_DISTANCE 2.4 m |
| generation job | one_move, start_frame, structure_image, flip_layout_guide | Clip constraints | depth/layout from grey render (pose needs posed figures) |
| previs job | plan_json, cameras (id, pos, look_at, lens_mm, use), still_frames, facing_deg | Blender inputs | facing_deg = (θ + 90) mod 360 |

## 4. Procedures

**P1. Order of work** [§0]
1. Once per film: the visual structure plan (P2).
2. Once per location: a floor plan (P3) with fixed objects, anchor and entrances, in final-picture orientation.
3. Per scene: blocking beat by beat (start marks, moves, the change on the turn); line of action for each part and the camera's side.
4. Per shot: fill the composition slots (dominant, placement, balance, headroom, lead room and eyeline, layers, frames within frame, glass state incl. visor), each non-default with a one-line reason naming a script object, line or action.
5. Run the checklists, then prompts (§6) or Blender (P4; C4 per shot).
User prompt: "Using file B3, write the floor plan, the blocking by beat, and a composition line for each shot. Mark every choice with the story reason." Then check by eye that each reason names something that happens in the scene.

**P2. Visual structure plan** [§2.6]
1. Score each scene 1–10 for story intensity across the film (not from A2's beat scores). First true row wins: **10** climax, main value turns for good (exactly one); **8–9** life at stake on screen, or a reversal/revelation that changes the plan (9 only for the one or two biggest); **6–7** turning point changing a relationship or the plan; **4–5** minor value turns, a test, needed information; **2–3** set-up, travel, aftermath, rest; **1** nothing at stake (rare; usually cut).
2. Mark peaks and the quietest point; one highest. If two look like 10, the earlier gets 9.
3. For space, line, shape, movement, rhythm: one sentence each for quiet stretches, peaks and end, with hold / progress / contrast per stretch.
4. Name counterpoint scenes and why.
5. Name reserved choices.
6. Write a per-scene lookup table.

**P3. Readable floor plan** [§6.1] (exact template)
```
FLOOR PLAN: <scene id and slugline>
Units: metres. Origin: <named corner>. +x = <compass direction>, +y = <direction>.
Room: <width> x <depth>, ceiling <height>. Wild walls: <which>.
Fixed objects: <id> at <x,y>, size <w x d x h>, <what it means in the story>
Anchor: <id>, seen in <which shots>
Exits: <door id>, <where it leads>
Start marks: <PERSON> at <x,y>, facing <person/object>, <standing/seated/lying>
Moves (one line each):
  <beat id> <PERSON> from <mark> to <x,y> via <x,y>, ends facing <target>. Why: <desire>
Lines of action: <beats>: <A>-<B>; camera stays on the <side> side
Cameras: <id> at <x,y,height> looking at <x,y,height>, <lens mm>, use: <shot purpose>
Distances at key beats: <A>-<B> <metres> (<Hall zone>)
```
Optional ASCII sketch [§6.2]: 0.5 m cells, north up, legend; eyes only (JSON coordinates are authoritative).

**Machine plan JSON** [§6.3]: `scene`, `units`, `origin`, `axes` ("+x east, +y north, +z up"), `fps`, `resolution` ([1920, 804]), `room` {`size` [w, d], `height`, `wild_walls`}, `fixed` [{`id`, `centre` [x, y], `size` [w, d, h], `z` optional base height}], `people` [{`id`, `eye`, `at`, `faces`} or {`id`, `lying_on`, `at`, `head_toward`}], `moves` [{`beat`, `who`, `start_s`, `dur_s`, `via` optional, `to`, `faces`, `why`}], `cameras` [{`id`, `pos` [x, y, z], `look_at` [x, y, z], `lens_mm`, `use`}]. Rules: metres from a named corner; every person has a start mark and a facing target (name or point, never "left/right"); every move has beat, start, duration, reason; moves in time order (facing uses the target's latest position); every camera on the correct side of the line for its beats.

**P4. Blender grey blocking** [§6.4]
1. `blender --python plan_to_blender.py -- <plan>.json` (or `python ...` with pip `bpy`; tested on bpy 5.0.1). Builds floor, boxes, grey cylinders with a cone "nose" (lying bodies horizontal), keyframed moves, TRACK_TO cameras (36 mm sensor).
2. Append `render_stills.py`: Workbench, one still per camera at 1 s and at each move's end, to `./stills/`.
3. Use stills as C2 depth/layout guides or a video model's clay reference (C1); not for pose control.
4. This is the master plan per location and scene; derive one C4 plan per shot, converting **facing_deg = (θ° + 90) mod 360** (θ = atan2(dy, dx); C4's 0 faces −y).
5. Limits: no camera animation, walls, stairs or poses; turning in place needs a move to the same point; a turn across due west may spin the long way (fix ±360°).
6. Mirrored phases: the render is already final-picture; flip it only as the layout guide for a plate C2 generates un-flipped (C2 R5, W3).

**P5. Reflection check** [R28]: twin → line to B → camera on the extension → lighting check; if the line parallels the glass, move a person and log it.

**P6. Three-person coverage** [§4.4]: write the scene as a sequence of pairs, then apply Rule 25.

**P7. Prose to marks** [Ex5]: quote the phrase → metres → named mark → Hall zone → reuse number and camera on every return.

## 5. Checklists

**Per shot** [§10.1] (a "no" needs a fix or a written reason): (1) dominant named, ≥3 cues agree; (2) placement chosen, reason if not thirds; (3) balance fits (symmetry only in reserved slots, imbalance only for waiting/dread); (4) headroom, lead room, planned short-siding, eyeline side and height; (5) every foreground object frames, blocks or comments; (6) space type matches the plan; (7) lines follow the plan (diagonals for peaks); (8) frame-within-frame meaning stated; (9) *The Catch*: glass state and camera-to-glass for every transparent surface incl. visor and tent, physically possible (Rules 37–38); (10) mirror state checked, hands as "nearest the camera", text as insert graphics (C2); (11) screen direction consistent in the final flipped picture; (12) eye-trace smooth or jump intended; (13) anchor visible or geography clear; (14) reserved compositions only in their slots; (15) frame tells the beat with sound off; (16) reason names a script object/line/action, passes the any-film test, every symbol in the source; (17) at most one expressive device.

**Per scene** [§10.2]: (1) floor plan with fixed objects, anchor, exits, start marks with facing targets; (2) every move has beat id and why; (3) configuration changes on each turn, not before or after; (4) key distances in metres with Hall zone, changing only with value; (5) stillness and movement match power; (6) line of action per movement, side chosen, crossings motivated; (7) master or anchor before the first important move; (8) entrances and exits chosen (edge or door), appearing-without-entering only for the uncanny; (9) pivot named (3+); (10) barriers listed with visibility and camera side; (11) rhyme: what one thing changes; (12) POV character named and dominant in master and turn shot, or a reason; (13) AI: one major move per clip; (14) prose: every mark from a quoted phrase, none contradicting the text; screenplay: every unwritten move logged as a staging addition; (15) could one wide replace several singles; (16) direction kept across cuts, re-establish after mark changes; (17) three-hander: engaged pair per beat, silent third visible when it matters.

**Common mistakes** [§11] (spot → fix): no system → plan and reserved choices first; dominant on the beat's loser → re-rank or state the irony; stand-and-deliver (zero moves, >half singles) → stage the turn as a move in a wide; lost geography (consecutive singles looking the same way) → master, anchor, one side; cliché stacked on several channels (hand on glass + push-in + swelling score; rain for sadness; mirror-staring; blind shadows; tilt for madness) → one channel, usually staging; glass MARKED in every shot → keep it mostly CLEAR; shallow focus everywhere → deepen where the background carries story; mirror errors ("left/right" hands, readable text in the wrong phase) → "nearest the camera", B1 phases, C2 flips; impossible glass → Rules 37–38; forgotten visor → add its glass state, light from inside the helmet.

## 6. Saying it to AI models [§12]

File's judgment as of 2026-09-27, not benchmarks.

**Usually understood:** shot sizes, over-the-shoulder, two-shot; "centered/symmetrical composition" for one subject; "seen through a window", "framed by a doorway"; one foreground plus one background element; "in profile"; "silhouette"; "reflection in the glass" (appears, often physically wrong).

**Often ignored or misread:** "rule of thirds"; jargon (lead room, headroom, short-sided, planimetric, limited space, contrast and affinity, 180-degree rule, screen direction); "frame-left" (read as the character's left); distances in metres; which hand is raised; two people "looking at each other"; more than three people in set positions; the same geography across separate clips.

**Plainer phrasings (quoted):**
- Short-sided: "Close-up of a woman near the right edge of the image, in profile facing right, her face close to the edge; a large empty area of bare wall fills the left two-thirds of the image behind her."
- Lead room: "She is on the left side of the image, facing right, with open space in front of her face."
- sc10 reflection two-shot: "Wide 2.39:1 frame, long lens from far away, depth flattened. Two women in exact profile face each other across a kitchen table, one on the left side of the image facing right, one on the right side facing left, the same distance from the centre. Each raises the hand nearest the camera, palm out, at the same height. A man lies on the table between them. Far in the background, exactly in the centre, a thin bearded man stands by a fridge. Symmetrical composition." (Composition only; mirror state and rings via C2 flip-and-composite; check hands by eye.)
- Interposition: "She stands directly between the doctor on the left of the image and the man on the right, facing the doctor, blocking the doctor's view of him."
- Depth: "In the foreground, the doctor's shoulder; in the middle distance, the woman; in the far background, small and sharp, the man at the fridge."
- Social distance: "About two body-lengths apart" / "the table between them".
- REFLECTING: "Seen at an angle through a glass wall. She stands brightly lit on this side; the room behind the glass is dim. Her faint reflection lies over his face on the glass." (State the lighting; models will not do the physics.)
- CLEAR: "Seen through perfectly clear glass with no reflections; the room on the camera's side is dark."
- Visor: "Close-up of a woman in a white pressure-suit helmet; her face clearly visible through the clear visor, lit softly from inside the helmet; no reflections over her eyes."
- Cheat: "Her face turned three-quarters toward the camera while her eyes look off to the right of the image, at the man she is talking to."

**Methods that beat words:** Blender grey render as structure image or start frame/clay reference; one major move per clip (split at the moves); generate or composite each person separately when position, facing or hands must be exact (C2); positions as parts of the image (left third, right edge, exact centre, lower half); check each output against the per-shot checklist (hands, facing, mirror state).

## 7. The Catch

Scene numbers: 25 Sept 2026 workshop revision, sc1–sc30.

**Visual structure plan** [§2.7] (intensity; space; line/shape; movement):
- **sc1–5 break-in**: 3→7; deep; shaft verticals, first diagonals on violence; lateral truck along the windows.
- **sc6 fall**: 9; deepest (down the shaft); diagonals; bodies move, camera calm.
- **sc7–10 wrong world**: 5→6; limited/flat; horizontals; affinity so only the reversed world contrasts.
- **sc11–13 quarantine**: 4→7; limited, planimetric; glass edge as surface division; stillness, tightening to "You.".
- **sc14–17 figure**: 8→5; ambiguous; a tall black vertical; arrivals without movement.
- **sc18–22 ship**: 5→6; sc18 flat, then ambiguous with one limited room; curves vs rectangles; the chamber's length is the only deep axis.
- **sc23–25 sacrifice**: 8→9; limited to deep; shapes give way to the circle; the figure moves fast once.
- **sc26–27 ledge/crossing**: **10**; extreme ambiguity; **counterpoint** (still camera, slow drift).
- **sc28–30 return**: 6→2; flat, symmetry, circles in rectangles; the last moves are chairs closing (sc29) and a folded cloth under the vessel (sc30).

**Reserved:** straight down the shaft (sc6 and its footage); full ambiguity (ship, crossing); perfect symmetry (two reflection two-shots); circles as dominant (sc10 ring inserts, sc25 on).

**Geography** [§5.4]: vertical is the main axis (up = survival). Rescue direction frame-left → right in sc3 and sc20. In phase B, Eli's room is at the corridor's other end, correctly (the corridor, Eli's room and the maintenance passage appear in both phases). **Anchors:** red cage-gate tag; bright sill; table with Jude; monitor to the glass (sc13); needle box over beds; six-socket rack; glass-fronted cabinet; yellow line; RECEIVING (sc28).

**Glass system** [§8.1]: CLEAR (connection wins), MARKED (barrier matters this beat), REFLECTING (doubling, identity), SCREEN (truth second-hand), BROKEN/OPEN (breached). THROUGH (audience on that side), ALONG (equal weight), ANGLED 30–60° (usual for REFLECTING). **Camera on Iona's side by default**; crosses only for the sc13 master and once in sc23. ALONG reserved for the two reflection two-shots plus an imperfect sc28 version. **Visor (sc18–28):** CLEAR, lit from inside, for readable close-ups; REFLECTING only when the world presses; its SCREEN display (C2) never covers her eyes on a decision beat. Hoods sc18/sc28 CLEAR. **Tent (sc29–30):** against the partition so one barrier reads. Bed shell closing: THROUGH, never ALONG. Named in script: sc3 crack BROKEN; sc21 figure in the curved container REFLECTING/ANGLED (suit-camera frame, figure close); sc12 monitor SCREEN through CLEAR.

**Mirror geometry** [§8.2]: facing frame-right shows the right side. Reflection two-shot: ALONG, level, 85 mm from well back, profiles equidistant from centre. **sc10:** Iona frame-left facing right, Saye frame-right facing left, each raising the hand nearest camera; rings in a separate insert. **sc29:** reversed; Iona frame-right, Jude frame-left, ringed hands nearest camera. Only literal mirror: sc9 rear-view.

**Hands-on-glass ladder** [§8.3], one insert (THROUGH, square, hand ~1/3 frame height, 50 mm, no push-in, no score swell): sc3 strapped hand falls; sc11 two hands, two panes; sc12 first palm, by the F; sc17 toward the monitor; sc25 the animal's limb; sc26 animal touches the picture (match sc17); sc29 two hands meet. Add none. **Crossings** [§8.4]: only objects cross (hatch, meal, radio drawer, courier pod); sc29's half roll stops short, framed like the sc20 radio. The sc25 taping is framed like the sc3 crack.

**Scenes:**
- **sc9 car**: if the country drives on the left, mirrored car puts Iona frame-right, Eli frame-left; her gearstick reach hits the door; Eli leans between the seats so the mirror can hold his eyes (key shot, held through the flask look).
- **sc13** [§8.6, Ex2]: Jude pivot in bed, row facing the monitor (anchor). M: master from Saye's side, 50 mm, CLEAR. R: reverse, 35 mm. S1/S2: 85 mm dirty singles from the bed-head side. The flinch returns to the master; Jude's remote insert repeats Iona's.
- **sc20/23** [§8.7]: chamber 14 × 4 m, ceiling 3.2; rooms Jude, Eli, Nell west to east; rack anchor. Iona takes Saye's sc13 position (camera O, 50 mm, observer in frame). sc23: Iona 1.2 m from the figure; the turn is Eli joining Nell while the glass stays shut.
- **sc10** [Ex1]: camera A 85 mm from ~6.3 m, 1.45 m high; Jude, lamp, Eli on the centre line; Iona sets the lamp down before B4; bottle cap in the same frame, focus to Eli; B9 resets to camera F; B10 interposition in the wide; B11 she steps aside.
- **sc23** [Ex3]: the planned reflection on Eli is **impossible** from her mark (twin (11.0, 5.2), Eli (9.0, 5.3)). (a) She steps opposite him to about (9.0, 2.7), an added move; or (b) play THROUGH, CLEAR.
- **sc28/29** [Ex4]: 35 mm lateral wide, slightly high, 3 m apart; Saye's raised hand on the centre line where the glass edge sat. sc29: ALONG but wider; chairs from ~1.5 m to the glass, both moving.
- ***The Long Places*** [Ex5]: GOOD_DISTANCE = 2.4 m; one low (~0.8 m) static camera; five dissolved shots; only the girl's mark changes (2.4, 1.8, 1.2, 0.6 m, touching); the lamp flame is the clock.

**For the writer/user:** the car's driving side (sc9 flips otherwise); inferences (Eli front seat sc9, Jude in bed sc13, room order); sc23 option (a) or (b); sc10 bottle-cap version (this file's, or A2's B5.a with Saye foreground): choose one per breakdown.

## 8. Conflicts and open questions

- **Intensity scales:** scenes 1–10 here vs A2's beats 1–5; do not convert.
- **Counterpoint** unconfirmed as Block's; Block is paraphrased from summaries (check pages before quoting).
- **C4 facing convention** differs; use the conversion formula.
- **sc10 camera A** moved from 50 mm at 4 m to 85 mm at 6.3 m to match B1's sc29 lens. *Digester's note:* the B1 digest puts 85 mm "from the confession on"; check that it covers sc10.
- **sc10 staging** differs from A2's B5.a.
- **§8.2 depends on B1's phases**; redo if they change.
- **Hall's zones** are North American; the story's own "good distance" overrides.
- **Glass figures** are for plain clear glass; coated visors and plastic differ.
- **Unverified:** Arijon's variation names; *Paris, Texas* shots; the Spielberg Oner essay.
- **Blender script** tested on the sc10, sc13 and sc20/23 plans; it has no camera animation or poses (C4 has).
- **AI phrasing claims** (§12) are the file's judgment, not tested benchmarks.
- **Resolved here:** A2's sc10 lamp continuity flag (Iona sets the lamp on the table before B4).

## 9. Section map

- **§0 How to use**: order of work for an LLM; the user prompt. **§0.1** glossary (~60 terms).
- **§1 Core principles**: P1–P10.
- **§2 Block's visual structure**: §2.1 seven components; §2.2 contrast/affinity at three levels; §2.3 four space types, depth cues, holding ambiguity, surface divisions; §2.4 line, shape, tone, movement, rhythm; §2.5 story and visual graphs, progression, counterpoint, Lumet's *12 Angry Men*; §2.6 plan procedure with 1–10 scoring; §2.7 *The Catch* plan table and reserved choices.
- **§3 Single frame**: §3.1 attention cues, dominant rule, blocking and revealing; §3.2 thirds; §3.3 centre/symmetry (Kubrick, Anderson); §3.4 balance; §3.5 headroom, lead room, eyeline, cheating, short-siding; §3.6 negative space; §3.7 frame within frame; §3.8 leading lines; §3.9 layers (Toland); §3.10 open/closed form with prompt words; §3.11 eye-trace (Murch, *Fury Road*).
- **§4 Staging and blocking**: §4.1 depth vs lateral, intensified continuity, walk-and-talk, oner; §4.2 Hall's zones and power cues; §4.3 two people (Arijon, arrangement table); §4.4 three people, pivot, coverage rule; §4.5 four or more; §4.6 entrances and exits; §4.7 stations; §4.8 doors, windows, glass, barriers; §4.9 turning-point blocking test.
- **§5 Geography**: §5.1 establishing the space; §5.2 180° and 30° rules, Ozu, movement-across-cuts rules; §5.3 direction as meaning; §5.4 *The Catch* geography, phase derivation, anchors.
- **§6 Floor plans**: §6.1 readable template; §6.2 ASCII sketch (sc10); §6.3 JSON plan (sc10) and writing rules; §6.4 `plan_to_blender.py`, `render_stills.py`, C4 conversion, limits, mirrored phases.
- **§7**: §7.1 translation table (17 meanings); §7.2 Rules 1–29.
- **§8 *The Catch***: §8.1 glass states, camera positions, optics, visor/hood/tent/shell; §8.2 mirror geometry (sc10, sc29); §8.3 hands-on-glass ladder; §8.4 crossings, crack and repair; §8.5 the car (sc9); §8.6 sc13 floor plan; §8.7 ship rooms (sc20, sc23) floor plan.
- **§9 Worked examples**: Ex1 sc10 kitchen; Ex2 sc13 row and pivot; Ex3 sc23 question through glass (reflection geometry check); Ex4 sc28 hand as barrier, sc29 payoff; Ex5 *The Long Places* "good distance".
- **§10 Checklists**: §10.1 per shot (17); §10.2 per scene (17).
- **§11 Common mistakes**: symptom, test and fix table.
- **§12 AI phrasing**: understood, misread, plainer phrasings, working methods.
- **§13 Limits and open points**.
- **Sources**: books, web pages checked 2026-09-27, films, test stories.
