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

### TAKE <TK-, the clip ID, -T and 2 digits, like TK-SC10-SH150.1-T03 or TK-SC10-CL03-T01> <a short plain title>
- clip: <add-on, AI video: an ID of CLIP (SC10-SH150.1, or a route clip such as SC10-CL03)>
- model: <add-on, AI video: text>
- route: <add-on, AI video: text>
- inputs: <add-on, AI video: short phrases separated by commas>
- seed: <add-on, AI video: a number, or none>
- settings: <add-on, AI video: text>
- cost_usd: <add-on, AI video: US dollars>
- file: <add-on, AI video: a file name>
- review: <add-on, AI video, one line each: text> | answer: <yes or no> | evidence: <text>
- rule: <add-on, AI video, one line each: a rule ID of the route, like H3R-16> | verdict: <confirmed, wrong or unclear> | note: <text>
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
