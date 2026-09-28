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
