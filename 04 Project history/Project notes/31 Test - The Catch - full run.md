# 31 Test - The Catch - full run

The first complete run of the kit: all 30 scenes of The Catch, from "Break down my story." to the finished book. Log entry 31 in "Stage - project story.md".

## What happened, in short

**The kit got all the way through.** It made a breakdown of the whole film: 514 shots, about 43 minutes, every scene with its shots, reasons, sound, timing, captions and cost. The book reads well. 29 of the 30 scenes pass the kit's own scoring, and the one that fails misses by a single point.

**What it means for your idea:** the approach works on a whole film, not just on a few scenes. But it was harder than it should be. The checking program argued with itself in about a dozen places. The AI helpers could not satisfy both sides, so they worked around the problem or left warnings standing. Most of this can be fixed in the code and instructions, without changing how the kit works.

## One example: the climax (scene 26)

Iona stands on the outside of the falling ship and works out how to get home. The book's page for this scene opens like this:

> 14 beats, 23 shots, about 1 minute 28 seconds. The turn is beat 14, in shot 230.
>
> - shot 070, wide, 4.5 seconds: the same wide from the east end, held: she hangs a hand's breadth above the deck with the screw beside her; the stars do not move and there is no feeling of speed at all
> - shot 080, insert, 6 seconds: on the inside of her visor she selects the crossing preview: her projected outline turns red on one frame, far below the receiving room, below the loading tunnel, inside solid rock and still travelling down; she cancels the preview and the outline is green again
> - shot 230, wide, 8 seconds, the turn: held long, on the widest lens: she pushes gently away from the rail and the camera leaves its fixed place and drifts free with her while the ship falls away behind

Each line of the script has a shot, in story order. The camera stays fixed to the ship for the whole scene, then breaks free for the first and only time at the moment she lets go. That was planned at the start of the film and kept until scene 26.

**One fault on the same page:** the "why it's shot this way" lines print the kit's internal names, for example "A break from CAMSYS" and "(PLAN peak camera_break)". You should never see those.

## How the run was done

- **Planning (your steps 1 to 7)** was done by one helper on the main model. It covered the story plan, world and style, characters, places, things, continuity and the film rules.
- **The scenes (your steps 8 and 9)** were done by 10 helpers on Sonnet 5.5, one after another, one per group of scenes. The kit calls a group of scenes a sequence.
- **The finish (your steps 10 to 12)** was done by one more helper on Sonnet 5.5: the whole-film check, the scoring, the cost and time, and the book.
- **The "user" was simulated.** It answered "defaults" to every question, "next" at every group of shots, and "no changes" at the end.
- **The helpers were only allowed to use the kit.** They could not read my notes or the tests, and could not change any kit file. Each kept a log of every problem and unclear instruction: 254 notes, about 11,600 words. I read all of them and did this analysis myself, as you asked.
- **It ran from the evening of 28 September to early on 30 September.** In the middle, it stopped for many hours while the command safety checker was broken (log entry 30).

## What it made

| What | Result |
|---|---|
| Pieces of work (units) | 180 |
| Shots | 514, in 30 scenes, average 4.9 seconds |
| Film length | about 42 minutes of story, 43 with titles and credits |
| Book | 15,112 lines (1.3 MB), as a web page and as text |
| Shot list spreadsheet | 514 rows, 20 columns |
| Captions | 1,413 lines, with speaker names only where the speaker is off screen |
| Audio description script | 364 items |
| Edit timelines | two formats, 514 events each, format checks passed |
| Cost to make it with today's video models | budget $2,742, middle $4,696, premium $11,445 (mixed plan $5,221), prices checked 27 September |
| Your time to make it | about 512 hours (394 to 788), about 26 weeks at 20 hours a week |

## How good is it

**Scoring.** The kit scores each scene on 10 questions, each from 0 to 3, and 20 of 30 is a pass.
- 29 scenes pass, and the average is 22.
- The best are scenes 3, 4, 10 and 25, at 24 each.
- Scene 30 fails at 19. It runs 56 seconds against a planned 36, and its video prompt asks the model to draw the words "THE END" (video models write words badly).
- Because one scene fails, the whole film does not pass (18 of 30).

**Review questions.** The kit made 2,033 yes-or-no questions about the shots, such as "Does this shot show only what the script gives?".
- 25 answers were "no". 15 of those were small invented details, such as a door sign reading "FIRE EXIT" or a date on a label. They were either accepted with a reason or were already listed as additions.
- 10 were real mistakes. Eight were fixed. The other two were about the same thing, which way round the last label reads, and went to the user as a question. For example, one fixed mistake was a count of "two words" for "Not that one.", which is three words.

**The book.** The finishing helper read three scene pages: the climax (scene 26), the scene with the most talk (13) and the biggest action scene (6). I read the climax page's shot list and checked the faults it found.
- The shots follow the script closely and in order.
- The strong choices are rationed across the film. There is one extreme close-up in the whole film (scene 13, shot 290) and one camera break (scene 26).
- **The camera almost never moves:** 512 of the 514 shots have a still camera. The planning helper chose this style at the big-choices question, and the simulated user accepted it with "defaults". It is a strong choice, and a real user might want a different one.
- About a third of the shots (164) are inserts: close views of hands, objects, screens and the visor display.
- Scene 13's staging line says Iona goes "only as far as her husband's bed". The script never says "husband". It is a fair guess from the wedding rings, but it is printed as fact.
- Scene 13 lists the same addition twice.
- The "why" lines in the book print internal names 60 times: CAMSYS 13, SOUNDPLAN 6, LADDER 35 and "PLAN peak" 6.

**The final check.**
- 1 error and 126 warnings. An error is a problem the checker says must be fixed; a warning is one it only points out.
- The one error is in text the checker wrote itself, so nobody can fix it (problem 2 below).
- Most of the warnings come from rules that contradict each other (problems 8 to 11 below).

**The video prompt check** found 133 problems. Many are false alarms (problem 14 below).

## What went wrong, most important first

For each problem: what happens, one example, and the fix I would make. The line starting "For maintainers" gives the technical names, so the fix can be found in the code.

### Bugs in the code (small, clear fixes)

**1. Jump cuts are invisible after shots numbered below 100.** A jump cut is a deliberate cut between two shots from nearly the same place. The kit warns when two shots are too alike, unless you mark the join as a jump cut. For shots 010 to 090 the mark is never found, because the program drops the zero ("070" becomes "70"). Three helpers hit this, in scenes 3, 11 and 29.
*Fix:* keep the zero. One line.
For maintainers: `checks_sides_geometry.cut_after` builds `f"{scene}-C{int(number.group(1))}"`; use `number.group(1)`.

**2. One error can never be cleared, and the kit never says "finished".** The checker wrote a suggested fix containing "...", and its own rule forbids "..." in records. The AI is not allowed to edit text the checker wrote, so the error stays for ever. Because of it, "what's next" keeps sending the AI back to the film pass, even after the book is made.
*Fix:* never write "..." in the checker's own text. Also make "what's next" say "finished" once the book is made.
For maintainers: FORM-08 on FIND-005 `fix` (FILM-01's fix text holds "reason: ..."). `next` routes back to step 9 on any `check --all` error; add a "finished" state after step 11.

**3. The kit wrote into its own example folder.** A helper ran two commands from the Stage folder without naming the project. The tool picked the example folder (The Catch, scene 10) and rebuilt it. **Already fixed during the run** (entry 29): from the Stage folder, the example is never picked.

**4. The approval mark reports an error that nobody can fix.** When a scene's shot list is written, the checker reports "approved is missing" as an error. It says "run build", which does nothing. The step instructions say a special command approves the list, but a plain "what's next" already does it, and the special command then says nothing is waiting. All 10 scene helpers reported this.
*Fix:* don't count a mark only code can set as an error, and make the instructions match what the code does.
For maintainers: FORM-05 `SHOTLIST.approved` (code_state) should be "not yet due" until checkpoint C; steps 07 and SKILL.md say `next --checkpoint-passed`, but plain `next` approves.

**5. Long scenes get planned twice.** A scene with more than 14 beats is meant to be written in parts. Scene 6 was offered as one piece of work and written whole. Then "what's next" re-planned it in parts and handed out new beat numbers for beats that already existed.
*Fix:* decide the split once, before the first handout, and never re-plan a finished scene.
For maintainers: `scene_split_beats` is applied after apply; the plan must be fixed when U-07 is first issued.

**6. Handouts are too big.** The handout for writing shots was 21,000 to 50,000 tokens. That is 2 to 4 times what the AI's file reader takes at once, so every handout needed several reads. A token is roughly three quarters of a word. The scoring handout was 175,000 tokens, with no way to split it.
When a handout is too big, the kit cuts parts of the knowledge cards the step needs most. For example, the mirror rule was dropped from the world step.
*Fix:*
- Leave out the 2,033 answers from the scoring handout; give counts instead.
- Cut repeated records before cutting card parts.
- Make the promised part-units for the judging and scoring steps.

**7. What you read on the health check page depends on which check ran last.** A check that checks nothing, the one for the book step, rewrote the page to "no warnings". The scores are never shown in plain words, although the guide says they are.
*Fix:* only a full check writes the plain part, and it includes the scores.

### Rules that contradict each other (the AI cannot satisfy both)

**8. How close the camera goes at the turn.** One rule says a scene's turn must be the closest shot the character's camera rule allows. But the film's own plan (the "ladder", which sets how close each scene's turn goes, so the film builds) often asks for a wide or medium shot on purpose. Also, shot sizes may not change after the list is approved.
This one rule gave 40 of the 126 final warnings. Example: scene 26's turn is the planned wide shot of Iona letting go, and the checker asks for an extreme close-up there. The film rules forbid an extreme close-up in that scene.
*Fix:* the ladder wins, and the checker compares the turn with the ladder rather than with the camera rule's closest size.
For maintainers: CRAFT-03 against LADDER, RESERVE and ID-08.

**9. Light and sound.** One rule wants a light change wherever the script writes light. Another warns when a light change is added on a moment the script marks. Planned silences count as "added changes", one light cue counts twice (as light and as colour), and "grey" in "grey and tidy" hair is read as a light word.
*Fix:* a light cue that quotes the script's own line satisfies both. Planned silences from the sound plan don't count, and colour words about people are ignored.
For maintainers: COVER-08 against CRAFT-10 and CRAFT-19.

**10. Timing.** One rule gives a scene room to breathe after an intense one, and another then flags the longer scene. The time the plan promises for each shot leaves out the time needed to read words on screen and the pause owed after a turn. So the approved times can't be kept, and scenes come out 15% to 25% longer than planned.
Word reading time is checked on a blurred background sign but was not checked on plot-critical visor text in scenes 26 and 27.
*Fix:*
- Include reading time and owed pauses in the promised time.
- Check reading time only on text the audience must read.
- Measure scene length against the scene's design, not the first word-count guess.

**11. Hiding a secret.** When a shot shows something the audience must not understand yet, the kit says to write "keep hidden, and how". But the warning only goes away if the thing is deleted from the shot's list of what's in frame. So helpers deleted things that are really on screen, and the shot list under-reports what's in frame.
A related false alarm: naming the idea of "labels" set off a warning about every labelled object in the film.
*Fix:* "keep hidden" must clear the warning.
For maintainers: INFO-01 ignores `keep_hidden` and expands MOTIF to every carrier.

**12. Things with no state yet.** A prop can only be named in a shot once its continuity record starts. When continuity missed an early appearance, the shot writers were not allowed to add it, so they left the prop out. Examples: the courier in scene 18, and the transport shell in scene 15.
A recording that shows an earlier time can't be described at all. For example, the puck whole on the tablet in scene 13, when it is burnt by then.
*Fix:* let the shot step add a missing continuity state as a flagged addition, and let a shot say "this is footage from an earlier time".
For maintainers: STATE-01; step 8 "You write: SHOT, CUT".

### False alarms

**13. Wrong words flagged.**
- The retired-word list flags ordinary English because some field names are English words: "movement", "bed", "her look", "withholding".
- "as before" in a plain sentence is read as a shortcut.
- "scar" in "bullet scars in the roof" is read as a body scar.
- "Left palm" is matched to the other hand.
- A black screen in the middle of a scene is told to renumber as if it were the end.

*Fix:* check whole phrases in context, and allow a black screen mid-scene.

**14. The video prompt check (133 problems).** Many are not real:
- "cage" is banned in prompts, and the project swaps it for "open steel freight elevator car", but the swap is not applied to the place descriptions pasted into the prompt.
- "THE END" is flagged on shots that show no text.
- The F on the toy carriage is flagged as "text to draw", but seeing the F flip is the point of the shot.

*Fix:* apply the swaps everywhere, flag only real text, and let a shot mark text that must be drawn.
For maintainers: GEN-12, GEN-06 and GEN-05 need compiler rules; GEN-15 wrongly flags quoted script lines.

### Missing instructions

**15. Rules that live only in the code.** Helpers found these only by being warned:
- one main action per 4 seconds of shot;
- the formula that turns lens and distance into shot size;
- cameras may not stand inside furniture;
- which fields count as showing the key moment;
- a speech's words are on the line after the speaker's name.

Also, the shot handout says the lenses are 28, 40 and 75 mm for the whole film, but from scene 11 the film rules change them to 40, 75 and 100. And the handout does not give the speech numbers the shots must name.
*Fix:* put each rule in the step file and the handout, and use the film rules' lens change.

**16. A wrong field can't be removed.** Writing "none" is refused, so a mistake stays stored. A place with no floor plan can't say where the camera looks.
*Fix:* allow "none" to clear a field.

**17. No record for the animal.** The creature inside the figure acts in scenes 26 to 30, but it can't be a character, so it can't be the one who acts in a beat.
*Fix:* allow a character that does not speak and is not human.

**18. The last steps are thin.** Several things at the end have no instructions:
- no instructions for where the user's final answers go;
- nothing to say where the film's own review answers come from;
- some top scores cannot be reached at this depth;
- two different film lengths are reported (42 and 43 minutes).

*Fix:* write the missing instructions, and report one length with "plus titles".

## The rule for switching the file format

The blueprint set a test: if format errors outnumber craft errors, the kit should switch its record files to a stricter format that people can't read (JSON).

**The numbers trip the rule.** Format errors before repair were 192. Craft, reason, timing and geometry errors together were 90.

**But the format itself was not the problem.** From reading the logs:
- Most format errors were "missing field" reports. Many were for fields only code fills, like the approval mark in problem 4, or fields not due yet.
- Most of the rest were refused values such as "none" (problem 16).
- The headings and field lines themselves caused no reported errors. The END line's record count caused about 13.
- I could not get exact counts of each kind from the logs; this comes from reading them.

**My call: keep the readable text format.** Change the switching rule so it only counts real layout mistakes.

## What was tested and what was not

**Tested:**
- The whole kit, on one film, in Claude Code, with the Stage checking program.
- Every step, from the start to the book and exports.
- The format checks on every export file.

**Not tested:**
- **A real person.** The user's answers were simulated, and always "defaults" and "no changes". Nobody chose anything or changed a scene.
- **Truly fresh reviewers.** The 2,033 review questions were answered by the finishing helper. It wrote none of the shots, but it is the same kind of AI.
- **Pictures, videos and voices.** Nothing was sent to a video model. The prompts stop at "checked and priced".
- **Grey 3D previews.** None were made in this run.
- **The chat-app route** (ChatGPT, Gemini) and **The Long Places**.
- **Whether the fixes above work.** None of problems 1 to 18 is fixed yet, except problem 3.

**Unsure:**
- The quality judgement rests on three scene pages and the scores. Nobody has read all 30 scene pages.
- The cost figures are only as good as the model prices, which change often.
