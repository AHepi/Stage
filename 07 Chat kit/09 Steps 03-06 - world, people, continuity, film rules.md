# 09 Steps 03-06 - world, people, continuity, film rules

Part of the Stage chat kit: a step-group file, attached to the chat that runs one of these steps (not knowledge). It joins the step files 03 World and style, 04 Characters, places and things, 05 Continuity, 06 Film rules, each whole. Read the one for this unit every time, quote its one-line task back before any work, and follow its section "If you cannot run code" when this chat has no code. 01 House rules (in the knowledge) says where every other skill file is.

---

From the skill file `steps/03 World and style.md`:

# Step 3. World and style

This is step 3 of the pipeline; the user counts it as step 4 of 12, "world and style". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Decide once where and when the story happens, the film's style, and the rules of the story's world, turning every choice the story leaves open into a choice for the user with a default and a reason.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Decide once where and when the story happens, what the whole film is made to look like, and the story-world rules. Everything the story does not state becomes a CHOICE with a default and a reason; the user answers them all at once with the big choices, after step 5.

## When it runs

Once, after the story plan. One unit (U-03-WORLD) for the whole film.

## Inputs

- PLAN and the SCENE records (events, tones, tags).
- Locale cues harvested by code, each with its line: words such as "torch" and "night bus", signs, vehicles, money, institutions.
- The answers to the length question.

## Outputs

- `06 World and style.md`: STYLE, WORLD, and one RULE per story-world rule, such as `WR-MIRROR` with its eras, an exception rule such as `WR-F-EXCEPTION`, `WR-TITLES`, and for prose the recurring-device rules of step 2.
- `01 Choices.md`: CHOICE records (`asked: yes`, `checkpoint: b`) for place and time, style and frame shape, music, and each group of story-world rules, with SETVALUE records for structured answers such as the era lines. A tone CHOICE only when `tone_home` is unclear from the story.
- `00 Start here.md`: PROJECT `prompt_words` (`torch | use: flashlight`, K19).

## Card parts to open

- At every depth: card 08, whole; card 17, part "Text orientation".
- When a rule concerns handedness (a mirror rule): also card 16, whole.

## Procedure

1. **Harvest the locale cues** with their evidence, and label each `inferred`. The Catch never names a country, but "Torchlight on wet brick." and "A night bus comes at them" point to Britain. Write them as WORLD `evidence` items (`12 | quote: "Torchlight on wet brick."`), with `origin: inferred` (D17 R1).
2. **Propose the world:** a default and one alternative. WORLD `place` and `period` are the user's (through the place-and-time CHOICE, whose `sets` lines write them); you write `drives_on`, `language`, `accents`, `signage`, `emergency_lights`, `institutions`, `money`, `evidence` and `origin`. Check the real colours of local signals (British emergency lights are blue; B2 R19). A real institution keeps its researched grammar under an invented name (D17 R12). A cue that conflicts with the rest is a question with both readings, never a quiet change (D17 R2).
3. **Propose three style directions** and the frame shape, in one CHOICE. STYLE `medium` is the user's; you write `style_words` (`style_words_count` plain, visible descriptors: no names of films or artists, no feelings, no banned words), `texture`, `words_to_avoid`. Mark the style "provisional until you see pictures": `provisional` stays `yes` until D5's test of three directions on three hard shots, the first job of the storyboards or of the generation packs. Give the frame shape a story reason from the story's own images (B1 §5): The Catch's pairs face each other across tables and glass, so the default is the wide `2.39` frame.
4. **Write each story-world rule** as a RULE: `kind`, `statement`, `governs` (every ID it covers, or a note listing names step 4 will give IDs to), `exception` items (`<ID> | reads: normal | why:`). Anchor every rule to the exact lines where it starts and ends.
5. **For a mirror rule** (K03), write the eras through a CHOICE and its SETVALUE, since `era` is the user's field: each era's lines and its frame value, `original` or `reversed`, and note which elements start `original` and which `reversed` (step 5 records each element's handedness). The Catch:

   ```
   ### SETVALUE CHOICE-010-A
   - target: WR-MIRROR
   - era: a | from: 10 | to: 261 | frame: original
   - era: b | from: 263 | to: 1563 | frame: original
   - era: c | from: 1565 | to: 1852 | frame: reversed
   ```

   Era b starts at "Her eyes open." (line 263): the frame stays original and the world elements are reversed around Iona, Jude and Eli. Era c starts at "The ship is gone. The stars are gone." (line 1565). Detail rules follow K04: `WR-TITLES` (title cards always read normally), world screens, the copied name label, screen text, the replayed recording; each is one RULE listing what it governs (card 17, "Text orientation").
6. **Music.** One CHOICE for `SOUNDPLAN.music_policy` (`none`, `sparse`, `scored`, `source_only`) with a story reason; The Catch's default is `none`, because the pump and the engine click do music's job. No clip ever has music baked in, whatever the answer.
7. **Every choice the story does not state** becomes a CHOICE with a default, a one-line reason and `based_on` (the research reference). Keep `asked: yes` for the big ones; small ones are `asked: no` and go under "small choices I made".
8. **Check.** Run `stage.py check --step 3`; fix only the lines it prints, at most `repair_rounds_max` rounds.

## Record template

`templates/06 World and style.md` (STYLE, WORLD, RULE), `templates/01 Choices.md` (CHOICE, SETVALUE), and the PROJECT part of `templates/00 Start here.md` for `prompt_words`.

## IDs you will be given

- Rule IDs are named from the rule in capitals and hyphens (`WR-MIRROR`, `WR-TITLES`, `WR-F-EXCEPTION`); a name once used is never reused.
- CHOICE numbers come from the handout's block, in order; each SETVALUE takes its choice's number and the option letter (`CHOICE-010-A`).
- STYLE and WORLD are single records with no ID (`### STYLE`, `### WORLD`).

## Batch and chunk rules

One unit for the whole film. It reads the plan and the harvested cues with their lines, never the whole story.

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Are STYLE and WORLD present?
2. Does every choice the story does not state have a CHOICE with a default and a reason?
3. Is every WORLD value the story does not state `inferred` from a quoted cue, or left to a CHOICE?
4. Does every story-world rule have start and end lines found in the story, and a list of what it governs (each ID existing, or listed for step 4)?
5. Are the style words within `style_words_count`, visible, and free of names, feelings and banned words (WORDS-03)?
6. Does the frame shape have a reason taken from the story's own images?
7. Does `check --step 3` exit 0?

## The report

```
Done: step 4 of 12, world and style.
Example: your script never names a country, but "Torchlight on wet brick." and the
  night bus point to Britain, so I propose an unnamed British city, today, cars on
  the left, with British voices.
Made: 06 World and style (the world, three possible styles, the rules of the mirror
  world), and their choices in 01 Choices.
Needs you: nothing now. You'll see these choices together with the big choices,
  after the continuity step.
Next: characters, places and things.
```

## Checkpoint

None here. Every CHOICE this step writes (place and time, style and frame shape, music, the story-world rules, the tone when unclear) is shown at the big choices after step 5, in the order step 5 gives, with its default.

## How to redo

- "Make it animated": STYLE changes; shot designs stand; fixed descriptions, look blocks and every compiled prompt are marked stale.
- A different place or time: answer the place-and-time CHOICE again; WORLD changes, and `stage.py impact` lists every record that cites it.
- An era moved to other lines: a new answer to its CHOICE writes a new SETVALUE; every scene and state in the changed era goes stale.

## If you cannot run code

Every line reference is a quote anchor: `evidence` items, RULE start and end lines and era lines are exact quotes of at least `quote_anchor_words_min` words, found once in the whole story. A line too short to quote ("She fires.") is reached by quoting the line before it: an era's `to` runs on through the short lines that follow its anchor. The Catch's eras in chat:

```
- era: a | from: "INT. MEDICAL FACTORY - LOADING TUNNEL - NIGHT" | to: "A dark with nothing in it." | frame: original
- era: b | from: "Her eyes open." | to: "The whole outline clears the hull's last projection." | frame: original
- era: c | from: "The ship is gone." | to: "Three uneven strokes in the dark." | frame: reversed
```

1. Harvest the locale cues yourself from the attached story: search it for place words, signs, vehicles, money and institutions, and quote each exactly.
2. Write `06 World and style.md` in one copy box with "Save as:" above it, and the new CHOICE and SETVALUE records in a second box saved as `01 Choices - world and style.md` (`adopt` merges it with `01 Choices.md` by ID, G10). Leave the user's fields `open` in STYLE `medium`, WORLD `place` and `period` and RULE `era` until the big choices are answered; step 5's chat writes them then. PROJECT `prompt_words` waits for the next save of `00 Start here`.
3. Write each CHOICE's `status: open` and each record's `status` and `locked`.
4. Each box: plain part, divider, records, a `---` line, the checks-in-words table (`reference/06 Checks in words.md` part 1), the END line. Print "Checked in words: 14 of 14 passed" (or only the failures).
5. Report as above, then the resume line:

```
Save as: 06 World and style.md, 01 Choices - world and style.md   (save only boxes that end with the END line)
To continue later: new chat in this project; attach, in two messages, 00 Start here,
01 Choices and its files, 04 Scene list and its plan files, 05 Story plan, 06 World and
style, 09 Steps 03-06 - world, people, continuity, film rules and your story;
type with the second: Continue my breakdown. Next is characters, places and things.
```

**One-line task, again:** Decide once where and when the story happens, the film's style, and the rules of the story's world, turning every choice the story leaves open into a choice for the user with a default and a reason.

---

From the skill file `steps/04 Characters, places and things.md`:

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
  fifties, short neat grey hair, ...". It goes word for word into every picture
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
To continue later: new chat in this project; attach, in two messages if they are
more than 10 files, 00 Start here, 04 Scene list and its plan files, 05 Story plan,
06 World and style, 07 Characters and voices and its files, 08 Places and things and
its files, 09 Steps 03-06 - world, people, continuity, film rules and your story;
type with the last: Continue my breakdown. Next is Iona.
```

**One-line task, again:** Design everything the film shows more than once (the characters and their voices, the places with their set plans, the things, the text in picture, the motifs and the cameras inside the story), each resting on quoted lines.

---

From the skill file `steps/05 Continuity.md`:

# Step 5. Continuity

This is step 5 of the pipeline; the user counts it as step 6 of 12, "continuity". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Record the state of every changeable person, thing and place in every scene, each change with the line that causes it and every side in its own terms, then put the big choices to the user.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Know the state of every changeable element in every scene, with the line that changed it, and every side. Then close the first half of the work with the big choices (checkpoint B), and write the whole-film summary every scene unit reads.

## When it runs

After characters, places and things: units of scenes in story order, then the big choices, then the summary.

## Inputs

- The unit's scenes, in slices, with the states entering them (the exit states of the unit before).
- CHARACTER, PROP and LOCATION records (fixed descriptions, sides); RULE records, above all a mirror rule.

## Outputs

- `09 Continuity.md`: STATE records (`CH-IONA.S02`, `PR-FLASK.S02`, `LOC-QUARANTINE.S02`): `element`, `from`, `cause`, `state_line` (words pasted after the fixed description in prompts), `changes`, `side` items in own terms, `handedness` (`original` or `reversed`, only under a mirror rule), `origin`.
- `01 Choices.md`: small choices for sides the story does not confirm; the checkpoint answers.
- After the big choices: `02 Whole-film summary.md` (code writes it; the AI in chat).

## Card parts to open

- At every depth: card 05, part "State lines".
- When a handedness (mirror) rule exists: also card 16, whole.

## Procedure

1. **Walk the lines** of the unit's scenes in order. At each scene's start copy the previous exit state into the entry, exactly; under `CONTINUOUS` it must match (STATE-03).
2. **Add each change** as a new STATE with its `cause` line quoted (STATE-02) and `from` naming where it starts (`from: SC06 | line: 263`). Code works out `until` from the next state; never type it.
3. **Write each state line** from visible nouns: what is worn, carried, torn, bloodied. No image-side words ("frame left") ever (SIDE-02); a sided feature goes in a `side` item with `own: left` or `own: right` and `plot: yes` when the story needs that side (SIDE-01).
4. **Apparent sides** (K03). A side the story states for an element that is mirrored on screen is an apparent side: record the own side and mark `origin: inferred`. The Catch, era b: "Saye's wedding ring. On her right hand." (line 436) is her own left:

   ```
   ### STATE CH-SAYE.S01 Dressed at four in the morning
   - element: CH-SAYE
   - from: SC10 | line: 399
   - cause: 399 | quote: "fully dressed at four in the morning"
   - state_line: dark grey trousers and flat black shoes, a stethoscope round her neck, a plain gold ring on her left hand
   - changes: first seen
   - side: wedding ring | own: left | plot: yes
   - handedness: reversed
   - origin: inferred
   ```

5. **Gaps.** A difference the story does not explain is recorded `origin: inferred` at first sight with the gap named in `changes`, or raised as a CHOICE. An unconfirmed side becomes a small choice for checkpoint B.
6. **Check.** Run `stage.py check --step 5`; fix only the lines it prints, at most `repair_rounds_max` rounds.
7. **Checkpoint B** (below). Then the whole-film summary: code writes it; in chat the AI writes it as unit U-05-SUMMARY.

## Record template

`templates/09 Continuity.md` (STATE), `templates/01 Choices.md` (CHOICE, SETVALUE).

## IDs you will be given

A state's ID is its element's ID, `.S` and two digits in story order: `CH-IONA.S01` is Iona as she first appears, `CH-IONA.S02` her next state. Continue each element's numbers from the unit before; never renumber. CHOICE numbers come from the handout's block.

## Batch and chunk rules

One unit per `continuity_unit_scenes` scenes (U-05-SC01..SC05 on; 6 units for The Catch), carrying the exit states forward; for prose, one unit per sequence (U-05-SQ01 on). The big choices are one message after the last unit.

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Does every change cite a line found in the story?
2. Does every `CONTINUOUS` scene inherit the previous exit state?
3. Is every element named in a scene given a state valid there?
4. Is anything worn, carried or hurt in a scene without a state?
5. Does every sided feature have an own side and an origin, and no state line an image-side word?
6. Does the big-choices message hold at most `checkpoint_b_items_max` items, in the order below, with `checkpoint_b_marked_items` marked?
7. Does `check --step 5` exit 0?

## The report

After each unit, a short report (Done, Example, Made, Needs you: nothing, Next). After the last unit the report is the big-choices message.

## Checkpoint

Checkpoint B, shown to the user as "the big choices". It blocks. One message, at most `checkpoint_b_items_max` numbered items, each one or two lines with its default and reason, in this order: the climax reading; style and frame shape (with the home tone in the same line, only when it is unclear); place and time; music; the story-world rules (grouped, with eras and exceptions); what each principal's appearance must say (one sentence each); "small choices I made" (one accept item pointing to `01 Choices`). Mark with * the `checkpoint_b_marked_items` choices whose change would redo the most records (from each CHOICE's `affects`; for The Catch: the frame shape, the mirror world, the climax). The Catch (`reference/07`):

```
Done: steps 4 to 6 of 12 (world and style; characters, places and things; continuity).
Example: Saye's fixed description now reads "Dr Saye, a slim, upright woman in her
  fifties, ...". It goes word for word into every picture prompt with her.

The big choices. Reply "defaults", or answer by number.
*1. The climax: the crossing beside the ship (scenes 26 and 27), where the main
    question is settled for good. "She deletes the way home." (scene 24) is the
    choice that forces it; the chest opening (scene 25) is the biggest reveal.     [26-27]
*2. Style and frame shape: like a real film, clinical and plain (for now: you'll
    choose by eye when pictures are made); wide cinema frame, 2.39 to 1, because
    people face each other across glass and tables.                              [yes]
 3. Place and time: the script never names a country. An unnamed British city,
    today, cars on the left, British voices (from "torch" and "night bus").       [yes]
 4. Music in the finished film: none; the pump and the engine click do music's
    job. No clip ever has music baked in.                                          [none]
*5. The mirror world: normal until "CLACK." (line 259); from "Her eyes open."
    (line 263) the world is mirrored around the three of them until "She fires."
    (line 1563); after that only Eli and Jude stay mirrored. Plus 6 detail rules
    (the toy carriage's Fs read normally, world screens mirrored, and the rest).   [as written]
 6. What each main character's appearance must say: Iona, a working body whose flat
    hand tests whether things will hold; Saye, tidy grey control with one living
    thing that becomes her proof. (Jude, Eli, Nell and the figure are in 07.)      [all fine]
 7. Small choices I made: 23 in 01 Choices, including which hand and shoulder carry
    each injury, how the kitchen in scene 10 is staged, and the fall in scene 6
    told longer than real time from overlapping real-time pieces, never slow motion. [accept]
Next: I'll write the film's camera, light and sound rules from these answers,
then design scene 1.
```

Print your own computed counts. On a code surface pass each answer on as `### CHOICE CHOICE-NNN` with `- answer: <letter>` (or `- answer: defaults` for all) in the inbox, and run `stage.py apply`: the answers set their fields and SETVALUE lines and lock the step 2 to 5 records they name. Then code writes `02 Whole-film summary.md`.

## How to redo

- "Redo continuity from scene 12": units from scene 12 run again; earlier states stand.
- A new side or injury found later is a new STATE; `stage.py impact` lists the shots that show the element.
- A big choice changed later ("make it 16:9") is answered again; the AI lists what it affects in plain words first and asks once if it is costly.

## If you cannot run code

Every line reference is a quote anchor: `from` and `cause` quote the story exactly, at least `quote_anchor_words_min` words, found once in the whole story (`- from: SC10 | line: "fully dressed at four in the morning"`, `- cause: "fully dressed at four in the morning" | quote: "fully dressed at four in the morning"`).

1. Save each unit's STATE records in one copy box: `09 Continuity.md` first, then `09 Continuity - scenes 06-10.md` and so on (merged by ID, G10).
2. After the big-choices answers, write in copy boxes: `01 Choices.md` again, whole, with every choice's `status` (`answered` or `defaulted`), `answer` and `date`; `00 Start here.md` again, whole, with "Big choices so far" and the PROJECT values the answers set (`frame_shape`) or earlier steps filled (`genre`, `tone_home`, `tone_range`, `prompt_words`); `06 World and style.md` again, whole, with the answered values in place of `open` (STYLE `medium`, WORLD `place` and `period`, RULE `era`) and any other file whose values an answer changed; then unit U-05-SUMMARY, `02 Whole-film summary.md`: the scene list with events, sequences and plan fields, fixed descriptions, state lines, voices, the `movement` field and status lines, FACT and PLANT lines and world rules, without set plans, at most `whole_film_summary_words_max` words. Tell the user which earlier choice files to delete. Leave `locked` as saved; `adopt` sets the locks from the answered choices.
3. Each box: plain part, divider, records, a `---` line, the checks-in-words table (`reference/06 Checks in words.md` part 1), the END line. Print "Checked in words: 14 of 14 passed" (or only the failures).
4. Report, then the resume line:

```
Save as: 02 Whole-film summary.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach, in two messages if they are
more than 10 files, 00 Start here, 01 Choices, 02 Whole-film summary, 05 Story plan,
06 World and style, 07 Characters and voices and 08 Places and things with their files,
09 Steps 03-06 - world, people, continuity, film rules and your story;
type with the last: Continue my breakdown. Next is the film's rules.
```

**One-line task, again:** Record the state of every changeable person, thing and place in every scene, each change with the line that causes it and every side in its own terms, then put the big choices to the user.

---

From the skill file `steps/06 Film rules.md`:

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
- SOUNDPLAN: music policy from the big choices, the clip audio rule, `voice_policy`, `device_budget`, `rupture_plan`.
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
4. **Saved choices and lens exceptions.** Each RESERVE: `choice`, `match` (how code knows a use: `size = extreme_close_up`), `max_uses`, `allowed_in`, `never_on`, `because`; always the two film-level ones above (B1 P5; FILM-08). Each LENS names exactly where it is allowed (CRAFT-07).
5. **Looks** (U-06-LOOKS), one per place and time in use: the main light placed in the room (`from:` a set-plan object or a wall), so code works out its frame side per shot and per era; hold light as the look unless a story source changes it; a `light_cue` only where the story causes one (card 11). The look block stays within `look_block_sentences` and `look_block_words_max`.
6. **Colour script** (U-06-PLANS): one VISUAL row per sequence, peaks first, valleys lower, then the monotony test (no `colour_monotony_run` sequences alike without a reason; B2 §8.3).
7. **Visual structure**: for each sequence, `space`, each `component` (hold, progress or contrast, with why) and any `counterpoint` (B3 §2.6).
8. **Sound plan**: `music_policy` as answered; `device_budget` within `device_budget_short` for a short; the `rupture_plan` from the peaks; `voice_policy` as a small choice.
9. **The ladder**: one `rung` per scene with a main turn, as a story point with size, hold and why. It escalates by size and hold together; other scenes' main turns land at close-up or on a deliberate wide (A2 R4, R31). The Catch: `rung: SC10 "Her face changes." | size: close_up | hold: long | why: ...`, leaving the tightest size for scene 13.
10. **Check.** Run `stage.py check --step 6`; fix only the lines it prints, at most `repair_rounds_max` rounds.

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

1. Save the three units' records as `10 Film rules.md`, then `10 Film rules - looks.md` and `10 Film rules - colour, sound and ladder.md`; `adopt` merges them by ID (G10). Save the voice choice, a small choice written `status: defaulted`, as `01 Choices - film rules.md`, and write its default (`voice_policy: designed_only`) in SOUNDPLAN.
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
