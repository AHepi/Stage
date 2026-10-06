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
- object: <standard, when set_plan_needed, always at detailed, one line each: one word> | at: <[x, y] or [x, y, z] in metres> | size: <[width, depth, height] in metres> | base: <metres> | material: <text; "from scene NN" when it arrives later> | meaning: <text> | furniture: <seat, bed or none>
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
- words_from: <quick, when text_in_story, one line each: the story line that writes the words (a line number, or a quote anchor in a chat without code)> | quote: "<the exact words inside the line, in double quotes, when the line holds more than the text>"
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
