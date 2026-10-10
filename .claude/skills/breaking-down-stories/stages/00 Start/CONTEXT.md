# Step 0. Start

This is step 0 of the pipeline; the user counts it as step 1 of 12, "starting". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Make the project, test what this app can do, ask the one rights question, and show the user one finished shot from their own story.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Make the project, test the app, settle rights, and show the user one finished shot from their own story before any question (principle 7: example first, one question, a default).

## When it runs

Once, first, when the user says "Break down my story." (or means it) and no project exists for this story; "Start again" runs it again beside the old project.

## Inputs

The story file (in `My stories/` in Claude Code and Cowork; attached in chat apps) and the app you are running in.

## Outputs

| File | Records |
|---|---|
| `00 Start here.md` | PROJECT, written by code here (in chat, by you): `title`, `depth`, `training_off`, `rights`, `surface`, `code_execution`, `batch_size`, and code's housekeeping fields |
| `01 Choices.md` | CHOICE-001 rights (`asked: yes`); CHOICE-002 depth (`asked: no`, default standard); CHOICE-003 privacy setting (`asked: no`, default `not_confirmed`, answered when the user says the setting is off) |
| `22 Rights and credits.md` | RIGHTS RT-001, the story's own rights record (`subject: source`, `clearance`, `holder` by role, never a name) |
| `Original/` | the story exactly as given, and its fingerprint (code surfaces only) |

## Card parts to open

At every depth: card 24, part "The rights question".

## Procedure

1. **Hidden self-test**, never shown to the user: how much one reply can safely hold (D1 §2.4, §5.3).
   - First try to run Python. If you can, and you find this skill's `tools/stage.py` (on ChatGPT, in `breaking-down-stories/` of the unpacked `07 Tools.zip`), you are on a code surface: go on below. Otherwise follow "If you cannot run code".
   - Run `stage.py new "<story file>"`; it makes the project folder and its first files, with CHOICE-001 to CHOICE-003.
   - Run `stage.py selftest --prepare`. It checks the story and the ZIP maker and writes the handout `U-00-SELFTEST.md`: test shot IDs in a scene the story does not use (`selftest_scene`), rules and a SHOT template.
   - Unit U-00-SELFTEST: follow that handout. Write `selftest_records` full SHOT records and the END line, in one reply, into `For machines - do not edit/inbox/U-00-SELFTEST.md`, every record in full (G11), with every field the template marks required; one with nothing to hold is `none` (G7).
   - Run `stage.py selftest --score --surface <this app>` (`claude_code`, `claude_cowork`, `claude_web` or `chatgpt`). It sets PROJECT `batch_size` (the larger value if every record and the END line pass, else the default), `code_execution` and `surface`, prints the error count, writes every error to a file and deletes the test records; never type these three fields yourself. A retry uses the same issued IDs.
2. **Find one strong turn** (unit U-00-START). Read only enough of the story to find one moment where a scene turns, and write one finished shot line from it (scene and shot, size, what the camera does, what we see, one quoted line, the seconds, a "Why" that quotes the story), every quoted word the story's own (G12). It is an example for the welcome, not a record.
3. **Welcome the user** with the message in "The report": the example, how the work goes, the depth stated (not asked), and one question, rights.
4. **Pass on the answers.** On a code surface write into `For machines - do not edit/inbox/U-00-START.md`:
   - `### CHOICE CHOICE-001` with only `- answer: a` (or `- answer: defaults`). `new` already wrote its 16 `sets` lines (for each option, `PROJECT.rights` and RT-001's `subject`, `clearance` and `holder`). Leave them out: a field you send replaces all its stored lines, so sending some would delete the rest;
   - `### RIGHTS RT-001 The story` with `- evidence: the user said: It's mine`.

   Run `stage.py apply`. It sets the choice's status and date, writes what the chosen `sets` lines name, and makes `22 Rights and credits.md`. Never write `status`, `date` or `locked` yourself on a code surface. CHOICE-002 and CHOICE-003 are small choices, defaulted unless the user says "quick", "detailed" or that the privacy setting is off; pass those on the same way.
5. **Not mine, no permission.** Option d sets `rights: study_only`: private study only, every export marked "Private study, not for publication", no public-release packs (GEN-14; card 24). Say: "Then I'll plan it for your private study only. Every file will say 'Private study, not for publication', and I won't make video prompts for public release."
6. **Check.** Run `stage.py check --step 0` (it asks only for fields filled by step 0; FORM-05). Fix only the lines it prints, at most `repair_rounds_max` rounds (C5 R13), then ask one plain question.

## Record template

`templates/00 Start here.md` (PROJECT), `templates/01 Choices.md` (CHOICE), `templates/22 Rights and credits.md` (RIGHTS). The self-test's SHOT template is in its handout.

## IDs you will be given

- Self-test shots: from its handout (`SC99-SH010` to `SC99-SH200`).
- `CHOICE-001`, `CHOICE-002`, `CHOICE-003` and `RT-001`.
- The project ID, 3 to 8 capitals from the title (`CATCH`, `LONG`), made by `new`. Copy every ID; never make one up.

## Batch and chunk rules

None: the self-test and the start unit are one reply each; nothing reads the whole story.

## Self-check

Answer each question yes or no from what you just wrote; each "no" is a fix before you report.

1. Does PROJECT hold `rights`, `depth`, `training_off`, `surface`, `code_execution` and `batch_size`, and are CHOICE-001 to CHOICE-003 answered or defaulted?
2. Does `check --step 0` exit 0?
3. Is every word inside double quotes in the example shot the story's own?
4. Is the example a turn, and does its "Why" quote the story instead of naming a feeling?
5. Did the welcome ask exactly one question, and state the depth instead of asking it?
6. Is everything the user reads free of codes, IDs and abbreviations (WORDS-04)?

## The report

The welcome, filled from the user's own story (The Catch here; `reference/07 Report and message formats.md`):

```
Hello. I'll turn The Catch into a scene-by-scene plan for making it as a film,
including with AI picture and video tools.

Here is one finished moment from your story, so you can see what you'll get:
  Scene 10, shot 150. Close-up, camera still. Iona chews the leaf. She stops,
  frowns, chews once more, slowly. "Not mint." We stay on her face while Saye
  answers off screen. About 15 seconds.
  Why: "Her face changes." The scene turns inside her mouth, so we don't cut away.

How it works: I do the work. You'll be asked to choose about four times
(the scene list, the big choices, the first group of shots, and the finished
check), each with an answer ready if you just say "defaults". You can stop any
time and carry on another day: everything is saved in files with plain names.

I'll make a complete shot plan (standard). Say "quick" for one line per shot,
or "detailed" for extra detail on every shot.

One question first:
1. Is this story yours, or do you have permission to adapt it?   [It's mine]
```

After the answer, the four-part report:

```
Done: step 1 of 12, starting.
Example: your title page says "An original short screenplay" and you told me it
  is yours, so the plan and everything made from it can be shared.
Made: 00 Start here, 01 Choices, 22 Rights and credits.
Needs you: nothing.
Next: I'll read the whole story, number its lines and show you the scene list.
```

## Checkpoint

The rights question, worded as in the welcome. It blocks: nothing else runs until it is answered or defaulted.

- Options: a, it's mine (`mine`); b, I have permission (`permission`); c, public domain (`public_domain`); d, not mine and no permission: private study only (`study_only`).
- Default: a, "It's mine". "defaults" accepts it.
- If the user is unsure, say in one line what each answer allows (card 24); never give legal advice beyond the card.

## How to redo

- "Start again": a new project ("The Catch 2"); the old one is kept.
- "Quick", "Standard" or "Detailed" at any time answers CHOICE-002 again; nothing is thrown away.
- A new rights answer ("I got permission") answers CHOICE-001 again; run `stage.py impact RT-001` and tell the user in one line what it changes (exports and packs).

## If you cannot run code

No code here (Gemini, or any app without it), so there is no numbered story: from now on every line reference is a quote anchor, a short exact quotation of the story (G5).

1. **Self-test in words.** In your first reply quote the story's first line and its last line exactly ("= THE CATCH" and "= THE END"). If you cannot, the app did not read the whole file: ask the user to paste the missing part (`reference/07`, "When something goes wrong"). Then `batch_size: 12`, `code_execution: no`, `surface: gemini` (or `other`).
2. Find the turn, write the example shot and send the welcome exactly as above.
3. After the answer, write three files, each in its own copy box with "Save as:" above it: `00 Start here.md`, `01 Choices.md`, `22 Rights and credits.md`. Each box holds the plain part (for `00 Start here`, the template's six sections, with "Checked by the checker: never"), the divider line, the records, then the checks-in-words table and the END line.
4. Write CHOICE-001 to CHOICE-003 whole: options (rights as in "Checkpoint"; depth a standard, b quick, c detailed; privacy a not confirmed, b off), one `sets` line per option, `answer`, `status`, `date`. Write every field the templates mark "in a chat without code you write it" (PROJECT `title` from the first title-page line, `source_fingerprint: none`, `checker_last_run: never`), every record's `status` and `locked`, and what the choices set: PROJECT `rights`, `depth`, `training_off`; RT-001 `subject`, `clearance`, `holder`.
5. Run the checks of `reference/06 Checks in words.md` part 1 on each file; the table goes after a `---` line below the last record, before the END line, and rows about beats and shots say "PASS (no beats or shots in this file)". Print one line: "Checked in words: 14 of 14 passed" (or only the failures).
6. Tell the user once: make a folder "The Catch - breakdown" and save each box in it under its "Save as" name.
7. End with the four-part report, then:

```
Save as: 00 Start here.md, 01 Choices.md, 22 Rights and credits.md   (save only boxes that end with the END line)
To continue later: new chat in this project; attach 00 Start here, 01 Choices,
08 Steps 00-02 - start, reading, plan and your story; type: Continue my breakdown.
Next is reading the story.
```

**One-line task, again:** Make the project, test what this app can do, ask the one rights question, and show the user one finished shot from their own story.
