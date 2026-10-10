# Rule order

When two rules want different things for the same shot, the higher rule on this list wins, and the record's `why` says which rule won and names the line, object or ID it rests on. Example: in The Catch scene 10, Eli's warning "Don't open the flask." would get a single on Eli under ordinary dialogue coverage (rule 9), but his camera rule `CR-ELI` saves his closest singles for scene 13 (rule 4), so shot 130 hears him off screen. The order merges A1, A2, A4 and B1 to B3, readability second as B2 and A1 put it.

1. What the story itself states we see and hear.
2. Readability of the beat.
3. Physical honesty.
4. The film's systems and budgets.
5. Flaw handling.
6. Turn rules.
7. Emotion over spatial continuity, logged as a departure.
8. Conflict-type defaults.
9. General beat defaults and translation menus.
10. The baseline.

## 1. What the story states

Directions, named light, written transitions and stated sounds are binding (A1's precedence, rule 1). **Tie-break.** The Catch scene 15 writes "A small CLICK, from nowhere." Played as horror, the dread tone's defaults would make the click loud and place it off frame (D10 §12.1; `tone_defaults.json`, rule 9). The story says small, so the effect item keeps a low `sound_emphasis`, and the `why` quotes the line.

## 2. Readability of the beat

The audience must be able to read the face, the text and the geography (B2, A1). **Tie-break.** The tag "Goods only. No persons." needs its reading time from the `text_floor` constant: K09 works it out as 4.0 seconds, and twice that where the text is mirrored. A tense scene's shorter target shot length (rule 9) or the film's rhythm plan (rule 4) cannot cut the insert shorter; TIME-01 holds the floor. The same rule keeps every face readable in a dark look (B2 R24).

## 3. Physical honesty

In-story footage, physics and glass optics behave as they would for real (B1 R22-R23). **Tie-break.** Scene 13 replays the recording from the shaft camera `CAM-SHAFT-TOP`. The film's camera system (rule 4) would put the lens at the owner's eye height with the normal lens, but footage from an in-story camera keeps that camera's fixed place, lens, frame rate and overlays from its CAMERA record, and every excerpt is cut from one master take of the scene 6 event (B1 R22, §10.4).

## 4. The film's systems and budgets

Banned and saved choices, character camera rules, the motif code, the colour script and location continuity are written at step 6 and hold for every scene (B1 P5, B4). **Tie-break.** The turn rule (rule 6) would give scene 10's main turn the most extreme framing the scene can reach. The film-level saved choice `extreme_close_up_film_max` and the ladder keep the film's tightest size for scene 13 (K05, K12), so shot 150 lands at `close_up`: still the scene's tightest frame, spent on its turn, within the budget.

## 5. Flaw handling

Lines carrying a BEAT `flag` are staged to contain the flaw, never rewritten: on-the-nose or melodramatic lines are staged small (A1 R35-R36), forced exposition moves to an image or off screen (R22), a monologue gets listener coverage (R31). A1 ranks these above its turning-point rules. **Tie-break.** A line flagged `melodrama` falls on a turn beat. Rule 6 wants the scene's tightest framing on the turn; A1 R36 wants the speaker static, one size wider than the scene's other beats, with no score. Flaw handling wins: the speaker's shot stays static and wider (CRAFT-21 checks size, move and music), and the turn's tightest frame goes to the listener's landing face when the listener carries the change (A1 R1).

## 6. Turn rules

The scene's most extreme framing goes on its turn, and nothing tighter comes before it (B1 R1, A2 R4; CRAFT-03), within the rules above: the ladder's rung (rule 4) sets the turn's size, a wide rung marking the turn by opening out, and a rung or a camera rule's cap may let earlier shots equal it; through one fixed in-story camera (rule 3) size cannot change, so the frame's action and the cuts carry the turn (B1 §10.5). **Tie-break.** A black-comedy reading of scene 10 would widen beat 7 and cut after "Not mint." to Saye's unmoved face (D10 §12.2), that tone's default (rule 9). The turn rule wins: the tone moves the dial, never the turn (D10 principle 1), so beat 7 keeps the scene's closest frame and the comic undercurrent rides on lines and wide shots elsewhere.

## 7. Emotion over spatial continuity

When a cut that serves the emotion breaks the geography, keep the emotion (A4 R1: emotion first, space last). **Tie-break.** In a balanced two-person scene the matched singles (A2, rule 8) keep both sides on one lens and one side of the line. If the strongest reaction can only be seen from across the line, the shot crosses it, and the scene's `departure` answers GEOM-03.

## 8. Conflict-type defaults

Each conflict type has its coverage (A2 R12-R17). **Tie-break.** Scene 10 is asymmetric: Saye drives, and the resister stays still, anchored in a task, with her closest shot saved for her turning line. The approach progression (rule 9) would tighten on Iona beat by beat; the conflict type holds her wider until her line "Not mint."

## 9. General beat defaults and translation menus

The menus in cards 10 to 14 and the tone defaults apply where nothing above decides. **Tie-break.** Scene 10 opens on Saye's view at her door: a point-of-view pan to the flask. The menu's pan beats the static baseline, and the `why` names the flask.

## 10. The baseline

Static, the owner's eye height, a normal lens, room sound. It is a strong answer, and a normal shot that departs from nothing may give `because: default` with no `why` (REASON-01, REASON-02). **Tie-break.** When two menus pull different ways and neither can cite a line, an object or an action from this story, neither wins: the shot returns to the baseline.
