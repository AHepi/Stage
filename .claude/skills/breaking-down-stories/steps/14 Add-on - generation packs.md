# Step 14. Add-on - generation packs

This is add-on C, "prompts for AI video". The user asks for it ("Get it ready for AI video"); it is not counted among the 12 steps. Read this file at the start of every unit of this add-on, never from memory.

**One-line task:** Get the breakdown ready for AI video: settle the style, the voices and the spending cap, make reference pictures and voice takes first, let code compile, lint and price each scene's prompts, and log every take with a keep-or-reject suggestion.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Turn approved records into pictures and clips, deciding nothing again: scene 10, shot 150 is 15 seconds; with `handles_s` at each end its clip is 17 seconds, longer than Kling 3.0 Omni allows. A turn shot is a held take, never split, so it goes to Seedance 2.5 as one take. Its prompt is motion only ("the woman"), because a start picture is attached (C3 R1); its held time is small timed actions (she chews, stops, swallows), never a list of parts that stay still, and it ends "No background music." Its pack asks: "Only her mouth moves, and only at 6 to 8 seconds?", "Does Iona move between the written actions: breathing, eyes, small shifts?", and "Is Iona's face as readable and as true in colour as the other faces in this frame?" (B2 R24).

## When it runs

On request, after the book and exports; packs on any app, spending only with a connector or a model service account, and the cap. Quick-depth scenes are made standard first ("go deeper on scene 10").

## Inputs

Every shot-related record; STYLE; CHARACTER, VOICE and STATE; LOOK; SOUNDPLAN; RIGHTS and PROJECT `rights`; the dated adapter files and `adapters/prices.json`.

## Outputs

- `20 Prompts for AI video/`: `Pictures.md` (PIC: reference, start and end pictures), `Voices.md` (VOICETAKE), `Takes.md` (TAKE); one pack page per scene and model (`Scene 10 - Saye's kitchen - Kling 3.0 Omni.md`); `Reference pictures/`, `Voices/`, `Text graphics/`.
- On the H3 route in ComfyUI, the clip book instead: `20 Prompts for AI video/MiniMax H3 in ComfyUI/` (`00 Settings and how to run a clip.md`, `01 Pictures to make first.md`, one page per scene with one part per clip, `Shot map.md`, `If a clip goes wrong.md`, `Take log.md`), and `Master pictures/`, `Start pictures/`.
- `22 Rights and credits.md`: RIGHTS for voices, likeness, music, fonts, stock and tool terms, and the disclosure text.
- PROJECT `spend_cap_usd`, `intended_use`, `licensed_data_only`, `video_route`; CHARACTER `skin_light`; VOICE `source`; CHOICE records; on the H3 route, each TAKE's `rule` lines.

## Card parts to open

At every depth: card 21, whole; card 06, part "Lip sync and voice takes"; card 24, whole.

## Procedure

1. **The style test first**, if add-on A has not run it (U-14-STYLETEST): as in add-on A, three directions on three shots, one question, "Which of these three styles? [A]" (D5 §7.1).
2. **Four questions, once** ("Checkpoint"): the voices (confirming `VOICE.source` and `SOUNDPLAN.voice_policy`); where the film will go (`intended_use`, "just for you" is `personal`); the spending cap (`spend_cap_usd`), with no default: nothing is spent until it is set, and code refuses any batch above it; and which way the video is made (`video_route`, a CHOICE whose `sets` lines write `PROJECT.video_route | value: per_scene | when: a` and `PROJECT.video_route | value: h3_comfyui_r2v | when: b`). `licensed_data_only` stays a small choice, default no.
3. **Rights before pictures.** With `rights: study_only`, packs refuse public release (GEN-14). A film to be sold or shown at festivals needs every kept take, voice and sound made on a plan allowing commercial use, as a RIGHTS record (D4 R13). Every face and voice is invented unless a consenting adult signed for that use; never a celebrity's, a child's or a dead person's voice (D4 P3; D3 R16).
4. **Fresh model facts.** Above `model_facts_max_age_days` no pack is paid and no money is printed (GEN-11). With web access, re-read the makers' pages and run `stage.py refresh-models --propose`; the user approves any price change; then `--apply`.
5. **Reference pictures** (U-14-REFERENCES, one group of scenes per unit): every element state in frame (C2 Rule 1). Places are empty; later states are edited from the base (C2 Rule 17). The user chooses the casting types the story leaves open from two or three options; then write each principal's `skin_light`.
6. **Voices first** (U-14-VOICES): every recurring speaker gets one locked voice before any clip with a visible speaking mouth (D3 R1). `stage.py export voices` writes the voice line script; each line gets three takes (VOICETAKE), code checks the words, the user picks by ear. A relayed voice (earpiece, radio, recording) gets its path in the edit, one saved treatment per path (D3 R24); a voice stays `draft` while accents are undecided (D3 R6).
7. **Compile each scene** (U-14-SC10): `stage.py compile --scene SC10`; prompts are compiled, never typed. Code picks the scene model (serving most shots with recurring characters), logs each override with its reason (C1 §9), works out clip lengths and sends a held take longer than the scene model allows to a model that allows it (C1 R11); where none does, GEN-10 is an error and the shot is redesigned with a motivated cut. It writes, lints and prices the prompts; `stage.py graphics` draws readable text as text graphics. The end picture is edited from the start picture (C2 Rule 15). Fix every GEN error in its record, then compile again.
   **On the H3 route in ComfyUI** (`video_route: h3_comfyui_r2v`, or `stage.py compile --scene SC10 --route h3-comfyui`), compile makes the clip book instead: code groups the shots into clips of one to three shots, sets each clip's length on H3's grid with a tail to throw away, writes each prompt in MiniMax's reference format and runs the ROUTE checks. Fix every ROUTE error in its record; a ROUTE warning is a suggestion until the take log confirms its rule. Then: read the clip book; make the master pictures, then each clip's start picture against the checklist; run a few clips at the small test size first; and log every take with its rule verdicts (a TAKE `rule` line: the rule, confirmed, wrong or unclear, and what was seen). Draft on the same route at the small size, never on another model.
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
2. Is every voice locked before its mouth is seen? Is every held take one clip? On the H3 route, does every clip page name its master picture and character pictures, and does every take log its rule verdicts?
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

Keeping takes. First the four questions of item 2, once, in one message:

```
Before anything is made, four questions. Reply by number.
1. Every voice is designed, never copied from a real person. Keep it so?        [yes]
2. Where will the film go: just for you, festivals, free online, online with
   money made from it, or for sale?                                    [just for you]
3. The most one batch of takes may cost, in dollars. Nothing is spent until you
   say, so this one has no answer ready.
4. Which way will you make the video?   [Stage picks a model for each scene]
   a. Stage picks a model for each scene
   b. MiniMax H3 in ComfyUI, Reference to Video
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
