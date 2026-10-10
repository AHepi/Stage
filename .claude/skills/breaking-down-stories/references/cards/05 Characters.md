# Card 05. Characters

Read whole at step 4. Step 5 reads only the part "State lines". "B5 R21" names rule 21 in B5's numbered rules (§9); "M" numbers are B5's mistakes (§13).

## The job

Design every person the film shows more than once so that a video model can rebuild them from words and every visible choice serves role, arc and theme (B5 §0.1). Work from evidence outward; write the fixed description (the words pasted unchanged into every prompt that shows them) last. Step 4 hands on CHARACTER records whose fixed descriptions fit `fixed_description_words`, whose principals (`tier: principal`, the main parts) differ by lineup, whose sided features have own sides and whose unstated skin tone and ethnicity stay open. Step 5 hands on STATE records, each with the line that causes it.

## Questions in order

1. **What does the story say?** Quote every line about face, body, clothes, marks and gestures into `evidence`; mark the rest `inferred` or `invented`, with a reason. Never "improve" a stated feature; keep inventions ordinary (B5 R23).
2. **What is the design thesis?** One sentence: must read as a first impression, and carry a contradiction the story later confirms or overturns, because of the arc (B5 §2.6, P2): Saye's grey control and her pot of mint.
3. **Does the lineup separate them?** The lineup is six word columns (height, mass, shape, value (how light or dark the whole figure reads), colour, tempo); principals differ in at least `lineup_columns_differ_min` columns (B5 R3, CRAFT-20), by height or mass first (B5 §2.2).
4. **What are the face's three largest distinguishers?** Large features survive a model's drift toward an average face: hair, facial hair, age lines, brows. A chipped tooth goes to reference pictures and inserts (B5 R21, R24).
5. **How do they move?** Write `movement` for home (the default way of moving), stress (under pressure) and break (when defences fail), each as body part, direction, speed and what stays still (B5 §5.7, M14).
6. **What are the psychological gesture and the one signature gesture?** The psychological gesture is one verb phrase for the inner pressure (Saye: a flat hand raised between two people); everyday gestures are small versions of it (B5 §5.2, §10.4). Quote the signature's line. Each return keeps the hand shape and framing and changes one thing (B5 R17). Minor characters get none (B5 §5.6).
7. **What status and distance?** Status (`status_play`) is how a person raises or lowers themselves against another, played, not held (B5 §5.3). High by stillness breaks once, leaning toward something (B5 R15). Distance: default and closest in metres, with the scenes that change them (B5 §5.5).
8. **What do they wear?** Answer B4's five questions first, in nouns and materials: choice, means and job, history, what the story did to it, what an institution put on them. Name the wear; change costume only at a turning point or a forced circumstance; keep one chosen thing through imposed clothes (B4 §6.1, R19; B5 R7).
9. **Not human?** Fear from silhouette, sound first and wrong proportions in a human plan; pity from damage suffered and care shown; every clue strange, never hidden; with no face, its thinking goes to head direction, hands and the order of its looks (B5 §6.2-§6.4, R10-R12).
10. **What stays open?** Skin tone and ethnicity the story does not state, with a marked placeholder (`skin_light: open` until the casting choice) and a small choice (B5 R19). Apparent sex and age band are always fixed (B5 §7.2 rule 7).

## State lines

A **state** is a person's or thing's costume, injury and condition from one change to the next (`CH-IONA.S03`); its **state line** is the phrase pasted after the fixed description in every prompt that shows that state (B5 §7.2 rule 4; K26).

1. **Start a state where the story changes it,** and quote the line in `cause`. The nurse dresses Iona's palm at line 498 ("dressing Iona's palm"), so the dressed state starts at that line, not at the top of SC11. An unexplained difference gets `origin: inferred` with the gap named, or a CHOICE (B4 §5.3; STATE-02).
2. **Copy the exit state into a `CONTINUOUS` scene exactly;** only a line inside the scene may change it (A3 R8; STATE-03).
3. **Write what is there,** in visible nouns and materials: "right palm bandaged in white gauze", not "hurt hand", never "no ring" (B5 §7.2 rule 8). No expression words.
4. **Rings, wounds and anything that changes live in state lines,** never in fixed descriptions (K26).
5. **Never store image sides.** Write own sides ("her own left hand"); code derives frame-left and frame-right per shot (blueprint 5.4 rule 8; SIDE-02).
6. **Give every sided feature a `side` item** with `own` (the side on the body itself) and `plot` (`yes` when the story depends on which side) (SIDE-01). Where the story leaves repeated damage unsided, put it all on one side and keep the other clean for a ring, as a small choice (B4 R14, B5 R8).
7. **In a mirror story, set `handedness` (`original`, or `reversed` once the element has turned) on every state.** A side the story states for an element shown mirrored is apparent: record the opposite own side, `origin: inferred`. "Saye's wedding ring. On her right hand." (line 436, era b, when the world is mirrored) is her own left (K03; SIDE-04). Card 16 holds the mirror method.
8. **Order wounds in story time:** fresh, reopened, dressed, bandaged; each state needs its own reference pictures (`pictures_needed`), because a model keeps a state only when every prompt restates it (B4 §6.1; B5 §7.3, §14).

```
### STATE CH-IONA.S03 Palm reopened
- element: CH-IONA
- from: SC09 | line: 370
- cause: 370 | quote: "her skinned palm opens"
- state_line: right shirt sleeve torn away, right palm raw and bleeding, dried blood on both hands, plain gold ring on her left hand
- side: palm | own: right | plot: yes
- side: ring | own: left | plot: yes
- handedness: original
- origin: story
> Own right for the palm is K26's default: the story does not say which hand.
```

## Translation menus with pitfalls

Pick at most one option per character from a row, tied to a line, object or action in this story; one column carries the meaning, the rest stay ordinary (B5 §8).

| Story meaning | Options | Pitfall |
|---|---|---|
| Competence | hands arrive before the eyes; worn, fitted work clothes | the heroic pose, chin up, shot from below (B5 M15) |
| Hidden knowledge | eyes go to text first; one hand out of sight (B5 R5) | the shifty-eyed villain |
| Control over grief | a still face; everything fastened; the break is one lean | all four at once: a poster (B5 §8 rule 1) |
| Cost paid | one mark that stays; guarding the hurt side | suffering make-up on every face (B5 M16) |
| Taken over by an institution | wristband, printed name, oversuit; one chosen thing kept | a symbol with no practical reason (B5 R25) |

## Budgets and saved choices

- `fixed_description_words`, principal and minor ranges (WORDS-05).
- Lineup: principals differ in at least `lineup_columns_differ_min` columns (CRAFT-20).
- One signature gesture per principal, at most once per scene outside a payoff scene (B5 §5.6, M6).
- One colour identity per principal, on one garment, not repeated at that saturation in the scene (B5 §4.2).
- Expression range, Detailed depth only: named faces tied to beats, written as muscle, eyes and head (B5 §3.3).

## The baseline is a strong answer

An ordinary body, clothes worn by this person's own life, and a still face while the line or the cut carries the beat are choices, not failures. A minor character needs one read and one key prop (B5 R20). Depart only for a reason you can cite (B5 R23).

## Cliché traps

Tests: the **any-film test** (would it fit any film with this theme?), the **mood-word test** (does the reason name only a feeling?), the **stacking test** (more than one signal saying one thing?), the **sound-off test** (does the body tell the beat with the sound off?).

- Adjective design ("mysterious, tough") fails the mood-word test. Fix: distinguishers and `movement` items (B5 M1).
- A lab coat for a scientist fails the any-film test. Fix: the five costume questions (B5 M2).
- Villain coding by scars, skin tone or body size: remove the moral role; does the design still stand? (B5 M3).
- Glowing eyes or chrome on a creature: remove what a famous robot would have (B5 R26).
- An expression in the fixed description ("composed") fights every other beat (B5 M18).

## Reasons that fail and reasons that pass

- Fails: "Saye is cold and controlled." Passes: "Saye's head stays still while her hands work quick and flat (line 408); her one break is a lean toward the screen (line 983) (B5 R15)."
- Fails: "Give Eli a scar to show his guilt." Passes: "Eli's half-smile lifts on his own left, a small choice, so 'on the wrong side of his face' (line 1696) pays off line 137 (B5 R2)."

## Two worked examples

### The Catch: CH-SAYE at step 4

Evidence: "DR SAYE, fifties, grey and tidy, fully dressed at four in the morning" (line 399); "quick flat hands" (line 408). Thesis: upright and fully fastened, dressed and waiting for years, her one living thing a pot of mint (B5 §10.4). Lineup: `height: average | mass: slight | shape: long | value: light | colour: grey | tempo: slow` (the body's tempo; the field `tempo` says "fast hands, slow body"). Nell shares her mass, shape and value; height, colour and tempo keep them apart, exactly `lineup_columns_differ_min` (B5 §10.11). Gesture: "She waits until Iona steps aside. | line: 481". `status_play`: `default: high | flips: SC17 "Leans in until her face is almost on the screen."`. Fixed description, no expression, her age in the story's word (B5 §7.2 rule 2; K26): "Dr Saye, a slim, upright woman in her fifties, short neat grey hair, a long pale lined face, thin straight brows, level grey eyes, a light grey cardigan buttoned to the collar over a white blouse." Her ring goes to the state line (K26).

### The Long Places: Melek, a prose portrait

"Seventy-eight, built like a doorpost ... knuckles like burl, a burn gone silver across the back of the right one" (line 47). A model draws a metaphor literally (a doorpost returns as wood), so turn each into shape, proportion and posture and keep the metaphor in the thesis (B5 R18, Ex5). The doorpost becomes tall, straight-backed, square-shouldered; the burl becomes large knotted knuckles. The burn is an own-right mark: a `side` item and a state line (K26). Gesture: "knocked twice, softly" on the sounding stone (line 419). Skin and hair colour stay placeholders (B5 R19).

## Self-check

- Is every descriptive line quoted in `evidence`, and every other choice marked `inferred` or `invented`?
- Do principals differ in at least `lineup_columns_differ_min` columns, with three distinguishers large enough to survive drift?
- Does every `movement` item name a part, a direction, a speed and what stays still, and the gesture its line?
- Is the fixed description within `fixed_description_words`, visible nouns only, with no expression, no real person, no ring and no wound?
- Does every sided feature have an own side, and every state a cause line?
- Are unstated skin tone and ethnicity open, and apparent sex and age band fixed?

## Words for AI models

Works (B5 §14): age in decades ("in her fifties"), build words, hair, facial hair, named garments with colour and condition ("faded blue work shirt, sleeves rolled to the elbow"), materials. Paste the fixed description unchanged, then the state line; a synonym is drift (B5 §7.2 rule 3; C3 §11). Say what is there: "a low domed head sunk deep between high shoulders", not "no neck".

Fails: left and right on bodies (fix the side in an edited still); words on clothes (card 17); "faceless"; theory words; famous names. High status becomes "stands still, head level, looks straight at her"; a half-smile becomes "only one corner of his mouth lifts", then check the side.

## Look up for more

B5 §3.2 (the face), §5 (how people move, status, distance), §6 (non-human characters), §7.2 (fixed description rules), §9 (R1-R26), §10 (The Catch's cast), §11, §13, §14; B4 §6 (costume); K03 and K26 in `references/library/00 Resolved conflicts.md`. Print one rule with `stage.py lib B5 R21`.
