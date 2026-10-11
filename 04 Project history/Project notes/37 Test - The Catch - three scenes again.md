# 37 Test - The Catch - three scenes again

Log entry 37. The same test as note 35, run again after the fixes in note 36. A fresh Opus 5.5 helper, using only the kit, started The Catch from scratch in a test folder. It planned the whole film, then wrote scenes 2, 13 and 26 after the simulated user said "Only do scenes 2, 13 and 26 for now". Your own breakdown of The Catch was not touched.

## In short

**All three scenes finished clean: no errors and no warnings.** The final full check said "nothing needs you, no small fixes needed, no warnings". I re-ran that check myself on a copy of the test project and got the same.

**What it means for your idea:** a helper following the kit can now write a scene, fix what the checker prints, and end with nothing left. The problems left are smaller:
- a few instructions and handouts leave things out;
- the book still prints some numbers a reader can't use.

## One example: scene 13, the long scene

Scene 13 (the glass partition, the most talk in the film) became 22 beats and 39 shots, about 4 minutes. The kit split its design into two parts and a shot list, once, at the start. Then it handed out the shots in three batches of 13.
- Last time, each part of this scene showed errors that belonged to the next part (29 of them).
- This time, part 1 showed 5, and they cleared when part 2 was applied.
- At the end, the scene check printed nothing.

Those 5 are the last kind of "not yet due" problem still shown as errors (problem 1 below).

## The numbers

| | First test (entry 23) | Full run (entry 31) | Three-scene test (entry 35) | This test |
|---|---|---|---|---|
| Pieces of work | 40 | 180 | 50 | 48 |
| Errors before repair | many, mostly impossible to clear | 455 | 92 | 25 |
| Errors a piece was shown but could not fix | most of them | many | 43 | 5 |
| Warnings left on the scenes at the end | — | about 4 per scene | 1 per scene | 0 |
| Final full check | 44 problems | 1 error, 126 warnings | 1 error, 4 warnings | 0 errors, 0 warnings |

The scenes and helpers differ between tests, so this is a rough comparison. The direction is clear, though. This test's helper also fixed every warning it met along the way: three light lines in scene 2, four suspense holds in scene 13, and one light line in scene 26.

## The scenes

| Scene | Beats | Shots | Length | Most repair rounds |
|---|---|---|---|---|
| 2, the ladder climb | 9 | 11 | about 66 seconds | 1 |
| 13, the glass partition (split in two parts) | 22 | 39 | about 4 minutes 3 seconds | 2 |
| 26, the climax | 11 | 19 | about 1 minute 46 seconds | 1 |

## What still goes wrong, most important first

1. **A split scene's first part still shows errors for references to the second part's beats** (5 errors, "ID-02"). Step 7 tells part 1 to write the scene-level fields, and those point at part 2's beats. They should be "not yet due", like the other cases fixed in note 36.
2. **Records a later piece may not change force workarounds.** The helper got round three such cases, but this shouldn't be necessary:
   - A planned long hold needs a "saved choice" written in a certain form ("pause after = hold"). The film rules piece wrote a different form, which the template allows, and step 6 never says which form the check wants.
   - Two story secrets had the wrong people listed as knowing them (from the story plan step), so the suspense check flagged the scene 13 shots. The shot piece may not correct them.
   - A broken rung's state started on a later line than the shot showing it.
3. **A split scene's handouts leave things out.**
   - Part 2's handout doesn't show part 1's design fields, yet a field sent again replaces all its lines, so part 2 must re-send them from memory.
   - The shot-list piece's handout doesn't show the scene's beats, cameras or moves, which the list is built from.
4. **The book still has faults:**
   - numbers a reader can't use: "emphasis 2", "grey preview level 1", and "beat 17" when the book never lists the beats;
   - "floor-plan move 2" as a name;
   - one addition listed twice;
   - one-line entries that lose who acts. The one-line list now follows the written shot, but a shot's moments lean on its subject: "her finger draws down the shaft" reads as Iona's, but it is Saye's;
   - the recording shots in scene 13 don't say they are recordings, so people appear "in the room" in their scene 6 clothes, next to a 3 mm lens;
   - scene 26 calls its turns "another turn", "the second turn" and "the turn", in a confusing order;
   - some eyeline wording reads oddly ("eyes on down into the dark");
   - one state's name contradicts its shot.
5. **Place headings are still matched loosely.** Iona's room got no headings and another room got hers. A piece may not write headings, so the wrong ones stay.
6. **My own mistake from entry 36:** the step 4 example of a silent person's arc ("none: seen once, unchanged") is a form the kit refuses. **Fixed now:** step 4 shows the arc in the accepted form, the same at both ends, and I checked the kit accepts it.
7. **Smaller unclear points:**
   - a non-human's description length is 20 to 30 words in the template but 25 to 40 in the check;
   - the field guide says "only these scenes" is set at a different checkpoint from step 1;
   - the world step's handout again left out the mirror card;
   - each character's handout shows Iona's finished record as its example, which gives Iona's own piece the answer;
   - scene 26's handout says a saved push-in is allowed there, while the choice itself says "never in scenes 26 and 27";
   - the health check points to "05 How to read your breakdown" without saying it is in the kit's own folder;
   - the length check of step 2 is skipped while only some scenes are chosen;
   - the choices file lists small choices under "Big choices".
8. **Staging slips no check catches.** The helper found these itself:
   - a camera across the line between Iona and Eli;
   - a camera position the ledge's floor plan doesn't allow;
   - a move that starts before a line ends.

   A check comparing cameras, moves and shots would catch them.

## What was tested, and what was not

**Tested:**
- The whole kit from a new project to the book, for the planning and three scenes, by a helper that had seen none of the fixes.
- I re-ran the final full check on a copy of the test project: no errors, no warnings.
- I checked that the corrected arc form is accepted.

**Not tested:**
- The other 27 scenes.
- The whole-film pass, the scores and the other exports.
- A real person answering the questions.
- The chat apps, The Long Places, pictures and video.

**Unsure:**
- Two small tests in a row are still a small sample.
