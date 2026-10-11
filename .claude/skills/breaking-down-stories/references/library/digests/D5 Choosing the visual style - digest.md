# Digest D5: Choosing and locking the film's visual style (27 Sept 2026)

Source: `research/D5_visual_style_bible.md` (fact-checked 27 Sept 2026). R# = rule; §2.n = principle; P# = procedure (section 4 here); **[V]** verified; **[U]** unverified; **[J]** judgment. Re-check tool facts after 30 days (C1 §0).

## 1. Scope

1. Helps the user choose medium and style (photoreal, CG, stop-motion, 2D, painterly, ink, hybrid) at checkpoint B, before any sheet or keyframe, by testing three directions on three hard shots.
2. Fixes it in one style bible compiled into C5's `global_look_key`, sets post grain, halation, weave and cadence, and keeps film, artist and studio names out of prompts.
3. Lists what style changes in B1, B2, B5, C1, C2, C3; worked on *The Catch* and *The Long Places*.

**Terms** [§1]: *style* = medium plus fixed rendering; *look* = one scene's light and colour; *descriptor* = one short visible phrase; *on twos* = each picture held two frames [V]; *halation* = red-orange glow round highlights [V]; *regression* = a design pulled back to a stock one; *LoRA* = small add-on trained on your images (open models only); *boiling* = lines redrawing every frame.

## 2. Rules

**Principles**
1. [§2.1] If choosing a style, then start from what the audience must believe, then check model support, because style is a story decision first.
2. [§2.2] If a shot prompt, identity key or scene look key contains style words, then move them to the global key, because style lives in one place.
3. [§2.3] If a shot moves, then animate an approved still in the style, because video models keep a style better than they invent one.
4. [§2.5; R12] If comparing directions, then judge by the face and hard shots, not the prettiest wide, because hard shots set the film's cost.
5. [§2.6] If texture or cadence is wanted, then add it in post, one setting for the film, because generated texture varies per clip.
6. [§2.7] If the style changes another file's wording, then keep that file's story reason, because style changes how, not why.
7. [§2.8] If the style is not approved at checkpoint B, then make no sheet, style frame or keyframe, because each would be redone.

**Choosing**
8. [R1] If the story's force comes from the real world going slightly wrong, then choose photoreal, because wrongness reads only against a trusted baseline [J].
9. [R2] If the source is nonrealist (fantasy, SF, fable, myth), then consider stylised media and allow frontal, iconic framing, because nonrealism changes what audiences accept (A1 §5).
10. [R3] If the film has many dialogue close-ups and no budget for a face LoRA, then prefer simplified faces (2D, ink), because shape drives perceived realism and material drives appeal [V].
11. [R4] If native-audio lip sync is essential, then photoreal or CG; if stylised anyway, then plan dialogue as performance transfer and test one spoken line, because transfer onto different proportions is documented [V] but stylised lip accuracy is not [U].
12. [R5] If generation budget is under $1,000, then prefer ink, painterly or stop-motion, because held stills with a slow push-in read as the style there [J].
13. [R6] If a non-human must frighten then earn pity, then test it in every style, because each style has its own regression target [J].
14. [R7] If the script has violence, then do not pick a cartoon style to pass filters, because an anime duel was refused as graphic violence (C1 §4) [U].
15. [R8] If licensed-data routes are required (Marey, Firefly Video), then test styles there first, because they have fewer consistency tools [J].
16. [R9] If in-story footage appears, then keep the film's medium with the device's grammar (B1 R22), because a switch reads as another film [J].
17. [R10] If a second style is wanted (memory, letters, dream), then write a `style_exception` with a story reason and short bible, at most two, because a break works by rarity [J].
18. [R11] If a hybrid is proposed, then only for a two-world story (B2 R13), with a join rule, because hybrids double consistency work [J].
19. [R23] If D17 sets `near_future` or a period, then record `period_distance` and put futurity in designed props and devices, never in the global key, because "futuristic" or "sci-fi" pulls in the stock neon look (B2 §12) [J].
20. [R24] If the whole film is stylised, then tag shots by their real need, not C1's `stylised` (D13 `easy`), because the film would be under-budgeted [J].

**Names and references**
21. [R13] If anyone proposes a film, director, cinematographer, artist, studio or franchise as a reference, then put the name in `style_human_notes` and translate it into descriptors (P3), because names pull models toward protected frames and trigger filters (D4 R5); ignore Google's "Pixar-like 3D animation" examples [V], and ban studio names even though OpenAI permits "broader studio styles" [V].
22. [R14] If a style reference image is attached, then it must be generated here, the user's own photo, or licensed for AI input, never a film still or another artist's work, because attachments are copied more closely than names [J].
23. [R15] If a Midjourney style code is used, then record code, model version, `--sv` and `--sw`, and keep the approved images as the real references, because codes are version-bound [V] and Midjourney cannot be automated (C2 Rule 8).

**Holding the style**
24. [R16] If the acceptance probe fails twice, then change direction rather than add descriptors, because a style needing constant rescue fails across 300 shots [J].
25. [R17] If more than 1 frame in 10 drifts in style despite references, then train a style LoRA (20 to 40 images, or 10 to 50 clips; fal LTX 2.3 about $12 per default run [V]; on Wan 2.2 train the I2V kind [V]) or move those shots to still + push-in, because references alone are not holding [J].

**Post**
26. [R18] If film emulation is wanted, then allow one prompt texture phrase at most ("fine even film grain"), rest in post, because post is identical and removable [J].
27. [R19] If delivering by streaming, then keep grain fine, because grain is "notoriously difficult to compress" [V]; YouTube: 15 to 20 Mbps at 1080p (D8-R56).
28. [R20] If halation is used, then subtly, round practicals only, never on faces, because everywhere it is decoration [J].
29. [R21] If 2D or stop-motion, then generate smooth motion, convert cadence in post and slow camera moves, because prompted "on twos" is unreliable and moves on twos judder [J].
30. [R22] If anamorphic is proposed, then check B1 §4.4, because models return flares, not the squeeze [J].
31. [§5] If writing a descriptor, then name something visible in every shot, positively, with no scene light, colour or material, emotion, name or booster ("8K"), one word per concept, because the key goes into every shot unchanged [J].
32. [§14] If a scene's meaning is a physical change in light, then choose naturalistic, because the medium must hold exact values; painterly only where the text is voice, not event [J].

## 3. Breakdown fields

`authored` fields carry `decided_by` and `locked` (C5).

| level | field_name | meaning | allowed values / example |
|---|---|---|---|
| film | `style_medium` | The medium | `photoreal_digital` / `photoreal_film` / `cg_3d` / `stop_motion` / `anime_cel` / `painterly` / `ink_graphic` / `hybrid` |
| film | `style_bible_id` | Pointer to the bible | `SB-CATCH-01` |
| film | `rendering_descriptors[]` | 8 to 15 frozen phrases | strings |
| film | `global_look_key` | Compiled bible, pasted first | 40 to 80 words |
| film | `grain_level`, `grain_made_in` | Texture intent; D8 `finish.grain` holds method and strength | `none` / `fine` / `medium` / `heavy`; `post` / `prompt` |
| film | `halation` | Highlight glow | `none` / `subtle_practicals` / `strong` |
| film | `lens_character` | Optical signature | `spherical_clean` / `spherical_vintage` / `anamorphic` / `drawn_flat` / `miniature_macro` |
| film | `motion_cadence`, `delivery_fps` | Cadence and rate | `live_24` / `on_twos` / `on_threes` / `mixed_ones_twos`; 24 / 25 |
| film | `period_distance` | Distance from today (R23) | `today` / `near_future_subtle` / `near_future_marked` / `period:<year>` |
| film | `lettering_style` | Insert text look; feeds D12 | `printed` / `hand_lettered` |
| film | `style_reference_images[]` | Approved style images | {file, source: `generated` / `owned` / `licensed`, approved} |
| film | `style_codes[]` | Tool style codes | {tool, code, model_version, sv} |
| film | `style_lora` | Trained style add-on | {base, trigger, file, licence} / `none` |
| film | `banned_style_words[]`, `exclude_medium_nouns[]` | Never sent; negative-field nouns | lists |
| film | `post_chain[]` | Ordered post steps (D8 order) | `cadence`, `upscale`, `flip`, `composite`, `grade`, `grain`, `halation`, `weave` |
| film | `style_directions_tested[]` | Test record | {id, bible, shots, scores, total_of_48, verdict} |
| film | `style_locked` | Approved at checkpoint B | `yes` / `no` |
| film | `style_human_notes` | Named inspirations; never compiled (D4-V17) | text |
| sequence | `style_exception` | Second style with reason (R10) | {reason, bible_id} / `none` |
| shot | `style_override` | Shot departs from film style | `none` / `diegetic_device` / `exception` |
| shot | `style_drift_check` | Checked against style frame | `pass` / `fail` / `not_checked` |
| character | `style_proportions` | Overrides to B5's face spec | {head_heights, eye_size, nose, mouth} |
| generation job | `global_look_key_version`, `style_refs_attached[]` | What was sent | `SB-CATCH-01 v2`; files |

## 4. Procedures

**P1. Selection test: three directions, three shots** [§7.1]. Cost about $20 to $50 [J]; user time 2 to 3 hours.
1. Paste into the LLM: logline and themes (A2), B1's camera system, B2's colour script and motif table, B5's design theses and identity keys (provisional), and D5.
2. Ask: "Using D5 Sections 3 and 4, propose three style directions for this film: one photoreal, and two others that fit the story. For each, write a draft style bible (Section 5) with 8 to 15 descriptors and a compiled global look key. Put any film or artist names only under HUMAN NOTES. For each, say in one sentence which story reason it serves and which failure in table 4.2 it risks most."
3. Ask: "Pick the three test shots from the breakdown and quote their script lines exactly." One face, one wide, one hard shot.
4. Stills: four candidates per direction and shot at 2K, 21:9 where offered, else 16:9 with heads, hands and text out of the top and bottom eighths. Prompt order, blocks pasted unchanged:
   ```
   [GLOBAL LOOK KEY of this direction]
   [SCENE LOOK KEY (C3 `look_key`, written from B2's lighting plan), with its style words removed]
   [IDENTITY KEYS of the people or creature in frame (B5)]
   [SHOT: shot size, angle, lens effect in this direction's words (Section 9), subject, action, end state]
   ```
   No style reference yet.
5. Two short video drafts per shot from the best still, cheap tier (C1 R13), motion only (C3 R1).
6. Run each direction's post chain (P5).
7. Score (P2); the LLM fills a first pass, the user overrides.
8. The user picks one direction, or one merge ("A's line with C's colour"), re-tested on the hard shot only.
9. Lock: `style_locked: yes`, `decided_by: human`.

**P2. Scoring** [§7.2]. Each criterion 0 = fails, 1 = usable with fixes, 2 = holds: Readability (in the first second); Identity (no regression); Mirror and text (after compositing and flipping); Motif survival; Motion (no boiling or melting); Cost (2 = one or two takes, 1 = three or four, 0 = five or more). Per shot up to 12. Direction total = face shot + wide + 2 × hard shot (max 48). A 0 on Identity or Mirror disqualifies unless a named fix passes a re-test; within 4 points, the user chooses on taste.

**P3. Translate a named reference** [§7.3].
1. The user names what they like.
2. LLM: "Without using any names, list what is visible in that style under these headings: line, edge, surface texture, black level, highlight behaviour, colour range, depth of field, grain, proportion of faces, motion. Give one short phrase per heading."
3. Keep 8 to 15 phrases that serve the story; drop anything describing a specific character, costume, logo or composition.
4. Write the name and what was taken into `style_human_notes`.

**P4. Fill and compile the bible** [§5]. Fill every line (write `none`, never delete). Template, exactly:
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
Compile prompt: "Compile the global look key from this style bible. Start with the medium phrase, then the descriptors in their frozen order, joined with semicolons. 40 to 80 words. No light sources, times of day, colours of particular scenes, emotions, names or banned words. Return the key and its word count." Version it (`SB-<PROJECT>-01 v1`); every change raises the version. Then strip style words from scene look keys (C3's "realistic film look" endings).

**P5. Post chain, free route** [§8.3]; FFmpeg lines tested on 7.0.2 [V, X1]; the LLM can run them.
0. Frame rate must be 24: `ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 in.mp4` prints `24/1` (untested; `ffmpeg -i in.mp4` also shows "24 fps"). If not, D8's rate step first.
1. On twos: `ffmpeg -i in.mp4 -vf "fps=12,fps=24" -c:v libx264 -crf 12 -preset slow -c:a copy out.mp4`. On threes: `"fps=8,fps=24"`. Mixed: convert only the slow parts.
2. Upscale if needed (D8).
3. Flip mirror-era shots: `ffmpeg -i in.mp4 -vf hflip -c:v libx264 -crf 12 -preset slow -c:a copy out.mp4`.
4. Composite inserts and text (C1 R6, D6) in the bible's lettering; add paper or grain over them.
5. Grade each sequence to its style frame (B2 §13.4; D8-R28).
6. Grain once, whole film or timeline (D8-R34): `ffmpeg -i film.mp4 -vf "noise=alls=6:allf=t" -c:v libx264 -crf 12 -preset slow -c:a copy film_grain.mp4`; brightness-only: `"noise=c0s=6:c0f=t"`. Starting strengths [J]: fine 4 to 6, medium 8 to 12, heavy 15 to 20 at 1080p; judge on one dark and one bright shot.
7. Optional gate weave (photoreal film only): `ffmpeg -i film.mp4 -vf "crop=iw-8:ih-8:4+2*(random(1)-0.5):4+2*(random(2)-0.5),scale=1920:804,setsar=1" -c:v libx264 -crf 12 -preset slow -c:a copy out.mp4` (use your film's size); drop it if it reads as shake.
8. Halation: no simple FFmpeg route. Paid: Resolve Studio 21 ($295) Film Look Creator adds "film stocks, halation, grain, gate weave, split toning and more" (Studio-only) [V].

**P6. Acceptance probe, then style frames** [§7.4].
1. B2's four-shot probe (B2 §13.5: wide, medium, close-up, reverse) in the locked style with one approved style reference; check B2's items plus descriptors visible, faces, grain and cadence identical after post.
2. Fails once: fix descriptors or reference; fails twice: second-ranked direction (R16).
3. Then C2 style frames per sequence (§6.5), then asset sheets.

**Post values** [§8.2, J]: photoreal film: grain 6 to 10, subtle halation, slight weave; stylised: on twos or holds, no grain.

## 5. Checklists

**Checkpoint B, style lock** [§11]
- [ ] Three directions tested on a face shot, a wide and a hard shot; scores and totals recorded.
- [ ] Bible filled on every line; 8 to 15 positive, visible descriptors; no names outside `style_human_notes`.
- [ ] Global look key compiled and versioned; scene look keys stripped of style words.
- [ ] Post chain tested on one dark and one bright shot.
- [ ] Probe passed before any sheet is made.
- [ ] Style references generated, owned or licensed; none is a film still or someone's artwork.
- [ ] Style exceptions (if any) have story reasons; at most two.
- [ ] `period_distance` set; futurity in props and devices, not in the key.
- [ ] Lettering spec handed to D12.
- [ ] If stylised: one spoken line tested; hard shot scored at least 1 on Identity.

**Per batch** [§11]
- [ ] Slideshow in story order: same line weight, texture, proportions and black level.
- [ ] No descriptor missing in more than 1 frame in 10 (else R17).
- [ ] Inserts drawn in the bible's lettering.

**Failure scan** [§12]: drift to generic photoreal (key first, style frame, EXCLUDE, R17); semi-real faces in close-ups (drop skin words, set `style_proportions`); boiling (less motion, on twos, still + push-in); uneven grain (post only); pasted-on text (texture over insert); stock creature (materials, silhouette refs, LoRA); a leaked name (D4-V17).

## 6. Saying it to AI models

- **Order** [§5]: as P1 step 4; the medium phrase opens the prompt (C3 §3A).
- **Effect, not lens** [§9, J]: 2D and ink: long lens = "flat, compressed perspective", wide = "strong converging perspective, close to the face".
- **Light by style** [§9, J]: 2D "hard-edged shadow shapes, two tones on the face"; ink "solid black shadow shapes, paper-white light", motif colours as spot colour; painterly warm and cool as paint.
- **Faces by style** [§9, J]: anime about 6.5 to 7.5 head heights, larger eyes, simplified nose, distinguishers in hair silhouette, hair colour and costume shape; ink distinguishers as black masses.
- **Motion words** [§9, J]: stop-motion "small, deliberate movements"; 2D "simple, readable poses; little camera movement"; ink "held panel, slow push-in"; painterly "slow drift; minimal movement".
- **EXCLUDE nouns** [§9, J]: photoreal "illustration, cartoon, painting, 3D render"; CG "photograph, live action, clay"; stop-motion "photograph, live action, cartoon, smooth CG"; 2D "photograph, 3D render, painting"; ink "photograph, colour painting, 3D render"; painterly "photograph, 3D render, clean vector".
- **Never**: names, banned words, "on twos".
- **Tools** [§3.2]: Midjourney V8.2 keeps V7 srefs, `--sw` default 100, by hand only; Nano Banana Pro has 3 style slots, Nano Banana 2 none; Aleph 2.0 restyles 2 to 30 s clips guided by an edited first frame [V]; Luma Modify: Adhere, Flex, Reimagine [V]. Adapter example (SC01, three directions): source §9.

## 7. The Catch

**Decisions made (drafts for the user)** [§13]
- Three directions: (a) photoreal, clinical, spherical, 2.39 (library default, `photoreal_film`); (b) ink graphic novel with B2's red/green/yellow code as spot colour and B2's value script as grey washes, red filling a frame only at the fire (sequence 18); (c) tactile miniature stop-motion.
- Compiled keys in source §13.1 ((a) 45 words, (b) 56, (c) 66); (a) lost the tunnel's "wet brick" materials, (c) gained an eighth descriptor.
- Test shots (quotations verified): **T1** SC01 bolt-hole insert ("Four bright bolt holes in each." / "Feels the thread. Still sharp."); **T2** SC10 reflection two-shot ("like a woman and her reflection, each with the wrong hand in the air." / "Saye's wedding ring. On her right hand."), Saye generated and flipped, Iona unflipped, rings as inserts; **T3** SC15 figure on the tablet ("It is simply there, in the space between one moment and the next."), 16:9 feed inside 2.39, static high corner, appearance by a cut.
- Score: T1 + T2 + 2 × T3 (T3 is both the wide and the defining hard shot), max 48.
- Predictions [J]: (c) likeliest to fail T1 (clay threads contradict "Still sharp."); (b) likeliest to win T3; (a) keeps B1 and B2 unchanged. **Recommendation:** keep (a) unless (b) beats it on T3 and equals it on T2; then B2's kelvin words become shadow shapes and spot colour, and B1's 85 mm step becomes "flat, compressed perspective".
- T3 uses B5's figure key, not C3's diving-suit example; in (c), B5 M11's plush warning (about the animal) extends to the figure.
- Period: `near_future_subtle`: today's world; only story devices (wrist display, tablet, suit, courier) advanced.

**Flagged for the user**: which direction; whether the test-only mirrored label on Saye's medical case stays (not in the script); whether the ink tablet feed may be grey-only; whether `near_future_subtle` is right; the SC01 light side (B2 Ex1 frame-right versus the B1 digest's left) must be settled before the test.

**The Long Places** [§14]: naturalistic for the investigation chapters, because "finished" is shown by physics (the same ~1,800 K flame bouncing off a pale ceiling); painterly risks glow erasing the black ceilings. Proposal [J, user decides]: the keeper's italic letters ("*To the one who keeps the lamps after me:*") as the one `style_exception`, restrained painterly, same flame colour. Test: the Ch. I warmth shot, a sooted niche, the finished room; pass if the third shape stays uncertain and ceilings read black versus pale.

## 8. Conflicts and open questions

- **C3** look keys end in "realistic film look" (move style to the global key), and C3's figure key says "built like an armoured deep-sea diving suit", the regression B5 §7.5 names: use B5's key; update C3.
- **Midjourney**: C1 §5 routes stylised shots through it; C2 Rule 8 forbids automation. Resolution: look development and by-hand stills only.
- **D8**: post order now follows D8 (time, size, composites, colour, grain; grain once, D8-R34); D8 `finish.grain` holds method and strength, D5 `grain_level` the intent.
- **Aspect ratio**: C2 Rule 25 wants the delivery ratio, B1 §5 allows a 16:9 crop. Resolution: 21:9 where offered.
- **D13** classes `stylised` as `easy` (R24 limits the tag). **D17** hands period distance to D5 (proposal in 7). **D4** proposes `human_notes`; D5 uses `style_human_notes`; D4-V17 must scan both.
- **"P" numbers** in the B1 and B2 digests mean both principles and procedures; D5 cites the probe as B2 §13.5.
- **Open**: SC01 light side (B1 vs B2); on twos keeps real-time speed, so B1's slow-motion ban holds.
- **Unverified**: `--sw` on V8.2; Ray3 Modify via API; stylised lip sync; per-style retake ratios and §3.3 costs; GPT Image 2.5's living-artist rule; a usable grain effect in free Resolve.

## 9. Section map

- Header, §1, §2 (purpose, labels, fact-check note; glossary; principles) → digest 1, 2
- §3 (style catalogue, tool facts, relative cost) → 6, 2, 8
- §4 (choosing factors, failures by style, R1 to R12, R23, R24) → 2
- §5 (bible template, descriptor rules, compile prompt) → 4 P4
- §6 (named references, R13 to R15) → 2
- §7 (selection test, scoring, name translation, probe; R16, R17) → 4 P1 to P3, P6
- §8 (post rules R18 to R22, parameters, FFmpeg and Resolve) → 2, 4 P5
- §9 (downstream changes by style; adapter example) → 6
- §10 (fields) → 3; §11, §12 (checklists, failures) → 5
- §13, §14 (*The Catch*, *The Long Places*) → 7; §15, Sources (S1 to S26, X1) → 8
