# D12. Diegetic UI and on-screen graphics: visors, wrist displays, monitors, CCTV overlays, signs, title cards

> **What this file is for**
> 1. Designing every graphic the audience must read (visor, wrist display, monitors, security overlays, files, title cards) so it reads at a glance, teaches its own meaning and survives the mirror world.
> 2. One style guide per film (grid, OFL typefaces, colours from B2's motif code, icons, states, frame timings, mirror behaviour), as a template and filled for *The Catch*.
> 3. Making the graphics with tools an LLM can drive: SVG drawn frame by frame (tested script included), browser animation captured headless, Blender text, Resolve by hand.
> 4. The fields, checks and failure modes this subject adds; the whole visor arc of *The Catch*, the SC13 security overlay, the Nell file, the title card, and Yusuf's tally screen from *The Long Places*.

**Fact-check note (2026-09-28, adversarial).** Re-opened S1, S2, S3, S5 (record), S6 (§9.2.1-9.2.2 and the `tts:lineHeight` guidance), S7, S8, S9, S10, S12, S13, S14 (both), S15 (Playwright's docs source), S16 (both), S17, S18, S19 (three manual pages and Blender's colour-management notes), S20 and S21; re-matched every quoted line of both texts; re-ran Recipe 3 (resvg-py 0.5.0), the ProRes 4444 alpha round trip (ffmpeg 7.0.2), the Pillow aliasing test, the font measurements and the colour arithmetic; ran Recipe 4 for the first time (Playwright 1.63.0, Chrome Headless Shell 153). **Corrections:** B612's cap height is 0.75 em in its OS/2 table (the H glyph measures 0.76), which leaves the 43 px size unchanged; the SC28 wall sign is not the first *forward word* since SC06, because the turned SC12 meal label reads forward ("The letters face the right way. She reads it again.", l.639) and B1 §10.2 builds the SC28 payoff as its rhyme (it is the first untouched *world* word to read forward); the missed-call phone in W6 is Dr. Arat's, in chapter IV, not Yusuf's; free Resolve 21.1 keeps console scripting (rule 25's reason restated, as D8 conflict 15 asked); rule 8's doubling is cited to A4 R8 and D8-R53 (D8 conflict 16); rule 4's invented-text limit was lower than two of this file's own worked examples (raised to 2.5%, below every scripted word); S3 and S5 are now read; D6 already follows this file on the visor (conflicts updated). **Added:** rules 2a, 15a, 25a; a tested timeline for Recipe 3; a tested page and capture script for Recipe 4; Recipe 9 (what to tell the models); the SC26 carriage recording on the wrist (B4 M06's payoff, missing from W1); W7 (the SC15-16 tablet overlay); the mapping to the blueprint's TEXT record (§8); five new conflicts (§12).

## 0. How to read this file

- **Tags.** [V] verified at a primary source on 2026-09-27 or 2026-09-28, or run by the author of this file ("author test"); [U] unverified or secondary only; [J] judgment. Tool facts go stale: re-check anything older than 30 days (C1 staleness rule).
- **Builds on, not repeated:** A3 R11 (text spec), A4 R8 and B1 R2 (reading times), B1 §10.2-10.6 (mirror phases, VISOR VIEW, surveillance), B2 §8.4 (motif colours), B3 §8.1 (visor glass), B4 M01, R7, R23, R26, C2 R6 and the era table, C3 §13A-B, C4 Route 5, D4 (licences), D6 (Rec1 corner pin, Rec2, Rec6 visor HUD, W2 tablet feed, W5 SC26, flip counting, `comp_plan`), D8 (cards, credits, safe areas, subtitles). This file designs the graphic; D6 lays it into the shot; D8 places it in the cut.
- **Scene numbers** follow the 30 headings of *The Catch* (SC01 tunnel to SC30); "l." is the line in the workshop revision.
- **Rule numbers are stable** because other files cite them (D6, D8, D18 cite rules 6, 8, 19, 21, 25, VG1 and Recipe 7); rules added later carry a letter (2a, 15a, 25a).

## 1. Terms (one plain sentence each)

- **Graphic:** any picture element drawn by code (lines, outlines, words, numbers), never by an image or video model.
- **Display:** an in-story device surface that shows graphics (visor, wrist display, monitor, tablet, phone).
- **Visor display (HUD):** the graphics on the inside of Iona's helmet glass; HUD means heads-up display.
- **Diegetic:** part of the story world, so characters can see it; **non-diegetic:** seen only by the audience (title cards, credits, subtitles). Game designers add two in-between kinds (Fagerholt and Lorentzon's *spatial* and *meta* interfaces, S5); a film needs only the two.
- **Hero graphic:** a graphic the story needs read; **ambient graphic:** background texture nobody needs to read (Territory Studio's "hero screens that help to explain plot points" versus "ambient screens that help to create background 'noise'" [V, S1]).
- **FUI:** the trade name for screen graphics made for films; Pushing Pixels runs its interviews as a series "on fantasy user interfaces" (S3; also written "fictional").
- **Label:** a word naming a drawn thing (RECEIVING); **readout:** a word or number reporting a value (UPWARD SPEED, 12).
- **Icon:** a small symbolic drawing (a marker, an arrow, a dot).
- **State:** one look of an element that means one thing (idle, go, limit, selected, preview).
- **Graphic language:** the film's fixed set of icons, colours and states with one meaning each.
- **Teaching shot:** the first clear, unhurried sight of a graphic, placed before the moment that depends on it (B4 R7).
- **Cap height:** the height of capital letters, measured here as a percentage of the finished picture's height.
- **Tabular digits:** digits of equal width, so a changing number does not shift sideways.
- **Screen-locked / surface-pinned / world-locked:** fixed to the frame; fixed to a moving device surface by a corner pin (D6 Rec1); drawn as a 3D object seen through the shot's camera.
- **Whole flip:** mirroring an entire graphic layer left to right; **in-place flip:** mirroring each word about its own centre while everything else stays where it is.
- **Timeline:** a list of changes to a graphic by frame number; **frame-driven rendering** draws every frame from its number, never from a clock, so renders repeat exactly.
- **Headless browser:** a web browser run by a script without a window.
- **Borrowed words:** *OFL*, the SIL Open Font License, lets anyone use a font free in video; *era* A, B or C is C2's mirror phase of *The Catch* (before the cage turns, while Iona is turned, after her second turn); *L0-L3* are B4's emphasis levels, L3 the loudest; *plate* is the generated clip a graphic sits on (D6); *VISOR VIEW* is the script's term for Iona's point of view through the helmet; *alpha* is a picture's transparency; *ProRes 4444* is a video format that keeps it.
- **Style guide:** the one file fixing a film's graphic grid, fonts, colours, icons, states and timings; **graphic register:** the list of every graphic, each with a script-issued ID (C5 R23).

## 2. Core principles

1. **Story first, plausibility second** [V, S2]. Jayse Hansen designs screens "to a degree that it works for the story – which is the most important – and reality comes in as a second".
2. **Read at a glance, in about three seconds** [V, S1, S2]. Territory Studio's hero screens "tie into specific 'story beats' and are only in shot for about 3 seconds", and "The FUI has to clearly communicate the narrative point, visualise and explain often complex information at a glance"; of the wearer of his Mark VII Iron Man HUD, Hansen says "he can read the patterns at a glance, rather than just raw information". Shapes and colour first, words second, numbers last.
3. **Teach before you pay off** [J, B4 R7]. Every meaning the climax uses is shown once, plainly, earlier; it never changes meaning afterwards.
4. **Few words, the script's words** [J, A3 R11]. Scripted words exactly; invented words ambient, small and logged.
5. **Design for the flip** [J]. Only words and digits should change when mirrored; build everything else symmetric about a vertical axis or running vertically.
6. **One maker, one look** [J]. Saye's monitors, the suit and the wrist share one language, learned once.
7. **Colour never works alone** [V, S7]. "About 1 in 12 men have color vision deficiency", most often red-green; every colour state also differs in line style or brightness.
8. **Graphics last** [J, D6 principles 1, 2, 4]: drawn after every AI pass, then matched to the plate's blur and grain.
9. **Frame-driven, file-based** [J]. The LLM writes a timeline and runs a script that renders numbered PNGs; the user judges three named frames (D6 principle 7).
10. **Familiar first, then one step further** [V, S3]. Mark Coleran: "You look for those hooks where people are familiar with something, and then add to that"; his "pragmatic futurism" is to "make it feel like its feet are still on the ground". For *The Catch*: aircraft-cockpit plainness (B612), not holograms.

## 3. Decision rules

**Design and meaning**
1. If the script names what a display shows ("her outline, the engine, a bar of charge", l.1028), then draw exactly those elements, because extras dilute a 3-second read [J; S1].
2. If a later scene depends on reading a graphic, then give its meaning an L2 teaching shot at least one scene earlier, recorded in `teaches`, because suspense needs knowledge (B4 R7).
2a. If a display appears after its motif's L3 payoff (the visor in SC26-SC27, after M01's two green outlines in SC25), then frame it only as large and as long as legibility needs, up to L2, with no rhyme, held beat or signal that recalls the payoff, because a loud return explains the payoff twice (B4 R26 and its display exception).
3. If a meaning already has a colour in B2's motif code, then reuse it and never give it a second meaning, because red is "A limit, and its cost" and green "Fits, allowed, go" film-wide (B2 §8.4).
4. If a word is not in the script (timestamps, units, dates), then keep its cap height at or below 2.5% (rule 7's secondary size) and smaller than every scripted word in the same shot, log it as an invention and never let the plot depend on it, because invented text competes with scripted text [J]. (The first version said "under 2%", which W2's 2.3% clock broke.)
5. If a display is world-made, then design it as its makers would (Saye's institute: clinical, plain), because plausibility comes from one consistent maker [J; supported by S3's "pragmatic futurism", V].

**Legibility and timing**
6. If the audience must read a word, then its cap height in the finished frame is at least 4% of picture height (5% preferred), because that matches a BBC subtitle shown at 0.6-0.8 of its authored size inside a letterboxed 2.39 picture [J, arithmetic from S6, V: the BBC authors "a line height in the range 7% to 8% of the active video height", recommends `tts:lineHeight="120%"` of the font size, and says "For most screen sizes, the preferred font size is between 0.6 and 0.8 times the required authoring font size". So: 7.5% ÷ 1.2 = 6.25% font size of a 1080 frame; × about 0.7 cap-to-em = 4.4%, or 47 px; × 0.6-0.8 = 28-38 px; divided by the 804 px of a 2.39 picture = 3.5-4.7%, centre about 4%].
7. If text is secondary (a unit, a sub-label), then 2.5-3% cap height; if texture, under 1.5%, because readable-but-unimportant text makes the audience hunt [J].
8. If a word must be read, then hold it for the longer of B1 R2 (2 s + 0.5 s per word) and A4 R8 (1 s + characters ÷ 12, counting spaces and punctuation), doubled if mirrored (A4 R8; D8-R53; D8-R43 takes the longer of the two); count time across consecutive shots only if the word keeps its place and size, with one uninterrupted hold of the unmirrored time, because a cut restarts the eye's search [J].
9. If a readout changes value, then use tabular digits and change the value on a cut frame, because proportional digits jiggle and rolling numbers cannot be read [J].
10. If a device appears small in frame, then size its words for their smallest appearance: cap on the device ≥ required on-frame cap ÷ the device's share of frame height, because full-screen designs shot wide lose every word [J]. CONTROL on a monitor filling 30% of frame height needs a cap of 4 ÷ 0.30 ≈ 13% of the monitor's picture.
11. If a graphic must work on phones, then check a still at 640 px wide, because most short films are watched small [J].

**Colour and states**
12. If an element changes state colour (red to green), then cut on one frame, never cross-fade, because an additive red-to-green blend passes through khaki-yellow (midpoint #98895A of this file's colours [author computation]) and B2 reserves yellow for "The line", with the rule "Painted only, never a light." (B2 §8.4).
13. If red and green carry meaning, then red is also dashed and darker, green solid and brighter, because this pair measures 2.8:1 in luminance and 2.2:1 after a deuteranopia simulation, where red turns olive (#8F8023) and green pale khaki (#CEC290) [author computation, Machado 2009 matrix at severity 1, S8].
14. If an element is selected, previewed or erased, then show it by line weight, dash or opacity, never a new hue, because the motif code has taken every hue [J].
15. If a practical light shares the code (SC23's shell light), then match its hue by compositing or grading, because models ignore hex codes (B2 §13.3: "Hex codes are not reliably reproduced") while code-drawn graphics obey them [J].
15a. If a practical light carries red and green with no second cue (the script's single "A light on the shell", l.1331), then give it a position cue the colour-blind can read, as D18 proposes (two lamps, red below and green above, like a traffic light), or accept a colour-only moment and let the drawn outlines (rule 13) carry the meaning, because a single lamp changing hue fails rule 7 for about 1 in 12 men; the two-lamp version changes the script's image, so the user decides [J; flag].
16. If a display state changes, then add no blink, pulse or sting unless the script writes one ("Iona's wrist chimes", l.1374), because a script marker allows zero added signals (B4 R23).

**Mirror**
17. If a graphic is non-diegetic (title card, credits, subtitles), then it never follows the mirror rule, because the rule belongs to what Iona sees [J; the blueprint's `WR-TITLES`: "title cards always read normally"; D8-R53 covers the subtitling of backwards text].
18. If a world-made display shows a picture of the world (recordings, feeds, files, dish footage), then flip the whole picture once in era B, because it is world content (B1 §10.4; D6 rules 15-17).
19. If a world-made display draws positions of things also in the plate (her outline, the hull, the room), then mirror only its words in place and keep the geometry true to the plate, because a whole flip puts the drawn hull opposite the real one [J].
20. If an element is asymmetric (play triangle, horizontal arrow, spinner, 45° hatching, seven-segment digits), then replace it in mirrored displays or accept the reversal knowingly, because a flipped play triangle reads as rewind and a flipped seven-segment 2 reads as 5 [J].
21. If a device sits inside Iona's outline at a turn (suit, visor, wrist display, engine), then its mirror state relative to her does not change, because the turn is drawn "round everything inside her outline. Herself. The suit." (l.1536) [J; §4.3].

**Production**
22. If a graphic is 2D, screen-locked or corner-pinned, then draw it with Python and SVG (Recipe 3), because it is exact, free and needs no GUI [V, author test].
23. If a graphic already exists as web animation, Lottie or canvas code, then capture it in a headless browser, seeking each frame (Recipe 4), because real-time capture drops and doubles frames [J; S14-S16].
24. If a graphic must change perspective with a moving camera, then build it in Blender through `camera_track.json` (Recipe 5; C4 Route 5), because 2D cannot fake changing perspective [J].
25. If a card or credit needs no animation, then render it as a PNG (D8 Rec9) and use Resolve only to place it, because an LLM cannot drive free Resolve 21.1 from outside: external scripting, Workflow Integrations and the MCP server are Studio-only, and only console scripting pasted by hand remains free [V via D8 §3 and its sources; corrected 2026-09-28 at D8's request, conflict 15], while a PNG is exact and needs no clicks.
25a. If a graphic will be drawn in a browser (Recipe 4), then leave Playwright's screenshot `animations` option at its default for page screenshots (`"allow"`) and seek every frame yourself, because `"disabled"` "stops CSS animations, CSS transitions and Web Animations" and fast-forwards finite ones "to completion", which would replace your seeked frame with the last one [V, S15 docs source].

## 4. Mirror behaviour

### 4.1 What a left-right flip does to each kind of element [J; author test for rows marked T]

| Element | After a flip | Use in a mirrored display |
|---|---|---|
| Words (T) | Reversed letters in reversed order; only asymmetric letters betray it (D6 W4) | Flip in place or whole, by rule 18-19 |
| Digits (T) | Order reversed, glyphs mirrored: "12" reads like "Ƨ1" or "21"; 0 and 8 unchanged | Pair numbers with a shape (a vertical arrow or bar); 0 reads the same |
| Seven-segment digits | 2 becomes 5, 5 becomes 2 | Never use |
| Front-view person outline (T) | Unchanged | Safe |
| Vertical bar or gauge (T) | Unchanged | Safe; make every gauge vertical |
| Vertical arrow (T) | Unchanged | Safe |
| Horizontal arrow, play triangle, progress bar filling left to right | Reverses meaning | Avoid, or accept as world-made reversal |
| Pause glyph, dot, ring, diamond, square | Unchanged | Safe |
| Needle meter ("a grey box with a needle in it", l.498) | Swings the other way | World prop, flips with the world |
| 45° hatching | Becomes 135° | Use horizontal or vertical hatching, or stipple (D6 W5 uses vertical; pick one per film) |
| Rewind or fast-forward glyph (◀◀, ▶▶) | Swap meanings | Never use; show a rewind by the picture and the clock running backwards (W7) |

### 4.2 The *Catch* policy [J]

- **Era A** (to the CLACK): nothing mirrored.
- **Era B, world pictures** (SC12 dishes, SC13 playback, SC15 tablet feed (D6 W2), SC17 recording and Nell file, Saye's recordings on the wrist): whole flip once (rule 18).
- **Era B, the suit's own graphics** (wrist from SC18, visor from SC23): words flipped in place, geometry true to the plate (rule 19). The wordless SC18 teaching shot looks the same either way.
- **Era C, after Iona's second turn**: the suit's graphics stay as they were (rule 21). The first forward world word of era C is the wall sign: "On the wall above Saye: RECEIVING." (l.1620), which rhymes with the one forward label of era B, the meal in SC12 that Saye had turned ("The letters face the right way. She reads it again.", l.639; B1 §10.2).
- **Non-diegetic**: never.

### 4.3 What snaps readable after Iona's turn: nothing on the suit [J]

B1 (§16) recommends that "the visor text snapping to readable after her final turn becomes an extra cue"; D6's first draft repeated it (D6 has since adopted this section: its rules 19a-19b, Rec6 and W5). By the script's own mechanism it cannot happen: the SC26 turn is drawn "round everything inside her outline. Herself. The suit. The engine. The vessel on her chest. The container under it." (l.1536). Suit and wearer turn together, so the suit's letters keep their relation to Iona; the script already says the suit's words read backwards to her in era B ("Every word printed on it reads backwards to her.", l.1006); after the turn it says "Then stars. The same view, from the same side." (l.1569). It is also better drama: the visor shows RECEIVING backwards through SC26-SC27, then the wall shows the same word forwards in SC28: the first untouched world word to read forward since SC06 (the SC12 meal label, l.639, read forward only because Saye had turned it, and B1 §10.2 asks SC28 to repeat its framing); that is why Iona "Reads it again". By the same logic the suit's printed lettering stays backwards in era C, a row missing from C2's era table (C2 §7.4 item 3 already reasons the same way about the container that turned with her). A snap would need an on-screen reason (a technician's setting shown in SC18) and would break the SC28 rhyme.

## 5. The style guide

### 5.1 Template (JSON; one file per film; the LLM fills it, the user approves once)

```json
{"style_guide_id": "UISG-<FILM>-V01",
 "canvas": {"delivery_px": [1920, 804], "safe_margin_pct": 5, "base_unit_px": 8,
            "keep_clear_centre_pct": [40, 60]},
 "devices": [{"id": "<GR-...>", "native_px": [0, 0], "lock": "screen_locked | surface_pinned | world_locked",
              "maker": "world | turned | none", "mirror_mode_by_era": {"A": "none", "B": "...", "C": "..."}}],
 "type": {"ui_family": "<OFL face>", "ui_numbers": "<mono face>", "cards_family": "<OFL face>",
          "licences": {"<face>": "ofl_1_1"}, "cap_height_per_em": {"<face>": 0.0},
          "fallback_by_script": {"<script, e.g. ja>": "<OFL face covering it>"},
          "must_read_cap_pct": 4.0, "secondary_cap_pct": 2.5, "texture_cap_pct_max": 1.5,
          "case": "upper", "tracking_pct": 3},
 "colours": {"ui_neutral": "#......", "state_go": "#......", "state_limit": "#......",
             "forbidden": ["<hue families the motif code reserves>"]},
 "line": {"stroke_px": 3, "selected_px": 5, "preview_px": 2, "limit_dash": "10 8", "preview_dash": "4 6"},
 "icons": [{"name": "...", "symmetric": true, "meaning": "..."}],
 "states": {"idle": "...", "go": "...", "limit": "...", "selected": "...", "preview": "...", "off": "..."},
 "timing_frames_24fps": {"build_on": 6, "teach_draw_on": 12, "state_colour": 0, "select": 4,
                         "remove": 4, "erase_line": 10, "level_change": [12, 24], "cascade_gap": 6, "number_change": 0},
 "motion_blur_on_graphics": false,
 "teaching_order": [{"meaning": "...", "scene": "..."}]}
```

Timing basis: Material Design 3's duration tokens run from 50 to 1,000 ms (medium1 250 ms) with "emphasized" easing `cubic-bezier(0.2, 0, 0, 1)` [V, S9]; at 24 fps, 250 ms is 6 frames. Film graphics sit at the slow end: the audience did not press the button [J].

### 5.2 *The Catch*, filled [J unless marked]

- **Grid (visor, 1920×804):** safe area x 96-1824, y 40-764 (D8 R45); centre 768×482 px kept clear so the world reads; schematics lower left, readouts upper right; unit 8 px. **Wrist:** native 800×500 drawn at 1600×1000, outline centre-left, bar right; only ever an insert on her glove (B1 §10.6).
- **Typefaces:** world UI in **B612**, "designed and tested to be used on aircraft cockpit screens" (Airbus with ENAC and Université de Toulouse III, drawn by Intactile), licensed EPL 2.0, EDL 1.0 and SIL OFL 1.1 [V, S10]; numbers in **B612 Mono** (OFL) [V, S10]. Cards and credits in **IBM Plex Sans** (OFL) [V, S11], the choice D8 left to this file: a neutral voice so the title never looks like a display. OFL allows "video titling"; credit is "not required" [V, S12]; IBM Plex's licence names "Plex" a Reserved Font Name, which only stops a *modified* font using that name [V, licence file]. Cap height: B612 0.75 em by its OS/2 table (its H measures 0.76), IBM Plex Sans 0.698 em [V, author test], so a 4% cap on 804 px (32 px) needs B612 at 43 px (32 ÷ 0.75 = 42.7) and Plex at 46 px. Digits: B612, B612 Mono and IBM Plex Sans all draw 0-9 at one width (tabular by default); Atkinson Hyperlegible does not [V, author test]. For other scripts (D18-R37): Noto Sans JP or Noto Sans SC, both OFL in Google Fonts [V: licence files; glyph coverage not tested].
- **Colours** (drawn by code, so hex is exact): `ui_neutral` #E8E6DF at 85%; `state_go` #58E08A, solid; `state_limit` #D8322B, dashed 10/8, a placeholder until the SC01 tag is sampled from the approved key frame; forbidden: yellow light, saturated blue (B2 §8.4). In exterior close-ups the face glow follows the dominant state colour and goes out when the green line is deleted (B2 Ex4); drive it from the same timeline.
- **Icons** (all symmetric or vertical): person outline (front view; Iona 1.0, the figure 1.4 times her height, head low between its shoulders), vessel capsule, engine block at the shoulders, charge bar with a reserve tick at 25% and an empty line, marker (diamond), path line, turn ring (a ring with a vertical axis stroke), vertical arrow, radio dot, recording frame, rock band in horizontal hatching.
- **States:** off; idle (neutral); go (green, solid); limit (red, dashed); selected (+2 px); preview (2 px, dash 4/6, 60%).
- **Teaching order:** levels and moving icons SC17; outline, engine, charge SC18; green lights SC20; red then green as a load limit SC23 (shell light, and the load check); outline around objects SC24; the vessel capsule SC25. After SC25 no new colour or state meaning; new shapes only where the script labels them (RECEIVING, TURN, CROSS AT 0, HULL CLEARANCE, UPWARD SPEED) or they picture what is in the plate (the room, the rock, the hull) [J].

## 6. Tools an LLM can drive (checked 2026-09-27; re-checked 2026-09-28)

| Tool | Facts | Use here |
|---|---|---|
| **Python + resvg-py** | resvg renders SVG to PNG, Apache 2.0 or MIT, "No animations. There are no plans on implementing them either.", and draws text itself, without system text libraries [V, S13]; resvg-py is its MIT Python binding, whose `font_files` and `skip_system_fonts` arguments load exactly the fonts you name [V, S13 and author test] | Default (Recipe 3): 48 frames at 1920×804 in 5.4-5.9 s on CPU [V, author test 27 and 28 Sept] |
| **Python + Pillow** | `ImageDraw.fontmode`: "Set to "1" to disable antialiasing" [V, S21]; but `stroke_width` outlines stay antialiased (82 grey levels in the re-test, against 3 for offset copies) [V, author test] | Low-resolution overlays (CCTV, W2) |
| **ffmpeg** | PNG sequence to ProRes 4444 with alpha (`prores_ks -profile:v 4444 -pix_fmt yuva444p10le`) [V, author test: frame 30 decoded back with identical colours and alpha, ffmpeg 7.0.2; D6] | Every hand-off to the comp |
| **Headless Chromium via Playwright** | `omitBackground`: "Hides default white background and allows capturing screenshots with transparency. Not applicable to `jpeg` images." [V, S15]; `pip install playwright` then `playwright install chromium` fetches a headless Chrome (153 on 28 Sept) [V, author test, Playwright 1.63.0] | Capturing SVG, CSS, canvas or Lottie animation (Recipe 4: 48 frames in 3.9 s) |
| **Seeking browser animation** | `setCurrentTime(seconds)` and `pauseAnimations()` for SVG; `document.getAnimations()` returns "CSS Animations, CSS Transitions, and Web Animations" [V, S16] | Frame-exact capture (Recipe 4) |
| **Lottie** | Open vector animation format kept by the Lottie Animation Community, "hosted by The Linux Foundation"; lottie-web (MIT) has `goToAndStop(value, isFrame)` [V, S14] | Only if a designer delivers Lottie |
| **Remotion** | Free for individuals, companies "with up to 3 employees" and non-profits; others buy a licence [V, S17] | Optional |
| **Manim Community** | `-t, --transparent` "Render scenes with alpha channel" [V, S18] | Optional: Python diagrams |
| **Blender 5.2 LTS** | Text objects use a built-in font or "PostScript Type 1, OpenType and TrueType fonts" [V, S19] and can be converted to curve or mesh [J]; the Wireframe modifier turns "edges into four-sided polygons" and needs a mesh with faces; Freestyle is "an edge/line-based non-photorealistic (NPR) rendering engine" [V, S19]; AgX "replaces Filmic as the default in new files" since 4.0, while Standard "Does no extra conversion besides the conversion for the display" [V, S19 colour pages] | World-locked text and wireframes (Recipe 5) |
| **DaVinci Resolve 21.1 free** | Fusion page for "powerful broadcast graphics and sophisticated title animations"; "For 2D text, drag a Text+ node into the node tree and type your text" [V, S20]; Edit-page menu paths [U]; an LLM cannot drive it from outside: external scripting, Workflow Integrations and MCP are Studio-only, console scripting stays free (D8 §3) [V via D8] | Manual route and final placement |

**Default** [J]: Python + resvg-py + ffmpeg, run by the LLM; nothing to buy.

## 7. Recipes

### Recipe 1. Style guide and graphic register from the script (30-60 min, once per film)

1. Ask: *"List every script line where something is displayed, printed, labelled, projected or shown on a screen, with line number and exact words. For each: device, maker, era (A/B/C), whether the plot depends on reading it, and the scene that first teaches its meaning."*
2. Ask: *"Fill the style guide template (D12 §5.1) from the style bible (D5), B2's motif code and the device list. Only OFL fonts. Mark every invented value."*
3. A script issues the IDs (`GR-VISOR`, `GR-WRIST`, ...), never the LLM (C5 R23).
4. The user approves one test sheet: every icon in every state on black and on mid-grey, full size and 640 px wide.
5. **Acceptance:** one icon and one state per meaning; no asymmetric icon in a mirrored display; must-read words ≥ 4% cap.

### Recipe 2. Spec one graphic and check its reading time (10-20 min per graphic)

1. Quote the script lines. List elements, states, events by frame.
2. Compute reading time per word group: T = max(2 + 0.5 × words, 1 + characters ÷ 12) seconds, characters counted with spaces and full stops; double if mirrored (rule 8). Example: CROSS AT 0 is 3 words and 10 characters, so max(3.5, 1.8) = 3.5 s, mirrored 7.0 s = 168 frames at 24 fps. A changing number: at least 24 frames per value, 48 if mirrored, except 0, which reads the same both ways (24).
3. If the shot is too short, put the words up earlier and let the geometry carry the moment ("words early, change late") [J].
4. **Acceptance:** VG1, VG2, VG2a and VG3 in §8 pass; the result goes into the shot's `read_time_s` and `on_screen_s`.

### Recipe 3. Animated HUD frames with Python and SVG (Easy; 30-60 min first, 10 min later) [V, author test]

Tested 2026-09-27 and re-run 2026-09-28 (S22): in-place flipped words stayed in position (HULL CLEARANCE centred on x 1500); a red dashed outline snapped to solid green on frame 30 (#D8322B on frames 0-29, #58E08A from 30); zero speed drew a flat tick; alpha survived into ProRes 4444. The 28 Sept copy adds only `escape()`, and its frames are byte-identical to the 27 Sept ones.

```python
"""hud_frames.py timeline.json out_dir - HUD as transparent PNGs (pip install resvg-py).
Element "mirror": "none" | "in_place"; timeline "mirror_whole": true flips the whole layer."""
import json, sys, os, resvg_py
from xml.sax.saxutils import escape   # so "&" or "<" in a word cannot break the SVG

def ease(t): return t * t * (3 - 2 * t)

def value_at(keys, prop, f):
    ks = sorted([k for k in keys if prop in k], key=lambda k: k["f"])
    if not ks: return None
    if f <= ks[0]["f"]: return ks[0][prop]
    for a, b in zip(ks, ks[1:]):
        if a["f"] <= f < b["f"]:
            va, vb = a[prop], b[prop]
            if isinstance(va, str) or b.get("step"): return va   # colours, text: snap
            return va + (vb - va) * ease((f - a["f"]) / (b["f"] - a["f"]))
    return ks[-1][prop]

def person(cx, top, h, colour, width, dash):   # symmetric: left half mirrored
    s = h / 100.0
    half = [(0, 22), (-9, 24), (-16, 30), (-18, 58), (-12, 60), (-11, 100), (0, 100)]
    pts = [(cx + x*s, top + y*s) for x, y in half] + [(cx - x*s, top + y*s) for x, y in reversed(half)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<g fill="none" stroke="{colour}" stroke-width="{width}"{da} stroke-linejoin="round">'
            f'<circle cx="{cx}" cy="{top + 11*s:.1f}" r="{10*s:.1f}"/><path d="{d}"/></g>')

def frame_svg(tl, f):
    W, H, out = tl["w"], tl["h"], []
    for e in tl["elements"]:
        def g(p, d=None):
            v = value_at(e.get("keys", []), p, f)
            return v if v is not None else e.get(p, d)
        op = g("opacity", 1)
        if op <= 0: continue
        t = e["type"]
        if t == "person":
            out.append(f'<g opacity="{op}">' + person(g("x"), g("y"), g("h"), g("colour"), g("stroke", 3), g("dash")) + "</g>")
        elif t == "bar":   # vertical, so a flip cannot reverse it
            x, y, w, h, lv, r = g("x"), g("y"), g("w"), g("h"), g("level"), g("reserve", 0.25)
            c = g("colour")
            out.append(f'<g opacity="{op}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{c}" stroke-width="2"/>'
                       f'<rect x="{x}" y="{y + h*(1-lv):.1f}" width="{w}" height="{h*lv:.1f}" fill="{c}"/>'
                       f'<line x1="{x-8}" x2="{x+w+8}" y1="{y + h*(1-r):.1f}" y2="{y + h*(1-r):.1f}" stroke="{c}" stroke-width="2"/></g>')
        elif t == "line":
            da = f' stroke-dasharray="{g("dash")}"' if g("dash") else ""
            out.append(f'<line x1="{g("x1")}" y1="{g("y1")}" x2="{g("x2")}" y2="{g("y2")}" stroke="{g("colour")}" stroke-width="{g("stroke", 3)}"{da} opacity="{op}"/>')
        elif t == "arrow_v":   # length in px; 0 draws a flat tick
            x, y, n = g("x"), g("y"), g("length")
            if abs(n) < 1:
                out.append(f'<line x1="{x-14}" y1="{y}" x2="{x+14}" y2="{y}" stroke="{g("colour")}" stroke-width="3" opacity="{op}"/>'); continue
            tip, k = y - n, (14 if n > 0 else -14)
            out.append(f'<g stroke="{g("colour")}" stroke-width="3" fill="none" opacity="{op}"><line x1="{x}" y1="{y}" x2="{x}" y2="{tip:.1f}"/>'
                       f'<polyline points="{x-12},{tip+k:.1f} {x},{tip:.1f} {x+12},{tip+k:.1f}"/></g>')
        elif t == "text":
            x, y = g("x"), g("y")
            s = (f'<text x="{x}" y="{y}" font-family="{g("font")}" font-size="{g("size")}" fill="{g("colour")}" '
                 f'text-anchor="middle" letter-spacing="{g("tracking", 2)}">{escape(str(g("text")))}</text>')
            if e.get("mirror") == "in_place":   # x' = 2x - x: flip about the word's own centre
                s = f'<g transform="translate({2*x},0) scale(-1,1)">{s}</g>'
            out.append(f'<g opacity="{op}">{s}</g>')
    body = "".join(out)
    if tl.get("mirror_whole"):   # C2 R6 wrapper
        body = f'<g transform="translate({W},0) scale(-1,1)">{body}</g>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}</svg>'

if __name__ == "__main__":
    tl, out = json.load(open(sys.argv[1])), sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for f in range(tl["frames"]):
        png = resvg_py.svg_to_bytes(svg_string=frame_svg(tl, f), font_files=tl["font_files"], skip_system_fonts=True)
        open(os.path.join(out, f"hud_{f:04d}.png"), "wb").write(bytes(png))
```

**A timeline, in plain words.** One JSON file lists the canvas (`w`, `h`, `frames`), the font files, and the elements. Each element has fixed values (position, colour) and optional `keys`: at frame `f`, a property takes a value. Numbers glide between keys with an ease; text, colours and dash patterns always jump; `"step": true` on a key makes a number jump too. The tested SC27 example (HULL CLEARANCE: the outline snaps from red dashed to green solid on frame 30, the charge bar eases down, the speed arrow drops to a flat tick on frame 40):

```json
{"w": 1920, "h": 804, "fps": 24, "frames": 48, "mirror_whole": false,
 "font_files": ["fonts/B612-Regular.ttf", "fonts/B612Mono-Regular.ttf"],
 "elements": [
  {"id": "outline_iona", "type": "person", "x": 400, "y": 300, "h": 300, "stroke": 3,
   "keys": [{"f": 0, "colour": "#D8322B", "dash": "10 8"}, {"f": 30, "colour": "#58E08A", "dash": "", "step": true}]},
  {"id": "hull", "type": "line", "x1": 250, "y1": 250, "x2": 250, "y2": 650, "colour": "#E8E6DF", "stroke": 3},
  {"id": "label", "type": "text", "text": "HULL CLEARANCE", "font": "B612", "size": 43, "x": 1500, "y": 150,
   "colour": "#E8E6DF", "mirror": "in_place"},
  {"id": "bar", "type": "bar", "x": 1700, "y": 300, "w": 40, "h": 300, "colour": "#E8E6DF",
   "keys": [{"f": 0, "level": 0.6}, {"f": 24, "level": 0.3}]},
  {"id": "speed", "type": "arrow_v", "x": 1500, "y": 600, "colour": "#E8E6DF",
   "keys": [{"f": 0, "length": 200}, {"f": 40, "length": 0, "step": true}]}
 ]}
```

Steps: (1) download the fonts from Google Fonts (github.com/google/fonts, folders `ofl/b612`, `ofl/b612mono`, `ofl/ibmplexsans`), keeping each `OFL.txt` (D4 `asset_licence`); (2) the LLM writes `timeline.json` from the spec, as above; (3) run `python hud_frames.py timeline.json out` (about 6 s for 48 frames); (4) encode: `ffmpeg -framerate 24 -i out/hud_%04d.png -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le hud.mov`; (5) hand to D6 (Rec6 screen-locked, Rec1 pinned); (6) the user checks the first, the state-change and the last frame. Never combine `in_place` words with `mirror_whole`: in the test the two flips cancelled and HULL CLEARANCE read forwards [V, author test]. Shapes the script does not have yet (the wire-frame room, the diamond marker, the vessel capsule, the turn ring) are built from `line` elements, or the LLM adds a new element type and re-renders the test sheet (Recipe 1 step 4) before any shot uses it [J].

### Recipe 4. Browser animation captured frame by frame (Medium; 1-2 h first) [V, author test 2026-09-28]

Use it when the animation already exists as a web page (a designer's SVG, CSS or Lottie file) or is easier to describe as one. Tested 2026-09-28 (Playwright 1.63.0, Chrome Headless Shell 153): 48 transparent 1920×804 PNGs in 3.9 s; an SVG `<set>` snapped red to green exactly on frame 30 (1.25 s × 24); a CSS bar animation landed on the computed height on frames 29, 30 and 47; the corners stayed fully transparent.

1. The LLM writes one HTML page at delivery size with a transparent background and a `showFrame(n)` function that puts every animation at frame `n` [V API, S14, S16; method J]. The tested page (a red-to-green ring and a falling bar):

```html
<!doctype html><html><head><meta charset="utf-8">
<style>
 html,body{margin:0;background:transparent}
 #bar{position:absolute;left:1700px;top:300px;width:40px;height:300px;background:#E8E6DF;
      transform-origin:bottom;animation:fall 2s linear forwards}
 @keyframes fall{from{transform:scaleY(1)}to{transform:scaleY(0.25)}}
</style></head><body>
<svg id="hud" width="1920" height="804" style="position:absolute;left:0;top:0">
 <circle cx="400" cy="300" r="40" fill="none" stroke="#D8322B" stroke-width="3">
  <set attributeName="stroke" to="#58E08A" begin="1.25s" fill="freeze"/>
 </circle>
</svg>
<div id="bar"></div>
<script>
 const FPS = 24;
 function showFrame(n){
   const svg = document.getElementById('hud');
   svg.pauseAnimations(); svg.setCurrentTime(n / FPS);          // SVG animation, seconds
   for (const a of document.getAnimations()) {                  // CSS and Web Animations
     a.pause(); a.currentTime = n * 1000 / FPS; }               // milliseconds
   // Lottie: anim.goToAndStop(n, true);  canvas: draw(n);
 }
</script></body></html>
```

2. The capture script (save as `capture.py`; run `python capture.py page.html out 48`):

```python
"""capture.py page.html out_dir frames - one transparent PNG per frame
(pip install playwright; playwright install chromium)."""
import sys, os, pathlib
from playwright.sync_api import sync_playwright
page_file, out, frames = sys.argv[1], sys.argv[2], int(sys.argv[3])
os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 804}, device_scale_factor=1)
    page.goto(pathlib.Path(page_file).resolve().as_uri())
    page.evaluate("document.fonts.ready")          # wait for web fonts
    for n in range(frames):
        page.evaluate(f"showFrame({n})")
        page.screenshot(path=os.path.join(out, f"hud_{n:04d}.png"), omit_background=True)
    browser.close()
```

3. Encode as Recipe 3 step 4; the user checks the first, the state-change and the last frame against the page. Never screen-record in real time [J]; never pass `animations="disabled"` (rule 25a).

### Recipe 5. Text and wireframes in Blender through the shot camera (Medium; 1-2 h, needs C4 previs)

1. Load the previs camera from `camera_track.json` (D6 `element_layer.py` pattern).
2. The LLM builds a room-sized cube with the Wireframe modifier, and a centre-aligned text object whose X scale of −1 flips it in place (rule 19); emission material in the style guide colour.
3. Animate what the script says (the room sliding up, l.1516); render with transparent film (Render Properties > Film > Transparent), view transform **Standard**, not the AgX default of new files, because Standard adds nothing beyond the display conversion and so keeps the style guide's hex colours (S19; C4 R25 explains the transforms for depth passes), motion blur off; stack screen-locked (D6 Rec6). Check one rendered pixel of the line against its hex before rendering the shot [J].
Only when the POV moves; SC26's still POV ("Nothing moves.", l.1518) needs only Recipe 3 [J].

### Recipe 6. Screens in frame (links D6 Rec1)

1. Generate the device with a dark or pure green screen (C3 §13B; D6 rule 8).
2. Make the content as its own clip at the device's native ratio (monitors, tablet 16:9; CCTV 4:3), sized by rule 10.
3. Screen physics per D6 Rec1 step 5; no scan lines or glitches unless scripted [J]. Pin it (D6 Rec1); match its light on faces (D6 rule 22).

### Recipe 7. Title cards and credits (Easy; 20 min)

1. Title: IBM Plex Sans Medium, capitals, tracking +8%, off-white #EDEBE6 on true black, cap height 6% of picture height (48 px on 804, font size 69 px), optically centred about 2% above the middle; hold and cut per D8 R42-R43 and §9.3 [J; D8]. In numbers for the LLM: a 1920×804 PNG, background #000000, text "THE CATCH" in IBM Plex Sans Medium at 69 px, letter spacing 5.5 px (8% of 69), colour #EDEBE6, centred left to right, baseline at y = 410 (so the 48 px capitals are centred on y = 386, 16 px above the middle line at 402); then open it and check that the letters' top edge is at about y = 362 [J, arithmetic].
2. Credits: IBM Plex Sans Regular; roles 2.5% cap, names 3.2% cap, 3-4 names per card, 72 frames (D8 Rec9 and §9.3); last card carries D4's AI line and D9's CC BY lines (D8 §9.3). Credits are scanned, not read word by word: a card of 4 role-and-name pairs would need about 6-7 s by rule 8, so 72 frames is a deliberate exception for non-plot text; if the user wants every name readable at once, use 3 names and 120 frames [J; flag].
3. Render as PNG (D8 Rec9); never mirrored (rule 17); check spelling of every name against the cast list.
4. For *The Long Places*, check the font covers Turkish: IBM Plex Sans and Mono cover ı İ ş Ş ğ Ğ; B612 lacks all six and Atkinson Hyperlegible lacks İ in the files Google Fonts served [V, author test on 2026-09-27 files]; its 2025 successor, Atkinson Hyperlegible Next (OFL), has all six [V, author test on the Google Fonts file, 2026-09-28]. Check any other face the same way: ask the LLM to "open the font file with fontTools and list which of these letters are missing: ı İ ş Ş ğ Ğ ç Ç ö Ö ü Ü".

### Recipe 8. Resolve by hand (fallback)

Ask the LLM for numbered click steps; send a screenshot after each (D6 rule 10). Import the rendered PNG or ProRes rather than rebuilding in Text+, so the spec survives [J]. The usual shape of the steps [J; Edit-page menu names U, check against your screen]: (1) Media page or File > Import: bring in `hud.mov` or the card PNG; (2) Edit page: drag it onto the track above the plate, starting on the frame the spec names; (3) for a PNG card, set its length to the spec's `hold_frames`; (4) for a HUD, set the clip's composite mode to Add in the Inspector (D6 rule 5); (5) play the shot once at full screen and check the three named frames. If a title truly must be built in Resolve: select the clip, open the Fusion page and, as Blackmagic's page says, "drag a Text+ node into the node tree and type your text" [V, S20]; type the size, tracking and colour from the style guide, never by eye.

### Recipe 9. What to tell the models (image, video and the LLM) [J]

- **To an image or video model, for a device:** describe the device with its screen blank: "the monitor's screen is dark and blank, switched off" for a static shot; "the screen is a flat, evenly lit, pure bright green panel, matte, not glowing; nothing covers its corners at the start" for a moving one (D6 Rec1). For the helmet: "a clear glass helmet visor, nothing drawn on it". Never write "HUD", "hologram", "sci-fi interface" or the script's words (RECEIVING, HULL CLEARANCE) into a video prompt, because models then invent their own text and glow, which you must paint out before your graphic goes on (D6 principle 2; C2 §7.1).
- **To a model, for a practical light that carries the code** (SC23's shell light): "a small round lamp on the shell, glowing red"; then grade or comp it to the style guide's hex (rule 15), because hex codes are not followed (B2 §13.3).
- **To the LLM, for a graphic:** "Write `timeline.json` for `hud_frames.py` from this spec: [paste the W1 row]. Use only the style guide's colours, sizes and timings; text exactly as quoted; every colour change a jump on one frame; mirror words `in_place` if the register says so; list any value you invented." Then: "Render it, and show me frames [first], [state change] and [last]."
- **To the LLM, for checking:** "Run VG1-VG9 on this shot's `graphics[]` and print every failure with its fix."

## 8. Fields this subject adds to the breakdown

Enums follow C5 R29 (lowercase snake_case, `"none"`). IDs are script-issued.

| Level | Field | Meaning | Allowed values / example |
|---|---|---|---|
| film | `ui_style_guide` | The approved style guide | `UISG-CATCH-V01` |
| film | `ui_mirror_policy` | How each class flips in each era | `{world_picture: whole, suit_words: in_place, suit_geometry: plate_true, non_diegetic: none}` (the same values as `mirror_mode`, so VG5 compares like with like) |
| film | `graphic_register[]` | Every graphic ID | `[GR-VISOR, GR-WRIST, GR-CCTV-SHAFT, ...]` |
| graphic | `graphic_id` | Script-issued ID | `GR-` + name |
| graphic | `device` | Where it appears | `visor` \| `wrist` \| `monitor` \| `tablet` \| `cctv` \| `phone` \| `sign` \| `file` \| `card` \| `credits` |
| graphic | `diegesis` | Story world or audience only | `diegetic` \| `non_diegetic` |
| graphic | `maker` | Whose handedness made it | `world` \| `turned` \| `none` |
| graphic | `lock` | How it is fixed | `screen_locked` \| `surface_pinned` \| `world_locked` |
| graphic | `teaches[]` | Meanings it teaches and where | `{meaning: "outline = what the engine carries", scene: SC18, level: 2}` |
| graphic | `states[]` | Named states with look | `{state: limit, colour: state_limit, dash: "10 8"}` |
| graphic | `font`, `font_licence` | Face and licence (D4) | `B612`, `ofl_1_1` |
| shot | `graphics[]` | Graphics in this shot | objects below |
| shot graphic | `graphic_id`, `state_in`, `state_out` | Which graphic, entry and exit states | `GR-VISOR`, `go`, `go` |
| shot graphic | `events[]` | Frame-numbered changes | `{frame: 30, element: outline_iona, change: "limit -> go"}` |
| shot graphic | `text_exact[]` | Script words shown, with line and whether the audience must read them | `{text: "HULL CLEARANCE", line: 1559, must_read: yes}`; `{text: "STOP", line: 730, must_read: no}` |
| shot graphic | `invented_text[]` | Words not in the script | `"02:47:13"` \| `"none"` |
| shot graphic | `mirror_mode` | Flip method | `none` \| `in_place` \| `whole` |
| shot graphic | `on_frame_cap_pct` | Smallest must-read cap in the final frame | 4.1 |
| shot graphic | `read_time_s`, `on_screen_s` | Required (derived) and planned | 6.0, 7.5 |
| comp job (D6) | layer `kind` / `source_ref` | Link to the render | `hud` or `screen_content`; `GR-VISOR` job |

**Validator checks** [J]: **VG1** every `text_exact` item with `must_read: yes` has `on_frame_cap_pct` ≥ 4 (the first version tested every scripted word, which failed W3's secondary FLIGHT TEST at 3.5% and SC13's unreadable STOP). **VG2** `on_screen_s` ≥ `read_time_s` for every `must_read: yes` item (doubled when mirrored). **VG2a** every `invented_text` item is at or below 2.5% cap and smaller than every `text_exact` item in the shot (rule 4). **VG3** colour keys in timelines are steps. **VG4** no asymmetric icon from §4.1 in a mirrored graphic unless listed. **VG5** `mirror_mode` matches `ui_mirror_policy` for maker, class and era; never `in_place` plus a whole flip of the same layer (D6 VC1 counts flips). **VG6** `font_licence` present in D4 `asset_licence`. **VG7** `text_exact` letters match the quoted line; punctuation differences are listed for the user. **VG8** every meaning used at L2 or above appears in an earlier `teaches[]`. **VG9** `diegesis: non_diegetic` never has `mirror_mode` ≠ `none`.

**How these fields meet the blueprint's TEXT record** (`design/blueprint.md` §5.5: `kind, words, on, reader, plot_critical, emphasis, method, look, animation, translate`) [J]. The blueprint's record is the one the pipeline stores; this file's fields are the design detail behind it, so they map rather than duplicate: `text_exact.text` → TEXT `words` (story-written); `must_read` → `plot_critical`; B4 level → `emphasis`; `device` → `kind` (`visor`, `wrist`, `monitor` are shared; `tablet` and `cctv` → `screen`; `file` → `document`; `card` and `credits` → `title_card`; the CCTV clock → `timestamp`; `sign` → `sign`; `phone` → `screen`); `mirror_mode` and `ui_mirror_policy` → the `WR-*` rules of the blueprint's K04 (`WR-SCREEN-TEXT-B`, `WR-TITLES`); `states[]` and `events[]` → `animation`; the style-guide ID → `look`; `invented_text` → a TEXT whose `words` the AI writes with `origin: invented` (blueprint §5, "Conditional writers"); every graphic here → `method: composite`. The blueprint's `make_text_graphics.py` draws static TEXT items normal and mirrored; animated displays use Recipe 3 or 4.

## 9. Checklists

**Per graphic:** script lines quoted • one meaning per icon and colour • taught before use • symmetric or vertical elements where mirrored; no play, rewind or fast-forward glyphs (pause is safe) • must-read words ≥ 4% cap in the smallest shot • invented text ≤ 2.5% and smaller than every scripted word • tabular digits • no yellow light or saturated blue • red dashed, green solid; practical lights have a second cue or a logged decision (rule 15a) • inventions logged • OFL licence recorded (`ofl_1_1`) • every letter present in the font • test sheet approved at 640 px.

**Per shot:** timeline matches the edit • state changes on single frames • reading time met (VG2) • one mirror method • graphics after every AI pass • blur and grain matched (D6 Rec9) • centre clear on decision beats; eyes never covered in exterior close-ups (B3 §8.1) • face glow follows state • inside the safe area • after a payoff, no rhyme, hold or signal recalling it (rule 2a) • recordings on a display flipped whole, the display's own words in place.

**Per card:** exact text • IBM Plex Sans • hold per D8 • never mirrored • names spelled from the cast list • AI line on the last card.

## 10. Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Brown or yellow flash between red and green | Cross-faded state colour | Cut on one frame (rule 12) |
| Viewers miss the red/green payoff | Colour-only code; colour-blind viewers | Dash red, solid green, brightness gap (rule 13) |
| Mirrored words read forwards | In-place flip plus whole flip | One method per layer (VG5) [V, author test] |
| "12" read as "21" | Mirrored digits | Pair with a vertical arrow; hold longer |
| Play icon reads as rewind | Asymmetric icon flipped | Pause glyph or none (rule 20) |
| Drawn hull opposite the real ship | Whole flip of plate-registered geometry | In-place words (rule 19) |
| Numbers jiggle | Proportional digits | B612 Mono (B612 and IBM Plex Sans also have equal-width digits; Atkinson Hyperlegible does not) [V, author test] |
| Words unreadable on phone | Designed full screen, seen small | Rule 10; 640 px check |
| Letters garbled or "corrected" | AI pass after the graphic | Graphics last (D6 principle 2) |
| Frames skipped or doubled | Real-time screen capture | Seek each frame (Recipe 4) |
| Every captured frame shows the animation's end state | Playwright `animations="disabled"` fast-forwards finite animations | Leave the option at its default (rule 25a) [V, S15] |
| Hex colours shift in a Blender render | AgX view transform (default in new files) | View transform Standard (Recipe 5) [V, S19] |
| Rewind reads as fast-forward in a mirrored feed | Flipped ◀◀ glyph | No transport glyphs; picture and clock run backwards (W7) |
| Colour-blind viewers miss the shell light | A single practical changing hue | Rule 15a (position cue) or let the drawn outlines carry it |
| Soft CCTV text | Pillow softens stroked text even with `fontmode = "1"` [V, author test] | Offset black copies, then white (W2) |
| Missing letters (ı, ş) | Font lacks glyphs | Recipe 7 step 4 |
| Title card flipped in era B | Mirror rule applied to non-diegetic text | VG9 |
| Look-alike of a real app | Copied platform design | Invented, generic UI (D4 §3.3) |
| Countdown too fast to read | 12 m/s to 0 at 9.8 m/s² takes 1.2 s [J] | Stretch time with cutaways (W1) |

## 11. Worked examples

### W1. *The Catch*: the visor and wrist arc, SC17 to SC28

`GR-WRIST`, `GR-VISOR` and Saye's monitor (`GR-MON-CAMFEED`, SC17) share one language. Timings at 24 fps [J]; reading times from Recipe 2, mirrored; B4 levels in brackets.

| Scene, line | Script | Graphic and animation | Words, time needed |
|---|---|---|---|
| SC17 l.919-921, 946 | "a small diagram of the camera leaving a horizontal line" / "Beside the line: PASSAGE FLOOR." / "The camera's diagram turns." / "a second line: the ship's deck" | Precursor teaching (L1-L2): level line; symmetric camera icon moving with the recording; "turns" as a 10-frame card flip (X scale 1 to −1, a picture of a mirror turn); deck line dashed, dipping. Whole picture flipped | PASSAGE FLOOR 6.0 s, on screen through both recordings |
| SC18 l.1028 | "On Iona's wrist, a simple display: her outline, the engine, a bar of charge." | Teaching shot (L2): outline draws on green (12 frames), engine snaps on, bar fills with its reserve tick (12 frames), then a 48-frame clean hold before her finger moves (B4). No words: mirror-proof | None |
| SC18 l.1030, 1071 | "finds the recorded carriage, then her way home" / "The two places hold steady on her wrist." | Recording thumbnail (whole-flipped); green way-home line; two diamond markers | None |
| SC20 l.1122 | "Three green lights answer on her wrist." | Three dots snap green, 6 frames apart (L1) | None |
| SC23 l.1269-1273; SC24 l.1378 | "Saye's recorded face appears on her wrist." / "Behind Saye, Iona's own recording shows the cabinet." / "Its new recording opens on her wrist." | World recordings in the wrist display's recording frame: flipped whole once (rule 18), Saye mirrored like every era-B Saye; the cabinet seen inside Saye's message is a ship object (turned), so pre-reverse it inside the picture before the flip, as B1's table does for Jude on the tablet (B1 §10.2; D6 rule 16) [J; flag]; lip-sync per D3. Opening a recording: frame draws on (6 frames), picture cuts in; no play glyph (rule 20) | None |
| SC23 l.1296 | "She checks the load on her visor." | L1, under 36 frames: her outline green, a second outline red and dashed [design choice; flag] | None |
| SC23 l.1331, 1342 | "A light on the shell turns RED." / "The light turns GREEN." | Practical light in the UI hues, snapped (rule 15), with a second cue or a logged colour-only decision (rule 15a); teaches red = over the limit (L2) | None |
| SC24 l.1396-1412 | "her way home. Still green." / "The field outlines the canister." / "The charge bar falls." / "She deletes the way home." | Neutral outline widens (18 frames, eased); bar falls (24 frames) and stops hard; green line erases from its far end back to her (10 frames), face glow out with it (B2 Ex4) | None |
| SC25 l.1432-1436 | "She selects the other marked place on her visor" / "Two outlines. Hers green. Its own red." | Marker selected (4 frames); path draws on (12); the figure's outline, 1.4 times her height, snaps on red dashed; hold 48 frames (L2) | None |
| SC25 l.1464 | "Her outline alone: green." | Figure outline off (4 frames) | None |
| SC25 l.1488, 1500 | "two outlines turn green, one inside the other. A little to spare." / "The outlines stay green. Just." | Payoff (L3): vessel capsule draws on at her chest (8 frames), then both snap green on one frame; the bar shows the trip's cost as a hollow segment, a margin left above the reserve tick; hold 72-96 frames, nothing added (B4 R23). With the container the margin shrinks to a sliver (12 frames) | None |
| SC26 l.1506, 1516 | "a wire-frame room marked RECEIVING hangs beyond the ledge" / "the drawing of the room slides upwards. Goes on sliding." | Wireframe room in perspective, label flipped in place; slides up with an ease-in (story physics, not a measured scale) | RECEIVING 5.0 s from the first VISOR VIEW |
| SC26 l.1520-1524 | "She selects the crossing preview." / "Her projected outline turns red" / "Inside solid rock." / "She cancels the preview." | Preview outline (2 px, dash 4/6) drops past a tunnel line into a horizontally hatched rock band, snaps red; the rock is the largest area (D6 W5); hold 60 frames (L2); off in 4 | None |
| SC26 l.1528-1532 | "On her wrist, she opens the recording of the toy carriage. Down. Turn. Up." / "Sets a different path. Out from the ship. One turn. Up." | `GR-WRIST` insert: the SC18 thumbnail opens to fill the display, showing the SC12 demonstration in B1 §10.6's framing ("the same framing becomes the recording on her wrist"); a world picture, so whole-flipped once (rule 18), and the F's orientation follows the F decision (B1 §10.2, C2 §7.4 item 1); no play or progress glyph (rule 20). Then the visor path redraws (next row) | The F only; no words |
| SC26 l.1534-1536, 1549 | "TURN, below. CROSS AT 0, beside RECEIVING. The reserve bar drops, and stops, and a sliver is left above the line." / "It draws the turn round everything inside her outline." / "Only an arrow points towards it." | Path draws out, down, turn ring, up (20 frames); marks 6 frames apart, words flipped in place; bar drops (18 frames) into the reserve and stops with a sliver above the empty line; ring round the outline (12); room off the top edge leaves a vertical arrow | TURN 5.0 s; CROSS AT 0 7.0 s, cumulative through SC26-27 (same place and size) |
| SC26 l.1538-1540, 1544 | "She turns the wrist screen towards the vessel. Plays the carriage once. Its F reverses." / "The animal touches the moving picture through the glass." / "She taps the vessel's outline inside her own." | B4 M06's payoff (L3): an insert with the wrist screen, the vessel's glass and the animal's limb in one frame, the F large enough to read its orientation (rule 6 for a letter: at least 4% cap in the final frame); the recording plays once at its real speed, with no added signal (B4 R23: "Its F reverses" is the script marker). Then a `GR-VISOR` or `GR-WRIST` beat: the vessel capsule inside her outline takes the selected state (+2 px, 4 frames) on her tap; no new meaning (§5.2 teaching order) | None; the F held at least 2.5 s after it reverses (rule 8 for one mirrored "word" would ask 5 s: the reversal, not the letter, is what is read) [J] |
| SC27 l.1559-1561 | "On the visor: HULL CLEARANCE." / "The whole outline clears the hull's last projection. Turns green." | Side view, lower left: hull as a vertical line with projections, on the side the ship is in the plate; outline (vessel and container inside) drifts with the real drift; snaps green the frame the gap opens | HULL CLEARANCE 6.0 s: label up at least 6 s before "She fires." |
| SC27 l.1567 | "BLACK. Not distance. Not sky. Nothing." | Graphics off with the picture [J] | None |
| SC27 l.1581-1591 | "The arrow points up." / "Beside it: UPWARD SPEED, in metres per second. Twelve. Six. Three." / "The room settles round her outline like a coat." / "Nought." | Label flipped in place; B612 Mono values with a vertical arrow whose length follows the speed; each value its own VISOR VIEW insert of 48 frames, cut against her face, the vessel and the pump's strokes; the room box settles round the outline (30-frame ease-out); 0 with a flat tick | UPWARD SPEED 6.0 s cumulative; 48 frames per number; 0 reads unflipped |
| SC27 l.1597 | "The reserve bar empties." | Bar reaches the empty line (12 frames) | None |
| SC28 l.1620-1622 | "On the wall above Saye: RECEIVING." / "Iona looks at it. Reads it again." | Painted world sign, era C, forward, framed like the turned-meal label (B1); no further visor insert | RECEIVING 2.5 s, read twice |

Mirror state for every `GR-VISOR` and `GR-WRIST` word, SC18 to SC28: flipped in place (§4.3); every recording shown on the wrist (the carriage, Saye's messages) is a world picture and is flipped whole, once (rule 18), inside its own frame on the display. Physics note: at the film's stated gravity ("The pull is the same.", l.939), slowing from 12 m/s to 0 takes about 1.2 s, while the readouts need about 7 s of screen time: time stretched on purpose (A4 R6), carried by cutaways [J, arithmetic].

### W2. *The Catch* SC13: the security playback overlay (`GR-CCTV-SHAFT`)

Script: "Security footage, paused: a camera above the top gate, looking straight down the shaft." (l.674); "A small figure in the cage drives her elbow into STOP." (l.730); "Iona pauses the recording with the remote." (l.742); "She looks back at the screen. Lets the recording run." (l.824).

- **Two layers** [J]: (a) the camera's burnt-in overlay, drawn into the one master take (B1 §10.4, D8 §9.2); (b) the monitor's player: a symmetric pause glyph while paused, nothing while playing (a flipped play triangle reads as rewind).
- **Burnt-in overlay:** time only, 24-hour with seconds, B612 Mono at 15 px on the native 640×480, Pillow `fontmode = "1"`, four black copies offset 1 px then white: three colours, no softening [V, author test]. Digits about 11 px, 18 px after D8's resize to 804 high (2.3%, ambient). It ticks once per real second at 12 fps, so the fall's length can be counted but need not be read. Bottom-left in the source (bottom-right after the flip), clear of the centre where the cage, the puck and Eli's empty hand must read.
- **Invented text:** the clock value (for example "02:47:13") [flag]; no camera name.
- **Mirror:** an era-A recording of world events shown in era B: whole flip once, overlay included (B1 §10.4: do not "fix" it). "STOP" on the control box is unreadable from above and needs nothing.
- **Freeze:** "Iona pauses" cuts to the frozen frame with the pause glyph on; the clock stops; D8 §9.2 gives the 60-frame hold.

### W3. *The Catch* SC17: "NELL ROWAN. FLIGHT TEST." (`GR-FILE-NELL`)

Script: "Saye opens a file. The same woman, much younger. A flight suit. Unsmiling." / "NELL ROWAN. FLIGHT TEST." (l.988-990); "She leaves the file open. The date is nineteen years old." (l.998).

- **Layout** [J]: a plain records window in the institute's language: photo left, "NELL ROWAN" in B612 Bold, "FLIGHT TEST" beneath, a small date field. Keeping the script's full stops is a user decision (VG7).
- **Size:** the name is the hero, 5% cap in the insert; FLIGHT TEST 3.5%; the date 2%, an invented value [flag], because backwards digits will not read and the photo already says "much younger".
- **Mirror:** world picture, era B: whole flip, photo included (C2).
- **Timing:** 4 words mirrored = 8.0 s: one clean insert of at least 4 s, then the file stays in frame, same size and place, over "You knew her?" / "I sent her." No subtitle (D8 R53). The name is spoken in SC24 ("Nell is here.", l.1381).

### W4. *The Catch* SC12: the dish labels (`GR-MON-DISHES`)

"The left is labelled CONTROL. The right: VALE. CAR. STEERING WHEEL." (l.608). World picture, whole flip; put CONTROL on the right of the source so it lands left (D6 rule 17); size by rule 10 for the widest shot that must read it. The long label (8.0 s mirrored) only needs to look like a label with her name, because Iona's "That's off my wheel." (l.624) carries it [J]. In SC13 ("the two dishes are still up", l.676) both are ambient.

### W5. *The Catch*: title and end cards (`GR-CARD-TITLE`, `GR-CARD-END`)

"= THE CATCH" (l.488) after "> CUT TO BLACK." (l.486); "= THE END" (l.1852). Recipe 7 step 1 fills D8's `card_spec`: `"font": "IBM Plex Sans Medium", "font_licence": "ofl_1_1", "cap_height_pct": 6`. Not mirrored, though inside era B (VG9). Two words need 3.0 s; D8's 72 frames holds.

### W6. *The Long Places*: Yusuf's tally screen (chapter VI) and Dr. Arat's phone (chapter IV)

Text: "He had built the counter in four evenings that month, at the dig house: a tally screen, a toggle for each opening along, and condition tags he named himself — LAMPS (COLD/WARM), AIR (STILL/MOVING), GENERATOR, PEOPLE (n)." and "*19 Aug, 05:50, still, lamps cold, generator off — 41.*"

- **Maker and look** [J]: a streamer's homemade phone app: default-looking controls, one accent colour, no brand; invented, never a real platform's look (D4 §3.3).
- **Hierarchy:** the count is the hero, one numeral at 8-10% cap in the insert so "41" reads in under a second; tags as small chips with the text's exact names and chosen state ("LAMPS: COLD"), 3% cap; toggles ambient.
- **Font:** IBM Plex Sans, which covers the story's Turkish names [V, author test].
- **Timing:** the story is 40 versus 41: cut from a "40" insert to a "41" insert of the same framing, 48 frames each (Recipe 2 asks at least 24 per unmirrored value), no animation on the number (rule 9).
- **Phone (chapter IV, Dr. Arat landing):** "her phone, waking, showed one missed call from the dig-house number, Monday, 21:14, no message." A lock-screen notification in three lines, "Missed call" / "Dig house" / "Monday, 21:14": the time exact, the contact name adapted from "the dig-house number" and logged as the file's wording [J]; 6 words, so 5.0 s by rule 8 (the first version said 3.5 s). The phone's own look is generic, never a real maker's lock screen (D4 §3.3). D6 W6 covers Yusuf's livestream chat. No mirror world here: every mirror field is `none`.

### W7. *The Catch* SC14-SC16: the tablet feed's overlay (`GR-CCTV-JUDE`)

Script: "Iona on her bed, a tablet propped on her knees. On it: the camera in Jude's room." (l.832); "On the tablet a nurse appears beyond Jude's glass. Stops at the empty space." (l.875); "Iona runs the picture back. Stops it on the hand under his arm." (l.877).

- **Overlay** [J]: the same burnt-in design as W2 (time only, 24-hour with seconds, B612 Mono, three colours, bottom corner), because the institute made both cameras (rule 5). D6 W2 also burns in a camera label; that is invented text, allowed only at or below 2.5% and logged (rule 4), and this file would leave it out: the user decides (§12).
- **Mirror:** a world picture, flipped whole once with the feed, overlay included, so the clock reads backwards; Jude pre-reversed inside it (D6 W2, rule 16).
- **The rewind (SC16):** no transport glyph at all, since a flipped ◀◀ reads as ▶▶ (§4.1); the picture runs backwards and the burnt-in clock counts down with it, as a real recording's would (D6 W2). The stop on "the hand under his arm" is a cut to the held frame; the clock stops.
- **Size and time:** the clock is ambient (about 2.3% cap after fitting, like W2); nothing in the overlay is read, so no reading time applies.

## 12. For the writer/user; conflicts; unverified

**Decisions needed**
- Visor and wrist words backwards SC18-SC28 (this file), or forward throughout by a technician's setting shown in SC18?
- Add the red second outline to SC23's load check (a design choice, not in the script)?
- SC23's shell light: one lamp changing hue as written (colour-only for colour-blind viewers), or D18's two lamps, red below and green above (rule 15a)?
- Full stops in "NELL ROWAN. FLIGHT TEST." on screen or not; the date value; the CCTV clock value.
- A camera label on the SC15 tablet feed (D6 W2) or time only (W7)?
- The carriage F's orientation (B1 §10.2, C2 §7.4 item 1): it decides what the SC26 wrist recording shows when "Its F reverses".
- The cabinet inside Saye's SC23 message: pre-reversed (this file, by B1's rule for turned things in world pictures) or not?
- Credits: 72 frames per 3-4 names (D8; scanned, not read) or 3 names at 120 frames (readable by rule 8)?
- Sample the SC01 tag red and replace `state_limit`.

**Conflicts with other files**
- **Visor snap (B1 §16 and §10.6 (c)):** B1 recommends the visor text snap readable after the final turn; that contradicts l.1536 ("It draws the turn round everything inside her outline. Herself. The suit.") and l.1569 ("The same view, from the same side."). This file keeps the suit's words backwards; the first forward world word of era C is SC28's wall sign, rhyming with the turned SC12 meal label. D6 has adopted this (rules 19a-19b, Rec6, W5); B1 is not yet updated.
- **C2's era-C table** omits the suit: by the same logic its lettering stays mirrored in era C (C2 §7.4 item 3 reasons the same way about the container).
- **D6 W5's first draft** flipped the SC26 HUD layer whole; D6 now flips words in place (resolved). D6 W5 hatches the rock at 90°, this file horizontally: both survive a flip; choose one in the style guide.
- **D6 W2** burns a camera label into the SC15 feed; W2 and W7 here use time only. Invented text either way (rule 4); the user decides.
- **Reading time:** A4 R8 and B1 R2 differ; this file takes the longer (as D8-R43 does) and doubles it for mirrored text (A4 R8, D8-R53). The blueprint's checker computes its own floor: `text_floor` = max(2.0, 1.0 + characters ÷ 13), or at least 2.0 + 0.5 × words when `emphasis` ≥ 2, doubled if mirrored. For must-read graphics (emphasis 2-3) the two agree within a tenth of a second; for emphasis 0-1 the blueprint is shorter (PASSAGE FLOOR at L1: 4.0 s against 6.0 s here). The checker's floor is the enforced minimum; this file's times are the design targets for hero graphics.
- **Licence enum:** D8 §9.3's `card_spec` writes `"font_licence": "OFL-1.1"`; D4 `asset_licence` and this file use `ofl_1_1` (C5 R29 lowercase snake_case). Use `ofl_1_1`.
- **Title hold:** D8 holds THE CATCH 72 frames; D9's `sparse` music option wants about 96 (D8 conflict 12). Either passes rule 8 (3.0 s for two words).
- **D8 conflicts 15 and 16** (Resolve scripting reason, the doubling's citation): corrected here in rules 25 and 8.
- **D18:** proposes tick and cross marks and a two-lamp shell light for colour-blind viewers (D18 §7.4, row "Load fits or not"); this file keeps dash-versus-solid for the drawn outlines (rule 13) and puts the lamp to the user (rule 15a). D18 open question 15 (fonts for other scripts) is answered by the style guide's `fallback_by_script` (Noto Sans JP or SC).
- **Blueprint TEXT record:** field names differ; §8 maps them. The blueprint's `make_text_graphics.py` covers static text only; animated displays need Recipe 3 or 4, which the blueprint does not yet list.

**Unverified or judgment**
- Resolve Edit-page menu paths [U]. Blender text conversion to curve or mesh [J, not re-checked]. Noto Sans JP and SC glyph coverage not tested. All sizes, timings, colours and layouts are [J]. The scripts were tested on generated frames, not on a finished comp of *The Catch*. S4 is further reading only.

## Sources (checked 2026-09-27; re-opened 2026-09-28 unless noted)

- S1. Territory Studio (David Sheldon-Hicks, Marti Romances, Andrew Popplestone), Q&A, Sci-fi Interfaces, 2020. https://scifiinterfaces.com/2020/06/23/scifi-interfaces-qa-with-territory-studio/ [V]
- S2. Jayse Hansen, conversation, Pushing Pixels, 2012. https://www.pushing-pixels.org/2012/06/01/the-craft-of-screen-graphics-and-movie-user-interfaces-conversation-with-jayse-hansen.html [V]
- S3. Mark Coleran interview, Pushing Pixels, 21 Dec 2021. https://www.pushing-pixels.org/2021/12/21/pragmatic-futurism-and-screen-graphics-interview-with-mark-coleran.html [V, read 2026-09-28]
- S4. Shedroff and Noessel, *Make It So: Interaction Design Lessons from Science Fiction*, Rosenfeld Media, 2012. https://rosenfeldmedia.com/books/make-it-so/ [V: exists; further reading]
- S5. Fagerholt and Lorentzon, *Beyond the HUD: User Interfaces for Increased Player Immersion in FPS Games*, master's thesis, Chalmers, 2009. Record: https://odr.chalmers.se/items/d5fe6889-4cc6-49c2-ba56-0d759e2f37eb ; PDF: https://odr.chalmers.se/server/api/core/bitstreams/fd267f70-c295-4eae-ae01-af5db676e61d/content [V: record exists; its four-way taxonomy (diegetic, non-diegetic, spatial, meta) read through summaries, U]
- S6. BBC Subtitle Guidelines, §9.2.1-9.2.2 font size (line height 7-8% of active video height; `tts:lineHeight="120%"`; presentation 0.6-0.8×; 0.5° default). https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/ [V]
- S7. National Eye Institute, Color blindness. https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/color-blindness [V]
- S8. Machado et al. 2009 deuteranopia matrix, as published in the Colour library. https://colour.readthedocs.io/en/develop/generated/colour.matrix_cvd_Machado2009.html [V]
- S9. Material Design 3 motion tokens, material-web source. https://raw.githubusercontent.com/material-components/material-web/main/tokens/versions/v0_192/_md-sys-motion.scss [V]
- S10. B612 font family. https://github.com/polarsys/b612 ; B612 Mono (OFL) in Google Fonts: https://github.com/google/fonts/tree/main/ofl/b612mono [V]
- S11. IBM Plex (OFL, Reserved Font Name "Plex"). https://github.com/IBM/plex ; Atkinson Hyperlegible (OFL): https://github.com/googlefonts/atkinson-hyperlegible ; Atkinson Hyperlegible Next (OFL, 2025): https://github.com/googlefonts/atkinson-hyperlegible-next ; Noto Sans JP and SC (OFL): https://github.com/google/fonts/tree/main/ofl/notosansjp , .../ofl/notosanssc [V: licence files]
- S12. SIL OFL FAQ 1.1 and 1.1.2. https://openfontlicense.org/ofl-faq/ [V]
- S13. resvg. https://github.com/linebender/resvg ; resvg-py (MIT): https://github.com/baseplate-admin/resvg-py [V]
- S14. Lottie Animation Community. https://lottie.github.io/ ; lottie-web (MIT). https://github.com/airbnb/lottie-web [V]
- S15. Playwright `page.screenshot`. https://playwright.dev/docs/api/class-page ; option texts from the docs source https://github.com/microsoft/playwright/blob/main/docs/src/api/params.md [V]
- S16. MDN `SVGSVGElement.setCurrentTime()`: https://developer.mozilla.org/en-US/docs/Web/API/SVGSVGElement/setCurrentTime ; `Document.getAnimations()`: https://developer.mozilla.org/en-US/docs/Web/API/Document/getAnimations [V]
- S17. Remotion licence. https://github.com/remotion-dev/remotion/blob/main/LICENSE.md [V]
- S18. Manim Community configuration. https://docs.manim.community/en/stable/guides/configuration.html [V]
- S19. Blender 5.2 LTS Manual: Text https://docs.blender.org/manual/en/latest/modeling/texts/introduction.html ; Wireframe modifier https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/wireframe.html ; Freestyle https://docs.blender.org/manual/en/latest/render/freestyle/introduction.html ; colour management: Blender 4.0 release notes ("The AgX view transform has been added, and replaces Filmic as the default in new files.") https://developer.blender.org/docs/release_notes/4.0/color_management/ and the 5.2 manual's Displays and Views page ("Standard: Does no extra conversion besides the conversion for the display.") https://docs.blender.org/manual/en/latest/render/color_management/displays_views.html [V]
- S20. Blackmagic Design, DaVinci Resolve Fusion page. https://www.blackmagicdesign.com/products/davinciresolve/fusion [V]
- S21. Pillow `ImageDraw.fontmode`. https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html [V]
- S22. Author tests, 2026-09-27, re-run 2026-09-28: `hud_frames.py` (resvg-py 0.5.0, Pillow 12.3.0, ffmpeg 7.0.2 static) on three timelines at 1920×804; ProRes 4444 round trip; Recipe 4 page and `capture.py` (Playwright 1.63.0, Chrome Headless Shell 153); fonts from Google Fonts (github.com/google/fonts `ofl/`), cap heights, digit widths and Turkish coverage read with fontTools; Pillow aliasing test (`stroke_width` against offset copies); luminance (WCAG formula) and deuteranopia (Machado 2009, severity 1) computation: red #D8322B against green #58E08A 2.82:1, simulated 2.24:1 (#8F8023 against #CEC290).
- Library: A3, A4, B1, B2, B3, B4, C2, C3, C4, C5, D2, D3, D4, D5, D6, D8, D9, D18 (sections as cited); `design/blueprint.md` §5 (TEXT record, conditional writers), K04 (`WR-*` rules), text floor; *The Catch* (workshop revision) and *The Long Places* (revised final), every quoted line re-matched 2026-09-28.
