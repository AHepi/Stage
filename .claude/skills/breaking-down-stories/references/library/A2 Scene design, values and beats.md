# Scene Design: Values, Desire, Turning Points, Beats, and the Five Steps of Behavior

*Library file A2. Main source: Robert McKee, "Dialogue" (2016), Part Three (chapters 10–11) and Part Four (chapters 12–19). Written 2026-09-27; fact-checked against the book text and the screenplay, and revised, the same day.*

> **What this file is for**
> 1. It teaches an LLM, or a person with no film training, to take any scene (screenplay or prose) apart into values, desires, beats and a turning point.
> 2. It turns that analysis into a shot structure: which beats earn a new camera setup, which shot must exist, how long to hold, when to cut.
> 3. It gives a fill-in template, decision rules, a checklist and a list of common mistakes.
> 4. It shows the full method on two scenes of *The Catch* and one passage of *The Long Places*.
> 5. It sits upstream of the framing, lens, light and prompt files: they decide how a shot looks; this file decides which shots exist, and why.

---

## 1. The idea in one paragraph

A scene is not its dialogue. McKee's central claim in Part Four is that dialogue is "the final step, the frosting of text atop layers and layers of subtext" (ch. 12). Subtext is what characters want, feel and do beneath what they say. Under the words, each character wants something right now, meets resistance, chooses a tactic, acts, and gets a reaction. Each action and its reaction is a beat. Beats build until one of them changes the charge of a value at stake. That beat is the turning point. The audience reads this hidden layer from faces, bodies, objects and timing, not from the words alone, so the camera has to photograph it. The breakdown therefore works from the inside out: values, desires and beats first; shots last. McKee puts it this way: "A scene lives, not in the activity of talking, but in the action the character takes by talking" (ch. 12).

---

## 2. Vocabulary: one word per concept

Use these terms, and only these terms, everywhere in the pipeline. Do not swap in synonyms.

| Term | Plain definition |
|---|---|
| **Scene** | A stretch of story in more or less continuous time and place in which at least one value changes charge. (This is the working definition from McKee's earlier book *Story*; *Dialogue* says only that "Ideally, every scene contains a turning point", ch. 12.) |
| **Value** | A quality of a character's life with a positive pole and a negative pole: life/death, trust/betrayal, free/contained. Every scene has at least one (ch. 12). |
| **Charge** | Where a value sits at a given moment. Written with plus and minus signs, which is McKee's own notation in ch. 18 (he goes as far as "++++"). This pipeline caps the scale at −−− and +++. "+/−" means mixed; a short qualifier in brackets is allowed, e.g. "+ (uneasy)". |
| **Core value** | The one value the whole story turns on. McKee: "Change core value, change the genre" (ch. 12). |
| **Inciting incident** | The event that knocks the protagonist's life out of balance and starts the story. A scene can have a small one of its own; McKee calls it a "mini–inciting incident" (ch. 15). |
| **Object of desire** | What the character consciously believes will put life back in balance. |
| **Super-intention** | The deep, often unconscious need behind the object of desire. McKee: the object of desire is "what the protagonist wants", the super-intention "the emotional hunger that drives him" (ch. 12). The acting teacher Stanislavski had a related idea, translated as "super-objective" (Hapgood) or "supertask" (Benedetti); McKee does not cite him for it. This file uses McKee's word. |
| **Motivation** | Why the character needs what they need. Optional in a breakdown. |
| **Scene intention** | What the character wants right now, in this scene. Test: "If the writer were to grant the character his scene intention, the scene would stop" (ch. 12). |
| **Background desires** | The relationships and self-image a character will not risk. They limit what the character will say or do. |
| **Forces of antagonism** | Whatever blocks a desire, at four levels: physical, social, personal, inner (ch. 12). Not necessarily a villain. |
| **Spine of action** | The protagonist's continuous pursuit of the object of desire from the inciting incident to the climax. |
| **Tactic** | The specific action a character uses in pursuit of a scene intention: flattering, threatening, stalling. A new tactic starts a new beat. |
| **Beat** | One action plus the reaction it provokes. McKee uses "beat" in this "original sense: a unit of action/reaction. An action starts a beat; a corresponding reaction ends it" (ch. 12). It is not a pause, and it is not a plot point in an outline. |
| **Turning point** | The beat in which a value swings to the charge it will hold at the end of the scene. McKee asks: "In what precise beat of behavior does the value(s) change to the final charge?" (ch. 19). It happens "by action or revelation" (ch. 12). Step 7 turns this into a mechanical test. |
| **Movement** | A section of a scene with its own turning point. Most scenes have one; some have two. McKee's *Raisin* scene has two movements plus a two-beat "resolution movement" that eases the tension (ch. 15). |
| **Progression** | Each beat "tops" the one before it: more pressure, more risk, nearer the turning point. |
| **Scene driver** | The character who makes the scene happen (ch. 19: "Who drives this scene and makes it happen?"): the one whose want sets the scene moving and who starts most beats. The driver does not always win or control. Walter "compels the action and the turning points happen to him" (ch. 15); Tony starts every beat but the last, yet Melfi "controls the conflict from open to close" (ch. 13). Record both roles when they differ. |
| **Text / subtext** | What is said / what is actually being done and felt underneath it. |
| **On-the-nose** | Dialogue that states outright the feeling or intention it should only imply. |
| **Exposition** | Facts about the past, the setting or the characters that the audience needs in order to follow the story. |
| **Third thing** | A subject or object the characters talk about so they do not have to talk about themselves. McKee calls the resulting three-way exchange a "trialogue" and defines the term in ch. 8; his ch. 11 examples are the wine in SIDEWAYS and the film THREE DAYS OF THE CONDOR in Elmore Leonard's novel *Out of Sight*. |
| **Five steps of behavior** | Desire → sense of antagonism → choice of action → action → expression (ch. 12). |
| **Intensity** | Pipeline term, not McKee's. A 1–5 score of how much pressure a beat carries, set by the decision list in Step 6. Used to size shots. |
| **Plant / payoff** | A detail placed early that pays off later. McKee calls a plant a "setup"; this file says *plant* so it does not clash with *camera setup*. |
| **Context** | What the audience already knows and feels when a scene begins. McKee also calls this "setup" (ch. 18); this file says *context*. |
| **Camera setup** | One camera position with one lens. On a set, each new setup costs time; in AI video, each one costs at least one generation. |
| **Key shot** | Pipeline term. The shot a scene cannot lose: the frame in which a turning point is seen. One key shot per value turn listed in the scene's values table; the main turning point's key shot is planned first. |
| **Must-keep shot** | Pipeline term. A shot that is not a turning point but that a later key shot depends on (a plant, a silent beat that explains a later reaction). Never cut it for budget. |

Camera and editing words used below, each in one line:

- **Shot size**: how much of the person fills the frame. *Wide* shows the whole body and the room. *Medium* shows roughly waist up. *Medium close-up* shows chest up. *Close-up* shows the face. *Big close-up* (also "extreme close-up") shows part of the face, such as eyes and mouth. *Insert* is a close shot of an object or a hand.
- **Single / two-shot / three-shot**: one, two or three people in the frame.
- **Profile shot**: the person is seen side-on, nose pointing across the frame.
- **Over-the-shoulder shot**: a single framed past the back of the other person's head and shoulder.
- **Reaction shot**: a shot of the person receiving an action, not the one doing it.
- **Point-of-view (POV) shot**: the camera shows what a character sees, from where she stands.
- **Master shot**: a wide shot that covers the whole scene, or a long stretch of it, from one position.
- **Coverage**: all the shots made of one scene (master, singles, over-the-shoulders, inserts) from which the editor builds it.
- **Reverse (reverse angle)**: a shot from roughly the opposite direction to the one before, usually showing the other person.
- **Blocking**: where the actors stand and how they move during the scene.
- **Deep staging**: placing people at different distances from the camera so that foreground and background both carry action.
- **Pull focus (rack focus)**: shifting sharp focus during a shot from one distance to another, e.g. from a face in front to hands behind. *Soft* means out of focus.
- **Frame within a frame**: a subject seen through a window, doorway, screen or glass that forms a second border inside the picture.
- **Long take**: a shot that runs a long time without a cut.
- **Push-in**: the camera moves slowly toward the subject during the shot. **Pan**: the camera turns left or right on the spot. **Handheld**: the camera is carried, so it moves slightly with the operator.
- **Motivated move**: a camera move triggered by something in the scene (a look, a step, a sound), so it feels caused rather than decorative.
- **Freeze-frame**: a single frame of moving footage held still.
- **Eyeline**: the direction a character is looking. In a single it is recorded as frame-left, frame-right, toward the lens, down, or at a named object.
- **Line of action**: the imaginary line between two characters. Keeping the camera on one side of it keeps screen direction consistent (the "180-degree rule"): if A looks frame-right in her single, B must look frame-left in his.
- **Lens length**: a longer lens (for example 85 mm on a full-frame camera) sees a narrower slice and seems to flatten depth; a wider lens (for example 24 mm) sees more room and seems to stretch it. Strictly, the flattening comes from the camera standing farther away, which a longer lens allows at the same framing.
- **Key light**: the main light on a face, the one that sets where the shadows fall.
- **Cut, hard cut, cutaway**: a cut is a change from one shot to the next. A hard cut is an abrupt one with no transition effect. A cutaway is a cut to something outside the main action (a clock, a window, another person).
- **Match cut**: a cut between two shots that share a shape, movement or composition, so the eye links them.
- **J-cut / L-cut**: an edit where sound and picture change at different moments. In a J-cut the next shot's sound starts before its picture; in an L-cut the last shot's sound carries on over the next picture. In dialogue this lets a line play over the listener's face.
- **Music bed**: music running quietly under a scene.
- **Voice-over**: a voice heard over the picture, not spoken on screen. **Soliloquy**: a character speaking thoughts aloud, alone. **Direct address**: a character speaking to the camera. **Montage**: a quick series of short shots that compresses time.
- **Storyboard**: a drawn or generated still frame for each planned shot. **Previs**: see Step 10.

---

## 3. Core principles from McKee, each with its screen consequence

**P1. Work from the inside out.** "Until you know what you are talking about, you cannot know how your characters go about talking" (ch. 12). *On screen:* plan shots from beats, never from the list of lines. A shot list built line by line produces "ping-pong" coverage that shows who is talking, not what is happening.

**P2. Speech is evidence of character (Part Three).** In ch. 10 McKee argues that "Nouns and verbs express a character's intellectual life and range of knowledge. Modifiers (adjectives, adverbs, voice, modalities) express his emotional life and personality." Specific nouns and verbs ("shank", "sauntered") show knowledge; generic ones ("a big nail", "moved slowly") suggest ignorance. Adjectives and adverbs ("big" versus "stupendous"), active versus passive voice, and modal verbs (the helper verbs could, can, may, must, should, would) show temperament and a sense of what is possible, permitted and necessary. Culture supplies the images a character reaches for, which is how McKee reads the Colossus in *Julius Caesar*, THREE DAYS OF THE CONDOR in *Out of Sight*, yachts in 30 ROCK and wine in SIDEWAYS (ch. 10–11). He adds that "when people lose control of their emotions, their words, phrases, and sentences tend to shorten. Conversely, people in control often lengthen all three" (ch. 13). *On screen (a derived rule, not McKee's):* treat a character's way of speaking as a brief for the camera and for the character designer. Fill in the `speech_profile` in the template (Section 8). In *The Catch*, Saye speaks in full sentences without contractions ("That is your left."), which suggests steady, composed frames. Her one contraction in the script comes when she "has lost the voice she uses for answers" ("They're here. Nell is here.", sc24): a break in a speech pattern marks a loss of control and earns a change of framing. Eli speaks in counts ("One body."), which suggests framing him toward objects and screens, eyes away. At her most decisive Iona speaks in one-word commands ("Push." "Go."), which suggests framing her hands. Give whoever is in control the longer takes.

**P3. Close relationships say less.** McKee borrows Edward T. Hall's idea of high-context cultures, in-groups whose members share so much that "many things can be left unsaid" (ch. 12). *On screen:* the closer the relationship, the more the image must carry: looks, holds, objects. Iona and her brother Eli are an in-group of two ("She can always outwait him").

**P4. Scenes exist to change a value.** A value's charge can reverse, intensify, or wane, and "The precise moment in which the charge of one or more values changes is a scene's turning point" (ch. 12). *On screen:* every value has a visible form (Section 5). The camera shows the charge; the key shot shows the change.

**P5. Desire has five dimensions:** object of desire, super-intention, motivation, scene intention, background desires (ch. 12). *On screen:* the scene intention becomes a blocking goal, the thing the actor moves toward or guards. Background desires become visible restraints. In McKee's SOPRANOS analysis, Tony runs out instead of attacking Melfi because of how the opening was staged: a dozen members of a group session filed out past him as he arrived, so "there were witnesses" (ch. 13).

**P6. Antagonism comes from four levels:** physical, social, personal, inner (ch. 12). *On screen:* physical forces need the environment in frame; social forces need institutional things (glass, uniforms, cameras); personal forces need the other face; inner forces need close-ups, reflections and silence.

**P7. Every line is a tactic on the spine.** "What the protagonist (or any character) does from scene to scene or says from line to line is simply a behavioral tactic" (ch. 12). *On screen:* keep the protagonist's goal visibly consistent across scenes: what she reaches for, which way she moves.

**P8. A scene needs a turning point, timed right.** "If a scene has no turning point, if the value charge does not change in any kind or degree, then the scene is merely an exposition-filled nonevent" (ch. 12). Chapter 9 names three timing faults: too soon, too late, not at all. *On screen:* the turning point gets the key shot (Rules 4, 8, 9).

**P9. The beat is the unit, and repetition is one beat.** "No matter how many times a pattern of action/reaction repeats, it constitutes one, and only one, beat. A scene cannot progress unless its beats change, and beats cannot change until the characters change their tactics" (ch. 12). Name beats with gerunds (a verb plus "-ing"): "The use of gerunds to name the actions beneath exchanges of dialogue is the best way I know to stop yourself from writing on-the-nose" (ch. 12). A beat can run action/reaction/reaction, which McKee reads as intimacy: "When a reaction triggers yet another reaction, it often signals a deeper connection between the characters" (ch. 18). **Escalation is not repetition.** McKee's own breakdowns keep one tactic across several beats when each exchange tops the last: in FRASIER the brothers "for the next four beats choose name-calling as their underlying tactic", and McKee calls them "spiraling insults" ("idiot", "petulant child", "masochist", "crybaby"; ch. 14); in LOST IN TRANSLATION Beats 12 and 13 share the action "Offering false hope" but draw different reactions (ch. 18). The test for merging is therefore whether the exchange tops the previous one, not whether the verb is the same (Step 5). *On screen:* the image changes at beat boundaries and holds inside a beat.

**P10. The five steps of behavior can be slowed down.** In life the steps "fly from first to last in a blur", but "To create a scene, an author must separate the links in this chain of behavior" (ch. 12). McKee then has the writer piece the links back together "so they happen in the breath of time it takes an actor to act or a reader to read". *On screen:* do the same with the camera, but only where the audience must watch a choice being made. At routine beats all five steps sit inside one shot at normal speed. At a turning point, and at beats scored 4 or 5, give step 2 (seeing the obstacle) and step 3 (choosing) their own screen time, as a look or a held pause, before the action lands.

**P11. Silence is an action.** Melfi "turns silence into a weapon. In the right context, refusing to speak can be more powerful than anything said" (ch. 13). Tom's silences are his reactions in the *Gatsby* scene (ch. 16). *On screen:* see Rule 18.

**P12. Every scene is both payoff and plant.** McKee: "every scene, ideally, works as both payoff and setup" (ch. 15). *On screen:* see Rule 20.

**P13. Third things carry subtext.** Characters talk through a third thing so they do not have to name feelings: "To name a feeling is to kill it" (ch. 11). *On screen:* see Rule 19.

---

## 4. The six kinds of conflict in McKee's case studies

McKee says "The quality of conflict determines the quality of action, and the quality of action determines the quality of talk" (ch. 12). He shows six qualities of conflict in chapters 13–18. (His chapter 12 introduction calls the last one "Implied conflict"; the chapter 18 title calls it "Minimal Conflict". This file uses *minimal*.) The screen treatments in the right-hand column are this file's derived rules, not McKee's.

| Type (case study) | How it is built | Beat signature | Screen treatment (derived) |
|---|---|---|---|
| **Balanced** (THE SOPRANOS, "Two Tonys", 2004: Tony and Dr. Melfi) | Two equal wills; one side starts nearly every beat. Conflict builds, "backs off for a moment in Beat 5", then climbs; in the last beat the reactor acts. Three values arc at once. The initiator is not the controller: Tony "starts every beat but the last", yet Melfi "controls the conflict from open to close" through silence and stalling (ch. 13). | 13 beats. Actions escalate: "Turning on the charm", "Cornering her", "Daring her to cross him". | Matched singles or over-the-shoulder shots, same lens and size both sides, tightening together. Break the symmetry at the turning point. Keep the restraint (witnesses) in frame. |
| **Comic** (FRASIER, "Author, Author", 1994: Frasier and Niles) | Balanced conflict pushed to extremes by a "blind obsession", built on clarity, exaggeration, timing and incongruity. It "doesn't arc so much as it drills down"; by Beat 6 "subtext has risen to the text". | 14 beats, many of them mirrored: "Calling Niles an idiot / Calling Frasier a snob". | Wider shots holding both bodies, so action and reaction share a frame. Cut on the punch word, then hold for the laugh. Avoid sympathy-inviting close-ups: "Compassion kills laughs" (ch. 14). |
| **Asymmetric** (*A Raisin in the Sun*: Walter Lee and Ruth) | One side attacks, the other quietly resists: "Walter compels the action and the turning points happen to him" (ch. 15). Two movements, two turning points, both turned by the resister's short lines ("Walter, that ain't none of our money."). | 16 beats. Hansberry "never repeats a beat". | The attacker moves; the resister is anchored in an activity (Ruth making breakfast). Follow the attacker; save the resister's closest shot for her turning line; hold his silence after he loses. |
| **Indirect** (*The Great Gatsby*: Daisy and Tom) | Covert antagonism disguised as social behavior, performed for an audience inside the scene (Nick and Jordan). Objects carry the actions (candles, a bruised finger). Beats 4 and 5 serve the novel's spine, not the scene, by showing Daisy's self-absorption. Fitzgerald leaves Tom's reactions undescribed; McKee re-creates "the reactions that Fitzgerald chose to imply but not describe" (ch. 16). A screen version must show them. | 8 beats, named with single gerunds: "Revealing/Concealing … Attacking/Retreating". | Group shots that keep the witnesses in frame; inserts of the objects; held reaction shots on the target who hides his reaction. The camera sits where the narrator sits. |
| **Reflexive** (*Fräulein Else*; *The Museum of Innocence*) | Self against self. Else argues with her own critical voice in the present tense. Kemal, acting as the museum's guide, tells the reader (cast as a museum visitor) about his past torment in the past tense. The effort to solve the dilemma feeds the dilemma. | Beats inside one mind. McKee counts sentence length: Else's frightened thoughts "average 4.1 words", her critical self's "14.5 words" (ch. 17). | Voice-over, soliloquy or direct address. The setting shows the mind (Else's hotel as a "monstrous, illuminated magic castle": scale, low angles, wide lenses). Objects as exhibits in inserts. Cut faster while fear speaks, slower while reason speaks. |
| **Minimal** (LOST IN TRANSLATION, 2003: Bob and Charlotte at the bar) | Little open conflict; tension comes from what earlier scenes have already loaded into the audience. Pauses and glides ("Well…", "Hmmm…") hold the subtext. Two values move in opposite directions: lost/found sinks to −−−, intimacy/isolation climbs to ++++. | 15 beats; Beats 4, 5, 8 and 10 run action/reaction/reaction. | Longer takes, fewer cuts, two-shots so both reactions play in one frame. Keep every pause. Small physical acts (lighting a cigarette, a toast) are the beat markers. |

---

## 5. Translation table: story meaning to screen choices

Read each row as: "when the breakdown finds this, the shot plan should consider that." These are conventions, not laws; the decision rules in Section 7 say when to break them.

| Story meaning (found in the breakdown) | Screen choices to consider |
|---|---|
| Opening charge of a relationship value is positive (together, trusting) | Open in a shared frame: two-shot, bodies close, no barrier between them. |
| Opening charge is negative (apart, hostile) | Separate singles, a barrier or gap in the frame, bodies angled away. |
| The value changes (turning point) | The key shot. Change the composition at that moment: shared frame to singles (a split), singles to a shared frame (a joining), or a new side of the line of action. |
| A new beat (tactic changes) | Something on screen changes: a cut to a new camera setup, a change of shot size, a camera move, or an actor's move. |
| The same tactic repeated over many lines | Hold the same camera setup and size. Changing the image here signals a change that has not happened. |
| Rising intensity | Tighter shot sizes, shorter shots, or one slow push-in across the beats. |
| A breather beat (tension drops on purpose) | Widen the frame, let a group share it, allow warmer light or a laugh. |
| Scene driver | The camera takes the driver's side: the driver's eyeline, the driver's movement. If power shifts at the turning point, move the camera's allegiance. |
| Scene intention | A blocking goal: the object, door or person the character moves toward or guards. |
| Pursuing, pressing, advancing (gerunds of attack) | The character moves toward the object of the scene intention, or leans in, or stands. |
| Conceding, retreating, yielding (gerunds of retreat) | The character moves away, lowers (sits, looks down) or steps aside, as Iona "steps aside" at *The Catch* sc10 B11. |
| Background desires (restraint) | Witnesses kept in frame, distance held, a voice kept low, an object the character does not touch. |
| Revelation | An insert of the evidence, then the receiving face. Stay on the face long enough to see it land. |
| Action (physical) | The whole action inside one readable frame, usually wider than the shots around it. |
| Subtext (line says one thing, behavior another) | Show the behavior the line hides: a hand, a glance, a habit. The camera catches the contradiction; the actor does not underline it. |
| Silence or waiting used as a tactic | A held take on the person being waited on. No cutaway, no music bed. |
| Third thing (the object they talk through) | Inserts of the object. Stage the characters around it; their eyelines go to it, and a look away from it toward each other becomes a beat marker. |
| Plant, and later its payoff | Matching compositions: same size, angle and lens, ideally the same side of the frame. |
| A character in control (long sentences, McKee ch. 13) | Longer takes on that character. |
| A character losing control (short phrases) | Shorter shots, cuts on their lines, tighter sizes. |
| Status and power | Camera height and who stands or sits. A convention only: a low camera tends to enlarge, a high camera tends to diminish. |
| Unity or simultaneity (they all react at once) | One frame that contains everyone. Singles cannot show "at the same moment". |
| Inner conflict (self against self) | Close-ups, reflections, voice-over, sound design; the setting drawn as the character feels it. |

---

## 6. The breakdown method

Run the steps in order. Each step writes into the template in Section 8.

### Step 0. Find the scene, and in prose, sort scene from summary

- **Screenplay.** Treat each scene heading (the "slugline", such as `INT. SAYE'S HOUSE - KITCHEN - BEFORE DAWN`) as a boundary by default, then check it against the definition: one arc of value change. Several headings marked CONTINUOUS (meaning the action carries straight on with no time jump) can form one scene. The reverse also happens: if one slugline holds two separate value arcs with a time jump or a change of who is present between them, split it into two scenes and say so in `flags`. Keep the script's own slugline count as the scene ID either way, so IDs match the source.
- **Prose.** Tag every passage as one of three kinds. *Dramatized*: moment-by-moment action with quoted speech; this gets a full beat breakdown. *Narratized*: summary, such as "he told it, flat"; this becomes montage, voice-over, or a compressed scene, and the breakdown must say which. *Inner*: thought or memory; this needs a visible carrier (see "Reflexive" in Section 4).
- **Warning.** Screenplays write "(beat)" to mean a short pause, as *The Catch* does. A "(beat)" is not a beat; McKee draws the same distinction (ch. 12).

### Step 1. Context

Write three lines: what the audience knows entering; what has changed since these characters last met; which plants this scene pays off and which it lays. McKee calls this a scene's "setup"; this file says *context*, keeping "setup" for the camera. A quiet scene only works if earlier scenes have already loaded the audience (ch. 18).

### Step 2. Values

List one to three values as positive/negative pairs, named in the terms of the character's life ("Trust / Betrayal (Iona toward Eli)"), not in abstract terms ("family"). Mark which one is the scene's core. Score the opening charge and the closing charge of each. If every value opens and closes at the same charge, write `FLAG: possible nonevent`. Score charges from the character's point of view, and note separately when the audience knows more.

### Step 3. The complex of desire, per character on screen

For each character write: object of desire and super-intention (copied from the story-level file); **scene intention** in one line, "to [verb] [someone/something]"; hidden scene intention, if any; background desires (what they will not do or say here); motivation (optional); **tactics**, filled in after Step 5 as the list of that character's action gerunds by beat; and a **speech profile** (P2). Name the **scene driver**, and, if a different character holds power over the outcome, name that character too (`controls_outcome`). Test each scene intention: if the other side simply gave in, would the scene end? If not, the intention is wrong.

McKee's own question list for writing a scene (ch. 19, "Key Questions": background desires, objects of desire, super-intention, scene intentions, motivation, scene driver, forces of antagonism, scene values, subtext, beats, progression, tactics, turning point, deep character, scene progression) maps field for field onto the template in Section 8. His "deep character" question, "How do the choices of action in this scene reveal the truth about my characters?", goes in the `reveals` field: what the choice at the turning point shows about the chooser. The character-design files use it.

**Splintered scenes (ch. 9).** If the characters' scene intentions never cross, so that nobody blocks anybody, write `FLAG: splintered (parallel desires)`. McKee names this as one of four ways a scene "rambles out of joint"; the others are strong desire with bland dialogue, weak desire with overwrought dialogue, and intentions unrelated to what is said. Flag; do not fix.

### Step 4. Antagonism and conflict type

List the forces of antagonism by level, and any witnesses. Pick the conflict type from Section 4; for mixed types, name the main one and the undercurrent.

### Step 5. Split into beats

1. List every unit in order: each speech and each described physical action. Quote it exactly.
2. For each unit, write what the character is doing *to* someone as a gerund. An **action** gerund must be transitive (it acts on someone or something: accusing *him*, testing *her*) and playable (an actor can do it). A **reaction** gerund may be intransitive when the reaction is inward or a withdrawal, as in McKee's own "Recoiling in terror" and "Coping with defeat" (ch. 14, 15); it must still be playable.
3. Pair each action with the reaction it provokes. That pair is one beat. A reaction can be a line, a silence, a look, a move, or the acting character's own afterthought (McKee: the reaction "could come from within the acting character himself"). It can also come from the world: McKee's beat holds "an action and a reaction from someone or something somewhere in the setting" (ch. 12). In an action scene, "Iona hits STOP / the cage stops dead" is a beat. A second reaction is allowed (action/reaction/reaction).
4. Merge adjacent units into one beat **only if** they use the same tactic **and** the later one does not top the earlier one (no rise in risk, target, or specificity). If each repeat escalates, as FRASIER's insults do, keep each as its own beat and name it so the escalation shows. For every line, answer McKee's question "On which side of the beat does this line play? Is it an action or a reaction?" (ch. 19).
5. Name the beat `Action / Reaction` (or `Action / Reaction / Reaction`) and number it: `B1`, `B2`…
6. Sanity check the count. McKee's case studies run 8 beats (*Gatsby*), 13 (SOPRANOS), 14 (FRASIER), 15 (LOST IN TRANSLATION) and 16 (*Raisin*). The FRASIER scene runs "three minutes and fourteen seconds" on screen for 14 beats (ch. 14), about 14 seconds a beat. Use the industry rule of thumb that one screenplay page runs about one minute. **If** a dialogue scene has fewer than 3 beats per page, look for merged tactics or dropped nonverbal beats; **if** it has more than 10 per page, look for lines split that belong to one tactic. Action-heavy pages can run denser.

**Gerunds.** Use strong, transitive verbs. Weak verbs name activity, not action.

| Avoid (activity) | Prefer (action), choose by what the character is doing to the other |
|---|---|
| talking, saying, telling | accusing, admitting, confessing, warning, instructing, boasting |
| asking | probing, pleading, testing, cornering, inviting, daring |
| answering, replying | parrying, deflecting, minimizing, conceding, stonewalling |
| explaining | justifying, lecturing, reassuring, excusing, selling |
| looking, watching | clocking, appraising, studying, avoiding, witnessing |
| feeling, reacting, thinking | absorbing, doubting, recoiling, bracing, retreating |
| being quiet | outwaiting, withholding, freezing out, refusing |

### Step 6. Score each beat

After each beat, write the charge of each value. Then give the beat an intensity from 1 to 5. Do Step 7 (turning points) before scoring, because a 5 depends on it.

Score with this decision list. Go from the top; the first row that is true sets the score.

| Intensity | The beat contains… | Default shot size |
|---|---|---|
| 5 | A value turn found in Step 7. | The tightest size in the scene, or a deliberate wide (Rule 4) |
| 4 | Any of: an open accusation; a forbidding, threat or ultimatum; a confession; the disclosure of a secret or fact that damages someone present; a physical move that blocks, threatens or shields someone. | Close-up |
| 3 | Any of: a direct challenge, or a direct question the other does not want to answer; a demonstration or test; an open refusal; one character catching another in a slip; a value openly named as at risk. | Medium or medium close-up |
| 2 | Probing, hinting or noticing, with the stakes present but unnamed; a deliberate breather inside a tense scene; resolution beats after the main turning point. | Wide or medium |
| 1 | Logistics or pleasantries; nothing at risk yet. | Wide |

Scoring rules: score relative to this scene, not the whole film. Allow at most two 5s per movement; if Step 7 finds more turns than that in one movement, keep 5 for the main turning point (or, in a movement without it, the latest turn) plus the turn nearest to it, and score the others 4. Intensity should mostly rise ("each action/reaction tops the previous beat to and around the scene's turning point", ch. 12), but a planned drop is allowed. SOPRANOS drops at Beat 5; *Raisin* lightens at Beat 7. After the main turning point, a short fall is normal: that is the resolution (the beats after the turn that let the change settle). Two careful readers may still differ by one point; that is acceptable (Section 15).

### Step 7. Find the turning point

1. For each value, compare its opening and closing charge.
   - **If the sign changes** (positive to negative, negative to positive, or mixed to either), the value turns at the first beat after which its charge sits on the closing side and no later beat moves it back. This follows McKee: a turning point "pivots the instant the value at stake in the scene dynamically changes from positive to negative or negative to positive" (ch. 12).
   - **If the sign stays the same** (the value only intensifies, e.g. + to +++, or wanes, e.g. +++ to +), the value turns at the first beat where it reaches its closing charge and stays there.
   - **If opening and closing charge are identical**, the value does not turn: write `turns_at: none`.
2. Number every value turn `TP1`, `TP2`… in beat order. The **main turning point** is the turn of the core value; add `(main)` to its label.
3. Classify each turn as *action* or *revelation*.
4. Mark the **movements**. A new movement starts right after a turn if the next beat pursues a new goal (a new scene intention, or a new stage of the old one), as when Walter "goes silent for a moment to gather himself for an attack in a new direction with a new scene intention" after *Raisin*'s first turning point (ch. 15). Record for each new movement whether it starts **after a drop** in pressure (a silence, a pause or a change of subject between the turn and the new movement's first beat, or a first beat scored at least two points below the turn) or **without a drop** (the turn launches the next attack directly). Rule 10 uses this.
5. Check timing (ch. 9). **Too soon**: the main turn comes in the first or second beat and three or more beats follow it with no further value turn (McKee's example: the lovers break up in beat one, then "pour out their history"). **Too late**: three or more beats in a row before the turn repeat a tactic without topping, so the audience sees the turn coming. **Not at all**: no value turns; the scene is a nonevent.
6. The pipeline translates; it does not rewrite. If the source has a timing fault, flag it, and let the shot plan compensate by compressing the repetitive beats, never by inventing a new event.

### Step 8. Unfuse the five steps at the turning point

For the turning point, and for any beat scored 4 or higher, write one line per step and attach each to something the audience can see:

1. **Desire**: where the character's attention points (eyeline, the object reached for).
2. **Sense of antagonism**: the moment they register the obstacle (a look, a reaction shot, a point-of-view shot).
3. **Choice of action**: the hinge; a held half-second before they act.
4. **Action**: the move or the line.
5. **Expression**: the exact words or gesture.

### Step 9. Derive the shot structure

Apply the rules in Section 7. For each beat, output shot IDs, size, camera height and angle, movement, what is in frame, lens length ("wider / normal / longer" if the lens file is not loaded), eyeline, whether the line is spoken on screen or off screen, estimated duration, and the **behavior** the actor shows, derived from the gerund. Plan the key shots first (main turning point first), then work outward.

**Staging first.** Before any shot, write one line that places everyone in the room and names the line of action for each pair who exchange looks, e.g. "Seen from the monitor, left to right: Iona, Jude (bed, nearer the glass), Eli." If the script does not fix the positions, choose them and write "staging assumed". Every single's eyeline follows from this line (Rule 26).

**Duration estimates** (pipeline defaults; replace with measured times if a table read exists):

- Spoken lines: count the words and divide by 2.5 (ordinary speech runs roughly 150 words a minute), then add 0.5 s.
- A described action: 1–2 s for a small act (sets down scissors), 2–4 s for a whole-body move.
- Written pauses: "(beat)" about 1 s; "Silence." or "She waits." 2–3 s; "a long moment" or "a long time" 3–4 s.
- A reaction that lands a turning point: at least 2 s held after the line or event.

### Step 10. Hand-off options

The breakdown is the deliverable. Everything below is optional.

- **Storyboard (optional).** Even if you skip storyboarding, make one frame per key shot. That frame is the scene's contract.
- **3D previs in Blender (optional).** Previs is a rough 3D rehearsal of the shots. Block the camera setups on a floor plan; one camera setup is one camera object; beats become timeline markers.
- **Image or video prompts (optional).** One shot is one generation. Write behavior, not emotion: "Iona stops chewing; her eyes go to Saye; she swallows" is renderable; "Iona feels horror" gets a stock face (Rules 24–27). Spend reference images, retries and resolution on key shots first.

---

## 7. Decision rules

Each rule reads: **If** … **then consider** … **because** … A "then consider" rule is a default: break it only with a one-line reason in the breakdown. A plain "then" rule is firm. When two defaults clash, the rule about the turning point wins over the rule about conflict type, and both win over the general beat rules.

**Beats to shots**

1. **If** a new beat starts, **then consider** changing the image (new camera setup, new size, a camera move, or an actor's move), **because** the audience reads a change of tactic from a change of picture.
2. **If** a character repeats one tactic over several lines without topping it, **then consider** holding one camera setup, **because** it is one beat, and a new image falsely signals progress. **If** the repeats escalate (Step 5.4), **then** give each topper its own cut or reframe, on the punch word, **because** each is a new beat.
3. **If** a beat is nonverbal (a move, a gesture, a look), **then consider** giving it a shot in full view, **because** it is still a beat, and a line-based shot list will drop it.
4. **If** a beat is the main turning point, **then consider** the tightest size in the scene, or a deliberate wide when the change is about isolation, waiting or geography, **because** the turning point must look different from everything around it. Other turns get the tightest size of their own movement, or a deliberate wide. Do not spend the scene's tightest size before the main turn.
5. **If** a beat's meaning lands in the reaction (most do), **then consider** holding on the reactor, **because** in McKee "an action starts a beat; a corresponding reaction ends it" (ch. 12), and the film editor Walter Murch's "Rule of Six" (*In the Blink of an Eye*) ranks emotion (51%) above story (23%) and every other reason to cut.
6. **If** a beat runs action/reaction/reaction **and** the value moving is closeness (intimacy or trust rising), **then consider** a two-shot that plays both reactions in one frame, **because** McKee reads the chain as intimacy, and a cut separates what the beat joins. **If** the same shape breaks the relationship (trust falling, as in *The Catch* sc13 B15), **then** singles are right: the separation is the point.
7. **If** several characters react at the same instant, **then consider** one frame that holds all of them, **because** singles cannot show simultaneity.

**Turning points**

8. **If** the turning point is a revelation, **then consider** an insert of the evidence plus a held close-up of the receiver, **because** the audience must see the fact and the change it causes.
9. **If** the turning point is an action, **then consider** a frame that shows the whole action and its result without a cut, **because** a cut inside the action hides the change.
10. **If** a new movement starts after a drop in pressure (Step 7.4), **then consider** a return to a wide size, ideally from a new angle, at its first beat, **because** the second movement begins a new rise and needs room to climb. **If** it starts without a drop, **then** do not widen; cut straight in at the size the turn left you, **because** widening would release the pressure the turn created.
11. **If** power changes hands at the turning point, **then consider** moving the camera to the new driver's side of the line of action, or changing its height, **because** the camera's allegiance tells the audience who now drives the scene. Cross the line only on screen (a camera move or an actor's move that carries the viewer across) or through a neutral shot straight down the line, **because** a bare cut across it flips everyone's screen direction and reads as a mistake.

**Conflict type**

12. **If** the conflict is balanced, **then consider** matched coverage (same lens and size on both sides) that tightens in step, **because** equal framing makes equal wills; break the match only at the turning point.
13. **If** the conflict is asymmetric, **then consider** movement for the attacker, stillness for the resister, and the resister's closest shot saved for her turning line, **because** in *Raisin* the quiet side's short lines turn the scene.
14. **If** the conflict is indirect, **then consider** group shots that keep the witnesses in frame and inserts of the objects doing the damage, **because** the attack is performed for an audience inside the scene.
15. **If** the conflict is comic, **then consider** wider frames that hold both bodies and a hold after each punch line, **because** comedy needs clarity and distance, and, in the vaudeville saying McKee quotes, you must not "step on your own laughs" (ch. 14).
16. **If** the conflict is minimal, **then consider** longer takes, fewer cuts and two-shots, keeping every pause, **because** that is where the subtext lives.
17. **If** the conflict is reflexive, **then consider** voice-over, reflections and a setting drawn as the character feels it, **because** the opponent is inside the character.

**Silence, time and objects**

18. **If** a character uses silence or waiting as a tactic, **then consider** holding on the person being waited on, **because** the length of the silence is the action.
19. **If** a scene talks through a third thing, **then consider** inserts of it and staging around it, **because** it stores the subtext, and eyelines that leave it for the other person mark the escalation.
20. **If** a detail is a plant, **then consider** composing its payoff the same way, **because** matching frames let the audience link them unaided.
21. **If** background desires restrain a character (witnesses, a sleeping child, a sealed door), **then consider** keeping the restraint in frame at the moment of greatest pressure, **because** the audience must see why the character does not explode.

**Prose and AI generation**

22. **If** the source is narratized prose ("he told it"), **then consider** keeping the telling on the teller's face in one long take, not a flashback, **because** the event is often the telling itself. Flash back only when the old events are the turning point.
23. **If** the prose gives inner thought, **then consider** a physical correlate (gesture, object, setting) before voice-over, **because** thoughts cannot be photographed.
24. **If** a generated clip must be shorter than the planned long take, **then consider** splitting at a beat boundary with matched framing, **because** a split inside a beat breaks the action/reaction unit.
25. **If** a prompt names an emotion, **then consider** replacing it with the behavior implied by the beat's gerund, **because** video models render named emotions as stock expressions, while behavior can be checked against the beat.
26. **If** two singles of people looking at each other are generated separately, **then** write the eyeline of each into its prompt (frame-left or frame-right, from the staging line in Step 9) and keep them opposite, **because** each generation knows nothing of the other, and two faces looking the same way read as two people not talking to each other.
27. **If** the listener's face carries the beat (Rule 5), **then consider** playing the line off screen over the listener, joined by a J-cut or L-cut, **because** the audience reads the beat on the reactor; it also removes one lip-sync risk, since even models that generate synced speech vary most on mouths.

**Cuts and scene transitions**

28. **If** a beat ends, **then** cut at the end of the reaction, not in the middle of it, **because** the beat boundary is where a thought completes; Murch ties a well-placed cut to the moment a viewer would blink, at the end of a thought (*In the Blink of an Eye*).
29. **If** a scene opens in a new place, **then** let its first one or two shots show who is where (a wide, or a point-of-view shot followed by a wide), **unless** disorientation is the value at stake, **because** the audience cannot read eyelines and moves in a room it has not seen.
30. **If** a scene's closing charge contrasts with the next scene's opening charge, **then consider** a hard cut; **if** the two scenes share an object, shape or sound, **then consider** a match cut or a sound bridge (the next scene's sound starting early), **because** the transition is itself read as a comment. Follow the script's own transition ("CUT TO BLACK") when it gives one.
31. **If** you plan a whole film, **then** keep a list of every scene's main key shot and make them escalate across each act, **because** McKee's progression runs between scenes as well as inside them: a scene's turning point should top "the turning point in the previous scene" (ch. 12). Do not spend the film's tightest size or longest hold before its climax.

---

## 8. Fill-in scene analysis template

Copy this block once per scene. Every field is required unless its placeholder contains `(opt)`; an optional field may be left blank.

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

---

## 9. Checklist to run against a finished breakdown

Answer each with yes or no. Any "no" needs a fix or a written reason.

1. Does every value have a positive and a negative pole, named in the character's life?
2. Does at least one value close at a different charge than it opened?
3. Is the main turning point a single numbered beat, labeled action or revelation, and does every value's `turns_at` follow the sign test in Step 7?
4. Is the scene driver named, and does each scene intention pass the test "if granted, the scene ends"?
5. Are background desires listed for every character who holds back?
6. Is every action named with a transitive, playable gerund and every reaction with a playable one (none of "talking", "asking", "saying", "looking"), and where two adjacent beats share an action gerund, does the second one top the first or draw a different reaction?
7. Are nonverbal beats (moves, looks, silences) included, and "(beat)" pause markers left out?
8. Was every intensity set by the decision list in Step 6, with no more than two 5s per movement, and does intensity mostly rise toward the main turning point, with every drop explained?
9. Is there exactly one key shot for each value turn in the values table, with the main turning point's key shot planned first?
10. Does every beat change produce a change on screen, and does every held tactic hold the image?
11. Is the scene's tightest shot size saved for the main turning point (or is a deliberate wide explained)?
12. For the turning point and every beat of intensity 4 or higher, are the five steps written out and tied to visible moments?
13. Are plants and payoffs cross-referenced by scene ID, with matching compositions noted?
14. Is the third thing, if any, given inserts and used as the staging axis?
15. Do shot behaviors describe observable action rather than emotion labels?
16. For prose, is every passage tagged dramatized, narratized or inner, with a treatment chosen for each?
17. Are continuity problems (hands, props, eyelines, screen direction) flagged rather than silently fixed?
18. Is there a staging line, and do the singles of two people looking at each other have opposite eyelines (frame-left against frame-right)?
19. Are shot durations estimated with the defaults in Step 9, and does each turning point's reaction hold at least 2 seconds?

---

## 10. Common mistakes, and how to spot them

| Mistake | How to spot it | Fix |
|---|---|---|
| One beat per line of dialogue | Beat count close to line count; many adjacent beats share a gerund | Merge units that use the same tactic without topping each other (P9, Step 5.4). |
| Missing nonverbal beats | A scene with long action lines has beats only where people speak | Re-read the action lines; every move that provokes a response is a beat. |
| Activity verbs instead of actions | Gerunds like "talking", "asking", "explaining", "looking" | Ask "what is she doing *to* him?" and pick from the table in Step 5. |
| Emotions instead of actions | Beats named "sad", "angry", "shocked" | Emotions are results. Name the action that causes them and the behavior that shows them. |
| The loudest moment taken for the turning point | The flagged turning point is a shout, but the value was already settled | Apply the sign test in Step 7: find the beat after which the value sits on its closing side for good. It is often quiet ("I wasn't asking her."). |
| Values named as topics | "Values: medicine, the flask" | A value has two poles and lives in a character's life: "Trust / Betrayal (Iona toward Eli)". |
| Scene intention equals the super-intention | "Iona wants to save her family" for every scene | Scene intention is what she wants right now, from this person: "to make Eli tell her himself". |
| Ping-pong coverage | Shot list alternates speaker singles line by line | Cut at beat boundaries; hold within a beat; favor the reactor. |
| Cutting away from the turning point | The reaction at the key moment is covered by an insert or a cut to the speaker | Hold the reactor through the change. |
| Rewriting the story to "fix" a flat scene | New events appear in the breakdown | Flag the fault; compress in the shot plan; do not invent. |
| Prose summary filmed as dialogue | A narratized passage becomes invented dialogue | Tag it narratized; choose montage, voice-over, or the teller's face. |
| Emotion words in video prompts | Prompts say "feels betrayed", "looks devastated" | Use the behavior from the gerund: where the eyes go, what the hands do, what stops. |
| Escalation merged away | A run of insults or demands, each worse than the last, collapsed into one beat | Split them (Step 5.4). FRASIER's four rounds of name-calling are four beats. |
| Charges that contradict the turning point | The table says a value turns at B7, but its charge already changed sides at B3 or B6 | Re-run the sign test in Step 7, then fix either the charges or the turn. |
| Singles that do not look at each other | Separately generated singles both look frame-right | Write a staging line; give each single its eyeline in the prompt (Rule 26). |
| Every line lip-synced on screen | Shot list shows each speaker as they speak | Put lines the listener carries off screen (Rule 27). |

---

## 11. Worked example A: *The Catch*, sc10, the kitchen at Saye's house

Scene IDs count sluglines in the 25 September 2026 workshop revision. This is scene 10: `INT. SAYE'S HOUSE - KITCHEN - BEFORE DAWN`.

**Context.** Iona has broken her brother Eli out of a medical factory. In the escape the freight cage stopped dead, fell, and after "A hard metal CLACK" was going up; since then everything reads backwards to them. Jude, Iona's partner (matching rings in the last scenes imply a marriage), is shot. In the car (sc9) Iona asked "Eli. Are we going to be all right?" and got "Drive." The audience knows more than Iona: in sc6, Eli's hand went "Behind Jude's back. Out of sight."

**Values**

| Value (positive / negative) | Open | Close | Turns at |
|---|---|---|---|
| A. Normal / Altered: Iona's belief about their own bodies (core) | + | −−− | B7 (TP1, main), revelation |
| B. Free / Contained: who decides where the three of them go | + | −− | B11 (TP2), action |
| C. Trust / Distrust: Iona toward Eli | + | + (cracked) | none; the crack is planted at B6 |

**Movements.** M1 = B1–B8 (diagnosis), turned at B7. M2 = B9–B11 (containment), starting after a drop: Iona absorbs B8 in silence, B9 scores 3 against B7's 5, and Saye turns to a new goal.

**Staging** (partly fixed by the script, the rest "staging assumed"): Jude on the table in the middle of the room; Saye and Iona face each other across it (scripted: "They stand facing each other across the table"); Eli at the counter behind Saye, near the flask; the mint on the windowsill behind Iona.

**Desire**

- **Saye** (scene driver). Scene intention: to find out what happened to them and contain it. Hidden: to confirm her suspicion about the flask; she looks at the blood, "Then, for a long moment, at the flask." Background desires: her duty as a doctor to Jude; the trial she inspects.
- **Iona.** Scene intention: to get Jude treated and keep the three of them together and free. Hidden: to keep believing that the world changed, not them. Background desire: to protect her brother.
- **Eli.** Scene intention: to get Saye's help without explaining what he did. Background desire: Iona's trust.
- **Jude.** Scene intention: to stay alive and keep it light.

**Antagonism and conflict type.** Physical: the mirror reversal itself, and Jude's wound. Social: the hospital and the police. Personal: Eli's secret. Inner: Iona's denial. The main type is **asymmetric**: Saye drives with tests; Iona resists with denial, then with her body. Underneath runs **indirect** conflict: Eli hides what he knows, and an ordinary activity betrays him.

**Beats**

| # | Text (exact) | Action / Reaction | A · B · C after | Int. |
|---|---|---|---|---|
| B1 | Saye looks "At the blood. Then, for a long moment, at the flask." / "Kitchen." | The three appealing (bleeding on her step) / Saye admitting them on her terms | + · + · + | 2 |
| B2 | "Was your appendix on the left?" / "They didn't let me watch." | Saye probing / Jude joking | + · + · + | 2 |
| B3 | She moves the stethoscope "to the other side" and listens "a long time." / "That's his right. The scar. It's where it should be." | Saye verifying / Iona normalizing | + · + · + | 3 |
| B4 | "Hold up your right hand." … "That is your left." / "It's my right." Then "Saye's wedding ring. On her right hand." Iona looks at her own. | Saye demonstrating / Iona refusing / Iona doubting | +/− · + · + | 3 |
| B5 | Eli's cap "will not give. He stops. Twists it the other way." / "Saye is watching him. He sees her watching." | Eli compensating (betraying what he knows) / Saye clocking him | +/− · + · + | 3 |
| B6 | "Her hand moves towards the flask on the counter." / "Don't open the flask." / "Saye sets her scissors down." | Saye testing / Eli forbidding / Saye conceding | +/− · + · +/− | 4 |
| B7 **TP1 (main)** | "Chew that." … "What does it taste of?" / "Not mint." | Saye proving / Iona discovering | −− · + · +/− | 5 |
| B8 | "Nothing has happened to the mint. Nothing has happened to the street signs either." | Saye naming the truth / Iona absorbing it in silence | −−− · + · +/− | 4 |
| B9 | Saye picks up her phone. "Who are you calling?" / "The hospital. Then the police." | Saye reporting / Iona challenging | −−− · − · +/− | 3 |
| B10 | "Iona moves between her and Eli." / "Look at Jude. I cannot finish that here." | Iona shielding Eli / Saye redirecting her | −−− · +/− · + | 4 |
| B11 **TP2** | "She waits until Iona steps aside." / "Nobody leave this room." | Saye outwaiting / Iona yielding | −−− · −− · + | 5 |

**Why the turning points fall where they do.** B7 is a revelation by discovery: Iona's words deny the change twice (B3, B4); her body cannot deny it at B7. By the sign test in Step 7, value A sits at mixed (+/−) from B4 to B6 and first lands on the negative side at B7, where it stays; value B first lands on the negative side for good at B11 (the dip to − at B9 is pulled back to mixed by Iona's block at B10). The script's logic is real chemistry. Spearmint's smell comes from one mirror form of the molecule carvone, (R)-carvone; its mirror twin, (S)-carvone, smells of caraway. To a mirrored body, mint should taste like something familiar but wrong, closer to caraway seed than to anything rotten. So the performance, live or generated, is recognition and confusion, not disgust: prompt "she stops chewing, frowns, chews once more, slowly", never "disgusted". B11 is an action: Saye does not argue, she waits, as Melfi uses silence in McKee's SOPRANOS analysis (ch. 13). Like the *Raisin* scene, this one has two movements: diagnosis (B1–B8) and containment (B9–B11). The intensities follow the decision list in Step 6: B1 and B2 probe (2); B3–B5 test, refuse and catch a slip (3); B6 forbids (4); B7 turns A (5); B8 discloses a damaging fact (4); B9 challenges (3); B10 is a physical block (4); B11 turns B (5).

**The five steps at B7, unfused (Iona)**

1. Desire: to believe they are fine. *Visible:* her eyes on Saye, still defiant from B4.
2. Sense of antagonism: the leaf held out is a test she cannot refuse without admitting fear. *Visible:* the leaf, held into her frame.
3. Choice: she takes it. *Visible:* a half-second hold before her hand moves.
4. Action: she chews. *Visible:* one continuous close-up.
5. Expression: "Not mint." (the script's parenthetical: "not steady"). *Visible:* the line arrives after the face has already told us.

At the turning point the face moves before the line. The shot has to be long enough to contain that order.

**Shot plan** (IDs are sc10.B#.letter; "key" marks key shots, "must-keep" marks plants and other shots a later key shot depends on)

- **B1.** a (must-keep): Saye's point of view, medium on the three at the door; pan from the blood to the flask and hold on the flask ("a long moment": 3–4 s). Her priority is the camera's, and the hold plants the flask. Cut on "Kitchen."
- **B2.** a (must-keep): wide of the bare kitchen ("No photographs. No magnets on the fridge."), the pot of mint on the windowsill in frame as a plant for B7. This wide also shows the room's geography (Rule 29). Iona's lamp is the key light. b: insert, Saye's "quick flat hands" stopping at the scar. "Was your appendix on the left?" plays over the insert.
- **B3.** a: close on the stethoscope crossing the chest; the move is the story. b: Iona, medium close-up.
- **B4.** a: the mirror composition. Profile two-shot across the table on a longer lens, the women at the frame edges, hands raised, "like a woman and her reflection." b (must-keep): insert, Saye's ring on her right hand. c (must-keep): insert, Iona's ring on her own left hand, framed as the mirror of b. These plant sc29, where Iona's left hand meets Jude's through the glass "like a ring and its reflection"; match lens and angle there.
- **B5.** a: deep staging, Saye in the foreground, Eli at the counter behind; pull focus to his hands on the cap. b: Eli's single as he catches her look.
- **B6.** a: insert, flask in the foreground as Saye's hand enters. b: Eli's first close single of the scene, for "Don't open the flask"; saving it gives the line weight. c: insert led by sound, the scissors set down.
- **B7.** a: insert, the leaf torn. **b (key)**: Iona's close-up, the tightest size in the scene, held without a cut from the first chew through "Not mint."
- **B8.** Stay on B7.b; Saye's lines play off screen (Rule 27). The reactor holds the frame. B7.b therefore runs through two beats: about 4 s of chewing, "Not mint.", then Saye's 14 words (about 6 s by the Step 9 default) and a 2 s hold. If the video model cannot make a clip that long, split it at the B7/B8 boundary with matched framing (Rule 24).
- **B9.** a: a new wide from a new side of the room, on the same side of the line of action between Saye and Iona: the triangle of Saye, Iona and Eli, Jude on the table in the foreground. The second movement starts after a drop, so it resets the size (Rule 10).
- **B10.** Hold B9.a so Iona's move plays in one frame. a: cut on "Look at Jude" to Jude, from Iona's eyeline.
- **B11.** **a (key)**: hold the wide through the wait; the waiting is the tactic. b: Saye, medium, eye level, "Nobody leave this room." Hard cut to black, as scripted.

Totals: 11 beats, 19 shots, about 16 camera setups (the ring inserts can share one). Key shots: B7.b and B11.a, one per value turn. The shot-size curve runs wide, medium, the mirror two-shot, inserts, the tightest close-up at B7, back to wide for the second movement, and a medium on Saye to close.

**Continuity flag.** Iona "holds the lamp" yet must raise her right hand in B4. Decide which hand holds it, or have her set it on the table in B3; a lamp low in the middle of the table lights both women alike, which helps the mirror.

---

## 12. Worked example B: *The Catch*, sc13, "You did that"

`INT. QUARANTINE - GLASS PARTITION - LATER`

**Context.** In sc12 Iona demanded "I want the whole thing recorded." / "And no more waiting to tell us things.", and Eli "does not look back." Now Saye, outside the glass, plays the shaft's security footage on a monitor turned toward Iona, Eli and Jude inside. The recording is the **third thing** they argue through. The scene pays off four plants: the hidden hand (sc6); Iona's own warning in sc1, "Stop it hard and there's nothing under it to catch us"; the car question (sc9); "Don't open the flask" (sc10). It plants Nell through Saye's quiet "No. It is not." at B11, after which she "is looking at nothing".

**Values**

| Value (positive / negative) | Open | Close | Turns at |
|---|---|---|---|
| A. Truth / Concealment: what Iona knows about how the cage turned | − | +++ | B7 (TP1), revelation |
| B. Trust / Betrayal: Iona toward Eli (core) | + (uneasy) | −− | B15 (TP3, main), revelation |
| C. Innocent / Culpable: Iona's view of her own part in the fall | + | −− | B12 (TP2), revelation; it starts to slip, to mixed, at B6 |

Value A is limited to how the cage turned, so the flask facts in B1–B4 (what Eli took and why) leave it negative; they are exposition about the flask, not the truth Iona asked the recording for. The close is ironic: the truth arrives and the trust goes. B16 adds a flicker of a different value: whatever the words did, their bodies still react as one family.

**Movements.** M1 = B1–B7 (seeing what happened), turned at B7. M2 = B8–B16 (making Eli answer for it), with turns at B12 and B15. M2 starts **without a drop**: the freeze-frame at B7 launches "You did that." at once, and B8 scores 4, only one below the turn, so Rule 10's reset to wide does not apply; the only widening in M2 is the resolution at B16.

**Staging** ("staging assumed"; the script places only Jude beside Iona): seen from the monitor, left to right, Iona, then Jude in his bed nearer the glass, then Eli. Iona therefore looks frame-right to find Eli, across Jude; Eli, when he finally faces her, looks frame-left. Both look toward the lens while they watch the screen.

**Desire**

- **Iona** (scene driver). Scene intention: to make Eli tell her himself. The proof is her last line, "I wasn't asking her." Background desires: Jude's recovery (she moves his water into reach; at the reveal she looks "at her brother. Not at Jude."); Saye as a witness; a lifetime of sibling habit ("She can always outwait him").
- **Eli.** Scene intention: to justify the act without answering for the silence afterwards. Hidden: to be forgiven without confessing his fear. Background desire: his sister's love.
- **Saye.** Scene intention: to get a clean record. She also vouches for Eli, because his medicine "kept my sister out of hospital." Hidden: Nell, whom she sent across nineteen years ago (revealed in sc17).
- **Jude.** Scene intention: to protect Iona. He ends the scene by switching the screen off.

**Antagonism and conflict type.** Main type **balanced**: two equals; Iona starts nearly every beat, Eli answers in the fewest words. At B12 Eli flips the pattern and acts while she reacts, as Melfi does in the last beat of McKee's SOPRANOS analysis; Iona takes the scene back at B15. The delivery is **minimal** (short lines, pauses, silence as a tactic), with a **reflexive** layer underneath: Iona watches her own elbow cause the fall. The quarantine glass removes the usual exit, so the scene cannot end on a departure. It ends on a device: Jude switches off the screen.

**Beats**

| # | Text (exact) | Action / Reaction | A · B · C after | Int. |
|---|---|---|---|---|
| B1 | "You went back for that. What's in it?" / "A culture. To make medicine." | Iona probing / Eli minimizing | − · + · + | 2 |
| B2 | "His medicine kept my sister out of hospital." / "Turning each dose costs too much. The company wanted the culture turned. Let it grow. Make the medicine itself." | Saye vouching / Eli exposing the company's plan | − · + · + | 2 |
| B3 | "Like that." / "Like that. I wouldn't do it. That flask was proof of the trial they said didn't exist." | Iona implicating / Eli claiming integrity | − · + · + | 3 |
| B4 | "It went over with us." (Eli nods.) "Can it get out of that?" / "Not by itself. It does not own an engine." | Iona fearing / Saye containing ("Saye puts it in a sealed carrier.") | − · + · + | 3 |
| B5 | "Look at that idiot." … "I mean me." / "I know." | Jude mocking himself / Iona tending him | − · + · + | 2 (breather) |
| B6 | On screen her elbow hits STOP; the cage falls. "Iona watches her own elbow hit the button. Beside her, Jude watches her watch it." | The footage confronting Iona / Iona absorbing it / Jude witnessing | +/− · + · +/− | 4 |
| B7 **TP1** | "Eli's hand comes out from behind Jude's back. Empty." A "flat black puck is clipped to the grid." Iona pauses it and "Looks at her brother. Not at Jude." | The footage exposing Eli / Iona freezing it | ++ · +/− · +/− | 5 |
| B8 | "You did that." / "Yes." | Iona accusing / Eli admitting | ++ · − · +/− | 4 |
| B9 | "You could have moved us out of the shaft." / "We would still have been falling." / Saye's finger goes "straight down the screen. Then sideways, into the concrete of the wall." | Iona challenging / Eli justifying / Saye corroborating | ++ · − · +/− | 3 |
| B10 | "What was it rated for?" "She waits. She can always outwait him." / "One body." "One." "You." "Silence." / "I'd been looking at the service drawings for a way out. I knew what the cage weighed. … Us, I guessed. One turn. Nearly the whole charge. Nothing for another try." | Iona outwaiting / Eli confessing (it was bought for her alone) / Eli accounting for the gamble | +++ · +/− · +/− | 4 |
| B11 | "And if you'd got the sum wrong?" / "Then it runs out partway. And partway isn't a place." / "No. It is not." | Iona probing / Eli stating the cost / Saye grieving | +++ · +/− · +/− | 3 |
| B12 **TP2** | "You'd have come up out of that shaft on your own, Io. With me and Jude at the bottom of it. … Tell me that's what you'd have wanted." / "She opens her mouth. Nothing in it." "She looks down at her palm, where the sill took the skin off." "He watches her look at it." | Eli turning the tables / Iona conceding | +++ · + · −− | 5 |
| B13 | "You knew what would happen to us." / "I knew what would happen if I didn't." | Iona re-accusing / Eli parrying | +++ · +/− · −− | 4 |
| B14 | "And afterwards?" / "He has been looking at the screen. Now he looks at her." | Iona pressing / Eli facing her | +++ · +/− · −− | 3 |
| B15 **TP3 (main)** | "I asked you in the car. … You let me drive like that. … Don't open the flask. You could say that." / "I thought if I got us to Saye, she'd have an answer." / "I wasn't asking her." | Iona indicting the silence / Eli excusing / Iona rejecting the excuse | +++ · −− · −− | 5 |
| B16 | She "Lets the recording run." On the screen the upside-down cage falls empty. "All three of them flinch at the same moment." "Jude takes the remote and switches it off." | Iona releasing the footage / all three flinching / Jude ending it | +++ · −− · −− | 2 (resolution) |

**Reading the beat list.** The argument is won twice. Eli wins the question of the *act* at B12: Iona cannot say she would rather have come up alone, and the skinned palm is her body's proof that his gamble saved her. Iona wins the question of the *silence* at B15: her charge was never that he turned them; it was "You let me drive like that." B15 is the main turning point because it sets the core value's closing charge. The intensities follow the decision list in Step 6: probing and exposition score 2 (B1, B2), challenges and a named risk 3 (B3, B4), the breather 2 (B5), damaging disclosures, accusations and the confession 4 (B6, B8, B10, B13), direct questions 3 (B9, B11, B14), the three value turns 5 (B7, B12, B15), and the resolution 2 (B16). Note that B6 has no dialogue at all, yet it explains B12. Iona has just watched herself cause the fall she is blaming on him, and Jude watched her see it. A shot list built from lines would drop B6, and B12 would then play as a plot convenience.

**The five steps at B7, unfused (Iona)**

1. Desire: the whole truth, recorded. *Visible:* her eyes fixed on the monitor.
2. Sense of antagonism: the empty hand, the puck. *Visible:* an insert of the footage.
3. Choice: stop it here. *Visible:* her thumb on the remote; a freeze-frame.
4. Action: she pauses it and turns. *Visible:* the head turn.
5. Expression: the direction of the look, "Not at Jude." *Visible:* her eyeline crosses past Jude and lands on Eli.

**Camera setups**

- **S1, the monitor's view (master):** the camera sits where the screen is and looks back through the glass at the three faces lit by it; Saye at the frame edge; reflections on the glass.
- **S2, reverse from inside:** behind the three, toward the monitor and Saye beyond the glass.
- **S3, the footage, full frame:** the overhead security view down the shaft, the only high angle in the scene.
- **S4 and S5, Iona and Eli singles:** matched size and lens, as balanced conflict calls for. Eyelines from the staging line: both near the lens while watching the screen; Iona frame-right when she looks at Eli; Eli frame-left when he looks at her. Eli's eyeline stays on the screen, not on Iona, until B14.
- **S6, Saye single through the glass:** a frame within a frame.
- **S7, inserts:** flask, grey dish, remote, palm.
- **S8, three-shot:** Jude, Iona and Eli, for B5 and B16.

**Shot plan**

- **B1–B4.** S1 and S2, inserts of the flask and the grey dish, singles at a matched medium size. Cut when the beat changes, not on every line.
- **B5.** S8: the only laugh, a wider and warmer frame.
- **B6 (must-keep).** S3 (elbow, STOP, the fall), then S4: monitor light moving on Iona's face, Jude soft in the foreground with his eyes on her. No line; hold 3–4 seconds.
- **B7 (key, TP1).** a: S3 pushing in on the footage to the empty hand and the puck, motivated by Iona's attention. b: remote insert, freeze. c: S4, her head turn; the eyeline passes Jude and lands on Eli.
- **B8.** S4 and S5, close, matched, hard cuts, no music. Hold after "Yes."
- **B9.** S6 shot from inside, so Saye's finger-drawing is seen as Iona sees it.
- **B10.** S5 held on Eli while she waits, her shoulder soft at the frame edge. Cut to Iona only on "You." Hold her in the silence (2–3 s); the tightest sizes so far. Back to S5 for "I'd been looking at the service drawings…", which Eli says to the screen, not to her: the account is the second reaction, and his eyeline shows he still cannot face her.
- **B11.** S6, Saye "looking at nothing", held. This plants Nell.
- **B12 (key, TP2).** S5, "You'd have come up out of that shaft on your own, Io…" through "Tell me that's what you'd have wanted."; S4 as her mouth opens; S7 palm insert composed to rhyme with sc6, where "Her palm drags across the bright steel"; S5, Eli watching her look at it.
- **B13.** Singles, cut faster: the lines are short.
- **B14 (must-keep).** S5: Eli's head turns from the screen to Iona (eyeline from the lens to frame-left), the first time in this scene he looks at her. The eyeline change is the beat, and B15 depends on it.
- **B15 (key, TP3, main).** Slow push-in on Iona across "I asked you in the car…", her longest speech: she is in control. Eli's excuse in his single. "I wasn't asking her." on Iona, held at least 2 s; no cut to Eli until the hold lands. The push-in ends on a big close-up, the tightest size in the scene. The beat runs action/reaction/reaction, but it breaks the relationship, so singles, not a two-shot (Rule 6).
- **B16.** S8 or S1, all three in one frame for the flinch, because simultaneity needs one frame. Insert of Jude's thumb on the remote. The screen goes black, which can match-cut to the tablet screen that opens sc14.

Totals: 16 beats, about 31 shots, 8 camera setups (S1–S8). Key shots: B7, B12 and B15, one per value turn; must-keep: B6 and B14. The intensity line is 2, 2, 3, 3, 2, 4, 5, 4, 3, 4, 3, 5, 4, 3, 5, 2: it rises in waves, and the dips at B5, B9, B11 and B14 are the quiet hinges between blows; B14, the silent turn of Eli's head, is the last hinge before the main turn. The eyelines are the beat markers: Eli toward the screen (avoiding), Iona toward Eli "Not at Jude" (B7), Eli toward Iona (B14).

---

## 13. Worked example C: a question that travels across four scenes (*The Catch*)

Beats can pay off across scenes. The breakdown has to track them, or the shot designer will frame each occurrence differently and the thread disappears.

| Scene | Exact text | Beat | Screen choice |
|---|---|---|---|
| sc9, the car | "A red light. Iona finds his eyes in the mirror." / "Eli. Are we going to be all right?" / "He looks down at the flask in his hand for a long time." / "Drive." | Iona pleading / Eli withholding | Key shot: Eli's eyes found in the rear-view mirror, the flask low in frame. In a film about mirror reversal, the question is asked into a mirror. Hold the "long time" before "Drive." |
| sc13, the partition | "I asked you in the car." | Payoff inside B15, the main turning point | Push-in on Iona (Section 12). |
| sc23, the ship | "Eli looks through the wall at his sister." / "Io." / "Are we going to be all right?" / "I don't know." | Eli seeking comfort / Iona refusing to lie | The roles reverse: she gives the true answer he withheld. Frame it through the glass wall, echoing the mirror in sc9. |
| sc29, the last day | "In the car-" / "Yes." | Eli apologizing / Iona accepting | Minimal conflict at its purest: two words carry the whole thread. Two-shot through the glass. Keep the pause; do not cut. |

**Rule shown.** When a line or gesture recurs, record every occurrence under `plants` and `pays_off` in the template. Give all of them related compositions: here, always a barrier between the siblings (a mirror, then glass, then glass again). The kitchen ring insert (sc10.B4.b) and the rings through the glass in sc29 form the same kind of pair.

---

## 14. Worked example D: *The Long Places*, prose, chapter III ("The Measure")

The novella interleaves a lamp-keeper's italic letters with third-person narrative, and its narrative slides between dramatized and narratized telling.

**The text (exact).** Yusuf "put the camera up on the third still evening and asked, cheerfully, on the record, 'Professor, the watches. Three. Why?'" / "'I am equipment,' Márton said, 'not content,' and turned off nothing, because it was not his camera." / "But that night, at the table, with the tea gone cold and the generator off and the hill drinking somewhere under them, he told it, flat, in the voice he used for instrument logs." A paragraph of summary then tells the 1997 story. Then: "'Do you think it was real?' Yusuf asked, no camera, the first fully serious sentence Márton had heard from him." / "'It was measured,' Márton said."

**Step 0 and the value.** Two dramatized scenes (evening, night) bracket one narratized paragraph (1997). Value: Concealed / Disclosed, meaning Márton's old wound, the paper he withdrew after a referee called it "wishful". It opens at − and closes at ++.

**Beats.** Evening, B1: Yusuf probing on the record / Márton deflecting with a quip; no change, a failed attempt. Night, B2: generator off, tea cold, no camera; Márton confessing / the table listening. The value turns by action. Night, B3: Yusuf asking in earnest / Márton refusing to claim more than the data ("It was measured"). The value intensifies.

**Screen choices.**

1. **The camera prop is the value's visible form.** In the evening, Yusuf's camera sits in frame between the two men, its recording light on. At night the same table, framed the same way, has no camera. That absence is the key shot (Rule 20).
2. **No flashback by default.** Following Rule 22, keep the 1997 story on Márton's face in one long take, his voice flat. The event is the telling. McKee praises a related restraint in LOST IN TRANSLATION: rather than have her characters narrate their past conflicts "vividly and explicitly", Coppola "keeps the dramas offscreen and implicit" (ch. 18). (McKee's point there is about dialogue, not flashbacks; the screen rule is this file's.) If the telling runs longer than the video model's clip limit, split it at sentence ends where Márton's eyes move (to the tea, to the dark), never mid-sentence (Rule 24).
3. **Speech as a camera brief (P2).** Márton's lines are controlled and exact ("That is a different thing from real, and a different thing from false"). Give him the long take; give Yusuf's earnest question the cut.

A smaller moment in the same chapter is a one-beat scene with two reactions: "'Does it have a name?' she asked." / "'It has a serial number.'" / "'Poor thing,' she said, and went in to her wicks." Melek humanizing / Márton correcting / Melek pitying and leaving. Play it in one two-shot with no cut; her exit ends the beat. Her pity lands on the instrument and, by implication, on him, so his face must be in frame when she says it.

---

## 15. Limits and open points

- **Intensity is not McKee's.** The 1–5 scale and its decision list (Step 6) are pipeline tools for sizing shots. The list was calibrated on the two *Catch* scenes only; check it on the *Long Places* test before relying on it. Two analysts may still differ by one point.
- **Beat boundaries are judgment calls.** McKee himself calls his breakdowns "logical, after-the-fact analyses of finished work" (ch. 12). The same scene can be split one beat finer or coarser. The checks (merge repeated tactics; keep nonverbal beats) matter more than the exact count.
- **Screen treatments per conflict type are derived.** Section 4's right-hand column and the decision rules are this file's translations of McKee's scene theory into camera practice. McKee's book is about dialogue and does not prescribe coverage.
- **Clip length in video models** changes often and is not recorded here. The prompt file must supply current limits before long-take rules are applied.
- **Staging is often assumed.** Screenplays rarely fix who stands where. The worked examples mark their staging lines "assumed"; a downstream step that changes the staging must re-derive every eyeline.
- **Duration defaults are rough.** 2.5 words a second suits ordinary speech; slow, weighted delivery (Márton, Saye) runs slower, and comic delivery faster.
- **Charges scored from the character's view** can differ from the audience's. Record both when they differ (the audience suspects Eli well before Iona does).

---

## Sources

**Primary**

1. Robert McKee, *Dialogue: The Art of Verbal Action for Page, Stage, and Screen* (New York: Twelve, an imprint of Grand Central Publishing / Hachette Book Group, 2016). Read in full for this file: Part Three (ch. 10 "Character-Specific Dialogue", ch. 11 "Four Case Studies") and Part Four (ch. 12 "Story/Scene/Dialogue", chs. 13–18 case studies, ch. 19 "Mastering the Craft"); also ch. 9 ("Misshapen Scenes", "Splintered Scenes") for turning-point timing. Quotations are from the ebook edition (ISBN 978-1-4555-9192-3, per its copyright page). Chapter numbers are given instead of page numbers because the ebook has no fixed pages.
2. Robert McKee, *Story: Substance, Structure, Style and the Principles of Screenwriting* (New York: ReganBooks / HarperCollins, 1997). *Dialogue*'s endnotes cite it for ten of the eleven notes in chapter 12 (the other is Edward T. Hall, *Beyond Culture*, for high- and low-context cultures). Its chapter "Scene Analysis" gives a five-step method (define the conflict; note the opening value; break the scene into beats; note the closing value and compare it with the opening; survey the beats and locate the turning point). Cited from general knowledge of the book; not re-checked for this file. An earlier draft cited a social-media post for this; that post could not be opened and the citation was removed.

**Film craft**

3. Nicholas T. Proferes, *Film Directing Fundamentals: See Your Film Before Shooting* (Focal Press; the 2nd edition, 2005, was checked; other editions exist). Organizes scenes by "dramatic blocks", "narrative beats" and "the fulcrum" (his name for the moment a scene pivots, close to McKee's turning point), with a staging and camera analysis of the patio scene in Hitchcock's NOTORIOUS (1946), and later chapters on THE TRUMAN SHOW, 8½ and other films. Table of contents checked at https://catdir.loc.gov/catdir/toc/ecip0421/2004019069.html on 2026-09-27. Recommended as the closest published bridge from beats to camera.
4. David Mamet, *On Directing Film* (New York: Viking, 1991). Argues that a film should be built from a shot list of simple, "uninflected" shots (each showing one plain thing without comment) whose juxtaposition tells the story, worked out scene by scene in his Columbia class sessions. Summarized from general knowledge plus a secondary summary at https://www.premiumbeat.com/blog/gutter-editing-and-the-uninflected-shot/ (checked 2026-09-27; note that the summary misdates the book to 1988); not quoted.
5. David Mamet, memo to the writers of THE UNIT (signed "Santa Monica 19 Octo 05", i.e. 19 October 2005), widely reproduced. Asks of every scene: "WHO WANTS WHAT? WHAT HAPPENS IF HER DON'T GET IT? WHY NOW?" (sic). Checked at https://nofilmschool.com/2010/10/david-mamet-drama-a-memo-the-unit-writers on 2026-09-27.
6. Walter Murch, *In the Blink of an Eye: A Perspective on Film Editing* (Los Angeles: Silman-James Press, 2nd ed. 2001). The "Rule of Six": emotion 51%, story 23%, rhythm 10%, eye-trace 7%, two-dimensional plane of screen 5%, three-dimensional space of action 4%; also the book's title argument, that a viewer blinks at the end of a thought and a well-placed cut falls there (Rule 28). Percentages as given in the book, from general knowledge; the StudioBinder summary at https://www.studiobinder.com/blog/walter-murch-rule-of-six/ (checked 2026-09-27) confirms the order of the six and "over 50%" for emotion but does not list every figure.
7. Judith Weston, *Directing Actors: Creating Memorable Performances for Film and Television* (Studio City: Michael Wiese Productions, 1996). The case for playable action verbs over adjectives and "result" direction, which supports the gerund rules here.
8. Steven D. Katz, *Film Directing Shot by Shot: Visualizing from Concept to Screen* (Studio City: Michael Wiese Productions, 1991). Staging and coverage of dialogue scenes.
9. Daniel Arijon, *Grammar of the Film Language* (London: Focal Press, 1976). Coverage patterns for conversations and the line of action.
10. Konstantin Stanislavski, *An Actor Prepares*, trans. Elizabeth Reynolds Hapgood (New York: Theatre Arts, 1936). Source of "units", "objectives" and the "super-objective". The popular story that "beat" comes from a Russian-accented "bit" is often repeated but unverified; do not rely on it.

Items 7–10 are cited from general knowledge of these standard texts; no passages were re-checked for this file.

**Facts checked on the web (2026-09-27)**

11. THE SOPRANOS, "Two Tonys" (season 5, episode 1), written by David Chase and Terence Winter, directed by Tim Van Patten, first aired on HBO on 7 March 2004: https://en.wikipedia.org/wiki/Two_Tonys
12. FRASIER, "Author, Author" (season 1, episode 22), written by Don Seigel and Jerry Perzigian, directed by James Burrows, first aired on NBC on 5 May 1994: https://en.wikipedia.org/wiki/Frasier_season_1 (page opened 2026-09-27).
13. Carvone: (R)-(−)-carvone smells of spearmint and its mirror image (S)-(+)-carvone of caraway; the difference shows that smell receptors respond to one mirror form more than the other: https://en.wikipedia.org/wiki/Carvone (page opened 2026-09-27) and https://www.acs.org/molecule-of-the-week/archive/c/carvone.html (checked via search-result text).

**Test texts**

14. *The Catch*, original short screenplay, workshop revision of 25 September 2026 (upload `1edae70d-35_The_Catch_-_workshop_revision_of_Final4.txt`), read in full. Scene IDs count its 30 sluglines.
15. *The Long Places*, prose novella, revised final (upload `5dcd8176-19_The_Long_Places_-_revised_by_Claude_final.md`), chapters I–III read; the rest skimmed by heading.
