# Stage: the build blueprint

Chief architect's blueprint for the story-to-screen breakdown pipeline. It is the single specification that builder agents implement file by file and that test agents then run on *The Catch* and *The Long Places*. Where this blueprint and the three designs disagree, this blueprint wins. Written 27 Sep 2026 from the brief, the three designs, the three judges' verdicts, the 14 research digests, the D1, D2, D3, D4 and D13 research files and the C4 previs kit.

---

## How to read this blueprint

**The base.** Two of three judges chose machine-first as the host and the third chose user-first, but all three asked for the same result: machine-first's engine, user-first's user layer and craft-first's craft layer. This blueprint builds exactly that:

| Layer | Taken from | What it is here |
|---|---|---|
| Engine | machine-first | Line-based record text as the single source of truth; one writer per field; parser-owned speech; IDs issued before the AI writes; units that fit one reply; code derives time floors, sides, mirror routes, eyelines, sizes, clip lengths, labels, prompts and prices; dated model adapters; the tested previs compiler |
| User layer | user-first | Example-first welcome; the four-part report; "00 Start here" as the memory; fixed numbered plain-word files that are themselves the records; one-word recoveries; the word list; decision records with "small choices I made" |
| Craft layer | craft-first | purpose plus because on every shot and the eight reason checks; film rules written before scenes (character camera rules, reserve ledger, lens exceptions, lighting in room terms); turn pictures and the dial written before shots; the film pass; the nine-part card anatomy; the rule order that puts readability second; the user's 10-question review sheet |
| New, from D1 | none of the designs | Plan short, then expand (the one-line shot list fixes IDs and counts before detail); a hidden app self-test; shortening markers; batches of 12 or 18 shots; privacy line in every setup guide; 3-digit scene IDs for long prose |

**Decisions that settle the judges' disagreements** (details in the sections named):

1. Source of truth: machine-first's record grammar with named sub-parts only (never positional), snake_case plain-word field names, tolerant parsing of spaces, hyphens and case (section 5.1). The record files are the user's numbered files. Each opens with a plain part the user reads, then a fixed divider line, then the records for the AI and the checker (section 2.6).
2. Checkpoint B comes after world, cast, places and continuity and before film rules, holds at most 7 items, highlights the 3 hardest to undo, and film rules are then written from its answers without another stop (section 3).
3. Climax default for *The Catch*: SC26-SC27; crisis SC24 ("She deletes the way home.", l.1412) (K12).
4. Held takes (turn shots, one-take scenes and shots marked `held: yes`) are never split into chained clips; over the scene model's maximum they route to Seedance 2.5 or Wan 3.0 (section 8.4).
5. Pause tiers without gaps, as half-open ranges: short [0, 1.0) s, medium [1.0, 2.5) s, long [2.5, 4.0] s; above 4.0 s is a "hold" that needs a saved choice; at most two long pauses per scene (K10).
6. The browser helper page (Pyodide) is **later**. ChatGPT Plus and the Claude website run the checker in their own sandbox. Gemini users run `stage.py adopt` and the checker once on the Claude website's free plan, which turns their hand-saved folder into a checkable project (sections 2.4, 7.4).
7. Tools: one command, `stage.py`, over a small standard-library package, zipped into one file for chat sandboxes (section 7).
8. Checkpoint C blocks for the first sequence only; after that it reports and carries on unless the user says "stop after each group" (section 3, step 7). Steps 7 and 8 run sequence by sequence: design and list a sequence's scenes, pass checkpoint C, expand those scenes' shots, then start the next sequence (section 3).
9. Kill criterion: if the fresh-agent tests show more grammar errors than craft errors, the storage syntax switches to flat JSON under the same schema; checker and exporters do not change (section 14.3).

**Words used in this blueprint.** "Step" is a pipeline stage. "Unit" is one piece of AI work that fits one reply. "Record" is one `###` block in a record file. "Card" is a knowledge card (craft file). "Handout" is the one file the AI reads for a unit on a code surface. "Batch" is one reply's share of a scene's shots. "Checkpoint A, P, B, C, D, E" are internal names for the AI and code; the user sees each by what it is ("the scene list", "the big choices"; section 13.3). The full word list is in section 5.7.

---

## 1. Principles (ten)

1. **One source of truth that people can read.** The breakdown lives in Markdown record files in the numbered project folder, written in a strict line grammar. Each file opens with a plain part in plain words (At a glance, the shots in one line each, why it is shot this way), then one fixed divider line, then the records. The user reads the plain part of the files that are saved and never needs the records below the divider. JSON, the book, spreadsheets, timelines, prompts and previs plans are generated from the records, never edited, and can be deleted and rebuilt.
2. **The AI writes intent; code does the arithmetic; the user decides.** Every field has one primary writer: `story` (copied from the story by code), `ai`, `user` (only through a choice record), `code_state` (stored state code keeps, such as locks and status) or `code_derived` (computed on every build, never stored). The AI never types a derived value: a time floor, a clip length, a resolution, a price, a label, a prompt or an image side. Frame placement (`at`, `faces`) is the AI's where no set plan exists; where one exists code projects it from the marks and setups, and any placement the AI writes is only intent, checked against the projection (GEOM-06). The END line's record count is the one count the AI types, and it is checked. It copies IDs issued to it. In chat without code the AI also writes the `code_state` fields marked `chat_writer: ai`, and code re-owns them later (section 5.2).
3. **Cite, never copy.** The story's words live only in the numbered story and in speech records. Shots cite speech IDs and line numbers (quote anchors in chat without code, turned into line numbers by `adopt`); code shows the exact words; any short quotation in a record is checked word for word against the story. Flaws are flagged, never fixed. Every addition is labelled `invented`, kept small and listed; additions that change what a scene means are shown to the user to keep or cut, and the rest are kept and counted.
4. **Every choice names this story.** Each shot has a purpose and `because` links to the story records that justify it. A choice that departs from the film's baseline carries a `why` that quotes a line, names an object or action, or cites an ID. Mood-only reasons are rejected. The baseline (static, the owner's eye height, a normal lens, room sound) is a strong answer. Extreme choices are rationed by a reserve.
5. **Systems before shots; design from the turn.** Film rules (camera, light, colour, visual structure, sound, reserve) are written once before any scene. In each scene the turn picture is written as a sentence before any shot. Shots are the last thing written.
6. **Plan short, then expand; every reply is one unit.** A one-line shot list fixes the shot IDs and count before any detail is written. Each reply is one unit and ends with a counted END line, so cut-off and silently shortened replies are caught even without code.
7. **Ask little, default everything, say it plainly.** The user is asked only about what they want, and anything risky, costly or hard to undo. Every question has a default that the word "defaults" accepts. Every reply ends with one next step. Reports start with an example from the user's own story. One word for each thing; no abbreviations in anything the user reads.
8. **Approved work is locked; change flows downstream only.** Locked records can be added to but never silently changed. A change produces an impact list, and only what it touches is redone. IDs never shift and are never reused.
9. **Check by code, then by question, then by eye.** The checker catches what can be counted. Judgement is checked with yes/no questions built from the records, answered by a fresh unit (in chat apps, a separate "check chat"), never by the unit that wrote the records. The user reads three sample scenes. There is no "review and improve" step, and repairs stop after three rounds.
10. **One kit, every app, nothing tied to one vendor or one date.** The same steps, cards, file names and grammar work in Claude, ChatGPT and Gemini; only who runs the code changes. Model facts are dated and refreshed before money is spent. Privacy comes first: training off before an unpublished story is uploaded, and no personal information in any file the pipeline writes.

---

## 2. Repository layout

### 2.1 The repository "Stage"

`U` = for the user. `A` = for the AI. `C` = for code. `M` = for maintainers (builders, testers).

```
Stage/
  README.md                                   U   GitHub front page: what Stage is; open "01 Read me first"
  CLAUDE.md                                   A   tells Claude Code this folder is a breakdown kit; points to the skill
  AGENTS.md                                   A   the same for other coding agents (generated by stage.py build-kit)
  00 Project story.md                         M   the maintainers' running project story
  01 Read me first.md                         U   what you get (with an example), pick your app, what each app costs you, the first message
  02 Using Claude.md                          U   Claude desktop with a folder (Cowork), Claude Code, the Claude website
  03 Using ChatGPT.md                         U   ChatGPT Plus Project with the tools file
  04 Using Gemini or another chat app.md      U   chat without code: copy boxes, saving, checking on the Claude website
  05 How to read your breakdown.md            U   what each file is, how to read a scene page, the 10-question review sheet
  06 Word list.md                             U   one plain word for each thing
  07 Chat kit/                                U+A the files for a ChatGPT Project or a Gemini Gem (section 2.5)
  08 Skill for Claude apps.zip                U   the skill, zipped for Customize > Skills on the Claude website and Claude desktop (built by stage.py build-kit)
  09 Example - The Catch, scene 10/           U   a small finished project folder to look at first
  My stories/                                 U   put your story file here (Claude Code, Cowork)
  My breakdowns/                              U   your projects appear here
  .claude/skills/breaking-down-stories/       A+C the skill: the source of everything the kit contains
  tests/                                      M   unit tests, fixtures, gold replay; fixtures/ holds the two story excerpts (section 15, decision 16)
```

### 2.2 The skill folder (the source of everything)

```
.claude/skills/breaking-down-stories/
  SKILL.md
  steps/
    00 Start.md
    01 Read the story.md
    02 Story plan.md
    03 World and style.md
    04 Characters, places and things.md
    05 Continuity.md
    06 Film rules.md
    07 Scene design and shot list.md
    08 Shot details.md
    09 Film pass.md
    10 Check and estimate.md
    11 Book and exports.md
    12 Add-on - storyboards.md
    13 Add-on - previs.md
    14 Add-on - generation packs.md
    15 Add-on - edit and finishing.md
    16 Resume and recovery.md
  cards/
    01 Reading the whole story.md       02 Adapting prose.md
    03 Scenes, values and beats.md      04 Dialogue on screen.md
    05 Characters.md                    06 Voices and performance.md
    07 Places, things and motifs.md     08 World, style and genre.md
    09 Film rules and restraint.md      10 Camera.md
    11 Light and colour.md              12 Staging and composition.md
    13 Cutting, rhythm and sound.md     14 Shot design.md
    15 Action scenes.md                 16 Glass, mirrors and sides.md
    17 Screens, text and in-story cameras.md
    18 Suspense, reveals and the dark.md
    19 Inner life, montage and time.md  20 Creatures, violence and filters.md
    21 Making pictures and video with AI.md
    22 Previs.md                        23 Finishing, captions and delivery.md
    24 Rights, consent and disclosure.md
  reference/
    01 Record format.md                 02 Word list.md
    03 Field guide.md (generated)       04 Rule order.md
    05 Quality rubric.md                06 Checks in words.md
    07 Report and message formats.md
  schema/
    schema.json                         steps.json
  rules/
    constants.json    words.json    limits.json    tone_defaults.json
  adapters/
    video_models.json   image_models.json   audio_models.json   routing.json   phrasebook.json   prices.json
  templates/
    00 Start here.md   01 Choices.md   04 Scene list.md   05 Story plan.md   06 World and style.md
    07 Characters and voices.md   08 Places and things.md   09 Continuity.md   10 Film rules.md
    11 Scene.md   18 Add-on jobs.md
  examples/
    01 The Catch - scene 10.md
    02 The Catch - scene 10 - context.md
    03 The Catch - scene 10 - expected check.txt
    04 The Long Places - chapter 1.md
    05 The Long Places - chapter 1 - context.md
    06 The Long Places - chapter 1 - expected check.txt
  tools/
    stage.py
    stage_tools/  __init__.py  record_format.py  project_files.py  read_story.py  derive_fields.py
                  check_records.py  film_pass.py  make_handout.py  make_views.py  make_exports.py
                  estimate.py  compile_prompts.py  make_text_graphics.py  make_previs_plans.py  build_kit.py
    previs/  previs_from_plan.py  check_blocking.py  render_previs.py
             plans/  plan_cage_fall.json  plan_chest_opens.json  plan_grid_pov.json
                     plan_inversion_reveal.json  plan_push_sill.json
  library/
    00 Resolved conflicts.md   01 What the codes mean.md   02 Errata.md
    A1 ... A4, B1 ... B5, C1 ... C5 research files (renamed "<code> <plain title>.md")
    D1, D2, D3, D4, D13 and later D files (same naming)
    digests/  one "<code> <plain title> - digest.md" per research file
```

### 2.3 What each delivered file must contain

Lengths are targets; "words" means English words.

| File | For | Purpose | Required sections | Length |
|---|---|---|---|---|
| `README.md` | U | Front page | What Stage is (3 sentences); one example shot; "Open 01 Read me first" | 150-250 words |
| `CLAUDE.md` | A | Claude Code entry | "This folder is a story-breakdown kit. Use the skill breaking-down-stories. Stories are in My stories/, projects in My breakdowns/. Run tools with python .claude/skills/breaking-down-stories/tools/stage.py." Privacy rule. Never edit files under "For machines - do not edit" | under 300 words |
| `AGENTS.md` | A | Same for other agents | Generated copy of SKILL.md's body with paths made explicit | generated |
| `00 Project story.md` | M | Maintainers' memory (the user's own convention) | Goal; where things stand; how the pieces fit; word list; numbered log (tried, failed, changed); next step | grows; start 800 words |
| `01 Read me first.md` | U | Start in five minutes | What you get (a finished shot from The Catch as the example); which app to use (table: Claude desktop with a folder = best; Claude website = good; ChatGPT Plus = good; Gemini = works, with more saving by hand; grey previews need Claude Code on your computer); what each app costs you, one line each ("Gemini: you save each file yourself, about 80 for a 40-page script, and you still need a free Claude account to check the work"); a recommendation of the Claude website's free plan with the skill to anyone without Claude desktop or ChatGPT Plus; the first message (the same in every app); how long it takes; privacy line | 700-1,000 words |
| `02 Using Claude.md` | U | Setup and daily use on Claude | Privacy (turn off "Help improve our AI models"); Cowork with a connected folder; Claude Code; Claude website with the skill ZIP (turn on code execution, upload the skill, test "Which skills do you have?"); first message; resuming; saving; what to do when the chat is long; checking a folder saved from another app (one ZIP; the fallback of attaching files 00-10 plus one group's scene files per check, because the website takes at most 20 files per chat) | 900-1,300 words |
| `03 Using ChatGPT.md` | U | ChatGPT Plus | Privacy ("Improve the model for everyone" off); make a Project; paste "00 Paste into instructions.txt"; upload the other chat-kit files including "07 Tools.zip"; choose Thinking; first message; downloads expire, so save at once; resume | 700-1,000 words |
| `04 Using Gemini or another chat app.md` | U | Chat without code | The plan needed (Gemini AI Pro or higher: the Gem's knowledge is about 60,000 words, about 80,000 tokens, more than the 32,000 tokens D1 §3.4 gives the free plan); privacy (Keep Activity off; never free AI Studio); make a Gem with the six knowledge files named in 2.5 (no ZIP); which step file to attach to each chat (the resume line names it); copy boxes and "Save as"; save only boxes that end with the END line; the check on the Claude website's free plan (`adopt`, then `check`; section 7.4); optional: make `03 Story - numbered.md` once on the Claude website at step 1 and attach it to every chat; resume | 800-1,100 words |
| `05 How to read your breakdown.md` | U | Reading and judging | What each numbered file is; the plain part at the top of each file and the divider line ("Below this line: details for the AI and the checker. You never need to read them."); a scene page explained on The Catch SC10; "Shots are numbered in tens so that a shot added later fits between them (shot 155)"; the 10-question review sheet (section 11.5); how to ask for a change; the things you can type any time, including "Make storyboards", "Make grey previews", "Get it ready for AI video" and "Plan the edit" | 1,000-1,400 words |
| `06 Word list.md` | U | Plain meanings | Section 5.7's table in plain words, with an example each; "previs" explained once, as the word the AI's files use for grey previews | 1,200-1,600 words |
| `07 Chat kit/` | U+A | The kit for chat apps | Exactly the 13 files in section 2.5 | see 2.5 |
| `08 Skill for Claude apps.zip` | U | Upload | The skill folder with SKILL.md at the top of the folder inside the ZIP (library limited to digests and D files to keep it small) | generated |
| `09 Example - The Catch, scene 10/` | U | Show before telling | A project folder holding only files 00, 01, 04 (SC10 only), 07, 08, 09, 10 and 11 Scenes/Scene 10, plus the generated book page for SC10 | generated from the gold example (committed only if decision 16 allows the SC10 excerpt) |
| `SKILL.md` | A | House rules and the loop | Front matter (`name: breaking-down-stories`; `description` under 1,024 characters, third person, saying it breaks down screenplays and prose into scene-by-scene shot plans for AI filmmaking); the ten principles as instructions; how to talk to the user (report format, one next step, plain words); the loop (next, handout, quote the unit's one-line task back, write, apply, check, fix up to 3 rounds, report); the step table (name, file, what it makes, checkpoint, the step's number as the user counts it, from 1); commands the user may type; where things are; the run command, one sentence: `python <this skill's folder>/tools/stage.py <command>`; privacy rule; "if you cannot run code" twin for every command | under 4,500 words and 500 lines |
| `steps/NN *.md` | A | One step each | Purpose; when it runs; inputs; outputs (exact files and record types); card parts to open by depth and tag; numbered procedure; the record template name; IDs you will be given; batch and chunk rules; self-check questions (yes/no); the exact report to give; checkpoint wording with defaults; how to redo; "if you cannot run code" steps (the chat twin, which says that every line reference is a quote anchor); the one-line task, first and repeated at the end | 1,200-1,800 words each |
| `cards/NN *.md` | A | Craft knowledge | Section 6 anatomy | section 6 lengths |
| `reference/01 Record format.md` | A | The grammar | Section 5.1 in full with 3 examples and the 10 most common mistakes with fixes | 1,500-2,000 words |
| `reference/02 Word list.md` | A | Controlled vocabulary | Section 5.7 plus field names each word maps to | 1,500 words |
| `reference/03 Field guide.md` | A | Every field | Generated from schema.json: per record type, every field with plain meaning, values, depth, writer, the step that fills it (`filled_by_step`) and one example | generated |
| `reference/04 Rule order.md` | A | Precedence | Section 6.3 with one worked tie-break each | 800-1,000 words |
| `reference/05 Quality rubric.md` | A | Acceptance | Section 11.3 | 1,000 words |
| `reference/06 Checks in words.md` | A | No-code checking | Part 1: the mechanical checks an AI can apply in the reply that wrote the records (section 7.4), as a PASS/FAIL table template for the saved file's note block. Part 2: the judgement checks and step 10's questions for the separate check chat | 1,200 words |
| `reference/07 Report and message formats.md` | A | Talking to the user | Four-part report; checkpoint message shapes (named by what they are, never by letter); resume lines; failure replies; the plain-word command list | 1,000 words |
| `schema/schema.json` | C+A | The data model | Every record type, field, meaning, kind, allowed values, depth, writer (and `chat_writer` where it differs in chat), `filled_by_step`, `defines_id` where the field's first part declares an ID, plain label for views, example (section 5) | generated tables derive from it |
| `schema/steps.json` | C | The steps as data | Per step: units (scope, batch rule, and the unit order across steps 7 and 8), records read and written, card parts by depth and tag, checks run, checkpoint | small |
| `rules/constants.json` | C | Every number the checker uses | Section 5.8 | small |
| `rules/words.json` | C | Word lists | mood-only phrases; emotion adjectives; retired words with replacements (including "look" for a style or a character's appearance); exemptions ("Stage", capitalised, as the product's name, and `stage.py`); banned prompt words; prompt substitutions (torch → flashlight); shortening markers; abbreviation list | small |
| `rules/limits.json` | C | Per-surface sizes | handout token ceiling (Claude surfaces 30,000; ChatGPT sandbox 20,000); card tokens per unit at most 9,000; batch size; units per chat (one sequence); files per upload (Gemini 10 per prompt; the Claude website 20 per chat; ChatGPT Project 25) | small |
| `rules/tone_defaults.json` | C | Tone defaults | D10 §2.2's table per tone: shot-length factor on the estimate, size and lens, movement, contrast band, music default, performance display level; read by TIME-07, the rhythm checks and card 08 | small |
| `adapters/*.json` | C | Dated model facts | Section 8 | medium |
| `templates/*.md` | A | Empty record files | The plain part's headings (`#` and `##` only, G13), the divider line, then every field for each depth, in order, with allowed values in a note block after each record (not parsed) and the END line | 300-1,500 words each |
| `examples/*` | A+C | Gold | Section 14.2 WP12a and WP12b | SC10 about 6,000 words |
| `tools/*` | C | Code | Section 7 | see 7 |
| `library/00 Resolved conflicts.md` | A | K01-K31 | Section 12's table, with the research references | 3,000 words |
| `library/01 What the codes mean.md` | A | Map old codes | Research file codes; C3's old shot numbers (13-04 = SC11 ...); retired labels (C1-C6 costume phases, S1-S6 states, L1-L5 looks) | 800 words |

### 2.4 Surfaces, and who runs the code on each

| Surface | Who runs `stage.py` | Loop | Where files live | Checker |
|---|---|---|---|---|
| 1. Claude desktop with a connected folder (Cowork), or Claude Code | the AI, directly | the code loop (`next`, `handout`, write to the inbox, `apply`, `check`) | the folder (`My breakdowns/<Title>/`) | after every unit |
| 2. Claude website with the skill; ChatGPT Plus Project with "07 Tools.zip" | the AI, in the chat's sandbox | the same code loop; handouts are built from the skill (Claude) or from the ZIP, which holds the steps, cards, templates, examples and library digests (ChatGPT) | the sandbox; carried between chats as one save ZIP | after every unit |
| 3. Gemini, or any app whose self-test finds no code | nobody during the work | the chat loop (section 3): the attached step file, copy boxes, END lines | the user's own folder, saved by hand from copy boxes | mechanical "checks in words" in each reply; judgement checks in a separate check chat; the real checker on a code surface (the Claude website's free plan is enough) through `stage.py adopt` then `check --all`, at the end of each sequence or at least before acceptance |

**Line numbers in chat without code.** There is no numbered story, so every value of kind `lines`, and every line reference inside a sub-part (`line:` in `because`, `from:` in STATE, era lines in RULE, `evidence`, `cause`), is written as a quote anchor (G5). `stage.py adopt` later turns every anchor into line numbers. A user who wants numbers anyway can make `03 Story - numbered.md` once on the Claude website at step 1 and attach it to every chat; then line numbers are allowed.

Grey previews (previs) need Claude Code on the user's computer, where the AI runs Blender; they are offered only there. The browser helper page is **later** (section 14.4).

### 2.5 The chat kit (13 files)

Project knowledge in ChatGPT Projects and Gems may be searched in fragments (D1 rule 1), so anything the AI must read whole is attached to the chat instead. The step files are therefore not knowledge: each chat attaches the one step file it needs, and the resume line names it. Knowledge holds only what can be looked up in parts.

| File | Where it goes | Contents | Length |
|---|---|---|---|
| `00 Paste into instructions.txt` | the Project or Gem instruction box | The house rules condensed: principles, loop without code, "quote the step's one-line task back before working", report format, END line rule, batch size, privacy, "files are the memory" | at most 6,000 characters (the Project instruction limit is [U, smoke test]) |
| `01 House rules.md` | knowledge | SKILL.md body plus reference 07 (report and message formats) | about 5,500 words |
| `02 Cards - story and scenes.md` | knowledge | Cards 01-07 and 15-20 joined | about 16,000 words |
| `03 Cards - picture, sound and making.md` | knowledge | Cards 08-14 and 21-24 joined | about 18,000 words |
| `04 Templates and word list.md` | knowledge | All templates plus reference 01, 02, 04 | about 12,000 words |
| `05 Checks in words.md` | knowledge, and attached to every check chat | reference/06 plus the quality rubric | about 2,500 words |
| `06 Example - The Catch, scene 10.md` | knowledge | The gold scene file | about 6,000 words |
| `07 Tools.zip` | ChatGPT only (not uploaded to Gemini) | `stage.py` and `stage_tools/` plus schema, rules, adapters, steps, cards, templates, examples and library digests, so every command runs in ChatGPT's sandbox | ZIP |
| `08 Steps 00-02 - start, reading, plan.md` | attached to the chats of steps 0-2 | Step files 00, 01, 02 with their chat twins | about 5,000 words |
| `09 Steps 03-06 - world, people, continuity, film rules.md` | attached to the chats of steps 3-6 | Step files 03-06 with their chat twins | about 7,000 words |
| `10 Steps 07-08 - scenes and shots.md` | attached to every scene chat | Step files 07, 08 with their chat twins | about 3,600 words |
| `11 Steps 09-11 and 16 - film pass, check, book, resume.md` | attached to the chats of steps 9-11 and to any chat that resumes after a problem | Step files 09, 10, 11, 16 with their chat twins | about 7,000 words |
| `12 Steps for add-ons - storyboards, prompts, finishing.md` | attached when the user asks for an add-on | Step files 12, 14, 15 with their chat twins (previs, step 13, needs Claude Code and is left out) | about 5,000 words |

A Gem therefore holds six knowledge files (01-06); each working chat attaches at most seven files (the step file, the story (or `03 Story - numbered.md` when the user made it), `00 Start here`, `02 Whole-film summary`, `10 Film rules`, `08 Places and things` when the scene's place has a set plan, and the previous scene file), within Gemini's 10 files per prompt. A check chat (7.4) that needs more than 10 files takes them in two messages. A ChatGPT Project uses all 13 (`00` in its instruction box, the other 12 as files; its cap is 25). Before any work in a unit, the AI quotes the step's one-line task back, which shows that it read the attached step file. `stage.py build-kit` builds all thirteen from the skill, so there is one source.

### 2.6 A project folder (what the pipeline creates for its user)

The numbered files are the record files: the source of truth. Code surfaces write them through `stage.py apply`; chat users save them from copy boxes.

**Every record file has two parts.** The plain part comes first: headings with `#` or `##` only (G13), "At a glance", the shots or items in one plain line each ("shot 150, close-up, 15 seconds: Iona chews, stops, frowns; 'Not mint.'; we stay on her through Saye's answer"), and "Why it's shot this way". Then comes one fixed divider line: `Below this line: details for the AI and the checker. You never need to read them.` Then the records and the END line. Code writes the plain part from the records on code surfaces; the AI writes it in chat. WORDS-04 applies to everything above the divider on every app. In chat replies only the plain part is shown outside the copy box.

```
My breakdowns/The Catch/                   (chat apps: a folder the user makes, named "The Catch - breakdown")
  00 Start here.md                         PROJECT record; where things stand; next step for each app; big choices;
                                           files in this folder; word list; numbered log
  01 Choices.md                            CHOICE and SETVALUE records, open ones first
  02 Whole-film summary.md                 made from files 04-09: the records step 7 reads, minus set plans (never edited)
  03 Story - numbered.md                   the story with line numbers (made by code; in chat without code, only if the user
                                           made it once on the Claude website)
  04 Scene list.md                         SCENE records (list and plan fields)
  05 Story plan.md                         PLAN, SEQUENCE, PLANT, FACT, CHAPTER, STRAND, CARDINAL
  06 World and style.md                    STYLE, WORLD, RULE
  07 Characters and voices.md              CHARACTER, VOICE
  08 Places and things.md                  LOCATION, PROP, TEXT, MOTIF, CAMERA
  09 Continuity.md                         STATE
  10 Film rules.md                         CAMSYS, CAMRULE, RESERVE, LENS, LOOK, VISUAL, SOUNDPLAN, LADDER
  11 Scenes/
    Scene 01 - Loading tunnel.md           SCENE (design), PART, BEAT, SPEECH (prose only), MOVE, SETUP, SHOTLIST, SHOT, CUT
    Scene 10 - Saye's kitchen.md
    Scene 10 - Saye's kitchen - shots 130-200.md      (a second batch file in chat; merges by ID)
  12 Whole-film check.md                   FINDING records from the film pass, with the audit report above them
  13 Health check.md                       the checker's plain report, REVIEW records, quality scores, 3 scenes to read
  14 Time and cost.md                      runtime, shots, generated seconds, money by tier, hours, calendar
  15 The breakdown/                        the readable book: The breakdown.html, The breakdown.md
  16 Spreadsheets/                         Shot list.csv, People, places and things.csv
  17 Captions and audio description/       The Catch.srt, The Catch.vtt, Audio description script.md, Text to translate.md
  18 Storyboard/                           add-on A: Storyboard frames.md (PIC records), Scene 10 - frame prompts.md, Scene 10.html
  19 Grey previews/                        add-on B: Grey preview jobs.md (PREVIS records), Scene 10 - shot 080/ (renders), contact sheets
  20 Prompts for AI video/                 add-on C: Pictures.md, Takes.md, Voices.md (job records), Scene 10 - Saye's kitchen - Kling 3.0 Omni.md,
                                           Reference pictures/, Voices/, Text graphics/
  21 Edit and finishing/                   add-on D: Finishing jobs.md (FINISH, MUSIC records), Assembly guide.md
  22 Rights and credits.md                 RIGHTS records, licences, disclosure text
  Original/                                the story exactly as given, and its fingerprint
  For machines - do not edit/              breakdown.json, breakdown.schema.json, manifest.json, speeches.json, film strip.txt,
                                           handouts/, inbox/, history/, log.jsonl, prompts/, previs plans/, timeline.otio, timeline.edl
```

**File numbers.** Each file's number is its place in the list "Files in this folder" inside `00 Start here`, and no two entries share a number: paired formats sit together in one numbered folder (15, 16). The numbered log in `00 Start here` records every change and is a separate list; save ZIPs carry the log entry number (2.7). `00 Start here` says this in one plain line: "Each file's number is its place in the list Files in this folder; the log below records every change." No file is ever called "final" or "v2": history lives in the log, in git (Claude Code) and in save ZIPs.

### 2.7 Naming exceptions (each justified in one plain sentence)

| Exception | Reason |
|---|---|
| `README.md` | GitHub shows a folder's front page only from a file with this exact name. |
| `CLAUDE.md`, `AGENTS.md` | Claude Code and other coding agents read instructions only from files with these exact names. |
| `SKILL.md` inside `breaking-down-stories/` under `.claude/skills/` | Claude loads a skill only from a file with this name, in a folder with a lowercase hyphenated name, in this place. |
| Python files (`stage.py`, `stage_tools/read_story.py` ...) | Python can only load code files whose names have no spaces and do not start with a digit, so they use full plain words joined by underscores. |
| JSON files in `schema/`, `rules/`, `adapters/`, previs plans, and everything in "For machines - do not edit" | Code opens these by fixed names, so they carry no number and are never renamed. |
| Library files keep their research codes (`B1 Camera, lens and movement.md`) | Every card cites the research by code ("B1 R14"), so the code must stay at the front of the name. |
| Files inside a numbered folder (`11 Scenes/Scene 10 - Saye's kitchen.md`, `20 Prompts for AI video/Takes.md`) | The folder's number is its place in "Files in this folder"; the scene's own number is its identity, so it leads the name. |
| Save ZIPs (`023 Save - The Catch - after scene 10.zip`) | They sit outside the project folder and start with the number of the log entry that made them, which can pass 99, so it has three digits. |
| Media files (`Scene 10 - shot 150 - take 03.mp4`) | Named by scene and shot so they sort with the scene; they carry the take number, never "final". |

---

## 3. The steps

Each step is declared once in `schema/steps.json` (units, records read and written, card parts, checks, checkpoint). On code surfaces `stage.py next` hands out units in order; on chat surfaces the attached step file tells the AI what to do next. In messages to the user, steps are counted from 1 (step 7 here is "step 8 of 12") and named by what they do; the step table in SKILL.md lists both numbers.

**Unit order.** Steps 0 to 6 run in order, once each. Steps 7 and 8 run **sequence by sequence**: for each sequence, step 7 designs and lists its scenes, then checkpoint C, then step 8 expands the same scenes' shots batch by batch, then the next sequence starts. Steps 9 to 11 run after the last sequence. So "the previous scene's last shot" in a handout is always a finished SHOT for scenes in an earlier sequence, and a list item for an earlier scene of the same sequence. TIME-03 runs on a scene after its last step-8 batch. Example for The Catch (`steps/07` carries it): U-07-SC01, U-07-SC02, U-07-SC03, U-07-SC04, U-07-SC05, checkpoint C (blocks), U-08-SC01-B1, U-08-SC01-B2, ... U-08-SC05-B1, then U-07-SC06, checkpoint C (reports), U-08-SC06-B1 ... A chat holds one sequence (section 13.5).

**Common to every step.** *Unit IDs* are `U-<step>-<scope>[-<batch or part>]` (`U-07-SC10`, `U-08-SC10-B2`, `U-07-SC13-P1`). *Redo*: the user says "Redo step 6" or "Redo the shots for scene 10"; `stage.py impact <ID>` lists every record that cites what changes; locked records are left alone unless a choice unlocks them; only affected units are redone. *Loop on code surfaces*: `next` → read handout → quote the unit's one-line task back → write records to `For machines - do not edit/inbox/<unit>.md` → `apply` (parse, check writers, IDs and locks, merge into the numbered file, log) → `check` → fix only the listed problems (at most 3 rounds, then a CHOICE for the user or a trace to the earliest wrong record) → four-part report. *Loop in chat*: read the attached step file and quote its one-line task back → read the files the user attached → write the file in one copy box (plain part, divider, records, END line) with "Save as:" above it → run the mechanical checks in words (section 7.4) and put their PASS/FAIL table at the end of the file (after a `---` line that ends the last record, before the END line; free text, G1) → print one line ("Checked in words: 14 of 14 passed", or only the failures) → four-part report → resume line. At the end of each sequence the resume line also names the check chat (section 7.4).

**Chunking for long works.** Nothing ever reads the whole film's records at once. Whole-film judgement works from derived one-line summaries: the event list (30 lines for The Catch), chapter digests (14 × at most 350 words for The Long Places, about 5,000 words), and the film strip (one line per shot: about 12,000 tokens for 300 shots, about 22,000 for 580; split by act above 20,000).

### Step 0. Start

- **Purpose.** Make the project, test the app, settle rights, show what the user will get.
- **Inputs.** The story file; the app.
- **Outputs.** Project folder; `00 Start here.md` (PROJECT record); `01 Choices.md` with CHOICE-001 (rights), CHOICE-002 (depth, asked: no, default standard) and CHOICE-003 (privacy setting, asked: no, default `not_confirmed`, answered when the user says it is off); `Original/` with the untouched story and its fingerprint (code surfaces).
- **Cards.** 24 Rights, consent and disclosure (the rights question only).
- **Procedure.** (1) Hidden self-test (not shown to the user). On code surfaces: `stage.py new`, then the self-test unit U-00-SELFTEST. `stage.py selftest --prepare` counts the story's lines, checks that code can make and re-read a ZIP, issues the IDs `SC99-SH010` to `SC99-SH200` (a scene number the story does not use; `SC999` with 3-digit IDs) and hands the AI a SHOT template. The AI writes 20 full SHOT records with the END line to the inbox in one reply. `stage.py selftest --score` parses them and records `batch_size` 18 if all 20 records and the END line pass the FORM checks, else 12, then deletes them; it also records `code_execution` and `surface`. In chat without code: the AI quotes the story's first and last line; batch size is 12; `code_execution: no`. (2) The AI reads enough of the story to pick one strong turn and writes one finished shot line from it (example first). (3) Welcome message (section 13.2) with one question: rights. Depth is stated, not asked. (4) Create files.
- **Checkpoint.** Rights [It's mine]. If "not mine, no permission": the project continues for private study, `rights: study_only`, every export is marked "Private study, not for publication" and generation packs refuse public-release batches.
- **Redo.** "Start again" makes a new project; the old one is kept.
- **Chunking.** None.
- **Done test.** PROJECT record exists with `rights`, `depth`, `training_off`, `surface`, `code_execution`, `batch_size`; CHOICE-001 to CHOICE-003 answered or defaulted; `check --step 0` exits 0 (FORM-05 requires only fields whose `filled_by_step` is 0).

### Step 1. Read the story (checkpoint A)

- **Purpose.** Turn any story file into numbered text and fix the scene (or chapter) IDs everything hangs on.
- **Inputs.** The story (`My stories/` or attached). Formats: The Catch's dialect (`## ` headings, `@NAME` cues, `> ` transitions, `= ` title lines, `(...)` parentheticals); Fountain; plain screenplay text; Final Draft `.fdx`; Word `.docx`; `.epub`; `.md`/`.txt` prose; `.pdf` with a text layer when a converter exists; stage plays, treatments, comic and game scripts by the rules in card 02.
- **Outputs.** `03 Story - numbered.md`; `04 Scene list.md` (SCENE records for screenplays: heading, lines, time words, characters, speaking counts, transitions, presentation); CHAPTER stubs in `05 Story plan.md` for prose; CHARACTER stubs (ID and aliases only) in `07 Characters and voices.md`; `For machines/speeches.json` (screenplays); an odd-lines report inside `04 Scene list.md` above the divider; CHOICE records for anything odd, and CHOICE-004 for `format` (asked: no; default derived from the first estimate: `short` under 40 minutes, `feature` otherwise); the first runtime estimate (D13 v0) in `14 Time and cost.md`.
- **Cards.** 02 Adapting prose (intake part) for prose and unusual formats; 01 Reading the whole story (length part).
- **Procedure.** `stage.py read` detects the format (any line starting `## INT` or `## EXT` means The Catch's dialect), normalises, numbers every line (prose: one paragraph per line), keeps the original and its fingerprint, splits scenes or chapters, extracts speeches (speaker resolved to a character ID, path from the cue extension or parenthetical: `(V.O.)`, "in her ear", "(RECORDED)"), transitions and title lines, and proposes alias merges (`DR SAYE` = `SAYE`). It classifies capitalised tokens as sound, prop, text or emphasis and collects the light, colour and darkness words of each scene (for COVER-07 and COVER-08). **Placement rules** for lines outside scenes: `= ` lines before the first heading are title-page lines, not shots, and the first becomes `PROJECT.title` (The Catch l.1-6); a `> ` line before the first heading is SC01's `transition_in` (`> FADE IN:`, l.8); mid-film `= ` lines become card shots (`= THE CATCH` at l.488 → SC10-SH990); `= ` lines after the last scene's final transition become an end card of the last scene (`= THE END`, l.1852 → SC30-SH990). For prose, a heading is a chapter heading when it starts with a roman numeral and a full stop, a number and a full stop, or the word "Chapter"; the first heading is the title when it is not a chapter heading and the next heading is (The Long Places: l.1 is the title, and the AI proposes the clean title "The Long Places" as a small choice); lines between the title and the first chapter are front matter, listed in the odd-lines report (l.3's editorial note). The AI reads only the odd-lines report and confirms or corrects: secondary headings such as `(ON THE TABLET)` are presentation notes; scanned PDFs are refused with the one-step fix (open in Google Docs, save as text). A thin source (a treatment; little action per scene) switches on authoring mode: later steps may write scenes, each `origin: invented`, approved at checkpoint P or B. *Without code:* the AI writes the scene list one reply at a time (30 scenes in one or two replies), giving each scene's `lines` as a quote anchor pair (its first and last line, G5), and numbers speeches in cue order per scene by hand; `adopt` and the checker verify later.
- **Checkpoint A** (one message, section 13.3): the scene count is stated as a fact ("I found 30 scenes, one for each heading in your script"); anything genuinely odd (a heading that may be two scenes, a title card mid-film) goes under "small choices I made". One question: length, printing the first estimate as computed ("about 35 minutes as written (32 to 38; the page count suggests up to 44); keep everything, or give me a target?") [keep everything]. For prose, checkpoint A is only "I found 14 chapters, 49,152 words; I'll plan the whole book next" (no question); the scene list comes at checkpoint P.
- **Redo.** Before the lock: `stage.py read` again. After the lock scenes are never renumbered: an inserted scene takes a letter (`SC06A`); a removed one becomes `status: omitted`. A revised script is matched to old IDs by heading and text; changed scenes go stale.
- **Chunking.** Code reads any length. Without code, prose is read one chapter per reply.
- **Done test.** Screenplay: scene count equals the story's headings; every cue resolved to a character or listed as odd; every `= ` and `> ` line placed by the placement rules; the checkpoint A CHOICE records answered or defaulted; scene IDs locked. Prose: every chapter heading found; the title and front matter placed; chapter IDs fixed; first and last lines quoted per chapter. Both: `check --step 1` exits 0.

### Step 2. Story plan (checkpoint P for prose)

- **Purpose.** The film-level plan every later choice keys to: event per scene, sequences, one climax and a crisis, the peaks table, plants and payoffs, who knows what, whose scene, genre and tone, runtime and budgets; for prose, which chapters and strands survive, the format, the scope of the scene work, and the step outline.
- **Inputs.** Numbered story (in slices), scene or chapter records, checkpoint A answers.
- **Outputs.** `05 Story plan.md`: PLAN, SEQUENCE, PLANT, FACT (Standard for facts in suspense, mystery or dramatic irony; every fact at Detailed); prose adds CHAPTER digests, STRAND, CARDINAL. Plan fields on each SCENE in `04 Scene list.md` (`event`, `sequence`, `scene_intensity`, `whose_scene`, `story_day`, `rhythm_class`, `tone`, `tone_undercurrent`, `tags`; code writes `target_duration_s`). Prose: SCENE records for the step outline. No beat or shot exists yet, so every reference to a moment inside a scene is a **story point**: the scene ID and a quote anchor (`SC24 "She deletes the way home."`, kind in G5); code resolves it to a beat at step 7.
- **Cards.** 01 Reading the whole story; 02 Adapting prose (prose); 08 World, style and genre (genre and tone part).
- **Procedure, screenplay.** (1) Units of 10 scenes write `event` (one past-tense sentence, no psychology), `scene_intensity` (1-10 across the film; exactly one 10 or one 10 range on the climax), `whose_scene`, `story_day`, `rhythm_class`, `tone` and `tone_undercurrent` (D10 §2.1 values), `tags`. (2) One film unit reads only the 30 event lines plus short quoted evidence and writes PLAN (theme question, core value, core opposition as two nouns, `crisis`, `climax`, acts, peaks with reasons, point-of-view plan, genre, `tone_home`, `tone_range`), SEQUENCE records (one list; colour and visual plans are written in step 6 against these IDs), PLANT records (what is planted and paid off, as story points; the shots that plant and pay off are linked from the shot side at step 8), and FACT records for what the audience and each character know, with `element` naming what would give the fact away. When two climax readings are defensible, both go into a CHOICE for checkpoint B. (3) If the user set a shorter target at A: CARDINAL records by the deletion test, then a compression plan (trim, merge, fold, then cut a strand; D2 R10) written as `keep`, `merged_into` and `op` items, never rewriting lines.
- **Procedure, prose.** (1) One digest unit per chapter: at most 350 words (events, people, places, time markers, key lines by number), candidate scenes with A3's five-test scores and decisions. (2) One whole-book unit reads the 14 digests (about 5,000 words): strands, cardinal functions, recurring devices (as RULE records of kind `device`), and two or three independent macro plans with runtime, scene and shot budgets, cost and review hours from the first estimate (`stage.py estimate --version v0`). (3) Checkpoint P. (4) Outline units (two or three chapters each) write the SCENE records of the chosen plan in screen order, using IDs issued in the handout; every scene cites its source lines in `from_lines` or is `origin: invented`; for prose the AI writes `heading`, `int_ext`, `place_text` and `time_text`, and code derives `lines` from `from_lines`.
- **Checkpoint P (prose, blocking).** "Here is how the book becomes a film" with the plans side by side and "what the audience loses" in each. Default for The Long Places: plan A (a feature of about 100 minutes, 48 scenes) and "start the scene work with chapter I as a trial", which sets `PROJECT.scope` to the scenes of chapter I (5 of 48). The recurring-device rules (letters `open_and_close`, the threshold refrain as a saved template) are shown as small choices. **Scope:** checks, the film pass, estimates and exports run only on scenes in scope; the health check says "Scope: 5 of 48 scenes"; "go on to chapter II" widens it.
- **Redo.** "Redo the story plan" rewrites unlocked plan records and lists scenes that cite changed sequences or plants. "Make it 20 minutes" re-runs compression; cut scenes become `omitted`, never renumbered.
- **Chunking.** Screenplay: 3 event units plus 1 film unit. The Long Places: 14 digest units, 1 whole-book unit, about 6 outline units. The plan never reads the whole text.
- **Done test.** One climax; one scene-intensity 10 (or one 10 range) on it; every scene in exactly one sequence; every plant has a payoff; every peak away from the climax has a reason; every story point's quote found once in its scene; prose: every cardinal function in a kept scene, step targets within ±10% of the runtime target, checkpoint P answered, `scope` set, scene IDs issued and locked; `check --step 2` exits 0.

### Step 3. World and style

- **Purpose.** Decide once where and when the story happens, what the film looks like, and the story-world rules.
- **Inputs.** Plan, locale cues harvested by code (words such as "torch", "night bus", signage, vehicles), checkpoint A answers.
- **Outputs.** `06 World and style.md`: STYLE, WORLD, RULE records (story-world rules such as `WR-MIRROR` with its eras and each era's frame value; exceptions such as `WR-F-EXCEPTION`; `WR-TITLES`; recurring-device rules for prose). CHOICE records (asked: yes) for place and time, style and frame shape, music, and each story-world rule group, with SETVALUE records for structured answers such as the era lines (5.5, CHOICE). A tone CHOICE only when `tone_home` is unclear from the story.
- **Cards.** 08 World, style and genre; 16 Glass, mirrors and sides (only when a rule concerns handedness); 17 Screens, text and in-story cameras (text orientation rules).
- **Procedure.** Harvest locale cues with evidence and label each `inferred`; propose a default world and one alternative; propose three style directions and the frame shape with a story reason (B1 P3), the style marked "provisional until you see pictures" (D5's test of three directions on three hard shots is the first job of add-on A or C); write each story-world rule with the exact lines where it starts and ends (quote anchors); for a mirror rule, each era's `frame` value (`original` or `reversed`) and the handedness each element starts with (K03); list what each rule governs. Every choice not stated by the story becomes a CHOICE with a default and a reason.
- **Checkpoint.** None here: its CHOICE records go to checkpoint B.
- **Redo.** "Make it animated": STYLE changes; shot designs stand; fixed descriptions, look blocks and all compiled prompts are marked stale.
- **Chunking.** One unit.
- **Done test.** STYLE, WORLD present; every story-world rule has start and end lines found in the story; every governed ID exists or is listed for step 4; `check --step 3` exits 0.

### Step 4. Characters, places and things

- **Purpose.** Design everything the film shows more than once: characters and voices; places with set plans; props; text in picture; motifs; in-story cameras.
- **Inputs.** Per element, a code-built list of every source line mentioning its aliases (capped at 400 mentions plus every mention with a physical noun; `stage.py lines CH-X --more` on request); plan; world and style.
- **Outputs.** `07 Characters and voices.md` (CHARACTER, VOICE); `08 Places and things.md` (LOCATION with set plan objects and marks, PROP, TEXT, MOTIF, CAMERA); CHOICE records for sides, casting placeholders, invented names, and two small choices: every character's `likeness_basis` (default `invented`) and every voice's `source` (default `designed`; asked again at add-on C, decision 14).
- **Cards.** 05 Characters; 06 Voices and performance; 07 Places, things and motifs; 12 Staging and composition (set plans); 17 Screens, text and in-story cameras (TEXT and CAMERA); 24 Rights (name check, no real likeness).
- **Procedure (in this order, each feeds the next).** (1) Harvest: every thing named more than once or at a turn, with lines. (2) Motifs: theme question and core opposition from PLAN, B4's six tests, rank, emphasis map; appearances written as scenes or story points (no shot exists yet). (3) Characters: evidence, design thesis, the lineup (height, mass, shape, value, colour, tempo as words, so code can compare principals: they must differ in at least three), for principals at Standard the face (its three largest distinguishers, B5 R21), movement (home, stress and break effort, each as body part, direction, speed and what stays still), one signature gesture with its script line, status (default and the beats where it flips) and distance (default and closest, in metres, with the scenes that change them), fixed description last (25-40 words for principals, 20-30 for minor characters; visible nouns only; no expression words; no real person), sides in own terms, casting placeholders `open` (never guessed). (4) Voices: voice description, pitch band, pace in words per second (default 2.5; weighted speakers slower, Saye 2.0), accent from WORLD, how each is heard (paths). (5) Places: story job, loud or quiet set (at most `loud_sets_max`), anchor, exits, room sound; a set plan (size, origin corner, axes, objects, marks, in metres, in the orientation named by `plan_orientation`) for every place used by a shot likely to need previs level 2 or more, a reflection or glass shot, or three or more people in one space; all places at Detailed depth. (6) Things: real size, surface, states to come; every readable text as a TEXT record. (7) In-story cameras. (8) Name check (D4 Recipe 3) for invented names.
- **Checkpoint.** None here: design ideas and small choices go to checkpoint B.
- **Redo.** "Saye is frightened, not cold": only CH-SAYE re-runs; the impact list names every shot citing CH-SAYE or CR-SAYE.
- **Chunking.** One unit per principal character; four minor characters per unit; two places per unit; one unit for props and text; one for motifs. The Catch: about 12 units.
- **Done test.** Every speaking cue has a CHARACTER; every principal has a VOICE, a lineup, face, movement, gesture, status and distance; no two principals share four or more lineup columns (CRAFT-20); fixed descriptions within length; every sided feature has an own side and origin; every readable text item has a TEXT record; `check --step 4` exits 0.

### Step 5. Continuity

- **Purpose.** Know the state of every changeable element in every scene, with the line that changed it, and every side.
- **Inputs.** Scenes in slices of five, with the states entering them; characters, places and things; world rules.
- **Outputs.** `09 Continuity.md`: STATE records (`CH-IONA.S02`, `PR-FLASK.S02`, `LOC-QUARANTINE.S02`), each with scenes, cause line, state line (words appended to the fixed description in prompts), side features in own terms, handedness (`original` or `reversed`), pictures needed. A side the story states for an element that is mirrored on screen is an apparent side: the AI records the own side and marks its origin `inferred` (Saye's ring: "On her right hand." in era b is her own left; K03).
- **Cards.** 05 Characters (state lines); 16 Glass, mirrors and sides (when a handedness rule exists).
- **Procedure.** Walk the lines; copy the previous exit state into the entry (exactly, under `CONTINUOUS`); add each change with its cause line; an unexplained difference is recorded `origin: inferred` at first sight with the gap named, or raised as a CHOICE.
- **Checkpoint.** Unconfirmed sides go to checkpoint B as small choices.
- **Redo.** "Redo continuity from scene 12".
- **Chunking.** Five scenes per unit (6 units for The Catch); one sequence per unit for prose.
- **Done test.** Every change cites a line found in the story; `CONTINUOUS` scenes inherit; every element named in a scene has a state for it; `check --step 5` exits 0.

### Checkpoint B (big choices), between steps 5 and 6

One message, at most 7 numbered items, each one or two lines with its default and reason (section 13.3). Items in this order: climax reading; style and frame shape (with the home tone in the same line, only when it is unclear); place and time; music; story-world rules (grouped, with eras and exceptions); what each principal's appearance must say (one sentence each); "small choices I made" (one accept item pointing to `01 Choices.md`). Three items are marked "these matter most": the three whose change would redo the most records (computed from each CHOICE's `affects`; for The Catch: frame shape, the mirror world, the climax). The user may answer "defaults". Answers become CHOICE answers, set their fields, and lock steps 2-5 records they name. Then `02 Whole-film summary.md` is written (by code; by the AI in chat).

### Step 6. Film rules

- **Purpose.** Write each department's system for the whole film before any scene, keyed to the one sequence list and the one climax.
- **Inputs.** Plan, world and style, characters, places, continuity, checkpoint B answers.
- **Outputs.** `10 Film rules.md`: CAMSYS (frame shape and why, lens type and family, the normal lens, step changes, default height and move, banned choices, camera speed, the break, the time rule for expanded action); CAMRULE per principal (`CR-ELI`: in control, losing control, never, closest and where, as a story point, limit before); RESERVE (`RC-01`...: each rationed choice, how it is matched, most uses, allowed places, never on), always including two film-level reserves: the non-insert extreme close-up (at most `extreme_close_up_film_max`) and the push-in (in at most `push_in_scene_share_max` of scenes); LENS (`LX-01`: an exception and where it is allowed); LOOK per place and time (`LK-SAYE-KITCHEN-NIGHT`: the look block pasted into prompts, main light placed on a set-plan object or a compass wall, contrast, what stays dark, palette, accent, light cues at story points); VISUAL per sequence (`VS-SQ03`: colour-script row and visual-structure plan); SOUNDPLAN (music policy from B, clip audio rule, voice policy, device budget, loudness target, planned ruptures); LADDER (each scene's main turn as a story point with planned size and hold; it escalates by size and hold together; the film's tightest size and longest hold are not spent before the climax unless the peaks declare counterpoint; other scenes' main turns land at close-up or on a deliberate wide, A2 R4). A small choice CHOICE for `voice_policy` (default `designed_only`).
- **Cards.** 09 Film rules and restraint; 10 Camera; 11 Light and colour; 13 Cutting, rhythm and sound; 12 Staging and composition (visual structure part).
- **Procedure.** Climax and peaks first (from PLAN), then camera system and character rules, reserve and lens exceptions, looks (main light placed in the room so its frame side is derived per shot and era), colour script (peaks first, valleys lower, B2's monotony test), visual structure, sound plan, ladder. Every line cites a plan, character, motif or rule ID. Beats and shots do not exist yet: moments inside scenes are story points, which code resolves to beats at step 7.
- **Checkpoint.** None here (the user approved the choices that drive it at B). Film rules are locked on writing; the first checkpoint C message states them in five plain lines, where a change still costs little; the book shows them in plain words; a later change asks first.
- **Redo.** "Redo the colour script": VISUAL records re-run; scenes and shots citing them go stale.
- **Chunking.** Three units: (a) CAMSYS, CAMRULE, RESERVE, LENS; (b) LOOK records; (c) VISUAL, SOUNDPLAN, LADDER.
- **Done test.** Every principal has a CAMRULE; every saved and banned choice is listed, including the two film-level reserves; every lens exception names where it applies; every location in use has at least one LOOK; every sequence has a VISUAL; the ladder names every scene with a main turn; every story point's quote found once in its scene; `check --step 6` exits 0.

### Step 7. Scene design and shot list (checkpoint C per sequence)

- **Purpose.** Per scene: what happens, who wants what, where it turns, how bodies move, each department's one idea, the turn pictures, the dial, and a one-line shot list that fixes the shot IDs.
- **Inputs (the handout).** Step file excerpt; the scene's numbered lines; its plan fields and sequence row; only the film-rule records it touches (camera rules of characters present, reserve entries allowed here with their remaining uses, its VISUAL row, its LOOK, SOUNDPLAN lines, its LADDER rung); fixed descriptions, state lines, voices, and the movement, gesture and status lines of characters present; states at scene start; the FACT records whose elements appear here; plants and payoffs whose story points lie here; set plan if any; the previous scene's last shot (or list item, inside one sequence) and the next scene's heading; the template; one gold excerpt; pre-issued IDs (beats `SC10-B01..B30`, parts, moves, setups, shots `SC10-SH010..SH400` in tens, speeches listed with their IDs and words).
- **Outputs.** `11 Scenes/Scene NN - <place>.md`: the plain part ("At a glance", the shots in one plain line each, "Why it's shot this way"; written by code from the records on code surfaces, by the AI in chat), the divider, then SCENE design fields; PART; BEAT; SPEECH (prose only); MOVE; SETUP; SHOTLIST. After `apply`, code resolves every story point that lies in this scene (PLAN.crisis, LADDER, CAMRULE, LOOK light cues, FACT, PLANT, MOTIF appearances) to the beat whose lines contain its quote and stores the derived beat ID.
- **Cards (card parts by depth and tag; at most 9,000 card tokens per unit, `limits.json`).** Quick: 03 Scenes, values and beats; 14 Shot design: list part. Standard: add 04 Dialogue on screen: landing face, flaws and pauses; 12 Staging and composition: stations and configuration; 13 Cutting, rhythm and sound: scene rhythm. Detailed: add 06 Voices and performance: display and stillness; 07 Places, things and motifs: emphasis; 11 Light and colour: per-scene light. Situation cards by the scene's tags (their "questions in order" and "traps" parts): `action` → 15; `glass_and_reflection`, `handedness` → 16; `screens_and_text`, `in_story_footage` → 17; `suspense_and_reveal`, `darkness` → 18; `prose_interior`, `montage_and_time` → 19; `creature`, `violence` → 20. `steps.json` names the parts; `make_handout.py` drops the lowest-listed parts first when the cap is reached.
- **Procedure (in this order).** (1) Event sentence (from the plan) and the sign test on each value: open and close charges (kind `charge`, G5); every beat with `turn` other than `none` changes the sign of at least one value's charge or reaches that value's `close` (CRAFT-18). (2) Wants, driver, conflict type, third thing. (3) Beats: action and reaction as tactics (-ing words), tasks, nonverbal beats, beat intensity 1-5 (at most two 5s per part), turns (`turn`, `main_turn`), parts; line flags (`flag`: on the nose, melodrama, forced exposition, monologue, repetitious, can play silent, interrupted, each naming its speech); in a scene tagged `three_or_more`, each beat's engaged pair and silent third. (4) Five steps for each turn and each beat of intensity 4 or more. (5) Dialogue pass (Standard: turn beats, every flagged line, every beat where a fact is revealed, every refusal, and lines named by the plan; Detailed: every line): landing face, unsaid and its carrier, pause after each beat by tier. (6) Staging: one staging line (Standard) or moves on the set plan (Detailed or when a set plan exists), with each character's `start` (mark, facing, posture) when a set plan exists, setups, the line of action per part. The configuration changes on every turn. Between turns a body moves only when you can name the want behind the move (toward the door = escape, toward the other person = appeal) or its task, and distances change only when a value's charge changes (B3 P2-P3). A scene over 8 beats names 2-4 stations (marks) in its staging line. (7) Scene idea; one department idea each for camera, light, staging, sound and design, each citing an ID, where `holds_baseline` is a full answer (principle 4); at most two departments change at the main turn, and `scene_idea` names them (B3 R7, B1 P11). (8) Turn pictures: for each turn, one sentence describing the frame. (9) The dial: per beat, planned size, distance and height, drawn toward the turn and away from it; its light stays `as_look` and its sound `room_sound` unless a source in the story can change them (B2 R10) or at the planned rupture; a beat the script already marks gets no added light or sound change (B4 R17). (10) Rhythm shape, target average shot length (from the rhythm shape, the scene's tone and card 13; a suspense scene holds on the character who does not know, A4 S2), the one rupture. (11) Action scenes: geography, cause chain, escalation, reversals, the action score, time treatment (card 15, D11's values). (12) The one-line shot list: turn shots first, then must-keep shots (plants, reveals, geography), then the rest; every beat and every line covered; each list item names beats, role, size, frame, subject, seconds and one line of what we see. (13) Additions (inventions) listed, each marked whether it changes what the scene means.
- **Checkpoint C.** After the last scene of each sequence has its list, one message with each scene's "At a glance" and one-line list in plain words, total screen time, the additions that change meaning (the rest are counted in `00 Start here`: "41 small additions kept; the list is in 01 Choices") and anything flagged. It asks one thing: "Reply next, or tell me what to change." The first message (the first sequence, which waits for the user) also states the film rules in five plain lines, saying that a change there costs little now, and says once: "After this group I'll carry on and show you each group; say 'stop after each group' if you prefer." Later sequences are reported without waiting; any change the user sends is applied by redoing only what it touches. Scene-specific open choices (SC10: B3's staging or Saye in the foreground) appear here as the scene's small choices. In chat apps every scene reply ends with its one-line list anyway.
- **Redo.** "Redo scene 10" (design and list) or "Change shot 150 to ..." (list item; the expanded shot then goes stale).
- **Chunking.** One scene per unit. A scene over 70 non-blank lines or 14 beats is designed in two units by part and the list written in a third: counting non-blank lines with the heading (the same count `read` prints): in The Catch, SC12 (84) and SC13 (98), as U-07-SC13-P1, U-07-SC13-P2, U-07-SC13-LIST. SC10 (55 non-blank lines, 11 beats) is one unit.
- **Done test.** Every source line of the scene is in a beat; every speech is in a beat; every turn has a turn picture and at least one list item with `role: turn`; the dial covers every beat; list items cover every beat; every list ID is in the issued block and in tens; every story point in the scene resolved to a beat; `check --step 7 --scene SC10` exits 0.

### Step 8. Shot details

- **Purpose.** Expand the approved one-line list into full SHOT and CUT records, batch by batch.
- **Inputs (the handout).** As step 7 plus the scene design just written and the approved list items for this batch, each with its **provisional time floor** (5.6, computed from every speech whose cue lies in that item's beats and the pause owed by its beats). The handout lists only the sizes, angles and moves the camera system allows here (banned choices are left out; saved ones appear with their RC ID and remaining uses), so it never invites a banned choice. It also lists the fields that need a `why` when they differ from their default, with each default (5.4 rule 11).
- **Outputs.** SHOT and CUT records appended to the scene file (code surfaces) or saved as `Scene NN - <place> - shots 130-200.md` (chat; `adopt` merges batch files by ID, G10); derived fields computed by `stage.py build`. When a shot writes a `time_slice` or a CUT writes `shared_geometry`, code creates the named PREVIS stub with `status: planned` if it does not exist (`PV-SC06-MASTER-V01`, level 3).
- **Cards.** 14 Shot design: shot part; 10 Camera: slots and moves; 12 Staging and composition: frame rules; 13 Cutting, rhythm and sound: cut points and sound; Standard adds 04 Dialogue on screen: landing face and pauses, and 06 Voices and performance: display and stillness; Detailed adds 11 Light and colour: per-shot light; the same situation card parts as step 7; at most 9,000 card tokens per unit.
- **Procedure.** For each list item in order, one SHOT record at the project's depth, reason-first field order (purpose and because before camera values): purpose; because; role; camera; subjects with position and facing (only where no set plan exists; with a set plan code projects them), visible behaviour, tactic, energy, display level, what stays still, eyeline and its dwell, travel direction, and what must not happen yet (a look saved for a later beat); speeches heard and whether the speaker is seen; things with emphasis, and `plant:` or `payoff:` on the thing item that plants or pays off a PLANT; text; keep hidden (each item naming the FACT it hides and how), must show, must not show; light only if different from the look; sound; screen time at or above the provisional floor; moments; end; cut reason; making fields, including `held: yes` when the meaning depends on not cutting; `pov_break` when the shot leaves the whose-scene character's place or knowledge; `why` wherever a value on the list in 5.4 rule 11 departs from its default or the camera system, and always on turn shots. A CUT record only for a join that is not a plain cut.
- **Checkpoint.** None (the list was the checkpoint).
- **Redo.** "Redo the shots for scene 10" keeps the list; "Make shot 150 tighter" edits one list item and its shot.
- **Chunking.** Batches of `batch_size` shots (12 by default; 18 once the self-test passes), split by ID range from the list; the manifest records each scene's expected batch ranges. During step 8, ID-07 and COVER-02 to COVER-04 run only on the batch's ID range and its beats; they run in full after the scene's last batch, together with TIME-03. The Catch at Standard: 300 to 580 shots (D13's estimate at full length is 583), 25 to 50 batches.
- **Done test.** Every list item has exactly one SHOT with the same beats, role and size (a differing value is an error unless the list item was changed); every batch file's END count matches its range; `check --step 8 --scene SC10` exits 0 (no ERROR; warnings shown at the next checkpoint).

### Step 9. Film pass

- **Purpose.** Judge the whole film as a structure before any picture is made.
- **Inputs.** The film strip (derived, one line per shot: ID, beats, role, size, lens, move, reserve used, emphasis, screen time, scene intensity), film rules, plan, motif appearances, the checker's film-level report.
- **Outputs.** `12 Whole-film check.md`: the audit report (code) and FINDING records for fixes; fixes routed back to steps 7-8 for named scenes only.
- **Cards.** 09 Film rules and restraint (film pass part).
- **Procedure.** `stage.py check --film` runs the FILM checks (ladder, rhyme, character camera rules, colour monotony, peak rule, shot monotony, heavy-handedness counts, reserve positions, device budgets, motif and loud-set counts, tone outside the plan). Then one judgement unit (a fresh unit; in chat, a check chat) answers yes/no questions built from the records: the sound-off test on every turn picture; the stranger test (could someone who has not read the story say what each scene is about from its turn pictures and purposes?); the heavy-handedness questions (symbols not in the source; more than two plant inserts in a scene; music under subtext; a light cue on the line that states the point; rhymes the story does not support); "Does any shot feel like a different film?". Each "no" becomes a FINDING with record, rule, evidence, fix.
- **Checkpoint.** Only findings that change a creative decision reach the user (usually none to three, as CHOICE records); the rest are fixed and logged.
- **Redo.** "Run the film pass again".
- **Chunking.** One judgement unit per act when the strip exceeds 20,000 tokens.
- **Done test.** All FILM errors fixed; every FINDING `fixed` or `accepted` with a reason.

### Step 10. Check and estimate (acceptance)

- **Purpose.** Prove the breakdown is complete and consistent, score its quality, and say what it will cost.
- **Inputs.** All records; adapters and prices.
- **Outputs.** `13 Health check.md` (first line "In short: 2 things need you, 14 small fixes I made, 3 warnings"; on a partial scope, "Scope: 5 of 48 scenes"; then the quality scores; then "3 scenes to read"; then details by file); REVIEW records; `14 Time and cost.md` (the estimate from the shots, D13 v1); `For machines/breakdown.json`; a first `15 The breakdown/` on code surfaces.
- **Cards.** reference/05 Quality rubric.
- **Procedure.** On code surfaces `stage.py export book` runs first (it is cheap and can be remade at any time), so the user reads the three scenes as book pages. `stage.py check --all` (tidy fixes logged; real problems fixed in at most 3 rounds); `stage.py compile --lint-only` (routing and lint on every shot's scene model, no packs written; its GEN error count scores rubric criterion 9); `stage.py estimate --version v1`; `stage.py questions --sample` derives yes/no questions for every turn shot, every turn beat, every must-keep shot, every shot needing mirror, text or violence handling, and a seeded 10% of the rest; a fresh unit answers them against the story (never the unit that wrote the shots; in chat apps, a check chat with only the saved files and `05 Checks in words.md` attached); rubric scores with one line of evidence each.
- **Checkpoint (acceptance).** At most 3 things for the user to check, each with a default (often none), and the three scenes to read (the climax scene, the densest dialogue scene, the biggest action scene) as pages of `15 The breakdown` (in chat without code: the plain parts of their scene files), with the 10-question review sheet. One question: "Anything you want changed in these three scenes? [no]".
- **Redo.** "Check again" at any time.
- **Chunking.** Question batches of 40, each reading only the records and lines it cites.
- **Done test.** No ERROR; rubric pass rule met (section 11.3); acceptance answered or defaulted.

### Step 11. Book and exports

- **Purpose.** Hand the user the deliverable.
- **Outputs.** `15 The breakdown/The breakdown.html` and `The breakdown.md` (contents; "How to read this" with examples from the user's own story; story plan; people, places, things; film rules in plain words; each scene with At a glance, the one-line list first and full shots folded underneath; word list; printable); `16 Spreadsheets/Shot list.csv` (columns in 5.9) and `People, places and things.csv`; `17 Captions and audio description/`; `For machines/timeline.otio`, `timeline.edl`, `breakdown.json`, `breakdown.schema.json`.
- **Procedure.** `stage.py export all`. The last message names the three files to open first and ends with one recommended next step chosen for this project (for example: 'Next, if you want to see it: say "make storyboards" (about $10 and an hour)'). At Quick depth it says once: "Quick plans can't be turned into AI video prompts until a scene is made standard. Say 'go deeper on scene N' for the scenes you want to make." Without code: the AI writes `15 The breakdown/The breakdown.md` as a contents page linking the scene files; the rest is made when the folder is next checked on a code surface.
- **Cards.** None (code); reference/07 for the final message. **Checkpoint.** None; the report says which files are for reading and which are for other programs. **Redo.** "Make the book again" (minutes, by code). **Chunking.** Code; any size.
- **Done test.** Every export produced; CSV opens with its byte-order mark; OTIO passes the structural check; captions pass the SRT and WebVTT format checks.

### Add-ons

| Add-on | Step file | Makes | Checkpoint | Done test | Details |
|---|---|---|---|---|---|
| A. Storyboards | 12 | First job: D5's style test (three style directions on three hard shots; one question "Which of these three styles? [A]"). Then PIC records (`use: storyboard`), frame prompts, the storyboard page | none (slideshow per sequence; the user names only frames to redo) | every shot with `storyboard: yes` has a compiled frame prompt, and an approved PIC once pictures exist | section 10 |
| B. Previs ("grey previews" to the user; Claude Code only) | 13 | PREVIS records, plan files, grey renders, blocking reports, contact sheet | D: one contact sheet, "Reply with the numbers of any that look wrong, or 'fine'." [fine] | every shot at previs level 2 or more has a plan, `BLOCKING OK` and facings within 20°; shots with `framing_critical: yes` need the answer at D; the others are `approved: auto` once they pass those two checks | section 9 |
| C. Generation packs ("prompts for AI video" to the user) | 14 | First job, if add-on A has not run: D5's style test. Then reference-picture jobs, start and end picture jobs, voice line script and VOICETAKE records, compiled prompts per model, lint reports, cost lines, TAKE records | spending cap once; E: keep or reject each take | every shot in scope compiles with 0 GEN errors on its routed model and is priced with a model-facts date under 30 days; Quick-depth scenes are made standard first | section 8 |
| D. Edit and finishing | 15 | FINISH records created from shots (flip, composite, crop, speed, upscale, grade, title, lip sync, voice path), MUSIC cues if any, assembly guide, disclosure text | none | every derived post operation has a FINISH record; the timeline and assembly guide exist | section 8.7 |

---

## 4. Depth modes and optional modules

Depth is a filter on the schema, not a different template: every field carries `depth: q | s | f` (`f` is the Detailed depth) and `filled_by_step`; handouts and templates list only the fields at the project's depth; the checker requires only those, and on `check --step N` only those whose `filled_by_step` is N or earlier. The user's words are quick, standard and detailed. "Go deeper on scene 13" sets that scene's `depth` above the project's; nothing is thrown away.

| | Quick | Standard (default) | Detailed |
|---|---|---|---|
| Steps run | 0-7, 9 (code audits only), 10, 11. The one-line shot list is the final shot plan | 0-11 | 0-11, every field |
| What it adds | Scene list; plan (events, sequences, climax, crisis, peaks, plants); world and style; characters with fixed descriptions and sides; places and things by name; continuity of sides and injuries; minimal film rules (camera system, reserve, character rules for principals); per scene: values, beats with tactics and turns, turn pictures, the one-line list with size, subject, seconds; estimate; book | + voices; principals' face, movement, gesture, status and distance; who-knows-what facts for suspense, mystery and dramatic irony; set plans where needed; full continuity; looks; colour and visual plans; sound plan; ladder; department ideas (holding the baseline counts); dial; line flags and a dialogue pass on turn beats, flagged lines, revealed facts and refusals; full SHOT records with purpose, because, why, subjects (with display level, stillness and travel), speech, sound, moments, making fields; film pass judgement; rubric | + dialogue pass on every line (unsaid, core word, line design); set plans for every place; per-shot composition and light; each character's expression range and one image; performance continuity on every subject; every fact; information and rhythm plans; two independent turn-picture designs for the three most intense scenes (the user picks) |
| The Catch (estimates, to be measured in the test) | about 60 units; AI 2-4 h in Claude Code; user 30-45 min; chat 4-6 chats | about 130 units; AI 8-12 h (3-4 h with sub-agents); user 1.5-2 h; chat 10-14 chats | about 190 units; AI 14-20 h; user 2.5-3.5 h |
| The Long Places, plan A | whole-book plan plus one-line lists, AI 4-6 h | chapter by chapter, AI 18-28 h | per chapter only; rarely worth it for a whole novel |

**Modules** (switch on alone; none is needed for the breakdown):

| Module | Adds | Cost in time and money (The Catch; estimates) | Needs |
|---|---|---|---|
| A Storyboards | Grey sketch frames: turn and must-keep shots (default, about a third) or all shots; page per scene; the AI picks the frame that passes the yes/no checks | about $10 in batch for 300 frames through an image API; or the chat path, watched as a slideshow per group | any surface; code makes the page |
| B Previs (grey previews) | Grey 3D renders, plan views, depth videos, camera tracks, blocking checks for shots at previs level 2+ | seconds to a minute per shot to render; 15-30 min review per hard shot; about 20-40 shots | Claude Code on the user's computer, where the AI runs Blender (bpy). Offered only there; elsewhere the offer says "Grey previews need Claude Code on your computer; everything else works here." |
| C Generation packs | Reference pictures, start and end pictures, voices first, per-model prompts, linter, cost, take log | packs: $0 and 1-3 h AI time; spending them at full length: about $2,600-7,900 at C1's tiers rescaled by D2 (35 min), 45-90 h of review | any surface for packs; batches need a connector or API account and a spending cap |
| D Edit and finishing | Finishing jobs, assembly guide for DaVinci Resolve (free), music spotting, captions, audio description, disclosure line | minutes to produce; the editing takes days | any surface |

---
## 5. The data model

### 5.1 The single source of truth and its exact syntax

**Decision.** The truth is a set of Markdown record files (the numbered project files of section 2.6) written in "record text", machine-first's line grammar with named sub-parts only. `For machines - do not edit/breakdown.json` (with `breakdown.schema.json` in C5's portable subset: every field required, `none` for empty, lowercase enums, nesting at most 3 levels) is generated on every `stage.py build`, never edited. JSON from an API structured-output run is accepted through `stage.py import-json`, which writes record text. YAML is not used (indentation; "no" read as false). CSV is an export only.

**Why.** (1) The user reads exactly what is saved, which matters most in chat apps where no view is generated. (2) Gemini can download `.md` and `.txt` but not JSON or ZIP (D1 §3.4). (3) A cut-off reply loses at most one record, caught by the END line, whereas cut-off JSON does not parse at all and D1 §6.2 says to re-request rather than repair. (4) It costs about 40% fewer tokens than JSON (machine-first measured JSON at about 1.7 times the tokens; D1 measured 609 tokens for one JSON shot) and needs no escaping around dialogue. (5) Errors are reported by record and line. (6) Flat lines meet C5 P4's nesting limit by construction.

**The grammar (all of it).**

| Rule | Text |
|---|---|
| G1 | A record file is UTF-8 Markdown. Only record headings, field lines inside a record, and the END line mean anything to the parser. Every other line (the plain part above the divider, titles, "At a glance", tables, paragraphs, the check table after a `---` line) is free text for people, kept and ignored. |
| G2 | A record starts `### <TYPE> <ID> <optional plain title>`. TYPE is an upper-case word from `schema.json`. ID matches the type's pattern (5.3). Singleton types (PLAN, STYLE, WORLD, CAMSYS, SOUNDPLAN, LADDER) have no ID: `### PLAN`. The title is free text after the ID. |
| G3 | A record runs until the next line starting with `#`, a line `---`, or the END line. |
| G4 | A field is one line: `- <field>: <value>`. Field names are lowercase snake_case plain words from the schema. The parser lowercases names and turns spaces and hyphens into underscores, so `- Screen time: 15` is read as `screen_time` and logged as a tidy fix. |
| G5 | A value is one line. Kinds: **text** (to the end of the line; ` \| ` not allowed inside); **word** (one allowed value, lowercase snake_case, compared ignoring case, spaces and hyphens read as underscores: "medium close-up" = `medium_close_up`); **number** (units are in the field name: `_s` seconds, `_m` metres, `_mm` millimetres, `_usd` dollars, `_wps` words per second); **yes_no**; **id**; **id_list** (comma separated; a comma inside double quotes does not split it); **lines** (`402, 449-463`, or a quote anchor: one quoted string for one line, or a pair `"Iona chews it." to "street signs either."` for a range); **story_point** (a moment inside a scene before its beats exist: the scene ID and a quote anchor, `SC24 "She deletes the way home."`; from step 7 a beat ID is also accepted, and code stores the beat each story point resolves to); **charge** (a value's charge: `---`, `--`, `-`, `0`, `+`, `++`, `+++`; the sign is the direction); **point** `[x, y]` or `[x, y, z]` in metres; **size** `[w, d, h]`; **span** `t0-t1` in seconds. **Quote anchors** are allowed wherever a line number is, including `line:` in `because`, STATE `from` and `cause`, RULE `era`, `evidence` items and CARDINAL `lines`; in chat without a numbered story they are required there (2.4). Each quoted string in an anchor has at least 3 words and must match exactly once in its scope: the scene's lines for a story point or a scene field, the whole story otherwise (CITE-02). |
| G6 | A repeatable field appears once per item. An item is a first part followed by named sub-parts: `- subject: CH-IONA.S02 \| at: left_third \| faces: camera \| does: chews, stops, frowns`. The first part is the item's main value, usually an ID. Sub-part keys are schema words in any order; an unknown key is an error. Positional (unnamed) sub-parts are never allowed. |
| G7 | Empty is `none`. Undecided is `open` (listed as a question). `auto` means code decides. `null`, `N/A`, `-` and blank read as missing. |
| G8 | A line inside a record starting `> ` is a note attached to it (kept, not parsed). |
| G9 | Every file ends with exactly one END line: `END OF FILE \| <what the file holds> \| <n> records`, for example `END OF FILE \| Scene 10 shots 130-200 \| 8 records`. `n` counts the file's `###` records. A missing END line or a wrong count means a cut-off reply or a dropped record. |
| G10 | Records with the same TYPE and ID in several files merge field by field (a scene's list fields in `04 Scene list.md` and its design fields in its scene file; a scene's shots across batch files). The same field with two different values is an error. Items of a repeatable field are combined and exact duplicates removed. |
| G11 | Shortening markers inside a record ("...", "…", "etc.", "and so on", "same as above", "as before", "remaining shots", "omitted for brevity", a line starting `//`) are errors, unless inside double quotes that match the story. |
| G12 | Anything inside double quotes in a field value is a quotation from the story and must be found in the record's cited lines (or the scene's lines). Story words otherwise appear only in `TEXT.words` and prose `SPEECH.text`. |
| G13 | Free-text headings use `#` or `##` only. Any line starting `###` is a record heading, and an unknown TYPE after it is FORM-01. Templates and `make_views.py` follow this. |

**Example: the turn shot of The Catch SC10** (Standard depth; the scene file continues with other records and ends with its END line):

```
### SHOT SC10-SH150 Not mint
- beats: SC10-B07, SC10-B08
- lines: 454-466
- purpose: Iona's body admits what her words denied; Saye's proof lands on her face.
- because: SC10-B07, SC10-V1, MO-MINT, CR-IONA
- role: turn
- kind: live
- setup: SC10-SU02
- frame: single
- size: close_up
- angle: eye_level
- height: eye:CH-IONA
- lens_mm: 50
- focus: moderate
- focus_on: CH-IONA
- move: static
- subject: CH-IONA.S02 | at: left_third | faces: camera | eyeline: CH-SAYE | dwell_s: 15 | does: chews slowly; stops chewing; a small frown; chews once more, slowly; then listens | tactic: discovering | energy: held | display: 1 | still: head, hands, torso | travel: none
- hear: SC10-D10 | speaker: off_screen
- hear: SC10-D11 | speaker: on_screen
- hear: SC10-D12 | speaker: off_screen
- thing: MO-MINT | emphasis: 2
- screen_time: 15
- moment: 0-4 | shows: chews slowly, eyes on Saye just right of the lens
- moment: 4-6 | shows: stops chewing; a small frown; chews once more, slowly
- moment: 6-8 | shows: says two words, unsteady
- moment: 8-15 | shows: listens, does not speak; swallows once; eyes stay on Saye
- end: still, mouth closed, eyes on Saye
- silence: room_sound_only
- music: none
- needs_description: yes
- cut_out_on: thought_complete
- why: "Her face changes." puts the turn inside her mouth, so the scene's closest frame is spent here and held while Saye's proof lands off screen, on its target.
- previs_level: 0
- storyboard: yes
- cost_class: dialogue
- origin: story
```

In chat apps without code the `hear` items also carry the words, which code later verifies (`- hear: SC10-D11 | speaker: on_screen | words: "Not mint."`), and `lines` is a quote anchor pair (`- lines: "Iona chews it." to "street signs either."`), which `adopt` turns into `454-466`.

### 5.2 Writers and origin

Every field in `schema.json` has exactly one primary **writer**, enforced by `stage.py apply`:

| Writer | Who | Rule enforced | Examples |
|---|---|---|---|
| `story` | code, copying from the story | never typed by the AI; values come from the numbered story | `heading`, scene `lines` (screenplays), speech text, `names` aliases found in cues |
| `ai` | the AI | within the allowed values; references must exist; a departure needs `why` | `purpose`, `size`, `tactic`, `fixed_description` (until locked) |
| `user` | only through a CHOICE record whose `status` is `answered` or `defaulted` (both satisfy the rule) | an AI-written value without such a CHOICE is an error; the field locks when set | `rights`, `depth`, `training_off`, `format`, `frame_shape`, `runtime_target_s`, `scope`, `music_policy`, `voice_policy`, `likeness_basis`, era lines, sides left open by the story |
| `code_state` | code, stored in the record file | the AI may not change it (FORM-10); it travels with the data, so locks survive a move between apps | `status`, `locked`, CHOICE `status` and `date`, `SHOTLIST.approved`, `source_fingerprint`, `scene_id_digits`, `checker_last_run`, SCENE `characters` and `speaking`, `target_duration_s`, `runtime_estimate`, resolved story-point beats, PREVIS stubs |
| `code_derived` | `stage.py build` only | computed on every build, never stored in record files; an AI-typed value is dropped with a warning | labels, floors, clip lengths, mirror states, image sides, eyelines, size check, face height, prompts, prices |

**Chat writers.** Where a field's value must exist in chat before any code runs, `schema.json` gives it a second flag, `chat_writer: ai` (for example `status`, `locked`, `surface`, `code_execution`, `batch_size`, SCENE `characters`, CHAPTER `first_line` and `last_line`, SCENE `heading` and `lines` written as anchors when the AI writes the scene list). FORM-10 accepts an AI-written value in such a field only in a project marked `code_execution: no`. `stage.py adopt` (7.1) later re-owns these fields: it recomputes or confirms each value, writes the code's value, and logs each difference as a note (N), never as a warning or error.

**Conditional writers.** A few fields have one writer for one kind of source and another for the rest (SCENE `heading` and `lines`: `story` for screenplays, `ai` or derived for prose; TEXT `words`: `story` when the words are in the script, `ai` with `origin: invented` otherwise; FINDING records: `code_state` when `source: checker`, `ai` otherwise). `schema.json` writes the condition as `writer_when`, so exactly one writer applies to any one value. Rows in 5.5 that name two writers name them per field ("ai; user") or per condition, never as a shared field.

**Filled by step.** Every field also carries `filled_by_step` (a step number, a checkpoint letter, or an add-on letter; for comparison a checkpoint counts as the step it closes, A as 1, P as 2, B as 5, C as 7, and add-ons come after 11), for example `PROJECT.frame_shape` → B, `SCENE.event` → 2, `CHARACTER.fixed_description` → 4, `SHOT.screen_time` → 8. FORM-05 on `check --step N` requires only fields whose `filled_by_step` is N or earlier, at the project's depth; `check --all` requires every field at the depth.

**Origin** is a separate field on content records: `origin: story | inferred | invented` (fact in the story; inferred from it with evidence; invented by the pipeline). Every `invented` element in a shot is listed in the scene's `additions`, marked whether it changes what the scene means; those that do reach the user as keep-or-cut items at checkpoint C, and the rest are kept and counted.

### 5.3 IDs

| Record | Pattern | Example | Shown to the user as |
|---|---|---|---|
| Project | 3-8 capitals | `CATCH`, `LONG` | the title |
| Scene | `SC` + 2 digits (3 when the project has more than 99 scenes; fixed per project) + optional capital letter for an inserted scene | `SC10`, `SC06A`, `SC104` | "Scene 10" |
| Part | scene + `-P` + digit | `SC10-P2` | "part 2" |
| Value | scene + `-V` + digit, declared as the first part of a SCENE `value` item | `SC10-V1` | the value's name |
| Beat | scene + `-B` + 2 digits | `SC10-B07` | "beat 7" |
| Speech | scene + `-D` + 2 digits, numbered in cue order within the scene (3 digits if a scene has more than 99); screenplay speeches live in `speeches.json`, prose speeches in SPEECH records | `SC10-D11` | the words |
| Move, setup | scene + `-M` / `-SU` + 2 digits | `SC10-M04`, `SC10-SU02` | "move 4", "camera B" (setups lettered in order) |
| Shot list | scene + `-LIST`; each list item's first part declares its shot ID | `SC10-LIST` | "the shot list" |
| Shot | scene + `-SH` + 3 digits in steps of 10; an insert takes a number between (`SH155`); 990-999 for end cards and black | `SC10-SH150` | "shot 150" in every message and view; the crew label "10Q" (letters from A at SH010, skipping I and O) appears only in the shot-list spreadsheet |
| Clip | shot + `.` + digit (`code_derived`) | `SC10-SH150.1` | "shot 150, clip 1" |
| Cut | scene + `-C` + number of the shot it follows | `SC10-C200` | "the cut after shot 200" |
| Sequence, chapter | `SQ` + 2 digits; `CP` + 2 digits | `SQ03`, `CP01` | "group of scenes 3: the wrong world" (short: "group 3"); "chapter I" |
| Strand, cardinal event, plant, fact | `ST-`, `CF-`, `PL-`, `FT-` + 2 digits | `ST-01`, `CF-05`, `PL-07`, `FT-03` | plain name |
| Named records | `CH-` character, `VO-` voice, `LOC-` place, `PR-` thing, `TX-` text in picture, `MO-` motif, `CAM-` in-story camera, `WR-` rule, `LK-` look, `CR-` character camera rule, `VS-` + sequence (visual plan) + capitals and hyphens | `CH-IONA`, `LOC-SAYE-KITCHEN`, `WR-MIRROR`, `CR-ELI`, `VS-SQ03` | plain name |
| Reserve (saved choice), lens exception | `RC-`, `LX-` + 2 digits | `RC-01`, `LX-01` | "saved choice 1", "lens exception 1" |
| State | element + `.S` + 2 digits | `CH-IONA.S02`, `PR-FLASK.S02` | "Iona, state 2: sleeve torn, palm skinned" |
| Choice, finding, review, rights | `CHOICE-`, `FIND-`, `RT-` + 3 digits; `RV-` + scene or `RV-FILM` | `CHOICE-021`, `FIND-004`, `RV-SC10` | "choice 21" |
| Set value (a structured choice answer) | choice ID + `-` + option letter | `CHOICE-014-A` | not shown (its choice is) |
| Jobs | `PIC-` + shot or state + `-` + use + `-` 2 digits; `PV-` + shot (or `PV-SC06-MASTER`) + `-V` 2 digits; `TK-` + clip + `-T` 2 digits; `VT-` + speech + `-T` 2 digits; `FX-` + shot + `-` 2 digits; `MU-` 2 digits | `PIC-SC10-SH150-START-01`, `PV-SC10-SH080-V01`, `TK-SC10-SH150.1-T03`, `VT-SC10-D11-T01`, `FX-SC10-SH080-01` | "take 3"; a previs version as "try 1" |

**Who issues IDs.** Code issues scene, chapter and speech IDs when reading the story, and pre-issues a block for everything else in each handout ("your beats: SC10-B01 to SC10-B30; your shots: SC10-SH010 to SC10-SH400 in steps of 10, use as many as you need, in order"). The AI copies them; the checker verifies them. In chat without code the step file states the same rules and `adopt` and the checker verify later. Fields whose first part declares an ID (SCENE `value`, SHOTLIST `item`) carry `defines_id: true` in `schema.json`; all other ID-shaped first parts (turn pictures, dial and ladder items) only reference one. IDs never change and are never reused; a cut record keeps its ID with `status: omitted`. `library/01 What the codes mean.md` maps every example ID in the research to the canonical one (C3's "13-04" = SC11; "09-22" and "09-15" = SC06; "11-07A/B" and "11-08" = SC07; "14-05A/B" = SC15; "18-31..33" = SC25; A1's "07" = SC13; C4's `CATCH_SC06_SH14` = `SC06-SH140`).

### 5.4 Cross-reference rules and conventions

1. Relationships are ID lists, never names. Every CHARACTER keeps its aliases in `names`; a name in a story-derived field that matches no alias is an error.
2. An ID exists when it is a record ID in some record file of the project (G10 merges across files), an ID declared as the first part of an item whose field has `defines_id: true`, a speech in `speeches.json`, a clip ID derived by code, or a PREVIS stub with `status: planned` (created by code, 8 and 9).
3. `because` accepts: beat, value, motif, plant, fact, character, character camera rule, rule, reserve, lens exception, look, visual plan, state IDs, `line:NNN` or `line: "<quote anchor>"`, or `default` (only on normal shots where REASON-02 finds no departure from the defaults in rule 11). A turn shot's `because` must include a beat whose `turn` is not `none`.
4. `subject` and `thing` items name a state ID when the element has states; the state must be valid for the scene (its `from` at or before the shot, its `until` after). A SHOTLIST item's `subject` may name the character ID instead; its SHOT names the state.
5. A locked record may gain fields it did not have; changing an existing value needs an answered CHOICE that unlocks it, and marks every record citing it stale.
6. Omitted records keep their IDs and are skipped by coverage and exports; nothing may cite an omitted record.
7. Units: seconds `_s`, metres `_m`, millimetres `_mm`; angles in degrees; set-plan coordinates in metres from a named corner, +x east, +y north, z up, written in the orientation the LOCATION's `plan_orientation` names (default: the orientation of the place's first appearance on screen); code derives the other orientation by x → W − x, θ → 180° − θ.
8. Sides: `frame_left` / `frame_right` for the picture as the audience sees it; `own: left | right` for a body; "hand nearest the camera" in behaviour text. Image-side words ("the left side of the image") are never stored in state lines or fixed descriptions; code derives them per shot.
9. Emphasis and intensity scales keep separate names and ranges and are never converted into each other (K14).
10. Enums are lowercase snake_case; `yes`/`no`; `none` for empty. `status` on every record is one of `draft | approved | stale | omitted`, plus `planned` on PREVIS stubs; CHOICE (`open | answered | defaulted`) and FINDING (`open | fixed | accepted`) keep their own lists; a VOICE stays `draft` while place and accents are undecided (8.6).
11. **Fields that need a `why` when they differ from their default** (REASON-02), with each default: `angle` eye_level; `height` the eye of the `whose_scene` character, or of the subject; `lens_mm` the camera system's `normal_lens_mm`; `move` static; `focus` moderate; `light` as_look; `room_sound` as_place; `silence` none; `music` none; `display` 1 in a close-up or tighter. `size` and `frame` never need a `why` (the dial and the list carry their reasons). Turn shots always carry a `why`.
12. A **story point** (G5) is resolved by code at step 7 to the beat whose lines contain its quote; every later check reads the resolved beat.

### 5.5 Record types and fields

Columns: **field**; **plain meaning**; **values** (`\|` separates choices; "repeat" marks repeatable fields with their sub-parts); **d** = required from depth `q` quick, `s` standard, `f` detailed, `s*` standard when the condition in the meaning holds, `m` when its module is on, `o` optional; **w** = primary writer (`story`, `ai`, `user`, `code_state`, `code_derived`; "code" alone in a row means `code_state` when the field is stored and `code_derived` when section 5.6 computes it; "(AI in chat)" marks `chat_writer: ai`). Every record also takes `status` (`code_state`, chat writer ai; values in 5.4 rule 10), `locked` (`code_state`, set by approval; chat writer ai) and `note` (repeat, free text, ai or user). `schema.json` holds the same list plus `filled_by_step`, `defines_id`, a plain label for views and one example per field; `filled_by_step` defaults to the step that designs the record type (CHARACTER → 4, even though step 1 creates its stubs; CHAPTER `digest` → 2, though step 1 creates the stub), and every exception is written per field in `schema.json` (for example `PROJECT.format` → 1, `PROJECT.frame_shape` → B, `PROJECT.runtime_target_s` → A, `PROJECT.fps` → 6, `PROJECT.genre` → 2, `SCENE.event` → 2, `CHARACTER.names` → 1, `STYLE.medium` → B, `VOICE.source` → 4).

#### PROJECT (in `00 Start here.md`)

| field | plain meaning | values | d | w |
|---|---|---|---|---|
| title | the story's title | text | q | story (from the first title-page line or title heading; the AI may propose a clean title as a small choice) |
| source_file, source_fingerprint | original file name; SHA-256 of it | text | q | code_state |
| source_kind | kind of story | screenplay \| prose \| stage_play \| treatment \| comic_script \| game_script \| mixed | q | code (AI confirms) |
| source_format | file format found | catch_dialect \| fountain \| fdx \| docx \| epub \| pdf_text \| markdown \| plain_text | q | code |
| language | the story's language | word, e.g. english | q | code |
| depth | how deep | quick \| standard \| detailed | q | user |
| surface, code_execution, batch_size | app; whether Python runs; shots per detail batch | claude_code \| claude_cowork \| claude_web \| chatgpt \| gemini \| other; yes_no; 12 \| 18 | q | code_state (AI in chat) |
| training_off | the privacy setting was turned off | confirmed \| not_confirmed | q | user (CHOICE-003) |
| rights | right to adapt the story | mine \| permission \| public_domain \| study_only \| unknown | q | user |
| intended_use | where the film goes | personal \| festival \| online_free \| online_monetised \| commercial | m | user |
| licensed_data_only | route only to models the adapter marks `licensed_data` (8.4) | yes_no (default no) | m | user |
| format | kind of finished work | short \| feature \| limited_series | q | user (CHOICE-004, step 1) |
| runtime_target_s | target length with credits | number \| as_written | q | user |
| scope | the scenes the scene work, checks, film pass, estimates and exports cover | id_list \| all (default all; for prose, the scenes of chapter I) | q | user (the length choice at A sets `all` for a screenplay; checkpoint P sets it for prose) |
| frame_shape | delivery aspect ratio | 2.39 \| 1.85 \| 16_9 \| 4_3 \| 9_16 | q | user |
| fps | frame rate | 24 \| 25 \| 30 | q | ai |
| genre, tone_home, tone_range | named genre; the film's home tone and the tones allowed anywhere (D10 §2.1) | genre word; tone word; list of tone words | q | code_state (copied from PLAN) |
| scene_id_digits | width of scene numbers | 2 \| 3 | q | code_state |
| prompt_words | word swaps in compiled prompts | repeat: `torch \| use: flashlight` | s | ai |
| previs_colours | the flat colour of each character's grey stand-in | repeat: `<CH id> \| rgb: [r, g, b]` | m | code_state |
| spend_cap_usd, hours_per_week | most any batch may spend; hours for the schedule | number \| none | m | user |
| schema_version, checker_last_run, model_facts_date | housekeeping | text | q | code_state |

#### CHOICE (`01 Choices.md`)

| field | plain meaning | values | d | w |
|---|---|---|---|---|
| question | the question in plain words | text | q | ai |
| why | why it matters, one line | text | q | ai |
| option | one possible answer | repeat: `a \| text: ...` | q | ai |
| default | the answer used if the user says "defaults", and its reason | `a \| reason: ...` | q | ai |
| answer | the user's answer | letter \| text | q | user |
| asked | shown as its own question (yes) or grouped under "small choices I made" (no) | yes_no | q | ai |
| checkpoint | where it is shown | a \| p \| b \| c \| acceptance \| d \| e \| none | q | ai |
| affects | IDs or field paths the answer changes | id_list or `SC10-SU01.lens_mm` | q | ai |
| sets | what the answer writes | repeat, one per option letter: a single word or number as `<ID>.<field> \| value: ... \| when: a`; a structured value (an item with sub-parts, or several fields) as `<SETVALUE id> \| when: a` | q | ai |
| locks | records locked on answer | id_list | o | ai |
| based_on | research references | text ("K22; B3 Ex1") | s | ai |
| status, date | open \| answered \| defaulted; when | word; date | q | code_state (AI in chat) |

**SETVALUE** (`01 Choices.md`): the full value one option writes, for answers G6 cannot hold on one `sets` line. `### SETVALUE CHOICE-014-A`, then `- target: WR-MIRROR`, then field lines exactly as they would appear in the target record (`- era: b | from: 263 | to: 1563 | frame: original`), checked against the target's record type. When the choice is answered or defaulted to that option, code copies the lines into the target and locks them.

#### SCENE: list and plan fields (`04 Scene list.md`)

| field | plain meaning | values | d | w |
|---|---|---|---|---|
| heading, int_ext, place_text, time_text | the heading and its parts | text; int \| ext \| int_ext | q | story for screenplays (AI in chat); ai when `source_kind` is not screenplay |
| lines | the scene's line range | lines | q | story for screenplays (AI in chat, as an anchor pair); code_state derived from `from_lines` otherwise |
| characters, speaking | who is present; cue counts | id_list; repeat | q | code_state (AI in chat) |
| transition_in, transition_out | joins written in the story, else a plain cut | cut \| cut_to_black \| fade_in \| fade_out \| dissolve \| smash_cut \| match_cut \| continuous | q | story |
| presentation, host | how the scene is shown; the device showing it | normal \| on_screen \| recording \| flashback \| dream \| montage \| letter; PR or CAM id | q | ai |
| event | what changes, one past-tense sentence | text | q | ai |
| sequence | its group | SQ id | q | ai |
| scene_intensity | pressure across the whole film | 1-10 (one 10 or one 10 range) | q | ai |
| whose_scene | whose point of view the scene holds | CH id | s | ai |
| story_day | which day or night | D1, N1 ... | s | ai |
| rhythm_class | the scene's pace class, used only by the estimate (never as a design target) | action_peak \| suspense \| mixed \| dialogue \| contemplative | s | ai |
| tone, tone_undercurrent | the scene's main tone and an optional second tone (D10 §2.1) | grave \| tense \| dread \| enigmatic \| comic_light \| comic_dark \| romantic \| kinetic \| lyric \| wonder \| contemplative; the same \| none | s | ai |
| tags | situations that load situation cards | dialogue_duel \| three_or_more \| action \| glass_and_reflection \| handedness \| screens_and_text \| in_story_footage \| suspense_and_reveal \| darkness \| prose_interior \| montage_and_time \| creature \| violence | q | ai |
| depth | a depth for this scene above the project's ("Go deeper on scene 13") | quick \| standard \| detailed \| none | o | user (through the request, logged as a CHOICE) |
| target_duration_s | planned seconds (the first estimate, then the plan) | number | s | code_state |
| keep, merged_into | compression decision; where a merged scene went | keep \| trim \| merge \| fold \| cut; SC id | s* when compressing | ai |
| from_lines, five_test, cardinal, strands | prose: source passage; A3's five tests; cardinal events and strands it carries | lines; five 0/1 digits; id_list | q (prose) | ai |
| origin | story \| inferred \| invented | word | q | ai |

#### SCENE: design fields (`11 Scenes/Scene NN - <place>.md`)

| field | plain meaning | values | d | w |
|---|---|---|---|---|
| location, sub_area | the place; part of it | LOC id; text | q; f | ai |
| look | the place-and-time look | LK id | s | ai |
| value | a value the scene turns (the first part declares the value ID) | repeat: `SC10-V1 \| name: ... \| core: yes_no \| open: <charge> \| close: <charge> \| turns_at: SC10-B07 \| kind: action \| revelation \| none` | q (core), s (others) | ai |
| want | what each character wants here | repeat: `CH-SAYE \| want: to ... \| hidden: ... \| holds_back: ...` | s | ai |
| driver, conflict, third_thing | who drives; kind of conflict; what they fight through | CH id; balanced \| asymmetric \| indirect \| comic \| minimal \| reflexive; text | s | ai |
| staging | one line placing everyone, with 2-4 named stations in a scene over 8 beats; "staging assumed" when the story is silent | text | s | ai |
| start | where each character stands at the scene's start | repeat: `<CH id> \| at: <mark or point> \| faces: <id or point> \| posture: standing \| seated \| lying \| kneeling` | s* set plan exists | ai |
| scene_idea | the scene in one sentence as a director sees it, naming the at most two departments that change at the main turn | text | s | ai |
| department_idea | one idea each; holding the baseline is a full answer | repeat: `camera \| light \| staging \| sound \| design` + `\| idea: <text> \| holds_baseline` + `\| because: ids` | s | ai |
| turn_picture | the frame each turn must show, written before shots | repeat: `SC10-B07 \| picture: one sentence` | q | ai |
| dial | per beat, how close and how loud | repeat: `SC10-B07 \| size: \| distance_m: \| height: \| light: \| sound:` (`light` defaults to `as_look` and `sound` to `room_sound`; change them only where a story source can, B2 R10, or at the rupture) | s | ai |
| coverage | how the scene is covered | designed \| chained \| master_and_coverage \| oner | s | ai |
| rhythm_shape, target_asl_s | the shape of the cutting; average shot length (set from the rhythm shape, the tone and card 13, never from `rhythm_class`) | build_and_cut_out \| build_rupture_aftermath \| slow_burn \| steady; number | s | ai |
| rupture | the one break in the pattern | `SC10-B07 \| device: hold \| drop_out \| true_silence \| cut_to_black \| camera_change \| pov_change \| breaks: ...` | s | ai |
| tone_shift | a change of tone inside the scene, on a turn or a drop (D10 TN2) | `<beat> \| from: \| to: \| device: size_ladder \| light_cue \| music_in \| music_out \| camera_behaviour` \| none | s | ai |
| room_sound | the steady background sound here | as_place \| text | s | ai |
| geography, cause_chain, escalation, reversal, action_score, time_treatment | action scenes (card 15, D11): the action score is a text block, one row per count, one column per body, the set and the camera | text; text; text; beat ids; text; real_time_continuous \| held_real_time \| overlapping_slices \| elliptical \| slow_motion (only where the camera system allows it) | s* action | ai |
| departure | a scene-level break from a film rule | repeat: `<rule ID> \| what: ... \| why: ...` | s | ai |
| additions | inventions awaiting keep or cut | repeat: `<what, or an id> \| changes_meaning: yes_no` (yes for a new object, or a new move at a turn) | s | ai |
| flags | scene-level faults found, never fixed (line-level faults are BEAT `flag`) | nonevent \| splintered \| turn_too_soon \| turn_too_late \| continuity | s | ai |

Code derives on SCENE: `era`, `frame_handedness`, `switch_at`, states in play, `duration_est_s`, label, and each story point resolved to a beat.

#### PART, BEAT, SPEECH, MOVE, SETUP

| type | field | plain meaning | values | d | w |
|---|---|---|---|---|---|
| PART | beats, turn, starts | beats in the part; its turn beat; how it starts | id range; beat id \| none; scene_start \| after_drop \| without_drop | s | ai |
| BEAT | lines | lines it covers | lines | q | ai |
| BEAT | action, reaction | who does what to whom, as tactics | `CH-SAYE \| tactic: proving` | s | ai |
| BEAT | task | what the hands do | repeat: `CH-IONA \| does: chews the leaf` | s | ai |
| BEAT | beat_intensity | pressure inside the scene | 1-5 (at most two 5s per part) | s | ai |
| BEAT | turn, turn_kind | whether a value turns here | none \| turn \| main_turn; action \| revelation | q | ai |
| BEAT | charge | each value's charge after the beat | repeat: `SC10-V1 \| charge: <charge>` | s | ai |
| BEAT | flag | a flaw in one line, flagged, never fixed (A1) | repeat: `on_the_nose \| melodrama \| forced_exposition \| monologue \| repetitious \| can_play_silent \| interrupted` + `\| line: <speech ID>` | s (when found) | ai |
| BEAT | engaged_pair, silent_third | in a three-person scene, the two engaged and the witness (B3 R25, A1 R5) | `CH-A, CH-B`; CH id | s* tag `three_or_more` | ai |
| BEAT | five_steps | desire, obstacle, choice, action, expression as visible moments | repeat: `desire \| shows: ...` (five items) | s* turns and intensity 4+ | ai |
| BEAT | landing_face | who the audience watches when the line lands | CH id \| `insert:<ID>` \| wide | s* turns, flagged lines, revealed facts, refusals; f all | ai |
| BEAT | unsaid, carrier | what a character thinks and does not say; what makes it seen or heard | `CH-IONA \| thought: ...`; ID or text | s* turns; f all | ai |
| BEAT | pause_after | the pause after the beat | `none \| short \| medium \| long \| hold` + `\| seconds: \| picture: hold \| push_in \| cut \| cut_wide \| sound: ...` (`hold`, above 4.0 s, needs a saved choice) | s | ai |
| BEAT | emphasis, added_emphasis | how loud things are; extra signal on this beat | repeat: `MO-MINT \| level: 0-3`; `0 \| 1` + `\| what: ...` | s | ai |
| BEAT | change | the configuration change on a turn | text | s* turns | ai |
| BEAT | distance, core_word, cut_rule, fact | detailed dialogue and staging detail | `CH-A CH-B \| metres: \| zone: intimate \| personal \| social \| public`; text; cut_on_core_word \| cut_early_split \| hold \| no_cut_two_shot; FT ids | f | ai |
| SPEECH | speaker, line, text, parenthetical, extension, path, origin | one spoken line: screenplays are read by code into `speeches.json`; prose lines are written by the AI in the scene file | CH id; line number; exact words; text; text; direct \| off_screen \| earpiece \| radio \| intercom \| phone \| device_speaker \| recording \| helmet_inside \| helmet_outside \| through_glass \| voice_over \| thought; story \| adapted \| invented | q | story (screenplay), ai (prose) |
| MOVE | beat, who, from, to, via, start_s, dur_s, faces, posture, why, origin | a move on the set plan (a "floor-plan move" to the user, never a camera move); `start_s` counts from the start of the first shot that shows its beat | beat id; CH id; mark or point; point; point; number; number; ID or point; standing \| seated \| lying \| kneeling (the posture at the end); text; word | s* set plan; f | ai |
| SETUP | at or at_words, look_at, lens_mm, use, side, mount | a camera position | point \| text; point; number; text; a \| b (side of the line); world \| ID | s | ai |

#### SHOTLIST (the one-line list, in the scene file)

| field | plain meaning | values | d | w |
|---|---|---|---|---|
| item | one planned shot (the first part declares the shot ID) | repeat: `SC10-SH150 \| beats: SC10-B07, SC10-B08 \| role: turn \| size: close_up \| frame: single \| subject: CH-IONA \| time: 15 \| shows: Iona chews, stops, chews once more; "Not mint."; we stay on her through Saye's answer` | q | ai |
| approved | the user passed checkpoint C, or it was reported without changes | yes_no | q | code_state (AI in chat) |

At Quick depth the list items are the final shots. At Standard and Detailed each item becomes a SHOT with the same ID, beats, role and size.

#### SHOT

| group | field | plain meaning | values | d | w |
|---|---|---|---|---|---|
| story | beats, lines | beats and lines it shows | id_list; lines | q | ai |
| story | purpose | what the audience must get from it | one sentence | q | ai |
| story | because | the records that justify it | id_list (5.4 rule 3) | q | ai |
| story | role | how much the scene depends on it | turn \| must_keep \| normal | q | ai |
| story | kind | kind of shot | live \| insert \| pov \| screen \| card \| black | q | ai |
| story | why | the story reason for any value on the list in 5.4 rule 11 that departs from its default, or for any departure from the camera system; always on turn shots | one sentence quoting a line, naming an object or action, or citing an ID | s | ai |
| story | origin, additions | source of the content; inventions in frame | story \| inferred \| invented; id_list or text | q; s | ai |
| story | pov_break | why the shot leaves the whose-scene character's place or knowledge (A3 rule 37) | text | s* when used | ai |
| camera | setup | camera position | SETUP id | s | ai |
| camera | frame | who is framed | single \| two_shot \| three_shot \| group \| over_shoulder \| pov \| near_pov \| empty | q | ai |
| camera | frame_detail | framing variant | clean \| dirty \| symmetrical_profile \| none | f (s when reserved) | ai |
| camera | size | shot size | extreme_wide \| wide \| medium_wide \| medium \| medium_close_up \| close_up \| extreme_close_up \| insert | q | ai |
| camera | angle | tilt of the camera | eye_level \| low \| high \| top_down \| worms_eye (dutch only when reserved) | q | ai |
| camera | height | whose eye height, or metres | `eye:CH-IONA` \| `seated:CH` \| `kneeling:CH` \| floor \| number | s | ai |
| camera | lens_mm, focus, focus_on | lens (full-frame); depth of field; what is sharp | number; deep \| moderate \| shallow; id | s | ai |
| camera | move, move_reason | the one camera move and its cause | static \| pan \| tilt \| push_in \| pull_back \| sideways \| rise \| lower \| follow \| lead \| handheld \| crane (orbit \| zoom \| whip_pan \| dolly_zoom \| drone only when reserved); text | q; s | ai |
| camera | mount, stance | what the camera is fixed to; its stance | world \| carried \| ID; objective \| pov \| near_pov \| direct_address | f | ai |
| picture | dominant, placement, layers, frame_in_frame, device | what is seen first; where; foreground, middle, background; frame within frame; at most one expressive device | text; thirds \| centre \| edge; text; text; text \| none | f (at Standard code derives `dominant` from `focus_on`, `role` and the first `subject`) | ai |
| picture | glass | every glass surface in frame | repeat: `<surface> \| state: clear \| marked \| reflecting \| screen \| broken_open \| camera: through \| along \| angled` | s* glass in frame | ai |
| people | subject | who is in frame, where, facing, doing | repeat: `<state id> \| at: left_edge \| left_third \| centre \| right_third \| right_edge \| faces: frame_left \| frame_right \| camera \| away \| up \| down \| <id> \| does: <visible behaviour> \| tactic: <-ing> \| energy: still \| held \| rising \| breaking \| spent \| display: 1 \| 2 \| 3 \| still: head, eyes, mouth, hands, torso, whole_body \| eyeline: <id or direction> \| dwell_s: <seconds> \| travel: frame_left \| frame_right \| up \| down \| toward_camera \| away \| none \| must_not: <a visible behaviour saved for a later beat> \| continues: <shot id>` (`does` from q; `at`, `faces` from q where no set plan exists, otherwise projected by code and optional; `tactic`, `energy`, `display` (1 contained, 2 visible, 3 open; D15), `still`, `eyeline`, `travel` (required when the subject moves; defaults from SEQUENCE `travel`, derived from MOVE records with a set plan) from s; `dwell_s` s when `eyeline` is set; `must_not` s* when a later beat saves the behaviour, for example SC13's Eli "Now he looks at her."; `continues` f) | q | ai |
| things | thing | register items in frame and how loud | repeat: `<id or state> \| emphasis: 0-3 \| at: ... \| plant: <PL id> \| payoff: <PL id>` (`plant` or `payoff` on the shot that plants or pays off a PLANT; FILM-02 and CRAFT-08 read these links) | s | ai |
| things | text | text in picture in frame | TX id_list | s | ai |
| things | keep_hidden | what stays out of view, the fact it protects, and how | repeat: `<FT id> \| how: frame_edge \| focus \| dark \| obstruction \| timing \| sound_first` | s* when a FACT's element is in the scene before its reveal | ai |
| things | must_show, must_not_show | what must or must not appear | id_list; id_list | s | ai |
| things | physics_note, motion | deliberately wrong physics as visible evidence (words for prompts); structured physical motion the free-fall helper reads | text; repeat `free_fall \| object: <id> \| from_z: 9.2 \| to_z: 2.53 \| start_frame: 1` | s* when used | ai |
| light | light, light_cue | light if not the look; a change during the shot | as_look \| text; `what \| when: \| why:` | s | ai |
| light | dark, eye_light | what stays dark; a catchlight | text; yes_no | f | ai |
| sound | hear | a speech heard in the shot | repeat: `SC10-D11 \| speaker: on_screen \| off_screen \| hidden \| path: <path> \| at: <seconds> \| words: "..."` (`words` only in chat; `path` only to override the speech's path; `at` optional, the speech's start inside the shot, used by captions) | q | ai |
| sound | effect | a sound tied to an action | repeat: `<what> \| at: <seconds> \| sound_emphasis: 0-3` | s | ai |
| sound | room_sound, silence, music | background; silence grade; music | as_place \| text; none \| room_sound_only \| drop_out \| true_silence; none \| MU id | s | ai |
| sound | needs_description | the beat carries story with no sound (audio description) | yes_no | s | ai |
| time | screen_time | used length on screen, seconds | number | q | ai |
| time | moment | a timed visible change inside the shot | repeat: `0-1.5 \| shows: ...` | s | ai |
| time | start, end | how it opens (from the previous shot); the last picture | text \| `from_end_of: <shot>`; text | f (s for `from_end_of` when the join is a match cut or the scene is continuous action); s | ai |
| time | cut_in_on, cut_out_on | why the cut falls here | action \| look \| line \| sound \| rhythm \| reveal; thought_complete \| action_midpoint \| line_end \| sound_hit \| rhythm \| withholding | f; s | ai |
| time | time_slice | frames of a master previs this shot covers (`overlapping_slices`) | `PV-SC06-MASTER-V01 \| frames: 12-40` (code creates the PREVIS stub, `status: planned`, if it does not exist) | s* overlapping slices | ai |
| making | held | the meaning depends on not cutting inside this shot, so it is never split into chained clips (8.4) | yes_no (default no; turn shots and shots in a `oner` scene count as held) | s | ai |
| making | previs_level, storyboard | previs rung (C4); make a frame | 0-5; yes_no | s | ai |
| making | framing_critical, pose_critical | meaning depends on exact framing; a declared pose is needed | yes_no | s; f | ai |
| making | route | how to make it | auto \| text \| start_picture \| start_end_pictures \| references \| guide_video \| performance_transfer \| still_with_move \| composite_only | s (default auto) | ai |
| making | model | override of the scene model | `none` or `<model id> \| why: ...` | o | ai |
| making | flip | author override of the mirror route | auto \| never | s | ai |
| making | content_flags, policy_route | sensitive content and how it is made (D4) | violence_implied \| violence_onscreen \| weapon_visible \| gunfire \| blood_small \| gore \| nudity \| minor_present \| self_harm \| drug_use \| real_person \| real_brand \| fire \| none; as_written \| restated \| split_cause_reaction_aftermath \| composite_element \| sound_only \| cut | s | ai |
| making | cost_class, reuse_of | the work the shot needs (D13); an approved shot it reuses | graphic \| reuse \| still_move \| easy \| dialogue \| hard; shot id \| none | s | ai |
| making | departure | a change forced by a tool, with the meaning it keeps | repeat: `<slot> \| from: \| to: \| because: feasibility \| meaning_kept: ...` | s* when used | ai |
| making | gen_note | an instruction to the compiler the fields cannot express | text | o | ai |

Code derives on SHOT (never typed): `label`; `min_screen_time_s` and its reasons; `clips` (lengths per model, handles); `era` and per-element `mirror_state`; `mirror_route`; `post_ops`; image side and prompt side of every sided feature in frame; eyeline sides; frame placement and facing from the set plan (when one exists); `size_check` from lens and distance; `face_height` (fraction of frame height); `lip_sync` (none \| loose \| tight); `dominant` at Standard; `needs` tags; `scene_model`, `suggested_model`; the generation spec, prompts, lint result, resolution, safe band and cost.

#### CUT (only where the join is not a plain cut)

| field | plain meaning | values | d | w |
|---|---|---|---|---|
| to | the next shot | shot id | s | ai |
| type | kind of join | j_cut \| l_cut \| match_cut \| jump_cut \| smash_cut \| dissolve \| fade \| cut_to_black \| freeze \| continue | s | ai |
| split_s, black_frames | sound lead or lag; frames of black | number | s* | ai |
| sound_across | what sound carries over the cut | text | s* | ai |
| shared_geometry | previs both shots are built from (match cuts) | PV id (code creates the PREVIS stub, `status: planned`, if it does not exist) | s* match_cut | ai |
| why | the reason for the join | text | s | ai |

#### Story plan records (`05 Story plan.md`)

| type | field | plain meaning | values | d | w |
|---|---|---|---|---|---|
| PLAN | logline, theme_question | the story in one sentence; the question the film asks | text | q | ai |
| PLAN | core_value, core_opposition | the value at stake; two nouns in opposition | `name \| positive: \| negative:`; text | q; s | ai |
| PLAN | crisis | the decision that forces the climax | story point: `SC24 "She deletes the way home."` | q | ai |
| PLAN | climax | the scene or scenes where the core value turns for the last time | scene id or range | q | ai |
| PLAN | act | acts | repeat: `<name> \| scenes: \| turn: <story point>` | s | ai |
| PLAN | peak | where each component peaks, with a reason when away from the climax | repeat: `story \| crisis_choice \| colour \| contrast \| tightest_size \| longest_hold \| loudest_sound \| motif_payoff \| camera_break \| sound_rupture` + `\| scene: \| reason:` | s | ai |
| PLAN | pov_plan | default viewpoint and declared breaks | `default: CH \| breaks: ...` | s | ai |
| PLAN | genre, tone_home, tone_range, tone_mix_rule | the genre; the film's home tone; tones allowed anywhere; how tones mix (D10 §9); copied to PROJECT | word; tone word; list of tone words; text | q (genre, tone_home), s (rest) | ai |
| PLAN | plan_option | prose macro plans before checkpoint P | repeat: `A \| format: \| runtime_s: \| scenes: \| shots: \| keeps: \| cuts: \| loses:` | q (prose) | ai |
| PLAN | loses, op | what the audience loses; each adaptation operation | text; repeat: `trim \| merge_scenes \| fold_into \| composite_character \| move_line \| move_plant \| delete_strand \| reorder \| invention \| replace \| flashback_import \| lost_resonance` + `\| what: \| from: \| to: \| why:` | s* compressing or prose | ai |
| PLAN | runtime_estimate, scene_budget, shot_budget | from D13 v0 and D2 R7 | numbers | q | code_state |
| SEQUENCE | title, scenes, story_job, value_change, act, scene_intensity, travel | one group of scenes | text; range; text; text; name; range; left_to_right \| right_to_left \| up \| down \| none | q (title, scenes, value_change), s (rest) | ai |
| PLANT | what, planted_at, paid_off_at, plant_emphasis, payoff_emphasis, rhyme, motif | a plant and its payoff; the shots that plant and pay off name it on their `thing` items (`plant:`, `payoff:`) | text; story point; story point; 0-3; 0-3; `yes \| framing: ...` \| no; MO id | s | ai |
| FACT | what, element, audience_knows_from, known_by, mode | who knows what, from when; `element` names what would give the fact away in frame | text; id_list; story point; repeat `CH \| from: <story point>`; suspense \| mystery \| surprise \| dramatic_irony | s* mode suspense, mystery or dramatic_irony (about 5-15 in a film); f all | ai |
| CHAPTER | title, lines, words, first_line, last_line | a prose chapter; its first and last lines quoted as proof it was read | text; lines; number; quote anchors | q | story (title, lines, words; AI in chat as anchors), ai (first_line, last_line) |
| CHAPTER | digest, people, places, time_markers, pov | at most 350 words | text; id_list; text; text; CH id | q | ai |
| CHAPTER | candidate | a candidate scene | repeat: `<working title> \| lines: \| kind: dramatized \| narratized \| inner \| summary \| iterative \| letter \| description \| tests: 1 1 0 1 1 \| decision: own_scene \| fold \| montage \| voice_over \| cut \| becomes: SC05` | q | ai |
| STRAND | name, chapters, carries, feeds, decision, reason, seconds | a line of events through the work | text; CP ids; CF ids; text; keep \| compress \| composite \| fold \| cut; text; number | q (prose) | ai |
| CARDINAL | event, lines, depends | an event the story cannot lose | past-tense sentence; lines (or an anchor pair); CF ids | q (prose, compression) | ai |

#### World and style (`06 World and style.md`)

| type | field | plain meaning | values | d | w |
|---|---|---|---|---|---|
| STYLE | medium | what the film is made to look like | live_action \| 3d_animation \| 2d_animation \| stop_motion_look \| painted \| mixed | q | user |
| STYLE | style_words | 8-15 plain descriptors pasted into every prompt | text | q | ai |
| STYLE | texture | film texture | repeat: `grain \| halation \| lens_character \| softness \| cadence` + `\| as: ...` | s | ai |
| STYLE | named_reference_policy, words_to_avoid | never name films, directors, living artists in prompts | describe_qualities_only (fixed); text | q | code_state; ai |
| STYLE | style_picture | a picture fixing the style (chosen by D5's three-direction test) | file | m | ai |
| STYLE | provisional | the style was chosen from words only and awaits D5's picture test | yes_no (default yes) | q | code_state |
| WORLD | place, period, drives_on, language | where, when, road side, the language spoken | `named:<country>` \| invented \| unstated; text; left \| right \| none; word | q | user (place, period via CHOICE), ai (drives_on, language) |
| WORLD | accents, signage, emergency_lights, institutions, money | the local signals (D17, B2 R19) | text; text; text; text; text | s | ai |
| WORLD | evidence, origin | lines that point to the locale | repeat `<line or anchor> \| quote: "..."`; word | s | ai |
| RULE | kind, statement, governs | a story-world rule and what it governs | world \| mirror \| text \| titles \| device \| other; text; id_list | q | ai |
| RULE | era | a stretch under one frame handedness | repeat: `a \| from: <line or anchor> \| to: <line or anchor> \| frame: original \| reversed` | q (mirror rules) | user (via a CHOICE and its SETVALUE records) |
| RULE | exception | an element that breaks the rule | repeat: `<id> \| reads: normal \| mirrored \| why:` | s | ai |
| RULE | occurrences, policy, template_setup, varies | recurring devices (D2) | lines; open_only \| open_and_close \| every_return \| episode_cold_open \| template_refrain; shot id; text | q (device rules) | ai |

#### Characters, places, things (`07`, `08`)

| type | field | plain meaning | values | d | w |
|---|---|---|---|---|---|
| CHARACTER | names | aliases | text list | q | story |
| CHARACTER | tier, role | principal \| minor \| extra \| non_human; role in the story | word; text | q | ai |
| CHARACTER | life_want, arc, thesis | what they want in life; start, end, turning scene; the design idea in one sentence | text; `start: \| end: \| turning_scene:`; text | s | ai |
| CHARACTER | evidence | lines the design rests on | repeat: `<line or anchor> \| quote: "..."` | s | ai |
| CHARACTER | fixed_description | the words pasted into every prompt with them | 25-40 words (principal), 20-30 (minor); visible nouns only; no expression; no real person | q | ai (then locked) |
| CHARACTER | height_m, build, colour_identity, tempo, speech | body; colour; pace; how they talk | number; text; text; text; `sentences: \| contractions: yes_no \| vocabulary:` | s | ai |
| CHARACTER | lineup | the six lineup columns as words, so code can compare principals (B5 R3; CRAFT-20) | `height: short \| average \| tall \| mass: slight \| average \| heavy \| shape: round \| square \| triangle \| long \| value: dark \| mid \| light \| colour: <one colour word> \| tempo: slow \| medium \| fast` | s (principals) | ai |
| CHARACTER | face, movement, gesture, status, distance | the face's three largest distinguishers (B5 R21); home, stress and break effort, each as body part, direction, speed and what stays still (B5 §5.1-5.4); one signature gesture with its script line (R17); default status and the beats where it flips (R15-R16); default and closest distance in metres, with the scenes that change them (§5.5) | text; repeat `home \| stress \| break` + `\| part: \| direction: \| speed: \| still:`; `<text> \| line: <line or anchor>`; `default: high \| equal \| low \| flips: <story points>`; `default_m: \| closest_m: \| changes: <scene ids>` | s (principals); f all | ai |
| CHARACTER | one_image, expression | the one image that sums them up; expression range | text; text | f | ai |
| CHARACTER | skin_light | how their skin is lit and named in prompts, written when casting is chosen (B2 R24); added to the look block of every LOOK with contrast high or extreme | text | m (add-on C, once casting is chosen) | ai |
| CHARACTER | voice, likeness_basis, consent | their voice; source of face and voice; consent record | VO id; invented \| self_consented \| performer_consented (default invented, a small choice at step 4); RT id \| none | s; q; m | ai; user; user |
| VOICE | character, voice_description | the fixed words for the voice (30-50 words) | CH id; text | s | ai |
| VOICE | pitch, pace_wps, accent | pitch band; words per second; accent from WORLD | low \| low_mid \| mid \| mid_high \| high; number (default 2.5); text | s | ai |
| VOICE | path_sound | how a path sounds | repeat: `earpiece \| radio \| intercom \| recording \| helmet_inside \| phone \| through_glass \| treatment: ...` | s | ai |
| VOICE | source | how the voice is made (D3) | designed \| user_recorded \| actor_recorded \| own_clone \| consented_clone \| native_draft (default designed, a small choice at step 4; asked again at add-on C) | s | user |
| VOICE | consent, tool, provider_voice, texture, habits | the rest of how it is made (D3) | RT id; text; text; text; text | m | ai |
| LOCATION | headings, story_job, loudness, room_sound, anchor, exit, dressing | the place | text; text; loud \| quiet; text; text; repeat `<name> \| leads_to:`; text | s | story (headings), ai |
| LOCATION | plan_orientation | the orientation the set plan is written in | original \| reversed (default: the orientation of the place's first appearance on screen) | s* set plan | ai |
| LOCATION | size, origin_corner, axes, wild_walls, object, mark | the set plan in metres, in `plan_orientation` | size; text; text ("+x east, +y north"); text; repeat `<NAME> \| at: [x, y] \| size: [w, d, h] \| base: <z> \| material: \| meaning: \| furniture: seat \| bed \| none`; repeat `<NAME> \| at: [x, y]` | s* (4, step 4 rule); f all | ai |
| PROP | names, category, kind, fixed_description, real_size, surface, side, text, first_seen, motif | a thing | text; hero_prop \| prop \| set_dressing \| vehicle \| animal \| weapon \| consumable \| document \| wardrobe \| practical_effect \| visual_effect; emblem \| action \| plot_machinery \| dressing; text; size; ordinary \| matte_black \| clear \| shiny \| very_bright; repeat; TX ids; lines; MO id | q (names, category), s (rest), f (kind, surface) | story, ai |
| TEXT | kind, words, on, reader, plot_critical, emphasis, method, look, animation, translate | readable words in picture | sign \| label \| stencil \| screen \| visor \| wrist \| monitor \| document \| title_card \| caption \| timestamp; exact words; id; CH id; yes_no; 0-3; composite \| background_blur; text; none \| text; yes_no | q (kind, words, on), s (rest), f (look, translate) | story (words in the script), ai |
| MOTIF | meaning, rank, channel, appearance, signature | a thing that returns and gathers meaning | text; spine \| supporting \| single_scene \| minor \| plot_machinery; visual \| sound \| body; repeat `<scene or story point; a shot from step 8> \| role: plant \| develop \| teach \| reveal \| payoff \| coda \| emphasis: 0-3 \| sound_emphasis: 0-3 \| rhyme_with: <id>`; text (sound rhythm) | s | ai |
| MOTIF | direction, pole, test_score, rule, largest_payoff | full-depth register (B4) | text; text; 0-6; repeat; yes_no | f | ai |
| CAMERA | at, lens_mm, ratio, fps, overlays, moves, master_clip | a camera inside the story | point \| text; number; text; number; text; never \| pan_only \| operator; shot or PV id | s | ai |

#### Continuity (`09 Continuity.md`)

| field | plain meaning | values | d | w |
|---|---|---|---|---|
| element | whose state | CH, PR or LOC id | q | ai |
| from | where it starts | `SC06 \| line: 263` (in chat `SC06 \| line: "Her eyes open."`) | q | ai |
| cause | the line that causes it | `<line or anchor> \| quote: "..."` | s | ai |
| state_line | words appended after the fixed description in prompts | text, no image-side words | q | ai |
| changes | what differs from the last state | text | s | ai |
| side | sided features in this state | repeat: `<feature> \| own: left \| right \| plot: yes_no` | s | ai |
| handedness | story state in a mirror story | original \| reversed | s* mirror rule | ai (user confirms at B) |
| pictures_needed | reference views needed | text | m | ai |
| origin | story \| inferred \| invented | word | q | ai |

Code derives `until` (the next state's start) and states in play per scene.

#### Film rules (`10 Film rules.md`)

| type | field | plain meaning | values | d | w |
|---|---|---|---|---|---|
| CAMSYS | frame_shape_why | story reason for the frame shape | text | s | ai |
| CAMSYS | lens_type, lens_family, normal_lens_mm, step_change | lens type; lenses allowed; the normal lens, the default for `lens_mm` (5.4 rule 11); when the family changes | spherical \| anamorphic; mm list; number from the family; repeat `from: <scene> \| family: <mm list> \| why:` | s | ai |
| CAMSYS | default_height, default_move | the baseline | text; static | q | ai |
| CAMSYS | banned | choices this film never makes | repeat: `<choice> \| why:` | q | ai |
| CAMSYS | camera_speed, break, time_rule | real-time playback; the camera's one break; how expanded action is built | real_time; `<scene or story point> \| what: \| because:`; text | q; s; s | ai |
| CAMRULE | character, in_control, losing_control, never, closest, limit_before, eyeline, because | how the camera treats one character | CH id; text; text; list; `<size> \| at: <story point>`; size; text; ids | s | ai |
| RESERVE | choice, match, max_uses, allowed_in, never_on, because | a saved choice (a choice saved for special moments) | text; `<field> = <value>` \| manual; number \| 1_per_scene \| share (a fraction of scenes); ids or text; ids; ids | q | ai |
| LENS | mm, only_in, why, because | a lens exception | number; ids (setups, scenes); text; ids | s | ai |
| LOOK | for, time, look_block | the look of a place at a time; the 2-3 sentences (at most 60 words) pasted into every prompt there | LOC id; text; text | s | ai |
| LOOK | main_light | the main light, placed in the room so its frame side is derived per shot and era | `<source> \| colour: \| quality: hard \| soft \| from: <a set-plan object NAME, or a compass wall: north_wall \| east_wall \| south_wall \| west_wall \| ceiling>` (with neither, the light side is `open` and prompts omit it) | s | ai |
| LOOK | neutral_white, contrast, fill, stays_dark, palette, accent_allowed, light_cue, style_picture | the rest of the lighting plan | text; low \| medium \| medium_high \| high \| extreme; none \| low \| medium \| high; text; text; text; repeat `<story point> \| change: \| why:`; file | s (m for picture) | ai |
| VISUAL | sequence, frame_value, saturation, temperature, dominant, accent, main_light, contrast, exit | the colour-script row for a sequence | SQ id; 1-5; 1-5; warm \| neutral \| cool \| mixed; colour word; colour word \| none; hard \| soft \| mixed; low \| medium \| medium_high \| high \| extreme; text (how the sequence hands on to the next) | s | ai |
| VISUAL | sub_row | a scene-level colour row inside the sequence | repeat: `SC10 \| frame_value: 1-5 \| saturation: 1-5 \| temperature: \| dominant: \| accent: \| contrast:` | f | ai |
| VISUAL | space, component, counterpoint | the visual-structure plan | deep \| flat \| limited \| ambiguous; repeat `space \| line \| shape \| tone \| colour \| movement \| rhythm \| plan: hold \| progress \| contrast \| why:`; none \| text | s | ai |
| SOUNDPLAN | music_policy | music in the finished film | none \| sparse \| scored \| source_only | q | user |
| SOUNDPLAN | clip_audio, voice_policy | no music in any clip (fixed); how voices may be made | fixed text; designed_only \| designed_plus_own_clone \| designed_plus_consented_clones (default designed_only, a small choice at step 6; asked again at add-on C) | q | code_state; user |
| SOUNDPLAN | device_budget, rupture_plan, loudness_target | editor-made devices allowed; planned ruptures; delivery loudness | repeat `cut_to_black \| true_silence \| freeze \| max:`; repeat `<scene> \| device:`; text | s; s; f | ai |
| LADDER | rung | each scene's main turn: planned size and hold; the ladder escalates by size and hold together | repeat: `SC10 "Her face changes." \| size: close_up \| hold: long \| why:` (a story point; code adds the resolved beat at step 7) | s | ai |

#### Review and jobs

| type | field | plain meaning | values | d | w |
|---|---|---|---|---|---|
| FINDING | record, rule, evidence, fix, source, status, reason | a problem found, with its fix | id; check ID or question; text; text; checker \| film_pass \| review \| user; open \| fixed \| accepted; text | q | `writer_when`: code_state when `source: checker` (except `status` and `reason`, ai), ai otherwise |
| REVIEW | scope, answer, score | judge answers and rubric scores | scene id \| film; repeat `<question> \| answer: yes_no \| evidence:`; repeat `<criterion 1-10> \| score: 0-3 \| evidence:` | s | ai |
| PIC | for, use, moment, model, references, file, checks, approved, cost_usd | one picture job: the shot or element state it is for | id; storyboard \| start \| end \| pinned \| reference \| plate \| style \| layout; start \| middle \| end; exact name; repeat `<file> \| job: identity \| costume \| set \| prop \| layout`; file; repeat `<question> \| answer:`; yes_no; number | m | ai / user (approved); the AI sets storyboard frames approved when every check passes, and the user names only frames to redo |
| PREVIS | for, level, standin_level, route, extras, stills, approved | one previs job: its shot, master (`PV-SC06-MASTER`) or location; C4 level; stand-in detail; the route into video (C4 §6: 1 start and end pictures from grey stills, 2 depth guide video, 3 grey reference video, 5 layers composited) | id; 0-5; 1-5; 1 \| 2 \| 3 \| 5; file; frame list; yes \| no \| auto (auto: not framing-critical, `BLOCKING OK` and facings within 20°) | m | ai / user (approved); code_state for stubs (`status: planned`); code_derived plan_file, blocking |
| TAKE | clip, model, route, inputs, seed, settings, cost_usd, file, review, kept, refusals | one generated take | clip id; exact name with date; text; files; number; text; number; file; repeat `<question> \| answer: \| evidence:`; yes_no; number | m | ai / user (kept) |
| VOICETAKE | speech, voice, delivery, tts_text, tool, file, verdict, cost_usd | one voice take | speech id; VO id; up to 8 words; same words with tags; text; file; pick \| keep \| reject; number | m | ai (verdict: user); code_derived `words_match` |
| FINISH | shot, operation, tool, inputs, output, done | one finishing job (created from shots by code, edited by the AI) | shot id; flip \| composite \| crop \| speed \| upscale \| deflicker \| grain \| grade \| title \| lip_sync \| voice_path; text; files; file; yes_no | m | code_state (shot, operation); ai (tool, inputs, output, done) |
| MUSIC | in, out, function, must_not, source, licence | a music cue (only if the policy is sparse or scored) | shot or beat ids; text; text; score \| library \| ai; RT id | m | ai |
| RIGHTS | subject, status, holder, licence, evidence, commercial_ok, attribution, disclosure | a rights or licence record (D4) | source \| voice \| likeness \| music \| font \| stock \| model_terms; text; text (kept locally); file name; text; yes \| no \| check; text; text | q (source), m (rest) | user (subject, status, holder, licence, commercial_ok); ai (evidence, attribution, disclosure) |

### 5.6 What code derives (never typed by the AI)

| Derived | How |
|---|---|
| Labels and counts | crew labels ("10Q"), eighths, words per speech and character, speaking counts, coverage map |
| Speech records (screenplays) | from cues in order within each scene; path from extension and parenthetical |
| Shot time floor | Written as code: `floor = max(speech_floor, text_floor) + pause_owed`. `speech_floor` = the sum, over the shot's `hear` items, of (words ÷ the speaker's `pace_wps` + 0.5 s). `text_floor` = the largest, over TEXT in frame, of max(2.0, 1.0 + characters ÷ 13), or at least 2.0 + 0.5 × words when its emphasis is 2 or more; doubled if mirrored. `pause_owed` = the sum, over the beats in the shot whose last line lies inside the shot's lines, of max(`pause_after.seconds`, `turn_reaction_min_s` if the beat's `turn` is not `none`, else 0). Printed with its reasons ("speech floor 11.8 s: Saye 19 words at 2.0 = 9.5 s, Iona 2 words at 2.5 = 0.8 s, 3 speeches × 0.5 s; pause owed 2.0 s after the turn at beat 7"). At step 8 the handout prints a **provisional floor** per list item, computed from every speech whose cue lies in that item's beats; TIME-01 uses the shot's real `hear` items |
| Clips | per chosen model: screen time + 0.75 s handles each end, rounded up to an allowed length; routing first, splitting last (section 8.4) |
| Mirror world | per scene `era` and `frame_handedness` from the mirror RULE's era lines (with mid-scene switch lines); per element `mirror_state` = mirrored when its STATE handedness differs from the frame's; each location's `orientation` (single when seen in one mirror state only, both otherwise); per shot `mirror_route` (section 8.5); `post_ops`. Worked values for The Catch are in K03 |
| Sides | image side of every sided feature in frame from own side, facing and mirror state (facing camera: own right = frame left; facing frame right: own right = hand nearest the camera; mirrored: swap); prompt side before any flip; text orientation per era and rule exceptions. A side the story states for an element that is mirrored on screen is an apparent side; SIDE-04 compares apparent sides |
| Geometry (set plan present) | frame placement (`at`) and facing of every subject, projected from marks, MOVE records and the setup; eyeline side for every single; axis side per setup per part; face height as a fraction of frame height = `head_height_m` ÷ the visible height at the subject; size check: visible height at the subject = (36 ÷ lens_mm × distance) ÷ frame ratio, compared with the subject's height (≥2.0 × height extreme_wide; 1.1-2.0 wide; 0.75-1.1 medium_wide; 0.45-0.75 medium; 0.3-0.45 medium_close_up; 0.15-0.3 close_up; under 0.15 extreme_close_up); Blender facing `facing_deg = (θ + 90) mod 360`; each shot's plan in the orientation its scene's frame and the location's mirror state require, derived from the stored `plan_orientation` by x → W − x, θ → 180° − θ |
| Face height without a set plan | from `size`: extreme_close_up 0.6, close_up 0.4, medium_close_up 0.25, medium 0.15, medium_wide 0.1, wide 0.05, extreme_wide 0.02 (`face_height_by_size`) |
| Main light side | frame side of each LOOK's main light per setup and era, from the set-plan object or compass wall named in `from:`; with neither, `open` (prompts omit the side) |
| Generation | `needs` tags; scene model and suggested model; the generation spec; per-model prompts; lint; resolution and safe band from the frame shape; price |
| Estimates | runtime, shots, generated seconds, money, hours (D13 v0, shown to the user as "the first estimate", and v1, "the estimate from the shots") |
| Story points | each story point resolved to the beat whose lines contain its quote (step 7), stored as `code_state` |
| Film strip | one line per shot for the film pass |
| Views | the plain part of every record file (At a glance, the shots in one plain line each, "Why it's shot this way"); `00 Start here` status part; `02 Whole-film summary`; the book; exports |

### 5.7 The word list (one word for each thing)

This table is `reference/02 Word list.md` for the AI and, in plainer words with examples, `06 Word list.md` for the user. `rules/words.json` lists the retired words so the checker can flag them. Where the AI's word and the user's word differ, both are given ("AI: ...; user: ..."), and the user's word is the only one allowed above a file's divider and in messages.

| Thing | The one word (field or value) | Retired |
|---|---|---|
| Story state of a person or thing in a mirror story | **reversed** / **original** (`handedness`; never "turned", which belongs to value turns) | phase, frame reversed, turned (as a mirror state), handedness_phase, mirror true |
| A stretch of the film under one frame handedness | **era** (a, b, c) | phase |
| How an element appears in a shot | **mirrored** / **normal** (`mirror_state`, code) | MIRRORED, mirror_state capitals |
| The edit operation | **flip** | mirror_flip |
| The fixed words pasted into every prompt for a person, thing or place | **fixed description** | identity key, look line |
| A person's or thing's costume, injury and condition at a point | **state** (Iona, state 2) and its **state line** | look ID, costume phase C1-C6, states S1-S6 |
| The light, colour and texture of a place at a time | **look**; its pasted text is the **look block** ("look" is used for nothing else) | look key, lighting block, global look key |
| How the whole film is made to appear / how a character appears | **style** (with its **style words**) / **appearance** | look (for either), style key, "the film's look", "her look" |
| The main light | **main light** | key light |
| The shot where a scene turns | **turn shot** (`role: turn`) | key shot |
| The frame a turn must show, written before shots | **turn picture** | key frame (as a written frame) |
| Stills a video starts or ends on | **start picture**, **end picture**; one pinned inside a clip: **pinned picture** | keyframe, first frame, start frame |
| A grey still that fixes composition | **layout picture** | structure image, layout guide |
| A grey 3D video a model copies | **guide video**, made from a **grey render** | control video, clay render, greybox, motion guide |
| Reference pictures of one element state | **reference pictures**; one film-look still: **style picture** | reference pack, asset sheet, stack, model sheet, style frame |
| McKee's action and reaction | **beat** | bit |
| A timed visible change inside a shot | **moment** | BEATS (in prompts), timeline events, C4 beats |
| "(beat)" in a script | **pause** | beat |
| A part of a scene with its own turn | **part** | movement |
| One reply's share of a scene's shots | **batch** | part (for replies) |
| A group of scenes | AI: **sequence** (SQ); user: **group of scenes** ("group 3") | stretch, colour-script sequence, journey unit |
| The camera's movement / a character's move on the floor plan / Block's motion component | **camera move** (`move`) / **floor-plan move** (MOVE record) / **motion** | movement, "move" alone in user text |
| Whose point of view a scene holds / a shot through someone's eyes | **whose scene** / **point-of-view shot** (`frame: pov`) | POV for both |
| What a character wants in a scene / in life | **want** / **life want** | objective, intention, super-intention, spine, scene desire |
| What a line or act does to the other person | **tactic** (an -ing word) | action gerund, playable action, infinitives |
| What the hands do | **task** | activity, physical task |
| What we see the body do in a shot | **does** (visible behaviour) | emotion words, behaviour as a plan field |
| How openly a face or body shows a feeling / what does not move | **display** 1-3 (contained, visible, open) / **still** | performance scale, intensity (for display) |
| Which way a subject moves across the frame | **travel** | screen direction (as a field name) |
| A moment inside a scene named before its beats exist | **story point** (a scene and a quote) | beat reference (before step 7) |
| The feeling a film or scene is played in | **tone**: the film's **home tone**, a scene's **tone**, **undercurrent** and **tone shift** | mood (as a field), genre (for tone) |
| The record of changing states | **continuity** (file 09, STATE records) | continuity bible, ledger, state table, damage ledger |
| A thing that returns and gathers meaning | **motif**, with **plant**, **payoff**, **rhyme** | carrier log, thread, emblem, hinge, reserved framing |
| A choice saved for special moments | **saved choice** (RC, RESERVE record) | reserved choice, reserved framing |
| Kept out of frame for later | **keep hidden** | withhold, withheld |
| Readable words inside the picture | **text in picture** (TX); the drawn file is the **text graphic** | on-screen text, insert graphic, text spec |
| A character's voice / a place's steady background | **voice** (with its **voice description**) / **room sound** | sound key, voice key, room tone key, bed, ambience |
| How a voice reaches us | **path** | channel, voice_source, perspective |
| Where the camera stands in a scene | **setup** ("camera A") | camera position S1-S8 |
| Left and right | **frame-left**, **frame-right**; **own left**, **own right**; **hand nearest the camera** | screen left, image-left, camera left |
| The imaginary line between two people | **the line** (`line of action`) | axis, 180° line |
| Shot sizes | **extreme wide, wide, medium wide, medium, medium close-up, close-up, extreme close-up, insert** | big close-up; EWS, WS, MCU, CU, ECU, OTS and every abbreviation |
| Tilt / eye height | **angle** / **height** | angle_height |
| Where a fact comes from | **origin**: story, inferred, invented | fact, extracted, authored, added, [design choice] |
| Who may write a field | **writer**: story, ai, user, code_state, code_derived | extracted, authored, derived, human |
| Used length / length to generate | **screen time** / **clip length** | duration_s, clip_s |
| Why a shot exists | **purpose** | PURPOSE, purpose (as picture job kind) |
| The kind of picture job | **use** | purpose |
| A departure's reason | the record's **why** | override:, WHY slot, story_reason |
| How loud a thing is / a sound is | **emphasis** 0-3 / **sound emphasis** 0-3 | L0-L3, S0-S3, emphasis device |
| An extra signal on a beat | **added emphasis** (0 or 1) | emphasis device, added signal |
| Pressure inside a scene / across the film | **beat intensity** 1-5 / **scene intensity** 1-10 | intensity, story intensity |
| Whole-film facts | the **whole-film files** (05-10) and their **whole-film summary** (file 02) | bible, visual bible, asset bible, register, core facts |
| A question to the user with a default | **choice**; one grouped without asking: **small choice** ("small choices I made") | decision card, question record, small call, decision (for a choice), question (for a choice) |
| A place in the pipeline where the user answers | AI: **checkpoint** A, P, B, C, D, E; user: named by what it is: "the scene list" (A), "how the book becomes a film" (P), "the big choices" (B), "each group of shots" (C), "the finished check" (acceptance), "the grey previews" (D), "keeping takes" (E) | checkpoint letters in user text |
| How deep the breakdown goes | **quick**, **standard**, **detailed** (`depth`) | full (as a depth) |
| A problem found, with its fix | **finding** | issue |
| One step of the pipeline | **step** (counted from 1 for the user: "step 8 of 12") | stage (except "Stage", capitalised, the product's name, and `stage.py`, which WORDS-02 exempts) |
| A piece of AI work that fits one reply | **unit** | task, call |
| The file the AI reads for a unit | **handout** (code surfaces); the attached **step file** and **whole-film summary** (chat) | context pack |
| Grey 3D stand-in renders of shots | AI: **previs**; user: **grey previews** | clay preview, greybox (for the user) |
| Runtime and cost estimates | AI: v0, v1 (D13); user: **the first estimate**, **the estimate from the shots** | v0, v1 in user text |
| Where a take is kept or rejected | **take** | generation job |
| The flashlight in prompts | **flashlight**; "torch" only inside quotes of the script | torch in prompts |
| Model names | the exact name in `video_models.json`, with aliases ("Kling O3" = `kling-3.0-omni`) | informal names |

### 5.8 Constants (`rules/constants.json`)

| Name | Value | From |
|---|---|---|
| `speech_wps_default` | 2.5 words per second (per-voice `pace_wps` overrides; Saye 2.0) | K08 |
| `clip_speech_rule` | Σ(words ÷ pace) ≤ clip length − 1.0 s (17 words in 8 s at 2.5) | K08 |
| `speech_floor_extra_s` | 0.5 s per speech | A2, K10 |
| `text_floor` | max(2.0, 1.0 + characters ÷ 13); emphasis ≥ 2: at least 2.0 + 0.5 × words; mirrored × 2 | K09 |
| `pause_tiers` | half-open ranges: short [0, 1.0) s; medium [1.0, 2.5) s ("(beat)" = 1.0 s); long [2.5, 4.0] s ("Silence." and "She waits." 2.5-3 s; "A long moment" 3-4 s); above 4.0 s a `hold`, which needs a saved choice (RC) | K10 |
| `long_pauses_per_scene_max` | 2 | A1 R15 |
| `turn_reaction_min_s` | 2.0 | A2 |
| `handles_s` | 0.75 each end | K10 |
| `non_dialogue_seconds_by_intensity` | 1: 5-8; 2: 3.5-6; 3: 2.5-4; 4: 1-3; 5: under 1 or 6 and over | A4 §6.1 |
| `scene_total_tolerance` | ±10% of `target_duration_s` | C5 R27 |
| `main_actions_per_seconds` | at most 1 per 4 s unless the shot is marked compound | C3 R2 |
| `acting_characters_per_clip_max` | 3 | C3 L22 |
| `push_in_per_scene_max`, `extreme_close_up_per_scene_max` | 1, 1 (on the main turn); caps, never quotas | B1 P5 |
| `extreme_close_up_film_max`, `push_in_scene_share_max` | non-insert extreme close-ups: 3 in a short, 6 in a feature [judgement]; push-ins in at most 0.25 of scenes; both written as film-level RESERVE records at step 6 | B1 R19's budget shape, card 14's "push-in on every realisation" trap |
| `departments_changing_at_main_turn_max` | 2 | B3 R7, B1 P11 |
| `signals_changing_per_beat_max` | 2 of size, light, sound, camera move and colour | B3 R7 |
| `display_3_needs_why_at_or_tighter` | close_up | D15, A4 §6, B5 §3.3 |
| `hold_needs_still_s` | 2.0 (a moment of 2 s or more, or a pause held on picture, needs a `still` item) | D15 |
| `head_height_m` | 0.23 | [judgement, tune in test] |
| `face_height_by_size` | extreme_close_up 0.6; close_up 0.4; medium_close_up 0.25; medium 0.15; medium_wide 0.1; wide 0.05; extreme_wide 0.02 (used when no set plan exists) | [judgement, tune in test] |
| `motif_spines_max`, `sound_motif_max`, `body_motif_max` | visual spines 3-5 in a short, 5-8 in a feature; 1 sound motif; 1 body motif | B4 rule 7 |
| `loud_sets_max` | 2 in a short; 3 in a feature | B4 |
| `emphasis_3_rules` | at most 1 per motif in the film; at most 2 per scene, on different turns, never in consecutive shots | B4 |
| `added_emphasis_per_beat_max` | 1; 0 where the script marks the beat | B4 R23, B1 P11 |
| `plant_emphasis_max` | 1; 2 for a plot-event plant | K11 |
| `device_budget_short` | at most 2 each of editor-made cut to black, true silence, freeze | A4 P10 |
| `fixed_description_words` | principal 25-40; minor 20-30 | B5, C2, C5 |
| `look_block_words_max` | 60 | B2 |
| `batch_size` | 12 default; 18 after the self-test passes | D1 §2.4 |
| `repair_rounds_max` | 3 | C5 R13 |
| `plate_route_face_height` | 0.10 of frame height | machine-first E6 [judgement] |
| `lip_sync_tight_face_height` | 0.15 of frame height [judgement, tune in test] | D3 |
| `model_facts_max_age_days` | 30 | C1 §0, D13 R7 |
| `takes_stop_per_route`, `takes_stop_per_shot` | 4, 10 | C3 §17A, C1 |
| `cheap_test_above_usd_per_take` | 2 | C3 §17A |
| `film_asl_range_s` | 3-7 for the home tones grave and tense; other home tones scale it by their shot-length factor in `tone_defaults.json` | D13 R3, D10 §2.2 |
| `rhythm_class_asl_s` | action_peak 2.0; suspense 3.5; mixed 4.0; dialogue 4.5; contemplative 6.0; read only by `estimate.py`, never a design target | D13 §5 |
| `v0_action_seconds_per_word` | 0.166-0.220 | D2 §6, D13 §4.1 |
| `size_ladder_thresholds` | section 5.6 | [judgement, tune in test] |
| `caption_lead_s`, `caption_min_s`, `caption_max_s` | 0.25; 1.0; 7.0 (5.9) | [judgement, tune in test] |

**Tone defaults.** `rules/tone_defaults.json` holds D10 §2.2's row for each of the eleven tones (shot-length factor, size and lens, movement, contrast band, music default, performance display level). The estimate multiplies `rhythm_class_asl_s` by the scene tone's factor; TIME-07 and the rhythm checks read it; card 08 teaches it. A scene's tone outside `tone_range` is flagged for the user, never fixed (D10 TN7; FILM-12).

### 5.9 Export formats (shot list and captions)

**Shot list** (`16 Spreadsheets/Shot list.csv`; UTF-8 with byte-order mark; one row per shot in film order; the first row holds the column names in plain words). Columns, in order: Scene; Shot ("150"); Crew label ("10Q"; the only place it appears); Size; Angle; Camera move; Lens (mm); Subject (names); Description (the list item's one line); Dialogue (speech IDs, then the words); Screen time (s); Location; Look; Grey preview level; Storyboard (yes or no); Route; Model; Notes (the shot's `why`); Shot ID; Beats. The columns are Stage's own; they are chosen so that common shot-list tools can map them on import, and T8 checks this list, not any vendor's. `People, places and things.csv`: Kind; ID; Name; Fixed description; States (IDs with their state lines); Scenes.

**Captions** (SRT and WebVTT in `17 Captions and audio description/`). Shot start times are the running sum of screen times in film order (the first assembly). One cue per heard speech: it starts at the `hear` item's `at` when given; otherwise the shot's first speech starts `caption_lead_s` (0.25 s) after the shot starts and each later speech starts where the previous one ends. A speech lasts its words ÷ the speaker's `pace_wps`; a cue lasts at least `caption_min_s` (1.0 s) and at most `caption_max_s` (7.0 s), longer speeches split at a sentence end. An off-screen speaker's cue is prefixed with the name ("SAYE:"); an `effect` with `sound_emphasis` 2 or more adds a sound tag ("[the pump]"). Captions are rebuilt whenever screen times change.

---
## 6. Knowledge delivery

### 6.1 Four layers, and only the handout decides what is read

| Layer | What | Size | When the AI reads it |
|---|---|---|---|
| House rules | `SKILL.md` (Claude), `00 Paste into instructions.txt` plus `01 House rules.md` (chat) | under 4,500 words (chat: 6,000 characters plus about 5,500 words) | always |
| Step file | one per step and add-on | 1,200-1,800 words | at the start of every unit of that step, every time, never from memory; on code surfaces as the handout's excerpt, in chat as the attached step-group file; the AI quotes the one-line task back before working |
| Cards | 24 cards (below); a unit reads named parts of them | 600-2,000 words each | only the parts `steps.json` lists for the step, depth and scene tags, at most 9,000 card tokens per unit |
| Library | research files, digests, `00 Resolved conflicts.md`, `01 What the codes mean.md`, `02 Errata.md` | 30-160 KB each | never whole; `stage.py lib B1 R14` (or `§10.2`, `P5`, `Ex1`) prints one section or rule (at most 2,500 words) with any errata that apply, when a card points there or a hard case arises; where the full file is absent (the skill ZIP and the tools ZIP carry digests only) it prints the digest's entry and says so |

**Handout budget** (code surfaces, per unit, typical Standard): step excerpt 2,000 tokens + the whole-film summary's lines for the IDs in play 800-2,000 + card parts 3,000-9,000 (capped at 9,000) + one gold excerpt 1,500 + source lines 1,000-8,000 + records the unit needs 2,000-6,000 = 10,000-28,000 tokens. `stage.py handout` prints its size; over the surface ceiling in `limits.json` (30,000 tokens on Claude surfaces, 20,000 in ChatGPT's sandbox) it drops the example, then the lowest-listed card parts, then trims source to the unit's lines, then splits the unit. Instruction first; the one-line task repeated at the end (C5 R17).

**Chat surfaces** use `02 Whole-film summary.md`: exactly the records step 7 lists as inputs from files 04-09 (the scene list with events, sequences and plan fields; fixed descriptions, state lines, voices, movement and status lines; FACT and PLANT lines; world rules), minus set plans; at most about 6,000 words. The film rules are not summarised: `10 Film rules.md` is attached whole to every scene chat, and `08 Places and things.md` too when the scene's place has a set plan. With the step file, the story, `00 Start here` and the previous scene file, that is at most seven attachments (2.5). The summary is rewritten only at stop points in chat apps (end of a sequence, "stop", or the chat budget), and after every change to files 04-09 on code surfaces.

### 6.2 The cards

All examples inside cards use the pipeline's IDs and words (research numbering converted once, at build time). Every card ends with "Words for AI models" (what works, what fails) and "Look up for more" (library file and section).

**Department cards (anatomy in 6.4; 1,500-2,000 words each)**

| # | Card | Distils | Loaded by steps |
|---|---|---|---|
| 01 | Reading the whole story | A2 §2 and Steps 2, 7; A3 §3.2; B4 §3.1; B3 §2.6; A4 §6.5; D2 §3-§6; D13 §4.1 | 1, 2 |
| 02 | Adapting prose | A3 §4 and §7 (five tests, externalisation ladder, letters, time jumps); D2 R1-R23 and §8; D14 intake rules (formats, thin sources, stage plays, comic and game scripts, other languages) | 1, 2; 7 for tag `prose_interior` |
| 03 | Scenes, values and beats | A2 (values, charges, sign test, beats, tactics, intensity, five steps, parts, flags); A3 §3.2 | 7 |
| 04 | Dialogue on screen | A1 (landing face and tie-breaks R19, unsaid and carriers, pause ranking, cut rules, conflict levels; line-by-line flaws flagged and staged: on the nose R35, melodrama R36, forced exposition R22, monologue R31, interrupted R30a, can play silent R18; land off the speaker at least once per scene R2); D3 §5 delivery words | 7, 8 |
| 05 | Characters | B5 (thesis, the lineup as six word columns, face distinguishers R21, movement signature with home, stress and break efforts §5.1-5.4, psychological and signature gesture R17, status and flips R15-R16, proxemics §5.5, fixed description rules, state lines, sides by era, non-human rules); B4 §6.1 costume questions | 4, 5 |
| 06 | Voices and performance | D3 (voice design, pace, paths, consent, lip sync routes); D15 (display levels 1-3 and the closer-is-lower rule, stillness written out, eyeline dwell, looks saved for later beats, breath); A1 R8-R10; C3 §6 emotion as behaviour; energy continuity across clips | 4, 7 (display and stillness part), 8 (Standard), add-on C |
| 07 | Places, things and motifs | B4 (six tests, ranks, emphasis ladder, budgets, motif caps, loud and quiet sets, plants); B3 §6 set-plan template; A3 §5.3 element categories | 4, 7 (Detailed) |
| 08 | World, style and genre | D5 (medium, style words, film texture, the three-direction style test); D10 (tone values, home tone, undercurrents and shifts, the tone defaults table behind `tone_defaults.json`; genres of setting set the world, not the camera); D17 as available (locale, invented places); B1 P3 frame shape reasons; B2 R19 local signals; D4 style-imitation policy | 2 (tone part), 3 |
| 09 | Film rules and restraint | B1 §9 and P5 (camera system template, budgets); B2 §5, §8 (lighting plans, colour script, peaks first); B3 §2.5-2.7 (visual structure, counterpoint); B4 §3.4 (emphasis budget); A4 §6.9, §7.6 (rhythm across scenes, music policy); the reserve ledger; the ladder; the film-pass audits and questions | 6, 9 |
| 10 | Camera | B1 (six slots with reasons, size ladder, height, lens, move and its cause, character camera rules, mirror methods summary, AI camera words) | 6, 8 |
| 11 | Light and colour | B2 (lighting plan, main light placed in the room, light kept fixed where no story source can change it R10, colour script row, per-shot light, dark skin in low light exposed, filled and named R24, clichés, "flashlight not torch") | 6, 7 (Detailed), 8 (Detailed) |
| 12 | Staging and composition | B3 (floor plans, marks, stations, distances, moves with a named want P2-P3, the weaker person moves R3, the three-person pivot, engaged pair and silent third R25, configuration change on turns, glass physics summary, frame rules, prose to marks) | 4, 7, 8 |
| 13 | Cutting, rhythm and sound | A4 (cut points, duration table, the turn shot as the scene's longest or shortest R4, holding on the unaware in suspense S2, reading times, transitions only where written, split edits, sound labels, room sound, sound motifs, silence grades, rupture, music policy); D9 as available (spotting) | 6, 7, 8 |
| 14 | Shot design | The six camera slots in order; turn shot first; must-keep shots; coverage from the dial; purpose, because and why (pass and fail pairs); the fields that need a `why` and their defaults (5.4 rule 11); holding the baseline as a department idea; at most two departments changing at the main turn; the film-level saved choices for the extreme close-up and the push-in; the rule order (6.3); budgets; cliché traps; one camera move; behaviour not emotion; reading floors | 7 (list part), 8 |

**Situation cards (loaded by scene tag; 600-1,000 words each; anatomy: situation, questions in order, rules, traps, words for AI models, one worked example)**

| # | Card | Tags | Distils |
|---|---|---|---|
| 15 | Action scenes | `action` | D11 (geography first, cause and effect, escalation, reversals, the action score, the five time treatments, expanded time from overlapping real-time slices, never slow motion unless the camera system allows it; screen direction held until the story turns it); A3 R16 and rule 33; B1 R23; C4 R10-R12 physics; K20 |
| 16 | Glass, mirrors and sides | `glass_and_reflection`, `handedness` | B3 §8 and R28-R29 (glass states, twin check); K02 decision table; K03 eras; K07; B1 §10.2; C2 §7; side derivation rules |
| 17 | Screens, text and in-story cameras | `screens_and_text`, `in_story_footage` | D12 as available; B1 §10.4-10.6 and P6; C2 R6 (text graphics); A3 R9, R11; K09, K17 |
| 18 | Suspense, reveals and the dark | `suspense_and_reveal`, `darkness` | A4 S1-S6 (the information ledger, suspense, mystery and surprise, reveals designed backwards with a way of withholding on every earlier shot); A1 R3-R4; A3 rule 9; B1 P7; B2 R23-R24 |
| 19 | Inner life, montage and time | `prose_interior`, `montage_and_time` | A3 §7.2 externalisation ladder, §7.4 summaries; A1 R32-R34; A4 T2 |
| 20 | Creatures, violence and filters | `creature`, `violence` | B5 §6; C1 R9-R10, R25-R27; C3 §14; D4 §3.6 and rules 10-11 |

**Production cards (1,200-1,800 words each)**

| # | Card | Distils | Loaded by |
|---|---|---|---|
| 21 | Making pictures and video with AI | C1 (model landscape as of the adapter date, routing, costs); C2 (reference pictures, stack order, start pictures, drift checks); C3 (master prompt, adapters, linter, failure catalog); D3 routes for dialogue; D5's style test; B2 R24 in the review list (a darker face as readable and as true in colour as the others) | add-ons A and C; step 10 (cost part) |
| 22 | Previs | C4 (levels, master sets, plan schema, routes into video, checks, physics keying) | add-on B |
| 23 | Finishing, captions and delivery | D6, D8 as available (layers, flips, conform, colour matching, titles); D18 as available (captions, audio description, translation); D9 (music and effects licensing, spotting) | add-on D; step 11 |
| 24 | Rights, consent and disclosure | D4 (rights intake, public domain, likeness and voice consent, style imitation, content flags, licences, disclosure text) | 0, 4, add-on C |

"As available" means the D research file exists in the library at build time; when it does not, the card is written from the parts already in the library (listed in the brief's section 5 under "Already partly in") and marked "to be completed from D<n>".

### 6.3 Rule order (when rules disagree)

The higher rule wins; the choice is recorded in the record's `why`. Merged from A1, A2, A4, B1, B2 and B3 (craft-first's ladder, which puts readability second as B2 L2 and A1 do):

1. What the story itself states we see and hear (directions, named light, written transitions, "Nothing has happened to the mint").
2. Readability of the beat (the audience can read the face, the text, the geography).
3. Physical honesty (in-story footage, physics, glass optics).
4. The film's systems and budgets (banned and saved choices, character camera rules, motif code, colour script, location continuity).
5. Flaw handling (lines carrying a BEAT `flag`: on-the-nose or melodramatic lines are staged small, A1 R35-R36; forced exposition moves to an image or off screen, R22; a monologue gets listener coverage, R31).
6. Turn rules (the scene's most extreme framing on its turn; nothing tighter before it).
7. Emotion over spatial continuity (Murch), logged as a departure.
8. Conflict-type defaults (A1, A2).
9. General beat defaults and translation menus.
10. The baseline (static, the owner's eye height, a normal lens, room sound).

### 6.4 Anatomy of a department card (nine parts, always in this order)

1. **The job**: one paragraph, and what the step must hand on.
2. **Questions in order**: the questions a head of department asks, each pointing to its research rule (card 14, camera part: "Whose scene is this beat? Put the lens at that person's eye height (B1 R6). Is this beat a turn? Give it the scene's most extreme framing: closest if the turn happens inside a person, widest if it leaves them alone or waiting (B1 R1, A2 R4). Has the script already marked the beat? Then the camera adds nothing (B1 P11, B4 rule 17)").
3. **Translation menus with pitfalls**: options, "pick at most one; tie it to a line, object or action in this story".
4. **Budgets and reserved choices** for this step, by name from `constants.json` (numbers are never restated in cards).
5. **The baseline is a strong answer**: "Static, the owner's eye height, a normal lens, room sound are choices, not failures. Depart only for a reason you can cite."
6. **Cliché traps, each with its test and fix**: push-in on every realisation; low angle from the first beat; Dutch tilt for tension; crane-up on every sad ending; shallow focus everywhere; god rays, lightning at a revelation, flickering hospital tubes, teal-and-orange; rain on glass, ticking clocks, wilting plants, empty chairs; a sad cue under unspoken sadness; dissolves the script never wrote; glowing eyes and chrome on a creature. Tests: the **any-film test** (would this reason fit any film with this theme?), the **mood-word test** (does the reason name only a feeling?), the **stacking test** (more than one signal on one beat?), the **sound-off test** (does the frame tell the beat with the sound off?).
7. **Reasons that fail and reasons that pass, in pairs**: fails "Close-up to show her shock."; passes "The scene's tightest size, spent on its main turn (SC10-B07): 'Her face changes.' puts the change inside her." Fails "Low angle to make Saye powerful."; passes "Eye level on Saye (CR-SAYE: she holds power by stillness, not angle); she wins at SC10-B11 by waiting."
8. **Two worked examples** in different registers: one from The Catch, one from The Long Places or another tone (D10 §12), so the card does not teach one film's taste as law.
9. **Yes/no self-check** for the step (the same questions the review asks).

---

## 7. Tools

### 7.1 One command over a small package

All tools are Python 3.11 standard library (no installs), except the previs scripts, which need Blender's Python module (bpy 5.0.1 tested here; C4 targets 5.2.2 LTS). Each file starts with a plain note saying what it does; functions and variables use full plain words (`remove_empty_rows`, not `rmEmpty`). The AI runs every command for the user; the user never types one.

Usage is always `python <skill folder>/tools/stage.py <command> [options]`, from any folder: `stage.py` finds its own files (schema, rules, steps, cards, templates) through its own location (`__file__`), so the same command works in Claude Code (`python .claude/skills/breaking-down-stories/tools/stage.py`, as CLAUDE.md says), in the Claude website's skill folder and in ChatGPT's unpacked `07 Tools.zip`. `--project "<path>"` defaults to: the current folder if it holds `00 Start here.md`; else its single subfolder that does; else the single project in `My breakdowns/`, found by walking up to the folder that holds CLAUDE.md. With none or several, the command stops with exit 2 and names the choices.

| Module | Plain purpose |
|---|---|
| `stage.py` | The one entry point: reads the command and calls the modules below; prints plain lines; exit codes in 7.3 |
| `stage_tools/record_format.py` | Parse record files (grammar G1-G13), tidy slips, merge by ID, write records back in canonical order with the plain part and divider preserved, check END lines |
| `stage_tools/project_files.py` | Create projects; fixed file names per record type; manifest (fingerprints, locks, units done, batches with expected and received counts); log; save ZIPs; lock file for parallel helpers |
| `stage_tools/read_story.py` | Detect format, normalise, number, split scenes or chapters, place title-page lines, front matter and end cards (step 1's placement rules), extract speeches, cues, transitions, title lines, capitalised tokens (classified as sound, prop, text or emphasis) and light words; propose aliases; odd-lines report; counts for the v0 estimate; resolve quote anchors to line numbers |
| `stage_tools/adopt_folder.py` | Turn a folder saved by hand in a chat app into a checkable project (the `adopt` command) |
| `stage_tools/derive_fields.py` | Everything in 5.6, including story-point resolution |
| `stage_tools/check_records.py` | All checks in 7.2 except FILM; health-check report |
| `stage_tools/film_pass.py` | Film strip and FILM checks |
| `stage_tools/make_handout.py` | Build a unit's handout from `steps.json`, card parts, records, source lines, provisional floors and pre-issued IDs within the surface budget |
| `stage_tools/make_views.py` | `00 Start here` status part; `02 Whole-film summary`; the plain part of every record file; `12`, `13` reports; the book (HTML and Markdown) |
| `stage_tools/make_exports.py` | Shot list and elements CSV (UTF-8 with byte-order mark; columns in 5.9), OTIO written directly as JSON, CMX 3600 EDL, captions SRT and WebVTT (timing in 5.9), audio-description script, text-to-translate list, `breakdown.json` and its portable schema, voice line script, spotting sheet, finishing job list |
| `stage_tools/estimate.py` | D13 v0 (words) and v1 (shots): runtime, shots, generated seconds, money by tier, hours, calendar; staleness of prices |
| `stage_tools/compile_prompts.py` | Generation spec per clip; routing; per-model prompts; lint; packs; storyboard frame prompts; picture job lists |
| `stage_tools/make_text_graphics.py` | Draw each TEXT item as SVG, normal and mirrored (PNG when a converter exists) |
| `stage_tools/make_previs_plans.py` | Compile C4 plan JSON per shot from set plans, scene starts, moves, setups and shots; free-fall helper (reads SHOT `motion`) |
| `stage_tools/refresh_models.py` | Propose a dated update of the adapter files from the makers' pages, check its shape, apply it once the user approves any price change |
| `stage_tools/build_kit.py` | Maintainers: build `07 Chat kit/` (with `07 Tools.zip`), `08 Skill for Claude apps.zip`, `AGENTS.md`, `reference/03 Field guide.md` and templates' value notes from the skill |
| `previs/previs_from_plan.py`, `previs/check_blocking.py` | From the C4 kit, unchanged |
| `previs/render_previs.py` | Render a set of plans, run the blocking check on each, write a contact sheet page |

**Commands**

| Command | Plain purpose | Inputs → outputs | If the AI cannot run code |
|---|---|---|---|
| `new "<story file>" [--title] [--depth]` | Start a project | story → folder, `00 Start here.md`, `01 Choices.md`, `Original/` | the AI writes 00 and 01 from templates; the user makes the folder |
| `selftest --prepare` / `--score` | Test this surface (the self-test unit, step 0) | `--prepare` → issued IDs and a SHOT template; `--score` → `surface`, `code_execution`, `batch_size` on PROJECT, test records deleted | the AI quotes first and last lines; batch size 12 |
| `read` | Read and number the story | `Original/` → `03`, `04`, CHAPTER stubs, `speeches.json`, odd-lines report, v0 counts | the AI writes the scene list with quote anchors |
| `adopt "<folder>" "<story file>"` | Turn a folder saved by hand in a chat app into a checkable project | runs `read` on the story; builds `Original/`, `03 Story - numbered.md` and `speeches.json`; merges batch files by ID; turns every quote anchor into line numbers (CITE-02 on each); re-owns every `code_state` field the AI wrote under `chat_writer: ai` (each difference logged as N); sets `code_execution` to the new surface's value; then runs `check --all` | n/a (it is the bridge from chat to code) |
| `status` | Where things stand | manifest, records → one screen: done, stale, waiting for the user, next | "Where are we?" answered from `00 Start here` |
| `next` | The next unit | `steps.json`, manifest → unit ID and handout path | the step file's "what to do next" |
| `handout <unit>` | Build a unit's handout | → `For machines/handouts/<unit>.md` | the AI names the files the user should attach |
| `apply <inbox file>` | Accept the AI's records | inbox → numbered files, log, manifest | the user saves the copy box as the named file |
| `check [--step N] [--scene SCnn] [--film] [--all] [--story <path>]` | Run the checks | records → problem lines, `13 Health check.md`; `--step N` requires only fields filled by step N or earlier; during step 8, coverage runs on the batch's range | mechanical checks in words per unit; judgement checks in a check chat; the real check on a code surface after `adopt` |
| `build` | Compute derived fields | records → `breakdown.json`, views | on the next code surface |
| `impact <ID>` | What depends on a record | → list of IDs and units that go stale | the AI searches the files for the ID |
| `questions --sample [--seed N]` | Yes/no review questions | records → question batches | the rubric's questions in words, answered in a check chat |
| `estimate [--version v0\|v1]` | Time and cost (v0 is "the first estimate" to the user, v1 "the estimate from the shots") | records, prices → `14 Time and cost.md` | a rough estimate labelled rough |
| `compile [--scene <range>] [--model <list>] [--force-model <id>] [--storyboard] [--lint-only]` | Prompts and packs | records, adapters → `20 Prompts for AI video/`, `18 Storyboard/`, lint. `--scene` takes one ID, a comma list or a range `SC07..SC10`. `--model` writes packs only for shots whose routed or override model is in the list. `--force-model` compiles every shot in scope for one adapter, to test its syntax, with GEN-02 and GEN-10 reported as notes. `--lint-only` routes and lints without writing packs | the AI writes a few prompts by hand from card 21 and lints them in words |
| `graphics` | Draw text graphics | TEXT → `20 Prompts for AI video/Text graphics/` | the AI writes SVG text in a copy box |
| `previs [--shot] [--render]` | Previs plans and renders | records → plan JSON; with `--render`, renders and blocking report | not offered: grey previews need Claude Code on the user's computer |
| `export <shotlist\|book\|timeline\|captions\|json\|voices\|spotting\|finishing\|all>` | Exports | build → folders 15-17 and 21, machine files; `voices` writes the voice line script (8.6), `spotting` the music and effects spotting sheet, `finishing` the finishing job list | the AI writes `15 The breakdown/The breakdown.md` as a contents page |
| `pack` / `unpack <zip>` | Save or open the project as one ZIP | folder ↔ `NNN Save - <title> - after <what>.zip` | the user saves files one by one |
| `lines <ID> [--more]` | Every source line mentioning an element | aliases → lines | the AI searches the attached story |
| `lib <code> <reference>` | One library section or rule with its errata | `B1 §10.2`, `B1 R14`, `B1 P5`, `B1 Ex1` → text; the digest's entry, labelled as such, when the full file is absent | cards only |
| `refresh-models --propose` / `--apply` | Refresh the dated model facts (8.2) | the makers' pages → a proposed diff of the adapter files, shape-checked; `--apply` writes it after the user approves any price change | not available |
| `import-json <file>` | Accept API structured output | JSON → record text | n/a |
| `build-kit` | Build the chat kit, skill ZIP, AGENTS.md, field guide | skill → files | n/a (maintainers) |
| `replay [--story <path>]` | Regression: check the gold examples against their expected outputs | examples, and the story excerpts in `tests/fixtures/` (or the story at `--story`) → pass or fail; without any story text the CITE checks are reported "skipped: story not present" | n/a (maintainers) |

### 7.2 Every check

Level: **E** error (blocks the unit's "done"), **W** warning (shown at the next checkpoint), **N** note (logged). Build: **1** in the first build (needed by the tests), **2** later (add when the test run shows the error happens). Every message is one line: level, check ID, record, field, what is wrong, the allowed values or the fix. Example: `E TIME-01 SC10-SH150 screen_time 12 is under its floor 13.8 s (speech 11.8 s + pause owed after the turn at beat 7, 2.0 s). Fix: raise screen_time to 14 or move SC10-D12 to the next shot.`

| ID | Check | Level | Build |
|---|---|---|---|
| **FORM-01** | Unknown record type | E | 1 |
| FORM-02 | ID does not match its type's pattern | E | 1 |
| FORM-03 | Unknown field for this type ("did you mean ...") | E | 1 |
| FORM-04 | Value not allowed for the field's kind or list ("did you mean ...") | E | 1 |
| FORM-05 | Required field missing at the project's (or the scene's) depth, among fields whose `filled_by_step` is at or before the step checked (`--all`: every field) | E | 1 |
| FORM-06 | END line missing | E | 1 |
| FORM-07 | END count differs from the records in the file | E | 1 |
| FORM-08 | Shortening marker inside a record (G11) | E | 1 |
| FORM-09 | Same field with two different values across merged copies (G10) | E | 1 |
| FORM-10 | Wrong writer: a `code_derived` field typed (dropped, W); a `code_state` field changed by the AI (E), except a `chat_writer: ai` field in a project marked `code_execution: no`; a user field set without a CHOICE whose status is `answered` or `defaulted` (E) | E/W | 1 |
| FORM-11 | Locked record changed | E | 1 |
| FORM-12 | Unknown sub-part key, positional sub-part, or ` \| ` inside text | E | 1 |
| FORM-13 | Tidy fixes applied (case, spacing, synonyms from words.json) | N | 1 |
| **ID-01** | Duplicate ID, among record IDs and IDs declared in items (`defines_id`) | E | 1 |
| ID-02 | Reference to an ID that does not exist (5.4 rule 2; a PREVIS stub with `status: planned` exists), or to an omitted record | E | 1 |
| ID-03 | Shot numbers not in tens; an insert without a gap; cards and black below 990 | W | 1 |
| ID-04 | An omitted ID reused | E | 1 |
| ID-05 | Scene count differs from the story's headings (screenplay) | E | 1 |
| ID-06 | ID outside the handout's pre-issued block | E | 1 |
| ID-07 | SHOT not in its scene's SHOTLIST; or, at Standard and Detailed, a list item without its SHOT (during step 8, only within the batch's ID range; in full after the scene's last batch) | E | 1 |
| ID-08 | SHOT's beats, role or size differ from its list item without a changed list | E | 1 |
| ID-09 | Scene ID width differs from `scene_id_digits` | E | 1 |
| **CITE-01** | Line reference outside the scene's lines | E | 1 |
| CITE-02 | A quote anchor or story point whose quoted string is not found, or is found more than once, in its scope (the scene for story points and scene fields, the whole story otherwise), or has fewer than 3 words (G5) | E | 1 |
| CITE-03 | A quoted string (G12) not found in the cited or scene lines | E | 1 |
| CITE-04 | `words` on a hear item differ from the speech's text | E | 1 |
| CITE-05 | Heard speech whose cue lies outside the shot's lines | W | 1 |
| CITE-06 | Prose SPEECH with `origin: story` not found word for word in its lines | E | 1 |
| CITE-07 | A name in a story-derived field that matches no alias | E | 2 |
| **COVER-01** | A story line of the scene in no beat (blank lines and the heading excluded) | E | 1 |
| COVER-02 | A story line of the scene in no shot (list item at Quick) unless omitted with a reason (blank lines and the heading excluded; during step 8, only the batch's beats) | E | 1 |
| COVER-03 | A speech heard in no shot (during step 8, only the batch's beats) | E | 1 |
| COVER-04 | A beat with no shot (during step 8, only the batch's beats) | E | 1 |
| COVER-05 | A cardinal event in no kept scene | E | 1 |
| COVER-06 | A scene in no sequence, or in two | E | 1 |
| COVER-07 | A scripted sound (a capitalised sound token, A4 §4.2) with no `effect`, `room_sound` or MOTIF appearance in its scene | E | 1 |
| COVER-08 | A scripted light, colour or darkness line (B2 P2) with no LOOK `light_cue`, no `stays_dark` and no shot `light` covering it | W | 1 |
| **TIME-01** | Screen time under the derived floor, `max(speech_floor, text_floor) + pause_owed` (5.6) | E | 1 |
| TIME-02 | A moment outside the screen time, or moments overlapping | E | 1 |
| TIME-03 | Scene total outside ±10% of its target (run after the scene's last batch) | W | 1 |
| TIME-04 | More than two long pauses in a scene | E | 1 |
| TIME-05 | The pause owed by a turn beat (5.6) is under `turn_reaction_min_s` (2.0 s) | E | 1 |
| TIME-06 | More than one main action per 4 s of moments | W | 1 |
| TIME-07 | Film average shot length outside `film_asl_range_s` scaled by the home tone (`tone_defaults.json`) | W | 2 |
| TIME-08 | Pause seconds outside their tier (half-open ranges, 5.8); a `hold` above 4.0 s without a saved choice | E | 1 |
| TIME-09 | In a `suspense_and_reveal` scene, shots on the character who does not know the fact (not in its `known_by`) average shorter than the scene's dialogue shots, with no `why` (A4 S2) | W | 1 |
| TIME-10 | The main turn's shot is neither the longest nor the shortest shot of its scene (A4 R4) | W | 2 |
| **STATE-01** | A subject or thing without a state valid for this scene | E | 1 |
| STATE-02 | A state without a cause line found in the story | E | 1 |
| STATE-03 | A `CONTINUOUS` scene whose entry state differs from the previous exit with no cause | E | 1 |
| STATE-04 | Consecutive shots of one subject disagree on end and start | W | 2 |
| **SIDE-01** | A sided feature without an own side | E | 1 |
| SIDE-02 | Image-side words in a state line or fixed description | E | 1 |
| SIDE-03 | A sided insert (ring, palm, scar) with `flip` other than `never` | E | 1 |
| SIDE-04 | A derived apparent side contradicts a side the story states (an apparent side for a mirrored element), or one written in `does` or `end` | W | 1 |
| SIDE-05 | A TEXT in a mirrored scene with no orientation rule | E | 1 |
| **GEOM-01** | Paired singles in dialogue without opposite eyeline sides (set plan present) | E | 1 |
| GEOM-02 | Consecutive shots of one subject change neither a size step nor 30°, and the join is not a jump cut | W | 1 |
| GEOM-03 | The camera crosses the line inside a part without a declared crossing | W | 2 |
| GEOM-04 | Authored size two or more steps from the computed size | W | 1 |
| GEOM-05 | A setup inside an object, a setup outside the room other than through a wild wall, or a mark outside the room | E | 2 |
| GEOM-06 | An authored `at` or `faces` contradicts the set-plan projection | W | 1 |
| GEOM-07 | `travel` reverses between shots of one journey without a turn beat or an on-screen change of direction (A3 rule 33, B3 §5.2) | W | 1 |
| GEOM-08 | Paired singles within one part differ in size, lens or height with no turn beat between them and no `why` (B1 R7) | W | 1 |
| **CRAFT-01** | More than one push-in in a scene (a cap, not a quota) | W | 1 |
| CRAFT-02 | More than one extreme close-up in a scene, or one not on the main turn (a cap, not a quota) | W | 1 |
| CRAFT-03 | The scene's tightest non-insert size used before its main turn | W | 1 |
| CRAFT-04 | A turn beat without exactly one turn shot | E | 1 |
| CRAFT-05 | More than two beat-intensity 5s in a part | E | 1 |
| CRAFT-06 | More than one camera move in a shot | E | 1 |
| CRAFT-07 | A lens outside the family without a lens exception that covers it | W | 1 |
| CRAFT-08 | A plant louder than emphasis 1 (2 for a plot-event plant), read from `thing` items with `plant:` | W | 1 |
| CRAFT-09 | Emphasis-3 budgets broken | W | 1 |
| CRAFT-10 | Added emphasis above 1 on a beat, or above 0 where the script marks the beat; an added light or sound change (dial or shot) on a beat the script already marks | W | 1 |
| CRAFT-11 | A reserved choice beyond its uses or outside its allowed places; a banned choice used | E | 1 |
| CRAFT-12 | Editor-made device budgets exceeded (film) | W | 1 |
| CRAFT-13 | A dissolve, fade, cut to black, freeze or smash cut that the story does not write (A4 T5); a match cut whose `why` names no shared shape, motion or sound. J-cuts, L-cuts and jump cuts are free | W | 1 |
| CRAFT-14 | An invented thing in frame not listed in the scene's additions | E | 1 |
| CRAFT-15 | More than three acting characters in a shot | W | 1 |
| CRAFT-16 | Slow playback where the camera system bans it | E | 1 |
| CRAFT-17 | A shot's size two or more steps from the dial for its beat | W | 2 |
| CRAFT-18 | A beat with `turn` other than `none` that changes the sign of no value's charge and reaches no value's `close` (the sign test) | E | 1 |
| CRAFT-19 | Stacking: more than two of size, light, sound, camera move and colour change on the same beat (B3 R7); more than two departments change at the main turn, or `scene_idea` does not name them | W | 1 |
| CRAFT-20 | Two principals share four or more lineup columns (B5 R3) | W | 1 |
| CRAFT-21 | A shot that hears a line flagged `melodrama` is tighter than the scene's median size, moves, or has music (A1 R36) | W | 1 |
| CRAFT-22 | A beat flagged `monologue` has no listener in frame and no listener shot (A1 R31) | W | 1 |
| CRAFT-23 | A dialogue scene with no `hear` item whose speaker is off screen (A1 R2) | W | 1 |
| CRAFT-24 | A turn beat whose `silent_third` appears in no shot of that beat (A1 R5) | W | 1 |
| CRAFT-25 | `display: 3` at close-up or tighter without a `why` (D15) | W | 1 |
| CRAFT-26 | A moment of 2 s or more, or a pause held on picture, with no `still` item on the subject (D15) | W | 1 |
| **INFO-01** | A shot before a FACT's reveal (its `audience_knows_from`) whose subject, thing or `must_show` includes the fact's `element` (A4 S1-S3) | W | 1 |
| INFO-02 | A FACT's reveal shot whose role is neither `turn` nor `must_keep` | W | 1 |
| **REASON-01** | Purpose missing, or `because` without a resolvable story ID (`default` is accepted when REASON-02 finds no departure) | E | 1 |
| REASON-02 | A field on the list in 5.4 rule 11 that differs from its default, or a departure from the camera system, without `why`; a turn shot without `why` | E | 1 |
| REASON-03 | `why` not anchored: no quote found in the scene's lines, no ID, no named element of the scene | E | 1 |
| REASON-04 | `why` contains a mood-only phrase from `words.json` ("to build tension", "for drama", "cinematic", "moody", "to add interest", "dynamic", "to emphasise" with no object) | E | 1 |
| REASON-05 | A turn shot whose `because` cites no turn beat | E | 1 |
| REASON-06 | A reserved choice used without its RC in `because` | E | 1 |
| REASON-07 | A tool-forced departure without `meaning_kept` | E | 1 |
| REASON-08 | An `unsaid` with no carrier seen or heard in any shot of its beat (things, `does`, sound) | E | 1 |
| REASON-09 | In a scene with `whose_scene`, a shot whose setup lies outside the scene's place, or which shows a FACT's element that character does not know, without `pov_break` (A3 rule 37) | W | 2 |
| **WORDS-01** | Emotion adjectives in `does` or `task` | E | 1 |
| WORDS-02 | A retired word in a field value or in user-facing text ("Stage", capitalised as the product, and `stage.py` are exempt) | W | 1 |
| WORDS-03 | A real person, living artist, film title or brand in any field compiled into prompts | E | 1 |
| WORDS-04 | An abbreviation or internal code in user-facing text: everything above a file's divider, reports, the book, `reference/07` message formats and every checkpoint template | W | 1 |
| WORDS-05 | A fixed description outside its length, or with expression words | E | 1 |
| **PLAN-01** | Not exactly one climax; scene intensity 10 not on it | E | 1 |
| PLAN-02 | A plant without a payoff, or a payoff without a plant | E | 1 |
| PLAN-03 | A peak away from the climax without a reason | W | 1 |
| PLAN-04 | Step-outline targets outside ±10% of the runtime target | W | 1 |
| PLAN-05 | A kept scene citing a cut strand | E | 1 |
| **GEN-01** | Prompt over the model's limit (C3 L01) | E | 1 |
| GEN-02 | Clip length or resolution not allowed by the model (L02) | E | 1 |
| GEN-03 | Speech over the clip rule (L08, K08) | E | 1 |
| GEN-04 | Fixed description, state line or look block differs from its record (L16, L17) | E | 1 |
| GEN-05 | Start picture attached and appearance re-described (L18) | E | 1 |
| GEN-06 | Readable or backwards text asked of the model (L21) | E | 1 |
| GEN-07 | Negation of a visible thing outside the documented "No ..." lines (L14) | E | 1 |
| GEN-08 | Dialogue or audio sent to a silent model (L28) | E | 1 |
| GEN-09 | Speaker format wrong for the model (L09) | E | 1 |
| GEN-10 | A held take (a turn shot, a shot in a `oner` scene, or `held: yes`) split into chained clips | E | 1 |
| GEN-11 | Model facts older than 30 days on a paid pack | E | 1 |
| GEN-12 | "torch" or another banned word in a prompt | E | 1 |
| GEN-13 | Two on-screen speakers in one clip | W | 1 |
| GEN-14 | A public-release pack while rights are `study_only` | E | 1 |
| GEN-15 | Reasons (`why`, `because`, `purpose`, motif meaning) in prompt text | E | 1 |
| GEN-16 | A take over $2 with no cheaper test first (L30) | W | 2 |
| GEN-17 | Relayed voice without its path; more than 3 named sounds (L11, L13) | W | 2 |
| **FILM-01** | Ladder: a scene before the climax spends the film's tightest size or longest hold, unless the peaks place it there (`peak: tightest_size` or `longest_hold` with a reason, as for counterpoint) | W | 1 |
| FILM-02 | Rhyme: where `rhyme` is set, the payoff shot's lens, angle, size or frame side differs from the plant shot's (shots found by their `plant:` and `payoff:` links) | W | 1 |
| FILM-03 | A character camera rule broken (closer than `limit_before` before `closest`; a `never` item used) | E | 1 |
| FILM-04 | Colour monotony: three consecutive sequences with the same frame value, saturation and temperature | W | 1 |
| FILM-05 | More than two components raised at one story peak (B3) | W | 2 |
| FILM-06 | Three consecutive shots of the same subject from the same setup with the same size, angle and a static camera and no `why` (compliant sameness; matched singles are not counted) | W | 1 |
| FILM-07 | After a scene of intensity 8 or more, the next scene's target shot length is not longer | W | 2 |
| FILM-08 | Film-wide saved-choice counts and places, including the film-level extreme close-up and push-in reserves | E | 1 |
| FILM-09 | Heavy-handedness counts: more than two plant inserts in a scene; music under a beat with an `unsaid`; a light cue on the line that states the point | W | 2 |
| FILM-10 | Motif counts over `motif_spines_max`, `sound_motif_max` or `body_motif_max` | W | 1 |
| FILM-11 | More loud sets than `loud_sets_max` | W | 1 |
| FILM-12 | A scene's `tone` outside PLAN `tone_range`, or over a third of scenes with an undercurrent (D10 TN6-TN7); flagged for the user, never fixed | W | 1 |

Previs has its own checks in `check_blocking.py` (CLASH, OVERLAP, CAMERA; C4) and `render_previs.py` (PREVIS-01 plan fails to compile; PREVIS-02 blocking not OK; PREVIS-03 a figure's facing differs by more than 20° from the derived facing).

### 7.3 Exit behaviour

`0`: finished, no ERROR. `1`: finished, ERROR lines printed (the AI fixes only those, at most 3 rounds). `2`: could not run (missing file, bad command, unreadable story); one plain line says what to do. Every command writes a log line in `For machines/log.jsonl` and, when it changes records, a numbered entry in `00 Start here`'s log. No command ever deletes a record file; `apply` keeps the previous version in `For machines/history/`.

### 7.4 The no-code fallback

On chat surfaces without code, checking is split so that the AI never judges its own work in the reply that wrote it (C5 R12, D1 rule 3):

1. **In the reply (mechanical, 14 checks).** Each unit ends with the mechanical checks of `reference/06` part 1, which need only counting and matching: FORM-05, FORM-06, FORM-07, FORM-08, FORM-12, ID-01, ID-03, ID-06, ID-07, ID-08, COVER-01 to COVER-04 (END count, ID ranges, shortening markers, field presence, coverage). The PASS/FAIL table goes at the end of the saved file (after a `---` line, before the END line); the reply prints one line ("Checked in words: 14 of 14 passed", or only the failures) and marks the file "checked in words".
2. **In a check chat (judgement and arithmetic, 20 checks, plus questions).** At the end of each sequence the resume line names a check chat: a new chat in the same Gem or Project with only that sequence's saved files, the story, `02 Whole-film summary`, `10 Film rules` and `05 Checks in words.md` attached (in two messages when they pass 10 files), and the message "Check my group of scenes." That chat runs `reference/06` part 2: CITE-01, CITE-02, TIME-01 (floors computed from the voice paces), TIME-04, TIME-05, TIME-08, SIDE-01 to SIDE-03, CRAFT-01 to CRAFT-04, CRAFT-06, CRAFT-14, CRAFT-18, REASON-01, REASON-03, REASON-04 and WORDS-01, and, when the user reaches them, step 9's judgement questions and step 10's review questions. It returns `13 Health check.md` in a copy box with that group's REVIEW record and a FINDING for each failure; the next working chat attaches it and fixes the findings first.
3. `00 Start here` shows "Checked by the checker: never" (or the date) in its status, so the gap stays visible.
4. **The real check.** At the end of each sequence (or at least before acceptance) the guide tells the user: "Open the Claude website (the free plan is enough), attach the folder as one ZIP you make with right-click, Compress, and your story file, and type: Check my breakdown." The skill runs `stage.py adopt` (which makes the folder checkable: numbered story, speeches, anchors turned into line numbers, AI-written state fields re-owned) and then `check --all`, `build` and `export all`, and hands back the health check, the book and the exports as downloads. If the website refuses the ZIP ([U]), the fallback is to attach files 00-10 and one group's scene files per check (the website takes at most 20 files per chat).
5. ChatGPT Plus is not a no-code surface: its own Python runs `07 Tools.zip` (D1 §3.3), so ChatGPT users follow surface 2.

---
## 8. The generation layer (add-on C, with D for finishing)

Everything here is derived by `stage.py compile` from records; nothing in a prompt is typed at compile time. It can be tested in this environment up to "prompt pack ready to send": lint-clean, priced and routed.

### 8.1 The master shot prompt (the model-neutral generation spec)

One spec per clip, C3's master template filled from records:

| Template field | Filled from | Rule applied |
|---|---|---|
| SHOT_ID, PURPOSE | shot ID and label; `purpose` | never sent |
| MODEL_TARGETS | routing (8.4) or the shot's logged override | scene model first (K29) |
| DURATION_S, SHOT_MODE | derived clip length; always `single` | one shot per request (C5 R15) |
| INPUTS | approved PIC start and end pictures; reference pictures of the subjects' states, the location, props, the style picture, in C2's stack order; PREVIS guide video when routed | per-model limits from the adapter; faces never dropped |
| CAMERA | `size`, `angle`, `move` (with speed and where it ends), `lens_mm`, `focus` through `phrasebook.json` | unreliable terms rewritten ("85 mm" → "compressed background, shallow focus"; rack focus never trusted to words) |
| SUBJECTS | fixed description pasted word for word + state line + position and facing in image words from the derived prompt side + `travel` in image words + `still` items as sentences + the display level as the size of the visible behaviour | "on the left third of the image, facing right"; "she moves toward the right edge of the frame"; "Her head and hands stay still; only her eyes move" |
| SETTING, LOOK | location phrase and prop states; the look block pasted word for word (with each present character's `skin_light` added when the LOOK's contrast is high or extreme), then the style words | never paraphrased (C5 R4) |
| BEATS, END_STATE | `moment` items; `end` | one main action per 4-5 s (C3 R2) |
| DIALOGUE | speech text verbatim, voice description, parenthetical as delivery, path as a sound path ("through a small intercom speaker") | clip speech rule (K08); listener clips "listens, does not speak" |
| AUDIO | room sound, `effect` items (at most 3), "No background music." | music never in clips (K31) |
| TEXT_ON_SCREEN | always none: "plain, unmarked surfaces" | readable text is composited (K17) |
| EXCLUDE | adapter defaults + `must_not_show` + nouns from failures seen | negative field only where the model has one, else documented "No ..." lines (K18) |
| PHYSICS_NOTES, POST_OPS, CONTINUITY_IN, CONTINUITY_OUT, CONTENT_RISK, SEED, BUDGET | `physics_note` (and `motion`, which drives the previs guide); derived `post_ops`; previous and next `end`; `content_flags` and `policy_route`; take log; takes × seconds × price | physics wording goes into the prompt through the phrasebook; the rest never sent |

**Compile rules.** (1) *Protect first*: the first two sentences name the shot's dominant element (written at Detailed, derived at Standard from `focus_on`, `role` and the first subject) and the carrier of the beat. (2) *Reasons never travel*: `why`, `because`, `purpose`, motif meanings and mood words are never in prompt text (GEN-15). (3) With an approved start picture the prompt is motion only and people are "the woman", "the man" (C3 R1, GEN-05). (4) With a guide video the text carries look, identity and sound only; camera and blocking come from the video (C3 §9D). (5) `prompt_words` swaps apply ("torch" → "flashlight", K19). (6) Glass wording from the phrasebook by glass state (K18): clear → "seen through perfectly clear glass; the room on the camera's side is dark"; reflecting → B3's reflection phrase. (7) No named films, directors, cinematographers, living artists, actors or brands (WORDS-03). (8) Emotion becomes two or three visible behaviours; tone words only for the voice. (9) *Stillness is written*: each `still` item becomes a sentence, a hold of 2 s or more on a static camera adds "The camera does not move." (D15 rule 6), and `must_not` becomes a plain exclusion of that behaviour ("He does not look at her."). (10) Screen direction, vertical too, is stated in every prompt where the subject moves (A4 C5).

### 8.2 The dated adapter files

`adapters/video_models.json`, `image_models.json` and `audio_models.json` hold every model fact the compiler uses, under one date. Builders fill every model C1, C2, C3 and D3 name, from those files, marked with the date checked. Shape (values from C1 and C3, checked 2026-09-27):

```json
{"checked_on": "2026-09-27",
 "models": {
  "kling-3.0-omni": {
    "aliases": ["Kling O3", "Kling 3.0 Omni"],
    "routes": {"fal": "check the endpoint name on the day", "app": "Kling"},
    "length_s": {"min": 3, "max": 15, "step": 1},
    "resolution": ["1080p"], "shapes": ["16:9", "9:16", "1:1"],
    "inputs": {"start_picture": true, "end_picture": true, "references_max": 7,
               "references_max_with_video": 4, "voice": "bound voice (not on fal image elements)"},
    "audio": "native", "silent_option": true, "seed": {"fal": false},
    "negative_field": "negative_prompt", "negative_default": "blur, distort, and low quality",
    "order": ["atmosphere", "elements", "camera", "timed_actions", "dialogue", "ambient"],
    "time_marker": "At the {n}th second", "speaker": "{who} ({delivery}): \"{line}\"",
    "prompt_limit": {"characters": 2500},
    "price_usd_per_s": {"silent": 0.112, "audio": 0.168, "voice_control": 0.196, "route": "fal"},
    "strengths": ["recurring faces with references", "dialogue with bound voice"],
    "lint_extra": ["no seed on fal: reuse the start picture and prompt"]},
  "seedance-2.5": {
    "length_s": {"min": 4, "max": 30, "step": 1}, "resolution": ["480p", "720p"],
    "shapes": ["21:9", "16:9", "9:16"],
    "inputs": {"start_picture": true, "end_picture": true, "references_max": 30,
               "videos_max": 10, "audio_max": 10, "guide_video": "clay reference"},
    "audio": "native, switchable", "negative_field": null,
    "time_marker": "{t0}-{t1}s:", "end_state": "End state:",
    "price_usd_per_s": {"720p": [0.23, 0.47], "route_note": "Replicate cheaper than fal on 2026-09-27"},
    "strengths": ["single takes up to 30 s", "guide video"], "weaknesses": ["several subjects"]},
  "veo-3.1": {
    "length_s": {"allowed": [4, 6, 8], "forced_8_when": ["1080p", "4k", "references"]},
    "inputs": {"start_picture": true, "end_picture": true, "references_max": 3},
    "speaker": "{description} says: {line}", "speaker_quotes": false,
    "negative_field": "negativePrompt (Google Cloud only)", "prompt_limit": {"tokens": 1024},
    "price_usd_per_s": {"standard": 0.40, "standard_4k": 0.60, "fast": [0.10, 0.12], "lite": [0.05, 0.08]},
    "download_within_days": 2}},
 "retired": {"sora-2": ["veo-3.1", "gemini-omni-1.1-flash", "kling-3.0"],
             "kling-2.x": ["kling-3.0"], "seedance-1.x": ["seedance-2.5"], "wan-2.5-2.7": ["wan-3.0"]}}
```

`image_models.json` has the same shape for storyboard, start-picture and reference-picture models (C2); `audio_models.json` for voice design, text to speech, voice changing, lip sync, music and effects tools (D3, D9), with consent gates and commercial terms. `prices.json` holds D13's table (plans, upscaling, images, voice credits) with a URL per price.

**Freshness rule.** Every pack prints "Model facts are N days old". Above 30 days `compile` refuses to mark a pack `paid` and `estimate` prints no money (GEN-11, D13 R7) until a refresh unit has run: an AI with web access re-reads the makers' pages and runs `stage.py refresh-models --propose` with what it found, which writes a proposed diff and checks the files' shape; the user approves any price change; `refresh-models --apply` writes it with the new date. A retired model named in a record compiles to its listed replacement with a warning.

### 8.3 Model words and the phrasebook

`adapters/phrasebook.json` maps record values to words models follow (C3 §4, §6, B1 §15): each size, angle and reliable move; "static shot, the camera does not move"; handheld with an amount; the glass states; "falling" replaced by visible evidence ("hair, cloth and straps drift up; nothing settles"); weightless wording; the documented "No ..." lines; and the unreliable-term rewrites. Adapters decide order and syntax per model (C3 §16); a model with no entry uses C3's generic adapter, and the syntax that works is written back into the file (C3 R26).

### 8.4 Routing and clips

`adapters/routing.json` encodes C1 §5 as rules from derived `needs` to a first choice, a backup and a draft model:

| Need (derived) | First | Backup | Draft |
|---|---|---|---|
| on-screen dialogue of a recurring speaker | kling-3.0-omni (bound voice) | seedance-2.5 or minimax-h3 (audio reference) | omni-flash 360p |
| exact start and end pictures | minimax-h3 (first and last) | kling-3.0 | veo-3.1-lite (app only) |
| exact camera path (guide video) | seedance-2.5 (clay reference) | minimax-h3 (camera reference) | wan-3.0 480p |
| single take over 15 s | seedance-2.5 | wan-3.0 | wan-3.0 480p |
| recurring creature | kling-3.0-omni (4-7 references) | seedance-2.5 | kling-turbo |
| weightless or physics | seedance-2.5 with a guide video, floaters composited | wan-3.0 with a guide video | wan-3.0 480p |
| wide establishing, no dialogue | veo-3.1 (4K) | kling-3.0 (4K) | veo-3.1-lite |
| silent performance | wan-3.0 | runway-gen-4.5 | wan-3.0 480p |

**Scene model.** Per scene the compiler picks one model that meets the most needs of shots with recurring characters (C1 R14). A shot whose need that model cannot meet gets a logged override with its reason, and the review asks drift questions for every override (K29). A project with `licensed_data_only: yes` restricts routing to the models the adapter marks `licensed_data`.

**Clips, and the held-shot rule.** Clip length = screen time + 0.75 s handles each end, rounded up to a length the model allows. A **held take** is a shot with `role: turn`, a shot in a scene with `coverage: oner`, or a shot with `held: yes` (set by the AI when the meaning depends on not cutting). Then, in this order: (1) if the scene model allows that length, one clip; (2) otherwise, for a held take, route to a model that allows it (Seedance 2.5 or Wan 3.0 up to 30 s, C1 R11), logged as an override; if no model allows it, the shot must be redesigned with a motivated cut (GEN-10 error, never a chained split); (3) for every other shot, split only at a planned cut or cutaway, or, as a flagged last resort, chain clip 2 from clip 1's last frame inside one continuous take (C5 R31). The Catch SC10-SH150: 15 s + 1.5 s = 16.5 → 17 s; Kling's maximum is 15; it is a turn shot, so it routes to Seedance 2.5 as one take. A normal 18 s shot on Kling with a planned cutaway is split at the cutaway and stays on Kling (tested in T2).

### 8.5 The hard cases

**The mirror world.** Code picks each shot's `mirror_route` in this order (K02 table, craft-first's direct route added):

| Order | Condition (derived) | Route | What happens |
|---|---|---|---|
| 1 | Readable text in frame | text graphic (d) | always, in addition to any route: the text is drawn by `make_text_graphics.py` in its derived orientation and composited after any flip; the model sees a blank surface |
| 2 | A plot-sided detail of a mirrored element is visible (a STATE `side` with `plot: yes`: ring, raised hand, palm, scar), or a face of a character whose mirror state differs from the location's covers at least 0.10 of frame height | plate (c) | generate the location with the mirrored characters in world orientation; flip that picture; add the normal characters unflipped with an image-edit model; animate from that start picture; no flip after (C2 R5) |
| 3 | Every mirrored element in frame is seen in only one orientation in the whole film | direct (e) | prompt the final picture as it should appear, with derived sides and flipped reference pictures for mirrored elements; no flip |
| 4 | Characters whose mirror state differs from the location's are in frame, small, with no plot-sided detail | flip with mirrored references (b) | flip their reference pictures before generating, generate the location in world orientation, flip the clip (B1 method 1) |
| 5 | The location is mirrored and no character differs | flip all (a) | generate normally, flip the clip |
| 6 | Nothing is mirrored | none | |

Inserts of a sided detail are built from edited stills at their final side and never flipped (SIDE-03, K07). Each output is checked with the derived side questions ("Saye's ring on the hand that looks like her right?").

**The other hard cases.**

| Case | Route |
|---|---|
| Readable text | Never generated. Every TEXT is drawn as a text graphic, composited after any flip; reading floor per K09; mirrored text doubles it |
| Weightlessness and falls | a `motion` item or a `physics_note` means previs level 3 or more and a guide video (C1 R8; C4 routes 2-3); camera `mount` on the moving thing; visible-evidence wording; floating blood beads composited from a Blender layer |
| Violence and filters | Cause, reaction and aftermath as separate shots; impact off screen; gunfire in the sound mix; picture words, not injury words; after two refusals the element moves to compositing or sound and is logged; never reworded a third time (D4 rule 11) |
| A creature | Reference pictures with a scale object; depth guide, never pose guide (C4 R7); lint errors on "robot", "alien", "armour", "humanoid", "glowing eyes"; arrivals by a hard cut from an empty frame |
| Lip-synced dialogue | Voices first (8.6); one speaker per clip; listener clips silent; an audio-reference model first, post lip sync second, a cutaway third (D3 rule 21); visors, glass and hands over the mouth avoid on-screen sync (D3 rule 22); lip sync re-checked after any audio offset (C5 R31) |
| Screens within screens | The screen's content is its own spec built from its CAMERA record (position, lens, ratio, frame rate, overlays); the device shot asks for a dark screen; corner pin from the previs camera track when there is previs; replayed beats use the states at the replayed moment |
| Something appears or vanishes | Two clips from the same locked start picture, one with and one without; a hard cut (C3 Rec6) |
| Rack focus, dolly zoom | Split into two shots or composited; never trusted to words (B1 R14) |
| Slow motion | Only as a making technique whose playback is real time, logged as a `speed` finishing job; slow playback where the camera system bans it is an error (K30) |

### 8.6 Voices first (K16, D3)

Every recurring speaker gets one locked voice before any clip with a visible speaking mouth: designed with a voice-design tool, or recorded by the user or a consenting actor with a RIGHTS consent record; no clone of anyone without one, never a celebrity, a minor or a dead person (D3 rule 16). Add-on C asks the voice question once (decision 14), confirming or changing the small choices made at steps 4 and 6 (`VOICE.source`, `SOUNDPLAN.voice_policy`). `stage.py export voices` writes the voice line script (every speech with its ID, exact words, delivery from the parenthetical and the tactic in at most 8 words, path). Each rendered line is a VOICETAKE (three takes, transcript check, pick by ear; `tts_text` keeps the same words). Paths (earpiece, radio, helmet, recording, through glass) are added in the edit with one saved treatment per path (D3 rules 11, 24). Voices stay `draft` while the place and accents are undecided (D3 rule 6). The checker warns when more than half of a scene's speeches are lip-synced on screen, because A1 and A2 prefer the listener.

### 8.7 Finishing jobs (add-on D)

Code creates FINISH records from shots: `flip` (mirror routes a and b), `composite` (text graphics, screens, plates with people, blood beads), `crop` (to the frame shape), `speed` (16 fps sources to 24; slow generation back to real time), `upscale` (used seconds plus handles, after picture lock, 1080p unless 4K is required, D13 R14), `deflicker`, `grain`, `grade` (each sequence to its style picture), `title`, `lip_sync`, `voice_path`. Simple jobs (flip, crop, overlay a still graphic, speed change, joining) are `ffmpeg` commands the AI writes and runs on code surfaces; tracked or keyed work goes to DaVinci Resolve (free) with a guide. The assembly guide imports `timeline.otio` into Resolve (or the EDL elsewhere) at the frame shape and 24 fps.

### 8.8 Cost and spending rules

1. Nothing is spent until the user sets `spend_cap_usd` once; a batch over the cap is refused by code.
2. Draft on the cheapest tier first (C1 R13); a take over $2 needs a cheaper test first (C3 §17A).
3. Stop a route after 4 failed takes; stop a shot after 10 and change method (control video, compositing, a still with a push made in the editor), never just the wording.
4. Re-forecast after each batch (D13 Recipe 5); if half the video money is gone before half the shots are kept, move the remaining `normal` non-dialogue shots to the budget tier first (D13 R11); over budget, apply D13 R10's cuts one at a time. A `turn` or `must_keep` shot, or a cardinal event, is never cut or downgraded without asking, and any proposal to cut a must-keep shot names the later shot it breaks (A2).
5. Every kept take records the exact model name with date, settings, seed and cost; a wrong clip is traced to the earliest wrong record before anything is regenerated (C5 R28).
6. Watermarks and Content Credentials are never removed; `22 Rights and credits.md` holds the disclosure line (D4 Recipe 6); packs refuse public release while `rights: study_only`, and refuse commercial use of takes whose tool terms are not commercial when `intended_use` is commercial.

### 8.9 What the user sees in a pack

`20 Prompts for AI video/Scene 10 - Saye's kitchen - Kling 3.0 Omni.md`: a short "How to use this page" (with the one-time account or connector setup from C1 P1 when not yet done), then per shot: its one-line description and purpose; the prompt in a copy box; "Attach, in this order:" with plain file names and each picture's job; settings (length, resolution, frame shape, seed); planned takes and cost; "Check in the result:" (yes/no questions built from the records: "same face as the reference", "the torn sleeve on the side that looks like her right", "only her mouth moves, and only at 6-8 s", "no music, no other voices", and, for every face in the frame, "Is <name>'s face as readable and as true in colour as the other faces in this frame?" (B2 R24)); "Save the take as: Scene 10 - shot 150 - take 01.mp4". On Claude Code with a connector, the same pack runs as a batch after the user confirms the cap. Checkpoint E: the AI suggests keep or reject per take from the questions; the user watches every kept take (C1 R18).

---

## 9. The previs layer (add-on B)

**Which shots.** `previs_level` is set at shot design by C4's ladder: 0 for dialogue, inserts and simple coverage (most shots); 2 (grey 3D, a layout check) when meaning depends on camera position, lens or blocking (SC10's reflection two-shot); 3 (a guide video for a video model) for falls, weightlessness, the creature and complex moves; 4 (a performance capture) when a reach or flinch must be exact. The user sees one line: "I suggest grey previews for 26 shots (list). About N minutes of work. Go?" [yes]. Grey previews are offered only in Claude Code on the user's computer, where the AI runs Blender.

**From records to C4 plans, automatically (`make_previs_plans.py`).**

| Plan part | Built from | Rule |
|---|---|---|
| `boxes` | the LOCATION's `object` items (and floor and walls from `size`, except wild walls) | centre from `at` and `base`; one flat colour per material kind (C4 §4.3) |
| `figures` | characters present: each starts at its SCENE `start` item (mark or point, facing, posture); a shot's figures stand where all MOVE records of beats before the shot's first beat have left them (their `to`, `faces` and `posture`) | `height` from CHARACTER `height_m`; fixed colour per character (assigned once, stored in PROJECT `previs_colours`); `facing_deg = (θ + 90) mod 360`, θ the facing angle in plan coordinates (measured from +x, counter-clockwise) toward the `faces` target; a seated figure is a stand-in of height × 0.55 placed on the seat object; a lying body is a box of height_m × 0.45 × 0.25 m on the bed or floor; a kneeling figure is height × 0.7. Seat and bed objects (`furniture: seat` or `bed`) go into the plan's clash exclusion list so a seated or lying figure does not fail `check_blocking.py` |
| `animate` | MOVE records whose beat is among the shot's beats | animated from the shot's frame 1: keys at `start_s` and `start_s + dur_s` (counted from the start of the first shot that shows the beat) converted to frames, with the posture changing at the end key |
| `camera` | the shot's SETUP (`at`, `look_at`, `lens_mm`), sensor 36 mm | `move` adds keys: a push-in travels along the aim line to the next size step at the end; a pan moves the aim point; handheld adds C4's small noise; `mount` parents the rig |
| timing | `screen_time` and handles | frames = round((screen_time + 2 × 0.75) × fps) |
| `resolution` | PROJECT `frame_shape` | width 1280, height = round(1280 ÷ ratio): 2.39 → 1280 × 536 |
| `depth_range_m` | nearest and farthest subject from the camera | minus and plus 0.5 m |
| `stills` | first frame, each `moment` start, last frame | |
| `plan_view` | the room's centre and size | top view; side view for shafts and falls |
| `moments` | the shot's `moment` items with their story lines | for people to read (the kit ignores it); replaces the kit's old key name `beats` |
| mirrored eras | a location seen in both orientations | the plan is stored once, in the LOCATION's `plan_orientation`; the other orientation is derived by x → W − x, θ → 180° − θ (B3 R22), never hand-edited; each shot uses the orientation its scene's frame and the location's mirror state require |

**Not automatic** (the AI writes a fragment `19 Grey previews/extras/<shot>.json`, named by the shot's PREVIS record and merged into the plan): physical motion beyond the free-fall helper (the helper reads SHOT `motion` items, `free_fall | object: <id> | from_z: 9.2 | to_z: 2.53 | start_frame: 1`, and turns them into per-frame keys by z = z0 − 4.9 t², C4 R10, because eased keys float); bodies keyed relative to a moving cage (C4 R11); hinged or custom rigs (the figure's chest doors, the inverted cage); arm and hand poses (box stand-ins have none); performances (phone capture, C4 Rec7); creature shapes. Match cuts and replays share geometry: SC13's playback is rendered from SC06's master previs through `CAM-SHAFT-TOP` (C5 R30). For overlapping slices (K20) one master previs of the physical event is rendered and each shot's `time_slice` names its frame range; code created the master's PREVIS stub (`status: planned`) at step 8, and add-on B fills it.

**Kit files.** `previs_from_plan.py` and `check_blocking.py` are reused unchanged. The five kit plans are copied into `tools/previs/plans/` with two fixes: the key `beats` renamed `moments` (informational only) and `plan_chest_opens.json` corrected to B1 and B4 (K21: static at (0.25, −2.4, 1.7) on 35 mm, the aim tilting from (0, 0, 1.9) to (0, −0.1, 1.55), no push-in and no lens change; the vessel becomes a separate macro insert). `render_previs.py` is new: it renders each plan, runs `check_blocking.py`, compares each figure's facing with the derived facing (PREVIS-03), and writes `19 Grey previews/Scene NN - contact sheet.html` (plan view and stills per shot with the one-line description).

**Tested here.** The machine-first designer compiled SC10's reflection two-shot from B3's scene-10 plan (camera at (−3.5, 1.8, 1.45) looking at (2.8, 1.8, 1.4) on 85 mm; Iona at (2.8, 2.55) facing 0; Saye at (2.8, 1.05) facing 180; Eli at (5.1, 2.0) facing 292.4) and it rendered on bpy 5.0.1 with `BLOCKING OK` and the intended frame; the pipeline engineer judge re-ran it. That hand-made plan (`design/kit_run/plan_SC10-SH060.json`) does not follow this section's rules for frames, depth range, stills and plan view, so it is not the expected output as it stands: WP9 regenerates it by these rules as `tests/fixtures/previs/SC10-SH080 expected.json` (for a 9 s shot at 24 fps: 252 frames; depth range from the subjects ±0.5 m; stills at frame 1, each moment start and the last frame; plan view at the room's centre and size). WP9's acceptance compares only boxes, figures (location, height, `facing_deg` within 1°) and camera keys, and requires a render with `BLOCKING OK`.

**Checks and checkpoint D.** A plan goes to a video model only after `BLOCKING OK` (C4 R21); depth passes use the Raw view and a tight range. Shots that are not framing-critical are `approved: auto` once they pass `BLOCKING OK` and facings within 20°. For framing-critical shots the user sees one contact sheet, `19 Grey previews/Scene NN - contact sheet.html`, and one question: "Reply with the numbers of any that look wrong, or 'fine'." [fine]. Changes are asked in plain words ("lower the camera to knee height"); two or three rounds are normal.

**Into video.** The route per shot is recorded in its PREVIS record's `route`: start and end pictures restyled from grey stills (route 1), a depth guide video (route 2), a grey reference video (route 3), or layers composited (route 5) (C4 §6). Open-model control at 16 fps is tested once and the working route written into the adapter (K29).

---

## 10. The storyboard layer (add-on A)

- **Which frames.** Default: shots with `storyboard: yes` (turn and must-keep shots, about a third). Option: every shot. At Quick depth, one frame per list item marked turn.
- **Two kinds, asked once.** *Quick storyboard*: fixed descriptions only, no reference pictures; composition is what matters. *Consistent storyboard*: reference pictures first (C2 R1); needed if frames will become start pictures.
- **Prompts.** `stage.py compile --storyboard` writes `18 Storyboard/Scene NN - frame prompts.md`: per frame the greyscale style line (C2's default: charcoal and grey marker, four tones, strong light and shadow shapes), framing words from the shot, fixed descriptions and state lines word for word, the look block's light sentence, the reference list in stack order, the save-as name, and three yes/no checks. Bars for 2.39 and all arrows, numbers and labels are drawn by the page, never inside the image (C2 R3). A frame is drawn at the shot's most telling moment; a start picture made later is re-composed for the first instant (C2 §2.2). If previs exists, its grey still is the layout picture.
- **First job.** D5's style test, once, before any storyboard frame: three style directions drawn on three hard shots, and one question, "Which of these three styles? [A]". The answer sets `STYLE.style_picture` and clears `STYLE.provisional`.
- **Records.** Each frame is a PIC record with `use: storyboard`. The AI makes up to two options per shot and keeps the one that passes the frame's yes/no checks; the user is not asked to pick.
- **The page.** `make_views.py` lays approved frames out as `18 Storyboard/Scene NN.html`: frame, shot number ("shot 150"), one-line description, dialogue, seconds, labels added by the page ("HOLD 3 s", "ROOM SOUND", eyeline arrows). The user watches each group of scenes as a slideshow with the sound off and names only the frames to redo; if a beat cannot be read, the shot is revised, not the drawing.
- **Chat path.** Numbered prompts plus the list of files to attach, pasted into the user's image app (C2 R1); under about 150 frames this is cheaper than an API (D1 §5.1).
- **Skipping.** Nothing else depends on storyboards; turning them off changes no other file.

---

## 11. Quality control

### 11.1 Step checklists

Each step's "done test" in section 3 is its checklist; `stage.py check --step N` implements it and the step file lists the same items as yes/no questions for chat surfaces. Additional self-check questions per step (answered from the records just written, each "no" becomes a specific fix):

| Step | Self-check questions |
|---|---|
| 1 | Is every line the odd-lines report lists explained? Did I quote the first and last line of every scene or chapter? |
| 2 | Does each event sentence name a change, in the past tense, with no psychology? Is the climax the last turn of the core value, and the crisis the choice that forces it? |
| 3 | Does every choice the story does not state have a CHOICE with a default and a reason? |
| 4 | Could a stranger draw this character from the fixed description alone? Do principals differ in at least three lineup columns? Is any casting type guessed instead of left open? |
| 5 | Is anything worn, carried or hurt in a scene without a state? |
| 6 | Does every system line cite a plan, character, motif or rule ID? Is the tightest size or longest hold reserved for the climax (or its declared counterpoint)? |
| 7 | Is each turn visible in one frame (its turn picture)? Does the configuration change on every turn, and between turns does every body move for a want or a task I can name? Do more than two departments change at the main turn? Which list item's reason would fit any film? |
| 8 | Name the turn shot: is any earlier shot closer? For each `does`, is there an emotion word? Is anything left to move that should be written as `still`? Which `why` would fit any film? Which invented items could go? |
| 9 | Would the film's turn pictures tell the story with the sound off? Does any shot feel like a different film? |
| 10 | Were the review questions answered by a fresh unit (in chat, a check chat), not the writer? |

There is no "review your answer and improve it" step anywhere (C5 R12); repairs stop after three rounds (C5 R13), then become a CHOICE for the user or a trace to the earliest wrong record.

### 11.2 Review by question

`stage.py questions --sample` builds yes/no questions from records for every turn shot, turn beat and must-keep shot, every shot with mirror, text or violence needs, and a seeded 10% of the rest, each citing the lines it can be checked against ("Does Iona's face change before she says 'Not mint.' (l.454-463)?"; "Is Saye's 'Nothing has happened to the mint...' heard with Saye off screen, and does the story allow it?"). A fresh unit answers them against the story (in chat apps, the check chat of 7.4). Disagreements become FINDING records. LLM judges agree only weakly with people (C5: α 0.47-0.59), so scores are advice, and the user reads three scenes.

### 11.3 The quality rubric (`reference/05 Quality rubric.md`)

Ten criteria, each 0-3. **How**: M = measured by the checker; J = yes/no questions answered by a fresh unit; U = the user's sample. **Anchors** (craft-first's wording): 0 wrong or missing; 1 correct but generic (default coverage, reasons that would fit any film); 2 specific to this story and following the film rules; 3 a head of department would sign it (the choice reveals what the story implies without saying, with restraint).

| # | Criterion | How | 2 means | 3 means |
|---|---|---|---|---|
| 1 | Faithful to the story | M | every line covered; quotes exact; inventions labelled | and every addition approved |
| 2 | Story reading (events, values, turns, climax) | J, U | 80-94% of judge questions pass | 95% or more, and the user agrees on the sample |
| 3 | Shots serve beats | M, J | every purpose names a change; one turn shot per turn | and turn shots are the scene's extremes and match their turn pictures |
| 4 | Reasons | M, J | every `why` anchored; no mood-only reason | and no sampled reason fails the any-film test |
| 5 | Restraint and economy | M | budgets and reserve kept; plants quiet | and no shot a cut could replace; no stacked signals |
| 6 | Continuity and sides | M | no state or side errors | and every state has its reference plan |
| 7 | Rhythm and time | M, J | floors met; holds within budget; scene totals within ±10% | and each scene's rhythm shape shows in its durations |
| 8 | Visual system | M | film rules followed; departures carry reasons | and the ladder escalates and rhymes land (film pass clean) |
| 9 | Ready for generation | M | `compile --lint-only` at step 10 reports 0 GEN errors on the scene model | and every hard case has its references and guide inputs listed |
| 10 | Readable for the user | J, U | plain part above the divider; no abbreviations; At a glance per scene | and a fresh AI unit given only the scene's plain page answers 5 questions about the scene correctly (the user's part stays the 10-question review sheet) |

**Pass**: no ERROR; no criterion at 0; criteria 1, 3 and 6 at 2 or more; total 20 or more of 30. Scores below 2 carry one line of evidence and a fix.

### 11.4 Gold examples and regression

`examples/01 The Catch - scene 10.md` (Standard depth, complete) and `examples/04 The Long Places - chapter 1.md` (chapter digest, the chapter's step-outline scenes, and scene SC05, the mouth at night, fully designed), each with its expected checker output. `stage.py replay` re-checks them after any change to a card, constant, template or checker rule, reading the story text from the committed excerpts `tests/fixtures/The Catch - lines 397-489.txt` and `tests/fixtures/The Long Places - chapter I.md`, which keep the original line numbers through an offset header (decision 16); without them, the CITE checks run only when `--story <path>` is given and are otherwise reported "skipped: story not present"; a change that adds errors or lowers a measured criterion is undone (C5 R32). The same gold units are run by the smallest model in use before a step-file change is kept (C5 R19); this is a manual test step (section 14.3, T9).

### 11.5 The user's review sheet (in `05 How to read your breakdown.md` and at acceptance)

1. From its page alone, can you say what each scene is about?
2. Does each scene's biggest moment get the strongest picture?
3. Can you tell what each shot is for?
4. Is anything added that is not in your story?
5. Does anything feel as if it belongs to a different film?
6. Do the characters look and sound like the people you imagined?
7. Is anything too loud: too many close-ups, music telling you what to feel?
8. Is there a moment you want to see that no shot shows?
9. Do the places and things feel like this story's world?
10. Is anything confusing: who is where, who knows what?

### 11.6 Human checkpoints

| Checkpoint (AI's name) | The user sees it as | When | Blocks | Default |
|---|---|---|---|---|
| Rights | the rights question | step 0 | yes | "It's mine" |
| A | the scene list | after step 1 | yes | keep full length (the scene count is stated, not asked) |
| P (prose) | how the book becomes a film | inside step 2 | yes | plan A; chapter I first as a trial |
| B | the big choices | after step 5 | yes | accept all (7 items at most) |
| C | each group of shots | end of each sequence's step 7 | first sequence only, unless the user says "stop after each group" | "next" |
| Acceptance | the finished check | step 10 | yes | "no" to "Anything you want changed in these three scenes?" |
| D | the grey previews | add-on B | one contact sheet per scene of framing-critical shots | "fine" |
| E | keeping takes | add-on C | per take (spending needs a cap first; never defaulted) | the AI's suggestion |

The user is never asked about format, syntax or IDs; only meaning, taste, money, rights and anything hard to undo. Checkpoint letters never appear in what the user reads.

---
## 12. Conflict resolutions (K01-K31)

"B", "A" and so on name the checkpoint where the user is asked, with the default shown; "small choice" means a CHOICE with `asked: no`, grouped at checkpoint B under "small choices I made". Resolutions that are numbers live in `constants.json`; story-specific ones are worked examples in the cards and in `library/00 Resolved conflicts.md`.

| # | Resolution | Asked? |
|---|---|---|
| K01 IDs | C5 §10.1 as in 5.3: SC01-SC30 in heading order; beats `SC10-B07`; shots `SC10-SH150` in tens; crew labels derived. `library/01 What the codes mean.md` maps every research example (C3 13-04 = SC11; 09-22, 09-15 = SC06; 11-07A/B, 11-08 = SC07; 14-05A/B = SC15; 18-31..33 = SC25; A1's 07 and 7.4 = SC13; C4 `CATCH_SC06_SH14` = SC06-SH140). B2's 23 colour-script rows become `sub_row` items of the VISUAL records for SQ01-SQ09 | no |
| K02 Mirror method | One derived route table (8.5): text graphic always; plate for plot-sided details or large differing faces; direct for elements seen in one orientation only; flip with mirrored references; flip all. A3's "build it mirrored" is dropped for generation; B3's x → W − x, θ → 180° − θ stays for previs plans | no |
| K03 Era boundaries and frame values | Anchored to lines in `WR-MIRROR`, whose `era` items are set through SETVALUE records: era a from l.10 to l.261 ("A hard metal CLACK." l.259; "BLACK." l.261), `frame: original`, every element `original`; era b from l.263 ("Her eyes open.") to l.1563 ("She fires."), `frame: original`, every world element (places, things, Saye and everyone else met there) `reversed` from l.263, Iona, Jude and Eli `original`; era c from l.1565 ("The ship is gone. The stars are gone.") to the end, `frame: reversed`, Iona `reversed` from l.1563 (a STATE change caused by that line), Jude and Eli `original`, world elements still `reversed`. SC06 switches a → b at l.263; SC27 switches b → c at l.1565. An element is mirrored on screen when its STATE handedness differs from its scene's frame (5.6): in era b the world is mirrored around the three, and in era c only Jude and Eli are. Frame handedness per scene and each element's mirror state are derived; element handedness (`original`/`reversed`) lives in STATE. Craft-first's `frame_handedness: turned` for SC10 is superseded: the frame of era b is original and the world elements carry the reversal (worked values below the table). A side the story states for a mirrored element is an apparent side: "Saye's wedding ring. On her right hand." (l.436) is recorded as own left, `origin: inferred`, and "His wedding ring. On his right hand." (Jude, l.1779, era c) as own left too; SIDE-04 compares apparent sides. B2 R21's one-time key flip is dropped: the main light is written in room terms and its frame side is derived per era, so it flips lawfully with the picture at both boundaries | B item 5 (as proposed) |
| K04 Open mirror items | B1's recommendations as RULE records, each listing what it governs: `WR-F-EXCEPTION` (the toy carriage's Fs read as scripted), `WR-WORLD-SCREENS` (world screens mirrored in era b), `WR-COPIED-NAME` (the copied "IONA VALE" label backwards), `WR-SCREEN-TEXT-B` (visor, wrist and monitor text backwards in era b with doubled reading time), `WR-REPLAY` (the SC06 recording flipped when shown in era b), `WR-TITLES` (title cards always read normally) | B item 5, grouped (accept) |
| K05 SC13 turn | A2's value analysis: main turn SC13-B15 carries the scene's one push-in, on Iona, landing at `extreme_close_up`: one use of each film-level saved choice (the extreme close-up and the push-in, 5.8), and the film's tightest size, which K12's peaks place in SC13. On "You." the cut lands on Iona (A1 and A2 agree). Eli's closest single so far is `close_up`, one step wider; his near-lens look (a reserved choice) is spent on "Now he looks at her."; `CR-ELI` forbids push-ins on him and sets `limit_before: medium_close_up` until SC13 (FILM-03) | no |
| K06 SC13 geography | B3's tested floor plan is the location's set plan; every eyeline is derived from it (GEOM-01) and replaces A1, A2 and A3's text in the cards; "staging assumed" stays on the scene | no |
| K07 Reflection two-shots and rings | B1/B3 geometry for SC10 and SC29 (camera along the dividing plane, level, 85 mm from well back, profiles at the edges, ringed hands nearest the camera) as `RC-01` (at most 2 uses, SC10 setup A and SC29); SC10's 85 mm is `LX-01`. The SC29 hands insert follows B3's ladder; A2's rhyme moves to the two reflection two-shots (PLANT `rhyme`, FILM-02). State lines say "hand nearest the camera"; image sides are derived; ring inserts are edited stills with `flip: never` | small choice |
| K08 Words per clip | Σ(words ÷ pace) ≤ clip length − 1.0 s; default 2.5 words per second (17 words in 8 s), per voice `pace_wps` (Saye 2.0). A1's 16-24 is retired | no |
| K09 Reading time | max(2.0, 1.0 + characters ÷ 13); plot-critical text (emphasis 2 or more) at least 2.0 + 0.5 × words; doubled when mirrored ("Goods only. No persons." = 4.0 s, 8.0 s mirrored). Non-text inserts follow their emphasis | no |
| K10 Holds and handles | A2's dialogue formula is a floor per speech; A4's intensity table sets non-dialogue shots and cut placement. Pause tiers, one definition with no gaps, as half-open ranges: short [0, 1.0) s; medium [1.0, 2.5) s ("(beat)" = 1.0 s); long [2.5, 4.0] s ("Silence." and "She waits." 2.5-3 s; "A long moment" 3-4 s); above 4.0 s a `hold`, which needs a saved choice (TIME-08); at most two long pauses per scene; a turn's reaction at least 2.0 s. The long tier starts at 2.5 s rather than A1's 3 s so that "Silence." counts as long and no range is left unnamed. Handles 0.75 s | no |
| K11 Plant loudness | B4's emphasis ladder is the only scale: quiet plants (0-1) match their neighbours (A3 R22); a plot-event plant may be 2 with nothing pointing forward (A1's clear insert) (CRAFT-08) | no |
| K12 Climax and peaks | PLAN names `crisis` and `climax` separately. Default for The Catch: crisis SC24 ("She deletes the way home.", l.1412); climax SC26-SC27 (the crossing; the film's one scene-intensity 10, played in counterpoint). Peaks: colour saturation and red-green contrast at the SC24 fire; largest motif payoff SC25 (the chest opens); the camera's break SC26 ("She pushes gently away from the rail."); the sound rupture SC26 (the ship's hum drops out); the longest hold and the only sound emphasis 3 on SC30's last shot (the pump over black); the tightest size in SC13, declared as `peak: tightest_size \| scene: SC13 \| reason: the confession's turn lands inside Iona; the climax is played wide and still, in counterpoint`, so FILM-01 is silent on the default path. The ladder escalates by size and hold together. The SC24 and SC25 readings are shown beside the default | B item 1 (SC26-27) |
| K13 Sequences | One list from step 2. Default for The Catch: B3's nine stretches as SQ01-SQ09 (SC01-05, SC06, SC07-10, SC11-13, SC14-17, SC18-22, SC23-25, SC26-27, SC28-30); B2's 23 rows are VISUAL `sub_row` items | no |
| K14 Scales | Separate names and ranges: `beat_intensity` 1-5, `scene_intensity` 1-10, `emphasis` 0-3, `sound_emphasis` 0-3, `frame_value` and `saturation` 1-5, `previs_level` 0-5, `standin_level` 1-5. B1's emphasis device and B4's added signal merge into `added_emphasis` (0 or 1 per beat). Never converted | no |
| K15 Veo dialogue | Per-model adapter syntax: Veo and Omni colon form without quotes; Kling, Wan and LTX quoted; the freshness rule forces a re-check before a paid batch | no |
| K16 Voices | Voices first for every recurring speaker, one locked voice each; native in-clip voices only for drafts and one-line parts; off-screen delivery wherever A1 and A2 choose the listener (8.6) | no |
| K17 Readable text | All readable text is composited from text graphics; models draw only illegible background text; a quoted sign in a prompt is GEN-06 | no |
| K18 Negation and glass | Exclusions go to a negative field where the model has one, otherwise only the documented "No ..." lines; never "no people" in picture prompts. Glass wording by glass state (8.1 rule 6) | no |
| K19 "Torch" and light side | `prompt_words` swaps "torch" for "flashlight" in every compiled prompt; script quotes keep "torch". The SC01 bolt-hole insert takes B2's main-light side (frame-right); B1 Ex1 is corrected in `library/02 Errata.md` | no |
| K20 The SC06 fall | Expanded screen time built from overlapping real-time slices, never slow motion: one master previs `PV-SC06-MASTER` of the physical fall (z = z0 − 4.9 t²); each shot's `time_slice` names its frames; overlaps allowed; the yellow stripe never shrinks in frame across the fall shots (a review question on SC06); stated in `CAMSYS.time_rule` | small choice (named in B item 7) |
| K21 Chest-opens camera | B1 and B4: static 35 mm looking up, a motivated tilt down, the vessel by a macro insert, then static 50 mm on Iona; no push-in; `plan_chest_opens.json` fixed (section 9) | no |
| K22 SC10 staging | Default: B3's tested version (camera A 6.3 m back on the table's axis at 85 mm under `LX-01`; Iona sets the lamp down before the raised hands, an invention listed for keep or cut; Eli small and deep in the centre). Option b: A2's variant with Saye in the foreground. Shown again at checkpoint C for SQ03 | small choice |
| K23 Previs formats | C4's per-shot schema is canonical; B3's scene JSON becomes the LOCATION set plan, compiled per shot by `make_previs_plans.py` (tested on bpy 5.0.1 here; C4's 5.2.2 LTS is the target); B3's `plan_to_blender.py` is retired; resolution derived from the frame shape | no |
| K24 Frame shape | Chosen once. Default 2.39:1. Derived: storyboard bars; generation size per tool (Seedance 21:9; GPT Image 2560 × 1072; other 16:9 sources with heads, hands and text out of the top and bottom eighths); previs 1280 × 536 | B item 2 (2.39) |
| K25 Runtime | v0 at checkpoint A: 1,926-2,309 s (D2 §6, D13 §4.1), printed as "about 35 minutes (32 to 38; the page count suggests up to 44)" (the 44 is A3's page count, not v0), so C1's 20-minute budget scales by about 1.75; v1 from shot durations at step 10. Keep full length, or give a target (compression plan in step 2; lines never rewritten) | A, its one question (keep everything) |
| K26 States, sides and fixed descriptions | C5's state IDs with boundaries from continuity; B5 is the source of fixed descriptions; rings and wounds in state lines, never in fixed descriptions; C3's example keys replaced. Defaults: Iona's torn sleeve and skinned palm own right; Jude's wound own right shoulder (inferred from the ringed "good hand"); Eli's half-smile and parting own left, his one shoe on the right foot; the figure 2.4 m; Saye "fifties" (story); the blanket "OSTREL, stitched on it in blue" (story), rendered dark navy (design choice). Casting types stay `open` placeholders until pictures exist | small choices |
| K27 Locale | WORLD record: an unnamed British city, present day, driving on the left, British English voices, each marked `inferred` (from "torch", "night bus", "I know how a lift works"). Voices stay `draft` until answered | B item 3 |
| K28 Data conventions | Record text (5.1); lowercase snake_case enums compared ignoring case; `none`, never null; `yes`/`no`; one gerund field named `tactic`; A3's infinitives converted | no |
| K29 Model routing | One scene model by default; per-shot overrides logged with their reason and followed by drift questions; open-model control tested once and the working route written into the adapter | no |
| K30 Slow motion | Slow generation only as a technique whose playback is real time, logged as a `speed` finishing job; slow playback banned in The Catch's camera system (CRAFT-16) | no |
| K31 Music | Every clip music-free. The film's policy is the user's: default none for The Catch (the pump is the only sound to reach sound emphasis 3) | B item 4 (none) |

**K03 worked values for SC10** (era b, `frame: original`; T2 checks them):

| Element | Handedness (STATE) | mirror_state (derived) | What the picture shows |
|---|---|---|---|
| Iona, Jude, Eli | original | normal | as in era a; Iona's raised hand is her own right, the hand nearest the camera |
| Saye | reversed | mirrored | her own right appears as her left; her ring, own left, appears on her right hand, the far hand in the reflection two-shot |
| The kitchen, the mint and the other things of Saye's world | reversed | mirrored | the room is shown reversed; its readable text follows `WR-WORLD-SCREENS` and the text-graphic route (8.5) |

The vocabulary problems in the brief are resolved by the word list (5.7).

---

## 13. The user's experience

### 13.1 The first message in each app

The first message is the same everywhere, `Break down my story.`, with the story attached where the app needs it; the resume message is the same everywhere, `Continue my breakdown.`

| App | Once, before the first story | What the user does first |
|---|---|---|
| Claude desktop with a connected folder (Cowork) | Turn off "Help improve our AI models"; download the Stage folder; upload `08 Skill for Claude apps.zip` in Customize > Skills; connect the Stage folder; put the story in `My stories/` | types `Break down my story.` |
| Claude Code (needed for grey previews) | Same privacy setting; open the Stage folder; the skill loads from `.claude/skills/` | puts the story in `My stories/` and types `Break down my story.` |
| Claude website | Privacy off; Settings > Capabilities > code execution on; Customize > Skills > upload `08 Skill for Claude apps.zip`; test "Which skills do you have?"; make a Project for the film | attaches the story and types `Break down my story.` |
| ChatGPT Plus | "Improve the model for everyone" off; make a Project; paste `00 Paste into instructions.txt`; upload the other chat-kit files including `07 Tools.zip`; choose Thinking | attaches the story and types `Break down my story.` |
| Gemini (or any chat app without code; Gemini AI Pro or higher) | Keep Activity off; never free AI Studio; make a Gem: paste `00 Paste into instructions.txt` into its instructions and add the six knowledge files 01-06 (not the ZIP); keep the step files 08-12 to attach per chat | attaches the story and `08 Steps 00-02 - start, reading, plan.md`, and types `Break down my story.` |

(Menu names follow the apps' help pages on 27 Sep 2026; the guides say "if your app shows different names, follow the app".)

### 13.2 The welcome (example first, one question)

```
Hello. I'll turn The Catch into a scene-by-scene plan for making it as a film,
including with AI picture and video tools.

Here is one finished moment from your story, so you can see what you'll get:
  Scene 10, shot 150. Close-up, camera still. Iona chews the leaf. She stops,
  frowns, chews once more, slowly. "Not mint." We stay on her face while Saye
  answers off screen. About 15 seconds.
  Why: "Her face changes." The scene turns inside her mouth, so we don't cut away.

How it works: I do the work. You'll be asked for real decisions about four times
(the scene list, the big choices, the first group of shots, and the finished
check), each with an answer ready if you just say "defaults". You can stop any
time and carry on another day: everything is saved in files with plain names.

I'll make a complete shot plan (standard). Say "quick" for one line per shot,
or "detailed" for extra detail on every shot.

One question first:
1. Is this story yours, or do you have permission to adapt it?   [It's mine]
```

### 13.3 The checkpoints, as the user sees them (The Catch and The Long Places)

Each checkpoint is named by what it is; the letters in the headings below are the AI's names and never appear in the messages. Steps are counted from 1 ("step 2 of 12" is step 1 here).

**Checkpoint A: the scene list**

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

**Checkpoint P (prose): how the book becomes a film**

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

**Checkpoint B: the big choices** (at most 7 items; the three marked * would redo the most work if changed later)

```
Done: steps 4 to 6 of 12 (world and style; characters, places and things; continuity).
Example: Saye's fixed description now reads "Dr Saye, a slight, upright woman in her
  fifties, ...". It goes word for word into every picture prompt with her.

The big choices. Reply "defaults", or answer by number.
*1. The climax: the crossing beside the ship (scenes 26 and 27), where the main
    question is settled for good. "She deletes the way home." (scene 24) is the
    decision that forces it; the chest opening (scene 25) is the biggest reveal.   [26-27]
*2. Style and frame shape: like a real film, clinical and plain (for now: you'll
    choose by eye when pictures are made); wide cinema frame, 2.39 to 1, because
    people face each other across glass and tables.                              [yes]
 3. Place and time: the script never names a country. An unnamed British city,
    today, cars on the left, British voices (from "torch" and "night bus").       [yes]
 4. Music in the finished film: none; the pump and the engine click do music's
    job. No clip ever has music baked in.                                          [none]
*5. The mirror world: normal until "CLACK." (line 259); from "Her eyes open."
    (line 263) the world is mirrored around the three of them until "She fires."
    (line 1563); after that only Eli and Jude stay mirrored. Plus 6 detail rules
    (the toy carriage's Fs read normally, world screens mirrored, ...).            [as written]
 6. What each main character's appearance must say: Iona, a working body whose flat
    hand tests whether things will hold; Saye, tidy grey control with one living
    thing that becomes her proof. (Jude, Eli, Nell and the figure are in 07.)      [all fine]
 7. Small choices I made: 23 in 01 Choices, including which hand and shoulder carry
    each injury, how the kitchen in scene 10 is staged, and the fall in scene 6
    told longer than real time from overlapping real-time pieces, never slow motion. [accept]
Next: I'll write the film's camera, light and sound rules from these answers,
then design scene 1.
```

**Checkpoint C: each group of shots.** The first group's message waits for the user; later groups are reported and the work carries on. A later group (group 3):

```
Done: group 3, scenes 7 to 10 (step 8 of 12). 58 shots, about 4 minutes.
Example: shot 150 is the turn of scene 10: Iona's close-up held 15 seconds, from
  the first chew through Saye's "Nothing has happened to the mint...".
Made: 11 Scenes/Scene 07 to Scene 10 (designs and one-line shot lists).
  Checked: no problems. One added detail changes a scene, to keep or cut: Iona sets
  the lamp down before she raises her hand (scene 10). 6 small additions kept
  (listed in 01 Choices).

Scene 10 - Saye's kitchen - 20 shots and a title card - about 1 min 36 s
 shot 10    4 s   Saye's view at her door: the three on the step, the blood, then the flask
 shot 80    9 s   medium, camera A: the reflection; both raise the hand nearest the camera
 shot 150  15 s   the turn: close-up, Iona chews, stops, chews once more; "Not mint."
                  We stay on her through Saye's answer
 (the other 17 shots are listed in the scene file)
Needs you: nothing. I'm carrying on with group 4; tell me anything you want changed.
Next: scene 11, the treatment floor.
```

The first group's message (group 1, scenes 1 to 5) has the same parts and adds, before its question, the film rules in five plain lines (the defaults for The Catch):

```
The film's rules, in five lines (a change here costs little now):
  1. The camera stays still, at the eye height of the person the scene belongs to.
  2. It breaks that rule once, in scene 26, when she pushes away from the rail.
  3. Eli is never pushed in on; his closest shots are saved for scene 13.
  4. The film's tightest shot is saved for scene 13; the crossing is played wide and still.
  5. No slow motion and no music: the pump and the engine click do music's job.
Needs you: reply "next", or tell me what to change.
After this group I'll carry on and show you each group; say "stop after each group"
if you prefer.
```

**Acceptance: the finished check**

```
Done: step 11 of 12, the health check. In short: one thing needs you (reading three
  scenes); 14 small fixes I made; 3 warnings (listed in 13 Health check).
Example: the film runs about 36 minutes in 468 shots; making it with AI would cost
  about $2,900 to $7,600 and 45 to 90 hours of watching takes (14 Time and cost).
Made: 13 Health check, 14 Time and cost, and a first version of 15 The breakdown.
Needs you: please read three scenes in 15 The breakdown (about 20 minutes): 26 (the
  climax), 13 (the most talk), 06 (the most action), with the 10 questions in
  05 How to read your breakdown.
  Anything you want changed in these three scenes?                                  [no]
Next: I'll finish the book, the spreadsheets, the captions and the timeline.
```

(The numbers in the acceptance example are illustrative; step 10 prints the computed ones. In chat apps without code the three scenes are read as the plain parts of their scene files.)

### 13.4 Every reply's ending

Four parts, always in this order: **Done** (with progress: "scene 11 of 30, step 8 of 12"); **Example from your story** (one concrete line); **Made** (files); **Needs you** (nothing, or one question with its default). Then **Next** (one step). A new craft word is explained in one plain sentence the first time and added to the word list in `00 Start here`. In chat apps two more lines follow:

```
Save as: 11 Scenes/Scene 11 - Treatment floor.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 02 Whole-film summary,
10 Film rules, 10 Steps 07-08 - scenes and shots, your story and Scene 11 - Treatment
floor; type: Continue my breakdown. Next is scene 12.
```

At the end of a group of scenes the resume line first names the check chat: "Next: a check. New chat in this project; attach the files of scenes 7 to 10, your story, 02 Whole-film summary, 10 Film rules and 05 Checks in words; type: Check my group of scenes." (7.4).

**What the user can type any time** (their own words work too): *Where are we?* · *Why shot 150?* · *Change ...* (an impact list, then only the affected work is redone) · *Go deeper on scene 13* · *Quick* / *Standard* / *Detailed* · *Redo step 6* · *Stop here* (save and hand-over) · *Check* · *continue* · *next* · *defaults* · *Make storyboards* · *Make grey previews* (Claude Code on the user's computer only) · *Get it ready for AI video* · *Plan the edit*. When the user chooses quick, the AI says once: "Quick plans can't be turned into AI video prompts until a scene is made standard. Say 'go deeper on scene N' for the scenes you want to make."

### 13.5 Resuming, and a full chat

| Surface | Resume | When the chat is long |
|---|---|---|
| Cowork, Claude Code | `Continue my breakdown.` The AI runs `stage.py status` and answers in one line ("Yesterday we finished scenes 1 to 12. Next: scene 13. Nothing is waiting for you.") | Nothing lives only in the chat; after the app compacts, the AI re-runs `status` and re-reads the step file. Scenes may go to helper agents, each with its own handout; `apply` takes one at a time |
| Claude website, ChatGPT Plus | New chat in the same Project; attach the newest save ZIP; `Continue my breakdown.` The AI unpacks it and reads `00 Start here` | One sequence per chat by default (`limits.json`), or earlier if the app says it is summarising or usage passes about 80% (D1 rules 5-6): the AI finishes the unit, makes the save ZIP (`NNN Save - The Catch - after scene 10.zip`) and says "This chat is getting long. Start a new chat in this project, attach the save file, and type: Continue my breakdown." ChatGPT download links expire: save at once |
| Gemini, no code | New chat in the Gem; attach the files the resume line names (the step file, the story, `00 Start here`, `02 Whole-film summary`, `10 Film rules`, `08 Places and things` when needed, the previous scene file); `Continue my breakdown.` | One sequence (3-5 scenes) per chat; at the budget the AI rewrites `00 Start here` and `02 Whole-film summary` in copy boxes and gives the exact message for the new chat; at the end of each sequence the resume line names the check chat (7.4) |

App memory features are turned off or ignored (D1 rule 10); files are the only memory.

### 13.6 When something goes wrong

| Problem | How it is spotted | What happens (the user types only the bold word) |
|---|---|---|
| Reply cut off | no END line; count differs from the approved list | **continue**: the AI re-sends from the start of the last complete record; a record is never split across replies |
| Records silently skipped | IDs differ from the approved list; a shortening marker | **continue**: the AI sends only the missing IDs, then the END line (D1 §6.2 prompts) |
| Chat full, or the AI forgets a decision | budget reached; it cannot quote a CHOICE | hand-over: new chat with the resume line |
| Format slip ("medium closeup", an unknown field) | checker | tidy fixes spelling, case and known synonyms itself and logs them; real problems come back as "Fix only these", at most 3 rounds, then one plain question |
| A rule broken ("torch" in a prompt; 22 words in an 8-second clip) | checker | same loop |
| The user changes an early choice ("make it 16:9") | the user says so | the AI lists what it affects in plain words ("the picture edges of 214 shots, 31 grey previews and every prompt page; about 20 minutes"), asks once if costly, redoes only those |
| A file is lost | `00 Start here` lists what should exist | Claude surfaces restore from git or the save ZIP; chat apps redo that scene |
| The app cannot read an attached file in full | the AI cannot quote the first and last line | it asks the user to paste that part |
| A fact not in the story | CITE checks | flagged "not found in the story"; fixed, or relabelled `invented` |
| A text step refuses violent content (SC06's gunshot) | refusal | the AI states once that this is pre-production and uses production words ("gunshot sound effect", "wound make-up"); if refused again, logs it and suggests another model or app; never disguises the content (D1 §6.5) |

### 13.7 `00 Start here.md` (the project story for a pipeline user)

The user's own "project story" convention, applied to each project. Sections 1-6 are the file's plain part (headings with `#` and `##` only, G13), in order:

1. **Where things stand**: step and progress; "Checked by the checker: <date> | never"; the count of small additions kept ("41 small additions kept; the list is in 01 Choices"); anything waiting for the user.
2. **Next step**: the exact message to type or paste, for this app and for the other apps.
3. **Big choices so far**: numbered, one line each, with the CHOICE number ("1. The whole script, about 35 minutes (choice 5)").
4. **Files in this folder**: the numbered list; each number is the file's number; what each is for, one line.
5. **Word list**: every craft word used so far, with its plain meaning.
6. **Log**: numbered, dated entries of what was done, what failed and what changed ("017 2026-10-02 Scene 10 designed: 11 beats, 20 shots; one invention listed (the lamp)"; "018 ... Checker found 2 problems in scene 10; fixed").
7. The divider line, then the PROJECT record and the END line.

On code surfaces code rewrites sections 1-4 after every unit and appends to the log; the AI adds the example lines. In chat apps the AI rewrites it at stop points only.

---
## 14. Build plan and test plan

### 14.1 Build rules for every builder

1. Python 3.11 standard library only (previs: bpy). A plain note at the top of every code file saying what it does; full plain-word names; no abbreviations in names or messages.
2. Field names, record types, values and check IDs come only from `schema.json`, `constants.json` and section 7.2. A builder who needs a new field adds it to the schema first and records it in `00 Project story.md`'s log.
3. Cards and step files cite research by code and section ("B1 R14"); they never state a rule the library does not hold; numbers are named from `constants.json`, never restated.
4. Every user-facing sentence obeys section 5.7 and the user's rules: plain words, one word per thing, example first, no abbreviations.
5. No personal information (no email addresses, names of real people other than cited authors, account details) in any file, prompt or web request. The user's whole stories are never committed; only the two excerpts named in decision 16 (section 15) may be, as test fixtures; tests read the whole stories from a path given at test time.
6. Every work package ends with its acceptance test passing and a numbered entry in `00 Project story.md`.

### 14.2 Work packages, in order

| WP | Files the builder writes | Depends on | Acceptance |
|---|---|---|---|
| **WP0 Skeleton** | Folders of 2.1-2.2; `00 Project story.md` (started); library copies renamed `<code> <plain title>.md` with digests; the C4 kit copied into `tools/previs/` | none | tree matches 2.1-2.2; library files open |
| **WP1 Schema and rules** | `schema/schema.json` (every type and field of 5.5 with meaning, kind, values, depth, writer, `writer_when`, `chat_writer`, `filled_by_step`, `defines_id`, plain label, example); `schema/steps.json` (units, card parts, the unit order of steps 7 and 8); `rules/constants.json`, `words.json`, `limits.json`, `tone_defaults.json`; `reference/01 Record format.md`, `02 Word list.md`, `04 Rule order.md` | WP0 | JSON loads; every field in 5.5 present with a depth, one writer (or a `writer_when`) and a `filled_by_step`; every retired word of 5.7 in `words.json` |
| **WP12a Templates and gold fixture (early)** | `templates/*` (needed by `new`); `examples/01 The Catch - scene 10.md` and `02 The Catch - scene 10 - context.md` written by hand from the gold content below (the whole-film records SC10 cites: PROJECT, CHARACTER and VOICE for the four present, LOCATION with B3's set plan, PROP, TEXT, MOTIF, STATE, CAMSYS, CAMRULE, RESERVE, LENS, LOOK, VISUAL, SOUNDPLAN, WR-MIRROR); `tests/fixtures/The Catch - lines 397-489.txt` (decision 16); a chat-saved copy of the same scene (quote anchors, AI-written state fields, two batch files) for `adopt` | WP1 | each template holds its plain part, the divider, every field of its record types by depth and the END line; every Standard field of 5.5 present for SC10; the gold content list below met; the fixture is shared by WP4, WP5, WP6, WP8 and WP9 (WP2's acceptance parses it) |
| **WP2 Records and project files** | `record_format.py`, `project_files.py`, `stage.py` (dispatcher; `new`, `status`, `apply`, `pack`, `unpack`); fixtures for grammar G1-G13 including a cut-off file and a file with shortening markers | WP1, WP12a | fixture parse results equal expected; FORM-01 to FORM-13 fire on their fixtures; a write-read round trip leaves files unchanged; the WP12a fixture parses |
| **WP3 Story reader** | `read_story.py`; `read`, `lines`, `selftest`; fixtures: a short invented screenplay in The Catch's dialect, a Fountain sample, an FDX sample, a prose sample with chapters, DOCX and EPUB made from text by the test with `zipfile` | WP2 | T1 (14.3) |
| **WP4 Derive, check and adopt** | `derive_fields.py`, `check_records.py`, `film_pass.py`, `adopt_folder.py`; `check`, `build`, `impact`, `questions`, `adopt`; one faulty fixture per build-1 check. Split across builders by check family (FORM, ID and CITE; COVER, TIME and STATE; SIDE, GEOM and the derivations; CRAFT, REASON, INFO and WORDS; PLAN, GEN and FILM), each family its own group of functions | WP2, WP3, WP12a | every build-1 check fires on its fixture and is silent on the WP12a fixture; T2's derived numbers on it; `adopt` turns the chat-saved SC10 fixture into a project on which `check --all` exits 0, with each re-owned field logged as N |
| **WP5 Handouts and the loop** | `make_handout.py`; `next`, `handout` | WP4 | handouts for U-07-SC10 and U-08-SC10-B1 built from the WP12a fixture with stub step files and stub card parts at their target lengths, within the Claude ceiling of `limits.json`; pre-issued ID blocks present; instruction first and last (re-measured with the real step files and cards in WP14) |
| **WP6 Views and exports** | `make_views.py`, `make_exports.py`; `export` | WP4 | on the WP12a fixture: the plain part and divider of every record file; shot-list CSV with the columns of 5.9 and the byte-order mark; SRT and WebVTT pass format checks with the timing of 5.9; OTIO structural check; `breakdown.json` validates (T8 on T3's output stays in the test phase) |
| **WP7 Estimate** | `estimate.py`, `adapters/prices.json` | WP4 | v0 for The Catch between 1,926 and 2,309 s with central about 2,118 s (D13 §4.1); money withheld when prices are over 30 days old |
| **WP8 Generation** | `adapters/video_models.json`, `image_models.json`, `audio_models.json`, `routing.json`, `phrasebook.json`; `compile_prompts.py`, `make_text_graphics.py`, `refresh_models.py`; `compile`, `graphics`, `refresh-models` | WP4 | on the WP12a fixture: `compile --scene SC10` gives 0 GEN errors; SH150 one clip on Seedance 2.5; `--force-model veo-3.1` gives the colon speaker form without quotes; a non-held 18 s fixture shot on Kling splits at its planned cutaway (T7 on T3's output stays in the test phase) |
| **WP9 Previs** | `make_previs_plans.py`, `render_previs.py`; kit plans fixed (`moments`; chest-opens per K21); `previs`; `tests/fixtures/previs/SC10-SH080 expected.json` regenerated by section 9's rules | WP4 | the SC10-SH080 plan compiled from the WP12a fixture matches the expected file on boxes, figures (location, height, `facing_deg` within 1°) and camera keys, and renders with `BLOCKING OK`; T6 |
| **WP10 Skill text** | `SKILL.md`; `steps/00`-`16`; `reference/05 Quality rubric.md`, `06 Checks in words.md`, `07 Report and message formats.md` | WP1, WP5 | SKILL.md under 500 lines and 4,500 words; each step file has every section of 2.3, including its chat twin; every command named exists; WORDS-02 and WORDS-04 clean on `reference/07` and every checkpoint message |
| **WP11 Cards** | `cards/01`-`24` (split among builders: 01-04 and 19; 05-08, 16, 17; 09-12, 14; 13, 15, 18, 20; 21-24), each with the named parts `steps.json` loads | WP1 | anatomy of 6.4 or 6.2 complete; lengths in range; `WORDS-02` and `WORDS-04` clean on their text; every rule cites the library |
| **WP12b Gold and examples (final)** | the WP12a gold brought to its final form against the real cards and step files; `03 The Catch - scene 10 - expected check.txt`; `examples/04 The Long Places - chapter 1.md` (CHAPTER digest; the chapter's plan-A scenes; SC05 designed at Standard) with context, expected check and `tests/fixtures/The Long Places - chapter I.md`; templates revised if the cards changed them; `09 Example - The Catch, scene 10/` | WP4, WP9, WP10, WP11, WP12a | `stage.py replay` clean; the gold passes the rubric at 3 on criteria 1, 3, 4 in a critic's reading |
| **WP13 User documents and kit** | `README.md`, `CLAUDE.md`, `01`-`06` guides; `build_kit.py`; `07 Chat kit/`, `08 Skill for Claude apps.zip`, `AGENTS.md`, `reference/03 Field guide.md` | WP10, WP11, WP12b | the chat kit has exactly the 13 files of 2.5, `00` at most 6,000 characters, each knowledge file within its length in 2.5 and the six together about 60,000 words; the ZIP has `breaking-down-stories/SKILL.md` at its top folder; WORDS-04 clean on guides |
| **WP14 Tests** | `tests/run_tests.py` (runs all fixtures, replay, format checks); instructions for T3-T10 in `tests/01 Test plan.md` | WP2-WP9, WP12b | T0; WP5's handout sizes re-measured with the real step files and cards, all within `limits.json` |
| **WP15 Library notes** | `library/00 Resolved conflicts.md`, `01 What the codes mean.md`, `02 Errata.md` (B1 Ex1 light side, K19; C3's example keys superseded, K26; A3 Ex5's "word for word" refrain corrected per D2 §8.2) | WP0 | every K01-K31 row present with its research references |
| **WP16 Project story** | `00 Project story.md` completed (goal, state, how the pieces fit, word list, numbered log, next step) | all | read by a critic for plain language |

Parallel lanes: WP0 → WP1 → WP12a → WP2 → WP3 → WP4 → {WP5 to WP9}, with {WP11, WP15} in parallel from WP1; then WP10 → WP12b → WP13 → WP14 → WP16.

**Gold SC10 content** (written in WP12a, finished in WP12b), from user-first's walkthrough with the judges' corrections: 11 beats (A2's intensities 2 2 3 3 3 4 5 4 3 4 5; main turn B07, second turn B11); set plan and setups from B3's tested plan (room 6.0 × 3.6 × 2.5 m from the south-west inside corner, west wall wild; table at (2.8, 1.8); Iona's mark (2.8, 2.55), Saye's (2.8, 1.05), Eli's (5.1, 2.0); camera A at (−3.5, 1.8, 1.45) looking at (2.8, 1.8, 1.4) on 85 mm, through the wild wall; camera B beside Saye's shoulder on 50 mm for Iona; camera C behind Iona's shoulder on 50 mm for Saye; camera F high in the north-west corner on 35 mm); 20 shots and a title card: SH080 the reflection two-shot is **medium** (85 mm from 6.3 m frames about 2.67 × 1.12 m), `RC-01`, `LX-01`, plate route, previs level 2; SH090 and SH100 the ring inserts, edited stills, `flip: never`; SH110 Eli and the cap in camera A's deep frame (the rack focus A2 implies split out, B1 R14); SH130 Saye's hand moving toward the flask with Eli **off screen** on "Don't open the flask." (CR-ELI; his closest singles are saved for SC13); SH150 the turn shot as in 5.1, routed to Seedance 2.5 as one take; SH160 Saye's one look afterwards (A1 R19 tie-break); SH190 the held wide from camera F through the wait (second turn); SH200 "Nobody leave this room."; CUT SC10-C200 `cut_to_black`; SH990 the title card `TX-TITLE-CATCH`; the lamp set down listed as an invention; LOOK contrast `medium_high` (B2); every line 397-489 covered. Its compiled Seedance prompt follows C3 R1 (motion only, "the woman"), with no fixed description re-described.

### 14.3 The test plan

Test agents have only the delivered repository and the story files placed in `My stories/` by the harness (not committed). No generation keys. The harness answers checkpoints with "defaults" unless a test says otherwise.

| Test | What runs | On what | Pass |
|---|---|---|---|
| **T0 Unit tests** | `python tests/run_tests.py` | fixtures, gold, the committed story excerpts | all pass; if decision 16 is answered no, the gold's CITE checks report "skipped: story not present" unless the harness passes `--story <path>` |
| **T1 Reader** | `stage.py new`, `read` | both stories | The Catch: 1,852 lines; 30 scenes at the heading lines 10, 71, 116, 145, 181, 198, 300, 333, 343, 397, 490, 532, 672, 830, 838, 868, 912, 1000, 1098, 1112, 1211, 1259, 1265, 1376, 1428, 1502, 1555, 1599, 1713, 1814; 221 speeches; SC10 = lines 397-489 with 16 speeches (SC10-D01 "Kitchen." to SC10-D16 "Nobody leave this room."); `= THE CATCH` (l.488) becomes a card; `(ON THE TABLET)` noted as presentation. The Long Places: 1,444 lines; 49,152 words; 14 chapters at lines 5, 84, 163, 262, 385, 476, 541, 636, 777, 858, 943, 1048, 1155, 1287. v0 for The Catch between 1,926 and 2,309 s |
| **T2 Gold and derived fields** | `stage.py replay`; `build` on the gold | gold examples, plus one fixture shot | expected checks reproduced; SH150 floor 13.8 s (speech floor 11.8 s + pause owed 2.0 s after the turn at beat 7); SH150 clip 17 s, a held take (turn), routed to Seedance 2.5 as one clip; a normal (not held) 18 s fixture shot on Kling with a planned cutaway is split at the cutaway and stays on Kling; SH080 size check `medium`; SH080 route plate; Iona's raised hand = own right = hand nearest the camera; Saye's raised own right appears as her left, nearest the camera; Saye's ring (own left) appears on her right, the far hand; Iona and Saye eyelines opposite; SC10 derived era b with frame original, Saye, the kitchen and the mint mirrored, Iona, Jude and Eli normal (K03) |
| **T3 Whole screenplay, Claude surface** | a fresh agent in Claude Code with the repo, told only "Break down my story." | The Catch, all 30 scenes, Standard | finishes steps 0-11; `check --all` exits 0; every unit's errors recorded by family before repair; repair rounds per unit ≤ 3; book and exports made; wall time and unit count recorded |
| **T4 Prose, Claude surface** | a fresh agent; harness answers checkpoint P with "defaults" (plan A, chapter I first) and then "go on to chapter II" | The Long Places: whole-book plan; chapters I and II to step 8 | 14 digests of at most 350 words; every cardinal event in a kept scene; chapter I and II scenes pass `check`; prose SPEECH lines found word for word; no scene reads the whole book |
| **T5 Chat without code** | a fresh agent with only the chat kit's text files (the instructions, the six knowledge files, and the step file and saved files each chat attaches) and no code or file tools; the harness saves each copy box under its "Save as" name and runs one check chat at the end of each sequence; then `stage.py adopt` on the saved folder with the story, then `check --all` | The Catch SC01-SC06 | every file has its END line with the right count; no shortening markers; every quote anchor resolves once (CITE-02); `adopt` re-owns the AI-written state fields with notes only; FORM errors at most 1 per 20 records after tidy fixes; every saved file carries its checks-in-words table after its last record and each reply prints the one "Checked in words" line; each reply quotes its step's one-line task |
| **T6 Previs** | `stage.py previs --render` | SC10-SH080 (from the gold); SC06 master fall plus two time slices; SC13 master from B3's plan; SC25 chest opens (fixed plan) | `BLOCKING OK` for all; figure facings within 20° of derived; SC10-SH080's grey still shows Iona frame-left facing right, Saye frame-right facing left, Eli small and centred deep; render times recorded |
| **T7 Generation packs** | `stage.py compile --scene SC07..SC10 --model kling-3.0-omni,seedance-2.5,veo-3.1` (packs for the shots routed to those models), then `compile --scene SC10 --force-model veo-3.1` | T3's output | 0 GEN errors on the routed run; SH150 one clip on Seedance 2.5; the forced Veo run uses the colon speaker form without quotes (its GEN-02 and GEN-10 are notes); no `why`, `because` or `purpose` text in prompts; no "torch"; every pack priced and dated |
| **T8 Exports** | `stage.py export all` | T3's output | shot-list CSV has the byte-order mark and exactly the columns of 5.9; captions follow 5.9's timing; OTIO loads with `opentimelineio` if it installs, else passes a structural check; EDL and SRT/WebVTT pass format checks; `breakdown.json` validates against `breakdown.schema.json` (nesting at most 3 levels) |
| **T9 Smallest model** | a small-model agent runs U-07-SC10 and U-08-SC10-B1 from handouts | SC10 | 0 ERROR after at most 3 rounds |
| **T10 Critics** | four critic agents | T3, T4, T5 outputs | craft: rubric pass rule on the film, and an average of 2 or more on criteria 3, 4 and 5 across the unassisted scenes; executability: completion and repair statistics; generation readiness: T7 plus a reading of the hard cases; plain language: WORDS-04 clean on user-facing files and a critic's reading of `00 Start here`, `01 Choices`, the guides and the book |

**Assisted and unassisted scenes.** SC06, SC10, SC13, SC15, SC25, SC29 and The Long Places chapter I are analysed in the research or the gold examples, so critics score them separately from the unassisted scenes (for example SC02, SC09, SC16, SC20, SC24, SC26-27, SC30 and chapter II).

**Kill criterion.** If in T3 or T5 the grammar errors (FORM family) before repair outnumber the craft errors (CRAFT, REASON, TIME, GEOM families), the storage syntax switches to flat JSON under the same schema: `record_format.py` gains a JSON reader and writer, templates become JSON, and the checker, derivations and exporters do not change.

### 14.4 Later (not in the first build)

The browser helper page running `stage.py` through Pyodide (for Gemini users without any code surface); field-level staleness (the first build marks whole records stale); checks marked build 2; tone defaults tuned from test runs (the first build ships D10 §2.2's table as written); estimate versions v2 (animatic) and v3 (actuals); automated generation batches through connectors; posed stand-ins (MPFB, Mixamo) and performance capture; series tooling (episode tables, recaps); an FDX export for Movie Magic; the smallest-model replay as an automated harness.

### 14.5 What cannot be tested here

Image, video and voice generation end to end (packs stop at "ready to send", lint-clean and priced); the real behaviour of claude.ai skill upload, ChatGPT Projects and Gemini Gems, and their reply limits (T5 simulates the chat path); Blender 5.2.2 (5.0.1 is installed; the kit and the SC10 plan pass on it); OTIO import into Resolve or Premiere; the user's own judgement of the plain language and the craft.

---

## 15. Open decisions for the real user

The build uses the default in every row; each is a CHOICE the pipeline asks at the checkpoint named (or, for the build itself, in the first report to the user).

| # | Decision | Default the build uses | Asked at |
|---|---|---|---|
| 1 | Rights for each story | "It's mine" for both | step 0 |
| 2 | Depth | Standard | stated at step 0; "quick" or "detailed" any time |
| 3 | Privacy setting turned off before uploading | assumed not confirmed; the guides ask it first | setup guides |
| 4 | The Catch: length | full length, about 35 minutes | A |
| 5 | The Catch: climax reading | climax SC26-27; crisis SC24 | B |
| 6 | The Catch: style and frame shape | photographic, clinical and plain (provisional until the style test of add-on A or C); 2.39:1 | B |
| 7 | The Catch: place and time | an unnamed British city, present day, driving on the left, British voices | B |
| 8 | The Catch: music | none | B |
| 9 | The Catch: mirror eras and the six detail rules | as in K03 and K04 | B |
| 10 | The Catch: sides, the SC10 staging, the SC06 fall | B5's sides; B3's staging with the lamp as an invention; expanded time from overlapping real-time slices | B (small choices) |
| 11 | Casting types the script leaves open (skin tones, ethnicity, body types) | left open until reference pictures are made; then the user chooses from options | add-on C |
| 12 | The Long Places: format | plan A, a feature of about 100 minutes; chapter I first as a trial | P |
| 13 | The Long Places: the letters, keeper voices, Emre's face | letters open and close the film (hands only, 4-6 lines of voice-over); letter II carried by the humming; Emre kept at the lamp's edge | P (small choices) |
| 14 | Voices | designed voices only; no clones | add-on C |
| 15 | Spending cap | none set, so nothing is spent | add-on C |
| 16 | Whether the repository may include the two stories, or excerpts of them, as test files | whole stories: no. Excerpts: yes, as `tests/fixtures/The Catch - lines 397-489.txt` and `tests/fixtures/The Long Places - chapter I.md`, keeping their original line numbers through an offset header, in the private repository (decision 17), so `replay` and T0 can run the CITE checks on the gold. If the user says no, the excerpts and `09 Example` are left out, replay runs the CITE checks only with `--story <path>`, and T0 reports them "skipped: story not present" | first report of the build |
| 17 | Whether the Stage repository is public or private on GitHub | private | first report of the build |
| 18 | Whether previs is wanted for The Catch | offered after acceptance: about 26 framing-critical shots | after step 11 |

---

## Appendix. Where each research gap (D1-D18) lives

| Gap | Where in the pipeline |
|---|---|
| D1 Running in chat apps | Surfaces (2.4, 2.5, 13); step files attached per chat, never left to knowledge search (2.5); self-test unit and batch size (step 0); END lines and shortening markers (G9, G11, FORM-06 to FORM-08); plan short then expand (steps 7-8); quote anchors and `adopt` (G5, 7.1); checks split between the reply and a check chat (7.4); save ZIPs and resume lines; privacy lines in every guide; `limits.json` |
| D2 Whole-work adaptation | Step 2 (digests, strands, cardinal events, macro plans, checkpoint P, step outline, compression ops); card 02; COVER-05, PLAN-04, PLAN-05 |
| D3 Voices and dialogue audio | VOICE records; SPEECH paths; voices first (8.6); VOICETAKE; lip-sync routes; card 06; `audio_models.json` |
| D4 Rights and disclosure | Rights at step 0; RIGHTS records; `likeness_basis`; content flags and policy routes; WORDS-03; GEN-14; `22 Rights and credits.md`; card 24 |
| D5 Visual style | STYLE at step 3, asked at B as provisional; the three-direction style test as the first job of add-on A or C (section 10); card 08; style words pasted into prompts |
| D6 Compositing | FINISH jobs (8.7); mirror routes; text graphics; card 23 |
| D7 Judging a breakdown | Rubric (11.3); review by question (11.2); gold and replay (11.4); the user's review sheet (11.5) |
| D8 Assembly and finishing | Add-on D; OTIO and EDL; conform and finishing jobs; card 23 |
| D9 Music and effects | SOUNDPLAN; MUSIC cues; `effect` items; spotting sheet export; card 13 and 23 |
| D10 Genre and tone | PLAN and PROJECT `tone_home`, `tone_range`; SCENE `tone`, `tone_undercurrent`, `tone_shift`; `rules/tone_defaults.json` read by the estimate, TIME-07 and the rhythm checks; FILM-12; card 08 |
| D11 Action | Scene action fields (geography, cause chain, escalation, reversal, action score, the five time treatments); `time_slice` and the master previs stub; SHOT `motion`; card 15; previs level 3 for action |
| D12 Diegetic graphics | TEXT and CAMERA records; `make_text_graphics.py`; screens within screens (8.5); card 17 |
| D13 Runtime, cost, schedule | `estimate.py` v0 at A and P, v1 at step 10; `cost_class`; `prices.json`; spending rules (8.8) |
| D14 Any story format | `read_story.py` formats, thin sources and authoring mode (step 1); card 02 |
| D15 Performance | `subject` sub-parts `does`, `tactic`, `energy`, `display` (1-3), `still`, `eyeline` with `dwell_s`, `must_not`, `continues`; BEAT tasks; CHARACTER movement, gesture and status; CRAFT-25, CRAFT-26; compile rule 9 (stillness written out); card 06 |
| D16 Film-level structure | PLAN (crisis, climax, acts, peaks), SEQUENCE, LADDER; film pass (step 9) |
| D17 World and locale | WORLD at step 3, asked at B; card 08 |
| D18 Accessibility and localisation | `needs_description`; captions (SRT and WebVTT with sound tags); audio-description script; text-to-translate list; TEXT `translate`; card 23 |

---

## Critic findings not applied

Two critics reviewed the first version of this blueprint. Every blocker and major finding and every plainly correct minor finding was applied; the lines below record what was rejected, applied only in part, or applied in a different form, and why.

- **Merge each chat's shot batches into one scene file (critic 2, major, cost of the no-code path): not applied.** One reply cannot safely carry a scene's design and all its shots; D1's reply limits are the reason for batches of 12 or 18 and for END lines, and re-sending the whole scene file with every batch would multiply tokens and the risk of a cut-off. Batch files stay separate, `adopt` merges them by ID (G10), and `01 Read me first` states the real save count instead. The rest of that finding (a cost line per app, the Claude website free-plan recommendation, a one-line check result in each reply) is applied.
- **Cap step files at 1,500 words so file 01 stays under 25,000 words (critic 1, minor, sizes): not applied as written.** Splitting the chat kit (2.5) moved the step files out of file 01 into five step-group files attached per chat, so file 01 is about 5,500 words and step files keep their 1,200-1,800-word range. The card-part cap (9,000 tokens per unit) and the `limits.json` ceilings (30,000 and 20,000 tokens) are applied.
- **Rewrite the checkpoint C example as group 1 (critic 1, minor, examples): applied in a different form.** The group 3 example stays, now shown as a later group that reports and carries on, which is what the first-sequence rule makes it; the first group's extra part (the film rules in five plain lines and the one question) is shown separately. All codes in it are now plain words ("shot 150", "the turn").
- **"The StudioBinder columns" in T8 (critic 1, minor, exports): replaced, not matched.** Matching one named vendor's import format would tie the export to that vendor (principle 10) and needs a specification this blueprint does not hold, so 5.9 defines Stage's own column list, chosen to map onto common shot-list tools, and T8 checks that list.
- **Numbered story for Gemini users (critic 1, blocker 1, alternative 4): kept as an option only.** Quote anchors plus `adopt` make the no-code path checkable without it, so the extra setup step on the Claude website is offered in the Gemini guide, not required.
- **Alternatives chosen where a finding offered two fixes:** PREVIS stubs created by code, not a `master:` name bound later (critic 1, K20); a declared `tightest_size` peak for SC13 in K12, not a ladder by beat-intensity rank (both critics); SETVALUE records for structured choice answers, not values in `{ }` (critic 1, CHOICE.sets); the mirror state renamed `reversed`, not kept as `turned` with a word-list note (critic 2, word list).
