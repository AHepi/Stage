# 42 Handover - what Stage should make, and why

Log entry 42 · 10 October 2026 · for whoever improves Stage next (you, or a Claude session in this repository).

**Read it with:**
- This repository (Stage), as of commit `5efb514`.
- *40 The Catch - production plan - revised kit*: the plan Stage made for The Catch (log entry 40).
- *02 Prompts - The Catch - H3 clips up to the elevator shooting.txt*: 36 clips for MiniMax H3, made by hand from that plan. In this note it is called **the clip file**, and it is the example of what Stage should make.
- *42 Reference code - H3 clip builder.zip*: the script that built the clip file and checks every prompt; its checks can be moved into Stage's checker.
- MiniMax's official H3 prompt guides and ComfyUI's H3 pages (links under Sources).

## 1. The short version

**What happened.** Stage made a plan of The Catch. Then I was asked to turn scenes 1 to 6 of it into prompts for MiniMax H3. You run H3 in ComfyUI on a rented computer. Almost nothing could go straight from the plan into H3:
- I rebuilt every prompt by hand.
- I fixed 18 places where the plan didn't make physical sense.
- I regrouped the plan's shots into 36 clips.
- I designed every picture H3 needs.

That is a factory's work, done by hand.

**Why.** Stage is a planning factory. Each step checks that the plan agrees with itself, and the line ends in a book. Making video is an add-on that has never been run against a real video model (item 43 of note 41). Some of its rules are the opposite of what H3 needs, and its checker enforces them.

The clearest case is stillness. For any held moment of 2 seconds or more, Stage requires a list of the body parts that "stay still". In H3, those words freeze people. That is the wooden look.

**What the output should be.** For each clip, one page that a person or a program can carry out without having to think. It gives:
- the start picture to make
- which pictures to connect, and in what order
- the prompt, in the model's own format
- the length to type
- what to check in the result
- which seconds to keep

Around those pages go one settings page for the tool you actually use, and the empty set pictures that every start picture is built from.

**The first job.** Before rebuilding anything, run a few clips on your real setup, Stage's current prompt against the new shape (W1 below). Then every change rests on what H3 does on your machine, not on anyone's notes, mine included. Nothing in this note has been run on H3 yet.

## 2. One moment, before and after

**Before: what Stage writes for H3 today.** On 10 October I ran `stage.py compile --scene SC10 --force-model minimax-h3` on the repository's saved scene 10 test project (`tests/fixtures/chat saved scene 10`). Here is the prompt for shot 150, the turn, "Not mint.", exactly as it came out:

```
Starting from the opening picture: The woman chews slowly, eyes on the other woman just right of the lens. At 00:04.750, the woman stops chewing; a small frown; chews once more, slowly. At 00:06.750, the woman says two words, unsteady. The woman (S1) speaks unsteady, <d>[English] Not mint.</d> At 00:08.750, the woman listens, does not speak; swallows once; eyes stay on the other woman. Her head, hands and torso stay still; only her eyes and mouth move. Her face and body show small, contained movements. It ends: still, mouth closed, eyes on the other woman. Close-up, at eye level. The camera holds a perfectly static shot [static]. The camera does not move. The sound of her chewing, close, then stopping. overall_soundscape: a small bare kitchen before dawn: the fridge's low hum, and nothing else. non_diegetic_music: none.
```

Its questions for judging the clip include "Do Iona's head, hands and torso stay still?" and "Does the camera stay still?".

The scene's other 17 prompts follow the same pattern. Across all 18:
- "stays still" appears 44 times.
- "The camera does not move." appears 18 times.
- "and nothing else" appears 18 times.
- No picture labels and no shot markers appear at all, although up to five pictures are attached.

Of the 191 questions for judging the clips, 72 ask whether something stays still.

**After: the shape the clip file uses.** This is clip 03 (plan shot 1-050), shortened; the full prompt is in the clip file.

```
subject_definitions:
<Subject 1> is the loading tunnel shown in <Picture 1>: a low arched tunnel of wet red-brown brick ...
<Subject 2> is Iona, a compact, strong-shouldered woman in her late thirties ... Her face, hair and build come from <Picture 2>, and she is the woman in the faded blue work shirt in <Picture 1>.
<Picture 1> is the shot-planning reference for [Shot 1]: it sets where the camera stands, the shot size, the set, the props, the light and where each person is at the first moment; ... the people move on from their places at once.

summary:
[reference generation] In <Subject 1>, <Subject 2>, Iona, kneeling at the elevator car's floor frame ...

retention_analysis:
<Subject 2> (appears in [Shot 1]): partially_preserved - Iona's face, hair and build from <Picture 2> are kept exactly; ...

detailed_description:
The target video is photographic live action ... This clip is one single continuous shot from start to finish. The shot is static, on a tripod, with no camera movement whatsoever. ... Iona is alive in every second of this clip, during and between the actions below: her chest rises and falls, her eyes make small movements, and her weight settles on her knees; she blinks at about 00:01.200, 00:05.800 and 00:08.800. ...
[Shot 1] ... For the first two seconds Iona takes one long breath in through her nose; her shoulders rise and stay high. At about 00:02.200, <Subject 2> (S1), in a low-middle, slightly rough voice ..., says to the brackets, her eyes on them the whole time: <d>[English] The safety brakes are gone.</d> When she finishes her lips close, and her held breath goes out slowly through her nose; her shoulders come down. Above her, Jude's hands stop mid-turn ... his right thumb rubs slowly along the wire, once. ... From 00:08.600 to the end ...

overall_soundscape:
Water drips onto brick and the factory's low hum sounds far above. ...

non_diegetic_music:
N/A
```

**What changed, and why**

| Stage writes | The clip file writes | Why |
|---|---|---|
| "Her head, hands and torso stay still" | Each person is "alive in every second": breath, eyes, weight, blinks at stated times. Held time is filled with small timed actions. | Testers found that lines about not moving freeze faces, and that time with nothing in it gets frozen or cut short (h3-storyboard notes). |
| "holds a perfectly static shot [static]. The camera does not move." | One camera sentence, in the wording testers found works | Extra camera lines made cuts drift and the camera move (h3-storyboard notes). |
| "does not speak", "and nothing else", "music: none" | Only what is there; "N/A" for music | In ComfyUI, H3 has no negative side, so naming a thing adds it (ComfyUI prompt guide). MiniMax's guide uses N/A. |
| One paragraph in Stage's own order | Six sections in MiniMax's order, with a numbered label for every picture connected | In ComfyUI, H3 gets no rewriting step and reads the prompt as written. MiniMax's guide shows the form that step would produce. |
| "the woman" (a rule called "motion only") | Each person's full description, word for word, tied to their picture's label | In reference mode a picture is tied to a person only through its label. Rewording a description re-rolls the face. |
| One clip per shot; lengths in seconds, with spare time at both ends | Clips of one to three shots, on H3's own lengths, with a tail to throw away | A cut resets a face and lets each shot hold one beat. H3 breaks up in its last 1.2 to 1.7 seconds, so spare time at the end is unusable. |
| Pictures of the empty place and of each person | One start picture per clip, built from empty set pictures | H3 takes the camera position, the number of people, their eyes and the light from the picture more than from the words. |
| "Does X stay still?" | "After her line, Jude's hands stop, then his thumb rubs the wire. If both go stiff, run another seed." | Checks should catch known failures, not reward them. |

## 3. Why Stage's output doesn't work, and where in the code

1. **Stillness is required, written and checked.** One untested judgement runs from the research library all the way into the result checks:
   - **The rule** is library D15, rule 8: "If a hold is 2 s or longer, then name every still part and the one moving part, and add 'The camera does not move.'" It is marked [J]: a judgement nobody tested.
   - **The checker** turns it into check CRAFT-26 in `checks_craft_reasons_words.py`, set by `hold_needs_still_s` (2.0 seconds) in `rules/constants.json`. Step 8's self-check asks: "Is anything left to move that should be written as still?"
   - **The compiler** writes it: `phrasebook.json` holds "{Whose} {parts} stay still." and "small, contained movements", which `compile_prompts.py` uses at about line 1486. It asks about it again at about line 2256.
   - **The plan you gave me shows the result.** Plan shot 1-050 has "still: head, torso, hands", then "moment 5-10: his hands stop on the wire; neither of them moves".

2. **Sentences that say what isn't there.** "The camera does not move.", "nothing else", "music: none", "does not speak". ComfyUI's H3 templates run with no negative side, so every named thing is something to show.

3. **The prompt isn't in the model's format, and it ignores where the model runs.** Stage's H3 entry ("minimax-h3" in `adapters/video_models.json`) has one prompt order for every way of running H3.
   - On MiniMax's own service, a rewriting step (H3-Context-IR, mentioned in library C3) turns a short prompt into a long structured one.
   - In ComfyUI there is no such step. The prompt must already be in that long form: the six sections of MiniMax's reference-mode guide, with a label for every picture connected.
   - Stage's pages attach up to five pictures and never name them in the prompt.

4. **A rule forbids describing people when a start picture is attached.** It appears as library C3 rule R1, in card 21 ("Fix: motion only, 'the woman'"), and as check GEN-05, which is an error. That fits services that copy the first frame and animate it. It is wrong for H3's reference mode, where each person's description should be repeated, word for word, next to their picture's label.

5. **The shot is the unit; the clip should be.** Stage's default is one shot per clip (card 21), and the scene 10 compile made exactly that, splitting only long shots. Its lengths are seconds, with 0.75 seconds spare at each end (`handles_s`). The testing notes point the other way:
   - **Shots grouped into clips.** Short shots cut together inside one clip each hold one beat, and a cut resets a stiffening face.
   - **Collisions need a cut.** The cut-on-contact fix needs two shots in one clip.
   - **Facing angles need care.** Two people filmed facing each other need either a two-shot first in the same clip or a clip each.
   - **Lengths.** In ComfyUI, H3 runs only on fixed frame lengths (17 × k + 5), and its last 1.2 to 1.7 seconds break up. The spare time at the end is lost; a tail has to be planned and thrown away.

6. **Most clips get no start picture.** Scene 10 shot 010 attaches only reference pictures: the empty kitchen and each person. H3 then has to invent where the camera is, where people stand and how bright it is.

7. **The plan has physical mistakes that no check catches.** Some from the kit, all fixed by hand in the clip file:
   - The shaft is 2.4 metres square around a 2-metre car, which leaves about a hand's width to climb in.
   - Iona's torch is "a heavy black metal flashlight about 30 centimetres long", which she holds in her teeth while climbing.
   - A rung held at both ends "rolls like a rolling pin".
   - A line is spoken "round the torch", with the torch clamped in her teeth.
   - A strap is cut with nothing to cut it.
   - Men take cover from overhead shots under an open grid roof.
   - A weak man holds a big man up.

   The clip file's section 3 lists all of them. Note 41 already names the gap (items 3 and 5).

8. **Collisions written as cause and effect inside one shot.** "She swings it into the window; the glass cracks." Testers found video models can't reliably make one thing break or push another at the moment of contact. The fix is to cut at the contact and start the next shot with the result already there.

9. **Nothing has ever been made.** About 90 checks prove the plan agrees with itself; none asks whether a clip will move. Rough drafts are planned on a different, cheaper model (scene 10: "2 cheap drafts on Veo 3.1 Lite", "on Wan 3.0 at 480p"). A draft on another model says nothing about how H3 will behave.

10. **The pages don't fit your tool.** They name hosted services ("Hailuo app, MiniMax API, fal, Runway...") and set "2k". Your route is ComfyUI's Reference to Video template, whose own size is 1344 × 768. The pages need that template's own setting names: the Duration box, the order the pictures plug in, Lightning, seed, ref_image_size.

## 4. What the output should look like

The finished product is a **clip book** for one route. A route is a model plus the place it runs; build "MiniMax H3 in ComfyUI, Reference to Video" first. The clip file is a working example of a clip book. Its parts, and why each is there:

| Part | What it holds | Why |
|---|---|---|
| Settings page | The route's settings, named as the tool names them: Lightning off, size, length box, picture size, seed, steps | One wrong setting (Lightning on, or the template's small preview size) undoes everything else. |
| Look block | One paragraph pasted first in every picture prompt | Every picture shares one look. |
| Master pictures | Each place, empty, made once | Start pictures built from the same set keep it the same from clip to clip. |
| Clip pages, one per clip | The form below | One page is one job; nothing has to be looked up elsewhere. |
| Shot map | Each plan shot: which clip, which seconds | The edit is put together from it. |
| If a clip goes wrong | Symptom, then the first thing to change | Testers found speech faults follow the seed, so the seed changes before the words. |
| Take log | Each run's seed, settings, result and verdict | The route's rules get tested on real clips. |

**A clip page:**

```
CLIP 03 - The safety brakes are gone
Scene 1 - plan shot 1-050 - one shot
Length: 277 frames (11.54 seconds). Type 11.5 in Float (Duration).

START PICTURE   which master picture and character pictures to give the picture tool,
                and the prompt (look block first): camera place, who is where, what
                hands touch, eyes on the task, mouths closed
CONNECT         ref_image_0: start picture -> <Picture 1>
                ref_image_1: Iona picture  -> <Picture 2>
                Connect nothing else.
H3 PROMPT       the six sections, between COPY FROM HERE and COPY TO HERE
CHECK           what must happen, what failure looks like, what to change first
KEEP            seconds 0 to 10.0; plan shot 1-050 = seconds 0 to 10.0
```

**Rules every H3 prompt for this route follows** (the clip file's builder checks most of them in code):
- **Sections:** the six sections in MiniMax's order, each starting on its own line.
- **Picture labels:** one `<Picture N>` per picture connected, numbered in connection order.
- **The place:** `<Subject 1>` is the place.
- **People:** each person is a numbered subject with their full description, word for word.
- **Start picture:** `<Picture 1>` is defined as setting the camera, the set, the light and where people are at the first moment, and nothing about their poses.
- **Opening lines:** before `[Shot 1]` come one style sentence, the number of shots and the cut times, one camera sentence, who is in the clip, and the "alive" sentence with blink times.
- **Shot times:** they rise from 0, and each shot after the first opens with its time ("At 00:04.500, the camera cuts to...").
- **Shot content:** one main change of face per shot. Held time is filled with countable small actions. A hand that moves a thing is the subject of the sentence and stays on it.
- **Speakers:** numbered in the order they first speak. The spoken words come word for word from the approved captions, inside `<d>[English] ... </d>`. Off-screen voices are marked, with the on-screen person's lips closed.
- **Banned outside the spoken lines:** still, freeze, nothing, nobody, never, not, no (except "with no camera movement whatsoever"). Also comparisons such as "like a man noticing rain", which H3 may draw, and talk about speaking ("says two words", "sentence"), which H3 may say aloud.
- **Sound:** an overall_soundscape always; non_diegetic_music: N/A.
- **Length:** about 350 to 500 words in detailed_description, and the clip's frames on the 17 × k + 5 grid.
- **The tail:** at least 1.3 seconds after the last kept second, with one "From ... to the end" line of small actions so the tail isn't empty.

## 5. The factory, station by station

Each station takes something in, does one job, and hands on something the next station can use without asking. Each has a test that proves it worked.

| # | Station | Takes in | Does | Hands on | Proven by |
|---|---|---|---|---|---|
| 1 | Plan (steps 0 to 7, as now) | The story | Scenes, beats, turns, lines, people, places, states | The plan | Today's checks |
| 2 | Physical sense (new, inside steps 4 and 8) | The plan's sizes, props and actions | Checks that bodies fit, reach, hold and act as written | A plan a real body could perform | It flags the 18 slips in the clip file's section 3 |
| 3 | Actions (step 8, changed) | Each shot | What each body does, second by second, with held time filled | Timed actions, with no lists of what doesn't move | No stillness lists anywhere |
| 4 | Clips (new) | Shots and actions | Groups shots into clips; cuts at contact; sets lengths on the route's frame grid, plus a tail | The clip list | Scene 1 comes out close to the clip file's clips 01 to 08 |
| 5 | Pictures (new) | The clip list | Master set pictures; one start picture brief per clip; the checklist | Picture prompts | Every clip has a start picture brief |
| 6 | Compile (changed) | Clips, pictures, the route | Writes each prompt in the route's format and runs the route's own checks | Clip pages | Passes the route's checks |
| 7 | Test run (new) | Three clip pages | Runs them on the real setup and logs the results | Rules marked confirmed or wrong for this route | Before the rest is compiled |
| 8 | Make and keep (step 14, changed) | Clip pages | Takes, seeds, keep times, tails trimmed | Kept clips | Take log |
| 9 | Edit (step 15) | Kept clips and the shot map | Joins the kept parts | The film | The edit timeline |

## 6. Work list, in order

Each item ends with how to tell it's done.

**W0. Set up the project's own files**, as you ask in every project:
- **Decisions:** every decision, in its own words.
- **Lessons:** only times the work itself failed and was fixed.
- **Status:** where the project stands.
- **Glossary:** the terms from the authority documents, with where to find them.
- Add these W items to note 41.

*Done when:* the three files exist and note 41 lists W1 to W12.

**W1. Test run first.** On your rented computer, make three clips at the small test size (1152 × 480), two seeds each, each as Stage writes it today and as the clip file writes it:
- **A held turn:** clip 03, plan shot 1-050.
- **A collision:** clip 21, the window.
- **A two-person exchange:** clip 04 or 07.

Log every run in the take log.

*Done when:* the take log holds 12 runs, and every rule in section 4 is marked confirmed, wrong or unclear for this route. Rewrite the later items from what the runs showed.

**W2. Stop asking for stillness.**
- Turn CRAFT-26 round: a held moment of 2 seconds or more needs at least one timed action every 2 seconds.
- Take the stillness and "contained movements" sentences out of the compiler and the result questions.
- Rewrite library D15 rule 8 and card 06's "Display and stillness" part, saying why.

*Done when:* compiling scene 10 for H3 gives no "still" sentences and every held moment has timed actions.

**W3. Only say what is there.** Run every sentence about what is absent through the existing rewriter (`rewrite_negations` in `compile_prompts.py`) or drop it. Write music as "N/A".

*Done when:* no H3 prompt holds not, no, nothing, never or none outside the spoken lines, apart from "with no camera movement whatsoever".

**W4. Routes, not only models.** Split the H3 entry into "hosted, with the rewriting step" and "ComfyUI Reference to Video, without it". Give the ComfyUI route:
- its sizes: 1536 × 640 for a 2.39 film, 1152 × 480 for tests
- its frame grid: 17 × k + 5, from 124 to 362 frames
- a tail of at least 1.3 seconds
- seeds, and the template's own setting names
- the seconds to type for each length

*Done when:* a clip page for this route names only boxes that exist in ComfyUI's "MiniMax H3 R2V" template, and every length typed lands on the intended frame count.

**W5. Compile in MiniMax's reference format** for that route, following section 4's rules. Turn GEN-05 ("motion only") off on this route. Port the checks listed in section 4 into the route's checker.

*Done when:* Stage's compile of scenes 1 to 6 has the clip file's structure, clip for clip. The wording may differ.

**W6. Clips as the unit.** Add a step that groups one to three shots into a clip:
- **Where they can share a clip:** the same place and people, cut along roughly the same line, or an insert.
- **Facing angles:** two people facing each other get either a two-shot first in the same clip or a clip each.
- **Time:** the clip's lengths and tail come from the route.
- **The record:** a shot map back to plan shots.

*Done when:* scene 1's twelve plan shots become about eight clips, close to the clip file's clips 01 to 08.

**W7. Start pictures.** Master set pictures for each place, empty. One start picture brief per clip, showing the clip's first moment:
- eyes on the task, mouths closed
- hands already on what they will move
- only the people who appear
- props in their current state

Add the checklist from the clip file's section 6.7.

*Done when:* every clip page has a start picture brief that names its master picture and character pictures.

**W8. Physical sense checks.** Use code where the plan has numbers: room for a body (about half a metre to pass, more to climb), reach, which way a door swings against a brace, cover from above, one thing per hand. Use questions where it doesn't: "Can a person hold this in their teeth?", "What does she cut it with?".

*Done when:* run on the kit, they flag every slip in the clip file's section 3. That list is the test.

**W9. Cut at contact.** A shot where one thing breaks, pushes or trips another is split at the moment of contact, and the next shot starts with the result already there. The sound goes on the cut. Two shots that cut together must differ clearly in size or angle, because testers found H3 tends to blend a cut between similar framings into one continuous move.

*Done when:* the kit's window, strap and trip come out as the clip file's clips 21, 22 and 28.

**W10. Questions that catch real failures.** Replace the "stays still" questions with these:
- Does each person move between the written actions?
- Is each line said once, by the right mouth?
- Does each cut land within about a second of its written time?
- Is the tail trimmed?
- Does a collision happen across a cut, not on screen?

*Done when:* none of the questions rewards stillness.

**W11. The take log teaches the rules.** A rule marked [J] stays a suggestion until the take log confirms it on that route. Only then may a check enforce it. A rule the log shows is wrong is dropped, with a note.

*Done when:* the route's rules each carry a confirmed, wrong or unclear mark with the takes that decided it.

**W12 (later). Send clips straight to ComfyUI.** ComfyUI on a rented computer can take a prompt and pictures through its web address and hand back the clip (note 41, item 35). A cloud session like the one that wrote this note can reach web addresses; a real ComfyUI connection is untested.

*Done when:* one clip page runs from Stage to a downloaded clip with no copying by hand.

## 7. Keep these: they work

- The story numbered line by line. The approved lines, word for word, checked against the captions.
- Fixed descriptions and states (Iona with the chipped tooth, and so on), pasted word for word.
- The prompt word swaps: flashlight for torch, IV pole for drip stand, elevator for lift.
- Dated model facts with marks for verified, unverified and judgement. W11 builds on these marks.
- The one-piece-at-a-time loop, the take log, rights and privacy.

## 8. Two questions for you, each with a ready answer

1. Which route should be built first? **[MiniMax H3 in ComfyUI, Reference to Video]**
2. May a clip hold up to three shots? **[yes]**

## 9. Word list

| Word | Plain meaning |
|---|---|
| Clip | One run of the video model. Here it holds one to three shots, or part of one long shot. (Stage's word list says a clip is a piece of one shot; this note widens it.) |
| Shot | One piece of film between two cuts, as in Stage. A clip can hold cuts. |
| Plan shot | A shot as numbered in Stage's plan, such as 1-050. |
| Route | A model and the place it runs, such as "MiniMax H3 in ComfyUI, Reference to Video". |
| Rewriting step | A program on MiniMax's own service (H3-Context-IR) that turns a short request into a long, structured prompt. It is missing in ComfyUI. |
| Reference mode | H3 working from pictures you connect. ComfyUI's template for it is "Reference to Video". |
| Start picture | The still you make for a clip, showing its first moment. The prompt calls it `<Picture 1>`. |
| Master picture | An empty set picture, made once per place; start pictures are built from it. |
| Character picture | Your picture of one person, giving H3 the face. |
| Look block | The paragraph pasted first in every picture prompt. |
| Clip page | One clip's complete job: start picture, connections, prompt, length, checks, keep times. |
| Clip book | All the clip pages for one route, with its settings page, master pictures and shot map. |
| Tail | The extra second and a half at the end of a clip, made to be thrown away because H3 breaks up there. |
| Contact cut | Ending a shot as one thing reaches another, and starting the next with the result already there. |
| "Alive" sentence | A line saying each person breathes, moves their eyes and shifts weight throughout, with blink times. |
| Test run | A few real clips made on your own setup to confirm or reject a rule. |
| Take log | The record of every run: seed, settings, result, verdict. |
| Seed | The number that makes each run different. |
| Negative side | A second, "avoid this" prompt. ComfyUI's H3 templates have none. |

## 10. Sources

- [MiniMax H3 prompt guide, reference mode](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md)
- [MiniMax H3 prompt guide, base mode](https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md)
- [ComfyUI: MiniMax H3 prompt guide](https://docs.comfy.org/tutorials/video/minimax/minimax-h3-prompt-guide)
- [ComfyUI: MiniMax H3 templates and settings](https://docs.comfy.org/tutorials/video/minimax/minimax-h3-native)
- [h3-storyboard testing notes](https://github.com/phileiny/h3-storyboard-skill)
- In this repository: library D15 and C3, card 21, `checks_craft_reasons_words.py` (CRAFT-26), `checks_plan_generation_film.py` (GEN-05), `compile_prompts.py`, `adapters/video_models.json`, `adapters/phrasebook.json`, `rules/constants.json`.

## Traps

- **Untested in both directions.** Neither Stage's prompts nor the clip file's have been run on H3. Do W1 before rebuilding, or the work rests on notes, not results.
- **A [J] rule enforced as fact.** The stillness rule began as a judgement and became a check. A new rule from this note can go the same way. Keep it a suggestion until the take log confirms it.
- **The same model, different routes.** H3 on MiniMax's service and H3 in ComfyUI need different prompts. Never share one prompt between them.
- **Drafts on another model.** A cheap draft on another model says nothing about H3. Draft on the same route at a smaller size.
- **The checker can push the wrong way.** If a check demands something the model handles badly, a clean health check means a worse clip. Judge checks by clips, not by the number of warnings.
- **Spare time at the end of a clip is lost to the tail.** Don't plan cuts or lines into the last 1.3 seconds.
- **The repository is public.** The clip file and its reference code hold lines and descriptions from The Catch. Stage's own rule keeps stories out of git; keep these out too, unless you choose otherwise.
- **Example scene 10 is shared by many tests.** Changing how it compiles will break tests that compare against it. Update the tests and the example together.
