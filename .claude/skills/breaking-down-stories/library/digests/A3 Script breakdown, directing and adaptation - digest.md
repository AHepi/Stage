# Digest A3: script breakdown, directing analysis, continuity, adapting prose

Source: `research/A3_script_breakdown_directing_and_adaptation.md` (782 lines). Refs in brackets point to the file: R# = its decision rule (§9), P# = principle (§2), § = section, Ex# = worked example. "Rule N" without brackets means this digest's numbered rule in section 2.

## 1. Scope

1. Reading a script as a director does (event, objective, obstacle, playable action, key shot) and parsing screenplay text reliably, including Fountain and *The Catch*'s variant markup.
2. Turning that reading into production paperwork (breakdown sheet, story days and looks, stripboard, shot list, floor plan, continuity bible, lined script) and saying what each feeds downstream (asset lists, prompts, batches, Blender blocking).
3. Adapting prose into scenes (externalization ladder, POV, summary and iterative passages, letters, time jumps, scene selection), plus a 21-item element-extraction checklist. Pass order: parse → director's pass → breakdown → continuity; for prose, adaptation runs first.

## 2. Rules

**Convention [§9]:** "then" is firm; "then consider" is a default, broken only with a one-line reason in the scene's `notes`; firm beats default (as in A2).

*General*
1. [P2, R24] If any item enters the breakdown, then label it `fact` (stated), `inference` (implied, evidence cited) or `invention` (choice); inventions are minimal and logged with the source lines they serve, because unlabelled inventions rewrite the story.
2. [P10] If unsure, then add an open question, because a wrong guess costs every downstream generation.
3. [P8] If producing paperwork, then keep breakdown sheet, shot list, floor plan, storyboard, bible and lined script separate, because each answers one question.
4. [P6, §5.7] If planning shots, then draw the floor plan first and choose staging by comparing the frames each camera position gives, because a storyboard (optional) is only views into the plan.

*Analysis*
5. [P1, R1] If the event will not fit one past-tense sentence, then list beats (A2) and write it from the first beat after which a value or relationship differs; if none, `event: none`, flagged as transition or for review, because the event usually hides in a reaction.
6. [P3, R2] If a performance note is an emotion adjective, then replace it with a playable action or physical task (adjective to `notes`), because a result cannot be played or prompted reliably.
7. [§3.2] If a verb is offered as a playable action, then it must fit "I ___ you" (own particle allowed: "shut you down") and aim to change the other person; "to inspect" fails the first (→ `physical_task`), "to bristle" the second (→ the attempt behind it, "to rebuff"); a beat alone or on objects gets a task only, because only an attempt on someone can be played.
8. [R3] If an objective is granted mid-scene, then consider ending within one or two beats (`exit_point: beat N`), because the scene is then over.
9. [R4] If the audience must know what a character does not, then plan that shot at least one beat before it matters (`audience_knows_more`), because suspense needs advance knowledge.
10. [R5] If a face carries an unspoken thought, then record the shot before it (`cut_against`) and give the face a compatible physical task, never a blank stare, because the prior shot shapes the reading (Kuleshov), but modestly.
11. [P5, R13] If an object is handled or seen closely, then it is a prop with a reference asset, with inserts sized to its story importance, because hero objects must match shot to shot.

*Parsing*
12. [§4.3] If any line starts `## INT` or `## EXT`, then use the *Catch* dialect (`## ` heading; `@` cue, nothing else is a cue; leading `=` block title page, later `=` title card); else Fountain; no markup, standard text, because Fountain tools delete all 30 *Catch* headings and hide the cards.
13. [§4.1, §5.1] If a secondary heading appears (`ANGLE ON`, `CLOSE ON`, `WIDER`, `ON THE MONITOR`, bare `LATER`), then record a shot request or ellipsis in the scene, never a new record; keep source numbers, else number once, never renumber (additions 12A, cuts `OMITTED`), and put the scene number in every shot ID, because numbers must never shift.
14. [§4.1] If a cue has an extension, then strip it before counting characters (`(O.C.)` = `(O.S.)`; `(CONT'D)` is not a new speech; custom tags get a sound note); `(beat)` is a pause, not a McKee beat, because extensions describe hearing, not speakers.
15. [R15] If a `(V.O.)` cue has a device parenthetical (`(in her ear)`, `(over the radio)`, `(on the phone)`), then set `voice_source` to it as in-scene sound; else inherit the speaker's previous V.O. source in the sequence; only if none and the speaker is absent, narration, flagged, because they need different sound and picture.
16. [§4.1] If the time word is `CONTINUOUS`, then no time passes; `LATER` allows changes; `SAME` usually means intercut; `FLASHBACK`/`DREAM` set `time_frame` until closed, with flashback states on the earlier story day, because each word fixes what may change.
17. [§4.1, §5.2] If length is needed, then use eighths (minimum 1/8) for scheduling only and estimate screen time from beats, because page ≈ minute holds only across a whole script.

*Breakdown and continuity*
18. [§5.3] If an object is named or handled, then prop; only part of the room, set dressing; changes state on screen, prop plus continuity row; impossible for a real object, VFX; physical on set, SFX (plus VFX if unfilmable); a person falls, is thrown, fights or is carried, stunt; named silent roles, cast; creatures, cast and VFX; because each department supplies exactly its items.
19. [R6] If two headings may name one place, then merge only on evidence (a line saying so, matching objects, movement straight between), recorded with its label; else keep apart and ask, because a wrong split or merge forks every reference.
20. [P7, R7] If a state can change, then give it a bible row now, anchored to a source line, because late discovery means regenerating shots.
21. [R8] If a scene is `CONTINUOUS`, then copy every state, position and held object forward, changed only by a line inside, because it is the same moment.
22. [§6] If a non-continuous scene shows an unexplained new state, then log it where first visible as inference naming the gap; if entry ≠ previous exit with neither change nor ellipsis, flag an error and ask, because the fault is in source or breakdown.
23. [§5.4] If costume, hair, makeup or injury changes, then assign a new look ID (IONA-L2) cited by every shot and prompt, tracked by story day (a mid-scene change is a bible state change), because looks decide which references to make.
24. [R14] If a feature's side matters (ring hand, scar, injured palm), then record it in the look (fact, inference or open question) and state it in every prompt, because generators pick sides at random and mirror freely.
25. [R12] If a story rule changes how things look (mirror, colour shift), then add a per-scene flag listing obeying elements, because every department must apply it alike.
26. [R11] If on-screen text must be read, then specify wording, case, orientation (normal/mirrored), surface and `method: composite`; `generate` only for text too small to read, because models render text unreliably.
27. [R21] If a mark (scar, ring, burn) would identify an anonymous figure, then omit it unless the source identifies them, because makeup makes claims the text may withhold.

*Shots and staging*
28. [R16, §5.6] If continuous physical action needs several angles, then consider one designed shot or a chain each starting where the last ended, not master-plus-coverage; for dialogue, unmatched singles (one line per generation), the wide only at start and turning point; plan edit order now, because setups are separate generations, performances do not repeat, and nothing is spare.
29. [§5.6] If consecutive shots show one subject, then change size clearly or angle by ≥ about 30°, on one side of the line of action unless crossing is planned, because otherwise it reads as a jump cut or direction error.
30. [§5.8] If a character moves, then start the move on a new beat or tactic, else cut it, because unmotivated movement is noise and costs a generation.
31. [R10] If the source gives character-relative left/right, then convert to frame-left/right per named setup, because they are opposite when the camera faces the character.
32. [R9] If a later scene replays an earlier one on a screen, then add that camera to the earlier floor plan as a named setup, because the replay is a shot of the earlier scene.
33. [§5.9] If a sequence is a journey, then keep one direction of travel in every setup until the story turns it, because the reversal must be the one planned break.
34. [§3.1] If continuity must break, then only on purpose, for emotion, because audiences forgive spatial mismatch sooner than false emotion (Murch: emotion 51%, story 23%, rhythm 10%, eye-trace 7%, 2D plane 5%, 3D space 4%).
35. [R22] If a plant is deliberately buried, then match its neighbours' size, duration and framing (no push-in, music cue or isolating light), held about 1 s per 3 words, never under 2 s, because emphasis announces the ending.
36. [R23, §8] If a scene, image or motif recurs, then save the first occurrence's camera, lens, framing, light and blocking as a named template for every repeat, because repeats must match to be recognized.

*Adaptation*
37. [§7.3] If the source is close third person, then `pov: <character>` and no shot of what she cannot see or know without `pov_break: <reason>`; show her view as POV plus reaction, or over-the-shoulder (safer for AI: keeps her reference). First person: narrator is POV and first V.O. candidate. Omniscient: choose per scene, switching only on a shot that carries it. Because every camera position is a point of view.
38. [R17, §7.2] If a passage is interior, then consider the externalization ladder from behaviour down, stopping at the first rung that works, and log it, because V.O. and text used first weaken the image; V.O. must add what the picture cannot.
39. [R18] If a passage is iterative, then consider one dramatized instance (with a change or plant, else the first) or a montage of 3–4 visibly different instances, never identical repeats, because film shows one moment at a time.
40. [§7.4] If a passage is summary, then a short representative scene, montage, one implying image, or nothing; a pause becomes set design, light and one or two establishing images, not a held shot of nothing, because film is singulative scene.
41. [R19] If a summary sentence has a place, a time, two people and a change, then consider it a buried scene, because it can be dramatized.
42. [§7.6] If speech is reported, then give each report to a named speaker, let them contradict in the room, keep source words, and label short new lines, because one invented line usually suffices.
43. [R20, §7.7] If a letter reports a stageable event, then consider staging it with at most 4–6 letter lines as V.O.; value in voice or rules: V.O. frame or the act of writing/reading, cut to lines images do not say; exact words matter: insert those words only; framing text recurs: set its frequency once as a series rule; writer deliberately unidentified: hands, room or page, never a face, no unsourced voice features; because the letter must earn its voice.
44. [§7.8] If the audience must know how much time passed, then prefer a story-world carrier (dated document, light or season, costume, object state) to a title card; flashbacks need a clearer one (match cut on an object, sound bridge, consistent treatment), because a cut already implies time.
45. [§7.9] If deciding what becomes a scene, then score five tests (cardinal function; value change; plant; showable by behaviour/objects; defining first appearance) and apply in order: passes 1: keep (own scene if also 2 or 4, else fold into the nearest scene with the same place or people; never cut); ≥2: own scene; exactly 1: fold in as shot, line or prop; none: cut, moving and logging needed information; because reviewers must see why.
46. [§7.5] If material films badly, then substitute filmable material of the same meaning, preferring images tools render consistently, and log every composite, moved line or deleted strand with source lines, because later passes must know what is invented.

## 3. Breakdown fields

| Level | Field | Plain meaning | Values / example |
|---|---|---|---|
| film | `spines` | Whole-story want per principal, as a verb phrase | "to get her brother home" |
| film | `open_questions` | Decisions the source leaves open | "Does Iona keep the torch?" |
| film | `adaptation_log` | Per passage: five-test score, rule, ladder rung, compressions, labelled inventions | rung: behavior |
| film | `series_rule` | Frequency of a recurring framing text | open only \| open and close \| every return |
| sequence | `sequence`, `travel_direction` | Scenes playing as one action; screen direction held | "1–7 rescue"; "up = frame-top" |
| scene | `scene_number` | Locked number | 6 \| 12A \| OMITTED |
| scene | `int_ext`, `place`, `time`, `modifier` | Parsed heading | INT. \| EXT. \| INT./EXT. \| I/E; "(ON THE TABLET)" |
| scene | `set`, `location` | Canonical set; real place or generated environment | FACTORY: FREIGHT SHAFT |
| scene | `time_frame`, `story_day` | Story-time layer; day of story | present \| past \| dream; D1, N1 |
| scene | `eighths`, `synopsis` | Scheduling length; one line of what happens, no later reveals | `2 2/8` |
| scene | `analysis.*` | Event, driver, Mamet answers, beats, turning point, key shot, must-see, audience knowledge, entry/exit, facts, questions | template §4B |
| scene | `exit_point`, `pov`, `pov_break` | Early end; whose scene; reason for out-of-POV shot | beat N; IONA |
| scene | `frame` | Story-rule flag plus obeying elements | normal \| reversed |
| scene | `notes` | Default overrides; kept adjectives | free text |
| scene | element categories | Cast, stunts, extras silent/atmosphere, SFX, props, vehicles/animals, sound/music, wardrobe, makeup/hair, special equipment, production notes, set dressing, VFX, greenery, weapons, consumables/breakables, on-screen text, screens in frame, states, reference assets needed | canonical names |
| beat | `playable_actions_by_beat`, `physical_task`, `turning_point` | One transitive verb per character; hands' task; beat of the event | to warn \| "(task only)"; beat 2 |
| shot | shot-list columns | scene, shot (I and O skipped), setup, description, size, angle/height, lens, movement, subject and eyeline, characters, dialogue/action covered (first/last words), sound, special equipment, est. duration, notes | size: extreme wide … insert |
| shot | `key_shot`, `states_in_play`, `references`, `onscreen_text` | Pipeline additions | yes \| no |
| shot | `cut_against`; per-shot state | Shot before a thinking face; within-scene matches | shot id; "flask right hand" |
| shot | coverage map | Which shots show each line/beat, whose face is on | from lined script |
| character | `cast_number`, `aliases` | Fixed ID by role size; merged names | 1 = lead; DR SAYE = SAYE |
| character | `look_id` / looks | Complete appearance with scene range | IONA-L1 … L5 |
| character | side features, handedness, `voice` | Ring/scar/smile side; voice age, accent, texture | fact \| inference \| open question |
| character | `voice_source` (per V.O. line) | How it is heard | narration \| radio or phone \| recording \| thought |
| character | mark policy | Deliberate absence of identifying marks | `keeper_hands: … no identifying marks (deliberate)` |
| location | set record | Canonical name, sub-areas, INT/EXT, time, weather, period, practical lights, dressing states, merge evidence | period `unstated` |
| prop | element record | name, category, scenes, label, first-appearance line, states by scene, reference needed, notes | prop \| hero \| weapon \| consumable \| document \| set dressing |
| prop | text spec; screens in frame | Wording, case, orientation, surface, reader, method; screen content per shot | composite \| generate |
| prop / state | continuity row | element, scene, enter, exit, changes, label, anchor | template §4H |
| motif | plant/payoff registry | Plant, payoff scene, emphasis flag | "do not emphasize" |
| motif | named setup template | Saved setups for a bookend/refrain | camera, lens, framing, light, blocking |
| generation job | batch; queue row | Shots sharing set, look, light and references; one row = one clip or still | stripboard equivalent |
| previs job | floor plan | Top view: walls, doors, furniture, lights; numbered moves tied to beats; setups with lens and view wedge; line of action; named replay setups | IONA 1 → IONA 2; 6-SEC |

## 4. Procedures

**A. Parse** [§4.3]: (1) detect dialect (rule 12); (2) split at scene headings only, number (rule 13); (3) split heading into `int_ext`, `place` (after prefix, before the last ` - `, so hyphenated names survive), `time`, modifier (after time = presentation note; inside place = alias); (4) classify blocks: cue+extension, parenthetical, dialogue, action, transition, title card; set `voice_source` (rule 15); (5) tag capitalized action tokens, first test that fits: name/role with description or first appearance → character intro; printed/displayed/read → on-screen text; a noise or action whose point is noise → sound cue (+ action beat); object's first mention → prop/creature intro; else emphasis, then check for a state change (`RED` then `GREEN`); (6) flag inline shot instructions (`VISOR VIEW:` POV with overlay; `BLACK.` black frame; `(ON THE TABLET)` scene on a screen); (7) normalize characters (aliases; silent THE FIGURE counts); (8) normalize sets (rule 19); (9) one record per scene plus open questions; (10) check: records = headings, every stripped cue in cast list, every post-title `=` line a title card; mismatch = dialect misread.
Fountain [§4.2]: heading = `INT`/`EXT`/`EST`/`INT./EXT`/`INT/EXT`/`I/E` + dot or space, blank lines around (force `.`; numbers `#1#`); character = caps line, blank before, none after (force `@`); transition = caps ending `TO:` (force `>`; `>X<` is centred); `#` sections and `=` synopses are not printed.

**B. Director's pass** [§3.2]: (1) read the whole source twice; (2) facts list (quoted/line-pointed) and questions list; (3) spines; (4) per scene: event, driver, each character's objective, obstacle, playable action, and Mamet's "Who wants what? What happens if they don't get it? Why now?"; (5) beats and turning point (A2); (6) one playable verb per beat per character (rule 7); (7) must see: key shot, sized inserts, reactions and what each is cut against; (8) audience-vs-character knowledge and the shot that creates it; (9) physical tasks; (10) enter late / exit early. Template (verbatim):

```yaml
analysis:
  event: "past-tense sentence"
  driver: CHARACTER
  mamet: {who_wants_what: "...", if_not: "...", why_now: "..."}
  characters:
    - name: IONA
      objective: "to get Jude to run the cage gently"
      obstacle: "the brakes are gone; Jude's pride"
      playable_actions_by_beat: [to dismiss, "(task only)", to warn, to shut down, to instruct, to soothe, to command]
      physical_task: "checks rails, ropes, gate; kneels with torch under floor frame; finger in bolt hole"
  beats: [...]            # from A2
  turning_point: beat 2
  key_shot: "insert: finger in empty bolt hole, thread still sharp"
  must_see: [inserts, reactions and what each is cut against]
  audience_knows_more: "none yet" | "..."
  enter_late_exit_early: "..."
  facts: ["line 26: Two brake brackets, empty..."]
  questions: ["Does Iona keep the torch after scene 2?"]
```

Starter verbs (the file's own): to warn, test, probe, dismiss, reassure, soothe, needle, challenge, accuse, confide in, plead with, bargain with, stall, deflect, shut down, command, protect, recruit, comfort, punish, disarm, tease, corner, rebuff, release.

**C. Breakdown sheet** [§5.3]: header = sheet number; scene number; scene heading; INT/EXT; day or night; story day; page length in eighths; set; location (real place or generated environment); one-line synopsis. Conventional marks: cast red, stunts orange, silent extras yellow, atmosphere extras green, SFX blue, props purple, vehicles/animals pink, sound/music brown, wardrobe circle, makeup/hair asterisk, special equipment box, production notes underline. Add set dressing, VFX, greenery; AI additions: on-screen text and graphics, screens in frame, states, reference assets needed; keep weapons and consumables/breakables. Fill by rule 18.

**D. Days, looks, batches** [§5.4–5.5]: number days D1, N1, D2…; list each character's numbered looks with scenes (the AI "day out of days"). Strips: number, set, INT/EXT, day/night, eighths, cast numbers (white int day, yellow ext day, blue int night, green ext night); for AI, batch by set, look and light.

**E. Floor plan** [§5.8]: top view to rough scale: walls, doors, windows, furniture, lights; start marks and numbered moves tied to beats (text moves fact, added moves invention); setups with lens and view wedge; line of action; frame-left/right per setup. Tools: paper, Shot Designer, StudioBinder, Blender top orthographic view (becomes previs).

**F. Coverage map** [§5.9]: the lined script (one vertical line per setup, labelled `6C`; straight = speaker on camera, wavy = off) becomes a map of which shots show each line and action beat and whose face is on; it exposes unshown beats.

**G. Downstream** [§5.10]: breakdown → asset lists; looks and bible → per-shot prompt states; stripboard → batches; shot list → generation queue; floor plan → Blender blocking; storyboard → optional first frames; coverage map → edit plan.

**H. Continuity bible** [§6]: rows = changeable elements, columns = scenes, cells = states; built during breakdown. Row (verbatim):

```yaml
- element: IONA_PALM          # canonical name; side recorded once decided
  scene: 7
  enter: skinned              # must equal previous scene's exit
  exit: skinned
  changes: []                 # none here; in scene 11 it becomes [{to: "bandaged", anchor: "line 498: dressing Iona's palm", label: fact}]
  label: fact                 # fact | inference | invention
  anchor: "line 286: Her palm drags across the bright steel."
```

State diff after each scene: (1) copy previous `exit` to `enter` (binding under `CONTINUOUS`, with positions and held objects); (2) walk lines, add each change with line number; `exit` = last state; (3) unexplained non-continuous difference → log at first showing, inference, name the gap; (4) flag entry ≠ previous exit with no change or ellipsis, ask; (5) add per-shot state columns for within-scene matches.

**I. Adaptation** [§7]: (1) tag passages by Genette speed (scene, summary, ellipsis, pause) and singulative/iterative; find buried scenes (rule 41); (2) score and decide (rule 45), keeping every cardinal function; (3) set POV (rule 37); (4) externalization ladder, stopping at the first rung that works (a non-reader could tell the thought from picture and sound as clearly as the source, or with the same ambiguity): 1 behaviour, 2 object, 3 juxtaposition, 4 framing and light, 5 sound, 6 dialogue under pressure (rules often become lines to a newcomer), 7 voice-over, 8 on-screen text (rare, exact, legible), 9 cut it and say so; (5) letters, most to least dramatic: dramatize the event; V.O. frame; insert of an exact phrase; the act of writing/reading; on-screen text; cut (rule 43); (6) compress, convert reported speech, carry time jumps, log all; (7) output scenes in screenplay form and run A–H.

**J. Element extraction** [§10]: each item gets name (canonical), category, scenes, fact/inference/invention, first appearance line, states by scene, reference asset needed (yes/no), notes. Pass 1: line by line, is each noun a person, place, object, sound, text, light or substance? Pass 2: down the 21 categories (§5). Either pass lists an item. Merge across scenes by canonical name.

## 5. Checklists

**Per asset, 21 categories** [§10]: 1 speaking characters (aliases, cast number, look, side features, handedness, voice, numbered looks); 2 non-speaking characters and creatures (creatures also VFX); 3 extras, incl. implied ("Police lights" → police); 4 stunts (incl. weightlessness, carrying); 5 sets (sub-areas, INT/EXT, time, weather, period or `unstated`, practical lights, dressing states); 6 set dressing; 7 props and hero props (weapons; consumables/breakables with per-shot state; documents, text to 15); 8 wardrobe per story day with damage; 9 makeup, hair, injuries and progression; 10 vehicles and animals (incl. wheel side); 11 practical SFX; 12 VFX; 13 sound (diegetic, off-screen, radio/recorded and how heard, silences, sound plants); 14 music (only if specified or played); 15 on-screen text (wording, place, orientation, reader); 16 screens in frame, shot by shot; 17 special technique (Blender previs, compositing, motion reference, `BLACK.`); 18 states and story rules; 19 time (day, time, ellipses, jump carriers); 20 plants and payoffs (payoff scene, emphasis flag); 21 open questions.

**Per scene** [§11, 25 items]: heading parsed; event one past-tense sentence; driver named; each character has objective, obstacle, playable actions; no emotion adjectives; Mamet's three answered; key shot named and in shot list; plot inserts listed and sized; key reactions name `cut_against`; audience-knows-more shot in time; every line and action beat covered; floor plan has marks, moves, setups, line of action; left/right converted; all categories incl. four AI additions; entry states match previous exit (exactly if `CONTINUOUS`); changes anchored or marked inference; text word for word with orientation; screens have specs; plants registered with payoff and flag; inventions labelled and minimal; open questions listed; eighths and story day filled; replay camera in this plan if replayed later; every V.O. has `voice_source`; `pov` set, out-of-POV shots justified; every character cites a look ID, sides stated or open; "do not emphasize" plants match neighbours and are readable.

**Per shot** (assembled from §5.6, §5.9; the file gives no separate list): key-shot flag, states, references, text; `cut_against` for thinking faces; size change or ≥30° and same side of the line versus the previous shot; frame-left/right eyelines; matching action cut mid-movement; light matches within the scene.

**Common-mistake signals** [§12]: missing headings or title card; cast longer than the story's people; `STOP` tagged as sound; one place generated three ways; emotion words in performance; a torn sleeve with no causing line; a lamp on the wrong side; unfindable "facts"; push-ins on buried details; V.O. describing the picture; identical repeated scenes; durations from page length; garbled signs; an impossible playback angle; radio voices sounding like narration; records at `CLOSE ON`/`LATER`; rings or scars switching hands; unmatched angles of one action.

## 6. Saying it to AI models

- **Behaviour, not emotion** [R2, §3.2]: prompt actions and physical tasks; a task is "the most reliable way to give a figure believable motion". A held face gets a compatible task ("keeps her finger in the hole, breathes once, takes it out"), not "she is afraid" or a blank stare [Ex1, R5].
- **Look and states in every prompt** [§5.10]: "look IONA-L2: one shirt sleeve missing, palm skinned"; always name sides (ring hand, scar, palm), since generators pick sides at random and mirror freely [R14].
- **No readable text from the model**: composite exact wording; generate only illegibly small text [R11]. Screens are two layers, inner picture and outer frame [§8].
- **Coverage is expensive**: each setup ≥ one generation and performances do not repeat, so use designed or chained shots; in dialogue, one line per single [§5.6, R16]. Over-the-shoulder beats pure POV because it keeps the character reference in frame [§7.3].
- **Batch** by set, look and light from the same references; storyboards may be image-to-video first frames [§5.5, §5.10]. Prefer images tools render consistently [§7.5]; unmotivated movement wastes a generation [§5.8]; no identifying marks on anonymous figures [R21].

## 7. The Catch

**Parse** [§4.3]: expected counts: 30 headings; 221 cues (IONA 94; SAYE 57 + 5 SAYE (RECORDED); ELI 37 + 2 V.O.; JUDE 15 + 2 V.O.; NELL 8; IONA (O.S.) 1); 3 transitions; 18 parentheticals; 8 `=` lines (6 title page, then `= THE CATCH` after the first `CUT TO BLACK.`, and `= THE END`). `IONA VALE.` and `NELL ROWAN. FLIGHT TEST.` are on-screen text. JUDE (V.O.) is an earpiece, ELI (V.O.) a radio, unmarked later lines inherit (sc4, sc21); SAYE (RECORDED) plays on Iona's wrist display.

**Sets** [§4.4]: FACTORY: LOADING TUNNEL (1); FREIGHT SHAFT with CAGE as movable piece (2, 6); TREATMENT FLOOR (3, 4, 5, 11); quarantine rooms (12–17, 29, 30) = the same rooms sealed (inference); PASSAGE, later dressed as RECEIVING ROOM (7, 18, 28; fact); SHIP sets; STREET, CAR, SAYE'S KITCHEN.

**Days and looks** [§5.4]: sc1–10 night 1; 11–13 day 2; 14–16 night 2; 17–28 day 3; 29–30 unstated. Iona: L1 sc1–6 (blue shirt, both sleeves, inferred; chipped tooth from sc2; palm skinned end of 6); L2 sc7–10 (one sleeve gone, palm skinned, Jude's blood on hands); L3 sc11–17 (bandaged palm, printed wristband); L4 sc18–28 (white pressure suit, harness, helmet in 28); L5 sc29–30 (plastic tent, hand bandaged). About 42–44 pages (line model); sc8 2/8, sc6 2 2/8, sc13 3 5/8 (estimates).

**Sc1** [Ex1]: event "Iona found the safety brakes gone and committed the three of them to the cage anyway, on one condition: stop it gently." Turning point = the silent discovery; key shot = finger-in-bolt-hole insert, then her face held for "One breath."; full-frame insert of the empty bracket; low camera at kneeling height, Jude above. Plants: "Stop it hard" and the red tag pay off in sc6. Exit on hands on ladder, torch in teeth.

**Sc6** [Ex2]: the synopsis must not say Eli clipped and fired the puck (fact only from sc13). Hero prop FLASK with PUCK; offscreen shooter (a silhouette is invention); VFX floating blood, weightless bodies, reversal after the CLACK; `BLACK.` as technique; Blender previs of the cage's down, stop, fall, rise. Exit states: Jude shoulder wound; Iona palm skinned; sleeve gone by sc7 (inference); puck on grid, clip empty; Eli one shoe; frame reversed.

**Sc6/13** [Ex3]: from Iona's eye, Jude's body hides Eli's hand; from overhead, hand and grid patch show, clear of the control box (Eli against the wall beside the box, Jude sitting back into him, Eli's face over Jude's shoulder). Named setup **6-SEC** (above the top gate, looking down), unused in sc6, renders sc13's playback with all sc6 states. Sc13: Iona's single looks frame-left, Eli's frame-right; Jude at the edge of Iona's frame.

**Screen direction** [§5.9]: "up the shaft" = frame-top in all setups of sc1–7; the reversal is the one planned break.

**Mirror rule** [Ex4, inference]: the camera shares Iona's frame. From the CLACK (sc6) to her turn (sc27) the unturned world is mirrored; afterwards the world is normal and Eli, Jude and their things are mirrored (first proof sc28, `RECEIVING` read twice). Per-scene `frame`; obeying: world text, car wheel side, Saye's ring hand, Jude's appendix scar, Eli's half-smile, meal labels. Method recorded as a choice (build the world mirrored, or shoot normally and flip while pre-mirroring what must read normally); the file calls building mirrored safer for AI.

**For the writer/user**: day of sc29–30 (healing of Iona's hand, Jude's shoulder); which palm; Iona's clothes in L3; whether Iona keeps the torch after sc2; whether the visor reads backwards; who removed the brakes (never invent on screen); red-tag wording (inferred "Goods only. No persons."); mirror method.

***The Long Places* ch. I** [Ex5]: ten candidate scenes; V.O. in scene 1 only (the letter, dramatized, hands only, no marks on keeper or child); letter scene and threshold refrain are bookend templates; item 51 hand print, brother line and tally wall are buried plants (items 47–53 held readable, no push-in on 51). User questions: one letter voice or new each return; where Nilay stays and works; whether the clock appears; letter at every chapter head or only open and close.

## 8. Conflicts and open questions

- **Mirror method conflicts across files.** A3 Ex4 calls building the world mirrored "safer" for AI. C1 (rule 7), C2 (rule 11, §7) and C3 prefer generating normally and flipping, with asymmetric details pre-reversed; B1 mixes three methods by shot type (flip and compensate, flip the background only, mirrored props for readable text). Decide once.
- **Mirror granularity.** A3: per-scene `frame`. C2: per-asset-per-shot mirror state. C1: "prompt side" and "screen side" columns. Digest rule 24 [R14] needs that split if flipping is used.
- **Verb form.** A3 playable actions are infinitives ("to warn"); A2 tactics are gerunds. A3 equates objective with A2's scene intention.
- **Scene unit.** A3: heading-to-heading, with `sequence` for dramatic units. A2: several `CONTINUOUS` headings may be one scene and a slugline may split. Both keep slugline IDs.
- **ID formats.** A3: setups `6C`, `6-SEC`, looks `IONA-L2`. A2: shots `sc10.B1.a`.
- **Timing.** Digest rule 35's [R22] on-screen reading rate (1 s per 3 words, min 2 s) is separate from A2's speech rates. Eighths are never screen time.
- **Unverified** [§14]: Hitchcock size-rule wording; Mamet quotes via a review, *Unit* memo via isegoria; Weston's method and Hagen attributions from general knowledge; Kuleshov replications disagree; colour codes and I/O skipping are conventions; *Catch* eighths estimated; mirror reading inferred; "beat from bit" unsourced. Murch's percentages appear here uncaveated but A2 marks them unverified.

## 9. Section map

- **Header, How to use**: five aims; pass order.
- **§1 Words**: ~70 defined terms. **§2 P1–P10**: principles.
- **§3.1 Sources**: Stanislavski, Hagen, Clurman/Kazan, Weston, Mamet, Katz, Hitchcock/Truffaut, Kuleshov, Murch. **§3.2**: director's pass, YAML, verbs, playable test.
- **§4.1**: screenplay elements and time words. **§4.2**: Fountain. **§4.3**: *Catch* markup, counts, 10-step parse. **§4.4**: *Catch* set normalization.
- **§5.1–5.2**: locking, numbering, eighths (20–30 setups per 12-hour day). **§5.3**: breakdown sheet, colour code, additions, filling rules. **§5.4**: story days, Iona's looks. **§5.5**: stripboard, batching. **§5.6**: shot list, sizes, coverage vs designed, 30° and line. **§5.7–5.8**: storyboard, floor plan. **§5.9**: continuity notes, lined script. **§5.10**: downstream table.
- **§6**: continuity bible, row YAML, state diff.
- **§7.1–7.9**: adaptation (ladder, POV, Genette, compression, reported speech, letters, time jumps, scene selection).
- **§8**: translation table, meaning → screen → field (16 rows). **§9**: R1–R24. **§10**: extraction. **§11**: scene checklist. **§12**: 18 mistakes.
- **§13**: Ex1 sc1 pass; Ex2 sc6 sheet and bible; Ex3 sc6/13 floor plan, 6-SEC; Ex4 mirror rule; Ex5 *Long Places* ch. I (ten scenes).
- **§14**: confidence notes. **Sources**: books, web, films, test-source paths.
