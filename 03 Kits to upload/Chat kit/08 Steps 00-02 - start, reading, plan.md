# 08 Steps 00-02 - start, reading, plan

Part of the Stage chat kit: a step-group file, attached to the chat that runs one of these steps (not knowledge). It joins the step files 00 Start, 01 Read the story, 02 Story plan, each whole. Read the one for this unit every time, quote its one-line task back before any work, and follow its section "If you cannot run code" when this chat has no code. 01 House rules (in the knowledge) says where every other skill file is.

---

From the skill file `stages/00 Start/CONTEXT.md`:

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

`references/templates/00 Start here.md` (PROJECT), `references/templates/01 Choices.md` (CHOICE), `references/templates/22 Rights and credits.md` (RIGHTS). The self-test's SHOT template is in its handout.

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

The welcome, filled from the user's own story (The Catch here; `references/formats/07 Report and message formats.md`):

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

1. **Self-test in words.** In your first reply quote the story's first line and its last line exactly ("= THE CATCH" and "= THE END"). If you cannot, the app did not read the whole file: ask the user to paste the missing part (`references/formats/07`, "When something goes wrong"). Then `batch_size: 12`, `code_execution: no`, `surface: gemini` (or `other`).
2. Find the turn, write the example shot and send the welcome exactly as above.
3. After the answer, write three files, each in its own copy box with "Save as:" above it: `00 Start here.md`, `01 Choices.md`, `22 Rights and credits.md`. Each box holds the plain part (for `00 Start here`, the template's six sections, with "Checked by the checker: never"), the divider line, the records, then the checks-in-words table and the END line.
4. Write CHOICE-001 to CHOICE-003 whole: options (rights as in "Checkpoint"; depth a standard, b quick, c detailed; privacy a not confirmed, b off), one `sets` line per option, `answer`, `status`, `date`. Write every field the templates mark "in a chat without code you write it" (PROJECT `title` from the first title-page line, `source_fingerprint: none`, `checker_last_run: never`), every record's `status` and `locked`, and what the choices set: PROJECT `rights`, `depth`, `training_off`; RT-001 `subject`, `clearance`, `holder`.
5. Run the checks of `references/formats/06 Checks in words.md` part 1 on each file; the table goes after a `---` line below the last record, before the END line, and rows about beats and shots say "PASS (no beats or shots in this file)". Print one line: "Checked in words: 14 of 14 passed" (or only the failures).
6. Tell the user once: make a folder "The Catch - breakdown" and save each box in it under its "Save as" name.
7. End with the four-part report, then:

```
Save as: 00 Start here.md, 01 Choices.md, 22 Rights and credits.md   (save only boxes that end with the END line)
To continue later: new chat in this project; attach 00 Start here, 01 Choices,
08 Steps 00-02 - start, reading, plan and your story; type: Continue my breakdown.
Next is reading the story.
```

**One-line task, again:** Make the project, test what this app can do, ask the one rights question, and show the user one finished shot from their own story.

---

From the skill file `stages/01 Read the story/CONTEXT.md`:

# Step 1. Read the story

This is step 1 of the pipeline; the user counts it as step 2 of 12, "reading the story". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Turn the story into numbered lines, fix the scene or chapter IDs that everything hangs on, and show the user the scene list with its first estimate.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Turn any story file into numbered text and fix the scene (or chapter) IDs every later record cites; once the user has seen the scene list, they never change.

## When it runs

Once, after step 0: code reads the story and you confirm its odd lines, or, in chat, you write the scene list.

## Inputs

- The story, in `Original/` (code) or attached (chat): The Catch's own form (`## ` headings, `@NAME` cues, `> ` transitions, `= ` title lines), Fountain, Final Draft, Word, EPUB, plain text, prose or a PDF with a text layer; other forms by card 02.
- PROJECT and the choices of step 0.

## Outputs

- `03 Story - numbered.md`: every line numbered (prose: one paragraph per line).
- `04 Scene list.md`: a screenplay's SCENE list fields (`heading` to `origin` in the template), with the odd-lines report above the divider.
- `05 Story plan.md`: prose, CHAPTER stubs. `07 Characters and voices.md`: CHARACTER stubs, the ID and `names` only.
- `For machines - do not edit/speeches.json`: a screenplay's speeches, in cue order within each scene.
- `14 Time and cost.md`: the first estimate. `01 Choices.md`: a CHOICE for anything odd, CHOICE-004 `format`, the length choice.
- `00 Start here.md`: PROJECT `title`, `source_kind`, `source_format`, `language`, `format`, `scene_id_digits`.

## Card parts to open

- At every depth: card 01, part "Length".
- Prose, a treatment or a play: also card 02, part "Intake".

## Procedure

1. **Read.** Run `stage.py read`. It numbers the lines, splits scenes or chapters, extracts speeches, transitions and title lines, proposes alias merges (`DR SAYE` is `SAYE`), makes the first estimate and the choices of item 4, and writes the odd-lines report.
2. **The placement rules** code applies, for you to confirm: title-page `= ` lines before the first heading are not shots, and the first gives `PROJECT.title` (The Catch, lines 1 to 6); a `> ` line before it is the first scene's `transition_in` (`> FADE IN:`, line 8); a `= ` line inside the film is a card shot (`= THE CATCH`, line 488: `SC10-SH990`); `= ` lines after the last transition are the last scene's end card (`= THE END`, line 1852: `SC30-SH990`). Prose: a chapter heading starts with a roman numeral or a number and a full stop, or "Chapter"; a first heading that is not one, followed by one that is, is the title (The Long Places, line 1; propose the clean title as a small choice); lines before the first chapter are front matter, listed as odd (line 3).
3. **Odd lines** (unit U-01-ODDLINES). Read only the odd-lines report ("Lines to look at" in `04 Scene list`) and confirm or correct each line; write only corrections, as records in `For machines - do not edit/inbox/U-01-ODDLINES.md` (with none, only its END line, `0 records`), then run `stage.py apply`. A secondary heading such as `(ON THE TABLET)` is a presentation note (SCENE `presentation: on_screen`; its `host` is written at step 4 by the unit that writes the in-story cameras). A heading that may hold two scenes, or a title card inside the film that `read` did not place, is a CHOICE with `asked: no`, defaulting to the script's own count (card 01, "Length"). Confirm or refuse each alias merge; an unmatched cue stays odd. Prose: write each CHAPTER's `first_line` and `last_line`, quoted exactly. A scanned PDF is refused with the fix: open it in Google Docs, save it as text. A thin source (a treatment) switches on authoring mode: later steps may write scenes, each `origin: invented`, approved by the user (card 02).
4. **Choices.** `read` has written CHOICE-004, `format`, and the length choice (CHOICE-005 in The Catch), whose `sets` lines write `PROJECT.runtime_target_s` and `PROJECT.scope`. Never write them again.
5. **Check.** Run `stage.py check --step 1`; fix only the lines it prints, at most `repair_rounds_max` rounds.
6. **Checkpoint A** (below). Pass the answer on in an inbox file: `### CHOICE CHOICE-005` with `- answer: a` (or `- answer: defaults`); for a target, `- answer: b` and `### SETVALUE CHOICE-005-B` with `- target: PROJECT` and `- runtime_target_s: 1200`. Run `stage.py apply`; the scene IDs are then locked.

## Record template

`references/templates/04 Scene list.md` (SCENE), `references/templates/05 Story plan.md` (CHAPTER), `references/templates/07 Characters and voices.md` (CHARACTER), `references/templates/01 Choices.md` (CHOICE).

## IDs you will be given

Code gives every ID (in chat, you number them the same way); copy them, never make one up: scenes in heading order, `SC01` to `SC30` (3 digits, `SC001`, above `scene_ids_three_digits_above` scenes); chapters `CP01` to `CP14`; speeches in cue order within each scene, `SC10-D01` to `SC10-D16` (3 digits above `speech_ids_three_digits_above`); characters from the cue name (`CH-SAYE`); the next free CHOICE numbers.

## Batch and chunk rules

Code reads any length; you read only the odd-lines report. In chat a 30-scene list takes one or two replies; prose, one chapter per reply.

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Does the scene count equal the story's headings (ID-05)?
2. Is every cue resolved to a character, or listed as odd?
3. Is every `= ` and `> ` line placed, and every odd line explained?
4. Is the first and last line of every scene or chapter quoted (in chat, each scene's `lines` pair; prose, `first_line` and `last_line`)?
5. Are the length choice and CHOICE-004 answered or defaulted?
6. Does `check --step 1` exit 0?

## The report

For a screenplay, checkpoint A's message, with the first estimate as code computed it, a range (D13 R4). The Catch (`references/formats/07`):

```
Done: step 2 of 12, reading the story.
Example: scene 10 is Saye's kitchen, lines 397 to 489. Saye speaks 10 times, Iona 4,
  Jude and Eli once each. It ends with a cut to black and the title card "THE CATCH",
  which becomes its own shot.
Made: 03 Story - numbered, 04 Scene list, 14 Time and cost (a first estimate).
  I found 30 scenes, one for each heading in your script.
  Small choices I made (1): I treat it as a short film (under 40 minutes).

The scene list. One question. Reply "defaults", or answer it.
1. Length: as written it runs about 35 minutes (32 to 38; the page count suggests
   up to 44). Keep everything, or give me a target, for example 20 minutes?   [keep everything]
Next: I'll plan the whole story: its turns, its climax and its groups of scenes.
```

Prose, with no question (The Long Places):

```
Done: step 2 of 12, reading the story.
Example: chapter I, "The Lamps Are Old", opens with a letter that begins
  "To the one who keeps the lamps after me:".
Made: 03 Story - numbered, 05 Story plan (one entry for each chapter).
  I found 14 chapters, 49,152 words; I'll plan the whole book next.
Needs you: nothing.
Next: a short summary of each chapter, then three ways the book could become a film.
```

## Checkpoint

Checkpoint A, "the scene list" to the user; it blocks for a screenplay. The scene count is stated as a fact, never asked; anything genuinely odd goes under "Small choices I made". One question, length, with the first estimate as computed; default keep everything (`runtime_target_s: as_written`, `scope: all`). A target ("20 minutes") sets `runtime_target_s`, and step 2 runs its compression unit. "Only do scenes 2, 13 and 26 for now" is a CHOICE setting `scope` (SKILL.md), written after the scene list's answer in the same inbox, since the later choice wins. Prose: the message only states chapters and words; length and scope are chosen at step 2.

## How to redo

Before the lock, `stage.py read` again. After it, scenes are never renumbered: an inserted scene takes a letter (`SC06A`), a removed one becomes `status: omitted`. A revised script is matched to the old IDs by heading and text; changed scenes go stale (`stage.py impact`).

## If you cannot run code

There is no numbered story, so every line reference is a quote anchor: the exact words of one line, at least `quote_anchor_words_min` words, found once in its scope (G5); `stage.py adopt` turns them into numbers later. If the user made `03 Story - numbered.md` on the Claude website and attached it, line numbers are allowed.

1. Write the scene list yourself, in one or two replies for 30 scenes: each SCENE's fields marked "in a chat without code you write it", with `lines` as an anchor pair of its first and last line (`lines: "INT. SAYE'S HOUSE - KITCHEN - BEFORE DAWN" to "CUT TO BLACK."`) and `speaking` as cues counted per character. The CHARACTER stubs (ID and `names`) go in `07 Characters and voices.md`.
2. Number speeches by hand in cue order within each scene (scene 10's first cue is `SC10-D01`); you use them from step 7, and no speech file is saved.
3. Prose: one chapter per reply, a CHAPTER with `title`, `lines` as an anchor pair, `words` (your count), and `first_line` and `last_line` quoted exactly (a first line that recurs, as the letters do, is matched within its chapter), saved as `05 Story plan - chapter I.md`; step 2 saves it again, whole, with the digest.
4. The first estimate is a rough range labelled "rough", from the page check of D13 R22 or the word count, never a total you added up (D13 R4).
5. Write CHOICE-004 (`format`, `asked: no`, `status: defaulted`, `short` under `short_runtime_max_s` by the rough estimate) and, for a screenplay, the length choice (`asked: yes`, `status: open`; option a sets `runtime_target_s: as_written` and `scope: all`) in `01 Choices - scene list.md`. After the answer, save that file again with `answer`, `status` and `date`, and `00 Start here.md` again, whole.
6. Each file goes in one copy box with "Save as:" above it: plain part, divider, records, a `---` line, the checks-in-words table (`references/formats/06` part 1), the END line; a second reply for the same file is saved as `04 Scene list - scenes 16-30.md` (merged by ID, G10). Print "Checked in words: 14 of 14 passed" (or only the failures).
7. Report as above, with the estimate marked rough, then the resume line:

```
Save as: 04 Scene list.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 01 Choices and
its scene list file, 04 Scene list, 08 Steps 00-02 - start, reading, plan and your story;
type: Continue my breakdown. Next is planning the whole story.
```

**One-line task, again:** Turn the story into numbered lines, fix the scene or chapter IDs that everything hangs on, and show the user the scene list with its first estimate.

---

From the skill file `stages/02 Story plan/CONTEXT.md`:

# Step 2. Story plan

This is step 2 of the pipeline; the user counts it as step 3 of 12, "planning the whole story". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Plan the whole film before any scene is designed: what each scene changes, the groups of scenes, one climax and its crisis, the peaks, what is planted and paid off, and who knows what.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Write the film-level plan every later choice rests on; for prose also which chapters and strands survive, the format, the scope, and the step outline (the book's scenes in screen order).

## When it runs

Once, after the scene or chapter list, never reading the whole text at once.

## Inputs

- The numbered story, one unit's scenes or chapter at a time; SCENE or CHAPTER records from step 1; the length answer.

## Outputs

- `05 Story plan.md`: PLAN, SEQUENCE, PLANT, and FACT (at Standard only for facts in suspense, mystery or dramatic irony, about `fact_records_typical` in a film; at Detailed every fact). Prose adds CHAPTER digests, STRAND and CARDINAL.
- `04 Scene list.md`: the plan fields on each SCENE (procedure, and `sequence`). Prose: the SCENE records of the step outline.
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
   - PLANT records with `planted_at` and `paid_off_at` as story points.
   - FACT records for what the audience and each character know, from when, with `element` naming what would give the fact away in frame: its ID if it has one, else a story point where it shows, never a stand-in; step 4 re-points it to the new ID.
   - If two climax readings are defensible, write both into one CHOICE for the big choices (The Catch's default: climax `SC26..SC27`, crisis `SC24 "She deletes the way home."`, K12; D16 §8.6).
3. **Compression unit** (U-02-COMPRESS), only for a shorter target: CARDINAL records by the deletion test, then the compression plan in D2 R10's order (trim, merge, fold, then cut a strand) as SCENE `keep` and `merged_into` and PLAN `op` items; never rewrite a line of the story.

**Prose.**

1. **Digest units**, one per chapter (U-02-CP01 on): a CHAPTER `digest` of at most `chapter_digest_words_max` words (events, people, places, time markers, the lines that matter by number), `people`, `places`, `time_markers`, `pov`, and `candidate` scenes with A3's five-test scores and decisions (A3 §7.9).
2. **Whole-book unit** (U-02-BOOK) reads only the digests: STRAND and CARDINAL records, RULE records of kind `device`, and two or three independent macro plans as PLAN `plan_option` items with runtime, scene and shot budgets, cost and review hours from `stage.py estimate --version v0` (D2 R1).
3. **Checkpoint P** (below).
4. **Outline units** (U-02-OUTLINE-P1 on, `outline_chapters_per_unit` chapters each) write the chosen plan's SCENE records in screen order with the IDs the handout gives: `heading`, `int_ext`, `place_text`, `time_text`, and `from_lines`, or `origin: invented`; code works out `lines` from `from_lines`. Then PLAN, SEQUENCE, PLANT and FACT for the kept scenes.

**Both.** When the film unit is applied, code runs the first estimate itself: it fills each scene's `target_duration_s` and PLAN's `runtime_estimate`, `scene_budget` and `shot_budget`, and copies `genre`, `tone_home` and `tone_range` to PROJECT. Never type these. The targets come from word counts, not design, so TIME-03 later only warns. After each unit run `stage.py check --unit <unit>`, and after the last `stage.py check --step 2`; fix only the lines printed, at most `repair_rounds_max` rounds.

## Record template

`references/templates/05 Story plan.md` (PLAN, SEQUENCE, PLANT, FACT, CHAPTER, STRAND, CARDINAL), `references/templates/04 Scene list.md` (SCENE plan fields), `references/templates/06 World and style.md` (RULE), `references/templates/01 Choices.md`.

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

Prose: checkpoint P, "how the book becomes a film"; it blocks. Default for The Long Places: plan A, with chapter I first as a trial, which sets `PROJECT.scope` to its scenes (5 of 48); the device rules are small choices. Checks, the film pass, estimates and exports then cover only the scenes in scope ("Scope: 5 of 48 scenes"); "go on to chapter II" widens it. The message (`references/formats/07`; your own counts):

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
4. Each copy box: "Save as:" above it; plain part, divider, records, a `---` line, the checks-in-words table (`references/formats/06` part 1), the END line. Print "Checked in words: 14 of 14 passed" (or only the failures).
5. Report, then the resume line:

```
Save as: 05 Story plan.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 01 Choices and
its files, 04 Scene list and its plan files, 05 Story plan, 09 Steps 03-06 - world, people,
continuity, film rules and your story; type: Continue my breakdown.
Next is world and style.
```

**One-line task, again:** Plan the whole film before any scene is designed: what each scene changes, the groups of scenes, one climax and its crisis, the peaks, what is planted and paid off, and who knows what.
