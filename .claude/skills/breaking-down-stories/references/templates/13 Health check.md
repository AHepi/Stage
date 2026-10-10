# Health check

## At a glance

<How many problems, how many must be fixed, and whether the scenes are ready.>

## What to fix first

<One line for each problem that must be fixed: where it is and what to change.>

## The three scenes to read

<The climax scene, the scene with the most talk, and the biggest action scene.>

Below this line: details for the AI and the checker. You never need to read them.

### REVIEW <RV- and a scene ID, or RV-FILM, like RV-SC10> <a short plain title>
- scope: <standard: a scene ID or film>
- answer: <standard, one line each: text> | answer: <yes or no> | evidence: <text>
- score: <standard, one line each: a number from 1 to 10> | score: <a number from 0 to 3> | evidence: <text>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> REVIEW: Judge answers and rubric scores for a scene or the film. (review; ID RV- and a scene ID, or RV-FILM, like RV-SC10; lives in 13 Health check.md.)
> status: draft, approved, stale, omitted.

### FINDING <FIND- and 3 digits, like FIND-004> <a short plain title>
- record: <quick, code writes it when checker_finding; otherwise you write it: an ID of any record ID>
- rule: <quick, code writes it when checker_finding; otherwise you write it: text>
- evidence: <quick, code writes it when checker_finding; otherwise you write it: text>
- fix: <quick, code writes it when checker_finding; otherwise you write it: text>
- source: <quick, code writes it when checker_finding; otherwise you write it: checker, film_pass, review or user>
- status: <quick: open, fixed or accepted>
- reason: <quick: text>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> FINDING: A problem found, with its fix. (finding; ID FIND- and 3 digits, like FIND-004; lives in 12 Whole-film check.md, 13 Health check.md.)
> Conditions:
> - checker_finding: FINDING.source is checker.
> - otherwise: None of the other conditions in the same writer_when list holds.
> status: open, fixed, accepted.

END OF FILE | Health check | 2 records
