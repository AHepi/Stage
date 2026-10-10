# Digest D10: Genre and tone conventions

Source: `research/D10_genre_tone_conventions.md` (second check 2026-09-28: 25 sources re-fetched, two added; all quoted script and novella lines matched verbatim). Refs: [P#] §1; [TN#] §2.3; [CM#] §4; [HR#] §5; [SG#] §6; [GW#] §7; [R#] §8. Evidence: [V] read at source; [V-sec] via a secondary source; [U] unverified; [J] judgment. Every ASL range, factor and budget is [J].

## 1. Scope

1. Adds a `tone` field per film and per scene (11 values) and a table that moves every other file's defaults (pace, size and lens, movement, light, sound, performance, prompt opener) by tone.
2. Ten genre profiles with sourced pace anchors, plus working rules for comedy timing, horror and suspense, song sequences, and genre words that pull models toward stock looks and filters.
3. Runs at the story plan (film fields) and at each scene's breakdown, before B1/B2 shot design and C3 prompts; worked on *The Catch* SC15 and SC10 and on *The Long Places* ch. I.

**Plain terms.** *Tone*: the attitude of the telling (B1's "register"); *home tone*: the film's default; *undercurrent*: a second tone carried by lines and acting only. *ASL*: running time ÷ shots. *Punch*: what completes a joke. *Startle*: a jump scare. *Sting*: a sudden loud music hit. *Number*: a song or dance sequence. *Stem*: one isolated part of a mix. *Contrast ratio*: lit side of a face against its shadow side (2:1 soft, 8:1 dark). *Genre opener*: a prompt's first sentence naming genre and tone. *Display level* (D15): acting size per shot, 1–3.

## 2. Rules

**Principles and tone mixing**
1. [P1] If tone changes, then move baselines only (pace, size, light, sound, acting), never the turning points (A2), text marks (A4) or in-story footage and physics rules (B1 R22–R23), because tone is how the story is told, not what happens.
2. [P2, TN1] If a scene needs two tones, then set one `tone` and one `tone_undercurrent` and keep camera, light and cutting on the main tone, because the camera plays one tone at a time.
3. [P3] If a convention's reason would fit any film of the genre (B2's WHY test), then drop it, because it is a cliché.
4. [P4] If the genre is a setting genre (SF, fantasy, western, war, period), then let it set world and design (B4, B5) and take camera, light and cutting from the tone, because *The Catch* is SF in world, thriller in tone.
5. [P5] If a genre spends extremes (startles, numbers, slow motion), then budget them per film on top of B1 P5 and A4 P10, because strong devices wear out.
6. [P7, CM7] If a moment could read as pain or comedy, then the camera plays the more serious tone and size decides, because "Life is a tragedy when seen in closeup, but a comedy in long-shot" (Chaplin, indirect attribution) [V].
7. [P8] If a pace figure comes from published data, then use it as an anchor and let the animatic decide (A4 §6.1), because published ASLs describe whole past films.
8. [TN2, TN3] If the tone changes inside a scene, then put the shift on a turning point or drop (A2 R10), record `tone_shift`, and change one visible system there (size ladder, light cue, music in/out, camera behaviour), because a shift elsewhere reads as a wobble.
9. [TN4] If adjacent scenes contrast in tone, then cut hard and contrast their ASLs (A4 §6.9), because the gap does the shifting.
10. [TN5] If a comic beat falls just before a peak, then play it small; just after, let it land, because a laugh before a peak spends tension [J].
11. [TN6] If over a third of scenes carry an undercurrent, then re-check `tone_home`, because the film may be another genre.
12. [TN7] If `tone` is outside `tone_range`, or `tone_undercurrent` is neither in `tone_range` nor named in `tone_mix_rule`, then flag it for the user, never fix it, because tone is the writer's call.

**Comedy** (extends A2 §4: wide frames holding both bodies, hold for the laugh, no sympathy close-ups)
13. [CM1] If a line or action is the punch, then land it in a frame holding cause and victim, then cut to the reaction, because the laugh lives in the reaction (A2 R5).
14. [CM2] If a punch is being timed, then add no pause before it, because Attardo and Pickering found "no evidence" that "punch lines are preceded by pauses" in twenty joke performances [V] (spoken jokes; applying it to edits is [J]).
15. [CM3] If a punch lands, then hold the reaction 0.5–1.5 s (light) or 2–4 s (deadpan), with no music, because music tells the audience to laugh [J].
16. [CM4] If a gag repeats, then frame the first two identically and break only the third, because the pattern must be learned before it breaks (A2 R2).
17. [CM5] If the scene is deadpan, then frame frontal, centred, static and symmetrical with even light and no music, because the camera must not comment.
18. [CM6] If the joke is a reveal, then keep the frame static and let the thing enter or leave it, because a moving camera points before the joke (Every Frame a Painting on Edgar Wright) [V].
19. [CM8, CM9] If a joke needs sound, then use one sync effect on the exact frame, no laugh track, and cutaway gags only where scripted, because a precise sound beats a comic cue.
20. [CM10] If comic shots are generated, then prompt behaviours ("keeps a straight face; blinks once"), give reactions 1.5 s handles and one speaker per clip in banter (A2 R27), because AI faces over-act (A4 §4.2).

**Horror and suspense** (extends A4 §6)
21. [HR1] If the film is horror, then budget startles, false ones included, at about one per 10 minutes (any short: at most three), because recent films have "leveled off at around 10 scares per movie" (Where's the Jump, crowd data) [V].
22. [HR2] If a startle is placed, then give it Baird's "character presence", "implied off-screen threat" and "disturbing intrusion into the character's immediate space" [V-sec], because without all three it is only a loud noise.
23. [HR3] If a startle is placed, then precede it with a dread hold at least 3× the local ASL and make it the scene's shortest shot (A4 R4), because contrast is the scare [J].
24. [HR4, HR5] If a threat should grow or is withheld, then let it be heard before seen (A4 SND1–2), keep it at the frame edge or in darkness, and never tilt or pan to it (B1 P7), because a seen source loses power and in `dread` the threat never moves the camera.
25. [HR6, HR7] If building dread, then leave empty areas in frame and allow a sting only on a budgeted startle, rough rather than loud, because scary music imitates the "roughness" of screams [V].
26. [HR8] If choosing horror or mystery, then set A4's ledger mode first (`suspense`: audience knows more; `mystery`: knows what the character knows; `surprise`: knows less, once), because the ledger, not the lighting, makes the genre.
27. [HR9] If harm happens, then show cause, reaction and aftermath, never injury detail, because filters block it and Runway bars "Gore, such as dismemberment, beheadings, mutilations, and exposed organs/bones/muscle" [V].
28. [HR10] If a shot has lightning, strobes, muzzle flashes or alarms, then keep it at three flashes a second or fewer and mark it `flash_risk: check` (D18), because WCAG 2.3.1 forbids more than three flashes a second [V] and Ofcom fails more than three a second over 25%+ of the screen [V-sec].
29. [HR11] If a startle or peak has played, then give the next scene a release, because a second scare lands weaker [J].

**Song sequences**
30. [SG1] If a scene is a number, then lock the song (tempo, bars, lyric, vocal) before shot design, because picture is cut to music; ElevenLabs' `[sings]` tag is "experimental" [V].
31. [SG2] If cutting a number, then cut on bar lines or phrase ends, not beats, because beat cuts chop the dance; one beat = 1,440 ÷ BPM frames at 24 fps (120 BPM: 12 frames; a bar = 2 s).
32. [SG3] If the number is dance, then frame the full figure, track, cut rarely and never crop feet, because Astaire used "just four to eight cuts, while holding the dancers in full view at all times" [V]; write steps as counts plus a movement line.
33. [SG3] If no steps are locked, then Wan-Dancer-14B (open, July 2026; image + music + style prompt) may generate the dance [V]; never where counts are written, because it invents the steps.
34. [SG4] If a phrase outlasts one clip (most models 8–16 s; 20 s FLUX 3 Video, Ray3.2; 30 s Seedance 2.5, Wan 3.0), then cut on movement at a phrase end with axis, size and lens kept, or hide the cut in a body crossing the lens (A4 AI6).
35. [SG5] If a face sings, then send only the vocal stem to lip sync (sync. labs: "lipsync-2 is a good default", sync-3 best; "isolate and upload the vocals track") [V], because instruments disturb the mouth.
36. [SG6–SG8] If speech turns into song, then reuse one film-level entry rule, record `number_kind`, and name no artist or song in prompts (D9, D4), because the audience learns one rule and names raise rights issues.

**Genre pace** (§3, scene targets [J])
37. [§3] If setting a scene ASL, then start at: drama 4–8 s; thriller 2.5–5 s (peaks 1–2 s); mystery 4–7 s; horror dread 5–10 s; comedy banter 2.5–4 s, gags 4–8 s; romance 5–8 s; action fights 1.5–3 s; children's 3–6 s; slow cinema 10 s+, because ASLs fell from about 10 s (1930s–40s) to below 4 s after 2000 (Cutting) [V] and action films average 4 s (Follows; his horror 15.7 s is skewed, not a target) [V].
38. [§3.9] If the audience is young children, then set pace by comprehension and ration impossible events, because a 2024 review finds pacing effects "can be more certainly dismissed" but highlights "the negative effect of fantasy on inhibitory control" [V].

## 3. Breakdown fields

Enums lowercase snake_case; `none`, never empty. The blueprint wins on names: it already has `genre` (one field), `tone_home`, `tone_range`, `tone_mix_rule`, `tone`, `tone_undercurrent`, `tone_shift`. All other rows are proposals.

| level | field_name | meaning | allowed values / example |
|---|---|---|---|
| film | `genre_primary` | The main promise | `drama` `thriller` `mystery` `horror` `comedy` `romance` `action` `musical` `family_animation` `slow_cinema` |
| film | `genre_secondary` | Second promise or setting genre | same list + `science_fiction` `fantasy` `western` `war` `period` `none` |
| film | `tone_home` | Default tone | `grave` `tense` `dread` `enigmatic` `comic_light` `comic_dark` `romantic` `kinetic` `lyric` `wonder` `contemplative` |
| film | `tone_range[]` | Tones allowed as a scene `tone` | e.g. `[tense, enigmatic, dread, grave]` |
| film | `tone_mix_rule` | How the film mixes tones | text, e.g. "`comic_dark` only as undercurrent, never in camera" |
| film | `undercurrents_allowed[]` | Machine-readable form of the mix rule (proposed 09-28) | e.g. `[comic_dark]` |
| film | `audience_age` | Who it is for | `adult` `teen` `family` `young_children` |
| film | `genre_budgets` | Extremes the genre spends | `{startle: 1, false_startle: 0, sting: 1, number: 0, slow_motion: 0}` |
| film | `genre_opener`, `genre_words_banned[]`, `number_entry_rule` | Opener per tone; words never sent; how song starts | text; e.g. `gory` `funny`; text or `none` |
| scene | `tone` | Main tone | one of the 11 values |
| scene | `tone_undercurrent` | Second tone | one of the 11 values or `none` |
| scene | `tone_shift` | Change inside the scene | `<beat> \| from: <tone> \| to: <tone> \| device: size_ladder \| light_cue \| music_in \| music_out \| camera_behaviour`, or `none` (blueprint syntax) |
| scene | `set_piece` | Genre scene type (D11 reads it) | `startle` `stalk` `chase` `fight` `reveal` `gag` `number` `first_meeting` `confession` `task` `none` |
| scene | `performance_scale` | Acting size; caps D15's display level | `underplayed` (1) `naturalistic` (1–2) `heightened` (2–3) `broad` (3 + bigger gesture) |
| scene | `asl_factor` | Multiplier on D13's rhythm-class ASL | number from the tone table, e.g. `0.9` |
| beat | `comic_role` | Place in a joke | `setup` `repeat` `punch` `reaction` `none` |
| beat | `startle_part` | Place in a startle | `presence` `threat` `intrusion` `none` |
| shot | `reaction_hold_s` | Hold after a punch or startle | number, e.g. `2.5` |
| shot | `startle` | Spends a budgeted startle | `yes` `no` |
| shot | `flash_risk` | D18's field, reused | `none` `check` `fixed` |
| number | `number_kind` | Kind of number | `diegetic` `integrated` `fantasy` |
| number | `song_id`, `bpm`, `bars` | The locked song | `MU-##` (or theme `TH-##`); integer; integer |
| number shot | `bar_in`, `bar_out`, `lip_sync_route` | Where the shot sits; how the mouth syncs | integers; D3 `sync_method`: `none` `native` `audio_reference` `post_lipsync` |

**Tone defaults (§2.2; `rules/tone_defaults.json`).** "From this tone, start here"; a departure gets one line in `notes`.

| tone | asl_factor | size, lens | movement | light | sound | acting |
|---|---|---|---|---|---|---|
| `grave` | 1.0 | approach; normal | static; ≤1 push-in | ~4:1 | sparse | naturalistic |
| `tense` | 0.9; hold the unaware | tightening; long | static; handheld at loss of control | 4:1–8:1 | ticking, rising | contained |
| `dread` | 1.3; startle <1 s | empty wides; deep focus | threat never moves camera | 8:1+, readable | sound first; budgeted stings | underplayed |
| `enigmatic` | 1.1 | objective; inserts held | move only on noticing | readable | motifs as clues | withheld |
| `comic_light` | 0.9 + reaction holds | two-shots; normal-wide | static | ~2:1 | timed effects | heightened–broad |
| `comic_dark` | 1.1 | frontal, symmetrical | no push-ins | flat | no music under jokes | deadpan |
| `romantic` | 1.2 | matched singles; long; shallow | one push-in at turn | soft, warm | theme if `scored` | intimate |
| `kinetic` | 0.5 at peaks | geography first; wide | one move per clip | hard; ≤3 flashes/s | percussive | physical |
| `lyric` | 2–4 in numbers | full figure | track; one crane | cue at number | song first; bar cuts | heightened |
| `wonder` | 1.0; reading ×1.5 | centred; child height | smooth | bright | melodic | broad |
| `contemplative` | ≥2.5 (ASL ≥10 s) | wide; deep focus | static | natural | ambient only | task-based |

## 4. Procedures

**R1. Set genre and tone (once, 10–15 minutes).**
1. Paste the logline and the first ten pages (or first chapter).
2. Ask: "Propose `genre_primary`, `genre_secondary`, `tone_home` and `tone_range` from D10 §2.1. Quote three lines from the text as evidence for each. Name the set pieces the text already contains."
3. Choose, then ask: "Fill `genre_budgets` from D10 §5 and §6 for a film of [runtime]." Save the film fields (§9).
4. What you get back, for example:
```
genre_primary: thriller        genre_secondary: science_fiction
tone_home: tense               tone_range: [tense, enigmatic, dread, grave]
tone_mix_rule: "comic_dark only as undercurrent, never in camera"
genre_budgets: {startle: 1, false_startle: 0, sting: 1, number: 0, slow_motion: 0}
```
5. If any value has no quoted line behind it, ask again for that value only.

**R2. Tag each scene (per sequence, 5 minutes).**
1. Paste the scenes and the film fields.
2. Ask: "For each scene give `tone`, `tone_undercurrent` (or none) and any `tone_shift` with its beat ID, each with the exact line that justifies it. Flag any `tone` outside `tone_range`, and any `tone_undercurrent` that is neither in `tone_range` nor named in `tone_mix_rule` (TN7). Do not change the text."
3. Accept or correct each tag.

**R3. Move the defaults (per scene, with the breakdown).**
1. Ask: "Apply D10 §2.2 for this scene's tone to the A2/A4/B1/B2 defaults. List every default that moves, the new value and why. Keep turning points and text marks unchanged (principle 1)."
2. Strike any change that fails the cliché test (B2): if its reason would fit any film of the genre, it goes.
3. You get a three-column list, `default | new value | why`, for example `sizes | one step wider | comic_dark, CM7`. Nothing in it may touch a turning point.

**R4. Comedy pass (per comic scene).**
1. Ask: "Mark each beat's `comic_role` (setup, repeat, punch, reaction). Find any rule-of-three patterns. Apply CM1–CM10 and give reaction holds in seconds."
2. Watch the animatic once; if a laugh has no room, lengthen the hold, never add a pre-pause (CM2).

**R5. Horror and suspense budget (whole film).**
1. Ask: "List every candidate startle with its three Baird parts (HR2), its ledger mode and its dread hold. Rank them. Keep only the budget (HR1). Mark every shot with lightning, strobes, muzzle flashes or alarms `flash_risk: check` (HR10)."
2. Approve the list. A candidate that loses its place becomes a dread hold with no startle, never a smaller startle.

**R6. Plan a number (per song).**
1. Lock the song; write down its BPM and bar count.
2. Ask: "Split the song into phrases with bar numbers and times. Give one shot per phrase or longer, full figure for dance, cuts on phrase ends (SG2–SG4), and a lip-sync route per sung shot (SG5)."
3. Check the arithmetic once: at 120 BPM a 4-beat bar lasts 2 s, so an 8-bar phrase is 16 s; one clip on a 15 s model is too short, so the phrase needs a hidden cut or a 20–30 s model (SG4).

**R7. Test the genre opener (once per tone, 10 minutes, two draft takes).**
1. Pick one representative shot of the tone.
2. Generate it twice at draft quality: once with the opener, once without, all else identical.
3. Keep the take whose light and pace match the look key (B2). If the opener pulled the light darker or the cutting faster, keep it only with explicit light words after it (GW2), and record the result in `genre_opener`.

## 5. Checklists

**Film** (a "no" needs a fix or a written reason)
1. `genre_primary`, `tone_home`, `tone_range` set, each with quoted evidence?
2. Setting genre kept out of camera choices (P4)?
3. `genre_budgets` set; startle, sting and number lists within them?
4. Film ASL inside the genre's pace range (§3), and inside D13's band moved by `asl_factor`?
5. Genre opener checked against every look key (GW1–GW2)?
6. Banned words absent from every prompt?

**Scene**
1. One `tone`, at most one undercurrent, both passing TN7?
2. Any shift on a turn or drop, one system changed (TN2–TN3)?
3. Defaults moved per the table; turning points unchanged?
4. Comic: no pre-punch pause; reaction holds set; third repeat breaks?
5. Horror: every startle has presence, threat, intrusion; threat never moves the camera?
6. Numbers: song locked; phrase-end cuts; full figure; vocal stem?
7. Flashing shots marked `flash_risk: check`, ≤3 flashes a second?
8. Each convention has a story reason?

**Prompt**
1. Opener identical across the scene?
2. Light words follow any opener that contradicts the look?
3. No emotion or genre adjectives on faces (behaviours only)?
4. No gore, injury, artist or studio names?

## 6. Saying it to AI models

- **A genre word is a bundle the user did not choose.** Google's Veo guide ties "Suspenseful/tense" to "Dark, shadowy, quick cuts", "Horror" to "Dark, unsettling, eerie, gory (though be mindful of content filters)", and "low-key lighting" to "a dark, mysterious mood" [V]. So the mystery opener says "calm, puzzling", not "mysterious".
- **Openers per tone** (paste identically into every prompt of a scene; change only at a `tone_shift`): `grave` "A quiet, serious drama scene." · `tense` "A tense dramatic thriller scene." plus explicit light words · `dread` "A quiet, eerie suspense scene." · `enigmatic` "A calm, puzzling mystery scene." · `comic_light` "A warm, light comedy scene." · `comic_dark` "A dry, deadpan dark comedy scene." · `romantic` "A tender romantic drama scene." · `kinetic` "A fast, physical action scene." · `lyric` "A joyful musical scene with singing." · `wonder` "A bright, gentle family animation scene." · `contemplative` "A slow, quiet, observational scene in one long take."
- **Fix a clashing bundle with light words**: "A tense dramatic thriller scene. Even, flat daylight from ceiling panels; clear air; background in focus." Write visible light, never ratios (B2).
- **Horror:** avoid "horror", "gory" and injury words; implied violence "generally clears review when the prompt avoids literal injury language" (tester quoted in C3 §14) [V-sec]. Fewer Veo clips than asked means output "is being blocked": reword. "Horror" alone being blocked is [U].
- **Comedy:** never "funny", "comedic", "hilarious"; write behaviour ("keeps a straight face; blinks once").
- **Animation:** describe shapes and colour, not "Pixar-like" or "classic Disney" (both in Google's own guide [V]), because brand looks need clearing (D4).
- **Test every opener per model version (R7).** C3's SC15 feed prompts ("Fixed camera.") have no opener: that is the "without" take.

## 7. The Catch

**Decisions made (proposals [J]; the user confirms at the story plan)**
- Film fields: `genre_primary: thriller`, `genre_secondary: science_fiction`, `tone_home: tense`, `tone_range: [tense, enigmatic, dread, grave]`, `tone_mix_rule` "`comic_dark` only in dialogue and physical business (Jude's jokes, Iona's flat replies, Eli's cap); never in camera", `genre_budgets.startle: 1`.
- **SC15 (the figure on the tablet):** `tone: enigmatic`, `tone_undercurrent: dread`, because the cup moves "Into his reach" and the figure lifts the arm "As carefully as a nurse". Either way: static high-corner feed; the figure appears by a frame jump, never by a camera move. Mystery: feed shots 4–6 s; CLICK small and clean; pump band-limited but "clear and complete" (A4 WE3); opener "A calm, puzzling mystery scene seen on a security feed." Horror (not chosen): 6–8 s hold on "An empty chair beside the bed. The sealed door behind it."; loud off-frame CLICK; crushed blacks.
- **SC16 holds the film's one startle:** presence (Iona), threat ("Behind her: a pump. Three uneven strokes."), intrusion ("She turns." / "The figure stands between her and the sealed door. Taller than the door."), on B1's single looming frame. Mystery key shot: "Iona runs the picture back. Stops it on the hand under his arm."
- **SC10 (the kitchen):** `tone: tense`, `tone_undercurrent: comic_dark`, limited to B2 ("Was your appendix on the left?" / "They didn't let me watch.") and B5 (the cap: "Twists it the other way. It comes off."). No size changes: TP1 at B7 ("Not mint.") keeps Iona's tightest close-up. Saye's uncontracted lines ("That is your left.") are deadpan on the page; her only contraction is the recorded "They're here. Nell is here."
- **The Long Places ch. I as slow cinema:** `tone_home: contemplative`, music `source_only`, target ASL 12–25 s. Threshold: wide static 20 s; medium static 50 s on "At the mouth of Kırk Oda the air shaft breathed." (one out-breath and pause); B1 Ex7 warmth shot, 75 mm, 40 s+. Long takes are chained clips joined where nothing moves (A4 AI6), or a still plate with a small generated loop. Uncanny beats stay `enigmatic`: no stings, no startles.

**Flagged for the user**
1. SC15: mystery (recommended) or horror. Horror would also require changing A4 WE3's "clear and complete" pump.
2. SC10: keep the comic undercurrent or cut it.
3. *The Long Places*: slow cinema (~400–500 shots) or D2's 4–5 s ASL (1,200–1,500 shots); fewer shots do not cost less.

## 8. Conflicts and open questions

- **A2 "cut on the punch word" vs CM1 (cut after).** Cut on the word only in verbal banter shot in singles; otherwise CM1.
- **D13 rhythm class `contemplative` (6 s) vs D10 tone `contemplative` (×2.5+).** Together they give 15 s a shot; D13 suggests renaming its class `still_pace`. Builder decides.
- **ASL formula.** Blueprint sets `target_asl_s` "from the rhythm shape, the tone and card 13, never from `rhythm_class`"; D13 multiplies rhythm-class ASL by `asl_factor`. Pick one.
- **Genre fields.** Blueprint has one `genre`; D10 proposes `genre_primary` + `genre_secondary` and the other proposals above.
- **Undercurrents (new, 09-28).** Blueprint FILM-12 checks only `tone`; TN7 now covers undercurrents. Proposed `undercurrents_allowed[]` so code can check it.
- **Performance scale vs D15 display level (new).** D15 owns the shot-level 1–3; `performance_scale` only caps it; `broad` means level 3 plus bigger gesture (B5), not a bigger face.
- **Flash field (resolved).** D10's `flash_check` withdrawn; D18's `flash_risk` and `access.checks` reused.
- **Flash area (resolved).** D18 §3.5 marks the UK area limit [U]; S27 gives >3 flashes/s over >25% of the screen [V-sec]; D18 can upgrade.
- **Budgets overlap.** B1 `extreme_budgets`, blueprint `SOUNDPLAN.device_budget` and `genre_budgets`: merge into one ledger.
- **C3's default opener** "A tense dramatic thriller scene." suits dark scenes only; daylight scenes need light words after it (GW2).
- **Preset names.** D3 lists `earpiece_radio`, `small_speaker`; D9 has `device_speaker`, `earpiece`. D10 uses D9's; D3 should follow.
- **C3 example IDs.** C3 labels the tablet shots 14-05A/B under its own numbering; under C5 IDs they sit in SC15.
- **Dance.** D11 has no dance notation; SG3's counts line is a stopgap; Wan-Dancer is untested here.
- **Weak evidence.** ASL targets, factors, budgets [J]; Baird, Ofcom, Flanagan second-hand; "horror" alone tripping filters [U].

## 9. Section map

| Need | File section |
|---|---|
| Terms; performance scale to display level | §0 |
| Principles P1–P8 | §1 |
| Tone values, defaults table, mixing rules TN1–TN7 | §2 |
| Pace anchors and ten genre profiles | §3 |
| Comedy CM1–CM10; horror HR1–HR11; numbers SG1–SG8 | §4–§6 |
| Genre words and model bias GW1–GW7 | §7 |
| Recipes R1–R7; fields; checklists; failure modes | §8–§11 |
| Worked examples (SC15, SC10, *The Long Places*) | §12 |
| Conflicts; sources S1–S28 | §13; Sources |
