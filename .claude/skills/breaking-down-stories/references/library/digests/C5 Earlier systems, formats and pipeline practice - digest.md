# Digest C5: Prior systems, industry formats and reliable LLM pipelines (27 Sept 2026)

Source: `research/C5_prior_systems_formats_llm_practice.md` (660 lines). Brackets: R# = the file's decision rule (§5); L# = lesson (§2); Rec# = recipe (§7); E# = worked example (§9); V# = validator check (§6.6). Evidence labels: **[V]** verified at source, **[V-sec]** secondary only, **[U]** unverified, **[J]** author's judgment. Most pipeline-engineering rules are [J] built on [V] paper results; tool prices and features are [V] as of 2026-09-27 and go stale.

## 1. Scope

1. Surveys 2023–Sept 2026 research systems and commercial platforms that turn scripts into shots, and draws 14 lessons on what worked and failed.
2. Names the formats the breakdown imports (Fountain, FDX, PDF) and exports (shot list/element CSV, OTIO, EDL, Movie Magic, Flow), and how to run a long multi-stage LLM pipeline without drift (stages, gates, schema, IDs, validator, re-runs, Agent Skill packaging).
3. Supplies the recommended data model (entities, fields, IDs, files) and applies it to four hard moments of *The Catch*; it is the architecture the other 13 subjects plug into.

**Terms** [§0]: *bible* ("visual bible") = fixed facts no stage may contradict; *state* = an element's condition at one moment; *ledger* = every changeable element's state per scene (A3's "continuity bible"); *handedness* = `original` or mirror-reversed `turned`; *gate* = check before the next stage (*validator* = program, *checkpoint* = human); *field authority* = who may write a field: *extracted* (from source, with line ref), *authored* (creative decision), *derived* (script-computed); *identity key / look key* = fixed word blocks pasted unchanged into prompts (25–40 words per character; light/colour/texture per film or sequence); *context pack* = exact files/excerpts given to one call; *generation job* = one image/video request (the AI camera-report line); *previs job* = one Blender render; *handles* = extra seconds each side of the used clip; *greybox* = plain grey 3D render used as control input; *enum* = field limited to a word list; *drift* = unintended gradual change.

## 2. Rules

**Intake and chunking**
1. [R1] If the source is PDF or FDX, then convert to Fountain and have the human confirm the scene count before stage 1, because every ID hangs on the scene list and layout parsing fails silently.
2. [R2, §3] If a screenplay uses non-standard markup (`##` headings, `=` title cards), then normalize to strict Fountain by script, log every change, keep the original with its hash, because strict Fountain ignores `#` sections and `=` synopses (zero scenes found).
3. [R3] If the source is prose, then segment chapter → scene → numbered paragraphs and resolve aliases and pronouns to character IDs before shot design, because FilmWorld's entity resolution precedes all planning.
4. [R17, §6.2] If a call would need more than one scene's source plus its bible entries, then split it (one scene per call; instruction first, repeated last), because accuracy drops for facts mid-context and as input grows; "even a single distractor reduces performance".

**Structure and single source of truth**
5. [L1, L2, §6.1] If laying out records, then use five levels (project, scene, beat, shot, job), plan at the beat not the dialogue line, and prefer a chain of stages with gates over simulated agent crews, adding complexity only when it demonstrably helps, because skipping middle levels cost DreamFrame 0.14 CLIP, FilmAgent's per-line plan was too coarse for action, and the best 2026 results came from chains with explicit state and validators.
6. [R4, L8] If a fact holds for the whole film, then store it once in the bible, cross-reference by ID, and inject one global look block into every prompt, because restated facts drift.
7. [R24, L12] If a value holds for a whole scene (location state, lens package, look key, time of day, frame handedness), then set it once in scene `defaults`; shots carry only `overrides`; the prompt compiler merges them and records the result in the job, because restated values drift from what is staged (a restated sentence naming an unstaged console shifted frames 53% vs 18%).
8. [R23, L11] If a field is an ID, line range, count, duration total or cross-reference, then a script writes or checks it (IDs from `next_id`) and the LLM never invents it; every field is marked extracted/authored/derived, because CineForge fixes this "deterministic scaffold" in code and lets LLMs fill only bounded fields.
9. [§6.5, L7] If recording a relationship, then store ID lists, never names; keep an alias list per character; reject unlisted names, because names vary ("Io", "IONA", "her brother").
10. [§10.1] If a shot or scene is added or cut, then no ID shifts or is reused: shots step in 10s (insert `SH145`), inserted scenes take a letter (`SC06A`), cut records become `OMITTED`; industry labels ("6P", "12A") are generated display labels, never IDs.

**State and continuity**
11. [R5, L3] If anything about an element can change, then give it a ledger row from its first change, each change citing its cause line (validator refuses one without), because explicit state is the largest consistency effect found (FilmWorld 82.12 → 54.50 without; CANVAS background continuity −50–57% without location grouping).
12. [R6, L4] If a character's look changes (injury, costume, age, handedness), then create a new state ID with its own reference image made at first appearance, because references work per state.
13. [R7, L5, V4] If a shot ends, then record its end state; if the next shot or a `CONTINUOUS` scene follows on, then copy it into the start state unless a change cites a line, because joins break without it (FilmWorld needed both the written end state and the keyframe).
14. [R8, L6] If an action changes an object, then write the new state into every later shot and keyframe showing it, because generators keep the earlier state ("an empty glass remaining empty after water is poured").
15. [R33] If a shot must include or exclude an element, then list it in `required` or `forbidden`, because CineCrew's reviewer checks these explicit hooks.

**Structured output and validation**
16. [R9, R10] If a model call returns breakdown data, then use structured output and still run the validator, and put every code-checkable rule (IDs resolve, coverage, durations, words per second, anything the portable schema cannot express) in the validator, not a prompt, because a schema guarantees shape not meaning, and scripts are deterministic with only their output entering context.
17. [R29, §6.4] If a field is an enum, then use lowercase `snake_case` values differing by more than capitalization, compared case-insensitively; write `"none"` not `null`; store JSON not YAML; send one scene per call, because Claude does not guarantee enum capitalization, the portable subset has no unions, hand-edited YAML breaks, and a cut-off then loses one scene at most.
18. [R25, L14] If an LLM reports every event covered, then do not accept it: every shot cites source lines and the validator computes coverage, because PACE's LLM scorer re-attached a deliberately deleted event.
19. [R27, L13] If a scene's shot list is written, then the validator sums durations against the scene target (±10%), flags shots with more than one main action unless `compound`, and flags elements not in source or bible as additions for human keep/cut, because shot rhythm (2.74/5) and restraint in additions (3.34/5) were the weakest storyboard skills and duration is checkable before any picture.
20. [§6.6, §6.10] If the validator reports, then print one line per problem naming record, field, rule and allowed values.

**Review and judging**
21. [R11] If a check needs judgment, then ask yes/no questions derived from records ("Is Iona's hand bandaged in this frame?"), because an open-ended judge could not even rank real footage above generated.
22. [R12] If tempted to say "review and improve your answer", then put every requirement in the first instruction and run the validator, because intrinsic self-correction lowered accuracy (Llama-2 62.0% → 36.5%).
23. [R13, L10] If a repair loop fails 3 times, then stop and show the human, because gains per round roughly halve (39–45% of keyframe repairs were rolled back) and candidate count saturates at 3.
24. [R14] If options are wanted for a creative choice, then generate 2–3 independent versions for the human to pick, because equal-cost voting beat debate and taste is the human's call.
25. [L10, §6.7] If reviewing keyframes, then review each scene's keyframes as a sequence against a rubric and return findings `{record_id, rule, evidence, fix}`, because removing whole-sequence review cost Co-Director 9.8 points of asset fidelity.

**Generation and edit**
26. [R15, L9] If a sequence has several shots, then generate one shot per request with 0.5–1 s handles and join in the edit, because multi-shot requests lose 7.9 points on average (up to 22.8) and drop shots.
27. [R16] If a cut is a dissolve, wipe, J-cut or L-cut, then mark it on the cut record and make it in the edit, because generators collapse them into hard cuts.
28. [R30] If a cut is a match cut or occlusion wipe, then build both shots from the same previs geometry or shared keyframes, because per-shot generation did worse on cross-shot spatial continuity.
29. [R31] If an audio offset is applied in the edit, then re-check lip sync on affected shots before approval, because per-shot composition lowered A/V sync for every model tried.
30. [R26, L14] If framing carries the story (reveal, insert, playback, precise face size), then stage it in previs and pass the greybox as control; if action also matters, then declare the pose too, because words gave heads ~1.9× intended size, greybox 0.955×, and declaring pose raised action delivery 58.9% → 74.4%.
31. [§6.8, §8, E3] If extending video, then anchor to the original reference, not the last frame, chaining last → first frame only inside one continuous take; if a shot is action-heavy or the camera moves, then use a previs control video or performance transfer and keep action shots short, because last-frame chaining degraded quality and camera movement is the largest difference between models.
32. [R21] If a description would name a real person ("looks like [actor]"), then use a written identity key, because that shortcut creates likeness and consent problems.

**Re-runs, debugging, tools**
33. [R18, §6.9] If a stage's inputs are unchanged (`manifest.json` hashes), then skip it; if a record is `"locked": "yes"`, then later stages may add but never change it, because re-runs must not undo approved work.
34. [R28, Rec7] If a clip is wrong, then trace it to the earliest wrong record, fix that and re-run downstream; if every record was right, then make a new take (new seed or model) and leave the records alone, because upstream defects are "re-expressed downstream, not repaired" and remaining failures come from generators.
35. [R32] If a stage instruction or validator rule changes, then re-run the saved test scenes (SC06, SC13, SC15) against the baseline and undo if anything worsened, because CineForge admits rule changes only after replay shows no regression.
36. [R19] If different LLMs will run the pipeline, then keep core instructions free of provider-only features and test with the smallest model, because "what works perfectly for Opus might need more detail for Haiku".
37. [R20, R22] If a platform offers in-app script-to-video, then use it only as a sketch or render target; if a tool fact is over a month old, then re-check it and put the exact model name on every job, because no platform exports its shot plan as open data and features vanish (Sora 2 exports outlived the Sora 2 API).

## 3. Breakdown fields

Enums lowercase `snake_case`; empty = `"none"`. Every field is marked `extracted` (needs `source_lines` or `evidence` quote), `authored` (carries `decided_by`: `llm` | `human`, and `locked`) or `derived` (script only).

| Level | Field | Meaning | Values / example |
|---|---|---|---|
| film | `project_id`, `title`, `schema_version` | Project identity | 3–8 capitals: `CATCH` |
| film | `source_file`, `source_hash`, `source_type` | Normalized source; original's fingerprint | `source.fountain`; `screenplay` \| `prose` |
| film | `aspect_ratio`, `fps`, `runtime_target`, `tool_targets` | Delivery settings (timelines need fps) | per project |
| film | `global_look_key` | Look block injected in every prompt | `LK-` ID |
| film | `slate_convention` | Label letters: I/O always skipped; whether S/Y/Z skipped; first setup unlettered? | recorded once |
| film | story analysis: `events`, `sequences`, `spines`, `turning_points`, `plants_payoffs`, `themes`, `pov_plan`, `adaptation_notes` | Stage-1 output | `PL-04`: planted_by `SC06-B09`, paid_off_by `SC13-SH200` |
| film | bible: `look_keys`, `palette`, `lens_package`, `world_rules`, `style_frames`, cameras | Fixed visual facts | `WR-MIRROR`, `LK-CCTV`, `CAM-SHAFT-TOP` |
| sequence | `sequence` (scene field) | Group for checkpoint C shot lists | scenes 1–7 |
| scene | `id`, `label`, `heading`, `int_ext`, `time`, `story_day`, `location` | Locked ID, display label, slugline parts | `SC06` / "6"; `LOC-` ID |
| scene | `source_lines` | Line range (derived) | `198-299` |
| scene | `event`, `characters`, `start_states`, `end_states` | Scene change; cast; ledger state IDs | `CH-IONA.S03` |
| scene | `presentation`, `host` | How shown; prop that shows it | `on_screen`; `PR-TABLET` |
| scene | `defaults` | Inherited by shots: location state, time of day, look key, lens package, frame handedness | object |
| scene | `frame_handedness` | Which way the world is shown (human-authored only) | `original` \| `turned` |
| scene | `target_duration`, `status`, `locked` | Time budget; progress; approval | seconds; `designed`; `yes` \| `no` |
| beat | `id`, `lines`, `action`, `reaction`, `playable_action`, `turning_point`, `plant_payoff_links`, `key_shot` | One action + reaction | `SC06-B08` |
| shot | `id`, `label`, `scene`, `beats`, `type` | Identity; special kinds | `SC06-SH140`, "6P"; `card`, `screen_insert` |
| shot | `source_lines`, `evidence`, `purpose` | Cited lines/quote; why it exists | `242-244` |
| shot | `overrides` | Only values differing from scene defaults | object |
| shot | `size`, `angle`, `lens_mm`, `movement` | Camera | `medium wide`; `24` |
| shot | `subjects[]`: `state`, `position`, `facing`, `action`, `pose` | Who, where, which way, doing what; pose if action-critical | `frame left`; `right` |
| shot | `withhold`, `required`, `forbidden` | Must stay out of frame (for payoff); must / must not appear | "Eli's right hand and PR-PUCK.S02" |
| shot | `props`, `physics` | Prop state IDs; non-default physics | `PR-BLOOD-BEADS.S01`; "weightless relative to the cage" |
| shot | `dialogue[]` with `channel`, `sound` | Lines and how heard; sound | `radio` |
| shot | `on_screen_text` with handedness | Text items, computed orientation | ≤3 words per sign, else composited |
| shot | `duration_s`, `handles_s`, `compound` | Length; extra each end; >1 main action allowed | `4`; `1`; `no` |
| shot | `start_state`, `end_state`, `cut_out` | Opens from / closes on; next cut | "end state of SC06-SH130"; `SC06-C140` |
| shot | `vfx`, `previs`, `previs_level` | Compositing; previs job; depth (greybox for framing-critical) | `PV-SC06-SH140-V01`; `3` |
| shot | `replays`, `camera`, `look`, `host` | Playbacks: replayed beats, in-world camera, look, screen | `SC06-B08`; `CAM-SHAFT-TOP`; `PR-MONITOR` |
| shot | `model_targets`, `additions`, `status`, `locked`, `decided_by` | Generator choice; unapproved extras; progress | "per C1 section 5" |
| shot (cut) | `id`, `from_shot`, `to_shot`, `type` | Join record | `SC06-C140`; `hard` \| `dissolve` \| `wipe` \| `j` \| `l` \| `match` |
| shot (cut) | `made_in_edit`, `shared_geometry`, `audio_offset`, `lip_sync_check` | Edit-side handling | `yes`; previs ID; seconds; `yes` |
| character | `id`, `names_aliases`, `role`, `design_thesis`, `identity_key`, `voice_key`, `no_real_person` | Character record | `CH-IONA`; key 25–40 words |
| character/location/prop | `states`, `reference_image` per state | One reference per state | `CH-IONA.S03` |
| location | `headings_covered`, `layout_plan_file`, `look_key` | Place record | `LOC-` |
| prop | `breakdown_category`, `hero` | Industry category (props purple, etc.); hero flag | `PR-PUCK` |
| ledger state | `state_id`, `element_id`, `scene`, `line_range`, `attributes` (costume, injury, condition, `handedness`), `cause_line`, `reference_image` | One state row | `PR-PUCK.S02`, cause l.224 |
| motif | `id`, `meaning`, `visual_rule`, `occurrences` (shot IDs), `development` | Lets validator catch dropped motifs | `MO-HANDEDNESS` |
| generation job (storyboard) | `id`, `shot`, `moment`, `compiled_prompt`, `references`, `image_file`, `model`, `approved` | One frame | `SB-SC06-SH140-A`; `start` \| `middle` \| `end` |
| previs job | `id`, `shot`, `plan_file`, `lens_sensor`, `camera_path`, `beats_by_frame`, `passes`, `outputs`, `status` | One Blender render | `PV-SC06-SH140-V01` |
| generation job | `id`, `shot`, `platform`, `model` (exact), `mode`, `input_paradigm` | Request | `GJ-SC06-SH140-T03`; `first_last_frame` \| `reference_images` \| `keyframe` \| `control_video` |
| generation job | `inputs`, `compiled_prompt`, `duration`, `seed`, `resolution`, `cost`, `output_file`, `review` (`rule`, `evidence`, `fix`), `kept` | Settings, result, verdict (circled/NG) | `kept` \| `rejected` |
| film (log) | `id`, `stage`, `records_written`, `input_hashes`, `model`, `prompt_hash`, `time`, `earliest_causal_stage` | Decision trail | `LOG-000123` |

## 4. Procedures

**P1. Stages and gates** [§6.1] (one file per scene where possible):

| Stage | Reads | Writes | Gate |
|---|---|---|---|
| 0 Intake | Source | `source.fountain` (or numbered paragraphs), `scenes_index.json` (locked IDs, line ranges) | Validator; **checkpoint A** scene list |
| 1 Story analysis | Whole source (chapter summaries for a novel) | `story_analysis.json`: events, sequences, spines, plants/payoffs, motifs | Validator |
| 2 Bible | Source, analysis | `bible.json`: characters (aliases, identity keys), locations, props, looks, world rules | Validator; **checkpoint B** design theses, identity keys |
| 3 State ledger | Source, bible | `ledger.json`: state per element per scene, each change tied to a line | Validator |
| 4 Scene design | One scene + context pack | `scenes/SC06.json`: beats, blocking, event, key shot | Validator |
| 5 Shot design | Scene file + context pack | Shots and cuts in same file | Validator; **checkpoint C** one-line shot list per sequence |
| 6 Storyboard (opt.) | Shots, bible | Frame records and images | Plan-derived questions; spot-check |
| 7 Previs (opt.) | Shots, set plans | Previs jobs, plan files, renders | **Checkpoint D** camera and blocking |
| 8 Generation (opt.) | Shots, keyframes | Generation jobs, clips | **Checkpoint E** keep/reject takes |
| 9 Export | All records | CSV, OTIO, EDL, readable doc | Validator |

**P2. Context pack for shot design** [§6.2]: stage instructions; the scene's source text with line numbers; only bible entries whose IDs the scene uses; ledger rows for those elements at scene start; previous scene's last shot and next scene's heading; this scene's analysis lines; the schema and one example record.

**P3. Compile prompts** [§6.3]: a script builds each model prompt from shot record + pasted identity key + state line + look key, merging scene `defaults` with shot `overrides`, and records the merge in the job.

**P4. Portable schema subset** [§6.4]: objects with every field required and `additionalProperties: false`; strings, integers, numbers, booleans, arrays, lowercase `snake_case` enums; nesting ≤3 levels; no recursion, `pattern`, length/range limits or `anyOf`; `"none"` for empty; everything else in the validator (jsonschema 4.26.0 or pydantic 2.13.5). Claude limits per request: 20 strict tools, 24 optional and 16 union-typed parameters, 180 s compile; check `stop_reason` (`refusal`, `max_tokens`); OpenAI marks truncation `incomplete`; Gemini says "always validate values".

**P5. Validate-fix loop** [§6.6–6.7, Rec4]: validator after every stage → errors in plain English grouped by record → "Fix only these errors, change nothing else, and re-run the validator" → after 3 failed rounds, "Trace it back to the first stage and source line that caused it" (usually a story decision for the human).

**P6. Re-runs** [§6.9]: `manifest.json` holds input hashes per file; re-run only changed ones; locked records only added to; plans exist before rendering, so shots can generate in parallel. After an interruption: "Continue from the manifest".

**P7. Trace a bad clip** [§6.8, Rec7]: "Show the log trail for take GJ-…: compiled prompt, shot record, ledger rows, bible entries, source lines. Which is the earliest wrong record?" Fix; re-run downstream for that shot only; if all right, new seed or model.

**P8. Intake normalization** [E1, Rec2]: `## INT. …` → `INT. … #2#`; opening `=` lines → title page (`Title:`, `Draft date:`); mid-film `= TITLE` → centered `>TITLE<`, recorded as a `card` shot; `> FADE IN:` → cut-in to first shot; log changes; show scene list with IDs and line ranges; if the count differs, "List every line you treated as a heading and every heading you skipped"; "approved" locks IDs.

**P9. Evaluation first** [§6.10, Rec8]: three test scenarios (*The Catch* SC06, SC13, SC15); run without the skill for a baseline; write just enough instruction to pass; save stage 0–5 outputs as baseline; after any change re-run, validate, compare; undo if worse.

**P10. Export** [§3, Rec5]: shot list CSV (StudioBinder columns: scene number; shot number or letter; description; size; angle; equipment; movement; lens; frame rate; cast; notes; plus our IDs); element CSV by breakdown category; animatic as OTIO (several video tracks) plus CMX 3600 EDL (one track), needing `pip install opentimelineio OpenTimelineIO-Plugins`; normalized script as FDX via `screenplain` for Movie Magic (imports sluglines and speaking characters only; add elements by hand or via Filmustage's MMS export); Flow Production Tracking via a generated Python script; Markdown document. Resolve and Premiere import `.otio`; Avid takes the EDL; Final Cut Pro neither directly [J].

**P11. Agent Skill** [§6.11, Rec1]: `SKILL.md` front matter `name` (≤64 lowercase letters, digits, hyphens; no leading, trailing or double hyphen; matches folder; no "anthropic"/"claude"; gerund form) and `description` (≤1,024 chars, third person, what and when); optional `license`, `compatibility` (≤500 chars), `metadata`, experimental `allowed-tools`; body under 5,000 tokens and 500 lines; references one level deep; fully qualified MCP tool names; check with `skills-ref validate ./folder`. Layout (verbatim):
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
Install: claude.ai Settings > Capabilities > "Code execution and file creation"; Customize > Skills > "+" > "Create skill" > "Upload a skill" (ZIP); Claude Code `.claude/skills/` (Pro or higher). Test "Which skills do you have?"; if absent, check code execution and `SKILL.md` at the ZIP's top level. The API container has no network, so generation stages run in Claude Code or via MCP.

**P12. IDs and files** [§10.1, §10.3]: scene `SC`+2 digits(+letter); beat `-B`+2 digits; shot `-SH`+3 digits in 10s (label letters from A at SH010, skipping I and O); cut `-C`+number of the shot it follows; bible `CH-`, `LOC-`, `PR-`, `MO-`, `WR-`, `LK-`, `PL-`, `CAM-`+name; state element+`.S`+2 digits; `SB-`+shot+letter; `PV-`+shot+`-V`+2 digits; `GJ-`+shot+`-T`+2 digits; `LOG-`+6 digits. File names `PROJECT_SCENE_SHOT_slug_JOB.ext` (`CATCH_SC06_SH140_blood-beads_GJ-T03.mp4`). Files (verbatim):
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

**P13. Shot record template** [E3] (exact field list): `id, label, scene, beats, source_lines, purpose, size, angle, lens_mm, movement, subjects[{state, position, facing, action}], withhold, props, physics, on_screen_text, duration_s, handles_s, start_state, end_state, cut_out, vfx, previs, previs_level, model_targets, status, locked`; §10.2 adds `overrides`, `pose`, `required`, `forbidden`, dialogue with channel, sound, text handedness, additions.

**Prior-system templates** [§1A]: VGoT rejects any shot missing character, background, relation, camera pose or lighting; FilmWorld states (character: identity, age, costume; location: place, season, weather, time; prop: condition) plus shot directives with an end state; CineCrew clip = narrative action (action, emotion, dialogue) → staging (shot type, move, lighting, `character_refs`, `set_ref`, `required_props`, `forbidden_props`, `continuity_link`) → render spec (keyframe prompt, video prompt, negative prompt, duration, fps, seed).

## 5. Checklists

**Validator, every stage** [§6.6]: V1 schema match; IDs unique, well-formed, resolving. V2 every source scene has a record; every line covered by a shot or omitted with a reason. V3 every character/prop/location in a shot is in the bible with a ledger state for that scene. V4 continuity of start/end states (scenes and shots) unless a line or cut record says otherwise. V5 beats fit duration; ≤2.5 spoken words/s. V6 on-screen text ≤3 words per sign or marked for compositing; in mirror-flagged scenes each text item has a handedness. V7 no emotion adjectives in performance fields. V8 every plant has a payoff and vice versa. V9 every job points to an existing shot and existing files. V10 durations sum to scene target ±10%; ≤1 main action unless `compound`. V11 IDs script-issued and pattern-matching; enums compared lower-cased. V12 additions flagged. V13 every extracted fact has a source line or quote the validator finds.

**Human checkpoints** [§6.9]: A scene list (5 min); B design theses and identity keys (15–30 min; correct one character in one sentence, "Revise only this character"); C one-line shot list per sequence (~10 min each); D flagged previs stills; E takes. Each addition answered "keep" or "cut".

**Per shot** (beyond the validator): consequences carried; `withhold`/`required`/`forbidden` honoured; overrides only; cut record with type; handles; previs level (greybox if framing-critical, pose if action-critical).

**Per asset**: alias list; 25–40-word identity key, no real-person likeness; new state ID and reference per look change, made at first appearance; ledger changes cite cause lines.

**Per job**: exact model name, input paradigm, compiled prompt, seed, cost, structured review, kept/rejected, log entry with input hashes. **Per tool fact** over a month old: re-check.

## 6. Saying it to AI models

- **Compile, don't paraphrase**: identity keys and the global look block pasted unchanged into every image and video prompt; never restate scene-level values in shot prompts (the unstaged-console sentence).
- **Never "looks like [actor]"**; use a written identity key.
- **State consequences** in every later shot and keyframe; generators keep the first state.
- **One shot per request.** Multi-shot prompts scored 7.9 lower (up to 22.8, Hailuo 2.3); Vidu and Kling 2.5 Turbo often returned one continuous shot; transition scores fell as shots per request rose (MiniMax H3 0.542 at 2, 0.383 at 5–6). Dissolves/wipes become hard cuts; J/L-cuts mostly fail.
- **Words do not hold framing**: director-worded framing gave heads 1.906× staged size, a compiled prompt 1.733×, a greybox 0.955× (with less action; a declared pose recovers part).
- **Action is every model's weak point** (action and emotional performance, camera-work appeal, motion realism); camera movement lost 31.1 points on average in action scenes; "no model wins on all". Small figures and crowded frames lose identity; walking while talking fails.
- **References per state**; extend from the original reference, not the last frame.
- FilmBench writes test prompts as shot lists with slotted tags (`@scene1`, `@role1`, `@prop1`); Boords `@`-mentions cast per frame (observations, not rules).
- **Screen playbacks**: generate small and grainy, composite onto the monitor.
- **For the breakdown LLM** [§6.10]: one term per concept throughout; strict templates with input/output example pairs; exact commands for fragile steps; nothing time-sensitive in instructions.

## 7. The Catch

**Intake** [E1]: ~9,200 words, 30 scenes. `## INT. …` headings and `=` title page/cards make a strict parser find zero scenes and drop `= THE CATCH` (l.488) and `= THE END` (l.1852); fix per P8. `@JUDE (V.O.)` "(in her ear)" (l.93–94) gets `channel: "radio"` (inference: Jude is below in the tunnel; device unnamed).

| Scene | Heading | Lines | Handling |
|---|---|---|---|
| SC01 | INT. MEDICAL FACTORY - LOADING TUNNEL - NIGHT | 10–70 | `> FADE IN:` = cut-in to SC01-SH010 |
| SC06 | INT. FREIGHT CAGE - CONTINUOUS | 198–299 | The fall |
| SC10 | INT. SAYE'S HOUSE - KITCHEN - BEFORE DAWN | 397–489 | Ends in black; title card `SC10-SH990`, type `card` |
| SC15 | INT. QUARANTINE - JUDE'S ROOM - CONTINUOUS (ON THE TABLET) | 838–867 | `presentation: "on_screen"`, host `PR-TABLET` in SC14 |
| SC30 | INT. QUARANTINE - IONA'S ROOM - NIGHT | 1814–1852 | `SC30-SH990` black, sound only; `SC30-SH995` card THE END |

**Ledger** [E2]: `PR-PUCK.S01` clipped under flask (SC04–SC06 to l.223; cause l.162); `.S02` clipped by Eli to the cage floor grid, hidden (SC06 l.224–258; revealed l.740); `.S03` spent, "burnt into the grid" (SC06 l.259 "CLACK" on; SC21 l.1219). `PR-FLASK.S02` clip empty, carried, sealed, in ship's cabinet (SC07–SC23); `.S03` gone (SC24 on; l.1418).

**Handedness** [E2]: from l.259 Iona, Eli, Jude are `turned`; after Iona's second turn (SC27 l.1563) Iona `original` (inference; reads RECEIVING l.1620–1622), Eli and Jude stay `turned` (Jude's scar l.408–411, ring "On his right hand" l.1779). `PR-MEAL-SEALED` turned (l.642); `CH-ANIMAL` turned in the ship world, later original, "turned with Iona". Rule: a sign, label or lateral detail (ring hand, scar side, steering wheel) shows mirrored when its element's handedness differs from the scene's `frame_handedness`; every text item in SC07–SC30 gets a computed orientation and C2's flip-or-composite choice.

**SC06-SH140** [E3] (label "6P", l.242–244, beat SC06-B08): medium wide, cage level across the cage, 24 mm, camera locked to the falling cage; Iona frame left, fingers in the grid; Jude frame right limp across Eli's arms; Eli behind Jude facing Iona; withhold Eli's right hand and `PR-PUCK.S02`; `PR-BLOOD-BEADS.S01` stays in every later shot's props until the cage stops; walls stream upward; 4 s + 1 s handles; end state "Iona's grip slipping; beads mid-air"; beads composited; previs `PV-SC06-SH140-V01` level 3 as control video (C4's `CATCH_SC06_SH14_cage_fall`). "CLACK / BLACK" is its own shot after hard cut `SC06-C140`, made in the edit.

**SC13 playback** [E4]: `SC13-SH200`, `screen_insert`, host `PR-MONITOR`, replays `SC06-B08`/`B09`, camera `CAM-SHAFT-TOP` (straight down), look `LK-CCTV`. Plant `PL-04` planted by `SC06-B09` (l.253 "He has one hand she cannot see", echoing l.224), paid off by SC13-SH200. Validator: replayed beats exist; replayed elements use the state at that moment (`PR-PUCK.S02`, not `.S03`); every SC06 shot in l.224–258 honours `withhold`. Production: re-render SC06 previs from the top-gate camera, generate small and grainy, composite (C1 Recipe 9). `MO-HANDEDNESS` logs this and Iona's "Our cage." (SC12 l.589).

**Flagged for the writer/user**: the "(in her ear)" device; `frame_handedness` per scene (director's call, never inferred); Iona's post-SC27 handedness (inference); confirm 30 scenes and odd lines (title cards, transitions, `(ON THE TABLET)`); slate convention; keep/cut each addition; checkpoint B keys. Test scenes: SC06, SC13, SC15.

## 8. Conflicts and open questions

- **Per-shot trade-off**: one shot per request helps structure and transitions but hurts match cuts, occlusion wipes and A/V sync (Wan 2.7 0.436 → 0.277); handled by shared geometry and lip-sync re-checks (R28–29), not one rule.
- **Greybox trade-off**: holds framing, delivers less action; pose declaration only partly recovers it.
- **Levels**: record levels are project, scene, beat, shot, job; "sequence" is a scene field and analysis list, not a record.
- **Cross-file terms**: A3's "continuity bible" = ledger, and A3 writes rows in YAML where this file says store JSON. A3's "12A" is a display label here (`SC12A` ID). C3's display form "13-04" and C4's `CATCH_SC06_SH14` must map onto this file's ID rules (C4's example becomes `SC06-SH140`).
- **Judgment defaults**: handles 0.5–1 s, ±10% tolerance, 3-round cap, stage list, context pack, portable subset, most validator checks.
- **Evidence limits**: Co-Director tested advertising (4 shots, 12 s), not drama; MLLM judge vs humans only α 0.47–0.59; the best full DramaChain chain scored 3.30, just above usable (3.0).
- **Unverified** [§11]: FDX spec; whether Movie Magic reads `screenplain` FDX; Movie Magic price; StudioBinder, Celtx, Filmustage, LTX Studio project and M Studio APIs; Flora's MCP tools; Kaiber; Katalist formats and "Veo 3.2"; Storyboarder.ai prices; Chinese short-drama platforms; full camera-report columns; whether consumer ChatGPT/Gemini web load skills; claude.ai ZIP limit; first Premiere with OTIO out of beta (Resolve claim secondary); Gemini `anyOf`/`$ref`; twelve 2026 papers plus ViMax, AniMaker, VideoClaw unread; steps-of-10 authority; letter skipping rests on a blog.
- **Moving targets**: claude.ai menus (Help Center vs developer page differ; follow the app); skills do not sync across API, Claude Code, claude.ai; Katalist and Higgsfield still list Sora 2.

## 9. Section map

- **§0**: evidence labels; who reads what; glossary.
- **§1A Research systems**: 22-system table (intermediate plan, consistency method, failures, evaluation); CutCraft, FilmBench, DramaChain findings.
- **§1B Formats and software**: Fountain syntax, FDX, breakdown colours, shot list, camera report, slates, Movie Magic, Filmustage, Flow, EDL, OTIO.
- **§1C Commercial platforms**: 14 platforms' inputs, outputs, API/MCP, prices; none exports its plan as data.
- **§2 Fourteen lessons** with evidence.
- **§3 Formats in practice**: input normalization, *The Catch* markup problem, outputs, which editor opens what.
- **§4 Tool per aim**; **§4A** costs and difficulty.
- **§5 Decision rules** R1–R33.
- **§6 Reliable pipeline**: 6.1 stages; 6.2 chunks, context pack; 6.3 single source; 6.4 structured outputs, portable subset; 6.5 IDs; 6.6 validator; 6.7 self-critique; 6.8 drift; 6.9 checkpoints, re-runs; 6.10 instruction writing; 6.11 Agent Skill.
- **§7 Recipes 1–8**: install, intake, analysis/design, validator errors, export, commercial comparison, bad clip, testing.
- **§8 Failure modes**: 24-row table with workarounds.
- **§9 Worked examples**: E1 intake; E2 ledger and handedness; E3 full SC06-SH140 JSON; E4 SC13 playback.
- **§10 Data model**: 10.1 IDs, file names, field authority, inheritance; 10.2 entity table; 10.3 files.
- **§11 Could not verify**; **§12 Sources** S1–S78 and fact-check corrections.
