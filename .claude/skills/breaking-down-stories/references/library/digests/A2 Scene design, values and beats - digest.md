# Digest A2: McKee scene design, values, beats, turning points

Source: `research/A2_mckee_scene_design_and_beats.md` (710 lines). Bracket refs: R# is a file rule, P# a principle, S# a method step, § a section.

## 1. Scope

1. How to break any scene (screenplay or prose) into values, desires, beats and turning points, using McKee's *Dialogue* (2016), Parts Three and Four.
2. How to turn that analysis into shots: which beats earn a camera setup, which shots must exist, how long to hold, where to cut. Includes a 1–5 intensity scale, 31 rules, a YAML template, a checklist, and worked examples (*The Catch* sc10 and sc13; *The Long Places* ch. III).
3. It sits upstream of the lens, light, framing and prompt files. They decide how a shot looks; this file decides which shots exist, and why.

## 2. Rules

A "then consider" rule is a default: override it only with a one-line reason in the breakdown. A plain "then" rule is firm. When defaults clash, turning-point rules beat conflict-type rules, and both beat general beat rules [§7].

**Vocabulary and analysis**

1. [§2] If you write pipeline text, then use only these terms, because every rule depends on them:
   - **value**: a quality of a character's life with a + and a − pole
   - **charge**: from −−− to +++, "+/−" for mixed, qualifier allowed ("+ (uneasy)")
   - **core value**: the value the story turns on
   - **scene**: continuous time and place in which at least one value changes charge
   - **scene intention**: what the character wants right now
   - **background desires**: what the character will not risk
   - **tactic**: an action on someone; a new tactic starts a new beat
   - **beat**: an action plus the reaction it provokes; not a pause
   - **turning point (TP)**: the beat where a value swings to its closing charge, by action or revelation
   - **movement**: a scene part with its own TP
   - **scene driver**: starts most beats; may not control the outcome
   - **third thing**: an object the characters talk through
   - **plant/payoff** and **context**: McKee's "setup", renamed to keep *setup* for the camera
   - **camera setup**: one position, one lens; at least one generation in AI video
   - **key shot**: the frame showing a value turn, one per turn
   - **must-keep shot**: a shot a later key shot depends on; never cut it for budget
2. [P1] If you build a shot list, then work from beats, never lines, because a line-by-line list gives "ping-pong" coverage of who talks rather than what happens.
3. [S0] If the source is a screenplay, then each slugline is a scene boundary by default. CONTINUOUS headings may merge. A slugline holding two value arcs (with a time jump or a change of who is present) is split and flagged. IDs keep the script's slugline count, so they match the source.
4. [S0] If the source is prose, then tag each passage:
   - *dramatized*: full beats
   - *narratized*: montage, voice-over or a compressed scene; say which
   - *inner*: needs a visible carrier
5. [S0] If a script writes "(beat)", then treat it as a pause of about 1 s, not a beat.
6. [S2–S3] If every value opens and closes at the same charge, then write `FLAG: possible nonevent`. If scene intentions never cross, then write `FLAG: splintered (parallel desires)`. Flag these; never fix them.
7. [S3] If granting a scene intention would not end the scene, then the intention is wrong.
8. [S5.4, P9] If adjacent units share a tactic and the later one does not top the earlier (no rise in risk, target or specificity), then merge them. If each repeat escalates, then keep separate beats, because escalation is not repetition.
9. [S5.6] If a dialogue scene has fewer than 3 beats per page, then look for merged tactics or dropped nonverbal beats. If it has more than 10, then look for over-splitting. Scale: 1 page ≈ 1 minute; McKee's cases run 8–16 beats, about 14 s per beat. Action pages may run denser.
10. [S6] If you score intensity, then:
    - score relative to the scene
    - allow at most two 5s per movement; keep 5 for the main TP (or the latest turn) and the turn nearest it, and score other turns 4
    - let intensity mostly rise, with planned drops and a post-TP resolution allowed
    - accept a ±1 disagreement
11. [S7.5–6] Timing faults:
    - If the main turn is at B1 or B2, followed by 3+ beats with no further turn, then flag *TP too soon*.
    - If 3+ consecutive beats before the turn repeat an untopped tactic, then flag *TP too late*.
    - Compensate only by compressing beats in the shot plan, never by inventing events, because the pipeline translates and does not rewrite.
12. [P10, S8] If a beat is a TP or scores 4+, then give step 2 (seeing the obstacle) and step 3 (choosing) their own screen time, a look or a held half-second, before the action. On routine beats, all five steps sit inside one shot.

**Beats to shots**

13. [R1] If a new beat starts, then consider changing the image (a new setup or size, a camera move, an actor's move), because the audience reads a new tactic from a new picture.
14. [R2] If a tactic repeats untopped, then consider holding one setup, because a new image signals false progress. If the repeats escalate, then give each topper its own cut or reframe on the punch word.
15. [R3] If a beat is nonverbal, then consider a shot in full view, because line-based lists drop it.
16. [R4] If a beat is the main TP, then consider the scene's tightest size, or a deliberate wide when the change is about isolation, waiting or geography, because the TP must look unlike its surroundings. Other turns get their movement's tightest size. Never spend the scene's tightest size before the main turn.
17. [R5] If a beat's meaning lands in the reaction, then consider holding on the reactor, because the reaction ends the beat, and Murch ranks emotion (51%) above story (23%).
18. [R6] If a beat runs action/reaction/reaction as closeness rises, then consider a two-shot. If the same pattern breaks the relationship, then use singles.
19. [R7] If several people react at once, then consider one frame holding all of them, because singles cannot show simultaneity.
20. [§5, P3, P6] Conventions:
    - Positive relationship charge at the opening: a shared frame. Negative: singles, a barrier, bodies angled away.
    - Rising intensity: tighter, shorter shots, or one slow push-in.
    - A breather: wider, warmer.
    - Attack gerunds: toward, lean in, stand. Retreat gerunds: away, lower, step aside.
    - The scene intention becomes the blocking goal.
    - Subtext: show the hiding behavior.
    - Status: camera height, as a convention only.
    - Antagonism level: physical needs the environment in frame; social, institutional things; personal, the other face; inner, close-ups, reflections and silence.
    - The closer the relationship, the more the image carries.
21. [P2, §5] If a character is in control (long sentences), then consider longer takes. If a character is losing control (short phrases), then consider shorter, tighter shots cut on their lines. If a character breaks their own speech pattern, then consider changing the framing.

**Turning points**

22. [R8] If the TP is a revelation, then consider an insert of the evidence plus a held close-up of the receiver.
23. [R9] If the TP is an action, then consider one uncut frame showing the action and its result, because a cut hides the change.
24. [R10] If a new movement starts after a drop, then consider returning to wide, ideally from a new angle, because the new rise needs room. A drop is a silence, a pause, a change of subject, or a first beat at least 2 points below the turn. If there is no drop, then do not widen, because widening releases the pressure.
25. [R11] If power changes hands at the TP, then consider moving the camera to the new driver's side of the line, or changing its height. Cross the line only with an on-screen move or a neutral shot down the line, because a bare cut flips screen direction.

**Conflict type** (the file's derivations, not McKee's)

26. [R12–R17] If the conflict is:
    - **balanced**: matched coverage (same lens and size on both sides), tightening in step; break the match only at the TP
    - **asymmetric**: the attacker moves; the resister stays still, anchored in an activity, with her closest shot saved for her turning line
    - **indirect**: group shots keeping the witnesses in frame, plus inserts of the damaging objects
    - **comic**: wide frames holding both bodies; cut on the punch word, then hold; no sympathy close-ups
    - **minimal**: long takes, few cuts, two-shots, every pause kept
    - **reflexive**: voice-over, reflections, a setting drawn as the character feels it; cut faster while fear speaks

**Silence, objects, prose, generation**

27. [R18] If silence or waiting is a tactic, then consider holding on the person waited on, with no cutaway and no music bed, because the length of the silence is the action.
28. [R19] If the scene talks through a third thing, then consider inserts of it and staging around it. Eyelines leaving it for the other person mark escalation.
29. [R20] If a detail is a plant, then consider framing its payoff the same way (size, angle, lens, side of frame), because matching frames link the two unaided.
30. [R21] If background desires restrain a character, then consider keeping the restraint (witnesses, a sealed door) in frame at peak pressure.
31. [R22] If the prose is narratized, then consider a long take on the teller's face rather than a flashback. Flash back only when the past events are the TP.
32. [R23] If the prose gives inner thought, then consider a physical correlate (gesture, object, setting) before voice-over.
33. [R24–R27] If you generate shots, then:
    - split over-long clips at beat boundaries
    - replace emotion words with behavior
    - write opposite eyelines into separately generated singles (firm)
    - play listener-carried lines off screen (J-cut or L-cut)


**Cuts and the whole film**

34. [R28] If a beat ends, then cut at the end of the reaction, not during it, because a thought completes there (Murch's blink).
35. [R29] If a scene opens in a new place, then use its first one or two shots to show who is where (a wide, or a POV then a wide), unless disorientation is the value at stake.
36. [R30] If a scene's closing charge contrasts with the next scene's opening, then consider a hard cut. If the scenes share an object, shape or sound, then consider a match cut or sound bridge. The script's own transition wins.
37. [R31] If you plan a whole film, then list each scene's main key shot and make them escalate within each act. Do not spend the film's tightest size or longest hold before the climax.
38. [S9–S10] If you plan shots, then write the staging line first and plan key shots first (main TP first), and make one frame per key shot even without storyboards, because that frame is the scene's contract.

## 3. Breakdown fields

Fields come from the §8 template unless marked *(not in template)*. (opt) = optional.

| Level | Field | Plain meaning | Allowed values / example |
|---|---|---|---|
| scene | `id`, `heading`, `story_position` | ID from slugline count; slugline or prose chapter + first words; act/sequence and what came before | `sc10`; `INT. SAYE'S HOUSE - KITCHEN - BEFORE DAWN` |
| scene | `source_kind` | Passage kind | screenplay \| prose-dramatized \| prose-narratized \| prose-inner |
| scene | `staging` | One line placing everyone | "Seen from the monitor, left to right: Iona, Jude, Eli" (+ "staging assumed") |
| scene | `context.audience_knows`, `.changed_since_last_meeting` | Entering knowledge; change since last meeting | one line each |
| scene / motif | `context.pays_off`, `context.plants` | Plants and payoffs across scenes, by scene ID | `[flask hold, sc10]` |
| scene | `values[]`: `name`, `core`, `open`, `close`, `turns_at`, `turn_kind` | A two-pole value in a life, with its charges and its turn | "Trust / Betrayal (Iona toward Eli)"; true \| false; −−− .. +++ or +/−; B# \| none; action \| revelation \| none |
| scene | `movements[]`: `id`, `beats`, `turn`, `starts` | Parts of the scene with their own turn | M1; B1-B8; TP# \| none; scene start \| after a drop \| without a drop |
| scene | `scene_driver`, `controls_outcome` (opt) | Who makes the scene happen; who holds power, if different | names |
| scene | `antagonism.physical/.social/.personal/.inner/.witnesses` (opt) | What blocks desire, level by level | free text |
| scene | `conflict_type.main`, `.undercurrent` (opt) | The quality of conflict | balanced \| comic \| asymmetric \| indirect \| reflexive \| minimal |
| scene / prop | `third_thing` (opt) | The object talked through | "the security recording" |
| scene | `flags` | Faults, flagged but never fixed | nonevent \| splintered \| TP too soon \| TP too late \| continuity \| ... |
| scene | `handoff.storyboard/.previs/.prompts` | Optional jobs downstream | key shots only \| all \| none; yes \| no; yes \| no |
| character | `object_of_desire`, `super_intention` | Copied from the story-level file | free text |
| character | `scene_intention`, `hidden_scene_intention` (opt) | What the character wants now | "to make Eli tell her himself" |
| character | `background_desires`, `motivation` (opt) | Restraints; the reason behind the want | free text |
| character | `tactics` | Action gerunds, beat by beat | `[B8: accusing, ...]` |
| character | `speech_profile`: `sentence_length`, `contractions`, `vocabulary_field`, `modal_habit` (opt), `voice` (opt) | Speech read as a camera and design brief | short \| mixed \| long; yes \| no \| breaks pattern at B#; trade/world; must/should/could; active \| passive |
| character | `reveals` (opt) | What the TP choice shows (feeds character design) | free text |
| beat | `id`, `text` | Number; exact quote or action line | B1 |
| beat | `action`, `reaction`, `reaction_2` (opt) | Name + gerund | "Saye proving / Iona discovering" |
| beat | `charges_after` | Each value's charge after the beat | `{A: −−, B: +}` |
| beat | `intensity`, `tp` | Pressure score; turn marker | 1–5; none \| TP# \| TP# (main) |
| beat | `five_steps` | Required when intensity ≥ 4; each step tied to something visible | desire / antagonism / choice / action / expression |
| shot | `id`, `size` | Shot ID; shot size | `sc10.B1.a`; wide \| medium \| medium close-up \| close-up \| big close-up \| insert |
| shot | `people`, `angle_height` | Who is framed; camera height | single \| two-shot \| three-shot \| over-the-shoulder \| none; eye-level \| low \| high \| overhead \| POV of NAME |
| shot | `movement`, `lens` | Camera move; lens placeholder | static \| pan \| push-in \| handheld \| ...; wider \| normal \| longer |
| shot | `in_frame`, `eyeline`, `dialogue` | Content; look direction; where the line plays | frame-left \| frame-right \| lens \| down \| at OBJECT; none \| on screen \| off screen over this shot |
| shot | `behavior`, `duration_s`, `shot_role` | Observable action from the gerund; estimated seconds; priority | "stops chewing; eyes go to Saye; swallows"; key \| must-keep \| normal |
| previs job | camera setup list *(not in template; used in sc13)* | Named positions reused across shots; one setup = one camera object; beats = timeline markers | S1 monitor's view … S8 three-shot |
| film | main key shot list *(not in template; R31)* | Each scene's main key shot, escalating within each act | list |
| motif | recurring thread *(via plants/pays_off, §13)* | Every occurrence gets a related composition | "all right?" thread, always behind a barrier |
| generation job | one shot = one generation *(S10)* | Prompt carries the eyeline and the behavior | R24–R27 |

## 4. Procedures

**Scene breakdown, Steps 0–10.** Run in order; each step writes into the template.

0. **Find the scene** (rules 3–5).
1. **Context.** Three lines: what the audience knows; what has changed since these characters last met; the plants this scene pays off and the ones it lays.
2. **Values.** List 1–3 pairs, named in a character's life (never "family"). Mark the core value. Score the opening and closing charge (rule 6).
3. **Desire.** Fill the `characters` block for everyone on screen; write scene intentions as "to [verb] [someone/something]" and tactics after Step 5. Name the driver and `controls_outcome` (rules 6–7).
4. **Antagonism and conflict type.** List forces by level, plus witnesses. Name the main type and any undercurrent.
5. **Beats.**
   1. List every speech and action, quoted exactly.
   2. Give each a gerund. An action gerund is transitive and playable. A reaction gerund may be intransitive ("Recoiling in terror") but must be playable.
   3. Pair each action with its reaction. The reaction can be a line, a silence, a look, a move, the actor's own afterthought, or the world ("Iona hits STOP / the cage stops dead"). A second reaction is allowed.
   4. Merge by rule 8, asking of each line whether it is an action or a reaction.
   5. Name each beat `Action / Reaction` and number it B1, B2, and so on.
   6. Check the count (rule 9).

   Swap weak gerunds for strong ones:
   - talking → accusing / confessing / warning
   - asking → probing / pleading / testing / cornering / daring
   - answering → parrying / deflecting / minimizing / conceding / stonewalling
   - explaining → justifying / reassuring / excusing / selling
   - looking → clocking / appraising / studying / avoiding / witnessing
   - feeling → absorbing / doubting / recoiling / bracing
   - being quiet → outwaiting / withholding / freezing out / refusing
6. **Score** (after Step 7). Write each value's charge after every beat. The first true row sets the intensity and its default shot size; then apply rule 10.

   | Intensity | The beat contains | Default size |
   |---|---|---|
   | 5 | A value turn | Tightest in the scene, or a deliberate wide |
   | 4 | An open accusation; a forbidding, threat or ultimatum; a confession; a disclosure that damages someone present; a move that blocks, threatens or shields | Close-up |
   | 3 | A direct challenge or unwelcome question; a test; an open refusal; catching someone in a slip; a value named as at risk | Medium or medium close-up |
   | 2 | Probing, hinting or noticing (stakes unnamed); a breather; resolution | Wide or medium |
   | 1 | Logistics or pleasantries | Wide |

7. **Find the turning point.**
   1. Run the sign test on each value:
      - If the sign changes (a mixed charge counts), the turn is the first beat after which the value stays on its closing side.
      - If the sign holds, the turn is the first beat where it reaches its closing charge and stays there.
      - If it opens and closes the same, write `turns_at: none`.
   2. Number the turns TP1, TP2… in beat order. The core value's turn gets `(main)`.
   3. Label each turn as action or revelation.
   4. Mark movements. A new one starts when the beat after a turn pursues a new goal. Record whether it starts after a drop or without one.
   5. Check the timing (rule 11).
8. **Five steps**, for each TP and each beat of intensity 4 or more:
   - desire: the eyeline, or the object reached for
   - antagonism: a look, a reaction shot or a POV
   - choice: a held half-second
   - action: the move or the line
   - expression: the exact words or gesture
9. **Shots.** Write the staging line first, marking "staging assumed" if the source doesn't fix it. Fill in the template's shot fields; use wider/normal/longer for lens if no lens file is available. Plan key shots first.

   Default durations (measured times from a table read replace them):
   - Spoken line: words ÷ 2.5 + 0.5 s.
   - Small act: 1–2 s. Whole-body move: 2–4 s.
   - "(beat)": about 1 s. "Silence." or "She waits.": 2–3 s. "A long moment": 3–4 s.
   - A reaction that lands a TP: at least 2 s.
10. **Hand-off** (optional; the breakdown is the deliverable). Storyboard: at least one frame per key shot. Blender previs: setups blocked on a floor plan, one camera object each, beats as timeline markers. Prompts: see section 6.

**Threads across scenes [§13].** When a line or gesture recurs, record every occurrence under `plants`/`pays_off` and give them related compositions.

**Template [§8]**, reproduced exactly. Every field is required unless its placeholder contains `(opt)`.

```yaml
scene:
  id: <e.g. sc10>
  heading: <slugline, or prose chapter + first words of the passage>
  source_kind: <screenplay | prose-dramatized | prose-narratized | prose-inner>
  story_position: <what act/sequence; what came just before>
  staging: <one line placing everyone in the room; add "staging assumed" if the source does not fix it>
context:
  audience_knows: <one line>
  changed_since_last_meeting: <one line>
  pays_off: [<earlier plant + its scene ID>, ...]
  plants: [<new plant, and the scene where it pays off if known>, ...]
values:
  - name: <Positive / Negative (whose life)>
    core: <true | false>
    open: <--- .. +++, or +/->
    close: <--- .. +++, or +/->
    turns_at: <B# | none>
    turn_kind: <action | revelation | none>
movements:
  - id: <M1>
    beats: <B1-B#>
    turn: <TP# or none>
    starts: <scene start | after a drop | without a drop>
characters:
  - name: <name>
    object_of_desire: <from story file>
    super_intention: <from story file>
    scene_intention: <to VERB someone/something>
    hidden_scene_intention: <(opt)>
    background_desires: <what they will not do or say here>
    motivation: <(opt)>
    tactics: [<B#: gerund>, ...]
    speech_profile:
      sentence_length: <short | mixed | long>
      contractions: <yes | no | breaks pattern at B#>
      vocabulary_field: <the trade or world her nouns and verbs come from>
      modal_habit: <(opt) must / should / could / would ...>
      voice: <(opt) active | passive>
    reveals: <(opt) what the choice at the turning point shows about this character>
scene_driver: <name>
controls_outcome: <(opt) name, if different from the driver>
antagonism:
  physical: <(opt)>
  social: <(opt)>
  personal: <(opt)>
  inner: <(opt)>
  witnesses: <(opt)>
conflict_type:
  main: <balanced | comic | asymmetric | indirect | reflexive | minimal>
  undercurrent: <(opt)>
third_thing: <(opt) object or subject they talk through>
beats:
  - id: B1
    text: <exact quote(s) or action line(s)>
    action: <Name + gerund>
    reaction: <Name + gerund>
    reaction_2: <(opt)>
    charges_after: {<value name>: <charge>, ...}
    intensity: <1-5, from the decision list in Step 6>
    tp: <none | TP# | TP# (main)>
    five_steps: <(required if intensity >= 4) desire / antagonism / choice / action / expression, each tied to a visible moment>
    shots:
      - id: <sc10.B1.a>
        size: <wide | medium | medium close-up | close-up | big close-up | insert>
        people: <single | two-shot | three-shot | over-the-shoulder | none>
        angle_height: <eye-level | low | high | overhead | POV of NAME>
        movement: <static | pan | push-in | handheld | ...>
        lens: <wider | normal | longer>
        in_frame: <who/what>
        eyeline: <frame-left | frame-right | lens | down | at OBJECT>
        dialogue: <none | on screen | off screen over this shot>
        behavior: <observable action from the gerund>
        duration_s: <estimate, from the defaults in Step 9>
        shot_role: <key | must-keep | normal>
flags: [<nonevent | splintered | TP too soon | TP too late | continuity | ...>]
handoff:
  storyboard: <key shots only | all | none>
  previs: <yes | no>
  prompts: <yes | no>
```

## 5. Checklists

**Per scene [§9].** Answer yes or no; every "no" needs a fix or a written reason.

1. Every value has + and − poles, named in a character's life.
2. At least one value's closing charge differs from its opening charge.
3. The main TP is one numbered beat, labeled action or revelation, and every `turns_at` passes the sign test.
4. The driver is named, and each scene intention passes the test "if granted, the scene ends".
5. Background desires are listed for everyone who holds back.
6. Every gerund is transitive (actions) and playable, with no talking, asking, saying or looking. Where two beats share a gerund, the later one tops it or draws a different reaction.
7. Nonverbal beats are included; "(beat)" markers are not.
8. Intensities come from the Step 6 list: at most two 5s per movement, rising overall, and every drop explained.
9. There is exactly one key shot per value turn, with the main one planned first.
10. Every beat change changes the screen, and every held tactic holds the image.
11. The tightest size is saved for the main TP, or the wide used there is explained.
12. Each TP, and each beat at intensity 4 or more, has its five steps written and made visible.
13. Plants and payoffs are cross-referenced by scene ID, with matching compositions.
14. Any third thing has inserts and serves as the staging axis.
15. Shot behaviors describe observable action, not emotion labels.
16. Every prose passage is tagged, with a treatment chosen.
17. Continuity problems (hands, props, eyelines, screen direction) are flagged, not silently fixed.
18. There is a staging line, and singles of two people facing each other have opposite eyelines.
19. Durations use the defaults, and every TP reaction holds at least 2 s.

**Common mistakes [§10]** not already covered by the rules:
- Taking the loudest moment for the TP. The TP is often quiet ("I wasn't asking her."), so rerun the sign test.
- Naming values as topics ("medicine").
- Using the super-intention as the scene intention.
- Charges that contradict the TP.
- Invented dialogue for narratized prose.
- Every line lip-synced on screen.

The file has no separate per-shot or per-asset checklist. Items 9–11, 15, 18 and 19 are the checks that apply to shots.

## 6. Saying it to AI models

- **Budget.** One shot = one generation; each setup costs at least one. Spend references, retries and resolution on key shots first.
- **Behavior, not emotion [R25].**
  - Works: "Iona stops chewing; her eyes go to Saye; she swallows."
  - Fails: "Iona feels horror." It gets a stock face.
  - Name where the eyes go, what the hands do, what stops. For the mint in *The Catch*, write "she stops chewing, frowns, chews once more, slowly", never "disgusted". The beat is recognition and confusion.
- **Eyelines [R26, firm].** Each generation knows nothing of the others. Write the frame-left or frame-right eyeline from the staging line into each single, opposite each other; same-direction looks read as two people not talking.
- **Lip-sync [R27].** Play lines the listener carries off screen. Even speech-syncing models vary most on mouths.
- **Clip length [R24].** Split an over-long take at a beat boundary (in prose, at a sentence end where the eyes move), with matched framing. Never split mid-beat. Current clip limits are not recorded here; the prompt file must supply them [§15].

## 7. The Catch

Scene IDs count the 30 sluglines of the 25 September 2026 workshop revision.

**sc10, the kitchen**
- **Values.** A, Normal / Altered (core): + to −−−, turning at B7 (TP1, main, revelation). B, Free / Contained: + to −−, turning at B11 (TP2, action). C, Trust in Eli: + to "+ (cracked)", with no turn; the crack is planted at B6.
- **Structure.** M1 B1–B8; M2 B9–B11, after a drop. Saye drives; asymmetric, indirect undercurrent. Intensities 2 2 3 3 3 4 5 4 3 4 5.
- **Key shots.**
  - B7.b: Iona's close-up, the tightest size in the scene, held from the first chew through "Not mint." and on through B8, with Saye off screen.
  - B11.a: the wide held through the wait; B11.b (Saye, medium, "Nobody leave this room.") closes on the scripted hard cut to black.
- **Must-keep shots.** B1.a, Saye's POV pan to the flask (3–4 s). B2.a, a wide that plants the mint; Iona's lamp is the key light. B4.b and B4.c, the mirrored ring inserts.
- B4.a: profile two-shot, longer lens, "like a woman and her reflection". Totals: 11 beats, 19 shots, about 16 setups. Mint logic: (R)-carvone is spearmint; its mirror, (S)-carvone, smells of caraway.

**sc13, "You did that"**
- **Values.** A, Truth / Concealment: − to +++, turning at B7 (TP1). B, Trust / Betrayal (core): "+ (uneasy)" to −−, turning at B15 (TP3, main). C, Innocent / Culpable: + to −−, turning at B12 (TP2). All three turns are revelations.
- **Structure.** M2 starts without a drop, so no reset to wide. Iona drives; balanced conflict, minimal delivery, reflexive layer; the recording is the third thing.
- **Staging** (assumed). From the monitor: Iona, Jude, Eli. Iona looks frame-right, Eli frame-left. Eli watches the screen until B14.
- **Setups.** S1 monitor's view (master); S2 reverse; S3 footage (the only high angle); S4/S5 matched singles; S6 Saye through the glass; S7 inserts; S8 three-shot.
- **Key shots.** B7; B12, whose palm insert rhymes with sc6; and B15, a push-in to a big close-up played in singles.
- **Must-keep.** B6 (no dialogue, but it explains B12); B14 (Eli's head turn).
- **Plants and transitions.** B11 plants Nell (sc17). B16 is a three-shot for the shared flinch; its black screen may match-cut to the tablet in sc14.
- **Totals.** 16 beats, about 31 shots, 8 setups.

**The thread "Are we going to be all right?"**
- It runs sc9 (asked into the rear-view mirror), sc13 B15 (payoff), sc23 (roles reversed, through the glass wall) and sc29 ("In the car-" / "Yes.", a two-shot through the glass, with the pause kept).
- Every occurrence keeps a barrier between the siblings.
- The ring inserts in sc10.B4 match the hands through the glass in sc29, in lens and angle.

**Speech briefs**
- Saye uses no contractions: composed frames. Her one contraction (sc24) earns a change of framing.
- Eli talks in counts: frame him toward objects and screens.
- Iona gives commands: frame her hands.

***The Long Places*, ch. III.** Concealed / Disclosed runs − to ++. The key shot is the night table without the camera. No flashback: one long take on Márton.

**Flagged or left open for the writer/user**
- Which hand holds Iona's lamp in sc10 B4, or whether she sets it down at B3.
- Both staging lines are assumed; if either changes, re-derive the eyelines.
- Whether to use the sc13 to sc14 match cut.
- The Jude/Iona marriage is only implied, by the rings (noted, not decided).
- The hand-off jobs for each scene.

## 8. Conflicts and open questions

- **Intensity is a pipeline invention**, calibrated only on the two *Catch* scenes. Test it on *The Long Places*. Readers may differ by ±1.
- **Beat boundaries are judgment calls.** McKee calls his breakdowns "after-the-fact analyses". The merge and nonverbal checks matter more than the count.
- **All screen treatments and all 31 rules are the file's own derivations.** McKee does not prescribe coverage.
- **Duration defaults are rough.** Weighted delivery (Márton, Saye) runs slower than 2.5 words a second; comic delivery runs faster.
- **Charges for the audience versus the character** should both be recorded when they differ, but the template has no field for the audience's charge.
- **The scale is capped at +++**, but McKee himself writes "++++" (LOST IN TRANSLATION).
- **Boundaries with other files:**
  - Step 6's default sizes and digest rules 20, 21 and 26 reach into B1 and B3. The file says those files decide the look.
  - Digest rules 34–36 (R28–R30: cut points, transitions) overlap A4.
  - `lens` is a placeholder until the lens file applies.
  - Clip limits must come from C1 and C3.
  - `reveals` feeds B5.
  - The slugline split and merge rules should be squared with A3.
- **"Setup" means camera setup only.** Other files must not use the word for plant or context.
- **Unverified sources:**
  - Murch's percentages
  - the five-step method in *Story*
  - Weston, Katz, Arijon and Stanislavski, all cited from general knowledge
  - Mamet, via a secondary summary
  - the "beat" from "bit" etymology

## 9. Section map

- **Header box.** Purpose, and the file's place upstream of the look files.
- **§1 The idea.** Dialogue is frosting; work from the inside out.
- **§2 Vocabulary.** The fixed terms, plus one-line camera and editing definitions.
- **§3 Principles P1–P13.** Each principle with its screen consequence.
- **§4 Six conflict types.** Case studies, beat signatures and derived treatments.
- **§5 Translation table.** Story meanings mapped to screen choices.
- **§6 Method, Steps 0–10.** The gerund table, intensity list, sign test and duration defaults.
- **§7 Decision rules 1–31.**
- **§8 YAML template.**
- **§9 Checklist.** 19 checks.
- **§10 Common mistakes.** How to spot each one, and the fix.
- **§11 Example A.** sc10, with the beat table, the five steps at B7, the shot plan and the continuity flag.
- **§12 Example B.** sc13, with setups S1–S8 and the shot plan.
- **§13 Example C.** The question that travels across four scenes.
- **§14 Example D.** *The Long Places* ch. III: narratized prose.
- **§15 Limits and open points.**
- **Sources.** *Dialogue* (read in full), *Story*, film-craft texts, web-checked facts, test texts.
