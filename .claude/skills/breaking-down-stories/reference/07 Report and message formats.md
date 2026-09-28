# Report and message formats

Every message the user reads takes one of these shapes: keep the parts and their order, and fill them from the project. The examples come from The Catch and The Long Places; real numbers come from the records and the estimate. In every message: the user's words (scene 10, shot 150, beat 7, camera B, group 3, choice 21, saved choice 1, take 3), never internal codes, check names, research codes, checkpoint letters or abbreviations; each place where the user answers named by what it is (the rights question, the scene list, how the book becomes a film, the big choices, each group of shots, the finished check, which of three styles, the grey previews, keeping takes); steps counted from 1, out of 12, and add-ons named, not counted; each question's default in square brackets at the end of its line; a new craft word explained once and added to the word list in 00 Start here; one next step.

## Every reply's ending

Four parts in this order, then the next step:

```
Done: scene 11 of 30, step 9 of 12, writing the shots.
Example from your story: shot 150 is the turn of scene 10: Iona's close-up held
  15 seconds, from the first chew through Saye's answer.
Made: 11 Scenes/Scene 11 - Treatment floor (20 shots).
Needs you: nothing.
Next: scene 12.
```

In chat apps two lines follow:

```
Save as: 11 Scenes/Scene 11 - Treatment floor.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 02 Whole-film summary,
10 Film rules, 10 Steps 07-08 - scenes and shots, your story and Scene 11 - Treatment
floor; type: Continue my breakdown. Next is scene 12.
```

At the end of a group of scenes the next step is the check: "Next: a check. New chat in this project; attach the files of scenes 7 to 10, your story, 02 Whole-film summary, 10 Film rules and 05 Checks in words; type: Check my group of scenes."

## The welcome

```
Hello. I'll turn The Catch into a scene-by-scene plan for making it as a film,
including with AI picture and video tools.

Here is one finished moment from your story, so you can see what you'll get:
  Scene 10, shot 150. Close-up, camera still. Iona chews the leaf. She stops,
  frowns, chews once more, slowly. "Not mint." We stay on her face while Saye
  answers off screen. About 15 seconds.
  Why: "Her face changes." The scene turns inside her mouth, so we don't cut away.

How it works: I do the work. You'll be asked to choose about four times (the scene
list, the big choices, the first group of shots, and the finished check), each
with an answer ready if you just say "defaults". You can stop any time and carry
on another day: everything is saved in files with plain names.

I'll make a complete shot plan (standard). Say "quick" for one line per shot,
or "detailed" for extra detail on every shot.

One question first:
1. Is this story yours, or do you have permission to adapt it?   [It's mine]
```

If it is not theirs and they have no permission: "Then I'll plan it for your private study only. Every file will say 'Private study, not for publication', and I won't make video prompts for public release."

## The scene list

```
Done: step 2 of 12, reading the story.
Example: scene 10 is Saye's kitchen, lines 397 to 489. Saye speaks 10 times, Iona 4,
  Jude and Eli once each. It ends with a cut to black and the title card "THE CATCH",
  which becomes its own shot.
Made: 03 Story - numbered, 04 Scene list, 14 Time and cost (a first estimate).
  I found 30 scenes, one for each heading in your script.
  Small choices I made (1): I treat it as a short film (under 40 minutes).

The scene list. One question. Reply "defaults", or answer it.
1. Length: as written it runs about 35 minutes (32 to 38; the page count suggests
   up to 44). Keep everything, or give me a target, for example 20 minutes?   [keep everything]
Next: I'll plan the whole story: its turns, its climax and its groups of scenes.
```

For a book there is no question: "Done: step 2 of 12. I found 14 chapters, 49,152 words; I'll plan the whole book next."

## How the book becomes a film

```
Done: step 3 of 12, planning the whole book (14 chapters, 49,152 words).
Example: in plan A, chapter I gives five scenes; the fifth is Nilay on the threshold.
Made: 05 Story plan (14 chapter digests, 11 strands, three plans).

How should the book become a film? Reply "defaults", or answer by number.
1. A. A feature, about 100 minutes, 48 scenes; keeps Nilay and Emre whole, loses Malta.
   B. Six episodes of about 48 minutes; keeps nearly everything.
   C. A 15-minute short from chapters I and XIV; keeps the brother and the ending.  [A]
2. Start with chapter I as a trial (5 of the 48 scenes).                         [yes]
3. Small choices I made (3), listed in 01 Choices.                            [accept]
Next: characters, places and things for what the plan keeps.
```

## The big choices

At most `checkpoint_b_items_max` numbered items, in this order: the climax; style and frame shape; place and time; music; the story-world rules; what each main character's appearance must say; small choices I made. A star marks the `checkpoint_b_marked_items` items that would redo the most work if changed later.

```
Done: steps 4 to 6 of 12 (world and style; characters, places and things; continuity).
Example: Saye's fixed description now reads "Dr Saye, a slight, upright woman in her
  fifties, ...". It goes word for word into every picture prompt with her.

The big choices. Reply "defaults", or answer by number.
*1. The climax: the crossing beside the ship (scenes 26 and 27).        [26-27]
*2. Style and frame shape: clinical and plain, for now; wide frame, 2.39 to 1. [yes]
 3. Place and time: an unnamed British city, today, British voices.     [yes]
 4. Music in the finished film: none; the pump does its job.             [none]
*5. The mirror world: from "Her eyes open." (line 263) the world is mirrored
    around the three of them.                                     [as written]
 6. What each main character's appearance must say (the rest in 07).  [all fine]
 7. Small choices I made: 23 in 01 Choices.                           [accept]
Next: I'll write the film's camera, light and sound rules, then design scene 1.
```

## Each group of shots

The first group waits for the user and adds, before its question:

```
The film's rules, in five lines (a change here costs little now):
  1. The camera stays still, at the eye height of the person the scene belongs to.
  2. It breaks that rule once, in scene 26, when she pushes away from the rail.
  3. Eli is never pushed in on; his closest shots are saved for scene 13.
  4. The film's tightest shot is saved for scene 13; the crossing is played wide and still.
  5. No slow motion and no music: the pump and the engine click do music's job.
Needs you: reply "next", or tell me what to change.
After this group I'll carry on and show you each group; say "stop after each group"
if you prefer.
```

Later groups report and carry on:

```
Done: group 3, scenes 7 to 10 (step 8 of 12). 58 shots, about 4 minutes.
Example: shot 150 is the turn of scene 10: Iona's close-up held 15 seconds.
Made: 11 Scenes/Scene 07 to Scene 10. Checked: no problems. One added detail changes
  a scene, to keep or cut: Iona sets the lamp down (scene 10). 6 small additions kept.
Scene 10 - Saye's kitchen - 20 shots and a title card - about 1 min 36 s
 shot 150  15 s   the turn: close-up, Iona chews, stops, chews once more; "Not mint."
 (the other 19 shots are listed in the scene file)
Needs you: nothing. I'm carrying on with group 4; tell me anything you want changed.
Next: scene 11.
```

## The finished check

```
Done: step 11 of 12, the health check. In short: one thing needs you (reading three
  scenes); 14 small fixes I made; 3 warnings (listed in 13 Health check).
Example: the film runs about 36 minutes in 468 shots; making it with AI would cost
  about $2,900 to $7,600 and 45 to 90 hours of watching takes (14 Time and cost).
Made: 13 Health check, 14 Time and cost, and a first version of 15 The breakdown.
Needs you: please read three scenes in 15 The breakdown (about 20 minutes): 26 (the
  climax), 13 (the most talk), 06 (the most action), with the 10 questions in
  05 How to read your breakdown.
  Anything you want changed in these three scenes?                            [no]
Next: I'll finish the book, the spreadsheets, the captions and the timeline.
```

Without code, the three scenes are read as the plain parts of their scene files. The book step's last message names the three files to open first and one next step for this project: 'Next, if you want to see it: say "make storyboards" (about $10 and an hour).'

## Add-ons

- Storyboards start with which of three styles: "Which of these three styles? [A]", one frame of each on three hard shots.
- The grey previews: "Here are the grey previews for scene 10. Reply with the numbers of any that look wrong, or 'fine'. [fine]" Outside Claude Code: "Grey previews need Claude Code on your computer; everything else works here."
- Keeping takes: the spending cap first, asked once and never defaulted; then each take with a suggestion: "Take 3 of shot 150: keep it? [keep]"
- At quick depth, once: "Quick plans can't be turned into AI video prompts until a scene is made standard. Say 'go deeper on scene N' for the scenes you want to make."

## Resuming

- Claude desktop with a folder, Claude Code: "Yesterday we finished scenes 1 to 12. Next: scene 13. Nothing is waiting for you."
- The Claude website and ChatGPT, when the chat is long: "This chat is getting long. Start a new chat in this project, attach the save file, and type: Continue my breakdown." The save file is named like "023 Save - The Catch - after scene 10.zip". On ChatGPT add: "Download it now: the link expires."
- Chats without code: the "To continue later" line, naming every file to attach.

## When something goes wrong

The user types only the word in bold.

- Cut off: "My reply was cut off inside shot 170. Type **continue** and I'll send it again from shot 170." Shots skipped: the same, sending only the missing shots.
- The chat is full: the resume message above. A problem my repairs could not fix: one plain question with a default.
- An early choice changed: "The 16 to 9 frame touches the picture edges of 214 shots, 31 grey previews and every prompt page; about 20 minutes. Go ahead? [yes]"
- A file lost: "Scene 10's file is missing. I'll restore it from your last save." (Without code: "I'll make scene 10 again from your story.")
- A file I cannot read to the end: "I can't see the end of your story file. Please paste the part from scene 29 to the end."
- Something not in the story: "I couldn't find the blue door in your story, so I've marked it as added."
- A refusal: "This app would not plan the gunshot in scene 6, even as film planning. Please try scene 6 in another app; everything else carries on here."

## What the user can type

Break down my story. · Continue my breakdown. · Where are we? · Why shot 150? · Change ... · Go deeper on scene 13 · Quick / Standard / Detailed · Redo step 6 · Stop here · Check · continue · next · defaults · stop after each group · Make storyboards · Make grey previews (Claude Code on your computer only) · Get it ready for AI video · Plan the edit. Their own words work too.

## 00 Start here

Six plain sections, in order: **Where things stand** (step and progress; "Checked by the checker: never", or the date; "41 small additions kept; the list is in 01 Choices"; anything waiting). **Next step** (the exact message to type, for this app and the others). **Big choices so far** ("1. The whole script, about 35 minutes (choice 5)"). **Files in this folder** ("Each file's number is its place in the list Files in this folder; the log below records every change."). **Word list**. **Log** ("017 2026-10-02 Scene 10 designed: 11 beats, 20 shots; one invention listed (the lamp)"). Then the divider line, the project record and the END line.
