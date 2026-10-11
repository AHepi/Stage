# D7. Judging a Breakdown: a Scored Rubric, Gold Scenes, and a Review Routine a Non-Expert Can Run

*Library file D7. Written 2026-09-27. Test sources: "The Catch" (screenplay, workshop revision of 25 September 2026) and "The Long Places" (prose, revised final).*

> **What this file is for**
> 1. It merges the 275 checklist items spread over A1 to C5 into one acceptance test: nine dimensions, each scored 1 to 4 against written anchors.
> 2. It tags every check as decided by a script, by a yes/no question to an LLM, or by a person, and it says which shots get read (the sample) and what score passes.
> 3. It defines four gold scenes (The Catch SC06, SC13, SC15; The Long Places chapter I scene 1), each with a copy that has faults planted in it, replayed after every change to the pipeline.
> 4. It gives the user a ten-question review sheet for the readable export, and a calibration routine in which two LLMs and the user score the same scene.
> 5. It scores a deliberately flawed SC13 breakdown against a good one and shows which check catches each fault.

**Evidence labels.** [V] verified at the named source on 2026-09-27 (re-opened 2026-09-28); [U] unverified; [J] this file's judgment. Nearly every threshold (the 1–4 scale, the 10% sample, the pass marks) is [J], a starting value for calibration (Section 8) to adjust.

**Builds on, does not repeat.** C5 §6.6–6.7, R11–R14, R25, R27, R32, R33, Recipe 4, Recipe 8; the per-file checklists; A2's `shot_role`; D13 §11 (estimate block); D9 (music policy); D14 (source block IDs); D16 (scene `structure_role`). This file adds what those lack: scores, sampling, reference answers and a human routine.

**Reference conventions.** "C5 P5", "P9", "P10" and "P13" are procedure numbers in the C5 *digest* (`digests/C5_…digest.md`), not in C5 itself: P5 = C5 Recipe 4 and §6.6–6.7 (validate-fix loop), P9 = C5 Recipe 8 (evaluation first), P10 = C5 Recipe 5 (export), P13 = C5 E3 (shot record template). "l.224" means line 224 of the uploaded source file, which D14 stores as `original_ref` beside a block ID (`L0224` for the screenplay; `ch01.p00N` for prose paragraphs); gold files store the block ID **and** the quoted words, so a renumbered source still matches (rule 11).

**Fact-check pass (2026-09-28).** Re-opened: Anthropic's develop-tests page, Zheng et al., Wang et al., G-Eval, Prometheus, Shankar et al., Krippendorff's alpha (Wikipedia and the `krippendorff` Python package), the IPLF and ISO pages, Co-Director (full text, Table 2) and Huang et al. (full text, §4). Every quoted line of *The Catch* and *The Long Places* was checked against the uploaded files. Corrected: Co-Director's α given with its human–human ceiling and its advertising domain; Krippendorff's thresholds attributed to "social scientists" as he reports them; Prometheus's wording; "Eli's right hand" (the script does not give the side); the SC15 tablet "propped on her knees", not in her hands; the pump's returns (SC16, SC25, SC28, SC30, not only SC16 and SC30); the SC13 sample size (about 15, not 13); the P-number and D1 section references. Added: plain definitions, a key-scene definition (from D16), `unsure` handling, rules 11–15, the reviewer-pack template, privacy for the second app (D1), and new conflicts in Section 14.

---

## 1. Words this file uses (one word per concept)

- **Acceptance test**: the per-scene decision that the breakdown may go on to storyboards, previs or generation.
- **Rubric**: the table of dimensions and anchors used to score a scene.
- **Dimension**: one quality the rubric scores; there are nine.
- **Anchor**: a written description of what one score looks like, in things a reader can find in the records.
- **Check**: one merged question from Section 3, with an ID such as `FID-3` (stored as `fid_3`, per C5 R29).
- **Tag**: who decides a check. `code`: the validator (the pipeline's checking script). `ask`: an LLM answers a yes/no question built from quoted records (C5 R11). `human`: the user.
- **Finding**: one problem, recorded as `{record_id, check, severity, evidence, fix}` (C5 §6.7's format plus a severity).
- **Severity**: `blocking` if a viewer would misread the story, continuity would break, or a generation would be wasted; otherwise `minor`.
- **Reviewer**: whoever scores: the validator, an LLM or the user (C5's "judge").
- **Sample**: the shots a reviewer reads for the shot-level checks.
- **Key shot / must-keep shot / turning-point beat** (A2): a key shot carries a value turn; a must-keep shot is one a later key shot depends on; a turning-point beat is where a value changes sign.
- **Gold scene**: one scene's breakdown checked by a person against the source line by line, stored as must-have, must-not and acceptable-variant lists.
- **Seeded twin**: a copy of a gold scene with known faults planted in it.
- **Replay**: re-running the gold scenes after any change and comparing with stored results (C5 R32).
- **Calibration**: several reviewers score the same scene, compare, and fix the anchors where they disagree.
- **Readable export**: `exports/breakdown.md` (C5 P10), the plain-language document the user reads.
- **Key scene**: a scene whose D16 `structure_role` is anything other than `none` (inciting incident, act climax, midpoint, crisis, hinge payoff, sequence climax, climax, resolution), plus the four gold scenes. The user reads the full review sheet for these.
- **Value, charge and the sign test** (A2): a value is a pair of opposites in a character's life (trust/betrayal); its charge is where it stands (+ or −); the sign test asks whether the charge flips sign at the beat marked as the turn. A beat that only deepens a charge (+ to ++) is not a turn.
- **Bible and ledger** (C5): the bible holds fixed facts about each character, prop and place; the state ledger is the table of how each one changes over time (a wound, a skinned palm, a puck clipped then burnt).
- **Mirror phase**: the stretch of *The Catch* in which the world is left-right reversed (phase B, from the CLACK in SC06 to Iona's turn in SC27); sided details must be checked against it.
- **Linter**: C3's 31-item prompt checklist (L01–L31), run by a script or an LLM on each prompt before it is sent; it returns PASS, WARN or FAIL per item.
- **Enum, snake_case**: an enum is a field with a fixed list of allowed words; snake_case writes them in lowercase joined by underscores (`must_keep`).
- **Unwanted answer**: a review-sheet answer other than the one the question wants. `unsure` is not unwanted: it triggers the "say to the LLM" question but does not lower a score (rule 13).

---

## 2. Core principles

1. **Script first, then questions, then taste.** Anthropic ranks code grading "fastest and most reliable", human grading "slow and expensive", and LLM grading "fast and flexible", to be tested "first then scale" [V, develop-tests].
2. **Score evidence, not impressions.** Every score below 4 points to a finding quoting a record field and a source line; a finding without evidence is dropped [J, after C5 R11, R25].
3. **Facts are not voted on.** Fidelity, continuity and feasibility are settled by the source, the ledger and model limits. Visual storytelling and restraint are taste, the user's call (C5 R14).
4. **The reviewer is not the writer.** Zheng et al. name "position, verbosity, and self-enhancement biases" [V]; G-Eval warns of "a bias towards the LLM-generated texts" [V]; Anthropic's evaluation page calls it "Generally best practice to use a different model to evaluate than the model used to generate the evaluated output" [V, develop-tests]. Review with a different model, or at least a fresh session.
5. **Read where the story turns.** Key, must-keep and turning-point shots are always read; the rest is sampled.
6. **Reference answers make scores mean something.** Prometheus, an open-source evaluator model, matched GPT-4 (Pearson 0.897 against human scores on 45 custom rubrics) "when the appropriate reference materials (reference answer, score rubric) are accompanied" [V]. The gold scenes are those references.
7. **Test the tester.** Seeded twins show whether a reviewer catches what it should.
8. **Anchors will move.** "Users need criteria to grade outputs, but grading outputs helps users define criteria" (criteria drift, Shankar et al.) [V]. Version the rubric; replay after every change.
9. **Three rounds, then the user** (C5 R13).

---

## 3. The inventory: 275 items, 71 checks

### 3.1 What exists

A1 §8: 23 (dialogue scenes). A2 §9: 19. A3 §11: 26 (plus §10's 21 element categories, feeding FID-8). A4 §12: 12 scene + 17 shot. B1 §13: 5 + 17. B2 §11: 10 + 13. B3 §10: 18 composition + 20 staging. B4 §12: 8 film + 9 motif + 6 scene + 5 shot. B5 §12: 19 character + 4 shot. C3 §21: 31 prompt checks (L01–L31). C5 §6.6: 13 validator checks (V1–V13). Total 275.

(The gap list that commissioned this file gave 25 items for A3 §11 and 17 + 17 for B3 §10; the files hold 26 and 18 + 20.) Most items repeat another file's: "no emotion words in performance fields" appears in six files.

**Notation.** `A1.14` = A1 §8 item 14. Split lists add a letter: `A4s`/`A4h` (scene/shot), `B1s`/`B1h`, `B2s`/`B2h`, `B3c` (composition, 10.1) and `B3g` (staging, 10.2), `B4f`/`B4m`/`B4s`/`B4h` (film, motif, scene, shot), `B5c`/`B5h` (character, shot). C3 items are `L01`–`L31`; C5 items are `V1`–`V13`.

### 3.2 The merged checks, by dimension

**Fidelity (FID): the breakdown is the story that was written.**
- **FID-1** `code`: Every source scene has a record; every source line is in a shot or omitted with a reason. (V2, A3.10)
- **FID-2** `code`: Every extracted fact carries a source line or quote the script finds. (V13, B5c.2, B3g.14)
- **FID-3** `code`: Dialogue and "what we see" directions are quoted word for word. (A1.22, L31)
- **FID-4** `code + human`: Anything not in source or bible is flagged as an addition, with a reason and a keep/cut answer. (V12, A1.20, A3.19, B3g.20, B4f.7, B5c.3)
- **FID-5** `ask`: The text's own editing and sound marks (`BLACK.`, `CLACK`, `CUT TO BLACK.`) are listed and honoured. (A4s.10, A3 §10 item 17)
- **FID-6** `ask`: Source flaws and gaps are flagged as questions, not silently fixed. (A1.19, A2.17, A3.20)
- **FID-7** `ask`: Prose only: each passage is tagged dramatized, narratized or inner, with a treatment. (A2.16)
- **FID-8** `ask`: Element lists are complete (both of A3 §10's passes run). (A3.13, A3 §10)

**Dramatic accuracy (DRA): the breakdown reads the scene's meaning correctly.**
- **DRA-1** `ask`: Each value has two poles in a character's life; at least one changes charge. (A2.1, A2.2)
- **DRA-2** `code + ask`: The main turning point is one numbered beat, and the charges table agrees with every `turns_at` (A2's sign test). (A2.3, A1.3)
- **DRA-3** `ask`: The event is one past-tense sentence; driver, intentions and obstacles named. (A3.2, A3.3, A3.5, A2.4, A2.5, A1.2)
- **DRA-4** `code + ask`: Actions are transitive, playable gerunds; performance fields carry no emotion adjectives. (V7, A3.4, A2.6, A2.15, A1.1, L07, B5c.8) *Scope:* "performance fields" are `behavior`, `action` and prompt text; D15 R1 keeps an emotion word allowed in `notes` and in the voice-delivery field, so the script must not flag those two.
- **DRA-5** `ask`: Beats split at tactic changes; silent beats (moves, looks) are included; intensities follow A2 Step 6. (A2.7, A2.8)
- **DRA-6** `code`: Every plant has a payoff and every payoff a plant, linked by ID. (V8, A2.13, A3.18, A1.11, B4m.1)
- **DRA-7** `ask`: The information mode (suspense, mystery, surprise) is stated; needed facts arrive in time; no field reveals a fact before its scene does. (A4s.4, A3.9)
- **DRA-8** `ask`: The point-of-view character is named; shots outside that view carry a reason. (A3.24, B3g.12)
- **DRA-9** `ask`: The unsaid has a visible or audible carrier; forced exposition is flagged or moved into an image. (A1.6, A1.12, B4s.1)

**Visual storytelling (VIS): the pictures carry the story.**
- **VIS-1** `code + ask`: One key shot per value turn, the main one planned first, and each exists in the shot list. (A2.9, A3.6, A4s.1, B1s.2)
- **VIS-2** `ask`: A landing face (the face a line lands on) is chosen for every turn, reveal, refusal and interrupted line; at least once not the speaker; no line-by-line volleys. (A1.4, A1.5, A1.15, A1.23, A3.8)
- **VIS-3** `code + ask`: Shot size moves toward the turn; the tightest size is on the main turn; paired singles match unless power shifts. (A1.14, A2.11, B1s.2, B1s.5)
- **VIS-4** `ask`: Every beat change changes the screen; the staging changes on the turn, not before or after. (A2.10, B3g.3, B3g.4)
- **VIS-5** `ask`: The third thing (the object a conflict runs through) and every plot insert are in frame at the turns, readable in size and time. (A1.8, A2.14, A3.7, A4h.6)
- **VIS-6** `ask`: Each shot's purpose names an object, line or action from this script. (B3c.16, B2h.12, B1h.1)
- **VIS-7** `code + ask`: Motifs have plant, develop and payoff with emphasis levels; each return changes something; payoffs rhyme. (B4m.1–6, B4h.1, A4s.5, B2s.6)
- **VIS-8** `ask`: The dominant is named and the cues agree on it; the frame tells the beat with the sound off. (B3c.1–8, B3c.15)
- **VIS-9** `ask`: One main light idea tied to the value change; light cues on turns, with a cause in the story's world; dark shots readable. (B2s.1–5, B2h.2–4, B2h.11)
- **VIS-10** `code + ask`: A rhythm plan exists; the turn's shot is the scene's shortest or longest. (A4s.1, A4s.2, A4s.11)
- **VIS-11** `ask`: Pauses are ranked; each silence is specified as room tone, drop-out or true silence. (A1.9, A1.10, A4h.11)
- **VIS-12** `code + ask`: A floor plan with an anchor; moves with beat IDs and reasons; a master before the first important move; the pivot named. (B3g.1–2, B3g.5, B3g.7–10, B3g.17–18, A3.11)

**Continuity (CON): every shot agrees with every other shot.**
- **CON-1** `code`: Every element in a shot is in the bible, with a ledger state and look ID. (V3, A3.25)
- **CON-2** `code`: States chain shot to shot and across `CONTINUOUS`; each change cites a line. (V4, A3.14, A3.15, A4s.12, B4s.5, B5h.1)
- **CON-3** `code + ask`: The axis (the line the camera stays on one side of) is recorded; paired singles have opposite eyelines; a crossing is on a beat and shown by a move or bridging shot, never a bare cut. (A1.21, A2.18, A4h.2, A4h.4, B1h.14, B3c.11, B3g.6, B3g.16, A3.12, L25)
- **CON-4** `ask`: Consecutive shots of one subject differ by at least 30 degrees or a clear size step; a match on action holds the whole movement in both shots. (A4h.3, A4h.5)
- **CON-5** `code + ask`: Every sided detail is correct for the mirror phase; flipped shots re-checked; text carries an orientation. (V6, B1h.12–13, B3c.10, B3g.19, B4h.2, B5c.7, B5c.18, B5h.2, A4h.13, L27)
- **CON-6** `code + ask`: What is withheld stays out of every angle; `required` and `forbidden` lists are honoured. (B1h.9, A4h.8, B2h.5)
- **CON-7** `code`: In-story footage is identical at every viewing; its camera is in the original floor plan; replayed elements use their state at that moment. (B1h.11, A3.22, C5 E4)
- **CON-8** `ask`: The key light's side and the time-of-day step stay consistent within a scene. (B2h.1)
- **CON-9** `code`: Identity and look keys are pasted unchanged; the state line is current. (B5h.4, L16, L17)

**Restraint (RES): nothing is louder than the story needs.**
- **RES-1** `code`: At most one extreme close-up (on the turn) and one push-in per scene; film caps on Dutch tilt, orbit, dolly zoom. (B1s.3 (B1 principle 5))
- **RES-2** `code + ask`: At most one added emphasis device per beat, none where the script already marks it; one rupture; emphasis-3 caps. (B1s.4, B3c.17, B4h.4, B4s.2, A4s.3)
- **RES-3** `ask`: The any-film test (B3 rule 26: would this frame make sense pasted into a different film?): every symbolic object is sourced and has a practical job; no stock images (B4 rules 24–25: a cliché stays only if the text names it, it has a practical job and it changes something). (B3c.16, B4m.5, B4s.3, B1h.16, B2s.6)
- **RES-4** `code + ask`: Music follows the film's policy; every cue has in, out, function and "must not"; no cue states the subtext. (A1.17, A4s.8)
- **RES-5** `code + ask`: A "do not emphasise" plant matches its neighbours' size and duration; after a payoff, returns stay at emphasis 0–1. (A3.26, B4m.2–4, B4s.6)
- **RES-6** `ask`: Figures of speech are not illustrated; the unsaid is not turned into speech or voice-over. (A1.18)
- **RES-7** `code + ask`: Reserved choices appear only in their slot; a camera system's payoff is not spent early. (B3c.14, B1s.1)
- **RES-8** `ask`: No transition other than a cut unless the text or a time gap justifies it. (A4s.6)
- **RES-9** `code + ask`: Every camera move has a named motivation; at most one per shot; a cut would not do the same job. (B1h.7, B1h.8, B1h.17, L03)
- **RES-10** `human`: No stereotype coding by ethnicity, body, disability or face. (B5c.13)

**Feasibility (FEA): the plan can be made with today's tools.**
- **FEA-1** `code`: Clip length is valid for the chosen model; one main action unless `compound`; beats fit the duration. (V5, V10, A4h.17, L02, L05)
- **FEA-2** `code`: At most 2.5 spoken words per second; long lines split at a phrase boundary under a listener shot; listener shots generated silent. (V5, L08, A4h.15, A4h.16) The critic's reconciled constant is stricter: spoken words ≤ 2.5 × (clip seconds − 1.0), so at most 17 words in an 8 s clip, with a slower per-character rate from `speech_profile` (Saye about 2.0). The validator uses that constant once the constants file exists.
- **FEA-3** `code`: On-screen text is 3 words or fewer or composited, and on screen long enough to read. (V6, L21, A4h.14, A3.16, A3.17)
- **FEA-4** `code + human`: Content risk (injury, weapons, blood) has a recorded method (C3 §14, D4). (L24)
- **FEA-5** `code + ask`: Previs level is set: a greybox (plain grey 3D render) for framing-critical shots, a declared pose for action-critical ones. (C5 R26, per-shot checklist)
- **FEA-6** `code + ask`: At most 3 acting characters per clip; important things survive the output resolution. (L22, B4h.3)
- **FEA-7** `ask`: Impossible physics: the camera obeys the same physics; motion is written as visible behaviour, not "gravity". (B1h.10, L23)
- **FEA-8** `code`: Model sound versus edit sound stated; transitions made in the edit; handles planned. (A4h.9, A4h.12, C5 R16)

**Estimate (EST): the scene says what it will cost.**
- **EST-1** `code`: The scene's `estimate` block exists, is written by the script, and its price date is under 30 days old. (D13 §11.2, E11)
- **EST-2** `code`: Shot durations add up to the scene target within ±10%. (V10, D13 E1, A2.19)
- **EST-3** `code`: Every shot has a cost class, clip length and planned takes. (D13 §12)
- **EST-4** `code`: Eighths and story day are filled; the cost warning has been checked. (A3.21, L30)

**Readability (REA): a layperson can act on it.** (New; after ISO 24495-1: readers get what they need, find it, understand it, use it [V, via IPLF].)
- **REA-1** `code + human`: The readable export has one plain line per shot: what we see, why, which source line. (new)
- **REA-2** `ask`: No undefined term; one word per concept; no JSON shown to the user. (new; C5 §6.10)
- **REA-3** `code + human`: Open questions and additions are asked as answerable choices (keep/cut, A or B). (A3.20, V12)
- **REA-4** `human`: A "Key shots" list at the top finds each turn's picture in under a minute. (new)

**Downstream readiness (DOW): the next stages can use it without guessing.**
- **DOW-1** `code`: The file matches the schema (the agreed fields and types); IDs issued and resolving; jobs point to existing records. (V1, V9, V11)
- **DOW-2** `code`: Storyboard fields: subjects with position, facing and action; props with state; look. (C5 P13)
- **DOW-3** `code`: Previs fields: floor plan, marks, camera positions, lens. (B3g.1, A3.11)
- **DOW-4** `code`: The prompt linter (L01–L31) returns no FAIL. (L01–L31)
- **DOW-5** `code`: Each sound labelled diegetic (inside the story's world) or not, on- or off-screen; each V.O. has a voice source. (A4h.10, A3.23, L11)
- **DOW-6** `code`: The light spec is filled (key, colour, why, prompt line). (B2h.10, B2h.13)
- **DOW-7** `code + ask`: Every bible entry the scene uses is complete (B5, B4 register, B2 location plan). (B5c.*, B4f.*, B2s.2–3)

**Folded in as sub-questions:** B1h.2–6, B1h.15 → VIS-3; B2s.7–10, B2h.6–9 → VIS-9 (dark skin also RES-10); B3c.9, B3c.12–13, B3c.18 → VIS-8, CON-3; B3g.11, B3g.13, B3g.15 → VIS-12; B4s.4 → RES-3; B4h.5 → DOW-4; A4s.7 → DOW-5; A4s.9 → VIS-10; A4h.1, A4h.7 → VIS-2; A1.7, A1.13, A1.16, A2.12 → DRA-9, VIS-2; A3.1 → DOW-1; B5h.3 → DRA-4. B4f and B5c items are checked once, at checkpoint B, and referenced by DOW-7.

---

## 4. The rubric

### 4.1 One anchor rule for all nine dimensions [J]

The rubric runs only on a scene whose validator report shows zero errors (C5 P5). Validator warnings enter the rubric as minor findings. **Errors versus flags [J].** The script reports two kinds of result. *Errors* are failures the pipeline cannot proceed past: the schema and IDs (V1, V9, V11), coverage (V2), a quote not found in the source (V13), a missing bible entry or ledger state (V3), broken state chains (V4), and hard model limits (clip length, words per second, text length: V5, V6). An error stops the rubric (rule 1). Every other `code` check in Section 3 (budgets such as RES-1, eyeline sides in CON-3, the rhythm test in VIS-10, duration totals in V10 and EST-2, additions in V12, linter FAILs in DOW-4, the estimate checks in EST) is computed by the same script but reported as a *flag*: it enters the rubric as a finding, blocking or minor as Section 4.2 says, so the scene is still scored. That is how F3 (two push-ins) and F5 (same eyeline side) in Section 13 reach the scores.

| Score | Anchor |
|---|---|
| **4** | No findings, and the reviewer can point to the positive evidence named in 4.2 |
| **3** | Minor findings only (at most two), none on a key or must-keep shot |
| **2** | One blocking finding; or any finding on a key or must-keep shot; or three or more minor findings |
| **1** | Two or more blocking findings; or the dimension's core record is missing |

Each finding counts in one dimension only, the first whose check catches it in Section 3's order. Four points and no middle stop a reviewer parking at "average" [J].

### 4.2 What counts in each dimension

| Dimension | Positive evidence for a 4 | Blocking (examples) | Minor (examples) | Core record (missing = 1) |
|---|---|---|---|---|
| Fidelity | Every line covered; every addition answered keep/cut | A line or silent beat dropped without reason; an unlabelled invention; misquoted dialogue | An addition without a reason | Coverage map |
| Dramatic accuracy | Sign test passes; one main turn; playable gerunds | Wrong turning point; a must-keep silent beat missing; emotion labels bound for prompts; a reveal spoiled | An intensity off by one; a generic gerund | Values table |
| Visual storytelling | Each key shot is its beat's strongest image, with a landing face and a script-specific reason | A turn with no or a weak key shot; line-by-line cutting across a reveal; a plot insert missing; the wrong landing face at a turn | A normal shot with a generic purpose; a motif return that changes nothing | Key shot list |
| Continuity | Ledger chain intact; axis recorded; handedness computed | Axis crossed by a bare cut; a withheld thing visible; a sided detail wrong; a state jump | Background text without orientation; a near-duplicate angle | Start and end states |
| Restraint | Extremes within budget; one added device per beat at most; symbols sourced | Stacked emphasis on a turn; music stating subtext under a reveal; a stock symbol in a key shot; a telegraphed plant | One unmotivated move; one unjustified dissolve | none |
| Feasibility | Every clip generable; speech within limits; previs level and content-risk method recorded | A clip length the model cannot make; over 2.5 words per second; long text asked of the model; a framing-critical shot with no greybox | Missing handles; more than three named sounds | Durations and model targets |
| Estimate | A current `v1_shot_list` block within ±10% | No estimate; stale prices; total outside ±10% unexplained | A shot without cost class | Estimate block |
| Readability | The user answers the review sheet in about 15 minutes without asking what a word means | Export is JSON or IDs only; key shots cannot be found | One undefined term; an overlong line | Readable export |
| Downstream readiness | No linter FAIL; storyboard, previs, sound, light fields filled | A key shot lacking the fields to storyboard, previs or prompt it; a linter FAIL | Linter WARNs | Valid scene file |

Some blocking examples above (a clip length the model cannot make, over 2.5 words per second, misquoted dialogue, a state jump) are validator *errors* in practice: they stop the rubric before scoring (4.1) and never appear as scores. They stay in the table so a reviewer working without the script, for example in a chat app with no code execution, still treats them as blocking.

---

## 5. Sampling, adding up, and passing

### 5.1 Which shots are read [J]

The validator script picks the sample, so no LLM can choose easy shots. Its seed (the value that fixes a random draw so it repeats) is the scene ID plus the fix round, for example `SC13:r0` [J]. A replay of round 0 therefore draws the same shots every time, which keeps gold comparisons fair, and each fix round reads two fresh random shots, so an unsampled bad shot is not missed forever. (The first version used the scene ID alone; that made every round re-read the same random shots.)

1. Every shot with `shot_role` `key` or `must_keep`.
2. Every shot covering a beat with `turning_point: yes`.
3. 10% of the remaining shots, rounded up, at least 2 (all of them if 2 or fewer remain).
4. Scene-level checks always run on the whole scene.

**Escalation.** If a randomly drawn shot has a blocking finding, draw 10% more; if that draw has one too, read every shot. For SC13 (16 beats and about 31 shots in A2's plan) the sample is about 15: every shot of the key beats B7 (3 shots), B12 (4) and B15 (about 3) and of the must-keep beats B6 (2) and B14 (1), about 13 in all, plus 2 of the other 18 (10% of 18 is 1.8, rounded up to 2). The counts come from A2 §12's shot plan and will change with the real shot list.

### 5.2 Adding up

- **Scene:** one score per dimension, from the sample's findings plus the scene-level checks.
- **Scene verdict** [J]:
  - `pass` when the validator shows no errors, Fidelity, Dramatic accuracy, Continuity and Feasibility each score at least 3, no other dimension scores below 2, and the mean of the nine is at least 3.0;
  - `revise` otherwise;
  - `escalate` after three failed revise rounds (C5 R13), or when the fix needs a story decision.

  The four fact dimensions need a 3 because their errors are "re-expressed downstream, not repaired" (C5 lesson 13).
- **Sequence (checkpoint C):** every scene passes; the user answers questions 1–3 for every scene and the whole sheet for the sequence's key scenes (Section 1: a D16 `structure_role` other than `none`, or a gold scene). A sequence with no key scene gets the whole sheet on its highest-intensity scene (B3's story intensity, 1–10; the critic proposes the field name `scene_intensity`) [J].
- **Film:** every scene passes; the report gives each dimension's median and minimum and the five lowest scenes; no unwanted review-sheet answer lacks a note.

---

## 6. Gold scenes

### 6.1 What a gold file holds

Each gold scene is stored as `assets/examples/gold/<scene>.gold.json`, with its seeded twin `<scene>.twin.json`:

- `must_have[]`: each with source line, record and the check that tests it.
- `must_not[]`: things whose presence fails the scene.
- `acceptable_variants[]`: choices where the library allows more than one answer.
- `reference_scores`: what the gold breakdown earns (all 4 unless noted).
- `resolved_conflicts[]`: where library files disagree, the choice made and why.
- The twin's `seeded_faults[]`: fault, record, expected check, severity.

A gold file lists what must be true, not the one correct shot list: a breakdown meeting every must-have and tripping no must-not may differ in shot count and style.

### 6.2 SC06, the fall (l.198–299)

**Must-have**
- `withhold` on Eli's hidden hand and the puck in every angle from "His other hand goes underneath. Behind Jude's back. Out of sight." (l.224) to the CLACK (l.259) (CON-6). The script says only "His other hand"; C5 E3's example writes "right hand" as an illustration. Record the side once at checkpoint B and compute it per shot; the gold tests that the hand is hidden, not which hand it is.
- The fall's longest shot on Eli at "He has one hand she cannot see." (l.253), so SC13 can recall it (A4 WE1).
- An insert of "Iona hits STOP with her elbow." (l.228), replayed in SC13 (CON-7).
- "A hard metal CLACK." / "BLACK. A dark with nothing in it. One instant." (l.259–261) as its own shot: about 10 frames of black and true silence, made in the edit (FID-5, FEA-8).
- The camera bolted to the cage, no shake in the fall (B1 §10.1; FEA-7).
- Ledger rows: Jude's wound from l.222; `PR-PUCK.S02` from l.224, `.S03` from l.259; Iona's palm skinned at "Her palm drags across the bright steel." (l.286); handedness `turned` from l.259 (CON-2, CON-5).
- The blood beads (l.244) in every shot until the cage stops, composited.
- "This time they hear it land." (l.298) held on the three faces, the sequence's longest shot.
- The top-gate camera placed in the floor plan for SC13.

**Must-not:** any field saying Eli fired the puck (it spoils SC13; A3 Ex2; DRA-7); shake in free fall; music; a shooter shown beyond a flagged silhouette.

**Acceptable variants:** 30–40 shots (A4 WE1 plans 36); durations within ±10%; "Io." (l.251) over his close or just before it; the one short impact shudder at the stop (l.230–232), which B1 §10.1 allows as the sequence's only shake.

**Pending user decision:** the fall's screen time. A4 WE1 expands it to about 12 s over about 36 shots; B1 plays it "in real time" with no slow motion; the critic's resolution is expanded time built from overlapping real-time slices, no slow motion. The gold follows the critic until the user decides, and must be regenerated if the user chooses otherwise.

**Seeded faults:** Eli's hand visible in the wide at l.232 (CON-6, blocking); shake in the fall (FEA-7, minor); the black held 2 s under a music sting (FID-5, blocking); the puck at `.S03` before l.259 (CON-2, blocking).

### 6.3 SC13, the playback (l.672–829)

**Must-have**
- B6 kept as a silent beat: "Iona watches her own elbow hit the button. Beside her, Jude watches her watch it." (l.734) (DRA-5).
- Key shots on B7, B12 and B15 (VIS-1). B7 shows "Looks at her brother. Not at Jude." (l.742): her eyeline passes Jude before landing on Eli.
- The footage full-frame and static through "Empty." and the puck, then her face; Iona's freeze held in room tone only (A4 WE2).
- No line-by-line cutting on "One body." / "One." / "You." (l.764–770) (VIS-2).
- The palm, "She looks down at her palm, where the sill took the skin off." (l.798), framed to rhyme with SC06 l.286 (VIS-5, VIS-7).
- "He has been looking at the screen. Now he looks at her." (l.811) as a head turn inside a held single (must-keep).
- The scene's one push-in, on Iona across "I asked you in the car…", ending on its tightest size at "I wasn't asking her." (l.822) (VIS-3, RES-1).
- One frame for "All three of them flinch at the same moment." (l.826); the switch-off (l.828) as a sound drop-out.
- Singles from the bed-head side of the Iona–Eli line: Iona looks frame-right, Eli frame-left (B3 §8.6; CON-3).
- Replayed elements at SC06 states (`PR-PUCK.S02`); the footage mirrored, as a phase-B picture (B1 §10.4; CON-5, CON-7).

**Must-not:** music under the recording; the SC06 crash under the silent footage; a camera move on the footage itself; a second push-in.

**Acceptable variants:** on "You." stay on Iona (A1 Ex3) or hold Eli and cut to her (A2); on "Silence." (l.772) hold Iona 2–3 s (A2) or cut wide once to all three and the monitor (A1 Ex3 step 6); the palm as an insert (A2) or a focus pull to Eli (A1); reflections in the black screen, marked "added". Whichever is chosen, Eli's closest single stays one size wider than Iona's B15 frame, and his first look near the lens is spent on "Now he looks at her." (l.811) (critic's SC13 resolution).

**ID note.** A2's beat labels (B6, B7…) are written here for readability; the gold file stores C5 IDs (`SC13-B06`, `SC13-B07`; shots `SC13-SH010`…), because "B4" also names a library file.

**Seeded faults:** Section 13.

### 6.4 SC15, the figure on the tablet (l.838–867)

**Must-have**
- `presentation: on_screen`, host `PR-TABLET`, the tablet first seen "propped on her knees" in SC14 (l.832: "Iona on her bed, a tablet propped on her knees."). B1 §10.5's summary says "in Iona's hands"; the script's wording wins.
- One fixed high-corner feed camera; the figure arrives by a jump between frames, "It is simply there, in the space between one moment and the next." (l.850), with no travel and no other angle (B1 §10.5; RES-9).
- "A small CLICK, from nowhere." (l.844) with no visible source.
- The cup in the ledger: "The cup slides a hand's width across the table. Into his reach." (l.846), then "Jude grabs the cup before it tips." (l.862) (CON-2).
- "Its hand goes under his wounded arm and lifts it clear of the mattress. As carefully as a nurse." (l.860) in a frame the recording keeps, because SC16 "Stops it on the hand under his arm." (l.877) (CON-7).
- The pump, "three strokes, not quite even" (l.852), one sound file reused wherever the pump returns: SC16 ("Behind her: a pump. Three uneven strokes.", l.887), SC25 (l.1458, l.1478), SC28 ("Three uneven strokes.", l.1647) and SC30 (l.1838, l.1846) (VIS-7).
- The feed mirrored, any overlay text reversed (CON-5); "The chair is still there." (l.866) held at the end.

**Must-not:** a move toward the figure; glowing eyes or other stock-monster traits (B5 mistakes 9 and 17; RES-3); score; overlay text over three words asked of the model.

**Acceptable variants:** the pump heard before the strip moves (B5 Ex3, a logged addition); two clips joined by a hard cut (C3 Ex5) or one clip.

**Seeded faults:** a push-in on the figure (RES-9, blocking); the cup back at the table's edge in the next clip (CON-2, blocking); an un-mirrored timestamp (CON-5, minor).

### 6.5 The Long Places, chapter I scene 1, the keeper's letter (`LONGPL` `SC01`; l.7–33)

**Must-have**
- Hands only, faces withheld; no identifying marks on the keeper's or the child's hands, logged as `keeper_hands` and `child_hands` (A3 Ex5, rule 21).
- The letter's rules as inserts: "The oil goes to the first knuckle of the thumb and no further." (l.15); the wick "pinched, never cut" (l.15); "The flame you carry cupped and low" (l.17).
- Nine lamps, the room lit one pool at a time; "At the third lamp her hands shook, and at the fourth they did not, and at the ninth she yawned" (l.29) played as three beats.
- The last action, "you cut the day's mark, one line, low, beside all the other lines" (l.19), on a wall of such lines (the tally-wall plant).
- Voice-over of 4–6 letter lines, the last word "begin" (l.33) landing on the cut to SC02.
- Setups recorded for the novel's closing bookend; "before dawn" marked inference, the gallery invention (FID-4).

**Must-not:** faces; Melek's silver burn on the keeper's hand ("a burn gone silver across the back of the right one", l.47); a clock or a candle burning down to show time (B3 rule 24; B4 rule 25); voice-over beyond the budget; music stating the subtext.

**Source references.** The "l." numbers above are lines of the uploaded novel file. D14 stores prose as numbered paragraphs (`ch01.p001`…) with the file line as `original_ref`; the gold file cites the paragraph ID and the quoted words, never the file line alone.

**Acceptable variants:** which 4–6 lines are voiced; locked-off or hand-held camera.

**Seeded faults:** Melek's silver burn on the keeper (FID-4, blocking; Section 13); twelve voice-over lines (RES-6, blocking); a candle burning down (RES-3, minor).

### 6.6 Replay [J, extending C5 R32]

After any change to a stage instruction, validator rule, rubric or reviewer model: run stages 0–5 on the four gold scenes, run the validator and the rubric review, run the reviewer on the four twins, and compare with the stored baseline. Undo the change if a must-have was lost, a must-not tripped, any dimension score fell, or fewer seeded faults were caught. A reviewer must catch every blocking seeded fault and at least 80% of the minor ones across the four twins, rounded down [J]. The current twins hold 15 seeded faults: 12 blocking and 3 minor (SC06 shake, SC15 timestamp, LONGPL candle), so the reviewer must catch all 12 blocking and at least 2 minor.

## 7. The user's review sheet

Read `exports/breakdown.md` for one scene: a "Key shots" list, then one plain line per shot. Answer `yes`, `no` or `unsure`, with a note when the answer is not the one wanted; about 10–15 minutes [J]. At checkpoint C, answer questions 1–3 for every scene and the whole sheet for each sequence's key scenes.

| # | Question (the answer you want) | Dimension | If not, say to the LLM |
|---|---|---|---|
| 1 | Can you say in one sentence what changes in this scene? (yes) | DRA | "Show the turning point, its line and its value." |
| 2 | Can you tell what each shot is for? (yes) | VIS-6, REA-1 | "Rewrite the purposes of [IDs] from the script." |
| 3 | Does the moment the scene turns get the strongest picture, and only that moment? (yes) | VIS-1, VIS-3, RES-1 | "List every push-in, close-up and music cue, with its beat." |
| 4 | When a line hurts someone, are we watching the person it hits? (yes) | VIS-2 | "Who is on screen when each reveal lands, and why?" |
| 5 | Is everything that is not in the script marked "added"? (yes) | FID-4 | "List every addition as keep/cut questions." |
| 6 | Does anything feel like it belongs to a different film: a symbol, a music cue, a camera trick? (no) | RES-3, RES-4 | "Run the any-film test on shots [IDs]." |
| 7 | Is what the story hides until later hidden in every shot? (yes) | CON-6, DRA-7 | "Show any shot that breaks the withhold list." |
| 8 | Could you sketch where everyone is and which way they face? (yes) | CON-3, VIS-12 | "Describe the floor plan and each single's eyeline side." |
| 9 | Are the quiet moments (pauses, looks, a silence) kept as shots? (yes) | DRA-5, VIS-11 | "List the silent beats and the shot that carries each." |
| 10 | Is there anything you would not want to see made, or that is too much? (no) | RES, FEA-4 | "Propose a quieter version of [ID]." |

**Answers to scores (for calibration)** [J]: the sheet scores four dimensions only: DRA (questions 1 and 9), VIS (2, 3, 4 and 9), RES (3, 6 and 10) and REA (question 2, plus any word the user had to ask about). Per dimension, no unwanted answers = 4, one = 3, two = 2, three or more = 1; an unwanted answer on question 3 or 4 counts as blocking, so that dimension scores at most 2 (a `no` on question 7 is also treated as blocking, but as a CON-6 finding to verify, per the next paragraph). `unsure` does not count against a score; it makes the LLM answer that row's "say to the LLM" question, and the user then answers `yes` or `no`.

**Fact questions are not scored by the user.** Questions 5, 7 and 8 touch FID and CON, which are settled by the source and the ledger (principle 3). A `no` to them becomes a finding for the LLM to check against the quoted line; it is a score only if the quote confirms it.

---

## 8. Calibration: two LLMs and the user score the same scene

**When:** once before the first real run (on the SC13 twin), after every rubric change, then on one scene in every ten.

1. **Score blind.** Reviewers A and B, two different models in fresh sessions, score all nine dimensions from the scene file, source lines, rubric and gold file, following Anthropic's advice: "Ask the LLM to reason first before producing an evaluation score, and then discard the reasoning" [V, develop-tests]. Neither sees the other's scores or the user's. The user's review sheet scores DRA, VIS, RES and REA (Section 7). Code checks are run, not scored. **Privacy:** before pasting an unpublished script into a second app, turn model training off in that app and never use free Google AI Studio (D1 rule 9, D1 §8).
2. **Compare.** Per dimension: exact agreement, one apart, or two or more apart.
3. **Resolve.**
   - A script result beats any reviewer.
   - Fact dimensions and the sign test: the finding whose quote checks out against the source wins. No vote.
   - Taste dimensions (VIS, RES, REA): when the user differs from both LLMs by two or more, the user's score stands, the reason becomes an anchor example, and `rubric_version` goes up.
   - When the two LLMs differ by two or more, show the user both findings as one yes/no question. No LLM debate: with "an equivalent number of responses, multi-agent debate significantly underperforms simple self-consistency using majority voting", and LLMs "struggle to self-correct their responses without external feedback" (Huang et al., ICLR 2024, tested on reasoning benchmarks such as GSM8K, not on film review; C5 §6.7) [V].
   - When an LLM compares two versions, run it twice with the order swapped and keep only a preference that survives both. Rankings "can be easily hacked by simply altering their order" (Wang et al.) [V].
4. **Record** a `calibration` entry (Section 11).
5. **Set trust per dimension.** After at least ten calibrated scenes, compute Krippendorff's alpha between each LLM and the user: an agreement score that corrects for chance and handles ordered scales and missing ratings ("α = 1 indicates perfect reliability", "α = 0 indicates the complete absence of reliability", i.e. agreement no better than chance) [V, Wikipedia]. The LLM computes it with a script, never by hand: `pip install krippendorff`, then `krippendorff.alpha(reliability_data=…, level_of_measurement="ordinal")`; the default is "interval", so "ordinal" must be set [V, PyPI 0.8.2 and source]. Krippendorff (2004, pp. 241–243) reports that "social scientists commonly rely on data with reliabilities α ≥ 0.800, consider data with 0.800 > α ≥ 0.667 only to draw tentative conclusions, and discard data whose agreement measures α < 0.667" [V, via Wikipedia]. Here [J]: at 0.800 or above the LLM scores that dimension and the user reads its findings; from 0.667 the LLM scores first and the user checks each flagged finding; below 0.667 the user keeps scoring. Until then, the LLM must be within one point of the user on every dimension the user scored on the SC13 twin, and must raise every blocking finding the user raised.

   **Expect the user to keep the taste dimensions.** Co-Director (Google, April 2026) measured its multimodal reviewer against 5 human raters on 50 advertising videos, 5-point scales: reviewer–human α was 0.469–0.592 per dimension, and human–human α only 0.578–0.641 [V, Table 2]. Even people did not reach 0.667 there. Two cautions follow [J]: (a) with one user and ten scenes, alpha per dimension rests on ten pairs and swings widely; (b) when nearly every score is 4, chance agreement is already high, so a single disagreement pulls alpha down sharply (alpha divides observed by expected disagreement). If alpha cannot be computed or stays unstable, use the practical gate instead: the LLM is within one point of the user on at least 90% of scored dimensions across the last ten calibrated scenes and has missed no blocking finding the user raised [J].

---

## 9. Decision rules

1. **If** the validator reports any error, **then** do not start the rubric, **because** scores on a broken file measure the break (C5 P5).
2. **If** a check can be written as arithmetic, a count, a string match or an ID lookup, **then** tag it `code`, **because** scripts grade most reliably [V, develop-tests] and an LLM scorer once "re-attached" a deleted event (C5 R25).
3. **If** a check needs judgment, **then** phrase it as a yes/no question that names and quotes a record ("Does any shot citing l.798 show Iona's palm?"), **because** open questions to a reviewer fail (C5 R11).
4. **If** a finding has no quoted evidence, **then** drop it, **because** unanchored findings are how reviewers invent problems [J].
5. **If** a shot is `key` or `must_keep`, or covers a turning-point beat, **then** always read it, **because** a 10% random draw would usually miss the shots that decide the scene [J].
6. **If** a randomly sampled shot has a blocking finding, **then** widen the sample, **because** one fault found at random suggests others [J].
7. **If** Fidelity, Dramatic accuracy, Continuity or Feasibility is below 3, **then** the scene fails whatever its mean, **because** those faults grow more expensive at every later stage (C5 lesson 13).
8. **If** a finding survives three fix rounds, **then** set `escalate` and ask the user one question, **because** repair gains halve each round (C5 R13).
9. **If** the user's view of an anchor changes, **then** rewrite it, bump `rubric_version` and replay, **because** criteria drift is normal [V, Shankar et al.] and old scores must stay comparable.
10. **If** two library files disagree about a gold scene, **then** record the choice in `resolved_conflicts` and keep the other option as a variant if it meets every must-have, **because** a gold file must not fail a breakdown for following another file of this library [J].
11. **If** a gold must-have or must-not cites the source, **then** store the D14 block ID and the quoted words, and let the validator find the quote in the normalized source, **because** normalization can renumber lines, and a line number alone would silently point at the wrong text (C5 V13 finds quotes the same way) [J].
12. **If** a scene is a key scene (D16 `structure_role` other than `none`) or a gold scene, **then** the user answers the whole review sheet; otherwise questions 1–3, **because** the user's time is the scarcest input and the turns carry the film [J].
13. **If** the user answers `unsure`, **then** have the LLM answer that row's "say to the LLM" question with quotes and ask again for `yes` or `no`, **because** an unsure answer is a request for evidence, not a verdict [J].
14. **If** a review pack is pasted into a second app, **then** turn training off there first and never use a free tier that lets human reviewers read inputs, **because** the script is unpublished (D1 rule 9) [V via D1].
15. **If** the LLM–user agreement cannot reach Krippendorff's 0.667 on a taste dimension, **then** keep the user scoring it and use the LLM only to list findings with quotes, **because** in the one published test even humans agreed only at α 0.58–0.64 (Co-Director) [V; conclusion J].

---

## 10. Recipes (the LLM does the work; you read and answer)

**Recipe 1. Build the gold set (once; 2–3 hours of your reading).**
1. Say: "Build gold files for SC06, SC13, SC15 and LONGPL SC01 from D7 Section 6 and the library's worked examples (A1 Ex3, A2 §12, A3 Ex2 and Ex5, A4 WE1–WE2, B1 §10.4–10.5 and Ex2–4, B3 §8.6, B5 Ex3, C3 Ex5, C5 E3–E4). Every must-have cites a source block ID and the quoted words. List every disagreement between library files."
2. Read each must-have beside its quoted line; answer each disagreement.
3. Say: "Make the seeded twins from D7 Section 6 and lock all eight files."

**Recipe 2. Review one scene (you: 10–15 minutes).**
1. Say: "Run the validator on SC13. If clean, draw the D7 sample, score SC13 with rubric [version], list findings as record, check, severity, quote, fix, and write the review sheet."
2. Answer the ten questions.
3. If the verdict is `revise`, say: "Fix only these findings, change nothing else, re-run the validator, and re-score the affected dimensions."

**Recipe 3. Calibrate (about 1 hour).**
1. Say: "Make a review pack for the SC13 twin: the scene file, its source lines, D7 Sections 3–5 and the gold file, with the instruction to score all nine dimensions, reasoning first, and to list findings with quotes."
2. Paste the pack into a new chat in a second app (for example ChatGPT or Gemini; D1 §5 compares them) and into a new chat in your usual app. First turn off model training in the second app (D1 §8; never free Google AI Studio). Answer the review sheet yourself meanwhile, without looking at either reply.
3. Paste both replies back and say: "Compare the three scorings by D7 Section 8 and ask me only the questions it needs."
4. Answer them, then say: "Record the calibration and update the anchors I changed." If you disagree with a taste score, say why in one sentence; your score stands and becomes an anchor example.

**Recipe 4. Replay after a change (20–30 minutes).** Say: "Replay the gold set and the twins. Compare must-haves, must-nots, scores and seeded-fault detection with the baseline, one line per scene." **If** anything got worse, **then** say "Undo the change."

### 10.1 Templates (copy as written) [J]

**Reviewer instruction** (goes at the top of every review pack; fill the brackets):

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

**Finding** (one per problem; enums as in Section 11):

```json
{"id": "F-SC13-001", "record_id": "SC13-SH310", "check": "vis_2", "dimension": "visual_storytelling",
 "severity": "blocking", "evidence": {"quote": "You.", "line": "l.770", "block_id": "L0770"},
 "fix": "Hold Eli from 'She waits'; cut to Iona only on 'You.' and hold her through 'Silence.'",
 "found_by": "reviewer_a", "status": "open"}
```

**Gold file skeleton** (`assets/examples/gold/SC13.gold.json`):

```json
{"scene": "SC13", "rubric_version": "d7_v1", "source_range": "l.672-829",
 "must_have": [{"id": "MH-01", "quote": "Iona watches her own elbow hit the button.", "block_id": "L0734", "record": "SC13-B06", "check": "dra_5"}],
 "must_not": [{"id": "MN-01", "text": "music under the recording", "check": "res_4"}],
 "acceptable_variants": [{"id": "AV-01", "text": "on 'You.' stay on Iona (A1 Ex3) or hold Eli and cut to her (A2)"}],
 "reference_scores": {"fidelity": 4, "dramatic_accuracy": 4, "visual_storytelling": 4, "continuity": 4, "restraint": 4,
   "feasibility": 4, "estimate": 4, "readability": 4, "downstream_readiness": 4},
 "resolved_conflicts": [{"topic": "tightest frame", "choice": "B15, per A2's sign test", "other_files": ["A1 Ex3", "B1 Ex3"]}]}
```

**Calibration entry** (appended to the film's `calibration[]`):

```json
{"scene": "SC13-twin", "date": "2026-09-28", "rubric_version": "d7_v1",
 "reviewers": {"reviewer_a": "[exact model name]", "reviewer_b": "[exact model name]"},
 "scores": {"reviewer_a": {"visual_storytelling": 1}, "reviewer_b": {"visual_storytelling": 2}, "user": {"visual_storytelling": 1}},
 "resolutions": ["VIS: user and A agree; B missed F2 (palm)"], "alpha": "none", "anchor_changes": []}
```

---

## 11. Fields this subject adds to the breakdown

Enums are lowercase `snake_case`; empty is `"none"`. Fields marked (derived) are written only by the script.

| Level | Field | Meaning | Allowed values / example |
|---|---|---|---|
| film | `rubric_version` | Which rubric text scored the project | `d7_v1`, `d7_v2` |
| film | `reviewer_models` | Exact model names used as reviewers, so a replay can tell a model change from a rubric change (models and their behaviour change; C5 R22) | list of strings |
| film | `gold_set` | Gold and twin files replayed after changes | `gold/SC13.gold.json`, … |
| film | `acceptance` (derived) | Film verdict; each dimension's median and minimum | `accepted` \| `not_yet` |
| film | `calibration[]` | Scene, reviewers, scores, resolutions, alpha, anchor changes, date | object list |
| scene.review | `rubric_scores` | Score per dimension: `fidelity`, `dramatic_accuracy`, `visual_storytelling`, `continuity`, `restraint`, `feasibility`, `estimate`, `readability`, `downstream_readiness` | integers 1–4 |
| scene.review | `rubric_version` | Rubric text used for these scores (scores from different versions are not compared) | `d7_v1` |
| scene.review | `sample_shots` (derived) | Shots read | shot IDs |
| scene.review | `sample_seed` (derived) | Seed of the random pick: scene ID and fix round | `SC13:r0` |
| scene | `key_scene` (derived) | Whether the user answers the whole review sheet (D16 `structure_role` not `none`, or `gold: yes`) | `yes` \| `no` |
| scene.review | `findings[]` | `id`, `record_id`, `check`, `dimension`, `severity`, `evidence` (quote and line), `fix`, `found_by`, `status` | severity `blocking` \| `minor`; found_by `validator` \| `reviewer_a` \| `reviewer_b` \| `user`; status `open` \| `fixed` \| `wont_fix` |
| scene.review | `verdict` | Outcome | `pass` \| `revise` \| `escalate` |
| scene.review | `round` | Fix rounds so far | `0`–`3` |
| scene.review | `review_sheet` | The user's ten answers and notes | `yes` \| `no` \| `unsure` |
| scene | `gold` | This scene is a gold reference | `yes` \| `no` |
| shot | `shot_role` | A2's role, written in `snake_case` | `key` \| `must_keep` \| `normal` |
| twin | `seeded_faults[]` | `fault_id`, `record_id`, `description`, `expected_check`, `severity` | object list |

---

## 12. Failure modes

| Failure | Sign | Fix |
|---|---|---|
| Reviewer grades itself | All 4s on a scene the user dislikes | Different model or fresh session; run the twin first |
| Code coverage passes, picture fails | l.798 is cited by a shot, but no frame shows the palm | Add a record-derived `ask` check (rule 3; Section 13, F2) |
| Sample misses a fault | The user finds a bad normal shot in a passed scene | Widen the sample (rule 6); check the seed |
| Scores drift over time | The same kind of shot scored 4 in week one and 2 in week five | Version the rubric; replay the gold set (rule 9, Section 6.6) |
| Gold over-fits one script | Every rule tuned to *The Catch* | Keep LONGPL SC01; add each new project's first hand-checked scene |
| User overwhelmed | Review sheets skipped | Questions 1–3 per scene; the full sheet for key scenes |
| Calibration never converges | Alpha jumps between runs, or stays below 0.667 on VIS and RES | Keep the user on taste dimensions (rule 15); use the practical gate (Section 8 step 5); rewrite the anchor the reviewers split on |
| Gold points at the wrong line | A must-have fails after re-running intake, though the breakdown did not change | Cite block ID plus quote (rule 11); re-run the quote finder |
| Rubric used as a style mandate | A different but valid choice is marked down | Acceptable variants in the gold file (rule 10) |

---

## 13. Worked example: a flawed SC13 scored against the gold

The seeded twin keeps the gold breakdown and plants five faults (shot IDs illustrative [J], written short: `SH300` is stored as `SC13-SH300`). Every one is blocking.

**F1. Ping-pong on the confession.** B10, "One body." / "One." / "You." (l.764–770).
- Gold: hold Eli while "She waits"; cut to Iona only on "You." and hold her through "Silence." (l.772) (A2; A1's variant stays on Iona).
- Twin: `SH300` Eli "One body." → `SH310` Iona "One." → `SH320` Eli "You." → `SH330` Iona "Silence."
- Caught by VIS-2 (A1.4, A1.15): the reveal lands on the speaker. A script can pre-flag three or more consecutive one-line singles alternating between speakers.

**F2. The palm is cited but never seen.** B12, "She opens her mouth. Nothing in it." / "She looks down at her palm, where the sill took the skin off." / "He watches her look at it." (l.796–800).
- Gold: Iona single; the palm framed to rhyme with SC06 l.286; Eli watching.
- Twin: Iona's single cites l.796–798, but its `subjects` and `props` hold no palm; the next shot is Eli (l.800).
- FID-1 passes because l.798 is cited: citation is not picture. The record-derived question "Does any shot citing l.798 show `CH-IONA`'s skinned palm?" → no. VIS-5, on TP2's key shot.

**F3. A push-in on Eli.** B10.
- Gold: no move; the scene's one push-in is saved for Iona in B15.
- Twin: a slow push-in on Eli from "What was it rated for?" (l.759) through "You."
- Caught by RES-1 (a count: two push-ins, budget one) and RES-2 (the line already states the reveal; B1 principle 11).

**F4. Music under the recording.** B6–B7, from "On the screen: the shot." (l.730) to l.742.
- Gold: silent footage; room tone, the monitor's hum, the remote's click (A4 WE2).
- Twin: cue `MU-SC13-01`, "low strings, sorrowful", l.730–742, with no "must not" line.
- Caught by RES-4 (A1.17; A4s.8; D9: no music under open reveals).

**F5. The axis crossed by a bare cut.** B8, "You did that." / "Yes." (l.745–748).
- Gold: both singles from the bed-head side (B3 §8.6), Iona looking frame-right, Eli frame-left; the new line is set by her head turn in B7.
- Twin: Iona from the bed-head side, then a hard cut to Eli shot through the glass from Saye's side, so both look frame-right.
- Caught by CON-3, a script check: consecutive singles of two speakers with the same eyeline side and no bridge (A2.18, A4h.2).

**Scores.**

| Dimension | Gold | Twin | Reason |
|---|---|---|---|
| Fidelity | 4 | 4 | Every line cited; F2 counts under VIS |
| Dramatic accuracy | 4 | 4 | Beats and turns unchanged |
| Visual storytelling | 4 | **1** | F1, F2 |
| Continuity | 4 | **2** | F5 |
| Restraint | 4 | **1** | F3, F4 |
| Feasibility | 4 | 4 | Eli's 30-word account (l.775–777) is split at its "(beat)" into 17 and 13 words, under 2.5 per second (and within the stricter constant: 17 words fit an 8 s clip, 2.5 × (8 − 1) = 17.5) |
| Estimate, Readability, Downstream | 4 | 4 | Unchanged |
| **Verdict** | `pass` | `revise` | VIS and RES at 1; Continuity, a fact dimension, below 3 |

**The user's sheet on the twin.**
- Question 3, `no`: "the push on Eli feels like the big moment, but her last line is."
- Question 4, `no`: "we keep jumping to whoever talks."
- Question 6, `yes` (not the answer wanted): "the strings feel like TV."
- Question 8, `unsure`.
- Question 9, `no`: "she looks at her hand and we never see it."

The sheet finds four of the five faults in plain words; the axis fault needs the script. The two layers cover each other.

**Fix message:** "Fix only findings F1–F5 in SC13, change nothing else, re-run the validator, and re-score VIS, CON and RES." A reviewer that misses F2 or F5 fails the Section 6.6 detection test and reviews no real scene until fixed.

**The same test on prose.** A LONGPL SC01 twin whose keeper's hand shows "a burn gone silver across the back of the right one" (l.47, Melek's hand) contains an unflagged invention. It answers the book's open question of who the keeper is (A3 rule 21), so it is FID-4, blocking: Fidelity drops to 2 and the scene fails.

---

## 14. Conflicts and open questions

1. **SC13's tightest frame.** A2 puts the tightest size and the push-in on B15 ("I wasn't asking her."); B1 Ex3 puts the closest framing on "You.", and A1 Ex3 calls "One body." / "One." / "You." "the turn". The gold follows A2's sign test [J]: "You." deepens value A without changing its sign, so it is a reveal inside B10. **Flag for the user.**
2. **Push-in on the footage.** A2's B7a pushes in on it; B1 §10.4 says the security camera "never moves and is never re-framed; the characters can only pause, rewind, and (on a monitor) digitally enlarge", and B1 allows one push-in per scene. The gold keeps the footage static (A4 WE2). A digital enlargement that a character visibly performs would be a story event, not a camera move, and would need its own line in the script; none exists.
3. **Master row order.** A2 lists Iona, Jude, Eli from the monitor; B3 §8.6's rendered plan reads Eli, Jude, Iona from frame-left. The gold follows B3; the singles agree.
4. **SC15's pump before the strip** (B5 Ex3) reverses the script's order: accepted as a logged addition.
5. **`must-keep`** (A2) must be written `must_keep` (C5 R29). C5 §10.2 also gives the beat a key-shot flag; the pipeline should store `shot_role` on the shot and derive the beat flag from it, so the two cannot disagree [J].
6. **Eli's hidden hand.** C5 E3's example says "right hand"; the script says "His other hand" (l.224); no library file decides it. The gold tests only that the hand is hidden. **Flag for the user** at checkpoint B, with the other sided details (critic: character states and sides).
7. **SC06 screen time.** A4 WE1 (about 12 s over about 36 shots), B1 (real time, no slow motion) and C4 (a physical fall of about 1.2 s) disagree; the gold follows the critic's resolution (expanded time from overlapping real-time slices, no slow motion). **Flag for the user.**
8. **Music policy.** D9's default is `none`, C3 keeps every clip music-free, and the film policy is the user's choice at checkpoint B. The gold must-nots on music (SC06, SC13, SC15) hold under any policy, because A4 WE2 and D9's "none under open reveals" forbid a cue there even in a scored film.
9. **Mirror state of replayed footage.** The SC13 gold mirrors the SC06 recording as a phase-B picture (B1's recommendation, adopted by the critic as a default); this depends on the phase boundaries the user has not yet confirmed. **Flag for the user.**
10. **Line numbers versus block IDs.** This file cites file lines (l.224); D14 stores block IDs (`L0224`, `ch01.p007`) with the line as `original_ref`. Gold files use block ID plus quote (rule 11).
11. **Emotion words.** DRA-4 bans them in performance fields; D15 R1 allows them in `notes` and in voice delivery. The validator's word list must skip those two fields.
12. **Alpha thresholds may be unreachable.** Co-Director's human raters agreed at α 0.58–0.64, below Krippendorff's 0.667. If the user and the LLMs cannot reach it either, the LLM never takes over a taste dimension (rule 15); the practical gate in Section 8 step 5 is the fallback.
13. **Open:** should the user score all nine dimensions or only four (this file: four)? Krippendorff's thresholds come from content analysis, untested on film breakdowns [J]. The 10% sample, ±10% tolerance and pass marks are starting values. Should a later Long Places chapter (VII, A4 WE4) join the gold set?

---

## Sources

**Library:** the checklists named in Section 3; the worked examples named in Recipe 1; C5 §2, §5, §6.6–6.10, §10, E3–E4; the C5 digest's P5, P9, P10, P13; D1 §4 rule 9, §5, §8; D9 §3–4; D13 §11–12; D14 §11 (block IDs); D15 §3 R1; D16 §7 (`structure_role`); `design/critic_result.json` (conflicts on SC13, SC06 time, sides, music). Test sources: *The Catch* and *The Long Places*, lines as quoted and re-checked against the uploaded files on 2026-09-28.

**Web (all checked 2026-09-27; the first nine re-opened 2026-09-28 and their quotes matched):**
- Anthropic, "Define success criteria and build evaluations" (grading methods; LLM-grading tips): https://platform.claude.com/docs/en/test-and-evaluate/develop-tests [V]
- Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (2023), self-enhancement and position bias: https://arxiv.org/abs/2306.05685 [V]
- Wang et al., "Large Language Models are not Fair Evaluators" (2023), order effects: https://arxiv.org/abs/2305.17926 [V]
- Liu et al., "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment" (2023), bias toward LLM text: https://arxiv.org/abs/2303.16634 [V]
- Kim et al., "Prometheus: Inducing Fine-grained Evaluation Capability in Language Models" (2023), rubrics plus reference answers: https://arxiv.org/abs/2310.08491 [V]
- Shankar et al., "Who Validates the Validators?" (2024), criteria drift: https://arxiv.org/abs/2404.12272 [V]
- Krippendorff's alpha: definition and thresholds, citing Krippendorff (2004) pp. 241–243. https://en.wikipedia.org/wiki/Krippendorff's_alpha [V, secondary]
- ISO 24495-1:2023, "Plain language — Part 1: Governing principles and guidelines" (June 2023): https://www.iso.org/standard/78907.html (the page refused automated reading; title and date confirmed by search, 2026-09-28); principles as quoted by the International Plain Language Federation: https://www.iplfederation.org/iso-standard/ [V, secondary]
- Song et al., "Co-Director: Agentic Generative Video Storytelling" (27 April 2026), Section 5.2 and Table 2 (MLLM–human α 0.469–0.592; human–human α 0.578–0.641; 50 scenarios, 5 raters, advertising): https://arxiv.org/abs/2604.24842 (full text at https://arxiv.org/html/2604.24842) [V, 2026-09-28]
- Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet" (ICLR 2024), §4 on multi-agent debate versus self-consistency: https://arxiv.org/abs/2310.01798 [V, 2026-09-28]
- `krippendorff` Python package 0.8.2 (3 Nov 2025), `alpha(..., level_of_measurement="ordinal")`, default "interval": https://pypi.org/project/krippendorff/ and https://github.com/pln-fing-udelar/fast-krippendorff [V, 2026-09-28]
- Via C5 (verified there, 2026-09-27): StoryAgent https://arxiv.org/abs/2411.04925 ; CineForge https://arxiv.org/abs/2608.29621 ; PACE https://arxiv.org/abs/2609.19853 ; Anthropic skill best practices https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
