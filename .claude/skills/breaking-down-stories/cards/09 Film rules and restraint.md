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

Example: in The Catch the rhyme check compares scene 10's reflection two-shot (two people in profile at the frame's edges, shot along the glass) with scene 29's: the same lens, level, along the glass; sides reversed on purpose, since Iona is turned back: FILM-02's warning, answered in the `why` (B3 §8.2; K07). The **film pass** (step 9) judges the whole film as one structure before any picture is made. It reads the **film strip**, one line per shot (ID, beats, role, size, lens, camera move, saved choice used, emphasis, screen time, scene intensity). A **turn picture** is the one-sentence frame each turn must show; a **light cue** is a change of light the story causes.

**Code first.** `stage.py check --film` runs:
- FILM-01, the ladder: nothing before the climax spends the tightest size or longest hold unless a peak places it there.
- FILM-02, rhyme: a payoff shot marked `rhyme` repeats its plant shot's lens, angle, size and frame side (B3 P8).
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
