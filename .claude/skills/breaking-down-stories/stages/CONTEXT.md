# The steps, in order

One folder per step; the folder's `CONTEXT.md` is the step file, with the step's inputs, procedure and outputs. Read the step file of the unit you are doing every time (on a code surface, `stage.py handout` puts its excerpt in the handout), never this list instead. The step a message names for the user is counted from 1: step 7 here is "step 8 of 12".

Example: scene 10 of The Catch is designed at step 7 (its beats, floor-plan moves, camera setups and the one-line shot list in `11 Scenes/Scene 10 - Saye's kitchen.md`) and its shots are written at step 8 into the same file.

Where a step reads "the story", it reads it in the lines its handout cites, never whole. The project files named below are in the project folder (`My breakdowns/<title>/`); the step's own instructions name every record type it writes.

## Run once, in order, at the start

| Step | Folder | Reads | Writes |
|---|---|---|---|
| 0 | `00 Start/` | the story file and the app you are in | `00 Start here`, `01 Choices`, `Original/`, the story's rights record in `22 Rights and credits`; the self-test |
| 1 | `01 Read the story/` | the story as given, and step 0's choices | `03 Story - numbered`, `04 Scene list`, chapter and character stubs, the speeches, the first estimate in `14 Time and cost` |
| 2 | `02 Story plan/` | the numbered story, a unit at a time, and the scene list | `05 Story plan`; plan fields on each scene in `04 Scene list` |
| 3 | `03 World and style/` | the plan, the scene records, the numbered story searched for place and time | `06 World and style` |
| 4 | `04 Characters, places and things/` | the lines that name each character, place and thing; the plan, world and style | `07 Characters and voices`, `08 Places and things` |
| 5 | `05 Continuity/` | the scenes in slices, with the states entering them; characters, places and things | `09 Continuity`; then, after the big choices, code writes `02 Whole-film summary` |
| 6 | `06 Film rules/` | the plan, world, style, characters, places, things, motifs, states and the answered choices | `10 Film rules`, locked once written |

## Run sequence by sequence

| Step | Folder | Reads | Writes |
|---|---|---|---|
| 7 | `07 Scene design and shot list/` | the handout: the scene's lines and plan fields, the film rules it touches, the people, places and states in it, `02 Whole-film summary`, the previous scene's last shot | the scene file in `11 Scenes/`: its design, parts, beats, floor-plan moves, setups and one-line shot list |
| 8 | `08 Shot details/` | everything step 7 had, the scene design just written, the approved shot list items of the batch | the shot and cut records of the batch, in the same scene file (in a chat, a batch file beside it) |

## Run once, after the last sequence

| Step | Folder | Reads | Writes |
|---|---|---|---|
| 9 | `09 Film pass/` | the film strip (one line per shot, made by code), the film rules, the plan, the motifs, the scene records | `12 Whole-film check` |
| 10 | `10 Check and estimate/` | all records, the checker's report, `12 Whole-film check`, the model facts and prices | `13 Health check`, `14 Time and cost`, a first version of `15 The breakdown` |
| 11 | `11 Book and exports/` | all records, built by `stage.py build`; `13 Health check`, `14 Time and cost` | `15 The breakdown`, `16 Spreadsheets`, `17 Captions and audio description`, the timeline and machine files |

## Add-ons, only when the user asks, after step 11

| Step | Folder | The user types | Reads | Writes |
|---|---|---|---|---|
| 12 | `12 Add-on - storyboards/` | "Make storyboards" | shots, style, fixed descriptions and states, looks, places and things | `18 Storyboard/` |
| 13 | `13 Add-on - previs/` | "Make grey previews" (Claude Code with Blender only) | set plans, scene starts, floor-plan moves, setups, shots, character heights | `19 Grey previews/` |
| 14 | `14 Add-on - generation packs/` | "Get it ready for AI video" | every shot-related record, voices and states, rights, the model facts and prices | `20 Prompts for AI video/` (on the MiniMax H3 route in ComfyUI, the clip book in `20 Prompts for AI video/MiniMax H3 in ComfyUI/`), `22 Rights and credits` |
| 15 | `15 Add-on - edit and finishing/` | "Plan the edit" | shots, the sound plan, takes, rights | `21 Edit and finishing/`, `22 Rights and credits` |

## Whenever work stops or goes wrong

| Step | Folder | When | Reads | Writes |
|---|---|---|---|---|
| 16 | `16 Resume and recovery/` | "Continue my breakdown.", a cut-off reply, a full chat, a changed early choice | `00 Start here`, the project record, the machine folder's record of units done | nothing new, or the missing records sent again |

The same list, with every unit, card part, check and checkpoint, is `_config/schema/steps.json`; code reads it to build each handout. Change a step's inputs or outputs there and in its step file together, then run the tests.
