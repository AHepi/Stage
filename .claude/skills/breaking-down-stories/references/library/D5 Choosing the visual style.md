# D5. Choosing and locking the film's visual style: photoreal, animated or stylised; the style bible; the named-reference policy

Library file D5. Written 2026-09-27. Test sources: *The Catch* (screenplay, workshop revision of 25 September 2026) and *The Long Places* (prose novella, revised final).

> **What this file is for**
> 1. It helps the user choose the film's medium and style (photoreal, 3D animation, stop-motion, 2D, ink, painterly or a hybrid) at checkpoint B, before any character sheet or keyframe is made.
> 2. It records which image and video models handle each style well or badly, and which consistency tools keep a style steady across hundreds of shots.
> 3. It gives a fill-in style bible whose prompt form is C5's `global_look_key`, plus film-emulation and motion-cadence settings applied after generation.
> 4. It keeps film titles, artists and studios out of prompts, and runs a three-direction, three-shot test so the user picks a style by looking at hard shots.
> 5. It lists what changes in B1, B2, B5, C1, C2 and C3 once a style is chosen, worked through on *The Catch* and *The Long Places*.

**Evidence labels.** [V] = read at the primary source, or two agreeing independent sources; [U] = one secondary source, or the primary page refused automated reading; [J] = this file's judgment. [S#] = Sources list at the end; [X1] = a local command test listed there; every web fact there carries its URL and was checked 2026-09-27. Library references use the other files' own numbering (C1 R18 = rule 18 of file C1). **Staleness rule:** re-check any tool fact older than 30 days before spending money (as C1 §0).

**Not repeated here:** model prices and routes (C1 §3, §5, §10); image tools, style frames per sequence, LoRA licences and training steps (C2 §3.1, §3.4, §6.5); lighting and colour script (B2); camera system (B1 §9); character design (B5); prompt adapters and the linter (C3 §16, §21); the legal side of style imitation (D4 §3.3, R5). Storyboard frames stay greyscale whatever the film's style (C2 §2.1).

**Place in the pipeline.** Style is decided at C5's stage 2 (bible) and approved at **checkpoint B**, together with the design theses and identity keys. It must come before C2's asset sheets (C2 R2), because every sheet, style frame and keyframe is drawn in the style, and a style change afterwards means redoing all of them [J]. C5 lists a "global look key" among the project-level fields; this file names it `global_look_key` and defines what goes into it.

**Fact-check note (2026-09-27).** This file was re-checked against its sources: all quotations from *The Catch* and *The Long Places* match the supplied files word for word; web facts were re-opened at the source where possible, and the FFmpeg commands in Section 8.3 were run on a test clip (FFmpeg 7.0.2). Corrections made in that pass: Midjourney's current default is V8.2 (C2 §3.1), not V8; the 20 August 2026 changelog item is a bug fix; Luma Ray3 Modify and Midjourney's `--sw` range are now read at the source; Aleph 2.0 reference frames are documented on its API host; B5's "plush" warning concerns the animal, not the figure; compiled global look keys were added to Section 13.

---

## 1. Words this file uses (one word per concept)

| Word | Plain meaning |
|---|---|
| **Medium** | The kind of picture the film is made of: photoreal live action, 3D animation, stop-motion, 2D drawing, or a hybrid of two. |
| **Style** | The medium plus the fixed way it is rendered (line, texture, grain, lens, motion). In this file, *style* never means lighting or colour of one scene. |
| **Look** | The light and colour of one location or sequence (B2's plan, C3's `look_key`). A look sits inside the style and may change; the style may not. |
| **Photoreal** | Pictures meant to be taken as photographs of a real world. |
| **Stylised** | Any medium that is visibly made (drawn, painted, sculpted or computer-animated), not photographed. |
| **Style bible** | The one-page record of the chosen style (Section 5). It is fixed after checkpoint B. |
| **Rendering descriptor** | One short visible phrase about how every image is made ("bold black brush lines of varying weight"). The bible holds 8 to 15. |
| **Global look key** | C5's film-level field: the style bible compiled into one word block pasted unchanged at the start of every image and video prompt. |
| **Style direction** | One candidate style written as a draft bible, tested before the choice (Section 7). |
| **Style reference** | An approved image attached to a request only to carry the style (C2 Rule 26 labels it "for light, color and texture only"). |
| **Style code** | A tool's number for a style, such as a Midjourney `--sref` code. It is tied to one tool and one model version. |
| **Film emulation** | Making digital pictures look shot on film stock: grain, halation, gate weave, softer highlights. |
| **Grain** | Fine random texture that changes every frame, from the silver or dye particles of film. |
| **Halation** | A soft red-orange glow around bright highlights, made when light passes through film, reflects off its base and exposes it again from behind [S17][S18]. |
| **Gate weave** | A slight frame-to-frame wobble of the whole picture, from film moving through a camera or projector [J]; Resolve's Film Look Creator offers it as a setting [S13]. |
| **Lens character** | The fixed optical signature of a style: spherical or anamorphic (B1 §4.4), clean or soft edges, flares or none, focus falloff. |
| **Cadence** | How often the picture changes per second. Live action changes every frame (24 per second). |
| **On twos** | Each drawing is held for two frames, so 12 new pictures per second at 24 fps; "on ones" is 24 new pictures per second [S15][S16]. |
| **Restyle** | A video-to-video edit that keeps a clip's motion and changes its style (Runway Aleph 2.0, Luma Modify) [S7][S9]. |
| **Uncanny valley** | The drop in comfort viewers feel when a face is almost, but not quite, human [S19]. |
| **Regression** | A model pulling an original design back to a familiar stock design (B5 §7.5: robot, diver, glowing jellyfish). |
| **Spot colour** | A single flat colour printed on an otherwise black-and-white image, used only on chosen objects. |
| **`human_notes`** | D4's field where names of films, directors, artists, studios and franchises may live. Never compiled into a prompt (D4-V17). This file's film-level version is `style_human_notes`. |
| **Style frame** | One approved finished-looking still per sequence, in the locked style, attached to every request in that sequence (C2 §6.5). |
| **Probe** | A small test batch made before a large one, so a failure costs a few images rather than hundreds (B2 §13.5). |
| **Image-to-video** | A video model starts from an approved still and adds motion; the still fixes the style. |
| **Video-to-video** | A model takes an existing clip and changes it (a restyle) while keeping its motion. |
| **LoRA** | A small add-on file (tens to hundreds of MB) trained on your own approved images or clips, which teaches an open model one face, object or style (C2 §3.4). Hosted models such as Nano Banana, GPT Image and Midjourney cannot load one. |
| **fps** | Frames per second: how many still pictures make one second of video. This library delivers at 24. |
| **Cel** | Traditional hand-drawn animation look: clean outlines filled with flat colour, as painted on clear cels. "Cel-shaded" is the computer version. |
| **Hatching** | Shading drawn as many fine parallel lines; cross-hatching layers them at angles. |
| **Boiling** | Lines or textures that wobble and redraw themselves from frame to frame although nothing in the scene moves. |
| **Insert** | A close shot of an object or detail (a bolt hole, a ring, a label). **Plate:** a clean background clip onto which other elements are later composited (layered). |
| **Value** | How light or dark something is, regardless of its colour; B2 scores it 1 (dark) to 5 (bright). |

---

## 2. Core principles

1. **Style is a story decision first and a technical decision second.** Choose it from what the story needs the audience to believe, then check that current models can hold it [J].
2. **One style, fixed in one place.** Style words live only in the global look key. Scene look keys (C3), identity keys (B5) and shot prompts never add or change style words [J].
3. **The still sets the style; video keeps it.** Make approved stills in the style and animate them; do not ask a video model to invent the style from text (C1 §5 stylised row) [J].
4. **Describe, never name.** Every reference to a film, artist or studio is translated into visible descriptors; the name stays in `human_notes` (D4 principle 2) [J].
5. **Choose on the hard shots.** A style that looks good on an empty wide and fails on a face, a hand, a mirrored sign or the creature fails the film (C2 Rule 23) [J].
6. **Texture and cadence are finished in post.** Grain, halation, gate weave and on-twos timing are added after generation, the same way on every shot [J].
7. **A style changes the other files' defaults, never their story reasons.** B1's lens family, B2's key sides and motif code, B5's distinguishers keep their meaning; only their wording changes (Section 9) [J].
8. **Lock, then scale.** No sheet, style frame or keyframe is made until the user has approved the style at checkpoint B [J].

---

## 3. Style catalogue: what current models do well and badly

Model facts come from C1 and C2 (checked 2026-09-27) unless marked with a new source. Price per generated second does **not** fall for stylised work: the same video models cost the same [J]. Savings come only where a style accepts held stills and fewer moving shots (rule R5).

### 3.1 Summary table

| Style | Image models | Video models | Consistency tools | C1 route |
|---|---|---|---|---|
| **Photoreal digital** | Strongest everywhere; top Arena models are photoreal-led (C2 §3.1). Risk: the "AI house look" of unasked light shafts, rims and bokeh (B2 §12) | Best trained case: native audio, lip sync, performance transfer (C1 R1, R12). Weak: physics, hands, near-human faces in close-up | Reference packs (C1 P2), identity keys (B5), style frames (C2 §6.5), face LoRA if drift >1 in 10 (C2 Rule 14) | Every row of C1 §5, e.g. dialogue on Kling 3.0 Omni, MiniMax H3 or Seedance 2.5 with your own voice track; wides on Veo 3.1 or Kling 3.0; performance transfer (Act-Two, Ray3.2) |
| **Photoreal, film-stock emulation** | As above | As above; grain asked for in prompts varies clip to clip [J] | As above, plus one post grade and grain pass on all shots | As above + post (Section 8) |
| **3D animation, CG feature look** | Good at clean rounded CG surfaces; drifts to a generic family-film look with large eyes and toy proportions [J] | Stable motion; less uncanny in close-up than photoreal [J]; lip sync untested per model [U] | Style frames; Blender renders can be part of the final image (C4) | Image-to-video from approved stills; Luma Modify restyle of a previs clip ("turning live-action into CG or stylized animation") [S9]; for dialogue, act it on a phone and transfer the performance onto the CG character (C1 §5; Runway's Act-One launch page says it "accurately translates performances into characters with proportions different from the original source video" [V, S25]; mouth quality on stylised faces untested [U]) |
| **Stop-motion, clay, miniature** | Convincing clay, fingerprints, felt and card; scale drifts (a set turns into a real room) [J] | Motion comes out smooth, not stepped; clay surfaces may melt or morph in long moves [J]. Google lists "claymation style" and "stop-motion animation" as usable style phrases [S1] | Style frames; cadence conversion in post (Section 8.3); video LoRA on open models (LTX 2.3 trainer on fal, $0.006 per step, 2,000 steps default, "at least 10 clips") [S11] | Stills → image-to-video; draft on cheap tier |
| **2D cel or anime** | Midjourney Niji 7 (released 9 Jan 2026): "Niji V7 features improved anime coherence, prompt understanding, text rendering, and sref performance" [V, S2]. Google also lists "Japanese anime style" and "cel-shaded animation" as style phrases [S1] (this library writes the visible traits instead: "clean outlines, flat colour fills, two-tone shading"). Faces simplify, so identity rests on hair shape and colour [J] | Line weight "boils" and details swim between frames [J]; restyle possible ("Make it dark anime style", Aleph 2.0, clips up to 30 s at 1080p) [S7] | Style codes (`--sref`), style frames, style LoRA (image C2 §3.4; video Wan 2.2 trainer on fal, $0.004 per step, 480p, "for $4 you can fine-tune a LoRA for 1000 steps") [S12]; on twos in post | C1 §5: Midjourney stills → Midjourney video or Ray3.2; backup Aleph restyle |
| **2D painterly or watercolour** | Very strong for stills [J]; Google lists "watercolor painting coming to life" as a style phrase [S1] | Paint texture crawls; brush marks re-invented every frame [J] | Style frames; low motion; still + push-in (C1 rule 24) | Same as anime row |
| **Ink or graphic novel** | Strong; Google lists "gritty graphic novel illustration" and "charcoal sketch animation" [S1] | Hatching flickers; solid blacks and white paper hold better than mid-tone hatching [J] | Style frames; spot-colour rule; held panels with slow push-in are native to the form [J] | Stills first; image-to-video with minimal motion; still + push-in for inserts |
| **Hybrid** (drawn people on painted or photographed backgrounds; CG character in photoreal plates; photoreal with drawn inserts) | Each layer separately good; joins fail (light, edge, grain mismatch) [J] | Compositing needed per shot (C1 R6, R23) | Two bibles joined by a written join rule (R17) | Plate + character generated separately (C1 §5 "plate") |

### 3.2 Tool facts for keeping a style steady

- **Midjourney style references.** The V8 alpha announcement (17 March 2026) says its "ability to understand your aesthetics through personalization, style references (srefs) and moodboards is amazing" and "We support backwards compatibility with your V7 personalization profiles, moodboards, and srefs" [V, S3]. V8.2 has been the default since 24 July 2026 (C2 §3.1). Codes made before V7 need `--sv 4` or V6: "If you want to use old sref codes you can either use V6, or you'll need to specify `--sv 4`" [V, S4]. Style weight: "To increase the influence of the style, apply a style weight (`--sw`) that is closer to 1000 ... (default is 100)" [V, S6; stated for V6 in March 2024; the current docs page refused automated reading, so the V8.2 range is assumed unchanged [U]]. The changelog dated 20 August 2026 fixes a bug: "Video mode: dropping images on the Start and End Frame pills now works correctly", which confirms that video mode takes start and end frames [V, S5]. Midjourney has no API and its terms forbid automation (C2 Rule 8), so it is a look-development and by-hand tool, not a batch route. Plans start at about $10 a month (Basic) and $30 (Standard) [U, secondary price guides].
- **Nano Banana Pro** has three style-reference slots; Nano Banana 2 and 2 Lite have none (C2 §3.1, Rule 26). Recraft V4.1 offers "V4 Styles" style references (C2 §3.1).
- **Runway Aleph 2.0** edits clips "up to 30 seconds long at 1080p" and advertises restyling ("Make it dark anime style") [V, S7]. On its API host, a restyle can be steered by an edited frame: "You pull a still from the source video, edit that still externally ..., then send the edited frame back as a reference"; input clips run 2 to 30 s, up to 1080p [V, S24]. **Practical method:** take the clip's first frame, restyle it into an approved style frame with an image model, then send clip plus frame to Aleph [J].
- **Luma Modify Video** (API) has three strengths, "Adhere", "Flex" and "Reimagine", each with levels 1 to 3, and takes an "optional (but preferred)" first frame "to guide it"; the API page lists ray-2 (up to 10 s) and ray-flash-2 (up to 15 s) only [V, S9]. **Ray3 Modify** (announced 18 December 2025, in Luma's app) lets you "reimagine form, environment, and identity" while keeping the original motion, adds "Start and End Frame control to the video-to-video workflow", and can "lock likeness, costume, and identity continuity of a specific character" [V, S10]; its API availability is not stated there [U]; the Ray3.2 route is in C1.
- **Video style LoRA** (a small add-on file trained on your clips, C2 §3.4): fal's LTX 2.3 trainer teaches "a new subject, character, object, or visual style", $0.006 per step, 2,000 steps by default (about $12), "at least 10 clips; 20–50 varied clips often work better for a robust concept" [V, S11]; fal's Wan 2.2 trainer costs "$0.004 per step" at 480p (minimum 100 steps charged), and "A T2V LoRA is not compatible with the I2V inference model and vice versa", so train the image-to-video (I2V) kind when your shots start from stills [V, S12]. Open models only; hosted models cannot load them (C2 §3.4).
- **Performance transfer onto stylised characters.** Runway's Act-One page (22 October 2024) says the model "accurately translates performances into characters with proportions different from the original source video" [V, S25]; C1 routes performance through its successor Act-Two, Kling Motion Control or Ray3.2. This is the most promising dialogue route for CG, stop-motion and 2D characters, but no source tested lip accuracy on stylised mouths [U].
- **Filters do not relax for cartoons.** A tester's anime sword duel was flagged as graphic violence (C1 §4, source S67 there) [U].

### 3.3 What each style costs (pattern, not a quote)

Per-second video prices are the same for every style (C1 §3A). What changes is how many shots must move, how many retakes a style needs, and what extra work it adds. Costs below are relative to photoreal digital = 1.0 for a film of the same length [J; no published per-style retake ratios were found].

| Style | Relative generation cost | Why | Extra work the user must budget |
|---|---|---|---|
| Photoreal digital | 1.0 | Every shot moves; dialogue close-ups need voice-first routes (C1 R1) | Face LoRA if faces drift (C2 Rule 14) |
| Photoreal film emulation | 1.0 | Same shots | One grade and grain pass (Section 8), 1 to 2 hours once |
| CG 3D | 0.9 to 1.1 | Fewer face retakes; Blender renders can stand in for some shots (C4) | Model-sheet turnarounds (C2) |
| Stop-motion | 0.7 to 0.9 | Stepped motion hides small glitches; held inserts read as the style | Cadence conversion; hero props at larger scale for macro inserts |
| 2D cel or anime | 0.8 to 1.0 | Line boil forces retakes on moving shots | Style LoRA likely (R17); expression sheets |
| Painterly | 0.6 to 0.8 | Many shots can be still + push-in | Colour and value checks on every still |
| Ink graphic novel | 0.5 to 0.8 | Held panels and slow pushes are native to the form (R5) | Hand-lettering spec for inserts; spot-colour check |
| Hybrid | 1.3 to 1.6 | Two layers per shot plus compositing (C1 R6, R23; D6) | A join rule and a comp job per shot |

If the difference matters to the decision, then run the selection test (Section 7.1) and read the real retake ratio from the scores (criterion "Cost"), because these ranges are judgment, not measurement.

---

## 4. Choosing a style

### 4.1 What decides it

| Factor | Question to ask the user | Points toward |
|---|---|---|
| Story contract | Does the story work only if the audience trusts the world is ours? | Yes → photoreal. No, or the source is fable, myth or fantasy → any medium (A1: nonrealism permits frontal, iconic framing and on-the-nose moments) |
| Audience | Festival drama, family, genre fans, social feed? | Drama → photoreal or restrained stylised; genre → any; feed → bold, readable at phone size [J] |
| Budget | Under $1,000 for generation (C1 §10)? | Styles that accept held stills: ink, painterly, stop-motion [J] |
| Faces | How many dialogue close-ups on invented faces? How much uncanny drift can the user accept? | Many and low tolerance → a clearly stylised face, or budget a face LoRA [J] |
| Hard content | Readable text, hands, impossible physics, mirror text, a creature that must not look stock? | See 4.2 |
| Time | Can the user review 300 shots twice? | Stylised forgives small drift less than people expect: line and texture drift are visible [J] |

**Evidence on faces.** Mori, the author of the uncanny-valley idea, recommended "that designers instead take the first peak as their goal", meaning moderate human likeness rather than near-perfect [V, S19]. A perception study of computer-made faces found "shape is the dominant factor when rating realism and expression intensity, while material is the key component for appeal", and "realism alone is a bad predictor for appeal, eeriness, or attractiveness" [V, S20]. For a pipeline this means: a stylised face shape reduces the "almost human" risk, and surface material (skin, clay, paper) decides whether the audience likes the face [J].

### 4.2 How each style handles the known failures

| Failure (library rule) | Photoreal | 3D CG | Stop-motion | 2D cel or anime | Painterly | Ink |
|---|---|---|---|---|---|---|
| Readable text (C1 R6, C2 Rule 9) | Insert graphic, printed font, perspective and grain matched | Insert, clean font | Printed at prop scale; reads well [J] | Insert in the style's lettering | Insert; paint texture over it | Hand-lettered insert; lettering is part of the style [J] |
| Hands (C3 §13C) | Weakest in wides; inserts from stills | Better (simpler fingers) [J] | Puppet hands are chunky by design [J] | Four-finger or simplified hands accepted by convention [J] | Hidden in brushwork [J] | Silhouette hands; strong [J] |
| Impossible physics (C1 R8) | Composite; audiences judge harshly [J] | Previs render may become final [J] | Stepped motion hides some glitches [J] | Floating reads naturally [J] | Forgiving [J] | Forgiving; panels can hold [J] |
| Mirror text (C1 R21, C2 Rule 10) | Generate forward, composite, flip | Same | Same | Same | Same | Same; hand-lettered insert flipped |
| Creature regression (B5 §7.5) | Diver or robot | Cute mascot | Toy robot | Armoured mecha or suit [J] | Vague shadow | Superhero armour [J] |
| Near-human faces | Highest risk | Medium | Low | Low | Low | Low |

The mirror method is the same in every style; only the lettering changes [J].

### 4.3 Decision rules

1. **R1.** If the story's force comes from the real world going slightly wrong (a rule broken, a detail reversed), then choose photoreal, because the wrongness reads only against a baseline the audience trusts [J].
2. **R2.** If the source is nonrealist (fantasy, SF, fable, myth, horror; A1), then consider stylised media, and allow frontal, iconic framing where the bible says so, because nonrealism changes what the audience accepts (A1 §5).
3. **R3.** If the film depends on many dialogue close-ups and the user cannot budget a face LoRA (C2 Rule 14), then prefer a style whose faces are simplified shapes (2D, ink), because in the perception study "shape is the dominant factor when rating realism and expression intensity, while material is the key component for appeal" [S20]; test lip sync in the probe [J].
4. **R4.** If lip-synced speech from a native-audio model is essential, then photoreal or CG, because C1's dialogue routes were documented on realistic humans; stylised mouths are untested [U]. If a stylised medium is chosen anyway, then plan dialogue as performance transfer (act the line on a phone, transfer it onto the character; Section 3.2) and include one spoken line in the selection test, because transfer onto different proportions is documented [S25] while lip accuracy on drawn or puppet mouths is not.
5. **R5.** If the budget is under $1,000 (C1 §10), then prefer ink, painterly or stop-motion, because held stills with a slow push-in read as the style there, not as a failure [J].
6. **R6.** If a non-human must frighten and later earn pity (B5 R10), then test it in every candidate style before choosing, because each style has its own regression target (table 4.2) [J].
7. **R7.** If violence is in the script, then do not choose a cartoon style to pass filters, because filters flagged an anime duel as graphic violence (C1 §4) [U].
8. **R8.** If the project needs legally clean training data (C1 R19), then test the candidate styles on those routes first (C1 §5 names Marey, trained only on licensed footage, and Adobe Firefly Video), because the style must be reachable there and these routes have fewer consistency tools (no open LoRA) [J].
9. **R9.** If in-story footage appears (CCTV, tablet, recording), then keep it in the film's medium with the device's grammar (B1 R22: fixed frame, ratio, frame rate, overlay), unless the story says it is a different kind of image, because a medium switch reads as a different film [J].
10. **R10.** If a second style is wanted for part of the film (memory, letters, dream), then write it as a sequence-level `style_exception` with a story reason and its own short bible, at most two per film, because a style break is an extreme and works by rarity (B1 principle P5, extreme budgets) [J].
11. **R11.** If a hybrid is proposed, then choose it only when the story has two worlds (B2 R13), and write a join rule (which layer gets which descriptors, which light wins), because hybrids double the consistency work [J].
12. **R12.** If the user cannot choose among the three directions, then choose by the hard-shot scores, not the prettiest wide, because hard shots set the cost of the whole film (C2 Rule 23) [J].
13. **R23** (numbered after Section 8's rules so earlier references stay valid). If D17 has set `period: near_future` or a past period, then record in the bible how far the world looks from today (`period_distance`) and put the visible markers in props and devices (B4, D12), not in the global look key, because futurity words such as "futuristic" or "sci-fi" pull in the stock neon look that B2 §12 bans, while a device on a wrist can be designed exactly [J].
14. **R24.** If the medium is stylised for the whole film, then do not tag every shot with C1's `stylised` shot need (which D13 classes as `easy`); tag only by the shot's real need (dialogue, creature, text), because the `stylised` row describes a stylised sequence inside another style, and tagging the whole film would under-budget its hard shots [J].

---

## 5. The style bible template

Fill every line; write `none` rather than deleting a line. The LLM drafts; the user approves at checkpoint B.

```
STYLE BIBLE: <film title>                       ID: SB-<PROJECT>-<nn>   locked: yes|no
MEDIUM: photoreal_digital | photoreal_film | cg_3d | stop_motion | anime_cel |
        painterly | ink_graphic | hybrid (+ join rule)
WHY THIS MEDIUM: <one sentence tied to the story contract (R1-R2)>
RENDERING DESCRIPTORS (8-15, visible, positive, frozen word order):
  1. ...
COLOUR: follows B2's colour script and motif table; style limits only:
        <e.g. "spot colour only on motif objects"; "saturation ceiling 3 except sequence 18">
TEXTURE AND GRAIN: <none | fine | medium | heavy>; made in <post | prompt>; <paper, clay, brush>
LENS CHARACTER: <spherical_clean | spherical_vintage | anamorphic | drawn_flat | miniature_macro>
                + B1 lens family translated (Section 9)
MOTION CADENCE: <live_24 | on_twos | on_threes | mixed_ones_twos>; delivery fps <24>
ASPECT RATIO: <from B1 P3 (§5)>, composed for <tool output> and cropped in the edit
PERIOD DISTANCE: <today | near_future_subtle | near_future_marked | period:<year>>
        (D17 sets the period; markers go in props and devices, R23)
LETTERING: <printed font style | hand-lettered>; all text as insert graphics (C2 R6);
        feeds D12's UI style guide (D12 §5.1)
FACE AND BODY PROPORTION: <adult head heights; eye size; nose and mouth treatment>
REFERENCE IMAGES (owned or generated only): <files, role, approved yes|no>
STYLE CODES: <tool, code, model version, --sv, --sw> | none
STYLE LORA: <base model, trigger word, licence> | none
BANNED WORDS: cinematic, epic, blockbuster (B2 §4.8), 8K, ultra-realistic, masterpiece,
        award-winning, stunning, hyper-detailed, futuristic, sci-fi + <list>
EXCLUDE NOUNS (for negative fields, C3 R5): <3-6 nouns naming the wrong medium;
        C3 R5 allows up to 10 in total, so leave room for shot-specific nouns>
POST CHAIN: <cadence -> upscale -> flip mirror shots -> composite inserts and text -> grade -> grain/halation>
        (order follows D8: time before size, size before colour, colour before grain;
        text is composited after upscaling so it stays sharp)
GLOBAL LOOK KEY (compiled, 40-80 words, pasted first in every prompt): "..."
HUMAN NOTES (never compiled): <films, artists, studios that inspired it, and what was taken>
```

**Rules for writing descriptors** [J]:
- Each descriptor names something you could point at in a frame: line, edge, texture, surface, black level, highlight, depth of field, proportion.
- Positive wording only (C3 linter L14): "clean, sharp highlights" instead of "no bloom".
- No light sources or colours of particular scenes (those are B2 look keys), no emotions, no names.
- No quality boosters: "8K", "ultra-realistic", "masterpiece", "award-winning", "stunning", "hyper-detailed" are banned beside B2's three words. Google's own Veo guide (updated 2026-09-25) lists "ultra-realistic rendering", "shot on 8K camera" and "cinematic film look" as style phrases [V, S1]; this library does not use them, because they add the generic house look (B2 §12).
- One word per concept: if descriptor 3 says "brush line", no later prompt says "ink stroke".
- Each descriptor must hold in every shot. If a trait depends on shot size ("shallow focus in close shots"), then write it as a rule the model can apply to any frame ("focus falls off quickly behind the subject"), or move it to the shot prompt, because the global key is pasted into wides and close-ups alike [J].

**Compiling the global look key (prompt for the LLM).** "Compile the global look key from this style bible. Start with the medium phrase, then the descriptors in their frozen order, joined with semicolons. 40 to 80 words. No light sources, times of day, colours of particular scenes, emotions, names or banned words. Return the key and its word count." Check the result against the banned-words list, then store it with a version number (`SB-<PROJECT>-01 v1`); every later change raises the version, and the generation job records which version it used (Section 10).

**Global look key.** Compile the medium phrase and the descriptors into one block, medium first. It goes at the start of every image and video prompt, before C3's scene look key, because the style must be named early (C3 §3A). Scene look keys lose their style words: C3's illustrative keys end in "realistic film look" and "Gritty realistic film look with fine grain"; delete those endings and let the global key carry style [J].

---

## 6. The named-reference policy

1. **R13.** If anyone (user, LLM, a vendor guide) proposes a film, director, cinematographer, artist, studio or franchise as a style reference, then write the name in `style_human_notes` and translate it into descriptors with Recipe 7.3 (Fact-check edit: the draft pointed to a non-existent "Recipe 6.3"), because names pull models toward protected frames and characters and trigger filters (D4 R5) [J].
2. Google's Veo guide itself suggests "in the style of Van Gogh", "classic Disney animation style" and "Pixar-like 3D animation" [V, S1]. Do not follow those examples here.
3. OpenAI's system card for GPT-4o image generation (25 March 2025) says: "We added a refusal which triggers when a user attempts to generate an image in the style of a living artist" [V, S21]. An OpenAI spokesperson told TechCrunch that ChatGPT "refuses to replicate the style of individual living artists" while permitting "broader studio styles" [V, S26]. So a studio name may pass a vendor's filter; this library still keeps it out of prompts, because the rule here is about copying and consistency, not about what a filter allows. Whether GPT Image 2.5 keeps the same rule was not re-checked [U].
4. **R14.** If a style reference image is attached, then it must be generated in this project and approved, or a photograph the user took, or licensed for AI input, never a film still, poster or another artist's work (C2 §3.6 on ShotDeck), because the attachment is copied more closely than a name [J].
5. **R15.** If a Midjourney style code is used, then record the code, the model version and the `--sv` value, and keep the resulting approved images as the real references, because codes are tied to versions [S4] and Midjourney cannot be automated (C2 Rule 8).
6. The validator check D4-V17 (no `human_notes` name in any compiled prompt) covers the style bible too.

---

## 7. Recipes

### 7.1 Three directions, three shots (the selection test)

Cost [J, from C1 and C2 prices]: stills 3 directions × 3 shots × 4 candidates = 36 images × about $0.134 (Nano Banana Pro 2K) ≈ $5, or one Midjourney month ($10 to $30); video drafts 9 × 2 × 5 s × $0.05 to $0.10 ≈ $4.50 to $9; acceptance probe below ≈ $5 to $10. Total about $20 to $50. User time: 2 to 3 hours.

1. **Gather.** Paste into the LLM: the logline and themes (A2), B1's camera system, B2's colour script and motif table, B5's design theses and identity keys (provisional), and this file.
2. **Ask for directions.** "Using D5 Sections 3 and 4, propose three style directions for this film: one photoreal, and two others that fit the story. For each, write a draft style bible (Section 5) with 8 to 15 descriptors and a compiled global look key. Put any film or artist names only under HUMAN NOTES. For each, say in one sentence which story reason it serves and which failure in table 4.2 it risks most."
3. **Choose the three test shots.** One dialogue close-up or two-shot (a face that must read), one wide (the world), one hard shot (text, mirror, creature, physics). "Pick the three test shots from the breakdown and quote their script lines exactly."
4. **Make stills.** For each direction and shot, four candidates at 2K (C2 Rule 25), at 21:9 where the image model offers it, otherwise 16:9 with heads, hands and text kept out of the top and bottom eighths for a 2.39 crop (B1 §5). Build each prompt in this order and paste the blocks unchanged:
   ```
   [GLOBAL LOOK KEY of this direction]
   [SCENE LOOK KEY (C3 `look_key`, written from B2's lighting plan), with its style words removed]
   [IDENTITY KEYS of the people or creature in frame (B5)]
   [SHOT: shot size, angle, lens effect in this direction's words (Section 9), subject, action, end state]
   ```
   Attach no style reference yet: the test shows what the words alone do.
5. **Make two short video drafts** per shot from the best still, on the cheap tier (C1 R13), motion only (C3 R1).
6. **Apply post.** Run each direction's post chain (Section 8) so the user sees the finished texture and cadence.
7. **Score.** Show the user a grid: rows = directions, columns = shots. Score each cell 0 to 2 on the criteria in 7.2. The LLM fills a first pass; the user overrides.
8. **User picks** one direction, or asks for one merge ("A's line with C's colour"); a merge is re-tested on the hard shot only.
9. **Lock.** Set `style_locked: yes`, `decided_by: human` (C5 field authority).

### 7.2 Scoring criteria (0 = fails, 1 = usable with fixes, 2 = holds)

- **Readability:** the story information of the shot reads in the first second (B1 R2, B2 P1).
- **Identity:** faces and the creature match the design thesis; no regression (B5 §7.5).
- **Mirror and text:** handedness and lettering come out as the mirror era requires, after compositing and flipping.
- **Motif survival:** B2's motif colours read where they should and nowhere else.
- **Motion:** the draft moves without boiling, melting or smear that the style cannot explain.
- **Cost:** takes needed per kept draft (retake ratio, C1 §1): 2 = one or two takes, 1 = three or four, 0 = five or more.

**Adding up** [J]. Each shot gets up to 12 points (six criteria × 2). A direction's total = face shot + wide + 2 × hard shot (the hard shot counts double, R12), so the maximum is 48. If a direction scores 0 on Identity or on Mirror and text in any shot, then it is out unless the LLM names a specific fix and the fix is re-tested on that shot, because those two failures recur in every scene that contains them. If two directions end within 4 points of each other, then the user chooses on taste, because the difference is inside the noise of four candidates per shot.

### 7.3 Translating a named reference into descriptors

1. The user says what they like ("the look of film X", "artist Y's ink").
2. LLM: "Without using any names, list what is visible in that style under these headings: line, edge, surface texture, black level, highlight behaviour, colour range, depth of field, grain, proportion of faces, motion. Give one short phrase per heading."
3. Keep the 8 to 15 phrases that serve the story; drop any phrase that describes a specific character, costume, logo or composition.
4. Write the name and what was taken into `human_notes`.

### 7.4 Acceptance probe and style frames

1. Run B2's four-shot probe (B2 §13.5, the B2 digest's procedure P7: wide, medium, close-up and reverse of one location) in the locked style, with the global look key and one approved style reference attached. Check B2's items plus: descriptors visible in all four, face style identical, grain and cadence identical after post.
2. If the probe fails, fix descriptors or references once; if it fails again, return to 7.1 with the second-ranked direction (R16 below).
3. Then make C2's style frames, one per sequence (C2 §6.5), in the locked style; they replace the generic style reference from then on.
4. Only now build C2's asset sheets (R2 there), in the locked style.

- **R16.** If the probe fails twice, then change direction rather than add descriptors, because a style that needs constant rescue will fail across 300 shots [J].
- **R17.** If more than 1 in 10 frames in a batch drifts in style (line weight, texture, proportions) despite references, then train a style LoRA on 20 to 40 approved images (C2 §3.4 cites Black Forest Labs' guide at 15 to 40) or on 10 to 50 clips for video [S11], on an open model, or move those shots to still + push-in, because references alone are not holding [J].

---

## 8. Film emulation, lens character and cadence (post settings)

### 8.1 Rules

- **R18.** If film emulation is wanted, then put at most one texture phrase in the prompt ("fine even film grain") and add grain, halation and gate weave in post with one preset for the whole film, because generated grain differs from clip to clip, while a post preset is identical and removable [J].
- **R19.** If the film is delivered by streaming, then keep grain fine, because "film grain's random nature makes it notoriously difficult to compress"; Netflix's AV1 film grain synthesis denoises the source before encoding and re-creates the grain at playback [V, S22 via S23]. For a YouTube upload, D8 advises 15 to 20 Mbps at 1080p when the picture carries grain (D8-R56).
- **R20.** If halation is used, then only around practical lights and bright specular highlights, subtle, never on faces, because it is a film-stock artefact that becomes decoration when everywhere [J].
- **R21.** If the style is 2D or stop-motion, then generate normal smooth motion and convert the cadence in post, because video models output smooth motion and prompting "on twos" is unreliable [J]. Camera moves on twos judder; keep B1's one-move rule and slow the move, or keep the camera static [J].
- **R22.** If lens character is anamorphic, then check B1 §4.4 first: models return flares, not the squeeze (B1 §15); for a clinical film, spherical [J].

### 8.2 Parameter table [J unless marked]

| Setting | Photoreal digital | Photoreal film | CG | Stop-motion | Anime or cel | Ink | Painterly |
|---|---|---|---|---|---|---|---|
| Grain | none or very fine | fine, moving every frame | none | none; surface flicker is enough | none | paper texture, fixed | canvas or paper, fixed |
| Halation | none | subtle, practicals only | none | none | optional glow on lights | none | none |
| Gate weave | none | very slight | none | none | none | none | none |
| Lens character | spherical, clean | spherical, slightly soft corners | virtual spherical | macro, shallow focus in close shots | drawn, flat | drawn, flat | drawn |
| Cadence | 24 fps | 24 fps | 24 fps | on twos | on twos, ones for fast action | on twos or held panels | on twos or holds |
| FFmpeg grain start value (`noise` strength, test before use) | 0 to 4 | 6 to 10 | 0 | 0 | 0 | 0 (paper texture is an overlay) | 0 (canvas is an overlay) |

**Grain sizes as numbers** [J, starting points only]: `fine` = strength 4 to 6, `medium` = 8 to 12, `heavy` = 15 to 20 on a 1080p picture. Judge on a dark shot and a bright shot at full screen; grain that you notice before the image is too heavy.

### 8.3 Post recipe (free route; the LLM writes and explains the commands)

FFmpeg's `fps` filter converts "to specified constant frame rate by duplicating or dropping frames as necessary"; `noise` adds grain with strength `alls` from 0 to 100 and flag `t` for "temporal noise (noise pattern changes between frames)"; `hflip` flips horizontally [V, S14].

All FFmpeg commands below (not the `ffprobe` check in step 0) were run on a 2-second 24 fps test clip with FFmpeg 7.0.2 on 2026-09-27; the on-twos command produced 48 frames made of 24 different pictures, each shown twice [V, X1]. How to use them without technical knowledge: ask the LLM "Run this FFmpeg step on these files and tell me where the results are", or paste the command into a terminal in the folder that holds the clips. `in.mp4` is the clip you start from; `out.mp4` is the new file. Every re-save loses a little quality, so each command below saves at high quality (`-crf 12`; lower numbers mean higher quality and bigger files).

0. **Check the frame rate first:** `ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 in.mp4` must print `24/1` (this one command was not run in the test, because the test build had no `ffprobe`; `ffmpeg -i in.mp4` also prints the rate, as "24 fps"). If it does not, convert the rate first (D8's frame-rate step), because the on-twos command assumes 24 fps.
1. **Cadence on twos:** `ffmpeg -i in.mp4 -vf "fps=12,fps=24" -c:v libx264 -crf 12 -preset slow -c:a copy out.mp4` (the first filter keeps every second frame, the second shows each kept frame twice). On threes: `"fps=8,fps=24"`. Mixed ones and twos: cut the clip and convert only the slow parts [J].
2. **Upscale** if needed (D8; its size step comes before colour).
3. **Flip mirror-era shots:** `ffmpeg -i in.mp4 -vf hflip -c:v libx264 -crf 12 -preset slow -c:a copy out.mp4`.
4. **Composite inserts and text** (C1 R6, D6), in the bible's lettering; add the style's paper or grain over the insert afterwards so it does not look pasted on.
5. **Grade** each sequence together to its style frame (B2 §13.4, the B2 digest's P6 step 7; D8-R28; DaVinci Resolve free).
6. **Grain last, once, on the whole film or at timeline level** (D8-R34): `ffmpeg -i film.mp4 -vf "noise=alls=6:allf=t" -c:v libx264 -crf 12 -preset slow -c:a copy film_grain.mp4`. `alls` is the strength (0 to 100); `allf=t` makes the pattern change every frame, like real grain [V, S14]. For grain in brightness only, without coloured speckles, use `"noise=c0s=6:c0f=t"` (c0 is the brightness channel) [J; command tested, X1].
7. **Gate weave (optional, photoreal film only):** `ffmpeg -i film.mp4 -vf "crop=iw-8:ih-8:4+2*(random(1)-0.5):4+2*(random(2)-0.5),scale=1920:804,setsar=1" -c:v libx264 -crf 12 -preset slow -c:a copy out.mp4` moves the picture by up to one pixel each frame and scales it back to the film's size (replace `1920:804`, a 2.39 frame, with your film's width and height) [J; command tested, X1]. It is a rough stand-in; if it reads as camera shake, leave it out.
8. **Halation** has no simple FFmpeg equivalent; use Resolve (below) or leave it out [J].

Paid route: DaVinci Resolve Studio (version 21, $295 one-off) includes Film Look Creator, which "lets you add filmic color looks, film stocks, halation, grain, gate weave, split toning and more!"; the product page lists it among the Studio-only effects [V, S13]. Secondary guides report a basic Film Grain effect in the free version; D8 lists this as unverified [U].

---

## 9. What changes downstream once the style is chosen

| File | Photoreal (library default) | CG 3D | Stop-motion | 2D cel or anime | Ink graphic | Painterly |
|---|---|---|---|---|---|---|
| **B1** lens words | mm as style hints (C3: "85mm" unreliable; say the effect) | Same as photoreal | "miniature set, camera close, shallow focus" in inserts; wides deeper [J] | Perspective words: long lens → "flat, compressed perspective"; wide → "strong converging perspective, close to the face" [J] | Same as 2D; iconic frontal panels only where R2 allows | Same as 2D |
| **B2** light words | Sources and visible results (B2 §13) | Same; watch soft all-over bounce [J] | Real small lamps, bulbs at set scale [J] | Kelvin becomes flat colour fills; "hard-edged shadow shapes, two tones on the face" [J] | "solid black shadow shapes, paper-white light"; B2's motif colours as spot colour [J] | Warm and cool as paint; watch for unmotivated glow (B2 R4) [J] |
| **B5** faces | 13-field spec as written | Set head heights and eye size once in the bible | Sculpted features; expressions as a small set of mouth and brow shapes [J] | Adult head heights about 6.5 to 7.5 [J]; larger eyes, simplified nose; distinguishers move to hair silhouette, hair colour, costume shape, because line faces average out [J] | Distinguishers as black masses: hair, beard, brows [J] | Distinguishers as colour and value blocks [J] |
| **C1** routes | All §5 rows | Image-to-video; Blender render as final layer | Image-to-video + cadence post; open LoRA | Midjourney/Niji stills → image-to-video; Aleph or Luma restyle as backup [S7][S9] | Stills first; still + push-in for inserts | As 2D |
| **C2** assets | As written | Model-sheet turnarounds | Material and scale notes on every prop sheet | Sheets as clean line model sheets; expression sheet mandatory | Lettering spec for insert graphics | Palette swatches per character |
| **C3** adapters | Global key first, then look key | Same; EXCLUDE "photograph, live action, clay" | EXCLUDE "photograph, live action, cartoon, smooth CG" | EXCLUDE "photograph, 3D render, painting" | EXCLUDE "photograph, colour painting, 3D render" | EXCLUDE "photograph, 3D render, clean vector" |
| **C3** motion words | As C3 §4 | As C3 §4 | "small, deliberate movements"; slow camera or none (R21) | "simple, readable poses; little camera movement" | "held panel, slow push-in" for inserts | "slow drift; minimal movement" |
| **C3** style slot | Style field or first sentence carries the medium phrase only; LTX says named styles "work especially well when named early" (C3 §3A) | Same | Same | Same | Same | Same |

For photoreal, EXCLUDE takes "illustration, cartoon, painting, 3D render" [J]. All EXCLUDE lists are [J] starting points; add the nouns of the failure you actually saw (C3 R5). The motion words are [J]: they ask for less motion because every stylised texture boils or melts more as motion grows (Section 3.1).

**Adapter vocabulary, one example** [J]. The same shot (Iona kneels and puts her torch under the cage floor) in three directions, shot block only:
- (a) photoreal: "Low angle close on the floor frame; a woman's hand holds a flashlight beneath it; the beam rakes across two empty steel brackets."
- (b) ink: "Low panel close on the floor frame drawn in bold brush line; a woman's hand holds a flashlight beneath it; the beam is a white wedge across black shapes; two empty brackets with four white bolt holes each."
- (c) stop-motion: "Low, close view of the miniature floor frame; a puppet hand holds a tiny working flashlight beneath it; its beam rakes across two small painted-metal brackets."

---

## 10. Fields this subject adds to the breakdown

`authored` fields carry `decided_by` and `locked` (C5).

| Level | Field | Meaning | Allowed values / example |
|---|---|---|---|
| film | `style_medium` | The medium | `photoreal_digital` \| `photoreal_film` \| `cg_3d` \| `stop_motion` \| `anime_cel` \| `painterly` \| `ink_graphic` \| `hybrid` |
| film | `style_bible_id` | Pointer to the bible | `SB-CATCH-01` |
| film | `rendering_descriptors[]` | 8 to 15 frozen phrases | strings |
| film | `global_look_key` | C5's field; the compiled bible | 40 to 80 words |
| film | `grain_level`, `grain_made_in` | Texture and where it is made; D8's `finish.grain` records the method and exact strength used in post | `none` \| `fine` \| `medium` \| `heavy`; `post` \| `prompt` |
| film | `period_distance` | How far the world looks from today (D17 sets `period`; R23) | `today` \| `near_future_subtle` \| `near_future_marked` \| `period:<year>` |
| film | `halation` | Highlight glow | `none` \| `subtle_practicals` \| `strong` |
| film | `lens_character` | Optical signature | `spherical_clean` \| `spherical_vintage` \| `anamorphic` \| `drawn_flat` \| `miniature_macro` |
| film | `motion_cadence`, `delivery_fps` | Cadence and frame rate | `live_24` \| `on_twos` \| `on_threes` \| `mixed_ones_twos`; 24 \| 25 |
| film | `lettering_style` | How insert text looks | `printed` \| `hand_lettered` |
| film | `style_reference_images[]` | Approved style images | {file, source: `generated` \| `owned` \| `licensed`, approved} |
| film | `style_codes[]` | Tool style codes | {tool, code, model_version, sv} |
| film | `style_lora` | Trained style add-on | {base, trigger, file, licence} \| `none` |
| film | `banned_style_words[]`, `exclude_medium_nouns[]` | Words never sent; negative-field nouns | lists |
| film | `post_chain[]` | Ordered post operations (D8 order) | `cadence`, `upscale`, `flip`, `composite`, `grade`, `grain`, `halation`, `weave` |
| film | `style_directions_tested[]` | Record of the test | {id, bible, shots, scores, total_of_48, verdict} |
| film | `style_locked` | Approved at checkpoint B | `yes` \| `no` |
| film | `style_human_notes` | Named inspirations (D4) | text, never compiled |
| sequence | `style_exception` | Second style with story reason (R10) | {reason, bible_id} \| `none` |
| shot | `style_override` | Shot departs from film style | `none` \| `diegetic_device` \| `exception` |
| shot | `style_drift_check` | Checked against style frame | `pass` \| `fail` \| `not_checked` |
| character | `style_proportions` | Style overrides to B5's face spec | {head_heights, eye_size, nose, mouth} |
| generation job | `global_look_key_version`, `style_refs_attached[]` | Which bible version and references were sent | `SB-CATCH-01 v2`; files |

---

## 11. Checklists

**Checkpoint B, style lock**
- [ ] Three directions tested on a face shot, a wide and a hard shot; scores recorded.
- [ ] Bible filled on every line; 8 to 15 positive, visible descriptors; no names outside `style_human_notes`.
- [ ] Global look key compiled; scene look keys stripped of style words.
- [ ] Post chain set and tested on one dark and one bright shot.
- [ ] Probe passed (7.4) before any sheet is made.
- [ ] Style reference images are generated, owned or licensed; none is a film still or someone's artwork.
- [ ] Style exceptions (if any) have story reasons; at most two.
- [ ] `period_distance` set; futurity shown by designed props and devices, not by words in the global key (R23).
- [ ] Lettering spec handed to D12's UI style guide.
- [ ] If the medium is stylised, one spoken line was tested (R4) and the hard shot scored at least 1 on Identity.
- [ ] Global look key has a version number; every generation job will record it.

**Per batch** [J]
- [ ] Slideshow in story order: same line weight, texture, proportions and black level.
- [ ] No descriptor missing in more than 1 frame in 10 (else R17).
- [ ] Inserts drawn in the bible's lettering.

---

## 12. Failure modes and fixes

| Failure | Cause | Fix |
|---|---|---|
| Style slides toward generic photoreal over a batch | Model default pulls back to its training centre [J] | Global key first; attach the style frame; EXCLUDE medium nouns; R17 |
| Faces in a stylised film turn semi-real in close-ups | Close-up prompts carry skin and pore words | Remove material words from identity keys; set `style_proportions` |
| Line or texture boils in video | Model re-draws texture every frame | Lower motion; on twos; still + push-in |
| Grain differs shot to shot | Grain asked for in prompts | Remove from prompts; one post preset (R18) |
| Composited text looks pasted on | Font and texture do not match the style | Lettering spec; add grain or paper after compositing |
| The creature becomes a stock design | Regression (B5 §7.5) | Material words, silhouette references, scale object; LoRA |
| Style changed after sheets were made | Lock skipped | Redo sheets; never skip checkpoint B |
| A named reference leaks into a prompt | Copied from notes | D4-V17 validator; rewrite as descriptors |

---

## 13. Worked example: *The Catch*

**Given.** B1 §9.2 sets 2.39:1 and spherical lenses: 35 and 50 mm for human scenes, 85 mm from the confession on for dialogue singles and the final reflection two-shot, 24 mm in three places only (the cage, wides of the ship's spaces, the figure in Iona's room), and a macro lens for reserved inserts; it bans slow motion, dolly zoom, Dutch tilt and orbit, and reserves the symmetrical profile two-shot for the two reflection moments. B2 §8.4 codes red as a limit and its cost, green as fits, allowed, go (the mint is the one inversion), yellow as the painted line, never a light. SF is nonrealism in A1's sense, so a stylised treatment is allowed in principle.

### 13.1 The three directions (draft descriptors)

**(a) Photoreal, clinical, spherical, 2.39 (library default).** Medium `photoreal_film`. Descriptors: "photographic live-action image"; "clean spherical lens, straight lines stay straight"; "natural skin with pores and fine lines"; "real materials with visible wear, grime and texture"; "true blacks with detail in the shadows"; "neutral whites"; "background detail readable"; "clean, sharp highlights"; "muted colour except named objects". Post: fine grain, subtle halation on practicals only, 24 fps. (Fact-check edit: the draft's "real materials: wet brick, oily steel, worn cotton" named the tunnel's materials, which would pull brick into the quarantine scenes; scene materials belong in B2's look keys.)
*Compiled global look key (45 words):* "Photographic live-action image; clean spherical lens, straight lines stay straight; natural skin with pores and fine lines; real materials with visible wear, grime and texture; true blacks with detail in the shadows; neutral whites; background detail readable; clean, sharp highlights; muted colour except named objects." (The scene look keys then drop C3's "realistic film look" endings.)

**(b) Ink graphic novel with B2's motif code.** Medium `ink_graphic`. Descriptors: "hand-inked graphic-novel illustration"; "bold black brush lines of varying weight"; "large solid black shadow shapes"; "paper-white highlights"; "fine hatching only in mid-tones"; "flat grey ink washes"; "colour only as small flat spot areas of red, green or yellow on the objects that carry them"; "adult faces with realistic proportions drawn in few lines"; "visible paper texture". Post: on twos, fixed paper texture, no grain. B2's colour script survives as value (1 to 5) in grey washes; saturation becomes the presence or absence of spot colour, so the fire (sequence 18, B2's single saturation peak) is the only time red fills a frame [J].
*Compiled global look key (56 words):* "Hand-inked graphic-novel illustration; bold black brush lines of varying weight; large solid black shadow shapes; paper-white highlights; fine hatching only in mid-tones; flat grey ink washes; colour only as small flat spot areas of red, green or yellow on the objects that carry them; adult faces with realistic proportions drawn in few lines; visible paper texture." EXCLUDE: "photograph, 3D render, colour painting".

**(c) Tactile miniature, stop-motion.** Medium `stop_motion`. Descriptors: "handmade stop-motion miniature"; "puppets with sculpted, slightly matte faces and faint fingerprint texture"; "costumes of real woven fabric at small scale"; "sets built from painted wood, card, wire mesh and small real bricks"; "hand-painted surfaces with small visible imperfections"; "light falls off quickly across short distances, as on a small set"; "focus falls off quickly behind the subject"; "surfaces flicker very slightly from frame to frame". Post: on twos, no grain. (Fact-check edit: the draft had seven descriptors, below the minimum of eight, and two that broke the rules in Section 5: "small real lamps lighting the set" named a light source, which belongs to B2's look keys, and "shallow focus in close shots, deeper in wides" depended on shot size.)
*Compiled global look key (66 words):* "Handmade stop-motion miniature; puppets with sculpted, slightly matte faces and faint fingerprint texture; costumes of real woven fabric at small scale; sets built from painted wood, card, wire mesh and small real bricks; hand-painted surfaces with small visible imperfections; light falls off quickly across short distances, as on a small set; focus falls off quickly behind the subject; surfaces flicker very slightly from frame to frame." EXCLUDE: "photograph, live action, cartoon, smooth CG".

### 13.2 The three test shots

**T1. SC01, bolt-hole insert** (hard shot: evidence detail).
> "Two brake brackets, empty. Four bright bolt holes in each. Nothing between the brackets and the guide rail."
> "She puts a finger into one of the holes. Feels the thread. Still sharp."

B1 Ex1: static macro insert. Light: the flashlight beam rakes the bracket from the side B2's plan fixes (B2 Ex1: "entering from frame-right"; the B1 digest's Ex1 prompt says "torchlight from the left"; resolve before the test, and use the same side in all three directions). Readability criterion: "bright" holes and "still sharp" thread must say *removed recently* in the first second.
- (a) Macro detail and glint suit photoreal; risk: the fingertip melts into the hole (hands, C3 §13C); fix with a still + small push-in.
- (b) Brightness becomes paper-white inside black; "sharp" thread needs a few precise lines; risk: hatching turns the hole into noise. Held panel acceptable.
- (c) At macro scale a miniature reveals its material: clay threads read as soft, which contradicts "Still sharp." Needs a designed hero prop at larger scale [J]. This is the direction's weakest test.

**T2. SC10, the reflection two-shot** (face shot: identity and mirror).
> "Iona holds it up. Saye holds up hers."
> "They stand facing each other across the table like a woman and her reflection, each with the wrong hand in the air."
> "Saye's wedding ring. On her right hand."

Era B: the world and Saye are MIRRORED, Iona NORMAL (C2 §7.3). Method C2 W3: generate Saye in her kitchen, flip, add Iona unflipped; rings in separate close-ups. B1 reserves the symmetrical profile two-shot for this moment. The scene has no scripted lettering, so the test adds one mirrored world label on Saye's medical case, composited and flipped [design choice, test only, removed afterwards] to judge mirror-text readability. Criteria: two different women (B5 lineup: Saye light grey, Iona faded mid-blue), hands on the right image sides, ring close-ups readable, and, if the mint is in frame, its green reads in the lamplight rather than as a dark shape against the window (B2 §5.4).
- (a) Strongest on faces and rings if drift is controlled; highest uncanny risk in the matched profiles.
- (b) The symmetric composition becomes a graphic panel, which the ink form does well; faces must keep B5's distinguishers as black masses (Saye's short neat hair against Iona's low knot); the mint is the single green spot, which suits B2's inversion; the label becomes hand-lettered.
- (c) Puppet faces make the mirror pose read clearly; rings at puppet scale need inserts; printed labels at prop scale read well [J].

**T3. SC15, the figure on the tablet** (hard shot: creature and in-story footage).
> "Something tall and black stands beside his bed. It did not come through the door. It is simply there, in the space between one moment and the next."
> "THE FIGURE. Its head sits low between its shoulders. Where a face would be, a pale strip slides across, vanishes, slides across again."

B1: the feed is its own 16:9 clip inside 2.39, high corner, wide, static, desaturated, with a small mirrored overlay (phase B); the figure appears by a cut between frames (C3 Rec6). B5: about 2.4 m, block with a sunken dome, very large hands, matte black, pale strip that is soft and never red. Criteria: no regression; the reversed overlay (a few large characters, composited) readable as backwards; the appearance is a cut, not a fade. Use B5's identity key ("A towering matte-black machine shaped like a person, taller than a doorway, a low domed head sunk deep between high broad shoulders, a clear curved face cover with a soft pale strip behind it, very large hands."), not C3's illustrative key, which says "built like an armoured deep-sea diving suit" and so asks for the very regression B5 §7.5 warns against.
- (a) Regression risk "diver or robot" (B5 §7.5); rim light against the lighter wall (B2 R25) holds the silhouette.
- (b) A matte black mass is native to ink (a solid black shape); the risk becomes superhero armour or mecha if panel lines appear [J]. The pale strip as the one soft grey inside the black may read more clearly than in photoreal. R9: the feed stays ink, drawn coarser and in grey only.
- (c) Risk of a toy. B5 M11 warns, about the animal inside the figure, against a design that "would sell as a plush"; in miniature the same risk reaches the figure itself, because puppets read as handmade and small [J]. Fear depends on scale against the door, which miniature sets show well [J]. Check against B5's stock-monster rule: the pale strip must not become "a sweeping light bar"; it is "soft, pale matter behind glass" and "never red".

### 13.3 Score sheet (to be filled by the user after the test)

Score each shot on the six criteria of Section 7.2 (0, 1 or 2 each; up to 12 per shot). The three shots cover Section 7.1's roles this way: T2 is the face shot, T3 is the wide (the feed is a wide, high-corner frame) and also the film's defining hard shot, T1 is a second hard shot. **Total for this film = T1 + T2 + 2 × T3** (maximum 48) [J].

| Direction | T1 (R/I/M/Mo/Mt/C) | T1 sum | T2 (R/I/M/Mo/Mt/C) | T2 sum | T3 (R/I/M/Mo/Mt/C) | T3 sum | Total /48 | Any 0 on Identity or Mirror? |
|---|---|---|---|---|---|---|---|---|
| a photoreal | / / / / / | | / / / / / | | / / / / / | | | |
| b ink | / / / / / | | / / / / / | | / / / / / | | | |
| c stop-motion | / / / / / | | / / / / / | | / / / / / | | | |

Key: R = readability, I = identity, M = mirror and text, Mo = motif survival, Mt = motion, C = cost.

**Predictions, not results** [J]: (c) is likeliest to fail T1; (b) is likeliest to win T3 and to hold the motif code most cleanly; (a) keeps the library's B1 and B2 defaults unchanged and carries the widest model support for dialogue (C1 R1). **Recommendation:** keep (a) as the default unless (b) scores higher on T3 and at least equal on T2. If (b) wins, apply Section 9's ink column: B2's kelvin wording becomes shadow shapes and spot colour; B1's 85 mm step change becomes "flat, compressed perspective" from the confession on.

### 13.4 Period distance (D17 hands this decision to D5)

D17 sets `period: near_future` from the script's devices (tablets, security feeds, wrist displays, a courier that vanishes) and leaves the distance from today to this file. **Proposal [J, user decides]:** `near_future_subtle`. Everything ordinary looks like today (brick, freight lifts, night buses, a kitchen with a pot of mint); only the devices the story needs are advanced, and they are designed as plausible products, not as "sci-fi" (D12 builds their screens). Reason: the film's wrongness is handedness in a world the audience trusts (R1); a visibly futuristic world would give the audience a second, competing kind of strangeness. In the ink and stop-motion directions the same rule holds: devices are drawn or built as ordinary objects.

**For the writer/user:** which direction; whether the reflection label stays as a design choice (it is not in the script); whether the tablet feed may drop to grey-only in the ink direction; whether `near_future_subtle` is right, or the world should look further from today.

---

## 14. Worked example: *The Long Places*, the oil-lamp scenes

**Given.** B2 Ex6: small oil lamps, about 1,800 to 1,900 K; soot-black ceilings in every earlier room make a small hard pool; in the finished room the pale ceiling bounces the same flame; the third shape stays within about one stop of the wall, with no rim and no eye light.

**Text.**
> "She filled each small lamp to the first knuckle of her thumb, no further, from a tin can that smelled of the press and of some older oil than this year's."
> "over each niche the ceiling was black, and the black had depth, layer under layer under layer"
> "The room the lamp stood up was long and low and rounded at every corner, and it was finished."
> "the ceiling was pale as the day of its cutting, and unsooted, and every ceiling Nilay had ever met in that hill wore black like a surname."
> "at the hem of the light, where the polish gave back more than the flame had to give, a third shape sat, or the wall sat."

**Naturalistic** (`photoreal_film`): the change from sooted to unsooted rooms is pure physics: same flame, more bounce. The audience reads "finished" without being told [J]. Risks: faces of an elderly woman (Melek, seventy-eight) in near-darkness hit the uncanny zone; the model adds rim light to the third shape (B2 §12 house look), which would "certify" it.

**Painterly** (`painterly`): brushwork suits the novella's lyrical register. Risks: painterly models spread warm glow over everything, erasing the black ceilings, and they outline figures, so the third shape either vanishes or gets a halo; value control within one stop is harder in paint texture [J].

**Rule.** If the scene's meaning is a physical change in light (sooted to unsooted, one stop at the hem of the light), then naturalistic, because the medium must be able to hold exact values; painterly is allowed only where the text is voice rather than event [J].

**Proposal [J, user decides]:** naturalistic for the investigation chapters; the keeper's italic letters ("*To the one who keeps the lamps after me:*") as the one `style_exception` in a restrained painterly style, since they are a second narrative voice (R10), with the same lamp colour so the two styles share the flame.

**Test.** Three shots per direction: the Ch. I warmth scene ("The lamp at her left burned small and even."; B1 Ex7 static profile, 75 mm), a sooted niche wide, and the finished room with the third shape. Pass if the third shape stays uncertain and the ceilings read black versus pale.

---

## 15. Conflicts and open questions

- **C3's look keys** carry style words ("realistic film look"); this file moves them to the global key. C3's examples need editing once the style is locked.
- **Midjourney in C1 §5 vs C2 Rule 8:** C1 routes stylised shots through Midjourney stills; C2 forbids automating it. Resolution here: Midjourney for look development and by-hand stills only; production batches on API models with the approved stills as references.
- **B1/B2 light side in the SC01 insert** remains open (B2 digest conflict); the style test needs one side.
- **Cadence vs B1's real-time rule:** on twos does not change speed, so B1's ban on slow motion is unaffected; camera moves on twos judder (R21).
- **C3's illustrative figure key vs B5:** C3 §22.0 describes the figure as "built like an armoured deep-sea diving suit in matte black plates", which is the regression B5 §7.5 names. Use B5's revised key (Section 13.2, T3) in every test and production prompt; C3's example should be updated.
- **Post order vs D8:** this file's first draft composited before cadence and upscale; it now follows D8's order (time, size, composites, colour, grain; D8 §0 and core principle 3 in §2). Grain is added once at timeline level (D8-R34). D8's `finish.grain` holds the exact method and strength; this file's `grain_level` holds the intent.
- **C2 Rule 25 vs B1 §5 on aspect ratio:** C2 asks for images "in the delivery aspect ratio"; B1 allows 16:9 composed for a 2.39 crop when a tool cannot make 2.39. Resolution in Section 7.1: 21:9 where offered, otherwise 16:9 with the central band kept clear.
- **D13 cost classes:** D13 classes the `stylised` shot need as `easy`; R24 limits that tag to stylised sequences inside another style.
- **D17 period:** D17 hands the distance from today to this file; Section 13.4 proposes `near_future_subtle` for the user to confirm.
- **D4 field name:** D4 proposes shot- and bible-level `human_notes`; this file uses film-level `style_human_notes`. D4-V17 scans both.
- **B1 and B2 "P" numbers:** the B1 and B2 digests use "P#" both for core principles and for procedures (B2 P7 is "design what stays dark" and also the four-shot probe). This file cites the probe as B2 §13.5 to avoid the clash.
- **Unverified:** Midjourney `--sw` range on V8.2 (official figure is from the V6-era announcement; the docs page refused automated reading); Ray3 Modify on the API; lip sync in stylised faces and in performance transfer onto stylised characters; per-style retake ratios and the relative costs in Section 3.3 (no published figures found); current GPT Image 2.5 living-artist policy; whether free DaVinci Resolve includes a usable film-grain effect.

---

## Sources

All web sources checked 2026-09-27.

- [S1] Google Cloud, "Video generation prompt guide" (Veo), last updated 2026-09-25: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide (checked 2026-09-27) [V]
- [S2] Midjourney, "Niji V7!" (9 January 2026): https://updates.midjourney.com/niji-v7/ (checked 2026-09-27) [V]
- [S3] Midjourney, "V8 Alpha" (17 March 2026): https://updates.midjourney.com/v8-alpha/ (checked 2026-09-27) [V]
- [S4] Midjourney, "Style references for V7": https://updates.midjourney.com/style-references-for-v7/ (checked 2026-09-27) [V]
- [S5] Midjourney, "Changelog 8/20/26" (posted 21 August 2026): https://updates.midjourney.com/changelog-8-20-26/ (checked 2026-09-27) [V]
- [S6] Midjourney, "Style Ref v2" (15 March 2024; `--sw` default 100, towards 1000 for more influence): https://updates.midjourney.com/style-ref-v2/ (checked 2026-09-27) [V]. The current docs page, https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference, refused automated reading [U].
- [S7] Runway, "Aleph 2.0" product page: https://runway.com/product/aleph-2 (checked 2026-09-27) [V]
- [S8] Runway Help, "Aleph 2.0 Prompting Guide" (refused automated reading; superseded here by S24): https://help.runwayml.com/hc/en-us/articles/52150503729171-Aleph-2-0-Prompting-Guide (checked 2026-09-27) [U]
- [S9] Luma AI API docs, "Modify Video": https://docs.lumalabs.ai/docs/modify-video (checked 2026-09-27) [V]
- [S10] Luma AI, "Ray3 Modify" (18 December 2025): https://lumalabs.ai/news/ray3-modify (checked 2026-09-27) [V]
- [S11] fal, "LTX 2.3 Trainer (V2), Text-to-Video": https://fal.ai/models/fal-ai/ltx23-trainer-v2/t2v (checked 2026-09-27) [V]
- [S12] fal, "Wan-2.2 LoRA Trainer": https://fal.ai/models/fal-ai/wan-22-trainer (checked 2026-09-27) [V]
- [S13] Blackmagic Design, "DaVinci Resolve Studio": https://www.blackmagicdesign.com/products/davinciresolve/studio (checked 2026-09-27) [V]
- [S14] FFmpeg, "FFmpeg Filters Documentation" (fps, noise, hflip): https://ffmpeg.org/ffmpeg-filters.html (checked 2026-09-27) [V]
- [S15] Wikipedia, "Inbetweening": https://en.wikipedia.org/wiki/Inbetweening (checked 2026-09-27) [V with S16]
- [S16] iD Tech, "What Does Animating on Ones, Twos & Threes Mean?": https://www.idtech.com/blog/what-does-animating-on-ones-twos-and-threes-mean (checked 2026-09-27)
- [S17] Wikipedia, "Anti-halation backing": https://en.wikipedia.org/wiki/Anti-halation_backing (checked 2026-09-27) [V with S18]
- [S18] Lomography, "What is the Anti-Halation Layer in Film?": https://www.lomography.com/magazine/352787-what-is-the-anti-halation-layer (checked 2026-09-27)
- [S19] M. Mori, "The Uncanny Valley" (1970), authorised translation by K. F. MacDorman and N. Kageki, IEEE Spectrum, 12 June 2012: https://spectrum.ieee.org/the-uncanny-valley (checked 2026-09-27) [V]
- [S20] E. Zell, C. Aliaga, A. Jarabo, K. Zibrek, D. Gutierrez, R. McDonnell, M. Botsch, "To stylize or not to stylize? The effect of shape and material stylization on the perception of computer-generated faces", ACM Transactions on Graphics 34(6), 2015: https://dl.acm.org/doi/10.1145/2816795.2818126; findings quoted from the authors' group page https://cg.cs.tu-dortmund.de/research/faces/faces.html (checked 2026-09-27) [V]
- [S21] OpenAI, "Addendum to GPT-4o System Card: Native image generation", 25 March 2025: https://cdn.openai.com/11998be9-5319-4302-bfbf-1167e093f1fb/Native_Image_Generation_System_Card.pdf (checked 2026-09-27) [V]
- [S22] Netflix Technology Blog, "AV1 @ Scale: Film Grain Synthesis, The Awakening" (July 2025; page refused automated reading, read via S23): https://netflixtechblog.com/av1-scale-film-grain-synthesis-the-awakening-ee09cfdff40b (checked 2026-09-27) [U alone; V with S23]
- [S23] IBC, "Netflix rolls out AV1 Film Grain Synthesis for classic movies" (9 July 2025): https://www.ibc.org/content-management/news/netflix-rolls-out-av1-film-grain-synthesis-for-classic-movies/22018 (checked 2026-09-27) [V]
- [S24] Runware Docs, "Runway Aleph 2.0: Editing video": https://runware.ai/docs/models/runway-aleph-2-0/guides/editing-video (checked 2026-09-27) [V for the API route]
- [S25] Runway, "Introducing Act-One" (22 October 2024): https://runway.com/research/introducing-act-one (checked 2026-09-27) [V]
- [S26] TechCrunch, "OpenAI's viral Studio Ghibli moment highlights AI copyright concerns" (26 March 2025): https://techcrunch.com/2025/03/26/openais-viral-studio-ghibli-moment-highlights-ai-copyright-concerns/ (checked 2026-09-27) [V]
- [X1] Local test, 2026-09-27: FFmpeg 7.0.2 (static build) on a generated 2 s, 24 fps clip; `hflip`, `fps=12,fps=24` (48 frames, 24 distinct, each twice), `fps=8,fps=24` (16 distinct, each three times), `noise`, and the crop-based weave all ran without error.

**Library files:** A1 §5 (nonrealism); D8 §0, §2 principle 3, R28, R34, R56 (post order, grain); D12 §5.1 (UI style guide); D13 §6.1 (cost classes); D17 §6.1 (period); B1 §4.4, §9.2, §15, Ex1, Ex7, P3, R22; B2 §4.8, §5.4, §8.4, §12, §13, P6, P7, Ex6, R4, R13, R25; B5 §2.2, §6.2, §7.5, M11, R10; C1 §1, §4, §5, §10, R1, R6, R8, R13, R19, R21; C2 §2.1, §3.1, §3.4, §3.6, §6.5, §7.3, Rules 8, 9, 10, 14, 23, 25, 26, R2, R6, W3; C3 §3A, §13C, R1, R5, L14, Rec6; C4; C5 (`global_look_key`, checkpoint B, field authority); D4 principle 2, R5, D4-V17.

**Test texts:** *The Catch*, workshop revision, 25 September 2026 (SC01 lines 26 and 28, SC10 lines 426, 428 and 436, SC15 lines 850 and 852 of the supplied file); *The Long Places*, revised final (Ch. I lines 7, 47 and 79; finished room lines 587 and 597).
