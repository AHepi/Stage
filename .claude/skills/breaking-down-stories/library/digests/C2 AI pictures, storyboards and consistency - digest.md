# Digest C2: AI images for storyboards, keyframes and consistency

Source: `research/C2_ai_image_storyboards_consistency.md` (785 lines; tool facts checked 2026-09-27). Brackets: [P#] principle (§1); [Rule #] decision rule (§5); [R#] recipe (§8); [W#] worked example (§10). Most rules are author judgment [J]; model names and prices turn over monthly, the method lasts [P7].

## 1. Scope

1. Which image tools make cheap greyscale storyboard frames and photoreal keyframes for image-to-video, and how an LLM drives them (chat-only, node canvas, API/MCP).
2. The consistency system: asset bible (character, location, prop sheets), fixed look lines, states, style frames, per-shot reference stacks, a tool-neutral image request per shot, drift checks, optional LoRA.
3. Exact text and mirror handling (insert graphics, flipped plates), applied to *The Catch*; runs after the scene breakdown and B2 light plan, before any generation.

**Terms** (§0.1). *Storyboard frame*: drawing-like image showing people a shot's plan. *Keyframe*: clean, finished still a video model uses as the exact first (or last) picture of a clip. *Asset*: any repeating thing the audience must recognise; its *sheet* defines it from several views (a *turnaround*: front, three-quarter, side, back). *State*: one version of an asset at one story point (S1, S2...). *Reference stack*: all reference images attached to one request. *Style frame*: one approved image fixing a sequence's light, color and texture. *Drift*: an asset slowly changing across generations. *Edit model*: changes an image by instruction, keeping the rest; *inpainting*: regenerates one marked region. *LoRA*: small file trained on your pictures that teaches an open model one face or style. *Mirror state*: an asset appears as itself (**NORMAL**) or mirror-imaged (**MIRRORED**) relative to the camera. *Plate*: a location image with no characters, for compositing. *Insert graphic*: text, sign or screen made as a precise graphic outside the image model and composited in. *Look line*: fixed 25 to 40 word description of an asset, pasted unchanged into every prompt where it appears.

## 2. Rules

**Order of work**
1. [P1, Rule 1] If an asset repeats (and the story exceeds ~20 shots), then build its approved sheet before any storyboard frame, because consistency is a reference problem (words drift, pictures anchor) and earlier frames must be redone.
2. [P2, Rule 2, §2.1] If a shot will not become video, then stop at a greyscale storyboard frame (the default style); make color keyframes only for video shots whose framing is approved in greyscale, because keyframes cost ~2 to 10x more ($0.0168 batch Nano Banana 2 Lite vs $0.134 Nano Banana Pro 2K or ~$0.17 GPT Image 2.5 high).
3. [§2.2] If making a keyframe from a storyboard frame, then re-compose it for the first instant, not "add detail", because the storyboard shows the most telling (possibly compressed) moment.
4. [P6, §6.1] If a design choice is made, then log it in the index, and paste look lines unchanged, because synonyms are drift in word form and the index lets another LLM reproduce the film.
5. [R1, Rules 6-7] If choosing a path, then: under 150 frames chat-only; 150 to 600 a node canvas or one automated model; over 600 automated with batch pricing. User refuses all setup: chat-only with numbered prompts plus a list of files to attach. Same chain re-run without code: a node canvas (Flora has API and MCP).
6. [§3.7] On any path the user must by hand: create accounts and payment, approve sheet looks, and see every keyframe before video.

**Choosing a tool**
7. [Rule 3] If more than 200 storyboard frames, then Nano Banana 2 in batch for frames with named characters and Nano Banana 2 Lite for the rest, because batch halves the price and Lite has no character-reference capacity.
8. [Rule 4] If three or more named characters are in frame, then Nano Banana Pro with one clean face crop each, because it documents five character references; others blend faces.
9. [Rule 5] If a keyframe must keep a face exactly in a new pose or setting, then GPT Image 2.5 Sunburst (API) or Nano Banana Pro from the sheet; on ChatGPT, which picks Flare or Sunburst itself, check faces more strictly.
10. [Rule 8] If Midjourney's look is wanted, then only for look development and style frames, because it has no API and its terms forbid automation.
11. [Rule 21] If the project is commercial, then hosted paid models or Apache 2.0 weights (FLUX.2 klein 4B, Z-Image, Qwen-Image-Edit-2511); never self-host Qwen-Image-2.1, Ideogram 4.0 weights, FLUX.2 dev or klein 9B without a license, because open weights are not free for commercial use.
12. [Rules 20, 27] If a tool is over six months old or labelled preview/alpha/beta/early access, then re-check it and use it for tests only, because it changes without notice.
13. [Rule 23, R1] If testing a tool, then use the hardest asset (THE FIGURE beside a door) and report that image's cost, because easy prompts flatter every model.
14. [Rule 28] If a frame may need an exact re-run, then prefer a fixed-seed model (Runway Gen-4 Image, ComfyUI open models) and log seed and full prompt in `index.csv`, because chat-style models vary every time.
15. [§3.6] If using ShotDeck film stills, then only to find and describe a look, never as commercial references, because that copies a copyrighted frame.

**Resolution and keyframe composition**
16. [Rule 25, §2.3] If an image feeds image-to-video, then generate at 2K+ in the exact delivery ratio (never Nano Banana 2 Lite, 1K only); storyboards may be 1K, because 16:9 "1K" is 1376 px wide (under 1920) and upscaling invents detail the video model animates.
17. [Rule 16, §2.3] If delivery is 2.39:1, then use a custom-size model (GPT Image 2.5 at 2560x1072) or generate 21:9 and crop (Gemini 21:9 = 2.357:1; ~18 rows lost at 2K; keep heads and key props out of the top and bottom 1 percent), and draw 2.39 bars on storyboards from the start, because no preset offers 2.39.
18. [Rule 15] If a clip uses start and end keyframes, then make the end by editing the start, because very different frames make the video model cut instead of move.
19. [R4, W1] If making a keyframe, then pose it so the motion can begin (push-in starts wider; entrance space empty; action just begun), because the model then continues rather than invents.
20. [§2.2, R3, R4] If arrows, shot numbers, captions or dialogue are needed, then add them in the storyboard tool, never in the image, because any mark in a keyframe becomes part of the video.

**Consistency**
21. [P3, §6.6] If building a stack, then attach only what is in the shot, name each image's role in the prompt, and when over the limit drop props, then location, never faces, because extras leak backgrounds, light and clothes.
22. [§6.6] If counting a Nano Banana stack, then count every image showing a person as a character image (4 people on Nano Banana 2, 5 on Pro; 10 or 6 objects). If three characters would exceed it, then one full-body three-quarter image each (face large, right costume state) plus a face crop only for the character nearest camera.
23. [Rule 13, §9] If a reference has a busy background, then crop it or regenerate on plain grey, and attach single-view crops, never whole multi-view sheets, because backgrounds and sheet layouts leak.
24. [P5, Rule 17] If a location recurs or has states, then generate the base once and make angles and states by editing it, because fresh generations move doors, windows and furniture.
25. [Rule 18] If an asset is non-human or oddly scaled, then a scale object in every sheet view plus numbers in the prompt, because models pull toward human size.
26. [Rule 19, §6.5] If a sequence has a style frame, then attach it to every request, name the light identically (source, image direction, hardness, color, copied from B2), reuse one palette phrase, grade the sequence together, and review as a slideshow, because each generation relights and drift shows only side by side.
27. [Rule 26] If one look must hold on Nano Banana 2 (no style slot), then move keyframes to Nano Banana Pro (3 style slots) or attach the style frame as image 1 labelled "for light, color and texture only; take nothing else from it", because unlabelled style images leak content.
28. [Rule 14, §6.7] If a lead's face drifts in more than 1 frame in 10 despite a clean stack, then train a LoRA on 15 to 30 approved images and move that character to an open model (or a no-code identity feature); under 1 in 10 keep referencing; locations get more views, not training.
29. [R8] If a LoRA is trained, then test 10 shots: 9 pass, switch; else add 10 images and retrain once; still failing, use Higgsfield Soul ID and accept lock-in.
30. [R4] If a mostly good frame fails one check, then fix it locally (edit model or inpainting), never regenerate.

**Text and mirror**
31. [P4, Rule 9, §7.1] If text must be exact or repeats across shots, then make an insert graphic (LLM-written SVG → PNG → composite), because only a graphic is letter-perfect.
32. [Rule 10] If text must read mirror-reversed, then make correct text and flip only the graphic, because asking for "backwards letters" returns normal or garbled ones.
33. [Rule 11, R5] If a whole location is mirrored, then generate it empty, flip it, add characters with an edit model told not to mirror them, lettering last, because flipping a frame with people flips their faces, rings and wounds.
34. [§7.2, W2] If world lettering must reverse with the world, then composite it onto the unflipped plate and flip both; lettering that must read normally, or that an edit model might "un-flip", goes on last.
35. [Rule 12, R4] If a prompt involves left or right, then restate it by image side ("the hand nearest camera, on image-left"), naming both hand and side, check after generation, and carry small handedness points in separate close-ups, because models place rings and wounds on random hands.
36. [§7.2] If compositing onto a flipped plate, then pose people to its eyelines and exits and relight them to its light, because both flip.
37. [Rule 24] If a screen is in frame, then generate it dark or green and composite its content separately, because content needs its own framing, text and mirror state.
38. [§0, §7.3] If the story has any mirror or handedness logic, then tag every asset's mirror state in every shot.

**Other**
39. [Rule 22] If a scene is violent or bloody, then greyscale, clinical wording, aftermath not impact, gun out of the keyframe where possible, because filters refuse graphic phrasing.
40. [Rule 29] If keyframes go to video tools, then PNG named by shot (`SC012_SH03_start.png`, `SC012_SH03_end.png`).
41. [§6.6] If storyboards are skipped, then drop `purpose: storyboard` blocks (storyboards only: drop keyframe blocks); nothing else changes.

## 3. Breakdown fields

| Level | Field | Plain meaning | Values / example |
|---|---|---|---|
| film | `delivery_aspect_ratio` | Final frame shape, set before any keyframe | `16:9` / `2.39:1` |
| film | `project_use` | Decides usable licenses | `commercial` / `personal` |
| film | `image_path` | How tools are operated | `chat_only` / `node_canvas` / `automated` |
| film | `mirror_rule`, `mirror_eras` | Whose handedness the camera shares; eras with script start/end lines | "camera sees what Iona sees"; A/B/C |
| sequence | `style_frame` | Approved look image | `style/STY_SEQ01_tunnel_torch.png` |
| sequence | `light_line`, `palette_phrase` | Fixed wording from B2, reused verbatim | "single hand torch, from below frame-left, hard, cool white" |
| scene | `mirror_era` | Era; boundaries are script lines, so it can change mid-scene | `A` / `B` / `C` |
| shot | `goes_to_video` | Keyframe needed or storyboard only | `yes` / `no` |
| shot | `mirror_state` | Per asset in frame | `{plate: MIRRORED, IONA: NORMAL}` |
| shot | `handedness_image_terms` | Left/right facts by image side | "wound on his left shoulder, image-right because he faces camera" |
| shot | `keyframe_instant` | First instant, posed for the motion | "fingers in grid, boots just off floor" |
| generation job | `shot`, `purpose`, `model`, `aspect_ratio`, `resolution`, `mirror_state`, `references`, `prompt`, `inserts`, `checks`, `seed`, `output` | The per-image request block (§4) | `purpose`: `storyboard` / `keyframe_start` / `keyframe_end`; reference `role`: style / location / character (+name) |
| generation job | `insert_graphic` | SVG sign/label/screen, NORMAL and MIRRORED files | `INS_TAG_goods_only_NORMAL.svg` |
| character | `look_line` | Fixed 25-40 word description | "IONA: a lean woman in her late thirties, ... gold wedding ring on her left hand." |
| character | `script_facts`, `design_choices` | Must obey vs proposed and approved | "ring on her own left hand" / "which sleeve is torn" |
| character | `states`, `sheet_views` | States; hero, turnaround (front, 34L, side, back), 6 beat expressions, hands and marks, costume states | `CHR_IONA_S1_front.png` |
| character | `handedness_marks` | Left/right details as designed | ring hand, scar side, smile side, wounded shoulder |
| character | `mir_eras`, `scale_object` | Eras needing `_MIR` copies; scale reference | Saye: B; FIGURE: door |
| character | `drift_rate`, `lora_trigger` | From R7; trigger word if trained | "1 in 12"; `ionavale01` |
| location | `layout_drawing` | LLM-written SVG plan/section with heights | shaft section |
| location | `views`, `states` | Master wide, 3-5 angles, details; states edited from base | `LOC_SHAFT_S1_wide.png`; night/day/`_MIR` |
| location | `light_direction_room` | Light source in room terms | "from the window on the east wall" |
| prop | `look_line` (real size), `views`, `states`, `transparent_cutout` | Front, 3/4, top, in-hand; RGBA if composited | "flask about 25 cm tall" |

## 4. Procedures

**Order (§0):** R1 path (show the cost table first) → one image request per shot → R2 asset bible → tag mirror states → R3 greyscale storyboard (one per shot) → R4 keyframes (video shots only) → R7 drift check after every batch.

**Folder and index (§6.1), exactly:**
```
asset_bible/
  index.csv            one row per image: id, asset, state, view, mirror_state, file, look_line, script_quote, approved
  characters/  CHR_IONA_S1_front.png  CHR_IONA_S1_34L.png ...
  locations/   LOC_SHAFT_S1_wide.png  LOC_SHAFT_S1_ladder_up.png ...
  props/       PRP_FLASK_S1_front.png ...
  style/       STY_SEQ01_tunnel_torch.png ...
  inserts/     INS_TAG_goods_only_NORMAL.svg  INS_TAG_goods_only_MIRRORED.png ...
```
Pattern `TYPE_ASSET_STATE_VIEW`; `34L` = three-quarter facing image-left; `_MIR` = mirrored copy. One asset, one name, forever.

**Image request block (§6.6), exactly:**
```yaml
shot: SC014_SH03
purpose: keyframe_start        # storyboard | keyframe_start | keyframe_end
model: nano-banana-pro         # from Section 4; swap freely, the rest stays
aspect_ratio: "16:9"
resolution: 2K
mirror_state: {plate: MIRRORED, IONA: NORMAL, wristband: MIRRORED}
references:                    # order matters; the prompt refers to "image 1", "image 2"
  - {file: style/STY_SEQ05_quarantine_morning.png, role: style}
  - {file: locations/LOC_QUAR_room_S2_MIR.png, role: location}
  - {file: characters/CHR_IONA_S3_full.png, role: character, name: IONA}
prompt: "Image 1 is for light, color and texture only. Image 2 is the room; keep it exactly. Image 3 is Iona; keep her face and costume exactly ..."
inserts: [inserts/INS_WRISTBAND_MIRRORED.png]   # composited after generation (R6)
checks: [face, ring on left hand, wristband letters reversed, light from the room's window wall]
seed: null                     # fill in if the model accepts one (Rule 28)
output: keyframes/SC014_SH03_start.png
```
**Stack order (§6.6):** 1 style frame; 2 location view nearest the camera position; 3 per character, face crop + costume-state full body; 4 each story-critical prop; 5 optional layout reference (Blender/Storyboarder screenshot or stick sketch).

**R1 Setup (once).** User states budget and hand-pasting → LLM picks path (digest rule 5) → chat-only: Google AI Pro or ChatGPT Plus → automated: one account (fal, Replicate or Google AI Studio), card, spending cap, API key pasted where told, never in chat → one test image of the hardest asset, cost shown.

**R2 Asset bible.** (1) Extract every character, state, prop, location with its describing lines; split script facts from design choices. (2) Look lines, user approves. (3) Hero portraits, ~8 per character, grey, even light; user picks one; non-humans full-body with scale object. (4) Turnarounds, expressions, hands, states (12-20 per character), each its own image, cropped and named. (5) Locations (~15 each). (6) Props (~4 each), text as inserts. (7) Flip the right assets into `_MIR`; check any writing is meant to flip. (8) One style frame per sequence from B2's color script. (9) Drift-check every sheet against its look line. Budget ~330 kept images, ~1,000 generations, ~$100-135.
- *Character sheet (§6.2):* hero portrait (chest-up, front, neutral; 4-8 options; the identity anchor) → turnaround by edit model in one 16:9 or 3:2 strip, then cropped → six expressions tied to real beats → hands-and-marks close-ups → one full body per costume state, edited from the turnaround.
- *Location sheet (§6.3):* SVG layout first → master wide with layout attached → 3-5 angles from shot positions, edited from the master → story-critical details → states as edits → always empty.
- *Prop sheet (§6.4):* front, three-quarter, top on grey + one in the right character's hand; every state; transparent version if composited (GPT Image 2.5 `background: "transparent"`).

**R3 Storyboard.** Prompt = greyscale style line + framing and lens (B1) + look lines in frame + light line (B2) + stack list → 2 options per shot at 1K → user picks (~10 s per shot) or says why neither → frames laid out in Boords, StudioBinder or slides with numbers, arrows, dialogue added there → drift check per ~20.

**R4 Keyframe.** Approved shots only: first instant; Sunburst (`high`) or Nano Banana Pro at 2K+, exact ratio, ~3 tries; full stack, style first; left/right in image terms; room for motion; no marks; check, fix locally; end frame edited from start.

**R5 Mirrored plate.** Empty location, world orientation → flip, save `_MIR` → edit model with NORMAL sheets: "Add the woman from image 2 standing at the door on image-right. Do not mirror her. Keep the background exactly as given, including all lettering. Match the background's light, which comes from image-left." → lettering last → four mirror questions.

**R6 Insert graphics.** SVG per graphic → mirrored copy by wrapping everything in `<g transform="translate(W,0) scale(-1,1)"> ... </g>` (W = width; bare `scale(-1,1)` leaves a blank image), checked by eye → PNG → composite ("place the attached graphic onto the wall in perspective without changing any letters") → check every letter.

**R7 Drift check.** Compare each image with the sheets on the fixed list (§5); one-line fix per "no"; log drift rate per character; above 1 in 10, apply file Rule 14 (digest rule 28).

**R8 LoRA.** 15-30 approved images, one costume → captions with a made-up trigger word, describing everything except the face → base by license (klein 4B or Z-Image commercial; klein 9B or dev personal) → fal trainer (1,500-3,000 steps, ~$10-19), Civitai, or rented GPU (~$0.50) → 10-shot test.

## 5. Checklists

- **Character sheet (§6.2):** same face in all views; hair length and parting identical; costume colors identical; ring or mark on the designed side in every view; nothing written on the background; back view shows the same hair and collar; height in proportion to a door (FIGURE) or hand (ANIMAL).
- **Location sheet (§6.3):** doors, windows, fixed furniture where the plan puts them in every view; same count of beds, rails, lamps; materials and colors identical; light from the same room-side; no people; no invented signs.
- **Per keyframe (R4):** face, costume state, hands and rings, props, text, mirror state, light direction.
- **Drift check (R7):** face match, hair, costume state, colors, rings and wounds on the right sides, prop details, text exact, mirror state, light direction.
- **Mirror questions (R5):** world letters reversed? turned items read normally? rings, smiles, wounds on designed sides? light matches?
- **Per sequence (§6.5):** story-order slideshow; light direction consistent between adjacent frames; no sudden day-to-night jumps.
- **Prop (W5):** size against a hand; each state; vessel water dark, animal clear not white.

## 6. Saying it to AI models

**Works**
- Storyboard style lines: rough: "rough pencil storyboard sketch, loose lines, white paper, no color, no text"; default: "greyscale storyboard frame, charcoal and grey marker, 4 tonal values, strong light and shadow shapes, no color, no text, no arrows".
- Numbered roles, then relationship, then scenario: "Image 1 is the style. Image 2 is the room. Image 3 is Iona's face ... Keep image 3's face exactly." Restrict a reference: "use image 3 for the face only".
- Turnaround: "Using the attached portrait as the exact identity reference, create a character turnaround sheet of the same person: full body, front view, three-quarter view facing image-left, side view facing image-left, back view ... [LOOK LINE]. Flat even studio light, plain mid-grey background, no text, no labels, no shadows on the floor. Keep the face, hair, body proportions and clothing identical in every view. 3:2 landscape."
- Expressions: one image each; describe face mechanics (jaw, brow, eyes, mouth corners), never an emotion word alone ("afraid" drifts to a stock scream; "eyes wide, lips pressed together, chin pulled in" holds).
- Hands: name hand and image side: "The hand on image-right is her LEFT hand and wears a plain gold wedding band ...; the hand on image-left is her right hand and wears no ring."
- Location master: "Image 1 is a floor plan of the room; follow its walls, doors and furniture positions exactly. Create a wide establishing view of this empty room from [POSITION ON THE PLAN], eye height 1.6 m, [LENS FEELING]. [LOOK LINE]. [LIGHT LINE]. No people, no text, no signage unless listed. 16:9." Angles: "Show the same room, unchanged in every object, material and light, now seen from [POSITION] looking toward [TARGET]"; name light in room terms ("the window stays on the room's east wall"), since image-left changes per angle.
- Prop: "Product-style reference sheet of one object: [LOOK LINE with real-world size]. Three views side by side on plain mid-grey: front, three-quarter, top ... 3:2."
- Model-drawn text: exact words in quotes, font style, one to four words, position, 2K+.
- Hard cases: weightlessness by its evidence (hair spreading, cloth drifting, bodies horizontal, feet off the grid; compose first, edit floating details in); blood as "small dark red liquid spheres of different sizes, wobbling, catching the light"; "transparent body, faint internal structures visible, light passing through", backlit against dark water; name the glass ("seen through a glass partition, faint reflections of the viewer's room on the glass") plus a door frame; scale in numbers ("about 2.4 m, head above the top of the door frame"); state absence ("smooth featureless head, no eyes, no mouth"); name costume state ("left sleeve torn off at the shoulder") with identical color words.
- Runway Gen-4 Image tags: "@iona at the gate of @cage" (up to 3).

**Fails:** requesting backwards or "mirrored" letters or images (flip instead); "left/right hand" without image side; cliché triggers ("robot", "alien", "exosuit", "armor") giving glowing eyes and armor; emotion words alone; paraphrased look lines; unlabelled style images; whole sheets as references; graphic injury wording.

## 7. The Catch

**Camera rule (§7.3):** the camera sees what Iona sees; an asset is NORMAL when it shares her handedness at that moment, else MIRRORED. Iona never flips.

| Era | From / to | NORMAL | MIRRORED |
|---|---|---|---|
| A | FADE IN to "A hard metal CLACK. BLACK." | Everything | Nothing |
| B | "Her eyes open. Everything is in the wrong place" to Iona's own turn beside the falling ship | Iona, Eli, Jude, clothes, blood, wounds; flask; cage, tag, puck; all found from the cage; meals Saye turned; by inference the ship, THE FIGURE, ship's food | Factory, signs, street, car, bus; Saye, nurse, guard, technician; Saye's house, mint; blanket, wristband, suit lettering; Nell and her photo; by inference world screens |
| C | Receiving room ("RECEIVING ... Reads it again.") to end | Iona, world, Saye, Nell, the sign, vessel, THE ANIMAL | Eli, Jude, their meals |

**Consequences:** world locations in A and B need normal and `_MIR` sets (B's reversed corridor is correct). Saye, Nell: normal and `_MIR` (Saye's ring shows on her right in B). Eli, Jude: `_MIR` for C only. Jude's scar is on his right as designed (script fact), so on his left in C; his ring is on his left as designed.

**Sheets (R2, full state lists there):** IONA S1-S6 (climbing kit to the clear plastic tent); JUDE S1-S6; ELI S1-S5; SAYE S1-S3; NELL S0 (photo, 19 years younger)-S2; THE FIGURE S1-S6, ~2.4 m, matte black, no eyes; THE ANIMAL S1-S4, glass-squid-like. Locations: freight shaft and cage (section drawing first); quarantine rooms with glass (A NORMAL, B `_MIR`, C NORMAL); ship's human rooms (NORMAL in B by inference; deck tilt is camera, not a sheet). Inserts: red tag, floor stencil, exit sign, wristband, OSTREL, meal and dish labels, visor and wrist text ("RECEIVING", "HULL CLEARANCE", "TURN", "CROSS AT 0", "UPWARD SPEED"). Style frames: shaft torchlight; Saye's kitchen before dawn; quarantine morning; quarantine night; ship's dim chamber; outside among stars.

**Worked shots:** W1 falling cage: keyframe as fingers grip and beads start rising; 4 people images on Nano Banana Pro. W2 stencil and exit sign: empty plate, inserts, flip together, add the three unflipped. W3 kitchen: generate Saye in her kitchen, flip, add Iona and Jude; "Both women raise the hand nearest the camera, palms toward each other, exactly like a reflection"; rings in separate close-ups. W4 tablet: the feed is its own 16:9 layer; keyframe is the empty moment before the FIGURE appears (made in editing). W5: backlit vessel views, transparent cut-outs reused.

**Cost (~300 shots, ~120 to video):** bible $100-135; storyboard ~$10 batch; keyframes $50-80; inserts $0; optional LoRA ~$13.

**For the writer/user to decide (§7.4, §11):** Iona's torn sleeve; Jude's wounded shoulder; Eli's smile side and shod foot; the stencil's number and word; the toy carriage F (a follow the script as the one exception, b follow the rule, c show it on Saye's recording); world screens mirrored or not; the copied "IONA VALE" label (logically backwards in B and C, printed normally); ship NORMAL in B (inferred from "Turned, like us"); delivery aspect ratio; commercial or personal.

## 8. Conflicts and open questions

- **"Keyframe":** C2 means the start (or end) still; C1 and C3 mean any picture pinned inside a clip; B3 says "start frame". Pick one term.
- **Look line vs identity key:** B5's "identity key" is the same block, 20-30 words for minor characters; C2 says 25-40.
- **Mirror method:** C2 flips empty plates and adds un-flipped people (R5); B1 prefers "flip and compensate" for wides (pre-reverse turned things or flip the reference, generate, flip the output). State when each applies.
- **Open logic B1 already answers:** B1 recommends the F as exception props (C2 option a), treats world screens as mirrored, and assumes the copied name reads backwards; C2 leaves all three open.
- **Aspect ratio:** B1 recommends 2.39:1 (from 16:9, keep heads and text out of the top and bottom eighths); C2 leaves it open (21:9 crop or custom size).
- **Negation:** C2 image prompts use "no text, no people"; C3 says Luma video prompts should avoid "no/not/without".
- **Style-frame count:** R2 names 6 sequences; its budget counts 8.
- **Unverified (§11):** several tool prices and API access (LTX Studio, Figma Weave, Higgsfield, Artlist, Midjourney, Flora); GPT Image 2.5 per-image prices (Runway resale used); attachments per message in the Gemini app and ChatGPT (test the largest stack first). Budgets are [J].
- **Watch:** FLUX 3 Image, Gemini 4, Midjourney Edit Model leaving alpha. Ending: original Nano Banana (Oct 2, 2026), GPT Image 1 (Oct 23), `grok-imagine-image-quality` (Nov 2); gone: Imagen 4, Reve API, Sora 2 API.

## 9. Section map

- **§0:** order of work; terms; evidence labels. **§1:** seven principles.
- **§2 What you are making:** §2.1 three storyboard styles with prompt lines; §2.2 storyboard frame vs keyframe table; §2.3 aspect ratios and pixel sizes per tool, resolution rule, 2.39:1 method.
- **§3 Landscape:** §3.1 image model table and Arena ranks; §3.2 superseded; §3.3 open-weight adapters, Comfy MCP; §3.4 LoRA licenses, trainers, costs; §3.5 storyboard and canvas tools; §3.6 reference libraries; §3.7 three paths, cost table. **§4:** tool per aim. **§5:** Rules 1-29.
- **§6 Consistency system:** §6.1 folder, names, look line; §6.2 character sheet, prompts, checklist; §6.3 location sheet; §6.4 prop sheet; §6.5 light and color; §6.6 reference stack, Nano Banana counting, YAML block; §6.7 when to train.
- **§7 Text and mirror world:** §7.1 ordinary text; §7.2 flip method, seven failure modes; §7.3 eras table and consequences; §7.4 three unresolved logic points.
- **§8 Recipes R1-R8** (R2 holds the cast and location tables). **§9:** failure-mode table. **§10:** W1-W5. **§11:** open questions. **§12:** 97 sources.
