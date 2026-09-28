# Digest D6: Compositing and VFX execution (28 Sept 2026)

Source: `research/D6_compositing_vfx.md` (fact-checked 27 Sept, re-checked 28 Sept 2026). Brackets: **R#** = rule in §4, **P#** = principle in §2, **Rec#** = recipe in §6, **W#** = worked example in §11, **VC#** = validator check in §8. **[V]** primary page read or script run 27-28 Sept; **[U]** unverified; **[J]** judgment. Prices change monthly: re-check before paying. Kit `research/D6_comp_kit/`, all scripts re-run 28 Sept.

## 1. Scope

1. Does the jobs other files send to "composite": screens, exact text, flipped worlds, floating beads, sparks, reflections, visor graphics, appear/vanish cuts, multi-take shots, and matching.
2. Picks tools an LLM can run for a non-technical user (ffmpeg, Python, headless Blender, fal-hosted helpers), Resolve free as manual fallback; nine recipes with times and acceptance tests.
3. Adds one `comp_plan` per composited shot (merging C5 `vfx`, C4 `composite_layers`, C1 `composite_elements`, C2 `insert_graphic`), 8 validator checks and a QC list, worked on *The Catch* and *The Long Places*.

**Terms** [§1]: *plate* = background clip; *element* = one added thing; *layer* = one picture stream, plate = 1; *matte* = black-and-white picture saying where a layer shows; *key* = matte from a colour; *despill* = removing green tint; *roto* = hand-drawn matte; *planar track* = four moving corners of a flat surface; *corner pin* = warping a flat picture onto four points; *insert graphic* = exact text or screen image made outside AI; *flip count* = times a layer is mirrored before the final frame; *screen-locked* = fixed to the frame; *intermediate* = file between steps (PNG or ProRes 4444); *difference view* = frame minus frame, changes light up; *era A/B/C* = *The Catch*'s mirror periods (A nothing mirrored; B world mirrored, turned people normal; C world normal, Jude, Eli and their meals mirrored); *pre-reverse* = mirror on purpose so a later whole flip makes it right.

## 2. Rules

**Principles**
1. [P1, R1] If a thing must be exact (text, screen image, HUD drawing, anything backwards), then make it as an insert graphic and composite it, because models misspell and cannot mirror (C1 R6-R7, C2 rules 31-32).
2. [P2, R6] If an AI pass (removal, relight, inpaint, upscale) is needed, then run it on the plate before any exact layer, because it redraws what it touches.
3. [P3] If a layer must end `mirrored`, then its flip count must be odd (`normal`: even), because most mirror errors are one flip too many or too few.
4. [P4, P5] If an element disagrees with the plate (light, grain, blur, blacks, rate, size) or a clip drifted from the previs, then change the element, never the plate.
5. [P6] If a shot is locked off (CCTV, tablet feed, insert), then a checked still with animated grain may be the plate (C1 rule 24).
6. [P8] If a plate needs upscaling, then upscale before exact layers go on, because upscalers redraw text (D8-R24).

**Where the work happens**
7. [R2] If the fix is possible on the keyframe still (a label, people on a mirrored plate, a ring), then do it there and animate minimally, because a still comp takes minutes, a video comp hours [J].
8. [R3] If text sits on a soft or curved surface (OSTREL blanket), then fix it on the still, because corner pins fit only flat, rigid surfaces [J].
9. [R4] If the element moves in 3D relative to the camera (beads, sparks, screw), then render it in Blender through `camera_track.json` (C4 Route 5), because 2D cannot change perspective.
10. [R5] If the element is light (sparks, glow, reflection, HUD), then use add or screen blend, because light only adds.

**Tools**
11. [R7, R8] If the shot is locked off, then ffmpeg fixed pin (§4 P1); if a screen moves, then generate it pure green and run `screen_insert.py`, because corners are found automatically and fingers stay in front [V].
12. [R9] If the screen cannot be green, then generate it dark and track corners by hand (Blender Plane Track Deform or Resolve Fusion planar tracker) [J].
13. [R10] If a program needs clicks, then the LLM writes numbered steps with menu names and the user sends a screenshot after each [J].
14. [R11] If the project is commercial, then avoid MatAnyone 2, ProPainter, CoTracker and Nuke Non-commercial, because their licences forbid it [V].
15. [§3B] If a SAM 3/3.1 matte is ordered from fal, then set `apply_mask: false` and check one clip is pure black and white, because the default draws the mask onto the picture [V; `false` output U].

**Tracking**
16. [R12] If the clip's camera differs from the previs by more than about 1% of frame width at a beat (two fixed points), then track and shift the element layer [J].
17. [R13] If the camera is bolted to a carrier (the cage), then set `carrier_follows_camera: true`, because elements float in carrier space [V].
18. [R14] If corners jitter over 2 px on a static or slow screen, then `--smooth 3`; if the screen moves, then never average, because the picture lags and leaves a dark sliver [V].
19. [R14a] If a finger crosses a corner, then `--jump 6` holds it at its prediction; if over about 12 frames in a row are `held`, then track by hand, because a prediction drifts [V; 12 J].
20. [Rec1] If `corners.csv` feeds ffmpeg, then swap the last two corners, because the CSV is TL, TR, BR, BL and ffmpeg wants TL, TR, BL, BR [V].

**Mirror world**
21. [R14b] If a shot is in a flipped era, then pick its route in the blueprint's order (§8.5), first match after row 1: (1) readable text → always a text graphic in its derived orientation, composited after any flip; (2) plot-sided detail (ring, raised hand, palm, scar) or a differing face ≥0.10 of frame height → plate route (Rec3); (3) every mirrored element seen in one orientation only in the film → prompt the final picture, no flip; (4) small differing characters → flip their references, generate, flip the clip (B1 method 1); (5) only the location mirrored → generate, flip; (6) nothing mirrored → nothing. Because cheap routes are safe only when no sided detail can land wrong. Never prompt "the world mirrored".
22. [R15] If world lettering is in a flipped era, then add NORMAL before the whole-shot flip or MIRRORED after, never both.
23. [R16] If a turned character appears inside a world screen or recording in era B, then pre-reverse them inside the feed and flip the feed once (B1 §10.2).
24. [R17] If the script states a side on a screen ("The left is labelled CONTROL."), then lay out the feed so it is true after the flip (C2 §7.3).
25. [R18] If lettering must read normally in a flipped shot (exception props, the F), then add it after the flip.
26. [R19] If a character is added unflipped to a flipped plate, then light from the flipped plate's key and aim eyelines at flipped positions (C2 rule 36, B2 R20).
27. [R19a] If a world display draws things also in the plate (outline, room, hull), then mirror only its words in place and keep geometry true, because a whole flip moves the drawn room (D12 rule 19).
28. [R19b] If a device sits inside Iona's outline at a turn (suit, visor, wrist, engine), then its mirror state relative to her does not change, because the turn is drawn "round everything inside her outline. Herself. The suit." (SC26); visor and wrist words stay backwards in B and C (D12 rule 21).

**Look and stop**
29. [R20, P9] If an added layer is cleaner than the plate, then grain that layer alone to the plate's level and set `grain_pass: none`; only a comp delivered without D8's timeline grain gets one whole-frame pass, because doubled grain shows (D8-R34).
30. [R21] If an element is sharper than the plate, then blur until a comparable edge matches (0.5-1.5 px at 1080p) [J].
31. [R22] If a screen lights a face, then keep inserted content close to that light (B2 R29).
32. [R23] If a reflection is added to glass, then 4-10% brightness, blacks zero, far side darker, eyes clear (B3 §8.1).
33. [R24] If a comp fails its acceptance test three times, then change method, because repair gains halve each round (C5 R13).
34. [R25] If bodies touch across a proposed seam, then do not split takes there [J].

## 3. Breakdown fields

One `comp_plan` per composited shot; enums lowercase, `"none"` for empty (C5 R29). In the blueprint it is a FINISH record (`operation: composite`): `comp_id` = its `FX-` ID (`FX-SC06-SH140-01`), a take's `source_ref` = its `TK-` ID; `CP-`/`GJ-` IDs below are placeholders.

| Level | Field | Meaning | Allowed values / example |
|---|---|---|---|
| shot | `vfx` (C5) | Pointer to the comp plan | `CP-SC06-SH140-V01` \| `none` |
| comp job | `comp_id` | Script-issued ID | `CP-` + shot + `-V` + 2 digits (pipeline: `FX-` ID) |
| comp job | `delivery_resolution` | Final pixel size | `[1920, 1080]`; `[1920, 804]` for 2.39:1 |
| comp job | `fps` | Comp rate | 24 |
| comp job | `whole_frame_flip` | Whole shot flipped once at stack step 4 | `yes` \| `no` |
| comp job | `layers[]` | Stack from the bottom | objects below |
| layer | `layer_id`, `order` | Name; position | `L1`, 1 |
| layer | `kind` | What it is | `plate` \| `clean_plate` \| `element_3d` \| `insert_graphic` \| `screen_content` \| `character` \| `reflection` \| `hud` \| `light_fx` |
| layer | `source`, `source_ref` | Origin; job ID or file | `generation_job` \| `previs_render` \| `script_graphic` \| `svg_graphic` \| `still_edit` \| `stock`; `GJ-SC06-SH140-T03` |
| layer | `method` | How laid on | `alpha_over` \| `corner_pin_static` \| `corner_pin_tracked` \| `green_screen_pin` \| `screen_locked` \| `add_blend` \| `matte_over` \| `split_screen` |
| layer | `tracking` | How position is known | `none` \| `static` \| `green_detect` \| `planar_track_manual` \| `camera_track_json` \| `point_track` |
| layer | `matte_source` | Matte origin | `none` \| `render_alpha` \| `green_key` \| `sam_mask` \| `background_removal` \| `roto` |
| layer | `mirror_state` | Required final state (C2 era table) | `normal` \| `mirrored` |
| layer | `added_before_flip` | Added before the whole-frame flip | `yes` \| `no` |
| layer | `own_flips` | Flips of this layer alone | 0 \| 1 |
| layer | `text_exact` | Exact letters as in the script | "IONA VALE" \| `none` |
| layer | `blend`, `opacity` | Mode; 0-1 | `normal` \| `add` \| `screen` \| `multiply`; 0.06 |
| layer | `match_notes` | Blur, grain, colour, light side | "blur 0.8 px; key frame-left" |
| comp job | `grain_pass` | Whole-frame grain in the comp | `none` (default) \| `blender_film_grain` \| `blender_sensor_noise` \| `ffmpeg_noise` \| `python_noise` |
| comp job | `tool` | Main tool | `ffmpeg` \| `python_script` \| `blender` \| `resolve_free_manual` \| `resolve_studio` \| `after_effects` |
| comp job | `difficulty`, `est_hours` | From §7 | `easy` \| `medium` \| `hard`; 1.5 |
| comp job | `qc` | §9 results | list of `{check, result, note}`; `pass` \| `fail` |
| comp job | `status` | Progress | `planned` \| `in_progress` \| `review` \| `approved` |

**Validator checks** (add to C5 §6.6) [J]: **VC1** `own_flips` + (1 if `added_before_flip` and `whole_frame_flip` are both `yes`) is odd exactly when `mirror_state` = `mirrored`. **VC2** every `insert_graphic` has `text_exact` matching a quoted script line. **VC3** every `element_3d` points to a previs job with `camera_track.json`. **VC4** `add`/`screen` for every `reflection`, `light_fx`, `hud`. **VC5** no AI-pass layer above an `insert_graphic`. **VC6** text inside the 2.39 safe band when cropped. **VC7** `grain_pass` = `none` whenever D8 `finish.grain.method` ≠ `none`. **VC8** if `whole_frame_flip` = `yes`, D8 `finish.flip` = `no` for the comp output.

## 4. Procedures

**P0. Running any recipe** [§6]
1. Put the kept take, content or element files and the comp plan in one folder named after the shot.
2. Say to the LLM (template): "Run D6 Rec<N> for <shot ID> from comp plan <comp_id>. Keep every in-between file as PNG or ProRes 4444. When done, export the first, middle and last frames as PNG at full size, plus a 200% crop of the worst edge, and show them to me with the recipe's acceptance test as a checklist."
3. Answer pass or fail per acceptance line; on a fail, describe it plainly ("green line on her thumb"); the LLM maps it to §10.
4. After three fails, change method (rule 33).

**P1. Static screen or card** [Rec1-2; V, re-run 28 Sept]
1. Content as its own 16:9 clip or PNG, overlay text burnt in, flip decided (rules 22-24).
2. Four corners from one frame (the LLM by colour, or hover each corner in an image viewer and read x, y).
3. Run (template; corner order TL, TR, **BL, BR**; `scale` = plate size; the 8 px transparent pad stops edge colours smearing over the frame):
```
ffmpeg -i plate.mp4 -loop 1 -i content.png -filter_complex "[1:v]format=rgba,pad=iw+8:ih+8:4:4:color=black@0,scale=1920:1080,perspective=x0=TLx:y0=TLy:x1=TRx:y1=TRy:x2=BLx:y2=BLy:x3=BRx:y3=BRy:sense=destination:eval=init[g];[0:v][g]overlay=0:0:shortest=1,format=yuv420p" out.mp4
```
4. Screen look: blacks slightly lifted, 3-5% soft highlight (add), blur to plate softness [J].

**P2. Moving green screen** [Rec1; V]
1. Prompt the device (§6 template).
2. `python screen_insert.py plate.mp4 content.mp4 out.mp4 --blur 0.8` (`--flip-content` mirrors content; `--smooth 3` static only; `--grain 4` only if no D8 grain follows).
3. Output is a viewing file (`mp4v`); for the final stack the LLM re-pins from `corners.csv` into PNG or ProRes 4444 (rule 20).

**P3. Text** [Rec2]
1. Draw at 2-4× on-screen size in the design font (SVG or Pillow); MIRRORED copy by C2 R6's SVG wrapper or `hflip`; check each letter.
2. Choose the row:

| Text | Era / plate | Add which file | When | Flip count |
|---|---|---|---|---|
| World lettering in a flipped era, whole shot flipped later | B, method 1 | NORMAL | before the flip | 1 |
| World lettering on a plate already flipped (C2 R5 still) | B | MIRRORED | after | 1 |
| Exception prop meant to read normally | B | NORMAL | after the flip | 0 |
| Unflipped era text | A, and C world | NORMAL | any time | 0 |

3. Pin; blur and grain to the surface.
4. Hold max(2 s + 0.5 s/word; 1 s + characters ÷ 12), doubled if mirrored (B1 R2, A4 R8, D12 rule 8): RECEIVING 2.5 s; mirrored "NELL ROWAN. FLIGHT TEST." 8 s.

**P4. Unflipped character on a flipped plate** [Rec3]
1. Generate the location normally; flip; save `_MIR`.
2. Generate the turned character on plain grey, same lens, height, angle, lit from the flipped key side.
3. Still route (preferred), edit-model wording (template, C2 R5): "Do not mirror her. Keep the background exactly as given, including all lettering. Match the background's light, which comes from image-left." Rings in separate close-ups.
4. Video route: matte (removal service or SAM with `apply_mask: false`), place by contact line, contact shadow multiply 20-40%; relight the still with IC-Light V2 first if the key side disagrees.

**P5. Blender elements** [Rec4; V, re-run 28 Sept: 40 frames in 56 s on CPU]
1. The LLM writes `elements.json` (size m, start, drift/s, spin, colour, `carrier_follows_camera`).
2. `python element_layer.py camera_track.json elements.json out_dir` (headless bpy, Standard view transform).
3. Check on `clay.mp4`, then on the plate at beat frames; occlusion by (1 − body's SAM matte).
4. Intermediates: `-c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le` [V]. Readable beads within about 1 m of a 24 mm lens.

**P6. Other recipes** [Rec5-9]: *Reflection:* plate ANGLED 30-60°, Iona's side lit (B3 §8.1, R28); source = Iona seen from the glass, flipped; blacks zero; screen 4-10%; 1-2 px blur. *Visor POV:* Python HUD per frame, add 70-90%, 1 px fringe, words mirrored in place; *exterior:* hand track of the rim, unreadable shapes only. *Appear/vanish:* A's last frame held with grain, B's thing (and what it touches) matted over from the cut. *Multi-take:* locked camera split, seam in static background, feather 40-80 px; moving camera matte-over only if paths match within 2 px, else regenerate. *Matching:* blacks, tint, blur, motion blur (shutter 0.5), 2-4 px light wrap, grain on added layers (Python, Blender Sensor Noise/Film Grain "Animated", or `noise=alls=4:allf=t`).

**P7. Stack order** [§5]: plate prep (16→24 fps, upscale) → AI passes → clean plates → world-flip step (add what flips with the world, flip once) → unflipped characters → elements → normal-reading text → screen-locked HUD → matching → no film grain → 2.39 crop, one final encode.

**Comp plan template** (W1, exact)
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

**Novice time, first/later** [§7, J]: static screen 30/10 min; moving green 60/20 min; dark moving 2/1 h; text 20-45 min; Rec3 still 90/45 min, video 4/2 h; Blender elements 2 h/30 min; reflection 90/45 min; POV HUD 60/20 min, exterior 3/1 h; appear/vanish 90/45 min; split 1 h, matte-over 2-6 h; matching 20/10 min. Helper cost per 5 s shot: SAM 3 ≈ $0.04, SAM 3.1 $0.08, VEED $0.09, Bria eraser $0.70, Wan VACE 720p $0.40 (81 frames at 16 fps) or $0.60 (120 frames).

## 5. Checklists

**QC, every comp, at 100% and at speed** [§9]
- [ ] Edges: no halo, no green on hair, fingers or gloves, no boiling.
- [ ] Key side as the plate, wide and close-up (B2 R20).
- [ ] Mirror: world letters reversed in the right eras; turned items normal; rings, scars, smiles on designed sides; VC1 passes; spelling letter by letter.
- [ ] Temporal: mattes steady, corners not swimming, grain animated, timestamps tick once a second.
- [ ] Reflections: never across a face in ALONG; eyes readable in REFLECTING; only brighten.
- [ ] Tracking: elements stick at first, middle, last frames and fastest move.
- [ ] Match: blacks, saturation, sharpness, motion blur, grain; no film grain when D8 adds it.
- [ ] Occlusion: fingers over screens, bodies over beads.
- [ ] No stretched motion from 16/24 fps mixes.
- [ ] Text, HUD, key props out of the top and bottom eighths for 2.39:1.

**Acceptance tests** [§6]: Rec1 corners steady, no fringe at 200%, fingers in front, screen no sharper than bezel. Rec2 C2's four mirror questions plus spelling. Rec3 key side, eyelines, ring sides. Rec5 eyes readable, moves only with Iona, reads as "her reflection". Rec6 POV HUD steady to the pixel; nothing readable from outside. Rec7 difference view: only the thing changes. Rec8 no doubled limb. Rec9 element never the sharpest, cleanest or most saturated thing unless intended.

**Common fixes** [§10]: frame floods with graphic colour → 8 px pad; no `drawtext` → Pillow; green fringe → despill, shrink matte 1 px; dark sliver → `--smooth 1`; dark Blender elements → fixed script; "Film Grain" not found → bpy below 5.2; washed colours → Standard view; dark rims → `overlay=...:alpha=premultiplied`; banding → 16-bit intermediates, grain last.

## 6. Saying it to AI models

- **Green device screen** (template): "the screen is a flat, evenly lit, pure bright green panel, matte, not glowing; nothing covers its corners at the start".
- **Unflipped person on a flipped plate:** C2 R5's wording (P4), naming the plate's light side.
- **Surfaces for text:** the model sees a blank sign or screen; text arrives as a graphic.
- **SAM 3/3.1 on fal:** short nouns ("tall black figure"; "person, cloth" for several), points or boxes; `apply_mask: false`; $0.005 / $0.01 per 16 frames [V].
- **Bria Video Eraser:** plain nouns ("person", "car", "logo"); up to 5 s; $0.14/s [V].
- **Wan VACE:** mask video + prompt; billed frames ÷ 16 at $0.08/s (720p); set frame count and rate deliberately [V].
- **IC-Light V2 (fal):** stills only, $0.1/megapixel [V]. **Aleph 2.0:** "Change a specific element, preserve the rest", 30 s at 1080p, hands-on in Edit Studio.
- **Resolve:** free 21.1 is manual only. Studio 21.1 ($295): "Resolve Studio 21.1 can connect to Claude, Claude Code and ChatGPT Codex, with setup handled through File > Setup AI Assistants" [V]; test on a copy of the project.
- **Blender:** headless `bpy`; Film Grain (asset, 5.2 LTS), String to Image (node, 5.2), Sensor Noise (asset, 5.0+); assets load from the Essentials library, not by name; none in bpy 5.0.1.

## 7. The Catch

**Decisions made**
- **SC06-SH140 beads (W1):** plate without blood; 20-30 beads, radius 0.5-1.5 cm, squashed 10%, drift 5-15 cm/s, spin 40-80°/s, key from the cage lamp; check frames 12, 26, 40; beads behind Jude cut by his matte; carried until the cage stops. Sparks: screen blend; roof shot = still + tiny warm flicker, no shooter (D11).
- **SC12 monitor:** static pin through CLEAR glass; feed laid out so CONTROL stays left after the flip.
- **SC13 playback:** SC06 previs from the top-gate camera, 4:3, low-res, even 12 fps, timestamp, whole picture flipped once as a pre-turn recording.
- **SC15 feed (W2):** own clip; Jude pre-reversed (wounded arm on the other side); cup moved by matte and clean plate over 12-18 frames; figure by Rec7 hard cut; chair untouched; timestamp burnt in before the one flip (reads backwards) and runs backwards with "Iona runs the picture back."
- **SC17 monitor:** whole picture flipped once; Jude and Eli pre-reversed; Nell unturned (Eli, SC20: "Turned, like us. ... Hers it has to go and find."); "NELL ROWAN. FLIGHT TEST." held 8 s.
- **SC10 kitchen (W3):** Saye's kitchen generated normal and flipped; Iona, Jude, Eli added unflipped; lamp on the table (B3's logged addition: the script says "Iona holds the lamp"); rings in separate close-ups.
- **Wrist (SC18 on):** green patch, `screen_insert.py`; words mirrored in place in B and C; SC23's recorded Saye is a world recording, flipped whole.
- **SC21/SC30 label (W4):** traced letterforms; if backwards, made by flipping the NORMAL drawing, never look-alike characters; flat card, static pin.
- **SC23:** comp reflection, option (c) beside B3's (a) and (b).
- **SC26 visor (W5):** still ledge plate ("Nothing moves."); floating screw in Blender; POV HUD: room labelled RECEIVING, tunnel, rock hatching at 90° (not 45°), her outline red inside rock; RECEIVING mirrored in place; stays backwards after SC27; the first forward RECEIVING is the SC28 wall ("On the wall above Saye: RECEIVING.").
- **Text:** "Goods only. No persons." era A normal; SC07 signs flipped with the plate; OSTREL fixed on the still.

**Flagged for the user**
- Era B world screen text: backwards (used) or legible?
- Visor/wrist text after SC27: stays backwards (D12, used) or snaps readable (B1)?
- "IONA VALE" backwards in SC21 and SC30 (assumed) or normal?
- SC23: comp reflection vs B3's (a) or (b).
- The SC26 carriage recording's F (exception-prop decision, open).
- Which wrist carries the display; charge-bar direction; whether to buy Resolve Studio.

## 8. Conflicts and open questions

- **Blueprint §8.5:** adds a "direct" mirror route and a 0.10 face threshold; rule 21 now follows it. **Blueprint §8.7** and C1 P9 send tracked or keyed work to Resolve; D6 uses scripts, Resolve only for hand tracks.
- **C3 vs C2/D6:** C3 lets models draw short signs; library resolution: composite all readable text.
- **B3 R28** calls the SC23 reflection impossible; D6 adds a comp cheat. **B1 §16 vs D12 §4.3** visor snap: D6 follows D12; B1 not updated.
- **D8:** grain resolved (VC7); `finish.flip` and `whole_frame_flip` are one flip (VC8).
- **D5 `post_chain`** puts `flip` before `composite`; for shots with layers added before the flip, the comp's flip replaces it. D5's "add paper or grain over" inserts must mean layer grain.
- **D13 R20** counts a generation plate per `text` and `screen`; text needs none, screens only if generated; use §7 times instead of the 40 min placeholder.
- **D3 rule 23** routes mouths behind a visor to "a composited face, D6"; no recipe exists: nearest is exterior visor track + lip-synced face + faint reflection, Hard 2-4 h [J].
- **Bead count:** C1 20-30, C4 three; D6 recommends 20-30. **C4's track** matches the previs, not the clip (rule 16).
- **Resolve free:** Puget says scripting removed; Digital Production says console remains; either way not LLM-drivable.
- **Open [U]:** fal SAM's `apply_mask: false` output; Bria removal price; Aleph price, API, removal; Beeble API; After Effects MCP reliability; headless Essentials assets; free Resolve's 10-bit handling. No *Catch* shot composited end to end.

## 9. Section map

| Need | File section |
|---|---|
| Fact-check notes and re-tests | header |
| Tags, kit | §0 |
| Definitions (eras, turned, pre-reverse) | §1 |
| Principles 1-9 | §2 |
| Programs, prices, LLM-drivability | §3A |
| AI helpers, licences | §3B |
| Rules 1-25 (14a, 14b, 19a, 19b) | §4 |
| Stack order, flip-count check | §5 |
| Running any recipe; Rec1-Rec9 | §6 |
| Difficulty, time, cost | §7 |
| `comp_plan`, blueprint mapping, VC1-VC8 | §8 |
| QC checklist | §9 |
| Failure modes | §10 |
| Worked examples W1-W6 | §11 |
| Decisions, conflicts, unverified | §12 |
| Sources 1-23 | §13 |
