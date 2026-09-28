# Step 4. Characters, places and things

This is step 4 of the pipeline; the user counts it as step 5 of 12, "characters, places and things". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Design everything the film shows more than once (the characters and their voices, the places with their set plans, the things, the text in picture, the motifs and the cameras inside the story), each resting on quoted lines.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Design everything the film shows more than once: characters and voices; places with set plans; things; text in picture; motifs; in-story cameras. Every later prompt pastes these fixed descriptions word for word, so they are written once, from evidence, and then locked.

## When it runs

Once, after world and style, in several units: motifs first, then one unit per principal character, the minor characters, the places, and the things. Each unit feeds the next.

## Inputs

- For each element, a list code builds of every source line that mentions its aliases, capped at `alias_mentions_cap` plus every mention with a physical noun; ask `stage.py lines CH-SAYE --more` for the rest.
- PLAN, SEQUENCE and the SCENE records; STYLE, WORLD and RULE.
- The CHARACTER stubs from step 1.

## Outputs

- `07 Characters and voices.md`: CHARACTER and VOICE.
- `08 Places and things.md`: LOCATION (with set-plan `object` and `mark` items where one is needed), PROP, TEXT, MOTIF, CAMERA.
- `01 Choices.md`: small choices for sides the story leaves open, casting placeholders, invented names, every character's `likeness_basis` (default `invented`) and every voice's `source` (default `designed`; asked again with the generation packs).

## Card parts to open

Each unit opens only the parts listed for it (steps.json):

- Motifs (U-04-MOTIFS): card 07, whole.
- A principal (U-04-CH-IONA) or a group of minor characters (U-04-MINOR-P1): card 05, whole; card 06, part "Voices"; card 24, part "Names and likeness".
- Places (U-04-PLACES-P1): card 12, part "Set plans"; card 07, whole.
- Things (U-04-THINGS): card 07, whole; card 17, whole.

## Procedure

Work in this order; each part feeds the next.

1. **Harvest** (in the motifs unit): every thing named more than once or at a turn, with its lines.
2. **Motifs.** From PLAN's `theme_question` and `core_opposition`, run B4's six tests on each candidate, rank it (`spine`, `supporting`, `single_scene`, `minor`, `plot_machinery`), keep within `motif_spines_max`, `sound_motif_max` and `body_motif_max`, and write its `appearance` items as scenes or story points (no shot exists yet), each with a role and emphasis (B4 §3.3; card 07).
3. **Characters.** For each: `tier`, `role`, `evidence` (quoted lines), `thesis` (the design idea in one sentence), `life_want`, `arc`, then:
   - the `lineup`: height, mass, shape, value, colour and tempo as words, so code can compare principals; they must differ in at least `lineup_columns_differ_min` columns (B5 R3; CRAFT-20);
   - for principals at Standard: the `face` (its three largest distinguishers, B5 R21); the `movement` field (home, stress and break effort, each as body part, direction, speed and what stays still; B5 §5.1-5.4); one `gesture` with its script line; `status_play` (default and the story points where it flips); `distance` (default and closest, in metres, with the scenes that change them; B5 §5.5);
   - the `fixed_description` last: within `fixed_description_words` for its tier; visible nouns only; no expression words (WORDS-05); no real person (WORDS-03); any sided feature in own terms, never image sides (SIDE-02);
   - casting placeholders stay `open`, never guessed; `likeness_basis` goes to a small choice.
4. **Voices.** One VOICE per speaking character (every principal has one): `voice_description` (within `voice_description_words`), `pitch`, `pace_wps` (default `speech_wps_default`; slower for weighted speakers: Saye 2.0), `accent` from WORLD, `path_sound` for each way the voice is heard (earpiece, recording, through glass); `source` goes to a small choice.
5. **Places.** For each LOCATION: `story_job`, `loudness` (at most `loud_sets_max` loud sets), `room_sound`, `anchor`, `exit`, `dressing`. Add a set plan (`plan_orientation`, `size`, `origin_corner`, `axes`, `wild_walls`, `object` and `mark` items, in metres; B3 §6) for every place used by a shot likely to need previs level `previs_plan_level_min` or more, a reflection or glass shot, or three or more people in one space; at Detailed, every place. Saye's kitchen: `size: [6.0, 3.6, 2.5]` from the south-west inside corner, west wall wild, `object: TABLE | at: [2.8, 1.8]`, `mark: IONA_MARK | at: [2.8, 2.55]`.
6. **Things.** Each PROP: `names`, `category`, `fixed_description`, `real_size`, `side` (own terms), `first_seen`, `motif`, `origin`. Every readable text becomes a TEXT record with the exact `words`, what it is `on`, its `reader`, `plot_critical` and `emphasis` (card 17).
7. **In-story cameras.** Each CAMERA: `at`, `lens_mm`, `ratio`, `fps`, `overlays`, `moves`, `master_clip`.
8. **Name check** every invented name (D4 Recipe 3): search it, then give the verdict (clear, a low-risk coincidence, or a conflict) as a `> ` note on its record; a conflict becomes a small choice proposing a rename (card 24).
9. **Check.** Run `stage.py check --step 4`; fix only the lines it prints, at most `repair_rounds_max` rounds.

## Record template

`templates/07 Characters and voices.md` (CHARACTER, VOICE), `templates/08 Places and things.md` (LOCATION, PROP, TEXT, MOTIF, CAMERA), `templates/01 Choices.md`.

## IDs you will be given

- Characters keep their step 1 IDs (`CH-SAYE`); a character with no cue is named here in capitals and hyphens (`CH-FIGURE`).
- You name the rest from the element in capitals and hyphens: `VO-SAYE`, `LOC-SAYE-KITCHEN`, `PR-FLASK`, `TX-TITLE-CATCH`, `MO-MINT`, `CAM-SHAFT-TOP`. Never rename or reuse one.
- CHOICE numbers come from the handout's block, in order.

## Batch and chunk rules

One unit for the motifs, one per principal character, one per `minor_characters_per_unit` minor characters, one per `places_per_unit` places, one for all things, text and in-story cameras. The Catch takes about 12 units.

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Does every speaking cue have a CHARACTER?
2. Does every principal have a VOICE, a lineup, a face, the `movement` field, a gesture, `status_play` and a distance?
3. Do principals differ in at least `lineup_columns_differ_min` lineup columns (CRAFT-20)?
4. Could a stranger draw each character from the fixed description alone, and is each within `fixed_description_words`?
5. Is any casting type guessed instead of left `open`?
6. Does every sided feature have an own side and an origin, with no image-side words?
7. Does every readable text have a TEXT record?
8. Does `check --step 4` exit 0?

## The report

After each unit, a short report (Done, Example, Made, Needs you: nothing, Next). After the last unit:

```
Done: step 5 of 12, characters, places and things.
Example: Saye's fixed description now reads "Dr Saye, a slim, upright woman in her
  late fifties, short neat grey hair, ...". It goes word for word into every picture
  prompt with her.
Made: 07 Characters and voices, 08 Places and things (with a floor plan of Saye's
  kitchen), and small choices in 01 Choices.
Needs you: nothing now. Faces, voices and names go to the big choices.
Next: continuity: how each person and thing appears in every scene.
```

## Checkpoint

None here. Design ideas and small choices (sides, casting placeholders, invented names, faces and voices) go to the big choices after step 5; what each principal's appearance must say is item 6 there.

## How to redo

- "Saye is frightened, not cold": only CH-SAYE runs again; `stage.py impact CH-SAYE` names every shot that cites CH-SAYE or CR-SAYE.
- A new place or thing found later is added with a new ID; nothing is renumbered.

## If you cannot run code

Every line reference is a quote anchor: `evidence` items, `gesture` lines, PROP `first_seen` and every `line:` are exact quotes of at least `quote_anchor_words_min` words, found once in the whole story (`- evidence: "fully dressed at four in the morning" | quote: "fully dressed at four in the morning"`).

1. Build each element's line list yourself: search the attached story for every alias and quote what you use.
2. Each unit's records go in one copy box with "Save as:" above it. The first unit that writes a file saves it under its name (`07 Characters and voices.md`); later units save theirs by content (`07 Characters and voices - Saye.md`, `08 Places and things - the kitchen and the quarantine.md`), and choices as `01 Choices - characters.md`; `adopt` merges them by ID (G10).
3. Small choices (`asked: no`) are written `status: defaulted`, and their default values go into the records at once (`likeness_basis: invented`, VOICE `source: designed`); if the user changes one at the big choices, that file is saved again.
4. Each box: plain part, divider, records, a `---` line, the checks-in-words table (`reference/06 Checks in words.md` part 1), the END line. Print "Checked in words: 14 of 14 passed" (or only the failures).
5. Report as above, then the resume line naming every file saved so far that the next unit needs:

```
Save as: 07 Characters and voices - Saye.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 05 Story plan,
06 World and style, 07 Characters and voices and its files, 08 Places and things and
its files, 09 Steps 03-06 - world, people, continuity, film rules and your story;
type: Continue my breakdown. Next is Iona.
```

**One-line task, again:** Design everything the film shows more than once (the characters and their voices, the places with their set plans, the things, the text in picture, the motifs and the cameras inside the story), each resting on quoted lines.
