# Card 15. Action scenes

Situation card for the tag `action`. Steps 7 and 8 read only "Questions in order" and "Traps"; chat apps read it whole. "D11 R12" is rule 12 in D11 §2.

## Situation

A passage holds a fall, a fight, a strike, a climb, a push, a throw, weightlessness, or a move the text calls fast (D11 R1). Models fail most here (D11 P7). An action scene is still a scene: someone wants a physical result, the danger grows, fortune flips at least once, and it ends changed (D11 P1).

## Questions in order

Example: The Catch scene 2, "Her hand closes on a rung and the rung TURNS." (line 81): cause the grip, effect the turning rung, anchor the bright sheared bracket (D11 WE1).

1. **What physical result does someone want, and what has changed by the end?** (D11 P1)
2. **Where is everything?** Write `geography`: the **anchors** (fixed, easily seen objects that orient the viewer), exits and the direction of travel. Show it once, calmly, before the pressure (D11 R5-R6; A4 C6). A journey keeps one `travel` in every shot until the story turns it (A3 §5.9; GEOM-07).
3. **What causes what?** Write `cause_chain`: each cause and its effect as two visible events (D11 R2).
4. **How does the danger grow, and where does fortune flip?** Write `escalation`, and each **reversal** (a beat that flips fortune) in `reversal` as beat IDs. None written? Find the one the text implies: a habit, a false relief (D11 R3).
5. **Does a beat fail?** Write the failure as the action, early, with a failed end state (D11 R4).
6. **Which `time_treatment`?** Reading time longer than story time: `overlapping_slices` (shots at real speed whose story times overlap); a wait: `held_real_time`; long and repetitive: `elliptical`; otherwise `real_time_continuous`; `slow_motion` only where the camera system (CAMSYS) allows it (D11 R12; CRAFT-16; K30).
7. **Write the `action_score`:** one row per **count** (one step of the action, an order, not a length), one column per body, the set and the camera; `+` applies force, `-` receives it, `=` holds still; `+` and `-` on one count means touching (D11 §4.2).
8. **What is the camera fixed to?** It obeys the characters' physics and changes its **mount** (what it is fixed to) only on a cut hidden in black or a passing body, or as the film's one CAMSYS `break` (B1 R23; D11 R17).

## Rules

1. **Physics is honest where the audience can measure it.** A **clock** is anything in frame that measures story time (the yellow stripe growing). Clock shots play at real speed, screen time equal to their **slice** (the story time shown), always forward; only clockless shots are held (D11 §3.2, R13; K20). Falls are positioned from `free_fall_half_g` on every frame (C4 R10), in a SHOT `motion` item or a master previs (a grey 3D rehearsal) named in `time_slice`; weightless bodies are positioned relative to the moving room (C4 R11).
2. **One acting body per clip where possible** (at most `acting_characters_per_clip_max`); one main action per `main_actions_per_seconds`; one camera move or none (D11 P7, R18; CRAFT-06, CRAFT-15).
3. **Touching bodies are split** so one acts per clip; a strike is angle, reaction and sound, the impact heard, never shown (D11 R20, R28).
4. **Several angles of one continuous action** become a designed shot or a chain (`start: from_end_of:`), not master and coverage (A3 R16; D11 R19).
5. **Cut on the same motion mid-action**, the whole action in both clips; cutting away, let it rest first (A4 R3; D11 R9).
6. **Never perform** height, speed, impact, falling or striking for reference (D11 R25).

## Traps

- **Nobody knows where anyone is.** Test: could a stranger point to every body at each cut? Fix: an anchor shot before the pressure (D11 P2, R5).
- **The effect before the cause.** Fix: two shots (D11 R2).
- **The grip holds**, because models favour success. Fix: the failure as the action (D11 R4).
- **Slow motion to stretch a moment.** Fix: overlapping real-time slices (K20, K30; B1 §6.1).
- **A fall that floats, or a clock that runs backwards** (the stripe shrinks between shots). Fix: compute the fall from `free_fall_half_g`; slices only move forward (D11 §8).
- **Shake for excitement.** Test: does the camera share the characters' physics? Fix: lock it to what they ride (B1 R23).
- **Bodies merge at the hit.** Fix: separate clips (D11 R28).

## Words for AI models

Works: one main action and its end state; the failure as the action; the direction of travel (D11 Recipe E). Weightless: "hair, cloth and straps drift up; nothing settles", the camera locked to the room (C3 §12). A fast move made "in slow motion" and doubled in the edit plays at real speed (D11 R15; K30). Fails: "falling" for floating bodies (C3 §12); injury words (C1 R9); fine hand work in wides (D11 R21).

## Worked example

**The Catch, scene 6 (tense):** `overlapping_slices` from "The cage falls." (line 240) to "A hard metal CLACK." (line 259), positioned in `PV-SC06-MASTER` (K20). Clock shots (the wall, the opening, "the yellow stripe. Coming.", line 248) are short forward slices; the stripe never shrinks. Held, clockless: the floating body, the blood beads, "He has one hand she cannot see." (line 253), the longest. "Her grip begins to slip." (line 255) precedes the reversal, "She hooks her fingers deeper into the grid." (line 257) (D11 WE2). The camera, fixed to the cage, never shakes (B1 §10.1).

**The Long Places, chapter II (quiet, unscored):** "She pushed with the flat of her hand, the heel of her hand, her shoulder; the pivot gritted and kept its opinion." (line 140): three escalating beats, more of her body each time, the grit an `effect`. The reversal, "The flame lay down and would not stand", turns being shut in into bad air. Pushes `real_time_continuous`, the flame's three lyings-down `elliptical`; for reference, push a real door on a locked-off phone (D11 WE5, R24).

## Look up for more

`stage.py lib D11 §2` (rules), `D11 §3` (time), `D11 §4` (score), `D11 §9`. `C4 §8`; `A3 §5.6`; `B1 §10.1`; K20, K30.
