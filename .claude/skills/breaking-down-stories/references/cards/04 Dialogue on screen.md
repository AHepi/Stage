# Card 04. Dialogue on screen

Steps 7 and 8 read only "Landing face", "Flaws" and "Pauses"; chat apps read it whole. "A1 R19" is rule 19 in A1 §6.

## The job

In The Catch scene 13, "One body." / "One." / "You." plays on Iona with Eli heard off screen: the fact is fired at her, so the change happens in her face (A1 Ex3). Every line is something the speaker does to someone; film that action and where it lands, not the words (A1 §1, P1).

The dialogue pass covers turn beats, flagged lines, revealed facts and refusals at standard, every line at detailed. It writes BEAT `landing_face`, `unsaid`, `carrier`, `pause_after`, `flag` (detailed adds `core_word`, `cut_rule`); at step 8 each SHOT `hear` item says whether its speaker is seen.

- The **unsaid** is what a character could say and chooses not to; a **carrier** is the object, hand, distance or sound that makes it seen or heard (A1 §2, P3).
- The **core word** carries a line's meaning (A1 §3.5); a **split edit** changes sound and picture at different moments (A1 §2).
- **Room sound** is a place's steady background; a **third thing** is what two people talk through instead of themselves (A1 §2).
- A **beat** is an action and its reaction; its **tactic** is the -ing word for what it does; a **turn** is where a **value**, a two-pole quality of a life, changes for good (A2 §2).

## Questions in order

1. For each line in scope: its tactic, unsaid and core word (A1 §7)?
2. Is each fact fired, planted, forced, or shown by an object (A1 R19-R22)?
3. Which conflict levels are in play, physical, social, personal, private (A1 P7)?
4. Which line turns the scene; where are the pauses around it (A1 R13-R15)?
5. Who is frame-left and frame-right; where does each look (A1 R39-R43)?
6. Whose face does each key line land on (A1 R1-R7)?
7. What do the hands do or keep still, and how does it change at the turn (A1 P4, R8-R10)?
8. Which cut rule for each key line; what is heard in each silence (A1 R17, R27-R29)?

## Landing face

Example: in scene 10, "Don't open the flask." is Eli forbidding Saye. It lands on Saye, whose answer is "Saye sets her scissors down.", so Eli is heard off screen (A1 R1; K05: `CR-ELI`, Eli's camera rule, keeps his close singles for scene 13).

The **landing face** is the face on screen when a line's core word lands, the biggest camera choice in a dialogue scene (A1 §2, P2). Write a character ID; `insert:` joined to a prop or text ID (`insert:PR-FLASK`) when the line lands through an object; or `wide`. Highest rule first:
- The script's directions about what we see are binding: "Looks at her brother. Not at Jude." (A1 §6, precedence).
- A line aimed at someone lands on the receiver; the speaker is partly or wholly off screen (A1 R1).
- A line that costs the speaker (a confession, the dangerous question) holds on the speaker through it and the silence after (A1 R2). When both apply: the speaker through the line, the receiver from the core word on (A1 §6 tie-break).
- A **fired fact**, a fact used as a weapon, lands on its target; the shooter gets one short reaction after (A1 R19, P6).
- To share someone's not-knowing, stay on that face while the other keeps the secret (A1 R3).
- A silent third character gets at least one reaction at the turn (A1 R5; CRAFT-24).
- Two equals in a small beat stay in one two-shot; when the relationship breaks, go to singles on the turning line, not before (A1 R6-R7).
- A **volley**, three or more quick short lines, keeps one angle; only the line that carries the change gets a new, closer shot (A1 R29).

At least once in every dialogue scene the landing face is not the speaker (A1 §8 check 5, R1; CRAFT-23). Every unsaid needs a carrier in a shot of its beat (A1 P3; REASON-08): "She is hurt" is not a shot; "Her thumb stops turning the ring" is.

## Flaws

Example: "Eli. Are we going to be all right?" is direct, yet takes no flag: Iona chooses directness; her tactic is `demanding` (A1 Ex2).

A flaw is a fault in one written line. Flag it on its BEAT, `flag: <flaw> | line: <speech ID>`, and design the shots around it; never change a word, since rewording makes lines more on the nose (A1 R38).
- `on_the_nose`: the line says exactly what the character feels. Give the actor a hidden action under it; add no emphasis (A1 R35).
- `melodrama`: big words, small stakes. A static camera one size wider than the scene's other beats, no score (A1 R36; CRAFT-21).
- `forced_exposition`: people telling each other what both know. Play it off screen over a busier picture, or move the fact to an insert or a document (A1 R22).
- `monologue`: a long speech with no reaction (A1 counts a line over 40 words as long). Mark each change of tactic as a beat and choose speaker or listener beat by beat, or keep the listener in frame (A1 R31, §5; CRAFT-22).
- `repetitious`: the same action and reaction in new words. Vary each beat's size, height or distance (A1 §3.7, P9).
- `can_play_silent`: a nod or a glance could carry it. Flag it for the director and keep the words (A1 R18).
- `interrupted`: a line cut off with a dash ("In the car-"). Stay on that face through the cut-off, or cut to it just after (A1 R30a).

A scene with no turn takes the SCENE flag `nonevent`; busy coverage must not hide it (A1 R37). Flaw handling outranks the turn rules (A1 §6 precedence).

## Pauses

Example: scene 13's "She waits." is the pause before the fired fact: long, held on Eli past comfort, room sound and the monitor's hum. "Silence." after "You." is the pause after it: cut wide once, then hold (A1 Ex3; D3 §11.2).

A written pause becomes a hold, a cut or a push-in, and always a sound (A1 P5). Its tier comes from `pause_tiers`: short, medium, long, or `hold` beyond long, which needs a saved choice, a RESERVE record (K10; TIME-08); script words map through `pause_tiers.script_words`. Write `pause_after: long | seconds: 3 | picture: hold | sound: room sound and the monitor's hum`.
- Before a turn: `picture: hold` if the character in frame waits or is outwaited, `picture: push_in` if deciding, using the scene's one push-in (`push_in_per_scene_max`; A1 R13, P5).
- After a turn: `picture: hold` on the receiver, or `picture: cut_wide` to show the new distance (A1 R14), for at least `turn_reaction_min_s` (TIME-05).
- A refusal to answer is a line: give the silence a shot, a length and a tactic, `refusing` (A1 R16).
- Rank the marked pauses, nearest the turn first, then by how much each changes what the audience knows; only the top `long_pauses_per_scene_max` are long, the rest short, medium or cuts (A1 R15; TIME-04).
- Every pause has a sound: room sound and one small real sound, never dead air, and no music that states the subtext (A1 R17, §8).

## Translation menus with pitfalls

Pick at most one per line; tie it to a line, object or action in this story.
- Subtext differs from the words: land on the receiver, held past the line; the speaker's task betrays the action. Pitfall: music under it (A1 §5).
- A fact planted for later: one calm, readable shot, no push-in, no music (A1 R20). A fact that can be shown: the object in frame, the line confirming it (A1 R21).
- Line design: core word last, `cut_on_core_word`; core word first, `cut_early_split`; a volley, `hold` or `no_cut_two_shot` (A1 R27-R29).
- Conflict levels: physical, the hazard wide; social, glass or desks between people; personal, two-shots and distance; private, close frames (A1 R23-R26).
- The turning line changes the shot grammar: a new angle or size, the camera stopping or starting (A1 R30). Pitfall: showing what a figure of speech compares (A1 §5).

## Budgets and saved choices

- `pause_tiers`; at most `long_pauses_per_scene_max` long pauses a scene; a `hold` needs a saved choice (K10; A1 R15). One push-in a scene (`push_in_per_scene_max`; A1 P5).
- Pace `speech_wps_default` unless a voice's `pace_wps` differs; one clip holds speech by `clip_speech_rule` (K08).
- At most `on_screen_speakers_per_clip_max` on-screen speaker a clip (GEN-13; C3 §20 item 2); delivery notes within `voice_delivery_words_max` (D3 §5.2).

## The baseline is a strong answer

Static, the owner's eye height, a normal lens, room sound are choices, not failures; depart only for a reason you can cite. A small beat between equals stays in one two-shot (A1 R6); paired singles share size, lens and height (A1 R40); a single looks just past the lens, never into it (A1 R44).

## Cliché traps

- **Following the speaker.** Test: does the landing face ever leave the speaker? Fix: a landing face per key line (A1 R1).
- **Illustrating the words.** Test: a cut to every object a line names. Fix: insert an object only when it changes hands or state (A1 R11).
- **Emotion labels or the unsaid spoken aloud.** Fix: a tactic and a behaviour, `evading`, looks at the flask, not at her; name a carrier (A1 §9, P3).
- **Scoring the subtext.** Test: the sound-off test, does the frame tell the beat without music? Fix: room sound or one real sound (A1 §9).
- **Every beat a hold; flat framing; ping-pong.** Fix: rank pauses (A1 R15); tighten toward the turn (A1 P9); a two-shot (A1 R29).

## Reasons that fail and reasons that pass

- Fails `landing_face: CH-ELI` "because he is speaking". Passes `landing_face: CH-IONA`: "One body." / "You." is a fact fired at her, so her face carries the change (A1 R19; K05).
- Fails every marked pause in scene 13 made long. Passes long only for "She waits." and "Silence.", nearest the turn; the three "(beat)" marks stay medium (A1 R15; `pause_tiers.script_words`).
- Fails music under "I wasn't asking her.". Passes room sound only, Iona held at least `turn_reaction_min_s` before any cut (A1 R14, §8).

## Two worked examples

### The Catch, scene 13 (balanced, few words)

`SC13-D17` "What was it rated for?" to `D20` "You.": `landing_face: CH-IONA`; Eli is off screen, and "You." is marked by a cut in on her face, not a cut to him (A1 R19, R30; K05). Unsaid `CH-ELI | thought: the device was bought to save her alone`; carrier: his eyes stay on the monitor until "Now he looks at her." (line 811). "She waits." and "Silence." are the long pauses (A1 R15). The one push-in runs on Iona from "I asked you in the car." to `extreme_close_up` on "I wasn't asking her." (K05).

### The Long Places, chapter IV (an understated reveal)

Halden: "Before your birth. And once since." (line 328). The narration's unsaids ("had already said when") do not exist on screen (A1 R32, Ex5). The open volume lies between them as the third thing, the margin "4–5.ix. Kept the hours. A.H." readable in an insert; "And once since." lands on Nilay looking down at the page (A1 R11, R19). Nilay's carrier: she puts the leaves back in their sleeve; cut away before she speaks, so the cut is her silence (A1 R16).

## Self-check

Yes or no (A1 §8).
1. Does every key line (a turn, a fact, a refusal, an interruption) have a landing face, and does one leave the speaker?
2. Does every unsaid have a carrier seen or heard?
3. Are pauses ranked, each with a sound, within `long_pauses_per_scene_max` long ones?
4. Are flaws flagged, every word unchanged?

## Words for AI models

Works: each quote with its speaker named in the same sentence; a reaction clip that says "she listens; no dialogue"; the silence written in, sound and length; frame side, eyeline and "does not look into the camera" (A1 §11). Delivery words from the tactic: to press, "level, quiet, unhurried" (D3 §5.2). Fails: "he is secretly guilty"; unattributed quotes with two people in frame (D3 §5.2).

## Look up for more

`stage.py lib A1 §6` (rules, tie-breaks), `A1 §7`, `A1 §10`: `references/library/A1 Dialogue as action and subtext.md`. `D3 §5`, `§11`: `references/library/D3 Voices and dialogue audio.md`. `A2 §12` (scene 13).
