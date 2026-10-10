# Step 13. Add-on - previs

This is add-on B, "grey previews" (the AI's word is previs). The user asks for it ("Make grey previews"); it is not counted among the 12 steps. It runs only in Claude Code on the user's computer, where you run Blender. Read this file at the start of every unit of this add-on, never from memory.

**One-line task:** Make grey previews for the shots whose meaning depends on where the camera stands, its lens or how bodies move: compile each plan from the records, write only what code cannot, render, pass the blocking check, and show the user one contact sheet per scene of framing-critical shots.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Fix camera placement, lens, timing and where bodies stand before any video is made (C4 R1). Example: scene 10, shot 80, the reflection. Code builds the kitchen from its set plan with the west wall left open, puts camera A 6.3 metres back on the table's line, 1.45 metres high, on the 85 lens, and stands Iona, Saye and Eli on their marks; Jude is a lying box on the table. The 9-second shot at 24 frames a second renders 252 frames, its screen time plus handles. The render must print `BLOCKING OK` and show both profiles level at the edges of the frame, the raised hands nearest the camera, Eli small and deep in the middle.

## When it runs

On request, after the book and exports; this is where it is offered for The Catch (about 26 framing-critical shots). Only in Claude Code on the user's computer. On any other app say once: "Grey previews need Claude Code on your computer; everything else works here."

## Inputs

LOCATION set plans (objects, marks, `plan_orientation`); each SCENE's `start` items; MOVE and SETUP records; SHOT records (`previs_level`, `framing_critical`, `screen_time`, `moment` items, `move`, `lens_mm`, `motion`, `time_slice`); CHARACTER `height_m`; PROJECT `frame_shape` and `fps`; the PREVIS stubs code made at step 8 for masters (`PV-SC06-MASTER-V01`, `status: planned`).

## Outputs

- PREVIS records in `19 Grey previews/Grey preview jobs.md`: `for`, `level`, `standin_level`, `route`, `extras`, `stills`, `approved`; code works out `plan_file` and `blocking`.
- Plan files in `For machines - do not edit/previs plans/`; renders in `19 Grey previews/Scene 10 - shot 080/`; one `19 Grey previews/Scene 10 - contact sheet.html` per scene.
- Extras fragments `19 Grey previews/extras/<shot>.json`, where needed.
- PROJECT `previs_colours`, one flat colour per character's stand-in, set once by code.

## Card parts to open

At every depth: card 22, whole.

## Procedure

1. **Offer it.** The shots at `previs_plan_level_min` or above were chosen at step 8 by C4's ladder (C4 §9): 0 for most shots, 2 for a layout check, 3 for a guide video (falls, weightlessness, the creature, complex moves), 4 when a reach or flinch must be exact. Say: "I suggest grey previews for 26 shots (list). About N minutes of work. Go? [yes]", with N from the render times.
2. **Compile the plans.** Run `stage.py previs` (one shot: `--shot SC10-SH080`). Code builds each plan from the records: boxes from set-plan objects; figures from the scene's starts and every floor-plan move before the shot; the camera from the setup; frames from screen time plus `handles_s` at each end; the size from `previs_width_px` and the frame shape; stills at the first frame, each moment's start and the last frame. A place seen in both mirror states is stored once; code derives the other, and nobody edits either by hand (B3 §5.4).
3. **Write only what code cannot**, as a fragment named in `PREVIS.extras`: physical motion beyond the free-fall helper; bodies riding a moving cage, keyed to it (C4 R11); doors on hinges, such as the figure's chest; arm and hand poses; a performance filmed on a phone (C4 Recipe 7); creature shapes. A fall is keyed on every frame from `free_fall_half_g`, never eased (C4 R10).
4. **Masters.** One physical event shown in overlapping shots is one master: scene 6's fall is `PV-SC06-MASTER-V01`, and each shot's `time_slice` names its frames of it. Scene 13's playback is rendered from scene 6's master through its in-story camera.
5. **Render and check.** Run `stage.py previs --render`. It renders each plan, runs the blocking check (CLASH, OVERLAP and CAMERA lines) and PREVIS-01 to PREVIS-03. Nothing goes to a video model before `BLOCKING OK` (C4 R21), and every figure faces within `facing_tolerance_deg` of its derived facing. A fault is fixed in the records or the fragment and rendered again, never in a prompt (C4 R20).
6. **Approve.** A shot that is not framing-critical is `approved: auto` once it passes both checks. Framing-critical shots go on the scene's contact sheet for the user.
7. **The route into video**, one per shot in `PREVIS.route` (C4 §6): 1, grey stills restyled into start and end pictures; 2, a depth guide video; 3, a grey reference video; 5, layers composited. Never lay a guide video over a face whose lips must sync (C4 R13).
8. **The user's changes**, in plain words ("lower the camera to knee height"): change the setup or shot record, compile and render again. Two or three rounds are normal (C4 Recipe 3).

## Record template

`references/templates/18 Add-on jobs.md` (PREVIS).

## IDs you will be given

A PREVIS is named by its shot and a try number: `PV-SC10-SH080-V01`, shown to the user as "try 1"; a new try after a change is `-V02`, never a reused number. Masters keep the names code gave their stubs at step 8. Stand-in colours and plan file names come from code.

## Batch and chunk rules

One scene per unit (U-13-SC10), in scene order; code compiles and renders, taking seconds to a minute per shot. Masters are rendered before the shots that take slices of them. The Catch: about 20 to 40 shots; about 15 to 30 minutes of the user's review for each hard shot.

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Does every shot at `previs_plan_level_min` or above have a plan, `BLOCKING OK` and facings within `facing_tolerance_deg`?
2. Is every extra written as a fragment, never by editing a compiled plan or a derived mirror copy?
3. Is every fall keyed on every frame, and every rider moving with what carries it?
4. Does every framing-critical shot have the user's answer, and every other passing shot `approved: auto`?
5. Does every PREVIS record name its route?
6. Is any shot here that a start picture would serve as well?

## The report

```
Done: grey previews for scene 10: 2 shots.
Example: shot 80, the reflection, seen from far back along the table: both women
  in profile at the edges, the raised hands nearest the camera, Eli small in the
  middle.
Made: 19 Grey previews/Scene 10 - contact sheet (a plan from above and stills for
  each shot).
Needs you: here are the grey previews for scene 10. Reply with the numbers of any
  that look wrong, or "fine".                                                [fine]
Next: grey previews for scene 13.
```

## Checkpoint

The grey previews. One contact sheet per scene of framing-critical shots: a plan from above and the stills of each shot, with its one-line description. One question: "Reply with the numbers of any that look wrong, or 'fine'. [fine]". Changes come in plain words and are made as in procedure 8; nothing else waits for this answer.

## How to redo

A plain-word change ("lower the camera to knee height", "camera A a step further back") changes the setup, mark or shot record, then compiles and renders a new try. A change to a set plan or a shot marks its plans stale; they are made again before any video uses them.

## If you cannot run code

Every line reference is a quote anchor in chat, but this add-on has no chat form: grey previews need Claude Code on the user's computer, where Blender runs. On the Claude website, ChatGPT or any chat app, say once: "Grey previews need Claude Code on your computer; everything else works here." Then offer the next add-on that works here.

1. Nothing is lost: `previs_level`, `framing_critical` and the set plans were written at steps 4 and 8, and the PREVIS stubs wait. When the folder is opened in Claude Code, `stage.py adopt` makes it a project there, and this add-on runs from its first step.
2. Never write a plan file, a render or a PREVIS record by hand, and never mark a shot `approved: auto`: those need the blocking check.
3. Report, then:

```
Save as: nothing new in this reply.
To continue later: open your breakdown folder in Claude Code on your computer and
type: Make grey previews.
```

**One-line task, again:** Make grey previews for the shots whose meaning depends on where the camera stands, its lens or how bodies move: compile each plan from the records, write only what code cannot, render, pass the blocking check, and show the user one contact sheet per scene of framing-critical shots.
