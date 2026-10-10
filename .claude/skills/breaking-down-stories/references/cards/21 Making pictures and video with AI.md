# Card 21. Making pictures and video with AI

Add-ons A and C read it whole; step 10 reads only "Cost". "C1 R9" is rule 9 in C1 §6; "C2 Rule 12" is rule 12 in C2 §5 and "C2 R6" its recipe 6; "C3 R1" is rule 1 in C3 §18 and "C3 L14" its linter check 14. Model facts live only in `adapters/*.json`, dated (C1 §0).

## The job

Turn approved records into pictures and clips, deciding nothing again. `stage.py compile` fills C3's master template into each clip's **generation specification** (`generation_spec`, one model-neutral description) and rewrites it per model with a dated **adapter** (one model's rules for word order and syntax) (C3 §15-§16). The AI supplies inputs, reads every **pack** (one scene's prompts for one model), fixes a record rather than a prompt, and logs every take. It hands on PIC, VOICETAKE and TAKE records, packs with 0 GEN errors, cost lines, and a keep-or-reject suggestion per take at checkpoint E ("keeping takes").

## Questions in order

1. **Is the style provisional?** Run D5's style test first: three directions each tried on a face, a wide and a hard shot (D5 §7.1-7.2, R12). Ask once: "Which of these three styles? [A]" (blueprint 10).
2. **Does every element state in frame have reference pictures?** **Reference pictures** are approved stills of one element in one state that a model copies: portrait, front-side-back views, hands and marks, one view per picture; places empty; later states edited from the base (C2 Rule 1, Rule 17, §6.2).
3. **Will it become video?** If not, stop at a grey storyboard frame of the most telling moment; arrows and bars are drawn by the page, never in the picture (C2 Rule 2, §2.2, R3).
4. **Is a speaking mouth on screen?** Voices first: the VOICE locked and its VOICETAKE picked before the clip (K16; D3 R1). Prefer the listener; then a model that takes the line's audio, then lip sync after, then a cutaway (D3 R20-R21).
5. **Which model?** Code picks one **scene model** per scene (the model serving most of its shots with recurring characters) and logs each override with its reason, followed by drift questions (K29; C1 R14). A **held take** (a turn shot, where the scene turns; a shot in a one-take `oner` scene; or `held: yes`) is never chained: it routes to a model that allows its length, or is redesigned with a motivated cut (GEN-10; blueprint 8.4).
6. **Is it a hard case?** Readable words are a **text graphic**, drawn outside any model and composited after any flip (K17; C2 Rule 9); floating bodies take a **guide video**, a grey 3D video the model copies (C1 R8; card 22); violence is split into cause, reaction and aftermath (C1 R9).
7. **Does the pack pass?** 0 GEN errors (rubric criterion 9), and for each face in frame: "Is <name>'s face as readable and as true in colour as the other faces in this frame?" (B2 R24; blueprint 8.9). Without code, run C3 §21 in words.

## Cost

Example first: the fall in The Catch's SC06 is 36 shots in 49.7 seconds, yet every take pays for a whole clip, so it bills about 1,250 generated seconds, about 25 per second on screen (D13 §15.1). A **generated second** is one second of clip a model makes, kept or not; **clip length** is what one take bills; a **tier** is the price level of final takes: budget, mid or premium (C1 §10).

1. **Code prices; the AI never writes a total** (D13 P1, R4): `stage.py estimate` works from words first, from the shots at step 10.
2. **Clip length** is the model's shortest clip or screen time plus `handles_s` at each end, whichever is longer, rounded up to an allowed length (D13 §6.2; blueprint 8.4). Short shots pay whole clips, so fast scenes cost most (D13 P4).
3. **Each shot has a `cost_class`**: `graphic` and `reuse` cost no takes; `still_move` is one picture, held or pushed slowly in the editor; the push is a `push_in` inside the scene's budget and camera rules (B1 P5); `easy`, `dialogue` and `hard` take D13 §6.1's draft and final takes. Several needs take the dearest class, and text or a screen adds a **plate**, an extra element for compositing (D13 R20); zero gravity, an exact camera path, a performance or a creature is `hard` (D13 R8).
4. **Video money** is clip length × (draft takes × draft price + final takes × tier price), plus plates (D13 E7). Show all three tiers (D13 R9).
5. **Other lines**: pictures, voices and effects, music (none under `music_policy: none`, D13 R24), upscaling of kept takes after picture lock (D13 R14), contingency (D13 §6.9). A tool whose terms exclude film is not budgeted (D13 R19).
6. **Freshness**: prices older than `model_facts_max_age_days` print no money (GEN-11; D13 R7).
7. **While spending**: nothing before `spend_cap_usd` is set; a take above `cheap_test_above_usd_per_take` needs a cheaper test first (GEN-16); stop a route after `takes_stop_per_route` failed takes and a shot after `takes_stop_per_shot`, and change method, not wording (C3 §17A; D13 R12); once `spend_check_share` of the video money is spent before that share of shots is kept, move remaining non-dialogue shots to the budget tier (D13 R11); over budget, apply D13 R10's cuts in order (`stage.py lib D13 R10`). A turn shot, a must-keep shot or a cardinal event (a scene the story cannot lose) is never cut or cheapened without asking (blueprint 8.8).

## Translation menus with pitfalls

Pick one `SHOT.route` per shot, from its derived `needs` (C1 §5; C3 §20):

| Need | Route | Pitfall |
|---|---|---|
| Exact first and last picture | `start_end_pictures`, the end picture edited from the start picture (C2 Rule 15) | Two different pictures make the model cut (C3 F27) |
| Exact camera path | `guide_video` from previs (C1 R4; card 22) | The camera described again in words (C3 §9D) |
| A glance that must land | `performance_transfer`: act it on a phone (C1 R12) | An emotion word in the prompt (C3 L07) |
| Hands, rings, a held last image | `still_with_move` (C1 Ex8) | Forcing motion into hands (C3 §13C) |
| A recurring face | `references` in C2 §6.6's order; props dropped first, faces never | Extra references leak their light (C2 §1; C3 F37) |

## Budgets and saved choices

- `clip_speech_rule` with `speech_wps_default` (K08; GEN-03); `on_screen_speakers_per_clip_max` (C1 R2; GEN-13); `acting_characters_per_clip_max` (C3 R16); `main_actions_per_seconds` (C3 R2).
- `named_sounds_per_prompt_max` (C3 L13; GEN-17); no music in any clip (K31; C3 R10).
- The **fixed description** (a character's or thing's unchanging words), **state line** (its state now) and **look block** (the place's light and colour words) are pasted word for word, within `fixed_description_words`, `look_block_words_max` and `style_words_count` (C3 R6; GEN-04).
- `plate_route_face_height`, `lip_sync_tight_face_height`: larger faces change the routes (blueprint 8.5).
- **Drift** (an element changing across pictures) above one frame in ten: train a **LoRA**, a small file teaching an open model one face, or use a still with a push-in (C2 Rule 14; D5 R17).

## The H3 route in ComfyUI

Example first: scene 10's turn, shot 150, is 15 seconds; on this route it is clip 07, 362 frames (type 15.0 in Float (Duration)), and only its first 13.8 seconds fit before the tail, so the rest of the hold is made in the edit (ROUTE-13). A **route** is a model plus the place it runs. "MiniMax H3 in ComfyUI, Reference to Video" (`minimax-h3-comfyui-r2v`) is never chosen by routing: `stage.py compile --route h3-comfyui`, or the project's `video_route` set to `h3_comfyui_r2v` at add-on C's checkpoint, makes its **clip book** in `20 Prompts for AI video/MiniMax H3 in ComfyUI/` (C3 §25; Project notes 42, 43).

Why it differs from every other route:
1. **No rewriting step.** MiniMax's hosted service rewrites a short prompt into a long structured one; ComfyUI runs H3 on the words as written, so code writes the long form: six sections in MiniMax's order, with a label for every picture connected (C3 §25).
2. **No negative side.** A word naming something absent adds it, so no "no", "not", "nothing" or "still" outside the spoken lines; a clause that needs one is left out and listed on the clip page. The one camera line is "static, on a tripod, with no camera movement whatsoever".
3. **Descriptions repeated, word for word.** In reference mode a picture is tied to a person only through its label, so each person's fixed description and state line stand next to their `<Picture N>`. This is the exception to C3 R1's motion only, and GEN-05 never applies here.
4. **Clips of one to three shots.** Short shots cut together inside one clip each hold one beat. A held take, a moving camera and part of a long shot are clips of their own; two singles of people facing each other share a clip only after a shot showing both; a **contact cut** (end the shot as one thing reaches another, open the next on the result, the sound on the cut) keeps its pair together.
5. **The tail.** Lengths sit on H3's grid of 17 × k + 5 frames; every clip ends with a **tail** of at least 1.3 seconds, thrown away, because H3 breaks up near the end. The page gives the seconds to type and the seconds to keep.
6. **Start pictures from master pictures.** One **master picture** per place, empty, made once; each clip's **start picture** is built from it and shows the clip's first moment: hands already on what they move, eyes on the task, mouths closed. H3 takes the camera, the people and the light from it more than from the words.
7. **People are alive.** Each person "is alive in every second of this clip": breathing, eyes, weight, blinks at stated times; held time is small timed actions, never parts that stay still.
8. **Rules are marked.** Format facts from MiniMax's and ComfyUI's documents are errors; every judgement rule (ROUTE checks marked unclear) stays a suggestion until two takes in the take log confirm it, and is dropped when the takes show it wrong.

## The baseline is a strong answer

One scene model, one shot per clip, an approved start picture with a motion-only prompt, room sound, no music, and a still with a push-in where motion adds nothing are choices, not failures (C3 §10; K29; C3 R1, R10). Depart only for a need code can name.

## Cliché traps

Tests: any-film, mood-word, stacking and sound-off (card 05), and the **reference test**: does the take pass its yes/no questions against its reference pictures?

- **The house style**: unasked light shafts, "cinematic", "moody" (B2 §12; GEN-12). Fix: look block and style words only.
- **Creature clichés**: "robot", "alien", "glowing eyes" (C2 §9). Fix: plain shapes.
- **Emotion labels** (C3 L07). Fix: two or three visible behaviours.
- **Re-describing a start picture** (C3 R1; GEN-05). Fix: motion only, "the woman". On the H3 route in ComfyUI the opposite holds: each description is repeated word for word next to its picture label.
- **Backwards text asked of a model** (C1 R7; GEN-06), or **"falling" for floating bodies** (C3 R13, §12). Fix: a flipped text graphic; "hair and straps drift up; nothing settles".
- **"No people"** (K18; GEN-07). Fix: nouns in a **negative field** (a box of things to leave out) where the model has one, else positive words.

## Reasons that fail and reasons that pass

- Fails: "Seedance for a more cinematic take." Passes: "SC10-SH150 is a held take longer than the scene model allows, so it goes to `seedance-2.5` whole (blueprint 8.4; GEN-10)."
- Fails: "Reject take 2; it feels off." Passes: "Reject TK-SC10-SH150.1-T02: her mouth moves before 6 s, failing 'only her mouth moves, and only at 6-8 s?' (blueprint 8.9)."
- Fails: "Try better wording" after repeated failures. Passes: "`takes_stop_per_route` reached; change to a start and end picture (D13 R12)."

## Two worked examples

### The Catch: SC10-SH150, "Not mint." (line 463)

A static close-up of 15 seconds; with `handles_s` at each end its clip rounds up to 17, beyond `kling-3.0-omni`, so this held take routes to `seedance-2.5` as one take (blueprint 8.4). VT-SC10-D11-T01 carries "Not mint."; Saye's lines stay off screen, placed in the edit (D3 R20). A close-up's `face_height_by_size` is above `lip_sync_tight_face_height`, so the audio goes in as a reference (D3 R21). The prompt is motion only (C3 R1), and its held time is small timed actions: she chews, stops, frowns, chews once more, says the two words, swallows, and her eyes stay on Saye. It never lists parts that stay still: models read such a list as an order to freeze (Project notes 42).

### The Long Places: SC05, "She did not turn her head." (line 79)

A contemplative, locked-off medium holds the dark at Nilay's right shoulder for 12 seconds; its 14-second clip is beyond `veo-3.1`, so the scene model must allow it (D13 §15.4). The warmth, "the way a cat commits itself", is never shown: the prompt says "the dark space at her right shoulder stays empty", and "cat" goes only into a negative field (K18; C3 R5). Her held time is written as small timed actions (a breath, a blink, the lamp flame wavering), never a list of parts that stay still (Project notes 42). The shoulder settling "with weight" is acted on a phone and transferred (C1 R12). When the refrain returns at first light, a shot whose light differs is a new take from its saved setup; the rest are reused (D13 R6).

## Self-check

- Is the style locked, with reference pictures for every element state in frame?
- Is every voice locked before its mouth is seen?
- Does every held take stay one clip, and does every override carry a reason?
- Is readable text a text graphic, with no reason, name or emotion word in any prompt (GEN-15, WORDS-03)?
- Is the cap set, are model facts fresh, and has a person watched every kept take (C1 R18)?

## Words for AI models

Works: one camera move and where it ends (C3 §4); moments in the model's own time marks, then an end state (C3 §5); the model's speaker format (Veo: colon, no quotation marks; Kling: `Name (delivery): "line"`; K15); the path of a relayed voice (C3 R21); "flashlight", never "torch" (K19).

Fails: reasons in prompt text (GEN-15); lens numbers or focus shifts trusted to words (C3 §4; B1 R14); two camera moves (C3 L03); negating a visible thing (C3 L14).

## Look up for more

C1 §5-§11; C2 §2.2, §5-§9; C3 §4-§9, §15-§21; D13 §6, §9, §15; D5 §7; D3 §3.
