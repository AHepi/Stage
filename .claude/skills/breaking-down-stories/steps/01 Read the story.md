# Step 1. Read the story

This is step 1 of the pipeline; the user counts it as step 2 of 12, "reading the story". Read this file at the start of every unit of this step, never from memory.

**One-line task:** Turn the story into numbered lines, fix the scene or chapter IDs that everything hangs on, and show the user the scene list with its first estimate.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Turn any story file into numbered text and fix the scene (or chapter) IDs that every later record cites. Once the user has seen the scene list, scene IDs never change.

## When it runs

Once, after step 0. On a code surface code reads the story and you read only its odd-lines report; in chat you write the scene list yourself.

## Inputs

- The story, in `Original/` (code) or attached (chat): The Catch's own form (`## ` headings, `@NAME` cues, `> ` transitions, `= ` title lines), Fountain, Final Draft, Word, EPUB, plain text or prose, or a PDF with a text layer. Theatre plays, treatments, comic and game scripts follow card 02.
- PROJECT, and CHOICE-001 to CHOICE-003 from step 0.

## Outputs

| File | What it holds |
|---|---|
| `03 Story - numbered.md` | every line numbered (prose: one paragraph per line) |
| `04 Scene list.md` | a screenplay's SCENE list fields: `heading`, `int_ext`, `place_text`, `time_text`, `lines`, `characters`, `speaking`, `transition_in`, `transition_out`, `presentation`, `host`, `origin`; the odd-lines report above the divider |
| `05 Story plan.md` | prose: CHAPTER stubs |
| `07 Characters and voices.md` | CHARACTER stubs: the ID and `names` only |
| `For machines - do not edit/speeches.json` | a screenplay's speeches, numbered in cue order within each scene |
| `14 Time and cost.md` | the first estimate (code) |
| `01 Choices.md` | a CHOICE for anything odd; CHOICE-004 `format`; the length choice |
| `00 Start here.md` | PROJECT `title`, `source_kind`, `source_format`, `language`, `format`, `scene_id_digits` |

## Card parts to open

- At every depth: card 01, part "Length".
- When the source is not a screenplay (prose, a treatment, a play): also card 02, part "Intake".

## Procedure

1. **Read.** Run `stage.py read`. It numbers every line, keeps the original and its fingerprint, splits scenes or chapters, extracts speeches (speaker and path), transitions, title lines, capitalised words and each scene's light and darkness words, proposes alias merges (`DR SAYE` is `SAYE`), makes the first estimate and writes the odd-lines report.
2. **Know the placement rules** code applies, so you can confirm them (The Catch's lines):
   - `= ` lines before the first heading are title-page lines, not shots; the first becomes `PROJECT.title` (lines 1 to 6).
   - A `> ` line before the first heading is the first scene's `transition_in` (`> FADE IN:`, line 8).
   - A `= ` line inside the film becomes a card shot (`= THE CATCH`, line 488, becomes `SC10-SH990`).
   - `= ` lines after the last scene's final transition become an end card of the last scene (`= THE END`, line 1852, becomes `SC30-SH990`).
   - Prose: a chapter heading starts with a roman numeral or a number and a full stop, or the word "Chapter". A first heading that is not a chapter heading, followed by one that is, is the title (The Long Places, line 1; propose the clean title "The Long Places" as a small choice). Lines before the first chapter are front matter, listed as odd (line 3's note).
3. **Odd lines** (unit U-01-ODDLINES). Read only the odd-lines report and confirm or correct each line:
   - A secondary heading such as `(ON THE TABLET)` is a presentation note: set `presentation` (`on_screen`) and `host` on that SCENE.
   - A heading that may hold two scenes, or a title card inside the film, becomes a CHOICE with `asked: no`, defaulting to the script's own count (card 01, "Length").
   - Confirm or refuse each alias merge; a cue that matches no character stays listed as odd.
   - Set `presentation` and `origin` on every SCENE.
   - A scanned PDF is refused with the one-step fix: open it in Google Docs and save it as text.
   - A thin source (a treatment) switches on authoring mode: later steps may write scenes, each `origin: invented`, approved by the user (card 02).
4. **Choices.** Write CHOICE-004 for `format` (`asked: no`; `short` when the first estimate is under `short_runtime_max_s`, otherwise `feature`) and the length choice (`asked: yes`, `checkpoint: a`), whose `sets` lines write `PROJECT.runtime_target_s` and, for a screenplay, `PROJECT.scope` as `all`.
5. **Check.** Run `stage.py check --step 1`; fix only the lines it prints, at most `repair_rounds_max` rounds.
6. **Checkpoint A** (below). Pass the answer on by writing the length choice's heading (`### CHOICE CHOICE-005` in The Catch) with `- answer: a` (or `- answer: defaults`) into the unit's inbox file and running `stage.py apply`. After it, the scene IDs are locked.

## Record template

`templates/04 Scene list.md` (SCENE), `templates/05 Story plan.md` (CHAPTER), `templates/07 Characters and voices.md` (CHARACTER), `templates/01 Choices.md` (CHOICE).

## IDs you will be given

Code gives every ID; copy them, never make one up.

- Scenes in heading order, `SC01` to `SC30`; 3 digits (`SC001`) above `scene_ids_three_digits_above` scenes.
- Chapters `CP01` to `CP14` (The Long Places).
- Speeches in cue order within each scene: `SC10-D01` ("Kitchen.") to `SC10-D16`; 3 digits above `speech_ids_three_digits_above`.
- Characters from the cue name (`CH-SAYE`); the next free CHOICE numbers.

## Batch and chunk rules

Code reads any length. You read only the odd-lines report, in one unit. In chat a 30-scene list takes one or two replies, and prose is read one chapter per reply.

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Does the scene count equal the story's headings (ID-05)?
2. Is every cue resolved to a character, or listed as odd?
3. Is every `= ` and `> ` line placed by the placement rules?
4. Is every line the odd-lines report lists explained?
5. Did I quote the first and last line of every scene or chapter (in chat, each scene's `lines` anchor pair; for prose, each chapter's `first_line` and `last_line`)?
6. Are the length choice and CHOICE-004 answered or defaulted?
7. Does `check --step 1` exit 0?

## The report

For a screenplay the report is checkpoint A's message, with the first estimate printed as code computed it, as a range (D13 R4). The Catch (`reference/07`):

```
Done: step 2 of 12, reading the story.
Example: scene 10 is Saye's kitchen, lines 397 to 489. Saye speaks 10 times, Iona 4,
  Jude and Eli once each. It ends with a cut to black and the title card "THE CATCH",
  which becomes its own shot.
Made: 03 Story - numbered, 04 Scene list, 14 Time and cost (a first estimate).
  I found 30 scenes, one for each heading in your script.
  Small choices I made (1): I treat it as a short film (under 40 minutes), which
  sets how often the film may use its saved choices.

The scene list. One question. Reply "defaults", or answer it.
1. Length: as written it runs about 35 minutes (32 to 38; the page count suggests
   up to 44). Keep everything, or give me a target, for example 20 minutes?   [keep everything]
Next: I'll plan the whole story: its turns, its climax and its groups of scenes.
```

For prose there is no question (The Long Places):

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

Checkpoint A, shown to the user as "the scene list". It blocks for a screenplay.

- The scene count is stated as a fact, never asked; anything genuinely odd goes under "Small choices I made".
- One question, length, with the first estimate as computed. Default: keep everything (`runtime_target_s: as_written`, `scope: all`). A target ("20 minutes") sets `runtime_target_s`, and step 2 runs its compression unit.
- Prose: the message only states chapters and words; length and scope are chosen at step 2.

## How to redo

- Before the lock: run `stage.py read` again.
- After it scenes are never renumbered: an inserted scene takes a letter (`SC06A`); a removed one becomes `status: omitted`.
- A revised script is matched to the old IDs by heading and text; changed scenes go stale (`stage.py impact` lists what cites them).

## If you cannot run code

There is no numbered story, so every line reference is a quote anchor: the exact words of one line, at least `quote_anchor_words_min` words, found once in its scope (G5). `stage.py adopt` turns them into numbers later, and the checker verifies them.

1. Write the scene list yourself, in one or two replies for 30 scenes: for each SCENE the fields the template marks "in a chat without code you write it", with `lines` as an anchor pair of its first and last line (`lines: "INT. SAYE'S HOUSE - KITCHEN - BEFORE DAWN" to "CUT TO BLACK."`) and `speaking` as cues counted per character.
2. Number speeches by hand in cue order within each scene (scene 10's first cue is `SC10-D01`); you use these numbers from step 7. No speech file is saved in chat.
3. Write the CHARACTER stubs (ID and `names`) in `07 Characters and voices.md`.
4. Prose: one chapter per reply, a CHAPTER record each with `title`, `lines` as an anchor pair, `words` (your count; `adopt` replaces it), and `first_line` and `last_line` quoted exactly. A first line that recurs in the book (the letters open alike) is matched within its chapter only.
5. The first estimate is a rough range labelled "rough", from the page check of D13 R22 or the word count, never a total you added up (D13 R4). CHOICE-004 follows from it. The real first estimate is made when the folder is next checked on a code surface.
6. If the user made `03 Story - numbered.md` on the Claude website and attached it, line numbers are allowed.
7. Each file goes in one copy box with "Save as:" above it: plain part, divider, records, a `---` line, the checks-in-words table (`reference/06 Checks in words.md` part 1), the END line. A second reply for the same file is saved as `04 Scene list - scenes 16-30.md`; `adopt` merges them by ID (G10). Print "Checked in words: 14 of 14 passed" (or only the failures).
8. Report as above, with the estimate marked rough, then the resume line:

```
Save as: 04 Scene list.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 01 Choices,
04 Scene list, 08 Steps 00-02 - start, reading, plan and your story;
type: Continue my breakdown. Next is planning the whole story.
```

**One-line task, again:** Turn the story into numbered lines, fix the scene or chapter IDs that everything hangs on, and show the user the scene list with its first estimate.
