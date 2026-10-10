# Where to go

Stage turns a story into a scene-by-scene plan for a film. One finished moment, from The Catch, scene 10: shot 150, a close-up with the camera still. Iona chews the leaf, frowns, chews once more: "Not mint." This page says where to go for what you want to do, for a person and for the AI.

## What do you want to do?

| You want to | Go to | Then type |
|---|---|---|
| Break down your story | Put the story in `My stories`. Which app to use: `01 Start here/01 Read me first.md` | Break down my story. |
| Carry on with a breakdown | Your project in `My breakdowns` (on the Claude website or ChatGPT, attach your newest save file; in Gemini, the files the last reply named) | Continue my breakdown. |
| Check a breakdown made in a chat app | `01 Start here/02 Using Claude.md`, "Checking a folder saved from another app" | Check my breakdown. |
| Make the video with MiniMax H3 in ComfyUI | Finish and check the breakdown first; then ask for the prompts and answer "b" to "Which way will you make the video?". The clip book lands in your project's `20 Prompts for AI video/MiniMax H3 in ComfyUI/` | Get it ready for AI video. |
| Use the Claude website or Claude desktop | `01 Start here/02 Using Claude.md`, with `03 Kits to upload/Skill for Claude apps.zip` | Break down my story. |
| Use ChatGPT or Gemini | `01 Start here/03 Using ChatGPT.md` or `04 Using Gemini or another chat app.md`, with the folder `03 Kits to upload/Chat kit` | Break down my story. |
| See a finished scene first | `02 Example - The Catch, scene 10/15 The breakdown/The breakdown.html` | nothing |
| Read how Stage was built and tested | `04 Project history/Stage - project story.md`, then `04 Project history/Project notes/` | nothing |
| Change the kit itself (for maintainers) | `.claude/skills/breaking-down-stories/SKILL.md`; each folder inside has its own `CONTEXT.md`. Afterwards run `stage.py build-kit` and the tests in `tests/` | nothing |

## How the folders are arranged

The kit is laid out the way a paper on organising AI work as folders suggests (Van Clief and McDermott, "Interpretable Context Methodology", 2026): numbered folders in the order you use them, and five kinds of file, each answering one question.

1. **Where am I?** `CLAUDE.md` (read by Claude Code) and `AGENTS.md` (read by other coding apps): what this folder is and its rules.
2. **Where do I go?** This page; inside the kit, `.claude/skills/breaking-down-stories/SKILL.md`, which says which step handles what the user types.
3. **What do I do in this step?** One folder per step, with its own instructions: `.claude/skills/breaking-down-stories/stages/08 Shot details/CONTEXT.md`, and so on, from step 0 to step 16. The list of steps, with what each reads and writes, is the `CONTEXT.md` beside them.
4. **What rules apply?** Files that stay the same for every story: the craft cards, record format, word list, templates, worked example and research in `references/`, and the settings the checker reads in `_config/` (both inside the kit folder). Changing these changes every breakdown made after.
5. **What am I working with?** Files that are new for every story: your story in `My stories`, and your project in `My breakdowns/<title>/`. Its numbered files are what each step made, in order, and every one opens in a text editor.

Two rules follow from this. Fix the cause, not the result: when a breakdown comes out wrong, the AI changes the records it was made from and builds again, and never edits the book, the spreadsheets, the prompts or anything in a project's `For machines - do not edit`. And your stories and breakdowns stay on your computer: `My stories` and `My breakdowns` are never uploaded with the kit.
