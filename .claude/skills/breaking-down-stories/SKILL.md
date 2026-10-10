---
name: breaking-down-stories
description: Breaks down screenplays and prose (novels, stories, treatments, plays) into scene-by-scene shot plans for making a film, including with AI picture and video tools. It numbers the story, plans the whole film, designs characters, places, continuity and film rules, then writes each scene's beats and a checked shot list in which every shot gives its reason; on request it adds storyboards, grey 3D previews, prompts for AI video models and an edit plan. It works in Claude Code, Claude desktop, the Claude website, ChatGPT and Gemini, running its Python checker where code runs and checking in words where it cannot. Use it when someone wants to break down, adapt, shot-list or storyboard a story or script for the screen, or types "Break down my story.", "Continue my breakdown." or "Check my breakdown."
---

# Breaking down stories

What this skill makes, in one finished moment from The Catch, scene 10, as the user reads it:

> Shot 150. Close-up, camera still. Iona chews the leaf, stops, frowns, chews once more. "Not mint." We stay on her while Saye answers off screen. About 15 seconds. Why: "Her face changes." The scene turns inside her mouth, so we do not cut away.

Behind it is one SHOT record (`SC10-SH150`, in `references/formats/01 Record format.md`) whose `purpose`, `because` and `why` name this story. These are the house rules; each step file says what to do in its step.

## The ten principles, as instructions

1. **Keep one source of truth that people can read.** Write the breakdown only as record text in the numbered project files: the plain part (headings with `#` and `##` only, "At a glance", one plain line per shot or item, "Why it's shot this way"), the divider line `Below this line: details for the AI and the checker. You never need to read them.`, the records, the END line. Code makes JSON, the book, spreadsheets, prompts and previs plans from the records: rebuild, never edit them.
2. **Write intent; code does the arithmetic; the user decides.** Every field has one writer in `_config/schema/schema.json`. Write only `ai` fields, plus, in a chat without code, those marked `chat_writer: ai`. Never type a derived value: a time floor, clip length, resolution, price, label, prompt or image side. Copy issued IDs; never make one up (C5 R23). A `user` field is set only by a choice answered or defaulted; `apply` refuses it from you (FORM-10). With a set plan, `at` and `faces` are intent that code checks (GEOM-06). The END line's count is the one count you type.
3. **Cite, never copy.** The story's words live only in `03 Story - numbered` and in speech records. Cite speech IDs and line numbers (quote anchors in a chat without code); a short quotation must match the story word for word (G12). Flag flaws in the story; never fix them. Label every addition `origin: invented`, keep it small, and list it in the scene's `additions`; those that change what the scene means go to the user to keep or cut.
4. **Make every choice name this story.** Every shot has a `purpose` and a `because` linking story records. A value that departs from the baseline carries a `why` that quotes a line, names an object or action, or cites an ID (the fields and their defaults: card 14). Mood-only reasons fail (REASON-04). The baseline (camera still, at the eye height of the person the scene belongs to, the normal lens, room sound) is a strong answer. Saved choices ration the extremes.
5. **Build systems before shots; design from the turn.** The film rules (camera, light, colour, visual structure, sound, saved choices) are written once, at step 6, before any scene. In each scene, write the turn picture as one sentence before any shot. Shots come last.
6. **Plan short, then expand; do one unit per reply.** The one-line shot list fixes shot IDs and the count before any detail. Each reply does one unit and ends with its counted END line, so a cut-off or shortened reply is caught even without code (D1 R4).
7. **Ask little, default everything, say it plainly.** Ask only about what the user wants and what is risky, costly or hard to undo, never about format, syntax or IDs. Every question has a default that "defaults" accepts. End every reply with one next step. Start reports with an example from the user's story. One word for each thing; no abbreviations or codes in what the user reads.
8. **Lock approved work; let change flow downstream only.** Add to a locked record; never change it silently (C5 R18). A change produces an impact list (`stage.py impact <ID>`), and only what it touches is redone. IDs never shift and are never reused; a cut record keeps its ID with `status: omitted`.
9. **Check by code, then by question, then by eye.** Run the checker after every unit. Judgement is checked with yes/no questions built from the records (C5 R11), answered by a fresh unit (in chat apps, a check chat), never by the unit that wrote them. There is no "review and improve" pass (C5 R12). Repairs stop after `repair_rounds_max` rounds (3; C5 R13), then become a choice for the user or a trace to the earliest wrong record (C5 R28). The user reads three scenes.
10. **One kit, every app, no vendor, no date.** The same steps, cards, file names and grammar work in every app; only who runs the code changes (C5 R19). Model facts are dated and refreshed before money is spent (C5 R22). Privacy comes first.

## How to talk to the user

- **End every reply the same way.** **Done** (with progress: "scene 11 of 30, step 9 of 12"), **Example from your story** (one concrete line), **Made** (files), **Needs you** (nothing, or one question with its default in square brackets), then **Next** (one step); in chat apps, then "Save as" and "To continue later". Every message shape is in `references/formats/07 Report and message formats.md`.
- **Use the user's words, never the codes.** "Scene 10", "shot 150", "beat 7", "camera B" (a setup), "floor-plan move 4", "group 3" (a sequence), "choice 21", "saved choice 1", "Iona, state 2", "take 3"; named records by their plain names. Name checkpoints by what they are, never by letter. Count steps from 1: step 7 here is "step 8 of 12". Say "grey previews" for previs, "the first estimate" and "the estimate from the shots". The checker flags retired words and codes (WORDS-02, WORDS-04; `_config/rules/words.json`).
- **Plain words, example first.** Explain a new craft word in one plain sentence the first time and add it to the word list in `00 Start here`.
- **Ask as little as you can.** The user answers only at checkpoints; everything else is a small choice (`asked: no`), listed under "small choices I made". Questions are numbered.
- **On a code surface, pass answers through records.** Write `### CHOICE CHOICE-NNN` with `- answer: <letter>` (or `- answer: defaults`) to an inbox file and apply it; code sets `status`, `date`, the fields the choice `sets`, and the locks; never write those yourself there. Write a small choice whole, with `- answer: defaults`, so it is defaulted at once. In a chat without code you write the answer, `status`, `date` and what it sets.
- **Stop only when you must:** at a blocking checkpoint, after "stop here" or "stop after each group", before any money is spent, and when a repair has failed `repair_rounds_max` times. Otherwise report and carry on.

## The loop

**Every unit, every surface.** A unit is one piece of AI work that fits one reply, named `U-<step>-<scope>[-<batch or part>]` (`U-07-SC10`, `U-08-SC10-B2`). Read the unit's step file every time, never from memory, and quote its one-line task back before you write anything. Steps 0 to 6 run once each, in order. Steps 7 and 8 run sequence by sequence: step 7 designs and lists a sequence's scenes, the user sees that group of shots, step 8 writes their shots in batches, then the next sequence starts. Steps 9 to 11 follow the last sequence. Never read the whole film's records at once; whole-film judgement uses one-line summaries (the event list, chapter digests, the film strip).

**On a code surface** (Claude Code; Claude desktop with a connected folder; the Claude website with this skill; ChatGPT with `07 Tools.zip`):

1. `stage.py next` names the next unit and its handout.
2. `stage.py handout <unit>` writes `For machines - do not edit/handouts/<unit>.md`. Read it whole (in parts if need be): step excerpt, card parts, records, source lines, issued IDs.
3. Quote the one-line task back.
4. Write the records to `For machines - do not edit/inbox/<unit>.md`, ending with the END line.
5. `stage.py apply "<inbox file>"`. Any error refuses the whole inbox and changes no file: fix the lines it names and apply again. A field you send replaces all its stored lines: send every item of a repeated field you change.
6. `stage.py check --unit <unit>` (what the unit wrote and cites); after a step's last unit, `stage.py check --step N` (with `--scene SCnn` at steps 7 and 8).
7. Fix only the problems listed, at most `repair_rounds_max` rounds (a refused apply fixed in place is no round), each round's inbox `<unit ID> - fix <N>.md`; then ask the user one plain question, or trace the earliest wrong record and redo from there.
8. Report, or carry on when nothing waits for the user.

In Claude Code, helper agents may take scenes, one handout each; `apply` takes one inbox at a time. After the app compacts the conversation, run `stage.py status` and reread the step file.

**In a chat without code** (Gemini, or any app whose self-test finds no code):

1. Read the attached step file and quote its one-line task back as your reply's first line.
2. Read the attached files: the story, `00 Start here`, `02 Whole-film summary`, `10 Film rules`, `08 Places and things` when the place has a set plan, the previous scene file.
3. Write the whole file in one copy box: plain part, divider, records, a `---` line, the checks-in-words table, the END line, with "Save as: <file name>" above the box. Write every line reference as a quote anchor (G5), put the words on every `hear` item, and never type the ` = <beat>` ending code adds to story points.
4. Run the checks of `references/formats/06 Checks in words.md` part 1 (in the chat kit, `05 Checks in words`) and print one line: "Checked in words: 14 of 14 passed", or only the failures. Fix a failing box and send it again before the user saves it. A constant named in a step file (`event_unit_scenes`) has its value in the last table of `references/formats/06`.
5. After every checkpoint answer and at every stop, save `00 Start here.md` again, whole: its six plain sections and every PROJECT field filled so far (`format`, `scope`, `genre`, `tone_home`, `frame_shape`, `prompt_words`, `fps`).
6. Report, then "Save as" and "To continue later". A resume line naming more files than the app takes at once (Gemini: 10) says to attach them in two messages.

After each sequence's last batch the resume line names the check chat (`references/formats/06` part 2); then, or at least before acceptance, the user takes the folder to the Claude website for the real check.

**Sizes.** At step 8 a reply holds `batch_size` shots (12, or 18 once the self-test passes). A chat holds one sequence; hand over earlier if the app says it is summarising or usage passes `chat_usage_handover_share` (D1 R5, R6).

**Which surface you are on.** Before anything else, try to run Python. If you can, and you find this skill's `tools/stage.py` (on ChatGPT, in `breaking-down-stories/` of the unpacked `07 Tools.zip`), you are on a code surface; otherwise you are in a chat without code. Step 0's hidden self-test then records `surface`, `code_execution` and `batch_size` (`stages/00 Start/CONTEXT.md`).

## The steps

"User's count" is how messages number the steps. Checkpoints are named as the user sees them; the letter is only for you and the records. A blocking checkpoint waits for an answer; its default is in square brackets. On a code surface a checkpoint passes when its answered choices are applied; one with no choice record (the first group of shots, the finished check) passes, once the user replies, with `stage.py next --checkpoint-passed`. Later groups do not wait: `stage.py next` passes them.

| Step | User's count | Step file | What it makes | Checkpoint |
|---|---|---|---|---|
| 0 Start | step 1 of 12, starting | `stages/00 Start/CONTEXT.md` | the project, `00 Start here`, `01 Choices`, `Original/`; the self-test | rights: "the rights question", blocks [It's mine] |
| 1 Read the story | step 2 of 12, reading the story | `stages/01 Read the story/CONTEXT.md` | `03 Story - numbered`, `04 Scene list`, stubs, speeches, odd-lines report, the first estimate | A: "the scene list", blocks [keep everything]; prose: a statement only |
| 2 Story plan | step 3 of 12, planning the whole story | `stages/02 Story plan/CONTEXT.md` | `05 Story plan`; plan fields on each SCENE | P, prose only: "how the book becomes a film", blocks [plan A; chapter I first] |
| 3 World and style | step 4 of 12, world and style | `stages/03 World and style/CONTEXT.md` | `06 World and style` | none; choices go to B |
| 4 Characters, places and things | step 5 of 12, characters, places and things | `stages/04 Characters, places and things/CONTEXT.md` | `07 Characters and voices`, `08 Places and things` | none; to B |
| 5 Continuity | step 6 of 12, continuity | `stages/05 Continuity/CONTEXT.md` | `09 Continuity` | then B: "the big choices", blocks [accept all]; then code writes `02 Whole-film summary` |
| 6 Film rules | step 7 of 12, the film's rules | `stages/06 Film rules/CONTEXT.md` | `10 Film rules`, locked on writing | none |
| 7 Scene design and shot list | step 8 of 12, designing the scenes and listing their shots | `stages/07 Scene design and shot list/CONTEXT.md` | scene files: design, parts, beats, floor-plan moves, setups, the one-line shot list | C per sequence: "each group of shots" [next]; blocks for the first sequence only, unless "stop after each group" |
| 8 Shot details | step 9 of 12, writing the shots | `stages/08 Shot details/CONTEXT.md` | SHOT and CUT records, batch by batch | none |
| 9 Film pass | step 10 of 12, the film pass | `stages/09 Film pass/CONTEXT.md` | `12 Whole-film check` | only findings that change a creative choice, as choices |
| 10 Check and estimate | step 11 of 12, the health check | `stages/10 Check and estimate/CONTEXT.md` | `13 Health check` with rubric scores, `14 Time and cost`, a first book | acceptance: "the finished check", blocks [no] |
| 11 Book and exports | step 12 of 12, the book and exports | `stages/11 Book and exports/CONTEXT.md` | folders 15 to 17, machine files | none |
| 12 Add-on storyboards | "storyboards" | `stages/12 Add-on - storyboards/CONTEXT.md` | the three-style test, frames, `18 Storyboard` | "which of three styles", blocks [A] |
| 13 Add-on previs | "grey previews" | `stages/13 Add-on - previs/CONTEXT.md` | `19 Grey previews` | D: "the grey previews" [fine] |
| 14 Add-on generation packs | "prompts for AI video" | `stages/14 Add-on - generation packs/CONTEXT.md` | `20 Prompts for AI video` | E: "keeping takes", per take; a spending cap first, never defaulted |
| 15 Add-on edit and finishing | "planning the edit" | `stages/15 Add-on - edit and finishing/CONTEXT.md` | `21 Edit and finishing` | none |
| 16 Resume and recovery | "carrying on" | `stages/16 Resume and recovery/CONTEXT.md` | picks up after a stop or a failure | none |

**Depth** is quick, standard (the default) or detailed (`depth` on PROJECT or one SCENE). It filters fields; quick runs only steps 0 to 7, 9 (code audits), 10 and 11, and its one-line list is the final shot plan.

## What the user may type

Their own words work too.

- "Break down my story.": Step 0: the welcome with one finished shot and the rights question.
- "Continue my breakdown.": Step 16: with code, unpack the newest save ZIP (Claude website, ChatGPT), run `stage.py status`, say one line ("Next: scene 13. Nothing is waiting for you."); without code, read `00 Start here` and the attached files.
- "Where are we?": `stage.py status`, or `00 Start here` without code.
- "Why shot 150?": Its purpose and `why` in plain words, with its line.
- "Change ...": `stage.py impact <ID>`; say what it touches and how long; ask once if costly; redo only that.
- "Go deeper on scene 13": Raise that scene's `depth` and redo its units.
- "Quick", "Standard", "Detailed": Change the project's depth; at quick, say the quick-plan sentence of `references/formats/07` once.
- "Redo step 6", "Redo scene 10": The redo rule in that step's file.
- "Stop here": Finish the unit, save (`pack` on the Claude website and ChatGPT; in chat, rewrite `00 Start here` and `02 Whole-film summary`), give the resume message.
- "Check", "Check again": `stage.py check --all`; without code, name the check chat.
- "Check my breakdown." (a ZIP of a folder saved in a chat app, and the story): Unzip; `stage.py adopt "<folder>" "<story file>"`; `check --all`; `build`; `export all`; hand back the health check, the book and the exports. If the ZIP is refused, the user attaches files 00 to 10 and one group's scene files per check.
- "Check my group of scenes." (a check chat): `references/formats/06 Checks in words.md` part 2. "Run the film pass on these scenes.": step 9's check chat.
- "continue": Re-send from the start of the cut record, or only the missing records, then the END line (step 16).
- "next", "defaults": Carry on after a group; accept every default in the open message.
- "Only do scenes 2, 9 and 16 for now", "go on to chapter II", "Do the rest": A CHOICE setting `scope` (steps 7 and 8 take only those scenes; checks and exports say "Scope: 3 of 30 scenes"); "Do the rest" sets `all`.
- "stop after each group", "Start again": Each group of shots waits; a new project, keeping the old one.
- "Make storyboards", "Make grey previews", "Get it ready for AI video", "Plan the edit": Steps 12 to 15; grey previews only in Claude Code on the user's computer.

## Tools: one command

Run every tool as `python <this skill's folder>/tools/stage.py <command>`, from any folder (in Claude Code: `python .claude/skills/breaking-down-stories/tools/stage.py <command>`; on ChatGPT, `breaking-down-stories/` at the top of the unpacked `07 Tools.zip`). You run the commands; the user never types one. `--project "<path>"` picks one of several projects. Exit 0: done; 1: errors printed, fix only those; 2: could not run, and one plain line says why.

Every command, what it does and what to do instead when you cannot run code: `references/formats/08 Commands.md`.

## Where things are

**This skill's folder** (`.claude/skills/breaking-down-stories/`; the top folder, `breaking-down-stories/`, of both ZIPs):

- `stages/00` to `16`: one folder per step, each holding its step file `CONTEXT.md`, read at the start of every unit (on a code surface, as the handout's excerpt). `stages/CONTEXT.md` lists the steps in order with what each reads and writes.
- `references/` (what you read, the same every run; `references/CONTEXT.md` says which folder holds what):
  - `references/cards/01` to `24`: craft knowledge. Read only the parts the step file names for the depth and the scene's tags, at most `card_tokens_per_unit_max` card tokens a unit.
  - `references/formats/`: `01 Record format` (the grammar G1 to G13), `02 Word list`, `03 Field guide` (every field in words), `04 Rule order`, `05 Quality rubric`, `06 Checks in words`, `07 Report and message formats`, `08 Commands`.
  - `references/templates/` (the empty record files); `references/examples/` (the gold scene 10 and its records).
  - `references/library/`: research files by code (`A2 ...`), digests, `00 Resolved conflicts` (K01 to K31), `01 What the codes mean`, `02 Errata`. Never read it whole: `stage.py lib B1 R14` prints one rule with its errata; without code, the cards are enough.
- `_config/` (the settings the code reads; `_config/CONTEXT.md` says who may change them): `_config/schema/` (`schema.json`: types, fields, values, writers, depths; `steps.json`: units, card parts, checks, checkpoints); `_config/rules/` (`constants.json`, `words.json`, `limits.json`, `tone_defaults.json`); `_config/adapters/` (dated model facts and prices).
- `tools/`: `stage.py` and the code it runs.

**A project folder**: `My breakdowns/<Title>/` in Claude Code and Claude desktop (`new` puts it there, walking up from here or the story to `CLAUDE.md` or `My breakdowns`; never elsewhere in the repository); the sandbox, carried between chats as a save ZIP, on the Claude website and ChatGPT; a folder the user makes, "<Title> - breakdown", in a chat without code. Stories go in `My stories/` or are attached. It holds `00 Start here` (the project's memory and the PROJECT record), `01 Choices`, `02 Whole-film summary` (one line per record of 04 to 09, only the fields step 7 reads, at most `summary_words_max` words; made after the big choices, never edited), `03 Story - numbered`, the whole-film files `04 Scene list` to `10 Film rules`, `11 Scenes/Scene NN - <place>.md` (in chat also batch files, `... - shots 130-200.md`), the checks and exports `12` to `17`, add-ons `18` to `21`, `22 Rights and credits`, `Original/` (the story as given, and its fingerprint) and `For machines - do not edit/`.

## Records

The record grammar and what you most often need (headings and field lines, the END line, no shortening markers, who issues IDs, story points, which rule wins): `references/formats/01 Record format.md`.

## When something goes wrong

Step 16 and `references/formats/07` hold the replies: a cut-off reply or skipped records ("continue" above; D1 §6.2); a full chat (the resume line); a changed early choice (an impact list, one question if costly, a redo of only what it touches); a fact not in the story (fixed, or relabelled `invented`). If a text step refuses violent content, say once that this is pre-production and use production words ("gunshot sound effect"); if refused again, log it and suggest another model or app; never disguise the content (D1 R12, D1 §6.5).

## Privacy

- Before an unpublished story is uploaded, the user turns model training off ("Help improve our AI models" in Claude, "Improve the model for everyone" in ChatGPT, Keep Activity in Gemini; never free Google AI Studio; D1 R9, D1 §8). CHOICE-003 records whether they confirmed it; never assume it.
- Put no personal information in any file, prompt or web request: no email addresses, account details, or names of real people other than cited authors. Never put the user's email address in a request header.
- The story stays in the project (`Original/`, `03 Story - numbered`): never copy it whole elsewhere, commit it to a repository or paste it into a web request (D4 §3.8).
- Turn app memory off or ignore it; the files are the only memory (D1 R10).
- Rights come first. A story that is not the user's, with no permission, continues for private study only: `rights: study_only`, every export marked "Private study, not for publication", no public-release generation batches (card 24).
