# Digest D16: Film-level story structure (acts, sequences, climax, peak register)

Source: `research/D16_film_level_structure.md` (fact-checked 27 Sept 2026). Brackets: R*n* = D16 decision rule (§4); P*n* = principle (§2); V*n* = validator check (§7); § = section. Other files' numbers are their main files' own (B4 R2 = B4 digest rule 9; B3 R9 = B3 digest rule 6). Evidence: **[V]** read at the source, **[V-sec]** secondary only, **[J]** judgment or arithmetic on the test sources.

## 1. Scope

1. Fixes the film's shape once, in `story_structure`: core value, dramatic question, inciting incident, act climaxes, midpoint, crisis, the one climax, resolution, secondary peaks, per-scene charge, and one sequence/segment list that B2, B3, A4, D13 and checkpoint C key to.
2. Adds a **peak register**: each craft component names where it peaks; a peak outside the climax carries one allowed reason.
3. Drafted at C5 stage 1, re-checked on D2's step outline, approved on one page at D2's checkpoint M, then locked; no other file re-derives it. Worked on *The Catch* (30 scenes) and *The Long Places* (14 chapters, D2 Plans A–C).

**Terms** [§1]. *Core value*: the value in the protagonist's life the story turns on (+/− poles). *Charge*: −−− to +++, or +/−. *Major reversal*: a swing of ≥2 steps or a sign change. *Dramatic question*: raised by the inciting incident, answered by the climax (Gulino's "main tension" [V]). *Sequence*: consecutive scenes answering one short-term question (`SQ01`); *segment*: a run inside it sharing place, time or light (`SQ01c`). *Crisis*: the hardest choice. *Climax*: the scene or unbroken CONTINUOUS run where the core value turns for good; exactly one; its *decisive beat* is where the turn lands. *Hinge payoff*: reveal of the hinge motif closest to the climax (B4 R2). *Displaced peak*: a component peak outside the climax. *Counterpoint*: visual calm under a story peak (B3 §2.5). *Word %*: share of source words before a quoted line. *Cardinal function*: an event the plot cannot lose (D2).

## 2. Rules

**Shape and value**
1. [R1] If any stage needs a film-wide high point, then it reads `story_structure`, because four files that derived their own named three different climax scenes for *The Catch* (SC24, SC25, SC26–27).
2. [R2] If the work runs under about 30 minutes with no major reversal before the end, then `structure_shape: one_act`; a series → `series_arc`; loosely linked episodes → `episodic` (still one climax); otherwise `multi_act`, because McKee: one movement "usually asks its audience for less than 30 minutes" [V].
3. [R3] If choosing the core value, then chart 2–3 candidates across all scenes and pick the one whose last big turn (a) is the last major reversal, (b) is caused by the protagonist, (c) answers the dramatic question; if none meets all three, take (a)+(c), set `turn_kind: revelation | external` and ask at checkpoint M, because a theme-chosen value points at a payoff instead of the ending.
4. [R4] If a character knows less than the audience, then score the film-level charge by what truly happened and note the character's view in `audience_knows`, because roles must not move when a character learns late.

**Roles**
5. [R5, P3] If one scene holds the hardest choice and a later one the action that turns the value for good, then label them `crisis` and `climax`, because McKee separates decision from result [V-sec].
6. [R6] If the decisive turn spans CONTINUOUS scenes, then the climax may be that run with one `decisive_beat`, because B3 §2.6 allows one scene "or one continuous sequence" at 10.
7. [R7] If choosing the inciting incident, then keep candidates passing all four tests (on screen, not backstory; swings the value ≥2 steps or first raises the question; the climax answers it; deleting it removes the climax's cause) and pick the earliest, because McKee's central-plot inciting incident "must happen on screen" [V-sec].
8. [R8] If the source marks its own break (title card, part heading, END OF ACT, intermission, cut to black plus card), then test it first as an act boundary, because the author outranks inference; D14 R34 records these as `break_kind`, D16 decides.
9. [R9] If placing act climaxes, then choose major reversals of the core value that change the plan, with escalating stakes and non-falling B3 scores, because McKee's films "progress … to an all-or-nothing climax" [V].
10. [R10] If a turn falls mid-scene, then the boundary is the next scene boundary, because the scene is the record unit (C5).
11. [R11] If there are subplots, then record each in `subplots[]` with its own value and turns, ranked below the climax, because a subplot climax is not the climax.

**Sequences**
12. [R12] If grouping sequences, then each is consecutive scenes, answers one question with a quoted line, ends inside its act, and the count is 6–10 (film or episode of 25 min or more) or 3–6 (under 25 min), warning only, because Gulino's sequences are "shorter films built inside the larger film", seven to nine in his own analyses [V]; the short-film counts are [J].
13. [R13] If a component needs finer steps, then use segments (`SQ03b`), never its own numbering, because B2's 23 rows and B3's 9 stretches could not be joined.
14. [R14] If a component's grouping straddles a sequence boundary, then re-key it by segment and keep its values, because only the IDs conflicted.

**Peaks**
15. [R15] If a component peak is not in the climax, then give a `displaced_reason` (§3) and meet its constraint, or move the peak, or ask the user, because A2 R31 ("Do not spend the film's tightest size or longest hold before its climax") and B3 §2.6 ("one highest peak").
16. [R16] If the climax is in counterpoint, then it still owns `core_value_turn`, `story_intensity` 10, and at least one of `longest_hold`, `camera_break`, `tightest_size`, because a calm climax needs other layers to mark it.
17. [R17] If scoring secondary peaks, then keep each at least one step below the climax on every component the register places in the climax, except the one component it holds as a displaced peak, because intensity needs room (B2 R9); components without a register row are not checked.

**Running it with an LLM**
18. [R18] If an LLM proposes the structure, then make three independent runs; if every role (inciting, each act climax, crisis, climax) is within one scene across runs and the core value matches, accept the majority, else show options at checkpoint M, because human annotators share only about a third of their scene picks [V].
19. [R19] If finding turns, then work on the one-line event list first and map to scenes second, because TRIPOD agreement was 64% on synopsis sentences against 35% scene overlap [V].
20. [R20] If a role falls outside its window on both measures (runtime % over its scene span; word % at its quote), then flag it, never move it, because templates force slots and LLMs place climaxes early [V]. Windows [J, checked against TRIPOD Table 3]: inciting after 30%; first act climax outside 20–35% (35–43% soft); climax before 70%; resolution over 20%.

**Change and scope**
21. [R21] If D2 cuts or merges scenes, then recompute every role on the step outline, because each role scene must stay a D2 cardinal function (D2 P3).
22. [R22] If the user changes the climax, then rebuild the register and list every newly unexplained peak, because each peak's reason depended on the old climax.
23. [R23, R24] If the source is prose or a series, then build the whole-work (book, season) structure first and project it onto the step outline or episodes (`E6-SQ03`), because the film's climax must be traced to the source's.
24. [R25; C5 R23] Always compute in screen order, and let a script do every percentage, because the audience meets peaks in screen order and LLM arithmetic is not trusted.

## 3. Breakdown fields

Enums lowercase `snake_case`; empty = `"none"` or `[]`. Authority per C5: `extracted`, `authored`, `derived`.

| level | field_name | meaning | allowed values / example |
|---|---|---|---|
| film | `structure_shape` | Overall shape (R2) | `multi_act` \| `one_act` \| `episodic` \| `series_arc` |
| film | `core_value` | `{positive, negative, whose, alternatives[]}` | `{"Home","Stranded","Iona and those she carries"}` |
| film | `dramatic_question` | The question, quoted if stated | "Eli. Are we going to be all right?" (SC09, L390) |
| film | `inciting_incident` | `{scene, beat, quote, source_ref, candidates[]}` | `SC06`, "A hard metal CLACK." |
| film | `acts[]` | `{act_id, scenes, sequences[], act_climax_scene, quote, charge_close}` | `ACT1`, SC01–SC10 |
| film | `midpoint`, `crisis`, `climax` | `{scene(s), decisive_beat, quote, source_ref, charge_before, charge_after, turn_kind}` | climax `["SC26","SC27"]`; `action` \| `revelation` \| `external` |
| film | `resolution` | Scenes after the climax | SC28–SC30 |
| film | `secondary_peaks[]` | `{scene, role, rank}`; rank 1 highest by B3 score, ties to later | `inciting_incident` \| `act_climax` \| `midpoint` \| `crisis` \| `hinge_payoff` |
| film | `sequences[]` | `{sequence_id, title, scenes, act_id, question, answer_quote, share_pct}` | `SQ04`, "Taken" |
| film | `segments[]` | `{segment_id, sequence_id, scenes, place_time}` | `SQ04b`, SC17 |
| film | `subplots[]` | `{value, whose, turns[], resolves_at}` | Trust / Betrayal (Iona toward Eli) |
| film | `charge_by_scene` | Core value's charge after each scene | `{"SC27": "++"}` |
| film | `position_check` | Percentages (derived) and flags | `{climax_pct: "83-89 / 85.6-88.4", flags: []}` |
| film | `peak_register[]` | `{component, owner_file, peak_scene, peak_role, displaced_reason, rhyme_target, climax_counterpoint, status}` | status `placed` \| `to_place` \| `conflict` |
| film | `structure_runs[]` | Each run's roles (derived) | three entries |
| film | `structure_checkpoint` | Approval at checkpoint M | `{status: pending \| approved, version, date}` |
| film | `notes` | Reasons for overriding a default or accepting a flag | `["R12: 9 sequences accepted"]` |
| film | `open_questions[]` | One decision each | `["Climax: SC26-27 or SC24?"]` |
| scene | `sequence_id`, `segment_id`, `act_id` | Keys; replace C5's free-text `sequence` | `SQ07`, `SQ07b`, `ACT3` |
| scene | `structure_role[]` | Roles held | secondary-peak roles + `climax` \| `sequence_climax` \| `resolution` \| `none` |
| scene | `core_value_charge_after` | Film-scale charge | `−−−` … `+++`, `+/−`, qualifier allowed |
| scene | `audience_knows` (opt) | Audience ahead of character (R4) | "turn seen; Iona sees it in SC07, has it proved in SC10" |

**Register components** [§6], default peak the climax: `core_value_turn`; `story_intensity` 10 (B3); `camera_break` (B1); `longest_hold` (A4 P10); `rupture_double` (A4 §6.8); `sound_dropout` (A4, D9); `tightest_size` (A2 R31); `saturation` / `climax_component` (B2 R9); `largest_payoff` (B4 R2); `sound_emphasis_3` (B4, D9); `protagonist_turn` = B5 `turning_scene` (crisis or climax).

**`displaced_reason` values**: `crisis` (peak scene = the crisis); `hinge_payoff` (last act, before the climax, a B4 hinge reveal); `rhyme_plant` (`rhyme_target` is a climax beat repeating it with one change, B3 P8/R9); `coda` (in the resolution, within the "once" budget: one emphasis-3 moment per motif, one S3 per sound motif, B4 P5); `none`. `climax_counterpoint: true` marks a component deliberately calm at the climax; its peak must use a reason.

## 4. Procedures

**Recipe** [§5]. Inputs: locked scene list (C5 stage 0), one-line event list and cardinal functions (C5 stage 1, D2 M2), per-scene runtime (D2 §6 or D13 v0).
1. Event list: one past-tense line per scene, one exact quote and line reference (reuse D2's).
2. Core value: three candidates charted scene by scene; apply R3.
3. Climax and crisis (R5, R6); say if they share a scene.
4. Inciting incident: up to three candidates from the first third; R7's four tests.
5. Acts and midpoint: author breaks first (R8), then major reversals (R9); midpoint only if the goal changes near 50%.
6. Sequences (R12), then segments where place, time or light changes (R13).
7. Fill `charge_by_scene` and each `structure_role`.
8. Position check by script: runtime % over scene spans, word % at quotes; flag under R20.
9. Peak register: one row per component, filled from component files or `to_place`.
10. Repeat steps 2–6 twice in fresh chats; compare with the comparison prompt; apply R18.
11. Fill the checkpoint M page; the user approves or changes one item at a time ("make SC24 the climax"); a climax change triggers R22; set `structure_checkpoint.status: approved`.

**The user's part** (about 15–20 minutes [J]): read the page, pick at each OPTION, search the script for each quote, say "approved".

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

**JSON template** (abridged *The Catch*; `…` marks repeated rows; parses as JSON):

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

**Validator checks** [V1–V11]: exactly one climax (one scene or one CONTINUOUS run); climax after the last act climax; inciting incident before the first act climax; every scene in one sequence and one act, no sequence crossing an act; B3 has one 10 on the climax and at most two 9s; B5 `turning_scene` is crisis or climax; every register row in the climax or with a valid reason; every role scene is a D2 cardinal function; sequence count per R12 (warning); every `rhyme_plant` targets the climax and every `coda` sits in the resolution; the climax is a major reversal and nothing reverses the core value after it.

## 5. Checklists

**At checkpoint M** [§10]
- [ ] Core value has two poles, sits in the protagonist's life, chosen by R3.
- [ ] Dramatic question written, quoted if the source states it.
- [ ] Every role has scene ID, exact quote, line reference, charges before and after.
- [ ] Crisis and climax named separately (or declared the same scene).
- [ ] Inciting incident passes all four R7 tests.
- [ ] Act climaxes escalate; author-marked breaks tested first.
- [ ] Sequence count per R12; each answers a question with a quote; none crosses an act.
- [ ] Segments nest in sequences; B2 rows map one to one.
- [ ] Position check run by script on both measures; flags explained, not "fixed".
- [ ] Three runs compared; disagreements shown as options.
- [ ] Subplots recorded.

**Peak register**
- [ ] One row per component, with an owner; each in the climax or with a valid reason.
- [ ] Climax owns at least three peaks (R16); B3 has one 10 and at most two 9s; B5 turning scene = crisis or climax.
- [ ] No "once" device (true silence, a motif's L3, a sound's S3) spent twice; `rhyme_plant` and `coda` constraints met.
- [ ] No component file still calls the crisis "the climax".

**Failure modes** [§11]: loudest scene, crisis (SC24) or theme payoff (SC25) called the climax; each file setting its own peak (V7); an invented "all is lost"; sequences = locations or = acts; inciting incident from backstory (wrist photograph, March permit); charges scored by character knowledge; no re-run after D2 merges (SC17 into SC18 carries the midpoint); one LLM pass trusted; ending scored too positive (LLM stories "homogeneously positive" [V]; carry-over to analysis untested [J]).

## 6. Saying it to AI models

- Structure work is text-only; no image or video model sees `story_structure`.
- Give only scene IDs and quotes, say "do not invent events", and demand an exact quote per role so a script can find it.
- Event list first, scenes second (R19); three values, not one (R3); three fresh runs, never "review and improve" (C5 R12, R14).
- A shot prompt never says "climax"; it gets the concrete treatment the register assigns (SC26–27: still camera, near-black, helmet light on gloves and vessel).
- Distrust an early climax: LLMs generating stories place TP4 and TP5 early ("substantial advancement") [V, Tian et al. 2024]; 2024-era models scored 26–30+% on turning-point identification against humans' 46.6% [V].

## 7. *The Catch*: decisions made, and points flagged for the user

**Recommended structure** [§8, all [J] unless marked]
- Core value: **Home / Stranded** (Iona and those she carries); only it passes R3's three tests. Keeps/Gives turns at SC24 but SC26–27 reverse again; Person/Goods (B4's theme) turns at SC25 and fails (c).
- Dramatic question: "Eli. Are we going to be all right?" (L390, SC09); Eli asks it back at SC23, "Are we going to be all right?" / "I don't know." (L1352–1355); answered in SC29, "In the car-" / "Yes." (L1788–1791; reading "Yes." as the answer is [J]).
- Inciting incident: **SC06**, "A hard metal CLACK." / "The cage is going UP." (L259, L267), 10–15% runtime, 14.6% words. SC01 ("The safety brakes are gone.", L35) is SQ01's own trigger; SC03 fails mirror and deletion; the wrist photograph is backstory.
- Roles (runtime % / word %): act 1 climax SC10, author-marked ("Nobody leave this room.", CUT TO BLACK, `= THE CATCH`, L484–488; 19–24 / 25.3); midpoint SC17 "I sent her." (L996; 48–54 / 50.9); act 2 climax SC23 "They vanish together." (L1370; 70–76 / 72.4); crisis SC24 "She deletes the way home." (L1412; 76–79 / 75.1); hinge payoff SC25 "two outlines turn green, one inside the other." (L1488; 79–83 / 80.6); **climax SC26–27**, decisive beat "Nought." / "The engine crosses." (L1591–1593; 83–89 / 85.6–88.4); resolution SC28–30 (11.2). No flags.
- Sequences (runtime %): SQ01 Rescue and fall SC01–06 (15.2); SQ02 Wrong world SC07–10 (8.5); SQ03 Told SC11–13 (19.9); SQ04 Taken SC14–17 (9.3); SQ05 Going over SC18–20 (13.8); SQ06 The collection SC21–23 (9.2); SQ07 Fire and the chest SC24–25 (7.0); SQ08 Ledge and crossing SC26–27 (6.0); SQ09 Return SC28–30 (11.2). Acts: SQ01–02 | SQ03–06 | SQ07–09. Each B2 row = one segment; B3's sc18–22 and sc23–25 stretches split at SQ05/06 and SQ06/07.
- B3 intensity re-keyed per scene inside B3's ranges; only SC25 changes (9 → 8) so the two 9s are SC06 and SC24.
- Subplot Trust / Betrayal (Iona toward Eli): cracks for the audience in SC06 (L253), falls to −− in SC13, resolves to + in SC29.
- Register: climax owns six peaks (value turn SC27; intensity 10; B1's break at "She pushes gently away from the rail."; the hum's drop-out "Then not."; longest hold and tightest size `to_place` in SQ08). Displaced: A4's cut-to-black-plus-silence at SC06 = `rhyme_plant` → SC27 "BLACK again. Her lit gloves."; B2 saturation 5 at SC24 = `crisis`; B5 turning scene SC24 = `crisis`; B4 M17 chest opening SC25 = `hinge_payoff` (keeps B4 R2's longest emphasis-3 frame); pump S3 in SC30 = `coda`.

**Flagged for the user**
1. Core value: Home / Stranded (recommended)?
2. Inciting incident: SC06 (recommended), or SC01 / SC03 as the brief offered?
3. Climax: SC26–27 (recommended), SC24 (the crisis; would break the last-reversal test and move B3's 10, B1's break and A4's hold) or SC25 (hinge payoff; SC26 still falls to −−− after it)?
4. SC13's big close-up (A2 B15): stop at a close-up (recommended), or keep it and go tighter in SQ08.
5. B3 to confirm SC25 at 8.

## 8. Conflicts and open questions

**With other library files**
- **B2** (§4.4, §8.5; digest rule 16 and field `climax_component`) calls the SC24 fire "the climax" / "the film's visual climax". Values stand; relabel as the crisis peak; B2 must say whether any colour component marks SC26–27 (D16 registers colour as counterpoint there).
- **B4 R2** (digest rule 9) gives SC25 "the longest held frame" of the emphasis-3 moments; **A4 P10** and **A2 R31** keep the film's longest hold for the climax. Resolved without changing B4: the film's longest shot is a non-motif shot in SQ08 (the rise to "Nought."), and SC26's F insert (M06, L3) is held shorter than SC25's frame.
- **A2 R31 vs A2 B15** (SC13 push-in "ends on a big close-up"): conflict unless SQ08 goes tighter (open item 4 above).
- **A4 §6.8** allows two rupture devices at once only at "the film's biggest moment" and uses them at SC06; wording needs "or a plant whose rhyme falls in the climax".
- **A3 §1** makes "scenes 1 to 7 … one rescue"; D16's SQ01 is SC01–06. A3's frame-top rule for scenes 1–7 stays a scene-range rule.
- **B3** SC25 9 → 8 and re-key by SQ/segment; **D2 CF11** "The climax choice" → `crisis`; **C5** `sequence` → `sequence_id`; B5's sc24 turning scene is allowed as the crisis.
- **D13** sizes checkpoint C at "about 6 scenes" per sequence; *The Catch* averages about 3; D13 should read the count from `story_structure`.
- **D14 R34** records author breaks as `break_kind`; D16 decides act status (resolved).

**Weak evidence**: McKee's on-screen rule and Thompson's equal parts are [V-sec]; R12's short-film counts and R20's windows are [J]; LLM accuracy figures are from 2024-era models.

**Book level, *The Long Places*** (§9): Kept / Lost (Emre, in Nilay's life); inciting ch. II's reopened file (l.118, 8.3%); act climaxes IV, XI; midpoint VII (l.607); crisis XIII (l.1272); climax XIV "It was me." / "I know it now." (l.1331–1333, 93.8%). Plan A: act 1 ends at 33% vs the book's 26% (inside the window; D2 decides). Plan C (15 min, 3 sequences): inciting flag (first present-day turn 31–42%), fixed by moving l.118 into step 02 (about 12%); climax step spans 57–81%, decisive beat near 67% [J].

## 9. Section map

| § | Contents |
|---|---|
| Header | Purpose, evidence labels, cross-reference numbering, pipeline place |
| 1–2 | Glossary; principles P1–P8 |
| 3 | McKee, Gulino sequences, beat sheet/TRIPOD compared; reliability evidence; chosen procedure |
| 4 | Rules R1–R25 |
| 5 | Recipe, structure prompt, comparison prompt, checkpoint M page |
| 6 | Peak register and `displaced_reason` constraints |
| 7 | Fields, validator V1–V11, JSON template |
| 8 | *The Catch*: 8.1 core value, 8.2 inciting incident, 8.3 roles and positions, 8.4 sequence list (B2/B3 reconciled), 8.5 scene by scene, 8.6 climax options, 8.7 register and re-keying jobs |
| 9 | *The Long Places* and D2 Plans A–C |
| 10–12 | Checklists; failure modes; conflicts and open questions |
| Sources | 17 entries |
