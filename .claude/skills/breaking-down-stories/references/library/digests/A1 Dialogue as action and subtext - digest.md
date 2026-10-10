# A1 digest: McKee's *Dialogue* as staging (dialogue layer of the breakdown)

## 1. Scope

- Turns McKee's *Dialogue* (2016), Preface to Chapter 9, into screen decisions for talk scenes: whose face we see, what hands and props do, where pauses hold, where cuts fall, and how dialogue flaws get flagged (never rewritten).
- Input: one scene already split into beats, with value and turning point named (beat analysis is A2's job). Output: scene-level geography plus per-line fields (action, unsaid, landing face, activity, carrier, pause/sound, cut rule, flags).
- Core idea: every line is an action named by an "-ing" verb; the camera films the action and where it lands, not the words. The file adds coverage grammar (axis, eyelines) and AI-video notes, which McKee lacks.

## 2. Rules

**Terms.** *Action*: what a line really does, as a gerund (*warning*). *Activity*: the visible task it runs through. *Receiver / target*: who a line is aimed at (target when a fact is fired). *Unsaid*: what a character could say but holds back. *Unsayable*: what they do not know (unconscious), seen only in repeated choices. *Landing face* (file's term): the face on screen when a line's key word lands. *Carrier* (file's term): an object, body part, place or sound holding what the talk does not say. *Third thing*: what two characters fight through (*trialogue*; head-on is a *duelogue*). *Core word*: the word carrying a line's meaning; line designs *suspense* (last), *cumulative* (first), *balanced* (middle), *parallel*. *On-the-nose*: saying exactly what one feels. *Split edit*: picture and sound change at different moments. *Axis of action*: the line through two talkers. *Narratized*: voice-over, direct address. *Nonrealism*: fantasy, SF, musical, animation, horror, farce, myth.

**Application.** "Consider X" means "do X by default"; any departure is written in `flags` as `override:<reason>`.
**Precedence:** (1) the script's own directions about what we see ("Looks at her brother. Not at Jude.") are binding; (2) flaw rules R35-R38; (3) turning-point rules R7, R13, R14, R30; (4) the pause budget R15 caps all holds; (5) the rest.
**Tie-breaks:** R1 vs R2 (a confession or dangerous question aimed at someone): hold speaker through the line, cut to receiver on the core word, hold receiver through the pause. R6 vs R7: R7 wins, go to singles on the turning line. R19 vs R2 (a fired fact that costs the shooter): land on target, then one short shooter reaction. R29 vs R1 (volley): stay in one angle; only the change-carrying line (usually the last) gets a new closer shot on the face R1/R2 picks.

*Whose face*
1. [P1] If framing a line, then write its gerund first and let it choose (*warning* → receiver's face; *hiding* → speaker's hands; *punishing* → distance, stillness), because following words just shows whoever talks.
2. [R1, P2] If a line is aimed at someone (warning, accusing, begging, revealing), then land on the receiver, line partly or wholly off-screen, because the result shows there. At least once per scene, land off the speaker.
3. [R2] If the speaker takes the risk (confessing, asking the dangerous question), then hold on the speaker through the line and the silence after, because the cost of speaking is the story.
4. [R3] If the audience should share a character's not-knowing, then stay on that character's face/POV while the other withholds, because camera withholding creates narrative drive.
5. [R4] If the audience should know more (dramatic irony), then show the hidden thing in a shot the other cannot see, because suspense is "curiosity charged with empathy" (Hitchcock's bomb).
6. [R5] If a third character is silent, then give them at least one reaction shot at the turn, because witnesses carry the social level.
7. [R6] If equals in personal conflict play a small beat, then stay in a two-shot, because singles inflate it.
8. [R7] If the relationship breaks at the turn, then go from two-shots to singles at the turn, not before, because the reframing is the break.

*Hands, props, activity*
9. [R8, R9] If the script names a task, then frame it with the face or insert it at beat changes, and treat its stopping or changing as a reaction shot, because hands often react before faces.
10. [R10, P4] If a talk-heavy scene has no task, then propose one (`added`) that carries the action (slammed drawer = refusal) or contradicts the words ("I'm fine" while scrubbing a clean plate), or a deliberate stillness (often best for the most powerful character), changing at the turn, because empty hands push on-the-nose acting.
11. [R11] If an object is passed, grabbed, hidden, destroyed or switched off, then mark a beat and insert it, because object transfer is power transfer. Otherwise insert objects only when handled or changed.
12. [R12] If an object recurs across scenes with changing meaning, then log it as a carrier, framed the same way each time with one change, so development reads.
13. [P3] If a line has an important unsaid, then name a carrier (held reaction, hands on a prop, recurring object, changing distance, a sound swelling or dropping out, a frame within a frame), because "the camera cannot photograph thought." "She is hurt" is not a shot; "Her thumb stops turning the ring" is.

*Pauses and silence*
14. [P5] If a pause is written, then pick one picture choice and always a sound plan: hold if the character is waiting or being waited out; push-in if deciding (max one push-in per scene); cut if it is a refusal or exit, or cut wide to show new distance after a turn.
15. [R13] If it precedes the turn, then hold or slow push-in, no cut, activity stops, room tone only, no music, because it dams tension.
16. [R14] If it follows the turn, then hold on the receiver or cut wide to the new distance, let bodies rearrange and a small real sound return, because the audience must absorb the change.
17. [R15] If a scene has more than two marked pauses ("(beat)", "pause", "silence", "a long moment", "She waits", a direction with no line), then rank them by closeness to the turn, then by change in audience knowledge; long hold (≥3 s) for ranks 1-2 only; others short (<1 s), medium (1-2 s) or cuts, because "A pause must be earned."
18. [R16] If a character refuses to answer, then give the silence a shot, a duration and a gerund (*refusing*, *punishing*, *protecting*), because silence is an action. A silent powerful character: hold, camera stops, one precise movement.
19. [R17] If silence would be dead digital air, then specify room tone plus one small real sound, because true silence reads as a fault.
20. [R18] If a line could play as a nod or glance, then flag "can play silent"; never delete it.
21. [Sec. 5, 9] If music would state the subtext, then use room tone or one diegetic sound instead, saving score for transitions or counterpoint, because scoring subtext makes it on-the-nose.

*Exposition*
22. [R19, P6] If a fact is fired as ammunition, then fire it in a tight shot, hold on the target through and after, cover the shooter wider, drop ambience, let the reply come late, because the fact is learned through the emotion. Exception: confession (rule 3).
23. [R20] If a fact is planted, then one clear, unemphatic insert or single, about 1-2 s, no push-in, music accent or second close-up; plant a critical fact again later instead of lingering.
24. [R21] If a fact can be shown by an object, test or demonstration, then show it and let the line confirm.
25. [R22] If exposition is forced ("as you know"), then move it to an image or prop, or play it off-screen, low in the mix, over action, and flag it, because McKee forgives quick visual telling, not facts shoehorned into dialogue.
26. [Sec. 5] If a question is withheld, then show that a secret exists (hand out of sight, object pocketed), unscored. If a backstory secret breaks at the turn, then tighten toward it, hold before, stop bodies, silence or one sound.

*Conflict levels* (physical, social, personal, private)
27. [R23] If physical conflict dominates, then minimize talk coverage, maximize geography and hazard inserts, POV sparingly, add no dialogue (McKee's quantity rule: more physical/social conflict, less talk).
28. [R24] If the social level is present, then put its sign between the characters (glass, desk, uniform, posted rule), formal symmetrical framing, witnesses in frame; speeches allowed at its peak.
29. [R25, P7] If personal conflict sits in a physical crisis, then one tight two-shot amid wide hazard coverage. Personal conflict generally lives in two-shots, OTS pairs and body distance; singles only when the relationship splits.
30. [R26] If private conflict peaks, then the scene's closest shot, POV, subjective sound; voice-over last.
31. [Sec. 5] If showing surface traits, then use wider, costume-readable frames; save the tightest frames for choices under pressure (true character).

*Cutting and line design*
32. [R27] If a line ends on its core word, then cut to the landing face on that word.
33. [R28] If it front-loads the core word, then cut to the listener early and run the rest as a split edit.
34. [R29] If three or more consecutive lines have five words or fewer, then use fewer cuts (two-shot, deep staging, or held single with the other voice off-screen), because ping-pong hides the turn.
35. [R30] If the turn is one line, then change shot grammar on it (angle, size, camera stops or starts).
36. [R30a] If a line is cut off (ends in a dash), then stay on or cut to the interrupted speaker just after, because the unfinished half is an unsaid.
37. [P9] If every beat looks the same, then revise so size, height, lens or distance progresses toward the turn and changes after (Lumet's *12 Angry Men* plan).
38. [P10] If a line is big, then keep staging small: stillness, held frame, no music swell, because the camera magnifies.

*Speeches, narration, adaptation*
39. [R31] If one uninterrupted line exceeds 40 words (about 15-20 s), then mark each tactic change as a beat and pick speaker or listener per beat, or one take with the listener in frame, because a speech without reaction is the monologue fallacy.
40. [R32] If prose states an unspoken thought, then convert to a held face, carrier, activity or staging before voice-over.
41. [R33] If prose summarizes talk, then dramatize one line and summarize the rest in images (montage without sync sound).
42. [R34] If a novel's best language is narration, then translate its images into design and composition, not lines.
43. [Sec. 5] If a line uses a figure of speech, then do not illustrate it; echo it only through a real object already in the scene.
44. [Sec. 5] If narratized, then decide whom the narrator works on; counterpoint, don't illustrate. If the unsayable is in play, then compose it (mirrors, reflections, frames within frames, recurring shot pattern), never an explanatory insert. If nonrealism, then on-the-nose and frontal iconic framing are allowed.

*Flawed dialogue*
45. [R35] If a line is on-the-nose, then flag it and stage a hidden action (contradicting activity, wider cooler framing, no emphasis).
46. [R36] If melodramatic, then static camera, one size wider than the scene's other beats, no score, flag `melodrama`.
47. [R37] If there is no turning point, then flag `no_turning_point` and do not hide it with busy coverage.
48. [Sec. 5] If beats repeat, then vary size, height, distance and activity; if identical, flag for trimming.
49. [R38] If tempted to rewrite, then flag instead and quote exactly, because rephrasing makes lines more on-the-nose.

*Coverage grammar (file's addition)*
50. [R39] If two characters talk, then record who is screen left/right and which way each looks, because separate shots and AI clips only cohere on one side of the axis.
51. [R40] If singles or OTS shots are paired, then match size, lens and height, eyelines just past the lens on opposite sides; break only as planned progression.
52. [R41] If the relationship flips at the turn, then cross the axis on the turning line with a visible camera move or character cross, not a cut.
53. [R42] If a third character enters or speaks, then one wider re-establishing shot before singles.
54. [R43] If seen through glass, mirror or screen, then record the camera's side and whether the image is mirror-reversed, because AI tools will not track it.
55. [R44] If a character looks into the lens, then it is direct address or deliberate subjectivity; ordinary singles keep eyelines just off lens.

## 3. Breakdown fields

Names come from the file's YAML unless marked *(unnamed)*.

| Level | Field | Meaning | Values / example |
|---|---|---|---|
| scene | `scene_id` | Scene reference | `07` (illustrative) |
| scene / character | `scene_desires` | Each character's one-line want | `IONA: "make Eli admit what he did..."` |
| scene | `value` | Stake and charge change | `"(+ ... collapses to - at the turn)"` |
| scene | `turning_line` | Line where the value turns | `"ELI: You."` |
| scene | `conflict_levels` | Levels with visible sign | `physical`, `social`, `personal`, `private`; `social(glass partition)` |
| scene | `third_thing` | What the conflict routes through | `"security recording on monitor; remote control"` |
| scene | `geography` | Left/right, eyelines, glass/mirror, axis crossing | `"IONA screen left looking right; ... axis not crossed"` |
| beat | `beat`, `line` | Reference; exact source quote | `7.4`; `"IONA: What was it rated for?"` |
| beat | `action` | One gerund | `pressing` |
| beat | `unsaid` | One sentence or "none" | `"She already suspects the answer."` |
| beat / character | `unsayable` | Only with 2+ occurrences in source, both cited | blank by default |
| beat | `core_word` | Meaning-carrying word | `"rated for"` |
| beat | `line_design` | Core-word position | `suspense`, `cumulative`, `balanced`, `parallel` |
| beat | `function` | Line's jobs | `exposition`, `characterization`, `action` |
| beat | `landing_face` / `landing_reason` | Face as line lands; why in ≤5 words | name, `INSERT:<object>`, `WIDE` |
| beat / character | `activity` | Hand task or stillness, and its change at turn | `"Iona holds the remote, thumb still"` |
| beat / prop | `carrier` | What holds the unsaid | `"remote (who controls the recording)"` |
| beat | `pause_after` | `rank`, `size`, `seconds`, `picture`, `sound` | size `short` (<1 s) / `medium` (1-2 s) / `long_hold` (≥3 s); picture `hold`, `push_in`, `cut`, `cut_wide`; sound required |
| beat | `cut_rule` | Cut behavior | `cut_on_core_word`, `cut_early_split`, `hold`, `no_cut_two_shot` |
| beat | `flags` | Labeled notes | `on_the_nose`, `melodrama`, `forced_exposition`, `repetitious_beat`, `no_turning_point`, `splintered`, `monologue`, `override:<reason>`; plus "can play silent" (R18, no label given) |
| beat | `added` | Every choice beyond the source | list |
| beat | fact type *(unnamed)* | Step 3 marking | ammunition / planted / forced / shown by object |
| beat | key line *(unnamed)* | Carries a turn, fired/revealed fact, refusal, interruption, or unanswered question | yes/no |
| prop / motif | carrier log *(unnamed)* | Same framing with one change per return; same prompt wording per clip | red tag; "a small steel flask, the kind that keeps coffee hot" |
| shot (storyboard) | panel labels *(unnamed)* | Gerund + core word; "HOLD 3 s"; "ROOM TONE"; eyeline arrows | per panel |
| previs job | *(unnamed)* | Named carrier objects; body distance per beat; camera height by power | camera low with kneeling Iona, levels as she stands |
| generation job | *(unnamed)* | Speaker attribution, "no dialogue" reactions, room tone, geography, no look to lens | section 6 |

## 4. Procedures

**A. Dialogue pass on one scene** (after beats, value and turn are named):
1. Name each character's scene desire in one line. If impossible, flag "splintered scene?".
2. Label every line: action (one gerund); unsaid (one sentence or "none"); unsayable (only if the same unnoticed behavior, or act against stated aim, appears at least twice in the source, this scene or others, both cited; else blank); core word; function (most lines are action plus one other).
3. Mark each fact: ammunition, planted, forced, or shown by an object.
4. Mark conflict levels and the visible sign of each.
5. Find the turning line; mark pauses before and after; rank all pauses; long holds for one or two at most.
6. Set geography (R39-R44): left/right, eyelines, glass/mirror/screen, axis crossing at the turn.
7. Choose the landing face for each key line (R1-R7, tie-breaks); reason in five words or fewer.
8. Assign activity (task or stillness per character, and its change at the turn) and list every carrier and third thing with insert points.
9. Set `cut_rule` per key line.
10. Set sound and duration for each pause; music only if it does not state the subtext.
11. Check progression toward and after the turn; revise flat framing.
12. Run the flaw screen (flaw table, R35-R38). Flag; do not rewrite.
13. Run the checklist.

**B. Output template (exact):**

```yaml
scene_id: 07
scene_desires:
  IONA: "make Eli admit what he did and why he hid it"
  ELI: "be forgiven without having to say he was wrong"
value: "Iona's case against Eli (+ for her at the start, collapses to - at the turn)"  # one reasonable reading
turning_line: "ELI: You."
conflict_levels: [personal, private, social(glass partition)]
third_thing: "security recording on monitor; remote control"
geography: "IONA screen left looking right; ELI screen right looking left; monitor beyond the glass, behind Eli's shoulder; axis not crossed"  # added: the page does not fix positions
beats:
  - beat: 7.4
    line: "IONA: What was it rated for?"
    action: pressing
    unsaid: "She already suspects the answer."
    unsayable: ""
    core_word: "rated for"
    line_design: suspense
    function: [action, exposition]
    landing_face: ELI
    landing_reason: "he must decide to answer"
    activity: "Iona holds the remote, thumb still"
    carrier: "remote (who controls the recording)"
    pause_after: {rank: 2, size: long_hold, seconds: 3, picture: hold, sound: "room tone, monitor hum"}
    cut_rule: hold
    flags: []
    added: []
```

Mergeable into the pipeline's per-shot format; allowed values in section 3.

**C. Handoff** (file section 11):
- *Storyboards:* draw the landing face, not the speaker; label panels with gerund and core word; draw carriers and third things as the same object on the same side; mark "HOLD 3 s" and "ROOM TONE"; keep sides fixed with eyeline arrows; wordless hand/object/face panels are often the key ones.
- *3D previs:* carriers and third things as named objects; body distance blocked per beat; camera height matching power; holds timed to the pause ranking (unearned holds show as dead time).
- *AI video:* section 6.

## 5. Checklists

**Per dialogue scene** (a "no" means revise or flag):
1. Every line has a gerund, distinct where beats differ. 2. Each character has a scene desire. 3. Turning line identified; value changes there. 4. Landing face with reason for every turn, reveal or refusal line. 5. Landing face is not the speaker at least once. 6. Every important unsaid has a carrier. 7. Each character has activity or stillness, with its change at the turn. 8. Third things kept in frame or inserted at turns. 9. Pauses ranked; at most one or two long holds. 10. Every silence has a sound. 11. Plants readable; fired facts held on the target. 12. Forced exposition flagged or moved to an image. 13. Each conflict level visible in at least one frame. 14. Framing progresses to the turn and changes after. 15. Volleys without ping-pong. 16. Long speeches broken into beats with listener coverage, or listener in frame. 17. No music states the subtext. 18. Metaphors un-illustrated unless a real object matches. 19. Flaws flagged, not rewritten. 20. Choices beyond the source marked `added`. 21. Geography recorded and kept by every pair, except a planned crossing. 22. Script directions about what we see kept unchanged. 23. Every dash-interrupted line has a landing face.

**Common mistakes** (sign → fix): following the speaker (A-B-A-B → landing faces, off-screen lines); illustrating the words (→ insert objects only when handled); emotion labels (→ gerund plus behavior: "*withholding*: looks at the flask, not at her"); unsaid added as speech or voice-over (→ carrier); scoring the subtext; five or more long holds (→ rank); flat progression; over-covered small beats (→ two-shot); listener lost in a speech; third thing missing at the turn; literal metaphors; busy coverage hiding a non-event; misquoted lines; wholesale voice-over in adaptation (→ R32).

No separate per-shot or per-asset checklist; use the handoff lists (4C) and section 6.

## 6. Saying it to AI models

**Verified 2026-09-27 (re-check; features change):** Google's "Ultimate prompting guide for Veo 3.1" (16 Oct 2025): "use quotation marks for specific speech"; separate sound-effect and ambient instructions; 4, 6 or 8 s clips; "timestamp prompting" for timed multi-shot sequences in one generation. Gemini API Veo 3.1 page (Jan 2026): quoted speech with a described speaker ("'This must be the key,' he murmured"); 8 s required with reference images or extensions; up to three reference images "of a single person, character, or product"; extension in 7 s steps. The Vertex AI guide did not render and is not relied on.

**File's recommendations:**
- At 2-3 words per second, an 8 s clip holds at most 16-24 words, fewer with a pause; default one beat per clip.
- Generate reactions as their own clips, stating "she listens; no dialogue".
- Describe subtext as behavior ("he looks down at the flask and does not answer"), never "he is secretly guilty"; emotion labels invite generic acting.
- Write silence into audio: room tone, one single sound, stillness duration; otherwise models fill gaps with speech or music.
- Describe each carrier in identical words every clip.
- Attribute every quote to a described character in the same sentence ("the kneeling woman says, '...'").
- Prefer the speaker off-screen on the listener's clip, audio laid in as a split edit; this avoids lip-sync, among the least reliable model skills.
- Put left/right placement and eyeline in every prompt; check for mirrored compositions that cross the axis.
- For ordinary singles, say the character does not look into the camera.

## 7. The Catch

Quotes are from the 25 September 2026 workshop revision. The file uses no canonical scene numbers (see section 8).

- **Opening, loading tunnel.** Red tag = carrier: opening insert, framed identically when it returns. Fingertip in the bolt hole ("Still sharp") carries the unsaid. "One breath" + "The safety brakes are gone" in one deep frame (Iona low foreground profile, Jude's hands on the wire above); "He stops unwinding" is the in-shot reaction; room tone, no music. Volley in one angle; the only cut is closer on Iona for "Not when I last saw him". Ladder look becomes a tilt planting ladder and yellow band. Frame levels when Iona rises. Jude on one side in all set-ups. "I know how a lift works" / "I know you know": one tight equal-height two-shot. Jude re-hooking the tag: unhurried insert, action left open. Plant: "Stop it hard..." pays off at STOP.
- **The car.** Eli held still in profile against mirrored signs, intercut with Iona's hands on the wheel; the red light times the pause; Iona's question lands on Eli in the rear-view mirror, his eyes leaving the mirror as he looks at the flask (flask below the mirror: a secret exists, unrevealed); cut on "Drive." to the car moving, engine and indicator, no score.
- **Motif: the car question** returns in the recording scene (fired at Eli), on the ship (roles reversed, "I don't know"), and in quarantine ("In the car-" / "Yes.", interrupted line). Stage each through a frame within a frame (mirror, ship glass, quarantine glass), changing who is framed **(added)**.
- **The recording (quarantine).** Third thing: recording and remote (pause = *seizing control*; run = *releasing*; Jude's switch-off = *ending it, protecting both*). Monitor on Saye's side facing the glass, in most backgrounds. Iona turns past a soft Jude to Eli. Clean insert of Saye's finger stroking down, then sideways off the screen. "What was it rated for?" / "She waits": OTS on Eli, no cut, room tone plus monitor hum. "One body." / "One." / "You.": stay on Iona, Eli off-screen, mark "You." by a cut-in or camera stop. "Silence.": cut wide once, hold. Saye's "No. It is not.": one short readable reaction (plant for Nell). "Nothing in it." recorded as unsaid; palm in foreground racking to Eli watching. **(Added option):** monitor goes black, three reflections.
- **The mint (kitchen).** Symmetrical two-shot across the table as mirror; leaf insert; Eli's bottle cap and Saye watching in one deep frame; hold on Iona chewing, cut on "Not mint." to Saye; no music.
- **Carriers/motifs:** red tag, bolt holes, ladder and yellow band, steel flask, remote and monitor, Iona's skinned palm, mirror/frame within a frame, the car question, mint, bottle cap, paired wedding rings (last scene).
- **The Long Places (prose test):** volume as third thing, landing on Nilay reading the margin; Halden's two identical desk-wipe inserts qualify as `unsayable`; no voice-over for Nilay; "question as a lamp" logged as motif, words saved for Chapter XIV; mother closing the oven door on her line **(added)**.
- **For the writer/user to decide:** binding versus advisory script directions; unsayable bar (two occurrences vs two scenes); tuning pause durations and the 40-word threshold; the added geography; Eli's side of the glass (unstated); the tag action (left open); the added options above; all flaw and "can play silent" flags.

## 8. Conflicts and open questions

- **Scene numbering.** A1's template labels the recording scene `07`, beat `7.4`; A2, A3 and A4 call it sc13 ("GLASS PARTITION"), and A3's scene 7 is another scene. Treat A1's numbers as illustrative.
- **Turning point of sc13.** A1 names "ELI: You." A2 scores that exchange as B10 (confession) and puts TP1 at B7, TP2 at B12 ("Nothing in it") and the main turn at B15 ("I asked you in the car..."), with a push-in on Iona there. Reconcile with A1's change-of-shot at "You." and the one-push-in limit (which B1 shares).
- **sc13 geography.** A1 (added) and A2: Iona screen left looking right, Eli right looking left. A3's coverage map: Iona looking frame-left, Eli frame-right. Pick one.
- **Words per clip.** A1: 16-24 per 8 s (2-3 words/s). A4 and C3: 2.5 words/s with margins, about 15-18. A1 is looser.
- **Veo limits.** C1/C3 add that 1080p/4K also force 8 s and Lite-tier limits; A1's facts are dated and need re-checking.
- **File defaults, not McKee:** pause durations, 40-word threshold, one push-in, two-occurrence unsayable bar, R39-R44.
- **Kuleshov effect:** real but modest (replications mixed; papers not re-read); a neutral face cannot carry a turn by editing alone.
- **Beat analysis** (McKee Part Four) is out of scope; the procedure assumes A2. Rules are defaults ("forms, not formulae").

## 9. Section map

- **Box:** purpose, input/output, reading order. **1. Why this file exists:** dialogue as action; three questions per line. **2. Terms:** dialogue, camera, sound and editing glossaries.
- **3. McKee's working ideas:** 3.1 definition, narratized/indirect dialogue; 3.2 exposition, characterization, kinds of action; 3.3 said/unsaid/unsayable, action vs activity, subtext; 3.4 conflict levels, quantity rule, media; 3.5 line design, economy, pause, silence; 3.6 six tasks; 3.7 flaw table with fixes.
- **4. Principles P1-P10:** incl. pause-duration table and picture-choice rules (P5), Lumet progression (P9).
- **5. Translation table:** about 30 rows, story meaning to camera, blocking, sound.
- **6. Decision rules:** application, precedence, tie-breaks; R1-R44 in nine groups (6.1-6.9).
- **7. Procedure:** 13 steps, YAML template, allowed values.
- **8. Checklist:** 23 questions.
- **9. Common mistakes:** 14 rows.
- **10. Worked examples:** tunnel, car, recording, mint (*The Catch*); Register and bread oven (*The Long Places*).
- **11. Handoff:** storyboards, previs, AI video (verified Veo facts, recommendations).
- **12. Open questions.**
- **Sources:** McKee; works he cites; film-craft books; Kuleshov studies; Veo pages.
