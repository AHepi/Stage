# D1. Running the pipeline day to day in Claude, ChatGPT and Gemini: sessions, files, limits, resumption

```
+-----------------------------------------------------------------------------------------------+
| WHAT THIS FILE IS FOR                                                                         |
| 1. Lets someone whose only skill is chatting with an LLM run the C5 pipeline for weeks.       |
| 2. Says, per app and plan, what fits in one message, what persists, whether Python runs.      |
| 3. Gives the split rule for long scenes, the resume message, and how to catch cut-off JSON.   |
| 4. Picks the app for each goal (breakdown, storyboards, previs, generation) with a smoke test.|
| 5. Worked sessions for The Catch (claude.ai Pro, then ChatGPT Plus, Gemini) and Long Places I.|
+-----------------------------------------------------------------------------------------------+
```

**Evidence labels.** **[V]** read on the official page. **[V-sec]** seen only in a search excerpt of the official page or on a secondary site (OpenAI's help pages block automated reading: HTTP 403 on 2026-09-27). **[U]** undocumented or unverified: the §5.3 smoke test checks it. **[J]** my judgment. [S#] points to Sources; every URL was checked 2026-09-27. Re-check any fact older than a month (C5 R22).

**Fact-check pass, 2026-09-27.** A second reader re-opened 30 of the cited pages. Corrected: Claude Pro includes Fable only through paid usage credits (§3.1); consumer Claude plans have network access on by default and the sandbox can read project files (§3.1, which settles one open question in §13); ChatGPT Plus Instant has a 54K window, too small for the whole *Long Places* (§2.3, §3.3); Gemini's free plan, not AI Plus, is the one described as "3.6 Flash" with "varying access to 3.1 Pro" (§3.4); Gemini Spark is AI Ultra only, US only, in beta (§3.4, §5.1, §6.1); custom GPTs retire on 11 Dec 2026 (§3.3); the Gemini API terms date is 28 Apr 2026; the puck line references in §10.4. Added: ChatGPT message caps, Canvas downloads, GPT-6 Sol API price, Haiku 4.5's retirement date, and plain definitions in §0. All quotations from *The Catch* and *The Long Places* were checked against the files and are verbatim.

**Builds on:** C5 §6.2, §6.11, Recipe 1, P1, R17–R19, §10.3; C2 §3.7 and R1; C1 P1; C4 §5.1.

## 0. Terms (one plain sentence each)

- **Surface**: one app you type into (claude.ai, Claude Code, ChatGPT, the Gemini app, AI Studio, NotebookLM).
- **Token**: the unit an LLM counts text in; English prose runs about 1.2 to 1.8 tokens per word.
- **Context window**: the most text (files, chat so far, and reply) the model can hold at once.
- **Reply limit**: the most text the model writes in one reply before stopping.
- **Truncation**: a reply that stops mid-way, leaving broken JSON.
- **Silent shortening**: a finished-looking reply that skipped records or wrote "..." instead.
- **Part**: one reply's share of a scene file, named by its first and last record ID (SH010–SH180).
- **END line**: a fixed last line the model writes after each part; if it is missing, the reply was cut off.
- **Project knowledge**: files stored once in a Claude Project, ChatGPT Project, Gem or Notebook so every chat there can see them.
- **Retrieval mode**: the app shows the model only fragments of stored files that match the request.
- **Sandbox**: a temporary computer inside the chat app where the model runs Python and makes files to download.
- **Connected folder**: a folder on your computer that an agent mode (Claude Cowork, ChatGPT Work, Gemini Spark) reads and writes directly.
- **Snapshot**: a ZIP of the whole project folder saved at the end of a session.
- **State files**: the files that carry the project between sessions (C5 §10.3).
- **Usage limit**: the plan's cap on use per time window.
- **Smoke test**: a 10-minute trial of everything the pipeline needs, before real work.
- **JSON**: a plain-text format for records (`{"id": "SC06-SH140", "size": "medium wide"}`); one missing bracket makes the whole file unreadable to a program.
- **Validator** (`validate.py`): a small program that checks every file against the rules and prints one line per problem; it never changes the file.
- **Hash**: a short fingerprint computed from a file or record; if one character changes, the fingerprint changes, so it proves a locked record was not edited.
- **ZIP**: one file that packs a whole folder; you download it, then "unzip" (extract) it into your folder.
- **API**: paying per token to use a model from a program instead of a monthly app subscription.
- **Connector (MCP)**: a plug-in that lets the chat app use another service, such as an image or video generator.
- **Usage credits**: extra paid usage on top of a Claude plan; Claude Pro reaches the Fable model only this way [V S1].

## 1. Core principles

1. **Files are the memory; chats are disposable** [J]. Every approved result lives in a state file on your computer, so any chat can be lost without losing work. Chat history and app memory are never trusted for pipeline state.
2. **One scene per call, one part per reply** [J, extends C5 R17]. A call is sized by the context pack; a reply is sized by the part rule (§2.4).
3. **Attach what must be read whole** [J]. Paid Claude projects switch to retrieval mode near capacity [V S5], so packs and previous scenes are attached to the message.
4. **Plan short, then expand** [J]. The one-line shot list is approved first (checkpoint C), then expanded into full records by ID range, so every part is checkable.
5. **Check every reply** [J, C5 R9–R10]: the validator after every part; where no Python runs, a fresh-chat checklist.
6. **Close every session with a snapshot** [J]: update `manifest.json`, download one ZIP, unzip it into your folder. ChatGPT sandbox files vanish when a chat idles [V-sec S28]; Claude says created files "remain available for download throughout conversations" [V S6], but how long after the chat goes quiet is [U], so download anyway.
7. **Privacy before the first upload** [J]: training off everywhere (§8).
8. **Portable** [J, C5 R19]: scripts use only Python's standard library; instructions avoid one-app features.

## 2. Sizing the work

### 2.1 The two sources

Measured with OpenAI's `o200k_base` tokenizer [V, own measurement S44; re-measured by the fact-checker with tiktoken 0.14.0, same totals]. Claude's current tokenizer (since Opus 4.7) fits "roughly 555k words" in 1M tokens, against about 750k words for older models [V S12], so Claude counts can be up to about 1.35 times these [J]. "With line numbers" depends on the format: `253 He is...` adds about 28% to *The Catch*; right-aligned `  253  He is...` adds about 45% [own measurement].

| Source | Words | Lines | Tokens (o200k) | With line numbers | Claude estimate [J] |
|---|---|---|---|---|---|
| *The Catch* | 9,217 | 1,852 | 12,484 | 15,900–18,100 | 16k–24k numbered |
| *The Long Places* (14 chapters) | 49,152 | 1,444 | 60,998 | 63,600–65,500 | 64k–88k numbered |
| *Long Places* ch. I (lines 5–83) | 3,025 | 79 | 3,759 | about 4,000 | 4k–5.5k |
| Largest chapter, XIV | 4,669 | 159 | 5,686 | about 6,000 | 6k–8k |

### 2.2 The size of one scene file

Measured on example records with C5 §10.2's fields [V, own measurement]: full shot record **609 tokens, about 1.8 KB** of indented JSON; beat 104; cut 79; C5's abbreviated E3 record 418.

| Scene file | Contents | Tokens (o200k) | Size | Claude estimate [J] |
|---|---|---|---|---|
| `scenes/SC06.json` | ~36 shots (A4 WE1), ~14 beats, 36 cuts, header | about 26,700 | about 80 KB | about 35k |
| `scenes/SC13.json` | ~31 shots, 16 beats (A2), 31 cuts, header | about 23,400 | about 70 KB | about 31k |
| All 30 scenes (~300 shots) | whole film | about 230,000 | about 700 KB | about 300k |
| One scene's context pack (C5 P2) | as C5 P2 | 12,000–15,000 | 40–50 KB | 16k–20k |

### 2.3 What fits where

| Job | Claude paid (200K standard; 1M on newest models) | ChatGPT Plus (Instant 54K; Thinking 256K [V-sec S47]) | Gemini app AI Pro (1M) | Gemini app free (32K) |
|---|---|---|---|---|
| Whole *Catch*, numbered (stage 1) | fits | fits in both modes; Instant leaves about 35K for the reply and chat | fits | fits, little room left |
| Whole *Long Places*, numbered (stage 1) | fits | Thinking only; **does not fit Instant** | fits | no: use chapter summaries |
| One context pack (stages 4–5) | fits | fits | fits | fits |
| SC06 full file in **one reply** | risky: not documented in the app [U] | risky [U] | risky: API cap 65,536 [V S37] | no |
| SC06 in **two parts** of 18 shots | yes [J] | yes [J] | yes [J] | not tested |

**If** a job's input (files plus chat so far) is more than about 60% of the window, **then** start a new chat with only the files the job needs, **because** the reply and later turns need the rest, and Claude's automatic summarizing "consume[s] more of your usage limit" [V S3] and drops exact records [J].

### 2.4 The part rule

**If** a scene has more than 18 shots, **then** expand it in parts of at most 18 shots with their cut records, split by ID range from the approved one-line list, **because** 18 full records plus cuts are about 12,500 tokens (o200k), well under every documented cap (Gemini 65,536 [V S37]; Claude and GPT-5.6 128K through the API [V S12, S25]), and models shorten long repetitive lists well before they reach a hard cap [J]. Beats go in their own reply (stage 4) before any part.

- SC06 (36 shots): part 1 = `SC06-SH010` to `SC06-SH180`; part 2 = `SC06-SH190` to `SC06-SH360`.
- SC13 (31 shots): part 1 = `SH010`–`SH180`; part 2 = `SH190`–`SH310`.
- **If** the smoke test (§5.3 step 3) shows shortening before 20 records, **then** use parts of 12 (`SH010`–`SH120`, `SH130`–`SH240`...).
- Every part ends with the END line, exactly: `END SC06 PART 1 OF 2 | SC06-SH010..SC06-SH180 | 18 SHOTS | 18 CUTS`.

C5 R17 still holds: the call carries one scene's pack; only the reply is split.

## 3. Surface sheets (dated 2026-09-27)

Names and limits change often: re-check, do not memorize.

### 3.1 claude.ai (web, desktop and mobile apps)

| Item | Fact |
|---|---|
| Plans and price | Free $0; Pro $20 a month or $17 a month billed yearly; Max from $100 a month (5x or 20x Pro usage per 5-hour session) [V S1] |
| Models | Free: Sonnet, Haiku. Pro and Max: Opus, Sonnet, Haiku, plus Fable through paid "usage credits" [V S1]. API names: Fable 5.1, Opus 5.5, Sonnet 5, Haiku 4.5 [V S12] |
| Context window | Paid plans: 200K for most models; 1M for Fable 5.1, Opus 5.5, Opus 5 and Sonnet 5; 500K for Fable 5 and Opus 4.6–4.8 [V S2]. Cowork and Claude Code: 1M on the newest models [V S2]. Near the limit, "Claude summarizes earlier messages", which needs code execution on and uses more of the usage limit [V S3] |
| Reply limit | Not documented for the app [U]; the pricing page lists "Higher output limits for all tasks" as a Max benefit [V S1], so the app's reply cap differs by plan. The API allows 128K output on Opus 5.5, Sonnet 5 and Fable 5.1, 64K on Haiku 4.5 [V S12] |
| Uploads | 500 MB per chat file; 20 files per chat; 30 MB per project file; PDF, DOCX, CSV, TXT, HTML, ODT, RTF, EPUB, JSON, XLSX, images [V S4]. Rename `.fountain` to `.txt` if refused [U] |
| Persistence | Chat files stay in their chat; project files persist [V S4]. Free: 5 projects [V S5]. Paid projects switch to retrieval mode near capacity ("up to 10x" more room) [V S5] |
| Python | "Code execution and file creation" on every plan (Settings > Capabilities). Free, Pro and Max have network access on by default, so the model can install packages [V S6]. "Files in your projects are now accessible through Claude's computing environment" [V S6], so `validate.py` can read project files |
| Downloads | Yes: .xlsx, .pptx, .docx, .pdf named; 30 MB per file for uploads and downloads; files "remain available for download throughout conversations" and can be saved to Google Drive [V S6]. JSON, CSV, ZIP [U: smoke test step 4] |
| Skills | All plans; Customize > Skills > "+" > "+ Create skill" > "Upload a skill"; needs code execution; ZIP size cap not stated [V S7]. Syncs one way to Claude Code (v2.1.273+) at session start and about every 10 minutes; off with `syncClaudeAiSkills: false` [V S7] |
| Connectors (MCP) | Customize > Connectors > "+" > "Add custom connector" on every plan; Free is limited to one [V S8] |
| Usage caps | "five-hour session" limit plus weekly limit, shown as progress bars in Settings > Usage [V S11]; cached project content "count[s] less against your limits" when reused [V S11]; file creation uses more [V S6]. Pro gives about 5x Free per 5-hour session; Max 5x or 20x Pro [V S1]. A secondary count: about 45 average messages per 5 hours on Pro [V-sec S48] |

### 3.2 Claude desktop: Cowork and Claude Code

- **Cowork** (Pro, Max, Team, Enterprise; desktop on macOS and Windows, and also on the web and mobile for Pro and Max): select "Cowork" in the message box. "On desktop, Claude can read from and write to your local files without manual uploads or downloads"; the work "runs on Anthropic's servers, in an isolated environment"; it uses your connectors and plugins; multi-step tasks "use more of your usage than a quick question" [V S10]. On the desktop app the `CATCH/` folder becomes the state store, with no download step [J]; on the web and mobile there is no local folder [J from V S10].
- **Claude Code** (Pro and Max; usage shared with the chat apps) [V S9]: runs on your own computer, so it can run the scripts, OpenTimelineIO and Blender in background mode (C4 Mode B). It is the only Claude surface for local previs [J].

### 3.3 ChatGPT

| Item | Fact |
|---|---|
| Plans and price | Free; Go $8 (priced by region); Plus $20; Pro $100 (5x Plus usage) and $200 (20x) a month [V-sec S29] |
| Models | Instant runs GPT-5.6 Sol on paid plans and GPT-5.6 Luna on Free and Go; the Thinking slider (Medium, High, Extra High by plan) uses GPT-5.6 Sol [V-sec S18]. GPT-6 Sol and Luna launched 22 Sep 2026 in ChatGPT Work, Codex and the API, and are rolling out gradually to ChatGPT paid accounts [V-sec S26]; GPT-6 Astra (announced 3 Sep 2026) shows as "GPT-6 Pro" on Pro [V-sec S29]. Picker names change weekly: note the exact name in `sessions[]` |
| Context window | Instant: 27K Free, 54K Go and Plus, 128K Pro. Thinking: 256K Go and Plus, 400K Pro [V-sec S47, two secondary sites agree, Sept 2026]. An older excerpt said "128K for Instant and Thinking" [V-sec S18]: the smoke test decides |
| Reply limit | Not documented in the app [U]; GPT-5.6 Sol and GPT-6 Sol through the API: 128K output, 1.05M context [V S25, S49] |
| Message caps | Plus has no published cap on ordinary chats; a secondary guide gives about 10–100 Sol (Thinking) messages per 5 hours on Plus, higher for lighter models [V-sec S48]. Treat as [U] |
| Uploads | 512 MB per file; text files capped at 2M tokens; up to 80 uploads every 3 hours [V-sec S16] |
| Persistence | Projects: 5 files (Free), 25 (Go, Plus), 40 (Pro), 10 per upload; project memory draws on the project's chats, or "project-only" memory chosen at creation [V-sec S17]. Custom GPTs retire on 11 Dec 2026; personal accounts can no longer create new ones [V-sec S24]: do not use |
| Python | Data analysis: a "stateful Jupyter notebook" with no internet access [V-sec S19], so no `pip install`; files expire when the session idles, exact time [U] [V-sec S28] |
| Downloads | Yes, through sandbox links; ZIP links sometimes fail and must be re-made [V-sec S28]. Canvas code documents download with a language extension (`.py`, `.js`); text documents as PDF, `.md` or `.docx` [V-sec S50]; whether a JSON canvas downloads as `.json` is [U] |
| Skills | Upload: Business, Enterprise, Healthcare, Edu only; not Free, Plus or Pro [V-sec S22]. Standalone skills run in the ChatGPT desktop app, Codex CLI and IDE extension [V S23]. On Plus, paste instead (§10.6) |
| Connectors (MCP) | Developer mode: "Pro, Plus, Business, Enterprise, and Education accounts on the web": Settings > Security and login > Developer mode; marked "Elevated risk" [V S20] |
| Agent with folder | ChatGPT Work in the desktop app uses a local folder you grant; on the web it cannot read your computer; rolling out gradually [V-sec S27] |

### 3.4 Gemini app, Google AI Studio, NotebookLM

| Item | Fact |
|---|---|
| Plans and price | Google AI Plus $4.99, AI Pro $19.99, AI Ultra from $99.99 (a higher tier $199.99) a month [V S31] (C2 recorded AI Plus at $7.99; the page may show an offer) |
| Models | Free: "Access to 3.6 Flash" and "Varying access to 3.1 Pro"; AI Plus: everything in Free with more access; AI Pro: 3.1 Pro with "4x higher usage limits than Free" [V S31] |
| Context window | No plan 32K; AI Plus 128K; AI Pro and Ultra 1M tokens [V S30]; Deep Think (AI Ultra only) uses 192K [V S30, S32] |
| Reply limit | Not documented in the app [U]; Gemini 3.1 Pro through the API: 65,536 output tokens [V S37] |
| Uploads | Up to 10 files per prompt; 100 MB per file (2 GB video); a ZIP up to 100 MB holding up to 10 files, no audio or video [V S32]. The page lists no file types by name, so `.json` and `.txt` are [U]: smoke test step 1 |
| Persistence | Notebooks in Gemini (since 8 Apr 2026; AI Plus, Pro and Ultra on the web first, mobile and free later) keep chats, instructions and files; "any source you add in one place automatically appears in the other" (NotebookLM) [V S35]. Gems keep a name, instructions and files; a file added from Drive is re-read at its "most recent version" [V S46]; file count undocumented [U] |
| Python | No documented Python sandbox in chat [U]. Canvas exports Python to Colab: "At the top of the Canvas panel, click Export to Colab" [V-sec S33] |
| Downloads | Since 29 Apr 2026, for all users: Docs, Sheets, Slides, .pdf, .docx, .xlsx, .csv, LaTeX, TXT, RTF, MD; JSON and ZIP not listed [V S34] |
| Skills and MCP | No skill upload found in the app [U]. Gemini Spark (macOS desktop agent) reads folders you link; beta, AI Ultra only, US only, 18+; custom MCP support "arriving" [V-sec S43] |
| Usage caps | "Your limit refreshes every 5 hours until you reach your weekly limit"; AI Plus "2x", AI Pro "4x higher than standard limits"; Ultra 5x or 20x AI Pro [V S30]. No prompt counts published |
| **Google AI Studio** | Gemini 3.1 Pro (preview, Feb 2026) and 3.8 Flash: 1,048,576 in, 65,536 out; code execution, structured output [V S37, S45]. Free tier trains on content, human reviewers [V S39] |
| **NotebookLM** (now Gemini Notebook [V-sec S42]) | 50/100/300 sources per notebook, 100/200/500 notebooks and 50/200/500 chats a day (free/Plus/Pro); the page warns of changes from 2 Sep 2026 [V S40]. For questions about the novel, not long JSON [J] |

## 4. Decision rules

1. **If** a file must be read whole (context pack, previous scene, file being checked), **then** attach it to the message, **because** project knowledge may be searched in fragments [V S5; J].
2. **If** the surface runs Python, **then** run `validate.py` after every part and every merge, **because** a schema guarantees shape, not meaning (C5 R9–R10).
3. **If** it runs no Python, **then** run the §6.3 checklist in a **fresh** chat and the real validator at the next chance (claude.ai Free has code execution [V S6]), **because** self-review lowers accuracy (C5 R12) and an independent check does not share the writer's blind spots [J].
4. **If** a reply lacks the END line, its count differs from the approved list, or it contains "...", "…", "etc.", "same as above", "remaining" or "omitted", **then** treat the part as unsaved and send a continue prompt (§6.2), **because** silent shortening leaves no other trace [J].
5. **If** a chat has handled one sequence, or the app says it is summarizing earlier messages, **then** start a new chat and resume from files, **because** summaries drop exact records [J from V S3].
6. **If** the usage bar passes about 80%, **then** finish the current part, save, snapshot and stop, **because** a limit that hits mid-part leaves half a record [J].
7. **If** a session ends, **then** update `manifest.json` and download the snapshot first, **because** ChatGPT sandbox files expire when idle [V-sec S28] and Claude only promises availability "throughout conversations" [V S6].
8. **If** the pipeline runs on more than one app, **then** keep scripts on Python's standard library (`export_otio.py` writes OTIO's JSON directly), **because** ChatGPT's sandbox has no internet [V-sec S19] and cannot `pip install`.
9. **If** the manuscript is unpublished, **then** turn training off everywhere before uploading and never use free Google AI Studio, **because** free-tier content may be read by human reviewers [V S39].
10. **If** an app offers memory (Claude memory, ChatGPT project memory, Gemini personal context), **then** turn it off for this project or ignore it, **because** remembered facts from older versions can contradict the state files [J].
11. **If** a record is `"locked": "yes"`, **then** it is read-only in every session and the validator compares it with the manifest's hash (D1-V14), **because** locks live in data, not in the chat (C5 R18).
12. **If** a text-only analysis is refused, **then** follow §6.5 and never try to trick the model, **because** the pipeline needs staging, not graphic description [J].
13. **If** choosing a model for a stage, **then** use §7.1 and keep the smallest that passes the validator (C5 R19), **because** larger models use the usage limit faster [J].

## 5. Choosing a surface

### 5.1 Decision tree

1. **Breakdown only** (JSON, CSV, readable document):
   - Best: **Claude Pro** with a Project, the skill and code execution, or **Cowork** with a connected `CATCH/` folder [J from V S1, S6, S7, S10].
   - No budget: **claude.ai Free** (5 projects, skills, code execution, Sonnet) [V S1, S5]; expect frequent usage stops [J].
   - Already on ChatGPT Plus: a **ChatGPT Project**, Thinking, data analysis [J].
   - Already on Google AI Pro: a **Notebook in Gemini**; validation through Colab or claude.ai Free [J]. Gemini Spark's local folder needs AI Ultra in the US [V-sec S43], so AI Pro works from the downloaded folder.
2. **Plus storyboards** (C2): keep the breakdown in Claude; for under about 150 frames use C2's chat-only path (paste compiled prompts into the Gemini app or ChatGPT); above that, a connector (C1 P1) [J from C2 R1].
3. **Plus previs** (C4): **Claude Code** on your computer with Blender installed (C4 Mode B, headless). If you will not install anything, Mode A works from any surface: the LLM writes the script, you run it in Blender [J from C4 §5.1].
4. **Plus generation through connectors** (C1): **Claude** (custom connectors on every plan, one on Free [V S8]) or **ChatGPT Plus developer mode** on the web [V S20]. Not the Gemini app, which has no custom connectors today [V-sec S43].

### 5.2 Setup clicks

**claude.ai Pro** (15 minutes):
1. Settings > Privacy > turn off "Help Improve our AI models" [V S14].
2. Settings > Capabilities > turn on "Code execution and file creation" [V S6].
3. Customize > Skills > "+" > "+ Create skill" > "Upload a skill" > choose `breaking-down-screenplays.zip` [V S7]. Test: "Which skills do you have? Describe breaking-down-screenplays in two sentences." (C5 Recipe 1).
4. Projects > new project named `CATCH breakdown`; paste the project instructions from §10.1 [U: exact button label].
5. Settings > Usage: note when your 5-hour session resets and how much of the weekly limit is left [V S11].
6. Make a folder on your computer: `CATCH/` with the C5 §10.3 subfolders plus `snapshots/`.

**ChatGPT Plus** (15 minutes): Settings > Data controls > turn off "Improve the model for everyone" > Done [V-sec S21]; new Project `CATCH breakdown` with project-only memory [V-sec S17]; paste a short `SKILL.md` as instructions (§10.6); upload the rule and script files (at most 25 files, 10 at a time [V-sec S17]); in the model picker choose Thinking for stages 1–5, because Instant's 54K window is too small for the novel [V-sec S47]. For connectors: Settings > Security and login > Developer mode [V S20].

**Gemini app, AI Pro** (15 minutes): Gemini Apps Activity > "Keep Activity" off (chats then kept 72 hours and gone from history [V S36], so resume only from your folder); a Notebook `CATCH breakdown` with the rule file and state files as sources [V S35]; the Pro model in each chat. Whether Notebooks keep chats with Keep Activity off is [U]. Alternative: a Gem whose knowledge files are added from Google Drive, because Gemini then uses "the most recent version of the file" [V S46], so replacing `bible.json` in Drive updates the Gem with no re-upload (whether Drive `.json` files are accepted is [U]: smoke test step 5).

**Claude Code** (previs, 20 minutes): install it, sign in with the Pro account [V S9], open `CATCH/`, install the skill (C5 Recipe 1), then C4 P9 for Blender.

### 5.3 The 10-minute smoke test (run on every new surface or plan)

1. Attach *The Catch* .txt. "How many lines does this file have, and what is line 253, word for word?" Pass: 1,852 lines and "He is looking straight at her. He has one hand she cannot see." A wrong line means the file was cut or fragmented.
2. Attach *The Long Places*. "Quote line 1385." Pass: "Going down for the evening round she passed the schoolteacher's mat. Seher did not open her eyes. "Was it kept, Hanım?"" (tests a 61k-token input read to the end).
3. "Write 20 complete shot records for SC06 using this example record [paste C5 E3], IDs SC06-SH010 to SC06-SH200, all fields filled, then the END line `END TEST | 20 SHOTS`." Pass: 20 records, no "...", END line present. Fail: set the part size to 12.
4. "Using Python, count the lines in the attached file, write `test.json` containing {"ok": "yes"}, zip it as `test.zip`, and give me both to download." Pass: both files download and open. Fail: no sandbox; use rule 3.
5. In a new chat in the same Project or Notebook: "Quote line 1 of `scenes_index.json` from project knowledge." Pass: exact quote (tests persistence).
6. "Give a one-line shot list for The Catch lines 214–224 (the gunshot)." Pass: a normal answer (§6.5).
7. Confirm training is off in the privacy settings; record `training_optout` in `manifest.json`.

## 6. Keeping state between sessions

### 6.1 Three ways to store the C5 §10.3 files

| Store | How | Good for | Watch for |
|---|---|---|---|
| **(a) Project knowledge** (Claude or ChatGPT Project, Gemini Notebook) | Film-level files only: `source.fountain`, `scenes_index.json`, `story_analysis.json`, `bible.json`, `ledger.json`, `manifest.json`, rules | Fewer attachments | Retrieval mode (rule 1); ChatGPT's 25-file cap; stale versions: delete the old file before uploading the new |
| **(b) Local folder** (always: the master copy) | `CATCH/` on your computer; each session's ZIP unzipped into it | Every surface; survives app changes | Download and unzip every time |
| **(c) Connected folder** (Cowork, ChatGPT Work, Gemini Spark) | The agent reads and writes `CATCH/` | No download step | Desktop apps on paid plans only (Spark: AI Ultra, US, beta [V-sec S43]); grant this folder only [V S10] |

Scene files stay out of project knowledge: all 30 are about 300k Claude tokens and would force retrieval mode [J from §2.2]. Attach only the previous scene's file.

**Naming and versions** [J]. File names never change (`bible.json`, `scenes/SC06.json`), so instructions and scripts always find them. Each file carries `file_meta.file_version` (rises by one on every save) and `saved_at`; `manifest.json` lists every file's version, record count and hash. Snapshots are named `CATCH_S04_2026-10-02_after-SC07.zip` (project, session, date, last finished scene). To undo a session, unzip the previous snapshot.

**How locks survive** [J]. A lock is the field `"locked": "yes"` inside the record, so it travels with the file; `manifest.json` keeps each locked record's hash. At session start the validator compares them (D1-V14); any change rejects the file. To change one, write "unlock SC06-SH140"; the log records it.

**The resume message** (exact form):

> Resume stage 5 at SC07; attached bible.json, ledger.json, scenes/SC06.json.
> Also attached: manifest.json, scenes_index.json, source.fountain.
> Records with "locked": "yes" are read-only.
> First run validate.py on the attached files and tell me the resume_point in manifest.json. Then wait for me to say "go".

**The close message** (exact form, added in the fact-check pass) [J]:

> Close session S04. Update manifest.json: file_meta for every changed file, resume_point (stage, scene, last_record, next_record) and one sessions[] row. Run validate.py on everything. Then give me one ZIP named CATCH_S04_<date>_after-SC07.zip with the whole CATCH folder, and list every file inside it with its file_version.

**Unzipping, for someone who has never done it** [J]: on Windows, right-click the downloaded ZIP > "Extract All..." > choose the `CATCH` folder > when asked, replace the files. On a Mac, double-click the ZIP; it makes a folder beside it; drag everything inside into `CATCH` and choose "Replace". Then move the ZIP itself into `CATCH/snapshots/`. **If** the file list in the chat differs from what you see in the folder, **then** do not start the next session until they match.

### 6.2 Catching cut-off and shortened JSON

Signs, strongest first [J]: (1) the END line is missing or its count differs from the records received; (2) the JSON does not parse (V1) or lacks closing brackets; (3) the IDs differ from the approved list for that range; (4) the text contains "...", "…", "etc.", "same as above", "remaining shots", "omitted for brevity" or a `//` comment; (5) a record lacks schema fields (V1); (6) the part is far smaller than expected (18 shots with cuts are about 35 KB; under 25 KB is suspect); (7) the app shows "Continue" or the reply stops mid-word.

**Continue prompts** (paste exactly, changing the IDs):
- Cut mid-record: "Your reply stopped inside SC06-SH170. Discard it. Send SC06-SH170 to SC06-SH180 again, complete, then the END line. Do not repeat earlier records."
- Records skipped: "Your part 1 skipped SC06-SH120 and SC06-SH130. Send only those two records, complete, then `END SC06 PATCH | 2 SHOTS`."
- Continue from a record: "Continue from record SC06-SH190: send SC06-SH190 to SC06-SH360 as part 2, complete, then the END line."

Never hand-repair brackets: re-request the part [J]. Save a part only after it passes; `parts[]` records `complete` or `partial`.

### 6.3 Checking without Python (fresh-chat checklist)

In a new chat, attach the part, the approved list and the scene's previous version, and paste: "Answer each question yes or no, then list every problem as record ID, field, problem."

1. Does the text begin with `[` or `{` and end with the matching bracket?
2. Is the END line present, and do its counts equal the records present?
3. List every shot ID. Does the list equal the approved list for this range, in steps of 10?
4. Does any record contain "...", "…", "etc." or "same as above"?
5. Does every shot have all fields of the example record, with `"none"` for empty ones?
6. Is every `source_lines` value inside the scene's line range in `scenes_index.json`?
7. Is every enum value lower-case and from the allowed list?
8. Do the shots' `duration_s` values add up to the scene's `target_duration`, give or take 10%?
9. Is every locked record identical, word for word, to the same record in the previous version?
10. For shots in lines 224–258 of SC06: is `PR-PUCK.S02` absent from the frame, as `withhold` requires?

Weaker than code (C5 R12): run `validate.py` at the next chance.

### 6.4 Failure modes

| Symptom | Likely cause | Fix |
|---|---|---|
| Line 253 quoted wrongly | File retrieved in fragments or cut at upload | Attach the file to the message; split the source by scene |
| Reply ends mid-record | Reply limit | Continue prompt; smaller parts |
| 18 records asked, 14 returned, no error | Silent shortening | Rule 4; re-request missing IDs |
| "File not found" on a download link | Sandbox expired [V-sec S28] | Ask to re-make the file; next time download at once |
| Validator says a locked record changed | Model rewrote approved work | Reject the file; re-send the previous version; repeat the lock rule |
| Old bible facts appear | Two versions in project knowledge, or memory | Delete old versions; turn memory off (rule 10) |
| Gemini problems | JSON not downloadable; 10-file cap | See §10.6 |
| ChatGPT answers about late chapters of *The Long Places* are vague or wrong | Instant's 54K window holds less than the numbered novel (about 64K) [V-sec S47] | Switch to Thinking; repeat smoke test step 2 |
| A model name vanished from the picker | Retirement or rollout (Haiku 4.5 from 15 Oct 2026 [V S12]; GPT-6 Sol [V-sec S26]) | Pick the next tier up, log it in `sessions[]`, re-run SC06/SC13/SC15 (C5 R32) |

### 6.5 When an app refuses the SC06 gunshot and blood

Lines: "Far above, the stair door gives with a crash. Someone KICKS the top gate open and FIRES down through the roof." (l.216), "He sits down into Eli with a hole through his shoulder." (l.222), and "Jude's blood lifts off the steel in round red beads and hangs in the air between them, turning." (l.244). Text analysis of such fiction is normally accepted [J]; refusals are likelier in image and video generation (C1).

If a text stage refuses [J]:
1. Say once: "This is pre-production for my own short film. I need camera, staging and continuity fields only, no graphic description."
2. Use production words: "gunshot sound effect", "wound make-up on Jude's shoulder", "blood beads, a composited visual effect".
3. If refused again, run that scene on another model or surface and log it in `refusals[]` (§9). Never disguise the content: it is a legitimate film scene. (Through the API, Claude marks this `stop_reason: "refusal"`, C5 P4.)

## 7. Models and money

### 7.1 Model tier per stage [J, following C5 R19]

| Stage | Claude | ChatGPT | Gemini |
|---|---|---|---|
| 0 Intake (script does the work) | Sonnet 5 | Instant | Flash |
| 1 Story analysis | Opus 5.5; Fable 5.1 (paid usage credits on Pro and Max [V S1]) for the whole novel only if Opus falls short | Thinking | 3.1 Pro |
| 2 Bible, identity keys | Opus 5.5 | Thinking | 3.1 Pro |
| 3 Ledger | Sonnet 5, Opus for prose | Thinking | 3.1 Pro |
| 4 Scene design, 5a one-line list | Opus 5.5 | Thinking | 3.1 Pro |
| 5b Expanding approved lists | Sonnet 5; test Haiku 4.5 | Instant or Thinking | Flash |
| 6–9 Prompts, export (scripts) | any | any | any |

Test the smallest first: run SC06 and SC13 through stage 5b on Haiku 4.5 or Flash; if the validator and checkpoint C pass, keep it for expansion (C5 P9). Haiku 4.5's API retirement is "Not sooner than October 15, 2026" [V S12]: **if** it disappears from the picker, **then** use Sonnet 5 for 5b and re-run the SC06/SC13/SC15 test (C5 R32). On ChatGPT, GPT-6 Sol may replace GPT-5.6 Sol in the picker during the project [V-sec S26]: record the model name per session and re-run the test scenes after a switch.

### 7.2 Subscription or API

Estimate for *The Catch* [J from §2]: about 1.5M input and 0.35M output tokens (o200k), including 30% re-runs; about 2.0M and 0.45M in Claude tokens. At API prices:

| Model (price per million tokens, in / out) | Cost for *The Catch* [J] |
|---|---|
| Claude Fable 5.1 ($10 / $50) [V S12] | about $43 |
| Claude Opus 5.5 ($4 / $20) [V S12] | about $17 |
| Claude Sonnet 5 ($2 / $10) [V S12] | about $9 |
| Claude Haiku 4.5 ($1 / $5) [V S12] | about $4 |
| GPT-5.6 Sol ($4 / $20) [V S25] | about $13 |
| GPT-6 Sol ($2 / $10) [V S49] | about $7 |
| Gemini 3.1 Pro ($2 / $12 up to 200K-token prompts; $4 / $18 above) [V S38] | about $7 |

*The Long Places* is about five times the source and more invention: roughly $40–85 on Opus 5.5 [J]. Claude's Batch API halves prices [V S12]. These figures exclude thinking tokens, which are billed as output and can double the output cost [J]. Gemini 3.1 Pro doubles its input price for prompts over 200K tokens [V S38]: one scene per call keeps every call far below that.

**Rule** [J]: **if** the user will not handle API keys, **then** subscribe (Claude Pro, $20 for a month or two), **because** the API saves little at this size and needs setup. **If** a rule change forces re-running all 30 scenes (C5 R32), **then** consider batch API through Claude Code.

## 8. Privacy for an unpublished manuscript

| Surface | Setting | What happens [label] |
|---|---|---|
| claude.ai Free, Pro, Max | Settings > Privacy > "Help Improve our AI models" off [V S14]; when off, "we will not use any new chats and coding sessions you have with Claude for future model training" [V S14] | If on: kept "in a de-identified format for up to 5 years" [V S13]; if off, the 30-day retention applies [V-sec S15]. Deleted chats leave back-end storage "within 30 days"; incognito chats are not used to improve Claude even with the setting on; content flagged for policy violations is kept up to 2 years [V S13] |
| ChatGPT | Settings > Data controls > "Improve the model for everyone" off > Done [V-sec S21] | New chats are then not used for training but stay in history. Temporary Chats are not used for training; OpenAI may keep a copy up to 30 days; a Temporary Chat you save becomes a normal chat [V-sec S21] |
| Gemini app | "Keep Activity" in Gemini Apps Activity [V S36] | Default auto-delete 18 months (3 or 36 months selectable); with it off, chats kept 72 hours; chats read by human reviewers kept up to 3 years; thumbs up/down feedback sends the conversation to reviewers; Google says "Please don't enter confidential information that you wouldn't want a reviewer to see" [V S36] |
| Google AI Studio, free tier | none | Content used to improve products; "Human reviewers may read, annotate, and process your API input and output"; "Do not submit sensitive, confidential, or personal information to the Unpaid Services" [V S39]. Paid tier: "Google doesn't use your prompts ... or responses to improve our products" [V S39] |
| NotebookLM / Gemini Notebook | none needed | "will not be used to directly train our foundational AI models, unless you choose to provide feedback"; reviewed feedback kept up to 3 years [V S41]; data shared with the Gemini app follows the Google Privacy Policy [V S41]. Notebooks in Gemini sync sources both ways [V S35], so a manuscript added in the Gemini app is also governed by the Gemini app's settings [J] |

**Rule** [J]: **if** the manuscript is unpublished, **then** use Claude or ChatGPT with training off, or NotebookLM for questions; in the Gemini app keep Keep Activity off and never press thumbs up or down; never use free AI Studio, **because** feedback and free-tier content reach human reviewers [V S36, S39, S41].

## 9. Fields this subject adds to the breakdown

Enums lowercase `snake_case`; empty is `"none"`; all `derived` (script or session-close step) unless marked.

| Level | Field | Meaning | Allowed values |
|---|---|---|---|
| film (manifest) | `surface` | App running the pipeline | `claude_web` \| `claude_cowork` \| `claude_code` \| `chatgpt_web` \| `chatgpt_work` \| `gemini_app` \| `ai_studio` \| `other` |
| film | `code_execution` | Whether Python runs there | `yes` \| `no` |
| film | `state_store` | Where state lives between sessions | `project_knowledge` \| `local_folder` \| `connected_folder` |
| film | `training_optout` | Training setting checked (authored by human) | `confirmed` \| `not_confirmed` |
| film | `part_size` | Most shots per reply, from the smoke test | integer, default `18` |
| film | `resume_point` | Where the next session starts | object: `stage`, `scene`, `last_record`, `next_record` |
| film | `sessions[]` | One row per session | `session_id` (`S01`...), `date`, `surface`, `plan`, `model`, `stages`, `scenes`, `snapshot_file` |
| every file | `file_meta` | Version stamp | `project`, `path`, `file_version` (integer), `saved_at` (ISO date-time), `stage`, `model`, `record_count`, `content_hash` (or `"none"` where no code ran) |
| scene | `shot_plan_approved` | Checkpoint C passed before expansion | `yes` \| `no` |
| scene | `parts[]` | One row per reply part | `part_id` (`SC06-P1`), `first_record`, `last_record`, `expected_count`, `received_count`, `end_line_seen` (`yes` \| `no`), `status` (`complete` \| `partial` \| `missing`) |
| log | `refusals[]` | Refused requests | `surface`, `model`, `stage`, `record`, `action` (`restated` \| `switched_model` \| `human_handled`) |

**New validator checks** (numbered to avoid C5's V1–V13): **D1-V14** every locked record equals its hash in `manifest.json`; **D1-V15** every part's IDs equal the approved list for its range, its END line is present and counts match, and no shortening marker appears; **D1-V16** each changed file's `file_version` is one higher than in the previous snapshot, and `manifest.json` agrees.

## 10. Worked example: *The Catch*, session by session on claude.ai Pro

### 10.1 Session 0: setup (20 minutes)

Do the clicks in §5.2 and the smoke test in §5.3. Paste these project instructions:

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

### 10.2 Session 1: intake and checkpoint A (30 minutes)

Attach `The_Catch_-_workshop_revision_of_Final4.txt`. Say:

> Session S01. Run stage 0 on the attached screenplay with scripts/normalize_fountain.py. Show the change log, the scene list with IDs and line ranges, and every odd line: title cards, transitions, and headings with brackets. Stop at checkpoint A.

Check against C5 E1: 30 scenes; SC06 `INT. FREIGHT CAGE - CONTINUOUS` at 198–299; SC15 at 838–867 "(ON THE TABLET)"; `= THE CATCH` (l.488) a card; `> CUT TO BLACK.` (l.486, l.1848); `= THE END` (l.1852). If the count differs: "List every line you treated as a heading and every heading you skipped." Then:

> approved. Lock the scene IDs, write manifest.json with resume_point stage 1, and give me the ZIP.

Download `CATCH_S01_<date>_intake.zip`, unzip into `CATCH/`, upload `source.fountain` and `scenes_index.json` to project knowledge.

### 10.3 Session 2: story analysis, bible and checkpoint B (60–90 minutes)

Attach `manifest.json`, `source.fountain`, `scenes_index.json`. Choose Opus 5.5.

> Session S02. Run validate.py and tell me the resume_point. Then run stage 1 (story analysis) on the whole script and save story_analysis.json. Show me a one-page plain summary.

> Run stage 2, part 1: characters only, each with aliases, design thesis and identity key.

> Run stage 2, part 2: locations, props, look keys and world rules.

Checkpoint B (15–30 minutes): read each character's thesis and identity key. To correct one: "Revise only CH-IONA: [one sentence]." Then:

> approved: lock every character record. Update manifest.json and give me the ZIP.

Update project knowledge. If usage passes 80% before part 2, save part 1 and stop; the resume point reads "stage 2, part 2".

### 10.4 Session 3: ledger (45 minutes)

> Session S03. Run stage 3 (ledger) in three parts: SC01–SC10, SC11–SC20, SC21–SC30. Each change cites its cause line. Run validate.py after each part.

Check C5 E2's hard rows: `PR-PUCK.S02` from l.224 ("His other hand goes underneath. Behind Jude's back. Out of sight."); `.S03` from l.259 ("A hard metal CLACK."), described as "burnt into the grid" only at l.1219 in SC21; the first handedness change is at l.259, and Iona's second turn at SC27 l.1563 ("She fires.") returns her to original (C5 E2, an inference).

### 10.5 Sessions 4–9: one sequence each

Sequence boundaries come from `story_analysis.json`; a likely split by the headings is [J]: S04 SC01–SC07 (lines 10–332, the escape); S05 SC08–SC10 (333–489); S06 SC11–SC16 (490–911); S07 SC17–SC18 (912–1097); S08 SC19–SC26 (1098–1554, the ship); S09 SC27–SC30 (1555–1852).

Session S04 opening (attach `manifest.json`, `bible.json`, `ledger.json`, `story_analysis.json`, `scenes_index.json`, `source.fountain`):

> Session S04. Run validate.py and tell me the resume_point. Then, for SC01 to SC07 one scene at a time: build the context pack, run stage 4 (beats), then stage 5a (the one-line shot list). Stop after each list for my approval.

For SC06, after reading the one-line list (about 36 lines) at checkpoint C:

> approved SC06 list. Expand part 1: SC06-SH010 to SC06-SH180 with their cut records, then the END line. Run validate.py.

> Expand part 2: SC06-SH190 to SC06-SH360, then the END line. Merge both parts into scenes/SC06.json, run validate.py, and show the report.

Check by eye that SH140 matches C5 E3 (withhold Eli's right hand and `PR-PUCK.S02`, l.242–244) and that "A hard metal CLACK." (l.259) and "BLACK. A dark with nothing in it. One instant." (l.261) follow the hard cut. If the session ends after SC06, the next opens with the §6.1 resume message. Session S10: "Run stage 9: shot_list.csv, elements.csv, animatic.otio, breakdown.md, and give me the ZIP."

### 10.6 The same plan on ChatGPT Plus and on Gemini AI Pro

| Step | ChatGPT Plus: what breaks | Workaround | Gemini AI Pro: what breaks | Workaround |
|---|---|---|---|---|
| Install the skill | No skill upload on Plus [V-sec S22]; custom GPTs retiring [V-sec S24] | Project instructions: short `SKILL.md`; project files: `pipeline_rules.md` (stage files joined), `schema.json`, `scripts.zip` | No upload [U] | Notebook sources: the same three files (Notebook instructions: the short `SKILL.md`) |
| Project files | 25-file cap [V-sec S17] | Film-level files only; attach scene files | 10 files per prompt [V S32] | One `pack_SCxx.md` per scene |
| Python | Runs, no internet [V-sec S19] | Standard-library scripts; "unzip scripts.zip and use it" | No sandbox [U] | Export to Colab [V-sec S33], claude.ai Free, or §6.3 |
| Downloads | Links expire [V-sec S28] | Download after every scene | No JSON or ZIP [V S34] | Canvas code document saved as .txt, renamed .json |
| Whole script (stage 1) | Instant 54K, Thinking 256K [V-sec S47] | Choose Thinking; smoke test step 2 | 1M [V S30] | none needed |
| Memory | Project memory [V-sec S17] | Off or ignore (rule 10) | Personal context [U] | Keep Activity off; folder |
| Connectors | Developer mode, web only [V S20] | As C1 P1 | None; Spark's MCP is AI Ultra and "arriving" [V-sec S43] | Generate via Claude or ChatGPT |

## 11. Worked example: *The Long Places* chapter I in one session

**Plan** (claude.ai Pro, Opus 5.5, about 2 hours) [J]. Stage 0: split lines 5–83 into numbered paragraphs and A3 Ex5's ten candidate scenes (letter to the mouth); checkpoint A. Stages 1–3 for chapter I only, with A3 Ex5's whole-book notes as analysis lines (the threshold refrain returns in VI, XI and XIV; item 51, the brother line and the tally wall are plants). Then stages 4–5 per scene, each with its own context pack. Chapter I scenes should stay under 18 shots each [J]; a longer one is split by §2.4.

**Open problem found here** [J]: C5 scene IDs have two digits (`SC01`–`SC99`). Ten candidate scenes in chapter I suggest over 100 scenes in 14 chapters, so a prose project needs `SC001` or a chapter prefix. The example uses `SC10` for chapter I's tenth scene.

**The context pack for scene 10, as pasted** (the bible and ledger entries are illustrative drafts awaiting checkpoint B):

```
=== STAGE 5a INSTRUCTIONS (read first) ===
Project LONGPL. Run stage 5a (one-line shot list) for ONE scene: SC10.
Use only the material below. One line per shot: ID | size | beat | subject | action | source line.
IDs SC10-SH010 upward in steps of 10. Every shot cites its source line.
Records with "locked": "yes" are read-only. Enums lowercase snake_case; empty = "none".
End with: END SC10 LIST | <n> SHOTS

=== SOURCE: chapter I, lines 73-81 ===
73 On the last night of June, with the dig to open at dawn, she took a borrowed lamp down to the first door and sat on the threshold to learn the place's breathing, because the ventilation plan would want it.
75 At the mouth of Kırk Oda the air shaft breathed. The breath went out for a long while, mild, carrying stone and cold water and something like the inside of a pocket; then a pause long enough to be mistaken for stillness; then in again, the same length, the same patience — a tide with no sea. Anyone with a watch and an hour to waste could time it, and anyone who timed it came away with the same figure: eighteen minutes, and eighteen again, obedient to nothing anyone had ever identified, keeping its own time the way the sea keeps the moon's.
77 She thought about where the baseline CO₂ readings should be taken, and lost that thought, and sat.
79 The warmth came against her right shoulder the way a cat commits itself: suddenly, entirely, with weight. The lamp stood on her left, on the stone. The village cats administered themselves to warmth wherever it pooled, and were shameless about it. The stone had drunk the sun all day above and was giving it back now like a bank. She did not turn her head. You do not turn your head on a night bus when a stranger's child falls asleep against your arm; you go still, and go careful, and carry the debt of it yourself. The lamp at her left burned small and even. The warmth at her right stayed exactly the weight of a sleeping child.
81 It was homesickness, she decided on the climb up. It kept homesickness's hours and homesickness's appetite. Only it stood on nothing. Homesickness has a floor — the place, the table, the bread. This had the place, the table, the bread, and under them the rooms, and under the rooms the deep air going in and out, in and out, on a tide with no sea — and somewhere in the middle of all that, a warmth leaning its whole weight on her shoulder, and nothing under any of it but the kept dark.

=== BIBLE ENTRIES USED (draft) ===
CH-NILAY  aliases: Nilay, Nilay Arat, Dr. N. Arat. identity_key: woman of forty-four, archaeologist,
  lean field build, dark hair tied back, dusty field shirt and trousers, a wristwatch, no rings.
LOC-KIRKODA-MOUTH  fitted tuff threshold behind the low cemetery wall; the first door.
PR-LAMP-BORROWED  small oil lamp, lit.
WR-NO-FIGURE  show no figure, no shadow, no child at Nilay's right (A3 Ex5).
MO-THRESHOLD  bookend setups recorded here; the refrain returns in chapters VI, XI, XIV.

=== LEDGER ROWS AT SCENE START ===
CH-NILAY.S01  field clothes; sitting on the threshold (from l.73).
PR-LAMP-BORROWED.S01  lit, on the stone at her LEFT (l.79).

=== NEIGHBOURS ===
Previous: SC09's last shot, copied from scenes/SC09.json (village lane).  Next: none (end of chapter I).

=== ANALYSIS LINES FOR THIS SCENE (A3 Ex5) ===
- Frontal locked-off medium; empty space at her right shoulder, a two-shot with one person missing.
- Frontal setup: lamp frame-right, empty space frame-left.
- The breath seen and heard: flame leans out, stands, leans in; watch insert; dissolve for the cycle.
- Cut the closing interpretation (l.81); end on the climb with one look back down.

=== FORMAT EXAMPLE ===
SC10-SH010 | wide | SC10-B01 | CH-NILAY | carries the lamp down to the first door, sits | l.73

=== STAGE 5a INSTRUCTIONS (repeated) ===
One scene only. One line per shot. Cite source lines. End with the END line.
```

About 1,500 tokens: instruction first and repeated last (C5 §6.2); only the entries this scene uses. In the identity key, "forty-four" is computed from the text (eighteen, then "Twenty-six years" away, l.39) and "archaeologist" comes from A3 Ex5; build, hair, clothes, wristwatch and "no rings" are drafting inventions to be approved or replaced at checkpoint B. The location line quotes l.43 ("a fitted tuff threshold behind the low cemetery wall"). After approval the list is expanded in one part, validated and saved as `scenes/SC10.json`; the session closes with `LONGPL_S01_<date>_ch-I.zip`.

## 12. Checklists

**Session start**: last snapshot unzipped in `CATCH/` • new chat in the Project or Notebook • `manifest.json` and the stage's files attached • resume message pasted • validator report read before "go".

**Every part**: END line present • count matches the approved list • no shortening markers • validator (or §6.3) clean • `parts[]` updated.

**Session end**: `manifest.json` updated • ZIP downloaded and unzipped • film-level files replaced, not duplicated, in project knowledge.

**New surface or plan**: §5.3 smoke test • training off • `part_size` set • `surface` and `code_execution` recorded.

**Monthly**: re-check every [V] fact in §3 and §8; re-run SC06, SC13 and SC15 as test scenes (C5 R32).

## 13. Conflicts and open questions

- **Correction to C5 §6.11**: skills now sync between claude.ai and Claude Code when signed in (Claude Code v2.1.273+) [V S7]; C5 said they do not sync.
- **Price drift**: Google AI Plus is $4.99 on the subscriptions page [V S31]; C2 recorded $7.99.
- **Undocumented** [U]: the reply limit in all three apps; ChatGPT's context windows come only from secondary sites (Instant 54K, Thinking 256K on Plus); whether the Gemini app runs Python and how many files a Gem holds; whether claude.ai can add created files to a project; whether `.json` and ZIP files download from claude.ai. The smoke test covers the reply limit, the windows and downloads.
- **Settled in the fact-check**: Claude's sandbox can read project files [V S6]; this file still attaches packs because retrieval mode may show only fragments to the model (rule 1).
- **Model churn during the project**: Haiku 4.5 may retire from 15 Oct 2026 [V S12]; GPT-6 Sol is rolling out in ChatGPT [V-sec S26]; custom GPTs retire 11 Dec 2026 [V-sec S24]. Each forces the C5 R32 re-run of the test scenes.
- Checkpoint C before full records (principle 4) changes C5 P1's order: C5 gates stage 5's output with "one-line shot list per sequence"; this file splits stage 5 into 5a (list, approved per scene in §10.5) and 5b (expansion). The pipeline design should confirm both the timing and per-scene versus per-sequence approval.
- The C5 ID pattern for scenes (`SC` plus two digits) is too small for a novel (§11).
- **Conflict with D14 (intake)**: D14 normalizes prose to `source_paragraphs.md` with block IDs such as `ch08.p027` and keeps the file line as `original_ref`; §11's context pack cites raw file lines (`73`, `l.73`). Once D14's intake runs, the pack should cite block IDs, with file lines only as a cross-check.
- **Conflict with D14 Recipe I5**: D14 says Cowork is "an agent that runs code on your computer"; Anthropic says Cowork's work "runs on Anthropic's servers, in an isolated environment" and only reads and writes local files on desktop [V S10]. Locally installed tools (Tesseract, Blender) need Claude Code, not Cowork.
- **Menu path drift in C1 P1**: C1 writes "Claude settings → Connectors → Add custom connector"; the Help Center now says Customize > Connectors > "+" > "Add custom connector" [V S8].
- **Scene list may change after D2**: D2's Option 3 (a shorter cut) marks SC08 `OMITTED`, `merged_into: SC09`; the session plan in §10.5 follows whatever scene list is locked at checkpoint A, not the raw heading count.

## Sources

All checked 2026-09-27. "Excerpt" = read only through a search-engine excerpt.

- S1 Claude pricing: https://claude.com/pricing
- S2 Claude context windows: https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-plans
- S3 Claude usage and length limits: https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work
- S4 Uploading files to Claude (23 Jul 2026): https://support.claude.com/en/articles/8241126-uploading-files-to-claude
- S5 Claude Projects: https://support.claude.com/en/articles/9517075-what-are-projects
- S6 Create and edit files with Claude (6 Aug 2026): https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude
- S7 Use skills in Claude: https://support.claude.com/en/articles/12512180-use-skills-in-claude
- S8 Custom connectors (11 Aug 2026): https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp
- S9 Claude Code on Pro or Max (19 Aug 2026): https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan
- S10 Claude Cowork: https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork
- S11 Usage limit best practices (read in full in the fact-check): https://support.claude.com/en/articles/9797557-usage-limit-best-practices ; excerpt: https://support.claude.com/en/articles/8325606-what-is-the-pro-plan
- S12 Claude models overview: https://platform.claude.com/docs/en/about-claude/models/overview
- S13 Claude data retention (1 Jul 2026): https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data
- S14 Claude model-improvement setting (3 Aug 2026): https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings
- S15 Anthropic consumer terms update, excerpt: https://www.anthropic.com/news/updates-to-our-consumer-terms
- S16 OpenAI file uploads FAQ, excerpt: https://help.openai.com/en/articles/8555545-file-uploads-faq
- S17 Projects in ChatGPT, excerpt: https://help.openai.com/en/articles/10169521-projects-in-chatgpt
- S18 GPT-5.6 in ChatGPT, excerpts: https://help.openai.com/en/articles/20001354-gpt-56-and-gpt-6-pro-in-chatgpt
- S19 Data analysis with ChatGPT, excerpt: https://help.openai.com/en/articles/8437071-data-analysis-with-chatgpt
- S20 ChatGPT developer mode: https://developers.openai.com/api/docs/guides/developer-mode
- S21 ChatGPT data controls, excerpt: https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt
- S22 Skills in ChatGPT, excerpt: https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- S23 Build skills (ChatGPT Learn): https://learn.chatgpt.com/docs/build-skills
- S24 Creating GPTs, excerpt: https://help.openai.com/en/articles/8554397-creating-and-editing-gpts ; Custom GPT retirement and migration FAQ (announced 11 Sep 2026; creation ends 26 Oct, retirement 11 Dec 2026), excerpt: https://help.openai.com/en/articles/20001519-custom-gpt-retirement-and-migration-faq
- S25 GPT-5.6 Sol model page: https://developers.openai.com/api/docs/models/gpt-5.6-sol
- S26 TechCrunch, GPT-6 Sol and Luna (22 Sep 2026): https://techcrunch.com/2026/09/22/openai-launches-gpt-6-sol-and-luna/
- S27 ChatGPT Work and Codex, excerpt: https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
- S28 Sandbox file expiry, community reports: https://community.openai.com/t/preventing-file-expiration-in-chatgpt-sandbox-ttl-workaround/1247404 ; https://community.openai.com/t/chatgpt-cannot-download-generated-zip-artifacts-mnt-data-download-failure/1376287
- S29 ChatGPT plans compared (secondary): https://theaicareerlab.com/blog/chatgpt-pricing-plans-explained
- S30 Gemini Apps limits: https://support.google.com/gemini/answer/16275805
- S31 Google AI subscriptions: https://gemini.google/subscriptions/
- S32 Gemini file uploads: https://support.google.com/gemini/answer/14903178
- S33 Gemini Canvas, excerpt: https://support.google.com/gemini/answer/16047321
- S34 Gemini file generation (29 Apr 2026): https://blog.google/innovation-and-ai/products/gemini-app/generate-files-in-gemini/
- S35 Notebooks in Gemini (8 Apr 2026): https://blog.google/innovation-and-ai/products/gemini-app/notebooks-gemini-notebooklm/
- S36 Gemini Apps Privacy Hub (24 Sep 2026): https://support.google.com/gemini/answer/13594961
- S37 Gemini 3.1 Pro Preview: https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview
- S38 Gemini API pricing: https://ai.google.dev/gemini-api/docs/pricing
- S39 Gemini API terms (last modified 28 Apr 2026): https://ai.google.dev/gemini-api/terms
- S40 Gemini Notebook limits: https://support.google.com/notebooklm/answer/16213268
- S41 Gemini Notebook privacy: https://support.google.com/gemininotebook/answer/17004255
- S42 NotebookLM renamed, excerpt: https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/
- S43 MacRumors, Gemini Spark on Mac (1 Jul 2026): https://www.macrumors.com/2026/07/01/google-gemini-spark-comes-to-mac/
- S44 Own counts, tiktoken 0.14.0 (`o200k_base`; `cl100k_base` gives 12,589 and 61,457): https://github.com/openai/tiktoken
- S45 Gemini 3.8 Flash: https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash
- S46 Use Gems, excerpt: https://support.google.com/gemini/answer/15146780
- S47 ChatGPT context windows by plan (secondary, updated 15 Sep 2026): https://www.ai-toolbox.co/chatgpt-models/chatgpt-context-window-token-limits-2026
- S48 AI usage limits compared (secondary, updated 22 Sep 2026): https://theaicareerlab.com/blog/ai-usage-limits-compared-2026
- S49 GPT-6 Sol model page: https://developers.openai.com/api/docs/models/gpt-6-sol
- S50 ChatGPT Canvas export formats (secondary, 9 Aug 2026): https://www.itechguides.com/openais-chatgpt-breaks-out-of-its-box-and-onto-a-canvas/
- Library: C5, C2, C1, C4, A2, A3, A4 (sections as cited).
