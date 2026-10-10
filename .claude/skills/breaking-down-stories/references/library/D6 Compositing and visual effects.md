# D6. Compositing and VFX execution: layers, keying, roto, tracking, corner pins, text inserts, flips, grain match

> **What this file is for**
> 1. Doing the jobs the other files send to "composite": screens, exact text, flipped worlds, floating beads, sparks, reflections, visor graphics, appear/vanish cuts, multi-take shots.
> 2. Choosing a tool a non-technical user can run through an LLM (ffmpeg, Python, Blender), and knowing when hands-on GUI work (Resolve, After Effects) cannot be avoided.
> 3. Nine step-by-step recipes with difficulty, novice time, what a script automates, and an acceptance test; two scripts tested for this file.
> 4. One `comp_plan` per shot that merges C5 `vfx`, C4 `composite_layers`, C1 `composite_elements` and C2 `insert_graphic`, plus a QC checklist.
> 5. Worked examples on *The Catch* (SC06 beads, SC15 tablet feed, SC10 kitchen, SC21 label, SC26 visor) and *The Long Places* (the livestream, the pool).

**Fact-check note (2026-09-27).** An adversarial re-check opened Blackmagic's Fusion and Studio pages, Puget Systems, CG Channel, Digital Production and CineD on Resolve 21.0/21.1, Foundry's Nuke Non-commercial page and FAQ, Adobe's After Effects plans, eight Blender 5.2 LTS manual pages and the 5.0, 5.1 and 5.2 compositor release notes, the FFmpeg filter manual, Meta's SAM 3.1 post, the SAM 2 and SAM 3 repositories and licence, seven fal model pages, Runway's Aleph 2.0 page, Beeble's pricing, and the MatAnyone 2, ProPainter, IC-Light, CoTracker and davinci-resolve-mcp repositories; re-matched every quoted line of *The Catch* and *The Long Places*; and re-ran both kit scripts. **Corrections:** Blender's **Film Grain** is a built-in node-group asset new in 5.2 LTS, **Sensor Noise** a built-in asset since 5.0, **String to Image** a node new in 5.2; none is in the bpy 5.0.1 the kit was tested on (§3A, Rec9); Blender's Inpaint node fills only a few pixels (wires), not objects; free Resolve 21.1 keeps console scripting but moved Python, external scripting and Workflow Integrations to Studio, and **Studio 21.1 has a native MCP server** for Claude and Claude Code (§3A); IC-Light V2 is hosted only (the Apache 2.0 code is V1); Wan VACE is priced per second **at 16 fps**; a misquotation of C2 removed (W4). **Kit bugs fixed and re-tested:** `screen_insert.py` averaged corners over 3 frames by default, which on a moving screen left a dark sliver at the leading edge (about 500-700 dark pixels per frame in the test), and a finger crossing a corner threw that corner off by up to 30 px; the default is now no averaging, and a corner that jumps is replaced by its predicted position (0 bad pixels on all 48 test frames). `element_layer.py` put its key light about 4 m behind the camera (a world position set before parenting), so beads rendered dark (mean red 57 of 255); fixed (mean red 148, with a highlight). **Reconciled with later files:** the grain pass (D8-R34: one film grain at timeline level) and the visor text after the turn (D12 §4.3: it does not snap readable). New rows: SC17 and SC23 screens, the SC26 floating screw, the SC06 muzzle flicker (D11).

**Second fact-check (2026-09-28).** Re-opened Blackmagic's Studio and Fusion pages, Digital Production, Puget and CineD on 21.1, CG Channel on 21.0, Foundry's Nuke Non-commercial page, five Blender 5.2 manual pages (Film Grain, Sensor Noise, String to Image, Inpaint, Plane Track Deform), the FFmpeg filter manual (`perspective`, `noise`, `overlay`), Meta's SAM 3.1 post, the SAM 3 README and licence, the SAM 2, IC-Light, ProPainter, MatAnyone 2 and CoTracker licences, the davinci-resolve-mcp README, fal's SAM 3, SAM 3.1 (page and API schema), VEED, Wan VACE (page and API), IC-Light V2 and Bria Video Eraser pages, Runway's Aleph 2.0 page and Beeble's pricing; re-matched every quoted line of *The Catch* and *The Long Places* and the scene each is assigned to (all verbatim, all in the stated scene); re-ran the static ffmpeg pin (ffmpeg 7.0.2), `screen_insert.py` and `element_layer.py` (bpy 5.0.1; frame 26 bead mean red 148, as before). **Corrections:** free Resolve's limit is UHD at 60 fps; "no 10-bit" was too strong (Studio's page lists 10-bit real-time playback and hardware H.264/H.265 among its additions); the Studio-only grain is the **Film Look Creator**, not an "Advanced film grain"; Bria Video Eraser **accepts up to 5 s** (`auto_trim` on by default); Wan VACE bills frames ÷ 16, so matching a 120-frame 24 fps plate costs $0.60, not $0.40; fal's SAM 3.1 also takes point and box prompts (up to 16 objects); fal's SAM 3 video returns the video **with the mask drawn on it** by default (`apply_mask: true`), not a clean matte (Rec3, Rec7, §3B); Rec5 cited B3 R29 (CLEAR glass) for the ANGLED reflection set-up (now B3 §8.1 and R28); Aleph 2.0's page says "Change a specific element, preserve the rest" (removal by prompt now [U]). **Added:** the order mismatch between `corners.csv` (TL, TR, BR, BL) and ffmpeg's `perspective` (TL, TR, BL, BR) (Rec1); rule 14b choosing the mirror method (the library's agreed decision table); era definitions (§1); the script support for Nell being unturned (SC17 row); a five-step routine for running any recipe (§6); validator check VC8 (no second flip in D8's conform); conflicts with D5's `post_chain`, D8's `finish.flip`, D3's "composited face" and D13's plate counting (§12). **Re-tests:** static pin with four coloured quadrants: each landed on its named corner, and without the 8 px pad the whole frame took the edge colours; `screen_insert.py` on the 48-frame drifting plate: 0 green and 0 dark pixels left inside the screen, 6 frames `held`.

## 0. How to read this file

- **Tags.** [V] verified at a primary source on 2026-09-27, or run by the author of this file ("author test"); [U] unverified or secondary only; [J] judgment. Tool facts go stale monthly: re-check anything older than 30 days before paying (C1 staleness rule).
- **Companion kit** `research/D6_comp_kit/` [V, author test 2026-09-27; both scripts fixed and re-tested by the fact-check the same day]: `screen_insert.py` (pins a picture or clip to a green screen in every frame; Python 3.11, OpenCV 4.10, NumPy 1.26); `element_layer.py` (renders floating elements as a transparent layer through C4's `camera_track.json`; tested on bpy 5.0.1); `beads_example.json`; `make_test_plate.py`; three example frames (made before the fixes). Keep NumPy below 2.0 in the same Python as bpy 5.0.1, which requires it [V, fact-check: installing OpenCV 5 pulled NumPy 2.4 and broke the requirement].
- **Builds on:** C1 (R6-R8, Rec8, Rec9), C2 (R5, R6, rules 31-37, mirror eras), C3 (§12-13, Rec5, Rec6), C4 (Route 5, `camera_track.json`, rule 42), B1 (§10.2 methods, §10.4-10.6, VISOR VIEW), B2 (R20), B3 (R28-R29, §8.1), B4 (M01, M11, §14.2), A3 (R11), C5 (IDs, `vfx`, validator). "Rule N" means the numbered rules in that file's digest; "R#" and "Rec#" are the file's own labels.
- **Scope.** This is the "compositing file" C1 Rec9 cites: 2D compositing of generated clips. Not covered: CG characters, matchmove of handheld live action, whole-film grading.

## 1. Terms (one plain sentence each; one word per concept)

- **Composite (comp):** one finished shot built by stacking several pictures.
- **Plate:** the background clip or still everything else sits on (as in C1, C2).
- **Clean plate:** a plate with an unwanted thing removed.
- **Element:** any single thing added to a plate (beads, sparks, a reflection, a character).
- **Layer:** one picture stream in the stack, counted from the bottom (the plate is layer 1).
- **Matte:** a black-and-white picture that says where a layer shows (white shows, black hides); tools also call it a mask or alpha.
- **Key (keying):** making a matte automatically from a colour, usually bright green.
- **Despill:** removing the green tint a green screen leaves on nearby edges and skin.
- **Roto:** making a matte by drawing shapes by hand, frame by frame.
- **Segmentation model:** an AI model that makes a matte for a named object in every frame (SAM 3).
- **Track:** the recorded positions of points or corners in every frame; **tracking** is making it.
- **Planar track:** a track of a flat surface (screen, sign, label) as four moving corners.
- **Corner pin:** warping a flat picture so its four corners land on four chosen points.
- **Insert graphic:** exact text or a screen image made outside any AI model (C2 R6).
- **Flip:** mirroring a picture left-right; **flip count** is how many times a layer is flipped on its way to the final frame.
- **Grain:** the fine, moving random texture of film or a camera sensor (this file uses "grain" for both).
- **Edge halo:** a light or dark rim around an element that gives the comp away.
- **Light wrap:** a thin bleed of plate light over an element's edges so it sits inside the scene.
- **Add / screen blend:** ways of laying a layer on that can only brighten the plate (for light, sparks, reflections, glows).
- **Parallax:** near things moving more than far things when the camera moves.
- **Screen-locked:** a layer fixed to the frame, not to anything in the scene.
- **Intermediate:** a file passed between comp steps; use PNG or ProRes 4444, never repeated H.264, which loses detail at each save.
- **ProRes 4444:** a high-quality video format that can carry a matte (alpha) inside the file.
- **Straight / premultiplied alpha:** two ways a file stores see-through edges; reading one as the other gives dark or light rims.
- **Headless:** a program run by a script with no window (Blender as `bpy`, the Python module version of Blender).
- **Difference view:** one frame subtracted from another, so anything unchanged shows black and only changes light up.
- **Era (C2) or phase (B1) A / B / C** (*The Catch*): the film's three mirror periods. A: from the opening to the first turn, nothing mirrored. B: from "Her eyes open" to the second turn, the world (shaft, city, all text, Saye, the nurse, Nell, world-made screens and suits) is mirrored to Iona and so to the camera, while turned people and things (Iona, Jude, Eli, the cage, the flask, their clothes, turned meals, the ship interior) are not. C: after Iona's second turn, the world reads normally again and Jude, Eli and their meals are mirrored (B1's summary).
- **Turned:** having passed through the reversal, so the body is mirror-reversed relative to the world (a ring on the other hand, a scar on the other side).
- **Pre-reverse:** mirror a character or detail on purpose before a whole-picture flip, so that it comes out the right way round after the flip.
- **Asset (Blender):** a ready-made node group that ships with Blender and is added from the asset shelf; a script must load it from Blender's Essentials library rather than create it by name.

## 2. Core principles

1. **Exact things are made, not generated** [J, from C1 R6-R8, C2 rule 31, C4 R9]: words, screens, beads, visor drawings, anything backwards.
2. **Regenerating tools first, exact tools last** [J]. AI passes (removal, relighting, inpainting, upscaling) redraw pixels and garble letters, so they run on the plate before any exact layer.
3. **Count the flips** [J]. Every layer must reach the frame with the mirror state C2's era table gives it: `normal` = even flip count, `mirrored` = odd. Most mirror errors are one flip too many or too few.
4. **The plate sets the rules** [J]: light direction, grain, blur, black level, frame rate and size; elements match it.
5. **One camera, stored** [J, C4 R9]. Render Blender elements through the stored previs camera; if the generated clip drifted, correct the element, not the plate.
6. **A still is a valid plate** [J, C1 rule 24]. For locked-off shots (CCTV, tablet feeds, inserts), a checked still with animated grain beats a clip that wobbles.
7. **The LLM writes and runs the scripts; the user judges by eye** [J], looking at three named frames per shot.
8. **Comp at delivery size** [J]. Upscale the plate first (C1, D8-R24), then add exact layers, because upscalers redraw text.
9. **Match grain in the comp; add film grain once, later** [J, reconciled with D8-R34]. The comp gives added layers the plate's own texture; the one grain for the whole film goes on at timeline level after the grade (D8), so a comp never adds a second film-wide grain.

## 3. Tool landscape (checked 2026-09-27; re-checked 2026-09-28)

### 3A. Compositing programs

| Tool | Cost | Good for | LLM-drivable? | Verdict |
|---|---|---|---|---|
| **ffmpeg** | Free | Overlays, fixed corner pins (`perspective`), `hflip`, grain (`noise`), keys (`chromakey`, `despill`), blur, retiming, ProRes 4444 with alpha [V: docs; author test] | **Yes, fully** | First choice for static shots and final assembly. Some builds lack `drawtext` (the tested one did) [V, author test]: draw text in Python |
| **Python + OpenCV + Pillow** | Free | Per-frame pins, green-screen detection, timestamps, HUD drawings, measuring grain and blacks [V, author test] | **Yes, fully** | First choice for anything that moves or needs exact text |
| **Blender compositor** (5.2 LTS) | Free | Nodes: Corner Pin, Plane Track Deform ("used to replace flat planes in footage by another image, using plane tracks"), Keying, Cryptomatte, Inpaint (fills only a few pixels, for wires, not objects), String to Image (new in 5.2). Built-in assets: Sensor Noise and Chromatic Aberration (since 5.0), Film Grain (new in 5.2) [V: manual, release notes]; elements through `camera_track.json` [V, author test] | **Yes** via headless bpy; planar tracks need markers placed by hand in the Movie Clip Editor [V: manual]. bpy 5.0.1 has no Film Grain or String to Image [V, fact-check test] | First choice for 3D elements; for grain in Blender install 5.2 LTS, else use ffmpeg or Python. Mind C4 §4.8's Blender 5.x traps |
| **DaVinci Resolve 21.1 free** | Free (Studio $295 once) [V: Blackmagic] | Fusion page: planar tracker, 3D camera tracker, Delta Keyer, bezier and B-spline roto [V: Blackmagic]; free edits and finishes "up to 60 fps in resolutions as high as Ultra HD 3840 x 2160" [V: Blackmagic Studio page]; Studio's additions include "real time playback of professional 10-bit formats" and hardware H.264/H.265 decoding and encoding [V: same page]; exactly which 10-bit files free handles is [U] | **No, not directly**: 21.1 moved Python to Studio ("We have moved the ability to script in Python to the Studio version.") [V: Puget quoting Blackmagic]; "the scripting API remains available from the console in the free edition", while "Workflow Integrations, the native UIManager and external scripting access require Resolve Studio" [V: Digital Production]. An LLM can only write steps or a console script the user pastes | Manual fallback for planar tracking, with click-by-click LLM steps. Magic Mask and the Film Look Creator ("film stocks, halation, grain, gate weave") are Studio-only [V: Blackmagic Studio page] |
| **Resolve Studio 21.1** | $295 once [V] | Adds Magic Mask ("Render in Place" since 21.0) [V: CG Channel], Python and Lua scripting [V: Blackmagic] | **Yes**: a native MCP server: "Resolve Studio 21.1 can connect to Claude, Claude Code and ChatGPT Codex, with setup handled through File > Setup AI Assistants" [V: Digital Production, CineD]; also community servers (e.g. `samuelgursky/davinci-resolve-mcp`, MIT; its free-edition bridge is a 21.0.x path) [V: repo; U: reliability] | Only if someone will also edit or grade in Resolve (D8 lists the same trigger) |
| **After Effects** | US$22.99/mo, annual billed monthly [V: Adobe; on 2026-09-28 Adobe's page served a regional CAD $29.99 price, and 2026 secondary sources give US$22.99] | Standard 2D comp, roto, tracking [U] | Partly: ExtendScript; community MCP servers [V: exist; U: quality] | Only if already paid for |
| **Online editors** | Varies [U] | Runway Edit Studio runs Aleph 2.0 in the browser [V: Runway]; browser editors offer overlays and green removal [U] | Runway via its connector (C1) [U for Aleph]; others no | AI passes only; exact layers locally |
| **Nuke Non-commercial** | Free | Film-grade comp | **No**: "Rendered output is restricted to 1920x1080 HD and the MPEG4 and H.264 formats are disabled"; "The Python API only allows the retrieval of 10 nodes per script"; "meant for personal, educational, and other non-commercial use"; each version works "for 180 days after a version of Nuke is built and released" (newer versions keep it free) [V: Foundry] | Not for this project |

### 3B. AI helpers

| Helper | Does | Access, price | Licence / caution |
|---|---|---|---|
| **SAM 3 / 3.1** (Meta) | Matte for every instance of a named thing across a video; 3.1 (27 Mar 2026) can "track up to 16 objects in a single forward pass" [V] | fal `fal-ai/sam-3/video`: "$0.005 per 16 frames", prompts by text, points, boxes or masks, output an MP4 plus optional per-frame boxes [V]; `fal-ai/sam-3-1/video`: "$0.01 per 16 frames", text (comma-separated for several objects), point or box prompts, `max_num_objects` 16, MP4 or VP9 WebM [V: page and API schema]. **Matte caution:** both default to `apply_mask: true` ("Apply the mask on the video"), which returns the picture with the mask drawn on it, not a black-and-white matte; set `apply_mask: false` and check on one clip that the output is a clean black-and-white matte before building a comp on it [V: parameter; U: what the `false` output looks like]; local: Python 3.12+, PyTorch 2.7+, CUDA 12.6+ GPU, checkpoints gated (request access on Hugging Face) [V] | SAM License (19 Nov 2025): "royalty-free limited license", bars ITAR, military, weapons and similar uses [V]. SAM 2: Apache 2.0 [V] |
| **Video background removal** | Subject matte with alpha | VEED on fal: "$0.0225 per 30 frames" with edge refinement, $0.015 without; "VP9 with alpha channel (WebM) or dual H264 streams (RGB + alpha mask)" [V]; Bria on fal: transparent WebM VP9 by default, also ProRes in MOV; input under 30 s and under 4000×4000 [V; price U] | Check hair and hands |
| **MatAnyone 2** | Fine human matte from a first-frame mask (make it with SAM) [V] | Local GPU; Hugging Face demo | NTU S-Lab 1.0, non-commercial [V] |
| **Object removal / inpainting** | Removes a thing, fills the hole | Bria Video Eraser: "$0.14 per second of video", text prompt of a plain noun ("person", "car", "logo"), accepts videos up to 5 s (`auto_trim`, on by default, cuts longer input to 5 s) [V]; Wan VACE 14B inpainting with a mask video: "$0.08 per video second for 720p, $0.06 per video second for 580p, $0.04 per video second for 480p. Video seconds are calculated at 16 frames per second" (so the bill is frames ÷ 16); output 81-241 frames at 16 fps by default, or matched to the input's frame count and rate [V: page and API]; retime a 16 fps output to 24 (C4 R14) [J]; Runway Aleph 2.0: "Change a specific element, preserve the rest", clips "up to 30 seconds long at 1080p", in Runway's Edit Studio [V]; removal by prompt, price and API [U] | ProPainter: NTU S-Lab 1.0, "strictly for non-commercial purposes" [V]. All regenerate pixels |
| **Relighting** | New light direction on a person | IC-Light V2 on fal (stills only): "$0.1 per megapixel" [V]; the open IC-Light code (V1) is Apache 2.0, and its default background remover (BRIA RMBG 1.4) is non-commercial, so swap it for commercial use [V: repo]; Beeble SwitchLight 3.0 video relighting, Creator $19/month or $16/month billed yearly, "Full commercial license", API sold separately [V] | Relight the keyframe still before image-to-video when possible [J] |
| **Point tracking** | Tracks any points | CoTracker (Meta), local | Mainly CC BY-NC (non-commercial) [V]; commercial: OpenCV or green detection [J] |

fal endpoints are LLM-drivable through the fal connector; Beeble, Hugging Face demos and Runway's Edit Studio are hands-on [U for Runway's API]. **Default** [J]: ffmpeg + Python + Blender run by the LLM, hosted helpers via the fal connector (C1 Rec1), Resolve free as manual fallback; nothing to buy. Buy Resolve Studio only if the film is also edited or graded in Resolve; then its MCP server lets the LLM drive it (test on a copy of the project first, D8).

## 4. Decision rules

**Where the work happens**
1. If the element is exact text, a screen image, a HUD drawing or anything backwards, then make it as an insert graphic and composite it, because models misspell and cannot mirror text (C1 R6-R7, C2 rules 31-32).
2. If the fix is possible on the keyframe still (a label, people added to a mirrored plate, a ring), then do it there (C2 R4-R5) and animate with minimal motion, because a still comp takes minutes and a video comp hours [J].
3. If text sits on a soft or curved surface (a stitched blanket), then fix it on the still and keep motion minimal, because corner pins fit only flat, rigid surfaces [J].
4. If the element moves in 3D relative to the camera (beads, sparks), then render it in Blender through `camera_track.json`, because a 2D element cannot change size and perspective correctly [J, C4 Route 5].
5. If the element is light (sparks, glow, reflection, HUD), then use add or screen blend, because light only adds [J].
6. If an AI pass (removal, relight, inpaint, upscale) is needed, then run it before any exact layer, because it redraws what it touches (principle 2).

**Tool choice**
7. If the shot is locked off, then use ffmpeg with fixed corners, because nothing needs tracking [V, author test].
8. If a screen or flat card moves, then generate it pure green and run `screen_insert.py`, because corners are then found automatically and fingers stay in front [V, author test].
9. If the screen cannot be green (refused, or green light would fall on a face), then generate it dark and track its corners by hand (Blender Movie Clip Editor or Resolve Fusion planar tracker), because a dark screen has no colour to key [J].
10. If a program needs clicks, then the LLM writes numbered steps with menu names and the user sends a screenshot after each, because that is how a non-technical user gets through a GUI [J].
11. If the project is commercial, then avoid non-commercial helpers (MatAnyone, ProPainter, CoTracker, Nuke NC), because their licences forbid it [V].

**Tracking**
12. If the generated clip's camera differs from the previs by more than about 1% of frame width at any beat (compare two fixed points), then track the clip and move the element layer by the difference, because control video is followed closely, not exactly [J; C4: no end-to-end test was run].
13. If the camera is bolted to a moving carrier (the cage), then move elements by the camera's translation so they float in carrier space, which is what "hangs in the air between them" needs [V, author test].
14. If corners jitter more than 2 px in a static or slow shot, then average them over 3-5 frames (`--smooth 3`); if the screen moves, then do not average, because detection noise reads as a trembling screen, while averaging a moving screen makes the picture lag and leaves a dark sliver at its leading edge [V, author test and fact-check re-test; threshold J].
14a. If a finger, hand or prop crosses a screen corner, then let `screen_insert.py` replace the jumping corner by its predicted position (`--jump 6`, marked `held` in `corners.csv`), and if more than about 12 frames in a row are `held`, track by hand (rule 9), because a prediction drifts [V, fact-check re-test: a crossing finger moved one corner by up to 30 px before the fix; 12 frames J].

**Mirror world**
14b. **Choosing the mirror method for a flipped-era shot** [J; follows the blueprint's `mirror_route` order, `design/blueprint.md` §8.5, which settles A3, B1, C1, C2 and C3's differing routes; first match wins after row 1]: (1) if readable text is in frame, then always add it as a text graphic in its derived orientation, composited after any flip (Rec2), and let the model see a blank surface; (2) if a plot-sided detail of a mirrored element is visible (ring, raised hand, palm, scar), or the face of a character whose mirror state differs from the location's covers at least 0.10 of frame height, then use the plate route (Rec3: flip the location picture, add the unflipped characters with an image-edit model, no flip after); (3) if every mirrored element in frame is seen in only one orientation in the whole film, then prompt the final picture directly (derived sides, flipped reference pictures), no flip; (4) if characters who differ from the location are in frame but small, with no plot-sided detail, then flip their reference pictures before generating and flip the clip after (B1 method 1); (5) if the location is mirrored and no character differs, then generate normally and flip the clip; (6) if nothing is mirrored, then do nothing. Because the cheaper routes are safe only when no small sided detail can come out on the wrong side. Do not "build the world mirrored" in the prompt (A3 Ex4): models asked for backwards text produce gibberish (C1 R7). Inserts of a sided detail (a ring close-up) are made from edited stills at their final side and never flipped (blueprint §8.5).
15. If a layer is world-made lettering in a flipped era, then add the NORMAL graphic before the whole-shot flip or the MIRRORED graphic after it, never both, because the flip count must be odd.
16. If a turned character appears inside a world-made screen or recording in era B, then pre-reverse the character inside the feed and flip the whole feed once, because B1 §10.2 wants the feed mirrored and the character normal.
17. If the script states a side on a screen ("The left is labelled CONTROL."), then lay out the feed so that side is true after the flip, because the camera shares Iona's view (C2 §7.3).
18. If lettering must read normally inside a flipped shot (B1's exception props, such as the F), then add it after the flip.
19. If a character is added unflipped to a flipped plate, then light them from the flipped plate's light and aim eyelines at flipped positions, because both reversed (C2 rule 36; B2 R20).
19a. If a world-made display draws the position of things that are also in the plate (her outline, the room, the hull), then mirror only its words, each in place, and keep the drawing's geometry true to the plate, because a whole flip puts the drawn room or hull on the wrong side (D12 rule 19).
19b. If a device sits inside Iona's outline when she turns (suit, visor, wrist display, engine), then its mirror state relative to her does not change at that turn, because the script draws the turn "round everything inside her outline. Herself. The suit." (SC26); so visor and wrist text stay backwards in eras B and C (D12 rule 21, §4.3).

**Look**
20. If an added layer is cleaner than the plate, then give that layer alone the plate's measured grain; leave the film-wide grain to D8's single timeline pass (D8-R34) and set `grain_pass: none`; only if a comp is delivered without D8's pass (a test, a one-off), then add one grain pass over the finished frame, because doubled grain shows in flat areas [J].
21. If an element is sharper than the plate, then blur it until a comparable edge matches (typically 0.5-1.5 px at 1080p) [J], because over-sharp edges are the commonest giveaway.
22. If a screen lights a face in the plate, then keep the inserted content's brightness and colour close to that light (B2 R29).
23. If a reflection is added to glass, then keep it at about 4-10% brightness, blacks crushed to zero, far side darker, eyes clear, because glass reflects about 4% per surface square on (B3 §8.1).

**Stop rules**
24. If a comp fails its acceptance test three times, then change method (regenerate, move the fix to the still, or restage), because repair gains halve each round (C5 R13).
25. If bodies touch across a proposed seam (Jude across Eli's arms), then do not split takes there [J].

## 5. The comp stack: order of operations

Build every comp in this order; the comp plan (§8) lists layers in the same order [J].

1. **Plate prep:** pick the kept take; retime to 24 fps if it came at 16 fps (C4 R14); upscale to delivery size if needed.
2. **AI passes on the plate:** object removal, relight, inpainting (regenerating tools).
3. **Clean plates:** freeze or inpaint backgrounds needed for vanishings.
4. **World-flip decision:** if the whole shot is flipped (B1 method 1), add everything that must flip with the world here (world lettering as NORMAL graphics, world screens with their unflipped feed), then flip the whole frame once.
5. **Characters added unflipped** (B1 method 2), relit to the flipped plate.
6. **Elements:** Blender layers, sparks, reflections, mattes for occlusion.
7. **Exact text that must read normally** (exception props, era C world text on an unflipped shot).
8. **Screen-locked layers:** VISOR VIEW HUD.
9. **Matching:** black level, colour, blur per element, and grain on added layers only, to the plate's measured level (Rec9).
10. **No film-wide grain here:** D8 adds one grain to the whole film at timeline level after the grade (D8-R34). Only a comp delivered on its own gets one grain pass over the whole frame (rule 20).
11. **Crop and deliver:** 2.39:1 crop last if used (keep text and HUD out of the top and bottom eighths, B1); one final encode.

**Flip-count check** (the LLM runs it on the comp plan): per layer, its own flips plus the whole-frame flip if added before step 4; odd = `mirrored`, even = `normal`; must equal its `mirror_state` from C2's era table.

## 6. Recipes

Difficulty: **Easy** (a script does it), **Medium** (one manual step or several checks), **Hard** (hands-on tracking or roto, or likely regeneration). Times: novice with an LLM, first / later shots [J].

**Running any recipe, for a non-technical user** [J]:
1. Put the kept take (plate), any content or element files and the shot's comp plan (§8) in one folder named after the shot.
2. Say to the LLM: "Run D6 Rec<N> for <shot ID> from comp plan <comp_id>. Keep every in-between file as PNG or ProRes 4444. When done, export the first, middle and last frames as PNG at full size, plus a 200% crop of the worst edge, and show them to me with the recipe's acceptance test as a checklist."
3. Look at the frames and answer pass or fail for each line of the acceptance test.
4. On a fail, say what you see in plain words ("green line on her thumb", "the screen floats", "the letters are the wrong way round"); the LLM matches it to §10 and re-runs.
5. After three fails on one shot, stop and change method (rule 24).

### Rec1. Screen replacement with tracking and corner pin (C1 Rec9)
**Easy to Medium. 45-90 min / 15-30 min. Script: `screen_insert.py` or one ffmpeg command.**

Catch screens: Saye's monitor (SC12, SC13), the tablet (SC14, SC16), the wrist display (SC18 on), the security playback (SC13).

1. **Content first**, as its own 16:9 clip (C1 Rec9, C3 §13B), overlay text (timestamp, labels) burnt in, then its flip decision (rules 15-17).
2. **Device plate.** Moving device: prompt "the screen is a flat, evenly lit, pure bright green panel, matte, not glowing; nothing covers its corners at the start". Static device: a dark screen is fine.
3. **Static shot:** find the four corners on one frame (the LLM by colour, or the user in any image viewer: hover the mouse over each screen corner and read the x, y pixel position the viewer shows), then run this (tested 2026-09-27 and re-run 2026-09-28 with ffmpeg 7.0.2: four coloured quadrants landed on their named corners; without the 8 px transparent border, ffmpeg's `perspective` smeared the graphic's edge pixels over the whole frame):
   ```
   ffmpeg -i plate.mp4 -loop 1 -i content.png -filter_complex "[1:v]format=rgba,pad=iw+8:ih+8:4:4:color=black@0,scale=1920:1080,perspective=x0=TLx:y0=TLy:x1=TRx:y1=TRy:x2=BLx:y2=BLy:x3=BRx:y3=BRy:sense=destination:eval=init[g];[0:v][g]overlay=0:0:shortest=1,format=yuv420p" out.mp4
   ```
   Corner order: top-left, top-right, **bottom-left, bottom-right** (ffmpeg docs); `scale` = the plate's size.
4. **Moving shot:** `python screen_insert.py plate.mp4 content.mp4 out.mp4 --blur 0.8` (`--flip-content` mirrors the content; `--smooth 3` only for a static or slow screen, rule 14; `--grain 4` only if no D8 grain pass follows, rule 20). It finds the green quad per frame, replaces a corner that jumps more than 6 px from its predicted place (`--jump`), pins the content, keeps fingers in front, removes spill, writes `corners.csv` with a `held` note on repaired frames [V, author test: exact corners on frame 0, finger in front, mirrored timestamp; fact-check re-test 2026-09-27 after the fix: 0 uncovered or dark pixels inside the screen on all 48 frames of the drifting test plate, with a finger crossing two corners; re-run 2026-09-28: same result, 6 frames `held`]. Its output is an `mp4v` viewing file: for the final stack, re-run the pin from `corners.csv` into PNG or ProRes 4444 (ask the LLM), because `mp4v` is lossy [J]. **Corner-order trap:** `corners.csv` lists corners clockwise (top-left, top-right, **bottom-right, bottom-left**), while ffmpeg's `perspective` wants top-left, top-right, **bottom-left, bottom-right**; if the LLM feeds `corners.csv` into ffmpeg, it must swap the last two pairs, or the picture comes out twisted into a bow-tie [V: script source and FFmpeg manual].
5. **Screen look:** blacks lifted slightly, a 3-5% soft highlight from the room's main light (add blend), blur to the plate's softness [J].
6. **Acceptance test:** corners steady at first/middle/last frames; no green fringe at 200%; fingers in front; text in the intended direction; screen no sharper than its bezel.

**Per screen.** SC12 monitor: static, seen THROUGH CLEAR glass (B3), ffmpeg; lay out the feed so "The left is labelled CONTROL." holds after the flip (rule 17); the right dish's label "VALE. CAR. STEERING WHEEL." is the same world lettering. SC13: two screens, the paused security footage ("a camera above the top gate, looking straight down the shaft") and "a second screen beside it" with the dishes still up; the playback is SC06 previs re-rendered from the top-gate camera (C5 E4), 4:3, low-res, 12-15 fps (D8: an even 12), timestamp, whole picture flipped as a pre-turn recording, with no compensation because nobody in it had turned yet (B1 §10.2); static, ffmpeg. Strictly, the recording's tail ("On the screen the upside-down cage falls empty.") shows the cage after it turned, whose red tag would need pre-reversal; at this size and angle nobody can read it, so ignore it [J]. SC14 tablet: W2. SC17 monitor ("On the monitor: stars, slowly turning."): the camera's recording with its corner diagram and the word PASSAGE FLOOR, then Jude and Eli on the ship and Nell behind them, then the file "NELL ROWAN. FLIGHT TEST."; whole picture flipped once (era B world picture, D12 rule 18); Jude and Eli are turned, so pre-reverse them inside the picture before the flip (rule 16), while Nell never turned and needs nothing (Eli in SC20: "Turned, like us. ... Hers it has to go and find."; B1 lists Nell with the mirrored world in phase B). Wrist display ("On Iona's wrist, a simple display: her outline, the engine, a bar of charge." SC18): a small green patch on the glove, `screen_insert.py`; its words mirrored in place in era B and C (rules 19a-19b), while the charge bar's direction is a D12 style decision. SC23 ("Saye's recorded face appears on her wrist."): a recording of the world, so the whole picture flips once. SC25 ("Iona turns the screen towards the figure.") and SC26 ("She turns the wrist screen towards the vessel. Plays the carriage once. Its F reverses."): the carriage recording follows B1's exception-prop decision on the F (open).

If a corner leaves frame or stays covered, track by hand (rule 9): a Blender plane track feeding the Plane Track Deform node ("used to replace flat planes in footage by another image, using plane tracks") [V: manual], or Resolve Fusion's planar tracker.

### Rec2. Text in perspective on a flipped or unflipped plate (C2 R6, A3 R11)
**Easy (static) / Medium (moving). 20-45 min.**

1. The LLM writes the graphic (SVG or Python/Pillow) at 2-4× its on-screen size, in the design file's font; MIRRORED copy by C2 R6's SVG wrapper or `hflip`; check each letter by eye.
2. Choose the row (rule 15, 18):

| Text | Era / plate | Add which file | When | Flip count |
|---|---|---|---|---|
| World lettering in a flipped era, whole shot flipped later | B, method 1 | NORMAL | before the flip | 1 |
| World lettering on a plate already flipped (C2 R5 still) | B | MIRRORED | after | 1 |
| Exception prop meant to read normally | B | NORMAL | after the flip | 0 |
| Unflipped era text | A, and C world | NORMAL | any time | 0 |

3. Pin it (Rec1); blur and grain to the surface.
4. Hold for the longer of B1 R2 (2 s + about 0.5 s per word) and A4 R8 (1 s + characters ÷ 12), doubled for mirrored text (D12 rule 8). Examples: RECEIVING (1 word, 9 characters, normal in SC28) needs max(2.5, 1.75) = 2.5 s; "NELL ROWAN. FLIGHT TEST." (4 words, 24 characters, mirrored in SC17) needs max(4.0, 3.0) × 2 = 8 s.
5. **Acceptance test:** C2's four mirror questions, plus spelling letter by letter against the script.

Catch rows: "Goods only. No persons." (SC01, era A: NORMAL; B4: the red must read, the lettering need not); the SC07 stencil and fire sign (era B, flipped with the plate: C2 W2); OSTREL ("OSTREL, stitched on it in blue. Backwards." soft surface: rule 3); RECEIVING ("On the wall above Saye: RECEIVING." SC28, era C: NORMAL, flip count 0, framed like the turned-meal label per B1).

### Rec3. An unflipped character over a flipped background (B1 method 2, C2 R5, C3 R12)
**Medium on the still, 45-90 min; Hard as video, 2-4 h per shot.**

1. Generate the location (with any world people) in normal orientation; flip it; save `_MIR` (C2 R5).
2. Generate the turned character as designed (not pre-reversed) on plain grey, same lens, height and angle, facing their final direction, lit from the flipped plate's key side (rule 19).
3. **Still route (preferred):** an edit model adds the character to the `_MIR` plate with C2 R5's wording ("Do not mirror her. Keep the background exactly as given, including all lettering. Match the background's light, which comes from image-left."); rings in separate close-ups; animate with minimal motion.
4. **Video route:** matte the character (background removal, which returns a transparent video, or SAM 3 with `apply_mask: false`, §3B); place and scale by the contact line (feet, table edge); soft contact shadow (multiply, 20-40%); plate objects in front cut the character via a SAM 3 matte.
5. If the key side still disagrees, relight the still with IC-Light V2 before animating, or grade it with a soft gradient matte [J].
6. **Acceptance test:** key side as the plate in wide and close-up (B2 R20); eyelines meet; ring and scar sides per C2; no halo.

### Rec4. Blender element layers aligned by `camera_track.json` (C4 Route 5)
**Medium. 1-2 h / 20-40 min per extra shot (previs must exist). Script: `element_layer.py`.**

1. The LLM writes `elements.json`: size (m), start position, drift per second, spin, colour; `carrier_follows_camera: true` when the camera is bolted to the carrier.
2. Run `python element_layer.py camera_track.json elements.json out_dir` (headless bpy). It copies the previs camera per frame, keys the elements, rides a key light with the camera (upper left of the lens, in camera space), renders a transparent background with motion blur and view transform Standard (AgX would shift colours; C4 R25) to RGBA PNGs [V, author test: 40 frames, 640×360, 52 s on CPU; fact-check re-test of the light fix on frame 26 of C4's cage-fall track: bead pixels mean red 148 with a highlight to 193, against 57 before]. To move the key to the cage lamp's side, ask the LLM to change the light's camera-space position in the script.
3. Stack it on `clay.mp4` first (exact by construction), then on the plate; check the beat frames (rule 12).
4. Occlusion: multiply an element passing behind a body by (1 − that body's SAM 3 matte), or keep elements in front of the nearest body [J].
5. Intermediates: `-c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le` kept the alpha [V, author test].
6. Readability: 1-1.5 cm beads were a few pixels at 2.5 m from a 24 mm lens (640 px test); keep readable beads within about 1 m [V, author test; 1 m is J].

Sparks ("Another shot sparks off the grid beside her boot." SC06): a Blender particle burst (1-3 frames, emission shader) or stock spark on black, screen blend, plus a 2-frame +0.3-stop flash on the grid around the hit [J]. The shot through the roof ("Someone KICKS the top gate open and FIRES down through the roof.") is, per D11, a still with "a tiny flicker far above", composited the same way: 1-2 frames of a small warm glow, screen blend, no gun or shooter [J].

Floating screw ("A loose screw rises off the deck beside her boot and hangs in her lamplight." SC26): one `element_layer.py` item with a screw mesh in place of a sphere (ask the LLM), rising 5-10 cm off the deck over about a second and then hanging with a slow spin (keyframed positions rather than one steady drift), lit from her helmet-lamp side; its whole point is that it stays still against her boot ("Nothing moves.") while the drawing on the visor slides, so check it at the first, middle and last frames against a fixed point on the deck [J].

### Rec5. Glass reflections added in comp where B3 R28 says they are physically impossible (SC23)
**Medium. 45-90 min. Director's choice, logged as staging option (c) next to B3's (a) step to the glass and (b) play it CLEAR.**

1. Plate: Iona's side, ANGLED 30-60° to the glass (B3 §8.1: the usual set-up for a REFLECTING shot), Eli beyond the glass, Iona's side lit and Eli's side darker (B3 R28).
2. Reflection source: Iona seen from the glass's position (her front), lit by her helmet and suit lamps.
3. **Flip it**: a reflection is a mirror image, so her ring and suit lettering swap sides.
4. Place over Eli's face; scale as if she stood as far behind the glass as she is in front.
5. Crush its blacks to zero; screen blend at 4-10%; 1-2 px blur [J].
6. **Acceptance test:** Eli's eyes readable; no edge; it moves only when Iona moves; an unprepared viewer calls it "her reflection", not "a double exposure".

### Rec6. Visor HUD: flat, no parallax (B1 VISOR VIEW, B3 §8.1)
**POV: Easy-Medium, 30-60 min. Exterior close-up: Medium-Hard, 1-3 h.**

- **VISOR VIEW (Iona's POV):** screen-locked. The LLM draws the HUD per frame in Python to D12's style guide (same style as the SC18 wrist teaching shot, B4), RGBA PNGs, add blend at 70-90%, 1 px chromatic fringe and slight softness so it sits on glass [J]. No parallax: it moves only with its own animation. Mirror: words mirrored in place, geometry true to the plate (rule 19a). B1 recommended that the visor text snap readable after the final turn as a cue; D12 §4.3 shows the script rules this out (the suit turns with her, rule 19b), and the forward RECEIVING on the SC28 wall becomes the cue instead. This file follows D12; the user confirms (§12).
- **Exterior close-up:** pin the display to the visor with a hand planar track of the rim, not to the frame. From outside it is seen from behind (one more flip), so show only unreadable coloured shapes, off her eyes on decision beats (B3 §8.1) [J].
- **Acceptance test:** eyes clear; no text readable from outside; POV HUD steady to the pixel while the world moves.

### Rec7. Clean appear/vanish hard cuts (C3 Rec6, C1 rule 24)
**Medium. 45-90 min.**

C3 Rec6 cuts hard from clip A (without the thing) to clip B (with it). The usual flaw: B's background differs slightly, so the whole frame jumps.
1. Matte the thing in B (SAM 3 with `apply_mask: false`, §3B; text prompt such as "tall black figure").
2. Background = A's last frame held (static camera), with animated grain (principle 6).
3. Lay B's thing, and any object it touches, over it from the cut on.
4. Vanish: the reverse, cutting to a clean plate made from A's frame.
5. **Acceptance test:** in a difference view across the cut, only the thing changes.

### Rec8. Combining separate takes for multi-person shots (C4 rule 42)
**Locked camera: Medium, 30-60 min. Moving camera: Hard, 2-6 h, often regenerate instead.**

1. **Locked camera, split screen:** both takes from one start frame; seam through static background between the people, feathered 40-80 px at 1080p [J].
2. **Moving camera, matte over:** matte the good person from take B (SAM 3) over take A only if camera paths match within 2 px at three frames; else regenerate with C4 Route 2 depth per body.
3. Never split where bodies touch (rule 25); cut to singles or move the contact into an insert.
4. **Acceptance test:** no doubled or missing limb at the seam; grain continuous.

### Rec9. Matching grain, blur, colour and noise so layers sit together
**Part of every comp. 10-20 min per shot. Measurements scripted, judgment by eye.**

1. **Black level:** element blacks no darker than comparable plate blacks (script-measured).
2. **Colour:** tint the element to a neutral sampled near it; match saturation.
3. **Sharpness:** blur until an element edge matches a similar plate edge (rule 21).
4. **Motion blur:** as the plate (Blender shutter 0.5 = 180°).
5. **Light:** key side and colour from B2; 2-4 px light wrap on bright backgrounds [J].
6. **Grain:** measure the plate's (spread of a flat patch after removing detail), then grain the added layers alone to that level: Python (random noise per frame inside the layer's matte), Blender's Sensor Noise asset (5.0+) or Film Grain asset (5.2 LTS; presets from "8 mm Caffenol" and "8 mm Home Movie" to "70 mm Cinema"; "Animated" makes a new pattern every frame), or ffmpeg `noise=alls=4:allf=t` on the layer (`t` = the pattern changes every frame) [V: manual, docs; value J]. The film-wide grain is D8's (rule 20).
7. **Rate and size:** element and plate match before stacking.
8. **Acceptance test:** at 100% and at speed, the element is not the sharpest, cleanest or most saturated thing in frame unless the story wants it.

## 7. Difficulty, time and automation summary

| Recipe | Difficulty | Novice time, first / later | Fully scriptable? | Hands-on part |
|---|---|---|---|---|
| Rec1 static screen | Easy | 30 / 10 min | Yes (ffmpeg) | Checking three frames |
| Rec1 moving green screen | Easy-Medium | 60 / 20 min | Yes (`screen_insert.py`) | None unless the screen leaves frame or a corner is covered for more than about 12 frames |
| Rec1 dark screen, moving | Medium-Hard | 2 / 1 h | No | Placing track markers |
| Rec2 text, static | Easy | 20 / 10 min | Yes | Letter check |
| Rec2 text, moving | Medium | 45 / 20 min | Yes if on a green or high-contrast card | Letter check |
| Rec3 on the still | Medium | 90 / 45 min | Mostly (edit model) | Judging light and eyeline |
| Rec3 as video | Hard | 4 / 2 h | Partly | Mattes, contact shadow |
| Rec4 Blender elements | Medium | 2 h / 30 min | Yes | Alignment check; tracking if the clip drifted |
| Rec5 reflection | Medium | 90 / 45 min | Mostly | Judging opacity |
| Rec6 POV HUD | Easy-Medium | 60 / 20 min | Yes | Reading-time check |
| Rec6 exterior HUD | Medium-Hard | 3 / 1 h | No | Visor track |
| Rec7 appear/vanish | Medium | 90 / 45 min | Mostly | Difference view |
| Rec8 split screen / matte over | Medium / Hard | 1 h / 2-6 h | Partly | Seam placement |
| Rec9 matching | Easy | 20 / 10 min | Measurements yes | Final look |

All times [J]. Helper cost per 5 s shot (120 frames), from §3B prices: SAM 3 about $0.04, SAM 3.1 $0.08, VEED removal $0.09, Bria eraser $0.70 (its 5 s limit), Wan VACE inpaint (720p) $0.40 for its minimum 81 frames at 16 fps, retimed to 24, or $0.60 if the output matches the plate's 120 frames (frames ÷ 16 × $0.08) [arithmetic from §3B prices].

## 8. The comp plan: fields this subject adds to the breakdown

One `comp_plan` per composited shot, merging C5 `vfx` (now holds the `comp_id`), C4 `composite_layers`, C1 `composite_elements[]` and C2 `insert_graphic` (each becomes a layer). Enums per C5 R29 (lowercase, `"none"` for empty); C2's NORMAL/MIRRORED become `normal`/`mirrored`.

**Blueprint mapping** (`design/blueprint.md` §5.3, FINISH record) [J]: the blueprint files each finishing job as a FINISH record with `operation: composite` and the ID `FX-` + shot + `-` 2 digits (`FX-SC06-SH140-01`), and names takes `TK-` + clip + `-T` 2 digits; it also uses `CP` + 2 digits for chapters. So in the pipeline, `comp_id` = the FINISH record's `FX-` ID, `source_ref` for a take = its `TK-` ID, and the `layers[]` below hang under that FINISH record. The `CP-…-V01` and `GJ-…` IDs in this file's examples are C5-style placeholders; replace them.

| Level | Field | Meaning | Allowed values / example |
|---|---|---|---|
| shot | `vfx` (C5) | Pointer to the comp plan | `CP-SC06-SH140-V01` \| `none` |
| comp job | `comp_id` | Script-issued ID (C5 style) | `CP-` + shot ID + `-V` + 2 digits |
| comp job | `delivery_resolution` | Final pixel size | `[1920, 1080]`; `[1920, 804]` for 2.39:1 |
| comp job | `fps` | Comp frame rate | 24 |
| comp job | `whole_frame_flip` | Whole shot flipped once at stack step 4 | `yes` \| `no` |
| comp job | `layers[]` | Stack from the bottom | objects below |
| layer | `layer_id`, `order` | Name; position (1 = plate) | `L1`, 1 |
| layer | `kind` | What it is | `plate` \| `clean_plate` \| `element_3d` \| `insert_graphic` \| `screen_content` \| `character` \| `reflection` \| `hud` \| `light_fx` |
| layer | `source`, `source_ref` | Where it comes from; job ID or file | `generation_job` \| `previs_render` \| `script_graphic` \| `svg_graphic` \| `still_edit` \| `stock`; `GJ-SC06-SH140-T03` |
| layer | `method` | How it is laid on | `alpha_over` \| `corner_pin_static` \| `corner_pin_tracked` \| `green_screen_pin` \| `screen_locked` \| `add_blend` \| `matte_over` \| `split_screen` |
| layer | `tracking` | How its position is known | `none` \| `static` \| `green_detect` \| `planar_track_manual` \| `camera_track_json` \| `point_track` |
| layer | `matte_source` | Where its matte comes from | `none` \| `render_alpha` \| `green_key` \| `sam_mask` \| `background_removal` \| `roto` |
| layer | `mirror_state` | Required final state (C2 era table) | `normal` \| `mirrored` |
| layer | `added_before_flip` | Added before the whole-frame flip | `yes` \| `no` |
| layer | `own_flips` | Flips applied to this layer alone | 0 \| 1 |
| layer | `text_exact` | Exact letters, as written in the script | "IONA VALE" \| `none` |
| layer | `blend`, `opacity` | Blend mode; 0-1 | `normal` \| `add` \| `screen` \| `multiply`; 0.06 |
| layer | `match_notes` | Blur px, grain, colour, light side | "blur 0.8 px; key frame-left" |
| comp job | `grain_pass` | Whole-frame grain in the comp; `none` whenever D8 adds the film grain (rule 20); layer grain goes in `match_notes` | `none` (default) \| `blender_film_grain` \| `blender_sensor_noise` \| `ffmpeg_noise` \| `python_noise` |
| comp job | `tool` | Main tool | `ffmpeg` \| `python_script` \| `blender` \| `resolve_free_manual` \| `resolve_studio` \| `after_effects` |
| comp job | `difficulty`, `est_hours` | From §7 | `easy` \| `medium` \| `hard`; 1.5 |
| comp job | `qc` | §9 results | list of `{check, result, note}`; result `pass` \| `fail` |
| comp job | `status` | Progress | `planned` \| `in_progress` \| `review` \| `approved` |

**Validator checks to add to C5 §6.6** [J]: (VC1) for every layer, `own_flips` + (1 if `added_before_flip` = yes and `whole_frame_flip` = yes, else 0) is odd exactly when `mirror_state` = `mirrored`; (VC2) every `insert_graphic` layer has `text_exact` matching a quoted script line; (VC3) every `element_3d` layer points to a previs job with `camera_track.json`; (VC4) `add` or `screen` blend for every `reflection`, `light_fx` and `hud` layer; (VC5) no AI-pass layer above an `insert_graphic` layer; (VC6) text layers inside the 2.39 safe band when the film is cropped; (VC7) `grain_pass` is `none` whenever D8's film field `finish.grain.method` is not `none`, so grain is never doubled. (VC8) when `whole_frame_flip` = `yes`, the shot's D8 `finish.flip` is `no` for the comp's output, because the flip already happened inside the comp and a second flip in the conform would undo it [J; added 2026-09-28].

## 9. QC checklist (every comp, at 100% and at playback speed)

- **Edges:** no halo; no green on hair, fingers or glove edges; matte edges do not boil.
- **Key side** (B2 R20): added layers lit from the plate's key side, wide and close-up alike.
- **Flipped text** (C2 mirror questions): world letters reversed in the right eras; turned items normal; rings, scars, smiles on designed sides; flip-count check (§5) passes; spelling letter by letter.
- **Temporal flicker:** AI mattes steady; corners not swimming; grain animated; timestamps tick once a second.
- **Reflections** (B3 §8.1): never across a face in an ALONG shot; eyes readable in REFLECTING shots; reflections only brighten.
- **Tracking:** elements stick to their surface at first, middle, last frames and at the fastest camera move.
- **Match:** blacks, saturation, sharpness, motion blur and grain as the plate (Rec9); no film-wide grain in the comp when D8 adds it (VC7).
- **Occlusion:** things in front stay in front (fingers over screens, bodies over beads).
- **Frame rate:** no stretched motion from mixing 16 fps and 24 fps sources.
- **Crop:** text, HUD and key props out of the top and bottom eighths for 2.39:1.

## 10. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| The whole frame turns the graphic's colour | ffmpeg `perspective` extends edge pixels | Pad with an 8 px transparent border first [V, author test] |
| "No such filter: drawtext" | ffmpeg build without the font library | Draw text with Python/Pillow into PNGs [V, author test] |
| Green fringe on fingers or screen edge | Spill from the green screen | Despill (`screen_insert.py` does it), shrink the matte 1 px |
| Green light on a face in the plate | The green screen was generated glowing | Prompt "matte green panel, not glowing"; else use a dark screen and Rec1's hand route |
| Screen trembles | Corner detection noise | Static or slow screen: average corners (`--smooth 3` to `5`); raise screen contrast |
| Dark sliver along one or two edges of a moving screen | Corner averaging makes the picture lag the screen | `--smooth 1` (the default since the fix) [V, fact-check re-test] |
| One corner jumps for a few frames | A finger or prop covers it | `--jump 6` (default) replaces it; if `held` runs past about 12 frames, track by hand [V, fact-check re-test; 12 J] |
| Blender elements come out dark or flat | Key light too far away (the first `element_layer.py` placed it about 4 m behind the camera) | Use the fixed script; move the light in camera space [V, fact-check re-test] |
| "Film Grain" or "String to Image" not found in a script | bpy older than 5.2 | Install Blender 5.2 LTS, or use ffmpeg or Python [V, fact-check test on bpy 5.0.1] |
| Beads drift against the actors | Generated camera differs from previs | Rule 12: track two fixed points, move the layer |
| Bead in front of a body it should pass behind | 2D stack has no depth | Rule 4 matte with SAM 3; or keep beads in front |
| Colours of the Blender layer look washed out | View transform AgX or Filmic | Standard for layers (C4 R25) |
| Dark rims around elements | Premultiplied alpha read as straight | ffmpeg `overlay=...:alpha=premultiplied` for premultiplied sources [V: docs] |
| Reflection looks like a double exposure | Normal blend, grey blacks, too strong | Screen blend, blacks to zero, 4-10% |
| Matte flickers on hair | Segmentation per frame | Background-removal service with edge refinement, or MatAnyone (non-commercial) |
| Banding after grain | 8-bit intermediates | Work in 16-bit PNG or ProRes 4444; grain last |

## 11. Worked examples

### W1. *The Catch* SC06-SH140: the blood beads (C5 E3, C4 Example A)

Script: "Jude's blood lifts off the steel in round red beads and hangs in the air between them, turning."

- **Plate:** generated **without** blood (C1 Ex2; C4 rule 45) by C4 Route 2 or 3 from `plan_cage_fall.json`; camera parented to the cage, 24 mm; 4 s + 1 s handles (C5 E3).
- **Beads:** `element_layer.py`, `carrier_follows_camera: true`, 20-30 beads (C1 Ex2), radius 0.5-1.5 cm, squashed 10% so the turning reads, drift 5-15 cm/s, spin 40-80°/s, dark red with a sharp highlight, key from the cage lamp side (B2) [V, author test with 3 beads on the kit's cage-fall camera; values J]; readable beads within about 1 m of the lens, between Iona (frame left) and Jude and Eli (frame right).
- **Checks:** frames 12, 26, 40: two grid corners in plate versus clay (rule 12); beads behind Jude cut by his SAM 3 matte; beads carried into every later shot until the cage stops (C5 E3).
- **Comp plan (abridged):**
```json
{"comp_id": "CP-SC06-SH140-V01", "delivery_resolution": [1920, 1080], "fps": 24, "whole_frame_flip": "no",
 "layers": [
  {"layer_id": "L1", "order": 1, "kind": "plate", "source": "generation_job", "source_ref": "GJ-SC06-SH140-T03",
   "method": "alpha_over", "tracking": "none", "matte_source": "none", "mirror_state": "normal",
   "added_before_flip": "no", "own_flips": 0, "text_exact": "none", "blend": "normal", "opacity": 1.0, "match_notes": "none"},
  {"layer_id": "L2", "order": 2, "kind": "element_3d", "source": "previs_render", "source_ref": "PV-SC06-SH140-V01",
   "method": "alpha_over", "tracking": "camera_track_json", "matte_source": "render_alpha", "mirror_state": "normal",
   "added_before_flip": "no", "own_flips": 0, "text_exact": "none", "blend": "normal", "opacity": 1.0,
   "match_notes": "blur 0.6 px; grain to plate level; key from cage lamp side; cut by Jude's sam_mask where behind"}],
 "grain_pass": "none", "tool": "blender", "difficulty": "medium", "est_hours": 3.0, "qc": [], "status": "planned"}
```

### W2. *The Catch* SC15: the tablet feed (B1 §10.4-10.5; C3 14-05A/B)

Script: "A small CLICK, from nowhere." / "The cup slides a hand's width across the table. Into his reach." / "It did not come through the door. It is simply there, in the space between one moment and the next." / "The bed, and Jude, and the cup, and the figure are gone." / "The chair is still there."

- **The feed is its own master clip** (B1: high corner, wide, static, desaturated, small overlay, mirrored):
  1. **Plate A:** a checked still of Jude's room, Jude **pre-reversed** (his wounded arm and its dressing on the other side, so "his good hand" is too), since the feed is flipped once and he is turned (rule 16); animate only his small movements, or use the still with grain (principle 6).
  2. **Cup slide:** SAM 3 matte of the cup, clean plate under it, the cut-out moved a hand's width over 12-18 frames with ease-out and its shadow [J]. No generation.
  3. **Figure:** clip B with the figure (C3 Rec6); Rec7 lays only the figure over the held room, frame to frame, no fade.
  4. **Gone:** clean plate without bed, Jude, cup and figure; chair untouched; hard cut.
  5. **Overlay:** timestamp and camera label drawn by Python, ticking once a second, burnt in **before** the flip, so it reads backwards (era B world-made text; B1's recommendation).
  6. **CCTV look:** desaturate, down to 640×360 and back, slight barrel (`lenscorrection`), 12-15 fps by held frames (B1), then **one flip of the whole feed**.
- **Into the tablet** (SC14, SC16): B1 cuts to the feed full screen, so most shots need no pin; the establishing tablet uses Rec1. Iona's room is itself mirrored in era B: insert the unflipped feed before the room's flip, or the flipped feed after it. "Iona runs the picture back." is the feed reversed; the burnt-in timestamp runs backwards with it, as a real recording's would.
- **Flip count:** room 1 (mirrored); Jude 1 plus pre-reversal (reads normal); overlay 1 (backwards).

### W3. *The Catch* SC10: the kitchen flip-and-add (C2 W3, B3 Ex1)

Script: "They stand facing each other across the table like a woman and her reflection, each with the wrong hand in the air." / "Saye's wedding ring. On her right hand." / "Iona looks down at her own ring, on her own left hand."

- **Plate:** kitchen with Saye, generated normal with her ring on her **left** hand, standing frame-left facing right, lamp on the table centre (B3 Ex1); flip → Saye frame-right facing left, ring reads on her right (C1 Ex3) [flip count 1].
- **Added unflipped** (Rec3 still route): Iona frame-left facing right (ring on her own left, no pre-reversal), Jude on the table, Eli at the fridge in the centre. B3 Ex1's camera: 85 mm from about 6.3 m, 1.45 m high.
- **Light:** the lamp stands on the table between the women (a staging addition B3 logs: the script says "Iona holds the lamp", so she sets it down before the raised hands), so after the flip Iona is lit from image-right, low, like Saye's mirror image (rule 19).
- **Rings:** in separate close-up inserts (C2 W3), each hand its own plate: Saye's from the flipped plate, Iona's unflipped.
- **Check:** both women raise "the hand nearest the camera" (C2 W3) at the same height; eyelines meet; the flip-count check shows Saye and kitchen 1, Iona, Jude and Eli 0.

### W4. *The Catch* SC21: the copied name label (B4 M11)

Script: "Above it, a label. Her name, copied from a hospital wristband stroke for stroke, the way you would copy a drawing. By someone who did not know they were letters." / "IONA VALE."

- **Graphic:** drawn, not printed (B4): the wristband's printed letterforms traced as even, slow, single-weight lines with slight wobble, dark on a pale card.
- **Mirror state:** B1 assumes the copy reads backwards to Iona like the wristband ("Her own name, printed backwards." SC11). C2 §7.4 reasons that a faithful copy of a backwards wristband reads backwards in era B and, since the container later turns with her, strictly still backwards in era C, while the script prints it normally; both ask the user to decide. On that assumption the screen shows, left to right: mirrored E, mirrored L, A, V, space, A, mirrored N, O, I (Ǝ⅃AV AИOI). Make it by flipping the NORMAL drawing, never by typing look-alike characters.
- **Tell-tale letters:** only E, L and N change shape; in symmetric lettering A, V, O and I look the same, so keep E, L and N distinctive [J].
- **Placement:** a flat card on the shelf edge above the container, so a static pin fits; if attached to the curved container, render it in Blender instead (rules 3-4). SC30 ("The label still carries the marks copied from Iona's wristband.") reuses the file.
- **Emphasis:** the motif's only L3 (B4); reading time doubled for mirrored text (B1 R2).

### W5. *The Catch* SC26: the red outline inside rock (B4 M01; B1 VISOR VIEW)

Script: "On the visor, the drawing of the room slides upwards. Goes on sliding." / "Her projected outline turns red: far below the receiving room. Below the loading tunnel. Inside solid rock. Still travelling down."

- **Layers:** L1 plate (the ledge, the deck and the rail beyond the hatch; nothing in it moves: "Nothing moves."); L2 the loose screw hanging in her lamplight, only if this shot includes the deck by her boot (Rec4; [J]); L3 HUD, screen-locked (Rec6 POV).
- **HUD drawing** (Python per frame, D12's style, SC18 wrist style): a wire-frame room labelled RECEIVING (the script's own "VISOR VIEW: a wire-frame room marked RECEIVING hangs beyond the ledge."), a line for the loading tunnel, rock hatching below, and her outline, turning red inside the hatching. Room, tunnel and rock slide upwards together; her outline stays fixed on the glass. The same HUD later draws "TURN, below. CROSS AT 0, beside RECEIVING." and the reserve bar (D12's worked example).
- **Readability:** B4 asks for L2 "where the audience must read where the outline sits (the red outline inside rock)": red outline, rock the largest hatched area, RECEIVING the only word.
- **Mirror state:** era B world-made display. Mirror the word RECEIVING in place and keep the drawing's geometry as it is (rule 19a); never flip the whole HUD layer, which would swap the room's side. It stays backwards after the SC27 turn, because the suit turns with her (rule 19b; D12 §4.3); the first forward RECEIVING is the SC28 wall. Use rock hatching at 90° or a stipple, not 45°, which a mirror reverses (D12 rule 20).
- **Blend:** add, about 80%; 1 px fringe; out of the 2.39 top and bottom eighths.

### W6. *The Long Places*, Chapter VI "Server Lag": the livestream and the pool

Text: "gülce, small letters, a yellow flower where a face would go, who came on after two and stayed to the end and typed, some nights, one line. *the wicks are good tonight.*"

- **Livestream:** the stream picture (niches, flames) is the plate; chat line and viewer name are a Python-drawn insert graphic, screen-locked full frame, pinned by Rec1 on the phone in his hand; a font with "ü", lower case as written [J].

Text: "the standing water had held two lamps, doubled; his own shape, doubled, coming with the light; and at the pool's far edge, in nine or ten frames, a figure's worth of dark, upright, with a lamp's rim along its shoulder, which stood still while everything else in the water moved."

- **Comp:** plate = the pool reflecting two lamps and Yusuf's approaching shape; a ripple (Blender Displace node, animated noise) moves the whole reflection; the dark upright shape is laid **after** the ripple, so it alone stays still, for 10 frames (the text says "nine or ten"; pick one and keep it); faceless, a thin lamp-coloured rim on one shoulder (screen blend) [J].
- **Why comp:** the prose keeps the evidence ambiguous; a generated clip would omit the figure or show too much, while a layer controls the ten frames exactly [J].
- **How it is seen:** the file died ("the reflection was not footage anymore. It was a memory of footage"), so the comp is shown as he scrubbed it at lunch, on the phone screen, frame by frame (Rec1 static pin on the phone), not as a clean full-frame clip; D2 decides whether it is shown at all [J].

## 12. For the writer/user; conflicts; unverified

**Decisions needed**
- Era B world-made screen text (monitor labels, feed overlays, wrist, visor): keep backwards (B1's recommendation, used here) or legible?
- Visor and wrist text after the SC27 turn: stays backwards (D12 §4.3, used here, because the suit turns with her) or snaps readable (B1's original cue, which needs an on-screen reason)?
- The copied "IONA VALE": backwards in SC21 and SC30 (assumed here) or normal?
- SC23: comp reflection (option c) versus B3's (a) added step or (b) CLEAR.
- The SC12 feed layout so "The left is labelled CONTROL." holds after the flip (rule 17).
- Which wrist carries the display; whether to buy Resolve Studio (only if someone will edit in Resolve).

**Conflicts with other files**
- B3 R28 rules the SC23 reflection impossible from Iona's mark; this file adds a cheat B3 does not list.
- C3 lets a model draw short signs; C2 and this file composite exact text, except on soft surfaces (OSTREL), where this file generates and fixes on the still.
- C4's `camera_track.json` aligns layers with the previs, not automatically with the generated clip (rule 12).
- **Grain (D8-R34):** D8 adds one grain for the whole film at timeline level after the grade; this file's first version added a grain pass in every comp. Resolved here: comps grain only their added layers; `grain_pass: none` by default (rule 20, VC7).
- **Visor snap (B1 §16 vs D12 §4.3):** B1 recommends the visor text snap readable after her final turn; D12 shows the suit turns with her, so it stays backwards. This file now follows D12 (W5, rule 19b); B1 is not yet updated.
- **Whole flip vs in-place flip of HUDs (D12 rule 19):** this file's first W5 flipped the whole HUD layer; corrected to in-place words, true geometry.
- **Bead count:** C1 Ex2 says 20-30 simulated beads; C4 Example A animates three; this file's test used three and recommends 20-30 for the finished shot, readable ones within about 1 m.
- **Blueprint tool route:** the blueprint (§8.7) sends "tracked or keyed work" to Resolve free with a guide; this file sends moving green screens to `screen_insert.py` and 3D elements to Blender, keeping Resolve free for hand planar tracks only (rule 9), because the scripts need no clicks. Its rule that text is drawn "in its derived orientation and composited after any flip" is Rec2's second row, and fits every case except a world screen showing a pre-reversed turned character (rule 16), where the feed is built unflipped and flipped whole.
- **Resolve scripting:** this file said free 21.1 had no scripting; D8 (and Digital Production) say console scripting remains in free. Both agree an LLM cannot drive free Resolve directly. Puget reads the change as removing scripting from free altogether; Digital Production quotes the console exception. Treat free Resolve as manual-only.
- **Corner-pin tool (C1 P9/Rec9):** C1 suggests corner-pinning in DaVinci Resolve; this file uses ffmpeg (static) and `screen_insert.py` (moving), keeping Resolve for hand tracks (rule 9), because the scripts need no clicks.
- **Mirror route (blueprint §8.5 vs this file's first version):** the blueprint adds a "direct" route (row 3: prompt the final picture when every mirrored element is seen in only one orientation) and a 0.10-of-frame-height face threshold for the plate route; rule 14b now follows the blueprint.
- **D5 `post_chain` order:** D5 lists `cadence, upscale, flip, composite, grade, grain, halation, weave`, a flip before the composite. For shots where world lettering or a world screen is added *before* the whole-frame flip (§5 step 4; Rec2 row 1; W2), the flip happens inside the comp, not before it; for those shots the comp plan's `whole_frame_flip: yes` replaces D5's separate `flip` step. Otherwise the two agree.
- **D8 `finish.flip` vs `whole_frame_flip`:** D8 stores the shot's mirror operation as `finish.flip` (`yes` | `no`, derived from C1 `mirror_flip`); this file flips inside the comp when layers must go on before the flip. Both fields describe the same single flip; VC8 stops it happening twice.
- **D3 rule 23 "a composited face, D6":** D3 sends mouths behind a visor to "a composited face" in this file; there is no dedicated recipe. Nearest route: Rec6's exterior visor track to pin a separately lip-synced face clip inside the visor, then Rec9 matching and a Rec5-style faint reflection over it; Hard, 2-4 h per shot [J]. Prefer D3's cheaper options (from behind, in profile, over the visor display). The SC23 recorded Saye on the wrist (D3: "her face is a separate lip-synced clip composited on the display") is an ordinary Rec1 screen insert.
- **D13 plate counting:** D13 R20 adds "one plate each for `text` and `screen`", each costing one final generation take plus a comp job (40 min until this file's `est_hours` exist). Text graphics are drawn by script, not generated, so a text layer needs no generation take; a screen needs one only if its content is generated video. Use §7 times for the comp job.

**Unverified or judgment**
- External scripting Studio-only "since 19.1"; Bria background-removal price; Aleph 2.0 price, API and removal by prompt; Beeble API; After Effects features; MCP servers' reliability; what fal's SAM 3 video returns with `apply_mask: false` (expected: a black-and-white matte; untested); whether Blender's Essentials assets load cleanly from a headless script (not tested). Times, blur and opacity values are [J]. No *Catch* shot was composited end to end; the kit was tested on a synthetic plate and C4's clay render; the static ffmpeg pin was re-run on 2026-09-28 (ffmpeg 7.0.2) with the corner order confirmed; `element_layer.py` was re-run on 2026-09-28 (bpy 5.0.1, C4's cage-fall previs rebuilt from `plan_cage_fall.json`): 40 RGBA frames in 56 s on CPU, frame 26 bead pixels mean red 148, highest 193, as in the first fact-check.

## 13. Sources (all checked 2026-09-27; re-checked 2026-09-28 unless noted)

1. Blackmagic Design, Resolve Fusion page. https://www.blackmagicdesign.com/products/davinciresolve/fusion
2. CG Channel, "Blackmagic Design releases DaVinci Resolve 21.0" (4 June 2026). https://www.cgchannel.com/2026/06/blackmagic-design-releases-davinci-resolve-21-0/
3. Puget Systems, "How DaVinci Resolve Free v21.1 Scripting Changes Affect Puget Bench" (10 Sept 2026; quotes Blackmagic). https://www.pugetsystems.com/blog/2026/09/10/how-davinci-resolve-free-v21-1-scripting-changes-affect-puget-bench/
4. Secondary [U]: https://davinciresolveclub.com/davinci-resolve-21-ai-tools/ ; https://xere.my/journal/davinci-resolve-21-1-free-python-scripting-removed-lua-benchmark/
5. samuelgursky/davinci-resolve-mcp (MIT; free edition via in-app bridge). https://github.com/samuelgursky/davinci-resolve-mcp
6. Adobe, After Effects plans (US$22.99/mo annual, billed monthly). https://www.adobe.com/products/aftereffects/plans.html
7. After Effects MCP servers (examples). https://github.com/TheLlamainator/after-effects-mcp ; https://github.com/ishu86/after-effects-mcp
8. Foundry Learn, "About Nuke Non-commercial" (Nuke 17.1). https://learn.foundry.com/nuke/content/getting_started/meet_nuke/about_nc.html ; Foundry product page. https://www.foundry.com/products/nuke-family/non-commercial
9. Blender 5.2 LTS Manual: node list https://docs.blender.org/manual/en/latest/compositing/types/index.html ; Corner Pin https://docs.blender.org/manual/en/latest/compositing/types/transform/corner_pin.html ; Plane Track Deform https://docs.blender.org/manual/en/5.2/compositing/types/tracking/plane_track_deform.html ; Keying https://docs.blender.org/manual/en/latest/compositing/types/keying/keying.html ; Film Grain https://docs.blender.org/manual/en/latest/compositing/types/camera_lens_effects/film_grain.html ; Sensor Noise https://docs.blender.org/manual/en/latest/compositing/types/camera_lens_effects/sensor_noise.html ; String to Image https://docs.blender.org/manual/en/latest/compositing/types/input/string_to_image.html ; Inpaint https://docs.blender.org/manual/en/latest/compositing/types/filter/inpaint.html ; Cryptomatte https://docs.blender.org/manual/en/latest/compositing/types/mask/cryptomatte.html
10. FFmpeg Filters Documentation. https://ffmpeg.org/ffmpeg-filters.html
11. Meta AI, "SAM 3.1" (27 March 2026). https://ai.meta.com/blog/segment-anything-model-3/ ; facebookresearch/sam3 repo and LICENSE (SAM License, 19 Nov 2025). https://github.com/facebookresearch/sam3 ; SAM 2 LICENSE (Apache 2.0). https://github.com/facebookresearch/sam2
12. fal: SAM 3 video https://fal.ai/models/fal-ai/sam-3/video ; SAM 3.1 video https://fal.ai/models/fal-ai/sam-3-1/video ; VEED background removal https://fal.ai/models/veed/video-background-removal ; Bria background removal API https://fal.ai/models/bria/video/background-removal/api ; Bria Video Eraser guide https://fal.ai/learn/devs/bria-video-eraser-prompt-guide ; Wan VACE 14B inpainting https://fal.ai/models/fal-ai/wan-vace-14b/inpainting ; IC-Light V2 https://fal.ai/models/fal-ai/iclight-v2
13. Runway, Aleph 2.0 product page. https://runway.com/product/aleph-2
14. Beeble, cloud pricing. https://beeble.ai/pricing-cloud
15. Licences: MatAnyone 2 (NTU S-Lab 1.0) https://github.com/pq-yang/MatAnyone2 ; ProPainter (S-Lab 1.0) https://github.com/sczhou/ProPainter ; IC-Light (Apache 2.0) https://github.com/lllyasviel/IC-Light ; CoTracker (CC BY-NC 4.0) https://github.com/facebookresearch/co-tracker
16. Author tests, 2026-09-27: ffmpeg 7.0.2 static build (corner pin, border fix, missing `drawtext`, ProRes 4444 alpha); `screen_insert.py` on a synthetic plate; `element_layer.py` on bpy 5.0.1 with C4's cage-fall `camera_track.json`. Fact-check re-tests the same day: both scripts before and after their fixes (OpenCV 4.10, NumPy 1.26, bpy 5.0.1), and a list of bpy 5.0.1's compositor node types. Files in `research/D6_comp_kit/`.
17. Library files C1-C5, B1-B4, A3, D5, D8, D11, D12, D13 (digests in `research/digests/`) and `design/blueprint.md` §5.3, §8.5, §8.7; *The Catch* (workshop revision, 25 Sept 2026); *The Long Places* (revised final).
18. Blackmagic Design, DaVinci Resolve Studio page (free: "up to 60 fps in resolutions as high as Ultra HD 3840 x 2160"; Studio-only Magic Mask, film grain, "Python and LUA scripting"). https://www.blackmagicdesign.com/products/davinciresolve/studio
19. Digital Production, "Resolve 21.1 adds MCP and finally gets presets" (8 Sept 2026). https://digitalproduction.com/2026/09/08/resolve-21-1-adds-mcp-and-finally-gets-presets/ ; CineD on 21.1 (9 Sept 2026). https://www.cined.com/davinci-resolve-21-1-released-ai-assistant-integration-via-mcp-individual-hdr-trims-and-python-scripting-moves-to-studio/
20. Blender release notes, compositor: 5.0 (built-in assets incl. Sensor Noise) https://developer.blender.org/docs/release_notes/5.0/compositor/ ; 5.2 LTS (String To Image node, Film Grain asset) https://developer.blender.org/docs/release_notes/5.2/compositor/
21. Foundry, Nuke Non-commercial product page. https://www.foundry.com/products/nuke-family/non-commercial
22. fal API schemas (inputs `apply_mask`, `max_num_objects`, `video_output_type`, `num_frames`, `frames_per_second`, `match_input_*`), checked 2026-09-28: https://fal.ai/models/fal-ai/sam-3/video/api ; https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=fal-ai/sam-3-1/video ; https://fal.ai/models/fal-ai/wan-vace-14b/inpainting/api
23. Re-tests 2026-09-28: static ffmpeg pin with four coloured quadrants and without the pad (ffmpeg 7.0.2 from imageio-ffmpeg; no `drawtext` in this build either); `screen_insert.py` on `make_test_plate.py`'s plate; `element_layer.py` on bpy 5.0.1 with a cage-fall `camera_track.json` rebuilt by C4's `previs_from_plan.py`.
