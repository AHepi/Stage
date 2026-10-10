# D18. Accessibility and localisation: SDH, audio description, dubbing and translated text in picture

*Library file D18. Written 2026-09-27. Test sources: "The Catch" (screenplay, workshop revision of 25 September 2026) and "The Long Places" (prose, revised final).*

> **What this file is for**
> 1. It makes the finished film usable by deaf and hard-of-hearing viewers (SDH), blind and low-vision viewers (audio description), colour-blind viewers and people with photosensitive epilepsy.
> 2. It makes foreign-language versions: translated subtitles, AI dubs made line by line from the breakdown, and translated or kept text in the picture (C2 R6 insert graphics).
> 3. It moves these decisions into the breakdown, before generation, so nothing is baked into the picture that later has to be undone.
> 4. It adds access and language fields to the breakdown, with recipes a non-technical user can run by asking an LLM.
> 5. It is worked on *The Catch* (SC06 CLACK and black, SC10 "Not mint.", SC28 RECEIVING read twice) and *The Long Places* (chapters V, VII, XI).

**Evidence labels.** [V] read on the named source; [U] unverified (search excerpt only, page blocked, or not documented); [J] this file's judgment. [S#] points to Sources; every URL there was checked 2026-09-27. Re-check platform and tool facts older than a month.

**Fact-check note (2026-09-28, adversarial).** Re-opened: Netflix's English, Japanese, Turkish and template timed-text guides, the forced-narrative page, Localization Best Practices, the Dubbing Creative Guidelines and the AD Style Guide v2.5; the BBC Subtitle Guidelines v1.2.5 (downloaded page); DCMP Description Key pages 617 and 618; WCAG 2.2; the WHATWG `track` table; YouTube's AD, multi-language audio, automatic dubbing and Advanced features pages; Vimeo's audio-track page; ElevenLabs' dubbing docs, pricing and models pages; the JoSTrans study; the NEI page; the PMC tool study; EA's IRIS; the FFmpeg filter manual; the ITC/Ofcom flashing-images note (a mirror copy of the same PDF); Able Player's description demo; the Trace Center's PEAT page. Every quoted line of both test texts was re-matched against the source files. **Corrections:** the "speaker's unique characteristics and accent" wording belongs to ElevenLabs **Multilingual v2** (29 languages), not Eleven v3 (§3.4, Recipe 5); "Describe what you see" is on DCMP's *What to Describe* page (618), not 617 (§2, S30); browsers do not voice a WebVTT `descriptions` track on their own, so a text AD needs a player such as Able Player (§3.2, D18-R39); YouTube's AD track needs the original-language audio track uploaded first (§3.3); Netflix names characters "until introduced through dialogue or plot-point" (§3.2); the UK flash-area limit is now [V] from the PDF (§3.5); PEAT, the free flash checker, **may not be used on film** (D18-R36); **SC06's AD table was re-timed from A4's row durations: seven lines broke this file's own 2.5 words-per-second budget and were cut, and two more ended less than 0.3 s before a key sound and were moved** (§7.1); "Io." is two syllables, not one (§7.1); ミントじゃない is 6 morae, not 5 (§7.2); the SC28 AD line is 18 words, 7.2 s (§7.3); the exit-sign AD line is adapted from l.331, not quoted (§7.3); C3's negative is "subtitles, captions, on-screen text" (§10); the dub credit estimate now uses the counted 7,657 spoken characters (D13's conflict, Recipe 5). **Added:** a tested ffmpeg AD-mix template (Recipe 3), WebVTT, template-note, forced-narrative and transcript samples, concrete flash spacing (D18-R40), a font rule for other scripts (D18-R37), YouTube and web-player rules (D18-R38, R39), a map to the blueprint's field names (§6), and new conflicts (§11).

**Builds on, does not repeat.** D8 §4.7 and §9.4 (subtitle rules D8-R47 to R55, Netflix limits, SDH house style, cue fields, the SC06 SDH sample, backwards text D8-R53, unknown languages D8-R54); D3 (voice assets, line fields, paths, lip-sync tools and prices); C2 R6 and W2 (insert graphics as SVG, the mirror transform, mirrored plates); C3 §7 (dialogue formats, keeping text off the screen); A4 (information ledger, true silence, motifs, `sync_fx`); D15 (`behavior` steps); C5 (`purpose`, `withhold`, IDs); B1 (phase B screens). **Leaves to:** D12 (designing signs and UI), D17 (the world's country and language), D4 (disclosure wording).

---

## 0. Where this sits

1. **Breakdown** (after A4 and D3, before generation): the access plan, the double-coding audit (Recipe 1), `on_screen_text` and `language_plan`. This is "accessible filmmaking": planning translation and access inside production, not after it (Romero-Fresco, 2019 [V S23]).
2. **Generation** (C2, C3, D6): every readable word is an insert graphic on its own layer; every voice line is its own file.
3. **Post** (after D8 checkpoint F, picture lock): SDH, audio description, template, translations, dubs and access checks, delivered at D8 checkpoint H.

---

## 1. Terms (one plain sentence each)

- **Accessibility**: making the film usable by people who cannot hear it, cannot see it, cannot tell some colours apart, or cannot safely watch flashing light.
- **Localisation**: making a version of the film for people who speak another language.
- **Version**: one finished output for one audience (the Spanish dub). **Track**: one audio or subtitle file inside a version.
- **Subtitle**: timed text on screen; this file uses the word for all timed text, including closed captions. One subtitle event is a **cue** (D8).
- **SDH**: subtitles for deaf and hard-of-hearing viewers, adding sound labels and speaker names (D8).
- **Forced narrative (FN)**: a subtitle every viewer of a language gets, translating plot-pertinent on-screen text or foreign speech.
- **Template**: an annotated, timed English subtitle file that translators work from, so every language keeps the same cues.
- **Glossary**: one list of names and in-world terms saying, for each, translate, keep or explain. **DNT** (do not translate) marks a term kept as written.
- **Audio description (AD)**: a narrator's voice, placed in the gaps of the soundtrack, telling a blind viewer what they need to see.
- **Gap**: a stretch with no dialogue and no key sound, where AD can speak.
- **Dip**: lowering the film's own sound under an AD line.
- **Pre-description**: describing something just before it appears because there is no room when it does.
- **Extended AD**: AD that pauses the picture to make room; only some web players can do it.
- **Open / closed**: mixed into the picture or main sound for everyone / a separate track the viewer switches on.
- **Descriptive transcript**: a text file with all dialogue, sound labels and descriptions in time order, readable on a braille display.
- **Dub**: a version whose dialogue is replaced by speech in another language.
- **Lip line / free line**: a dubbed line whose speaker's mouth is visible, so it must match the lips / one whose mouth is not, so it must match only timing.
- **Keep-original track**: lines that stay in their original sound in every dub. **M&E** is music and effects without dialogue (D8).
- **Textless plate**: a shot without its insert graphics, kept so text can be re-made.
- **Mirror state**: whether a graphic reads normally or reversed in a shot (C2).
- **Double-coding**: carrying one story fact through two senses, so a viewer who misses one still gets it.
- **Colour-vision deficiency (CVD)**: difficulty telling some colours apart, most often red from green.
- **Photosensitive epilepsy (PSE)**: seizures that flashing or patterned light can trigger.
- **BCP 47 code**: the standard short name for a language and region, such as `es-ES`.
- **SRT / WebVTT**: the two common subtitle file formats, plain text files of numbered or named cues with start and end times; WebVTT (`.vtt`) is the web one and can also carry AD text (D8-R55).
- **Sidecar file**: a subtitle or AD file delivered next to the video rather than burned into it; the viewer switches it on.
- **Stem**: one group of the film's sound kept as its own file (dialogue, music, effects), so it can be swapped or re-mixed (D8).
- **dB (decibel)**: the unit for loudness changes; lowering by 6 dB halves the signal's amplitude, which sounds clearly quieter but still present (a sound heard as "half as loud" is nearer 10 dB down).
- **Lock file (`lock_v1.otio`)**: the edit's final shot list with every in and out point, exported at picture lock (D8 checkpoint F); OTIO is the OpenTimelineIO format.
- **ffmpeg**: a free command-line program that cuts, mixes and converts audio and video; the LLM writes the command and you paste it into a terminal.

---

## 2. Core principles

1. **Plan access in the breakdown.** An AD gap, a mirrored sign or a red/green light is cheap to fix before generation and expensive after lock [J; S23].
2. **Double-code every plot-critical event.** *The Catch* does it once: the CLACK (sound) lands on black (picture). Elsewhere backwards text is picture-only, the pump sound-only, the outlines colour-only (§7.4) [J].
3. **Same thing, same words.** A motif gets one SDH label (D8-R51), one AD wording and one glossary entry, reused verbatim [J].
4. **Describe, do not explain; never reveal a `withhold`.** "Generally, describe what you see" (DCMP [V S30]) and "Describe objectively without personal interpretation, censorship, or comment" (DCMP [V S11]); never name what the film hides before it shows it [J].
5. **Protect designed silences.** A4's true silences and listening holds are story; "Do not try to fill every pause. Allow atmosphere and background sound to come through." (DCMP [V S11]); Netflix: "Only interrupt music, sound effects ... and intentional silence for vital, timely information that must be described." [V S9].
6. **Words from the script, times from the audio** (D8), for subtitles, AD and dubs alike.
7. **Text is a layer, never a pixel.** Readable words stay insert graphics on textless plates (C2 R6), so they can be mirrored, translated or checked without regenerating video [J].
8. **Voices are files, not mixes.** One file per line (D3) and separate dialogue, M&E and keep-original stems (D8-R37) make a dub a swap of dialogue files [J].
9. **Test with the sense removed**: eyes closed, sound off, greyscale [J].
10. **Machine output is a draft.** A native speaker checks each language; if possible a blind viewer checks the AD and a deaf viewer the SDH [J].

---

## 3. Standards and tools (checked 2026-09-27)

### 3.1 Subtitles and SDH beyond D8

| Point | Netflix | BBC |
|---|---|---|
| Sound labels | `[brackets]`, "all lowercase, except for proper nouns"; describe "sounds and audio as opposed to visual elements or actions" [V S1, updated 19 Dec 2025] | "white caps", no brackets, "on a separate line", placed left; "subject + active, finite verb" (`FLOORBOARDS CREAK`); "all editorially significant sound effects", including those "not obvious from the action", but no label for a man "clearly sobbing"; "Describe sounds, not actions" [V S10, v1.2.5, March 2026] |
| Speakers | `[name]` only "when they cannot be visually identified" [V S1] | Colour first; single quotes for an out-of-vision speaker [V S10] |
| Foreign speech | `[in Spanish]` translated, `[speaking Spanish]` untranslated; "[speaking foreign language] should never be used" [V S1] | Capitals language label above the translation [V S10] |
| Reading speed | English SDH 20 characters per second (D8); English template 17 [V S3]; Turkish subtitles 17, SDH 20 [V S5]; Japanese 13 full-width characters per line (SDH 16), 4 characters per second, SDH 7 [V S4] | "recommended rate of 160-180 words per minute", about 0.3 s per word on screen [V S10] |

Forced narratives [V S2]: an FN "clarifies communications or alternate languages meant to be understood by the viewer"; it shows only when the viewer's subtitles are off, so "all Forced Narrative events are also included in each full Subtitle and SDH/CC file", and the picture is delivered textless. English and Turkish FN for on-screen text are ALL CAPS (sentence case for long passages), and "Never combine a forced narrative with dialogue in the same subtitle box" [V S3, S5]; each language's own guide can differ (Japanese FN are italic, and redundant ones "must be deleted" [V S4]). Translate plot-pertinent on-screen text "unless redundant in the target language"; when text and dialogue overlap, "precedence should be given to the most plot-pertinent message"; flag it when a foreign language "creates an intentional barrier between characters and matches the dub target language" [V S6]. Templates carry annotations on "cultural references, idioms, jokes... puns and plays on words" [V S3].

### 3.2 Audio description

- **Netflix AD Style Guide v2.5** (27 Apr 2023) [V S9]: present tense, "third-person omniscient"; convey "facial expressions, body language and reactions, especially when in opposition to the dialogue"; "Description over dialogue should be utilized only as a last resort"; "Determine if the information is already being provided by other elements, such as dialogue, before adding to the description"; characters "should remain unnamed until introduced through dialogue or plot-point", but may be named earlier "when necessary for timing and clarification"; on-screen text "verbatim or paraphrased"; foreign-language subtitles "read by the AD voice" with the original dipped; "Description may adjust timings (pre-description) ... when there is no other way to sensibly inform the audience"; dip "6-12 dB, per mixer discretion", transitions "in no more than 5 seconds". It does not mention synthetic voices.
- **DCMP Description Key** [V S11]: "Describe objectively without personal interpretation, censorship, or comment"; "establish a pattern of on-screen words being read"; describe sources of sounds "that may not be immediately recognizable"; match the rate "to the pace of the program".
- **WCAG 2.2** (12 Dec 2024) [V S12]: captions Level A (1.2.2); AD **or** a text alternative Level A (1.2.3); AD Level AA (1.2.5); extended AD Level AAA (1.2.7). They bind websites that promise conformance, not festivals [J].
- **DCMP, What to Describe** [V S30]: "Generally, describe what you see and do not use cinematic terms (e.g., flashback or dream sequence)".
- **HTML `descriptions` track** [V S13]: "Textual descriptions of the video component of the media resource, intended for audio synthesis". Browsers do not speak it on their own [U: stated by 3Play Media's Able Player guide, not by a browser vendor]; Able Player reads it "using the Web Speech API", or through the viewer's screen reader where that API is missing, and offers "Automatically pause video when description starts", which is a form of extended AD [V S29].
- **Synthetic narrators** [V S22]: with 67 blind and partially sighted participants, "most participants accept Catalan text-to-speech audio description", but "natural voices obtain statistically higher scores" (2015; voices have improved since [J]).

### 3.3 Platforms

| Platform | AD track | Dub tracks | Source |
|---|---|---|---|
| YouTube | "Descriptive audio" in Studio > Languages; needs Advanced features; audio-only file "roughly the same length as your video"; the original or dubbed audio track in that language must be uploaded first; the file replaces the sound, so it is the full mix with AD [J] | Multi-language audio, also Advanced features | [V S14, S15] |
| YouTube Advanced features | Automatic with "sufficient channel history", or by verifying identity "using a valid ID or video" | | [V S17] |
| YouTube automatic dubbing | | "enabled by default for eligible creators"; marked "auto-dubbed"; "Publish manually" to review; minimal-speech videos ineligible; experimental lip sync for select channels | [V S16] |
| Vimeo | Track type "Audio description"; the feature "is included with all Vimeo plans" (Free "1 additional" track, Starter 5, Standard 10, Advanced 15, Enterprise 50) | Type "Dubbed audio" (a third type is "Commentary"); WAV, M4A, AAC, MP3 | [V S18] |

### 3.4 Dubbing

- **Per-line route**: the D3 voice assets speak the translated line. ElevenLabs Eleven v3 covers "70+ languages" [V S21]. The promise of "consistent voice quality and personality across all supported languages while maintaining the speaker's unique characteristics and accent" is made for **Multilingual v2** (29 languages), not for v3 [V S21]. So an English-accented design may stay English-accented in Spanish; test three lines, and design a new voice for the language if it does [J]. Lip-sync tools and prices: D3 §2B.
- **Automatic route**: ElevenLabs automatic dubbing (the default "Dubbing v2 Alpha model") takes a mixed file, detects speakers "even with overlapping speech", can "Keep background audio", "90+ languages", "Up to 1 GB and 180 minutes" in the app; automatic v2 has no in-app editor, while Dubbing Studio (v1) allows "transcript editing, speaker reassignment, and per-clip regeneration"; transcript editing via the API is "on Enterprise plans only" [V S19]. The pricing page lists 2,000 credits per minute (automatic, with watermark), 3,000 (automatic, without), 5,000 (Dubbing Studio, with) and 10,000 (Studio, without) [V S20], but the docs say "Free-tier dubs are watermarked automatically; paid-tier dubs are not" [V S19]; confirm which rate a paid plan is charged before paying.
- **Netflix dubbing** [V S8]: pursue lip sync without sacrificing "the message and intention" of the original; for off-screen dialogue, match the original waveform; follow the original stems for breaths and reactions. Its M&E guidance, per a search excerpt, puts "Language(s) being spoken that is foreign to that of the original language of production" and non-dialogue vocal sounds in separate optional tracks rather than the M&E [U S7: the page is script-rendered and would not load].

### 3.5 Colour and flashes

- About 1 in 12 men have a colour-vision deficiency, most often red–green [V S24]. WCAG 1.4.1: colour must not be "the only visual means of conveying information" [V S12].
- WCAG 2.3.1: nothing may flash "more than three times in any one second period, or the flash is below the general flash and red flash thresholds" [V S12]. The UK broadcast note (ITC, 2001, amended 2002, hosted by Ofcom as a legacy document) forbids a flash sequence only when both hold: the flashes together cover "more than one quarter of the displayed screen area" and "there are more than three flashes within any one-second period"; flashes whose leading edges are "separated by 9 frames or more are acceptable, irrespective of their brightness or screen area" (at 25 fps); "a transition to or from a saturated red is also potentially harmful" [V S25, read from a mirror copy of the same PDF; whether Ofcom's current guidance changed any number was not checked, U].
- FFmpeg's `photosensitivity` filter "Reduce[s] various flashes in video" [V S27]. EA's open-source IRIS (BSD-3-Clause) analyses video files for luminance flashes, red saturation flashes and patterns; it fails "More than 3 flashes per second in any given second" and flags "Between 2-3 flashes per second in any given 5 consecutive seconds" as an extended failure; it must be compiled (CMake, Ninja, vcpkg) [V S28]. A 2025 study says of FFmpeg's filter, IRIS and Apple's tool: "None of these three tools have algorithms that follow any published PSE standards"; it calls HardingFPA "a long-standing commercial tool" [V S26]. The Trace Center's PEAT is free (Windows), but "Use of PEAT to assess material commercially produced for television broadcast, film, home entertainment, or gaming industries is prohibited" [V S31]. Free tools screen; they do not certify [J].

---

## 4. Decision rules

### A. Planning

1. **D18-R1.** If the film will be public, then plan English SDH, an AD script and a descriptive transcript, because all three come cheaply from the breakdown and only AD written late is expensive [J].
2. **D18-R2.** If a story fact travels by one channel only (picture, sound or colour), then add a second channel in the breakdown or plan the AD or SDH line that carries it, because each audience loses one channel [J].
3. **D18-R3.** If a shot has `withhold` (C5), then AD and SDH state only what the frame shows, because naming the hidden thing spoils the payoff for the viewers who most depend on the description [J].
4. **D18-R4.** If A4 marks true silence, a listening hold or a rupture, then set `protect_silence: yes`, because a voice over it destroys what the silence was built for [J].

### B. SDH (extends D8-R50 to R54)

5. **D18-R5.** If the absence of a sound plants a later payoff, then label it once, neutrally (`[no sound of it landing]`), because deaf viewers cannot notice an absence [J].
6. **D18-R6.** If a sound stopping is the event, then label the stop (`[hum stops]`), because the BBC labels sounds not obvious from the action [V S10] [J].
7. **D18-R7.** If a motif has a distinguishing pattern, then put the pattern into its fixed `sdh_label`, because the payoff may depend on recognising it: the pump is "three strokes, not quite even" (l.852), so `[three uneven pump strokes]` rather than D8's first `[pump thumping]`; D8 has since adopted this wording as its default (§11 item 1) [J].
8. **D18-R8.** If a sound's source is withheld, then label the sound, not the source, because "describe sounds, not actions" [V S10] and the source is story [J].

### C. Audio description

9. **D18-R9.** If choosing what to describe in a gap, then rank: (1) facts a later payoff needs (A4 ledger, `ad_must_carry`); (2) actions that contradict or complete the dialogue; (3) setting and identity; (4) texture; fill in rank order, because gaps are short [J; Netflix "plot-critical" V S9].
10. **D18-R10.** If a shot has a `behavior` list (D15), then write AD from it and use `purpose` only to rank, because `behavior` is observable and `purpose` is interpretation [J].
11. **D18-R11.** If writing an AD line, then budget 2.5 words per second of gap and end 0.3 s before the next line or key sound, because AD over dialogue is a "last resort" [V S9]; 2.5 matches C3 and D3 [J].
12. **D18-R12.** If a gap is too short for a rank-1 fact, then pre-describe it in the nearest earlier gap, because Netflix allows it "when there is no other way" [V S9].
13. **D18-R13.** If a visual motif recurs, then fix one AD wording in `ad_words` and reuse it verbatim, taking the script's phrase when objective ("The letters face the right way.", l.639) [J].
14. **D18-R14.** If on-screen text is plot-pertinent, then AD reads it verbatim and names its orientation when mirrored ("backwards"), because DCMP asks for a reading pattern [V S11] and orientation is the plot here [J].
15. **D18-R15.** If the soundtrack is sparse and has no music, then dip 6 dB, not 12, with about 0.3 s ramps, because a deep dip in a quiet mix makes the room vanish [J within V S9].
16. **D18-R16.** If AD needs a voice, then design one narrator (`VOICE-AD`, D3) unlike every character in the lineup test, calm and level, because blind viewers must never mistake the narrator for a character [J].
17. **D18-R17.** If the platform has no AD track, then deliver a clearly titled open-AD copy, and prefer tightening the edit over extended AD, because extended AD works only in some players [J; WCAG 1.2.7 is AAA, V S12].

### D. Translation and subtitles

18. **D18-R18.** If translating, then work from the annotated English template at 17 characters per second, never from the SDH file or speech recognition, because every language must keep the same cues [V S3; D8-R47].
19. **D18-R19.** If a name is also a common word in a target language, then add a glossary note and check every cue, because viewers read the word, not the name: "Io." is "I" in Italian; "VALE" is "OK" in Spanish [J].
20. **D18-R20.** If a language reads slowly (Japanese: 4 characters per second [V S4]), then the template note names the words that carry the beat, because the translator must cut and needs to know what to keep [J].
21. **D18-R21.** If on-screen text reads forward and is plot-pertinent, then give it an FN at its first forward appearance; if the beat is the text's shape or direction, give no FN there, because a subtitle pulls the eye off the sign that carries the beat [J; precedence rule V S6].
22. **D18-R22.** If on-screen text reads backwards, then no FN in any language (D8-R53), and AD says "backwards" [J].
23. **D18-R23.** If a language difference between characters is story and a dub language equals one of the story's languages, then log it in `language_plan.barrier_moments` and decide per version, because the dub can erase the barrier [V S6] [J].

### E. Dubbing

24. **D18-R24.** If dialogue is already per-line files (D3), then dub per line (Recipe 5), keeping automatic dubbing for quick tests, because per-line dubbing keeps each line's path chain, timing and delivery notes [J].
25. **D18-R25.** If `mouth_on_screen` is `visible`, then treat it as a lip line: syllables within about ±30% and a lip closure (m, b, p) near the original's; otherwise a free line matching start, end and pauses (waveform rule [V S8]) [J].
26. **D18-R26.** If a lip line still mismatches after adaptation, then lip-sync only that shot (D3 §2B), because doing every shot in every language multiplies cost [J].
27. **D18-R27.** If a line has a `path_preset` (earpiece, recording, helmet), then apply the same chain to the dub, because the path is story (D3 §8) [J].
28. **D18-R28.** If a line is invented speech or a word the story says cannot be held, then set `keep_original: yes` and put it on the keep-original track, because no dub may replace it [U S7] [J].
29. **D18-R29.** If uploading to YouTube, then turn automatic dubbing off or set "Publish manually", because it is on by default for eligible channels [V S16] and would replace designed voices [J].

### F. Text in picture

30. **D18-R30.** If a version localises graphics, then translate only forward-reading, plot-pertinent insert graphics by swapping the SVG text and re-compositing on the textless plate, because English signs are part of the world (D17) and FN covers them [J].
31. **D18-R31.** If a translated word must read backwards, then check that at least two of its letters or characters look backwards once flipped, because a flip of mirror-symmetric characters (口, 出, 田; A, H, M, O, T) only swaps their order (出口 becomes 口出, MAX becomes XAM), which a hurried viewer reads as a typo, not as a mirror, and in vertical text the order does not change at all; if it fails, keep the English or rely on a pictogram [J].
32. **D18-R32.** If a text is a glyph, not a word (the carriage's F), then never translate it, because it was chosen for its asymmetry [J].
33. **D18-R33.** If a display can speak in digits, arrows or icons, then prefer them (D12; B1 §16 also advises icons), because they need no translation, no FN and little AD [J].

### G. Colour and flashes

34. **D18-R34.** If a colour signals a state, then add a second cue (shape, position, brightness or sound) and pass the greyscale test, because 1 in 12 men may not tell red from green [V S24; V S12] [J].
35. **D18-R35.** If a shot has police lights, sparks, glare or generated flicker, then check the locked film and fix a failing shot at its source (re-time, soften, deflicker) before any filter or warning card, because a filtered master is not a verified one [J; S26, S27].
36. **D18-R36.** If checking flashes in a film you will show publicly, then do not use PEAT, and use IRIS (or Recipe 7's frame scan) as a screen; if a broadcaster or distributor asks for a flash certificate, then pay for a HardingFPA test, because PEAT's terms prohibit film use [V S31] and a 2025 study found that FFmpeg's filter, IRIS and Apple's tool follow no published PSE standard [V S26], so they screen but do not certify.
37. **D18-R37.** If a translated insert graphic needs letters the film's typeface lacks (Japanese, Chinese, Arabic; Turkish ı İ ş ğ in some fonts, D12 Recipe 7), then choose one matching OFL typeface per script, log it in D4 `asset_licence` and re-check the cap height, because a missing letter renders as an empty box or a fallback font that breaks the style [J; D12].
38. **D18-R38.** If adding AD on YouTube, then first upload the original-language audio track, then add the full AD mix (film sound plus AD, the film's exact length) as "Descriptive audio", because YouTube asks for a file "roughly the same length as your video" and a base track in that language first [V S14]; the AD file replaces the sound, it is not layered on it [J].
39. **D18-R39.** If publishing text AD (a WebVTT `descriptions` file) on your own site, then embed a player that voices it, such as Able Player, because browsers do not speak description tracks by themselves [U; V S29 for Able Player].
40. **D18-R40.** If a shot must show flashing light (police lights, a warning lamp, a strobe), then space flash onsets at least 12 frames apart at 24 fps (at most 2 a second), or keep the flashing area under a quarter of the frame and its brightness change small (behind the script's frosted windows), because more than 3 a second fails WCAG 2.3.1 unless the flashes stay below its brightness thresholds, and fails the UK note when they also cover more than a quarter of the screen [V S12, S25], and IRIS also flags 2 to 3 a second held for 5 seconds [V S28]. Prompt the rate in words ("slow police lights, about one flash a second") and check the result frame by frame [J].

---

## 5. Recipes

### Recipe 1. Access plan and double-coding audit (breakdown; 20–40 min; $0)

1. Ask the LLM: *"Read the breakdown. List every plot-critical fact (A4 information-ledger entries and every `withhold` payoff) and the channels carrying it: picture, sound, dialogue, colour, on-screen text. Flag single-channel facts and propose one fix each: an added sound or shape, an AD line, an SDH label. Fill `ad_must_carry`, `protect_silence`, `colour_codes` and `on_screen_text`."*
2. Approve changes to picture or sound as creative decisions; AD and SDH fixes need no approval.
3. Ask: *"Fill `access.versions`: English SDH, English AD mix, descriptive transcript, plus [languages], each as subtitles or dub. Start the glossary: every name, place, label and sign; mark DNT; note any name that is a common word in a planned language."*

### Recipe 2. SDH additions (after lock; 20 min)

1. Run D8-Rec10.
2. Ask: *"Apply D18-R5 to R8: label planted absences, stopped sounds and withheld sources by sound only; use each motif's `sdh_label`. List every change with its script line."*
3. Watch with sound off; any moment you do not understand gets a label.

### Recipe 3. AD script, voice and mix (after lock; 2–4 hours for 20 minutes; $0–22)

1. **Gaps.** *"Write and run a script that reads `lock_v1.otio` and the placed dialogue files and lists every gap of 1.2 s or more without dialogue, key `sync_fx` or `protect_silence`. Save `ad/gaps.csv` (start, end, length, shot)."*
2. **Draft.** *"For each gap, write present-tense AD from `behavior`, `on_screen_text` and `ad_must_carry`, ranked by D18-R9. Obey `withhold`. Use `ad_words`. Name characters once dialogue names them, or earlier where clarity needs it, and log which. At most 2.5 words per second of gap. Save `ad/CATCH_ad_en.csv`: ad_id, start, text, words, gap_s, rank, basis."*
3. **Check** against the film. Delete anything that interprets ("she is afraid"), explains ("this means") or repeats the sound.
4. **Voice.** First design the narrator once (D18-R16; D3's voice-design recipe). Brief in D3's `voice_brief` fields [J]: `timbre` smooth and rounded, close to the microphone; `accent` the film's market default (D17; the user decides); `pace_wps` 2.5; `status_in_voice` level, unhurried, no acting. Pitch cannot do the separating in *The Catch*: D3 §4.2 already gives Jude `low`, Iona `low_mid`, Eli and Saye `mid`, Nell `mid_high`. So design two candidates that differ from all five in age, timbre and pace together (for example a woman in her forties, mid pitch, smooth and rounded, unlike Saye's crisp late-fifties voice at 2.0 words per second; or a man in his fifties, low-mid, smooth and even, unlike Jude's gravel and Eli's thin voice) and keep the one that passes D3 §4.3's lineup check [J]. Design prompt: *"A calm, clear narrator, [woman in her forties / man in his fifties], [pitch] voice, smooth and rounded, [accent] accent, even and unhurried, close to the microphone in a quiet room; warm but neutral, never dramatic."* Then: *"Generate each line with VOICE-AD, three takes, named like `CATCH_SC06_AD010_T01.wav`; report any take longer than its gap."* Cut words, never speed up.
5. **Mix.** *"Write an ffmpeg command in the pattern below for every picked AD file in `ad/CATCH_ad_en.csv`; output `CATCH_ad_mix_en.wav`, the film's exact length."* [V S27] The pattern, tested at fact-check on ffmpeg 7.0 (the main mix measured 6.0 dB lower inside the dip and the output kept the input's length) [V, author test]:

   ```
   ffmpeg -i CATCH_mix_en.wav -i CATCH_SC06_AD020_T02.wav -i CATCH_SC06_AD030_T01.wav -filter_complex "\
   [1:a]adelay=4000:all=1[a1];[2:a]adelay=8600:all=1[a2];\
   [a1][a2]amix=inputs=2:duration=longest:normalize=0,apad,aformat=channel_layouts=stereo[ad];\
   [0:a]volume='1-0.4988*max(min(1,max(0,min((t-3.7)/0.3,(7.1-t)/0.3))),min(1,max(0,min((t-8.3)/0.3,(10.1-t)/0.3))))':eval=frame[duck];\
   [duck][ad]amix=inputs=2:duration=first:normalize=0[out]" -map "[out]" -c:a pcm_s24le CATCH_ad_mix_en.wav
   ```

   In plain words: `adelay=4000` starts an AD file 4.000 s into the film (one per file); the `volume` line lowers the film's own mix by 6 dB (to 0.501 of its level: `1-0.4988`) from 0.3 s before each AD line starts until 0.3 s after it ends, with 0.3 s slopes (here lines at 4.0–6.8 s and 8.6–9.8 s); one `min(...)` block per line goes inside `max(...)`; `duration=first` keeps the film's length. For a 12 dB dip use `1-0.749`.
6. **Listen with eyes closed.** Note every moment you are lost; fix and re-mix.
7. **Deliver**: the AD mix as a YouTube "Descriptive audio" (D18-R38) or Vimeo "Audio description" track [V S14, S18], or an open-AD copy; the AD text as a WebVTT `descriptions` file (D18-R39) [V S13]; and *"merge dialogue, SDH labels and AD lines in time order into `CATCH_transcript_en.txt`."* Samples:

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

   (The times are from A4's SC06 table, counted from the start of that sequence, not the film.)

### Recipe 4. Template and translations (per language; 1–2 hours plus a native check)

1. *"Make `subtitles/CATCH_template_en.srt` at 17 characters per second, with a notes file keyed by cue explaining every pun, parallel, reference, register and glossary term."* Notes file format (`subtitles/CATCH_template_notes_en.csv`) [J]:

   ```
   cue,line_id,words_to_keep,note
   118,SC10-DL0465,"mint; street signs","Parallel is the point: mint and street signs are unchanged; Iona changed. Keep 'mint' literal (A2 chemistry)."
   ```

   (Cue 118 is a placeholder; the line ID follows D3 §10.3, scene + `DL` + the line number of the speaker's cue.)

2. *"Translate the template into [language] with the glossary. Keep cue numbers and times. Look up that language's Netflix limits, give me the page, and list cues over the limit with cuts that keep the annotated words."*
3. Add FN cues (D18-R21, R22) as a separate file `subtitles/CATCH_fn_<lang>.srt` and copy each one into the full file at the same time [V S2]. FN cue, English style, ALL CAPS and never in the same cue as dialogue [V S3]:

   ```
   41
   00:08:12,000 --> 00:08:14,500
   VALE. CAR. STEERING WHEEL.
   ```

   (Cue number and times are placeholders; the line is l.608, and it gets an FN only if that monitor is kept forward, §7.4.)
4. A native speaker watches the film with the file, not just reads it.

### Recipe 5. Dub from the breakdown (per language; 3–6 hours)

1. *"For each line write `dub_text` in [language] from the translation and notes. Lip lines (D18-R25): syllables within ±30%, a lip closure near the original's, counts reported. Free lines: match length."*
2. Choose voices: the same assets (identity kept; the accent may carry over, a behaviour ElevenLabs documents for Multilingual v2 [V S21]) or new designs from each `voice_brief`. Test three lines per character; if a character must sound native in the dub, design a new voice [J].
3. *"Generate each dub line with its voice, delivery and path preset, three takes, naming as D3 plus the language code. Place picked takes at the original line's start over the M&E and the keep-original track."*
4. Check every lip line; lip-sync only failures (D3 §2B).
5. Make target-language SDH from the dub text, because hard-of-hearing viewers hear parts of the dub [J].
6. Cost [arithmetic, D13 method]: *The Catch* has 221 dialogue cues, 1,579 words and about 7,660 spoken characters (re-counted at fact-check without parentheticals; D3 and D13 give 7,666). At 1 credit per character on v3 (D3) and 5 tries per line, that is about 38,000 credits per language; allow about 48,000 for a language that runs a quarter longer than English (a common rough allowance for Spanish or German [J]), still inside one Creator month (121,000 credits, $22 [V S20]). Automatic dubbing of a 20-minute cut instead: 40,000 credits (automatic, with watermark) to 200,000 (Dubbing Studio, without) at the listed rates [V S20]; 60,000 if a paid plan is charged the no-watermark automatic rate.

### Recipe 6. Translate an insert graphic (10 min each)

1. *"Copy `INS_<name>_NORMAL.svg` to `INS_<name>_<lang>_NORMAL.svg`; replace only the text with the glossary rendering; keep font, size and colours; if longer, reduce letter spacing, then size, never below a cap height of 4% of picture height in the smallest shot that shows it (D12 rule 6, VG1); if the font lacks any letter, stop and tell me (D18-R37)."*
2. If the shot is mirrored: *"Make `_MIRRORED` with the C2 R6 transform, render both to PNG, and tell me whether the flipped word looks different from the unflipped one."*
3. Re-composite on the textless plate, flip the plate if mirrored (C2 W2), and check every letter at full size.

### Recipe 7. Access check viewing (per version; 1–2 hours)

1. **Eyes closed** with the AD mix, start to finish; note every moment you are lost.
2. **Sound off** with SDH; any moment you do not understand gets a label.
3. **Greyscale** over every `colour_codes` shot: `ffmpeg -i CATCH_lock_v1.mp4 -vf hue=s=0 -c:a copy CATCH_grey.mp4` (tested at fact-check [V, author test]). If you cannot tell the two states apart, add the second cue (D18-R34).
4. **Flash screen** on `flash_risk: check` shots. Run `ffmpeg -i CATCH_lock_v1.mp4 -vf "signalstats,metadata=mode=print:key=lavfi.signalstats.YAVG:file=yavg.txt" -an -f null -` (writes each frame's average brightness, 0 to 255; tested at fact-check [V, author test]), then ask: *"Read `yavg.txt`. Count a flash as a rise and a fall (or fall and rise) of 20 or more. List every 1-second window with more than 3 flashes, and every 5-second stretch averaging 2 or more a second, with timecodes."* This whole-frame average misses small or red flashes [J], so also step frame by frame through each flagged shot, or use IRIS if the LLM can build it with you (D18-R36). Never use PEAT on the film [V S31].
5. **Native speaker** watches one dub or subtitle version with the film.
6. Log each as an `access.checks` row (`check`, `version_id`, `tool`, `date`, `result`).

---

## 6. Fields this file adds to the breakdown

Enums lower-case `snake_case`, empty `none` (C5). Authority as in C5: **derived** (from script or files), **authored** (a decision with `decided_by`).

| Level | Field | Meaning | Allowed values / example | Authority |
|---|---|---|---|---|
| film | `access.versions[]` | Versions to make | {`version_id` `V-ES-DUB`, `lang` (BCP 47), `kind`: `sdh` \| `subtitles` \| `forced_narrative` \| `ad_mix` \| `open_ad_video` \| `ad_text_vtt` \| `descriptive_transcript` \| `dub`, `status`: `planned` \| `draft` \| `checked` \| `delivered`} | authored |
| film | `access.ad_voice_id` | Narrator voice asset | `VOICE-AD` (D3 §10.2) | authored |
| film | `access.ad_rate_wps`, `access.ad_dip_db` | AD word budget; dip | `2.5`; `6`–`12` | authored |
| film | `access.glossary[]` | Names and terms | {`term`, `type`: `name` \| `place` \| `in_world_text` \| `technical`, `dnt`: yes/no, `note`, `per_lang` {lang: rendering}} | authored |
| film | `access.graphics_policy` | Text in picture | `original_plus_fn` \| `localise_forward_ui` \| `localise_all` | authored |
| film | `access.platform_auto_dub` | YouTube setting | `off` \| `publish_manually` \| `on` | authored |
| film | `access.checks[]` | Recipe 7 results | {`check`: `eyes_closed` \| `sound_off` \| `greyscale` \| `flash` \| `native_speaker`, `version_id`, `tool`, `date`, `result`: `pass` \| `fail` \| `not_run`} | authored |
| motif | `ad_words` | Fixed AD wording | "The letters face the right way." | authored |
| scene | `language_plan` | Languages spoken | {`spoken[]`, `barrier_moments[]` (line IDs), `notes`} | authored |
| scene | `ad_must_carry[]` | Visual facts a payoff needs | {`fact`, `shot`, `payoff_ref`} | authored |
| shot | `protect_silence` | No AD or SDH inside | `yes` \| `no` | derived from A4 |
| shot | `ad_events[]` | One AD line | {`ad_id` `SC06-AD010`, `text`, `start_tc`, `gap_s`, `words`, `rank`: `1_payoff` \| `2_dialogue_gap` \| `3_setting_identity` \| `4_texture`, `basis`: `behavior` \| `on_screen_text` \| `setting` \| `identity` \| `action`, `over`: `none` \| `effects`, `pre_described`: yes/no, `file`} | text authored, times derived |
| shot | `on_screen_text[]` (adds to C5) | Each readable text | {`text_id`, `exact_text`, `mirror_state`: `normal` \| `mirrored`, `plot_pertinent`: yes/no, `spoken_in` (line ID or `none`), `fn_policy`: `fn_every_lang` \| `fn_first_only` \| `none`, `localisable`: `yes` \| `dnt_name` \| `glyph` \| `digits_only` \| `mirror_symmetric`, `graphic_file`} | text derived, rest authored |
| shot | `colour_codes[]` | Colour signalling a state | {`element`, `colours`, `second_cue`: `shape` \| `position` \| `luminance` \| `sound` \| `none`} | authored |
| shot | `flash_risk` | Flashing content | `none` \| `check` \| `fixed` | authored |
| line (D3) | `keep_original` | Stays in every dub | `yes` \| `no` | authored |
| line (D3) | `dub_sync` | Sync demand | `lip` \| `free` | derived from `mouth_on_screen` |
| line (D3) | `translations.<lang>` | Per language | {`sub_text`, `dub_text`, `syllables_src`, `syllables_dub`, `lip_closure_ok`: yes/no, `picked_take`, `lipsync`: `none` \| `post`, `checked_by`} | authored |
| line (D3) | `template_note` | Note for translators | text | authored |
| cue (D8) | `lang`, `version_id` | Which version | `es-ES`, `V-ES-SUB` | derived |

Validator checks [J]: every plot-pertinent forward text has an FN or a stated reason; no `ad_events` inside `protect_silence`; no `ad_events` text names an item in that shot's `withhold`; `words ≤ gap_s × ad_rate_wps`; every AD line ends at least 0.3 s before the next dialogue line or key sound (D18-R11); every `colour_codes` entry has a `second_cue` or an AD line; every lip line has `syllables_dub`; every `flash_risk: check` shot has an `access.checks` row of type `flash` before delivery.

**Map to the pipeline blueprint's names** (added at fact-check; the blueprint wins where it already has a field [J]). The blueprint (appendix, D18 row) keeps D18's work in `needs_description`, captions, the audio-description script, the text-to-translate list and `TEXT.translate`. Read D18's fields onto it this way: `on_screen_text[]` = the blueprint's TEXT record (`exact_text` = `TEXT.words`; `plot_pertinent` = `TEXT.plot_critical`; `fn_policy` and `localisable` extend `TEXT.translate`, which is only yes/no); `ad_must_carry` non-empty on a shot = `needs_description: yes`; `dub_sync: lip` = a `hear` item with `speaker: on_screen` (D3's `mouth_on_screen: visible`). The other D18 fields have no blueprint twin and are added under `access` or on the shot.

---

## 7. Worked examples: *The Catch*

### 7.1 SC06: the CLACK and the black

**Source.** "Eli gets one arm round Jude's chest. His other hand goes underneath. Behind Jude's back. Out of sight." (l.224); "He has one hand she cannot see." (l.253); "Her grip begins to slip." (l.255); "A hard metal CLACK." (l.259); "BLACK. A dark with nothing in it. One instant." (l.261); "Her eyes open." (l.263); "The cage is going UP." (l.267); "This time they hear it land." (l.298).

**Double-coding.** A4 row 17 already carries the rupture twice: CLACK and true silence for the ear, black for the eye. The blind viewer gets it from the silence, the deaf viewer from the black, so **no AD and no added SDH inside the 10 frames** (`protect_silence: yes`); D8's `[metal clacks]` cue stands.

**The plant for SC13.** `withhold` keeps the puck out of frame (C5: "Eli's right hand and PR-PUCK.S02 stay out of frame"). AD says only what is visible: at l.224 "His other hand slides behind Jude's back."; in row 13 "One hand hidden." Never "puck" or "clips" (D18-R3). `ad_must_carry` lists the puck under the flask ("A flat black PUCK clipped underneath it.", l.162) and "The clip under it is empty." (l.312), so SC13's reveal lands for blind viewers too.

**AD script** against A4 Worked Example 1. Times are seconds from the start of A4 row 1, summed from A4's row durations (49.7 s in all); the window is where the line is spoken; each line needs words ÷ 2.5 seconds and ends at least 0.3 s before the next line or key sound (D18-R11). Re-timed at fact-check: in the first draft seven lines over-ran the word budget and two more ended less than 0.3 s before a key sound [J, arithmetic]:

| A4 row | Window (s) | AD line | Words | Needs (s) | Rank |
|---|---|---|---|---|---|
| 1–2 | −0.9–1.1 (pre-described; button clunk at 1.5) | "Iona elbows the STOP button." | 5 | 2.0 | 1 (SC13 replays her elbow) |
| 5 | 4.0–6.8 (shriek starts 7.1) | "The bright sill, level. A way out." | 7 | 2.8 | 1 |
| 7 | 8.6–9.8 (over the shriek's tail) | "They look up." | 3 | 1.2 | 3 |
| 8 | 10.2–11.4 (after the motor cuts) | "The cage falls." | 3 | 1.2 | 1 |
| 9–10 | 11.9–15.1 | "Her body floats; her fingers grip the grid." | 8 | 3.2 | 1 |
| 11–12 | 15.1–17.1 ("Io." at 17.4) | "Opening flicks past. Stripe below." | 5 | 2.0 | 1 |
| 13 | 18.1–19.3 (after "Io.") | "One hand hidden." | 3 | 1.2 | 1 |
| 14–16 | 20.1–21.7 (CLACK at 22.1) | "Grip slips. Eyes shut." | 4 | 1.6 | 2 |
| 17 | none | protected: CLACK, black, silence | 0 | — | — |
| 18–21 | 23.0–26.2 (starts 0.5 s after the sound returns, so the return is heard) | "Eyes open. Upside down. The stripe shrinks below." | 8 | 3.2 | 1 |
| 22 | 26.3–27.5 | "The cage rises." | 3 | 1.2 | 1 |
| 24–25 | 28.9–31.7 | "The opening descends to meet them, slower." | 7 | 2.8 | 1 |
| 26 | 32.2–33.4 ("Push." at 34.1) | "She lets go." | 3 | 1.2 | 2 |
| 28–30 | 35.2–36.8 (pre-described; palm on steel at 37.2) | "She catches the sill." | 4 | 1.6 | 1 (SC02 plant) |
| 31–32 | 38.8–40.4 (boot scrape at 40.8) | "Through. The cage sinks." | 4 | 1.6 | 2 |
| 36 | none | protected: the listening hold before the late crash | 0 | — | — |

The blood beads (row 10), the sprung gate (row 23) and the tag on the upside-down gate (row 35) are rank 3–4 and do not fit. The blind version loses them: the ranking working [J]. Naming: dialogue names Jude (l.125) and Eli (l.190) before SC06 but calls Iona only "Io" until "Iona?" (l.858), so AD uses "Iona" from SC01 under Netflix's exception for "timing and clarification" [V S9].

**SDH additions.** SC02's "Spits into the dark. Does not hear it land." (l.101) gets `[no sound of it landing]` (D18-R5), so the row-36 cue `[distant crash far below]`, placed on the late crash and not before, pays off "This time they hear it land."

**Dub.** "Io." (two syllables if said "EYE-oh", as the name Iona suggests [J]) and "Push." (one) are lip lines: row 13 is an Eli close single, row 27 is "close on 'Push.'" (A4). "Io." is DNT; in Italian the subtitle writes "Iona" because *io* reads as "I", while the dub keeps the spoken "Io", which the ear hears as a name [J]. "Push." takes a one-syllable equivalent where one exists (German *Los!*) [J: native check].

### 7.2 SC10: "Not mint."

**Source.** "Saye's wedding ring. On her right hand." (l.436); "Iona looks down at her own ring, on her own left hand." (l.438); "Across the room Eli twists the cap of a water bottle. It will not give. He stops. Twists it the other way. It comes off." (l.440); "Iona chews it." (l.454); "Her face changes." (l.456); "(not steady)" / "Not mint." (l.462–463); "Nothing has happened to the mint. Nothing has happened to the street signs either." (l.466).

**AD.** The dialogue carries the hand test ("That is your left." / "It's my right."), so AD adds only what it cannot:

- After "It's my right.": "Saye's wedding ring is on her right hand. Iona's is on her left." (13 words, 5.2 s; rank 1, paid off by the rings in SC29).
- Next gap: "Across the room, Eli twists a bottle cap. It won't turn. He twists it the other way. It opens." (19 words, 7.6 s; rank 1). Short gap: "Eli's bottle cap opens the other way." (7 words, 2.8 s; "the wrong way" would interpret, D18-R10).
- "Her face changes." names a feeling, so AD uses D15's `behavior` steps: "She chews, then stops. Her eyes drift down. One more slow chew." (12 words, 4.8 s), ending before Saye's "What does it taste of?" Never "horrified" (D18-R10).

**SDH.** "(not steady)" gets no label: both styles label sounds, and the delivery is visible in the tightest close-up [J]. Saye, off screen but in the room and known, needs no speaker label [V S1].

**Template note** for Saye's cue: *"The parallel is the point: mint and street signs are unchanged; Iona is what changed. 'Street signs' points back to the backwards signs of SC07–SC09. Keep 'mint' literal: A2's chemistry (mirrored mint tastes of caraway) breaks if a local herb is swapped in."* At Japanese 4 characters per second, Saye's roughly 6 seconds hold about 24 characters, so the translation keeps the two nouns and the parallel [J from V S4].

**Dub adaptation.** "Not mint.": 2 syllables, planned 1.3 s, lip line in close-up, closure on the *m* [J; native check required]:

| Language | Candidate | Syllables | Lip closure |
|---|---|---|---|
| es-ES | "No es menta." | 3–4 | *m*, second half, as the original |
| fr-FR | "Pas d'la menthe." | 3 | *m*, second half |
| de-DE | "Nicht Minze." | 3 | *m*, second half |
| ja-JP | ミントじゃない (*minto ja nai*) | 6 morae (mi-n-to-ja-na-i) | *m* first: lip-sync this shot or accept |

Saye's lines here are off screen (A2 B8), so they are free lines: match length and pauses only.

### 7.3 SC28: RECEIVING, read twice

**Source.** "On the wall above Saye: RECEIVING." (l.1620); "Iona looks at it. Reads it again." (l.1622). Earlier: "VISOR VIEW: a wire-frame room marked RECEIVING hangs beyond the ledge." (l.1506); "The visor draws two separate marks on the path. TURN, below. CROSS AT 0, beside RECEIVING." (l.1534); and SC12's rhyme: "Iona reads the label. The letters face the right way. She reads it again." (l.639).

**What the beat is.** Since SC07 the world's text has read backwards to Iona (C2's Era B). The wall sign is the first world text to read forward: she is back (Era C). Sighted viewers get this from the letters; blind viewers get nothing unless AD says it.

**AD.** From SC07 on, AD reads mirrored text with "backwards" (D18-R14), taking the script's own words where they fit: "Every letter is backwards." (l.327, verbatim); "At the fire door, the green sign is backwards too. The little running man runs the other way." (adapted from l.331, which reads "...The little running man is running the other way."). SC12 and SC28 share `ad_words` (D18-R13):

- SC12: "She reads the label. The letters face the right way. She reads it again."
- SC28, in the gap after "Leave it on.": "Above Saye, a sign: RECEIVING. Iona looks at it. Reads it again. The letters face the right way." (18 words, 7.2 s at 2.5 words per second). If the gap is shorter, pre-describe the sign while Jude and Iona fall onto the mat, keeping "Reads it again. The letters face the right way." for the gap.

The repeated sentence lets a blind viewer hear the rhyme a sighted viewer sees [J].

**SDH.** No cue: nothing is heard, and English viewers read the sign.

**Translations.** Whether the visor reads backwards in phase B is B1's open question (B1 §16 recommends backwards, with icons carrying the meaning). If it reads backwards, it gets no FN (D18-R22); if it reads forward, "RECEIVING" gets its FN at l.1506 only. Either way, **l.1620 gets no FN**: the beat is the letters' direction, and a subtitle would pull the eye off them (D18-R21). This refines D8, which allowed an FN here.

```yaml
- text_id: TXT-SC28-RECEIVING
  exact_text: "RECEIVING"
  mirror_state: normal          # Era C (C2)
  plot_pertinent: yes
  spoken_in: none
  fn_policy: none               # beat is orientation (D18-R21)
  localisable: yes
  graphic_file: inserts/INS_SIGN_receiving_NORMAL.svg
```

**Localised graphics** (only under `localise_forward_ui` or `localise_all`): Recipe 6 makes `INS_SIGN_receiving_es-ES_NORMAL.svg` ("RECEPCIÓN"). "RECEPCIÓN" passes the flip test, because R, E, C, P and N look different mirrored; a Latin word made only of symmetric capitals (A H I M O T U V W X Y) would fail it: "MAX" flips to "XAM", reversed in order but with no backwards letter, and "OTTO" does not change at all (D18-R31) [J]. In a Chinese or Japanese version, a sign made of near-symmetric characters such as 出口 ("exit") would show no backwards character, only swapped order (口出), so the SC07 exit sign keeps the running man as the carrier, as the script already does [J]. The carriage's F (l.534) is a glyph: DNT in every version (D18-R32).

### 7.4 Audit summary for *The Catch* (Recipe 1)

| Fact | Channels in the script | Missing for | Fix |
|---|---|---|---|
| The world reads backwards (SC07 on) | Text in picture; one line, "Io. Your dashboard's on backwards." (l.353) | Blind | AD "backwards" pattern (D18-R14) |
| Eli is still turned (SC28–29) | "The familiar little smile, on the wrong side of his face." (l.1696); rings | Blind | AD in script wording |
| The pump is the figure's heart | Sound only until SC25 | Deaf | `sdh_label` with "three uneven" (D18-R7) |
| Load fits or not | "A light on the shell turns RED." (l.1331); "The light turns GREEN." (l.1342); "Two outlines. Hers green. Its own red." (l.1436) | CVD | Solid outline and tick for green, dashed and cross for red, green brighter; a two-lamp shell light (red below, green above); AD names the colour; D12 designs it [J] |
| The ship is falling | "The sick motor through them." / "Then not." (l.1508–1510) | Deaf | `[hum stops]` (D18-R6) |
| Upward speed reaches zero | "Beside it: UPWARD SPEED, in metres per second. Twelve. Six. Three." (l.1587); "Nought." (l.1591) | Blind; other languages | AD reads the numbers in sync; digits need no FN (D18-R33) |
| Whose dish it is | "The right: VALE. CAR. STEERING WHEEL." (l.608) | Other languages | FN (Saye's monitor reads backwards in phase B, B1 §16, so the FN applies only if that screen is kept forward); glossary: VALE is Iona's surname and Spanish for "OK" |

Flash risk (`flash_risk: check`): "Police lights beyond frosted windows." (l.492, l.1004), "Light fills the shelves." (l.1392), the sparks (l.1420), and the strip that "slides across, vanishes, slides across again" (l.852). Prompt the police lights slow ("slow police lights behind frosted glass, about one flash a second"), keep flash onsets at least 12 frames apart at 24 fps, and screen the locked film (D18-R35, R40; Recipe 7 step 4). The frosted windows already soften and shrink the flashing area, which helps [J].

---

## 8. Worked examples: *The Long Places*

**Language plan (chapter VII; D17 decides the spoken language).** The village speaks Turkish, Márton is Hungarian, the prose is English. The elder speaks "in a speech that was no language any of them had, and that each of them carried up in their own — Nilay's came up an old, smoothed Turkish; Márton's, he said later, came up Hungarian, which he had not dreamed in for forty years." (l.601).

- The elder's sound is `keep_original: yes`, on the keep-original track, never dubbed (D18-R28).
- The subtitle shows what the point-of-view character understands, "*the little sun that doesn't burn.*" (D8-R54). In a Turkish dub this matches Nilay's own hearing; in a Hungarian dub Márton's private experience becomes the audience's. Log both in `barrier_moments` and decide per version (D18-R23).
- If village scenes play in Turkish with English subtitles, the English AD must read those subtitles aloud with the dialogue dipped [V S9], roughly doubling AD work for those chapters: a line for D13's budget [J].

**The knock (chapter V).** "Melek rose, laid the flat of her hand on the sounding stone, and knocked twice, softly, and then stood in the waiting, two breaths entire, and the waiting was the rite, if it was a rite" (l.419); "On the second breath of the after-quiet, something came under the knock. Low. Shaped. With the fall of a sentence in it." (l.421).

- AD before the knock: "Melek lays her palm on the stone beside the niche. Knocks twice, softly." Then nothing: the two breaths are `protect_silence: yes`.
- SDH: `[two soft knocks]`, then `[a low voice answers from the stone, no words]`: the sound, not a source the book never names (D18-R8).
- The prose is a quarry, not a script: "the waiting was the rite, if it was a rite" is the narrator's thought, never AD [J].

**The sign (chapter XI).** "a sign in two languages saying nothing either of them meant" (l.967). On this file's reading, the joke is that neither half means anything [J], so no FN (not plot-pertinent), but AD reads it once, verbatim, because its emptiness is only noticeable if its words are heard [J].

---

## 9. Failure modes

| Failure | Cause | Fix |
|---|---|---|
| AD spoils the twist (the puck named before SC13) | Written from `purpose` or prose, ignoring `withhold` | D18-R3; validator check |
| A voice inside the CLACK's black | Gap finder ignored A4 | `protect_silence` (D18-R4) |
| AD says feelings ("she is horrified") | Written from emotion lines | Rewrite from `behavior` (D18-R10) |
| AD cuts into dialogue | Word budget ignored; slow TTS | Cut words, re-voice |
| Backwards sign subtitled forward, or FN covering RECEIVING | Automatic on-screen-text pass | D18-R21, R22 |
| Italian viewers read "Io." as "I" | No glossary note | D18-R19 |
| Languages drift apart | Translated from SDH or recognition | Template (D18-R18) |
| Jude's earpiece voice sounds in the room in a dub | Path chain not re-applied | D18-R27 |
| The elder speaks Spanish | Line not flagged | `keep_original` (D18-R28) |
| A localised mirrored word looks normal | Symmetric characters | D18-R31 |
| Colour-blind viewers miss the load state | Colour-only code | D18-R34; greyscale test |

---

## 10. Checklists

**Breakdown**
- [ ] Recipe 1 run; every single-channel fact has a fix.
- [ ] Every readable text has `on_screen_text` with `mirror_state`, `plot_pertinent`, `fn_policy`, `localisable`.
- [ ] `withhold`, `protect_silence`, `ad_must_carry` set on SC06, SC07, SC13 and every payoff shot.
- [ ] Glossary started; names that are common words flagged.
- [ ] `colour_codes` have second cues; `flash_risk` marked; `language_plan` filled.

**Generation**
- [ ] No readable text generated into a clip; where a model has a negative-prompt field, it includes "subtitles, captions, on-screen text" (C3 §7G).
- [ ] Flashing lights prompted slow (about one a second; D18-R40).
- [ ] Textless plates and insert graphics saved separately; every line its own file.

**Post and delivery**
- [ ] SDH made and watched with sound off.
- [ ] AD ranked, fitted, voiced, mixed, watched with eyes closed; transcript exported.
- [ ] Template with notes; native check per language; FN in both FN and full files.
- [ ] Dubs: lip lines checked; path chains applied; keep-original track present.
- [ ] Translated graphics: every letter present in the font (D18-R37), cap height ≥ 4% (D12), flip test passed where mirrored (D18-R31).
- [ ] Flash screen run on every `flash_risk: check` shot with IRIS or the Recipe 7 scan, not PEAT (D18-R36).
- [ ] YouTube AD uploaded as the full mix after the original-language track (D18-R38); web text AD served through a player that voices it (D18-R39).
- [ ] Greyscale and flash checks logged; YouTube auto-dubbing off or manual; tracks uploaded with the right type.
- [ ] AI-voice disclosure covers the AD narrator and dub voices (D3 `ai_voice_disclosure`, D4).

---

## 11. Conflicts and open questions

1. **Pump label** (was a conflict with D8 §9.4): D8's second pass adopted `[three uneven pump strokes]` (D18-R7) as its default in D8-R51, §6 and §9 (D8 §10 item 11); the user confirms the wording once.
2. **CLICK/CLACK family**: D8 labels all of it `[metal clacks]`; SC15's "A small CLICK, from nowhere." (l.844) reads better as `[small metal click]`, keeping "metal" as the family word [J].
3. **FN at RECEIVING**: D8 §9.4 still says "translations may add a forced narrative" at l.1620; this file says none (§7.3, D18-R21). Resolve in D8.
4. **Visor and monitor mirror state** (B1 §16) decides which UI text gets FN at all.
5. **Colour-blind cues** (outline shapes, a two-lamp light, a chime) change the design: D12 and the user approve.
6. **Graphics policy**: default `original_plus_fn`; localising is a per-market creative choice.
7. **Which languages**, and which are dubbed rather than subtitled.
8. **Human or synthetic AD narrator**: most listeners accept synthetic, but human scores higher [V S22].
9. **YouTube Advanced features** need channel history or identity verification "using a valid ID or video" [V S17]; whether to verify is the user's privacy choice. Vimeo's audio tracks, AD among them, are "included with all Vimeo plans" (Free: one extra track) [V S18].
10. ***The Long Places* on-screen language** (D17; D3 open question 6) sets the AD and dub workload.
11. **Unverified**: Netflix M&E optional-track wording (page script-rendered; search excerpt only); ElevenLabs watermark rules (the pricing page lists watermarked dubbing rates, the docs say paid-tier dubs carry none); whether browsers voice `descriptions` tracks natively (3Play says none do); whether Ofcom's current flash guidance changed the ITC numbers.
12. **Dub credits** (conflict with D13 §16): D13 asked D18 to use the counted characters. Resolved here: about 38,000 credits per language at English length, about 48,000 with a 25% longer language (Recipe 5 step 6); D13's 38,000 is the floor.
13. **BBC style status** (conflict with D8-R50): D8 marks the BBC's upper-case, no-bracket style [U]; this file read it in v1.2.5 [V S10]. D8 can change its mark; its default (Netflix style) is unaffected.
14. **Field names** (conflict with the blueprint): the blueprint has `TEXT.words`, `TEXT.plot_critical`, `TEXT.translate` (yes/no) and `needs_description`; this file's `exact_text`, `plot_pertinent`, `fn_policy`/`localisable` and `ad_must_carry` map onto them as §6 states. The builder decides whether `TEXT.translate` grows into `fn_policy` + `localisable` or D18 keeps its own fields.
15. **Fonts for other scripts** (touches D12 and D4): D12 fixes B612 and IBM Plex Sans for *The Catch*; a Japanese or Chinese graphic needs a second typeface (D18-R37), which D12's style guide does not yet list.
16. **Flash-check tool**: PEAT is barred for film [V S31]; IRIS needs compiling; the Recipe 7 scan is this file's own screen [J]. If the film goes to a broadcaster, a paid HardingFPA report is the user's cost decision.
17. **"Io." pronunciation** (D3): §7.1 assumes "EYE-oh" (two syllables); if D3's voice for Eli says it otherwise, the lip-line count changes.
18. **C3 citation** (critic brief): the brief points to "C3 §7A (languages)"; C3's language material is §7B, and keeping words off the screen is §7G.

---

## Sources

All checked 2026-09-27; S1–S6, S8–S22 and S24–S31 re-opened 2026-09-28 at fact-check (S29–S31 added then); S23, a publisher's book page, was not re-opened.

- S1 Netflix, English (USA) Timed Text Style Guide (updated 19 Dec 2025): https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-USA-Timed-Text-Style-Guide [V]
- S2 Netflix, Understanding Forced Narrative Subtitles: https://partnerhelp.netflixstudios.com/hc/en-us/articles/217558918-Understanding-Forced-Narrative-Subtitles [V]
- S3 Netflix, Timed Text Style Guide: Subtitle Templates (updated 28 Jun 2024): https://partnerhelp.netflixstudios.com/hc/en-us/articles/219375728-English-Template-Timed-Text-Style-Guide [V]
- S4 Netflix, Japanese Timed Text Style Guide (updated 19 Dec 2025): https://partnerhelp.netflixstudios.com/hc/en-us/articles/215767517-Japanese-Timed-Text-Style-Guide [V]
- S5 Netflix, Turkish Timed Text Style Guide (updated 17 Oct 2025): https://partnerhelp.netflixstudios.com/hc/en-us/articles/215342858-Turkish-Timed-Text-Style-Guide [V]
- S6 Netflix, Localization Best Practices – Features & Series (updated 13 Jul 2023): https://partnerhelp.netflixstudios.com/hc/en-us/articles/360000119507-Localization-Best-Practices-Features-Series [V]
- S7 Netflix, M&E Creation & Delivery Guidelines (redirects to https://studiopartner.netflix.net/studio/m-and-e-creation-and-delivery-guidelines, script-rendered; wording from a search excerpt, re-tried 2026-09-28): https://partnerhelp.netflixstudios.com/hc/en-us/articles/115006122187-M-E-Creation-Delivery-Guidelines [U]
- S8 Netflix, Dubbing Creative Guidelines – Films & Series (English): https://partnerhelp.netflixstudios.com/hc/en-us/articles/11220839130771-Dubbing-Creative-Guidelines-Films-Series-English [V]
- S9 Netflix, Audio Description Style Guide v2.5 (updated 27 Apr 2023): https://partnerhelp.netflixstudios.com/hc/en-us/articles/215510667-Audio-Description-Style-Guide-v2-5 [V]
- S10 BBC, Subtitle Guidelines v1.2.5 (March 2026): https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/ [V; re-read 2026-09-28 from the downloaded page]
- S11 DCMP, Description Key – How to Describe: https://dcmp.org/learn/descriptionkey/617 [V; "Describe what you see" is not on this page, see S30]
- S12 W3C, WCAG 2.2 (Recommendation, 12 Dec 2024): https://www.w3.org/TR/WCAG22/ [V]
- S13 WHATWG, HTML Standard, track `kind`: https://html.spec.whatwg.org/multipage/media.html#attr-track-kind [V]
- S14 YouTube Help, Add audio descriptions: https://support.google.com/youtube/answer/16166822 [V]
- S15 YouTube Help, Multi-language audio: https://support.google.com/youtube/answer/13338784?hl=en [V]
- S16 YouTube Help, Use automatic dubbing: https://support.google.com/youtube/answer/15569972?hl=en [V]
- S17 YouTube Help, Advanced features: https://support.google.com/youtube/answer/9890437?hl=en [V]
- S18 Vimeo Help, How to add multiple audio tracks: https://help.vimeo.com/hc/en-us/articles/20233722972689-How-to-add-multiple-audio-tracks-to-my-video [V]
- S19 ElevenLabs, Dubbing: https://elevenlabs.io/docs/capabilities/dubbing [V]
- S20 ElevenLabs, Pricing (dubbing credits per minute): https://elevenlabs.io/pricing [V]
- S21 ElevenLabs, Models (Eleven v3 "70+ languages"; the accent-keeping sentence is under Multilingual v2): https://elevenlabs.io/docs/overview/models [V]
- S22 Fernández-Torné, A. and Matamala, A. (2015), "Text-to-speech vs. human voiced audio descriptions: a reception study in films dubbed into Catalan", *JoSTrans* 24: https://www.jostrans.org/article/view/7708 [V]
- S23 Romero-Fresco, P. (2019), *Accessible Filmmaking: Integrating translation and accessibility into the filmmaking process*, Routledge: https://www.routledge.com/Accessible-Filmmaking-Integrating-translation-and-accessibility-into-the-filmmaking-process/Romero-Fresco/p/book/9781138493018 [V]
- S24 National Eye Institute, Color Blindness: https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/color-blindness [V]
- S25 ITC Guidance Note for Licensees on Flashing Images and Regular Patterns in Television (revised July 2001, amended June 2002; Ofcom legacy document): https://www.ofcom.org.uk/__data/assets/pdf_file/0021/16248/gn_flash.pdf (403 to this agent); read from the same PDF at http://static.mtv.co.uk/tam/Ofcom_flashing_Imagery_and_Luminance_guidance.pdf [V, 2026-09-28]
- S26 "Evaluating Conformance of Video Safety Tools for Photosensitive Epilepsy" (PMC, 2025): https://pmc.ncbi.nlm.nih.gov/articles/PMC12249941/ [V]
- S27 FFmpeg Filters Documentation (`photosensitivity`, `sidechaincompress`, `hue`): https://ffmpeg.org/ffmpeg-filters.html [V]
- S28 Electronic Arts, IRIS: https://github.com/electronicarts/IRIS [V]
- S29 Able Player demo, "Audio description via VTT track, read by browsers": https://ableplayer.github.io/ableplayer/demos/desc1.html [V, 2026-09-28]
- S30 DCMP, Description Key – What to Describe: https://dcmp.org/learn/descriptionkey/618 [V, 2026-09-28]
- S31 Trace Center (University of Maryland), Photosensitive Epilepsy Analysis Tool (PEAT): https://trace.umd.edu/peat/ [V, 2026-09-28]
- Library files: D8 (subtitle rules, SC06 SDH sample), D3 (voices, lip-sync prices), C2 R6, W2 and the era table (insert graphics, mirror states), C3 §7, A4 Worked Example 1 (SC06 rhythm), D15 (SC10 behaviour), C5 (`withhold`, IDs), B1 §16 (phase B screens), D13 (credit method); D12 (rule 6 and VG1 cap height, Recipe 7 font coverage, red dashed and green solid), D13 §16 (credit count), the pipeline blueprint (appendix D18 row, TEXT record, `needs_description`).
