# Card 16. Glass, mirrors and sides

Situation card for the tags `glass_and_reflection` and `handedness`. Steps 7 and 8 read only "Questions in order" and "Traps"; steps 3 and 5 read it whole when a mirror rule exists.

## Situation

Glass stands between people, a shot needs a reflection, or a sided feature (a ring, a raised hand, a scar) is in frame in a mirrored world. Glass lets the eye through and stops the hand; who sees whom is a lighting choice (B3 §4.8). A wrong side breaks a plant (B4 R13).

## Questions in order

1. **Which era is the scene in, and is its frame `original` or `reversed`?** An **era** is a stretch of the film under one frame handedness; code derives it from the `WR-MIRROR` era lines (K03). Never type it.
2. **What is each element's `handedness` in its STATE?** Code derives `mirror_state`: mirrored where it differs from the frame (K03; blueprint 5.6).
3. **Which sided features are in frame?** Each needs an own side (SIDE-01); code derives the image side. Behaviour text says "hand nearest the camera"; state lines never say frame-left (blueprint 5.4 rule 8; SIDE-02).
4. **Does the story state a side for a mirrored element?** That side is apparent: the own side is the opposite, `origin: inferred` (K03; SIDE-04).
5. **In profile, which hand is nearest the camera?** A person facing frame-right shows their own right side; facing frame-left, their own left (B3 §8.2).
6. **Is there glass in frame?** Give it a `glass` item: state `clear`, `marked` (a smear, label or crack makes the pane visible), `reflecting`, `screen` or `broken_open`, and camera `through`, `along` or `angled` (B3 §8.1).
7. **Which side of the glass is the camera on?** The side of the character whose scene it is (`whose_scene`); it crosses only when the point of view shifts (B3 R11).
8. **Must a reflection lie over someone?** Check the twin and the light (B3 R28-R29).
9. **Is a plot-sided detail of a mirrored element, or readable text, in frame?** Code routes the shot (K02): text becomes a text graphic added after any flip; the detail takes the **plate route** (the place and its mirrored people made in world orientation and flipped as a still, the normal people added unflipped, then animated). A sided insert is an edited still, `flip: never` (K07).

## Rules

1. **A reflection appears where the mirror twin stands:** the reflected person as far behind the pane as they are in front. Put the camera on the line through the twin and the far person, and keep the far side darker, because glass reflects little light; side by side along the glass, they cannot line up (B3 R28).
2. **For clear glass with no reflection,** keep the camera's side darker than the far side (B3 R29).
3. **Across the world's turn, repeat size, lens and position,** so the world changes and the camera does not (B1 §10.2).
4. **Code picks `mirror_route` in K02's order:** a text graphic for readable text, always; the plate route (question 9) for a plot-sided detail of a mirrored element or a differing face of `plate_route_face_height` or more; then direct, flip with mirrored references, flip all (blueprint 8.5; C2 R5).
5. **A sided insert** (a ring, a palm) is an edited still at its final side, with `flip: never` (K07; SIDE-03).
6. **Hands on glass are rationed:** repeat the insert's framing, change one thing each time, and never add one the story does not have (B3 §8.3, R20, R27).
7. **A helmet visor stays `clear`, lit from inside, in every close-up where the face must read;** story content reflects in it at most once (B3 §8.1).

## Traps

- Asking a model for "mirrored", "backwards" or "the wrong hand" returns garbled or random sides (C2 §7.2; GEN-06). Fix: make the side right in a still, then flip or composite.
- Flipping a shot with a normal character in it moves her ring to the other hand. Fix: the plate route (C2 §7.2).
- An edit model quietly "un-flips" backwards letters. Fix: add lettering last (C2 §7.2).
- Glass so clean the hands seem to touch: the payoff is contact without touch, so let a frame edge or a faint reflection show (B4 §9.3).
- Breath fog, tears on the glass, a slow push-in with music: the familiar image played big (B4 R24).

## Words for AI models

Glass wording comes from the phrasebook by glass state (K18): clear becomes "seen through perfectly clear glass; the room on the camera's side is dark". Raised hands become "both raise the hand nearest the camera, palms toward each other, exactly like a reflection" (C2 W3). Never write "mirror image", "backwards text" or a side that a flip will change (C2 §7.2).

## Worked example

**The Catch, SC10:** "They stand facing each other across the table like a woman and her reflection, each with the wrong hand in the air." (line 428). Era b, frame `original`: Saye's state is `reversed`, so she is mirrored; Iona is normal (K03). Camera A looks along the table's centre line, on lens exception `LX-01`, spending one use of saved choice `RC-01` (K07). Iona, frame-left facing right, raises her own right hand, nearest the camera. Saye, frame-right facing left, raises her own right, which reads as her left, also nearest the camera; her ring, own left and apparent right (line 436), is on the far, lowered hand (B3 §8.2). Saye's raised hand is plot-sided, so SH080 takes the plate route (question 9). The rings are edited-still inserts, SH090 and SH100, `flip: never` (K07, K22).

**Another tone, The Long Places, chapter VI:** Yusuf's pool holds "a figure's worth of dark, upright" that stays still "while everything else in the water moved" (line 524). Lay the still shape over the rippling reflection as its own layer, so the evidence stays exact and uncertain (D6 W6).

## Look up for more

B3 §7.2 (R28-R29), §8 (glass and mirrors); B1 §10.2; C2 §7; D6 W6; K02, K03, K07, K18, K22. Print one rule with `stage.py lib B3 R28`.
