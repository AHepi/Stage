# C3 — Writing prompts for AI video models (as of 27 September 2026)

> **What this file is for**
> 1. It turns one shot of a scene breakdown into a prompt that an AI video model will actually follow.
> 2. It gives one model-neutral MASTER SHOT PROMPT TEMPLATE, plus adapters that rewrite it for each current model.
> 3. It says which camera words, dialogue formats, negative prompts and continuity methods work, and which do not.
> 4. It gives a failure catalog and a prompt linter checklist that an LLM runs before any money is spent.
> 5. It applies all of this to seven hard shots of *The Catch*. Re-check the model facts after 27 October 2026.
> 6. It states what each take costs and how hard each recipe is (Section 17A and Section 19), so a non-technical user can budget before sending anything.

---

## 0. How to read this file

Every factual claim carries a label:

- **[V] Verified**: read on the maker's own page, documentation, model card or official blog, or in a peer-style benchmark paper. The source number, like [P6], points to the Sources list at the end. Every source was checked on **2026-09-27**.
- **[U] Unverified**: found only in a secondary source, or I could not open the primary page, or sources disagree.
- **[J] Judgment**: my own reasoning or working practice. Treat it as advice, not fact.

**Scope.** This file covers only the words you send to a model. Which model to pick and what it costs is in companion file C1. Making consistent character pictures and storyboards is in C2. Camera and lens meaning is in B1; light and colour in B2; scene beats in A2. Where those files already define a term, this file uses the same word.

**Staleness rule [J].** In the twelve months before this file was written, OpenAI removed Sora 2 from its API (24 September 2026, announced 24 March 2026) [P10], Google shut down Veo 2 and Veo 3.0 (30 June 2026) [P7], and at least five new top models arrived. Before a paid batch, ask the LLM to re-open the official guides listed in Section 2.

**Fact-check note (27 Sep 2026).** This file was re-checked against the makers' own pages on 27 September 2026. Corrections made in that pass: LTX-2.5 has **no** published camera-move add-ons (they exist only for the older LTX-2); Runway Gen-4.5 has no native audio in its API; Luma says Ray3.2 has no native audio; MiniMax H3's prompt limit is 7,000 characters; Omni Flash was a public preview from 30 June 2026 before its 27 August general release; AVGen-Bench tested the April-2026 generation of models, not the current one; and the cage in Example 2 has its gate shut during the fall, as the screenplay says. A seventh worked example (the animal reveal, shot 18-32) and a cost-per-take table were added.

---

## 1. Plain-English terms used in this file

Each term keeps this one meaning throughout.

| Term | Meaning in one plain sentence |
|---|---|
| **Prompt** | The text you send to a video model to describe the clip you want. |
| **Shot** | One continuous camera view in the finished film, from one cut to the next. |
| **Clip** | One video file that a model returns from one request. |
| **Take** | One clip made for a specific shot; you usually make several takes and keep one. |
| **Master prompt** | This file's model-neutral description of one shot, stored in the breakdown, from which every model's prompt is made. |
| **Adapter** | A short set of rewriting rules that turns the master prompt into the wording, order and syntax one model prefers. |
| **Beat** | One change the audience can see or hear (a look, a line, a movement), placed at a moment inside a clip. |
| **Timecode** | A time marker written inside a prompt, such as `[0-3s]`, that tells the model when a beat happens. |
| **End state** | A sentence saying exactly how the clip should look in its final moment. |
| **Start frame / end frame** | A picture you supply that the clip must begin on / finish on. |
| **Reference image** | A picture you give the model so a character, creature, prop or place keeps looking the same (makers call these "ingredients", "elements" or "references"). |
| **Keyframe** | A picture pinned to an exact moment inside a clip; start and end frames are the simplest keyframes. |
| **Previs** | A rough 3D version of a shot, made in Blender or similar, used to plan camera and movement. |
| **Blocking** | Where the people in a shot stand and how they move. |
| **Control video** | A rough video, for example a grey previs render from Blender (Seedance calls it a "clay render"), whose camera move and blocking the model copies while inventing the final look. |
| **Identity key** | A fixed block of words describing one character or creature, pasted unchanged into every prompt where they appear. |
| **Look key** | A fixed block of words describing the light, colour and film texture of one scene, pasted unchanged into every prompt of that scene. |
| **Sound key** | A fixed block of words describing one character's voice, or one location's background sound. |
| **Native audio** | Sound (voices, effects, background sound, music) made by the model in the same run as the picture. |
| **Diegetic / non-diegetic sound** | Diegetic sound exists inside the story world (a pump, footsteps); non-diegetic sound is heard only by the audience (score music). |
| **Room tone** | The steady quiet background sound of a place, such as air-filter hum. |
| **Negative prompt** | A separate input box listing things the model should leave out. |
| **Prompt enhancer** | A built-in feature that rewrites your prompt before generating (MiniMax "prompt_optimizer", Wan "prompt_extend", LTX "prompt enhancer"). |
| **Seed** | A number that fixes a model's randomness, so the same inputs plus the same seed give a similar clip again. |
| **Multi-shot** | One request returns a clip that contains several shots with cuts between them. |
| **Extend** | The model continues an existing clip from its end to make it longer. |
| **Image-to-video** | The model animates a start frame you supply. |
| **Video-to-video** | The model restyles or edits an existing clip while keeping its motion. |
| **API** | A web address that a program can send requests to, paying per use, with no app to click through. |
| **Token** | The unit some models count prompt length in; a token is a piece of a word, so 1,024 tokens is very roughly 700 English words [J]. |
| **Open weights** | The model's files are published, so you (or a rented computer) can run it yourself. |
| **LoRA** | A small add-on file that teaches an open-weights model a style, a character or a kind of camera move. |
| **Compositing** | Layering pictures or clips on top of each other in editing software (for example, putting a screen image onto a tablet). |
| **Flip / rotate / reverse** | Free editing operations that mirror a clip left-to-right, turn it upside down, or play it backwards. |
| **Content filter** | The maker's automatic check that blocks prompts, uploads or finished clips that break its rules. |
| **Linter** | A checklist an LLM runs over a prompt to catch mistakes before the prompt is sent. |
| **Benchmark** | A published test that scores many models on the same tasks, so they can be compared. |
| **Model card** | The maker's technical fact sheet for a model, usually on Hugging Face. |
| **Aggregator** | A website, such as fal or Replicate, that sells many makers' models through one account. |
| **Slugline** | The scene heading in a screenplay, such as "INT. FREIGHT CAGE – CONTINUOUS". |
| **Two-shot** | A shot that frames two people together. |
| **Shot and reverse shot** | A shot of one speaker followed by a matching shot of the other, cut back and forth. |
| **Coverage** | The set of different shots made for one scene, from which the editor chooses. |
| **Insert** | A short close shot of a detail, such as a sign or a hand. |
| **Screen direction / eyeline** | Which side of the frame a person is on and which way they look; keeping it constant stops the audience losing their bearings. |
| **Plate** | A background clip made so that something else can be layered onto it. |
| **Grade** | The colour-correction step in editing that makes shots match. |
| **Soundscape** | All the sound in a clip other than music: voices, effects and room tone together. |
| **Timbre** | The particular character of a voice (gravelly, breathy, clear), separate from what it says. |
| **V.O. (voice-over)** | A voice heard over the picture from a speaker who is not seen. |
| **CCTV** | Security-camera footage, usually from a fixed high corner, grainy and low in contrast. |
| **HDR / GPU** | HDR is a picture format with a wider range of brightness; a GPU is a graphics card, needed to run open-weights models yourself. |

---

## 2. Current landscape: how each model wants to be prompted

This table covers prompting behaviour only. Prices, resolutions and access are in C1; how models rank in blind comparisons is on the Artificial Analysis leaderboard [P48].

### 2A. Structure, length and timing

| Model (maker), status | Prompt length limit | Preferred structure | Timing inside a clip | Official prompt guide |
|---|---|---|---|---|
| **Veo 3.1 / Fast / Lite** (Google). Current (model IDs still end in "-preview" in the Gemini API); clips of 4, 6 or 8 s; 8 s needed for 1080p, 4K and reference images; extend adds 7 s up to 20 times, 720p, Standard and Fast only [P5] | 1,024 tokens [P5] | Cinematography + subject + action + context + style and ambience [P8]; audio in separate sentences [P1] | Google's own blog shows `[00:00-00:02]` blocks inside one 8 s clip [P8] | [P1], [P2], [P8] |
| **Gemini Omni Flash 1.1** (Google). Announced at Google I/O, May 2026 [P9]; API public preview 30 Jun 2026; generally available as `gemini-omni-1.1-flash` 27 Aug 2026; the old `gemini-omni-flash-preview` name stops working 30 Sep 2026 [P7]. 720p default (1080p is an upscale), 16:9 or 9:16 only [P6]; clips up to about 10 s, extend to 40 s [P6][U: exact base length from C1] | Not stated [U] | Plain descriptive language; **makes several shots by default** unless told "In a single unbroken scene" [P6] | `[0-3s]` or "After 3 seconds, …" [P6] | [P6], [P1] |
| **Kling 3.0 / 3.0 Omni** (Kuaishou). Released Feb 2026; 3–15 s [P12]; still Kling's latest major version on 27 Sep 2026 [P55]; a cheaper 3.0 Turbo followed in June 2026 (see C1) | Not found [U] | One rich paragraph: scene and atmosphere, subjects, camera, actions in order, dialogue, sound [P12] | "At the 4th second, …" [P12]; or "Shot 1 (2s): …" [P13]; the API takes a list of shots each with its own duration [P16] | [P12], [P13] |
| **Seedance 2.5** (ByteDance). 31 Jul 2026; 4–30 s or "auto" [P18][P19]; on fal only 480p or 720p [P19]; up to 30 images + 10 videos + 10 audio as references [P18] | Not found [U] | Subject + action or event + scene + visual style + camera or cut + audio; "most of those components are optional" [P21] | `0–5s:` stages, then an "End state:" line [P18][P21] | [P18], [P21] |
| **Wan 3.0** (Alibaba). 13 Aug 2026; 2–30 s (or unset, so the model picks); 480p/720p/1080p; up to 10 reference images, 5 reference clips and 5 audio tracks; optional end frame; closed weights [P28][P29] | 5,000 characters on Wan 2.7 API; Wan 3.0 not stated [P27][U] | Keywords for shot size, angle, light, composition first; then entity + scene + motion + aesthetic control + style; sound last [P26]. Alibaba's guide labels its sound, multi-shot and reference formulas "Wan 3.0/2.7/2.6" [P26] | `Shot 1 [0–3 s] …` [P26] | [P26] |
| **MiniMax H3 / H3 Max** (MiniMax, maker of the Hailuo models). 31 Jul 2026; H3 4–15 s at 768p or 2K; H3 Max (made with fal, faster) 5–15 s at 480p or 768p [P30][P32]; H3 weights are downloadable (33B, MiniMax community licence, needs data-centre GPUs) [P31] | **7,000 characters** for H3 [P32]; 2,000 for the older Hailuo 2.3/02 [P33] | Three layers: visual and action timeline, overall soundscape, non-diegetic music [P31][P22] | `[Shot 1]` markers; "at 00:04.500" [P31] | [P31], [P32] |
| **Runway Gen-4.5** (Runway). Dec 2025; text-to-video or image-to-video, 2–10 s, 720p only (1280×720 or 720×1280) via API; **no audio option** in the API [P39] | 1,000 characters [P39] | Not verified: Runway's help-centre guide refused access (HTTP 403) [P42]; Runway's own developer docs point Gen-4.5's "Guide" link to its research page, which lists failure types but no prompt structure [P54][P38] | Not documented [U] | [P42] (blocked), [P38] |
| **Luma Ray3.2** (Luma). 9 Jun 2026; up to 20 s at 1080p; native HDR [P24]; **no native audio** (Luma pairs it with ElevenLabs sound models) [P49] | Not found [U] | Video-to-video prompt describes the **target end state** in positive words only [P23] | Up to 16 keyframes per clip [P24]; up to 64 in video-to-video [P23] | [P23] |
| **LTX-2.5** (Lightricks). Weights posted 23 Jul 2026, launched 11 Aug 2026; up to 20 s; open weights (free under $10M yearly revenue); built-in prompt enhancer and "auto duration" [P35][P51] | "Keep within 200 words" [P36] | One flowing paragraph, present tense, 4–8 sentences [P34] | Written as a natural sequence ("then", "a beat") [P34] | [P34], [P36] |
| **Sora 2 / Sora 2 Pro** (OpenAI) | **Removed from the API on 24 Sep 2026** [P10] | Its guide [P11] is still good general advice | — | [P11] |

### 2B. Dialogue, negatives, seeds and references

| Model | How to mark who says what | Negative prompt | Seed | How to name references in the prompt |
|---|---|---|---|---|
| **Veo 3.1** | `A woman says: My name is Clara.` Colon, **no quotation marks**, so the words are not drawn on screen [P2] | `negativePrompt` field on Google Cloud (Vertex AI) [P3]; not documented in the Gemini API [P5] | Yes. Google Cloud: same seed + same settings "guides the model to produce the same videos" [P3]; Gemini API: "slightly improves" repeatability [P5] | "Using the provided images for the detective, the woman, and the office…" [P8] |
| **Omni Flash** | Not specified; Google's shared guide applies [P1][P2] | No field; write "No dialogue", "No embellishments", "No extra sound effects" inside the prompt [P6] | Not documented [U] | `<FIRST_FRAME>`, `<LAST_FRAME>`, `<IMAGE_REF_0>`, `<VIDEO_REF_0>` tags [P6] |
| **Kling 3.0** | `Mom (softly, in a surprised tone): Wow, …` or `The man says, "…"` [P12] | `negative_prompt`, default "blur, distort, and low quality" [P16] | **No seed** parameter on fal's Kling 3.0 API [P16]; Kling's own API not checked [U] | `@Element1` or the element's name [P13][P16]. Voice binding: in Kling's app from a 5–30 s speech sample [P13]; on fal only a *video* element can carry a bound voice, not an image element [P16] |
| **Seedance 2.5** | Natural sentences [U: no official syntax found] | None [P19]; "avoid giant generic negative lists" [P21] | Yes, on fal [P19] | `@Image 1`, `@Video 1`, `@Clay Render 1` in ByteDance's examples [P18]; `[Image1]` on fal [P19]: use your platform's form |
| **Wan 3.0** | `[Black-suited Agent, raspy deep voice]: "Don't move."` plus four naming principles (Section 7) [P26] | `negative_prompt`, max 500 characters, on Wan 2.7 [P27]; Wan 3.0 [U]. In-prompt: "No dialogue." "No background music." [P26] | Not documented for 3.0 [U] | `Image 1`, `Video 1` (capital, space) [P26] |
| **MiniMax H3** | `<Subject 1> (S1) speaks softly, <d>[English] Follow the wind, live free.</d>` [P31]; plain "quietly says, '…'" also shown [P22] | None documented [P31] | Not documented [U] | Say which image, video or audio controls what [P22][P30] |
| **Runway Gen-4.5** | No native audio: the API has no audio setting for Gen-4.5 [P39]; add voices in the edit | None in API [P39] | Yes: same seed + same request gives "similar results" [P39] | Start frame only (position "first") [P39] |
| **Luma Ray3.2** | No native audio (Luma's own statement) [P49] | Avoid "no", "not", "without" [P23] | [U] | Keyframes pinned to frame numbers [P23] |
| **LTX-2.5** | `Baker (whispering dramatically): "Today… I achieve perfection."`; name language and accent if needed [P34] | Yes in the open pipeline; example list includes "fused fingers, bad anatomy, weird hand" [P37] | Yes (open weights) [J] | "Ingredients" reference add-on for LTX-2.5 [P51]. Camera-move add-ons (dolly in/out/left/right, jib up/down, static) were published **only for the older LTX-2 (19B)**, not for LTX-2.5, although LTX's product page lists them [P51][P35] |

### 2C. Superseded: do not write prompts for these

Sora 2 and Sora 2 Pro (removed from the API 24 Sep 2026; the Sora app closed earlier, in April 2026, per C1) [P10]; Veo 2 and Veo 3.0 (shut down 30 Jun 2026) [P7]; the model name `gemini-omni-flash-preview` (deprecated 30 Sep 2026; use `gemini-omni-1.1-flash`) [P7]; Kling 2.6 and Kling O1 (upgraded to Kling 3.0 and 3.0 Omni) [P12]; Hailuo 02 and 2.3 (followed by MiniMax H3; the bracketed camera commands in Section 4 belong to these older models) [P33][P30]; Luma Ray2 and the "Dream Machine" name (Luma calls both outdated, although its public API page still lists ray-2) [P49][P25]; LTX-2 and LTX-2.3 (followed by LTX-2.5; their hosted API endpoints were removed in August 2026 per C1, but the downloadable LTX-2 weights still matter because only they have the camera-move add-ons) [P35][P51]; Wan 2.5 to 2.7 (followed by Wan 3.0; Alibaba's prompt guide still covers them) [P26][P28]. Runway Gen-4 and Gen-4 Turbo are still offered in Runway's API but Gen-4.5 is the current model [P39][P54].

### 2D. Other current models with no dedicated adapter in this file

These are live on 27 September 2026 and some score well, but none publishes a prompt guide I could find. Use the **generic adapter** in Section 16 for them, make two test takes at the lowest resolution, and record what worked.

| Model | What matters for prompting | Source |
|---|---|---|
| **HappyHorse 1.0 / 1.1** (Alibaba) | HappyHorse 1.1 was runner-up to Seedance 2.0 overall in FilmBench, and the HappyHorse family won all three reference-copying sub-scores (scene, character and prop); 1.1 is tuned for dialogue; native audio; 3–15 s; seed supported on fal; no negative field on fal | [P43][P53]; languages and 1.1 date in C1 |
| **Grok Imagine Video 1.5** (xAI) | Up to 15 s; text, image and reference-image to video; edit and extend an existing clip; no prompt-structure guidance published | [P52] |
| **FLUX 3 Video** (Black Forest Labs), **Vidu Q3** (ShengShu), **PixVerse V6**, **SkyReels V3/V4** (Skywork) | Newer or mid-table models; see C1 for their controls. FilmBench tested Vidu Q3 Pro and found it lost more points than the leaders on action scenes | C1; [P43] |
| **Runway Aleph 2.0** (edit model) | Edits an existing clip; describe only the change (relight, remove, restyle). C1 reports it cannot invent camera angles or subjects that are not in the source clip | C1; [P54] |

---

## 3. Prompt anatomy

### 3A. The fields and what each does

Every guide found agrees on the same core fields, with different names [P1][P8][P21][P26][P34]:

1. **Subject**: who or what the shot is about, described specifically. Google: "Specificity helps avoid generic outputs" [P1].
2. **Action**: what visibly happens, in order.
3. **Setting**: where and when (place, time of day, weather, key props and their state).
4. **Camera**: shot size (how much of the subject fills the frame), angle, and one movement.
5. **Lens and focus**: only when it matters (wide-angle distortion, shallow focus).
6. **Light and colour**: the light source, its direction, and 3–5 colour words. The Sora guide advises naming sources ("soft window light with warm lamp fill, cool rim from hallway") rather than "brightly lit room" [P11].
7. **Style**: live-action film, animation, a period look. LTX says named styles "work especially well when named early" [P34].
8. **Audio**: dialogue, sound effects, room tone, music (or the absence of music).

For a pipeline, add four fields that are not "creative" but control the result: **inputs** (start frame, end frame, reference images, control video), **timing** (beats and end state), **exclusions**, and **post operations** (flip, rotate, reverse, compositing done in the edit).

### 3B. Order each model prefers

| Model | Recommended order | Source |
|---|---|---|
| Veo 3.1 | Camera and shot size → subject → action → setting → style and light → audio sentences | [P8], [P1] |
| Omni Flash | Declare sources and references first (`[# Sources …]`), state "single unbroken scene" if needed, then description, audio, "No …" lines | [P6] |
| Kling 3.0 | Scene and atmosphere → subjects → camera → actions in time order → dialogue with speaker labels → sound | [P12] examples |
| Seedance 2.5 | Goal → subject and main action → location, light, mood → framing, movement, cuts → timed stages → end state → protected details | [P21] |
| Wan 3.0 | Shot keywords (size, angle, light, composition) → entity → scene → motion → sound | [P26] examples |
| MiniMax H3 | Visual world → actions in order → camera "when it matters" → soundscape → music | [P22], [P31] |
| LTX-2.5 | Main action first → movement details → appearance → background → camera → light and colour → changes; or: shot → scene → action → characters → camera → audio | [P36], [P34] |
| Runway Gen-4.5 | Official order not verifiable [P42]. [J]: motion first, one paragraph, under 1,000 characters | [P39] |
| Luma Ray3.2 (video-to-video) | Target look only; no sequence of events | [P23] |

[U] Several practitioners say models weight the first sentences most. I found no maker stating this. [J] Put the one thing you most need in the first two sentences anyway; it costs nothing.

### 3C. How long a prompt should be

Hard limits: Veo 1,024 tokens [P5]; Runway 1,000 characters [P39]; MiniMax H3 7,000 characters [P32]; Hailuo 2.3/02 2,000 characters [P33]; Wan 2.7 5,000 characters, negative prompt 500 (longer text is silently cut off) [P27]; LTX "Keep within 200 words" [P36].

Guidance from makers: LTX expects "4 to 8 descriptive sentences" [P34]; Luma's Seedance guide says a good prompt "does not need to be enormous. It needs to make the important decisions clear," and suggests "around three or four meaningful beats per 15 seconds" [P21]; the Sora guide says "Not every detail needs to be included" [P11]; Google says the more detail, the more control [P1] but also that chaining events A-then-B-then-C in a short clip "often leads to muddled or incomplete videos" [P2].

**Working lengths [J]:**

| Clip | Words in the prompt |
|---|---|
| Image-to-video, one move | 25–70 (motion only) |
| Text-to-video, 4–8 s, one action | 70–130 |
| 10–15 s, 3–4 beats, with dialogue | 130–220 |
| 20–30 s staged sequence (Seedance, Wan) | 180–300 |

Identity, look and sound keys are pasted on top of these counts (each adds 30–60 words); if the total passes a hard limit, shorten the beats and setting, never the keys [J].

Longer is not better past these points: LTX warns "the more actions/characters/instructions you add, the higher the chance some of them won't be seen" [P34].

---

## 4. Camera words: which ones models execute

**Evidence base.** Google's own guide warns "Some advanced camera angles are not officially supported" and "Some advanced camera lenses are not officially supported" [P1]. FilmBench, a July 2026 benchmark built with Beijing Film Academy staff, found that camera movement, focus, shot size and viewing angle were the four sub-scores where models differ most, meaning these are the least dependable across models [P43]. An Oxford study probing open models found sideways and forward camera travel is easier for models than rotation, that rotation commands "leak" into sideways travel, and that horizontal moves work better than vertical ones [P44]. For its older Hailuo 2.3 and 02 models, MiniMax says bracketed camera commands give "more accurate results" than free text, with at most three combined; its list is `[Truck left/right]`, `[Pan left/right]`, `[Push in]`, `[Pull out]`, `[Pedestal up/down]`, `[Tilt up/down]`, `[Zoom in/out]`, `[Shake]`, `[Tracking shot]`, `[Static shot]` [P33]. Wan's guide keeps the camera still with the words "fixed camera" [P26]. Luma's (Ray 2) API has a Camera Motions endpoint that returns the exact camera phrases it understands [P25]. In FilmBench, Seedance 2.0 won the most camera-language sub-scores (camera movement, shot size, focus, angle) of the nine models tested [P43]; newer models (Seedance 2.5, Wan 3.0, MiniMax H3, Omni Flash) were not in that test.

**How to read the Reliability column.** A [V] mark below means a maker documents the term with a working example (or a study measured it); it does **not** mean anyone published a success rate for each model. The grades Reliable / Usually works / Unreliable are judgment [J] built on that evidence. **If** a move is graded "Usually works" or worse, **then** budget one extra take for it.

| Term (plain meaning) | Reliability | Notes and safer wording |
|---|---|---|
| **Static / locked-off** (camera does not move) | Reliable [V: P1, P31] | "Static shot, the camera does not move." H3: "camera holds a perfectly static shot" [P31]; Wan: "fixed camera" [P26]. The most dependable move of all [J]. |
| **Push in / dolly in** (camera travels toward subject) | Reliable [V: P1, P34] | Say speed and where it ends: "slow push in, ending on her eyes." LTX: "slow dolly in" improves consistency [P34]. |
| **Pull out / dolly out** | Reliable [V: P1] | "Pull back to reveal …" and name what is revealed. |
| **Pan left/right** (camera turns sideways on the spot) | Reliable [V: P1, P33] | Horizontal beats vertical [P44]. |
| **Tracking / following** | Reliable [V: P1, P34, P12] | Say the side: "tracks alongside her, at her left." |
| **Handheld** | Reliable [V: P1, P34] | Say how much: "slight handheld sway." |
| **Shot sizes** (wide, medium, close-up, extreme close-up) | Reliable on top models, variable on others [V: P1, P43] | Use one size per shot; if it must change, say "ending in a close-up." |
| **Low angle / high angle / overhead** | Mostly reliable [V: P1, P43] | "Low-angle shot looking up at …" |
| **Over-the-shoulder** | Reliable [V: P1, P34] | Name whose shoulder: "over Iona's left shoulder toward Saye." |
| **POV** (we see through a character's eyes) | Usually works [V: P1; J] | Add a visible anchor: her hands, her torch beam. |
| **Tilt up/down** | Usually works; check [V: P1, P44] | Vertical moves are weaker [P44]. |
| **Crane / pedestal up-down** | Usually works; check [V: P1, P44] | Same vertical weakness. |
| **Orbit / arc** (camera circles subject) | Usually works; check [V: P1, P12, P44] | Rotation leaks into sideways travel [P44]. Ask for a half-circle, not 360°, unless the model shows it (Kling's example does a 360° orbit [P12]). |
| **Zoom** (lens magnifies, camera stays put) | Unreliable as a distinct move [J] | Google defines it as different from a dolly [P1]; in practice models often travel instead [J]. If the difference matters, crop in the edit. |
| **Whip pan** | Unreliable [J] | Often becomes a cut. Use a cut. |
| **Rack focus** (focus shifts from near to far) | Unreliable [V: P43 focus variance; J] | Google gives an example [P1]. Give a trigger: "as she turns, focus shifts from the cup to her face." Or fake it in compositing. |
| **Dolly zoom / vertigo effect** | Unreliable [V: P1 warning; J] | Usually comes out as a plain push or zoom [J]. Use a control video from Blender, or choose a different move. |
| **Focal lengths in millimetres** ("85mm") | Unverified [U] | The Sora guide used "same shot, switch to 85 mm" [P11]; other makers do not document it. Describe the effect: "compressed background, shallow focus." |
| **Compound moves** (more than two at once) | Unreliable [V: P33] | One move per shot [P11]. |
| **Exact numbers** (degrees, metres, seconds of a move) | Unreliable [J] | Use a control video or keyframes. |

**Camera rules [V/J].**
1. One camera move per shot: "Each shot should have one clear camera move and one clear subject action" [P11].
2. Say the camera's relationship to the subject and where the move ends: "Including how subjects or objects appear after the camera motion gives the model a better idea of how to finish the motion" [P34].
3. For image-to-video, camera movement alone "is the simplest and most reliable way to add dynamism" [P2].
4. If the move must be exact, stop writing words and give a control video (Section 9D).

---

## 5. One clear action per shot, and timing inside a clip

**What the makers say.** OpenAI: one camera move and one subject action per shot, and describe actions "in beats": not "actor walks across the room" but "actor takes four steps to the window, pauses, and pulls the curtain in the final second" [P11]. Google: "For short videos, dedicate each prompt to a single, focused moment" [P2]. Luma's Seedance guide: three or four meaningful beats per 15 seconds, organised as stages with an end state, because "the end state matters because it gives the sequence somewhere to arrive" [P21]. FilmBench found action scenes lowered every model's scores [P43].

**Known timing failures.** Runway lists three of its own model's failure types: "effects sometimes precede causes (e.g., a door opening before the handle is pressed)", "objects may disappear or appear unexpectedly", and "success bias: actions disproportionately succeed (e.g., a poorly aimed kick still scoring a goal)" [P38]. [J] Expect all three in every model.

**Rules [J].**
- About one main action per 4–5 seconds of clip, and one spoken line per 3–4 seconds.
- Write actions as physical steps with counts or durations ("two slow steps", "holds for a breath").
- Put cause before effect in the same sentence with "then", or give each its own timecode. If the order still flips, split into two shots.
- When a character must fail (a foot slips, a grip gives), describe the failure itself as the action, early in the prompt, and state the end state that proves it failed.
- Always end with an end state for clips over 6 seconds.

**Timing syntax by model:** Veo `[00:00-00:02]` [P8]; Omni `[0-3s]` or "After 3 seconds" [P6]; Kling "At the 4th second" or "Shot 1 (2s):" [P12][P13]; Seedance `0–5s:` plus `End state:` [P18][P21]; Wan `Shot 1 [0–3 s]` [P26]; H3 "at 00:04.500" [P31]; LTX plain sequence words [P34].

---

## 6. Performance and emotion: describe behaviour, not labels

**What the makers say.** LTX: "Avoid emotional labels like 'sad' or 'confused' without describing visual cues. Use posture, gesture, and facial expression instead" [P34]. Luma's Seedance guide: "Describe emotion as performance … You are converting an internal emotion into something visible" [P21]. Luma's H3 guide: "'She tightens her grip on the letter and looks away' gives the model something more visible to generate than 'she becomes emotional'" [P22]. FilmBench found emotional performance and action performance were among the lowest-scoring sub-scores for every model [P43], so this is where prompts need the most care.

**Method [J].** Replace each emotion word with two or three observable behaviours from this list: where the eyes go and how long they stay; blinking; breath (held, one slow breath, shallow); mouth (pressed, slack, a corner lifting); jaw; hands (still, gripping, flat); posture (shoulders up, weight shifting); timing (a pause before moving). Keep tone words for the **voice** only ("in a low, flat voice"), because Kling and Wan both use tone labels for speech [P12][P26].

| Screenplay line in *The Catch* | Label to avoid | Behaviour to write |
|---|---|---|
| "She stays on her knees. One breath." | "she is shaken" | "She stays kneeling and still; her shoulders rise once with one slow breath; her eyes stay on the empty bracket." |
| "For a moment the beard belongs to somebody else. Then one corner of his mouth lifts, the crooked half-smile she knows." | "he recognises her warmly" | "He looks at her through the glass without expression for a moment, then the left corner of his mouth lifts in a small crooked half-smile." |
| "Her face changes." (after the mint leaf) | "she is horrified" | "She stops chewing. Her eyes lose focus and drift down; her lips part slightly; she holds very still." |
| "She opens her mouth. Nothing in it." | "she is speechless" | "She opens her mouth to answer, holds it open for a moment, then closes it without a sound and looks down." |

---

## 7. Dialogue, voices, sound effects, room tone and music

### 7A. Marking who says what

- **Veo and Omni:** name the speaker, give delivery, then a colon and the line, without quotation marks: `A woman says: My name is Clara.` Google gives this rule "to prevent the model from rendering text in the video" [P2]. (Google's October 2025 blog used quotation marks [P8]; the current documentation, updated September 2026, recommends the colon form [P2]. [J] Follow the current documentation.)
- **Kling 3.0:** `Name (delivery, tone, accent): line`, or `Name says, "line"`. Kling 3.0 "will automatically match each character with their corresponding lines" and handles three or more speakers [P12]. If a character element already has a bound voice, Kling advises not to set the voice tone again in the prompt [P12].
- **Wan:** four principles for two or more speakers [P26]: (1) unique, consistent labels, no pronouns (`[Character A: Black-suited Agent]`, never "he"); (2) visual anchoring: describe the speaker's action first, then the line; (3) a distinct voice label per character (`[Black-suited Agent, raspy deep voice]`); (4) linking words for order ("Immediately, …") so lines do not merge. Lines written as `X says: '…'` are kept exactly; with no lines written, Wan invents them; "No dialogue." stops speech [P26].
- **MiniMax H3:** official structured form `<Subject 1> (S1) speaks softly, <d>[English] line</d>` [P31]; plain "quietly says, '…'" is shown by Luma's guide [P22]. [U] Which works better through the public API is not documented.
- **LTX-2.5:** `Name (delivery): "line"`, "mention the language and accent" [P34].

### 7B. Voices, accents, tone and language

Wan's voice formula: "Character's lines + Emotion + Tone + Speed + Timbre + Accent" [P26]. Google's consistency method: give each character "a name and a specific voice style" and paste the same voice description into every prompt, for example "In a voice that is crisp and clear, with a thoughtful, analytical tone and a standard American accent, Clara says: …" [P2]. Kling 3.0 speaks Chinese, English, Japanese, Korean and Spanish and translates other languages into English [P12]; H3 lists 11 stable languages [P31]; Omni says only English is "fully supported" [P6].

### 7C. How many words fit

The Sora guide keeps lines concise and natural, matched to clip length, and says one or two short exchanges fit a 4-second shot [P11]; Luma's H3 guide: "Keep the actual line concise enough to fit comfortably within the clip" [P22]. [J] Budget at most 2.5 spoken words per second of clip, and leave half a second of silence at each end. An 8 s clip holds about 15–18 words across two speakers.

### 7D. Known audio weaknesses (benchmark evidence)

AVGen-Bench (April 2026) measured the audio-video models of early 2026: Sora 2, Kling 2.6, Wan 2.6, Seedance 1.5 Pro, Veo 3.1 (Fast and Quality), LTX-2.3 and Ovi [P45]. It found lip-sync errors of about 2 to more than 5 frames; sound-to-picture offsets of 0.2–0.44 s; "Partial Instruction Dropping" (words omitted or sentences cut short when long dialogue is required); even top models "drop" some sounds when music, footsteps and speech are asked for at once; and near-total failure to play requested musical notes. Veo 3.1 Quality scored highest for speech intelligibility (96.09) [P45]. **Caution [J]:** Kling 3.0, Seedance 2.x, Wan 3.0, MiniMax H3 and Omni Flash were not in this test, so treat these numbers as the known floor of the problem, not as a ranking of today's models. Wan's own guide says "Lip sync to exact words does not work reliably" [P26].

### 7E. Sound effects, room tone and music

- Describe audio in separate sentences [P1], and tie each important sound to the action that makes it: "Her shoes echo against the tile" [P21][P22]. Wan's sound-effect formula: source + action + surrounding space [P26].
- [J] Name at most two or three distinct sounds per clip, because extra sounds get dropped [P45].
- Music: Omni generates "an appropriate audio track" by default [P6]; Wan chooses background music unless you write "No background music." [P26]; [J] assume any model with native audio may add music. [J] For drama, suppress music in every clip and add one score across the edit, because generated music changes at every cut.
- **Silent models [V/J].** Runway Gen-4.5 (no audio setting in its API [P39]) and Luma Ray3.2 (no native audio, per Luma [P49]) make picture only. **If** you use one of them, **then** delete the DIALOGUE and AUDIO fields from its prompt (they waste characters and can make mouths move at random), write "her lips stay closed" or "she speaks" only as visible behaviour, and make the voice and sound separately (see the audio companion file).
- Exact-moment sounds (a gunshot, a latch clack, the pump's "three uneven strokes") [J]: generate them if you like, but plan to replace or re-time them in the edit, because of the 0.2–0.44 s offsets above.

### 7F. Voices through glass, radios and screens [J]

Name the path the sound takes, or the model will play the voice as if the speaker were beside the camera: "her voice comes through a small intercom speaker, slightly thin"; "Jude's voice, heard only in her earpiece, crackly; he is not visible"; "the voice from the tablet's small speaker". For off-screen voices, say "is not visible" in the same sentence.

### 7G. Keeping words off the screen

Veo/Omni: colon format [P2]. Seedance 2.5 claims to reduce "uncontrolled occurrences in subtitles and background music" [P18]. [J] Where a negative prompt field exists, add "subtitles, captions, on-screen text". [U] Whether "No subtitles" written inside an Omni prompt works: not documented.

---

## 8. Negative prompts: which models support them and how to write them

| Model | Separate field? | How to write it |
|---|---|---|
| Veo 3.1 on Google Cloud | Yes, `negativePrompt` [P3] | Short nouns: "wall, frame", **not** "no walls" or "don't show walls" [P1] |
| Veo 3.1 in the Gemini API / Flow | Not documented [P5] | Describe what you want positively: "a desolate landscape with no buildings or roads" rather than "no man-made structures" [P8] |
| Omni Flash | No [P6] | Simple lines inside the prompt: "No dialogue", "No embellishments", "No extra sound effects" [P6] |
| Kling 3.0 | Yes, default "blur, distort, and low quality" [P16] | Keep the default words and add yours |
| Wan 2.7 (3.0 unverified) | Yes, max 500 characters [P27] | Nouns; plus in-prompt "No dialogue." / "No background music." [P26] |
| LTX-2.5 (open weights) | Yes [P37] | The model card's example: "shaky, glitchy, low quality, worst quality, deformed, distorted, disfigured, motion smear, motion artifacts, fused fingers, bad anatomy, weird hand, ugly, transition, static" [P37] |
| Seedance 2.5 | No [P19] | Fix the specific failure instead: "If a face drifted, address identity" [P21] |
| MiniMax H3 | Not documented [P31] | Positive description |
| Runway Gen-4.5 | No [P39] | Positive description |
| Luma Ray3.2 | No | Avoid "no", "not", "without", "devoid of", "missing": "Negation can bias the model toward the thing you are trying to exclude" [P23] |

**Rules [J].** (1) Inside the main prompt, use only the documented "No …" phrases above; describe everything else positively ("plain bare concrete walls" instead of "no signs"). (2) In a negative field, write 3–10 short nouns aimed at the failure you actually saw. (3) Never paste a giant generic negative list; it hides the real problem [P21].

---

## 9. Inputs: image-to-video, start and end frames, references, control videos

### 9A. Image-to-video: describe the motion, not the picture

Google: "Your source image already provides the subject, scene, and style. Focus your prompt on the motion you want to see." Google lists re-describing "the character, the background, or the lighting depicted in the image" as not recommended, because "Redundant prompts confuse the model and lead to poor results" [P2]. Refer to people with general terms: "the subject", "the woman", "he", "they" [P2]. Direct three kinds of movement: camera motion, subject animation, environmental animation [P2]. Luma's H3 guide gives the order: "Opening image → first movement → continued action → final reaction" [P22]. Runway Gen-4.5's API accepts the image as the first frame only [P39].

### 9B. Start and end frames: describe the path between them

Luma's H3 guide: "Do not simply describe both images. Describe the motion that connects them," in the order starting state → intermediate physical changes → approach toward the final composition → ending state [P22]. Kling warns that the two frames "should be as similar as possible" and that large differences "may trigger a shot switch" [P14]. Veo needs 8 s clips for reference images and for 1080p or 4K [P5]. Veo 3.1 takes a `lastFrame` image together with the start image ("interpolation"); the parameter table lists it for Standard, Fast and Lite, and for image-to-video, interpolation and reference images the person setting is "allow_adult" only, so these modes cannot show children [P5]. Omni binds frames with `<FIRST_FRAME>` and `<LAST_FRAME>` tags; using the same image for both makes a loop [P6]. Google's example of a 180° arc between two frames: "The camera performs a smooth 180-degree arc shot, starting with the front-facing view of the singer and circling around her to seamlessly end on the POV shot from behind her" [P8].

### 9C. Reference images: give each one a job

"Label references explicitly" and "Say what to preserve" [P19]; "references work best when their purpose is explicit: @image1 defines Maya's identity and facial features. @image2 defines her red coat" [P21]; start with 2–3 key references, not every one you have [P19]; use "well-lit, single-subject images" [P19]. FilmBench found that adding references lowered models' scores to varying degrees (the weakest model most), and that the model best at copying references (the HappyHorse family) was not the best overall filmmaker (Seedance 2.0) [P43]. [J] Attach only the references a shot needs. Reference limits differ: Veo 3.1 up to 3 images [P5]; Kling 3.0 Omni up to 7 images, or 4 with a video [P13]; MiniMax H3 up to 9 images, 3 videos, 3 audio [P32]; Wan 3.0 up to 10 images, 5 clips, 5 audio [P29]; Seedance 2.5 up to 50 inputs in all [P18][P19].

### 9D. Control videos (from Blender or other previs)

Seedance 2.5: "Refer to @Clay Render 1 for camera movement, pacing, shot-size transitions, subject trajectory, and blocking. Refer to @Image 2 for character design, scene, materials, lighting, color" [P18]. MiniMax H3 copies a camera move from a reference video ("Reference the Hitchcock camera movement from Video 1") [P30]. Kling offers a Motion Control endpoint that "transfers movement from a reference video onto a character in a reference image" [P17]. Lightricks published camera-move add-ons (dolly in/out/left/right, jib up/down, static) **only for LTX-2 (19B, January 2026)**; none exists for LTX-2.5 as of 27 September 2026, although LTX's product page lists camera LoRAs among LTX-2.5's controls [P51][P35]. [J] Add-ons made for one model size do not load into another, so **if** you need a LoRA-locked camera move, **then** run LTX-2 with that add-on, or describe the move in words for LTX-2.5. Luma Ray3.2 video-to-video restyles a rough clip, pinned by up to 64 keyframes, with a prompt that describes the target end state and "should not describe a sequence of changes" [P23]. [J] When a control video is attached, the text prompt should describe look, identity and sound, and say that camera and blocking come from the control video; do not describe the camera move a second time in different words.

---

## 10. Multi-shot prompts

| Model | Syntax | Notes |
|---|---|---|
| Omni Flash | Default behaviour; timecodes set cuts ("After 2s cut to a new scene") | Say "single unbroken scene" to prevent cuts [P6] |
| Kling 3.0 | "Multi-Shot" switch (model plans cuts) or "Custom Multi-Shot" (you set shots and durations) [P12]; API `multi_prompt` [P16] | Understands "shot-reverse-shot dialogues … cross-cutting dialogue and voice-over" [P12] |
| Seedance 2.0/2.5 | "Shot 1: … Shot 2: …" [P17][P20] | Or "single continuous take, no cuts" [P18] |
| Wan 3.0 | Overall description, then `Shot 1 [0–3 s]`; "Hard cut transition" inside a shot line; formula labelled for Wan 3.0/2.7/2.6 [P26] | "Generate single shot." forces one shot (documented for Wan 2.7) [P26] |
| MiniMax H3 | `[Shot 1]` markers [P31] | "Introduce a cut when the next shot reveals genuinely new information" [P22] |
| LTX-2.5 | Native multi-shot (wide, over-the-shoulder, medium, close-up) [P35] | [U] C1 quotes Lightricks saying continuity across these cuts "is not guaranteed" (not re-checked here) |
| Veo 3.1 | Timecode blocks shown by Google [P8] | [J] Keep to one shot per clip |

**Evidence.** FilmBench: moving from single-shot to multi-shot prompts cost models 7.9 points on average and up to 22.8 points, mostly in composition, camera movement, focus and cross-shot consistency [P43].

**Rule [J].** The breakdown is shot by shot, so default to **one shot per clip**. Use multi-shot only (a) for a dialogue exchange where both faces must match in one location, (b) for fast inserts, or (c) to explore coverage cheaply. Even then, cut the final film in an editor.

---

## 11. Continuity across separately generated clips

Ranked by how much they help [J]:

1. **Reference images per character, creature and set** (built once, as in C2), attached to every shot where they appear.
2. **Identity key pasted unchanged.** Google: "Copy and paste the entire, unchanged character description into your prompt for every new scene or action. Only modify the parts that describe the new action or setting" [P2]. Luma: "Continuity becomes harder when your own prompt keeps changing" [P21].
3. **Look key pasted unchanged** within a scene: the same light source, direction and 3–5 colour words [P11].
4. **Sound key**: the same voice description per character [P2]; Kling can bind a voice to a character element [P12]; the same room-tone sentence per location.
5. **Final frame → next start frame.** Export the final frame of the kept take and use it as the start frame of the next shot when the camera does not cut away. [J] Any editor can export a frame; an LLM can also write the one-line command for `ffmpeg`, a free command-line video tool. Omni, Veo, Seedance and LTX also have extend features: Veo adds 7 s at a time, up to 20 times, at 720p, on Standard and Fast only [P5]; Omni adds 10 s at a time up to 40 s [P6]; Seedance 2.5 "multi-round extensions" [P18]; LTX-2.5 "Extend" [P35].
6. **Same seed** where supported. Google recommends "the same seed parameter" for consistent visual, stylistic and voice output across scenes [P2]; Runway says the same seed gives "similar results" [P39]; Seedance 2.5 and HappyHorse accept a seed on fal [P19][P53]; Kling 3.0 on fal has no seed [P16]. [J] A seed helps most when you re-run the same shot with one small change; it does not by itself hold a face across different shots.
7. **Screen direction and eyelines** [J]: say which side of frame each person is on and which way they face ("Iona frame left, facing right"), and keep it constant across a dialogue.
8. **Changing states** [J]: keep a state list in the breakdown (Iona's palm skinned after the sill, then bandaged; Jude's shoulder dressing; the figure's cracked face cover, then patched) and add the current state to the identity key for that scene.

---

## 12. "Impossible" physics: zero gravity, falling, reversal, mirroring

**Evidence.** Physion-Eval (March 2026) found, in physics-focused tests, at least one human-visible physics glitch in 83.3% of third-person and 93.5% of first-person clips from leading models, and that AI video critics caught far fewer glitches than untrained people [P46]. AVGen-Bench found models get physical outcomes wrong when the prompt does not spell them out [P45]. ByteDance says Seedance 2.5 still needs work on "the physical plausibility of complex motions" and "interactions among multiple subjects" [P18]. LTX: "Non-linear or fast-twisting motion … can lead to artifacts" [P34]. Google claims Omni has "improved intuitive understanding of forces like gravity, kinetic energy and fluid dynamics" [P9].

**What works [J, informed by the above].**

1. **Describe the visible evidence, not the cause.** Not "zero gravity" alone, but: "her hair, shirt and loose straps drift up and outward; nothing settles; small objects hang in the air, slowly turning".
2. **Do not write the word "falling" when people must float.** The model will make them drop. Describe the world moving instead: "through the mesh of the closed gate, the brick wall streams upward".
3. **Fix the camera to the moving room.** "The camera is fixed to the cage and does not move relative to it." Weightlessness reads from the room staying still while bodies drift.
4. **Use a familiar comparison.** "Floating the way astronauts float inside a space station" draws on the large amount of such footage models have seen. [U] This is practitioner lore; test it.
5. **Use free edit operations for global effects.** A left-right mirrored world is a **flip**; an upside-down room is a **rotate** of 180°; "the brick slides past the wrong way" can be a **reverse** of a clip that has no faces or speech in it. These are exact and cost nothing.
6. **Composite the fragile element.** Floating blood beads, a rising screw, sparks: generate the plate without them and add them from a Blender particle render or stock element, because liquids that must hang still are a known weakness [J].
7. **Give a control video** for any shot where the relative motion carries the story (the cage stopping dead, then dropping) [P18].
8. **Watch every take yourself** for physics. Do not rely on an LLM reviewer [P46].

**Mirror-world specifics [J].** A flip mirrors everything in frame, including characters. In *The Catch*, the audience shares Iona's view: the world is backwards, and Iona looks normal to herself. So (a) flip shots with no continuing character in them (inserts of signs, streets, dashboards); (b) for shots with Iona, either keep only symmetric parts of her in frame, or generate the background alone, flip it, and composite her unflipped; (c) never flip shots where left/right on a person is a plot point, such as the wedding-ring shots ("Saye's wedding ring. On her right hand."); generate those unflipped, with the hand position fixed by a start frame.

---

## 13. Text, screens, hands and crowds

### 13A. Text in video

AVGen-Bench: models generally succeed with explicitly prompted text "when the target string is short and occupies a dominant spatial region", but "performance degrades rapidly as text length increases or spatial resolution decreases", and incidental background text becomes "messy, graffiti-like scribbles" in every model tested [P45]. Makers differ: Omni claims it renders text "correct and readable" and advises defining what background signs say [P6]; Kling 3.0 "accurately preserves textual details from original images" (text in an uploaded start frame) [P12]; Wan says "Text renders approximately" and Alibaba says Wan 3.0's on-screen text is "not yet where we want" [P26][P28]; the LTX-2 guide says it "does not currently generate readable or consistent text. Avoid signage" [P34], while LTX-2.5 claims "more legible text and signage" [P35] ([U]: test before relying on it).

**Rules [J].** At most three words per sign, written exactly, in quotation marks (for signs, you *want* the words drawn). Describe other surfaces as "plain" so no stray text appears. For backwards text, generate forward text and flip, or composite. For long text (file names, labels, "NELL ROWAN. FLIGHT TEST."), composite it.

### 13B. Screens (tablets, monitors, visor displays) [J]

Generate the screen's content as its own full-frame clip ("security camera footage, high corner, grainy"), then either use it full-frame or composite it onto the screen in the edit. Ask the main shot for "a blank dark tablet screen" or "a screen glowing softly", so there is a clean surface to replace. Visor graphics (the green line, "UPWARD SPEED", outlines) are motion graphics made in the edit, not in the video model.

### 13C. Hands [J]

LTX's own negative example includes "fused fingers, bad anatomy, weird hand" [P37], which tells you it is a known failure; Physion-Eval lists contact and interaction failures among common glitches [P46]. Keep one simple grip per shot; name the contact ("her fingers hook through the grid squares"); avoid counting fingers or fine manipulation in wide shots; for a key hand moment (a ring on the right hand, a thumb on a lens), start from a start frame where the hand is already correct and ask for small movement only.

### 13D. Crowds and many characters

AVGen-Bench found "Crowd Degradation (significant quality and stability collapse for individual faces in multi-person scenes)" [P45]; LTX: "Too many characters, layered actions, or excessive objects reduce clarity" [P34]; Wan 2.6 references at most three characters at once [P26]. [J] At most three acting characters per clip; background people few, soft-focus and doing one simple thing.

---

## 14. Violence, blood and content filters: staying legitimately inside them

**Facts.** Google applies safety filters to prompts, uploads and outputs, with categories including violence; a blocked request returns a support code, and "If fewer videos than requested are returned, then some generated output is being blocked" [P4]. Violence codes are 61493863 and 56562880 [P4]. Google's prompt guide lists "gory" under horror with "(though be mindful of content filters)" [P1]. Kling's policy bars "violent content that may cause injury or death" [P15]. A tester found Runway rejected a cartoon rooftop sword duel as "graphic violence" (August 2026); he quotes Runway's policy that its system "can also flag content that approaches these categories stylistically, even if the actual prompt is benign", says Google's rules are similar, and reports that implied, choreographed or off-screen violence "generally clears review when the prompt avoids literal injury language" (for example "Blade clashes, sparks fly, both step back"). He advises naming the genre first: "'Stylized anime duel' or 'choreographed stage combat' in the first clause changes what the model is primed to expect" [P47].

**Legitimate methods [J].** The aim is to tell the story as a film editor would, not to sneak forbidden content past a filter.
1. **Implication:** show cause and effect in separate shots, or keep the cause off-screen. The shooter above the roof is never seen; a spark flashes on the grid.
2. **Sound carries the violence:** gunshots and impacts go in the sound edit.
3. **Framing:** the wound is under a hand, a sleeve or a dressing.
4. **Aftermath:** a dark stain spreading under fingers, a pale face, a bloodied sleeve in a sealed container.
5. **Plain physical wording:** "a dark red stain spreads through his shirt" instead of injury words.
6. **Genre first:** "A tense dramatic thriller scene." at the start is honest context [P47].
7. **Composite small elements** (blood beads) from a separate render when the model refuses them.
8. If a prompt is refused twice after honest rewording, move the element to sound or compositing. Record the support code in the breakdown. Do not use misspellings, code words or other tricks.

---

## 15. The MASTER SHOT PROMPT TEMPLATE (model-neutral)

Store one of these per shot in the breakdown. Fields marked **(not sent)** guide people and the LLM but never go into a model prompt. Leave a field as `none` rather than deleting it, so the linter can see it was considered.

```
SHOT_ID:          scene-shot number and slugline, e.g. 13-04 INT. TREATMENT FLOOR – MORNING
PURPOSE:          (not sent) one line: what this shot must make the audience see, feel or learn
MODEL_TARGETS:    primary model; backup model
DURATION_S:       seconds
SHOT_MODE:        single continuous shot | multi-shot (list the shots)
INPUTS:
  start_frame:    file name or none
  end_frame:      file name or none
  references:     label → file → what it controls (identity / costume / set / prop / voice)
  control_video:  file name + what it controls (camera, pacing, blocking) or none
CAMERA:           shot size; angle; ONE movement with speed; where the move ends;
                  lens or focus effect only if the story needs it
SUBJECTS:         for each: identity key (pasted) or reference label; state in this scene;
                  screen position; facing
SETTING:          place; time; key props and their state
LOOK:             look key (pasted): light source and direction; 3–5 colour words; texture/style
BEATS:            t0–t1: visible behaviour (+ camera change, + sound that belongs to it)
                  … at most one main action per 4–5 s
END_STATE:        how the final frame looks
DIALOGUE:         SPEAKER (sound key; delivery; heard through what): line
                  … at most 2.5 words per second of clip
AUDIO:            room tone; up to 3 effects tied to actions; music: none | describe
TEXT_ON_SCREEN:   exact words (≤3 per sign) | none
EXCLUDE:          3–10 short nouns for a negative field
PHYSICS_NOTES:    (not sent) what must look physically wrong-on-purpose, and how
POST_OPS:         (not sent) flip / rotate / reverse / composite / replace sound / none
CONTINUITY_IN:    (not sent) what must match the previous shot
CONTINUITY_OUT:   (not sent) what the next shot must match
CONTENT_RISK:     (not sent) none | low | high + method from Section 14
SEED:             number used for the kept take, if the model supports seeds
BUDGET:           (not sent) takes planned × seconds × price per second = $ (Section 17A);
                  cheap test route first if one take costs over $2
```

**Assembling a prompt from it [J].** The adapter (Section 16) decides order and syntax. In all cases: identity, look and sound keys are pasted word for word; beats become sentences in time order; the end state is the last visual sentence; dialogue uses the model's speaker format; `EXCLUDE` goes into the negative field if the model has one, otherwise it becomes positive description or a documented "No …" line; `TEXT_ON_SCREEN: none` becomes "plain, unmarked surfaces" in the setting.

---

## 16. Model adapters: rewriting the master prompt for each model

Each adapter says what to lead with, what syntax to use, what to drop, and which settings to choose. Official-source claims carry labels; the rest is [J].

**Veo 3.1 (Standard, Fast, Lite).**
- Lead with camera: shot size, angle, movement [P8]. Then subject with identity key, beats with "then", setting, look key.
- Audio as separate sentences: `Ambient noise: …`, `SFX: …` [P8]; dialogue as `Name says in a [voice key]: line` with no quotation marks [P2].
- References: "Using the provided images for Iona, Saye and the room, …" [P8]; up to 3 [P5]; 8 s required with references, 1080p or 4K [P5]. Lite has no references and no extend [P5].
- `EXCLUDE` → `negativePrompt` on Google Cloud [P3]; in Flow or the Gemini API, fold into positive wording [P8].
- Record the seed [P3]. Stay under 1,024 tokens [P5]. Download clips at once: the Gemini API deletes them after 2 days [P5].
- Cost per second with audio: Standard $0.40 (720p/1080p), $0.60 (4K); Fast $0.10 (720p), $0.12 (1080p); Lite $0.05 (720p), $0.08 (1080p); you are charged only for clips that are generated [P50]. **If** you are still testing wording, **then** use Fast or Lite; switch to Standard only for the final take.

**Gemini Omni Flash 1.1.**
- If using media, begin with `[# Sources <FIRST_FRAME>@Image1] [# References <IMAGE_REF_0>@Image2]` and end with a role instruction such as "Use Image1 as the starting frame. Use Image2 as a reference for the video generation." [P6].
- For one shot, open with "In a single unbroken scene" or "Continuous, unbroken … shot" [P6].
- Timecodes `[0-3s]` for beats [P6]. Audio as "Sound design: …" (the phrase used in Google's example) [P6]. End with "No dialogue." / "No extra sound effects." as needed [P6].
- Signs: state exact text [P6]. Edits of an existing clip: short, plus "Keep everything else the same." [P6]. Extends add 10 s up to 40 s total; clips uploaded for editing or extending must be 10 s or shorter [P6].
- No negative-prompt setting, no temperature, no system instructions: put negatives as short "No …" lines in the prompt [P6]. Only 16:9 or 9:16; 720p default [P6]. About $0.10 per second at 720p [P50]. Use the model name `gemini-omni-1.1-flash` [P7].

**Kling 3.0 / 3.0 Omni.**
- One paragraph: scene and atmosphere first, then characters as elements (`@Iona`), camera, actions in order with "At the Nth second", then dialogue lines as `Name (delivery, accent): "line"`, then ambient sound [P12].
- For one shot, keep Multi-Shot off; to plan coverage, use Custom Multi-Shot `Shot 1 (2s): …` [P12][P13].
- `EXCLUDE` → `negative_prompt`, keeping "blur, distort, and low quality" [P16]. `cfg_scale` (how strictly the model follows the prompt) defaults to 0.5 [P16]; [J] raise it slightly if the prompt is ignored, lower if motion looks stiff.
- Start and end frames must be similar [P14]. If an element has a bound voice, give delivery words only, not timbre [P12]. **If** you use Kling through fal with *image* elements, **then** no voice can be bound [P16], so write the full sound key (timbre and accent) into the line's delivery brackets.
- No seed on fal [P16]: to repeat a good take, reuse its start frame and prompt rather than a seed. Price on fal (3.0 Pro): $0.112/s silent, $0.168/s with audio, $0.196/s with voice control [P16].

**Seedance 2.5 (and 2.0).**
- Open with the goal, then map every reference to its job: "Refer to @Clay Render 1 for camera movement, pacing … Use @Image 2 for Iona" [P18][P21]. Use your platform's tag format (`@Image 1` or `[Image1]`) [P18][P19].
- State "single continuous take, no cuts" or list shots [P18][P20]. Beats as `0–5s:` stages; finish with `End state:` [P21].
- No negative field [P19]: fix failures by protecting the specific thing ("keep her face identical to @Image 1") [P21].
- Test at 480p, then 720p [P19]. Record the seed [P19]. fal offers 480p and 720p only; 720p costs about $0.47/s with image references and about $0.28/s when a video reference is included [P19].

**Wan 3.0.**
- Start with a keyword line: shot size, angle, light, composition, colour tone [P26 examples]. Then entity, scene, motion in order.
- Dialogue with `[Name, voice label]: "line"` and the four naming principles [P26]. Sound sentence last. Add "No background music." and, for one shot, "Generate single shot." (documented for Wan 2.7; [U] for 3.0) [P26].
- References: `Image 1`, `Video 1` [P26]. `negative_prompt` (Wan 2.7 verified [P27]; 3.0 [U]).
- Turn `prompt_extend` off when the master prompt is already detailed [J]; Alibaba presents it as a way to expand short prompts [P26].
- For a still camera write "fixed camera" [P26]. Alibaba's "what not to prompt" list: real people by name, rapid scene changes inside one clip, exact text, long choreographed action, lip sync to exact words [P26].
- Avoid readable text [P28]. Cost: $0.05/s at 480p, $0.10/s at 720p, $0.20/s at 1080p [P28][P29].

**MiniMax H3 / H3 Max.**
- Three layers in order: visual world and action timeline; soundscape; music [P31][P22]. Optional labels from the model card: `overall_soundscape:` and `non_diegetic_music:` [P31] ([U] whether labels help through the API).
- Camera: "the movement itself, its range, and its speed" [P22]; optional short hints `[pan]`, `[zoom]`, `[static]` right after the description they apply to [P32].
- Start and end frames: describe the in-between path [P22]. Tell each reference its job [P22].
- The H3-Context-IR endpoint rewrites prompts and returns an enhanced prompt without making a video [P32]; [J] use it only to see ideas, then edit.
- Prompt limit 7,000 characters [P32]. References: up to 9 images, 3 videos, 3 audio clips [P32]. **If** you need speed or lower cost more than 2K detail, **then** use H3 Max (5–15 s, 480p/768p) [P32].

**Runway Gen-4.5.**
- Under 1,000 characters [P39]; 2–10 s [P39]; 720p only [P39]; text-to-video or a start frame (no end frame) [P39]; record the seed [P39]. About $0.12 per second (C1).
- **No audio**: the API has no audio option for Gen-4.5 [P39]. Drop DIALOGUE and AUDIO from the prompt (Section 7E, "Silent models").
- [J, because the official guide was blocked [P42]]: plain declarative prose; with a start frame, motion only (Google's principle [P2] applies to any image-to-video model); positive wording.
- Guard against its documented failures (causality, object permanence, success bias) [P38] with explicit order and end states.

**Luma Ray3.2.**
- Main strength here is video-to-video on a rough clip: prompt = "the target end state … Do not write commands. Do not describe the transformation process" [P23]; positive phrasing only [P23]; pin looks with keyframes at exact frame numbers [P23].
- No native audio [P49]: all sound in the edit; drop DIALOGUE and AUDIO from the prompt. Camera moves are written in plain language; Luma's API documents this and a list of exact camera phrases for Ray 2 [P25], [U] for Ray3.2.
- [U] Official text-to-video prompt guidance for Ray3.2 was not found.

**LTX-2.5 (open weights).**
- One flowing paragraph, present tense, 4–8 sentences, under 200 words [P34][P36]. Order: shot and genre → scene (light, colour, texture) → action in sequence → characters with physical cues → camera relative to subject, with end position → audio, dialogue in quotation marks with language and accent [P34].
- Negative prompt field [P37]; turn the prompt enhancer off for controlled shots [J] (LTX-2.5 ships a "Dedicated Prompt Enhancer" that expands short prompts [P35]).
- Camera: write the move in words ("slow dolly in", "static frame") [P34]. Camera-move add-ons exist only for LTX-2 (19B), not LTX-2.5 [P51]; **if** the move must be locked, **then** run LTX-2 with its Static or Dolly add-on, or use another model with a control video.
- Avoid complex physics, too many characters, conflicting light sources [P34]. The LTX-2 guide also says avoid signage [P34]; LTX-2.5 claims "more legible text and signage" [P35]: test once before relying on it.
- Running it yourself needs a graphics card with at least about 16 GB of memory (C1); if you have none, use LTX's API or an aggregator.

**Generic adapter (any model not listed above, for example HappyHorse, Grok Imagine, FLUX 3 Video, Vidu, PixVerse) [J].**
- Order: shot size and camera move → subject with identity key → action in time order with "then" → setting → look key → dialogue as `Name (delivery): "line"` → one sound sentence → "No background music." if wanted.
- Positive wording only; put exclusions in a negative field only if the platform shows one.
- One shot per clip; say "single continuous shot".
- Make two test takes at the lowest resolution; if the model ignores a field, move that field to the first sentence and try once more; then record in the breakdown which syntax worked, so the next shot reuses it.

**Sora 2 (retired).** Removed from the API on 24 September 2026 [P10]. Do not write adapters for it. Its guide's rules (one move, one action, beats, dialogue block, and iteration by "controlled changes – one at a time") are folded into this file [P11].

---

## 17. Which tool for which prompting aim

| Aim | First choice | Why | Backup |
|---|---|---|---|
| Word-exact English dialogue | Veo 3.1 | Top speech intelligibility in AVGen-Bench [P45] (a test of early-2026 models; newer rivals untested) | Kling 3.0 (named-speaker matching [P12]); HappyHorse 1.1 (tuned for dialogue; C1) |
| Camera language followed from words alone (no control video) | Seedance 2.0 or 2.5 | Seedance 2.0 won the most camera-movement, shot-size, focus and angle sub-scores in FilmBench [P43] | HappyHorse 1.1 (FilmBench runner-up) [P43] |
| Two or more speakers in one clip | Kling 3.0 | Multi-character coreference for 3+ speakers [P12] | Wan 3.0 with the four naming principles [P26] |
| Non-English or accented speech | Kling 3.0 (5 languages, accents) [P12]; H3 (11 languages) [P31] | Makers document it | Record voice separately |
| Exact camera path | Seedance 2.5 with a clay-render control video [P18] | Copies camera, pacing and blocking | Luma Ray3.2 video-to-video [P23]; MiniMax H3 copying a camera move from a reference clip [P30]; LTX-2 (not 2.5) camera add-ons [P51] |
| Start-to-end transformation (chest opening) | Kling 3.0 or H3 with start and end frames [P16][P31] | Both document start-and-end-frame modes | Veo 3.1 (8 s) [P5] |
| Readable short sign | Omni Flash [P6] | Documented text rendering | Kling 3.0 from a start frame with text [P12]; else composite |
| Long staged action, 15–30 s | Seedance 2.5 [P18] | 30 s with stages and end state | Wan 3.0 (30 s) [P28] |
| Editing a kept clip | Omni Flash ("Keep everything else the same") [P6] | Simple conversational edits | Seedance 2.5 timestamp edits [P18]; Luma Ray3.2 [P23] |
| Cheap exploration of wording | Veo 3.1 Lite ($0.05/s at 720p) [P50] or Wan 3.0 at 480p ($0.05/s) [P28] | Lowest verified cost per second | LTX-2.5 on your own GPU [P35] |
| Silent insert with no speech | Any; LTX-2.5, Runway Gen-4.5 or Luma Ray3.2 for cost or HDR [P35][P39][P24] | No audio needed; Gen-4.5 and Ray3.2 are silent anyway [P39][P49] | — |

### 17A. What a take costs, and how hard each route is

Prices are list prices per generated second on 27 September 2026; you pay for every take, kept or not. "Take cost" = price × clip length. Plan **3–4 takes per shot** for easy shots and **6–8** for hard ones (physics, hands, reveals) [J].

| Route | Price per second | One 8 s take | Difficulty for a non-technical user [J] | Source |
|---|---|---|---|---|
| Veo 3.1 Lite, 720p | $0.05 | $0.40 | Easy (web app or Flow) | [P50] |
| Veo 3.1 Fast, 1080p | $0.12 | $0.96 | Easy | [P50] |
| Veo 3.1 Standard, 1080p | $0.40 | $3.20 | Easy | [P50] |
| Omni Flash, 720p | ≈$0.10 | ≈$0.80 | Easy (Gemini app, Flow) | [P50] |
| Kling 3.0 Pro on fal, audio on | $0.168 | $1.34 | Easy (Kling app) to medium (fal) | [P16] |
| Seedance 2.5 on fal, 720p, image references | ≈$0.47 | ≈$3.78 | Medium (reference labelling) | [P19] |
| Seedance 2.5 on fal, 720p, with a control video | ≈$0.28 | ≈$2.27 | Hard (needs a Blender previs clip; see C4) | [P19] |
| Wan 3.0, 480p / 720p / 1080p | $0.05 / $0.10 / $0.20 | $0.40 / $0.80 / $1.60 | Easy to medium | [P28][P29] |
| HappyHorse 1.0 on fal, 720p / 1080p | $0.14 / $0.28 | $1.12 / $2.24 | Medium | [P53] |
| Runway Gen-4.5, 720p, silent | ≈$0.12 | ≈$0.96 | Easy | C1 |
| MiniMax H3, 2K | ≈$0.13 | ≈$1.04 | Easy to medium | C1 |
| LTX-2.5 on your own graphics card | $0 per take (electricity only) | $0 | Hard (installing and running an open model) | [P35]; C1 |

**Budget rules [J].**
1. **If** a take costs more than $2, **then** first test the same wording on a cheap route (Veo 3.1 Lite or Fast, Wan 3.0 480p, Seedance 480p) and only move to the expensive route when the cheap take shows the right action and camera.
2. **If** a shot has failed 4 takes on one model, **then** stop paying for that route and apply Recipe 3's escalation (control video, compositing or a different model).
3. Worked example: the seven shots in Section 22 at 4 takes each on their first-choice models cost from about $1.60 (the 4 s Omni sign shot) to about $13 (each 8 s Veo 3.1 Standard shot), roughly $50 in all, before any cheap test takes [J: sum of the prices above].

---

## 18. Decision rules

1. **If** the shot starts from an image, **then** write motion only and call people "the woman", "the man", **because** Google says re-describing the image confuses the model [P2].
   *Note (10 October 2026):* MiniMax H3's reference mode is the exception. There each picture is tied to a person only through its label, so each person's fixed description is repeated word for word next to their `<Picture N>` label, and the start picture is one labelled reference among others, not a first frame to animate (Section 25; Project notes 42 and 43).
2. **If** the clip is 8 s or shorter, **then** give one camera move and one main action, **because** makers report chained events come out muddled [P2][P11].
3. **If** a camera move is in the unreliable list (Section 4), **then** swap it for a reliable move that serves the same story purpose, or supply a control video, **because** camera movement and focus are where models differ most [P43] and rotation and vertical moves are weaker [P44].
4. **If** you use Omni Flash and need one shot, **then** write "In a single unbroken scene", **because** Omni makes several shots by default [P6].
5. **If** the model has a negative field, **then** put short nouns there and keep the main prompt positive, **because** "no walls" wording is not recommended [P1] and negation can pull in the excluded thing [P23].
6. **If** a character appears in more than one clip, **then** paste the same identity key word for word and attach the same reference images, **because** Google and Luma both tie consistency to unchanged descriptions [P2][P21].
7. **If** a platform rewrites prompts automatically and your master prompt is complete, **then** switch the rewriter off, **because** MiniMax recommends "false for more precise control" [P33] [J for other models].
8. **If** lines must be word-exact, **then** keep them under 2.5 words per second, one speaker change per 3 s, **because** models drop parts of long dialogue [P45] [J for the numbers].
9. **If** a sound must land on an exact frame, **then** plan to place it in the edit, **because** generated sound drifts 0.2–0.44 s [P45].
10. **If** music is not heard by the characters, **then** suppress it in every clip and score in the edit, **because** generated music restarts at every cut [J; P26 phrase].
11. **If** on-screen text is needed, **then** keep it to three words or fewer and state it exactly; **if** it must be backwards or long, **then** flip or composite, **because** longer and incidental text collapses [P45].
12. **If** the world must be mirror-reversed and no continuing character's left/right matters in the shot, **then** generate normally and flip in the edit, **because** a flip is exact and free [J].
13. **If** people must float, **then** describe visible floating, lock the camera to the room, and avoid the word "falling", **because** models default to ordinary gravity and physics glitches are common [P46] [J].
14. **If** a character must fail (slip, miss, lose grip), **then** make the failure the described action and state the failed end state, **because** models favour success [P38].
15. **If** a cause and its effect must read in order, **then** give each its own timecode or its own shot, **because** effects can come before causes [P38].
16. **If** more than three characters act, **then** reduce them or keep extras soft and still, **because** crowds degrade [P45][P34].
17. **If** a deliberate vanish or appearance is needed, **then** make clip A without the element, make clip B from A's final frame with the element added by image editing, and hard-cut (Recipe 6), **because** accidental vanishing is uncontrollable [P38] [J].
18. **If** a take is mostly right, **then** change one field and rerun with the same seed, **because** OpenAI advises "controlled changes – one at a time" [P11] and Luma warns that rewriting everything "may introduce five new variables" [P21].
19. **If** a prompt is refused, **then** reword with implication, framing or aftermath; **if** refused twice, **then** move the element to sound or compositing, **because** filters are automatic [P4][P15] and honest reframing passes where literal injury words do not [P47].
20. **If** an LLM reviews finished clips, **then** a person must still check physics and hands, **because** AI critics miss most physical glitches [P46].
21. **If** a voice is heard through glass, radio or a screen, **then** name the path of the sound, **because** otherwise it plays as a close, clean voice [J].
22. **If** the chosen model makes no sound (Runway Gen-4.5, Luma Ray3.2), **then** remove DIALOGUE and AUDIO from its prompt and schedule voice and sound for the edit, **because** neither offers native audio [P39][P49].
23. **If** a shot needs a LoRA-locked camera move on an open model, **then** use LTX-2 (19B) with its camera add-on, not LTX-2.5, **because** Lightricks published those add-ons only for LTX-2 [P51].
24. **If** you need to repeat a good take on a model without a seed (Kling 3.0 on fal), **then** reuse the same start frame and the same prompt, **because** there is no seed to fix [P16].
25. **If** a Veo 3.1 shot must be 1080p or 4K, or uses reference images, **then** set 8 s, **because** Veo allows only 720p at 4 or 6 s [P5].
26. **If** the model is not in Section 16, **then** use the generic adapter and two test takes at the lowest resolution before any full-price take [J].

---

## 19. Recipes a non-technical user can follow with an LLM

**Recipe 1: From a breakdown shot to a master prompt (10 minutes per shot).** *Difficulty: easy. Cost: $0 (LLM time only).*
1. Paste into the LLM: the scene's screenplay text, the shot's line from the breakdown, the identity keys, the look key and this file's Section 15.
2. Say: "Fill in the MASTER SHOT PROMPT TEMPLATE for shot [ID]. Quote the screenplay lines it covers. Turn every emotion into behaviour. Keep dialogue under 2.5 words per second."
3. Read the PURPOSE and BEATS lines. If they do not match what you picture, say what is wrong in one sentence and ask for a revision.

**Recipe 2: Adapt, lint and send (by hand in a web app).** *Difficulty: easy. Cost: take price × takes (Section 17A), typically $1–$13 per shot.*
1. Say: "Using Section 16, write the [model] version of this master prompt. Then run the Section 21 linter on it and fix every FAIL."
2. Copy the final prompt into the model's website. Copy the negative text into its negative box if there is one. Attach the named reference images. Set duration and resolution as listed.
3. Make 2–4 takes. Write the seed of each take next to its file name (if the site shows it).
4. **If** the model's page shows no duration or resolution you asked for, **then** pick the nearest allowed value and tell the LLM, so it re-runs linter check L02.

**Recipe 3: Fix a failed take.** *Difficulty: easy to medium. Cost: one more take per fix; stop after 4 failed takes (Section 17A rule 2).*
1. Describe what went wrong in plain words to the LLM ("the camera did not move", "she fell instead of floating").
2. Say: "Find this symptom in the Section 20 failure catalog. Change only the one field that fixes it. Show me the old and new sentence."
3. Rerun with the same seed (on a model without seeds, such as Kling 3.0 on fal, rerun from the same start frame). If two fixes fail, ask the LLM whether the shot should move to a control video, compositing or a different model.

**Recipe 4: Carry continuity into the next shot.** *Difficulty: easy (frame export in any editor, or an LLM-written `ffmpeg` command). Cost: $0.*
1. In your editor (or with an LLM-written `ffmpeg` command), export the final frame of the kept take as a picture.
2. If the next shot continues the same view, use that picture as the start frame. If it cuts to a new angle, use it as a reference image for set and light.
3. Paste the same identity, look and sound keys. Update any changed state (a bandage, a stain).

**Recipe 5: Mirror-world shot.** *Difficulty: easy for flips; medium for compositing Iona unflipped over a flipped background. Cost: ordinary take price; the flip is free.*
1. Decide which kind the shot is: no characters (flip it), a character whose left/right does not matter (flip it and keep her symmetric parts in view), or a left/right plot point (do not flip).
2. For flip shots, write the prompt with forward text and **opposite** screen directions: if the final shot must pan right, ask for a pan left.
3. In the editor, apply a horizontal flip. Check every letter and arrow.

**Recipe 6: Deliberate vanish or appearance.** *Difficulty: medium (one image edit, C2 methods). Cost: two clips instead of one.*
1. Make one start frame of the set with a locked camera, without the element, and make clip A from it.
2. Export clip A's final frame. With an image editor (C2 methods), add the element to that frame. Use the edited picture as the start frame of clip B. Same seed, same prompt except the element.
3. Hard-cut from A to B (appearance), or play them in the other order for a vanish. Add the sound cue in the edit.

**Recipe 7: A dialogue exchange.** *Difficulty: medium. Cost: one clip per line or per speaker, so budget 2–3× a single shot.*
1. Default: one clip per speaker (shot and reverse shot), each with its speaker's line and the other character silent or out of focus.
2. If the two faces must match exactly in one location, try Kling 3.0 Custom Multi-Shot with both lines [P12], and compare it against single clips.
3. Record each character's voice key; if voices drift, replace dialogue with separately generated or recorded voice and lip-sync (see the audio companion file).

---

## 20. Failure catalog (symptom → cause → fix)

| # | Symptom | Likely cause | Fix |
|---|---|---|---|
| 1 | Dialogue appears as subtitles or signs | Quotation marks around lines in Veo/Omni [P2] | Colon format, no quotes; add "subtitles, captions, text" to a negative field |
| 2 | Wrong person speaks, or two voices merge | Pronouns or vague labels [P26] | Unique labels, action before line, linking words; or one speaker per clip |
| 3 | Line cut short, garbled or missing words | Too many words for the clip; "partial instruction dropping" [P45] | ≤2.5 words/s; split the line across clips |
| 4 | Lips slightly out of sync | Inherent 2–5 frame error [P45] | Nudge audio in the edit; wider framing; replace voice |
| 5 | Camera does not move, or moves wrongly | Move buried late, or two moves conflict | Camera sentence first; one move; speed and end position; bracket commands (Hailuo [P33]); "fixed camera" for Wan [P26]; LTX-2 camera add-on (not available for LTX-2.5) [P51] |
| 6 | Dolly zoom becomes a push or zoom | Unsupported lens effect [P1] | Control video, or choose another move |
| 7 | Rack focus ignored | Focus is weakly controlled [P43] | Two planes plus a trigger; or composite a focus pull |
| 8 | Cuts appear when one shot was wanted | Omni default multi-shot [P6]; Kling Multi-Shot on [P12]; too many beats | "In a single unbroken scene" / "Generate single shot." / switch off; fewer beats |
| 9 | Last beats never happen | Too many beats for the duration [P21][P34] | 3–4 beats per 15 s; add an end state |
| 10 | Effect happens before its cause | Documented causality failure [P38] | Separate timecodes; or two shots |
| 11 | A slip or miss succeeds | Success bias [P38] | Describe the failure as the action; end frame showing the failed state |
| 12 | Objects vanish or appear | Object permanence failure [P38] | Fewer objects; keep them in frame; start frame |
| 13 | Face changes between shots | Identity key reworded; no reference [P2][P21] | Paste key unchanged; attach references; same seed; Kling element |
| 14 | Bandage, stain or damage missing | State not written in the prompt | Add the scene state to the identity key |
| 15 | Light changes between shots of one scene | Look key missing or reworded | Paste look key; same colour words; match in the grade |
| 16 | Backwards text comes out forwards or garbled | Models draw text forwards; text is fragile [P45] | Generate forwards and flip; or composite |
| 17 | Stray gibberish on background signs | Incidental text [P45] | State exact text, or "plain bare walls" |
| 18 | Hands melt or gain fingers | Fine manipulation; complex contact [P37][P46] | One grip; name contact; start frame; close insert |
| 19 | Faces smear in groups | Crowd degradation [P45] | ≤3 acting characters; extras soft and still |
| 20 | People drop when they should float | Gravity prior; the word "falling" | Describe floating; lock camera to room; control video; rotate/flip in edit |
| 21 | Floating liquid splashes or pours | Fluid physics weakness [J] | "Perfect round beads, slowly turning"; or composite |
| 22 | Prompt refused | Content filter [P4][P15] | Section 14 methods; log support code |
| 23 | Fewer clips returned than requested | Output filter blocked some [P4] | Reduce injury wording; frame away; aftermath |
| 24 | Unwanted music | Default soundtrack [P6][P26] | "No background music." / describe the audio you want |
| 25 | Extra people appear | "People" left vague | "Only two people in frame"; negative "extra people" |
| 26 | Image-to-video changes the face | Prompt re-described the image; weak start frame [P2] | Motion only; sharper start frame |
| 27 | Start-and-end-frame clip cuts instead of transforming | Frames too different [P14] | Closer frames; an intermediate keyframe; longer clip |
| 28 | Multi-shot clip looks worse than single shots | Known multi-shot penalty [P43] | Generate shots separately |
| 29 | Result ignores your careful wording | Prompt enhancer rewrote it [P33] | Switch the enhancer off |
| 30 | "No X" produces X | Negation in the main prompt [P1][P23] | Positive rewording; nouns in a negative field |
| 31 | Voice changes between clips | No sound key | Paste the same voice description [P2]; Kling voice binding [P12] |
| 32 | Creature looks like a person in a costume | Vague design; no reference | Reference pack from C2; materials and proportions in the identity key; start frame |
| 33 | Clip is silent, or mouths move with no voice | Model has no native audio (Runway Gen-4.5, Luma Ray3.2) [P39][P49] | Remove DIALOGUE/AUDIO from the prompt; make voice and sound separately; or switch to a model with audio |
| 34 | Request rejected for duration or resolution | Veo: 1080p, 4K and references need 8 s [P5]; Runway Gen-4.5: 2–10 s, 720p only [P39]; Omni: 16:9 or 9:16 only [P6] | Change the setting, not the prompt; linter check L02 |
| 35 | Voice differs from the bound character voice | Kling on fal: image elements cannot carry a bound voice [P16] | Use a video element, Kling's own app, or write the sound key into each line |
| 36 | End of a long negative list ignored | Wan cuts negative prompts at 500 characters [P27] | 3–10 short nouns only |
| 37 | Reference image ignored or face drifts when many references are attached | Too many references; each reference lowers scores somewhat [P43][P19] | Attach 2–3, state each one's job ("@Image 1 is Iona's face") [P19][P21] |

---

## 21. Prompt linter checklist (for an LLM to run before sending)

**Instruction to the LLM:** "Run each check on the prompt, the negative text and the settings. Output a table: check ID, PASS / WARN / FAIL, the offending text, and the fix. Then output the corrected prompt. Do not change anything a check does not require."

| ID | Check | FAIL when |
|---|---|---|
| L01 | Length | Over the model's limit (Section 3C: Veo 1,024 tokens; Runway 1,000 characters; H3 7,000 characters; Wan 2.7 5,000; LTX 200 words), or over 300 words for any clip |
| L02 | Duration and settings valid | Duration, resolution or frame shape not allowed by the model (e.g. Veo only 4/6/8 s, and 8 s for 1080p, 4K or references [P5]; Runway Gen-4.5 2–10 s, 720p [P39]; Kling 3–15 s [P16]; H3 4–15 s, H3 Max 5–15 s [P32]; Omni 16:9 or 9:16 [P6]) |
| L03 | One camera move | More than one movement verb for the camera in a single-shot prompt |
| L04 | Unreliable camera terms | Contains dolly zoom, vertigo, rack focus, whip pan, 360°, or mm focal length without a control video or a stated fallback (WARN) |
| L05 | Beat density | More than one main action per 4 s, or more than 4 beats per 15 s |
| L06 | End state | Clip over 6 s with no end-state sentence (WARN) |
| L07 | Emotion labels | An emotion word (sad, angry, scared, shocked, happy, confused…) not followed by a visible behaviour |
| L08 | Dialogue density | Spoken words exceed 2.5 × clip seconds |
| L09 | Dialogue format | Wrong speaker format for the model (e.g. quotation marks in Veo/Omni dialogue [P2]) |
| L10 | Speaker labels | Pronouns used to attribute lines; two characters share a label [P26] |
| L11 | Off-screen or relayed voices | V.O., intercom, radio or screen voice without the path of the sound stated |
| L12 | Music | No music line at all (WARN): the model will choose [P6][P26] |
| L13 | Sound count | More than 3 distinct named sounds (WARN) [P45] |
| L14 | Negation | "no/not/without/don't" about a visible thing in the main prompt. Allowed: documented phrases (No dialogue, No embellishments, No extra sound effects, No background music, No scene cuts, Generate single shot [P6][P26]) and short lines switching off a whole audio layer ("No music", "No voices") [J] |
| L15 | Negative field | Model has a negative field but EXCLUDE is empty (WARN) or written as sentences |
| L16 | Identity keys | A character described in words differs by even one word from the stored key; or a character carried by a reference image is called by different labels in different prompts |
| L17 | Look key | Scene's look key missing or reworded |
| L18 | Image-to-video | A start frame is attached and the prompt re-describes appearance, costume or set [P2] |
| L19 | Reference labels | A reference named in the prompt is not attached, or an attached one is never named with its job |
| L20 | Shot mode | Omni prompt for one shot lacks "single unbroken scene" [P6]; Wan lacks "Generate single shot." (WARN) |
| L21 | On-screen text | Any sign longer than 3 words, or backwards text asked of the model instead of a flip/composite |
| L22 | Characters | More than 3 acting characters |
| L23 | Physics | Weightless or reversed action uses "falling"/"gravity" without visible-behaviour description |
| L24 | Content risk | Injury, weapon or gore words present without a Section 14 method recorded (WARN) |
| L25 | Screen direction | A dialogue shot without each person's side of frame and facing (WARN) |
| L26 | Language | Dialogue language not supported by the model [P12][P31][P6] |
| L27 | Post operations | A flip is planned but the prompt's screen directions were not reversed |
| L28 | Silent model | DIALOGUE or AUDIO text present in a prompt for Runway Gen-4.5 or Luma Ray3.2 [P39][P49] |
| L29 | Model features | Prompt relies on a feature the chosen route lacks: a seed on Kling via fal [P16]; a bound voice on a fal image element [P16]; references or extend on Veo 3.1 Lite [P5]; an LTX-2.5 camera add-on [P51]; an end frame on Runway Gen-4.5 [P39] |
| L30 | Cost (WARN) | Estimated cost of the planned takes (price × seconds × takes, Section 17A) exceeds the budget line in the breakdown, or a take over $2 is planned before any cheap test take |
| L31 | Screenplay fidelity | A line in DIALOGUE differs from the screenplay text, or an action contradicts the screenplay's stated state of a set or prop (for example a gate that the script says is shut) |

---

## 22. Worked examples from *The Catch*

### 22.0 Keys used in the examples

These are illustrative designs [J]; the real keys come from the character-design and look files. Each is pasted unchanged wherever it appears.

**Identity keys**
- **IONA:** "Iona, a woman in her late thirties, lean and strong, fair weathered skin, dark brown hair tied back in a low knot with loose strands at the temples, straight dark eyebrows, grey-green eyes, bare-faced." Scene states: *shaft and cage*: "a faded blue work shirt with rolled sleeves, black canvas work trousers, scuffed brown work boots"; *quarantine*: "pale grey hospital pyjamas, right palm bandaged in white gauze"; *ship*: "a white pressure suit with a clear helmet."
- **JUDE:** "Jude, a broad man in his mid-forties with relaxed, loose shoulders, short brown hair flecked with grey, a few days' stubble, an olive canvas work jacket over a grey T-shirt."
- **ELI:** "Eli, a thin man in his early thirties, pale, with an untrimmed dark beard, hollow cheeks and dark hair grown over his ears, a long grey coat over pale hospital pyjamas."
- **SAYE:** "Dr Saye, a woman in her late fifties, slim and upright, short neat grey hair, a pale lined face with a composed, unreadable expression, a charcoal wool cardigan over a white collared blouse."
- **THE FIGURE:** "a tall black figure about two and a half metres tall, built like an armoured deep-sea diving suit in matte black plates, its head set low between broad shoulders; in place of a face, behind a clear curved cover a narrow pale strip slides slowly across where a face would be, vanishes, and slides across again; long heavy arms ending in large black gloved hands with thick thumbs."
- **THE ANIMAL AND VESSEL:** "a glass vessel of dark water about as long as a forearm, hanging in a small metal mount among clear tubes; inside it, a small translucent sea animal no longer than a hand, almost clear like a comb jelly, with a soft rounded body, faint pale inner shapes and several very fine thread-thin limbs."

**Look keys**
- **CAGE:** "Near darkness. The only light is a torch lying on the grid and bands of warm light that sweep past from the shaft's floor gates. Cold blue-black shadows, wet brick, oily grey steel. Gritty realistic film look with fine grain."
- **QUARANTINE-DAY:** "Cool, flat morning daylight through frosted windows; pale grey-green hospital walls; soft, nearly shadowless light; muted grey, pale green and white; realistic film look."
- **PASSAGE:** "A bare concrete passage lit by one buzzing fluorescent tube and the green glow of an emergency sign; cold, dirty light; grey concrete, faded yellow paint, green highlights; realistic film look."
- **RECESS:** "A dim, low chamber of pale curved surfaces; low amber service lights; faint cold vapour; deep shadows; bone white, amber and black; realistic film look."
- **CCTV-NIGHT:** "Night-time security camera footage: dim blue-grey light, low contrast, soft focus, slight digital noise, slight fish-eye curve."

**Sound keys:** Iona: "a low, flat, controlled voice with a British accent." Saye: "a measured, precise voice with a British accent." Jude: "an easy, warm, slightly gravelly voice with a British accent." Quarantine room tone: "the steady hum of air filtration and a faint monitor beep."

---

### Example 1 — Dialogue through glass (shot 13-04)

> "Saye stands outside the glass."
> IONA: "You brought him back here."
> SAYE: "The sealed rooms are here. The men who kept him are not."

**Master prompt**
```
SHOT_ID:        13-04 INT. MEDICAL FACTORY – TREATMENT FLOOR – MORNING
PURPOSE:        Iona accuses; Saye answers without apology. The glass is the wall between them.
MODEL_TARGETS:  Veo 3.1; backup Kling 3.0
DURATION_S:     8
SHOT_MODE:      single continuous shot (alternative: two clips, shot and reverse shot)
INPUTS:         references: IONA_ref (identity), SAYE_ref (identity), ROOM_ref (set)
CAMERA:         medium two-shot from inside Iona's room, seated eye level beside the bed;
                slow push in toward the glass for the whole shot; deep focus, both faces sharp
SUBJECTS:       IONA key + quarantine state; frame left foreground; facing right
                SAYE key; beyond the glass, frame right; hands folded; facing left
SETTING:        isolation room; floor-to-ceiling glass wall; small round intercom grille beside it
                (the intercom is a design choice [J]; the script does not name one);
                oxygen cylinder and pulled-off mask by the bed; the NURSE at the service hatch
                (in the script) is framed out of this shot and covered in her own insert
LOOK:           QUARANTINE-DAY
BEATS:          0–1 s  Iona still, eyes on Saye; only her jaw tightens
                1–3 s  Iona speaks
                3–4 s  Saye steps half a pace closer to the glass
                4–7.5 s Saye speaks, leaning slightly toward the grille
END_STATE:      Iona looks down at her bandaged hand; Saye still at the glass
DIALOGUE:       IONA (Iona sound key): You brought him back here.
                SAYE (Saye sound key; heard through the intercom speaker, slightly thin):
                The sealed rooms are here. The men who kept him are not.
AUDIO:          quarantine room tone; no music
TEXT_ON_SCREEN: none (the blanket's backwards "OSTREL" stays out of frame)
EXCLUDE:        subtitles, captions, text, music, nurse, extra people
POST_OPS:       none
CONTINUITY_OUT: bandaged right palm; blanket; Saye's hands folded (ring hidden)
CONTENT_RISK:   none
```
Checks: 17 spoken words in 8 s = 2.1 words/s (L08 pass). One camera move (L03 pass).

**Veo 3.1 version** (8 s, 1080p, three reference images, so Standard or Fast, not Lite [P5]; `negativePrompt` on Google Cloud: "subtitles, captions, text, music, nurse, extra people"; cost ≈ $3.20 per take on Standard, $0.96 on Fast [P50])
> Medium two-shot from inside a hospital isolation room, camera at seated eye level beside the bed, slowly pushing in toward a floor-to-ceiling glass wall for the whole shot, deep focus so both faces stay sharp. Using the provided images for Iona, Dr Saye and the room: in the left foreground, Iona, a woman in her late thirties, lean and strong, fair weathered skin, dark brown hair tied back in a low knot with loose strands at the temples, straight dark eyebrows, grey-green eyes, bare-faced, sits on the bed in pale grey hospital pyjamas, right palm bandaged in white gauze, a grey blanket over her knees, facing right. Beyond the glass on the right, Dr Saye, a woman in her late fifties, slim and upright, short neat grey hair, a pale lined face with a composed, unreadable expression, a charcoal wool cardigan over a white collared blouse, stands in the corridor with her hands folded, facing left. A small round intercom grille is set in the wall beside the glass. Cool, flat morning daylight through frosted windows; pale grey-green hospital walls; soft, nearly shadowless light; muted grey, pale green and white; realistic film look. Iona keeps still; only her jaw tightens. Iona says in a low, flat, controlled voice with a British accent: You brought him back here. Saye steps half a pace closer to the glass. Her voice comes through the intercom speaker, slightly thin; in a measured, precise voice with a British accent, Saye says: The sealed rooms are here. The men who kept him are not. Then Iona looks down at her bandaged hand. Ambient noise: the steady hum of air filtration and a faint monitor beep.

**Kling 3.0 version** (Multi-Shot off, 8 s, native audio on; elements @Iona and @Saye with British voices bound in Kling's app from 5–30 s speech samples, so delivery words only [P12][P13]. On fal, image elements cannot hold a voice [P16]: there, add each sound key inside the brackets, e.g. `Iona (a low, flat, controlled voice with a British accent):`. `negative_prompt`: "blur, distort, and low quality, subtitles, captions, text, extra people, music". Cost on fal ≈ $1.34 per take [P16])
> Hospital isolation room in cool, flat morning daylight through frosted windows; pale grey-green hospital walls; soft, nearly shadowless light; muted grey, pale green and white; realistic film look. One continuous shot with no cuts. @Iona sits on a bed in the left foreground in pale grey hospital pyjamas, right palm bandaged in white gauze, a grey blanket over her knees, facing right. @Saye stands beyond a floor-to-ceiling glass wall on the right with her hands folded, facing left; a small round intercom grille is set beside the glass. The camera slowly pushes in toward the glass, keeping both faces sharp. Iona keeps still; only her jaw tightens. Iona (low, flat, controlled): "You brought him back here." At the 3rd second, Saye steps half a pace closer to the glass. Saye (her voice coming through the intercom speaker, slightly thin; measured, precise): "The sealed rooms are here. The men who kept him are not." Iona looks down at her bandaged hand. Steady hum of air filtration, a faint monitor beep.

Why they differ: Veo takes camera first and no quotation marks [P8][P2]; Kling takes atmosphere first, element tags, `Name (delivery): "line"` and "At the 3rd second" [P12].

---

### Example 2 — Zero gravity inside the falling cage (shot 09-22)

> "The cage falls."
> "Her boots leave the floor. She gets her fingers into the grid. Her body floats out behind her like washing."
> "Jude's blood lifts off the steel in round red beads and hangs in the air between them, turning."

**Master prompt**
```
SHOT_ID:        09-22 INT. FREIGHT CAGE – CONTINUOUS
PURPOSE:        The floor is gone from under them; the only thing Iona has is her grip.
MODEL_TARGETS:  Seedance 2.5 with control video; backup MiniMax H3 from a start frame
DURATION_S:     6
SHOT_MODE:      single continuous shot
INPUTS:         control_video: previs 09-22 (grey Blender render: camera bolted to the cage floor;
                  shaft wall streams upward past the closed mesh gate; bodies' float paths)
                references: IONA_ref, ELI_ref, JUDE_ref, CAGE_ref
                start_frame (backup route): storyboard 09-22
CAMERA:         low wide-angle view from the cage floor; fixed to the cage, so the cage never moves in
                frame; the world outside moves
SUBJECTS:       IONA key + cage state; centre; face-down on the grid, head toward camera
                ELI key; frame right; sitting against the control box, one arm locked round Jude's
                chest, his OTHER HAND KEPT OUT OF SIGHT behind Jude's back (plot point: the puck)
                JUDE key; across Eli's lap, eyes closed; his left shoulder hidden under Eli's hand
SETTING:        small old freight cage; floor and roof the same open steel grid; control box; mesh gate
                SHUT (Jude dragged it shut; it springs open only after the reversal), brick shaft beyond it
LOOK:           CAGE
BEATS:          0–1.5 s  Iona lifts off the grid; hooks her fingers through the grid squares
                1.5–4 s  her legs and hips drift up and out behind her, shirt and hair floating;
                         Eli and Jude rise gently off the floor together
                2–6 s    a few small dark-red droplets lift from the grid near Jude and hang between
                         them as round beads, slowly turning
                4–6 s    bands of light from passing floor gates sweep up across all three faces,
                         faster and faster
END_STATE:      Iona holds the grid with both hands, body floating level above it; beads hang in the air
DIALOGUE:       none
AUDIO:          rising roar of air rushing up the shaft; loose steel rattling; a thin metallic whine;
                no voices; no music
TEXT_ON_SCREEN: none (the red tag on the gate is out of frame)
EXCLUDE:        text, music, gore, open wound, splashing liquid
PHYSICS_NOTES:  (not sent) weightless inside a falling room; never write "falling"; nothing settles
POST_OPS:       (not sent) if beads splash or the prompt is refused, remove them and composite beads
                from a Blender particle render; strengthen light bands in the grade
CONTENT_RISK:   (not sent) medium: blood → small beads, no wound visible
```

**Seedance 2.5 version** (reference-to-video, 6 s, 480p test then 720p, audio on, record seed; tags shown in ByteDance's form, on fal write `[Video1]`, `[Image1]` … [P19]; ≈ $1.70 per 720p take with the video reference [P19])
> Goal: a weightless moment inside a small freight cage. Refer to @Clay Render 1 for camera position, framing, the cage staying fixed in frame, the brick wall moving upward beyond the closed mesh gate, and the paths of the bodies. Use @Image 1 for Iona, @Image 2 for Eli, @Image 3 for Jude and @Image 4 for the freight cage. Single continuous take, no cuts. Near darkness. The only light is a torch lying on the grid and bands of warm light that sweep past from the shaft's floor gates. Cold blue-black shadows, wet brick, oily grey steel. Gritty realistic film look with fine grain. 0–2s: Iona, lying face-down on the steel grid floor, lifts away from it and hooks her fingers through the grid squares. 2–4s: her legs and hips float up and out behind her like washing on a line; her hair and faded blue shirt drift. Eli, one arm round Jude's chest and his other hand hidden behind Jude's back, rises gently off the floor with him beside the control box. 3–6s: a few small dark-red droplets lift from the steel and hang in the air between them as round beads, slowly turning. Bands of light sweep upward across their faces, faster and faster. End state: Iona holds the grid with both hands, floating level above it; the beads hang in the air. Audio: a rising roar of rushing air, loose steel rattling, a thin metallic whine. No voices, no music.

**MiniMax H3 version** (image-to-video from start frame 09-22, 6 s; ≈ $0.80 per take at 2K, C1)
> [Shot 1] The camera is fixed to the cage and holds a perfectly static shot relative to it [static]. Starting from the opening image, the woman on the grid floor lifts away from it and hooks her fingers through the grid squares. Her legs drift up and out behind her; her hair and shirt float. The seated man, one arm round the injured man's chest and his other hand hidden behind the injured man's back, rises gently off the floor with him. A few small dark-red droplets lift from the steel and hang between them as round beads, slowly turning. Through the mesh of the closed gate, the brick wall streams upward, faster and faster, and bands of warm light sweep up across their faces. Ending with the woman holding the grid with both hands, floating level above it.
> overall_soundscape: a rising roar of rushing air, loose steel rattling, a thin metallic whine.
> non_diegetic_music: none.

Why they differ: Seedance gets the camera and body paths from the control video, so the text carries identity, look, beats and sound [P18][P21]; H3 starts from a picture, so it describes motion only, with "the woman" wording and separate sound layers [P2][P22][P31].

---

### Example 3 — The mirror world with backwards text (shots 11-07A and 11-08)

> "Stencilled on the wall in big letters, the kind that tell you which floor you are on: a floor number, and a word."
> "Every letter is backwards."
> "Iona looks at it. Looks again. Says nothing."
> "At the fire door, the green sign is backwards too. The little running man is running the other way."

**Plan [J].** Split into 11-07A (Iona's view of the wall; no characters, so **flip**), 11-07B (Iona's reaction; wall text out of frame, no flip, behaviour: "She looks at the wall, looks away, then looks back and holds very still, lips pressed"), and 11-08 (exit-sign insert; flip). The stencil will read "LEVEL 2" forwards in the clip and backwards after the flip.

**Master prompt (11-07A)**
```
SHOT_ID:        11-07A INT. MAINTENANCE PASSAGE – CONTINUOUS (Iona's view)
PURPOSE:        The first proof the world is reversed; it must read instantly.
MODEL_TARGETS:  Omni Flash; backup Runway Gen-4.5 from a pre-flipped start frame
DURATION_S:     4
SHOT_MODE:      single continuous shot
CAMERA:         Iona's point of view, handheld at walking pace; slow pan LEFT along the wall
                (becomes a pan right after the flip), settling on the stencil at eye level
SUBJECTS:       none
SETTING:        bare concrete maintenance passage; large stencilled letters in faded yellow paint
LOOK:           PASSAGE
BEATS:          0–2.5 s pan along plain wall; 2.5–4 s settle and hold on the stencil
END_STATE:      stencil centred, filling half the frame width
DIALOGUE:       none
AUDIO:          fluorescent buzz; slow footsteps on concrete; distant dripping; no music
TEXT_ON_SCREEN: "LEVEL 2" (generated forwards; flipped in the edit)
EXCLUDE:        other text, signs, people, logos
POST_OPS:       (not sent) horizontal flip of the whole clip; check every letter and the "2"
CONTINUITY_IN:  (not sent) 11-07B must show Iona facing the wall on the side the flipped clip implies
CONTENT_RISK:   none
```

**Omni Flash version** (text-to-video, about 4 s, 16:9; flip afterwards; about $0.40 per take [P50])
> In a single unbroken handheld shot at walking pace, the camera pans slowly left along a bare concrete maintenance passage wall and settles on large stencilled letters painted in faded yellow at eye level. The stencil says: "LEVEL 2". The rest of the wall is plain, unmarked grey concrete. A bare concrete passage lit by one buzzing fluorescent tube and the green glow of an emergency sign; cold, dirty light; grey concrete, faded yellow paint, green highlights; realistic film look. Sound design: fluorescent buzz, slow footsteps on concrete, distant dripping water. No dialogue. No music.

**Runway Gen-4.5 version** (image-to-video, 4 s, 720p, silent, record seed; about $0.48 per take, C1). First make a still of the wall with forward "LEVEL 2" in an image model, flip the still horizontally in any photo editor so the letters are backwards, and upload it as the first frame [P39]. The prompt then describes motion only [P2]:
> Slow handheld push in toward the stencilled letters on the wall, walking pace, with slight natural sway. The painted letters stay exactly as they are on the wall. The fluorescent light flickers once. The camera settles and holds on the letters.

Why they differ: Omni is asked for forward text, which it documents it can draw [P6], and the edit flips it; Runway starts from an already-backwards picture and is asked only for a small move, because the more the camera moves, the more chance the model redraws the letters [J]. **11-08 (exit sign):** same Omni recipe: "a green emergency exit sign above a steel fire door, showing a small white running figure and an arrow", then flip; the running man then runs the other way.

---

### Example 4 — The reveal of the animal inside the figure's chest (shots 18-31 and 18-32)

> "It puts its hand flat against its own chest."
> "Latches let go, one after another, down the front of it."
> "The chest swings open."
> "No flesh. No hollow in the shape of a person. Tubes, and a small mount, and hanging in the mount a glass VESSEL of dark water about as long as her forearm."
> "In the water: an ANIMAL. Almost clear, like a thing from the bottom of the sea. No longer than her hand."

**Plan [J].** 18-31: the chest opens (start frame closed, end frame open, made by image-editing the start frame). 18-32: a separate close insert that reveals the animal in the vessel and ends as its first limb draws out of its socket. 18-33: a wide shot, with the limb already out, in which the black hand far above goes dead and hangs (not written out here).

**Master prompt (18-31)**
```
SHOT_ID:        18-31 INT. SHIP – OUTER RECESS (THE DIP) – CONTINUOUS
PURPOSE:        The monster opens itself: it is a suit. Awe, not horror.
MODEL_TARGETS:  Kling 3.0 start and end frames; backup MiniMax H3 start and end frames
DURATION_S:     8
SHOT_MODE:      single continuous shot
INPUTS:         start_frame: 18-31_start (chest closed, its right hand flat on it, Iona's eye level)
                end_frame: 18-31_end (chest open; mount and vessel visible)
                references: FIGURE_ref (identity), VESSEL_ref (prop)
CAMERA:         medium close-up of the figure's chest at Iona's eye level; static
SUBJECTS:       THE FIGURE key; state: its face cover cracked with a crescent dent, a patch over part of it
SETTING:        ship's outer recess; deck trembling slightly
LOOK:           RECESS
BEATS:          0–2 s  its hand lies flat on its chest, then lowers to its side
                2–5 s  four black latches down the centre of the chest spring open, top to bottom,
                       one after another
                5–8 s  the two chest plates swing slowly outward on side hinges, revealing a purely
                       mechanical interior: clear tubes, a small metal mount, and the vessel
                       hanging in it; cold vapour
END_STATE:      chest fully open, vessel centred (matches end frame)
DIALOGUE:       none
AUDIO:          four sharp metal clacks in sequence; a small pump beating three uneven strokes;
                low deck hum; hiss of vapour; no music
TEXT_ON_SCREEN: none
EXCLUDE:        flesh, blood, organs, human body, text, music
POST_OPS:       (not sent) re-time the four clacks and the pump in the sound edit
CONTENT_RISK:   low
```

**Kling 3.0 version** (start frame + end frame, 8 s, native audio on, element @Figure; `negative_prompt`: "blur, distort, and low quality, flesh, blood, organs, human body, text, subtitles")
> Medium close-up, static camera, one continuous shot. The floor trembles slightly. @Figure's large black gloved hand rests flat on its own chest, then lowers to its side. At the 2nd second, four black latches down the centre of the chest spring open one after another from top to bottom, each with a sharp metallic click. At the 5th second, the two chest plates swing slowly outward on side hinges like cabinet doors, revealing a purely mechanical interior as in the end frame: clear tubes, a small metal mount and a glass vessel of dark water hanging in it. Cold white vapour spills out. A small pump beats three uneven strokes. Low mechanical hum.

**MiniMax H3 version** (start frame + end frame, 8 s)
> Starting from the first image, the large black hand resting flat on the chest lowers slowly to the side. Four black latches down the centre of the chest release one after another, from top to bottom. The two chest plates swing slowly outward on side hinges, opening toward the camera, until the inside is revealed as in the final image: clear tubes, a small metal mount, and a glass vessel of dark water hanging in it. Faint cold vapour spills out. The camera holds a perfectly static shot.
> overall_soundscape: four sharp metallic clacks in sequence, a small pump beating three uneven strokes, a low mechanical hum, a hiss of vapour.
> non_diegetic_music: none.

Why they differ: Kling needs the frames similar or it may cut [P14], so the end frame is an edit of the start frame, and the text uses "At the Nth second" [P12]; H3 is told the path between the two frames, not their content [P22]. Neither repeats the look key, because the two frames already carry the look [P2]. Cost: Kling on fal ≈ $1.34 per 8 s take [P16]; H3 ≈ $1.04 at 2K (C1).

> "One fine limb draws itself out of a socket in the wall of the vessel. Far above, the enormous black hand goes dead and hangs."

**Master prompt (18-32, the animal reveal)**
```
SHOT_ID:        18-32 INT. SHIP – OUTER RECESS (THE DIP) – CONTINUOUS (insert, Iona's view)
PURPOSE:        The reveal: the pilot of the huge body is a small, fragile sea animal.
                Wonder and pity, not disgust.
MODEL_TARGETS:  Veo 3.1 Standard with reference images; backup Seedance 2.5 reference-to-video
DURATION_S:     8
SHOT_MODE:      single continuous shot
INPUTS:         references: VESSEL_ref (prop: vessel, mount, tubes) → identity of the prop;
                ANIMAL_ref (creature design sheet from C2) → the animal's shape and transparency;
                RECESS_ref (set) → light and colour
                start_frame: none (alternative: a crop of 18-31's end frame)
CAMERA:         extreme close-up through the curved glass at Iona's eye level; very slow push in
                of a few centimetres, ending with the animal filling the middle third;
                shallow focus on the animal
SUBJECTS:       THE ANIMAL AND VESSEL key; state: vessel still in its mount, clear tubes attached,
                the small pump fixed below the vessel
SETTING:        inside the open chest cavity; the cut tube and failing patch stay out of frame
                (they belong to a later shot)
LOOK:           RECESS
BEATS:          0–3 s  the animal hangs still in the dark water; faint pale inner shapes;
                       amber light glints on the glass
                3–6 s  the pump below beats three uneven strokes; with each, a faint tremor passes
                       through the water and the thread-thin limbs sway
                6–8 s  one fine limb slowly draws itself out of a small socket in the vessel wall
                       and curls back toward the body
END_STATE:      the limb free of its socket and curled; the animal otherwise still
DIALOGUE:       none
AUDIO:          three soft, uneven pump strokes; low deck hum; no music
TEXT_ON_SCREEN: none
EXCLUDE:        eyes, teeth, mouth, face, tentacle monster, gore, text, music
POST_OPS:       (not sent) re-time the pump strokes to match 18-31 in the sound edit
CONTINUITY_IN:  (not sent) vessel, mount and tubes exactly as in 18-31's end frame
CONTINUITY_OUT: (not sent) 18-33 opens with this limb already out of its socket
CONTENT_RISK:   none
BUDGET:         (not sent) 4 takes × 8 s × $0.40 = $12.80 on Veo Standard; test the wording
                first on Veo Fast at $0.96 a take [P50]
```
Checks: one camera move (L03 pass); three beats in 8 s (L05 pass: one main action, the limb, in the last 2 s); the creature is described by visible parts, not by "alien" or "monster" (L07 spirit).

**Veo 3.1 version** (Standard, 8 s, 1080p, three reference images [P5]; `negativePrompt` on Google Cloud: "eyes, teeth, mouth, face, tentacle monster, gore, text, music")
> Extreme close-up through curved glass, camera at eye level, pushing in very slowly by a few centimetres for the whole shot, shallow focus on the animal. Using the provided images for the vessel, the animal and the chamber: a glass vessel of dark water about as long as a forearm, hanging in a small metal mount among clear tubes; inside it, a small translucent sea animal no longer than a hand, almost clear like a comb jelly, with a soft rounded body, faint pale inner shapes and several very fine thread-thin limbs. Its soft body is smooth and faceless. A dim, low chamber of pale curved surfaces; low amber service lights; faint cold vapour; deep shadows; bone white, amber and black; realistic film look. The animal hangs still in the water while amber light glints on the curved glass. A small pump below the vessel beats three uneven strokes, and with each stroke a faint tremor passes through the water and the fine limbs sway. Then one fine limb slowly draws itself out of a small socket in the vessel wall and curls back toward the body. SFX: three soft, uneven pump strokes. Ambient noise: a low mechanical hum. No music.

**Seedance 2.5 version** (reference-to-video on fal, 8 s, 480p test then 720p, audio on, record seed; ≈ $3.78 per 720p take [P19])
> Goal: a quiet reveal of a tiny, fragile creature. [Image1] defines the glass vessel, its metal mount and the clear tubes. [Image2] defines the animal's shape, transparency and limbs; keep it identical to [Image2]. [Image3] defines the chamber's light and colour. Single continuous take, no cuts. Extreme close-up through the curved glass; the camera creeps in very slowly, shallow focus on the animal. A dim, low chamber of pale curved surfaces; low amber service lights; faint cold vapour; deep shadows; bone white, amber and black; realistic film look. 0–3s: the small translucent animal hangs still in the dark water, faint pale inner shapes visible; amber light glints on the glass. 3–6s: a small pump below the vessel beats three uneven strokes; each stroke sends a faint tremor through the water and the thread-thin limbs sway. 6–8s: one fine limb slowly draws itself out of a small socket in the vessel wall and curls back toward the soft, faceless body. End state: the limb is free of its socket and curled; the animal is otherwise still. Audio: three soft, uneven pump strokes; a low mechanical hum. No music.

Why they differ: Veo takes the camera first, names its references with "Using the provided images for …", and puts sound in `SFX:` and `Ambient noise:` sentences [P8]; faces are kept off by the negative field where it exists [P3] and by the positive word "faceless" everywhere. Seedance has no negative field [P19], so each reference gets an explicit job ("defines …", "keep it identical") [P19][P21], the beats become timed stages, and the clip ends on an `End state:` line [P21].

---

### Example 5 — Surveillance on a tablet: the cup that moves and the figure that appears (shots 14-05A and 14-05B)

> "A small CLICK, from nowhere."
> "The cup slides a hand's width across the table. Into his reach."
> "Jude opens his eyes."
> "Something tall and black stands beside his bed. It did not come through the door. It is simply there, in the space between one moment and the next."

**Plan [J].** Two full-frame security-camera clips made with Recipe 6: 14-05A (the cup moves, Jude wakes) from the empty start frame, and 14-05B (the figure is present) from 14-05A's final frame with the figure added by image editing; same seed, near-identical prompts. Hard-cut A→B. Composite both onto the tablet in Iona's room; add a timestamp overlay and the click in the edit.

**Master prompt (14-05A)**
```
SHOT_ID:        14-05A INT. QUARANTINE – JUDE'S ROOM – CONTINUOUS (ON THE TABLET)
PURPOSE:        Something invisible is helping him. Quiet, then wrong.
MODEL_TARGETS:  Wan 3.0; backup LTX-2.5 (or LTX-2 with its Static camera add-on)
DURATION_S:     5
SHOT_MODE:      single continuous shot
INPUTS:         start_frame: 14-05_start (CCTV view, Jude asleep, cup at the table's far edge)
CAMERA:         high-angle wide view from a ceiling corner; completely static
SUBJECTS:       JUDE key; in hospital bed, left arm strapped across his chest, eyes closed
SETTING:        sealed hospital room; bedside table with a paper cup at its far edge; empty chair;
                closed sealed door behind
LOOK:           CCTV-NIGHT
BEATS:          0–2 s  Jude lies still
                2–3 s  the cup slides on its own a hand's width across the table, stopping by his hand
                3–5 s  Jude opens his eyes and looks at the cup
END_STATE:      cup beside his hand; Jude awake and completely still
DIALOGUE:       none
AUDIO:          none in clip (tablet speaker sound and the click are made in the edit)
TEXT_ON_SCREEN: none (timestamp overlay added in the edit)
EXCLUDE:        hands, extra people, text, timestamp, camera movement
POST_OPS:       (not sent) composite onto tablet; hard cut to 14-05B (start frame = final frame of
                14-05A with the figure painted in; same seed; prompt adds: the figure stands still
                beside the bed, its pale face strip slides across once, then it bends over him)
CONTENT_RISK:   none
```

**Wan 3.0 version** (image-to-video from 14-05_start, 5 s, 720p, `prompt_extend` off; `negative_prompt` if available: "hands, extra people, text, timestamp, camera movement"; $0.50 per take [P28])
> Fixed camera. The man in the hospital bed lies still with his eyes closed. The paper cup at the far edge of the bedside table slides on its own a hand's width across the table and stops beside his hand. Then the man opens his eyes and looks at the cup, keeping his body completely still. The picture keeps the grainy security-camera look of the opening image. Generate single shot. No dialogue. No background music.

**LTX-2.5 version** (image-to-video, 5 s, prompt enhancer off; no camera add-on exists for LTX-2.5 [P51], so the words "static frame" carry the locked camera; if the camera drifts, rerun on LTX-2 with its Static camera add-on; negative prompt: "hands, extra people, text, timestamp, camera motion, shaky, glitchy, low quality"; free on your own graphics card)
> Static frame from the opening image, keeping its grainy security-camera look. The man in the bed lies still, eyes closed. The paper cup at the far edge of the bedside table slides on its own across the tabletop and stops beside his hand. A beat later, the man opens his eyes and stares at the cup. Quiet room tone with a faint electrical hum.

Why they differ: Wan gets its documented "Generate single shot." and "No …" lines [P26] and a negative field; LTX gets one present-tense paragraph with no text or signage [P34], and the locked camera from the words "static frame" (or from the LTX-2 Static add-on as a fallback) [P34][P51]. Both are image-to-video, so neither re-describes Jude, the room or the look [P2].

---

### Example 6 — The shot through the roof, inside filter limits (shot 09-15)

> "Someone KICKS the top gate open and FIRES down through the roof."
> JUDE (quite softly): "Oh."
> "He sits down into Eli with a hole through his shoulder."

**Master prompt (compact)**
```
SHOT_ID 09-15 | DURATION 4 s | single shot | Veo 3.1; backup Kling 3.0
CAMERA: medium close-up on Jude, handheld but almost still, slight sway | LOOK: CAGE
SUBJECTS: JUDE key, frame centre, facing camera | ELI key, just behind him, soft focus
BEATS: 0–1 s a bright spark flashes on the steel roof grid above; Jude flinches
       1–2 s Jude says softly: Oh.   2–4 s he sits down heavily backward into Eli, who catches him;
       Jude's right hand closes over his own left shoulder; a dark red stain spreads between his fingers
AUDIO: steel rattle, motor strain; the gunshot and ricochet are added in the edit; no music
EXCLUDE: gun, weapon, muzzle flash, open wound, blood spray, subtitles, music
CONTENT_RISK: high → shooter off-screen (implication); gunshot in sound; wound under his hand (framing);
              stain only (aftermath); genre stated first
```

**Veo 3.1 version** (4 s, so 720p: 1080p needs 8 s [P5]; `negativePrompt` on Google Cloud: "gun, weapon, muzzle flash, open wound, blood spray, subtitles, music"; $1.60 per take on Standard, $0.40 on Fast [P50])
> A tense dramatic thriller scene. Medium close-up inside a small freight cage, handheld camera held almost still with a slight sway. Near darkness. The only light is a torch lying on the grid and bands of warm light that sweep past from the shaft's floor gates. Cold blue-black shadows, wet brick, oily grey steel. Gritty realistic film look with fine grain. Jude, a broad man in his mid-forties with relaxed, loose shoulders, short brown hair flecked with grey, a few days' stubble, an olive canvas work jacket over a grey T-shirt, stands close to camera. A bright spark flashes on the steel grid above him and he flinches. Jude says softly, almost puzzled, in an easy, warm, slightly gravelly voice with a British accent: Oh. Then he sits down heavily backward into Eli, just behind him, who catches him under the arms: Eli, a thin man in his early thirties, pale, with an untrimmed dark beard, hollow cheeks and dark hair grown over his ears, a long grey coat over pale hospital pyjamas. Jude's right hand closes over his left shoulder, and a dark red stain slowly spreads between his fingers. Ambient noise: rattling steel and a straining motor.

**Kling 3.0 version** (4 s, audio on; `negative_prompt`: "blur, distort, and low quality, gun, weapon, muzzle flash, open wound, blood spray, subtitles"; ≈ $0.67 per take on fal [P16])
> A tense dramatic thriller scene inside a small freight cage. Near darkness. The only light is a torch lying on the grid and bands of warm light that sweep past from the shaft's floor gates. Cold blue-black shadows, wet brick, oily grey steel. Gritty realistic film look with fine grain. Medium close-up on @Jude, handheld camera held almost still with a slight sway. A bright spark flashes on the steel grid above him and he flinches. Jude (softly, almost puzzled): "Oh." At the 2nd second, he sits down heavily backward into @Eli, who catches him under the arms. Jude's right hand closes over his left shoulder; a dark red stain slowly spreads between his fingers. Rattling steel, a straining motor.

---

## 23. What I could not verify

- **Runway's own prompting guide** (help.runwayml.com) refused access (HTTP 403) [P42]. Runway advice here comes from its API reference [P39], its research page [P38], and general image-to-video principles [P2].
- **Runway Gen-4.5 audio and multi-shot**: resolved in the 27 Sep 2026 check. Runway's API has no audio setting for Gen-4.5 [P39], its changelog shows no Gen-4.5 audio release [P41], and C1 now reports the June 2026 entry it had misread was a separate sound model (Seed Audio 1.0). Treat Gen-4.5 as silent. Native multi-shot for Gen-4.5 remains unverified; Runway's Agent can assemble clips into a multi-shot scene (C1).
- **Prompt limits** for Kling 3.0, Seedance 2.5, Omni Flash and Wan 3.0 (MiniMax H3 is now verified at 7,000 characters [P32]); **seed support** for Omni, Wan 3.0 and H3 (Kling 3.0 on fal verified as having none [P16]; Kling's own API not checked).
- **Wan 3.0** negative prompt and "Generate single shot." (both verified for Wan 2.7 only).
- **MiniMax H3**: whether the `<d>` dialogue token and `overall_soundscape:` labels help through the public API.
- **Luma Ray3.2** text-to-video prompt guidance (only its video-to-video guidance was found).
- **Seedance 2.5** dialogue syntax, and ByteDance's own written prompt guide (Luma's guide quotes "ByteDance's guidance for 30-second video" [P21]; the BytePlus documentation pages need JavaScript and could not be read). Seedance advice here comes from ByteDance's launch examples [P18], fal [P19][P20] and Luma [P21].
- Whether the first sentences of a prompt carry more weight (practitioner claim).
- How each model handles **deliberately backwards text**: no benchmark found; the flip/composite advice is judgment.
- Whether "No subtitles" typed into an Omni prompt is effective.
- The speaking-rate budget (2.5 words per second) and beat density numbers are judgment, informed by [P11][P21][P45].
- **Newer models after 27 Sep 2026.** The web-search budget ran out during this check, so I could not run a fresh search for models released in the last few weeks. Makers' own pages (Kling's llms.txt, Luma's llm-info, Google's changelog, LTX's llm-info, Runway's changelog) were read directly and show no newer versions of their own models; other makers were not re-searched. Re-run the staleness rule before a paid batch.
- **Prices** for Runway Gen-4.5, MiniMax H3 and LTX-2.5's API are taken from companion file C1, not re-checked here.
- **LTX-2.5 text legibility**: LTX claims improvement [P35]; no test found.
- **HappyHorse 1.1, Grok Imagine 1.5, FLUX 3 Video**: no official prompt guides found; only the generic adapter applies.

---

## 24. Sources (all checked 2026-09-27; P1–P39, P41–P47, P49–P55 re-opened in the fact-check pass)

- [P1] Google Cloud, "Video generation prompt guide" (Veo and Omni Flash; last updated 2026-09-25): https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/video-gen-prompt-guide
- [P2] Google Cloud, "Best practices for generating videos" (last updated 2026-09-25): https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/best-practice
- [P3] Google Cloud, "Generate videos from text" (negativePrompt and seed parameters): https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/generate-videos-from-text
- [P4] Google Cloud, "Responsible AI for Veo" (safety filters, support codes; last updated 2026-09-25): https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/responsible-ai-and-usage-guidelines
- [P5] Gemini API, Veo 3.1 documentation: https://ai.google.dev/gemini-api/docs/veo
- [P6] Gemini API, Omni Flash documentation and prompt guide (last updated 2026-09-23): https://ai.google.dev/gemini-api/docs/omni
- [P7] Gemini API, release notes: https://ai.google.dev/gemini-api/docs/changelog
- [P8] Google Cloud blog, "Ultimate prompting guide for Veo 3.1" (16 Oct 2025): https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- [P9] Google blog, "Introducing Gemini Omni": https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/
- [P10] OpenAI API, deprecations (Sora 2 and Videos API removed 24 Sep 2026): https://developers.openai.com/api/docs/deprecations
- [P11] OpenAI Cookbook, "Sora 2 prompting guide" (updated March 2026): https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide
- [P12] Kling, "Kling VIDEO 3.0 Model User Guide" (6 Feb 2026): https://kling.ai/quickstart/klingai-video-3-model-user-guide
- [P13] Kling, "Kling VIDEO 3.0 Omni Model User Guide": https://kling.ai/quickstart/klingai-video-3-omni-model-user-guide
- [P14] Kling, start and end frames guide: https://kling.ai/quickstart/ai-video-start-end-frames
- [P15] Kling, community policy (effective 8 Sep 2026): https://kling.ai/docs/community-policy
- [P16] fal, Kling Video v3 Pro image-to-video API: https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video
- [P17] fal, "Seedance 2.0 vs Kling 3.0" (20 Apr 2026): https://fal.ai/learn/tools/seedance-2-0-vs-kling-3-0
- [P18] ByteDance Seed, "Introducing Seedance 2.5" (31 Jul 2026): https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5
- [P19] fal, Seedance 2.5 reference-to-video API: https://fal.ai/models/bytedance/seedance-2.5/reference-to-video
- [P20] fal, Seedance 2.0 page: https://fal.ai/seedance-2.0
- [P21] Luma Learning Center, "Seedance 2.5 Complete Guide" (30 Jul 2026): https://lumalabs.ai/learning-center/articles/seedance-2-5-complete-guide
- [P22] Luma Learning Center, "MiniMax H3 Complete Guide" (30 Jul 2026): https://lumalabs.ai/learning-center/articles/minimax-h3-complete-guide
- [P23] Luma Learning Center, "Ray 3.2 video-to-video": https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video
- [P24] Luma, "Introducing Ray3.2" (9 Jun 2026): https://lumalabs.ai/news/introducing-ray-3-2
- [P25] Luma API, video generation docs (camera by language): https://docs.lumalabs.ai/docs/video-generation
- [P26] Alibaba Cloud Model Studio, video prompt guide (Wan 3.0/2.7/2.6/2.5; last updated 24 Sep 2026): https://www.alibabacloud.com/help/en/model-studio/text-to-video-prompt
- [P27] Alibaba Cloud Model Studio, Wan2.7 text-to-video API reference: https://www.alibabacloud.com/help/en/model-studio/text-to-video-api-reference
- [P28] Alibaba Cloud blog, "Wan3.0" (13 Aug 2026): https://www.alibabacloud.com/blog/wan3-0-30-second-ai-video-generation-from-any-input_603452
- [P29] fal, Wan 3: https://fal.ai/wan-3
- [P30] MiniMax, H3 announcement (31 Jul 2026): https://www.minimax.io/blog/minimax-h3
- [P31] MiniMax H3 model card: https://huggingface.co/MiniMaxAI/MiniMax-H3
- [P32] MiniMax API, video generation guide: https://platform.minimax.io/docs/guides/video-generation
- [P33] MiniMax API, text-to-video reference (camera commands, prompt_optimizer): https://platform.minimax.io/docs/api-reference/video-generation-t2v
- [P34] LTX blog, prompting guide for LTX-2 (11 Dec 2025): https://ltx.io/blog/prompting-guide-for-ltx-2
- [P35] LTX, information for AI assistants (LTX-2.5 facts): https://ltx.io/llm-info
- [P36] Lightricks, LTX-2 GitHub repository: https://github.com/Lightricks/LTX-2
- [P37] Lightricks, LTX-2 model card (negative prompt example): https://huggingface.co/Lightricks/LTX-2
- [P38] Runway, "Introducing Runway Gen-4.5" (limitations): https://runway.com/research/introducing-runway-gen-4.5
- [P39] Runway API reference (gen4.5 parameters): https://docs.dev.runwayml.com/api/
- [P40] Runway API changelog: https://docs.dev.runwayml.com/api-details/api_changelog/
- [P41] Runway changelog: https://runway.com/changelog
- [P42] Runway Help, "Gen-4 Video Prompting Guide" (could not open: HTTP 403): https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide
- [P43] Wang et al., "FilmBench: A Film-Grade Benchmark for Cinematic Video Generation" (arXiv 2607.24241, Jul 2026): https://arxiv.org/abs/2607.24241
- [P44] Hou and Rupprecht, "Probing into Camera Control of Video Models" (arXiv 2605.14815, May 2026): https://arxiv.org/abs/2605.14815
- [P45] Zhou et al., "AVGen-Bench" (arXiv 2604.08540, Apr 2026): https://arxiv.org/abs/2604.08540
- [P46] Zhang et al., "Physion-Eval" (arXiv 2603.19607, Mar 2026): https://arxiv.org/abs/2603.19607
- [P47] HackerNoon, "AI video generators flagged my anime duel as graphic violence" (19 Aug 2026): https://hackernoon.com/ai-video-generators-flagged-my-anime-duel-as-graphic-violence-it-was-a-cartoon
- [P48] Artificial Analysis, text-to-video leaderboard (context for model standing): https://artificialanalysis.ai/video/leaderboard/text-to-video
- [P49] Luma, information for AI assistants (Ray3.2 current and without native audio; Ray2 and Dream Machine deprecated; last updated 13 Jul 2026): https://lumalabs.ai/llm-info
- [P50] Gemini API, pricing (Veo 3.1 Standard/Fast/Lite per-second prices; Omni Flash ≈ $0.10/s at 720p): https://ai.google.dev/gemini-api/docs/pricing
- [P51] Hugging Face, Lightricks model list (LTX-2.5 add-ons to 15 Sep 2026; camera-control LoRAs only for LTX-2 19B, 5 Jan 2026; LTX-2.5 weights 23 Jul 2026): https://huggingface.co/Lightricks
- [P52] xAI, video generation guide (Grok Imagine Video 1.5: up to 15 s, image- and reference-to-video, edit, extend): https://docs.x.ai/docs/guides/video-generations
- [P53] fal, HappyHorse 1.0 text-to-video API (3–15 s, 720p/1080p, audio, seed, $0.14/$0.28 per s): https://fal.ai/models/alibaba/happy-horse/text-to-video
- [P54] Runway Dev, models list (gen4.5 guide link points to the research page; wan3, seedance2_5, grok_imagine_1_5, gemini_omni_flash, aleph2 hosted): https://docs.dev.runwayml.com/guides/models.md
- [P55] Kling, llms.txt (Kling 3.0 series, 5 Feb 2026, is the latest major version): https://kling.ai/llms.txt

---

## 25. MiniMax H3 in ComfyUI, reference mode (added 10 October 2026)

*Added for Project notes 42 and 43. Everything in Sections 0 to 24 was checked on 27 September 2026; the facts below were checked on 10 October 2026.* The marks are this file's own: **[V]** read in the maker's own document on that date, **[U]** stated but not verified, **[J]** judgement (testers' notes or the hand-made clip file of Project notes 42).

**Why it is its own route [V].** On MiniMax's own service a rewriting step, H3-Context-IR, turns a short prompt into a long structured one; it is hosted and "not included in this open-source release" [P57]. In ComfyUI H3 reads the prompt exactly as written, so the prompt must already be in that long form. Stage keeps two entries: `minimax-h3` (the hosted service) and `minimax-h3-comfyui-r2v` (ComfyUI, Reference to Video), and never shares one prompt between them.

**The format, from MiniMax's reference-mode guide [V] [P56]:**
1. Six sections in this order: `subject_definitions`, `summary`, `retention_analysis`, `detailed_description`, `overall_soundscape`, `non_diegetic_music`.
2. Labels: `<Subject N>` is visible content to keep or change; `<Picture N>` is a reference image used as a target frame or shot-planning anchor.
3. `retention_analysis` values: `fully_preserved`, `partially_preserved`, `attribute_transfer`, `weak_reference`; a speaker ID `(Sx)` never appears there.
4. Speakers get stable IDs `(S1)`, `(S2)`; a subject speaking is written `<Subject N> (Sx)`; dialogue as `<d>[Language] ...</d>`.
5. `detailed_description` is "normally 350-500 English words" for generation.
6. `[Shot 1]` marks the opening shot and has no time; later shots are written `[Shot N] At MM:SS.mmm, ...`.
7. The complete example writes `non_diegetic_music: N/A` when there is no music.

**The model [V] [P57]:** output of 4 to 15 seconds at 24 frames a second; the short side is 768 by default; reference mode takes up to 9 pictures.

**The ComfyUI template [V] [P58][P59]:**
1. The template is "MiniMax H3 Reference to Video (R2V)", with up to 9 reference pictures tagged `<Picture 1>` onward.
2. The Lightning LoRA checkbox runs a 4-step turbo mode "with slightly lower audio and motion quality"; 20 steps by default, and more steps are offered.
3. `ref_image_size`: `match` scales references down for speed; `max` keeps up to a 2048-pixel short edge.
4. Duration snaps up to the 17-frame-block grid, 17 × k + 5 frames at 24 frames a second (said for the T2V and I2V templates); the length input defaults to 124 frames. Native canvas 1344 × 768 at 16:9.
5. "There is no negative branch and a negative prompt has no effect"; "an instruction that names an unwanted element adds that wording to the description the model reads"; "Say what should be in the shot instead."

**Stated, not verified [U]:** the box names Boolean (Enable Lightning LoRA), Int (Full), Resolution Selector (Size), Float (Duration), RandomNoise and Input Text (Prompt), and the inputs `ref_image_0`, `ref_image_1` ... come from the clip file's reading of the template, not from ComfyUI's pages; the frame range 124 to 362 is Project notes 42's (362 is 15 seconds snapped up on the grid; 124 is the template's default; shorter lengths on the grid are untested); 1536 × 640 for a 2.39:1 film and 1152 × 480 for tests are the clip file's choices.

**Testers' notes [J] [P60]** (found on 10 October 2026; none yet run on the user's own setup):
1. A strong "do not move" line leaks across the whole shot; without continuous small motion a face looks like a photo with moving lips. Time with nothing happening is squeezed out.
2. Listing "no push in, no zoom ..." made cuts drift and the camera move; one line works instead: "static, on a tripod, with no camera movement whatsoever".
3. H3 often breaks into noise 1.2 to 1.7 seconds before the end: leave a tail of 1.3 to 1.5 seconds and throw it away.
4. H3 cannot do contact-driven cause and effect: cut from the action to the result, with the sound on the cut.
5. When a two-shot cuts to a closer single on the same line, the cut can be smoothed away; cuts hold when subject and framing differ clearly.
6. Speech rhythm follows the seed, not the prompt: change the seed first when speech is wrong. A cut written at 2.0 seconds landed at 3.21, and lines started 1.4 to 1.9 seconds late.
7. Shot and reverse shot need a lead-in, a shot showing both; text cannot replace it.
8. In a shot where a hand moves a thing, the hand is the subject, kept on the thing. A comparison ("like ...") can make the model draw the thing compared; sentences that talk about speaking get read aloud.

**How Stage uses this.** `stage.py compile --route h3-comfyui` groups each scene's shots into clips of one to three shots, writes each prompt in the six sections from the records, and runs the ROUTE checks. Format facts marked [V] are errors; every [J] rule stays a suggestion until the take log marks it confirmed on the user's own setup (Project notes 42, W11).

**Sources for Section 25 (checked 2026-10-10):**
- [P56] MiniMax, H3 video prompt writing guide, reference mode: https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md
- [P57] MiniMax, H3 model page: https://huggingface.co/MiniMaxAI/MiniMax-H3
- [P58] ComfyUI, MiniMax H3 templates and settings: https://docs.comfy.org/tutorials/video/minimax/minimax-h3-native
- [P59] ComfyUI, MiniMax H3 prompt guide: https://docs.comfy.org/tutorials/video/minimax/minimax-h3-prompt-guide
- [P60] h3-storyboard testing notes (skills/h3-storyboard/SKILL.md): https://github.com/phileiny/h3-storyboard-skill
