# 12 Steps for add-ons - storyboards, prompts, finishing

Part of the Stage chat kit: a step-group file, attached to the chat that runs one of these steps (not knowledge). It joins the step files 12 Add-on - storyboards, 14 Add-on - generation packs, 15 Add-on - edit and finishing, each whole. Read the one for this unit every time, quote its one-line task back before any work, and follow its section "If you cannot run code" when this chat has no code. 01 House rules (in the knowledge) says where every other skill file is.

---

From the skill file `steps/12 Add-on - storyboards.md`:

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

`templates/18 Add-on jobs.md` (PIC), `templates/01 Choices.md` (CHOICE).

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

---

From the skill file `steps/14 Add-on - generation packs.md`:

# Step 14. Add-on - generation packs

This is add-on C, "prompts for AI video". The user asks for it ("Get it ready for AI video"); it is not counted among the 12 steps. Read this file at the start of every unit of this add-on, never from memory.

**One-line task:** Get the breakdown ready for AI video: settle the style, the voices and the spending cap, make reference pictures and voice takes first, let code compile, lint and price each scene's prompts, and log every take with a keep-or-reject suggestion.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Turn approved records into pictures and clips, deciding nothing again: scene 10, shot 150 is 15 seconds; with `handles_s` at each end its clip is 17 seconds, longer than Kling 3.0 Omni allows. A turn shot is a held take, never split, so it goes to Seedance 2.5 as one take. Its prompt is motion only ("the woman"), because a start picture is attached (C3 R1), and ends "Her head and hands stay still; only her eyes move. The camera does not move. No background music." Its pack asks: "Only her mouth moves, and only at 6 to 8 seconds?", and "Is Iona's face as readable and as true in colour as the other faces in this frame?" (B2 R24).

## When it runs

On request, after the book and exports; packs on any app, spending only with a connector or a model service account, and the cap. Quick-depth scenes are made standard first ("go deeper on scene 10").

## Inputs

Every shot-related record; STYLE; CHARACTER, VOICE and STATE; LOOK; SOUNDPLAN; RIGHTS and PROJECT `rights`; the dated adapter files and `adapters/prices.json`.

## Outputs

- `20 Prompts for AI video/`: `Pictures.md` (PIC: reference, start and end pictures), `Voices.md` (VOICETAKE), `Takes.md` (TAKE); one pack page per scene and model (`Scene 10 - Saye's kitchen - Kling 3.0 Omni.md`); `Reference pictures/`, `Voices/`, `Text graphics/`.
- `22 Rights and credits.md`: RIGHTS for voices, likeness, music, fonts, stock and tool terms, and the disclosure text.
- PROJECT `spend_cap_usd`, `intended_use`, `licensed_data_only`; CHARACTER `skin_light`; VOICE `source`; CHOICE records.

## Card parts to open

At every depth: card 21, whole; card 06, part "Lip sync and voice takes"; card 24, whole.

## Procedure

1. **The style test first**, if add-on A has not run it (U-14-STYLETEST): as in add-on A, three directions on three shots, one question, "Which of these three styles? [A]" (D5 §7.1).
2. **Three questions, once** ("Checkpoint"): the voices (confirming `VOICE.source` and `SOUNDPLAN.voice_policy`); where the film will go (`intended_use`, "just for you" is `personal`); the spending cap (`spend_cap_usd`), with no default: nothing is spent until it is set, and code refuses any batch above it. `licensed_data_only` stays a small choice, default no.
3. **Rights before pictures.** With `rights: study_only`, packs refuse public release (GEN-14). A film to be sold or shown at festivals needs every kept take, voice and sound made on a plan allowing commercial use, as a RIGHTS record (D4 R13). Every face and voice is invented unless a consenting adult signed for that use; never a celebrity's, a child's or a dead person's voice (D4 P3; D3 R16).
4. **Fresh model facts.** Above `model_facts_max_age_days` no pack is paid and no money is printed (GEN-11). With web access, re-read the makers' pages and run `stage.py refresh-models --propose`; the user approves any price change; then `--apply`.
5. **Reference pictures** (U-14-REFERENCES, one group of scenes per unit): every element state in frame (C2 Rule 1). Places are empty; later states are edited from the base (C2 Rule 17). The user chooses the casting types the story leaves open from two or three options; then write each principal's `skin_light`.
6. **Voices first** (U-14-VOICES): every recurring speaker gets one locked voice before any clip with a visible speaking mouth (D3 R1). `stage.py export voices` writes the voice line script; each line gets three takes (VOICETAKE), code checks the words, the user picks by ear. A relayed voice (earpiece, radio, recording) gets its path in the edit, one saved treatment per path (D3 R24); a voice stays `draft` while accents are undecided (D3 R6).
7. **Compile each scene** (U-14-SC10): `stage.py compile --scene SC10`; prompts are compiled, never typed. Code picks the scene model (serving most shots with recurring characters), logs each override with its reason (C1 §9), works out clip lengths and sends a held take longer than the scene model allows to a model that allows it (C1 R11); where none does, GEN-10 is an error and the shot is redesigned with a motivated cut. It writes, lints and prices the prompts; `stage.py graphics` draws readable text as text graphics. The end picture is edited from the start picture (C2 Rule 15). Fix every GEN error in its record, then compile again.
8. **Read each pack page** as the user will: "How to use this page" (with the one-time account setup, C1 Recipe 1); per shot its line, the prompt in a copy box, "Attach, in this order:", settings, takes and cost, "Check in the result:" questions, the save-as name and the age of its model facts.
9. **Spend carefully.** Draft on the cheapest tier first (C1 R13); a take above `cheap_test_above_usd_per_take` needs a cheaper test first (GEN-16); stop a route after `takes_stop_per_route` failed takes and a shot after `takes_stop_per_shot`, and change method, not wording (D13 R12). Run `stage.py estimate` after each batch (D13 Recipe 5); once `spend_check_share` of the video money is gone before that share of shots is kept, move the other non-dialogue shots to the budget tier (D13 R11); over budget, apply D13 R10's cuts one at a time. Never cut or cheapen a turn or must-keep shot, or a scene the story cannot lose, without asking.
10. **Log every take** (U-14-TAKES-SC10): a TAKE with the clip, exact model name and date, route, inputs, seed, settings, cost, file, each check's answer and any refusals. Suggest keep or reject from the checks; the user watches every kept take (C1 R18). Trace a wrong clip to its earliest wrong record first (C5 R28). After two refusals, move the element to compositing or sound and log it; never reword a third time (D4 R11).
11. **Disclosure.** Never remove a watermark or Content Credentials; write the disclosure line in `22 Rights and credits.md` (D4 Recipe 6).

## Record template

`templates/18 Add-on jobs.md` (PIC, TAKE, VOICETAKE), `templates/22 Rights and credits.md` (RIGHTS), `templates/01 Choices.md` (CHOICE).

## IDs you will be given

PIC by element state or shot, use and number: `PIC-CH-IONA.S02-REFERENCE-01`, `PIC-SC10-SH150-START-01`. Clips are numbered by code (`SC10-SH150.1`). Takes: `TK-SC10-SH150.1-T01`; voice takes: `VT-SC10-D11-T01`. RIGHTS and CHOICE take the next free numbers. A new try takes the next number; none is reused.

## Batch and chunk rules

References: one group of scenes per unit. Voices: one unit, first. Packs and takes: one scene per unit.

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Does every shot in scope compile with 0 GEN errors on its routed model, priced on model facts under `model_facts_max_age_days` old?
2. Is every voice locked before its mouth is seen? Is every held take one clip?
3. Is readable text a text graphic, with no reason, name or emotion word in any prompt?
4. Is every face and voice invented or backed by a consent record?
5. Was nothing spent before the cap, and does every kept take name its exact model, date, seed and cost?
6. Did the user watch every kept take?

## The report

```
Done: prompts for AI video, scene 10: 20 shots and a title card, ready to send.
Example: shot 150 is one 17-second take on Seedance 2.5, because the turn must
  not be cut and Kling 3.0 Omni's longest take is 15 seconds.
Made: 20 Prompts for AI video (scene 10's pages for Kling 3.0 Omni and
  Seedance 2.5, the pictures to attach, settings and cost); Voices (Iona's
  "Not mint." picked from three takes).
Needs you: nothing; these takes fit the most you set for one batch.
Next: the takes for scene 10.
```

## Checkpoint

Keeping takes. First the three questions of item 2, once, in one message:

```
Before anything is made, three questions. Reply by number.
1. Every voice is designed, never copied from a real person. Keep it so?        [yes]
2. Where will the film go: just for you, festivals, free online, online with
   money made from it, or for sale?                                    [just for you]
3. The most one batch of takes may cost, in dollars. Nothing is spent until you
   say, so this one has no answer ready.
```

Then each take with the suggestion from its checks: "Take 3 of shot 150: keep it? [keep]". The user watches every kept take; `kept` is theirs alone.

## How to redo

"Make a new take of shot 150": the next take number, the same prompt unless a record changed. A wrong clip is traced to its earliest wrong record, which is fixed; the pack is compiled again, and every clip that record touches goes stale.

## If you cannot run code

Every line reference is a quote anchor: each check question quotes its line, never a line number.

1. Packs, linting and prices need code. Write a few prompts by hand for the shots the user wants first, from card 21 (fixed descriptions, state lines and the look block word for word; motion only when a start picture is attached; no reasons, names, emotion words or music), then run the prompt linter of C3 §21 in words.
2. Mark each page "written by hand, not linted by code, not priced", and print no money.
3. The user may paste these prompts into a video app by hand; you spend nothing and run no batches. For linted, priced packs: the real check on the Claude website, then "Get it ready for AI video." there.
4. Save `20 Prompts for AI video/Scene 10 - Saye's kitchen - by hand.md` in one copy box with its END line; take records go in `20 Prompts for AI video/Takes - scene 10.md`.

```
Save as: 20 Prompts for AI video/Scene 10 - Saye's kitchen - by hand.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 02 Whole-film summary,
10 Film rules, 12 Steps for add-ons - storyboards, prompts, finishing, and Scene 10 -
Saye's kitchen; type: Get it ready for AI video. Next is scene 10's takes.
```

**One-line task, again:** Get the breakdown ready for AI video: settle the style, the voices and the spending cap, make reference pictures and voice takes first, let code compile, lint and price each scene's prompts, and log every take with a keep-or-reject suggestion.

---

From the skill file `steps/15 Add-on - edit and finishing.md`:

# Step 15. Add-on - edit and finishing

This is add-on D, "planning the edit". The user asks for it ("Plan the edit"); it is not counted among the 12 steps. Read this file at the start of every unit of this add-on, never from memory.

**One-line task:** Plan the edit: fill in each finishing job code made from the shots, spot music cues only where the music policy allows them, and write the assembly guide and the disclosure text.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Turn kept takes, voice takes and records into one film that can be watched, captioned and delivered. Example: after scene 10's "Nobody leave this room." the script writes "> CUT TO BLACK." and "= THE CATCH". Code makes the title card's finishing job, `FX-SC10-SH990-01`, `operation: title`; you fill it in: white on black inside the graphics-safe area, cut in and out with no fade, held longer than its `text_floor`, in true silence, in one free font (D8 R42-R45). The ring inserts, shots 90 and 100, get no flip job: they were made from edited stills at their final side and are never flipped.

## When it runs

On request, after the book and exports, on any app. It can run before any take exists (the jobs then list the takes to come) and runs again as takes are kept. Nothing else depends on it.

## Inputs

SHOT records and what code derives from them (mirror routes, post operations, text in frame, frame shape); SOUNDPLAN (`music_policy`, `loudness_target`, `device_budget`); TAKE and VOICETAKE records; RIGHTS; PROJECT `frame_shape`, `fps` and `rights`; the timeline files of step 11.

## Outputs

- `21 Edit and finishing/Finishing jobs.md`: FINISH records (code sets `shot` and `operation`; you write `tool`, `inputs`, `output`, `done`), and MUSIC records when the policy allows cues.
- `21 Edit and finishing/Assembly guide.md`: how to bring the film together in DaVinci Resolve's free version.
- `22 Rights and credits.md`: a RIGHTS record for every music, sound, font and stock file, and the disclosure line.

## Card parts to open

At every depth: card 23, whole.

## Procedure

1. **Let code make the jobs.** Run `stage.py export finishing`. It creates one FINISH record for each operation a shot needs: `flip` (the "flip all" and "flip with mirrored references" routes), `composite` (text graphics, screens, plates with people, blood beads), `crop` (to the frame shape), `speed` (slower sources to the film's rate; slow generation back to real time), `upscale`, `deflicker`, `grain`, `grade`, `title`, `lip_sync`, `voice_path`. Never add, delete or renumber a derived job; a missing one means a record to fix.
2. **The order of work:** time before size, size before colour, colour before grain (D8 §2). The whole film runs at `PROJECT.fps`; measure every take (D8 R9).
3. **One flip, never two.** A layer shows mirrored after an odd number of flips. A shot flipped inside its composite is not flipped again (D6 VC8); world lettering goes on normal before the whole-frame flip or mirrored after it, never both (D6 R15).
4. **Fill each job.** Simple jobs (flip, crop, a still graphic laid over, a speed change, joining) are ffmpeg commands you write and run on code surfaces. Tracked or keyed work goes to DaVinci Resolve (free), with click-by-click steps in the assembly guide. Set `done: yes` only when the output file exists.
5. **Size and colour.** Upscale only kept takes, after picture lock (when shot lengths stop changing): whole takes to 1080p, and to 4K only the used seconds plus handles when delivery needs it (D8 R20; D13 R14). Grade: first a normalize step per model, then each sequence to its style picture (D8 R28); darker skin stays rich, never grey (B2 R24). One grain for the whole film, once, after the grade (D8 R34).
6. **Sound.** Three stems, dialogue, music and effects, so a dub swaps only dialogue (D8 R37); loudness set to `SOUNDPLAN.loudness_target` over the whole film (D8 R38); each relayed voice through its path's one saved chain (D3 R24); lip sync checked again after any sound is moved against the picture (C5 R31).
7. **Music** (U-15-MUSIC), only when `music_policy` is sparse or scored. Run `stage.py export spotting` for the spotting sheet. Each cue is a MUSIC record: `in`, `out`, `function`, `must_not`, `source`, `licence` (its RIGHTS record). A cue enters on a motion or a cut and leaves before a rupture (D9 §4.2). Under `none`, as in The Catch, there are no cues, and a drone needs a source in the story, such as the ship's hum (D9 R4).
8. **Rights and disclosure.** A RIGHTS record for every music, sound, font and stock file, made when it enters (D4 P6); a licence that forbids earning money keeps it out of a film that will (D9 R19). Never crop, blur or remove a watermark or Content Credentials (D8 R26; D4 P8). Write one disclosure wording for credits, platform labels and festival forms (D4 R20, Recipe 6). With `rights: study_only` the guide and credits say "Private study, not for publication".
9. **The assembly guide:** import `timeline.otio` into DaVinci Resolve (another editing program takes the EDL) at the frame shape and frame rate; where each kept take goes; the finishing jobs in order; the caption files and description track beside the picture, not burned in (D8 R55).
10. **Check:** every derived operation has a FINISH record with its tool, inputs and output; the timeline and the assembly guide exist; `22 Rights and credits.md` holds the disclosure line.

## Record template

`templates/18 Add-on jobs.md` (FINISH, MUSIC), `templates/22 Rights and credits.md` (RIGHTS).

## IDs you will be given

Code names every finishing job by its shot and a number: `FX-SC10-SH990-01`, `FX-SC10-SH080-01`; copy them, never add one. Music cues take `MU-01` onward, and RIGHTS records the next free numbers, from the handout.

## Batch and chunk rules

One unit per group of scenes (U-15-FINISH), filling that group's jobs in shot order. Music is one unit for the whole film, only when the policy allows cues. The assembly guide is written once, at the end, and brought up to date when takes are kept.

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Does every derived operation have a FINISH record with its tool, inputs and output?
2. Is no shot flipped twice, and no sided insert flipped at all?
3. Is every take at the film's frame rate, cropped to the frame shape, and upscaled only after picture lock?
4. Is there one grain and one font for the whole film?
5. Does every sound, music, font and stock file have a RIGHTS record, and is every watermark kept?
6. Are there music cues only where the policy allows them?

## The report

```
Done: the edit plan for all 30 scenes, and the assembly guide.
Example: the title after scene 10, THE CATCH, is cut in and out of black with no
  fade and held longer than it takes to read, in silence.
Made: 21 Edit and finishing (every finishing job in order, and a guide for the
  free DaVinci Resolve); 22 Rights and credits (the line that says how AI tools
  were used, for the credits and for festivals).
Needs you: nothing.
Next: when your takes are kept, open the assembly guide and follow it from the top.
```

## Checkpoint

None. The report names the guide and what to do first; nothing waits.

## How to redo

"Plan the edit again": run `stage.py export finishing` again. Code adds jobs for new or changed shots and marks the jobs of changed shots stale; the jobs you filled for unchanged shots keep their tools and files. A kept take that changes means its jobs run again, in order.

## If you cannot run code

Every line reference is a quote anchor: each job or cue that points at the story quotes its line ("Nobody leave this room."), never a line number.

1. There are no derived operations without code. Write FINISH records only for what the records name plainly: a `title` for each card shot, a `composite` for each text in picture, a `crop` for the frame shape, a `grade` for each sequence, `lip_sync` where a speaking mouth is seen, `voice_path` for each relayed voice. Flips and other mirror jobs need code's mirror routes: they are added at the real check on a code surface, where `adopt` is followed by `export finishing`.
2. Write the assembly guide as steps in DaVinci Resolve's own menus, with no commands to type.
3. Save `21 Edit and finishing/Finishing jobs - scenes 07-10.md` for each group of scenes, with the checks-in-words table and its END line, and `21 Edit and finishing/Assembly guide.md` once.

```
Save as: 21 Edit and finishing/Finishing jobs - scenes 07-10.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 02 Whole-film summary,
10 Film rules, 12 Steps for add-ons - storyboards, prompts, finishing and the files
of scenes 11 to 13; type: Plan the edit. Next is scenes 11 to 13.
```

**One-line task, again:** Plan the edit: fill in each finishing job code made from the shots, spot music cues only where the music policy allows them, and write the assembly guide and the disclosure text.
