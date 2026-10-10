# Step 12. Add-on - storyboards

This is add-on A, "storyboards". The user asks for it ("Make storyboards"); it is not counted among the 12 steps, and nothing else depends on it. Read this file at the start of every unit of this add-on, never from memory.

**One-line task:** Make storyboard frames: first the three-style test if the style is still provisional, then one kept grey frame for each chosen shot, drawn at the shot's most telling moment, and a page per scene the user watches with the sound off.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Let the user see the film before anything costly is made. Example: shot 150 of scene 10 becomes one grey charcoal frame of Iona's close-up at the moment she stops chewing, eyes on Saye just right of the lens; under it the page prints "shot 150", its one line, "Not mint.", its seconds and a hold label. A frame that cannot tell its beat with the sound off shows a problem in the shot, which is fixed in the shot, not the drawing.

## When it runs

On request, after the book and exports, on any app. Default frames: the shots with `storyboard: yes` (turn and must-keep shots, about a third); on request, every shot; at quick depth, one frame per list item marked turn. Turning storyboards off changes no other file.

## Inputs

SHOT records (list items at quick depth); STYLE; each subject's fixed description and state line; the LOOK of each place and time; LOCATION and PROP; approved reference pictures when the storyboard is consistent; a grey preview still when one exists, which becomes the frame's layout picture.

## Outputs

- The style test: nine PIC records (`use: style`), three directions on three shots, and a CHOICE whose answer sets `STYLE.style_picture` and clears `STYLE.provisional`.
- `18 Storyboard/Storyboard frames.md`: one PIC record (`use: storyboard`) per kept frame.
- `18 Storyboard/Scene 10 - frame prompts.md`, compiled by code; `18 Storyboard/Scene 10.html`, the page, laid out by code.

## Card parts to open

At every depth: card 21, whole.

## Procedure

1. **The style test** (U-12-STYLETEST), once, and only while `STYLE.provisional` is yes; add-on C may already have run it (D5 §7.1). Propose three directions, one of them photographic, each in `style_words_count` style words that describe qualities and never name a film or an artist. Draw each on three shots from the breakdown, quoting their lines: a face that must read (scene 10, shot 150), a wide of the world (shot 190, the kitchen held from the high corner) and one hard shot of mirror, text, creature or physics (shot 80, the reflection). Score each frame on D5 §7.2's criteria; the hard shot counts double. Ask once: "Which of these three styles? [A]". If the user cannot choose, choose by the hard-shot scores (D5 R12). A changed style marks fixed descriptions, look blocks and compiled prompts stale (`stage.py impact`).
2. **The kind, asked once.** A quick storyboard uses fixed descriptions only, no reference pictures: composition is what matters. A consistent storyboard makes reference pictures first (C2 Rule 1), and is needed if frames will later become start pictures. Default: quick.
3. **Compile the prompts.** Run `stage.py compile --storyboard`. Per frame it writes the greyscale style line (charcoal and grey marker, four tones, strong light and shadow shapes; C2 §2.1), framing words from the shot, the fixed descriptions and state lines word for word, the look block's light sentence, the references in stack order, the save-as name and three yes/no checks. Never retype a prompt; fix its record and compile again.
4. **The moment.** A frame is drawn at the shot's most telling moment, which may compress an action; a start picture made later is composed again for the shot's first instant (C2 §2.2). Letterbox bars for a 2.39 frame, arrows, numbers and labels are drawn by the page, never inside the picture (C2 R3). Readable words are never drawn by the model: it gets a blank surface (C2 Rule 9).
5. **Make the frames** (U-12-SC10, one scene per unit). Up to two options per shot; keep the one that passes its three checks and write its PIC record: `for`, `use: storyboard`, `moment`, `model` (the exact name), `references`, `file`, `checks` (each answer), `approved: yes`, `cost_usd`. The user is not asked to pick. Checks come from the records: "Is Saye's ring on the hand that looks like her right?" A frame that fails both options is a finding on its shot.
6. **Spending.** Through an image service, nothing is spent until the user has set the most one batch may cost (`spend_cap_usd`), asked once and never defaulted. About 300 frames cost about $10 in batch (C2 R3); the pasted chat path below costs nothing extra (C2 Rule 6).
7. **The page.** Code lays the kept frames out per scene: the frame, "shot 150", the one-line description, the dialogue, the seconds, and the labels it adds (hold, room sound, eyeline arrows).
8. **The slideshow.** The user watches each group of scenes with the sound off and names only frames to redo. If a beat cannot be read, revise the shot (step 8's record, with its impact), then redraw.

## Record template

`references/templates/18 Add-on jobs.md` (PIC), `references/templates/01 Choices.md` (CHOICE).

## IDs you will be given

A PIC is named by what it is for, its use and a number: `PIC-SC10-SH150-STORYBOARD-01`; a redrawn frame takes the next number (`-02`), never a used one. Style-test frames: `PIC-SC10-SH150-STYLE-01` to `-03` for directions A to C, the same for shots 190 and 80. The choice takes the next free number from the handout.

## Batch and chunk rules

The style test is one unit, once. Frames go one scene per unit, in scene order, one group of scenes at a time, each unit reading only its scene's shots and the records they cite. The slideshow is per group of scenes.

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Does every shot with `storyboard: yes` have a compiled frame prompt?
2. Does every kept frame pass its three checks, with its answers in its PIC record?
3. Was the style test run once, and did its answer set the style picture?
4. Are all arrows, bars, numbers and labels outside the picture?
5. Is every fixed description and state line pasted word for word, with no film or artist named?
6. Was nothing spent before the spending cap was set?

## The report

```
Done: storyboards for group 3, scenes 7 to 10: 24 frames.
Example: shot 150 is drawn at the moment Iona stops chewing, her eyes on Saye
  just right of the lens; the page marks it "hold" and "room sound".
Made: 18 Storyboard (a page for each of scenes 7 to 10).
Needs you: watch each page as a slideshow with the sound off. Reply with the
  numbers of any frames to redo, or "fine".                                 [fine]
Next: storyboards for group 4.
```

## Checkpoint

Which of three styles. It waits: "Which of these three styles? [A]", with one frame of each direction on each of the three shots. For The Catch, for example: A, like a real film, clinical and plain; B, painted, broad brush and muted colour; C, stop-motion, small handmade sets in soft light. Then the kind, once: "Quick frames drawn from the written descriptions, or frames that keep each face and place the same from shot to shot (slower; needed only if the frames will later start AI video)? [quick]". Through an image service, the spending cap first: "What is the most one batch of pictures may cost, in dollars? Nothing is spent until you say." (no default). After it, a slideshow per group of scenes; the user names only frames to redo, and "fine" accepts them.

## How to redo

"Redo the frames for scene 10": new options for its shots, each a new number; the kept frame is replaced and the page made again. A change to a shot marks its frame stale, and it is redrawn with the next group.

## If you cannot run code

Every line reference is a quote anchor: each frame check quotes the line it rests on ("Is Saye's ring on the hand that looks like her right?", with "On her right hand."), never a line number.

1. The style test comes first, the same way: nine prompts (three directions on the three shots), then the one question. Then write the frame prompts yourself from the records and card 21, pasting fixed descriptions, state lines and the look block's light sentence word for word, in one copy box: `18 Storyboard/Scene 10 - frame prompts.md`, numbered, each with the list of files to attach and its save-as name. Under about 150 frames this chat path is cheaper than an image service (C2 R1).
2. The user pastes each prompt into their picture app and saves each picture under its name. When they attach the pictures, answer each frame's three checks and write the PIC records in `18 Storyboard/Storyboard frames - scene 10.md`, with the checks-in-words table and the END line.
3. The page and letterbox bars are made at the next real check on a code surface; until then the user watches the saved pictures in order.
4. Report, then:

```
Save as: 18 Storyboard/Storyboard frames - scene 10.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 02 Whole-film summary,
10 Film rules, 12 Steps for add-ons - storyboards, prompts, finishing, and Scene 11 -
Treatment floor; type: Make storyboards. Next is scene 11.
```

**One-line task, again:** Make storyboard frames: first the three-style test if the style is still provisional, then one kept grey frame for each chosen shot, drawn at the shot's most telling moment, and a page per scene the user watches with the sound off.
