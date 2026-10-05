# Stage - project story

Last updated: 5 October 2026 (log entry 35).

## The goal

Build a kit that turns a screenplay or a prose story into a scene-by-scene plan for making it as a film, including with AI picture and video tools. The plan is called the **breakdown**. For every scene and every shot, it says what we see and hear, and why.

- **The output is the breakdown.** It can later be plugged into an image generator, a video generator, or a longer production pipeline.
- **Storyboards are optional**, and so are 3D mock-ups and video prompts.
- **Anyone who can use an AI chat app must be able to run it.** It has to be easy for you and exact enough for an AI to follow.

The film craft behind it comes from research: dialogue, scenes, camera, light, composition, symbols, character design, editing and sound, starting from Robert McKee's *Dialogue*.

## Where things stand

**Built and uploaded:**
- Everything is on the branch `claude/screenplay-video-pipeline-5j08tw` of your GitHub repository "Stage".
- The kit is a Claude skill with its own checking program. It also comes as a bundle for ChatGPT and Gemini, with setup guides for each app.
- There is one finished model scene (The Catch, scene 10, Saye's kitchen) and its 3D mock-up.

**Tested:**
- The automatic tests pass in 18 of 19 groups. The failing group is a size target, explained under "Known issues".
- A fresh AI with only the kit planned the whole of The Catch and broke down three scenes (entries 23 to 25). Its 36 problems are fixed.
- **The whole of The Catch, all 30 scenes, from start to finished book (entries 28 to 31).** It made 514 shots and about 43 minutes of film. 29 of 30 scenes pass the kit's own scoring. The run also found 18 groups of problems, listed in `Project notes/31 Test - The Catch - full run.md`.
- **All 18 problem groups are fixed, and the fixes were cross-examined (entries 32 to 34).** A second helper tried to prove the fixes wrong and found five that went too far. Those are repaired too. Re-checking The Catch's finished breakdown now gives no errors and 37 warnings (126 before), and "what's next" says "Finished". Only the handouts for the biggest scenes are still a little too large to read in one go.

- **The fixed kit on new writing (entry 35).** A fresh helper planned The Catch from scratch and wrote scenes 2, 13 and 26. Each scene ended with one warning: one was the helper's own slip, two were false alarms. None of the old rule arguments came back.

**Not tested yet:**
- The other 27 scenes with the fixed kit.
- A real person answering the questions. In the tests, the answers were always "defaults" and "no changes".
- The Long Places (you asked to leave it for later).
- The chat-app route in the real ChatGPT and Gemini apps. It is designed and bundled, but was only simulated here.
- Actually making pictures, videos or voices. This computer has no accounts for those services, so the prompt packs stop at "ready to send, checked and priced".

**Known issues:**
- **The Catch still has 37 warnings.** They are real points in its records (for example 8 light moments with no light cue), not faults in the kit. They can only be cleared by redoing those scenes through the kit's steps.
- **The light check reads words.** A change of light written in words it does not know would slip through.
- **The three-scene test's list (entry 35):**
  - some checks still show errors that belong to a later piece of work;
  - an error about the video-model prices date appears before any step fills it;
  - two false alarms;
  - "pause after: none" is refused;
  - the book's one-line list can contradict the full shot;
  - the planning steps are still unclear in places.
- Three of the chat-app files are 26% to 49% longer than the blueprint aimed for. This may matter in Gemini, because Google does not publish how much a Gem can hold.
- The start page's "last checked" line only updates at the next save, not straight after a check.
- The repository is public, so the quoted passages from both stories are public (entry 19).
- No pull request yet: the repository has no main branch to merge into.

## How the pieces fit

**An example first.** You put The Catch in "My stories" and type "Break down my story."
1. The AI reads the skill's house rules.
2. It runs the checking program's `new` command, which makes the folder "My breakdowns/The Catch" with a start page.
3. It runs `read`, which numbers every line of the script and finds its 30 scenes.
4. From then on the AI works in small pieces. The `next` command hands it one piece at a time, with only the knowledge, records and story lines that piece needs.
5. The AI writes its part of the breakdown. `apply` saves it into your numbered files, and `check` looks for problems. The AI fixes them, at most three times, then tells you in four short lines what it did.
6. A few times it stops to ask you something, such as the film's length or the big creative choices. Each question comes with a ready answer, and "defaults" accepts them all.
7. At the end, `export` makes the readable book, a shot list spreadsheet, captions and an edit timeline.

**The parts, and what each hands on:**

| Part | Where | What it does | What it hands on |
|---|---|---|---|
| Research library | `.claude/skills/breaking-down-stories/library/` | 32 fact-checked files on film craft and AI tools, each with a short summary | The rules, numbers and examples the cards are made from |
| Knowledge cards | `.../cards/` (24 files) | The research boiled down to working rules, traps to avoid, and good and bad reasons in pairs | The craft each piece of work needs, cut to size |
| Step files | `.../steps/` (17 files) | What to do at each of the 12 steps and the 4 add-ons, with a version for chat apps that cannot run code | Instructions for each piece of work |
| House rules | `.../SKILL.md` | How the AI works, talks to you and saves | The loop the AI follows every time |
| Data format | `.../schema/`, `.../rules/` | 47 kinds of record and 576 fields, each with a plain meaning, plus every number the checker uses | What a correct breakdown looks like |
| Checking program | `.../tools/stage.py` and `stage_tools/` | Reads stories; numbers lines; checks about 90 things; works out timings, sides and camera distances; builds handouts; exports; estimates cost; writes video prompts; builds 3D mock-ups | Checked, readable files |
| Templates and model scene | `.../templates/`, `.../examples/` | Empty forms, and the finished scene 10 | A model to copy |
| Guides and bundles | Repository top: `01` to `09` | How to start in each app; the chat-app bundle; the skill file for Claude; the example folder | What you open first |
| Project notes | `Project notes/` | The blueprint, the test reports, the fix notes and the cross-examination | The record of how it was built and tested |

## Word list

| Word | Plain meaning |
|---|---|
| Breakdown | The full plan: every scene and shot, what we see and hear, and why. |
| Scene | One continuous place and time in the story. |
| Beat | One action and the reaction it causes, such as "Saye tests; Iona fails". |
| Turn | The moment a scene changes direction, such as "Not mint." in scene 10. |
| Shot | One continuous piece of film between two cuts. |
| Clip | One piece a video model makes. A long shot may need several clips. |
| Take | One attempt at making a clip. |
| Reason | Every shot says what it is for and which story line, object or rule justifies it. Moods alone ("to build tension") are refused. |
| Record | One entry in a breakdown file, such as one shot or one character. |
| Card | One knowledge file for the AI, such as "Camera" or "Dialogue on screen". |
| Step | One of the 12 stages of the work, from "Start" to "Book and exports". |
| Piece of work (unit) | The small job the AI does in one reply. |
| Handout | The single file the AI reads for one piece of work. |
| Checker | The program that checks the breakdown and says exactly what to fix. |
| Checkpoint | A moment when the AI stops and asks you something, always with a ready answer. |
| Depth | How much detail: quick, standard (the usual) or detailed. |
| Scope | Which scenes to work on for now, such as "Only do scenes 2, 9 and 16 for now". |
| Fixed description | The exact words that describe a character every time a picture of them is made, so they look the same in every shot. |
| Reversed (mirror world) | In The Catch, things that are turned look back to front on screen. The kit works out which side everything appears on. |
| Camera rule | A rule for how the camera treats one character, such as keeping Eli's close-ups for scene 13. |
| Saved choice | A strong camera choice rationed across the film, such as the extreme close-up. |
| Set plan | A floor plan of a place in metres, with marks for where people stand. |
| 3D mock-up (grey preview, previs) | A plain grey 3D version of a shot, made in Blender, to check framing and movement. |
| Storyboard | Sketch pictures of the shots. Optional. |
| Prompt pack | The words and settings to send to a video model for each shot, checked and priced. |
| Model facts | A dated file of what each AI video model can do and what it costs. It needs refreshing every 30 days. |
| Skill | An add-on that Claude loads when you ask it to do a certain job. |
| Chat kit | The files you upload to ChatGPT or Gemini to use the kit there. |
| Blender | Free 3D software. The kit drives it to make the mock-ups. |
| Helper | A separate AI worker I started to research, build, test or review part of the job. |
| Fact-check | A second helper checking the first one's work against sources and fixing mistakes. |
| Fuzz test | Feeding a program strange input on purpose, to find crashes. |
| Usage limit | A cap on how much AI work this session can do in a few hours. Work pauses until it resets. |
| Repository | The project's folder on GitHub. |
| Branch | A separate line of work in the repository. |
| Pull request | A GitHub page proposing that one branch be merged into the main line. |
| Sequence | A group of scenes that belong together, such as scenes 1 to 3. The kit works through the film one sequence at a time. |
| Error | A problem the checker says must be fixed before going on. |
| Warning | A problem the checker only points out. It does not stop the work. |
| Scoring (rubric) | The kit's scoresheet: 10 questions per scene, each scored 0 to 3. A scene passes at 20 of 30. |
| Ladder | The film's plan for how close the camera gets at each scene's turn, so the film builds toward its climax. |
| Jump cut | A deliberate cut between two shots taken from nearly the same place, so the picture seems to jump. |
| Insert | A close shot of a hand, an object or a screen, cut into a scene. |
| Command safety checker | The automatic check in this session that approves or blocks each command before it runs. |
| Cross-examination | A second helper, which did not do the work, trying to prove it wrong. |
| Locked record | A record you approved. It cannot change unless you answer a question that unlocks it. |
| False alarm | A warning about something that is not really a problem. |
| Effort | How long and how carefully a helper thinks before answering. "Highest" (xhigh) is the slowest and most careful. |

## Numbered log

1. **Received your three files and an empty repository.** The files were The Catch (a screenplay of 1,852 lines), The Long Places (a novella of 49,152 words in 14 chapters) and McKee's *Dialogue* as an e-book.
2. **Turned the McKee e-book into plain text, one file per chapter.** The e-book's internal file numbers run one off from its chapter numbers, so they were matched by title.
3. **Installed Blender's 3D engine, to test controlling the camera.** The first attempt failed because a graphics library was missing. Installing it fixed that, and a test picture rendered in under 3 seconds.
4. **Researched 14 subjects, each written by one helper and fact-checked by a second.** The subjects were dialogue as action, scene design and beats, script breakdown and adaptation, editing and sound, camera, light and colour, composition and staging, symbols and design, character design, AI video models, AI pictures and consistency, writing video prompts, Blender previs, and earlier systems. After 16 to 28 corrections each, all scored 8 to 8.5 out of 10.
5. **Failure: the session's allowance of 200 web searches ran out during fact-checking.** Later checks opened known pages directly instead.
6. **Failure: the usage limit stopped 4 fact-checks.** They were re-run after it reset.
7. **Privacy lapse.** One fact-checker put your email address in the label of one batch of requests to Wikipedia. It stopped at once, I told you straight away, and every helper since has had an explicit rule against it.
8. **The research came out far longer than asked:** 10,000 to 20,000 words per subject, 235,000 in all. Each file got a short working summary so later helpers could use it.
9. **Found and fixed mistakes in a 3D mock-up kit a research helper had built.** Its fact-checker found bodies passing through walls, a falling cage that stalled and then sped up, and wrongly encoded depth pictures.
10. **A completeness check found 18 gaps, 31 disagreements between files, and 25 words used inconsistently.** The worst disagreements were about scene numbering, the mirror world, and where scene 13 turns.
11. **Researched the 18 gaps**, including chat apps, adapting a whole work, voices, rights and disclosure, visual style, visual effects, judging a breakdown, post-production, music, genre, action, on-screen graphics, cost and schedule, story formats, performance, film structure, places, and captions. The usage limit paused this twice.
12. **Three designers each designed the whole pipeline:** one for ease of use, one for film craft, one for reliability.
13. **Three judges scored the designs, and the best parts were merged into one blueprint.** The reliability design scored highest (56, 56, 58 out of 70). Two critics then found 84 problems, all handled. File: `Project notes/13 Blueprint - how Stage is built.md`.
14. **Found that your GitHub repository is public, and asked you about it.** You chose to make it private (see entry 19).
15. **Built the data format: 47 kinds of record and 576 fields.** A second helper broke it on purpose in 15 ways, and its test caught all 15.
16. **Built the written guidance.** That meant 24 knowledge cards (about 42,000 words), the house rules and 17 step files, each reviewed for film craft and plain language. The usage limit paused this once.
17. **Built the code:** the story reader, the checker, handouts, the readable views and exports, the cost estimate, video prompt packs and 3D mock-ups. Also a hand-built model scene (The Catch, scene 10).
18. **You asked for two code reviewers, so I switched from one to two.** Between them they fixed dozens of bugs, and all 17 test groups passed.
19. **You asked me to upload even though the repository is public, and I did.** I could not open a pull request, because the repository has no main branch.
20. **You asked me to use fewer helpers.** I cut the test plan to one test on The Catch, and The Long Places waits, at your request.
21. **Fixed the reviewers' leftovers myself.** A fuzz test had found that the video-prompt code froze on an absurdly long shot; that shot is now refused with a plain note. One fix I tried (refreshing the start page after a full check) broke the protection on locked records, so I undid it.
22. **Wrote the guides and app bundles:** read me first, Claude, ChatGPT, Gemini, reading your breakdown, the word list, the chat kit and the skill file.
23. **First real test: a fresh AI with only the kit worked on The Catch.** It did the whole-film planning, then scenes 2, 9 and 15. The craft was good, but the code's bookkeeping had 36 problems. File: `Project notes/23 Test - The Catch - first run.md`.
24. **Wrote a fix list with a decision for each problem.** File: `Project notes/24 Fix list - after the first test.md`.
25. **Two helpers applied all 36 fixes.** On the tester's project, problems went from 44 (most of them impossible to clear) to 13, all clearable with plain instructions. The whole-film summary went from 23,717 words to 5,940. Tests: 18 of 19 groups pass, and the failing one is the chat-app size target.
26. **Wrote this project story.**
27. **Mistake: I told you Sonnet 5.5 was not available.** You asked for the scene work to run on Sonnet 5.5 (a faster, cheaper model), with the planning and the analysis on the main model. I wrongly said Sonnet 5.5 did not exist. You asked again. I checked, it does exist, and I apologised. A small helper on Sonnet 5.5 ran fine before the real run started.
28. **Started the full run of The Catch.** One helper on the main model did the planning: your steps 1 to 7. Then 10 helpers on Sonnet 5.5 did the scenes, one group of scenes each. One more on Sonnet 5.5 did the finish: the whole-film check, the scores, the cost and time, and the book. The "user" was simulated and answered "defaults" to every question.
29. **Failure: the kit wrote into its own example folder.** A scene helper ran two commands from the Stage folder without naming the project, and the tool picked the example folder (The Catch, scene 10) and rebuilt it. The helper tried to undo it, but the command safety checker blocked that. I restored the example folder, and changed the tool so that from the Stage folder it never picks the example. I also fixed one test that depended on the old behaviour. Tests: 18 of 19 groups pass, the same as before.
30. **Failure: the command safety checker stopped working, and the run stopped at scene 24.** No commands could run for many hours. When you said "Go", the run picked up where it stopped, without redoing finished work.
31. **The full run finished, and I analysed it myself (as you asked, not Sonnet).** The results:
    - 180 pieces of work, 514 shots and about 43 minutes of film.
    - The book is 15,112 lines, with a shot list, captions, audio description and edit timelines.
    - 29 of 30 scenes pass the scoring. Scene 30 fails by one point because it runs long and asks the video model to draw words.
    - The final check left 1 error, which nobody can clear, and 126 warnings.
    - The cost to make the film with today's video models is $2,742 to $11,445.
    - The book reads well and follows the script shot by shot. But it prints internal names like "CAMSYS", and in one place it calls Jude Iona's "husband", which the script never says.
    - The 10 scene helpers logged 254 problems and unclear instructions. I grouped them into 18 groups, each with a fix. The worst are a code slip that hides jump cuts, an error nobody can clear, and checking rules that contradict the film's own plan.
    - File: `Project notes/31 Test - The Catch - full run.md`.
32. **Fixed the 18 problem groups, with one helper at the highest effort, as you asked.** The helper also added a test for each fix, rebuilt the chat kit and re-checked The Catch's finished breakdown. The results:
    - Errors went from 1 to 0 and warnings from 126 to 29.
    - Video-prompt problems went from 133 to 40.
    - "What's next" says "Finished" at the end.
    - The book no longer shows the kit's internal names.
    - Only the handouts for the biggest scenes are still slightly too large.
    - File: `Project notes/32 Fixes - after the full run.md`.
33. **Cross-examination by Opus 5.5.** You asked for GLM to cross-examine the work. GLM could not be reached: it needs an access key this environment does not have. You chose Opus 5.5 instead. A fresh Opus 5.5 helper at the highest effort tried to prove the fixes wrong, on copies only. It confirmed most of the work, and found five fixes that went too far:
    - "none" could wipe fields of records you had approved and locked;
    - "Finished" could appear with no spreadsheets or captions;
    - the light check let "The lamp goes out." through;
    - any quote excused an added light change;
    - a close shot of a ring could lose its protection from being flipped.
    It also found twelve smaller problems, and wrong sentences in note 32. File: `Project notes/33 Cross-examination - the fixes checked.md`.
34. **Repaired everything the cross-examination found, myself, without more helpers.** Each repair has a test that fails if the repair is undone; the new test file now has 42 groups.
    - Failure: my first light repair made four false alarms on The Catch ("turns the tag to the light", "the bright steel", "comes into the light", "a fire shutter"). I caught them on the re-check and fixed them, with tests.
    - Final re-check of The Catch: no errors, 37 warnings (up from 29, because the repaired checks catch real faults again), 40 video-prompt problems, and "Finished" only after every export.
    - Tests: 19 of 20 files pass; the failing one is the old chat-kit size check, whose files are within 3 words of their size before all this.
    - Note 32 is corrected, and note 33 ends with what was done about each finding.
35. **Tested the fixed kit on new writing, with one Opus 5.5 helper, as you asked.** It started The Catch from scratch in a test folder: 37 pieces of work to plan the whole film, then 13 for scenes 2, 13 and 26 (12, 37 and 20 shots). It took about 96 minutes. Your real breakdown was not touched.
    - Each scene ended with exactly one warning: scene 2 a false alarm (two shots counted as alike because the check ignores camera height), scene 13 the helper's own slip at the design step, scene 26 a false alarm.
    - Failure of mine: scene 26's false alarm comes partly from my repair in entry 34, which asks the sound plan to quote its moment, while step 6 never tells the writer to.
    - Scene 13 was split into parts once and never planned again, so that fix works. The turn-size, light and secret-keeping arguments did not come back.
    - The helper cut "Iona's husband" from Jude's role by itself, because the script never says it.
    - The final check left 1 error, a code fault: the video-model prices date is asked for before any step fills it.
    - New problems found: 43 of the 92 errors before repair belonged to later pieces of work. The book's one-line list can contradict the full shot below it. "Pause after: none" is refused. I confirmed the last two myself.
    - File: `Project notes/35 Test - The Catch - three scenes with the fixed kit.md`.

## Next step

Fix what the three-scene test found, myself, without helpers. The code faults come first:
- errors shown before they are due;
- the prices date;
- the two false alarms;
- "pause after: none";
- the book's one-line list.

Then the unclear planning instructions. Then re-run the tests, and re-check the test project to confirm its warnings clear.
