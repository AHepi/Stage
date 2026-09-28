# Digest A4: Editing, transitions, rhythm, suspense and sound

Source: `research/A4_editing_transitions_rhythm_sound.md` (840 lines). Refs: C#, R#, S#, T#, SND#, AI# are the file's rules (§9); P# is a principle (§2); § is a section; WE# is a worked example (§11). "[judgment]" marks a house value, not a sourced fact.

## 1. Scope

1. How shots join into scenes and scenes into a film: cut points, durations, transitions, rhythm, suspense, reveals, ruptures and sound.
2. Adds to A2's template. Per shot: cut-in and cut-out reasons, duration, handles, transition, sound. Per scene: rhythm plan, information ledger, rupture, beds, motifs, music, continuity log.
3. Runs after A2, A1 and B1, before the prompt files. AI clips (4–15 s) are joined, and given their sound, in an editing program.

**Terms** (§1):
- *Cut point*: the frame where a shot ends.
- *Hold*: letting a shot run on.
- *ASL*: running time ÷ shot count.
- *Rupture*: the film suddenly stops doing something it has been doing (a sound, camera behavior, cutting pattern, or the picture itself).
- *Information ledger*: who knows what, when.
- *Landing face* (A1): the face on screen when a fact lands.
- *Ambience bed*: one location sound under several shots.
- *J-cut / L-cut*: next shot's sound early / last shot's sound running on. Across scenes: a *sound bridge*.
- *Handles*: spare frames at each end.
- *Acousmatic*: heard, source unseen. *De-acousmatization*: the source shown.
- *On-the-air*: radio, phone, playback.
- *Stems*: separate dialogue, music and effects tracks.
- Frame rate: 24 fps.

## 2. Rules

"Consider" is a default. Departing needs one line in `notes` [§9]. Precedence: the text's own marks > emotion (R1) > ledger (S rules) > the rest.

**Principles**
1. [P1] If shots are generated separately, then unify them through eyelines, direction and sound, because meaning is made between shots.
2. [R1, P2] If cuts or rules conflict, then keep the emotion, dropping Murch's criteria from the bottom (emotion 51%, story 23%, rhythm 10%, eye-trace 7%, planarity 5%, 3D space 4%), because emotion comes "at all costs".
3. [P3, §4.1] If picking a cut frame, then try where a viewer would blink or look away [judgment], because a cut ends a thought. A subject near where the eye already rests cuts smoothly; one far away jolts.
4. [P10] If using a cut to black, true silence, a freeze, a smash cut or slow motion, then spend it on turning points, because such devices wear out. More than two editor-made uses per kind in a short film is inflation. Script marks and character-made freezes are exempt.

**Continuity (C)**
5. [C1] If two characters face each other, then draw the axis on the location plan first, because all singles and reverses share one side.
6. [C2, C3] If crossing the axis, then show it (a camera move, a buffer shot, a character crossing, or an insert or wide reset), or cross on a turn to disorient, because an unexplained crossing reads as an error.
7. [C4] If consecutive shots share a subject, then change the angle by at least 30° or the size by one ladder step (or intend a jump cut), because less reads as a jump.
8. [C5] If a journey spans clips, then fix screen direction (vertical too) in every prompt, reversing only with the story, because models forget direction.
9. [C6] If geography will matter under pressure, then show it calmly first and re-establish after ruptures, because it cannot be learned in a rush.
10. [C7] If a character, prop, wound or garment recurs, then log its exact state (hand, shoulder, sleeve) into every prompt, because each clip is generated fresh.
11. [C8] If cutting a conversation, then match lens, height and distance, and go to clean singles only as the conflict separates the two. The first clean close-up goes to the scene's owner at the turn, because a mismatch enlarges one person.
12. [§3.3, AI3] If an eyeline unit loses a shot, then keep the reaction, because meaning lands there. If a clip is flipped, then treat its direction, text and handedness as reversed, because a flip crosses the axis.

**Cut points and rhythm (R)**
13. [R2, AI1] If unsure where to cut, then cut later, with 0.5–1 s handles [judgment], because a long shot can be trimmed but a short one cannot grow.
14. [R3] If a movement crosses a cut, then cut mid-movement with all of it in both clips, starting and ending clips in motion, because motion hides joins.
15. [R4] If a scene turns, then make the turning shot the scene's shortest (a physical event) or longest (a realization, decision, revelation or refusal), or the event shortest and then a longer hold, because a peak is an extreme.
16. [R5] If shots have been shortening, then hold at or just after the turn, because that is the simplest rupture.
17. [§6.1, judgment] If mapping A2's intensity to duration, then start at 1 → 5–8 s; 2 → 3.5–6 s; 3 → 2.5–4 s; 4 → 1–3 s; 5 → under 1 s or 6 s+ (3× the ASL or more in fast scenes), because peaks are extremes.
18. [R8, judgment] If a shot must be read, then allow ~1 s for an insert, ~1.5 s for a face, ~1 s plus reading time at 12–15 characters/s at most for text, and double for mirrored text, because an unread shot does nothing.
19. [§6.2] If choosing a rhythm shape, then decide it before any durations, because the kind of turn sets the curve:
    - *build and cut out*: the turn launches action that continues;
    - *build, rupture, aftermath*: a loss or revelation must be absorbed;
    - *slow burn*: talk or watching that turns on one line or look.
20. [R6] If a time limit is stated, then honor it or stretch it on purpose with a note, because the audience counts.
21. [R7] If a reaction follows an event, then cut to it after the event is seen, on the landing face (usually whoever pays most), because a reaction to something unseen confuses.
22. [R9] If a pause is marked, then hold before the turn on whoever will act, and after it on whoever changed, with room tone and one sound, because the two pauses do different jobs.
23. [§3.7] If a line changes the listener, then cut to them mid-line (L-cut) on a look, breath or hitting word, not on line ends, because cutting line by line is a "tennis match".
24. [§4.2] If context gives a reaction its meaning, then shape the shot before it, ask for small expressions and skip music, because both color the face.

**Suspense, reveals, ruptures (S, §6)**
25. [S1] If surprise or suspense is possible, then choose suspense (surprise once, fair on replay), because "the public must be informed".
26. [S2] If the audience knows a danger the character does not, then hold longer on the character, because suspense is waiting.
27. [S3] If a reveal is coming, then design earlier shots backwards, each with a way of withholding, because one glimpse spoils it. The ways: frame edge (never tilting down), focus or dark, obstruction, timing, sound first, a recording. Reveal cleanly, then the landing face.
28. [S4] If clues were given, then play the reveal as confirmation (real time, clear view), because the audience is waiting.
29. [S5] If a plant matters, then show it once, calmly and unstressed, and rhyme the payoff's framing, lens or sound, because rhymes trigger memory.
30. [S6] If suspense ends, then release it in a way the audience accepts, and mislead only if the payoff rewards them, because punished suspense backfires (*Sabotage*).
31. [§6.8] If a scene turns, then allow one rupture (a break in the telling, not a loud event) at the turn, after a taught pattern, then re-establish. Stack two only at the film's peak, because a break needs a pattern.
32. [§6.9, judgment] If ordering scenes, then follow an intensity-5 scene with a quieter one, contrast ASLs at turns, keep dread in slow scenes, and save the longest holds and true silences for the biggest turns, because adjacent peaks blur.

**Transitions (T)**
33. [§5.1, T5] If no transition is written, then cut. If one is written, then keep it. Add nothing unwritten, and no new device late, to an all-cut film, because it reads as a change of style.
34. [T1] If the next scene continues, then cut (often split), keeping dissolves, fades and blacks for the story's paragraph breaks, because effects imply gaps.
35. [T2] If time passes, then use a time cut (minutes), a dissolve or fade (days, years) or a montage (the passage as content). In an all-cut script, use a cut plus a light and ambience change, because the script's grammar wins.
36. [T3] If scenes share a motivated shape, motion or sound, then consider a match cut (never a merely clever one), because it links meaning without words.
37. [T4] If a scene ends unresolved, then cut to black, stating frames and sound, because black stops a scene rather than closing it.
38. [T6] If the film is tied to one point of view, then report events elsewhere through sound, because cross-cutting breaks the point of view and the ledger.
39. [§5] If a turn falls in compressed time, then give it a scene, because a montage cannot hold a turn. If one unbroken moment outlasts any clip, then hide a cut in a motivated join object.

**Sound (SND, §7)**
40. [§7.2] If specifying sound, then label it diegetic or not, on- or off-screen, and its perspective (radio, phone and playback are on-the-air, with a device perspective), because "V.O." alone does not say how it sounds.
41. [SND1–2] If a threat should grow, then let it be heard before it is seen, placed in space. To make it pitiable, show and sync its source, because unseen sources feed imagination and seen ones lose power.
42. [SND3] If a sound recurs in the text, then make it a motif (one asset, fixed signature, clear first statement, occurrence table, rationed), because identical statements build meaning.
43. [SND4] If a scene is "silent", then specify room tone plus one sound, keeping drop-outs for ruptures and true silence for once or twice a film, because dead silence reads as a fault.
44. [SND5] If the meaning should stay open, then use no music, because music says how to read faces.
45. [SND6] If a scene should pull forward, then J-cut; to resonate, L-cut, because leading sound pulls and trailing sound lingers.
46. [SND7] If sounds compete, then name the one to hear and keep the rest below, across four layers (dialogue, sync effects, bed, music), because audiences follow about 2.5 similar layers (three or more need no exact sync) and at most 5 layers per 5 s. Never bury a key effect under a line.
47. [AI4] If shots share a location, then run one bed under all of them, replacing native ambience, and change it only for location or story, because native audio varies.
48. [§7.6] If spotting music, then set the policy once, because music must fit the final timing:
    - each cue gets an ID, in, out, function and "must not" (usually: must not state the subtext);
    - enter on a motion or cut; exit before or on a rupture;
    - spot after picture lock.
49. [SND8] If ending on a sound, then never cut it mid-pattern, because a stopped pulse reads as death.
50. [§7.1] If a static shot must build, then add a rising or ticking sound, add breath and friction where bodies must be felt, and specify the feeling, not just the source, because sound gives the image time and weight.
51. [§7.7, §5.1] If adapting narration, then use voice-over only for what the picture cannot say, and never illustrate a prose simile, because voice-over is weaker than drama.

**AI production (AI)**
52. [AI2] If a transition is not a cut, then make it in the editor, never in the prompt, because models make clips, not edits.
53. [AI5] If a line runs past ~15–17 words per 8 s clip (2.5 words/s, ~1 s of margin), then split it at a phrase boundary under a listener shot. Recurring speakers get one fixed voice plus lip-sync, because both joins and voice drift show.
54. [AI6] If clips must join invisibly, then start clip B from clip A's cut-point frame, because a shared frame makes separate generations meet.
55. [AI7] If a shot shows listening, then prompt "listening, does not speak", strip the audio and lay the line over it, because lips stay still and cuts stay movable.
56. [WE1] If a clip shows free fall or hanging liquid, then use under 3 s of it and strip the audio, because models make physics errors there.
57. [§7.8, judgment] If sourcing sound, then take:
    - dialogue: native, or a voice model plus lip-sync;
    - sync effects: native, checked;
    - beds, off-screen sound, silence: the edit;
    - motifs: one asset;
    - music: after picture lock.

    Sync is hard to add later, native ambience varies, and models fill silence.

## 3. Breakdown fields

Scene fields go in `scene_edit`; shot fields in each A2 shot (`shot_edit`). *(Not in template)* = used by the file but outside §10.

| Level | Field | Plain meaning | Allowed values / example |
|---|---|---|---|
| film | `music.policy` (set once) | Music policy | score \| sparse \| source only \| none |
| film | device budget; rupture list *(not in template)* | Editor-made blacks, freezes, true silences; all ruptures | ≤2 per kind in a short film |
| film | delivery *(not in template)* | Stems; loudness | −23 LUFS (EBU R 128); −24 LKFS (ATSC); web ~−14 |
| scene | `transition_in`, `transition_out` | Scene joins | cut, J/L-cut, fade or dissolve <frames>, cut to black <frames>, match cut, intercut |
| scene | `rhythm_shape`, `rhythm_plan`, `target_asl_s` | Curve type; curve in words; target ASL | slow burn; "build 4 s to 1.5 s over B1-B6; rupture B7; aftermath 5 s+"; 1.4 |
| scene | `rupture` | The one break | {beat, device, pattern_broken}; device: drop-out, true silence, cut to black, hold, camera behavior, music stops, pov change |
| scene | `info_ledger[]` | Who knows each fact, from when | mode: suspense \| mystery \| surprise |
| scene | `time_limit` (opt) | Stated clock | honored: yes \| stretched on purpose |
| scene | `text_cues[]`; `music.cues[]`; `notes` | Quoted text marks; cues; departures | "CUT TO BLACK."; {id, in, out, function, must_not} |
| character / prop | `continuity_log[]` | States kept across clips | "Eli: one shoe" |
| location | `ambience_beds[]`; floor plan with axis *(not in template)* | One bed per location; the axis | AMB_SHAFT_MOVING |
| motif | `motifs[]`; signature and occurrence table *(not in template)* | Statement here; fixed pattern; every use | statement: full \| partial \| transformed |
| shot | `duration_s`; `cut_in_on`; `cut_out_on` | Used length; start and end reasons | 0.6; action, look, line, sound, rhythm, reveal; thought complete, action midpoint, line end, sound hit, rhythm, withholding |
| shot | `transition_out` | Join to next shot | cut, J/L-cut <s>, match, jump, smash, dissolve, cut to black, freeze, whip pan |
| shot | `overlap_action`, `axis`, `screen_direction`, `withholds`, `text_on_screen`, `continuity` (opt) | Shared movement; sides; motion; what is hidden and how; readable text; logged states | direction: left, right, up, down, static; text: {text, mirrored, min_read_s} |
| shot | `sound.*`: `dialogue`, `sync_fx`, `offscreen`, `ambience`, `motif`, `music`, `silence`, `point_of_sync`, `split` | The shot's sound, labeled | perspective: on-screen close, off-screen, radio in ear, recording, V.O.; silence: none, room tone only, drop-out, true silence |
| generation job | `handles_s`, `clip_length_s`, `start_frame_from`, `listener_clip` | Spare frames; generated length; start image; silent listener | 0.75; Veo 3.1: 4, 6, 8 |
| generation job | `sound.model_audio`, `sound.prompt_sound_line` | Native audio kept; prompt's sound line | use native, ambience only, strip all, dialogue only |
| previs job | animatic; EDL or OpenTimelineIO *(not in template)* | Timed frames or renders with temp sound; optional export | Resolve, Kdenlive, Shotcut, Blender Video Sequencer |

## 4. Procedures

**4.1 Order of work per scene** [§0]
1. Copy the turn and intensities from A2, and list the text's edit and sound marks.
2. Fill the ledger.
3. Pick the rhythm shape, write the plan, mark the rupture.
4. For each shot: cut-in reason, cut-out reason, duration, transition out.
5. Spot the sound: beds, sync effects, off-screen sounds, motifs, music, silence.
6. Fill the spec (4.5) and run the checklist (§5).

**4.2 Reading the text's marks** [§5.1]
- FADE IN or OUT: 24–48 frames by default.
- CUT TO: a cut with a hard sound change.
- SMASH, MATCH or DISSOLVE TO: keep it.
- CUT TO BLACK.: set the frames and the sound.
- "BLACK." inside the action: an in-scene black, a rupture candidate.
- INTERCUT: plan both sides.
- MONTAGE: one short shot per item.
- FLASHBACK: a memory transition only if the grammar allows.
- (O.S.): off-screen diegetic sound.
- (V.O.) with a parenthetical, or (RECORDED): read the perspective from it.
- (PRE-LAP): a J-cut.
- (beat) or "Silence.": rank and budget it.
- CAPITALS: classify first (sound, new character, prop, on-screen text, emphasis). Only sounds go to `sync_fx`, `offscreen` or `motif`.
- Prose: a section break or "Later" is a cut or time cut. "For three days…" is a montage or time cut.

**4.3 Rhythm, reveal, motif**
- **Rhythm** [§6.1–6.2]:
  1. Choose the shape.
  2. Write the plan.
  3. Set durations, with the turn as the extreme.
  4. Check reading minimums.
  5. Contrast the ASL with the previous scene.
  6. Watch an animatic once without pausing. Needing to pause means a shot is too short or badly composed.
- **Reveal** [§6.6]: fix the final image, fill `withholds` backwards, and check all wides and reverses against it.
- **Motif** [§7.4]:
  1. Find the repeated phrase.
  2. Fix one asset and signature.
  3. State it clearly first.
  4. Map every occurrence (scene, perspective, source visible or not, meaning).
  5. Ration it.

**4.4 Invisible joins** [§5, AI6]
- Match on action: both clips hold the whole movement.
- Graphic match: compose clip B's start frame to match clip A's last frame.
- Hidden cut: end clip A on a frame filled by a join object (dark foreground, a body crossing the lens, whip-pan blur, a wall). Generate B from it and cut inside the fill.

**4.5 Template** [§10], exactly:

```yaml
scene_edit:
  transition_in: <cut | J-cut from <scene> | dissolve <frames> | fade in <frames> | ...>
  transition_out: <cut | L-cut into <scene> | cut to black <frames> | fade out <frames> | match cut (graphic|action|sound) to <scene> | ...>
  rhythm_plan: <e.g. "build 4 s to 1.5 s over B1-B6; rupture B7; aftermath 5 s+">
  target_asl_s: <number>
  rupture: {beat: <B#>, device: <sound drop-out | true silence | cut to black | hold | camera behavior | music stops | pov change>, pattern_broken: <what the film was doing before>}
  info_ledger:
    - fact: <one line>
      audience_knows_from: <scene/shot or "not yet">
      characters_who_know: [<names>]
      mode: <suspense | mystery | surprise>
  ambience_beds: [{id: <AMB_...>, location: <...>, description: <...>, changes_at: <beat, reason>}]
  motifs: [{id: <MOT_...>, statement: <full | partial | transformed>, perspective: <...>, meaning_here: <...>}]
  music: {policy: <score | sparse | source only | none>, cues: [{id, in: <beat/frame>, out: <beat/frame>, function, must_not}]}
  time_limit: (opt) {stated_in_text: <quote>, screen_time_s: <number>, honored: <yes | stretched on purpose>}
  rhythm_shape: <build and cut out | build, rupture, aftermath | slow burn>   # Section 6.2
  text_cues: [<every editing or sound mark the text itself gives, quoted: "CUT TO BLACK.", "(O.S.)", "METAL SHRIEK", ...>]   # Section 5.1
  continuity_log: [{item: <character, prop, wound, wardrobe>, state: <e.g. "Eli: one shoe; the script does not say which foot, so choose once and log it">, from_shot: <ID>}]   # Section 3.8
  notes: (opt) <reasons for departing from any rule marked "consider">

shot_edit:            # add inside each shot of A2's template
  duration_s: <number>              # already in A2; the used length
  handles_s: <e.g. 0.75 each end>
  clip_length_s: <length to generate: duration_s plus both handles, rounded up to a length the model offers (Veo 3.1: 4, 6 or 8)>
  start_frame_from: (opt) <shot ID and frame, for a match on action, hidden cut or graphic match (AI6)>
  listener_clip: (opt) <yes: generate silent listening, strip audio, lay the speaker's line over it (AI7)>
  text_on_screen: (opt) {text: "<exact>", mirrored: <yes | no>, min_read_s: <number>}
  continuity: (opt) <states from the scene's continuity_log that must be visible in this shot>
  cut_in_on: <action | look | line | sound | rhythm | reveal>
  cut_out_on: <thought complete | action midpoint | line end | sound hit | rhythm | withholding>
  overlap_action: (opt) <movement both clips must contain>
  axis: (opt) <e.g. "Iona frame-left, Eli frame-right">
  screen_direction: (opt) <toward frame left | toward frame right | up | down | static>
  withholds: (opt) <what this shot keeps out of view, and how>
  transition_out: <cut | J-cut <s> | L-cut <s> | match cut <kind> | jump cut | smash cut | dissolve <frames> | cut to black <frames> | freeze <frames> | whip pan | ...>
  sound:
    dialogue: [{who: <NAME>, line: "<exact quote>", perspective: <on-screen close | off-screen | radio in ear | recording | V.O.>}]
    sync_fx: [{what: <...>, at_s: <time in shot>}]
    offscreen: [{what: <...>, where: <behind | above | below | next room>, source_ever_shown: <yes, in <scene> | no>}]
    ambience: <bed id; level; any change>
    motif: (opt) <MOT id; statement; perspective>
    music: (opt) <cue id; in/out>
    silence: <none | room tone only | drop-out | true silence>
    point_of_sync: (opt) <event and time>
    split: (opt) {type: <J | L>, seconds: <number>, element: <what sound crosses the cut>}
    model_audio: <use native | ambience only | strip all | dialogue only>
    prompt_sound_line: (opt) '<Speaker: (delivery) "line". SFX: ... Ambience: ... No music.>'
  notes: (opt) <reasons for departing from any rule marked "consider">
```

A filled example is in §10 (sc6.S2: 0.6 s used, 0.75 s handles, a 4 s clip, audio stripped).

**4.6 Hand-off** [§14]
- Edit in Resolve (free), Kdenlive, Shotcut or Premiere.
- Deliver stems at the platform's loudness.
- EDL or OpenTimelineIO export is optional.
- Check video-to-audio output (e.g. MMAudio) against `sync_fx`.
- Check freesound.org licenses individually.

## 5. Checklists

A "no" needs a fix or a written reason [§12].

**Scene**
- Is the turning shot the shortest or longest?
- Is the rhythm plan written and followed?
- Is there at most one rupture, at the turn, breaking a taught pattern?
- Is the ledger filled, with editing that fits its mode (suspense: longer holds; mystery: point of view kept; surprise: once, fair)?
- Are plants shown once clearly, with rhyming payoffs?
- Is every non-cut transition justified by a time gap or story break?
- Is there one bed per location, changing only for story?
- Is the music policy followed, and does each cue have in, out, function and "must not"?
- Is the screen time of any time limit decided?
- Are all text marks listed and honored?
- Was the shape chosen by rule, with ASL contrast at turns?
- Do all clips match the continuity log?

**Shot**
- Does every cut have a named reason?
- Is the axis kept, or crossed deliberately and readably?
- Do repeated shots of a subject differ by ≥30° or a size step?
- Is screen direction written and consistent?
- Does a match on action hold the whole movement in both clips?
- Are inserts readable (animatic)?
- Does the reaction come after the event unless withholding?
- Does each withholding shot say what and how?
- Are handles planned?
- Is every sound labeled?
- Is silence graded?
- Is the source (model or edit) stated?
- Are flips checked?
- Does text meet its reading minimum?
- Are listener shots silent?
- Does each line fit its clip?
- Is `clip_length_s` a length the model can make?

**Common mistakes: sign → fix** [§13]
- Shot count equals line count → cut on beat changes; L-cut to listeners.
- The turning shot is as long as its neighbors → R4.
- Suspense scenes have the scene's lowest ASL → S2.
- Silence, black or handheld with nothing steady before it → teach the pattern or drop the device.
- More than two editor-made blacks, freezes or true silences of one kind → P10.
- Two singles with both characters looking the same way → floor plan; regenerate or flip (check AI3).
- A journey reverses direction between clips → C5.
- Two consecutive near-identical framings → the 30° rule, or an intended jump cut.
- A wide or reverse shows what a close shot withholds → `withholds` (S3).
- The payoff uses a different lens and angle from its plant → S5.
- "Silence" with no room tone → SND4.
- A "sad" cue under unspoken sadness → remove it, or make it anempathetic (indifferent to the emotion).
- A threat's sound and body arrive together → SND1–2.
- A motif is described differently in each scene → one asset ID.
- Native audio kept on every clip → AI4.
- "Then dissolves to…" in a prompt → AI2.
- The last sound is cut mid-pattern → SND8.
- A wound changes shoulder or a prop changes hand → C7.
- The listener's lips move → AI7.
- More than ~17 quoted words in an 8 s clip → AI5.
- Text on screen under 1 s, or mirrored text held like normal text → R8.
- Dissolves or fades the script never wrote → T5.

## 6. Saying it to AI models

- **No edits in prompts.** Never write "cut to" or "dissolves to". Split edits and motifs go in the spec.
- **Sound line order** (after Veo's documentation):
  1. Picture first.
  2. Speaker and delivery before the quoted line: `Man: (Hand on his hunting knife) "That's no ordinary bear."`
  3. "SFX:" items tied to actions.
  4. "Ambience:".
  5. "No music." if none.

  Include only what happens in that clip. Veo's own advice: "Use quotes for specific speech", "Explicitly describe sounds", "Describe the environment's soundscape".
- **Worked line** (sc6, shot 2): `Close on a woman's elbow driving into a steel STOP button on an old freight-lift control box. SFX: a heavy button clunk on impact; cage motor whine; loose grid rattling. Ambience: brick shaft, echo. No music. No dialogue.` The motor and rattle are replaced in the edit, but asking for them stops the model inventing other sounds.
- **Listener clips:** "listening, does not speak", with no quoted line. Given another's line, a model may mouth it or give it to the wrong face [judgment; check every take].
- **Every prompt states** screen direction (vertical too) and continuity states.
- **Inserts** use macro wording.
- **Faces:** ask for small, open expressions, because AI faces over-act. Constant blinking leaves no cut marks.
- **Match on action:** name the full movement in both clips ("both clips contain the full elbow strike on STOP").
- **Known failures:** models fill silence; native ambience varies; free fall and hanging liquid break physics; voices drift; flips reverse text.
- **Veo 3.1** (checked 2026-09-27): clips of 4, 6 or 8 s at 24 fps. A voice extends poorly unless present in the last 1 s. Only English is fully supported.
- **Other models:** the Sora 2 API was removed on 24 Sept 2026. Seedance 2.x, Wan 3.0 and MiniMax H3 accept audio references (C1).

## 7. The Catch

**Grammar**
- FADE IN appears once. CUT TO BLACK appears twice: after "Nobody leave this room." (just before the title card), and at the very end. Add no other non-cut scene transitions.
- Time gaps are a cut plus a change of light and ambience.
- Every freeze is made by a character (sc13, sc16, sc17).
- The film is tied to Iona's point of view, so events elsewhere arrive as sound (sc3: "Far below, a motor wakes."). The tablet feed in sc15 is its one change of point of view (a rupture device).
- Music: none, or very sparse.

**Plants and continuity**
- sc2 calmly establishes the ladder, the yellow stripe, the maintenance opening and the arm on the sill, plus a listening hold on the tooth, which is never heard to land.
- The log:
  - Eli has one shoe from sc4 (which foot is unstated).
  - Jude's shoulder wound from sc6.
  - Iona's sleeve is gone from sc7 (a prop in sc21).
  - Her palm is skinned.
  - After the turn, rings and handedness are mirrored (sc10).
- sc4's "Thirty seconds." is a clock. sc5 is build and cut out.

**sc6 (WE1).** ~36 shots in ~50 s, ASL ≈1.4 s, shaped build, rupture, aftermath. B1 bolts the camera inside the cage.
- The sill shot is held 3.0 s: false relief.
- The METAL SHRIEK arrives as a J-cut, its source unseen.
- Eli's hidden hand gets 2.5 s, the longest shot of the fall.
- Cut on the eyelids closing. Then **10 frames of black, the CLACK on the first, and true silence**: the film's only such pairing inside a scene.
- Framings repeat with the wall's direction reversed, and "UP" is held 1.5 s. Mirrored "phase B" starts here.
- Shots lengthen as the cage slows.
- The arm-on-sill insert reuses sc2's lens and angle.
- Do not cut before the boot clears the gate.
- The final shot is 5.0 s on faces: ~2.5 s of air, a late crash, then an L-cut into sc7.
- Motor and rattle mean guided travel; their absence means free fall.
- Effects are fixed assets placed in the edit.

**sc7–9.** sc7 opens on holds, with double reading time for its mirrored text. sc7 to sc8 is a time cut. sc8–9 are slow and full of dread: wrong details, traffic on the wrong side.

**sc13 (WE2).** This is confirmation (the clues came in sc6, 7, 9 and 12), mostly a slow burn.
- The footage is silent [judgment]; the room gives hum, breath, and the remote's click.
- It runs in real time: "the long second", against sc6's ~12 s.
- The looking is stacked: footage, then Iona, then Jude watching her.
- The footage stays full-frame through "Empty." and the puck.
- A diegetic freeze on the click is held ~2.5 s, then stays frozen on the background monitor: the longest-held image.
- "Not at Jude." is one held shot.
- One three-shot flinch at the silent fall; no crash is added.
- The switch-off is a drop-out into A2's graphic match to sc14.
- Shots run 3–4 s in dialogue and 4–6 s on the recording.

**Motifs (WE3)**
- **Pump**, "three uneven strokes" (example signature: 0.45 s / 0.6 s / 1.2 s rest):
  - sc15: first statement, from the tablet speaker.
  - sc16: acousmatic, behind her (a J-cut).
  - sc20–24: optional, low.
  - sc25: de-acousmatized, the flap in sync.
  - sc27: muffled in the helmet under her breath, with nothing from outside.
  - sc28: ordinary level.
  - sc30: a glass tap is added, then removed by the cloth; then the pump alone over black.
- **Engine CLICK/CLACK:** one family of sounds for every firing (sc6, sc15, sc24, sc27, the pod, the carriage).
- **Ship HUM:** a gauge. It wavers in sc23, misses a beat in sc24, and drops out in sc26 as the rupture.
- The sc27 crossings are near-black, not a cut to black.

**Ending (sc30).** Hold the vessel on the cloth for at least two cycles after the tapping stops, lowering the ambience. Cut to black (not a fade) in the rest between cycles. No music. `transition_out: cut to black; sound continues (L-cut into black)`.

**The Long Places, chapter VII (WE4)**
- The three days: a montage on the drill's metric note, with same-position jump cuts on Melek and a growing core stack (no window).
- "You knock loudly" is half-masked by the drill.
- The rupture: the hollow note. Switching the drill off is a staging choice.
- The lost camera is only heard: a tick, a silence, one knock, no bounce. It plants "They stand, or they roll." The sound designer must not "improve" it.
- The knock motif comes in three sizes. The letters are voice-over candidates.

**To decide** [§15]
1. The music policy.
2. After the final cut, the pump continues under the credits or recedes.
3. The sc13 footage silent or tinny.
4. The optional pump in sc20–24.
5. The *Long Places* letters as voice-over or not, and whose voice.
6. Platform and length.

Also: whether sc4's clock is honored, and which foot is Eli's.

## 8. Conflicts and open questions

- **Words per clip:** A4 says 15–17 per 8 s; A1 says 16–24.
- **Holds:** A4's intensity-5 hold is 6 s or more; A1 R15's long hold is 3 s or more; A2's "(beat)" is ~1 s. These are unreconciled.
- **Scene vs film peaks:** R4 makes every turn its scene's extreme; §6.9 and A2 R31 save the film's longest holds for the biggest turns. There is no precedence.
- **Scene numbering:** A4 follows A2 (sc13 is the glass partition); A1 calls it 07.
- **Clip lengths:** 4–15 s generally (C1); the spec uses Veo's 4, 6 or 8 s.
- **Device budget:** it counts only editor-made devices, so each black or freeze needs an origin tag.
- **Depends on:**
  - B1: ladder, phase B, flips.
  - A1: landing face, pause ranking.
  - A2: intensities, plants, the sc14 match.
  - C1: audio references, physics failures.
  - C2: animatics.
- **Judgments, not sourced:** the duration table, reading minimums, handles, the 10 frames, the silent sc13 footage, rhythm across scenes, the sound-source table, the blink test.
- **Unverified:**
  - Murch's date (1995 vs 1992).
  - The Hackman blink story.
  - Eisenstein's own examples.
  - Dmytryk's rules 4–7.
  - Five of Chion's terms.
  - Bordwell's per-film ASLs.
  - The Kuleshov effect's replication (mixed).
  - Salt's small J/L-cut sample.
  - YouTube's −14 LUFS.
  - All "well-known" film examples.

## 9. Section map

- **§0** How to use: position, order of work.
- **§1** Vocabulary.
- **§2** Principles P1–P10.
- **§3** Continuity:
  - 3.1 axis, flips
  - 3.2 the 30° rule
  - 3.3 eyeline
  - 3.4 match on action
  - 3.5 direction
  - 3.6 establishing shots, creative geography
  - 3.7 shot/reverse
  - 3.8 continuity log
- **§4** Theory:
  - 4.1 Murch's Rule of Six, the blink
  - 4.2 Kuleshov
  - 4.3 Eisenstein's five methods
  - 4.4 the editors, Dmytryk
- **§5** 18-transition catalogue (meaning, use, avoid, AI method); 5.1 text marks mapped to fields.
- **§6** Rhythm:
  - 6.1 ASL, duration table, reading minimums
  - 6.2 shapes
  - 6.3 holds
  - 6.4 reactions
  - 6.5 ledger, clocks
  - 6.6 reveals
  - 6.7 plants
  - 6.8 ruptures
  - 6.9 across scenes
- **§7** Sound:
  - 7.1 Chion
  - 7.2 labels
  - 7.3 layers, bridges
  - 7.4 motifs
  - 7.5 silence
  - 7.6 spotting
  - 7.7 voice-over
  - 7.8 model audio, dialogue fitting, sources, prompt line
- **§8** Translation table: 25 story meanings mapped to cutting, transition and sound.
- **§9** Rules and precedence.
- **§10** Spec and filled example.
- **§11** Worked examples: WE1 sc6 shot table; WE2 sc13; WE3 motifs and ending; WE4 *Long Places*.
- **§12** Checklist.
- **§13** Mistakes.
- **§14** Tools, delivery.
- **§15** Open questions.
- Sources.
