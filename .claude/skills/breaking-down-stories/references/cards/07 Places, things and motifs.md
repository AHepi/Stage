# Card 07. Places, things and motifs

Read whole at step 4 (the motif, place and things units). Step 7 at Detailed depth reads only "Emphasis". "B4 R23" names rule 23 in B4's numbered rules (§8); "P" numbers are its principles (§1).

## The job

Turn the things a story names into records the camera can point at with the right loudness. A **motif** is a concrete thing (object, place, colour, gesture, sound) that returns and gathers meaning; a **prop** is a thing a character names, handles or changes; a **place** is a location with a job in the story (B4 §0.3). Harvest before you invent (B4 P1). Step 4 hands on MOTIF records ranked and mapped as story points, PROP records with `category`, `origin`, real size and sides, LOCATION records with their job, loudness, room sound, anchor (a fixed object seen in most shots) and exits, and every readable word as a TEXT record (card 17).

## Questions in order

1. **What is the theme as a question, and the core opposition as two nouns?** Read both from PLAN; The Catch sets GOODS against PERSONS, from its first prop: "Goods only. No persons." (line 19) (B4 §3.1).
2. **What does the story name more than once, or at a turning point?** Harvest objects, places, clothes, marks, sounds and words on things, each with its lines (B4 §3.1 step 3).
3. **Prop or dressing?** A thing a character names or handles, or that changes state on screen, is a prop; a thing only described as part of the room is dressing in `LOCATION.dressing` (A3 §5.3). The mint is a prop: Saye tears a leaf from it.
4. **Which pole is it on, or does it cross from one to the other?** A thing that crosses is the most valuable motif; the film's largest payoff (`largest_payoff: yes`) goes to the crossing closest to the climax (B4 §3.1 step 4, R2).
5. **How strong is it?** Score B4's six tests: named in the text; seen or heard without a caption; changes state; changes at a turning point; handled or looked at; cutting it loses a beat. Five or six yeses rank `spine`, three or four `supporting`, one or two become dressing at emphasis 0. Then, in order: all appearances in one scene, `single_scene`; strong but on neither pole, `plot_machinery`, framed only for clarity; not named in the text, at most `supporting` and marked `invented` (B4 §3.3).
6. **What does it mean, in one line, and which way does the meaning travel?** The user approves each meaning (B4 §3.1 step 6).
7. **Where does it appear?** Each appearance is a scene or a story point (a scene and a quote, placed before beats exist), with an emphasis and a role: plant (the first clear sight), develop (a return that changes something), teach (how it works), reveal (its meaning learned), payoff (its meaning spent), coda (one quiet return after) (B4 §0.3, §3.1).
8. **What does each place do, and is its set loud?** A **loud set** is a mind or a history made into a room: one establishing wide shows its governing feature, then it is shot for the action. A **quiet set** shows only where people are and what the danger is (B4 §4.1, R17). Write `dressing` as history: wear, absences, one kept living thing (B4 §4.3).
9. **Does the place need a set plan,** a measured floor plan with objects and marks? Yes where a shot is likely to need previs (grey 3D stand-in renders) at level `previs_plan_level_min` or more, a reflection or glass shot, or three or more people in one space (blueprint step 4; card 12).
10. **What states and sides will it have?** Real size, surface, the states to come, and an own side for any sided detail (B4 R13; PROP `side`).

## Emphasis

**Emphasis** is how loudly the camera points at a thing, on its own scale, never converted to another (B4 §3.4; K14): 0 present (small, part of the set); 1 placed (on a strong point, catching a highlight); 2 featured (an insert or medium close-up, handled or looked at); 3 spent (the beat turns on it: the only sharp or moving thing, or a rhyme: the plant's side, height, size and light repeated). A sound motif has its own **sound emphasis**, from buried under other sounds to heard alone (B4 §3.4). At step 7 write `emphasis` items and `added_emphasis` on each beat. On its own shot a plant's or payoff's emphasis wins; the beat's emphasis covers the rest.

1. **Plants stay within `plant_emphasis_max`,** made clear by composition and light, not size; a plant that is itself a plot event (a rung breaks, a sign is read aloud) may use its plot-event value, with nothing pointing forward (B4 R6; K11; CRAFT-08).
2. **Emphasis 3 is a budget:** `emphasis_3_rules`. A second 3 for one motif only as a deliberate inversion of the first (B4 P5; CRAFT-09).
3. **At emphasis 3, sort what points at the thing.** Script markers (a state change on screen, a line about it, a look or a touch) are never removed. Framing (size, a held frame, a rhyme) is how you reach 3. Added emphasis (a music cue, a light change, a sound change, slow motion, an unmotivated camera move toward it) stays within `added_emphasis_per_beat_max`, and there is none where the script already marks the beat (B4 R23; CRAFT-10).
4. **A payoff is louder than its plant, or an exact rhyme of the plant's framing;** a payoff that depends on how a thing works gets one teaching appearance at 2 before it (B4 §3.4, R7, R8).
5. **While a line states what a thing means, keep the thing at 0 or 1** (B4 R21). Two spine motifs in one shot: only one above 1 (B4 R11).
6. **After the payoff,** later appearances stay at 0 or 1, with at most one quiet coda; a readout the plot needs may reach 2, with nothing recalling the payoff (B4 R26).
7. **An absence is shown by its holder,** with a look leading to it: "The clip under it is empty." (line 312) (B4 R9).
8. **Light follows emphasis:** at 0 and 1 only the scene's own light; a light change at 3 needs a motivating source in the scene (B4 §3.4).

## Translation menus with pitfalls

B4's table is a list of questions, not a lookup: ask "what is this story's version?"; pick at most one thing per beat and tie it to a line (B4 §7).

| Story meaning | This story's thing | Pitfall |
|---|---|---|
| A life on hold after a loss | "A pot of mint on the windowsill, and that is all." (line 404) | a lone houseplant no line asked for |
| A secret choice | an empty holder where something was | a glint on the object |
| Estrangement | labels and rings that read wrong | the camera noticing before the character does |
| Being treated as goods | tags, labels, people framed at the size of objects | bars for "trapped" before the story earns them (B4 §4.2) |

## Budgets and saved choices

- Visual spine motifs within `motif_spines_max` for the film's format, plus at most `sound_motif_max` sound motif and `body_motif_max` body motif (B4 §3.2; FILM-10).
- Loud sets within `loud_sets_max` (B4 R17; FILM-11).
- `emphasis_3_rules`, `plant_emphasis_max`, `added_emphasis_per_beat_max`; more plant inserts in a scene than `plant_inserts_per_scene_max` reads as heavy-handed (FILM-09).
- Supporting motifs never above 2, except at their own payoff when it is a plot beat (B4 §3.2).

## The baseline is a strong answer

Most appearances sit at emphasis 0 in the scene's light, and most sets are quiet. A thing that literally exists in the story, does something, and only also resembles the theme needs no pointing: the audience gets the literal meaning first (B4 §2.3, P4). Depart only for a reason you can cite.

## Cliché traps

Tests: any-film, mood-word, stacking, sound-off (card 05).

- Borrowed meaning (a dove, a ticking clock, a caged bird, rain for sadness, an empty chair) fails the any-film test. Fix: a thing only this story has, with a detail from the text (B4 R5, R25).
- A familiar image the text does name (hands on glass) is kept only if it has a practical job and changes between appearances, and is played plainly: no slow motion, no score swell, no push-in (B4 R24).
- Telegraphing: a plant framed bigger than its payoff (B4 §13).
- A glowing object, lit from within or brighter than the faces (B4 §13).
- Wallpaper: a return that changes nothing. Each return changes the state, the owner, the neighbour in frame or what the audience knows (B4 R12).

## Reasons that fail and reasons that pass

- Fails: "An insert of the mint so the audience notices it." Passes: "MO-MINT is planted at 1 in the kitchen wide, placed, not inserted, because it pays off in the same scene (B4 §9.3, R6)."
- Fails: "Push in on the flask for tension." Passes: "PR-FLASK stays at 1 while Saye looks at it (line 399); its one 3 is saved for 'She looks at the flask inside the outline. Leaves it there.' (line 1406) (B4 §9.3)."

## Two worked examples

### The Catch: the mint and Saye's kitchen (SC10)

LOC-SAYE-KITCHEN is one of the film's two loud sets: its bareness is the point ("No photographs. No magnets on the fridge.", line 404), so it gets one establishing wide that shows it, and no object in it points to Nell (B4 §4.1, §4.3). MO-MINT is `single_scene`: every appearance falls in SC10 (B4 §3.3).

```
- appearance: SC10 "A pot of mint on the windowsill" | role: plant | emphasis: 1
- appearance: SC10 "Her face changes." | role: payoff | emphasis: 2
```

The tearing is a medium shot; then Iona's face, not the leaf, carries the payoff. The script marks the beat (the line, the chewing), so nothing is added (B4 §9.3, R23).

### The Long Places: oil to the knuckle

"The oil goes to the first knuckle of the thumb and no further." (line 15). One composition serves every appearance: lens, angle, light and hand position stay; only the hand and the oil level change. Four hands get the insert: Melek's, Nilay's filled past the knuckle in 1999 and Nilay's first round at 2 each, and last Emre's at 3, because his line turns it into recognition: "Past the knuckle. The greedy or the frightened." (line 1315). The red ribbon he lays down on the same turn stays at 2, straight after the lamp's 3 (B4 §10, Ex 11.5; `emphasis_3_rules`). No montage of hands with music, no dissolve from hand to hand, no flashback to Melek under his line: the same frame does the linking (B4 Ex 11.5).

## Self-check

- Is the theme a question and the opposition two nouns, read from PLAN?
- Was every motif harvested from the text, and every invention marked `invented` with a practical job (B4 R27)?
- Does each spine motif have a plant, a develop and a payoff, each a story point with a role and an emphasis?
- Are counts within `motif_spines_max`, `sound_motif_max`, `body_motif_max` and `loud_sets_max`?
- Is every plant within `plant_emphasis_max`, and every 3 within `emphasis_3_rules`?
- Does every symbolic thing have a practical reason to be there, and every sided thing an own side?

## Words for AI models

Works (B4 §14): concrete nouns with material, colour and size ("a small brushed-steel vacuum flask"); wear described physically ("a grey steel sill with one bright polished band along its edge"); position and size in frame to set the emphasis ("in the background, small, slightly out of focus" for 0); one saturated accent in a muted scene.

Fails: meaning words ("symbolizes", "motif", "foreshadowing"); mood words on objects ("ominous", "important"), which return glowing, centred, hero-lit things; named absences, which get drawn, so describe what is there ("a bare metal spring clip closed on nothing"); exact words on props (card 17). A model keeps a thing's state only with a reference picture for each state.

## Look up for more

B4 §3 (procedure, tests, scales), §4 (sets), §5 (props), §7 (translation table), §8 (R1-R27), §9 (The Catch's motifs), §10 (The Long Places), §11, §13, §14; A3 §5.3 (element categories); card 12 and B3 §6 (set plans); K11 and K14. Print one rule with `stage.py lib B4 R23`.
