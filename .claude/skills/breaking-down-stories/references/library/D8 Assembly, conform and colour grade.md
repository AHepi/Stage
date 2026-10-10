# D8. Post-production assembly: conform from the breakdown, cross-model colour matching, finishing, titles, subtitles and deliverables

> **What this file is for**
> 1. It turns kept AI takes, voices, effects and music into one finished film: assembly, conform, picture lock, upscaling, grade, sound finish, cards, subtitles and delivery files.
> 2. It says what an LLM can do for a non-technical user here (write scripts, timelines, subtitle files and commands) and what the user must do by hand in an editor.
> 3. It fixes one frame rate, one frame shape and one order of finishing steps, so takes from Veo, Kling, Seedance, Wan and Blender sit together.
> 4. It adds conform, grade, subtitle, card and delivery fields to the breakdown, most of them checkable by the validator.
> 5. It is worked on *The Catch* (SC06 fall, SC13 playback, title and end cards, subtitles) and *The Long Places* chapter VII.

Evidence labels: **[V]** verified at a primary source or two agreeing sources, checked 2026-09-27; **[U]** unverified or secondary only; **[J]** this file's judgment. Tool facts go stale: re-check anything over a month old (C5 R22). Rules are **D8-R#**, recipes **D8-Rec#**.

**Fact-check note (2026-09-27).** An adversarial re-check opened the Resolve 21.1 press release, the Resolve Studio page, three 21.1 reports, the FFmpeg filter manual, fal's Topaz, Topaz-generative, SeedVR2 and Seedance 2.5 pages, Alibaba's Wan 3.0 guide, Topaz Labs pricing, Practical-RIFE, Kdenlive's manual and 25.04 notes, YouTube's encoding and AI-disclosure pages, Vimeo's compression guide, EBU R 128 (PDF) and R 95, Netflix's two timed-text guides, W3C WebVTT, DCP-o-matic, Cologne's DCP sheet, the OFL site and Cinema Tools, and re-matched every quoted line of both test texts. Corrections: free Resolve 21.1 **keeps console scripting**; external scripting, Workflow Integrations and the MCP server are Studio-only (§3); **Topaz Starlight models and SeedVR2 are diffusion models** that rebuild detail, so they are not "non-generative" (§3, D8-R22); Topaz Video Pro's price is restated in §3 (second pass: $699 a year, which is about $58 a month); Film Look Creator is Studio-only [V]; Vimeo *recommends* constant frame rate rather than requiring it (D8-R16); `loudnorm`'s linear mode silently falls back to dynamic mode when the target would break the true-peak ceiling (D8-R40); Netflix loudness is now [V]; the ending no longer lets the pump stop after one cycle, because A4 SND8 and A4 §11 WE3 forbid it (D8-R41, §9.3); B2's sequence 4 is paraphrased, not quoted. Added: Netflix's "only when they cannot be visually identified" rule for SDH labels (D8-R50), Seedance 2.5's H.265 output and 21:9 option, exact ffmpeg commands for VFR, audio, loudness, flicker scans and the web file (Rec2, Rec8, Rec11), the RIFE 16 → 24 route, and a WebVTT sample (§9.4).

**Second fact-check (2026-09-27, adversarial).** Re-opened: the FFmpeg filter and format manuals (loudnorm, deflicker, signalstats, noise, fps, minterpolate, `use_editlist`), fal's Topaz page and API schema, fal's Topaz-generative and SeedVR2 pages, Topaz's model guide and pricing page, Blackmagic's 21.1 press release and Studio page, CineD, Digital Production and Newsshooter on 21.1, YouTube's encoding and AI-disclosure pages, Vimeo's compression guide, EBU R 128 and R 95, Netflix's English guide, General Requirements and **Subtitle Timing Guidelines**, W3C WebVTT, Kdenlive 25.04 notes and subtitle manual, Cologne's DCP sheet, DCP-o-matic, the OFL site, Cinema Tools, Alibaba's Wan 3.0 guide, fal's Seedance 2.5 API, Google's Veo 3.1 docs and Practical-RIFE's `inference_video.py`; every quoted line of both test texts was re-matched. Corrections: on fal's Topaz endpoint **Nyx is a denoise model**, not a precision upscaler, and the words "rebuild detail that is not in the source" could not be found at any primary page, so they are replaced by fal's own "Starlight models use diffusion for restoration and upscaling" (§3, D8-R22); Topaz Video Pro is **$699 a year** (about $58 a month) or $74 a month on a yearly commitment, and Personal's "Limited commercial use" means "Personal and commercial use for orgs under $1M USD annual revenue" (§3); SeedVR2 bills the **upscaled** size (resolved, §3); RIFE's `--fps` switch sets the playback rate and its output is named `<name>_3X_48fps.mp4` (resolved from the code, D8-R12, Rec2); deflicker is listed on Blackmagic's Studio page ("de-flickering") [V]; Wan 3.0 offers no 21:9 and defaults to 1080P; Seedance 2.5 also offers 4:3 and 3:4 and makes audio unless `generate_audio` is off; B2's growth rule reads "never a sickly green" (D8-R32). Added: Netflix's shot-change and gap timing rules as [V] (D8-R49), YouTube's GOP, B-frame, edit-list and 384 kb/s audio recommendations (D8-R56, Rec11), Veo 3.1's documented 24 fps and 8-second limit at 1080p and 4K, a crop formula for any take size (D8-R18), the 16 fps branch for previs rendered at 16 fps (D8-R11), higher source rates (D8-R13), the 4K relink step (Rec5), and seven new conflicts with D3, D9, D12, D18, A4 and D6 (§10).

**Builds on:** A4 §10–§14 (edit and sound fields, stems, loudness); C5 P10, P12, §10.3 (OTIO export, IDs, file names, folders); B2 P6, §8.4–8.5 (style frames, motif colours); C4 R14, Rec5 (16 fps); C1 R23, C2 R16, B1 P3 (2.39:1); B1 §10.4 (in-story footage); D3, D4 Recipe 6, D9, D13 R14. **Leaves to:** D6 (compositing), D12 (card and screen design), D18 (audio description, dubbing).

---

## 0. Where this sits

After C5's checkpoint E (kept takes named `PROJECT_SCENE_SHOT_slug_JOB.ext`), post runs in three parts, each closed by a new checkpoint: **A** assembly to lock (**F: picture lock**); **B** finishing: final frame rate, upscale, composites (D6), grade, grain (**G: grade review**); **C** sound, cards, subtitles, delivery, archive (**H: delivery QC**). At each, a human watches the film once without stopping (A4 §4.3) and answers §7.

---

## 1. Terms (one plain sentence each)

- **Conform**: rebuilding the edit with final media, every take matched to the timeline's frame rate, size and shape.
- **Take**: one generated clip for a shot (C1). **Timeline clip**: the part of a take on the timeline.
- **Relink**: pointing a timeline clip at a different file without changing the edit.
- **Slip**: changing which part of a take a timeline clip uses, keeping its place and length.
- **Handles**: spare frames each side of the used part (A4: 0.75 s, 18 frames at 24 fps).
- **Picture lock**: freezing the order and length of every shot.
- **Transcode**: rewriting a file in another format. **Intermediate codec**: a large, easy-to-edit format (DNxHR, ProRes).
- **CFR / VFR**: constant / variable frame rate (frames of equal / unequal duration).
- **Source rate / timeline rate**: the frame rate a take was made at / the film's frame rate (24 fps).
- **Reinterpret**: playing every frame at a new rate: speed changes, nothing is dropped or invented.
- **Frame interpolation**: inventing in-between frames so motion keeps its real speed at a new rate.
- **Upscaling**: enlarging a picture; AI upscaling invents fine detail, plain resizing does not.
- **Crop**: cutting away edges to reach the delivery shape. **Letterbox / pillarbox**: black bars above and below / at the sides.
- **Grade**: adjusting brightness, contrast and colour. **Grade group**: shots graded together to one look (one B2 colour-script sequence).
- **Style frame**: the approved still defining a sequence's look (B2's key frame).
- **Normalize node**: the first grading step, removing a generator's own look.
- **Gamma**: how bright the middle tones are; **contrast**: the distance between dark and light; **saturation**: how strong colours are.
- **Scopes**: picture graphs: **waveform** (brightness across the frame), **RGB parade** (each colour channel), **vectorscope** (colour direction and strength).
- **LUT (lookup table)**: a file mapping each input colour to an output colour.
- **Grain**: fine random texture over the picture. **Deflicker**: removing frame-to-frame brightness pumping.
- **Stems**: separate dialogue, music and effects mixes. **M&E**: music and effects without dialogue, for dubbing.
- **LUFS / LKFS**: one unit of perceived loudness under two names. **True peak (dBTP)**: the highest level the signal really reaches.
- **Cue**: one subtitle event (start, end, text). **SRT / VTT**: the two common subtitle file formats.
- **SDH**: subtitles for the deaf and hard of hearing, with sound labels and speaker names. **Forced narrative**: a subtitle for everyone translating on-screen text or foreign speech.
- **Card**: a full-screen text shot (C5 type `card`).
- **Master**: the best finished file, source of every delivery file. **Textless**: without titles or subtitles.
- **DCP (Digital Cinema Package)**: the folder of files a cinema server plays.
- **Forced alignment**: software that finds when each word of a known text is spoken in an audio file.
- **GOP (group of pictures)**: in a compressed file, the run of frames from one complete picture to the next; **B-frames** are frames rebuilt from the pictures on both sides. **Fast Start**: the file's index placed at its front so playback can begin before the download ends.
- **Precision upscaler / diffusion upscaler**: a precision model enlarges what is there; a diffusion model (the kind that generates images) redraws detail and can change faces.

---

## 2. Core principles

1. **Records drive the timeline.** A script writes it from shot records and kept-take jobs, because hand relinking hundreds of takes fails silently [J, after C5 R23].
2. **One name per take, one folder per stage**, so a whole stage can be swapped at once [J].
3. **Time before size, size before colour, colour before grain**: rate changes alter the edit, upscaling changes what the grade sees, grain must not be enlarged or re-graded [J].
4. **Spend only on what is locked**, because most generated seconds are thrown away (C1: about four takes per kept take) [J, D13 R14].
5. **Normalize the generator, then grade the story** (B2's sequence look) [J].
6. **Motif colours are the grade's fixed points** (B2 §8.4), checked on every grade group [J].
7. **Words from the script, times from the audio** for subtitles [J].
8. **Keep what cannot be remade**: raw downloads with provenance, lock timeline, stems, breakdown (D4) [J].

---

## 3. Tools on 27 September 2026

| Tool | Role here | Cost | Can an LLM drive it? |
|---|---|---|---|
| **DaVinci Resolve 21.1** (free), released 8 Sep 2026 [V] | Edit, colour, Fairlight audio, titles, subtitles, delivery | Free | Not directly: in 21.1 external scripting, Workflow Integrations and the MCP server need Studio, but "the scripting API remains available from the console in the free edition" [V, Digital Production; Newsshooter: "Advanced scripting now requires DaVinci Resolve Studio"]. So the LLM writes files Resolve imports (OTIO, EDL, SRT, LUT), or a short Python script the user pastes into Resolve's console (Workspace > Console [U menu]). The free edition edits and finishes "up to 60 fps in resolutions as high as Ultra HD 3840 x 2160" [V, Studio page], so a 3840×1608 master fits it; ProRes and DNxHR encoding on every operating system is reported, not checked [U] |
| **Resolve Studio 21.1** | Adds Super Scale, Speed Warp retiming, UltraNR, Magic Mask, voice isolation, Film Look Creator (film looks, "grain, gate weave"), "Python and LUA scripting", up to 32K and 120 fps, "remote scripting API", and Resolve FX for "dirt removal, dust busting and de-flickering" [V, Studio page]; the separate Film Grain effect and audio-to-subtitles reported Studio-only [U]; native MCP server for "Claude, Claude Code and ChatGPT Codex" ("analyze projects, organize media, adjust settings and batch render" [V, Blackmagic release]), Studio-only [V, CineD: "it is Studio only"; the release itself does not say] | $295 once [V] | Yes, via MCP (new: test on a copy) [J] |
| **Kdenlive** (manual 26.08) | Open-source editor; OTIO in and out since 25.04, without effects or transitions [V]; subtitles in (SRT, ASS, VTT, SBV) and out (SRT, ASS); Whisper speech-to-text [V] | Free | Through OTIO and subtitle files |
| **ffmpeg** | Measure, transcode, retime (`minterpolate`), crop, `deflicker`, grain (`noise`), `loudnorm`, `signalstats` [V] | Free | Yes: the LLM runs commands (Claude Code, Cowork, code execution; D1) |
| **Topaz on fal** (`fal-ai/topaz/upscale/video`) | One endpoint, three families: **Precision** ("Proteus fits most footage, Artemis denoises and sharpens degraded sources, Gaia HQ/CG refine rendered content, Gaia 2 handles animation and motion graphics at 2x"), **Denoise** (Nyx) and **Generative**: "Starlight models use diffusion for restoration and upscaling" [V, fal API schema]; default model Proteus, `upscale_factor` default 2, up to 8× and 120 fps; `target_fps` turns on interpolation (Apollo) [V]; a `grain` setting (0–0.1, "Default varies by model") [V]: set it to 0, because grain goes on once, later (D8-R34) [J]; $0.01/s to 720p, $0.02/s to 1080p, $0.08/s above; "Price doubles for 60fps output"; Gaia 2 half price; **default output H.265** (`H264_output` switch) [V] | Per second | Yes (fal MCP, C1 Rec1) |
| **Topaz generative on fal** | Starlight Precise 2.6, HQ, Mini, Sharp: $1.20 per 10 s to 1080p, $2.60 at 4K; Starlight Fast 2: $0.60 / $1.30 (all priced at 30 fps; 60 fps doubles) [V] | Per clip | Yes |
| **SeedVR2 on fal** | One-step **diffusion** restoration and upscaling (ByteDance Seed, arXiv 2506.05301) [V]; $0.001 per megapixel of "width × height × frames", billed on the result: "if your upscaled video is 1920×1080 with 121 frames, the total cost will be $0.25"; commercial use allowed [V]: about $0.04/s at 1920×804, 24 fps [J arithmetic] | Per MP | Yes |
| **Topaz Video** desktop | Upscaling; interpolation models Apollo, Chronos, Aion [V] | Personal $299/yr ($39/month on a yearly commitment, $59 month to month); Pro $699/yr (about $58/month) or $74/month on a yearly commitment; no perpetual licence [V]. Personal's "Limited commercial use" means "Personal and commercial use for orgs under $1M USD annual revenue"; Pro adds "Full commercial use" [V], so Personal covers a small film-maker [J] | No |
| **Practical-RIFE** | Open frame interpolation (model 4.25 recommended, 4.26 newest), MIT licence [V]; `--multi=N` multiplies the frame count; `--fps` only sets the playback rate of the written file (so it changes speed); output named `<name>_<N>X_<fps>fps.mp4` [V, `inference_video.py`] | Free, needs a GPU [J] | Yes (Claude Code) |
| **DCP-o-matic 2.18.50** (8 Sep 2026) | Makes DCPs; open source; Windows, macOS, Linux [V] | Free | Partly |

**Platform trap** [U, secondary]: free Resolve on Linux decodes neither H.264 nor H.265, and no Resolve on Linux reads AAC. AI takes usually arrive as H.264 with AAC; fal's Topaz returns H.265 unless told otherwise, and Seedance 2.5 on fal picks H.264 or H.265 itself (`codec` default `auto`) [V]. Transcoding first (D8-Rec2) fixes this everywhere.

**Other generator facts this file relies on** [V, checked 2026-09-27]: Wan 3.0 (Alibaba Model Studio) outputs "30fps", 480P, 720P and 1080P (default), 2–30 s, MP4, ratios 16:9, 4:3, 1:1, 3:4, 9:16 and adaptive (no 21:9), and "Video URL is valid for 24 hours"; Seedance 2.5 on fal offers 480p, 720p (default) and 1080p, the ratios auto, **21:9**, 16:9, 4:3, 1:1, 3:4 and 9:16, and `generate_audio` on by default ("The cost of video generation is the same regardless"), so switch it off for silent plates; its output frame rate is not stated [U]; Veo 3.1 (Gemini API) makes "24fps" at 720p, 1080p or 4k, 16:9 or 9:16, 4, 6 or 8 s, with 1080p and 4k at 8 s only, SynthID-watermarked. Kling 3.0 has no frame-rate setting in its API and secondary sources report outputs up to 60 fps at 4K [U]: measure every take (Rec2).

---

## 4. Decision rules

### 4.1 Assembly, versions, lock

1. **D8-R1.** If building the first timeline, then have the LLM write `conform_v01.otio` from the shot records rather than relink the animatic, because swapping stills for video is unreliable [J; C5 P10].
2. **D8-R2.** If a shot has no kept take, then leave its previs render or still with a marker `MISSING <job>`, because timing stays testable and gaps visible [J].
3. **D8-R3.** If a take is replaced, then stack the new one above, disable the old one and log it, because the old take is the fallback until lock [J].
4. **D8-R4.** If slipping a take, then place the used frames where the action is, because models rarely start the action exactly 0.75 s in [J].
5. **D8-R5.** If durations are stored in seconds, then cut in whole frames, allowing ±1 frame per shot against A4's plan, because 0.6 s is 14.4 frames [J].
6. **D8-R6.** If picture lock is declared, then export `lock_v1.otio` and `.edl`, have a script write each shot's timing into `finish.edit`, and set scenes `locked: yes`, because subtitles, music, upscaling and runtime read them [J].
7. **D8-R7.** If anything changes after lock, then log it and re-run everything that reads timing (subtitles, music, stems), because downstream files drift silently [J].
8. **D8-R8.** If a join is not a hard cut, then build it in the editor from the cut record (C5 `made_in_edit: yes`), because OTIO does not reliably carry transitions (Kdenlive exports none [V]) [J].

### 4.2 Frame rate

9. **D8-R9.** If choosing the timeline rate, then use exactly 24.000 fps (not 23.976), because Veo 3.1 makes "24fps" [V, Google docs], DCPs take 24 [V, Cologne] and YouTube asks for "the same frame rate it was recorded" [V].
10. **D8-R10.** If a take measures 24 fps, then change only its codec [J].
11. **D8-R11.** If a take is 16 fps and its frame count equals its 24 fps control video's (C4 Route 2), then reinterpret it at 24, because each output frame belongs to one control frame (C4 Rec5) [J]. If instead the control video was itself rendered at 16 fps (C4 R14's other option), then the take already moves at real speed at 16: treat it as free (D8-R12) [J].
12. **D8-R12.** If a take is 16 fps and generated freely, then keep real speed: frame-blend to 24 for editing and, after lock, interpolate (Practical-RIFE, Topaz `target_fps`, Resolve optical flow), because reinterpreting plays it 1.5× too fast [J]. Open Wan 2.1/2.2 A14B and fal's Wan VACE run at 16 fps (C4); hosted **Wan 3.0 outputs 30 fps** [V]; Wan 2.2 TI2V-5B 24 fps [V]. With Practical-RIFE, 16 → 24 is not a whole multiple: run `--multi=3` (16 → 48 fps, real speed kept), then keep every other frame with ffmpeg `-vf fps=24` [J; `--multi` V]. Two of every three final frames are then invented, so check hands and fast moves frame by frame [J arithmetic]. Do not use RIFE's `--fps` switch to reach 24: it only sets the playback rate of the written file, which changes speed [V, `inference_video.py`].
13. **D8-R13.** If a take is faster than 24 fps, then bring it to 24 by dropping frames (`-vf fps=24`), interpolating after lock only where a fast move skips, because dropping keeps real time and lip sync [J]. By source rate [J arithmetic]: **48** keeps exactly every other frame (clean); **30** (Wan 3.0) drops one frame in five; **60** (Kling 3.0 reportedly up to 60 [U]) keeps frames in an uneven 2-3 pattern, which can judder on slow pans; **25** drops one frame a second, which can hitch on smooth pans. If a pan judders or hitches, then interpolate that shot after lock.
14. **D8-R14.** If a take was generated in slow motion to avoid smear (C1), then return it to real time and log `realtime_from_slow`, because B1 bans slow motion in *The Catch* [J].
15. **D8-R15.** If footage exists inside the story (CCTV, tablet, rod camera), then step-print it (12 fps: each frame held twice), never interpolate, because a stutter reads as a recording (B1 rule 22 and §10.4: "about 12 to 15 pictures per second") [J].
16. **D8-R16.** If a take is VFR, then convert it to CFR first (ffmpeg's `fps` filter converts "to specified constant frame rate by duplicating or dropping frames" [V]), because editors mis-time VFR and Vimeo tells uploaders to "always choose a constant frame rate" [V; J].

### 4.3 Size, shape, upscaling, cleanup

17. **D8-R17.** If delivering 2.39:1 (B1's recommendation; the user decides), then edit at 1920×804 and master at 1920×804 or 3840×1608, because both share the shape and fit HD and UHD [J]. A 16:9 source loses 12.8% of its height top and bottom (138 rows each at 1080, 92 at 720): B1's "top and bottom eighths" [J arithmetic].
18. **D8-R18.** If a take was generated at 21:9 (Seedance 2.5 offers it; Wan 3.0 and Veo 3.1 do not [V]), then measure its pixels before cropping, because 21:9 is about 2.33:1 (C1) and sizes differ by route [U]. For any take [J arithmetic]: kept height = width ÷ 2.39, rounded to an even number; rows removed at top and at bottom = (height − kept height) ÷ 2. So 1920×1080 → 1920×804 (138 each), 1280×720 → 1280×536 (92 each), and a hypothetical 2560×1080 21:9 take → 2560×1072 (4 each). If the result is narrower than the master width, then it goes on the upscale list (D8-R20).
19. **D8-R19.** If a head, hand or prop leaves the 2.39 band, then move the clip's position in the timeline and log `crop.offset_y_px`, because reframing is a free edit decision [J].
20. **D8-R20.** If a take is below master size after cropping, then upscale only kept takes after lock: whole takes at 1080p (cheap; name and frame count unchanged, so relinking works), used seconds plus handles only at 4K, because upscaling after lock spends only on kept takes (D13 R14's logic), whole 1080p takes cost little, and trimmed files break source timing [J]. At or above master size, do not upscale. Seedance 2.5 on fal now lists 480p, 720p and 1080p [V]; C1 recorded 480/720p.
21. **D8-R21.** If an upscale would exceed about 2×, then regenerate hero shots at higher resolution, because enlarged small faces get invented features [J].
22. **D8-R22.** If faces are in frame, then use a precision upscaler first (Topaz Proteus, the fal default, or Gaia HQ for rendered content; or Studio's Super Scale [U whether diffusion-based]); try a diffusion upscaler (any Topaz Starlight model, SeedVR2) only if the precision result is too soft, and check every face, ring and hand against the reference pack, because "Starlight models use diffusion for restoration and upscaling" [V, fal] and reviewers warn it "may hallucinate facial details" [U, secondary] [J]. Nyx is a denoiser, not an upscaler choice [V].
23. **D8-R23.** If footage is diegetic and low-resolution, then never AI-upscale it; use a plain resize, because its softness is the story's evidence [J].
24. **D8-R24.** If a shot gets composited elements, then upscale the plate first and render the elements at master size from `camera_track.json` (C4, D6), because upscaling a composite smears thin edges [J].
25. **D8-R25.** If the whole frame pumps in brightness, then deflicker (ffmpeg `deflicker`, a moving average over 2–129 frames, default 5 [V], or Studio's "de-flickering" Resolve FX [V]); if detail crawls ("boils") at steady brightness, then try grain, a new take or C1 R24's still plus push-in, because deflicker only evens brightness [J]. ffmpeg `signalstats` reports `YDIF` (change from the previous frame), so a script can find flicker [V].
26. **D8-R26.** If a take carries a visible platform watermark, then do not crop, blur or paint it out; regenerate on a plan without one or keep it and credit it, because a visible mark means a free tier, and D4 rules 13–14 say free Kling, Luma and ElevenLabs outputs are non-commercial and free Kling outputs must keep the mark or say "generated by Kling AI" (paid Kling members may remove it) [J, applying D4]. Treat a 2.39 crop that removes a corner mark as removal [J]. Invisible provenance (C2PA Content Credentials, SynthID) is never stripped either (D4 principle 8); re-encoding can lose C2PA, so archive the raw download (D8-R60).

### 4.4 Colour

27. **D8-R27.** If all sources are 8-bit BT.709 AI video, then use a Rec.709 Gamma 2.4 timeline with no conversions, converting only HDR or EXR sources (Luma Ray3.2, C1) on their normalize node, because conversions add error [J].
28. **D8-R28.** If grading, then use four levels in order (Resolve's group grading [U]): (1) a **normalize node** per generator per grade group, saved and shared; (2) a per-shot trim starting from Shot Match; (3) the **group look** matched to the style frame; (4) timeline grain and output, because each level answers one question (model, shot, story) [J].
29. **D8-R29.** If takes from different models share a group, then normalize each model on one neutral take: black and white points on the waveform, grey balance on the parade, saturation to the style frame on the vectorscope, gamma last, because models differ mostly in black level, contrast, saturation and cast [J]. A script can list each take's `YLOW`, `YAVG`, `YHIGH` and `SATAVG` (`signalstats` [V]) to find outliers first.
30. **D8-R30.** If using Shot Match ("Shot Match to This Clip", free Resolve [U, secondary]), then treat it as a first guess, because it matches overall statistics and fails when shots contain different things [J].
31. **D8-R31.** If grading a sequence, then compare each shot with the style frame and watch the group as a slideshow, because drift shows only in sequence (C2 rule 26) [J].
32. **D8-R32.** If a motif colour is in frame, then check it against `motif_color_locks`, because motif meanings (B2 §8.4) survive only if the grade keeps them. *The Catch*: red stays a small accent below the fire's saturation (B2 sequence 18, the only saturation 5); yellow is paint, never glowing; Iona's shirt keeps one blue in every generator while other blues are lowered; the grey growth stays near-neutral ("never a sickly green", B2 §8.4) [J applying B2].
33. **D8-R33.** If a light change is in the picture (B2 R21's key-side flip after the BLACK, a light cue), then do not grade it away, because the grade corrects models, not story [J].
34. **D8-R34.** If adding grain, then add one grain for the whole film, once, at timeline level, after upscale and grade, keeping bars and editor blacks clean, because grain unifies generators' textures and hides upscaler smoothness [J]. Free routes: Cinema Tools' free 10 s 4K DCI grain scan in Overlay mode, looped with flips [V], or ffmpeg `noise=alls=<n>:allf=t` at export (strength 0–100; `t` makes the pattern change every frame, as real grain does) [V], starting at D5's "fine" = 4 to 6 on a 1080p picture and judged on one dark and one bright shot at full screen (D5 §8) [J]; keep the grain fine for streaming (D5 R19); in Resolve, Film Look Creator's grain is Studio-only [V] and the separate Film Grain effect is reported Studio-only [U].
35. **D8-R35.** If using a LUT, then use it only to carry a finished look elsewhere, never on raw takes, because a LUT built on one generator does not normalize another [J].
36. **D8-R36.** If the film will be judged on Macs or web players, then check a private 10-second test upload on two devices first, because a Rec.709 file can show a gamma shift in QuickTime and browsers (Resolve's "Rec.709-A" tag addresses this) [U; J].

### 4.5 Sound finish

37. **D8-R37.** If mixing, then route every track to one of three stems (dialogue; music; effects with beds and motifs) feeding the main mix, because A4 requires stems and dubbing needs an M&E (D18) [J].
38. **D8-R38.** If setting loudness, then set it per deliverable, measured over the whole film: web about −14 LUFS, true peak ≤ −1 dBTP (reported for YouTube, not documented [U]); EBU R 128 (v5.0, 2023) −23 LUFS ±0.5 LU, measured over the whole programme, true peak "shall not exceed −1 dBTP" [V]; US broadcast −24 LKFS (A4); Netflix −27 LKFS ±2 LU dialogue-gated (ITU-R BS.1770-1), true peak −2 dBTP [V, two agreeing sources; Netflix's own page now sits behind its partner portal], because platforms turn loud files down [J].
39. **D8-R39.** If the film is quiet by design (*The Catch*: no music or very sparse music, A4 §15 question 1 and D9 `music_policy`, which the user decides; rationed true silence), then mix to the dialogue and let the integrated figure fall (−16 to −18 LUFS is acceptable on the web), because platforms turn loud files down but not quiet ones up [J; U].
40. **D8-R40.** If normalizing with ffmpeg, then run `loudnorm` in two passes (measure, then linear gain) with `I`, `TP` and `LRA` stated, set `LRA` at or above the measured loudness range, add `-ar 48000`, and read the second pass's report to confirm `normalization_type` is `linear`, because its defaults are −24 LUFS, −2 dBTP and LRA 7 [V], linear mode "will revert to dynamic" if the target LRA is below the source's or the gain would push true peak over `TP` [V], dynamic mode upsamples to 192 kHz [V], and dynamic mode reshapes a quiet mix [J]. If it reverts, then lower `I` or raise the ceiling on a limiter in the editor instead.
41. **D8-R41.** If the last sound is a motif pattern, then place the cut to black in the rest between two cycles, let the black carry at least one complete statement, and after it either continue the motif at the same level under the end card and credits or let it recede over two or three more cycles; never let it stop dead, because A4 SND8 and A4 §11 WE3 ("a stopped heartbeat reads as a death") forbid both a mid-pattern cut and an abrupt stop, and A4 open question 2 leaves the choice between continue and recede to the user [J, applying A4].

### 4.6 Titles and cards

42. **D8-R42.** If the script writes a card (`= THE CATCH`, `= THE END`), then make it a `card` shot (C5 E1: SC10-SH990, SC30-SH995), cut in and out with no fade unless written, because A4 T5 adds no device to an all-cut film [J].
43. **D8-R43.** If a card holds text, then hold it for the longer of A4 R8 and B1's rule (2 s plus 0.5 s per word), at least 3 s for a title, because it must be read without pausing [J].
44. **D8-R44.** If choosing a typeface, then use one SIL Open Font License font (free for artwork, posters and logos with no acknowledgement required [V]; video is the same kind of use [J]) for all cards and credits, logged with D4 and D9 [J].
45. **D8-R45.** If placing text, then keep it inside the 2.39 picture's graphics-safe area (5% in from each edge; action-safe 3.5% [V, EBU R 95 v1.1, defined for 16:9; applying it to the 2.39 picture is J]): on 1920×804, text stays inside x 96–1824 and y 40–764 [J arithmetic]; never in bars, because players crop differently [J].
46. **D8-R46.** If crediting, then use D4's AI-use credit line, worded as on platform labels and festival forms (D4 rule 20) [J].

### 4.7 Subtitles

47. **D8-R47.** If writing subtitle text, then copy the exact line from the shot record (A4 `sound.dialogue`), never from recognition, because recognition changes words [J].
48. **D8-R48.** If timing cues, then take each line's times from its placed dialogue file (D3: one file per line), using forced alignment or Whisper only for native model audio, because file positions are exact [J].
49. **D8-R49.** If checking cues, then apply Netflix's English limits by default: ≤42 characters per line, ≤2 lines, ≤20 characters per second (17 for children), ≥5/6 s (20 frames at 24 fps), ≤7 s [V]. Then apply Netflix's timing rules at 24 fps, where "half a second" is 12 frames [V, Subtitle Timing Guidelines]: (a) start within 1–2 frames of the first sound of the line; (b) if nothing follows, end about 12 frames after the speech ends; (c) at least 2 frames between cues, and any gap of 3–11 frames closed to 2; (d) if speech starts on a cut or up to 12 frames after it, start the cue on the cut; (e) if a cue would end within 12 frames before a cut, end it 2 frames before the cut; (f) a cue that crosses a cut ends 2 frames before it or at least 12 frames after it. These keep cues from flashing across cuts.
50. **D8-R50.** If making SDH, then pick one house style, Netflix (brackets, "all lowercase, except for proper nouns", "detailed and descriptive", e.g. `[metal shrieking]` [V]) or BBC (upper case, no brackets [U]), because mixed styles read as error. Default Netflix [J]. In either style, label a sound or name a speaker only when it "cannot be visually identified" (Netflix [V]): the CLACK over black gets a label; a remote click we see pressed does not.
51. **D8-R51.** If a sound is a motif (A4 MOT_, C5 MO-), then store its SDH words once as `sdh_label` and reuse them verbatim, because deaf viewers need the same repeated signal [J]. If the motif has a pattern the payoff depends on, then put the pattern in the label (D18-R7: `[three uneven pump strokes]`, not this file's earlier `[pump thumping]`); the user confirms the wording once (§10 item 11).
52. **D8-R52.** If a speaker is not in the scene at all (narration, voice-over, a voice through a phone, earpiece, radio or screen from another place), then italicize; if only off screen in the same place, then do not, because Netflix says "Only use italics when a speaker is not in the scene(s), not merely off screen, behind a door or out of shot" [V].
53. **D8-R53.** If on-screen text reads backwards, then do not subtitle it in the original language, SDH included, and give it double reading time instead (A4 R8), because its meaning is its orientation and a forward subtitle contradicts the world [J]. Translations add a forced narrative only for plot-pertinent words (Netflix [V]) that read forward on screen [J].
54. **D8-R54.** If speech is in a language the story leaves untranslated, then SDH names the language (Netflix forbids generic placeholders [V]); if it is invented, then describe it plainly; if the story lets the point-of-view character understand a line, then subtitle what she understands, because the subtitle then does the story's job [J].
55. **D8-R55.** If delivering subtitles, then export SRT (comma before milliseconds) and WebVTT (header `WEBVTT`, `HH:MM:SS.mmm`; W3C Candidate Recommendation Draft of 20 May 2026 [V]), with times counted from the delivered file's first frame (timeline timecode minus 01:00:00:00), burning in only where demanded, because burned-in text cannot be removed and players read sidecar times from zero [J].

### 4.8 Delivery and archive

56. **D8-R56.** If uploading to YouTube, then upload MP4 with Fast Start and "No Edit Lists", H.264 High Profile, progressive, 4:2:0, "2 consecutive B frames", "Closed GOP. GOP of half the frame rate" (12 frames at 24 fps), variable bitrate, AAC-LC (or Opus or Eclipsa Audio) 48 kHz at 384 kb/s stereo, BT.709, at the timeline rate, 8 Mbps at 1080p and 35–45 Mbps at 2160p (SDR, 24–30 fps), without baked bars, because "the player automatically adapts itself to the size of the video" [V]. Grain needs 15–20 Mbps at 1080p [J].
57. **D8-R57.** If uploading to Vimeo, then use H.264, H.265 or ProRes 422 HQ, 10–20 Mbps at 1080p or 30–60 at 4K, CFR, AAC-LC 48 kHz 320 kb/s [V].
58. **D8-R58.** If a festival wants a projection copy, then make a DCP with DCP-o-matic: Scope 2048×858 (4K 4096×1716), 24 fps (Cologne also takes 25), stereo or 5.1, subtitles burned in or as "DCI-standard subtitle files (Version File)", because festivals such as Cologne require these, refuse `.srt` and accept no other format for cinema screenings ("We cannot accept ... H.264, ProRes, MP4") [V]; choose SMPTE unless told otherwise; test on a cinema server [J].
59. **D8-R59.** If a festival wants an online screener, then send H.264 MP4 at 1080 (10–20 Mbps), stereo, burning in English subtitles only for non-English dialogue, and follow its own sheet, because calls for entries differ (D4) [J].
60. **D8-R60.** If archiving, then keep texted and textless masters (ProRes 422 HQ or DNxHR HQX 10-bit); stems and mix as WAV 48 kHz 24-bit, same length and start as picture; SRT and VTT; lock OTIO and EDL; the project archive; the breakdown and `manifest.json`; raw downloads with any Content Credentials; licences and the disclosure record, because re-encoding loses embedded provenance (D4) and nothing else rebuilds the film [J].

---

## 5. Recipes (the LLM types; the user clicks)

### D8-Rec1. Set up (20 minutes, free)

1. Ask the LLM: *"Add to the CATCH folder: `media/01_raw`, `02_edit`, `03_final`; `audio/` (dialogue, fx, beds, motifs, music); `graphics/cards`; `subtitles`; `timelines`; `deliver/` (web, festival, dcp, archive). Update `manifest.json`."*
2. Copy kept takes unchanged into `01_raw`; never edit files there.
3. In Resolve: timeline 1920×804, 24 fps, start 01:00:00:00, Rec.709 Gamma 2.4, mismatched resolution set to fill with crop ("Scale full frame with crop" [U menu name]); record these in the film's `finish` block [J; the LLM walks you through your version's menus]. Set the timeline frame rate before importing anything, because Resolve fixes it once media is in the project [U].

### D8-Rec2. Measure and normalize every take (LLM-run)

1. Ask: *"Write and run `measure_takes.py`: ffprobe every file in `media/01_raw` (codec, size, `r_frame_rate`, `avg_frame_rate`, frame count, audio codec) into `finish.measured`, `vfr: yes` where the rates differ. Flag anything not 24 fps CFR or narrower than 1920 pixels after a 2.39 crop."*
2. Ask: *"Write and run `normalize_takes.py`: choose `fps_action` from D8-R10–R16, write `media/02_edit/<same name>.mov` as DNxHR HQ 4:2:2, 24 fps CFR; keep audio as 48 kHz 24-bit PCM only where `model_audio` is `use_native` or `dialogue_only`; log every command."* Commands to expect [V filters; J choices]:
   - codec only: `ffmpeg -i IN.mp4 -map 0:v:0 -c:v dnxhd -profile:v dnxhr_hq -pix_fmt yuv422p -an OUT.mov`
   - reinterpret 16 → 24: add `-vf "setpts=N/(24*TB)" -r 24`
   - drop 25, 30, 48 or 60 → 24: add `-vf fps=24`
   - quick blend 16 → 24 for editing: add `-vf "minterpolate=fps=24:mi_mode=blend"`
   - step print 12 in a 24 fps file: add `-vf "fps=12,fps=24"`
   - VFR to CFR at 24: add `-vf fps=24` (the same filter as the drop)
   - keep planned native audio: replace `-an` with `-map 0:a:0 -c:a pcm_s24le -ar 48000`
   - 16 → 24 at real speed after lock, with RIFE: `python3 inference_video.py --multi=3 --video=IN.mp4` (writes `IN_3X_48fps.mp4` [V, code]; add `--scale=0.5` only for 4K input), then `ffmpeg -i IN_3X_48fps.mp4 -vf fps=24 -c:v dnxhd -profile:v dnxhr_hq -pix_fmt yuv422p -an OUT.mov`

### D8-Rec3. Build the conform timeline from records (LLM-run)

1. Ask: *"Extend `export_otio.py` to write `timelines/conform_v01.otio`: V1 the kept takes from `media/02_edit` in shot order, each starting `handles_s` × 24 frames in and lasting `duration_s` × 24 frames, named by shot ID; V2 the animatic, disabled; A1–A3 dialogue, A4–A6 effects and beds, A7 motifs, A8 music; `MISSING <job>` markers. Also write a CMX 3600 EDL."* (C5 P10 packages.)
2. Resolve: File > Import > Timeline, pick the `.otio` with source-clip import on; relink offline clips to `media/02_edit` from the Media Pool [U, secondary for menus].

### D8-Rec4. Cut to picture lock (hands-on, the longest step)

1. Per shot: slip to the action (D8-R4), trim to A4's cut reasons, keep lip sync. Build split edits, fades and cuts to black from the cut records; black is the editor's black, never generated (B2).
2. Save each version as a new timeline (`CATCH_cut_v007`); lock as `CATCH_LOCK_v1`; export `lock_v1.otio` and `.edl`.
3. Ask: *"Read `lock_v1.otio`, write each shot's `finish.edit`, and list shots that moved by more than 2 frames and scenes that moved by more than 10% from A4's plan."* Checkpoint F.

### D8-Rec5. Final media (LLM-run; about $0.02 per second to 1080p)

1. Ask: *"List locked shots needing interpolation or upscaling; price them on fal Topaz and SeedVR2; show the total before running."*
2. Run on the **whole take** from `01_raw` with a precision model first (Proteus; D8-R22), `upscale_factor` set to reach master width (1.5 for 1280 → 1920), `grain: 0`, `H264_output` on, and `target_fps: 24` only where interpolation is planned; normalize as in Rec2 into `media/03_final` with the **same name and frame count**. Copy untouched takes from `02_edit`. The request the LLM sends looks like this [V parameter names; J values]: `{"video_url": "<take>", "model": "Proteus", "upscale_factor": 1.5, "grain": 0, "H264_output": true}`.
   - **At 4K (used seconds plus handles only, D8-R20):** the upscaled file is shorter than the take, so relinking by name fails. Name it `<take>_4k.mov` and cut it to start 18 frames (the handle) before the used part, or at the take's first frame if fewer than 18 frames come before it. Then have the LLM point the OTIO clip at the new file with its source range starting at the handle length actually kept (normally frame 18), and check the first and last frames against the lock by eye [J].
3. Check faces, rings and hands against the reference pack; a failed upscale falls back to plain resize.
4. Ask the LLM to rewrite `lock_v1.otio`'s paths to `03_final` and import it as `CATCH_FINAL_v1` (safer than hand relinking) [J]. D6 composites return to `03_final` under the same names.

### D8-Rec6. The 2.39 frame

Fill scaling centre-crops 16:9 takes. Scrub with the safe-area overlay; where something leaves the band, move the clip and log `crop.offset_y_px`. In-story footage of another shape is fitted inside the frame (§9.2).

### D8-Rec7. Grade by groups (hands-on with LLM coaching)

1. Ask: *"From B2's colour script, list grade groups, scene ranges, style frames and motif colour locks. Run `signalstats` on every take in GG-04 and list takes whose `YLOW`, `YAVG`, `YHIGH` or `SATAVG` sit far from the group median."* Starting thresholds [J]: flag a take whose average `YLOW`, `YAVG` or `YHIGH` differs from the group median by more than 10 (on the 0–255 scale), or whose `SATAVG` differs by more than 20%; flagged takes get their normalize node checked first. The per-frame command it will run [V filter; J choice of fields]: `ffprobe -v error -f lavfi -i "movie=IN.mov,signalstats" -show_entries frame_tags=lavfi.signalstats.YLOW,lavfi.signalstats.YAVG,lavfi.signalstats.YHIGH,lavfi.signalstats.SATAVG,lavfi.signalstats.YDIF -of csv=p=0`. `YLOW` and `YHIGH` are the 10% and 90% brightness points (0–255), `SATAVG` the average saturation, `YDIF` the change from the previous frame (a jump in it is flicker).
2. Load the style frame as a comparison still. Per generator: build node 1 on its most neutral take against the style frame (D8-R29), save it as a shared node `NORM_<MODEL>_<GROUP>`, apply it to that model's takes.
3. Node 2 per shot: Shot Match to the group's anchor, then trim by eye. Put the shots in one group and build the sequence look at its post-clip level.
4. Run the §7 motif questions and B2 R24. Timeline level: grain only. Checkpoint G: each group as a slideshow, then the film.

### D8-Rec8. Sound finish in Fairlight

1. Tracks arrive sorted from Rec3. Create stem buses DIA, FX, MUS and route tracks to them, buses to main [J; menus U].
2. Balance dialogue first, then beds, sync effects, motifs, any music; keep A4's ruptures and silences exact.
3. Loudness meter: choose the deliverable's standard, reset at the first frame, play the whole film, read Integrated and True Peak [U, secondary]. Adjust buses; limiter on main at the true-peak ceiling.
4. Render main mix and each stem as WAV 48 kHz 24-bit from the first frame; M&E is the mix with DIA muted.
5. Without Fairlight, ask: *"Measure the mix with loudnorm, then apply the measured values with `linear=true`, confirm the second pass stayed linear (D8-R40), and report before and after."* The two commands [V options; J values; LRA 20 chosen to stay above a quiet film's range]:
   - pass 1: `ffmpeg -i CATCH_mix.wav -af loudnorm=I=-14:TP=-1:LRA=20:print_format=json -f null -`
   - pass 2: `ffmpeg -i CATCH_mix.wav -af loudnorm=I=-14:TP=-1:LRA=20:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true:print_format=json -ar 48000 -c:a pcm_s24le CATCH_mix_web.wav`
   For *The Catch*, change `I=-14` to the level D8-R39 accepts if the report says the pass fell back to dynamic.

### D8-Rec9. Cards and credits

1. Ask: *"For every `card` shot, fill `card_spec` from its source line and D8-R42–R46, and render each as a 1920×804 PNG (and 3840×1608 if mastering at 4K), off-white on pure black, centred in the graphics-safe area."* (D12 designs the typography.)
2. Place PNGs as the card shots; cut in and out.
3. Credits: cards of 3–4 names, about 3 s each, or a roll moving a whole number of pixels per frame (2–4 at 1080) to avoid judder [J].

### D8-Rec10. Subtitles from the breakdown

1. Ask: *"From `lock_v1.otio` and the shot records, make one cue per dialogue line with the exact text from `sound.dialogue`, timed to its placed dialogue file (forced-alignment times where it came from native audio). Apply D8-R49, split at phrase boundaries, italicize per D8-R52. Write `subtitles/CATCH_en.srt` and `.vtt`."*
2. SDH: *"Add cues for every `sync_fx`, `offscreen` and motif entry marked `sdh: yes` (motifs use `sdh_label` verbatim) and speaker labels where unclear. Write `CATCH_en_sdh.srt` and `.vtt`."*
3. *"List every cue breaking D8-R49."* Fix; import into the editor; watch once with sound off, once on.

### D8-Rec11. Deliver and archive

1. Render the master (ProRes 422 HQ or DNxHR HQX, master size, 24 fps, PCM mix) and the textless master.
2. Ask: *"Make `deliver/web/CATCH_web.mp4` from the master: H.264 high profile, 4:2:0, BT.709 tags, 18 Mbps, 2 B-frames, GOP 12, AAC-LC 48 kHz 384 kb/s, fast start, no edit lists, web mix. Check with ffprobe that every value matches `deliverables.web_upload`."* Repeat per deliverable. The command to expect [J values; ffmpeg options V in the FFmpeg manuals; x264's GOP is closed by default]:
   `ffmpeg -i CATCH_master.mov -i CATCH_mix_web.wav -map 0:v:0 -map 1:a:0 -c:v libx264 -profile:v high -pix_fmt yuv420p -b:v 18M -maxrate 20M -bufsize 36M -bf 2 -g 12 -r 24 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 384k -ar 48000 -movflags +faststart -use_editlist 0 deliver/web/CATCH_web.mp4`
   One file serves YouTube (384 kb/s audio recommended) and Vimeo (320 kb/s recommended, 10–20 Mbps at 1080p) [V; J that one file suits both].
   The check: `ffprobe -v error -show_entries stream=codec_name,profile,width,height,pix_fmt,r_frame_rate,color_primaries,color_transfer,color_space,sample_rate,bit_rate -of json deliver/web/CATCH_web.mp4`.
3. DCP: DCP-o-matic, Scope container, 24 fps, subtitles per the festival sheet; test on a cinema server. Upload privately first (D8-R36, R38); set the platform AI label (YouTube: Attributes > "AI use" [V]).
4. Ask: *"Build `deliver/archive/` per D8-R60 with a checksum list, and add every file to `manifest.json`."* Checkpoint H.

### D8-Rec12. The Kdenlive route (differences only)

Import the OTIO (no effects or transitions carried [V]); build joins there; subtitles on its subtitle track (Whisper for timing only) [V]; grade with its colour effects and scopes, carrying the group look as a `.cube` LUT [U]; render a ProRes or DNxHR master; the LLM makes delivery files with ffmpeg. No Linux codec trap, no group grading [J].

---

## 6. Fields this subject adds to the breakdown

Enums lowercase `snake_case`, empty `"none"` (C5 R29). Authority per C5: **derived** = script only; **authored** = human or LLM with `decided_by`.

| Level | Field | Meaning | Allowed values / example | Authority |
|---|---|---|---|---|
| film | `finish.timeline_fps` | Timeline rate | `24` \| `25` | authored |
| film | `finish.working_resolution`, `finish.master_resolution` | Edit size; master size | `1920x804`; `1920x804` \| `3840x1608` | authored |
| film | `finish.editor` | Editing program | `resolve_free` \| `resolve_studio` \| `kdenlive` \| `other` | authored |
| film | `finish.output_color_tag` | Tag in delivery files | `rec709` \| `rec709a` | authored |
| film | `finish.grain` | The one film grain | {`method`: `grain_scan_overlay` \| `ffmpeg_noise` \| `resolve_film_grain` \| `none`, `strength`} | authored |
| film | `finish.sdh_style` | SDH house style | `netflix` \| `bbc` | authored |
| film | `finish.picture_lock` | Lock record | {`version`, `date`, `otio_file`} | derived |
| film | `deliverables[]` | Files to make | {`id`, `kind`: `web_upload` \| `festival_screener` \| `dcp` \| `archive_master` \| `textless_master` \| `stems` \| `subtitles`, `container`, `video_codec`, `resolution`, `fps`, `bitrate_mbps`, `audio`, `loudness_target_lufs`, `true_peak_dbtp`, `subtitles_mode`: `burned_in` \| `sidecar_srt` \| `sidecar_vtt` \| `dcp_xml` \| `none`, `status`} | authored |
| film | `credits_spec` | End credits | {`type`: `cards` \| `roll`, `seconds_per_card` or `px_per_frame`, `font`}; credit line from D4 | authored |
| scene | `grade_group` | Look the scene is graded in | `GG-04` (B2 sequence 4); in-story footage uses its look key, e.g. `LK-CCTV` | authored |
| scene | `style_frame` | Approved still | path (B2 `key_frame_ref`) | authored |
| scene | `motif_color_locks[]` | Colours the grade keeps | {`motif_id`, `colour`, `rule`: `never_glow` \| `hue_fixed` \| `max_saturation_below_peak` \| `desaturate_others` \| `near_neutral`, `check`: yes/no question} | authored |
| scene | `edit_status` | Progress | `assembly` \| `rough` \| `fine` \| `locked` | authored |
| shot | `finish.measured` | What the take is | {`fps`, `width`, `height`, `codec`, `frame_count`, `vfr`} | derived |
| shot | `finish.fps_action` | Rate handling | `none` \| `reinterpret_24` \| `drop_frames` \| `frame_blend` \| `optical_flow` \| `ai_interpolate` \| `step_print_12` \| `step_print_15` \| `realtime_from_slow` | authored |
| shot | `finish.crop` | Shape handling | {`mode`: `none` \| `center` \| `offset` \| `fit_pillarbox`, `offset_y_px`} | authored |
| shot | `finish.scale_action`, `finish.upscale_tool` | Size handling | `none` \| `plain_resize` \| `ai_upscale`; exact tool and model | authored |
| shot | `finish.cleanup` | Repair | `none` \| `deflicker` \| `denoise` \| `deflicker_denoise` | authored |
| shot | `finish.flip` | Mirror edit operation (C1 `mirror_flip`) | `yes` \| `no` | derived |
| shot | `finish.normalize_node`, `finish.match_to` | Grade level 1; anchor shot | `NORM_SEEDANCE25_GG04`; shot ID | authored |
| shot | `finish.conform_notes` | One or two lines for the editor | text | authored |
| shot | `finish.conform_status` | Progress | `raw` \| `normalized` \| `cut` \| `locked` \| `final_media` \| `composited` \| `graded` \| `delivered` | derived |
| shot | `finish.edit` | Lock timing | {`record_in_tc`, `record_out_tc`, `source_in_frame`, `frame_count`} | derived |
| subtitle cue | `cue_id`, `shot`, `kind`, `text`, `start_tc`, `end_tc`, `italic`, `position`, `source_ref`, `track` | One cue | `SUB-0042`; `dialogue` \| `sdh_sound` \| `sdh_speaker` \| `forced_narrative` \| `lyric`; `bottom` \| `top`; line number or record ID; `standard` \| `sdh` \| `both` | text extracted, times derived |
| shot (`card`) | `card_spec` | A card | {`text` (exact), `font`, `font_licence`, `cap_height_pct`, `colour`, `background`, `hold_frames`, `in`: `cut` \| `fade_<frames>`, `out`, `sound`: `none` \| `room_tone` \| `motif_continues` \| `motif_recedes`, `safe_area`: `graphics_safe`} | text extracted, rest authored |
| motif | `sdh_label` | Fixed SDH words | `[three uneven pump strokes]` (D18-R7; user confirms) | authored |

Example shot block:

```json
"finish": {
  "measured": {"fps": 16, "width": 1280, "height": 720, "codec": "h264", "frame_count": 81, "vfr": "no"},
  "fps_action": "reinterpret_24",
  "crop": {"mode": "offset", "offset_y_px": -20},
  "scale_action": "ai_upscale", "upscale_tool": "fal-ai/topaz/upscale/video, Proteus",
  "cleanup": "none", "flip": "no",
  "normalize_node": "NORM_WANVACE_GG04", "match_to": "SC06-SH030",
  "conform_notes": "Wan VACE, frame-matched to previs: reinterpret.",
  "conform_status": "final_media",
  "edit": {"record_in_tc": "01:04:12:03", "record_out_tc": "01:04:12:23", "source_in_frame": 12, "frame_count": 20}
}
```

**Validator additions** [J]: every locked shot has `finish.measured`; `fps_action` fits `measured.fps` (24 → `none`; 16 → `reinterpret_24` only if the job has a control video of equal frame count); no `ai_upscale` where `grade_group` is an in-story look key; every `card` shot's `text` matches its source line; every cue passes D8-R49; each scene's summed `frame_count` is within 10% of target (C5 R27); every deliverable has a `status`.

---

## 7. Checklists

**Per take**: measured • CFR at 24 fps or a logged `fps_action` • audio only where planned • name unchanged.

**Checkpoint F, lock**: every cut has a reason (A4) • no `MISSING` markers, or each accepted as a still • reading times met • A4's ruptures, blacks and silences exact • lock OTIO/EDL exported, `finish.edit` written.

**Per final take**: same name and frame count as in `02_edit` • faces match the reference pack • no new artifacts or warping • in-story footage not AI-upscaled.

**Checkpoint G, per grade group** (yes/no):
- Does every shot sit with the style frame side by side?
- Do takes from different generators look like one camera in a slideshow?
- Is every red accent smaller and less saturated than the fire will be?
- Does the yellow line look painted, not glowing?
- Is Iona's shirt one blue everywhere, other blues quieter?
- Is the grey growth grey, with no green?
- Are B2's written light changes still visible?
- Is dark skin rich, never grey or ashy?
- Is grain applied once, at timeline level, with clean blacks?

**Checkpoint H, delivery**: ffprobe values match each deliverable • loudness measured on the actual file • subtitles pass D8-R49 on the final cut • cards and credits exact, D4 line present • AI label set • private upload watched on phone and computer • archive checksummed.

---

## 8. Failure modes

| Sign | Cause | Fix |
|---|---|---|
| Media offline or no picture in free Resolve on Linux | H.264/H.265 or AAC | Rec2 transcode |
| A Wan shot's action is too fast | Free 16 fps take reinterpreted | D8-R12 |
| A control-video Wan shot is 1.5× long | Frame-matched output left at 16 fps | D8-R11 |
| Skip every fifth frame in a pan | 30 → 24 drop | Interpolate that shot (D8-R13) |
| Rubbery hands after a retime | Interpolation over fast motion | Drop frames or new take |
| Heads cut off at the top | Centre crop of a 16:9 take | D8-R19; prompt the safe band next time (B1) |
| Relink fails after upscaling | Name, frame count or extension changed | D8-R20; Rec5 step 4 |
| A face changes after upscaling | Generative detail | D8-R22 |
| Upscaled file will not import | fal Topaz's default H.265 | H.264 output, then Rec2 |
| Two models never match | Look graded before normalizing | D8-R28, R29 |
| Beads or tag compete with the fire | Group look raised saturation | D8-R32 |
| Fine in Resolve, washed out on a Mac | Gamma tagging | D8-R36 |
| Grain soft or uneven | Added before upscale or grade | D8-R34 |
| Loudness "normalized" but wrong | `loudnorm` defaults | D8-R40 |
| Last pump stroke cut off | Black placed mid-pattern | D8-R41 |
| "Io." subtitle flashes | Timed to speech length | 20-frame minimum |
| Festival rejects the subtitles | `.srt` with a DCP | D8-R58 |
| Subtitles appear an hour late or never | Times copied from timeline timecode (01:00:00:00 start) | D8-R55: subtract the start |
| `loudnorm` result pumps or sounds squashed | Linear pass fell back to dynamic | D8-R40: lower `I`, raise `LRA` |
| The film seems to end on a death | Pump stopped dead after the last cycle | D8-R41: continue or recede |
| Subtitles blink on and off around cuts | Cues end a few frames either side of a shot change | D8-R49 (c)–(f) |
| A 4K upscale plays the wrong frames | Trimmed file relinked as if it were the whole take | Rec5, the 4K step |
| A Kling or Wan 3.0 pan judders after conform | 60 or 30 → 24 frame drop | D8-R13: interpolate that shot after lock |
| Upscaled shots look grainier than their neighbours | Topaz `grain` left at the model default | Rec5: `grain: 0` |

---

## 9. Worked examples

### 9.1 *The Catch*, SC06: conforming the fall

**Plan in.** A4 WE1: about 36 shots in about 50 s (ASL about 1.4 s, 34 frames), from "The opening reaches them." (l.228) to "This time they hear it land." (l.298). Grade group `GG-04`, B2 colour-script sequence 4 (paraphrased: cage descent, fall, turn, catch; value 2, saturation 2, cool; brick and grid; accents the red blood beads and the yellow stripe; extreme, rhythmic contrast; out on the BLACK, then the same light arriving from the other direction). Handles 18 frames.

| Family | A4 rows | Made with | Expect | Conform |
|---|---|---|---|---|
| Fall wides and mediums | 3, 8, 9, 19–23, 31–32 | Seedance 2.5, clay reference, 720p, no audio (C1 Ex2) | 1280×720 (fps [U]) | 1280×536 band; after lock upscale ×1.5 (fal Topaz, about $0.02/s [V]) |
| Grid points of view on the stripe | 11, 12, 15 | Wan VACE depth from previs, frame-matched | 16 fps, 81 frames padded (C4) | `reinterpret_24`; upscale |
| Faces and lines: "Io." (l.251), "Push." (l.278) | 4, 13, 16, 18, 27 | Kling 3.0, voice first (C1 R1, D3) | 1080p, 24, 30 or up to 60 fps [U] | If above 24: `drop_frames` (keeps sync, D8-R13); crop only |
| Inserts: STOP, fingers, arm on sill, boot | 2, 14, 29–30, 33 | Stills plus push-in or any model | varies | The arm-on-sill insert matches sc2's grade as well as its lens (A4) |
| Blood beads: "Jude's blood lifts off the steel in round red beads and hangs in the air between them, turning." (l.244) | 10, and every shot with `PR-BLOOD-BEADS.S01` (C5 E3) | Plates without blood; Blender beads (D6) | Beads at 1920×804 | D8-R24: upscale plate first |
| Black: "A hard metal CLACK." (l.259) / "BLACK. A dark with nothing in it. One instant." (l.261) | 17 | Editor black | 10 frames | CLACK on frame 1, then true silence (A4) |

**Steps.**
1. Rec2 flags the under-width Seedance and Wan takes, the 16 fps Wan takes and any 30 fps Kling take; Rec3 writes 36 timeline clips named by shot ID, beds and the CLACK as A4's fixed assets.
2. Rec4: slip each fall take so its used 14–48 frames sit in its cleanest seconds (A4: free fall under 3 s). Row 13 (Eli, 60 frames) stays the fall's longest; row 36 (120 frames) L-cuts into SC07. Lock.
3. Rows 8 and 19 share a framing with the direction reversed: give them the same `offset_y_px` so the repeat reads (A4, B1).
4. Grade: one normalize node per family (`NORM_SEEDANCE25_GG04`, `NORM_WANVACE_GG04`, `NORM_KLING30_GG04`); Shot Match rows 19–21 to the shots they repeat. Do not correct the key light arriving from the other side after row 17 (B2 R21, D8-R33).
5. Locks for GG-04: beads and the row-35 tag small and below the fire's saturation; the yellow stripe painted, never glowing as it grows in rows 12 and 15 ("Through the grid, the yellow stripe. Coming.", l.248); Iona's shirt one blue across all families; the bright sill brighter than the brick, never glowing.
6. Grain at timeline level; the 10 black frames stay pure black.

`conform_notes`, row 17: *"Editor black, 10 frames, no grain. CLACK (A7) on frame 1; all other tracks silent frames 2–10. In on the eyelids closing, out on 'Her eyes open.'"*

### 9.2 *The Catch*, SC13: the security playback inside 2.39

**Source.** "A monitor turned to face the glass. Security footage, paused: a camera above the top gate, looking straight down the shaft. The cage is a small bright box with three small people in it." (l.674); "On the floor of the cage, where his hand was, a flat black puck is clipped to the grid." (l.740); "Iona pauses the recording with the remote. Looks at her brother. Not at Jude." (l.742).

**Design in**: `SC13-SH200` (C5 E4) with B1 §10.4's CCTV spec (4:3, low resolution, 12–15 fps, timestamp, one master take, mirrored in phase B) and A4 WE2's silent, real-time playback with a 2.5 s freeze on the click (silent is A4's choice; A4 §15 question 3 leaves "tinny sound" open for the user).

**Conform.**
1. **One master take** from the top-gate previs (C5 E4); every excerpt in SC13, SC16 and SC17 is cut from it.
2. **Rate:** `step_print_12` (even cadence inside B1's range) [J]; the timestamp (D6, D12) ticks in real seconds.
3. **Size:** master made at 640×480 [J]; full-screen insert `fit_pillarbox`: plain resize to 1072×804, centred, 424 pixels each side [arithmetic]. Fill the sides with the monitor's dark bezel, not flat bars [J]. Never AI-upscale (D8-R23).
4. **Grade group** `LK-CCTV`: desaturated, cage lights allowed to flare [J].
5. **The freeze:** export the real frozen frame of the 12 fps master as `CATCH_SC13_SH200_cctv-freeze_still.png`; 60 frames full screen, then corner-pinned on the background monitor until "Lets the recording run." (D6).
6. **Mirroring:** flipped with the phase-B world; do not fix it (B1).
7. **Validator:** replayed beats `SC06-B08`/`B09` exist; the puck is `PR-PUCK.S02`, not `.S03` (C5 E4); `fps_action` is `step_print_12`; no `ai_upscale`.

**Subtitles.** The footage is silent, so no SDH inside it; the seen remote click needs no label [J]; the timestamp gets no forced narrative. "On the screen the upside-down cage falls empty. All three of them flinch at the same moment." (l.826) gets no crash label, because A4 adds no crash.

### 9.3 *The Catch*: title, end card, credits

**SC10-SH990.** "Nobody leave this room." (l.484), "> CUT TO BLACK." (l.486), "= THE CATCH" (l.488).

```json
"card_spec": {"text": "THE CATCH", "font": "<one OFL typeface chosen in D12>", "font_licence": "OFL-1.1",
  "cap_height_pct": 6, "colour": "off-white", "background": "black", "hold_frames": 72,
  "in": "cut", "out": "cut", "sound": "none", "safe_area": "graphics_safe"}
```

Timing [J]: 24 frames of black after Saye's line; the card for 72 frames (B1: 2 s + 2 words × 0.5 s; A4 R8 about 1.7 s); 12 frames of black; hard cut into SC11. Sound [J]: the kitchen's room tone stops with the picture (A4: a hard sound change), silence under black and card. This black is script-made, outside A4's device budget.

**SC30-SH990 and SH995.** "The pump goes on." (l.1846), "> CUT TO BLACK." (l.1848), "Three uneven strokes in the dark." (l.1850), "= THE END" (l.1852). The cut to black falls in the rest between cycles (A4 WE3). `SH990` is black carrying one complete cycle, cut out on the rest after the third stroke's decay (D8-R41): about 60–84 frames with A4's example signature [J]. SDH: the pump's `sdh_label` verbatim (D8-R51; `[three uneven pump strokes]` if the user accepts D18-R7) across the cycle. `SH995`: "THE END", same spec, 72 frames, **except `sound`**: the pump does not stop at the card. Either it goes on at the same level under the card and the credits (`"sound": "motif_continues"`), or it recedes over two or three more cycles (`"sound": "motif_recedes"`), because A4 SND8 and A4 §11 WE3 forbid an abrupt stop ("a stopped heartbeat reads as a death"); which one is A4's open question 2, for the user. SDH under the card: `[pump strokes continue]` or `[pump strokes fade]`, placed at the bottom of the picture below the card text [J].

**Credits.** Cards of 3–4 names, 72 frames each; the last carries D4's credit line and D9's CC BY lines. YouTube "AI use": Yes, since the film shows "a realistic scene that didn't actually occur" [V].

### 9.4 *The Catch*: subtitles and SDH (Netflix style)

Sample of `CATCH_en_sdh.srt` (times illustrative; real ones come from the lock). Subtitle times count from the first frame of the delivered file, so the LLM subtracts the timeline start (01:00:00:00) from every record timecode [J]: a line at timeline 01:04:02:00 is `00:04:02,000` in the file.

```
41
00:04:02,000 --> 00:04:03,917
[door crashes open above]
[gunshots]

42
00:04:04,000 --> 00:04:04,833
[softly] Oh.

57
00:04:13,042 --> 00:04:14,500
[metal shrieking above]

63
00:04:20,208 --> 00:04:21,042
Io.

66
00:04:23,375 --> 00:04:24,292
[metal clacks]
```

The same cues in `CATCH_en_sdh.vtt` (header line, blank line, full stop before milliseconds; cue numbers optional) [V, W3C WebVTT]:

```
WEBVTT

41
00:04:02.000 --> 00:04:03.917
[door crashes open above]
[gunshots]

42
00:04:04.000 --> 00:04:04.833
[softly] Oh.

66
00:04:23.375 --> 00:04:24.292
[metal clacks]
```

- "Far above, the stair door gives with a crash. Someone KICKS the top gate open and FIRES down through the roof." (l.216): the capitals are the writer's sound marks (A4 §5.1), relabelled in house style; "(quite softly)" (l.219) becomes `[softly]`, in SDH only.
- "one long METAL SHRIEK" (l.238) is A4's J-cut under row 6, so its cue starts with the sound, before the faces turn up. "Io." (l.251): 3 characters, still 20 frames.
- "A hard metal CLACK." (l.259) lands on the first of 10 black frames; its cue runs 22 frames, over the black and 12 frames into "Her eyes open.", because a 20-frame cue would end 10 frames after that cut, inside D8-R49's 12-frame zone [J]. No cue marks the silence after it: the black and the text leaving are the signal [J].
- JUDE (V.O.) "(in her ear)" (l.93–94): Jude is elsewhere, so italic, `[over earpiece]` the first time (D8-R52).
- **Backwards text** (D8-R53): "Every letter is backwards." (l.327), the green sign (l.331), "OSTREL, stitched on it in blue. Backwards." (l.496) and "Her own name, printed backwards." (l.500): no subtitle, no forced narrative. "On the wall above Saye: RECEIVING." (l.1620) with "Iona looks at it. Reads it again." (l.1622) reads forward on screen: translations may add a forced narrative; English needs only reading time.
- **Motif labels** (D8-R51): the pump carries one `sdh_label` (D18-R7's `[three uneven pump strokes]` unless the user picks other words) from its first statement, "From inside it, a PUMP: three strokes, not quite even." (SC15, l.852), to the end; the CLICK/CLACK family is always `[metal clacks]`.

### 9.5 *The Long Places*, chapter VII

**Narration.** The keeper's letter, a voice-over candidate (A4 WE4), is italic in every version (Netflix: always italicize narration [V]). "When they are on the road, the flame leans toward the deep rooms, the way a plant leans at a window, and there is no draft to blame, and you do not go looking for one." (l.549; 167 characters) splits at phrase boundaries into three cues: "When they are on the road, / the flame leans toward the deep rooms," (65 characters, at least 3.3 s at 20 cps); "the way a plant leans at a window, / and there is no draft to blame," (66, 3.3 s); "and you do not go looking for one." (34, 1.7 s). If the voice is faster, cues trail it slightly rather than cut the author's words [J].

**Speech no one knows.** The elder speaks "in a speech that was no language any of them had", and Nilay carries up "*the little sun that doesn't burn.*" (l.601). The subtitle shows what she understands, not italic (the speaker is in the room; D8-R54); SDH first adds `[speaking an unknown language]`. The woman's "word of three syllables, the middle one long" (l.603) stays untranslated because the story says "It did not sit in the mouth."; SDH: `[says a three-syllable word]`. Netflix forbids `[speaking foreign language]` for real languages [V]; describing a language the story itself leaves unknown is this file's judgment [J]. "Is the fire mountain awake?" (l.607) is subtitled in full.

**In-story footage.** The "forty seconds of image on Márton's laptop" in which "the picture closed like an eye" (l.581): one master take, look key `LK-RODCAM`, plain resize, step-printed, corner-pinned on the laptop (D6). The recovered frame ("Recovery ground all night and handed up one frame in the morning", l.619) is a real still, never interpolated or AI-upscaled (D8-R23). Chapter cards ("VII. The Breach") are D2's call; if kept, each is a `card` shot.

---

## 10. Conflicts and open questions

1. **Delivery ratio** (needs the user): 2.39 assumed; at 1.85 the rules hold, with DCI Flat 1998×1080 in the DCP.
2. **Upscaling unit** vs D13: resolved in the text. D13 R14 and §6.7 now upscale whole kept takes to 1080p and only used seconds plus handles to 4K, as D8-R20 does. One number still differs: D13 prices v0 whole takes at runtime × 1.5, while for 1–2 s shots cut from 4–8 s takes (A4: duration plus two 0.75 s handles, rounded up to a length the model offers; Veo 3.1 at 1080p makes only 8 s [V]) the upscaled seconds are 2–4× runtime [J arithmetic]. For fast scenes such as SC06 (ASL 1.4 s), price at 3× runtime; at $0.02/s this stays small.
3. **16 fps** (C4 R14 vs Rec5): resolved by frame count (D8-R11, R12); C4 should say the same.
4. **SDH style:** Netflix by default; the brief's `[METAL SHRIEK]` capitals match neither style exactly. The user picks once; D18 extends SDH, audio description and translation.
5. **Sound under the title card** (proposed: silence) and **the pump after the last cycle** (A4 open question 2: continue under the credits or recede over two or three cycles) need the user. The earlier draft of this file let the pump end with SH990 and ran THE END silent, which A4 SND8 forbids; corrected in D8-R41 and §9.3.
6. **Web loudness:** −14 LUFS for YouTube is reported, not documented [U]; *The Catch* may sit quieter (D8-R39).
7. **Unverified:** Kling 3.0 and Seedance 2.5 frame rates; free Resolve's Film Grain effect, optical flow, Shot Match and group grading; free Resolve's ProRes and DNxHR encoding on Windows and Linux; Linux codec limits; menu names; whether Super Scale is diffusion-based; YouTube's −14 LUFS; BBC style. Resolved in the second pass: SeedVR2 bills output pixels; RIFE's `--fps` changes speed; deflicker is a Studio feature; free Resolve keeps console scripting. Measure takes rather than trust documented rates.
8. **Studio or free:** Studio ($295) pays if the film needs Super Scale, Speed Warp, deflicker, Film Look Creator or Film Grain in Resolve, or Claude driving Resolve over MCP or external scripts (both Studio-only in 21.1 [V]); otherwise the free route costs only fal seconds, and the LLM reaches free Resolve through import files and pasted console scripts [J].
9. **Checkpoints F, G, H** extend C5's A–E; C5 and D13's week-by-week schedule should name them, or map them to C5's last checkpoint.
10. **Upscaler vocabulary** in other files: C1 and D13 speak of "Topaz" as one thing. The fal endpoint mixes precision (Proteus, Artemis, Gaia), denoise (Nyx) and diffusion (Starlight) models; a breakdown should always name the model (`finish.upscale_tool`), because the face risk differs.
11. **Pump SDH label** vs D18-R7: D18 puts the pattern in the label, `[three uneven pump strokes]`, because the payoff depends on recognising "three strokes, not quite even" (l.852); this file first used `[pump thumping]`. This pass adopts D18's wording as the default in D8-R51, §6 and §9; the user confirms once.
12. **Title-card hold** vs D9: D9's `sparse` music option spots its cue "card held 4 s"; D8-R43 and §9.3 hold "THE CATCH" 72 frames (3 s). If the user picks `sparse`, then the card may run 96 frames so the cue can breathe; otherwise 72. One number goes in `card_spec.hold_frames`.
13. **Sound under the title card** vs D9: D9's `sparse` option puts its one music cue under the black and the card; this file proposes silence. Both depend on D9 `music_policy` (A4 §15 question 1), for the user.
14. **Pump under the credits** vs D9: D9 rule 4b lets an `end_credits_only` cue enter only after the pump has receded, never under it (B4 M10: "Never put score over it"). So `motif_continues` under the credits (D8-R41) rules out a credits cue; `motif_recedes` allows one after the last cycle.
15. **Free Resolve scripting** vs D12: D12 rule 25 says "free Resolve 21.1 has no Python scripting [V via D8]"; D8 says console scripting remains free ("The scripting API remains available from the console in the free edition", Digital Production [V]) while external scripting, Workflow Integrations and the MCP server need Studio. D12's reason should be corrected; its rule (PNG cards placed in Resolve) still stands.
16. **Mirrored reading time** citation in D12: D12 rule 8 doubles the hold for mirrored words "(D8 R43)"; the doubling is D8-R53. Same rule, wrong reference.
17. **Loudness command** vs D3: D3 §9 step 8 gives a one-pass `loudnorm=I=-23:TP=-2`; one pass runs in dynamic mode, which reshapes a quiet mix and upsamples to 192 kHz [V]. Use D8-R40's two-pass linear method; D3's `-ar 48000` is right.
18. **SC13 footage audio** vs A4 §15 question 3: this file follows A4's silent choice; if the user picks "tinny sound", then SDH needs a label for it and D8 §9.2's subtitle note changes.
19. **Crop timing** vs D6: D6 §5 (comp stack) step 11 crops to 2.39 "last if used". This file sets the crop in the edit (D8-R17, R19). They agree if D6 delivers every composite **uncropped** at full take size, so D8's per-shot `offset_y_px` still works; the breakdown should say so.
20. **CLICK/CLACK label** vs D18 §11 item 2: this file labels the whole family `[metal clacks]`; D18 suggests `[small metal click]` for SC15's "A small CLICK, from nowhere." (l.844), keeping "metal" as the family word. Both keep one family word; the user picks. D18 agrees with this file that nothing is added inside SC06's 10 black frames (`protect_silence`).

---

## Sources

All checked 2026-09-27; re-opened in the second fact-check the same day.

1. Blackmagic, Resolve 21.1 release: https://www.blackmagicdesign.com/media/partial/release/20260908-03 [V]
2. Blackmagic, Resolve Studio: https://www.blackmagicdesign.com/products/davinciresolve/studio [V]
3. Resolve 21.1 reports (CineD, Digital Production, Newsshooter): https://www.cined.com/davinci-resolve-21-1-released-ai-assistant-integration-via-mcp-individual-hdr-trims-and-python-scripting-moves-to-studio/ https://digitalproduction.com/2026/09/08/resolve-21-1-adds-mcp-and-finally-gets-presets/ https://www.newsshooter.com/2026/09/07/blackmagic-design-davinci-resolve-21-1/ [V]
4. Storyblocks, free vs Studio (15 Sep 2026): https://www.storyblocks.com/resources/tutorials/davinci-resolve-free-vs-studio [U]
5. davinci-kit, Linux codecs: https://github.com/drsnxt/davinci-kit/blob/main/docs/DAVINCI-RESOLVE-LINUX-GUIDE.md [U]
6. Pulse Edit, OTIO in Resolve: https://pulseedit.com/otio-import-davinci-resolve-free.html [U]
7. Shot Match; Resolve subtitles: https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=220994 ; https://sonix.ai/ai/add-subtitles-davinci-resolve/ [U]
8. Group grading: https://www.neatvideo.com/blog/post/resolve-groups-batch-grading [U]; Rec.709-A: https://www.knuterikevensen.com/2021/06/22/avoiding-gamma-shift-in-resolve/ [U]
9. Kdenlive 25.04.0 (OTIO): https://kdenlive.org/news/releases/25.04.0/ [V]
10. Kdenlive manual 26.08: https://docs.kdenlive.org/en/effects_and_filters/speech_to_text.html ; https://docs.kdenlive.org/en/effects_and_filters/subtitles.html [V]
11. FFmpeg filters: https://ffmpeg.org/ffmpeg-filters.html [V]; formats (`movflags +faststart`, `use_editlist`): https://ffmpeg.org/ffmpeg-formats.html [V]
12. Alibaba Cloud, Wan 3.0 (30 fps, 480P–1080P, 2–30 s): https://www.alibabacloud.com/help/en/model-studio/wan3-video-generation-guide [V]
13. Wan2.2-TI2V-5B: https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B [V]
14. fal, Seedance 2.5 API: https://fal.ai/models/bytedance/seedance-2.5/reference-to-video/api [V]
15. fal, Topaz upscale: https://fal.ai/models/fal-ai/topaz/upscale/video and /api [V]; generative: https://fal.ai/models/topaz/upscale/video/generative [V]
16. fal, SeedVR2: https://fal.ai/models/fal-ai/seedvr/upscale/video [V]
17. Topaz Labs pricing: https://www.topazlabs.com/pricing [V]
18. Practical-RIFE (MIT, `--multi`): https://github.com/hzwer/Practical-RIFE and its `inference_video.py` (`--fps`, output name) [V]; SeedVR2 paper: https://arxiv.org/abs/2506.05301 [V]; Topaz model guide (Proteus, Artemis, Gaia, Nyx described; Starlight as diffusion): https://docs.topazlabs.com/topaz-video/filters/enhancement [V]; face-hallucination warning: https://www.videoproc.com/resource/topaz-project-starlight.htm [U, secondary]
19. Cinema Tools grain scan: https://www.cinematools.co/blog/film-grain [V]
20. YouTube, upload encoding: https://support.google.com/youtube/answer/1722171 [V]; AI disclosure: https://support.google.com/youtube/answer/14328491 [V]
21. Vimeo, compression: https://help.vimeo.com/hc/en-us/articles/12426043233169-Video-and-audio-compression-guidelines [V]
22. EBU R 128 v5.0: https://tech.ebu.ch/publications/r128 ; true peak: https://tech.ebu.ch/docs/r/r128.pdf [V]
23. EBU R 95 v1.1: https://tech.ebu.ch/publications/r095 [V]
24. Netflix Subtitle Timing Guidelines: https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines [V]; Netflix English Timed Text Style Guide: https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide [V]; General Requirements: https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements [V]
25. Netflix loudness: https://www.production-expert.com/production-expert-1/how-to-optimise-an-audio-mix-for-delivery-to-netflix and Netflix Sound Mix Specifications v1.6 (partnerhelp, now redirected to studiopartner.netflix.net) [V, two agreeing]
26. BBC subtitle guidelines, summary (BBC page unreachable): https://www.clevercast.com/bbc-subtitling-guidelines/ [U]
27. YouTube loudness: https://www.criticallisteninglab.com/en/learn/loudness/youtube [U]
28. W3C WebVTT (Candidate Recommendation Draft, 20 May 2026): https://www.w3.org/TR/webvtt1/ [V]
29. SIL Open Font License: https://openfontlicense.org/ [V]
30. DCP-o-matic 2.18.50: https://dcpomatic.com/download [V]
31. Film Festival Cologne, DCP: https://filmfestival.cologne/en/technical-requirements-for-dcp-delivery [V]
31a. Google, Veo 3.1 in the Gemini API (24fps; 1080p and 4k 8 s only): https://ai.google.dev/gemini-api/docs/veo [V]
31b. Kling 3.0 frame rate, secondary only: https://aiwiki.ai/wiki/kling_3 ; https://prompt-architects.com/blog/410-frame-rate-settings-in-ai-video [U]
32. Library: A4 (§10, §11 WE1–WE3, §14, §15), B1 (§5, §10.4), B2 (P6, R21, §8.4–8.5), C1 (R23, Ex2, Ex7), C2 (R16, rule 26), C4 (R14, Rec5), C5 (P10, P12, E1, E3, E4), D3 (§9), D4 (Recipe 6, rule 20), D5 (§8, R19), D6 (§5, rule 20), D9 (rules 4b, spotting options), D12 (rules 8, 25, Recipe 7), D13 (R14, §6.7), D18 (R7).
33. Test sources, matched verbatim on 2026-09-27: *The Catch* (`1edae70d-35_The_Catch_-_workshop_revision_of_Final4.txt`, lines 93–94, 216, 219, 228, 238, 244, 248, 251, 259, 261, 278, 298, 327, 331, 484, 486, 488, 496, 500, 674, 740, 742, 824, 826, 844, 852, 1620, 1622, 1846, 1848, 1850, 1852); *The Long Places* (`5dcd8176-19_The_Long_Places_-_revised_by_Claude_final.md`, lines 549, 581, 601, 603, 607, 619).
