# Scene NN - <place>

## At a glance

<What happens and where it turns, in three or four sentences; then how many beats and shots, and how long it runs.>

## The shots, one line each

<shot 150, close-up, 15 seconds, the turn: Iona chews, stops, chews once more; "Not mint."; we stay on her through Saye's answer>

## Why it's shot this way

<Three to six lines, each naming what in the story it serves, with the story's own words in quotes.>

## Small choices I made

<One line for each addition or staging choice the story does not state, and how to change it.>

Below this line: details for the AI and the checker. You never need to read them.

> Step 7 writes SCENE (design fields; its status and locked stay on its copy in 04 Scene list.md), PART, BEAT, SPEECH (prose only), MOVE, SETUP and SHOTLIST. Step 8 writes SHOT and CUT, in this file or in batch files named Scene NN - <place> - shots NNN-NNN.md with the same plain part and divider.

### SCENE <SCnn> <the place, in plain words>
- location: <quick: an ID of LOCATION (LOC-SAYE-KITCHEN)>
- sub_area: <detailed: text>
- look: <standard: an ID of LOOK (LK-SAYE-KITCHEN-NIGHT)>
- value: <quick, one line each: an ID of VALUE (SC10-V1)> | name: <text> | core: <yes or no> | open: <---, --, -, 0, +, ++ or +++> | close: <---, --, -, 0, +, ++ or +++> | turns_at: <an ID of BEAT (SC10-B07)> | kind: <action, revelation or none>
- want: <standard, one line each: an ID of CHARACTER (CH-IONA)> | want: <text> | hidden: <text> | holds_back: <text>
- driver: <standard: an ID of CHARACTER (CH-IONA)>
- conflict: <standard: one word from the note>
- third_thing: <standard: text>
- staging: <standard: text>
- start: <standard, when set_plan_exists, one line each: an ID of CHARACTER (CH-IONA)> | at: <MARK_NAME or [x, y]> | faces: <ID or [x, y]> | posture: <standing, seated, lying or kneeling>
- scene_idea: <standard: text; one sentence naming what the camera and the sound do>
- department_idea: <standard, one line each: camera, light, staging, sound or design> | idea: <text> | holds_baseline: <yes or no> | because: <IDs of any record ID, separated by commas>
- turn_picture: <quick, one line each: an ID of BEAT (SC10-B07)> | picture: <text>
- dial: <standard, one line each: an ID of BEAT (SC10-B07)> | size: <one word from the note> | distance_m: <metres> | height: <eye:CH-ID, seated:CH-ID, kneeling:CH-ID, floor or metres> | light: <text; default as_look> | sound: <text; default room_sound>
- coverage: <standard: designed, chained, master_and_coverage or oner>
- rhythm_shape: <standard: build_and_cut_out, build_rupture_aftermath, slow_burn or steady>
- target_asl_s: <standard: seconds>
- rupture: <standard: an ID of BEAT (SC10-B07)> | device: <one word from the note> | breaks: <text>
- tone_shift: <standard: an ID of BEAT (SC10-B07)> | from: <one word from the note> | to: <one word from the note> | device: <size_ladder, light_cue, music_in, music_out or camera_behaviour>
- room_sound: <standard: text, or as_place>
- geography: <standard, when action_scene: text>
- cause_chain: <standard, when action_scene: text>
- escalation: <standard, when action_scene: text>
- reversal: <standard, when action_scene: IDs of BEAT (SC10-B07), separated by commas>
- action_score: <standard, when action_scene: text; the block itself may sit in the plain part and be referred to here>
- time_treatment: <standard, when action_scene: real_time_continuous, held_real_time, overlapping_slices, elliptical or slow_motion>
- departure: <standard, one line each: an ID of CAMSYS or CAMRULE (CR-ELI) or RESERVE (RC-01) or LENS (LX-01) or LOOK (LK-SAYE-KITCHEN-NIGHT) or VISUAL (VS-SQ03) or SOUNDPLAN or LADDER or RULE (WR-MIRROR)> | what: <text> | why: <text>
- additions: <standard, one line each: text> | changes_meaning: <yes or no>
- lines_not_shown: <optional, one line each: line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)> | why: <text>
- flags: <standard: any of nonevent, splintered, turn_too_soon, turn_too_late, continuity, separated by commas, or none>
- note: <optional, one line each: text>

> SCENE: One scene: its list and plan fields live in 04 Scene list.md, its design fields in its scene file; the copies merge by ID (G10). (scene; ID SC and 2 digits (3 when the project has more than 99 scenes; fixed per project), plus an optional capital letter for an inserted scene, like SC10; lives in 04 Scene list.md, 11 Scenes/Scene NN - <place>.md.)
> Allowed values:
> - conflict: balanced, asymmetric, indirect, comic, minimal, reflexive
> - dial size: extreme_wide, wide, medium_wide, medium, medium_close_up, close_up, extreme_close_up, insert
> - rupture device: hold, drop_out, true_silence, cut_to_black, camera_change, pov_change
> - tone_shift from: grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative
> - tone_shift to: grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative
> - flags: nonevent, splintered, turn_too_soon, turn_too_late, continuity
> Conditions:
> - action_scene: The scene is tagged action.
> - set_plan_exists: The scene's location has a set plan (LOCATION size, object and mark items).
> status: draft, approved, stale, omitted.

### PART <scene ID, -P and one digit, like SC10-P2> <a short plain title>
- beats: <standard: an ID, or first..last, or IDs separated by commas>
- turn: <standard: an ID of BEAT (SC10-B07), or none>
- starts: <standard: scene_start, after_drop or without_drop>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> PART: A part of a scene with its own turn. (part; ID scene ID, -P and one digit, like SC10-P2; lives in 11 Scenes/Scene NN - <place>.md.)
> status: draft, approved, stale, omitted.

### BEAT <scene ID, -B and 2 digits, like SC10-B07> <a short plain title>
- lines: <quick: line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)>
- action: <standard: an ID of CHARACTER (CH-IONA)> | tactic: <one word ending in -ing>
- reaction: <standard: an ID of CHARACTER (CH-IONA)> | tactic: <one word ending in -ing>
- task: <standard, one line each: an ID of CHARACTER (CH-IONA)> | does: <text; visible behaviour only, never emotion words>
- beat_intensity: <standard: a number from 1 to 5>
- turn: <quick: none, turn or main_turn>
- turn_kind: <quick, when turn_beat: action or revelation>
- charge: <standard, one line each: an ID of VALUE (SC10-V1)> | charge: <---, --, -, 0, +, ++ or +++>
- flag: <standard, when when_used, one line each: one word from the note> | line: <an ID of SPEECH (SC10-D11)>
- engaged_pair: <standard, when tag_three_or_more: IDs of CHARACTER (CH-IONA), separated by commas>
- silent_third: <standard, when tag_three_or_more: an ID of CHARACTER (CH-IONA)>
- five_steps: <standard, when turn_or_intense_beat, one line each: desire, obstacle, choice, action or expression> | shows: <text>
- landing_face: <standard, when dialogue_pass_beat, always at detailed: a character ID, insert:<ID>, or wide>
- unsaid: <standard, when turn_beat, always at detailed: an ID of CHARACTER (CH-IONA)> | thought: <text>
- carrier: <standard, when turn_beat, always at detailed: an ID or text>
- pause_after: <standard: none, short, medium, long or hold> | seconds: <seconds> | picture: <hold, push_in, cut or cut_wide> | sound: <text>
- emphasis: <standard, one line each: an ID of MOTIF (MO-MINT) or PROP (PR-FLASK) or TEXT (TX-GOODS-ONLY) or STATE (CH-IONA.S02)> | level: <a number from 0 to 3>
- added_emphasis: <standard: 0 or 1> | what: <text>
- change: <standard, when turn_beat: text>
- distance: <detailed, one line each: IDs of CHARACTER (CH-IONA), separated by commas> | metres: <metres> | zone: <intimate, personal, social or public>
- core_word: <detailed: text>
- cut_rule: <detailed: cut_on_core_word, cut_early_split, hold or no_cut_two_shot>
- fact: <detailed: IDs of FACT (FT-03), separated by commas, or none>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> BEAT: One action and reaction (McKee's beat). (beat; ID scene ID, -B and 2 digits, like SC10-B07; lives in 11 Scenes/Scene NN - <place>.md.)
> Allowed values:
> - flag (first part): on_the_nose, melodrama, forced_exposition, monologue, repetitious, can_play_silent, interrupted
> Conditions:
> - dialogue_pass_beat: At standard: a turn beat, a beat with a flagged line, a beat where a fact is revealed, a refusal, or a line the plan names. At detailed: every beat.
> - tag_three_or_more: The scene is tagged three_or_more.
> - turn_beat: The beat's turn is not none.
> - turn_or_intense_beat: The beat's turn is not none, or its beat_intensity is 4 or more.
> - when_used: Written only when the thing it records exists (a departure, a flaw, a pov break); the checker never asks for it.
> Code adds these on every build; never type them: script_marked.
> status: draft, approved, stale, omitted.

### SPEECH <scene ID, -D and 2 digits (3 if a scene has more than 99), numbered in cue order within the scene, like SC10-D11> <a short plain title>
- speaker: <quick, code copies it from the story when source_is_screenplay; you write it when source_not_screenplay: an ID of CHARACTER (CH-IONA)>
- line: <quick, code copies it from the story when source_is_screenplay; you write it when source_not_screenplay: line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)>
- text: <quick, code copies it from the story when source_is_screenplay; you write it when source_not_screenplay: text>
- parenthetical: <quick, code copies it from the story when source_is_screenplay; you write it when source_not_screenplay: text, or none>
- extension: <quick, code copies it from the story when source_is_screenplay; you write it when source_not_screenplay: text, or none>
- path: <quick, code copies it from the story when source_is_screenplay; you write it when source_not_screenplay: one word from the note>
- origin: <quick, code copies it from the story when source_is_screenplay; you write it when source_not_screenplay: story, adapted or invented>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> SPEECH: One spoken line. Screenplay speeches are read by code into speeches.json; prose speeches are written by the AI in the scene file. (speech; ID scene ID, -D and 2 digits (3 if a scene has more than 99), numbered in cue order within the scene, like SC10-D11; lives in 11 Scenes/Scene NN - <place>.md, For machines - do not edit/speeches.json.)
> Allowed values:
> - path: direct, off_screen, earpiece, radio, intercom, phone, device_speaker, recording, helmet_inside, helmet_outside, through_glass, voice_over, thought
> Conditions:
> - source_is_screenplay: PROJECT.source_kind is screenplay.
> - source_not_screenplay: PROJECT.source_kind is not screenplay (prose, stage play, treatment, comic or game script, mixed): scenes come from the step outline.
> Code adds these on every build; never type them: word_count.
> status: draft, approved, stale, omitted.

### MOVE <scene ID, -M and 2 digits, like SC10-M04> <a short plain title>
- beat: <standard: an ID of BEAT (SC10-B07)>
- who: <standard: an ID of CHARACTER (CH-IONA)>
- from: <standard: MARK_NAME or [x, y]>
- to: <standard: MARK_NAME or [x, y]>
- via: <standard: [x, y] or [x, y, z] in metres, or none>
- start_s: <standard: seconds>
- dur_s: <standard: seconds>
- faces: <standard: ID or [x, y]>
- posture: <standard: standing, seated, lying or kneeling>
- why: <standard: text>
- origin: <standard: story, inferred or invented>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> MOVE: A character's move on the set plan (never a camera move). (floor-plan move; ID scene ID, -M and 2 digits, like SC10-M04; lives in 11 Scenes/Scene NN - <place>.md.)
> Written only when set_plan_exists: The scene's location has a set plan (LOCATION size, object and mark items).
> status: draft, approved, stale, omitted.

### SETUP <scene ID, -SU and 2 digits, like SC10-SU02> <a short plain title>
- at: <standard, or write at_words instead: [x, y] or [x, y, z] in metres>
- at_words: <standard, or write at instead: text>
- look_at: <standard: [x, y] or [x, y, z] in metres>
- lens_mm: <standard: millimetres>
- use: <standard: text>
- side: <standard: a or b>
- mount: <standard: world or an ID>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> SETUP: A camera position in a scene (shown to the user as camera A, B, C ... in order). (setup; ID scene ID, -SU and 2 digits, like SC10-SU02; lives in 11 Scenes/Scene NN - <place>.md.)
> status: draft, approved, stale, omitted.

### SHOTLIST <scene ID and -LIST, like SC10-LIST> <a short plain title>
- item: <quick, one line each: an ID of SHOT (SC10-SH150)> | beats: <IDs of BEAT (SC10-B07), separated by commas> | role: <turn, must_keep or normal> | size: <one word from the note> | frame: <one word from the note> | subject: <IDs of CHARACTER (CH-IONA) or STATE (CH-IONA.S02) or PROP (PR-FLASK) or TEXT (TX-GOODS-ONLY) or LOCATION (LOC-SAYE-KITCHEN), separated by commas> | time: <seconds> | shows: <text>
- approved: <quick, code writes it; in a chat without code you write it: yes or no>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> SHOTLIST: The one-line shot list that fixes the shot IDs and count before detail is written. (shot list; ID scene ID and -LIST, like SC10-LIST; lives in 11 Scenes/Scene NN - <place>.md.)
> Allowed values:
> - item size: extreme_wide, wide, medium_wide, medium, medium_close_up, close_up, extreme_close_up, insert
> - item frame: single, two_shot, three_shot, group, over_shoulder, pov, near_pov, empty
> status: draft, approved, stale, omitted.

### SHOT <scene ID, -SH and 3 digits in steps of 10; an insert takes a number between (SH155); 990-999 for end cards and black, like SC10-SH150> <a short plain title>
- beats: <quick: IDs of BEAT (SC10-B07), separated by commas>
- lines: <quick: line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)>
- purpose: <quick: text; one sentence: what the audience must get>
- because: <quick: IDs, line:NNN or line: "<quote anchor>", or default>
- role: <quick: turn, must_keep or normal>
- kind: <quick: one word from the note>
- why: <standard, when when_used: text; one sentence that quotes the story, names an object or action, or cites an ID>
- origin: <quick: story, inferred or invented>
- additions: <standard: IDs separated by commas, or text, or none>
- pov_break: <standard, when when_used: text>
- setup: <standard, when filmed_shot: an ID of SETUP (SC10-SU02)>
- frame: <quick: one word from the note>
- frame_detail: <standard, when reserved_choice, always at detailed: clean, dirty, symmetrical_profile or none>
- size: <quick: one word from the note>
- angle: <quick: one word from the note; default eye_level>
- height: <standard, when filmed_shot: eye:CH-ID, seated:CH-ID, kneeling:CH-ID, floor, or metres; default the eye of the whose_scene character, or of the subject>
- lens_mm: <standard, when filmed_shot: millimetres; default CAMSYS.normal_lens_mm>
- focus: <standard, when filmed_shot: deep, moderate or shallow; default moderate>
- focus_on: <standard, when filmed_shot: an ID of CHARACTER (CH-IONA) or STATE (CH-IONA.S02) or PROP (PR-FLASK) or TEXT (TX-GOODS-ONLY) or MOTIF (MO-MINT) or LOCATION (LOC-SAYE-KITCHEN)>
- move: <quick: one word from the note; default static>
- move_reason: <standard, when filmed_shot: text, or none>
- mount: <detailed: world, carried, or an ID>
- stance: <detailed: objective, pov, near_pov or direct_address>
- dominant: <detailed, you write it when depth_detailed; code derives it when depth_below_detailed: text>
- placement: <detailed: thirds, centre or edge>
- layers: <detailed: text>
- frame_in_frame: <detailed: text, or none>
- device: <detailed: text, or none>
- glass: <standard, when glass_in_frame, one line each: text> | state: <clear, marked, reflecting, screen or broken_open> | camera: <through, along or angled>
- subject: <quick, one line each: an ID of STATE (CH-IONA.S02) or CHARACTER (CH-IONA)> | at: <unless set_plan_exists: left_edge, left_third, centre, right_third or right_edge> | faces: <unless set_plan_exists: a direction word, or the ID of what the subject faces, or an ID> | does: <text; visible behaviour only, never emotion words> | tactic: <standard: one word ending in -ing> | energy: <standard: still, held, rising, breaking or spent> | display: <standard: 1, 2 or 3> | still: <standard: words from the note, separated by commas> | eyeline: <standard: text> | dwell_s: <standard, when eyeline_set: seconds> | travel: <standard, when subject_moves: one word from the note> | must_not: <standard, when later_beat_saves_behaviour: text> | continues: <detailed: an ID of SHOT (SC10-SH150)>
- thing: <standard, one line each: an ID of PROP (PR-FLASK) or STATE (CH-IONA.S02) or MOTIF (MO-MINT) or TEXT (TX-GOODS-ONLY)> | emphasis: <a number from 0 to 3> | at: <text> | plant: <an ID of PLANT (PL-07)> | payoff: <an ID of PLANT (PL-07)>
- text: <standard: IDs of TEXT (TX-GOODS-ONLY), separated by commas, or none>
- keep_hidden: <standard, when fact_element_before_reveal, one line each: an ID of FACT (FT-03)> | how: <one word from the note>
- must_show: <standard: IDs of CHARACTER (CH-IONA) or STATE (CH-IONA.S02) or PROP (PR-FLASK) or TEXT (TX-GOODS-ONLY) or MOTIF (MO-MINT) or LOCATION (LOC-SAYE-KITCHEN) or CAMERA (CAM-SHAFT-TOP), separated by commas, or none>
- must_not_show: <standard: IDs of CHARACTER (CH-IONA) or STATE (CH-IONA.S02) or PROP (PR-FLASK) or TEXT (TX-GOODS-ONLY) or MOTIF (MO-MINT) or LOCATION (LOC-SAYE-KITCHEN) or CAMERA (CAM-SHAFT-TOP), separated by commas, or none>
- physics_note: <standard, when when_used: text>
- motion: <standard, when when_used, one line each: free_fall> | object: <an ID of PROP (PR-FLASK) or CHARACTER (CH-IONA) or STATE (CH-IONA.S02)> | from_z: <metres> | to_z: <metres> | start_frame: <a number>
- light: <standard: text, or as_look; default as_look>
- light_cue: <standard: text> | when: <seconds> | why: <text>
- dark: <detailed: text>
- eye_light: <detailed: yes or no>
- hear: <quick, one line each: an ID of SPEECH (SC10-D11)> | speaker: <on_screen, off_screen or hidden> | path: <one word from the note> | at: <seconds> | words: <"exact story words">
- effect: <standard, one line each: text> | at: <seconds> | sound_emphasis: <a number from 0 to 3>
- room_sound: <standard: text, or as_place; default as_place>
- silence: <standard: none, room_sound_only, drop_out or true_silence; default none>
- music: <standard: an ID of MUSIC (MU-01), or none; default none>
- needs_description: <standard: yes or no>
- screen_time: <quick: seconds>
- moment: <standard, one line each: t0-t1 in seconds from the shot's start> | shows: <text>
- compound: <optional: yes or no; default no>
- start: <detailed, earlier when match_cut_or_continuous_action: text, or from_end_of: <shot ID>>
- end: <standard: text>
- cut_in_on: <detailed: one word from the note>
- cut_out_on: <standard: one word from the note>
- time_slice: <standard, when overlapping_slices: an ID of PREVIS (PV-SC10-SH080-V01)> | frames: <text>
- held: <standard: yes or no; default no>
- previs_level: <standard: a number from 0 to 5>
- storyboard: <standard: yes or no>
- framing_critical: <standard: yes or no>
- pose_critical: <detailed: yes or no>
- route: <standard: one word from the note; default auto>
- model: <optional: text> | why: <text>
- flip: <standard: auto or never>
- content_flags: <standard: words from the note, separated by commas>
- policy_route: <standard: one word from the note>
- cost_class: <standard: one word from the note>
- reuse_of: <standard: an ID of SHOT (SC10-SH150), or none>
- departure: <standard, when when_used, one line each: text> | from: <text> | to: <text> | because: <feasibility> | meaning_kept: <text>
- gen_note: <optional: text>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> SHOT: One shot, written from its list item at standard and detailed, reason-first (purpose and because before camera values). (shot; ID scene ID, -SH and 3 digits in steps of 10; an insert takes a number between (SH155); 990-999 for end cards and black, like SC10-SH150; lives in 11 Scenes/Scene NN - <place>.md, 11 Scenes/Scene NN - <place> - shots NNN-NNN.md.)
> Allowed values:
> - kind: live, insert, pov, screen, card, black
> - frame: single, two_shot, three_shot, group, over_shoulder, pov, near_pov, empty
> - size: extreme_wide, wide, medium_wide, medium, medium_close_up, close_up, extreme_close_up, insert
> - angle: eye_level, low, high, top_down, worms_eye, dutch
> - angle, only under a saved choice (RESERVE): dutch
> - move: static, pan, tilt, push_in, pull_back, sideways, rise, lower, follow, lead, handheld, crane, orbit, zoom, whip_pan, dolly_zoom, drone
> - move, only under a saved choice (RESERVE): orbit, zoom, whip_pan, dolly_zoom, drone
> - subject faces: frame_left, frame_right, camera, away, up, down
> - subject still: head, eyes, mouth, hands, torso, whole_body
> - subject travel: frame_left, frame_right, up, down, toward_camera, away, none
> - keep_hidden how: frame_edge, focus, dark, obstruction, timing, sound_first
> - hear path: direct, off_screen, earpiece, radio, intercom, phone, device_speaker, recording, helmet_inside, helmet_outside, through_glass, voice_over, thought
> - cut_in_on: action, look, line, sound, rhythm, reveal
> - cut_out_on: thought_complete, action_midpoint, line_end, sound_hit, rhythm, withholding
> - route: auto, text, start_picture, start_end_pictures, references, guide_video, performance_transfer, still_with_move, composite_only
> - content_flags: violence_implied, violence_onscreen, weapon_visible, gunfire, blood_small, gore, nudity, minor_present, self_harm, drug_use, real_person, real_brand, fire, none
> - policy_route: as_written, restated, split_cause_reaction_aftermath, composite_element, sound_only, cut
> - cost_class: graphic, reuse, still_move, easy, dialogue, hard
> Conditions:
> - depth_below_detailed: The project's (or the scene's) depth is quick or standard.
> - depth_detailed: The project's (or the scene's) depth is detailed.
> - eyeline_set: The subject item has an eyeline.
> - fact_element_before_reveal: A FACT's element is in the scene before its reveal (audience_knows_from).
> - filmed_shot: The SHOT kind is not card or black: a camera films it (a title card or black has no setup, height, lens or focus).
> - glass_in_frame: A glass surface is in frame.
> - later_beat_saves_behaviour: A later beat saves a visible behaviour (for example SC13's "Now he looks at her.").
> - overlapping_slices: The scene's time_treatment is overlapping_slices.
> - reserved_choice: The value is used under a saved choice (RESERVE).
> - set_plan_exists: The scene's location has a set plan (LOCATION size, object and mark items).
> - subject_moves: The subject moves in the frame.
> - when_used: Written only when the thing it records exists (a departure, a flaw, a pov break); the checker never asks for it.
> Code adds these on every build; never type them: label, min_screen_time_s, clips, era, mirror_state, mirror_route, post_ops, image_sides, main_light_side, eyeline_sides, projected_placement, size_check, face_height, lip_sync, needs, scene_model, suggested_model, generation_spec.
> status: draft, approved, stale, omitted.

### CUT <scene ID, -C and the number of the shot it follows, like SC10-C200> <a short plain title>
- to: <standard: an ID of SHOT (SC10-SH150)>
- type: <standard: one word from the note>
- split_s: <standard, when cut_is_split: seconds>
- black_frames: <standard, when cut_has_black: a number>
- sound_across: <standard, when cut_is_split: text>
- shared_geometry: <standard, when cut_is_match: an ID of PREVIS (PV-SC10-SH080-V01)>
- why: <standard: text; one sentence that quotes the story, names an object or action, or cites an ID>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> CUT: A join between shots, only where it is not a plain cut. (cut; ID scene ID, -C and the number of the shot it follows, like SC10-C200; lives in 11 Scenes/Scene NN - <place>.md, 11 Scenes/Scene NN - <place> - shots NNN-NNN.md.)
> Allowed values:
> - type: j_cut, l_cut, match_cut, jump_cut, smash_cut, dissolve, fade, cut_to_black, freeze, continue
> Conditions:
> - cut_has_black: The CUT type is cut_to_black, fade or freeze.
> - cut_is_match: The CUT type is match_cut.
> - cut_is_split: The CUT type is j_cut or l_cut.
> status: draft, approved, stale, omitted.

END OF FILE | Scene NN - <place> | 9 records
