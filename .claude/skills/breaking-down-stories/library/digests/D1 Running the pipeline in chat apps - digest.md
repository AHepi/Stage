# Digest D1: Running the pipeline day to day in Claude, ChatGPT and Gemini (27 Sept 2026)

Source: `research/D1_llm_app_operations.md` (fact-checked 27 Sept 2026). Brackets: §1.n = core principle n; §4.n = decision rule n; §2.4, §6.x etc. = section. Evidence: **[V]** official page read, **[V-sec]** search excerpt or secondary site, **[U]** unverified (the smoke test decides), **[J]** judgment. App facts go stale fast: re-check monthly (C5 R22).

## 1. Scope

1. An operating manual for a user whose only skill is chatting with an LLM: what fits in one message and one reply, what persists, whether Python runs, and what each plan costs on claude.ai, Cowork, Claude Code, ChatGPT, the Gemini app, AI Studio and NotebookLM.
2. Keeps a weeks-long C5 pipeline alive across disposable chats: files on disk are the memory, 18-shot reply parts with an END line, validator or fresh-chat checks, resume and close messages, and snapshots.
3. Picks a surface per goal, gives a 10-minute smoke test, and works through *The Catch* session by session on claude.ai Pro (adapted to ChatGPT Plus and Gemini AI Pro) and *The Long Places* chapter I in one session.

**Terms** [§0]: *token* = unit of text (English prose about 1.2–1.8 per word); *context window* = most text held at once (files + chat + reply); *reply limit* = most text written in one reply; *truncation* = reply stops mid-way; *silent shortening* = finished-looking reply that skipped records or wrote "..."; *part* = one reply's share of a scene file; *END line* = fixed last line proving the reply finished; *retrieval mode* = the app shows the model only matching fragments of stored files; *sandbox* = temporary computer in the chat where Python runs; *connected folder* = a local folder an agent mode reads and writes; *snapshot* = ZIP of the project folder at session end; *hash* = fingerprint proving a record was not edited; *usage credits* = extra paid Claude usage (the only way Pro reaches Fable).

## 2. Rules

**Sizing**
1. [§2.4] If a scene has more than 18 shots, then expand it in parts of at most 18 shots plus their cut records, split by ID range from the approved one-line list, because 18 records plus cuts are about 12,500 tokens, far under every documented cap (Gemini 65,536; Claude and GPT 128K via API [V]), and models shorten long repetitive lists before any hard cap [J].
2. [§2.4] If smoke test step 3 shows shortening before 20 records, then set `part_size` to 12, because the observed limit beats the documented one.
3. [§2.3] If a job's input (files plus chat) exceeds about 60% of the window, then start a new chat with only the files the job needs, because the reply needs room and Claude's automatic summarizing uses more of the usage limit [V] and drops exact records [J].
4. [§2.3, §5.2] If the whole *Long Places* goes to ChatGPT Plus, then choose Thinking (256K), never Instant (54K), because the numbered novel is about 64K tokens [V-sec].

**Reading and state**
5. [§1.1, §1.3, §4.1] If a file must be read whole (context pack, previous scene, file being checked), then attach it to the message, because project knowledge on paid Claude plans may switch to retrieval mode near capacity [V].
6. [§4.10] If an app offers memory, then turn it off for this project (ChatGPT: project-only memory) or ignore it, because remembered facts from older versions contradict the state files [J].
7. [§4.11, C5 R18] If a record is `"locked": "yes"`, then it is read-only in every session and the validator checks it against its hash in `manifest.json` (D1-V14), because locks must live in the data, not the chat.
8. [§6.1] If a file is saved, then its name never changes and `file_meta.file_version` rises by one, because instructions and scripts find files by fixed names.

**Checking**
9. [§4.2, C5 R9–R10] If the surface runs Python, then run `validate.py` after every part and every merge, because a schema guarantees shape, not meaning.
10. [§4.3, C5 R12] If it runs no Python, then run the §6.3 checklist in a fresh chat and the real validator at the next chance (claude.ai Free has code execution [V]), because self-review lowers accuracy.
11. [§4.4] If a reply lacks the END line, its count differs from the approved list, or it contains "...", "…", "etc.", "same as above", "remaining" or "omitted", then treat the part as unsaved and send a continue prompt, because silent shortening leaves no other trace [J].
12. [§6.2] If brackets are broken, then re-request the part and never hand-repair it, because a repaired part hides missing records [J].

**Sessions**
13. [§4.5] If a chat has handled one sequence, or the app says it is summarizing earlier messages, then start a new chat and resume from files, because summaries drop exact records.
14. [§4.6] If the usage bar passes about 80%, then finish the current part, save, snapshot and stop, because a limit hit mid-part leaves half a record.
15. [§4.7, §1.6] If a session ends, then send the close message and download the snapshot before closing, because ChatGPT sandbox files expire when idle [V-sec] and Claude promises files only "throughout conversations" [V].
16. [§6.1] If the file list in the chat differs from the unzipped folder, then do not start the next session until they match.

**Portability, models and privacy**
17. [§4.8, §1.8] If the pipeline runs on more than one app, then keep scripts on Python's standard library (`export_otio.py` writes OTIO JSON directly), because ChatGPT's sandbox has no internet and cannot `pip install` [V-sec].
18. [§4.13, §7.1, C5 R19] If choosing a model for a stage, then use the smallest that passes the validator, because larger models drain the usage limit faster.
19. [§7.1, C5 R32] If a model vanishes from the picker or changes (Haiku 4.5 may retire from 15 Oct 2026 [V]; GPT-6 Sol is rolling out [V-sec]), then move one tier up, log it in `sessions[]` and re-run SC06, SC13 and SC15.
20. [§7.2] If the user will not handle API keys, then subscribe (Claude Pro $20) rather than use the API, because the API saves little at this size (*The Catch* about $17 on Opus 5.5) [J]; if a rule change forces re-running all 30 scenes, then consider the batch API (half price [V]) through Claude Code.
21. [§4.9, §8] If the manuscript is unpublished, then turn training off everywhere before the first upload, keep Gemini's Keep Activity off, never press thumbs up or down, and never use free AI Studio, because feedback and free-tier content reach human reviewers [V].
22. [§4.12, §6.5] If a text stage refuses the SC06 gunshot or blood, then restate once as pre-production, use production words, and if still refused switch model or surface and log it, never disguising the content, because the pipeline needs staging, not graphic description [J].

## 3. Breakdown fields

Enums lowercase `snake_case`; empty is `"none"`; all `derived` (script or session-close step) unless marked.

| Level | Field name | Meaning | Allowed values / example |
|---|---|---|---|
| film (manifest) | `surface` | App running the pipeline | `claude_web` \| `claude_cowork` \| `claude_code` \| `chatgpt_web` \| `chatgpt_work` \| `gemini_app` \| `ai_studio` \| `other` |
| film | `code_execution` | Whether Python runs there | `yes` \| `no` |
| film | `state_store` | Where state lives between sessions | `project_knowledge` \| `local_folder` \| `connected_folder` |
| film | `training_optout` | Training setting checked (authored by human) | `confirmed` \| `not_confirmed` |
| film | `part_size` | Most shots per reply, from the smoke test | integer, default `18` |
| film | `resume_point` | Where the next session starts | object: `stage`, `scene`, `last_record`, `next_record` |
| film | `sessions[]` | One row per session | `session_id` (`S01`), `date`, `surface`, `plan`, `model` (exact picker name), `stages`, `scenes`, `snapshot_file` |
| every file | `file_meta` | Version stamp | `project`, `path`, `file_version` (integer), `saved_at` (ISO date-time), `stage`, `model`, `record_count`, `content_hash` (or `"none"` where no code ran) |
| scene | `shot_plan_approved` | Checkpoint C passed before expansion | `yes` \| `no` |
| scene | `parts[]` | One row per reply part | `part_id` (`SC06-P1`), `first_record`, `last_record`, `expected_count`, `received_count`, `end_line_seen` (`yes` \| `no`), `status` (`complete` \| `partial` \| `missing`) |
| log | `refusals[]` | Refused requests | `surface`, `model`, `stage`, `record`, `action` (`restated` \| `switched_model` \| `human_handled`) |

**Validator checks** (numbered after C5's V1–V13): **D1-V14** every locked record equals its hash in `manifest.json`; **D1-V15** every part's IDs equal the approved list for its range, the END line is present, counts match, no shortening marker; **D1-V16** each changed file's `file_version` is one higher than in the previous snapshot and `manifest.json` agrees.

## 4. Procedures

**P1. Pick a surface** [§5.1].
1. Breakdown only: Claude Pro with a Project, the skill and code execution, or Cowork on desktop with a connected `CATCH/` folder. No budget: claude.ai Free (5 projects, skills, code execution, Sonnet). Already on ChatGPT Plus: a Project with Thinking and data analysis. Already on Google AI Pro: a Notebook in Gemini, validation via Colab or claude.ai Free (Spark's local folder needs AI Ultra in the US).
2. Plus storyboards: breakdown stays in Claude; under about 150 frames use C2's chat-only path; above, a connector (C1 P1).
3. Plus previs: Claude Code with Blender (C4 Mode B); or Mode A from any surface (the LLM writes the script, you run it).
4. Plus generation via connectors: Claude (custom connectors on every plan, one on Free) or ChatGPT Plus developer mode on the web; not the Gemini app.

**P2. Set up claude.ai Pro (15 minutes)** [§5.2].
1. Settings > Privacy > turn off "Help Improve our AI models".
2. Settings > Capabilities > turn on "Code execution and file creation".
3. Customize > Skills > "+" > "+ Create skill" > "Upload a skill" > choose `breaking-down-screenplays.zip`. Test: "Which skills do you have? Describe breaking-down-screenplays in two sentences."
4. Projects > new project `CATCH breakdown`; paste the project instructions (P4) [button label U].
5. Settings > Usage: note the 5-hour reset and weekly remainder.
6. Make `CATCH/` on your computer with the C5 §10.3 subfolders plus `snapshots/`.
ChatGPT Plus: Settings > Data controls > "Improve the model for everyone" off > Done; Project with project-only memory; short `SKILL.md` as instructions; at most 25 files, 10 per upload; Thinking for stages 1–5; developer mode at Settings > Security and login. Gemini AI Pro: Keep Activity off (chats kept 72 hours, then gone from history); a Notebook with rule and state files as sources; or a Gem whose files come from Google Drive, which Gemini re-reads at their "most recent version" [V] (Drive `.json` [U]).

**P3. Smoke test, 10 minutes, on every new surface or plan** [§5.3] (prompts exact).
1. Attach *The Catch* .txt: "How many lines does this file have, and what is line 253, word for word?" Pass: 1,852 and "He is looking straight at her. He has one hand she cannot see."
2. Attach *The Long Places*: "Quote line 1385." Pass: "Going down for the evening round she passed the schoolteacher's mat. Seher did not open her eyes. "Was it kept, Hanım?""
3. "Write 20 complete shot records for SC06 using this example record [paste C5 E3], IDs SC06-SH010 to SC06-SH200, all fields filled, then the END line `END TEST | 20 SHOTS`." Pass: 20 records, no "...", END line. Fail: part size 12.
4. "Using Python, count the lines in the attached file, write `test.json` containing {"ok": "yes"}, zip it as `test.zip`, and give me both to download." Fail: no sandbox; use rule 10.
5. New chat, same Project or Notebook: "Quote line 1 of `scenes_index.json` from project knowledge."
6. "Give a one-line shot list for The Catch lines 214–224 (the gunshot)." Pass: a normal answer.
7. Confirm training is off; record `training_optout`.

**P4. Project instructions (paste exactly)** [§10.1]:
```
This project runs the breaking-down-screenplays skill on THE CATCH.
1. Files are the only memory. Trust attached files over the chat, memory or project knowledge.
2. One scene per call. Any reply with more than 18 shot records is split into parts by ID range.
3. End every JSON part with: END <scene> PART <n> OF <m> | <first>..<last> | <n> SHOTS | <n> CUTS
4. Never change a record whose "locked" is "yes".
5. After every part, run scripts/validate.py and show its report, one line per problem.
6. At session end, update manifest.json (file_meta, resume_point, sessions[]) and give me one ZIP
   named CATCH_S<nn>_<date>_<last-scene>.zip.
```
END line example: `END SC06 PART 1 OF 2 | SC06-SH010..SC06-SH180 | 18 SHOTS | 18 CUTS`

**P5. Resume a session** [§6.1] (exact):
> Resume stage 5 at SC07; attached bible.json, ledger.json, scenes/SC06.json.
> Also attached: manifest.json, scenes_index.json, source.fountain.
> Records with "locked": "yes" are read-only.
> First run validate.py on the attached files and tell me the resume_point in manifest.json. Then wait for me to say "go".

**P6. Close a session** [§6.1] (exact):
> Close session S04. Update manifest.json: file_meta for every changed file, resume_point (stage, scene, last_record, next_record) and one sessions[] row. Run validate.py on everything. Then give me one ZIP named CATCH_S04_<date>_after-SC07.zip with the whole CATCH folder, and list every file inside it with its file_version.

Then unzip: Windows, right-click > "Extract All..." > choose `CATCH` > replace; Mac, double-click, drag contents into `CATCH`, "Replace". Move the ZIP into `CATCH/snapshots/`. Snapshot name: project, session, date, last finished scene (`CATCH_S04_2026-10-02_after-SC07.zip`). To undo a session, unzip the previous snapshot.

**P7. Continue prompts** [§6.2] (exact, change the IDs):
- "Your reply stopped inside SC06-SH170. Discard it. Send SC06-SH170 to SC06-SH180 again, complete, then the END line. Do not repeat earlier records."
- "Your part 1 skipped SC06-SH120 and SC06-SH130. Send only those two records, complete, then `END SC06 PATCH | 2 SHOTS`."
- "Continue from record SC06-SH190: send SC06-SH190 to SC06-SH360 as part 2, complete, then the END line."
Signs of a bad part, strongest first: END line missing or wrong count; JSON does not parse; IDs differ from the approved range; "...", "…", "etc.", "same as above", "remaining shots", "omitted for brevity" or `//`; missing fields; under 25 KB for 18 shots (expected about 35 KB); "Continue" button or mid-word stop.

**P8. Fresh-chat checklist where no Python runs** [§6.3]. Attach the part, the approved list and the previous version; paste: "Answer each question yes or no, then list every problem as record ID, field, problem." Questions: (1) begins with `[` or `{` and ends with the matching bracket? (2) END line present, counts equal records? (3) shot IDs equal the approved list, steps of 10? (4) any "...", "…", "etc.", "same as above"? (5) all fields of the example record, `"none"` for empty? (6) every `source_lines` inside the scene's range in `scenes_index.json`? (7) enums lower-case and allowed? (8) `duration_s` sums to `target_duration` ±10%? (9) locked records identical word for word? (10) SC06 lines 224–258: `PR-PUCK.S02` absent from frame per `withhold`?

**P9. Refusal handling** [§6.5]. Say once: "This is pre-production for my own short film. I need camera, staging and continuity fields only, no graphic description." Then production words: "gunshot sound effect", "wound make-up on Jude's shoulder", "blood beads, a composited visual effect". Then switch model or surface and log `refusals[]`.

**P10. Context pack as pasted (prose)** [§11]. Section headers, in order: `=== STAGE 5a INSTRUCTIONS (read first) ===`, `=== SOURCE: chapter I, lines 73-81 ===`, `=== BIBLE ENTRIES USED (draft) ===`, `=== LEDGER ROWS AT SCENE START ===`, `=== NEIGHBOURS ===`, `=== ANALYSIS LINES FOR THIS SCENE (A3 Ex5) ===`, `=== FORMAT EXAMPLE ===`, `=== STAGE 5a INSTRUCTIONS (repeated) ===`. Opening block (exact):
```
Project LONGPL. Run stage 5a (one-line shot list) for ONE scene: SC10.
Use only the material below. One line per shot: ID | size | beat | subject | action | source line.
IDs SC10-SH010 upward in steps of 10. Every shot cites its source line.
Records with "locked": "yes" are read-only. Enums lowercase snake_case; empty = "none".
End with: END SC10 LIST | <n> SHOTS
```
Format example: `SC10-SH010 | wide | SC10-B01 | CH-NILAY | carries the lamp down to the first door, sits | l.73`. Closing block: `One scene only. One line per shot. Cite source lines. End with the END line.` About 1,500 tokens; full text in §11.

## 5. Checklists

**Session start**: last snapshot unzipped in `CATCH/` • new chat in the Project or Notebook • `manifest.json` and the stage's files attached • resume message pasted • validator report read before "go".
**Every part**: END line present • count matches the approved list • no shortening markers • validator (or P8) clean • `parts[]` updated.
**Session end**: close message sent • ZIP downloaded, unzipped, file list matches • film-level files replaced, not duplicated, in project knowledge.
**New surface or plan**: P3 smoke test • training off • `part_size` set • `surface`, `code_execution` and exact model name recorded.
**Monthly**: re-check every [V] fact in §3 and §8; re-run SC06, SC13, SC15.

**Surface facts to re-check** (27 Sept 2026): Claude Pro $20 ($17 yearly), Max from $100; paid window 200K, 1M on Fable 5.1/Opus 5.5/Opus 5/Sonnet 5; 20 files per chat, 500 MB each, 30 MB project files; sandbox 30 MB per file, network on by default, reads project files [V]. ChatGPT Plus $20; Instant 54K, Thinking 256K; 25 project files; no skill upload on Plus; custom GPTs retire 11 Dec 2026 [V-sec]. Gemini AI Pro $19.99, 1M window; 10 files per prompt; downloads include .csv, .txt, .md but not JSON or ZIP; no documented chat Python [V/U].

## 6. Saying it to AI models

- Put the instruction first and repeat it last; give only the entries the scene uses (C5 §6.2; P10).
- Always name the ID range and the END line: "Expand part 1: SC06-SH010 to SC06-SH180 with their cut records, then the END line. Run validate.py."
- Ask the model to prove it read the whole file: quote a named line (P3 steps 1–2) before any whole-work stage.
- For corrections, one target per message: "Revise only CH-IONA: [one sentence]."
- Approvals are single words the log can find: "approved", "approved SC06 list", "unlock SC06-SH140".
- On ChatGPT paste the short `SKILL.md` as project instructions and attach `pipeline_rules.md`, `schema.json`, `scripts.zip`, then say "unzip scripts.zip and use it"; on Gemini use the same three files as Notebook sources and ask for a Canvas code document saved as .txt, renamed .json.
- Never ask a model to "review and improve"; ask the checklist questions in a fresh chat (C5 R12).

## 7. The Catch

**Decisions made** [§2, §10]:
- Sizes: 9,217 words, 1,852 lines, 12,484 tokens (o200k); about 16k–18k numbered. SC06 file about 26,700 tokens (36 shots), SC13 about 23,400 (31 shots); all 30 scenes about 230,000 (about 300k Claude tokens), so scene files never go into project knowledge.
- Parts: SC06 = `SC06-SH010`–`SC06-SH180`, then `SC06-SH190`–`SC06-SH360`; SC13 = `SH010`–`SH180`, then `SH190`–`SH310`. Beats go in their own reply first.
- Sessions on claude.ai Pro: S0 setup and smoke test (20 min); S01 intake and checkpoint A (30 min; check 30 scenes, SC06 `INT. FREIGHT CAGE - CONTINUOUS` at 198–299, SC15 838–867 "(ON THE TABLET)", `= THE CATCH` l.488 as a card, `> CUT TO BLACK.` l.486 and l.1848, `= THE END` l.1852); S02 story analysis and bible, checkpoint B (60–90 min, Opus 5.5); S03 ledger in three parts SC01–10, SC11–20, SC21–30 (45 min); S04–S09 one sequence each: SC01–07 (l.10–332), SC08–10 (333–489), SC11–16 (490–911), SC17–18 (912–1097), SC19–26 (1098–1554), SC27–30 (1555–1852) [J]; S10 exports.
- Ledger checks: `PR-PUCK.S02` from l.224 ("His other hand goes underneath. Behind Jude's back. Out of sight."); `.S03` from l.259 ("A hard metal CLACK."), "burnt into the grid" at l.1219; first handedness change at l.259.
- Eye checks for SC06: SH140 withholds Eli's right hand and `PR-PUCK.S02` (l.242–244); "A hard metal CLACK." (l.259) and "BLACK. A dark with nothing in it. One instant." (l.261) follow the hard cut.
- Refusal-prone lines: l.216 ("Someone KICKS the top gate open and FIRES down through the roof."), l.222 ("a hole through his shoulder"), l.244 (the blood beads).

**Flagged for the user**:
- Which surface and plan (Claude Pro recommended); whether to install Claude Code for previs.
- Confirm checkpoint C per scene (this file) or per sequence (C5).
- Confirm the sequence split, and whether D2's SC08-into-SC09 merge applies.
- Whether Fable's usage credits are worth buying for stage 1 on the novel.
- Record `training_optout: confirmed` yourself.

## 8. Conflicts and open questions

- **C5 §6.11 corrected**: skills now sync one way from claude.ai to Claude Code (v2.1.273+) [V]; C5 said they do not.
- **C2 price drift**: Google AI Plus $4.99 [V] versus C2's $7.99.
- **C5 P1 order**: C5 gates stage 5 with a one-line list per sequence; D1 approves a 5a list per scene before 5b expansion. Pipeline design must choose.
- **C5 ID pattern**: `SC` plus two digits is too small for a novel (ten candidate scenes in chapter I alone); needs `SC001` or a chapter prefix.
- **D14 (intake)**: prose becomes `source_paragraphs.md` with block IDs (`ch08.p027`); D1's chapter I pack cites raw file lines. Once D14 runs, packs should cite block IDs.
- **D14 Recipe I5**: calls Cowork an agent that "runs code on your computer"; Anthropic says Cowork runs "on Anthropic's servers, in an isolated environment" [V]. Local tools (Tesseract, Blender) need Claude Code.
- **C1 P1 menu path**: "Claude settings → Connectors" is now Customize > Connectors > "+" > "Add custom connector" [V].
- **D2 Option 3** merges SC08 into SC09; session plans follow the scene list locked at checkpoint A.
- **Open [U]**: reply limit in every app (Max advertises "Higher output limits", so it varies by plan); ChatGPT windows only from secondary sites; whether Gemini chat runs Python; Gem file count; whether claude.ai downloads `.json`/ZIP and can add created files to a project; ChatGPT sandbox idle time; whether Notebooks keep chats with Keep Activity off.
- **Churn**: Haiku 4.5 retirement not before 15 Oct 2026; GPT-6 Sol/Luna rollout; custom GPT creation ends 26 Oct and GPTs retire 11 Dec 2026 [V-sec].
- **Invented detail**: the chapter I identity key's build, hair, clothes, wristwatch and "no rings" are drafts for checkpoint B; "forty-four" is computed from l.39 and the location quotes l.43.

## 9. Section map

- **§0** terms (JSON, validator, hash, ZIP, API, connector, usage credits added) • **§1** eight principles • **§2** sizing: 2.1 source tokens, 2.2 scene file sizes, 2.3 what fits where plus 60% rule, 2.4 part rule • **§3** surface sheets: 3.1 claude.ai, 3.2 Cowork and Claude Code, 3.3 ChatGPT, 3.4 Gemini, AI Studio, NotebookLM • **§4** 13 decision rules • **§5** choosing: 5.1 decision tree, 5.2 setup clicks, 5.3 smoke test • **§6** state: 6.1 stores, naming, locks, resume, close, unzipping; 6.2 cut-off JSON and continue prompts; 6.3 fresh-chat checklist; 6.4 failure table; 6.5 refusals • **§7** models: 7.1 tier per stage, 7.2 subscription vs API costs • **§8** privacy table • **§9** fields and D1-V14–V16 • **§10** *The Catch* sessions 0–10; 10.6 ChatGPT Plus and Gemini AI Pro adaptations • **§11** *Long Places* chapter I pack • **§12** checklists • **§13** conflicts • **Sources** S1–S50.
