# 36 Fixes - after the three-scene test

Log entry 36. The fixes for what the three-scene test found (Project notes 35). I made them myself, without helpers.

## In short

**The test project now ends with no errors and 2 warnings, both real slips by the helper.** Before this round it had 1 error and 4 warnings, two of them false alarms. Re-checking your full breakdown of The Catch gives no errors and 36 warnings, and "what's next" still says "Finished".

**One example from the story.** In scene 26 the ship's motor stops: "The sick motor through them." then "Then not." That silence was flagged as "an added change" for two reasons:
- a nearby line about a floating screw "hangs in her lamplight", and the checker took that light word as the script marking the moment;
- the sound plan named only the scene, not the moment.

Now a light word marks a moment only when the light changes or moves near it. A silence on the beat the scene's own planned break names counts as planned, and step 6 tells the writer to quote the moment. The false alarm is gone.

## What was fixed (numbers as in note 35)

1. **Errors that belonged to a later piece of work.** These are now "not yet due" in each piece's own check, as they already were in a whole step's check. They still show on the health check page, and never count as errors.
   - A scene-plan piece is no longer asked for the groups of scenes and planned lengths the next piece brings. That piece is also no longer told to write the groups.
   - Each part of a split scene is no longer asked for the later parts' beats or the shot list.
   - The answers to the big choices wait until those choices are answered.

   On a fresh project from the small test screenplay, a scene-plan piece now shows "Not yet due: 9 lines" and no errors. Before, it showed 9 errors it could not fix.
2. **The prices date.** The check no longer asks for the date of the video-model prices. The cost estimate writes it, and the prompt check judges its age when prompts are made. Advice for a field only you may set now says to answer the question that sets it, never to type it.
3. **The scene 26 false alarm** (the example above).
4. **"Two shots too alike" now counts camera height.** The angle between the two cameras is measured in 3D from the person's eyes, so scene 2's low camera tilted up is a new angle, as it should be.
5. **The book.**
   - The one-line list now follows the shot as written (its moments, in order), so it can no longer contradict the full shot below it.
   - States are named by what they are, not by number ("Iona (palm dressed, banded)", not "Iona, state 6").
   - Saved choices are named by their title.
   - Floors are rounded up to one decimal.
   - "seated:Jude" reads "at Jude's seated eye height".
   - A plant and a motif with the same name are said once.
6. **"Pause after: none" is accepted.**
7. **Footage of an earlier time.** "recorded: scene 6" now means some time in scene 6, so any state that held during it fits. A quoted moment pins it to that line. Step 8 and the template say so.
8. **Splitting a long speech** over a speaker shot and a listener shot now works as card 13 says. Each shot gives the run of words it hears, and is timed for those words. The words must be the speech's own, in order.
9. **Smaller code faults:**
   - "apply" also finds an inbox path written from the project folder;
   - an empty record is named instead of passing in silence;
   - a piece's check says when its inbox file is still not applied;
   - after the answers at a checkpoint, apply suggests that step's own check instead of a full one;
   - a one-letter text (the paper F) only matches when its thing is in the scene;
   - an in-story camera's own angle no longer counts as using the film's saved top-down shot;
   - the loud-places check now runs at step 4, where the places are written.
10. **The planning instructions:**
    - the self-test handout prints every allowed value;
    - the start piece's list of what to write is corrected, and the film-rules piece now lists the frame rate;
    - "sets: none" is allowed for a choice with nothing to set;
    - how to say "only these scenes" is in step 1;
    - a rule's "governs" may be "none" with a note naming what step 4 will give names to;
    - one physical place is one place, however many ways the script names it;
    - a silent extra writes a one-line arc;
    - one likeness choice per character;
    - a thing whose side can show in the mirrored world gets a state;
    - you write side items yourself;
    - where the web can't be searched, the name check says so.

## Not fixed

- **The two slips the helper made,** in scene 13 and the loud places. They are in the test project's records and would need those steps redone. Both are real warnings, which is the checker working.
- **No check compares a turn's picture with its cameras, or a move's timing with its shots.** The helper found three such slips by itself. A future check could catch them.
- **"What's next" still names the next piece when the last check failed.** The check's own output says so, but "what's next" does not.
- **The look description's 2 to 3 sentences are still not checked.**
- **A rule's title can read like a name inside the book's sentences.**

## Tests

- New: `tests/fix03_three_scene_test_acceptance.py`, 7 groups, on small fixtures only. All pass.
- The full suite: see the project story, entry 36.

## What was not tested

- A new test run with a fresh helper after these fixes.
- The chat apps, The Long Places, pictures and video.
- Splitting a speech in a real scene. It was tested on the rule's own small cases only.
