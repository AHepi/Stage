# D16. Film-Level Story Structure: Acts, Sequences, Climax, and One Source for Every Peak

*Library file D16. Written 2026-09-27; fact-checked 2026-09-27 (every quote re-found in both test sources; 19 web sources re-fetched; every cross-reference to another library file re-read). Test sources: "The Catch" (screenplay, 25 September 2026 workshop revision, 30 scene headings, about 9,200 words) and "The Long Places" (prose, 14 chapters, about 49,000 words).*

> **What this file is for**
> 1. It fixes the whole film's shape once: the core value, the inciting incident, the act breaks, one sequence list, the crisis, the single climax and the secondary peaks.
> 2. It gives every scene a sequence ID, an act, a structural role and the core value's charge after it, so every visual plan keys to the same map.
> 3. It adds a peak register: each craft component names where it peaks, and any peak away from the climax states an allowed reason.
> 4. It shows the method on *The Catch*: why the library's three climax scenes (named by four files) are really a crisis, a payoff and a climax, and how B2's 23 rows and B3's 9 stretches become one list.
> 5. It shows the same pass at book level for *The Long Places*, and how it carries into D2's three plans.

**Evidence labels.** [V] verified at the named source on 2026-09-27; [V-sec] verified only in a secondary source; [U] unverified; [J] this file's judgment, including arithmetic on the test sources.

**Cross-reference numbering.** Rule and section numbers for other library files are the main files' own (for example B4 R2, B3 §2.6). The digests renumber their rules; where the first draft cited a digest number, it is given in brackets ("B4 R2, digest rule 9").

**Place in the pipeline.** C5 stage 1 (story analysis) drafts `story_structure` inside `story_analysis.json`. D2's macro pass may cut or merge scenes, so the structure is re-checked on the step outline. The user approves it on one extra page at D2's **checkpoint M**. It is then locked, and A2, A4, B1–B5, D9 and C5's checkpoint C read it; none of them re-derives it.

---

## 1. Words this file uses (one word per concept)

| Word | Plain meaning |
|---|---|
| **Core value** | The one value in the protagonist's life that the whole story turns on, with a + and a − pole (A2's term, fixed once per film here). A2's per-scene `core: true` marks a scene's own main value, which may differ. |
| **Charge** | Where a value stands, from −−− to +++, or +/− for mixed, with an optional qualifier (A2). |
| **Turn** | A change of charge. A **major reversal** swings two or more steps or changes sign. |
| **Dramatic question** | The yes/no question the inciting incident raises and the climax answers. Gulino's "main tension" [V]. |
| **Inciting incident** | The on-screen event that first upsets the protagonist's life and raises the dramatic question. |
| **Act** | A run of whole sequences ending in an act climax. |
| **Act climax** | The major reversal that ends an act and changes the protagonist's plan. |
| **Midpoint** | A turn near the middle that changes the goal. Optional. |
| **Sequence** | Consecutive scenes that pursue one short-term question and answer it at their end. IDs `SQ01`… |
| **Sequence climax** | The turn that ends a sequence. |
| **Segment** | A run of scenes inside one sequence that shares place, time or light. IDs `SQ01a`…. It is the only finer unit. |
| **Crisis** | The protagonist's hardest choice, which causes the climax. |
| **Climax** | The scene, or unbroken run of CONTINUOUS scenes, where the core value turns for good. There is exactly one. |
| **Resolution** | Everything after the climax. |
| **Secondary peak** | A structural high point other than the climax: the inciting incident, the act climaxes, the midpoint, the crisis, the hinge payoff. |
| **Hinge payoff** | The reveal of the hinge motif whose change falls closest to the climax; B4 R2 (digest rule 9) gives it the film's largest single payoff. A hinge is a motif that crosses from one pole of the theme's opposition to the other (B4 §3.1 step 4). |
| **Decisive beat** | The one beat inside the climax where the value turns for good (in *The Catch*, "The engine crosses."). |
| **Cardinal function** | An event the plot cannot lose: remove it and later events stop making sense (Barthes' term via McFarlane; D2 §1, A3 §7.1). D2 lists them as CF01…; every structural role must sit on one. |
| **Step outline** | D2's scene-by-scene plan of the film after cuts and merges; the structure is re-checked on it. |
| **Checkpoint M / checkpoint C** | M: the user's approval of D2's macro plan, where this file's one-page structure summary is shown. C: C5's review of the one-line shot list, one sequence at a time. |
| **Word %** | The share of the source's words that come before a quoted line; a cheap stand-in for screen time before shots exist. |
| **Component** | One craft layer that has its own film-wide maximum: story intensity (B3), saturation (B2), longest hold (A4), the camera's break (B1), largest payoff (B4), and so on. |
| **Component peak** | The one place a component reaches its film-wide maximum. |
| **Displaced peak** | A component peak that is not in the climax. It needs an allowed reason (§6). |
| **Counterpoint** | Deliberate visual calm under a story peak (B3 §2.5). |
| **Position check** | Comparing where the roles fall (as % of runtime) with the usual ranges, to raise flags only. |
| **Structure run** | One independent LLM pass that proposes the whole structure. |
| **Screen order** | The order the audience sees events, flashbacks included. |

---

## 2. Core principles

- **P1. One map, many layers.** Structure is decided once, by this file. Every component reads it; none derives its own climax.
- **P2. Values first.** A role is a claim about a charge. Every role cites a quoted line and the charges before and after.
- **P3. Crisis is not climax.** The choice and the result can sit in different scenes. Most disagreements about "the climax" are this confusion.
- **P4. Loud is not high.** The biggest spectacle is often the crisis or a payoff. The climax is where the value turns for good, and it may be staged quietly.
- **P5. Sequences are the working unit.** Acts are too coarse to plan colour or review shots; scenes are too fine. Components needing finer steps use segments nested inside sequences.
- **P6. Percentages flag; they never place.** Beat-sheet positions check a proposal; they never choose a scene.
- **P7. The LLM proposes, the user decides.** Several runs, options where they disagree, a human pick at checkpoint M (C5 R14).
- **P8. Peaks are a budget.** A component peak away from the climax spends the climax's room, so it must state its reason.

---

## 3. Three methods compared, and the one chosen

| Method | What it gives | Good for this pipeline | Weak for this pipeline |
|---|---|---|---|
| **McKee's five-part design and act climaxes** (*Story*, 1997) | "A story is a design in 5 parts: The Inciting Incident, Progressive Complications, Crisis, Climax + Resolution" (McKee's own post) [V-sec]. Acts end in major reversals that build toward the story climax. Crisis is the decision; climax is the action that results [V-sec]. | It uses A2's words (value, charge, turn) at film scale. It gives tests for "which scene is the climax", and it separates crisis from climax. | The number of acts varies. McKee's site says full-length films run "three-, four-, five- or more act[s]" [V], and it says nothing about sequence length. |
| **The sequence approach** (Frank Daniel, written up by Paul Gulino, *Screenwriting: The Sequence Approach*, 2004) | Gulino: "A typical two-hour film is composed of sequences—eight- to fifteen-minute segments that have their own internal structure—in effect, shorter films built inside the larger film" [V, book text]. "In general, a two-hour film will have two fifteen-minute sequences in the first act, four in the second, and two more in the third", with "Variations … mostly in the length of the sequences and sometimes in their number" [V, book text]. His own analyses include *The Graduate* with seven sequences and *North by Northwest* with nine, "ranging in length from nine to eighteen minutes" [V, book text]. A sequence's issues are "only partially resolved within the sequence" [V, book text]. Gulino on tension: "Your character wants something, are they going to get it or not?" [V, Film Courage]; the film-wide version is the dramatic question, "known as the main tension" [V, book text]. | It supplies the missing middle unit, with a boundary test: a question and its answer. | It is calibrated on two-hour features. Boundaries are partly judgment. |
| **A beat sheet** (Snyder's *Save the Cat!*; Hauge's five turning points as used in TRIPOD) | Snyder has "15 story beats from Opening Image to Final Image" [V, savethecat.com]. Guides put Catalyst at about 10%, Midpoint at 50%, All Is Lost at 75% and Break Into Three at 80%, and say "the percentages serve as a guide, rather than a prescriptive formula" [V-sec, Reedsy]. TRIPOD (Papalampidi, Keller and Lapata 2019, citing Hauge, spelled "Hague") defines five turning points: Opportunity, Change of Plans, Point of No Return, Major Setback, Climax, and gives "rules of thumb": "the Opportunity occurs after the first 10% of a screenplay, Change of Plans is approximately 25% in" [V]. Its Table 3 sets theory at 10, 25, 50, 75 and 94.5% and measured, on 84 annotated synopses, means of 11.4, 31.9, 50.7, 74.2 and 89.4% with standard deviations of 6.7, 11.3, 12.2, 8.4 and 4.7 points [V]. | Quick position checks, now with measured spreads. TRIPOD also measured how far humans agree. | Templates invite forcing a story into slots. B3 §2.5 notes that summaries of Block's examples show stories need not follow textbook order. |

**What the evidence says about reliability.**
- Two human annotators picked the same synopsis sentence for a turning point 64.00% of the time (mean distance 4.30% of the synopsis). On full screenplays (six doubly annotated films) their scene choices overlapped by only 35.48% on average (shared scenes ÷ all scenes either picked); at least one scene was shared for 56.67% of turning points, and the nearest picks were a mean 1.48% of the script apart. The authors: "annotators rarely indicate the same scenes", but pick "scenes which are in close proximity", and "annotating the synopses first limits the degree of overall disagreement". Turning points 1, 4 and 5 (Opportunity, Major Setback, Climax) were the easiest to place, 2 and 3 the hardest [V, Papalampidi et al. 2019].
- On turning-point identification, Gemini and Claude averaged "over 30%" accuracy and GPT-4 26%, against a human 46.6% [V, Tian et al. 2024, 2024-era models].
- When they write stories, LLMs show "a substantial advancement (i.e., early occurrence) of TP4 and TP5" [V].
- Consequences [J]: work on a one-line event list first, then map to scenes. Accept a range of one scene either way. Run several passes. Distrust a climax proposed early.

**Chosen procedure: values first, sequences second, percentages last** [J].
1. McKee's definitions and tests decide every role.
2. The sequence approach groups the scenes.
3. Beat-sheet and TRIPOD positions only raise flags.
4. Thompson's four large parts (setup, complicating action, development, climax; "A short epilogue usually follows the climax" [V-sec]), described in secondary accounts as roughly equal in length [V-sec], serve as an optional cross-check of the midpoint.

Block's story-intensity graph stays in B3. It reads this file's roles.

---

## 4. Decision rules

"Then" is firm; "then consider" is a default, overridden only with a one-line reason in `story_structure.notes`.

**Shape and value**
- **R1.** If any stage needs a film-wide high point (climax, act break, sequence, peak), then it reads `story_structure`, because four files that derived their own named three different climax scenes for *The Catch* (B2's fire and B5's turning scene at SC24, B4's largest payoff at SC25, B3's 10 at SC26–27).
- **R2.** If the finished work runs under about 30 minutes and has no major reversal before the end, then set `structure_shape: one_act` (inciting incident, climax, resolution, no act climaxes), because McKee: "If a story spans only one movement with no major turnings, it usually asks its audience for less than 30 minutes of performance time" [V]. If the work is a series, set `series_arc` (R24). If it is a string of loosely linked episodes with only a thin through-line (an anthology, a road film of separate stops), set `episodic`: still name one climax (the last major reversal of the through-line) and treat each episode's peak as a `sequence_climax`. Otherwise set `multi_act`.
- **R3.** If you are choosing the core value, then chart two or three candidates in the protagonist's life across all scenes. Pick the one whose last big turn meets three conditions: (a) it is the story's last major reversal; (b) it is caused by the protagonist's own action; (c) it answers the dramatic question. A value chosen for theme alone can point at a payoff instead of the ending's turn. If no candidate meets all three (a passive protagonist, an ending that happens to her), then choose the one meeting (a) and (c), set the climax's `turn_kind` to `revelation` or `external`, and put the choice in `open_questions` for checkpoint M.
- **R4.** If the charge a character knows differs from the true one, then score the film-level charge by what has truly happened (what the audience has seen) and put the character's view in an `audience_knows` note, because roles must not move when a character learns late. In SC06 *The Catch* turns; Iona starts to see it in SC07 ("Every letter is backwards.") and has it proved in SC10 ("Not mint."). This applies A2's "Record both when they differ" at film scale; A2's own per-scene charges stay scored from the character's view (A2 Step 2), so the two may differ by design.

**Roles**
- **R5.** If one scene holds the protagonist's hardest choice and a later one holds the action that turns the core value for good, then label them `crisis` and `climax`, because McKee separates decision from result [V-sec].
- **R6.** If the decisive turn spans CONTINUOUS scenes, then the climax may be that unbroken run, with one `decisive_beat`, because B3 allows exactly one scene "or one continuous sequence" at 10.
- **R7.** If you are choosing the inciting incident, then keep only candidates that pass all four tests:
  1. It is dramatized on screen, not backstory.
  2. It swings the core value two or more steps, or first raises the dramatic question.
  3. Mirror test: the climax answers it.
  4. Deletion test: remove it and the climax loses its cause.

  Pick the earliest candidate that passes. An earlier plant or complication is not an inciting incident. (McKee's on-screen requirement, "The inciting incident of the central plot must happen on screen", while a subplot's "may or may not be seen on screen": [V-sec], from a reader's notes on *Story*; Wikipedia's "Three-act structure" also calls it "a dynamic, on-screen incident" [V].)
- **R8.** If the source marks its own break (a title card, a part heading, "END OF ACT", an intermission, or a cut to black followed by a card), then test that break first as an act boundary, because the author's structure outranks an inferred one. D14 R34 keeps every such break as a block with a `break_kind` (`card`, `cut_to_black`, `part`, `intermission`…); D14 only records breaks, and this rule decides whether each is an act break.
- **R9.** If you are placing act climaxes, then choose major reversals of the core value that change the protagonist's plan. Check that their stakes escalate and that B3's scores at them do not fall, because McKee's multi-act films "progress their conflicts around major turning points to an all-or-nothing climax" [V].
- **R10.** If a structural turn falls mid-scene, then the boundary is the scene boundary after it, because the scene is the pipeline's record unit (C5).
- **R11.** If the work has subplots, then record each in `subplots[]` with its own value and turns, because a subplot climax is not the climax. A subplot's peaks rank below the climax on the register.

**Sequences**
- **R12.** If you are grouping sequences, then each one must:
  - consist of consecutive scenes;
  - answer one short-term question at its end, with a quoted line;
  - end inside the act it starts in;
  - fall within a count set by the finished runtime: **6–10** for any film or episode of 25 minutes or more; **3–6** under 25 minutes. If the count falls outside, merge or split at the weakest question and give a reason, or accept it with a note (the check is a warning).

  This follows Gulino's "shorter films built inside the larger film" [V] and his own counts of seven to nine in finished features [V], and gives checkpoint C one review of about ten minutes per sequence (C5). The count for works under two hours, and the 25-minute line, are [J]: on *The Catch* (about 35 minutes as written) nine sequences run 2–7 minutes each.
- **R13.** If a component needs finer steps (colour script rows, visual stretches), then use segments with IDs such as `SQ03b`, never a separate numbering, because B2's 23 rows and B3's 9 stretches could not be joined without a map.
- **R14.** If a component's own grouping straddles a sequence boundary, then re-key it by segments and keep its values, because the values were sound and only the IDs were in conflict.

**Peaks**
- **R15.** If a component peak is not in the climax, then give a `displaced_reason` from §6 and meet that reason's constraint; otherwise move the peak or ask the user, because unexplained peaks spend the climax's room (A2 R31: "Do not spend the film's tightest size or longest hold before its climax"; B3 §2.6 step 2: "There must be one highest peak (the climax)").
- **R16.** If the climax is in counterpoint, then it must still own at least three component peaks: `core_value_turn`, `story_intensity` 10, and at least one of `longest_hold`, `camera_break` or `tightest_size`. A calm climax needs other layers to mark it.
- **R17.** If you are scoring secondary peaks, then keep each at least one step below the climax on every component that the register places in the climax, except the one component whose displaced peak that scene holds, because intensity needs room (B2 R9, after Block). Components with no register row (for example B2's light-dark contrast, already "extreme" in SC01–02 of *The Catch*) are not checked by this rule.

**Running it with an LLM**
- **R18.** If an LLM proposes the structure, then make three independent structure runs (fresh chats, same prompt) and compare four roles: the inciting incident, each act climax, the crisis and the climax. If, for every role, all three runs name the same scene or scenes no more than one scene apart, accept the majority. If any role differs by more than one scene, or the runs choose different core values, show the options side by side at checkpoint M. Humans themselves share only about a third of their scene picks, though their picks usually sit close together [V].
- **R19.** If you are finding turns, then work on the one-line event list first and map to scene IDs second, because TRIPOD's annotators agreed far more on synopsis sentences (64% exact) than on scenes (35% overlap), and its authors found that annotating synopses first "limits the degree of overall disagreement" [V].
- **R20.** If a role falls outside the usual range, then flag it. Never move it for that reason alone, because templates pull stories into slots and LLMs already place climaxes early [V]. Measure each role twice: runtime % over its whole scene span (D2 seconds or D13 v0), and word % at its quoted line. Raise a flag only when both measures fall outside the window; where only one measure exists (a projected plan with no source line, or the resolution's length), use it alone. The flags are:
  - inciting incident after 30% (TRIPOD's measured mean 11.4% plus three standard deviations is about 31%);
  - first act climax outside 20–35% (TRIPOD's Change of Plans averaged 31.9% with a spread of 11.3 points, so treat 35–43% as a soft flag);
  - climax before 70% (TRIPOD's climax averaged 89.4%, spread 4.7);
  - resolution longer than 20% of runtime.

  The windows are [J], checked against TRIPOD's Table 3 [V].

**Change and scope**
- **R21.** If D2 cuts or merges scenes, then recompute every role on the step outline. Each role scene must be one of D2's cardinal functions, and removing one needs the user's explicit approval (D2 P3).
- **R22.** If the user changes the climax, then rebuild the peak register and list every component whose peak is now unexplained.
- **R23.** If the source is prose, then build the structure for the whole book first and project it onto the approved step outline. If the film's climax is not the book's, then D2's log says why.
- **R24.** If the format is a series, then build two levels: the season (the whole work) and each episode. Each episode gets its own inciting incident, climax and sequences (R12's count by the episode's runtime), with IDs like `E6-SQ03`. The season climax falls in the last episode, and D2's episode `value_arc` is the episode's core value.
- **R25.** Always compute structure in screen order, because the audience experiences peaks in that order.

---

## 5. The recipe (an LLM does the work; the user reads one page)

**Inputs:** the locked scene list (C5 stage 0), the one-line event list and cardinal functions (C5 stage 1, D2 M2), and the runtime estimate per scene (D2 §6, D13).

1. **Event list.** One past-tense line per scene, with one exact quote and a line reference. Reuse D2's list.
2. **Core value.** Ask for three candidate values in the protagonist's life, each charted scene by scene. Apply R3.
3. **Climax and crisis.** For the chosen value, find where it turns for good (R5, R6). Name the crisis. If they fall in one scene, say so.
4. **Inciting incident.** Take up to three candidates from the first third and run R7's four tests.
5. **Acts and midpoint.** Test author-marked breaks first (R8), then major reversals (R9). Name a midpoint only if the goal changes near 50%.
6. **Sequences and segments.** Group scenes under R12, then list segments where place, time or light changes (R13).
7. **Charges and roles.** Fill `charge_by_scene` and each scene's `structure_role`.
8. **Position check.** A script (not the LLM; C5 R23) computes runtime % over each role's scene span from D2's per-scene seconds (or D13's v0 estimate) and word % at each role's quoted line. Flag under R20.
9. **Peak register.** One row per component (§6), filled from the component files or marked `to_place`.
10. **Three runs.** Repeat steps 2–6 twice in fresh chats with the same prompt, then paste the three JSON answers into a fourth chat with the comparison prompt below and apply R18.
11. **Checkpoint M page.** Fill the page template below. The user answers "approved" or changes one item at a time ("make SC24 the climax"; "use SC01 as the inciting incident"). A change to the climax triggers R22. Then lock: set `structure_checkpoint.status: approved`.

**What the non-technical user does** (about 15–20 minutes at checkpoint M for a short film [J]): read the one page; for each line marked OPTION, say which one you want; check that each quote really is where the page says (open the script and search for it); say "approved". You never edit the JSON yourself.

**Prompt for steps 2–7** (paste with the event list):

```
You are running the film-structure pass (library file D16). Use only the scene IDs and quotes given; do not invent events.
1. Propose three core values in <PROTAGONIST>'s life as "+ pole / - pole". For each, give the charge after every scene (--- to +++, or +/-), and the scene where it turns for good. Say for each whether that turn is (a) the last major reversal, (b) caused by the protagonist's action, (c) the answer to the story's first question. Choose one.
2. Name the crisis (hardest choice) and the climax (action that turns the core value for good), each with scene ID and exact quote.
3. List up to three inciting-incident candidates from the first third; run four tests (on screen; swings the value two steps or raises the question; the climax answers it; deletion). Choose the earliest that passes.
4. Mark act climaxes (author-marked breaks first), then sequences: consecutive scenes, one question each, answered by a quoted line, never crossing an act break, 6-10 in total.
5. Output JSON in the story_structure format. Put every uncertainty in open_questions.
Repeat the task in one sentence before answering, and again at the end.
```

In line 4, replace "6-10" with "3-6" when the finished film will run under 25 minutes (R12).

**Comparison prompt for step 10** (paste with the three JSON answers, labelled RUN 1, RUN 2, RUN 3):

```
Compare these three structure runs for the same script. Do not re-analyse the script.
Make one table with a row for each of: core value, inciting incident, each act climax, crisis, climax. Columns: RUN 1, RUN 2, RUN 3, AGREE (yes if all three name the same scene or scenes no more than one scene apart, and the same core value).
Below the table, for every row where AGREE is no, write "OPTION A / OPTION B (/ OPTION C)": the scene, the quote each run gave, and one sentence on what would change downstream if it were chosen.
Do not choose between options.
```

**Checkpoint M page template** (one page; the LLM fills the angle brackets, a script fills the percentages):

```
STRUCTURE FOR <TITLE>  (D16, version <n>, <date>)
Shape: <multi_act | one_act | episodic | series_arc>
Dramatic question: "<quote>" (<scene>, <line>)
Core value: <+ pole> / <- pole>, in <whose> life. Alternatives rejected: <value: reason>.
Inciting incident: <scene> "<quote>" (<runtime %>, <word %>)   OPTION if runs disagreed
Act climaxes: <scene> "<quote>"; <scene> "<quote>"
Midpoint (optional): <scene> "<quote>"
Crisis: <scene> "<quote>"
CLIMAX: <scene or continuous run>, decisive beat "<quote>" (<runtime %>, <word %>)
Resolution: <scenes>
Sequences: <SQ01 title (scenes): question -> "answer quote"> ... one line each
Peak register: <component: scene, reason> ... one line each; any `conflict` rows in CAPITALS
Position flags: <none | list>
Open questions: <one decision per line>
Reply "approved", or change one item at a time.
```
---

## 6. The peak register

| Component (`component`) | Owner | Default peak |
|---|---|---|
| `core_value_turn` | D16 | climax |
| `story_intensity` (the one 10) | B3 §2.6 | climax |
| `camera_break` ("the break") | B1 | climax |
| `longest_hold` (the film's longest shot) | A4 P10 | climax |
| `rupture_double` (cut to black plus true silence) | A4 §6.8 | climax |
| `sound_dropout` | A4, D9 | climax |
| `tightest_size` | A2 R31 | climax |
| `saturation` (the colour component B2 saves for the climax: B2 §4.4; field `climax_component` in B2's digest) | B2 R9 | climax |
| `largest_payoff` (longest held frame among emphasis-3 moments, plus strongest contrast in one component) | B4 R2 (digest rule 9) | climax |
| `sound_emphasis_3` (a sound motif's single loudest moment) | B4, D9 | climax |
| `protagonist_turn` (the turning scene in the protagonist's B5 ARC line; field `turning_scene` in B5's digest) | B5 §7 bible entry | crisis or climax |

**Allowed `displaced_reason` values and their constraints:**
- `crisis`: `peak_scene` equals `story_structure.crisis.scene`.
- `hinge_payoff`: in the last act, before the climax, and listed by B4 as a hinge reveal or payoff.
- `rhyme_plant`: `rhyme_target` names a beat in the climax that repeats this peak with one change (B3 principle 8 "Rhyme, do not repeat" and R9; digest rule 6).
- `coda`: in the resolution, and within the component's "once" budget (B4 principle 5: one emphasis-3 moment per motif; S3, the sound motif heard alone, "Once per sound motif").
- `none`: the peak is in the climax.

**`climax_counterpoint: true`** marks a component that is deliberately calm at the climax (B3). The component's peak must then use one of the reasons above.

---

## 7. Fields this subject adds

Enums are lowercase `snake_case`; an empty value is `"none"` and an empty list is `[]`. Authority marks follow C5: `extracted`, `authored`, `derived`.

| Level | Field | Meaning | Allowed values / example |
|---|---|---|---|
| film | `structure_shape` | Overall shape | `multi_act` \| `one_act` \| `episodic` \| `series_arc` |
| film | `core_value` | `{positive, negative, whose, alternatives[]}` | `{"Home","Stranded","Iona and those she carries"}` |
| film | `dramatic_question` | The question, quoted if the source states it | "Are we going to be all right?" (SC09) |
| film | `inciting_incident` | `{scene, beat, quote, source_ref, candidates[]}` | `SC06`, "A hard metal CLACK." |
| film | `acts[]` | `{act_id, scenes, sequences[], act_climax_scene, quote, charge_close}` | `ACT1`, `SC01–SC10` |
| film | `midpoint`, `crisis`, `climax` | `{scene(s), decisive_beat, quote, source_ref, charge_before, charge_after, turn_kind}` | climax `["SC26","SC27"]`; turn_kind `action` \| `revelation` \| `external` (R3) |
| film | `resolution` | Scenes after the climax | `SC28–SC30` |
| film | `secondary_peaks[]` | `{scene, role, rank}`; rank 1 = highest, ordered by B3 score, ties going to the later scene | role: `inciting_incident` \| `act_climax` \| `midpoint` \| `crisis` \| `hinge_payoff` |
| film | `sequences[]` | `{sequence_id, title, scenes, act_id, question, answer_quote, share_pct}` | `SQ04`, "Taken" |
| film | `segments[]` | `{segment_id, sequence_id, scenes, place_time}` | `SQ04b`, `SC17` |
| film | `subplots[]` | `{value, whose, turns[], resolves_at}` | Trust / Betrayal (Iona toward Eli) |
| film | `charge_by_scene` | Core value's charge after each scene (derived from roles, authored at stage 1) | `{"SC27": "++"}` |
| film | `position_check` | Percentages and flags | `{climax_pct: 83–89, flags: []}` |
| film | `peak_register[]` | `{component, owner_file, peak_scene, peak_role, displaced_reason, rhyme_target, climax_counterpoint, status}` | status `placed` \| `to_place` \| `conflict` |
| film | `structure_runs[]` | Each run's roles, for agreement | derived |
| film | `structure_checkpoint` | Approval, shown at checkpoint M | `{status: pending \| approved, version, date}` |
| film | `notes` | One-line reasons for overriding a "then consider" default, or accepting a flag | `["R12: 9 sequences accepted"]` |
| film | `open_questions[]` | One decision per item, for checkpoint M | `["Climax: SC26–27 (recommended) or SC24?"]` |
| scene | `sequence_id`, `segment_id`, `act_id` | Keys; replace C5's free-text `sequence` | `SQ07`, `SQ07b`, `ACT3` |
| scene | `structure_role[]` | Roles held | the `secondary_peaks` roles plus `climax` \| `sequence_climax` \| `resolution` \| `none` |
| scene | `core_value_charge_after` | Film-scale charge | `−−−` … `+++`, `+/−`, qualifier allowed |
| scene | `audience_knows` (opt) | When the audience is ahead of the character (R4) | "turn seen; Iona sees it in SC07, has it proved in SC10" |

**Validator checks** (C5 style):
1. Exactly one climax, which is one scene or one unbroken CONTINUOUS run.
2. The climax comes after the last act climax.
3. The inciting incident comes before the first act climax.
4. Every scene has exactly one sequence and one act, and no sequence crosses an act boundary.
5. B3 has exactly one 10, placed on the climax, and at most two 9s.
6. The turning scene in the protagonist's B5 ARC line (`turning_scene`) is either the crisis or the climax.
7. Every register row either sits in the climax or carries a valid reason.
8. Every role scene is a D2 cardinal function.
9. The sequence count is 6–10 (runtime 25 minutes or more) or 3–6 (under 25 minutes); a warning only.
10. Every `rhyme_plant` row names a `rhyme_target` inside the climax, and every `coda` row sits in the resolution.
11. The climax's `charge_before` and `charge_after` differ by two or more steps or change sign (a major reversal), and no later scene reverses the core value again.

**Template: `story_structure` for *The Catch*** (abridged; `…` marks repeated rows; fields are `authored` unless marked, and percentages are `derived` by a script):

```json
{
  "story_structure": {
    "structure_shape": "multi_act",
    "core_value": {"positive": "Home", "negative": "Stranded", "whose": "Iona and those she carries",
                   "alternatives": ["Keeps / Gives (her way home)", "Person / Goods (B4 theme)"]},
    "dramatic_question": {"text": "Eli. Are we going to be all right?", "scene": "SC09", "source_ref": "L390"},
    "inciting_incident": {"scene": "SC06", "beat": "CLACK", "quote": "A hard metal CLACK.", "source_ref": "L259",
                          "candidates": ["SC01", "SC03", "SC06"]},
    "acts": [
      {"act_id": "ACT1", "scenes": "SC01-SC10", "sequences": ["SQ01", "SQ02"], "act_climax_scene": "SC10",
       "quote": "Nobody leave this room.", "charge_close": "---"},
      {"act_id": "ACT2", "scenes": "SC11-SC23", "sequences": ["SQ03", "SQ04", "SQ05", "SQ06"], "act_climax_scene": "SC23",
       "quote": "They vanish together.", "charge_close": "+/-"},
      {"act_id": "ACT3", "scenes": "SC24-SC30", "sequences": ["SQ07", "SQ08", "SQ09"], "act_climax_scene": "none",
       "quote": "none", "charge_close": "+"}
    ],
    "midpoint": {"scene": "SC17", "quote": "I sent her.", "source_ref": "L996", "charge_before": "---", "charge_after": "--", "turn_kind": "revelation"},
    "crisis": {"scene": "SC24", "quote": "She deletes the way home.", "source_ref": "L1412", "charge_before": "+/-", "charge_after": "---", "turn_kind": "action"},
    "climax": {"scene": ["SC26", "SC27"], "decisive_beat": "The engine crosses.", "quote": "Nought.", "source_ref": "L1591-L1593",
               "charge_before": "--", "charge_after": "++", "turn_kind": "action"},
    "resolution": ["SC28", "SC29", "SC30"],
    "secondary_peaks": [{"scene": "SC06", "role": "inciting_incident", "rank": 2}, {"scene": "SC24", "role": "crisis", "rank": 1},
                        {"scene": "SC25", "role": "hinge_payoff", "rank": 3}, {"scene": "SC23", "role": "act_climax", "rank": 4},
                        {"scene": "SC10", "role": "act_climax", "rank": 5}, {"scene": "SC17", "role": "midpoint", "rank": 6}],
    "sequences": [{"sequence_id": "SQ01", "title": "Rescue and fall", "scenes": "SC01-SC06", "act_id": "ACT1",
                   "question": "Can she get Eli out alive?", "answer_quote": "This time they hear it land.", "share_pct": 15.2}, "…"],
    "segments": [{"segment_id": "SQ01c", "sequence_id": "SQ01", "scenes": "SC03-SC05", "place_time": "treatment floor, night"}, "…"],
    "subplots": [{"value": "Trust / Betrayal", "whose": "Iona toward Eli", "turns": ["SC06", "SC13"], "resolves_at": "SC29"}],
    "charge_by_scene": {"SC01": "-", "SC06": "--", "SC10": "---", "SC24": "---", "SC26": "---", "SC27": "++", "…": "…"},
    "position_check": {"inciting_pct": "10-15 / 14.6", "act1_climax_pct": "19-24 / 25.3", "climax_pct": "83-89 / 85.6-88.4",
                       "resolution_pct": 11.2, "flags": []},
    "peak_register": [{"component": "saturation", "owner_file": "B2", "peak_scene": "SC24", "peak_role": "crisis",
                       "displaced_reason": "crisis", "rhyme_target": "none", "climax_counterpoint": true, "status": "placed"}, "…"],
    "structure_runs": [],
    "structure_checkpoint": {"status": "pending", "version": 1, "date": "2026-09-27"},
    "notes": [],
    "open_questions": ["Core value: Home / Stranded (recommended)?", "Inciting incident: SC06 (recommended), SC01 or SC03?",
                       "Climax: SC26-27 (recommended), SC24 or SC25?"]
  }
}
```

---

## 8. Worked example: *The Catch*

### 8.1 Core value

| Candidate | Turns for good at | Last major reversal? | Caused by Iona's action? | Answers the dramatic question? |
|---|---|---|---|---|
| Home / Stranded (Iona and those she carries) | SC27: "Nought." / "The engine crosses." (L1591–1593) | Yes; nothing reverses after | Yes; she sets "One turn. Up. Cross at the top of the climb" | Yes; they are back, and in SC29 "In the car-" is answered "Yes." (L1788–1791) |
| Keeps / Gives (her own way home) | SC24: "She deletes the way home." (L1412) | No; SC26 falls to −−− and SC27 reverses | Yes | Partly |
| Person / Goods (how she carries others; B4's theme) | SC25: "Then she straps the vessel to her chest." (L1486) | No; SC26–27 still reverse | Yes | No |

**Recommendation [J]:** Home / Stranded. The dramatic question is the script's own: "Eli. Are we going to be all right?" (L390, SC09), first asked just after the turn. Eli asks it back at the act 2 climax, "Are we going to be all right?" / "I don't know." (L1352–1355, SC23), which confirms SC23 as a structural turn. It is answered in SC29, when Eli's "In the car-" (the place it was first asked) gets "Yes." (L1788–1791). Reading that "Yes." as the answer to the question, and not only as forgiveness, is [J]; B4 already tracks it as M14, "the question asked twice".

### 8.2 Inciting incident

| Candidate | Quote | On screen | Swing / question | Mirror | Deletion |
|---|---|---|---|---|---|
| SC01 | "The safety brakes are gone." (L35) | yes | Raises the danger of a goal already set before the film | weak | The fall needs it, but the turned world does not |
| SC03 | "the crooked half-smile she knows" (L137) | yes | + turn inside the same rescue | no | nothing later depends on it |
| **SC06** | "A hard metal CLACK." / "The cage is going UP." (L259, L267) | yes | + to −−; raises the dramatic question, asked aloud in SC09 ("Eli. Are we going to be all right?") | Yes. Eli turns them without asking (SC13 reveals it: "One body." / "You.", L764–770); in SC26–27 Iona turns herself and the animal after asking: "All of us. I can't do it without you turning too." (L1543) | Nothing after SC06 exists without it |

**Recommendation:** SC06, at 10–15% of runtime and 14.6% of script words. SC01 is recorded as SQ01's own inciting incident. The rescue's real trigger, the photograph of Eli's wrist, is backstory and fails test 1. If the user wants one of the two original candidates, choose SC01.

### 8.3 Acts, midpoint, crisis, climax, and the position check

| Role | Scene | Quote | Runtime % (D2 §6 seconds) | Words % |
|---|---|---|---|---|
| Inciting incident | SC06 | "A hard metal CLACK." | 10–15 | 14.6 |
| Act 1 climax (author-marked, R8) | SC10 | "Not mint." … "Nobody leave this room." then `= THE CATCH` (L463–488) | 19–24 | 25.3 |
| Midpoint (goal changes: go over) | SC17 | "I sent her." (L996) | 48–54 [J split of D2's SC17+18] | 50.9 |
| Act 2 climax | SC23 | "Go." … "They vanish together." (L1360–1370) | 70–76 | 72.4 |
| Crisis | SC24 | "She looks at the flask inside the outline. Leaves it there." … "She deletes the way home." (L1406–1412) | 76–79 | 75.1 |
| Hinge payoff | SC25 | "A suit." … "two outlines turn green, one inside the other." (L1462–1488) | 79–83 | 80.6 |
| **Climax** (decisive beat SC27) | SC26–SC27 | "She pushes gently away from the rail." … "Nought." / "The engine crosses." (L1553–1593) | 83–89 | 85.6–88.4 |
| Resolution | SC28–SC30 | "Three uneven strokes in the dark." (L1850) | 89–100 | — |

Runtime % is the role scene's span in D2 §6's as-written seconds (2,116 s in all; SC17's share of D2's combined SC17+18 row is split by word count [J]). Word % is the share of the script's words before the quoted line (script count, 9,219 words including the title page).

No flags: every role's runtime span meets R20's window, and the resolution is 11.2% of runtime. The two measures agree within about 3 points. *The Catch* reads as three acts (breaks after SC10 and SC23) or as Thompson's four parts (breaks after SC10, SC17 and SC23, giving parts of about 24, 30, 22 and 24% of runtime, close to her roughly equal quarters); the two readings do not conflict.

### 8.4 One sequence list (reconciles B2's 23 rows and B3's 9 stretches)

Each B2 colour-script row is a clean run of scenes, so each row becomes one segment. Each sequence is a union of whole rows.

| Seq | Scenes | Question → answer (quote) | Segments = B2 rows | B3 stretch | Runtime % (min) [J] |
|---|---|---|---|---|---|
| SQ01 Rescue and fall | SC01–06 | Can she get Eli out alive? → "This time they hear it land." | a SC01 (1), b SC02 (2), c SC03–05 (3), d SC06 (4) | sc1–5 and sc6 → SQ01a–c, SQ01d | 15.2 (5.4) |
| SQ02 Wrong world | SC07–10 | What has happened to us? → "Not mint." | a SC07 (5), b SC08–09 (6), c SC10 (7) | sc7–10 | 8.5 (3.0) |
| SQ03 Told | SC11–13 | Will she be told the truth? → "You did that." / "Yes." | a SC11 (8), b SC12 (9), c SC13 (10) | sc11–13 | 19.9 (7.0) |
| SQ04 Taken | SC14–17 | What took them, and where? → "I sent her." | a SC14–16 (11), b SC17 (12) | sc14–17 | 9.3 (3.3) |
| SQ05 Going over | SC18–20 | Can she reach them? → "She lets go of the tool." | a SC18 (13), b SC19 (14), c SC20 (15) | sc18–22, split → SQ05 + SQ06a | 13.8 (4.9) |
| SQ06 The collection | SC21–23 | Can she get them home? → "They vanish together." | a SC21–22 (16), b SC23 (17) | sc23–25, split → SQ06b + SQ07 | 9.2 (3.3) |
| SQ07 Fire and the chest | SC24–25 | Can she contain the fire and still get out? → "The outlines stay green. Just." | a SC24 (18), b SC25 (19) | (as above) | 7.0 (2.5) |
| SQ08 Ledge and crossing | SC26–27 | Can she get home at all? → "The engine crosses." | a SC26–27 (20) | sc26–27 | 6.0 (2.1) |
| SQ09 Return | SC28–30 | What is left between them? → "Yes." | a SC28 (21), b SC29 (22), c SC30 (23) | sc28–30 | 11.2 (4.0) |

Runtime shares come from D2 §6's as-written seconds (SC17+18 split by words) [J]. The acts are ACT1 = SQ01–02, ACT2 = SQ03–06, ACT3 = SQ07–09. Nine sequences fall within R12's range for a film over 25 minutes, and checkpoint C reviews them one at a time. Every question is Gulino's "wants something… get it or not?" at sequence scale, and every answer is a quoted line. A3's rule to keep "up the shaft" as frame-top in scenes 1 to 7 stays a scene-range continuity rule; it may cross SQ01–SQ02.

### 8.5 Scene by scene

"B3" is B3's film-scale intensity (B3 §2.7). B3 gives a range per stretch ("3 → 7"); the per-scene values below are this file's interpolation inside each range, keeping each stretch's start and end values [J]. The only value that contradicts B3 is SC25, lowered from 9 to 8, so that the two 9s are SC06 and SC24 (B3 §2.6 allows 9 "only for the one or two biggest such events before the climax").

| Scene | Seg | Act | Role | Charge after | B3 | Evidence |
|---|---|---|---|---|---|---|
| SC01 | SQ01a | 1 | seq. inciting | − | 3 | "The safety brakes are gone." |
| SC02 | SQ01b | 1 | — | − | 4 | "It was my tooth." |
| SC03 | SQ01c | 1 | — | +/− | 5 | "the crooked half-smile she knows" |
| SC04 | SQ01c | 1 | — | +/− | 5 | "She gives Eli one shoe." |
| SC05 | SQ01c | 1 | — | + | 7 | "Takes the flask and its puck." |
| SC06 | SQ01d | 1 | inciting; seq. climax | −− | 9 | "The cage is going UP." |
| SC07 | SQ02a | 1 | — | −− | 5 | "Every letter is backwards." |
| SC08 | SQ02b | 1 | — | −− | 5 | "The wheel is on the other side." |
| SC09 | SQ02b | 1 | question stated | −− | 5 | "Eli. Are we going to be all right?" / "Drive." |
| SC10 | SQ02c | 1 | act climax | −−− | 6 | "Nobody leave this room." |
| SC11 | SQ03a | 2 | — | −− | 4 | "You brought him back here." |
| SC12 | SQ03b | 2 | — | − | 5 | "Do that to us." / "I can. And you would still be in quarantine." |
| SC13 | SQ03c | 2 | seq. climax; subplot turn | −− | 7 | "You did that." / "Yes." |
| SC14 | SQ04a | 2 | — | −− | 3 | "The needle lies flat." |
| SC15 | SQ04a | 2 | — | −−− | 8 | "The bed, and Jude, and the cup, and the figure are gone." |
| SC16 | SQ04a | 2 | — | −−− | 8 | "A clean square on the floor where Eli's bed stood." |
| SC17 | SQ04b | 2 | midpoint; seq. climax | −− | 5 | "I sent her." |
| SC18 | SQ05a | 2 | — | − | 5 | "Iona steps onto the yellow line." |
| SC19 | SQ05b | 2 | — | −− | 5 | "Stars. Below her feet." |
| SC20 | SQ05c | 2 | seq. climax | − | 6 | "She lets go of the tool." |
| SC21 | SQ06a | 2 | — | −− | 6 | "IONA VALE." |
| SC22 | SQ06a | 2 | — | − | 6 | "It goes." |
| SC23 | SQ06b | 2 | act climax | +/− | 8 | "Go." |
| SC24 | SQ07a | 3 | crisis | −−− | 9 | "She deletes the way home." |
| SC25 | SQ07b | 3 | hinge payoff | −− | 8 | "The outlines stay green. Just." |
| SC26 | SQ08a | 3 | climax | −−− | 10 | "Then not." |
| SC27 | SQ08a | 3 | climax (decisive) | ++ | 10 | "Nought." / "The engine crosses." |
| SC28 | SQ09a | 3 | resolution | + (apart) | 6 | "on the wrong side of his face" |
| SC29 | SQ09b | 3 | resolution; subplot resolves | ++ (through glass) | 4 | "In the car-" / "Yes." |
| SC30 | SQ09c | 3 | resolution | + (uneasy) | 2 | "Three uneven strokes in the dark." |

**Subplot:** Trust / Betrayal (Iona toward Eli). For the audience it cracks in SC06 ("He has one hand she cannot see.", L253); for Iona it strains in SC09 ("Drive.") and falls to −− in SC13 ("You did that." / "Yes."; A2 scores that scene + (uneasy) → −−); it resolves to + in SC29.

### 8.6 The climax options, laid out for the user

| Option | What it is under McKee | Files already there | What changes if chosen |
|---|---|---|---|
| **SC24**, the fire | The **crisis**: her hardest choice, between irreconcilable goods | B2 (saturation peak, row 18, called "the film's visual climax"), B5 (Iona's ARC: "Turning scene: sc24"), D2 (CF11 "The climax choice") | B3's 10 moves here. SC26–27 then sit after the climax yet hold a bigger reversal, which breaks the last-reversal test. B1's break and A4's hold need moving or reasons. |
| **SC25**, the chest | The **hinge payoff**: the theme's reveal (B4: "a person inside goods") | B4 (largest payoff, M17) | The same problem: SC26 falls to −−− after it. |
| **SC26–27**, ledge and crossing (recommended) | The **climax**: the action that turns the core value for good, paying off SC12's carriage (D2 CF05→CF13) | B3 (10, counterpoint), B1 (the break), A4 and D9 (the hum's drop-out, "Then not.") | B2, B4 and B5 keep their scenes and add reasons (below). No values change. |

**Why the library disagreed:** each file found a real peak. SC24 is the crisis, SC25 the hinge payoff and SC26–27 the climax; McKee's design has a place for all three.

### 8.7 Peak register (after approval)

| Component | Owner | Peak | Role | `displaced_reason` |
|---|---|---|---|---|
| core_value_turn | D16 | SC27 | climax | none |
| story_intensity 10 | B3 | SC26–27 | climax (`climax_counterpoint: true` for movement and space) | none |
| camera_break | B1 | SC26, still, then floating free at "She pushes gently away from the rail." | climax | none |
| sound_dropout | A4, D9 | SC26, "Then not." | climax | none |
| longest_hold | A4 | `to_place` in SQ08, e.g. the rise "Twelve. Six. Three." to "Nought." | climax | none |
| tightest_size | A2 | `to_place` in SQ08 | climax | none (see §12) |
| rupture_double | A4 | SC06 (10 frames of black and true silence) | inciting | `rhyme_plant` → SC27, "BLACK again. Her lit gloves." |
| saturation | B2 | SC24 (row 18, sat 5, red against green) | crisis | `crisis` (the climax is black and near-colourless in counterpoint) |
| protagonist_turn | B5 | SC24 | crisis | `crisis` |
| largest_payoff | B4 | SC25 (M17) | hinge payoff | `hinge_payoff`; keeps B4 R2 in full (the longest held frame among the film's emphasis-3 moments, plus the strongest scale contrast), because the film's longest shot overall goes to a non-motif shot in SQ08 and SC26's F insert (M06, L3) is held shorter than SC25's frame |
| sound_emphasis_3 (pump) | B4, D9 | SC30 | resolution | `coda` |

The climax owns six component peaks, so R16 is met.

**Re-keying jobs:**
- B2: add `sequence_id` and `segment_id` to rows 1–23 (values unchanged); in §4.4 and §8.5 call row 18 the crisis peak, not "the climax" or "the film's visual climax".
- B3: re-key its plan by SQ and segment, and set SC25 to 8.
- A4: place the film's longest shot in SQ08, longer than sc06's 5.0 s passage hold and sc13's freeze; in §6.8, read "unless it is the film's biggest moment" as "unless it is the film's biggest moment, or a plant whose rhyme falls in the climax".
- B4: no change; R2 stands (see the `largest_payoff` row).
- B5: no change; its turning scene is the crisis, which check 6 allows.
- D2: label CF11's role `crisis` (its table says "The climax choice").
- D13: size checkpoint C reviews from this file's sequences (nine for *The Catch*, about 3 scenes each), not its default "about 6 scenes".
- C5: rename `sequence` to `sequence_id`.

---

## 9. Worked example: *The Long Places* (book level; links D2)

**Core value:** Kept / Lost (Emre, in Nilay's life). This matches D2's episode 6 arc, "brother lost (−−−) → brother kept (+, with loss)". The alternative, Knowing / Not knowing, fails R3(c): the book refuses the explanation ("Would you want it explained, if explaining it ended it?", ch13 l.1272).

**Book sequences** (`BSQ1`–`BSQ6`) are D2's six episodes. Chapters are their segments.

| Ch. | Words % | Book seq. | Act | Role | Charge | Evidence |
|---|---|---|---|---|---|---|
| I | 0–6 | BSQ1 | 1 | plant | −− | "*Brother — missing, earthquake, September 1999 — province.*" (l.69) |
| II | 6–12 | BSQ1 | 1 | **inciting incident** | −−− | "*the undersigned file is reopened for administrative review.*" (l.118); the ribbon: "there was nothing. Wind, or anyone." (l.148) |
| III | 12–19 | BSQ2 | 1 | — | −− | "*Mass absent. Extent unknown. Cause unknown.*" |
| IV | 19–26 | BSQ2 | 1 | **act climax** | − | "*Below the fourth door, count nothing.*" (l.348); "the ninth niche filled." (l.380) |
| V | 26–33 | BSQ3 | 2 | — | − | Havva: "I spoke with my mother." |
| VI | 33–39 | BSQ3 | 2 | seq. climax | −− | "By Sunday it was past four million and had stopped being his." |
| VII | 39–48 | BSQ4 | 2 | **midpoint** | +/− | "Is the fire mountain awake?" (l.607, 45%) |
| VIII | 48–56 | BSQ4 | 2 | seq. climax | − | "*item six: not located*" |
| IX | 56–63 | BSQ5 | 2 | — | − | "Twice is a result." |
| X | 63–70 | BSQ5 | 2 | major setback | −−− | "The professor is at the fourth door. His lamp is out. He does not answer me." (l.886) |
| XI | 70–77 | BSQ5 | 2 | **act climax** | + | "*and the lamps are kept.*" (l.1027); first round (l.1043) |
| XII | 77–84 | BSQ6 | 3 | subplot (Yusuf) | + | "*Viewed: no.*" (l.1116) |
| XIII | 84–91 | BSQ6 | 3 | **crisis** | − | "Would you want it explained, if explaining it ended it?" (l.1272) |
| XIV | 91–100 | BSQ6 | 3 | **climax**; resolution | ++ (with loss) | "It was me." / "I know it now." (l.1331–1333, 93.8%); "*The print is mine.*" (l.1397); "The lamps were kept." (l.1411) |

**Inciting-incident candidates:**
- Ch. I's sibling line and item 51 are plants, with no swing.
- The March permit is reported, not dramatized.
- The breach (VII) comes too late; it is the midpoint.
- **Choice: ch. II's reopened file** (8.3% of words, l.118).

**Climax options:**
- (a) Emre: "It was me." / "I know it now.". Recommended; the core value turns for good.
- (b) "*The print is mine.*": a hinge reveal after the climax, logged as `coda`.
- (c) Melek's death and the oil can (XI): the act 2 climax.

No position flags at book level.

**Projection onto D2's plans** (R23):
- **Plan A (feature, 48 scenes):** nine film sequences (I | II | III–IV | V–VI | VII | VIII–IX | X–XI | XII–XIII | XIV).
  - The first act climax lands at 33% (scenes 1–16 of 48, at about 125 s each), against 26% in the book. That is inside R20's 20–35% window and close to TRIPOD's measured mean of 31.9%, so no flag fires; record it as a drift for D2 in `notes`.
  - If the user wants the book's proportion, compress I–II from ten scenes to eight (act break at about 29–30%); otherwise accept.
  - Each of the nine sequences runs about 8–15 minutes (4–7 scenes), inside Gulino's range.
- **Plan B (series):** there are two levels (R24). The season climax falls in E6, and each episode's `ending_turn` is its climax.
- **Plan C (short, 15 minutes, `one_act`):**
  - Sequences: SQ01 = steps 01–04, SQ02 = 05–08 (the climax is step 08), SQ03 = 09–11. Three sequences meet R12's 3–6 for a film under 25 minutes.
  - The book's inciting incident is cut; the first present-day turn is step 05's letter at 31–42% of runtime, so the check flags "inciting incident after 30%".
  - The climax, step 08, spans 57–81% of runtime (500–710 s of 875 s of story), so it meets R20. Its decisive beat, "It was me.", falls about two-fifths into the step, near 67% [J], much earlier than the book's 93.8%; the resolution (steps 09–11, 165 s) is 19%, just inside the 20% limit. Show both at checkpoint M as notes, not flags.
  - Recommended: `move_plant` the reopened-file line (l.118) into step 02 as one insert of 5–10 seconds. It is a source line, not an invention, and it lands the inciting incident at about 12%.

---

## 10. Checklists

**Structure (at checkpoint M):**
1. The core value has two poles, sits in the protagonist's life, and was chosen by R3's three conditions.
2. The dramatic question is written, quoted if the source states it.
3. Every role has a scene ID, an exact quote, a line reference, and charges before and after.
4. The crisis and the climax are named separately, or declared to be the same scene.
5. The inciting incident passes all four R7 tests.
6. The act climaxes escalate, and author-marked breaks were tested first.
7. There are 6–10 sequences (3–6 under 25 minutes); each answers a question with a quote and none crosses an act.
8. Segments nest inside sequences, and B2's rows map one to one.
9. The position check has been run by a script, on both measures, with flags explained, not "fixed".
10. Three runs were compared, and any disagreement is shown as options.
11. The subplots are recorded.

**Peak register:**
1. There is one row per component, and each has an owner.
2. Every row is in the climax or carries a valid reason.
3. The climax owns at least three peaks (R16).
4. B3 has exactly one 10 and at most two 9s.
5. The turning scene in the protagonist's B5 ARC line is the crisis or the climax.
6. No component's "once" device (true silence, a motif's emphasis-3 moment, a sound motif's S3) is spent twice.
7. Every `rhyme_plant` names its rhyme beat inside the climax, and every `coda` sits in the resolution.
8. Each component file's own wording agrees with the register (no file still calls the crisis "the climax").

---

## 11. Failure modes

- **The loudest scene is called the climax.** The fire in *The Catch* is the spectacle; the value turns later. Run R5.
- **The crisis is called the climax.** This is the SC24 reading. Test for a bigger reversal after it.
- **A theme payoff is called the climax.** This is the SC25 reading. Chart the core value, not the theme.
- **Each file sets its own peak.** This is the problem this file exists to fix. Validator check 7 catches it.
- **Beats are forced to a template.** The LLM invents an "all is lost" to fill a slot. R20 allows flags only.
- **Sequences are the wrong size.** Sequence = location (23 rows) is too fine; sequence = act is too coarse. Use R12 and segments.
- **A sequence crosses an act break.**
- **An inciting incident is taken from backstory,** such as the wrist photograph or the March permit.
- **Charges are scored by what the character knows.** SC06 and SC10 are the example; use R4.
- **The structure is not re-run after D2 merges scenes.** SC17 merged into SC18 must carry the midpoint.
- **One LLM pass is trusted.** Agreement with humans is low; use R18.
- **A continuous climax is split, or a climax is spread across non-continuous scenes.** Validator check 1.
- **The ending is scored too positive.** Tian et al. found LLM-written stories "homogeneously positive" [V]; whether that bias carries into analysis is untested [J]. Check the last scenes' charges against a quoted line (*The Catch* ends "+ (uneasy)": "The pump goes on.").
- **An LLM does the percentages.** Positions and shares come from a script (C5 R23); an LLM total is ignored.
- **A file keeps calling the crisis "the climax".** B2 and D2 do this for SC24. Fix the wording, not the values (§8.7 re-keying jobs).

---

## 12. Conflicts and open questions

1. **For the user:**
   - the core value (Home / Stranded recommended);
   - the inciting incident (SC06 recommended; the brief offered SC01 or SC03);
   - the climax (SC26–27 recommended).
2. **A2 R31 against A2's own SC13 B15**, whose push-in "ends on a big close-up, the tightest size in the scene". If no shot in SQ08 goes tighter (an extreme close-up), the film's tightest size is spent before the climax. Options: (a) SC13 stops at a close-up (recommended); (b) keep the big close-up and place an extreme close-up in SQ08 (for example on the gloves and vessel in "BLACK again. Her lit gloves."); (c) register SC13 with a reason, although none of the allowed reasons fits.
3. **B4 R2 against A4 P10 and A2 R31.** B4 gives its largest payoff "the longest held frame" of "all the film's emphasis-3 moments"; A4 and A2 keep the film's longest hold for the climax. Resolved here without changing B4: the film's longest shot overall is a non-motif shot in SQ08 (the rise to "Nought."), and SC25's chest opening is the longest of the emphasis-3 frames, so SC26's F insert (M06, L3) must be held shorter than it. (The first draft cited this rule by its digest number, "rule 9", and took the longest hold away from SC25, which B4 R2 does not require: its hold is measured only against other emphasis-3 moments.)
4. **B3's SC25 score of 9** becomes 8, to keep two 9s (SC06, SC24). B3 must confirm.
5. **A3's example "1–7 rescue"** (A3 §1: "in *The Catch*, scenes 1 to 7 are one rescue") differs from SQ01 (SC01–06). Travel direction ("keep 'up the shaft' as frame-top in every setup of scenes 1 to 7") stays a scene-range rule.
6. **A4 §6.8** says two rupture devices at once only at "the film's biggest moment" and uses them at sc06. Under this file sc06 is the inciting incident, registered as a `rhyme_plant` for SC27; A4's wording needs the added case (§8.7).
7. **B2 §4.4 and §8.5** call the fire (row 18, SC24) "the climax" and "the film's visual climax"; B2 R9 then asks earlier sequences to stay below "the climax". Under this file that is the crisis peak; B2's values stand and its wording changes. B2 must also name which component (if any) marks SC26–27; this file registers the climax as counterpoint for colour.
8. **D2 CF11** is labelled "The climax choice"; relabel `crisis`.
9. **D13** sizes checkpoint C at "sequence of about 6 scenes"; *The Catch*'s sequences average about 3 scenes. D13 should read the count from `story_structure`.
10. **Evidence still weak or untested:**
    - McKee's on-screen requirement is seen only in a reader's notes on *Story* and in Wikipedia [V-sec];
    - Thompson's roughly equal part lengths are from secondary accounts (the Harvard University Press page did not load) [V-sec];
    - the sequence counts for works under two hours, and the 25-minute line in R12 [J];
    - R20's windows are this file's, checked against TRIPOD's synopsis-level positions [J];
    - the LLM accuracy figures come from 2024-era models; current models are untested on this task [J].
11. **Plan A's 33% first act** (§9) is inside the window; whether to restore the book's 26% is a D2 decision.

---

## Sources

1. McKee, "A story is a design in 5 parts: The Inciting Incident, Progressive Complications, Crisis, Climax + Resolution", X post by @McKeeStory, text seen in search results (the page itself does not load without login): https://twitter.com/McKeeStory/status/916738399108726785 — checked 2026-09-27 [V-sec]
2. McKee Seminars, "The Rise of One-Act Films" (quotes on one-act films and "three-, four-, five- or more act films"): https://mckeestory.com/the-rise-of-one-act-films/ — checked 2026-09-27 [V]
3. McKee Seminars, *Story* book page (title only; McKee, *Story: Substance, Structure, Style and the Principles of Screenwriting*, ReganBooks, 1997): https://mckeestory.com/books/story/ — checked 2026-09-27 [V]
4. Crisis as "decision or dilemma" and climax as the resulting action (secondary summary of *Story*): https://www.skyword.com/contentstandard/crisis-climax-and-resolution-story-elements-for-a-meaningful-ending/ — checked 2026-09-27 [V-sec]
5. Reader's notes on *Story* ("The inciting incident of the central plot must happen on screen"): http://harimohanparuvu.blogspot.com/2016/12/story-robert-mckee_22.html — checked 2026-09-27 [V-sec]; Mordego Films summary (inciting incident "radically upsets the balance of forces in the protagonist's life"): https://www.mordego.com/screenplay/the-inciting-incident-by-mckee/ — checked 2026-09-27 [V-sec]
6. Paul Joseph Gulino, *Screenwriting: The Sequence Approach* (Continuum, 2004), full text on the Internet Archive (eight- to fifteen-minute sequences; "shorter films built inside the larger film"; two, four and two per act; *The Graduate* seven; *North by Northwest* nine, nine to eighteen minutes; "main tension"): https://archive.org/stream/screenwritingthesequenceapproachpauljosephgulino/ — checked 2026-09-27 [V]
7. The Story Department, "The Sequence Approach" (review; says "usually 10 to 15 minutes"): https://www.thestorydepartment.com/the-sequence-approach/ — checked 2026-09-27 [V-sec]
8. Wikipedia, "Sequence (filmmaking)" (Frank Daniel; Gulino 2004): https://en.wikipedia.org/wiki/Sequence_(filmmaking) — checked 2026-09-27 [V]
9. Film Courage, Gulino interview: https://filmcourage.com/2019/04/09/8-sequence-approach-to-writing-a-screenplay-by-chapman-professor-paul-joseph-gulino/ — checked 2026-09-27 [V]
10. Save the Cat!, "Beat Sheets": https://savethecat.com/beat-sheets — checked 2026-09-27 [V]
11. Reedsy, "Save the Cat Beat Sheet" (beat percentages): https://reedsy.com/blog/guide/story-structure/save-the-cat-beat-sheet/ — checked 2026-09-27 [V-sec]
12. Papalampidi, Keller, Lapata (2019), "Movie Plot Analysis via Turning Point Identification", EMNLP-IJCNLP, pp. 1707–1717 (Table 1 definitions; Table 3 positions; agreement 64.00%, 35.48%, 56.67%, 1.48%): https://aclanthology.org/D19-1180.pdf ; https://arxiv.org/abs/1908.10328 — checked 2026-09-27 [V]
13. Tian, Huang, Liu, Jiang, Spangher, Chen, May, Peng (2024), "Are Large Language Models Capable of Generating Human-Level Narratives?", EMNLP 2024: https://arxiv.org/abs/2407.13248 ; https://arxiv.org/html/2407.13248v1 — checked 2026-09-27 [V]
14. Thompson (1999), *Storytelling in the New Hollywood* (Harvard University Press), via secondary pages: https://www.ibiblio.org/cdeemer/wright/4act.html (four parts; "A short epilogue usually follows the climax") [V-sec]; https://www.screenplayology.com/content-sections/screenplay-form-content/3-2/ [V-sec]; https://intermittentmechanism.blog/2019/12/04/when-splitting-up-a-narrative-gets-dicey/ ("four acts of equal length") [V-sec] — all checked 2026-09-27; Harvard University Press page https://www.hup.harvard.edu/books/9780674839755 (content not loadable) [U]
15. Wikipedia, "Three-act structure" (Field 1979; "A dynamic, on-screen incident occurs, known as the inciting incident, or catalyst"): https://en.wikipedia.org/wiki/Three-act_structure — checked 2026-09-27 [V]
16. Library files A2, A3, A4, B1–B5, C5, D2, D9, D13, D14 (scratchpad/research/), re-read 2026-09-27 for every cross-reference.
17. Test sources: *The Catch* (L-numbers are file lines); *The Long Places* (l. = file lines; D14 paragraph IDs replace them after intake). Every quote in this file was re-found verbatim in its source on 2026-09-27.
