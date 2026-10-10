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

## 9. The handover's work list (Project notes 42)

Added in entry 43. Each item's "done when" is in note 42, section 6. Where it stands is updated each round.

50. **W1. Test run first:** three clips on your rented computer, two seeds each, as Stage wrote them before entry 43 and as the clip file writes them; twelve runs in the take log. *High.* Done in entry 45 (note 45): 14 runs; the contact cut confirmed, the planning picture decides the camera. Waits on your listening for the speech rules.
51. **W2. Stop asking for stillness.** *High.* Done in entry 43 (met for scene 10).
52. **W3. Only say what is there.** *High.* Done in entry 43 (met for scene 10).
53. **W4. Routes, not only models:** H3 on MiniMax's service and H3 in ComfyUI as separate entries. *High.* Done in entry 43; the template's box names are still unverified.
54. **W5. Compile in MiniMax's reference format** for the ComfyUI route, with the route's own checks. *High.* Built in entry 43; the clip-for-clip comparison with scenes 1 to 6 waits for their plan.
55. **W6. Clips as the unit:** one to three shots per clip, a shot map back to plan shots. *High.* Built in entry 43 (scene 10: 11 clips for 18 video shots); scene 1's count waits for its plan.
56. **W7. Start pictures:** master set pictures and one start picture brief per clip. *High.* Done in entry 43.
57. **W8. Physical sense checks.** *Medium.* Built in entry 43: 11 checks catch 11 of the clip file's 18 slip types, 3 in part, 4 not.
58. **W9. Cut at contact.** *Medium.* Built in entry 43; the clips 21, 22 and 28 comparison waits for the plan of scenes 3 to 5.
59. **W10. Questions that catch real failures**, never rewarding stillness. *Medium.* Done in entry 43.
60. **W11. The take log teaches the rules:** each route rule marked confirmed, wrong or unclear by real takes. *Medium.* Done in entry 43; every judgement rule is unclear until the test run.
61. **W12 (later). Send clips straight to ComfyUI** from Stage, with no copying by hand. *Low for now.*

## 10. Left over from entry 43 (note 43)

62. **The plan checks still miss some wordings** (held-out set after the fixes: 2 false alarms, 12 misses): "kneels", "lies", "doesn't budge", "stays right where", "staggers", "crumples", "tumble", "stamps on", a list after "grabs", a log that rolls, "in her mouth" after a leading clause; false alarms "the dog jumps up" and "she freezes the leftovers". *Low.*
63. **A voice description can end on a dangling word** after its other clauses are cut ("clear and quick, quieter"). Better: a short sound-only voice line in the VOICE record. *Low.*
64. **Still pictures for the edit say a face "shows small movements".** The old picture prompt's display sentence. *Low.*
65. **A shot-list line that held a quoted line reads "Dr Saye, unseen"** in a clip's summary. *Low.*
66. **Big clips run long:** a clip of three shots and four people can pass MiniMax's normal 350 to 500 words (scene 10, clip 01: 782). It is a suggestion; whether it matters is for the test run. *Low.*
67. **Shot 150's hold is 1.22 seconds longer than H3 can make** with its tail. The page says what to do; the plan itself is unchanged. *Low.*
68. **Several guides and kit files sit near their word limits** (CLAUDE.md 293 of 299, README 246 of 250, the Gemini guide 1,093 of 1,100). Any added sentence may fail the length test. *Low.*
69. **SKILL.md is still about 5,500 tokens**, against the paper's 1,100 for the first two layers; only two sections moved out. *Low.*
70. **Untested choices of entry 43:** four people's pictures in one clip; off-screen lines sent in the prompt; the closing "goes on with what she is doing" line; mirror-world shots kept as later shots of a clip; the 2.4:1 frame at 1152 x 480. All marked J; the test run decides. *Medium.*

## 11. From the first H3 test (entries 45 and 46)

71. **Action clips on another model.** Your verdict on the first H3 test (entry 46): H3's action was unusable, while dialogue can work. Let the clip book mark each clip for a model (H3 for dialogue and performance, Seedance or another for action) and test scene 5's trip on Seedance. *High.* Source: entry 46.
72. **Several takes per dialogue clip.** Only 1 of 4 dialogue takes was usable; the clip page should say how many takes to make and how to choose. *Medium.* Source: entry 46.
