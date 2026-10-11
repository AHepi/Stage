# Digest D3: Voice casting and dialogue audio for AI filmmaking (27 Sept 2026)

Source: `research/D3_voice_dialogue_audio.md` (fact-checked 27 Sept 2026). Brackets: §3 rule n = decision rule; §1.n = principle; other § = section. **[V]** primary page read 27 Sept 2026; **[U]** unverified; **[J]** judgment. After 27 Oct 2026, re-check prices before paying.

## 1. Scope

1. Turns every spoken line into a finished audio file: tool, voice, delivery, three takes, the device it is heard through, and how it meets the picture (off screen, audio-reference model, or post lip sync).
2. Adds a VOICE section to each B5 character, one frozen voice record with delivery states per speaker, and a lineup test so no two voices blur.
3. Sets consent and labelling rules for designed and cloned voices, and works everything through *The Catch* and one *Long Places* chapter.

**Terms** [§0]: *TTS* = text read aloud by a synthetic voice; *clone* = a voice copied from a real person; *STS* = you perform the line, the tool swaps in the character's voice; *audio tag* = bracketed direction (`[whispers]`); *delivery state* = a named way one voice sounds for a stretch of story; *alternate* = a different reading with its own takes; *path* = how a line reaches us (direct, earpiece, radio...); *audio-reference model* = a video model driven by your line audio.

## 2. Rules

**Choosing tools**
1. [§3 rule 1; §1.1] If a character speaks in more than one scene, then lock one voice record (provider, voice ID, model version, frozen settings) before any video with a visible speaking mouth, because fresh voices per clip do not match (C1 R1).
2. [§3 rule 2] If opening the first voice account, then use ElevenLabs (Starter $6/30k credits is the cheapest commercial plan; Creator $22/121k leaves room for redos) or, cheapest, Gemini 3.8 Flash TTS, because both cover design, tags and two-speaker exchanges, and *The Catch* needs ≈ 26,000 characters [V prices; J].
3. [§3 rule 3] If a line's acting is hard to write (mouth full, whisper, breath for a word), then perform it on a phone and convert it with STS, because STS keeps your timing and breath [J].
4. [§3 rule 4] If the work must stay offline or free, then use Chatterbox (MIT) or Dia (Apache 2.0, English only), because IndexTTS2's bilibili licence is not a standard open licence [V].
5. [§3 rule 5] If the vendor changes the model mid-project, then regenerate whole scenes, because one voice ID can sound different on a new model [J].

**Casting**
6. [§3 rule 6] If `WORLD.accents` is `undecided` (D17), then cast with a placeholder accent, keep voices `draft`, and make no synced finals, because an accent change redoes every sync shot [J].
7. [§3 rule 7; §4.3] If two voices share three or more of the six lineup columns (age, pitch band, timbre, pace, accent, status), then change pitch band or pace first, because similar voices blur on small speakers [J].
8. [§3 rule 8] If `speech_profile` says `contractions: no` (Saye), then check transcripts for slipped-in contractions and keep her near 2.0 words/s, because her one contraction ("They're here.", SC24) is a story event [V script].
9. [§3 rule 9] If the script writes a pausing habit ("Eli thinks before he answers. He always does.", l.1142), then make the ~1 s pause a silence in the edit, because it can still be tuned there.

**Delivery**
10. [§3 rule 10; §5.3] If a line has a delivery parenthetical, is a turning line or starts a delivery state, then make 2 alternates × 3 takes (otherwise 3 takes), because parentheticals are the writer's only acting notes.
11. [§3 rule 11] If a parenthetical names a place or device ("in her ear", "over the radio", "into her helmet", "from the back"), then treat it as a path, because it describes hearing, not acting [J].
12. [§3 rule 12] If a line contains "(beat)", then split it into two files about 1 s apart, because a pause inside a file cannot be moved.
13. [§3 rule 13] If a line has three words or fewer, then generate it inside its exchange and cut it out, because very short inputs are inconsistent [U: earlier ElevenLabs guide only; J].
14. [§3 rule 14; §1.4] If the text sent to the tool changes, then keep the spoken words identical and store `line_text` and `tts_text` separately, because C3 L31 fails lines that differ from the script.
15. [§3 rule 15] If choosing between takes, then transcribe each, reject wrong words or spoken tags, then pick by ear, because Creative is "prone to hallucinations" [V].

**Consent and law** (not legal advice)
16. [§3 rule 16] If anyone proposes cloning a real person, then require a signed consent record and the vendor's own verification, and never clone from existing recordings, a celebrity, a dead person or a minor (project policy, stricter than law), because the ELVIS Act covers "the actual voice or a simulation of the voice of the individual" [V].
17. [§3 rule 17] If the clone is the user's own voice, then it is allowed with the vendor's verification as evidence, because the owner consents; YouTube exempts "Cloning one's own voice to create voice overs or dubs" [V].
18. [§3 rule 18] If writing a design prompt, then never name a real person or write "sounds like [name]", because a recognizable imitation is that person's voice under ELVIS [V].
19. [§3 rule 19] If the film is shown in the EU from 2 Aug 2026, on YouTube, or uses OpenAI voices, then add D4's credit line naming the voice tool, keep watermarks and fill `ai_voice_disclosure`, because OpenAI requires saying the voice "is AI-generated", YouTube labels realistic synthetic content and Article 50 covers deepfakes [V]; a designed voice resembling no one is probably not one, so for the EU this is insurance [J].
20. [§6.1] If a New York trailer or ad shows a generated person differently from the film, then add a synthetic-performer notice, because the 9 June 2026 law exempts film ads only where use matches the work [V].

**Lip sync**
21. [§3 rule 20; §1.5] If the listener can carry the line (A1 R1, A2 R27), then play it off screen, because it costs nothing and cannot drift.
22. [§3 rule 21] If the mouth must be seen, then use an audio-reference video model first, post lip sync second (sync-3 for profiles and obstructions; lipsync-2-pro for frontal beards), a cutaway third, because each step down costs and risks less.
23. [§3 rule 22] If the mouth is behind a visor, glass, hand or prop, then avoid on-screen sync (from behind, in profile, over the visor display, or a composited face, D6), because obstructions are the named weak point [V S28; J visors].
24. [§3 rule 23] If post lip sync fails twice on one shot, then cut to the listener or an insert, because C1 rule 24 says switch method.

**Paths and edit**
25. [§3 rule 24; §1.3] If a voice reaches us through a device, then generate it clean and apply one saved chain per path in post, because "sound like a radio" in TTS varies between takes [J].
26. [§3 rule 25] If a line crosses a cut from the speaker's side to the listener's, then process per shot and crossfade the two versions, because the path depends on where we listen [J].
27. [§3 rule 26] If a take misses the planned duration (words ÷ 2.5 + 0.5 s; Saye 2.0 words/s) by more than 20%, then pick another take or change speed, never time-stretch beyond ~8%, because stretching smears consonants [J].
28. [§3 rule 27; §1.8] If the dialogue is TTS, then run room tone under the whole scene plus the location's short reverb, because dry voices sound pasted on [J].
29. [§8.1] If characters talk through the quarantine glass (SC11–13, SC17, SC29), then apply one world rule: `intercom` for speech, `through_glass` for knocks and breath only, because the script never says and C3's intercom is a design choice [J].

## 3. Breakdown fields

Blueprint names, where different, are in brackets and **win** (§10.5).

| Level | Field name | Meaning | Allowed values / example |
|---|---|---|---|
| film | `voice_policy` (SOUNDPLAN) | How voices may be made | `designed_only` \| `designed_plus_own_clone` \| `designed_plus_consented_clones` |
| film | `world_accent_rule` | Pointer to the accents the world uses | `WORLD.accents` (D17); `undecided` blocks sync finals |
| film | `ai_voice_disclosure` | Label text and where it shows | text + `end_credits` \| `description` \| `platform_label` |
| film | `path_presets[]` | Saved chains per path | `PRESET-RADIO-01` (renamed from `FX-`, which clashes with blueprint FINISH jobs) |
| character (voice) | `voice_id`, `character_id` | Voice record and its character | `VOICE-SAYE` [blueprint `VO-SAYE`], `CH-SAYE` |
| character | `source` | How the voice was made | `prebuilt` \| `designed` \| `own_clone` \| `consented_clone` [blueprint adds `user_recorded`, `actor_recorded`, `native_draft`] |
| character | `provider`, `provider_model`, `provider_voice_id` | Exact tool, model version, voice | `elevenlabs`, `eleven_v3`, vendor ID |
| character | `voice_brief` | The six lineup columns | {age_read, pitch_band: `low`\|`low_mid`\|`mid`\|`mid_high`\|`high`, timbre, accent, pace_wps, status_in_voice} |
| character | `design_prompt` | Frozen voice description, also the voice sentence in native-audio drafts | 30–50 words, `{accent}` slot, no real names |
| character | `settings` | Default generation settings | {stability: `creative`\|`natural`\|`robust`, speed 0.7–1.2, style, seed} |
| character | `delivery_states[]` | Named states | {state_id `VOICE-SAYE.D02`, name, settings override, starts_at `SC24-DL1380`} |
| character | `reference_samples[]` | Audio for audio-reference video models | 10–30 s per state (C1 P2); `video_voice_element` for Kling via fal |
| character | `consent_record_id` [blueprint `consent` = `RT-` RIGHTS ID] | Offline consent record | `null` if designed; `RT-001` |
| character | `status` | Lock | `draft` \| `locked` (after accent decided and lineup test passed) |
| line [blueprint SPEECH] | `line_id` | Stable script-derived ID | `SC10-DL0461` (scene + DL + cue line) |
| line | `speaker`, `voice_id`, `voice_state` | Who, voice, state | `CH-IONA`, `VOICE-IONA`, `VOICE-IONA.D02` |
| line | `line_text`, `parenthetical` | Exact script text | "Not mint.", "(not steady)" |
| line | `tts_text` | Text as sent; same words | "[quietly] Not... mint." |
| line | `delivery` | ≤8 words from the playable action | "breath caught, quiet, bewildered" |
| line | `path` | How it reaches us | `direct` \| `off_screen` \| `earpiece` \| `radio` \| `intercom` \| `device_speaker` \| `recording` \| `helmet_internal` [`helmet_inside`] \| `helmet_external` [`helmet_outside`] \| `through_glass` \| `tape` \| `voice_over` \| `unsourced_room` |
| line (per shot) | `listen_from` | Whose position we hear from | character ID \| `neutral` |
| line (per shot) | `mouth_on_screen` | Speaking mouth visible | `visible` \| `hidden` \| `not_in_shot` |
| line (per shot) | `sync_method` | How mouth and sound meet | `none` \| `native` \| `audio_reference` \| `post_lipsync` |
| line | `planned_duration_s`, `pause_before_s`, `pause_after_s` | From A2 and A1 | seconds, e.g. 1.3 |
| take [blueprint VOICETAKE `VT-`] | `takes[]` | Take log | {take_id, alternate, file, model, settings, date, cost_usd, speech_s, words_match, verdict: `pick`\|`keep`\|`reject`, reason} |
| line | `picked_take`, `path_preset` | Choice; chain | `T02`, `PRESET-EARPIECE-01` |

Replaced [§10.4]: `voice_key`, `sound_key` (voice half), A3 `voice` → `voice_brief`; `bound_voice`, `voice_sample` → `reference_samples[]`; `voice_source`, `channel`, `perspective` → `path`.

## 4. Procedures

**P1. Add the VOICE section to a B5 entry** [§4.1] (after STATUS in B5 §7.1):
```
VOICE:
  VOICE BRIEF:      age read | pitch band | timbre (≤3 words) | accent (world rule) | pace (words/s) | status in the voice
  SPEECH PROFILE:   from A2 (sentence length, contractions, vocabulary field)
  DESIGN PROMPT:    30–50 words, frozen word order, no real names, {accent} slot
  DELIVERY STATES:  D01 default ... with the scene where each starts
  LINEUP ROW:       six columns (§4.3)
  SOURCE:           designed | prebuilt | own-voice clone | consented clone (+ consent record ID)
```
Status in the voice (B5 §5.3): high status = level, falling ends, no fillers; low status = rising ends and "hesitation sounds before speaking".

**P2. Design one voice without code** [§4.3] (20 min per voice)
1. Ask the LLM to fill `{accent}` from `WORLD.accents` (placeholder while undecided) and write one 20–30-word test line in the character's own speech pattern, from the script.
2. In ElevenLabs open Voices, then Voice Design; paste the design prompt and the test line; generate three previews.
3. Listen on a phone speaker. If none fits, change one phrase and regenerate; stop after three rounds and take the closest.
4. Save as `VOICE-IONA`; copy the voice ID, model (`eleven_v3`), stability and speed into the voice record.
5. Run the lineup sentence against the voices already cast before designing the next.
6. When all pass, export 10–30 s per delivery state as `reference_samples`; lock only when the accent is decided.

**P3. Lineup test** [§4.3] (15 min, under $1)
1. Ask the LLM for one neutral 20-word sentence; generate it in all five voices.
2. Have it rename the files 1–5 in random order and keep the key.
3. Next day, name each voice from a phone speaker; on any confusion change one voice's pitch band or pace and retest.
4. Repeat through each relay you will use, because band-limiting erases pitch and timbre differences first.

**P4. Direct one scene's dialogue** [§5.4] (30–60 min, about $0.10–1)
1. Paste the scene, its A1/A2 plan (turning line, pauses), A3 playable actions and the voice records. Say: "Make one D3 line record per cue. Copy `line_text` exactly. Put at most two audio tags in `tts_text`, split at (beat), and mark path parentheticals as paths."
2. Check words, speakers and paths yourself.
3. Have the LLM (through the ElevenLabs MCP, or a script it writes) generate 3 takes per line, named as in P7.
4. Have it transcribe every take and delete mismatches.
5. Listen in scene order, pick, and give your reasons.
6. Have it log picks and durations and flag takes outside ±20% of `planned_duration_s`.

**P5. Build a path preset** [§8.1] (10 min each)
1. Ask the LLM: "Write an ffmpeg command that applies the D3 `radio` chain to `in.wav`, saving `out.wav` at 48 kHz." A typical answer: `ffmpeg -i in.wav -af "highpass=f=300,lowpass=f=3400,equalizer=f=1800:t=q:w=2:g=4,acompressor=threshold=0.1:ratio=4,acrusher=bits=10:mix=0.25" -ar 48000 out.wav`
2. Run it on one line; listen on a laptop and a phone; change one value at a time.
3. Save the final command as `PRESET-RADIO-01`; apply it to every line with that path (or by hand in Audacity or Resolve).
4. Intelligibility test: play quietly on a phone; if unclear, reduce saturation before narrowing the band.

Starting strings (all ran on FFmpeg 7.0.2 on 27 Sept 2026; use as `ffmpeg -i in.wav -af "<string>" -ac 1 -ar 48000 out.wav`):
- `radio`: the string in step 1.
- `earpiece`: `highpass=f=400,lowpass=f=3400,acompressor=threshold=0.125:ratio=3,asoftclip=type=tanh` (mono, centre, 3–6 dB under direct, no reverb)
- `intercom`: `highpass=f=250,lowpass=f=5000,acompressor=threshold=0.2:ratio=2` (then the listener's room reverb)
- `device_speaker`: `highpass=f=500,lowpass=f=5000,asoftclip=type=tanh`
- `helmet_internal`: `aecho=0.8:0.7:6|9:0.3|0.2,equalizer=f=300:t=q:w=1:g=3` (breath kept)
- `helmet_external`: `lowpass=f=1800,volume=-8dB`
- Others [§8.1]: `off_screen` more reverb, 1–3 dB lower; `recording` = device chain plus the recorded room; `through_glass` low-pass 1–1.5 kHz, 12 dB down, non-verbal only; `tape` 60–10,000 Hz, wow and hiss, then the room.

**P6. Post lip sync one shot** [§7.2] ($0.10–1)
1. Lock the picked take, trimmed to 0.2 s before the first sound.
2. Generate the picture with natural speaking motion ("speaks quietly"); a still face is fine only for sync-3.
3. Upload clip and audio to sync. (app or API); with two faces in frame, turn on active-speaker detection.
4. Check at half speed: lips close on every "m", "b", "p" ("mint", "body"); no teeth flicker; no beard smear.
5. Two failures: cut away (rule 24). After any audio slip in the edit, re-check sync (C5 R31).

**P7. From takes to a dialogue stem** [§9]
1. One file per line, named `CATCH_SC10_DL0461_IONA_T02.wav` (project, scene, line ID = cue's script line, speaker, take). Keep the original; work on a 48 kHz WAV copy.
2. Trim to 0.2 s before the first sound and 0.3 s after the last; keep the in-breath, remove clicks.
3. Word check against `line_text`.
4. Time each line to A2's `duration_s` and A1's `pause_after`; for exact word times use ElevenLabs with-timestamps (speech or Text to Dialogue) or Forced Alignment [V].
5. Seat: continuous room tone, the location's short reverb on `direct` lines, path presets on the rest.
6. Level by ear against each character's calm reference line.
7. Keep breaths that act ("Nothing but breath", l.1613); every pause gets room tone plus at most one sound (A1 R17).
8. Loudness once on the final mix to A4's target (−23 LUFS EBU; −24 LKFS ATSC; about −14 web; Netflix −27 LKFS dialogue-gated [U]): `ffmpeg -i mix.wav -af loudnorm=I=-23:TP=-2 -ar 48000 mix_-23.wav`.
9. Export the dialogue stem (relays included) apart from effects and music.

**P8. Clone a consenting person** [§6.2–6.3] (only if designed voices will not do)
1. Have the LLM turn the consent fields into a one-page plain-language agreement; the person signs it. Fields: record ID; full name; date; adult (yes/no); scope (project, characters, media, territories, duration); whether new lines beyond the script are allowed; payment; how to withdraw and what happens to finished work; vendor verification result; where samples are kept; deletion date; signature.
2. Record 1–2 minutes of clean speech (no more than 3) in the delivery you want; the clone copies pace, inflection, accent and breathing [V].
3. The person completes the vendor's verification themselves (ElevenLabs professional clones: own voice only; Gemini and Azure: a recorded consent statement).
4. Keep recordings and the record offline; only the record ID goes in the voice record. Never: clone from film, TV, podcasts or videos; prompt "in the voice of" anyone real; use a minor's voice; remove watermarks.

**P9. Choose the dialogue route** [§12] (cost per finished minute, [J] arithmetic from C1 prices and its 8× generated-to-finished ratio)
| Route | Use when | Avoid when | Cost |
|---|---|---|---|
| Off-screen line over a listener, insert or wide | Listener carries the line; relays; any doubt | The speaker's face is the point | TTS ≈ $0.02–1; no sync risk |
| Voice first + audio-reference model | On-screen close-ups of recurring speakers | Visors, bearded profiles, two speakers per clip | ≈ $62–226 |
| TTS + lip sync in post | Silent or performance-transfer picture; failed audio-reference takes | Obstructed mouths | ≈ $64–70 |
| Native model audio | Drafts; one-line parts | Any recurring speaker | ≈ $81 plus redos |

## 5. Checklists

- **Voice record, before `locked`:** accent decided; design prompt names no real person; lineup test passed, also through each relay; delivery states listed with start lines; 10–30 s reference samples saved; source `designed`/`prebuilt`, or consent record and vendor verification present; provider, model version and settings recorded.
- **Each line, before `picked_take`:** `line_text` exact and `tts_text` same words; paths treated as paths; "(beat)" split; 3 takes (2 × 3 for marked lines); transcripts match; length within ±20% of plan; Saye: no contractions except "They're here." (SC24).
- **Each scene, before picture lock:** off-screen rule applied first; sync checked at half speed on every visible mouth; room tone continuous; presets applied per `listen_from`; pauses match A1's ranking.
- **Release:** D4 credit line; watermarks kept; consent records offline, scope respected; dialogue stem exported; loudness per A4; TTS licence covers film.
- **Failure signs** [§13]: drift → regenerate the scene on locked settings; spoken tags → Robust, fewer tags; relay pasted on → listener's room reverb after the chain; wrong face moves → mask, or a silent listener clip (A4 AI7).

## 6. Saying it to AI models

- **ElevenLabs v3:** one or two tags before the words (`[whispers] Iona?`); pauses by ellipses and dashes; IPA in slashes; speed 0.7–1.2. Documented tags include `[whispers]`, `[sighs]`, `[exhales]`, `[laughs]`, `[crying]`, `[strong X accent]`, `[sings]`; test others per voice.
- **Gemini 3.8 Flash TTS:** a short `style` per turn, not long "Director's Notes" (which "are the most common cause of voice drift"); inline `<breath>`, `<sigh>`, `<short pause>`, `<long pause>`, `<laugh>`, `<gasp>`; at most 2 speakers per request.
- **Others:** OpenAI `instructions` (voices `marin`, `cedar`); Hume `description` and `speed` 0.5–2.0; Chatterbox `exaggeration` 0.7+, `cfg_weight` ~0.3; Dia `[S1]`/`[S2]` and `(laughs)`.
- **Playable action → delivery string** [§5.2]: to warn = "low, firm, urgent, falling ends" (Natural, 1.0); to press = "level, quiet, unhurried, no rise" (Robust, 0.95); to soothe = "soft, warm, slower" (Natural, 0.9); to dismiss = "flat, quick, clipped" (Robust, 1.1); to plead = "breathy, rising, uneven" (Creative, 0.95).
- **Design prompts:** 30–50 words, fixed order (age and sex, pitch and texture, `{accent}`, delivery, "close, clean studio recording"), never a real name.
- **Native-audio drafts only:** name the path in the same sentence and say "is not visible" (C3 R21): "Jude's voice, heard only in her earpiece, crackly; he is not visible". Listener clips: small timed actions with the lips closed ("her lips closed; she breathes in; she blinks"), no quoted dialogue (A4 AI7, read through errata 27).
- **To the LLM:** use P4's prompt verbatim; never ask it to paraphrase a line "for the voice".

## 7. The Catch

**Decisions made** [§4.2, §5.1, §11]:
- Counts (rechecked against the script): 221 cues, five speakers (Iona 95, Saye 62, Eli 39, Jude 17, Nell 8, extensions included), 1,579 spoken words, 7,666 characters; guard, nurse and technician never speak. Budget ≈ 26,000 characters with takes and alternates.
- Five voices (proposals; design prompts verbatim in §4.2): IONA late 30s, low-mid, dry husky, 2.6 w/s, states *work*, *cracked* (SC10, SC13), *helmet* (SC23–28), *level* (SC29–30); JUDE mid 40s, low, warm gravelly, 2.4 w/s, *easy*, *wounded* (from SC06), *whisper* (SC15); ELI early 30s, mid, thin clear, 2.2 w/s plus ~1 s silent lead-in, *counting*, *open* (SC23, SC29); SAYE late 50s, mid, crisp, formal, 2.0 w/s, *answers voice*, *lost answers voice* (SC24), *softened* (SC28 "Yes, Nell."); NELL older than 60, mid-high, papery, 1.9 w/s.
- The 18 parentheticals: 7 "(beat)" (Eli ×3, Iona ×2, Saye ×2); 4 paths ("(in her ear)" l.94, "(from the back)" l.352, "(over the radio)" l.1214, "(into her helmet)" l.1610); 2 actions (l.620, l.1148); 5 delivery ("(through the torch)", "(quite softly)", "(not steady)", "(quietly)", "(a whisper)"). Whisper and torch lines go by STS.
- SC10 "(not steady) Not mint." (l.461–463): `VOICE-IONA.D02`, planned 1.3 s; alternates `[quietly] Not... mint.` (Natural, 0.9), `[exhales] Not mint.` (Creative, 0.95), STS with a mint leaf in the mouth; audio-reference sync, sync-3 fallback (≈ $0.53).
- SC13 "One body." / "One." / "You.": one two-voice call from "What was it rated for?", cut by timestamps; 3 s hold on "She waits."; Eli off screen; ~1 s silence before "You." with a cut-in on Iona; "Silence." held ≥3 s, room tone and monitor hum, no music.
- Jude in her ear is SC02 (l.93–95) and SC04 (l.176–177), not SC01: earpiece preset, mono, no shaft reverb; "(through the torch) No." is `direct`, STS with a pencil in the teeth, no lip sync.
- SAYE (RECORDED) SC23/SC24: identical chain (recording → wrist → inside the helmet) so we hear Saye change, not the device; D01 Robust 0.9, D02 Creative 1.0 or STS; the 29-word part before "(beat)" runs ≈ 14.5 s; her face is a separate lip-synced clip composited on the display.
- Visor: `helmet_internal` on Iona's side, `radio` from Eli's (l.1120), crossfaded at cuts; no sync through the visor.
- *The Long Places* ch. XI: Melek's song is `tape` in the stone room; the returned phrase (l.1027) is `unsourced_room`, no tape chain, Robust, no tags.

**Flagged for the user**:
- Country, period and accent (blocks locking; D17 default option A is a British regional set).
- Whether Nell shares the accent; whether the helmet is on in SC18–22 (B5 costume phase C4 says SC18–27) and whether the suit has an external speaker in SC28.
- Whether the torch is still in Iona's teeth for "It was my tooth." (l.104) after "Spits into the dark." (l.101).
- The glass world rule (intercom for speech, or no speech through glass).
- Whether any voice will be the user's own clone (`voice_policy`).
- Singing (Melek) is weak in TTS: a consenting singer or a music model.

## 8. Conflicts and open questions

- **Blueprint naming** (§10.5): the blueprint uses `VO-` voice IDs, SPEECH records, VOICETAKE `VT-SC10-D11-T01`, `RT-` consent IDs, paths `helmet_inside`/`helmet_outside` plus `phone` and `thought`, and no YAML. The blueprint wins; D3's `tape`, `unsourced_room` and `prebuilt` are proposals to add.
- **ID clash fixed:** path presets were `FX-RADIO-01`, but blueprint `FX-` means finishing jobs; renamed `PRESET-...`. Still to merge with D9's presets; D9's `earpiece_radio` (3 kHz low-pass) merges two paths D3 keeps apart.
- **D15** `voice_ref` uses `VOICE-IONA.D02`: move to `VO-`. **D17**: locale lives in `WORLD.accents`, not a `WR-` rule (D3 updated). **D4**: `likeness_basis` values and its credit template govern; D4 has Denmark "Proposed 2025", D3 records unconfirmed 2026 dates. **C3** gives everyone a British voice; D3 keeps `{accent}` open. **A2** `speech_profile.voice` means grammar: rename `grammatical_voice`.
- **Corrected at fact-check:** Hume commercial only from Creator ($7); Dubbing Studio is Creator+; Switzerland dropped from Gemini's reported blocks; Dia English only; EU Art. 50(2) grace to 2 Dec 2026; NY exemptions; NO FAKES not passed [U].
- **Open [U]:** ElevenLabs' short-prompt advice; Cartesia speed/volume; Gemini region blocks; Netflix −27 LKFS; Denmark's start date; whether TTS licences cover film (D9 found ElevenLabs Music self-serve excludes film); visors in lip-sync tools.
- **Lineup arithmetic:** all five share accent A, so every pair starts one column down; Saye (2.0) and Nell (1.9) nearly share pace. Test Saye–Nell and Iona–Saye first.

## 9. Section map

- **§0** labels, terms • **§1** eight principles • **§2A** TTS, design, cloning, STS tools • **§2B** lip-sync tools • **§3** 27 rules • **§4** VOICE template, five Catch voices, lineup test, no-code design recipe • **§5** parentheticals, playable actions, take policy, scene recipe • **§6** law table, consent record, clone recipe • **§7** lip-sync cases and recipe • **§8** path chains, glass rule, tested ffmpeg strings • **§9** dialogue edit • **§10** fields, old names, blueprint alignment • **§11** worked examples (SC10, SC13, SC02/04, SC23/24, visor, *Long Places*) • **§12** routes and costs • **§13** failures • **§14** checklists • **§15** open questions • **Sources** S1–S47.
