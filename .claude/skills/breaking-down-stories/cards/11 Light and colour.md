# Card 11. Light and colour

Step 6 reads "Lighting plan" and "Colour script"; at Detailed depth step 7 reads "Per-scene light" and step 8 "Per-shot light"; chat apps read it whole. "B2 R10" is rule 10 in B2 §7 and "B2 P7" principle 7 in B2 §1; "B2 Ex2" is worked example 2 in B2 §10.

## The job

In Saye's kitchen the only warm light is the lamp Iona holds, and when Saye says "Nothing has happened to the mint." (line 466) the light does not change (B2 Ex2). Light decides what the audience may see: attention first, feeling second, beauty third (B2 P1). Step 6 hands on one LOOK per place and time and one VISUAL row per sequence; steps 7 and 8 record only what differs from them.

## Questions in order

1. **What does the story already say?** Every light, colour and darkness word is binding (B2 §5.1, R3; COVER-08). In prose, figurative light ("A question is a lamp you hold up on somebody", The Long Places, line 92) guides meaning only (B2 §5.1).
2. **What is each source, and where is it in the room?** (B2 P2)
3. **Which source reads as plain white?** (B2 §4.1)
4. **What stays dark?** (B2 P7)
5. **Whose face must be read?** Keep its eye light (B2 P8, R5).
6. **Can a story source change at the turn?** If not, hold the light (B2 R10).
7. **Is this sequence below the next peak?** (B2 R9)
8. **Do the motif colours survive this light?** (B2 §4.7, R15)

## Lighting plan

Example: `LK-SAYE-KITCHEN-NIGHT`: `main_light: Iona's lamp | colour: warm | quality: soft | from: TABLE`; `neutral_white`: the lamp; `contrast: medium_high`; `fill: low`; `stays_dark`: the room's corners and bare walls; `accent_allowed`: the mint's green (B2 §5.4; K22).

A **look** (LOOK record) is the light, colour and texture of one place at one time. Its **look block** is the two or three sentences pasted unchanged into every prompt there, within `look_block_sentences` and `look_block_words_max` (B2 §13.4). Fields, from B2's plan format (§5.3):
- `main_light`: the **main light** is the story source that lights faces in most shots: name it, its colour, its quality, and where it stands. **Hard** light comes from a source that looks small from the subject and gives crisp shadows; **soft** light from one that looks large (B2 P5). `from:` names a set-plan object or a wall (`north_wall`, `east_wall`, `south_wall`, `west_wall`, `ceiling`); code works out its frame side per shot and, in a mirror story, per era (card 16), so it flips lawfully with a mirrored picture (K03). With neither, the side stays `open`.
- `neutral_white`: the source that reads as plain white; every other source is warmer or cooler than it (B2 §4.1).
- `contrast`: `low` (gentle, open), `medium` (most drama), `medium_high`, `high` (one side of the face dark) or `extreme` (the shadow side goes black) (B2 §2.3).
- `fill` (`none`, `low`, `medium`, `high`): how far the dark side is lifted; little fill reads as secrecy or danger, much as openness (B2 §2.1).
- `stays_dark`: what the audience must not see yet (B2 P7).
- `palette`, `accent_allowed`: an **accent** is a small area of colour that stands out; keep the palette low in saturation around a motif colour, and keep that hue out of the set elsewhere (B2 R14, §4.7).
- `light_cue`: a **light cue** is a change of light the story causes, written as a story point (a scene and a quote) with its change and why (B2 §0.1).

Rules: a night interior takes one practical (a working lamp seen in frame) as its main light (B2 R1); a carried light lights what its carrier looks at (B2 R2); sourceless light only where the story leaves ordinary time (B2 R4); a machine's light dips once when the story says it falters, and never flickers otherwise (B2 R26); signals keep their real colours (B2 R19).

## Colour script

Example: The Catch opens at frame value 1, saturation 1 and extreme contrast in the tunnel, so contrast cannot climb at the climax; saturation and red against green are saved for the fire in scene 24, the only saturation 5 (B2 §8.5; K12).

A **colour script** is one VISUAL row per sequence, written before any shot, so the film's colour and light arc shows at a glance (B2 §8.1). Fields (B2 §8.2): `frame_value` 1 to 5 (how light the whole frame is, mostly black to mostly bright), `saturation` 1 to 5 (near grey to the film's most intense colour, used once or twice), `temperature` (warm, neutral, cool, mixed), `dominant`, `accent`, `main_light` (hard, soft, mixed), `contrast`, `exit` (how light leaves the sequence). At Detailed, `sub_row` items give scenes their own rows (K01, K13).

Steps (B2 §8.3):
1. Read each sequence's value change and the plan's peaks.
2. Write the colour logic: the story's oppositions and the motif colours the text supplies (B2 §8.4).
3. Assign peaks first, then the valleys lower: a sequence building to a peak sits at least one step below it in the component (saturation, contrast and so on) the peak spends (B2 R9). If the opening spends one component, the climax peaks in another (B2 §4.4).
4. **Monotony test:** no `colour_monotony_run` sequences in a row share frame value, saturation and temperature, unless the row says why (B2 §8.3; FILM-04).
5. Each motif colour appears only where its meaning applies.
6. Write each principal's colour arc in one line.

The film teaches its own colour meanings (B2 P4, R17); a warm-cool split names the opposition it stands for (B2 R16); a motif inverted once lands harder than one repeated (B2 R18).

## Per-scene light

Example: at scene 10's main turn, beat 7, the dial keeps `light: as_look`, because the script's point is that the world has not changed (B2 Ex2, R10).

The **dial** (SCENE `dial`) plans size, distance, height, light and sound for every beat. Its light stays `as_look` unless a story source can change at that moment: a door opens, a screen switches off, a lamp is set down, a machine falters (B2 R10). One light idea per scene, tied to the value change (B2 P10, §11). A cue falls on a turn and has a cause in the story (B2 §11); it never syncs to the line that states the point: offset it a beat, or let the world change it for its own reasons (B2 §12; FILM-09). A beat the script already marks gets no added light change (B4 R23; CRAFT-10), and a light change counts toward `signals_changing_per_beat_max` (CRAFT-19). The scene's one idea for light may be `holds_baseline`. Time passing inside one place moves in planned steps (B2 R22).

## Per-shot light

Example: scene 1's bolt-hole insert: the flashlight rakes in from frame-right across the empty bracket, everything beyond it black; on "She stays on her knees. One breath." (line 30) the beam stops and holds (B2 Ex1; K19).

Write SHOT `light` only where it differs from the look, else `as_look` (B2 §9). At Detailed add `dark` and `eye_light`: an **eye light** is the small reflection of a source in the eye that makes a face read as alive (B2 §0.1).
- Keep an eye light on anyone whose thought must be read (B2 R5). To show a character hiding something from another, hide a hand or object, not the face; lose the eyes only when the audience is kept out too (B2 R6, R7).
- The darkest shot keeps one readable element: a **rim** (a thin bright edge from a light behind), an eye light or a lit hand (B2 R23).
- Dark skin in low light: exposure and fill chosen for that skin, soft bounce and careful eye light, never just more front light; reject a take where darker skin goes grey, ashy or lost while lighter skin reads (B2 R24).
- Matte black shows by its rim against something lighter; an almost clear thing is lit from behind or the side (B2 R25, R25a).
- A face in a helmet gets its own light inside it (B2 R27); screen light matches the picture on the screen (B2 R29); the brightest costume keeps its fabric detail (B2 R28).
- The main light's side stays fixed to the set when the camera turns (B2 R20).

## Translation menus with pitfalls

Pick at most one per beat and tie it to a line, object or action (B2 §6):
- **Safety:** soft warm practicals, eye light on everyone. Pitfall: a greeting-card glow.
- **Threat kept hidden:** a mostly dark frame, light dropping away fast. Pitfall: too dark to read.
- **Truth revealed:** the flattest light available (B2 R11).
- **Institution:** flat top light. Pitfall: flickering tubes.
- **Unchanged world, changed person:** keep the light exactly as it was. Pitfall: a cue that "helps".
- **Care:** the carer holds the light. Pitfall: the halo.

## Budgets and saved choices

`look_block_words_max`; saturation 5 once or twice a film (B2 §8.2); one light idea per scene (B2 P10); `signals_changing_per_beat_max`; `added_emphasis_per_beat_max`, where a light change is added emphasis (B4 R23).

## The baseline is a strong answer

Static, the owner's eye height, a normal lens, room sound are choices, not failures; so is light held as the look. Depart only for a reason you can cite: a story source that changes (B2 P11, R10).

## Cliché traps

Test: can you name the lamp (B2 §12)?
- God rays in every interior. Fix: haze only where the place has dust, smoke or damp (B2 §5.2).
- Lightning at a revelation; a cold blue shift when the monster appears; flickering hospital tubes (B2 §12, §5.4).
- Teal-and-orange; candles for romance; a halo on the saint (B2 §4.8, §12).
- The AI house look: light shafts, rims, wet floors. Fix: name real sources in positive words (B2 §12).

## Reasons that fail and reasons that pass

- Fails: "Moody low-key light for tension." Passes: "The flashlight is the only source: Jude turns the tag into her beam to read it (line 16; B2 Ex1, R2)."
- Fails: "The light turns green on 'Drive.'" Passes: "The traffic light holds red a beat after 'Drive.', then changes by itself (B2 Ex3, §12)."
- Fails: a cue on "Not mint.". Passes: `light: as_look`: "Nothing has happened to the mint." (B2 Ex2).

## Two worked examples

### The Catch, scene 24 (the crisis)

The film's one saturation 5. Fire from the cabinet side and the faint green of her way home on the visor meet on Iona's face. At "She deletes the way home." (line 1412) the green leaves her face; when she fires, the cue is the loss of the white glare (line 1418), not darkness: the room still burns. Her eyes stay lit inside the helmet (B2 Ex4, R27).

### The Long Places, chapter VII (contemplative)

The finished room (line 587): the same small oil lamps, but a pale, unsooted ceiling bounces the flame, so the room is softer and brighter with no added source; the third shape sits at the edge of the falloff, with no rim and no eye light, because the story will not make it certain (line 597; B2 Ex6, R4, R23). Light stays source-true (D10 §2.2).

## Self-check

Yes or no (B2 §11).
1. Is every light, colour and darkness word covered?
2. Does every source have a colour, a quality and a place?
3. Does every cue fall on a turn, with a story cause?
4. Is one element readable in the darkest shot, and darker skin rendered richly?
5. Is this sequence below the next peak, and not a repeated row?

## Words for AI models

Works (B2 §13): named sources ("a mostly dark room lit only by one small lamp on the table"); colour on objects ("a small red tag on a grey steel gate"); direction as a result ("the left half of her face is in deep shadow"); "flashlight", never "torch" (K19). Fails: kelvin numbers, ratios, rig words, "practical", negatives ("no blue"), "cinematic lighting", named cinematographers, a light change inside one clip (make two clips).

## Look up for more

`stage.py lib B2 §5` (plans; §5.4 The Catch), `B2 §7` (R1 to R29), `B2 §8` (§8.5 The Catch's colour script), `B2 §9`, `§10` (Ex1 to Ex6), `§12`, `§13`; `B4 R23`; `D10 §2.2`; K03, K12, K19.
