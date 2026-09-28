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
