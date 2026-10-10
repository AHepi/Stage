# C2. AI Images for Storyboards, Keyframes, and Consistency

> **What this file is for**
> 1. It tells the pipeline which image tools to use (as of 2026-09-27) for storyboard frames, for photoreal keyframes that feed video models, and for keeping characters, costumes, props and places the same across hundreds of shots.
> 2. It gives a current landscape table, a "which tool for which aim" table, "If ... then use ... because ..." rules, step-by-step recipes, and a failure-and-fix table.
> 3. It explains how to build an asset bible (character, location and prop sheets) and reuse it as reference images, with the full process for the cast and key places of *The Catch*.
> 4. It solves the hard text problem in *The Catch*: a mirror-reversed world where some writing must read backwards and some must read correctly.
> 5. Read it after the scene breakdown and the light-and-color plan (file B2) exist, and before any image or video is generated.

---

## 0. How to use this file

**Order of work for an LLM running the pipeline:**

1. **Pick a path** (Section 3.7 and Recipe R1): chat-only, node canvas, or automated. The user's budget and patience decide this, not the story. Show the user the "cost and difficulty at a glance" table at the end of Section 3.7 first.
1a. **Write one image-request block per shot** (Section 6.6, the YAML example) into the breakdown. This is what makes storyboards optional and lets any image or video tool be plugged in later.
2. **Build the asset bible** (Section 6, Recipe R2) before a single storyboard frame. Consistency is set up front; it cannot be added later.
3. **Tag mirror state** for every asset in every scene (Section 7) if the story has any mirror, reflection or handedness logic.
4. **Storyboard pass** (Recipe R3): one cheap greyscale storyboard frame per shot.
5. **Keyframe pass** (Recipe R4): only for shots that will become video.
6. **Drift check** (Recipe R7) after every batch.

**For the non-technical user:** you do not need to understand any of this in advance. Say to the LLM: "Run Recipe R2 from file C2 on my script, using the chat-only path." The LLM should then tell you exactly what to paste where, and what to check by eye.

### 0.1 Words this file uses (one word per concept)

| Term | Plain definition |
|---|---|
| **Storyboard frame** | A drawing-like image that shows people what one shot will look like: framing, who is where, where the light falls. It may carry arrows and notes. |
| **Keyframe** | A finished, clean still image that a video model uses as the exact first (or last) picture of a clip. |
| **Image-to-video** | A video model mode that starts from a keyframe you supply instead of from words alone. |
| **Asset** | Any repeating thing the audience must recognise: a character, a costume, a prop, a place. |
| **Asset sheet** | One image (or small set) that defines an asset from several views so it can be reused. A **character sheet**, **location sheet** or **prop sheet** is an asset sheet for that kind of asset. |
| **Turnaround** | The same character shown front, three-quarter, side and back, same pose, same light. |
| **State** | One version of an asset at one point in the story (Jude before and after he is shot; the cage before and after it is wrecked). |
| **Reference image** | An image you attach to a request so the model copies something from it (a face, a room, a style). |
| **Reference stack** | The full set of reference images attached to one request. |
| **Style frame** | One approved image that fixes the look (light, color, texture) of a sequence; attached to every request in that sequence. |
| **Drift** | A repeated asset slowly changing across generations (a face ageing, a blue shirt turning grey). |
| **Edit model** | An image model that changes an existing image from written instructions while keeping the rest. |
| **Inpainting** | Regenerating only a marked region of an image (for example, one hand). |
| **LoRA** | A small add-on file trained on your own pictures that teaches an open image model one face, object or style. |
| **Open-weight model** | A model whose files are published, so it can run on your own computer or a rented one. |
| **API** | A way for a program (or an LLM writing a script) to use a tool without clicking through its website. |
| **MCP server** | A connector that lets an LLM app such as Claude call a tool directly from the conversation. |
| **Node canvas** | A website where you wire boxes together ("prompt" into "image model" into "video model") to make a repeatable chain. |
| **Mirror state** | Whether an asset appears in a shot as itself (**NORMAL**) or as its mirror image (**MIRRORED**), relative to the camera. |
| **Flip** | Mirroring an image left to right. |
| **Composite** | Layering one image on top of another (a character placed on a background). |
| **Plate** | A background image of a location with no characters in it, made to have characters composited onto it. |
| **Insert graphic** | Any text, screen, label or display made as a precise graphic outside the image model and placed into the frame. |

### 0.2 Evidence labels

Every factual claim about a tool carries a label and a source number from Section 12 (all checked 2026-09-27):

- **[V]** verified at the maker's own page or documentation.
- **[V-sec]** verified only at a reputable third-party page (press, reseller, review); likely true, re-check before spending money.
- **[U]** could not verify; treat as rumor.
- **[J]** my own judgment from the evidence and from how these models behave; not a sourced fact.

---

## 1. Core principles

1. **Consistency is a reference problem, not a prompt problem.** Words drift; pictures anchor. Every repeated asset needs an approved picture before it appears in any shot. [J]
2. **Storyboard frames and keyframes are different products.** Make hundreds of cheap storyboard frames; make keyframes only for shots going to video. (Section 2.2.) [J]
3. **Attach only what is in the shot.** A reference stack of three good images beats ten mixed ones; extra references leak their backgrounds, light and clothes into the new image. [J]
4. **Never trust an image model with exact text or handedness.** Rings on the right hand, a smile on the left side, letters that must read backwards: plan them as separate checks or insert graphics. [J]
5. **Make the world once, reuse it forever.** Generate each location once in several angles and reuse those images; never re-describe a room from scratch per shot. [J]
6. **Record every choice in writing.** The asset bible index (Section 6.1) is what lets a different LLM, next month, reproduce the same film. [J]
7. **Tools turn over every few months.** The landscape below is dated 2026-09-27. The *method* (sheets, stacks, states, drift checks) survives model changes; the model names do not. [J]

---

## 2. What you are making

### 2.1 Three storyboard styles

| Style | What it looks like | Use it for | Cost and speed | How to ask for it |
|---|---|---|---|---|
| **Rough pencil** (thumbnail) | Loose line sketch, little shading, stick-like figures allowed | Exploring shot order and coverage fast; nobody judges faces | Cheapest; any model, lowest resolution | "rough pencil storyboard sketch, loose lines, white paper, no color, no text" |
| **Greyscale value sketch** | Soft charcoal or marker drawing in 3 to 5 grey tones; shows where light and dark masses fall | **The default for this pipeline.** It shows framing *and* lighting, hides small identity drift, and is fast | Cheap; 1K resolution is enough | "greyscale storyboard frame, charcoal and grey marker, 4 tonal values, strong light and shadow shapes, no color, no text, no arrows" |
| **Color keyframe** | Near-final painted or photoreal image in the film's palette | Hero moments, pitch decks, and every image that will feed image-to-video | Most expensive; 2K or more | Full keyframe spec (Recipe R4) |

The film trade escalates fidelity as decisions lock: thumbnails first, then cleaner storyboard frames, then animatics (storyboard frames timed to sound) [V-sec, 77]. Do the same: never make a color keyframe for a shot whose framing is not yet approved in greyscale. [J]

### 2.2 Why a storyboard frame and a keyframe are different things

| Question | Storyboard frame | Keyframe |
|---|---|---|
| Who reads it | People (you, a collaborator, an LLM checking the plan) | A video model |
| Job | Communicate intent | Be the literal first (or last) picture of the clip |
| Fidelity | Rough is fine | Final look, final light, final costume state |
| Arrows, labels, shot numbers | Yes, added in a storyboard tool | Never. Any mark in the image becomes part of the video |
| Time | May compress an action (a figure drawn mid-leap to show the whole move) | One instant only |
| Which instant | The most telling moment of the shot | The *start* of the shot, posed so the planned motion can begin (a push-in starts wider; an entrance leaves space) |
| Aspect ratio | Roughly right | Exactly the delivery aspect ratio and at least 1920 pixels wide [J] |
| Identity | Readable silhouette and costume | Exact face, hair, costume state, wounds, props, mirror state |
| Cost of an error | A few cents | Wasted video credits, often dollars per clip [J] |

Two consequences. First, a storyboard frame is not "upgraded" into a keyframe by asking for more detail; the keyframe is re-composed for its instant (Recipe R4). Second, if a clip uses a start and an end keyframe, make the end keyframe by *editing* the start keyframe, not by generating it fresh: Kling's own guide warns that start and end frames that differ too much make the model cut to a new shot instead of moving smoothly [V, 73].

### 2.3 Aspect ratio control

"Aspect ratio" means the width of the frame divided by its height (16:9 is television and most streaming; 2.39:1 is wide cinema).

| Tool | Aspect ratio control (as of 2026-09-27) |
|---|---|
| Gemini image models ("Nano Banana" family) | Fixed list: 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9 [V, 2]; Nano Banana 2 adds 1:4, 4:1, 1:8, 8:1 [V, 2, 6]. Sizes 1K, 2K, 4K; 0.5K on Nano Banana 2 only; Nano Banana 2 Lite 1K only [V, 2]. **Actual pixel sizes matter:** 16:9 is 1376x768 at 1K, 2752x1536 at 2K, 5504x3072 at 4K; 21:9 is 1584x672 at 1K and 3168x1344 at 2K [V, 2] |
| OpenAI GPT Image 2.5 | Any width and height in multiples of 16, ratio between 1:3 and 3:1, longest edge up to 3840 pixels, total 655,360 to 8,294,400 pixels; above 2560x1440 is "experimental" [V, 10] |
| FLUX.2 | Custom sizes; edits up to 4 megapixels [V, 21] |
| Grok Imagine Image 2.0 (xAI) | Presets including 16:9, 21:9, 20:9, 5:2, 2:1; `1k` or `2k` resolution [V, 89] |
| Midjourney V8.2 | `--ar` parameter; up to 14:1, HD mode up to 4:1 [V-sec, 18] |
| Seedream 5.0 Pro (on fal) | Up to 2048x2048 pixels; priced in two size tiers [V, 28] |
| Qwen-Image-2.1 | 1:1, 4:3, 3:4, 3:2, 2:3, 16:9, 9:16 at up to 2K (16:9 = 2752x1536) [V, 32] |

**Resolution rule for keyframes.** A 16:9 image at "1K" is only 1376 pixels wide, below the 1920 needed for a 1080p video start frame. **If** an image will feed image-to-video, **then** generate it at 2K or larger (never on Nano Banana 2 Lite, which is 1K only). Storyboard frames can stay at 1K. [J, sizes V, 2]

**For 2.39:1 delivery** no model offers it as a preset. Either use a custom-size model (GPT Image 2.5 at 2560x1072, which is 2.39:1 and within the limits above) or generate at 21:9 and crop. Gemini's 21:9 is really 2.357:1 (3168x1344 at 2K), so cropping to 2.39:1 removes only about 18 pixel rows at 2K (under 1.5 percent of the height, split top and bottom); keep heads and key props out of the top and bottom 1 percent. Frame the storyboard for 2.39:1 from the start by drawing thin bars in the storyboard tool. [J]

---

## 3. The current landscape (checked 2026-09-27)

### 3.1 Image models

"Refs" means the maximum number of reference images per request. "LLM-drivable" says whether an LLM can operate it for you.

| Model (maker) | Status and date | Refs | Text in image | Price (USD) | LLM-drivable | Best at, for this pipeline |
|---|---|---|---|---|---|---|
| **Nano Banana Pro** = Gemini 3 Pro Image, `gemini-3-pro-image` (Google) | Preview Nov 2025; generally available May 28, 2026 [V, 3] | 5 character + 6 object + 3 style (14 total) [V, 2]; the **only** Gemini model with a documented style-reference slot | Strong; Google itself warns "Rendering small text, fine details, and producing accurate spellings may not work perfectly" and "character consistency across edits may vary" [V, 5] | $0.134 per 1K/2K image, $0.24 per 4K; batch or Flex $0.067 (1K/2K), $0.12 (4K); no free API tier [V, 1] | Yes: Gemini API; fal ($0.15 per image, 4K double) [V, 88]; Runway API (20 credits = $0.20 per 1K/2K) [V, 91]; also the Gemini app by hand, where Nano Banana 2 replaced Pro as the default in Feb 2026 [V, 4] (how to pick Pro in the app depends on plan [U]) | Character sheets, multi-character frames, sheet-to-shot consistency |
| **Nano Banana 2** = Gemini 3.1 Flash Image, `gemini-3.1-flash-image` (Google) | Announced Feb 26, 2026 [V, 4]; generally available May 28, 2026 [V, 3] | 4 character + 10 object (14 total); **no style-reference slot** in the API table [V, 2]. (Google's launch post says "up to five characters and 14 objects" [V, 4]; plan on the API doc's 4) | Good | $0.045 (0.5K), $0.067 (1K), $0.101 (2K), $0.151 (4K); batch 50% off [V, 1] | Yes, as above; default image model in Google Flow, where it cost zero credits at launch [V, 4] | Bulk storyboard frames with consistent characters |
| **Nano Banana 2 Lite** = `gemini-3.1-flash-lite-image` (Google) | Generally available Jun 30, 2026 [V, 3] | Up to 14 object references; **no character-reference or style slot** [V, 2] | Fair | $0.0336 per 1K image; batch $0.0168 [V, 1] | Yes | Cheapest rough and greyscale storyboard frames without named characters (empty sets, inserts, distant figures); 1K only, so never a keyframe |
| Nano Banana (original) = `gemini-2.5-flash-image` | **Superseded.** Deprecated; shuts down Oct 2, 2026 [V, 1] | | | $0.039 | | Do not build on it |
| **GPT Image 2.5 Sunburst** and **Flare** (OpenAI), `gpt-image-2.5-sunburst`, `gpt-image-2.5-flare` | Released Sep 8, 2026 [V-sec, 11, 12, 13]; both listed in OpenAI's API guide and pricing page [V, 9, 10] | No hard limit documented; examples use 4 [V, 10] | Best-ranked overall; OpenAI still warns "the model can still struggle with precise text placement and clarity" and "may occasionally struggle to maintain visual consistency for recurring characters" [V, 10] | Token-priced: text in $5, image in $8, image out $30 per million tokens, same as GPT Image 2 [V, 9]. Five quality levels: low, medium, high, xhigh, max [V-sec, 11]. Per-image, as resold by Runway's API (1 credit = $0.01): low $0.01, medium $0.05, high $0.16, xhigh $0.28, max $0.63 at 1K/2K; at 4K $0.02, $0.11, $0.19, $0.34, $0.76; plus $0.01 per reference image per output [V, 91] | Yes: OpenAI API; Runway API [V, 91]. **ChatGPT by hand (all tiers) uses Flare and switches to Sunburst on its own for complex prompts; you cannot pick Sunburst in ChatGPT** [V-sec, 11, 12] | Photoreal keyframes; precise edits that keep the rest intact. Ranked #1 on Arena for both text-to-image and image editing (Sep 24 and 21, 2026) [V, 43, 44]. Sunburst = more precise, slower; Flare = about 50% faster [V-sec, 11, 12] |
| GPT Image 2, 1.5, 1-mini, 1 (OpenAI) | Superseded by 2.5 but still sold; GPT Image 2 is the only one of the 2.x line with a documented batch price (image output $15 per million tokens, half price) [V, 9]; GPT Image 1 reported deprecating Oct 23, 2026; DALL-E 2 and 3 left the API May 12, 2026 [V-sec, 14] | | | GPT Image 2 about $0.005 to $0.21 per image by quality and size [V-sec, 14]; 1-mini $0.005 to $0.052 [V-sec, 14] | Yes | GPT Image 2 in batch for cheap bulk frames if already on OpenAI; otherwise only if already in a working script |
| **ChatGPT "Sketch"** (OpenAI) | Sep 8, 2026: type `@Sketch` to draw a rough layout, then generate from it [V-sec, 12] | | | ChatGPT plan | By hand | Turning a stick-figure layout into a frame without any other software |
| **Midjourney V8.2** with the **Edit Model** | V8.2 default since Jul 24, 2026 [V-sec, 18, 19]; Edit Model opened Aug 27, 2026 as an alpha test [V, 16]; Sep 24, 2026 update lets edits change only selected pixels [V, 17] | Up to 4 image references in the Edit Model, "replacing omni-reference" [V, 16]; `--oref` does not work on V8.x, and `--cref` was already limited to V6 and Niji 6 [V-sec, 18] | Short text fine [V-sec, 18] | Plans $10, $30, $60, $120 per month [V-sec, 18] | **No.** No public API; the terms forbid automated access [V-sec, 20] | Look development and style exploration; `--sref` (style reference, weight `--sw` 0 to 1000) still works [V-sec, 18] |
| **FLUX.2** pro / flex / max / dev / klein (Black Forest Labs) | Released Nov 25, 2025; klein Jan 2026 [V, 21, 26] | Up to 10 [V, 21] | Strong on typography [V, 21] | pro from $0.03 per megapixel (create), $0.045 (edit); flex from $0.05; max from $0.07; klein 4B from $0.014, klein 9B from $0.015; dev is not hosted by BFL (local, or third parties such as fal) [V, 22]. **Licenses of the open weights:** klein 4B is Apache 2.0 (commercial use allowed); klein 9B and dev are under the FLUX Non-Commercial License: running them yourself for paid or production work needs a separate BFL license, although the license lets you use the *outputs* commercially [V, 92] | Yes: API, fal, Replicate, ComfyUI | Multi-reference keyframes; the open klein and dev versions accept LoRAs |
| FLUX.1 Kontext pro / max | Previous generation [V, 22] | 1 | | $0.04 to $0.08 per image [V, 22] | Yes | Superseded by FLUX.2 for new work |
| FLUX 3 (Black Forest Labs) | Announced Jul 23, 2026 as one model for images, video and audio; video tier live; **image tier ("FLUX 3 Image") promised as "early access ... in the following weeks"** and not publicly available as of early September [V, 23; V-sec, 24] | Announced: "visual references help ensure that the characters remain consistent across all scenes" [V, 23] | | Video $0.17 to $0.80 per second by resolution; draft $0.06 [V, 22] | | Watch this space; do not plan on it |
| **Seedream 5.0 Pro** (ByteDance) | July 2026 (fal lists Jul 14) [V, 29] | Up to 10 [V, 28] | 14 languages; long text blocks still weak [V, 29] | $0.0675 per image up to 1536x1536, $0.135 up to 2048x2048, +$0.0045 per extra reference; fal labels this "tentative pricing" [V, 28]. Runway API: $0.05 (1K), $0.09 (2K) [V, 91] | Yes: BytePlus API, fal, Runway API | Region edits by drawing colored boxes on the image, each box tied to one instruction; layer separation; sketch completion [V, 28, 29] |
| Seedream 4.5 / 5.0 Lite | 4.5 Dec 3, 2025 [V, 27]; 5.0 Lite Feb 2026 [V-sec, 84; product page 30] | 10 [V, 27] | Improved small text [V, 27] | 4.5 about $0.035 [V-sec, 80] | Yes | Cheap multi-image batches; 4.5's "sequential" mode returns up to 15 related images in one call [V-sec, 80] |
| **Qwen-Image-2.1** (Alibaba) | Open weights, Sep 21, 2026 (repository created Sep 14) [V, 31, 32]; 7B-parameter image generator [V, 31, 32] | Up to 10 [V, 32] | Good (English examples shown) [V, 32] | Free to run yourself, **but research and evaluation use only**: the Qwen Research License says "You shall not use the Materials for any commercial purpose without obtaining a separate commercial license" [V, 32] | Via ComfyUI or scripts | Transparent-background (RGBA) props and local editing [V, 32]; personal and test projects |
| Qwen-Image-Edit-2511 (Alibaba) | Last of the 20B edit line, Dec 2025 [V-sec, 81; V, 93] | Multi-image | | Free to run yourself; **Apache 2.0, commercial use allowed** [V, 93] | ComfyUI | The open editor to use on a *commercial* project, since 2.1 is research-only [J] |
| Qwen-Image-3.0 / 3.0-Pro (Alibaba) | Shown Jul 21, 2026 in Qwen Chat with no weights, benchmarks or license [V-sec, 33]; API from Aug 4, 2026 [V-sec, 33] | | Text down to 10 pixels, 12 languages [V-sec, 33] | Pro about $0.04 (1K), $0.075 (2K) [V-sec, 33] | Yes: Alibaba Cloud API | Dense signage and labels |
| **Ideogram 4.0** | Released Jun 3, 2026; 9.3B open weights; weights under the "Ideogram 4 Non-Commercial" license, code Apache 2.0 [V, 34, 94; V-sec, 87]; the smaller nf4 version fits on one 24 GB graphics card [V, 34] | Character reference documented for 3.0 [V, 35]; the site lists a "Character consistency" workflow but gives no 4.0 details [V, 34] | Strongest open-weight text (0.97 English OCR); layout by bounding boxes in JSON; palette of up to 16 hex colors per image [V, 34] | API about $0.03 / $0.06 / $0.10 (Turbo / Default / Quality) [V-sec, 36] | Yes: API; its site also lists an MCP server [V, 34] | Posters, signs, labels, graphic inserts |
| **Recraft V4.1** | May 14, 2026; main, Vector (logos, typography) and Utility ("flat lighting, front-facing composition, and simple scenes", useful for clean sheets) variants; the launch post lists "character design and reference sheets" among its uses [V, 37] | Style references ("V4 Styles", Aug 2026) [V-sec, 86] | Strong typography and vectors [V, 37] | Plans; not checked | Yes: API [V, 37] | Clean vector insert graphics, signage, UI; storyboard "look" lock |
| **Reve 2.1** | Jul 9, 2026 [V, 38] | References supported [V, 38] | Strong multilingual | App plans | **API launched Jul 14, 2026** [V, 38] **and was discontinued Aug 14, 2026** [V-sec, 40]; OpenAI invested and some Reve researchers joined OpenAI, while Reve says it "will continue to operate independently" (Jul 27, 2026) [V, 39] | Hand-made frames in its layout editor; not for automation |
| **Adobe Firefly Image Model 5** | Generally available (Mar 19, 2026 post) [V, 41] | Custom Models (train on your images) in public beta [V, 41] | | Adobe plans | Limited [U] | Teams already paying for Adobe; Firefly also offers "more than 30" partner models, including Nano Banana 2, Veo 3.1, Runway Gen-4.5 and Kling 2.5 Turbo [V, 41] |
| MAI-Image-2.6 (Microsoft) | Aug 10, 2026; public preview on Microsoft Foundry (post updated Sep 4, 2026) [V-sec, 42] | Multi-reference work announced, details "coming later" [V-sec, 42] | Improved (+91 Elo on text over 2.5) [V-sec, 42] | Not published | Yes: Azure API | An alternative if on Azure; ranked #4 text-to-image [V, 43] |
| **Grok Imagine Image 2.0** (xAI), `grok-imagine-image-2.0` | Current; replaces `grok-imagine-image-quality`, which retires Nov 2, 2026 [V, 90] | Up to 5 source images per edit [V, 90] | Not documented | $0.04 per image on xAI's API [V, 95]; quality `low` or `medium` [V, 89] | Yes: xAI API; Runway API (4 to 8 credits) [V, 91] | Cheap second opinion for edits: ranked #4 in image editing and #6 in text-to-image [V, 43, 44]; 21:9 preset |
| **Runway Gen-4 Image** (`gen4_image`, `gen4_image_turbo`) | Current on Runway's API [V, 96] | Up to 3, each given a short **tag** you then write in the prompt (for example `@iona` in `@shaft`) [V, 96] | | $0.05 per 720p, $0.08 per 1080p; turbo $0.02 [V, 91] | Yes: Runway API; Runway app by hand | Tagged references read naturally in a breakdown ("@iona at the gate of @cage"); accepts a fixed seed for repeatable re-runs [V, 96]; the same API key also runs Runway's video models |
| Meta muse-image | On Arena (#7 text-to-image, #6 editing) [V, 43, 44] | Not documented | | Runway API: 1 credit = $0.01 per image [V, 91] | Via Runway API | Very cheap bulk frames if its look suits; not tested for references [J] |
| **Stable Diffusion XL (SDXL)** with ControlNet, IP-Adapter, InstantID, PuLID | Mature, 2023 to 2024 research [V, 46 to 49] | Via adapters | Weak | Free to run | ComfyUI (Section 3.3) | Only when you need pose-exact control on a cheap local GPU; newer open models beat it on quality [J] |

**What the leaderboards say (Arena, human votes).** Text-to-image, Sep 24, 2026: GPT Image 2.5 Sunburst, GPT Image 2.5 Flare, GPT Image 2, MAI-Image-2.6, Reve 2.1, then Grok Imagine Image 2.0, Meta's muse-image, Reve 2.0, Nano Banana 2, Seedream 5.0 Pro, Qwen-Image-3.0-Pro; Nano Banana Pro is 14th [V, 43]. Image editing, Sep 21, 2026: the three OpenAI models lead, then Grok Imagine Image 2.0, MAI-Image-2.6, muse-image, MAI-Image-2.5, Seedream 5.0 Pro and Nano Banana Pro (9th) [V, 44]. Leaderboards measure single-image appeal, not consistency across 300 shots; for character sheets and multi-character consistency, Google's documented reference limits (5 characters on Pro) are the more relevant number [J].

**Rumors, not facts.** "Nano Banana 2.5" exists only in leaks as of Sep 22, 2026 [U, 83]. Gemini 4 is in post-training with no date [V-sec, 82]. FLUX 3 Image has no public endpoint [V-sec, 24].

### 3.2 Superseded or ending: do not build on these

- `gemini-2.5-flash-image` (original Nano Banana): shuts down Oct 2, 2026 [V, 1].
- Gemini 3 preview model names (`...-preview`): shut down Jun 25, 2026 [V, 3].
- Google Imagen 4 (`imagen-4.0-...`): shut down Aug 17, 2026 [V, 3]. Old tutorials that say "use Imagen for photoreal" are out of date.
- GPT Image 1: reported deprecation Oct 23, 2026; DALL-E 2 and 3: removed from the API May 12, 2026 [V-sec, 14].
- xAI `grok-imagine-image-quality`: retires Nov 2, 2026, after which calls are silently redirected to Grok Imagine Image 2.0 at low quality [V, 90].
- Midjourney Omni Reference (`--oref`) and Character Reference (`--cref`): V7-only; replaced by the Edit Model on V8.x [V, 16].
- Reve API: discontinued Aug 14, 2026 [V-sec, 40].
- OpenAI Sora: app closed Apr 26, 2026; Sora 2 API removed Sep 24, 2026 [V-sec, 15]. Any tool advertising "export to Sora 2" (for example Higgsfield Popcorn's page [V, 69]) is out of date on that point.
- Storyboarder (Wonder Unit): still free and usable, but the last release is v3.0.0 from Feb 17, 2024 [V, 61]. Some 2026 review sites claim a 2026 release; GitHub does not show one.

### 3.3 The open-weight toolbox, explained plainly

These matter only if you (or a rented cloud machine) run models yourself, usually inside **ComfyUI**, a free node-based program for open models.

- **ControlNet**: makes the model follow a structure image: a pose skeleton, an edge drawing or a depth map. Use it to force an exact composition from a Blender screenshot [V, 46].
- **IP-Adapter**: lets an image act as part of the prompt ("look like this") [V, 47].
- **InstantID** and **PuLID**: identity adapters that copy one face from a single photo without training [V, 48, 49]. Practitioners in 2026 still combine a face adapter, a character LoRA and ControlNet on FLUX-family models [V-sec, 79].
- **LoRA** (Section 3.4).

**Can an LLM run ComfyUI for you?** Yes, increasingly. Comfy Org launched an official MCP server on Jun 30, 2026 (still labelled **public beta**): a hosted connection at `https://cloud.comfy.org/mcp` that runs on their cloud GPUs (no local graphics card needed; new accounts get 5 free runs) and a fully open-source local connection [V, 54, 55]. Comfy's own guide recommends the cloud connection for new users and for Claude Desktop or claude.ai; in Claude Code it installs as a plugin with `/plugin marketplace add Comfy-Org/comfy-skills` then `/plugin install comfy-cloud@comfy-skills` [V, 55]. The popular community server `artokun/comfyui-mcp` is being archived on Oct 9, 2026 and points users to the official one [V, 57]. Comfy Cloud: Standard $20 a month ($16 billed yearly); importing your own LoRAs from Civitai or Hugging Face needs Creator, $35 a month ($28 billed yearly), or higher [V, 56].

### 3.4 LoRA: what it is, when you need one, what it costs

**What:** a LoRA ("low-rank adaptation") freezes the big model and trains a small set of extra numbers on your pictures [V, 45]. The result is a file of roughly 10 to 200 MB that teaches one face, costume or style [V, 25].

**When:** only when reference images stop holding a face or style across many shots (Rule 14). Hosted models such as Nano Banana, GPT Image and Midjourney cannot load LoRAs; LoRAs work on open models (FLUX.2 klein and dev, Qwen-Image, Z-Image [V-sec, 76], SDXL) [J].

**Which base model, by license** (checked on each model's Hugging Face page [V, 92, 93]):

| Base model for a LoRA | License of the weights | Use it when |
|---|---|---|
| FLUX.2 klein 4B | Apache 2.0 (commercial use allowed) | Commercial project, open-model path |
| Z-Image and Z-Image-Turbo (Alibaba Tongyi) | Apache 2.0 | Commercial project; also trainable on Civitai [V, 50] |
| FLUX.2 klein 9B, FLUX.2 dev | FLUX Non-Commercial License | Personal or test project, or you buy a BFL commercial license; BFL's hosted klein 9B LoRA endpoint is a paid API and the simpler route [V, 22, 25] |
| Qwen-Image-2.1 | Qwen Research License (research and evaluation only) | Personal experiments only |

**How many images:** Black Forest Labs recommends 1024 pixels or larger, detailed captions with a made-up trigger word ("Describe everything visible except the style/concept you want to teach"), and 1,500 to 3,000 training steps for a character [V, 25]. Their Hugging Face guide suggests 15 to 40 images for a style [V, 26]; fal's trainer page says "9-50 images typically sufficient for style training; more for complex subjects" [V, 51]. For a character, 15 to 30 varied images (angles, expressions, light; same costume if you want the costume learned) is common practice [J]. The picks come from your character sheet work (Recipe R2), so you already have them.

**Cost and services (no graphics card needed):**

| Service | What it trains | Price | Difficulty |
|---|---|---|---|
| fal FLUX.2 [dev] trainer | FLUX.2 dev LoRA (non-commercial base weights; see license table above) | $0.0064 x steps ($6.40 per 1,000 steps; a 2,000-step character run is about $13) [V, 51] | Upload a zip of images with optional matching `.txt` captions; an LLM can drive it through the fal MCP server |
| Civitai on-site trainer | SD 1.5, SDXL, FLUX.1 dev, FLUX.2 dev, FLUX.2 klein 4B and 9B, Qwen-Image, Z-Image, Chroma, and video models (Wan 2.1, Hunyuan, LTX2) [V, 50] | From 500 "Buzz" (site credit) for SD 1.5 and SDXL; FLUX and video cost more [V, 50] | Web form; captions generated for you |
| Your own or rented GPU with `ostris/ai-toolkit` | FLUX.2 klein | About 1 hour on an RTX 4090, roughly $0.50 of rented time [V, 26] | Hard for a non-technical user; an LLM can write the steps |
| Black Forest Labs dashboard | Serves a klein 9B LoRA you upload (Customization, then Finetunes), from $0.015 per megapixel, the base price, during beta [V, 22, 25] | Per image | Upload file, call by `finetune_id` |
| No-code "identity" features | Higgsfield Soul ID: 20 or more photos (up to 80, 960 px or larger), trains in 3 to 5 minutes for 25 credits (about $1.25) on any paid plan, then works across Higgsfield's image models and several video models [V, 69]; Adobe Firefly Custom Models (public beta) [V, 41] | Plan credits | Easiest; locked to that platform |

### 3.5 Storyboard, canvas and all-in-one tools

| Tool | What it is | Current? | Cost | Can an LLM drive it? | What the user does by hand |
|---|---|---|---|---|---|
| **Boords** | Storyboard app with AI frames; name cast, locations and props once and `@`-mention them in every frame; Sketch, Vector or Photoreal styles; PDF, shot list and MP4 animatic export; "Boords Agent" [V, 58] | Yes | Solo $39 per month (250 AI images); Pro $75 (1,000); Team $125 (2,000); Agency $250 (3,000); billed yearly $26, $50, $85, $165 per month; free trial [V, 59] | Partly: public API and webhooks [V, 58] | Paste script, review frames |
| **StudioBinder** | Production-management suite; "The synced script automatically generates storyboards for each scene" (panels you fill), shot lists, heavily customisable PDF export; its editor accepts "any kind of image, including any made from an AI generator" [V, 60] | Yes | Free plan limited; paid plans reported from about $42 per month [V-sec, 85] | No public API found [U] | Upload images you made elsewhere; its page does not mention built-in AI images [V, 60] |
| **Storyboarder** (Wonder Unit) | Free open-source drawing app with a 3D "Shot Generator" for posing figures and cameras [V, 61] | Usable, not updated since Feb 2024 [V, 61] | Free | No | Pose mannequins, screenshot, use as a layout reference |
| **LTX Studio** | Script-to-storyboard-to-video; splits a screenplay into scenes and shots, extracts characters, objects and locations as reusable "Elements"; choose FLUX or Nano Banana models and set the aspect ratio up front (rebuilt Jan 6, 2026) [V, 62] | Yes | Free 800 one-time credits (personal use); Lite $15, Standard $35 (commercial use starts here), Pro $125 per month [V-sec, 63] | The storyboard app: no API found [U]. LTX's video models have a separate API [V-sec, 63] | Paste script, fix shots |
| **Katalist** | Script-to-storyboard; character library, 10 styles, posing tool, camera-angle control; ZIP, PDF, shooting-board export [V, 64] | Yes | 7-day trial; Essential $19 per month (200 image credits, 1 custom character), Pro $39 (700, 10 characters), Unlimited $99 [V, 97] | No [U] | Upload script, review |
| **Krea** | Canvas with its own Krea 2 model plus many partner models; Nodes; "Krea Agents" beta (Sep 3, 2026) [V-sec, 65] | Yes | API: Krea 2 Medium about $0.03 per image [V-sec, 65] | Yes: API | Build a node graph or brief the agent |
| **Magnific Spaces** (formerly Freepik Spaces) | Node canvas chaining image and video models. Freepik renamed itself Magnific on Apr 28, 2026 [V-sec, 66] | Yes | $20, $45, $280 per month tiers ($14.50, $33.75, $210 billed yearly) [V-sec, 66] | Spaces itself has no API; some Magnific tools do [V-sec, 66] | Wire nodes by hand |
| **Flora** | Node canvas, 50+ models including Nano Banana 2 and Pro, FLUX variants, Recraft V4 [V, 67] | Yes | Its site says "One plan. 50+ models" without a price; about $18 per seat per month reported [V-sec, 67] | **Yes: API and MCP server** [V, 67] | Little, if driven by MCP |
| **Figma Weave** (formerly Weavy; bought by Figma Oct 2025) | Node canvas for image and video pipelines, with models from Google, OpenAI, Runway, Black Forest Labs, ByteDance, Kling, Recraft and others, plus compositing tools (layers, inpaint, relight, depth) [V, 68] | Yes | Free 150 credits; Starter $24 per month [V-sec, 68] | Not mentioned on its site [U] | Wire nodes |
| **Higgsfield** Popcorn and Soul ID | Popcorn: up to 8 consistent frames per sequence; feed the last frame back in as a reference to continue longer sequences; Soul ID: a trained face reused across models [V, 69] | Yes (its Sora 2 export is stale) | Daily free credits; Soul ID needs a paid plan (plan prices not checked) [V, 69] | No [U] | Upload faces, generate |
| **Artlist** Studio and Original 1.0 | Cast characters, build locations, direct shots; own cinematic image model (Jan 25, 2026) [V, 70] | Yes | Not published in the post | No [U] | All by hand |
| **Google Flow** | Google's filmmaking app; Nano Banana images as "ingredients" for Veo video; Whisk merged in (2026) [V-sec, 75]; Nano Banana 2 is its default image model and cost zero credits at launch [V, 4] | Yes | Google AI plans; Pro and Ultra can buy extra Flow credits [V-sec, 8] | No [U] | By hand |
| **Google Pics** | New (Sep 1, 2026) Nano Banana image editor at pics.new: isolate one object and change it "without altering the rest", edit or translate text inside an image, several options per prompt, shared editing [V, 7] | Yes, rolling out | Google AI Pro ($19.99 per month) and Ultra, most Workspace business plans [V, 7; V-sec, 8] | No | Region fixes by pointing and clicking |
| **Intangible** | Browser 3D blocking: build a set, place cameras, animate the move, render [V, 71] | Yes | Not published on that page | No [U] | Place cameras by hand |
| **Cuebric** | Camera-ready environments for virtual production [V-sec, 78] | Yes | Not checked | No [U] | Specialist |

### 3.6 Reference libraries

- **ShotDeck**: hand-tagged film stills (lens, lighting, framing, color) from over 5,000 titles; about $12.95 a month or $99.95 a year, 14-day trial [V-sec, 72]. Use it to *find* a look, then describe the look in words or use your own generated style frame. Do not paste film stills into generators as references for a commercial project; that copies someone else's copyrighted frame [J].
- **Flim**: a competitor with AI visual search [V-sec, 72].

### 3.7 Three ways an LLM can operate image tools

| Path | How it works | Difficulty for the user | Cost | Good for |
|---|---|---|---|---|
| **Chat-only** | The LLM writes every prompt; you paste it into the Gemini app or ChatGPT, attach the listed reference images, download results, and name them as told | Easiest; no setup | Google AI Plus $7.99, Google AI Pro $19.99, or ChatGPT Plus $20 per month [V-sec, 8]; Google's usage limits reset every five hours up to a weekly cap [V-sec, 8] | Up to about 100 images a week [J]. Limits: in ChatGPT you get GPT Image 2.5 Flare and cannot choose Sunburst [V-sec, 11]; in the Gemini app Nano Banana 2 is the default [V, 4]; how many images the apps accept as attachments per message is not documented [U], so test with your largest reference stack first |
| **Node canvas** | You build one reusable graph (script text in, frames out) in Flora, Magnific Spaces, Figma Weave or Krea, following the LLM's wiring instructions | Medium | Plan credits | Repeatable batches without code |
| **Automated** | An LLM app with MCP servers (fal: `https://mcp.fal.ai/mcp`, 9 tools, the server itself free, you pay per model run [V, 52]; Replicate: hosted at mcp.replicate.com [V-sec, 53]; Comfy Cloud [V, 54, 55]; Flora [V, 67]) or with small scripts it writes against the Gemini, OpenAI, xAI or Runway APIs. Runway's single API key reaches GPT Image 2.5, Nano Banana Pro and 2, Seedream 5.0, Grok Imagine, Runway Gen-4 Image and Runway's video models, with credits at $0.01 each [V, 91, 96] | Setup once: create an account, add a payment card, paste an API key where the LLM tells you | Pay per image (Section 3.1) | Hundreds of frames, re-runs, drift checks |

The user must always do three things by hand, whatever the path: create accounts and add payment, approve the look of the asset sheets, and look at every keyframe before it is sent to video [J].

**Cost and difficulty at a glance for a 10 to 15 minute short like *The Catch*** (about 300 shots, about 120 of them going to video) [J, prices from Section 3.1]:

| Job | Images kept x tries | Cheapest sensible model | Approximate cost | Difficulty for the user |
|---|---|---|---|---|
| Asset bible (Recipe R2) | 330 x 3 | Nano Banana 2 at 2K ($0.101) or Pro ($0.134) | $100 to $135, or one month of a chat plan | Medium: you judge faces and approve looks |
| Greyscale storyboard (R3) | 300 x 2 | Nano Banana 2 Lite, batch ($0.0168) | About $10 (about $20 without batch) | Easy: pick one of two |
| Keyframes (R4) | 120 x 3 | GPT Image 2.5 Sunburst at high ($0.16 plus $0.01 per reference) or Nano Banana Pro 2K ($0.134) | $50 to $80 | Medium: you check hands, rings, text, mirror state |
| Insert graphics (R6) | about 30 SVG files | None: the LLM writes them | $0 | Easy |
| Optional LoRA for one lead (R8) | 1 run | fal trainer, 2,000 steps | About $13 | Medium with MCP; hard by hand |

---

## 4. Which tool for which aim

Choices below are **[J]** built on the verified facts in Section 3. "First choice" assumes the automated or chat path; the "no-code" column is for users who want a website that does it all.

| Aim | First choice | Second choice | No-code all-in-one | Why |
|---|---|---|---|---|
| Rough or greyscale storyboard frames for a whole film (hundreds) | Nano Banana 2 at 1K, batch mode, for frames with named characters; Nano Banana 2 Lite (no character-reference slot, objects only [V, 2]) for empty sets, inserts and distant figures | Seedream 4.5 or 5.0 Lite; GPT Image 2 in batch | Boords (Sketch style) or LTX Studio | Cheapest per frame with character references; batch halves the Gemini price [V, 1] |
| Character sheets (turnaround, expressions, hands) | Nano Banana Pro | GPT Image 2.5 Sunburst (API only; ChatGPT picks the model itself [V-sec, 11]) | Boords characters, LTX Elements, Higgsfield Soul ID | Pro takes 5 character references and is widely used for sheets; Sunburst best preserves a subject through edits |
| Location sheets | Nano Banana Pro or GPT Image 2.5 Sunburst | FLUX.2 pro (10 references) | Artlist Studio "scout locations" | Needs many angles of one space, kept identical |
| Prop sheets, transparent cut-outs | GPT Image 2.5 (transparent background) [V, 10] | Qwen-Image-2.1 (RGBA; non-commercial projects only) [V, 32], Seedream 5.0 Pro layers | Recraft | Clean isolated objects composite well |
| Photoreal keyframes for image-to-video | GPT Image 2.5 Sunburst at 2K or more | Nano Banana Pro at 2K or 4K; FLUX.2 max | LTX Studio, Flora | Top edit and text-to-image rankings [V, 43, 44]; custom sizes allow exact delivery aspect ratio |
| Multi-character frames (3 or more people) | Nano Banana Pro | Nano Banana 2 | Boords | Documented multi-character support [V, 2, 5] |
| Exact readable text (signs, labels) | Insert graphic (SVG written by the LLM) | Ideogram 4.0, Qwen-Image-3.0-Pro, GPT Image 2.5 | Recraft | Only a graphic is guaranteed letter-perfect |
| Mirror-reversed text | Insert graphic, flipped | (none reliable) | (none) | Image models tend to "correct" or garble reversed letters [J] |
| Exact pose or camera from a rough layout | Blender or Storyboarder screenshot as a layout reference | ChatGPT `@Sketch` [V-sec, 12]; ControlNet in ComfyUI [V, 46] | Intangible, Katalist posing tool | A picture of the layout beats a description of it |
| One look (palette, grain, light) across a sequence | Style frame attached to every request (in Nano Banana Pro's style slot; on other models as an ordinary reference labelled "style only") | Midjourney `--sref`; Recraft V4 Styles; Krea style references; Ideogram 4.0 hex-palette conditioning [V, 34] | Firefly Custom Models | Visual anchor instead of adjectives |
| A face that keeps drifting after 50 shots | LoRA on FLUX.2 klein 4B (commercial) or klein 9B / dev (personal) | Face adapter (PuLID) in ComfyUI | Higgsfield Soul ID, Firefly Custom Models | Training beats referencing once references stop holding |
| Fixing one hand, ring or label in a finished image | Edit model with a precise instruction, or inpainting | Google Pics object selection [V, 7]; Seedream box annotations [V, 29] | Midjourney Editor | Change the region, keep the rest |
| Finding a visual reference to describe a look | ShotDeck | Flim | | Tagged by lens, light, color [V-sec, 72] |
| Free, no-AI fallback | Storyboarder | Hand sketches photographed with a phone | | Always available |

---

## 5. Decision rules

Each rule is **[J]** unless it cites a source.

1. **If** the story is longer than about 20 shots, **then** build the asset bible (Recipe R2) before any storyboard frame, **because** every frame made before the sheets exist will have to be redone to match them.
2. **If** a shot will not become video, **then** stop at a greyscale storyboard frame, **because** color keyframes cost roughly 2 to 10 times more per image (a batch Nano Banana 2 Lite frame is $0.0168; a 2K keyframe is $0.134 on Nano Banana Pro or about $0.17 on GPT Image 2.5 high with a reference [V, 1, 91]) and nobody else needs them.
3. **If** you need more than 200 storyboard frames and have no reason to prefer another model, **then** use Nano Banana 2 through the batch mode for every frame with a named character, and Nano Banana 2 Lite for frames without one, **because** batch halves an already low price [V, 1] and only Nano Banana 2 (4) and Pro (5) have character-reference slots; Lite takes object references only [V, 2].
4. **If** a frame shows three or more named characters, **then** use Nano Banana Pro and attach one clean face crop per character, **because** it documents up to five character references [V, 2]; other models blend faces when overloaded.
5. **If** a keyframe must preserve a character's face exactly while changing the pose or setting, **then** make it with GPT Image 2.5 Sunburst (through the API) or Nano Banana Pro from the character sheet, **because** these lead on editing that keeps the subject [V, 44; V-sec, 11]. **If** you are on the chat-only path in ChatGPT, **then** accept that it chooses Flare or Sunburst for you, and check faces more strictly [V-sec, 11].
6. **If** the user refuses all setup, **then** use the chat-only path with the Gemini app or ChatGPT and have the LLM produce numbered prompts plus a checklist of which reference files to attach, **because** it needs no keys or code.
7. **If** the user wants the same chain run many times without code, **then** build it once in Flora (which also has an API and MCP server [V, 67]) or another node canvas, **because** the graph can be re-run per scene.
8. **If** you want Midjourney's look, **then** use it only for look development and style frames, never for the shot-by-shot run, **because** it has no public API and its terms forbid automation [V-sec, 20].
9. **If** text in the frame must be readable and exact (a tag, a label, a sign, a screen), **then** make it as an insert graphic and composite it, **because** even the best model still warns about text errors [V, 10].
10. **If** text must appear mirror-reversed, **then** make the correct text as an insert graphic and flip only that graphic, **because** asking a model for "backwards letters" usually yields normal or garbled letters.
11. **If** a whole location must appear mirrored, **then** generate it normally, flip the picture, and add the characters afterwards (Recipe R5), **because** flipping a frame that already contains characters flips their faces, rings and wounds too.
12. **If** a prompt mentions a character's left or right hand, **then** translate it into image terms ("on the hand nearest camera, on image-left") and check it after generation, **because** models place rings and wounds on random hands.
13. **If** a reference image carries a busy background, **then** crop or regenerate it on plain grey before using it, **because** reference backgrounds leak into the new image.
14. **If** a lead's face drifts noticeably in more than 1 frame in 10 despite a clean reference stack, **then** train a LoRA on 15 to 30 approved images from the sheets and switch that character's shots to an open model, **because** a trained identity holds better than a referenced one over hundreds of shots.
15. **If** a clip will use start and end keyframes, **then** make the end keyframe by editing the start keyframe, **because** very different frames make the video model cut instead of move [V, 73].
16. **If** the delivery aspect ratio is 2.39:1, **then** use a custom-size model or generate 21:9 and crop, **because** no preset list includes 2.39:1 [V, 2, 10].
17. **If** a location appears in several states (night and day, whole and broken), **then** generate the base state first and make each other state by editing it, **because** fresh generations move doors, windows and furniture.
18. **If** an asset is non-human or has unusual scale (a figure taller than a door), **then** put a scale object in every sheet view (a door, a person, a ruler), **because** models pull unusual things back toward human size.
19. **If** a sequence has an established style frame, **then** attach it to every request in that sequence and name its light in the prompt ("single torch from below, frame-left"), **because** light drifts between separate generations (see B2 for what the light should be).
20. **If** a tool shows a date older than six months or a model marked "preview", **then** re-check the maker's page before committing, **because** names and prices in this field change monthly (Section 3.2 lists casualties).
21. **If** the project is commercial (sold, paid for, or made for a client), **then** use hosted paid models, or open weights with a commercial license: FLUX.2 klein 4B, Z-Image and Qwen-Image-Edit-2511 are Apache 2.0 [V, 92, 93]. Do **not** self-host Qwen-Image-2.1 (research-only license), Ideogram 4.0 weights (non-commercial), FLUX.2 dev or klein 9B (FLUX Non-Commercial License) for it without buying a license [V, 32, 92, 94], **because** "open weights" does not mean "free for commercial use".
22. **If** a scene is violent or bloody (a gunshot wound, floating blood), **then** storyboard it in greyscale and describe injuries plainly and clinically, **because** safety filters refuse graphic phrasing more often than plain phrasing, and greyscale reads as drawing.
23. **If** you have fewer than 20 minutes to try a tool, **then** test it with your hardest asset (for *The Catch*, THE FIGURE with a door beside it), **because** easy prompts make every model look good.
24. **If** a frame shows a screen (tablet, monitor, visor), **then** generate the screen dark or green and composite the screen content as its own image, **because** screen contents need their own framing, text and, in *The Catch*, their own mirror state.
25. **If** an image will feed image-to-video, **then** generate it at 2K or larger in the delivery aspect ratio, **because** a 16:9 "1K" image is only 1376 pixels wide [V, 2] and upscaling later invents detail that the video model then animates.
26. **If** a sequence must hold one look and you are on Nano Banana 2 (which has no style slot [V, 2]), **then** either switch that sequence's keyframes to Nano Banana Pro (3 style slots) or attach the style frame as image 1 and write "Image 1 is for light, color and texture only; take nothing else from it", **because** an unlabelled style image leaks its content into the shot.
27. **If** a tool or feature is labelled alpha, beta, preview or "early access" (Midjourney's Edit Model, Comfy MCP, FLUX 3 Image, Firefly Custom Models on 2026-09-27), **then** use it for tests only and keep the main run on a generally available model, **because** betas change behavior and prices without notice.
28. **If** you need to re-run the exact same frame later (a fix to one detail, a client note), **then** prefer a model that accepts a fixed seed (Runway Gen-4 Image [V, 96], every open model in ComfyUI) and log the seed and full prompt in `index.csv`, **because** hosted chat-style models give a different image every time.
29. **If** the pipeline must hand off to video tools later, **then** export every keyframe as PNG with the shot number in the filename (`SC012_SH03_start.png`, `SC012_SH03_end.png`), **because** that is what image-to-video tools and node canvases expect to be matched to a shot.

---

## 6. The consistency system: the asset bible

### 6.1 Folder, names and index

Keep one folder per project with this layout (the LLM can create it and keep the index):

```
asset_bible/
  index.csv            one row per image: id, asset, state, view, mirror_state, file, look_line, script_quote, approved
  characters/  CHR_IONA_S1_front.png  CHR_IONA_S1_34L.png ...
  locations/   LOC_SHAFT_S1_wide.png  LOC_SHAFT_S1_ladder_up.png ...
  props/       PRP_FLASK_S1_front.png ...
  style/       STY_SEQ01_tunnel_torch.png ...
  inserts/     INS_TAG_goods_only_NORMAL.svg  INS_TAG_goods_only_MIRRORED.png ...
```

Name pattern: `TYPE_ASSET_STATE_VIEW`. `S1`, `S2` are states. `34L` means three-quarter view facing image-left. Add `_MIR` for a mirrored copy. One asset, one name, forever.

The **look line** is a fixed 25 to 40 word description of the asset that is pasted *unchanged* into every prompt where the asset appears. It is never paraphrased: synonyms are drift in word form. [J]

### 6.2 Character sheet

A complete character sheet has five parts. Make each as its own image; do not ask for all of them in one crowded image. [J]

1. **Hero portrait.** Chest-up, front, neutral expression, even soft light, plain mid-grey background. Generate 4 to 8 options; the user picks one. This picture is the identity anchor.
2. **Turnaround.** From the hero portrait, with an edit model: full body, front, three-quarter, side, back, same costume, same light, grey background, in one 16:9 or 3:2 strip. Then crop each view into its own file.
3. **Expressions.** Six head-and-shoulders crops tied to real beats in the script (not generic "happy, sad").
4. **Hands and marks.** Close-ups of anything that is left-right specific: rings, scars, wounds, a smile that lifts on one side. These are the details models get wrong.
5. **Costume states.** One full-body front view per state, made by editing the base turnaround ("same person, same pose, now wearing ...").

**Prompt pattern for a turnaround** (works on Nano Banana Pro, GPT Image 2.5, FLUX.2; [J] from practice and Google's reference guidance [V, 6]):

> "Using the attached portrait as the exact identity reference, create a character turnaround sheet of the same person: full body, front view, three-quarter view facing image-left, side view facing image-left, back view, standing in a relaxed neutral pose, arms slightly away from the body. [LOOK LINE]. Flat even studio light, plain mid-grey background, no text, no labels, no shadows on the floor. Keep the face, hair, body proportions and clothing identical in every view. 3:2 landscape."

**Prompt pattern for one expression** (one image per expression, not a grid) [J]:

> "Image 1 is the exact identity of this person; keep the face, hair and skin identical. Head-and-shoulders portrait, three-quarter view facing image-left, plain mid-grey background, soft even light. Expression: [BEAT, in physical terms, e.g. 'jaw clenched on a torch held crosswise between her teeth, eyes looking up, brow tight with effort']. [LOOK LINE]. No text. 4:5 portrait."

Describe the face's *mechanics* (jaw, brow, eyes, mouth corners), never an emotion word alone: "afraid" drifts to a stock scream; "eyes wide, lips pressed together, chin pulled in" holds. [J]

**Prompt pattern for a hands-and-marks close-up** [J]:

> "Image 1 is the exact identity of this person. Close-up of her two hands held palms down side by side on a plain grey table, fingers spread, seen from above. The hand on image-right is her LEFT hand and wears a plain gold wedding band on the ring finger; the hand on image-left is her right hand and wears no ring. [WOUND OR BANDAGE STATE]. Even light, no text."

Always state which *image side* each hand is on and say it twice (which hand, which side). Then check it by eye, because this is the detail models get wrong most often (Section 9).

**Checklist before approving a character sheet** (the user answers yes or no; the LLM can pre-check): same face in all views; hair length and parting identical; costume colors identical; the ring or mark on the designed side in every view; nothing written on the background; the back view shows the same hair and collar; body height in proportion to a door (for THE FIGURE) or a hand (for THE ANIMAL). [J]

### 6.3 Location sheet

1. **Layout first.** Ask the LLM for a simple floor plan or section drawing as an SVG (a code-drawn image it can write directly): walls, doors, windows, key furniture, heights. This fixes geography before any pretty picture exists.
2. **Master wide.** One wide image in the base state, with the layout drawing attached as a reference.
3. **Angles.** Three to five further views of the same space from the positions the shots will need (reverse angle, looking toward the door, the corner where the action happens), each made by editing or referencing the master.
4. **Details.** Close views of story-critical details (in *The Catch*: the bright sill, the empty brake brackets, the needle box).
5. **States.** Night, day, damaged, burning: each an edit of the base, never fresh.
6. **Empty.** Locations are sheeted without people. People are added per shot.

**Prompt pattern for the master wide** [J; structure from Google's reference guidance, V, 6]:

> "Image 1 is a floor plan of the room; follow its walls, doors and furniture positions exactly. Create a wide establishing view of this empty room from [CAMERA POSITION ON THE PLAN, e.g. 'the doorway at the bottom of the plan, looking toward the far wall'], eye height 1.6 m, [LENS FEELING from B1, e.g. 'moderately wide, little distortion']. [LOCATION LOOK LINE]. [LIGHT LINE from B2]. No people, no text, no signage unless listed. 16:9."

**Prompt pattern for each further angle:**

> "Image 1 is the master view of this room; Image 2 is its floor plan. Show the same room, unchanged in every object, material and light, now seen from [NEW POSITION ON THE PLAN] looking toward [TARGET]. Keep the same time of day and light direction relative to the room (the window stays on the room's east wall). No people. 16:9."

Say where the light comes from *in the room* ("from the window on the east wall"), not only in the image, because image-left changes with every angle. [J]

**Checklist before approving a location sheet:** doors, windows and fixed furniture in the same places in every view (compare against the plan); the same number of beds, rails, lamps; materials and colors identical; light enters from the same room-side; no people; no invented signs or text. [J]

### 6.4 Prop sheet

Front, three-quarter and top views on grey, plus one view in a hand for scale. Add every state (full, empty, cracked, burnt). Make a transparent-background version if the prop will be composited. [J]

**Prompt pattern** [J]:

> "Product-style reference sheet of one object: [PROP LOOK LINE, with real-world size, e.g. 'a small steel vacuum flask of the kind that keeps coffee hot, about 25 cm tall, with a flat matte-black disc about 8 cm across clipped underneath' (script: "a small steel FLASK, the kind that keeps coffee hot. A flat black PUCK clipped underneath it"; the sizes are design choices to approve)]. Three views side by side on plain mid-grey: front, three-quarter, top. Even soft light, no shadows on the background, no text or labels unless listed. 3:2."

Then crop each view to its own file. For the hand-for-scale view, attach the character's hand close-up as a second reference so the hand is the right person's hand. For a transparent cut-out, use GPT Image 2.5 (`background: "transparent"`, PNG or WebP output [V, 10]) or Qwen-Image-2.1 RGBA on a non-commercial project [V, 32].

### 6.5 Keeping light and color the same

What the light *should* be is decided in file B2 (lighting plan per location and a color script per sequence). This file covers how to make separate generations *obey* it:

1. **One style frame per sequence**, approved by the user, attached to every request in that sequence as a style reference (Nano Banana Pro has up to 3 style-reference slots; Nano Banana 2 and 2 Lite have none, so label the style frame in the prompt, Rule 26 [V, 2]; Midjourney uses `--sref` [V-sec, 18]).
2. **Name the light the same way every time**: source, direction in image terms, hardness, color ("single hand torch, from below frame-left, hard, cool white"). Copy it from the B2 plan; never improvise per shot.
3. **Name the palette** with plain color words (and hex codes if the model accepts them) in the style frame's prompt, and reuse the phrase.
4. **Grade afterwards.** Run all approved keyframes of a sequence through one color correction in a grading tool (for example DaVinci Resolve's free version) so small shifts are evened out. [J]
5. **Check in sequence.** View frames in story order as a slideshow; drift in light shows up only side by side. A practitioner checklist for Nano Banana Pro storyboards checks exactly this: "Lighting direction is consistent between adjacent frames", and warns of "Sudden jumps from day to night" [V-sec, 74]. The slideshow itself is [J].

### 6.6 The reference stack for one shot

For every shot, the breakdown lists what to attach. Typical stack, in this order [J]:

1. Style frame of the sequence (1 image).
2. Location view closest to the shot's camera position (1 image).
3. For each character in frame: the face crop plus the costume-state full body (2 images each).
4. Each story-critical prop in frame (1 image each).
5. Optional layout reference (Blender or Storyboarder screenshot, or a stick sketch).

Then state in the prompt what each image is for: "Image 1 is the style. Image 2 is the room. Image 3 is Iona's face; image 4 is Iona's costume. Keep image 3's face exactly." Google's guide recommends exactly this pattern: reference images, a relationship instruction, then the new scenario [V, 6]. Stay under the model's documented limits (Section 3.1). If the stack exceeds them, drop props first, then the location, never the faces.

**Counting the stack on Nano Banana.** Google's limits are fidelity limits, not labelled upload slots: you simply attach images, and the model keeps up to 4 (Nano Banana 2) or 5 (Pro) *people* faithfully and up to 10 or 6 *objects* [V, 2]. So count every image showing a person as a character image [J]. With 3 characters at 2 images each (6), you exceed both models; instead attach **one** image per character, a full-body three-quarter view of the right costume state in which the face is large and sharp, and put the tight face crop back only for the character nearest camera. Example for W1 (Iona, Jude, Eli in the cage) on Nano Banana Pro: Iona face crop, Iona full body, Jude full body, Eli full body = 4 people images (limit 5); style frame (style slot); cage interior view = 1 object image (limit 6). [J]

**One image request per shot, written so any tool can take it.** The breakdown should carry, for every shot that needs an image, a block like this (the LLM fills it; a script, node canvas or person can execute it; nothing in it is specific to one model except the `model` line) [J]:

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

**If** the user later wants storyboards skipped, **then** leave `purpose: storyboard` blocks out; **if** they want only storyboards, **then** leave the keyframe blocks out. The rest of the breakdown is unaffected.

### 6.7 When to stop referencing and train

Watch the drift rate in Recipe R7. Under 1 in 10 frames: keep referencing. Above that for a lead: train a LoRA (Section 3.4) or use a no-code identity feature. For locations, drift is fixed by using more location views, not by training. [J]

---

## 7. Text in images, and the mirror world of *The Catch*

### 7.1 Ordinary text

What works across current models [V, 5, 6, 10; J]: put the exact words in quotation marks; say the font style ("stencilled block capitals, faded yellow paint"); keep it short (one to four words); say where it sits; generate at 2K or more; check every letter at full size. For anything the audience must read, or anything repeated across shots (a label, a tag, a wristband), make an **insert graphic** instead: ask the LLM to write it as an SVG file (a text-based drawing format the LLM can produce directly, which opens in any web browser), export it as a PNG image, and composite it. It will be identical every time.

### 7.2 The flip method, and what goes wrong

A mirror-reversed world is cheap to make: generate the place normally, then flip the picture left to right. Any image editor does it; an LLM can also do it with a three-line script (`ImageOps.mirror` in the Python Pillow library). Everything in the picture reverses at once: letters, the running man on the exit sign, the side the steering wheel is on, the side the light comes from. That is exactly what *The Catch* needs for its world after the cage turns. What goes wrong [J]:

1. **People and turned objects in the plate flip too.** A flipped frame moves Iona's ring to her other hand, Eli's crooked smile to the other side of his face, Jude's wound to the other shoulder. Fix: flip plates *without* the turned characters in them, then add those characters (Recipe R5).
2. **Text that must read correctly becomes backwards.** Things that turned with Iona read normally to her: "Iona reads the label. The letters face the right way." Fix: add them as normal insert graphics after the flip.
3. **Mixed objects.** A NORMAL person can carry a MIRRORED thing: Iona's pressure suit ("Every word printed on it reads backwards to her") or the wristband on her wrist. Fix: build the costume normally, then add the lettering as a flipped insert graphic.
4. **Screen direction flips.** Whoever looked toward image-left now looks toward image-right. Composited characters must be posed to match the flipped plate's eyelines and exits.
5. **Light direction flips.** A character lit from the left pasted onto a plate now lit from the right looks cut out. Fix: ask the edit model to "relight the added person to match the background's light direction", then check.
6. **Edit models "un-flip".** When asked to add a person to a plate with backwards letters, a model may quietly correct or garble the letters. Fix: put the lettering on last, as an insert.
7. **Asking for backwards text directly fails.** "The word RECEIVING written backwards" usually returns normal letters, garbled letters, or a mix. Fix: always produce correct text, then flip the graphic.

### 7.3 Mirror states in *The Catch*

**The camera rule (from the script):** the camera sees what Iona sees. Evidence: after the cage turns, "Every letter is backwards"; the blanket's OSTREL is "Backwards"; the wristband shows "Her own name, printed backwards"; at the end Eli's smile is "on the wrong side of his face". So an asset renders **NORMAL** when it shares Iona's handedness at that moment and **MIRRORED** when it does not.

| Era | Runs from, to | NORMAL (render as designed) | MIRRORED (render flipped) |
|---|---|---|---|
| **A** | FADE IN to the cage going black ("A hard metal CLACK. BLACK.") | Everything | Nothing |
| **B** | "Her eyes open. Everything is in the wrong place" to Iona's own turn beside the falling ship ("She fires ... Then stars ... Iona already inverted") | Iona, Eli, Jude, their clothes, blood and wounds; the flask; the cage, its red tag and puck; everything later found from the cage (wreck, bloody cloth, one shoe, shirt strip); the sealed meals Saye turned; **by inference** the ship, THE FIGURE and the ship's food ("Its own food, and we can eat it. Turned, like us.") | The factory, passage signs, fire-exit sign, street, car and bus; Saye, the nurse, guard and technician; Saye's house and mint; the blanket, wristband, pressure-suit lettering; Nell and her photo (she never turned: "Hers it has to go and find"); **by inference** every picture shown on a world screen (tablet, monitors) |
| **C** | Iona back in the receiving room ("On the wall above Saye: RECEIVING. Iona looks at it. Reads it again.") to the end | Iona, the world, Saye, Nell, the receiving-room sign, the vessel and THE ANIMAL (turned with her) | Eli and Jude ("His wedding ring. On his right hand."), their meals ("The labels run opposite ways") |

Practical consequences for the asset bible:

- **World locations** that appear in both Era A and Era B (the treatment-floor corridor, Eli's room, the passage) get one normal location sheet and one flipped `_MIR` set. In Era B, the corridor's layout is reversed: Eli's "last room" is at the other end. That is correct, not an error.
- **Saye** and **Nell** need normal and `_MIR` character sheets. Saye's ring is on her left hand in her own design; in Era B it shows on her right ("Saye's wedding ring. On her right hand.").
- **Eli** and **Jude** need `_MIR` sheets for Era C only. Record *now* which side Eli's half-smile lifts and which shoulder Jude is shot in, or the flip cannot be checked. Jude's appendix scar is a fixed script fact: on his right in Eras A and B (the kitchen scene depends on it: "That's his right. The scar. It's where it should be."), so in any Era C shot showing it, it appears on his left.
- **Iona never flips.** Only objects on or around her do.

### 7.4 Unresolved logic the director must decide before any text asset is made

1. **The toy carriage's F.** The script says the F is normal at the start, "backwards" after one turn, and "faces the right way" after two. Under the camera rule, a world-made F would *look* backwards to Iona from the start and *normal* after one turn, the same way the turned meal label reads correctly. Options: (a) follow the script's wording and treat this scene as the one exception, (b) follow the rule strictly and let the audience see it reversed, (c) show the demonstration on Saye's recording so the camera is a world camera. The image tools can do any of these; the choice is a story decision.
2. **World screens.** By the rule, everything shown on a world monitor or tablet (the security feed of Jude's room, the paused cage footage, the dish labels "CONTROL" and "VALE. CAR. STEERING WHEEL.") would appear mirrored, including Jude inside the feed. That is a clever clue but costs readability; Iona's line "That's off my wheel" carries the meaning if the labels are hard to read.
3. **The copied name "IONA VALE"** on the collection-room container. It was "copied from a hospital wristband stroke for stroke" by someone "who did not know they were letters". If the wristband read backwards to Iona, a faithful copy reads backwards too, in Era B. In Era C the container turned with her, so strictly it still reads backwards to her. The script prints it normally. Decide and log it.

---

## 8. Recipes

Each recipe says who does what. "LLM" means the assistant running the pipeline; "You" means the user.

### R1. Choose a path and set up (30 to 60 minutes, once)

1. **You** tell the LLM your monthly budget and whether you will paste prompts by hand.
2. **LLM** recommends a path from Section 3.7. Rule of thumb [J]: under 150 frames, chat-only; 150 to 600, a node canvas or one automated model; over 600, automated with batch pricing.
3. **Chat-only:** you subscribe to Google AI Pro or ChatGPT Plus. Nothing else.
4. **Automated:** you create one account (fal, Replicate, or Google AI Studio), add a payment card, set a spending cap, copy the API key, and paste it where the LLM's instructions say (for fal in Claude Code, the LLM gives you the one-line `claude mcp add` command from fal's page [V, 52]). Never paste keys into a chat message.
5. **LLM** runs one test image with the hardest asset (Rule 23) and shows you the cost of that image.

### R2. The asset-sheet process for *The Catch*

**Step 1. Extract assets (LLM, 10 minutes).** Read the script and list every character, costume state, prop and location with the exact lines that describe them. Separate *script facts* (must obey) from *design choices* (the LLM proposes, you approve). The result for the cast:

| Character | Script facts (quoted or close) | Design choices to approve [J] | States to sheet |
|---|---|---|---|
| **IONA** | "late thirties"; puts "the torch between her teeth" to climb; lifts "with her legs, not her back"; shirt is blue (the torn sleeve is "a strip of blue cloth"); ring "on her own left hand"; chips a front tooth ("finds a new edge"); skinned then bandaged palm; white pressure suit with lettering; engine locked "onto the harness between Iona's shoulders" | Lean, strong forearms; hair tied back; dark work trousers, boots; which sleeve is torn | S1 climbing kit; S2 after the cage (sleeve gone, skinned palm, blood under nails); S3 quarantine (blanket, bandage, wristband); S4 pressure suit, harness, engine, wrist display; S5 suit with vessel strapped to chest; S6 final, in the clear plastic tent |
| **JUDE** | "forties, easy in the shoulders"; "a hole through his shoulder"; "an old white scar low on his belly", on his right side as designed (Iona: "That's his right. The scar. It's where it should be."); wedding ring (seen "On his right hand" in Era C, so on his left as designed) | Build, hair, clothing; **which shoulder is shot** | S1 unhurt; S2 wounded, blood; S3 dressed wound; S4 on the ship, "fresh dressing ... neater"; S5 paper oversuit; S6 arm strapped across chest. `_MIR` copies for Era C |
| **ELI** | "thirties, thin, a beard she has never seen"; "the crooked half-smile"; one wrist strapped; leaves one shoe behind; wears a coat | **Which side the smile lifts; which foot keeps the shoe** | S1 strapped to the bed; S2 escape (coat, one shoe); S3 quarantine; S4 ship glass room; S5 paper oversuit. `_MIR` for Era C |
| **DR SAYE** | "fifties, grey and tidy, fully dressed at four in the morning"; wedding ring; later "inside a protective hood" | Clothing, glasses or not | S1 kitchen; S2 quarantine; S3 protective hood. Normal and `_MIR` |
| **NELL ROWAN** | "Sixty, perhaps. She looks older"; thin wrists; a book; file photo "much younger. A flight suit. Unsmiling" | Face shared across two ages | S0 photo, 19 years younger, flight suit; S1 ship; S2 paper oversuit. Normal and `_MIR` |
| **THE FIGURE** | "tall and black"; "Its head sits low between its shoulders"; "Taller than the door"; "a pale strip slides across" where a face would be, under "a transparent cover"; "A huge black thumb"; a black cell "between its shoulders"; chest opens on latches | Height about 2.4 m; matte black; no eyes; describe shapes plainly (words like "robot" or "armor" pull toward clichés) | S1 intact; S2 cover cracked, white jet; S3 patched strip, fluid beneath, carrying a tank; S4 cell removed, strip dimmed; S5 chest open; S6 empty body against the wall |
| **THE ANIMAL** | "Almost clear, like a thing from the bottom of the sea. No longer than her hand"; fine limbs that draw out of "a socket in the wall of the vessel"; vessel of "dark water about as long as her forearm"; a small pump; "the soft sealed sleeve in the wall of its vessel" | Body shape (glass-squid-like, faint internal structures); no eyes or tiny ones | S1 in the mount inside the open chest; S2 strapped to Iona; S3 in the padded tray; S4 bedside on a folded cloth, container attached, cloudy growth "half the container" |

And for the three key locations:

| Location | Must-have elements (script) | Sheet views | States |
|---|---|---|---|
| **Freight shaft and cage** | Wet brick tunnel; cage "floor and its roof are the same open steel grid"; red tag on the gate ("Goods only. No persons."); control box, STOP button; "Two brake brackets, empty. Four bright bolt holes in each"; ladder bolted to the brick; a rung sheared on one bracket; "A band of yellow paint circles the whole shaft at head height"; gates with light under them; "a tall maintenance opening" halfway with a steel sill "worn bright"; top mesh gate; a camera above the top gate looking down | **Section drawing first** (LLM-written SVG with heights: ladder, yellow band, opening, gates); tunnel wide; cage exterior; cage interior looking down through the grid; shaft looking up from the cage; shaft looking down from the ladder; opening and sill from inside the cage; top-down security view | Normal; falling (interior, loose objects afloat); inverted and rising; the wreck on the ship (roof crushed, puck "burnt into the grid") |
| **Quarantine rooms with glass partitions** (inside the same medical factory: "The same corridor, by daylight") | Corridor with "A window into every room"; sealed rooms with beds; glass between rooms; service hatch with sealed gloves; transfer drawer; "a grey box with a needle in it" over each bed; oxygen cylinder; frosted windows with police lights; demonstration room (ramp, block, toy carriage); observation room (desk, monitor turned to the glass); receiving room (yellow line, padded floor, sign "RECEIVING") | Floor plan first; corridor both directions; one room from the bed; one room through the glass from the next room; two rooms seen together through a partition; demonstration bench; receiving room wide | Night (Era A, NORMAL); morning and night (Era B, `_MIR`); Eli's window broken, then boarded; "A clean square on the floor where Eli's bed stood"; day (Era C, NORMAL) |
| **Ship's human rooms** | "A long dim chamber"; "three glass rooms, each with a hospital bed in it"; drawers through the walls; Nell's shelf (bowl and spoon, drawings, old harness with empty socket and dated tag); rack of six sockets, "Five empty, the metal round them scorched", one black cell "the size of a paving stone"; service cavity with a low window showing "Stars. Below her feet"; collection room (the cage wreck, sealed containers, glass-fronted cabinet, cables into the deck) | Floor plan; chamber wide both directions; each glass room; Nell's shelf detail; the rack; collection room wide; cabinet detail; service cavity window | Calm; rack emptied; shell light red, then green; collection room burning; deck tilting (camera tilt, not a new sheet). NORMAL in Era B by inference (Section 7.3) |

**Step 2. Write the look lines (LLM, you approve).** One fixed 25 to 40 word line per character and location, built only from the table. Example: *"IONA: a lean woman in her late thirties, strong forearms, dark hair tied back, weathered face, plain faded blue work shirt, dark work trousers, scuffed boots, simple gold wedding ring on her left hand."*

**Step 3. Hero portraits (about 8 images per character).** Nano Banana Pro or GPT Image 2.5 Sunburst; plain grey background; even light. You pick one per character. For THE FIGURE and THE ANIMAL, make a full-body or full-object hero image with a scale object (a standard door; a human hand).

**Step 4. Turnarounds, expressions, hands, states (about 12 to 20 images per character).** Use the prompt pattern in Section 6.2. Tie expressions to beats: Iona counting rungs with the torch in her teeth; "not steady" after the mint; "Stay there"; exhaustion at the end. Eli: the crooked half-smile; the flat look at "the backwards city". Hands sheet: every ring and wound. Crop each view into its own file and name it (Section 6.1).

**Step 5. Location sheets (about 15 images per location).** Section 6.3 order: layout drawing, master wide, angles, details, states. For the shaft, attach the section drawing to every shaft image.

**Step 6. Prop sheets (about 4 images per prop).** The flask with the black puck "clipped underneath"; the red tag; the toy carriage with its F; engine heads ("Black. Heavy. The size of a loaf"); the courier pod ("open like a little suitcase"); the black cells; the vessel; the oxygen cylinder; the needle box; the wristband, blanket and meal labels (as insert graphics, Recipe R6).

**Step 7. Mirror copies.** Flip every Era B world location, Saye and Nell into `_MIR` files; flip Eli and Jude for Era C (Section 7.3). Check that anything written on those assets is meant to be flipped.

**Step 8. Style frames.** One per sequence, from B2's color script (tunnel and shaft torchlight; Saye's kitchen before dawn; quarantine morning; quarantine night; the ship's dim chamber; outside the ship among stars).

**Step 9. Drift check (Recipe R7)** on every sheet against its look line.

**Budget [J]:** about 7 characters x 30 + 3 locations x 20 + 15 props x 4 + 8 style frames, roughly 330 kept images; with about three tries per kept image, about 1,000 generations. At Nano Banana 2's 2K price ($0.101 [V, 1]) that is about $100; at Nano Banana Pro ($0.134) about $135; on the chat-only path it is a month of subscription and several evenings.

### R3. Storyboard pass (greyscale)

1. **LLM** takes each shot from the breakdown and writes one prompt: the greyscale style line (Section 2.1) + the shot's framing and lens from file B1 + the look lines of what is in frame + the light line from B2 + the reference stack list.
2. **LLM or you** generate 2 options per shot at 1K: Nano Banana 2 for shots with named characters (their face crops attached as character references), Nano Banana 2 Lite for shots without (Rule 3). Cost for 300 shots: about $10 in batch mode, about $20 without [V, 1; J].
3. **You** pick one per shot (or say "neither" and why). Allow about 10 seconds per shot, so about an hour for 300 shots.
4. **LLM** places frames in shot order in a storyboard tool (Boords or StudioBinder) or a simple slide deck, and adds shot numbers, arrows and dialogue there, never in the image.
5. Run the drift check (R7) on each batch of about 20.

### R4. Keyframe pass (for image-to-video)

1. Only for approved shots. Re-compose for the *first instant* of the shot (Section 2.2).
2. Use GPT Image 2.5 Sunburst (API, quality `high`, about $0.16 plus $0.01 per reference [V, 91]) or Nano Banana Pro ($0.134 at 2K [V, 1]) at 2K or more, in the exact delivery aspect ratio (Section 2.3, Rule 25). Budget about three tries per kept keyframe.
3. Full reference stack (Section 6.6), style frame first.
4. State every left-right fact in image terms ("wound on his left shoulder, which is on image-right because he faces camera").
5. Leave room for motion: if the camera will push in, frame wider; if something will enter, leave that space empty.
6. No arrows, no captions, no watermark-like marks.
7. Check: face, costume state, hands and rings, props, text, mirror state, light direction. Fix locally with the edit model or inpainting; do not regenerate a mostly-good frame.
8. If the clip needs an end frame, edit the start frame into it [V, 73].

### R5. A mirrored plate with un-mirrored people

1. Generate or reuse the location view **with no people in it**, in the world's own orientation.
2. Flip it (any editor, or the LLM's Pillow script). Save as `_MIR`.
3. Attach the flipped plate plus the NORMAL character sheets to an edit model: "Add the woman from image 2 standing at the door on image-right. Do not mirror her. Keep the background exactly as given, including all lettering. Match the background's light, which comes from image-left."
4. Composite any lettering that must stay reversed or must read normally last (R6).
5. Check the four mirror questions: Are world letters reversed? Do turned items read normally? Are rings, smiles and wounds on the designed sides? Does light match?

### R6. Screens, signs and labels as insert graphics

1. **LLM** writes an SVG for each graphic: the red tag, the stencilled floor number, the fire-exit sign, the wristband, the blanket's OSTREL, the meal labels, the dish labels, the wrist display and visor (with its exact words: "RECEIVING", "HULL CLEARANCE", "TURN", "CROSS AT 0", "UPWARD SPEED").
2. For a mirrored version, the LLM wraps the whole drawing in one group that flips it in place and saves a second file: `<g transform="translate(W,0) scale(-1,1)"> ... </g>`, where W is the SVG's width. (A bare `scale(-1,1)` flips the drawing around the left edge and pushes it out of view, leaving a blank image.) The LLM then checks the PNG by eye: every letter reversed, nothing cut off.
3. You open each SVG in a web browser and take a screenshot, or the LLM converts it to PNG.
4. Composite onto the plate: ask an edit model to "place the attached graphic onto the wall in perspective without changing any letters", or use any editor with a perspective tool. Check every letter afterwards.
5. For screens, generate the device with a dark screen, then composite the screen content as a separate image (its own framing, its own mirror state).

### R7. Drift check (LLM with image viewing, 5 minutes per batch)

1. For each new image, the LLM compares it with the asset sheets and answers a fixed list: face match (yes/no), hair, costume state, colors, rings and wounds on the right sides, prop details, text exact, mirror state correct, light direction as planned.
2. Any "no" gets a one-line fix instruction for the edit model.
3. The LLM logs the drift rate per character in `index.csv`. Above 1 in 10, apply Rule 14.

### R8. Optional LoRA for a lead (only if R7 says so)

1. Pick 15 to 30 approved images of the character from the sheets and keyframes: varied angles, expressions and light, one costume.
2. The LLM writes captions with a made-up trigger word (for example `ionavale01`) and describes everything *except* the face [V, 25, 26].
3. Pick the base model by license first (Section 3.4 table): FLUX.2 klein 4B or Z-Image for a commercial project; klein 9B or dev for a personal one. Train on fal (FLUX.2 dev trainer: 1,500 to 3,000 steps is about $10 to $19 [V, 51]), Civitai (Buzz credits [V, 50]), or a rented GPU with ai-toolkit (about $0.50 for a klein run [V, 26]).
4. Test on 10 shots before switching the whole sequence. **If** 9 of 10 pass the R7 face check, **then** switch; **if** not, add 10 more varied training images and retrain once; **if** it still fails, fall back to a no-code identity feature (Higgsfield Soul ID) and accept platform lock-in.

---

## 9. Failure modes and workarounds

All entries are **[J]** (observed behavior of this class of model) unless a source is given.

| Failure | What you see | Why | Workaround |
|---|---|---|---|
| Identity drift | The face ages, widens, or turns into a generic model face over many shots | Each generation re-interprets the reference | Attach the face crop every time; shorter look lines; the drift check; LoRA if the rate passes 1 in 10 |
| Costume drift | Iona's blue shirt turns grey or teal; the sleeve reappears | Costume words are weak; lighting shifts color | Costume-state image in every stack; color word identical each time; state named in the prompt ("left sleeve torn off at the shoulder") |
| Handedness errors | Rings, wounds, scars, the half-smile on the wrong side | Models do not track left and right reliably | Image-side wording (Rule 12); carry the story point with separate close-ups; fix by inpainting |
| Reference bleed | The grey sheet background, or the sheet's flat light, appears in the shot | The model copies the whole reference, not just the face | Crop references tight; attach the style frame; say "use image 3 for the face only" |
| Sheet-layout bleed | You ask for a shot and get several frames side by side or a turnaround again | A multi-view sheet was attached | Attach single-view crops, never the whole sheet |
| Scale collapse | THE FIGURE comes out human-sized; the cell looks like a phone | Priors toward everyday sizes | Scale object in every sheet view; numbers in the prompt ("about 2.4 m, head above the top of the door frame") |
| Cliché pull | THE FIGURE gets glowing eyes and armor plates | Words like "robot", "alien", "exosuit" trigger stock designs | Describe shapes plainly; always attach the hero image; say what is absent ("smooth featureless head, no eyes, no mouth") |
| Garbled or "corrected" text | "GOODS ONLY. NO PERSONS." misspelt; backwards letters turned forwards | Text is drawn as shapes | Insert graphics (R6), flipped when needed; check every letter [V, 10] |
| Flip damage | People and turned items flipped along with the world | The flip affects every pixel | Flip empty plates only, then add people (R5) |
| Gravity default | In the falling cage, people stand on the floor and hair hangs down | Almost all training images have gravity | Say "weightless" and describe the evidence: hair spreading, loose cloth drifting, bodies horizontal, feet off the grid; generate composition first, then edit in the floating details |
| Blood as marbles | Floating blood looks like glass beads or bubbles | Few real references | Describe "small dark red liquid spheres of different sizes, wobbling, catching the light"; public photos of water spheres on the space station are a useful physics reference (check each image's terms) |
| Transparency failure | THE ANIMAL comes out milky white or solid | Translucent bodies are hard to render | Put it against the dark water and a lit tube behind it; say "transparent body, faint internal structures visible, light passing through" |
| Glass confusion | Glass partitions vanish, or reflections copy the wrong room | Reflections are poorly modeled | Name the glass in every quarantine prompt ("seen through a glass partition, faint reflections of the viewer's room on the glass"); add a door frame or hatch so the glass reads |
| Light jumps between shots | Key light moves sides; color temperature shifts | Each generation relights | Style frame; identical light line from B2; grade the sequence together (Section 6.5) |
| Refusals | Wounds, blood or the gun refused or softened | Safety filters | Clinical wording; greyscale; show aftermath rather than impact; keep the gun out of the keyframe if the shot allows |
| Hidden marks | Images carry invisible provenance marks | Google adds SynthID and C2PA credentials to every output [V, 2, 6] | Not a problem for storyboards; note it when delivering to a client who asks about AI provenance |
| Model disappears | A model or API shuts down mid-project | Fast turnover (Section 3.2) | Keep the asset bible model-neutral: images plus look lines work on any successor |

---

## 10. Worked examples from *The Catch*

Framing and lens choices come from file B1 and light from B2; they are stated here only so the image steps are concrete.

### W1. Zero gravity in the falling cage (Era A, all NORMAL)

> "The cage falls. Her boots leave the floor. She gets her fingers into the grid. Her body floats out behind her like washing. Jude's blood lifts off the steel in round red beads and hangs in the air between them, turning."

**Storyboard frame.** Greyscale value sketch, 16:9. Inside the cage from the gate corner, slightly high. Iona on image-left, fingers hooked in the floor grid, body horizontal toward image-right "like washing". Jude slumped across Eli's arms on image-right behind the control box; Eli's hidden hand behind Jude's back. Blood beads in the space between. Light: bands of gate light passing across everything (B2's shaft plan: "Light, brick, light, brick").

**Keyframe (the clip's first instant).** Iona's fingers already in the grid, boots just off the floor, beads only beginning to rise, so the video model continues the motion instead of inventing it. Reference stack (6 images): style frame for the shaft sequence; `LOC_CAGE_S1_interior`; `CHR_IONA_S1` face and full body (sleeve still on; it becomes Jude's bandage in the passage; front tooth already chipped from the ladder); `CHR_JUDE_S2` full body (wounded); `CHR_ELI_S2` full body (one shoe; coat). That is 4 people images, within Nano Banana Pro's 5 (Section 6.6). Prompt core: "Everyone is weightless: Iona's hair spreads upward and outward, her body floats horizontal behind her hands, loose cloth drifts; small dark red liquid spheres rise from the steel grid between them, slowly turning. Bands of light from the passing landing gates slide across the scene." Checks: grid floor and roof identical; red tag visible on the gate; wound on the designed shoulder; Eli's second hand hidden.

**Companion shot.** "Through the grid, the yellow stripe. Coming." Iona's point of view straight down through the floor grid; the yellow band as a thin bright ring far below. Use the shaft section drawing to get the band's height and the ladder's side right.

### W2. The backwards stencil and exit sign (Era B: world MIRRORED, the three of them NORMAL)

> "Stencilled on the wall in big letters, the kind that tell you which floor you are on: a floor number, and a word. Every letter is backwards. ... At the fire door, the green sign is backwards too. The little running man is running the other way."

1. Plate: the maintenance passage with **no people**, normal orientation, a blank wall panel where the stencil goes, and a blank green sign over the fire door.
2. Insert graphics (R6): the stencil (the script gives no floor or word; propose one, for example "4 PLANT", and log it as a design choice) and a plain exit sign with a running figure.
3. Composite the inserts onto the *unflipped* plate, then flip the whole plate. Letters and running man reverse together, matching the world's reversal exactly.
4. Edit model adds Iona, Eli and Jude **without flipping them**: Eli with the flask "in his fist" and the empty clip under it; Jude pressing the sleeve to his shoulder; Iona's left sleeve gone (or whichever arm was approved). Tell the model not to alter any lettering; add lettering last if it does.
5. Storyboard sequence: wide of the three moving; close-up of the stencil (backwards); Iona's look; "Looks again"; close-up of the exit sign.

### W3. "Like a woman and her reflection" (Era B, the kitchen)

> "Iona holds it up. Saye holds up hers. They stand facing each other across the table like a woman and her reflection, each with the wrong hand in the air. ... Saye's wedding ring. On her right hand. Iona looks down at her own ring, on her own left hand."

Saye and her kitchen are world, so both are MIRRORED; Iona and Jude are NORMAL. Two easy routes: (a) generate Saye *in* her kitchen from her normal sheet, flip that whole plate, then add Iona and Jude; or (b) use the `_MIR` Saye sheet and the `_MIR` kitchen together. Route (a) is simpler because world things flip together. In the pre-flip plate, prompt Saye on image-left facing right, raising her right hand (the hand nearest the camera), gold ring on her lowered left hand; after the flip she stands on image-right exactly as the script needs.

Translate the hands into image terms. Camera side-on to the table, Iona on image-left facing right, Saye on image-right facing left. Iona raises her right hand, which is the hand **nearest the camera**. Saye raises her own right hand, which, rendered mirrored, looks like her left: also the hand **nearest the camera**. So the prompt says: "Both women raise the hand nearest the camera, palms toward each other, exactly like a reflection." Each ring sits on the lowered hand farthest from the camera. Rings are too small to read in the wide, so the story point lives in two close-ups: Saye's hand with the ring on what appears as her right hand; Iona's ring on her left. Make these close-ups separately, check them against the hands sheets, and fix by inpainting if needed.

### W4. THE FIGURE on the tablet (Era B: two layers with different mirror states)

> "Something tall and black stands beside his bed. It did not come through the door. It is simply there, in the space between one moment and the next. THE FIGURE. Its head sits low between its shoulders. Where a face would be, a pale strip slides across, vanishes, slides across again."

**Layer 1, the feed.** Generate as its own 16:9 image: a high corner security-camera view of Jude's room, wide lens, flat light, a little soft. Stack: `CHR_FIGURE_S1` hero (with the door for scale), `CHR_JUDE_S3` (dressed wound), `LOC_QUAR_room_S2`, the cup and the empty chair. Prompt: "a very tall figure, head top well above the door frame, matte black, smooth featureless head set low between the shoulders, a pale horizontal band of light behind a clear cover where a face would be, no eyes." Any timestamp is an insert graphic.

**Layer 2, Iona's room.** Her room is world (`_MIR` plate); Iona is NORMAL, tablet on her knees, screen dark.

**Composite** the feed onto the tablet screen. If the director chooses the strict rule for world screens (Section 7.4), flip the feed first, so Jude appears mirrored inside it.

**Keyframe for video.** The moment before the figure is there: empty space beside the bed, so a cut or a one-frame appearance ("between one moment and the next") can be made in editing rather than asking a video model to materialise it.

### W5. The vessel and THE ANIMAL (prop sheet, the hardest translucency case)

> "Tubes, and a small mount, and hanging in the mount a glass VESSEL of dark water about as long as her forearm. In the water: an ANIMAL. Almost clear, like a thing from the bottom of the sea. No longer than her hand."

Sheet views: vessel alone on grey with a forearm beside it for scale; the animal close through the glass, lit from behind by the tube loop so the light passes through it; the limb drawn out of a socket in the vessel wall; the vessel with the pump and the clipped container; state S4 at the bedside with the cloudy growth half filling the container. Transparent-background versions (GPT Image 2.5 [V, 10], or Qwen-Image-2.1 on a non-commercial project only [V, 32]) let the same vessel be composited into the open chest, onto Iona's suit, into the tray and onto the bedside table without redrawing it. Checks: dark water, not clear; animal clear, not white; size against the hand.

---

## 11. Open questions

1. The director must fix, before sheets are made: which sleeve Iona tears; which shoulder Jude is shot in; which side Eli's smile lifts; which foot keeps Eli's shoe; the floor number and word on the stencil.
2. The three logic conflicts in Section 7.4 (the carriage F, world screens, the copied name) need a ruling, logged in the index.
3. The ship's mirror state (NORMAL in Era B) is an inference from "Turned, like us"; the writer should confirm.
4. Delivery aspect ratio (16:9 or 2.39:1) must be set before any keyframe.
5. Commercial or personal project? It decides whether Qwen-Image-2.1, Ideogram 4.0 weights, and some canvas tiers are usable.
6. Not verified: LTX Studio (storyboard app) and Figma Weave API access; Higgsfield and Artlist plan prices; Midjourney plan prices from Midjourney itself (its documentation blocked automated reading); GPT Image 2.5 per-image prices *direct from OpenAI* (only token rates are published; the per-image figures here are Runway's resale prices); how many reference images the Gemini app and ChatGPT accept per message; Flora's price; Reve API shutdown (one secondary source only); the ShotDeck and Figma Weave plan pages (both refused automated reading on 2026-09-27).
7. Watch: FLUX 3 Image, a rumored Nano Banana successor, Gemini 4, Midjourney's Edit Model leaving alpha, and MAI-Image-2.6's promised multi-reference features. Re-check Section 3 monthly.

---

## 12. Sources

All checked 2026-09-27. "(search)" means the fact was read from the search engine's summary of that page because the page itself blocked automated reading; treat those as [V-sec].

1. Google, Gemini API pricing: https://ai.google.dev/gemini-api/docs/pricing
2. Google, Gemini API image generation guide: https://ai.google.dev/gemini-api/docs/image-generation
3. Google, Gemini API release notes: https://ai.google.dev/gemini-api/docs/changelog
4. Google, "Nano Banana 2" (Feb 26, 2026): https://blog.google/innovation-and-ai/technology/ai/nano-banana-2/
5. Google, Nano Banana Pro prompting tips (Nov 20, 2025): https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/
6. Google Cloud, "Ultimate prompting guide for Nano Banana" (Mar 6, 2026): https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana
7. Google, "Google Pics" (Sep 1, 2026): https://blog.google/products-and-platforms/products/workspace/google-pics/
8. The Decoder, Google AI subscription tiers after I/O 2026: https://the-decoder.com/google-overhauls-its-ai-subscriptions-at-i-o-2026-with-three-tiers-starting-at-10-a-month/ ; ChatGPT plan prices (search): https://chatgpt.com/plans/plus/
9. OpenAI, API pricing: https://developers.openai.com/api/docs/pricing
10. OpenAI, image generation guide: https://developers.openai.com/api/docs/guides/image-generation
11. OpenAI Developer Community, "Introducing GPT Images 2.5": https://community.openai.com/t/introducing-chatgpt-images-2-5/1395897
12. Unite.AI, "OpenAI Releases ChatGPT Images 2.5 With Sketch and Two New API Models": https://www.unite.ai/openai-releases-chatgpt-images-2-5-with-sketch-and-two-new-api-models/ (OpenAI's own post https://openai.com/index/introducing-chatgpt-images-2-5/ blocked reading)
13. Wikipedia, "GPT Image": https://en.wikipedia.org/wiki/GPT_Image
14. CostGoat, OpenAI image pricing calculator (updated Sep 5, 2026): https://costgoat.com/pricing/openai-images
15. The Decoder, two-stage Sora shutdown (search): https://the-decoder.com/openai-sets-two-stage-sora-shutdown-with-app-closing-april-2026-and-api-following-in-september/ ; OpenAI Help Center (search): https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation
16. Midjourney, "Edit Model for V8" (Aug 27, 2026): https://updates.midjourney.com/edit-model-for-v8/
17. Midjourney, updates index (latest Sep 24, 2026): https://updates.midjourney.com/ ; "Edit updates, thumbnail previews, and more" (Sep 24, 2026): https://updates.midjourney.com/edit-updates-thumbnail-previews-and-more/
18. Blake Crosley, Midjourney 8.2 guide (updated Sep 22, 2026): https://blakecrosley.com/guides/midjourney
19. Wikipedia, "Midjourney": https://en.wikipedia.org/wiki/Midjourney
20. Wireflow, "Best Midjourney API Tools in 2026 (No Official API Yet)" (search): https://www.wireflow.ai/blog/best-midjourney-api-tools-in-2026
21. Black Forest Labs, "FLUX.2" (Nov 25, 2025): https://bfl.ai/blog/flux-2
22. Black Forest Labs, pricing documentation: https://docs.bfl.ml/quick_start/pricing
23. Black Forest Labs, "FLUX 3": https://bfl.ai/blog/flux-3
24. OrcaRouter, "GPT-Image-2.5 vs Flux 3" (search): https://www.orcarouter.ai/blog/gpt-image-2-5-vs-flux-3
25. Black Forest Labs, FLUX.2 [klein] training documentation: https://docs.bfl.ml/flux_2/flux2_klein_training
26. Hugging Face and Black Forest Labs, "Fine-tune FLUX.2 [klein] with a LoRA" (Jun 4, 2026): https://huggingface.co/blog/black-forest-labs/flux-2-klein-lora
27. BytePlus, "Seedream 4.5": https://www.byteplus.com/en/blog/seedream4-5
28. fal, Seedream 5.0 Pro edit endpoint: https://fal.ai/models/bytedance/seedream/v5/pro/edit
29. fal, "How to use Seedream 5.0 Pro": https://fal.ai/learn/tools/how-to-use-seedream-5-0-pro-v2
30. ByteDance Seed, Seedream 5.0 Lite: https://seed.bytedance.com/en/seedream5_0_lite
31. TechNode, Qwen-Image-2.1 open-sourced (Sep 21, 2026): https://technode.com/2026/09/21/alibabas-qwen-open-sources-qwen-image-2-1-for-unified-image-generation-and-editing/
32. Hugging Face, Qwen/Qwen-Image-2.1 model card: https://huggingface.co/Qwen/Qwen-Image-2.1
33. Unite.AI, "Alibaba Launches Qwen-Image-3.0 Without Benchmarks or Weights" (search): https://www.unite.ai/alibaba-launches-qwen-image-3-0-without-benchmarks-or-weights/ ; Alibaba Cloud model page (search): https://www.alibabacloud.com/help/en/model-studio/qwen-image-3-0-pro
34. Ideogram, "Ideogram 4.0 Technical Details" (Jun 3, 2026): https://ideogram.ai/blog/ideogram-4.0/
35. Ideogram, available models documentation: https://docs.ideogram.ai/using-ideogram/generation-settings/available-models
36. Puter, Ideogram API pricing (search): https://developer.puter.com/tutorials/ideogram-api-pricing/
37. Recraft, "Recraft V4.1" (May 14, 2026): https://www.recraft.ai/blog/recraft-v4-1-more-beautiful-by-nature
38. Reve blog index: https://blog.reve.com/
39. Reve, "A New Chapter for Reve" (Jul 27, 2026): https://blog.reve.com/posts/a-new-chapter-for-reve/
40. The Rundown, Reve API status: https://www.therundown.ai/tools/reve-api
41. Adobe, Firefly custom models and Image Model 5 (Mar 19, 2026): https://blog.adobe.com/en/publish/2026/03/19/adobe-firefly-expands-video-image-creation-with-new-ai-capabilities-custom-models
42. Microsoft AI, MAI-Image-2.6 (search): https://microsoft.ai/news/mai-image-2-6-launches-at-no-2-on-arena-ahead-of-google-meta-and-xai/
43. Arena, text-to-image leaderboard (updated Sep 24, 2026): https://arena.ai/leaderboard/text-to-image
44. Arena, image-edit leaderboard (updated Sep 21, 2026): https://arena.ai/leaderboard/image-edit
45. Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models": https://arxiv.org/abs/2106.09685
46. Zhang et al., "Adding Conditional Control to Text-to-Image Diffusion Models" (ControlNet): https://arxiv.org/abs/2302.05543
47. Ye et al., "IP-Adapter": https://arxiv.org/abs/2308.06721
48. Wang et al., "InstantID": https://arxiv.org/abs/2401.07519
49. Guo et al., "PuLID": https://arxiv.org/abs/2404.16022
50. Civitai, on-site LoRA trainer guide (updated Apr 1, 2026): https://education.civitai.com/using-civitai-the-on-site-lora-trainer/
51. fal, FLUX.2 trainer: https://fal.ai/models/fal-ai/flux-2-trainer
52. fal, "Connect your AI to 1,000+ models with the fal MCP Server" (Mar 19, 2026): https://blog.fal.ai/connect-your-ai-to-1-000-models-with-the-fal-mcp-server
53. Replicate, MCP server documentation (search): https://replicate.com/docs/reference/mcp
54. ComfyUI Wiki, "Comfy MCP" (Jun 30, 2026): https://comfyui-wiki.com/en/news/2026-06-30-comfy-mcp-agent-integration
55. Comfy Org documentation, "Comfy MCP: Connect AI Agents to ComfyUI" (public beta): https://docs.comfy.org/agent-tools/mcp
56. Comfy Cloud pricing: https://comfy.org/pricing/
57. GitHub, artokun/comfyui-mcp (archiving Oct 9, 2026): https://github.com/artokun/comfyui-mcp
58. Boords, AI storyboard generator: https://boords.com/ai-storyboard-generator
59. Boords, pricing: https://boords.com/pricing
60. StudioBinder, storyboard creator: https://www.studiobinder.com/storyboard-creator/
61. GitHub, wonderunit/storyboarder releases: https://github.com/wonderunit/storyboarder/releases
62. LTX, "LTX Storyboard Generator Update": https://ltx.io/blog/ltx-storyboard-generator-update
63. The Rundown, LTX Studio pricing (Aug 28, 2026): https://www.therundown.ai/tools/ltx-studio
64. Katalist, AI storyboard generator: https://www.katalist.ai/ai-storyboard-generator
65. Krea API pricing (search): https://www.krea.ai/app/api/pricing ; Krea Agents report (search): https://aitoolsreview.co.uk/insights/krea-agents-creative-orchestration
66. Wireflow, "Freepik Spaces Is Now Magnific" (Jul 14, 2026): https://www.wireflow.ai/blog/freepik-spaces-is-now-magnific ; PR Newswire (search): https://www.prnewswire.com/news-releases/freepik-becomes-magnific-hits-230m-arr-and-introduces-the-no-collar-creative-economy-302755376.html
67. Flora: https://flora.ai/ ; pricing (search): https://www.therundown.ai/tools/flora-ai
68. Figma Weave: https://weave.figma.com/ ; plans (search): https://help.weavy.ai/en/articles/12267070-figma-weave-s-subscription-plans ; Figma acquisition (search): https://diginomica.com/config-2026-weave-layer-precision-design-workflows-figma
69. Higgsfield, storyboard generator (Popcorn) and Soul ID: https://higgsfield.ai/storyboard-generator ; https://higgsfield.ai/blog/sould-id-best-character-consistency
70. Artlist, 2026 launch (Jan 25, 2026): https://artlist.io/blog/artlist-nyc-ai-video-production-launch/
71. Intangible: https://www.intangible.ai/answers/ai-storyboarding-previsualization
72. ShotDeck pricing (search): https://shotdeck.com/welcome/pricing ; Flim (search): https://flim.ai/shotdeck-alternative
73. Kling, start and end frames guide: https://kling.ai/quickstart/ai-video-start-end-frames
74. APIYI, Nano Banana Pro storyboard consistency practices (practitioner guide): https://help.apiyi.com/en/nano-banana-pro-ai-video-storyboard-character-consistency-guide-en.html
75. Whisk-to-Flow migration guide (search, unofficial): https://whiskaitemplate.com/blog/whisk-ai-google-flow-migration-guide-2026
76. Hugging Face, Tongyi-MAI/Z-Image-Turbo (search): https://huggingface.co/Tongyi-MAI/Z-Image-Turbo
77. Pixune, types of storyboards (search): https://pixune.com/blog/types-of-storyboards/
78. Unite.AI, AI pre-production tools, Aug 2026 (search): https://www.unite.ai/best-ai-pre-production-tools-for-filmmakers/
79. Runflow, ComfyUI consistent characters with FLUX, 2026 guide (search): https://www.runflow.io/blog/comfyui-consistent-characters-flux
80. Atlas Cloud, Seedream v4.5 Sequential (search): https://www.atlascloud.ai/models/bytedance/seedream-v4.5/sequential
81. Qwen, Qwen-Image-Edit (search): https://qwen.ai/blog?id=qwen-image-edit
82. 9to5Google, Gemini 4 timing (Sep 24, 2026; search): https://9to5google.com/2026/09/24/google-says-gemini-4-release-is-coming-as-soon-as-possible/
83. BananaBanana, "Nano Banana 2.5" rumors (search; rumor site): https://bananabanana.pro/nano-banana-2-5
84. Build Fast with AI, Seedream 5.0 family dates (search): https://www.buildfastwithai.com/blogs/seedream-5-0-pro-review-bytedance-multimodal-image-model-2026
85. SaaSworthy, StudioBinder pricing (search): https://www.saasworthy.com/product/studiobinder/pricing
86. MindStudio, Recraft V4.1 and V4 Styles (search): https://www.mindstudio.ai/blog/what-is-recraft-v4-1-ai-image-model-design-assets
87. Build Fast with AI, Ideogram 4.0 license (search): https://www.buildfastwithai.com/blogs/ideogram-4-open-weight-image-model
88. fal, Nano Banana Pro edit page ($0.15 per image, 4K double, up to 14 inputs): https://fal.ai/models/fal-ai/nano-banana-pro/edit
89. xAI, Grok Imagine image generation guide (aspect ratios, `1k`/`2k`, quality): https://docs.x.ai/developers/model-capabilities/images/generation.md
90. xAI, "grok-imagine-image-quality Retirement on November 2, 2026" (up to five source images for editing): https://docs.x.ai/developers/migration/imagine-image-quality-nov-2.md ; multi-image editing: https://docs.x.ai/developers/model-capabilities/images/multi-image-editing.md
91. Runway API pricing (credits at $0.01; per-image prices for GPT Image 2.5, Nano Banana Pro, Seedream 5.0, Grok Imagine, muse-image, Gen-4 Image): https://docs.dev.runwayml.com/guides/pricing/
92. Hugging Face model pages and license files, checked through the Hugging Face API: FLUX.2 klein 4B (apache-2.0) https://huggingface.co/black-forest-labs/FLUX.2-klein-4B ; FLUX.2 klein 9B (flux-non-commercial-license) https://huggingface.co/black-forest-labs/FLUX.2-klein-9B ; FLUX.2 dev (FLUX Non-Commercial License v2.1, text read in full) https://huggingface.co/black-forest-labs/FLUX.2-dev/blob/main/LICENSE.md ; Z-Image and Z-Image-Turbo (apache-2.0) https://huggingface.co/Tongyi-MAI/Z-Image
93. Hugging Face, Qwen/Qwen-Image-Edit-2511 (apache-2.0, Dec 2025): https://huggingface.co/Qwen/Qwen-Image-Edit-2511 ; Qwen-Image-2.1 LICENSE (Qwen Research License): https://huggingface.co/Qwen/Qwen-Image-2.1/blob/main/LICENSE
94. GitHub, ideogram-oss/ideogram-4 (weights "Ideogram 4 Non-Commercial", code Apache-2.0): https://github.com/ideogram-oss/ideogram-4
95. xAI, API pricing (Imagine: `grok-imagine-image-2.0` $0.04 per image): https://docs.x.ai/developers/pricing.md
96. Runway API reference (Gen-4 Image: up to 3 tagged `referenceImages`; `seed` accepted by `gen4_image` and `gen4_image_turbo`): https://docs.dev.runwayml.com/api.md
97. Katalist, pricing: https://www.katalist.ai/katalist-pricing
