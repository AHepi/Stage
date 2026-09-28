# Step 2. Story plan

This is step 2 of the pipeline; the user counts it as step 3 of 12, "planning the whole story". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Plan the whole film before any scene is designed: what each scene changes, the groups of scenes, one climax and its crisis, the peaks, what is planted and paid off, and who knows what.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Write the film-level plan every later choice rests on; for prose also which chapters and strands survive, the format, the scope of the scene work, and the step outline (the book's scenes in screen order).

## When it runs

Once, after the scene or chapter list, never reading the whole text at once.

## Inputs

- The numbered story, in slices: one unit's scenes or chapter at a time.
- SCENE or CHAPTER records from step 1, and the answers to the length question.

## Outputs

- `05 Story plan.md`: PLAN, SEQUENCE, PLANT, and FACT (at Standard only for facts in suspense, mystery or dramatic irony, about `fact_records_typical` in a film; at Detailed every fact). Prose adds CHAPTER digests, STRAND and CARDINAL.
- `04 Scene list.md`: the plan fields on each SCENE (procedure, and `sequence`; code writes `target_duration_s`). Prose: the SCENE records of the step outline.
- `06 World and style.md`: prose only, RULE records of kind `device` (letters, refrains).
- `01 Choices.md`: a second climax reading when two are defensible; prose, the plan choice.

No beat or shot exists yet, so a moment inside a scene is a **story point**: the scene ID and a quote anchor, `SC24 "She deletes the way home."` (G5), resolved to a beat by code at step 7.

## Card parts to open

- At every depth: card 01, whole; card 08, part "Genre and tone".
- When the source is not a screenplay: also card 02, whole.

## Procedure

**Screenplay.**

1. **Event units** (U-02-SC01..SC10 and on). For each scene write `event` (one past-tense sentence naming the deed, no psychology; D2 §3.4), `scene_intensity` (across the whole film; exactly one 10 or one 10 range, on the climax; card 01 question 5), `whose_scene`, `story_day` (`D1`, `N1`), `rhythm_class` (read only by the estimate, never a design target), `tone` and `tone_undercurrent` (D10 §2.1 values), and `tags` (they choose which situation cards step 7 opens).
2. **Film unit** (U-02-FILM). Read only the event lines, with short quoted evidence, and write:
   - PLAN: `logline`, `theme_question`, `core_value` (`name | positive: | negative:`), `core_opposition` (two nouns), `crisis` (a story point), `climax` (a scene or range), `act` items, `peak` items (a reason for any peak away from the climax; PLAN-03), `pov_plan`, `genre`, `tone_home`, `tone_range`, `tone_mix_rule`.
   - SEQUENCE records, one list for the whole film, and each scene's `sequence`.
   - PLANT records with `planted_at` and `paid_off_at` as story points; shots link to them at step 8.
   - FACT records for what the audience and each character know, from when, with `element` naming what would give the fact away in frame.
   - If two climax readings are defensible, write both into one CHOICE for the big choices (The Catch's default: climax `SC26..SC27`, crisis `SC24 "She deletes the way home."`, K12; D16 §8.6).
3. **Compression unit** (U-02-COMPRESS), only for a shorter target: CARDINAL records by the deletion test, then the compression plan in D2 R10's order (trim, merge, fold, then cut a strand) as SCENE `keep` and `merged_into` and PLAN `op` items; never rewrite a line of the story.

**Prose.**

1. **Digest units**, one per chapter (U-02-CP01 on): a CHAPTER `digest` of at most `chapter_digest_words_max` words (events, people, places, time markers, the lines that matter by number), `people`, `places`, `time_markers`, `pov`, and `candidate` scenes with A3's five-test scores and decisions (A3 §7.9).
2. **Whole-book unit** (U-02-BOOK) reads only the digests: STRAND and CARDINAL records, RULE records of kind `device`, and two or three independent macro plans as PLAN `plan_option` items with runtime, scene and shot budgets, cost and review hours from `stage.py estimate --version v0` (D2 R1).
3. **Checkpoint P** (below).
4. **Outline units** (U-02-OUTLINE-P1 on, `outline_chapters_per_unit` chapters each) write the chosen plan's SCENE records in screen order with the IDs the handout gives: `heading`, `int_ext`, `place_text`, `time_text`, and `from_lines`, or `origin: invented`; code works out `lines` from `from_lines`. Then PLAN, SEQUENCE, PLANT and FACT for the kept scenes.

**Both.** Run `stage.py check --step 2`; fix only the lines it prints, at most `repair_rounds_max` rounds.

## Record template

`templates/05 Story plan.md` (PLAN, SEQUENCE, PLANT, FACT, CHAPTER, STRAND, CARDINAL), `templates/04 Scene list.md` (SCENE plan fields), `templates/06 World and style.md` (RULE), `templates/01 Choices.md`.

## IDs you will be given

The handout (in chat, you, in order) gives `SQ01`, `PL-01`, `FT-01` on, and for prose `ST-01`, `CF-01` and the step outline's scene IDs (`SC01` to `SC48` for The Long Places' plan A; 3 digits above `scene_ids_three_digits_above` scenes). Use them in order, never reusing one.

## Batch and chunk rules

- Screenplay: one event unit per `event_unit_scenes` scenes (The Catch: 3 units), 1 film unit, and the compression unit only when needed.
- Prose: one digest unit per chapter, 1 whole-book unit, about 6 outline units.

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Does each event sentence name a change, in the past tense, with no psychology?
2. Is there exactly one climax, with the one scene intensity 10 (or 10 range) on it (PLAN-01)?
3. Is the climax the core value's last turn, and the crisis the choice that forces it?
4. Is every scene in exactly one sequence (COVER-06)?
5. Does every plant have a payoff (PLAN-02), and every peak away from the climax a reason?
6. Is every story point's quote found once in its scene?
7. Prose: is every cardinal event in a kept scene, every step target within `step_outline_tolerance` of the runtime target, and the scope set?
8. Does `check --step 2` exit 0?

## The report

Screenplay (The Catch):

```
Done: step 3 of 12, planning the whole story.
Example: the story turns for the last time at the crossing beside the ship, in
  scenes 26 and 27. "She deletes the way home." in scene 24 is the choice that
  forces it.
Made: 05 Story plan (the turns, 9 groups of scenes, what is planted and paid off,
  who knows what, and when), and one plain line for each scene in 04 Scene list.
Needs you: nothing now. Another reading of the climax waits for the big choices.
Next: I'll settle where and when the story happens, and the film's style.
```

## Checkpoint

Screenplay: none here; a second climax reading goes to the big choices.

Prose: checkpoint P, "how the book becomes a film"; it blocks. The plans stand side by side, each with what the audience loses. Default for The Long Places: plan A, with chapter I first as a trial, which sets `PROJECT.scope` to its scenes (5 of 48); the device rules are small choices. Checks, the film pass, estimates and exports then cover only the scenes in scope ("Scope: 5 of 48 scenes"); "go on to chapter II" widens it. The message (`reference/07`; your own counts):

```
Done: step 3 of 12, planning the whole book (14 chapters, 49,152 words).
Example: in plan A, chapter I gives five scenes; the fifth is Nilay on the threshold at
  night, where a warmth leans against her right shoulder and she does not turn her head.
Made: 05 Story plan (14 chapter digests, 11 strands, 10 events the story cannot lose,
  three plans).

How should the book become a film? Reply "defaults", or answer by number.
1. A. A feature, about 100 minutes, 48 scenes, about 1,300 shots. Keeps Nilay and Emre
      whole, with the breach as the middle; loses Malta, much of the village's grief,
      Yusuf's redemption.
   B. Six episodes of about 48 minutes, about 120 scenes, about 3,900 shots. Keeps
      nearly everything.
   C. A 15-minute short from chapters I and XIV, 11 scenes, about 200 shots. Keeps the
      brother and the ending; loses everything else.                               [A]
2. Start the scene work with chapter I as a trial (5 of the 48 scenes), then decide
   whether to go on.                                                               [yes]
3. Small choices I made (3): the letters open and close the film; the cave-mouth passage
   uses one saved camera setup each time it returns, with only the minutes changing;
   letter II has no voice-over, only the humming.                                  [accept]
Next: characters, places and things for what the plan keeps.
```

## How to redo

- "Redo the story plan" rewrites unlocked plan records and lists scenes citing changed sequences or plants.
- "Make it 20 minutes" runs the compression unit again; cut scenes become `omitted`, keeping their numbers.

## If you cannot run code

Every line reference is a quote anchor: story points are a scene ID and an exact quote of at least `quote_anchor_words_min` words, found once in that scene; `from_lines` and CARDINAL `lines` are anchor pairs. Never add the ` = SC24-B05` ending; code writes it later.

1. Steps 0 to 2 share one chat (`08 Steps 00-02 - start, reading, plan.md`).
2. Save each event unit's SCENE plan fields as `04 Scene list - plan, scenes 01-10.md` and so on (merged by ID, G10). The film unit saves `05 Story plan.md`, and a climax CHOICE (`status: open` until the big choices) as `01 Choices - story plan.md`.
3. Prose: each digest saves `05 Story plan - chapter I.md` again, whole; each outline unit saves `04 Scene list - chapters I-III.md`; the whole-book unit saves `05 Story plan.md` and the plan choice in `01 Choices - story plan.md`, each plan's estimate rough and labelled so (D13 R4). After checkpoint P, save the choice file again with the answers, and `00 Start here.md`. From step 3 on, attach `05 Story plan` without the chapter files.
4. Each copy box: "Save as:" above it; plain part, divider, records, a `---` line, the checks-in-words table (`reference/06` part 1), the END line. Print "Checked in words: 14 of 14 passed" (or only the failures).
5. Report, then the resume line:

```
Save as: 05 Story plan.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 01 Choices and
its files, 04 Scene list and its plan files, 05 Story plan, 09 Steps 03-06 - world, people,
continuity, film rules and your story; type: Continue my breakdown.
Next is world and style.
```

**One-line task, again:** Plan the whole film before any scene is designed: what each scene changes, the groups of scenes, one climax and its crisis, the peaks, what is planted and paid off, and who knows what.
