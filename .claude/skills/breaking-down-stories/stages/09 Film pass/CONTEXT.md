# Step 9. Film pass

This is step 9 of the pipeline; the user counts it as step 10 of 12, "the film pass". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Judge the whole film as one structure before any picture is made: run the film checks, answer the film pass questions in a fresh unit, and turn every "no" into a finding with its fix.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Scenes were designed one at a time; this step reads them as one. The Catch: scene 29's reflection shot must repeat scene 10's framing (the same long lens, level, along the glass) for the rhyme to land, and no scene before scene 13 may spend the film's tightest size. No single scene can see either. Structure beats single frames (B3 P4): a film whose every scene spends its strongest choice has nowhere to go. It finds where the film repeats itself or spends too early, and sends each fix to the scene that needs it.

## When it runs

Once, after the last sequence's shots are written, before the health check. At quick depth only the code audits run: there are no full shots to judge. With a partial scope (The Long Places, chapter I as a trial) it covers the scenes in scope only. "Run the film pass again" runs it again at any time.

## Inputs

- The **film strip**, made by code: one line per shot with its ID, beats, role, size, lens, camera move, saved choice used, emphasis, screen time and the scene's intensity. For example: `SC10-SH150 | SC10-B07, SC10-B08 | turn | close_up | 50 | static | none | MO-MINT 2 | 15 | 6`.
- The film rules: CAMSYS, CAMRULE, RESERVE, LENS, LOOK, VISUAL, SOUNDPLAN, LADDER.
- PLAN (`crisis`, `climax`, each `peak` and its reason), MOTIF appearances, and the SCENE records (plan fields, turn pictures).
- The checker's film-level report.

Judgement works from these, never the story whole.

## Outputs

- `12 Whole-film check.md`: the plain part (code's audit report: what was checked, found and fixed), the divider, one FINDING per problem, the END line. Code writes the checker's findings (`source: checker`); the judgement unit writes its own (`source: film_pass`).
- CHOICE records in `01 Choices.md` for findings that change a creative choice, usually none to three.
- Fixes, routed back to steps 7 and 8 for the named scenes only.

## Card parts to open

At every depth: card 09, part "Film pass".

## Procedure

1. **Code audits.** Run `stage.py check --film`. It builds the film strip and runs FILM-01 to FILM-12 and TIME-07; card 09, "Film pass", says what each one catches. Two are errors: FILM-03 (a character camera rule broken: Eli closer than `medium_close_up` before scene 13) and FILM-08 (a saved choice over its uses or outside its places, including the film-level extreme close-up and push-in). The rest are warnings. Code writes one FINDING per problem.
2. **Fix what the checker found.** Every error is fixed. Every warning is fixed or accepted with a `reason` that quotes the story or cites a record: FILM-02's warning on scene 29 is accepted because the sides are reversed on purpose, Iona being turned back (B3 P8). `stage.py impact <ID>` names what a fix touches; redo only those units of steps 7 and 8. Fix only the lines printed, at most `repair_rounds_max` rounds (C5 R13), then trace the fault to its earliest wrong record or ask one plain question.
3. **Judgement unit** (U-09-JUDGE; `next` may hand it out before or after the item 2 fixes). A fresh unit that wrote none of the shots answers these questions, one scene or turn at a time, each naming and quoting its record (C5 R12; D7 R3):
   - **Sound-off test:** with the sound off, does each turn picture tell its beat (B3 §10.1)? "Does shot 150's picture (Iona chews, stops, frowns) tell beat 7, 'Her face changes.', without her line?"
   - **Stranger test:** could someone who has not read the story say what changes in each scene from its turn pictures and purposes alone (D7 §7)?
   - **Heavy-handedness:** a symbol the story does not hold (B3 R24; B4 R25)? More than `plant_inserts_per_scene_max` inserts of plants in one scene? Music under a beat whose meaning is unsaid (A4 §7.6)? A light cue timed to the line that states the point (B2 §12)? A rhyme the story does not support (B3 P8)?
   - **Different film:** does any shot feel as if it belongs to a different film (B3 R26)?
4. **Write the findings.** Each "no" becomes a FINDING: `record` (the shot, scene or film rule), `rule` (the check ID, or the question as asked), `evidence` (the record's words and the story line they rest on), `fix`, `source: film_pass`, `status: open`. A finding with no quoted evidence is dropped (D7 R4).
5. **Sort the findings.** A fix that only brings a shot back inside the film rules is made and logged, and its FINDING set `fixed`. A finding that changes a creative choice (a peak moved, a saved choice spent somewhere else, a rhyme dropped, a scene played in a different tone) becomes a CHOICE with a default and its reason, `asked: yes`, `checkpoint: acceptance`, and the FINDING stays `open` until it is answered.
6. **Check.** Run `stage.py check --step 9` (`next` waits on it until it passes): every FILM error fixed, every FINDING `fixed` or `accepted` with a reason, or `open` behind an open CHOICE.

## Record template

`references/templates/13 Health check.md`, its FINDING part (the same record in `12 Whole-film check.md`); `references/templates/01 Choices.md` (CHOICE).

## IDs you will be given

Code numbers the checker's findings. The handout gives the judgement unit a block of finding numbers that follows them (for example FIND-021 onward) and the next free choice number (CHOICE-031 onward). Copy them in order; never reuse a number, even for a finding later accepted.

## Batch and chunk rules

The judgement unit reads the whole strip at once when it is under `film_strip_tokens_per_unit_max` tokens (The Catch at about 300 shots: about 12,000); above that, one unit per act (U-09-JUDGE-A1, U-09-JUDGE-A2 ...), each with the film rules and PLAN, and the last asks one more question: do the acts' ladders join into one climb?

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Would the film's turn pictures tell the story with the sound off?
2. Does no shot feel like a different film?
3. Is every FILM error fixed, and every warning fixed or accepted with a reason that quotes a line or cites a record?
4. Was the judgement unit fresh, and did every question quote its record?
5. Does every finding name its record, rule, evidence and fix?
6. Did each fix redo only the scenes it names?
7. Does each choice put to the user change a creative choice, and have a default?

## The report

Fill it from the project; these are illustrative counts for The Catch (message shapes: `references/formats/07 Report and message formats.md`):

```
Done: step 10 of 12, the film pass.
Example: nothing before scene 13 is as close as its shot of Iona on "You.", and the
  crossing in scenes 26 and 27 is played wide and still, as the film's rules say.
Made: 12 Whole-film check: 7 problems found and fixed in 4 scenes (the details are
  in the file), 1 for you to choose.
Needs you: one choice, with an answer ready.
  1. Scene 24 already spends the film's strongest colour and contrast on the
     fire. A push-in on "She deletes the way home." would add a third. Keep the
     camera still there?                                                      [yes]
  I'm carrying on with the health check; your answer changes only scene 24.
Next: the health check, with three scenes for you to read.
```

## Checkpoint

None that waits. Only findings that change a creative choice reach the user, as choices with defaults, in this step's report; the work carries on. A choice not answered by the finished check is shown there again, among its things to check, and then defaulted.

## How to redo

"Run the film pass again": `stage.py check --film` runs again and a fresh judgement unit answers the questions again. Fixed findings stay fixed, accepted ones keep their reasons, and only new problems get new numbers. A later change to one scene ("Redo scene 10") marks the film pass stale; it runs again before the health check.

## If you cannot run code

Every line reference is a quote anchor: each finding's `evidence` quotes the record and the story line exactly, at least `quote_anchor_words_min` words, never a line number.

1. There is no film strip. The film pass runs in check chats, one per group of scenes, after the last group's own check. Each chat attaches that group's scene files (in two messages when they pass the app's file limit), `02 Whole-film summary`, `10 Film rules`, `05 Checks in words`, `11 Steps 09-11 and 16 - film pass, check, book, resume`, and the last saved `12 Whole-film check` (for the first group, the last `13 Health check` instead), and the user types "Run the film pass on these scenes."
2. In that chat, quote this step's one-line task, then answer step 9's questions of `references/formats/06 Checks in words.md` part 2 for the group, and check by hand the two errors you can count: each character camera rule (nothing closer than its `limit_before` before its `closest` story point; nothing on its `never` list) and each saved choice's uses against `max_uses` and `allowed_in`.
3. Save the findings as `12 Whole-film check.md`, the whole file each time: the earlier groups' findings carried forward, then this group's, numbered on from the highest FIND number in the attached files, the checks-in-words table, the END line. Choices go in `01 Choices - film pass.md`.
4. The other film checks (the ladder, rhymes, colour, sameness, counts) need code: they run at the real check on a code surface, where `adopt` is followed by `check --film`. Say so once in the report.
5. Report, then the resume line; after the last group it names step 10's first health-check chat:

```
Save as: 12 Whole-film check.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach the files of scenes 11 to 13,
02 Whole-film summary, 10 Film rules, 05 Checks in words, 12 Whole-film check and
11 Steps 09-11 and 16 - film pass, check, book, resume; type: Run the film pass
on these scenes.
```

**One-line task, again:** Judge the whole film as one structure before any picture is made: run the film checks, answer the film pass questions in a fresh unit, and turn every "no" into a finding with its fix.
