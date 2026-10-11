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
- The numbered story, which you search for locale cues (procedure 1): words such as "torch" and "night bus", signs, vehicles, money, institutions.
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
3. **Propose three style directions** and the frame shape, in one CHOICE. STYLE `medium` is the user's; you write `style_words` (`style_words_count` plain, visible descriptors: no names of films or artists, no feelings, no banned words), `texture`, `words_to_avoid`. The style is "provisional until you see pictures": code writes `provisional: yes` until D5's test of three directions on three hard shots (the first job of the storyboards or of the generation packs), and `named_reference_policy`; never type either. Give the frame shape a story reason from the story's own images (B1 §5): The Catch's pairs face each other across tables and glass, so the default is the wide `2.39` frame.
4. **Write each story-world rule** as a RULE: `kind`, `statement`, `governs` (every ID it covers, or `none` with a note listing names step 4 will give IDs to), `exception` items (`<ID> | reads: normal | why:`). Anchor every rule to the exact lines where it starts and ends.
5. **For a mirror rule** (K03), write the eras through a CHOICE and its SETVALUE, since `era` is the user's field: each era's lines and its frame value, `original` or `reversed`, and note which elements start `original` and which `reversed` (step 5 records each element's handedness). The Catch:

   ```
   ### SETVALUE CHOICE-010-A
   - target: WR-MIRROR
   - era: a | from: 10 | to: 261 | frame: original
   - era: b | from: 263 | to: 1563 | frame: original
   - era: c | from: 1565 | to: 1852 | frame: reversed
   ```

   Era b starts at "Her eyes open." (line 263): the frame stays original and the world elements are reversed around Iona, Jude and Eli. Era c starts at "The ship is gone. The stars are gone." (line 1565). Detail rules follow K04: `WR-TITLES` (title cards always read normally), world screens, the copied name label, screen text, the replayed recording; each is one RULE listing what it governs (card 17, "Text orientation").
6. **Music.** One CHOICE for `SOUNDPLAN.music_policy` (`none`, `sparse`, `scored`, `source_only`) with a story reason; The Catch's default is `none`, because the pump and the engine click do music's job. No clip ever has music baked in, whatever the answer. SOUNDPLAN does not exist until step 6: code keeps the answer and writes `music_policy` when step 6 makes SOUNDPLAN (logged). Never write a SOUNDPLAN or a `music_policy` line yourself.
7. **Every choice the story does not state** becomes a CHOICE with a default, a one-line reason and `based_on` (the research reference). Keep `asked: yes` for the big ones; small ones are `asked: no` and go under "small choices I made". On a code surface write no `status` or `date`: code fills them when a choice is answered or defaulted.
8. **Check.** Run `stage.py check --step 3`; fix only the lines it prints, at most `repair_rounds_max` rounds.

## Record template

`references/templates/06 World and style.md` (STYLE, WORLD, RULE), `references/templates/01 Choices.md` (CHOICE, SETVALUE), and the PROJECT part of `references/templates/00 Start here.md` for `prompt_words`.

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
3. Write each CHOICE's `status: open`, each record's `status` and `locked`, and STYLE `provisional: yes` and `named_reference_policy: describe_qualities_only`.
4. Each box: plain part, divider, records, a `---` line, the checks-in-words table (`references/formats/06 Checks in words.md` part 1), the END line. Print "Checked in words: 14 of 14 passed" (or only the failures).
5. Report as above, then the resume line:

```
Save as: 06 World and style.md, 01 Choices - world and style.md   (save only boxes that end with the END line)
To continue later: new chat in this project; attach, in two messages, 00 Start here,
01 Choices and its files, 04 Scene list and its plan files, 05 Story plan, 06 World and
style, 09 Steps 03-06 - world, people, continuity, film rules and your story;
type with the second: Continue my breakdown. Next is characters, places and things.
```

**One-line task, again:** Decide once where and when the story happens, the film's style, and the rules of the story's world, turning every choice the story leaves open into a choice for the user with a default and a reason.
