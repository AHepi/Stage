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
- exception: <standard, one line each: an ID of any record ID> | reads: <normal or mirrored> | why: <text>
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
