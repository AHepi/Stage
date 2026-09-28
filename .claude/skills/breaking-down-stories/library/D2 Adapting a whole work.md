# D2. Whole-Work Adaptation and Scope: Format, Runtime, What to Keep, and the Step Outline

*Library file D2. Written 2026-09-27. Test sources: "The Catch" (screenplay, 25 September 2026 revision) and "The Long Places" (prose, 14 chapters).*

> **What this file is for**
> 1. It runs once, before any scene is designed, and sizes the film: format (short, feature or limited series), total runtime, and the scenes and shots that allows.
> 2. It builds a whole-work event list, finds the strands and the events the story cannot lose, and decides which strands and chapters survive, with reasons.
> 3. It produces a step outline (one line per scene, citing source lines or paragraphs) that the user approves before A3's passage-level adaptation and C5's stages start.
> 4. It decides recurring devices once, as series rules, and gives episode rules for series and reduction rules for shorts.
> 5. It settles *The Catch*'s likely runtime, shows it cut to 20 minutes, and plans *The Long Places* three ways.

**Evidence labels.** [V] verified at the named source on 2026-09-27; [U] unverified; [J] this file's judgment (including arithmetic on the test sources). Every quotation from the two test sources, every line and paragraph reference, the word and scene counts and the table sums in §6–§8 were re-checked by script against the source files on 2026-09-27.

**Place in the pipeline.** A macro pass between C5's stage 1 (story analysis) and stage 2 (bible), ending in a human approval, **checkpoint M**. For prose, A3 §7 then adapts only the passages the approved step outline keeps. For a screenplay, the pass estimates runtime and, under a cap, cuts or merges scenes.

---

## 1. Words this file uses (one word per concept)

| Word | Plain meaning |
|---|---|
| **Format** | The kind of finished work: `short` (40 minutes or less with credits), `feature` (one film over 40 minutes), `limited_series` (a fixed number of episodes). |
| **Runtime target** | The finished length the user wants, in seconds, credits included (`runtime_target_s`). |
| **Natural runtime** | How long the source would run filmed as written. |
| **Scene budget, shot budget** | How many scenes and shots the runtime allows, from an average scene length and a target average shot length (A4). |
| **Event** | One thing that happens, written in one or two past-tense sentences (McKee's method, §3.4). |
| **Cardinal function** | An event the story cannot lose: remove it and later events stop making sense (Barthes' term, via McFarlane; see A3 §7.1). |
| **Catalyser** | Barthes' word for every other event: it fills in, colours or delays, but removing it leaves the chain of cause and effect intact. Catalysers are what a cut removes first. |
| **Set piece** | A large, costly sequence built around one spectacle (the cage fall in SC06; the chamber in chapter VII). |
| **Strand** | A line of events that follows one character or one question through the work (for example "Márton's clocks"). |
| **Deletion test** | Asking of an event or strand: "If this were gone, which later events would lose their cause, setup or meaning?" |
| **Step outline** | A list with one line per planned scene, in screen order. Wikipedia: it "briefly details every scene of the screenplay's story" [V, S13]. |
| **Macro plan** | This file's decisions (format, runtime, strands, series rules, step outline), saved as `adaptation_plan.json`. |
| **Series rule** | A decision about a recurring device, made once for the whole work (A3's `series_rule`, widened to any device). |
| **Composite** | Two scenes, or two characters, merged into one (A3 §7.5). |
| **Fold** | Moving a passage's useful content into a neighbouring scene as a shot, line or prop (A3 §7.9, rule 3). |
| **Value arc** | The value an episode or film turns on, with its opening and closing charge (A2's terms, scaled up). |
| **Charge** | Whether a value is positive (+) or negative (−) for the character at a moment; `−−` or `−−−` means worse still. "Grief contained (+) → reopened (−−)" is a value arc. |
| **Bookend** | A structure that opens and closes on matching material (the same letter, place or image), with the middle cut short or skipped. |
| **Cold open** | The part of an episode that plays before its title. |
| **Recap** | The "previously on" montage at an episode's head, built from shots already made. |
| **Generation factor** | Seconds a video model must generate for each finished second: C1 §10's overshoot (clips longer than the part used) × retake ratio (takes made per take kept). C1's typical case is 2 × 4 = 8. |
| **Validator** | A small script (or, without one, a spreadsheet) that adds up seconds, counts scenes and checks that every ID and cardinal function is present. It does the arithmetic the LLM must not be trusted with. |
| **Enum** | A field whose value must be one word from a fixed list, such as `short`, `feature` or `limited_series`. |
| **JSON** | A plain-text file format of labelled fields in braces; `adaptation_plan.json` (§9) is the saved macro plan. |
| **Checkpoint M** | The user's approval of the macro plan; nothing downstream starts before it. |

---

## 2. Core principles

- **P1. Size before detail.** Format and runtime fix every later budget: scenes, shots, money and review hours (C1 §10). Decide them first.
- **P2. Estimate as a range.** Pages, words and beats each mislead differently. Use two or more methods; report low, central and high.
- **P3. The cardinal functions are the contract.** Every one appears in the step outline. Everything else may be trimmed, merged, folded or cut, and each change is logged.
- **P4. Cut from the outside in.** Trim, then merge, then fold, then delete a strand, and drop a set piece last (R10).
- **P5. A cut leaves orphans.** The deletion test finds payoffs that lost their setup; the log records where each moved.
- **P6. Decide recurring devices once**, as series rules; decided scene by scene they drift.
- **P7. Offer options.** Two or three independent macro plans beat one plan argued at length (C5 R14).
- **P8. Scripts count.** A script sums seconds and checks cardinal functions and IDs (C5 R23, R25). The LLM proposes; the validator checks; the user approves.

---

## 3. What the evidence says

### 3.1 How long sources become films

| Source | Kind | Screen result | What the adapters did |
|---|---|---|---|
| "Story of Your Life" (Ted Chiang, 1998) | Novella; 1999 Nebula for Best Novella [V, S7]; Nebula novellas are "at least 17,500 words but fewer than 40,000 words" [V, S5] | *Arrival* (2016), 116 min [V, S6] | Added an event: the aliens arrive on Earth, "as he felt this helped to create the tension and conflict needed for a film" (Heisserer, as reported) [V, S6] |
| "Brokeback Mountain" (Annie Proulx) | Short story, *The New Yorker*, 13 Oct 1997 [V, S8]; about 10,000 words (one online text counts 10,650; counts vary by edition) [U, S19] | Film (2005), 134 min; screenplay Larry McMurtry and Diana Ossana [V, S8] | Expansion [J]; Proulx: "I may be the first writer in America to have a piece of writing make its way to the screen whole and entire" [V, S8] |
| *The Remains of the Day* (Ishiguro, 1989) | Novel | Film (1993), 134 min [V, S9] | Congressman Jack Lewis "is a composite of two separate American characters" in the novel, Senator Lewis and Mr Farraday [V, S9] |
| *Normal People* (Rooney, 2018) | Novel | 12 episodes, 23–34 min each (BBC Three, RTÉ One and Hulu, 2020) [V, S10] | The novel's "timeline ... jumps around"; the series was told "in chronological order". Director Lenny Abrahamson: "we initially felt that we were going to follow Sally in that shifting timeline, but in the end the adaptation was more direct" [V, S15]. This is McKee's step 4 (reorder in story time) applied to a series. |
| "An Occurrence at Owl Creek Bridge" (Bierce, 1890) | Short story | *La Rivière du hibou* (1961), 28 min; Best Short Subject, Cannes 1962; Academy Award for Live Action Short, 1963 [V, S11] | Kept short; "The soundtrack contains only bird noises and brief military orders" [V, S11] |

The pattern [J]: short stories and novellas grow (summaries become scenes; events are added); novels shrink (strands deleted, characters combined, as with *Jaws* in A3 §7.5); long novels with many turns suit a series. Runtime follows the number of cardinal functions and strands, not the word count.

### 3.2 Pages, scenes and minutes

- **Page per minute is an average, not a rule.** Stephen Follows matched about 2,870 feature scripts (2,520 on US Letter paper, 351 on A4) to their released films: "One page does not equal one minute - it equals about 55 seconds." The median ratio of pages to minutes is 1.1, with the released runtime counted including its end credits (median end crawl 4.3 minutes); only 18.2% of scripts fall within 0.95–1.05; comedy runs about 1.15, war films about 0.99, musicals about 0.9 [V, S1]. This is the data behind A2 S5.6's and A3 §5.2's warning. Because a feature's credit crawl is inside the 1.1, a short (with a minute or less of credits) plays slightly less story per page than pages ÷ 1.1 suggests [J].
- **Scenes per feature.** McKee: "For a typical film, the writer will choose forty to sixty Story Events or, as they're commonly known, scenes. A novelist may want more than sixty, a playwright rarely as many as forty." And: "A typical two-hour feature plays forty to sixty scenes. This means, on average, a scene lasts two and a half minutes. But not every scene. Rather, for every one-minute scene there's a four-minute scene" [V, S3]. The average sizes a budget; it is not a length for every scene. Follows' survey of 12,309 mostly unproduced scripts found "110 scenes – just over one scene per page" [V, S2]; spec scripts cut scenes finer than finished dramas [J].
- **Beats and seconds.** A2 S5.6 (about 14 s a beat) and A2 Step 9's per-line defaults; §6 uses both.

### 3.3 Formats and their fixed lengths

- **Short.** The Academy: "an original motion picture that has a running time of 40 minutes or less, including all credits" [V, S4 (97th), S17 (98th); the 99th rules, announced 1 May 2026, keep the short-film categories, S18]. The same rule excludes "Works originally created as episodic television (for broadcast and/or streaming)", so an episode cut from a series plan is not a short [V, S17].
- **Category fit for an AI film [J, flag to the user].** The Academy's live-action definition is "imagery and sound created primarily through practical photographic techniques used to capture physical actors, props, sets, and locations"; its animation definition is movement created "by any human means" [V, S17]. A film whose pictures come from a video model may fit neither cleanly. The 99th rules add that the Academy "reserves the right to request more information about the nature of the use and human authorship" of generative AI, that "screenplays must be human-authored", and that acting awards need roles "demonstrably performed by humans with their consent" [V, S18]. D4 §3.5 and its rule 22 cover festival and award AI clauses.
- **Festivals set their own limits.** Sundance 2027: a short is "less than 50 minutes, including credits"; 50 minutes or more is a feature; multi-episode work has its own categories (60 minutes or less, over 60) [V, S16]. Check each call for entries.
- **Television.** A network "hour" is about 44 minutes without commercials, about 44–45 script pages; a streaming hour runs "in the neighborhood of 55-65 pages" [V, S12]. Streaming lengths vary: *Normal People* ran 23–34 minutes [V, S10].
- **Feature.** Over 40 minutes by the Academy's line (over 50 at Sundance). For AI production, 100 minutes is already very large (§8.3).

### 3.4 How adapters choose what survives

McKee's method (*Story*, 1997, "The Problem of Adaptation", pp. 364–370) [V, S3], in his words where it matters:

1. "read the work over and over without taking notes".
2. "reduce each event to a one- or two-sentence statement of what happens and no more. No psychology, no sociology."
3. Ask "Is this story well told?"; a novel may be "four hundred pages long, three times as much material as you can use for a film".
4. "reorder them in time from first to last... From these create a step-outline... feeling free to cut scenes and, if necessary, to create new ones."
5. "turn what is mental into the physical" (A3 §7.2's ladder does this per passage).

He warns: "The purer the novel, the purer the play, the worse the film." *The Long Places* is largely inner and quiet: expect heavy externalization (A3 §7.2).

Barthes' cardinal functions are the hinge events a story cannot lose; Otake and others (COLING 2020) measure event salience on this idea [V: abstract, S14]. §1's deletion test is a plain version [J].

---

## 4. Decision rules

A plain "then" is firm; "then consider" is a default, broken only with a one-line reason in the plan's `notes` (A2, A3 convention).

**Format and runtime**

- **R1.** If the user names no format, then offer two or three independent macro plans, each with runtime, scene and shot budgets, cost and review hours, because format fixes every later budget and choosing is the user's call (C5 R14).
- **R2.** If the source is a screenplay, then estimate runtime three ways: pages ÷ 1.1 (Follows); A2's line and action defaults summed over three sample scenes and extrapolated by word counts; beats × 14 s. Report low, central and high, because page ≈ minute misses by more than 5% four times in five [V, S1].
- **R3.** If the source is prose, then natural runtime = candidate scenes (run A3 §7.9 on two sample chapters, average, multiply by chapter count) × average scene length (2–2.5 min for drama, McKee), because words per minute vary too much with style.
- **R4.** If the user wants festival or award eligibility as a short, then keep the total with credits at 38 minutes (2,280 s) or less (a 5% margin under the Academy's 40), read the target festival's own limit (Sundance: under 50) and its AI rules, and flag at checkpoint M that an AI-generated film may not fit the Academy's live-action or animation definitions (§3.3), because the rules count credits, differ by festival, and define categories by how the pictures were made.
- **R5.** If natural runtime exceeds the target by more than about half (ratio above 1.5), then expect to delete a strand or change format, because trims and merges alone recovered about a third of *The Catch* (35 → 24 minutes, §7) [J].
- **R6.** If natural runtime is under about two-thirds of the target, then expand first by dramatizing the source's own summaries (A3 §7.4) and label any invented event `invention`, because expansion is invention (A3 P2 keeps facts apart from choices; A3 rule 24 labels every invention; *Arrival* added the landing).
- **R24.** If M4 must propose format options, then choose them from the natural runtime [J]: up to about 45 minutes, offer the film as written, a trimmed cut under the user's cap, and (only if asked) an expansion; about 45–150 minutes, offer a feature and a short built by R19; over about 150 minutes or more than about eight strands, offer a series (episodes ≈ natural runtime ÷ episode length), a feature that deletes strands, and a short; because the options should span the realistic range and at least one must fit the user's money and hours (C1 §10; D13 R17). (Numbered after R23 so that other files' references to R1–R23 stay valid.)

**Budgets**

- **R7.** If the runtime target is set, then scene budget = runtime ÷ average scene length and shot budget = runtime ÷ target ASL (average shot length, A4), because cost and review time scale with shots (C1) and asset work with scenes and sets (C2).
- **R8.** If candidate scenes exceed the scene budget, then rank them by A3's five tests and remove from the bottom, never a passage that passes test 1 (cardinal function), because the cardinal functions are the story.
- **R9.** If the step outline's `target_duration` values miss the runtime target by more than ±10% (credits and cards included), then revise before checkpoint M, because C5's validator uses the same default tolerance per scene (C5 R27 with §6.6 check 10: "within a stated tolerance (default ±10% [J])"), and a larger miss changes the scene and shot budgets.

**Strands and cuts**

- **R10.** If cutting to a cap, then cut in this order and stop when the budget fits: (1) trim inside scenes (enter late, exit early; A3 §3.2 step 10 and A3 rule 3); (2) merge consecutive scenes in one place and time; (3) fold low-scoring scenes into neighbours; (4) delete a strand that carries no cardinal function of the spine; (5) drop a set piece; because each step changes the story more than the one before.
- **R11.** If a strand is deleted, then run the deletion test on each of its events and move every dependency a kept event needs (a line, a prop, an insert, an image) into a kept scene, logged with source lines, because a cut strand leaves orphan payoffs.
- **R12.** If two minor characters do one job, then consider a composite character, logged (*The Remains of the Day*'s Lewis), because each character costs screen time, a reference pack and a voice (C1, C2).
- **R13.** If a proposed merge would put an effect before its cause (a scene needs knowledge or an object that the merged-away scene supplies), then reject the merge or reorder with logged line changes, because causal order outranks runtime.

**Recurring devices**

- **R14.** If a device recurs (letter, refrain, bookend, repeated question), then list every occurrence, choose one screen policy for the whole work (§9 enum), and save the first occurrence's setup as a template (A3 R23), because scene-by-scene choices drift.
- **R15.** If a refrain repeats with one detail changed, then keep everything else identical and make the changed detail readable on screen, because the change is the information.
- **R16.** If the source later identifies a framing text's unnamed writer, then decide that text's voice with the whole work in view (the later character's voice, or no voice at all), because an early voice can contradict or spoil the reveal.

**Series and shorts**

- **R17.** If the format is a series, then break episodes at the source's major turns, not at equal word counts; each episode needs a value arc that closes at a different charge than it opens, and an ending turn (a revelation or a choice), because an episode is a story unit and the turn brings viewers back [J].
- **R18.** If an episode pays off a plant from an earlier episode, then list that plant in the episode's recap and build the recap from already-approved shots, because recaps cost no new generation.
- **R19.** If a short is cut from a long work, then choose one reduction: (a) one strand end to end; (b) a bookend of opening and ending with a minimal bridge; (c) one chapter. Prefer (b) when the ending pays off the opening, because a short holds one value arc.
- **R20.** If a bookend short skips the middle, then the bridge carries the time gap with a story-world marker (A3 §7.8) and imports every plant the ending needs (flashback shots or props, logged `flashback_import`), because the audience never saw the middle.

**Process**

- **R21.** If the macro plan is drafted, then show the user a one-page summary and the step outline, and lock scene IDs only after "approved", because every later file hangs on the scene list (C5 R1).
- **R22.** If the user changes format or runtime after approval, then re-run M4–M8 (§5) and mark changed steps; never renumber (A3 §5.1: cut scenes stay as `OMITTED`, added ones take letter suffixes such as `SC12A`; C5 §10.1), because approved downstream work must survive.
- **R23.** If the LLM proposes a cut, then it must list the cardinal functions touched (must be none), the dependencies moved and the seconds saved; the validator re-sums, because LLMs re-attach deleted events and misreport coverage (C5 R25).

---

## 5. The macro pass, step by step

Each step is a prompt the user gives an LLM; a script checks the numbers. Attach the source with numbered lines (screenplay) or numbered paragraphs (prose, C5 R3).

**Running it without code.** Paste each prompt into a chat with the numbered source attached, one step per message, and save each answer as a text file named after the step (`M1_events.md`, `M2_strands.md`, and so on). Where the text says "a script checks", ask the LLM for a table with one row per scene and a seconds column, paste it into a spreadsheet, and let the spreadsheet add the column: never accept a total the LLM typed itself (C5 R23). If an answer is wrong, reply "Revise only [item]" rather than asking for a fresh answer, so approved parts stay fixed.

**M0. Constraints.** *Prompt:* "Ask me, one at a time: format wish; maximum runtime; money for generation; hours I can spend reviewing; any festival target. Record my answers under `constraints`."

**M1. Whole-work event list.** *Prompt:* "Read the whole source twice. List every event in one or two past-tense sentences, no psychology, each with its source reference (screenplay: line range; prose: chapter.paragraph such as ch02.p024). Give two orders: the order told, and story-time order. Mark each event `cardinal` or `catalyser` by the deletion test, and for each cardinal event name the later events that depend on it."

**M2. Strands.** *Prompt:* "Group the events into strands. For each strand give its events, the chapters or scenes it occupies, the cardinal functions it carries, and every point where it feeds another strand (a plant, an object, a piece of knowledge)." A strand that feeds the spine's cardinal functions cannot be cut without moving those feeds (R11).

**M3. Natural runtime.** Screenplay: §6 (R2). Prose: R3. A script does the sums.

**M4. Format options.** *Prompt:* "Propose two or three independent macro plans within my constraints, chosen by R24: format, runtime target in seconds, scene and shot budgets, strands kept, compressed and cut, and what the audience loses. Do not argue for one." A script adds generated seconds (finished seconds × generation factor, typically 8, C1 §10), money at C1's three price tiers (about $0.07, $0.17 and $0.45 per generated second as of C1's date; re-check prices older than 30 days) and review hours (5–10 minutes a shot). *Worked sum:* 1,200 s × 8 = 9,600 generated seconds; × $0.07 = $672 at budget tier; 300 shots × 5–10 min = 25–50 review hours.

**M5. Keep/cut table.** One row per strand and per chapter (prose) or sequence (screenplay): decision (`keep`, `compress`, `composite`, `fold`, `cut`), reason, cardinal functions touched, dependencies moved, seconds.

**M6. Step outline.** *Prompt:* "Write the step outline for the chosen plan: one line per scene with heading, one-line event, source references, strand and cardinal-function IDs, A3's five-test scores and §7.9 rule, target seconds, compression operations." The validator runs §10's checks.

**M7. Series rules and episode rules.** For every recurring device, write a series rule (R14–R16). For a series, write the episode table (R17–R18).

**M8. Checkpoint M.** Show the one-page summary, keep/cut table and step outline. The user answers "approved" or corrects one item at a time ("Revise only step 7"). On approval a script locks scene IDs and writes the log (§9); then A3 §7 and C5 stages 2–9 run.

Time [J]: about an hour of the user's attention for a screenplay; two to four hours for a novel.

---

## 6. Estimating a screenplay's runtime: *The Catch*

**The disagreement.** A3 §5.2 measures *The Catch* at about 42–44 pages; C1 §10 costs a 20-minute film (1,200 s). C1 assumed a length; A3 measured pages. The question is what the pages play as.

**Counts** (script over the source, [J] method): 30 scenes; 221 speeches holding 1,579 words of dialogue; 543 action paragraphs holding 7,091 words; 3 `(beat)` parentheticals in SC13 (6 in the whole script). A re-run of A3's line model gives 41.7 pages. (A fact-check recount found 545 action paragraphs and 7,097 words, the difference being whether lines such as `> FADE IN:` count as action; it moves the total by about a second.)

**Method 1: pages ÷ 1.1** (Follows) → 42 ÷ 1.1 ≈ 38 minutes, credits included. Follows' figure contains a feature-length credit crawl (median 4.3 minutes); taking it out (a 110-page feature: 100 minutes less 4.3 of credits, about 0.87 minutes of story a page) gives about 36 minutes of story for 41.7 pages [J].

**Method 2: A2 defaults on three sample scenes, extrapolated.**

| Scene | Dialogue (A2: words ÷ 2.5 + 0.5 s per speech) | Action (A2 defaults, line by line) | Total |
|---|---|---|---|
| SC06 FREIGHT CAGE (l.198–299) | 6.5 s | 69–87 s (A4 WE1 times the fall, "The opening reaches them." to "This time they hear it land.", at 49.7 s; the lead-in adds 25–43 s, its lines included) | 75–93 s |
| SC10 KITCHEN (l.397–489) | 40.8 s | 53–76 s (Saye's "long moment" at the flask 3–4 s; the stethoscope "a long time" 3–4 s; the mint turn held at least 2 s; the `= THE CATCH` card) | 94–117 s |
| SC13 GLASS PARTITION (l.672–829) | 118.7 s + 3 s of `(beat)` | 57–76 s (the freeze held about 2.5 s, A4 WE2; "Silence." 2–3 s) | 179–198 s |

Action time per action word in these three scenes: 0.166–0.220 s. Applied to every scene (dialogue by A2's formula, action by that rate), the whole script comes to **1,916–2,304 s, 32–38 minutes**, before titles and credits.

**Method 3: beats × 14 s.** A2 counts 11 beats in SC10 and 16 in SC13: 154 s and 224 s, 13–64% above Method 2. Weighted delivery (Saye) runs slower than 2.5 words a second (A2 §15). Scaling Method 2's high figure by SC13's ratio (about 1.15) gives about 44 minutes, which is A3's pages read as minutes: an upper bound.

**Answer.** *The Catch* as written plays **about 35 minutes (range 32–44)**, plus about a minute of titles and credits [J]. Consequences:

1. C1's 1,200 s budget covers about 55–60% of the film. Scale its figures by about 1.75 (range 1.6–2.2): the typical-case $1,750 becomes about $3,100; the $1,500–4,500 range becomes about $2,600–7,900; its 300 shots become about 525; review time 45–90 hours [J, arithmetic on C1's [J] model].
2. It sits near the Academy's 40-minute short limit. If eligibility matters, set `runtime_target_s` ≤ 2,280 (R4) and trim (§7, option 2).
3. Record it as `runtime_estimate_s: {low: 1920, central: 2100, high: 2640, method: "pages/1.1; A2 defaults on SC06, SC10, SC13 extrapolated by word counts; beats x 14 s"}`.

---

## 7. Worked example (i): *The Catch* capped at 20 minutes

**Cardinal functions that must survive** (the brief's five, plus others found by the deletion test [J]):

| ID | Scene | Event (quoted where exact) | Why it cannot go |
|---|---|---|---|
| CF01 | SC01 | "The safety brakes are gone."; "Stop it hard and there's nothing under it to catch us." | SC06's fall; Iona's guilt ("I put them in that cage.", SC18) |
| CF02 | SC06 | "He has one hand she cannot see." / "A hard metal CLACK." | Everything mirrored follows |
| CF03 | SC07 | "The clip under it is empty." / backwards letters | First proof of the turn; plants SC13 |
| CF04 | SC10 | Mirrored hands; "Not mint." | Confirms the turn; delivers them to Saye |
| CF05 | SC12 | The carriage turned twice: "A turn." / "Our cage." | The rule Iona uses in SC26–27 |
| CF06 | SC13 | The recording: "You did that." / "Yes." | The core betrayal |
| CF07 | SC15–16 | The Figure takes Jude; Iona's cylinder cracks its strip | Plants SC25's repair ("the crescent dent her cylinder left in the cover") |
| CF08 | SC18 | Two engines for three people; the spare stays in the case | Sets up every later choice |
| CF09 | SC21 | The sleeve and the copied label "IONA VALE."; the flask in the cabinet; Iona's recorded message | SC23's burn order answers it: "You showed me sealed containers." |
| CF10 | SC23 | The Figure moves the beds; "Are we going to be all right?" / "I don't know." / "Go." | Her brother leaves; she stays |
| CF11 | SC24 | "She deletes the way home." | The climax choice |
| CF12 | SC25 | The chest opens; the animal; the tape | She saves what she hurt |
| CF13 | SC26–27 | The turn at the top of the climb; the crossing | Pays off CF05 |
| CF14 | SC28 | "RECEIVING" reads right; Eli's smile "on the wrong side of his face" | She is turned apart from them |
| CF15 | SC29 | "His wedding ring. On his right hand." / "like a ring and its reflection" | The ending image |

**Three options** (R1). Option 1: as written, about 35 minutes, 30 scenes. Option 2: trims and merges only, about 24 minutes of story plus credits (about 25), all strands kept, 25 active scene records. Option 3: the 20-minute cap below. The user chooses at checkpoint M.

**Option 3, scene by scene** (seconds are [J]; "as written" is §6's model midpoint):

| Scenes | As written | Target | Operation (logged) |
|---|---|---|---|
| SC01–SC05 rescue | 216 | 110 | Trim: keep brakes, rung, tooth, sill, flask-and-puck insert, gunshots, and "She gives Eli one shoe. He leaves the other." (paid off in SC21: "One shoe."); cut the "Can he climb?" and "I sent you to Saye" exchanges. |
| SC06 | 105 | 85 | Trim the lead-in only; A4's fall stays intact. |
| SC07 | 31 | 20 | Trim. |
| SC08 + SC09 | 57 | 30 | Merge: the wheel on the wrong side is found from inside the car. SC08 `OMITTED`, `merged_into: SC09`. Keep "Eli. Are we going to be all right?" / "Drive." |
| SC10 | 91 | 65 | Trim the stethoscope beat. |
| SC11 | 54 | 0 | Cut. Move "I inspect their trials. Your brother sent me enough to stop this one." to SC12's first beat; move the oxygen-cylinder plant ("a portable oxygen cylinder and a mask she has pulled off") to an insert in SC14, because SC16 needs "Her hand closes round the neck of the oxygen cylinder." |
| SC12 | 185 | 85 | Trim: keep the carriage turns, the dishes (nothing eats the culture), the sealed meal; cut the paper F and the napkin-ring speech. |
| SC13 | 182 | 105 | Trim the culture exposition already given in SC12; keep the recording, the freeze, "One body." / "You.", "I wasn't asking her.", the flinch. |
| SC14–SC16 | 84 | 55 | Trim. |
| SC17 + SC18 | 263 | 110 | Composite scene at SC18's place and time: Saye shows the returned camera's footage on a monitor while sealing Iona's suit. SC17 `OMITTED`, `merged_into: SC18`. |
| SC19 + SC20 | 141 | 55 | SC19 folds into SC20's first shot (stars below her feet); `merged_into: SC20`. |
| SC21 + SC22 | 71 | 45 | SC22 folds into SC21's last shot, through the hatch; `merged_into: SC21`. |
| SC23 | 124 | 75 | Trim. |
| SC24 | 57 | 45 | Trim; CF11 untouched. |
| SC25 | 92 | 65 | Trim. |
| SC26 + SC27 | 126 | 80 | Trim; keep both records (continuous). |
| SC28 | 107 | 55 | Trim. |
| SC29 | 94 | 50 | Trim; keep the rings and "In the car-" / "Yes." |
| SC30 | 36 | 25 | Trim. |
| **Total** | **2,116** | **1,160** | Plus 40 s of titles and credits = **1,200 s**. |

Trims and merges alone reach about 1,445 s (Option 2). The last 285 s needs R10 step 4 plus deeper trims: **deleting the Nell strand** (SC17's file, "NELL ROWAN. FLIGHT TEST."; SC18's question; SC20's dialogue; SC23's shared bed; SC24's recorded "Nell is here."; SC28's window) saves roughly 75–120 s; trimming almost every scene a further 5–30 s saves the rest. The deletion test (R11) finds five dependencies of Nell:

1. *The cell count.* Nell says "It brought theirs in with those. That's all I know.", then "Nell holds up two fingers." Move: the rack ("Five empty, the metal round them scorched") and "the second black cell locked between its shoulders" are already pictures; hold each an extra beat. No new line.
2. *Eli's exit.* Without Nell's bed, the Figure puts its own cell under Eli's bed. The choice survives; the lines survive.
3. *The Figure's motive.* In SC23 "it turns its head to Nell's shelf. To the drawing propped against the bowl: a window, a tree, a small house." Nothing kept carries this. Any replacement is an `invention` and goes to the user as an open question.
4. *Saye's guilt.* "Did it take anyone you sent?" (SC18) loses its answer; cut the line; Saye's arc thins. (Gain: one speaking character, reference pack and voice fewer.)
5. *Saye's last message.* SC24 opens with Saye's recording "They're here. Nell is here." (l.1380). Cut the second sentence (`trim`, logged); "They're here." still tells Iona that the others arrived [J: the source does not name them], and "Iona. Leave the ship." is untouched.

**The suggested SC20 + SC23 merge fails R13.** SC23 opens "The courier returns to the recess. Iona brings the spare engine back into the human rooms." (l.1267), and Saye's recorded order answers SC21: "You showed me sealed containers. We do not know what is outside them. The whole room has to burn." SC21's message in turn reports SC20 ("It brought me air." ... "Send the spare."). The courier's round trip between the two human-room scenes causes SC23. A merge works only if SC21–22 move before SC20 and two message lines change: about 25 s saved for three logged inventions. Offer it only below 20 minutes.

**Losses at 20 minutes:** breathing room, Nell, Saye's guilt, the Figure's motive image. Recommendation [J]: Option 2 (about 25 minutes) keeps the film whole; choose Option 3 only for a hard cap.

---

## 8. Worked example (ii): *The Long Places*, three macro plans

### 8.1 What the whole work contains

About 49,400 words in 14 chapters (script count): 3,000–4,700 per chapter; chapters I–XIII open with an italic letter of 518–744 words; XIV has none at its head and ends by repeating letter I whole. By the Nebula bands this is a short novel, not a novella [J]. A3 Ex5 found 10 candidate scenes in chapter I; at that density the whole book yields about 140 (natural runtime 280–350 minutes at 2–2.5 minutes a scene, R3).

**Strands (M2)**

| ID | Strand | Chapters | Carries |
|---|---|---|---|
| ST1 | Nilay and Emre (spine) | I, II, IV, VII, X, XIII, XIV | The missing brother; the ending |
| ST2 | Melek and the keeping | I, II, IV, V, VII, X, XI | The rules; the handover of the oil can |
| ST3 | The Trust and Halden | throughout; key in IV, XIII | The letters in the slope; Book Zero; the vigil protocol |
| ST4 | Márton's measurements | III, VI–X | Hollow, triangle, clocks; his death; the elimination prints |
| ST5 | Priska's air | V, VII–XI, XIV | The explanation; the witness in XIV |
| ST6 | Yusuf's channel | VI–VIII, XII | The count of 41; exposure; the unwatched 14 seconds |
| ST7 | The breach and the far lamplighters | VII, VIII | The chamber below the fourth door |
| ST8 | The village sittings | I, V, VIII, X, XI | Havva, Seher, Leyla, the queue and the fence |
| ST9 | Malta (Hypogeum, Mrs Vella, the child's shoe) | IV | A parallel site |
| ST10 | The List and Ayios Nikandros | XIII | The unpaid keeping |
| ST11 | Ministry, Kaya Bey, the committee | II, V, VIII, X, XI | Orders, closure, the fence |

**Cardinal functions of the spine (M1)**

| ID | Ref | Event |
|---|---|---|
| CF01 | ch01.p030–p031 | She types item 51, "*Hand print, right, red ochre, above the first marks, lower wall.*"; the file lists "*Brother — missing, earthquake, September 1999 — province.*" |
| CF02 | ch01.p034–p036 | The breathing shaft; warmth "against her right shoulder" |
| CF03 | ch02.p022–p031 | 1999: Emre vanishes on 4 September; at eighteen she is shut below the fourth door; humming; the red ribbon gone from the door iron |
| CF04 | ch04.p027, p042 | The Register's margin "*4–5.ix. Kept the hours. A.H.*"; the founder's slip "*Below the fourth door, count nothing.*" |
| CF05 | ch07.p016–p032 | The coring breaks into a void (the camera falls into it on 4 September); they enter a finished chamber; "Is the fire mountain awake?" |
| CF06 | ch10.p016, p021 | Márton dead at the fourth door; elimination prints taken |
| CF07 | ch11.p037 | Melek dies; the oil can passes to Nilay |
| CF08 | ch13.p045, p059 | The Vigil of the Sealed Hour; "The transfer," he said, "was the least I could do." |
| CF09 | ch14.p007–p035 | The vigil; Emre with "A strip of red ribbon."; "It was me." / "I know it now." |
| CF10 | ch14.p038, p055 | Her palm beside the old print; "*The print is mine.*" |

### 8.2 Series rules, decided once (R14–R16)

| Device | Source occurrences | Rule for all three plans |
|---|---|---|
| Letters "*To the one who keeps the lamps after me:*" | Heads of I–XIII; letter I repeated whole, all 14 paragraphs identical (checked by script), after XIV (ch14.p063–p076 = ch01.p001–p014) | Feature: `open_and_close` (letter I dramatized, hands only, 4–6 lines of voice-over, at both ends; the others live in images, as the Coens' *No Country for Old Men* treats Bell's chapter monologues, A3 §7.7). Series: `episode_cold_open`, one letter per episode, dramatized. Short: `open_and_close`. |
| Threshold refrain "At the mouth of Kırk Oda the air shaft breathed." | ch01.p034, ch06.p030, ch11.p054, ch14.p059 | `template_refrain`: one saved setup and sound. Correction to A3 Ex5: the paragraph is word for word *except its figure*, "eighteen minutes", then "nineteen", "twenty", "eighteen" again (checked by script against the source); in XI the same paragraph also opens with a lead-in sentence, "She came up at full dark with the oil smell on her hands.", which belongs to the scene before the refrain, not to the refrain. R15: show the figure (a watch or notebook insert), change nothing else. |
| Letter II's keeper (the humming) | ch02.p002–p012; in XIV Emre tells of humming to "a girl behind a stone" and Nilay answers "It was me." (ch14.p021–p022) | R16: no voice-over for letter II in any plan; carry it as the humming sound, which Emre's scene later explains. |

POV plan (all plans): close third person on Nilay (A3 §7.3); keeper hands unmarked (A3 R21). Declared breaks: letter scenes (keeper's hands); Márton's and Priska's scenes in the feature and series (`pov: MARTON`, `pov: PRISKA`); ch14.p008–p010, the book's only second-person narration, as subjective POV shots.

### 8.3 Plan A: feature, about 100 minutes

**Budgets.** 6,000 s; 48 scenes at about 125 s; 1,200–1,500 shots at a 4–5 s ASL; at C1's typical 8× factor, 48,000 generated seconds, $3,400 (budget tier) to $21,600 (premium), and 100–250 review hours [J].

**Scenes per chapter:** I 5, II 5, III 3, IV 3, V 3, VI 3, VII 5, VIII 2, IX 2, X 3, XI 4, XII 1, XIII 3, XIV 6 = 48.

**Kept:** ST1 whole; ST7 as the midpoint set piece. **Compressed:** ST2–ST6 (ST6 to the 41 count, the viral post and the unwatched stick); VIII's four statements into one intercut scene; XI's queue and fence into a montage; ST11 to one scene (the closure memo dated before the request). **Cut:** ST9 Malta (the knock already comes from Melek; the child's shoe is lost); ST10; Leyla's vigil; most of XII; Marques (her "Two clocks is an anecdote" moves to Priska, `move_line`; caution: in ch10.p020 Marques says it *to* Priska, "I am sorry, Doctor Vogel; grief is not a witness", so in Priska's mouth it becomes her own doubt, a new reading to put to the user; the alternative is to give it to the ministry, ST11); the lab minutiae except XIV's certificate. **Loses:** the Malta parallel, much of the village's grief, Yusuf's redemption.

A3 Ex5's ten chapter-I candidates become five steps: 1 → 01; 2 and 3 → 02 (composite scene); 4 → 03, with 5's clock saying folded in as one line; 8 → 04, with 7's crossed-out forty-one folded in as an insert on the form (it plants VI's count); 10 → 05; 6 and 9 cut (the team arrives in III). First steps (M6 format):

| Step | Heading | Event | Refs | Tests 1–5 | Target |
|---|---|---|---|---|---|
| 01 | INT. KIRK ODA - FIRST GALLERY - BEFORE DAWN (PERIOD UNSTATED) | A keeper teaches a child the nine lamps; the day's mark is cut | ch01.p001–p014 | 1 1 1 1 0 | 90 s |
| 02 | EXT. ROAD'S END / INT. MOTHER'S HOUSE - DAY | Nilay arrives; the mother's bed and towel; the Trust's "*in advance*" | ch01.p015–p017 | 0 0 1 1 1 | 120 s |
| 03 | INT. KIRK ODA - GRANDMOTHERS' CUPBOARDS - EVENING | Melek, "Why nine?"; the rain rule; the clock saying | ch01.p020–p027 | 0 0 1 1 1 | 110 s |
| 04 | INT. MOTHER'S HOUSE - NIGHT (as A3 Ex5) | Item 51 typed at even pace; the crossed-out forty-one; the sibling line | ch01.p029–p031 | 1 1 1 1 0 | 80 s |
| 05 | INT./EXT. KIRK ODA - MOUTH - NIGHT | Refrain (18); the warmth at her right shoulder | ch01.p033–p037 | 1 1 1 1 0 | 120 s |

### 8.4 Plan B: limited series, six episodes of about 48 minutes

**Budgets.** About 17,300 s; about 120 scenes (86% of the natural 140); 3,500–4,300 shots; about 138,000 generated seconds, $9,700–62,300 [J]. Nearly every strand survives; ST10 shrinks to one insert in Book Zero.

| Ep | Chapters | Value arc (open → close) | Ending turn | Recap must show |
|---|---|---|---|---|
| 1 | I–II | Nilay's grief: contained (+) → reopened (−−) | The ribbon gone from the door iron, 1999; "The rooms were full of weather." | none |
| 2 | III–IV | Márton's certainty: + → −; Nilay: stranger → taught | Melek: "Below the fourth door, you don't count."; Nilay lights the ninth lamp | "*in advance*"; "*Valletta, 7.ix.1999*"; the crossed-out forty-one |
| 3 | V–VI | Yusuf: unseen (−) → exposed (−−); Priska: explained → haunted | Four million views; the pin on the map; refrain (19) | The knock (IV); the crossed-out forty-one (I) |
| 4 | VII–VIII | The hill: closed → opened; the witnesses: agreeing → divided | The coin's empty foam circle; the closure memo dated before the request | "count nothing"; the 1999 low room; 4 September; the hollow |
| 5 | IX–XI | Márton: vindicated (+) → dead (−−−); Nilay: licensee → keeper on trial | Nilay's first round; refrain (20) | The three watches and 1997 (III); the hollow and triangle (III) |
| 6 | XII–XIV | Nilay: brother lost (−−−) → brother kept (+, with loss) | "*The print is mine.*"; refrain (18); letter I | The ribbon, the humming, item 51, the elimination prints, "*4–5.ix*", Melek's four sentences |

Episodes 5 and 6 carry about 10,500 and 11,400 source words against an 8,200 average; compress XII hardest (R17: breaks at turns, not word counts).

### 8.5 Plan C: short, 15 minutes, chapters I and XIV as a bookend (R19 b)

**Budgets.** 900 s; 10 scenes plus one imported flashback; about 180–225 shots; about 7,200 generated seconds, $500–3,200; 15–40 review hours [J]. **Kept:** ST1 and the keeping frame; Priska reduced to the witness. **Cut:** everything else. **Bridge** (R20): the ribbon and the humming are imported from II; the time jump rides on the mother's line "He would be forty." and the oil can in Nilay's hands.

| Step | Heading | Event | Refs | Tests 1–5 | Target |
|---|---|---|---|---|---|
| 01 | INT. KIRK ODA - FIRST GALLERY - BEFORE DAWN (PERIOD UNSTATED) | Keeper teaches the child; voice-over ends on "*begin*" | ch01.p001–p014 | 1 1 1 1 0 | 90 |
| 02 | INT. MOTHER'S HOUSE - NIGHT (JUNE; as A3 Ex5) | Item 51 typed; her thumb on the sibling line; folder shut | ch01.p030–p031 | 1 0 1 1 1 | 60 |
| 03 | INT./EXT. KIRK ODA - MOUTH - NIGHT | Refrain (18, watch insert); warmth at her right shoulder | ch01.p033–p036 | 1 1 1 1 0 | 80 |
| 04 | INT. KIRK ODA - LOW CORRIDOR - NIGHT (SEPTEMBER 1999) | Flashback, three shots: a strip of red tied on the door iron; the stone shut; humming (`flashback_import`) | ch02.p024–p030 | 1 0 1 1 0 | 45 |
| 05 | INT. DIG HOUSE - DAY (4 SEPTEMBER, THE NEXT YEAR) | "He would be forty."; the letter; the wax: "Nothing. That's why it's you."; watch stopped at 9:20 | ch14.p001–p006 | 1 1 0 1 1 | 90 |
| 06 | INT. KIRK ODA - ANSWERING NICHE - NIGHT | The round; the tin box laid; two knocks, two breaths | ch14.p007 | 1 0 0 1 0 | 60 |
| 07 | INT. THE OTHER KEEPING - MORNING | She wakes; the stemmed lamp; the letter dated tomorrow; insert "*and I did not cry until the ribbon.*" | ch14.p008–p011 | 1 1 1 1 0 | 75 |
| 08 | same, continuous | Emre; the ribbon; "You filled the lamp badly, that night"; names; "It was me." / "I know it now."; "a road that's long instead of far" | ch14.p012–p035 | 1 1 0 1 1 | 210 |
| 09 | INT. KIRK ODA - LOWER WALL - CONTINUOUS | Her palm beside the old print; "To the one who keeps the lamps after me." | ch14.p038–p040 | 1 1 0 1 0 | 75 |
| 10 | EXT. KIRK ODA - MOUTH - FIRST LIGHT (5 SEPTEMBER) | "The wax?" / "Broken. By me, below."; refrain (18) | ch14.p041–p047, p059 | 1 1 0 1 0 | 45 |
| 11 | INT. DIG HOUSE - WINTER | Rendering the wall: a keeper teaching a child (step 01's template); voice-over "*begin*" | ch14.p061, p076 | 1 1 0 1 0 | 45 |
| | | | | **Total** | **875 + 25 s titles = 900** |

**Adaptation log for Plan C:** `flashback_import` (step 04, ch02.p024–p030); `delete_strand` ST2–ST4 and ST6–ST11, with reasons (ST5 compressed to the witness); `lost_resonance`: the watch stopped at 9:20 echoes the 1999 shock "At twenty past nine" (ch02.p022), unplanted here; `replace`: step 09's picture stands in for the certificate and fingerprint chit (ch14.p052–p055), since step 02's item 51 already says "Hand print, right". **Open questions:** keep Priska or make the witness nameless; show Emre's face (the book gives "their mother's jaw") or keep him at the lamp's edge; include "Emre Arat kept here" as a written insert in step 11.

---

## 9. Fields this subject adds

Enums are lowercase `snake_case`; an empty value is `"none"`, an empty list `[]`; each field carries C5's authority mark (`extracted`, `authored`, `derived`).

| Level | Field | Meaning | Allowed values / example |
|---|---|---|---|
| film | `format` | Kind of finished work | `short` \| `feature` \| `limited_series` |
| film | `runtime_target_s` | Target incl. credits (C5's `runtime_target`, with its unit named) | `1200` |
| film | `runtime_estimate_s` | Natural runtime range and method (derived) | `{low, central, high, method}` |
| film | `constraints` | User's M0 answers | `{max_runtime_s, budget_usd, review_hours, festival}` |
| film | `scene_budget`, `shot_budget` | Derived budgets | `{scenes, avg_scene_s}`; `{shots, target_asl_s}` |
| film | `strands[]` | `id`, `name`, `chapters_or_scenes`, `cardinal_ids`, `feeds[]`, `decision`, `reason`, `seconds` | decision: `keep` \| `compress` \| `composite` \| `fold` \| `cut` |
| film | `strands_kept`, `strands_cut` | ID lists (derived from `strands[]`) | `["ST1","ST2"]` |
| film | `cardinal_functions[]` | `id`, `event`, `source_refs`, `depends_on_it[]` | `CF11`, "She deletes the way home." |
| film | `series_rules[]` | `id`, `device`, `occurrences[]`, `policy`, `template_setup`, `varies`, `notes` | policy: `open_only` \| `open_and_close` \| `every_return` \| `episode_cold_open` \| `template_refrain` |
| film | `pov_plan` | Default POV and declared breaks | `{default: "NILAY", breaks: [...]}` |
| film | `episodes[]` | `id`, `chapters`, `runtime_target_s`, `value_arc {value, open, close}`, `ending_turn`, `recap_plants[]` | series only, else `[]` |
| film | `macro_checkpoint` | Approval record | `{status: approved \| pending, version, date}` |
| scene | `step_id`, `source_refs`, `strand_ids`, `cardinal_ids` | Step-outline links | `ch14.p012-p035`; `L1376-1427` |
| scene | `five_test`, `a3_rule` | A3 §7.9 scores and the rule applied | `[1,1,0,1,1]`; `own_scene` \| `fold` \| `cut` |
| scene | `target_duration` (C5), `merged_into` | Seconds; where an `OMITTED` scene went | `85`; `SC18` |
| scene | `status`, `heading`, `event`, `compression_ops[]` | Whether the step plays; its scene heading; the one-line event; the log operations applied to it | `active` \| `omitted`; `"INT. SAYE'S HOUSE - KITCHEN - BEFORE DAWN"`; `["trim"]` |
| film | `open_questions[]` | Questions for the user at checkpoint M, one decision each | `["Replacement image for the Figure's motive once Nell is cut?"]` |
| log | `adaptation_log[]` | `op`, `what`, `from`, `to`, `reason` (plus `five_test` for prose passages, A3 §7.9) | `{op: "move_plant", what: "oxygen cylinder", from: "L498", to: "SC14"}` |
| log | `op` | Adaptation-log operation | `trim` \| `merge_scenes` \| `fold_into` \| `composite_character` \| `move_line` \| `move_plant` \| `delete_strand` \| `reorder` \| `invention` \| `replace` \| `flashback_import` \| `lost_resonance` |

**Template, `adaptation_plan.json`** (written after C5 stage 1's `story_analysis.json`, whose `events`, `spines`, `plants_payoffs` and `pov_plan` it reads; values from §7):

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

---

## 10. Checklists

**Before checkpoint M (validator and human):**
- Every kept cardinal function is in a step.
- Step targets sum to `runtime_target_s` ±10%, credits and cards included.
- Every step cites sources or is labelled `invention`.
- Every deleted strand's dependencies are moved or accepted as losses.
- No merge puts an effect before its cause (R13).
- Every recurring device has a series rule listing all occurrences.
- Series: each episode has a value arc that changes charge, an ending turn, and recap plants from earlier episodes.
- Short: one reduction type; every plant the ending needs is present.
- The summary states what the audience loses.
- Screenplay: `OMITTED` and `merged_into` set; no renumbering.
- Every quoted line in the step outline and every series-rule occurrence is found verbatim in the source by a text search (not by the LLM's say-so).
- If a festival or award is a goal: R4's limit, the festival's own limit and the AI-category flag are shown in the summary.

**After checkpoint M:** IDs locked; log written; A3 §7 runs only on kept passages.

---

## 11. Failure modes

| Failure | Sign | Fix |
|---|---|---|
| Scene explosion from prose | Chapter-by-chapter adaptation yields about 140 scenes | M1–M6 before A3 §7; budget first |
| Orphan payoff | A kept scene refers to something never shown (SC16's cylinder after SC11 is cut) | R11: deletion test; `move_plant` |
| Effect before cause | A merge needs knowledge the removed scene supplied (SC20 + SC23) | R13: reject or reorder with logged lines |
| Cardinal function lost | A CF with no step | Restore it (P3) |
| LLM re-attaches cut material | The step outline cites a deleted strand | Validator checks strand IDs against `strands_cut` |
| Refrain drift | Returns shot differently | Template setup (A3 R23); only the declared variable changes |
| Cost blind spot | Runtime approved without cost or review hours | M4 adds C1's formula |
| Phantom occurrence | A series rule lists a scene where the device never appears (an earlier draft of §9's template listed SC13 for "Are we going to be all right?"; the line is at l.390 and l.1352 only) | A script searches the source for the device's text and writes `occurrences[]`; the LLM only proposes the policy |

---

## 12. Conflicts with other files, and open questions

- **C1 (20 minutes) vs A3 (42–44 pages):** resolved in §6; C1's costs should scale by `runtime_estimate_s.central / 1200`.
- **C5's `runtime_target`** has no unit; rename it `runtime_target_s`.
- **C5's checkpoint A** (scene list, stage 0): for a screenplay, A confirms the parsed scene list first; M comes after stage 1 and may only mark scenes `OMITTED` or `merged_into`, never renumber them (D1 §10.5 follows the list as locked). For prose, A confirms the paragraph numbering (and, per D4 rule 4, the rights status), but no scene list exists until the step outline, so M is where prose scene IDs are first locked.
- **D13's runtime figures** for *The Catch* (1,926–2,309 s, central 2,118 s) differ from §6's (1,916–2,304 s; central rounded to 2,100) only by rounding and the action-rate precision; use §6's `runtime_estimate_s` as the recorded value and D13's as the script re-run.
- **D10's shot counts:** D10 notes that a slow-cinema treatment of *The Long Places* Plan A needs roughly 400–500 shots, not §8.3's 1,200–1,500 at a 4–5 s ASL. The ASL is a style choice made at checkpoint M; the shot budget follows it.
- **Award categories for AI films (§3.3):** the Academy's short limit is settled (40 minutes with credits), but whether a generated film counts as live action or animation is not; flag it whenever R4 applies.
- **A3 Ex5** calls the threshold refrain word for word; its minute figure changes (§8.2).
- **A3 R21 and Plan C:** the ending hints that Nilay may be the keeper whose hands open and close the film. Keep them unmarked unless the user decides otherwise at checkpoint M.
- **Unverified:** the two stories' exact word lengths (Brokeback about 10,000 by one online text; "Story of Your Life" only by its Nebula novella category, 17,500–40,000); festival limits other than Sundance 2027; Plans A–C costs (C1's model, stale after 30 days). Follows' scene count is from mostly unproduced scripts.
- **For the user:** *The Catch*: Option 1, 2 or 3 (if 3, the Figure's motive image). *The Long Places*: Plan A, B or C; letter policy; keeper voices; Emre's face; in Plan A, who speaks Marques's "Two clocks is an anecdote"; the ASL (4–5 s, or slow cinema, D10).

---

## Sources

Web (all checked 2026-09-27; cited in the text as S1–S19):

1. Stephen Follows, page-per-minute study (30 March 2026): 2,520 US Letter and 351 A4 feature scripts; median ratio 1.1; 18.2% within 0.95–1.05; median end crawl 4.3 minutes. https://stephenfollows.com/p/is-the-page-per-minute-rule-correct [V]
2. Stephen Follows, "Defining the average screenplay" (4 February 2019): 12,309 scripts, mostly unproduced. https://stephenfollows.com/p/what-the-average-screenplay-contains [V]
3. Robert McKee, *Story* (1997): scene counts, "Rhythm and Tempo", "The Problem of Adaptation" (pp. 364–370), archive.org full text. https://archive.org/stream/RobertMcKeeStorypdf/Robert%20McKee%20-%20Story%20(pdf)_djvu.txt [V]
4. Academy of Motion Picture Arts and Sciences, 97th Academy Awards, Rule Sixteen, Live Action Short Film (definition I.A read from the PDF). https://www.oscars.org/sites/oscars/files/2024-04/97_live_action_short_rules.pdf [V]
5. SFWA, Nebula Rules (word-count categories). https://nebulas.sfwa.org/about-the-nebulas/nebula-rules/ [V]
6. Wikipedia, "Arrival (film)". https://en.wikipedia.org/wiki/Arrival_(film) [V]
7. Wikipedia, "Story of Your Life". https://en.wikipedia.org/wiki/Story_of_Your_Life [V]
8. Wikipedia, "Brokeback Mountain" and "Brokeback Mountain (short story)". https://en.wikipedia.org/wiki/Brokeback_Mountain ; https://en.wikipedia.org/wiki/Brokeback_Mountain_(short_story) [V]
9. Wikipedia, "The Remains of the Day (film)". https://en.wikipedia.org/wiki/The_Remains_of_the_Day_(film) [V]
10. Wikipedia, "Normal People (TV series)". https://en.wikipedia.org/wiki/Normal_People_(TV_series) [V]
11. Wikipedia, "An Occurrence at Owl Creek Bridge (film)". https://en.wikipedia.org/wiki/An_Occurrence_at_Owl_Creek_Bridge_(film) [V]
12. StudioBinder, "How Long is a TV Show Script". https://www.studiobinder.com/blog/how-long-is-a-tv-show-script/ [V]
13. Wikipedia, "Step outline". https://en.wikipedia.org/wiki/Step_outline [V]
14. T. Otake, S. Yokoi, N. Inoue, R. Takahashi, T. Kuribayashi, K. Inui, "Modeling Event Salience in Narratives via Barthes' Cardinal Functions", COLING 2020. https://arxiv.org/abs/2011.01785 [V: title and abstract only]
15. Newsweek, "'Normal People' on Hulu: The Biggest Changes from the Sally Rooney Book" (Abrahamson quoted from BT magazine). https://www.newsweek.com/normal-people-hulu-book-changes-novel-sally-rooney-scenes-1500850 [V]
16. Sundance Institute, "Rules & Regulations for Submitting to the 2027 Sundance Film Festival" (June 2026): short films "less than 50 minutes, including credits". https://www.sundance.org/wp-content/uploads/2026/06/2027_Submissions_Rules.pdf [V]
17. Academy, 98th Academy Awards, Live Action Short Film and Animated Short Film rules (April 2025): definitions I.A–C, read from the PDFs. https://www.oscars.org/sites/oscars/files/2025-04/98th_aa_live_action_short.pdf ; https://www.oscars.org/sites/oscars/files/2025-04/98th_aa_animated_short.pdf [V]
18. Academy press release, "Awards rules and campaign promotional regulations approved for 99th Oscars" (1 May 2026): generative AI, human-authored screenplays, human performance, short-film deadlines 13 August and 8 October 2026. https://press.oscars.org/news/awards-rules-and-campaign-promotional-regulations-approved-99th-oscarsr [V]. The 99th category rule PDFs refused this session's download; the 40-minute definition for the 99th year is [U] beyond a search summary.
19. xpressenglish.com, "Brokeback Mountain by Annie Proulx" (text and word count, 10,650 words). https://xpressenglish.com/brokeback-mountain/ [U: an unofficial text; counts vary by edition]

Library files: A2 (S5.6, Step 9 defaults, sc10 and sc13 beat counts); A3 (§5.2, §7.1–7.9, R3, R13, R21, R23, Ex5); A4 (WE1 and WE2 timings); C1 (§10 cost model); C5 (R1, R14, R23, R25, R27, §10 IDs and data model).

Test sources: `/root/.claude/uploads/fbbb0203-69e3-5f8e-b675-32d722ec580d/1edae70d-35_The_Catch_-_workshop_revision_of_Final4.txt` (line numbers as cited); `/root/.claude/uploads/fbbb0203-69e3-5f8e-b675-32d722ec580d/5dcd8176-19_The_Long_Places_-_revised_by_Claude_final.md` (paragraph references `chNN.pNNN` count non-empty lines within each chapter, letters included, section breaks excluded).
