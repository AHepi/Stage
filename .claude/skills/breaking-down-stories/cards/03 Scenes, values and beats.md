# Card 03. Scenes, values and beats

Read whole at step 7 for every scene. "A2 R4" is rule 4 in A2 §7; A2's "sc10, B7" is `SC10-B07` here.

## The job

In The Catch scene 10 the core value is Iona's belief about her own body: `+` at "Kitchen.", `---` after "Nothing has happened to the mint." It swings at `SC10-B07`, where "Chew that." meets "Her face changes." Everything the camera does later in the scene is spent on that beat.

A scene exists to change at least one value (A2 P4, P8). Hand on to the shot list (card 14) the turn beats, the nonverbal beats a line-by-line list drops, and every beat's intensity. Fields: SCENE `value`, `want`, `driver`, `conflict`, `third_thing`, `flags`; PART; BEAT `action`, `reaction`, `task`, `beat_intensity`, `turn`, `charge`, `five_steps`.

- A **value** is a quality of a character's life with two poles, such as trust or distrust (A2 §2).
- A **charge** is where a value sits at one moment, `---` to `+++`; A2's mixed "+/−" is written `0`.
- A **beat** is one action plus the reaction it provokes; "(beat)" in a script is a pause (A2 §2, Step 0).
- A **tactic** is what a line or act does to the other person, an -ing word such as `proving` (A2 P9).
- A **turn** is the beat where a value swings to the charge it keeps to the scene's end (A2 Step 7).
- A **part** is a stretch of a scene with its own turn; the **driver** is the character whose want sets the scene moving (A2 §2).
- The **third thing** is what two people talk through so they need not talk about themselves (A2 P13).
- The **five steps** are desire, obstacle, choice, action and expression: one decision slowed down (A2 P10).

## Questions in order

1. What does the audience already know, and what changed since these people last met (A2 Step 1)?
2. What is the **event**, the one change the scene exists to deliver, in the plan's past-tense sentence? If no beat changes anything, flag `nonevent`; never invent one (A3 P1, A3 R1).
3. Which one to three values are at stake, named in a life ("trust or distrust, Iona toward Eli"), not as topics ("the flask")? Mark one `core: yes`; score `open` and `close` from the character's side (A2 Step 2).
4. What does each character want now, from this person? Test: if the other side gave in, would the scene end? If not, the want is wrong (A2 Step 3; A3 §3.2). Wants that never cross: flag `splintered`.
5. Who drives, and which conflict type below holds (A2 §4)?
6. Where are the beats? Pair each speech or described act with its reaction; merge beats only when a tactic repeats without topping the last, since escalation is not repetition (A2 Step 5, P9). A move or look that provokes a response is a beat (A2 R3).
7. What does each beat do? An action tactic acts on someone (`accusing`, `testing`); a reaction may be inward (`absorbing`) but playable. The hands go in `task` (A2 Step 5; A3 §3.2).
8. Where does each value turn? Run the sign test (A2 Step 7).
9. Does each new part start after a drop in pressure or without one (A2 Step 7, R10)?
10. How intense is each beat? Use the list below (A2 Step 6).
11. At each turn and each beat of intensity 4 or 5, what are the five steps, each a visible moment (A2 Step 8)?

**The sign test** (A2 Step 7; CRAFT-18). If a value's sign changes between `open` and `close`, it turns at the first beat after which its charge sits on the closing side for good. If only the strength changes, it turns at the first beat that reaches `close` and stays. If `open` equals `close`, `kind: none`. Every beat whose `turn` is not `none` must pass this test; the core value's turn is `main_turn`.

**Beat intensity** (A2 Step 6; range in `scales`). Take the first level, from 5 down, that fits. **5:** a value turn. **4:** an open accusation; a forbidding, threat or ultimatum; a confession; a disclosure that damages someone present; a move that blocks, threatens or shields. **3:** a direct challenge or unwanted question; a demonstration or test; an open refusal; a slip caught. **2:** probing, hinting, noticing; a planned breather; beats after the main turn. **1:** logistics, nothing at risk. Score inside the scene, not against the film.

## Translation menus with pitfalls

Pick at most one option per row; tie it to a line, object or action in this story.

| The scene holds | Options | Pitfall |
|---|---|---|
| A new tactic | a new setup, size, camera move or actor's move (A2 R1) | a new picture inside a held tactic fakes progress (A2 R2) |
| A revelation turn | an insert of the evidence, then the receiver's face held (A2 R8) | cutting away from the reactor |
| An action turn | the whole act and its result in one frame (A2 R9) | a cut inside the act hides the change |
| A new part after a drop | a wide from a new angle (A2 R10) | widening with no drop releases the pressure |
| Power changes hands | the camera takes the new driver's side or height, crossing on screen (A2 R11) | a bare cut across the line |
| Waiting as a tactic | hold on the one waited on; the silence's length is the action (A2 R18, P11) | inserts that break the wait |
| A third thing | inserts of it; eyelines leaving it mark escalation (A2 R19) | losing it at the turn |
| Several react at once | one frame holding all (A2 R7) | singles cannot show "at the same moment" |
| Action, reaction, reaction | trust rising: one two-shot holds both; trust breaking: singles (A2 R6) | a cut splitting what the beat joins |
| A witness or sleeper restrains someone | the restraint in frame at peak pressure (A2 R21) | no visible reason she does not explode |

By conflict type (A2 R12-R17): balanced, matched sizes tightening in step; asymmetric, the attacker moves, the resister stays in a task until her turning line; indirect, group frames keeping the witnesses; comic, wide frames, a hold after the punch line; minimal, long takes, every pause kept; reflexive, reflections and a setting drawn as she feels it (card 19).

## Budgets and saved choices

- At most `beat_intensity_5_per_part_max` beats of intensity 5 in a part (CRAFT-05); keep 5 for the main turn and the turn nearest it, score other turns 4 (A2 Step 6).
- A turn owes at least `turn_reaction_min_s` of held reaction (A2 Step 9; TIME-05); leave room for it in the list item.
- The scene's tightest size, its one push-in (`push_in_per_scene_max`) and its one extreme close-up (`extreme_close_up_per_scene_max`) belong to the main turn: caps, never quotas (A2 R4; CRAFT-01 to CRAFT-03).
- Beat IDs come from `issued_blocks`; a scene over `scene_split_beats` beats or `scene_split_non_blank_lines` non-blank lines is designed in two units by part. Every line sits in a beat (COVER-01).

## The baseline is a strong answer

Static, the owner's eye height, a normal lens, **room sound** (the place's steady background) are choices, not failures; depart only for a reason you can cite. A held tactic holds one setup (A2 R2); routine beats keep all five steps inside one shot at normal speed (A2 P10); one value with one turn is a complete scene.

## Cliché traps

Each with its test and fix (A2 §10).
- **One beat per line.** Test: the beat count nears the line count. Fix: merge repeats that do not top each other (A2 P9).
- **The loudest moment called the turn.** Test: the sign test lands elsewhere, often quietly ("I wasn't asking her."). Fix: move `turn` (A2 §10).
- **Activity verbs** (`talking`, `asking`, `explaining`, `looking`). Test: can it be done to the other person? Fix: `probing`, `cornering`, `justifying`, `outwaiting` (A2 Step 5).
- **Emotions as beats** ("shocked"). Fix: the action that causes the feeling and the behaviour that shows it (A2 §10; A3 R2).
- **Values as topics; the want as the life want** ("to save her family"). Fix: two poles in a life; what she wants now, from this person (A2 §10).
- **Rewriting a flat scene.** Fix: flag `nonevent`, `turn_too_soon`, `turn_too_late` or `splintered`; never invent an event (A2 Step 7).
- **The any-film test**: "love or loss" fits any film (A2 Step 2).

## Reasons that fail and reasons that pass

- Fails `SC10-V1 | name: family`. Passes `SC10-V1 | name: normal or altered, Iona's belief about her own body | core: yes | open: + | close: --- | turns_at: SC10-B07 | kind: revelation` (A2 §11).
- Fails `main_turn` on `SC10-B04` "because it is the biggest argument". Passes: after B04 the core value sits at `0` ("It's my right."); it first reaches the negative side at B07, "Her face changes.", and stays, so the sign test puts the main turn there (A2 §11).
- Fails `SC10-B06` scored 5 "because it is tense". Passes 4: "Don't open the flask." is a forbidding and no value turns on it (A2 Step 6).

## Two worked examples

### The Catch, scene 10 (asymmetric)

Values (A2 §11): `SC10-V1` normal or altered, core, `+` to `---`, turns at B07, revelation; `SC10-V2` free or contained, `+` to `--`, turns at B11, action; `SC10-V3` trust or distrust, Iona toward Eli, `+` to `+`, `kind: none`. Saye drives with tests; Iona resists; Eli's knowledge leaks through a task ("He stops. Twists it the other way.").

Beats (action / reaction, intensity): B01 appealing / admitting on her terms, 2; B02 probing / joking, 2; B03 verifying / normalizing, 3; B04 demonstrating / refusing, 3; B05 compensating / clocking him, 3; B06 testing / forbidding / conceding, 4; B07 proving / discovering, 5; B08 naming the truth / absorbing, 4; B09 reporting / challenging, 3; B10 shielding / redirecting, 4; B11 outwaiting / yielding, 5. `SC10-P2` covers B09 to B11 and `starts: after_drop`: Iona absorbs B08 in silence.

```
### BEAT SC10-B07
- lines: 449-463
- action: CH-SAYE | tactic: proving
- reaction: CH-IONA | tactic: discovering
- task: CH-IONA | does: chews the leaf, stops, chews once more
- beat_intensity: 5
- turn: main_turn
- turn_kind: revelation
- charge: SC10-V1 | charge: --
- five_steps: desire | shows: her eyes on Saye, still defiant
- five_steps: obstacle | shows: the leaf held out into her frame
- five_steps: choice | shows: a half-second before her hand moves
- five_steps: action | shows: she chews, in one unbroken frame
- five_steps: expression | shows: "Not mint." after her face has told us
```

### The Long Places, chapter III (quiet prose)

"I am equipment," Márton said, "not content" (line 247). Value: concealed or disclosed, Márton's old wound, `-` to `++` (A2 §14). Night brings the action turn: "he told it, flat, in the voice he used for instrument logs" (line 249); "It was measured" (line 255) strengthens it without changing its sign. The value's visible form is the camera: in the evening it sits between the men, light on; at night the same table, framed the same way, has none, and that absence is the turn picture (A2 §14, R20).

## Self-check

Yes or no; a "no" needs a fix (A2 §9).
1. Does every value have two poles in a life, and does one close at a new charge?
2. Does every turn pass the sign test, with one `main_turn` on the core value?
3. Does each want pass "if granted, the scene would end"?
4. Is every tactic a playable -ing word, none of talking, asking, saying or looking?
5. Are nonverbal beats in, and every "(beat)" a pause?
6. Is every beat intensity from the list, within `beat_intensity_5_per_part_max` fives a part?
7. Are the five steps written for every turn and every beat of intensity 4 or 5?
8. Is every line and speech of the scene in a beat, and every timing fault flagged, not fixed?

## Words for AI models

Works: behaviour from the tactic, "she stops chewing, frowns, chews once more, slowly"; the wrong-tasting mint means recognition and confusion, never disgust (A2 R25, §11). Split a long take only at a beat boundary with matched framing (A2 R24), and write each single's eyeline into its prompt (A2 R26). Fails: a named emotion ("disgusted", "betrayed") gets a stock face (A2 R25).

## Look up for more

`stage.py lib A2 §6` (the method), `A2 §7` (rules), `A2 §11`, `§12`, `§14` (worked scenes): `library/A2 Scene design, values and beats.md`. `A3 §3.2` (the director's pass): `library/A3 Script breakdown, directing and adaptation.md`.
