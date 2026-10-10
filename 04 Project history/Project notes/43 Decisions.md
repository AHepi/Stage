# 43 Decisions

Log entry 43 started this file. Every decision about the kit, in its own words, newest last. Each says who decided, when, and why. When a decision is changed, the old one stays and a new one says what replaced it.

## Decisions from earlier entries, gathered here

1. **The story stays out of git.** `My stories/` and `My breakdowns/` are in `.gitignore`; no story is copied whole into a committed file or a web request. (Blueprint, entry 13; the folder's CLAUDE.md.)
2. **The repository stays public, with short quoted passages from both stories in it.** You chose this in entry 19.
3. **Helpers.** Fewer helpers (entry 20); one helper at a time (entry 39); for this round, never more than two Opus 5.5 helpers on high effort (your message of 10 October 2026).
4. **The test answers are always "defaults".** Every test so far has answered the questions with their ready answers (entries 23 to 40).

## Decisions of entry 43 (10 October 2026)

5. **The first video route is MiniMax H3 in ComfyUI, Reference to Video.** The handover's question 1, with its ready answer, which you accepted by asking for the handover to be done.
6. **A clip may hold one to three shots.** The handover's question 2, ready answer accepted.
7. **The test run on your rented computer (handover item W1) waits.** You asked me not to use the RunPod zip yet. So the new route's rules are built now but stay suggestions until real clips confirm them (decision 11).
8. **The H3 route's prompts are made by code from the records**, like every Stage prompt ("prompts are compiled, never typed"). The AI improves the records, never a prompt. No new kind of record is written by the AI for this.
9. **Clip grouping, clip lengths, the tail, start picture briefs and master picture prompts are made by code** from the shot records, the set plans and the descriptions.
10. **Two routes for one model.** H3 on MiniMax's own service (with its rewriting step) and H3 in ComfyUI (without it) are separate entries that never share a prompt. The ComfyUI route is never chosen automatically: you ask for it, or set it as the project's way of making video.
11. **A rule from testers' notes is a suggestion until your take log confirms it.** Its check is a warning. Rules that are format facts from MiniMax's or ComfyUI's own documents may be errors. A rule two takes confirm (and none contradicts) becomes an error on that route; a rule two takes show wrong is dropped, with the takes listed. (Handover item W11.)
12. **Stillness is never asked for again.** Held moments are written as small timed actions, at least one every 2 seconds; the old "still" list is no longer written or sent. (Handover item W2.) The craft point behind it, "less display, more time", stays.
13. **Only what is there is written for H3.** No "not", "no", "nothing", "never" or "none" outside the spoken lines, except the one camera line testers found works, "with no camera movement whatsoever". Music with none is written "N/A". (Handover item W3; ComfyUI's prompt guide.)
14. **Off-screen lines are sent in the H3 route's prompt**, marked as coming from off screen, with the on-screen person's lips closed, as the clip file does. Stage's other routes still lay them in from voice takes. This is a judgement, marked J.
15. **The "motion only" rule does not apply to the H3 route.** In H3's reference mode each person's description is repeated word for word next to their picture's label. (Handover item W5.)
16. **The clip file and its reference code stay out of git**, because they hold lines and descriptions from scenes 1 to 6 of The Catch (the handover's trap). The handover note itself (note 42) is committed: its few quotations from the story are already in the repository.
17. **The handover's sources were checked on 10 October 2026** before building. MiniMax's guide, MiniMax's model page and ComfyUI's two H3 pages confirm the format facts; the testers' notes confirm the stillness, tail, contact, seed and shot/reverse-shot findings. Two points are narrower than the handover says: lines started 1.4 to 1.9 seconds late in the testers' runs, and a cut is smoothed away when a two-shot cuts to a closer single on the same line (not "any similar framings"). The facts carry marks: verified, unverified or judgement.
18. **Two helpers at a time.** You confirmed this on 10 October 2026 ("Two at a time I mean"): never more than two Opus 5.5 helpers on high effort at once.
19. **The repository is laid out as folders as stages,** after Van Clief and McDermott, "Interpretable Context Methodology" (arXiv 2603.16021, 2026), which you asked for because the repository was "disorganised and chaotic". The top level now holds `CONTEXT.md` (where to go), `01 Start here/`, `02 Example - The Catch, scene 10/`, `03 Kits to upload/` and `04 Project history/`; inside the kit, `stages/` (one folder per step, each with its `CONTEXT.md`), `references/` (what the AI reads), `_config/` (what the code reads) and `tools/`. Kept as they were, on purpose: `My stories/` and `My breakdowns/` (your names and habits), a project's own numbered files (already numbered stage outputs; changing them would break every breakdown made so far), `tests/` at the top, and the kit's place in `.claude/skills/` (where Claude Code finds skills). Notes before entry 43 keep the old folder names; `04 Project history/Project notes/00 About these notes.md` maps them.
20. **At most three people's pictures in one H3 clip** (a judgement: the hand-made clip file never wires more). A shot that needs more gets a clip of its own and a warning.
21. **"Picture style block"** is the paragraph pasted first in every picture prompt on the H3 route, so it is never confused with a place's "look block" (its light and colour words).
22. **The hosted H3 entry keeps MiniMax's own speaker form** (`<Subject 1> (S1) speaks softly, <d>...`, from MiniMax's guide); the ComfyUI route writes "says:" before a line, as the clip file does.
