# 02 Cards - story and scenes

Part of the Stage chat kit (knowledge). It joins these craft cards, each whole: 01 Reading the whole story, 02 Adapting prose, 03 Scenes, values and beats, 04 Dialogue on screen, 05 Characters, 06 Voices and performance, 07 Places, things and motifs, 15 Action scenes, 16 Glass, mirrors and sides, 17 Screens, text and in-story cameras, 18 Suspense, reveals and the dark, 19 Inner life, montage and time, 20 Creatures, violence and filters. A step file names the card parts to read for each unit; read only those parts. 01 House rules says where every other skill file is in this kit.

---

From the skill file `cards/01 Reading the whole story.md`:

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
6. Where do the sequences break? Test the author's own breaks first, such as a cut to black followed by a title card (D16 R8); each sequence ends inside its act and answers one question with a quoted line (D16 R12).
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

---

From the skill file `cards/02 Adapting prose.md`:

# Card 02. Adapting prose

Read whole at step 2 for prose. Step 1 reads only "Intake" for a story that is not a screenplay; steps 7 and 8 read "Externalising inner life" for the tag `prose_interior`. "A3 R17" is rule 17 in A3 §9.

## The job

The Long Places chapter I holds ten candidate scenes; plan A keeps five (A3 Ex5; D2 §8.3). Prose tells what film must show, so every narrated sentence becomes something seen or heard, or is cut on purpose (A3 P9).

At step 2 you write a digest per chapter with its candidate scenes, the strands, the events the story cannot lose, the recurring devices, two or three plans for checkpoint P (the plan choice), and after it the step outline as SCENE records, each citing `from_lines` or marked `origin: invented` (D2 P3; A3 R24).

- A **candidate** is a passage that might become a scene; its kind is dramatized, narratized, inner, summary, iterative, letter or description (A2 Step 0; A3 §7.4).
- **Iterative** prose tells once what happened many times ("In the evenings she entered the 1924 survey"); **summary** compresses a stretch of time (A3 §1).
- A **cardinal event** is one the story cannot lose; a **strand** is a line of events following one person or question (D2 §1).
- A **step outline** is one line per planned scene, in screen order; a **composite** merges two scenes or characters into one (D2 §1).
- A **montage** is a run of short shots that compresses time; **voice-over** is a voice heard over the picture, not spoken in it (A2 §2).

## Intake

Example: The Long Places arrives as Markdown. Its fifteen lines starting "# " are a file title and fourteen chapters; its 69 lines starting ">" are quotations, not transitions; line 3's italic note ("revised by three Claude agents") is about the file, so it is **front matter**, excluded with a reason (D14 E2, R2-R3, R29).

Code reads the file; you read the odd-lines report (the lines code could not place) and confirm or correct it, because programs extract and the model classifies (D14 principle 3). Check, in order:
1. Kind from content, never from the file name: `## INT` at a line's start means The Catch's dialect even in a `.md` file; `# ` headings without scene headings are chapters (D14 principle 1, R1-R2). `PROJECT.source_kind` is screenplay, prose, `stage_play`, treatment, `comic_script`, `game_script` or mixed.
2. An **embedded document** is a set-off letter, list, report, message, sign or verse. Name its writer (or `unknown`) and whether it exists in the story; compare a repeat character by character, because one changed word is information (D14 R27-R28).
3. A play: acts and scenes become groups of scenes and candidates; soliloquies and asides are decided once for the whole play; a place moved off the play's set is `invented` (D14 §5, R13-R14).
4. A comic script: a panel is a shot candidate, a page turn hides a reveal, captions are decided once per work. A game script: the user picks one path (D14 §6, R15).
5. A **thin source** (a treatment, synopsis or logline) gives too little to extract scenes. List every stated fact; ask the user about gaps that change meaning, most important first; decide and label the gaps that only connect. Later steps write scenes as `origin: invented`, approved at checkpoint P or B (D14 §7, R17-R18).
6. Another language: analyse in the original where the model reads it well, write descriptions and prompts in English, keep dialogue in the original, set any translation beside it, and list honorific forms as aliases ("Kaya Bey") (D14 R21-R23, R26).
7. A scanned PDF with no text layer is refused with a one-step fix: open it in Google Docs and save it as text (D14 principle 8).
8. Without code: never count by eye; list each matching line with its number, so the list can be checked (D14 Recipe I1, R32).

## Questions in order

1. Have you read the whole book? Chapter I's hand print makes sense only from chapter XIV (A3 Ex5).
2. Per chapter, within `chapter_digest_words_max` words: what happens, who, where, when, which key lines? Quote the first and last line (D2 §5, §8).
3. What kind is each passage, and is a scene buried in summary? A sentence with a place, a time, two people and a change is a **buried scene** (A3 §7.4, R19).
4. What do A3's five tests say: a cardinal event; a value (a two-pole quality of a life) changes; it plants something; it can be shown by behaviour; a defining first appearance? Apply A3's rules in order: cardinal, kept; two tests, its own scene; one, folded into a neighbour as a shot, line or prop; none, cut (A3 §7.9).
5. Which strands feed which, and what does the deletion test say: if this went, what would lose its cause (D2 §5, R11)?
6. How long would it run filmed whole? Candidate scenes (two sample chapters averaged, times the chapter count) times 2 to 2.5 minutes a drama scene; code does the sums. Then two or three independent plans, each with what it keeps, cuts and loses (D2 R1, R3, R24, M3).
7. Which devices recur? List every occurrence, choose one policy for the whole work, and save the first occurrence's setup as a template (D2 R14-R16; A3 R23).
8. Whose scene: in close third person the camera stays with that person, and a shot outside her knowledge needs a reason (A3 §7.3).

## Externalising inner life

Example: "The warmth came against her right shoulder the way a cat commits itself" (line 79). The book already gives the behaviour, "She did not turn her head.": a locked-off frontal medium shot framed as a two-shot with one person missing, empty space at her right shoulder; her shoulder settles a fraction, "with weight" (B1 Ex7 hides that side instead, in profile from her left). No figure, no shadow. The closing thought, "It was homesickness, she decided", is cut; one look back into the dark on the climb replaces it, logged as `invented` (A3 Ex5).

**Externalising** turns what prose puts inside a character into something seen or heard. Try each rung in order and stop at the first that works; a rung works when a viewer who never read the book could say what she thinks from picture and sound, or keeps the book's own doubt (A3 §7.2, R17; A1 R32):
1. behaviour, often already in the prose;
2. an object she handles, keeps, avoids or reads;
3. juxtaposition: her face cut against what she thinks of, with a task, not a blank stare (A3 R5);
4. framing and light: isolation, empty space, a light that misses her;
5. a sound she attends to;
6. a line said to someone, under pressure;
7. voice-over, only when the words are the point, over pictures that do not repeat them;
8. text in picture: dates, places, documents;
9. cut it, and say so.

Record the thought she keeps back in BEAT `unsaid` (`CH-NILAY | thought: it is homesickness`) and the thing that shows it in `carrier`; an added carrier goes in the scene's `additions` (A3 R24; REASON-08). The book's best images belong in design and composition, not new lines (A1 R34).

## Translation menus with pitfalls

Pick one per passage; tie it to lines in the book (A3 §7.4-§7.8).
- Summary: a short scene standing for the stretch, a montage, one image, or nothing. Pitfall: a summary filmed as invented dialogue (A2 §10).
- Iterative: one instance, the one with a change or a plant, else the first; or a montage of three or four visibly different instances. Pitfall: identical repeats (A3 R18).
- Narratized telling ("he told it, flat"): the teller's face in one long take, not a flashback, unless the story turns on the old events (A2 R22).
- Reported speech: each report to a named speaker, the book's own words kept, new lines short and `invented` (A3 §7.6).
- A letter: dramatise what it reports with four to six of its lines over it; a voice-over frame; an insert of exact words; the writing or reading as a scene (A3 §7.7, R20).
- A time jump: a carrier from the story's world before any title card: a dated page, light, season, a new injury, a cold cup (A3 §7.8).

## Budgets and saved choices

- Digests within `chapter_digest_words_max`; outline units of `outline_chapters_per_unit` chapters; step targets within `step_outline_tolerance` of the runtime target (PLAN-04; D2 R9).
- A cardinal event is never cut (COVER-05; D2 P3); a kept scene never cites a cut strand (PLAN-05; D2 R11).
- First and last line quotes of at least `quote_anchor_words_min` words, found within their chapter (CITE-02).

## The baseline is a strong answer

Static, the owner's eye height, a normal lens, room sound (the place's steady background) are choices, not failures; depart only for a reason you can cite. In adaptation: behaviour before voice-over (A3 §7.2), the book's own words (A3 §7.6), one dramatised instance (A3 R18), no flashback by default (A2 R22).

## Cliché traps

- **Voice-over first.** Test: does the voice say what the picture shows? Fix: climb the ladder (A3 §12).
- **Scene explosion**: every candidate a scene, about 140 for The Long Places. Fix: budget first (D2 §11, R8).
- **Marks on an anonymous writer**: the keeper's hands given Melek's silver burn. Fix: unmarked hands (A3 R21).
- **A buried plant pushed in on.** Fix: item 51 gets the size and length of items 50 and 52 (A3 R22).
- **A refrain shot differently each time.** Fix: one saved setup (D2 §11; A3 R23).
- **A merge that puts effect before cause.** Fix: reject it or reorder with logged lines (D2 R13).

## Reasons that fail and reasons that pass

- Fails: five evenings of typing as a montage. Passes: one evening, items 47 to 53 at one pace, "Item fifty-one took her no longer than item fifty." (line 67; A3 R18, R22).
- Fails: voice-over "It was homesickness, she decided". Passes: the thought cut, a look back into the dark (A3 Ex5, §7.2).
- Fails: letters decided chapter by chapter. Passes: one RULE, `kind: device`, `policy: open_and_close` (D2 §8.2, R14).

## Two worked examples

### The Long Places, chapter I (plan A)

Ten candidates become five scenes (D2 §8.3; A3 Ex5): the letter, on hands only; arrival and her mother's house, a composite; Melek's "Why nine?", the clock saying folded in; the survey evening, the crossed-out forty-one as an insert; the threshold. The meeting and the team's arrival are cut.

```
- candidate: the survey evening | lines: 67-69 | kind: iterative | tests: 1 1 1 1 0 | decision: own_scene | becomes: SC04
- candidate: the threshold at night | lines: 73-81 | kind: dramatized | tests: 1 1 1 1 0 | decision: own_scene | becomes: SC05
```

Devices: the letters `open_and_close`; the threshold paragraph `template_refrain`, where only the minutes change (D2 §8.2).

### The Catch as a thin source

Had the user sent only a paragraph (D14 E3), its facts would never say who Jude is to Iona, nor when Iona learns Eli fired the device. Ask those; decide and label the factory's layout. The lesson: an invented cage scene can be vivid and still miss "Goods only. No persons.", which later scenes pay off, so labels must survive (D14 E3, R17-R19).

## Self-check

1. Is every chapter digested, with first and last lines found in it?
2. Does every candidate have a kind, five test scores and a decision?
3. Is every cardinal event in a kept scene?
4. Does every unsaid have a carrier from the lowest rung that works?
5. Is each recurring device one RULE with a policy?
6. Is every invention labelled `invented`?

## Words for AI models

Works: letters and documents as text graphics, exact words, never drawn by the model (A3 R11); prompts in English, names spelled as the book spells them ("Kırk Oda") (D14 R10, R21). Fails: "she remembers", "she thinks of her brother" (A3 P3; A2 R25).

## Look up for more

`stage.py lib A3 §7` and `A3 Ex5`: `library/A3 Script breakdown, directing and adaptation.md`. `D2 §4`, `§8`: `library/D2 Adapting a whole work.md`. `D14 §2`, `§5` to `§9`: `library/D14 Reading any story format.md`. `A1 R32` to `R34`.

---

From the skill file `cards/03 Scenes, values and beats.md`:

# Card 03. Scenes, values and beats

Read whole at step 7 for every scene. "A2 R4" is rule 4 in A2 §7; A2's "sc10, B7" is `SC10-B07` here.

## The job

In The Catch scene 10 the core value is Iona's belief about her own body: `+` at "Kitchen.", `---` after "Nothing has happened to the mint." It swings at `SC10-B07`, where "Chew that." meets "Her face changes." Everything the camera does later in the scene is spent on that beat.

A scene exists to change at least one value (A2 P4, P8). Hand on to the shot list (card 14) the turn beats, the nonverbal beats a line-by-line list drops, and every beat's intensity. Fields: SCENE `value`, `want`, `driver`, `conflict`, `third_thing`, `flags`; PART; BEAT `action`, `reaction`, `task`, `beat_intensity`, `turn`, `charge`, `five_steps`.

- A **value** is a quality of a character's life with two poles, such as trust or distrust (A2 §2).
- A **charge** is where a value sits at one moment, `---` to `+++`; A2's mixed "+/−" is written `0`.
- A **beat** is one action plus the reaction it provokes; "(beat)" in a script is a pause (A2 §2, Step 0).
- A **tactic** is what a line or act does to the other person, an -ing word such as `proving` (A2 P9).
- A **turn** is the beat where a value swings to the charge it keeps to the scene's end (A2 Step 7).
- A **part** is a stretch of a scene with its own turn; the **driver** is the character whose want sets the scene moving (A2 §2).
- The **third thing** is what two people talk through so they need not talk about themselves (A2 P13).
- The **five steps** are desire, obstacle, choice, action and expression: one decision slowed down (A2 P10).

## Questions in order

1. What does the audience already know, and what changed since these people last met (A2 Step 1)?
2. What is the **event**, the one change the scene exists to deliver, in the plan's past-tense sentence? If no beat changes anything, flag `nonevent`; never invent one (A3 P1, A3 R1).
3. Which one to three values are at stake, named in a life ("trust or distrust, Iona toward Eli"), not as topics ("the flask")? Mark one `core: yes`; score `open` and `close` from the character's side (A2 Step 2).
4. What does each character want now, from this person? Test: if the other side gave in, would the scene end? If not, the want is wrong (A2 Step 3; A3 §3.2). Wants that never cross: flag `splintered`.
5. Who drives, and which conflict type below holds (A2 §4)?
6. Where are the beats? Pair each speech or described act with its reaction; merge beats only when a tactic repeats without topping the last, since escalation is not repetition (A2 Step 5, P9). A move or look that provokes a response is a beat (A2 R3).
7. What does each beat do? An action tactic acts on someone (`accusing`, `testing`); a reaction may be inward (`absorbing`) but playable. The hands go in `task` (A2 Step 5; A3 §3.2).
8. Where does each value turn? Run the sign test (A2 Step 7).
9. Does each new part start after a drop in pressure or without one (A2 Step 7, R10)?
10. How intense is each beat? Use the list below (A2 Step 6).
11. At each turn and each beat of intensity 4 or 5, what are the five steps, each a visible moment (A2 Step 8)?

**The sign test** (A2 Step 7; CRAFT-18). If a value's sign changes between `open` and `close`, it turns at the first beat after which its charge sits on the closing side for good. If only the strength changes, it turns at the first beat that reaches `close` and stays. If `open` equals `close`, `kind: none`. Every beat whose `turn` is not `none` must pass this test; the core value's turn is `main_turn`.

**Beat intensity** (A2 Step 6; range in `scales`). Take the first level, from 5 down, that fits. **5:** a value turn. **4:** an open accusation; a forbidding, threat or ultimatum; a confession; a disclosure that damages someone present; a move that blocks, threatens or shields. **3:** a direct challenge or unwanted question; a demonstration or test; an open refusal; a slip caught. **2:** probing, hinting, noticing; a planned breather; beats after the main turn. **1:** logistics, nothing at risk. Score inside the scene, not against the film.

## Translation menus with pitfalls

Pick at most one option per row; tie it to a line, object or action in this story.

| The scene holds | Options | Pitfall |
|---|---|---|
| A new tactic | a new setup, size, camera move or actor's move (A2 R1) | a new picture inside a held tactic fakes progress (A2 R2) |
| A revelation turn | an insert of the evidence, then the receiver's face held (A2 R8) | cutting away from the reactor |
| An action turn | the whole act and its result in one frame (A2 R9) | a cut inside the act hides the change |
| A new part after a drop | a wide from a new angle (A2 R10) | widening with no drop releases the pressure |
| Power changes hands | the camera takes the new driver's side or height, crossing on screen (A2 R11) | a bare cut across the line |
| Waiting as a tactic | hold on the one waited on; the silence's length is the action (A2 R18, P11) | inserts that break the wait |
| A third thing | inserts of it; eyelines leaving it mark escalation (A2 R19) | losing it at the turn |
| Several react at once | one frame holding all (A2 R7) | singles cannot show "at the same moment" |
| Action, reaction, reaction | trust rising: one two-shot holds both; trust breaking: singles (A2 R6) | a cut splitting what the beat joins |
| A witness or sleeper restrains someone | the restraint in frame at peak pressure (A2 R21) | no visible reason she does not explode |

By conflict type (A2 R12-R17): balanced, matched sizes tightening in step; asymmetric, the attacker moves, the resister stays in a task until her turning line; indirect, group frames keeping the witnesses; comic, wide frames, a hold after the punch line; minimal, long takes, every pause kept; reflexive, reflections and a setting drawn as she feels it (card 19).

## Budgets and saved choices

- At most `beat_intensity_5_per_part_max` beats of intensity 5 in a part (CRAFT-05); keep 5 for the main turn and the turn nearest it, score other turns 4 (A2 Step 6).
- A turn owes at least `turn_reaction_min_s` of held reaction (A2 Step 9; TIME-05); leave room for it in the list item.
- The scene's tightest size, its one push-in (`push_in_per_scene_max`) and its one extreme close-up (`extreme_close_up_per_scene_max`) belong to the main turn: caps, never quotas (A2 R4; CRAFT-01 to CRAFT-03).
- Beat IDs come from `issued_blocks`; a scene over `scene_split_beats` beats or `scene_split_non_blank_lines` non-blank lines is designed in two units by part. Every line sits in a beat (COVER-01).

## The baseline is a strong answer

Static, the owner's eye height, a normal lens, **room sound** (the place's steady background) are choices, not failures; depart only for a reason you can cite. A held tactic holds one setup (A2 R2); routine beats keep all five steps inside one shot at normal speed (A2 P10); one value with one turn is a complete scene.

## Cliché traps

Each with its test and fix (A2 §10).
- **One beat per line.** Test: the beat count nears the line count. Fix: merge repeats that do not top each other (A2 P9).
- **The loudest moment called the turn.** Test: the sign test lands elsewhere, often quietly ("I wasn't asking her."). Fix: move `turn` (A2 §10).
- **Activity verbs** (`talking`, `asking`, `explaining`, `looking`). Test: can it be done to the other person? Fix: `probing`, `cornering`, `justifying`, `outwaiting` (A2 Step 5).
- **Emotions as beats** ("shocked"). Fix: the action that causes the feeling and the behaviour that shows it (A2 §10; A3 R2).
- **Values as topics; the want as the life want** ("to save her family"). Fix: two poles in a life; what she wants now, from this person (A2 §10).
- **Rewriting a flat scene.** Fix: flag `nonevent`, `turn_too_soon`, `turn_too_late` or `splintered`; never invent an event (A2 Step 7).
- **The any-film test**: "love or loss" fits any film (A2 Step 2).

## Reasons that fail and reasons that pass

- Fails `SC10-V1 | name: family`. Passes `SC10-V1 | name: normal or altered, Iona's belief about her own body | core: yes | open: + | close: --- | turns_at: SC10-B07 | kind: revelation` (A2 §11).
- Fails `main_turn` on `SC10-B04` "because it is the biggest argument". Passes: after B04 the core value sits at `0` ("It's my right."); it first reaches the negative side at B07, "Her face changes.", and stays, so the sign test puts the main turn there (A2 §11).
- Fails `SC10-B06` scored 5 "because it is tense". Passes 4: "Don't open the flask." is a forbidding and no value turns on it (A2 Step 6).

## Two worked examples

### The Catch, scene 10 (asymmetric)

Values (A2 §11): `SC10-V1` normal or altered, core, `+` to `---`, turns at B07, revelation; `SC10-V2` free or contained, `+` to `--`, turns at B11, action; `SC10-V3` trust or distrust, Iona toward Eli, `+` to `+`, `kind: none`. Saye drives with tests; Iona resists; Eli's knowledge leaks through a task ("He stops. Twists it the other way.").

Beats (action / reaction, intensity): B01 appealing / admitting on her terms, 2; B02 probing / joking, 2; B03 verifying / normalizing, 3; B04 demonstrating / refusing, 3; B05 compensating / clocking him, 3; B06 testing / forbidding / conceding, 4; B07 proving / discovering, 5; B08 naming the truth / absorbing, 4; B09 reporting / challenging, 3; B10 shielding / redirecting, 4; B11 outwaiting / yielding, 5. `SC10-P2` covers B09 to B11 and `starts: after_drop`: Iona absorbs B08 in silence.

```
### BEAT SC10-B07
- lines: 449-463
- action: CH-SAYE | tactic: proving
- reaction: CH-IONA | tactic: discovering
- task: CH-IONA | does: chews the leaf, stops, chews once more
- beat_intensity: 5
- turn: main_turn
- turn_kind: revelation
- charge: SC10-V1 | charge: --
- five_steps: desire | shows: her eyes on Saye, still defiant
- five_steps: obstacle | shows: the leaf held out into her frame
- five_steps: choice | shows: a half-second before her hand moves
- five_steps: action | shows: she chews, in one unbroken frame
- five_steps: expression | shows: "Not mint." after her face has told us
```

### The Long Places, chapter III (quiet prose)

"I am equipment," Márton said, "not content" (line 247). Value: concealed or disclosed, Márton's old wound, `-` to `++` (A2 §14). Night brings the action turn: "he told it, flat, in the voice he used for instrument logs" (line 249); "It was measured" (line 255) strengthens it without changing its sign. The value's visible form is the camera: in the evening it sits between the men, light on; at night the same table, framed the same way, has none, and that absence is the turn picture (A2 §14, R20).

## Self-check

Yes or no; a "no" needs a fix (A2 §9).
1. Does every value have two poles in a life, and does one close at a new charge?
2. Does every turn pass the sign test, with one `main_turn` on the core value?
3. Does each want pass "if granted, the scene would end"?
4. Is every tactic a playable -ing word, none of talking, asking, saying or looking?
5. Are nonverbal beats in, and every "(beat)" a pause?
6. Is every beat intensity from the list, within `beat_intensity_5_per_part_max` fives a part?
7. Are the five steps written for every turn and every beat of intensity 4 or 5?
8. Is every line and speech of the scene in a beat, and every timing fault flagged, not fixed?

## Words for AI models

Works: behaviour from the tactic, "she stops chewing, frowns, chews once more, slowly"; the wrong-tasting mint means recognition and confusion, never disgust (A2 R25, §11). Split a long take only at a beat boundary with matched framing (A2 R24), and write each single's eyeline into its prompt (A2 R26). Fails: a named emotion ("disgusted", "betrayed") gets a stock face (A2 R25).

## Look up for more

`stage.py lib A2 §6` (the method), `A2 §7` (rules), `A2 §11`, `§12`, `§14` (worked scenes): `library/A2 Scene design, values and beats.md`. `A3 §3.2` (the director's pass): `library/A3 Script breakdown, directing and adaptation.md`.

---

From the skill file `cards/04 Dialogue on screen.md`:

# Card 04. Dialogue on screen

Steps 7 and 8 read only "Landing face", "Flaws" and "Pauses"; chat apps read it whole. "A1 R19" is rule 19 in A1 §6.

## The job

In The Catch scene 13, "One body." / "One." / "You." plays on Iona with Eli heard off screen: the fact is fired at her, so the change happens in her face (A1 Ex3). Every line is something the speaker does to someone; film that action and where it lands, not the words (A1 §1, P1).

The dialogue pass covers turn beats, flagged lines, revealed facts and refusals at standard, every line at detailed. It writes BEAT `landing_face`, `unsaid`, `carrier`, `pause_after`, `flag` (detailed adds `core_word`, `cut_rule`); at step 8 each SHOT `hear` item says whether its speaker is seen.

- The **unsaid** is what a character could say and chooses not to; a **carrier** is the object, hand, distance or sound that makes it seen or heard (A1 §2, P3).
- The **core word** carries a line's meaning (A1 §3.5); a **split edit** changes sound and picture at different moments (A1 §2).
- **Room sound** is a place's steady background; a **third thing** is what two people talk through instead of themselves (A1 §2).
- A **beat** is an action and its reaction; its **tactic** is the -ing word for what it does; a **turn** is where a **value**, a two-pole quality of a life, changes for good (A2 §2).

## Questions in order

1. For each line in scope: its tactic, unsaid and core word (A1 §7)?
2. Is each fact fired, planted, forced, or shown by an object (A1 R19-R22)?
3. Which conflict levels are in play, physical, social, personal, private (A1 P7)?
4. Which line turns the scene; where are the pauses around it (A1 R13-R15)?
5. Who is frame-left and frame-right; where does each look (A1 R39-R43)?
6. Whose face does each key line land on (A1 R1-R7)?
7. What do the hands do or keep still, and how does it change at the turn (A1 P4, R8-R10)?
8. Which cut rule for each key line; what is heard in each silence (A1 R17, R27-R29)?

## Landing face

Example: in scene 10, "Don't open the flask." is Eli forbidding Saye. It lands on Saye, whose answer is "Saye sets her scissors down.", so Eli is heard off screen (A1 R1; K05: `CR-ELI`, Eli's camera rule, keeps his close singles for scene 13).

The **landing face** is the face on screen when a line's core word lands, the biggest camera choice in a dialogue scene (A1 §2, P2). Write a character ID; `insert:` joined to a prop or text ID (`insert:PR-FLASK`) when the line lands through an object; or `wide`. Highest rule first:
- The script's directions about what we see are binding: "Looks at her brother. Not at Jude." (A1 §6, precedence).
- A line aimed at someone lands on the receiver; the speaker is partly or wholly off screen (A1 R1).
- A line that costs the speaker (a confession, the dangerous question) holds on the speaker through it and the silence after (A1 R2). When both apply: the speaker through the line, the receiver from the core word on (A1 §6 tie-break).
- A **fired fact**, a fact used as a weapon, lands on its target; the shooter gets one short reaction after (A1 R19, P6).
- To share someone's not-knowing, stay on that face while the other keeps the secret (A1 R3).
- A silent third character gets at least one reaction at the turn (A1 R5; CRAFT-24).
- Two equals in a small beat stay in one two-shot; when the relationship breaks, go to singles on the turning line, not before (A1 R6-R7).
- A **volley**, three or more quick short lines, keeps one angle; only the line that carries the change gets a new, closer shot (A1 R29).

At least once in every dialogue scene the landing face is not the speaker (A1 §8 check 5, R1; CRAFT-23). Every unsaid needs a carrier in a shot of its beat (A1 P3; REASON-08): "She is hurt" is not a shot; "Her thumb stops turning the ring" is.

## Flaws

Example: "Eli. Are we going to be all right?" is direct, yet takes no flag: Iona chooses directness; her tactic is `demanding` (A1 Ex2).

A flaw is a fault in one written line. Flag it on its BEAT, `flag: <flaw> | line: <speech ID>`, and design the shots around it; never change a word, since rewording makes lines more on the nose (A1 R38).
- `on_the_nose`: the line says exactly what the character feels. Give the actor a hidden action under it; add no emphasis (A1 R35).
- `melodrama`: big words, small stakes. A static camera one size wider than the scene's other beats, no score (A1 R36; CRAFT-21).
- `forced_exposition`: people telling each other what both know. Play it off screen over a busier picture, or move the fact to an insert or a document (A1 R22).
- `monologue`: a long speech with no reaction (A1 counts a line over 40 words as long). Mark each change of tactic as a beat and choose speaker or listener beat by beat, or keep the listener in frame (A1 R31, §5; CRAFT-22).
- `repetitious`: the same action and reaction in new words. Vary each beat's size, height or distance (A1 §3.7, P9).
- `can_play_silent`: a nod or a glance could carry it. Flag it for the director and keep the words (A1 R18).
- `interrupted`: a line cut off with a dash ("In the car-"). Stay on that face through the cut-off, or cut to it just after (A1 R30a).

A scene with no turn takes the SCENE flag `nonevent`; busy coverage must not hide it (A1 R37). Flaw handling outranks the turn rules (A1 §6 precedence).

## Pauses

Example: scene 13's "She waits." is the pause before the fired fact: long, held on Eli past comfort, room sound and the monitor's hum. "Silence." after "You." is the pause after it: cut wide once, then hold (A1 Ex3; D3 §11.2).

A written pause becomes a hold, a cut or a push-in, and always a sound (A1 P5). Its tier comes from `pause_tiers`: short, medium, long, or `hold` beyond long, which needs a saved choice, a RESERVE record (K10; TIME-08); script words map through `pause_tiers.script_words`. Write `pause_after: long | seconds: 3 | picture: hold | sound: room sound and the monitor's hum`.
- Before a turn: `picture: hold` if the character in frame waits or is outwaited, `picture: push_in` if deciding, using the scene's one push-in (`push_in_per_scene_max`; A1 R13, P5).
- After a turn: `picture: hold` on the receiver, or `picture: cut_wide` to show the new distance (A1 R14), for at least `turn_reaction_min_s` (TIME-05).
- A refusal to answer is a line: give the silence a shot, a length and a tactic, `refusing` (A1 R16).
- Rank the marked pauses, nearest the turn first, then by how much each changes what the audience knows; only the top `long_pauses_per_scene_max` are long, the rest short, medium or cuts (A1 R15; TIME-04).
- Every pause has a sound: room sound and one small real sound, never dead air, and no music that states the subtext (A1 R17, §8).

## Translation menus with pitfalls

Pick at most one per line; tie it to a line, object or action in this story.
- Subtext differs from the words: land on the receiver, held past the line; the speaker's task betrays the action. Pitfall: music under it (A1 §5).
- A fact planted for later: one calm, readable shot, no push-in, no music (A1 R20). A fact that can be shown: the object in frame, the line confirming it (A1 R21).
- Line design: core word last, `cut_on_core_word`; core word first, `cut_early_split`; a volley, `hold` or `no_cut_two_shot` (A1 R27-R29).
- Conflict levels: physical, the hazard wide; social, glass or desks between people; personal, two-shots and distance; private, close frames (A1 R23-R26).
- The turning line changes the shot grammar: a new angle or size, the camera stopping or starting (A1 R30). Pitfall: showing what a figure of speech compares (A1 §5).

## Budgets and saved choices

- `pause_tiers`; at most `long_pauses_per_scene_max` long pauses a scene; a `hold` needs a saved choice (K10; A1 R15). One push-in a scene (`push_in_per_scene_max`; A1 P5).
- Pace `speech_wps_default` unless a voice's `pace_wps` differs; one clip holds speech by `clip_speech_rule` (K08).
- At most `on_screen_speakers_per_clip_max` on-screen speaker a clip (GEN-13; C3 §20 item 2); delivery notes within `voice_delivery_words_max` (D3 §5.2).

## The baseline is a strong answer

Static, the owner's eye height, a normal lens, room sound are choices, not failures; depart only for a reason you can cite. A small beat between equals stays in one two-shot (A1 R6); paired singles share size, lens and height (A1 R40); a single looks just past the lens, never into it (A1 R44).

## Cliché traps

- **Following the speaker.** Test: does the landing face ever leave the speaker? Fix: a landing face per key line (A1 R1).
- **Illustrating the words.** Test: a cut to every object a line names. Fix: insert an object only when it changes hands or state (A1 R11).
- **Emotion labels or the unsaid spoken aloud.** Fix: a tactic and a behaviour, `evading`, looks at the flask, not at her; name a carrier (A1 §9, P3).
- **Scoring the subtext.** Test: the sound-off test, does the frame tell the beat without music? Fix: room sound or one real sound (A1 §9).
- **Every beat a hold; flat framing; ping-pong.** Fix: rank pauses (A1 R15); tighten toward the turn (A1 P9); a two-shot (A1 R29).

## Reasons that fail and reasons that pass

- Fails `landing_face: CH-ELI` "because he is speaking". Passes `landing_face: CH-IONA`: "One body." / "You." is a fact fired at her, so her face carries the change (A1 R19; K05).
- Fails every marked pause in scene 13 made long. Passes long only for "She waits." and "Silence.", nearest the turn; the three "(beat)" marks stay medium (A1 R15; `pause_tiers.script_words`).
- Fails music under "I wasn't asking her.". Passes room sound only, Iona held at least `turn_reaction_min_s` before any cut (A1 R14, §8).

## Two worked examples

### The Catch, scene 13 (balanced, few words)

`SC13-D17` "What was it rated for?" to `D20` "You.": `landing_face: CH-IONA`; Eli is off screen, and "You." is marked by a cut in on her face, not a cut to him (A1 R19, R30; K05). Unsaid `CH-ELI | thought: the device was bought to save her alone`; carrier: his eyes stay on the monitor until "Now he looks at her." (line 811). "She waits." and "Silence." are the long pauses (A1 R15). The one push-in runs on Iona from "I asked you in the car." to `extreme_close_up` on "I wasn't asking her." (K05).

### The Long Places, chapter IV (an understated reveal)

Halden: "Before your birth. And once since." (line 328). The narration's unsaids ("had already said when") do not exist on screen (A1 R32, Ex5). The open volume lies between them as the third thing, the margin "4–5.ix. Kept the hours. A.H." readable in an insert; "And once since." lands on Nilay looking down at the page (A1 R11, R19). Nilay's carrier: she puts the leaves back in their sleeve; cut away before she speaks, so the cut is her silence (A1 R16).

## Self-check

Yes or no (A1 §8).
1. Does every key line (a turn, a fact, a refusal, an interruption) have a landing face, and does one leave the speaker?
2. Does every unsaid have a carrier seen or heard?
3. Are pauses ranked, each with a sound, within `long_pauses_per_scene_max` long ones?
4. Are flaws flagged, every word unchanged?

## Words for AI models

Works: each quote with its speaker named in the same sentence; a reaction clip that says "she listens; no dialogue"; the silence written in, sound and length; frame side, eyeline and "does not look into the camera" (A1 §11). Delivery words from the tactic: to press, "level, quiet, unhurried" (D3 §5.2). Fails: "he is secretly guilty"; unattributed quotes with two people in frame (D3 §5.2).

## Look up for more

`stage.py lib A1 §6` (rules, tie-breaks), `A1 §7`, `A1 §10`: `library/A1 Dialogue as action and subtext.md`. `D3 §5`, `§11`: `library/D3 Voices and dialogue audio.md`. `A2 §12` (scene 13).

---

From the skill file `cards/05 Characters.md`:

# Card 05. Characters

Read whole at step 4. Step 5 reads only the part "State lines". "B5 R21" names rule 21 in B5's numbered rules (§9); "M" numbers are B5's mistakes (§13).

## The job

Design every person the film shows more than once so that a video model can rebuild them from words and every visible choice serves role, arc and theme (B5 §0.1). Work from evidence outward; write the fixed description (the words pasted unchanged into every prompt that shows them) last. Step 4 hands on CHARACTER records whose fixed descriptions fit `fixed_description_words`, whose principals (`tier: principal`, the main parts) differ by lineup, whose sided features have own sides and whose unstated skin tone and ethnicity stay open. Step 5 hands on STATE records, each with the line that causes it.

## Questions in order

1. **What does the story say?** Quote every line about face, body, clothes, marks and gestures into `evidence`; mark the rest `inferred` or `invented`, with a reason. Never "improve" a stated feature; keep inventions ordinary (B5 R23).
2. **What is the design thesis?** One sentence: must read as a first impression, and carry a contradiction the story later confirms or overturns, because of the arc (B5 §2.6, P2): Saye's grey control and her pot of mint.
3. **Does the lineup separate them?** The lineup is six word columns (height, mass, shape, value (how light or dark the whole figure reads), colour, tempo); principals differ in at least `lineup_columns_differ_min` columns (B5 R3, CRAFT-20), by height or mass first (B5 §2.2).
4. **What are the face's three largest distinguishers?** Large features survive a model's drift toward an average face: hair, facial hair, age lines, brows. A chipped tooth goes to reference pictures and inserts (B5 R21, R24).
5. **How do they move?** Write `movement` for home (the default way of moving), stress (under pressure) and break (when defences fail), each as body part, direction, speed and what stays still (B5 §5.7, M14).
6. **What are the psychological gesture and the one signature gesture?** The psychological gesture is one verb phrase for the inner pressure (Saye: a flat hand raised between two people); everyday gestures are small versions of it (B5 §5.2, §10.4). Quote the signature's line. Each return keeps the hand shape and framing and changes one thing (B5 R17). Minor characters get none (B5 §5.6).
7. **What status and distance?** Status (`status_play`) is how a person raises or lowers themselves against another, played, not held (B5 §5.3). High by stillness breaks once, leaning toward something (B5 R15). Distance: default and closest in metres, with the scenes that change them (B5 §5.5).
8. **What do they wear?** Answer B4's five questions first, in nouns and materials: choice, means and job, history, what the story did to it, what an institution put on them. Name the wear; change costume only at a turning point or a forced circumstance; keep one chosen thing through imposed clothes (B4 §6.1, R19; B5 R7).
9. **Not human?** Fear from silhouette, sound first and wrong proportions in a human plan; pity from damage suffered and care shown; every clue strange, never hidden; with no face, its thinking goes to head direction, hands and the order of its looks (B5 §6.2-§6.4, R10-R12).
10. **What stays open?** Skin tone and ethnicity the story does not state, with a marked placeholder and a small choice (B5 R19). Apparent sex and age band are always fixed (B5 §7.2 rule 7).

## State lines

A **state** is a person's or thing's costume, injury and condition from one change to the next (`CH-IONA.S03`); its **state line** is the phrase pasted after the fixed description in every prompt that shows that state (B5 §7.2 rule 4; K26).

1. **Start a state where the story changes it,** and quote the line in `cause`. The nurse dresses Iona's palm at line 498 ("dressing Iona's palm"), so the dressed state starts at that line, not at the top of SC11. An unexplained difference gets `origin: inferred` with the gap named, or a CHOICE (B4 §5.3; STATE-02).
2. **Copy the exit state into a `CONTINUOUS` scene exactly;** only a line inside the scene may change it (A3 R8; STATE-03).
3. **Write what is there,** in visible nouns and materials: "right palm bandaged in white gauze", not "hurt hand", never "no ring" (B5 §7.2 rule 8). No expression words.
4. **Rings, wounds and anything that changes live in state lines,** never in fixed descriptions (K26).
5. **Never store image sides.** Write own sides ("her own left hand"); code derives frame-left and frame-right per shot (blueprint 5.4 rule 8; SIDE-02).
6. **Give every sided feature a `side` item** with `own` (the side on the body itself) and `plot` (`yes` when the story depends on which side) (SIDE-01). Where the story leaves repeated damage unsided, put it all on one side and keep the other clean for a ring, as a small choice (B4 R14, B5 R8).
7. **In a mirror story, set `handedness` (`original`, or `reversed` once the element has turned) on every state.** A side the story states for an element shown mirrored is apparent: record the opposite own side, `origin: inferred`. "Saye's wedding ring. On her right hand." (line 436, era b, when the world is mirrored) is her own left (K03; SIDE-04). Card 16 holds the mirror method.
8. **Order wounds in story time:** fresh, reopened, dressed, bandaged; each state needs its own reference pictures (`pictures_needed`), because a model keeps a state only when every prompt restates it (B4 §6.1; B5 §7.3, §14).

```
### STATE CH-IONA.S03 Palm reopened
- element: CH-IONA
- from: SC09 | line: 370
- cause: 370 | quote: "her skinned palm opens"
- state_line: right shirt sleeve torn away, right palm raw and bleeding, dried blood on both hands, plain gold ring on her left hand
- side: palm | own: right | plot: yes
- side: ring | own: left | plot: yes
- handedness: original
- origin: story
> Own right for the palm is K26's default: the story does not say which hand.
```

## Translation menus with pitfalls

Pick at most one option per character from a row, tied to a line, object or action in this story; one column carries the meaning, the rest stay ordinary (B5 §8).

| Story meaning | Options | Pitfall |
|---|---|---|
| Competence | hands arrive before the eyes; worn, fitted work clothes | the heroic pose, chin up, shot from below (B5 M15) |
| Hidden knowledge | eyes go to text first; one hand out of sight (B5 R5) | the shifty-eyed villain |
| Control over grief | a still face; everything fastened; the break is one lean | all four at once: a poster (B5 §8 rule 1) |
| Cost paid | one mark that stays; guarding the hurt side | suffering make-up on every face (B5 M16) |
| Taken over by an institution | wristband, printed name, oversuit; one chosen thing kept | a symbol with no practical reason (B5 R25) |

## Budgets and saved choices

- `fixed_description_words`, principal and minor ranges (WORDS-05).
- Lineup: principals differ in at least `lineup_columns_differ_min` columns (CRAFT-20).
- One signature gesture per principal, at most once per scene outside a payoff scene (B5 §5.6, M6).
- One colour identity per principal, on one garment, not repeated at that saturation in the scene (B5 §4.2).
- Expression range, Detailed depth only: named faces tied to beats, written as muscle, eyes and head (B5 §3.3).

## The baseline is a strong answer

An ordinary body, clothes worn by this person's own life, and a still face while the line or the cut carries the beat are choices, not failures. A minor character needs one read and one key prop (B5 R20). Depart only for a reason you can cite (B5 R23).

## Cliché traps

Tests: the **any-film test** (would it fit any film with this theme?), the **mood-word test** (does the reason name only a feeling?), the **stacking test** (more than one signal saying one thing?), the **sound-off test** (does the body tell the beat with the sound off?).

- Adjective design ("mysterious, tough") fails the mood-word test. Fix: distinguishers and `movement` items (B5 M1).
- A lab coat for a scientist fails the any-film test. Fix: the five costume questions (B5 M2).
- Villain coding by scars, skin tone or body size: remove the moral role; does the design still stand? (B5 M3).
- Glowing eyes or chrome on a creature: remove what a famous robot would have (B5 R26).
- An expression in the fixed description ("composed") fights every other beat (B5 M18).

## Reasons that fail and reasons that pass

- Fails: "Saye is cold and controlled." Passes: "Saye's head stays still while her hands work quick and flat (line 408); her one break is a lean toward the screen (line 983) (B5 R15)."
- Fails: "Give Eli a scar to show his guilt." Passes: "Eli's half-smile lifts on his own left, a small choice, so 'on the wrong side of his face' (line 1696) pays off line 137 (B5 R2)."

## Two worked examples

### The Catch: CH-SAYE at step 4

Evidence: "DR SAYE, fifties, grey and tidy, fully dressed at four in the morning" (line 399); "quick flat hands" (line 408). Thesis: upright and fully fastened, dressed and waiting for years, her one living thing a pot of mint (B5 §10.4). Lineup: `height: average | mass: slight | shape: long | value: light | colour: grey | tempo: fast`. Nell shares her mass, shape and value; tempo written fast, from the quick hands, keeps them apart in height, colour and tempo, exactly `lineup_columns_differ_min` (B5 §10.11). Gesture: "She waits until Iona steps aside. | line: 481". `status_play`: `default: high | flips: SC17 "Leans in until her face is almost on the screen."`. Fixed description, no expression, her age in the story's word (B5 §7.2 rule 2; K26): "Dr Saye, a slim, upright woman in her fifties, short neat grey hair, a long pale lined face, thin straight brows, level grey eyes, a light grey cardigan buttoned to the collar over a white blouse." Her ring goes to the state line (K26).

### The Long Places: Melek, a prose portrait

"Seventy-eight, built like a doorpost ... knuckles like burl, a burn gone silver across the back of the right one" (line 47). A model draws a metaphor literally (a doorpost returns as wood), so turn each into shape, proportion and posture and keep the metaphor in the thesis (B5 R18, Ex5). The doorpost becomes tall, straight-backed, square-shouldered; the burl becomes large knotted knuckles. The burn is an own-right mark: a `side` item and a state line (K26). Gesture: "knocked twice, softly" on the sounding stone (line 419). Skin and hair colour stay placeholders (B5 R19).

## Self-check

- Is every descriptive line quoted in `evidence`, and every other choice marked `inferred` or `invented`?
- Do principals differ in at least `lineup_columns_differ_min` columns, with three distinguishers large enough to survive drift?
- Does every `movement` item name a part, a direction, a speed and what stays still, and the gesture its line?
- Is the fixed description within `fixed_description_words`, visible nouns only, with no expression, no real person, no ring and no wound?
- Does every sided feature have an own side, and every state a cause line?
- Are unstated skin tone and ethnicity open, and apparent sex and age band fixed?

## Words for AI models

Works (B5 §14): age in decades ("in her fifties"), build words, hair, facial hair, named garments with colour and condition ("faded blue work shirt, sleeves rolled to the elbow"), materials. Paste the fixed description unchanged, then the state line; a synonym is drift (B5 §7.2 rule 3; C3 §11). Say what is there: "a low domed head sunk deep between high shoulders", not "no neck".

Fails: left and right on bodies (fix the side in an edited still); words on clothes (card 17); "faceless"; theory words; famous names. High status becomes "stands still, head level, looks straight at her"; a half-smile becomes "only one corner of his mouth lifts", then check the side.

## Look up for more

B5 §3.2 (the face), §5 (how people move, status, distance), §6 (non-human characters), §7.2 (fixed description rules), §9 (R1-R26), §10 (The Catch's cast), §11, §13, §14; B4 §6 (costume); K03 and K26 in `library/00 Resolved conflicts.md`. Print one rule with `stage.py lib B5 R21`.

---

From the skill file `cards/06 Voices and performance.md`:

# Card 06. Voices and performance

Step 4 reads only "Voices"; steps 7 (Detailed) and 8 read only "Display and stillness"; add-on C reads only "Lip sync and voice takes". "D3 R13" names rule 13 in D3's numbered rules (§3); D15 and A1 rules are cited the same way.

## The job

Give every speaking character one voice that can be made the same way every time, and every acting body a performance a model can follow: what it does to the other person, what we see, how much shows, what stays still, where the eyes go (D3 §1; D15 §1). Step 4 hands on VOICE records. Steps 7 and 8 hand on `tactic`, `does`, `display`, `still`, `eyeline`, `dwell_s` and `must_not` on every subject. Add-on C hands on voice takes and a lip-sync route for every shot with a speaking mouth.

## Questions in order

1. Does the character speak in more than one scene? Then one VOICE record, locked before any picture shows their speaking mouth (D3 R1; K16).
2. What does the line do to the other person? Write the tactic as an -ing word and `does` as visible steps, never the feeling (D15 R1; A3 R2; WORDS-01).
3. Who carries the line? Where the listener's face can, the speaker is heard off screen (A1 R1; D3 R20).
4. What do the hands do? Frame a named task with the face; a task that stops is a reaction shot; where the script gives none in a talk scene, propose one marked `invented` (A1 R8-R10).
5. Is this look spent later? Then it goes in `must_not` on every earlier shot (D15 R9).
6. Does the shot continue the last one? Its subject starts where the last one ended (D15 R11).

## Voices

A VOICE record holds the fixed words for a voice (`voice_description`, `voice_description_words` long, frozen word order), its pitch band, pace, accent and path treatments (D3 §4.1).

1. **Build the voice from the character:** the age it reads as, pitch band, timbre in a few words, accent from `WORLD.accents`, pace, and status in the voice: high status is level, with falling ends and no fillers; low status adds rising ends and hesitation sounds (D3 §4.1; B5 §5.3). Saye's: "A woman in her fifties with a clear mid-pitched voice and crisp consonants; {accent}, formal; slow, even, complete sentences with firm falling ends; very still, no filler sounds; close, clean studio recording." (D3 §4.2; her age in the story's word, K26).
2. **Never name a real person** or write "sounds like" anyone, because a recognisable imitation is that person's voice in law (D3 R18).
3. **Pace is timing.** `pace_wps` defaults to `speech_wps_default`; a formal, weighted speaker is slower (K08 sets Saye slower). Code builds time floors from it (`speech_floor_extra_s`) and caps speech per clip with `clip_speech_rule`.
4. **Keep voices apart:** two voices that share three or more of age band, pitch band, timbre, pace, accent and status blur on small speakers; change pitch band or pace first (D3 R7, §4.3).
5. **Accent undecided** (`WORLD.accents` not set): every VOICE stays `draft` (D3 R6; blueprint 5.4 rule 10).
6. **Paths are sound, not acting.** A **path** is how a voice reaches us: direct, earpiece, radio, intercom, recording, through glass. A parenthetical naming a place or device ("in her ear", "over the radio") is a path (D3 R11). Each path gets one `path_sound` treatment, added after a clean take (D3 §1, R24); a line heard from both sides of a cut is treated per shot (D3 R25). Decide speech through glass once, as a story-world rule: intercom for speech, "through glass" only for knocks and breath (D3 §8.1).
7. **Speech habits go in `speech`** and in the edit: a speaker who never contracts keeps it in every take (D3 R8); "Eli thinks before he answers. He always does." (line 1142) is a silence placed in the edit (D3 R9).
8. **`source` defaults to `designed`,** a small choice. Cloning is only for the user's own voice or a consenting, verified adult with a RIGHTS record; never a celebrity, a minor, a dead person, or from films and recordings (D3 R16-R17; card 24).

## Display and stillness

**Display** is how openly the body shows the pressure: 1 contained (one or two small changes, the rest still), 2 visible (two or three changes nobody can miss), 3 open (whole body, audible) (D15 §2.2).

1. **The closer the shot, the lower the display.** Display 3 in a close-up reads as melodrama; `display: 3` at `display_3_needs_why_at_or_tighter` or tighter needs a `why` (D15 §2.2; A1 P10, R36; CRAFT-25).
2. **Beat intensity is not display.** A beat of the highest intensity often plays best at display 1 (D15 §0; K14).
3. **If the line, the eyeline or the cut already carries the beat,** use display 1: still, or one small action (D15 R3).
4. **On a turn,** write the five steps as timed behaviour: the want as an eyeline, seeing the obstacle, the choice as a held moment, the action, and the face before the line (D15 R2, §1).
5. **Write stillness.** A moment of `hold_needs_still_s` or more, or a pause held on picture, names every still part in `still`, because models fill empty time with nods and drift (D15 R6, §1; CRAFT-26). Lips that part in silence need "No dialogue." and "closes it without a sound" (D15 R7).
6. **Eyes carry thought.** `eyeline` names a target and `dwell_s` how long; never "looks around". Singles made separately look past the lens on opposite sides and never into it (D15 R10; A1 R40, R44).
7. **Energy changes inside a shot, never at a cut;** breath not seen (a helmet, a back) is carried in sound (D15 R12-R13).
8. **Pauses:** tiers come from `pause_tiers`, with at most `long_pauses_per_scene_max` long pauses per scene (A1 R15; D15 R8); a turn's reaction lasts at least `turn_reaction_min_s` (TIME-05).

## Lip sync and voice takes

1. **Voices first.** No clip with a visible speaking mouth before the VOICE is locked; a model's own voices only for drafts and one-line parts (K16; D3 §1).
2. **Route order:** where the listener can carry the line, play it off screen; where the mouth must be seen, a video model that takes the line's audio as input first, lip sync after generation second, a cutaway third (D3 R20-R21; blueprint 8.5).
3. **Code derives `lip_sync`** from face height; a speaking face at `lip_sync_tight_face_height` or larger needs tight sync.
4. **A visor, glass, a hand or a prop over the mouth:** avoid on-screen sync; play the line from behind, in profile or on the listener. When lip sync fails twice on one shot, cut to the listener or an insert (D3 R22-R23).
5. **One speaker on screen per clip** (`on_screen_speakers_per_clip_max`, GEN-13), and at most `acting_characters_per_clip_max` acting.
6. **Takes:** three per line; for delivery parentheticals and turning lines, two alternates of three takes each; transcribe each take, reject wrong words, pick by ear (D3 §5.3, R10, R15). A VOICETAKE (one take of one line) keeps its `delivery` within `voice_delivery_words_max` words; `tts_text` keeps the story's exact words (D3 R14). "(beat)" splits a line into two files; very short lines are made inside their exchange (D3 R12-R13).
7. **Seat every line** in continuous room sound (D3 R27).

## Translation menus with pitfalls

Pick one behaviour, primary first, tied to this line; the rows are untested until D15 §4.4's test is run (D15 §4.2):

| Script word | Behaviour | Pitfall |
|---|---|---|
| shock | stops moving completely; eyes fix on Saye | a gasp, a hand to the mouth |
| holding back | eyes go to the flask, not to her; does not answer | shifty eyes |
| speechless | opens her mouth, holds it, closes it without a sound | generated speech: add "No dialogue." |

Delivery words come from the tactic: pressing becomes "level, quiet, unhurried, no rise" (D3 §5.2).

## Budgets and saved choices

`long_pauses_per_scene_max`; `display_3_needs_why_at_or_tighter`; `hold_needs_still_s`; `on_screen_speakers_per_clip_max`; `acting_characters_per_clip_max`; `voice_description_words`; `voice_delivery_words_max`. One display peak per scene, at or after the main turn (D15 §8).

## The baseline is a strong answer

Display 1, a still head, eyes on the other person, room sound and a clean designed voice at `speech_wps_default` are choices, not failures. Most reactions to a turn are contained: the camera magnifies (D15 §2.2; A1 P10).

## Cliché traps

Tests: any-film, mood-word, stacking, sound-off (card 05).

- "Looks sad" in `does` fails the mood-word test. Fix: two or three timed behaviours (D15 R1; WORDS-01).
- Sobbing in a close-up: display 3 where 1 would land (A1 R36; CRAFT-25).
- A hold with stillness unwritten comes back nodding and swaying (D15 §9).
- An early glance spends the later look (D15 R9).
- Stacking: a sad face, a sad line and music under it (A1 P10).

## Reasons that fail and reasons that pass

- Fails: "Close-up so we feel her shock." Passes: "SC10-B07, 'Her face changes.': display 1; she stops chewing, brows draw together, eyes drift down, and the line comes after the face (D15 Ex1, R2)."
- Fails: "Saye sounds cold." Passes: "VO-SAYE speaks in complete sentences with falling ends and no contractions until 'Saye has lost the voice she uses for answers.' (line 1383) (D3 §4.2, R8)."

## Two worked examples

### The Catch: SC10, "Not mint." (SC10-D11)

The scene's closest frame holds Iona through the line. Her subject item at step 8, built from D15 Ex1:

```
- subject: CH-IONA.S02 | at: left_third | faces: camera | eyeline: CH-SAYE | does: chews steadily; chewing slows and stops; brows draw together slightly; eyes drift down; chews once more, very slowly | tactic: discovering | energy: held | display: 1 | still: head, hands, torso | must_not: looking at Eli
```

The glance at Eli is saved for "Iona moves between her and Eli." (line 476). A raised upper lip reads as disgust, but the taste is familiar and wrong, so it goes on the take review's list with tears (D15 Ex1, §8). The take's delivery is "breath caught, quiet"; Saye's reply stays in her answers voice for contrast (D3 §11.1).

### The Long Places: "two breaths entire" (line 419)

Prose gives time in breaths: Melek "stood in the waiting, two breaths entire". Two calm breaths run longer than the long tier of `pause_tiers`, so the shot is a hold that needs a saved choice (K10; TIME-08). Breath is visible: the shoulders rise and fall twice and nothing else moves, so `still: head, hands` and `energy: held` (D15 Ex6). The knock passes to Yusuf and Nilay: record it once, as a MOTIF with `channel: body`, and keep its timing each time it returns (D15 Ex6).

## Self-check

- Does every recurring speaker have a VOICE with a description of `voice_description_words`, no real name, a pitch band, a pace and an accent from WORLD?
- Does every subject have a tactic, a `does` with no emotion words and a display that fits the size?
- Does every hold of `hold_needs_still_s` or more name its still parts?
- Does every `eyeline` have a dwell, and every saved look sit in earlier `must_not` items?
- Is the listener used wherever it can carry the line?

## Words for AI models

Works: behaviour steps joined by "then"; named body parts ("her lower lip"); stillness with its length ("her head and hands stay completely still; only her eyes move"); "The camera does not move." on a hold; "No dialogue." for silent lips (D15 §4.3, R6; C3 L14). Tone words only for the voice ("says quietly and unsteadily") (C3 §6). In a draft whose voice the video model makes, name the path: "his voice, heard only in her earpiece, thin; he is not visible" (C3 §7F).

Fails: emotion labels; `must_not` written as "no X" in a prompt (D15 §0); a one-sided expression's side in words (flip an approved still, D15 R19); long acting notes to a voice tool, which make the voice drift (D3 §2A).

## Look up for more

D3 §1, §3 (R1-R27), §4 (voice design), §5 (delivery), §8 (paths), §11; D15 §2 (display), §3 (R1-R24), §4.2 (behaviour words), §6, §10 (Ex1-Ex6); A1 R1, R8-R10, R15; C3 §6; K08, K10, K16. Print one rule with `stage.py lib D15 R9`.

---

From the skill file `cards/07 Places, things and motifs.md`:

# Card 07. Places, things and motifs

Read whole at step 4 (the motif, place and things units). Step 7 at Detailed depth reads only "Emphasis". "B4 R23" names rule 23 in B4's numbered rules (§8); "P" numbers are its principles (§1).

## The job

Turn the things a story names into records the camera can point at with the right loudness. A **motif** is a concrete thing (object, place, colour, gesture, sound) that returns and gathers meaning; a **prop** is a thing a character names, handles or changes; a **place** is a location with a job in the story (B4 §0.3). Harvest before you invent (B4 P1). Step 4 hands on MOTIF records ranked and mapped as story points, PROP records with `category`, `origin`, real size and sides, LOCATION records with their job, loudness, room sound, anchor (a fixed object seen in most shots) and exits, and every readable word as a TEXT record (card 17).

## Questions in order

1. **What is the theme as a question, and the core opposition as two nouns?** Read both from PLAN; The Catch sets GOODS against PERSONS, from its first prop: "Goods only. No persons." (line 19) (B4 §3.1).
2. **What does the story name more than once, or at a turning point?** Harvest objects, places, clothes, marks, sounds and words on things, each with its lines (B4 §3.1 step 3).
3. **Prop or dressing?** A thing a character names or handles, or that changes state on screen, is a prop; a thing only described as part of the room is dressing in `LOCATION.dressing` (A3 §5.3). The mint is a prop: Saye tears a leaf from it.
4. **Which pole is it on, or does it cross from one to the other?** A thing that crosses is the most valuable motif; the film's largest payoff (`largest_payoff: yes`) goes to the crossing closest to the climax (B4 §3.1 step 4, R2).
5. **How strong is it?** Score B4's six tests: named in the text; seen or heard without a caption; changes state; changes at a turning point; handled or looked at; cutting it loses a beat. Five or six yeses rank `spine`, three or four `supporting`, one or two become dressing at emphasis 0. Then, in order: all appearances in one scene, `single_scene`; strong but on neither pole, `plot_machinery`, framed only for clarity; not named in the text, at most `supporting` and marked `invented` (B4 §3.3).
6. **What does it mean, in one line, and which way does the meaning travel?** The user approves each meaning (B4 §3.1 step 6).
7. **Where does it appear?** Each appearance is a scene or a story point (a scene and a quote, placed before beats exist), with an emphasis and a role: plant (the first clear sight), develop (a return that changes something), teach (how it works), reveal (its meaning learned), payoff (its meaning spent), coda (one quiet return after) (B4 §0.3, §3.1).
8. **What does each place do, and is its set loud?** A **loud set** is a mind or a history made into a room: one establishing wide shows its governing feature, then it is shot for the action. A **quiet set** shows only where people are and what the danger is (B4 §4.1, R17). Write `dressing` as history: wear, absences, one kept living thing (B4 §4.3).
9. **Does the place need a set plan,** a measured floor plan with objects and marks? Yes where a shot is likely to need previs (grey 3D stand-in renders) at level `previs_plan_level_min` or more, a reflection or glass shot, or three or more people in one space (blueprint step 4; card 12).
10. **What states and sides will it have?** Real size, surface, the states to come, and an own side for any sided detail (B4 R13; PROP `side`).

## Emphasis

**Emphasis** is how loudly the camera points at a thing, on its own scale, never converted to another (B4 §3.4; K14): 0 present (small, part of the set); 1 placed (on a strong point, catching a highlight); 2 featured (an insert or medium close-up, handled or looked at); 3 spent (the beat turns on it: the only sharp or moving thing, or a rhyme: the plant's side, height, size and light repeated). A sound motif has its own **sound emphasis**, from buried under other sounds to heard alone (B4 §3.4). At step 7 write `emphasis` items and `added_emphasis` on each beat.

1. **Plants stay within `plant_emphasis_max`,** made clear by composition and light, not size; a plant that is itself a plot event (a rung breaks, a sign is read aloud) may use its plot-event value, with nothing pointing forward (B4 R6; K11; CRAFT-08).
2. **Emphasis 3 is a budget:** `emphasis_3_rules`. A second 3 for one motif only as a deliberate inversion of the first (B4 P5; CRAFT-09).
3. **At emphasis 3, sort what points at the thing.** Script markers (a state change on screen, a line about it, a look or a touch) are never removed. Framing (size, a held frame, a rhyme) is how you reach 3. Added emphasis (a music cue, a light change, a sound change, slow motion, an unmotivated camera move toward it) stays within `added_emphasis_per_beat_max`, and there is none where the script already marks the beat (B4 R23; CRAFT-10).
4. **A payoff is louder than its plant, or an exact rhyme of the plant's framing;** a payoff that depends on how a thing works gets one teaching appearance at 2 before it (B4 §3.4, R7, R8).
5. **While a line states what a thing means, keep the thing at 0 or 1** (B4 R21). Two spine motifs in one shot: only one above 1 (B4 R11).
6. **After the payoff,** later appearances stay at 0 or 1, with at most one quiet coda; a readout the plot needs may reach 2, with nothing recalling the payoff (B4 R26).
7. **An absence is shown by its holder,** with a look leading to it: "The clip under it is empty." (line 312) (B4 R9).
8. **Light follows emphasis:** at 0 and 1 only the scene's own light; a light change at 3 needs a motivating source in the scene (B4 §3.4).

## Translation menus with pitfalls

B4's table is a list of questions, not a lookup: ask "what is this story's version?"; pick at most one thing per beat and tie it to a line (B4 §7).

| Story meaning | This story's thing | Pitfall |
|---|---|---|
| A life on hold after a loss | "A pot of mint on the windowsill, and that is all." (line 404) | a lone houseplant no line asked for |
| A secret choice | an empty holder where something was | a glint on the object |
| Estrangement | labels and rings that read wrong | the camera noticing before the character does |
| Being treated as goods | tags, labels, people framed at the size of objects | bars for "trapped" before the story earns them (B4 §4.2) |

## Budgets and saved choices

- Visual spine motifs within `motif_spines_max` for the film's format, plus at most `sound_motif_max` sound motif and `body_motif_max` body motif (B4 §3.2; FILM-10).
- Loud sets within `loud_sets_max` (B4 R17; FILM-11).
- `emphasis_3_rules`, `plant_emphasis_max`, `added_emphasis_per_beat_max`; more plant inserts in a scene than `plant_inserts_per_scene_max` reads as heavy-handed (FILM-09).
- Supporting motifs never above 2, except at their own payoff when it is a plot beat (B4 §3.2).

## The baseline is a strong answer

Most appearances sit at emphasis 0 in the scene's light, and most sets are quiet. A thing that literally exists in the story, does something, and only also resembles the theme needs no pointing: the audience gets the literal meaning first (B4 §2.3, P4). Depart only for a reason you can cite.

## Cliché traps

Tests: any-film, mood-word, stacking, sound-off (card 05).

- Borrowed meaning (a dove, a ticking clock, a caged bird, rain for sadness, an empty chair) fails the any-film test. Fix: a thing only this story has, with a detail from the text (B4 R5, R25).
- A familiar image the text does name (hands on glass) is kept only if it has a practical job and changes between appearances, and is played plainly: no slow motion, no score swell, no push-in (B4 R24).
- Telegraphing: a plant framed bigger than its payoff (B4 §13).
- A glowing object, lit from within or brighter than the faces (B4 §13).
- Wallpaper: a return that changes nothing. Each return changes the state, the owner, the neighbour in frame or what the audience knows (B4 R12).

## Reasons that fail and reasons that pass

- Fails: "An insert of the mint so the audience notices it." Passes: "MO-MINT is planted at 1 in the kitchen wide, placed, not inserted, because it pays off in the same scene (B4 §9.3, R6)."
- Fails: "Push in on the flask for tension." Passes: "PR-FLASK stays at 1 while Saye looks at it (line 399); its one 3 is saved for 'She looks at the flask inside the outline. Leaves it there.' (line 1406) (B4 §9.3)."

## Two worked examples

### The Catch: the mint and Saye's kitchen (SC10)

LOC-SAYE-KITCHEN is one of the film's two loud sets: its bareness is the point ("No photographs. No magnets on the fridge.", line 404), so it gets one establishing wide that shows it, and no object in it points to Nell (B4 §4.1, §4.3). MO-MINT is `single_scene`: every appearance falls in SC10 (B4 §3.3).

```
- appearance: SC10 "A pot of mint on the windowsill" | role: plant | emphasis: 1
- appearance: SC10 "Her face changes." | role: payoff | emphasis: 2
```

The tearing is a medium shot; then Iona's face, not the leaf, carries the payoff. The script marks the beat (the line, the chewing), so nothing is added (B4 §9.3, R23).

### The Long Places: oil to the knuckle

"The oil goes to the first knuckle of the thumb and no further." (line 15). One composition serves every appearance: lens, angle, light and hand position stay; only the hand and the oil level change. Four hands get the insert: Melek's, Nilay's filled past the knuckle in 1999 and Nilay's first round at 2 each, and last Emre's at 3, because his line turns it into recognition: "Past the knuckle. The greedy or the frightened." (line 1315). The red ribbon he lays down on the same turn stays at 2, straight after the lamp's 3 (B4 §10, Ex 11.5; `emphasis_3_rules`). No montage of hands with music, no dissolve from hand to hand, no flashback to Melek under his line: the same frame does the linking (B4 Ex 11.5).

## Self-check

- Is the theme a question and the opposition two nouns, read from PLAN?
- Was every motif harvested from the text, and every invention marked `invented` with a practical job (B4 R27)?
- Does each spine motif have a plant, a develop and a payoff, each a story point with a role and an emphasis?
- Are counts within `motif_spines_max`, `sound_motif_max`, `body_motif_max` and `loud_sets_max`?
- Is every plant within `plant_emphasis_max`, and every 3 within `emphasis_3_rules`?
- Does every symbolic thing have a practical reason to be there, and every sided thing an own side?

## Words for AI models

Works (B4 §14): concrete nouns with material, colour and size ("a small brushed-steel vacuum flask"); wear described physically ("a grey steel sill with one bright polished band along its edge"); position and size in frame to set the emphasis ("in the background, small, slightly out of focus" for 0); one saturated accent in a muted scene.

Fails: meaning words ("symbolizes", "motif", "foreshadowing"); mood words on objects ("ominous", "important"), which return glowing, centred, hero-lit things; named absences, which get drawn, so describe what is there ("a bare metal spring clip closed on nothing"); exact words on props (card 17). A model keeps a thing's state only with a reference picture for each state.

## Look up for more

B4 §3 (procedure, tests, scales), §4 (sets), §5 (props), §7 (translation table), §8 (R1-R27), §9 (The Catch's motifs), §10 (The Long Places), §11, §13, §14; A3 §5.3 (element categories); card 12 and B3 §6 (set plans); K11 and K14. Print one rule with `stage.py lib B4 R23`.

---

From the skill file `cards/15 Action scenes.md`:

# Card 15. Action scenes

Situation card for the tag `action`. Steps 7 and 8 read only "Questions in order" and "Traps"; chat apps read it whole. "D11 R12" is rule 12 in D11 §2.

## Situation

A passage holds a fall, a fight, a strike, a climb, a push, a throw, weightlessness, or a move the text calls fast (D11 R1). Models fail most here (D11 P7). An action scene is still a scene: someone wants a physical result, the danger grows, fortune flips at least once, and it ends changed (D11 P1).

## Questions in order

Example: The Catch scene 2, "Her hand closes on a rung and the rung TURNS." (line 81): cause the grip, effect the turning rung, anchor the bright sheared bracket (D11 WE1).

1. **What physical result does someone want, and what has changed by the end?** (D11 P1)
2. **Where is everything?** Write `geography`: the **anchors** (fixed, easily seen objects that orient the viewer), exits and the direction of travel. Show it once, calmly, before the pressure (D11 R5-R6; A4 C6). A journey keeps one `travel` in every shot until the story turns it (A3 §5.9; GEOM-07).
3. **What causes what?** Write `cause_chain`: each cause and its effect as two visible events (D11 R2).
4. **How does the danger grow, and where does fortune flip?** Write `escalation`, and each **reversal** (a beat that flips fortune) in `reversal` as beat IDs. None written? Find the one the text implies: a habit, a false relief (D11 R3).
5. **Does a beat fail?** Write the failure as the action, early, with a failed end state (D11 R4).
6. **Which `time_treatment`?** Reading time longer than story time: `overlapping_slices` (shots at real speed whose story times overlap); a wait: `held_real_time`; long and repetitive: `elliptical`; otherwise `real_time_continuous`; `slow_motion` only where the camera system (CAMSYS) allows it (D11 R12; CRAFT-16; K30).
7. **Write the `action_score`:** one row per **count** (one step of the action, an order, not a length), one column per body, the set and the camera; `+` applies force, `-` receives it, `=` holds still; `+` and `-` on one count means touching (D11 §4.2).
8. **What is the camera fixed to?** It obeys the characters' physics and changes its **mount** (what it is fixed to) only on a cut hidden in black or a passing body, or as the film's one CAMSYS `break` (B1 R23; D11 R17).

## Rules

1. **Physics is honest where the audience can measure it.** A **clock** is anything in frame that measures story time (the yellow stripe growing). Clock shots play at real speed, screen time equal to their **slice** (the story time shown), always forward; only clockless shots are held (D11 §3.2, R13; K20). Falls are positioned from `free_fall_half_g` on every frame (C4 R10), in a SHOT `motion` item or a master previs (a grey 3D rehearsal) named in `time_slice`; weightless bodies are positioned relative to the moving room (C4 R11).
2. **One acting body per clip where possible** (at most `acting_characters_per_clip_max`); one main action per `main_actions_per_seconds`; one camera move or none (D11 P7, R18; CRAFT-06, CRAFT-15).
3. **Touching bodies are split** so one acts per clip; a strike is angle, reaction and sound, the impact heard, never shown (D11 R20, R28).
4. **Several angles of one continuous action** become a designed shot or a chain (`start: from_end_of:`), not master and coverage (A3 R16; D11 R19).
5. **Cut on the same motion mid-action**, the whole action in both clips; cutting away, let it rest first (A4 R3; D11 R9).
6. **Never perform** height, speed, impact, falling or striking for reference (D11 R25).

## Traps

- **Nobody knows where anyone is.** Test: could a stranger point to every body at each cut? Fix: an anchor shot before the pressure (D11 P2, R5).
- **The effect before the cause.** Fix: two shots (D11 R2).
- **The grip holds**, because models favour success. Fix: the failure as the action (D11 R4).
- **Slow motion to stretch a moment.** Fix: overlapping real-time slices (K20, K30; B1 §6.1).
- **A fall that floats, or a clock that runs backwards** (the stripe shrinks between shots). Fix: compute the fall from `free_fall_half_g`; slices only move forward (D11 §8).
- **Shake for excitement.** Test: does the camera share the characters' physics? Fix: lock it to what they ride (B1 R23).
- **Bodies merge at the hit.** Fix: separate clips (D11 R28).

## Words for AI models

Works: one main action and its end state; the failure as the action; the direction of travel (D11 Recipe E). Weightless: "hair, cloth and straps drift up; nothing settles", the camera locked to the room (C3 §12). A fast move made "in slow motion" and doubled in the edit plays at real speed (D11 R15; K30). Fails: "falling" for floating bodies (C3 §12); injury words (C1 R9); fine hand work in wides (D11 R21).

## Worked example

**The Catch, scene 6 (tense):** `overlapping_slices` from "The cage falls." (line 240) to "A hard metal CLACK." (line 259), positioned in `PV-SC06-MASTER` (K20). Clock shots (the wall, the opening, "the yellow stripe. Coming.", line 248) are short forward slices; the stripe never shrinks. Held, clockless: the floating body, the blood beads, "He has one hand she cannot see." (line 253), the longest. "Her grip begins to slip." (line 255) precedes the reversal, "She hooks her fingers deeper into the grid." (line 257) (D11 WE2). The camera, fixed to the cage, never shakes (B1 §10.1).

**The Long Places, chapter II (quiet, unscored):** "She pushed with the flat of her hand, the heel of her hand, her shoulder; the pivot gritted and kept its opinion." (line 140): three escalating beats, more of her body each time, the grit an `effect`. The reversal, "The flame lay down and would not stand", turns being shut in into bad air. Pushes `real_time_continuous`, the flame's three lyings-down `elliptical`; for reference, push a real door on a locked-off phone (D11 WE5, R24).

## Look up for more

`stage.py lib D11 §2` (rules), `D11 §3` (time), `D11 §4` (score), `D11 §9`. `C4 §8`; `A3 §5.6`; `B1 §10.1`; K20, K30.

---

From the skill file `cards/16 Glass, mirrors and sides.md`:

# Card 16. Glass, mirrors and sides

Situation card for the tags `glass_and_reflection` and `handedness`. Steps 7 and 8 read only "Questions in order" and "Traps"; steps 3 and 5 read it whole when a mirror rule exists.

## Situation

Glass stands between people, a shot needs a reflection, or a sided feature (a ring, a raised hand, a scar) is in frame in a mirrored world. Glass lets the eye through and stops the hand; who sees whom is a lighting choice (B3 §4.8). A wrong side breaks a plant (B4 R13).

## Questions in order

1. **Which era is the scene in, and is its frame `original` or `reversed`?** An **era** is a stretch of the film under one frame handedness; code derives it from the `WR-MIRROR` era lines (K03). Never type it.
2. **What is each element's `handedness` in its STATE?** Code derives `mirror_state`: mirrored where it differs from the frame (K03; blueprint 5.6).
3. **Which sided features are in frame?** Each needs an own side (SIDE-01); code derives the image side. Behaviour text says "hand nearest the camera"; state lines never say frame-left (blueprint 5.4 rule 8; SIDE-02).
4. **Does the story state a side for a mirrored element?** That side is apparent: the own side is the opposite, `origin: inferred` (K03; SIDE-04).
5. **In profile, which hand is nearest the camera?** A person facing frame-right shows their own right side; one facing frame-left shows their own left (B3 §8.2).
6. **Is there glass in frame?** Give it a `glass` item: state `clear`, `marked` (a smear, label or crack makes the pane visible), `reflecting`, `screen` or `broken_open`, and camera `through`, `along` or `angled` (B3 §8.1).
7. **Which side of the glass is the camera on?** The side of the character whose scene it is (`whose_scene`); it crosses only when the point of view shifts (B3 R11).
8. **Must a reflection lie over someone?** Check the twin and the light (B3 R28-R29).
9. **Is a plot-sided detail of a mirrored element, or readable text, in frame?** Code routes the shot (K02): text becomes a text graphic added after any flip; the detail takes the **plate route** (the place and its mirrored people made in world orientation and flipped as a still, the normal people added unflipped, then animated). A sided insert is an edited still, `flip: never` (K07).

## Rules

1. **A reflection appears where the mirror twin stands:** the reflected person as far behind the pane as they are in front. Put the camera on the line through the twin and the far person, and keep the far side darker, because glass reflects little light; side by side along the glass, they cannot line up (B3 R28).
2. **For clear glass with no reflection,** keep the camera's side darker than the far side (B3 R29).
3. **Across the world's turn, repeat size, lens and position,** so the world changes and the camera does not (B1 §10.2).
4. **Code picks `mirror_route` in K02's order:** a text graphic for readable text, always; the plate route (question 9) for a plot-sided detail of a mirrored element or a differing face of `plate_route_face_height` or more; then direct, flip with mirrored references, flip all (blueprint 8.5; C2 R5).
5. **A sided insert** (a ring, a palm) is an edited still at its final side, with `flip: never` (K07; SIDE-03).
6. **Hands on glass are rationed:** repeat the insert's framing, change one thing each time, and never add one the story does not have (B3 §8.3, R20, R27).
7. **A helmet visor stays `clear`, lit from inside, in every close-up where the face must read;** story content reflects in it at most once (B3 §8.1).

## Traps

- Asking a model for "mirrored", "backwards" or "the wrong hand" returns garbled or random sides (C2 §7.2; GEN-06). Fix: make the side right in a still, then flip or composite.
- Flipping a shot with a normal character in it moves her ring to the other hand. Fix: the plate route (C2 §7.2).
- An edit model quietly "un-flips" backwards letters. Fix: add lettering last (C2 §7.2).
- Glass so clean the hands seem to touch: the payoff is contact without touch, so let a frame edge or a faint reflection show (B4 §9.3).
- Breath fog, tears on the glass, a slow push-in with music: the familiar image played big (B4 R24).

## Words for AI models

Glass wording comes from the phrasebook by glass state (K18): clear becomes "seen through perfectly clear glass; the room on the camera's side is dark". Raised hands become "both raise the hand nearest the camera, palms toward each other, exactly like a reflection" (C2 W3). Never write "mirror image", "backwards text" or a side that a flip will change (C2 §7.2).

## Worked example

**The Catch, SC10:** "They stand facing each other across the table like a woman and her reflection, each with the wrong hand in the air." (line 428). Era b, frame `original`: Saye's state is `reversed`, so she is mirrored; Iona is normal (K03). Camera A looks along the table's centre line, on lens exception `LX-01`, spending one use of saved choice `RC-01` (K07). Iona, frame-left facing right, raises her own right hand, nearest the camera. Saye, frame-right facing left, raises her own right, which reads as her left, also nearest the camera; her ring, own left and apparent right (line 436), is on the far, lowered hand (B3 §8.2). Saye's raised hand is plot-sided, so SH080 takes the plate route (question 9). The rings are edited-still inserts, SH090 and SH100, `flip: never` (K07, K22).

**Another tone, The Long Places, chapter VI:** Yusuf's pool holds "a figure's worth of dark, upright" that stays still "while everything else in the water moved" (line 524). Lay the still shape over the rippling reflection as its own layer, so the evidence stays exact and uncertain (D6 W6).

## Look up for more

B3 §7.2 (R28-R29), §8 (glass and mirrors); B1 §10.2; C2 §7; D6 W6; K02, K03, K07, K18, K22. Print one rule with `stage.py lib B3 R28`.

---

From the skill file `cards/17 Screens, text and in-story cameras.md`:

# Card 17. Screens, text and in-story cameras

Situation card for the tags `screens_and_text` and `in_story_footage`. Steps 7 and 8 read only "Questions in order" and "Traps"; step 3 reads only "Text orientation"; step 4 reads it whole.

## Situation

Words the audience must read (signs, labels, displays, title cards), screens inside the frame, and footage recorded inside the story. Models draw text badly and change it between clips, so every readable word is drawn by code and laid in afterwards (K17; C3 §13A).

## Questions in order

1. **Must the audience read it?** Make a TEXT record with the exact words, case, orientation and surface, `method: composite`; only text too small to read is left to the model (A3 R11; K17).
2. **How long must it stay?** Code derives the reading floor from `text_floor`, doubled when mirrored (K09). If the shot is short, put the words up early and let the change come late (D12 Recipe 2).
3. **How big?** Size a must-read word for the device's smallest appearance in frame (D12 R6, R10).
4. **Is its meaning taught first?** A display the plot will read gets one teaching appearance at emphasis 2 at least a scene earlier (D12 R2; B4 R7).
5. **Who made it?** The maker decides its orientation in a mirrored scene ("Text orientation"; SIDE-05).
6. **Is it footage recorded inside the story?** Give it a CAMERA record (position, lens, frame shape, frame rate, overlays, `moves`), record the event once as one continuous take, and cut every viewing from it (B1 §10.4, R22).
7. **Is a screen in frame?** The device shot asks for a blank screen; its content is its own shot, pinned on afterwards (blueprint 8.5; C2 R6; C3 §13B).
8. **Does a later scene replay this one?** Put the replaying camera into this scene's set plan as a named setup (A3 R9).
9. **Does something appear or vanish on a fixed feed?** Between two frames: no camera move, no dissolve, no glow (B1 R20, §10.6).

## Rules

1. Draw exactly what the script says a display shows (D12 R1).
2. A colour keeps one meaning film-wide, and a state colour changes on one frame, never by a cross-fade (D12 R3, R12).
3. Colour never works alone: red is also dashed and darker, green solid and brighter (D12 R13).
4. Invented words (a clock, a unit) stay smaller than every scripted word and are logged `origin: invented` (D12 R4).
5. No blink, pulse or sting on a display change the script does not write (D12 R16; B4 R23).
6. Design in-story footage backwards from what it must reveal (B1 §10.4).

## Text orientation

In a mirror story every TEXT follows a story-world RULE of kind `text` that names what it governs and its exceptions (`reads: normal | mirrored`, `why`) (K04; SIDE-05).

1. Title cards, credits and captions are never mirrored (D12 R17; `WR-TITLES`).
2. A picture made inside the story world and shown on a screen (a recording, a feed, a file) is flipped whole, once, in a mirrored **era** (a stretch of film under one frame handedness) (D12 R18; B1 §10.2).
3. A display that draws the positions of things also in the picture reverses only its words, each where it stands, and keeps its drawing true (D12 R19).
4. A device that turned with the character keeps its orientation to her: by default the suit's words stay backwards after Iona's second turn (a question for the user, D6 §12), so the first forward world word is the wall sign, "On the wall above Saye: RECEIVING." (line 1620) (D12 R21, §4.3).
5. Mirrored words must visibly reverse: build them from letters that change in a mirror, not from A, H, I, M, O, T, U, V, W, X or Y (D17 R18).
6. Never reverse each word where it stands and then flip the whole layer: the two cancel (D12 Recipe 3).

## Traps

- Readable or backwards text asked of a video model (GEN-06; C2 §7.2). Fix: a code-drawn TEXT record.
- "Hologram", "interface" or the script's own words in a video prompt: the model invents its own text and glow. Fix: ask for a blank screen (D12 Recipe 9).
- A red-to-green cross-fade passes through yellow, the colour of the painted line. Fix: change on one frame (D12 R12).
- A mirrored play triangle reads as rewind. Fix: a pause glyph or none (D12 R20).
- Security footage zoomed into a clean close-up: the evidence stays small in the fixed frame (B4 Ex 11.2).
- A title card flipped with its era. Fix: never flip titles (D12 R17).

## Words for AI models

The device with a blank screen: "the monitor's screen is dark and blank, switched off", or for a moving shot "a flat, evenly lit, pure bright green panel" (D12 Recipe 9). A feed as its own clip: "high corner security camera view, wide lens, grainy, fixed" (C3 §13B). A lamp carrying a colour code: "a small round lamp on the shell, glowing red", its hue matched in the grade (D12 Recipe 9, R15).

## Worked example

**The Catch, SC13:** "Security footage, paused: a camera above the top gate, looking straight down the shaft." (line 674). `CAM-SHAFT-TOP` is fixed and top-down, with a wide lens, a low frame rate and a clock printed into the picture; the fall is recorded once for every viewing (B1 §10.4). It was recorded in era a and is shown in era b, so the whole picture, clock included, flips once (`WR-REPLAY`; D12 W2). The puck stays small in the paused frame; "Iona pauses the recording with the remote." (line 742) carries the emphasis, not a zoom (B4 Ex 11.2).

**Another tone, The Long Places:** Yusuf's tally screen counts openings (line 504). The count is the hero, in large numerals; cut from a "40" insert to a "41" insert of the same framing, with no animation on the number (D12 W6, R9).

## Look up for more

D12 §3, §4 (mirrors), §11; B1 §10.4-§10.6; C3 §13; K04, K09, K17; card 16. `stage.py lib D12 R19` prints one rule.

---

From the skill file `cards/18 Suspense, reveals and the dark.md`:

# Card 18. Suspense, reveals and the dark

Situation card for the tags `suspense_and_reveal` and `darkness`. Steps 7 and 8 read only "Questions in order" and "Traps". "A4 S2" is rule S2 in A4 §9; "B2 R23" is rule 23 in B2 §7.

## Situation

A fact matters and someone does not know it yet, a reveal is coming, or the scene is dark. FACT records hold who knows what, from when (A4 §6.5). What the frame keeps out is as authored as what it shows (B1 P7), and what stays dark is designed as carefully as what is lit (B2 P7).

## Questions in order

Example: in The Catch scene 6, "He has one hand she cannot see." (line 253): we learn that Eli hides something, not what; the frame keeps his hand out of view (B1 Ex2).

1. **Which FACT records have an element in this scene before their reveal?** Every earlier shot that could show a FACT's `element` (what would give it away) carries `keep_hidden`: the fact and a way from question 4 (`FT-03 | how: frame_edge`) (A4 S3; INFO-01).
2. **What is each fact's `mode`?** **Suspense** and **dramatic irony** (we know more than a character): show the danger early and clearly, then hold longer on the unaware (A4 S1-S2; TIME-09). **Mystery** (we know the same): stay with the **whose-scene** character, the one whose point of view the scene holds; reveal with them. **Surprise** (we know less): once, at a big turn, fair on replay (A4 §6.5).
3. **Should the audience know more?** Plan the telling shot at least one beat before it matters (A3 R4), showing the hidden thing where the other character cannot see it (A1 R4). To share a character's not-knowing, stay on that face while the other keeps the secret (A1 R3).
4. **How does each earlier shot keep it hidden?** Mildest first: `frame_edge`, `focus`, `dark`, `obstruction`, `timing`, `sound_first` (A4 §6.6).
5. **Does a shot show what that character cannot know?** Give it a `pov_break` (A3 §7.3; REASON-09).
6. **At the reveal:** a clean, readable view, then the landing face (the face showing what it means); `role: turn` or `must_keep` (A4 §6.6; INFO-02). With clues already given, play it as confirmation in real time (A4 S4).
7. **A stated time limit?** Honour it in screen time, or stretch it with a `why` (A4 R6).
8. **In the dark:** what stays dark (LOOK `stays_dark`, SHOT `dark`), and what one element stays readable in every shot: a rim, an eye light, a lit hand (B2 R23)? Darker skin is exposed, filled and named (`skin_light`), never grey (B2 R24).

## Rules

1. A **plant** (a detail shown early so a later moment pays it off) gets one calm, clear shot within `plant_emphasis_max`; the payoff repeats its framing or sound (A4 S5; K11; FILM-02).
2. Hide a body part or an object, not the face, when a character hides something from another but not from us; lose the eyes only to hide their inner life from us (B2 R6-R7).
3. A large revelation lands hardest in the flattest light available (B2 R11).
4. A growing threat is heard before it is seen (A4 SND1); no music under a reveal meant to stay open (A4 SND5).
5. If a later scene replays this one on a screen, put that camera in this scene's set plan now (A3 R9).
6. Release suspense in a way the audience accepts; do not punish it (A4 S6).
7. Every dark line the story writes needs a `stays_dark`, a `light_cue` or a shot `light` (COVER-08).

## Traps

- **Faster cutting for suspense.** Test: the unaware character's shots average shorter than the scene's dialogue shots. Fix: hold (A4 S2; TIME-09).
- **A reveal spoiled by coverage.** Test: a wide or reverse shows what a close shot keeps hidden. Fix: check `keep_hidden` against every shot (A4 §13).
- **The camera finds the secret**, tilting down to the hidden hand. Fix: keep the frame edge (B1 Ex2).
- **A sting or push-in on a reveal the script already marks.** Fix: add nothing (`added_emphasis_per_beat_max`; CRAFT-10).
- **Too dark to follow.** Fix: one readable element per shot (B2 R23).
- **A darker face gone grey** beside a correct lighter one. Fix: reject it (B2 R24).

## Words for AI models

Works: name only what is in frame; hidden things go in `must_not_show`, sent to the model's exclusion field where it has one (K18). Darkness as a visible result: "the far corner falls into deep shadow; her face is lit from the lamp at her knee" (B2 P12); the skin tone and the light on it named (B2 R24). Fails: "moody", "atmospheric", "dramatic lighting" (GEN-12); the secret named in a prompt.

## Worked example

**The Catch, scenes 6 and 13 (tense):**

```
### FACT FT-03 The hand in the fall
- what: in the fall, Eli's hidden hand clipped the puck to the grid
- element: PR-PUCK.S02
- audience_knows_from: SC13 "Eli's hand comes out from behind Jude's back."
- known_by: CH-ELI | from: SC06 "He has one hand she cannot see."
- mode: mystery
```

That Eli hides a hand at all is a separate FACT, `dramatic_irony` from scene 6 (card 01).

In scene 6 Eli's arm leaves the bottom of the frame: `keep_hidden: FT-03 | how: frame_edge` (B1 Ex2; B2 R6). In scene 13 the recording from `CAM-SHAFT-TOP` plays in real time, flat and top-down (B2 R11), and "Jude watches her watch it." (line 734). The footage holds through "Empty.", so we find the puck before Iona reacts; then her face: "Looks at her brother. Not at Jude." (line 742) (A4 WE2, S4).

**The Long Places, chapter V (enigmatic, dark):** "the cough came, beside her, at her left, where nobody was" (line 439). The lamp at her knee is the shot's one readable element (B2 R23); the cough is heard off screen and never given a source; the camera stays with her and never turns to search the dark (A4 §6.6; B1 P7).

## Look up for more

`stage.py lib A4 §6.5`, `A4 §6.6`, `A4 §9`: `library/A4 Editing, transitions, rhythm and sound.md`. `A1 §6`; `A3 §9`; `B1 §10.4`; `B2 §7`; card 17.

---

From the skill file `cards/19 Inner life, montage and time.md`:

# Card 19. Inner life, montage and time

Situation card for the tags `prose_interior` and `montage_and_time`. Steps 7 and 8 read only "Questions in order" and "Traps" (with card 02's "Externalising inner life" for `prose_interior`); chat apps read it whole.

## Situation

The scene holds what a camera cannot photograph as written: a thought, memory or feeling inside a character (`prose_interior`), or time that passes, repeats or is summed up (`montage_and_time`). Screenplays have it too: "Everything in her wants to be on the other side of the road." (The Catch, line 370).

## Questions in order

1. What kind of passage is it: a scene, where story time runs at telling speed; a **summary**, much time in little text; an **iterative** passage, told once but happening many times; a pause for description; or inner thought (A3 §7.4)?
2. For thought: has the source already given the behaviour? If not, climb card 02's ladder in order (behaviour; an object; her face cut against what she thinks of; framing and light; a sound; a line to someone; voice-over; text in picture; cut it) and stop at the first rung a stranger could read (A3 §7.2, R17; A1 R32).
3. A held face needs a task, and a chosen shot before it that shapes how it is read; never a blank stare (A3 R5).
4. Is the best language in the narration? Put its images into design and composition, not new lines (A1 R34).
5. Is the talk only reported? Dramatise one line and carry the rest in pictures (A1 R33; A3 §7.6).
6. Is it iterative? Film one instance, the one with a change or a **plant** (a detail placed for a later payoff), or a **montage**, a run of short shots that compresses time, of three or four visibly different instances (A3 R18).
7. Does a summary hide a scene, with a place, a time, two people and a change? Dramatise it (A3 R19).
8. Does time jump, and must the audience know how far? Carry it with something from the story's world first: a dated page, light, season, a new injury, a cold cup (A3 §7.8).
9. How is the jump joined? A time cut for minutes, a dissolve or fade for days or years, a montage when the passing is the point; but where the story writes only cuts, a cut with a clear change of light and **room sound**, the place's steady background (A4 T2, T5).
10. Record it: BEAT `unsaid` and its **carrier**, the thing that makes it seen or heard; SCENE `presentation: montage` or `time_treatment: elliptical`; an added carrier in `additions`, marked `invented` (A3 R24).

## Rules

- **Voice-over**, a voice heard over the picture, only where the words are the point, such as a letter, over pictures that do not repeat them (A3 §7.2, §7.7).
- A turn, the beat where a value (a two-pole quality of a life) changes for good, never sits inside a montage; it needs a scene (A4 §5).
- A dissolve, fade, freeze or cut to black needs a break the story itself makes: a written transition, or a section break in prose (A4 §5.1, T5; CRAFT-13). In a short, cut to black, true silence and freeze stay within `device_budget_short` (A4 P10; CRAFT-12).
- A dated page or a document shown as a time carrier is text in picture and gets its reading time from `text_floor` (K09; TIME-01).
- Description becomes set design, light and one or two establishing pictures, never a held shot of nothing (A3 §7.4).

## Traps

- **Voice-over first.** Test: does the voice say what the picture shows? Fix: climb the ladder; keep a voice only if it adds (A3 §12).
- **The thought spoken to nobody.** Fix: a line to someone under pressure, or a carrier (A3 §7.2; A1 P3).
- **A simile filmed.** Test: is the compared thing really in the scene? Fix: play it on the face (A1 §5; A4 §5.1).
- **Identical repeats** of an iterative act. Fix: one instance, or instances that differ visibly (A3 R18).
- **A montage over a turn.** Fix: make the turn a scene (A4 §5).
- **An invented dissolve or title card for time.** Fix: a carrier from the story's world (A3 §7.8; A4 T5).
- **A blank face held as "thinking".** Fix: a task, and the shot it is cut against (A3 R5).

## Words for AI models

Works: the behaviour itself, "she holds the wheel so hard her skinned palm opens"; one prompt per montage shot, each with its own visible difference in light, season or object state; time as a thing, "a cup of tea gone cold" (A3 §7.8, R18). Fails: "she remembers", "she feels homesick", "time passes" (A3 P3; A2 R25).

## Worked example

### The Catch, scene 9 (inner life in a screenplay)

"Everything in her wants to be on the other side of the road." is thought, and the script gives the first rung at once: "She holds the wheel so hard her skinned palm opens." (line 370). "He looks at it the way you look at a result you expected." (line 374) is carried by stillness: Eli in profile against the backwards street, calm, while her hands whiten (A1 Ex2). "Street names. Shop signs. The dashboard clock" (line 372) is a small montage inside the drive, one insert per backwards thing (A3 §7.4; A4 §5). Tags: `prose_interior, montage_and_time`.

### The Long Places, chapter I (repeated time)

"In the evenings she entered the 1924 survey" (line 67) becomes one evening (A3 R18). The shaft's breath, "eighteen minutes, and eighteen again" (line 75), passes as a watch insert (A3 Ex5) and a time cut, since only minutes pass (A4 T2). "She did not turn her head." carries the warmth at her shoulder; "It was homesickness, she decided" is cut (card 02).

## Look up for more

`stage.py lib A3 §7.2`, `§7.4`, `§7.8`: `library/A3 Script breakdown, directing and adaptation.md`. `A1 R32` to `R34`: `library/A1 Dialogue as action and subtext.md`. `A4 T2`, `A4 §5`: `library/A4 Editing, transitions, rhythm and sound.md`.

---

From the skill file `cards/20 Creatures, violence and filters.md`:

# Card 20. Creatures, violence and filters

Situation card for the tags `creature` and `violence`. Steps 7 and 8 read only "Questions in order" and "Traps"; chat apps read it whole. "B5 §6.2 rule 4" is rule 4 of B5 §6.2; "C1 R9" and "D4 R10" are rules in C1 §6 and D4 §4.

## Situation

A non-human character (`tier: non_human`) must frighten, move us, or both; or a shot holds violence, a weapon, blood or fire, which hosted models' **filters** (automatic checks that refuse a request) may block (C1 §4; D4 §3.6). Plan around filters, never through them (D4 P4). A shot's **content flags** name the sensitive subjects it touches, and its **policy route** says how it is made (D4 §6); **compositing** lays a separately made element over the clip in the edit (D11 §0).

## Questions in order

Example: in The Catch scene 16, "Behind her: a pump. Three uneven strokes." (line 887) comes before any picture of the figure; then it is simply there, "Taller than the door." (line 891) (B5 §6.2).

Creature:
1. **What must it do to the audience, and when?** Frighten first, earn pity after, play fair throughout (B5 §6; B5 R10).
2. **Fear:** silhouette before surface, matte black lit by its rim against something lighter (B2 R25); two or three wrong proportions in an otherwise human body; one face feature removed or moved; sound before sight; in human rooms, arrival without travel, a hard cut from an empty frame; scale against a door, a bed, a chair (B5 §6.2).
3. **Pity:** damage it suffers, care shown before explanation, a cost paid, a gesture echoing one already in the film (B5 §6.3, R13).
4. **Fairness:** is every **clue** to the reveal (a strange detail that makes sense later) seen the first time, strange rather than hidden, as a PLANT (a detail shown early and paid off later) within `plant_emphasis_max` (B5 §6.4, R11; K11)?
5. **No face?** Its thinking goes to head direction, hands and the order of its looks (B5 R12).

Violence:
6. **Which `content_flags` and which `policy_route`** does each shot carry (D4 R10)? Flags include `violence_implied`, `violence_onscreen`, `weapon_visible`, `gunfire`, `blood_small`, `gore` and `fire`; routes are `as_written`, `restated`, `split_cause_reaction_aftermath`, `composite_element`, `sound_only` and `cut`.
7. **Can cause, reaction and aftermath be separate shots,** the impact off screen, gunfire in the sound, blood and sparks composited (C1 R9; C3 §14)?
8. **Must a strike land?** Build it from angle, reaction and sound, in separate clips (D11 R28).

## Rules

1. Words for the visible result, never injury words: "a dark red stain spreads through his shirt" (C3 §14; C1 §4).
2. Weapons partial, soft, never aimed at a person in frame; gunfire in the mix; a muzzle flash is a composited flicker (D4 §3.6).
3. A request refused twice: stop rewording, move the element to compositing or sound, log it; never code words or misspellings (C1 R10; D4 R11).
4. Open weights remove the filter, not the law: keep it non-graphic, check the licence, disclose (D4 §3.6, R12).
5. A creature has **reference pictures** (fixed pictures of each state) with a scale object in every shot, and a depth guide (a grey picture where brightness means distance), never a pose guide (a stick figure), which forces human proportions on it (C1 R5; C4 R7; blueprint 8.5).
6. Nothing that fits a famous robot or alien: no glowing eyes, chrome or scanning light bar (B5 §6.2 rule 7, R26).
7. No slow motion to make violence weigh more (B1 §6.1).

## Traps

- **Glowing eyes and chrome on a creature.** Test: would it fit a famous robot? Fix: remove what that robot would have (B5 §6.2 rule 7).
- **Walking it in** through a human room's door. Fix: a hard cut from the empty frame (B5 §6.2 rule 5).
- **Body and sound arriving together.** Fix: sound first, source later (A4 SND1-SND2).
- **The cute reveal**, a toy's big eyes. Fix: pity from behaviour (B5 §13 mistake 11).
- **A clue first seen at the reveal.** Fix: plant it earlier (B5 §13 mistake 10).
- **The wound entering in one clip.** Fix: split (C1 R9).
- **A third rewording of a refused prompt.** Fix: reroute (D4 R11).

## Words for AI models

Works: "shaped like a person", never "humanoid"; the visible quality, "soft pale matter behind glass" (B5 §6.2, §10.9); the genre first, "A tense dramatic thriller scene." (C3 §14); injury by look, "he sits down heavily; a dark stain spreads on his shoulder" (C1 §4). Fails: "robot", "alien", "armour", "humanoid", "glowing eyes", "exosuit", "chrome" (GEN-12); gunshots or blood asked of the model (D4 §3.6).

## Worked example

**The Catch, scene 16 (tense; creature and violence at once):** the pump is heard over Iona's face first (A4 WE3). A hard cut shows the figure against the lighter sealed door, rim-lit, taller than the door frame (B2 R25; B5 §6.2). Its raised arm reads as an attack now and as reaching later, a fair clue (B5 §6.4). "She swings the cylinder with both hands." (line 898) is her swing in one clip, the figure's reaction in another, the impact in the sound: `content_flags: violence_implied`, `policy_route: split_cause_reaction_aftermath` (D11 R28). "A thin WHITE JET shoots from underneath it." (line 900) is damage it suffers, planted for later pity (B5 §6.3), composited if refused (C1 R10).

**The Long Places, chapter V (enigmatic):** "something came under the knock. Low. Shaped. With the fall of a sentence in it." (line 421). The source is never shown: stay on the women listening along the walls (B1 P7). Build the sound from breath and the room's resonance, never a generated voice, which would settle what the book leaves open, and it must not be intelligible (D9 §8.4; A4 SND1).

## Look up for more

`stage.py lib B5 §6` (non-human characters), `B5 §10.9` (the figure): `library/B5 Character design for story.md`. `C1 §4`, `C1 §6`; `C3 §14`; `D4 §3.6`, `D4 §4`; `D11 R28`. Card 24 for rights and content flags.
