# Step 6. Film rules

This is step 6 of the pipeline; the user counts it as step 7 of 12, "the film's rules". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Write each department's rules for the whole film before any scene is designed (camera, character camera rules, saved choices, light for each place, colour for each group of scenes, sound, and the ladder of main turns), keyed to the one climax and each citing its reason.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Write each department's system for the whole film before any scene, keyed to the one sequence list and the one climax (principle 5: systems before shots). Scenes then spend what these rules allow instead of each one reaching for its strongest choice.

## When it runs

Once, straight after the big choices are answered, in three units. There is no stop for the user: they approved what drives it at the big choices. Film rules are locked when written.

## Inputs

PLAN (climax, crisis, peaks) and the SEQUENCE list; STYLE, WORLD and RULE; CHARACTER, VOICE, LOCATION (with set plans), PROP, MOTIF, STATE; the answered choices.

## Outputs

`10 Film rules.md`:
- CAMSYS: `frame_shape_why`, `lens_type`, `lens_family`, `normal_lens_mm`, `step_change`, `default_height`, `default_move`, `banned`, `camera_speed`, `break`, `time_rule`.
- CAMRULE per principal (`CR-ELI`): `in_control`, `losing_control`, `never`, `closest` (a size at a story point), `limit_before`, `eyeline`, `because`.
- RESERVE (`RC-01` on), always including two film-level saved choices: the non-insert extreme close-up (at most `extreme_close_up_film_max` for the format) and the push-in (in at most `push_in_scene_share_max` of scenes).
- LENS (`LX-01`): a lens exception and the setups or scenes it is allowed in.
- LOOK per place and time (`LK-SAYE-KITCHEN-NIGHT`): the `look_block` pasted into prompts, `main_light` placed on a set-plan object or a compass wall, `contrast`, `fill`, `stays_dark`, `palette`, `accent_allowed`, `light_cue` items at story points.
- VISUAL per sequence (`VS-SQ03`): the colour-script row and the visual-structure plan.
- SOUNDPLAN: `voice_policy`, `device_budget`, `rupture_plan`. When it is first applied, code adds `music_policy` (the music answer, kept since step 3) and `clip_audio` (from the music and voice policies).
- LADDER: each scene's main turn as a story point, with its planned size and hold.

Also PROJECT `fps`, and a small choice in `01 Choices.md` for `voice_policy` (default `designed_only`).

## Card parts to open

Each unit opens only its own parts:
- U-06-CAMERA: card 09, whole; card 10, part "Camera system".
- U-06-LOOKS: card 11, part "Lighting plan".
- U-06-PLANS: card 11, part "Colour script"; card 12, part "Visual structure"; card 13, part "Sound plan"; card 09, whole.

## Procedure

Work in this order (card 09, questions in order). Every line cites a plan, character, motif or rule ID in its `because` or `why`. Beats and shots do not exist yet: a moment inside a scene is a story point, which code resolves to a beat at step 7.

1. **Climax and peaks first.** Read PLAN `climax` and each `peak`. Decide which component the climax spends and which the opening may spend (B2 §4.4); the film's tightest size and longest hold are never spent before the climax unless PLAN's peaks place them there with a reason, as for a climax in counterpoint (D16 R16; FILM-01).
2. **Camera system** (U-06-CAMERA): the baseline (static, at the whose-scene character's eye height, the normal lens), the lens family, what is banned with its why, real-time playback, the time rule for expanded action (overlapping real-time slices, never slow motion; K20), and the one `break` (B1 §9). The Catch breaks once, in scene 26: `break: SC26 "She pushes gently away from the rail."`.
3. **Character camera rules**, one per principal: what the camera does when they hold control and when they lose it, what it never does to them, and their closest size saved for one story point, with nothing closer before it (B1 §9.2). `CR-ELI`: `never: push_in`, `closest: close_up | at: SC13 "Now he looks at her."`, `limit_before: medium_close_up`.
4. **Saved choices and lens exceptions.** Each RESERVE: `choice`, `match` (how code knows a use: `size = extreme_close_up`), `max_uses` (a number, `1_per_scene` or `share`), `allowed_in`, `never_on`, `because`; always the two film-level ones above (B1 P5; FILM-08). Each LENS names exactly where it is allowed (CRAFT-07); footage from an in-story camera (SHOT `kind: screen`) keeps its CAMERA's lens and needs no LENS.
5. **Looks** (U-06-LOOKS), one per place and time in use: the main light placed in the room (`from:` a set-plan object or a wall), so code works out its frame side per shot and per era; hold light as the look unless a story source changes it; a `light_cue` only where the story causes one (card 11). The look block stays within `look_block_sentences` and `look_block_words_max`.
6. **Colour script** (U-06-PLANS): one VISUAL row per sequence, peaks first, valleys lower, then the monotony test (no `colour_monotony_run` sequences alike without a reason; B2 §8.3).
7. **Visual structure**: for each sequence, `space`, each `component` (hold, progress or contrast, with why) and any `counterpoint` (B3 §2.6).
8. **Sound plan**: `device_budget` within `device_budget_short` for a short; the `rupture_plan` from the peaks; `voice_policy` as a small choice. Never type `music_policy` (the user's, set only through the music choice) or `clip_audio` (code's): `apply` refuses both (FORM-10).
9. **The ladder**: one `rung` per scene with a main turn, as a story point with size, hold and why. It escalates by size and hold together; other scenes' main turns land at close-up or on a deliberate wide (A2 R4, R31). The Catch: `rung: SC10 "Her face changes." | size: close_up | hold: long | why: ...`, leaving the tightest size for scene 13.
10. **Check.** Run `stage.py check --unit <unit>`, and after the last unit `stage.py check --step 6`; fix only the lines printed, at most `repair_rounds_max` rounds.

## Record template

`templates/10 Film rules.md` (CAMSYS, CAMRULE, RESERVE, LENS, LOOK, VISUAL, SOUNDPLAN, LADDER), `templates/01 Choices.md`, and the PROJECT part of `templates/00 Start here.md` for `fps`.

## IDs you will be given

`RC-01` and `LX-01` on come from the handout's block, in order. You name the rest from the record they serve: `CR-` and the character (`CR-ELI`), `LK-` and the place and time (`LK-SAYE-KITCHEN-NIGHT`), `VS-` and the sequence (`VS-SQ03`). CAMSYS, SOUNDPLAN and LADDER are single records with no ID.

## Batch and chunk rules

Three units, in this order: (a) U-06-CAMERA: CAMSYS, CAMRULE, RESERVE, LENS; (b) U-06-LOOKS: every LOOK; (c) U-06-PLANS: VISUAL, SOUNDPLAN, LADDER. Each reads the plan and the records it needs, never the story whole.

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Does every principal have a CAMRULE?
2. Is every saved and banned choice listed, including the two film-level saved choices?
3. Does every lens exception name where it applies?
4. Does every place in use have at least one LOOK, and every sequence a VISUAL?
5. Does the ladder name every scene with a main turn?
6. Does every system line cite a plan, character, motif or rule ID?
7. Is the tightest size or longest hold kept for the climax (or its declared counterpoint)?
8. Is every story point's quote found once in its scene, and does `check --step 6` exit 0?

## The report

```
Done: step 7 of 12, the film's rules.
Example: the camera stays still at the eye height of the person each scene belongs
  to, and breaks that rule once, in scene 26, when Iona pushes away from the rail.
Made: 10 Film rules: the camera, how it treats each main character, the strong
  choices saved for a few moments, the light of each place, the colour of each group
  of scenes, the sound, and how each scene's biggest moment builds to the climax.
Needs you: nothing now. You'll see these rules in five lines with the first group
  of shots, while a change still costs little.
Next: I'll design scene 1 and list its shots.
```

## Checkpoint

None here. The user approved the choices that drive these rules at the big choices. The first group-of-shots message at step 7 states the rules in five plain lines, where a change still costs little; the book shows them in plain words; a later change asks first.

## How to redo

- "Redo the colour script": the VISUAL records run again; the scenes and shots that cite them go stale.
- Any other rule changed after the first group of shots: say what it affects in plain words (`stage.py impact` on the record), ask once, then redo only that.

## If you cannot run code

Every line reference is a quote anchor: every story point (`break`, `closest`, `light_cue`, `rupture_plan`, the ladder's rungs) is a scene ID and an exact quote of at least `quote_anchor_words_min` words, found once in that scene. Never add the ` = SC10-B07` ending; code writes it after step 7.

1. Save the three units' records as `10 Film rules.md`, then `10 Film rules - looks.md` and `10 Film rules - colour, sound and ladder.md`; `adopt` merges them by ID (G10). Save the voice choice, a small choice written `status: defaulted`, as `01 Choices - film rules.md`, and write its default (`voice_policy: designed_only`) in SOUNDPLAN, with `music_policy` as answered at the big choices and `clip_audio: No music in any clip.`
2. Write each record's `status: approved` and `locked: yes`: film rules are locked on writing. Save `00 Start here.md` again, whole, with PROJECT `fps` and the log line.
3. Each box: plain part, divider, records, a `---` line, the checks-in-words table (`reference/06 Checks in words.md` part 1), the END line. Print "Checked in words: 14 of 14 passed" (or only the failures).
4. Report, then the resume line for the first scene chat:

```
Save as: 10 Film rules.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 02 Whole-film summary,
10 Film rules and its files, 10 Steps 07-08 - scenes and shots and your story, and
08 Places and things (with its files) when the scene's place has a floor plan;
type: Continue my breakdown. Next is scene 1.
```

**One-line task, again:** Write each department's rules for the whole film before any scene is designed (camera, character camera rules, saved choices, light for each place, colour for each group of scenes, sound, and the ladder of main turns), keyed to the one climax and each citing its reason.
