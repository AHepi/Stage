# Digest B5: Character design for narrative

Source: `research/B5_character_design_for_narrative.md` (946 lines). Brackets: P# = principle (§1); R# = decision rule (§9, R1–R26); § = section; Ex# = worked example (§11); M# = mistake (§13). R1, R4, R13 are "consider" defaults; the rest are firm.

## 1. Scope

1. Deciding each character's look and movement (silhouette, shape, face, costume, color, damage, effort, status, proxemics) so every visible choice serves role, theme and arc; including non-humans that frighten first and earn pity later.
2. Writing it down so a performer, animator or AI model can reproduce it: bible entry, identity key, state lines, sheets, reference strategy.
3. Runs after breakdown (A2, A3) and motifs (B4), before shots (B1, B3), light (B2) and sheets (C2, C3); ends with all ten *Catch* characters.

**Terms** (§0.3). *Design thesis*: one sentence on what look and movement must communicate, and why. *Silhouette*: figure filled solid black ("outline" is kept for *The Catch*'s visor display). *Value*: lightness, not hue. *Distinguisher*: one of three features making a face unlike the rest of the cast. *Costume state*: one numbered version of clothes, marks and injuries; *costume plot*: all states by scene. *Damage ledger*: every injury, stain, tear or loss with start scene, side and changes. *Color identity*: the one hue and value belonging to a character. *Effort* (Laban): movement quality by weight, time, space, flow. *Psychological gesture* (Chekhov): one whole-body gesture summing up a want. *Status* (Johnstone): raising or lowering oneself moment to moment, played, not held. *Expression range*: named facial states tied to beats. *Clue ledger*: early details that explain a later reveal on rewatch. *Emphasis level* (B4 §3.4): L0 in frame, not pointed at, to L3 the shot is about it. *Mirror state* NORMAL/MIRRORED and *eras* A/B/C: C2 §7.3. *Identity key*: fixed 25–40-word block (minor 20–30) pasted unchanged into every prompt (C2's "look line"). *State line*: phrase appended after the key for the scene's costume state. *Hero portrait*: the approved head-and-shoulders image all others are checked against. *Placeholder*: value filled so generation can start, marked for the user.

## 2. Rules

**Foundations**
1. [P1, P2] If designing any character, then set up a surface a later choice can confirm or contradict, with one visible element against the dominant one, because a one-note design is a poster (Saye's grey control, her mint).
2. [P4, §2.1] If a design is proposed, then test it as silhouette and value at wide-shot size (who, doing what, what changed), because detail is for close-ups.
3. [P7, P8, M1, M14] If writing a design line, then write drawable specifics, and movement as body part, direction, speed, force, duration and what stays still, because "a hard life" or "moves sadly" cannot be performed or prompted.
4. [§0.1, R23] If a choice is not in the text, then tag it [design choice] or [inferred] with the reason; never contradict or "improve" a stated feature, and keep inventions ordinary unless they serve the thesis, because they compete with the writer's choices.
5. [R1, R18, M13] If the text gives one physical detail, then consider building from it; if it uses a metaphor, then convert it to shape, proportion and posture, metaphor kept in the thesis only, because models draw metaphors literally.
6. [§8] If using the translation table, then let one column carry a row's meaning strongly, trace choices to lines, and drop conventions showing the moral role at first sight unless overturned later, because stacking makes stock images.

**Figure and ensemble**
7. [P5, R3, §2.5, M4] If characters share scenes, then they differ in at least three of height, mass, dominant shape, value, color identity, tempo (principals sharing four or more: change one), because audiences and models confuse similar figures.
8. [R4, §7.2] If characters are blood relatives, then consider one or two shared face features with different builds and colors, and separate their keys by at least two large features, because kinship should read without merging.
9. [§2.2] If using shape language (circle warm, square stable, triangle danger), then use it for contrast and arc only, carried in one place (coat cut, shoulders, hair) on a real body; separate same-shape principals by height or mass first; give a character the story overturns the first-impression shape, because these are learned conventions.
10. [§2.3, §2.4, R14] If setting body and age, then ~7–8 heads, a build from the character's history, one signature body part, two or three age markers, a default posture with the scenes it changes, and a story cause for any looks-older gap, because unexplained ageing reads as makeup.
11. [R19, §2.7, M3] If the text is silent on ethnicity, skin tone or body type, then leave it open with a marked placeholder and ask the user; never code morality into ethnicity, body size, disability or facial difference, because these are casting decisions.
12. [R20, M15] If a minor character is a function, then one read and one key prop; if posing a protagonist, then the text's small economies, not a poster pose, because detail spends attention the story has not given and poster poses fit any film.

**Faces**
13. [P3, §3.1] If choosing features, then treat trait readings (babyface warm; heavy brow dominant) as conventions audiences apply in ~100 ms, never truth, because physiognomy is pseudoscience but the reading happens.
14. [R21, §3.2] If a character appears in many AI shots, then put the three largest distinguishers (hair, facial hair, age lines, face width, brows) in the key and carry small ones by references and inserts, because faces drift toward an average attractive face.
15. [§3.3, M8] If writing an expression, then muscle movement plus eyes plus head (FACS units allowed), never a bare emotion word; if line, eyeline or cut carries the beat, "still" or one movement, because context does much of the work.
16. [§3.1, §3.3] If a micro-expression is wanted, then flicker (~0.25–0.5 s, 6–12 frames at 24 fps) then cover, a crack the story explains, never a lie detector, because the lie-detection evidence is weak; a smile without AU6 reads forced (convention only).

**Costume, color, damage**
17. [P6, §4.1, M2] If designing costume, then start from a text line: work, means, garment history, chosen or imposed, fit for task, because costume is biography plus present state.
18. [§4.2] If assigning color identity, then one hue and value on one garment, rest muted, with a practical in-story reason, on nobody else in the scene at that saturation, value first in dark scenes (it may pass to an object), because scarcity keeps meaning.
19. [R25, M7] If an element only symbolises, then give it a practical reason or drop it, because unexplained symbolism talks down (white suit lit as equipment, no halo).
20. [§4.4, R8, M5, M16] If a character is damaged, then start it where the text does, keep its side, change it only on an event, keep a clean side for emblems, use only marks the text gives, because continuity depends on it.
21. [R9, R7] If a costume item becomes a prop, then design it once as the same object and state; if clothing is imposed, keep one chosen element visible (ring, book), because the audience recognises objects by color and shape, and the person must stay findable.
22. [R2, P9, R24] If a late scene depends on a side, then fix it early at L0–L1; if a detail reads only when pointed at, keep it out of the key, show it at L0 after first appearance, because change needs a baseline and repeated pointing turns cost into decoration.

**Movement**
23. [§5.1, §5.2, §5.4] If writing movement, then home, stress and break efforts (each convertible to instructions), a psychological gesture (verb phrase), departures from neutral and a resting tempo, because effort changes are visible beats.
24. [§5.3, R15, R16] If setting status, then a default plus flip beats (status is not power); stillness-held status breaks with one movement toward something; a joker under pain keeps face loose, body guarded, because change is measured against baseline.
25. [R5, R6] If a character withholds, then give it a place in the body (hidden hand, pause); if the arc is loss of control, then break one element at the turn, because subtext needs a visible home.
26. [§5.5] If a principal, then write default and closest distances with the scenes they change (zones in B3 §4.2), because the change carries the arc (sc29 chairs moved to the glass).
27. [§5.6, R17, M6] If a signature gesture is used, then one per principal (none for minors), once per scene except payoffs, same hand shape and framing with one change, because recognition precedes change.
28. [R22] If a movement must be exact (puppeteered hand, slow fall, mirrored reach), then Blender previs or control video (C4), because words control movement weakly.

**Non-human**
29. [R10] If a character must frighten then earn pity, then fear from silhouette, sound, scale, arrival; pity from damage suffered, care shown, cost paid, because fear built on cruelty cannot be reversed.
30. [§6.2] If frightening first, then dark against lighter; human plan, two or three wrong proportions; one face feature removed or relocated; sound before sight; in human rooms, before it shows care, arrival without travel (normal entrances on its ship); scale against door, bed, chair, because withholding the full view and how it moves sustains fear (*Alien*, Daleks).
31. [R26, M9, M17] If an element fits a famous robot or creature (light bar, glowing eyes, chrome, pistons, teeth, skull head), then remove it, because a familiar monster frightens only as a quotation.
32. [§6.3, M11] If earning pity, then damage suffered, care before explanation, cost paid, scale inverted at reveal, one human-readable gesture; keep the small being alien, not plush, because pity must come from behavior.
33. [R11, §6.4, M10] If a reveal is coming, then ledger every clue, strange not hidden, planted at L0–L1, because a fair reveal rewards rewatching.
34. [R12, R13] If a character has no face, then thought via head direction, hands, order of looks; for a small creature, consider echoing a human gesture from the film, because the echo does a face's work.
35. [§6.1, §6.5] If sourcing or staging a non-human, then real animals over films' aliens; glass, haze or water for long looks; for a suit worked by a small body, two tempos, a dead-weight tell, one very tall, thin, slow performer (never two people or bulk), because movement matters as much as sculpture.

**AI consistency**
36. [§7.2] If writing an identity key, then 25–40 words (minor 20–30): name, age read, build, skin placeholder, hair, distinguishers, one constant costume anchor, one large mark; visible nouns and adjectives only (no meaning, backstory, movement or expression words); pasted unchanged, word order frozen; no two share hair color + age band + build; apparent sex and age band always fixed; state what is there, not what is absent, because synonyms and open attributes are drift.
37. [§7.2 r4] If costume changes, then change the state line, never the key, because a changing item makes a fixed key wrong somewhere (Iona's ring is hidden by gloves in C4–C5).
38. [§7.2 r5] If a side matters, then record own left/right in the NORMAL design, convert for prompts (facing camera: own right = frame left; back to camera: frame right; MIRRORED: swap first), then generate as designed, flip or edit, check by eye, because models place sides at random.
39. [§7.4] If attaching references, then portrait when the face is readable (one-reference tools: face > ~1/10 frame height), else the costume-state image; several characters: one each, named in reference order, else composite or repair; faceless: silhouette and scale sheet, because each generation is a new artist.
40. [§7.3, §7.4] If a MIRRORED or damaged version is needed, then flip or edit an approved image (never prompt "mirrored"; "same person, same pose, now with ..."), recheck sides after flips, attach only approved images, because flipped errors spread.
41. [P10, §7.5] If planning generation, then budget rejects, plan inserts from edited stills for hands, teeth and marks, and expect flipped sides, merged look-alikes and non-humans regressing to robot, diver or glowing jellyfish (maybe a LoRA), because keys reduce variation, not stop it.

## 3. Breakdown fields

| Level | Field | Meaning | Values / example |
|---|---|---|---|
| film | `lineup` | Contrast check, one row per character | height, mass, dominant_shape, value, color_identity, tempo |
| film | `casting_open` | Unstated casting types, with placeholders | "skin tone: open" |
| character | `tier` | Entry depth | `principal` / `minor` |
| character | `role`, `arc`, `turning_scene`, `evidence` | One line each; quoted text lines | "sc24" |
| character | `design_thesis`, `one_image` | Thesis; the poster frame | "sc01: hand flat on ropes" |
| character | `face_spec`, `distinguishers` | 13 fields (§4 P3); three largest features | "straight low brows, ..." |
| character | `body_silhouette`, `signature_body_part` | Height, build, posture, dominant shape | "~1.68 m, vertical rectangle; hands" |
| character | `age_read`, `age_gap_cause` | Read age; cause of any gap | "no sun, nineteen years" |
| character | `costume_states` | Numbered, with scenes, garments, condition, color | `C1` sc01–sc06 |
| character | `damage_ledger` | Item, side, starts, changes, ends | "palm; right; sc06; sc09, sc11; sc30" |
| character | `color_identity` | Hue + value; where forbidden | "faded mid-blue; nobody else" |
| character | `movement_signature` | 8 fields + arc (§4 P4) | home/stress/break efforts |
| character | `psychological_gesture` | Verb phrase | "flat hand raised between two people" |
| character | `status_default`, `status_flips` | Default; flip beats | "high; drops once, sc13" |
| character | `proxemics_default`, `proxemics_closest` | Metres + scenes | "~1 m; touching" |
| character | `signature_gesture` | Exact script line | "Lays her hand flat on the ropes ..." |
| character | `expression_range` | 5–8 (minor 2–3), scene + movement | "sc13: lips parted, eyes drop" |
| character | `mirror_state_by_era`, `side_features` | Per era; own side + on-screen side | "smile own left; frame right facing camera" |
| character | `identity_key`, `state_lines`, `references` | Frozen key; phrase per state; approved images | portrait, turnaround, expressions, hands_marks, states, scale |
| character (non-human) | `clue_ledger`, `tempo_modes`, `arrival_rule` | Clue rows; care/task tempo; travel allowed | "no travel in human rooms" |
| scene | `costume_state_by_character`, `signature_gesture_use` | From plot and ledger; count | max 1 unless payoff |
| beat | `expression_state`, `effort`, `status_flip`, `proxemic_change` | Range entry; home/stress/break | `stress: punch` |
| shot | `state_line`, `side_features_frame`, `mark_emphasis` | Current state; sides in frame terms for the era; emphasis of small marks | `L0` |
| prop | `costume_origin` | Costume item reused as prop, same object and state | sleeve strip, Eli's shoe |
| generation job | `identity_key`, `state_line`, `references`, `reference_order`, `flip_after`, `side_check` | Prompt assembly and checks | portrait if face > ~1/10 frame |
| previs job | `exact_movement`, `performer_spec` | Movement too exact for words; stand-in | "one very tall, thin, slow performer" |

## 4. Procedures

**P1. Order of work** [§0.1]: (1) quote every line on face, body, clothes, marks, gestures, movement; (2) role and arc; (3) design thesis; (4) whole figure against the cast; (5) face spec, then expression range tied to beats; (6) costume states and damage ledger; (7) movement signature; (8) non-humans: §6 with clue ledger; (9) bible entry and key; (10) checklist and mistakes, then hand to C2 for sheets. Tag [design choice] / [inferred] throughout.

**P2. Design thesis** [§2.6]: "*[Character] must read as [first impression], and carry [the contradiction or clue] that the story will later [confirm / overturn], because [theme or arc reason].*" Then name the one image (pose, costume state, expression); if you cannot, the design is unfinished.

**P3. Face spec** [§3.2], fixed order: 1 age read (and why older/younger); 2 head and face shape; 3 bone structure; 4 eyes; 5 brows; 6 nose; 7 mouth (resting set, teeth); 8 skin (tone often casting); 9 hair (incl. parting side); 10 facial hair; 11 marks with side; 12 asymmetries in own left/right; 13 three distinguishers.

**P4. Movement signature** [§5.7], one line each: 1 centre; 2 home, stress, break effort; 3 tempo in plain terms; 4 default posture (spine, shoulders, head, weight foot); 5 hands at rest; 6 eyes on entering; 7 signature gesture with exact line; 8 what never moves; then arc with scene numbers. Laban actions: strong = punch (sudden, direct), press (sustained, direct), slash (sudden, indirect), wring (sustained, indirect); light = dab, glide, flick, float in the same order; flow bound or free. Conversion: glide → "palm flat, hand slides slowly along the rope, even pressure, no pauses except where she checks, eyes ahead".

**P5. Character bible entry** [§7.1], exact fields and order:
```
NAME / ROLE:          narrative role in one line
ARC:                  start state -> end state, with the turning scene
DESIGN THESIS:        one sentence (Section 2.6)
ONE IMAGE:            the single frame that carries the thesis (Section 2.6)
EVIDENCE:             quoted lines from the text about look and movement
FACE:                 the 13-field face specification (Section 3.2)
BODY / SILHOUETTE:    height, build, proportion, posture, dominant shape
COSTUME BY PHASE:     C1, C2 ... with scenes, garments, condition, color
DAMAGE LEDGER:        rows (Section 4.4)
COLOR IDENTITY:       hue + value, and where it must not appear
MOVEMENT SIGNATURE:   the 8 fields (Section 5.7) + arc of movement
PSYCHOLOGICAL GESTURE: one verb phrase
STATUS:               default, and the beats where it flips
PROXEMICS:            default and closest distance, with the scenes where they change (Section 5.5)
EXPRESSION RANGE:     5 to 8 states (minor characters 2 to 3), each tied to a scene
MIRROR STATE:         NORMAL/MIRRORED by era (C2, Section 7.3), with every left/right feature
IDENTITY KEY:         25 to 40 words, fixed
STATE LINES:          one short phrase per costume state
REFERENCES:           list of approved images: portrait, turnaround, expressions, hands/marks, states
```
Minor characters fill every field in one line. Example key (Iona, 32 words): "Iona, a lean, strong woman in her late thirties, weathered fair skin, dark brown hair in a low knot with loose strands at the temples, straight low dark eyebrows, deep-set grey-green eyes."

**P6. Ledger columns**: damage `Item | Side | Starts | Changes | Ends` [§4.4]; clue `Clue | First shown | How to show it (emphasis level) | What it means on rewatch` [§6.4]; lineup `Character | Height | Mass | Dominant shape | Value | Color identity | Tempo` [§2.5].

**P7. AI casting** [§2.7]: 6–12 candidate portraits from the key alone, neutral light; user picks against the thesis, for what the face does at rest (reject young, glossy faces that erase age or thinness); winner becomes hero portrait; if none fits, edit the key's words.

**P8. Sheets** [§7.3, working practice]: hero portrait; turnaround as separate images per view, neutral pose arms slightly out, flat light, mid-grey ground, chest-height camera, ~50 mm, whole figure, first costume state (figure: plus a rim-light view); expression sheet labelled with scene and movement text; hands-and-marks sheet labelled "own left/right"; one full-body image per costume state (damage edited from the previous approved image); non-humans: scale sheet (door, bed, Iona). Approve before use.

**P9. User review** [§0.2]: user reads only thesis and key, corrects in plain words ("Saye is not cold, she is frightened"), decides every [design choice].

## 5. Checklists

**Per character** [§12]: role, arc, thesis, one image; look lines quoted; unstated choices tagged; silhouette distinct at wide size; no two principals share ≥4 lineup columns; face spec, three distinguishers; every left/right feature with own and on-screen side per era; expressions tied to beats, as movement; costume states numbered, damage ledger complete; color identity unrepeated at that saturation in a scene; movement signature complete with quoted gesture and arc; psychological gesture, status flips, proxemics; stereotype check; casting placeholders marked; non-human: clue ledger, fear and pity rules; key within length, visible only, unique, no expression words, negatives, famous names or changing items, gender and age band fixed; state lines; hands-and-marks sheet (scale sheet for non-humans).

**Per shot** [§12]: costume and damage match the ledger; side features correct for the era; movement uses home, stress or break effort as the beat needs; key pasted unchanged with current state line.

**Mistake scan** [§13] (with the spot test): M1 adjective design (nothing drawable); M2 job-label costume (fits any story); M3 villain coding (remove the role: still justified?); M4 clone cast (lineup); M5 damage breaks (shots vs ledger); M6 overused signature (>1 per scene); M7 symbolic costume (not chosen or issued); M8 over-acting (no still faces); M9/M17 monster clichés (resembles a known creature); M10 unfair reveal (clue with no earlier scene); M11 cute reveal (would sell as a plush); M12 paraphrased keys; M13 metaphors; M14 movement as feeling; M15 heroic posing; M16 suffering make-up; M18 expression in key.

## 6. Saying it to AI models [§14]

Judgment, not tests; C2 and C3 hold tool details. Metaphors are converted first (Ex5).
- **Works:** age in decades; build words; hair color, length, style; facial hair; named garments with color and condition; simple accessories; materials ("matte black", "glass", "translucent"); framing and light words.
- **Partly:** facial geometry (averaged away without references); subtle expressions (one-sided smiles become full); scale (needs a door in frame); costume states (restate every prompt).
- **Fails:** left/right (flip or edit, check); text on costumes; "faceless" (gives mask or face); negatives ("no eyes"); theory terms (Laban, "shape language", "arc", "symbolizes"); famous names; "humanoid" (stock robots); "narrow band of pale light" (scanner bar); "deep-sea" (anglerfish teeth); "comb jelly" (rainbow glow; reference images only).
- **Say instead:** glide → "moves slowly and smoothly, her hand sliding along the surface"; punch → "one fast, hard swing"; bound flow → "tight, controlled movements that stop sharply"; float → "drifts slowly, limbs loose, as if underwater"; high status → "stands still, head level, looks straight at her, does not fidget"; low status → "glances away and back, small nods, touches his face"; hidden hand → "one hand stays behind the other man's back, out of view"; half-smile → "a small lopsided smile, only one corner of his mouth lifts" (check side); pale strip → "behind the clear face cover, a soft pale strip like wet tissue slides slowly across, disappears, and slides across again"; head low → "its domed head sits deep between high shoulders; the top of the head is level with the tops of the shoulders"; frightening → light and framing ("seen from low, lit only along its edges, filling the doorway"); pitiable → behavior ("it shrinks to the far side of the glass"); almost clear → "glass-clear and soft, faint milky shapes inside, dim, lit only where light passes through it".
- **Motion:** image-to-video from an approved still (Ex1: "the flat hand slides slowly down the rope, pauses, slides again; the head does not move"); flip stills, never prompt "smile on the wrong side" (Ex2).

## 7. The Catch

**Conventions** [§10]: sc01–sc30; eras A to the black after "CLACK" (sc06), B to Iona's own turn (sc27), C sc28–sc30. Skin tones are C3 placeholders. These entries supersede C3's illustrative keys.

**Characters** (keys in §10.x):
- **Iona**: ~1.68 m, lean, vertical rectangle; faded mid-blue (no one else; blanket "OSTREL" in navy), then suit white; gesture: pressing a flat hand to feel whether it will hold; never flips. States C1–C6 start sc01, sc06, sc11, sc18, sc28, sc29: work clothes (ring own left, earpiece left); torn right sleeve, skinned right palm, Jude's blood; pyjamas, wristband, bandage; white suit, engine between shoulders like the figure's cell, vessel from sc25; helmet on; tent. Tooth chipped upper left, out of key. Turning scene sc24.
- **Jude**: ~1.85 m, rounded rectangle; olive; open hand holding then letting go; MIRRORED in C. Right-shoulder wound [inferred from ring on the "good hand"]; appendix scar own right (script), on his left in C; C6 state line in on-screen terms; generate as designed and flip.
- **Eli**: ~1.78 m, thin angular lines (instability, not villainy); charcoal; hand closing on something and drawing it behind the body; MIRRORED in C. Smile and parting own left; one brown lace-up on the right foot; shares Iona's brows and eyes, separated by beard and hair.
- **Saye**: ~1.65 m, narrow vertical; light grey and white, mint accent; flat hand held between two people; MIRRORED in B (ring on right). Clothes never loosen; the sc17 lean is her change.
- **Nell**: small, very thin; faded sage (full strength in the sc17 photo); holding something to the chest while reaching for a handhold; MIRRORED in B.
- **Minor**: guard (navy, lanyard card in state line), nurse (pale grey-green, black hatch gloves, placeholder woman), technician (pale grey, placeholder man); MIRRORED in B.
- **Figure**: ~2.4 m, block with sunken dome, very large hands, no claws; matte black like puck, engines, cells; face cover in the top of one front hatch [inferred]; pale strip soft, cycling, never red, same tissue as the animal; latches and seam only in rim light. States S0–S5: intact; cracked jet (sc16); patch and cell (sc20); strip dims (sc23); chest open (sc25); empty, leaning. Pump sc15, 16, 25, 27, 28, last line. No travel sc15–16; walks from sc20. Stage sc16 and sc21 approaches at the same distance and height. NORMAL in B; MIRRORED on world screens (sc17).
- **Animal**: ~15 cm, glass-clear, thread-fine limbs, no visible eyes, no blue; forearm-length vessel of dark water, frost in warm rooms; limb gestures echo Iona's grip and palm; states V1–V5 (sc25 mount to sc30 cloth); NORMAL in B and C.

**Lineup** [§10.11]: Eli–Saye share grey on purpose; Iona–Eli share brows and eyes; Saye–Nell closest pair (widen with posture and white vs grey hair).

**Props and damage**: sleeve torn sc06 → Jude's wound → cut away sc10 → "Jude's dressings" sc17 [inferred] → collection room sc21 → vessel sc25 → growth sc30. Eli's shoe lost in the cage sc06 at L0 = sc21 "One shoe" (Ex4).

**Gestures**: flat hand (Ex1): sc01 L2 insert, right hand, ~30 cm in 2 s, two pauses, eyes off hand; sc12, sc17 on glass; transfers to figure (sc25) and Jude (sc29). Half-smile (Ex2): sc03 two-part beat; sc28 weaker, apparent right, made by flipping the sc03 still.

**Figure clues** [§6.4]: low head (sc15, L1); cycling strip (L2); pump (sound L2); white jet (sc16); frost, latches, seam, late-settling hands (L0) [design choices]; raised arm (sc16); cell and handmade air fitting (sc20); cup caught without looking, strip dims (sc23). Ex3: sc15 cut in, silhouette on lighter door, pump before strip [design choice against script order]; tablet feed in C3's security look.

**Prose** (Ex5, *The Long Places*): Melek's metaphors become "an upright, square-shouldered woman in her late seventies, very short nails, large knotted knuckles, a pale shiny burn scar across the back of her right hand"; hands sheet first; hold ~6–8 s after the knock.

**User decides** [§15]: casting types; marriage; sides (Iona sleeve and palm right, tooth upper left, earpiece left; Jude right shoulder; Eli smile and parting own left, shoe right foot); Eli's shoe; Nell's ship clothes; how much animal and whether eyes; figure height; Eli–Saye grey; sleeve's route (decides if sc10 shows it bagged); nurse and technician genders; face cover in the hatch; flap as animal tissue [interpretation].

## 8. Conflicts and open questions

- **Key length**: B5 minor 20–30 words; C2 and C5 say 25–40 for all.
- **State numbering**: B5's C1..C6 collides with file names and era C; C2 uses S1..S6 with different counts (Eli 5 vs 6; figure S1–S6 vs S0–S5; animal S1–S4 vs V1–V5). Pick one.
- **C3 keys superseded**: Saye "charcoal cardigan" (B5 light grey); figure "~2.5 m armoured diving suit" (B5 ~2.4 m, warns of "diver" regression; C2 lists "armor" as a trigger); animal "comb-jelly-like" (dropped); C2's "glass-squid-like".
- **Candidates**: B5 6–12 portraits; C2 ~8.
- **Low angle**: B5's "seen from low" vs B1 allowing the figure's looming frame once.
- **Hands on glass**: B3's glass ladder (sc3, 11, 12, 17, 25 limb, 26, 29; "add none") vs B5's flat-hand chain (adds sc01 rope insert at L2 and the figure's hand on its own chest, sc25); agree which are inserts.
- **Color ownership**: B2 flags overlap with B4 and B5 costume color.
- **Negation**: B5 bans negatives in keys; C2 image prompts use "no text"; C3 lints negation.
- **Sides**: A3 R14 states sides in every prompt; B5 and C2 rely on frame terms plus flipping and checks.
- **Unverified**: Bancroft's hierarchy and shape wording; Johnstone and Lecoq wording (incl. "seven levels"); *Illusion of Life* on silhouettes; Chekhov's imaginary centre; *Inside Out* shapes; Hybride; Porter and ten Brinke title; Zebrowitz; the Google Cloud quote. Sheet practice and §14 are judgment.
- **Interpretations**: marriage; wound side; face cover in hatch; flap as tissue; the cup catch.

## 9. Section map

- **§0** order of work, user guide, glossary. **§1** ten principles.
- **§2** figure: silhouette; shape table and restraint rules; proportion; age, posture; lineup; thesis; stereotype, AI casting.
- **§3** faces: evidence (Todorov, Kuleshov, FACS, micro-expressions); 13-field spec; expressions as movement, AU table.
- **§4** costume: Landis questions; color identity; costume plot; damage ledger; imposed costume.
- **§5** movement: Laban efforts and actions; Chekhov; Johnstone; Lecoq; proxemics; signature gestures; 8-field signature.
- **§6** non-human: precedents (*Alien*, Daleks, *Pan's Labyrinth*, *Arrival*, *Elephant Man*, others, deep-sea animals); fear and pity rules; clue ledger; suit worked by a small body.
- **§7** AI: entry template; key rules 1–8; sheets; references; limits.
- **§8** translation table (12 meanings × face, body, costume, movement) and usage rules. **§9** R1–R26.
- **§10** entries for all ten characters; lineup. **§11** Ex1–Ex5. **§12** checklist. **§13** M1–M18. **§14** AI phrasing. **§15** open questions. **Sources**, verified and unverified lists.
