# Card 12. Staging and composition

Step 4 reads "Set plans"; step 6 "Visual structure"; step 7 (Standard) "Stations and configuration"; step 8 "Frame rules"; chat apps read it whole. "B3 R3" is rule 3 in B3 §7.2, "B3 P2" principle 2 in B3 §1, "B3 Ex1" worked example 1 in B3 §9.

## The job

In Saye's kitchen Iona walks between Saye and Eli ("Iona moves between her and Eli.", line 476), and Saye wins by standing still until Iona steps aside (B3 Ex1, R3). Bodies are read before words: where people stand, how far apart, who moves (B3 P1 to P3). Step 4 hands on set plans; step 6 each sequence's visual structure; step 7 the staging, marks, moves and setups; step 8 each frame's placement, glass and dominant.

## Questions in order

1. **Where is everything?** A set plan, anchor and exits (B3 §6, §5.1).
2. **Who holds power, and who moves?** (B3 §4.2, R3)
3. **How far apart, and does it change only with a value?** (B3 P2, R2)
4. **Does the configuration change on the turn?** (B3 §4.9, R1)
5. **With three or more: the engaged pair, the silent third, the pivot?** (B3 §4.4, R5)
6. **Where is the line, and the camera's side of it?** (B3 §5.2)
7. **What does each frame show first?** (B3 §3.1)
8. **Is there a barrier, and whose side is the camera on?** (B3 R11)

## Set plans

Example: `LOC-SAYE-KITCHEN`: `size: [6.0, 3.6, 2.5]`, `origin_corner: south-west inside corner`, `axes: +x east, +y north`, `wild_walls: west wall`; `TABLE | at: [2.8, 1.8]`; marks `IONA_MARK | at: [2.8, 2.55]`, `SAYE_MARK | at: [2.8, 1.05]`; anchor: the table with Jude on it (B3 §6.3; K22).

A **set plan** is a top-down map of a place in metres, which code turns into frame positions, eyelines and previs, the grey 3D stand-in renders (B3 §6). Step 4 writes one for every place used by a shot likely to need previs level `previs_plan_level_min` or more, a reflection or glass shot, or three or more people in one space; at Detailed, for every place. Fields:
- `size`, `origin_corner`, `axes`: metres from a named corner, +x east, +y north.
- `wild_walls`: a **wild wall** can be removed so the camera can stand where it was (B3 §0.1).
- `object`: NAME, `at`, `size`, `base`, `material`, `meaning` (what it means in the story), `furniture`.
- `mark`: a **mark** is a named position where a person stands, sits or lies at a given beat (B3 §0.1).
- `anchor`: the **anchor** is a fixed object seen in most shots, keeping the geography clear (B3 §5.1); `exit` items with `leads_to`.

Rules: each person gets a mark and a facing target, a name or point, never "left" (B3 §6.3). A distance the prose gives as a feeling becomes a named mark, reused whenever the phrase returns (B3 P10, R19). `plan_orientation` is the orientation of the place's first appearance on screen; code derives the mirrored plan (x becomes width minus x; a facing angle θ becomes 180° minus θ), so never hand-edit a derived plan (B3 §5.4; K02). Claim no frame position code has not projected (B3 §11; GEOM-06).

## Visual structure

Example: sequence 3, the wrong world (scenes 7 to 10): limited and flat space, horizontals, affinity in camera and space, so the only contrast is the reversed world itself (B3 §2.7, P5).

**Visual structure** is Bruce Block's plan for how the picture rises and falls with the story (B3 §2). Every picture is built from seven **components**: space, line, shape, tone, colour, motion, rhythm (B3 §2.1). **Contrast** (difference within a component) raises visual intensity; **affinity** (sameness) lowers it (B3 §2.2). Space is **deep** (lines running away, motion toward the lens), **flat** (frontal planes, motion across), **limited** (frontal planes stacked in depth, nothing moving toward the lens) or **ambiguous** (size and position unreadable) (B3 §2.3).

Each VISUAL record writes `space`, `component` items (`plan: hold`, `progress` or `contrast`, with `why`) and `counterpoint` (B3 §2.6):
1. Read the sequence's scene intensities and the plan's peaks, the film's maximum moments.
2. For each component, one sentence: what it does in quiet stretches, at peaks, at the end.
3. Name any **counterpoint**: calm picture under a story peak, justified in one sentence (B3 §2.5).
4. Name choices kept for the peaks only.

At a peak, raise contrast in no more than two components (B3 R7; FILM-05); after a high-contrast sequence, strong affinity (B3 R8). A limited space turns deep when someone walks toward the lens: save that for an intrusion (B3 §2.3).

## Stations and configuration

Example: scene 10's stations are the table, the counter with the flask and phone, and the space between Saye and Eli; at beat 10 Iona moves into that space, at beat 11 she steps aside (B3 Ex1).

SCENE `staging` is one line placing everyone, or "staging assumed" when the story is silent (A2 Step 9). A scene over `stations_needed_above_beats` beats names `stations_per_scene` **stations**: marks each tied to a part of the scene, the route between them part of the story, toward the door for escape, toward the other person for appeal (B3 §4.7).
- The **configuration** (who stands, sits, faces whom, how far apart) changes on every turn, written in BEAT `change`; identical before and after means the turn is missed (B3 §4.9, R1).
- Between turns a body moves only for a want or task you can name; distances change only when a value's charge changes (B3 P2, P3, R2).
- The one holding power stays still while the other moves; standing up on a turn takes the scene; **interposition**, stepping between two people, plays in one wide that sees all three (B3 §4.2, R3, R4).
- Distances in metres, with Hall's zones: intimate, personal, social, public (B3 §4.2).
- Three people: per beat name the **engaged pair** (the two in the exchange) and the **silent third**; the **pivot** stands between the others and moves the line with a turn of the head; keep the silent third visible when their reaction matters (B3 §4.4, R5; A1 R5; CRAFT-24). Four or more: subgroups, one master side (B3 §4.5).
- With a set plan: `start` per character (mark, facing, posture); MOVE records, each a **floor-plan move** with beat, from, to, timing, facing and why; SETUP records, each a **setup** (a camera position) with its lens and side of the line. A move the story does not write is `origin: invented`, in `additions` (B3 §10.2); one it implies is `origin: inferred`, listed too. Two people side by side in a car: the line runs through both heads, across the car; keep the cameras on its front side (through the windscreen).
- **The line** (line of action) runs through the engaged pair; the camera keeps one side per part and crosses only inside a shot or on a beat that reverses the relationship (B3 §5.2, R16). One staged wide can replace several singles (B3 §4.1).

## Frame rules

Example: SC10-SH080 puts Iona frame-left facing right and Saye frame-right facing left, each raising the hand nearest the camera, with Jude, the lamp and Eli on the centre line (B3 §8.2; K07).

- Name the **dominant**, what is seen first; at least three attention cues agree on it, and none of face, motion, brightest area or sharpest focus points elsewhere (B3 §3.1).
- Thirds is the neutral baseline; centre, edge or symmetry needs a story reason, and symmetry belongs to ritual, confrontation and mirrors (B3 §3.2, §3.3, R12).
- **Lead room** (space in front of a face, the way it looks) about two-thirds of the width; **headroom** with the eyes on or just above the upper third line; **short-siding** (facing the near edge) only where something is behind or cut off (B3 §3.5). Paired singles mirror each other (GEOM-01, GEOM-08).
- For waiting or dread, leave the empty side of the frame toward where the absent person would come (B3 §3.4).
- One frame within a frame (a door, window or screen framing part of the picture) and one expressive device (a barrier, reflection or short-siding) per shot (B3 §3.7, R25); a foreground object frames, blocks or comments, or goes (B3 R13); a short shot keeps the dominant where the last one was (B3 R14).
- Keep the camera on its side of the line: an exit frame-right enters frame-left; a change of direction shows inside a shot (B3 §5.2; GEOM-03, GEOM-07). Directions describe the final picture, after any flip (B3 R22).
- Every pane in frame gets `glass`: state `clear`, `marked`, `reflecting`, `screen` or `broken_open`; camera `through`, `along` or `angled` (B3 §8.1). A reflection shows only against something darker: to lay A's reflection over B, put the camera on the line through A's mirror twin and B (B3 R28); clear glass needs the camera's side darker (B3 R29). Facing frame-right shows the right side, so the right hand is nearest the camera (B3 §8.2; card 16).

## Translation menus with pitfalls

At most one composition and one staging choice per moment (each row: composition / staging), preferring staging, tied to an object, line or action (B3 §7.1):
- **Control:** symmetry / fixed marks. **Isolation:** negative space / beyond social distance.
- **Power held:** height / holds still, holds the doorway.
- **Divided:** a surface division / a barrier. **Reconciliation:** the gap closed by both.
- **A world turned over:** an earlier frame repeated, one thing reversed.
Pitfall: all at once, the stock version of every film.

## Budgets and saved choices

`stations_per_scene`; `acting_characters_per_clip_max` (CRAFT-15); one major move per AI clip (B3 R21); hands on glass only where the script has them, same insert framing, one thing changed each time (B3 §8.3, R20, R27); perfect symmetry only as a saved choice (B3 §2.7).

## The baseline is a strong answer

Static, the owner's eye height, a normal lens, room sound are choices, not failures; so are thirds, matched singles and marks held between turns. Depart only for a reason you can cite (B3 P5, §4.1).

## Cliché traps

Test: would this fit any film (B3 R26)? Fix: the script's own object, carried by one department (B3 §11):
- Stand-and-deliver singles in a scene with a turn; moves "for variety".
- Rain on the window, a wilting plant, a ticking clock, bars of blinds, a stare into a mirror (B3 R24).
- The barrier marked in every shot; symmetry as style; hands on glass with music.

## Reasons that fail and reasons that pass

- Fails: "She crosses to the window for variety." Passes: "IONA between Saye and Eli at SC10-B10; why: 'Iona moves between her and Eli.'" (B3 R4)
- Fails: "Symmetry for a striking image." Passes: "`RC-01`: 'like a woman and her reflection' (line 428)." (K07)
- Fails: "They sit apart to show distance." Passes: "GOOD_DISTANCE, 2.4 metres, reused whenever 'the good distance' returns." (B3 Ex5, R19)

## Two worked examples

### The Catch, scene 13 (three on one side of the glass)

Jude, in bed between the siblings, is the pivot; the three face the monitor they talk through, and the master looks through the glass from Saye's side. At "Looks at her brother. Not at Jude." (line 742) the line swings to Iona and Eli, over Jude. "All three of them flinch at the same moment." (line 826) needs one frame (B3 Ex2, §8.6; A2 R7; K06).

### The Long Places, chapter II (contemplative)

The girl in the corner "where the wall gives its shoulder" (line 92); the lamp set down; the keeper at GOOD_DISTANCE, 2.4 metres. One low static camera all night; the keeper never moves; only the girl's mark changes, "Near morning" (line 102), by degrees (B3 Ex5, R3, R19).

## Self-check

Yes or no (B3 §10).
1. Does the set plan have an anchor, exits, marks and facing targets?
2. Does every move have a beat and a why?
3. Does the configuration change on each turn, and only there?
4. Is the line written per part, the pivot and silent third named?
5. Is every staging addition logged?

## Words for AI models

Works (B3 §12): positions as parts of the image ("on the left side of the image, facing right, with open space in front of her face"); "in the foreground", "in the background"; "the table between them". Fails: "lead room", "short-sided", "180-degree rule", "frame-left" (read as the character's left), exact metres, which hand is raised. Previs beats words for blocking.

## Look up for more

`stage.py lib B3 §2`, `B3 §3` to `§6`, `§7.2` (R1 to R29), `§8` (glass), `§9`, `§10` to `§12`; K02, K06, K07, K22.
