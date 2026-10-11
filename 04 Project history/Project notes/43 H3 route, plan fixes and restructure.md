# 43 The H3 route, the plan fixes and the restructure

Log entry 43, 10 October 2026. What was built from the handover (note 42), how the repository was restructured, what two rounds of cross-examination found, and what is still open. Decisions are in `43 Decisions.md`, lessons in `43 Lessons.md`, where things stand in `43 Status.md`.

## One moment, before and after

Scene 10, shot 150, "Not mint.", compiled for MiniMax H3.

**Before** (Stage as it was; the handover's own example):

> ... Her head, hands and torso stay still; only her eyes and mouth move. Her face and body show small, contained movements. It ends: still, mouth closed ... The camera holds a perfectly static shot [static]. The camera does not move. ... the fridge's low hum, and nothing else. non_diegetic_music: none.

**After**, on the new route "MiniMax H3 in ComfyUI, Reference to Video" (clip 07 of scene 10, shortened):

> subject_definitions: <Subject 1> is Saye's kitchen shown in <Picture 1> ... <Subject 2> is Iona, a lean, strong woman ... Her face, hair and build come from <Picture 2> ...
> detailed_description: ... The shot is static, on a tripod, with no camera movement whatsoever. ... Iona is alive in every second of this clip ...; she blinks at about 00:01.000, 00:04.000, 00:07.000, 00:10.000 and 00:13.000. [Shot 1] ... For the first 4 seconds, Iona chews slowly ... At about 00:06.000, <Subject 2> (S2), ..., says, unsteady: <d>[English] Not mint.</d> ... At about 00:08.000, Iona swallows once; breathes out slowly through her nose; blinks ... From 00:12.800 to the end, Iona goes on with what she is doing ...
> non_diegetic_music: N/A

Across scene 10, the hosted H3 prompts held "stays still" 44 times and "The camera does not move." 18 times; now none.

## What was built, item by item

The handover's work list, with its "done when" and where it stands. "Cannot test here" means the plan of scenes 1 to 6 of The Catch is not in this session; only scene 10 is.

| Item | Built | Done when (note 42) | Where it stands |
|---|---|---|---|
| W0 | The decisions, lessons, status and glossary files; W1 to W12 added to note 41 | the files exist and note 41 lists W1 to W12 | Met |
| W1 | A test-run pack, kept outside git: scene 10's held turn and one exchange in both forms, and the clip file's clips 03, 21 and 04 in the new shape, 16 runs with a take log to fill | 12 runs logged, every rule marked | Waits for you: the RunPod setup was not used, as you asked |
| W2 | No stillness written or sent: CRAFT-26 turned round (a held moment needs a small timed action every 2 seconds), CRAFT-27 (stillness words), library D15 rewritten with errata, cards and step 8 rewritten, the gold example rewritten as timed actions | no "still" sentences for H3; every held moment has timed actions | Met for scene 10 |
| W3 | For both H3 entries: words naming what is absent are cut and listed; music is N/A; one camera line | no not, no, nothing, never or none outside the lines, except the camera line | Met for scene 10 |
| W4 | A separate route entry, `minimax-h3-comfyui-r2v`, never chosen automatically, with the template's box names, sizes, the 17 x k + 5 frame grid, a 1.3-second tail and the seconds to type | only boxes that exist in the template; every typed length lands on its frames | Lengths met (all 15 grid lengths land both ways); box names are from the clip file's reading of the template, unverified |
| W5 | The prompt in MiniMax's six sections with picture labels, built by code from the records, and 27 route checks (ROUTE-01 to 27) | scenes 1 to 6 compile with the clip file's structure, clip for clip | Cannot test here; scene 10 has the structure |
| W6 | Clips of one to three shots, grouped by rules (same place, clearly different framing, no line crossed, facing singles need a shot of both first, held takes alone, at most four new pictures), each clip saying why it starts or what it shares; a shot map | scene 1's twelve shots become about eight clips | Cannot test here; scene 10's 18 video shots make 11 clips |
| W7 | Master pictures (one per place, empty) and a start picture brief per clip; the picture style block; the checklist; stills for the edit | every clip page names its master and character pictures | Met for scene 10 |
| W8 | Eleven physical sense checks (PHYS-01 to 11): room for a body, a thing held in the teeth, a line spoken round it, reach, cutting with nothing, cover under something open, a fixed bar that rolls, the weak running or holding up the heavy, door braces and kicks, one thing per hand, too small to see | they flag every slip in the clip file's section 3 | Partly: 11 of the 18 slip types caught, 3 in part, 4 not (story logic, what can be seen from where, speed, the hidden disc) |
| W9 | CRAFT-28 (a contact and its result in one shot) and contact pairs kept together in one clip, read by one shared rule | the window, the strap and the trip come out as clips 21, 22 and 28 | Cannot test here |
| W10 | Take questions that catch real failures; no question asks whether something stays still; each clip's check opens with its own key actions | no question rewards stillness | Met |
| W11 | Every route rule carries a mark (verified, confirmed, wrong or unclear) worked out from the take log; a check's level follows its rule's mark | each rule marked, with the takes that decided it | Met: 27 rules, 9 verified from the makers' documents, 18 unclear until takes decide |
| W12 | Not started (sending clips straight to ComfyUI) | | Later |

## The restructure

You asked for the repository to be restructured around Van Clief and McDermott's "Interpretable Context Methodology" (arXiv 2603.16021, 2026), because it was disorganised.

- **The top level:**
  - `CONTEXT.md`, a page on where to go for what you want to do
  - `01 Start here/` (the six guides)
  - `02 Example - The Catch, scene 10/`
  - `03 Kits to upload/` (the chat kit and the skill zip)
  - `04 Project history/` (these notes and the project story)
  - `My stories/`, `My breakdowns/` and `tests/`, as they were
- **Inside the kit:**
  - `stages/`: one folder per step, each with its own `CONTEXT.md`; the list of steps is made by build-kit from the settings
  - `references/`: cards, library, formats, templates, example
  - `_config/`: schema, rules, adapters
  - `tools/`
  - each of the first three with a short guide file
- **What the AI reads:** each handout now shows the rules for the piece of work first and the story's material second, the paper's split between reference and working files.
- **Unchanged on purpose:**
  - the layout of a breakdown project (already numbered outputs; changing it would break every existing breakdown)
  - your two folders' names
  - the kit's place in `.claude/skills/`
- **Old names:** notes before this entry keep the old folder names; `00 About these notes.md` maps them.

## Cross-examination

Two rounds, two read-only reviewers each, then two fixers each, never more than two helpers at once.

- **Round 1 found 20 faults in the new work** (3 high):
  - lines stacked at second 0
  - no mirror-world support on the route
  - the people cap applied wrongly
  
  Also: repeated warnings, clip pages that did not say why shots share a clip, inserts written as whole people, stillness still taught in a few texts, false alarms in the plan checks. All 20 were repaired.
- **Round 2 found 22 more:**
  - On the restructure: 2 medium, 5 low. It also confirmed that every path resolves, both zips run, and a project made before the restructure still runs.
  - On the repairs: 1 high, 6 medium, 8 low. The high one: one repair could drop a spoken line with no error. Another left sentence fragments where words were cut.
  
  All were repaired; the plan checks' wording faults only in part (below).
- **The plan checks on realistic wordings.** The reviewers' own wordings now give no false alarms and no misses. A separate set written before the rules were changed went from 5 false alarms and 16 misses to 2 and 12. That set was written by the fixer who changed the rules, so it is not fully independent.

## Tests

- **25 of 27 test files pass.** The two that fail failed before this work: the PDF-reading group (it depends on this computer's converter) and the chat kit's size target. The chat kit is now about 77,000 words against a target of about 60,000.
- **New test files:**
  - `fix06a` (the route, 24 groups)
  - `fix06b` (the plan checks, 22 groups)
  - `fix06c` (round 2 route repairs, 11 groups)
  - `fix07` (the routing files and the layout, 9 groups)
- **What was run:** the kit was rebuilt and run end to end in the new layout: a fresh project, an adopted chat folder, both zips unpacked and run.

## What I did not test, and what is still open

- **Nothing has been run on H3.** Every judgement rule is a suggestion (a warning) until your take log confirms it.
- **The route's box names** are from your clip file's reading of the template.
- **Scenes 1 to 6** could not be compiled here (their plan is not in this session), so the clip file comparison is by structure on scene 10, not clip for clip.
- **The plan checks still miss some wordings,** for example "kneels", "doesn't budge", "staggers", "a log that rolls". One false alarm remains: "the dog jumps up". All are listed in note 41.
- **Small leftovers on the pages:**
  - a voice description can end on a dangling word after its other words are cut ("clear and quick, quieter")
  - still-picture prompts for the edit say a face "shows small movements"
  - a shot-list line that held a quoted line can read "Dr Saye, unseen" in the summary
  - clip 01 of scene 10 (three shots, four people) has a 782-word description, over MiniMax's normal 350 to 500 (a suggestion, not an error)
- **Shot 150's length:** the plan's 15-second hold is 1.22 seconds longer than H3 can make with its tail. The clip page says to make the rest in the edit or redesign the shot. This is an error the route check reports, as planned.
- **Note 42 itself** is in the public repository and quotes a few lines of clip 03's prompt (see Status).
