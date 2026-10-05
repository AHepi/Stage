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
3. **Odd lines** (unit U-01-ODDLINES). Read only the odd-lines report ("Lines to look at" in `04 Scene list`) and confirm or correct each line; write only corrections, as records in `For machines - do not edit/inbox/U-01-ODDLINES.md`, then run `stage.py apply`. A secondary heading such as `(ON THE TABLET)` is a presentation note (SCENE `presentation: on_screen`; its `host` is written at step 4 by the unit that writes the in-story cameras). A heading that may hold two scenes, or a title card inside the film that `read` did not place, is a CHOICE with `asked: no`, defaulting to the script's own count (card 01, "Length"). Confirm or refuse each alias merge; an unmatched cue stays odd. Prose: write each CHAPTER's `first_line` and `last_line`, quoted exactly. A scanned PDF is refused with the fix: open it in Google Docs, save it as text. A thin source (a treatment) switches on authoring mode: later steps may write scenes, each `origin: invented`, approved by the user (card 02).
4. **Choices.** `read` has written CHOICE-004, `format`, and the length choice (CHOICE-005 in The Catch), whose `sets` lines write `PROJECT.runtime_target_s` and `PROJECT.scope`. Never write them again.
5. **Check.** Run `stage.py check --step 1`; fix only the lines it prints, at most `repair_rounds_max` rounds.
6. **Checkpoint A** (below). Pass the answer on in an inbox file: `### CHOICE CHOICE-005` with `- answer: a` (or `- answer: defaults`); for a target, `- answer: b` and `### SETVALUE CHOICE-005-B` with `- target: PROJECT` and `- runtime_target_s: 1200`. Run `stage.py apply`; the scene IDs are then locked.

## Record template

`templates/04 Scene list.md` (SCENE), `templates/05 Story plan.md` (CHAPTER), `templates/07 Characters and voices.md` (CHARACTER), `templates/01 Choices.md` (CHOICE).

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

For a screenplay, checkpoint A's message, with the first estimate as code computed it, a range (D13 R4). The Catch (`reference/07`):

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
6. Each file goes in one copy box with "Save as:" above it: plain part, divider, records, a `---` line, the checks-in-words table (`reference/06` part 1), the END line; a second reply for the same file is saved as `04 Scene list - scenes 16-30.md` (merged by ID, G10). Print "Checked in words: 14 of 14 passed" (or only the failures).
7. Report as above, with the estimate marked rough, then the resume line:

```
Save as: 04 Scene list.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 01 Choices and
its scene list file, 04 Scene list, 08 Steps 00-02 - start, reading, plan and your story;
type: Continue my breakdown. Next is planning the whole story.
```

**One-line task, again:** Turn the story into numbered lines, fix the scene or chapter IDs that everything hangs on, and show the user the scene list with its first estimate.
