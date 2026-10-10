# C1 — AI video generation models: what exists and what each can do (as of 27 September 2026)

> **What this file is for**
> 1. It tells the pipeline which AI video model to use for each shot in a breakdown, and why.
> 2. It lists every significant model current on 27 Sept 2026, with checked limits, prices and controls.
> 3. It gives decision rules, recipes and failure fixes that a non-technical user can run through an LLM.
> 4. It explains how an LLM can call these models automatically (APIs, MCP connectors, aggregators).
> 5. It applies all of this to hard shots in *The Catch*. Re-check before use: this field changes monthly.

---

## 0. How to read this file

Claims carry one of three labels (a source number such as [S2] with no label also means the claim is verified from that source):

- **[V] Verified**: I found it on a primary source (the maker's own page, docs, model card or official changelog) or on two agreeing independent sources. The source number in square brackets, like [S2], points to the Sources list at the end. Every source was checked on **2026-09-27** unless the list says otherwise.
- **[U] Unverified**: I found it only on one secondary source, or sources disagree, or I could not find it at all.
- **[J] Judgment**: my own reasoning or recommendation. Treat it as advice, not fact.

**Staleness rule [J]:** if you are reading this more than 30 days after 2026-09-27, ask the LLM to re-check the landscape table (Section 3) and the prices before spending money. In the twelve months before this file was written, OpenAI launched and then shut down its Sora 2 video platform, Google shut down two Veo versions, and at least six new top-ranked models appeared.

---

## 1. Plain-English terms used in this file

Each term below is used with this one meaning throughout. Where makers use different names for the same thing, the maker's name is given once and then this file's word is used.

| Term | Meaning in one plain sentence |
|---|---|
| **Model** | The AI system that makes the video (for example Veo 3.1 or Kling 3.0). |
| **Platform** | A website or app where you use one or more models (for example Google Flow or Runway). |
| **Aggregator** | A platform that gives you many different makers' models behind one account and one bill. |
| **Shot** | One continuous camera view in the finished film, from one cut to the next. |
| **Clip** | One video file that a model returns from one request. |
| **Take** | One clip made for a specific shot; you usually make several takes and keep one. |
| **Retake ratio** | How many takes you make for every take you keep. |
| **Text-to-video** | The model makes a clip from written words alone. |
| **Image-to-video** | The model animates a still picture you give it, which becomes the first frame of the clip. |
| **Start frame / end frame** | A picture you supply that the clip must begin on / finish on; "start-and-end-frame control" means you supply both. |
| **Keyframe** | A picture you pin to a particular moment inside the clip (start and end frames are the simplest keyframes). |
| **Reference image** | A picture you give the model so a character, object, costume or place keeps looking the same; makers call these "ingredients" (Google), "elements" (Kling), "references" (Seedance, Runway, Wan), "Soul ID" (Higgsfield) or "characters". |
| **Reference pack** | Your own folder of reference images for one character, creature, prop or set, made once and reused for every shot. |
| **Native audio** | The model makes the sound (voices, effects, ambience, music) in the same run as the picture. |
| **Lip sync** | Mouth movements that match the spoken words. |
| **Multi-shot** | One request returns a clip containing several shots with cuts between them. |
| **Extend** | The model continues an existing clip from its last frame to make it longer. |
| **Video-to-video** | The model takes an existing clip and changes it (new look, new lighting, object removed) while keeping its motion. |
| **Control video** | A rough video (for example a grey 3D render from Blender) whose camera move, poses or depth the model copies while inventing the final look. |
| **Motion transfer** | Copying the movement of a person or camera from one clip onto a different character or scene. |
| **Previs** | A rough 3D version of shots, made in Blender or similar, used to plan and control camera and movement. |
| **Compositing** | Layering pictures or clips on top of each other in editing software (for example putting a generated screen clip onto a tablet). |
| **Plate** | A background clip made to have something else composited onto it. |
| **Open weights** | The model's files are published so you (or a rented computer) can run it yourself, often free of per-clip fees. |
| **API** | A web address that a program can send requests to, paying per use, with no app to click through. |
| **MCP connector** | A plug-in (Model Context Protocol server) that lets an LLM such as Claude call a tool directly from a chat. |
| **Credits** | A platform's prepaid in-app currency; each clip costs a number of credits. |
| **720p / 1080p / 4K** | Picture sizes: 1280×720, 1920×1080 and about 3840×2160 pixels. "Upscaled" means made at a smaller size and enlarged afterwards. |
| **Elo score** | A leaderboard score calculated from many blind "which clip is better?" votes by people; higher is better. |
| **GPU / VRAM** | A graphics card and its memory; open-weight models need a large one. |
| **LoRA** | A small add-on file that teaches an open-weight model a style, a character or a kind of control. |
| **ComfyUI** | A free app that runs open-weight models (and some paid ones) by connecting boxes on a canvas. |
| **Generated second** | One second of clip that a model makes; hosted models charge per generated second, whether or not you keep the take. |
| **Seed** | A number that fixes a model's randomness, so the same inputs and seed give a similar clip again (not every platform shows it). |
| **Render** | A picture or video output by 3D software such as Blender (a grey "clay" render shows shapes and movement only). |
| **fps** | Frames per second; film is usually 24. |
| **SDR / HDR / EXR** | Standard and high dynamic range (how wide a brightness range the picture holds), and EXR, a professional file type for visual-effects work. |
| **Parameters (B)** | A rough measure of a model's size, in billions ("22B"); bigger models need bigger GPUs. |
| **C2PA / SynthID** | Two kinds of built-in label that record a clip was made by AI: C2PA is a metadata standard attached to the file, SynthID is Google's invisible watermark in the picture. |
| **Prompt** | The written instructions you give a model. |
| **API key** | A long secret password that lets a program (or an LLM) spend money on your account; keep it private. |
| **Preview / GA** | "Preview" means an early, changeable release; "GA" (generally available) means the finished, supported release. |
| **Close-up / two-shot / insert** | A shot of one face; a shot framing two people; a short shot of a detail (a hand, a ring, a sign) cut into a scene. |
| **Coverage** | The set of shots filmed of one scene (wide, two-shot, close-ups, inserts) that the editor cuts between. |
| **Animatic** | A rough version of the whole film made from stills or cheap clips, to check timing before making finals. |
| **Macro** | Extreme close-up of something small. |
| **Aspect ratio** | The shape of the frame, width to height (16:9 is widescreen; 9:16 is phone-vertical). |

---

## 2. The situation in one page (27 September 2026)

**Verified facts [V]:**

1. **OpenAI's Sora is gone.** OpenAI announced the shutdown on 24 March 2026; the Sora app and website closed on 26 April 2026 [S9][S84], and the Sora 2 API models (`sora-2`, `sora-2-pro` and their dated snapshots) and the whole Videos API were removed on **24 September 2026**, three days before this file was written, with no replacement named [S8]. Any older guide recommending Sora 2 is out of date. Some platforms (for example Replicate's and Runway's older model lists) may still show it; expect those requests to fail.
2. **Google now has two video lines.** Veo 3.1 (with cheaper Fast and Lite versions; Lite added 31 March 2026) is the specialised video model [S1][S2]. **Gemini Omni Flash** is a new "any input to video" model announced at Google I/O in May 2026, released to the Gemini API as a preview on 30 June 2026, and generally available since **27 August 2026** as `gemini-omni-1.1-flash` [S1][S5]. Veo 2 and Veo 3.0 were shut down on 30 June 2026 (notice given 15 June) [S1]. No "Veo 4" (or "Veo 3.2") appears in Google's API changelog, Veo docs or Flow help as of this date [U: absence of evidence; S1][S2][S6].
3. **Blind-vote leaders (Artificial Analysis arena, checked 2026-09-27)** [S61][S62][S63]:
   - Text-to-video *with audio*: Gemini Omni Flash 1233, Wan 3.0 1229, MiniMax H3 Max (fal's post-trained version) 1227, MiniMax H3 1220, Seedance 2.0 1210.
   - Text-to-video *without audio*: Wan 3.0 1335, Gemini Omni Flash 1332, MiniMax H3 1302, HappyHorse 1.0 1286, HappyHorse 1.1 1272 (from the leaderboard FAQ; the silent table itself did not load).
   - Image-to-video: MiniMax H3 Max 1194, MiniMax H3 1181, Gemini Omni Flash 1178, Seedance 2.0 1176, HiDream-O1-Video 1174, Wan 3.0 1164.
   - Video editing: Wan 3.0 1188, MiniMax H3 1132, Gemini Omni Flash 1125, HappyHorse 1.0 1089; Runway Aleph 2.0 1012; Kling 3.0 Omni 1000.
   - Veo 3.1 (1088), Kling 3.0 Pro (1095) and Skywork's SkyReels V4 (1095) now sit mid-table on text-to-video with audio; LTX-2.5 scores 1055 [S61]. Seedance 2.5, Runway Gen-4.5, Luma Ray3.2 and FLUX 3 Video were not on the with-audio boards on this date.
   - Newer names on the boards that this file covers only briefly: **HiDream-O1-Video** (HiDream, Aug 2026, image-to-video 1174, ≈$0.10/s) and **Agnes-Video-2.5** (Sapiens AI, Aug 2026, 1076, ≈$0.025/s, the cheapest listed) [S61][S62]. Treat both as "test before relying on".
4. **Single clips of 20–30 seconds now exist**: Seedance 2.5 and Wan 3.0 go to 30 s [S18][S33]; FLUX 3 Video and Luma Ray3.2 go to 20 s [S60][S28]. Most others stop at 8–16 s.
5. **Native audio is now normal.** Exceptions I found: Runway Gen-4.5 (no audio option in Runway's API pricing; not on the with-audio leaderboards) [S82][S61], Luma Ray3.2 (no audio documented; Luma offers ElevenLabs sound models alongside it) [S28][S29], Moonvalley Marey, and Midjourney's video model [S50][S46].
6. **Open weights moved forward**: MiniMax H3 (33-billion-parameter core, July 2026), Lightricks LTX-2.5 (22B, July–August 2026) and Sand.ai MAGI-2 preview (August 2026; 114B, needs eight data-centre GPUs) all have downloadable weights with audio [S32][S43][S64]. Skywork's **SkyReels V3** (January 2026) adds open reference-to-video, audio-driven talking-head and shot-extension models [S85][S86]. **Wan 3.0 is not open**: the official Wan-AI Hugging Face account's newest releases are still the Wan 2.2 family (latest: Wan-Animate-2, weights July–August 2026, and Wan-Dancer, July 2026) [S35][S36]. A third-party site claiming Wan 3.0 weights were released is contradicted by the official account.
7. **LLMs can now drive video models directly.** fal, Replicate, Runway, Higgsfield, Krea and OpenArt all offer MCP connectors, and Freepik's developer platform (now branded Magnific) advertises one [S58][S59][S26][S57][S88][S71][S89].

**Judgment [J]:** There is no single best model. The top five on the leaderboard are within about 25 Elo points of each other, which is small; the practical differences are in *controls* (start and end frames, reference images, audio input, clip length, editing) and *policies* (what they refuse). The pipeline should therefore choose a model per shot using Sections 5 and 6, and should route every request through an aggregator or MCP connector so that a model that disappears (as Sora did) can be swapped without rewriting the breakdown.

---

## 3. Landscape tables

### 3A. Hosted (closed) models: basics

Prices are list prices per *generated* second (you pay for every take, not just the one you keep). "Audio" means native audio.

| Model (maker) | Current version, date | Access | Price per generated second | Longest single clip; picture size | Audio and lip-synced dialogue |
|---|---|---|---|---|---|
| **Veo 3.1** (Google) | 3.1 15 Oct 2025; 3.1 Lite 31 Mar 2026 [S1][S87] | Gemini app, Flow, Gemini API, Vertex AI; many aggregators (fal, Replicate, Runway, Krea, Adobe Firefly) | Standard $0.40 (720p/1080p), $0.60 (4K); Fast $0.10 (720p), $0.12 (1080p), $0.30 (4K); Lite $0.05 (720p), $0.08 (1080p), no 4K. Audio included in all prices [S4] | 4, 6 or 8 s (1080p/4K, reference images and extension all force 8 s); extend (Standard/Fast only, not Lite) 7 s at a time to ≈148 s at 720p [S2] | Yes, always on; dialogue, effects, ambience; only English "fully supported" [S2] |
| **Gemini Omni Flash** (Google) | Announced May 2026; API preview 30 Jun 2026; 1.1 GA 27 Aug 2026 [S1][S5] | Gemini app, Flow, YouTube Shorts/Create, Gemini API; Runway, Higgsfield | ≈$0.10/s at 720p (billed as 5,792 output tokens per second at $17.50 per million) [S4]; 1080p/4K are upscales [S3][S7] | 3–10 s; extend (append only) to 40 s; 360p/720p native; 16:9 or 9:16 only [S3][S7] | Yes; voice references and voice editing not supported in the API [S3] |
| **Kling 3.0 / 3.0 Omni ("O3") / 3.0 Turbo** (Kuaishou) | 3.0 and Omni Feb 2026 (5 Feb per press release) [S10][S61]; Turbo and Omni upgrade 17 Jun 2026 [S14] | Kling app, Kling API, fal, Replicate, Runway (app since Jan 2026; MCP from 18 Sep 2026), Adobe Firefly, Higgsfield, Krea [S24][S52][S88] | fal: 3.0 Pro $0.112 silent, $0.168 with audio, $0.196 with voice control [S12]; O3 4K $0.42 [S13]; Turbo ≈$0.11 (720p)–0.14 (1080p) [S14] | 3–15 s; 720p/1080p, native 4K endpoints [S12][S13] | Yes; English, Chinese, Japanese, Korean, Spanish [S10][U: press release unreachable on 2026-09-27]; fal's O3 4K lists Chinese and English only [S13]; Omni binds a voice from a 5–30 s speech sample in Kling's app [S11], but on fal only a *video* element can carry a bound voice [S12] |
| **Seedance 2.0** (ByteDance) | Feb 2026; on fal 9 Apr 2026 [S17] | Dreamina/CapCut, BytePlus, fal, Replicate, Runway (Standard, Fast, Mini) [S25] | ≈$0.24–0.30 at 720p on fal, audio included [S16]; Runway $0.30 (720p), $0.20 (480p), Mini $0.16 [S25] | 4–15 s; 480p/720p (higher on some routes); 21:9 to 9:16 [S17] | Yes, included [S17] |
| **Seedance 2.5** (ByteDance) | Announced 23 Jun 2026 (enterprise beta) [S19]; public release 31 Jul 2026; API from 7 Aug 2026 [S18][S21] | Jimeng, Doubao, BytePlus, fal, Replicate, Runway, Krea, Higgsfield; Pika offers "Seedance" (version not stated) [S45] | $0.23 (Replicate/BytePlus launch rate) to $0.47 (fal) at 720p; $0.22 at 480p on fal; Runway 20–68 credits/s ($0.20–0.68) [S20][S22][S90][S82] | 4–30 s (or "auto"), 24 fps; 480p/720p native; 1080p on some routes (Runway since 18 Aug 2026) [S20][S21][S24][S90]. ByteDance's launch claim of native 4K 10-bit output is not offered by any API checked [S19][S21] | Yes, joint with picture; can be switched off on fal [S22][S90] |
| **Wan 3.0** (Alibaba) | Official blog 13 Aug 2026 (says generally available on Alibaba Model Studio) [S33]; on Runway 24–26 Aug 2026 [S24][S25] | Wan.video, Alibaba Model Studio, fal, Runway, Krea | $0.05 (480p), $0.10 (720p), $0.20 (1080p) [S33][S34] | 2–30 s; up to 1080p; 16:9, 4:3, 1:1, 3:4, 9:16 [S33][S34] | Yes; Alibaba says "audio texture … not yet where we want" [S33] |
| **MiniMax H3 (Hailuo 3.0)** (MiniMax) | 31 Jul 2026 [S31] | Hailuo app, MiniMax API, fal, Runway, Krea, Pika; OpenRouter [U]; also open weights | ≈$0.13/s at 2K (MiniMax list, from $7.80/min); fal's post-trained "H3 Max" ≈$0.04/s [S61]; Runway 10 credits/s (768p), 15 (2K) = $0.10/$0.15 [S25] | 4–15 s, 24 fps; API default 2K with a cheaper 768p option; open weights are 768p only (the 2K re-generator stays API-only) [S31][S32] | Yes, 32 kHz stereo; 11 languages "stable" [S32] |
| **HappyHorse 1.0 / 1.1** (Alibaba ATH unit) | 1.0 Apr 2026 [S38]; 1.1 23 Jun 2026 [S37] | Alibaba Model Studio, fal, invideo, Runway (1.0) [S83] | ≈$0.125 (720p), ≈$0.22 (1080p) [S37] | 3–15 s; up to 1080p; 24 fps [S37] | Yes; 7 languages (English, Mandarin, Cantonese, Japanese, Korean, German, French); 1.1 tuned for dialogue [S37] |
| **Runway Gen-4.5** (Runway) | Research release 1 Dec 2025; all paid plans 4 Dec 2025; API 10 Feb 2026 [S23][S24][S25] | Runway app, API, MCP; also Replicate, Adobe Firefly, Krea [S52][S88] | $0.12 (12 credits/s; 1 credit = $0.01) [S82] | 2–10 s per API request [S25] | **No native audio verified.** Runway's API charges one flat rate with no audio option (unlike its Veo 3.1 route), and Gen-4.5 is absent from the with-audio leaderboards [S82][S61]. An earlier draft of this file read a 29 Jun 2026 changelog entry as "Gen-4.5 audio"; that entry is **Seed Audio 1.0**, a separate sound model [S24]. Add sound with Runway's audio models (Seed Audio 1.0, ElevenLabs) or your own mix [S83] |
| **Luma Ray3.2** (Luma AI) | 9 Jun 2026 [S28] | Luma app/Agents, API, Adobe Firefly (Ray3.14) [U] | ≈$0.24 at 1080p SDR; HDR ×2; HDR+EXR ×3 [S30][U] | Up to 20 s at 1080p; native HDR, 16-bit EXR [S28] | Not documented (treat as no); Luma offers ElevenLabs sound models in the same app [S28][S29] |
| **Grok Imagine Video 1.5** (xAI, now "SpaceXAI" [S76][S61]) | Preview late May 2026; GA June 2026 (Vercel lists 22 Jun) [S48][S61] | Grok app, xAI API, Vercel AI Gateway, fal, Runway (from 7–11 Aug 2026) [S24][S25] | xAI list price from $0.08/s [S81]; Runway $0.10 (480p), $0.16 (720p), $0.29 (1080p) [S25] | 1–15 s; 480p/720p/1080p [S25][S47][S48] | Yes: effects, ambience, speech [S48] |
| **FLUX 3 Video** (Black Forest Labs) | GA 4 Aug 2026 [S60] | BFL API and partners (fal, Krea, OpenArt) [S60][S88][S71] | Not disclosed [S60] | Up to 20 s; 720p/1080p [S60] | Yes, lip sync in many languages (English, Chinese, Spanish, French, German, Japanese, Hindi and more) [S60] |
| **Vidu Q3** (ShengShu) | Jan 2026 [S61]; Reference-to-Video 13 Apr 2026 [S54] | Vidu app, Vidu API, Alibaba Model Studio, fal [S54] | ≈$0.154 at 1080p on fal [S55][U]; leaderboard list $0.12/s [S61] | Up to 16 s with audio [S54]; 1080p [U] | Yes: ambience, motion sound, foley, emotional cues [S54] |
| **PixVerse V6** (PixVerse) | 30 Mar 2026 [S56] | PixVerse app, API, and a command-line tool usable by coding agents (Claude Code, Codex, Cursor) [S56] | ≈$0.115 (from leaderboard $6.90/min) [S61][U] | 1–15 s [U: duration from secondary]; up to 1080p [S56] | Yes [S56] |
| **Marey Realism v1.5** (Moonvalley) | 8 Jul 2025; no 2026 successor found [S92] | Moonvalley app, fal, Adobe Firefly [U: Firefly] | $0.30 ($1.50 per 5 s on fal) [S50] | 5 or 10 s; 1080p [S50] | No |
| **Midjourney Video V1** (Midjourney) | 18 Jun 2025; no V2 video found (Midjourney's September 2026 changelogs cover image model V8.x and the editor) [S46][U] | Midjourney website, subscription only | Subscription GPU time; a video job ≈ 8 image jobs [S46] | 5 s, extend 4 × ~4 s ≈ 21 s [S46] | No |
| **Adobe Firefly Video** (Adobe) | Custom-model training ("Firefly Foundry") [S52]; Creative Agent Apr 2026 [S53] | Firefly app, Premiere; hosts partner models including Kling 3.0 and 3.0 Omni, Veo 3.1 and Runway Gen-4.5 [S52] | Credits / subscription [U] | Not verified | Not verified |
| **SkyReels V4** (Skywork AI) | Mar 2026 [S61] | Skywork API [U] | ≈$0.35 (leaderboard $21/min) [S61] | [U] | Yes (listed on the with-audio board, 1095) [S61] |
| **HiDream-O1-Video** (HiDream) | Aug 2026 [S62] | API [U]; no open weights found [S91] | ≈$0.10 (leaderboard $5.80/min) [S62] | [U] | Yes (with-audio image-to-video board, 1174, fifth place) [S62] |

### 3B. Hosted models: controls

"—" means not offered or not documented. "Camera" means how you direct the camera.

| Model | Image-to-video | Start-and-end frames | Reference images | Camera | Multi-shot | Video-to-video / edit / motion transfer | Extend |
|---|---|---|---|---|---|---|---|
| **Veo 3.1** | Yes | Yes, `lastFrame`, Standard and Fast only in the API (4, 6 or 8 s; 8 s if 1080p/4K); in Google Flow even Lite offers first-and-last frames [S2][S6] | Up to 3 "asset" images, one subject each; forces 8 s; not on Lite in the API (Flow: Lite and Fast yes, Quality no) [S2][S6] | Text only [S2] | No ("multi-video prompting" unsupported) [S2] | Not documented in API [S2] | +7 s × up to 20, Standard/Fast only, 720p [S2] |
| **Omni Flash** | Yes | Yes [S3] | Several images; up to 3 video clips of ≤3 s; no audio references [S3] | Text, including timecodes like "[0-3s] …" [S3] | Via timecoded beats [J] | Conversational edits of clips ≤10 s; style and motion transfer [S3][S5] | Append only, to 40 s [S3] |
| **Kling 3.0 / O3** | Yes | Yes [S12] | Up to 7 images, or 1 video (3–10 s) + 4 images; addressed as @Element1 etc. [S11][S13] | Text; Motion Control copies movement from a reference clip [S80] | Up to 6 shots, each with its own duration, size and camera [S10][U: "6"] | O3 edits 3–15 s clips up to 4K [S14] | [U] |
| **Seedance 2.0** | Yes | Yes (start and end frame on fal's image-to-video) [S17] | 9 images + 3 videos + 3 audio [S17] | Text; reference video [S16] | "Shot 1: … Shot 2: …" prompts; "multiple shots with natural cuts" [S16][S17] | Reference video | [U] |
| **Seedance 2.5** | Yes | Yes (optional `end_image_url` on fal's image-to-video) [S90] | Up to 30 images + 10 videos + 10 audio (50 in all); addressed as "[Image1]", "[Video1]", "[Audio1]" [S18][S22] | Grey "clay" 3D renders as reference for camera, pacing and blocking [S18] | Yes, "multiple logically connected shots" in one generation [S18] | Timestamp-level edits, camera-perspective edits, green-screen background replacement, reference-based edits [S18] | Multi-round [S18][S21] |
| **Wan 3.0** | Yes | Optional end frame [S34] | 10 images, 5 video clips (15 s total), 5 audio (15 s total), plus a document [S34][S33] | Text | [U] | Edits "visuals, plot, and dialogue" [S33] | Yes [S33] |
| **MiniMax H3** | Yes | Yes: first, last, or both (FL2VA mode) [S32] | ≤9 images, ≤3 videos, ≤3 audio, ≤12 files total [S32] | Copy a camera move from a reference video [S31] | Native [S31] | Video-to-video motion transfer [S31] | [U] |
| **HappyHorse 1.1** | Yes | [U] | Up to 5 [S37] | Text | [U] | Text-instruction editing [S37] | [U] |
| **Runway Gen-4.5** | Yes | Keyframes promised at launch ("all existing control modes") [S23]; not verified in the API [U] | Via Runway References / Characters [U] | Text | No native multi-shot verified; Runway's Agent can assemble clips into a multi-shot scene on a timeline (8 Jul 2026) [S24] | Aleph 2.0 for edits; Act-Two for performance capture [S24][S78][S83] | [U] |
| **Runway Aleph 2.0** (edit model) | — | Up to 5 keyframe images pinned at timestamps [S27] | — | Cannot invent angles or subjects not in the source clip [S27][U] | Propagates edits across ≤10 cuts [S27] | Relight, weather, remove objects, wardrobe, restyle; 2–30 s input [S25][S27]. Released in Runway's Edit Studio 13 May 2026, API 2 Jun 2026 [S24][S25] | — |
| **Luma Ray3.2** | Yes | Up to 16 keyframes [S28] | Face tracking up to 8 faces [S28] | Frame-level camera paths via keyframes [S28] | [U] | Modify, Reframe, performance transfer, 20 s at 1080p [S28][S29] | [U] |
| **Grok Imagine 1.5** | Yes (main mode) [S48]; xAI's docs also list text-to-video [S47] | [U] | Reference images [S47] | Text | — | API offers edit [S47] | Yes, from an existing clip [S47] |
| **FLUX 3 Video** | Yes | Start, end, and multiple keyframes [S60] | [U] | Several shots/angles in one clip [S60] | Yes [S60] | Continuation from ≤4 s of video + audio [S60] | Via continuation |
| **Vidu Q3** | Yes | [U] | Subjects, sets, costumes, props, styles [S54] | Camera control; listed as an effect type [S54] | Yes, "multi-shot composition" [S54] | [U] | [U] |
| **PixVerse V6** | Yes | [U] | [U] | Improved tracking and reveals [S56]; camera presets [U: count] | Yes [S56] | [U] | [U] |
| **Marey v1.5** | Yes | [U] | [U] | Camera control from a single image; drawn trajectory control [S92][S51] | — | Motion transfer, pose transfer [S92][S51] | — |
| **Midjourney V1** | Only | Start frame; end frame for loops [U] | — | "Low motion" / "high motion" only [S46] | — | — | ×4 [S46] |

### 3C. Open-weight models (run on your own or a rented GPU)

| Model | Released | Licence | What it does | Hardware |
|---|---|---|---|---|
| **LTX-2.5** (Lightricks) | Weights on Hugging Face 23 Jul 2026; announced 11 Aug 2026 [S43][S42] | LTX-2.x Community Licence: free commercial use under $10M annual revenue [S41] | Text/image/video/audio-to-video with audio; native multi-shot ("continuity is not guaranteed"); auto duration; 4K HDR (Fast API); 6–20 s [S41][S42]. Quality trade-off: 1055 on the with-audio leaderboard, about 175 points below the leaders [S61] | "16 GB minimum path" for running; 32–80 GB for training add-ons [S41] |
| LTX control add-ons | Jan–Sep 2026 [S43] | Same | **Which base model each add-on fits matters.** For LTX-2 (19B, Jan 2026): camera-move LoRAs (dolly in/out/left/right, jib up/down, static), depth, pose, edge ("canny"), union and motion-track control. For LTX-2.3 (22B, Mar 2026): union and motion-track control, plus relight, HDR, day-to-night, clean plate, in/outpaint, water simulation, "Ingredients" references. For LTX-2.5 (as of 15 Sep 2026): upscaler, day-to-night, water simulation, clean plate, deblur, colourisation, cinemagraph, "Ingredients" and a slow-motion control LoRA; **no LTX-2.5-specific union, depth, pose or camera-move LoRA was published** on Lightricks' Hugging Face account, although ComfyUI's LTX-2.5 example workflows show union control [S43][S42] | Same |
| **MiniMax H3** | 28 Jul 2026 [S32] | MiniMax H3 Community Licence; commercial users in the USA, EU, UK and South Korea must fill in an application form [S32] | Text/first-frame/last-frame/first-and-last-frame/reference-to-video with stereo audio at 768p; the 2K re-generator and the prompt pre-processor stay API-only [S32] | 33B transformer + 32B text encoder [S32]; the example deployment uses 4 GPUs [S32]; [J] needs data-centre GPUs |
| **Wan 2.2 family** (Alibaba) | Jul 2025 – Aug 2026 [S35] | Apache 2.0 [S35][S36] | text-to-video and image-to-video (14B), a combined text-and-image model (5B), speech-to-video (S2V), Animate-2 (character animation from a driving video, weights 14 Jul 2026, Diffusers 6 Aug 2026), Wan-Dancer (Jul 2026) [S35][S36]; Wan 2.1 VACE for control and editing [S35] | 5B runs on consumer cards [J] |
| **HunyuanVideo 1.5** (Tencent) | 20 Nov 2025 [S40] | Tencent licence [U] | 8.3B text-to-video and image-to-video, 480p–1080p, built-in super-resolution; no newer Tencent video weights found [S40] | 14 GB minimum with offloading (official); ~6 GB via Wan2GP [S40][U: Wan2GP] |
| **MAGI-2 preview** (Sand.ai) | Aug 2026; updated build "0912" on the leaderboard [S64][S61] | Apache 2.0 [S64] | Text/image-to-video with audio; one clip length only (10 s) at 1080p; #6 on text-to-video with audio (1156) [S64][S61] | 114B mixture-of-experts (6B active); eight NVIDIA Hopper (H100-class) GPUs; ≈307 GB download [S64]. Not a home-computer model |
| **SkyReels V3** (Skywork AI) | 19 Jan 2026 [S86] | "skywork-license" [S85][U: terms] | Reference-to-video from 1–4 images (14B, 5 s, 720p); audio-to-video talking heads from one portrait plus up to 200 s of speech (19B, 720p); video extension 5–30 s and shot switching (cut-in, cut-out, shot/reverse-shot, multi-angle, cut-away) (14B) [S85] | Under 24 GB with the low-VRAM option [S85] |

### 3D. Model notes: strengths, weaknesses, restrictions

- **Veo 3.1.** Strengths [J, consistent with leaderboard history]: strong prompt-following, convincing lip-synced English dialogue, 4K, and the longest extend chain (148 s) [S2]. Weaknesses [V]: 8-second cap; 1080p/4K and reference images only at 8 s; extensions only at 720p and only on Standard/Fast; in the API, Lite has no last frame, no reference images and no extension (Google Flow's Lite does offer first-and-last frames and ingredients, so features differ between Flow and the API) [S2][S6]; clips deleted from Google's servers after 2 days, so download immediately [S2]. Restrictions [V]: image-to-video, start-and-end frames and reference images only allow adult people, and in the EU, UK, Switzerland and Middle East/North Africa only adults are allowed at all [S2]. Google's policy bans content that incites violence but allows "artistic" exceptions; its automatic filters still block many injury words [S68][S67].
- **Gemini Omni Flash 1.1.** Strengths [V]: top of the audio leaderboard; conversational editing ("make the light colder", building on the last edit); takes image, video and audio inputs in one request [S3][S5][S61]. Weaknesses [V]: clips ≤10 s; native picture only 720p; only 16:9 or 9:16 frames; uploaded clips for editing must be ≤10 s; no voice references, no voice editing in the API; images of certain recognisable people restricted (Google's launch post steers users to avatars of themselves instead) [S3][S5][S7]. The preview model name `gemini-omni-flash-preview` is deprecated on 30 Sep 2026 [S1].
- **Kling 3.0 family.** Strengths [V]: real native 4K; multi-shot storyboard with per-shot camera and size; strongest reference system among mid-price models (7 references, or a reference video); voice binding for a consistent voice; Motion Control [S10][S11][S13][S80]. Kling claims accurate on-screen text [S10][U: press release unreachable at re-check]. Kling Motion Control (2.6 and 3.0) copies body movement *and* facial expression from a 2–5 s reference clip; face consistency is its most common failure [S80]. Weaknesses [J]: audio languages vary by endpoint (fal's O3 4K lists only Chinese and English with auto-translation [S13]). Restrictions [V/U]: bans violent content "that may cause injury or death" [S15]; secondary sources report realistic gunfire and blood prompts are commonly refused [U].
- **Seedance 2.0 / 2.5.** Strengths [V]: the richest reference system anywhere (2.5 takes 50 inputs including 3D "clay" renders for camera and blocking); 30-second single clips; timestamp-level edits and camera-perspective edits of an existing clip [S18]; start and end frames on fal [S17][S90]. Weaknesses [V]: ByteDance itself says "the physical plausibility of complex motions" and "interactions among multiple subjects" need improvement [S18]; native API output is only 480p/720p [S20]. Restrictions [V/U]: after cease-and-desist letters from Disney, Warner Bros. Discovery, Paramount and Netflix, ByteDance paused the global rollout in mid-March 2026 and added face-blocking and copyrighted-character filters plus C2PA labels [S19][S77]; the official BytePlus route is not available in the US, Canada, UK, Australia or New Zealand, but fal, Replicate and others serve those countries [S20].
- **Wan 3.0.** Strengths [V]: #1 without audio, #1 at editing, 30-second clips, cheap ($0.20/s at 1080p), can read one document or web link (≤100 MB, ≤50 pages; PDF, Word, text, Markdown and others) as input, for example a scene breakdown, in its "thinking" mode [S33][S34][S61][S63]. Weaknesses [V]: Alibaba says audio texture and on-screen text are still weak [S33].
- **MiniMax H3.** Strengths [V]: top image-to-video scores; 11 dialogue languages; true start/end frame mode; copies camera moves from a reference clip ("Reference the Hitchcock camera movement from Video 1"); open weights [S31][S32][S62]. Weaknesses [V]: open weights only 768p; MiniMax says visual detail "can still be improved" and multimodal understanding has "significant room to improve" [S31][S32].
- **HappyHorse 1.1.** Strengths [V]: built for dialogue with sound; 7 languages; 5 references [S37]. Closed weights only.
- **Runway Gen-4.5 / Aleph 2.0 / Act-Two.** Strengths [V]: an ecosystem more than a model: editing (Aleph 2.0), performance capture from a webcam video onto a character (Act-Two), SDR-to-HDR conversion ("Ruby", Aug 2026), frame-rate enhancement up to 5 minutes, Magnific upscalers, ElevenLabs and Seed Audio sound models, Runway directly inside Premiere Pro and After Effects (8 Sep 2026), an MCP connector, and third-party models inside the same credits [S24][S25][S26][S78][S83]. Weakness [V/J]: Gen-4.5 itself is silent as far as I could verify, so dialogue shots need another model or a separate lip-sync step [S82][S61]. Runway publishes its own known failure types: effects before causes, objects vanishing after being hidden, and actions that succeed too easily [S23]. Runway retired Gen-3 Alpha Turbo and the first Aleph (`gen4_aleph`) from its API on 30 Jul 2026 [S25].
- **Luma Ray3.2.** Strengths [V]: 16 keyframes per clip (the finest timing control found), facial-performance transfer for up to 8 faces, and cinema-grade HDR/EXR files [S28]. Weakness [V]: no native audio documented.
- **Grok Imagine 1.5.** Strengths [V]: cheap (from $0.08/s at xAI), audio included, edit and extend in the same API [S81][S47][S48]. Restrictions [U]: blocks graphic violence and real people without consent [S75].
- **SkyReels (Skywork).** V4 is a hosted model scoring level with Kling 3.0 Pro (1095) but it is expensive (≈$0.35/s) and weak at editing (953) [S61][S63]. The open V3 family is useful for this pipeline in two narrow jobs: a talking head driven by your own recorded line (A2V) and shot/reverse-shot or cut-away continuations of an existing clip (V2V) [S85]. [J] Test before relying on either.
- **LTX-2.5.** Strength [V]: the most complete *open* package (audio, multi-shot, 4K HDR on the Fast API, many control and repair add-ons) under a licence free for small companies [S41][S42][S43]. Weakness [V]: picture quality sits well below the hosted leaders (1055 versus ≈1230) [S61]; several control add-ons exist only for older LTX versions (see 3C).
- **FLUX 3 Video.** Strengths [V]: 20 s, multiple keyframes, continuation from existing video and audio, lip sync in many languages [S60]. It is new (August 2026) and not yet on the leaderboards I checked [J: test before relying on it].
- **Marey.** Strength [V]: trained only on licensed footage, which matters if you need a legally "clean" film; motion and pose transfer [S50][S51]. Weakness: 10-second cap, no audio.
- **Midjourney Video V1.** Strength [J]: animates Midjourney's painterly stills well. Weaknesses: image-to-video only and no audio [V][S46]; no public API found [U].

### 3E. Superseded or discontinued: do not plan around these

| Old name | Status [V unless marked] | Use instead |
|---|---|---|
| Sora 2, Sora 2 Pro (OpenAI) | App closed 26 Apr 2026 [S84]; API (and the whole Videos API) removed 24 Sep 2026 [S8] | Veo 3.1, Omni Flash, Kling 3.0 |
| Veo 2, Veo 3.0 | Shut down 30 Jun 2026 [S1] | Veo 3.1 / Fast / Lite |
| `gemini-omni-flash-preview` | Deprecated 30 Sep 2026 [S1] | `gemini-omni-1.1-flash` |
| Kling 2.x, Kling O1 | Merged into Kling 3.0 (Feb 2026) [S10]; Kling V1.5–2.1 retired 15 Sep 2026 in ComfyUI [U] | Kling 3.0 / O3 / Turbo |
| Runway Gen-4, Gen-4 Turbo, Aleph (1), Gen-3 Alpha Turbo | Aleph (1) (`gen4_aleph`) and Gen-3 Alpha Turbo removed from Runway's API on 30 Jul 2026; Gen-4 Turbo still in the API but superseded [S25][S83] | Gen-4.5, Aleph 2.0 |
| Luma Ray3, Ray3.14; "Dream Machine" brand | Superseded by Ray3.2 [S29] | Ray3.2 |
| MiniMax Hailuo 02, 2.3 | Superseded by H3 (= Hailuo 3.0) [S31] | H3 |
| Seedance 1.x | Superseded by 2.0 and 2.5 [S18] | Seedance 2.5 (or 2.0 for price) |
| Wan 2.5, 2.6, 2.7 (API) | Superseded by Wan 3.0 [S33]; Wan 2.7 (Apr 2026) offered 2–15 s, start and end frames, 5 references and editing [S39]; open line stops at 2.2 [S35] | Wan 3.0 (API), Wan 2.2 (open) |
| LTX-2, LTX-2.3; old `ltx-2-fast/pro` API | API endpoints removed 16 Aug 2026 [S41]; the open weights stay downloadable and still carry control add-ons that 2.5 lacks (see 3C) [S43] | LTX-2.5 (keep LTX-2.3 weights for union/motion-track control) |
| Pika 2.x as a stand-alone model | Pika relaunched on 17 Sep 2026 as a multi-model platform (Pika's own models plus Seedance, MiniMax H3, GPT Image "and others"; it can pick the model for you) [S45] | Treat Pika as an aggregator |
| Vidu Q2, PixVerse V5.x, Grok Imagine Video (1.0) | Superseded by Vidu Q3, PixVerse V6, Grok Imagine 1.5 [S54][S56][S48] | Newer versions |

---

## 4. Content restrictions that matter for drama

*The Catch* has gunshots, a gunshot wound, floating blood, a woman striking a creature with a cylinder, and fire. Every hosted model runs automatic filters on your words, your uploaded images, and often the finished frames.

| Topic | What is verified | Practical rule [J] |
|---|---|---|
| **Violence and injury** | Google's policy bans "violence or the incitement of violence" but says Google "may make exceptions … based on educational, documentary, scientific, or artistic considerations" [S68]. Kling bans "inciting, promoting, or glorifying violence" and "violent content that may cause injury or death" [S15]. A tester found Runway refused a stylised anime sword duel as "graphic violence" (Aug 2026), noted that Google's artistic exception is not applied by its automatic filters, and found that implied, choreographed and off-screen violence passed; the classifier appeared to react to the combination "weapon + fast motion + contact" [S67]. | Show cause and effect in separate shots: the flash and the reaction, not the wound entering. Describe the *visible picture* ("he sits down heavily; a dark stain spreads on his shoulder") rather than injury words. Put gunshots in the sound mix, not the model prompt. |
| **Blood** | Secondary sources list "blood splatter" as a Kling-blocked term [U]. | Generate blood as a separate element (Blender or compositing) or describe it by look ("small dark-red spheres"), and keep it small and non-gory. Do not try to trick filters; if a shot is refused twice, move the element to compositing. |
| **Guns** | Kling's rules name firearms in a sales context [S15]; refusals of "realistic weapons fire" are reported [U]. | Keep weapons partial and out of focus; use sound for shots. |
| **Real people** | Omni Flash blocks recognisable people [S3]; Seedance blocks real-face uploads [S19][S77]; Veo limits person generation by region [S2]. | Design original faces with an image model; never use actors' or celebrities' photos as references. |
| **Children** | Omni Flash: no uploads of minors in the EEA, UK, Switzerland [S3]; Veo reference/frame modes allow adults only [S2]. | *The Catch* has no children; if your story does, expect heavy limits. |
| **Watermarks** | Google marks every clip with invisible SynthID [S2][S5]; Seedance 2.x adds C2PA labels [S19]. | Do not try to remove them; disclose AI use. |

**Per-model summary for drama (what a refusal is most likely to hit) [J unless cited]:**

| Model | Violence / blood / guns | Real people | Practical note for *The Catch* |
|---|---|---|---|
| Veo 3.1, Omni Flash | Automatic filters; artistic exception in policy but not reliably applied [S67][S68] | Region limits on people; Omni restricts recognisable people [S2][S3] | Keep the wound and the shooter out of frame; gunshots in the mix. |
| Kling 3.0 / O3 | Policy bans violent content that may cause injury or death [S15]; third-party reports of blocked blood and gunfire terms [U] | Bans defamation and harassment of others [S15] | Use Kling for the Figure and faces, not for the shot through the roof. |
| Seedance 2.x | [U] | Face-blocking and copyrighted-character filters since March 2026 [S19] | Do not upload photos of real actors as references; use designed faces. |
| Runway (all models it hosts) | Refused a stylised sword duel [S67] | [U] | Expect the strictest filter on weapon-plus-contact shots. |
| Grok Imagine 1.5 | Graphic violence blocked [S75][U] | Real people only with consent [S75][U] | — |
| Open weights (LTX, Wan 2.2, H3, SkyReels, HunyuanVideo) | No hosted filter when run yourself; the licence terms still apply [S41][S32][J] | Same | The fallback for a shot every hosted model refuses; keep it non-graphic anyway. |

---

## 5. Which model for which shot (decision table)

"First choice" is my recommendation [J] built on the verified capabilities in Section 3. "Draft with" is a cheap model for trying ideas before paying for the final take. Prices are from Section 3A.

| Shot need | First choice | Backup | Draft with | Why [J] |
|---|---|---|---|---|
| **Two-person dialogue close-up, synced English speech, same voices all film** | Kling 3.0 Omni with voice binding (in Kling's app: a 5–30 s speech sample; on fal: only a *video* element of the character can carry the voice), or MiniMax H3 / Seedance 2.5 fed your own voice recording as an audio reference | Veo 3.1 or HappyHorse 1.1 (dialogue-tuned) — good generated speech, but you cannot feed either a voice, so voices drift; open-weight fallback: SkyReels V3 talking-head (A2V) from a still plus your audio | Omni Flash 360p, Kling 3.0 Turbo | Voices made fresh in every clip drift; models that accept a voice sample or audio track keep voices consistent across 100+ clips [S11][S12][S32][S22][S37][S85]. Do not use Runway Gen-4.5 for speaking shots (no native audio verified) [S82]. |
| **Dialogue where the performance matters most** | Act it yourself on a phone, then Runway Act-Two, Kling Motion Control or Luma Ray3.2 performance transfer onto the character | Wan-Animate-2 (open) | — | Transferring a real performance gives you timing and emotion that text cannot specify [S78][S80][S28][S36]. |
| **Wide establishing shot, no dialogue** | Veo 3.1 at 4K, or Kling 3.0 native 4K | Wan 3.0 1080p | Veo 3.1 Lite | Big, stable, detailed pictures; audio is only ambience. |
| **Exact start and end picture** (e.g. the cage stopping level with the sill) | MiniMax H3 (first-and-last mode) or Kling 3.0 | Veo 3.1 / Fast (4–8 s), Seedance 2.0 / 2.5, Wan 3.0 (optional end frame), Omni Flash, FLUX 3 | Omni Flash 360p; Veo 3.1 Lite *in Flow only* | All verified to take both frames; in the API, Veo 3.1 Lite does not [S32][S12][S2][S17][S90][S34][S3][S60][S6]. |
| **Several timed beats inside one clip** | Luma Ray3.2 (16 keyframes) | FLUX 3 Video (multiple keyframes) | — | Only these two generation models document more than two pinned pictures; Aleph 2.0 takes up to 5, but only when editing an existing clip [S28][S60][S27]. |
| **Exact camera movement** | Blender previs as a control video → Seedance 2.5 with clay-render reference, H3 copying the move, or open LTX with union (depth/pose/edge) control (LTX-2.3's published union LoRA; LTX-2.5 only via ComfyUI's example workflow) | Luma Ray3.2 Modify; Marey trajectory control; Kling Motion Control; Higgsfield or PixVerse camera presets | — | Words describe camera moves loosely; a control video fixes speed, path and framing [S43][S42][S18][S31][S28][S51][S80]. |
| **The tall black creature (same design in every shot)** | Kling O3 with a 4–7-image reference pack | Seedance 2.5 (up to 30 images), Wan 3.0 (10) | Kling 3.0 Turbo | Most references and per-reference addressing (@Element1) [S11][S13]. |
| **Zero gravity, floating objects** | Blender simulation → control video (Seedance 2.5 clay reference, LTX-2.3 union control, or Wan 2.1 VACE), or plate + composited floating elements | Seedance 2.5 / Omni Flash with start and end frames | Omni Flash 360p | Models learned from Earth footage; objects "want" to fall. In a March 2026 study, 83% (third-person) to 94% (first-person) of clips from five late-2025 models had at least one physics glitch that ordinary viewers could spot [S65]. |
| **Long take, 15–30 s, one camera move** | Seedance 2.5 or Wan 3.0 (30 s) | FLUX 3 or Ray3.2 (20 s); Veo 3.1 extend | Wan 3.0 480p | Single-pass 30 s avoids the visible "seams" of extension [S18][S33]. |
| **Stylised or painterly sequence** | Midjourney stills → Midjourney video or Ray3.2 | Aleph 2.0 restyle of a live-action-look clip | — | Style is decided in the still; video models keep it. |
| **Change an existing clip** (relight, remove object, new weather) | Wan 3.0 edit or Omni Flash conversational edit | Aleph 2.0; Seedance 2.5 region edit; Kling O3 edit | — | Top editing scores [S63]; Aleph adds timed keyframes [S27]. |
| **Readable signs, labels, screen text** | Generate without text and add text in compositing | Kling 3.0 / H3 (claim good text) [S10][S31] | — | Text is still unreliable, and must be exact in this story. |
| **Screens (tablet, security-camera monitor)** | Generate the screen content as its own clip, then composite onto the screen | — | — | You control what is on screen, frame by frame. |
| **Fire, sparks, smoke** | Any top model; Vidu Q3 advertises particles and fluids [S54] | Kling 3.0 | Veo 3.1 Lite | Fire is well represented in training footage [J]. |
| **Licensed-data requirement** | Marey; Adobe Firefly Video | — | — | Marey is trained only on licensed footage [S50]. |
| **Free / private / offline** | LTX-2.5 (≥16 GB GPU) | Wan 2.2, HunyuanVideo 1.5 (≥14 GB), SkyReels V3 (<24 GB with low-VRAM mode) | — | Open weights, no per-clip fee [S41][S35][S40][S85]. MAGI-2 and H3 are open but need data-centre GPUs (rent them by the hour) [S64][S32]. |
| **Cheap animatic of the whole film** | Veo 3.1 Lite ($0.05/s) or Wan 3.0 480p ($0.05/s) | Omni Flash 360p; fal's H3 Max (≈$0.04/s); Agnes-Video-2.5 (≈$0.025/s, untested) | — | Lowest verified prices [S4][S33][S61]. |
| **Very wide "scope" frame (about 2.39:1)** | Seedance 2.x at 21:9 | Any model at 16:9, cropped top and bottom in the editor | — | Seedance lists 21:9 natively; Omni Flash allows only 16:9 or 9:16; Wan 3.0 tops out at 16:9 [S17][S90][S7][S34]. |
| **Silent picture you will score and sound-design yourself** | Kling 3.0 with audio off ($0.112 instead of $0.168 on fal), Runway Gen-4.5, Luma Ray3.2 | Seedance 2.5 with audio switched off | — | Kling charges a third less with audio off; with the others you mainly avoid unwanted music and voices (fal's Seedance 2.5 price is set by picture size, so switching audio off may not save money) [S12][S82][S90]. |

---

## 6. Decision rules

Each rule is written "If … then use … because …". Rules marked [J] are my judgment; the facts they rest on are cited.

1. **If** the shot has spoken lines **then** decide *voice first*: record or synthesise the line with a fixed voice before making the picture, and use a model that accepts an audio track or voice sample (Kling 3.0 Omni, MiniMax H3, Seedance 2.x, Wan 3.0, LTX-2.5; open: SkyReels V3 A2V, Wan 2.2 S2V) **because** voices generated fresh per clip will not match across a 20-minute film [J; audio inputs verified S11 S32 S22 S34 S41 S85 S35]. **If** you use Kling through fal **then** make a 3–8 s video clip of the character (not just stills) to carry the bound voice, **because** fal only binds voices to video elements [S12].
2. **If** two characters speak in the same clip **then** keep the second speaker silent or off-screen and cut to them for their line **because** models often move the wrong mouth when two faces are visible; ByteDance itself names multi-subject interaction as a weakness [S18][J].
3. **If** a shot must begin or end on an exact picture (to match the neighbouring shot) **then** make that picture first with an image model and use start-and-end-frame control (H3, Kling 3.0, Veo 3.1 or Fast, Seedance 2.x, Wan 3.0, Omni Flash, FLUX 3) **because** text alone never lands the same composition twice [J; capability S32 S12 S2 S17 S90 S34 S3 S60].
4. **If** a shot needs a precise camera path **then** build a quick Blender previs and feed it as a control video (Seedance 2.5 clay-render reference, H3 camera reference, Ray3.2 Modify, or open LTX union control) **because** text descriptions of camera moves are interpreted loosely [J; S42 S43 S18 S31 S28]. **If** you go the open LTX route **then** use LTX-2.3 with its published union-control LoRA unless your ComfyUI template already supports union control on LTX-2.5, **because** Lightricks had not published an LTX-2.5-specific union LoRA by 27 Sep 2026 [S43][S42].
5. **If** a character, creature or prop appears in more than one shot **then** build its reference pack once and use a model with reference images in every shot where it appears **because** text-only descriptions drift between clips [J].
6. **If** the shot contains readable text of any kind **then** generate the picture with the text area blank or blurred and add the text in compositing **because** generated text is unreliable (Alibaba still lists text as a weakness of its newest model) [S33][J].
7. **If** the text must read backwards (a mirror world) **then** generate the *whole shot the right way round* and flip it horizontally in the editor **because** a flip mirrors everything consistently, while models asked for backwards text produce gibberish [J].
8. **If** objects must float, fall wrongly or defy gravity **then** simulate them in Blender or add them in compositing over a model-made plate **because** 83–94% of clips from five late-2025 models (Sora 2, Veo 3.1 Fast, Kling 2.5, Hailuo 2.3, Wan 2.2) contained a physics glitch that ordinary viewers could spot, and models lean towards normal gravity [S65][J].
9. **If** a shot shows violence **then** split it into cause, reaction and aftermath shots, keep the impact off-screen, and put the gunshot in the sound mix **because** automatic filters block injury words and graphic frames even in artistic work [S67][S68].
10. **If** a model refuses the same shot twice **then** stop rewording, and move the refused element into compositing or sound **because** repeated refusals waste money and repeated attempts to get round filters can get an account flagged [J].
11. **If** the shot is longer than 15 s and is one continuous move **then** use Seedance 2.5 or Wan 3.0 (30 s) **because** extending a clip often shows a seam or a drift in faces and light at each join [S18][S33][J].
12. **If** the shot is a subtle performance (a look, a held breath) **then** act it on a phone and transfer the performance (Act-Two, Kling Motion Control, Ray3.2) **because** you control the timing of a look far better than a prompt can [S78][S80][S28].
13. **If** you are still exploring ideas **then** draft at 360p–480p on the cheapest model (Veo 3.1 Lite, Wan 3.0 480p, Omni Flash 360p) and re-make only the chosen version in the final model **because** most takes are thrown away [S66][J].
14. **If** the model must be swappable later **then** call it through an aggregator (fal, Replicate, Runway, Higgsfield) and store the model name as a field in the breakdown **because** models are retired with a few months' notice (Sora: 6 months; Veo 2/3.0) [S8][S1].
15. **If** you need 4K masters **then** generate native 4K only for wide, detailed shots (Kling O3 4K, Veo 3.1 4K) and upscale the rest **because** native 4K costs 1.5–4× more per second [S4][S13].
16. **If** a clip comes from Google's API **then** download it the same day **because** Google deletes generated videos after 2 days [S2].
17. **If** a shot needs only a small change to an existing good take **then** edit it (Wan 3.0, Omni Flash, Aleph 2.0) instead of regenerating **because** regenerating changes everything else too [J; S63].
18. **If** an LLM checks takes for you **then** still watch every kept take yourself **because** in a 2026 study Gemini 3.0 Pro missed over 74% of third-person and 90% of first-person clips with glitches that untrained viewers readily spotted, and the LLM critics often placed failures at the wrong moment and invented explanations [S65].
19. **If** a commercial release needs legally clean training data **then** prefer Marey or Adobe Firefly Video **because** Marey is trained only on licensed footage [S50].
20. **If** your country is the US, Canada, UK, Australia or New Zealand and you want Seedance **then** use fal, Replicate or Runway rather than the BytePlus route **because** BytePlus's official route is not offered there [S20].
21. **If** a recipe or older guide names Sora 2, Veo 2/3.0, Hailuo 02, Runway Gen-3 or the first Aleph **then** substitute the current model from Section 3E **because** those are retired or superseded [S8][S1][S31][S25].
22. **If** the chosen model has no native audio (Runway Gen-4.5, Luma Ray3.2, Marey, Midjourney) **then** use it only for silent shots or shots whose sound you build in the mix, and never for on-screen speech **because** adding lip sync afterwards is a separate, error-prone step [S82][S28][S50][S46][J].
23. **If** the film's frame is wider than 16:9 (for example 2.39:1) **then** decide the aspect ratio in the breakdown before generating anything, and either use Seedance 2.x at 21:9 or generate 16:9 with the important action kept inside the middle band and crop in the editor **because** most models output only 16:9 or 9:16, and Omni Flash allows nothing else [S17][S7][J].
24. **If** a platform shows a model price that differs from Section 3A **then** trust the platform's own price page on the day, and log it in the breakdown **because** the same model costs up to twice as much on different routes (Seedance 2.5 at 720p: $0.23 on Replicate, $0.47 on fal) [S20].
25. **If** a shot needs a model that your connected aggregator does not carry **then** ask the LLM to list the aggregator's models and pick the closest verified substitute from Section 5, rather than opening a new account for one shot **because** every new account adds a key, a bill and a learning curve [J].

---

## 7. Aggregators and automation: how an LLM can run the models

An **aggregator** gives you many makers' models behind one account. For this pipeline, the important question is whether an LLM can call it *without you clicking*.

| Platform | Models (examples) | Can an LLM drive it? | Cost model | Difficulty for a non-technical user [J] |
|---|---|---|---|---|
| **fal** | 1,000+ models incl. Kling 3.0/O3, Seedance 2.0/2.5, Wan 3.0, H3 Max, Veo 3.1, Marey, Vidu Q3, HappyHorse, LTX [S58][S12][S22][S34] | **Yes.** Official MCP at `https://mcp.fal.ai/mcp` with tools to search models, read each model's inputs, see price, run, queue long jobs and upload files [S58]. Also a plain API that an LLM can write scripts for. | Pay per use; top up a balance | Medium: you create an account, add a card and paste one API key once. |
| **Replicate** | Runway Gen-4.5, Veo 3.1 (all three), Kling 3.0 and Omni, Seedance 2.0 and 2.5, Vidu Q3, Wan, Luma, LTX and thousands of open models [S59][S20]. Its public "text-to-video" collection page still lists some older models (Hailuo 2.3, PixVerse 5.6), so ask the MCP what is live | **Yes.** Official remote MCP at `mcp.replicate.com` (you paste a Replicate API token once in a web sign-in step); works with Claude Desktop, Claude Code, Cursor, VS Code; experimental "code mode" lets the LLM write small programs against it [S59]. | Pay per use | Medium: API token needed. |
| **Runway** | Own: Gen-4.5, Aleph 2.0, Act-Two, Ruby (SDR→HDR). Others: Seedance 2.0 and 2.5, Veo 3.1, Wan 3.0, Hailuo 3.0 / H3 Max, Omni Flash, HappyHorse 1.0, Grok Imagine 1.5 (API and app), Kling 3.0/O3 (MCP, from 18 Sep 2026); sound: Seed Audio 1.0, ElevenLabs [S24][S25][S26][S83] | **Yes.** Official MCP connector, sign-in with your Runway account, no key; works in Claude, ChatGPT, Cursor and others; say "@Runway" in chat [S26]. Runway's own Agent can also build and run Workflows (22 Jul 2026) [S24]. | Runway credits ($0.01 per credit on the API) / subscription [S82] | Easy: add connector, sign in. |
| **Higgsfield** | 30+ models incl. Omni Flash, Seedance 2.5/2.0, Kling 3, plus "Cinema Studio" camera presets and "Soul ID" characters [S57] | **Yes.** Official MCP at `https://mcp.higgsfield.ai/mcp`, sign in with your Higgsfield account, no API key; shipped 30 Apr 2026 [S57][U: date] | Credits / subscription [U] | Easy. |
| **Google Flow / Gemini app** | Veo 3.1 (Quality/Fast/Lite), Omni Flash 1.1 (720p standard, 360p draft) [S6]. Flow's features differ from the API: Lite and Fast take first-and-last frames and ingredients (8 s), Quality takes no ingredients, only Omni does video-to-video editing, only Lite extends [S6] | No direct LLM control of Flow found [U]; the Gemini API (Veo/Omni) is scriptable. | Google AI subscription credits (Pro $19.99/mo ≈1,000 Flow credits; Omni 10 s ≈30 credits, from a May 2026 article) [S79][U]; Flow shows live credit costs before each generation [S6] | Easy by hand. |
| **Adobe Firefly** | Firefly Video + partner models, verified: Kling 3.0 and 3.0 Omni, Veo 3.1, Runway Gen-4.5 ("more than 30" models in all) [S52]; Ray3.14, Marey, Aleph [U] | Adobe's own Creative Agent (Apr 2026) orchestrates inside Adobe [S53]; outside-LLM control not verified | Creative Cloud credits | Easy by hand; good if you already edit in Premiere. |
| **Krea** | Seedance 2.5 and 2.0 Fast, Veo 3.1 (all three), Kling 3.0, Wan 3.0, MiniMax H3 Max, Omni Flash, Runway Gen-4.5, FLUX 3 Video, LTX-2.5 Pro/Fast, Hailuo 2.3 [S88] | **Yes.** Krea's docs describe an MCP server that agents join with sign-in (OAuth) or an API key, plus a REST API [S88] | Compute units (subscription + API) [S88][U: rates] | Medium. |
| **Freepik** | 40+ video models; "Spaces" node canvas [S69][U] | Probably: Freepik's developer docs now redirect to **Magnific** (Freepik's upscaling brand), which advertises an MCP server that can "create videos"; the video models listed there looked older (Kling v2) [S89][U] | Subscription | Easy by hand. |
| **OpenArt** | 100+ image, video and audio models incl. Kling 3.0, Seedance, FLUX 3; Character Builder; One-Click Story [S71] | **Yes.** "Access to OpenArt MCP" is listed on every plan [S71] | Starter $13, Plus $27, Pro $44, Wonder $175 per seat per month as displayed on 2026-09-27 (may be annual-billing rates); commercial rights from Plus [S71] | Easy by hand. |
| **LTX Studio** | LTX models (+ others) [S72][U] | Not verified (the pricing page failed to load on 2026-09-27) | Free–$125/mo; commercial use from $35 [S72][U] | Easy; closest to "script → storyboard → clips" in one app. |
| **Pika (relaunched 17 Sep 2026)** | Pika's own models + Seedance, MiniMax H3, GPT Image "and others"; auto-picks a model; says Seedance costs half what other platforms charge [S45] | Developer access via "Pika API Club" and an Enterprise API at dev.pika.art [S45]; MCP not mentioned [U] | Subscription (plans differ only in credits and concurrency) [S45] | Easy. |
| **ComfyUI / Comfy Cloud** | Any open model locally; "partner nodes" call Kling, Seedance, Veo, Grok etc. [S74][U] | Partly: an LLM can write ComfyUI workflow files, but you must load and run them [J] | Free locally; cloud credits | Hard. |

**Recommendation [J]:** For this pipeline, connect **one pay-per-use aggregator with an MCP connector (fal)** for automation and price transparency, plus **Runway or Higgsfield** (sign-in connectors, no keys) for the easiest start; Krea and OpenArt are alternatives with MCP connectors [S88][S71]. That covers every first-choice model in Section 5 except Luma Ray3.2 (use Luma's own API or app) and Midjourney (website only).

**If/then for choosing where to start [J]:**
- **If** you have never used an API key **then** start with Runway's connector (sign in, no key), **because** it carries Seedance 2.x, Veo 3.1, Wan 3.0, H3, Omni Flash and (via MCP) Kling in one credit balance [S25][S26].
- **If** you want the lowest price per clip and a price check before every run **then** add fal, **because** its MCP has a `get_pricing` tool and fal often lists models first [S58].
- **If** a model you need is on neither **then** check Replicate (Gen-4.5, Vidu Q3) or the maker's own app (Luma, Midjourney), before opening any other account.

---

## 8. Recipes (step by step, with an LLM helping)

Each recipe starts with a **Cost / time / difficulty** line. Costs are my estimates [J] from the prices in Section 3A, for one shot unless stated. Difficulty: *Easy* = clicking and pasting; *Medium* = you must check pictures carefully or use an editor's basic tools; *Hard* = you will need Blender or compositing, with the LLM walking you through each step.

### Recipe 1: Connect your LLM to a video aggregator (one-time, 15 minutes)

*Cost / time / difficulty:* free to connect; $10–50 of starter credit; 15 minutes; Easy (Runway, Higgsfield, Krea, OpenArt sign-in) or Medium (fal, Replicate: one API key).

*Easiest path, no keys (Runway or Higgsfield):*
1. Open Claude's settings → **Connectors** → **Add custom connector**.
2. Paste the connector address: Higgsfield `https://mcp.higgsfield.ai/mcp` [S57] or the Runway address shown on runway.com/mcp [S26].
3. Click **Connect** and sign in to your Runway or Higgsfield account. Buy the smallest credit pack.
4. Ask the LLM: "Using the connector, list the video models you can call and what each costs per second."
5. Test with one 4-second draft of something simple ("a torch beam moving across wet brick"). Confirm the clip appears and the credit charge matches.

*Pay-per-use path with the widest choice (fal):*
1. Create a fal account, add $20–50 of credit, and create an API key (a long password for programs).
2. Ask the LLM to connect it. In Claude Code the LLM runs: `claude mcp add --transport http fal-ai https://mcp.fal.ai/mcp --header "Authorization: Bearer $FAL_KEY"`; in Claude Desktop it gives you a small settings snippet to paste [S58]. You paste the key when asked; never paste it into a shared document.
3. Ask: "Use get_pricing for Kling 3.0 Pro image-to-video, Seedance 2.5 reference-to-video, Wan 3.0 and Veo 3.1 Lite." Compare with Section 3A.

### Recipe 2: Build a reference pack for a character or creature (per character, ~30 minutes)

*Cost / time / difficulty:* about $0.50–3 of image generation per character (6–30 stills at $0.02–0.10), plus $0–5 for a voice sample; 30–60 minutes; Easy, but you must reject inconsistent sets.

1. Give the LLM the character's design notes from the breakdown (face, build, clothing, colour palette, what they carry).
2. Ask it to write six image prompts: front face, three-quarter face, profile, full body front, full body back, and one "in-scene" still under the film's lighting. Use a plain grey background for the first five.
3. Generate them with an image model (the image-model file in this library covers which). Reject any set where the face changes between images.
4. Name files clearly: `IONA_front.png`, `IONA_34.png`, … Keep one folder per character.
5. Record in the breakdown which model limits apply: Veo 3.1 takes 3 images (and then must make an 8 s clip) [S2], SkyReels V3 4 [S85], HappyHorse 5 [S37], Kling O3 7 (4 if you also give a video) [S11][S13], H3 9 [S32], Seedance 2.0 9 [S17], Wan 3.0 10 [S34], Seedance 2.5 30 [S22]. Choose the best 3 for Veo, and so on. **If** you can only keep three, **then** keep front face, three-quarter face and full body front, **because** those carry identity, costume and proportions [J].
6. For voices: record or synthesise a 10–30 s sample per speaking character and store it with the pack (Kling Omni takes 5–30 s in Kling's app [S11]; H3 and Wan 3.0 take audio clips up to 15 s in total [S32][S34]). If you will use Kling through fal, also make a 3–8 s video clip of the character speaking that sample, because fal binds voices only to video elements [S12][S11].

### Recipe 3: Make one shot from the breakdown (repeat for every shot)

*Cost / time / difficulty:* drafts $0.20–1.00 (two 5 s drafts at $0.02–0.10/s); finals $2–10 (2–4 takes of 5–8 s at $0.12–0.47/s); 10–20 minutes of your attention; Easy to Medium.

1. Paste the shot's entry from the breakdown into the LLM and ask: "Using the C1 decision table and rules, choose the model, the input mode (text, image-to-video, start-and-end, references, control video) and write the model-specific prompt."
2. Check the LLM's choice against Section 5 yourself: does the shot have dialogue, text, floating objects, violence, a creature, an exact camera path?
3. If needed, make the start frame (and end frame) as stills first and approve them.
4. Generate **two drafts** on the cheap draft model. Watch them.
5. Fix the prompt or inputs once. Then generate the final on the first-choice model: usually 2–4 takes.
6. Log in the breakdown: model name and version, date, settings, seed (if shown), cost, and which take you kept. This makes the shot repeatable when models change.

### Recipe 4: Dialogue exchange (a two-hander)

*Cost / time / difficulty:* for an exchange of 6 lines: one silent two-shot (8 s × 3 takes) plus 6 close-ups × 6 s × 3 takes ≈ 130 s of generation, about $22–62 at $0.17–0.47/s, plus $0–5 of voice synthesis; 1–2 hours; Medium (you line clips up against the audio in an editor).

1. Lock the voices first (Recipe 2, step 6). Make the full exchange as audio, one line per file, with the pauses you want.
2. Plan coverage: a two-shot (both people) with no one speaking on screen, then a single close-up per line.
3. For each close-up, use image-to-video from an approved still of that character plus the line's audio as an audio reference (Seedance 2.x, H3, Wan 3.0), or Kling 3.0 Omni with the bound voice. Prompt what the *listener's* face does only if they are in shot.
4. If a performance matters, act the line yourself on a phone and use performance transfer (Recipe 7).
5. Cut the close-ups against your audio track in the editor. If lip sync is slightly off, slide the clip a few frames; if it is badly off, redo only that take.

### Recipe 5: Exact start and end picture

*Cost / time / difficulty:* two stills ($0.05–0.20) + 3 takes × 5–8 s ≈ $2–8; 20–30 minutes; Easy to Medium.

1. Make the start still and the end still with the same reference pack and lighting description.
2. Check both stills side by side: same costume, same set, logical movement between them. **If** the two stills differ in anything except what the shot is meant to change **then** remake one of them first, **because** the model will animate every difference, including mistakes [J].
3. Use H3 first-and-last mode, Kling 3.0 start + end image (`end_image_url` on fal), Seedance 2.x start + end image on fal, or Veo 3.1 / Fast `image` + `lastFrame` (4, 6 or 8 s; 8 s if you want 1080p or 4K; not Veo 3.1 Lite in the API) [S32][S12][S17][S90][S2].
4. Prompt only the *motion between* the frames ("the cage drops, then stops hard; everyone jolts forward"). Do not re-describe the pictures.

### Recipe 6: Blender previs to final clip (for exact camera or impossible physics)

*Cost / time / difficulty:* Blender is free; 2–6 hours the first time, 30–90 minutes once you have a template; generation $5–25 per shot on hosted models, or $0 plus electricity on your own GPU; Hard (the LLM can write the Blender script, but you must run it and check the render).

1. Build or ask the LLM to script a rough Blender scene (the Blender file in this library covers how): grey boxes for sets, simple figures, the camera path, simulated floating objects.
2. Render a grey "clay" video at the final length and aspect ratio, plus, if the tool supports it, a depth render.
3. Choose the route. Hosted, easiest first: **Seedance 2.5** with the clay render as a video reference [S18]; **H3** with "reference the camera movement from Video 1" [S31]; **Luma Ray3.2** Modify [S28]. Open weights (needs ComfyUI and a GPU): **LTX** with union control (depth, pose and edges) — the published union LoRA is for LTX-2.3; ComfyUI's LTX-2.5 example workflows show union control too [S43][S42]; camera-move LoRAs (dolly, jib) exist only for the earlier LTX-2 [S43]; **Wan 2.1 VACE** [S35]. **If** you have no GPU and no ComfyUI experience **then** take a hosted route, **because** the open route adds hours of setup [J].
4. Add the reference pack for the characters in the shot.
5. Prompt the *look* (light, materials, mood), because the motion comes from the control video.
6. Compare the result with the previs frame by frame at the key moments.

### Recipe 7: Performance transfer from your own acting

*Cost / time / difficulty:* $1–5 per shot (Kling Motion Control ≈$0.07–0.10/s on one reseller [S80]); 30 minutes including filming; Medium (you have to act, light and frame a phone video).

1. Film yourself on a phone, eye-level, plain background, good light, acting the moment (head, face, hands). For Kling Motion Control keep the driving clip 2–5 s; longer clips blur the motion signal [S80].
2. Make a still of the character in the target set (for Kling 3.0, up to 7 reference images of the character improve face consistency, the most common failure [S80]).
3. Use Runway Act-Two (driving video + character) [S78], Kling Motion Control [S80], Luma Ray3.2 (faces up to 8) [S28], or open Wan-Animate-2 [S36].
4. Check hands and where the eyes look (the eyeline must match the other person's position); redo with a slower performance if limbs smear.

### Recipe 8: Mirror-world shots (text and layout reversed)

*Cost / time / difficulty:* no extra generation cost; +10 minutes per shot for the flip and text overlay; Easy to Medium.

1. Write the shot the *normal* way round in the prompt: signs read correctly, the steering wheel is on the usual side, and so on. Where the script says a turned character's asymmetric feature appears "wrong" to the audience (a ring, a scar, a lopsided smile), place it on the *opposite* side in the prompt.
2. Generate, then flip the whole clip horizontally in the editor (every editor has "flip horizontal").
3. Add or replace any readable text *before* flipping, in compositing, so it is exact.
4. Keep a "mirror" column in the breakdown so the editor knows which shots to flip.

### Recipe 9: Screens (tablets, security-camera monitors, recorded clips)

*Cost / time / difficulty:* two clips instead of one, about $2–8; 30–60 minutes; Medium (corner-pinning a clip onto a screen is a basic compositing task; the LLM can talk you through it in a free editor such as DaVinci Resolve).

1. Make the screen content as its own clip (for security-camera pictures: high angle, wide lens, desaturated, low frame rate, timestamp added in compositing).
2. Make the shot of the device with the screen showing plain green or a dark neutral image.
3. Composite the content onto the screen in the editor (the compositing file in this library covers how). If you cannot composite, use image-to-video from a still where the screen image is already correct, and keep screen motion minimal.

### Recipe 10: Batch automation from the breakdown file

*Cost / time / difficulty:* whatever the shots cost (Section 10), with a hard spending cap; 1–2 hours to set up with the LLM; Medium (you run one script the LLM writes, after testing it on three shots).

1. Keep the breakdown as a structured file (one entry per shot: shot ID, model, mode, prompt, reference files, start/end frames, audio file, duration, status).
2. Ask the LLM: "Write a Python script that reads `breakdown.json`, sends every shot with status `ready` to fal using the model and inputs listed, saves each clip as `SHOTID_takeN.mp4`, and writes the cost back into the file. Stop if the total cost passes $X." One shot entry might look like this (illustrative; the model ID must be copied from the aggregator's own model page on the day, because IDs change):

   ```json
   {"shot_id": "S07_03", "status": "ready", "model": "fal: kling-video v3 pro image-to-video",
    "mode": "start_end_frames", "start_frame": "refs/S07_03_start.png", "end_frame": "refs/S07_03_end.png",
    "references": ["refs/IONA_front.png"], "audio_in": null, "native_audio": false,
    "duration_s": 5, "aspect": "16:9", "mirror_flip": false, "takes_wanted": 3,
    "prompt": "The rung rolls in its brackets; her fingers open; torchlight trembles.",
    "cost_usd": null, "kept_take": null}
   ```
3. Run a test on three shots. Check files, names and costs. **If** any clip's measured cost differs from the logged price by more than 20% **then** stop and ask the LLM to re-read the platform's price page (rule 24) before running the rest.
4. Run the rest overnight. Next day, review every take yourself (rule 18) and mark keepers.

### Recipe 11: Take review checklist (human, for every kept take)

*Cost / time / difficulty:* free; 2–5 minutes per take; Easy, but do not skip it (rule 18).

Faces match the reference pack • hands have five fingers and hold things properly • rings, scars and smiles on the correct side • no objects appearing or vanishing • cause before effect • gravity behaves as the script says • text correct (or blank for compositing) • right person's mouth moves • audio has no unwanted music or extra voices • cuts cleanly against neighbouring shots.

---

## 9. Known failure modes and workarounds

| Failure | Where it is documented | Workaround [J unless cited] |
|---|---|---|
| **Physics errors** (things fall wrongly, liquids break apart, objects pass through each other) | 83.3% of third-person and 93.5% of first-person clips from Sora 2, Veo 3.1 Fast, Kling 2.5, Hailuo 2.3 and Wan 2.2 had at least one glitch that ordinary human viewers could identify (March 2026 study) [S65]; these are one generation behind today's leaders, so current rates may be lower [J] | Previs + control video (Recipe 6); shorter clips; composite the element. |
| **Objects vanish after being hidden; effects before causes; actions succeed too easily** | Runway's own list for Gen-4.5 [S23] | Keep props visible; split cause and effect into two shots; check every take. |
| **Character drift** (face, costume, creature design change between shots) | [J] common experience | Reference pack in every shot (Recipe 2); same model for all shots of one scene. |
| **Voice drift** (a character sounds different in each clip) | [J] | Voice first (rule 1); audio references or voice binding. |
| **Wrong mouth moves**, or both people talk | ByteDance notes multi-subject weakness [S18] | One speaker on screen per clip (rule 2). |
| **Garbled or mirrored text** | Alibaba lists text as a weak point of Wan 3.0 [S33] | Blank text areas, add in compositing; flip whole frames (Recipe 8). |
| **Hands** (extra fingers, ring on the wrong finger, grip passing through objects) | [J] | Insert close-ups made from a checked still; hide hands in wide shots. |
| **Fast motion smears** (falls, fights, whip pans) | [J] | Slow-motion in prompt then speed up in edit; control video; shorter clip. |
| **Seams on extended clips** (light or face jumps at each join) | [J]; Veo extends in 7 s steps at 720p only [S2] | Use 20–30 s models; hide joins with cutaways. |
| **Unwanted audio** (music you didn't ask for, extra voices, subtitles) | [J] | Say "no music, no subtitles" in the prompt; strip audio and rebuild in the mix when needed. |
| **Refusals of violence, blood, guns** | [S67][S15][S68] | Rule 9 and rule 10. |
| **Clips deleted by the platform** | Google keeps clips 2 days [S2] | Download immediately; batch script saves locally (Recipe 10). |
| **Model retired mid-project** | Sora 2 API removed 24 Sep 2026 [S8]; Veo 2/3.0 shut 30 Jun 2026 [S1] | Log model versions; keep stills and prompts so shots can be re-made on a successor. |
| **LLM reviewer misses errors** | Best LLM critics caught far fewer glitches than untrained viewers [S65] | Human review of every kept take (Recipe 11). |
| **Glass and reflections** (dialogue through glass shows impossible reflections or no glass) | [J] | Ask for "faint reflections"; or shoot each side separately and composite the glass layer. |
| **Transparent things** (the clear sea animal, the clear shell) look solid or disappear | [J] | Strong backlight and dark water in the prompt; reference images of the design; macro framing. |

---

## 10. What a 20-minute short costs to generate

**How the arithmetic works [J]:** you pay for every generated second, not every second you keep.

*Generated seconds = finished seconds × overshoot × retake ratio.*

- **Finished seconds:** 20 minutes = 1,200 s.
- **Overshoot:** models have minimum lengths (often 3–5 s) and you trim the start and end, so each clip is longer than the part you use. Typical 1.5–3× [J]. (An earlier draft cited a vendor for "5 s used from each 15 s clip"; I could not find that figure on the cited page, so treat the overshoot range as my estimate.)
- **Retake ratio:** takes made per take kept. A vendor reports 164 clips generated and 41 used on a 3-minute episode (a 25% "editorial yield", i.e. 4:1), made by two people in two days for $950 ($315 per finished minute), and recommends budgeting "roughly three generations per usable shot" [S66]. (This is a vendor's own data; treat as indicative. It also notes that shots with several characters touching, and point-of-view shots, cost well above average.)

**Three price tiers per generated second (from Section 3A, audio included where offered):**

- *Budget* ≈ $0.07: Veo 3.1 Lite ($0.05–0.08), Wan 3.0 480p ($0.05), Omni Flash 720p (≈$0.10), fal's H3 Max (≈$0.04).
- *Mid* ≈ $0.17: Kling 3.0 Pro with audio ($0.168), Veo 3.1 Fast 1080p ($0.12), Wan 3.0 1080p ($0.20), Grok Imagine 1.5 720p ($0.14–0.16), MiniMax H3 at 2K (≈$0.13).
- *Premium* ≈ $0.45: Veo 3.1 Standard ($0.40), Kling O3 4K ($0.42), Seedance 2.5 720p on fal ($0.47).

| Scenario | Overshoot × retakes | Generated seconds | All budget | All mid | All premium |
|---|---|---|---|---|---|
| Lean (careful previs, start frames, experienced) | 1.5 × 3 = 4.5 | 5,400 | $378 | $918 | $2,430 |
| Typical | 2 × 4 = 8 | 9,600 | $672 | $1,632 | $4,320 |
| Heavy (first-timer, no previs: the vendor's documented 4:1 retake ratio with 3× overshoot) | 3 × 4 = 12 | 14,400 | $1,008 | $2,448 | $6,480 |

**Recommended mix [J]:** draft everything at budget price, then re-make only kept shots at mid or premium. Typical case: 9,600 s of drafts × $0.07 = **$672**, plus finals 1,200 s × 2 overshoot × 1.5 retakes = 3,600 s × $0.30 average = **$1,080**, total **≈ $1,750**. Add, as rough estimates [U]: reference and start-frame stills (~1,000 images at $0.02–0.10 each: $20–100), voices and music ($20–100/month subscriptions), upscaling, and one editing app subscription. A realistic generation budget for *The Catch* at 20 minutes is **$1,500–4,500**; a first-time user who does not previs should budget the "heavy" row. A vendor reports finished AI shorts at $315–750 per finished minute (platform-credit spend at $0.21–0.25 per credit, including all iteration), which would be $6,300–15,000 for 20 minutes [S66]; its cheapest case was a 3-minute animated episode, so live-action-look drama with dialogue is likely to sit nearer the top of that range [J].

**If/then budget rules [J]:**
- **If** your total budget is under $1,000 **then** make the whole film as a budget-tier animatic first, and upgrade only dialogue close-ups and key images (for *The Catch*: the rung, the cage fall, the Figure, the chest, the rings) to mid or premium.
- **If** a single shot has used more than 10 takes **then** stop, and switch method (start-and-end frames, previs, compositing, or a still with a slow push-in) rather than spending more on the same prompt.
- **If** the spend passes 50% of the budget before 50% of the shots are kept **then** move all remaining non-dialogue shots to the budget tier.

**Time [J]:** at 5–10 minutes per shot of human attention (choose, check, log) and about 300 shots, expect 25–50 hours of review work, separate from the time spent waiting for clips.

---

## 11. Worked examples from *The Catch*

Each example quotes the screenplay, names the hard part, and gives the model choice. Model choices are judgments [J] resting on the verified capabilities cited.

**Example 1: the rung turns (INT. FREIGHT SHAFT)**
> "Her hand closes on a rung and the rung TURNS. / She goes still. The rung rolls in its brackets like a rolling pin."

- *Hard part:* a small, exact hand action lit only by a torch held in her teeth; hands are a known weak spot.
- *Plan:* make two stills: hand closing on the rung, and the rung rotated with her fingers opened. Use **MiniMax H3 first-and-last mode** or **Kling 3.0 start + end image** (both verified [S32][S12]); 5 s, silent (the metallic creak is added in the sound mix). Draft on Omni Flash at 360p (it accepts start and end frames [S3]). Cover with a separate insert of the sheared bracket ("one bracket sheared clean through") as its own still-based shot.

**Example 2: the cage falls and the blood floats (INT. FREIGHT CAGE)**
> "Her boots leave the floor. She gets her fingers into the grid. Her body floats out behind her like washing. / Jude's blood lifts off the steel in round red beads and hangs in the air between them, turning."

- *Hard part:* zero gravity inside a falling cage (models favour normal gravity [S65]), plus blood (filter risk [S15][S67]).
- *Plan:* Blender previs of the cage interior, the camera locked to the cage, figures rising, and a simple particle simulation for 20–30 beads. Route A (hosted, easier): **Seedance 2.5** with the clay render as a video reference plus the three character reference packs, 10–15 s at 720p [S18][S22]. Route B (open, free per clip, harder): **LTX** with union control (depth from the previs), using LTX-2.3's published union LoRA or a ComfyUI LTX-2.5 union workflow [S42][S43]. Generate the shot **without blood**, then composite the beads from the Blender render as small dark-red spheres. Keep the wound itself out of frame.

**Example 3: the backwards world (INT. MAINTENANCE PASSAGE / EXT. STREET)**
> "Every letter is backwards." … "At the fire door, the green sign is backwards too. The little running man is running the other way." … "The wheel is on the other side. Her own coffee cup in the holder, on the wrong side of the gearstick."

- *Hard part:* exact reversed text and reversed car layout.
- *Plan:* Recipe 8. Generate a normal fire-exit sign and a normal car interior (any top model; Kling 3.0 or H3 claim better text [S10][S31]), add exact text in compositing, then flip the whole clip. The actors' asymmetric details must be planned *before* the flip: in *The Catch* the three turned characters (Iona, Eli, Jude) should be prompted with rings on the *right* hand so that after the flip they read as left, matching "Iona looks down at her own ring, on her own left hand." Unturned characters are prompted the normal way (Saye's ring on her *left* hand), so that after the flip it reads "Saye's wedding ring. On her right hand." The same rule works unflipped at the end of the film: after Iona turns back, the final scenes are not flipped, and Jude (still turned) wears his ring on his right hand exactly as scripted ("His wedding ring. On his right hand."). Eli's lopsided smile must likewise be designed once and then placed on the side that makes it read as "The familiar little smile, on the wrong side of his face." in the unflipped homecoming scene. **If** the breakdown marks a scene "mirror" **then** every asymmetric detail in it (rings, scars, parting, smile, a bandaged hand) gets a "prompt side" and a "screen side" column, **because** the LLM writing prompts will otherwise put details on the screen side and the flip will reverse them [J].

**Example 4: the kitchen, hands raised (INT. SAYE'S HOUSE - KITCHEN)**
> SAYE: "Hold up your right hand." … "They stand facing each other across the table like a woman and her reflection, each with the wrong hand in the air." / SAYE: "That is your left." / IONA: "It's my right."

- *Hard part:* two-person dialogue with a precise, readable hand-and-ring action, and the mirror logic of Example 3.
- *Plan:* voice first (rule 1). A silent two-shot of both raising hands, made from an approved still where the hands and rings are correct, flipped if the scene is in the mirror set (decide per scene in the breakdown). Then single close-ups per line: **Kling 3.0 Omni** with bound voices (through fal, bind each voice to a short video element of the character [S12]), or **Seedance 2.5 / H3** with each line's audio as a reference [S11][S22][S32]. Ring close-ups ("Saye's wedding ring. On her right hand.") as separate inserts made from stills, because ring-hand accuracy in motion is unreliable [J].

**Example 5: the Figure beside Jude's bed, seen on a tablet (INT. QUARANTINE - JUDE'S ROOM (ON THE TABLET))**
> "Something tall and black stands beside his bed. It did not come through the door. It is simply there … Where a face would be, a pale strip slides across, vanishes, slides across again. From inside it, a PUMP: three strokes, not quite even."

- *Hard parts:* a creature design that must match in several later scenes; it appears between frames; it is seen on a tablet screen.
- *Plan:* build the Figure's reference pack (front, side, back, the head with the strip lit, the hand) and keep it for every appearance; **Kling O3** (7 references [S13]) is first choice; Seedance 2.5 as backup. Make the appearance as a hard cut (empty frame, then the Figure present) rather than asking the model to "materialise" it. Generate the room as a security-camera-style clip (Recipe 9: high angle, wide, desaturated) and composite it onto the tablet. The pump is sound design, not model audio: three uneven strokes must be identical every time it recurs, including the last line of the film ("Three uneven strokes in the dark.").

**Example 6: the chest opens (INT. SHIP - OUTER RECESS (THE DIP))**
> "Latches let go, one after another, down the front of it. / The chest swings open. … hanging in the mount a glass VESSEL of dark water … In the water: an ANIMAL. Almost clear, like a thing from the bottom of the sea."

- *Hard parts:* a mechanical reveal with sequential latches; a transparent animal; continuity with the Figure pack.
- *Plan:* **Luma Ray3.2** with keyframes pinned to each latch release (up to 16 keyframes [S28]) for the opening, silent, latch clicks in the sound mix. The animal as its own macro shots from its own reference pack, strongly backlit in dark water; **Veo 3.1** at 4K or **Kling O3 4K** for detail. Keep the vessel and animal shots short (4–6 s) to avoid drift.

**Example 7: the shot through the roof (INT. FREIGHT CAGE)**
> "Far above, the stair door gives with a crash. Someone KICKS the top gate open and FIRES down through the roof. / JUDE (quite softly) Oh. / He sits down into Eli with a hole through his shoulder."

- *Hard part:* gunfire and a wound, the most likely refusal in the film.
- *Plan:* rule 9. Shot A: looking up the shaft, a flicker of muzzle flash far above (small, abstract light). Shot B: Jude's face as he says "Oh." (dialogue close-up, voice first). Shot C: Jude sitting down heavily into Eli's arms, the shoulder turned away from camera. Gunshots and the ricochet ("Another shot sparks off the grid beside her boot") are sound plus a spark element composited onto the grid. Any mid-tier model works; Kling 3.0 or H3 for the faces.

**Example 8: the end, rings through glass (INT. QUARANTINE - IONA'S ROOM - DAY)**
> "She lifts her own left hand and lays it against his, through the glass. The two rings sit directly across from each other, like a ring and its reflection."

- *Hard part:* the image the whole film builds to; two hands, two rings, glass.
- *Plan:* make the exact final frame as a still first (image model, checked by eye for fingers and ring placement), then **image-to-video** with minimal motion (Veo 3.1 or Kling 3.0, 6–8 s), prompting only slight breathing and light change. If the model disturbs the hands, use the still with a slow push-in (a gradual zoom towards the hands) done in the editor instead: a still is a valid shot.

**Budget and difficulty for the eight examples [J]** (final takes only; add about 30% for cheap drafts; prices from Section 3A):

| Example | Model and mode | Generated seconds | Estimated cost | Difficulty |
|---|---|---|---|---|
| 1 Rung turns | H3 first-and-last, 5 s × 4 takes, + bracket insert from a still | 20 s | ≈$3 (H3 at ≈$0.13/s) | Medium: two matching stills |
| 2 Cage falls, blood floats | Seedance 2.5 clay reference, 12 s × 4 takes; beads composited | 48 s | ≈$23 (fal 720p) or ≈$11 (Replicate); $0 on own GPU via LTX | Hard: Blender previs + compositing |
| 3 Backwards world (3 shots) | Kling 3.0 Pro silent, 6 s × 3 takes each; text overlay; flip | 54 s | ≈$6 | Medium: editor flip + text |
| 4 Kitchen hands (two-shot + 4 lines) | Silent two-shot 8 s × 3; close-ups 6 s × 3 on Kling Omni / H3 with voice | 96 s | ≈$13 (H3) to $45 (Seedance 2.5 on fal) | Medium |
| 5 Figure on the tablet | Kling O3 references, 8 s × 4 takes (1080p is enough for a screen) | 32 s | ≈$5–13 | Medium–Hard: screen composite |
| 6 Chest opens + animal macro | Ray3.2 keyframes 10 s × 4; Veo 3.1 4K macro 8 s × 3 | 64 s | ≈$10 + $14 ≈ $24 | Hard: keyframe stills, transparency |
| 7 Shot through the roof (3 shots) | Kling 3.0 / H3, 5 s × 3 takes each; flash and sparks composited | 45 s | ≈$6–8 | Medium |
| 8 Rings through glass | Still → Veo 3.1 1080p i2v, 8 s × 3 | 24 s | ≈$10 (or $0 with the still-and-push-in fallback) | Easy–Medium |

These eight moments cost roughly $80–130 in final takes: small next to the whole film (Section 10), because the expensive part of a 20-minute film is the hundreds of ordinary coverage shots, not the showpieces.

---

## 12. What I could not verify

- **Grok Imagine 1.5** per-resolution prices at xAI itself (xAI lists one "from $0.08/s" rate; Runway's per-resolution credits are verified) and whether text-to-video is offered on every route (xAI's docs say yes; Vercel's page says image-to-video only) [S81][S25][S47][S48].
- Whether **HappyHorse** accepts an *end* frame through third-party APIs. (Seedance 2.0 and 2.5 do, on fal: verified.)
- **Runway Gen-4.5** native audio: I found no evidence of it and treat it as silent; if Runway adds audio, Section 3A, rule 22 and the dialogue row need updating. Also unverified: keyframes and References with Gen-4.5 in the API.
- **Luma Ray3.2** pricing (from a secondary source) [S30].
- **Kling 3.0** multi-shot maximum ("6 shots" is from secondary sources), Kling's extend feature, and the audio-language list (the Kuaishou press release [S10] was unreachable on 2026-09-27).
- **Aleph 2.0**'s exact abilities (one secondary source says it cannot create new camera angles; Aleph 1 marketing said it could) [S27].
- **Adobe Firefly Video**'s own specs and whether Ray3.14, Marey and Aleph are in Firefly; **Freepik**/Magnific's current video models; **LTX Studio** prices and API access (its pages failed to load); Krea's compute-unit rates.
- **SkyReels V4** and **HiDream-O1-Video**: access routes, clip length and controls (only leaderboard data found). **Agnes-Video-2.5** (Sapiens AI): everything except its leaderboard score and price.
- Whether **LTX-2.5** accepts the LTX-2.3 union-control LoRA directly (ComfyUI example workflows suggest union control works on 2.5, but no 2.5-specific LoRA is published) [S42][S43].
- Whether **Google Flow** can be driven by an outside LLM; Flow credit costs per model (Flow shows them live in settings) [S6].
- The **HunyuanVideo 1.5** licence terms, the **SkyReels V3** licence terms, and whether the **MiniMax H3** licence has a revenue threshold (it requires an application form for commercial use in the USA, EU, UK and South Korea) [S32].
- **Midjourney** video resolution and whether an API exists in 2026 (none found).
- How each platform actually treats blood and gunfire prompts in 2026: only one hands-on report (it names Runway refusing and says Google's filters ignore the policy's artistic exception) was found [S67]; Kling's blocked-term lists come from third-party guides.
- Whether a successor to Veo 3.1, Kling 3.0 or Gen-4.5 is imminent: none is announced in the sources I could open, but my web search allowance ran out during this check, so news from the last few days of September 2026 may be missing.

---

## 13. Sources (all checked 2026-09-27)

"(search)" means the fact came from the search-engine summary of that page, not from opening the page itself.

- [S1] Gemini API release notes (Veo 3.1, Lite, Omni Flash GA, Veo 2/3.0 shutdown): https://ai.google.dev/gemini-api/docs/changelog
- [S2] Gemini API, Veo 3.1 documentation: https://ai.google.dev/gemini-api/docs/veo
- [S3] Gemini API, Omni Flash documentation: https://ai.google.dev/gemini-api/docs/omni
- [S4] Gemini API pricing: https://ai.google.dev/gemini-api/docs/pricing
- [S5] Google blog, "Introducing Gemini Omni": https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/
- [S6] Google Flow Help, models and features: https://support.google.com/flow/answer/16352836?hl=en
- [S7] The Rundown, Gemini Omni Flash specs (reviewed 28 Aug 2026): https://www.therundown.ai/tools/gemini-omni
- [S8] OpenAI API deprecations (Sora 2 / Videos API): https://developers.openai.com/api/docs/deprecations
- [S9] OpenAI Help, Sora discontinuation (search): https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation
- [S10] Kuaishou press release, Kling 3.0: https://ir.kuaishou.com/news-releases/news-release-details/kling-ai-launches-30-model-ushering-era-where-everyone-can-be
- [S11] Kling VIDEO 3.0 Omni user guide: https://kling.ai/quickstart/klingai-video-3-omni-model-user-guide
- [S12] fal, Kling Video v3 Pro image-to-video: https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video
- [S13] fal, Kling O3 4K reference-to-video: https://fal.ai/models/fal-ai/kling-video/o3/4k/reference-to-video
- [S14] Atlas Cloud, Kling 3.0 Turbo and Omni (17 Jun 2026): https://www.atlascloud.ai/blog/guides/kling-3.0-turbo-kling-omni
- [S15] Kling community policy: https://kling.ai/docs/community-policy
- [S16] fal, Seedance 2.0 vs Kling 3.0 (20 Apr 2026): https://fal.ai/learn/tools/seedance-2-0-vs-kling-3-0
- [S17] fal, Seedance 2.0 page: https://fal.ai/seedance-2.0
- [S18] ByteDance Seed, "Introducing Seedance 2.5": https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5
- [S19] The Next Web, Seedance 2.5 announcement: https://thenextweb.com/news/bytedance-seedance-2-5-ai-video-4k-30-seconds
- [S20] CellCog, Seedance 2.5 pricing by provider (updated 8 Sep 2026): https://cellcog.ai/blog/seedance-2-5-pricing/
- [S21] EvoLink, Seedance 2.5 API status: https://evolink.ai/blog/seedance-2-5-api-status
- [S22] fal, Seedance 2.5 reference-to-video: https://fal.ai/models/bytedance/seedance-2.5/reference-to-video
- [S23] Runway, Gen-4.5 research page: https://runway.com/research/introducing-runway-gen-4.5
- [S24] Runway changelog: https://runway.com/changelog
- [S25] Runway API changelog: https://docs.dev.runwayml.com/api-details/api_changelog/
- [S26] Runway MCP: https://runway.com/mcp
- [S27] Pexo, Runway Aleph 2.0 explainer: https://pexo.ai/blog/what-is-runway-aleph-2-0-6791
- [S28] Luma, "Introducing Ray3.2": https://lumalabs.ai/news/introducing-ray-3-2
- [S29] Luma, information for AI assistants: https://lumalabs.ai/llm-info
- [S30] eesel AI, Luma pricing (search): https://www.eesel.ai/blog/luma-ai-pricing
- [S31] MiniMax, H3 blog: https://www.minimax.io/blog/minimax-h3
- [S32] MiniMax H3 model card: https://huggingface.co/MiniMaxAI/MiniMax-H3
- [S33] Alibaba Cloud blog, Wan3.0: https://www.alibabacloud.com/blog/wan3-0-30-second-ai-video-generation-from-any-input_603452
- [S34] fal, Wan 3: https://fal.ai/wan-3
- [S35] Hugging Face, Wan-AI model list: https://huggingface.co/api/models?author=Wan-AI
- [S36] Wan-Animate-2 model card: https://huggingface.co/Wan-AI/Wan2.2-Animate-2-14B
- [S37] invideo, HappyHorse 1.0 vs 1.1: https://invideo.io/blog/happyhorse-ai-video-generator/
- [S38] CNBC, Alibaba revealed as HappyHorse maker (search): https://www.cnbc.com/2026/04/10/alibaba-happyhorse-ai-video-model-benchmark-reveal.html
- [S39] Apiframe, Wan 2.7 guide (search): https://apiframe.ai/guides/wan-2.7-guide
- [S40] HunyuanVideo-1.5 GitHub: https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5
- [S41] The Rundown, LTX-2 / LTX-2.5 review (31 Aug 2026): https://www.therundown.ai/tools/ltx-2
- [S42] ComfyUI Wiki, LTX-2.5 open weights: https://comfyui-wiki.com/en/news/2026-08-11-ltx-2-5-open-weights-release
- [S43] Hugging Face, Lightricks model list: https://huggingface.co/api/models?author=Lightricks
- [S44] Pika blog: https://pika.art/blog
- [S45] Pika, "Welcome to the New Pika": https://pika.art/blog/welcome-to-the-new-pika
- [S46] Midjourney, V1 video model: https://updates.midjourney.com/introducing-our-v1-video-model/
- [S47] xAI docs, video generation: https://docs.x.ai/docs/guides/video-generations
- [S48] Vercel AI Gateway, Grok Imagine Video 1.5: https://vercel.com/ai-gateway/models/grok-imagine-video-1.5
- [S49] Creeta, Grok Imagine Video 1.5 pricing and dates (search): https://news.creeta.com/en/grok-imagine-video-1-5-release-2026/
- [S50] fal, Marey Realism v1.5 image-to-video: https://fal.ai/models/moonvalley/marey/i2v
- [S51] fal blog, Marey v1.5 (search): https://blog.fal.ai/moonvalleys-marey-realism-v1-5-is-now-on-fal-the-most-advanced-generative-filmmaking-yet/
- [S52] Adobe blog, video in Firefly (15 Apr 2026): https://blog.adobe.com/en/publish/2026/04/15/adobe-extends-leadership-video-unleashing-new-ai-powered-creation-firefly-reinventing-color-editors-in-premiere
- [S53] Adobe news, Creative Agent (search): https://news.adobe.com/news/2026/04/adobe-new-creative-agent
- [S54] PR Newswire, Vidu Q3 Reference-to-Video (13 Apr 2026): https://www.prnewswire.com/news-releases/shengshu-launches-vidu-q3-reference-to-video-with-expanded-visual-and-audio-capabilities-302740489.html
- [S55] fal, Vidu Q3 image-to-video (search): https://fal.ai/models/fal-ai/vidu/q3/image-to-video
- [S56] PixVerse, V6 launch: https://pixverse.ai/en/blog/pixverse-launches-v6-advancing-ai-video-generation
- [S57] Higgsfield MCP: https://higgsfield.ai/mcp
- [S58] fal blog, fal MCP server (19 Mar 2026): https://blog.fal.ai/connect-your-ai-to-1-000-models-with-the-fal-mcp-server
- [S59] Replicate, MCP server docs: https://replicate.com/docs/reference/mcp
- [S60] Black Forest Labs, FLUX 3 Video: https://bfl.ai/blog/flux-3-video
- [S61] Artificial Analysis, text-to-video leaderboard: https://artificialanalysis.ai/video/leaderboard/text-to-video
- [S62] Artificial Analysis, image-to-video leaderboard: https://artificialanalysis.ai/video/leaderboard/image-to-video
- [S63] Artificial Analysis, video-editing leaderboard: https://artificialanalysis.ai/video/leaderboard/video-editing
- [S64] Hugging Face, Sand.ai MAGI-2 preview: https://huggingface.co/sand-ai/MAGI-2-preview
- [S65] Physion-Eval (arXiv 2603.19607), physical realism in generated video: https://arxiv.org/abs/2603.19607
- [S66] invideo, AI film production cost (updated 15 Jul 2026): https://invideo.io/blog/ai-film-production-cost/
- [S67] HackerNoon, violence filters (19 Aug 2026): https://hackernoon.com/ai-video-generators-flagged-my-anime-duel-as-graphic-violence-it-was-a-cartoon
- [S68] Google Generative AI Prohibited Use Policy (search): https://policies.google.com/terms/generative-ai/use-policy
- [S69] NemoVideo, Freepik video review (search): https://www.nemovideo.com/blog/freepik-ai-video-generator-review
- [S70] Krea blog, best video models on Krea (search): https://www.krea.ai/blog/the-5-best-ai-video-models-on-krea-in-2026
- [S71] OpenArt pricing (opened 2026-09-27; plans, commercial rights and "OpenArt MCP"): https://openart.ai/pricing
- [S72] The Rundown, LTX Studio (search): https://www.therundown.ai/tools/ltx-studio
- [S73] TeamDay, AI API pricing comparison (updated 23 Sep 2026; no longer cited in the body, replaced by Runway's own price page [S82]): https://www.teamday.ai/blog/ai-api-pricing-comparison-2026
- [S74] ComfyUI docs, partner node pricing (search): https://docs.comfy.org/tutorials/partner-nodes/pricing
- [S75] Sloane, Grok Imagine content policy 2026 (search): https://www.sloane.world/guides/grok-imagine-nsfw-content-policy-2026
- [S76] Wikipedia, SpaceXAI (search): https://en.wikipedia.org/wiki/SpaceXAI
- [S77] MindStudio, Seedance 2.0 face restrictions (search): https://www.mindstudio.ai/blog/seedance-2-0-content-restrictions-workarounds
- [S78] Runway Help, Act-Two performance capture (search): https://help.runwayml.com/hc/en-us/articles/42311337895827-Performance-Capture-with-Act-Two
- [S79] WaveSpeed, Omni Flash Flow credits (21 May 2026): https://wavespeed.ai/blog/posts/omni-flash-pricing/
- [S80] Atlas Cloud, Kling Motion Control guide (14 Jul 2026): https://www.atlascloud.ai/blog/guides/kling-ai-motion-control
- [S81] xAI docs, models and pricing (Grok Imagine Video 1.5 "$0.080 / sec"): https://docs.x.ai/docs/models
- [S82] Runway API pricing (credits per second per model; $0.01 per credit): https://docs.dev.runwayml.com/guides/pricing/
- [S83] Runway API model list: https://docs.dev.runwayml.com/guides/models/
- [S84] Wikipedia, Sora (text-to-video model) (app shut 26 Apr 2026, API 24 Sep 2026, announced 24 Mar 2026): https://en.wikipedia.org/wiki/Sora_(text-to-video_model)
- [S85] Hugging Face, SkyReels V3 R2V model card (family capabilities, licence name, VRAM): https://huggingface.co/Skywork/SkyReels-V3-R2V-14B
- [S86] Hugging Face, Skywork model list: https://huggingface.co/api/models?author=Skywork
- [S87] Wikipedia, Veo (text-to-video model) (Veo 3.1 date 15 Oct 2025): https://en.wikipedia.org/wiki/Veo_(text-to-video_model)
- [S88] Krea developer docs index (video models on the API; MCP server with OAuth or API key): https://www.krea.ai/docs/llms.txt
- [S89] Magnific API docs (Freepik's developer docs redirect here; MCP server): https://docs.magnific.com/introduction
- [S90] fal, Seedance 2.5 image-to-video (end frame, durations, prices): https://fal.ai/models/bytedance/seedance-2.5/image-to-video
- [S91] Hugging Face, HiDream-ai model list (no video weights): https://huggingface.co/api/models?author=HiDream-ai
- [S92] Moonvalley homepage (Marey Realism v1.5, 8 Jul 2025; camera, pose, motion and trajectory control): https://www.moonvalley.com/

**Fact-check note (2026-09-27):** an adversarial re-check opened these sources directly: S1, S2, S3, S4, S5, S6, S7, S8, S11, S12, S13, S14, S15, S17, S18, S19, S20, S21, S22, S23, S24, S25, S26, S27, S28, S29, S31, S32, S33, S34, S35, S37, S40, S41, S42, S43, S45, S46 (index only), S47, S48, S50, S52, S54, S56, S57, S58, S59, S60, S61, S62, S63, S64, S65, S66, S67, S68, S71, S79, S80 and S81–S92. Unreachable on that day: S9 (403), S10 (503), S78 (403); their claims are cross-checked against S84 and S83 where possible. Main corrections in that pass: Runway Gen-4.5 has no verified native audio (a Seed Audio 1.0 changelog entry had been misread); Veo 3.1 first-and-last frames do not require 8 s; Seedance 2.0/2.5 end frames verified; LTX control add-ons tied to the right LTX version; Grok Imagine 1.5 prices and lengths re-sourced; Aleph (1) retirement from Runway's API added; the unsupported "5 s used from 15 s" cost claim removed and the heavy cost row recalculated; Krea and OpenArt MCP connectors, SkyReels V3/V4, HiDream-O1-Video and Agnes-Video-2.5 added; OpenArt prices updated; the HackerNoon violence test re-attributed (Runway refused; Google's filters were described, not tested).
