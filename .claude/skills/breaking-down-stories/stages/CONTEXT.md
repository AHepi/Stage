# The steps, in order

One folder per step; the folder's `CONTEXT.md` is the step file, with the step's inputs, procedure and outputs. Read the step file of the unit you are doing every time (on a code surface, `stage.py handout` puts its excerpt in the handout), never this list instead. The step a message names for the user is counted from 1: step 7 here is "step 8 of 12".

Example: scene 10 of The Catch is designed at step 7 (its beats, floor-plan moves, camera setups and the one-line shot list in `11 Scenes/Scene 10 - Saye's kitchen.md`) and its shots are written at step 8 into the same file.

Where a step reads "the story", it reads it in the lines its handout cites, never whole. Reads names the record types a step's handout carries (the field guide, `references/formats/03 Field guide.md`, says which file holds each); Writes names the files it writes, in the project folder (`My breakdowns/<title>/`). The step's own instructions say what goes in each.

## Run once, in order, at the start

| Step | Folder | Reads | Writes |
|---|---|---|---|
| 0 | `00 Start/` | no records: it starts the project | `00 Start here.md`; `01 Choices.md`; `Original/`; `22 Rights and credits.md` (the story's own RIGHTS record) |
| 1 | `01 Read the story/` | PROJECT, CHOICE | `03 Story - numbered.md`; `04 Scene list.md`; `05 Story plan.md` (CHAPTER stubs); `07 Characters and voices.md` (CHARACTER stubs); `14 Time and cost.md` (the first estimate); `For machines - do not edit/speeches.json`; `00 Start here.md` (PROJECT title, source kind and format, format, scene_id_digits); `01 Choices.md` |
| 2 | `02 Story plan/` | SCENE, CHAPTER, CHOICE, PROJECT | `05 Story plan.md`; `04 Scene list.md` (plan fields; prose: the step-outline SCENE records); `06 World and style.md` (prose: RULE records of kind device); `01 Choices.md` |
| 3 | `03 World and style/` | PLAN, SCENE, CHOICE, PROJECT | `06 World and style.md`; `01 Choices.md`; `00 Start here.md` (PROJECT prompt_words) |
| 4 | `04 Characters, places and things/` | PLAN, SCENE, STYLE, WORLD, RULE, CHARACTER | `07 Characters and voices.md`; `08 Places and things.md`; `01 Choices.md` |
| 5 | `05 Continuity/` | SCENE, CHARACTER, PROP, LOCATION, RULE, STATE | `09 Continuity.md`; `01 Choices.md`; `02 Whole-film summary.md` (after checkpoint B: code; the AI in chat) |
| 6 | `06 Film rules/` | PLAN, SEQUENCE, SCENE, STYLE, WORLD, RULE, CHARACTER, VOICE, LOCATION, PROP, MOTIF, STATE, CHOICE | `10 Film rules.md`; `01 Choices.md` |

## Run sequence by sequence

| Step | Folder | Reads | Writes |
|---|---|---|---|
| 7 | `07 Scene design and shot list/` | SCENE, SEQUENCE, PLAN, CAMSYS, CAMRULE, RESERVE, LENS, VISUAL, LOOK, SOUNDPLAN, LADDER, CHARACTER, VOICE, STATE, FACT, PLANT, MOTIF, LOCATION, PROP, TEXT, SPEECH, SHOT or SHOTLIST (the previous scene's last shot) | `11 Scenes/Scene NN - <place>.md`; `01 Choices.md` (the scene's small choices) |
| 8 | `08 Shot details/` | everything step 7 reads, SCENE (design), PART, BEAT, MOVE, SETUP, SHOTLIST | `11 Scenes/Scene NN - <place>.md` (code surfaces); `11 Scenes/Scene NN - <place> - shots NNN-NNN.md` (chat batch files); `19 Grey previews/Grey preview jobs.md` (PREVIS stubs, by code) |

## Run once, after the last sequence

| Step | Folder | Reads | Writes |
|---|---|---|---|
| 9 | `09 Film pass/` | film strip (derived), CAMSYS, CAMRULE, RESERVE, LENS, LOOK, VISUAL, SOUNDPLAN, LADDER, PLAN, MOTIF, SCENE | `12 Whole-film check.md`; `01 Choices.md` |
| 10 | `10 Check and estimate/` | all records, adapters, prices | `13 Health check.md`; `14 Time and cost.md`; `For machines - do not edit/breakdown.json`; `15 The breakdown/` (first version) |
| 11 | `11 Book and exports/` | all records | `15 The breakdown/The breakdown.html`; `15 The breakdown/The breakdown.md`; `16 Spreadsheets/Shot list.csv`; `16 Spreadsheets/People, places and things.csv`; `17 Captions and audio description/`; `For machines - do not edit/timeline.otio`; `For machines - do not edit/timeline.edl`; `For machines - do not edit/breakdown.json`; `For machines - do not edit/breakdown.schema.json` |

## Add-ons, only when the user asks, after step 11

| Step | Folder | The user types | Reads | Writes |
|---|---|---|---|---|
| 12 | `12 Add-on - storyboards/` | "Make storyboards" | SHOT, SHOTLIST, STYLE, CHARACTER, STATE, LOOK, LOCATION, PROP | `18 Storyboard/`; `06 World and style.md` (STYLE style_picture); `01 Choices.md` |
| 13 | `13 Add-on - previs/` | "Make grey previews" (Claude Code with Blender only) | LOCATION, SCENE (start), MOVE, SETUP, SHOT, CHARACTER, PROJECT | `19 Grey previews/`; `For machines - do not edit/previs plans/`; `00 Start here.md` (PROJECT previs_colours) |
| 14 | `14 Add-on - generation packs/` | "Get it ready for AI video" | all shot-related records, adapters, prices | `20 Prompts for AI video/` (on the MiniMax H3 route in ComfyUI, the clip book in its folder MiniMax H3 in ComfyUI/); `22 Rights and credits.md`; `00 Start here.md` (PROJECT spend_cap_usd, intended_use, licensed_data_only, video_route); `01 Choices.md`; `07 Characters and voices.md` (CHARACTER skin_light, VOICE source) |
| 15 | `15 Add-on - edit and finishing/` | "Plan the edit" | SHOT, SOUNDPLAN, TAKE, RIGHTS | `21 Edit and finishing/`; `22 Rights and credits.md` |

## Whenever work stops or goes wrong

| Step | Folder | When | Reads | Writes |
|---|---|---|---|---|
| 16 | `16 Resume and recovery/` | "Continue my breakdown.", a cut-off reply, a full chat, a changed early choice | PROJECT, 00 Start here.md, manifest | none, or the missing records re-sent; `00 Start here.md` (rewritten at a stop point, in a chat without code); `02 Whole-film summary.md` (rewritten at a stop point, in a chat without code) |

The same list, with every unit, card part, check and checkpoint, is `_config/schema/steps.json`; code reads it to build each handout. The Folder, Reads and Writes cells above are made from it by `stage.py build-kit` (each step's `reads` and `files_written`), so never change them here: change a step's inputs or outputs in `_config/schema/steps.json` and in its step file's Outputs together, run `stage.py build-kit`, then the tests.
