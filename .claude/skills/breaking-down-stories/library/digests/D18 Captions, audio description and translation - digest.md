# Digest D18: Accessibility and localisation (28 Sept 2026)

Source: `research/D18_accessibility_localization.md` (fact-checked 28 Sept 2026). Brackets: R*n* = D18-R*n* in §4; Rec*n* = Recipe *n* in §5; other § = section. **[V]** primary page read 27–28 Sept 2026; **[U]** unverified; **[J]** judgment. Re-check platform and tool facts after 28 Oct 2026.

## 1. Scope

1. Plans SDH captions, audio description (AD), a descriptive transcript, colour-blind and flash safety inside the breakdown, before generation, so nothing inaccessible is baked into the picture.
2. Makes foreign-language versions: an annotated English template, translated subtitles, forced narratives (FN), per-line AI dubs from D3's voice files, and translated insert graphics from C2 R6 SVGs.
3. Adds `access`, `ad_*`, `on_screen_text`, `language_plan` and dub fields; worked on *The Catch* (SC06 CLACK, SC10 "Not mint.", SC28 RECEIVING) and *The Long Places* (chapters V, VII, XI).

## 2. Rules

**Planning** [§4 A; §2]
1. [R1] If the film will be public, then plan English SDH, an AD script and a descriptive transcript, because all three come cheaply from the breakdown; only AD written late is expensive [J].
2. [R2] If a story fact travels by one channel only (picture, sound or colour), then add a second channel or plan the AD/SDH line that carries it, because each audience loses one channel [J].
3. [R3] If a shot has `withhold` (C5), then AD and SDH state only what the frame shows, because naming the hidden thing spoils the payoff for those who most depend on description [J].
4. [R4] If A4 marks true silence, a listening hold or a rupture, then set `protect_silence: yes`, because Netflix interrupts "intentional silence" only "for vital, timely information" and DCMP says "Do not try to fill every pause" [V].

**SDH** (extends D8-R50 to R54) [§4 B]
5. [R5] If the absence of a sound plants a payoff, then label it once, neutrally (`[no sound of it landing]`), because deaf viewers cannot notice an absence [J].
6. [R6] If a sound stopping is the event, then label the stop (`[hum stops]`), because the BBC labels sounds "not obvious from the action" [V].
7. [R7] If a motif has a pattern the payoff needs, then put it in the fixed `sdh_label` (`[three uneven pump strokes]`), because recognition depends on it; D8 has adopted this default [J].
8. [R8] If a sound's source is withheld, then label the sound, not the source, because the BBC says "Describe sounds, not actions" and the source is story [V/J].

**Audio description** [§4 C]
9. [R9] If choosing what to describe, then rank (1) facts a payoff needs, (2) actions that contradict or complete dialogue, (3) setting and identity, (4) texture, and fill in that order, because gaps are short [J].
10. [R10] If a shot has `behavior` steps (D15), then write AD from them and use `purpose` only to rank, because `behavior` is observable [J].
11. [R11] If writing an AD line, then allow 2.5 words per second of gap and end 0.3 s before the next line or key sound, because Netflix calls description over dialogue "a last resort" [V].
12. [R12] If a gap is too short for a rank-1 fact, then pre-describe it in the nearest earlier gap, because Netflix allows it "when there is no other way" [V].
13. [R13] If a visual motif recurs, then fix one wording in `ad_words` and reuse it verbatim, taking the script's phrase when objective [J].
14. [R14] If on-screen text is plot-pertinent, then AD reads it verbatim and says "backwards" when mirrored, because DCMP asks to "establish a pattern of on-screen words being read" [V].
15. [R15] If the mix is sparse with no music, then dip 6 dB (not 12) with about 0.3 s ramps, because a deep dip makes the room vanish (Netflix allows 6–12 dB) [J/V].
16. [R16] If AD needs a voice, then design one narrator `VOICE-AD` unlike every character in D3's lineup check, because blind viewers must never mistake it for a character [J].
17. [R17] If the platform has no AD track, then deliver a titled open-AD copy and prefer tightening the edit over extended AD, because extended AD (WCAG 1.2.7, AAA) works only in some players [J].

**Translation** [§4 D]
18. [R18] If translating, then work from the annotated English template at 17 characters per second, never from SDH or speech recognition, because every language must keep the same cues [V].
19. [R19] If a name is a common word in a target language, then add a glossary note and check every cue ("Io." is "I" in Italian; "VALE" is "OK" in Spanish) [J].
20. [R20] If a language reads slowly (Japanese 4 characters per second [V]), then the template note names the words that carry the beat, because the translator must cut [J].
21. [R21] If on-screen text reads forward and is plot-pertinent, then FN at its first forward appearance; if the beat is the text's direction, then no FN there, because a subtitle pulls the eye off the sign [J].
22. [R22] If on-screen text reads backwards, then no FN in any language (D8-R53), and AD says "backwards" [J].
23. [R23] If a language barrier is story and a dub language equals one of the story's languages, then log `barrier_moments` and decide per version, because Netflix asks partners to flag this [V].

**Dubbing** [§4 E]
24. [R24] If dialogue is per-line files (D3), then dub per line (Rec5), automatic dubbing only for tests, because per-line keeps path chains, timing and delivery [J].
25. [R25] If `mouth_on_screen: visible`, then it is a lip line: syllables within about ±30% and a lip closure (m, b, p) near the original's; otherwise a free line matching start, end and pauses (Netflix's waveform rule [V]) [J].
26. [R26] If a lip line still mismatches, then lip-sync only that shot (D3 §2B), because doing all shots multiplies cost [J].
27. [R27] If a line has a `path_preset`, then apply the same chain to the dub, because the path is story (D3 §8) [J].
28. [R28] If a line is invented speech or a word the story says cannot be held, then `keep_original: yes`, on the keep-original track [J; U S7].
29. [R29] If uploading to YouTube, then set automatic dubbing off or "Publish manually", because it is "enabled by default for eligible creators" [V].

**Text in picture** [§4 F]
30. [R30] If a version localises graphics, then swap text only in forward-reading, plot-pertinent SVG inserts and re-composite on the textless plate [J].
31. [R31] If a translated word must read backwards, then check at least two of its characters look backwards when flipped, because symmetric characters only swap order (出口 → 口出, MAX → XAM; vertical text not even that); if it fails, keep the English or use a pictogram [J].
32. [R32] If a text is a glyph (the carriage's F), then never translate it [J].
33. [R33] If a display can use digits, arrows or icons, then prefer them, because they need no translation or FN (D12, B1 §16) [J].

**Colour and flashes** [§4 G]
34. [R34] If colour signals a state, then add shape, position, brightness or sound and pass the greyscale test, because "About 1 in 12 men have color vision deficiency" [V].
35. [R35] If a shot has police lights, sparks, glare or flicker, then fix a failing shot at its source before any filter or warning card [J].
36. [R36] If checking flashes in a public film, then never use PEAT (its terms prohibit film use [V]); screen with IRIS or the Rec7 scan; buy a HardingFPA test if a broadcaster asks, because free tools follow no published standard [V].
37. [R37] If a translated graphic needs letters the film's font lacks, then choose one matching OFL font per script, log it in D4 `asset_licence`, re-check cap height [J].
38. [R38] If adding AD on YouTube, then upload the original-language track first, then the full AD mix as "Descriptive audio", "roughly the same length as your video" [V].
39. [R39] If publishing text AD on a website, then embed a player that voices it (Able Player), because browsers do not speak `descriptions` tracks alone [U; V for Able Player].
40. [R40] If a shot must flash, then space flash onsets at least 12 frames apart at 24 fps or keep the area under a quarter of frame and the change small, because over 3 a second fails WCAG 2.3.1 and the UK note, and IRIS flags 2–3 a second sustained 5 s [V].

## 3. Breakdown fields

Enums `snake_case`, empty `none` (C5). [§6]

| level | field_name | meaning | allowed values / example |
|---|---|---|---|
| film | `access.versions[]` | Versions to make | {`version_id` `V-ES-DUB`, `lang` BCP 47, `kind`: `sdh`\|`subtitles`\|`forced_narrative`\|`ad_mix`\|`open_ad_video`\|`ad_text_vtt`\|`descriptive_transcript`\|`dub`, `status`: `planned`\|`draft`\|`checked`\|`delivered`} |
| film | `access.ad_voice_id` | Narrator voice | `VOICE-AD` (D3 §10.2 format) |
| film | `access.ad_rate_wps`, `access.ad_dip_db` | AD budget; dip | `2.5`; `6`–`12` |
| film | `access.glossary[]` | Names and terms | {`term`, `type`: `name`\|`place`\|`in_world_text`\|`technical`, `dnt`: yes/no, `note`, `per_lang`} |
| film | `access.graphics_policy` | Text in picture | `original_plus_fn` (default) \| `localise_forward_ui` \| `localise_all` |
| film | `access.platform_auto_dub` | YouTube setting | `off` \| `publish_manually` \| `on` |
| film | `access.checks[]` | Rec7 results | {`check`: `eyes_closed`\|`sound_off`\|`greyscale`\|`flash`\|`native_speaker`, `version_id`, `tool`, `date`, `result`: `pass`\|`fail`\|`not_run`} |
| motif | `ad_words` | Fixed AD wording | "The letters face the right way." |
| scene | `language_plan` | Languages spoken | {`spoken[]`, `barrier_moments[]` (line IDs), `notes`} |
| scene | `ad_must_carry[]` | Visual facts a payoff needs | {`fact`, `shot`, `payoff_ref`} |
| shot | `protect_silence` | No AD or SDH inside | `yes` \| `no` (derived from A4) |
| shot | `ad_events[]` | One AD line | {`ad_id` `SC06-AD010`, `text`, `start_tc`, `gap_s`, `words`, `rank`: `1_payoff`\|`2_dialogue_gap`\|`3_setting_identity`\|`4_texture`, `basis`: `behavior`\|`on_screen_text`\|`setting`\|`identity`\|`action`, `over`: `none`\|`effects`, `pre_described`, `file`} |
| shot | `on_screen_text[]` | Each readable text | {`text_id`, `exact_text`, `mirror_state`: `normal`\|`mirrored`, `plot_pertinent`, `spoken_in`, `fn_policy`: `fn_every_lang`\|`fn_first_only`\|`none`, `localisable`: `yes`\|`dnt_name`\|`glyph`\|`digits_only`\|`mirror_symmetric`, `graphic_file`} |
| shot | `colour_codes[]` | Colour signalling state | {`element`, `colours`, `second_cue`: `shape`\|`position`\|`luminance`\|`sound`\|`none`} |
| shot | `flash_risk` | Flashing content | `none` \| `check` \| `fixed` |
| line | `keep_original` | Stays in every dub | `yes` \| `no` |
| line | `dub_sync` | Sync demand | `lip` \| `free` (from `mouth_on_screen`) |
| line | `translations.<lang>` | Per language | {`sub_text`, `dub_text`, `syllables_src`, `syllables_dub`, `lip_closure_ok`, `picked_take`, `lipsync`: `none`\|`post`, `checked_by`} |
| line | `template_note` | Note for translators | text |
| cue | `lang`, `version_id` | Which version | `es-ES`, `V-ES-SUB` |

**Validator** [J]: plot-pertinent forward text has an FN or a reason; no `ad_events` inside `protect_silence`; no AD text names a `withhold` item; `words ≤ gap_s × ad_rate_wps`; AD ends ≥ 0.3 s before the next line or key sound; each `colour_codes` has a `second_cue` or AD line; each lip line has `syllables_dub`; each `flash_risk: check` shot has a `flash` check. **Blueprint map**: `exact_text` = `TEXT.words`; `plot_pertinent` = `TEXT.plot_critical`; `fn_policy`/`localisable` extend `TEXT.translate`; non-empty `ad_must_carry` = `needs_description: yes`; `dub_sync: lip` = `hear` with `speaker: on_screen`.

## 4. Procedures

**P1. Access plan** [Rec1; breakdown; 20–40 min]
1. Ask: *"Read the breakdown. List every plot-critical fact (A4 information-ledger entries and every `withhold` payoff) and the channels carrying it: picture, sound, dialogue, colour, on-screen text. Flag single-channel facts and propose one fix each: an added sound or shape, an AD line, an SDH label. Fill `ad_must_carry`, `protect_silence`, `colour_codes` and `on_screen_text`."*
2. The user approves picture or sound changes; AD and SDH fixes need no approval.
3. Ask: *"Fill `access.versions`: English SDH, English AD mix, descriptive transcript, plus [languages], each as subtitles or dub. Start the glossary: every name, place, label and sign; mark DNT; note any name that is a common word in a planned language."*

**P2. SDH** [Rec2; after lock] Run D8-Rec10; ask *"Apply D18-R5 to R8: label planted absences, stopped sounds and withheld sources by sound only; use each motif's `sdh_label`. List every change with its script line."*; watch with sound off.

**P3. AD script, voice, mix** [Rec3; 2–4 h per 20 min]
1. *"Write and run a script that reads `lock_v1.otio` and the placed dialogue files and lists every gap of 1.2 s or more without dialogue, key `sync_fx` or `protect_silence`. Save `ad/gaps.csv` (start, end, length, shot)."*
2. *"For each gap, write present-tense AD from `behavior`, `on_screen_text` and `ad_must_carry`, ranked by D18-R9. Obey `withhold`. Use `ad_words`. Name characters once dialogue names them, or earlier where clarity needs it, and log which. At most 2.5 words per second of gap. Save `ad/CATCH_ad_en.csv`: ad_id, start, text, words, gap_s, rank, basis."*
3. Delete anything that interprets, explains or repeats the sound.
4. Design the narrator: *"A calm, clear narrator, [woman in her forties / man in his fifties], [pitch] voice, smooth and rounded, [accent] accent, even and unhurried, close to the microphone in a quiet room; warm but neutral, never dramatic."* Then *"Generate each line with VOICE-AD, three takes, named like `CATCH_SC06_AD010_T01.wav`; report any take longer than its gap."* Cut words, never speed up.
5. Mix (tested on ffmpeg 7.0: 6.0 dB dip, length kept):
```
ffmpeg -i CATCH_mix_en.wav -i CATCH_SC06_AD020_T02.wav -i CATCH_SC06_AD030_T01.wav -filter_complex "\
[1:a]adelay=4000:all=1[a1];[2:a]adelay=8600:all=1[a2];\
[a1][a2]amix=inputs=2:duration=longest:normalize=0,apad,aformat=channel_layouts=stereo[ad];\
[0:a]volume='1-0.4988*max(min(1,max(0,min((t-3.7)/0.3,(7.1-t)/0.3))),min(1,max(0,min((t-8.3)/0.3,(10.1-t)/0.3))))':eval=frame[duck];\
[duck][ad]amix=inputs=2:duration=first:normalize=0[out]" -map "[out]" -c:a pcm_s24le CATCH_ad_mix_en.wav
```
`adelay` = start in ms per file; one `min(...)` block per line (start − 0.3 to end + 0.3); `1-0.749` for 12 dB.
6. Listen eyes closed; fix; re-mix.
7. Deliver the mix (YouTube "Descriptive audio" per R38, or Vimeo "Audio description"), a WebVTT `descriptions` file, and *"merge dialogue, SDH labels and AD lines in time order into `CATCH_transcript_en.txt`."*
```
WEBVTT

SC06-AD020
00:00:04.000 --> 00:00:06.800
The bright sill, level. A way out.
```
```
00:00:04.0  [AD] The bright sill, level. A way out.
00:00:07.1  [metal shrieking]
00:00:17.4  ELI: Io.
```

**P4. Template and translations** [Rec4; per language]
1. *"Make `subtitles/CATCH_template_en.srt` at 17 characters per second, with a notes file keyed by cue explaining every pun, parallel, reference, register and glossary term."*
```
cue,line_id,words_to_keep,note
118,SC10-DL0465,"mint; street signs","Parallel is the point: mint and street signs are unchanged; Iona changed. Keep 'mint' literal (A2 chemistry)."
```
2. *"Translate the template into [language] with the glossary. Keep cue numbers and times. Look up that language's Netflix limits, give me the page, and list cues over the limit with cuts that keep the annotated words."*
3. FN cues in `subtitles/CATCH_fn_<lang>.srt`, each also copied into the full file:
```
41
00:08:12,000 --> 00:08:14,500
VALE. CAR. STEERING WHEEL.
```
4. A native speaker watches the film with the file.

**P5. Dub** [Rec5; 3–6 h per language]
1. *"For each line write `dub_text` in [language] from the translation and notes. Lip lines (D18-R25): syllables within ±30%, a lip closure near the original's, counts reported. Free lines: match length."*
2. Reuse or redesign voices; test three lines each.
3. *"Generate each dub line with its voice, delivery and path preset, three takes, naming as D3 plus the language code. Place picked takes at the original line's start over the M&E and the keep-original track."*
4. Lip-sync failures only; make target-language SDH from the dub text.
5. Budget: about 38,000 ElevenLabs credits per language (7,660 characters × 5 tries), 48,000 for a quarter-longer language; one Creator month (121,000, $22).

**P6. Translate a graphic** [Rec6] *"Copy `INS_<name>_NORMAL.svg` to `INS_<name>_<lang>_NORMAL.svg`; replace only the text with the glossary rendering; keep font, size and colours; if longer, reduce letter spacing, then size, never below a cap height of 4% of picture height in the smallest shot that shows it (D12 rule 6, VG1); if the font lacks any letter, stop and tell me (D18-R37)."* If mirrored: *"Make `_MIRRORED` with the C2 R6 transform, render both to PNG, and tell me whether the flipped word looks different from the unflipped one."* Re-composite on the textless plate; check every letter.

**P7. Access checks** [Rec7]
1. Eyes closed with the AD mix; sound off with SDH.
2. Greyscale: `ffmpeg -i CATCH_lock_v1.mp4 -vf hue=s=0 -c:a copy CATCH_grey.mp4`
3. Flash screen: `ffmpeg -i CATCH_lock_v1.mp4 -vf "signalstats,metadata=mode=print:key=lavfi.signalstats.YAVG:file=yavg.txt" -an -f null -` then *"Read `yavg.txt`. Count a flash as a rise and a fall (or fall and rise) of 20 or more. List every 1-second window with more than 3 flashes, and every 5-second stretch averaging 2 or more a second, with timecodes."* Step through flagged shots frame by frame; never PEAT.
4. Native speaker per version; log `access.checks`.

## 5. Checklists

**Breakdown** [§10]: Rec1 run, every single-channel fact fixed • every readable text has `on_screen_text` with `mirror_state`, `plot_pertinent`, `fn_policy`, `localisable` • `withhold`, `protect_silence`, `ad_must_carry` on SC06, SC07, SC13 and every payoff shot • glossary started, common-word names flagged • `colour_codes` second cues, `flash_risk`, `language_plan` filled.

**Generation**: no readable text generated; negative field (where one exists) has "subtitles, captions, on-screen text" (C3 §7G) • flashing lights prompted slow • textless plates and inserts saved separately; every line its own file.

**Post and delivery**: SDH watched with sound off • AD ranked, fitted, voiced, mixed, heard eyes closed; transcript exported • template with notes; native check; FN in FN and full files • dubs: lip lines checked, path chains applied, keep-original track present • translated graphics: all letters in font, cap ≥ 4%, flip test • flash screen with IRIS or Rec7 scan, not PEAT • greyscale logged • YouTube auto-dub off or manual; AD uploaded after the base track; web text AD via Able Player • AI-voice disclosure covers the narrator and dub voices (D3 `ai_voice_disclosure`, D4).

## 6. Saying it to AI models

- **Video models**: never ask for readable words; where a negative field exists add "subtitles, captions, on-screen text" (C3 §7G). Flashes in words: "slow police lights behind frosted glass, about one flash a second" (R40).
- **LLM writing AD**: give `behavior`, `on_screen_text`, `ad_must_carry`, `withhold`, `ad_words` and the gap list; demand present tense, word counts per line, no feelings, no names of withheld items (Rec3 prompts).
- **TTS narrator**: the frozen design prompt in P3 step 4; separate from the cast by age, timbre and pace, not pitch (all bands are taken in *The Catch*).
- **Translation LLM**: template plus notes plus glossary; ask for the language's Netflix limits with the page, and syllable and lip-closure counts for lip lines.
- **Dubbing voices**: Eleven v3 covers "70+ languages" [V]; the accent-keeping promise is documented for Multilingual v2 [V], so test whether a voice keeps its English accent before dubbing a whole language.

## 7. The Catch

**Decisions made** [§7]
- SC06: nothing added inside the CLACK's 10 black frames (`protect_silence`); D8's `[metal clacks]` stands. AD re-timed from A4's rows (49.7 s): 14 lines, e.g. "One hand hidden." (row 13), "Grip slips. Eyes shut." (ends before the CLACK at 22.1 s), "Eyes open. Upside down. The stripe shrinks below." (starts 0.5 s after the sound returns). Never "puck" or "clips" before SC13. Blood beads, sprung gate and upside-down tag lose out (rank 3–4).
- AD calls Iona "Iona" from SC01 (Netflix's clarity exception); dialogue says only "Io" until "Iona?" (l.858).
- SC02 gets `[no sound of it landing]` so SC06's late crash pays off "This time they hear it land."
- SC10: AD adds only the rings, the bottle cap ("Eli's bottle cap opens the other way." in a short gap) and "She chews, then stops. Her eyes drift down. One more slow chew." No label for "(not steady)". Template note keeps "mint" literal and the mint/street-signs parallel.
- SC10 dub: "Not mint." candidates es "No es menta.", fr "Pas d'la menthe.", de "Nicht Minze." (closure on *m* in the second half), ja ミントじゃない (6 morae, *m* first: lip-sync or accept).
- SC28: `ad_words` "The letters face the right way." shared with SC12; AD line 18 words, 7.2 s after "Leave it on."; **no FN at l.1620** in any language; no SDH cue.
- Audit fixes: "backwards" AD pattern from SC07; pump label with "three uneven"; `[hum stops]` at l.1508–1510; AD reads UPWARD SPEED digits; load light gets dashed red with a cross, solid brighter green with a tick, two lamps (D12 designs).
- `flash_risk: check`: police lights (l.492, l.1004), shelves (l.1392), sparks (l.1420), the figure's strip (l.852).

**Flagged for the user**
- Pump label wording (D8 now defaults to D18's).
- CLICK label: `[small metal click]` for l.844, or D8's `[metal clacks]` throughout.
- Colour-blind cues change the design (outline shapes, two-lamp light, possibly a chime).
- Graphics policy per market; which languages; dub or subtitle.
- Human or synthetic AD narrator (synthetic accepted, human preferred [V]).
- YouTube identity verification for Advanced features (a privacy choice).
- "Io." pronunciation (two syllables assumed); German "Push." as *Los!* needs a native check.
- Paid HardingFPA test only if a broadcaster asks.

## 8. Conflicts and open questions

1. **D8 §9.4 RECEIVING FN**: D8 says translations may add one at l.1620; D18-R21 says none. Resolve in D8.
2. **D8-R50 BBC style marked [U]**: D18 read it in BBC v1.2.5 [V]; D8's Netflix default unaffected.
3. **D8 CLICK/CLACK family**: `[metal clacks]` vs `[small metal click]`; user picks.
4. **D13 §16 dub credits**: resolved; counted characters give 38,000 per language, 48,000 with expansion.
5. **Blueprint field names**: `TEXT.words`/`plot_critical`/`translate`, `needs_description` vs D18's names (map in §3); the builder decides whether `TEXT.translate` grows into `fn_policy` + `localisable`.
6. **D12 fonts**: no second typeface for Japanese or Chinese graphics yet (R37).
7. **B1 §16 mirror state** of visor and monitors decides which UI text gets FN at all (RECEIVING at l.1506; VALE at l.608).
8. **C3 citation**: the critic's brief points to "C3 §7A (languages)"; languages are C3 §7B, keeping text off screen §7G.
9. **The Long Places**: on-screen language (D17 open question 5; D3 open question 6) sets AD and dub load; Turkish scenes with English subtitles roughly double AD work (AD reads subtitles aloud [V]).
10. **Unverified**: Netflix M&E optional-track wording; ElevenLabs watermark rates on paid plans; native browser support for `descriptions`; whether Ofcom's current flash guidance changed the ITC numbers.
11. **Flash tools**: PEAT barred; IRIS needs compiling; Rec7 scan is a screen only [J].

## 9. Section map

| § | Contents |
|---|---|
| Header | Purpose, evidence labels, fact-check note (corrections list), builds-on list |
| §0 | Where D18 sits: breakdown, generation, post |
| §1 | Terms (SDH, FN, template, AD, gap, dip, lip/free line, M&E, SRT/WebVTT, stem, dB, lock file, ffmpeg) |
| §2 | Ten principles |
| §3 | Standards and tools: Netflix/BBC table, FN, AD guides, WCAG, `track`, platforms, dubbing, colour and flashes |
| §4 | Rules R1–R40 (A planning, B SDH, C AD, D translation, E dubbing, F text in picture, G colour and flashes) |
| §5 | Recipes 1–7 with prompts, ffmpeg templates and file samples |
| §6 | Fields, validator, blueprint map |
| §7 | *The Catch*: SC06, SC10, SC28, audit table, flash list |
| §8 | *The Long Places*: chapters VII, V, XI |
| §9 | Failure modes |
| §10 | Checklists |
| §11 | Conflicts and open questions (18 items) |
| Sources | S1–S31 plus library files |
