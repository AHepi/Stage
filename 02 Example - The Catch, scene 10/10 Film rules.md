# Film rules

## At a glance

The frame: 2.39 to 1.
The camera: static, at Iona's eye height; when she kneels, the camera kneels, on the normal lens of 50 millimetres.
Music: none.

## Camera rules for each person

- Eli: in control: partial framings, profile or three-quarter, eyes well off the lens, one hand often out of frame or behind something, static; losing control: his closest and most frontal framing at the confession in scene 13 and then his first look near the lens; never: push in; closest: close-up, scene 13, "Now he looks at her."
- Iona: in control: static frames, or smooth moves at her pace, at her eye height; the camera inspects what her hands inspect; losing control: handheld, closer, on a wider lens, only on the broken rung and in the car and with the figure in her room; never: dutch; closest: extreme close-up, scene 13, "She can always outwait him."
- Jude: in control: warm medium two-shots with Iona; losing control: static and patient framing while he is wounded; never: handheld; closest: close-up, scene 15, "Jude opens his eyes."
- Dr Saye: in control: centred or on a third, static, on the 50 from farther back than anyone else and often beside screens she controls; losing control: off-centre and closer, only in the recorded message where she has lost her answering voice; never: low angle and push in; closest: close-up, scene 24, "Saye has lost the voice she uses for answers."

## Saved choices

- Saved choice 1, the reflection two-shot: the perfectly symmetrical profile two-shot along the dividing plane, on the 85 from well back; used at most 2 times.
- Saved choice 2, the extreme close-up: the non-insert extreme close-up (a film-level saved choice); used at most 3 times.
- Saved choice 3, the push-in: the push-in (a film-level saved choice); used in at most a quarter of the scenes.

## Lens exceptions

- The early 85 (a lens exception): the 85 millimetre lens, only in scene 10, camera A; the reflection two-shot needs the camera well back through the wild wall, on the same lens and distance as the rings shot in scene 29 that it rhymes with.

## Looks

- Saye's kitchen before dawn: A bare, tidy kitchen before dawn, lit only by one small warm lamp low on the table. A faint cool blue shows in the window over the counter. Pale walls, a white fridge, pale wood and steel; the corners fall into soft shadow while every face stays readable.

## Visual plan by group of scenes

- The visual plan for group of scenes 3: dominant: grey; accent: green; contrast: high; space: limited.

## Sound

- Voices: designed only.

## The ladder

- Scene 10, "Her face changes.": close-up, held long; the turn happens inside her mouth, so it lands close and is held; the film's tightest size waits for scene 13 and its longest hold for the last scene.

Below this line: details for the AI and the checker. You never need to read them.

### CAMSYS
- frame_shape_why: the film's pairs face each other across tables and glass, and a very wide frame puts them at its opposite edges; rows of glass rooms and a figure taller than a door need its width
- lens_type: spherical
- lens_family: 35, 50
- normal_lens_mm: 50
- step_change: from: SC13 | family: 35, 50, 85 | why: from the confession on, the singles move to the 85, closer but private
- default_height: Iona's eye height; when she kneels, the camera kneels
- default_move: static
- banned: dolly_zoom | why: it would read as a quotation of another film
- banned: dutch | why: the film's wrongness is handedness, and a tilted horizon would blur that one clear signal
- banned: slow_motion | why: playback is always real time; the fall is played in real time
- banned: orbit | why: nothing in this story is seen from a circling view
- camera_speed: real_time
- break: SC26 "She pushes gently away from the rail." | what: the camera floats free with her for the first time, by her choice | because: stillness has meant control and floating has meant helplessness; at the climax floating becomes her choice
- time_rule: expanded time is built from overlapping real-time slices of one master grey preview, never slow motion
- note: The 24 millimetre exceptions (the cage, the ship's wides, the figure in Iona's room) are lens exceptions outside this excerpt.
- status: approved
- locked: yes

### CAMRULE CR-IONA Iona
- character: CH-IONA
- in_control: static frames, or smooth moves at her pace, at her eye height; the camera inspects what her hands inspect
- losing_control: handheld, closer, on a wider lens, only on the broken rung, in the car and with the figure in her room
- never: dutch
- closest: extreme_close_up | at: SC13 "She can always outwait him."
- limit_before: close_up
- eyeline: just off the lens on the side of the person she answers, never into it
- because: CH-IONA, PLAN, RC-02
- status: approved
- locked: yes

### CAMRULE CR-SAYE Saye
- character: CH-SAYE
- in_control: centred or on a third, static, on the 50 from farther back than anyone else, often beside screens she controls
- losing_control: off-centre and closer, only in the recorded message where she has lost her answering voice
- never: low angle, push_in
- closest: close_up | at: SC24 "Saye has lost the voice she uses for answers."
- limit_before: medium_close_up
- eyeline: level, on the person she is testing, or for a long moment on the thing of risk
- because: CH-SAYE
- status: approved
- locked: yes

### CAMRULE CR-ELI Eli
- character: CH-ELI
- in_control: partial framings, profile or three-quarter, eyes well off the lens, one hand often out of frame or behind something, static
- losing_control: his closest and most frontal framing at the confession in scene 13, then his first look near the lens
- never: push_in
- closest: close_up | at: SC13 "Now he looks at her."
- limit_before: medium_close_up
- eyeline: his near-lens look is saved for scene 13
- because: CH-ELI, PLAN, RC-03
- status: approved
- locked: yes

### CAMRULE CR-JUDE Jude
- character: CH-JUDE
- in_control: warm medium two-shots with Iona
- losing_control: static, patient framing while he is wounded
- never: handheld
- closest: close_up | at: SC15 "Jude opens his eyes."
- limit_before: medium_close_up
- eyeline: on Iona
- because: CH-JUDE
- status: approved
- locked: yes

### RESERVE RC-01 The reflection two-shot
- choice: the perfectly symmetrical profile two-shot along the dividing plane, on the 85 from well back
- match: frame_detail = symmetrical_profile
- max_uses: 2
- allowed_in: SC10-SU01, the raised hands; and scene 29, the rings at the glass
- never_on: none
- because: MO-RINGS, PL-07, LX-01
- status: approved
- locked: yes

### RESERVE RC-02 The extreme close-up
- choice: the non-insert extreme close-up (a film-level saved choice)
- match: size = extreme_close_up
- max_uses: 3
- allowed_in: main turns only; the first in scene 13
- never_on: CH-ELI
- because: PLAN, CR-IONA
- status: approved
- locked: yes

### RESERVE RC-03 The push-in
- choice: the push-in (a film-level saved choice)
- match: move = push_in
- max_uses: share | fraction: 0.25
- allowed_in: main turns that happen inside a person; the first in scene 13
- never_on: CH-ELI
- because: PLAN, CR-ELI
- status: approved
- locked: yes

### LENS LX-01 The early 85
- mm: 85
- only_in: SC10-SU01
- why: the reflection two-shot needs the camera well back through the wild wall, on the same lens and distance as the rings shot in scene 29 that it rhymes with
- because: RC-01, PL-07
- status: approved
- locked: yes

### LOOK LK-SAYE-KITCHEN-NIGHT Saye's kitchen before dawn
- for: LOC-SAYE-KITCHEN
- time: before dawn
- look_block: A bare, tidy kitchen before dawn, lit only by one small warm lamp low on the table. A faint cool blue shows in the window over the counter. Pale walls, a white fridge, pale wood and steel; the corners fall into soft shadow while every face stays readable.
- main_light: the lamp | colour: warm, about 2,700 kelvin | quality: soft | from: LAMP
- neutral_white: balanced between the lamp and the window, so the lamp reads warm and the window blue
- contrast: medium_high
- fill: low
- stays_dark: the corners, the hall doorway and the ceiling
- palette: grey, off-white and pale wood, the lamp's amber, the window's blue
- accent_allowed: the mint's green, and only once it is in the lamplight
- light_cue: SC10 "Iona holds the lamp." = SC10-B02 | change: the lamp is in Iona's hand over Jude, so the light moves when she moves | why: the story puts the only light in her hand
- light_cue: SC10 "It's where it should be." = SC10-B03 | change: Iona sets the lamp back on the table between the women and the light steadies | why: the addition that frees her hands and lights both women alike
- light_cue: SC10 "She picks up her phone." = SC10-B09 | change: the phone's screen lights Saye's hand and chin | why: the story gives her the phone
- status: approved
- locked: yes

### VISUAL VS-SQ03 The wrong world
- sequence: SQ03
- frame_value: 2
- saturation: 2
- temperature: cool
- dominant: grey
- accent: green
- main_light: mixed
- contrast: high
- exit: cut to black and the title card
- sub_row: SC10 | frame_value: 3 | saturation: 2 | temperature: mixed | dominant: grey | accent: green | contrast: medium_high
- space: limited
- component: space | plan: hold | why: the passage, the street, the car and the kitchen are all seen squarely and kept flat, so the only contrast is the reversed world itself
- component: line | plan: hold | why: horizontals and frontal planes; in the kitchen the table is the mirror's centre line
- component: colour | plan: contrast | why: after the cool streets the kitchen brings the first warm light and the one green, the mint
- component: rhythm | plan: progress | why: the cutting quickens through the tests and stops dead on the mint
- counterpoint: none
- note: The other rows of this sequence, scenes 7 to 9, are outside this excerpt.
- status: approved
- locked: yes

### SOUNDPLAN
- music_policy: none
- clip_audio: No music in any clip.
- voice_policy: designed_only
- device_budget: cut_to_black | max: 2
- device_budget: true_silence | max: 2
- device_budget: freeze | max: 2
- rupture_plan: SC26 | device: drop_out, the ship's hum
- status: approved
- locked: yes

### LADDER
- rung: SC10 "Her face changes." = SC10-B07 | size: close_up | hold: long | why: the turn happens inside her mouth, so it lands close and is held; the film's tightest size waits for scene 13 and its longest hold for the last scene
- note: The other rungs of the ladder, one for each scene with a main turn, are outside this excerpt.
- status: approved
- locked: yes

END OF FILE | 10 Film rules | 13 records
