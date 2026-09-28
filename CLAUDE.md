# Stage: a story-breakdown kit

This folder is a story-breakdown kit. Use the skill `breaking-down-stories` (in `.claude/skills/breaking-down-stories/`; read its `SKILL.md` first). Stories are in `My stories/`, projects in `My breakdowns/`. Run tools with `python .claude/skills/breaking-down-stories/tools/stage.py <command>`; you run them, the user never types a command.

When the user types "Break down my story.", take the story from `My stories/` (if there are several, ask which one) and start at step 0 of the skill. "Continue my breakdown." picks up the project in `My breakdowns/`.

Rules for this folder:

- **Privacy.** No personal information in any file, prompt or web request: no email addresses, no account details, no names of real people other than cited authors. Never put the user's email address in a request header. Never copy a user's story whole out of its project, commit it, or paste it into a web request. `My stories/` and `My breakdowns/` stay out of git (`.gitignore`).
- **Never edit files under "For machines - do not edit".** Code writes them. Change the numbered record files only through the skill's loop (`handout`, write to the inbox, `apply`, `check`), and never edit what code makes (the book, spreadsheets, prompts, `breakdown.json`): change the records and build again.
- **Plain words for the user.** Every message follows the skill's report format: one example from the story first, no abbreviations or codes, one next step.
- **Grey previews** need Blender on this computer; they are offered only here, in Claude Code.

For maintainers: the skill folder is the one source. After changing it, run `python .claude/skills/breaking-down-stories/tools/stage.py build-kit` to remake `07 Chat kit/`, `08 Skill for Claude apps.zip`, `AGENTS.md`, the field guide and `09 Example - The Catch, scene 10/`, and run the tests in `tests/`.
