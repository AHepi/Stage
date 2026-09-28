# Film rules

## At a glance

<The camera, light and sound rules for the whole film, in three or four sentences.>

## Camera

<How the camera treats each person, the normal lens and height, and what is saved for later.>

## Light and colour

<One line for each place and time: its light and its colours.>

## Sound

<Music, silence and the sound of each place.>

## Saved for later

<The few strong choices kept for one or two moments, and where they are spent.>

Below this line: details for the AI and the checker. You never need to read them.

### CAMSYS
- frame_shape_why: <standard: text>
- lens_type: <standard: spherical or anamorphic>
- lens_family: <standard: numbers separated by commas>
- normal_lens_mm: <standard: millimetres>
- step_change: from: <standard, one line each: an ID of SCENE (SC10)> | family: <numbers separated by commas> | why: <text>
- default_height: <quick: text>
- default_move: <quick: static>
- banned: <quick, one line each: text> | why: <text>
- camera_speed: <quick: real_time>
- break: <standard: SCnn, or SCnn "<quote anchor>"> | what: <text> | because: <text>
- time_rule: <standard: text>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> CAMSYS: The film's camera system: frame shape reason, lenses, baseline, banned choices, the one break. (camera system; one per project; lives in 10 Film rules.md.)
> status: draft, approved, stale, omitted.

### CAMRULE <CR- and capitals and hyphens, like CR-ELI> <a short plain title>
- character: <standard: an ID of CHARACTER (CH-IONA)>
- in_control: <standard: text>
- losing_control: <standard: text>
- never: <standard: short phrases separated by commas>
- closest: <standard: one word from the note> | at: <SCnn "<exact story words, 3 or more, found once in that scene>">
- limit_before: <standard: one word from the note>
- eyeline: <standard: text>
- because: <standard: IDs of any record ID, separated by commas>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> CAMRULE: How the camera treats one character. (character camera rule; ID CR- and capitals and hyphens, like CR-ELI; lives in 10 Film rules.md.)
> Allowed values:
> - closest (first part): extreme_wide, wide, medium_wide, medium, medium_close_up, close_up, extreme_close_up, insert
> - limit_before: extreme_wide, wide, medium_wide, medium, medium_close_up, close_up, extreme_close_up, insert
> status: draft, approved, stale, omitted.

### RESERVE <RC- and 2 digits, like RC-01> <a short plain title>
- choice: <quick: text>
- match: <quick: <field> = <value>, or manual>
- max_uses: <quick: text> | fraction: <a number from 0 to 1>
- allowed_in: <quick: IDs or text>
- never_on: <quick: IDs of any record ID, separated by commas, or none>
- because: <quick: IDs of any record ID, separated by commas>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> RESERVE: A choice saved for special moments, with its uses rationed. Always includes the two film-level reserves: the non-insert extreme close-up and the push-in. (saved choice; ID RC- and 2 digits, like RC-01; lives in 10 Film rules.md.)
> status: draft, approved, stale, omitted.

### LENS <LX- and 2 digits, like LX-01> <a short plain title>
- mm: <standard: millimetres>
- only_in: <standard: IDs of SETUP (SC10-SU02) or SCENE (SC10), separated by commas>
- why: <standard: text>
- because: <standard: IDs of any record ID, separated by commas>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> LENS: A lens outside the family and where it is allowed. (lens exception; ID LX- and 2 digits, like LX-01; lives in 10 Film rules.md.)
> status: draft, approved, stale, omitted.

### LOOK <LK- and capitals and hyphens, like LK-SAYE-KITCHEN-NIGHT> <a short plain title>
- for: <standard: an ID of LOCATION (LOC-SAYE-KITCHEN)>
- time: <standard: text>
- look_block: <standard: text; 2 or 3 sentences, at most 60 words>
- main_light: <standard: text> | colour: <text> | quality: <hard or soft> | from: <OBJECT_NAME, north_wall, east_wall, south_wall, west_wall or ceiling>
- neutral_white: <standard: text>
- contrast: <standard: low, medium, medium_high, high or extreme>
- fill: <standard: none, low, medium or high>
- stays_dark: <standard: text>
- palette: <standard: text>
- accent_allowed: <standard: text>
- light_cue: <standard, one line each: SCnn "<exact story words, 3 or more, found once in that scene>"> | change: <text> | why: <text>
- style_picture: <add-on, storyboards or AI video: a file name>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> LOOK: The light, colour and texture of a place at a time; its look block is pasted word for word into every prompt there. (look; ID LK- and capitals and hyphens, like LK-SAYE-KITCHEN-NIGHT; lives in 10 Film rules.md.)
> status: draft, approved, stale, omitted.

### VISUAL <VS- and the sequence ID, like VS-SQ03> <a short plain title>
- sequence: <standard: an ID of SEQUENCE (SQ03)>
- frame_value: <standard: a number from 1 to 5>
- saturation: <standard: a number from 1 to 5>
- temperature: <standard: warm, neutral, cool or mixed>
- dominant: <standard: word>
- accent: <standard: word, or none>
- main_light: <standard: hard, soft or mixed>
- contrast: <standard: low, medium, medium_high, high or extreme>
- exit: <standard: text>
- sub_row: <detailed, one line each: an ID of SCENE (SC10)> | frame_value: <a number from 1 to 5> | saturation: <a number from 1 to 5> | temperature: <warm, neutral, cool or mixed> | dominant: <word> | accent: <word> | contrast: <low, medium, medium_high, high or extreme>
- space: <standard: deep, flat, limited or ambiguous>
- component: <standard, one line each: one word from the note> | plan: <hold, progress or contrast> | why: <text>
- counterpoint: <standard: text, or none>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> VISUAL: The colour-script row and visual-structure plan for a sequence. (visual plan; ID VS- and the sequence ID, like VS-SQ03; lives in 10 Film rules.md.)
> Allowed values:
> - component (first part): space, line, shape, tone, colour, motion, rhythm
> status: draft, approved, stale, omitted.

### SOUNDPLAN
- music_policy: <quick, the user's answer, set through a choice: none, sparse, scored or source_only>
- clip_audio: <quick, code writes it; in a chat without code you write it: text>
- voice_policy: <quick, the user's answer, set through a choice: designed_only, designed_plus_own_clone or designed_plus_consented_clones; default designed_only>
- device_budget: <standard, one line each: cut_to_black, true_silence or freeze> | max: <a number>
- rupture_plan: <standard, one line each: an ID of SCENE (SC10)> | device: <text>
- loudness_target: <detailed: text>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> SOUNDPLAN: The film's music policy, voice policy, device budget and planned ruptures. (sound plan; one per project; lives in 10 Film rules.md.)
> status: draft, approved, stale, omitted.

### LADDER
- rung: <standard, one line each: SCnn "<exact story words, 3 or more, found once in that scene>"> | size: <one word from the note> | hold: <short, medium, long or hold> | why: <text>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> LADDER: Each scene's main turn with planned size and hold; the ladder escalates by size and hold together. (ladder; one per project; lives in 10 Film rules.md.)
> Allowed values:
> - rung size: extreme_wide, wide, medium_wide, medium, medium_close_up, close_up, extreme_close_up, insert
> status: draft, approved, stale, omitted.

END OF FILE | Film rules | 8 records
