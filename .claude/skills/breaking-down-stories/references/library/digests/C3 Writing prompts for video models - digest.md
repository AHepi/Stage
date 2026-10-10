# Digest C3: Writing prompts for AI video models

Source: `research/C3_prompting_video_models.md` (1,173 lines, ~22,500 words; facts checked 2026-09-27, re-check after 2026-10-27). Brackets: [R#] decision rule (§18); [L##] linter check (§21); [F#] failure row (§20); [Rec#] recipe (§19); § section. The file labels facts [V] verified, [U] unverified, [J] judgment; nearly all numeric defaults (words per second, beats, takes) are [J].

## 1. Scope

1. Turns one breakdown shot into a prompt a video model will follow: one model-neutral MASTER SHOT PROMPT TEMPLATE stored per shot, plus adapters for Veo 3.1, Omni Flash 1.1, Kling 3.0, Seedance 2.5, Wan 3.0, MiniMax H3, Runway Gen-4.5, Luma Ray3.2, LTX-2.5 and a generic adapter.
2. Covers camera words, timing, performance, dialogue/sound, negatives, inputs, multi-shot, continuity, impossible physics, text/screens/hands/crowds, content filters, cost per take, a 37-row failure catalog and a 31-check linter. Model choice is C1; image consistency C2; camera meaning B1; light B2; beats A2.
3. Applies it to nine *The Catch* shots in six worked examples.

**Terms** [§1]. *Shot*: one camera view between cuts. *Clip*: one file from one request. *Take*: one clip made for a shot. *Master prompt*: model-neutral shot description stored in the breakdown. *Adapter*: rules rewriting it into one model's order and syntax. *Beat*: one visible/audible change at a moment in a clip. *Timecode*: in-prompt marker like `[0-3s]`. *End state*: sentence describing the final moment. *Identity / look / sound key*: fixed word block for a character (or creature/prop), a scene's light-colour-texture, or a voice / location background sound, pasted unchanged. *Control video*: rough clip (e.g. grey Blender "clay render") whose camera and blocking the model copies. *Native audio*: sound made in the same run. *Room tone*: steady background sound. *Negative prompt*: separate box of things to leave out. *Prompt enhancer*: built-in rewriter (MiniMax `prompt_optimizer`, Wan `prompt_extend`, LTX enhancer). *Seed*: number fixing randomness. *Multi-shot*: one request returning several cut shots. *Post operations*: flip, rotate, reverse, compositing in the edit. *Linter*: pre-send checklist run by an LLM.

## 2. Rules

**Inputs and length**
1. [R1, §9A] If the shot starts from an image, then write motion only (camera, subject, environment; opening image → first movement → continued action → final reaction) and call people "the woman", "the subject", because re-describing the image confuses the model.
2. [§9B] If using start and end frames, then describe the path between them, not both pictures, and make the end frame by editing the start frame, because very different frames make the model cut instead of transform.
3. [§9C] If attaching references, then attach only what the shot needs (start with 2–3, well-lit, single-subject) and name each one's job ("@Image 1 defines Iona's face"), because each reference lowered benchmark scores and unlabelled ones get ignored. Limits: Veo 3 images; Kling 3.0 Omni 7 (4 with a video); H3 9 images/3 videos/3 audio; Wan 3.0 10/5/5; Seedance 2.5 50 total.
4. [§9D] If a control video is attached, then text carries look, identity and sound and says camera and blocking come from the video, because describing the move again in other words competes with it.
5. [§3C] If sizing a prompt, then aim for: image-to-video one move 25–70 words; text-to-video 4–8 s 70–130; 10–15 s with 3–4 beats and dialogue 130–220; 20–30 s staged 180–300; each key adds 30–60. If over a hard limit, then cut beats and setting, never keys, because extra instructions go unseen. Limits: Veo 1,024 tokens; Runway 1,000 characters; H3 7,000; Hailuo 2.3/02 2,000; Wan 2.7 5,000 (negative 500, silently cut); LTX 200 words.
6. [§3B] If one element matters most, then put it in the first two sentences, because it costs nothing (first-sentence weighting is unverified).

**Camera**
7. [R3, §4] If a move is graded Unreliable (list in §6 below), then swap it for a reliable move with the same story purpose or give a control video, because camera, focus, size and angle vary most across models, rotation leaks into sideways travel and vertical moves are weaker. If graded "Usually works", then budget one extra take.
8. [§4] If writing camera, then one move per shot, with speed, relation to subject and where it ends ("slow push in, ending on her eyes"); for image-to-video, camera motion alone is the most reliable dynamism; if the move must be exact, then use a control video, because words cannot fix exact paths.

**Action and timing**
9. [R2, §5] If the clip is 8 s or shorter, then one camera move and one main action; generally one main action per 4–5 s, one line per 3–4 s, 3–4 beats per 15 s, because chained events come out muddled.
10. [§5] If writing actions, then use physical steps with counts or durations ("two slow steps") and end every clip over 6 s with an end state, because it gives the action somewhere to arrive.
11. [R15] If cause and effect must read in order, then use "then" or separate timecodes; if still flipped, then two shots, because effects can precede causes.
12. [R14] If a character must fail, then make the failure the described action, early, with a failed end state, because models favour success.
13. [R17] If a deliberate vanish/appearance is needed, then use Rec6, because accidental vanishing is uncontrollable.

**Performance**
14. [§6] If the script names an emotion, then write two or three observable behaviours (eyes and dwell, blinks, breath, mouth, jaw, hands, posture, a pause) and keep tone words for the voice only, because emotional performance is every model's weakest score.

**Dialogue and sound**
15. [R8, §7C] If lines must be word-exact, then ≤2.5 spoken words per second, one speaker change per 3 s, half a second of silence each end (8 s ≈ 15–18 words across two speakers), because models drop parts of long dialogue.
16. [R21, §7F] If a voice comes through glass, radio, earpiece or screen, then name its path; off-screen voices get "is not visible" in the same sentence, because otherwise it plays close and clean.
17. [R9, §7E] If a sound must land on an exact frame, then place or re-time it in the edit, because generated sound drifts 0.2–0.44 s and lip-sync errs 2–5 frames.
18. [R10, §7E] If music is non-diegetic, then suppress it in every clip and score once in the edit, because generated music changes at every cut and native-audio models may add it unasked.
19. [§7E] If writing sound, then name at most 2–3 sounds, each tied to the action making it (source + action + space), because extra sounds get dropped.
20. [R22] If the model is silent (Runway Gen-4.5, Luma Ray3.2), then delete DIALOGUE and AUDIO, write speaking only as visible behaviour, and make sound separately, because the text wastes characters and causes random mouth movement.
21. [§7B, §16] If a character speaks in several clips, then paste the same voice description; a Kling element with a bound voice gets delivery words only; Kling via fal with image elements cannot bind voices, so write the full sound key in the brackets, because voices otherwise drift.

**Negatives, shot mode, enhancers**
22. [R5, §8] If the model has a negative field, then put 3–10 short nouns aimed at the failure you saw and keep the main prompt positive, allowing only documented "No …" lines (No dialogue, No embellishments, No extra sound effects, No background music, Generate single shot); never a giant generic list, because negation can pull in the excluded thing and long lists hide the real problem.
23. [R4, §10] If one shot is wanted, then say so ("In a single unbroken scene" on Omni, which cuts by default; "Generate single shot." on Wan; Kling Multi-Shot off). Default one shot per clip; multi-shot only for a dialogue whose faces must match in one location, fast inserts, or cheap coverage tests, because multi-shot cost 7.9 points on average (up to 22.8).
24. [R7] If a platform rewrites prompts and the master prompt is complete, then turn the rewriter off, because it overrides careful wording.

**Continuity**
25. [R6, §11] If a character recurs, then paste the identity key word for word with the same references, the scene's look key unchanged, the current state (bandage, dressing) added, and each person's side and facing held through a dialogue, because consistency depends on unchanged descriptions. Ranked aids: references, identity key, look key, sound key, final frame as next start frame, seed, screen direction, state list.
26. [R18] If a take is mostly right, then change one field and rerun with the same seed, because rewriting everything adds new variables; a seed does not hold a face across different shots.
27. [R24] If there is no seed (Kling 3.0 on fal), then reuse the start frame and prompt.

**Physics**
28. [R13, §12] If people must float, then describe visible evidence (hair, cloth, straps drift; nothing settles), lock the camera to the room, show the world moving, never write "falling", because models default to gravity.
29. [R12, §12] If the world must be mirrored, inverted or reversed, then flip, rotate 180° or reverse in the edit (reverse only clips without faces or speech), because edits are exact and free. Mirror world: flip shots with no continuing character; with Iona, keep only her symmetric parts in frame or composite her unflipped over a flipped background; never flip a shot where a person's left/right is a plot point.
30. [§12] If an element is fragile (floating blood beads, sparks, a rising screw), then composite it from a Blender particle render or stock; if relative motion carries the story, then use a control video, because hanging liquid and complex motion fail.
31. [R20] If an LLM reviews clips, then a person still checks physics and hands, because AI critics miss most glitches (83.3–93.5% of clips had one).

**Text, screens, hands, crowds**
32. [R11, §13A] If on-screen text is needed, then ≤3 words per sign, exact, in quotation marks, other surfaces "plain"; backwards → generate forwards and flip, or composite; long → composite, because longer and incidental text collapses.
33. [§13B] If a screen appears, then make its content a separate full-frame clip and composite it, asking the main shot for "a blank dark tablet screen"; visor graphics are edit motion graphics.
34. [§13C] If hands matter, then one simple grip, name the contact, no finger counting in wides, key moments from a correct start frame with small movement, because hands melt.
35. [R16, §13D] If more than three characters act, then reduce them or keep extras few, soft and simple, because faces degrade in crowds.

**Filters, routes, budget**
36. [R19, §14] If refused, then reword by implication, sound, framing, aftermath, plain physical wording, genre first; if refused twice, then move the element to sound or compositing and log the support code, because filters are automatic and honest reframing passes; no misspellings or code words.
37. [R25] If Veo 3.1 needs 1080p/4K or references, then set 8 s, because 4 and 6 s are 720p only (Lite: no references, no extend; download within 2 days).
38. [R23] If a LoRA-locked camera move is needed on an open model, then use LTX-2 (19B), because LTX-2.5 has no camera add-ons.
39. [R26] If the model has no adapter, then use the generic adapter with two lowest-resolution tests and record what syntax worked.
40. [§17A] If a take costs over $2, then test the wording first on a cheap route (Veo Lite/Fast, Wan 480p, Seedance 480p); if a shot fails 4 takes on one route, then stop and escalate (control video, compositing, other model). Plan 3–4 takes for easy shots, 6–8 for hard ones.
41. [§0] If about to run a paid batch, then have the LLM re-open the official guides, because models and syntax changed repeatedly within a year.

## 3. Breakdown fields

| Level | Field | Plain meaning | Values / example |
|---|---|---|---|
| film | `model_facts_checked_on` | Date guides were re-read | 2026-09-27 |
| film | `music_policy` | Music in clips or not | `none_in_clips_score_in_edit` |
| character / prop | `identity_key` | Fixed appearance words | "Iona, a woman in her late thirties, lean and strong…" |
| character | `state_by_scene` | State appended to key | "right palm bandaged in white gauze" |
| character | `sound_key` | Fixed voice words | "a low, flat, controlled voice with a British accent" |
| character | `reference_images`, `bound_voice` | Reference pack; Kling voice | IONA_ref; 5–30 s sample |
| scene | `look_key` | Light source/direction, 3–5 colours, texture | CAGE, QUARANTINE-DAY |
| location | `room_tone_key` | Background sound sentence | "steady hum of air filtration…" |
| shot | `shot_id`, `purpose` (not sent) | Number + slugline; what audience must get | 13-04 INT. … |
| shot | `model_targets`, `duration_s`, `shot_mode` | Primary/backup; length; single or multi | Veo 3.1; Kling 3.0 / 8 / single |
| shot | `start_frame`, `end_frame`, `references`, `control_video` | Inputs, each with its job | label → file → identity/costume/set/prop/voice |
| shot | `camera` | Size; angle; one move, speed, end; lens only if needed | "slow push in toward the glass" |
| shot | `subjects` | Key or label; state; screen position; facing | "frame left, facing right" |
| shot | `setting`, `look` | Place, time, prop states; look key | "mesh gate SHUT" |
| shot | `beats`, `end_state` | `t0–t1:` behaviour (+camera, +sound); final frame | ≤1 main action per 4–5 s |
| shot | `dialogue` | SPEAKER (sound key; delivery; heard through): line | ≤2.5 words/s |
| shot | `audio` | Room tone; ≤3 effects; music | music: none |
| shot | `text_on_screen`, `exclude` | Exact sign words; negative nouns | ≤3 words / 3–10 nouns |
| shot | `physics_notes`, `post_ops` (not sent) | Deliberate wrong physics; edit ops | flip / rotate / reverse / composite / replace sound |
| shot | `continuity_in`, `continuity_out` (not sent) | Matches with neighbours | "ring hidden" |
| shot | `content_risk` (not sent) | Risk + §14 method | none / low / high + method |
| shot | `seed`, `budget` (not sent) | Kept seed; takes × s × $/s | "4 × 8 × $0.40 = $12.80" |
| generation job | `model_prompt`, `negative_text`, `settings` | Adapted prompt; negative box; duration/res/aspect | per §16 |
| generation job | `lint_report` | L01–L31 PASS/WARN/FAIL table | |
| generation job | `take_log`, `kept_take` | Files with seeds | |
| generation job | `refusal_support_code`, `refusal_count` | Filter log; 2 → move element | Veo 61493863 |
| generation job | `syntax_that_worked` | For generic-adapter models | |

## 4. Procedures

**4.1 MASTER SHOT PROMPT TEMPLATE [§15]** (verbatim; one per shot; write `none`, never delete a field):
```
SHOT_ID:          scene-shot number and slugline, e.g. 13-04 INT. TREATMENT FLOOR – MORNING
PURPOSE:          (not sent) one line: what this shot must make the audience see, feel or learn
MODEL_TARGETS:    primary model; backup model
DURATION_S:       seconds
SHOT_MODE:        single continuous shot | multi-shot (list the shots)
INPUTS:
  start_frame:    file name or none
  end_frame:      file name or none
  references:     label → file → what it controls (identity / costume / set / prop / voice)
  control_video:  file name + what it controls (camera, pacing, blocking) or none
CAMERA:           shot size; angle; ONE movement with speed; where the move ends;
                  lens or focus effect only if the story needs it
SUBJECTS:         for each: identity key (pasted) or reference label; state in this scene;
                  screen position; facing
SETTING:          place; time; key props and their state
LOOK:             look key (pasted): light source and direction; 3–5 colour words; texture/style
BEATS:            t0–t1: visible behaviour (+ camera change, + sound that belongs to it)
                  … at most one main action per 4–5 s
END_STATE:        how the final frame looks
DIALOGUE:         SPEAKER (sound key; delivery; heard through what): line
                  … at most 2.5 words per second of clip
AUDIO:            room tone; up to 3 effects tied to actions; music: none | describe
TEXT_ON_SCREEN:   exact words (≤3 per sign) | none
EXCLUDE:          3–10 short nouns for a negative field
PHYSICS_NOTES:    (not sent) what must look physically wrong-on-purpose, and how
POST_OPS:         (not sent) flip / rotate / reverse / composite / replace sound / none
CONTINUITY_IN:    (not sent) what must match the previous shot
CONTINUITY_OUT:   (not sent) what the next shot must match
CONTENT_RISK:     (not sent) none | low | high + method from Section 14
SEED:             number used for the kept take, if the model supports seeds
BUDGET:           (not sent) takes planned × seconds × price per second = $ (Section 17A);
                  cheap test route first if one take costs over $2
```

**4.2 Assembly [§15].** Adapter sets order and syntax. Keys pasted word for word; beats become time-ordered sentences; end state is the last visual sentence; dialogue in the model's speaker format; EXCLUDE → negative field, else positive wording or a documented "No …" line; `TEXT_ON_SCREEN: none` → "plain, unmarked surfaces".

**4.3 Recipes [§19].**
- **Rec1 Shot → master prompt** ($0, ~10 min): paste scene text, breakdown line, identity and look keys, §15; say "Fill in the MASTER SHOT PROMPT TEMPLATE for shot [ID]. Quote the screenplay lines it covers. Turn every emotion into behaviour. Keep dialogue under 2.5 words per second."; check PURPOSE and BEATS, correct in one sentence.
- **Rec2 Adapt, lint, send** ($1–$13 per shot): "Using Section 16, write the [model] version of this master prompt. Then run the Section 21 linter on it and fix every FAIL."; paste prompt and negative, attach named references, set duration/resolution; 2–4 takes, note each seed; if a setting is unavailable, pick nearest and re-run L02.
- **Rec3 Fix a take** (stop after 4 fails): describe the symptom; "Find this symptom in the Section 20 failure catalog. Change only the one field that fixes it. Show me the old and new sentence."; rerun same seed (or same start frame); after two failed fixes, consider control video, compositing or another model.
- **Rec4 Continuity** ($0): export kept take's final frame (editor or LLM-written `ffmpeg`); same view → start frame; new angle → set/light reference; same keys, updated states.
- **Rec5 Mirror shot**: classify (no character → flip; character, left/right irrelevant → flip, symmetric parts only; left/right plot point → no flip); prompt forward text and opposite directions (final pan right → ask pan left); flip; check every letter and arrow.
- **Rec6 Vanish/appearance**: locked-camera start frame without the element → clip A; add element to A's final frame by image editing (C2) → start frame of clip B, same seed and prompt except the element; hard-cut A→B (reverse order for a vanish); sound cue in edit.
- **Rec7 Dialogue**: one clip per speaker (shot/reverse shot), listener silent or soft; Kling Custom Multi-Shot only if faces must match in one location; if voices drift, replace with separate voice plus lip-sync.

**4.4 Generic adapter [§16].** Shot size and move → subject with key → actions with "then" → setting → look key → `Name (delivery): "line"` → one sound sentence → "No background music." if wanted; positive wording; "single continuous shot"; if a field is ignored, move it to the first sentence once; record what worked.

## 5. Checklists

**Linter, per shot before sending [§21].** Instruction: "Run each check on the prompt, the negative text and the settings. Output a table: check ID, PASS / WARN / FAIL, the offending text, and the fix. Then output the corrected prompt. Do not change anything a check does not require." FAIL (W = WARN) when:
- L01 over model limit or 300 words. L02 invalid duration/resolution/shape (Veo 4/6/8 s, 8 s for 1080p/4K/refs; Runway 2–10 s, 720p; Kling 3–15 s; H3 4–15 s, Max 5–15 s; Omni 16:9 or 9:16). L03 >1 camera move. L04 (W) dolly zoom, vertigo, rack focus, whip pan, 360°, mm lens without control video or fallback. L05 >1 main action per 4 s or >4 beats per 15 s. L06 (W) >6 s without end state. L07 emotion word without behaviour. L08 words >2.5 × seconds. L09 wrong speaker format. L10 pronouns or shared speaker labels. L11 relayed voice without path. L12 (W) no music line. L13 (W) >3 named sounds.
- L14 negation of a visible thing (documented "No …" lines, "No scene cuts" and whole-layer "No music"/"No voices" allowed). L15 negative field exists but EXCLUDE empty (W) or in sentences. L16 identity key differs by one word, or reference label varies. L17 look key missing/reworded. L18 start frame attached but appearance/set re-described. L19 named reference not attached, or attached one unnamed. L20 (W) single-shot phrase missing on Omni/Wan. L21 sign >3 words or backwards text asked of the model. L22 >3 acting characters. L23 "falling"/"gravity" without visible behaviour. L24 (W) injury/weapon words without §14 method. L25 (W) dialogue shot without sides and facing. L26 unsupported language. L27 flip planned, directions not reversed. L28 DIALOGUE/AUDIO sent to a silent model. L29 relies on a missing feature (seed on Kling via fal; voice on fal image element; references/extend on Veo Lite; LTX-2.5 camera add-on; end frame on Runway). L30 (W) cost over budget, or >$2 take before a cheap test. L31 dialogue differs from screenplay or action contradicts a stated set/prop state.

**Failure catalog, per take [§20].** Most rows restate §2 rules. Fixes not stated above: F1 dialogue shown as subtitles → colon format, "subtitles, captions, text" in negative. F4 lips off → nudge audio, wider framing, replace voice. F7 rack focus → two named planes plus trigger, or composite. F14/F15 missing bandage or light shift → state into key; look key; match in grade. F21 floating liquid splashes → "perfect round beads, slowly turning". F23 fewer clips returned than requested → output filter; reduce injury words. F25 extra people → "Only two people in frame" + "extra people" negative. F27 start/end clip cuts → closer frames, intermediate keyframe, longer clip. F32 creature looks like costumed person → C2 reference pack, materials and proportions in key, start frame. F34 settings rejected → change setting, not prompt. F36 negative tail ignored → Wan cuts at 500 characters.

**Continuity, per shot [§11, Rec4].** Same references; keys unchanged; current state added; sides and facing stated; final frame exported; seed logged.

## 6. Saying it to AI models

**Core fields [§3A]:** subject (specific), action (in order), setting, camera, lens/focus only if needed, light by named source ("soft window light with warm lamp fill, cool rim from hallway", not "brightly lit room") plus 3–5 colours, style named early, audio in separate sentences.

**Camera [§4]:** Reliable: "Static shot, the camera does not move" (Wan "fixed camera"; H3 "holds a perfectly static shot"), push in with speed and end, "pull back to reveal …", pan, tracking with side ("at her left"), handheld with amount ("slight sway"), over-the-shoulder naming the shoulder, one shot size ("ending in a close-up"). Usually: POV with an anchor (hands, torch beam), tilt, crane, half-circle orbit. Unreliable: zoom (crop in edit), whip pan (cut), rack focus (trigger: "as she turns, focus shifts from the cup to her face"), dolly zoom, "85mm" (say "compressed background, shallow focus"), compound or numeric moves. Old Hailuo brackets (`[Push in]`, `[Static shot]` etc., max three) belong to retired models.

**Timing:** Veo `[00:00-00:02]`; Omni `[0-3s]`/"After 3 seconds"; Kling "At the 4th second"/"Shot 1 (2s):"; Seedance `0–5s:` + `End state:`; Wan `Shot 1 [0–3 s]`; H3 "at 00:04.500"; LTX "then", "a beat".

**Speakers [§7A]:** Veo/Omni `A woman says: My name is Clara.` (no quotes, or words get drawn). Kling `Name (delivery, tone, accent): line`. Wan `[Name, voice label]: "line"`, unique labels, action before line, linking words ("Immediately, …"); unwritten lines get invented. H3 `<Subject 1> (S1) speaks softly, <d>[English] line</d>` or "quietly says, '…'". LTX `Name (delivery): "line"` plus language and accent. Voice formula: lines + emotion + tone + speed + timbre + accent. Omni fully supports English only; Kling 5 languages; H3 11.

**References:** Veo "Using the provided images for …"; Omni `<FIRST_FRAME>`, `<IMAGE_REF_0>` (same first and last frame = loop); Kling `@Element1`; Seedance `@Image 1`/`[Image1]`, "Refer to @Clay Render 1 for camera movement, pacing, shot-size transitions, subject trajectory, and blocking."; Wan `Image 1`.

**Adapter order and quirks [§3B, §16]:** *Veo*: camera → subject → beats → setting → look → `Ambient noise:`/`SFX:`; `negativePrompt` only on Google Cloud. *Omni* (`gemini-omni-1.1-flash`): `[# Sources …] [# References …]` first, role line last, "In a single unbroken scene", `Sound design:`, "No …" lines, exact sign text; edits "Keep everything else the same.". *Kling*: atmosphere → `@elements` → camera → timed actions → dialogue → ambient; keep default negative "blur, distort, and low quality"; `cfg_scale` 0.5 (raise if ignored, lower if stiff). *Seedance*: goal → reference jobs → "single continuous take, no cuts" → stages → end state; no negative field, so protect the thing ("keep her face identical to @Image 1"). *Wan*: keyword line (size, angle, light, composition, tone) → entity → scene → motion → sound; avoid real names, rapid scene changes, exact text, long choreography, exact lip sync. *H3*: world and action timeline → `overall_soundscape:` → `non_diegetic_music:`; hints `[pan]`/`[static]` after their description. *Runway*: plain declarative, positive, motion only from a start frame, under 1,000 characters. *Ray3.2*: target end state only, no commands, no "no/not/without/devoid of/missing". *LTX-2.5*: one present-tense paragraph, 4–8 sentences: shot and genre → scene → action → characters' physical cues → camera with end position → audio; avoid complex physics, many characters, clashing lights.

**Phrases that work [§12–14]:** "her hair, shirt and loose straps drift up and outward; nothing settles"; "through the mesh of the closed gate, the brick wall streams upward"; "The camera is fixed to the cage and does not move relative to it"; "a dark red stain spreads through his shirt"; "A tense dramatic thriller scene."; "her voice comes through a small intercom speaker, slightly thin"; creatures by visible parts, "faceless", never "alien"/"monster". What fails: "zero gravity" or "falling" alone, emotion labels, "no walls", quoted Veo dialogue, long or backwards signs, literal injury words.

## 7. The Catch

**Keys [§22.0]** (illustrative; real ones come from the character-design and look files). Identity: IONA (late thirties, dark brown low knot, grey-green eyes; states: cage faded blue work shirt; quarantine grey pyjamas, right palm bandaged; ship white pressure suit), JUDE (mid-forties, olive canvas jacket), ELI (early thirties, untrimmed beard, grey coat over pyjamas), SAYE (late fifties, grey hair, charcoal cardigan), THE FIGURE (~2.5 m matte-black armoured diving suit, pale strip sliding behind a clear face cover), THE ANIMAL AND VESSEL (forearm-long vessel of dark water; hand-sized comb-jelly-like animal, thread-thin limbs). Look: CAGE, QUARANTINE-DAY, PASSAGE, RECESS, CCTV-NIGHT. Sound: British voices (Iona low, flat, controlled; Saye measured, precise; Jude warm, slightly gravelly); quarantine room tone. States to track: Iona's palm, Jude's shoulder dressing, the figure's cracked then patched cover.

**Shots.** **13-04** dialogue through glass: 8 s Veo 3.1 (backup Kling), two-shot push in, Saye via intercom, 2.1 words/s. **09-22** weightless cage: 6 s Seedance 2.5 + clay-render control video (backup H3 from start frame), camera bolted to cage, gate SHUT, Eli's other hand hidden (the puck), blood beads composited if needed. **11-07A/B, 11-08** mirror world: "LEVEL 2" generated forwards on Omni, pan left, flipped (backup Runway from pre-flipped still); reaction 11-07B unflipped; exit sign flipped. **18-31** chest opens: Kling start+end frames (backup H3), four latches, re-time clacks and pump. **18-32** animal reveal: Veo 3.1 Standard, three references (backup Seedance), "faceless"; **18-33** planned only. **14-05A/B** tablet surveillance: Rec6 on Wan 3.0 (backup LTX), CCTV-NIGHT, cup slides, then figure present; composite onto tablet, timestamp and click in edit. **09-15** shot through roof: 4 s Veo 720p (backup Kling), shooter off-screen, spark, "Oh.", stain under his hand, gunshot in edit. Never flip ring shots ("On her right hand."). Budget ≈ $50 at 4 takes each before tests.

**Flagged for writer/user:** the 13-04 intercom is a design choice not in the script; the nurse is framed out and needs her own insert; keys and British voices await the design files; which mirror shots contain Iona (Rec5 class); 18-33 unwritten; budget ceiling.

## 8. Conflicts and open questions

- **Unverified [§23]:** Runway's prompt guide (blocked); Gen-4.5 multi-shot; prompt limits for Kling, Seedance, Omni, Wan 3.0; seeds on Omni, Wan 3.0, H3; Wan 3.0 negative field and "Generate single shot."; H3 `<d>` token via API; Ray3.2 text-to-video; Seedance dialogue syntax; first-sentence weighting; backwards text; Omni "No subtitles"; Runway/H3/LTX prices (from C1); models released in late September 2026.
- **Dated benchmarks:** AVGen-Bench (audio) and FilmBench did not test several current models.
- **Veo quotes:** 2025 blog used quotation marks; Sept 2026 docs say colon form (file follows docs).
- **Versus C1 (voice):** C3 generates voices in-clip and replaces only on drift; C1's digest says record/synthesise lines first. Pipeline must pick.
- **Versus C1 (LTX):** C3 camera LoRAs only on LTX-2 (19B); C1's digest routes open control via an LTX-2.3 union LoRA. Different add-ons; confirm with C4.
- **Versus C2 (text):** C3 lets Omni draw a ≤3-word sign then flips the clip; C2's digest makes exact text an SVG insert.
- **Aspect ratio:** examples assume 16:9; B1/C1 discuss 2.39:1.
- **Naming:** "Kling 3.0 Omni" here vs "Kling O3" in C1's digest.
- **Internal:** file claims "seven" examples/shots; §22 has six examples, nine shot IDs.

## 9. Section map

- **§0** Labels, scope, staleness rule, fact-check corrections. **§1** Glossary.
- **§2A–D** Per-model limits, structure, timing; dialogue, negatives, seeds, references; superseded models; unadapted models.
- **§3A–C** Fields; order per model; lengths. **§4** Camera reliability and rules. **§5** Action and timing. **§6** Emotion as behaviour with *Catch* lines.
- **§7A–G** Speakers, voices, word budget, audio benchmark, effects/music/silent models, relayed voices, text off screen.
- **§8** Negatives per model. **§9A–D** Image-to-video, start/end frames, references, control videos. **§10** Multi-shot. **§11** Continuity. **§12** Physics and mirror world. **§13A–D** Text, screens, hands, crowds. **§14** Filters.
- **§15** Master template. **§16** Adapters. **§17/17A** Tool per aim; costs and budget rules. **§18** 26 rules. **§19** 7 recipes. **§20** Failure catalog. **§21** Linter.
- **§22** Keys and six worked examples (full master prompts and per-model prompts). **§23** Unverified. **§24** Sources P1–P55.
