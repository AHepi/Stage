# Fix list after test 01 (The Catch, fresh AI, Standard depth)

Source: scratchpad/test_runs/01 Test - The Catch.md (read it for exact commands and outputs). The tester's project is at
"/home/user/Stage/My breakdowns/The Catch" (or where the report says; use a COPY for experiments, never edit the original).
Decisions below are final; implement them. "Code" items belong to the code fixer, "Text" items to the text fixer.
Where an item needs both, the contract is stated here so both sides match.

## Code (tools/, schema/, rules/, templates/, tests/)

C1. Project location: `stage.py new` must put projects in "My breakdowns/" whenever the folder holding CLAUDE.md or a
    "My breakdowns" folder can be found by walking up from the current folder or the story file; never elsewhere inside
    the repository. Test it with and without CLAUDE.md.
C2. Build `lib <code> <reference>` (print one library section, rule, principle or example, with errata; fall back to the
    digest entry, labelled) and `replay [--story <path>]` (blueprint 7.1). `import-json` stays planned: its message says
    plainly it is not in this version.
C3. `next` must never skip a unit whose own apply has not happened, and never pass an unanswered blocking checkpoint.
    Mark units done only from the manifest's units_done (written by apply), not from "evidence" that a record type exists
    (the SOUNDPLAN stub made next jump from step 3 to step 7).
C4. FORM-05 must never demand a field that no writer fills. Make code fill (on apply/build) every code-owned field:
    PROJECT genre, tone_home, tone_range (copied from PLAN once written); CHOICE date (only answered or defaulted choices
    need one); STYLE provisional and named_reference_policy (code defaults: provisional yes until the style test,
    policy from rules); SOUNDPLAN clip_audio (derived from music and voice policy); LOCATION headings (from the scenes
    that use the place); TEXT words for origin story (the exact story words of the cited lines). CHARACTER voice is
    required only for characters with speeches; `voice: none` is valid for the rest. Add a test that walks schema.json
    and fails if any required field's writer is code and no code path fills it.
C5. A CHOICE that sets a field on a record that does not exist yet (music -> SOUNDPLAN.music_policy at step 3) keeps the
    value pending and applies it when the record is created (step 6), logged; never drop it silently.
C6. apply refuses an AI unit writing a field whose writer is `user` (FORM-10, like code-owned fields); such values
    come only through CHOICE or SETVALUE.
C7. Add `check --unit <unit ID>`: checks only the records that unit wrote plus what they cite, and requires only fields
    filled by that unit's step; `check --step N` counts fields of units not yet run as "not yet due", never errors.
C8. When the step-2 film unit is applied, code runs the first estimate (v0) itself to fill target_duration_s and the
    PLAN budgets. TIME-03 (scene total vs target) becomes a warning with the tolerance in constants.json
    (scene_duration_tolerance_share 0.25), because the target comes from word counts, not design.
C9. selftest: the handout's SHOT template marks every required field and gives real IDs to cite; `--score` writes all
    errors to a file and prints the count; a retry with the same issued IDs works; `--surface` is documented in its help.
C10. The same checks run at step 7 and step 8 on step-7 records: REASON-03 on MOVE `why` shows at `check --step 7`;
    STATE-01 treats a subject's state the same way at both steps.
C11. GEOM-04 (and any distance check) uses 3-D distance including height (z) from vertical set plans and mark heights.
C12. INFO-01 respects `keep_hidden` items whose `how` hides the thing from sight (sound_first, off_frame, ...).
C13. CRAFT-07: shots whose kind is `screen` (in-story camera footage) use that CAMERA record's lens, not the film's lens
    family.
C14. One `because` kind everywhere: any ID of a story record (scene, beat, character, place, prop, text, motif, rule,
    plan, camera rule, reserve, look, fact, plant...) or a line reference. SHOT and SCENE accept the same set.
C15. status: PROJECT.checker_last_run is updated whenever `check --all` runs (also when a scope is set) and status reads
    it; status names steps with the user's count ("step 4 of 12, world and style") everywhere.
C16. Reader: a parenthetical like "(through the torch)" is not a device path. Device paths come only from a word list
    (radio, phone, speaker, intercom, tablet, screen, recording, earpiece, "in her/his ear", V.O., RECORDED, O.S. rules).
C17. Repair inbox files are named "<unit ID> - fix <N>.md"; apply records the base unit in units_done, never the fix name.
C18. Book export: speech lines are shown whole (no cut at the first full stop); fix the broken phrases ("made from put
    together in the edit", "does settles"); show CUT records (joins such as jump cuts) in each scene; fix the "30 shots in
    30 scenes" count. Run the checker's WORDS rules on the book in the test.
C19. PROJECT.scope works for screenplays: `next` hands out only in-scope scenes (their sequences' other scenes are
    skipped, not forced), checks and exports say "Scope: 3 of 30 scenes". A choice "Only do scenes 2, 9 and 16 for now"
    sets it; "Do the rest" clears it.
C20. Step-7 handout: include the MOVE template; the scene's LOCATION with its set plan and the place's STATE at scene
    start (from the scene list's location); the in-story CAMERA records for scenes whose SCENE.host or tags need one; and
    the PROP and TEXT records that the scene's lines mention (by alias).
C21. SCENE.host is assigned at step 4 by the unit that writes in-story cameras: its handout lists the scenes the reader
    flagged as seen on a device, and the unit writes SCENE.host for each (contract with T7).
C22. Character units: principals are the characters with the most speeches or scenes (Saye in The Catch is a principal):
    principal if speeches >= principal_speech_share (constants, default 0.08 of all speeches) or present in >= 25% of
    scenes. Minor speakers are grouped; non-speaking characters (the figure, guard, nurse, technician) get their own unit
    with a reduced field set (required_when speaks for voice and speech fields).
C23. FACT `element` may be a story point before step 4; the step-4 THINGS unit's handout lists FACT records whose element
    is not yet an ID and the unit re-points them (contract with T7).
C24. CRAFT-03 honours camera rules: the main turn must be at least as tight as every earlier shot, and at the tightest
    size the scene's CAMRULE caps allow for its subject; equal sizes are allowed when a cap applies; skip CRAFT-03 when
    every shot of the scene is kind `screen` (a fixed in-story camera).
C25. "02 Whole-film summary.md" must be compact: at most summary_words_max (constants, 6,000) for The Catch: one line per
    record with only the fields step 7 reads; if still over, drop the lowest-priority record types first and say so.
C26. Templates match the checker: RESERVE max_uses (a number, 1_per_scene or share), LOCATION wild_walls (compass wall
    names), STYLE with provisional and named_reference_policy; every repeated field that may be empty shows `none`.

## Text (SKILL.md, steps/, cards/, reference/, root guides 01-06, CLAUDE.md)

T1. SKILL.md: projects live in "My breakdowns/"; repair inboxes are named "<unit ID> - fix <N>.md"; `next
    --checkpoint-passed` is explained where checkpoints are; `lib` and `replay` exist; `import-json` is marked "not in this
    version"; the ZIP's top folder is breaking-down-stories/ (match build_kit).
T2. Step 0: fix the instruction that contradicts "a field you send replaces all its lines" (send every line of the field).
T3. Scope for screenplays: SKILL.md's commands list and step 7 say "Only do scenes 2, 9 and 16 for now" sets scope (C19).
T4. Step 3: the music choice's answer is kept until step 6 writes the sound plan (C5); say so.
T5. `because` accepts any story record ID or a line reference, in every record (C14): card 14, reference/01, step 8.
T6. Step 4: principal, minor and non-speaking character units (C22); the in-story cameras unit writes SCENE.host (C21);
    the THINGS unit re-points FACT elements (C23); the name check (D4 Recipe 3) is done in the THINGS unit and recorded in
    22 Rights and credits (say exactly where).
T7. Step 7 and card 10 or 14: the main turn is the tightest shot the camera rules allow (C24); in a fixed in-story camera
    scene the turn is carried by the frame's content and cuts, not size.
T8. Step 2 and step 10: the first estimate fills scene targets automatically (C8); TIME-03 is a warning.
T9. Wherever "02 Whole-film summary" is described, say what it holds and its size (C25).
T10. Check the guides 01-06 and CLAUDE.md still match after these changes.
