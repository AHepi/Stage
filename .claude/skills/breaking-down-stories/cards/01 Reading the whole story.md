# Card 01. Reading the whole story

Read whole at step 2; step 1 reads only "Length". "D16 R5" is rule 5 in D16 §4; `stage.py lib D16 R5` prints it.

## The job

The Catch's plan fits on one page: an event for each scene, nine groups of scenes, the crisis `SC24 "She deletes the way home."`, the climax `SC26..SC27` with the film's only scene intensity 10, plants and payoffs, and who knows what, from when (K12, K13).

Step 1 confirms the scene list and asks the length question. Step 2 plans the whole film before any scene is designed: PLAN, SEQUENCE, PLANT, FACT and the SCENE plan fields (tone is card 08).

- An **event** is the one change a scene delivers, one past-tense sentence with "no psychology, no sociology" (D2 §3.4; A3 §1).
- A **sequence** is a run of scenes that answers one short question; the user sees "group 3" (D16 R12; A3 §1).
- A **value** is a quality of a life with two poles; the **core value** is the one the whole story turns on (A2 §2).
- The **climax** is the scene, or unbroken run, where the core value turns for the last time; the **crisis** is the hardest choice that forces it (D16 R5-R6).
- A **peak** is where one component, such as colour, the tightest size or the longest hold, is strongest (D16 §6).
- A **plant** is a detail placed early so that a later **payoff** makes sense (A2 §2).
- A **story point** names a moment before beats (card 03) exist: a scene ID and a quote of at least `quote_anchor_words_min` words; code resolves it to a beat at step 7.
- A **strand** is a line of events following one character or question; **dramatic irony** is the audience knowing what a character does not (D2 §1; A3 §1).
- **Scene intensity** is a scene's pressure across the whole film, scaled in `scales` (B3 §2.6).

## Questions in order

1. Have you read the whole story? Plants in scene 1 often make sense only from scene 30 (A3 §3.2 step 1).
2. What changes in each scene? The deed, past tense; if nothing changes, say so (D2 §3.4; A3 R1).
3. What does the story turn on? The core value with two poles; the theme as a question the story tests, not a moral; the core opposition as two nouns (B4 §3.1 steps 1-2).
4. Where does the core value turn for good? Chart two or three candidate values across all scenes; keep the one whose last big turn is the last major reversal, caused by the protagonist, answering the story's question (D16 R3).
5. How intense is each scene across the film? Go from the top: 10 only for the climax; 8 or 9 a life at stake or a reversal that changes the whole plan (9 for at most the one or two biggest before the climax); 6 or 7 a turn that changes a relationship or the plan; 4 or 5 a minor turn, a test or needed information; 2 or 3 set-up, travel, aftermath; 1 nothing at stake. Never derive it from beat scores (B3 §2.6).
6. Where do the sequences break? Test the author's own breaks first, such as a cut to black followed by a title card (D16 R8); each sequence ends inside its act and answers one question with a quoted line, written in its `story_job` (D16 R12).
7. What is planted, and where is it paid off? Every scene is both (A2 P12); write both ends as story points (PLAN-02).
8. Who knows what, from when? Only for suspense, mystery and dramatic irony, write a FACT naming the `element` that would give it away in frame (A4 §6.5; A3 R4).
9. **Whose scene** is it: whose place and knowledge does the camera share (A3 §7.3)?
10. Which events can the story not lose? The **deletion test**: if this were gone, which later events would lose their cause (D2 §1, P3)?

## Length

Example: at checkpoint A (the scene-list stop) The Catch's message says "I found 30 scenes, one for each heading in your script" and asks one question: "as written it runs about 35 minutes (32 to 38; the page count suggests up to 44). Keep everything, or give me a target?" [keep everything] (K25).

Code reads the story at step 1 and makes the **first estimate** per scene from dialogue words, speeches, "(beat)" marks and action words (`speech_wps_default`, `speech_floor_extra_s`, `pause_tiers`, `v0_action_seconds_per_word`), summed over scenes (D13 §4.1; D2 §6). Never add these up yourself (D13 R4).

Your part:
- Read only the **odd-lines report** (the lines code could not place); code extracts, you classify and confirm (D14 principle 3).
- Scene headings are the only scene boundaries. A secondary heading (`CLOSE ON`, `LATER`) is a note inside its scene; a modifier after the time, such as `(ON THE TABLET)`, is a presentation note (A3 §4.1, §4.3). Keep the script's heading count even where `CONTINUOUS` headings play as one action (A2 Step 0).
- A heading that may hold two scenes, or a mid-film title card, goes under "small choices I made", defaulting to the script's count (A2 Step 0).
- State the count as a fact, and the length as a range, never one number (D2 P2; D13 P3). The page count is a cross-check that runs high on short scripts, so print it only as "the page count suggests up to" (D13 §4.1, R22; K25).
- A first estimate under `short_runtime_max_s` makes `format: short` a small choice, otherwise `feature` (D2 §1, §3.3).
- A target from the user starts step 2's compression plan, in this order, stopping when it fits: trim inside scenes, merge scenes in one place and time, fold weak scenes into neighbours as a shot, line or prop, delete a strand, drop a set piece. Lines are never rewritten; a cut scene becomes `omitted` or `merged_into`, never renumbered (D2 R10, R22; A3 §5.1).
- Prose: checkpoint A only states chapters and words ("I found 14 chapters, 49,152 words"); length is chosen at checkpoint P, the plan choice (D2 R1, R3).
- Without code, write each scene's `lines` as a quote anchor pair (its first and last line, quoted exactly) and never total an estimate by eye (D14 R32; D13 R4).

## Translation menus with pitfalls

Pick at most one reading per row; tie it to a line, object or action in this story.

| Finding | Plan field | Pitfall |
|---|---|---|
| The hardest choice | PLAN `crisis`, a story point | calling it the climax (D16 §11) |
| The last turn of the core value | PLAN `climax`, a scene or range | the loudest, most spectacular scene (D16 §11) |
| A component peaking away from the climax | PLAN `peak` with `reason` (counterpoint, a calm picture under high pressure; a planted rhyme) | an unexplained early peak spends the climax's room (D16 R15; A2 R31) |
| The audience knows more than a character, or the same | FACT `mode: suspense` or `dramatic_irony`; `mystery` | a FACT for every scene (A4 §6.5) |
| A detail the story buries | PLANT at a low `plant_emphasis` | a push-in announces the ending (A3 R22) |
| What a scene holds | `tags`: `suspense_and_reveal` where a FACT's element is in play (A4 §6.5); `prose_interior` for thought (A3 §7.2); `montage_and_time` for passing time (A3 §7.4) | tagging by genre |

## Budgets and saved choices

- `event_unit_scenes` scenes per unit writing events; the one unit writing PLAN reads only the event lines (D16 R19).
- Exactly one scene intensity 10, or one 10 range, on the climax (PLAN-01; B3 §2.6).
- After a scene of intensity `high_intensity_scene_min` or more, the next scene's target shot length runs longer (FILM-07; A4 §6.9).
- About `fact_records_typical` FACT records at standard, a guide, never a check (A4 §6.5).
- A plant at most `plant_emphasis_max` loud (K11; A3 R22). Every peak away from the climax has a reason (PLAN-03; D16 R15).

## The baseline is a strong answer

Static, the owner's eye height, a normal lens, room sound (the place's steady background) are choices, not failures; depart only for a reason you can cite. In planning the defaults are the story's own: its order, its full length ("keep everything"), a plain cut between scenes unless the script writes another join (A4 §5.1), and low intensity for set-up and travel (B3 §2.6).

## Cliché traps

- **The loudest scene called the climax.** Test: does the core value reverse again after it? Fix: D16 R5; the fire in The Catch is spectacle, and the value turns later (D16 §11).
- **The theme as a moral** ("family matters"). Test: could the story answer it either way? Fix: a question (B4 §3.1).
- **Events with psychology** ("Iona realises she has changed and feels lost"). Fix: the deed, past tense (D2 §3.4).
- **Every scene a 7.** Test: one highest peak, one quietest point? Fix: B3's list, top row first (B3 §2.6).
- **Template acts.** Fix: flag a role outside its usual place; never move it to fit (D16 R20).
- **The any-film test**: a theme question that fits any film on this subject fails (B4 §3.1).

## Reasons that fail and reasons that pass

- Fails `climax: SC24`, "the most dramatic scene". Passes `climax: SC26..SC27`: home or stranded turns for good at "Nought." / "The engine crosses.", and `SC24 "She deletes the way home."` is the crisis that forces it (D16 §8.3, R5; K12).
- Fails "Iona is shaken to learn she is different." Passes "Saye proved with a mint leaf that the three had been turned, and took charge of where they would go." (D2 §3.4).
- Fails `peak: tightest_size | scene: SC13 | reason: emotional impact`. Passes `reason: the confession's turn lands inside Iona; the climax is played wide and still, in counterpoint` (K12; D16 R16).

## Two worked examples

### The Catch (a screenplay of about 35 minutes)

Core value: home or stranded (D16 §8.1). Theme question: when you carry someone, do you carry them as goods or as a person? Core opposition: goods against persons, stated on the first prop, "Goods only. No persons." (B4 §3.1). Climax SC26..SC27, the one 10, played in counterpoint; SQ03, "the wrong world", is SC07..SC10 (K12, K13).

```
### PLANT PL-01
- what: a hard stop leaves nothing under the cage
- planted_at: SC01 "Stop it hard and there's nothing under it to catch us."
- paid_off_at: SC06 "Iona hits STOP with her elbow."
```

A FACT: the audience sees "He has one hand she cannot see." in SC06; Iona sees it only on the SC13 recording: `mode: dramatic_irony`; what the hand did is a separate FACT, a `mystery` (card 18; A4 WE2).

### The Long Places (prose, 14 chapters)

Step 2 writes fourteen digests, the strands and the events it cannot lose, then three plans for checkpoint P: a feature of 48 scenes, six episodes, or a short from chapters I and XIV (D2 §8). The deletion test keeps two CARDINAL records (events the story cannot lose): `CF-01`, item 51 and the brother line, and `CF-02`, the breathing shaft and the warmth at her right shoulder (D2 §8.1). Whose scene: close third person on Nilay (D2 §8.2; A3 §7.3). The book reveals late that the hand print is hers ("The print is mine.", line 1397), so item 51 is a plant typed at the same pace as item 50 (A3 Ex5, R22).

## Self-check

1. Does every scene have one past-tense event, a deed?
2. Is there one climax with the one scene intensity 10, and a separate crisis?
3. Is every scene in exactly one sequence?
4. Does every plant have a payoff, both as story points found once in their scene?
5. Does every peak away from the climax carry a reason?
6. Is length reported as a range, defaulting to "keep everything"?

## Words for AI models

The plan reaches prompts only through later records, so write it as things a camera shows: an event is a deed, "She deletes the way home."; a theme word ("goods", "persons") never enters a prompt, only the things that carry it (B4 §2.7; A3 P3). Fails: "symbolic", "the emotional climax", "tension builds" (A2 R25).

## Look up for more

`stage.py lib D16 §4` (roles, sequences, peaks), `D16 §8` (The Catch), `D2 §5`, `§6`, `§8`, `D13 §4.1`, `B3 §2.6`, `B4 §3.1`, `A4 §6.5`, `A2 Step 7`, `A3 §3.2`; the files are in `library/`.
