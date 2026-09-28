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
  late fifties, ...". It goes word for word into every picture prompt with her.

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
