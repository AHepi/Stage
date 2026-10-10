# Card 22. Previs

Add-on B reads it whole. It runs only in Claude Code on the user's computer, where the AI runs Blender; the user's word is "grey previews" (blueprint 9). "C4 R21" is rule 21 in C4 §8 and "C4 Rec3" its recipe 3 (§10); "D6 Rec4" is recipe 4 in D6 §6.

## The job

**Previs** is a rough grey 3D version of a shot that fixes camera placement, lens, timing and where bodies stand before any video is made (C4 §1). Code compiles one plan per shot at `previs_plan_level_min` or above from the records (`make_previs_plans.py`: set plans, scene starts, floor-plan moves, setups (where each camera stands), shots); the AI writes only what code cannot, renders with `render_previs.py`, fixes every blocking fault, and records the route into video. It hands on PREVIS records (`level`, `standin_level`, `route`, `stills`, `approved`), **grey renders** (untextured renders showing shapes and light direction), plan views (a flat top or side view of the set), and one contact sheet per scene of framing-critical shots for checkpoint D, "the grey previews" (blueprint 9).

## Questions in order

1. **Does the meaning depend on where the camera stands, its lens or how bodies move?** Then previs; a static or simple dialogue shot skips 3D (C4 R1-R2). `previs_level` follows C4's ladder: 0 no 3D (dialogue, object close-ups, simple scenes: most shots); 2 grey 3D, a layout check; 3 a **guide video** a model copies (falls, weightlessness, the creature, complex moves); 4 a performance captured on a phone when a reach or flinch must be exact; 1 (posed stills) and 5 (open models on a rented graphics card) are rarely worth it (C4 §9; K14).
2. **Does the place have a set plan?** A location in three or more shots gets one grey set that every shot there reuses, so the door is always on the same wall (C4 R3, Rec2); in the pipeline it is the LOCATION's set plan (K23). A place seen in both mirror states is stored once, in `plan_orientation`; code derives the other and nobody edits it by hand (B3 §5.4; K02).
3. **Which stand-in?** A **stand-in** is the simple figure that takes a character's place. `standin_level` 1 is boxes, enough for depth and eyelines; 2 a shaped human; 3 a rigged human with a motion; 4 the user's own capture; 5 a hand-posed rig (C4 §4.4). A pose guide needs a human shape; a body that is not human-shaped (the figure) is guided by depth, never pose (C4 R6-R7).
4. **What is not automatic?** Physical motion beyond the free-fall helper, bodies riding a moving cage, doors that swing on a pivot, arm and hand poses, performances and creature shapes go into the shot's extras fragment, `19 Grey previews/extras/<shot>.json`, named in `PREVIS.extras` (blueprint 9).
5. **Does it obey physics?** A fall is keyed (its position set) on every frame from z = z0 − `free_fall_half_g` × t², because eased keys stall and read as floating (C4 R10, §4.2). Bodies inside a moving object are parented to it (attached, so they move with it) or keyed on the same frames, or its floor passes through their legs (C4 R11, R22).
6. **Did it pass the check?** Nothing goes to a video model before `check_blocking.py` prints `BLOCKING OK` (no stand-in through a wall or another stand-in, no camera inside a solid) (C4 R21) and every figure faces within `facing_tolerance_deg` of the derived facing (PREVIS-03).
7. **Is it framing-critical?** Then the user answers at checkpoint D; otherwise it is `approved: auto` once it passes question 6 (blueprint 9).
8. **Which route into video?** One `PREVIS.route` per shot (menus below). Hosted "camera control" takes presets or a reference video, never numbers, so an exact camera path goes in as a video (C4 R24).
9. **Is geometry shared?** One physical event shown in overlapping shots is one **master previs**, and each shot's `time_slice` names its frames of it (K20); a replay on a screen is cut from one master take through the in-story camera, and a match cut shares its geometry (B1 §10.4; C5 R30).

## Translation menus with pitfalls

Pick one route per shot, tied to what the shot must keep exact (C4 §6, R8):

| Route | What the model gets | Use when | Pitfall |
|---|---|---|---|
| 1 | Grey stills restyled into start and end pictures (C4 Rec4) | Composition matters, motion is simple | Weak when the motion itself is the point |
| 2 | The **depth pass** (grey where brightness means distance) as a guide video, plus a style picture (C4 Rec5) | An exact camera path, floating bodies | A depth range wider than the subjects turns actors flat grey (C4 R15, R25); a slower model frame rate needs a retime (C4 R14) |
| 3 | The grey render as a reference video to a hosted model (C4 Rec6) | The camera move matters and nothing can be installed | People swap or merge: split the shot by person (C4 Rec6) |
| 5 | Elements rendered through the stored camera track, composited (C4 R9; D6 Rec4) | Exact text, screens, floating beads | A second flip in the edit (D6 VC8) |

Never lay a guide video over a face whose lips must sync (C4 R13). There is no route 4: camera numbers work only in research models (C4 §6, R19).

## Budgets and saved choices

- `previs_plan_level_min`: plans and blocking checks only at or above it; `facing_tolerance_deg`: the facing check (PREVIS-03).
- `previs_width_px`, with the height from `frame_shape` (K24); `previs_sensor_width_mm`, so lens numbers match B1's full-frame family (C4 §4.1); frames cover screen time plus `handles_s` at each end (blueprint 9).
- `previs_depth_margin_m` around the nearest and farthest subject (C4 R15).
- `previs_seated_height_factor`, `previs_kneeling_height_factor`, `previs_lying_box` for stand-ins not standing; seats and beds go in the clash exclusion list (blueprint 9).
- `free_fall_half_g` (C4 R10).
- Two or three rounds of plain-word changes are normal ("lower the camera to knee height") (C4 Rec3).

## The baseline is a strong answer

Level 0 is right for most shots: C4 puts dialogue, object close-ups and simple scenes there, "most of The Catch" (C4 §9). A start picture from an approved still serves better than a grey render wherever camera and blocking carry no meaning (C4 R2). Depart only when a question above names the reason.

## Cliché traps

Tests: the **plan-view test** (is the camera where its SETUP says?) and the **moment test** (does each still show what its `moment` says?).

- **"It rendered, so it works"** (C4 R21). Fix: `BLOCKING OK`, then the plan view, then the stills.
- **Eased keys on a fall** (C4 R10). Fix: every-frame keys from the formula.
- **Riders keyed apart from the cage** (C4 R22). Fix: parent them, or key them on the cage's frames.
- **A pose guide on boxes or the figure** (C4 R6-R7). Fix: depth.
- **Fixing the prompt when the structure is wrong** (C4 R20). Fix: the plan or the guide's strength.
- **The camera described again in words once a guide video exists** (C3 §9D; blueprint 8.1). Fix: the text carries only the look block (the place's light and colour words), fixed descriptions and sound.
- **A pale, flat depth pass** (C4 R25). Fix: the data view transform ("Raw") and a tight range.
- **Planning around a research camera model** (C4 R19). Fix: wait for a hosted service.

## Reasons that fail and reasons that pass

- Fails: "Level 3 for a more dynamic shot." Passes: "SC06's fall: bodies float inside a falling cage and models add gravity back, so level 3 with a depth guide video (C1 R8; C4 R11)."
- Fails: "Approved: it rendered." Passes: "`BLOCKING OK`; every facing within `facing_tolerance_deg`; the plan view puts camera A where SC10-SU01 says (C4 R21; PREVIS-03)."
- Fails: "Previs every shot, to be safe." Passes: "SC10-SH150 stays at level 0: a static close-up whose meaning is in the face, not the camera (C4 R2)."

## Two worked examples

### The Catch: SC10-SH080, the reflection shot

Level 2 and framing-critical: the scene's image is two women "like a woman and her reflection, each with the wrong hand in the air." (line 428). Code builds the kitchen from its set plan, the west wall wild so camera A (SC10-SU01) can stand outside it, 6.3 metres back on the table's line, 1.45 metres high, with `lens_mm: 85` (K22; B3 Ex1). Iona, Saye and Eli stand on their marks with the facings the records give, Jude a lying box on the table (`previs_lying_box`); the 9-second shot at 24 frames a second renders 252 frames, screen time plus handles (blueprint 9). The render must print `BLOCKING OK` and show both profiles level, the raised hands nearest the camera, the rings out of sight on the far hands (K07; C2 W3). The user sees it on the scene's contact sheet: "Reply with the numbers of any that look wrong, or 'fine'." [fine]. Route 1: its grey stills become the layout pictures for the start and end pictures (the shot's `route: start_end_pictures`), and the mirror route is the plate route: the kitchen and Saye are made in world orientation and flipped, then Iona, Jude and Eli are added unflipped (blueprint 8.5; K03).

### The Long Places: SC05, the threshold at night (lines 73-81)

A contemplative scene needs almost no 3D. The lamp flame leaning out and in with the breath is timing, solved by moments in the prompt; the one exact action, her shoulder taking the warmth "with weight" (line 79), is level 4: the user films the settle on a phone, camera locked off, whole body in frame, plain background, and it is transferred (C4 Rec7; D13 §15.4). At Standard depth no set plan is needed: one person, no glass, and no shot at `previs_plan_level_min` (blueprint 3, step 4).

## Self-check

- Does every shot at `previs_plan_level_min` or above have a plan, `BLOCKING OK` and facings within `facing_tolerance_deg`?
- Is every extra written as a fragment, never by editing a compiled plan or a derived mirror copy?
- Is every fall keyed per frame, and every rider moving with its carrier?
- Does every framing-critical shot have the user's answer, and every PREVIS record a route?
- Is any shot in previs that a start picture would serve as well?

## Words for AI models

Works (route 3): "Follow [Video1] exactly for the camera's path, positions and timing; it is a grey 3D layout, not the appearance", with each stand-in colour mapped to a named reference picture (C4 Rec6). With a guide video, the prompt carries appearance, not camera (C3 §9D). Route 1: prompt the appearance, not the layout, and reject any start picture where someone moved, changed size or lost the eyeline, because the previs is the contract (C4 Rec4).

Fails: numbers for a camera path (C4 R24); "falling" for floating bodies (C3 R13); a guide video over a face whose lips must sync (C4 R13).

## Look up for more

C4 §4, §5.2 (plan fields), §6 (routes), §8 (R1-R26), §9 (ladder), §10 (recipes), §11 (failures), §12 (the SC06 fall, the push, the chest); blueprint 9; K02, K14, K20, K21, K23. Print one rule: `stage.py lib C4 R21`.
