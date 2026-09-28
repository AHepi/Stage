# Card 18. Suspense, reveals and the dark

Situation card for the tags `suspense_and_reveal` and `darkness`. Steps 7 and 8 read only "Questions in order" and "Traps". "A4 S2" is rule S2 in A4 §9; "B2 R23" is rule 23 in B2 §7.

## Situation

A fact matters and someone does not know it yet, a reveal is coming, or the scene is dark. FACT records hold who knows what, from when (A4 §6.5). What the frame keeps out is as authored as what it shows (B1 P7), and what stays dark is designed as carefully as what is lit (B2 P7).

## Questions in order

Example: in The Catch scene 6, "He has one hand she cannot see." (line 253): we learn that Eli hides something, not what; the frame keeps his hand out of view (B1 Ex2).

1. **Which FACT records have an element in this scene before their reveal?** Every earlier shot that could show a FACT's `element` (what would give it away) carries `keep_hidden`: the fact and a way from question 4 (`FT-03 | how: frame_edge`) (A4 S3; INFO-01).
2. **What is each fact's `mode`?** **Suspense** and **dramatic irony** (we know more than a character): show the danger early and clearly, then hold longer on the unaware (A4 S1-S2; TIME-09). **Mystery** (we know the same): stay with the **whose-scene** character, the one whose point of view the scene holds; reveal with them. **Surprise** (we know less): once, at a big turn, fair on replay (A4 §6.5).
3. **Should the audience know more?** Plan the telling shot at least one beat before it matters (A3 R4), showing the hidden thing where the other character cannot see it (A1 R4). To share a character's not-knowing, stay on that face while the other keeps the secret (A1 R3).
4. **How does each earlier shot keep it hidden?** Mildest first: `frame_edge`, `focus`, `dark`, `obstruction`, `timing`, `sound_first` (A4 §6.6).
5. **Does a shot show what that character cannot know?** Give it a `pov_break` (A3 §7.3; REASON-09).
6. **At the reveal:** a clean, readable view, then the landing face (the face showing what it means); `role: turn` or `must_keep` (A4 §6.6; INFO-02). With clues already given, play it as confirmation in real time (A4 S4).
7. **A stated time limit?** Honour it in screen time, or stretch it with a `why` (A4 R6).
8. **In the dark:** what stays dark (LOOK `stays_dark`, SHOT `dark`), and what one element stays readable in every shot: a rim, an eye light, a lit hand (B2 R23)? Darker skin is exposed, filled and named (`skin_light`), never grey (B2 R24).

## Rules

1. A **plant** (a detail shown early so a later moment pays it off) gets one calm, clear shot within `plant_emphasis_max`; the payoff repeats its framing or sound (A4 S5; K11; FILM-02).
2. Hide a body part or an object, not the face, when a character hides something from another but not from us; lose the eyes only to hide their inner life from us (B2 R6-R7).
3. A large revelation lands hardest in the flattest light available (B2 R11).
4. A growing threat is heard before it is seen (A4 SND1); no music under a reveal meant to stay open (A4 SND5).
5. If a later scene replays this one on a screen, put that camera in this scene's set plan now (A3 R9).
6. Release suspense in a way the audience accepts; do not punish it (A4 S6).
7. Every dark line the story writes needs a `stays_dark`, a `light_cue` or a shot `light` (COVER-08).

## Traps

- **Faster cutting for suspense.** Test: the unaware character's shots average shorter than the scene's dialogue shots. Fix: hold (A4 S2; TIME-09).
- **A reveal spoiled by coverage.** Test: a wide or reverse shows what a close shot keeps hidden. Fix: check `keep_hidden` against every shot (A4 §13).
- **The camera finds the secret**, tilting down to the hidden hand. Fix: keep the frame edge (B1 Ex2).
- **A sting or push-in on a reveal the script already marks.** Fix: add nothing (`added_emphasis_per_beat_max`; CRAFT-10).
- **Too dark to follow.** Fix: one readable element per shot (B2 R23).
- **A darker face gone grey** beside a correct lighter one. Fix: reject it (B2 R24).

## Words for AI models

Works: name only what is in frame; hidden things go in `must_not_show`, sent to the model's exclusion field where it has one (K18). Darkness as a visible result: "the far corner falls into deep shadow; her face is lit from the lamp at her knee" (B2 P12); the skin tone and the light on it named (B2 R24). Fails: "moody", "atmospheric", "dramatic lighting" (GEN-12); the secret named in a prompt.

## Worked example

**The Catch, scenes 6 and 13 (tense):**

```
### FACT FT-03 The hand in the fall
- what: in the fall, Eli's hidden hand clipped the puck to the grid
- element: PR-PUCK.S02
- audience_knows_from: SC13 "Eli's hand comes out from behind Jude's back."
- known_by: CH-ELI | from: SC06 "He has one hand she cannot see."
- mode: mystery
```

That Eli hides a hand at all is a separate FACT, `dramatic_irony` from scene 6 (card 01).

In scene 6 Eli's arm leaves the bottom of the frame: `keep_hidden: FT-03 | how: frame_edge` (B1 Ex2; B2 R6). In scene 13 the recording from `CAM-SHAFT-TOP` plays in real time, flat and top-down (B2 R11), and "Jude watches her watch it." (line 734). The footage holds through "Empty.", so we find the puck before Iona reacts; then her face: "Looks at her brother. Not at Jude." (line 742) (A4 WE2, S4).

**The Long Places, chapter V (enigmatic, dark):** "the cough came, beside her, at her left, where nobody was" (line 439). The lamp at her knee is the shot's one readable element (B2 R23); the cough is heard off screen and never given a source; the camera stays with her and never turns to search the dark (A4 §6.6; B1 P7).

## Look up for more

`stage.py lib A4 §6.5`, `A4 §6.6`, `A4 §9`: `library/A4 Editing, transitions, rhythm and sound.md`. `A1 §6`; `A3 §9`; `B1 §10.4`; `B2 §7`; card 17.
