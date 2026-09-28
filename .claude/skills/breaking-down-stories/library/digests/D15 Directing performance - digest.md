# Digest D15: Directing performance for generated characters (28 Sept 2026)

Source: `research/D15_performance_direction.md` (fact-checked 28 Sept 2026). Brackets: §3 rule n = decision rule; §1.n = principle; other § = section. **[V]** primary page read 27-28 Sept 2026; **[U]** unverified; **[J]** judgment. Re-check tool limits and prices after 28 Oct 2026.

## 1. Scope

1. Merges A1, A2, A3, B5 and C3 into one `performance` block per acting character per shot: tactic, task, timed behaviour, eyeline with dwell, breath, stillness, display level 1-3, must-not, state in and out, capture route.
2. Gives a maker-backed (still untested) vocabulary of visible behaviours, and a non-actor's guide to recording 3-5 s driving clips for Runway Act-Two, Kling Motion Control, Luma Ray3.2 Modify Video and Wan-Animate-2.
3. Keeps breath, energy, eyes and hands continuous across separate clips; worked through *The Catch* and *The Long Places*.

## 2. Rules

**Principles** [§1]
1. [§1.1] If a script line names a feeling, then play the tactic and show behaviour, never the word, because every maker guide asks for visible cues and FilmBench found "the performance group is uniformly the lowest-scoring L2 cluster in both tasks" (action performance averages 50.8 and 46.8 of 100) [V].
2. [§1.3; §2.2] If the shot is closer, then the display level is lower, because level 3 in a close-up reads as melodrama (A1 P10) [J].

**Writing the block** [§3]
3. [§3 rule 1] If a script line names an emotion ("Her face changes.", "not steady"), then write two or three timed behaviour steps and keep the word only in `notes` and the voice delivery, because maker guides ask for visible cues and A3 R2 bans emotion adjectives.
4. [§3 rule 2] If a beat is a turning point or has A2 intensity 4+, then write A2's five steps as timed steps (desire as eyeline; antagonism as what is seen; choice as a held half-second; action; expression), because A2 P10/Step 8 give seeing and choosing their own screen time.
5. [§3 rule 3] If the line, eyeline or cut already carries the beat, then use display level 1, "still" or one movement, because B5's restraint rule saves bigger faces for turning points.
6. [§3 rule 4] If a character is alone or acts only on objects, then fill `task` and write `tactic: (task only)`, because only an attempt on a person can be played (A3 §3.2).
7. [§3 rule 5] If a behaviour step is shorter than about 0.5 s, then lengthen it or plan a transfer, because a micro-expression is "a quarter to half a second" (B5), 6-12 frames at 24 fps [J].

**Stillness, silence, eyelines**
8. [§3 rule 6] If a hold is 2 s or longer, then name every still part and the one moving part, and add "The camera does not move.", because models fill empty time [J].
9. [§3 rule 7] If lips part in silence, then add "No dialogue." and "closes it without a sound", because parted lips invite generated speech on native-audio models [J; C3 L14 allows "No dialogue"].
10. [§3 rule 8] If pauses compete for long holds, then apply A1 R15 (long hold = 3 s or more, ranks 1 and 2 only) before writing stillness over 3 s.
11. [§3 rule 9] If an eyeline change is itself a beat, then put that look in `must_not` for every earlier shot; if the script gives an earlier look, then aim it at a different target and add "meets her eyes" to its `must_not`, because one early glance spends the beat.
12. [§3 rule 10] If the eyes move, then name target and dwell ("to the flask; stays 2 s"), never "looks around"; for separately generated singles write opposite frame directions and "does not look into the camera" (A2 R26; A1 R44).

**Continuity**
13. [§3 rule 11] If a shot continues the previous one, then copy the previous `state_out` into `state_in` and make it the prompt's first sentence; if the camera does not cut away, then also use the last frame as start frame (C3 §11), because each clip starts blank.
14. [§3 rule 12; §6.3] If a state must change, then change it inside a behaviour step, never at a clip boundary, and match breath phase across cuts (out-breath into out-breath), because a change at a cut reads as an error [J].
15. [§3 rule 13] If breath is not visible (helmet, back, wide), then carry it in sound (D3), because the audience hears breath before it sees it.

**Capture route**
16. [§3 rule 14] If a key shot's meaning depends on the timing of a look, swallow or breath, then consider `transfer_face`, because "you control the timing of a look far better than a prompt can" (C1 R12).
17. [§3 rule 15] If hands, posture or distance carry the beat, then use `transfer_body` or `previs`; if only the face does, then `transfer_face`, because body capture adds hand errors for no gain [J].
18. [§3 rule 16] If the character is not human-shaped, then use `previs` (C4 Level 2-3) or Wan-Animate-2, because Kling's driving clip "Should contain a realistic style character" with matched full- or half-body framing, while Wan-Animate-2's model card animates a kitten [V].
19. [§3 rule 17] If a prompt-route take fails the same must-not twice, then change the capture route, not the wording (C3 Recipe 3).
20. [§3 rule 18] If `capture` is a transfer, then send no movement words: Act-Two has no text prompt; Kling's prompt is optional; Wan-Animate-2 wants appearance and background [V]. Where text exists, send identity key, state line, look and setting only, because the clip carries the movement [J].
21. [§3 rule 23] If the framing, camera move and blocking can be acted for real, then consider Ray3.2 Modify Video with Face on, because it transforms the recording itself ("Your original movement, timing, and intent become the instruction") [V]; it has no sound, and Face "pays less attention to the center of the forehead and the upper cheeks", so brow- or cheek-only beats need Structure 8 or another route [V].
22. [§3 rule 24] If two or more faces must act against each other in one frame, then act together and use Ray3.2 ("up to eight faces simultaneously") or act each alone and composite, because Kling uses only "the character occupying the largest portion of the frame" [V].

**Sides and models**
23. [§3 rule 19] If a one-sided expression's side matters, then never ask for the side in words; flip an approved still and run the mirror test before any transfer, because models place sides at random (B5 §14, Ex2).
24. [§3 rule 20] If the performer can only make the expression on the wrong side, then flip the driving clip before upload, never the output, because flipping the output flips the set and its text [J].
25. [§3 rule 21] If a prompt-only shot is performance-led, then start with Seedance 2.0 (FilmBench's performance leader) or its successor; FilmBench did not test Seedance 2.5, Wan, LTX, Sora 2 or any transfer tool [V; J].
26. [§3 rule 22] If the model's guide pairs labels with cues (Kling, Wan), then one mood word may follow the behaviours, never replace them [V; J].

**Recording**
27. [§5.1 correction] If recording a driving clip for Act-Two or Kling, then make each trimmed piece at least 3 s (record 3-5 s per beat), because both set a 3 s minimum; C1's "2-5 s" is wrong [V].

## 3. Breakdown fields

| Level | Field name | Meaning | Allowed values / example |
|---|---|---|---|
| shot | `character` | who acts | B5 name: `IONA` |
| shot | `tactic` | action on someone, one gerund | transitive gerund; reactions may be intransitive (`absorbing`); `(task only)` |
| shot | `task` | what hands or body physically do | verb phrase or `stillness`: `"chews the mint leaf"` |
| shot | `behavior` | timed visible steps | list of `t0-t1: behaviour`; ≤1 main action per 4-5 s (C3 §5) |
| shot | `eyeline` | target, direction, dwell, next | `{target, frame: frame-left \| frame-right \| lens \| down \| up \| at OBJECT \| off-screen, dwell_s, then}` |
| shot | `breath` | state, how it shows, when it changes | `{state, visible_as, change_at}`; states: `normal`, `one_breath`, `controlled`, `held` (≤~3 s on screen), `catch`, `release`, `shallow_fast`, `voiced`, `not_visible` |
| shot | `stillness` | parts that do not move | `head, eyes, mouth, hands, torso, feet, whole_body, none` |
| shot | `display_level` | how much shows | `1` contained, `2` visible, `3` open |
| shot | `must_not` | what would break the beat | short phrases: `[upper lip raised, tears, looking at Eli]` |
| shot | `expression_ref`, `effort` | links to B5 | `"B5 IONA (3), revised"`; `home \| stress \| break` |
| shot | `state_in`, `state_out` | state carried in and out | `{breath, display_level, eyeline, hands, posture, eyes_wet: yes \| no}` |
| shot | `capture` | how the performance is made | `prompt \| still_then_i2v \| transfer_face \| transfer_body \| previs \| flip_still` |
| shot | `driving_clip`, `voice_ref` | clip file; D3 delivery ID | file or `none`; `VOICE-IONA.D02` |
| character | `default_display_level`, `tells` | usual level; small repeated giveaways | 1-3; exact line + behaviour (Melek's knock + two breaths) |
| scene/sequence | `through_line` | state ledger for one character | table: `shot_id`, end-of-shot `breath`, `display_level`, `eyeline`, `hands` (sides), `posture`, `eyes_wet`, `carried_by` (start frame, first sentence, driving take, sound) |
| generation job | `performance_prompt`, `performance_check` | behaviour sentences for one model; take review | text; PASS/FAIL per item |
| film | `vocab_test_log` | vocabulary test results | phrase, model, date, takes, followed 0-3 |

Write `none` rather than deleting a field. Blueprint names differ and win (see §8 item 1).

**Terms** [§0]: *tactic* = what a character tries to do to someone, one "-ing" verb; *task* = what the hands or body do; *behaviour step* = `start-end: what happens`, in seconds; *dwell* = how long the eyes stay; *display level* = how much inner pressure shows (1-3), not A2's *intensity* (1-5 story pressure); *must-not* = behaviours that break the beat, never written as "no X"; *state ledger* = breath, level, eyeline, hands, posture, wet eyes, shot by shot; *driving clip* = a short video of a real person acting; *performance transfer* = copying its movement onto a character.

## 4. Procedures

**4.1 Block template** [§2.4], reproduced exactly:

```yaml
performance:
  - character: <NAME>
    tactic: <gerund>
    task: <hands/body task>
    display_level: <1 | 2 | 3>
    behavior: ["<t0>-<t1>: <visible behaviour>"]
    eyeline: {target: <>, frame: <>, dwell_s: <>, then: <>}
    breath: {state: <>, visible_as: <>, change_at: <>}
    stillness: [<>]
    must_not: [<>]
    expression_ref: <or none>
    effort: <home | stress | break>
    state_in: {breath: <>, display_level: <>, eyeline: <>, hands: <>, posture: <>, eyes_wet: <yes | no>}
    state_out: {breath: <>, display_level: <>, eyeline: <>, hands: <>, posture: <>, eyes_wet: <yes | no>}
    capture: <prompt | still_then_i2v | transfer_face | transfer_body | previs | flip_still>
    driving_clip: <file | none>
    voice_ref: <D3 ID | none>
```

**4.2 Recipe P: fill the blocks for a scene** [§7] ($0, ~20 min)
1. Paste the scene text, its A2 beat table, its A1 labels, the relevant B5 entries and D15 sections 2-4.
2. Say: "Fill a D15 performance block for every acting character in every shot of scene [ID]. Quote the line each block serves. Use only §4.2 behaviours or behaviours the script gives; mark others [design choice]. Set state_in from the previous state_out."
3. Read only `tactic`, the first step and `must_not`. Correct in plain words ("She is confused here, not angry").
4. Say: "List every hold of 2 s or more and check it against A1's pause ranking."

**4.3 Recipe W: performance into a prompt** [§7] ($0). Say: "Using this D15 block and C3 §16, write the [model] behaviour sentences. Primary behaviour first; tone words only in the dialogue line; turn every must_not into a positive stillness sentence or a negative-field noun." Paste under BEATS in C3's master prompt; run C3's linter.

**4.4 Recipe V: test a vocabulary row** [§4.4] (~$3-6, 20 min per row)
1. Make one neutral still of a test character in a plain room, medium close-up (C2).
2. Ask the LLM: "Write a 5 s image-to-video prompt for this still using only row [n] of D15 §4.2. Static camera. No dialogue. No background music."
3. Make three takes on each of two models.
4. Mark each take yes/no: primary behaviour present and in order? Stillness held? Anything from the must-not list?
5. Log in `vocab_test_log`. 2+ of 3 = "tested: works on {model}"; 0-1 on both models = use a transfer.
6. Test the riskiest rows first: outwaiting, trying to smile, speechless, shock.

**4.5 Recording set-up** [§5.3] (10 min, once)
1. Phone on a tripod or books, eye height, locked; no beauty filter or portrait blur.
2. Record 1080p, 24 or 30 fps, MP4 (under Runway's 32 MB URL limit [V]).
3. Check the *saved* file for mirroring, not the preview [U].
4. Face a window or soft lamp, nothing bright behind; light both sides evenly.
5. Plain wall, nobody else in frame.
6. Plain top contrasting with the wall, sleeves above wrists, hair off face, no glasses.
7. Tape marks at eye height left and right of the phone where other characters "stand".
8. Use the real prop from `task`.
9. Hands away from the front of the body; never cross arms [V Kling visibility; U "spaghetti limbs"].
10. Match the character image's framing (half body with half body).
11. Anyone else performing signs D4's consent form before upload (D4 Recipe 4 step 5); your own face: `self_consented` with date (D4 rule 9).

**4.6 Acting sheet** [§5.4] (the LLM prints it under each shot)
1. Hold the `state_in` pose 0.5 s before, the `state_out` pose 0.5 s after.
2. Do the task for real.
3. Say A1's `unsaid` line silently to the tape mark.
4. Count step times under your breath or with a metronome app.
5. Breathe the breath state: actually stop breathing on `held`.
6. Play it smaller than feels right.
7. Keep your head still unless a step moves it [U: sharp turns cause Kling face drift].
8. Three takes, at display levels 1, 2 and 3.
9. Speak the lines with sound on, so one file drives the face and D3's speech-to-speech voice.

**4.7 Recipe T: act and transfer one shot** [§7] ($1-5, ~40 min first time)
1. Say: "Print the D15 §5.4 acting sheet for shot [ID], with the behaviour times as counts."
2. Set up (4.5). Record three takes with 0.5 s heads and tails; trimmed clip ≥3 s.
3. Trim: `ffmpeg -ss 0.5 -i take1.mp4 -t 4 -c:v libx264 -pix_fmt yuv420p -c:a aac take1_trim.mp4`. Flip if the one-sided expression landed wrong: `ffmpeg -i take1_trim.mp4 -vf hflip -c:a copy take1_flip.mp4` [tested, ffmpeg 7.0.2].
4. Upload with the approved character still (flipped for a MIRRORED era). Act-Two: no text. Kling/Wan: identity, look, setting only.
5. Settings: Act-Two `expressionIntensity` 2 for display level 1, else 3; `bodyControl` off for face-only. Kling: `image` orientation ≤10 s or `video` ≤30 s with a face element. Ray3.2: Face on, Structure 8 for a real-looking face.
6. Review in order: eyeline direction; timing (key behaviour within ~0.25 s of the driving clip); hands; identity against the B5 hero portrait; display level; sides; must-not list. Log in `performance_check`. Fail once: re-perform with the fix; fail twice: change route.

**4.8 Recipe C: carry-over between clips** [§6.2]
1. Export shot N's last frame: `ffmpeg -sseof -1 -i shotN.mp4 -update 1 -q:v 1 shotN_last.png` [tested].
2. Copy N's `state_out` into N+1's `state_in`.
3. Same view: frame = N+1's start frame. New angle: pose reference, and open the prompt with the state ("She is still kneeling, not breathing, eyes on the bracket.").
4. Trim any settling movement or fresh face at N+1's head.
5. Lay continuous breath sound across the cut (D3).

## 5. Checklists

**Per shot** [§8]: (1) a block for every acting character; (2) tactic a gerund, task physical; (3) no emotion words in `behavior`; (4) steps timed, ≤1 main action per 4-5 s; (5) eyeline has target, direction, dwell; (6) breath state set; (7) stillness named for any hold ≥2 s; (8) display level fits shot size; (9) must-not filled, none written as "no X"; (10) `state_in` = previous `state_out`; (11) capture route chosen, with a reason for key shots; (12) D3 delivery matches the breath; (13) transfer shots: no movement words in any text box.

**Per scene**: (1) at most two long holds, per A1's ranking; (2) beat-eyelines protected in earlier shots; (3) one display peak, at or after the main turn; (4) no unexplained jumps in the ledger; (5) signatures at most once per scene except in a payoff scene (B5 §5.6).

**Per take**: (1) primary behaviour present, in order; (2) stillness held; (3) no must-not items; (4) eyeline and sides correct; (5) nobody speaks who should not; (6) no face reset at the start; (7) hands intact.

**Failure → fix**: see file §9 (11 symptoms, each with cause and fix).

## 6. Saying it to AI models

- **Vocabulary** [§4.2; untested until Recipe V runs; full table there]: shock "stops moving completely; eyes fix on {target}" (1.5-3 s); recognition "eyes fix on {target}; brows draw together slightly"; confusion "eyes lose focus and drift down"; fear "eyes widen slightly, stay on {target}; she backs one step"; suppressed anger "jaw tightens; one slow breath through the nose; eyes fixed"; withholding "eyes go to {object}, not to {person}"; relief "shoulders drop; one long breath out"; outwaiting "does not move or speak; eyes stay on {target}"; trying to smile "one corner of the mouth lifts; cheeks do not rise; eyes stay flat"; speechless "opens her mouth, holds it open, closes it without a sound; eyes drop". *Disgust* and *anguish* deliberately missing.
- **Breath wording** [§2.3]: "her shoulders rise once with one slow breath"; "she breathes slowly through her nose; her shoulders stay level"; "her shoulders and chest go completely still"; "a short, sharp breath in through parted lips"; "she lets out one long breath; her shoulders drop".
- **Phrasing** [§4.3]: primary behaviour first; one sentence per step joined by "then"; timecodes only where the model supports them (C3 §5); name body parts ("his left thumb"); for stillness say what is still and for how long ("Her head and hands stay completely still for three seconds; only her eyes move."); tone words only in the voice line.
- **Maker evidence** [§4.1, V]: LTX "Avoid emotional labels like 'sad' or 'confused' without describing visual cues"; Seedance 2.5 "You are converting an internal emotion into something visible". Kling and Wan pair labels with cues and print tears or sobbing beside grief. No guide covers whole-body holds, one-sided expressions or breath-holding.
- **Transfers**: no movement text (rule 20). Figure prompt, untested: "It moves in separate, complete motions with a full stop between each; its arms move first and its body follows a moment later; its head stays level; when it stops, one hand sinks slightly and hangs."

## 7. The Catch

**Decisions made (for the user to confirm where marked)**
- **sc10 B7, the mint** (Ex1): tactic *discovering*, level 1, close-up, `transfer_face`, Act-Two first. Order: half-second hold, chew, chewing stops, brows draw together and eyes drift down, one slow check-chew, stillness, then "Not mint." on the out-breath (6 s; breath `held` 2.0-5.0). Must-not: upper lip raised, nose wrinkled, tears, looking at Eli, a smile. Voice `VOICE-IONA.D02`. B8 splits off at the beat boundary from one continuous driving take; Iona *absorbing*, eyes come up at "street signs either".
- **sc13 "Silence."** (Ex2): one wide, 3 s, all three still; Iona *absorbing* (held breath, one blink), Eli *withholding* (eyes on the monitor, must-not "looking at Iona"), Jude *witnessing* (eyes on Iona). Fallback: three face transfers composited.
- **sc28 Eli's wrong-side smile** (Ex3): *reassuring*, level 1, one corner lifts on the MIRRORED side (frame left), cheeks do not rise; C5 paper oversuit. Mirror test once before any sc28 shot (~$1-3): flipped sc03 still with neutral mouth on an unflipped RECEIVING background; 4 s clip lifting the frame-left corner; Act-Two (intensity 2) and Kling `video`; score side, one-sidedness, cheeks, parting; if symmetric, use `flip_still`. Flip Kling face-element photos too.
- **The figure** (Ex4): two tempos only (care: glide/press; task: punch), arms lead and trunk follows, no human weight shifts, one early hand-drop as the dead-weight clue, pale strip never tracks. Capture: C4 previs first, Wan-Animate-2 second, Ray3.2 Poses on a previs render third (untested).
- **Breath sc01-02** (Ex5): `one_breath` → `controlled` through the climb (torch in teeth) → `held` at "She goes still." → jaw clamped at the fall → `release` into "(through the torch) No." → slower `controlled` → one long `release` at the sill. Must-not: panting before the rung, any sound of fear, looking down after the fall. Arc closes at sc27 "Breath in the helmet." and sc28 "Nothing but breath." (`voiced`).
- **The Long Places** (Ex6): "two breaths entire" ≈ 6-10 s (resting 12-20 breaths/min [V]); log Melek's knock-and-two-breaths once in `tells` (Yusuf, Márton, Nilay inherit it).

**Flagged for the user**
1. Drop B5 IONA (3)'s upper-lip lift for the mint (reads as disgust; A2 says "recognition and confusion, not disgust").
2. sc13 long holds: "Silence." and the post-"I wasn't asking her." hold get 3 s; "She waits" becomes ~2 s; "Nothing in it" is A1's focus-pull shot.
3. sc13 B12 "He watches her look at it.": Eli watches her palm, never her eyes, so B14 stays new.
4. sc20 "Almost smiles.": does any corner move (era B, NORMAL side)?
5. Consent: whoever performs driving clips (D4).

## 8. Conflicts and open questions

1. **Blueprint field names win.** Its `subject` line uses `display`, `still` (no `feet`, `none`), untimed `does`, `energy` (still/held/rising/breaking/spent) plus `continues` instead of `state_in`/`state_out`, snake_case `frame_left`, and `must_not` only for behaviour saved for a later beat. It has no `breath` or `driving_clip`. Proposal: add `breath` as a subject sub-part.
2. **Intensity vs display**: A2 `intensity` 1-5 is story pressure; display 1-3 is what shows; keep both.
3. **B5 (3) vs A2 vs C3** on the mint face: file drops the lip lift; user decides.
4. **A1 vs A2 on sc13's turn** ("You." vs B7/B12/B15): changes which pauses get long holds.
5. **A1 R15 (long ≥3 s) vs A2 ("at least 2 s")**: file uses 3 s.
6. **C1 Recipe 7 "2-5 s"** vs the 3 s minimum of Act-Two and Kling [V].
7. **C4's "up to 15 s"** for Kling 3.0 Motion Control vs fal's 10 s `image` / 30 s `video` [V]; C4 should be updated.
8. **C1/C3 "16 keyframes"** is Ray3.2 generation; Ray3.2 Modify Video takes 64 [V].
9. **Act-Two has no prompt** [V]; the first draft's "look and setting in the text" holds only for Kling and Wan.
10. **Side handling** in Act-Two, Kling and Ray3.2 is unknown until the mirror test runs.
11. **Vocabulary is untested**: no §4.2 row has been generated.
12. **Awards**: 99th Oscars acting needs roles "demonstrably performed by humans with their consent" [V]; whether transferred performances qualify is D4's question.
13. **Runway help pages** were bot-blocked; limits come from the API and pricing pages only.
14. **Verb form**: A3 infinitives vs A2/D15 gerunds; store gerunds (blueprint K28 agrees).

## 9. Section map

| Need | File section |
|---|---|
| Terms | §0 |
| Principles | §1 |
| Fields, display levels, breath states, template | §2.1-2.4 |
| Decision rules 1-24 | §3 |
| Maker quotes; vocabulary; phrasing; Recipe V | §4.1-4.4 |
| Tool limits; face vs body; set-up; acting sheet; review | §5.1-5.4 |
| State ledger; Recipe C; energy across cuts | §6.1-6.3 |
| Recipes P, W, T | §7 |
| Checklists | §8 |
| Failure modes | §9 |
| Worked examples: mint, Silence, wrong-side smile, figure, breath, *Long Places* | §10 Ex1-Ex6 |
| Conflicts | §11 |
| Sources | end |
