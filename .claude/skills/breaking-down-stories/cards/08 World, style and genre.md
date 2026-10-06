# Card 08. World, style and genre

Read whole at step 3. Step 2 reads only "Genre and tone". "D17 R1" names rule 1 in D17's numbered rules (§3), and D5's rules the same way; D10 labels its rules TN, CM, HR and GW, and its recipes R.

## The job

Decide once where and when the story happens, what the whole film is made to look like, and the feeling each scene is played in, so that every later file reads one world (D17 §0; D5 §2; D10 §1). Step 2 writes `genre`, `tone_home`, `tone_range` and `tone_mix_rule` in PLAN, and `tone`, `tone_undercurrent` and `tone_shift` on each scene. Step 3 writes WORLD with its evidence, STYLE (medium, style words, texture), the frame shape's story reason, and a RULE record for each rule of the story world. Each big choice the story leaves open becomes a CHOICE with a default.

## Questions in order

1. **Does the story name the place and time?** If not, set `place` and `period` to `unstated`, harvest the cues with their lines into `evidence`, each `origin: inferred`, and write one CHOICE with a default and one alternative (D17 R1).
2. **Does a cue conflict with the rest?** List it as a question with both readings; never quietly change the story (D17 R2).
3. **Is the place invented?** Borrow one real country's conventions (a **model country**) or design all of them; a half-designed place drifts to the models' American default (D17 R4, §1).
4. **Does the story span several times?** Give every scene a **period layer** (which of the story's times it belongs to); a scene outside time gets only objects that existed across the whole span (D17 R5-R6).
5. **Which local signals will be seen or heard?** Research from a primary source anything seen for more than a glance or in more than one shot, read, or heard clearly; mark an answer from memory as unverified (D17 R7-R8). Check the real colours of signals, such as emergency lights (B2 R19).
6. **Is an institution real and identifiable?** Invent its name, crest and livery, and keep its researched grammar (D17 R12; D4 R19).
7. **Does the story mirror its world?** Record the home driving side and every body custom it uses as a cue, such as the wedding-ring hand (D17 R16, R21).
8. **What medium does the story ask for?** Photographic live action when the story's force is the real world going slightly wrong; stylised media are open to fable, myth and fantasy (D5 R1-R2). Test a creature in every candidate style (D5 R6); never choose a cartoon style to pass filters (D5 R7).
9. **What frame shape, and why?** Decide once, with a story reason: upright figures and confinement favour a narrow frame, two or three people in rooms `1.85`, pairs at opposite edges or rows of rooms `2.39` (B1 §5; `PROJECT.frame_shape`).
10. **Which story-world rules govern the picture?** One RULE each, with the quoted lines where it starts and ends, what it governs, and each exception with `reads` (`normal` or `mirrored`) and a `why` (K03, K04). Cards 16 and 17 hold mirror and text rules.

## Genre and tone

**Genre** is the kind of promise a story makes (a scare, a laugh, a love story); **tone** is the attitude the telling takes toward events, moment to moment (D10 §0). The tones: grave (serious, no threat), tense (danger with stakes), dread (fear of an unseen threat), enigmatic (a puzzle), comic_light (warm comedy), comic_dark (pain treated flatly for laughs), romantic (two people moving together), kinetic (bodies, speed, impact), lyric (feeling becomes song), wonder (safe discovery), contemplative (time itself, observed) (D10 §2.1).

1. **One home tone per film, one main tone per scene.** A second tone is `tone_undercurrent`, carried by lines, props and acting, never by the camera (D10 §1, TN1).
2. **When tones mix, the camera plays the more serious one** (D10 §1).
3. **A shift inside a scene sits on a turn or a drop** (a planned fall in pressure, such as a silence), is recorded in `tone_shift`, and changes one visible system, which then holds (D10 TN2-TN3).
4. **Tone changes how a beat is played, not what happens:** it never changes which beat turns, what the text marks, in-story footage or physics (D10 §1).
5. **A setting genre** (science fiction, fantasy, western, war, period) sets the world and the design, never the camera; camera, light and cutting come from tone (D10 §1). The Catch is science fiction in its world and a thriller in its tone.
6. **Quote evidence for every tone value** (D10 R1). **Flag, never fix:** a `tone` outside `tone_range`, or undercurrents in more than `undercurrent_scene_share_max` of scenes, go to the user (D10 TN6-TN7; FILM-12).
7. **Start from the tone's row** in `rules/tone_defaults.json`: shot-length factor, size and lens, camera behaviour, contrast band, music default and display level. Log any departure (D10 §2.2). The estimate multiplies `rhythm_class_asl_s` by the factor, and the film's average shot length is checked against `film_asl_range_s` (TIME-07); `rhythm_class_asl_s` is never a design target.
8. **Each genre rations its own extremes,** on top of the camera's saved choices: horror its startles (about one per ten minutes, at most three in a short), comedy its broken patterns, a musical its song numbers, action its slow motion and big hits (D10 §1, HR1).
9. **Comedy lives after the punch:** no pause before it, a held reaction after it, in a frame that holds both the cause and the victim (D10 CM1-CM3). **A startle needs three parts:** a character present, a threat implied off screen, and an intrusion into their space; the threat never causes a camera move (D10 HR2, HR5).

The Catch, proposed: `tone_home: tense`; `tone_range: tense, enigmatic, dread, grave`; `tone_mix_rule`: comic_dark only in dialogue and physical business, never in the camera (D10 §12).

## Translation menus with pitfalls

Pick one answer per question and tie it to a line in this story.

| Question | Options | Pitfall |
|---|---|---|
| Medium | `live_action`, `painted`, `2d_animation`, `stop_motion_look`, `3d_animation`, `mixed` | choosing on the prettiest wide, not the hard shots (D5 R12) |
| Place | a named country; invented on a model country; invented with its own conventions | an accent chosen before the place (D17 §5) |
| Texture | fine grain, and a soft glow only round lamps, set once in post for the whole film | more than one texture phrase in a prompt: generated grain changes clip to clip (D5 R18, R20) |
| A second style | one part of the film (letters, a memory) with its own story reason | a style break with no reason (D5 R10) |

## Budgets and saved choices

- Style words: `style_words_count` plain descriptors, each visible and positive, in frozen word order (D5 §5).
- `named_reference_policy` is fixed: describe qualities, never name a film, director, living artist, studio or brand; names go to `words_to_avoid` or nowhere (D5 R13; D4 R5; WORDS-03).
- A second style is a CHOICE with a story reason, at most two per film (D5 R10).
- `undercurrent_scene_share_max`, `film_asl_range_s`.
- The style stays `provisional` until D5's test of three directions on three hard shots (D5 §7.1, R12).

## The baseline is a strong answer

Photographic live action, a present-day world, the frame shape the story's images need, and one home tone with few shifts are choices, not failures. Style words describe how every image is made, never one scene's light or a feeling (D5 §5). Depart only for a reason you can cite.

## Cliché traps

Tests: any-film, mood-word, stacking, sound-off (card 05).

- "Cinematic", "epic", "futuristic" or "sci-fi" as style words fail the any-film test and pull a stock neon picture; show the future in designed devices and props (D5 R23; GEN-12).
- A named film or artist as the style (D5 R13).
- American defaults in an unstated world: school buses, red-and-blue light bars, overhead signals (D17 §1, §9).
- A mixed bundle: British voices under American exit signs (D17 R1).
- A comic undercurrent moved into camera and light, so a thriller plays like a sitcom (D10 TN1, §11).
- Teal-and-orange night as a genre's default (D10 §3.2).

## Reasons that fail and reasons that pass

- Fails: "2.39 because it looks cinematic." Passes: "2.39 because the story's key images are pairs at opposite edges and rows of glass rooms (B1 §5; K24)."
- Fails: "Tone: dark." Passes: "SC15 `tone: enigmatic` with `tone_undercurrent: dread`: the cup slides 'Into his reach' (line 846) before the figure is seen (D10 §12.1)."
- Fails: "Set in London." Passes: "An unnamed British city, `inferred` from 'torch', 'night bus' and 'I know how a lift works, Io.' (line 59) (K27; D17 §6.1)."

## Two worked examples

### The Catch: world, style and tone

WORLD: an unnamed British city, present day, driving on the left, British English accents, each `inferred`, from "I know how a lift works, Io." (line 59), "The little running man is running the other way." (line 331) and "A night bus comes at them" (line 370) (K27). The guard's pistol (line 183) conflicts with a British reading, so it becomes a question for the writer, never a quiet swap for a baton (D17 R2, §6.1). Customs: the wedding ring on the left hand, so "Saye's wedding ring. On her right hand." (line 436) reads as wrong (D17 R21). STYLE: `live_action`, `provisional`, with style words such as "photographic live-action image; clean spherical lens, straight lines stay straight; natural skin with pores and fine lines; real materials with visible wear, grime and texture; true blacks with detail in the shadows; clean, sharp highlights; muted colour except named objects" (D5 §13.1). Frame shape `2.39` (K24). SC10 plays `tense` with a `comic_dark` undercurrent limited to "They didn't let me watch." (line 414) and Eli's water-bottle cap, in the wides the plan already has (D10 §12.2).

### The Long Places: a real region, three times, a slow tone

`place: named:turkey`, `origin: story`, from Kayseri, Derinkuyu and Cappadocia; the site is invented inside a real region, modelled on several real analogues rather than one (D17 R3, §7.1). Period layers: the present season, 1999, and the keeper's letters outside time, which get no print, plastic or electric light (D17 R5-R6, §7.4). Text with ı and İ is made as a text graphic (D17 R14; card 17). Tone: `tone_home: contemplative`, range contemplative, enigmatic and grave, music from sources only; the uncanny beats stay `enigmatic`, never `dread` (D10 §12.3). Style: live action, because the change from soot-black to pale ceilings needs exact values; a restrained painted style for the letters is a CHOICE (D5 §14, R10).

## Self-check

- Is every WORLD value the story does not state `inferred` from a quoted cue, or a CHOICE with a default?
- Is every conflicting cue a question, not a quiet change?
- Are real institutions renamed, with their grammar kept?
- Are the style words within `style_words_count`, visible, positive, and free of names, of any one scene's light, of feelings and of banned words ("practical light from lamps and windows" is a whole-film style), with STYLE `provisional`?
- Does the frame shape have a story reason?
- Does every scene have one tone, at most one undercurrent, and quoted evidence?
- Does every story-world rule have start and end lines and a list of what it governs?

## Words for AI models

Works: conventions in plain words, early in the prompt ("traffic keeps to the left; right-hand-drive cars", "only blue flashing lights, no red") (D17 R13, §10); the style words first and unchanged, before the look block (the pasted light, colour and texture of a place at a time) (D5 §5); a tone opener followed by explicit light words: "A tense dramatic thriller scene. Even, flat daylight from ceiling panels." (D10 GW2).

Fails: a country or city name alone, which pulls landmarks and logos; film, artist or studio names; "cinematic", "8K", "masterpiece", "futuristic"; "horror", which pulls gore (D10 GW3); "funny", which invites mugging (D10 GW4); more than one texture phrase (D5 R18).

## Look up for more

D17 §1, §3 (R1-R22), §4 (recipes), §6 (The Catch's world options), §7 (The Long Places); D5 §4 (R1-R24), §5 (style words), §7 (the three-direction test), §13-§14; D10 §1, §2 (tones and the defaults table), §7 (GW1-GW7), §12; B1 §5; B2 R19; D4 R5, R19; K24, K27. Print one rule with `stage.py lib D17 R21`.
