# C5. What already exists: script-to-video research systems, industry breakdown formats, and how to make an LLM pipeline reliable (as of 27 September 2026)

> **What this file is for**
> 1. It surveys research systems (2023 to September 2026) and commercial platforms that turn scripts or stories into shots, and extracts what worked and what failed.
> 2. It lists the industry formats a breakdown should import from and export to (Fountain, Final Draft, breakdown sheets, shot lists, EDL, OpenTimelineIO, production trackers).
> 3. It gives engineering rules for running a long, multi-stage LLM pipeline without drift or contradiction, and explains how to package it as an Agent Skill.
> 4. It applies all of this to four hard moments of *The Catch*.
> 5. It ends with the recommended data model (entities, fields, IDs) for the breakdown.

---

## 0. How to read this file

**Evidence labels.** **[V]** = a current fact I verified at the numbered source on 2026-09-27. **[V-sec]** = verified only at a secondary source (a review site, a blog, a paper that cites the product). **[U]** = I could not verify it. **[J]** = my own judgment. "Via C1" or "via C2" means that sibling file verified the fact the same day; I did not re-open the page. An adversarial fact-check pass on the same day re-opened most sources; its corrections are listed at the end of Section 12.

**Who reads what.** The non-technical user needs Sections 4, 7 and 9. The LLM running the pipeline needs everything, especially Sections 5, 6 and 10. A3 covers breakdown sheets, shot lists, lined scripts and scene numbering in depth; C1–C4 cover video models, image tools, prompting and Blender previs. This file treats those as data and tells the pipeline how to hand work to them.

### Words this file uses (one word per concept)

| Term | Plain definition |
|---|---|
| **Source** | The screenplay or prose story being adapted. |
| **Breakdown** | The pipeline's main output: files that say, scene by scene and shot by shot, what the audience sees and hears and why. |
| **Record** | One entry in the breakdown (one scene, one shot, one character, one job). |
| **Stage** | One step of the pipeline: it reads named files and writes one named file. |
| **Gate** | A check that must pass before the next stage. A **validator** gate is a program; a **checkpoint** is a gate where the human decides. |
| **Validator** | A small program that reads the breakdown files and prints every rule they break, record by record. |
| **Intermediate representation** | The in-between plan a system writes between the story and the pictures ("script, then scene list, then shot list, then prompts"). |
| **Bible** | The file of fixed facts every stage reads and none may contradict: characters, locations, props, looks, world rules. The data model calls it the *visual bible*. |
| **State** | The condition of a changeable element at one moment (a sleeve whole or torn; a flask with or without its puck). |
| **State ledger** (short: **ledger**) | The table of every changeable element's state in every scene. A3 calls it the continuity bible; papers call it a world state. |
| **Handedness** | Which way round something is: *original*, or mirror-reversed (*turned*, the word *The Catch* uses). |
| **Beat** | One action plus the reaction it provokes (A2). |
| **Plant / payoff** | A detail placed early (plant) that matters later (payoff). |
| **Identity key / look key** | Fixed blocks of words pasted unchanged into every prompt: 25–40 words describing a character (B5), or the light, colour and texture of the film or a sequence (C3). |
| **ID** | A short, fixed label that names one record and is never reused, e.g. `SC06-SH140`. |
| **Cross-reference** | A field that holds another record's ID instead of repeating its content. |
| **Schema** | A machine-readable list of the fields a record must have and each field's type. **JSON Schema** is the standard way to write one. |
| **Structured output** | An API feature that forces the model's reply to match a schema. |
| **Chunk** | A piece of the source small enough for one LLM call (usually one scene). |
| **Context / context pack** | Everything an LLM is given in one call / the exact files and excerpts we choose to give it. |
| **JSON, YAML, CSV** | Plain-text file formats: JSON and YAML hold structured records (names and values); CSV holds a table a spreadsheet can open. |
| **Hash** | A short fingerprint of a file's contents; it changes whenever the file changes. |
| **API / MCP connector** | A web address a program sends requests to and pays per use / a plug-in that lets an LLM app call a tool directly (C1). |
| **MLLM** | A multimodal LLM: one that reads images (and sometimes video) as well as text. |
| **Embedding** | A list of numbers a model uses internally to represent a face, a word or an image. |
| **Drift** | An unintended, gradual change in a character's look or a story fact across shots or stages. |
| **Generator** | Any image or video model, as opposed to the LLM that writes the breakdown. |
| **Shot / clip / take** | As in C1: one continuous camera view in the film / one file a model returns / one clip made for a specific shot. |
| **Storyboard frame** | A still picture made to plan a shot. |
| **Keyframe** | A still picture fed to a video model as a start, end or pinned frame (C1, C2). |
| **Reference image** | A picture given to a model so a character, prop or place keeps its look. Papers call a stored one an "anchor". |
| **Generation job** | One request to an image or video model: inputs, settings, cost, result. It is the AI-era camera report line. |
| **Previs job** | One Blender render made from a plan file (C4). |
| **Fountain** | A plain-text screenplay format: headings, action, names and dialogue as ordinary text with a few markup rules. |
| **FDX** | Final Draft's own screenplay file format. |
| **EDL** | Edit decision list: a plain-text list of clips with in and out timecodes; CMX 3600 is the common old dialect. |
| **OpenTimelineIO (OTIO)** | An open, JSON-text file format for an edit timeline: clips, tracks, gaps, transitions, markers. |
| **Agent Skill** | A folder with a `SKILL.md` instruction file plus optional reference files and scripts that an LLM loads when a task needs it. |
| **Handles** | Extra seconds generated before and after the part of a clip the edit will use, so cuts can be adjusted later. |
| **Greybox** | A plain grey 3D render of a planned shot (shapes and camera only, no textures), used as a control input so a generator keeps the planned framing (C4). |
| **Enum** | A field that may hold only one of a fixed list of words, e.g. `hard`, `dissolve`, `wipe`. |
| **Field authority** | Who may write a field: *extracted* from the source (with a line reference), *authored* as a creative decision, or *derived* by a script. |

---

## 1. Landscape

### 1A. Research systems that turn scripts or stories into films or storyboards

"IR" = intermediate representation. All cells [V] from the paper cited; the lessons drawn are in Section 2. Metric names (CLIP, FVD, VBench) are automatic scores of text-picture match, video realism and general quality.

| System (date, venue) | IR: what it writes between story and pictures | How it keeps characters consistent | What it reported failing | How it was evaluated |
|---|---|---|---|---|
| **DirecT2V** (May 2023) [S9] | One prompt → one self-contained description per frame that must "account for all objects and their properties" | Shared attention inside the image model | LLM text not always "vision-friendly"; counting and placement errors | CLIP similarity; user preference |
| **VideoDirectorGPT** (Sep 2023; COLM 2024) [S4] | "Video plan": scene descriptions, entities with per-frame boxes, background, consistency groupings such as `{chef:[1,2,3,4]}` | Same entity embedding across a group's scenes | Planning rated 4.52–4.92 of 5, final video 3.61: the loss is at generation | Layout and motion accuracy; per-stage error analysis |
| **Vlogger** (Jan 2024; CVPR 2024) [S13] | Script drafted Rough → Detailed → Completed (checks missing parts, transitions) → Scheduled (duration per scene); actor list | Actor reference images fed to the video model | Not itemised | FVD, CLIP; clips over 5 minutes |
| **Mora** (Mar 2024) [S12] | Fixed chain: prompt → image → edit → video → connecting video | Humans review each stage; MLLM picks among candidates | About 12 s outputs; weak joins | VBench; removing the human step lowered quality |
| **StoryDiffusion** (May 2024; NeurIPS 2024) [S11] | A batch of panel prompts | Attention shared across one batch of images | Fine details drift; long sequences hard | Character similarity; user study |
| **MovieLLM**, renamed **DreamFrame** (Mar 2024; ACM MM 2025) [S23] | Overview → chapters → sub-chapters → frames ("story expansion") | Learned style token; characters written as look-alikes of named celebrities | Removing story expansion cut CLIP score by about 0.14 | Video-QA benchmarks |
| **MovieDreamer** (Jul 2024; ICLR 2025) [S6] | "Multimodal script" per keyframe: characters (text plus face embedding), scene elements, plot | Face embeddings; first frame kept as anchor | Chaining from each clip's last frame degraded quality; crowded frames mixed identities | Short- and long-term character consistency |
| **Anim-Director** (Aug 2024; SIGGRAPH Asia) [S3] | Character and setting lists, then `[All Characters Included][Setting Included]: description`, then a pass that flags any name not on the lists | Character and setting images first; GPT-4V picks the best of 4 and repairs regions | Short, simple stories only | CLIP text-image and image-image |
| **DreamFactory** (Aug 2024) [S5] | Phase documents: style, script, scenes, shots, character and background databases | A "Base Description" from the first keyframe passed into every later one; a Monitor reviews each | "Controlling details of characters proves most challenging" | Cross-scene face and style consistency |
| **StoryAgent** (Nov 2024) [S7] | Shot list: characters and actions, their regions in frame, background, shot size, motion | Subject redrawn into each frame; small per-subject add-on model | Gemini and GPT-4o judges did not rank real footage above generated | FVD etc.; 14-person user study |
| **MovieBench** (Nov 2024; CVPR 2025) [S16] | Movie (synopsis, character bank with reference images and voice samples) → scene → shot (characters, plot, background, camera motion, style, timed dialogue) | Benchmark, not a generator | GPT-4o annotations still hallucinated; two annotators spent about a week correcting the test set | Character-ID precision, recall, F1 per shot |
| **VideoGen-of-Thought** (Dec 2024; v3 Oct 2025) [S8] | Shot draft → five fields (character, background, relation, camera pose, lighting); a rule rejects any shot missing one | One reference image ("portrait") per character state ("Young Mary", "Elderly Mary") | Without the story step: "identical camera angles and repetitive scenes" | Within- and cross-shot face and style |
| **FilmAgent** (Jan 2025) [S1] | Per dialogue line, JSON: position, action (1 of 21), camera (1 of 272 presets), rendered in Unity | Fixed 3D assets | "A single line of script may involve multiple character actions and camera transitions"; no visual feedback | Human 1–5, average 3.98; a GPT-4o team beat single-agent o1 |
| **CineMaster** (Feb 2025) [S10] | User places 3D boxes and a camera path; preview render | 3D layout control | Object orientation not controllable | Layout and trajectory error |
| **MovieAgent** (Mar 2025) [S2] | Synopsis → sub-scripts (each split justified) → scenes (tone, style, props, camera notes) → shots (size, move, timed subtitle) | Character bank (reference images, voice samples) | Small figures lose identity; walking while talking fails; abrupt joins ("charging" then "defending") | VBench plus human 1–5 rubrics |
| **Captain Cinema** (Jul 2025) [S14] | Keyframe text-image pairs with fixed `<character name>` tags, then video between keyframes | Earlier frames retrieved by content, not only recency | Needs its story text from a human or LLM | Long-context stress test (8 to 48 pairs) |
| **HoloCine** (Oct 2025; CVPR 2026) [S15] | Global scene prompt plus per-shot prompts split by `[shot cut]` | All shots of a scene generated together | "An empty glass remaining empty after water is poured"; Vidu and Kling 2.5 Turbo often returned one continuous shot | Shot-cut accuracy; consistency |
| **CANVAS** (Apr 2026) [S20] | Before any image, a continuity plan: character appearance state, location ID and object state for every shot | Stored reference per character state and per location; 3 candidates scored by questions drawn from the plan | Without location grouping, background continuity fell 50–57%; without character references, face and clothing similarity fell 38–39.5% | ContinuityEval; human win rates up to 90.9% |
| **Co-Director** (Apr 2026, Google) [S19] | Brief → storyline → assets → storyboard (scene descriptors, camera, timing, entity-present flags, audio) → first-frame keyframes → Veo 3.1 | One global "creative configuration" injected into every sub-agent; an MLLM reviews the whole keyframe sequence | Names "cascading failures" and the "credit assignment problem" | 400 **advertising** scenarios (4 shots, 12 s each), so transfer to drama is [J]; MLLM judge vs humans α 0.47–0.59; 81.4 vs 63.6 for Veo 3.1 alone; removing the whole-sequence keyframe review cost 9.8 points of asset fidelity |
| **FilmWorld** (Jul 2026) [S18] | Novel → chapters → scenes with inferred light, season, weather → entity states with IDs (character: identity, age, costume; location: place, season, weather, time; prop: condition) → shot directives with an **end state** | Reference made at each state's first appearance and reused; each shot opens from the previous end state; verifier up to 3 rounds | Remaining errors come from the generators; upstream errors propagate | 15 novels (1,000–3,000 English words each, planned as 20–50 scenes and 50–300 shots of 1–15 s); human ranking equalled automatic (Spearman 1.0); without the world state, character consistency fell 82.12 → 54.50; dropping only the written end state cost 5.65 points, dropping only the visual keyframe hurt other measures: both are needed |
| **CineForge** (Aug 2026) [S17] | Typed production state (episode, scene, shot, character, spatial, cinematic fields); character and scene ledgers (identity, position, gaze, references, transitions) | Deterministic (same result every time) checks of schema, IDs, coverage of every story event, state consistency, durations, model limits; a log of every decision | Traces a bad clip to "the earliest evidence-supported causal stage" | CineScope (causal state, directorial orchestration, pacing, character arc): 4.02 → 4.38; identifiers, schemas and normalizers are fixed by code ("deterministic scaffold") while LLMs fill only bounded creative fields ("creative infill") |
| **CineCrew** (Sep 2026, UMass/MIT) [S62] | "FilmDSL", one JSON: global meta (fps, aspect, tone, era, cast) + asset references + memory + a clip list; each clip has three layers: narrative action (action, emotion, dialogue) → cinematic staging (shot type, move, lighting, `character_refs`, `set_ref`, `required_props`, `forbidden_props`, `continuity_link`) → render spec (keyframe prompt, video prompt, negative prompt, duration, fps, seed) | Character sheets and set assets stored by ID, never re-described; a "Persona Schema" maps traits to visible behaviour, plus per-shot performance blocks; last-frame-to-first-frame chaining only where clips form one continuous take | Identity drift, props duplicating or "teleporting", layout resets, camera mismatch (caught by a "Dailies Reviewer") | 20 MovieBench stories; beat MovieAgent, AniMaker and **LTX Studio**; removing FilmDSL was the largest single loss (beat readability 4.90 → 3.05 of 5) |
| **PACE** (Sep 2026, Studio π) [S63] | Typed fields inherited script → scene → shot → panel ("a value is written once at the level it belongs to"); every field is *extracted* (from the screenplay, with a quotation), *authored* (a directing decision the script leaves open) or *derived* (computed); compiled into both a prompt and a metric 3D scene with a solved camera | Registries of characters, props and locations; shared staging across setups | Framing written in the director's own words came back with heads 1.906× the staged size (1.733× from a compiled prompt, 0.955× with a greybox control render); the greybox held framing but drew the action less (declaring the pose raised action delivery 58.9% → 74.4%); an LLM coverage scorer rated a breakdown 0.95 but re-attached a deliberately deleted event instead of reporting it missing | Measured geometry, not a judge: one subject lands within 1.2% of frame width of its declared position; 204 external director-storyboard shots |
| **DramaChain Bench** (Sep 2026, Tencent with Beijing Film Academy) [S64] | Scores every stage of script → storyboard → keyframe → shot video → episode → short drama on the stage's own upstream output | Benchmark, not a generator | Upstream defects cascade and are "re-expressed downstream, not repaired"; storyboards were weakest on shooting rhythm (2.74 of 5) and restraint in additions (3.34); the best chain (GPT-5.5 → GPT-Image-2 → Seedance 2.0) finished at 3.30, just above the 3.0 usable line | 5,785 items, 3 professional annotators each, every deduction localised; automated judge PLCC 0.918 with human ranking |

Also found on alphaXiv, not read [V titles and dates]: VideoGen-Agent (21 Sep 2026), WanPE cinematic prompt enhancement (24 Sep 2026), CamPilot (10 Sep 2026), Temporal Context Routing for script-driven audio-video (2 Sep 2026), FRAMEWORKERS (30 Aug 2026), SEAM shot entity-attribute memory (24 Aug 2026), SAGE self-evolving storyboard rules (18 Aug 2026), PersonaShot (17 Aug 2026), CineWeaver (29 Jul 2026), ShotPlan (20 Jul 2026), CineAGI and Camera Artist (Apr 2026), InfinityStory (Mar 2026). Baselines ViMax (arXiv 2606.07649), AniMaker and VideoClaw appear in FilmWorld's and CineForge's comparison tables but were not read [U].

**Three 2026 benchmarks that change tool choice** [V]:
- **CutCraft** (8 Sep 2026) [S21]: transitions degrade as shots per request rise (MiniMax H3: 0.542 at 2 shots, 0.383 at 5–6); dissolves and wipes "collapse into hard cuts"; J-cuts and L-cuts (sound leading or trailing the picture) mostly fail. An agent that generated each shot separately "with additional temporal headroom" and did transitions and audio in an edit timeline lifted Wan 2.7 from 0.498 to 0.623. Image quality correlated only weakly with edit execution (Spearman 0.32–0.49). Two costs of the per-shot approach [V]: it did *worse* on transitions that need cross-shot spatial continuity (match cuts, occlusion wipes), and audio-visual synchronisation fell for all three models it was applied to (Wan 2.7 0.436 → 0.277, HappyHorse 1.1 0.673 → 0.479, LTX-2.3 0.667 → 0.477).
- **FilmBench** (27–29 Jul 2026; Alibaba with the Beijing Film Academy and the Hujing film studio) [S22]: 1,169 prompts reverse-engineered from award-winning film clips, written as shot lists with slotted tags (`@scene1`, `@role1`, `@prop1`); multi-shot prompts scored 7.9 points lower on average (up to 22.8, Hailuo 2.3); every model was weakest on action performance, camera-work appeal, motion realism and emotional performance; "no model wins on all" sub-skills (Seedance 2.0 led overall at 88.93 but won only 18 of 35); action scenes lowered every model, with camera movement the worst-hit sub-skill (−31.1 on average).
- **DramaChain Bench** (1 Sep 2026) [S64]: see the table; its lesson for us is that a storyboard's duration budgeting "follows quantitative arithmetic rules and can be verified before any visual rendering", which makes it the one stage whose main defect can be caught in pre-production.

### 1B. Industry formats and software (import sources and export targets)

| Format or tool | What it is | Our use | LLM-drivable? |
|---|---|---|---|
| **Fountain 1.1** (14 Mar 2014) [S24] | Plain-text screenplay markup. Headings start `INT`/`EXT`/`EST`/`INT./EXT`/`I/E` with a blank line before and after, or are forced with a leading period; `@` forces a character; `>` forces a transition; `>TEXT<` is centered text; `#` lines are **sections**, "ignored completely in formatted output"; `=` lines are **synopses**, "ignored in formatted output"; `===` is a page break; scene numbers between hashes (`#1A#`); title page as `Key: value` lines | **Canonical input**; every source is normalized to it | Yes; free. `screenplain` 0.12.0 (28 Apr 2026, Python) converts Fountain to FDX, HTML or PDF [V S66] |
| **FDX** (Final Draft 13; $249.99 to buy, or the Final Draft Suite at $99.99 a year or $16.99 a month, with Final Draft Cloud) [S26] | Final Draft's native file; Fountain's site offers the same script as `.fountain`, `.pdf` and `.fdx` [S25] | Import by converting to Fountain; export back to FDX (via `screenplain`) when a scheduler needs it | Partly; XML text [U: no official spec found] |
| **PDF script** | Printed layout | Import only; extract, then normalize | Yes, but indentation (which carries meaning) is lost |
| **Breakdown categories** [S27][S28] | Cast red; stunts orange; silent extras yellow; atmosphere extras green; special effects blue; props purple; vehicles and animals pink; sound or music brown; wardrobe a circle; make-up and hair an asterisk; special equipment a box; notes underlined. StudioBinder uses the same red, yellow, blue and purple and allows custom categories | Element categories in the bible (full sheet: A3 §5.3) | Yes |
| **Shot list** [S29] | Scene number; shot number or letter ("1A, 1B"); description; size; angle; equipment; movement; lens; frame rate; cast; notes | CSV export of shot records | Yes |
| **Camera report** [S30] | Per take: lens, filters, take, f- or T-stop, ISO, file number [V]. Other columns commonly printed on report sheets: roll or card, scene/slate, take, circled ("print") or NG, frame rate, shutter, white balance, notes [J: common practice; no single primary source found] | Becomes the generation job log: take number, kept/rejected (= circled/NG), model and settings in place of lens and stop | Yes |
| **Slate and setup naming** [S74][S75] | American slates show scene, setup letter and take (e.g. 24C, take 3); European slates number every setup consecutively. Letters that read like digits are skipped: I and O always, and some crews also skip S, Y or Z [V-sec S74]; letters are spoken as words ("27A" = "twenty-seven apple") | Display labels only (Section 10.1); choose one convention per project and record it | Yes |
| **Lined script** (A3 §5.9) | Lines showing which setup covered which script lines | Becomes a **coverage map**: every source line maps to shots or to an omission | Yes |
| **Movie Magic Scheduling** [S31][S65] | Stripboard, breakdown reports, day-out-of-days, multi-unit boards; one-line reports to Excel (.xlsx) and PDF. **Imports** `.fdx` (sluglines and speaking characters only), `.sex` ("Scheduling Export" from a tagged Final Draft or Movie Magic Screenwriter script, carrying every tagged element and any new categories) or Movie Magic Screenwriter files [V S65] | Target via Fountain → FDX; for full elements, tag in Final Draft and export `.sex`, or use Filmustage's MMS export | No API found [U]; price not published on the page [U] |
| **StudioBinder, Celtx** [S28][S29][S32] | Web breakdown, shot list, storyboard, scheduling, budgeting (Celtx adds a Premiere Pro plug-in and a 7-day trial) | Paste CSV by hand | No public API found [U] |
| **Filmustage** [S33][S67] | AI breakdown (cast, props, locations, VFX, wardrobe), schedules, budgets; imports PDF, FDX, Fountain; exports PDF, Excel, MMS and MMB (Movie Magic Scheduling and Budgeting); "We do not use your data for training". Free plan: AI breakdown of 20% of scenes, one project; "Director's Cut" from $55 a month billed yearly ($660) or $79 monthly | Cross-check of our element extraction; bridge to Movie Magic | No API found [U] |
| **Toon Boom Storyboard Pro** (via PACE [S63], citing Toon Boom's online help) | Industry storyboard software: four caption fields per panel by default, no dedicated field for cast, props, location or shot size; one controlled vocabulary, transitions (Cut, Dissolve, three Wipes) | Storyboard frames can be handed to board artists; our records carry what its panels do not | Not checked [U] |
| **Flow Production Tracking** (formerly ShotGrid/Shotgun) [S34] | Tracker of Project, Sequence, Shot, Asset, Task, Version; Python API v3.10.3, "low-level", user or script-key login | Optional team export | Yes, via generated Python |
| **EDL (CMX 3600)** [S35][S38] | "Simple editing decisions only"; reel names 8 characters in Final Cut's version; the OTIO adapter writes one video track, audio, gaps, markers, transitions, in Avid, Premiere or Nucoda style; no multiple video tracks, no nesting | Animatic fallback | Yes |
| **OpenTimelineIO 0.18.1** (9 Nov 2025; still the latest on PyPI on 27 Sep 2026) [S36][S37][S39] | "A modern Edit Decision List (EDL) that also includes an API"; JSON `.otio` references media; `.otioz` and `.otiod` bundle it; Academy Software Foundation. The core package reads and writes only `.otio`/`.otioz`/`.otiod`: the EDL, FCP XML and AAF adapters need **`OpenTimelineIO-Plugins`** (same version) [V S37]. Editors: DaVinci Resolve imports and exports OTIO (since 18.x) [V-sec S73]; Premiere Pro's OTIO import and export left beta ("Now Released") [V S72; version U] | **Preferred timeline export** | Yes: `pip install opentimelineio OpenTimelineIO-Plugins` |

### 1C. Commercial platforms that ingest a script or plan and produce shots

| Platform | In | Out | API / MCP | Cost (verified) |
|---|---|---|---|---|
| **LTX Studio** (Lightricks; ltx.studio now redirects to ltx.io/studio) [S40]–[S43] | "Currently, LTX Studio only supports plain text (.txt) files"; any language, but "results will be translated to English" | Script "divided into scenes and shots"; characters, objects and locations extracted as reusable "Elements"; MP4 storyboards; PDF pitch deck. Models on the plans page: LTX-2.5 and LTX-2.3 (own), FLUX.2, Nano Banana 2/Pro, Kling 2.6/3.0 Pro, Seedance 2.0; Veo 3.1 (all three tiers) on Pro only | Model API ("LTX API") exists; no API for Studio projects found [U] | Free 800 credits once; Lite $15/mo, 8,000 credits (personal use only); Standard $35/mo, 28,000 credits (commercial licence; needed for AI storyboards and saved Elements); Pro $125/mo, 110,000 credits. Yearly billing about 20% less. In CineCrew's test it was the strongest baseline on look and physics but weaker on beat readability and narrative coherence [S62] |
| **Katalist** [S44][S68] | "A written script" (format not stated); an "AI Script Assistant" breaks it down into scenes and characters | Storyboards in 10 styles; "ZIP, Shooting Board, or PDF"; the pricing page adds PPT, video, and Premiere Pro and Final Cut Pro export | "API Access" listed on the Enterprise plan only | 7-day free trial; Essential $19–29/mo (two prices shown), Pro $39/mo, Unlimited $99/mo. Its model list still advertises Sora 2 (API removed 24 Sep 2026, via C1) and a "Veo 3.2" that Google does not list (via C1): treat the list as stale |
| **Higgsfield Popcorn** [S47] | One prompt per scene plus optional references | "Up to 8 images in a single sequence", consistent; the last image can seed the next sequence | Higgsfield MCP connector (via C1) | Free daily credits, then credits; its "One-Click Export to Sora 2" is stale: the Sora 2 API was removed 24 Sep 2026 (via C1, C2) |
| **Showrunner** (Fable Studio) [S45] | "Write a scene, get an episode"; characters by look, voice, personality | Animated episodes published inside Showrunner, where viewers can "branch the canon"; iOS app "coming soon" | None on the page | Not on the page |
| **Luma** [S46] | Ray3.2 video model (released June 2026), UNI-1.1 image model, Luma Agents ("plan, generate, iterate, and refine") in the Luma App; partner models Seedance 2.0, Veo 3.1, Kling 3.0 and Omni, Nano Banana; ElevenLabs sound and music | Clips, images | API (credit-based); MCP not mentioned; "Do not use 'Dream Machine'" (deprecated); Boards absent from current documentation | App plans Plus, Pro, Ultra, Enterprise [V]; prices not on this page |
| **Flora** [S48][S69] | Node canvas, "50+ models", reusable "Techniques" | Images, clips | "API & MCP access" from the Starter plan up | Free $0 (text and image models, up to 17 generations); Starter $18 per seat a month (launch offer through 30 Sep 2026); Pro $50 per seat a month |
| **Runway** (via C1) | Gen-4.5, Aleph 2.0, Act-Two, partner models | Clips; its agent builds Workflows and can assemble clips on a timeline | Official MCP connector, sign-in | Credits ($0.01 each on the API) |
| **Google Flow** (via C1, C2) | Prompts plus "ingredients" (reference images); no script import | Veo 3.1 and Gemini Omni Flash clips; Nano Banana 2 images | No outside-LLM control found [U] | Google AI plan credits |
| **Adobe Firefly** (via C1) | Prompts; Adobe's own Creative Agent (Apr 2026) | Firefly Video plus partner models (Kling 3.0, Veo 3.1, Runway Gen-4.5); Premiere integration | Outside-LLM control not verified [U] | Creative Cloud credits |
| **Boords** (via C2) | Named cast, locations, props `@`-mentioned per frame | Storyboards; PDF, shot list, MP4 animatic | Partly (API, webhooks) | From $39/mo ($26 billed yearly) |
| **M Studio** [S76] | An idea or a script; plans "scenes and numbered shots" | Storyboard frame per shot, clips, voices, score; a timeline exported as MP4, WebM or MOV | "API docs" link on the site; not read [U] | From $27/mo, no free plan (its own buyer's guide also ranks competitors; treat that ranking as marketing) |
| **Storyboarder.ai** [S77] | "Upload your script" | Storyboard, shot list, animatic with audio, pitch deck | None mentioned | Free plan; paid prices not readable [U] |
| **Kaiber Superstudio** [S78] | Node canvas aggregating third-party video models (reviews list Kling, Veo, Runway, Luma, MiniMax); strongest at audio-reactive music visuals | Clips | None found [U] | Reviews report 50 free credits and paid plans from about $29/mo [V-sec S78]; its own site needs JavaScript and could not be read [U] |
| **Chinese short-drama platforms** (OiiOii, Flova, XiaoYunQue, LibTV, as named by DramaChain [S64]) | A story premise | Script → storyboard → keyframes → shot videos → assembled episode | [U] | [U]: not opened |

**The pattern [J]:** every platform that accepts a script keeps its breakdown inside the app. Some export pictures and timelines (Katalist to Premiere Pro and Final Cut Pro, Boords a shot list, M Studio a finished cut), but none found exports its scene-and-shot plan as open, structured data with stable IDs that could be re-imported. Our breakdown is the portable source of truth; platforms are render targets.

---

## 2. What the research teaches: fourteen lessons

The evidence is cited; the wording of each lesson is [J].

1. **Everyone climbs the same ladder: story → scene → shot → prompt.** MovieAgent, MovieBench, Vlogger, DreamFrame and FilmWorld all add levels rather than jump from story to prompts, and DreamFrame's test with the middle levels removed shows the cost [S2][S16][S13][S23][S18]. Our breakdown has five levels: project, scene, beat, shot, job.
2. **Plan at the beat, not the line.** FilmAgent's per-line plan was too coarse for action [S1]. A shot record lists timed beats (C3's `BEATS` field).
3. **An explicit state ledger is the largest consistency win found.** FilmWorld lost 27.6 points of character consistency without it; CANVAS lost half its background continuity without location grouping [S18][S20]; CineForge keeps ledgers and VGoT keeps per-state reference images [S17][S8].
4. **References belong to states.** "Young Mary" and "Elderly Mary" are separate references [S8]; FilmWorld makes one at each state's first appearance [S18]. Iona with a skinned palm is a new state.
5. **Every shot closes with an end state; the next opens from it.** FilmWorld chains them [S18]; MovieAgent's abrupt joins show what happens without it [S2].
6. **Write consequences explicitly.** Generators keep the first state ("an empty glass remaining empty after water is poured") [S15]; the ledger carries cause and effect.
7. **Closed name lists and mechanical checks beat good intentions.** Anim-Director rejects unlisted names [S3]; VGoT rejects shots missing a field [S8]; CineForge validates IDs and coverage in code [S17].
8. **One shared look block, injected everywhere.** Co-Director's "creative configuration" fixed the disjointed look of independent templates [S19]; DreamFactory's Base Description did the same [S5].
9. **Generate one shot per request and cut in the edit.** Multi-shot requests lose 7.9 points on average; transitions and J/L-cuts succeed as edit operations with handles, not inside generators [S22][S21]. Two exceptions to plan for: match cuts and occlusion wipes need both shots built from shared geometry (previs or shared keyframes), and any audio offset must be re-checked for lip sync, because per-shot composition lost audio-visual sync in CutCraft [S21].
10. **Judges need targets, a round limit and a log.** An open "is this good?" judge failed [S7] and self-correction without outside feedback hurt [S50]; reviewing a scene's keyframes as a sequence measurably helped (removing it cost Co-Director 9.8 points of asset fidelity), while plan-derived questions and reference comparisons added smaller gains [S19][S20][S18]; FilmWorld's gain per extra repair round roughly halved each time, CutCraft stopped at 2 rounds and CANVAS's candidate count saturated at 3 [S18][S21][S20]; CineForge's decision log lets you find the first wrong decision, the "credit assignment problem" Co-Director names [S17][S19].
11. **Code owns the skeleton; the LLM fills bounded fields.** CineForge fixes identifiers, schemas and normalizers in code and lets LLMs fill only "bounded semantic fields" [S17]; PACE labels every field *extracted* (from the script, with a quotation), *authored* (a directing decision) or *derived* (computed) [S63]. So: IDs, line ranges, durations and cross-references are written or checked by scripts; the LLM writes purposes, descriptions and choices.
12. **Write a value once, at the level it belongs to, and inherit it.** PACE's scene-level lens is not restated per panel; in one scene a restated location sentence named a console that was never staged, and with that sentence in the prompts the frames shifted far more than without it (53% against 18% on PACE's measure) [S63]. Scene records carry defaults (location state, look, lens package); shots carry only overrides.
13. **Fix defects at the stage that made them.** Upstream defects are "re-expressed downstream, not repaired"; the storyboard stage's weakest points were shot rhythm and invented additions, and duration budgeting can be checked by arithmetic before any picture exists [S64]. CineCrew's largest single loss came from removing its structured intermediate layer [S62].
14. **Words do not hold framing; geometry does, at a price.** Framing written in words came back with heads about 1.9× the intended size, while a greybox control render held it (0.955×) but delivered less of the written action; declaring the pose recovered part of the action (58.9% → 74.4%) [S63]. Previs (C4) is worth its cost for framing-critical shots; for action-critical shots, declare the pose too. And do not let an LLM grade coverage: PACE's scorer quietly re-attached a deleted event [S63]; coverage is computed from cited lines.

---

## 3. Formats in practice

**Input.** Normalize every source to strict Fountain (screenplays) or numbered paragraphs (prose) and store a hash of the original [J]. Fountain is free, human-readable and easy for any LLM to read and write [S24][S25]. Convert FDX and PDF into it rather than analyzing PDFs directly [J].

**The Catch uses a variant that strict Fountain misreads** [V against S24]: headings written `## INT. …` are level-2 sections, "ignored in output", and the `=` title page and mid-film title card are synopses, also ignored. A strict parser finds zero scenes and drops the title card at line 488 and the end card at line 1852. Worked example E1 shows the fix.

**Outputs** [J]: the breakdown's JSON files are the source of truth (Section 10). Generate from them a readable document; a shot list CSV with the StudioBinder columns [S29] plus our IDs; an element CSV by breakdown category [S27]; an animatic as OTIO, which can hold several video tracks, with a CMX 3600 EDL fallback, which holds one [S36][S38]; the normalized script as FDX (via `screenplain` [S66]) for Movie Magic Scheduling, which reads sluglines and speaking characters from FDX [S65]; and, for teams that already use it, Flow Production Tracking records via its Python API [S34]. Industry display names (scene 12A, OMITTED, shot 6B) are generated labels, never IDs (Section 10).

**Which editor opens what** [V S72, V-sec S73; J for the rest]: DaVinci Resolve (free version included) and Premiere Pro import `.otio`; Avid Media Composer takes the CMX 3600 EDL (the adapter's default "avid" style) [S38]; Final Cut Pro takes neither directly [J: it uses FCPXML; OTIO's FCP adapter lives in `OpenTimelineIO-Plugins`].

---

## 4. Which tool for which aim

| Aim | First choice | Alternative | Why [J unless marked] |
|---|---|---|---|
| Write the breakdown | An LLM running this pipeline as an Agent Skill, writing JSON | The same instructions pasted into any chat LLM | Only this yields portable, validated data; Agent Skills are read by Claude, ChatGPT & Codex, Gemini CLI, GitHub Copilot, Cursor and others [V S53] |
| Force valid JSON | Structured outputs with the portable schema (6.4) | Plain JSON plus the validator | Claude, OpenAI and Gemini all enforce a JSON Schema subset [V S57][S58][S59] |
| Check the breakdown | `validate.py` in the skill | LLM checklist review | Deterministic; "only the script's output" enters context [V S54] |
| Cross-check element extraction | Filmustage on the same script [V S33] (free plan covers 20% of scenes; full breakdown from $55/mo [V S67]) | A second pass with another model | Independent misses |
| Quick sketch of the whole script | LTX Studio from a `.txt` export [V S41] (AI storyboards need the $35/mo Standard plan [V S43]) | Katalist (7-day trial) [V S44][S68] | Fast; a sketch, not data |
| Storyboard frames | C2 tools driven by shot records | Boords for presentation (via C2) | Our records hold the consistency data |
| Exact camera and blocking | Blender previs from a plan file (C4) | 3D layout tools like CineMaster [S10]; PACE's open code [S63] | Words describe camera moves and framing loosely: heads came back 1.9× the intended size from words, 0.955× from a greybox [V S63] |
| Video clips | Per-shot model choice (C1, C3), one shot per request | Multi-shot request only for simple dialogue coverage | Multi-shot and transitions degrade [V S21][S22] |
| Transitions, J-cuts, L-cuts | Edit timeline (OTIO) with handles | None | Post-production raised transition scores sharply [V S21] |
| Team tracking | Flow Production Tracking via Python API [V S34] | Shared spreadsheet from CSV | Only if the team already tracks |
| Live-action scheduling | Movie Magic Scheduling from our FDX export (sluglines and speaking roles) plus the element CSV typed in, or Filmustage's MMS export [V S65][S67] | StudioBinder | Industry standard; the `.sex` route (all tagged elements) needs Final Draft's tagger [V S65] |

### 4A. Cost and difficulty at a glance (prices checked 27 Sep 2026; re-check before buying)

| Item | What you pay | Difficulty for a non-technical user [J] | Source |
|---|---|---|---|
| Claude (to run the skill) | Free plan lists Skills; Pro $20/mo ($17/mo billed yearly); Max from $100/mo; Claude Code needs Pro or higher | Easy on claude.ai; medium in Claude Code (a terminal or desktop app) | [V S71][S70] |
| Final Draft 13 (only if a collaborator needs `.fdx` edited) | $249.99 once, or $16.99/mo, or $99.99/yr | Easy | [V S26] |
| Filmustage (cross-check, Movie Magic bridge) | Free for 20% of scenes; $55–79/mo for full AI breakdown | Easy | [V S67] |
| Movie Magic Scheduling | Not published on the product page | Medium (industry training assumed) | [U S31] |
| LTX Studio (sketch, comparison) | Free 800 credits once; $35/mo for commercial use and AI storyboards | Easy | [V S43] |
| OTIO, EDL, `screenplain`, `jsonschema` | Free, open source | Hidden from the user: the LLM runs them | [V S39][S61][S66] |
| DaVinci Resolve (open the animatic) | Free version imports OTIO | Medium | [V-sec S73] |
| Video generation | Per second of clip; see C1 (roughly $0.05 to $0.70 a second across C1's table, before retakes) | Easy per clip; hard to budget without the job log | via C1 |

---

## 5. Decision rules

1. **If** the source is a PDF or FDX, **then** convert it to Fountain and have the human confirm the scene count before stage 1, **because** every ID hangs on the scene list and layout parsing fails silently [J].
2. **If** a screenplay uses non-standard markup (`##` headings, `=` title cards), **then** normalize it with a script and log every change, **because** strict Fountain ignores sections and synopses [V S24].
3. **If** the source is prose, **then** segment chapter → scene → paragraph and resolve aliases and pronouns to character IDs before shot design, **because** FilmWorld's entity resolution and scene structuring precede all planning [V S18].
4. **If** a fact holds for the whole film, **then** store it once in the bible and cross-reference it by ID, **because** restated facts drift [J, supported by S5][S19].
5. **If** anything about an element can change, **then** give it a ledger row from its first change, **because** explicit states are the largest consistency effect found [V S18][S20].
6. **If** a character's look changes (injury, costume, age, handedness), **then** create a new state ID with its own reference image, **because** references work per state [V S8][S18].
7. **If** a shot ends, **then** record its end state, and **if** the next shot is continuous, **then** copy it into that shot's start state, **because** joins break without it [V S2][S18].
8. **If** an action changes an object, **then** write the resulting state into every later shot showing it, **because** generators keep the earlier state [V S15].
9. **If** a model call returns breakdown data, **then** use structured output and still run the validator, **because** a schema guarantees shape, not meaning: a valid ID can point to the wrong character [V S57][J].
10. **If** a check can be code (IDs resolve, coverage, durations, words per second), **then** put it in the validator, not a prompt, **because** scripts are deterministic and cheap in context [V S54][S55].
11. **If** a check needs judgment, **then** ask yes/no questions derived from the records ("Is Iona's hand bandaged in this frame?"), **because** CANVAS scores candidates this way, while an open-ended judge in StoryAgent could not even rank real footage above generated [V S20][S7].
12. **If** you want to say "review and improve your answer", **then** instead put every requirement in the first instruction and run the validator, **because** intrinsic self-correction lowered accuracy and apparent gains came from weak first prompts [V S50].
13. **If** a repair loop fails 3 times, **then** stop and show the human, **because** FilmWorld's gain per round roughly halved each time and CutCraft stopped at 2 rounds [V S18][S21].
14. **If** you want options for a creative choice, **then** generate 2–3 independent versions and let the human pick, **because** equal-cost voting beat multi-agent debate [V S50] and taste is the human's call [J].
15. **If** a sequence has several shots, **then** generate one shot per request with 0.5–1 s handles and join them in the edit, **because** multi-shot requests lose structure and transitions [V S21][S22] (handle length [J]).
16. **If** a cut is a dissolve, wipe, J-cut or L-cut, **then** mark it on the cut record and do it in the edit, **because** generators collapse them into hard cuts [V S21].
17. **If** a call would need more than one scene's source plus its bible entries, **then** split it, **because** accuracy falls when needed text sits mid-context and as inputs grow [V S49][S51].
18. **If** a stage's inputs are unchanged, **then** skip it; **if** a human locked a record, **then** never overwrite it, **because** re-runs must not undo approved work [J].
19. **If** different LLMs will run the pipeline, **then** keep core instructions free of provider-only features and test with the smallest model, **because** "what works perfectly for Opus might need more detail for Haiku" [V S55].
20. **If** a platform offers in-app "script to video", **then** use it as a sketch or render target, never as the breakdown, **because** none found exports its shot plan as data [J from S41][S44][S45].
21. **If** a description would name a real person ("looks like [actor]"), **then** replace it with a written identity key, **because** that research shortcut [V S23] creates likeness and consent problems [J].
22. **If** a tool fact is over a month old, **then** re-check it before a production run, **because** features vanish (Higgsfield's Sora 2 export and Katalist's Sora 2 listing outlived the Sora 2 API) [V S47][S68; via C1, C2].
23. **If** a field is an ID, a line range, a count, a duration total or a cross-reference, **then** a script writes it or checks it and the LLM never invents it, **because** CineForge fixes identifiers and schemas in code and lets LLMs fill only bounded fields [V S17]; PACE separates extracted, authored and derived fields [V S63].
24. **If** a value holds for a whole scene (location state, lens package, look key, time of day), **then** set it once on the scene record and let every shot inherit it, overriding only on the shot that differs, **because** restated values drift from what is staged [V S63].
25. **If** an LLM reports that "every event is covered", **then** do not accept it: every shot must cite source lines and the validator computes coverage, **because** PACE's LLM scorer re-attached a deliberately deleted event instead of reporting it missing [V S63].
26. **If** a shot's framing carries the story (a reveal, an insert, the playback in scene 13, a precise size of face), **then** stage it in previs and pass the greybox as a control input; **if** its action also matters, **then** declare the pose as well, **because** words alone gave heads about 1.9× the intended size, the greybox held framing but drew less action, and declaring the pose raised action delivery from 58.9% to 74.4% [V S63].
27. **If** a scene's shot list is written, **then** the validator adds up shot durations against the scene's target length and flags any shot with more than one main action or any element not in the source, **because** shot rhythm (2.74 of 5) and restraint in additions (3.34) were the weakest storyboard skills, and duration budgeting can be checked by arithmetic before any picture exists [V S64].
28. **If** a clip is wrong, **then** trace it to the earliest wrong record, fix that record and re-run everything downstream of it; **do not** patch only the prompt, **because** upstream defects are "re-expressed downstream, not repaired" [V S64] and CineForge assigns each defect to its earliest causal stage [V S17].
29. **If** a structured-output field is an enum, **then** use lowercase `snake_case` values that differ by more than capitalization and compare them case-insensitively in the validator, **because** Claude's structured outputs do not guarantee the capitalization of enum values [V S57].
30. **If** a cut is a match cut or an occlusion wipe, **then** build both shots from the same previs geometry or shared keyframes rather than generating them independently, **because** CutCraft's per-shot agent did worse on transitions that need cross-shot spatial continuity [V S21].
31. **If** an audio offset is applied in the edit (J-cut, L-cut, moved dialogue), **then** re-check lip sync on the affected shots before approving, **because** per-shot composition lowered audio-visual sync for every model CutCraft tried it on [V S21].
32. **If** you change a stage instruction or a validator rule, **then** re-run the saved test cases (for *The Catch*: SC06, SC13, SC15) and compare old and new outputs before adopting the change, **because** CineForge admits a rule change only after replay shows no regression [V S17] and Anthropic recommends building evaluations before writing instructions [V S55].
33. **If** a shot must include or must exclude an element (the puck must stay hidden in SC06; the beads must stay in the air), **then** list it in the shot's `required` or `forbidden` elements, **because** CineCrew makes these continuity hooks explicit fields that its reviewer checks [V S62].

---

## 6. Making a long, multi-stage LLM pipeline reliable

### 6.1 The shape: a chain of stages with gates

Anthropic calls this "prompt chaining" with programmatic "gates" and advises adding complexity "only when it demonstrably improves outcomes" [V S60]. The best 2026 results come from chains with explicit state and validators (FilmWorld, CineForge, CANVAS), not from simulated crews chatting (DreamFactory, FilmAgent) [J from S17][S18][S20][S5][S1]. Recommended stages [J]; each writes one file per scene where possible so any scene can be re-run alone:

| Stage | Reads | Writes | Gate after it |
|---|---|---|---|
| 0 Intake | Source | `source.fountain` (or numbered paragraphs), `scenes_index.json` with locked scene IDs and line ranges | Validator; **checkpoint A**: human confirms the scene list |
| 1 Story analysis | Whole source (chapter summaries for a novel) | `story_analysis.json`: events, sequences, spines, plants and payoffs, motifs (A1, A2, B4) | Validator |
| 2 Bible | Source, analysis | `bible.json`: characters with aliases and identity keys, locations, props, looks, world rules (B2, B5) | Validator; **checkpoint B**: design theses and identity keys |
| 3 State ledger | Source, bible | `ledger.json`: state per element per scene, each change tied to a line | Validator |
| 4 Scene design | One scene + context pack | `scenes/SC06.json`: beats, blocking, event, key shot (A2, A3, B3) | Validator |
| 5 Shot design | Scene file + context pack | Shots and cuts in the same file (B1–B3, A4) | Validator; **checkpoint C**: one-line shot list per sequence |
| 6 Storyboard (optional) | Shots, bible | Storyboard frame records and images (C2) | Plan-derived questions; spot-check |
| 7 Previs (optional) | Shots, set plans | Previs jobs, plan files, renders (C4) | **Checkpoint D**: camera and blocking |
| 8 Generation (optional) | Shots, keyframes | Generation jobs and clips (C1, C3) | **Checkpoint E**: keep or reject takes |
| 9 Export | All records | CSV, OTIO, EDL, readable document | Validator |

### 6.2 Chunks and context packs

- **Screenplays:** one scene per chunk [J]; scenes are the production unit (A3) and the natural boundary for state changes.
- **Prose:** segment chapters into scenes first, as FilmWorld does [V S18]; DreamFrame's level-by-level expansion exists "to mitigate context length limitations" [V S23].
- **Why small:** accuracy is highest when the needed facts sit at the start or end of the input and drops in the middle [V S49]; performance "varies significantly as input length changes, even on simple tasks", and "even a single distractor reduces performance" [V S51]. Put the instruction first and repeat it last [J from S49, where placing the query before and after the data made key-value retrieval near-perfect].

**Context pack for one scene's shot design** [J]: the stage instructions; the scene's source text with line numbers; only the bible entries whose IDs the scene uses; the ledger rows for those elements at scene start; the previous scene's last shot and the next scene's heading; the analysis lines for this scene; the schema and one example record.

### 6.3 One source of truth

Fixed facts live in `bible.json`, changing facts in `ledger.json`; shot records hold IDs, never restated descriptions [J; FilmWorld treats its world state as the single source of truth, S18]. Prompts are **compiled, not written**: a script assembles each model prompt from the shot record plus the pasted identity key, state line and look key (C3 §15, B5 §7). Every ledger change cites the source line that causes it, and the validator refuses one without a cause [J; CineForge checks state consistency in code, S17].

### 6.4 Structured outputs and a portable schema

All three major APIs can force schema-matching JSON [V]:
- **Claude** (generally available; the older `output_format` parameter and its beta header are deprecated): `output_config.format` with `json_schema`, or `strict: true` on tools. Supported: `enum`, `const`, `anyOf`/`allOf` (limited), internal `$ref`/`$defs`, string formats (`date-time`, `date`, `uuid`, …) and **simple `pattern` regexes** (no backreferences, lookarounds or `\b`). Not supported: recursive schemas, `minimum`/`maximum`/`multipleOf`, `minLength`/`maxLength`, array limits beyond `minItems` 0 or 1 (so no `uniqueItems`); `additionalProperties` must be `false`. Limits per request: 20 strict tools, **24 optional parameters** and 16 union-typed parameters across all strict schemas, plus a 180-second compile timeout ("Schema is too complex for compilation"). A compiled schema is cached 24 hours from last use. Required properties come out first. Exceptions to "always valid": a refusal (`stop_reason: "refusal"`), a cut-off (`stop_reason: "max_tokens"`), and **enum values whose capitalization may differ** from the schema [S57].
- **OpenAI**: `text.format` with `json_schema` and `strict: true`; every field required, optional ones as a union with null; `additionalProperties: false`; the root must be an object, not `anyOf`; supports `pattern`, `format`, numeric ranges, `minItems`/`maxItems`, `$defs` and recursion; up to 5,000 properties, 10 levels of nesting, 1,000 enum values and 120,000 characters of names and values per schema; keys come out in schema order; refusals arrive in a `refusal` field; a truncated reply is marked `incomplete` with reason `max_output_tokens` [S58].
- **Gemini** (current docs use `response_format` with `mime_type: "application/json"` and a `schema`): types including `null` via type arrays, `required`, `additionalProperties`, `enum`, `format` (date-time, date, time), `minimum`/`maximum`, `items`, `prefixItems`, `minItems`/`maxItems`; the documentation's own examples use `anyOf` and a recursive `$ref: "#"`; "Not all JSON Schema features are supported", "Very large or deeply nested schemas may be rejected", and "always validate values in your application" [S59].

**Portable subset** [J, from those three lists]: objects with every field required and `additionalProperties: false` (which also keeps Claude's 24-optional-parameter limit from biting); strings, integers, numbers, booleans, arrays, string enums in lowercase `snake_case`; nesting at most 3 levels; no recursion, regex, length or range limits (Claude's API returns a 400 error for ranges, its SDKs strip them into the description, and Gemini's docs do not list `pattern`); no `anyOf` unions; write `"none"` instead of `null` (C3 already asks for `none` so a reader sees the field was considered). Send one scene's records per call, not the whole film, so the schema stays small and a cut-off loses one scene at most. Every rule the subset cannot express goes into the validator (jsonschema 4.26.0 or pydantic 2.13.5 are current Python libraries for this [V S61]). Store JSON, not YAML: structured outputs emit JSON, and hand-edited YAML breaks on indentation [J]. Generate Markdown and CSV views for people.

### 6.5 IDs and cross-references

Give each record an ID at birth, never reuse it (rules in 10.1), and store relationships as ID lists (`characters: ["CH-IONA", "CH-ELI"]`), never names. Names vary ("Io", "IONA", "her brother"); IDs do not [J; the reason Anim-Director checks names and FilmWorld resolves aliases, S3][S18].

### 6.6 What the validator checks

It runs after every stage and prints one line per problem, naming record, rule and allowed values; Anthropic recommends messages like "Field 'signature_date' not found. Available fields: …" [V S55]. Minimum checks [J]:
1. Every file matches the schema; every ID is unique, well-formed, and every cross-reference resolves.
2. Every source scene has a record; every source line is covered by a shot or listed as omitted with a reason (CineForge's "narrative atom" coverage, S17).
3. Every character, prop and location in a shot exists in the bible and has a ledger state for that scene.
4. `CONTINUOUS` scenes start in the previous scene's end states unless a change cites a line; within a scene, each shot starts in the previous shot's end state unless its cut record says otherwise.
5. Beats fit the shot duration; spoken words ≤ 2.5 per second (C3).
6. On-screen text ≤ 3 words per sign or marked for compositing (C3); in mirror-flagged scenes each text item has a handedness (E2).
7. No emotion adjectives in performance fields (A3).
8. Every plant has a payoff and vice versa.
9. Every job points to an existing shot and to files that exist.
10. Shot durations in a scene add up to the scene's target length within a stated tolerance (default ±10% [J]); each shot lists at most one main action unless marked `compound` (DramaChain's weakest storyboard skills, S64).
11. IDs match their pattern and were issued by the ID script, not typed by the LLM; enum values are compared after lower-casing (S57).
12. Every element in a shot that is not in the source or the bible is flagged as an addition for the human to approve (DramaChain's "restraint in additions", S64).
13. Every extracted fact carries a source line or a short verbatim quote that the validator finds in the normalized source (PACE's evidence quotes, S63).

### 6.7 Self-critique that helps and hurts

**Hurts:** "review your answer and fix problems" with no new information. GPT-3.5 changed right answers to wrong (8.8%) more often than wrong to right (7.6%); Llama-2 fell from 62.0% to 36.5% after two rounds; debate lost to majority voting at equal cost [V S50]. **Helps:** validator errors; yes/no questions generated from the records [V S20]; comparison with stored references [V S18]; a rubric-based review of a whole sequence, capped at 3 rounds as in Co-Director and FilmAgent [V S19][S1]; a reviewer whose findings are structured objects (identity drift, prop teleportation, layout reset) that point at the field to change [V S62]. **Limits of even good review:** in FilmWorld each extra repair round recovered less than half of the previous round's fixes (ratios 0.41–0.55), and 39–45% of keyframe repairs were rolled back because they did not improve [V S18]; CANVAS without its question-based selection stayed close to the full system, so most of its gain came from planning and memory, not from judging [V S20]. A reviewer returns `{record_id, rule, evidence, fix}` items; the writing stage applies fixes; the validator runs again [J].

### 6.8 Drift across 100+ shots

Compile prompts from IDs and never paraphrase an identity key; paste one global look block into every image and video prompt [V S19]; keep one reference image per state, made at first appearance [V S18][S20]; anchor video extensions to the original reference, not the last frame [V S6]; plan continuity as a table before drawing [V S20]; review each scene's keyframes as a sequence [V S19]; keep a log of which stage wrote each record, from which input hashes, with which prompt and model, so a bad clip can be walked back (clip → compiled prompt → shot → ledger → bible → source line) to the earliest wrong record [V S17].

### 6.9 Checkpoints and re-runs

Five checkpoints (6.1), each a short read [J]: A scene list (5 minutes); B design theses and identity keys (15–30 minutes); C one-line shot list per sequence (about 10 minutes each); D flagged previs stills; E takes. Mora's test without the human step scored lower [V S12]; MovieBench needed human correction even at 93% character F1 [V S16].

Re-runs [J]: one stage, one file per scene; `manifest.json` stores the input hashes each file was made from, and a stage re-runs only when one changed; approved records carry `"locked": "yes"` and later stages may add but not change them; IDs never shift (new shots take in-between numbers; cut ones become `OMITTED`). Rule changes follow decision rule 32: re-run the saved test scenes first, as CineForge admits a rule change only if replay shows no regression [V S17]. Because every shot's plan (state, keyframe, end state) exists before any rendering, shots can be generated in parallel; FilmWorld cut keyframe wall-clock time from 0.61 to 0.11 minutes per shot with six parallel workers [V S18].

### 6.10 Instructions any LLM can follow

From Anthropic's skill guidance, applicable to any model [V S55]: numbered workflows with a copyable checklist; "Run validator → fix errors → repeat"; "plan-validate-execute" (write a plan file, check it with a script, then act); "Choose one term and use it throughout"; strict templates where format matters; input/output example pairs; exact commands for fragile steps; nothing time-sensitive in instructions; test with every model you plan to use. Also from the same page [V S55]: **build evaluations before writing extensive instructions** (three test scenarios, run without the skill for a baseline, then write just enough to pass them); make validator messages name the field and list the allowed values; name skills in gerund form ("breaking-down-screenplays"); when a skill calls MCP tools, use fully qualified tool names. For this pipeline the three evaluation scenarios are *The Catch* SC06 (the fall), SC13 (the playback) and SC15 (the tablet insert) [J].

### 6.11 Packaging as an Agent Skill

**How it works** [V S52][S54][S55]. A skill is a folder: `SKILL.md` (YAML front matter with `name` and `description`, then instructions) plus optional `scripts/`, `references/` and `assets/`. Loading is progressive: about 100 tokens of name and description at start-up; the `SKILL.md` body (recommended under 5,000 tokens and 500 lines) when a task matches; other files only when read; scripts run with "only the script's output" entering context. `name`: up to 64 lowercase letters, digits and hyphens, not starting or ending with a hyphen, no double hyphens, matching the folder name, and (for Anthropic) without "anthropic" or "claude". `description`: up to 1,024 characters, third person, saying what the skill does and when to use it. Optional front-matter fields in the open standard: `license`, `compatibility` (up to 500 characters, e.g. "Needs Python 3 and network access for generation stages"), `metadata`, and the experimental `allowed-tools`. The standard's `skills-ref validate ./folder` command checks the front matter [V S52]. Keep references one level deep, because nested files may be read only partially ("head -100").

**Where it runs** [V S54][S70]: the Claude API (with the code execution tool; no network and no package installation in the container; shared across a workspace); Claude Code (`~/.claude/skills/` or `.claude/skills/`; full network; shareable as a Claude Code plugin); claude.ai (private to each user; network access depends on user and admin settings). **claude.ai steps, per the Help Center on 27 Sep 2026** [V S70]: Settings > Capabilities > turn on "Code execution and file creation"; then Customize > Skills > "+" > "Create skill" > "Upload a skill" and choose the ZIP. The Help Center lists Free, Pro, Max, Team and Enterprise plans, and the pricing page's feature table marks Skills "Yes" for Free [V S71]; the developer overview page still says "Settings > Features" and "Pro, Max, Team, and Enterprise" [S54], so if the menus differ, follow what the app shows. Skills do not sync between these surfaces. Anthropic published the format as an open standard on 18 December 2025 [V S56]; the standard's client list includes ChatGPT & Codex, Gemini CLI, GitHub Copilot, VS Code, Cursor, Junie, Goose and many more [V S53].

**Does it suit this pipeline? Yes** [J]: this knowledge library becomes `references/`, loaded only when a stage needs it; parser, validator, prompt compiler and exporters become deterministic `scripts/`; schema and templates become `assets/`; one folder serves Claude and other agents that read the standard. Limits: the API container has no network, so generation stages must run in Claude Code or via MCP connectors; audit any skill that fetches outside content [V S54].

```
breaking-down-screenplays/
  SKILL.md                 overview, stage table, checklists, which reference to read when
  references/
    stage-0-intake.md … stage-9-export.md   inputs, steps, output, one example each
    knowledge/A1…C5.md     this library, read on demand
    schema-guide.md        every field in plain English
  assets/
    breakdown.schema.json  templates/  examples/catch-SC06.json
  scripts/
    normalize_fountain.py  validate.py  compile_prompts.py
    export_csv.py  export_otio.py  export_edl.py  export_doc.py
```

---

## 7. Recipes (step by step, with an LLM doing the technical work)

**Recipe 1. Install the pipeline (once, 15–30 minutes; cost: a Claude plan, $0–20 a month for a short film [V S71; sufficiency J]).** Get the skill folder as a ZIP. On claude.ai: Settings > Capabilities > turn on "Code execution and file creation"; then Customize > Skills > "+" > "Create skill" > "Upload a skill" [V S70]. In Claude Code (Pro plan or higher [V S71]) say "Put this skill folder in `.claude/skills/`." In another agent that supports the standard [V S53], follow its skills instructions, or paste `SKILL.md` into the chat and attach the reference files [J]. Test: "Which skills do you have? Describe breaking-down-screenplays in two sentences." **If** the answer does not mention the skill, **then** check that code execution is on and re-upload the ZIP with `SKILL.md` at the top level of the folder [J].

**Recipe 2. Intake a screenplay (10–20 minutes; no extra cost).** Say: "Run stage 0. Normalize this script to strict Fountain, list every change, and show the scene list with IDs and line ranges." Check the count against the script (*The Catch*: 30 scenes) and the odd lines the LLM lists (title cards such as `= THE CATCH` and `= THE END`, transitions, headings like `(ON THE TABLET)`). **If** the count differs from your own count of headings, **then** say "List every line you treated as a heading and every heading you skipped" before approving. Say "approved" to lock the scene IDs.

**Recipe 3. Analysis and design (a few hours of LLM time spread over several sessions for a script the length of *The Catch*, about 9,200 words and 30 scenes; your reading time about 1–2 hours [J]).** "Run stages 1 to 3 and stop at checkpoint B." Read only each character's design thesis and identity key (B5) and answer in plain words where they feel wrong. **If** one feels wrong, **then** name the character and the problem in one sentence ("Saye reads as cold; she should read as tired") and say "Revise only this character." Then: "Run stages 4 and 5 for scenes 1 to 7 and show me the one-line shot list." Approve or correct, then repeat per sequence. **If** a plan limit or context limit interrupts the run, **then** say "Continue from the manifest"; finished scene files are skipped (Section 6.9). The LLM runs the validator after every stage; you never read JSON.

**Recipe 4. When the validator reports errors.** "Show the errors in plain English, grouped by record." Then: "Fix only these errors, change nothing else, and re-run the validator." **If** an error survives three rounds, **then** say "Trace it back to the first stage and source line that caused it." The missing piece is usually a story decision; make it yourself. **If** the validator flags an *addition* (an element not in the script), **then** answer "keep" or "cut" for each; never let it pass silently (Section 6.6, check 12).

**Recipe 5. Export (10 minutes; free tools).** "Export the shot list as CSV, the elements by breakdown category as CSV, and an animatic as OTIO with an EDL copy." (The LLM needs `pip install opentimelineio OpenTimelineIO-Plugins`; the EDL writer is in the second package [V S37].) Open the CSVs in any spreadsheet; import the OTIO into DaVinci Resolve or Premiere Pro, or the EDL into Avid (A4) [V S72, V-sec S73]. For Movie Magic Scheduling: "Export the normalized script as FDX" (via `screenplain` [V S66]), then in Movie Magic use File > Import Script; it brings in sluglines and speaking characters only, so import the element CSV by hand or use Filmustage's MMS export for the rest [V S65][S67]. Teams on Flow Production Tracking: "Write a script that creates Shots and Assets from our records," then run it with a script key from the admin [V S34 for the API; procedure J].

**Recipe 6. Compare with a commercial tool (optional, 30 minutes; free credits cover a sketch, AI storyboards need LTX's $35/mo Standard plan [V S43]).** "Export the normalized script as `.txt`" (LTX Studio accepts only `.txt` [V S41]). Upload it to LTX Studio's script-to-video and look at its scene and shot split. Paste its scene 6 split back to the LLM: "List shots it has that we lack, and anything it invented." Adopt what helps by editing our records, never the reverse.

**Recipe 7. A clip is wrong: find the cause (15 minutes).** "Show the log trail for take GJ-SC06-SH140-T03: compiled prompt, shot record, ledger rows, bible entries, source lines. Which is the earliest wrong record?" Fix it, then: "Re-run everything downstream of it for this shot only." **If** the trail shows every record was right, **then** the generator failed: "Make a new take with a different seed, or switch model per C1"; do not rewrite the records to chase one bad clip [J, following FilmWorld's finding that remaining failures come from the generators, S18].

**Recipe 8. Test the pipeline before a real run (once, 1–2 hours; then 20 minutes after every change).** Say: "Run stages 0–5 on the three test scenes SC06, SC13 and SC15 and save the outputs as the baseline." After any change to the skill's instructions or scripts: "Re-run the three test scenes, run the validator, and show me what changed against the baseline." **If** anything got worse, **then** undo the change [J, following S55 and decision rule 32].

---

## 8. Known failure modes and workarounds

| Failure | Seen in | Workaround |
|---|---|---|
| Parser finds no scenes or drops a title card | Strict Fountain on *The Catch* [V S24] | Normalize by script, log changes, human confirms scene count (Recipe 2) |
| One person under several names becomes several characters | Why Anim-Director checks names and FilmWorld resolves aliases [V S3][S18] | Alias list per character ID; validator rejects unknown names |
| Faces, costumes and sets drift | MovieAgent, DreamFactory, MovieBench [V S2][S5][S16] | Compiled identity keys; reference per state; keyframe-sequence review |
| A prop or wound contradicts an earlier scene | The motivation for FilmWorld and CANVAS [V S18][S20] | State ledger with causes; validator continuity checks |
| Abrupt joins | MovieAgent [V S2] | Start and end state on every shot; a cut record per join |
| Multi-shot request returns one shot or loses shots | HoloCine on Vidu, Kling 2.5 Turbo; FilmBench [V S15][S22] | One shot per request; join in the edit |
| Dissolves, J-cuts, L-cuts become hard cuts | CutCraft [V S21] | Transitions in the edit timeline, with handles |
| A consequence is not shown | HoloCine's glass [V S15] | Write the new state into every later shot and keyframe |
| "Review and improve" makes it worse | Huang et al. [V S50] | Validator errors and targeted questions; 3 rounds, then the human |
| Facts buried in long context are ignored | Lost in the Middle; Context Rot [V S49][S51] | One scene per call; context pack by ID; instruction first and last |
| Invented events, or source events skipped | FilmWorld fidelity results; MovieBench hallucinations [V S18][S16] | Coverage map: every shot cites lines; every line maps to a shot or an omission |
| Action and performance look weakest | FilmBench [V S22] | Previs control video (C4) or performance transfer (C1); short action shots |
| Stale export targets, retired models | Higgsfield's Sora 2 export [V S47; via C2] | Exact model name on every job; monthly re-check |
| Likeness problems from "looks like [actor]" | DreamFrame's method [V S23] | Written identity keys only |
| Structured output cut off mid-record | OpenAI's `incomplete` status [V S58] | One scene per call; check status; validator catches partial files |
| Breakdown trapped inside a platform | LTX Studio, Showrunner [V S41][S45] | Our JSON is the source of truth; platforms render |
| An LLM judge says coverage is complete when an event was dropped | PACE's scorer re-attached a deleted event [V S63] | Coverage computed by the validator from cited lines (rule 25) |
| An upstream storyboard defect reappears in every later stage | DramaChain [V S64] | Fix the earliest wrong record, re-run downstream (rule 28) |
| Shot list overruns the scene's time, or crams several actions into one shot | DramaChain's weakest storyboard skills [V S64] | Duration sum and one-main-action checks in the validator (rule 27) |
| Framing drifts from the plan (faces too big, subject off its mark) | PACE [V S63] | Previs greybox as control input; declare pose for action (rule 26) |
| Lip sync lost after J-cut or L-cut offsets | CutCraft per-shot agent [V S21] | Re-check sync on offset shots before approval (rule 31) |
| Enum values come back with different capitals and fail an exact match | Claude structured outputs [V S57] | Lowercase `snake_case` enums; case-insensitive compare (rule 29) |
| Schema rejected as "too complex for compilation" | Claude's limits: 24 optional or 16 union-typed parameters per request [V S57] | Portable subset (all fields required, no unions); one scene per call |
| A restated description contradicts the staged scene | PACE's console sentence [V S63] | Scene-level defaults inherited by shots; no restating (rule 24) |

---

## 9. Worked examples from *The Catch*

### E1. Intake: variant markup, scene IDs, and two moments that are not scenes

The headings read `## INT. FREIGHT SHAFT - CONTINUOUS`. Strict Fountain treats `#` lines as sections, "ignored completely in formatted output" [V S24], so a standard parser finds none of the 30 scenes. After the kitchen scene the script reads `> CUT TO BLACK.` then `= THE CATCH` (line 488): a synopsis line, also ignored, so the film's title card would vanish. The script ends on sound over black: `> CUT TO BLACK.` / `Three uneven strokes in the dark.` (lines 1848–1850), then `= THE END` (line 1852), a third synopsis line that would also vanish.

**Normalization (logged, then approved)** [J]: `## INT. …` → `INT. … #2#` (heading plus scene number); the opening `=` lines → a Fountain title page (`Title: THE CATCH`, `Draft date: …`); line 488 `= THE CATCH` → centered text `>THE CATCH<` in the action, recorded as a card shot; line 1852 `= THE END` → `>THE END<`, recorded as an end card; `@JUDE (V.O.)` with `(in her ear)` (lines 93–94) stays, but its dialogue record gets `channel: "radio"`, because Jude is below in the tunnel while Iona climbs the shaft, so "in her ear" implies a radio or earpiece (the script does not name the device; flag it for the director), filtered and heard in her space.

| Scene ID | Heading | Lines [V] | Special handling [J] |
|---|---|---|---|
| SC01 | INT. MEDICAL FACTORY - LOADING TUNNEL - NIGHT | 10–70 | `> FADE IN:` becomes the cut-in to SC01-SH010 |
| SC06 | INT. FREIGHT CAGE - CONTINUOUS | 198–299 | The fall (E3) |
| SC10 | INT. SAYE'S HOUSE - KITCHEN - BEFORE DAWN | 397–489 | Ends in black; title card shot `SC10-SH990`, type `card` |
| SC15 | INT. QUARANTINE - JUDE'S ROOM - CONTINUOUS (ON THE TABLET) | 838–867 | `presentation: "on_screen"`, host `PR-TABLET` in SC14 |
| SC30 | INT. QUARANTINE - IONA'S ROOM - NIGHT | 1814–1852 | `SC30-SH990`: picture black, sound only ("Three uneven strokes"); `SC30-SH995`, type `card`: THE END |

### E2. The state ledger: the puck, the flask, and who is mirrored

**Puck and flask.** Scene 4: "Inside: a small steel FLASK, the kind that keeps coffee hot. A flat black PUCK clipped underneath it." Scene 6: "His other hand goes underneath. Behind Jude's back. Out of sight." Scene 7: "The clip under it is empty." Scene 21: "The puck is still there, burnt into the grid where it was clipped."

| State ID | Scenes | State | Cause (line) |
|---|---|---|---|
| PR-PUCK.S01 | SC04–SC06 to l.223 | Clipped under the flask | l.162 |
| PR-PUCK.S02 | SC06 l.224–258 | Clipped by Eli to the cage floor grid, hidden | l.224; revealed l.740 |
| PR-PUCK.S03 | SC06 l.259 on; SC21 | Spent, "burnt into the grid", a "black blister" | l.259 ("CLACK"); l.1219 |
| PR-FLASK.S02 | SC07–SC23 | Clip empty; carried, then sealed, then in the ship's cabinet | l.312, l.713, l.1221 |
| PR-FLASK.S03 | SC24 on | Gone: "Cabinet, canister, flask and engine vanish together." | l.1418 |

**Handedness.** Scene 7: "Every letter is backwards." Scene 11: "Her own name, printed backwards." Scene 12, of the meal Saye turned: "Iona reads the label. The letters face the right way." Scene 28: "Iona looks at it. Reads it again." (the sign RECEIVING), then Eli's "familiar little smile, on the wrong side of his face." Scene 29: "The labels run opposite ways."

| Element | Before l.259 | From l.259 | After Iona's second turn (SC27 l.1563) | Evidence |
|---|---|---|---|---|
| CH-IONA | original | turned | original (inference) | l.327, l.500; reads RECEIVING l.1620–1622 |
| CH-ELI | original | turned | turned | l.1696, l.1721 |
| CH-JUDE | original | turned | turned | l.408–411 (an old white scar; Saye asks "Was your appendix on the left?"), l.1779 (ring "On his right hand") |
| PR-MEAL-SEALED | — | turned | — | l.642 "We turned it." |
| CH-ANIMAL | turned (ship world) | — | original, turned with Iona | l.1147 "Turned, like us"; l.1543; l.1801 "It used to eat what you eat." |

**Rule the validator enforces** [J]: a sign, label or lateral detail (ring hand, scar side, steering wheel) appears mirrored on screen when the element's handedness differs from the scene's `frame_handedness`. That field is a **director's decision per scene**, never inferred by the LLM: C2 lists this logic among the questions the director must settle before any text asset is made, and A3 recommends a per-scene flag for such rules. Once it is set, every text item in SC07–SC30 gets a computed orientation and C2's flip-or-composite method is chosen per item.

### E3. The cage falls: one shot record

> "Her boots leave the floor. She gets her fingers into the grid. Her body floats out behind her like washing."
> "Jude's blood lifts off the steel in round red beads and hangs in the air between them, turning."

Weightlessness, blood, three people and a moving shaft: action is every model's weakest area [V S22] and consequences get dropped [V S15]. The record, abbreviated [J]:

```json
{
  "id": "SC06-SH140", "label": "6P", "scene": "SC06",
  "beats": ["SC06-B08"], "source_lines": "242-244",
  "purpose": "The fall made visible: bodies and blood float; Iona holds on.",
  "size": "medium wide", "angle": "cage level, across the cage",
  "lens_mm": "24", "movement": "locked to the cage; the camera falls with it",
  "subjects": [
    {"state": "CH-IONA.S03", "position": "frame left", "facing": "right", "action": "fingers hooked in the floor grid, body trailing up"},
    {"state": "CH-JUDE.S02", "position": "frame right", "facing": "left", "action": "limp across Eli's arms"},
    {"state": "CH-ELI.S02", "position": "frame right, behind Jude", "facing": "Iona", "action": "holds Jude"}
  ],
  "withhold": ["Eli's right hand and PR-PUCK.S02 stay out of frame"],
  "props": ["PR-BLOOD-BEADS.S01"],
  "physics": "weightless relative to the cage; walls stream upward past the grid",
  "on_screen_text": "none",
  "duration_s": "4", "handles_s": "1",
  "start_state": "end state of SC06-SH130",
  "end_state": "Iona's grip slipping; beads mid-air between the three",
  "cut_out": "SC06-C140",
  "vfx": ["blood beads composited"],
  "previs": "PV-SC06-SH140-V01", "previs_level": "3",
  "model_targets": "per C1 section 5", "status": "designed", "locked": "no"
}
```

What the research changed [J]: `withhold` exists because scene 13 pays it off (E4); `start_state` and `end_state` come from FilmWorld [S18]; the beads stay in every later shot's `props` until the cage stops, because generators keep earlier states [S15]; the previs job supplies a control video because camera movement is the largest difference between models [S22] (C4's example plan `CATCH_SC06_SH14_cage_fall` becomes `SC06-SH140` under this file's ID rule). The next moment, "A hard metal CLACK. / BLACK. A dark with nothing in it. One instant.", is its own shot, joined by cut `SC06-C140` of type `hard`, made in the edit [S21].

### E4. The playback in scene 13: cross-references across the film

> "Security footage, paused: a camera above the top gate, looking straight down the shaft."
> "And in the long second of the fall, Eli's hand comes out from behind Jude's back. / Empty. / On the floor of the cage, where his hand was, a flat black puck is clipped to the grid."

New footage of an old moment from a new camera, paying off scene 6's "He has one hand she cannot see." (l.253). Records [J]:
- Plant `PL-04`: planted by beat `SC06-B09` (l.253, echoing l.224), paid off by shot `SC13-SH200`.
- `SC13-SH200`: `type: "screen_insert"`, `host: "PR-MONITOR"`, `replays: ["SC06-B08", "SC06-B09"]`, `camera: "CAM-SHAFT-TOP"` (straight down), `look: "LK-CCTV"`.
- Validator: replayed beats exist; elements use the ledger state **at the replayed moment** (`PR-PUCK.S02`, clipped, not `S03`, burnt); every SC06 shot between l.224 and l.258 honours its `withhold`; `PL-04` has both ends.
- Production: re-render the SC06 previs plan from the top-gate camera (C4) so the geometry matches, generate the clip small and grainy, and composite it onto the monitor (C1 Recipe 9). Iona's "Our cage." in SC12 (l.589), after the carriage turns, and this playback are logged under one motif, `MO-HANDEDNESS` (B4).

---

## 10. Recommended data model

### 10.1 ID rules

| Record | Pattern | Example | Display label |
|---|---|---|---|
| Project | 3–8 capitals | `CATCH` | *The Catch* |
| Scene | `SC` + 2 digits (+ letter if inserted) | `SC06`, `SC06A` | "6", "6A" |
| Beat | scene + `-B` + 2 digits | `SC06-B08` | — |
| Shot | scene + `-SH` + 3 digits, steps of 10 | `SC06-SH140`; insert `SC06-SH145` | "6P" (letters in order from A for SH010, I and O skipped [V-sec S74]; the project records whether S, Y, Z are also skipped and whether the first setup is unlettered) |
| Cut | scene + `-C` + number of the shot it follows | `SC06-C140` | — |
| Bible entries | `CH-`, `LOC-`, `PR-`, `MO-`, `WR-`, `LK-`, `PL-`, `CAM-` + name | `CH-IONA`, `WR-MIRROR` | Name |
| State | element + `.S` + 2 digits | `CH-IONA.S03` | — |
| Storyboard frame | `SB-` + shot + frame letter | `SB-SC06-SH140-A` | — |
| Previs job | `PV-` + shot + `-V` + 2 digits | `PV-SC06-SH140-V01` | "previs version 1" |
| Generation job | `GJ-` + shot + `-T` + 2 digits | `GJ-SC06-SH140-T03` | "take 3" |
| Log entry | `LOG-` + 6 digits | `LOG-000123` | — |

File names: `PROJECT_SCENE_SHOT_slug_JOB.ext`, e.g. `CATCH_SC06_SH140_blood-beads_GJ-T03.mp4`; C3's display form "13-04" and C4's `CATCH_SC06_SH14` map onto these rules. Steps of 10 let a new shot fit between two others without renumbering, the purpose of A3's "12A" rule for scenes (common VFX practice [U: no single authority found]). IDs never change and are never reused; cut records become `OMITTED` [J]. IDs are issued by a script (`next_id`), never typed by the LLM (rule 23).

**Field authority** (PACE [S63]): every field in the schema guide is marked `extracted` (read from the source; must carry `source_lines` or a short `evidence` quote), `authored` (a creative decision; carries `decided_by`: `llm` or `human`, and `locked`) or `derived` (computed by a script; the LLM may not write it). The validator enforces all three.

**Inheritance** (PACE [S63]): a scene record holds `defaults` (location state, time of day, look key, lens package, frame handedness); a shot holds only `overrides`; the prompt compiler merges defaults and overrides and records the result in the job, so no value is ever restated by hand.

### 10.2 Entities, key fields and why

| Entity | Key fields | Why |
|---|---|---|
| **Project** | ID, title, source file and hash, source type, aspect ratio, fps (frames per second), runtime target, global look key, tool targets, schema version | One configuration shared by all stages [S19]; timelines need fps [S36][S38] |
| **Story analysis** | Events per scene, sequences, character spines, turning points, plants and payoffs, themes, point-of-view plan, adaptation notes | MovieAgent's reasoned splits [S2]; CineScope's causal and character-arc measures [S17]; A1, A2 |
| **Visual bible** | Look keys, palette, lens package, world rules, style frames; contains character, location, prop and motif entries | DreamFactory, Co-Director [S5][S19]; B1–B4 |
| **Character** | Names and aliases, role, design thesis, identity key (25–40 words), voice key, states, reference image per state, "no real person" rule | MovieBench character bank [S16]; per-state reference images [S8][S18]; B5 |
| **Location** | Headings covered, layout plan file, look key, states, reference image per state | CANVAS location grouping [S20]; FilmWorld location attributes [S18]; C4 |
| **Prop** | Breakdown category, hero flag, states, references | CANVAS object states [S20]; breakdown categories [S27] |
| **State** (ledger row) | Element ID, scene and line range, attributes (costume, injury, condition, handedness), cause line, reference image | FilmWorld state IDs [S18]; CineForge ledgers [S17] |
| **Motif** | Meaning, visual rule, occurrences (shot IDs), development | B4; lets the validator catch a dropped motif |
| **Scene** | Heading, INT/EXT, time, story day, location, lines, sequence, event, presentation, characters, start and end states, `defaults` inherited by its shots, target duration, status, locked | MovieBench scene level [S16]; PACE inheritance [S63]; DramaChain duration budgeting [S64]; A3 |
| **Beat** | Lines, action, reaction, playable action, turning-point flag, plant/payoff links, key-shot flag | FilmAgent's line-level lesson [S1]; A2 |
| **Shot** | Label, beats, source lines, purpose, `overrides` of scene defaults, size, angle, lens, movement, subjects (state, position, facing, action, pose if action-critical), withhold, `required` and `forbidden` elements, dialogue with channel, sound, on-screen text with handedness, duration, handles, start and end state, cut out, VFX, previs level (framing-critical shots get a greybox control), model targets, additions flagged for approval, status, locked | MovieBench shot level [S16]; FilmWorld end states [S18]; CineCrew continuity hooks [S62]; PACE framing and pose [S63]; C3 §15; C4; A3 |
| **Cut** | From shot, to shot, type (hard, dissolve, wipe, J, L, match), made in edit, shared geometry for match cuts, audio offset and a lip-sync check flag | CutCraft [S21]; A4 |
| **Storyboard frame** | Shot, moment (start, middle, end), compiled prompt, references, image file, model, approved | StoryDiffusion, CANVAS [S11][S20]; C2 |
| **Previs job** | Shot, plan file, lens and sensor, camera path, beats by frame, passes, outputs, status | CineMaster [S10]; C4 |
| **Generation job** | Shot, platform, exact model name, mode, input paradigm (first/last frame, reference images, keyframe, control video), inputs, compiled prompt, duration, seed, resolution, cost, output file, review answers (structured findings: rule, evidence, fix), kept (= circled) or rejected (= NG) | Camera report tradition [S30]; DramaChain input paradigms [S64]; CineCrew QA objects [S62]; C1, C3 |
| **Log entry** | Stage, records written, input hashes, model, prompt hash, time, earliest causal stage when a defect is traced | CineForge's decision log and causal-stage attribution [S17] |

### 10.3 Files on disk

```
CATCH/
  manifest.json        every file, its stage, the hashes of its inputs
  source.fountain      normalized; the original kept beside it with its hash
  scenes_index.json    SC01 … SC30 with line ranges, locked
  story_analysis.json  bible.json  ledger.json
  scenes/SC01.json …   scene, beats, shots, cuts
  jobs/                storyboard, previs and generation job records
  exports/             shot_list.csv  elements.csv  animatic.otio  animatic.edl  breakdown.md
  log/                 one entry per stage run
```

---

## 11. What I could not verify

- Final Draft's own FDX specification (I relied on Fountain's site offering `.fdx` files, `screenplain`'s FDX writer and general knowledge that FDX is XML). Whether Movie Magic reads `screenplain`'s FDX output cleanly is untested.
- Movie Magic Scheduling's price (import formats are now verified, S65); StudioBinder and Celtx APIs; Filmustage's API.
- Kaiber's current product and prices from Kaiber itself (its site needs JavaScript; review sites only); Katalist's input file formats and its "Veo 3.2" listing; Storyboarder.ai's paid prices; M Studio's API.
- The Chinese short-drama platforms named by DramaChain (OiiOii, Flova, XiaoYunQue, LibTV): not opened.
- Whether LTX Studio exposes projects, shot splits or Elements through any API; Flora's MCP tool list (its documentation page did not list them).
- A complete camera report column list from a primary source.
- Whether consumer ChatGPT and the Gemini web app load a skill folder; the standard's client list names "ChatGPT & Codex" and "Gemini CLI". The maximum ZIP size for a claude.ai skill upload (the Help Center mentions a limit without a number).
- Which Premiere Pro version first shipped OTIO outside beta; the DaVinci Resolve OTIO claim rests on a copy of the Resolve 18.6 manual and search summaries.
- Gemini: the keyword list does not name `anyOf` or `$ref`, but the documentation's examples use both; the portable subset avoids both anyway.
- Twelve 2026 papers found but not read (listed in Section 1A), and the baselines ViMax, AniMaker and VideoClaw. Co-Director's evidence comes from advertising, not drama.
- The single authority for steps-of-10 shot numbers; letter skipping (I and O, sometimes S, Y, Z) rests on a camera-assistant blog (S74), not a union or studio rulebook.

---

## 12. Sources (all checked 2026-09-27)

Research papers (read through alphaXiv, https://www.alphaxiv.org ; the "also found" titles in Section 1A were located with alphaXiv search the same day):
- [S1] Xu et al., FilmAgent: https://arxiv.org/abs/2501.12909
- [S2] Wu, Zhu, Shou, MovieAgent (Automated Movie Generation via Multi-Agent CoT Planning): https://arxiv.org/abs/2503.07314
- [S3] Li et al., Anim-Director: https://arxiv.org/abs/2408.09787
- [S4] Lin et al., VideoDirectorGPT: https://arxiv.org/abs/2309.15091
- [S5] Xie et al., DreamFactory: https://arxiv.org/abs/2408.11788
- [S6] Zhao et al., MovieDreamer: https://arxiv.org/abs/2407.16655
- [S7] Hu et al., StoryAgent: https://arxiv.org/abs/2411.04925
- [S8] Zheng et al., VideoGen-of-Thought: https://arxiv.org/abs/2412.02259
- [S9] Hong et al., DirecT2V: https://arxiv.org/abs/2305.14330
- [S10] CineMaster: https://arxiv.org/abs/2502.08639
- [S11] Zhou et al., StoryDiffusion: https://arxiv.org/abs/2405.01434
- [S12] Yuan et al., Mora: https://arxiv.org/abs/2403.13248
- [S13] Zhuang et al., Vlogger: https://arxiv.org/abs/2401.09414
- [S14] Xiao et al., Captain Cinema: https://arxiv.org/abs/2507.18634
- [S15] Meng et al., HoloCine: https://arxiv.org/abs/2510.20822
- [S16] Wu et al., MovieBench: https://arxiv.org/abs/2411.15262
- [S17] Liu, Wang et al., CineForge: https://arxiv.org/abs/2608.29621
- [S18] Zuo et al., FilmWorld: https://arxiv.org/abs/2607.19038
- [S19] Song et al., Co-Director: https://arxiv.org/abs/2604.24842
- [S20] Mondal et al., CANVAS: https://arxiv.org/abs/2604.13452
- [S21] Zeng et al., Beyond Coherence (CutCraft): https://arxiv.org/abs/2609.08275
- [S22] Wang et al., FilmBench: https://arxiv.org/abs/2607.24241
- [S23] Song et al., DreamFrame (formerly MovieLLM): https://arxiv.org/abs/2403.01422
- [S62] Chen, Dong et al., Better Call CineCrew (7 Sep 2026): https://arxiv.org/abs/2609.07720
- [S63] Duan et al., PACE: Precise AI Cinematic Expression (17–18 Sep 2026): https://arxiv.org/abs/2609.19853 (code: https://github.com/StudioPiLabs/pace-core)
- [S64] Shi, Chen et al., DramaChain Bench (1 Sep 2026): https://arxiv.org/abs/2609.00646

Formats and production software:
- [S24] Fountain syntax (version 1.1): https://fountain.io/syntax
- [S25] Fountain home: https://fountain.io/
- [S26] Final Draft product page: https://www.finaldraft.com/products/final-draft/
- [S27] Wikipedia, Script breakdown: https://en.wikipedia.org/wiki/Script_breakdown
- [S28] StudioBinder, script breakdown colors: https://www.studiobinder.com/blog/script-breakdown-colors/
- [S29] StudioBinder, how to make a shot list: https://www.studiobinder.com/blog/how-to-make-a-shot-list/
- [S30] StudioBinder, camera report template: https://www.studiobinder.com/blog/camera-report-template/
- [S31] Entertainment Partners, Movie Magic Scheduling: https://www.ep.com/movie-magic-scheduling/
- [S32] Celtx: https://www.celtx.com/
- [S33] Filmustage: https://filmustage.com/
- [S34] Flow Production Tracking Python API: https://developers.shotgridsoftware.com/python-api/
- [S35] Wikipedia, Edit decision list: https://en.wikipedia.org/wiki/Edit_decision_list
- [S36] OpenTimelineIO documentation: https://opentimelineio.readthedocs.io/en/latest/
- [S37] OpenTimelineIO README: https://github.com/AcademySoftwareFoundation/OpenTimelineIO
- [S38] OTIO CMX 3600 adapter README: https://github.com/OpenTimelineIO/otio-cmx3600-adapter
- [S39] PyPI, opentimelineio 0.18.1 and OpenTimelineIO-Plugins 0.18.1: https://pypi.org/project/opentimelineio/
- [S65] Movie Magic Scheduling Manual, Importing Breakdown Sheets (.fdx, .sex, Movie Magic Screenwriter): https://mms-docs.ep.com/Breakdown/ImportingBreakdownSheets.html
- [S66] screenplain 0.12.0 (PyPI, 28 Apr 2026) and README (FDX, HTML, PDF output): https://pypi.org/project/screenplain/ ; https://github.com/vilcans/screenplain
- [S67] Filmustage, pricing: https://filmustage.com/pricing/
- [S72] Adobe Community, "[Now Released] OTIO Import and Export" (Premiere Pro): https://community.adobe.com/announcements-732/now-released-otio-import-and-export-311699
- [S73] DaVinci Resolve 18.6 manual, "Importing OTIO Project Files" (unofficial mirror; secondary): https://www.steakunderwater.com/VFXPedia/__man/Resolve18-6/DaVinciResolve18_Manual_files/part1411.htm
- [S74] The Black and Blue (camera-assistant blog), "Slating the Alphabet from Apple to X-Ray" (letters skipped: I, O, Y, Z): https://www.theblackandblue.com/2011/03/03/slating-the-alphabet-from-apple-to-x-ray/
- [S75] Wikipedia, Clapperboard (American and European slate systems): https://en.wikipedia.org/wiki/Clapperboard

Commercial platforms:
- [S40] LTX Studio: https://ltx.io/studio
- [S41] LTX Studio, script to video: https://ltx.io/studio/platform/script-to-video
- [S42] LTX Studio, AI storyboard generator: https://ltx.io/studio/platform/ai-storyboard-generator
- [S43] LTX Studio, pricing: https://ltx.io/studio/pricing
- [S44] Katalist, AI storyboard generator: https://www.katalist.ai/ai-storyboard-generator
- [S45] Showrunner: https://www.showrunnerstudio.com/
- [S46] Luma, information for AI assistants (updated 13 Jul 2026): https://lumalabs.ai/llm-info
- [S47] Higgsfield, storyboard generator (Popcorn): https://higgsfield.ai/storyboard-generator
- [S48] Flora: https://flora.ai/
- [S68] Katalist, pricing: https://www.katalist.ai/katalist-pricing
- [S69] Flora, pricing: https://flora.ai/pricing
- [S76] M Studio, home page and its "Best script-to-video tools 2026" guide (vendor-written): https://mstudio.ai/ ; https://mstudio.ai/insights/best-script-to-video-tools-2026
- [S77] Storyboarder.ai: https://www.storyboarder.ai/
- [S78] Kaiber (own site needs JavaScript): https://kaiber.ai/ ; secondary: Product Hunt https://www.producthunt.com/products/kaiber and review summaries found by web search (e.g. https://videoia.fr/en/kaiber-ai-review/)
- Via C1 and C2 (verified by those files the same day): Runway MCP https://runway.com/mcp ; Higgsfield MCP https://higgsfield.ai/mcp ; Boords https://boords.com/ai-storyboard-generator ; Sora 2 API removal date as reported in C2.

LLM engineering:
- [S49] Liu et al., Lost in the Middle: https://arxiv.org/abs/2307.03172
- [S50] Huang et al., Large Language Models Cannot Self-Correct Reasoning Yet: https://arxiv.org/abs/2310.01798
- [S51] Chroma, Context Rot (14 Jul 2025): https://www.trychroma.com/research/context-rot
- [S52] Agent Skills specification: https://agentskills.io/specification
- [S53] Agent Skills client showcase: https://agentskills.io/clients.md
- [S54] Anthropic, Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- [S55] Anthropic, Skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- [S56] Anthropic Engineering, Equipping agents for the real world with Agent Skills (16 Oct 2025; open-standard update 18 Dec 2025): https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- [S57] Anthropic, Structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- [S58] OpenAI, Structured Outputs: https://developers.openai.com/api/docs/guides/structured-outputs
- [S59] Google, Gemini structured output: https://ai.google.dev/gemini-api/docs/structured-output
- [S60] Anthropic Engineering, Building effective agents (19 Dec 2024): https://www.anthropic.com/engineering/building-effective-agents
- [S61] PyPI, jsonschema 4.26.0 and pydantic 2.13.5 (validator libraries): https://pypi.org/project/jsonschema/ ; https://pypi.org/project/pydantic/
- [S70] Claude Help Center, Using Skills in Claude (Settings > Capabilities; Customize > Skills; plans): https://support.claude.com/en/articles/12512180-using-skills-in-claude
- [S71] Claude pricing (Pro $20/mo or $17/mo yearly; Max from $100; Skills listed for Free): https://claude.com/pricing

**Fact-check note (2026-09-27).** An adversarial pass re-opened S1, S2, S4, S6, S15–S22, S24, S26, S28–S32, S34, S37–S41, S43–S48 and S50–S61, and added S62–S78; S3, S5, S7–S14, S23, S25, S33 (home page), S35, S36 and S42 were not re-opened and keep the first author's verification. Every quotation from *The Catch* in Section 9 was matched verbatim against the screenplay file and its line numbers. Corrections made: Claude structured outputs **do** support simple `pattern` regexes (the draft said not), and their limits (24 optional parameters, 16 union parameters, 20 strict tools), enum-capitalization caveat, refusal and cut-off cases were added; OpenAI's size limits and Gemini's `anyOf`/`$ref` examples were added; the claude.ai skill upload path moved to Customize > Skills and the Free plan is now listed; OTIO's EDL writer needs `OpenTimelineIO-Plugins`; Movie Magic's import formats, Filmustage, Katalist, Flora and Final Draft prices, Luma's current products and LTX Studio's plan contents were verified and added; Katalist's and Higgsfield's stale Sora 2 listings flagged; `= THE END` (line 1852) added to the intake problems; Jude's scar evidence re-cited to lines 408–411; the "earpiece" reading marked as an inference; CineCrew, PACE and DramaChain Bench read and added, with four new lessons and eleven new decision rules; M Studio, Storyboarder.ai, Google Flow, Adobe Firefly, Kaiber and Chinese short-drama platforms added to the platform table; a cost-and-difficulty table (4A) and an evaluation recipe (Recipe 8) added.
