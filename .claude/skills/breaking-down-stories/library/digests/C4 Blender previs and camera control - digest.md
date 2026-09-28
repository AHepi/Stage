# Digest C4: Blender previs, camera control, motion capture, and feeding them to video models

Source: `research/C4_blender_previs_camera_control.md` (854 lines; tool facts checked 2026-09-27 and change monthly). Companion kit `research/C4_previs_kit/`: `previs_from_plan.py` (tested script), `check_blocking.py` (blocking checker), five plans for *The Catch*, sample renders. Brackets: [R#] = the file's decision rule # (§8); [Rec#] = recipe # (§10); [§x] = section. File tags: [V] verified (primary source or run by the author), [U] unverified, [J] author judgment. All focal lengths are full-frame equivalent (36 mm sensor), as in B1.

## 1. Scope

1. How to fix camera position, lens, movement and body positions before any AI video: an LLM writes a JSON plan file, renders it headless in Blender (clay, normal, depth, plan view, per-frame camera data, FBX/USD/.blend) and runs an automatic blocking check.
2. Current previs, posing, motion-capture and connector tools (cost, difficulty, LLM-drivable or not), and five routes from previs into AI video (keyframe images, control video, reference video, camera numbers, compositing).
3. Applied to three hard moments of *The Catch* (cage fall and inversion; push through the opening; the figure's chest opening); runs after the breakdown (A3) and lens plan (B1), before generation (C1-C3).

**Terms** (§1). *Previs*: rough 3D shot fixing camera, lens, timing, positions. *Grey-box set*: plain boxes at real size. *Master set*: the one grey-box set per location that every shot there reuses. *Stand-in*: simple figure replacing a character. *Blocking*: who stands and moves where, when. *Plan file*: JSON floor plan for one shot. *Key*: value stored at one frame; Blender fills between keys. *Keyframe image*: still pinned to a clip's start or end frame. *Camera rig*: camera plus a moving handle and an aim point. *Roll*: rotation around the lens axis. *Parent*: attach an object so it moves with another. *Pass*: one kind of render. *Clay render*: grey untextured render. *Depth pass*: greyscale, near = white. *Normal pass*: colour = surface direction. *Pose pass*: stick-figure skeleton. *Control video*: a pass a video model must keep the structure and motion of. *Reference video*: example a hosted model copies, more loosely. *Control strength*: how strictly the model follows control. *Motion transfer*: copy a body's movement from a video onto a character image. *Restyle*: turn a clay still into a finished image keeping its layout. *Mocap / retarget*: record movement as skeleton data / move it to another skeleton. *Plan view*: orthographic render from above or the side. *Blocking check*: `check_blocking.py`, reports a stand-in passing through the set or another stand-in, or the camera inside a solid. *Headless*: Blender with no window. *bpy*: Blender's Python interface and pip package. *MCP connector*: lets an LLM operate another program.

## 2. Rules

**Whether and how much previs**
1. [R1] If a shot's meaning depends on where the camera is or how it moves, then make previs, because words leave speed, height and lens to chance.
2. [R2, §9] If a shot is static or simple dialogue, then skip 3D (Level 0: keyframe images, text camera directions, image-to-video), because previs costs more than it saves; this covers dialogue, inserts and simple coverage, i.e. most of *The Catch*.
3. [§9] If a shot needs an exact camera move, blocking or geography, then Level 2 (headless clay previs, the minimum viable setup); hard shots (falls, zero gravity, the creature) Level 3 (previs into control/reference models); physical acting or stunts Level 4 (performance capture); Level 5 (ComfyUI open-model control) only when hosted services lack the control.
4. [R3, §4.3] If a location appears in three or more shots, then build one master grey-box set before any shot and reuse it, because the set, not the prompt, remembers where the door is.
5. [R26] If you only want to try "3D layout → AI shot" before installing anything, then try a browser tool such as Intangible for an afternoon, then move to the Blender kit, because the browser tool gives no depth pass or camera numbers to reuse.

**How the LLM operates Blender**
6. [R4, §5.1] If the LLM can run programs, then use headless bpy (Mode B), because every render is repeatable from a stored plan; if not, it writes the script and the user runs it in Blender (Mode A); live MCP control (Mode C) only for adjusting one shot.
7. [R5, §5.4] If using MCP on an open scene, then only on a machine with nothing private, after saving, asking for plan-file edits and re-renders rather than free-form modelling, because both connectors run arbitrary code and plan edits are stored.
8. [R16, §4.8] If an LLM script uses `scene.node_tree`, `BLENDER_EEVEE_NEXT`, `action.fcurves` or other pre-5.0 forms, then say "Blender 5.2" and have it fix them, because 5.0 removed them; run every script once and fix it before trusting it.
9. [§5.3] If the script is extended (imported models, Follow Path, EEVEE pass), then re-run all kit plans and `check_blocking.py`.

**Set, stand-ins, camera**
10. [§4.3] Build sets to real size in metres with one meaningful flat colour per material (brick brown, steel grey, sill white, band yellow), because clay then reads at a glance and image models can be told "the white strip is the bright steel sill"; model a scripted feature wherever the camera can see it (the band "circles the whole shaft": all four walls).
11. [§4.1] Keep sensor width at 36 mm always. Horizontal FOV = 2 × arctan(sensor ÷ (2 × focal)): 18 mm 90.0°, 24 mm 73.7°, 35 mm 54.4°, 50 mm 39.6°, 85 mm 23.9°, 135 mm 15.2°.
12. [§4.1, §11] If the set is tight (2 m cage), then set clip start 0.01–0.05 m (default 0.1 m), because nearer objects vanish.
13. [§4.1] Leave depth of field off in Workbench passes so control videos stay sharp, but record f-stop and focus object, because they go into `camera_track.json`, the breakdown and the prompt.
14. [R6] If the control model follows pose, then use human-shaped stand-ins (MPFB or Mixamo), because pose detectors find no skeleton in boxes; for depth, boxes suffice.
15. [R7, §4.4] If the body is not human-shaped (the figure), then boxes at true height and depth control, never pose, because human pose detectors force human proportions onto it.
16. [§4.2] If the camera rides a moving object, then parent the rig to it ("bolt the camera to the cage"); long even move = Follow Path; handheld = Noise modifier under ~1 cm and 0.5°.
17. [R22] If stand-ins travel inside a moving object, then parent them to it or key them on exactly its frames, because two curves drift apart between keys and the floor passes through their legs.

**Motion**
18. [R10, §4.2] If motion must obey physics (a fall, a dead stop, a swing), then key it from real numbers on every frame (free fall: distance = 4.9 × seconds² m) or use Cascadeur, because Blender's default Bezier easing, even between formula keys 8 frames apart, dropped the test cage from 13.4 to 3.7 m/s before impact and reads as floating.
19. [R11] If the scene is weightless, then hand-key bodies and objects relative to the cage and parent the camera to the cage, because mocap and physics assume gravity.
20. [R12, Rec7] If a performance matters (a reach, a flinch), then act it on a phone and use mocap or motion transfer, because hand-keyed acting is an animator's skill; two people in one take need DeepMotion or QuickMagic (Rokoko Vision takes one performer).
21. [§12 Ex B] If the script asks for cinematic speed ("Slower now."), then ease to the mark rather than use ballistic numbers.

**Passes and checks**
22. [§4.6] Render previs passes in Workbench (no GPU, seconds per pass); EEVEE or Cycles only when the previs frame will be the keyframe image's lighting guide.
23. [R15, R25, §4.6] If you need a depth pass, then set `depth_range_m` to the nearest and farthest things that matter and render with the "Raw" view transform (clay and normal: "Standard"; never AgX/Filmic), because a whole-shaft range or the sRGB display curve turns actors into flat grey.
24. [§4.6] If a control model reads the kit's linear depth as too flat, then ask for inverse-depth mapping or send `clay.mp4` for the service to estimate depth, because estimators (Depth Anything) produce inverse depth.
25. [§4.6] Skip a separate outline pass (models make canny edges from clay); for a pose pass render a level 2–3 stand-in and let the tool extract the skeleton (DWPose).
26. [R21] If `check_blocking.py` prints any CLASH, OVERLAP or CAMERA line, then fix the plan and re-render before any pass goes to a video model, because a body inside a wall in the depth video stays inside it in the AI clip; three of the first four kit plans rendered without errors and still failed.

**Route into video (§6, §7)**
27. [§6] Default to Route 1; combine routes for hard shots.
28. [R8] If the camera move is the point, then prefer Route 3 (Seedance 2.5 or MiniMax H3 with the clay render) or Route 2 (depth) over text, because they take the move from video, not words.
29. [§6] In a control model: depth for camera moves and sets, pose for human bodies, edges for hard architecture; combine where allowed.
30. [§7] Several people: Route 1 for simple moves, Route 2 depth plus reference images for complex ones, plan views for sign-off. Stunts: Cascadeur or mocap of a safe mime, then Route 2 pose + depth or Kling Motion Control. Creature: Route 2 depth plus Route 3 for surface detail, or act it and transfer with a skeleton-free model (Wan-Animate-2, cloud only).
31. [R13] If lip-synced dialogue, then no control video over the face; previs only places the camera (coverage plan: positions, eyelines, the 180° line), then Route 1 to a talking model, because structure control fights mouth movement.
32. [R9, §6 Route 5] If the shot has on-screen words, screens, visor graphics or exact elements (floating blood beads), then render them in Blender as layers from the same camera and composite, because models misspell and cannot mirror text; `camera_track.json` keeps layers aligned.
33. [§7] If the world is mirror-reversed, then generate normally, flip in edit, mark `flip`, and pre-reverse whatever turned with Iona (the three characters, the cage); exact backwards text by Route 5.
34. [R17, §6.1] If ComfyUI would be needed only for depth control, then use fal's hosted Wan VACE depth endpoint (no install, cents per second).
35. [R24, §6 Route 4] If a hosted product offers "camera control", then check whether it takes presets, a directed move, a reference video or numbers, because none found accepts a numeric camera track; exact moves go in as video. Route 4 only to re-film an already generated clip from a new angle.
36. [R19] If a research camera model looks perfect in a paper, then wait until it is hosted or in a maintained ComfyUI node, because research code often lacks weights, licences or support.
37. [R18] If a tool cannot be driven by an LLM (Previs Pro, ShotPro, FrameForge, Spark Story), then use it only if someone on the project enjoys operating it; Cascadeur and Intangible (new MCP servers) are untested exceptions.

**Generation-time fixes**
38. [R14] If a control model runs at 16 fps (Wan family), then render the previs at 16 fps or retime afterwards, because mismatched rates stretch the motion.
39. [R23] If a control clip is under the service minimum (81 frames, fal Wan VACE), then pad by holding the last frame or set `match_input_num_frames`, and trim after, because the service otherwise stretches the motion.
40. [R20] If previs and clip disagree at a key moment, then fix the plan file or control strength, not the prompt wording, because structure comes from the control input.
41. [§11, Rec5] Painted-box look: lower strength (H3 `control_context_scale` below 1.0), richer prompt, more restyled keyframe. Camera move ignored: switch to Route 2 depth, shorten the clip. Structure ignored: retry with `clay.mp4` and `preprocess` on.
42. [Rec6, §11] If people swap or merge in both takes, then split by person (Route 2 depth per body, composite), with distinct stand-in colours mapped to named references, because multi-subject interaction is a named weakness.
43. [§11] Motion transfer breaks at the hands: re-perform with hands clear of the torso. Face drift: several character images.
44. [§11] Glass or water (the vessel): a separate insert kept out of depth control, because transparent depth is ambiguous.
45. [§11] Blood refused: composite the beads and use neutral wording ("small dark red droplets").
46. [Rec4] If a restyled keyframe shows anyone moved, resized or off their eyeline, then reject it, because the previs is the contract.

## 3. Breakdown fields

The first ten rows are the file's own names (Rec3, "Breakdown fields for a previs shot [J]"); rows marked (name mine) hold content the file specifies without naming a field.

| Level | Field | Plain meaning | Allowed values / example |
|---|---|---|---|
| shot | `previs_level` | Rung of the §9 ladder | 0 no 3D; 1 posed stills; 1b browser 3D try-out; 2 headless clay; 3 previs into control; 4 performance; 5 open-model control |
| shot | `plan_file` | Path of the shot's JSON plan | `plan_cage_fall.json` |
| shot | `lens_mm`, `sensor_mm` | Focal length (keyable per frame); sensor width | 24 / 35 / 50; sensor 36 |
| shot | `camera_path` | One sentence: how position, aim, lens change | "parented to cage, low SE corner, level, no roll" |
| beat | `beats` | Frame: event (plan stores `[frame, "what happens", "script line"]`) | `[12, "Cage drops", "The cage falls."]` |
| shot | `passes` | Renders sent onward | clay / depth / normal / pose |
| shot | `route` | Bridge into video (§6) | 1 keyframe → image-to-video; 2 control video; 3 reference video; 4 camera numbers; 5 composite |
| shot | `control_strength` | Strictness of control | 0–1 (H3 `control_context_scale`) |
| shot | `flip` | Flipped in edit (C1 Recipe 8) | yes / no |
| shot | `composite_layers` | Elements rendered in Blender and laid over the clip | screens, text, blood beads, red tag |
| shot | `depth_range_m` (plan) | Near/far metres of depth pass | fall 0.3–4; script default [0.3, 15.0] |
| shot | `fps`, `frames` (plan) | Frame rate; length | 24 (16 for Wan control); ≥81 for fal Wan VACE or pad |
| location | master set (name mine) | Set-only plan every shot copies | `SET_<location>.json` |
| location | plan views (name mine) | Top plan and side elevation filed for sign-off | `plan_view.png`, red cone = camera |
| character | stand-in colour (name mine) | Fixed colour, mapped to a reference image | Iona blue, Eli orange, Jude red, figure near-black |
| character | stand-in level (name mine) | §4.4 ladder | 1 box mannequin; 2 MPFB; 3 Mixamo + motion; 4 own mocap; 5 Rigify or Cascadeur |
| character | `height` (plan) | Stand-in height, m | figure 2.4; Iona 1.68; default 1.75 |
| character | control type (name mine) | Control that fits the body | human: pose or depth; figure: depth only |
| prop / set mark | `rgb` (plan) | Meaningful flat colour | sill white, band yellow |
| previs job | blocking result (name mine) | `check_blocking.py` output | `BLOCKING OK` / `CLASH frame 26: IONA_head passes through wall_S` |
| previs job | outputs | Per-shot folder | `clay.mp4`, `normal.mp4`, `depth.mp4`, PNG stills per pass, `plan_view.png`, `camera_track.json`, `shot.fbx`, `shot.usdc`, `shot.blend` |
| previs job | `camera_track.json` | Per-frame camera | top: `shot`, `fps`, `resolution`, `axes`, `frames`; per frame: `frame`, `position_m`, `rotation_euler_deg`, `matrix_world`, `lens_mm`, `sensor_width_mm`, `hfov_deg` |
| generation job | fal Wan VACE inputs | Depth-route parameters | `first_frame_url`, `last_frame_url`, `match_input_num_frames`, `match_input_frames_per_second`, `preprocess` |
| generation job | padding / retime (name mine) | Held last frames; speed change | pad 40 → 81; play 16 fps output at 24 fps; trim |
| generation job | reference mapping (name mine) | Stand-in colour → image slot | "[Image1] is Iona (the blue figure)" |

## 4. Procedures

**P1. Overall path [§2 J].** (1) LLM writes a plan file from the breakdown. (2) Runs Blender headless. (3) Runs `check_blocking.py`, fixes any clash. (4) User reviews clay stills and plan view, asks for changes. (5) Chosen still is restyled into a keyframe image. (6) Image-to-video with start and end frames, or the depth pass goes to a control model.

**P2. One-time setup (Rec1, ~30 min).** (1) LLM app that runs programs, empty folder. (2) "Create a Python 3.13 virtual environment, install `bpy==5.2.2`, copy `C4_previs_kit/previs_from_plan.py` and `plan_cage_fall.json` here, and run it into `out/cage_fall`." (~1 GB installed; not Intel Macs.) (3) View `plan_view.png` and clay stills; run the checker; success = shaft, cage, three coloured figures, `BLOCKING OK`. (4) Install the Blender app too, to open `shot.blend` (middle-mouse orbit, Numpad 0 camera view).
Commands: `blender -b -P previs_from_plan.py -- plan.json out_dir` or `python previs_from_plan.py plan.json out_dir`; checker `python check_blocking.py out/<shot>/shot.blend` or `blender -b -P check_blocking.py -- out/<shot>/shot.blend`. "EGL Error" lines without a GPU are harmless.

**P3. Master set (Rec2, per location, 20–40 min).** (1) Give the LLM every scene description for the location plus A3's floor-plan notes. (2) Ask for a set-only plan: walls, doors, openings, furniture, fixed marks, metres, one colour per material, list of guesses. (3) Render a top plan and a side elevation; check that everything the script mentions is present and every scripted action possible. (4) Save as `SET_<location>.json`; every shot plan there starts from a copy.

**P4. Previs one shot (Rec3, 15–30 min).** (1) Paste the shot's breakdown entry and master set with this prompt (§5.2, verbatim):
> "Here is shot [ID] from the breakdown and the master set plan for this location. Write a plan file for `previs_from_plan.py` (schema in C4 §5.2). Use real sizes in metres, 24 fps, the lens from the breakdown with a 36 mm sensor, and keys at every story beat named in the shot. Put the beats first, in a `beats` list inside the plan file: frame number, what happens, script line. Then render it, show me the plan view and the stills, and list anything you had to guess."

(2) Check the beat list first; timing is cheaper to fix in words. (3) Render; run the checker until `BLOCKING OK`; then plan view (camera where the breakdown says?); then clay stills at each beat (framing does the shot's job?). (4) Ask for changes in plain words ("lower the camera to knee height", "Jude clears the gate on frame 56, not 60", "roll the camera 15° by the end"); 2–3 rounds normal. (5) Lock: store plan path and the Rec3 fields.

**Plan-file template (§5.2, exact).** Metres; Z up; `facing_deg` 0 faces −Y (toward the audience in front view), 90 +X, 180 +Y, 270 −X; `loc` is relative to `parent` if given.
- `shot`, `fps`, `frames`, `resolution`: shot ID from the breakdown; 24 fps; length in frames; pixels (default [1280, 720]).
- `pivots`: invisible handles (hinges, groups, a whole cage): `name`, `loc`, optional `parent`.
- `boxes`: grey-box pieces: `name`, `loc` (centre), `size` (x, y, z metres), `rgb`, optional `parent`.
- `figures`: stand-ins: `name`, `loc` (feet), `height`, `facing_deg`, `rgb`, optional `parent`.
- `animate`: keys for any object: `{"object": name, "keys": [[frame, [x,y,z], [rx,ry,rz] degrees], ...]}`.
- `camera`: `lens_mm`, `sensor_mm`, optional `fstop` and `focus_on`, optional `parent`; `keys` as `[frame, camera position, aim point, optional lens mm]`; optional `roll_keys` as `[frame, degrees]`.
- `depth_range_m`: near and far distances for the depth pass.
- `stills`: frames saved as PNG keyframe-image candidates (default first, middle, last).
- `plan_view`: `direction` "top" (floor plan) or "side" (elevation, for shafts and falls), `center`, `size_m` (default 8), `hide` (walls to leave out).
- `beats` (optional): `[frame, "what happens", "script line"]`; ignored by the script, as are unknown fields.

Script behaviour (§5.3): sizes baked into meshes; box mannequin with a "nose" showing facing; rig `CAM_RIG` (keyed, Track To `CAM_TARGET`) with child `CAM` for roll; one sun light; clay (Workbench, outline, cavity, Standard), normal (matcap `check_normal+y.exr`), depth (Map Range near 1.0 / far 0.0, clamped, Raw, 5.x compositor node group), each as H.264 MP4 plus PNG stills; orthographic plan view with a red cone at the camera; camera JSON; USD, baked FBX, .blend. The checker shrinks stand-in parts 3% so touching is not reported; it does not judge pose plausibility or whether a hand reaches its mark.

**P5. Keyframes from clay (Rec4, Route 1).** (1) Clay still for the first (and last) frame. (2) Send with the C2 character reference pack to an image model that accepts a layout image; prompt the look, not the layout. (3) Reject any image where someone moved, resized or lost the eyeline. (4) Use as start and end frames (C1 Recipe 5).

**P6. Depth clip via fal (Rec5, Route 2).** (1) Connect fal's MCP connector (C1 Recipe 1). (2) Ask (verbatim): "Upload `depth.mp4` and the approved first keyframe image. Using `fal-ai/wan-vace-14b/depth` (or `wan-22-vace-fun-a14b/depth`), make a 720p clip with this prompt. Pass the keyframe image as `first_frame_url`, set `match_input_num_frames` and `match_input_frames_per_second` to true and `preprocess` to false. If the clip is under 81 frames, first pad `depth.mp4` by repeating its last frame up to 81. Tell me the price first." (720p: $0.08 or $0.10 per 16 frames; 81 frames ≈ $0.40–0.51.) (3) Compare with the clay video at each beat; apply Rule 41. (4) If output is 16 fps, the editor plays it at 24 fps (every frame kept, no interpolation), then trims the padding.

**P7. Clay reference to a hosted model (Rec6, Route 3).** (1) `clay.mp4` as reference video plus character images to Seedance 2.5 reference-to-video (or H3). (2) Prompt with the §6 template, mapping stand-in colours to characters. (3) Two takes; keep the one whose blocking matches the plan view; if both swap or merge people, apply Rule 42.

**P8. Own performance (Rec7, Level 4).** (1) Film yourself: locked-off phone, whole body, plain background, good light. (2) Rokoko Vision (one performer) or DeepMotion (several) → FBX or BVH. (3) LLM imports it onto an MPFB or Mixamo stand-in in the master set and re-renders. (4) Stand-in render + character image to Kling Motion Control, or the pose pass via Route 2.

**P9. Live MCP (§5.4, optional).** (1) Save; spare machine. (2) Community: install `uv`; add `{"command": "uvx", "args": ["mcp-for-blender"]}` to the LLM app's MCP settings; `uvx mcp-for-blender install-addon`; enable "Interface: MCP for Blender"; N → MCP tab → Start MCP Server (optional `BLENDER_MCP_SAFE_MODE=1`, `DISABLE_TELEMETRY=true`). (3) Or official Blender Lab connector (Blender 5.1+; official Claude connector since 28 Apr 2026). (4) Test: "List the objects in the scene and take a viewport screenshot." (5) Work by plan-file edits.

**Route menu (§6).** Route 1: restyled start/end keyframes → image-to-video; model invents the motion between; weak when motion is the point. Route 2: depth/clay/normal/pose video plus look reference → control model (Wan VACE depth on fal, Wan 2.2 Fun Control, LTX-2.3 union control, H3 ControlNet); camera path and blocking come through almost exactly. Route 3: clay as reference video to Seedance 2.5, H3, Kling Motion Control, Marey, Runway Act-Two/Aleph 2.0, Luma Modify V2, Wan-Animate-2; looser, better image, native audio on Seedance and H3; best for a non-technical user when the move matters. Route 4: `camera_track.json` → research models (Uni3C: 7 numbers, distance, elevation, azimuth, three offsets, focal length; ReCamMaster: 10 presets). Route 5: Blender layers composited.

## 5. Checklists

Assembled from the file's recipe checks and failure table.

**Per location (Rec2)**
- Everything the script mentions is present, at real size, placed so each scripted action is possible; fixed marks modelled wherever visible; one flat colour per material.
- Top plan and side elevation filed; guesses listed.

**Per shot, before any pass goes to a video model (Rec3, §11)**
- Beat list checked before rendering.
- Checker prints `BLOCKING OK`.
- Plan view: red cone where the breakdown puts the camera; camera not in a wall; clip start 0.01–0.05 m in tight sets.
- Clay stills frame each beat's purpose; figures face correctly (nose marker; `facing_deg` 0 = −Y).
- Riders parented or keyed on the carrier's frames; physical motion keyed every frame; weightless bodies hand-keyed to the cage.
- Depth: Raw, tight `depth_range_m`, actors not flat grey.
- Frame rate and length suit the model (16 fps Wan; ≥81 frames or padded).
- Text, screens, beads in `composite_layers`; glass/water inserts separate; no control over lip-sync faces.
- Rec3 fields filled.

**Per keyframe image / clip (Rec4–6)**
- Nobody moved, resized or lost eyeline against the clay still.
- Clip matches clay at each beat and the plan view; no identity swap or merge; Rule 41 fixes applied.
- 16 fps output retimed; padding trimmed.

**Per LLM-written script (§4.8 Blender 5.x traps)**
- Compositor: `bpy.data.node_groups.new(name, "CompositorNodeTree")`, `scene.compositing_node_group = tree`, Group Output; not `scene.use_nodes`/`scene.node_tree`.
- `"BLENDER_EEVEE"`, not `_NEXT`; no `action.fcurves` (use `keyframe_insert()` or channelbags via `bpy_extras.anim_utils`).
- Annotations = `bpy.data.annotations`; Grease Pencil = `bpy.data.grease_pencils` (no `grease_pencils_v3`).
- File Output: `directory`, `file_name`, `file_output_items` (not `base_path`, `file_slots`, `layer_slots`).
- `ShaderNodeMapRange`/`ShaderNodeMath` in compositor trees (no `CompositorNode...` versions).
- Set `image_settings.media_type = "VIDEO"` before `file_format = "FFMPEG"`.
- View transform Standard for clay/normal, Raw for depth/data.
- Sizes baked into meshes, never `obj.scale` on a parent.

**Per stand-in (§4.4)**: level fits the control (boxes for depth; MPFB/Mixamo for pose; own mocap for exact acting; Rigify/Cascadeur for creatures and precise stunts); non-human = boxes + depth.

## 6. Saying it to AI models

- **Video beats words** [§7, §4.1]: words are ambiguous about speed, height and lens, and models blur move versus zoom; a depth or clay video is not ambiguous. Hosted "camera control" is presets or references, not numbers (Higgsfield's 50+ named moves: dolly, crane, bullet time, FPV drone; Marey re-framing one still; Kling 3.0 per-shot camera; Luma Ray3.2 up to 16 keyframes; move-copying in Seedance 2.5 and H3).
- **Restyle prompts** [Rec4]: prompt the look, not the layout; name what each flat colour is: "the white strip is the worn bright steel sill; wet brick; light from the landing gates striping past; Iona in a blue work shirt…".
- **Reference-video template** [Rec6, verbatim]: "Follow [Video1] exactly for camera movement, positions and timing; it is a grey 3D layout, not the look. Characters: [Image1] is Iona (the blue figure), [Image2] is Eli (orange), [Image3] is Jude (red). Make it a photographic scene: …". Seedance 2.5 addresses uploads as "[Video1]", "[Image1]".
- **Depth of field**: the recorded f-stop tells the prompt "shallow focus, background soft" or not [§4.1].
- **When output disagrees with previs**: change plan or strength, not wording [R20]; textured-box output needs a more descriptive prompt [Rec5].
- **What fails in words**: exact text ("HULL CLEARANCE", "UPWARD SPEED … Twelve. Six. Three."), mirrored text, physics (models add gravity back), multi-person interaction, hands crossing the body ("spaghetti limbs"), face drift (give several character images), injury content (say "small dark red droplets" or composite).

## 7. The Catch

**Conventions** [§12]: stand-ins Iona blue, Eli orange, Jude red, the figure near-black (renders dark grey); sill white, band yellow; 24 fps; camera choices follow B1 §10 (cage camera level, never shakes; Iona's grid POV top-down; framing repeats across the black). All five plans pass the checker.

**Shaft master set** [§4.3, author's numbers]: shaft ~2.6 m square; cage 2.0 × 2.0 × 2.3 m; opening 2.0 m wide × 2.2 m tall; sill ~9 m (9.05); band at 2.0 m on all four walls; walls to 25 m. Figure: boxes, 2.4 m, head low between the shoulders, pale strip at 2.28 m, depth only. Iona 1.68 m.

**Example A, cage stops, falls, turns.**
- `plan_cage_fall.json` ("fall", 40 frames): camera parented to the cage, low SE corner on the grid (0.8, −0.8, 0.3), aimed at Iona's middle, 24 mm, f/2.8, focus Iona, level. Frames 1–12 stopped at the sill; drop at 12; 12–40 free fall 9.2 → 2.53 m keyed every frame; Iona's hands and head stay at the grid, legs float to a 60° tilt ("like washing"); three blood beads rise and turn; no roll, no shake; cut on the CLACK at 40. Route 2 (depth 0.3–4 m, padded to 81, restyled first frame) or Route 3 Seedance; beads by Route 5.
- `plan_grid_pov.json` (insert, 29 frames = fall frames 12–40): lattice floor (2.5 cm bars every 25 cm); camera parented at (0.3, 0.25, 0.35) looking straight down, 24 mm; the band grows from a thin ring to fill frame by frame 22 (the stripe as "the fall's clock", B1). Route 2 depth or simply Route 1.
- `plan_inversion_reveal.json` ("reveal", 36 frames after one black frame): cage built inverted, rising 5.0 → 6.4 m, slowing; stand-ins keyed on the cage's frames (Jude across Eli's arms); camera not parented, world-upright (0.7, −0.9, 3.2 → 4.6), 24 mm, so the grid is at the top of frame. Directing choice [J]: during the fall the camera belongs to the cage, after the black to the world, so "Everything is in the wrong place." is a 180° swap with no camera move; low SE 24 mm framing repeated both sides. Route 1 (frames 1 and 36).

**Example B, push through the opening** (`plan_push_sill.json`, 72 frames): camera static low in the passage (4.2, −0.8, 9.3), 2.9 m from the sill, aimed at the opening, 24 mm, f/4, focus Iona. Inverted cage rises 9.0 → 11.6 (apex frame 50) → 11.2 (72, starting down); body heights keyed every 2 frames from the cage's curve; 37–48 bodies go sideways through the gate (Jude horizontal, head first; Eli leaning; Iona upright); 48 palm meets sill (cut to a 50 mm insert, Level 0); Jude's boot past the wall 56, Iona's knees 60; small camera drift by 72. Rise eased, not ballistic. Route 3 first (Seedance, `clay.mp4`, three references); if people swap or merge, Route 2 depth for bodies and Route 1 for the palm insert.

**Example C, the chest opens** (`plan_chest_opens.json`, 96 frames): over Iona's right shoulder (0.25, −2.4, 1.7), 35 mm, f/2.8, focus on vessel; latches 8–26 (sound only); left door swings 105° over 30–70, right 4 frames later; Iona steps back 20 cm (40–60); slow push to (0.12, −1.95, 1.6), 50 mm, vessel (0.14 × 0.14 × 0.45 m) centred. Route 2 depth (no pose) with C2 references of the black exosuit and pale strip, or Route 3; the animal and the limb leaving its socket as separate macro image-to-video inserts shot from high; "the enormous black hand goes dead" as a second small plan with a keyed shoulder pivot, low and wide.

**Flagged for the writer/user**
- Sill height: the script says "Halfway up"; end the shaft at ~18 m or accept the kit's 25 m walls (sill a third of the way up).
- Adopt C1 Recipe 8 (flip the turned world)? If so, the reveal is the first flipped shot and Iona, Eli, Jude and the cage are pre-reversed.
- The red tag after the turn: turn it away in the plan, or render it as its own layer so it is not mirrored.
- Chest-opens camera: kit push to 50 mm, or B1 strict (static at (0.25, −2.4, 1.7) on 35 mm, aim moving from (0, 0, 1.9) to (0, −0.1, 1.55), vessel by macro insert).
- Iona's reach in the push: hand-keyed or mimed and captured.
- Not built (copy a plan): "the opening flicks past. Going up." POV (aim at the east wall); "The yellow stripe is under her boots, getting smaller" (grid POV, rising cage, world-upright camera); the hand flat on the chest (needs a shoulder pivot); the dead-hand arm drop.

## 8. Conflicts and open questions

- **16 fps handling is given two ways** [R14 vs Route 2 / Rec5]: render previs at 16 fps, or send 24 fps control with `match_input_frames_per_second` and play the 16 fps output at 24 fps. The file does not reconcile how these interact; stage writers should pick one per model and test.
- **Two ladders**: `previs_level` 0–5 uses the §9 ladder (with a "1b"); the §4.4 stand-in ladder is a separate 1–5 scale.
- **Chest-opens lens vs B1** (B1 §9.2 / Example 5: 35 mm looking up, tilt, macro, then 50 mm on Iona; 24 mm on the ship only for wides): the kit adds a push to 50 mm.
- **Linear vs inverse depth**: how control models read the kit's linear depth is untested.
- **No end-to-end generation was run**: routes rest on makers' descriptions and PrevizWhiz (CHI 2026, 10 participants: faster iteration, but match-to-intent median 3, "not very controllable").
- **Numeric camera tracks**: no hosted product found takes one [U: absence of evidence]; CameraAnything and CoaG state no released code or weights.
- **Unverified** [§13]: Mixamo status and terms; makers' prices for FrameForge, set.a.light 3D, Flow Studio, Jetset/Spark Story, DeepMotion paid, Unreal licence, Move One (Jan 2025 page); MPFB headless; LTX-2.5 union control; UE 5.9/UE6; Claude Blender connector switch-on; fal `preprocess`; Cascadeur and Intangible MCP; Meshcapade closure; Runway Aleph 2.0 limits; script inside the Blender GUI; Kling Motion Control audio.
- **Licensing**: DeepMotion, QuickMagic and Cascadeur free tiers are non-commercial; the open GVHMR pipeline's body model may bar commercial use [U]; Mixamo terms bar redistributing characters; H3 ControlNet licence has regional conditions.
- **Hardware**: Wan 2.2 14B control 64 GB download, 24 GB+ GPU; Uni3C ~46–51 GB; H3 ControlNet 80 GB; Wan-Animate-2 eight data-centre GPUs; Comfy Cloud Standard cannot import own models, 30-minute cap.
- **Dependencies**: B1 (lens family, §10 camera choices, §10.2 flip); C1 (model choice, prices, Recipes 1, 4, 5, 8, text failures §9, filters §4); C2 (layout-accepting image models, reference pack); A3 (floor plans, breakdown).

## 9. Section map

- **Header box**: the file's five purposes.
- **§0 How to read**: tags; companion kit and its correction history; related files; full-frame convention; search limits.
- **§1 Terms**: ~45 plain-English definitions.
- **§2 Situation (27 Sep 2026)**: nine verified facts (Blender 5.2.2 LTS/bpy; 5.0 script breakage; VR scouting; Blender MCP connectors incl. Claude's official one; Unreal 5.8 MCP and free MetaHuman markerless capture; hosted models accepting previs; cheap open control; camera-trajectory control still research, PrevizWhiz; cheap phone mocap) plus the recommended path.
- **§3 Landscape tables**: 3A Blender and add-ons; 3B LLM connectors; 3C previs/posing apps with verdicts; 3D AI mocap from video with prices; 3E bridges into AI video.
- **§4 Blender basics**: 4.1 camera (FOV table, depth of field, move vs zoom, clip start); 4.2 rigs and paths (free-fall timing); 4.3 grey-box sets; 4.4 stand-in ladder; 4.5 Grease Pencil; 4.6 engines and passes (Raw depth); 4.7 camera exports; 4.8 Blender 5.x trap table.
- **§5 LLM-driven Blender**: 5.1 Modes A/B/C; 5.2 plan-file schema and prompt; 5.3 full tested script, outputs, blocking checker; 5.4 live MCP setup.
- **§6 Bridging into AI video**: Routes 1–5 with fal Wan VACE limits; 6.1 ComfyUI install, hardware, Comfy Cloud prices, comfy-mcp.
- **§7 Which tool for which aim**: nine aims × no-3D option, previs option, route, reason.
- **§8 Decision rules**: rules 1–26.
- **§9 Difficulty ladder**: Levels 0, 1, 1b, 2–5; minimum viable setup.
- **§10 Recipes 1–7**: setup, master set, one shot (+ breakdown fields), keyframes, fal depth clip, hosted reference, own performance.
- **§11 Failure modes**: 18-row table.
- **§12 Worked examples**: A fall, grid POV, reveal (diagram, camera tables, kit correction, routes); B push; C chest opens (lens note vs B1).
- **§13 What I could not verify.**
- **§14 Sources**: P1–P68; P58 is the author's own test.
