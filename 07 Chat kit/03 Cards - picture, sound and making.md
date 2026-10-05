# 03 Cards - picture, sound and making

Part of the Stage chat kit (knowledge). It joins these craft cards, each whole: 08 World, style and genre, 09 Film rules and restraint, 10 Camera, 11 Light and colour, 12 Staging and composition, 13 Cutting, rhythm and sound, 14 Shot design, 21 Making pictures and video with AI, 22 Previs, 23 Finishing, captions and delivery, 24 Rights, consent and disclosure. A step file names the card parts to read for each unit; read only those parts. 01 House rules says where every other skill file is in this kit.

---

From the skill file `cards/08 World, style and genre.md`:

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
- Are the style words within `style_words_count`, visible, positive, and free of names, light sources, feelings and banned words, with STYLE `provisional`?
- Does the frame shape have a story reason?
- Does every scene have one tone, at most one undercurrent, and quoted evidence?
- Does every story-world rule have start and end lines and a list of what it governs?

## Words for AI models

Works: conventions in plain words, early in the prompt ("traffic keeps to the left; right-hand-drive cars", "only blue flashing lights, no red") (D17 R13, §10); the style words first and unchanged, before the look block (the pasted light, colour and texture of a place at a time) (D5 §5); a tone opener followed by explicit light words: "A tense dramatic thriller scene. Even, flat daylight from ceiling panels." (D10 GW2).

Fails: a country or city name alone, which pulls landmarks and logos; film, artist or studio names; "cinematic", "8K", "masterpiece", "futuristic"; "horror", which pulls gore (D10 GW3); "funny", which invites mugging (D10 GW4); more than one texture phrase (D5 R18).

## Look up for more

D17 §1, §3 (R1-R22), §4 (recipes), §6 (The Catch's world options), §7 (The Long Places); D5 §4 (R1-R24), §5 (style words), §7 (the three-direction test), §13-§14; D10 §1, §2 (tones and the defaults table), §7 (GW1-GW7), §12; B1 §5; B2 R19; D4 R5, R19; K24, K27. Print one rule with `stage.py lib D17 R21`.

---

From the skill file `cards/09 Film rules and restraint.md`:

# Card 09. Film rules and restraint

Read whole at step 6, beside the step-6 parts of cards 10 to 13. Step 9 reads only "Film pass". "B1 P5" is principle 5 in B1 §1 and "B1 R19" rule 19 in B1 §11; B2 and B3 number principles in §1 and rules in §7; A2's rules are in A2 §7, A4's principles in A4 §2, D16's rules in D16 §4.

## The job

In The Catch the film's tightest size is spent once, in scene 13, and its longest hold once, on the last shot of scene 30, the pump over black (K12); nothing before them matches them. Write each department's system once, before any scene, from the one climax and the peaks, so that choices build instead of repeating (B1 §9; B3 P4).

- **Film rules** are the records of `10 Film rules.md`: CAMSYS, CAMRULE, RESERVE, LENS, LOOK, VISUAL, SOUNDPLAN, LADDER. Every line cites a plan, character, motif or rule ID.
- A **peak** is where one component (size, hold, colour, contrast, sound) reaches its maximum for the whole film (D16 §6).
- A **saved choice** (RESERVE, `RC-`) is a choice rationed for special moments; a **banned choice** is one the film never makes (B1 §9.1).
- The **ladder** (LADDER) lists each scene's main turn with its planned size and hold; each line is a **rung** (A2 R31).
- A **story point** is a scene ID and a quote, `SC24 "She deletes the way home."`, used before beats exist.

## Questions in order

Step 6 answers them in this order (D16 §4; B2 §8.3):
1. **Where is the climax, and where does each component peak?** Read PLAN `climax` and `peak`; a peak away from the climax carries its reason (D16 R15; PLAN-03). A climax in **counterpoint** (visually calm under the story's highest pressure) still owns the core value's turn, the one scene intensity 10 and one of longest hold, camera break or tightest size (D16 R16).
2. **Which component does the climax save?** If the opening spends one component's maximum, save another for the peak (B2 §4.4, R9).
3. **What is the camera's baseline, and what is banned?** (card 10; B1 §9.1)
4. **What does each principal's camera rule keep for later?** (B1 §9.2, R24)
5. **Which choices are rationed, how often, where?** (B1 P5)
6. **What is each place's lighting plan, and the colour script, peaks first?** (card 11; B2 §5.3, §8.3)
7. **What does each visual component do per sequence?** (card 12; B3 §2.6)
8. **What is the sound plan?** (card 13; A4 §7.6, P10)
9. **Does the ladder climb?** Each scene's main turn lands at that scene's tightest size or on a deliberate wide; nothing spends the film's tightest size or longest hold before the climax (A2 R4, R31).

## Film pass

Example: in The Catch the rhyme check compares scene 10's reflection two-shot with scene 29's: the same lens, level, along the glass; sides reversed on purpose (Iona is turned back), so the PLANT says `rhyme: yes | framing: profile two-shot | side: reversed` (B3 §8.2; K07). The **film pass** (step 9) judges the whole film as one structure before any picture is made. It reads the **film strip**, one line per shot (ID, beats, role, size, lens, camera move, saved choice used, emphasis, screen time, scene intensity). A **turn picture** is the one-sentence frame each turn must show; a **light cue** is a change of light the story causes.

**Code first.** `stage.py check --film` runs:
- FILM-01, the ladder: nothing before the climax spends the tightest size or longest hold unless a peak places it there.
- FILM-02, rhyme: a payoff shot marked `rhyme` repeats its plant shot's lens, angle, size and frame side (the opposite side under `side: reversed`) (B3 P8).
- FILM-03, character camera rules: nothing tighter than a character's `limit_before` size before the story point in `closest`; nothing listed in `never` used.
- FILM-04, colour monotony: `colour_monotony_run` sequences in a row with the same frame value (how light the frame is), saturation (how intense its colour) and temperature (warm or cool) (B2 §8.3).
- FILM-05, more than two components raised at one peak (B3 R7).
- FILM-06, compliant sameness: `compliant_sameness_run` static shots of one subject from one setup (camera position), same size and angle, with no `why`.
- FILM-07, a scene of scene intensity `high_intensity_scene_min` or more followed by one that does not cut slower (A4 §6.9).
- FILM-08, film-wide saved-choice counts and places.
- FILM-09, heavy-handedness: more than `plant_inserts_per_scene_max` inserts of a **plant** (a thing shown early so a later payoff lands) in a scene, music under a beat with an `unsaid`, a light cue on the line that states the point.
- FILM-10 and FILM-11, motif and loud-set counts (B4 §3.2, R17); FILM-12, a tone outside the plan, flagged, never fixed (D10 TN7).

**Then judgement.** A fresh unit, never the one that wrote the shots (in chat, a check chat), answers yes or no:
1. **Sound-off test:** with the sound off, does each turn picture tell its beat (B3 §10.1)?
2. **Stranger test:** could someone who has not read the story say what changes in each scene from its turn pictures and purposes (D7 §7)?
3. **Heavy-handedness:** a symbol the source lacks (B3 R24; B4 R25)? Music under subtext (A4 §7.6)? A light cue synced to the line that states the point (B2 §12)? A rhyme the story does not support (B3 P8)?
4. **Does any shot feel like a different film** (B3 R26; D7 §7)?

Each "no" becomes a FINDING with `record`, `rule`, `evidence`, `fix`, `source: film_pass`. Fixes return to steps 7 and 8 for the named scenes only. Only findings that change a creative choice reach the user, as CHOICE records (usually none to three). A strip longer than `film_strip_tokens_per_unit_max` is judged one act per unit.

## Translation menus with pitfalls

Pick at most one per component per part of the film; tie it to a line, object or action in this story (B3 §7.1).
- **Progression:** one component changes slowly across the film, such as lenses lengthening as a room closes in (B3 §2.5; B1 §4.2). Pitfall: progressing everything at once.
- **Step change:** from a named scene the **lens family** (the short list of lenses the film allows) shifts (B1 §4.3, R15). Pitfall: no story change behind it.
- **Two worlds:** each world has its own light logic, meeting only at boundaries (B2 R13). Pitfall: a code no story needs becomes a filter (B2 §3).
- **The break:** a rule held all film, broken once on the turn it serves (B1 P9, R24). Pitfall: breaking it twice.
- **Counterpoint:** calm picture under a story peak, justified in one sentence (B3 §2.5). Pitfall: calm by accident.

## Budgets and saved choices

- Two film-level RESERVE records, always: the non-insert extreme close-up within `extreme_close_up_film_max` for the format, and push-ins in no more than `push_in_scene_share_max` of scenes (B1 P5; FILM-08). Per scene, `extreme_close_up_per_scene_max` and `push_in_per_scene_max` are caps, never quotas (CRAFT-01, CRAFT-02).
- Dolly zoom, orbit, Dutch tilt and an unmotivated overhead at most once or twice a film each, unless the camera system bans them (B1 P5, §9.2). Crane-up or pull-back endings on at most one scene in four (B1 P5, R19).
- Editor-made cut to black, true silence and freeze within `device_budget_short` (A4 P10; CRAFT-12).
- Emphasis 3 within `emphasis_3_rules`; added emphasis within `added_emphasis_per_beat_max` (B4 P5, R23).
- At a main turn at most `departments_changing_at_main_turn_max` departments change; on any beat at most `signals_changing_per_beat_max` of size, light, sound, camera move and colour (B3 R7; B1 P11; CRAFT-19).
- The film's average shot length inside `film_asl_range_s` for the home tone (D10 §2.2; TIME-07).

## The baseline is a strong answer

Static, the owner's eye height, a normal lens, room sound are choices, not failures. Depart only for a reason you can cite. A system is mostly baseline, because a departure means something only against a taught pattern (B1 P4; B2 P3; B3 P5).

## Cliché traps

Tests: the **any-film test** (would this reason fit any film with this theme?), the **mood-word test** (does the reason name only a feeling?), the **stacking test** (more than one signal on one beat?), the **sound-off test** (does the frame tell the beat with the sound off?) (B3 R23, R26, §10.1).
- **No valleys:** every sequence at full contrast. Test: does anything but the peak reach a component's maximum? Fix: peaks first, valleys lower (B2 §8.3; B3 P4).
- **Push-in on every realisation.** Test: count them per film. Fix: the film reserve (B1 §6, P5).
- **Teal-and-orange, or a warm-cool split no opposition asks for.** Fix: name the opposition or drop it (B2 §4.8, R16).
- **Motif wallpaper:** a motif colour in most shots. Fix: ration it to meaningful beats (B2 §12; B4 P2).
- **A sad cue under unspoken sadness; dissolves the script never wrote.** Fix: the music policy and written transitions only (A4 §7.6, §13, T5; CRAFT-13).
- **A rule's payoff spent early**, such as an earlier look into the lens. Fix: search the shot list for each saved choice before approving a scene (B1 §14).

## Reasons that fail and reasons that pass

- Fails: RESERVE `allowed_in` "big moments". Passes: "main turns only; the first at SC13's main turn, 'I wasn't asking her.' (K05)".
- Fails: `peak: colour` "the fire is exciting". Passes: `peak: colour | scene: SC24 | reason: the crisis, "She deletes the way home."; the climax is black and near colourless in counterpoint` (K12; D16 §8.7).
- Fails: CAMSYS `break` "a big move at the end". Passes: `SC26 "She pushes gently away from the rail." | what: the camera floats free for the first time | because: PLAN` (B1 §9.2).

## Two worked examples

### The Catch (tense, 30 scenes)

Peaks (K12): crisis SC24; climax SC26 to SC27, the one scene intensity 10, in counterpoint; the tightest size in SC13, with its reason; saturation and red against green at the fire in SC24; the camera's break and the sound rupture in SC26 ("Then not.", line 1510); the longest hold and the only sound emphasis 3 on SC30's last shot. The tunnel opens at extreme light-dark contrast, so saturation is the component saved (B2 §4.4, §8.5). CAMSYS bans the dolly zoom, the Dutch tilt (the film's wrongness is handedness), slow motion (K30) and the orbit (B1 §9.2). RESERVE: `RC-01`, the reflection two-shot, scene 10 camera A and scene 29 only (K07); the non-insert extreme close-up; the push-in share. Rung: `SC10 "Her face changes." | size: close_up | hold: long`, one step wider than SC13's `extreme_close_up` (K05).

### The Long Places (contemplative, prose)

Home tone `contemplative`, music `source_only` (D10 §12.3). Turns are held rather than tightened: wide or held medium, deep focus, the frame outlasting the action (D10 §2.2). The book rhymes a distance: the keeper sits "at the good distance" (line 98), and the floor mark GOOD_DISTANCE, the same low static camera and an object set down between two bodies return whenever the phrase does (B3 Ex5, R19). Uncanny beats stay `enigmatic`: no stings, no startles.

## Self-check

Yes or no (D16 §10; B2 §11; B1 §13).
1. Does every system line cite a plan, character, motif or rule ID?
2. Are the tightest size and longest hold kept for the climax, or displaced with a reason?
3. Are both film-level saved choices written, with uses and places?
4. Does every sequence have a VISUAL row, with no run of identical rows?
5. Does every scene with a main turn have a rung, and does the ladder climb?
6. Is every story point's quote found once in its scene?

## Words for AI models

Film rules reach prompts only as repeated words: the same lens, height and move words in every prompt keep separate shots consistent (B1 §9), and each place's **look block** (the light and colour sentences of its LOOK) is pasted unchanged (B2 §13.4). Works: "The camera holds completely still for the whole shot." (B1 §15). Fails: "cinematic", "epic", "blockbuster" (B2 §4.8); named cinematographers (B2 §13.3); peaks, budgets and reasons in prompt text (GEN-15).

## Look up for more

`stage.py lib B1 §9`, `B1 P5`, `B1 §14`; `B2 §8` (colour scripts); `B3 §2.5` to `§2.7`; `B4 §3.4`; `A4 §6.9`, `§7.6`, `P10`; `D16 §4` (R15 to R17) and `§6` (the table of peaks); `D7 §7`; `A2 R31`; `D10 §12.3`; K05, K07, K12, K30.

---

From the skill file `cards/10 Camera.md`:

# Card 10. Camera

Step 6 reads only "Camera system"; step 8 reads only "Slots and moves"; chat apps read it whole. "B1 R6" is rule 6 in B1 §11 and "B1 P5" principle 5 in B1 §1; "B1 Ex3" is worked example 3 in B1 §12. Lenses are full-frame equivalents in millimetres (B1 §0.1).

## The job

In The Catch the camera kneels when Iona kneels, stays still while she is in control, and turns handheld only on three passages where she loses it (B1 §9.2). The camera is a narrator with a body: where it stands, how high, how far and through which lens each say something; if you cannot say what, choose again (B1 P1). Step 6 hands on CAMSYS, a CAMRULE per principal, RESERVE and LENS records; step 8, each SHOT's camera fields, every departure with a `why`.

## Questions in order

1. **Whose scene is this beat?** Put the lens at that person's eye height (B1 R6).
2. **Is this beat a turn?** Give it the scene's most extreme framing: closest if the turn happens inside a person, widest if it leaves them alone or waiting (B1 R1, A2 R4).
3. **Has the script already marked the beat** (a line, a look, a change of state)? Then the camera adds nothing (B1 P11, B4 R23).
4. **Is someone hiding a feeling?** One size wider than the progression would reach, except on a turn (B1 R5, R1).
5. **Is power shifting?** Change angle only on that beat, in both halves of the exchange (B1 R7).
6. **Where does the camera stand?** Position first, lens second (B1 P6).
7. **What causes the move?** Name it, or stay static and cut (B1 P8, R21).
8. **What does the story keep hidden?** Keep it out of frame; never tilt to find it (B1 P7, Ex2).

## Camera system

Example: The Catch frames `2.39` because pairs face each other across glass and tables; spherical lenses, 35 and 50 for people, 85 from scene 13, 24 only in the cage, the ship's wides and Iona's room; the lens at Iona's eye; `static`; dolly zoom, Dutch tilt, slow motion and orbit banned (B1 §9.2).

The **camera system** is the film's written rules for the camera, filled once before any shot, every line with its story reason (B1 §9.1). Its fields:
- `frame_shape_why`: decide once. Upright figures, confinement and faces favour a narrow frame; two or three people in rooms `1.85`; pairs at opposite edges, rows of rooms or a figure small in space `2.39`. A tool that makes only 16:9 serves a `2.39` film by keeping heads, hands and text in the central band (B1 §5; K24).
- `lens_type`: spherical for clinical, documentary honesty; anamorphic for romance, myth and epic width (B1 §4.4).
- `lens_family`: the **lens family** is the short list of lenses the film allows: wide up to about 35, normal about 40 to 58, long from about 75 (B1 §0.1, §4.3). The **normal lens** (`normal_lens_mm`) is the default for every shot's `lens_mm` (REASON-02).
- `step_change`: from a named scene the family shifts (B1 R15). A **lens exception** (LENS, `LX-`) allows one lens at named camera positions only (B1 §4.3; CRAFT-07).
- `default_height`: whose eye the lens sits at (B1 R6); `default_move`: `static`.
- `banned`: choices the film never makes, each with its why (B1 §9.2).
- `camera_speed: real_time`; `time_rule`: expanded action is built from overlapping real-time slices, never slow motion (K20, K30; CRAFT-16).
- `break`: **the break** is the one time the camera does the opposite of its rule, on the turn it serves (B1 P9, R24).

A **character camera rule** (CAMRULE, one per principal) says how the camera treats one person: `in_control`, `losing_control`, `never`, `closest` (a size at a story point), `limit_before` (nothing closer before `closest`), `eyeline`; a **story point** is a scene and a quote (B1 §9.2; FILM-03). Example `CR-ELI`: partial framings, eyes well off the lens, `never: push_in`, `limit_before: medium_close_up` until scene 13, his first near-lens look spent on "Now he looks at her." (line 811; B1 Ex3; K05).

A **saved choice** (RESERVE, `RC-`) names the choice, its `match` (how code recognises a use: `size = extreme_close_up`), most uses, where allowed and never on whom; card 09 adds the two film-level ones (B1 P5, §9.2). An in-story camera keeps its fixed position, lens, frame shape, frame rate and overlays in its CAMERA record (B1 R22).

## Slots and moves

Example: SC10-SH150 is `close_up`, `eye_level`, `height: eye:CH-IONA`, `lens_mm: 50`, `focus: moderate`, `move: static`: the scene's tightest frame on its main turn, with no push-in, because "Her face changes." (line 456) already marks the beat (B1 P11); the film's tightest size waits for scene 13 (K05).

Fill the six camera slots (fields) in B1's order, after `purpose` and `because` (B1 §0):
1. **Size** (`size`). Size equals importance now, and distance is emotional distance (B1 P2, P3). A scene's sizes approach, withdraw, hold or break (B1 §2.2). The turn gets the extreme its camera rules allow (B1 R1); equals get matched singles, same size, lens and height (B1 R3; GEOM-08); a breaking relationship moves from two-shots to singles, or from dirty to clean singles (B1 R4). A **single** holds one person, a **two-shot** two; an **over-shoulder** looks past one at the other; a **dirty single** keeps a soft sliver of the other person, a **clean single** none (B1 §2.1).
2. **Angle and height** (`angle`, `height`). Height is where the lens sits; angle is its tilt (B1 §0.1). `height: eye:CH-IONA` or `kneeling:CH-IONA`: the eye of the person whose point of view the scene holds (B1 R6). Low or high only on the beat power shifts: up at the winner, down at the loser (B1 R7); top-down for a machine's or institution's view (B1 R9); a Dutch tilt only while a perception is wrong, and only as a saved choice, a RESERVE record that rations it (B1 R8).
3. **Lens** (`lens_mm`). Stand first, then choose the lens: how near and far things compare in size depends only on where the camera stands (B1 P6, §4.1). A long lens from far away: closeness kept private (B1 R10); a wide lens close: a person pressed by the place (B1 R11); two people across a barrier: a long lens along the line between them, or the camera in the plane of the glass; a long lens shortens only distances toward the camera (B1 R13).
4. **Focus** (`focus`, `focus_on`). `moderate` for dialogue; `deep` when the audience must read something behind; `shallow` hides what the character ignores (B1 §4.5). A **rack focus** (sharpness moving from one plane to another) becomes two shots for AI video unless a test shows the tool can do it (B1 R14).
5. **Camera move** (`move`, `move_reason`). One per shot (B1 §13; CRAFT-06), with a named cause: a character moves or looks, or a sound draws attention (B1 P8). A **push-in** (the camera travels toward the subject) starts before the realisation and lands on the decision, at most `push_in_per_scene_max` a scene (B1 §6). A zoom is an observer's gaze, not approach (B1 §6). **Handheld** comes in on the exact beat control is lost (B1 R17). An impossible arrival happens in a static frame between cuts (B1 R20). If a cut does the move's job, cut (B1 R21). Orbit, zoom, whip pan, dolly zoom and drone only as saved choices; a crane above head height only for a view nobody in the scene has (B1 §6).
6. **Frame shape** changes only for footage inside the story, shown in its own shape (B1 R22).

A point-of-view shot (`frame: pov`, what one character sees from their eyes) comes in a short dose, then the face (B1 §3.2). A value that departs from its default needs a `why`: `angle` eye_level, `height` the owner's eye, `lens_mm` the normal lens, `move` static, `focus` moderate (REASON-02).

## Translation menus with pitfalls

Change one or two slots, leave the rest at the baseline, and tie the choice to a line, object or action (B1 §8):
- **In control:** medium clean singles, eye level, static. Pitfall: dull competence; show skill in inserts.
- **Losing control:** sizes jump tighter; handheld enters. Pitfall: shake before the loss.
- **Kept hidden:** partial framing. Pitfall: hiding so obviously the audience guesses.
- **Revelation:** an insert, then the face. Pitfall: insert, rack focus and push-in together.
- **Dread:** a static wide, deep focus; the threat never moves the camera (B1 §9.2; D10 §2.2).
- **Confession:** one size held, near the lens line. Pitfall: cutting the truth into pieces.

## Budgets and saved choices

`push_in_per_scene_max` and `extreme_close_up_per_scene_max`, on the main turn only: caps, not quotas (B1 P5; CRAFT-01 to CRAFT-03). Film-level: `extreme_close_up_film_max` and `push_in_scene_share_max` (FILM-08). A saved choice cites its RC in `because` (REASON-06; CRAFT-11). Consecutive shots of one subject change a size step or at least `geometry_angle_change_min_deg` (GEOM-02).

## The baseline is a strong answer

Static, the owner's eye height, a normal lens, room sound are choices, not failures. Depart only for a reason you can cite. The neutral fallback is never wrong and keeps the extremes available (B1 R25); a static frame can judge or trap (B1 §6).

## Cliché traps

Tests as in card 09.
- **Push-in on every realisation.** Fix: one, on the turn, starting before it (B1 §6, §14).
- **Low angle from the first beat; the monster from below.** Fix: eye level until power rises (B1 R7, §14).
- **Dutch tilt for tension.** Test: does the script say a perception is wrong? Fix: level it (B1 R8).
- **Crane-up on every sad ending.** Fix: a pull-back or crane-up ending on at most one scene ending in four (B1 R19).
- **Shallow focus everywhere; handheld as realism; slow motion for importance.** Fix: deep focus where the place matters; handheld only for lost control; real time, held longer (B1 §6.1, §14).

## Reasons that fail and reasons that pass

- Fails: "Low angle to make Saye powerful." Passes: "Eye level on Saye (CR-SAYE: she holds power by stillness, not angle); she wins at SC10-B11 by waiting." (B1 R7)
- Fails: "Push-in as she realises." Passes: "Static: 'Her face changes.' already marks the beat (B1 P11)."
- Fails: "85 for a cinematic look." Passes: "`LX-01`: camera A stands 6.3 metres back, through a wall removed for it, so both profiles in the reflection two-shot are the same size (B3 §6.3; K07)."

## Two worked examples

### The Catch, scene 10 (tense)

SH080, the reflection two-shot: camera A on the table's centre line, `lens_mm: 85` under `LX-01`, `frame_detail: symmetrical_profile`, one of `RC-01`'s two uses (K07, K22). SH150: the turn, above. SH190: the held wide from camera F through "She waits until Iona steps aside." (line 481): a turn about waiting takes a deliberate wide (A2 R4, R18).

### The Long Places, scene 5 (contemplative)

"She did not turn her head." (line 79): a static medium close-up in profile from her left, level, at her seated eye height, on a long lens; her right side, and whatever leans on it, hidden behind her own body. No push-in, pan or reverse: she refuses to look, so the camera refuses too (B1 Ex7; D10 §12.3).

## Self-check

Yes or no (B1 §13).
1. Does every camera-system line give a story reason?
2. Does every principal have a camera rule, kept?
3. Is the scene's most extreme framing the camera rules allow on its turn, nothing tighter before?
4. Is every lens in the family or a declared exception?
5. Does every move name its cause, one per shot?
6. Is what the story hides out of frame?

## Words for AI models

Works: "The camera holds completely still for the whole shot."; "The camera moves slowly closer to her face while she stays still." (B1 §15); one move per clip, saying where it ends; "over Iona's left shoulder toward Saye" (C3 §4). Fails: rack focus, dolly zoom, whip pan, zoom as distinct from push-in, "objective camera", a frame shape in the prompt (B1 §15; C3 §4). A lens number is a hint: write "compressed background, shallow focus" (C3 §4).

## Look up for more

`stage.py lib B1 §9`, `B1 §11` (R1 to R25), `B1 §2`, `§4`, `§6`, `§8`, `§12`, `§14`, `§15`; `C3 §4`; `D10 §2.2`; K05, K07, K20, K22, K24, K30.

---

From the skill file `cards/11 Light and colour.md`:

# Card 11. Light and colour

Step 6 reads "Lighting plan" and "Colour script"; at Detailed depth step 7 reads "Per-scene light" and step 8 "Per-shot light"; chat apps read it whole. "B2 R10" is rule 10 in B2 §7 and "B2 P7" principle 7 in B2 §1; "B2 Ex2" is worked example 2 in B2 §10.

## The job

In Saye's kitchen the only warm light is the lamp Iona holds, and when Saye says "Nothing has happened to the mint." (line 466) the light does not change (B2 Ex2). Light decides what the audience may see: attention first, feeling second, beauty third (B2 P1). Step 6 hands on one LOOK per place and time and one VISUAL row per sequence; steps 7 and 8 record only what differs from them.

## Questions in order

1. **What does the story already say?** Every light, colour and darkness word is binding (B2 §5.1, R3; COVER-08): the look carries a light at rest; a light that changes or moves (goes out, is held up) needs a light cue quoting its line, and that cue adds nothing (CRAFT-10). A colour describing a person ("grey and tidy") is not light. In prose, figurative light ("A question is a lamp you hold up on somebody", The Long Places, line 92) guides meaning only (B2 §5.1).
2. **What is each source, and where is it in the room?** (B2 P2)
3. **Which source reads as plain white?** (B2 §4.1)
4. **What stays dark?** (B2 P7)
5. **Whose face must be read?** Keep its eye light (B2 P8, R5).
6. **Can a story source change at the turn?** If not, hold the light (B2 R10).
7. **Is this sequence below the next peak?** (B2 R9)
8. **Do the motif colours survive this light?** (B2 §4.7, R15)

## Lighting plan

Example: `LK-SAYE-KITCHEN-NIGHT`: `main_light: Iona's lamp | colour: warm | quality: soft | from: TABLE`; `neutral_white`: the lamp; `contrast: medium_high`; `fill: low`; `stays_dark`: the room's corners and bare walls; `accent_allowed`: the mint's green (B2 §5.4; K22).

A **look** (LOOK record) is the light, colour and texture of one place at one time. Its **look block** is the two or three sentences pasted unchanged into every prompt there, within `look_block_sentences` and `look_block_words_max` (B2 §13.4). Fields, from B2's plan format (§5.3):
- `main_light`: the **main light** is the story source that lights faces in most shots: name it, its colour, its quality, and where it stands. **Hard** light comes from a source that looks small from the subject and gives crisp shadows; **soft** light from one that looks large (B2 P5). `from:` names a set-plan object or a wall (`north_wall`, `east_wall`, `south_wall`, `west_wall`, `ceiling`); code works out its frame side per shot and, in a mirror story, per era (card 16), so it flips lawfully with a mirrored picture (K03). With neither, the side stays `open`.
- `neutral_white`: the source that reads as plain white; every other source is warmer or cooler than it (B2 §4.1).
- `contrast`: `low` (gentle, open), `medium` (most drama), `medium_high`, `high` (one side of the face dark) or `extreme` (the shadow side goes black) (B2 §2.3).
- `fill` (`none`, `low`, `medium`, `high`): how far the dark side is lifted; little fill reads as secrecy or danger, much as openness (B2 §2.1).
- `stays_dark`: what the audience must not see yet (B2 P7).
- `palette`, `accent_allowed`: an **accent** is a small area of colour that stands out; keep the palette low in saturation around a motif colour, and keep that hue out of the set elsewhere (B2 R14, §4.7).
- `light_cue`: a **light cue** is a change of light the story causes, written as a story point (a scene and a quote) with its change and why (B2 §0.1).

Rules: a night interior takes one practical (a working lamp seen in frame) as its main light (B2 R1); a carried light lights what its carrier looks at (B2 R2); sourceless light only where the story leaves ordinary time (B2 R4); a machine's light dips once when the story says it falters, and never flickers otherwise (B2 R26); signals keep their real colours (B2 R19).

## Colour script

Example: The Catch opens at frame value 1, saturation 1 and extreme contrast in the tunnel, so contrast cannot climb at the climax; saturation and red against green are saved for the fire in scene 24, the only saturation 5 (B2 §8.5; K12).

A **colour script** is one VISUAL row per sequence, written before any shot, so the film's colour and light arc shows at a glance (B2 §8.1). Fields (B2 §8.2): `frame_value` 1 to 5 (how light the whole frame is, mostly black to mostly bright), `saturation` 1 to 5 (near grey to the film's most intense colour, used once or twice), `temperature` (warm, neutral, cool, mixed), `dominant`, `accent`, `main_light` (hard, soft, mixed), `contrast`, `exit` (how light leaves the sequence). At Detailed, `sub_row` items give scenes their own rows (K01, K13).

Steps (B2 §8.3):
1. Read each sequence's value change and the plan's peaks.
2. Write the colour logic: the story's oppositions and the motif colours the text supplies (B2 §8.4).
3. Assign peaks first, then the valleys lower: a sequence building to a peak sits at least one step below it in the component (saturation, contrast and so on) the peak spends (B2 R9). If the opening spends one component, the climax peaks in another (B2 §4.4).
4. **Monotony test:** no `colour_monotony_run` sequences in a row share frame value, saturation and temperature, unless the row says why (B2 §8.3; FILM-04).
5. Each motif colour appears only where its meaning applies.
6. Write each principal's colour arc in one line.

The film teaches its own colour meanings (B2 P4, R17); a warm-cool split names the opposition it stands for (B2 R16); a motif inverted once lands harder than one repeated (B2 R18).

## Per-scene light

Example: at scene 10's main turn, beat 7, the dial keeps `light: as_look`, because the script's point is that the world has not changed (B2 Ex2, R10).

The **dial** (SCENE `dial`) plans size, distance, height, light and sound for every beat. Its light stays `as_look` unless a story source can change at that moment: a door opens, a screen switches off, a lamp is set down, a machine falters (B2 R10). One light idea per scene, tied to the value change (B2 P10, §11). A cue falls on a turn and has a cause in the story (B2 §11); it never syncs to the line that states the point: offset it a beat, or let the world change it for its own reasons (B2 §12; FILM-09). A beat the script already marks gets no added light change (B4 R23; CRAFT-10), and a light change counts toward `signals_changing_per_beat_max` (CRAFT-19). The scene's one idea for light may be `holds_baseline`. Time passing inside one place moves in planned steps (B2 R22).

## Per-shot light

Example: scene 1's bolt-hole insert: the flashlight rakes in from frame-right across the empty bracket, everything beyond it black; on "She stays on her knees. One breath." (line 30) the beam stops and holds (B2 Ex1; K19).

Write SHOT `light` only where it differs from the look, else `as_look` (B2 §9). At Detailed add `dark` and `eye_light`: an **eye light** is the small reflection of a source in the eye that makes a face read as alive (B2 §0.1).
- Keep an eye light on anyone whose thought must be read (B2 R5). To show a character hiding something from another, hide a hand or object, not the face; lose the eyes only when the audience is kept out too (B2 R6, R7).
- The darkest shot keeps one readable element: a **rim** (a thin bright edge from a light behind), an eye light or a lit hand (B2 R23).
- Dark skin in low light: exposure and fill chosen for that skin, soft bounce and careful eye light, never just more front light; reject a take where darker skin goes grey, ashy or lost while lighter skin reads (B2 R24).
- Matte black shows by its rim against something lighter; an almost clear thing is lit from behind or the side (B2 R25, R25a).
- A face in a helmet gets its own light inside it (B2 R27); screen light matches the picture on the screen (B2 R29); the brightest costume keeps its fabric detail (B2 R28).
- The main light's side stays fixed to the set when the camera turns (B2 R20).

## Translation menus with pitfalls

Pick at most one per beat and tie it to a line, object or action (B2 §6):
- **Safety:** soft warm practicals, eye light on everyone. Pitfall: a greeting-card glow.
- **Threat kept hidden:** a mostly dark frame, light dropping away fast. Pitfall: too dark to read.
- **Truth revealed:** the flattest light available (B2 R11).
- **Institution:** flat top light. Pitfall: flickering tubes.
- **Unchanged world, changed person:** keep the light exactly as it was. Pitfall: a cue that "helps".
- **Care:** the carer holds the light. Pitfall: the halo.

## Budgets and saved choices

`look_block_words_max`; saturation 5 once or twice a film (B2 §8.2); one light idea per scene (B2 P10); `signals_changing_per_beat_max`; `added_emphasis_per_beat_max`, where a light change is added emphasis (B4 R23).

## The baseline is a strong answer

Static, the owner's eye height, a normal lens, room sound are choices, not failures; so is light held as the look. Depart only for a reason you can cite: a story source that changes (B2 P11, R10).

## Cliché traps

Test: can you name the lamp (B2 §12)?
- God rays in every interior. Fix: haze only where the place has dust, smoke or damp (B2 §5.2).
- Lightning at a revelation; a cold blue shift when the monster appears; flickering hospital tubes (B2 §12, §5.4).
- Teal-and-orange; candles for romance; a halo on the saint (B2 §4.8, §12).
- The AI house look: light shafts, rims, wet floors. Fix: name real sources in positive words (B2 §12).

## Reasons that fail and reasons that pass

- Fails: "Moody low-key light for tension." Passes: "The flashlight is the only source: Jude turns the tag into her beam to read it (line 16; B2 Ex1, R2)."
- Fails: "The light turns green on 'Drive.'" Passes: "The traffic light holds red a beat after 'Drive.', then changes by itself (B2 Ex3, §12)."
- Fails: a cue on "Not mint.". Passes: `light: as_look`: "Nothing has happened to the mint." (B2 Ex2).

## Two worked examples

### The Catch, scene 24 (the crisis)

The film's one saturation 5. Fire from the cabinet side and the faint green of her way home on the visor meet on Iona's face. At "She deletes the way home." (line 1412) the green leaves her face; when she fires, the cue is the loss of the white glare (line 1418), not darkness: the room still burns. Her eyes stay lit inside the helmet (B2 Ex4, R27).

### The Long Places, chapter VII (contemplative)

The finished room (line 587): the same small oil lamps, but a pale, unsooted ceiling bounces the flame, so the room is softer and brighter with no added source; the third shape sits at the edge of the falloff, with no rim and no eye light, because the story will not make it certain (line 597; B2 Ex6, R4, R23). Light stays source-true (D10 §2.2).

## Self-check

Yes or no (B2 §11).
1. Is every light, colour and darkness word covered?
2. Does every source have a colour, a quality and a place?
3. Does every cue fall on a turn, with a story cause?
4. Is one element readable in the darkest shot, and darker skin rendered richly?
5. Is this sequence below the next peak, and not a repeated row?

## Words for AI models

Works (B2 §13): named sources ("a mostly dark room lit only by one small lamp on the table"); colour on objects ("a small red tag on a grey steel gate"); direction as a result ("the left half of her face is in deep shadow"); "flashlight", never "torch" (K19). Fails: kelvin numbers, ratios, rig words, "practical", negatives ("no blue"), "cinematic lighting", named cinematographers, a light change inside one clip (make two clips).

## Look up for more

`stage.py lib B2 §5` (plans; §5.4 The Catch), `B2 §7` (R1 to R29), `B2 §8` (§8.5 The Catch's colour script), `B2 §9`, `§10` (Ex1 to Ex6), `§12`, `§13`; `B4 R23`; `D10 §2.2`; K03, K12, K19.

---

From the skill file `cards/12 Staging and composition.md`:

# Card 12. Staging and composition

Step 4 reads "Set plans"; step 6 "Visual structure"; step 7 (Standard) "Stations and configuration"; step 8 "Frame rules"; chat apps read it whole. "B3 R3" is rule 3 in B3 §7.2, "B3 P2" principle 2 in B3 §1, "B3 Ex1" worked example 1 in B3 §9.

## The job

In Saye's kitchen Iona walks between Saye and Eli ("Iona moves between her and Eli.", line 476), and Saye wins by standing still until Iona steps aside (B3 Ex1, R3). Bodies are read before words: where people stand, how far apart, who moves (B3 P1 to P3). Step 4 hands on set plans; step 6 each sequence's visual structure; step 7 the staging, marks, moves and setups; step 8 each frame's placement, glass and dominant.

## Questions in order

1. **Where is everything?** A set plan, anchor and exits (B3 §6, §5.1).
2. **Who holds power, and who moves?** (B3 §4.2, R3)
3. **How far apart, and does it change only with a value?** (B3 P2, R2)
4. **Does the configuration change on the turn?** (B3 §4.9, R1)
5. **With three or more: the engaged pair, the silent third, the pivot?** (B3 §4.4, R5)
6. **Where is the line, and the camera's side of it?** (B3 §5.2)
7. **What does each frame show first?** (B3 §3.1)
8. **Is there a barrier, and whose side is the camera on?** (B3 R11)

## Set plans

Example: `LOC-SAYE-KITCHEN`: `size: [6.0, 3.6, 2.5]`, `origin_corner: south-west inside corner`, `axes: +x east, +y north`, `wild_walls: west wall`; `TABLE | at: [2.8, 1.8]`; marks `IONA_MARK | at: [2.8, 2.55]`, `SAYE_MARK | at: [2.8, 1.05]`; anchor: the table with Jude on it (B3 §6.3; K22).

A **set plan** is a top-down map of a place in metres, which code turns into frame positions, eyelines and previs, the grey 3D stand-in renders (B3 §6). Step 4 writes one for every place used by a shot likely to need previs level `previs_plan_level_min` or more, a reflection or glass shot, or three or more people in one space; at Detailed, for every place. Fields:
- `size`, `origin_corner`, `axes`: metres from a named corner, +x east, +y north.
- `wild_walls`: a **wild wall** can be removed so the camera can stand where it was (B3 §0.1).
- `object`: NAME, `at`, `size`, `base`, `material`, `meaning` (what it means in the story), `furniture`.
- `mark`: a **mark** is a named position where a person stands, sits or lies at a given beat (B3 §0.1).
- `anchor`: the **anchor** is a fixed object seen in most shots, keeping the geography clear (B3 §5.1); `exit` items with `leads_to`.

Rules: each person gets a mark and a facing target, a name or point, never "left" (B3 §6.3). A distance the prose gives as a feeling becomes a named mark, reused whenever the phrase returns (B3 P10, R19). `plan_orientation` is the orientation of the place's first appearance on screen; code derives the mirrored plan (x becomes width minus x; a facing angle θ becomes 180° minus θ), so never hand-edit a derived plan (B3 §5.4; K02). Claim no frame position code has not projected (B3 §11; GEOM-06).

## Visual structure

Example: sequence 3, the wrong world (scenes 7 to 10): limited and flat space, horizontals, affinity in camera and space, so the only contrast is the reversed world itself (B3 §2.7, P5).

**Visual structure** is Bruce Block's plan for how the picture rises and falls with the story (B3 §2). Every picture is built from seven **components**: space, line, shape, tone, colour, motion, rhythm (B3 §2.1). **Contrast** (difference within a component) raises visual intensity; **affinity** (sameness) lowers it (B3 §2.2). Space is **deep** (lines running away, motion toward the lens), **flat** (frontal planes, motion across), **limited** (frontal planes stacked in depth, nothing moving toward the lens) or **ambiguous** (size and position unreadable) (B3 §2.3).

Each VISUAL record writes `space`, `component` items (`plan: hold`, `progress` or `contrast`, with `why`) and `counterpoint` (B3 §2.6):
1. Read the sequence's scene intensities and the plan's peaks, the film's maximum moments.
2. For each component, one sentence: what it does in quiet stretches, at peaks, at the end.
3. Name any **counterpoint**: calm picture under a story peak, justified in one sentence (B3 §2.5).
4. Name choices kept for the peaks only.

At a peak, raise contrast in no more than two components (B3 R7; FILM-05); after a high-contrast sequence, strong affinity (B3 R8). A limited space turns deep when someone walks toward the lens: save that for an intrusion (B3 §2.3).

## Stations and configuration

Example: scene 10's stations are the table, the counter with the flask and phone, and the space between Saye and Eli; at beat 10 Iona moves into that space, at beat 11 she steps aside (B3 Ex1).

SCENE `staging` is one line placing everyone, or "staging assumed" when the story is silent (A2 Step 9). A scene over `stations_needed_above_beats` beats names `stations_per_scene` **stations**: marks each tied to a part of the scene, the route between them part of the story, toward the door for escape, toward the other person for appeal (B3 §4.7).
- The **configuration** (who stands, sits, faces whom, how far apart) changes on every turn, written in BEAT `change`; identical before and after means the turn is missed (B3 §4.9, R1).
- Between turns a body moves only for a want or task you can name; distances change only when a value's charge changes (B3 P2, P3, R2).
- The one holding power stays still while the other moves; standing up on a turn takes the scene; **interposition**, stepping between two people, plays in one wide that sees all three (B3 §4.2, R3, R4).
- Distances in metres, with Hall's zones: intimate, personal, social, public (B3 §4.2).
- Three people: per beat name the **engaged pair** (the two in the exchange) and the **silent third**; the **pivot** stands between the others and moves the line with a turn of the head; keep the silent third visible when their reaction matters (B3 §4.4, R5; A1 R5; CRAFT-24). Four or more: subgroups, one master side (B3 §4.5).
- With a set plan: `start` per character (mark, facing, posture); MOVE records, each a **floor-plan move** with beat, from, to, timing, facing and why; SETUP records, each a **setup** (a camera position) with its lens and side of the line. A move the story does not write is `origin: invented`, in `additions` (B3 §10.2).
- **The line** (line of action) runs through the engaged pair; the camera keeps one side per part and crosses only inside a shot or on a beat that reverses the relationship (B3 §5.2, R16). One staged wide can replace several singles (B3 §4.1).

## Frame rules

Example: SC10-SH080 puts Iona frame-left facing right and Saye frame-right facing left, each raising the hand nearest the camera, with Jude, the lamp and Eli on the centre line (B3 §8.2; K07).

- Name the **dominant**, what is seen first; at least three attention cues agree on it, and none of face, motion, brightest area or sharpest focus points elsewhere (B3 §3.1).
- Thirds is the neutral baseline; centre, edge or symmetry needs a story reason, and symmetry belongs to ritual, confrontation and mirrors (B3 §3.2, §3.3, R12).
- **Lead room** (space in front of a face, the way it looks) about two-thirds of the width; **headroom** with the eyes on or just above the upper third line; **short-siding** (facing the near edge) only where something is behind or cut off (B3 §3.5). Paired singles mirror each other (GEOM-01, GEOM-08).
- For waiting or dread, leave the empty side of the frame toward where the absent person would come (B3 §3.4).
- One frame within a frame (a door, window or screen framing part of the picture) and one expressive device (a barrier, reflection or short-siding) per shot (B3 §3.7, R25); a foreground object frames, blocks or comments, or goes (B3 R13); a short shot keeps the dominant where the last one was (B3 R14).
- Keep the camera on its side of the line: an exit frame-right enters frame-left; a change of direction shows inside a shot (B3 §5.2; GEOM-03, GEOM-07). Directions describe the final picture, after any flip (B3 R22).
- Every pane in frame gets `glass`: state `clear`, `marked`, `reflecting`, `screen` or `broken_open`; camera `through`, `along` or `angled` (B3 §8.1). A reflection shows only against something darker: to lay A's reflection over B, put the camera on the line through A's mirror twin and B (B3 R28); clear glass needs the camera's side darker (B3 R29). Facing frame-right shows the right side, so the right hand is nearest the camera (B3 §8.2; card 16).

## Translation menus with pitfalls

At most one composition and one staging choice per moment (each row: composition / staging), preferring staging, tied to an object, line or action (B3 §7.1):
- **Control:** symmetry / fixed marks. **Isolation:** negative space / beyond social distance.
- **Power held:** height / holds still, holds the doorway.
- **Divided:** a surface division / a barrier. **Reconciliation:** the gap closed by both.
- **A world turned over:** an earlier frame repeated, one thing reversed.
Pitfall: all at once, the stock version of every film.

## Budgets and saved choices

`stations_per_scene`; `acting_characters_per_clip_max` (CRAFT-15); one major move per AI clip (B3 R21); hands on glass only where the script has them, same insert framing, one thing changed each time (B3 §8.3, R20, R27); perfect symmetry only as a saved choice (B3 §2.7).

## The baseline is a strong answer

Static, the owner's eye height, a normal lens, room sound are choices, not failures; so are thirds, matched singles and marks held between turns. Depart only for a reason you can cite (B3 P5, §4.1).

## Cliché traps

Test: would this fit any film (B3 R26)? Fix: the script's own object, carried by one department (B3 §11):
- Stand-and-deliver singles in a scene with a turn; moves "for variety".
- Rain on the window, a wilting plant, a ticking clock, bars of blinds, a stare into a mirror (B3 R24).
- The barrier marked in every shot; symmetry as style; hands on glass with music.

## Reasons that fail and reasons that pass

- Fails: "She crosses to the window for variety." Passes: "IONA between Saye and Eli at SC10-B10; why: 'Iona moves between her and Eli.'" (B3 R4)
- Fails: "Symmetry for a striking image." Passes: "`RC-01`: 'like a woman and her reflection' (line 428)." (K07)
- Fails: "They sit apart to show distance." Passes: "GOOD_DISTANCE, 2.4 metres, reused whenever 'the good distance' returns." (B3 Ex5, R19)

## Two worked examples

### The Catch, scene 13 (three on one side of the glass)

Jude, in bed between the siblings, is the pivot; the three face the monitor they talk through, and the master looks through the glass from Saye's side. At "Looks at her brother. Not at Jude." (line 742) the line swings to Iona and Eli, over Jude. "All three of them flinch at the same moment." (line 826) needs one frame (B3 Ex2, §8.6; A2 R7; K06).

### The Long Places, chapter II (contemplative)

The girl in the corner "where the wall gives its shoulder" (line 92); the lamp set down; the keeper at GOOD_DISTANCE, 2.4 metres. One low static camera all night; the keeper never moves; only the girl's mark changes, "Near morning" (line 102), by degrees (B3 Ex5, R3, R19).

## Self-check

Yes or no (B3 §10).
1. Does the set plan have an anchor, exits, marks and facing targets?
2. Does every move have a beat and a why?
3. Does the configuration change on each turn, and only there?
4. Is the line written per part, the pivot and silent third named?
5. Is every staging addition logged?

## Words for AI models

Works (B3 §12): positions as parts of the image ("on the left side of the image, facing right, with open space in front of her face"); "in the foreground", "in the background"; "the table between them". Fails: "lead room", "short-sided", "180-degree rule", "frame-left" (read as the character's left), exact metres, which hand is raised. Previs beats words for blocking.

## Look up for more

`stage.py lib B3 §2`, `B3 §3` to `§6`, `§7.2` (R1 to R29), `§8` (glass), `§9`, `§10` to `§12`; K02, K06, K07, K22.

---

From the skill file `cards/13 Cutting, rhythm and sound.md`:

# Card 13. Cutting, rhythm and sound

Step 6 reads "Sound plan"; step 7 (Standard) reads "Scene rhythm"; step 8 reads "Cut points and sound"; chat apps read it whole. "A4 R4" and "A4 SND7" are rules in A4 §9; "D9 R3" is rule 3 in D9 §3.

## The job

In The Catch the fall ends on "A hard metal CLACK." and "BLACK. A dark with nothing in it. One instant." (lines 259-261): the CLACK lands on the first black frame, true silence follows, and "Her eyes open." brings every sound back (A4 WE1). This card decides where cuts fall, how long shots run, how shots join and what is heard (A4 §0), handing on SOUNDPLAN (step 6), scene rhythm (step 7) and shot timing, cuts and sound (step 8). A **turn** is the beat where a value changes for good (card 03).

## Questions in order

1. What editing and sound marks does the text write? They outrank every other rule (A4 §5.1, §9).
2. What is the music policy; where are the planned ruptures (D9 P4; K12)?
3. Is the turn an event or a realization (A4 R4)?
4. Who knows what (A4 S2)?
5. What pattern does the scene teach; where does it break, once (A4 P7)?
6. Why does each cut fall where it does (A4 P3)?
7. Which one sound must be heard now (A4 SND7)?

## Sound plan

Example: The Catch defaults to `music_policy: none` (K31), so the pump, "three strokes, not quite even" (line 852), is its sound motif, at sound emphasis 3 only over black at the end (K12; B4 M10). The planned sound rupture is scene 26, where the ship's hum stops: "The sick motor through them." / "Then not." (lines 1508-1510).

- The **music policy**: `none`, `sparse`, `scored`, or `source_only`, music the characters hear (D9 §5).
- A **rupture** is the film breaking its own pattern at a turn: a change in the telling, not a loud event (A4 §6.8).
- The **device budget** caps the editor-made cut to black, true silence and freeze (A4 P10).
- A **sound motif** is a returning sound with one rhythm and timbre; only its path and loudness change (A4 §7.4).

Rules:
- `music_policy` is the user's (checkpoint B): propose, never set. Every clip stays music-free (`clip_audio`; D9 P1, P4).
- Propose `none` when the story gives no reason for score (D9 R1). `sparse`: few cues, each at a paragraph break (title, act change, end), never under an open reveal (D9 R3; A4 SND5). Under `none` a drone needs a source in the world, such as the ship's hum (D9 R4); a radio the story names plays murmured speech, never a tune (D9 R4a).
- A MUSIC cue has `in`, `out`, `function`, `must_not` and `licence`; it enters on a motion or a cut and leaves before or on a rupture (A4 §7.6; D9 §4.2).
- `device_budget`: one item per device, `max` from `device_budget_short`. Marks the story writes, and freezes a character makes on a screen, do not count (A4 §13; CRAFT-12).
- `rupture_plan`: one line per planned rupture, from PLAN's `peak` items; two devices at one moment only at the film's largest turn (A4 §6.8, §6.9).
- At most `sound_motif_max` sound motif, recorded once as a master sound, its rhythm in the MOTIF's `signature`; each appearance is a copy with its own path and `sound_emphasis`, emphasis 3 once per motif (D9 P2, R12; B4 §3.4).

## Scene rhythm

Example: The Catch scene 13 is a slow burn, long holds on the recording broken by her thumb on the remote and the freeze; scene 6 builds, breaks and lets the aftermath sit; scene 5 builds and cuts out into the cage (A4 §6.2).

The **rhythm shape** is the curve of shot lengths across a scene; the **average shot length** (`target_asl_s`) is screen time divided by the number of shots.

1. **`rhythm_shape`** (A4 §6.2): `build_and_cut_out` when the turn launches action into the next scene; `build_rupture_aftermath` when the turn is a loss, shock or revelation to absorb; `slow_burn` for talk, waiting or watching that turns on one line, look or discovery; `steady` only for a scene with no turn. Plan the curve before any duration: "build 4 s to 1.5 s over B1-B6; rupture B7; aftermath 5 s+" (A4 §10).
2. **`target_asl_s`**: speech shots from their time floors (the least time their words need), others from `non_dialogue_seconds_by_intensity` (K10; A4 §6.1), times the tone's `shot_length_factor` in `tone_defaults.json` (D10 §2.2); never from `rhythm_class_asl_s`, which feeds only the estimate (D13 §5). After a scene at `high_intensity_scene_min` or more, the next target is longer (FILM-07; A4 §6.9); the film stays inside `film_asl_range_s` (TIME-07).
3. **The main turn gets an extreme** (A4 R4, P5; TIME-10): the scene's shortest shot for a physical event (an impact, a fall, a black), its longest for a realization, a choice made, a revelation or a refusal. A turn that is both: the event gets the shortest shot, the realization after it a hold longer than its neighbours.
4. **Suspense**, the audience knowing a danger a character does not, holds longer on the unaware and never cuts faster (A4 S2; TIME-09).
5. **`rupture`** on the main turn or the beat causing it: a `device` (`hold`, `drop_out`, `true_silence`, `cut_to_black`, `camera_change`, `pov_change`) and `breaks`, the pattern taught first; one re-orienting shot follows. A gunshot is action, not a rupture, unless the telling breaks too (A4 §6.8).
6. **`room_sound: as_place`** unless the story changes the place's sound; in the dial (the per-beat plan) `sound` stays `room_sound` except at the rupture or a story source, never on a beat the script marks (blueprint step 7; B4 R23; CRAFT-10).

## Cut points and sound

Example: in The Catch scene 6, "Closes her eyes." is cut on the eyelids closing, and "This time they hear it land." (line 298) is the sequence's longest shot, its decay running under scene 7's "Tell me that was the brake." (line 305) as an L-cut (A4 WE1).

A **split edit** changes sound and picture at different moments: a **J-cut** starts the next shot's sound early; an **L-cut** lets this shot's sound run on. **Room sound** is a place's steady background, so no silence is dead (A4 §1, §7.3).

- `cut_out_on` (`thought_complete`, `action_midpoint`, `line_end`, `sound_hit`, `rhythm`, `keep_hidden`; at Detailed also `cut_in_on`): cut when the thought changes (a look, a breath, a word that hits), not at every line end (A4 P3, §3.7). Unsure: cut later (A4 R2).
- An action crossing a cut: cut mid-action, the whole action in both clips (A4 R3); cutting away: let the motion rest first (D11 R9). A reaction follows the event fully seen, unless hiding it is the point, `cut_out_on: keep_hidden` (A4 R7).
- `screen_time` never under the time floor code derives, the least time its speech, text and pauses need (TIME-01; K09, K10). Consecutive shots of one subject change a size step or at least `geometry_angle_change_min_deg`, unless it is a jump cut (A4 C4; GEOM-02).
- A CUT only where the join is not a plain cut: `j_cut`, `l_cut` (with `split_s`, `sound_across`) are free (A4 SND6); `match_cut` names the shared shape, motion or sound in its `why` (A4 T3); `dissolve`, `fade`, `cut_to_black`, `freeze`, `smash_cut` only where the story writes them (A4 T5; CRAFT-13), `cut_to_black` with `black_frames` and what the sound does (A4 T4).
- `hear` each speech (`speaker: on_screen`, `off_screen`, `hidden`); a listener shot hears it off screen (A4 AI7); a speech over `clip_speech_rule` splits at a phrase under a listener shot, each shot's `words:` the run it hears (A4 AI5).
- `effect` items (`at`, `sound_emphasis`) for sounds tied to actions; every sound the script writes in capitals becomes an effect, the room sound or a MOTIF appearance (COVER-07).
- `silence`: `none`; `room_sound_only`, room sound plus one small real sound; `drop_out`, the background suddenly thins, a rupture; `true_silence`, nothing, from the budget (A4 §7.5, SND4).
- `music: none` under an open reveal or a beat with an `unsaid`, a thought not spoken (A4 SND5; FILM-09).

## Translation menus with pitfalls

Pick at most one per beat; tie it to a line, object or action in this story (A4 §8):
- Rising pressure: shorter shots, one more sound layer. Pitfall: music.
- Dread: longer holds on the unaware, one off-screen sound. Pitfall: faster cutting.
- Shock: the shortest shot, a loud sound, then quiet. Pitfall: a sting where the script marks the beat (B4 R23).
- The world indifferent: a machine carries on (A4 §7.1).

## Budgets and saved choices

- `device_budget_short` (CRAFT-12); `pause_tiers`, `long_pauses_per_scene_max`; a `hold` beyond the long tier needs a saved choice (K10; TIME-04, TIME-08).
- `turn_reaction_min_s` after every turn (TIME-05); `sound_motif_max` (FILM-10).
- A sound change counts toward `signals_changing_per_beat_max` (CRAFT-19); `added_emphasis_per_beat_max` (CRAFT-10); `named_sounds_per_prompt_max` (GEN-17).

## The baseline is a strong answer

A plain cut, room sound, `silence: none` and `music: none` are choices, not failures, and need no `why` (blueprint 5.4 rule 11). Depart only for a reason you can cite: a written mark, the turn, the rupture plan (A4 T1, SND4, SND5).

## Cliché traps

- **Cutting on every line.** Test: shot count equals line count. Fix: cut on beat changes, L-cuts to the listener (A4 §13).
- **The average peak.** Test: the turn shot as long as its neighbours. Fix: make it the scene's shortest or longest (A4 R4).
- **A sad cue under unspoken sadness.** Test: does the frame tell the beat with the music off? Fix: remove it (A4 SND5).
- **Dissolves the script never wrote.** Fix: a cut; light and room sound carry the gap (A4 T2, T5).
- **Dead silence; room sound jumping at cuts; a last sound cut mid-pattern.** Fix: room sound under every silence, even across cuts; let the last sound finish (A4 SND4, AI4, SND8).

## Reasons that fail and reasons that pass

- Fails `music: MU-01` "to build tension" (REASON-04). Passes `music: none` (K31): the pressure has a story source, "The hum under the floor wavers." (line 1311) (D9 R4).
- Fails a dissolve into scene 8 "to show time passing". Passes a plain cut: the script only cuts, and "Two streets away. Her car, where she left it." (line 335) carries the gap (A4 T2, T5).
- Fails scene 10's turn shot at average length. Passes SC10-SH150 as its longest: "Her face changes." (line 456) is a realization (A4 R4).

## Two worked examples

### The Catch, scene 30 (the pump over black)

Hold the vessel on the cloth through two pump cycles after "The tapping stops.", lowering the room sound. The story writes "CUT TO BLACK." (line 1848): a CUT with `black_frames` in the rest between cycles and `sound_across: MO-PUMP`, so the dark opens on one whole "Three uneven strokes in the dark." (line 1850). No music; the pump goes on or recedes, never stops dead (A4 WE3, SND8).

### The Long Places, chapter VII (contemplative)

"For three days the little rig argued with the hill" (line 573): a montage, short shots compressing time, cut on the drill's note, each day a jump cut in one repeated framing of Melek. The rupture is "the drill's note went hollow" (line 575), `device: drop_out`, then a hold on Márton in room sound only. The lost camera is heard, not seen, "a knuckle on wood, once." (line 581): one small knock, no bounce, because it plants "It is a cylinder. They stand, or they roll." (line 593) (A4 WE4; D9 §8.4).

## Self-check

1. Every written mark honoured, no join added?
2. Each main turn's shot the scene's shortest or longest, by the kind of turn?
3. At most one rupture per scene, on the turn, after a taught pattern?
4. Cut reasons, room sound and silence grade on every shot?
5. Every clip music-free, every cue inside the policy?

## Words for AI models

Works: only what happens inside the clip: speech with its speaker, sounds tied to visible actions, the room sound, "No music." (A4 §7.8); for a listener, "listens, does not speak" (A4 AI7). Fails: "then cuts to" (A4 AI2); split edits or motifs, which live in CUT and MOTIF records; asking for silence, which models fill; make it in the edit (A4 §7.8); feelings or artist names in a music prompt (D9 §4.3).

## Look up for more

`stage.py lib A4 §9`, `A4 §6`, `A4 §7`, `A4 §11`; `D9 §3`, `D9 §4.2`, `D9 §8`. `D10 §2.2`, `D13 §5`; K10, K12, K31.

---

From the skill file `cards/14 Shot design.md`:

# Card 14. Shot design

Step 7 reads only "The one-line shot list"; step 8 reads only "Full shots"; chat apps read it whole. "B1 R6" is rule 6 in B1 §11, "B1 P11" principle 11 in B1 §1; "A2 R4" is rule 4 in A2 §7, "D15 R6" in D15 §3.

## The job

Shot 150 of The Catch's scene 10 is its turn shot, a close-up held on Iona through "Not mint." and Saye's answer, because "Her face changes." (line 456) puts the turn inside her. Shots are the last thing written, from the turn pictures and the dial (A2 Step 9). Step 7 hands on the one-line list (every shot's ID and count); step 8, one full SHOT per item.

## Questions in order

1. **Whose scene is this beat?** Put the lens at that person's eye height (B1 R6).
2. **Is this beat a turn?** Give it the scene's most extreme framing: closest if the turn happens inside a person, widest if it leaves them alone or waiting (B1 R1, A2 R4).
3. **Has the script already marked the beat** (a line, a look, a change of state)? Then the camera adds nothing (B1 P11, B4 R23).
4. **Is someone hiding a feeling?** Keep them one size wider than the progression would reach, except on a turn (B1 R5, R1).
5. **What must the audience get from this shot, and which records justify it?** (A2 Step 9; REASON-01)
6. **What does the body do, and what stays still?** (D15 P1, P4)
7. **How long must it stay up to be read?** (K08 to K10)

## The one-line shot list

Example: `SC10-SH150 | beats: SC10-B07, SC10-B08 | role: turn | size: close_up | frame: single | subject: CH-IONA | time: 15 | shows: Iona chews, stops, chews once more; "Not mint."; we stay on her through Saye's answer`.

The **one-line shot list** (SHOTLIST `item`) fixes each shot's ID, beats, role, size, frame, subject, seconds and one line of what we see, before any detail. IDs come from the handout's issued block, in steps of `shot_number_step`; an insert takes a number between (SH155); end cards and black use `end_card_numbers` (ID-03, ID-06). At Quick depth these items are the final shots.

Write them in this order (A2 Step 9):
1. **Turn shots** (`role: turn`), one per turn, from the **turn pictures**, the one-sentence frames each turn must show, written at step 7 before any shot (CRAFT-04). The main turn takes its ladder rung's size, and nothing tighter comes before it unless the rung plays it wide on purpose (A2 R4, R31; CRAFT-03); with no rung, the most extreme framing its camera rule and the saved choices allow. Through one fixed in-story camera, what the frame shows and the cuts carry the turn, not size (B1 §10.5, R22). A later turn gets its part's tightest size or a deliberate wide.
2. **Must-keep shots** (`role: must_keep`): plants, reveals and the geography of a new place. A fact's reveal shot is a turn or must-keep shot (INFO-02); a new place gets who-is-where in its first one or two shots (A2 R29).
3. **The rest**, until every beat and every line is covered (COVER-02 to COVER-04). A new beat changes the image; a repeated tactic keeps one setup (camera position); a beat with no words still gets its shot, in full view (A2 R1 to R3).

**Coverage from the dial.** The **dial** gives each beat a planned size, distance and height, drawn toward the turn and away from it; list sizes stay within `size_step_difference_warning` steps of it (CRAFT-17). SCENE `coverage` is `designed` (each shot planned for its beat), `chained` (each starts where the last ended, for continuous physical action), `master_and_coverage` (a wide of the whole action plus closer shots; hardest for AI, since no performance repeats exactly) or `oner` (one shot) (A3 §5.6, R16).

Rules for the list:
- In dialogue, plan singles that need not match frame for frame, and keep the wide for the start and the turn (A3 §5.6); one staged wide can do the work of several singles (B3 §4.1).
- Several people reacting at once share one frame (A2 R7).
- Estimate seconds from the speech and pauses in the item's beats (A2 Step 9); a shot without dialogue starts from `non_dialogue_seconds_by_intensity` (A4 §6.1). Step 8 holds each full shot to its floor.
- The main turn's shot is the scene's longest or its shortest (A4 P5; TIME-10), and the written shots keep the list's total: TIME-03 warns past `scene_total_tolerance` of the list, and when the list is over twice or under half the first estimate's guess.

## Full shots

Example, from the turn shot: `purpose: Iona's body admits what her words denied; Saye's proof lands on her face.` `because: SC10-B07, SC10-V1, MO-MINT, CR-IONA`. `why: "Her face changes." puts the turn inside her mouth, so the scene's closest frame is spent here and held while Saye's proof lands off screen.`

Write each SHOT reason first: `purpose`, `because`, `role`, then the camera.
- `purpose`: one sentence saying what the audience must get; it names a change (A2 Step 9; REASON-01).
- `because`: the ID of any story record that justifies the shot (scene, beat, value, character, state, place, prop, text, motif, rule, plan, camera rule, saved choice, look, fact, plant) or a `line:` reference; SCENE and SHOT take the same set. `default` only on a normal shot with no departure (REASON-01). A turn shot cites its turn beat (REASON-05); a saved choice (a rationed choice, RESERVE) cites its RC (REASON-06).
- `why`: one sentence that quotes a line, names an object or action, or cites an ID, never a mood (REASON-03, REASON-04). Always on turn shots. Otherwise needed wherever a field departs from its default: `angle` eye_level; `height` the eye of the whose-scene character (the person whose point of view the scene holds) or of the subject; `lens_mm` the normal lens of CAMSYS; `move` static; `focus` moderate; `light` as_look; `room_sound` as_place; `silence` none; `music` none; `display` 1 in a close-up or tighter. `size` and `frame` never need one (REASON-02).
- **The camera slots**, in order: size, angle and height, lens, focus, camera move, and frame shape only for footage inside the story (B1 §0; card 10). One camera move per shot (CRAFT-06).
- **Behaviour, not emotion.** `does` holds visible behaviour, never emotion words (WORDS-01; A3 R2). A line that names a feeling ("Her face changes.") becomes two or three timed steps (D15 R1). **Display** is how openly a face shows: 1 contained, 2 visible, 3 open; the closer the shot, the lower the level, and `display: 3` at `display_3_needs_why_at_or_tighter` or tighter needs a `why` (D15 §2.2; CRAFT-25). `still` names what does not move, required on any hold of `hold_needs_still_s` or more (D15 R6; CRAFT-26). `eyeline` takes a `dwell_s`; `must_not` holds a look saved for a later beat (D15 R9, R10).
- `moment` items: timed visible changes inside the screen time, no more main actions than `main_actions_per_seconds` allows (TIME-02, TIME-06); `end` is the last picture.
- **Reading floors.** Code works out each shot's **time floor**: speech at the voice's pace (`speech_wps_default` unless the voice differs) plus `speech_floor_extra_s` a speech, or text by `text_floor`, whichever is longer, plus the pause owed, with `turn_reaction_min_s` after a turn. `screen_time` sits at or above it; never type the floor (TIME-01; K08 to K10).
- `held: yes` where meaning depends on not cutting; turn shots count as held (GEN-10).
- The film-level extreme close-up and push-in (the camera travelling toward the subject) are spent only where their RESERVE allows (FILM-08).
- At the main turn at most `departments_changing_at_main_turn_max` departments change, named in `scene_idea` (B3 R7; B1 P11; CRAFT-19). Holding the baseline is a full **department idea**, the scene's one idea for camera, light, staging, sound or design (`holds_baseline`).
- When rules disagree, the higher wins and the `why` names it: the story, readability, physical honesty, systems and budgets, flaws, turns, emotion over continuity, conflict type, beat defaults, the baseline (A1 §6; B1 §11; B2 §7; reference/04).

## Translation menus with pitfalls

Pick at most one per beat; tie it to a line, object or action in this story (A2 §7):
- **A turn inside a person:** the closest size, held (B1 R1). Pitfall: a push-in plus music.
- **A turn about waiting:** a deliberate wide, held on the one waited on (A2 R4, R18).
- **A revelation:** an insert of the evidence, then a held close-up of the receiver (A2 R8).
- **An action turn:** one frame showing the action and its result (A2 R9).
- **A plant:** the same size and length as its neighbours, no push-in (A3 R22).

## Budgets and saved choices

Per scene: `push_in_per_scene_max`, `extreme_close_up_per_scene_max`, `long_pauses_per_scene_max`. Per beat: `signals_changing_per_beat_max`, `added_emphasis_per_beat_max`. Per clip: `acting_characters_per_clip_max`. Film: `extreme_close_up_film_max`, `push_in_scene_share_max`. Caps, never quotas (B1 P5; B4 R23).

## The baseline is a strong answer

"Static, the owner's eye height, a normal lens, room sound are choices, not failures. Depart only for a reason you can cite." A normal shot with no departure may give `because: default` and no `why` (REASON-01).

## Cliché traps

Tests: **any-film** (would this reason fit any film with this theme?), **mood-word** (does it name only a feeling?), **stacking** (more than one signal on one beat?), **sound-off** (does the frame tell the beat without sound?) (B3 R23, R26, §10.1; B1 P11):
- Push-in on every realisation; low angle from the first beat; Dutch tilt for tension; crane-up on every sad ending; shallow focus everywhere (B1 §14).
- God rays, lightning at a revelation, flickering hospital tubes, teal-and-orange (B2 §12).
- Rain on glass, ticking clocks, wilting plants, empty chairs (B3 R24; B4 R25).
- A sad cue under unspoken sadness; dissolves never written (A4 §7.6, §13, T5).
- **Default coverage**, the opposite failure: every scene wide, over-shoulders, singles, or one static frame repeated. Test: do all lists share one shape? Fix: design from the turn (B1 §14; FILM-06).
Fix: the baseline, or this story's own line, object or action.

## Reasons that fail and reasons that pass

- Fails: "Close-up to show her shock." Passes: "The scene's tightest size, spent on its main turn (SC10-B07): 'Her face changes.' puts the change inside her." (B1 R1)
- Fails: "Low angle to make Saye powerful." Passes: "Eye level on Saye (CR-SAYE: she holds power by stillness, not angle); she wins at SC10-B11 by waiting." (B1 R7)
- Fails: `does: horrified`. Passes: `does: chews slowly; stops chewing; a small frown; chews once more, slowly` (D15 R1).

## Two worked examples

### The Catch, scene 10 (tense, 20 shots and a title card)

SH080, the reflection two-shot, both women in one frame (`RC-01`); SH090 and SH100, the ring inserts, edited stills with `flip: never` (K07); SH150, the turn; SH160, Saye's one look afterwards (A1 R19); SH190, the held wide through the wait, the second turn; SH200, "Nobody leave this room." (line 484); the cut `SC10-C200`, `type: cut_to_black`; SH990, the title card.

### The Long Places, scene 5 (contemplative)

Three shots in about 110 seconds: the mouth at night, wide, static; a static medium through one out-breath of the shaft; the warmth shot, a static profile medium close-up, held, no reverse. "She did not turn her head." (line 79) gets the held frame, and the warmth stays behind her body (D10 §12.3; B1 Ex7, P7).

## Self-check

Yes or no (B1 §13; A2 §9; D15 §8).
1. Is every shot before the turn shot at its size or wider?
2. Is every beat and every line covered?
3. Is every `does` free of emotion words?
4. Is everything that must not move written in `still`?
5. Does every `why` fit only this film?
6. Is every screen time at or above its floor?

## Words for AI models

Works: one camera move and one action per clip, as timed steps with an end state (C3 §5); behaviour, not labels: "She stops chewing. Her eyes lose focus and drift down; her lips part slightly; she holds very still." (C3 §6); "The camera does not move." on a hold (D15 R6); "she listens; no dialogue" for a listener (A1 §11). Fails: emotion words; purposes and reasons in prompt text (GEN-15); parted lips in silence without "No dialogue." (D15 R7).

## Look up for more

`stage.py lib B1 §0`, `B1 §11`, `§13`; `A2 Step 9`, `A2 §7` (R1 to R31); `A3 §5.6`, `R16`, `R22`; `A4 §6.1`; `D15 §2.2`, `§3`; K05, K07, K08 to K10.

---

From the skill file `cards/21 Making pictures and video with AI.md`:

# Card 21. Making pictures and video with AI

Add-ons A and C read it whole; step 10 reads only "Cost". "C1 R9" is rule 9 in C1 §6; "C2 Rule 12" is rule 12 in C2 §5 and "C2 R6" its recipe 6; "C3 R1" is rule 1 in C3 §18 and "C3 L14" its linter check 14. Model facts live only in `adapters/*.json`, dated (C1 §0).

## The job

Turn approved records into pictures and clips, deciding nothing again. `stage.py compile` fills C3's master template into each clip's **generation specification** (`generation_spec`, one model-neutral description) and rewrites it per model with a dated **adapter** (one model's rules for word order and syntax) (C3 §15-§16). The AI supplies inputs, reads every **pack** (one scene's prompts for one model), fixes a record rather than a prompt, and logs every take. It hands on PIC, VOICETAKE and TAKE records, packs with 0 GEN errors, cost lines, and a keep-or-reject suggestion per take at checkpoint E ("keeping takes").

## Questions in order

1. **Is the style provisional?** Run D5's style test first: three directions each tried on a face, a wide and a hard shot (D5 §7.1-7.2, R12). Ask once: "Which of these three styles? [A]" (blueprint 10).
2. **Does every element state in frame have reference pictures?** **Reference pictures** are approved stills of one element in one state that a model copies: portrait, front-side-back views, hands and marks, one view per picture; places empty; later states edited from the base (C2 Rule 1, Rule 17, §6.2).
3. **Will it become video?** If not, stop at a grey storyboard frame of the most telling moment; arrows and bars are drawn by the page, never in the picture (C2 Rule 2, §2.2, R3).
4. **Is a speaking mouth on screen?** Voices first: the VOICE locked and its VOICETAKE picked before the clip (K16; D3 R1). Prefer the listener; then a model that takes the line's audio, then lip sync after, then a cutaway (D3 R20-R21).
5. **Which model?** Code picks one **scene model** per scene (the model serving most of its shots with recurring characters) and logs each override with its reason, followed by drift questions (K29; C1 R14). A **held take** (a turn shot, where the scene turns; a shot in a one-take `oner` scene; or `held: yes`) is never chained: it routes to a model that allows its length, or is redesigned with a motivated cut (GEN-10; blueprint 8.4).
6. **Is it a hard case?** Readable words are a **text graphic**, drawn outside any model and composited after any flip (K17; C2 Rule 9); floating bodies take a **guide video**, a grey 3D video the model copies (C1 R8; card 22); violence is split into cause, reaction and aftermath (C1 R9).
7. **Does the pack pass?** 0 GEN errors (rubric criterion 9), and for each face in frame: "Is <name>'s face as readable and as true in colour as the other faces in this frame?" (B2 R24; blueprint 8.9). Without code, run C3 §21 in words.

## Cost

Example first: the fall in The Catch's SC06 is 36 shots in 49.7 seconds, yet every take pays for a whole clip, so it bills about 1,250 generated seconds, about 25 per second on screen (D13 §15.1). A **generated second** is one second of clip a model makes, kept or not; **clip length** is what one take bills; a **tier** is the price level of final takes: budget, mid or premium (C1 §10).

1. **Code prices; the AI never writes a total** (D13 P1, R4): `stage.py estimate` works from words first, from the shots at step 10.
2. **Clip length** is the model's shortest clip or screen time plus `handles_s` at each end, whichever is longer, rounded up to an allowed length (D13 §6.2; blueprint 8.4). Short shots pay whole clips, so fast scenes cost most (D13 P4).
3. **Each shot has a `cost_class`**: `graphic` and `reuse` cost no takes; `still_move` is one picture, held or pushed slowly in the editor; the push is a `push_in` inside the scene's budget and camera rules (B1 P5); `easy`, `dialogue` and `hard` take D13 §6.1's draft and final takes. Several needs take the dearest class, and text or a screen adds a **plate**, an extra element for compositing (D13 R20); zero gravity, an exact camera path, a performance or a creature is `hard` (D13 R8).
4. **Video money** is clip length × (draft takes × draft price + final takes × tier price), plus plates (D13 E7). Show all three tiers (D13 R9).
5. **Other lines**: pictures, voices and effects, music (none under `music_policy: none`, D13 R24), upscaling of kept takes after picture lock (D13 R14), contingency (D13 §6.9). A tool whose terms exclude film is not budgeted (D13 R19).
6. **Freshness**: prices older than `model_facts_max_age_days` print no money (GEN-11; D13 R7).
7. **While spending**: nothing before `spend_cap_usd` is set; a take above `cheap_test_above_usd_per_take` needs a cheaper test first (GEN-16); stop a route after `takes_stop_per_route` failed takes and a shot after `takes_stop_per_shot`, and change method, not wording (C3 §17A; D13 R12); once `spend_check_share` of the video money is spent before that share of shots is kept, move remaining non-dialogue shots to the budget tier (D13 R11); over budget, apply D13 R10's cuts in order (`stage.py lib D13 R10`). A turn shot, a must-keep shot or a cardinal event (a scene the story cannot lose) is never cut or cheapened without asking (blueprint 8.8).

## Translation menus with pitfalls

Pick one `SHOT.route` per shot, from its derived `needs` (C1 §5; C3 §20):

| Need | Route | Pitfall |
|---|---|---|
| Exact first and last picture | `start_end_pictures`, the end picture edited from the start picture (C2 Rule 15) | Two different pictures make the model cut (C3 F27) |
| Exact camera path | `guide_video` from previs (C1 R4; card 22) | The camera described again in words (C3 §9D) |
| A glance that must land | `performance_transfer`: act it on a phone (C1 R12) | An emotion word in the prompt (C3 L07) |
| Hands, rings, a held last image | `still_with_move` (C1 Ex8) | Forcing motion into hands (C3 §13C) |
| A recurring face | `references` in C2 §6.6's order; props dropped first, faces never | Extra references leak their light (C2 §1; C3 F37) |

## Budgets and saved choices

- `clip_speech_rule` with `speech_wps_default` (K08; GEN-03); `on_screen_speakers_per_clip_max` (C1 R2; GEN-13); `acting_characters_per_clip_max` (C3 R16); `main_actions_per_seconds` (C3 R2).
- `named_sounds_per_prompt_max` (C3 L13; GEN-17); no music in any clip (K31; C3 R10).
- The **fixed description** (a character's or thing's unchanging words), **state line** (its state now) and **look block** (the place's light and colour words) are pasted word for word, within `fixed_description_words`, `look_block_words_max` and `style_words_count` (C3 R6; GEN-04).
- `plate_route_face_height`, `lip_sync_tight_face_height`: larger faces change the routes (blueprint 8.5).
- **Drift** (an element changing across pictures) above one frame in ten: train a **LoRA**, a small file teaching an open model one face, or use a still with a push-in (C2 Rule 14; D5 R17).

## The baseline is a strong answer

One scene model, one shot per clip, an approved start picture with a motion-only prompt, room sound, no music, and a still with a push-in where motion adds nothing are choices, not failures (C3 §10; K29; C3 R1, R10). Depart only for a need code can name.

## Cliché traps

Tests: any-film, mood-word, stacking and sound-off (card 05), and the **reference test**: does the take pass its yes/no questions against its reference pictures?

- **The house style**: unasked light shafts, "cinematic", "moody" (B2 §12; GEN-12). Fix: look block and style words only.
- **Creature clichés**: "robot", "alien", "glowing eyes" (C2 §9). Fix: plain shapes.
- **Emotion labels** (C3 L07). Fix: two or three visible behaviours.
- **Re-describing a start picture** (C3 R1; GEN-05). Fix: motion only, "the woman".
- **Backwards text asked of a model** (C1 R7; GEN-06), or **"falling" for floating bodies** (C3 R13, §12). Fix: a flipped text graphic; "hair and straps drift up; nothing settles".
- **"No people"** (K18; GEN-07). Fix: nouns in a **negative field** (a box of things to leave out) where the model has one, else positive words.

## Reasons that fail and reasons that pass

- Fails: "Seedance for a more cinematic take." Passes: "SC10-SH150 is a held take longer than the scene model allows, so it goes to `seedance-2.5` whole (blueprint 8.4; GEN-10)."
- Fails: "Reject take 2; it feels off." Passes: "Reject TK-SC10-SH150.1-T02: her mouth moves before 6 s, failing 'only her mouth moves, and only at 6-8 s?' (blueprint 8.9)."
- Fails: "Try better wording" after repeated failures. Passes: "`takes_stop_per_route` reached; change to a start and end picture (D13 R12)."

## Two worked examples

### The Catch: SC10-SH150, "Not mint." (line 463)

A static close-up of 15 seconds; with `handles_s` at each end its clip rounds up to 17, beyond `kling-3.0-omni`, so this held take routes to `seedance-2.5` as one take (blueprint 8.4). VT-SC10-D11-T01 carries "Not mint."; Saye's lines stay off screen, placed in the edit (D3 R20). A close-up's `face_height_by_size` is above `lip_sync_tight_face_height`, so the audio goes in as a reference (D3 R21). The prompt is motion only (C3 R1): "Her head and hands stay still; only her eyes move. The camera does not move. No background music." (blueprint 8.1).

### The Long Places: SC05, "She did not turn her head." (line 79)

A contemplative, locked-off medium holds the dark at Nilay's right shoulder for 12 seconds; its 14-second clip is beyond `veo-3.1`, so the scene model must allow it (D13 §15.4). The warmth, "the way a cat commits itself", is never shown: the prompt says "the dark space at her right shoulder stays empty", and "cat" goes only into a negative field (K18; C3 R5). "Her head and hands stay still; only the lamp flame moves." (blueprint 8.1). The shoulder settling "with weight" is acted on a phone and transferred (C1 R12). When the refrain returns at first light, a shot whose light differs is a new take from its saved setup; the rest are reused (D13 R6).

## Self-check

- Is the style locked, with reference pictures for every element state in frame?
- Is every voice locked before its mouth is seen?
- Does every held take stay one clip, and does every override carry a reason?
- Is readable text a text graphic, with no reason, name or emotion word in any prompt (GEN-15, WORDS-03)?
- Is the cap set, are model facts fresh, and has a person watched every kept take (C1 R18)?

## Words for AI models

Works: one camera move and where it ends (C3 §4); moments in the model's own time marks, then an end state (C3 §5); the model's speaker format (Veo: colon, no quotation marks; Kling: `Name (delivery): "line"`; K15); the path of a relayed voice (C3 R21); "flashlight", never "torch" (K19).

Fails: reasons in prompt text (GEN-15); lens numbers or focus shifts trusted to words (C3 §4; B1 R14); two camera moves (C3 L03); negating a visible thing (C3 L14).

## Look up for more

C1 §5-§11; C2 §2.2, §5-§9; C3 §4-§9, §15-§21; D13 §6, §9, §15; D5 §7; D3 §3.

---

From the skill file `cards/22 Previs.md`:

# Card 22. Previs

Add-on B reads it whole. It runs only in Claude Code on the user's computer, where the AI runs Blender; the user's word is "grey previews" (blueprint 9). "C4 R21" is rule 21 in C4 §8 and "C4 Rec3" its recipe 3 (§10); "D6 Rec4" is recipe 4 in D6 §6.

## The job

**Previs** is a rough grey 3D version of a shot that fixes camera placement, lens, timing and where bodies stand before any video is made (C4 §1). Code compiles one plan per shot at `previs_plan_level_min` or above from the records (`make_previs_plans.py`: set plans, scene starts, floor-plan moves, setups (where each camera stands), shots); the AI writes only what code cannot, renders with `render_previs.py`, fixes every blocking fault, and records the route into video. It hands on PREVIS records (`level`, `standin_level`, `route`, `stills`, `approved`), **grey renders** (untextured renders showing shapes and light direction), plan views (a flat top or side view of the set), and one contact sheet per scene of framing-critical shots for checkpoint D, "the grey previews" (blueprint 9).

## Questions in order

1. **Does the meaning depend on where the camera stands, its lens or how bodies move?** Then previs; a static or simple dialogue shot skips 3D (C4 R1-R2). `previs_level` follows C4's ladder: 0 no 3D (dialogue, object close-ups, simple scenes: most shots); 2 grey 3D, a layout check; 3 a **guide video** a model copies (falls, weightlessness, the creature, complex moves); 4 a performance captured on a phone when a reach or flinch must be exact; 1 (posed stills) and 5 (open models on a rented graphics card) are rarely worth it (C4 §9; K14).
2. **Does the place have a set plan?** A location in three or more shots gets one grey set that every shot there reuses, so the door is always on the same wall (C4 R3, Rec2); in the pipeline it is the LOCATION's set plan (K23). A place seen in both mirror states is stored once, in `plan_orientation`; code derives the other and nobody edits it by hand (B3 §5.4; K02).
3. **Which stand-in?** A **stand-in** is the simple figure that takes a character's place. `standin_level` 1 is boxes, enough for depth and eyelines; 2 a shaped human; 3 a rigged human with a motion; 4 the user's own capture; 5 a hand-posed rig (C4 §4.4). A pose guide needs a human shape; a body that is not human-shaped (the figure) is guided by depth, never pose (C4 R6-R7).
4. **What is not automatic?** Physical motion beyond the free-fall helper, bodies riding a moving cage, doors that swing on a pivot, arm and hand poses, performances and creature shapes go into the shot's extras fragment, `19 Grey previews/extras/<shot>.json`, named in `PREVIS.extras` (blueprint 9).
5. **Does it obey physics?** A fall is keyed (its position set) on every frame from z = z0 − `free_fall_half_g` × t², because eased keys stall and read as floating (C4 R10, §4.2). Bodies inside a moving object are parented to it (attached, so they move with it) or keyed on the same frames, or its floor passes through their legs (C4 R11, R22).
6. **Did it pass the check?** Nothing goes to a video model before `check_blocking.py` prints `BLOCKING OK` (no stand-in through a wall or another stand-in, no camera inside a solid) (C4 R21) and every figure faces within `facing_tolerance_deg` of the derived facing (PREVIS-03).
7. **Is it framing-critical?** Then the user answers at checkpoint D; otherwise it is `approved: auto` once it passes question 6 (blueprint 9).
8. **Which route into video?** One `PREVIS.route` per shot (menus below). Hosted "camera control" takes presets or a reference video, never numbers, so an exact camera path goes in as a video (C4 R24).
9. **Is geometry shared?** One physical event shown in overlapping shots is one **master previs**, and each shot's `time_slice` names its frames of it (K20); a replay on a screen is cut from one master take through the in-story camera, and a match cut shares its geometry (B1 §10.4; C5 R30).

## Translation menus with pitfalls

Pick one route per shot, tied to what the shot must keep exact (C4 §6, R8):

| Route | What the model gets | Use when | Pitfall |
|---|---|---|---|
| 1 | Grey stills restyled into start and end pictures (C4 Rec4) | Composition matters, motion is simple | Weak when the motion itself is the point |
| 2 | The **depth pass** (grey where brightness means distance) as a guide video, plus a style picture (C4 Rec5) | An exact camera path, floating bodies | A depth range wider than the subjects turns actors flat grey (C4 R15, R25); a slower model frame rate needs a retime (C4 R14) |
| 3 | The grey render as a reference video to a hosted model (C4 Rec6) | The camera move matters and nothing can be installed | People swap or merge: split the shot by person (C4 Rec6) |
| 5 | Elements rendered through the stored camera track, composited (C4 R9; D6 Rec4) | Exact text, screens, floating beads | A second flip in the edit (D6 VC8) |

Never lay a guide video over a face whose lips must sync (C4 R13). There is no route 4: camera numbers work only in research models (C4 §6, R19).

## Budgets and saved choices

- `previs_plan_level_min`: plans and blocking checks only at or above it; `facing_tolerance_deg`: the facing check (PREVIS-03).
- `previs_width_px`, with the height from `frame_shape` (K24); `previs_sensor_width_mm`, so lens numbers match B1's full-frame family (C4 §4.1); frames cover screen time plus `handles_s` at each end (blueprint 9).
- `previs_depth_margin_m` around the nearest and farthest subject (C4 R15).
- `previs_seated_height_factor`, `previs_kneeling_height_factor`, `previs_lying_box` for stand-ins not standing; seats and beds go in the clash exclusion list (blueprint 9).
- `free_fall_half_g` (C4 R10).
- Two or three rounds of plain-word changes are normal ("lower the camera to knee height") (C4 Rec3).

## The baseline is a strong answer

Level 0 is right for most shots: C4 puts dialogue, object close-ups and simple scenes there, "most of The Catch" (C4 §9). A start picture from an approved still serves better than a grey render wherever camera and blocking carry no meaning (C4 R2). Depart only when a question above names the reason.

## Cliché traps

Tests: the **plan-view test** (is the camera where its SETUP says?) and the **moment test** (does each still show what its `moment` says?).

- **"It rendered, so it works"** (C4 R21). Fix: `BLOCKING OK`, then the plan view, then the stills.
- **Eased keys on a fall** (C4 R10). Fix: every-frame keys from the formula.
- **Riders keyed apart from the cage** (C4 R22). Fix: parent them, or key them on the cage's frames.
- **A pose guide on boxes or the figure** (C4 R6-R7). Fix: depth.
- **Fixing the prompt when the structure is wrong** (C4 R20). Fix: the plan or the guide's strength.
- **The camera described again in words once a guide video exists** (C3 §9D; blueprint 8.1). Fix: the text carries only the look block (the place's light and colour words), fixed descriptions and sound.
- **A pale, flat depth pass** (C4 R25). Fix: the data view transform ("Raw") and a tight range.
- **Planning around a research camera model** (C4 R19). Fix: wait for a hosted service.

## Reasons that fail and reasons that pass

- Fails: "Level 3 for a more dynamic shot." Passes: "SC06's fall: bodies float inside a falling cage and models add gravity back, so level 3 with a depth guide video (C1 R8; C4 R11)."
- Fails: "Approved: it rendered." Passes: "`BLOCKING OK`; every facing within `facing_tolerance_deg`; the plan view puts camera A where SC10-SU01 says (C4 R21; PREVIS-03)."
- Fails: "Previs every shot, to be safe." Passes: "SC10-SH150 stays at level 0: a static close-up whose meaning is in the face, not the camera (C4 R2)."

## Two worked examples

### The Catch: SC10-SH080, the reflection shot

Level 2 and framing-critical: the scene's image is two women "like a woman and her reflection, each with the wrong hand in the air." (line 428). Code builds the kitchen from its set plan, the west wall wild so camera A (SC10-SU01) can stand outside it, 6.3 metres back on the table's line, 1.45 metres high, with `lens_mm: 85` (K22; B3 Ex1). Iona, Saye and Eli stand on their marks with the facings the records give, Jude a lying box on the table (`previs_lying_box`); the 9-second shot at 24 frames a second renders 252 frames, screen time plus handles (blueprint 9). The render must print `BLOCKING OK` and show both profiles level, the raised hands nearest the camera, the rings out of sight on the far hands (K07; C2 W3). The user sees it on the scene's contact sheet: "Reply with the numbers of any that look wrong, or 'fine'." [fine]. Route 1: its grey stills become the layout pictures for the start and end pictures (the shot's `route: start_end_pictures`), and the mirror route is the plate route: the kitchen and Saye are made in world orientation and flipped, then Iona, Jude and Eli are added unflipped (blueprint 8.5; K03).

### The Long Places: SC05, the threshold at night (lines 73-81)

A contemplative scene needs almost no 3D. The lamp flame leaning out and in with the breath is timing, solved by moments in the prompt; the one exact action, her shoulder taking the warmth "with weight" (line 79), is level 4: the user films the settle on a phone, camera locked off, whole body in frame, plain background, and it is transferred (C4 Rec7; D13 §15.4). At Standard depth no set plan is needed: one person, no glass, and no shot at `previs_plan_level_min` (blueprint 3, step 4).

## Self-check

- Does every shot at `previs_plan_level_min` or above have a plan, `BLOCKING OK` and facings within `facing_tolerance_deg`?
- Is every extra written as a fragment, never by editing a compiled plan or a derived mirror copy?
- Is every fall keyed per frame, and every rider moving with its carrier?
- Does every framing-critical shot have the user's answer, and every PREVIS record a route?
- Is any shot in previs that a start picture would serve as well?

## Words for AI models

Works (route 3): "Follow [Video1] exactly for the camera's path, positions and timing; it is a grey 3D layout, not the appearance", with each stand-in colour mapped to a named reference picture (C4 Rec6). With a guide video, the prompt carries appearance, not camera (C3 §9D). Route 1: prompt the appearance, not the layout, and reject any start picture where someone moved, changed size or lost the eyeline, because the previs is the contract (C4 Rec4).

Fails: numbers for a camera path (C4 R24); "falling" for floating bodies (C3 R13); a guide video over a face whose lips must sync (C4 R13).

## Look up for more

C4 §4, §5.2 (plan fields), §6 (routes), §8 (R1-R26), §9 (ladder), §10 (recipes), §11 (failures), §12 (the SC06 fall, the push, the chest); blueprint 9; K02, K14, K20, K21, K23. Print one rule: `stage.py lib C4 R21`.

---

From the skill file `cards/23 Finishing, captions and delivery.md`:

# Card 23. Finishing, captions and delivery

Add-on D and step 11 read it whole. "D8 R41" is rule D8-R41 in D8 §4 and "D8 Rec10" its recipe 10 (§5); "D6 R15" is rule 15 in D6 §4 and "D6 VC8" check 8 of its layer plan (§8); "D18 R11" is D18-R11 (§4); "D9 R4" is rule 4 in D9 §3.

## The job

Turn kept takes, voice takes, effects and records into one film that can be watched, captioned, described, translated and delivered. Code creates a FINISH record for each operation a shot needs and, at step 11, writes the timeline files (`timeline.otio`, `timeline.edl`), the caption files, the audio-description script and the text-to-translate list (blueprint 8.7, 5.9). The AI fills each FINISH record's `tool`, `inputs` and `output`, runs simple jobs (flip, crop, a still overlay, a speed change, joining) as ffmpeg commands on code surfaces, writes click-by-click steps for DaVinci Resolve's free version where hands are needed, spots MUSIC cues when the policy allows them, and hands on the assembly guide.

## Questions in order

1. **In what order?** "Time before size, size before colour, colour before grain" (D8 §2); inside a composite, tools that redraw pixels run before any exact layer (D6 P2, R6).
2. **One frame rate?** The whole film runs at `PROJECT.fps`; measure every take (D8 R9). A slower take made against a guide video of the same frame count plays at the film's rate; a free one is interpolated after picture lock (D8 R11-R12); slow generation returns to real time as a `speed` job (K30); in-story footage is never interpolated (D8 R15).
3. **Does it fit the frame shape?** Crop to `frame_shape`; where a head, hand or prop leaves the band, move the clip and log it (D8 R17-R19). Cropping away a visible watermark counts as removing it (D8 R26).
4. **How many flips?** A layer shows mirrored after an odd number of flips, normal after an even number (D6 §5, VC1). World lettering goes on normal before the whole-frame flip or mirrored after it, never both (D6 R15); a shot flipped inside its composite is not flipped again (D6 VC8).
5. **Upscale?** Only kept takes, after **picture lock** (when shot lengths stop changing): whole takes to 1080p so the edit relinks, used seconds plus handles to 4K only if delivery needs it; a precision upscaler before a diffusion one, which redraws detail and can change faces; in-story footage never (D8 R20-R23; D13 R14).
6. **Grade.** First a **normalize** step per model, removing its own colour and contrast; then each sequence graded to its style picture; motif colours stay fixed, and a light change the story writes is never graded away (D8 R28-R33). Darker skin stays rich, never grey or ashy (B2 R24). One grain for the whole film, once, after the grade (D8 R34; D6 R20).
7. **Sound.** Three **stems** (separate dialogue, music and effects mixes), so a dub swaps only dialogue (D8 R37); loudness set per deliverable over the whole film (`SOUNDPLAN.loudness_target`), a quiet film mixed to its dialogue (D8 R38-R39); each relayed voice through its path's one saved chain (D3 R24); a sound motif laid from one master file (D9 R12), never stopped dead at the end (D8 R41).
8. **Music?** Only as `SOUNDPLAN.music_policy` allows; under `none`, a drone needs a source in the story (D9 R1, R4); a cue enters on a motion or cut and leaves before a rupture (D9 §4.2). Every sound file carries a RIGHTS record, and a licence forbidding commercial use or changes keeps it out (D9 R19; D4 R15).
9. **Titles.** A card cuts in and out with no fade the script did not write, holds at least `text_floor`, uses one font under the SIL Open Font License, and stays inside the graphics-safe area (D8 R42-R45).
10. **Captions** (code times them, 5.9): the words come from the speech records, never from recognition (D8 R47); an off-screen speaker's cue starts with the name, italics only for a speaker not in the scene (D8 R52); an effect at sound emphasis 2 or more gets a sound tag, a motif always the same tag (D8 R51; D18 R7); backwards text gets no subtitle (D8 R53; D18 R22).
11. **Audio description**, a narrator's voice in the gaps telling a blind viewer what to see, covers every shot with `needs_description: yes`: what the frame shows, from `does`, never a feeling or anything kept hidden (D18 R3, R10); what a later payoff needs comes first (D18 R9); about `speech_wps_default` words per second of gap, ending before the next line (D18 R11); designed silences stay empty (D18 R4).
12. **Translation.** TEXT with `translate: yes` goes on the text-to-translate list; translators work from an annotated template, not the captions (D18 R18); a name that is a word in the target language gets a note (D18 R19); a glyph chosen for its shape is never translated (D18 R32).
13. **Delivery.** Keep a textless master, stems, caption files and raw downloads with their provenance marks, never stripped (D8 R60; D4 P8); the disclosure line is card 24's.

## Translation menus with pitfalls

One method per job, by the FINISH `operation` (blueprint 8.7):

| Operation | When | Pitfall |
|---|---|---|
| `flip` | The mirror routes "flip all" and "flip with mirrored references" | A second flip in the edit (D6 VC8) |
| `composite` | Text graphics, screens, plates with people, beads | An element sharper or cleaner than the plate (D6 R21, Rec9) |
| `speed` | Retimes; slow generation back to real time | A free slow-rate take simply played faster (D8 R12) |
| `upscale` | Below master size after the crop | A diffusion upscaler redrawing faces (D8 R22) |
| `deflicker` | Brightness pumping | Expecting it to steady crawling detail (D8 R25) |
| `grade` | Every sequence | A lookup table on raw takes (D8 R35) |
| `lip_sync` | A mouth that must be seen | A third try instead of cutting to the listener (D3 R23) |

## Budgets and saved choices

- `caption_lead_s`, `caption_min_s`, `caption_max_s` time every cue; longer speeches split at a sentence end (blueprint 5.9).
- `text_floor` holds every card and text in picture, doubled when mirrored (K09).
- `device_budget_short` caps editor-made cuts to black, true silences and freezes; a black the script writes is outside it (A4 P10; D8 §9.3).
- `handles_s`: the spare picture each side of every used part (D8 §1).
- `sound_motif_max` caps sound motifs (B4).

## The baseline is a strong answer

A hard cut, room sound under every line, one grain, one font, caption files beside the picture rather than burned in, and no music under `music_policy: none` are choices, not failures (D8 R42, R34, R44, R55; D9 R1). Depart only for what the story writes.

## Cliché traps

Tests: any-film, stacking and sound-off (card 05), plus **eyes closed** with the description track and **sound off** with the captions (D18 Rec7).

- **Fades and dissolves the script never wrote** (D8 R42; A4 T5). Fix: a cut.
- **A musical hit on a reveal the script already marks** (D9 §7; B4 R23). Fix: remove it.
- **A drone with no source** under `none` (D9 R4). Fix: a story source, or silence.
- **The generator's own colour left in**, or one "film" preset over everything (D8 R28, R35). Fix: normalize, then grade each sequence.
- **Grain asked for in prompts, or added twice** (D5 R18; D6 R20). Fix: one grain, after the grade.
- **Generic tags** such as "[music]" or "[speaking foreign language]" (D8 R54). Fix: name the sound and its pattern.
- **Description that interprets**: "she is horrified" (D18 R10). Fix: what the frame shows, from `does`.
- **A quiet film pushed loud for the web** (D8 R39). Fix: mix to the dialogue.

## Reasons that fail and reasons that pass

- Fails: "Dissolve into the morning to show time passing." Passes: "Hard cut into SC11: the story writes no transition there (D8 R42; A4 T5)."
- Fails: "[pump thumping]". Passes: "[three uneven pump strokes], the motif's one tag, because its payoff depends on the pattern (D18 R7; D8 R51)."

## Two worked examples

### The Catch: the end of SC10 (lines 484-488)

"Nobody leave this room." (line 484) is followed by "> CUT TO BLACK." (line 486) and "= THE CATCH" (line 488). The CUT record SC10-C200 is `cut_to_black`; SC10-SH990 is the title card TX-TITLE-CATCH, white on black inside the graphics-safe area, cut in and out, held beyond its `text_floor` in true silence: the kitchen's room sound stops with the picture and `music_policy` is `none` (D8 R42-R45, §9.3). The script writes this black, so it spends nothing from `device_budget_short`. In SC10-SH150's captions "Not mint." is its own cue of at least `caption_min_s`; Saye's lines begin "SAYE:" because she is off screen, but are not in italics, because she is in the room (blueprint 5.9; D8 R52). The description, in the gap before Saye's question, gives the face as behaviour: "She chews, then stops. Her eyes drift down. One more slow chew." (D18 §7.2).

### The Long Places: the knock (lines 419-421)

Melek "knocked twice, softly, and then stood in the waiting, two breaths entire" (line 419). The description speaks before the knock ("Melek lays her palm on the stone beside the niche. Knocks twice, softly.") and then nothing: the two breaths are a designed silence (D18 R4, §8). The captions name the sound, not a source the book never names: "[two soft knocks]", then "[a low, shaped sound under the knock, no words]", not D18 §8's "voice", which the sound design refuses (D18 R8). The answer, "Low. Shaped. With the fall of a sentence in it." (line 421), is built from breath and room resonance, never a generated voice, which would settle what the book leaves open (D9 §8.4). "the waiting was the rite, if it was a rite" (line 419) is the narrator's thought, never description (D18 §8).

## Self-check

- Does every derived operation have a FINISH record with tool, inputs and output, and no shot a second flip?
- Is every take at the film's frame rate, cropped to the frame shape, and upscaled only after picture lock?
- Is there one grain and one font, and a RIGHTS record for every sound file and font?
- Do captions use the script's words, and does description skip designed silences and hidden things?
- Is every watermark and provenance mark kept?

## Words for AI models

Works: ffmpeg commands the AI writes and runs for simple jobs (blueprint 8.7); for a music cue, "Instrumental only, no vocals.", a tempo, two to four instruments, a timed shape and "one sustained note that decays naturally" at the end (D9 §4.3); for an effect, its source, its action and the space around it (C3 §7E).

Fails: artist names, song titles or lyrics in a music prompt (D9 §4.3); a generated voice where the story keeps a sound unknown (D9 §8.4); speech recognition as the source of caption words (D8 R47).

## Look up for more

D8 §4, §5, §9; D6 §4, §5 (layer order), §6, §8; D18 §4, §5, §7, §8; D9 §3, §4, §8; A4 T5; blueprint 5.9, 8.7. Print one rule: `stage.py lib D8 R41`.

---

From the skill file `cards/24 Rights, consent and disclosure.md`:

# Card 24. Rights, consent and disclosure

Step 0 reads only "The rights question"; step 4 reads only "Names and likeness"; add-on C reads it whole. "D4 R7" is rule 7 in D4 §4, "D4 P3" principle 3 (§2), "D4 Rec3" recipe 3 (§5). This is a production checklist, not legal advice: for a film that will be sold, made for a client, or that uses a real person or a licensed book, suggest a lawyer before release (D4 R27).

## The job

Settle, before any work, whether the user may adapt the story; keep real faces, voices, names, brands and protected designs out of pictures and prompts; plan sensitive shots around filters without tricks; record every licence; keep the provenance marks; write one honest disclosure line (D4 §2). Step 0 hands on PROJECT `rights` (CHOICE-001) and the source's RIGHTS record; step 4, `likeness_basis`, small choices for invented names and the name checks (notes on RT-001); add-on C, RIGHTS records for voices, likeness, music, fonts, stock and tool terms, and the disclosure text in `22 Rights and credits.md`.

## Questions in order

1. **Who owns the story? Is any face or voice real? Is every invented name clear?** See the two parts below (D4 R1, R7, R17).
2. **Does the shot touch a sensitive subject?** Set `content_flags` and a `policy_route` at shot design (D4 R10): a **content flag** marks a sensitive subject (violence, blood, a minor, a real person or brand); a **policy route** says how it is made instead. A minor is never in a flagged subject (D4 R8).
3. **Was a request refused twice?** Stop, reroute to compositing, sound or restaging, and log it; wording meant to slip past a filter can end the account (D4 R11; C1 R10).
4. **Does the tool plan allow the use?** A film that will be sold, shown at festivals or earn money needs every kept take, voice and sound made on a commercial plan (D4 R13), recorded as a RIGHTS record (`subject: model_terms`, `commercial_ok`). A take resembling a protected character, logo or artwork is rejected at checkpoint E (D4 R6).
5. **Does every asset carry its licence?** One RIGHTS record per library sound, stock file or font, made when it enters (D4 P6, R15-R16).
6. **What is disclosed?** Keep Content Credentials and watermarks (**provenance marks**, proof of where a file came from) (D4 P8; D8 R26); write one wording for credits, platform AI labels and festival answers (D4 R20-R22, Rec6).
7. **Are the facts fresh?** Re-check any law, policy or terms fact older than `model_facts_max_age_days` before release or a large spend (D4 R29).

## The rights question

Example first: The Catch's title page says "= An original short screenplay" (line 3). "Original" means not adapted from another work; it does not say who wrote it (D4 §9.1). So the welcome asks once: "Is this story yours, or do you have permission to adapt it? [It's mine]". Adapting a story is its owner's right (D4 §3.1).

PROJECT `rights` takes one value; D4's finer statuses map onto it (D4 §6.1):

- `mine`: the user wrote it.
- `permission`: a licence, an **option** (a paid, time-limited right to buy the film rights later) or written permission. It must be written and allow a film made with AI tools, say where, for how long and whether it may earn money (D4 §3.1, R28). The finer kind goes in the RIGHTS record's `clearance`.
- `public_domain`: out of copyright. Check every country of showing and the exact edition or translation (D4 R3, Rec2).
- `study_only`: "not mine, no permission", and the nearest value for a fan work, since not earning money is no defence (D4 R2). Work goes on privately; every export is marked "Private study, not for publication"; packs refuse public release (GEN-14); the text never goes to tools that train on it (D4 R1).
- `unknown`: until answered.

The source's RIGHTS record (`subject: source`) names the holder by role ("the author"), never by name or contact (blueprint principle 10). A source written or revised with an AI model is said so in credits and festival answers, and awards requiring a human-written screenplay are skipped (D4 R4, R30).

## Names and likeness

Example first: "Saye opens a file. The same woman, much younger. A flight suit. Unsmiling." (line 988), then "NELL ROWAN. FLIGHT TEST." (line 990). A real pilot's photo would be a real person's **likeness** (a recognisable face, body or voice). Instead Nell is designed at "Sixty, perhaps. She looks older." (line 1135), the photograph is made by editing that face about nineteen years younger ("The date is nineteen years old.", line 998), the flight-suit patch is invented, and the name is a text graphic (D4 §9.3).

1. **Every face and voice is invented** unless a living adult has signed **consent** (written permission for that exact use); a dead person's face and voice are protected too, and a celebrity's are never used (D4 P3, R7; D3 R16). `likeness_basis` defaults to `invented` as a small choice; `self_consented` or `performer_consented` needs a RIGHTS record whose ID goes in `consent` at add-on C, the signed form kept outside every AI tool (D4 Rec4). A child's face is always designed (D4 R8).
2. **Describe, never name.** A fixed description names no real person and never says "looks like" (D4 P2, R5; WORDS-03); each approved face gets a lookalike check by eye (D4 Rec4).
3. **Voices.** `VOICE.source` defaults to `designed`; a clone only of the user's own voice or of a consenting, verified adult (D3 R16-R17).
4. **Name check** every invented character, company, product, institution and place: search it in quotes, then the national trademark databases, and give D4's verdict: clear, a low-risk coincidence (same name, unrelated field) or a conflict (D4 R17, Rec3). A conflict becomes a small choice proposing a rename, shown at checkpoint B. OSTREL ("OSTREL, stitched on it in blue.", line 496) is near a household-goods mark, and "IONA VALE." (line 1233) is an author name on colouring books: both low-risk coincidences (D4 §9.4).
5. **Real institutions**: keep the place, invent the name, crest and livery (D4 R19); "Police lights beyond frosted windows." (line 492) show no livery, so nothing is flagged.
6. **Brands and signs** are invented; any that must be read is a text graphic (D4 R18; K17).

## Translation menus with pitfalls

One `policy_route` per flagged shot, tied to its flag (D4 §3.6, Rec5):

| Flag | Route | Pitfall |
|---|---|---|
| `gunfire` | `sound_only`, plus a composited flicker | A weapon aimed at a person in frame |
| `violence_implied` | `split_cause_reaction_aftermath`, with words for the visible result (C1 R9) | Injury words in the prompt |
| `blood_small` | `composite_element`: the plate made without blood | "Blood splatter" asked of a model (C1 §4) |
| `real_brand`, `real_person` | `restated` as an invented design, or `cut` | A model-drawn real logo (D4 §3.3) |
| `drug_use`, `self_harm` | `restated`: aftermath, never method | A word a filter misreads: SC11's "needle" is a gauge (D4 §9.2) |

## Budgets and saved choices

- `model_facts_max_age_days`: the age at which law, terms and prices are re-checked (D4 R29; GEN-11).
- `fixed_description_words`: invented faces described in visible nouns only (WORDS-05).
- `licensed_data_only: yes` limits routing to models trained on licensed footage (blueprint 8.4; C1 R19).
- One disclosure wording for every place (D4 P8).

## The baseline is a strong answer

An invented face, a designed voice, an invented brand drawn as a text graphic, and the plain credit line are choices, not failures (D4 P3, R18, Rec6). Depart only with a signed consent or a written licence.

## Cliché traps

Test: would the credit line and every festival answer still be true if the project log were read aloud (D4 Rec6-Rec7)?

- **"The filter let it through"**: a filter is a floor, not permission. Fix: the rights checks still apply (D4 §3.3, P5).
- **"Looks like" an actor** in a fixed description. Fix: visible features only (D4 Rec4; WORDS-03).
- **Cropping a watermark** away. Fix: keep it in frame (D8 R26).
- **Overstating human work**: "designed" only for what a human designed (D4 Rec6).
- **"No AI" to a narrow festival question** without checking how the source was written. Fix: read the project log first (D4 Rec6).

## Reasons that fail and reasons that pass

- Fails: "Nell's photo from a real pilot archive, for realism." Passes: "Nell's photo edited from her designed face nineteen years younger (line 998); `likeness_basis: invented` (D4 R7, §9.3)."
- Fails: "Keep 'blood splatter'; the scene needs it." Passes: "SC06's beads: `blood_small`, `composite_element`; the plate is made without blood (D4 §9.2; C1 Ex2)."
- Fails: "Directed and designed by [names]" when the AI drafted the shots. Passes: "Directed and edited by [names], who chose and approved every shot planned with an AI assistant." (D4 Rec6)

## Two worked examples

### The Catch: SC06, the shot through the roof (lines 216-222)

"Someone KICKS the top gate open and FIRES down through the roof." (line 216) gets `gunfire` and `violence_implied`, route `split_cause_reaction_aftermath`: a bright flicker through the roof grid and the three looking up; the shots and the crash in the sound mix; the spark at her boot composited (D4 §9.2). "He sits down into Eli with a hole through his shoulder." (line 222) becomes "He sits down heavily against Eli, a dark stain spreading on his shoulder"; the hole is never shown.

### The Long Places: an AI-written source (lines 1-3)

The file names itself "revised by Claude, final" (line 1), and line 3 says the novella came from "GLM 5.3's novella (file 10), revised by three Claude agents". The credit uses D4's template for an AI-written source: "Based on The Long Places, a novella generated with GLM 5.3 and revised with Claude under the direction of [names]." A screenplay the pipeline drafts from it is AI-written too, so festival answers say so (D4 R30). Its real places stay ("Erciyes stood up out of the haze", line 37), while any Ministry letterhead is invented (D4 R19, §9.6).

## Self-check

- Is `rights` answered or defaulted, and every export marked when it is `study_only`?
- Does every character have `likeness_basis`, and every non-invented one a consent record?
- Is every invented name checked, with conflicts shown as small choices?
- Does every flagged shot have a policy route, and did nothing go a third time after two refusals?
- Does every kept take, sound and font have a RIGHTS record allowing its use?

## Words for AI models

Works: visible attributes instead of names ("short neat grey hair, a pale lined face"); plain physical wording for injuries ("a dark red stain spreads through his shirt"); honest genre context first ("A tense dramatic thriller scene.") (C3 §14); invented brands as plain surfaces, the graphic composited later (D4 R18).

Fails: a real person, artist, film or brand in a prompt field (WORDS-03); misspellings or code words to pass a filter (C3 §14; D4 R11); a real person's photo as a reference (D4 R25).

## Look up for more

D4 §2, §3, §4, §5, §6.1 (pipeline names), §9; D3 §3 (R16-R19), §6; D8 R26; D9 R19-R20; C1 §4, R9-R10. Print one rule: `stage.py lib D4 R11`.
