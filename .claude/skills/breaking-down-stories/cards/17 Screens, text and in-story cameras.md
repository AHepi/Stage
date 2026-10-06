# Card 17. Screens, text and in-story cameras

Situation card for the tags `screens_and_text` and `in_story_footage`. Steps 7 and 8 read only "Questions in order" and "Traps"; step 3 reads only "Text orientation"; step 4 reads it whole.

## Situation

Words the audience must read (signs, labels, displays, title cards), screens in the frame, and footage recorded in the story. Models draw text badly and change it between clips, so code draws every readable word and lays it in after (K17; C3 §13A).

## Questions in order

1. **Must the audience read it?** Make a TEXT record with the exact words, case, orientation and surface, `method: composite`; only text too small to read is left to the model (A3 R11; K17); a lone letter the shot is about may be `model_drawn`.
2. **How long must it stay?** Code derives the reading floor from `text_floor`, doubled when mirrored (K09). If the shot is short, put the words up early and let the change come late (D12 Recipe 2).
3. **How big?** Size a must-read word for its smallest appearance in frame (D12 R6, R10).
4. **Is its meaning taught first?** A display the plot will read gets one teaching appearance at emphasis 2 at least a scene earlier (D12 R2; B4 R7).
5. **Who made it?** The maker decides its orientation in a mirrored scene ("Text orientation"; SIDE-05).
6. **Is it footage recorded inside the story?** Give it a CAMERA record (position, lens, frame shape, frame rate, overlays, `moves`), record the event once as one continuous take, and cut every viewing from it (B1 §10.4, R22).
7. **Is a screen in frame?** The device shot asks for a blank screen; its content is its own shot, pinned on after (blueprint 8.5; C2 R6; C3 §13B).
8. **Does a later scene replay this one?** Put the replaying camera into this scene's set plan as a named setup (A3 R9).
9. **Does something appear or vanish on a fixed feed?** Between two frames: no camera move, no dissolve, no glow (B1 R20, §10.6). Chained pieces of one feed are joined by a `continue` CUT; a `kind: screen` shot's `height` is the in-story camera's, in metres.

## Rules

1. Draw exactly what the script says a display shows (D12 R1).
2. A colour keeps one meaning film-wide, and a state colour changes on one frame, never by a cross-fade (D12 R3, R12).
3. Colour never works alone: red is also dashed and darker, green solid and brighter (D12 R13).
4. Invented words (a clock, a unit) stay smaller than every scripted word and are logged `origin: invented` (D12 R4).
5. No blink, pulse or sting on a display change the script does not write (D12 R16; B4 R23).
6. Design in-story footage backwards from what it must reveal (B1 §10.4).

## Text orientation

In a mirror story every TEXT follows a story-world RULE of kind `text` that names what it governs and its exceptions (`reads: normal | mirrored`, `why`) (K04; SIDE-05).

1. Title cards, credits and captions are never mirrored (D12 R17; `WR-TITLES`).
2. A picture made inside the story world and shown on a screen (a recording, a feed, a file) is flipped whole, once, in a mirrored **era** (a stretch of film under one frame handedness) (D12 R18; B1 §10.2).
3. A display that draws the positions of things also in the picture reverses only its words, each where it stands, and keeps its drawing true (D12 R19).
4. A device that turned with the character keeps its orientation to her: by default the suit's words stay backwards after Iona's second turn (a question for the user, D6 §12), so the first forward world word is the wall sign, "On the wall above Saye: RECEIVING." (line 1620) (D12 R21, §4.3).
5. Mirrored words must visibly reverse: build them from letters that change in a mirror, not from A, H, I, M, O, T, U, V, W, X or Y (D17 R18).
6. Never reverse each word where it stands and then flip the whole layer: the two cancel (D12 Recipe 3).

## Traps

- Readable or backwards text asked of a video model (GEN-06; C2 §7.2). Fix: a code-drawn TEXT record.
- "Hologram", "interface" or the script's own words in a video prompt: the model invents its own text and glow. Fix: ask for a blank screen (D12 Recipe 9).
- A red-to-green cross-fade passes through yellow, the colour of the painted line. Fix: change on one frame (D12 R12).
- A mirrored play triangle reads as rewind. Fix: a pause glyph or none (D12 R20).
- Security footage zoomed into a clean close-up: the evidence stays small in the fixed frame (B4 Ex 11.2).
- A title card flipped with its era. Fix: never flip titles (D12 R17).

## Words for AI models

The device with a blank screen: "the monitor's screen is dark and blank, switched off", or for a moving shot "a flat, evenly lit, pure bright green panel" (D12 Recipe 9). A feed as its own clip: "high corner security camera view, wide lens, grainy, fixed" (C3 §13B). A lamp carrying a colour code: "a small round lamp on the shell, glowing red", its hue matched in the grade (D12 Recipe 9, R15).

## Worked example

**The Catch, SC13:** "Security footage, paused: a camera above the top gate, looking straight down the shaft." (line 674). `CAM-SHAFT-TOP` is fixed and top-down, with a wide lens, a low frame rate and a clock printed into the picture; the fall is recorded once for every viewing (B1 §10.4). It was recorded in era a and is shown in era b, so the whole picture, clock included, flips once (`WR-REPLAY`; D12 W2). The puck stays small in the paused frame; "Iona pauses the recording with the remote." (line 742) carries the emphasis, not a zoom (B4 Ex 11.2).

**Another tone, The Long Places:** Yusuf's tally screen counts openings (line 504). The count is the hero, in large numerals; cut from a "40" insert to a "41" insert of the same framing, with no animation on the number (D12 W6, R9).

## Look up for more

D12 §3, §4 (mirrors), §11; B1 §10.4-§10.6; C3 §13; K04, K09, K17; card 16. `stage.py lib D12 R19` prints one rule.
