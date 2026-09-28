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
- rhyme: <standard: yes or no> | framing: <text>
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
