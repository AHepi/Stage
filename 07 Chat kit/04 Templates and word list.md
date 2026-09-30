# 04 Templates and word list

Part of the Stage chat kit (knowledge). It holds every empty record file of the skill (00 Start here, 01 Choices, 04 Scene list, 05 Story plan, 06 World and style, 07 Characters and voices, 08 Places and things, 09 Continuity, 10 Film rules, 11 Scene, 13 Health check, 18 Add-on jobs, 22 Rights and credits), each between two ~~~~ lines to copy as it is, then the record format, the word list and the rule order. Fill a template's angle brackets; the note block after each record lists the allowed values, and you need not copy it. 01 House rules says where every other skill file is in this kit.

---

From the skill file `templates/00 Start here.md`:

~~~~markdown
# <The story's title>

## Where things stand

<Step N of 12, its name; when the checker last ran; what is waiting for the user.>

## Next step

<One next step, in one sentence, with an example of what the user can type.>

## Big choices so far

<One numbered line for each big choice: what was chosen, and whether it was the user's answer or the default.>

## Files in this folder

<One line for each numbered file: its name and what it holds, in plain words.>

## Word list

<The few words this project uses, one line each, with a plain meaning.>

## Log

<One dated line for each change: what was made, tried, failed or changed.>

Below this line: details for the AI and the checker. You never need to read them.

### PROJECT <3 to 8 capital letters, like CATCH> <a short plain title>
- title: <quick, code copies it from the story; in a chat without code you write it: text>
- source_file: <quick, code writes it; in a chat without code you write it: text>
- source_fingerprint: <quick, code writes it; in a chat without code you write it: text>
- source_kind: <quick, code writes it; in a chat without code you write it: one word from the note>
- source_format: <quick, code writes it; in a chat without code you write it: one word from the note>
- language: <quick, code writes it; in a chat without code you write it: word>
- depth: <quick, the user's answer, set through a choice: quick, standard or detailed>
- surface: <quick, code writes it; in a chat without code you write it: one word from the note>
- code_execution: <quick, code writes it; in a chat without code you write it: yes or no>
- batch_size: <quick, code writes it; in a chat without code you write it: 12 or 18>
- training_off: <quick, the user's answer, set through a choice: confirmed or not_confirmed>
- rights: <quick, the user's answer, set through a choice: mine, permission, public_domain, study_only or unknown>
- intended_use: <add-on, AI video, the user's answer, set through a choice: personal, festival, online_free, online_monetised or commercial>
- licensed_data_only: <add-on, AI video, the user's answer, set through a choice: yes or no; default no>
- format: <quick, the user's answer, set through a choice: short, feature or limited_series>
- runtime_target_s: <quick, the user's answer, set through a choice: seconds, or as_written>
- scope: <quick, the user's answer, set through a choice: IDs of SCENE (SC10), separated by commas, or all>
- frame_shape: <quick, the user's answer, set through a choice: 2.39, 1.85, 16_9, 4_3 or 9_16>
- fps: <quick: 24, 25 or 30>
- genre: <quick, code writes it; in a chat without code you write it: word>
- tone_home: <quick, code writes it; in a chat without code you write it: one word from the note>
- tone_range: <quick, code writes it; in a chat without code you write it: words from the note, separated by commas>
- scene_id_digits: <quick, code writes it; in a chat without code you write it: 2 or 3>
- prompt_words: <standard, one line each: text> | use: <text>
- previs_colours: <add-on, grey previews, code writes it, one line each: an ID of CHARACTER (CH-IONA)> | rgb: <[r, g, b] (Red, green and blue from 0 to 1, as [r, g, b])>
- spend_cap_usd: <add-on, AI video, the user's answer, set through a choice: US dollars, or none>
- hours_per_week: <add-on, AI video, the user's answer, set through a choice: a number, or none>
- schema_version: <quick, code writes it; in a chat without code you write it: text>
- checker_last_run: <quick, code writes it; in a chat without code you write it: a date (year-month-day) or never>
- model_facts_date: <quick, code writes it; in a chat without code you write it: year-month-day, or none>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> PROJECT: One per project: the story, the app, the depth, the rights and the big settings. (the project; ID 3 to 8 capital letters, like CATCH; lives in 00 Start here.md.)
> Allowed values:
> - source_kind: screenplay, prose, stage_play, treatment, comic_script, game_script, mixed
> - source_format: catch_dialect, fountain, fdx, docx, epub, pdf_text, markdown, plain_text
> - surface: claude_code, claude_cowork, claude_web, chatgpt, gemini, other
> - tone_home: grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative
> - tone_range: grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative
> status: draft, approved, stale, omitted.

END OF FILE | Start here | 1 records
~~~~

---

From the skill file `templates/01 Choices.md`:

~~~~markdown
# Choices

## Waiting for you

<One numbered question for each open choice, with what happens if the user says nothing.>

## Small choices I made

<One line for each choice taken by default, and how to change it.>

## Answered

<One line for each answered choice and the answer.>

Below this line: details for the AI and the checker. You never need to read them.

### CHOICE <CHOICE- and 3 digits, like CHOICE-021> <a short plain title>
- question: <quick: text>
- why: <quick: text>
- option: <quick, one line each: one word> | text: <text>
- default: <quick: one word> | reason: <text>
- answer: <quick, when choice_answered, the user's answer, set through a choice: an option letter, or text>
- asked: <quick: yes or no>
- checkpoint: <quick: one word from the note>
- affects: <quick: IDs, or <ID>.<field> paths, separated by commas>
- sets: <quick, one line each: <ID>.<field> or CHOICE-NNN-X> | value: <text> | when: <one word>
- locks: <optional: IDs of any record ID, separated by commas>
- based_on: <standard: text>
- status: <quick, code writes it; in a chat without code you write it: open, answered or defaulted>
- date: <quick, code writes it; in a chat without code you write it: year-month-day, or none>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> CHOICE: A question for the user with a default; a small choice (asked: no) is grouped under 'small choices I made'. (choice; ID CHOICE- and 3 digits, like CHOICE-021; lives in 01 Choices.md.)
> Allowed values:
> - checkpoint: a, p, b, c, acceptance, d, e, none
> Conditions:
> - choice_answered: CHOICE.status is answered.
> status: open, answered, defaulted.

### SETVALUE <the choice ID, a hyphen and the option letter in capitals, like CHOICE-014-A> <a short plain title>
- target: <quick: a record ID, or the type name of a singleton record or the project (PLAN, STYLE, PROJECT)>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> SETVALUE: The full value one option of a CHOICE writes, for answers a sets line cannot hold; code copies its field lines into the target and locks them when that option is chosen. (set value; ID the choice ID, a hyphen and the option letter in capitals, like CHOICE-014-A; lives in 01 Choices.md.)
> status: draft, approved, stale, omitted.
> After target, write the field lines this option sets, exactly as they would appear in the target record.

END OF FILE | Choices | 2 records
~~~~

---

From the skill file `templates/04 Scene list.md`:

~~~~markdown
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
~~~~

---

From the skill file `templates/05 Story plan.md`:

~~~~markdown
# Story plan

## At a glance

<The story in one sentence, the question it asks, and how it ends.>

## How the story is built

<The acts, the crisis and the climax, with the scenes where they happen.>

## Groups of scenes

<One line for each group of scenes: what it is for and how it ends.>

## Plants and payoffs

<One line for each thing shown early that pays off later.>

## What the audience knows

<One line for each secret: who knows it and when the audience learns it.>

## How the book becomes a film

<Only for prose or a shorter film: what is kept, merged and cut.>

Below this line: details for the AI and the checker. You never need to read them.

### PLAN
- logline: <quick: text>
- theme_question: <quick: text>
- core_value: <quick: text> | positive: <text> | negative: <text>
- core_opposition: <standard: text>
- crisis: <quick: SCnn "<exact story words, 3 or more, found once in that scene>">
- climax: <quick: an ID, or first..last, or IDs separated by commas>
- act: <standard, one line each: text> | scenes: <an ID, or first..last, or IDs separated by commas> | turn: <SCnn "<exact story words, 3 or more, found once in that scene>">
- peak: <standard, one line each: one word from the note> | scene: <an ID of SCENE (SC10)> | reason: <text>
- pov_plan: default: <standard: an ID of CHARACTER (CH-IONA)> | breaks: <text>
- genre: <quick: word>
- tone_home: <quick: one word from the note>
- tone_range: <standard: words from the note, separated by commas>
- tone_mix_rule: <standard: text>
- plan_option: <quick, when source_not_screenplay, one line each: one word> | format: <short, feature or limited_series> | runtime_s: <seconds> | scenes: <a number> | shots: <a number> | keeps: <text> | cuts: <text> | loses: <text>
- loses: <standard, when compressing: text>
- op: <standard, when compressing, one line each: one word from the note> | what: <text> | from: <text> | to: <text> | why: <text>
- runtime_estimate: <quick, code writes it; in a chat without code you write it: seconds>
- scene_budget: <quick, code writes it; in a chat without code you write it: a number>
- shot_budget: <quick, code writes it; in a chat without code you write it: a number>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> PLAN: The film-level plan every later choice keys to. (story plan; one per project; lives in 05 Story plan.md.)
> Allowed values:
> - peak (first part): story, crisis_choice, colour, contrast, tightest_size, longest_hold, loudest_sound, motif_payoff, camera_break, sound_rupture
> - tone_home: grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative
> - tone_range: grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative
> - op (first part): trim, merge_scenes, fold_into, composite_character, move_line, move_plant, delete_strand, reorder, invention, replace, flashback_import, lost_resonance
> Conditions:
> - compressing: The user set a runtime target shorter than the story as written, or the source is prose (step 2 compression plan).
> - source_not_screenplay: PROJECT.source_kind is not screenplay (prose, stage play, treatment, comic or game script, mixed): scenes come from the step outline.
> status: draft, approved, stale, omitted.

### SEQUENCE <SQ and 2 digits, like SQ03> <a short plain title>
- title: <quick: text>
- scenes: <quick: an ID, or first..last, or IDs separated by commas>
- story_job: <standard: text>
- value_change: <quick: text>
- act: <standard: text>
- scene_intensity: <standard: text>
- travel: <standard: left_to_right, right_to_left, up, down or none>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> SEQUENCE: One group of scenes; colour and visual plans are written at step 6 against these IDs. (sequence (group of scenes); ID SQ and 2 digits, like SQ03; lives in 05 Story plan.md.)
> status: draft, approved, stale, omitted.

### PLANT <PL- and 2 digits, like PL-07> <a short plain title>
- what: <standard: text>
- planted_at: <standard: SCnn "<exact story words, 3 or more, found once in that scene>">
- paid_off_at: <standard: SCnn "<exact story words, 3 or more, found once in that scene>">
- plant_emphasis: <standard: a number from 0 to 3>
- plot_event: <optional: yes or no; default no>
- payoff_emphasis: <standard: a number from 0 to 3>
- rhyme: <standard: yes or no> | framing: <text> | side: <same or reversed>
- motif: <standard: an ID of MOTIF (MO-MINT), or none>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> PLANT: A plant and its payoff; the shots that plant and pay off name it on their thing items (plant:, payoff:). (plant; ID PL- and 2 digits, like PL-07; lives in 05 Story plan.md.)
> status: draft, approved, stale, omitted.

### FACT <FT- and 2 digits, like FT-03> <a short plain title>
- what: <standard: text>
- element: <standard: IDs of CHARACTER (CH-IONA) or STATE (CH-IONA.S02) or PROP (PR-FLASK) or TEXT (TX-GOODS-ONLY) or MOTIF (MO-MINT) or LOCATION (LOC-SAYE-KITCHEN) or CAMERA (CAM-SHAFT-TOP), separated by commas>
- audience_knows_from: <standard: SCnn "<exact story words, 3 or more, found once in that scene>">
- known_by: <standard, one line each: an ID of CHARACTER (CH-IONA)> | from: <SCnn "<exact story words, 3 or more, found once in that scene>">
- mode: <standard: suspense, mystery, surprise or dramatic_irony>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> FACT: Who knows what, from when; element names what would give the fact away in frame. (fact; ID FT- and 2 digits, like FT-03; lives in 05 Story plan.md.)
> Written only when fact_mode_needs_record: FACT.mode is suspense, mystery or dramatic_irony (about 5-15 in a film); every fact at detailed.
> status: draft, approved, stale, omitted.

### CHAPTER <CP and 2 digits, like CP01> <a short plain title>
- title: <quick, code copies it from the story; in a chat without code you write it: text>
- lines: <quick, code copies it from the story; in a chat without code you write it: line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)>
- words: <quick, code copies it from the story; in a chat without code you write it: a number>
- first_line: <quick: "exact story words">
- last_line: <quick: "exact story words">
- digest: <quick: text>
- people: <quick: IDs of CHARACTER (CH-IONA), separated by commas>
- places: <quick: text>
- time_markers: <quick: text>
- pov: <quick: an ID of CHARACTER (CH-IONA)>
- candidate: <quick, one line each: text> | lines: <line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)> | kind: <one word from the note> | tests: <text> | decision: <own_scene, fold, montage, voice_over or cut> | becomes: <an ID of SCENE (SC10)>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> CHAPTER: A prose chapter: its stub from step 1, its digest from step 2. (chapter; ID CP and 2 digits, like CP01; lives in 05 Story plan.md.)
> Allowed values:
> - candidate kind: dramatized, narratized, inner, summary, iterative, letter, description
> status: draft, approved, stale, omitted.

### STRAND <ST- and 2 digits, like ST-01> <a short plain title>
- name: <quick: text>
- chapters: <quick: IDs of CHAPTER (CP01), separated by commas>
- carries: <quick: IDs of CARDINAL (CF-05), separated by commas>
- feeds: <quick: text>
- decision: <quick: keep, compress, composite, fold or cut>
- reason: <quick: text>
- seconds: <quick: seconds>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> STRAND: A line of events through a prose work. (strand; ID ST- and 2 digits, like ST-01; lives in 05 Story plan.md.)
> status: draft, approved, stale, omitted.

### CARDINAL <CF- and 2 digits, like CF-05> <a short plain title>
- event: <quick: text>
- lines: <quick: line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)>
- depends: <quick: IDs of CARDINAL (CF-05), separated by commas, or none>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> CARDINAL: An event the story cannot lose (the deletion test). (cardinal event; ID CF- and 2 digits, like CF-05; lives in 05 Story plan.md.)
> Written only when compressing: The user set a runtime target shorter than the story as written, or the source is prose (step 2 compression plan).
> status: draft, approved, stale, omitted.

END OF FILE | Story plan | 7 records
~~~~

---

From the skill file `templates/06 World and style.md`:

~~~~markdown
# World and style

## At a glance

<Where and when the story happens, and how the film looks, in two or three sentences.>

## Where and when

<The place, the period and the season, and what the story leaves open.>

## How the film looks

<The style in plain words: photographic or drawn, the frame shape, the colour.>

## Rules of the story's world

<One line for each rule the pictures must keep, such as a mirrored world or how titles appear.>

Below this line: details for the AI and the checker. You never need to read them.

### STYLE
- medium: <quick, the user's answer, set through a choice: one word from the note>
- style_words: <quick: text>
- texture: <standard, one line each: grain, halation, lens_character, softness or cadence> | as: <text>
- named_reference_policy: <quick, code writes it; in a chat without code you write it: describe_qualities_only>
- words_to_avoid: <quick: text>
- style_picture: <add-on, storyboards or AI video: a file name>
- provisional: <quick, code writes it; in a chat without code you write it: yes or no; default yes>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> STYLE: How the whole film is made to appear. (style; one per project; lives in 06 World and style.md.)
> Allowed values:
> - medium: live_action, 3d_animation, 2d_animation, stop_motion_look, painted, mixed
> status: draft, approved, stale, omitted.

### WORLD
- place: <quick, the user's answer, set through a choice: named:<country>, invented or unstated>
- period: <quick, the user's answer, set through a choice: text>
- drives_on: <quick: left, right or none>
- language: <quick: word>
- accents: <standard: text>
- signage: <standard: text>
- emergency_lights: <standard: text>
- institutions: <standard: text>
- money: <standard: text>
- evidence: <standard, one line each: line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)> | quote: <"exact story words">
- origin: <standard: story, inferred or invented>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> WORLD: Where and when the story happens, and its local signals. (world; one per project; lives in 06 World and style.md.)
> status: draft, approved, stale, omitted.

### RULE <WR- and capitals and hyphens, like WR-MIRROR> <a short plain title>
- kind: <quick: one word from the note>
- statement: <quick: text>
- governs: <quick: IDs of any record ID, separated by commas>
- era: <quick, when mirror_rule, the user's answer, set through a choice, one line each: one word> | from: <line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)> | to: <line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)> | frame: <original or reversed>
- exception: <standard, one line each: an ID of any record ID; write none when there is nothing> | reads: <normal or mirrored> | why: <text>
- occurrences: <quick, when device_rule: line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)>
- policy: <quick, when device_rule: open_only, open_and_close, every_return, episode_cold_open or template_refrain>
- template_setup: <quick, when device_rule: an ID of SHOT (SC10-SH150), or none>
- varies: <quick, when device_rule: text>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> RULE: A story-world rule and what it governs (mirror rules, text rules, titles, recurring devices). (story-world rule; ID WR- and capitals and hyphens, like WR-MIRROR; lives in 06 World and style.md.)
> Allowed values:
> - kind: world, mirror, text, titles, device, other
> Conditions:
> - device_rule: This RULE's kind is device (a recurring device in prose).
> - mirror_rule: This RULE's kind is mirror.
> status: draft, approved, stale, omitted.

END OF FILE | World and style | 3 records
~~~~

---

From the skill file `templates/07 Characters and voices.md`:

~~~~markdown
# Characters and voices

## At a glance

<How many people, and who carries the story.>

## The people, one line each

<Iona: a lift engineer, lean and strong; what she wants, and how she changes.>

## Their voices

<One line for each speaking person: how the voice sounds.>

Below this line: details for the AI and the checker. You never need to read them.

### CHARACTER <CH- and capitals and hyphens, like CH-IONA> <a short plain title>
- names: <quick, code copies it from the story when character_has_cue; otherwise you write it; in a chat without code you write it: short phrases separated by commas>
- tier: <quick: principal, minor, extra or non_human>
- role: <quick: text>
- life_want: <standard: text>
- arc: start: <standard: text> | end: <text> | turning_scene: <an ID of SCENE (SC10)>
- thesis: <standard: text>
- evidence: <standard, one line each: line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)> | quote: <"exact story words">
- fixed_description: <quick: text; 25-40 words for a principal, 20-30 for others; appearance only: no expression and no image sides>
- height_m: <standard: metres>
- build: <standard: text>
- colour_identity: <standard: text>
- tempo: <standard: text>
- speech: sentences: <standard: text> | contractions: <yes or no> | vocabulary: <text>
- lineup: height: <standard, when principal: short, average or tall> | mass: <slight, average or heavy> | shape: <round, square, triangle or long> | value: <dark, mid or light> | colour: <word> | tempo: <slow, medium or fast>
- face: <standard, when principal, always at detailed: text>
- movement: <standard, when principal, always at detailed, one line each: home, stress or break> | part: <text> | direction: <text> | speed: <text> | still: <text>
- gesture: <standard, when principal, always at detailed: text> | line: <line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)>
- status_play: default: <standard, when principal, always at detailed: high, equal or low> | flips: <story points separated by commas>
- distance: default_m: <standard, when principal, always at detailed: metres> | closest_m: <metres> | changes: <IDs of SCENE (SC10), separated by commas>
- one_image: <detailed: text>
- expression: <detailed: text>
- skin_light: <add-on, AI video, when casting_chosen: text>
- voice: <standard: an ID of VOICE (VO-SAYE)>
- likeness_basis: <quick, the user's answer, set through a choice: invented, self_consented or performer_consented; default invented>
- consent: <add-on, AI video, the user's answer, set through a choice: an ID of RIGHTS (RT-001), or none>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> CHARACTER: A person or being the film shows more than once, with the design every prompt keeps. (character; ID CH- and capitals and hyphens, like CH-IONA; lives in 07 Characters and voices.md.)
> Conditions:
> - casting_chosen: Casting (the appearance of the people who play the characters) has been chosen in add-on C.
> - character_has_cue: The character speaks: code found a cue for it in the story.
> - otherwise: None of the other conditions in the same writer_when list holds.
> - principal: CHARACTER.tier is principal.
> status: draft, approved, stale, omitted.

### VOICE <VO- and capitals and hyphens, like VO-SAYE> <a short plain title>
- character: <standard: an ID of CHARACTER (CH-IONA)>
- voice_description: <standard: text; 30-50 words>
- pitch: <standard: low, low_mid, mid, mid_high or high>
- pace_wps: <standard: words per second; default 2.5>
- accent: <standard: text>
- path_sound: <standard, one line each: one word from the note; write none when there is nothing> | treatment: <text>
- source: <standard, the user's answer, set through a choice: one word from the note; default designed>
- consent: <add-on, AI video: an ID of RIGHTS (RT-001), or none>
- tool: <add-on, AI video: text>
- provider_voice: <add-on, AI video: text>
- texture: <add-on, AI video: text>
- habits: <add-on, AI video: text>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> VOICE: One character's voice: the fixed words for it, pitch, pace and how it is made (D3). (voice; ID VO- and capitals and hyphens, like VO-SAYE; lives in 07 Characters and voices.md.)
> Allowed values:
> - path_sound (first part): earpiece, radio, intercom, recording, helmet_inside, phone, through_glass
> - source: designed, user_recorded, actor_recorded, own_clone, consented_clone, native_draft
> status: draft, approved, stale, omitted.

END OF FILE | Characters and voices | 2 records
~~~~

---

From the skill file `templates/08 Places and things.md`:

~~~~markdown
# Places and things

## At a glance

<How many places and things, and which ones matter most.>

## Places

<One line for each place: what it looks like and which scenes use it.>

## Things

<One line for each thing the story needs: what it looks like and why it matters.>

## Words in the picture

<One line for each sign, screen or title: its exact words.>

## Things that come back

<One line for each thing that returns and gathers meaning.>

Below this line: details for the AI and the checker. You never need to read them.

### LOCATION <LOC- and capitals and hyphens, like LOC-SAYE-KITCHEN> <a short plain title>
- headings: <standard, code copies it from the story when source_is_screenplay; you write it when source_not_screenplay; in a chat without code you write it: text>
- story_job: <standard: text>
- loudness: <standard: loud or quiet>
- room_sound: <standard: text>
- anchor: <standard: text>
- exit: <standard, one line each: text> | leads_to: <text>
- dressing: <standard: text>
- plan_orientation: <standard, when set_plan_needed, always at detailed: original or reversed>
- size: <standard, when set_plan_needed, always at detailed: [width, depth, height] in metres>
- origin_corner: <standard, when set_plan_needed, always at detailed: text>
- axes: <standard, when set_plan_needed, always at detailed: text>
- wild_walls: <standard, when set_plan_needed, always at detailed: the compass names of the walls the camera may pass through (north, south, east or west, separated by commas), or none>
- object: <standard, when set_plan_needed, always at detailed, one line each: one word> | at: <[x, y] or [x, y, z] in metres> | size: <[width, depth, height] in metres> | base: <metres> | material: <text> | meaning: <text> | furniture: <seat, bed or none>
- mark: <standard, when set_plan_needed, always at detailed, one line each: one word> | at: <[x, y] or [x, y, z] in metres>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> LOCATION: A place, with a set plan in metres when step 4's rule needs one. (place; ID LOC- and capitals and hyphens, like LOC-SAYE-KITCHEN; lives in 08 Places and things.md.)
> Conditions:
> - set_plan_needed: Step 4's rule: the place is used by a shot likely to need previs level 2 or more, a reflection or glass shot, or three or more people in one space.
> - source_is_screenplay: PROJECT.source_kind is screenplay.
> - source_not_screenplay: PROJECT.source_kind is not screenplay (prose, stage play, treatment, comic or game script, mixed): scenes come from the step outline.
> Code adds these on every build; never type them: orientation.
> status: draft, approved, stale, omitted.

### PROP <PR- and capitals and hyphens, like PR-FLASK> <a short plain title>
- names: <quick: short phrases separated by commas>
- category: <quick: one word from the note>
- kind: <detailed: emblem, action, plot_machinery or dressing>
- fixed_description: <standard: text; what it is, what it looks like and its size; no state and no image sides>
- real_size: <standard: [width, depth, height] in metres>
- surface: <detailed: ordinary, matte_black, clear, shiny or very_bright>
- side: <standard, one line each: text; write none when there is nothing> | own: <left or right> | plot: <yes or no>
- text: <standard: IDs of TEXT (TX-GOODS-ONLY), separated by commas, or none>
- first_seen: <standard: line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)>
- motif: <standard: an ID of MOTIF (MO-MINT), or none>
- origin: <quick: story, inferred or invented>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> PROP: A thing the film shows more than once or at a turn. (thing; ID PR- and capitals and hyphens, like PR-FLASK; lives in 08 Places and things.md.)
> Allowed values:
> - category: hero_prop, prop, set_dressing, vehicle, animal, weapon, consumable, document, wardrobe, practical_effect, visual_effect
> status: draft, approved, stale, omitted.

### TEXT <TX- and capitals and hyphens, like TX-GOODS-ONLY> <a short plain title>
- kind: <quick: one word from the note>
- words: <quick, code copies it from the story lines of words_from when origin is story; you write it when origin is inferred or invented: text>
- on: <quick: an ID of PROP (PR-FLASK) or LOCATION (LOC-SAYE-KITCHEN) or CAMERA (CAM-SHAFT-TOP) or CHARACTER (CH-IONA), or none>
- origin: <quick: story, inferred or invented>
- words_from: <quick, when text_in_story, one line each: the story line that writes the words (a line number, or a quote anchor in a chat without code)> | quote: <the exact words inside the line, when the line holds more than the text>
- reader: <standard: an ID of CHARACTER (CH-IONA), or none>
- plot_critical: <standard: yes or no>
- emphasis: <standard: a number from 0 to 3>
- method: <standard: composite, background_blur or model_drawn>
- lettering: <detailed: text>
- animation: <standard: text, or none>
- translate: <detailed: yes or no>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> TEXT: Readable words inside the picture; never generated, always composited from a text graphic (K17). (text in picture; ID TX- and capitals and hyphens, like TX-GOODS-ONLY; lives in 08 Places and things.md.)
> Allowed values:
> - kind: sign, label, stencil, screen, visor, wrist, monitor, document, title_card, caption, timestamp
> Conditions:
> - otherwise: None of the other conditions in the same writer_when list holds.
> - text_in_story: The TEXT words are written in the story.
> status: draft, approved, stale, omitted.

### MOTIF <MO- and capitals and hyphens, like MO-MINT> <a short plain title>
- meaning: <standard: text>
- rank: <standard: spine, supporting, single_scene, minor or plot_machinery>
- channel: <standard: visual, sound or body>
- appearance: <standard, one line each: SCNN, a story point, or a shot ID> | role: <one word from the note> | emphasis: <a number from 0 to 3> | sound_emphasis: <a number from 0 to 3> | rhyme_with: <an ID of any record ID> | side: <same or reversed>
- signature: <standard: text, or none>
- direction: <detailed: text>
- pole: <detailed: text>
- test_score: <detailed: a number from 0 to 6>
- rule: <detailed, one line each: text>
- largest_payoff: <detailed: yes or no>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> MOTIF: A thing that returns and gathers meaning. (motif; ID MO- and capitals and hyphens, like MO-MINT; lives in 08 Places and things.md.)
> Allowed values:
> - appearance role: plant, develop, teach, reveal, payoff, coda
> status: draft, approved, stale, omitted.

### CAMERA <CAM- and capitals and hyphens, like CAM-SHAFT-TOP> <a short plain title>
- at: <standard: a point [x, y, z] or text>
- lens_mm: <standard: millimetres>
- ratio: <standard: text>
- fps: <standard: a number>
- overlays: <standard: text>
- moves: <standard: never, pan_only or operator>
- master_clip: <standard: an ID of SHOT (SC10-SH150) or PREVIS (PV-SC10-SH080-V01), or none>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> CAMERA: A camera inside the story (security feeds, recordings). (in-story camera; ID CAM- and capitals and hyphens, like CAM-SHAFT-TOP; lives in 08 Places and things.md.)
> status: draft, approved, stale, omitted.

END OF FILE | Places and things | 5 records
~~~~

---

From the skill file `templates/09 Continuity.md`:

~~~~markdown
# Continuity

## At a glance

<How many looks each person and thing has across the film.>

## Who looks how, scene by scene

<Iona, from scene 6: her right sleeve gone, her right palm skinned.>

## Things and places that change

<One line for each change to a thing or a place, and the scene where it happens.>

Below this line: details for the AI and the checker. You never need to read them.

### STATE <the element's ID, .S and 2 digits, like CH-IONA.S02> <a short plain title>
- element: <quick: an ID of CHARACTER (CH-IONA) or PROP (PR-FLASK) or LOCATION (LOC-SAYE-KITCHEN)>
- from: <quick: an ID of SCENE (SC10)> | line: <line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)>
- cause: <standard: line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range)> | quote: <"exact story words">
- state_line: <quick: text; clothes, wounds and condition; own sides only (her right hand), never image sides>
- changes: <standard: text>
- side: <standard, one line each: text; write none when there is nothing> | own: <left or right> | plot: <yes or no>
- handedness: <standard, when mirror_rule_exists: original or reversed>
- pictures_needed: <add-on, storyboards or AI video: text>
- origin: <quick: story, inferred or invented>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> STATE: The state of a changeable person, thing or place from one line to the next state: costume, injury, condition, handedness. (state; ID the element's ID, .S and 2 digits, like CH-IONA.S02; lives in 09 Continuity.md.)
> Conditions:
> - mirror_rule_exists: The project has a RULE whose kind is mirror.
> Code adds these on every build; never type them: until.
> status: draft, approved, stale, omitted.

END OF FILE | Continuity | 1 records
~~~~

---

From the skill file `templates/10 Film rules.md`:

~~~~markdown
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
- banned: <quick, one line each: text; write none when there is nothing> | why: <text>
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
- max_uses: <quick: a whole number (3), 1_per_scene, or share> | fraction: <a number from 0 to 1, only with share>
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
- light_cue: <standard, one line each: SCnn "<exact story words, 3 or more, found once in that scene>"; write none when there is nothing> | change: <text> | why: <text>
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
- rupture_plan: <standard, one line each: an ID of SCENE (SC10); write none when there is nothing> | device: <text>
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
~~~~

---

From the skill file `templates/11 Scene.md`:

~~~~markdown
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
- departure: <standard, one line each: an ID of CAMSYS or CAMRULE (CR-ELI) or RESERVE (RC-01) or LENS (LX-01) or LOOK (LK-SAYE-KITCHEN-NIGHT) or VISUAL (VS-SQ03) or SOUNDPLAN or LADDER or RULE (WR-MIRROR); write none when there is nothing> | what: <text> | why: <text>
- additions: <standard, one line each: text; write none when there is nothing> | changes_meaning: <yes or no>
- lines_not_shown: <optional, one line each: line numbers like 449-463, or a quote anchor "<exact story words>" ("<first>" to "<last>" for a range); write none when there is nothing> | why: <text>
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
- emphasis: <standard, one line each: an ID of MOTIF (MO-MINT) or PROP (PR-FLASK) or TEXT (TX-GOODS-ONLY) or STATE (CH-IONA.S02); write none when there is nothing> | level: <a number from 0 to 3>
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
- look_at: <standard, or write look_at_words instead: [x, y] or [x, y, z] in metres>
- look_at_words: <standard, or write look_at instead: text>
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
- subject: <quick, one line each: an ID of STATE (CH-IONA.S02) or CHARACTER (CH-IONA); write none when there is nothing> | at: <unless set_plan_exists: left_edge, left_third, centre, right_third or right_edge> | faces: <unless set_plan_exists: a direction word, or the ID of what the subject faces, or an ID> | does: <text; visible behaviour only, never emotion words> | tactic: <standard: one word ending in -ing> | energy: <standard: still, held, rising, breaking or spent> | display: <standard: 1, 2 or 3> | still: <standard: words from the note, separated by commas> | eyeline: <standard: text> | dwell_s: <standard, when eyeline_set: seconds> | travel: <standard, when subject_moves: one word from the note> | must_not: <standard, when later_beat_saves_behaviour: text> | continues: <detailed: an ID of SHOT (SC10-SH150)> | recorded: <footage only: SC06>
- thing: <standard, one line each: an ID of PROP (PR-FLASK) or STATE (CH-IONA.S02) or MOTIF (MO-MINT) or TEXT (TX-GOODS-ONLY); write none when there is nothing> | emphasis: <a number from 0 to 3> | at: <text> | plant: <an ID of PLANT (PL-07)> | payoff: <an ID of PLANT (PL-07)> | recorded: <footage only: SC06>
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
- hear: <quick, one line each: an ID of SPEECH (SC10-D11); write none when there is nothing> | speaker: <on_screen, off_screen or hidden> | path: <one word from the note> | at: <seconds> | words: <"exact story words">
- effect: <standard, one line each: text; write none when there is nothing> | at: <seconds> | sound_emphasis: <a number from 0 to 3>
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
> - cut_out_on: thought_complete, action_midpoint, line_end, sound_hit, rhythm, keep_hidden
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
~~~~

---

From the skill file `templates/13 Health check.md`:

~~~~markdown
# Health check

## At a glance

<How many problems, how many must be fixed, and whether the scenes are ready.>

## What to fix first

<One line for each problem that must be fixed: where it is and what to change.>

## The three scenes to read

<The climax scene, the scene with the most talk, and the biggest action scene.>

Below this line: details for the AI and the checker. You never need to read them.

### REVIEW <RV- and a scene ID, or RV-FILM, like RV-SC10> <a short plain title>
- scope: <standard: a scene ID or film>
- answer: <standard, one line each: text> | answer: <yes or no> | evidence: <text>
- score: <standard, one line each: a number from 1 to 10> | score: <a number from 0 to 3> | evidence: <text>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> REVIEW: Judge answers and rubric scores for a scene or the film. (review; ID RV- and a scene ID, or RV-FILM, like RV-SC10; lives in 13 Health check.md.)
> status: draft, approved, stale, omitted.

### FINDING <FIND- and 3 digits, like FIND-004> <a short plain title>
- record: <quick, code writes it when checker_finding; otherwise you write it: an ID of any record ID>
- rule: <quick, code writes it when checker_finding; otherwise you write it: text>
- evidence: <quick, code writes it when checker_finding; otherwise you write it: text>
- fix: <quick, code writes it when checker_finding; otherwise you write it: text>
- source: <quick, code writes it when checker_finding; otherwise you write it: checker, film_pass, review or user>
- status: <quick: open, fixed or accepted>
- reason: <quick: text>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> FINDING: A problem found, with its fix. (finding; ID FIND- and 3 digits, like FIND-004; lives in 12 Whole-film check.md, 13 Health check.md.)
> Conditions:
> - checker_finding: FINDING.source is checker.
> - otherwise: None of the other conditions in the same writer_when list holds.
> status: open, fixed, accepted.

END OF FILE | Health check | 2 records
~~~~

---

From the skill file `templates/18 Add-on jobs.md`:

~~~~markdown
# Add-on jobs

## At a glance

<Which add-ons are on: storyboards, grey previews, AI video, or edit and finishing.>

## Storyboard frames

<One line for each frame: which shot, and what it shows.>

## Grey previews

<One line for each hard shot previewed in grey, and why.>

## Takes and voices

<One line for each video or voice take: which shot or speech, and whether it is kept.>

## Edit and finishing

<One line for each finishing job and each music cue.>

Below this line: details for the AI and the checker. You never need to read them.

> Each add-on record lives in its own file (named in its note below); this template holds them all so one file teaches every add-on.

### PIC <PIC-, the shot or element state, -, the use in capitals, - and 2 digits, like PIC-SC10-SH150-START-01> <a short plain title>
- for: <add-on, storyboards or AI video: an ID of SHOT (SC10-SH150) or STATE (CH-IONA.S02) or CHARACTER (CH-IONA) or PROP (PR-FLASK) or LOCATION (LOC-SAYE-KITCHEN)>
- use: <add-on, storyboards or AI video: one word from the note>
- moment: <add-on, storyboards or AI video: start, middle or end>
- model: <add-on, storyboards or AI video: text>
- references: <add-on, storyboards or AI video, one line each: a file name> | job: <identity, costume, set, prop or layout>
- file: <add-on, storyboards or AI video: a file name>
- checks: <add-on, storyboards or AI video, one line each: text> | answer: <yes or no>
- approved: <add-on, storyboards or AI video, you write it when storyboard_frame; otherwise the user's answer sets it: yes or no>
- cost_usd: <add-on, storyboards or AI video: US dollars>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> PIC: One picture job: the shot or element state it is for. (picture job; ID PIC-, the shot or element state, -, the use in capitals, - and 2 digits, like PIC-SC10-SH150-START-01; lives in 18 Storyboard/Storyboard frames.md, 20 Prompts for AI video/Pictures.md.)
> Allowed values:
> - use: storyboard, start, end, pinned, reference, plate, style, layout
> Conditions:
> - otherwise: None of the other conditions in the same writer_when list holds.
> - storyboard_frame: PIC.use is storyboard.
> status: draft, approved, stale, omitted.

### PREVIS <PV-, the shot (or SCNN-MASTER, or a location), -V and 2 digits, like PV-SC10-SH080-V01> <a short plain title>
- for: <add-on, grey previews, code writes it when previs_stub; otherwise you write it: an ID of SHOT (SC10-SH150) or LOCATION (LOC-SAYE-KITCHEN), or <scene>-MASTER>
- level: <add-on, grey previews, code writes it when previs_stub; otherwise you write it: a number from 0 to 5>
- standin_level: <add-on, grey previews: a number from 1 to 5>
- route: <add-on, grey previews: 1, 2, 3 or 5>
- extras: <add-on, grey previews: a file name, or none>
- stills: <add-on, grey previews: numbers separated by commas>
- approved: <add-on, grey previews, the user's answer sets it when framing_critical; otherwise code writes it: yes, no or auto>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> PREVIS: One previs job: its shot, a master (PV-SC06-MASTER) or a location. (grey preview job; ID PV-, the shot (or SCNN-MASTER, or a location), -V and 2 digits, like PV-SC10-SH080-V01; lives in 19 Grey previews/Grey preview jobs.md.)
> Conditions:
> - framing_critical: The PREVIS record's shot has framing_critical: yes.
> - otherwise: None of the other conditions in the same writer_when list holds.
> - previs_stub: The PREVIS record is a stub code created (status: planned).
> Code adds these on every build; never type them: plan_file, blocking.
> status: draft, approved, stale, omitted, planned.

### TAKE <TK-, the clip ID, -T and 2 digits, like TK-SC10-SH150.1-T03> <a short plain title>
- clip: <add-on, AI video: an ID of CLIP (SC10-SH150.1)>
- model: <add-on, AI video: text>
- route: <add-on, AI video: text>
- inputs: <add-on, AI video: short phrases separated by commas>
- seed: <add-on, AI video: a number, or none>
- settings: <add-on, AI video: text>
- cost_usd: <add-on, AI video: US dollars>
- file: <add-on, AI video: a file name>
- review: <add-on, AI video, one line each: text> | answer: <yes or no> | evidence: <text>
- kept: <add-on, AI video, the user's answer, set through a choice: yes or no>
- refusals: <add-on, AI video: a number>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> TAKE: One generated take. (take; ID TK-, the clip ID, -T and 2 digits, like TK-SC10-SH150.1-T03; lives in 20 Prompts for AI video/Takes.md.)
> status: draft, approved, stale, omitted.

### VOICETAKE <VT-, the speech ID, -T and 2 digits, like VT-SC10-D11-T01> <a short plain title>
- speech: <add-on, AI video: an ID of SPEECH (SC10-D11)>
- voice: <add-on, AI video: an ID of VOICE (VO-SAYE)>
- delivery: <add-on, AI video: text>
- tts_text: <add-on, AI video: text>
- tool: <add-on, AI video: text>
- file: <add-on, AI video: a file name>
- verdict: <add-on, AI video, the user's answer, set through a choice: pick, keep or reject>
- cost_usd: <add-on, AI video: US dollars>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> VOICETAKE: One voice take for one speech. (voice take; ID VT-, the speech ID, -T and 2 digits, like VT-SC10-D11-T01; lives in 20 Prompts for AI video/Voices.md.)
> Code adds these on every build; never type them: words_match.
> status: draft, approved, stale, omitted.

### FINISH <FX-, the shot ID, - and 2 digits, like FX-SC10-SH080-01> <a short plain title>
- shot: <add-on, edit and finishing, code writes it; in a chat without code you write it: an ID of SHOT (SC10-SH150)>
- operation: <add-on, edit and finishing, code writes it; in a chat without code you write it: one word from the note>
- tool: <add-on, edit and finishing: text>
- inputs: <add-on, edit and finishing: short phrases separated by commas>
- output: <add-on, edit and finishing: a file name>
- done: <add-on, edit and finishing: yes or no>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> FINISH: One finishing job, created from shots by code and edited by the AI. (finishing job; ID FX-, the shot ID, - and 2 digits, like FX-SC10-SH080-01; lives in 21 Edit and finishing/Finishing jobs.md.)
> Allowed values:
> - operation: flip, composite, crop, speed, upscale, deflicker, grain, grade, title, lip_sync, voice_path
> status: draft, approved, stale, omitted.

### MUSIC <MU- and 2 digits, like MU-01> <a short plain title>
- in: <add-on, edit and finishing: an ID of SHOT (SC10-SH150) or BEAT (SC10-B07)>
- out: <add-on, edit and finishing: an ID of SHOT (SC10-SH150) or BEAT (SC10-B07)>
- function: <add-on, edit and finishing: text>
- must_not: <add-on, edit and finishing: text>
- source: <add-on, edit and finishing: score, library or ai>
- licence: <add-on, edit and finishing: an ID of RIGHTS (RT-001)>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> MUSIC: A music cue (only if the policy is sparse or scored). (music cue; ID MU- and 2 digits, like MU-01; lives in 21 Edit and finishing/Finishing jobs.md.)
> Written only when music_policy_allows_cues: SOUNDPLAN.music_policy is sparse or scored.
> status: draft, approved, stale, omitted.

END OF FILE | Add-on jobs | 6 records
~~~~

---

From the skill file `templates/22 Rights and credits.md`:

~~~~markdown
# Rights and credits

## At a glance

<Whose story it is, and what may be done with the film.>

## What you may do with the film

<Private study, or sharing and publishing, and why.>

## Consent and disclosure

<Whose face or voice is used, with their consent, and how the film says that AI made it.>

## Credits

<The credit lines, one each: the story's author, the people who gave consent, the tools used.>

Below this line: details for the AI and the checker. You never need to read them.

### RIGHTS <RT- and 3 digits, like RT-001> <a short plain title>
- subject: <add-on, AI video, earlier when rights_subject_source, the user's answer, set through a choice: one word from the note>
- clearance: <add-on, AI video, earlier when rights_subject_source, the user's answer, set through a choice: text>
- holder: <add-on, AI video, earlier when rights_subject_source, the user's answer, set through a choice: text>
- licence: <add-on, AI video, the user's answer, set through a choice: a file name, or none>
- evidence: <add-on, AI video: text>
- commercial_ok: <add-on, AI video, the user's answer, set through a choice: yes, no or check>
- attribution: <add-on, AI video: text>
- disclosure: <add-on, AI video: text>
- status: <quick, code writes it; in a chat without code you write it: draft, approved, stale or omitted>
- locked: <quick, code writes it; in a chat without code you write it: yes or no>
- note: <optional, one line each: text>

> RIGHTS: A rights or licence record (D4). (rights record; ID RT- and 3 digits, like RT-001; lives in 22 Rights and credits.md.)
> Allowed values:
> - subject: source, voice, likeness, music, font, stock, model_terms
> status: draft, approved, stale, omitted.

END OF FILE | Rights and credits | 1 records
~~~~

---

From the skill file `reference/01 Record format.md`:

# Record format

Every numbered file in a project stores its records in "record text": plain lines that people can read and code can check. This page is the whole grammar (rules G1 to G13), three examples, and the ten mistakes that come up most, with their fixes. Field names, kinds and allowed values live in `schema/schema.json`; `reference/03 Field guide.md` lists them in words.

## Example 1: one record

```
### STATE CH-IONA.S02 Sleeve torn, palm skinned
- element: CH-IONA
- from: SC07 | line: 302
- cause: 302 | quote: "what is left of her shirt sleeve"
- state_line: one shirt sleeve torn away, palm skinned
- changes: the sleeve is gone, first seen here; the palm was skinned on the sill in scene 6
- side: skinned palm | own: right | plot: yes
- handedness: original
- origin: story
> Own right is a default (K26): the story does not say which hand.
```

A heading line names the record type, its ID and a plain title. Each field is one line: a dash, the field name, a colon, the value. A field with several parts (`side`) has a main value first and then named parts, each after ` | `. The `> ` line is a note (G8).

## The grammar

**G1. What counts.** A record file is UTF-8 Markdown. Only record headings, field lines inside a record, and the END line mean anything to the parser. Every other line (the plain part, titles, tables, paragraphs, the check table after a `---` line) is free text, kept and ignored.

**G2. Headings.** A record starts `### <TYPE> <ID> <optional plain title>`. TYPE is an upper-case word from the schema. The ID matches its type's pattern (`SC10-SH150`, `CH-IONA`, `CHOICE-021`). Singleton types (PLAN, STYLE, WORLD, CAMSYS, SOUNDPLAN, LADDER) have no ID: `### PLAN`. The title is free text after the ID.

**G3. Where a record ends.** At the next line starting with `#`, at a line `---`, or at the END line.

**G4. Field lines.** A field is one line: `- <field>: <value>`. Field names are lowercase snake_case plain words from the schema. Names are read in lower case, spaces and hyphens as underscores (`- Screen time: 15` is `screen_time`, a logged tidy fix).

**G5. Values.** A value is one line. Its kind comes from the schema:

| Kind | How to write it | Example |
|---|---|---|
| text | words to the end of the line; ` \| ` is not allowed inside | `Iona's body admits what her words denied.` |
| word | one allowed value, lowercase snake_case; case, spaces and hyphens are forgiven | `medium_close_up` ("medium close-up" is read the same) |
| number | digits; the unit is in the field name (`_s` seconds, `_m` metres, `_mm` millimetres, `_usd` dollars, `_wps` words per second) | `15` |
| yes_no | yes or no | `yes` |
| id, id_list | one ID; IDs separated by commas (a comma inside double quotes does not split) | `SC10-B07, SC10-V1, MO-MINT` |
| id_range | first and last joined by two full stops | `SC07..SC10` |
| lines | line numbers and ranges, or a quote anchor: one quoted string for one line, or two joined by `to` | `402, 449-463` or `"Iona chews it." to "street signs either."` |
| story_point | a moment inside a scene before its beats exist: scene ID and a quote anchor; from step 7 a beat ID also works | `SC24 "She deletes the way home."` |
| charge | a value's charge: `---` `--` `-` `0` `+` `++` `+++`; the sign is the direction | `---` |
| point, size | `[x, y]` or `[x, y, z]` in metres; a box `[w, d, h]` | `[2.8, 2.55]` |
| span | `t0-t1` seconds inside a shot | `0-4` |
| because_list | the ID of any story record (scene, beat, value, character, state, place, prop, text, motif, rule, plan, camera rule, saved choice, look, fact, plant), `line:NNN` or `line: "<quote anchor>"`, separated by commas, the same set in every record; or `default` on a normal shot | `SC10-B07, MO-MINT, line:456` |
| reference_list | IDs and field paths `<ID>.<field>`; a singleton record or the project is named by its type | `PROJECT.frame_shape, SC10-SU01.lens_mm` |
| scene_or_story_point | a scene ID alone for the whole scene, or a story point | `SC26` |

Quote anchors are allowed wherever a line number is: `line:` in `because`, STATE `from` and `cause`, RULE `era`, `evidence` items and CARDINAL `lines`. In chat without a numbered story they are required there. Each quoted string has at least 3 words and must match exactly once in its scope: the scene's lines for a story point or a scene field, the whole story otherwise (CITE-02). When code resolves a story point at step 7 it adds ` = ` and the beat: `SC24 "She deletes the way home." = SC24-B05`. That ending belongs to code; never type or change it.

**G6. Items.** A repeatable field appears once per item. An item is a first part followed by named sub-parts: `- subject: CH-IONA.S02 | at: left_third | faces: camera | does: chews, stops, frowns`. The first part is the item's main value, usually an ID. Sub-part keys are schema words in any order; an unknown key is an error. Positional (unnamed) sub-parts are never allowed. A few fields have no first part (the schema marks them `first_part: null`); their value starts with the first named sub-part: `- lineup: height: short | mass: slight | shape: long | value: light | colour: grey | tempo: slow`.

**G7. Empty and undecided.** Empty is `none`: a field the depth asks for with nothing to hold is written `none` (`- effect: none`), never left out (FORM-05). Undecided is `open` (listed as a question for the user). `auto` means code decides. `null`, `N/A`, `-` and a blank read as missing. Elsewhere, `- at: none` in an inbox clears a stored field you wrote (a wrong `at` once `at_words` is there).

**G8. Notes.** A line inside a record starting `> ` is a note attached to it, kept and not parsed.

**G9. The END line.** Every file ends with exactly one END line: `END OF FILE | <what the file holds> | <n> records`, for example `END OF FILE | Scene 10 shots 130-200 | 8 records`. `n` counts the file's `###` records. A missing END line or a wrong count means a cut-off reply or a dropped record.

**G10. Merging.** Records with the same TYPE and ID in several files merge field by field: a scene's list fields in `04 Scene list.md` and its design fields in its scene file; a scene's shots across batch files. The same field with two different values is an error. Items of a repeatable field are combined and exact duplicates removed.

**G11. No shortening.** Shortening markers inside a record ("...", "…", "etc.", "and so on", "same as above", "as before", "remaining shots", "omitted for brevity", a line starting `//`) are errors, unless inside double quotes that match the story.

**G12. Quotes are the story's.** Anything inside double quotes in a field value is a quotation from the story and must be found in the record's cited lines (or the scene's lines). Story words otherwise appear only in `TEXT.words` and prose `SPEECH.text`.

**G13. Headings in free text.** Free-text headings use `#` or `##` only. Any line starting `###` is a record heading, and an unknown TYPE after it is FORM-01.

## Who writes what

Every field has one writer (schema `writer`): `story` (code copies it from the story), `ai` (you), `user` (only through an answered or defaulted CHOICE), `code_state` (code keeps it: status, locks, resolved story points) or `code_derived` (computed on every build, never stored: labels, time floors, clip lengths, sides, prompts, prices). Write only `ai` fields, plus the fields marked `chat_writer: ai` when you work in chat without code; on a code surface `apply` refuses a `user` or code field from you (FORM-10). A few fields change writer with the record: TEXT `words` is copied by code from `words_from` when the story writes the text, and is yours only for invented or inferred text.

## Example 2: a whole file saved from chat

```
# Continuity

## At a glance
Iona skins her palm on the sill in scene 6; from scene 7 her shirt sleeve is gone, pressed into Jude's wound.

Below this line: details for the AI and the checker. You never need to read them.

### STATE CH-IONA.S02 Sleeve torn, palm skinned
- element: CH-IONA
- from: SC07 | line: "pressing what is left of her shirt sleeve"
- cause: "pressing what is left of her shirt sleeve" | quote: "what is left of her shirt sleeve"
- state_line: one shirt sleeve torn away, palm skinned
- changes: the sleeve is gone, first seen here; the palm was skinned on the sill in scene 6
- side: skinned palm | own: right | plot: yes
- handedness: original
- origin: story
> Own right is a default (K26): the story does not say which hand.

---
| Check | Result |
|---|---|
| FORM-06 END line present | PASS |

END OF FILE | Continuity, scene 7 | 1 records
```

This is Example 1 as it is saved from a chat app. The plain part comes first, then the fixed divider line, then the records, then the checks-in-words table after a `---` line, then the END line. The real table has a row for each of the 14 checks (`reference/06` part 1). In chat every line reference is a quote anchor; `stage.py adopt` turns anchors into numbers later.

## Example 3: the turn shot of scene 10, and one scene item

```
### SHOT SC10-SH150 Not mint
- beats: SC10-B07, SC10-B08
- lines: 454-466
- purpose: Iona's body admits what her words denied; Saye's proof lands on her face.
- because: SC10-B07, SC10-V1, MO-MINT, CR-IONA
- role: turn
- frame: single
- size: close_up
- move: static
- subject: CH-IONA.S02 | at: left_third | faces: camera | eyeline: CH-SAYE | dwell_s: 15 | does: chews slowly; stops chewing; a small frown | still: head, hands, torso
- hear: SC10-D11 | speaker: on_screen
- screen_time: 15
- moment: 4-6 | shows: stops chewing; a small frown; chews once more, slowly
- why: "Her face changes." puts the turn inside her mouth, so the scene's closest frame is spent here.
```

The lines above are some of the shot's fields, in their order; the whole record, with every Standard field, is in `examples/01 The Catch - scene 10.md`. In the same scene file the turn picture, written before any shot, reads `- turn_picture: SC10-B07 | picture: Iona close, eyes on Saye just off the lens, her mouth stopped mid-chew`.

## The ten most common mistakes

1. **Unnamed sub-parts.** Wrong: `- subject: CH-IONA.S02 | left_third | camera`. Right: `- subject: CH-IONA.S02 | at: left_third | faces: camera` (G6, FORM-12).
2. **Shortening a long list.** Wrong: `- moment: 8-15 | shows: as before`. Right: write every record in full; if the reply is getting long, stop at a whole record and the next batch continues (G11, FORM-08).
3. **A missing or wrong END line.** Count the `###` records in the file, not the shots you meant to write. `END OF FILE | Scene 10 shots 130-200 | 8 records` (G9, FORM-06, FORM-07).
4. **`###` on a free-text heading.** Wrong: `### At a glance`. Right: `## At a glance` (G13, FORM-01).
5. **A bar inside text.** Wrong: `- purpose: Iona tests the leaf | Saye waits`. Right: `- purpose: Iona tests the leaf; Saye waits` (G5, FORM-12).
6. **Typing what code works out.** Leave out labels ("10Q"), time floors, clip lengths, image sides, mirror states and prices; code computes them and drops typed values with a warning (FORM-10).
7. **Abbreviations and values off the list.** Wrong: `- size: MCU`, `- move: dolly in`. Right: `- size: medium_close_up`, `- move: push_in`. Known spellings are tidied and logged (FORM-13); others are FORM-04.
8. **Wrong ID shapes.** Wrong: `SC10-SH15`, `SC10-B7`, an ID outside the handout's block. Right: `SC10-SH150`, `SC10-B07`, IDs copied from the issued block, shots in tens (FORM-02, ID-03, ID-06).
9. **Quotes that are not exact, or anchors that are too short.** `"She fires."` has two words and appears twice in The Catch. Quote at least three words that occur once in their scope, copied exactly with the story's punctuation (G5, G12, CITE-02, CITE-03).
10. **`null`, `N/A` or a blank for "nothing".** These read as missing (FORM-05). Write `none` for empty and `open` for a question the user must answer (G7).

---

From the skill file `reference/02 Word list.md`:

# Word list

One plain word for each thing. Write "turn shot", never "key shot"; in a record that is `- role: turn`. Use the middle column in every record, card, step file and message, and never the retired words in the last column. Where the AI's word and the user's word differ, the user's word is the only one allowed above a file's divider and in messages ("group 3", never "SQ03"). The same list, as data the checker reads, is `rules/words.json`; the user's plainer version is `06 Word list.md`.

## The words and the fields they map to

| Thing | The one word, and its field | Retired |
|---|---|---|
| Story state of a person or thing in a mirror story | **reversed** / **original** (`STATE.handedness`); never "turned", which belongs to value turns | phase, frame reversed, turned (as a mirror state), handedness_phase, mirror true |
| A stretch of the film under one frame handedness | **era** a, b, c (`RULE.era`) | phase |
| How an element appears in a shot | **mirrored** / **normal** (`mirror_state`, code) | MIRRORED, mirror_state capitals |
| The edit operation | **flip** (`SHOT.flip`, `FINISH.operation`) | mirror_flip |
| The fixed words pasted into every prompt | **fixed description** (`CHARACTER.fixed_description`, `PROP.fixed_description`) | identity key, look line |
| Costume, injury and condition at a point | **state** ("Iona, state 2", STATE records) and its **state line** (`STATE.state_line`) | look ID, costume phase C1-C6, states S1-S6 |
| Light, colour and texture of a place at a time | **look** (LOOK, `SCENE.look`); its pasted text is the **look block** (`LOOK.look_block`); "look" means nothing else | look key, lighting block, global look key |
| How the film appears / how a character appears | **style** with its **style words** (`STYLE.style_words`) / **appearance** | look (for either), style key, "the film's look", "her look" |
| The main light | **main light** (`LOOK.main_light`) | key light |
| The shot where a scene turns | **turn shot** (`SHOT.role: turn`) | key shot |
| The frame a turn must show, written before shots | **turn picture** (`SCENE.turn_picture`) | key frame (as a written frame) |
| Stills a video starts or ends on | **start picture**, **end picture**, **pinned picture** (`PIC.use`) | keyframe, first frame, start frame |
| A grey still that fixes composition | **layout picture** (`PIC.use: layout`) | structure image, layout guide |
| A grey 3D video a model copies | **guide video**, made from a **grey render** (`PREVIS.route`) | control video, clay render, greybox, motion guide |
| Reference pictures of one element state | **reference pictures**; one film-look still: **style picture** (`PIC.use`, `STYLE.style_picture`) | reference pack, asset sheet, stack, model sheet, style frame |
| McKee's action and reaction | **beat** (BEAT) | bit |
| A timed visible change inside a shot | **moment** (`SHOT.moment`) | BEATS (in prompts), timeline events, C4 beats |
| "(beat)" in a script | **pause** (`BEAT.pause_after`) | beat |
| A part of a scene with its own turn | **part** (PART) | movement |
| One reply's share of a scene's shots | **batch** (`PROJECT.batch_size`) | part (for replies) |
| A group of scenes | AI: **sequence** (SEQUENCE, `SCENE.sequence`); user: **group of scenes** ("group 3") | stretch, colour-script sequence, journey unit |
| Camera movement / a character's move on the floor plan / Block's motion component | **camera move** (`SHOT.move`) / **floor-plan move** (MOVE) / **motion** (`VISUAL.component`) | movement, "move" alone in user text |
| Whose point of view a scene holds / a shot through someone's eyes | **whose scene** (`SCENE.whose_scene`) / **point-of-view shot** (`SHOT.frame: pov`) | POV for both |
| What a character wants in a scene / in life | **want** (`SCENE.want`) / **life want** (`CHARACTER.life_want`) | objective, intention, super-intention, spine, scene desire |
| What a line or act does to the other person | **tactic**, an -ing word (`tactic` sub-parts of BEAT and SHOT) | action gerund, playable action, infinitives |
| What the hands do | **task** (`BEAT.task`) | activity, physical task |
| What we see the body do | **does** (`SHOT.subject` sub-part) | emotion words, behaviour as a plan field |
| How openly a body shows a feeling / what does not move | **display** 1-3 / **still** (`SHOT.subject` sub-parts) | performance scale, intensity (for display) |
| Which way a subject crosses the frame | **travel** (`SHOT.subject`, `SEQUENCE.travel`) | screen direction (as a field name) |
| A moment in a scene named before its beats exist | **story point** (kind story_point) | beat reference (before step 7) |
| The feeling a film or scene is played in | **tone**: **home tone** (`PLAN.tone_home`), a scene's **tone**, **undercurrent**, **tone shift** (`SCENE` fields) | mood (as a field), genre (for tone) |
| The record of changing states | **continuity** (`09 Continuity.md`, STATE) | continuity bible, ledger, state table, damage ledger |
| A thing that returns and gathers meaning | **motif** (MOTIF) with **plant**, **payoff** (PLANT, `SHOT.thing` sub-parts) and **rhyme** (`PLANT.rhyme`) | carrier log, thread, emblem, hinge, reserved framing |
| A choice saved for special moments | **saved choice** (RESERVE, RC IDs) | reserved choice, reserved framing |
| Kept out of frame for later | **keep hidden** (`SHOT.keep_hidden`) | withhold, withheld |
| Readable words inside the picture | **text in picture** (TEXT, `SHOT.text`); the drawn file is the **text graphic** | on-screen text, insert graphic, text spec |
| A character's voice / a place's steady background | **voice** with its **voice description** (VOICE) / **room sound** (`room_sound` fields) | sound key, voice key, room tone key, bed, ambience |
| How a voice reaches us | **path** (`SPEECH.path`, `hear` path, `VOICE.path_sound`) | channel, voice_source, perspective |
| Where the camera stands in a scene | **setup**, "camera A" to the user (SETUP, `SHOT.setup`) | camera position S1-S8 |
| Left and right | **frame-left**, **frame-right** (`frame_left` values); **own left**, **own right** (`side` items); **hand nearest the camera** | screen left, image-left, camera left |
| The imaginary line between two people | **the line**, line of action (`SETUP.side`) | axis, 180° line |
| Shot sizes | **extreme wide, wide, medium wide, medium, medium close-up, close-up, extreme close-up, insert** (`SHOT.size`) | big close-up, EWS, WS, MCU, CU, ECU, OTS and every abbreviation |
| Tilt / eye height | **angle** / **height** (`SHOT.angle`, `SHOT.height`) | angle_height |
| Where a fact comes from | **origin**: story, inferred, invented (`origin` fields) | fact, extracted, authored, added, [design choice] |
| Who may write a field | **writer**: story, ai, user, code_state, code_derived (schema) | extracted, authored, derived, human |
| Used length / length to generate | **screen time** (`SHOT.screen_time`) / **clip length** (code) | duration_s, clip_s |
| Why a shot exists | **purpose** (`SHOT.purpose`) | PURPOSE, purpose (as picture job kind) |
| The kind of picture job | **use** (`PIC.use`) | purpose |
| A departure's reason | the record's **why** (`why` fields) | override:, WHY slot, story_reason |
| How loud a thing is / a sound is | **emphasis** 0-3 / **sound emphasis** 0-3 (`thing`, `effect`, `BEAT.emphasis`) | L0-L3, S0-S3, emphasis device |
| An extra signal on a beat | **added emphasis**, 0 or 1 (`BEAT.added_emphasis`) | emphasis device, added signal |
| Pressure inside a scene / across the film | **beat intensity** 1-5 / **scene intensity** 1-10 | intensity, story intensity |
| Whole-film facts | the **whole-film files** (05-10) and their **whole-film summary** (file 02) | bible, visual bible, asset bible, register, core facts |
| A question to the user with a default | **choice**; one grouped without asking: **small choice** (CHOICE, `CHOICE.asked: no`) | decision card, question record, small call, decision (for a choice), question (for a choice) |
| A place where the user answers | AI: **checkpoint** A, P, B, C, D, E (`CHOICE.checkpoint`); user: named by what it is | checkpoint letters in user text |
| How deep the breakdown goes | **quick**, **standard**, **detailed** (`PROJECT.depth`, `SCENE.depth`) | full (as a depth) |
| A problem found, with its fix | **finding** (FINDING) | issue |
| One step of the pipeline | **step**, counted from 1 for the user ("step 8 of 12") | stage (except "Stage", capitalised, the product's name, and `stage.py`) |
| A piece of AI work that fits one reply | **unit** (`steps.json` units) | task, call |
| The file the AI reads for a unit | **handout** on code surfaces; the attached **step file** and **whole-film summary** in chat | context pack |
| Grey 3D stand-in renders of shots | AI: **previs** (PREVIS, `SHOT.previs_level`); user: **grey previews** | clay preview, greybox (for the user) |
| Runtime and cost estimates | AI: v0, v1 (D13); user: **the first estimate**, **the estimate from the shots** | v0, v1 in user text |
| Where a take is kept or rejected | **take** (TAKE) | generation job |
| The flashlight in prompts | **flashlight** (`PROJECT.prompt_words`); "torch" only inside quotes of the script | torch in prompts |
| Model names | the exact name in `video_models.json`, with aliases ("Kling O3" = kling-3.0-omni) | informal names |

## What the user reads instead

Only the user's words go above a file's divider, into reports and into messages:

| The AI's word | The user's word |
|---|---|
| sequence, SQ03 | group of scenes, "group 3" |
| checkpoint A, P, B, C | the scene list; how the book becomes a film; the big choices; each group of shots |
| acceptance, checkpoint D, checkpoint E | the finished check; the grey previews; keeping takes |
| previs | grey previews |
| v0, v1 | the first estimate, the estimate from the shots |
| step 7 (counted from 0) | step 8 of 12 (counted from 1) |
| SC10-SH150 | shot 150 (scene 10) |

## Where the checker looks

WORDS-02 warns on a retired word in a field value or in user-facing text, read in its retired sense ("camera movement", "a sound bed"; "his movement" is plain English). Each entry in `rules/words.json` says where: everywhere, only in user text, only in named fields, only as a field name (FORM-03), only in prompts (GEN-12), or nowhere (`emblem` as a PROP kind, `spine` as a MOTIF rank).

Always allowed: "Stage" as the product's name and `stage.py`; story words inside double quotes (a script's "torch" stays); the field names `CHARACTER.movement` (label "How they move") and `SETUP.look_at` (label "Aimed at"); research codes in AI-facing files. Mood-only reasons, emotion words and banned prompt words have their own lists (REASON-04, WORDS-01, GEN-12).

---

From the skill file `reference/04 Rule order.md`:

# Rule order

When two rules want different things for the same shot, the higher rule on this list wins, and the record's `why` says which rule won and names the line, object or ID it rests on. Example: in The Catch scene 10, Eli's warning "Don't open the flask." would get a single on Eli under ordinary dialogue coverage (rule 9), but his camera rule `CR-ELI` saves his closest singles for scene 13 (rule 4), so shot 130 hears him off screen. The order merges A1, A2, A4 and B1 to B3, readability second as B2 and A1 put it.

1. What the story itself states we see and hear.
2. Readability of the beat.
3. Physical honesty.
4. The film's systems and budgets.
5. Flaw handling.
6. Turn rules.
7. Emotion over spatial continuity, logged as a departure.
8. Conflict-type defaults.
9. General beat defaults and translation menus.
10. The baseline.

## 1. What the story states

Directions, named light, written transitions and stated sounds are binding (A1's precedence, rule 1). **Tie-break.** The Catch scene 15 writes "A small CLICK, from nowhere." Played as horror, the dread tone's defaults would make the click loud and place it off frame (D10 §12.1; `tone_defaults.json`, rule 9). The story says small, so the effect item keeps a low `sound_emphasis`, and the `why` quotes the line.

## 2. Readability of the beat

The audience must be able to read the face, the text and the geography (B2, A1). **Tie-break.** The tag "Goods only. No persons." needs its reading time from the `text_floor` constant: K09 works it out as 4.0 seconds, and twice that where the text is mirrored. A tense scene's shorter target shot length (rule 9) or the film's rhythm plan (rule 4) cannot cut the insert shorter; TIME-01 holds the floor. The same rule keeps every face readable in a dark look (B2 R24).

## 3. Physical honesty

In-story footage, physics and glass optics behave as they would for real (B1 R22-R23). **Tie-break.** Scene 13 replays the recording from the shaft camera `CAM-SHAFT-TOP`. The film's camera system (rule 4) would put the lens at the owner's eye height with the normal lens, but footage from an in-story camera keeps that camera's fixed place, lens, frame rate and overlays from its CAMERA record, and every excerpt is cut from one master take of the scene 6 event (B1 R22, §10.4).

## 4. The film's systems and budgets

Banned and saved choices, character camera rules, the motif code, the colour script and location continuity are written at step 6 and hold for every scene (B1 P5, B4). **Tie-break.** The turn rule (rule 6) would give scene 10's main turn the most extreme framing the scene can reach. The film-level saved choice `extreme_close_up_film_max` and the ladder keep the film's tightest size for scene 13 (K05, K12), so shot 150 lands at `close_up`: still the scene's tightest frame, spent on its turn, within the budget.

## 5. Flaw handling

Lines carrying a BEAT `flag` are staged to contain the flaw, never rewritten: on-the-nose or melodramatic lines are staged small (A1 R35-R36), forced exposition moves to an image or off screen (R22), a monologue gets listener coverage (R31). A1 ranks these above its turning-point rules. **Tie-break.** A line flagged `melodrama` falls on a turn beat. Rule 6 wants the scene's tightest framing on the turn; A1 R36 wants the speaker static, one size wider than the scene's other beats, with no score. Flaw handling wins: the speaker's shot stays static and wider (CRAFT-21 checks size, move and music), and the turn's tightest frame goes to the listener's landing face when the listener carries the change (A1 R1).

## 6. Turn rules

The scene's most extreme framing goes on its turn, and nothing tighter comes before it (B1 R1, A2 R4; CRAFT-03), within the rules above: the ladder's rung (rule 4) sets the turn's size, a wide rung marking the turn by opening out, and a rung or a camera rule's cap may let earlier shots equal it; through one fixed in-story camera (rule 3) size cannot change, so the frame's action and the cuts carry the turn (B1 §10.5). **Tie-break.** A black-comedy reading of scene 10 would widen beat 7 and cut after "Not mint." to Saye's unmoved face (D10 §12.2), that tone's default (rule 9). The turn rule wins: the tone moves the dial, never the turn (D10 principle 1), so beat 7 keeps the scene's closest frame and the comic undercurrent rides on lines and wide shots elsewhere.

## 7. Emotion over spatial continuity

When a cut that serves the emotion breaks the geography, keep the emotion (A4 R1: emotion first, space last). **Tie-break.** In a balanced two-person scene the matched singles (A2, rule 8) keep both sides on one lens and one side of the line. If the strongest reaction can only be seen from across the line, the shot crosses it, and the scene's `departure` answers GEOM-03.

## 8. Conflict-type defaults

Each conflict type has its coverage (A2 R12-R17). **Tie-break.** Scene 10 is asymmetric: Saye drives, and the resister stays still, anchored in a task, with her closest shot saved for her turning line. The approach progression (rule 9) would tighten on Iona beat by beat; the conflict type holds her wider until her line "Not mint."

## 9. General beat defaults and translation menus

The menus in cards 10 to 14 and the tone defaults apply where nothing above decides. **Tie-break.** Scene 10 opens on Saye's view at her door: a point-of-view pan to the flask. The menu's pan beats the static baseline, and the `why` names the flask.

## 10. The baseline

Static, the owner's eye height, a normal lens, room sound. It is a strong answer, and a normal shot that departs from nothing may give `because: default` with no `why` (REASON-01, REASON-02). **Tie-break.** When two menus pull different ways and neither can cite a line, an object or an action from this story, neither wins: the shot returns to the baseline.
