# D3 — Voice casting and dialogue audio for AI filmmaking (as of 27 September 2026)

> **What this file is for**
> 1. Turning every spoken line into a finished audio file: which tool, which voice, which delivery, which take, and heard through what.
> 2. Adding a voice section to each character's bible entry (B5 §7.1) and one **voice asset** record that replaces five older field names.
> 3. Consent, verification and labelling rules for synthetic and cloned voices, dated 27 Sept 2026.
> 4. When to use the video model's own audio, when to lip-sync afterwards, and when to keep the speaker off screen.
> 5. Runs after A1–A3 (lines, pauses, playable actions) and B5 (characters); feeds C1/C3 (audio into video models) and A4 (edit and mix).

---

## 0. Labels, staleness, terms

**Evidence labels.** [V] verified on a primary source; [U] unverified (secondary source or blocked page); [J] this file's judgment. Every tool, price and policy fact carries a key [Sn] resolving to a URL in **Sources**, all checked 2026-09-27.

**Staleness rule.** Voice tools change monthly. More than 30 days after 2026-09-27, have the LLM re-open the Sources pages before paying.

**Terms (one word per concept).**
- **TTS** (text to speech): software that reads typed text aloud in a synthetic voice.
- **Voice design**: making a new synthetic voice from a written description, with no real person's recording.
- **Clone**: a synthetic voice copied from recordings of a real person; *instant* clones use seconds to minutes of audio, *professional* clones train on 30 minutes or more.
- **Speech-to-speech (STS)**: you perform the line and the tool swaps your voice for the character's, keeping your timing and stress (ElevenLabs "Voice Changer").
- **Audio tag**: a bracketed word in the text that directs delivery: `[whispers]` (ElevenLabs), `<breath>` (Gemini).
- **Voice asset**: the one record per speaking character (§10). It replaces C5 `voice_key`, the voice half of C3 `sound_key`, C3 `bound_voice`, C1 `voice_sample` and A3 `voice`.
- **Delivery state**: a named way one voice sounds for a stretch of story (Saye's "answers voice").
- **Take**: one generated audio file of one line. **Alternate**: a deliberately different reading of the same line, with its own takes.
- **Path**: how a line reaches the audience (direct, earpiece, radio, helmet...). It replaces A3 `voice_source`, C5 `channel`, A4 `perspective` and C3 "heard through". A **relay** is a device in the path.
- **Band-pass**: a filter that keeps only a middle band of frequencies; it makes a voice sound "through a device".
- **Native audio**: sound the video model makes in the same run. **Audio-reference model**: a video model that takes your line audio as input (C1 R1).
- **Lip sync (post)**: re-drawing the mouth of a finished clip to match an audio file.
- **Room tone**: a place's quiet background sound. **LUFS**: the unit of perceived loudness (A4). **Dialogue stem**: the mix track holding only dialogue.
- **Stability** (ElevenLabs v3): one setting with three positions. *Creative* = most emotional, may add or garble words; *Natural* = closest to the designed voice; *Robust* = steadiest, follows tags least.
- **High-pass / low-pass**: filters that remove sound below (high-pass) or above (low-pass) a frequency. **Saturation**: mild, deliberate distortion that makes a small speaker sound strained. **Compression**: evens out loud and quiet parts. **Reverb**: the echo of a room. **Crossfade**: one sound fading out while another fades in.
- **IPA**: the International Phonetic Alphabet, spelling a word by its sounds so the tool says it right.
- **API**: a way for a program (or the LLM) to use a tool without its web page. **MCP**: a connector that lets an AI chat app (Claude, for example) call a tool directly. **OAuth**: signing in through the vendor's own page, so no secret key is pasted anywhere.
- **Watermark** (audio): an inaudible mark some tools put in every file so it can later be identified as AI-made.
- **VRAM**: the memory on a computer's graphics card; open models list how much they need.
- **Forced alignment**: software that finds when each word starts and ends in a recording.

---

## 1. Core principles

1. **Voice first.** Lock every recurring voice before generating any picture with a speaking mouth (the critic's resolution of the C1/C3/A4 conflict; native in-clip voices only for drafts and one-line parts).
2. **Design, don't copy.** Characters get designed voices. Cloning is only for the user's own voice or a consenting, verified person.
3. **Performance in TTS, path in post.** Generate every line clean; earpiece, radio or helmet is added afterwards, because one take is often heard from two places.
4. **Words are sacred, text is not.** Spoken words match the script exactly (C3 L31); tags, punctuation and phonetic spellings may change in what is sent to the tool.
5. **The listener carries the line when possible** (A1 R1, A2 R27): the cheapest and safest sync is none.
6. **Three takes and a pick.** Reject wrong words by transcript; choose by ear.
7. **Timing lives in the edit.** "(beat)" and Eli's thinking pause are silences in the timeline, not in a file.
8. **Seat the voice.** TTS is dead-dry; every scene gets continuous room tone and the location's small reverb.

---

## 2. Landscape (checked 2026-09-27)

### 2A. Speech, voice design, cloning, speech-to-speech

| Tool | What it gives this pipeline | Price | Languages | Access | Commercial terms, consent gate | Tag |
|---|---|---|---|---|---|---|
| **ElevenLabs Eleven v3** | Released (no alpha label). Tags `[whispers]`, `[sighs]`, `[exhales]`, `[laughs]`, `[strong X accent]`, `[sings]`. Stability *Creative* ("prone to hallucinations"), *Natural*, *Robust*. Speed 0.7–1.2. No SSML break tags: pauses by ellipses and dashes. IPA in slashes ("80-90% pronunciation consistency"). 5,000 characters per request. Very short inputs are less consistent [U: from the earlier v3 alpha prompting guide, which advised "prompts greater than 250 characters"; not on the current page]. **Text to Dialogue** (v3 only): several voices in one call, with a with-timestamps endpoint. | Free $0/10k credits; Starter $6/30k; Creator $22/121k ($11 first month); Pro $99/600k; 1 credit ≈ 1 character on v3, so ~1,000 credits ≈ 1 min of speech [J] | 70+ | App; API; **hosted MCP** `https://api.elevenlabs.io/v1/mcp` (OAuth); old local MCP archived 20 Aug 2026 | Free: not commercial. Starter+: commercial, instant clones. Creator+: professional clones, Dubbing Studio | [V] S1 S2 S3 S8 S9 |
| **ElevenLabs Voice Design** | Three previews from a text prompt; *guidance scale*, *loudness*. | Per preview text | as v3 | App, API, MCP | No stated real-person rule, so rule 18 applies | [V] S6 |
| **ElevenLabs cloning** | Instant: 1–2 min clean audio (more than 3 min "may harm clone quality"); copies "the speed of the person talking, the inflections, the accent, tonality, breathing pattern". Professional: ≥30 min (2–3 h recommended), 3–6 h training. | In plan | — | App, API | Instant: "confirm that you have the right and consent to clone the voice". Professional: "Even with their consent, you cannot clone someone else's voice"; voice-captcha verification, which "cannot guarantee that the provided recording truly belongs to the requester, only that the requester was present" | [V] S4 S5 S10 |
| **ElevenLabs Voice Changer** (STS) | Multilingual STS v2; `remove_background_noise`; `seed` for repeatable output. | Credits [U] | 29 | App, API, MCP | Your performance in, a designed voice out | [V] S2 S7 |
| **Gemini 3.8 Flash TTS / Flash-Lite TTS** | 30 voices; **2 speakers per request**; tags `<breath>`, `<sigh>`, `<short pause>`, `<long pause>`, `<laugh>`, `<gasp>`; **Voice Design** and **Voice Replication** (persistent `voice_id`, kept 1 year); 24 kHz default. Long "Director's Notes" "are the most common cause of voice drift": use a short `style` per turn. | Flash $0.50/1M text in, $9/1M audio out (25 audio tokens per second, so ≈$0.00225 per 10 s) to 31 Dec 2026, then double; Lite $6/1M out; free tier | >130 (Lite >100) | AI Studio, API | Replication: 10–30 s plus the same adult saying "I am the owner of this voice and I consent to Google using this voice to create a synthetic voice model", speaker-matched. Reportedly blocked in the UK, EEA, India, Texas and Illinois [U S16] | [V] S13 S14 S15; [U] S16 |
| **OpenAI gpt-4o-mini-tts** | 13 voices (marin, cedar best); `instructions` for accent, emotion, speed, whispering. | $0.60/1M in, $12/1M audio out (≈$0.015/min [U]) | 50+ | API | Custom voices by approval with a consent recording; tell listeners "the TTS voice they are hearing is AI-generated" | [V] S11 S12 |
| **Azure Speech** | HD voices; *personal voice* from 5–90 s plus a recorded consent statement. | HD $22/1M characters | 90+ | API | Limited Access: approved use cases only | [V] S17 S18 S19 |
| **Cartesia Sonic-3.6** | Emotion read from the text; `[laughter]` tag; clone "with 10 seconds of audio"; speed and volume controls [U: API docs not opened]. | Free 20k credits; Pro $5/100k; Startup $49/1.25M | 44 | API | Commercial from Pro; instant clones from Pro, professional clones from Startup | [V] S20 S21 |
| **Hume Octave 2** | Voice design from a description; acting `description` per line; `speed` 0.5–2.0; `trailing_silence` (seconds of silence after a line). | Free 10k characters; Starter $3/30k; Creator $7/140k; Pro $70/1M | [U] | API, app | **Commercial from Creator ($7)**; Free and Starter are not commercial; cloning on all paid plans | [V] S22 S23 |
| **Chatterbox** (open, Resemble AI) | MIT. Turbo (English, `[laugh]` `[cough]` `[chuckle]` tags), Nano (English, runs on CPU), Multilingual V3 (23+ languages). Clone from a ~10 s reference. Drama: `exaggeration` 0.7+, `cfg_weight` ~0.3. Perth watermark on every file. | Free (own GPU; Nano on CPU) | 23+ | Local, Replicate | Keep the watermark | [V] S24 |
| **Dia** (open, Nari Labs) | 1.6B parameters; `[S1]`/`[S2]` two-speaker dialogue; non-verbal cues written in round brackets, e.g. `(laughs)`, `(coughs)`, `(sighs)`, `(inhales)`; clone from a 5–10 s sample with its transcript. A larger Dia2 now exists. | Free | English only | Local | Apache 2.0 | [V] S25 |
| **IndexTTS2** (open weights) | Emotion separate from identity ("timbre-emotion disentanglement"); duration control "not yet enabled in this release". | Free | Chinese, English | Local | Custom bilibili licence: read before commercial use | [V] S26 |

### 2B. Lip sync after generation

| Tool | Price | Strengths and limits | Tag |
|---|---|---|---|
| **sync. sync-3** | $0.107–0.133/s | 4K; "natively supports extreme face angles including profiles, over-the-shoulder shots"; built-in obstruction detection ("hands, microphones, scarves"); can "open silent lips to match audio, though results are generic rather than speaker-style matched" | [V] S28 |
| **sync. lipsync-2-pro** | $0.067–0.083/s | 512×512; "Enhanced beard resolution", "Improved teeth generation"; needs natural speaking motion; "Extreme profile view faces can lead to sub-par results"; optional occlusion detection; 1.5–2× slower than lipsync-2 | [V] S28 |
| **sync. lipsync-2** | $0.04–0.05/s | As above without the detail pass. Plans $5–249/month plus per second. Several faces: `active_speaker_detection` (all models) syncs only the speaking face; if it picks the wrong one, mask or crop | [V] S28 S29 |
| **Kling Lip Sync** | 1 credit per second | Human characters (real, 3D or 2D), "provided the character's face is complete"; the guide names only Kling 1.0/1.5 videos (Omni voice binding: C1 R1) | [V] S30 |
| **Hedra Character-3** | $0.025/s (540p), $0.05/s (720p), $0.0625/s (1080p) | Start picture plus audio to talking video, up to 10 min; wants "clean speech ... zero background noise or heavy reverb". Good for screen inserts | [V] S32 |
| **Runway Act-Two** | 5 credits/s ≈ $0.05/s (verified in D15 §5.1 from Runway's API docs) | Performance transfer from your own 3–30 s driving video, lips included; needs "A visually recognizable face" (C1 R12; D15 §5.1). Speak the line while recording and the same file drives face and, through STS, voice | [V via D15]; help page S31 blocked (403) |
| **LatentSync 1.6** (open, ByteDance) | Free | 512×512; 18 GB VRAM (1.5 needs 8 GB); Apache 2.0 | [V] S33 |
| **MuseTalk** (open) | Free | 256×256 face region; "30fps+ on an NVIDIA Tesla V100"; MIT | [V] S34 |
| **InfiniteTalk** (open) | Free | Re-performs lips, head, body and expression from audio; 480p/720p; single-image input good "for up to 1 minute"; Apache 2.0 | [V] S35 |

Video models that take your audio, and their sample lengths, are in C1 R1 and C1 P2.

---

## 3. Decision rules

**Choosing tools**
1. **If** a character speaks in more than one scene, **then** give them one voice asset (provider, voice ID, model version, frozen settings) before any video with a visible mouth, **because** fresh voices per clip do not match across a film (C1 R1).
2. **If** opening the first voice account, **then** use ElevenLabs: Starter ($6, 30k credits) is the cheapest plan with commercial rights, Creator ($22, 121k credits; $11 the first month) gives four times the room for Voice Design previews and redos; **if** cost matters most or you already pay for Gemini, **then** Gemini 3.8 Flash TTS; **because** these two cover design, tagged delivery, two-speaker exchanges and LLM access, and The Catch needs about 26,000 characters (§12) [J from S1–S15].
3. **If** a line's acting is hard to put in words (mouth full, a whisper, a breath for a word), **then** perform it on a phone and convert it with STS, **because** STS keeps your timing, breath and stress [J; S7].
4. **If** the work must stay offline or free, **then** use Chatterbox or Dia, and read IndexTTS2's licence before commercial use, **because** it is not a standard open licence [V S24 S26].
5. **If** the vendor updates the model mid-project, **then** regenerate a whole scene's lines together, **because** one voice ID can sound different on a new model [J].

**Casting**
6. **If** the country and accent are undecided (`WORLD.accents` is `undecided`; critic conflict "Locale, accent and driving side"; D17 R1), **then** cast with a placeholder accent, keep voice assets at `status: draft`, and make no audio-reference or lip-synced finals, **because** an accent change redoes every sync shot [J].
7. **If** two voices share three or more of the six lineup columns (§4.3), **then** change pitch band or pace first, **because** same-sex, same-age voices blur on small speakers [J].
8. **If** A2's `speech_profile` says `contractions: no` (Saye), **then** check transcripts for slipped-in contractions and set her pace near 2.0 words/s (critic resolution), **because** her one contraction ("They're here.", SC24) is a story event (A2).
9. **If** a character has a written pausing habit ("Eli thinks before he answers. He always does.", l.1142), **then** place the pause (about 1 s, B5 §10.3) in the edit, **because** a timeline pause can still be tuned.

**Delivery**
10. **If** a line has a delivery parenthetical, **then** translate it with §5.1 and make two alternates of three takes, **because** parentheticals are the writer's only direct acting notes.
11. **If** a parenthetical names a place or device ("in her ear", "over the radio", "into her helmet", "from the back"), **then** treat it as a path (§8), **because** it describes hearing, not acting [J].
12. **If** a line contains "(beat)", **then** split it into two files about 1 s apart (A2's "(beat)" rule), **because** a pause inside one file cannot be moved.
13. **If** a line has three words or fewer, **then** generate it inside its exchange and cut it out, **because** very short inputs come out inconsistent [U: ElevenLabs' earlier v3 alpha guide said "Very short prompts are more likely to cause inconsistent outputs"; the current page no longer says so; J].
14. **If** you change the text sent to the tool, **then** keep the spoken words identical and store `line_text` and `tts_text` separately, **because** C3 L31 fails lines that differ from the screenplay.
15. **If** choosing between takes, **then** transcribe each one (ElevenLabs Scribe or any speech-to-text), reject wrong words or tags spoken aloud, then pick by ear, **because** Creative stability is "prone to hallucinations" and v3 "will still speak out" written delivery guides [V S3].

**Consent and law**
16. **If** anyone proposes cloning a real person, **then** require a signed consent record (§6.2) plus the vendor's own verification, and never clone an actor from existing recordings, a celebrity, a deceased person or a minor (a project policy, stricter than the law, which lets parents and estates authorize), **because** Tennessee's ELVIS Act covers "the actual voice or a simulation of the voice of the individual", the NO FAKES Act of 2026 has passed committee, and vendors require the speaker's own verification [V S36 S37 S5 S15].
17. **If** the voice to clone is the user's own, **then** it is allowed, with the vendor's verification as evidence, **because** the owner consents [V S5 S43].
18. **If** you write a voice design prompt, **then** never name a real person or write "sounds like [name]", **because** a recognizable imitation is that person's voice in law (ELVIS) [V S36].
19. **If** the film will be shown in the EU from 2 Aug 2026, on YouTube, or uses OpenAI voices, **then** add an AI-voice credit line (D4's credit template), keep watermarks, and fill `ai_voice_disclosure`, **because** OpenAI's policy requires telling listeners the voice "is AI-generated", YouTube requires a label on realistic synthetic content, and Article 50 requires deepfake disclosure (in a way "that does not hamper" an evidently fictional work) [V S11 S43 S38]. A designed voice resembling no one is probably not a "deepfake" at all [J], so for the EU the credit is cheap insurance, not a proven duty.

**Lip sync**
20. **If** the listener can carry the line (A1 R1, A2 R27), **then** play it off screen, **because** it costs nothing and cannot drift.
21. **If** the mouth must be seen, **then** use an audio-reference video model first (C1 R1), post lip sync second (sync-3 for profiles and obstructions; lipsync-2-pro for frontal beard and teeth), a cutaway third, **because** each step down costs less and risks less.
22. **If** the mouth is behind a visor, reflective glass, a hand or a prop, **then** avoid on-screen sync (stage from behind, in profile, over the visor display, or composite a clean face under the visor, D6), **because** obstructions and extreme angles are the named weak points [V S28; J for visors].
23. **If** post lip sync fails twice on one shot, **then** cut to the listener or an insert, **because** C1 rule 24 says switch method rather than spend more.

**Paths and edit**
24. **If** a voice reaches the audience through a device, **then** process the clean take in post with one saved chain per path (§8), **because** TTS asked to "sound like a radio" varies between takes [J].
25. **If** a line crosses a cut from the speaker's side to the listener's side, **then** process per shot and crossfade two versions of the take at the cut, **because** the path depends on where we listen, not who speaks [J].
26. **If** a take's speech length misses A2's planned duration (words ÷ 2.5 + 0.5 s; Saye 2.0 words/s) by more than 20%, **then** pick another take or change speed, and never time-stretch dialogue beyond about 8%, **because** stretching smears consonants [J].
27. **If** the dialogue is TTS, **then** run room tone under the whole scene and add the location's short reverb, **because** dry voices sound pasted on [J].

---

## 4. Voice casting as character design

### 4.1 Voice section for the B5 bible entry

Add after STATUS in B5 §7.1:

```
VOICE:
  VOICE BRIEF:      age read | pitch band | timbre (≤3 words) | accent (world rule) | pace (words/s) | status in the voice
  SPEECH PROFILE:   from A2 (sentence length, contractions, vocabulary field)
  DESIGN PROMPT:    30–50 words, frozen word order, no real names, {accent} slot
  DELIVERY STATES:  D01 default ... with the scene where each starts
  LINEUP ROW:       six columns (§4.3)
  SOURCE:           designed | prebuilt | own-voice clone | consented clone (+ consent record ID)
```

**Status in the voice** (B5 §5.3): high status sounds level, with falling ends and no fillers; low status adds rising ends and "hesitation sounds before speaking". B5's status flips are also voice cues.

### 4.2 The Catch: five speaking voices (proposals [J], accent pending)

221 cues, five speakers (A3); this file's recount: 1,579 spoken words, 7,666 characters. Guard, nurse and technician never speak. `{accent}` stays a placeholder until the world rule is set (C3's "British" is provisional).

| Voice | Brief | Delivery states | Design prompt (frozen) |
|---|---|---|---|
| **VOICE-IONA** | late 30s · low-mid · dry, husky · 2.6 w/s · high in work | D01 *work*; D02 *cracked* (SC10, SC13); D03 *helmet* (SC23–SC28); D04 *level* (SC29–SC30) | "A woman in her late thirties with a low, dry, slightly husky voice; {accent}; clipped, level delivery with falling sentence ends and no upward inflection; brisk but never rushed; close, clean studio recording." |
| **VOICE-JUDE** | mid 40s · low · warm, gravelly · 2.4 w/s · lowers himself to lift others | D01 *easy*; D02 *wounded* (from SC06 "(quite softly) Oh."); D03 *whisper* (SC15) | "A man in his mid-forties with a warm, low, slightly gravelly voice; {accent}; relaxed and unhurried, a smile audible under the words, easy breathing; close, clean studio recording." |
| **VOICE-ELI** | early 30s · mid · thin, clear · Iona's vowels · 2.2 w/s plus ~1 s silent lead-in · flat, informed | D01 *counting*; D02 *open* (SC23 "Are we going to be all right?", SC29) | "A thin-voiced man in his early thirties, mid pitch, clear, dry and quiet; {accent}; measured and flat, few rises, precise consonants, speaks as if reading figures aloud; close, clean studio recording." |
| **VOICE-SAYE** | late 50s · mid · crisp · formal · 2.0 w/s · high by stillness, no contractions | D01 *answers voice*; D02 *lost answers voice* (SC24); D03 *softened* (SC28 "Yes, Nell.") | "A woman in her late fifties with a clear mid-pitched voice and crisp consonants; {accent}, formal; slow, even, complete sentences with firm falling ends; very still, no filler sounds; close, clean studio recording." |
| **VOICE-NELL** | reads older than 60 · mid-high · light, papery · 1.9 w/s · quiet high | D01 only | "An elderly woman who sounds older than sixty, with a light, thin, slightly papery voice and a faint rasp; {accent}; slow and careful, each phrase said once, calm and direct; close, clean studio recording." |

Why: the siblings share accent and vowels, not pitch or pace (B5's shared brows, different beards). Losing "the voice she uses for answers" (l.1383) is Saye's second state, not an effect. Eli's lead-in is silent: hesitation sounds would lower his status.

### 4.3 Lineup check

| | Age band | Pitch band | Timbre | Pace | Accent | Status in voice |
|---|---|---|---|---|---|---|
| IONA | 35–40 | low-mid | dry, husky | 2.6 | A | high, clipped |
| JUDE | 40–50 | low | warm, gravelly | 2.4 | A | self-lowering |
| ELI | 30–35 | mid | thin, clear | 2.2 | A | flat, informed |
| SAYE | 55–60 | mid | crisp, clean | 2.0 | A | high, still |
| NELL | 60+ | mid-high | light, papery | 1.9 | A or B (user decides) | quiet high |

No pair may share three or more columns (rule 7). Risky pairs: Iona–Saye, Saye–Nell (also B5's closest visual pair), Eli–Jude.

**Recipe: lineup test** (15 min, under $1).
1. Ask the LLM for one neutral 20-word sentence and generate it in all five voices.
2. Have it rename the files 1–5 in random order and keep the key.
3. Next day, name each voice from a phone speaker; on any confusion, change one voice's pitch band or pace and retest.
4. Repeat through each relay you will use, because band-limiting erases pitch and timbre differences first [J].

**Recipe: design one voice without code** (20 min per voice; credits only). [J; steps from S6]
1. Ask the LLM to fill the `{accent}` slot of the character's design prompt from `WORLD.accents` (placeholder while undecided) and to write one 20–30-word test line in the character's own speech pattern, taken from the script.
2. In ElevenLabs, open Voices, then Voice Design. Paste the design prompt; paste the test line as the preview text. Generate: you get three previews.
3. Listen on a phone speaker. If none fits, change one phrase of the prompt (not five) and generate again; stop after three rounds and take the closest.
4. Save the voice under the asset name (`VOICE-IONA`). Copy its voice ID into the voice asset with the model (`eleven_v3`), stability and speed you will use.
5. Generate the lineup sentence (lineup test above) before designing the next voice, so each new voice is chosen against the ones already cast.
6. Once all five pass the lineup test, export 10–30 s of each delivery state as `reference_samples` (for audio-reference video models) and set `status: locked` only when the accent is decided (rule 6).

---

## 5. Delivery direction

### 5.1 The Catch's 18 parentheticals as controls

| Line | Speaker | Parenthetical | Kind | ElevenLabs v3 / Gemini control | Post and picture |
|---|---|---|---|---|---|
| 94 | JUDE (V.O.) | (in her ear) | path | clean take | earpiece chain (§8) |
| 98 | IONA | (through the torch) | delivery | STS: say "No." with a pencil between the teeth; fallback `[strained] No.` | mouth covered: no lip sync |
| 219 | JUDE | (quite softly) | delivery | `[softly] Oh.`, Natural; Gemini style "quiet, surprised" | — |
| 352 | JUDE | (from the back) | path | clean take | back seat: lower, more cabin reflection |
| 462 | IONA | (not steady) | delivery | example 11.1 | on screen |
| 620, 1148 | SAYE, ELI | (taps the right dish), (looks towards Nell) | action | none | picture |
| 776, 793, 815, 1063, 1146, 1256, 1278 | ELI ×3, IONA ×2, SAYE ×2 | (beat) | timing | split the file (rule 12) | ~1 s gap |
| 786 | SAYE | (quietly) | delivery | `[quietly]`; Gemini style "quiet, far away" | — |
| 857 | JUDE | (a whisper) | delivery | `[whispers] Iona?`; better STS of a real whisper | via the tablet speaker (`device_speaker`) |
| 1214 | ELI (V.O.) | (over the radio) | path | clean take | radio chain |
| 1610 | JUDE | (into her helmet) | path | `[quietly]`, Robust | helmet-shell chain |

Seven are timing, six are paths or actions, only five are delivery. [J] Whispers and obstructed mouths are TTS's weakest areas; STS is the dependable route.

### 5.2 Playable actions into delivery words

A3's playable action becomes the delivery string; emotion words belong here (C3 rule 14 keeps tone words "for the voice only").

| Playable action (A3) | Delivery string | Starting settings [J] |
|---|---|---|
| to warn | low, firm, urgent, falling ends | Natural, speed 1.0 |
| to press | level, quiet, unhurried, no rise | Robust, speed 0.95 |
| to soothe | soft, warm, slower | Natural, speed 0.9 |
| to dismiss | flat, quick, clipped | Robust, speed 1.1 |
| to plead | breathy, rising, uneven | Creative, speed 0.95 |

Syntax: ElevenLabs, one or two tags before the words; Gemini, a short `style` per turn; OpenAI, `instructions`; Hume, `description`; Chatterbox, raise `exaggeration`. Test undocumented tags per voice [J].

### 5.3 Take policy

- Every line: **3 takes**; pick one; keep the others in the take log.
- Delivery parentheticals, turning lines (A1) and delivery-state changes: **2 alternates × 3 takes**.
- Lines of ≤3 words: generate the exchange 3 times and cut per line (rule 13).
- Record a `verdict` and one-line reason per take (§10.3).

### 5.4 Recipe: direct one scene's dialogue (30–60 min, about $0.10–1)

1. Paste the scene, its A1/A2 plan (turning line, pauses), A3 playable actions and the voice assets. Say: "Make one D3 line record per cue. Copy `line_text` exactly. Put at most two audio tags in `tts_text`, split at (beat), and mark path parentheticals as paths."
2. Check words, speakers and paths yourself.
3. Have the LLM (through the ElevenLabs MCP, or a script it writes) generate 3 takes per line, named as in §9.
4. Have it transcribe every take and delete mismatches.
5. Listen in scene order, pick, and give your reasons.
6. Have it log picks and durations and flag takes outside ±20% of `planned_duration_s`.

---

## 6. Consent and law

### 6.1 What applies (checked 2026-09-27; not legal advice)

| Rule | What it says for this pipeline | Tag |
|---|---|---|
| **Tennessee ELVIS Act** (from 1 July 2024) | "Voice" is "a sound in a medium that is readily identifiable and attributable to a particular individual, regardless of whether the sound contains the actual voice or a simulation of the voice of the individual"; distributing a tool whose "primary purpose or function" is producing someone's voice or likeness without authorization is also actionable. | [V] S36 |
| **US NO FAKES Act of 2026** (S. 4591) | Federal, licensable right over digital replicas of voice and likeness; liability for makers and knowing platforms; DMCA-style notice-and-takedown; exceptions for news, parody, criticism; pre-2 Jan 2025 state laws survive. Senate Judiciary Committee advanced it by unanimous voice vote on 18 June 2026. As of late September 2026 it is reported to be on the Senate calendar, passed by neither chamber, not law. | [V] S37 (committee); [U] S47 (later status; GovTrack and congress.gov blocked) |
| **California AB 2602** (from 1 Jan 2025) | Digital-replica clauses in performer contracts need a specific description of uses and representation; matters if you hire a voice actor. | [V] S39 |
| **New York synthetic performer ads** (from 9 June 2026) | Advertisers must "conspicuously disclose" a synthetic performer in an ad. Exempt: ads for films, TV, streaming, video games where the use is consistent with the work, and audio-only ads. Matters only for a trailer or ad that shows a generated person differently from the film. | [V] S40 |
| **EU AI Act Article 50** (from 2 Aug 2026) | Deployers disclose deepfakes ("AI-generated or manipulated image, audio or video content that resembles existing persons...") "upon first exposure at the latest"; for "evidently artistic, creative, satirical, fictional or analogous works", only in a manner that does not hamper the work. Providers mark synthetic audio machine-readably (Art. 50(2)); tools already on the market before 2 Aug 2026 have until 2 Dec 2026. | [V] S38 |
| **China labelling measures** (from 1 Sept 2025) | Explicit and implicit labels on AI audio on Chinese platforms. | [V] S41 |
| **Denmark** | Proposed (June 2025) copyright-style right over one's own voice and likeness, lasting 50 years after death; reported start dates differ (31 March 2026 or Q3 2026); adoption not confirmed here. | [U] S42 |
| **YouTube** | Disclose realistic synthetic content; "Cloning one's own voice to create voice overs or dubs" needs no disclosure. | [V] S43 |

[J] A designed voice for a fictional character imitates no one, but it is still AI-generated content. Name the voice tool in the end credits by default, using D4's credit-line template ("voices designed with [tool]"; D4 Recipe 6): it meets the fictional-work standard and costs nothing. If a trailer or ad will run in New York and shows a generated person differently from the film, add the synthetic-performer notice (S40).

### 6.2 Consent record (only when a real person's voice is cloned)

Kept **offline** by the user; the breakdown holds only `consent_record_id`. Never put the person's name, contact details or recordings into prompts.

Fields: record ID; full name; date; adult (yes/no); scope (project, characters, media, territories, duration); whether new lines beyond the script are allowed; payment; how to withdraw and what happens to finished work; vendor verification result; where samples are kept; deletion date; signature.

### 6.3 Recipe: clone a consenting person (only if designed voices will not do)

1. Have the LLM turn the §6.2 fields into a one-page plain-language agreement; the person signs it.
2. Record 1–2 minutes of clean speech in the delivery you want; the clone copies it [V S4].
3. The person completes the vendor's verification themselves.
4. Store recordings and record offline; only the record ID goes in the voice asset. Stay inside the signed scope.

**Never:** clone from film, TV, podcasts or videos; prompt "in the voice of" anyone real; use a minor's voice; remove watermarks.

---

## 7. Lip sync after the fact

### 7.1 Where sync fails, and The Catch cases

| Condition | Tool behaviour | The Catch | Decision |
|---|---|---|---|
| Profile | lipsync-2/2-pro weak; sync-3 supports | SC10 profile two-shot "like a woman and her reflection" | sync-3, or no line in that shot |
| Beard | lipsync-2-pro "Enhanced beard resolution" | Eli's untrimmed beard | keep Eli off screen where A1 allows |
| Prop at the mouth | occlusion detection helps; risky [J] | SC02 torch in Iona's teeth | no sync: lay the audio |
| Visor with reflections | untested; treat as obstruction [J] | "She checks the load on her visor." (l.1296); SC28 "Leave it on." | off-mouth staging, or composite (D6) |
| Two faces | wrong-face risk; `active_speaker_detection` helps | SC29 through glass | turn on active-speaker detection; if the wrong face moves, mask the silent face |
| Still face | lipsync-2/2-pro need motion; sync-3 can open lips, "generic rather than speaker-style matched" | listener-style clips | sync-3 for short words; audio-reference regeneration for longer lines |

### 7.2 Recipe: post lip sync one shot ($0.10–1)

1. Lock the picked take, trimmed to 0.2 s before the first sound.
2. Generate the picture with natural speaking motion ("speaks quietly") for lipsync-2/2-pro; a neutral face or still is fine for sync-3.
3. Upload clip and audio to sync. (app or API).
4. Check at half speed: lips close on every "m", "b", "p" ("mint", "body"); no teeth flicker; no beard smear.
5. Two failures: cut away (rule 23). After any audio slip in the edit, re-check sync (C5 R31).

---

## 8. Relayed voices

Performance in TTS, path in post (rule 24). Only native-audio *drafts* name the path in the prompt (C3 R21: "Jude's voice, heard only in her earpiece, crackly; he is not visible").

### 8.1 Path chains (starting points; tune by ear) [J; telephone band 300–3,400 Hz from ITU-T G.712, S45; filters in FFmpeg, S46]

| Path | Chain | Where it sits |
|---|---|---|
| `direct` | none | scene room tone and reverb |
| `off_screen` | slightly more reverb, 1–3 dB lower | same space |
| `earpiece` | high-pass 400 Hz, low-pass 3,400 Hz, light saturation, gentle compression, no reverb | mono, centre, 3–6 dB under direct speech |
| `radio` | band-pass 300–3,400 Hz, more saturation or light bit-crush, peak near 1.8 kHz, key clicks | inside the listener's space |
| `intercom` | band-pass 250–5,000 Hz, light compression, speaker-box resonance, listener's room reverb | from the wall speaker |
| `device_speaker` (tablet, wrist) | high-pass 500 Hz, low-pass 5,000 Hz, slight distortion | on the device, in its space |
| `recording` | device chain plus the recorded room's tone | as device |
| `helmet_internal` (wearer's own voice) | 5–10 ms reflections, +3 dB at 200–400 Hz, breath kept, outside muffled | close, dry |
| `helmet_external` (heard outside the visor) | low-pass 1.5–2 kHz, 6–10 dB down | muffled |
| `through_glass` (no intercom) | low-pass 1–1.5 kHz, 12 dB down | non-verbal sound only |
| `tape` | 60–10,000 Hz, slight wow and hiss, then the room | cassette |

**Glass rule [J].** The script never says how voices cross the quarantine glass; C3's SC11 intercom is a design choice. Decide once, as a world rule, for every glass conversation (SC11–SC13, SC17, SC29): `intercom` for speech, `through_glass` only for knocks and breath.

**Recipe: build a path preset** (10 min each).
1. Ask the LLM: "Write an ffmpeg command that applies the D3 `radio` chain to `in.wav`, saving `out.wav` at 48 kHz." A typical answer: `ffmpeg -i in.wav -af "highpass=f=300,lowpass=f=3400,equalizer=f=1800:t=q:w=2:g=4,acompressor=threshold=0.1:ratio=4,acrusher=bits=10:mix=0.25" -ar 48000 out.wav`
2. Run it on one line; listen on a laptop and a phone; change one value at a time.
3. Save the final command as `PRESET-RADIO-01` and apply it to every line with that path (Audacity or DaVinci Resolve can do the same by hand).
4. **Intelligibility test:** play it quietly on a phone; if unclear, reduce saturation before narrowing the band [J].

**Starting filter strings** (each ran without error on FFmpeg 7.0.2 on 2026-09-27; the sound is a starting point, tune by ear). Use as `ffmpeg -i in.wav -af "<string>" -ac 1 -ar 48000 out.wav`:

| Path | `-af` string |
|---|---|
| `radio` | `highpass=f=300,lowpass=f=3400,equalizer=f=1800:t=q:w=2:g=4,acompressor=threshold=0.1:ratio=4,acrusher=bits=10:mix=0.25` |
| `earpiece` | `highpass=f=400,lowpass=f=3400,acompressor=threshold=0.125:ratio=3,asoftclip=type=tanh` |
| `intercom` | `highpass=f=250,lowpass=f=5000,acompressor=threshold=0.2:ratio=2` (then the listener's room reverb) |
| `device_speaker` | `highpass=f=500,lowpass=f=5000,asoftclip=type=tanh` |
| `helmet_internal` | `aecho=0.8:0.7:6\|9:0.3\|0.2,equalizer=f=300:t=q:w=1:g=3` |
| `helmet_external` | `lowpass=f=1800,volume=-8dB` |

(In the table the `|` inside `aecho` is escaped; type it as `aecho=0.8:0.7:6|9:0.3|0.2`.)

---

## 9. Dialogue editing

**Recipe: from takes to a dialogue stem**
1. **One file per line**, named `CATCH_SC10_DL0461_IONA_T02.wav` (project, scene, line ID = script line of the cue, speaker, take). Keep the original; make a 48 kHz WAV working copy (TTS gives 44.1 or 24 kHz) [J].
2. **Trim** to 0.2 s before the first sound and 0.3 s after the last; keep the in-breath, remove clicks.
3. **Word check** against `line_text` (rule 15).
4. **Time** each line to A2's `duration_s` and A1's `pause_after`; split edits per A4. For exact word times (sync, subtitles) use ElevenLabs `with-timestamps` or Forced Alignment, which finds each word's start and end [V S9].
5. **Seat**: continuous room tone (C3 `room_tone_key`), the location's short reverb on `direct` lines, path presets on the rest.
6. **Level** by ear against each character's calm reference line; never normalize line by line (whispers stay quiet).
7. **Breath and silence**: keep breaths that act ("Nothing but breath", l.1613, is a line in itself); every pause has room tone plus at most one sound (A1 R17; A4 SND4).
8. **Loudness** once, on the final mix, to A4's target (−23 LUFS EBU; −24 LKFS ATSC; about −14 web; Netflix −27 LKFS dialogue-gated [U S44: page now redirects and did not load]), e.g. `ffmpeg -i mix.wav -af loudnorm=I=-23:TP=-2 -ar 48000 mix_-23.wav` (ran on FFmpeg 7.0.2).
9. **Stems**: export the dialogue stem (relays included) apart from effects and music (A4).

---

## 10. Breakdown fields

### 10.1 Film level

| Field | Meaning | Allowed values |
|---|---|---|
| `voice_policy` | How voices may be made | `designed_only` \| `designed_plus_own_clone` \| `designed_plus_consented_clones` |
| `world_accent_rule` | Pointer to the accents the world uses (D17) | `WORLD.accents` (D17's reconciliation: locale lives in the WORLD record, not a `WR-` rule); value `undecided` blocks sync finals |
| `ai_voice_disclosure` | Label text and where it appears | text + `end_credits` \| `description` \| `platform_label` |
| `path_presets[]` | Saved chains | `PRESET-RADIO-01` |

### 10.2 Character level: the voice asset (`VOICE-` + name)

| Field | Meaning | Allowed values / example |
|---|---|---|
| `voice_id`, `character_id` | Asset and C5 character | `VOICE-SAYE`, `CH-SAYE` |
| `source` | How it was made | `prebuilt` \| `designed` \| `own_clone` \| `consented_clone` |
| `provider`, `provider_model`, `provider_voice_id` | Exact tool, model version, voice | `elevenlabs`, `eleven_v3`, vendor ID |
| `voice_brief` | Six lineup columns | {age_read, pitch_band: `low`\|`low_mid`\|`mid`\|`mid_high`\|`high`, timbre, accent, pace_wps, status_in_voice} |
| `design_prompt` | Frozen text; also the voice sentence for native-audio drafts | 30–50 words |
| `settings` | Defaults | {stability: `creative`\|`natural`\|`robust`, speed 0.7–1.2, style, seed} |
| `delivery_states[]` | Named states | {state_id `VOICE-SAYE.D02`, name, settings override, starts_at `SC24-DL1380`} |
| `reference_samples[]` | For audio-reference video models | 10–30 s per state (C1 P2); `video_voice_element` for Kling via fal |
| `consent_record_id` | Offline record | `null` if designed; `CONSENT-001` |
| `status` | Lock | `draft` \| `locked` (after accent rule and lineup test) |

### 10.3 Line level (ID = scene + `DL` + cue line number)

| Field | Meaning | Allowed values / example |
|---|---|---|
| `line_id` | Stable, script-derived | `SC10-DL0461` |
| `speaker`, `voice_id`, `voice_state` | Who, asset, state | `CH-IONA`, `VOICE-IONA`, `VOICE-IONA.D02` |
| `line_text`, `parenthetical` | Exact script text | "Not mint.", "(not steady)" |
| `tts_text` | As sent; same words | "[quietly] Not... mint." |
| `delivery` | ≤8 words from the playable action | "breath caught, quiet, bewildered" |
| `path` | How it reaches us | `direct` \| `off_screen` \| `earpiece` \| `radio` \| `intercom` \| `device_speaker` \| `recording` \| `helmet_internal` \| `helmet_external` \| `through_glass` \| `tape` \| `voice_over` \| `unsourced_room` |
| `listen_from` | Whose position we hear from, per shot | character ID \| `neutral` |
| `mouth_on_screen` | Speaking mouth visible | `visible` \| `hidden` \| `not_in_shot` |
| `sync_method` | How mouth and sound meet | `none` \| `native` \| `audio_reference` \| `post_lipsync` |
| `planned_duration_s`, `pause_before_s`, `pause_after_s` | From A2, A1 | seconds |
| `takes[]` | Take log | {take_id, alternate, file, model, settings, date, cost_usd, speech_s, words_match, verdict: `pick`\|`keep`\|`reject`, reason} |
| `picked_take`, `path_preset` | Choice; chain | `T02`, `PRESET-EARPIECE-01` |

### 10.4 Old names mapped

| Old field (file) | Becomes |
|---|---|
| `voice_key` (C5), voice half of `sound_key` (C3), `voice` (A3) | `voice_brief` + `design_prompt` |
| `bound_voice` (C3), `voice_sample`, `voice_video_element` (C1) | `reference_samples[]` |
| location half of `sound_key` (C3) | stays `room_tone_key` on the location |
| `voice_source` (A3), `channel` (C5), `perspective` (A4) | `path` |
| `audio_in` (C1) | file of `picked_take` |
| `speech_profile.voice: active \| passive` (A2) | **rename** `grammatical_voice`: grammar, not sound |

### 10.5 Alignment with the pipeline blueprint (added at fact-check, 2026-09-27)

The design blueprint (`design/blueprint.md`, §§ records and 8.6) already turned this file into records, with some different names. Where they differ, **the blueprint's names win** for the built pipeline; this file's extra values are proposals to add.

| This file | Blueprint | Action |
|---|---|---|
| voice asset `VOICE-IONA`; state `VOICE-IONA.D02` | VOICE record `VO-IONA` | Use `VO-`; keep states as `VO-IONA.D02` (D15 `voice_ref` also uses `VOICE-`; update it too) |
| line ID `SC10-DL0461` (cue line number) | SPEECH record; take ID `VT-` + speech + `-T` 2 digits, e.g. `VT-SC10-D11-T01` | Use the blueprint's speech IDs; keep the script line number in SPEECH `line` |
| `takes[]` inside the line | VOICETAKE record (speech, voice, delivery, tts_text, tool, file, verdict, cost_usd) | Use VOICETAKE; add `alternate`, `speech_s`, `reason` |
| `source`: prebuilt, designed, own_clone, consented_clone | `designed`, `user_recorded`, `actor_recorded`, `own_clone`, `consented_clone`, `native_draft` | Use the blueprint list; add `prebuilt` |
| `consent_record_id` `CONSENT-001` | VOICE `consent` = RIGHTS record `RT-001` (D4) | Use `RT-` IDs |
| paths `helmet_internal`, `helmet_external` | `helmet_inside`, `helmet_outside`; also `phone`, `thought` | Use the blueprint names; add `tape`, `unsourced_room` (The Long Places) |
| path presets `PRESET-RADIO-01` (renamed from `FX-RADIO-01`, which clashed with the blueprint's `FX-` finishing jobs) | VOICE `path_sound` (`treatment: ...`); FINISH operation `voice_path`; D9 preset names `earpiece_radio`, `small_speaker`, `helmet_inside` | One preset list shared with D9; this file's chains (§8.1) are the treatments |
| `voice_policy`, `ai_voice_disclosure` | SOUNDPLAN `voice_policy` (same values); disclosure text in D4 | Same |
| YAML in §11.1 | "YAML is not used" (record text) | §11.1 is shown for reading only |

---

## 11. Worked examples

### 11.1 SC10: "(not steady) Not mint." (l.461–463)

Context: "Chew that." (l.452), "Iona chews it." (l.454), "Her face changes." (l.456), "What does it taste of?" (l.459). A2 B7.b holds Iona's close-up, "the tightest size in the scene", through "Not mint." with Saye off screen, so her mouth is visible, perhaps still holding the leaf.

(Shown in YAML layout for reading; the pipeline stores the same fields as record text, §10.5.)

```yaml
line_id: SC10-DL0461
speaker: CH-IONA   voice_state: VOICE-IONA.D02   # cracked: first break of her work voice
line_text: "Not mint."
parenthetical: "(not steady)"
delivery: "breath caught, quiet, bewildered"
path: direct   listen_from: neutral   mouth_on_screen: visible
planned_duration_s: 1.3        # A2: 2 words / 2.5 + 0.5
alternates:
  A: {tts_text: "[quietly] Not... mint.", stability: natural, speed: 0.9}
  B: {tts_text: "[exhales] Not mint.",   stability: creative, speed: 0.95}
  C: {method: speech_to_speech, note: "user says it with a mint leaf in the mouth, chewing stopped"}
takes: 3 per alternate; reject any that says "exhales" aloud or adds a word
sync_method: audio_reference   # fallback post_lipsync sync-3; check the "m" closure in "mint"
```

Pick the take whose pitch drops on "mint" with an audible in-breath; Saye's reply ("Nothing has happened to the mint.") stays in her D01 answers voice for contrast. Cost: under 300 TTS characters; sync-3 fallback ≈ 2 s × 2 tries × $0.133 ≈ $0.53 [J from S28].

### 11.2 SC13: "One body." / "One." / "You." timed to the pause ranking (l.759–772)

A1 ranks "She waits." (after "What was it rated for?") as the pre-turn pause (rank 2, long hold, 3 s, "room tone, monitor hum"); "Silence." is the post-turn pause (cut wide once, then hold; by R15 the other long hold [J]). A1 stays on Iona, Eli off screen, and marks "You." by a cut-in or camera stop on her face.

| t (s) | Sound | Picture (A1) | Voice settings |
|---|---|---|---|
| 0.0–3.2 | room tone + monitor hum ("She waits.") | OTS on Eli, no cut | — |
| 3.2 | ELI "One body." (~0.8 s) | Iona single, Eli off screen | D01, Robust, speed 0.95 |
| 4.3 | IONA "One." (~0.4 s), 0.3 s after him | same shot | D02, Natural |
| 4.7–5.7 | ~1.0 s silence: Eli's habit (B5) | same shot | edit gap |
| 5.7 | ELI "You." (~0.4 s) | cut-in on Iona on "You." | D01, Robust |
| 6.1–9.5+ | "Silence.": room tone + hum, no music | cut wide once, hold ≥3 s | — |

Method (rule 13): generate the exchange from "What was it rated for?" to "You." as one two-voice call (ElevenLabs Text to Dialogue or Gemini two-speaker), 3 takes; cut per line by timestamps; re-space to the table. Eli needs no sync. Iona's "One." is a 0.4 s word on a still close-up: sync-3 (it can open still lips) or the close-up generated with her line as audio reference. No hesitation sounds for Eli: they would lower his high information status (B5).

### 11.3 JUDE (V.O.) in her ear: SC02 and SC04 (not SC01)

Correction to the brief's "SC01–02": SC01 has Jude on screen and one `off_screen` Iona line ("They all say that.", l.21–22). The earpiece lines are SC02 l.93–95 ("(in her ear)" / "Was that you?") and SC04 l.176–177 ("Cage is coming. Thirty seconds."), which inherits the earpiece (A3 R15). B5 puts it in her left ear (design choice).

- **SC02:** `VOICE-JUDE.D01`, easy with a thread of worry; clean take, then `PRESET-EARPIECE-01`, mono, centre, no shaft reverb (the voice is inside her ear). Her answer, "(through the torch)" / "No." (l.97–99): `direct`, close, STS with a pencil between the teeth; no lip sync ("Her jaw shuts on the torch."). "Behind one, a radio, far off." (l.79) is an effect behind a door, not a voice asset.
- **SC04:** "Cage is coming. Thirty seconds." lands between gunshots; pull the gunshot tails under the line (A4 SND7). Iona's "Jude. Now." (SC03, l.124–125) is her transmitting: `direct`.
- **Flag:** is the torch still in her teeth for "It was my tooth." (l.104), after she "Spits into the dark."?

### 11.4 SAYE (RECORDED) on the wrist display: SC23 and SC24

"Saye's recorded face appears on her wrist." (l.1269). SC23 plays three recorded lines (l.1271–1286); Iona answers "Give me time." (l.1282) to a recording that cannot hear her: "The recording goes on." (l.1284). SC24: "They're here. Nell is here." / "Saye has lost the voice she uses for answers." / "Iona. Leave the ship." (l.1380–1386).

| | SC23 | SC24 |
|---|---|---|
| Delivery state | `VOICE-SAYE.D01` answers voice: slow, complete, falling ends, 2.0 w/s | `VOICE-SAYE.D02` lost answers voice: faster then stalling, pitch up, breath before "Nell", her only contraction |
| Settings | Robust, speed 0.9 | Creative, speed 1.0, one tag such as `[shaky]`; or STS of the user's own performance |
| Path | `recording` → wrist `device_speaker` → inside Iona's helmet: `PRESET-WRIST-01` then `PRESET-HELMET-IN-01` | identical chain |
| Picture | Saye's face as its own full-frame clip, lip-synced (Hedra Character-3 or an audio-reference model), composited onto the display (C1 R23) | same |

The identical path makes the audience hear the change in Saye, not the device. Test the D01/D02 pair **after** processing, because band-limiting flattens differences. The (beat) line (l.1276–1279) is two files about 1 s apart; its 29-word first part runs about 14.5 s at 2.0 w/s, so split the screen clip at a sentence end if the model's limit requires (C1).

### 11.5 Iona inside the visor (SC23–SC28; SC18–SC22 by design choice)

The script names the visor first at l.1296 ("She checks the load on her visor.") and the helmet at l.1567 and l.1610–1618; B5 puts the helmet on from SC18, a choice to confirm.

- **Her lines on the ship**, heard from her side: `helmet_internal`, breath kept ("Breath in the helmet.", l.1583). "All of us. I can't do it without you turning too." (SC26, l.1543), to the animal: close, low, D03.
- **Heard by Eli, Jude and Nell** by radio ("She puts a radio in the drawer that goes through his wall.", l.1120): a shot from Eli's side hears her as `radio` in his room. Rule 25: two versions of the take, crossfaded at the cut.
- **SC28:** "(into her helmet)" / "Other shoulder, Io.": Jude reaches us through the shell (low-pass ~2.5 kHz, close). "She tries to answer. Nothing but breath." is a breath file. After Saye's "Leave it on." (l.1618), Iona's SC28 lines are `helmet_external` for the room, unless the user adds a suit speaker (not in the script).
- **Lip sync:** none through the visor (rule 22): play her lines over the visor display, from behind, in profile against glare, or on the listener; composite a clean face under the visor (D6) only for a line that must be seen.

### 11.6 The Long Places, ch. XI: the tape and the voice from the room

Melek: "Record it, kızım. The tape will keep the voice and lose the smell of the oil, and the oil is the half of it." (l.985). In the singing room, whose note is "a low A, one hundred and ten hertz" (l.306), Nilay plays the tape and the closing phrase comes back: "Not from the machine. From the room's own air, off no wall she could point to", "a young woman's voice, level, without performance, in the manner of someone returning a borrowed thing" (l.1027).

- Melek's song: `path: tape`, then the stone room's long reverb with a resonance near 110 Hz [J]. Singing is weak in TTS (v3 lists `[sings]`); prefer a consenting singer or a music model; flag it.
- The returned phrase: `path: unsourced_room`. It carries **none** of the tape chain (the text rules out the machine), only diffuse room reverb with no direction. New designed voice, lineup-tested against Nilay and Melek; "level, without performance": Robust, no tags.
- "kızım": IPA in slashes for v3, or a pronunciation dictionary on v2/Flash [V S3]; first decide the on-screen language (D18).

---

## 12. Decision table: which dialogue route, and cost per finished minute

Video costs use C1's prices and its "typical" 8× generated-to-finished ratio; audio costs use §2. All results are [J] arithmetic.

| Route | Use when | Avoid when | Cost per finished minute of dialogue |
|---|---|---|---|
| **Off-screen line** over a listener, insert or wide | The listener carries the line; relays; any doubt | The speaker's face is the point | TTS ≈ $0.02–1 on top of picture you need anyway; no sync risk |
| **Voice first + audio-reference model** (C1 R1) | On-screen close-ups of recurring speakers | Visors, bearded profiles, two speakers per clip (C1 R2) | TTS ≈ $1; video $0.13–0.47/s × 480 s ≈ **$62–226** |
| **TTS + lip sync in post** | Silent-model or performance-transfer picture; failed audio-reference takes | Obstructed mouths | $0.112/s × 480 s ≈ $54 + sync 60 s × 2 × $0.083–0.133 ≈ $10–16 → **≈ $64–70** |
| **Native model audio** | Drafts; one-line parts | Any recurring speaker | $0.168/s × 480 s ≈ **$81**, plus re-dos when voices drift |

**The Catch's voice budget [J]:** 7,666 characters × 3 takes plus alternates ≈ 26,000 characters. On ElevenLabs (1 credit per character on v3) that nearly fills Starter ($6, 30k credits) with no room for Voice Design previews or redos, so plan one month of Creator ($22, or $11 the first month; 121k credits). On Gemini 3.8 Flash TTS it is about $0.50 (≈12 min × 3 takes × $0.0135/min; 25 audio tokens per second at $9 per million), doubling after 31 Dec 2026. Sync is where money goes: if 45% of line-seconds still show mouths, sync-3 costs about 330 s × 2 tries × $0.133 ≈ $88.

---

## 13. Failure modes and fixes

| Failure | Sign | Fix |
|---|---|---|
| Voice drift | A character sounds different after a break | Lock provider, model version, voice ID, settings; regenerate the scene (rule 5) |
| Wrong words or spoken tags | Transcript mismatch | Reject; Robust stability; fewer tags |
| Short line sounds random | "You." varies wildly | Generate in context and cut (rule 13) |
| Voices blur | Listeners confuse two | Lineup test; change pitch band or pace |
| Relay unintelligible | Phone test fails | Less saturation first, then widen the band |
| Relay sounds pasted on | Radio with no space around it | Reverb of the listener's room after the chain |
| Lips miss "m/b/p" | Mouth open on "mint" | sync-3; retry once; cut away |
| Beard smear | Eli's mouth blurs | lipsync-2-pro or sync-3; wider framing; off screen |
| Wrong face moves | Listener's lips move | Mask the silent face; A4 AI7 listener clip |
| Model retired | Voice unavailable | Keep clean masters, samples, settings; recast with the lineup test |

---

## 14. Checklists

**Voice asset, before `locked`:** accent rule decided; design prompt names no real person; lineup test passed, also through each relay; delivery states listed with start lines; 10–30 s reference samples saved; source `designed`/`prebuilt`, or consent record and vendor verification present; provider, model version, settings recorded.

**Each line, before `picked_take`:** `line_text` exact and `tts_text` same words; paths treated as paths; "(beat)" split; 3 takes (2 × 3 for marked lines), transcripts match; length within ±20% of plan; Saye: no contractions except "They're here." (SC24).

**Each scene, before picture lock:** off-screen rule applied first; sync checked at half speed on every visible mouth; room tone continuous; presets applied per `listen_from`; pauses match A1's ranking.

**Release:** AI-voice credit and watermarks; consent records offline, scope respected; dialogue stem exported, loudness per A4.

---

## 15. Open questions for the user

1. Country, period and accent of *The Catch* (blocks locking voices; D17).
2. Whether Nell shares the accent.
3. Whether Iona's helmet is on in SC18–SC22, and whether the suit has an external speaker in SC28.
4. Whether the torch is still in Iona's teeth for "It was my tooth." (SC02).
5. Whether any voice will be the user's own clone (`voice_policy`).
6. *The Long Places*: letters as voice-over and whose voice (A4 open item); on-screen language.
7. Before paying: does the chosen TTS plan's licence cover film and festival distribution? D9 found every self-serve ElevenLabs *Music* plan excludes "film, TV, radio"; this check found no such limit for speech, but the TTS terms page was not opened [U].
8. Which glass world rule applies (§8.1): intercom for speech, or no speech through glass?

---

## Sources (all checked 2026-09-27)

- S1 ElevenLabs pricing — https://elevenlabs.io/pricing [V]
- S2 ElevenLabs models — https://elevenlabs.io/docs/overview/models [V]
- S3 ElevenLabs TTS best practices — https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices [V]
- S4 ElevenLabs Instant Voice Cloning — https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/instant-voice-cloning [V]
- S5 ElevenLabs Professional Voice Cloning — https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning [V]
- S6 ElevenLabs Voice Design — https://elevenlabs.io/docs/eleven-creative/voices/voice-design [V]
- S7 ElevenLabs Voice Changer API — https://elevenlabs.io/docs/api-reference/speech-to-speech/convert [V]
- S8 ElevenLabs MCP repository (archived) — https://github.com/elevenlabs/elevenlabs-mcp [V]
- S9 ElevenLabs speech with timestamps — https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps ; Forced Alignment — https://elevenlabs.io/docs/overview/capabilities/forced-alignment ; Text to Dialogue with timestamps — https://elevenlabs.io/docs/api-reference/text-to-dialogue/convert-with-timestamps [V]
- S10 ElevenLabs voice cloning concepts — https://elevenlabs.io/docs/eleven-api/concepts/voice-cloning [V]
- S11 OpenAI text-to-speech guide — https://developers.openai.com/api/docs/guides/text-to-speech [V]
- S12 OpenAI gpt-4o-mini-tts — https://developers.openai.com/api/docs/models/gpt-4o-mini-tts [V]; per-minute estimate https://costgoat.com/pricing/openai-tts [U]
- S13 Gemini API speech generation — https://ai.google.dev/gemini-api/docs/speech-generation [V]
- S14 Gemini API pricing — https://ai.google.dev/gemini-api/docs/pricing [V]
- S15 Gemini API voice replication — https://ai.google.dev/gemini-api/docs/voice-replication [V]
- S16 Android Authority, Gemini 3.8 TTS — https://www.androidauthority.com/gemini-3-8-flash-text-to-speech-rolling-out-3714915/ [U]
- S17 Azure personal voice overview — https://learn.microsoft.com/en-us/azure/ai-services/speech-service/personal-voice-overview [V]
- S18 Azure personal voice consent — https://learn.microsoft.com/en-us/azure/ai-services/speech-service/personal-voice-create-consent [V]
- S19 Microsoft Community Hub, HD voices — https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/azure-speech-%E2%80%93-neural-hd-text-to-speech-recent-voice-updates/4505380 [V]
- S20 Cartesia pricing — https://cartesia.ai/pricing [V]
- S21 Cartesia Sonic — https://cartesia.ai/sonic [V]
- S22 Hume pricing — https://www.hume.ai/pricing [V]
- S23 Hume acting instructions — https://dev.hume.ai/docs/text-to-speech-tts/acting-instructions [V]
- S24 Chatterbox (Resemble AI) — https://github.com/resemble-ai/chatterbox [V]
- S25 Dia — https://github.com/nari-labs/dia [V]
- S26 IndexTTS — https://github.com/index-tts/index-tts [V]
- S28 sync. lipsync models — https://sync.so/docs/models/lipsync [V]
- S29 sync. pricing — https://sync.so/pricing [V]
- S30 Kling lip sync guide — https://kling.ai/quickstart/ai-lip-sync-guide [V]
- S31 Runway Act-Two — https://help.runwayml.com/hc/en-us/articles/42311337895827-Performance-Capture-with-Act-Two [blocked 403; price and limits verified in D15 §5.1 from Runway's API docs]
- S32 Hedra Character-3 — https://www.hedra.com/models/video/hedra/character-3 [V]
- S33 LatentSync — https://github.com/bytedance/LatentSync [V]
- S34 MuseTalk — https://huggingface.co/TMElyralab/MuseTalk [V]
- S35 InfiniteTalk — https://github.com/MeiGen-AI/InfiniteTalk [V]
- S36 Tennessee ELVIS Act, HB 2091 text — https://www.capitol.tn.gov/Bills/113/Bill/HB2091.pdf [V]
- S37 NO FAKES Act of 2026, Holland & Knight — https://www.hklaw.com/en/insights/publications/2026/06/senate-judiciary-committee-advances-legislation-to-protect-name [V]; https://www.congress.gov/bill/119th-congress/senate-bill/4591 (blocked)
- S38 European Commission, Article 50 FAQ — https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act [V]
- S39 California AB 2602 — https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB2602 [V]
- S40 New York synthetic performer disclosure, S.8420-A text — https://www.nysenate.gov/legislation/bills/2025/S8420/amendment/A ; Governor's announcement (in effect 9 June 2026) — https://www.governor.ny.gov/news/governor-hochul-announces-first-nation-law-requiring-disclosure-when-advertisements-include-ai [V]
- S41 China labelling measures — https://www.chinalawtranslate.com/en/ai-labeling/ [V]
- S42 European Parliament, Denmark — https://www.europarl.europa.eu/RegData/etudes/ATAG/2026/782611/EPRS_ATA(2026)782611_EN.pdf [U]
- S43 YouTube disclosure — https://support.google.com/youtube/answer/14328491 [V]
- S44 Netflix sound mix specifications — https://partnerhelp.netflixstudios.com/hc/en-us/articles/360001794307-Netflix-Sound-Mix-Specifications-Best-Practices-v1-6 [U]
- S45 ITU-T G.712 — https://www.itu.int/rec/dologin_pub.asp?lang=e&id=T-REC-G.712-200111-I!!PDF-E&type=items [V]
- S46 FFmpeg filters — https://ffmpeg.org/ffmpeg-filters.html [V]
- S47 NO FAKES Act status after committee — search summaries of https://www.govtrack.us/congress/bills/119/s4591 and https://www.aifashionlaw.com/article/the-no-fakes-act-what-it-means-for-models-digital-likeness-2026-09-01 (GovTrack returned 403) [U]
- Fact-check note (2026-09-27): corrected Hume's commercial terms, ElevenLabs Dubbing Studio tier, Gemini's reported blocked regions, Dia's languages; added EU Art. 50(2) grace date, NY exemptions, NO FAKES status; S3's short-prompt advice is no longer on the current page.
- Library: A1, A2, A3, A4, B5, C1, C3, C5, D4, D9, D15, D17, the design blueprint and the critic's conflict list. Scripts: *The Catch* (workshop revision, 25 Sept 2026) and *The Long Places* (revised final); line numbers from the files.
