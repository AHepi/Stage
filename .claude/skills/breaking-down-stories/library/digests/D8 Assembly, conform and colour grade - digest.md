# Digest D8: Post-production assembly, conform, grade, finishing, subtitles and delivery (27 Sept 2026)

Source: `research/D8_post_assembly_conform_grade.md` (two fact-checks, 27 Sept 2026). Refs: **R#** = rule D8-R#, **Rec#** = recipe D8-Rec#, § = section. **[V]** primary page read 27 Sept 2026; **[U]** unverified; **[J]** judgment. Re-check tool facts and prices after 27 Oct 2026 (C5 R22).

## 1. Scope

1. Turns kept AI takes, voices, effects and music into one finished film: assembly, conform, lock, retime, upscale, grade, grain, sound, cards, subtitles, delivery, archive.
2. Fixes one timeline (24.000 fps, 1920×804, 2.39:1), one finishing order and three checkpoints (F lock, G grade, H delivery); the LLM writes scripts, OTIO, subtitle files and ffmpeg commands, the user clicks in the editor.
3. Adds `finish.*`, `grade_group`, `motif_color_locks`, `card_spec`, subtitle cue and `deliverables[]` fields, worked on *The Catch* (SC06, SC13, cards, SDH) and *The Long Places* ch. VII.

## 2. Rules

**Order and money**
1. [§2.3] If finishing, then do time, then size, then colour, then grain, because retiming alters the edit, upscaling changes what the grade sees, and grain must not be enlarged [J].
2. [§2.4, R20] If a step costs money, then run it only on locked, kept takes, because most generated seconds are thrown away [J].

**Assembly and lock**
3. [R1, R2] If building the first timeline, then have the LLM write `conform_v01.otio` from shot records, with `MISSING <job>` markers for gaps, because hand relinking fails silently [J].
4. [R3] If a take is replaced, then stack the new one above and disable the old, because it is the fallback until lock [J].
5. [R4, R5] If trimming, then put the used frames on the action and cut in whole frames (±1 per shot), because models rarely start on cue and 0.6 s is 14.4 frames [J].
6. [R6, R7] If lock is declared, then export `lock_v1.otio`/`.edl` and write `finish.edit`; if anything changes later, then re-run subtitles, music and stems, because they drift silently [J].
7. [R8] If a join is not a hard cut, then build it in the editor, because OTIO does not reliably carry transitions (Kdenlive exports none [V]).

**Frame rate**
8. [R9, R10] If choosing the timeline rate, then use 24.000 fps and only re-codec 24 fps takes, because Veo 3.1 makes "24fps", DCPs take 24 and YouTube wants the recorded rate [V].
9. [R11] If a 16 fps take has its 24 fps control video's frame count, then reinterpret it at 24; if the control was rendered at 16 fps, then treat it as free (rule 10), because only equal counts tie frames together [J].
10. [R12] If a 16 fps take is free, then blend to 24 for editing and interpolate after lock (RIFE `--multi=3`, keep every other frame; or Topaz `target_fps`), never RIFE's `--fps`, because reinterpreting plays 1.5× fast and `--fps` changes speed [V code]. Two in three final frames are invented: check hands.
11. [R13] If a take is 25, 30, 48 or 60 fps, then drop frames to 24 and interpolate after lock only a pan that judders, because dropping keeps real time and lip sync [J].
12. [R14] If a take was generated in slow motion, then return it to real time, because B1 bans slow motion in *The Catch*.
13. [R15, R23] If footage exists inside the story, then step-print it at 12 fps and plain-resize it, never interpolate or AI-upscale, because stutter and softness read as a recording (B1 §10.4) [J].
14. [R16] If a take is VFR, then convert it to CFR first, because editors mis-time VFR and Vimeo says "Always choose a constant frame rate" [V].

**Size, shape, cleanup**
15. [R17] If delivering 2.39:1 (user decides), then edit at 1920×804 and master at that or 3840×1608, because both fit HD and UHD, and free Resolve finishes up to 3840×2160 [V].
16. [R18, R19] If cropping, then kept height = width ÷ 2.39 rounded to even, rows off each side = (height − kept) ÷ 2 (1080 → 804, 138 each; 720 → 536, 92 each); measure 21:9 takes first; if a head or hand leaves the band, then move the clip and log `crop.offset_y_px` [J].
17. [R20, R21] If a take is below master size after cropping, then upscale after lock: whole takes to 1080p (name and frame count kept), used seconds plus handles only to 4K; never above about 2× (regenerate hero shots instead), because trimmed files break relinking and small faces get invented features [J].
18. [R22] If faces are in frame, then use a precision model first (Topaz Proteus, fal's default; Gaia HQ for rendered content), diffusion (Starlight, SeedVR2) only if too soft, checking faces, rings and hands, because "Starlight models use diffusion for restoration and upscaling" [V fal] and can invent faces [U]. Nyx is a denoiser.
19. [R24] If a shot gets composited elements, then upscale the plate first and render elements at master size (D6), because upscaling a composite smears edges [J].
20. [R25] If the whole frame pumps in brightness, then deflicker (ffmpeg `deflicker`, 2–129 frames [V]; Studio's de-flickering [V]); if detail crawls, then try grain or a new take, because deflicker only evens brightness [J].
21. [R26] If a take has a visible watermark, then regenerate on a paid plan or keep and credit it; never crop it out or strip C2PA or SynthID, because D4 rules 13–14 tie marks to free-tier terms [J].

**Colour**
22. [R27] If all sources are 8-bit BT.709, then grade on a Rec.709 Gamma 2.4 timeline with no conversions, because conversions add error [J].
23. [R28–R30] If grading mixed generators, then use four levels: a normalize node per generator per group (waveform black and white points, parade grey, vectorscope saturation, gamma last); a per-shot trim from Shot Match; the group look matched to the style frame; timeline grain, because models differ mostly in black level, contrast, saturation and cast [J].
24. [R31] If grading a sequence, then watch the group as a slideshow beside the style frame, because drift shows only in sequence (C2 rule 26).
25. [R32, R33] If a motif colour or written light change is in frame, then check `motif_color_locks` and never grade it away, because the grade corrects models, not story [J].
26. [R34] If adding grain, then add one grain once at timeline level after grade (Cinema Tools' free scan in Overlay, or `noise=alls=<n>:allf=t` from D5's fine 4–6) with Topaz `grain` at 0, because it unifies generators [V tools; J].
27. [R35, R36] If using a LUT, then only to carry a finished look; if Mac or browser viewing matters, then test a private upload on two devices, because of gamma shift [U].

**Sound**
28. [R37] If mixing, then route every track to DIA, MUS or FX stems, because A4 requires stems and dubbing needs an M&E [J].
29. [R38, R39] If setting loudness, then set it per deliverable over the whole film: web about −14 LUFS [U]; EBU R 128 −23 ±0.5, ≤ −1 dBTP [V]; US −24 LKFS; Netflix −27 LKFS dialogue-gated, −2 dBTP [V]; a quiet film may sit at −16 to −18 online, because platforms turn loud files down, not quiet ones up [J].
30. [R40] If normalizing with ffmpeg, then run two-pass `loudnorm` with `I`, `TP`, `LRA` (≥ measured) and `-ar 48000`, and confirm `linear`, because it "will revert to dynamic" otherwise and dynamic upsamples to 192 kHz [V].
31. [R41] If the film ends on a motif, then cut to black in a rest, carry one full statement, then continue under card and credits or recede over two or three cycles, because "a stopped heartbeat reads as a death" (A4 SND8) [J].

**Cards**
32. [R42, R43] If the script writes a card, then make it a `card` shot, cut in and out, held for the longer of A4 R8 and 2 s + 0.5 s per word (title ≥3 s), because A4 T5 adds no device to an all-cut film [J].
33. [R44–R46] If setting text, then use one OFL font (no acknowledgement needed [V]) inside graphics-safe (x 96–1824, y 40–764 on 1920×804; EBU R 95 [V]) and D4's credit line, because players crop bars [J].

**Subtitles**
34. [R47, R48] If writing cues, then copy text from the shot record and time it from the placed dialogue file, because recognition changes words [J].
35. [R49] If checking cues, then apply Netflix: ≤42 characters per line, ≤2 lines, ≤20 cps, ≥20 frames, ≤7 s; start within 1–2 frames of speech; gaps 2 frames or ≥12; within 12 frames of a cut, snap to it (end 2 frames before); a cue crossing a cut ends 2 frames before or ≥12 after, because cues must not flash [V].
36. [R50, R51] If making SDH, then use one style (default Netflix lowercase brackets), label only what "cannot be visually identified" [V], and give each motif one `sdh_label` carrying its pattern (D18-R7), because deaf viewers need the same signal [J].
37. [R52] If a speaker is not in the scene (narration, earpiece), then italicize; if merely off screen, then not [V Netflix].
38. [R53] If on-screen text reads backwards, then give no original-language subtitle and double reading time, because its meaning is its orientation [J].
39. [R54] If speech is untranslated, then SDH names the language (never `[speaking foreign language]` [V]); if the POV character understands it, then subtitle what she understands [J].
40. [R55] If delivering subtitles, then export SRT and WebVTT timed from the file's first frame (timeline minus 01:00:00:00), burning in only on demand, because players count from zero [J].

**Delivery**
41. [R56, R57] If uploading, then YouTube: MP4 Fast Start, no edit lists, H.264 High 4:2:0, 2 B-frames, closed GOP of 12, BT.709, 24 fps, 8 Mbps at 1080p (15–20 with grain [J]), AAC-LC 48 kHz 384 kb/s; Vimeo: 10–20 Mbps, CFR, AAC-LC 320 kb/s [V].
42. [R58, R59] If a festival wants projection, then make a DCP in DCP-o-matic (Scope 2048×858, 24 fps, subtitles burned in or DCI files), because sheets like Cologne's refuse `.srt` and other formats [V]; screeners are H.264 1080 at 10–20 Mbps [J].
43. [R60] If archiving, then keep texted and textless masters, WAV stems, SRT/VTT, lock OTIO/EDL, project, breakdown, raw downloads with Content Credentials, licences and disclosure record, because nothing else rebuilds the film [J].

## 3. Breakdown fields

Enums lowercase `snake_case`; empty = `"none"` (C5 R29). Authority: *derived* (script) or *authored* (with `decided_by`).

| Level | field_name | Meaning | Allowed values / example |
|---|---|---|---|
| film | `finish.timeline_fps` | Timeline rate | `24` \| `25` |
| film | `finish.working_resolution`, `finish.master_resolution` | Edit size; master size | `1920x804`; `1920x804` \| `3840x1608` |
| film | `finish.editor` | Editing program | `resolve_free` \| `resolve_studio` \| `kdenlive` \| `other` |
| film | `finish.output_color_tag` | Tag in delivery files | `rec709` \| `rec709a` |
| film | `finish.grain` | The one film grain | {`method`: `grain_scan_overlay` \| `ffmpeg_noise` \| `resolve_film_grain` \| `none`, `strength`} |
| film | `finish.sdh_style` | SDH house style | `netflix` \| `bbc` |
| film | `finish.picture_lock` | Lock record (derived) | {`version`, `date`, `otio_file`} |
| film | `deliverables[]` | Files to make | {`id`, `kind`: `web_upload` \| `festival_screener` \| `dcp` \| `archive_master` \| `textless_master` \| `stems` \| `subtitles`, `container`, `video_codec`, `resolution`, `fps`, `bitrate_mbps`, `audio`, `loudness_target_lufs`, `true_peak_dbtp`, `subtitles_mode`: `burned_in` \| `sidecar_srt` \| `sidecar_vtt` \| `dcp_xml` \| `none`, `status`} |
| film | `credits_spec` | End credits | {`type`: `cards` \| `roll`, `seconds_per_card` or `px_per_frame`, `font`} |
| scene | `grade_group` | Look the scene is graded in | `GG-04`; in-story look key `LK-CCTV` |
| scene | `style_frame` | Approved still | path (B2 `key_frame_ref`) |
| scene | `motif_color_locks[]` | Colours the grade keeps | {`motif_id`, `colour`, `rule`: `never_glow` \| `hue_fixed` \| `max_saturation_below_peak` \| `desaturate_others` \| `near_neutral`, `check`: yes/no question} |
| scene | `edit_status` | Progress | `assembly` \| `rough` \| `fine` \| `locked` |
| shot | `finish.measured` | What the take is (derived) | {`fps`, `width`, `height`, `codec`, `frame_count`, `vfr`} |
| shot | `finish.fps_action` | Rate handling | `none` \| `reinterpret_24` \| `drop_frames` \| `frame_blend` \| `optical_flow` \| `ai_interpolate` \| `step_print_12` \| `step_print_15` \| `realtime_from_slow` |
| shot | `finish.crop` | Shape handling | {`mode`: `none` \| `center` \| `offset` \| `fit_pillarbox`, `offset_y_px`} |
| shot | `finish.scale_action`, `finish.upscale_tool` | Size handling; exact tool and model | `none` \| `plain_resize` \| `ai_upscale`; `fal-ai/topaz/upscale/video, Proteus` |
| shot | `finish.cleanup` | Repair | `none` \| `deflicker` \| `denoise` \| `deflicker_denoise` |
| shot | `finish.flip` | Mirror operation (derived, C1 `mirror_flip`) | `yes` \| `no` |
| shot | `finish.normalize_node`, `finish.match_to` | Grade level 1; anchor shot | `NORM_SEEDANCE25_GG04`; `SC06-SH030` |
| shot | `finish.conform_notes` | One or two lines for the editor | text |
| shot | `finish.conform_status` | Progress (derived) | `raw` \| `normalized` \| `cut` \| `locked` \| `final_media` \| `composited` \| `graded` \| `delivered` |
| shot | `finish.edit` | Lock timing (derived) | {`record_in_tc`, `record_out_tc`, `source_in_frame`, `frame_count`} |
| subtitle cue | `cue_id`, `shot`, `kind`, `text`, `start_tc`, `end_tc`, `italic`, `position`, `source_ref`, `track` | One cue | `SUB-0042`; `dialogue` \| `sdh_sound` \| `sdh_speaker` \| `forced_narrative` \| `lyric`; `bottom` \| `top`; `standard` \| `sdh` \| `both` |
| shot (`card`) | `card_spec` | A card | {`text` (exact), `font`, `font_licence`, `cap_height_pct`, `colour`, `background`, `hold_frames`, `in`: `cut` \| `fade_<frames>`, `out`, `sound`: `none` \| `room_tone` \| `motif_continues` \| `motif_recedes`, `safe_area`: `graphics_safe`} |
| motif | `sdh_label` | Fixed SDH words | `[three uneven pump strokes]` (D18-R7; user confirms) |

**Validator** [§6, J]: every locked shot has `finish.measured`; `fps_action` fits `measured.fps` (24 → `none`; 16 → `reinterpret_24` only with an equal-frame-count control video); no `ai_upscale` where `grade_group` is an in-story look key; card `text` matches its source line; every cue passes R49; each scene's summed `frame_count` within 10% of target (C5 R27); every deliverable has a `status`.

## 4. Procedures

1. **Set up (Rec1, 20 min).** Ask: *"Add to the CATCH folder: `media/01_raw`, `02_edit`, `03_final`; `audio/` (dialogue, fx, beds, motifs, music); `graphics/cards`; `subtitles`; `timelines`; `deliver/` (web, festival, dcp, archive). Update `manifest.json`."* Copy kept takes unchanged into `01_raw`. In Resolve, before importing anything: timeline 1920×804, 24 fps, start 01:00:00:00, Rec.709 Gamma 2.4, mismatched resolution "Scale full frame with crop" [U menu].
2. **Measure and normalize (Rec2).** Ask: *"Write and run `measure_takes.py`: ffprobe every file in `media/01_raw` (codec, size, `r_frame_rate`, `avg_frame_rate`, frame count, audio codec) into `finish.measured`, `vfr: yes` where the rates differ. Flag anything not 24 fps CFR or narrower than 1920 pixels after a 2.39 crop."* Then: *"Write and run `normalize_takes.py`: choose `fps_action` from D8-R10–R16, write `media/02_edit/<same name>.mov` as DNxHR HQ 4:2:2, 24 fps CFR; keep audio as 48 kHz 24-bit PCM only where `model_audio` is `use_native` or `dialogue_only`; log every command."* Commands:
   - codec only: `ffmpeg -i IN.mp4 -map 0:v:0 -c:v dnxhd -profile:v dnxhr_hq -pix_fmt yuv422p -an OUT.mov`
   - reinterpret 16 → 24: add `-vf "setpts=N/(24*TB)" -r 24`
   - drop 25, 30, 48 or 60 → 24, or VFR → CFR: add `-vf fps=24`
   - quick blend 16 → 24 for editing: add `-vf "minterpolate=fps=24:mi_mode=blend"`
   - step print 12 in a 24 fps file: add `-vf "fps=12,fps=24"`
   - keep planned native audio: replace `-an` with `-map 0:a:0 -c:a pcm_s24le -ar 48000`
   - RIFE after lock: `python3 inference_video.py --multi=3 --video=IN.mp4` (writes `IN_3X_48fps.mp4`), then `ffmpeg -i IN_3X_48fps.mp4 -vf fps=24 -c:v dnxhd -profile:v dnxhr_hq -pix_fmt yuv422p -an OUT.mov`
3. **Conform timeline (Rec3).** Ask: *"Extend `export_otio.py` to write `timelines/conform_v01.otio`: V1 the kept takes from `media/02_edit` in shot order, each starting `handles_s` × 24 frames in and lasting `duration_s` × 24 frames, named by shot ID; V2 the animatic, disabled; A1–A3 dialogue, A4–A6 effects and beds, A7 motifs, A8 music; `MISSING <job>` markers. Also write a CMX 3600 EDL."* Resolve: File > Import > Timeline, source-clip import on; relink offline clips to `media/02_edit` [U menus].
4. **Cut to lock (Rec4, hands-on).** Slip to the action, trim to A4's cut reasons; cuts to black use editor black. Save versions as `CATCH_cut_v007`; lock as `CATCH_LOCK_v1`; export `lock_v1.otio` and `.edl`. Ask: *"Read `lock_v1.otio`, write each shot's `finish.edit`, and list shots that moved by more than 2 frames and scenes that moved by more than 10% from A4's plan."* Checkpoint F.
5. **Final media (Rec5, ~$0.02/s to 1080p).** Ask: *"List locked shots needing interpolation or upscaling; price them on fal Topaz and SeedVR2; show the total before running."* Whole takes from `01_raw`: `{"video_url": "<take>", "model": "Proteus", "upscale_factor": 1.5, "grain": 0, "H264_output": true}` (+ `target_fps: 24` only where planned); normalize into `03_final`, same name and frame count. **4K:** the file starts 18 frames before the used part (`<take>_4k.mov`); point the OTIO clip at frame 18. Check faces; failures get plain resize. The LLM rewrites `lock_v1.otio` paths to `03_final` (`CATCH_FINAL_v1`).
6. **2.39 frame (Rec6).** Fill scaling centre-crops; scrub with the safe-area overlay; move clips that lose heads or hands, log `crop.offset_y_px`.
7. **Grade (Rec7).** Ask: *"From B2's colour script, list grade groups, scene ranges, style frames and motif colour locks. Run `signalstats` on every take in GG-04 and list takes whose `YLOW`, `YAVG`, `YHIGH` or `SATAVG` sit far from the group median."* Command: `ffprobe -v error -f lavfi -i "movie=IN.mov,signalstats" -show_entries frame_tags=lavfi.signalstats.YLOW,lavfi.signalstats.YAVG,lavfi.signalstats.YHIGH,lavfi.signalstats.SATAVG,lavfi.signalstats.YDIF -of csv=p=0`. "Far" = more than 10 (0–255) on the Y values or 20% on `SATAVG` [J]. Node 1 per generator on its most neutral take, saved as `NORM_<MODEL>_<GROUP>`; node 2 Shot Match to the anchor, trim by eye; group look at post-clip level; grain only at timeline level. Checkpoint G.
8. **Sound (Rec8).** Buses DIA, FX, MUS → main; balance dialogue first; meter the whole film; limiter at the ceiling; render mix and stems WAV 48 kHz 24-bit from frame 1; M&E = mix minus DIA. Without Fairlight:
   - pass 1: `ffmpeg -i CATCH_mix.wav -af loudnorm=I=-14:TP=-1:LRA=20:print_format=json -f null -`
   - pass 2: `ffmpeg -i CATCH_mix.wav -af loudnorm=I=-14:TP=-1:LRA=20:measured_I=<input_i>:measured_TP=<input_tp>:measured_LRA=<input_lra>:measured_thresh=<input_thresh>:offset=<target_offset>:linear=true:print_format=json -ar 48000 -c:a pcm_s24le CATCH_mix_web.wav`
9. **Cards (Rec9).** Ask: *"For every `card` shot, fill `card_spec` from its source line and D8-R42–R46, and render each as a 1920×804 PNG (and 3840×1608 if mastering at 4K), off-white on pure black, centred in the graphics-safe area."* Credits: 3–4 names per card, ~3 s, or a roll at 2–4 whole pixels per frame.
10. **Subtitles (Rec10).** *"From `lock_v1.otio` and the shot records, make one cue per dialogue line with the exact text from `sound.dialogue`, timed to its placed dialogue file (forced-alignment times where it came from native audio). Apply D8-R49, split at phrase boundaries, italicize per D8-R52. Write `subtitles/CATCH_en.srt` and `.vtt`."* Then *"Add cues for every `sync_fx`, `offscreen` and motif entry marked `sdh: yes` (motifs use `sdh_label` verbatim) and speaker labels where unclear. Write `CATCH_en_sdh.srt` and `.vtt`."* Then *"List every cue breaking D8-R49."* Watch once muted, once with sound.
11. **Deliver (Rec11).** Render master (ProRes 422 HQ or DNxHR HQX, 24 fps, PCM) and textless master. Web file: `ffmpeg -i CATCH_master.mov -i CATCH_mix_web.wav -map 0:v:0 -map 1:a:0 -c:v libx264 -profile:v high -pix_fmt yuv420p -b:v 18M -maxrate 20M -bufsize 36M -bf 2 -g 12 -r 24 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 384k -ar 48000 -movflags +faststart -use_editlist 0 deliver/web/CATCH_web.mp4`; check: `ffprobe -v error -show_entries stream=codec_name,profile,width,height,pix_fmt,r_frame_rate,color_primaries,color_transfer,color_space,sample_rate,bit_rate -of json deliver/web/CATCH_web.mp4`. DCP in DCP-o-matic (Scope, 24 fps), tested on a cinema server; private upload first; YouTube Attributes > "AI use" [V]. Ask: *"Build `deliver/archive/` per D8-R60 with a checksum list, and add every file to `manifest.json`."* Checkpoint H.
12. **Kdenlive route (Rec12).** OTIO in (no effects or transitions [V]); build joins; subtitles import SRT/ASS/VTT/SBV, export SRT/ASS [V]; group look as `.cube` [U]; ffmpeg makes delivery files.

## 5. Checklists

**Per take:** measured • 24 fps CFR or logged `fps_action` • audio only where planned • name unchanged.
**Checkpoint F:** every cut has a reason • no `MISSING` (or accepted as still) • reading times met • A4 ruptures, blacks, silences exact • lock OTIO/EDL out, `finish.edit` written.
**Per final take:** same name and frame count (or 4K relink checked) • faces match reference pack • no warping • in-story footage not AI-upscaled • Topaz grain 0.
**Checkpoint G (per group):** sits with the style frame? one camera across generators? red below the fire? yellow painted, not glowing? Iona's blue fixed, other blues quieter? growth grey? B2's light changes intact? dark skin rich? grain once, clean blacks?
**Checkpoint H:** ffprobe matches each deliverable • loudness measured on the file, linear confirmed • subtitles pass R49 on the final cut, times from zero • cards exact, D4 line present • pump never stops dead • AI label set • private upload watched on phone and computer • archive checksummed.

## 6. Saying it to AI models

- **To the LLM:** name rule numbers and paths (§4 templates); ask for logged commands, a price before paid runs, the `loudnorm` mode, and subtitle times from zero.
- **To Resolve:** free 21.1 keeps console scripting, but external scripting, Workflow Integrations and the MCP server are Studio-only [V]; so the LLM writes OTIO, EDL, SRT, VTT, `.cube` and PNG files or a console snippet. With Studio ($295), plain requests work over MCP ("organize media", "batch render"); test on a copy [J].
- **To upscalers (fal):** name endpoint and model, `upscale_factor`, `grain: 0`, `H264_output: true`, and `target_fps` only when interpolating; for Starlight or SeedVR2 check every face against the reference pack.
- **To generators:** keep heads and hands inside the central 2.39 band (B1); use 21:9 where offered (Seedance 2.5 [V]); set Seedance `generate_audio` off for silent plates; no slow motion in *The Catch*; generate with handles; measure the frame rate.

## 7. The Catch

**Decisions made** [§9, J unless noted]
- **SC06 fall (GG-04, ~36 shots, ASL ~1.4 s, l.228–298):** Seedance 720p wides cropped to 1280×536, upscaled ×1.5 after lock; Wan VACE POVs `reinterpret_24`; Kling faces ("Io.", l.251; "Push.", l.278) `drop_frames` if above 24; beads rendered at 1920×804 over upscaled plates; row 17 = 10 frames editor black, CLACK (l.259) on frame 1. One normalize node per model; the flipped key light after row 17 kept (B2 R21); rows 8 and 19 share `offset_y_px`.
- **SC13 playback:** one 640×480 master take, `step_print_12`, plain resize to 1072×804 inside bezel-filled sides, `LK-CCTV`, mirrored with phase B; the freeze is a real exported frame; no SDH inside the silent footage.
- **Cards:** SC10-SH990 "THE CATCH" after "Nobody leave this room." / "> CUT TO BLACK." (l.484–488): 24 frames black, 72-frame card, 12 frames black, hard cut; silence under both. SC30-SH990 (after l.1848): black carrying one complete pump cycle (~60–84 frames); SH995 "THE END", 72 frames, pump continuing or receding.
- **SDH (Netflix style):** `[door crashes open above]` / `[gunshots]` (l.216); `[softly] Oh.` (l.219); SHRIEK cue (l.238) starts with the J-cut sound; "Io." held 20 frames; CLACK cue 22 frames, ending 12 past the cut; "(in her ear)" (l.93–94) italic, `[over earpiece]` once; one pump `sdh_label` from l.852. Backwards text (l.327, 331, 496, 500): no subtitle; "RECEIVING" (l.1620): reading time only.
- **Motif locks:** red below the fire's saturation; yellow painted, never glowing; Iona's blue fixed; growth near-neutral, "never a sickly green" (B2).
- **Long Places VII:** the letter (l.549) italic in three phrase cues; the elder's line subtitled as Nilay understands it (l.601); rod-camera footage step-printed; the recovered frame (l.619) a real still.

**Flagged for the user**
1. Delivery ratio (2.39 assumed; 1.85 works with DCI Flat 1998×1080).
2. Pump after the last cycle: continue under credits or recede (A4 §15 q2); affects any D9 credits cue.
3. Music policy (A4 §15 q1, D9): decides sound under the title card (D8 proposes silence) and the card's hold (72 or 96 frames).
4. SDH style (Netflix default) and wording: pump `[three uneven pump strokes]` (D18) or `[pump thumping]`; SC15 click `[small metal click]` or `[metal clacks]`.
5. SC13 footage silent (A4's choice) or tinny (A4 §15 q3).
6. Web loudness: accept −16 to −18 LUFS for a quiet film?
7. Free Resolve or Studio ($295): Studio only for Super Scale, Speed Warp, deflicker, Film Look Creator or Claude over MCP.

## 8. Conflicts and open questions

1. **D13 upscaling:** aligned, but its v0 factor (1.5 × runtime) underprices fast scenes such as SC06, where whole takes are 2–4× runtime; price those at 3×.
2. **C4 16 fps:** R14 (render previs at 16) vs Rec5 (play at 24) is resolved by frame count (R11, R12); C4 should say so.
3. **D18:** D8 now defaults to R7's pump label; SC15's click label open (D18 §11 q2).
4. **D9:** its `sparse` cue holds the title card 4 s (D8: 72 frames) and plays under it (D8: silence); `end_credits_only` excludes `motif_continues`.
5. **D12:** rule 25 says free Resolve has "no Python scripting" (console scripting remains); rule 8 cites R43 for doubled mirrored reading time (it is R53).
6. **D3 §9 step 8** uses one-pass `loudnorm=I=-23:TP=-2` (dynamic mode); use R40's two-pass linear method.
7. **D6 §5 step 11** crops "last"; compatible only if composites return uncropped, so D8's `offset_y_px` still works.
8. **Checkpoints F–H** extend C5's A–E; C5 and D13's schedule should name them.
9. **"Topaz"** in C1 and D13 hides three model families; always log the model.
10. **Unverified:** Kling 3.0 and Seedance 2.5 frame rates; which Resolve grading tools are free; Linux codecs; menus; YouTube −14 LUFS; BBC style.

## 9. Section map

| Need | Source section |
|---|---|
| Checkpoints F–H; terms; principles | §0–§2 |
| Tools, prices, what an LLM can drive; generator specs | §3 |
| Rules R1–R60 | §4.1–4.8 |
| Recipes Rec1–Rec12 | §5 |
| Breakdown fields, example block, validator | §6 |
| Checklists | §7 |
| Failure modes | §8 |
| SC06, SC13, cards, SDH samples (SRT, VTT), Long Places VII | §9.1–9.5 |
| Conflicts 1–20 | §10 |
| Sources | end |
