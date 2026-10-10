# Digest D7: Judging a breakdown: rubric, gold scenes, review routine (28 Sept 2026)

Source: `research/D7_breakdown_quality_rubric.md` (fact-checked 28 Sept 2026). Brackets: R*n* = D7 §9 decision rule; § = D7 section; FID-1 etc. = merged checks (§3.2), stored as `fid_1`. Evidence: **[V]** checked at the source, **[U]** unverified, **[J]** judgment. Nearly every number (1–4 scale, 10% sample, pass marks, 80% detection) is [J], a starting value for calibration to move.

## 1. Scope

1. One acceptance test per scene: 275 checklist items from A1–C5 merged into 71 checks in nine dimensions, each check tagged `code` (script), `ask` (yes/no LLM question quoting records) or `human`, each dimension scored 1–4 against written anchors.
2. Which shots get read (every key, must-keep and turning-point shot plus a seeded 10% draw), how scores add up to `pass` / `revise` / `escalate`, and four gold scenes with seeded twins replayed after every pipeline change.
3. A ten-question review sheet the non-expert user answers from `exports/breakdown.md`, a calibration routine (two LLMs plus the user), and a worked SC13 example showing which check catches each planted fault.

**Terms.** *Finding* = `{record_id, check, severity, evidence, fix}`; *blocking* = a viewer would misread the story, continuity would break, or a generation would be wasted, else *minor*. *Gold scene* = hand-checked must-have / must-not / variant lists; *seeded twin* = a copy with planted faults. *Key scene* = D16 `structure_role` not `none`, or a gold scene. *Sign test* (A2) = the value's charge flips sign at the turn (+ to ++ is not a turn). *Error* stops the rubric; *flag* enters it as a finding (§4.1).

## 2. Rules

**Gate and tagging**
1. [R1] If the validator reports any error, then do not start the rubric, because scores on a broken file measure the break (C5 P5 = C5 Recipe 4).
2. [§4.1] If a script check fails on schema, IDs, coverage, a missing quote, bible or ledger entry, a broken state chain or a hard model limit (V1–V6, V9, V11, V13), then it is an error; any other script result (budgets, eyelines, rhythm, totals, additions, linter, estimate) is a flag scored as a finding, because planted faults like two push-ins must still be scorable.
3. [R2] If a check is arithmetic, a count, a string match or an ID lookup, then tag it `code`, because code grading is "Fastest and most reliable" (Anthropic) [V] and an LLM scorer "re-attached" a deleted event (C5 R25).
4. [R3] If a check needs judgment, then ask a yes/no question naming and quoting a record ("Does any shot citing l.798 show Iona's palm?"), because open questions fail (C5 R11).
5. [R4] If a finding has no quoted evidence, then drop it, because unanchored findings are invented problems [J].
6. [§2] If a model wrote the breakdown, then review with a different model or a fresh session, because of "self-enhancement" bias (Zheng et al.) and Anthropic's "Generally best practice" advice [V].

**Sampling and scoring**
7. [R5] If a shot is `key` or `must_keep`, or covers a `turning_point: yes` beat, then always read it, because a 10% draw would miss the shots that decide the scene [J].
8. [§5.1] If a shot is `normal`, then it enters a draw of 10% of the rest (rounded up, at least 2) seeded by scene ID plus round (`SC13:r0`), because replays must match and each fix round must read fresh shots [J].
9. [R6] If a drawn shot has a blocking finding, then draw 10% more; if again, then read every shot [J].
10. [§4.1] If a finding matches checks in two dimensions, then count it once, in the first in §3 order (FID, DRA, VIS, CON, RES, FEA, EST, REA, DOW).
11. [R7, §5.2] If no errors, FID/DRA/CON/FEA ≥ 3, no other < 2 and mean ≥ 3.0, then `pass`; otherwise `revise`, because upstream errors are "re-expressed downstream, not repaired" (C5 lesson 13).
12. [R8] If a finding survives three rounds or needs a story decision, then `escalate` with one question to the user, because repair gains roughly halve each round (C5 R13).

**Gold and replay**
13. [R9] If the user's view of an anchor changes, then rewrite it, bump `rubric_version` and replay, because "grading outputs helps users define criteria" (Shankar et al.) [V].
14. [R10] If library files disagree about a gold scene, then record the choice in `resolved_conflicts` and keep the other as a variant if it meets every must-have [J].
15. [R11] If a gold entry cites the source, then store the D14 block ID and quoted words, because normalization can renumber lines [J].
16. [§6.6] If an instruction, rule, rubric or reviewer model changes, then replay four golds and four twins and undo the change if a must-have is lost, a must-not trips, a score falls or fewer faults are caught (C5 R32); a reviewer missing any blocking seeded fault or over 20% of minor ones (now: 2 of 3 required) reviews nothing real [J].

**User and calibration**
17. [R12] If a scene is a key scene, then the user answers all ten questions; otherwise questions 1–3 [J].
18. [R13] If the user answers `unsure`, then the LLM answers that row's question with quotes and the user answers again; `unsure` never lowers a score [J].
19. [§7] If the user answers `no` to question 5, 7 or 8, then it becomes a finding to verify against the source, not a vote (principle 3; C5 R14).
20. [R14] If a pack goes into a second app, then turn training off first and never use free Google AI Studio (D1 rule 9).
21. [§8] If two LLMs differ by two or more, then ask the user one yes/no question; never let them debate, because debate "significantly underperforms simple self-consistency using majority voting" (Huang et al., reasoning tasks) [V].
22. [§8] If an LLM compares two versions, then run both orders and keep only a surviving preference, because rankings "can be easily hacked by simply altering their order" (Wang et al.) [V].
23. [§8] If the user differs from both LLMs by two or more on VIS, RES or REA, then the user's score stands and becomes an anchor example; `rubric_version` goes up.
24. [R15] If LLM–user α stays below 0.667 on a taste dimension, then the user keeps scoring it, because Co-Director's human raters agreed only at α 0.578–0.641 [V; conclusion J].

## 3. Breakdown fields

Enums lowercase `snake_case`; empty = `"none"`; (derived) = written only by script.

| Level | field_name | Meaning | Allowed values / example |
|---|---|---|---|
| film | `rubric_version` | Rubric text that scored the project | `d7_v1`, `d7_v2` |
| film | `reviewer_models` | Exact reviewer model names (tells a model change from a rubric change; C5 R22) | list of strings |
| film | `gold_set` | Gold and twin files replayed after changes | `gold/SC13.gold.json`, … |
| film | `acceptance` (derived) | Film verdict with each dimension's median and minimum | `accepted` \| `not_yet` |
| film | `calibration[]` | Scene, reviewers, scores, resolutions, alpha, anchor changes, date | object list (§4 template) |
| scene.review | `rubric_version` | Version used for these scores; different versions are not compared | `d7_v1` |
| scene.review | `rubric_scores` | Score per dimension: `fidelity`, `dramatic_accuracy`, `visual_storytelling`, `continuity`, `restraint`, `feasibility`, `estimate`, `readability`, `downstream_readiness` | integers 1–4 |
| scene.review | `sample_shots` (derived) | Shots read | shot IDs |
| scene.review | `sample_seed` (derived) | Scene ID plus fix round | `SC13:r0` |
| scene.review | `findings[]` | `id`, `record_id`, `check`, `dimension`, `severity`, `evidence` (quote, line, block ID), `fix`, `found_by`, `status` | severity `blocking` \| `minor`; found_by `validator` \| `reviewer_a` \| `reviewer_b` \| `user`; status `open` \| `fixed` \| `wont_fix` |
| scene.review | `verdict` | Outcome | `pass` \| `revise` \| `escalate` |
| scene.review | `round` | Fix rounds so far | `0`–`3` |
| scene.review | `review_sheet` | The user's ten answers and notes | `yes` \| `no` \| `unsure` |
| scene | `gold` | Scene is a gold reference | `yes` \| `no` |
| scene | `key_scene` (derived) | User answers the whole sheet | `yes` \| `no` |
| shot | `shot_role` | A2's role (C5 beat key-shot flag derived from it) | `key` \| `must_keep` \| `normal` |
| beat | `turning_point` | Beat where a value changes sign (A2; C5 beat flag) | `yes` \| `no` |
| twin | `seeded_faults[]` | `fault_id`, `record_id`, `description`, `expected_check`, `severity` | object list |

## 4. Procedures

**P1. Review one scene** [§10 Recipe 2; user time 10–15 min]
1. Say: "Run the validator on SC13. If clean, draw the D7 sample, score SC13 with rubric [version], list findings as record, check, severity, quote, fix, and write the review sheet."
2. The script draws the sample (rules 7–9); a different model answers every `ask` check and scores the nine dimensions.
3. Read `exports/breakdown.md`: the "Key shots" list first, then one plain line per shot. Answer the ten questions (§5) with `yes`, `no` or `unsure`, adding a note to any unwanted answer.
4. If the verdict is `revise`, say: "Fix only these findings, change nothing else, re-run the validator, and re-score the affected dimensions."
5. After three failed rounds, the scene is `escalate`: answer the one question the LLM asks.

**Anchors (all dimensions)** [§4.1]: **4** no findings and the positive evidence of D7 §4.2 present (e.g. VIS: each key shot its beat's strongest image with a landing face); **3** at most two minor findings, none on a key or must-keep shot; **2** one blocking finding, or any finding on a key or must-keep shot, or three or more minor; **1** two or more blocking findings, or the dimension's core record missing.

**P2. Build the gold set** [Recipe 1; once, 2–3 h reading]
1. Say: "Build gold files for SC06, SC13, SC15 and LONGPL SC01 from D7 Section 6 and the library's worked examples (A1 Ex3, A2 §12, A3 Ex2 and Ex5, A4 WE1–WE2, B1 §10.4–10.5 and Ex2–4, B3 §8.6, B5 Ex3, C3 Ex5, C5 E3–E4). Every must-have cites a source block ID and the quoted words. List every disagreement between library files."
2. Read each must-have beside its quoted line; answer each disagreement.
3. Say: "Make the seeded twins from D7 Section 6 and lock all eight files."

**P3. Calibrate** [Recipe 3; about 1 h; before the first real run on the SC13 twin, after every rubric change, then one scene in ten]
1. Say: "Make a review pack for the SC13 twin: the scene file, its source lines, D7 Sections 3–5 and the gold file, with the instruction to score all nine dimensions, reasoning first, and to list findings with quotes."
2. Paste the pack into a new chat in a second app (D1 §5 compares them) and into a new chat in your usual app. First turn off model training in the second app (D1 §8; never free Google AI Studio). Answer the review sheet yourself meanwhile, without looking at either reply.
3. Paste both replies back and say: "Compare the three scorings by D7 Section 8 and ask me only the questions it needs."
4. Answer them, then say: "Record the calibration and update the anchors I changed." If you disagree with a taste score, say why in one sentence; your score stands and becomes an anchor example.
5. After ten calibrated scenes the LLM computes α by script: `pip install krippendorff`; `krippendorff.alpha(reliability_data=…, level_of_measurement="ordinal")` (default "interval") [V]. α ≥ 0.800: LLM scores, user reads findings; 0.667–0.800: user checks flagged findings; below: user scores. Until then, or if α is unstable: LLM within one point of the user on ≥ 90% of scored dimensions over ten scenes, and no missed blocking finding [J].

**P4. Replay after a change** [Recipe 4; 20–30 min]: say "Replay the gold set and the twins. Compare must-haves, must-nots, scores and seeded-fault detection with the baseline, one line per scene." If anything got worse, say "Undo the change."

**Templates (reproduced exactly from §10.1)**

Reviewer instruction:
```
You are reviewing one scene of a film breakdown. You did not write it.
Inputs: the scene file, the quoted source lines, the rubric (D7 Sections 3-5, version [rubric_version]) and the gold file if one exists.
1. Read only the shots listed in sample_shots, plus the scene-level records.
2. For each check tagged ask in D7 Section 3, answer yes or no. Quote the record field and the source line for every no.
3. List each problem as one finding: record_id, check, severity (blocking or minor), evidence (the quote and its line), fix.
   Drop any finding you cannot support with a quote.
4. Think through your reasoning first. Then give one score from 1 to 4 per dimension, using the anchors in D7 Section 4.1 and 4.2 only.
5. Output the findings list and the nine scores. Do not rewrite the scene.
```

Finding:
```json
{"id": "F-SC13-001", "record_id": "SC13-SH310", "check": "vis_2", "dimension": "visual_storytelling",
 "severity": "blocking", "evidence": {"quote": "You.", "line": "l.770", "block_id": "L0770"},
 "fix": "Hold Eli from 'She waits'; cut to Iona only on 'You.' and hold her through 'Silence.'",
 "found_by": "reviewer_a", "status": "open"}
```

Gold file skeleton (`assets/examples/gold/SC13.gold.json`):
```json
{"scene": "SC13", "rubric_version": "d7_v1", "source_range": "l.672-829",
 "must_have": [{"id": "MH-01", "quote": "Iona watches her own elbow hit the button.", "block_id": "L0734", "record": "SC13-B06", "check": "dra_5"}],
 "must_not": [{"id": "MN-01", "text": "music under the recording", "check": "res_4"}],
 "acceptable_variants": [{"id": "AV-01", "text": "on 'You.' stay on Iona (A1 Ex3) or hold Eli and cut to her (A2)"}],
 "reference_scores": {"fidelity": 4, "dramatic_accuracy": 4, "visual_storytelling": 4, "continuity": 4, "restraint": 4,
   "feasibility": 4, "estimate": 4, "readability": 4, "downstream_readiness": 4},
 "resolved_conflicts": [{"topic": "tightest frame", "choice": "B15, per A2's sign test", "other_files": ["A1 Ex3", "B1 Ex3"]}]}
```

Calibration entry:
```json
{"scene": "SC13-twin", "date": "2026-09-28", "rubric_version": "d7_v1",
 "reviewers": {"reviewer_a": "[exact model name]", "reviewer_b": "[exact model name]"},
 "scores": {"reviewer_a": {"visual_storytelling": 1}, "reviewer_b": {"visual_storytelling": 2}, "user": {"visual_storytelling": 1}},
 "resolutions": ["VIS: user and A agree; B missed F2 (palm)"], "alpha": "none", "anchor_changes": []}
```

## 5. Checklists

**The 71 checks** [§3.2] (`c` code, `a` ask, `h` human):
- **FID**: 1 every line covered or omitted with reason [c]; 2 facts carry findable quotes [c]; 3 dialogue verbatim [c]; 4 additions flagged, keep/cut [c+h]; 5 text marks (`BLACK.`, `CLACK`) honoured [a]; 6 source gaps asked, not fixed [a]; 7 prose passages tagged [a]; 8 element lists complete [a].
- **DRA**: 1 two-pole values, one changes [a]; 2 one main turn passing the sign test [c+a]; 3 event, driver, intentions, obstacles [a]; 4 playable gerunds, no emotion words in `behavior`/`action`/prompts (allowed in `notes`, voice delivery: D15 R1) [c+a]; 5 beats split at tactic changes, silent beats kept [a]; 6 plants and payoffs linked [c]; 7 no early reveal [a]; 8 POV named [a]; 9 the unsaid has a carrier [a].
- **VIS**: 1 one key shot per turn [c+a]; 2 landing face at turns, no volleys [a]; 3 size builds to the turn [c+a]; 4 staging changes on the turn [a]; 5 third thing and plot inserts readable [a]; 6 purpose names this script [a]; 7 motifs develop [c+a]; 8 reads with sound off [a]; 9 one light idea [a]; 10 turn shot shortest or longest [c+a]; 11 silences specified [a]; 12 floor plan and motivated moves [c+a].
- **CON**: 1 elements in bible and ledger [c]; 2 states chain [c]; 3 axis and eyelines, crossings bridged [c+a]; 4 30° or size step [a]; 5 sides right for mirror phase [c+a]; 6 withholds and `forbidden` honoured (C5 R33) [c+a]; 7 in-story footage identical [c]; 8 key-light side consistent [a]; 9 keys pasted unchanged [c].
- **RES**: 1 ≤ 1 ECU (on the turn), ≤ 1 push-in per scene (B1 principle 5) [c]; 2 ≤ 1 added emphasis per beat [c+a]; 3 any-film test (B3 R26; B4 R24–25) [a]; 4 music per policy, cue has "must not" [c+a]; 5 quiet plants [c+a]; 6 no illustrated metaphors or voiced subtext [a]; 7 reserved choices in slot [c+a]; 8 cuts unless justified [a]; 9 moves motivated [c+a]; 10 no stereotype coding [h].
- **FEA**: 1 valid clip length, one action [c]; 2 ≤ 2.5 words/s (reconciled ≤ 2.5 × (clip s − 1)) [c]; 3 text ≤ 3 words or composited [c]; 4 content-risk method [c+h]; 5 previs level [c+a]; 6 ≤ 3 acting characters [c+a]; 7 physics as visible behaviour [a]; 8 sound source, edit transitions, handles [c].
- **EST**: 1 derived block, prices < 30 days (D13 E11) [c]; 2 within ±10% of target (E1) [c]; 3 class, clip, takes per shot [c]; 4 eighths, story day [c].
- **REA** (ISO 24495-1: relevant, findable, understandable, usable [V]): 1 one plain line per shot [c+h]; 2 no undefined term or JSON [a]; 3 questions as choices [c+h]; 4 key shots found in under a minute [h].
- **DOW**: 1 schema and IDs [c]; 2 storyboard fields [c]; 3 previs fields [c]; 4 no linter FAIL [c]; 5 sound diegesis, V.O. source [c]; 6 light spec [c]; 7 bible entries complete [c+a].

**Core record (missing = score 1)** [§4.2]: FID coverage map; DRA values table; VIS key shot list; CON start and end states; RES none; FEA durations and model targets; EST estimate block; REA readable export; DOW valid scene file.

**User review sheet** [§7] (wanted answer; dimension; if not, say):
1. Can you say in one sentence what changes in this scene? (yes; DRA) "Show the turning point, its line and its value."
2. Can you tell what each shot is for? (yes; VIS-6, REA-1) "Rewrite the purposes of [IDs] from the script."
3. Does the moment the scene turns get the strongest picture, and only that moment? (yes; VIS-1, VIS-3, RES-1) "List every push-in, close-up and music cue, with its beat."
4. When a line hurts someone, are we watching the person it hits? (yes; VIS-2) "Who is on screen when each reveal lands, and why?"
5. Is everything that is not in the script marked "added"? (yes; FID-4) "List every addition as keep/cut questions."
6. Does anything feel like it belongs to a different film: a symbol, a music cue, a camera trick? (no; RES-3, RES-4) "Run the any-film test on shots [IDs]."
7. Is what the story hides until later hidden in every shot? (yes; CON-6, DRA-7) "Show any shot that breaks the withhold list."
8. Could you sketch where everyone is and which way they face? (yes; CON-3, VIS-12) "Describe the floor plan and each single's eyeline side."
9. Are the quiet moments (pauses, looks, a silence) kept as shots? (yes; DRA-5, VIS-11) "List the silent beats and the shot that carries each."
10. Is there anything you would not want to see made, or that is too much? (no; RES, FEA-4) "Propose a quieter version of [ID]."

Sheet to scores: DRA (Q1, Q9), VIS (Q2, 3, 4, 9), RES (Q3, 6, 10), REA (Q2 plus words asked about); 0 unwanted = 4, 1 = 3, 2 = 2, 3+ = 1; unwanted Q3 or Q4 is blocking (dimension ≤ 2). Q5, Q7, Q8 become findings to verify.

**Before `pass`**: validator zero errors; sample drawn by script and recorded; every finding quotes a record and a line; fact dimensions ≥ 3; none < 2; mean ≥ 3.0; review sheet answered (Q1–3, or all ten for key scenes); `rubric_version` and `reviewer_models` recorded.

## 6. Saying it to AI models

- Give the reviewer rubric, anchors, quoted source lines and the gold file: Prometheus matched GPT-4 "when the appropriate reference materials (reference answer, score rubric) are accompanied" [V].
- "Ask the LLM to reason first before producing an evaluation score, and then discard the reasoning" (Anthropic) [V]; store only findings and scores.
- Every judgment is a yes/no question naming a record and a line; never "Is this good?" or "Review and improve your answer" (C5 R11, R12).
- A different model or fresh session reviews; swap order in A/B comparisons; scripts, not LLMs, compute totals, coverage and α (C5 R23, R25).
- Fix narrowly: "Fix only findings F1–F5 in SC13, change nothing else, re-run the validator, and re-score VIS, CON and RES."

## 7. The Catch

**Decisions (gold content, §6).**
- **SC06 (l.198–299):** Eli's hidden hand and the puck withheld from l.224 to the CLACK (l.259); longest fall shot on "He has one hand she cannot see." (l.253); STOP insert (l.228) replayed in SC13; about 10 frames of black and true silence (l.261), made in the edit; camera bolted to the cage, no shake in free fall; ledger: wound l.222, `PR-PUCK.S02` l.224 then `.S03` l.259, palm l.286, `turned` from l.259; beads (l.244) composited until the cage stops; "This time they hear it land." (l.298) the longest shot. Must-not: a field saying Eli fired the puck; music. Twin: hand visible at l.232, sting under the black, early `.S03` (blocking); shake (minor).
- **SC13 (l.672–829):** B6 silent (l.734); key shots B7, B12, B15; B7's eyeline passes Jude to Eli (l.742); footage static and full-frame, freeze in room tone; no volley on "One body." / "One." / "You." (l.764–770); palm (l.798) rhymes with l.286; head turn (l.811) in a held single; one push-in, on Iona, tightest at "I wasn't asking her." (l.822); singles from the bed-head side, Iona frame-right, Eli frame-left; replayed puck `.S02`, footage mirrored. Must-not: music under the recording; a move on the footage; a second push-in. Eli's closest single one size wider than Iona's B15 frame. Sample about 15 shots.
- **SC15 (l.838–867):** tablet "propped on her knees" (l.832); one fixed feed camera; the figure appears between frames (l.850); sourceless CLICK (l.844); cup in the ledger (l.846, l.862); hand under the arm (l.860) kept for SC16 (l.877); one pump sound reused (SC16 l.887, SC25, SC28, SC30); end on "The chair is still there." (l.866). Twin: push-in, cup reset (blocking); un-mirrored timestamp (minor).
- **LONGPL SC01 (l.7–33):** hands only, no marks (A3 R21); letter rules as inserts (l.15, l.17); three lamp beats (l.29); tally wall (l.19); 4–6 V.O. lines ending "begin" (l.33). Twin: Melek's "burn gone silver" (l.47) on the keeper: FID-4 blocking, scene fails.

**Worked example (§13):** the SC13 twin plants F1 ping-pong on the confession (VIS-2), F2 palm cited but not shown (FID-1 passes; the record-derived question catches it, VIS-5), F3 push-in on Eli (RES-1, RES-2), F4 strings under the recording (RES-4), F5 axis crossed by a bare cut (CON-3 flag). Scores: VIS 1, CON 2, RES 1, others 4; mean 3.11 but `revise`. The user's sheet finds four of five in plain words (Q3, Q4, Q6, Q9); only the axis fault needs the script.

**Flagged for the user:** SC13's tightest frame (B15 by the sign test, not "You."); which hand Eli hides (script: "His other hand"); SC06 screen time (expanded slices versus real time); film music policy; whether replayed footage is mirrored (depends on phase boundaries); whether the user scores four dimensions or all nine; whether a later Long Places chapter (VII) joins the gold set.

## 8. Conflicts and open questions

1. **SC13 main turn:** A2 (B15, sign test) versus A1 Ex3 and B1 Ex3 ("You."). Gold follows A2 and the critic. User decision.
2. **Footage push-in:** A2 B7a pushes in; B1 §10.4 "never re-framed" (characters may pause, rewind, enlarge). Gold static.
3. **SC13 row order:** A2 Iona, Jude, Eli; B3's rendered master Eli, Jude, Iona from frame-left. B3 canonical.
4. **Pump before strip** (B5 Ex3): a logged addition.
5. **`must_keep`** spelling (C5 R29); derive C5's beat key-shot flag from `shot_role`.
6. **Eli's hand side:** C5 E3 says "right" illustratively; the script does not.
7. **SC06 time:** A4 WE1 (about 12 s), B1 (real time), C4 (about 1.2 s); critic: real-time slices, no slow motion.
8. **Music:** D9 default `none`; the user sets policy; gold music must-nots hold under any policy.
9. **Mirrored replay** depends on unconfirmed phase boundaries.
10. **Line numbers vs D14 block IDs:** gold stores block ID plus quote.
11. **Emotion words:** DRA-4 versus D15 R1 (`notes`, voice delivery allowed).
12. **Speech rate:** 2.5 words/s versus the critic's 2.5 × (clip − 1); validator adopts the constant.
13. **α may be unreachable:** Co-Director (advertising): reviewer–human 0.469–0.592, human–human 0.578–0.641 [V]; ten scenes and mostly-4 scores make α unstable [J]; fallback gate in P3.
14. **Vocabulary:** "key" and "beat" collide across files; D7 writes "key shot" and C5 beat IDs (`SC13-B07`).
15. **Open:** "C5 P5/P9/P10/P13" point to the C5 digest; sample size, ±10%, pass marks and 80% detection are uncalibrated [J]; REA-2 has no library source.

## 9. Section map

D7 header, §1 → digest 1 · §2 principles → 2, 6 · §3 inventory and 71 checks → 5 · §4 anchors, errors versus flags → 2, 4, 5 · §5 sampling and verdicts → 2 · §6 gold scenes and replay → 7, 2 · §7 review sheet → 5 · §8 calibration and α → 4, 2, 8 · §9 rules R1–R15 → 2 · §10 recipes and templates → 4 · §11 fields → 3 · §12 failure modes → 5, 8 · §13 worked example → 7 · §14 conflicts → 8 · Sources (re-checked 2026-09-28).
