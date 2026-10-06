# 41 Improvements to scope later

Log entry 41. One list of everything known to be open about the kit, gathered from the project notes, the project story, the blueprint and the code. Each item says where it came from and how much it matters. From now on I add to this list each round instead of scattering items across notes. When an item is done, it is marked done here with the entry that did it.

How much it matters:
- **High:** it can give a wrong plan or block work.
- **Medium:** it costs repair rounds or leaves a gap a reader would notice.
- **Low:** wording, tidiness, or something only some stories meet.

## 1. Needs a design decision first

These need you or me to decide how the kit should work before any code changes.

1. **The shot details step may not add a camera, move a person or retime the shot list** (fix list T1, Project notes 40). *Medium.* Some faults can only be fixed one step back: a second camera angle, a move timed to the cut, a scene's list times. The step either bends the shot or the scene is reopened. The question: may step 8 add a camera or move, as an addition you see?
2. **One set plan holds one room** (T2). *Medium.* A brother behind glass in the next room, a front step, a guard coming in from an unplanned room, two rooms under one heading. This needs joined plans or marks outside the room, plus the checks and grey previews to match.
3. **Action inside moving things and real physics** (T3). *Medium, for action stories.* The upside-down cage, hanging bodies, cameras fixed to a falling cage, an honest free fall shorter than the list planned. This needs new card content and checks.
4. **The review questions grow to the whole film** (T4). *Medium.* In a mirrored story, "every shot that needs mirror, text or violence handling" was 413 of 518 shots: 2,518 questions. It needs a narrower meaning of "needs handling".
5. **Earlier steps' content slips no check sees** (T5). *Medium.* A bed 2 m from its hatch, a cup with no shelf, a room sound describing another scene, a group's soft light against its place's hard light. This needs checks that compare records across steps.
6. **Which card parts an oversized handout drops first** (cross-examination X16 a). *Low.* The core parts of step 8's cards can still be dropped for the biggest scenes.

## 2. Checks written but switched off

7. **A camera crossing the line between two people within a part** (GEOM-03; Project notes 36 and 38). *Medium.* The helpers found three such slips by hand. A first try flagged the model scene 10, where glass and reflections change the sides, so it waits until reflections are worked out.
8. **A shot's size far from the planned size for its beat** (CRAFT-17). *Low.* Waits for test runs to show how far is too far.
9. **A shot leaving the main character's place or knowledge without saying so** (REASON-09). *Low.* Waits for test runs to show how scenes mark whose view they take.

## 3. Left over from the fixes

10. **Reader-facing shorthand in the "why" lines.** *Medium.* After the update run (Project notes 40), the test book still holds lens shorthand ("the 40") about 440 times, about 36 one-word names in capitals (some are the story's own words) and "emphasis 2" 6 times. Step 8 forbids them, but no check flags lens shorthand, and the full check does not flag the others: only the export does, two names at a time.
11. **The mid-crawl false alarm** (F20 a, c, d). *Low.* Shot size is measured where a person is part-way through a move the cut skips. Fixing it needs moves timed to the cut, a test of what is in frame from top to bottom, and a "leaning" posture.
12. **Who writes a scene's list of people** (F06, part). *Low.* People who never speak now reach the handouts. The scene's own list is still written by the AI, and can miss them.
13. **Scene files named from the place, not the script's heading** (F60). *Low.* Changing it would rename every project's files and the kit's example.
14. **The model example's extra lines** (F35, part). *Low.* The model scene 10 writes position details the step now calls optional. It was left alone because many tests compare against it.
15. **Capital words in prose stories** (X16 b). *Low, prose only.* A sign written in capitals in prose is found only through its `words_from` line.
16. **A move's "via" takes only one point** (X14, part). *Low.*
17. **Older projects are not asked for the rights evidence line** (X15 c, part). *Low.*

## 4. Older open items, not checked again since

From Project notes 32 and 36; some may have been fixed along the way.

18. A finding of the whole-film pass stays open after its problem goes away. *Medium.*
19. "What's next" names the next piece even when the last check failed. *Medium.* Seen again in the update run: after the film pass it offered the exports while the full check had an error, and nothing pointed back to the piece that wrote the record.
20. The look description's 2 to 3 sentences are not checked. *Low.*
21. A story rule's title can read like a name inside the book's sentences. *Low.*
22. The whole-film summary says it leaves out record types it has room for. *Low.*
23. Template gaps: naming a thing in a rule before the thing exists; where a time slice's frames go; putting a state between two others. *Low.*
24. "What's next" makes the next handout as a side effect; "status" is the command that only looks. *Low.*
25. A place with no states can't be named as a thing, and the refusal doesn't say why. *Low.*

## 5. Known issues (project story)

26. **The chat-app files are 26% to 49% over their size targets.** *Medium, for Gemini.* Google does not publish how much a Gem can hold.
27. **The light check reads words.** *Low.* A change of light in words it does not know would slip through.
28. **The start page's "last checked" line updates only at the next save.** *Low.*
29. **No pull request yet:** the repository has no main branch to merge into. *Low.*
30. **The repository is public, so short quoted passages from both stories are public** (entry 19, your choice). *Low.*

## 6. Planned for a later build (the blueprint, Project notes 13)

31. A page that runs the checker inside the browser, for Gemini users with no way to run code.
32. Marking single fields out of date, not whole records.
33. Tone defaults tuned from test runs.
34. Cost estimates from a rough edit and from real spending.
35. Sending generation batches through connected services automatically.
36. Posed stand-in figures and performance capture for grey previews.
37. Tools for series: episode tables, recaps.
38. An export for Movie Magic scheduling software.
39. Replaying a breakdown with the smallest model, as an automatic test.

## 7. Never tested yet

40. A real person answering the questions (every test so far answered "defaults").
41. The Long Places, or any story other than The Catch, end to end.
42. The chat apps for real (ChatGPT, Gemini, Claude on the web).
43. Making pictures, video or voices from the prompts.

## 8. Found while carrying the test project on (Project notes 40)

44. **Repair rounds carry over between runs.** *Medium.* A piece of work that used its 3 repair rounds in the first run has none left for a new fault a revised kit finds. One label in scene 18 stayed for that reason.
45. **Repair file numbers.** *Low.* apply accepts a repair file whose number was already used, and suggests "fix 4" after the third and last round.
46. **The export names only two labels of each kind at a time.** *Low.* The helper found the rest by exporting again, or by counting by hand.
47. **The size check offers no "kept on purpose" route** when the cause is a move in an earlier step. *Low.*
48. **Shot numbers are printed with their zeros** ("shot 010") in the book and the health check, 523 times. *Low.* This is the film-industry habit, but a reader may not expect it.
49. **A piece of work's own check takes about 15 seconds.** *Low.*
