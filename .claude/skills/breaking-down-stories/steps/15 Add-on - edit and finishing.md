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
