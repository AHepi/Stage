# Commands

Every `stage.py` command, what it does, and what to do instead when you cannot run code. This table was the section "Tools: one command" of `SKILL.md`, which keeps the rule for running them: run every tool as `python <this skill's folder>/tools/stage.py <command>`, from any folder (in Claude Code: `python .claude/skills/breaking-down-stories/tools/stage.py <command>`; on ChatGPT, `breaking-down-stories/` at the top of the unpacked `07 Tools.zip`). You run the commands; the user never types one.

| Command | What it does | If you cannot run code |
|---|---|---|
| `new "<story file>" [--title] [--depth]` | Makes the project folder, `00`, `01`, `Original/` | Write `00` and `01` from the templates; the user makes the folder |
| `selftest --prepare` / `--score` | The step 0 self-test; `--score` records `surface`, `code_execution`, `batch_size` | Quote the story's first and last line; batch size 12 |
| `read` | Numbers the story: `03`, `04`, stubs, `speeches.json`, odd-lines report, first-estimate counts | Write the scene list with quote anchors |
| `adopt "<folder>" "<story file>"` | Makes a folder saved in a chat app checkable, then runs `check --all` | None: it is the bridge from chat to code |
| `status` | Done, stale, waiting, next; changes no record | Answer from `00 Start here` |
| `next [--checkpoint-passed]` | The next unit and its handout; passes groups that do not wait | The step file and the resume line in `00 Start here` |
| `handout <unit>` | Builds a unit's handout | Name the files the user should attach |
| `apply <inbox file>` | Accepts your records into the numbered files and the log | The user saves the copy box under its "Save as" name |
| `check [--unit <unit>] [--step N] [--scene SCnn] [--film] [--all] [--story <path>]` | Runs the checks; writes `13 Health check` | Checks in words in each reply; judgement in a check chat; the real check after `adopt` |
| `build` | Derived fields, `breakdown.json`, the plain parts | Done on the next code surface |
| `impact <ID>` | What depends on a record | Search the files for the ID |
| `questions --sample [--seed N]` | Yes/no review questions from the records | The rubric's questions in words, in a check chat |
| `estimate [--version v0\|v1]` | The first estimate (also run by code at step 2), or the estimate from the shots | A rough estimate, labelled rough |
| `compile [--scene <range>] [--model <list>] [--force-model <id>] [--storyboard] [--lint-only]` | Prompts and packs, routing and lint | A few prompts by hand from card 21, linted in words |
| `graphics` | Text graphics for text in picture | SVG text in a copy box |
| `previs [--shot] [--render]` | Previs plans; with `--render`, grey renders and blocking checks | Not offered |
| `export <shotlist\|book\|timeline\|captions\|json\|voices\|spotting\|finishing\|all>` | The book, spreadsheets, captions, timeline, machine files | Write `15 The breakdown/The breakdown.md` as a contents page |
| `pack` / `unpack <zip>` | Saves or opens the project as one save ZIP | The user saves files one by one |
| `lines <ID> [--more]` | Every story line that mentions an element | Search the attached story |
| `lib <code> <reference>` | One library section or rule with its errata (`B1 R14`), or its digest entry, labelled | The cards only |
| `refresh-models --propose` / `--apply` | Dated model facts, applied once the user approves price changes | Not available |
| `import-json <file>` | Not in this version (planned) | None |
| `build-kit` | Maintainers: the chat kit, the skill ZIP, `AGENTS.md`, the field guide | None |
| `replay [--story <path>]` | Maintainers: re-checks the gold examples | None |
