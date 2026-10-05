# 35 Test - The Catch - three scenes with the fixed kit

Log entry 35. One fresh Opus 5.5 helper, using only the kit, started The Catch from scratch. It planned the whole film, then wrote scenes 2, 13 and 26 after the simulated user said "Only do scenes 2, 13 and 26 for now". It worked in a test folder; your own breakdown of The Catch was not touched.

## In short

**The fixes work on new writing.** Each of the three scenes ended with exactly one warning. In the full run, a scene often ended with several, most of them rules arguing with each other. Of the three left:
- one is a slip the helper made itself a step earlier;
- two are false alarms from the checker.

None of the old arguments came back: the turn's closest size, light against light cues, and secrets against "keep hidden" all stayed quiet.

**What it means for your idea:** a helper following the kit can now finish a scene almost cleanly. What's left is smaller and different:
- some checks still report problems that belong to a later piece of work, so a piece shows errors it isn't allowed to fix;
- two checks raised false alarms;
- the book still prints a few things a reader shouldn't see.

## One example: the one warning left on scene 26

In the climax the ship's sick motor stops under Iona's boots: "The sick motor through them." then "Then not." The film's sound plan made that silence the film's planned break in sound. The checker still flags the silence as "an added change" on a moment the script already marks.

It is wrong twice over:
- The "mark" it found is the word "lamplight" in a different line, about a floating screw. A light word should not stop a sound change.
- The silence is planned. But my repair after the cross-examination (entry 34) now asks the sound plan to point at the exact moment, by quoting the story, and step 6 never tells the writer to do that. The helper wrote the sound plan at step 6, before any beats existed, so it named only the scene.

This false alarm partly comes from my own repair. The fix: tell step 6 to quote the moment, and stop a light word from counting against a sound change.

## What was done

| Part | Result |
|---|---|
| Pieces of work | 50: 37 for planning the whole film, 13 for the three scenes |
| Time | about 96 minutes |
| Scene 2, the ladder climb | 6 beats, 12 shots, about 65 seconds; one piece of design, one batch of shots |
| Scene 13, the glass partition (the most talk) | 16 beats, 37 shots, about 253 seconds; split into two parts once, at the start, and never planned again (problem 5's fix worked) |
| Scene 26, the climax | 8 beats, 20 shots, about 110 seconds |
| Most repair rounds in one piece | 2 (the limit is 3) |
| Final full check | 1 error (a code fault, below) and 4 warnings |
| Book | made; format checks passed |

## The warnings left on each scene

| Scene | Warning | The helper's verdict | Mine |
|---|---|---|---|
| 2 | Two shots in a row are too alike (same size, only 15 degrees round her) | False alarm: the second camera is 1.1 m lower and tilted up 40 degrees, so the real angle between them is about 42 degrees | Agree. The check measures only the turn round her on the floor plan, never the height. |
| 13 | Saye, the silent third person, is in no shot of a turn | The helper's own slip at the design step: the turn's picture puts Saye behind Eli, but no camera there can see her, and the shot step may not add a camera | Agree. A real fault, which only redoing the design fixes. No check compares a turn's picture with its cameras. |
| 26 | A planned silence counted as an added change | False alarm | Agree; see the example above. |

The final full check also listed a whole-film warning: three loud places where a short film allows two. That was the helper's own slip at step 4.

## Compared with the earlier tests

The scenes and the helpers differ between tests, so this is a rough comparison, not a measurement.

| | First test (entry 23) | Full run (entry 31) | This test |
|---|---|---|---|
| What was left at the end | 44 problems, most of them impossible to clear | 1 error nobody could clear and 126 warnings, 40 of them the turn-size rule arguing with the film's own plan | 1 error (a code fault) and 4 warnings: 3 on the scenes (1 own slip, 2 false alarms) and 1 own slip at step 4 |
| Turn size against the film's plan | not measured | 40 warnings | 0 |

## What still goes wrong, most important first

I checked the first two and the book's contradiction myself. The rest come from the helper's log, with its commands and outputs.

1. **Errors that belong to later pieces of work (43 of the 92 errors before repair).** These cleared by themselves later, but they make a piece of work look broken:
   - the scene-plan pieces were asked for groups of scenes and planned lengths that only the next piece writes;
   - step 5 asked for the answers to the big choices before you were asked them;
   - each part of a split scene was asked for the beats and shots of the later parts.
   The approval mark had the same problem and was fixed (entry 32). These three need the same treatment: "not due yet", never an error.
2. **An error at the end that no step had filled yet.** The date of the video-model prices is filled only by the cost estimate at step 10, but the check asks for it earlier. Its advice ("run build") does not help.
3. **The planned silence in scene 26** (the example above).
4. **"Two shots too alike" ignores camera height** (scene 2).
5. **The book contradicts itself where the shot step changed a shot.** The one-line list prints the shot list as approved, and the full shot below it prints what was written. In scene 13, shot 250's line has Iona listening to the second half of Eli's speech, while shot 240's full shot already holds the whole speech. Other book faults:
   - state numbers no reader can use ("Iona, state 6");
   - "saved choice 1/4";
   - floors with two decimals ("17.21 seconds");
   - a plant and a motif with the same name printed twice in one line;
   - one raw value, "seated:Jude";
   - a rule's title used as if it were a name.
6. **"Pause after: none" is refused,** although the template offers "none". The helper had to write "none | seconds: 0 | ...".
7. **Footage of an earlier time** ("recorded: scene 6") reads the states at the end of scene 6. That was wrong for footage of its middle. A quoted moment works, but no instruction says so, and the checker's own advice pointed at the wrong state.
8. **Splitting a long speech over two shots:** card 13 says you may, but the time and citation checks refuse it. The two must agree.
9. **Smaller code faults:**
   - "apply" reads the inbox path relative to the current folder, and its message names that same path as the place to write;
   - an empty record is accepted without a word;
   - a single letter "F" matched a text from another scene;
   - footage from an in-story camera looking straight down was counted as using the film's own saved top-down shot;
   - the rule that a look description has 2 or 3 sentences is never checked;
   - "what's next" names the next piece even when the last check failed;
   - after the scene-list checkpoint, "apply" suggests a full check, which then prints 178 problems for later steps;
   - after a refused apply, the check still reports on the old files;
   - some advice tells the AI to write fields only you may set.
10. **The planning steps are still unclear in places.** These items were in the full run too, and were left for later in entry 32:
    - the self-test handout does not print the allowed values;
    - the start handout's list of what to write is wrong;
    - nothing says that a choice with nothing to set writes "sets: none";
    - how to say "only these scenes" is in the main instructions, not in step 1 or at the scene-list question;
    - how to name the people a rule governs before they exist;
    - whether one room named three ways is one place or three;
    - which fields a silent extra skips;
    - one likeness choice per character, or one for all;
    - whether unchanging things need a state to carry their side in the mirrored world;
    - sides set by choices (the example) or by state lines (the step file);
    - which piece writes the frame rate;
    - a name check that needs a web search.

## The craft

- The helper caught itself writing "Iona's husband" as Jude's role and cut it, because the script never says it. The full run's book had printed "her husband's bed". The rule against adding facts is working.
- It found three of its own staging slips that no check catches. In scene 13, a camera has Iona standing right between it and Jude. A remote is left on a table, which conflicts with "Lets the recording run." In scene 26, a move starts several seconds before the line it belongs to. A check comparing moves and cameras with the shots would catch these.
- The book pages "read in plain words", and every quotation from the story was exact.

## What was tested, and what was not

**Tested:**
- The whole kit from a new project to the book, for the planning and three scenes, by a helper that had seen none of the fixes made.
- I reproduced "pause after: none" being refused, and the book's contradiction in scene 13, myself.

**Not tested:**
- The other 27 scenes.
- The whole-film pass, the scores and the other exports.
- A real person answering the questions.
- The chat apps, The Long Places, pictures and video.

**Unsure:**
- One helper on three scenes is a small sample. Another helper might trip on different things.
