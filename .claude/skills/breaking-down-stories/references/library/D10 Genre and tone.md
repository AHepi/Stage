# D10. Genre and Tone Conventions: How Genre Shifts Camera, Light, Cutting, Sound and Performance Defaults

*Library file D10. Written 2026-09-27. Test sources: "The Catch" (screenplay, workshop revision of 25 September 2026) and "The Long Places" (prose, revised final).*

> **What this file is for**
> 1. The other files were tuned on a clinical SF thriller and a literary novella. This file tells the pipeline how their defaults move when the next story is a comedy, horror, romance, musical, action film, children's animation or slow film.
> 2. It adds one `tone` field per film and per scene, and a table saying how each tone value shifts pace, framing, movement, light, sound, performance and prompt wording.
> 3. It gives working rules for comedy timing, horror and suspense, and song sequences, plus ten short genre profiles with sources.
> 4. It explains how genre words in prompts pull models toward stock looks and filters, and what to write instead.
> 5. Worked examples: *The Catch* SC15 as horror and as mystery; SC10 as black comedy; *The Long Places* ch. I as slow cinema.

**Evidence labels.** [V] read on the named source on 2026-09-27; [V-secondary] read on a named secondary source that quotes the original; [U] unverified (search excerpt or general knowledge); [J] this file's judgment. Every ASL range, factor and budget below is [J] unless marked: the sources give anchors, not rules.

**Builds on, does not repeat:** A2 §4 (six conflict types, including *comic*), A1 §5 (nonrealism), B1 §4.4 (anamorphic by tone) and P5 budgets, B2 §12 (clichés and the AI house look), A4 §6 (suspense, ledger, ruptures) and §7 (sound), C3 §14 (filters), D3 (voice, lip sync), D9 (music policy, cues, motifs), D13 §5 (rhythm classes). D11 (action beat maps, stunts, and capturing fight choreography by mime, phone or motion capture) now exists and takes `kinetic` set pieces; it has nothing on dance, so dance notation stays an open gap (§6, §13).

**Names.** The build blueprint (`design/blueprint.md`) wins over this file on field names. It already carries `tone`, `tone_undercurrent`, `tone_shift`, `tone_home`, `tone_range` and `tone_mix_rule`; the other §9 fields are proposals (§13). *Checked 2026-09-27: every source was re-read; corrections are marked "(corrected)". Second adversarial check 2026-09-28: 25 sources re-fetched (S21 still blocked), two added, every quoted line of* The Catch *matched verbatim against the workshop revision; changes from this pass are marked "(checked 09-28)".*

**Scene numbers** follow C5's IDs (SC10 = A2's sc10).

---

## 0. Words this file uses (one word per concept)

| Word | Plain meaning |
|---|---|
| **Genre** | The kind of promise a story makes to its audience (a scare, a laugh, a love story), shown by its typical events. |
| **Tone** | The attitude the telling takes toward events, moment to moment: how the audience is asked to feel. B1's "register" is this file's tone. |
| **Home tone** | The film's default tone, set once. |
| **Undercurrent** | A second tone running under a scene's main tone, carried by lines or performance, not by the camera. |
| **Tone shift** | A change of tone inside a scene or at a cut. |
| **Set piece** | A scene type the genre promises (the chase, the jump scare, the duet). |
| **Convention** | A choice the audience expects from the genre. |
| **Cliché** | A convention used without a story reason (B2 test: its WHY line fits any film). |
| **ASL** | Average shot length: running time ÷ number of shots (A4). |
| **Punch** | The word, action or sound that completes a joke. |
| **Hold / reaction hold** | A hold lets a shot run on after its action (A4); a reaction hold is the seconds held on a face after a punch or a scare. |
| **Rule of three** | A pattern stated twice and broken on the third. |
| **Deadpan** | Comedy played with no visible reaction by performer or camera. |
| **Startle** | A jump scare: a sudden intrusion, usually with a loud sound. **False startle**: the intrusion is harmless. |
| **Dread** | Sustained fear of something not yet shown. |
| **Sting** | A sudden loud music or sound hit on one moment. |
| **Number** | A song or dance sequence. |
| **Bar / BPM** | A bar is a group of beats (usually four); BPM is beats per minute. |
| **Slow cinema** | Films built on very long takes, little plot and attention to ordinary time. |
| **Genre opener** | The first sentence of a video prompt naming genre and tone (C3). |
| **Look bundle** | The light, color and cutting a model attaches to a genre or mood word. |
| **Performance scale** | How big acting is: `underplayed`, `naturalistic`, `heightened`, `broad`. A scene-level default; each shot's actual size is D15's **display level** (1–3, how much inner pressure reaches the body). Mapping [J]: `underplayed` = 1; `naturalistic` = 1–2; `heightened` = 2–3; `broad` = 3 with enlarged gesture and silhouette (checked 09-28: added to match D15 and the blueprint's "performance display level"). |

---

## 1. Core principles

1. **Tone moves the dial, not the map** [J]. Tone changes baselines (pace, size, light, sound, acting). It never changes which beat is the turning point (A2), what the text marks (A4), in-story footage or physics rules (B1 R22–R23).
2. **One home tone per film, one main tone per scene** [J]. A second tone is an undercurrent or a shift at a named beat. Unplanned mixing reads as a mistake.
3. **Genre is expectation; conventions are tools, not duties** [J]. Keep a convention when it serves a beat; drop it when it would be a cliché.
4. **Setting genres do not set the camera** [J]. Science fiction, fantasy, westerns, war and period films set world and character design (B4, B5). Their camera, light and cutting come from their tone. *The Catch* is SF in world, thriller in tone.
5. **Extremes are budgeted by genre** [J]. Horror spends startles; comedy spends broken patterns; musicals spend numbers; action spends slow motion and big hits, on top of B1 P5 and A4 P10.
6. **Genre words in prompts are not neutral** [V, §7]. A tone word brings its own lighting and cutting. Name the look you want after it, or drop it.
7. **When tones mix, the camera plays the more serious one** [J]. The lighter tone rides on lines, props and performance. Chaplin's line sets the size logic: "Life is a tragedy when seen in closeup, but a comedy in long-shot" (Quote Investigator finds "substantive evidence that Charlie Chaplin made this remark although the crucial citations were indirect", chiefly via the critic Richard Roud) [V, S23] (checked 09-28: spelling as on S23).
8. **Pace data are anchors** [V/J]. Published ASLs describe whole past films; scene targets here are [J] starting values, and the animatic decides (A4 §6.1).

---

## 2. The tone field and how it moves every file's defaults

### 2.1 Tone values

Set `tone_home` once (R1); tag each scene with one `tone` and an optional `tone_undercurrent`.

| Value | Plain meaning | Typical genres |
|---|---|---|
| `grave` | Serious, attentive, no threat | Drama |
| `tense` | Danger with stakes and often a clock | Thriller, suspense |
| `dread` | Fear of an unseen threat to body or self | Horror |
| `enigmatic` | A puzzle the audience wants solved | Mystery |
| `comic_light` | Warm comedy; no one is truly hurt | Comedy, family |
| `comic_dark` | Pain or death treated flatly, for laughs | Black comedy |
| `romantic` | Two people moving toward each other | Romance |
| `kinetic` | Bodies, speed, impact, skill | Action |
| `lyric` | Feeling too big for speech becomes song or dance | Musical |
| `wonder` | Safe discovery, clear feelings | Children's animation |
| `contemplative` | Time itself; the everyday observed | Slow cinema |

### 2.2 The defaults shift table

Read a row as "from this scene's tone, start here". Column heads name the files whose defaults move. `asl_factor` multiplies D13's rhythm-class ASL [J]. A departure gets one line in `notes` (A4).

| Tone | `asl_factor` (D13, A4) | Size and lens (A2, B1) | Movement (B1) | Light (B2) | Sound and music (A4, D9) | Performance (B5, D3) | Opener (C3, §7) |
|---|---|---|---|---|---|---|---|
| `grave` | 1.0 | Approach progression; normal lens; tightest size on the turn | Static; ≤1 push-in | Motivated, ~4:1 | Sparse music that must not state subtext | Naturalistic | "A quiet, serious drama scene." |
| `tense` | 0.9, but hold on the unaware (A4 S2) | Sizes tighten across the scene; longer lens for watching | Static baseline; handheld only at loss of control (B1 R17) | 4:1–8:1, practical sources | Beds, a rising or ticking sound; score sparse | Contained | "A tense dramatic thriller scene." plus explicit light words |
| `dread` | 1.3 before a startle; the startle shot under 1 s | Wides with empty areas; deep focus; threat partial or off frame | Static or very slow push toward empty space; the threat never causes a move | 8:1+, dark but readable | Sound before sight; rough textures; stings only on budgeted startles | Underplayed until the break | "A quiet, eerie suspense scene." (§7) |
| `enigmatic` | 1.1 | Objective framings; evidence inserts held to read (A4 R8) | Static; move or rack only on a noticing beat | Readable, low to medium contrast | Minimal; motifs as clues, clean | Naturalistic, withheld | "A calm, puzzling mystery scene." |
| `comic_light` | 0.9 in banter; reaction holds added (§4) | Wides and two-shots holding both bodies; normal-to-wide lens; deep focus | Static; any move timed to the reveal | High-key, ~2:1 | Timed effects over music; no mickey-mousing | Heightened to broad | "A warm, light comedy scene." |
| `comic_dark` | 1.1 (deadpan holds) | Frontal, centered, symmetrical mediums and wides | Static; no push-ins | Even, flat, neutral | No music under jokes; one timed effect | Deadpan (underplayed) | "A dry, deadpan dark comedy scene." |
| `romantic` | 1.2 | Two-shots and matched close singles; long lens along the line between them (B1 R13); shallow focus; anamorphic may fit (B1 §4.4) | Slow, minimal; one push-in at the turn | Soft, warm key; low to medium contrast | A theme is allowed if the music policy is `scored` | Intimate, naturalistic | "A tender romantic drama scene." |
| `kinetic` | 0.5 at peaks | Calm geography wide first (A4 C6); wide lens near the action; each blow whole in frame | Follow or lead; one move per clip (B1) | Hard, high contrast; flashes ≤3 per second (§5) | Percussive; hits synced; music drops at the rupture | Physical, heightened | "A fast, physical action scene." |
| `lyric` | Numbers: 2–4 | Full figure for dance; near-frontal for singing | Track with the performer; one crane allowed | A light cue when the number starts | Song locked first; cuts on bars (§6) | Heightened | "A joyful musical scene with singing." |
| `wonder` | 1.0, reading times ×1.5 | Clear, centered staging; eye level at the child's height | Smooth, motivated | Bright, saturated | Melodic score; music matched to action tolerated | Broad, readable faces and silhouettes | "A bright, gentle family animation scene." |
| `contemplative` | ≥2.5, never under 10 s ASL | Wide or held medium; deep focus; the frame outlasts the action | Static; slow tracking only | Natural, source-true, changing in real time | Ambient and field sound; no score, or source only | Underplayed, task-based | "A slow, quiet, observational scene in one long take." |

**How to read the table (plain terms).** *ASL factor*: the multiplier on the scene's usual average shot length (0.5 halves it; 2.5 makes shots two and a half times longer). *Contrast ratio* (4:1, 8:1): how much brighter the lit side of a face is than the shadow side; 2:1 is soft and bright, 8:1 is dark and dramatic (B2's contrast bands). In prompts, write the visible result ("half her face falls into shadow"), never the ratio, because models follow described light better (B2). *Deep focus*: near and far both sharp. *Push-in*: the camera moves slowly toward the subject. *Stem*: one isolated part of a music mix (the voice only, the drums only).

**Where the moves land.** D13 already applies `asl_factor` (D13 §5 and R23, which also moves its warning band). The blueprint's `_config/rules/tone_defaults.json` holds this table. D11 takes over `kinetic` set pieces. The Performance column sets the ceiling for D15's display level (§0 mapping), never the level on a turn shot, where D15's closer-is-lower rule wins. Flash safety applies to every tone: D10 HR10 states the limits, D18 (shot field `flash_risk`, rule D18-R35) does the check (checked 09-28: D18's own IDs). B4 (motifs), D4 (rights) and D17 (world research) do not move with tone.

**Worked reading (one row).** SC10 tagged `comic_dark`: D13's ASL for its rhythm class × 1.1; sizes one step wider, frontal and centered; no push-ins; flatter light, more fill; no music under the jokes; Saye plays deadpan while Iona stays naturalistic; opener "A dry, deadpan dark comedy scene." The turn at B7 keeps its place (principle 1).

### 2.3 Tone mixing and shifts

- **TN1.** If a scene needs two tones, then set one as `tone`, the other as `tone_undercurrent`, and keep camera, light and cutting on the main tone, because the camera can play one tone at a time (principle 7).
- **TN2.** If the tone changes inside a scene, then put the shift on a turning point or a drop (A2 R10) and record `tone_shift`, because a shift anywhere else reads as a wobble.
- **TN3.** If the tone shifts, then change one visible system on that beat (the size ladder, light, music on or off, camera behavior) and hold it, because a shift is a rupture (A4 §6.8) and needs a taught pattern before it.
- **TN4.** If two adjacent scenes have contrasting tones, then cut hard and contrast their ASLs (A4 §6.9), because the gap does the shifting.
- **TN5.** If a comic beat falls just before a planned peak, then play it small (undercurrent only); just after a peak, let it land, because a laugh after a peak releases tension and one before it spends it [J].
- **TN6.** If over a third of scenes carry an undercurrent, then re-check `tone_home`, because the film may be another genre.
- **TN7.** If `tone` falls outside `tone_range`, or `tone_undercurrent` is neither in `tone_range` nor named in `tone_mix_rule`, then flag it for the user, never silently fix it, because tone is the writer's call (A2's flag-never-fix rule). *Example:* *The Catch*'s proposed range excludes `comic_dark`, but its `tone_mix_rule` names it as an undercurrent, so SC10's undercurrent passes (checked 09-28: undercurrents were not covered; the blueprint's FILM-12 check reads only `tone`).

---

## 3. Ten genre profiles

Pace ranges are scene-level ASL targets [J], set against these anchors.

**Pace anchors.**
- Bordwell (2007): "today it isn't uncommon to find films with average shot lengths of 2-4 seconds….and not just action movies." In the opening portion of the same scene (two men on the sidewalk), *The Shop Around the Corner* (1940) averages "about 82 seconds" a shot and *You've Got Mail* (1998) "about 4.1 seconds"; in the café portion, about 21 s against 4.3 s [V, S1] (corrected: the 82 s figure is one portion of the scene, and Bordwell says 2–4 s is common, not universal).
- Cutting and colleagues (160 English-language films, 1935–2010, five genres: action, adventure, animation, comedy, drama): ASLs fell from "about 10 s in the 1930s and 1940s" to "below 4 s after 2000", and "The trend was reliable for all five genres". Their extremes: *The Seven Year Itch* (1955) 26.2 s, *Rocky IV* (1985) 2.2 s. Motion rose, "most pronounced for action and adventure films"; films got darker, while animation stayed "generally brighter than other genres" [V, S3]. In climaxes shot durations fall and motion rises, then shots lengthen in the epilogue, and the image brightens through climax and epilogue ("epilogues are often the brightest sequence of a movie") [V, S4].
- Cinemetrics data summarized by Follows (1997–2016, crowd-sourced, "always a bit of an inexact science"): 1,045 shots per film on average; action has the most shots (1,913), documentaries the fewest (491), then "music-based movies" (814) and romance (869); ASL action 4 s, adventure 5.1 s, sci-fi 6.2 s, horror 15.7 s [V, S2] (corrected: "music-based movies", not "musicals"). The horror figure is probably skewed by a few long-take films [J]; do not use it as a target.

**3.1 Drama (`grave`).**
- Promise: people change under pressure.
- Pace: 4–8 s.
- Camera: B1 defaults, eye level, approach progression.
- Light: motivated, medium contrast.
- Music: sparse; must not state subtext (A4 §7.6).
- Performance: naturalistic.
- Set pieces: confrontation, confession, farewell.
- Clichés: crane-up on sad moments (B1); rain on grief; piano under every feeling.

**3.2 Thriller and suspense (`tense`).**
- Promise: danger with a clock; the audience often knows more than the character (A4 S1).
- Pace: 2.5–5 s; peaks 1–2 s; long holds on the unaware.
- Camera: longer lens for watching; singles tighten; handheld only at loss of control.
- Light: 4:1–8:1 from practical sources.
- Music: pulses and ticking, or none (D9 §4.8).
- Performance: contained.
- Set pieces: search, hiding, ambush, chase, deadline.
- Clichés: Dutch tilt for "tension" (B1 R8); teal-and-orange night (B2); a countdown in every scene.

**3.3 Mystery (`enigmatic`).**
- Promise: a fair puzzle; the audience knows what the investigator knows, and both know less than the truth (A4 ledger mode `mystery`: "Audience knows the same"; point of view kept) (corrected: A4's "knows less" row is `surprise`).
- Pace: 4–7 s; evidence held to its reading minimum.
- Camera: the investigator's point of view kept (A4 checklist); clues shown once, calmly (A4 S5). Lens [J]: normal (about 40–58 mm, B1), so nothing is distorted into a false clue.
- Light: readable.
- Music: minimal; a motif may be a clue.
- Performance: withheld.
- Set pieces: discovery, interrogation, the recording replayed, the confirming reveal (A4 S4).
- Clichés: an explaining flashback montage; a sting or zoom on each clue.

**3.4 Horror (`dread`).**
- Promise: fear for body and self from a threat that breaks rules.
- Pace: dread 5–10 s, the startle shortest. Where's the Jump counts "around 10 scares per movie" in recent films (crowd data) [V, S5].
- Camera: empty space in frame; the threat partial and sound-first; low angle only face to face and afraid (B1 §14). Lens [J]: wide (about 14–35 mm, B1) with deep focus, so the room behind the character stays searchable.
- Light: low-key but readable (B2 "too dark to follow").
- Music: drones, silence, rough textures. In Blumstein and colleagues' sample (adventure, drama, horror and war films), "Horror films suppressed abrupt frequency transitions and musical sidebands, but had more non-musical sidebands, and noisy screams than expected" [V, S6] (checked 09-28: full sentence; the roughness is noise-like, not simply a sudden pitch jump); scream-like film music imitates "a key feature of human screams (roughness)" [V, S7].
- Performance: underplayed until the break.
- Set pieces: the stalk, the startle, the false startle, the monster reveal, the last survivor's escape.
- Clichés: the cat that causes a false scare; the mirror-cabinet scare; flickering tubes and a cold blue shift for the monster (B2); gore close-ups (§5).

**3.5 Comedy (`comic_light`, `comic_dark`).**
- Promise: pleasure in a pattern and its breaking.
- Pace: banter 2.5–4 s; gag frames 4–8 s.
- Camera: wide frames holding both bodies (A2 comic); things entering and leaving frame (§4); frontal symmetry for deadpan. Lens [J]: normal to slightly wide with deep focus, so cause and reaction share one sharp frame.
- Light: high-key. Google's guide pairs "high-key lighting" with "a bright, cheerful scene" [V, S8].
- Music: timed effects over score. Mickey-mousing (music copying every movement) is "somewhat out of favor today, at least in serious films, because of overuse" [V, S9].
- Performance: heightened or broad; deadpan for dark comedy.
- Set pieces: the escalating misunderstanding, the physical gag, the dinner that goes wrong.
- Clichés: record scratch and freeze-frame narration; comic pizzicato; everyone laughing in reaction shots; mugging (AI faces "tend to over-act", A4 §4.2; B5 failure 8).

**3.6 Romance (`romantic`).**
- Promise: two people move toward each other against obstacles.
- Pace: 5–8 s; the first touch as one long hold.
- Camera: two-shots versus singles as the relationship's gauge (A2 R6, B1 R4); long lens along the line between them; shallow focus.
- Light: soft and warm; golden hour once, for a story reason.
- Music: a theme if the policy allows (D9 theme register).
- Performance: intimate.
- Set pieces: the first meeting, the interrupted kiss, the fight, the grand gesture.
- Clichés: candles for romance (B2); the rain kiss; the slow-motion run; golden-hour background blur in every frame (AI house look).

**3.7 Action (`kinetic`).**
- Promise: skill and bodies in danger, in clear space.
- Pace: fights and chases 1.5–3 s (*The Catch*'s fall: ASL ~1.4 s, A4 WE1); whole action films average 4 s [V, S2].
- Camera: geography shown calmly first (A4 C6). Bordwell's "pause/burst/pause pattern", written about Hong Kong martial-arts fights: "a rapid thrust or parry ... There follows a slight pause, often at the moment a blow is blocked ... Then comes another burst of activity" [V-secondary, S10]. Applying it to other action is [J]. Hold the pauses; keep each blow whole in frame. Beat maps and coverage: D11.
- Light: hard; flashes limited (§5 HR10).
- Music: percussive; hits synced; drop it at the rupture.
- Performance: physical.
- Set pieces: chase, fight, escape, heist, countdown.
- Clichés: walking from an explosion in slow motion; shaky camera to fake energy (B1 "handheld as realism"); every hit in slow motion; orange sparks. Filters block injury words and graphic frames, so split violence into cause, reaction and aftermath (C1 R9) (corrected: C1 R9 is about violence in general, not "weapon plus contact").

**3.8 Musical (`lyric`).**
- Promise: song and dance say what speech cannot.
- Pace: numbers in long takes. Astaire "insisted that a closely tracking dolly camera film a dance routine in as few shots as possible, typically with just four to eight cuts, while holding the dancers in full view at all times" [V, S11].
- Camera: full figure for dance; near-frontal for singing. Lens [J]: normal or wide enough to keep feet and hands in frame while tracking.
- Light: a cue marks entry into the number.
- Music: the song comes first.
- Performance: heightened. Nonrealism allows frontal, iconic framing (A1 §5).
- Set pieces: the "I want" song, the duet, the ensemble number, the reprise.
- Clichés: cutting on every beat; feet with no body; mouths off the vocal (AI). Details in §6.

**3.9 Children's animation (`wonder`).**
- Promise: safe adventure with clear feelings.
- Pace: 3–6 s, reading times ×1.5 [J]. Nine minutes of a fast-paced cartoon lowered sixty 4-year-olds' scores on executive-function tasks (self-control, working memory) against an educational cartoon or drawing [V, S12]. A 2024 systematic review of 15 studies says, for executive function, that "the impact of exposure to fantastical TV programs on children's EF remains unclear, while the influence of pacing can be more certainly dismissed"; its abstract highlights "the negative effect of fantasy on inhibitory control" [V, S13] (corrected quote). Set children's pace by comprehension, and treat impossible events as the thing to ration.
- Camera: eye level at the child's height; screen direction kept strictly. Lens [J]: normal; avoid wide-lens face distortion close up.
- Light: bright (Cutting: animation stayed brighter than other genres [V, S3]).
- Music: melodic; music matched to action tolerated.
- Performance: broad, with readable silhouettes (B5).
- Set pieces: the chase, the song, the lost-and-found, the lesson.
- Clichés: constant noise; jokes aimed over children's heads; studio-name looks (§7 GW5).

**3.10 Slow cinema (`contemplative`).**
- Promise: attention to time and the everyday; meaning left open.
- Pace: ASL 10 s or more. *Werckmeister Harmonies* is "composed of thirty-nine languidly paced shots" in 145 minutes [V, S14], an ASL of about 223 s [J arithmetic]. Flanagan (2008) names the style's features as "the employment of (often extremely) long takes, de-centred and understated modes of storytelling, and a pronounced emphasis on quietude and the everyday" [V-secondary, S24] (corrected: the quote is not on S15; S15 only names the essay).
- Camera: static; deep focus; hold after people leave frame. Lens [J]: wide to normal, placed far enough back that people are part of the place.
- Light: natural, changing in real time.
- Sound: slow films "opt for ambient noises or field recordings rather than bombastic sound design" (*The Guardian*, quoted on S15) [V-secondary, S15].
- Performance: underplayed, task-based.
- Set pieces: a task in real time, the walk, the meal, the wait.
- Clichés: long takes with nothing planned inside them; drone landscapes; piano over fields.

---

## 4. Comedy timing (expands A2's comic rules)

A2 gives (§4 table and rule 15): wide frames holding both bodies, cut on the punch word, then hold for the laugh, no sympathy close-ups ("Compassion kills laughs"). Add:

- **CM1.** If a line or action is the punch, then let it land inside a frame that holds both the cause and the victim, and cut after it to the reaction, because the laugh lives in the reaction (A2 R5) and the setup must stay visible.
- **CM2.** If a punch is being timed, then add no pause before it and put all the timing after it (the reaction hold, CM3), because the one measured study found no pre-punch pause in recorded joke-telling. Attardo and Pickering tested the "common assumption" that "punch lines are preceded by pauses" on twenty joke performances: "Our data show no evidence supporting this claim". Speakers also "do not significantly raise or lower their speech rate at and around the punch line" [V, S16]. The study measured spoken joke-telling, not film; carrying it to editing is [J]. Timing lives after the punch and in the edit.
- **CM3.** If a punch lands, then hold the reaction: 0.5–1.5 s in light comedy; 2–4 s in deadpan, where the missing reaction is the joke [J]. Never fill the hold with music, because music tells the audience to laugh.
- **CM4.** If a gag repeats (rule of three), then frame the first two statements identically (same setup, size, lens and duration) and break only the third, in size or in one changed element, because the pattern must be learned before it can break (A2 R2, refined for comedy).
- **CM5.** If the scene is deadpan, then frame frontal, centered, static and symmetrical at medium or wide, with even light, no push-in and no music, because the camera must not comment any more than the face does.
- **CM6.** If the joke is a reveal, then keep the frame static and let the thing enter or leave it. Edgar Wright's comedy is analyzed as "Things entering the frame in funny ways" and "People leaving the frame in funny ways" [V, S17]. A moving camera tells the audience where to look before the joke.
- **CM7.** If a moment could read as pain or as comedy, then let size decide: close for pain, wide for comedy (Chaplin, principle 7).
- **CM8.** If a joke needs sound, then use one sync effect on the exact frame ("The perfectly timed sound effect", S17), because a precise sound beats a comic cue. No laugh track.
- **CM9.** If a cutaway gag (a hard cut to another place or time that contradicts the line) is tempting, then use it only when the script writes it, because an unwritten cutaway adds story the text does not have [J]; A4 T5 makes the matching point for devices, which should not appear late in a film that has not used them (corrected reference).
- **CM10.** If shots are generated, then prompt behaviors ("keeps a straight face; blinks once") and give reaction shots 1.5 s handles, because AI faces tend to over-act (A4 §4.2) and comic timing is set in the edit. In fast banter, one speaker per clip; the other plays off screen (A2 R27).

---

## 5. Horror and suspense (extends A4 §6)

- **HR1.** If the film is horror, then budget startles at about one per 10 minutes, at most three in a short film, false startles included, because recent features have "leveled off at around 10 scares per movie" in Where's the Jump's 250-film database, while 1960s–70s films used "just one or two" [V, S5], and each must stay rare [J]. *Example:* a 20-minute short gets at most two startles; a 90-minute feature about nine.
- **HR2.** If a startle is placed, then build it from Baird's three parts: "a character presence", "an implied off-screen threat" and "a disturbing intrusion into the character's immediate space" (Baird sampled 100 American horror films) [V-secondary, S18]. Missing a part makes it a loud noise, not a scare. The intrusion need not be the threat itself: Baird notes false alarms still startle, which is why false startles count against the budget.
- **HR3.** If a startle is placed, then precede it with a dread hold at least 3× the local ASL and make the startle shot the scene's shortest (A4 R4), because the contrast is the scare [J].
- **HR4.** If a threat should grow, then it is heard before it is seen, placed in space (A4 SND1–2). Delay showing the source in sync to the film's turn, because a seen source loses power.
- **HR5.** If the script withholds the threat, then keep it at the frame edge, in darkness or behind an obstruction, and never tilt or pan to it (B1 P7, A4 S3). Generalized from B1's figure rule: in `dread`, the threat never causes a camera move.
- **HR6.** If building dread, then leave empty areas where the threat could appear (B1 translation menu: "static wide with empty areas"), because the audience searches the space.
- **HR7.** If a sting is proposed, then allow it only on a budgeted startle, never on a reveal the script already marks (D9 §7), and make it rough rather than merely loud (S6, S7), because such devices wear out with use (A4 P10).
- **HR8.** If deciding horror against mystery, then set the ledger mode first (A4): `suspense` (the audience knows more: it sees the danger; hold on the unaware), `mystery` (the audience knows what the character knows; keep the point of view) or `surprise` (the audience knows less; once, fair) (corrected to A4 §6.5). Horror uses suspense plus budgeted surprise; mystery plays new images as evidence.
- **HR9.** If harm happens, then show cause, reaction and aftermath, never injury detail (C3 §14). Runway's policy bars "Gore, such as dismemberment, beheadings, mutilations, and exposed organs/bones/muscle" [V, S19].
- **HR10.** If a scene has lightning, strobes, muzzle flashes or alarms, then keep flashes to three or fewer in any second. WCAG 2.3.1: "Web pages do not contain anything that flashes more than three times in any one second period" unless below the thresholds [V, S20]. UK TV regulation (Ofcom) restricts "the flash rate to three per second or less" and also limits the screen area that may flash, as reported by the Epilepsy Society [V-secondary, S25]. A 2024 review of international guidelines gives Ofcom's area figure: a flash sequence fails when it has more than three flashes in one second *and* the flashing covers more than 25% of the displayed screen; a flash counts when luminance changes by 20 cd/m² or more while the darker state is under 160 cd/m², and any change to or from saturated red counts [V-secondary, S27] (checked 09-28: area figure added). The Ofcom PDF itself (S21) still refused automated access on 2026-09-28. *Plain terms:* a "flash" is a pair of opposite brightness changes (bright-dark-bright); cd/m² measures screen brightness. *Rule for makers:* keep every shot at three flashes per second or fewer, whatever their size, because that passes both WCAG and Ofcom. Mark such shots `flash_risk: check` and screen the locked film with a free tool (D18 §3.5, D18-R35); only the commercial Harding test certifies.
- **HR11.** If a startle or peak has played, then give the next scene a release (A4 §6.9), because a second scare on a tense audience lands weaker [J].

---

## 6. Musical and song sequences

*Rule IDs are SG1–SG8 (corrected from MU1–MU8, which clashed with the blueprint's `MU-##` music-cue records, D9).*

- **SG1.** If a scene is a number, then lock the song (tempo, bars, lyric, vocal) before designing shots, because picture is cut to music. D9 §4.3 turns a cue into a generator prompt; D3 covers sung lines. ElevenLabs v3 lists `[sings]` among its "experimental tags" that "may be less consistent across different voices" [V, S26], so D3 prefers a consenting singer or a music model for any real song.
- **SG2.** If cutting a number, then cut on bar lines or phrase ends (every 4 or 8 bars), not on every beat. One beat = 1,440 ÷ BPM frames at 24 fps (120 BPM = 12 frames; one 4-beat bar = 48 frames = 2 s) [J arithmetic].
- **SG3.** If the number is dance, then frame the full figure, track with the dancer and cut rarely (Astaire's four to eight cuts, S11). Never crop the feet in footwork. D11's capture routes (mime, phone video, motion capture) work for dance too, but D11 has no dance notation; until one exists, write each phrase as counts plus one line of movement ("1–4: travel left; 5–8: turn, arms up") [J]. If the dance only has to feel right to the music and no choreography is locked, a music-to-dance model is a shortcut: Alibaba's open-weights **Wan-Dancer-14B** (Apache 2.0, announced 13 July 2026) takes a reference image, a music file and a dance-style prompt (Chinese classical, K-pop, street, tap, Latin) and produces "minute-scale" dance video [V, S28]; third-party write-ups give 720p at 30 fps [U]. It invents the steps, so do not use it where the counts are written; convert 30 fps to the film's rate in the conform (D8), and check the face against the character pack (C2) (checked 09-28: new).
- **SG4.** If a phrase is longer than one clip (most models stop at 8–16 s; FLUX 3 Video and Luma Ray3.2 reach 20 s; Seedance 2.5 and Wan 3.0 reach 30 s, C1 §2 item 4 and rule 11; checked 09-28), then cut on movement (A4 R3), at a phrase end, keeping axis, size and lens, so the dance reads continuous. For a longer unbroken feel, use a hidden cut through a body crossing the lens (A4 §5, "Hidden cut"; built per A4 AI6) (corrected reference; clip range updated).
- **SG5.** If a face sings on screen, then give the mouth the vocal stem only. sync. labs' FAQ: "lipsync-2 is a good default" for songs, sync-3 for best quality, and "be sure to isolate and upload the vocals track, as the instrumental sounds can sometimes interfere" [V, S22]. Alternatively, generate from an audio reference (C1: Seedance, Wan, MiniMax H3).
- **SG6.** If characters move from speech into song, then write one film-level entry rule (e.g., a sound in the world becomes the beat, a light cue follows, and the camera starts to move) and use it for every number, because the audience learns the rule. Performance steps up to `heightened`.
- **SG7.** If labeling a number, then record `number_kind`: `diegetic` (performed in the story world, sourced sound), `integrated` (characters sing as speech) or `fantasy` (an imagined space), because each takes different sound perspective (A4 §7.2) and light.
- **SG8.** If a song is generated, then name no artist or song in the prompt (D9) and log its licence (D9 §4.9, D4).

---

## 7. Genre words and model bias (extends C3 §14)

Google's Veo guide lists mood words with the look each implies [V, S8]:
- "Suspenseful/tense: Dark, shadowy, quick cuts (if implying edit), sense of unease, thrilling."
- "Romantic: Soft focus, warm colors, intimate."
- "Horror: Dark, unsettling, eerie, gory (though be mindful of content filters)."
- "Happy/joyful: Bright, vibrant, cheerful, uplifting, whimsical."

Its lighting examples add two more pairings: "high-key lighting for a bright, cheerful scene" and "low-key lighting for a dark, mysterious mood" [V, S8] (checked 09-28). So "mysterious" also pulls the image dark; that is why the `enigmatic` opener in §2.2 says "calm, puzzling", not "mysterious".

A genre word is a bundle of choices the user did not make.

- **GW1.** If writing the genre opener, then write it after the scene's look key (B2) and check it against the bundle, because the opener pulls light and cutting.
- **GW2.** If the bundle contradicts the look key, then keep the opener and follow it with explicit light words, or drop it. Example: "A tense dramatic thriller scene. Even, flat daylight from ceiling panels; clear air; background in focus." B2 already fixes the AI house look this way.
- **GW3.** If the film is horror, then prefer "A quiet, eerie suspense scene." over "horror". Google's own list attaches "gory" to horror [V, S8]. No primary source says the word "horror" alone is blocked [U]. The risk is the gore the bundle invites. A tester cited in C3 §14 [P47] reports that implied, choreographed or off-screen violence "generally clears review when the prompt avoids literal injury language", and that a genre phrase in the first clause ("choreographed stage combat") "changes what the model is primed to expect" [V-secondary, via C3] (checked 09-28). Test once (GW7) and never use injury words (HR9). If Veo returns fewer clips than asked, Google says some output "is being blocked" (C3 §14): treat that as a refusal and reword.
- **GW4.** If the scene is comic, then do not write "funny", "comedic" or "hilarious"; write the behavior, because comedy words invite mugging [J].
- **GW5.** If the film is animated, then describe the look (rounded shapes, soft saturated color, clean outlines) instead of a studio name, although Google's guide itself offers "Pixar-like 3D animation" and "classic Disney animation style" [V, S8], because a studio name imports a brand look that D4 must clear [J].
- **GW6.** If shots belong to one scene, then paste the same opener into every prompt and change it only at a `tone_shift`, because it works as a look key (C3).
- **GW7.** If an opener has not yet been tested on the current model and version, then make two draft takes of one shot, with and without it, and keep the one closer to the look key (Recipe R7), because models change by version and a guide's word list describes one model only.

---

## 8. Recipes (the LLM does the work; you decide)

**R1. Set genre and tone (once, 10–15 minutes).**
1. Paste the logline and the first ten pages (or first chapter).
2. Ask: "Propose `genre_primary`, `genre_secondary`, `tone_home` and `tone_range` from D10 §2.1. Quote three lines from the text as evidence for each. Name the set pieces the text already contains."
3. Choose, then ask: "Fill `genre_budgets` from D10 §5 and §6 for a film of [runtime]." Save the film fields (§9).
4. *What you get back:* one short block you can check at a glance, for example:
```
genre_primary: thriller        genre_secondary: science_fiction
tone_home: tense               tone_range: [tense, enigmatic, dread, grave]
tone_mix_rule: "comic_dark only as undercurrent, never in camera"
genre_budgets: {startle: 1, false_startle: 0, sting: 1, number: 0, slow_motion: 0}
```
If any value has no quoted line behind it, ask again for that value only.

**R2. Tag each scene (per sequence, 5 minutes).**
1. Paste the scenes and the film fields.
2. Ask: "For each scene give `tone`, `tone_undercurrent` (or none) and any `tone_shift` with its beat ID, each with the exact line that justifies it. Flag any `tone` outside `tone_range`, and any `tone_undercurrent` that is neither in `tone_range` nor named in `tone_mix_rule` (TN7). Do not change the text."
3. Accept or correct each tag.

**R3. Move the defaults (per scene, with the breakdown).**
1. Ask: "Apply D10 §2.2 for this scene's tone to the A2/A4/B1/B2 defaults. List every default that moves, the new value and why. Keep turning points and text marks unchanged (principle 1)."
2. Strike any change that fails the cliché test (B2): if its reason would fit any film of the genre, it goes.
3. *What you get back:* a three-column list, `default | new value | why`, for example `sizes | one step wider | comic_dark, CM7`. Nothing in it may touch a turning point.

**R4. Comedy pass (per comic scene).**
1. Ask: "Mark each beat's `comic_role` (setup, repeat, punch, reaction). Find any rule-of-three patterns. Apply CM1–CM10 and give reaction holds in seconds."
2. Watch the animatic once; if a laugh has no room, lengthen the hold, never add a pre-pause (CM2).

**R5. Horror and suspense budget (whole film).**
1. Ask: "List every candidate startle with its three Baird parts (HR2), its ledger mode and its dread hold. Rank them. Keep only the budget (HR1). Mark every shot with lightning, strobes, muzzle flashes or alarms `flash_risk: check` (HR10)."
2. Approve the list. A candidate that loses its place in the budget becomes a dread hold with no startle, never a smaller startle.

**R6. Plan a number (per song).**
1. Lock the song and write down its BPM and bar count.
2. Ask: "Split the song into phrases with bar numbers and times. Give one shot per phrase or longer, full figure for dance, cuts on phrase ends (SG2–SG4), and a lip-sync route per sung shot (SG5)."
3. Check the arithmetic yourself once: at 120 BPM a 4-beat bar lasts 2 s, so an 8-bar phrase is 16 s; one clip on a 15 s model is too short, so the phrase needs a hidden cut or a 20–30 s model (SG4; checked 09-28: 20 s models added).

**R7. Test the genre opener (once per tone, 10 minutes, two draft takes).**
1. Pick one representative shot of the tone.
2. Generate it twice at draft quality: once with the opener, once without, all else identical.
3. Keep the take whose light and pace match the look key (B2). If the opener pulled the light darker or the cutting faster, keep it only with explicit light words after it (GW2), and record the result in `genre_opener`.

---

## 9. Fields this file adds to the breakdown

Enums are lowercase snake_case; `none`, never empty (D9 convention). The blueprint already has `tone`, `tone_undercurrent`, `tone_shift`, `tone_home`, `tone_range`, `tone_mix_rule` and a single `genre`; every other row is a proposal (§13).

| Level | Field | Meaning | Allowed values |
|---|---|---|---|
| film | `genre_primary` | The main promise | `drama` `thriller` `mystery` `horror` `comedy` `romance` `action` `musical` `family_animation` `slow_cinema` |
| film | `genre_secondary` | A second promise, or a setting genre | the same list plus `science_fiction` `fantasy` `western` `war` `period` `none` |
| film | `tone_home` | Default tone | a §2.1 value |
| film | `tone_range[]` | Tones allowed anywhere | §2.1 values |
| film | `tone_mix_rule` | How the film mixes tones | text, e.g. "`comic_dark` only as undercurrent, never in camera" |
| film | `audience_age` | Who it is for | `adult` `teen` `family` `young_children` |
| film | `genre_budgets` | Extremes the genre spends | `{startle: n, false_startle: n, sting: n, number: n, slow_motion: n}` |
| film | `genre_opener` | Default first prompt sentence | text, identical per tone |
| film | `genre_words_banned[]` | Words never sent to models | e.g. `gory` `funny` `horror` |
| film | `number_entry_rule` | How song starts (SG6) | text or `none` |
| scene | `tone` | The scene's main tone | a §2.1 value |
| scene | `tone_undercurrent` | Optional second tone | a §2.1 value or `none` |
| scene | `tone_shift` | A change inside the scene | `<beat> \| from: <tone> \| to: <tone> \| device: size_ladder \| light_cue \| music_in \| music_out \| camera_behaviour`, or `none` (blueprint syntax and spelling; checked 09-28) |
| scene | `set_piece` | The genre scene type | `startle` `stalk` `chase` `fight` `reveal` `gag` `number` `first_meeting` `confession` `task` `none` |
| scene | `performance_scale` | How big acting is; sets the ceiling for D15's shot-level display level (§0 mapping) | `underplayed` `naturalistic` `heightened` `broad` |
| scene | `asl_factor` | Multiplier on D13's rhythm-class ASL | number (derived from `tone`, §2.2) |
| beat | `comic_role` | Place in a joke | `setup` `repeat` `punch` `reaction` `none` |
| beat | `startle_part` | Place in a startle | `presence` `threat` `intrusion` `none` |
| shot | `reaction_hold_s` | Hold after a punch or startle | number |
| shot | `startle` | This shot spends a budgeted startle | `yes` `no` |
| shot | `flash_risk` (D18's field, reused, not redefined) | Flashing content to check | `none` `check` `fixed` (D18); results go in D18's film-level `access.checks` (checked 09-28: replaces D10's earlier `flash_check` proposal) |
| number | `number_kind` | Kind of number | `diegetic` `integrated` `fantasy` |
| number | `song_id`, `bpm`, `bars` | The locked song | D9 music-cue ID `MU-##` (or a theme master `TH-##`); integer; integer (corrected: D9 retired `CUE-` IDs) |
| number shot | `bar_in`, `bar_out`, `lip_sync_route` | Where the shot sits; how the mouth syncs | integers; D3 `sync_method` values |

---

## 10. Checklists

**Film** (a "no" needs a fix or a written reason)
1. Are `genre_primary`, `tone_home` and `tone_range` set, with quoted evidence?
2. Is the setting genre kept out of camera choices (principle 4)?
3. Are `genre_budgets` set and the startle, sting and number lists within them?
4. Does the film-level ASL sit inside the genre's pace range (§3)?
5. Is the genre opener checked against every look key (GW1–GW2)?
6. Are banned words absent from every prompt?

**Scene**
1. One `tone`, at most one undercurrent?
2. Any shift sits on a turn or drop, with one system changed (TN2–TN3)?
3. Defaults moved per §2.2, turning points unchanged?
4. Comic scenes: no pre-punch pause; reaction holds set; third repeat breaks the pattern?
5. Horror scenes: every startle has presence, threat and intrusion; the threat never moves the camera; sound first?
6. Numbers: song locked; cuts on phrase ends; full figure in dance; vocal stem for lip sync?
7. Every flashing shot marked `flash_risk: check` and kept at three flashes per second or fewer (HR10)?
8. Does each convention have a story reason, not just a genre reason?

**Prompt**
1. Opener identical across the scene?
2. Light words follow any opener that contradicts the look?
3. No emotion or genre adjectives on faces?
4. No gore, injury, artist or studio names?

---

## 11. Failure modes (sign → cause → fix)

| Sign | Cause | Fix |
|---|---|---|
| Bright quarantine scenes come back dark and shadowy | "tense" opener's look bundle (S8) | Add explicit light words, or drop the opener (GW2) |
| A thriller suddenly plays like a sitcom | Comic undercurrent moved into camera and light | Camera plays the serious tone (TN1) |
| Jokes fall flat in the animatic | Pauses added before the punch; no reaction hold | Remove the pre-pause (CM2); hold after (CM3) |
| The third repeat gets no laugh | All three framed differently | Match the first two exactly (CM4) |
| Scares stop working mid-film | Too many startles and stings | Budget (HR1, HR7) |
| A startle feels cheap | Loud sound with no threat set up | Add Baird's missing part (HR2) |
| The monster feels like a costume | Shown early, whole, in sync | Sound first, partial, late (HR4–HR5) |
| Prompt refused or fewer clips returned | "Horror" plus gore wording | GW3, HR9; C3 refusal rule |
| Dance reads as chopped | Cuts on beats; feet cropped | Phrase-end cuts, full figure (SG2–SG3) |
| Singing mouth drifts | Mixed track sent to lip sync | Vocal stem only (SG5) |
| A slow film feels empty rather than slow | Long take with nothing planned inside | Plan a task or change inside each take (§12.3) |

---

## 12. Worked examples

**Film fields proposed for *The Catch* [J]:** `genre_primary: thriller`, `genre_secondary: science_fiction` (principle 4), `tone_home: tense`, `tone_range: [tense, enigmatic, dread, grave]`, `tone_mix_rule` as in §12.2, `genre_budgets.startle: 1` (§12.1). The user confirms at the story plan.

### 12.1 *The Catch* SC15, the figure on the tablet: horror against mystery

Fixed in both versions (B1 §10.5 and Example 4, A4 WE3): the feed is a high corner, wide, static, desaturated and "mirrored as a world-made picture" (B1 Ex4); the figure never causes a camera move; it appears by a frame jump; the pump's first statement comes from the tablet speaker; Iona's face comes only after the room is empty. The script's order is kept: "A small CLICK, from nowhere." / "The cup slides a hand's width across the table. Into his reach." / "Jude opens his eyes." / "Something tall and black stands beside his bed. It did not come through the door. It is simply there, in the space between one moment and the next."

| What moves | As horror (`dread`) | As mystery (`enigmatic`) |
|---|---|---|
| Ledger mode (A4) | Suspense: we watch the room before Jude wakes | Mystery: we watch as Iona does, looking for what it is |
| Pace | Hold "An empty chair beside the bed. The sealed door behind it." 6–8 s of dread; frame jump at full feed size | Feed shots 4–6 s, long enough to read the room; no extra hold |
| CLICK | Louder than the room, placed off frame, a threat | Small and clean, "from nowhere": a clue |
| Pump | The motif asset processed rough and close through D9's `device_speaker` preset. This departs from A4 WE3, which wants the first statement "clear and complete" so the motif can be recognised later; a horror reading must change A4's line or keep this statement clean | The same asset, band-limited through the tablet's small speaker but "clear and complete" (A4 WE3) |
| Light / grade | Crushed blacks; the figure the darkest shape | Readable exposure; the "pale strip" legible |
| "As carefully as a nurse." | Played as menace: care that should not be there; hold on the hand | Played as evidence: the key image of the scene |
| Jude's whispered "Iona?" | Fear | Confusion |
| Startle budget | None spent here; saved for SC16 | None |
| Opener | "A quiet, eerie suspense scene seen on a security feed." | "A calm, puzzling mystery scene seen on a security feed." |
| Unchanged in both | The order of events, the frame jump, no camera move for the figure, Iona's face only after "The chair is still there." | Same |

C3's worked prompts for these feed shots (C3 Example 5, shots 14-05A and 14-05B) use no genre opener at all and start "Fixed camera." or "Static frame". That is GW7's "without" take; test the openers above against it before adopting either.

SC16 already contains a full Baird startle: presence (Iona), threat ("Behind her: a pump. Three uneven strokes.") and intrusion ("She turns." / "The figure stands between her and the sealed door. Taller than the door."). Horror would spend its one startle there, on B1's single looming frame.

**Recommendation [J], for the user to decide.** The text leans mystery: the cup is moved "Into his reach" just before the figure is seen, the figure lifts the arm "As carefully as a nurse", and it later helps (B1 §9.2). Set SC15 `tone: enigmatic` with `tone_undercurrent: dread`. Keep SC16's turn as the film's one startle (`genre_budgets.startle: 1`). The line "Iona runs the picture back. Stops it on the hand under his arm." then gives SC16 its mystery key shot: the frozen hand.

### 12.2 *The Catch* SC10, the kitchen, as black comedy

The scene already has dry lines. Jude's scene intention is "to stay alive and keep it light" (A2), and beat B2 is a joke: "Was your appendix on the left?" / "They didn't let me watch." Saye does not contract anywhere in this scene ("That is your left."; "I cannot finish that here."), which is deadpan on the page; her one contraction in the script comes much later, "They're here. Nell is here." (A2 speech brief) (corrected: "never contracts" overstated it). The wrongness also comes in three: the scar (beats B2–B3), the hands and rings (beat B4), and the cap (beat B5): "Across the room Eli twists the cap of a water bottle. It will not give. He stops. Twists it the other way. It comes off." That is a rule-of-three pattern ending on a different person (CM4).

Which defaults would move if SC10 were played as `comic_dark`:

| Default | A2 / A4 / B1 as tuned | As black comedy |
|---|---|---|
| Sizes | Approach to Iona's close-up at B7 | One size wider throughout; B7 as a medium two-shot of Iona chewing and Saye watching flat (CM7) |
| Beat B4, mirror | Profile two-shot on a longer lens, then ring inserts | Same two-shot, frontal symmetry, held 2–3 s on "That is your left." / "It's my right." with no cut (CM5) |
| Beat B5, cap | Deep staging, focus pull to the hands | Static wide; the cap plays inside the frame; one clean click on "It comes off." (CM6, CM8) |
| Beat B7, punch | Hold through "Not mint." and B8 | Cut after "Not mint." to Saye's unmoved face; hold 2–3 s (CM3) |
| Light | Iona's lamp as key | Flatter; more fill |
| Performance | Naturalistic | Saye deadpan; Iona naturalistic |
| Unchanged | TP1 at B7, TP2 at B11, "CUT TO BLACK." | Unchanged (principle 1) |

**Recommendation [J].** *The Catch*'s home tone is `tense`. A full black-comedy reading would fight the turn at B7, where A2 needs Iona's tightest close-up. Tag SC10 `tone: tense`, `tone_undercurrent: comic_dark`, limited to beats B2 and B5. Play Jude's line and the cap in the wide shots the plan already has; do not change sizes. The same undercurrent sits in SC01's "Goods only. No persons." (Jude reading the tag) / "They all say that." (Iona) and SC09's "Io. Your dashboard's on backwards." (Jude) / "I can see it." (Iona) (`tone_mix_rule`: "`comic_dark` only in dialogue and physical business (Jude's jokes, Iona's flat replies, Eli's cap); never in camera", checked 09-28: the lines are split between Jude and Iona, and the cap is Eli's, so the earlier "only in Jude's lines" was too narrow). The user decides.

### 12.3 *The Long Places*, chapter I, as slow cinema

Set `genre_primary: slow_cinema`, `tone_home: contemplative`, `tone_range: [contemplative, enigmatic, grave]`, music policy `source_only` (D9 §8.4). Target ASL 12–25 s.

The chapter's last night of June, on the threshold:
1. **Wide, static, 20 s.** The mouth at night; the borrowed lamp on the stone. Nilay sits. Hold after she settles.
2. **Medium, static, 50 s.** "At the mouth of Kırk Oda the air shaft breathed." Sound carries the out-breath, then "a pause long enough to be mistaken for stillness; then in again, the same length, the same patience — a tide with no sea." The shot cannot hold "eighteen minutes, and eighteen again"; it holds one out-breath and its pause. Then, in the same frame: "She thought about where the baseline CO₂ readings should be taken, and lost that thought, and sat." Nothing moves but the flame; the frame outlasts the action.
3. **B1 Ex7's warmth shot, 40 s+.** Static profile medium close-up from her left, 75 mm, no reverse. The breath sound runs on under it.

Three shots in about 110 s: ASL ~37 s. Dialogue scenes at 8–12 s bring the chapter into the 12–25 s target.

Melek's round, earlier, gives a slow take its task: "She filled each small lamp to the first knuckle of her thumb, no further, from a tin can that smelled of the press and of some older oil than this year's." Play it in real time on two lamps and elide the rest with a time cut. The uncanny beats stay `enigmatic`, never `dread`: no stings, no startles. An example is the count, "She counted openings along, going in: forty-one."

**Making long takes from short clips [J].** Most models stop at 8–16 s; FLUX 3 Video and Luma Ray3.2 reach 20 s; Seedance 2.5 and Wan 3.0 reach 30 s (C1 §2 item 4, rule 11; checked 09-28). A 50 s take is still two to four clips.
- Chain clips from each one's last frame (A4 AI6), placing joins where nothing moves. Check identity at every join (C2).
- Or use a still plate with living parts: generate or paint one locked frame, and composite a small generated loop (the flame, dust) over it. This is cheapest for the stillest shots.
- One slow tracking move per chain, at most.

---

## 13. Conflicts with other files and open questions

- **D13's pace check (resolved).** D13 re-checks a film under 3 s or over 7 s ASL "for a drama or thriller"; its R23 now multiplies the rhythm-class ASL by D10's `asl_factor` and moves that warning band by the same factor, so slow cinema (over 10 s) and action peaks (under 2 s) no longer trip it.
- **The word `contemplative` (open).** D10's *tone* `contemplative` (factor 2.5 or more) is not D13's *rhythm class* `contemplative` (6 s). A contemplative-tone scene in that class would run 15 s a shot. D13 suggests renaming its class `still_pace`; the builder decides [J].
- **The blueprint's ASL source (open).** The blueprint sets `target_asl_s` "from the rhythm shape, the tone and card 13, never from `rhythm_class`", while D13 multiplies a rhythm class by `asl_factor`. Both use the tone; the builder should pick one formula.
- **Genre fields (open).** The blueprint has one `genre` field; D10 proposes `genre_primary` and `genre_secondary` (so a setting genre such as science fiction is kept out of camera choices, principle 4). The other proposals not yet in the blueprint: `audience_age`, `genre_budgets`, `genre_opener`, `genre_words_banned[]`, `number_entry_rule`, `set_piece` (D11 already reads it), `performance_scale`, `asl_factor`, `comic_role`, `startle_part`, `reaction_hold_s`, `startle`, and the number fields (`flash_check` withdrawn 09-28 in favour of D18's `flash_risk`).
- **Budgets (open).** B1's `extreme_budgets` (P5), the blueprint's `SOUNDPLAN.device_budget` (A4 P10: at most 2 each of cut to black, true silence and freeze in a short film) and D10's `genre_budgets` (HR1, HR7) overlap. Proposal: one ledger of extremes with D10's startles, stings, numbers and slow motion added as rows [J].
- **D2's shot counts (acknowledged in D2).** D2 sizes *The Long Places* Plan A at 1,200–1,500 shots (4–5 s ASL). A slow-cinema treatment gives roughly 400–500 shots [J]. D2 now says the ASL is a style choice made at checkpoint M. Fewer shots does not mean less money: generated seconds stay similar, and long chains fail more; D13 should re-run the estimate after the choice.
- **A2's comic rule.** "Cut on the punch word" (A2 §4) and CM1 ("land it inside a frame, cut after") differ. Proposed: cut on the punch word only in verbal banter shot in singles; for physical and visual jokes, CM1.
- **C3's default opener.** "A tense dramatic thriller scene." (C3 §14 item 6, "Genre first") suits dark scenes; *The Catch*'s daylight quarantine scenes need explicit light words after it (GW2).
- **D15's "tone words in the voice line only".** D15 keeps tone words out of performance lines; D10's opener is a scene-level sentence at the head of the prompt, never on a face. They agree if the opener stays first and faces get behaviors only (§10 prompt checklist 3).
- **D3 and D9 preset names.** D3 lists D9 presets as `earpiece_radio`, `small_speaker`; D9's own list has `device_speaker` and `earpiece`. D10 now uses D9's `device_speaker`; D3 should follow D9.
- **Dance.** D11 covers fights and physical set pieces, not dance notation; SG3 gives a stopgap (counts plus one movement line).
- **Flash area (resolved 09-28).** D18 §3.5 marks the UK area limit [U] because the Ofcom PDF is blocked. Jordan and Vanderheiden (2024) give it: more than three flashes in one second *and* more than 25% of the displayed screen [V-secondary, S27]; the Epilepsy Society confirms an area limit exists [V-secondary, S25]. D18 can upgrade its [U] to [V-secondary] with S27. HR10's working rule (three or fewer per second, any size) passes both limits.
- **Performance scale vs display level (open, 09-28).** D15 sizes acting per shot as display level 1–3 and the blueprint's `tone_defaults.json` stores a "performance display level" per tone; D10's `performance_scale` is a scene-level word. Proposal [J]: keep D15's number as the only shot field and store `performance_scale` only as the tone default that caps it (§0 mapping); `broad` has no D15 equivalent above 3, so D15 needs a note that `broad` means level 3 plus bigger gesture and silhouette (B5), not a bigger face.
- **Undercurrents outside the range (open, 09-28).** The blueprint's FILM-12 flags only a scene `tone` outside `tone_range`. TN7 now also covers undercurrents. Because `tone_mix_rule` is free text, code cannot read which undercurrents it allows; proposal [J]: add a list `undercurrents_allowed[]` to PLAN (for *The Catch*: `[comic_dark]`; `dread` is already in its range) and let FILM-12 check it.
- **Flash field (resolved 09-28).** D10 first proposed a shot field `flash_check`; D18 already owns `flash_risk` (`none` `check` `fixed`) and `access.checks`. D10 now reuses D18's field.
- **C3's shot IDs.** C3 Example 5 labels the tablet shots 14-05A and 14-05B under its own numbering; under C5's scene IDs used here they sit in SC15. The builder should map C3's example IDs, not copy them.
- **For the user.**
  1. SC15: mystery (recommended) or horror.
  2. SC10: comic undercurrent kept or cut.
  3. *The Long Places*: slow cinema or D2's 4–5 s ASL.
- **Weak evidence.** Genre ASL targets are [J]; the Cinemetrics horror figure looks skewed; Flanagan, Baird, Ofcom and Bordwell's action quote come second-hand; Attardo and Pickering measured spoken joke-telling, not film edits; that "horror" alone trips filters is unverified [U]: Google's guide only warns that its horror bundle includes "gory".

---

## Sources

All checked 2026-09-27. Re-fetched 2026-09-28 in the second check: S1–S20 and S22–S26 (S12 and S7 abstracts via the Europe PMC API, since PubMed shows a captcha); S27 and S28 added.

- S1. D. Bordwell, "Intensified continuity revisited" (27 May 2007): https://www.davidbordwell.net/blog/2007/05/27/intensified-continuity-revisited/ [V]
- S2. S. Follows, "How many shots are in the average movie?" (Cinemetrics data, 1997–2016): https://stephenfollows.com/p/many-shots-average-movie [V]
- S3. J. E. Cutting et al., "Quicker, faster, darker: Changes in Hollywood film over 75 years", *i-Perception* 2 (2011): https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/ [V]
- S4. J. E. Cutting, "The evolution of pace in popular movies", *Cognitive Research* (2016): https://pmc.ncbi.nlm.nih.gov/articles/PMC5256470/ [V]
- S5. Where's the Jump?, "Do modern horror movies contain more jump scares than older movies?": https://wheresthejump.com/do-modern-horror-movies-contain-more-jump-scares-than-older-movies/ [V; crowd data]
- S6. D. T. Blumstein, R. Davitian, P. D. Kaye, "Do film soundtracks contain nonlinear analogues to influence emotion?", *Biology Letters* 6 (2010): https://pmc.ncbi.nlm.nih.gov/articles/PMC3001365/ [V]
- S7. C. Trevor, L. H. Arnal, S. Frühholz, "Terrifying film music mimics alarming acoustic feature of human screams", *JASA* 147(6) EL540 (2020), abstract on PubMed: https://pubmed.ncbi.nlm.nih.gov/32611175/ [V; abstract read via Europe PMC, PubMed showed a captcha]
- S8. Google Cloud, "Video generation prompt guide" (last updated 2026-09-25): https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/video-gen-prompt-guide [V]
- S9. Wikipedia, "Mickey Mousing": https://en.wikipedia.org/wiki/Mickey_Mousing [V]
- S10. K. Barrowman, "Action Aesthetics: Realism and Martial Arts Cinema, Part 2", *Offscreen* (2014), quoting Bordwell's *Planet Hong Kong* (2000), p. 221: https://offscreen.com/view/action-aesthetics-pt2 [V-secondary]
- S11. Wikipedia, "Fred Astaire" (citing J. Mueller, *Astaire Dancing*): https://en.wikipedia.org/wiki/Fred_Astaire [V]
- S12. A. S. Lillard, J. Peterson, "The immediate impact of different types of television on young children's executive function", *Pediatrics* 128(4):644–649 (2011), abstract on PubMed: https://pubmed.ncbi.nlm.nih.gov/21911349/ [V]
- S13. S. A. Namazi, S. Sadeghi, "The immediate impacts of TV programs on preschoolers' executive functions and attention: a systematic review", *BMC Psychology* 12 (2024): https://pmc.ncbi.nlm.nih.gov/articles/PMC11044375/ [V; full text read via Europe PMC]
- S14. Wikipedia, "Werckmeister Harmonies": https://en.wikipedia.org/wiki/Werckmeister_Harmonies [V]
- S15. Wikipedia, "Slow cinema" (names M. Flanagan's 2008 essay "Towards an Aesthetic of Slow in Contemporary Cinema" as "influential"): https://en.wikipedia.org/wiki/Slow_cinema [V for the page and its quote from *The Guardian*; the Flanagan quote is not on this page, see S24]
- S16. S. Attardo, L. Pickering, "Timing in the performance of jokes", *Humor* 24(2) (2011): https://lair.etamu.edu/chssa-faculty-publications/8/ [V]
- S17. *MovieMaker*, on Every Frame a Painting's "Edgar Wright - How to Do Visual Comedy" (T. Zhou, 2014): https://www.moviemaker.com/edgar-wright-visual-comedy-video/ [V]
- S18. R. Fuoco, "Engineering Shock: Part 1", *Offscreen* 20(5) (May 2016), on R. Baird, "The Startle Effect", *Film Quarterly* 53(3) (2000): https://offscreen.com/view/engineering-shock-part-1 [V-secondary]
- S19. Runway, "Usage Policy" (last updated 6 March 2026): https://runway.com/safety/usage-policy [V]
- S20. W3C, "Understanding SC 2.3.1: Three Flashes or Below Threshold" (WCAG 2.2): https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html [V]
- S21. Ofcom (legacy ITC guidance note on flashing images): https://www.ofcom.org.uk/__data/assets/pdf_file/0021/16248/gn_flash.pdf [U; the server returned 403 to automated access on 2026-09-27 and again on 2026-09-28; see S25 and S27]
- S22. sync. labs, "Lipsync models" (FAQ on songs): https://sync.so/docs/models/lipsync [V]
- S23. Quote Investigator, "Life is a Tragedy when Seen in Closeup, But a Comedy in Longshot" (5 Feb 2017): https://quoteinvestigator.com/2017/02/05/comedy/ [V]
- S24. L. Elson, "Slow Cinema Modality: Applying Bordwell to Tsai Ming-Liang", *JUST*, Vol. V, No. 1 (2017), Trent University, quoting M. Flanagan, "16:9 in English: Towards an Aesthetic of Slow in Contemporary Cinema", *16:9 Filmtidsskrift* (Nov. 2008; journal and date from Elson's works cited): https://ojs.trentu.ca/index.php/just/article/download/126/83 [V-secondary]
- S25. Epilepsy Society, "Photosensitive epilepsy" (Ofcom flash-rate and area rules; the Harding test): https://epilepsysociety.org.uk/about-epilepsy/epileptic-seizures/seizure-triggers/photosensitive-epilepsy [V]
- S26. ElevenLabs, "Best practices" (Eleven v3 audio tags; `[sings]` listed under "Unique and special: Experimental tags for creative applications"): https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices [V]
- S27. J. B. Jordan, G. C. Vanderheiden, "International Guidelines for Photosensitive Epilepsy: Gap Analysis and Recommendations", *ACM Transactions on Accessible Computing* (2024), table of Ofcom thresholds: https://pmc.ncbi.nlm.nih.gov/articles/PMC11872230/ [V-secondary for Ofcom]
- S28. Wan-AI, "Wan-Dancer-14B" model card (Hugging Face; Apache 2.0; announced 13 July 2026): https://huggingface.co/Wan-AI/Wan-Dancer-14B [V]
