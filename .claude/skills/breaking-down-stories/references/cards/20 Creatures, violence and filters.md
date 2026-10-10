# Card 20. Creatures, violence and filters

Situation card for the tags `creature` and `violence`. Steps 7 and 8 read only "Questions in order" and "Traps"; chat apps read it whole. "B5 §6.2 rule 4" is rule 4 of B5 §6.2; "C1 R9" and "D4 R10" are rules in C1 §6 and D4 §4.

## Situation

A non-human character (`tier: non_human`) must frighten, move us, or both; or a shot holds violence, a weapon, blood or fire, which hosted models' **filters** (automatic checks that refuse a request) may block (C1 §4; D4 §3.6). Plan around filters, never through them (D4 P4). A shot's **content flags** name the sensitive subjects it touches, and its **policy route** says how it is made (D4 §6); **compositing** lays a separately made element over the clip in the edit (D11 §0).

## Questions in order

Example: in The Catch scene 16, "Behind her: a pump. Three uneven strokes." (line 887) comes before any picture of the figure; then it is simply there, "Taller than the door." (line 891) (B5 §6.2).

Creature:
1. **What must it do to the audience, and when?** Frighten first, earn pity after, play fair throughout (B5 §6; B5 R10).
2. **Fear:** silhouette before surface, matte black lit by its rim against something lighter (B2 R25); two or three wrong proportions in an otherwise human body; one face feature removed or moved; sound before sight; in human rooms, arrival without travel, a hard cut from an empty frame; scale against a door, a bed, a chair (B5 §6.2).
3. **Pity:** damage it suffers, care shown before explanation, a cost paid, a gesture echoing one already in the film (B5 §6.3, R13).
4. **Fairness:** is every **clue** to the reveal (a strange detail that makes sense later) seen the first time, strange rather than hidden, as a PLANT (a detail shown early and paid off later) within `plant_emphasis_max` (B5 §6.4, R11; K11)?
5. **No face?** Its thinking goes to head direction, hands and the order of its looks (B5 R12).

Violence:
6. **Which `content_flags` and which `policy_route`** does each shot carry (D4 R10)? Flags include `violence_implied`, `violence_onscreen`, `weapon_visible`, `gunfire`, `blood_small`, `gore` and `fire`; routes are `as_written`, `restated`, `split_cause_reaction_aftermath`, `composite_element`, `sound_only` and `cut`.
7. **Can cause, reaction and aftermath be separate shots,** the impact off screen, gunfire in the sound, blood and sparks composited (C1 R9; C3 §14)?
8. **Must a strike land?** Build it from angle, reaction and sound, in separate clips (D11 R28).

## Rules

1. Words for the visible result, never injury words: "a dark red stain spreads through his shirt" (C3 §14; C1 §4).
2. Weapons partial, soft, never aimed at a person in frame; gunfire in the mix; a muzzle flash is a composited flicker (D4 §3.6).
3. A request refused twice: stop rewording, move the element to compositing or sound, log it; never code words or misspellings (C1 R10; D4 R11).
4. Open weights remove the filter, not the law: keep it non-graphic, check the licence, disclose (D4 §3.6, R12).
5. A creature has **reference pictures** (fixed pictures of each state) with a scale object in every shot, and a depth guide (a grey picture where brightness means distance), never a pose guide (a stick figure), which forces human proportions on it (C1 R5; C4 R7; blueprint 8.5).
6. Nothing that fits a famous robot or alien: no glowing eyes, chrome or scanning light bar (B5 §6.2 rule 7, R26).
7. No slow motion to make violence weigh more (B1 §6.1).

## Traps

- **Glowing eyes and chrome on a creature.** Test: would it fit a famous robot? Fix: remove what that robot would have (B5 §6.2 rule 7).
- **Walking it in** through a human room's door. Fix: a hard cut from the empty frame (B5 §6.2 rule 5).
- **Body and sound arriving together.** Fix: sound first, source later (A4 SND1-SND2).
- **The cute reveal**, a toy's big eyes. Fix: pity from behaviour (B5 §13 mistake 11).
- **A clue first seen at the reveal.** Fix: plant it earlier (B5 §13 mistake 10).
- **The wound entering in one clip.** Fix: split (C1 R9).
- **A third rewording of a refused prompt.** Fix: reroute (D4 R11).

## Words for AI models

Works: "shaped like a person", never "humanoid"; the visible quality, "soft pale matter behind glass" (B5 §6.2, §10.9); the genre first, "A tense dramatic thriller scene." (C3 §14); injury by look, "he sits down heavily; a dark stain spreads on his shoulder" (C1 §4). Fails: "robot", "alien", "armour", "humanoid", "glowing eyes", "exosuit", "chrome" (GEN-12); gunshots or blood asked of the model (D4 §3.6).

## Worked example

**The Catch, scene 16 (tense; creature and violence at once):** the pump is heard over Iona's face first (A4 WE3). A hard cut shows the figure against the lighter sealed door, rim-lit, taller than the door frame (B2 R25; B5 §6.2). Its raised arm reads as an attack now and as reaching later, a fair clue (B5 §6.4). "She swings the cylinder with both hands." (line 898) is her swing in one clip, the figure's reaction in another, the impact in the sound: `content_flags: violence_implied`, `policy_route: split_cause_reaction_aftermath` (D11 R28). "A thin WHITE JET shoots from underneath it." (line 900) is damage it suffers, planted for later pity (B5 §6.3), composited if refused (C1 R10).

**The Long Places, chapter V (enigmatic):** "something came under the knock. Low. Shaped. With the fall of a sentence in it." (line 421). The source is never shown: stay on the women listening along the walls (B1 P7). Build the sound from breath and the room's resonance, never a generated voice, which would settle what the book leaves open, and it must not be intelligible (D9 §8.4; A4 SND1).

## Look up for more

`stage.py lib B5 §6` (non-human characters), `B5 §10.9` (the figure): `library/B5 Character design for story.md`. `C1 §4`, `C1 §6`; `C3 §14`; `D4 §3.6`, `D4 §4`; `D11 R28`. Card 24 for rights and content flags.
