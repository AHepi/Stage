# Scene list

## At a glance

<How many scenes, how long the film runs, and where it turns, in two or three sentences.>

## The scenes, one line each

<scene 10, Saye's kitchen, about 2 minutes: what happens, in one plain line.>

## Scenes to cut or merge

<Only when the film is shorter than the story: which scenes go, and why.>

Below this line: details for the AI and the checker. You never need to read them.

> The scene's list fields (step 1) and plan fields (step 2) live here; its design fields live in its scene file (templates/11 Scene.md). The copies merge by ID.

### SCENE <SCnn> <the place, in plain words>
- heading: <quick, code copies it from the story when source_is_screenplay; you write it when source_not_screenplay; in a chat without code you write it: text>
- int_ext: <quick, code copies it from the story when source_is_screenplay; you write it when source_not_screenplay; in a chat without code you write it: int, ext or int_ext>
- place_text: <quick, code copies it from the story when source_is_screenplay; you write it when source_not_screenplay; in a chat without code you write it: text>
- time_text: <quick, code copies it from the story when source_is_screenplay; you write it when source_not_screenplay; in a chat without code you write it: text>
- lines: <quick, code copies it from the story when source_is_screenplay; code writes it when source_not_screenplay; in a chat without code you write it: line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)>
- characters: <quick, code writes it; in a chat without code you write it: IDs of CHARACTER (CH-IONA), separated by commas>
- speaking: <quick, code writes it; in a chat without code you write it, one line each: an ID of CHARACTER (CH-IONA)> | cues: <a number>
- transition_in: <quick, code copies it from the story; in a chat without code you write it: one word from the note>
- transition_out: <quick, code copies it from the story; in a chat without code you write it: one word from the note>
- presentation: <quick: one word from the note>
- host: <quick, when presentation_on_device: an ID of PROP (PR-FLASK) or CAMERA (CAM-SHAFT-TOP), or none>
- event: <quick: text>
- sequence: <quick: an ID of SEQUENCE (SQ03)>
- scene_intensity: <quick: a number from 1 to 10>
- whose_scene: <standard: an ID of CHARACTER (CH-IONA)>
- story_day: <standard: text>
- rhythm_class: <standard: action_peak, suspense, mixed, dialogue or contemplative>
- tone: <standard: one word from the note>
- tone_undercurrent: <standard: one word from the note>
- tags: <quick: words from the note, separated by commas, or none>
- depth: <optional, the user's answer, set through a choice: quick, standard, detailed or none>
- target_duration_s: <standard, code writes it; in a chat without code you write it: seconds>
- keep: <standard, when compressing: keep, trim, merge, fold or cut>
- merged_into: <standard, when compressing: an ID of SCENE (SC10), or none>
- from_lines: <quick, when source_not_screenplay: line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)>
- five_test: <quick, when source_not_screenplay: text>
- cardinal: <quick, when source_not_screenplay: IDs of CARDINAL (CF-05), separated by commas, or none>
- strands: <quick, when source_not_screenplay: IDs of STRAND (ST-01), separated by commas, or none>
- origin: <quick: story, inferred or invented>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> SCENE: One scene: its list and plan fields live in 04 Scene list.md, its design fields in its scene file; the copies merge by ID (G10). (scene; ID SC and 2 digits (3 when the project has more than 99 scenes; fixed per project), plus an optional capital letter for an inserted scene, like SC10; lives in 04 Scene list.md, 11 Scenes/Scene NN - <place>.md.)
> Allowed values:
> - transition_in: cut, cut_to_black, fade_in, fade_out, dissolve, smash_cut, match_cut, continuous
> - transition_out: cut, cut_to_black, fade_in, fade_out, dissolve, smash_cut, match_cut, continuous
> - presentation: normal, on_screen, recording, flashback, dream, montage, letter
> - tone: grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative
> - tone_undercurrent: grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative, none
> - tags: dialogue_duel, three_or_more, action, glass_and_reflection, handedness, screens_and_text, in_story_footage, suspense_and_reveal, darkness, prose_interior, montage_and_time, creature, violence
> Conditions:
> - compressing: The user set a runtime target shorter than the story as written, or the source is prose (step 2 compression plan).
> - presentation_on_device: SCENE.presentation is on_screen or recording.
> - source_is_screenplay: PROJECT.source_kind is screenplay.
> - source_not_screenplay: PROJECT.source_kind is not screenplay (prose, stage play, treatment, comic or game script, mixed): scenes come from the step outline.
> status: draft, approved, stale, omitted.

END OF FILE | Scene list | 1 records
