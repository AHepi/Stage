# Digest D12: Diegetic UI and on-screen graphics (28 Sept 2026)

Source: `research/D12_diegetic_ui_graphics.md` (fact-checked 28 Sept 2026). Refs: **P#** principle (§2), **R#** rule (§3), **Rec#** recipe (§7), **VG#** check (§8), **W#** example (§11). **[V]** verified or run 27-28 Sept; **[U]** unverified; **[J]** judgment. Tested: resvg-py 0.5.0, Pillow 12.3.0, ffmpeg 7.0.2, Playwright 1.63.0.

## 1. Scope

1. Designs every graphic the audience must read or see (visor, wrist display, monitors, CCTV overlays, tablet feeds, files, signs, title cards, credits) so it reads at a glance, teaches its meaning before the payoff, and survives *The Catch*'s mirror world.
2. Gives one style-guide template per film (grid, OFL fonts, B2 motif colours, icons, states, frame timings, mirror behaviour per era), filled for *The Catch*, plus 9 recipes an LLM can run for a non-technical user (Python + SVG default, headless browser, Blender, Resolve by hand).
3. Adds graphic fields and 10 validator checks, mapped onto the blueprint's TEXT record; D6 lays the graphic into the shot, D8 places it in the cut.

## 2. Rules

**Terms** [§1]: *diegetic* = inside the story world; *hero* vs *ambient* = must be read vs texture; *cap height* = capital height as % of finished picture height; *tabular digits* = equal-width digits; *screen-locked / surface-pinned / world-locked* = fixed to frame / corner-pinned to a device / 3D through the shot camera; *whole flip* = mirror a layer, *in-place flip* = mirror each word about its centre; *era A/B/C* = before the cage turns / Iona turned / after her second turn; *L0-L3* = B4 emphasis.

**Principles**
1. [P1] If story and plausibility conflict, then story wins, because "it works for the story – which is the most important – and reality comes in as a second" (Hansen) [V].
2. [P2] If a graphic carries a plot point, then make it readable in about 3 s (shapes and colour, then words, then numbers), because hero screens "are only in shot for about 3 seconds" (Territory Studio) [V].
3. [P3, R2] If a later scene depends on reading a graphic, then give its meaning an L2 teaching shot at least one scene earlier, recorded in `teaches[]`, because suspense needs knowledge (B4 R7).
4. [P5] If a graphic may be mirrored, then build everything except words and digits symmetric or vertical, because only then does the flip change nothing but the text.
5. [P6, R5] If a display is world-made, then design it as its makers would (clinical, plain) in one language for monitors, suit and wrist, because one consistent maker makes it plausible [J].
6. [P8, P9] If AI passes remain, then add graphics after all of them, rendered from a frame-numbered timeline, because AI passes redraw letters (D6 P2) and frame-driven renders repeat exactly.
7. [P10] If choosing a look, then start from something familiar and add one step (cockpit plainness, B612; no holograms), because "You look for those hooks where people are familiar with something, and then add to that" (Coleran) [V].

**Design and meaning**
8. [R1] If the script names what a display shows ("her outline, the engine, a bar of charge", l.1028), then draw exactly those, because extras dilute a 3-second read.
9. [R2a] If a display appears after its motif's L3 payoff (visor in SC26-27 after SC25), then frame it only as legibility needs, up to L2, with no rhyme, hold or signal recalling the payoff, because a loud return explains it twice (B4 R26).
10. [R3] If a meaning already has a B2 motif colour, then reuse it and never give it a second meaning, because red = "A limit, and its cost", green = "Fits, allowed, go" film-wide (B2 §8.4).
11. [R4] If a word is not in the script (timestamp, unit, date), then keep it at or below 2.5% cap, smaller than every scripted word in the shot, logged, never plot-bearing, because invented text competes with scripted text [J; limit raised from 2% on 28 Sept].

**Legibility and timing**
12. [R6] If the audience must read a word, then its cap height in the finished frame is at least 4% of picture height (5% preferred), because BBC subtitle sizes land at 3.5-4.7% of a 2.39 picture [V source, J arithmetic].
13. [R7] If text is secondary, then 2.5-3% cap; if texture, under 1.5%, because readable-but-unimportant text makes the audience hunt [J].
14. [R8] If a word must be read, then hold it for max(2 s + 0.5 s × words, 1 s + characters ÷ 12), doubled if mirrored (A4 R8, D8-R53); count across shots only if place and size stay and one hold lasts the unmirrored time, because a cut restarts the eye's search [J].
15. [R9] If a readout changes value, then use tabular digits and change it on a cut frame, because proportional digits jiggle and rolling numbers cannot be read.
16. [R10] If a device is small in frame, then cap on device ≥ required on-frame cap ÷ device's share of frame height (CONTROL on a monitor 30% of frame height: 4 ÷ 0.30 ≈ 13%), because full-screen designs shot wide lose every word.
17. [R11] If a graphic must work on phones, then check a still at 640 px wide, because short films are watched small.

**Colour and states**
18. [R12] If an element changes colour state, then cut on one frame, never cross-fade, because red-to-green passes through khaki-yellow (#98895A) and B2 keeps yellow "Painted only, never a light."
19. [R13] If red and green carry meaning, then red is dashed and darker, green solid and brighter, because the pair is only 2.2:1 under deuteranopia and "About 1 in 12 men" have colour vision deficiency (NEI) [V].
20. [R14] If an element is selected, previewed or erased, then use weight, dash or opacity, never a new hue, because the motif code has taken every hue.
21. [R15] If a practical light shares the code, then match its hue in comp or grade, because models do not follow hex codes (B2 §13.3).
22. [R15a] If a practical light carries red/green with no second cue, then add a position cue (D18: two lamps, red below, green above) or log a colour-only decision and let the drawn outlines carry it, because a single hue change fails colour-blind viewers; the user decides [flag].
23. [R16] If a state changes, then add no blink, pulse or sting unless scripted ("Iona's wrist chimes", l.1374), because a script marker allows zero added signals (B4 R23).

**Mirror**
24. [R17] If a graphic is non-diegetic, then never mirror it, because the rule belongs to what Iona sees (blueprint `WR-TITLES`).
25. [R18] If a world-made display shows a picture of the world (recording, feed, file, dishes), then flip the whole picture once in era B, because it is world content (B1 §10.4; D6 rules 15-17).
26. [R19] If a world-made display draws things also in the plate (her outline, hull, room), then flip only its words in place and keep geometry true to the plate, because a whole flip puts the drawn hull opposite the real one.
27. [R20] If an element is asymmetric (play, rewind or fast-forward glyph, horizontal arrow, spinner, 45° hatching, seven-segment digits), then replace it, because a flipped play reads as rewind and a flipped seven-segment 2 as 5.
28. [R21] If a device sits inside Iona's outline at a turn (suit, visor, wrist, engine), then its mirror state relative to her never changes, because the turn is drawn "round everything inside her outline. Herself. The suit." (l.1536).

**Production**
29. [R22] If a graphic is 2D, screen-locked or corner-pinned, then draw it with Python + SVG (Rec3), because it is exact, free and needs no GUI [V].
30. [R23, R25a] If a graphic exists as web, Lottie or canvas animation, then capture it headless, seeking every frame, with Playwright's `animations` left at default, because real-time capture drops frames and `"disabled"` fast-forwards finite animations "to completion" [V].
31. [R24] If a graphic must change perspective with a moving camera, then build it in Blender through `camera_track.json` (Rec5; C4 Route 5), because 2D cannot fake it.
32. [R25] If a card or credit needs no animation, then render a PNG and use Resolve only to place it, because an LLM cannot drive free Resolve 21.1 from outside (external scripting, Workflow Integrations, MCP are Studio-only; console scripting stays free) [V via D8].

## 3. Breakdown fields

Enums lowercase `snake_case`, empty = `"none"` (C5 R29); IDs script-issued (C5 R23). These are the design detail behind the blueprint's TEXT record (mapping in §8 of the source).

| Level | field_name | Meaning | Allowed values / example |
|---|---|---|---|
| film | `ui_style_guide` | Approved style guide | `UISG-CATCH-V01` |
| film | `ui_mirror_policy` | How each class flips per era | `{world_picture: whole, suit_words: in_place, suit_geometry: plate_true, non_diegetic: none}` |
| film | `graphic_register[]` | Every graphic ID | `[GR-VISOR, GR-WRIST, GR-CCTV-SHAFT, ...]` |
| graphic | `graphic_id` | Script-issued ID | `GR-` + name |
| graphic | `device` | Where it appears | `visor` \| `wrist` \| `monitor` \| `tablet` \| `cctv` \| `phone` \| `sign` \| `file` \| `card` \| `credits` |
| graphic | `diegesis` | Story world or audience only | `diegetic` \| `non_diegetic` |
| graphic | `maker` | Whose handedness made it | `world` \| `turned` \| `none` |
| graphic | `lock` | How it is fixed | `screen_locked` \| `surface_pinned` \| `world_locked` |
| graphic | `teaches[]` | Meanings taught, where | `{meaning: "outline = what the engine carries", scene: SC18, level: 2}` |
| graphic | `states[]` | Named states with look | `{state: limit, colour: state_limit, dash: "10 8"}` |
| graphic | `font`, `font_licence` | Face and licence (D4) | `B612`, `ofl_1_1` |
| shot | `graphics[]` | Graphics in the shot | objects below |
| shot graphic | `graphic_id`, `state_in`, `state_out` | Which graphic; entry, exit state | `GR-VISOR`, `go`, `go` |
| shot graphic | `events[]` | Frame-numbered changes | `{frame: 30, element: outline_iona, change: "limit -> go"}` |
| shot graphic | `text_exact[]` | Script words, line, must-read flag | `{text: "HULL CLEARANCE", line: 1559, must_read: yes}` |
| shot graphic | `invented_text[]` | Words not in the script | `"02:47:13"` \| `"none"` |
| shot graphic | `mirror_mode` | Flip method | `none` \| `in_place` \| `whole` |
| shot graphic | `on_frame_cap_pct` | Smallest must-read cap in final frame | `4.1` |
| shot graphic | `read_time_s`, `on_screen_s` | Required (derived); planned | `6.0`, `7.5` |
| comp job (D6) | layer `kind`, `source_ref` | Link to the render | `hud` \| `screen_content`; `GR-VISOR` job |

**Blueprint mapping** [J]: `text_exact.text` → TEXT `words`; `must_read` → `plot_critical`; level → `emphasis`; `device` → `kind` (`tablet`/`cctv`/`phone` → `screen`, `file` → `document`, `card`/`credits` → `title_card`); `invented_text` → TEXT `origin: invented`; all `method: composite`.

**Validator** [J]: **VG1** `must_read: yes` items have `on_frame_cap_pct` ≥ 4. **VG2** `on_screen_s` ≥ `read_time_s` for must-read items (doubled when mirrored). **VG2a** invented text ≤ 2.5% and smaller than every `text_exact` item. **VG3** colour keys are steps. **VG4** no asymmetric §4.1 icon in a mirrored graphic unless listed. **VG5** `mirror_mode` matches `ui_mirror_policy` for maker, class, era; never `in_place` plus a whole flip of one layer (D6 VC1). **VG6** `font_licence` in D4 `asset_licence`. **VG7** `text_exact` letters match the quoted line; punctuation differences listed. **VG8** every meaning used at L2+ appears in an earlier `teaches[]`. **VG9** `non_diegetic` never has `mirror_mode` ≠ `none`.

## 4. Procedures

1. **Style guide and register (Rec1, 30-60 min, once).** Ask: *"List every script line where something is displayed, printed, labelled, projected or shown on a screen, with line number and exact words. For each: device, maker, era (A/B/C), whether the plot depends on reading it, and the scene that first teaches its meaning."* Then: *"Fill the style guide template (D12 §5.1) from the style bible (D5), B2's motif code and the device list. Only OFL fonts. Mark every invented value."* A script issues `GR-` IDs. The user approves one test sheet (every icon in every state, on black and mid-grey, full size and 640 px). Accept: one icon and one state per meaning; no asymmetric icon in a mirrored display; must-read ≥ 4% cap. Template (§5.1, exact):

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

   Timing basis: Material Design 3 tokens 50-1,000 ms, medium1 250 ms = 6 frames at 24 fps, emphasized easing `cubic-bezier(0.2, 0, 0, 1)` [V]; film graphics sit at the slow end.
2. **Spec one graphic (Rec2, 10-20 min).** Quote the lines; list elements, states, frame events. T = max(2 + 0.5 × words, 1 + characters ÷ 12), doubled if mirrored (CROSS AT 0: 3 words, 10 characters → 3.5 s, mirrored 7.0 s = 168 frames). Changing numbers: ≥ 24 frames per value, 48 mirrored, 0 reads both ways. Too short? Words early, change late. Accept: VG1, VG2, VG2a, VG3; write `read_time_s`, `on_screen_s`.
3. **Animated HUD with Python + SVG (Rec3, default; 30-60 min first, 10 min after).** (1) Download fonts from github.com/google/fonts (`ofl/b612`, `ofl/b612mono`, `ofl/ibmplexsans`), keep each `OFL.txt` (D4). (2) LLM writes `timeline.json`: numbers glide with an ease between keys, text/colours/dashes jump, `"step": true` makes a number jump. Tested example (source §7 Rec3, exact):

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

   (3) Run `python hud_frames.py timeline.json out` (script in source §7 Rec3; `pip install resvg-py`). (4) Encode: `ffmpeg -framerate 24 -i out/hud_%04d.png -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le hud.mov`. (5) Hand to D6 (Rec6, Rec1). (6) User checks first, state-change and last frames. Never combine `in_place` with `mirror_whole` (the flips cancel). New shapes: build from `line` elements or add a type and re-render the test sheet.
4. **Browser capture (Rec4, 1-2 h first).** LLM writes one HTML page at delivery size, transparent, with `showFrame(n)`: SVG `svg.pauseAnimations(); svg.setCurrentTime(n / FPS)`; CSS/Web Animations `a.pause(); a.currentTime = n * 1000 / FPS` for each `document.getAnimations()`; Lottie `anim.goToAndStop(n, true)`; canvas `draw(n)`. `capture.py` (source §7 Rec4) opens it at 1920×804, `device_scale_factor=1`, waits for `document.fonts.ready`, calls `showFrame(n)`, saves `page.screenshot(..., omit_background=True)`. Run `python capture.py page.html out 48`; encode as step 3.
5. **Blender (Rec5, only when the POV moves).** Load `camera_track.json`; cube with Wireframe modifier; centre-aligned text with X scale −1 for an in-place flip; emission in the style colour; animate what the script says; Film > Transparent, view transform **Standard** (not the AgX default), motion blur off; check one pixel against its hex.
6. **Screens in frame (Rec6).** Generate the device dark or pure green (D6 rule 8); make content as its own clip at native ratio (monitor/tablet 16:9, CCTV 4:3), sized by R10; D6 Rec1 screen physics and pin; no scan lines or glitches unless scripted; match face light (D6 rule 22).
7. **Cards and credits (Rec7, 20 min).** Title: 1920×804 PNG, #000000, IBM Plex Sans Medium 69 px, capitals, spacing 5.5 px, #EDEBE6, centred, baseline y = 410; hold per D8-R42/R43. Credits: Plex Regular, roles 2.5% cap, names 3.2%, 3-4 names, 72 frames; last card D4 AI line and D9 CC BY lines. Never mirrored. Turkish: Plex and Atkinson Hyperlegible Next cover ı İ ş Ş ğ Ğ; B612 lacks all six [V]. Check any font: *"open the font file with fontTools and list which of these letters are missing: ı İ ş Ş ğ Ğ ç Ç ö Ö ü Ü"*.
8. **Resolve by hand (Rec8).** Numbered click steps, a screenshot after each; import the PNG or ProRes above the plate, card length = `hold_frames`, HUD composite mode Add; menu names [U].

## 5. Checklists

**Per graphic:** lines quoted • one meaning per icon and colour • taught before use • symmetric or vertical where mirrored; no play, rewind or fast-forward glyphs • must-read ≥ 4% cap in the smallest shot • invented ≤ 2.5%, smaller than scripted words • tabular digits • no yellow light, no saturated blue • red dashed, green solid; practical lights have a second cue or a logged decision • inventions logged • `ofl_1_1` recorded • every letter in the font • test sheet approved at 640 px.
**Per shot:** timeline matches the edit • state changes on single frames • VG2 reading time • one mirror method per layer • graphics after every AI pass • blur and grain matched (D6 Rec9) • centre clear on decision beats; eyes never covered in exterior close-ups (B3 §8.1) • face glow follows state • inside safe area x 96-1824, y 40-764 • no payoff recall after the payoff • recordings on a display flipped whole, the display's own words in place.
**Per card:** exact text • Plex • D8 hold • never mirrored • names from the cast list • AI line last.
**Failure signs** (§10): brown flash = cross-fade; mirrored words reading forwards = double flip; end-state frames = `animations="disabled"`; hex shift in Blender = AgX; soft CCTV text = Pillow `stroke_width`; missing ı or ş = font coverage.

## 6. Saying it to AI models

- **Image/video model, device:** static: "the monitor's screen is dark and blank, switched off"; moving: "the screen is a flat, evenly lit, pure bright green panel, matte, not glowing; nothing covers its corners at the start" (D6 Rec1); helmet: "a clear glass helmet visor, nothing drawn on it". Never write "HUD", "hologram", "sci-fi interface" or display words into a video prompt: models invent text and glow [J].
- **Practical light:** "a small round lamp on the shell, glowing red", then grade to the hex (R15).
- **LLM, graphic:** *"Write `timeline.json` for `hud_frames.py` from this spec: [paste the W1 row]. Use only the style guide's colours, sizes and timings; text exactly as quoted; every colour change a jump on one frame; mirror words `in_place` if the register says so; list any value you invented."* Then *"Render it, and show me frames [first], [state change] and [last]."*
- **LLM, check:** *"Run VG1-VG9 on this shot's `graphics[]` and print every failure with its fix."*

## 7. The Catch

**Decisions made** [J unless noted]
- **Style guide:** visor 1920×804, centre 768×482 clear, schematics lower left, readouts upper right; wrist 800×500 at 1600×1000, always an insert on her glove. UI **B612** (cockpit face; EPL, EDL, OFL [V]), numbers **B612 Mono**, cards **IBM Plex Sans** (OFL); 4% cap = B612 43 px, Plex 46 px. `ui_neutral` #E8E6DF 85%, `state_go` #58E08A solid, `state_limit` #D8322B dashed 10/8 (placeholder); no yellow light or saturated blue. Face glow follows state, dies with the deleted way home (B2 Ex4).
- **Teaching order:** levels and moving icons SC17; outline, engine, charge SC18 (wordless, 48-frame clean hold); green lights SC20; red then green as load limit SC23; outline around objects SC24; vessel capsule SC25. After SC25 no new colour or state meaning; new shapes only if labelled by the script or picturing the plate.
- **Mirror policy:** era B world pictures (dishes, playback, feed, Nell file, recordings on the wrist) flipped whole once; suit graphics words in place, geometry true; the suit turns with her, so visor and wrist words stay backwards through SC27 (l.1006, l.1536). SC28's wall RECEIVING is the first untouched world word to read forward, rhyming with SC12's turned meal label (l.639).
- **W1 arc (SC17-SC28):** SC25 payoff: capsule draws on (8 frames), both outlines snap green on one frame, hold 72-96 frames, nothing added; SC26 preview red inside hatched rock, 60 frames; TURN 5.0 s, CROSS AT 0 7.0 s; the carriage recording on the wrist whole-flipped, "Its F reverses" played once, no added signal (B4 M06 L3); SC27 HULL CLEARANCE up ≥ 6 s before "She fires."; UPWARD SPEED 6.0 s; Twelve, Six, Three as 48-frame inserts against cutaways (1.2 s of physics stretched to ~7 s, A4 R6); "Nought." a flat tick.
- **W2/W7 CCTV and tablet:** time only, B612 Mono 15 px on 640×480, 1 px black offset copies then white [V], ~2.3% after resize, flipped whole with the footage; pause glyph only; rewinds shown by picture and clock running backwards.
- **W3 Nell file:** NELL ROWAN 5% cap, FLIGHT TEST 3.5%, date 2%; flipped whole; 8.0 s (insert ≥ 4 s, then held in frame); no subtitle. **W4:** CONTROL placed right in the source so it lands left. **W5:** cards Plex Medium 6% cap, 72 frames, never mirrored.
- **Long Places W6:** Yusuf's "40" then "41" inserts, 48 frames each; Dr. Arat's phone (chapter IV) "Missed call" / "Dig house" / "Monday, 21:14", 5.0 s; no mirroring.

**Flagged for the user**
1. Visor and wrist words backwards SC18-SC28 (default) or forward via a technician's setting shown in SC18.
2. The red second outline in SC23's load check (not in the script).
3. SC23 shell light: one lamp as written (colour-only) or D18's two lamps (R15a).
4. Full stops in "NELL ROWAN. FLIGHT TEST."; the file date; the CCTV clock value; a camera label on the SC15 feed (D6 W2) or none.
5. The carriage F's orientation (B1 §10.2, C2 §7.4 item 1): decides the SC26 wrist recording.
6. Pre-reverse the cabinet inside Saye's SC23 message (default yes, B1's rule for turned things in world pictures).
7. Credits: 72 frames per 3-4 names (scanned) or 3 names at 120 frames (readable).
8. Sample the SC01 tag red to replace `state_limit`.

## 8. Conflicts and open questions

1. **B1 §16 / §10.6 (c):** recommends the visor snap readable after the final turn; D12 keeps it backwards (l.1536, l.1569). D6 has adopted D12 (rules 19a-19b, Rec6, W5); B1 not yet updated.
2. **C2 era table:** era C omits the suit; by C2's own §7.4 item 3 logic its lettering stays mirrored.
3. **D6:** W5 hatches vertically, D12 horizontally (both mirror-safe; pick one); W2 adds a camera label to the SC15 feed, D12 uses time only (flag 4). D6's whole-flip HUD is resolved.
4. **Blueprint text floor:** max(2.0, 1 + characters ÷ 13), or ≥ 2.0 + 0.5 × words at emphasis ≥ 2, doubled if mirrored: same as D12 for must-read graphics, shorter at emphasis 0-1 (PASSAGE FLOOR: 4.0 s vs 6.0 s). The checker enforces its floor; D12's times are design targets.
5. **Licence enum:** D8 §9.3 `card_spec` writes `"OFL-1.1"`; D4 and D12 use `ofl_1_1`. Use `ofl_1_1`.
6. **Title hold:** D8 72 frames vs D9 `sparse` ~96; both pass R8.
7. **D8 conflicts 15-16:** corrected in D12 R25 and R8.
8. **D18:** proposes tick/cross marks and a two-lamp shell light; D12 keeps dash vs solid (R13) and puts the lamp to the user (R15a). D18 open question 15 answered by `fallback_by_script` (Noto Sans JP or SC, OFL; glyph coverage untested).
9. **Blueprint:** TEXT field names differ (mapping §3 above); `make_text_graphics.py` covers static text only, so animated displays need Rec3 or Rec4, which the blueprint does not yet list.
10. **Credits vs R8:** a 4-pair credit card needs 6-7 s by R8; D8 gives 3 s. Treated as scanned text (flag 7).
11. **Unverified:** Resolve menu names; Blender text-to-mesh [J]; Noto coverage. Sizes, timings, colours, layouts [J]; scripts tested on synthetic frames only.

## 9. Section map

| Need | Source section |
|---|---|
| Fact-check note, tags, what builds on what | top, §0 |
| Terms | §1 |
| Principles P1-P10 | §2 |
| Rules R1-R25a | §3 |
| Mirror table per element; *Catch* policy; why nothing snaps readable | §4.1-4.3 |
| Style-guide template; *Catch* filled | §5.1-5.2 |
| Tools, licences, versions | §6 |
| Recipes Rec1-Rec9 (scripts, timeline, page, prompts) | §7 |
| Fields, blueprint mapping, VG1-VG9 | §8 |
| Checklists | §9 |
| Failure modes | §10 |
| W1 visor/wrist arc; W2 CCTV; W3 Nell file; W4 dishes; W5 cards; W6 Long Places; W7 tablet | §11 |
| Decisions, conflicts, unverified | §12 |
| Sources S1-S22 | end |
