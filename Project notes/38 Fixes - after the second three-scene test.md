# 38 Fixes - after the second three-scene test

Log entry 38. The fixes for what the second three-scene test found (Project notes 37). I made them myself, without helpers, as you asked.

## In short

**The split-scene errors are gone, the split-scene handouts are complete, and the book no longer prints numbers a reader can't use.** Both test projects and your full breakdown of The Catch give the same results as before, so nothing that worked broke:
- the second test project: no errors, no warnings;
- your full breakdown of The Catch: no errors, 36 warnings, and "what's next" still says "Finished".

**One example from the story.** In scene 13, Saye pauses the old recording of the freight shaft and traces it with her finger. The book's one-line entry said "her finger draws straight down the paused shaft". Next to Iona's shots, that read as Iona's finger. It now reads:

> shot 200, insert, 4.5 seconds, on Saye: her finger draws straight down the paused shaft; ...

The full shots of the recording also end "as recorded in scene 6", so the people in it no longer seem to be in the room.

## What was fixed (numbers as in note 37)

1. **A split scene's first part is no longer shown errors for the second part's beats.** They are "not yet due" until the second part is applied, like the other cases fixed in note 36. Once it is applied, any reference still missing shows as an error again.
2. **Records a later piece may not change:**
   - step 6 now says which form a planned long hold takes (`pause_after = hold`), the form the check looks for;
   - when a story secret lists the wrong people as knowing it, the suspense check's advice now says to report it, since the story plan's records are corrected there, not in the shots.
3. **A split scene's handouts now show what the earlier parts wrote.** Part 2 sees part 1's design fields, with a note to re-send a field whole. The shot-list piece also sees the beats, cameras and moves the list is built from.
4. **The book:**
   - each scene lists its beats, one line each, so "beat 17" leads somewhere;
   - "emphasis 2" reads "pointed out", and "grey preview level 0" reads "no grey preview";
   - a move is named by who moves ("Iona's move (She sits on Jude's bed)"), not "floor-plan move 2";
   - an addition the scene already lists is said once, even when the shot words it a little differently;
   - a one-line entry names who acts when its words don't ("on Saye");
   - recordings say "as recorded in scene 6", and a shot on a screen says "on a screen";
   - turns are named in story order: "A first turn", "A second turn", "The main turn";
   - "eyes on down into the dark" reads "eyes down into the dark";
   - two repeats I found while checking are gone: "Jude's water (jude's water)" and "Iona (Iona)".
5. **Place headings.** A heading's most specific part now counts most ("IONA'S ROOM" in "QUARANTINE - IONA'S ROOM"). A word most places share, like "room", is no match on its own. In the test project, Iona's room now gets its own three headings.
6. Fixed in entry 37 already: the step 4 example of a silent person's arc.
7. **Smaller points:**
   - a non-human's description is 25 to 40 words everywhere: the template, the field guide and the check now agree;
   - the field guide says the same as step 1 about where "only these scenes" is set: the scene list (checkpoint A) for a screenplay, the prose plan (checkpoint P) for prose;
   - the world step gets the mirror card when the story plan tagged a scene with handedness or mirror, before the mirror rule is written;
   - a character's handout never shows that character's own finished record as its example (Iona's piece now sees Saye's);
   - a saved choice "never in scenes 26 and 27" is no longer offered in those scenes, and "scenes 10 and 29" now means both scenes;
   - the health check says where the guide "05 How to read your breakdown" is;
   - the length check of step 2 runs when only some scenes are chosen, as long as the whole film's scenes are there;
   - the choices file lists the small choices shown at the big-choices checkpoint under "Small choices".
8. **Smaller instructions:** step 7 says the staging always changes on a turn, so it counts among the departments that change there; step 8 says to fix a warning too when its fix is in the piece's own records; step 1 is clearer about title cards.

## My own slip

My first words for the grey preview levels did not match the kit's own scale. Card 22 says level 2 is a layout check in 3D and level 3 a guide video; I had written them as "with movement" and "full". I caught it before testing, and the words now follow card 22.

## Not fixed

- **No check compares cameras, moves and shots** (problem 8). I tried the planned check for a camera crossing the line between two people. It flagged the model scene 10, where glass and reflections change who is on which side, so I put it back as planned. A better version needs the reflections worked out first.
- **A thing's state that starts on a later line than the shot showing it** (problem 2, third case). Only the continuity step may change it, so a later piece of work can only report it. Nothing new was added for this.
- **One state's name contradicting its shot** (problem 4). That is the helper's wording in the test project, not a kit fault.
- **The chat-app files are still over their size targets** (the same three as before).

## Tests

- New: `tests/fix04_second_three_scene_test_acceptance.py`, 7 groups, on small copies of the model scene only. All pass.
- Changed: one older test expected the book's old words ("The turn is beat 7"); it now expects the new ones.
- The full suite on the final code: 21 of 22 test files pass. The failing one is the old check of the chat-kit files' sizes (the same three files as before).
- Re-checks on copies: the second test project (no errors, no warnings), your full breakdown of The Catch (no errors, 36 warnings, "Finished").

## What was not tested

- A fresh helper using the kit after these fixes. The next full run will be that test.
- The other 27 scenes with the fixed kit.
- The chat apps, The Long Places, pictures and video.
