# Digest C1: AI video models, what exists and what each can do (27 Sept 2026)

Source: `research/C1_ai_video_models_landscape.md` (682 lines). Brackets: R# = the file's decision rule (§6); §5 = its shot-need decision table; Rec# = recipe (§8); Ex# = worked example (§11). Evidence labels from the file: **[V]** verified (primary source or two agreeing sources), **[U]** unverified, **[J]** author's judgment. Prices are per *generated* second, checked 2026-09-27.

## 1. Scope

1. Chooses the AI video model and input mode for each shot: checked limits, prices, controls, content restrictions and retirements for every significant hosted and open-weight model on 27 Sept 2026.
2. Gives 25 decision rules, a shot-need decision table, aggregator/MCP routes so an LLM can run the models, 11 recipes, failure fixes and cost arithmetic for a 20-minute short.
3. Runs after shot design (B-series), alongside stills (C2), prompting (C3) and previs (C4); plans eight hard *Catch* shots. **Staleness rule [§0]:** more than 30 days after 2026-09-27, re-check models and prices before spending.

**Terms** [§1]: *clip* = one file a model returns; *take* = a clip made for a given shot; *retake ratio* = takes made per take kept; *start/end frame* = picture the clip must begin/end on; *keyframe* = picture pinned inside the clip; *reference image* = picture keeping a character, object or place consistent; *reference pack* = your folder of such images per asset, reused every shot; *native audio* = sound made in the same run; *extend* = continue from a clip's last frame; *control video* = rough video (e.g. grey Blender "clay" render) whose camera, poses or depth the model copies; *performance transfer* = copy a filmed performance onto a character; *plate* = background clip for compositing; *open weights* = model you run yourself; *aggregator* = one account for many makers' models; *MCP connector* = plug-in letting an LLM call a tool; *generated second* = billed second, kept or not; *overshoot* = generated length ÷ used length.

## 2. Rules

**Choosing and routing**
1. [§2, R14] If choosing a model, then choose per shot on controls (start/end frames, references, audio input, length, editing) and refusal policy, and call it through an aggregator or MCP with the model name stored in the breakdown, because the top five are within ~25 Elo and models are retired at months' notice (Sora 2: 6 months; Veo 2/3.0).
2. [R21, §3E] If a guide names a retired model, then substitute: Sora 2 → Veo 3.1, Omni Flash or Kling 3.0; Veo 2/3.0 → Veo 3.1; `gemini-omni-flash-preview` (deprecated 30 Sep 2026) → `gemini-omni-1.1-flash`; Kling 2.x/O1 → Kling 3.0; Runway Gen-3/Gen-4/first Aleph → Gen-4.5, Aleph 2.0; Luma Ray3 → Ray3.2; Hailuo 02/2.3 → H3; Seedance 1.x → 2.5; Wan 2.5–2.7 → Wan 3.0 (open: 2.2); LTX-2/2.3 API → LTX-2.5 (keep 2.3 weights for union control); treat Pika as an aggregator; because these are retired or superseded.
3. [R24] If a platform's price differs from the file, then trust the platform's page on the day and log it, because routes differ up to 2× (Seedance 2.5 720p: $0.23 Replicate, $0.47 fal).
4. [R25, §7] If your aggregator lacks a model, then pick the closest verified substitute from its list rather than open a new account (each adds a key, a bill, a learning curve). First account: no API-key experience → Runway connector (sign-in; Seedance, Veo, Wan, H3, Omni Flash, Kling on one balance); lowest price with pre-run price check → fal (`get_pricing`); else Replicate (Gen-4.5, Vidu Q3) or the maker's app (Luma, Midjourney).
5. [R20] If in the US, Canada, UK, Australia or New Zealand and using Seedance, then go through fal, Replicate or Runway, because BytePlus's route is not offered there.
6. [R19] If a commercial release needs legally clean training data, then use Marey or Adobe Firefly Video, because Marey is trained only on licensed footage.

**Dialogue and performance**
7. [R1, §5] If the shot has spoken lines, then fix the voice first (record or synthesise each line) and use a model that takes an audio track or voice sample (Kling 3.0 Omni voice binding; H3, Seedance 2.x, Wan 3.0, LTX-2.5 audio reference; open: SkyReels V3 talking head, Wan 2.2 S2V); backup Veo 3.1 or HappyHorse 1.1 (good speech, but voices drift); draft Omni Flash 360p or Kling Turbo; because fresh voices per clip will not match across the film. If Kling via fal, then make a 3–8 s *video* of the character to carry the voice, because fal binds voices only to video elements.
8. [R22, §5] If a model has no native audio (Runway Gen-4.5, Luma Ray3.2, Marey, Midjourney), then use it only for silent or mix-built shots, never on-screen speech, because lip sync afterwards is a separate error-prone step. If you will score the picture yourself, then Kling 3.0 audio-off ($0.112 vs $0.168 on fal), Gen-4.5 or Ray3.2 avoid unwanted music and voices.
9. [R2] If two characters speak in one clip, then keep the second silent or off-screen and cut to them, because models move the wrong mouth (ByteDance names multi-subject interaction as a weakness).
10. [R12, §5] If the performance is subtle or matters most, then act it on a phone and transfer it (Runway Act-Two, Kling Motion Control, Ray3.2; open Wan-Animate-2), because a prompt cannot time a look.

**Frames, camera, length, format**
11. [R3, §5] If a shot must start or end on an exact picture, then make the stills first and use start-and-end control: H3 (first-and-last mode) or Kling 3.0; backups Veo 3.1/Fast (4–8 s), Seedance 2.x, Wan 3.0, Omni Flash, FLUX 3; draft Omni Flash 360p or Veo 3.1 Lite in Flow only (not in the API); because text never lands the same composition twice.
12. [§5] If several timed beats must land in one clip, then use Ray3.2 (16 keyframes) or FLUX 3 Video (multiple keyframes), because only these document more than two pinned pictures (Aleph 2.0 takes 5, editing only).
13. [R4, §5, Rec6] If a shot needs a precise camera path, then feed a Blender previs as a control video (Seedance 2.5 clay reference, H3 camera reference, Ray3.2 Modify, open LTX union control; backups Marey trajectory, Kling Motion Control, Higgsfield/PixVerse presets), because text camera moves are loose. For open LTX use LTX-2.3's published union LoRA unless your ComfyUI template supports union on 2.5 (no 2.5 union LoRA by 27 Sep 2026). Without a GPU or ComfyUI experience, go hosted (open adds hours of setup).
14. [R5, §5, §9] If a character, creature or prop recurs, then build its reference pack once, use references in every shot and one model per scene, because text-only descriptions drift. Creature: Kling O3 with 4–7 images (per-reference addressing); backup Seedance 2.5 (30), Wan 3.0 (10); draft Kling Turbo.
15. [R11, §5] If a shot is one continuous move over 15 s, then use Seedance 2.5 or Wan 3.0 (30 s); backup FLUX 3 or Ray3.2 (20 s), Veo extend; because extension joins show seams and face/light drift.
16. [§5, R15] If a wide establishing shot has no dialogue, then use Veo 3.1 4K or Kling 3.0 native 4K (backup Wan 3.0 1080p; draft Veo Lite). Make native 4K only for wide, detailed shots and upscale the rest, because native 4K costs 1.5–4× more.
17. [R23, §5] If the frame is wider than 16:9 (e.g. 2.39:1), then fix the ratio in the breakdown before generating, and use Seedance 2.x at 21:9 or 16:9 with action in the middle band, cropped, because most models output only 16:9 or 9:16 (Omni Flash nothing else).
18. [§5] If stylised, then make Midjourney stills and animate them (Midjourney video or Ray3.2), because style is set in the still. If fire, sparks or smoke, then any top model (Vidu Q3 advertises particles). If free/private/offline, then LTX-2.5 (≥16 GB GPU); backups Wan 2.2, HunyuanVideo 1.5 (≥14 GB), SkyReels V3 (<24 GB).

**Physics, text, screens, mirror**
19. [R8, §5] If objects must float or defy gravity, then simulate them in Blender and use a control video (Seedance 2.5 clay, LTX-2.3 union, Wan 2.1 VACE) or composite them over a plate, because 83–94% of clips from five late-2025 models had viewer-visible physics glitches and models lean to normal gravity.
20. [R6] If a shot has readable text, then generate the area blank or blurred and add text in compositing, because generated text is unreliable.
21. [R7, Rec8] If text or layout must read backwards, then generate the shot the right way round, add text, then flip the whole clip, because models asked for backwards text produce gibberish.
22. [Ex3] If a scene is marked "mirror", then give every asymmetric detail (ring, scar, parting, smile, bandage) a *prompt side* and a *screen side*, because the prompt writer will otherwise use the screen side and the flip will reverse it.
23. [§5, Rec9] If a screen shows content, then generate it as its own clip and composite it, because you control it frame by frame.
24. [Ex5, Ex8, §10] If something must appear from nowhere, then hard-cut from empty frame to present, not "materialise". If the model keeps disturbing a critical still (hands, rings), then use the still with a slow push-in made in the editor ("a still is a valid shot"). If one shot passes 10 takes, then stop and switch method (start-and-end frames, previs, compositing, or still + push-in) instead of spending more on the same prompt.

**Violence and refusals**
25. [R9, §4] If violence, then split into cause, reaction and aftermath, keep impact off-screen, put gunshots in the mix, and describe the visible picture not injury words, because filters block injury words and graphic frames even in artistic work (one tester: "weapon + fast motion + contact" triggered refusal; implied and off-screen violence passed).
26. [§4] If blood, then make it a separate small, non-gory element (Blender/compositing) or describe it by look. If guns, then partial and out of focus. If real people, then design original faces; never actors' photos as references. Children: heavy limits. Never remove SynthID/C2PA marks; disclose AI use.
27. [R10, §4] If refused twice, then stop rewording and move the element to compositing or sound, because retries waste money and can flag the account. Open weights (no hosted filter, licence still applies) are the last fallback; keep it non-graphic. Expect Runway strictest on weapon-plus-contact.

**Workflow, review, budget**
28. [R13, §5] If exploring, then draft at 360p–480p on the cheapest model (Veo 3.1 Lite or Wan 3.0 480p $0.05/s, Omni Flash 360p, fal H3 Max ≈$0.04) and re-make only the chosen version, because most takes are thrown away.
29. [R17] If a good take needs a small change, then edit it (Wan 3.0, Omni Flash conversational; backups Aleph 2.0, Seedance 2.5 region edit, Kling O3) rather than regenerate, because regenerating changes everything else.
30. [R16] If a clip comes from Google's API, then download it the same day (deleted after 2 days).
31. [R18] If an LLM reviews takes, then still watch every kept take, because Gemini 3.0 Pro missed over 74%/90% of glitched clips that untrained viewers spotted.
32. [Rec5] If start and end stills differ beyond the intended change, then remake one, because the model animates every difference.
33. [Rec2] If only three references fit, then keep front face, three-quarter face and full body front (identity, costume, proportions).
34. [Rec10] If a test clip's cost differs from the logged price by over 20%, then stop and re-read the price page.
35. [§10] If the budget is under $1,000, then make the film as a budget-tier animatic and upgrade only dialogue close-ups and key images. If spend passes 50% before 50% of shots are kept, then move remaining non-dialogue shots to the budget tier.

## 3. Breakdown fields

\* = the file's own name (Rec10 JSON); others are this digest's names for things the file says to record.

| Level | Field | Meaning | Values / example |
|---|---|---|---|
| film | `aspect_ratio` | Fixed before generating (R23) | 16:9 \| 9:16 \| 21:9 \| 2.39:1 (crop) |
| film | `generation_budget_usd`, `spend_cap_usd` | Budget; batch hard cap | $1,500–4,500 (*Catch*) |
| film | `price_tier` | Draft/final tier | budget ≈$0.07 \| mid ≈$0.17 \| premium ≈$0.45 per s |
| film | `aggregators[]`, `licensed_data_required` | Routes; clean-data need | fal \| Replicate \| Runway \| Higgsfield \| Krea \| OpenArt; true → Marey/Firefly |
| scene | `mirror`, `scene_model` | Flipped in editor; one model per scene | true \| false; "Kling 3.0" |
| shot | `shot_id`* | Identifier | "S07_03" |
| shot | `shot_need` | §5 row routing the model | dialogue \| performance \| establishing \| exact_start_end \| timed_beats \| exact_camera \| recurring_asset \| zero_gravity \| long_take \| stylised \| edit \| text \| screen \| fire \| animatic \| scope \| silent |
| shot | `asymmetric_details[]` | Prompt side vs screen side (Ex3) | {detail: ring, prompt_side: right, screen_side: left} |
| shot | `composite_elements[]`, `sound_mix_elements[]` | Moved out of the model | text, blood beads, sparks, screen content; gunshots, pump, latch clicks |
| shot | `fallback` | If takes fail | still + push-in \| compositing \| previs |
| generation job | `status`*, `model`* | State; exact aggregator ID copied on the day | "ready"; "fal: kling-video v3 pro image-to-video" |
| generation job | `draft_model` | Cheap draft model | Veo 3.1 Lite \| Wan 3.0 480p \| Omni Flash 360p |
| generation job | `mode`* | Input mode | text \| image_to_video \| start_end_frames \| references \| control_video \| edit |
| generation job | `start_frame`*, `end_frame`*, `references`*, `control_video` | Input files | "refs/S07_03_start.png" |
| generation job | `audio_in`*, `native_audio`* | Line audio; model makes sound | path \| null; true \| false |
| generation job | `duration_s`*, `aspect`*, `mirror_flip`*, `takes_wanted`* | Length, frame, flip, takes | 5, "16:9", false, 3 (finals 2–4) |
| generation job | `prompt`* | Model-specific prompt | motion-only when frames given |
| generation job | `cost_usd`*, `price_logged`, `kept_take`* | Measured cost; day's price; chosen take | null until run |
| generation job | `model_version`, `date`, `settings`, `seed`, `refusal_count` | Repeatability log; refusals (2 → move element) | seed if shown |
| character / creature / prop / set | `reference_pack` | Six views, one folder | `IONA_front.png`, `IONA_34.png` |
| character | `voice_sample`, `voice_video_element` | 10–30 s voice; 3–8 s video for fal Kling | audio/video paths |

## 4. Procedures

**Lookup: model facts** [§3A–3D]. $ per generated second.

| Model | $/s | Length; picture | Audio | Start+end | References | Notes |
|---|---|---|---|---|---|---|
| Veo 3.1 Std/Fast/Lite | 0.40 (4K 0.60) / 0.10–0.30 / 0.05–0.08 | 4/6/8 s (1080p, 4K, refs force 8); extend to ≈148 s at 720p (not Lite) | Yes; English best | Yes, not Lite in API | 3 | Deleted after 2 days; image modes adults only |
| Omni Flash 1.1 | ≈0.10 | 3–10 s, append to 40; 360/720p; 16:9, 9:16 only | Yes, no voice refs | Yes | Images + ≤3 clips ≤3 s | Conversational edits; timecodes |
| Kling 3.0/O3/Turbo | 0.112 silent, 0.168 audio; O3 4K 0.42 | 3–15 s; native 4K | Yes, voice binding | Yes | 7 images, or video + 4 | Multi-shot; Motion Control |
| Seedance 2.0 | 0.24–0.30 | 4–15 s; 480/720p; 21:9–9:16 | Yes | Yes (fal) | 9 img, 3 video, 3 audio | Face filters |
| Seedance 2.5 | 0.23–0.47 (720p) | 4–30 s; 480/720p | Yes, switchable | Yes | 30 img, 10 video, 10 audio | Clay-render camera ref; multi-shot; weak on multi-subject |
| Wan 3.0 | 0.05/0.10/0.20 | 2–30 s; ≤1080p, ≤16:9 | Yes, weak texture | End optional | 10 img, 5 video, 5 audio, 1 document | Best silent and editing scores; weak text |
| MiniMax H3 | ≈0.13 (2K); fal Max ≈0.04 | 4–15 s | Yes, 11 languages | Yes | ≤12 files | Copies camera moves; open 768p |
| HappyHorse 1.1 | 0.125–0.22 | 3–15 s | Yes, dialogue-tuned | [U] | 5 | — |
| Runway Gen-4.5 | 0.12 | 2–10 s | No | [U] | [U] | Aleph 2.0 edits; Act-Two |
| Luma Ray3.2 | ≈0.24 [U] | 20 s, 1080p, HDR/EXR | No | 16 keyframes | 8 faces | Modify; performance transfer |
| Grok Imagine 1.5 | from 0.08 | 1–15 s | Yes | [U] | Yes | Edit, extend |
| FLUX 3 Video | undisclosed | 20 s | Yes | Multiple keyframes | [U] | New; test first |
| Marey 1.5 | 0.30 | 5/10 s | No | [U] | [U] | Licensed data only |

Open weights: LTX-2.5 (≥16 GB; audio; 1055 Elo vs ≈1230 leaders; free under $10M revenue); Wan 2.2 (Apache; S2V, Animate-2, 2.1 VACE); HunyuanVideo 1.5; SkyReels V3 (talking head from portrait + speech; shot/reverse-shot continuation); MAGI-2 and H3 need data-centre GPUs. Test first: HiDream-O1-Video, Agnes-Video-2.5, SkyReels V4.

**Aggregator MCPs** [§7]: fal `https://mcp.fal.ai/mcp` (API key, `get_pricing`); Replicate `mcp.replicate.com` (token); Runway (runway.com/mcp, sign-in, "@Runway"); Higgsfield `https://mcp.higgsfield.ai/mcp` (sign-in); Krea, OpenArt (MCP). No outside-LLM control found for Google Flow. fal plus Runway or Higgsfield covers every first choice except Ray3.2 (Luma) and Midjourney.

**P1 Connect an LLM** [Rec1; $10–50 credit, 15 min]. No-key: (1) Claude settings → Connectors → Add custom connector; (2) paste the Runway or Higgsfield address; (3) Connect, sign in, buy the smallest pack; (4) "Using the connector, list the video models you can call and what each costs per second."; (5) test a 4 s draft ("a torch beam moving across wet brick"), check the charge. fal: account, $20–50, API key; `claude mcp add --transport http fal-ai https://mcp.fal.ai/mcp --header "Authorization: Bearer $FAL_KEY"`; then "Use get_pricing for Kling 3.0 Pro image-to-video, Seedance 2.5 reference-to-video, Wan 3.0 and Veo 3.1 Lite." Never paste keys into shared documents.

**P2 Reference pack** [Rec2; ≈$0.50–3, 30–60 min]. (1) Give the LLM the design notes (face, build, clothing, palette, what they carry). (2) Six prompts: front face, three-quarter face, profile, full body front, full body back (plain grey), one in-scene still under the film's light. (3) Generate (C2); reject sets where the face changes. (4) Name `NAME_front.png`…, one folder per asset. (5) Record limits: Veo 3 (forces 8 s), SkyReels V3 4, HappyHorse 5, Kling O3 7 (4 with a video), H3 9, Seedance 2.0 9, Wan 3.0 10, Seedance 2.5 30. (6) Voice: 10–30 s sample per speaker (Kling app 5–30 s; H3 and Wan ≤15 s total); for Kling via fal, a 3–8 s video of the character speaking it.

**P3 One shot** [Rec3; drafts $0.20–1, finals $2–10]. (1) Paste the shot entry: "Using the C1 decision table and rules, choose the model, the input mode (text, image-to-video, start-and-end, references, control video) and write the model-specific prompt." (2) Check against the per-shot checklist. (3) Make and approve start/end stills. (4) Two cheap drafts; watch. (5) Fix inputs once; final on first-choice model, 2–4 takes. (6) Log model, version, date, settings, seed, cost, kept take.

**P4 Dialogue two-hander** [Rec4; six lines ≈130 s, $22–62]. (1) Lock voices; record the exchange, one file per line, with pauses. (2) One silent two-shot, one close-up per line. (3) Close-ups: image-to-video from an approved still plus line audio (Seedance 2.x, H3, Wan 3.0) or Kling Omni bound voice; prompt the listener only if in shot. (4) Key performances via P7. (5) Cut to the audio; slide slightly-off clips a few frames, redo badly-off takes.

**P5 Exact start and end** [Rec5; $2–8]. (1) Both stills from the same pack and lighting. (2) Compare (rule 32). (3) H3 first-and-last; Kling 3.0 `end_image_url` (fal); Seedance 2.x (fal); Veo 3.1/Fast `image` + `lastFrame` (8 s for 1080p/4K). (4) Prompt only the motion between.

**P6 Previs to final** [Rec6; $5–25 hosted, 2–6 h first time]. (1) Rough Blender scene (C4): grey boxes, simple figures, camera path, simulated floaters. (2) Clay render at final length and aspect, plus depth if supported. (3) Route: Seedance 2.5 clay reference; H3 "reference the camera movement from Video 1"; Ray3.2 Modify; open LTX union (dolly/jib LoRAs only for LTX-2) or Wan 2.1 VACE. (4) Add reference packs. (5) Prompt the look only. (6) Compare frame by frame at key moments.

**P7 Performance transfer** [Rec7; $1–5]. (1) Phone video at eye level, plain background, good light; Kling driving clip 2–5 s. (2) Character still in the set (Kling: up to 7 references). (3) Act-Two, Kling Motion Control, Ray3.2 or Wan-Animate-2. (4) Check hands and eyeline; redo slower if limbs smear.

**P8 Mirror world** [Rec8]. (1) Prompt normal orientation, with asymmetric "wrong" features on the opposite side. (2) Generate. (3) Composite exact text. (4) Flip horizontally; keep a mirror column.

**P9 Screens** [Rec9]. (1) Content as its own clip (security camera: high angle, wide lens, desaturated, low frame rate, timestamp composited). (2) Device shot with green or dark screen. (3) Corner-pin (e.g. DaVinci Resolve); else image-to-video from a still with the screen image correct, minimal motion.

**P10 Batch** [Rec10]. (1) Structured breakdown. (2) "Write a Python script that reads `breakdown.json`, sends every shot with status `ready` to fal using the model and inputs listed, saves each clip as `SHOTID_takeN.mp4`, and writes the cost back into the file. Stop if the total cost passes $X." Template (illustrative; copy model IDs on the day):
```json
{"shot_id": "S07_03", "status": "ready", "model": "fal: kling-video v3 pro image-to-video",
 "mode": "start_end_frames", "start_frame": "refs/S07_03_start.png", "end_frame": "refs/S07_03_end.png",
 "references": ["refs/IONA_front.png"], "audio_in": null, "native_audio": false,
 "duration_s": 5, "aspect": "16:9", "mirror_flip": false, "takes_wanted": 3,
 "prompt": "The rung rolls in its brackets; her fingers open; torchlight trembles.",
 "cost_usd": null, "kept_take": null}
```
(3) Test three shots (rule 34). (4) Run overnight; review every take.

**P11 Budget** [§10]. *Generated seconds = finished seconds × overshoot × retake ratio.* 1,200 s finished; overshoot 1.5–3× [J]; retakes ~4:1 (vendor: 164 clips, 41 used; "roughly three generations per usable shot"). Lean 4.5× = 5,400 s ($378 / $918 / $2,430 at budget/mid/premium); typical 8× = 9,600 s ($672 / $1,632 / $4,320); heavy, no previs, 12× = 14,400 s ($1,008 / $2,448 / $6,480). Recommended: drafts 9,600 s × $0.07 = $672 + finals 3,600 s × $0.30 = $1,080 ≈ $1,750, plus stills, voices, upscaling, editor. Review: 5–10 min × ~300 shots = 25–50 h.

## 5. Checklists

**Per shot, before choosing** [Rec3]: dialogue? readable text? floating objects? violence? creature? exact camera path? (plus mirror scene, screen, over 15 s).

**Per kept take** [Rec11, human, 2–5 min]: faces match the reference pack • hands have five fingers and hold things properly • rings, scars and smiles on the correct side • no objects appearing or vanishing • cause before effect • gravity behaves as the script says • text correct (or blank for compositing) • right person's mouth moves • audio has no unwanted music or extra voices • cuts cleanly against neighbouring shots.

**Per asset** [Rec2]: six views, same face throughout, named files, per-model limits recorded, voice sample (and fal video element).

**Failure → fix** [§9]: physics → previs, shorter clips, composite. Vanishing hidden objects, effects before causes, too-easy actions (Runway's own list) → keep props visible, split cause and effect. Character drift → packs, one model per scene. Voice drift → voice first. Wrong mouth → one speaker per clip. Hands → inserts from checked stills; hide in wides. Fast-motion smear → slow motion then speed up, control video, shorter clip. Extension seams → 20–30 s models, cutaways. Retired model → log versions, keep stills and prompts. Glass → shoot each side, composite glass. Transparent things → backlight, references, macro.

## 6. Saying it to AI models

- **Violence:** describe the picture, not the injury: "he sits down heavily; a dark stain spreads on his shoulder". Blood by look: "small dark-red spheres". No gunshots in prompts; do not trick filters.
- **Start/end frames:** prompt only the motion between ("the cage drops, then stops hard; everyone jolts forward"); never re-describe the pictures.
- **Control video:** prompt the look (light, materials, mood) only.
- **Near-still finals:** only "slight breathing and light change".
- **Audio:** "no music, no subtitles". **Fast action:** ask for slow motion, speed up later. **Glass:** "faint reflections". **Transparent creature:** strong backlight, dark water.
- **Fails:** backwards text, asking a thing to "materialise", camera paths in words (loose), recomposing the same frame from text, character descriptions without references (drift).
- **Syntax:** Omni Flash timecodes "[0-3s] …" and chained edits ("make the light colder"); Seedance 2.0 "Shot 1: … Shot 2: …"; Seedance 2.5 "[Image1]", "[Video1]", "[Audio1]"; Kling "@Element1"; H3 "Reference the Hitchcock camera movement from Video 1".

## 7. The Catch

C1 names scenes by heading (other digests: cage = sc6, tablet = sc15). Risks: gunshots, a wound, floating blood, a creature struck with a cylinder, fire.

- **Ex1 Rung turns (FREIGHT SHAFT):** stills of hand closing and rung rotated → H3 first-and-last or Kling 3.0, 5 s silent, creak in the mix; draft Omni Flash 360p; sheared-bracket insert from a still. ≈$3.
- **Ex2 Cage falls, blood floats (FREIGHT CAGE):** Blender previs, camera locked to cage, 20–30 simulated beads. Seedance 2.5 clay reference + three packs, 10–15 s 720p; or LTX union from previs depth. Generate without blood; composite beads; wound out of frame. ≈$11–23, Hard.
- **Ex3 Backwards world (MAINTENANCE PASSAGE / STREET):** normal sign and car generated (Kling 3.0 or H3), text composited, whole clip flipped. Flipped scenes: turned Iona, Eli, Jude prompted ring on *right* (reads left); unturned Saye prompted *left* (reads right). After Iona turns back, scenes are unflipped; Jude's ring on his right as scripted; Eli's smile placed to read "on the wrong side of his face".
- **Ex4 Kitchen hands (SAYE'S HOUSE):** voice first; silent two-shot from an approved still, flipped if in the mirror set; singles on Kling Omni or Seedance 2.5/H3 with line audio; ring close-ups as still-based inserts. ≈$13–45.
- **Ex5 Figure on the tablet (QUARANTINE, JUDE'S ROOM):** Figure pack (front, side, back, head with strip lit, hand) every appearance; Kling O3, backup Seedance 2.5; hard-cut appearance; security-camera clip composited onto the tablet. The pump (three uneven strokes) is identical sound design every time, including the last line.
- **Ex6 Chest opens (SHIP, OUTER RECESS):** Ray3.2 keyframe per latch, silent, clicks in the mix; clear animal as macro shots from its own pack, backlit, Veo 3.1 4K or Kling O3 4K, 4–6 s. ≈$24, Hard.
- **Ex7 Shot through the roof (FREIGHT CAGE):** A muzzle flicker far above; B Jude's "Oh." (voice first); C Jude sitting into Eli, shoulder away. Shots and ricochet as sound plus a composited spark; Kling or H3 for faces, not Kling for the roof shot.
- **Ex8 Rings through glass (IONA'S ROOM, DAY):** checked final still → image-to-video (Veo 3.1 or Kling 3.0, 6–8 s), minimal motion; fallback still + push-in.
- **Budget:** eight showpieces ≈$80–130 finals; film $1,500–4,500 (no-previs first-timer: heavy row). Under $1,000: upgrade only dialogue close-ups and the rung, cage fall, Figure, chest, rings.

**For the writer/user:** which scenes are in the mirror set; delivery aspect ratio; budget and tier; which accounts; whether licensed-data models are required; country (Seedance route).

## 8. Conflicts and open questions

- **Mirror method:** C1 generates normally and flips; A3 calls building mirrored "safer for AI"; B1 mixes methods. Decide once.
- **Aspect:** B1 recommends 2.39:1; C1 offers Seedance 21:9 (native 480/720p only) or a 16:9 crop. Arithmetic, not in the file: 21:9 ≈ 2.33:1, so a slight crop remains.
- **Slow motion:** B1 bans it in *The Catch*; C1's smear fix generates slow motion then speeds it up, which must end at real speed.
- **Clip lengths:** A4's spec uses Veo's 4/6/8 s; C1 routes many shots to 5–30 s models.
- **Missing file:** Rec9 cites "the compositing file in this library"; none of the 14 files covers compositing.
- **Evidence limits:** physics rates are from late-2025 models; cost ratios are one vendor's; filter behaviour rests on one hands-on report; Kling blocked terms are third-party.
- **Unverified [§12]:** Gen-4.5 audio, keyframes, references; Ray3.2 price; Kling multi-shot count, extend, languages; Aleph 2.0 new angles; Grok per-resolution prices; HappyHorse end frames; Firefly, Freepik, LTX Studio, Krea details; SkyReels V4, HiDream, Agnes; LTX-2.5 with the 2.3 union LoRA; Flow LLM control; several licences; Midjourney API; late-September successors (search ran out).

## 9. Section map

- **§0** Evidence labels; staleness rule. **§1** ≈40 plain terms.
- **§2** Situation: Sora gone, Google's two lines, leaderboards, 30 s clips, audio exceptions, open releases, MCPs.
- **§3A** Hosted basics (19 models); **3B** controls; **3C** open weights and LTX add-ons by version; **3D** strengths, weaknesses, restrictions; **3E** retired models and replacements.
- **§4** Content restrictions for drama; per-model refusal table.
- **§5** Decision table: 20 shot needs → first choice, backup, draft, why.
- **§6** 25 decision rules.
- **§7** Aggregators table, recommendation, where to start.
- **§8** Recipes 1–11.
- **§9** Failure modes and workarounds.
- **§10** Cost arithmetic, tiers, scenarios, budget rules, review time.
- **§11** Eight *Catch* examples; budget table.
- **§12** Unverified items. **§13** Sources S1–S92; fact-check corrections.
