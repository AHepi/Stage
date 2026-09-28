# Digest D2: Whole-work adaptation and scope (27 Sept 2026)

Source: `research/D2_whole_work_adaptation_plan.md` (526 lines, fact-checked 2026-09-27). Brackets: R# = the file's decision rule (§4); P# = principle (§2); M# = macro-pass step (§5); CF# = cardinal function; ST# = strand. Evidence labels: **[V]** verified at source, **[U]** unverified, **[J]** the file's judgment or arithmetic. All quotations from *The Catch* and *The Long Places*, line and paragraph references, counts and table sums were re-checked by script.

## 1. Scope

1. Runs once, after C5 stage 1 (story analysis) and before stage 2 (bible): fixes format (`short`, `feature`, `limited_series`), runtime in seconds, scene and shot budgets, and which strands, chapters and scenes survive.
2. Produces a whole-work event list, strands, cardinal functions, a keep/cut table, series rules for recurring devices, episode or reduction rules, and a one-line-per-scene step outline, saved as `adaptation_plan.json`.
3. Ends at **checkpoint M** (user approval; scene IDs lock). Worked cases: *The Catch* runs about 35 min (32–44) and is cut to 20; *The Long Places* is planned as a 100-min feature, a 6×48-min series and a 15-min short.

**Terms.** *Cardinal function* = event the story cannot lose (Barthes); *catalyser* = any other event; *strand* = line of events following one character or question; *deletion test* = "if this were gone, which later events lose their cause, setup or meaning?"; *step outline* = one line per planned scene; *fold* = move a passage's content into a neighbour as a shot, line or prop; *composite* = two scenes or characters merged; *series rule* = one decision for a recurring device; *charge* = + or − of a value; *generation factor* = generated ÷ finished seconds (C1's typical 2 overshoot × 4 retakes = 8); *validator* = script or spreadsheet that does the sums.

## 2. Rules

**Format and runtime**
1. [R1, P7] If the user names no format, then offer two or three independent macro plans, each with runtime, scene and shot budgets, cost and review hours, because format fixes every later budget and choosing is the user's call (C5 R14).
2. [R24] If M4 must propose options, then choose them from natural runtime: ≤ ~45 min → as written, a trimmed cut under the cap, expansion only if asked; ~45–150 min → a feature and an R19 short; > ~150 min or > ~8 strands → a series (episodes ≈ natural runtime ÷ episode length), a strand-deleting feature and a short, because the options must span the realistic range and one must fit the user's money and hours [J].
3. [R2, P2] If the source is a screenplay, then estimate runtime three ways (pages ÷ 1.1; A2 line and action defaults on three sample scenes extrapolated by word counts; beats × 14 s) and report low, central, high, because page ≈ minute misses by more than 5% four times in five [V, Follows].
4. [R3] If the source is prose, then natural runtime = candidate scenes (A3 §7.9 on two sample chapters, averaged, × chapter count) × 2–2.5 min, because words per minute vary too much with style.
5. [R4] If festival or award eligibility as a short matters, then keep the total with credits ≤ 38 min (2,280 s), read the festival's own limit (Sundance 2027: under 50 min) and AI rules, and flag that an AI film may fit neither the Academy's live-action nor animation definition, because rules count credits, differ, and define categories by how pictures were made.
6. [R5] If natural runtime exceeds the target by more than ~1.5×, then expect to delete a strand or change format, because trims and merges recovered only about a third of *The Catch* (35 → 24 min) [J].
7. [R6] If natural runtime is under ~⅔ of the target, then expand by dramatizing the source's own summaries (A3 §7.4) and label every invented event `invention`, because expansion is invention (A3 P2, rule 24; *Arrival* added the landing).

**Budgets**
8. [R7] If the runtime target is set, then scene budget = runtime ÷ average scene length and shot budget = runtime ÷ target ASL, because cost and review time scale with shots and asset work with scenes and sets.
9. [R8] If candidate scenes exceed the budget, then rank by A3's five tests and remove from the bottom, never a passage passing test 1 (cardinal function), because the cardinal functions are the story.
10. [R9] If step targets miss `runtime_target_s` by more than ±10% (credits and cards included), then revise before checkpoint M, because C5's validator uses the same default per scene (C5 §6.6 check 10 [J]; R27).

**Strands and cuts**
11. [R10, P4] If cutting to a cap, then cut in order, stopping when it fits: (1) trim inside scenes; (2) merge consecutive same-place-and-time scenes; (3) fold low scorers; (4) delete a strand carrying no spine cardinal function; (5) drop a set piece, because each step changes the story more.
12. [R11, P5] If a strand is deleted, then run the deletion test on each of its events and move every dependency (line, prop, insert, image) into a kept scene, logged with source lines, because a cut strand leaves orphan payoffs.
13. [R12] If two minor characters do one job, then consider a composite character, logged, because each character costs screen time, a reference pack and a voice (*Remains of the Day*'s Lewis [V]).
14. [R13] If a merge would put an effect before its cause, then reject it or reorder with logged line changes, because causal order outranks runtime.

**Recurring devices**
15. [R14, P6] If a device recurs, then list every occurrence (by text search), choose one policy for the whole work, and save the first occurrence's setup as a template (A3 rule 23), because scene-by-scene choices drift.
16. [R15] If a refrain repeats with one detail changed, then keep everything else identical and make the change readable on screen, because the change is the information.
17. [R16] If the source later identifies a framing text's unnamed writer, then decide that text's voice with the whole work in view, because an early voice can contradict or spoil the reveal.

**Series and shorts**
18. [R17] If the format is a series, then break episodes at major turns, not equal word counts; each needs a value arc that ends at a different charge and an ending turn, because an episode is a story unit and the turn brings viewers back [J].
19. [R18] If an episode pays off a plant from an earlier one, then list the plant in its recap, built from approved shots, because recaps cost no new generation.
20. [R19] If a short is cut from a long work, then choose one reduction: (a) one strand; (b) a bookend with a minimal bridge; (c) one chapter; prefer (b) when the ending pays off the opening, because a short holds one value arc.
21. [R20] If a bookend skips the middle, then the bridge carries the time gap with a story-world marker and imports every plant the ending needs (`flashback_import`), because the audience never saw the middle.

**Process**
22. [R21] If the plan is drafted, then show a one-page summary and step outline and lock IDs only after "approved", because every later file hangs on the scene list (C5 R1).
23. [R22] If format or runtime changes after approval, then re-run M4–M8 and mark changed steps; never renumber (`OMITTED`, letter suffixes; A3 §5.1, C5 §10.1), because approved downstream work must survive.
24. [R23, P8] If the LLM proposes a cut, then it lists cardinal functions touched (must be none), dependencies moved and seconds saved, and the validator re-sums, because LLMs re-attach deleted events and misreport coverage (C5 R25).

## 3. Breakdown fields

Enums lowercase `snake_case`; empty = `"none"`, empty list `[]`; each field carries C5's authority mark (`extracted`, `authored`, `derived`).

| level | field_name | meaning | allowed values / example |
|---|---|---|---|
| film | `format` | Kind of finished work | `short` \| `feature` \| `limited_series` |
| film | `runtime_target_s` | Target incl. credits (renames C5's unitless `runtime_target`) | `1200` |
| film | `runtime_estimate_s` | Natural runtime range, derived | `{low: 1920, central: 2100, high: 2640, method}` |
| film | `constraints` | M0 answers | `{max_runtime_s, budget_usd, review_hours, festival}` |
| film | `scene_budget`, `shot_budget` | Derived budgets | `{scenes: 25, avg_scene_s: 46}`; `{shots: 300, target_asl_s: 4}` |
| film | `strands[]` | `id`, `name`, `chapters_or_scenes`, `cardinal_ids`, `feeds[]`, `decision`, `reason`, `seconds` | decision: `keep` \| `compress` \| `composite` \| `fold` \| `cut` |
| film | `strands_kept`, `strands_cut` | ID lists derived from `strands[]` | `["ST1","ST2"]` |
| film | `cardinal_functions[]` | `id`, `event`, `source_refs`, `depends_on_it[]` | `CF11`, "She deletes the way home." |
| film | `series_rules[]` | `id`, `device`, `occurrences[]`, `policy`, `template_setup`, `varies`, `notes` | `open_only` \| `open_and_close` \| `every_return` \| `episode_cold_open` \| `template_refrain` |
| film | `pov_plan` | Default POV and declared breaks | `{default: "NILAY", breaks: [...]}` |
| film | `episodes[]` | `id`, `chapters`, `runtime_target_s`, `value_arc {value, open, close}`, `ending_turn`, `recap_plants[]` | series only, else `[]` |
| film | `open_questions[]` | One decision each for checkpoint M | `["Replacement image for the Figure's motive once Nell is cut?"]` |
| film | `macro_checkpoint` | Approval record | `{status: approved \| pending, version, date}` |
| scene | `step_id`, `source_refs`, `strand_ids`, `cardinal_ids` | Step-outline links | `ch14.p012-p035`; `L1376-1427` |
| scene | `status`, `heading`, `event`, `compression_ops[]` | Plays or not; heading; one-line event; ops applied | `active` \| `omitted`; `["trim"]` |
| scene | `five_test`, `a3_rule` | A3 §7.9 scores; rule applied | `[1,1,0,1,1]`; `own_scene` \| `fold` \| `cut` |
| scene | `target_duration` (C5), `merged_into` | Seconds; where an `OMITTED` scene went | `85`; `SC18` |
| log | `adaptation_log[]` | `op`, `what`, `from`, `to`, `reason` | `{op: "move_plant", what: "oxygen cylinder", from: "L498", to: "SC14"}` |
| log | `op` | Operation | `trim` \| `merge_scenes` \| `fold_into` \| `composite_character` \| `move_line` \| `move_plant` \| `delete_strand` \| `reorder` \| `invention` \| `replace` \| `flashback_import` \| `lost_resonance` |

## 4. Procedures

**Macro pass** [§5]. Attach the source with numbered lines (screenplay) or numbered paragraphs `chNN.pNNN` (prose: non-empty lines per chapter, letters included, section breaks excluded). Without code: one step per chat message, save each answer (`M1_events.md` …), paste any seconds column into a spreadsheet and let it add; never accept a total the LLM typed; correct with "Revise only [item]".

1. **M0 Constraints.** *Prompt:* "Ask me, one at a time: format wish; maximum runtime; money for generation; hours I can spend reviewing; any festival target. Record my answers under `constraints`."
2. **M1 Event list.** *Prompt:* "Read the whole source twice. List every event in one or two past-tense sentences, no psychology, each with its source reference (screenplay: line range; prose: chapter.paragraph such as ch02.p024). Give two orders: the order told, and story-time order. Mark each event `cardinal` or `catalyser` by the deletion test, and for each cardinal event name the later events that depend on it."
3. **M2 Strands.** *Prompt:* "Group the events into strands. For each strand give its events, the chapters or scenes it occupies, the cardinal functions it carries, and every point where it feeds another strand (a plant, an object, a piece of knowledge)."
4. **M3 Natural runtime.** Screenplay: three methods (step 10 below). Prose: R3. Script does the sums.
5. **M4 Format options.** *Prompt:* "Propose two or three independent macro plans within my constraints, chosen by R24: format, runtime target in seconds, scene and shot budgets, strands kept, compressed and cut, and what the audience loses. Do not argue for one." Script adds generated seconds (runtime × 8), money at C1 tiers (~$0.07 / $0.17 / $0.45 per generated second; re-check prices older than 30 days) and review hours (5–10 min a shot). Worked: 1,200 s × 8 = 9,600 s; × $0.07 = $672; 300 shots → 25–50 h.
6. **M5 Keep/cut table.** One row per strand and per chapter or sequence: decision, reason, cardinal functions touched, dependencies moved, seconds.
7. **M6 Step outline.** *Prompt:* "Write the step outline for the chosen plan: one line per scene with heading, one-line event, source references, strand and cardinal-function IDs, A3's five-test scores and §7.9 rule, target seconds, compression operations." Validator runs §5 checklist.
8. **M7 Series and episode rules** (R14–R18).
9. **M8 Checkpoint M.** Summary, keep/cut table, step outline; "approved" or one-item corrections; script locks IDs and writes the log; then A3 §7 (kept passages only) and C5 stages 2–9. Time [J]: ~1 h for a screenplay, 2–4 h for a novel.

10. **Screenplay runtime** [§6]. (a) pages ÷ 1.1 (Follows' ratio includes a feature's median 4.3-min credit crawl; for a short, story ≈ 0.87 min a page). (b) Dialogue = words ÷ 2.5 + 0.5 s per speech; action from A2 defaults on three sample scenes → seconds per action word → apply to all scenes. (c) Beats × 14 s on scenes A2 has beaten; use as an upper bound. Record `runtime_estimate_s`.

11. **Cutting to a cap** [§7]: apply R10 in order; for each merge check R13; for a deleted strand list every dependency with line refs and its destination; show "as written / target / operation" per scene or group; add titles and credits; state what the audience loses.

**Template, `adaptation_plan.json`** (reproduced exactly from §9):

```json
{
  "project_id": "CATCH",
  "format": "short",
  "runtime_target_s": 1200,
  "constraints": {"max_runtime_s": 1200, "budget_usd": "none", "review_hours": "none", "festival": "none"},
  "runtime_estimate_s": {"low": 1920, "central": 2100, "high": 2640,
    "method": "pages/1.1; A2 defaults on SC06 SC10 SC13 extrapolated; beats x 14 s"},
  "scene_budget": {"scenes": 25, "avg_scene_s": 46},
  "shot_budget": {"shots": 300, "target_asl_s": 4},
  "strands": [
    {"id": "ST_NELL", "name": "Nell Rowan", "chapters_or_scenes": ["SC17", "SC18", "SC20", "SC23", "SC24", "SC28"],
     "cardinal_ids": [], "feeds": ["cell count SC20", "Figure motive SC23", "Saye guilt SC18", "Saye message SC24"],
     "decision": "cut", "reason": "20-minute cap; R10 step 4", "seconds": -120}
  ],
  "strands_kept": ["ST_IONA_ELI", "ST_FIGURE", "ST_SAYE"],
  "strands_cut": ["ST_NELL"],
  "cardinal_functions": [
    {"id": "CF11", "event": "She deletes the way home.", "source_refs": ["L1412"], "depends_on_it": ["CF12", "CF13"]}
  ],
  "series_rules": [
    {"id": "SR01", "device": "Are we going to be all right?", "occurrences": ["SC09", "SC23", "SC29"],
     "policy": "every_return", "template_setup": "barrier between the siblings (A2)", "varies": "speaker",
     "notes": "L390 Iona asks; L1352 Eli asks; L1788 callback only: \"In the car-\" / \"Yes.\""}
  ],
  "pov_plan": {"default": "IONA", "breaks": []},
  "episodes": [],
  "step_outline": [
    {"step_id": "SC17", "status": "omitted", "merged_into": "SC18"},
    {"step_id": "SC18", "heading": "INT. MEDICAL FACTORY - THE PASSAGE (RECEIVING ROOM) - DAY",
     "event": "Saye shows the returned camera's footage while sealing Iona's suit; two engines for three.",
     "source_refs": ["L912-999", "L1000-1097"], "strand_ids": ["ST_IONA_ELI", "ST_SAYE"],
     "cardinal_ids": ["CF08"], "five_test": [1, 1, 1, 1, 0], "a3_rule": "own_scene",
     "target_duration": 110, "compression_ops": ["merge_scenes", "trim"]}
  ],
  "adaptation_log": [
    {"op": "move_plant", "what": "oxygen cylinder", "from": "L498", "to": "SC14", "reason": "SC11 cut; SC16 needs it"}
  ],
  "open_questions": ["Replacement image for the Figure's motive once Nell is cut?"],
  "macro_checkpoint": {"status": "pending", "version": 1, "date": "none"}
}
```

**Evidence behind the numbers.** Follows (~2,870 scripts): "One page does not equal one minute - it equals about 55 seconds"; median ratio 1.1; 18.2% within 0.95–1.05 [V]. McKee: 40–60 scenes, "a scene lasts two and a half minutes... for every one-minute scene there's a four-minute scene" [V]. Follows (12,309 mostly unproduced scripts): "110 scenes" [V]. Academy short: "40 minutes or less, including all credits" [V]. Network hour ≈ 44 min, 44–45 pages; streaming hour 55–65 pages [V]. Cases: novella → *Arrival* 116 min (added the landing); short story (~10,000 words [U]) → *Brokeback Mountain* 134 min; novel → *Remains of the Day* 134 min (composite Lewis); novel → *Normal People* 12 × 23–34 min, reordered chronologically [V].

## 5. Checklists

**Before checkpoint M** [§10]:
- Every kept cardinal function is in a step.
- Step targets sum to `runtime_target_s` ±10%, credits and cards included.
- Every step cites sources or is labelled `invention`.
- Every deleted strand's dependencies are moved or accepted as losses.
- No merge puts an effect before its cause (R13).
- Every recurring device has a series rule listing all occurrences.
- Series: each episode has a value arc that changes charge, an ending turn, and recap plants.
- Short: one reduction type; every plant the ending needs is present.
- The summary states what the audience loses.
- Screenplay: `OMITTED` and `merged_into` set; no renumbering.
- Every quoted line and series-rule occurrence is found verbatim by text search.
- If a festival or award is a goal: R4 limit, festival limit and AI-category flag shown.

**After:** IDs locked; log written; A3 §7 runs only on kept passages.

**Failure signs** [§11]: ~140 scenes from chapter-by-chapter prose (run M1–M6 first); orphan payoff (SC16's cylinder after SC11 cut → `move_plant`); effect before cause (SC20 + SC23); a CF with no step; step outline citing a cut strand (validator checks `strands_cut`); refrain shot differently (template setup); runtime approved without cost; phantom occurrence (a series rule citing a scene where the device is absent → script writes `occurrences[]`).

## 6. Saying it to AI models

- One step per call, source attached with numbered references; ask for tables, not totals; a script or spreadsheet sums (C5 R23).
- For options, ask for two or three independent plans and "Do not argue for one" (C5 R14).
- For every proposed cut, require the list "cardinal functions touched (must be none), dependencies moved, seconds saved" (R23); reject a claim that "everything is covered" unless the validator agrees (C5 R25).
- Never let the LLM write `occurrences[]`, line ranges or counts; a text search does (C5 R23).
- Correct with "Revise only step N", never "improve your answer" (C5 R12).

## 7. The Catch

**Decisions made (proposed, awaiting checkpoint M)** [§6–§7]:
- Counts: 30 scenes; 221 speeches, 1,579 dialogue words; ~543–545 action paragraphs, ~7,091–7,097 words; 41.7 pages by A3's line model.
- Natural runtime **about 35 min (32–44)** plus ~1 min titles: pages ÷ 1.1 ≈ 38 (≈ 36 story); A2 defaults 1,916–2,304 s (0.166–0.220 s per action word); beats × 14 s ≈ 44 (upper bound). `runtime_estimate_s {1920, 2100, 2640}`.
- C1's 20-min costs scale by ~1.75 (1.6–2.2): ~$3,100 typical; $2,600–7,900 range; ~525 shots; 45–90 review hours [J].
- Options: (1) as written ~35 min, 30 scenes; (2) trims and merges only ~24 min + credits, all strands, 25 active scenes; (3) 20-min cap: 1,160 s + 40 s titles = 1,200 s.
- Cardinal functions CF01–CF15 (SC01 brakes gone; SC06 the hidden hand and "A hard metal CLACK."; SC07 empty clip; SC10 "Not mint."; SC12 "A turn." / "Our cage."; SC13 "You did that." / "Yes."; SC15–16 cracked strip; SC18 two engines for three; SC21 "IONA VALE."; SC23 "Are we going to be all right?" / "I don't know." / "Go."; SC24 "She deletes the way home."; SC25 chest and animal; SC26–27 turn and crossing; SC28 "on the wrong side of his face"; SC29 "His wedding ring. On his right hand.").
- Option 3 operations: trim SC01–05 to 110 s (keep "She gives Eli one shoe. He leaves the other.", paid off by "One shoe." in SC21); merge SC08 → SC09; cut SC11 (move Saye's "I inspect their trials..." line to SC12; move the oxygen-cylinder plant to an SC14 insert because SC16 needs it); composite SC17 → SC18; fold SC19 → SC20 and SC22 → SC21; delete the Nell strand (saves ~75–120 s).
- Nell's five dependencies: the cell count (hold rack and "second black cell" pictures longer); Eli's exit (Figure uses Eli's bed); the Figure's motive image (the drawing on "Nell's shelf", SC23: no kept carrier); Saye's "Did it take anyone you sent?" (cut); SC24's recorded "They're here. Nell is here." (trim to "They're here.").
- The SC20 + SC23 merge fails R13 (the courier's round trip through SC21 causes SC23); only via a reorder costing three inventions for ~25 s.
- SR01 "Are we going to be all right?": SC09 (Iona asks, l.390), SC23 (Eli asks, l.1352), SC29 callback ("In the car-" / "Yes.", l.1788); policy `every_return`, varies by speaker. (An earlier draft wrongly listed SC13.)

**Flagged for the user:** choose Option 1, 2 or 3 (recommendation [J]: Option 2 keeps the film whole; 3 only for a hard cap); if 3, a replacement for the Figure's motive image (any is an `invention`); if festival or award eligibility matters, ≤ 2,280 s, and the AI-category question (§3.3); whether the lost Saye guilt beat is acceptable.

## 8. Conflicts and open questions

- **C1 vs A3:** C1 costed 1,200 s; A3 measured 42–44 pages. Resolved: ~2,100 s; scale C1 by `central / 1200`.
- **C5 `runtime_target`** has no unit → rename `runtime_target_s`.
- **Checkpoint order:** screenplay: C5 checkpoint A (parsed scene list) → stage 1 → M (only `OMITTED`/`merged_into`, no renumbering; D1 §10.5 follows the locked list). Prose: A confirms paragraph numbering and rights (D4 rule 4); scene IDs first lock at M. D14's checkpoint T (thin sources) precedes M.
- **A3 Ex5** calls the threshold refrain word for word; its minute figure changes (18, 19, 20, 18) and XI adds a lead-in sentence.
- **A3 rule 21 and Plan C:** the ending hints the opening keeper is Nilay; keep hands unmarked unless the user decides.
- **D13** reports 1,926–2,309 s (central 2,118) vs D2's 1,916–2,304 (2,100): rounding; record D2's.
- **D10:** slow-cinema Plan A needs ~400–500 shots, not 1,200–1,500; ASL is a checkpoint-M style choice.
- **Plan A `move_line`:** Marques says "Two clocks is an anecdote" *to* Priska ("I am sorry, Doctor Vogel", ch10.p020); in Priska's mouth it becomes her own doubt. Alternative: give it to ST11.
- **Awards:** Academy live action = "practical photographic techniques"; animation = "by any human means"; 99th rules require human-authored screenplays and human performances and may ask about AI use. Category fit of an AI film is unresolved [J].
- **Unverified:** exact word counts of "Brokeback Mountain" and "Story of Your Life"; festival limits beyond Sundance 2027; the 99th short-film PDF (download refused; 40-min rule [U] for that year beyond a summary); Plans A–C costs (C1 model, stale after 30 days).
- ***The Long Places* choices:** Plan A (100 min, 48 scenes, 1,200–1,500 shots, $3,400–21,600), B (6 × ~48 min, ~120 scenes, $9,700–62,300) or C (15 min, 10 scenes + flashback, $500–3,200); letter policy (`open_and_close` for feature and short, `episode_cold_open` for series); letter II carried as humming only (R16); keep Priska or a nameless witness; Emre's face; "Emre Arat kept here" insert; ASL.

## 9. Section map

| § | Content |
|---|---|
| Header | Purpose, evidence labels, place in pipeline |
| 1 | Glossary (format, cardinal function, catalyser, strand, charge, generation factor, validator, …) |
| 2 | Principles P1–P8 |
| 3.1–3.4 | Adaptation cases; page/scene/minute data; format lengths, Academy and Sundance rules, AI category fit; McKee's adaptation method |
| 4 | Rules R1–R24 (R24 placed with format rules) |
| 5 | Macro pass M0–M8 with prompts; running it without code |
| 6 | *The Catch* runtime: three methods, answer, cost scaling |
| 7 | *The Catch* at 20 min: CF01–CF15, Option 3 table, Nell dependencies, failed SC20+SC23 merge |
| 8.1–8.5 | *The Long Places*: counts, strands ST1–ST11, CF01–CF10, series rules, Plans A, B, C |
| 9 | Fields and the `adaptation_plan.json` template |
| 10 | Checklists |
| 11 | Failure modes |
| 12 | Conflicts and open questions |
| Sources | S1–S19 web; library files; test sources |
