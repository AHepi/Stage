# D15. Directing performance for generated characters: a per-shot performance spec and a capture workflow

> **What this file is for**
> 1. It merges the acting advice spread across A1, A2, A3, B5 and C3 into one `performance` block per acting character per shot.
> 2. It gives a vocabulary of visible behaviours for common emotions, with what each model maker's guide shows and what is still untested.
> 3. It tells a non-actor how to record a 3-5 s "driving clip" of themselves for Runway Act-Two, Kling Motion Control, Luma Ray3.2 or Wan-Animate-2.
> 4. It keeps breath, energy, eyes and hands continuous across separately generated clips.
> 5. Input: a scene split into beats (A2) with its lines labelled (A1). Output: filled blocks, prompt sentences and driving clips.

Labels: **[V]** verified on the web on 2026-09-27; **[U]** found but not confirmed from a primary source; **[J]** my judgment. Scene numbers count the 30 sluglines of *The Catch*'s 25 September 2026 workshop revision (as in A2 and B5).

> **Fact-check pass (2026-09-28).** Every tool limit, price and maker quote below was re-opened at its source; every quoted line of *The Catch* and *The Long Places* was matched word for word against the uploaded texts. Corrections made in this pass: Runway Act-Two takes **no text prompt** (rule 18, Recipe T); Luma's performance tool is **Ray3.2 Modify Video**, with up to **64** keyframes, not "Modify Video V2, 16 keyframes" (5.1); Kling asks for matched **framing** (full body or half body) and a "realistic style" driving figure, not matched "proportions" (rule 16, Example 4); library cross-references corrected (C1 R12 wording, A2 P10, C3 §5, C3 L14, A1 §11, D4 Recipe 4, B5 wording in Examples 3 and 6); the "no guide covers stillness" claim narrowed (Wan prints one stillness phrase); rule 9 given an exception for sc13 B12; new rules 23-24 (Ray3.2, several faces) and a recording file-format step (5.3).

---

## 0. Words this file uses

- **Performance**: what a character's body, face, eyes and breath do in a shot. Voice delivery belongs to D3.
- **Tactic**: what a character tries to do to someone, as one "-ing" verb. It is A2's *tactic* and A1's *action*. A3 writes it as an infinitive ("to press"); convert by dropping "to" and adding "-ing".
- **Task**: the physical job the hands or body are doing (A3's `physical_task`, A1's *activity*).
- **Behaviour**: something a camera can see or a microphone can hear. A **behaviour step** is one timed behaviour, written `start-end: what happens`, in seconds from the start of the clip. The field keeps A2's spelling, `behavior`.
- **Eyeline target**: the person or thing the eyes rest on, plus the frame direction (A2's `eyeline`) and the **dwell** (how long they stay).
- **Display level**: how much inner pressure reaches the body, from 1 to 3. The brief called this "intensity 1-3". It is renamed because A2 already uses *intensity* (1-5) for how much pressure a beat carries in the story. The two often run opposite ways: a beat at A2 intensity 5 often plays best at display level 1.
- **Must-not**: behaviours that would break the beat. They are used to review takes and to fill negative fields. They are never written into a prompt as "no X" (C3 L14).
- **Performance state**: what a character carries into and out of a shot: breath, display level, eyeline, hands, posture, and wet or dry eyes. A **state ledger** lists these states shot by shot.
- **Driving clip**: a short video of a real person acting a moment. **Performance transfer** copies its movement onto a character image or video (C1's term). **Face capture** uses only the face; **body capture** also uses the body and hands.

---

## 1. Core principles

1. **Play the tactic, show the behaviour, never name the feeling.** Every maker guide checked says this (4.1). FilmBench (July 2026) found "the performance group is uniformly the lowest-scoring L2 cluster in both tasks" across the models it tested; action performance averaged only 50.8 (text-to-video) and 46.8 (reference-to-video) out of 100 [V, arxiv.org/html/2607.24241].
2. **Order is the performance.** At a turning point the face moves before the line (A2 Step 8), so write timed steps, not adjectives.
3. **Less display, more time.** The camera magnifies (A1 P10). Pressure reads from how long a face holds one thought, and that time is filled with small timed actions: a breath, a blink, a swallow, a glance.
4. **Held time must be written as small timed actions, or the model fills it** with nods, drift or speech, or squeezes it out; a list of still parts freezes the face instead [J; rewritten 10 October 2026, see rule 6].
5. **Eyes carry thought; hands carry the unsaid** (A1, B5). This file adds a dwell to every eyeline, and a start and end state to every hand.
6. **Breath is the cheapest continuous signal.** It shows in shoulders, chest, nostrils, a fogged visor and sound, and it crosses cuts.
7. **A clip has no memory.** Continuity must be written into each clip's first sentence and start frame, or the face resets to a pleasant neutral [J].
8. **Where timing matters more than words can hold, act it and transfer it.** C1 R12: "you control the timing of a look far better than a prompt can".

---

## 2. The merged performance block

### 2.1 Fields

| Field | Level | Meaning | Merged from | Allowed values |
|---|---|---|---|---|
| `character` | shot | Who acts | A2 `people` | B5 name |
| `tactic` | shot | Action on someone, one gerund | A1 `action`, A2 `tactics`, A3 `playable_actions_by_beat` | transitive gerund; reactions may be intransitive ("absorbing"); `(task only)` |
| `task` | shot | What hands or body physically do | A1 `activity`, A3 `physical_task` | verb phrase or `stillness` |
| `behavior` | shot | Timed visible steps | A2 `behavior` (now a list), A2 `five_steps`, C3 `beats` | `t0-t1: behaviour`; ≤1 main action per 4-5 s (C3 §5) |
| `eyeline` | shot | Target, direction, dwell, next target | A2 `eyeline`, A1 R39-R44 | `{target, frame: frame-left \| frame-right \| lens \| down \| up \| at OBJECT \| off-screen, dwell_s, then}` |
| `breath` | shot | State, how it shows, when it changes | new (C3 §6 lists breath) | `{state, visible_as, change_at}`; states in 2.3 |
| `stillness` | shot | Parts that do not move | B5 "what never moves" | `head, eyes, mouth, hands, torso, feet, whole_body, none` |
| `display_level` | shot | How much shows | new | `1` contained, `2` visible, `3` open |
| `must_not` | shot | What would break the beat | new | short phrases |
| `expression_ref`, `effort` | shot | Links to B5 | B5 `expression_state`, `effort` | "B5 IONA (3)"; `home \| stress \| break` |
| `state_in`, `state_out` | shot | State carried in and out | new | `{breath, display_level, eyeline, hands, posture, eyes_wet}` |
| `capture` | shot | How the performance is made | C1 Rec7, C4 Rec7, B5 R22 | `prompt \| still_then_i2v \| transfer_face \| transfer_body \| previs \| flip_still` |
| `driving_clip`, `voice_ref` | shot | Clip file; D3 delivery ID | new; D3 | file or `none`; e.g. `VOICE-IONA.D02` |
| `default_display_level`, `tells` | character | Usual level; small repeated giveaways | B5 movement signature | 1-3; exact line + behaviour |
| `through_line` | scene/sequence | The state ledger for one character | new | table (6.1) |
| `performance_prompt`, `performance_check` | generation job | Behaviour sentences for one model; take review | new | text; PASS/FAIL per item |
| `vocab_test_log` | film | Vocabulary test results (4.4) | new | phrase, model, date, takes, followed 0-3 |

### 2.2 Display level

| Level | What shows | Use |
|---|---|---|
| 1 contained | One or two small movements (eyes, a stopped hand, one breath), with breath and blinks going on (rewritten 10 October 2026; errata 23) | Most turning-point reactions; guarded or powerful characters; close-ups |
| 2 visible | Two or three movements nobody can miss (a step back, a head turn with the eyes following) | Medium shots; physical stress |
| 3 open | Whole-body, audible, maybe tears or a raised voice | Only where the script is loud ("She swings the cylinder with both hands."), or in wides |

The closer the shot, the lower the level [J]. Level 3 in a close-up reads as melodrama (A1 P10, "Understate on screen"; A1 R36 on melodrama).

### 2.3 Breath states

| Value | Looks and sounds like | Prompt wording [J] |
|---|---|---|
| `normal` | unnoticed | (nothing) |
| `one_breath` | one slow visible breath | "her shoulders rise once with one slow breath" (C3 §6) |
| `controlled` | through the nose, steady, no heaving | "she breathes slowly through her nose; her shoulders stay level" |
| `held` | chest and shoulders stop; about 3 s maximum on screen | "her shoulders and chest go completely still" |
| `catch` | short sharp in-breath | "a short, sharp breath in through parted lips" |
| `release` | long out-breath; shoulders drop | "she lets out one long breath; her shoulders drop" |
| `shallow_fast` | quick upper-chest breathing | "quick, shallow breaths" |
| `voiced` | breath heard as the line ("Nothing but breath.") | a D3 breath file, not a prompt |
| `not_visible` | helmet, back view, wide | sound only |

### 2.4 Template

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

Write `none` rather than deleting a field (C3's convention).

---

## 3. Decision rules

"Then" is firm. "Then consider" is a default, and breaking it needs a one-line reason in `notes` (A2/A3 convention).

**Writing the block**
1. If a script line names an emotion ("Her face changes.", "not steady"), then write two or three timed behaviour steps and keep the word only in `notes` and in the voice delivery, because every maker guide asks for visible cues (4.1) and A3 R2 bans emotion adjectives.
2. If a beat is a turning point or has A2 intensity 4 or more, then write A2's five steps as timed steps (desire as eyeline; antagonism as what is seen; choice as a held half-second; action; expression), because the choice needs its own screen time (A2 P10 and Step 8: "give step 2 (seeing the obstacle) and step 3 (choosing) their own screen time").
3. If the line, eyeline or cut already carries the beat, then use display level 1: one small action, with breath and blinks going on, because B5's restraint rule saves bigger faces for turning points. (Rewritten 10 October 2026: until then this rule asked for display level 1 with the word "still" or one movement, and models read "still" as an order to freeze: rule 6; library/02 Errata, entry 23.)
4. If a character is alone or acts only on objects, then fill `task` and write `tactic: (task only)`, because only an attempt on a person can be played (A3 §3.2).
5. If a behaviour step is shorter than about 0.5 s, then lengthen it or plan a transfer, because B5 puts micro-expressions at "a quarter to half a second", only 6-12 frames at 24 fps [J].

**Stillness, silence, eyelines**
6. If a hold is 2 s or longer, then write at least one small timed action for every 2 s of it (a breath, a blink, a swallow, a glance, a hand that adjusts something; `hold_action_every_s`), and give the camera one plain sentence, never a list of what does not move, because models read a list of still parts as an order to freeze: testers found that a strong "do not move" line spreads over the whole shot, so parts that should move stop and a face looks like a photo with moving lips; and time with nothing happening in it is squeezed out or frozen [J; the h3-storyboard testing notes, checked 10 October 2026; Project notes 42 and 43]. (Rewritten 10 October 2026; until then this rule asked for every still part and "The camera does not move.": library/02 Errata, entry 23.)
7. If lips part in silence ("She opens her mouth. Nothing in it."), then add "No dialogue." and "closes it without a sound", because parted lips invite generated speech on native-audio models [J; C3 L14 allows "No dialogue", and Wan's guide says it stops speech (C3 §7A)].
8. If pauses compete for long holds, then apply A1 R15 (at most two long holds per scene) before filling a hold over 3 s with timed actions (rule 6).
9. If an eyeline change is itself a beat (sc13 B14 "Now he looks at her."), then put that look in `must_not` for every earlier shot in the scene, because one early glance spends the beat. If the script itself gives an earlier look (sc13 B12: "He watches her look at it.", her palm), then aim the earlier look at a different target (her palm, not her eyes) and put "meets her eyes" in its `must_not`, so B14's look into her face is still the first.
10. If the eyes move, then name the target and the dwell ("to the flask; stays 2 s"), never "looks around", and for separately generated singles write opposite frame directions and "does not look into the camera" (A2 R26; A1 R44).

**Continuity**
11. If a shot continues the previous one (CONTINUOUS, same scene, or split for length), then copy the previous `state_out` into `state_in` and make it the prompt's first sentence; if the camera does not cut away, then also use the last frame as the start frame (C3 §11), because each clip starts blank.
12. If a state must change, then change it inside a behaviour step, never at a clip boundary, because a change at a cut reads as an error [J].
13. If breath is not visible (helmet, back, wide), then carry it in sound (D3 breath files), because the audience hears breath before it sees it.

**Capture route**
14. If a key shot's meaning depends on the timing of a look, a swallow or a breath, then consider `transfer_face` (C1 R12).
15. If hands, posture or distance carry the beat, then use `transfer_body` or `previs`; if only the face does, then use `transfer_face`, because body capture adds hand errors for no gain [J].
16. If the character is not human-shaped, then use `previs` (C4 Level 2-3) or Wan-Animate-2, because Kling's driving clip "Should contain a realistic style character with entire body or upper body visible" and must match the character image's full-body or half-body framing [V fal; V Kling guide], while Wan-Animate-2's own model card animates a kitten [V].
17. If a prompt-route take fails the same must-not twice, then change the capture route, not the wording (C3 Recipe 3 moves the shot to another route after two failed fixes).
18. If `capture` is a transfer, then give the tool no movement words: Runway Act-Two has no text prompt at all [V API schema]; Kling Motion Control's prompt is optional [V fal]; Wan-Animate-2 wants a prompt describing appearance and background [V model card]. Where a text box exists, send identity key, state line, look and setting only, because the driving clip carries the movement and movement words would compete [J].

**Sides and models**
19. If a one-sided expression's side matters, then never ask for the side in words. Flip an approved still (B5 Ex2), and run the mirror test (Example 3) before any transfer, because models place sides at random (B5 §14).
20. If the performer can only make the expression on the wrong side, then flip the driving clip before upload, never the output, because flipping the output flips the set and its text [J].
21. If a prompt-only shot is performance-led, then start with the model FilmBench ranks highest on performance (Seedance 2.0's category wins are "concentrated on ... performance (action and emotional performance)—in both tasks") or its successor, because it is the best evidence available. FilmBench tested Seedance 2.0, HappyHorse 1.0/1.1, Kling 3.0 and 3.0 Omni, Veo 3.1, Grok Imagine Video, Vidu and Hailuo 2.3; it did not test Seedance 2.5, Wan, LTX, Sora 2 or any transfer tool [V; J].
22. If the model's own guide pairs labels with cues (Kling, Wan), then one mood word may follow the behaviours, never replace them [V guides; J].
23. If the shot's framing, camera move and blocking can be acted for real in a room, and the look can be changed afterwards, then consider Luma Ray3.2 Modify Video with Face on (or Face only for expression), because it transforms the recorded clip itself ("Your original movement, timing, and intent become the instruction") [V Luma]; it makes no sound, so the voice comes from D3 (C3 rule 22). Luma warns that Face "pays less attention to the center of the forehead and the upper cheeks", so a brow-only or cheek-only beat (sc10's drawn brows, sc28's unraised cheeks) needs Structure high (Luma suggests 8) or another route [V].
24. If two or more faces must act in the same frame and their timing against each other matters, then act them together and use Ray3.2 (it tracks "up to eight faces simultaneously") or act each alone and composite; never ask Act-Two or Kling to drive two people from one clip, because Kling uses only "the character occupying the largest portion of the frame" [V Luma; V Kling].

---

## 4. A vocabulary of visible behaviours

### 4.1 What the makers print (all [V], checked 2026-09-27)

| Model | Guidance | A phrase from the maker's own guide |
|---|---|---|
| LTX-2 (ltx.io/blog/prompting-guide-for-ltx-2) | "Avoid emotional labels like 'sad' or 'confused' without describing visual cues. Use posture, gesture, and facial expression instead." Claims to excel at "single-subject emotional expressions, subtle gestures, and facial nuance" | "The man exhales, slightly annoyed" |
| Seedance 2.5 (Luma guide) | "You are converting an internal emotion into something visible." | "His jaw tightens. He takes one slow breath through his nose. His right hand closes into a fist while he keeps his eyes fixed on the other man." |
| MiniMax H3 (Luma guide) | "describe physical changes rather than abstract intentions" | "She tightens her grip on the letter and looks away" |
| Kling VIDEO 3.0 | Labels paired with physical detail | "chest heaving, expression dazed and helpless, fear glinting in their eyes"; "Sobbing, the protagonist strokes the dinosaur gently and trembles" |
| Wan 3.0/2.7 (Alibaba, updated 24 Sep 2026) | Emotion section using labels plus cues | "her smile gradually widens, her eyes crinkle"; "his hands rest lightly on the table, unmoving"; "her eyes glistening with tears, showing loss and helplessness" |
| Veo 3.1 (Google blog, 16 Oct 2025) | Little on acting | "rubbing his temples in exhaustion"; "A slight, mysterious smile plays on her lips" |
| Sora 2 (OpenAI cookbook) | "Actions work best when described in beats or counts – small steps, gestures, or pauses" | "Actor takes four steps to the window, pauses, and pulls the curtain in the final second." |
| LTX-2 (second example, same guide) | Freeze, then a behaviour | "The guilty frog freezes, then lowers its head in visible shame" |

What these guides show [J]:
- All the makers agree: visible cues first.
- Kling and Wan tolerate a label next to cues.
- Seedance's guide is the most specific about breath and hands ("Her shoulders tighten. She pauses before reaching for the handle.").
- Only Wan prints a stillness phrase, and only for hands ("unmoving"); LTX prints one "freezes". No guide covers whole-body stillness held for seconds, one-sided expressions or breath-holding, so those rows are the riskiest.

### 4.2 The vocabulary

**Status: untested.** No generations were run for this file. "Notes" gives the evidence that exists. Section 4.4 is the test that turns a row into "tested".

| Script word | Primary behaviour (keep if short) | Secondary | Timing | Notes |
|---|---|---|---|---|
| shock | "stops moving completely; eyes fix on {target}" | `held`; hands stop mid-task | hold 1.5-3 s | Whole-body stops are gross motion, the likeliest to work; stillness drifts after ~2 s [J] |
| recognition | "eyes fix on {target}; brows draw together slightly" | task stops, resumes slower | 0.5 s delay, 1-2 s | B5 Iona (2) |
| confusion / wrongness | "eyes lose focus and drift down" | repeats the task once, slowly | 2-3 s | The repeated task is the reliable part [J] |
| fear (contained) | "eyes widen slightly, stay on {target}; she backs one step" | `catch` then `held`; hand closes on an object | 1-2 s | Seedance-guide pattern [V]; widened eyes are often overplayed [J] |
| dread | "shoulders rise and stay high; head still" | `controlled`; one hand grips {object} | sustained | "Her shoulders tighten" appears in the Seedance guide [V] |
| hurt | "inner brows lift slightly; eyes drop to {object}" | `release`; mouth corners pull down slightly | 1-2 s | B5 §3.3; brow detail is often averaged away [J]; Ray3.2's Face transfer also under-weights the forehead [V Luma] |
| grief held back | "jaw tightens; eyes stay on {target}; one slow blink" | `controlled`; hands still | 2-4 s | Wan prints "eyes glistening with tears" and Kling "Sobbing ... trembles" next to grief [V]; list "tears" in `must_not` if unwanted |
| anger (suppressed) | "jaw tightens; one slow breath through the nose; eyes fixed" | one hand closes | 1-3 s | Near-verbatim Seedance example [V] |
| withholding | "eyes go to {object}, not to {person}; does not answer" | hand moves the object out of view | 1-3 s | A1's "looks at the flask, not at her"; H3's "looks away" [V] |
| shame | "eyes drop to the floor; head lowers a little" | hands find a task | 2 s | LTX's guide prints "freezes, then lowers its head in visible shame" [V]; watch for an added head shake [J] |
| relief | "shoulders drop; one long breath out" | hand opens | 1-2 s | Visible in medium shots [J] |
| decision | "still, then one small nod" or "eyes go to {goal}, then she moves" | `held` → `release` on the move | 0.5 s hold first | A2 five steps |
| listening | "eyes on the speaker; still; blinks naturally" | `controlled` | clip length | "she listens; no dialogue" (A1 §11) |
| outwaiting | "does not move or speak; eyes stay on {target}" | hands still | 2-4 s | Stillness plus silence: the hardest row; transfer is safer [J] |
| trying to smile | "one corner of the mouth lifts; cheeks do not rise; eyes stay flat" | small in-breath | 1-2 s | One-sided smiles become full, and the side is random (B5 §14); see Example 3 |
| speechless | "opens her mouth, holds it open, closes it without a sound; eyes drop" | `held` | 2-3 s | C3 §6; add "No dialogue." (rule 7) |
| exhaustion | "eyes close for a second; head rests against {surface}" | slow `release` | 2-3 s | Veo guide's "rubbing his temples in exhaustion" [V] |
| tenderness | "hand rests flat on {surface/person}, still" | `controlled` | 2-4 s | Hand contact often fails (C3 §13C) |

Two words are deliberately missing. *Disgust* is a trap in *The Catch* (Example 1). *Anguish* has no single behaviour, so split it into rows above.

### 4.3 Phrasing rules [J]
- Primary behaviour first. One sentence per step, joined by "then" (C3 §5 and rule 15). Timecodes only where the model supports them (C3 §5 timing syntax).
- Name body parts ("her lower lip", "his left thumb"), not faces.
- For a hold, say what happens in it and when: "For three seconds her eyes stay on him; she breathes in through her nose; at about two seconds she blinks." Never a list of what does not move (rule 6, rewritten 10 October 2026).
- Tone words go in the voice line only (C3 §6).

### 4.4 Recipe V: test the vocabulary
About $3-6 and 20 minutes per row on cheap routes (C3 §17A).
1. Make one neutral still of a test character in a plain room, medium close-up (C2).
2. Ask the LLM: "Write a 5 s image-to-video prompt for this still using only row [n] of D15 §4.2. Static camera. No dialogue. No background music."
3. Make three takes on each of two models.
4. Mark each take yes or no: primary behaviour present and in order? Stillness held? Anything from the must-not list?
5. Log the result in `vocab_test_log`. Two or more takes out of three following it means "tested: works on {model}". Zero or one on both models means use a transfer.
6. Test the riskiest rows first: outwaiting, trying to smile, speechless, shock.

---

## 5. Recording a driving clip (for someone who has never acted)

### 5.1 The tools (checked 2026-09-27)

| Tool | Driving clip rules | Controls | Cost | Label |
|---|---|---|---|---|
| **Runway Act-Two** (API `/v1/character_performance`, model `act_two`) | "The video must be between 3 and 30 seconds in duration."; the character image or video needs "A visually recognizable face" that "must be visible and stay within the frame". A character *image* keeps its "original static environment"; a character *video* keeps its "original animated environment and some of the character's own movements" | **No text prompt.** `expressionIntensity` 1-5, default 3; `bodyControl` applies "non-facial movements and gestures"; six ratios (1280:720, 720:1280, 960:960, 1104:832, 832:1104, 1584:672); seed | 5 credits/s at $0.01 = $0.05/s | [V] docs.dev.runwayml.com/api; /guides/pricing |
| **Kling Motion Control** 2.6/3.0 | 3-30 s (2.6 and 3.0); "Avoid cuts, shot changes, or camera movements"; "Avoid overly fast motions"; one person (with two or more, "the character occupying the largest portion of the frame will be used"); "entire body and head are clearly visible and not obstructed"; "a wide range of motion, moderate speed, and minimal displacement"; match full-body with full-body, half-body with half-body. fal adds: the driving clip "Should contain a realistic style character"; the character in the image should "occupy more than 5% of the image area". 2.6: short edge ≥340 px, long edge ≤3850 px | `character_orientation`: `image` (≤10 s, camera moves) or `video` (≤30 s, complex motion); `keep_original_sound` default true; optional prompt; one face element, only in `video` orientation. Kling's 3.0 guide asks for element photos matching the angles and expressions in the clip: "A front-facing view, side views" for head turns; "A neutral front-facing image, a smiling front-facing image" for expressions | fal v3 Pro $0.168/s; Atlas Cloud $0.071 (Standard) - $0.095 (Pro)/s | [V] kling.ai guide; fal API page |
| Kling, community reports | 2-5 s "optimal"; hands crossing the body give "spaghetti limbs"; face drift is the commonest failure; a neutral driving face keeps identity; "significant head rotation" worsens face consistency | — | — | [U] Atlas Cloud blog (14 Jul 2026) |
| **Luma Ray3.2 Modify Video** | Transforms the recorded clip itself (output = same length, up to 20 s, 1080p); the model tracks "the full expressive state for up to eight faces simultaneously, frame by frame", keeping "skeletal posture and gestures"; Ray3.2 released 9 June 2026. Face "pays less attention to the center of the forehead and the upper cheeks" | Up to 64 keyframes at chosen source frames (the text-to-video side takes up to 16 per clip); Motion and Structure each Off or 1-9; Bodies and Poses on/off (Poses follows every limb; Blocking only the broad movement); Face on/off, and "Face by itself" drives only the expression. No native audio | credits (C1) | [V] lumalabs.ai/news/introducing-ray-3-2; lumalabs.ai/learning-center/articles/ray-3-2-video-to-video |
| **Wan-Animate-2** (open) | Transfers body motion and expression from a driving video to a reference image; the model card animates a kitten, so non-humans work; Apache 2.0; 7 Aug 2026 | Text prompt describing appearance and background | free weights; "8× A800 GPUs" for 720p (480p tested on 2), so cloud only | [V] huggingface.co/Wan-AI/Wan2.2-Animate-2-14B |

**Correction to C1:** its Recipe 7 says "Kling driving clip 2–5 s", but Kling's guide and Runway's API both set a 3 s minimum. Record 3-5 s per beat [V].

### 5.2 Face capture or body capture?

| Shot | Capture | Tool | Record |
|---|---|---|---|
| Close-up where eyes, mouth or breath carry the beat | face | Act-Two, `bodyControl` off; Ray3.2 with Face on (or Face only) | head and shoulders |
| Medium shot where hands or shoulders carry it | face + upper body | Act-Two, `bodyControl` on; Kling `video` | waist up, hands clear of torso |
| Full-figure move | whole body | Kling; C4 Rec7 (Rokoko/DeepMotion into Blender) | head to feet, margin, locked camera |
| Two people touching | each alone, or previs | C4 (DeepMotion/QuickMagic for two) | separate clips, composite |
| Non-human body | previs or Wan-Animate-2 | C4 Level 2-3 | — |

### 5.3 Set-up (10 minutes, once)
1. **Phone**: on a tripod or books, at eye height, locked (Kling asks for no "camera movements" in the driving clip [V]). No beauty filter or portrait blur [J].
2. **File**: record at 1080p (not 4K), 24 or 30 frames per second, saved as a normal MP4 [J]. A 5 s 1080p phone clip is roughly 10 MB [J], under Runway's 32 MB limit for a linked video [V, Runway inputs page]; 1080p also sits inside Kling 2.6's size limits (short edge at least 340 px, long edge at most 3850 px) [V].
3. **Mirror check**: front-camera previews are often mirrored while saved files are not, depending on phone and setting [U]. Check the saved file.
4. **Light**: face a window or a soft lamp, with nothing bright behind you. Light both sides of the face evenly [J].
5. **Background**: a plain wall, with nobody else in frame (Kling uses the largest figure [V]).
6. **Clothes**: a plain top that contrasts with the wall, sleeves above the wrists, hair off the face, no glasses [J].
7. **Marks**: tape at eye height left and right of the phone where the other characters "stand". This gives `eyeline.frame` without looking into the lens (A1 R44).
8. **Props**: the real object from `task`. A3 calls a task "the most reliable way to give a figure believable motion".
9. **Hands**: keep them away from the front of the body, and never cross your arms. Kling asks that body and head be "clearly visible and not obstructed" [V]; the "spaghetti limbs" failure from crossed hands is a community report (Atlas Cloud, repeated in C4 §11) [U].
10. **Framing**: match the character image; never drive a half-body image with a full-body clip [V Kling].
11. **Consent**: if anyone else performs, get D4's one-page consent form signed before any upload (D4 Recipe 4 step 5; rules 7 and 9). If you perform yourself, record `self_consented` with the date (D4 rule 9). Keep driving clips private.

### 5.4 Acting sheet (the LLM prints it under each shot)
1. Hold the `state_in` pose for 0.5 s before you start and the `state_out` pose for 0.5 s at the end. These give clean trims [J].
2. Do the task for real: chew, hold, twist.
3. Say A1's `unsaid` line silently to the tape mark. A specific thought fills the eyes; "feeling sad" does not [J].
4. Count the step times under your breath or with a metronome app.
5. Breathe the breath state: actually stop breathing on `held`.
6. Play it smaller than feels right. Act-Two's `expressionIntensity` can raise the display later, but it cannot remove a grimace [J].
7. Keep your head still unless a step moves it. Sharp turns cause face drift in Kling [U].
8. Record three takes, at display levels 1, 2 and 3, and choose in review.
9. Speak the lines with sound on. One file then drives the face (Kling keeps the sound by default) and the voice through D3's speech-to-speech route, which "keeps your timing, breath and stress".

**Continuous takes.** When beats run on without a story cut, act them in one take and cut it at A2 beat boundaries to fit the tool (Act-Two ≤30 s; Kling ≤10 s `image`, ≤30 s `video`; Ray3.2 Modify ≤20 s) [V]. Each piece then inherits the last one's breath and energy. Every piece must still be at least 3 s long for Act-Two and Kling [V].

**Review a transfer.** Check in this order:
1. Eyeline direction.
2. Timing: the key behaviour lands within about 0.25 s of the driving clip [J].
3. Hands.
4. Identity against the hero portrait (B5). For face drift, use more references or Kling's face element [V fal].
5. Display level. If it is too strong, set `expressionIntensity` to 2 [J].
6. Sides.
7. The must-not list.

If a take fails, re-perform once with the fix; if it fails again, change route (rule 17).

---

## 6. Continuity of performance across separate clips

### 6.1 State ledger
One row per shot, per character, for any run of shots without a time jump:
- `shot_id`
- `breath`, `display_level`, `eyeline`, `hands` (with sides), `posture`, `eyes_wet` at the end of the shot
- `carried_by`: start frame, first prompt sentence, driving take, or sound

### 6.2 Recipe C: carry-over
1. Export the last frame of shot N's kept take (C3 Recipe 4). In any editor, or with the free tool `ffmpeg`: `ffmpeg -sseof -1 -i shotN.mp4 -update 1 -q:v 1 shotN_last.png` [tested 2026-09-28, ffmpeg 7.0.2].
2. Copy N's `state_out` into N+1's `state_in`.
3. Same view: use the frame as N+1's start frame. New angle: use it as a pose reference and open the prompt with the state ("She is still kneeling, not breathing, eyes on the bracket.").
4. If the model opens N+1 with a settling movement or a fresh face, trim it. The 0.5 s heads and tails (5.4) exist for this.
5. Lay continuous breath sound across the cut (D3).

### 6.3 Energy across cuts [J]
- Energy never drops at a cut by itself; it falls inside a step.
- Match the breath phase across a cut: out-breath into out-breath.
- Wet eyes, sweat and a clenched jaw are continuity items, like a bandage. Log them, and put them in B5's state line if they last beyond one shot.
- A through-line can span the film. Iona's breath goes "One breath." (sc01), "She goes still." (sc02), "Breath in the helmet." (sc27), "She tries to answer. Nothing but breath." (sc28): from breath controlled to breath as her only voice (Example 5).

---

## 7. Recipes

**Recipe P: fill the blocks for a scene** ($0, about 20 min)
1. Paste the scene text, its A2 beat table, its A1 labels, the relevant B5 entries and D15 sections 2-4.
2. Say: "Fill a D15 performance block for every acting character in every shot of scene [ID]. Quote the line each block serves. Use only §4.2 behaviours or behaviours the script gives; mark others [design choice]. Set state_in from the previous state_out."
3. Read only `tactic`, the first step and `must_not`. Correct in plain words ("She is confused here, not angry").
4. Say: "List every hold of 2 s or more and check it against A1's pause ranking."

**Recipe W: performance into a prompt** ($0). Say: "Using this D15 block and C3 §16, write the [model] behaviour sentences. Primary behaviour first; tone words only in the dialogue line; turn every must_not into a positive stillness sentence or a negative-field noun." Paste the result under BEATS in C3's master prompt and run C3's linter.

**Recipe T: act and transfer one shot** ($1-5, about 40 min the first time)
1. Say: "Print the D15 §5.4 acting sheet for shot [ID], with the behaviour times as counts."
2. Set up (5.3). Record three takes of the beat plus 0.5 s heads and tails. The trimmed clip must still be at least 3 s long (Act-Two and Kling minimum [V]); if the beat is shorter, keep more of the held `state_in` pose.
3. Trim in any editor, or with `ffmpeg -ss 0.5 -i take1.mp4 -t 4 -c:v libx264 -pix_fmt yuv420p -c:a aac take1_trim.mp4` (start 0.5 s in, keep 4 s). Flip the clip if a one-sided expression landed on the wrong side (rule 20): `ffmpeg -i take1_trim.mp4 -vf hflip -c:a copy take1_flip.mp4`. Both commands [tested 2026-09-28, ffmpeg 7.0.2].
4. Upload the take with the approved character still. Use the flipped still for a MIRRORED era. Act-Two has no text box; in Kling or Wan, put identity, look and setting only in the text, no movement words (rule 18).
5. Settings: Act-Two `expressionIntensity` 2 for display level 1, otherwise 3 [J]; `bodyControl` per 5.2. Kling: `image` orientation for up to 10 s, or `video` orientation with a face element. Ray3.2 Modify: Face on, Structure high for a real-looking face (Luma suggests 8), Poses on only if the body moves [V Luma; J].
6. Review (5.4). Log the result in `performance_check`.

---

## 8. Checklists

**Per shot:**
1. A block for every acting character.
2. Tactic is a gerund; task is physical.
3. No emotion words in `behavior`.
4. Steps timed, at most one main action per 4-5 s.
5. Eyeline has a target, a direction and a dwell.
6. Breath state set.
7. Every hold of 2 s or more filled with small timed actions, one at least every 2 s (rule 6).
8. Display level fits the shot size.
9. Must-not list filled, and none of it written as "no X" in the prompt.
10. `state_in` = the previous `state_out`.
11. Capture route chosen, with a reason if it is a key shot.
12. D3 delivery matches the breath.
13. Transfer shots: no movement words in any text box; Act-Two gets none at all (rule 18).

**Per scene:**
1. At most two long holds, per A1's ranking.
2. Beat-eyelines protected in earlier shots (rule 9).
3. One display peak, at or after the main turn.
4. No unexplained jumps in the ledger.
5. Tells and signature gestures within B5's once-per-scene limit.

**Per take:**
1. Primary behaviour present, in order.
2. Each person moves between the written actions (breath, eyes, small shifts), and nothing freezes.
3. No must-not items.
4. Eyeline and sides correct.
5. Nobody speaks who should not.
6. No face reset at the start.
7. Hands intact.

---

## 9. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Generic "sad" or "shocked" face | Emotion word in prompt | §4.2 behaviours (rule 1) |
| Nodding or swaying in a hold, or a frozen face with moving lips | Held time left empty, or written as a list of still parts | Small timed actions, one at least every 2 s; one camera sentence; shorter clip; transfer (rule 6, rewritten) |
| Parted lips produce a word | Native audio reads lips as speech | "No dialogue."; "without a sound" (rule 7) |
| Half-smile turns full, or lands on the wrong side | Models average and randomise sides | Flip an approved still; transfer at intensity 2; mirror test (Example 3) |
| Unwanted tears | Grief words; Wan's guide pairs "eyes glistening with tears" and Kling's "Sobbing" with grief [V] | Remove grief words; "tears" in the negative field |
| Fresh relaxed face at clip start | No memory | `state_in` first sentence; previous last frame; trim the head (6.2) |
| Energy jump at a cut | Breath phase or level mismatch | Match phase; carry breath in sound (6.3) |
| "Spaghetti limbs" in a transfer | Hands crossed the body [U: Atlas Cloud community report, repeated in C4 §11] | Re-perform with hands clear of the torso |
| Face drifts in a transfer | Head turns; big face; one reference [U] | Frontal, smaller; more references or face element with front and side photos [V Kling 3.0 guide] |
| Wrong scale or limbs in a transfer | Framing mismatch (full body driving half body) [V Kling]; body-shape mismatch [J] | Match framing and build; previs for the figure |
| Machine body moves like a person in a suit | Human weight shifts, head bob | Previs stand-in; see Example 4 |

---

## 10. Worked examples

### Example 1. sc10 B7: recognising the mint (A2 five steps; B5 Iona expression 3)

> SAYE: "Chew that." / "Iona chews it." / "Her face changes." / SAYE: "What does it taste of?" / IONA: "(not steady)" "Not mint."

**Reconcile first.** Three files describe this face, and they disagree:
- **B5 Iona (3):** "chewing stops, upper lip lifts slightly, brows draw together".
- **A2:** "she stops chewing, frowns, chews once more, slowly", and "recognition and confusion, not disgust".
- **C3 §6:** "Her eyes lose focus and drift down; her lips part slightly; she holds very still."

A raised upper lip is the classic disgust movement. A2's chemistry says mirrored mint tastes of caraway: familiar but wrong. So this file drops the lip and keeps A2's check-chew and C3's unfocused eyes. That is a requested change to B5 (3) [J].

Shot B7.b is a close-up, the scene's tightest, held from the first chew through "Not mint." (A2).

```yaml
performance:
  - character: IONA
    tactic: discovering
    task: "chews the mint leaf"
    display_level: 1
    behavior:
      - "0.0-0.5: holds the leaf, eyes on Saye; a half-second before it goes in"        # choice
      - "0.5-2.0: chews steadily, eyes still on Saye"                                   # action
      - "2.0-2.5: chewing slows and stops; jaw still, lips closed"
      - "2.5-3.5: brows draw together slightly; eyes lose focus, drift down to the table"
      - "3.5-4.5: chews once more, very slowly, as if checking"
      - "4.5-5.0: completely still"
      - "5.0-6.0: says 'Not mint.' quietly, on the out-breath"                           # expression after the face
    eyeline: {target: Saye, frame: frame-left, dwell_s: 2.5, then: "down, unfocused"}
    breath: {state: held, visible_as: "shoulders stop at 2.0", change_at: "5.0: release into the line"}
    stillness: [head, hands, torso]
    must_not: [upper lip raised, nose wrinkled, spitting, hand to mouth, tears, looking at Eli, a smile]
    expression_ref: "B5 IONA (3), revised"
    effort: stress
    state_in: {breath: normal, display_level: 1, eyeline: Saye, hands: "right hand lowered after the mirror test", posture: standing, eyes_wet: no}
    state_out: {breath: release, display_level: 1, eyeline: "down", hands: still, posture: standing, eyes_wet: no}
    capture: transfer_face
    driving_clip: IONA_sc10_B7_take?.mp4
    voice_ref: "VOICE-IONA.D02 (cracked; D3 lists it for SC10 and SC13)"
```

**Why transfer.** This is the first act's key performance, and its meaning is the order: face first, then line. A prompt cannot hold that timing (C1 R12). Use Act-Two first: the beat lives in the brows and the stopped jaw, and Luma warns its Face transfer under-weights "the center of the forehead" [V]. If Ray3.2 is used, set Structure high (8) and check the brows first in review.

**Acting tip [J].** Chew a few caraway seeds wrapped in a real mint leaf. The surprise is genuine, and it is the right surprise: familiar but wrong. Record 6-7 s with sound; the same take can feed D3's voice route.

**Split continuity.** A2 notes that B7.b runs on through B8 (Saye's 14 words, about 6 s, plus a 2 s hold), which is too long for one clip. Split it at the beat boundary with matched framing:
- B8's `state_in` is B7's `state_out`.
- B8's tactic is *absorbing* (A2). Its step: "eyes stay down; at 'street signs either' they come up slowly to Saye and stay".
- One continuous driving take cut at that point gives both clips the same breath.

**Prompt fallback, withdrawn 10 October 2026** (library/02 Errata, entries 23 and 26: it writes the hold as parts that stay still, which models read as an order to freeze; write the hold as small timed actions instead, as rule 6 says and card 21 shows; the `stillness` list and the "completely still" step above are withdrawn with it) (Veo 3.1, image-to-video from the approved start still, colon speaker format per C3 §7A) [J]: "Close-up, static camera. The woman chews slowly, her eyes on the older woman off-screen at frame left. Her chewing slows, then stops; her head and hands stay completely still. Her brows draw together slightly and her eyes lose focus and drift down toward the table. Then she chews once more, very slowly, and holds still. A woman says quietly and unsteadily: Not mint. No background music."

### Example 2. sc13: the "Silence." hold (A1 pause ranking)

> ELI: "One body." / IONA: "One." / ELI: "You." / "Silence."

**Ranking.** The scene has at least ten marked pauses: "She waits.", "Silence.", three "(beat)"s, "Saye is looking at nothing.", "Nothing in it.", "Now he looks at her.", "Not at Jude.", and "Lets the recording run." Two readings compete:
- A1 takes "You." as the turn, so "She waits" and "Silence." rank first.
- A2's turns are B7, B12 and B15 (main), which favour "Nothing in it" and "I wasn't asking her."

**Proposal [J], for the user to confirm:**
- "Silence." gets a long hold of 3 s. R15's second test is change in audience knowledge, and nothing changes it more: the device was rated for Iona alone.
- The post-"I wasn't asking her." hold is the other long hold. A2 asks for "at least 2 s"; A1 R15 defines a long hold as "3 seconds or more", so use 3 s.
- "She waits" becomes a medium hold (about 2 s, uncut, on Eli).
- "Nothing in it" plays as A1's single focus-pull shot, not an empty hold.

**Shot** (A1): "Cut wide once, all three of them plus the monitor, to show the new distance. Then hold." The sound is room tone plus the monitor hum.

```yaml
performance:
  - character: IONA
    tactic: absorbing
    task: "(stillness) remote in hand, thumb off the button"
    display_level: 1
    behavior: ["0.0-3.0: completely still, eyes on Eli; one slow blink at about 2 s"]
    eyeline: {target: Eli, frame: frame-right, dwell_s: 3.0, then: none}
    breath: {state: held, visible_as: "shoulders still since 'You.'", change_at: none}
    stillness: [head, hands, mouth, torso]
    must_not: [gasp, hand to mouth, head shake, tears, speaking, looking at Jude]
  - character: ELI
    tactic: withholding
    task: "(stillness) facing the monitor"
    display_level: 1
    behavior: ["0.0-3.0: eyes on the monitor; jaw set; one slow breath out through the nose at about 1 s"]
    eyeline: {target: monitor, frame: "at monitor", dwell_s: 3.0, then: none}   # the monitor is in the wide, so not the lens
    breath: {state: release, visible_as: "shoulders settle once", change_at: "1.0"}
    stillness: [head, hands]
    must_not: [looking at Iona, speaking, a smile]   # protects B14 "Now he looks at her." (rule 9)
  - character: JUDE
    tactic: witnessing
    task: "(stillness) good hand resting on his lap"   # [design choice]: the script gives only "his good hand"
    display_level: 1
    behavior: ["0.0-3.0: eyes on Iona, not the screen; still"]   # B5 Jude (4)
    eyeline: {target: Iona, frame: frame-left, dwell_s: 3.0, then: none}
    breath: {state: controlled, visible_as: "not visible in the wide", change_at: none}
    stillness: [whole_body]
    must_not: [speaking, reaching for Iona]
```

**Generation [J].** Three people doing almost nothing in one wide is hard. Models fill time with motion (rule 6), and C3 rule 16 warns against more than three acting characters, so if Saye is in frame at all, keep her soft and small beyond the glass.

**Rule 9 in this scene.** Eli's must-not "looking at Iona" runs from B1 to B13, with one scripted exception: at B12 "He watches her look at it." Play that look at her palm, and add "meets her eyes" to that shot's `must_not`, so that B14 ("Now he looks at her.") is the first time his eyes meet hers.
- **Route:** image-to-video from the approved wide still, 4 s, trimmed to 3.
- **Prompt, withdrawn 10 October 2026** (library/02 Errata, entry 23: a list of what stays still and "The camera does not move." freeze the whole frame; write each person's small timed actions, a blink or a breath at least every 2 s, and one camera sentence, as rule 6 says; the "completely still" behaviour lines and `stillness` lists above are withdrawn with it): "Nobody speaks. The three people stay completely still for the whole shot; the only movements are one slow blink from the woman at frame left and one slow breath from the man at frame right. The camera does not move. No dialogue. No background music."
- **If two takes fail:** act the three parts yourself as three 4 s face takes, transfer each, and composite them in the edit (C3 post operations).

### Example 3. sc28: Eli's wrong-side smile (B5 Ex2), a transfer and mirror test

> "Eli has got to his feet. He lifts one hand and tries to smile." / "The familiar little smile, on the wrong side of his face."

**The design (B5).**
- The smile lifts Eli's own left corner, which shows at frame right in sc03 when he faces the camera.
- In era C he is MIRRORED, so the smile shows at frame left, and his parting flips with it.
- "Tries to smile" is weaker. B5 ELI (6): "one lip corner lifts, cheeks do not rise, on the wrong side". This file adds "eyes stay flat" [design choice], against sc03's "a slight cheek rise on that side, eyes softening" (B5 Ex2).
- In sc28 Eli wears the C5 "white paper oversuit" (B5 state line), not sc03's coat.
- sc20 has a third smile: "Eli gets to his feet when he sees her. Almost smiles." Eli is still NORMAL there (era B), so if any corner moves it is the sc03 side. Decide whether it moves at all; it should not steal sc28's payoff [J].

```yaml
performance:
  - character: ELI
    tactic: reassuring                 # aimed at Iona; the smile fails
    task: "lifts one hand"             # hand side: [design choice], own terms, converted per B5 §7.2 rule 5
    display_level: 1
    behavior:
      - "0.0-0.8: standing, weight just settled, eyes on Iona"
      - "0.8-1.8: lifts one hand to chest height, palm toward her"
      - "1.4-2.4: one mouth corner lifts (designed side, MIRRORED); cheeks do not rise; eyes stay flat"
      - "2.4-3.5: holds the half-smile and the hand"
    breath: {state: catch, visible_as: "small in-breath", change_at: "1.3"}
    stillness: [head, feet]
    must_not: [two-sided smile, teeth showing, cheeks raised, smile on the NORMAL side, looking into the camera]
    expression_ref: "B5 ELI (6)"
    capture: transfer_face             # bodyControl on if the hand is in frame
```

**Mirror test (once, before any sc28 shot; about $1-3) [J, method].** No maker says whether Act-Two, Kling or Ray3.2 keep a one-sided expression on the same side of the frame. This test finds out.
1. **Character image.** Flip the approved sc03 half-smile still, check the smile and parting are at frame left, edit the mouth to neutral, and edit the coat to the C5 paper oversuit (C2 image edit). If Kling's face element is used, flip its photos too; Kling's 3.0 guide asks for "a smiling front-facing image" among them, and an unflipped one would pull the smile back to the NORMAL side [V guide; J].
   - Act-Two keeps the character image's "original static environment" [V].
   - So place the flipped Eli on an *unflipped* receiving-room background by image edit (C2). Flipping the whole still would reverse "RECEIVING", which Iona reads in this scene.
2. **Driving clip (4 s).** Neutral for 1 s, then lift only the corner that is at frame left *in the saved file* (not the preview), hold, and relax. If your face will only lift the other corner, flip the clip (rule 20).
3. **Run.** Act-Two at `expressionIntensity` 2 with `bodyControl` off, and Kling in `video` orientation, one take each.
4. **Score each output:**
   - Smile at frame left?
   - One-sided?
   - Cheeks not raised?
   - Parting at frame left?
5. **Log and act on it.** Record the result in `vocab_test_log` as the first real test of the "trying to smile" row.
   - If a tool keeps sides, use it.
   - If it swaps them consistently, flip the driving clip and rerun.
   - If the smile goes symmetric, use `flip_still`: image-to-video from the flipped sc03 still with the smile already on the face, prompt "he lifts one hand slightly; his mouth keeps its shape; he does not smile wider".

Then cut the sc28 take next to the sc03 take. The payoff works only if the sc03 side was fixed, and this test protects it.

### Example 4. The figure: a machine worked by a small body (B5 §6.5)

> "Its hand goes under his wounded arm and lifts it clear of the mattress. As carefully as a nurse." (sc15) / "It catches the cup without looking." / "Then it moves, and it is fast." (sc23) / "One fine limb draws itself out of a socket in the wall of the vessel. Far above, the enormous black hand goes dead and hangs." (sc25)

**Direction.** The body must look "carried, not inhabited" (B5). It has no face, so display level applies to the hands and to where the head points.
- **Two tempos only.** Care is slow, sustained and direct (glide, press). Task is sudden, strong and direct (punch). Nothing in between, and no idling.
- **Arms lead, trunk follows a moment later** [design choice]. This is how a body driven from inside at the hands would move.
- **No human weight shifts.** No head bob on a step, no hip sway.
- **Hands settle late** (B5). Once, early, a hand sinks a few centimetres when the figure stops: the dead-weight clue.
- **The pale strip never tracks objects.** It keeps its steady cycle (B5); only the head points.

| Shot | Tactic | Behaviour | Must-not |
|---|---|---|---|
| sc15 lift | tending | "0-3: the huge hand slides under the arm slowly, lifts it straight up about 10 cm, stops; the hand settles a fraction late" | quick moves, head bob, strip following the arm |
| sc23 cup | (task only) | "0-1: head stays toward Iona's visor; the hand goes out sideways and closes on the sliding cup" | head turning to the cup |
| sc23 "fast" | (task only) | "one fast straight reach; full stop; next fast reach" | flowing, dance-like motion |
| sc25 hand on chest | offering | "0-2: lays one hand flat against its own chest, slowly; holds" (Iona's flat hand, B5 Ex1) | fingers moving, patting |

**Capture.** Kling wants a "realistic style character" in the driving clip and matched full-body or half-body framing [V]. A 2.4 m block with a sunken head fights a human driving clip, so:
- **First choice:** C4 previs, Level 2-3. Keyframe a tall block stand-in with the two tempos, then feed it as a depth-control video, or turn key poses into image-to-video.
- **Second choice:** Wan-Animate-2, which accepts non-humans [V], through a cloud service.
- **Third choice (untested):** Ray3.2 Modify Video on the previs render, Bodies and Poses on, Face off; Luma says Poses "carries every actual movement" [V], but nothing documents how it treats a non-human body [U].
- **If you act it for timing:** move only from the forearms, lock the trunk, keep the head level, and count the dead stops. Use the clip as a timing reference for previs, not as a direct transfer [J].
- **Untested prompt [J]:** "It moves in separate, complete motions with a full stop between each; its arms move first and its body follows a moment later; its head stays level; when it stops, one hand sinks slightly and hangs." Run Recipe V on it first.

### Example 5. Breath from "One breath." through the climb (sc01-sc02)

> "She stays on her knees. One breath." … "Her lips move around the torch: counting." … "She goes still." … "Her jaw shuts on the torch." / "She hangs." … "(through the torch) No." … "She climbs on. Now each foot goes only where a hand has already been." … "Rests her face against the brick."

Nobody can hold a breath for a whole climb, and nothing on screen should suggest it. What carries through is the held *quality*: breath under control, never heaving, breaking once at the rung [J]. A3 Ex1 already gives the first shot its task ("keeps her finger in the hole, breathes once, takes it out"). The ledger carries it on:

| Moment | Script | Breath at end | Display | Carried by |
|---|---|---|---|---|
| sc01 kneel | "One breath." | `one_breath` → `controlled` | 1 | next prompt's first sentence |
| sc01 lines | "The safety brakes are gone." | `controlled` | 1 | D3 delivery matches |
| sc02 climb | "Hand. Foot. Hand. Foot. … counting." | `controlled`, through the nose (torch in teeth) | 1 | the count sets rhythm; one continuous driving take |
| sc02 rung | "She goes still." | `held` | 1 → 2 | start frame from the climb's last frame |
| sc02 fall | "Her jaw shuts on the torch." / "She hangs." | `held`, jaw clamped | 2 | breath sound stops; one grunt through the torch [design choice] |
| sc02 radio | "(through the torch) No." | `release` through the nose → `controlled` | 2 → 1 | the line rides the release; a mouth-full line is D3 rule 3's case for speech-to-speech |
| sc02 climb on | "each foot goes only where a hand has already been" | `controlled`, slower | 1 | slower count |
| sc02 sill | "Rests her face against the brick." | `release`: one long breath out | 1 | its sound bridges to "Then up." |

**Must-not for the run:**
- Panting or mouth-breathing before the rung.
- Any sound of fear.
- Looking down after the fall. The script never says she does.

**Film-scale arc.** sc27 "Breath in the helmet." (`controlled`, audible) and sc28 "She tries to answer. Nothing but breath." (`voiced`) end the arc that sc01 starts. Plan all three together in D3's sound plan.

### Example 6. *The Long Places*: "two breaths entire" (prose)

> "Melek rose, laid the flat of her hand on the sounding stone, and knocked twice, softly, and then stood in the waiting, two breaths entire" (ch. V)
> "the hand went out and hung with its manners on, and nothing took it, and nothing refused it, and he repossessed it slowly, like a man who has offered his hand to weather. After a while — Yusuf said two breaths; Nilay, later, could not make it shorter than the length of a drummed finger — the elder on the far wall raised his own palm" (ch. VII)

**Prose gives durations in breaths.** A calm adult breath takes about 3-5 s: clinical sources give a resting rate of 12-20 breaths a minute (Cleveland Clinic: "12 to 18") [V], so "two breaths entire" is about 6-10 s. That agrees with B5 Ex5: "about two breaths (roughly six to eight seconds) of stillness, which the edit must hold".
- Melek's wait is a long hold (A1 R15 applies to prose too). Breath is `controlled` and visible: the shoulders rise and fall twice, and nothing else moves. (That last phrase is withdrawn, 10 October 2026, library/02 Errata, entry 23: in a prompt, write the hold as the two breaths and a blink or a glance between them, never as what does not move.)
- The knock-and-two-breaths is a **tell passed between characters**. Yusuf, Nilay and Márton all learn it, as Iona's flat hand passes to Jude and the figure. Log it once in `tells` and keep its timing each time it returns: the novel's point is who keeps "the two breaths entire".

**Márton's hand** [J]:
- `tactic: offering`.
- `behavior`: "0-1.5: steps forward, right hand out at handshake height; 1.5-5: the hand hangs, still, fingers open; 5-8: draws it back slowly to his side". ("The hand hangs, still" is withdrawn, 10 October 2026, library/02 Errata, entry 23: write "1.5-5: the hand hangs in the air, fingers open; his fingers curl a little; he breathes out" instead.)
- `must_not`: a fast drop; embarrassed gestures.
- Yusuf's "making the sounds of a man keeping his breathing voluntary" is `controlled` breath carried in sound (rule 13).

---

## 11. Conflicts and open questions

1. **Intensity names.** A2's `intensity` (1-5, story pressure) and `display_level` (1-3, what shows) are different fields. The brief said "intensity 1-3". Keep both, under different names.
2. **The mint face.** B5 (3), A2 and C3 disagree. This file drops B5's upper-lip lift; the user confirms.
3. **The sc13 turn.** A1 ("You.") and A2 (B7, B12, B15 main) change which pauses get long holds. The proposal in Example 2 needs the user's decision.
4. **Clip length.** C1 says 2-5 s, but the official minimum is 3 s [V].
5. **Kling trade-off.** A neutral driving face keeps identity [U], but expression is the point of a transfer. Lower the display and use a face element with front, side, neutral and (flipped where needed) smiling photos [V Kling 3.0 guide].
6. **Side handling in transfer tools** is unknown until the mirror test runs.
7. **Vocabulary status.** No §4.2 row has been generated. The vocabulary is maker-backed or judgment until Recipe V runs.
8. **Runway help pages** were blocked by a bot check. Limits come from Runway's API and pricing pages; third-party recording tips were not used as facts.
9. **Consent and awards.** D4 notes that for the 99th Oscars only roles "demonstrably performed by humans with their consent" are eligible for acting awards (Academy, 1 May 2026) [V]. Whether a performance transferred onto a generated face qualifies is D4's question.
10. **Verb form.** A3 uses infinitives, A2 and this file gerunds. Store gerunds.
11. **Kling Motion Control length in C4.** C4's tool table says Kling 3.0 Motion Control runs "up to 15 s"; fal's schema gives 10 s (`image`) and 30 s (`video`), and Kling's guide gives 3-30 s for the driving clip [V]. This file follows fal and Kling; C4 should be updated.
12. **Long-hold length.** A1 R15 defines a long hold as 3 s or more; A2 asks for "at least 2 s" after "I wasn't asking her." This file uses 3 s for every long hold.
13. **Eli's early look in sc13.** The script has Eli watch Iona's palm at B12 before B14's "Now he looks at her." Rule 9's exception (look at the palm, not her eyes) needs the user's confirmation.
14. **Act-Two has no prompt.** This file's first draft told the user to put look and setting "in the text" for Act-Two; its API has no text field. The advice holds for Kling and Wan-Animate [V].
15. **Luma keyframes.** C1 and C3 give Ray3.2 "up to 16 keyframes", which is right for generating a clip; Ray3.2 Modify Video (the performance route) takes up to 64 [V]. Both files are correct for what they describe; name the mode when citing.
16. **sc20 "Almost smiles."** Whether any corner moves there is a design decision for the user (Example 3).

---

## Sources

All checked 2026-09-27; the web sources were re-opened on 2026-09-28 in the fact-check pass.

- **Runway**
  - API reference, `/v1/character_performance` (3-30 s reference; face rule; `bodyControl`; `expressionIntensity` 1-5, default 3; ratios): https://docs.dev.runwayml.com/api/ [V]
  - Pricing (`act_two` 5 credits/s; $0.01 per credit): https://docs.dev.runwayml.com/guides/pricing/ [V]
  - Inputs (video by URL up to 32 MB; data URI 16 MB; upload 200 MB; MP4/H.264 accepted): https://docs.dev.runwayml.com/assets/inputs/ [V]
  - Help, "Performance Capture with Act-Two" (blocked; not used): https://help.runwayml.com/hc/en-us/articles/42311337895827 [U]
- **Kling**
  - Motion Control User Guide (durations, orientation, visibility, avoid cuts, camera moves and fast motion; face element): https://kling.ai/quickstart/motion-control-user-guide [V]
  - VIDEO 3.0 User Guide: https://kling.ai/quickstart/klingai-video-3-model-user-guide [V]
  - fal, Motion Control API schema (`image` ≤10 s, `video` ≤30 s; `keep_original_sound`; face element): https://fal.ai/models/fal-ai/kling-video/v3/pro/motion-control/api [V]; price $0.168/s: https://fal.ai/models/fal-ai/kling-video/v3/pro/motion-control [V]
  - Atlas Cloud guide (14 Jul 2026; community findings U, prices V as that reseller's): https://www.atlascloud.ai/blog/guides/kling-ai-motion-control
- **Luma**
  - "Introducing Ray3.2" (9 June 2026; eight faces, skeletal posture, 20 s at 1080p, 16 keyframes): https://lumalabs.ai/news/introducing-ray-3-2 [V]
  - "Ray 3.2 Video to Video" (Modify Video: 64 keyframes; Motion and Structure 1-9; Bodies, Poses, Face; forehead and upper-cheek blind spot): https://lumalabs.ai/learning-center/articles/ray-3-2-video-to-video [V]
  - "Introducing Ray3 Modify" (18 Dec 2025; "Your original movement, timing, and intent become the instruction."): https://lumalabs.ai/news/ray3-modify [V]
  - Seedance 2.5 guide: https://lumalabs.ai/learning-center/articles/seedance-2-5-complete-guide [V]
  - MiniMax H3 guide: https://lumalabs.ai/learning-center/articles/minimax-h3-complete-guide [V]
- **Wan**
  - Wan-AI, Wan2.2-Animate-2-14B model card: https://huggingface.co/Wan-AI/Wan2.2-Animate-2-14B [V]
  - Alibaba Cloud, Wan video prompt guide (updated 24 Sep 2026): https://www.alibabacloud.com/help/en/model-studio/text-to-video-prompt [V]
- **Other prompt guides**
  - LTX-2 prompting guide: https://ltx.io/blog/prompting-guide-for-ltx-2 [V]
  - Google, "Ultimate prompting guide for Veo 3.1" (16 Oct 2025): https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1 [V]
  - OpenAI Cookbook, Sora 2 prompting guide: https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide [V]
- **Papers**
  - FilmBench, arXiv 2607.24241 (July 2026): https://arxiv.org/abs/2607.24241, https://arxiv.org/html/2607.24241 [V]
  - LPM 1.0, arXiv 2604.07823 (definition of performance; background only): https://arxiv.org/abs/2604.07823 [V]
- **Other**
  - Academy of Motion Picture Arts and Sciences, 99th Oscars rules (1 May 2026): https://press.oscars.org/news/awards-rules-and-campaign-promotional-regulations-approved-99th-oscarsr [V]
  - Cleveland Clinic, "Vital Signs" (adult resting respiratory rate): https://my.clevelandclinic.org/health/articles/10881-vital-signs [V]
- **Library files built on**
  - A1 P10, §6 (R10-R17, R36-R44), §11, Ex3
  - A2 P10, Steps 5-9, rules 24-27, Ex A-B
  - A3 §3.2, R2, Ex1
  - B5 §3.3, §5 (5.6-5.7), §6.5, §10, Ex1-Ex3, Ex5, §14
  - C1 R12, Rec7
  - C2 §7.3 (mirror eras)
  - C3 §5, §6, §7A, §9D, §11, §16, rules 16 and 22, Recipes 3-4, linter (L14)
  - C4 §3D-3E, Rec7, §11
  - D3 voice table (VOICE-IONA D02), rule 3, speech-to-speech
  - D4 rules 7 and 9, Recipe 4 step 5
- **Test texts**
  - *The Catch* (25 Sep 2026 workshop revision)
  - *The Long Places* ch. V and VII
