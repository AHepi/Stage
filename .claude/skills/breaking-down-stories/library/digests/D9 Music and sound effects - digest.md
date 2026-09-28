# Digest D9: Music and sound effects for AI films (27 Sept 2026)

Source: `research/D9_music_and_sfx.md` (581 lines; two fact-check passes 27 Sept 2026, 25+ pages re-fetched, all script quotations verbatim). Refs: §3 rule n = decision rule; §1.n = principle; §4.n = procedure. **[V]** official page read; **[V-sec]** secondary; **[U]** unverified; **[J]** judgment. Re-check tool facts before paying. Record names follow `design/blueprint.md`. Terms [§0]: *spotting* = deciding where each cue starts and stops; *V2A* = video-to-audio (a model makes sounds timed to a silent clip); *master* = the one recording every use copies; *preset* = a named processing chain (filter, reverb); *sound emphasis* 0-3 = bed, clear, foreground, alone (B4); *bar line* = start of a bar (every 240 ÷ BPM s in 4/4).

## 1. Scope

1. Dated landscape of music generators (Suno v6, ElevenLabs Music, Lyria, Stable Audio 3.0, Firefly, ACE-Step 1.5; Udio walled off), text-to-SFX and V2A models, and libraries, with the licence terms that decide film use.
2. Procedures a non-musician runs with an LLM: policy, spotting, cue prompts, temp and re-spot, a theme without drift, motif masters and presets, effects, V2A checks, foley, licence log.
3. Worked on *The Catch* (policy, pump, CLICK/CLACK, hum, effects, foley) and *The Long Places* (drill, knock, lullaby).

## 2. Rules

**Policy**
1. [§1.1, C3 R10] If a generated clip has music, then strip it and prompt "No background music.", because model music restarts at every cut [J].
2. [§1.4, §4.1] If no `music_policy` is set, then generate no cue, because only the user sets it, once, at checkpoint B.
3. [§3 rule 1] If neither the text nor the director gives a reason for score, then set `none`, because "music tells the audience how to read faces" (A4 SND5) and an unscored film keeps its ruptures clean [J].
4. [§3 rule 2] If characters hear the music, then it is `source` music, made as a sound in the scene with a perspective preset, because it obeys the story's space [J].
5. [§3 rule 3] If the policy is `sparse`, then at most three cues under about 40 minutes (longer: agree `cue_budget`), each at a paragraph break, never under an open reveal, because each cue cheapens the others [J].
6. [§3 rule 4] If the policy is `none`, then a drone or tonal bed is allowed only when a source in the world makes it (hum, motor, room resonance), because an unmotivated drone is score by another name [J].
7. [§3 rule 4a] If the text names a device that could play music but does not say it does (SC02 "Behind one, a radio, far off."), then give it murmured speech, never a recognizable tune, and list it for the user, because radio music is source music needing a licence [J].
8. [§3 rule 4b] If the policy is `end_credits_only`, then the credits cue enters only after the last motif statement has ended or receded, because B4 M10 says of the pump "Never put score over it" and A4 SND8 forbids cutting it mid-pattern [J].

**Tools and rights**
9. [§3 rule 5] If the film goes to festivals, streaming or broadcast, then use only a plan whose terms cover it (Suno Pro/Premier, downloaded while subscribed; paid Lyria API; Stable Audio; ACE-Step; Firefly after reading the plan; ElevenLabs only on full Enterprise Music, not Lite), never a free tier, because Suno trial downloads are "not eligible for commercial use" and ElevenLabs below Enterprise Music excludes "film, TV, radio, & Studio Games" [V]; Google's and Stability's fit is read from ownership clauses [J; D4].
10. [§3 rule 5, §2.1] If a help page and the dated terms disagree (ElevenLabs docs claim film clearance), then follow the terms, because they are the contract [V; J].
11. [§3 rule 5a] If a cue is AI-generated, then never register it with Content ID or claim exclusivity, because Google and ElevenLabs both say others may get the same or similar output [V].
12. [§3 rule 5b] If you send storyboard frames or scene text to Lyria through the Gemini API, then use a paid key, because Google uses unpaid submissions to improve its products and not paid ones [V].
13. [§3 rule 6] If tempo and key must be exact, then use ACE-Step, Lyria RealTime or Suno Studio's Manual BPM, because only they expose tempo (and key) as settings [V].
14. [§3 rule 8] If a tool or tier cannot export for commercial use (Udio, downloads "disabled" since 29 Oct 2025; Suno Free), then keep it off the timeline, because you cannot clear what you cannot download [V].
15. [§3 rule 19] If a sound is CC BY-NC, then keep it out of anything sold, monetized or entered where fees or prizes apply, because Freesound says "you can't earn any money with the piece of work you create" [V; festivals J, D4]. If a file is ND and you will process it, then reject it (D4 rule 15).
16. [§3 rule 20] If music or effects are AI-made, then log tool, version, plan and date, keep watermarks (SynthID) and extend D4's one credit line, because prompts alone give no authorship (US Copyright Office, 29 Jan 2025) [V].
17. [§3 rule 17] If using an open V2A model, then follow the weights' licence, not the host's label, because MMAudio's weights are CC BY-NC 4.0 while fal says "Commercial use permitted" [V].
18. [§3 rule 18] If you live or distribute in the EU, UK or South Korea, then do not use HunyuanVideo-Foley, because its licence "DOES NOT APPLY" there [V; distribution J].

**Timing**
19. [§3 rule 9] If a cue has hit points (picture moments it must land on), then BPM = 60 × beats ÷ seconds between hits; at 24 fps one beat = 1440 ÷ BPM frames, because beats on cuts feel composed for picture [J].
20. [§3 rule 10] If generating a cue, then ask for 4 s more than the spot and a clean decaying tail, because music needs handles [J; A4 R2].
21. [§4.3 length per tool] If the tool's minimum is longer than the cue (Lyria 3 Clip is always 30 s; ACE-Step starts at 10 s; ElevenLabs 3 s), then generate longer, with the ending inside the first `length_s + 4` s, and trim on a bar line [V lengths; J].
22. [§3 rule 11] If picture changes after a cue is made, then first cut on bar lines before regenerating, because a bar-line cut is inaudible and keeps the approved take [J].
23. [§1.5, §4.4] If making finals, then spot on the animatic with temp and again after lock (and after any later change), because downstream files "drift silently" (D8-R7).

**Motifs, themes and effects**
24. [§3 rule 7, §4.5] If a theme must return, then make one master in one tool and make variations by processing its stems, because text-only regeneration gives a new tune each call [V].
25. [§3 rule 12, §1.2-1.3] If a sound recurs in the text, then build one dry master, write its signature in frames, make every appearance a processed copy, and mute generated occurrences, because native audio rarely repeats a rhythm exactly (B4 §14.2).
26. [§3 rule 12a] If an effect is heard through a device that also carries voices, then use D3 §8.1's chain of the same name, because the audience hears one speaker (SC15: Jude's whisper and the pump share the tablet) [J].
27. [§3 rules 13-14] If an effect is ordinary (door, gunshot, alarm), then use a library first (Sonniss, Freesound CC0/CC BY); if it exists nowhere (the engine, the figure's jet), then make it once as a master, because recordings are exact and cleared and regeneration drifts [J].
28. [§3 rule 15] If a silent-model shot has many small actions, then try V2A first, check it (P7), and replace key sounds by hand, because V2A invents "speech-like sounds" and "background music" [V].
29. [§3 rule 16] If hands, cloth or breath must be felt, then record foley at home, because models make them poorly and they are easy to perform [J].
30. [§4.5 step 4] If someone who heard the master once cannot hum along with a variation, then reject it [J].
31. [§4.9] If a file enters the project, then log its licence that moment and, before export, list every item not `yes` for `commercial_ok` or `film_ok`, because takedowns come from unlogged items.
32. [§4.7] If the script has a capitalised sound word (GUNSHOT, ALARM), then give it an `effect`, room sound or motif appearance in its scene, because blueprint check COVER-07 errors otherwise.

## 3. Breakdown fields

| level | field_name | meaning | allowed values / example |
|---|---|---|---|
| film (`SOUNDPLAN`) | `music_policy` | music rule (user) | `none` `source_only` `sparse` `scored`; proposed `end_credits_only` |
| film | `cue_budget` | most cues allowed | integer; `sparse` ≤ 3 under about 40 min [J] |
| film | `tonal_centre` | home note for cues and beds | `a` or `none` |
| film | `presets[]` | named processing chains; device ones shared with D3 | the eleven names in P6's table |
| film | `source_devices[]` | devices that could play music | `{scene, exact_text, plays}`; plays `speech_murmur`, a `MU-` ID, `none` |
| film | `theme_register[]` | each theme's master | `{theme_id: TH-01, master_file, bpm, key, bars, allowed_variations}` |
| cue (blueprint `MUSIC`) | `cue_id`, `in`, `out`, `must_not`, `bpm`, `key`, `length_s`, `hit_points[]`, `temp_file`, `final_file` | one spotted cue | `MU-01`; in: first black frame after "Nobody leave this room." |
| cue | `function` | what it does | `title` `transition` `montage_pace` `counterpoint` `tension` `release` `end_credits` `source` |
| cue | `source` | origin (blueprint: `score` `library` `ai`) | `generated` `library` `composed` `performed` |
| cue | `theme_id`, `variation` | link to a theme master | `TH-01`; `full` `fragment` `solo_line` `slowed` `transposed` `filtered` `none` |
| cue | `status` | progress | `spotted` `temp` `generated` `approved` `locked` `cut` |
| asset (`SOUND`, proposal) | `id`, `kind` | the sound and type | `MO-PUMP`, `SFX-ENGINE-L`, `AMB-HUM`; `bed` `motif` `sfx` `foley` `music_cue` |
| asset | `signature` | fixed pattern | "11 f, 14 f, 29 f rest" |
| asset | `master_file`, `states[]` | the master; source states | path; `{state_id: AMB-HUM.S03, description}` |
| asset | `source` | how it was made | `record` `library` `ai_sfx` `ai_music` `v2a` `native` |
| asset | `tool`, `tool_version`, `plan`, `made_on`, `downloaded_on`, `licence`, `licence_url`, `attribution_text`, `terms_file` | provenance, terms | dates; `cc0` `cc_by` `cc_by_nc` `royalty_free` `plan_terms` `open_weights` `own_recording` `unknown` |
| asset | `commercial_ok`, `film_ok` | cleared for sale / film | `yes` `no` `check` |
| asset | `ai_generated`, `must_not` | disclosure; plant rule | `yes` `no`; "no bounce, no roll" |
| asset → blueprint | `RIGHTS` | licence copied to a rights record | `RT-001`, `subject: music` / `stock` / `model_terms` |
| shot (blueprint `sound` → `effect`) | `effect` items = A4 `sync_fx` | a sound tied to an action | `<what> \| at: <seconds> \| sound_emphasis: 0-3` |
| shot | `effect.source` (proposal) | origin of each synced effect | `native` `library` `ai_sfx` `v2a` `foley` `record` |
| shot | `sound.motif` (= blueprint `MOTIF` appearance) | a motif copy here | `{id: MO-PUMP, preset: through_suit, sound_emphasis: 2, sync_to: none}` |
| shot | `sound.v2a_check` (proposal) | P7 result | `pass` `fail` `not_run` |

## 4. Procedures

**P1. Set the music policy** [§4.1] (checkpoint B, 5 min).
1. The LLM reads A4's ruptures, B4's sound motifs and every sound mark, and writes one paragraph each for `none`, `sparse` (naming 1-3 places), `end_credits_only`, `scored` (plus `source_only` if characters hear music), naming what music would compete with.
2. It lists every device that could play music and what each plays.
3. You answer with one word; the LLM writes `SOUNDPLAN.music_policy`.

Say: *"Using D9 §4.1, write the music-policy options for this film against A4's rupture list and B4's sound motifs. One paragraph each, then list every device in the text that could play music. Stop and wait for my one-word answer."*

**P2. Spot the cues** [§4.2] (per sequence, 10 min).
1. Candidates by A4 §7.6: enter on a motion or cut; exit before or on a rupture; none under open reveals.
2. One row each: `cue_id`, `in`, `out`, `function`, `must_not`, `hit_points`, `length_s`; delete the weakest until within `cue_budget`.
3. You mark keep or cut; a cue survives only if its function fits in five words.

Say: *"Spot cues for SC10 to SC11 under policy sparse, cue budget 1, using D9 §4.2. One spotting-sheet row per candidate with every §5 field; weakest first if you must cut."*

**P3. Cue to prompt** [§4.3]. Template, exactly:
```
Instrumental only, no vocals. About <length_s + 4> seconds.
Tempo <BPM> BPM, steady, no tempo changes. Key: <key>.
Instruments: <two to four, plainly named>.
Shape: [0:00-0:<a>] <quiet start>; [0:<a>-0:<b>] <development>; [0:<b>-end] <ending: one sustained note that decays naturally over 3 seconds>.
Texture: <sparse | medium>; no drums <if wanted>; no sound effects.
```
Per tool: see §6. Make three takes; keep the one that fits the hit points on the animatic, not the one that sounds best alone.

**P4. Temp, then re-spot** [§4.4].
1. Temp only from music you already hold a licence for; name files `TEMP_`; never temp with commercial film scores.
2. Watch with no music, then with temp; cut any cue that tells you what to feel before the face does.
3. Before replacing a temp, rewrite `function` and `must_not` from scratch and prompt from those words.
4. After lock: the LLM recomputes in, out, length, hit points and BPM; cues changed by under a bar are cut on bar lines; the rest are regenerated or remade from the theme master.
5. `status: locked` when it plays on the locked cut, tail intact; repeat step 4 after any post-lock change.

Say: *"Here is the locked cut's shot list with times. Using D9 §4.4 step 4 and rules 9 to 11, recompute every cue's in, out, length, hit points and BPM. For each cue say: keep, cut on bar lines (give the cut times), or regenerate."*

**P5. Theme without drift** [§4.5].
1. Generate one 20-40 s instrumental theme at fixed BPM and key; split stems; save `TH-01_master.wav`; write BPM, key, melody instrument, bar count.
2. Variations by processing: `fragment` (first two bars), `solo_line` (melody stem), `slowed` (Audacity Change Tempo, at most about 15%), `transposed` (Change Pitch, 2-5 semitones), `filtered` (a preset).
3. Only if processing fails: feed the master to ElevenLabs Audio Reference, ACE-Step cover or repaint, or Suno extend or remix.
4. Hum test (rule 30). 5. The LLM refuses any cue with a `theme_id` not made from the master.

**P6. Sound-motif master and presets** [§4.6].
1. Get the raw sound once (record 20 takes, cleared library, or ElevenLabs SFX / Stable Audio Small SFX); choose one.
2. Build the signature on exact frame counts at 24 fps in Audacity or Resolve Fairlight.
3. Save dry, 48 kHz WAV; write the signature.
4. Define presets once (starting values [J]; device rows are D3 §8.1's):

| Preset | Processing | Use |
|---|---|---|
| `dry_close` | none | on-screen, close |
| `room` | Reverb sized to the location | in the room |
| `off_screen` | slightly more reverb, 1-3 dB lower | unseen, same room |
| `device_speaker` | High-Pass 500 Hz, Low-Pass 5 kHz, slight Distortion | tablet, wrist, monitor |
| `earpiece` | HP 400 Hz, LP 3.4 kHz, light saturation, gentle compression | earpiece |
| `radio` | band 300-3,400 Hz, more saturation, peak near 1.8 kHz | radio |
| `through_glass` | LP 1-1.5 kHz, 12 dB down | quarantine glass (SC11-13, SC17, SC29, SC30) |
| `through_wall` | LP 800 Hz | next room |
| `through_suit` | LP 1 kHz, bass boost, very short small reverb | outside sound felt inside a suit |
| `far_below` | LP 2 kHz, quieter, long thin Echo | shaft, borehole, distant above |
| `over_black` | the scene's last preset, room bed faded out | after cut to black |

5. Place copies; never edit the master; set level in the mix.

Say: *"Using D9 §4.6, write each preset in `SOUNDPLAN.presets` as numbered Audacity steps a beginner can follow, with the menu name of every effect and its values, and as one ffmpeg command. Reuse D3's chain wherever the name matches."*

**P7. Effects: library, generation, V2A, foley** [§4.7].
1. List every `sync_fx` (`effect`), `offscreen` item and capitalised sound word. 2. Sort: ordinary → library; invented → generated master; hands, cloth, breath → foley.
3. Library: three search words each; filter Freesound to CC0 or CC BY; log the credit line on download.
4. Foley: phone in a closet or under a duvet, 30 cm away, five takes per action while watching the clip; name by shot (`CATCH_SC30_SH050_cloth-fold_FOLEY-T03.wav`); slide each transient (the sound's sharp first instant) onto its contact frame.
5. V2A check, fail on any line: every `sync_fx` present; each within 2 frames of its cause (zoom to single frames, park on the contact frame: does the waveform start there?); no music or murmur; nothing where nothing happens; nothing revealing a `withholds` item.
6. Never keep a generated motif occurrence.

Say: *"Using D9 §4.7, list every sync_fx and offscreen item in SC25 to SC30, sort each into library, generated master, or foley, and give three Freesound search words for each library item."*

**P8. No score, still tense** [§4.8]: pace from a rhythmic world source; waits from unseen approaching sounds; turns from a constant sound stopping; release from an ordinary bed returning; drones only with a source.

**P9. Licence log and credits** [§4.9]. Freesound's sentences, exactly: "This [video/theatre piece/...] uses these sounds from freesound: 'sound1' by user1 (http://freesound.org/s/soundID/) licensed under [licence]", or "This [video/theatre piece/...] uses many sounds from freesound, for the full list see here: [link]". Add "music generated with [tool]" or "music by [composer]" to D4's single credit line; never a second AI line. Keep dated terms pages in `rights/`; for Suno, record plan and download date.

## 5. Checklists

**Spotting sheet**: within policy and budget? Enters on a motion or cut, leaves before or on a rupture? Nothing under an open reveal, an emphasis-3 motif or a written silence? Five-word function and a `must_not`? BPM, hit points, 4 s extra? Shared `tonal_centre`?

**Generated cue**: instrumental, no murmurs? Tempo steady? Clean tail? Hum test if themed? Tool, plan, licence, `terms_file` logged; plan covers film (terms, not help pages); Suno downloaded while subscribed?

**Motif asset**: one dry 48 kHz master, signature in frames? Every occurrence from the master with a named preset? Emphasis 3 once per motif (B4 §3.4)? Never cut mid-pattern at the end (A4 SND8)?

**Effects and V2A**: every `sync_fx` and capitalised sound word sourced? V2A passed all five checks? Device effects on that device's D3 chain? Every radio or speaker in `source_devices[]`? No CC BY-NC, edited ND, RemArc (BBC) or free-tier item in a commercial or festival cut? Every CC BY credit on the end card?

**Failure signs** [§7]: theme differs (remake from master); cue drifts off cuts (Manual BPM); cue sour against the hum (`tonal_centre`); pump rhythm changes (lay the master); V2A murmur (replace); sting on a reveal (remove, B4 rule 23); Content ID claim (never register AI cues); tablet voice and effect differ (one D3 chain).

## 6. Saying it to AI models

- **Video clips**: "No background music." Native effects are drafts, 0.2-0.44 s off (C3 §7D).
- **Music prompts**: describe sound, not feelings; no artist, song, album, film, publisher or label names, no lyrics (ElevenLabs terms forbid them; Lyria blocks artist voices and copyrighted lyrics) [V]; at most three texture words.
- **Lyria 3.5** (`lyria-3.5`, $0.08 a song, no free tier): paste the P3 template and state the length; Google advises "Mention instruments, BPM, key, mood, and structure" and timestamps `[0:00 - 0:10]`; no iterative editing [V]. Lyria 3 Clip ($0.04, exactly 30 s) is now "Legacy".
- **Lyria RealTime** (`lyria-realtime-exp`): numbers for `bpm` (60-200), `scale` (12 values), `density`, `brightness`; text only for instruments and mood; record the stream [V].
- **ElevenLabs Music**: 3 s to 5 min, set in the length control; Audio Reference (about 30 s) guides style, "not a remixing or genre-transfer tool"; inpainting redoes one section [V].
- **Suno v6** (Pro/Premier; v6-mini free): style words in the style field, instrumental switch (UI names [U]); Studio (Premier) "Manual BPM" for "a consistent tempo" [V].
- **ACE-Step 1.5** (MIT, local): BPM, key, time signature in fields, shape in text; 10 s to 10 min; runs under 6 GB VRAM with the language model off [V].
- **Text-to-SFX (ElevenLabs)**: up to 30 s, 40 credits a second; "prompt influence" high for literal sounds; looping mode for beds [V].
- **V2A**: MMAudio is trained at 8 s and fails on unfamiliar concepts ("'gunfires' but not 'RPG firing'") [V]. For refusals on violent words: say once it is pre-production and use "gunshot sound effect" (blueprint §13.6).

## 7. The Catch

**Decisions made (proposals for checkpoint B)**
- Policy: `none` recommended (A4 §15 "none or very sparse"; blueprint K31 default none); the user decides. `sparse` = one title cue `MU-01` from the black after "Nobody leave this room." under "= THE CATCH", out on the cut into SC11 before dialogue, 60 BPM, low bowed strings and one piano note, in the hum's key, 6 s + 4 s handles. `end_credits_only` only if the pump recedes first.
- SC02 "Behind one, a radio, far off.": murmured speech, not music. The SC18-21 radios are two-way voice radios (D3 `radio`), not music sources.
- Pump `MO-PUMP` (B4 M10): stroke, 11 f, stroke, 14 f, stroke, 29 f rest (54 f = 2.25 s). Master: a hand-squeezed rubber bulb in a sink [J], third stroke softer, dry. SC15 ("(ON THE TABLET)") `device_speaker`, S1; SC16 `off_screen`, S2, J-cut; SC20-24 optional, S0 or omitted (default omitted [J]); SC25 `room`, synced to the flap, S1; SC27 `through_suit`, S2; SC28 `room`, S1; SC30 `room` plus `SFX-VESSEL-TAP`, S2, until "The tapping stops."; over black "Three uneven strokes in the dark." S3 once, the cut falling in the 29-frame rest.
- Engine `SFX-ENGINE` (S/M/L from one latch recording): written only at SC06 "A hard metal CLACK." (L, on the first of 10 black frames, then true silence) and SC15 "A small CLICK, from nowhere." (S, `device_speaker`). Added per A4 WE3 [J]: SC12 (S, `through_glass`), SC18 pod (S twice), SC23 (M), SC24 "She fires." (L, then the hum's missed beat), SC27 (L, `through_suit`).
- Hum `AMB-HUM`, states of one master: SC19 "A low HUM comes up through them." S01; SC21 S01; SC23 "The hum under the floor wavers." S02; SC24 "The hum misses a beat." S03 (12 frames cut out); SC26 "The sick motor through them." / "Then not." S04, then stop: the sound rupture (blueprint K12).
- Scripted effects, sorted [J]: SC02 rung "TURNS" (library/record); SC04 "A GUNSHOT." (library, `off_screen`); SC06 "KICKS" and "FIRES" (library, distant), "STOPS DEAD" and "METAL SHRIEK" (layered library); SC16 "WHITE JET" (a stored master: the figure's body); SC16 "An ALARM" (library, `through_wall`).
- Foley: SC06 palm on steel (a steel tray); SC11 wrist band (cable tie); SC25 repair tape; SC27 glove creak (then `through_suit`); SC30 cloth fold, and a jar set on a towel, which removes the tap.

**Flagged for the user**: music policy; the hum's note (`tonal_centre`); the SC02 radio and the unwritten engine sounds (SC12, SC18, SC23, SC24); pump under SC20-24; pump under the credits or receding (A4 §15 Q2); Iona's helmet in SC19 (B5 says on from SC18; confirm); one paid music plan; festival or online release; a 6 GB+ graphics card.

## 8. Conflicts and open questions

- **Blueprint names** (resolved): `SOUNDPLAN`, `MU-`, `RIGHTS`; effects `SFX-` (blueprint `FX-` = finishing jobs). Proposals: `SFX-`, `AMB-`, `TH-`, a `SOUND` asset record, `end_credits_only`, `MUSIC` under `source_only` with `source: performed` (the lullaby).
- **Shot effect field**: A4 `sync_fx` = blueprint `sound` → `effect` items; D9 proposes adding `source` and `v2a_check` to them.
- **Music policy**: A4's `score`/`source only` → blueprint `scored`/`source_only`; default `none` agrees with blueprint K31; the user decides.
- **Presets vs D3**: D9 uses D3's device names and values; `through_suit` is new, not blueprint `helmet_inside` (the wearer's own voice). **Stale in D3**: D3 §10.5 and its digest still cite D9's old `earpiece_radio`, `small_speaker`; D3's glass list omits SC30.
- **Licence vocabulary**: D9 `cc_by` etc. vs D4 `cc_by_4_0` etc., and different `source` lists; open (D4 proposes one list in `RIGHTS`, short names plus version suffix).
- **ElevenLabs Music**: docs page claims film clearance; terms exclude film below Enterprise Music; terms win (D13 R19 agrees).
- **Blueprint §13.6** calls the gunfire "SC06's gunshot"; the GUNSHOT is SC04 (l.172), SC06 has "FIRES" (l.216).
- **Motif count**: A4 WE3 calls pump, CLICK/CLACK and HUM motifs; B4 counts only M10; D9 files the others as `SFX-`/`AMB-` [J]. Pump signature: D9's frames replace A4's seconds.
- **Runtime**: A3 about 40 min vs C1's 20 (D13); V2A costs about $11 per 20 min per sample (Sonilo).
- **Lullaby region**: the book names none; D17 decides.
- **[U]**: Suno length, key control, UI names; Lyria RealTime price; ElevenLabs stem options, SFX film terms; Firefly plans; Sonilo/Mirelo lengths; fal's MMAudio licence; YouTube Audio Library off YouTube; RemArc primary page; ACE-Step training data, "extend"; Udio relaunch.

## 9. Section map

| D9 section | Lines | Contents |
|---|---|---|
| §0 Words | 20-57 | definitions |
| §1 Principles | 58-70 | eight principles |
| §2 Landscape | 71-119 | music tools, SFX, V2A, libraries |
| §3 Rules | 120-158 | 1-20 plus 4a, 4b, 5a, 5b, 12a |
| §4.1-4.3 | 159-207 | policy; spotting; prompt template; length per tool |
| §4.4-4.6 | 208-256 | temp and re-spot; theme; motif master and presets |
| §4.7 | 257-299 | effects, scripted sounds, foley, V2A check |
| §4.8-4.9 | 300-324 | no score; licence log and credits |
| §5 Fields | 325-358 | fields, blueprint mapping |
| §6-7 | 359-413 | checklists; failure modes |
| §8.1-8.3 | 414-487 | *The Catch*: policy, hum, pump, engine |
| §8.4 | 488-504 | *The Long Places*: drill, knock, lullaby |
| §9-10 | 505-541 | open questions; conflicts |
| Sources | 542-581 | S1-S35, library |
