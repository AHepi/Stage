# D9. Music and Sound Effects for AI Films: Spotting, AI Music, Libraries, Motif Assets, Licensing

*Library file D9. Written 2026-09-27. Test sources: "The Catch" (screenplay, workshop revision of 25 September 2026) and "The Long Places" (prose, revised final).*

> **What this file is for**
> 1. It lists, with dates, the tools that make music and sound effects today (AI music generators, AI sound-effect and video-to-audio models, libraries) and what their licences allow in a film.
> 2. It gives a spotting procedure a non-musician can run with an LLM: from A4's `music.cues` to a generator prompt, a temp score for the animatic, and a re-spot after picture lock.
> 3. It shows how to keep a theme and a sound motif identical across a film: one master file, variations made by processing a copy, never by regenerating.
> 4. It covers sound effects (library, generation, video-to-audio, home foley) and how a film with no score carries tension.
> 5. It adds sound fields and a licence log to the breakdown, with worked examples on *The Catch* (pump, CLICK/CLACK, the ship's hum, foley, music policy) and *The Long Places* (drill, knock, lullaby).

**Evidence labels.** [V] read on the named source; [V-sec] read on a secondary source (press, review site) or in search excerpts from several such sources; [U] unverified (single search excerpt, or not documented); [J] this file's judgment. [S#] points to Sources; every URL there was checked 2026-09-27, and the fact-check pass of the same day re-read S1–S4, S6, S8–S28, S30–S35 and corrected the entries marked "(corrected)". A second, adversarial pass the same day re-fetched S1–S4, S6, S8–S11, S13–S28, S30–S34 and Suno's own v6 release notes (S5 is now primary), re-checked every *The Catch* and *The Long Places* quotation against the texts (all verbatim), and marked its changes "(pass 2)". Tool facts age fast: re-check any fact older than a month before paying for anything.

**Builds on, does not repeat:** A4 §7.1–7.8 (Chion's terms, four layers, silence grades, spotting rules, the sound line in prompts), WE3–WE4 and §14; B4 §3.4 (sound levels S0–S3) and M10; C3 §7E and rule 10 (no music in clips); C1 rule 22 (silent models). Voices and dialogue are D3, including the device and helmet processing chains (D3 §8.1) that this file reuses for effects heard through the same devices; rights, likeness and disclosure law are D4; final mix and stems delivery are D8 (D8-R37: every motif and bed goes to the effects stem).

**Scene numbers** follow C5's IDs (SC06 = A4's sc6).

---

## 0. Words this file uses (one word per concept)

| Word | Plain meaning |
|---|---|
| **Cue** | One piece of music with a start (in) and an end (out) in the film. |
| **Spotting** | Deciding where each cue starts and stops and what it must do (A4 §7.6). |
| **Spotting sheet** | The table of all cues, one row each, with the fields in §5. |
| **Picture lock** | The point after which shot lengths no longer change. |
| **Animatic** | Timed storyboard frames or previs renders played with rough sound (C2, C4). |
| **Temp score** | Stand-in music laid on the animatic or rough cut to test a cue, replaced before release. Wikipedia: existing music "used during the editing phase ... serving as a guideline for the tempo, mood or atmosphere" [V, S35]. |
| **Theme** | A short tune the audience should recognize when it returns. |
| **Variation** | The same theme changed in speed, instruments, loudness, distance or length, but still recognizable. |
| **Tempo (BPM)** | Speed of the music in beats per minute. |
| **Key** | The home note and scale a piece is built on (for example A minor). |
| **Hit point** | A picture moment that a cue must land on (a cut, a door, a look). |
| **Stems** | Separate audio files for parts of a mix (drums, bass, melody; or dialogue, music, effects). |
| **Sound effect** | Any non-speech, non-music sound laid in the film (`sync_fx`, `offscreen`, beds, motifs). |
| **Foley** | Everyday body sounds (hands, cloth, footsteps) performed and recorded to match the picture. |
| **Text-to-SFX** | A model that makes a sound effect from a written description. |
| **Video-to-audio (V2A)** | A model that watches a silent clip and makes sounds timed to it. |
| **Library** | A collection of ready-made sounds or music under one licence. |
| **Royalty-free** | Paid once (or free), then usable without per-use fees; it does not mean "no conditions". |
| **Creative Commons (CC)** | Standard public licences: CC0 (no conditions), CC BY (credit the author), CC BY-NC (credit, and no commercial use). |
| **API, aggregator** | A programmatic way to call a model; aggregators such as fal sell many models through one account (C1 §7). |
| **Open weights; MIT licence** | A model you can download and run yourself; MIT is a permissive licence that allows commercial use if the notice is kept. |
| **Master file** | The one stored recording of a motif or theme from which every use is copied. |
| **Signature** | The fixed rhythm and sound of a motif, written down in numbers (A4 §7.4). |
| **Processing** | Changing a copy of a file with effects (filter, reverb, speed, pitch) while the master stays untouched. |
| **Preset** | A named, reusable processing chain (for example `through_suit`). D3 calls the same thing a "path chain"; one name per device is shared by voices and effects (§4.6). |
| **Filter / EQ** | Processing that removes or boosts some frequencies (pitch height, in Hz: vibrations per second; low numbers are deep sounds). A **low-pass** filter keeps the lows and removes highs (muffled); a **high-pass** keeps the highs and removes lows (thin). |
| **Reverb** | Added reflections that place a sound in a room of a given size. |
| **Transient** | The sharp first instant of a sound, which carries most of its identity. |
| **Tail** | The ring-out after a sound or cue ends; cutting it off sounds like an error. |
| **Drone** | A long held tone or hum. |
| **Sound emphasis** | B4's four mix levels for a sound motif, field `sound_emphasis`: 0 bed, 1 clear, 2 foreground, 3 alone (B4 writes S0–S3). |

---

## 1. Core principles

1. **Clips are music-free; music lives in the edit** (C3 rule 10). A model's music restarts at every cut, and Google's own music documentation warns: "Results may vary between calls, even with the same prompt" [V, S13].
2. **One master, many copies.** Every recurring sound or theme exists once as a master file. Every appearance is a processed copy, so the audience hears the same thing in a new place [J; extends A4 SND3 and B4 M10's rule "one recorded sound for every appearance, same rhythm and timbre"].
3. **Change the mix, not the sound.** Perspective (small speaker, helmet, behind her, over black) comes from processing presets; the signature never changes [J; B4 M10 "only the mix (distance, room) changes"].
4. **Policy before prompts.** The film-wide music policy is set once, at checkpoint B, by the user; no cue is generated before it [J; A4 §7.6; critic resolution].
5. **Spot twice.** Spot once on the animatic with a temp score; spot again after picture lock and make finals only then (A4 §7.6).
6. **A licence travels with every file.** No sound enters the timeline without a licence record (§5). The free tier of a tool is usually not a film licence (§2.1).
7. **Silence and diegetic sound are not a lack of music.** With policy `none`, beds, motifs, ruptures and tonal sounds from the story world carry the tension (§4.8).
8. **Check generated sound as you check generated picture.** Every video-to-audio or native track is listened to against the shot's `sync_fx` list before it is kept (A4 §14; §4.7 here).

---

## 2. Landscape (checked 2026-09-27)

### 2.1 Music generators

| Tool, version, date | Access and price | Length | Stems | Tempo and key control | Keeping a theme | Terms that matter for a film |
|---|---|---|---|---|---|---|
| **Suno v6** (9 Sep 2026): v6 ("reliable, precise") and v6-wild ("less predictable and more varied") "available only to paid users"; v6-mini "available to everyone" [V, S5]; new: edit one section or one lyric by plain-language instruction, and "Create with text, audio, images and video" [V, S5]. Older models are being retired (S2 explains what happens to songs made on "retired" models) [V, S2; full list of retired models V-sec, S5] (pass 2) | Free $0 ("Best free model (v6-mini)", "No monthly song downloads", "No commercial rights"; up to 7 lifetime trial downloads "for personal, non-commercial use only"); Pro $8/month, 20 song downloads a month; Premier $24/month, 60 a month, plus Suno Studio, the browser editing program, "now with MIDI, effects, automation" (Premier only) [V, S3, S1, S2] (corrected; pass 2) | Songs; maximum not stated on the pricing page [U]. Upload of your own audio: Free up to 8 min, Premier up to 30 min [V, S3] (pass 2) | Pro: 2 stem separation types ("Auto; Split from mix"); Premier: 3 (adds "Advanced split"); Studio exports "Multitrack" and MIDI [V, S3, S4] | Studio "Manual BPM" gives "a consistent tempo"; Suno says generated songs can have "tempo drift" [V, S4]; key by prompt only [U] | Remix or extend an existing song; operations on songs from retired models "run on the new models, so results may sound different from the original generation" [V, S2] | Paid-plan downloads "remain yours to use commercially or personally"; trial downloads are not [V, S1]. Rights attach to songs downloaded "as a paying subscriber" [V, S2]. New limits from 3 Sep 2026; "Downloading a song plus its stems counts once"; Studio work can still be downloaded "without limitation" [V, S2] |
| **Udio** | Generate and stream inside Udio only | — | "downloading of audio, video, and stems has been disabled" (page updated 17 Feb 2026) [V, S6]; disabled since the Universal Music Group (UMG) settlement and partnership announced 29 Oct 2025 [V, S6; V-sec, S7] (corrected, pass 2: first written 30 Oct) | — | — | A licensed relaunch "in 2026" was announced with UMG, and Warner Music signed a similar deal in Nov 2025 [V-sec, S7]; secondary sources say the new service is a "walled garden" whose creations "cannot be downloaded or posted elsewhere" [V-sec]; no relaunch with downloads found on 2026-09-27 [V-sec]. Not usable for film until export returns [J] |
| **ElevenLabs Music v2.5** (Music v2 offered; v1 "during a transition period") [V, S8] | ElevenLabs plans; "The Music API is available for paid subscribers" [V, S8] | 3 s to 5 min; MP3 44.1 kHz or WAV [V, S8] | Stem separation API; the stem options are not listed in the docs [V, S12; U on options] | Not documented [U] | "Audio Reference": upload up to about 30 s to guide style, "screened for copyright compliance"; "not a remixing or genre-transfer tool" [V, S8]; inpainting regenerates one selected section "without affecting the rest of the track" [V, S8] | Every plan from Free to Business, and also Enterprise Music Lite, allows commercial use "except film, TV, radio, & Studio Games"; only the full Enterprise Music tier says "All online and offline commercial use permitted"; Free requires attribution ("denote Eleven Music when distributing") [V, S10] (pass 2: Enterprise Music Lite added). **Beware:** the Music documentation page says "Eleven Music is cleared for nearly all commercial uses, from film and television to podcasts" [V, S8]; the dated Model-Specific Terms are the contract and exclude film below Enterprise Music, so follow the terms [J; D4 decides]. Prompts may not name artists, songwriters, song or album titles, publishers or labels, or quote a substantial part of a song's lyrics [V, S9]. Output "may not be unique and may be similar or identical to Output returned to other users" [V, S9] |
| **Google Lyria 3.5** (`lyria-3.5`, Gemini API, Sep 2026); **Lyria 3 Clip** (`lyria-3-clip-preview`, 30 s) [V, S13]. Availability in the consumer Gemini app not checked [U] (corrected) | $0.08 per song (Lyria 3.5), $0.04 per 30 s clip; free tier "Not available". The pricing page now labels Lyria 3 Clip and Lyria 3 Pro Preview "Legacy" [V, S15] (pass 2) | Exactly 30 s (Clip); "a couple of minutes" (3.5), length adjustable in the prompt; 44.1 kHz stereo MP3, WAV for 3.5 [V, S13] (pass 2) | None documented [U] | Prompt text: Google advises "Mention instruments, BPM, key, mood, and structure"; timestamped sections `[0:00 - 0:10]`; section tags `[Verse]`, `[Chorus]`, `[Bridge]`; "Instrumental only, no vocals"; up to 10 images may be sent with the text [V, S13] | "Iterative editing or refining a generated clip through multiple prompts is not supported"; "Results may vary between calls, even with the same prompt" [V, S13] | "Google won't claim ownership" of generated content; "You're responsible for your use of generated content"; Google "may generate the same or similar content for others"; users 18+ [V, S16]. On unpaid use (AI Studio, free quota) Google uses what you submit to improve its products; on paid use it does not [V, S16] (pass 2). SynthID watermark in all output [V, S13]. Blocks "specific artist voices" and "copyrighted lyrics" [V, S13] |
| **Lyria RealTime** (`lyria-realtime-exp`, "an experimental model") [V, S14] | Gemini API; price not listed on the pricing page [U, S15] | Continuous stream; 48 kHz stereo 16-bit PCM [V, S14] | — | BPM 60–200, `scale` (12 named key-and-mode values plus "unspecified"), density 0–1, brightness 0–1, seed, guidance 0–6, temperature 0–3, `mute_bass`, `mute_drums`, `only_bass_and_drums` [V, S14] (corrected, pass 2: first written "13 choices") | Same seed, BPM and scale reproduce a feel, not a tune [J] | "The model generates instrumental music only"; output "always watermarked" [V, S14] |
| **Stable Audio 3.0** (20 May 2026): Small SFX, Small, Medium (open weights), Large (paid API, or an enterprise licence above $1M revenue) [V-sec, S19; V, S17 lists Small and Medium weights for download] | Web app, API; open weights free under the Community Licence for "less than $1M in annual revenue" [V, S18] | Small and Small SFX up to 2 min; Medium and Large 6 min 20 s [V-sec, S19]; Stability's own page says "up to six minutes" [V, S17] | — | — | "Modify a segment of a track, rework part of a song, or extend your composition" [V, S17] | Community Licence: "you own outputs", used in compliance with the law and Stability's acceptable-use policy; the licence is revocable if you break it [V, S18]; "trained on fully licensed data"; indemnity only "under our Enterprise license" [V, S17] |
| **Adobe Firefly Generate Music** ("now broadly available", 20 Aug 2026) [V, S20] | Firefly plans [U on which plans]; the Firefly AI Assistant has "a free experience with daily generations", not stated to include music [V, S20] (corrected) | "tuned to your video's length and mood" [V, S20] | Not mentioned [U] | Not mentioned [U] | — | "universally licensed original tracks", "commercially safe and ready for finished work", "without worrying about takedowns" [V, S20]; read the plan terms before a festival or broadcast [J] |
| **ACE-Step 1.5** (open; XL variant 2 Apr 2026) [V, S21] | Free, on your own computer or in ComfyUI (a free app for running open models; an official ACE-Step partner). Graphics memory (VRAM): 6–8 GB runs a light setup; 6 GB or less works with the language model switched off and CPU offload; XL needs "≥12GB VRAM (with offload + quantization) or ≥20GB (without offload)" [V, S21] (corrected; pass 2) | "10 seconds to 10 minutes (600s)": nothing shorter than 10 s [V, S21] (pass 2) | Track separation and multi-track generation ("Add layers like Suno Studio's 'Add Layer' feature") [V, S21] | BPM, key/scale and time signature as fields; can also read BPM and key from an audio file [V, S21] | Cover, repaint (redo one part), LoRA (a small add-on trained on your own pieces: "8 songs, 1 hour on 3090 (12GB VRAM)") [V, S21]; a separate "extend" mode is not listed on the README [U] (pass 2) | MIT licence [V, S21]; training data not stated [U]. The README warns of "unintentional copyright infringement due to stylistic similarity" and asks users to "verify the originality of generated works" and "clearly disclose AI involvement" [V, S21] (pass 2) |

Stem splitters for any finished track: Suno Studio, ElevenLabs stem separation [V, S3, S12], and the free Demucs (MIT; four stems: drums, bass, vocals, other; an experimental six-stem model adds guitar and piano, "the piano source is not working great"). Meta's repository was archived on 1 Jan 2025 and is "not maintained anymore"; its author keeps a fork for "important bug fixes" [V, S32].

### 2.2 Sound-effect generators

| Tool | What it does | Limits and price | Licence |
|---|---|---|---|
| **ElevenLabs Sound Effects** | Text-to-SFX; "looping" for sounds that repeat "without perceptible start/end points"; a "prompt influence" setting (high = more literal) [V, S11] | 30 s per generation; "40 credits per second when duration is specified"; MP3 for all effects, WAV 48 kHz for non-looping effects [V, S11] | Plan terms; the docs say nothing on licence [U] |
| **Stable Audio 3.0 Small SFX** | Text-to-SFX, open weights [V, S19] | Up to 2 min [V, S19] | Community Licence [V, S18] |
| **Adobe Firefly Generate Sound Effects** | Sounds that "match the action, timing and energy of your content" [V, S20] | — | "commercially safe" [V, S20] |
| **Native audio in video models** | Effects made with the clip (C1 §3A) | 0.2–0.44 s picture offsets measured in early-2026 models (C3 §7D) | The video model's terms (C1) |

### 2.3 Video-to-audio (V2A) models

| Model | Where | Price | Licence and limits |
|---|---|---|---|
| **MMAudio** | Open (github); fal as `mmaudio-v2` | fal: $0.001 per second, "1-30 seconds configurable" [V, S23] | Code MIT, **weights CC BY-NC 4.0** [V, S22]; fal's page nevertheless says "License: Commercial use permitted" [V, S23]; whether fal holds a separate commercial licence from the authors is not stated [U] (pass 2). Documented failures: "unintelligible human speech-like sounds", "background music", unfamiliar concepts ("it can generate 'gunfires' but not 'RPG firing'"); trained at 8 s, and "a large deviation from the training duration may result in a lower quality" [V, S22] |
| **HunyuanVideo-Foley** (Tencent) | Open weights | — | Tencent Hunyuan Community License: "DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA"; "Tencent claims no rights in Outputs You generate. You and Your users are solely responsible for Outputs"; a separate licence is needed only above 100 million monthly active users [V, S24] (pass 2) |
| **Sonilo v1.1** | fal | "$0.009 per second of output and per sample" (each extra sample costs again); maximum length not stated [V, S25; U on length] | "synchronized, royalty-free sound effects timed to visible actions", "for commercial use" [V, S25] |
| **Mirelo SFX v1** | fal | $0.007 per second of output and per sample; maximum length not stated [V, S26; U on length] | "Commercial use" listed [V, S26] |

**Cost sense [J]:** one V2A pass, one sample, over every second of a 20-minute film costs about 1,200 s × $0.009 ≈ $11 on Sonilo; three samples to choose from cost about $32. A3 estimates *The Catch* at about 40 minutes (runtime is an open conflict, D13), so double these. Money is not the constraint; checking time is.

### 2.4 Libraries

| Library | Licence | Film use |
|---|---|---|
| **Freesound** | Each sound is CC0, CC BY, CC BY-NC, or Sampling+ ("being phased out") [V, S27] | CC0 and CC BY yes (credit for BY); **CC BY-NC: "you can't earn any money with the piece of work you create"** [V, S27]. Credit sentence, as the FAQ gives it: "This [video/theatre piece/...] uses these sounds from freesound: 'sound1' by user1 (http://freesound.org/s/soundID/) licensed under [licence]"; for many sounds: "This [video/theatre piece/...] uses many sounds from freesound, for the full list see here: [link to your credits page]" [V, S27] (corrected; pass 2: second sentence quoted) |
| **Sonniss GDC Game Audio Bundles** (2015–2024) | "royalty free and commercially usable"; "No attribution required"; "unlimited number of projects for the rest of your lifetime"; covers games, film, TV and more; "AI/ML training is strictly prohibited" [V, S28] | Yes |
| **BBC Sound Effects** | RemArc licence: personal, educational, research only; commercial licences sold through Pro Sound Effects [V-sec, S29; primary page unreachable again on 2026-09-27] | No, unless licensed separately [V-sec] |
| **YouTube Audio Library** | "copyright-safe"; "won't be claimed by a rights holder through the Content ID system" (YouTube's automatic copyright matching); Creative Commons tracks need the artist credited in the video description; YouTube "is not responsible" for "royalty-free" music from other channels or libraries [V, S30] | On YouTube yes; use elsewhere is not stated on that page [U] |
| **Pixabay** | Free, no attribution needed; content may be modified; no sale or distribution "on a Standalone basis" [V, S31] | Read the full licence first; the summary has no music-specific terms [V, S31] |

---

## 3. Decision rules

**Policy**
1. **If** the text or the director gives no reason for score, **then** set `music_policy: none` and let beds, motifs and ruptures carry the film, **because** "music tells the audience how to read faces" (A4 SND5) and an unscored film keeps its ruptures clean [J] (corrected, pass 2: the A4 wording was misquoted).
2. **If** music is heard by characters (a radio, a hummed tune), **then** it is `source` music: record or generate it as a sound in the scene, with a perspective preset, **because** it obeys the story's space, not the edit [J; A4 §7.2].
3. **If** the policy is `sparse`, **then** allow at most three cues in a short film (here: under about 40 minutes [J]; for a longer film set `cue_budget` with the user), each at a paragraph break (title, act change, end), never under a reveal whose meaning should stay open, **because** each added cue lowers the value of the others [J; A4 §7.6, P10].
4. **If** the policy is `none`, **then** a tonal bed or drone is allowed only when a source in the world makes it (ship hum, motor, room resonance), **because** an unmotivated drone is score by another name [J].
4a. **If** the policy is `none` or `sparse` and the text names a device that could play music but does not say it does (*The Catch* SC02: "Behind one, a radio, far off."), **then** fill it with indistinct speech or an unrecognizable murmur, never a recognizable tune, and list it for the user, **because** recognizable radio music is source music: it needs a licence and it counts against the policy [J].
4b. **If** the user picks `end_credits_only`, **then** the credits cue enters only after the film's last motif statement has ended or receded (never under it), **because** B4 M10 says of the pump "Never put score over it" and A4 SND8 forbids cutting it off mid-pattern [J].

**Choosing a music tool**
5. **If** the film will go to festivals, streaming or broadcast, **then** use a tool whose terms cover film on the plan you pay for (Suno Pro or Premier, downloading every final while the subscription is active; Lyria via the paid API; Stable Audio under its licence; ACE-Step; Adobe Firefly after reading the plan; or ElevenLabs Enterprise Music, not Enterprise Music Lite), and never a free tier, **because** Suno trial downloads carry no commercial rights, Suno grants rights for songs downloaded "as a paying subscriber", and every ElevenLabs tier below Enterprise Music excludes film, whatever its documentation page says [V, S1, S2, S10, S8] (pass 2). Whether Google's and Stability's terms suit a film is this file's reading of general ownership clauses, not an explicit film grant [J; D4 decides].
5a. **If** a cue is AI-generated, **then** never register it with a Content ID or other fingerprinting service and never claim it as exclusive, **because** Google "may generate the same or similar content for others" and ElevenLabs output "may be similar or identical to Output returned to other users" [V, S16, S9; J].
5b. **If** you use Lyria through the Gemini API and send anything from the unreleased film (storyboard frames as image inputs, scene text), **then** use a paid API key, not the free AI Studio quota, **because** Google uses unpaid submissions to improve its products and does not use paid ones [V, S16; J] (pass 2).
6. **If** you need to set tempo and key exactly, **then** use ACE-Step (BPM, key and time-signature fields), Lyria RealTime (BPM, scale) or Suno Studio's Manual BPM, **because** they expose those controls; others only read them from prompt text [V, S21, S14, S4].
7. **If** a theme must return, **then** make its master once, in one tool, and make variations from that master (§4.5), **because** text-only regeneration gives a new tune each call [V, S13].
8. **If** a tool or tier cannot export for commercial use (Udio; Suno Free, whose up to 7 lifetime trial downloads are "not eligible for commercial use"), **then** do not use it for anything that must reach the timeline, **because** you cannot conform what you cannot download or clear [V, S6, S1] (corrected: this rule first named v6-mini, a model that paid plans can also use).

**Timing**
9. **If** a cue has hit points, **then** choose the tempo from them: BPM = 60 × beats ÷ seconds between hits; at 24 fps one beat lasts 1440 ÷ BPM frames, **because** a cue whose beats fall on cuts feels composed for the picture [J; arithmetic].
10. **If** generating a cue, **then** ask for 4 s more than the spot needs and a clean ending tail, **because** music, like picture, needs handles to trim [J; A4 R2].
11. **If** picture changes after a cue was made, **then** first try cutting the cue on bar lines (every 240 ÷ BPM seconds in 4/4) before regenerating, **because** a bar-line cut is inaudible and keeps the approved take [J].

**Motifs and sound effects**
12. **If** a sound recurs in the text, **then** build one master file, write its signature in frames, and make every appearance from it with a preset (§4.6), **because** with native audio "the same exact rhythm repeated across clips is unlikely" (B4 §14.2) (corrected quotation).
12a. **If** an effect or motif is heard through a device that also carries voices (tablet, earpiece, radio, intercom, glass), **then** use D3 §8.1's chain of the same name (`device_speaker`, `earpiece`, `radio`, `intercom`, `through_glass`), **because** the audience hears one speaker, and in SC15 Jude's whisper and the pump come out of the same tablet [J; D3 §8.1].
13. **If** an effect is ordinary (door, footsteps, rain, crowd), **then** use a library first (Sonniss, Freesound CC0 or CC BY), **because** recorded sound is exact, cheap and cleared [J; S27, S28].
14. **If** an effect does not exist in the world (the figure's engine, a crossing, the ship's hum), **then** generate it or design it from recorded parts once, and store it as a master, **because** a library will not have it and regeneration drifts [J].
15. **If** a shot is silent from a silent model (C1 rule 22) and has many small actions, **then** try V2A for a first pass and replace the key sounds by hand, **because** V2A is fast but invents sounds and music [V, S22; J].
16. **If** hands, cloth or breath must be felt (A4 §7.1), **then** record foley at home with a phone (§4.7), **because** these sounds are intimate, easy to perform, and poorly made by models [J].
17. **If** using an open V2A model, **then** read the weights' licence, not the host's label, and follow the stricter, **because** MMAudio's weights are non-commercial while a host marks it "Commercial use" [V, S22, S23; J].
18. **If** you live or will distribute in the EU, UK or South Korea, **then** do not use HunyuanVideo-Foley, **because** its licence "DOES NOT APPLY" there [V, S24; J on distribution].

**Rights**
19. **If** a sound is CC BY-NC, **then** keep it out of any film that is sold, monetized, or entered where fees or prizes apply, **because** BY-NC forbids earning money with the work [V, S27; J on festivals: check D4]. **If** a file from any library is marked ND ("no derivatives") and you will filter, cut or pitch it, **then** reject it, **because** ND forbids changes (D4 rule 15) (pass 2).
20. **If** music or effects are AI-generated, **then** log the tool, version, plan and date, keep any watermark (SynthID, Google's inaudible watermark, in Lyria output), and add the AI-use line from D4, **because** prompts alone do not make you the author (US Copyright Office, 29 Jan 2025) and disclosure rules are D4's [V, S34, S13].

---

## 4. Procedures (the LLM does the work; you listen and decide)

### 4.1 Set the music policy (checkpoint B, 5 minutes)

1. The LLM reads A4's `rupture` list, B4's sound motifs and every text sound mark, and writes the options with one paragraph each: `none`, `sparse` (naming the one to three candidate places), `end_credits_only`, `scored`; plus `source_only` if characters hear music.
2. For each option it states what the music would compete with (for example "the pump's only S3 at the end").
3. It lists every device in the text that could play music (radios, televisions, speakers) and what it proposes each plays (rule 4a).
4. You answer with one word. The LLM writes `SOUNDPLAN.music_policy` (human authority: no stage may change it).

Say to the LLM: *"Using D9 §4.1, write the music-policy options for this film against A4's rupture list and B4's sound motifs. One paragraph each, then list every device in the text that could play music. Stop and wait for my one-word answer."*

### 4.2 Spot the cues (per sequence, 10 minutes)

1. The LLM lists candidate cue places using A4's rules: enter on a motion or cut; exit before or on a rupture; none under open reveals.
2. For each, it fills the spotting sheet row (§5): `cue_id`, `in`, `out`, `function`, `must_not`, `hit_points`, `length_s`.
3. It checks the policy budget and deletes the weakest rows first.
4. You approve rows as "keep" or "cut". A cue survives only if you can say its `function` in five words.

Say: *"Spot cues for SC10 to SC11 under policy sparse, cue budget 1, using D9 §4.2. One spotting-sheet row per candidate with every §5 field; weakest first if you must cut."*

`function` values [J]: `title` (under a title or chapter card), `transition` (carries a time or place jump), `montage_pace` (sets the cutting rhythm), `counterpoint` (indifferent to the emotion, A4's anempathetic), `tension` (holds a wait), `release` (lets tension go), `end_credits`, `source` (music in the world).

### 4.3 Turn a spotted cue into a generator prompt

The LLM fills this template from the row. Keep it to what the tool documents (Lyria: instruments, BPM, key, mood, structure, timestamps [V, S13]).

```
Instrumental only, no vocals. About <length_s + 4> seconds.
Tempo <BPM> BPM, steady, no tempo changes. Key: <key>.
Instruments: <two to four, plainly named>.
Shape: [0:00-0:<a>] <quiet start>; [0:<a>-0:<b>] <development>; [0:<b>-end] <ending: one sustained note that decays naturally over 3 seconds>.
Texture: <sparse | medium>; no drums <if wanted>; no sound effects.
```

Rules for the words [J]: describe sound, not the character's feelings (the `must_not` usually forbids stating subtext); no artist names, song, album or film titles, labels or lyrics (ElevenLabs forbids them in its terms, Lyria's filter blocks artist voices and copyrighted lyrics [V, S9, S13]); give two or three texture words at most. Make three takes; keep the one that fits the hit points on an animatic, not the one that sounds best alone.

**Per tool [J, from the §2.1 facts]:**
- **Lyria 3.5 (API):** paste the template as it is; the timestamps and "Instrumental only, no vocals" are Google's own advice.
- **ElevenLabs Music:** paste the template; set the length in the length control, not only in the text; remember the plan must be Enterprise Music for a film.
- **Suno (Pro or Premier):** put the instrument, tempo, key and texture words in the style field, switch the song to instrumental (field and switch names not checked [U]), and use Studio's Manual BPM if the cue must hold a tempo; download while subscribed.
- **ACE-Step:** type BPM, key and time signature into their fields, not the text; put the shape and instruments in the text.
- **Lyria RealTime:** set `bpm`, `scale`, `density` and `brightness` as numbers and use the text only for instruments and mood; record the stream.

**Length per tool (pass 2) [V, S13, S8, S21; J on trimming]:** a cue shorter than the tool's minimum is made longer and trimmed on a bar line (rule 11), keeping the tail.
- **If** the cue is under 30 s and you use **Lyria 3 Clip**, **then** you always get exactly 30 s: ask for the shape in the first `length_s + 4` seconds and ask for silence after it, then trim.
- **If** you use **ACE-Step**, **then** the shortest output is 10 s: a 6-s title cue plus 4 s of handles fits exactly.
- **If** you use **ElevenLabs Music**, **then** any length from 3 s to 5 min can be set (film use needs Enterprise Music).
- **If** you use **Lyria 3.5**, **then** say the length in the prompt ("About 10 seconds"); it defaults to "a couple of minutes".

### 4.4 Temp score for the animatic, then re-spot after picture lock

1. **Temp.** Lay temp cues from a source whose licence you already hold (a Suno Pro draft, a Sonniss or YouTube-library track), and name every file `TEMP_` so none can ship. Never temp with commercial film scores [J].
2. **Watch twice.** Once with no music, once with temp. Ask of every cue: "Did the music tell me what to feel before the face did?" If yes, cut the cue (A4 §4.2).
3. **Guard against attachment.** Before replacing a temp, write the cue's `function` and `must_not` again from scratch, and prompt the final from those words, not from the temp's sound [J].
4. **Re-spot after lock** (A4 §7.6): export the locked cut's shot times; the LLM recomputes each cue's `in`, `out`, `length_s`, hit points and BPM (rule 9); cues whose length changed by less than a bar are cut on bar lines (rule 11); the rest are regenerated from the same prompt, or, for a theme, re-made from the master (§4.5).
5. **Mark status** `locked` when the cue plays on the locked cut with its tail intact.
6. **If anything changes after lock**, re-run step 4, because music is one of the files that "drift silently" (D8-R7).

Say (step 4): *"Here is the locked cut's shot list with times. Using D9 §4.4 step 4 and rules 9 to 11, recompute every cue's in, out, length, hit points and BPM. For each cue say: keep, cut on bar lines (give the cut times), or regenerate."*

### 4.5 A theme and its variations without drift

1. **Make the master once.** Generate an instrumental theme of 20–40 s at a fixed BPM and key in one tool; split its stems; save as `TH-01_master.wav` plus stems. Write down: BPM, key, the melody's instrument, the bar count.
2. **Make variations by processing the master's stems** [J]:
   - `fragment`: first two bars only.
   - `solo_line`: the melody stem alone, other stems muted.
   - `slowed`: tempo down by at most about 15% with a tempo-only change (Audacity "Change Tempo ... without changing its pitch" [V, S33]).
   - `transposed`: pitch up or down two to five semitones (a semitone is one piano key) ("Change Pitch" [V, S33]).
   - `filtered`: the whole master through a preset (distance, radio, wall).
3. **Only if processing cannot do it**, use the master as the input to a reference-guided tool: ElevenLabs Audio Reference, ACE-Step cover or repaint, Suno extend or remix [V, S8, S21, S2].
4. **Hum test** [J]: someone who has heard the master once must be able to hum along with the variation. If they cannot, reject it.
5. The LLM keeps the theme register (§5) and refuses any cue marked with a `theme_id` whose file was not made from the master.

### 4.6 Build a sound-motif master and its presets

1. **Get the raw sound once**: record it (phone, quiet room, 20 takes), take it from a cleared library, or generate it (ElevenLabs SFX, Stable Audio Small SFX). Choose one take.
2. **Build the signature** in an editor (Audacity or Resolve's Fairlight page, A4 §14): place the pieces on exact frame counts at 24 fps, so later sync (synchresis, A4 §7.1) can land on frames.
3. **Save the master dry**: no reverb, no filter, 48 kHz (samples per second) WAV, with a written signature in `SOUND.signature`.
4. **Define presets once** per film; the LLM writes each as Audacity steps (effects named as in Audacity's manual: High-Pass Filter, Low-Pass Filter, Filter Curve EQ, Bass and Treble, Reverb, Echo, Distortion, Loudness Normalization [V, S33]) or as an ffmpeg command (D3 §8.1's recipe). Device presets use D3 §8.1's names and values, so a voice and an effect from the same device sound alike (rule 12a) (corrected: this table first had its own device names and values). Starting values [J]:

| Preset | Processing (starting values) | Use |
|---|---|---|
| `dry_close` | none | on-screen, close |
| `room` | Reverb sized to the location (D3's `direct`) | on-screen, in the room |
| `off_screen` | D3: "slightly more reverb, 1–3 dB lower"; lows kept | acousmatic, in the same room |
| `device_speaker` | D3: High-Pass 500 Hz, Low-Pass 5 kHz, slight Distortion | tablet, wrist unit, monitor |
| `earpiece` | D3: High-Pass 400 Hz, Low-Pass 3.4 kHz, light saturation (mild distortion), gentle compression, no reverb | earpiece |
| `radio` | D3: band-pass 300–3,400 Hz (both filters), more saturation, a peak near 1.8 kHz | radio |
| `through_glass` | D3: Low-Pass 1–1.5 kHz, 12 dB down; "non-verbal sound only" | the quarantine glass (SC11–SC13, SC17, SC29, and SC30, whose text also has "Beyond the glass", l.1818; D3 lists only the first five) (pass 2) |
| `through_wall` | Low-Pass 800 Hz | next room |
| `through_suit` | Low-Pass 1 kHz, bass boost (Bass and Treble), very short small-space reverb | a sound outside a suit heard by its wearer, felt through the body (the pump against Iona's chest in SC27). Not D3's `helmet_internal`, which is the wearer's own voice |
| `far_below` | Low-Pass 2 kHz, quieter, long thin Echo | down a shaft or borehole |
| `over_black` | the scene's last preset, with the room bed faded out | after a cut to black |

5. **Place copies, never edit the master.** Each shot's `sound.motif` names the motif, preset and `sound_emphasis`; the level is set in the mix, not baked into the file.

Say: *"Using D9 §4.6, write each preset in `SOUNDPLAN.presets` as numbered Audacity steps a beginner can follow, with the menu name of every effect and its values, and as one ffmpeg command. Reuse D3's chain wherever the name matches."*

### 4.7 Sound effects: library, generation, video-to-audio, foley

1. **List** every `sync_fx` and `offscreen` item from the shot specs (A4 §10).
2. **Sort**: ordinary → library; invented → generated master (rule 14); hands, cloth, breath, small objects → foley.
3. **Library search**: the LLM writes three search words per item; on Freesound filter by licence to CC0 or CC BY, and paste the credit line into the licence log as you download [V, S27].

   *The Catch*'s scripted sounds outside the motifs, sorted (pass 2). Every capitalised sound word must end up as an `effect` item, a room sound or a motif appearance in its scene, or the blueprint's check COVER-07 fails. Quotations checked against the script; sorting [J]:

| Scene | Exact text | Sort | Source and note |
|---|---|---|---|
| SC02 | "Her hand closes on a rung and the rung TURNS." | library or record | a metal bar turning in a loose socket; `dry_close`, inside the shaft's reverb |
| SC02 | "Behind one, a radio, far off." | library, not music | indistinct speech, `through_wall` then `far_below` (rule 4a) |
| SC04 | "A GUNSHOT. Down the corridor, the stair door jumps against the chair." | library | an indoor pistol shot plus a door rattle; `off_screen` (the shooter is not seen) |
| SC06 | "Someone KICKS the top gate open and FIRES down through the roof." | library | kick and shots from far above: `far_below` in reverse (distant, thin, long echo) |
| SC06 | "The cage STOPS DEAD." | library, layered | a heavy metal impact plus a cable twang; `dry_close` (the camera is bolted in the cage) |
| SC06 | "gives one long METAL SHRIEK and lets go of the wall." | library, layered | metal stress and tearing; the loudest non-motif sound before the CLACK |
| SC16 | "A thin WHITE JET shoots from underneath it." | library or generated | a short high gas hiss; the figure's body, so make it once and store it (rule 14) |
| SC16 | "An ALARM starts up next door." | library | a hospital or lab alarm through a wall: `through_wall` |

   Note: a text step may refuse the word "gunshot"; state once that this is pre-production and say "gunshot sound effect", as blueprint §13.6 advises (it calls it "SC06's gunshot"; the script's GUNSHOT is in SC04, l.172, and SC06 has "FIRES", l.216).
4. **Home foley** [J]: a phone in a closet or under a duvet (dead sound); 30 cm from the action; record each action five times while watching the clip on a laptop; sort by the best match; name files by shot ID (`CATCH_SC30_SH050_cloth-fold_FOLEY-T03.wav`, C5 file names). Slide each take in the editor until its transient sits on the frame where the action lands. *The Catch*'s hand and cloth list, with a home way to perform each:

| Scene | Exact text | Perform it with [J] |
|---|---|---|
| SC06 | "She catches it. Her palm drags across the bright steel." | a bare palm pushed hard along a steel baking tray or sink edge |
| SC11 | "The nurse snaps a plastic band round Iona's wrist." | a plastic cable tie or hospital-style band snapped shut near the phone |
| SC25 | "She takes the roll of repair tape from her suit and seals it." | duct tape pulled off the roll and pressed down with a thumb |
| SC27 | "Her other hand grips the strap until the glove creaks." | a leather or rubber glove squeezed round a bag strap; then `through_suit` |
| SC30 | "She takes a clean cloth. Folds it." | a cotton tea towel folded twice, slowly, close to the phone |
| SC30 | "Then she lifts the vessel just enough to slide the cloth beneath it." | a glass jar lifted off a metal tray and set down on the folded towel: the tap disappears |

5. **V2A pass** (optional, for busy silent shots): run the clip; then the V2A check:
   - every listed `sync_fx` is present;
   - each lands within 2 frames of its visible cause [J], given the 0.2–0.44 s offsets found in early-2026 models (C3 §7D);
   - no music, no speech-like murmur (MMAudio documents both [V, S22]);
   - nothing sounds where nothing happens;
   - no sound that would give away a `withholds` item (A4 S3).
   Fail on any line: keep only the good sounds, or replace by hand. Record `v2a_check`.
   How to check "within 2 frames" without a sound engineer [J]: in the editor, zoom the timeline until single frames show, put the playhead on the frame where the hand, door or foot makes contact, and look at whether the start of the sound's waveform (the transient) sits on that frame; drag the clip if not.
6. **Never keep** a generated motif occurrence; lay the master copy instead (rule 12).

Say: *"Using D9 §4.7, list every sync_fx and offscreen item in SC25 to SC30, sort each into library, generated master, or foley, and give three Freesound search words for each library item."*

### 4.8 A film with no score: carrying tension

| What a score would do | What sound does instead (A4 references) |
|---|---|
| Set the pace | A rhythmic world source (drill, pump, hum, footsteps) and cutting on it (WE4) |
| Build a wait over a static shot | A rising or ticking source; a sound approaching unseen (§7.1, SND1–2) |
| Mark a turn | One rupture: a drop-out, or a constant sound stopping (the ship's hum in SC26) |
| Mark a paragraph break | A cut to black the text writes, and a change of bed (T4) |
| Release tension | An ordinary bed returning (street, birds), a breath |
| Join scenes | J-cuts and L-cuts (SND6) |
| Carry memory | Motif statements at changing `sound_emphasis` |
| A felt low drone | A diegetic drone with a source (the ship's hum; the Ninth Room's 110 Hz) |

Silence grades and "room tone plus one small sound" stay as A4 §7.5 and SND4 set them.

### 4.9 Licence log and credits

1. Every file gets a `SOUND` record (§5) the moment it is downloaded or made.
2. Before export, the LLM lists every record with `commercial_ok` or `film_ok` not `yes` and every CC BY item's credit line.
3. The end card carries CC BY credits in Freesound's sentence ("This film uses these sounds from freesound: 'sound1' by user1 (http://freesound.org/s/soundID/) licensed under CC BY 4.0", or, for many sounds, "This film uses many sounds from freesound, for the full list see here: [your credits page]" [V, S27]) and D4's credit line, whose template already has slots for sound: "... voices with [tool]; sound effects from [libraries]" (D4 §5 recipes). Add "music generated with [tool]" or "music by [composer]" to that line; do not write a second, different AI line [J; D4 principle 8, one wording everywhere].
4. Keep downloaded terms pages (PDF or screenshot, dated) in `rights/`, and name each in the asset's `terms_file`, because plans change monthly (Suno changed download rules on 3 Sep 2026 [V, S2]).
5. For a Suno final, write the plan and the download date in the record: rights follow songs downloaded "as a paying subscriber" [V, S2].

---

## 5. Fields this file adds to the breakdown

Enums are lowercase snake_case; `none`, never empty. **Names follow the build blueprint** (`design/blueprint.md`, which wins over the designs; it was written before this file): the film-level sound record is the blueprint's singleton `SOUNDPLAN`; a music cue is a blueprint `MUSIC` record with ID `MU-` + 2 digits; licences go in blueprint `RIGHTS` records (`RT-` + 3 digits); motifs are `MO-` (A4's `MOT_`) with `channel: sound` and `signature`. Sound-effect assets use `SFX-` (not `FX-`, which the blueprint reserves for finishing jobs); ambience beds `AMB-` (A4's `AMB_`) and themes `TH-` are proposals the blueprint does not yet have, as is the per-file `SOUND` asset record below (corrected: this file first used `SYS-SOUND`, `CUE-SC##-##` and `FX-`). A4's `music.policy` values `score`, `source only` map to `scored`, `source_only`. **Shot-level names (pass 2):** A4's `sync_fx` list is the blueprint's shot `sound` → `effect` items (`<what> | at: <seconds> | sound_emphasis: 0-3`); a motif copy in a shot is a blueprint `MOTIF` `appearance` (with `sound_emphasis: 0-3`); the shot's music is the blueprint's `sound` → `music` (`none` or an `MU-` ID). The shot rows below extend those blueprint fields and do not replace them.

| Level | Field | Meaning | Allowed values |
|---|---|---|---|
| film (`SOUNDPLAN`) | `music_policy` | The film's music rule, set by the user at checkpoint B | `none` `source_only` `sparse` `end_credits_only` `scored` |
| film | `cue_budget` | Most cues allowed | integer; `sparse` ≤ 3 in a short film [J] |
| film | `tonal_centre` | One home note that cues and tonal beds agree with | note name (`a`) or `none` |
| film | `presets[]` | Named processing chains (§4.6); device chains shared with D3 `path_presets[]` | `dry_close` `room` `off_screen` `device_speaker` `earpiece` `radio` `through_glass` `through_wall` `through_suit` `far_below` `over_black`, plus film-specific names |
| film | `source_devices[]` | Devices in the text that could play music (rule 4a) | `{scene, exact_text, plays}`; `plays` is `speech_murmur`, a `MU-` ID, or `none` |
| film | `theme_register[]` | Each theme's master | `{theme_id: TH-##, master_file, bpm, key, bars, allowed_variations}` |
| film (`MUSIC` records) | `music.cues[]` (A4) = blueprint `MUSIC` | One spotted cue; the shot's `music` field names its `MU-` ID | `{cue_id: MU-##, in, out, function, must_not, source, theme_id, variation, bpm, key, length_s, hit_points[], temp_file, final_file, status}` |
| cue | `function` | What it does | `title` `transition` `montage_pace` `counterpoint` `tension` `release` `end_credits` `source` |
| cue | `source` | Where it comes from | `generated` `library` `composed` `performed` |
| cue | `variation` | How it differs from the master | `full` `fragment` `solo_line` `slowed` `transposed` `filtered` `none` |
| cue | `status` | Progress | `spotted` `temp` `generated` `approved` `locked` `cut` |
| asset (`SOUND`) | `id`, `kind` | The sound and its type | `MO-` `SFX-` `AMB-` `MU-`; `bed` `motif` `sfx` `foley` `music_cue` |
| asset | `signature` | Fixed pattern in frames or seconds | text ("11 f, 14 f, 29 f rest") |
| asset | `master_file`, `states[]` | The one master; named source states | path; `{state_id, description}` (for a sound that changes, like the drill) |
| asset | `source` | How it was made | `record` `library` `ai_sfx` `ai_music` `v2a` `native` |
| asset | `tool`, `tool_version`, `plan`, `made_on` | For AI or library sources | text; date |
| asset | `licence`, `licence_url`, `attribution_text` | The terms | `cc0` `cc_by` `cc_by_nc` `royalty_free` `plan_terms` `open_weights` `own_recording` `unknown`; URL; exact credit line |
| asset | `terms_file`, `downloaded_on` | The dated copy of the terms in `rights/`; the day the file was downloaded (Suno rights follow the plan on that day) | path; date |
| asset | `commercial_ok`, `film_ok` | Cleared for sale; cleared for film | `yes` `no` `check` |
| asset | `ai_generated` | For disclosure (D4) | `yes` `no` |
| asset | `must_not` | What no later stage may change (a plant rule) | text ("no bounce, no roll: plants 'It is a cylinder. They stand, or they roll.'") or `none` |
| asset | → `RIGHTS` | Each asset's licence fields are also written as a blueprint `RIGHTS` record (`subject: music`, `stock` for library effects, or `model_terms` for AI output) | `RT-` ID |
| shot | `sound.motif` (extends A4) | A motif copy in this shot | `{id, preset, sound_emphasis: 0-3, sync_to: <visible event> or none}`; `preset` is a `presets[]` name |
| shot | `sound.sync_fx[].source` | Origin of each synced effect | `native` `library` `ai_sfx` `v2a` `foley` `record` |
| shot | `sound.v2a_check` | Result of §4.7 step 5 | `pass` `fail` `not_run` |

---

## 6. Checklists

**Spotting sheet** (a "no" needs a fix or a reason)
- Does the number of cues fit `music_policy` and `cue_budget`?
- Does every cue enter on a motion or cut and leave before or on a rupture?
- Is there no cue under an open reveal, under a motif at emphasis 3, or under a text-marked silence?
- Does each cue have a five-word `function` and a `must_not`?
- Are BPM and hit points computed, with 4 s extra length?
- Do all cues share the `tonal_centre` or a named reason?

**Generated cue**
- Instrumental, no vocal murmurs, no drums unless asked?
- Tempo steady (no drift) across the cue?
- Ends with a clean tail?
- Passes the hum test if it carries a `theme_id`?
- Tool, plan and licence logged; plan covers film; `terms_file` saved; for Suno, downloaded while subscribed?

**Motif asset**
- One master, dry, 48 kHz, signature written in frames?
- Every occurrence made from the master with a named preset?
- `sound_emphasis` 3 used once per motif (B4 §3.4)? (corrected reference)
- Never cut mid-pattern at the end (A4 SND8)?

**Sound effects and V2A**
- Every `sync_fx` sourced and labeled?
- V2A output passed all five checks?
- Every effect heard through a device uses the same D3 chain as the voices from that device?
- Every radio or speaker the text names has a `source_devices[]` entry (rule 4a)?
- No CC BY-NC, RemArc or free-tier item in a commercial or festival cut?
- Every CC BY credit line in the end card?

---

## 7. Failure modes (sign → cause → fix)

| Sign | Cause | Fix |
|---|---|---|
| Music under a clip nobody asked for | Model default soundtrack (C3 §7E) | "No background music." in every prompt; strip audio in the edit |
| A theme sounds different each time | Regenerated from text | Remake from the master (§4.5) |
| Cue drifts off the cuts after a minute | Tempo drift in generated songs [V, S4] | Suno Studio Manual BPM, a tool with a BPM field, or cut shorter |
| Cue and ship hum sound sour together | Different home notes | Set `tonal_centre`; regenerate in that key or pitch-shift the cue |
| The pump's rhythm changes between scenes | Native audio or regeneration used | Lay the master copy; mute native |
| A murmur like speech in a V2A track | Documented model failure [V, S22] | Replace with library or foley |
| Effect lands a few frames late | Model offset (C3 §7D) | Slide to the frame of the visible cause |
| A sting (sudden music hit) on a reveal | Added signal where the script already marks the beat (B4 rule 23) (corrected reference) | Remove it |
| A motif becomes wallpaper | Too many statements | Drop optional statements (A4 WE3's SC20–24) |
| A sound designer "improves" a planted sound | No `must_not` on the asset | Write the plant rule in the asset's `must_not` (the Long Places knock) |
| Audible loop point in a bed | Short loop repeated | Use a longer bed or a looping-mode generation [V, S11] |
| Takedown or claim after release | Non-commercial or unlicensed item | Licence log check before export (§4.9) |
| Cannot download the final | Walled tool (Udio) or free tier | Rules 5 and 8 |
| A Content ID claim on your own film, or your music claimed by a stranger | AI music registered as exclusive; similar output given to others (Google, ElevenLabs terms) | Never register AI cues (rule 5a); keep the licence log and terms file to dispute |
| The tablet's voice and the tablet's pump sound like two speakers | Voice and effect processed with different chains | One D3 chain per device (rule 12a) |

---

## 8. Worked examples

### 8.1 *The Catch*: three music-policy options against A4's ruptures

The film's ruptures and sound peaks (A4 §11, B4 §9.3): SC06, "A hard metal CLACK." then "BLACK. A dark with nothing in it. One instant." (10 frames, true silence); SC10's text mark "CUT TO BLACK." after "Nobody leave this room.", then the title card "= THE CATCH"; SC13's drop-out as "Jude takes the remote and switches it off."; SC15's point-of-view change to the tablet; SC26's hum stopping ("The sick motor through them." / "Then not."); SC30's "Three uneven strokes in the dark.", the pump's only emphasis 3.

| Option | Where music may go | What it must avoid | Verdict [J] |
|---|---|---|---|
| `none` | Nowhere. Tension from the hum (a gauge, §8.1a), the pump, the CLICK/CLACK family, and silence grades. SC02's "Behind one, a radio, far off." carries murmured speech, not music (rule 4a) | — | **Recommended starting point**: A4 §15 recommends "none or very sparse"; the critic's resolution leaves the choice to the user at checkpoint B (corrected: this row first called `none` the critic's default). Every rupture stays clean, and the pump is the film's heartbeat |
| `sparse`, one cue | Under the title card only: enter on the cut to black after "Nobody leave this room.", play under "= THE CATCH", end on the cut into SC11's morning, before any dialogue. `function: title`; `must_not`: state Iona's fear; carry into SC11 | Any scene after SC14 (it would teach the audience to expect music before the pump's statements); SC27, where A4 WE3 rules that "the helmet is the only place any sound can exist" | Defensible: it marks the one mid-film paragraph break the script writes (the only other "CUT TO BLACK." is the ending), enters on a cut and stops before any dialogue, as A4 §7.6 asks |
| `end_credits_only` | After the last "Three uneven strokes in the dark.", the pump recedes over two or three cycles (A4 §15, question 2); the credits cue enters only in the rest after the pump has gone | Overlapping the last pump statement, which must be heard alone (`sound_emphasis` 3) | Acceptable if the pump recedes; not if it continues under the credits (B4 M10: "Never put score over it"; rule 4b) |

A spotting row for the `sparse` option (the LLM's output; values [J]):

```
cue_id: MU-01   in: first frame of black after "Nobody leave this room."
out: cut into SC11 (card held 4 s)   length_s: 6 + 4 handles   function: title
must_not: state Iona's fear; continue under SC11 dialogue
source: generated   bpm: 60   key: tonal_centre (the ship hum's note, fixed at checkpoint B)
prompt: Instrumental only, no vocals. About 10 seconds. Tempo 60 BPM, steady.
  Key: <tonal_centre> minor. Instruments: low bowed strings, one sustained piano note.
  Shape: [0:00-0:06] a single low chord swelling slowly from silence; [0:06-end]
  the chord decays naturally over 3 seconds. Texture: sparse; no drums; no sound effects.
```

### 8.1a The ship's hum (AMB-HUM): a gauge with states, not a score

Under `none` the hum does the work a low drone would do in a score, but it has a source (rule 4). One master, five states made by processing (`states[]`), each placed where the text writes it:

| Scene | Exact text | State and processing [J] | `sound_emphasis` |
|---|---|---|---|
| SC19 | "Her boots find a ledge. A low HUM comes up through them." | `AMB-HUM.S01` steady, felt more than heard: the master with its lows kept; `through_suit` if she is helmeted here ("lamps on"; confirm the costume phase in B5) | 1 (first statement, clear) |
| SC21 | "Behind the cabinet, cables run into the deck. The steady hum comes through them." | S01, `room` | 0 |
| SC23 | "The hum under the floor wavers." | `S02` wavering: a slow pitch wobble of a few percent (Change Pitch in short steps, or a vibrato plug-in) | 1 |
| SC24 | "The hum misses a beat. The deck drops beneath her, catches itself." | `S03`: S01 with a gap of about 12 frames cut out of it, then back | 2, for the gap only |
| SC26 | "Her boots on the deck. The sick motor through them." / "Then not." | `S04` sick: S02 plus a rough, uneven grind layer; then the rupture: the hum stops on a cut, leaving her breath (`through_suit`) | 2, then silence |

If a cue is ever added (`sparse` or `scored`), its key is the hum's note (`tonal_centre`), so the two never sound sour together (§7). The hum's note is the user's choice at checkpoint B (§9, question 2).

### 8.2 The pump (MO-PUMP, B4 M10): one master, six presets

**Signature.** A4's example, snapped to frames at 24 fps [J]: stroke, 11 frames, stroke, 14 frames, stroke, 29-frame rest. One cycle is 54 frames = 2.25 s, about 27 cycles a minute. Frame-exact strokes let SC25's flap ("opening and closing") be synced stroke for stroke.

**Master.** Record a soft, wet mechanical stroke (for example a hand-squeezed rubber bulb pump in a sink [J]), or generate candidates with a text-to-SFX tool. Keep one stroke take for each of the three positions (the third slightly softer, so "not quite even" is in both timing and weight). Assemble one cycle, dry, 48 kHz. Never regenerate it.

| Scene | Exact text | Preset | `sound_emphasis` |
|---|---|---|---|
| SC15 | "From inside it, a PUMP: three strokes, not quite even." | `device_speaker` (the tablet in Iona's room; the same chain as Jude's whisper, D3) | 1 |
| SC16 | "Behind her: a pump. Three uneven strokes." | `off_screen`, behind her, full-range; J-cut before the figure | 2 |
| SC20–24 | (not written; optional, A4 §15 question 4) | `through_wall`, under the hum | 0 or omit |
| SC25 | "The pump she heard in the dark of her room: the only heart the big body has." | `room`, synced to the flap | 1 (B4: the image carries the reveal) |
| SC27 | "Breath in the helmet. Three uneven strokes against her chest." | `through_suit`, with breath only | 2 |
| SC28 | "The little pump keeps working. Three uneven strokes." | `room` (receiving room), under voices | 1 |
| SC30 | "Each stroke of the pump makes the base of the vessel tap against the metal table." | `room` plus a second asset, `SFX-VESSEL-TAP` (glass on metal), locked to each stroke | 2 |
| SC30 | "The tapping stops." / "The pump goes on." / "Three uneven strokes in the dark." | tap layer removed; room bed faded; then `over_black` | 2 until the cut; 3 over black, once (B4 M10: "the only S3 of the film and its last sound") |

The same master plays in every row; only the preset and level change, as B4 M10 requires. The cut to black falls in a 29-frame rest, so the first sound in the dark is one whole cycle (A4 WE3).

### 8.3 The CLICK/CLACK family (SFX-ENGINE)

One recorded source (a heavy metal latch snapping shut [J]) makes three sizes by processing, with the transient kept identical: `SFX-ENGINE-S` (pitched up, thin, "CLICK"), `SFX-ENGINE-M` (as recorded), `SFX-ENGINE-L` (pitched down, with a low thump layer, "CLACK"). Size follows the mass the engine moves [J]. The script writes the sound only twice (SC06 "CLACK", the puck firing, and SC15 "CLICK"); every other row follows A4 WE3's instruction to give "every engine firing in the film" a member of the family, so those rows are [J] additions to list for the user.

| Scene | Exact text | Member and preset |
|---|---|---|
| SC06 | "A hard metal CLACK." | L, `dry_close`, on the first of 10 black frames, then true silence (A4 WE1) |
| SC12 | "It vanishes before the wood. The needle on the wall kicks." (no sound written) | S, `through_glass` (D3), because the carriage is "Beyond the glass": this teaches the family |
| SC15 | "A small CLICK, from nowhere." | S, `device_speaker` (written) |
| SC18 | "The pod closes. Vanishes. Returns with a black thumbprint on the card." (no sound written) | S twice (out and back), `room` |
| SC23 | "He vanishes." / "They vanish together." (no sound written) | M, `room` |
| SC24 | "She fires." (no sound written) | L, `room`, then the hum's missed beat (`AMB-HUM.S03`) |
| SC27 | "She fires." and "The engine crosses." | L, `through_suit` (no sound from outside; A4 WE3) |

By SC27 the audience knows by ear what just happened, with no visual effect needed (A4 WE3).

### 8.4 *The Long Places*: drill, knock and lullaby, with policy `source_only`

**Proposed policy [J]:** `source_only`. The book's music is sung or hummed in the world: the lullaby in the Chapter II letter, "I hummed the way you hum for a child that is not yours: the tune everyone's mother used, the one nobody owns", and in the 1999 night, where "someone was humming. The tune was the one everyone's mother used — hers, and not hers, as she would one day be told — and it had no words in it, and it paused where the words would be."

- **The lullaby (`MU-01` in that film, `source: performed`).** Record a person humming a traditional lullaby from the story's region, with no words, pausing where the words would be. The book never names the tune or its language; the region is D17's decision (the characters' names suggest Turkey, but that is an inference [J]) (corrected: this line first said "Turkish" as if the text did). A traditional melody may be free of copyright while every existing recording and arrangement is not [J; D4 decides]; so record your own, with the singer's written consent (D3). Do not generate it: the text's point is a tune nobody owns, and a generated melody is a new tune owned by the tool's terms [J]. Preset `through_wall` or `off_screen`: its source is never shown (A4 SND1–2), and the book never settles whose voice it is.
- **The Ninth Room's note sets the tonal centre.** Chapter III: "a low A, one hundred and nine hertz, one hundred ten, felt in the sternum a half-second before the ear agreed." Set `tonal_centre: a` and make the room's resonance a diegetic drone at 110 Hz (rule 4). Hum the lullaby in A, so that in that room it "sings" with the walls. If the user later chooses `sparse`, every cue is prompted in A (Lyria RealTime and ACE-Step take the scale as a field [V, S14, S21]).
- **The drill (`MO-DRILL`, two states).** "For three days the little rig argued with the hill"; "On the third morning the drill's note went hollow." Record or library-source one drilling sound; `MO-DRILL.S01` loaded, `MO-DRILL.S02` hollow, made from S01 by processing [J]: remove the low body with Filter Curve EQ, raise pitch slightly (an unloaded motor speeds up), drop the grinding layer. The change happens over a routine shot, mid-cycle, as A4 WE4's rupture. "You knock loudly" is mixed under the drill.
- **The knock family (`MO-KNOCK`).** One dry flat-hand knock on stone is the master, from which come:
  1. The courtesy (Chapter IV letter: "Knock twice, with the flat of the hand, on the sounding stone, and then wait the length of two breaths"): two copies, `dry_close`, then two breaths of room tone.
  2. The accident (Chapter VII: "a knuckle on wood, once"): one copy, `far_below`, no bounce, no roll. Note on the asset: "must not be improved; plants 'It is a cylinder. They stand, or they roll.'"
  3. The machine: the drill's percussive layer.
  4. The cough in Chapter V ("twice, and then the little knock at the end, like a knuckle on wood"): the master at `sound_emphasis` 1 closes the cough.
  Chapter VIII's letter, "They knocked loudly, with iron that ate downward, a woodpecker noise in the house's bone, for days", pays the motif off over recalled drill images (A4 WE4).
- **The answering niche (Chapter V).** "On the second breath of the after-quiet, something came under the knock. Low. Shaped. With the fall of a sentence in it." `must_not`: be intelligible. Build it from breath and room resonance at 110 Hz; never from a generated voice, which would settle what the book leaves open [J].

---

## 9. Open questions for the user

1. *The Catch*: `none` (recommended starting point), `sparse` (the title cue) or `end_credits_only`? Checkpoint B.
2. *The Catch*: the ship hum's note, which becomes `tonal_centre` if any cue is used.
3. Paid tools: which one plan to buy for music (Suno Pro, Lyria API, Stable Audio, or local ACE-Step)? ElevenLabs Music is out unless you buy Enterprise Music (rule 5).
4. *The Long Places*: whose voice hums the lullaby, and consent in writing (D3)?
5. Festival or online release? This sets which licences are acceptable (D4).
6. *The Catch*: what the SC02 radio plays (murmured speech by default, rule 4a), and whether the [J] engine sounds at SC12, SC18, SC23 and SC24 (no sound written) are wanted.
7. *The Catch*: if `end_credits_only`, does the pump recede before the credits cue (required by rule 4b), or continue under silent credits (A4 §15, question 2)?
8. Hardware: is there a computer with a graphics card of 6 GB or more for ACE-Step, or should music be made online?
9. *The Catch*: the optional pump under the ship scenes SC20–SC24 (A4 §15, question 4): at `sound_emphasis` 0 under the hum, or left out between SC16 and SC25 (default here: left out, so SC25's reveal lands on a sound not heard for five scenes [J]) (pass 2).

---

## 10. Conflicts with other library files, and how this file resolves them

| Topic | Other file says | This file | Status |
|---|---|---|---|
| Music policy values | A4 §10: `score \| sparse \| source only \| none`; blueprint `SOUNDPLAN.music_policy`: `none \| sparse \| scored \| source_only` | Blueprint's four values plus `end_credits_only` for the brief's third option | Proposal: add `end_credits_only`; without it, write `sparse` with `cue_budget: 1` and the one cue's `function: end_credits` [J] |
| When a `MUSIC` record may exist | Blueprint: "only if the policy is sparse or scored"; `source`: `score \| library \| ai` | Under `source_only` the performed lullaby is also a cue; this file's `source` values `generated` `library` `composed` `performed` map to `ai`, `library`, `score` and a new `performed` | Proposal: allow `MUSIC` under `source_only` when `function: source`, and add `performed` [J] |
| Device and helmet names | Blueprint `SPEECH.path` has `device_speaker`, `earpiece`, `radio`, `intercom`, `through_glass`, `off_screen`, `helmet_inside` (the wearer's own voice, D3's `helmet_internal`) | Uses the same names for effects through devices; `through_suit` (an outside sound felt through the suit) is new and is not `helmet_inside` | Resolved here |
| Default policy for *The Catch* | A4 §15: "recommends none or very sparse"; critic: "The user chooses ... at checkpoint B"; blueprint K31: "default none for The Catch", asked at checkpoint B | `none` as the recommended starting point; the user decides | Agrees with the blueprint; needs the user (§9, question 1) (pass 2) |
| Shot sound-effect field | A4 §10 `sync_fx`; blueprint shot `sound` → `effect` (`<what> \| at: <seconds> \| sound_emphasis: 0-3`), at most 3 in a clip prompt's AUDIO block | This file's `sync_fx[].source` and `v2a_check` are added to each blueprint `effect` item | Proposal: add `source` and `v2a_check` to `effect` items [J] (pass 2) |
| D3's record of D9's preset names | D3 §10.5 alignment table and the D3 digest still name D9 presets `earpiece_radio`, `small_speaker`, `helmet_inside` and say D9's `earpiece_radio` "merges two paths D3 keeps apart" | D9 now uses D3's own names and values (`earpiece`, `radio`, `device_speaker`, …); only `through_suit` is new | Stale in D3; update D3's table and digest (pass 2) |
| Licence vocabulary | D4 `asset_licence.licence_id`: `cc0`, `cc_by_4_0`, `cc_by_nc_4_0`, `ofl_1_1`, `provider_terms`, …; D4 `source`: `generated`, `library`, `original`, `public_domain` | `licence`: `cc0`, `cc_by`, `cc_by_nc`, `royalty_free`, `plan_terms`, `open_weights`, `own_recording`, `unknown`; asset `source`: `record`, `library`, `ai_sfx`, `ai_music`, `v2a`, `native` | Open; D4's proposal: one list in the `RIGHTS` record, D9's short names plus a version suffix where a licence has versions (`cc_by_4_0`) (pass 2) |
| ElevenLabs Music and film | ElevenLabs Music docs: "cleared for nearly all commercial uses, from film and television to podcasts"; D13 R19 and D3 follow the Model-Specific Terms | Terms win: film only on Enterprise Music | Resolved here; D13 already agrees (pass 2) |
| Device processing | D3 §8.1 path chains (`device_speaker` HP 500 Hz / LP 5 kHz; `earpiece`; `radio`; `through_glass`; `helmet_internal`) | Device presets reuse D3's names and values; `through_suit` is new and is not D3's `helmet_internal` (the wearer's own voice) | Resolved here (rule 12a) |
| What counts as a sound motif | A4 WE3: the pump, the engine's CLICK/CLACK and the HUM are all motifs; B4 §9.1: the sound channel has one motif, M10 | Pump = `MO-PUMP` (B4 M10); engine = effect family `SFX-ENGINE`; hum = bed with states `AMB-HUM`. All three still use one master each | Resolved here; B4's cap holds [J] |
| Pump signature | A4 §7.4: "stroke, 0.45 s, stroke, 0.6 s, stroke, 1.2 s rest" | 11, 14, 29 frames at 24 fps (0.46, 0.58, 1.21 s) | Frames rule; A4's seconds were an example |
| Record names and ID prefixes | Blueprint §5.3: `SOUNDPLAN` singleton, `MUSIC` records `MU-##`, `RIGHTS` `RT-###`, `MOTIF` `MO-`; `FX-` = finishing jobs; no sound-asset record, no `AMB-` or `TH-` | Now uses `SOUNDPLAN`, `MU-`, `RT-`, `MO-`; renamed its effects `FX-` to `SFX-`; keeps `SFX-`, `AMB-`, `TH-` and a `SOUND` asset record as proposals | Proposals to add to the blueprint's schema and `library/01 What the codes mean.md` [J] |
| Freesound credit | D4 §3 tools table and A4 §14: credit per the FAQ | The FAQ's full sentence (§4.9) | Same source; no conflict |
| AI credit line | D4 §5: one template with voices and sound-effect slots | Adds a music slot to D4's line; no second line | Resolved here |
| *The Catch* runtime | A3 about 40 minutes; C1 costs a 20-minute film (critic conflict) | Cost examples given for both | Open (D13) |
| Lullaby region | *The Long Places* never names it | Region set by D17 | Open (D17) |

---

## Sources

All checked 2026-09-27. Fact-check pass the same day: S1–S4, S6, S8–S28, S30–S35 re-read; S5 and S29 by search excerpts only. Second pass (same day): S1–S6, S8–S11, S13–S28, S30–S34 fetched again; S12 gives no stem options; S29's primary page still unreachable (search excerpts agree: personal, educational or research use only).

- S1 Suno, "An update to our downloads policy and Terms of Service" (10 Aug 2026): https://suno.com/blog/suno-updates-tos
- S2 Suno Help, "Upcoming Changes FAQ: Downloads, Models, and Terms of Service": https://help.suno.com/en/articles/13614785
- S3 Suno pricing: https://suno.com/pricing
- S4 Suno Help, "Fixing Tempo Drift": https://help.suno.com/en/articles/8363457
- S5 Suno, "Introducing v6" release notes (9 Sep 2026; primary, read in pass 2): https://suno.com/release-notes/introducing-v6 . Earlier secondary source: Digital Music News, "Suno Launches v6 Models" (9 Sep 2026; page returned no text on re-fetch, facts confirmed by search excerpts from it and from Music Ally, 9 Sep 2026: https://musically.com/2026/09/09/suno-launches-its-v6-ai-music-models-heres-what-you-need-to-know/): https://www.digitalmusicnews.com/2026/09/09/suno-v6-launch/
- S6 Udio Help, "Changes associated with the UMG partnership" (updated 17 Feb 2026): https://help.udio.com/en/articles/12683565-changes-associated-with-the-universal-music-group-umg-partnership
- S7 Music Business Worldwide, "Universal Music settles Udio lawsuit, strikes deal for licensed AI music platform" (29 Oct 2025 per search excerpts from it, Hollywood Reporter and Rolling Stone; not opened), plus search excerpts from Undetectr's "Udio Download" and "Udio Review 2026" pages (secondary): https://www.musicbusinessworldwide.com/universal-music-settles-udio-lawsuit-strikes-deal-for-licensed-ai-music-platform/
- S8 ElevenLabs, Eleven Music documentation: https://elevenlabs.io/docs/capabilities/music
- S9 ElevenLabs Music Terms (last updated 26 May 2026): https://elevenlabs.io/music-terms
- S10 ElevenLabs, Eleven Music Model-Specific Terms (26 May 2026): https://elevenlabs.io/eleven-music-model-specific-terms
- S11 ElevenLabs, Sound Effects documentation: https://elevenlabs.io/docs/capabilities/sound-effects
- S12 ElevenLabs API, Stem Separation: https://elevenlabs.io/docs/api-reference/music/separate-stems
- S13 Google, "Generate music with Lyria 3.5": https://ai.google.dev/gemini-api/docs/music-generation
- S14 Google, "Real-time music generation using Lyria RealTime": https://ai.google.dev/gemini-api/docs/realtime-music-generation
- S15 Google, Gemini API pricing: https://ai.google.dev/gemini-api/docs/pricing
- S16 Google, Gemini API Additional Terms (last modified 28 Apr 2026): https://ai.google.dev/gemini-api/terms
- S17 Stability AI, Stable Audio 3.0: https://stability.ai/stable-audio
- S18 Stability AI Community License: https://stability.ai/license
- S19 TechCrunch, "Stability AI releases a new audio model that can create 6-minute songs" (20 May 2026; secondary): https://techcrunch.com/2026/05/20/stability-ai-release-a-new-audio-model-that-can-create-six-minute-songs/
- S20 Adobe blog, "Adobe Firefly expands its creative AI studio" (20 Aug 2026): https://blog.adobe.com/en/publish/2026/08/20/adobe-firefly-expands-its-creative-ai-studio-generate-music-speech-and-sound-effects-in-one-place
- S21 ACE-Step 1.5, GitHub: https://github.com/ace-step/ACE-Step-1.5
- S22 MMAudio, GitHub (licences, limitations): https://github.com/hkchengrex/MMAudio
- S23 fal, MMAudio V2: https://fal.ai/models/fal-ai/mmaudio-v2
- S24 Tencent HunyuanVideo-Foley licence: https://huggingface.co/tencent/HunyuanVideo-Foley/blob/main/LICENSE
- S25 fal, Sonilo v1.1 Video to Sound Effects: https://fal.ai/models/sonilo/v1.1/video-to-sound-effects
- S26 fal, Mirelo SFX v1: https://fal.ai/models/mirelo-ai/sfx-v1/video-to-audio
- S27 Freesound FAQ (licences, attribution): https://freesound.org/help/faq/
- S28 Sonniss, GameAudioGDC bundles: https://sonniss.com/gameaudiogdc
- S29 BBC Sound Effects RemArc licence, secondary summaries (primary https://sound-effects.bbcrewind.co.uk unreachable, again on the fact-check pass): https://www.avosound.com/en-us/licensing/remarc-license ; https://blog.prosoundeffects.com/how-to-license-bbc-sound-effects-to-use-in-your-commercial-productions
- S30 YouTube Help, Audio Library: https://support.google.com/youtube/answer/3376882
- S31 Pixabay Content License summary: https://pixabay.com/service/license-summary/
- S32 Demucs, GitHub: https://github.com/facebookresearch/demucs
- S33 Audacity Manual, Index of Effects, Generators and Analyzers: https://manual.audacityteam.org/man/index_of_effects_generators_and_analyzers.html
- S34 US Copyright Office, Copyright and AI, Part 2 (29 Jan 2025): https://www.copyright.gov/ai/ ; NewsNet 1060: https://www.copyright.gov/newsnet/2025/1060.html
- S35 Wikipedia, "Temp track": https://en.wikipedia.org/wiki/Temp_track
- Library: A4 (§7, §10, §11 WE1–WE4, §14, §15), B4 (§3.4, §9.1, rule 23, M10, §14.2), C3 (§7D, §7E, rule 10), C1 (§3A, §7, rule 22), C5 (P12 / §10.1 IDs, §6.9 checkpoints), D3 (§8.1 path chains), D4 (§3, §5 credit line, principle 8), D8 (R7, R37), D13, D17; the build blueprint `design/blueprint.md` (§5.3 IDs, §5.5 record fields: SOUNDPLAN, MUSIC, RIGHTS, MOTIF, SPEECH.path); the library critic's resolutions on music policy and scale names. Test sources: *The Catch* (workshop revision, 25 Sep 2026); *The Long Places* (revised final), Chapters II, III, IV, V, VII, VIII.
