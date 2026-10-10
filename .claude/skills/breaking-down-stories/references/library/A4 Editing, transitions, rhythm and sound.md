# A4. How Moments Build and Break: Editing, Transitions, Rhythm, Suspense and Sound

*Library file A4. Written 2026-09-27; fact-checked and extended the same day. Main sources: Walter Murch, "In the Blink of an Eye"; Michel Chion, "Audio-Vision"; Sergei Eisenstein, "Methods of Montage"; François Truffaut, "Hitchcock"; David Bordwell, "Intensified Continuity"; Robert McKee, "Dialogue" (chapters 1, 2, 5 and 16, checked against the book text). Web facts were checked on 2026-09-27.*

> **What this file is for**
> 1. It teaches the pipeline how shots join into scenes and scenes into a film: where each cut falls, how long each shot runs, which transition joins two scenes, and what the audience hears.
> 2. It turns story beats (build, turning point, rupture, aftermath) into cut points, shot durations, transitions and sound cues.
> 3. It gives a vocabulary, a translation table, decision rules, a fill-in spec, a checklist and a list of common mistakes.
> 4. It works through *The Catch* (the cage fall, the recording reveal, the pump and the ending) and one passage of *The Long Places*.
> 5. It sits after the scene-design, dialogue and camera files (A2, A1, B1) and before the prompt files (C1, C2): those decide what each shot shows; this file decides order, length, joins and sound.

---

## 0. How to use this file

**Where it sits in the pipeline.** A2 splits a scene into beats and proposes shots. B1 chooses size, angle, lens and movement. This file then adds, per shot: why the shot starts and ends where it does, its duration, the transition out of it, and its sound. Per scene it adds: a rhythm plan, an information ledger (who knows what), the rupture (the moment the scene breaks), and the sound motifs in play.

**The fact that shapes everything for AI production.** Video models make *clips*, not edits: one shot at a time, usually 4 to 15 seconds (C1). Every transition in this file is made afterwards in an editing program, and most sound is finished there too. So the breakdown must plan each shot longer than it will be used, say where each cut falls, and list sound separately from picture.

**Order of work for an LLM** (details in Sections 9 to 11):
1. Copy the scene's turning point and beat intensities from A2, and list every editing or sound cue the text itself gives (Section 5.1: FADE IN, CUT TO BLACK, (O.S.), (V.O.), sound words in capitals, "BLACK.").
2. Fill the information ledger (Section 6.5).
3. Set the scene's rhythm plan and mark its rupture (Sections 6.1 to 6.8).
4. For each shot: cut-in reason, cut-out reason, duration, transition out (Sections 3 to 5).
5. Spot the sound: ambience, synchronized effects, off-screen sounds, motifs, music, silence (Section 7).
6. Fill the spec (Section 10) and run the checklist (Section 12).

---

## 1. Vocabulary: one word per concept

Use these words, and only these, everywhere in the breakdown. Chion's sound terms (added value, synchresis, point of synchronization, acousmatic sound, de-acousmatization, acousmêtre) are defined in Section 7.1; suspense, surprise and reveal in Sections 6.5 and 6.6; beat and turning point in A2.

| Term | Plain definition |
|---|---|
| **Transition** | Any join between two shots. |
| **Cut** | The transition where one shot simply stops and the next starts, with no effect. (Editors also say "straight cut"; this file says "cut".) |
| **Cut point** | The exact frame where a shot ends and the next begins. |
| **Coverage** | The full set of shots made for one scene, from which the editor chooses. |
| **Hold** | Letting a shot run on without cutting. |
| **Reverse** | A shot looking back the other way, usually at the person the previous shot's character was looking at. |
| **Insert** | A close shot of a detail that is part of the action already on screen (a hand, a button, a label). |
| **Cutaway** | A shot of something that is *not* part of the action on screen (another place, a watcher). |
| **Axis** | The imaginary line through two characters, or along a character's path, that the camera stays on one side of ("the line", "the 180-degree line"). |
| **Screen direction** | Which way a person or thing moves or looks across the frame: toward frame left, toward frame right, up or down. |
| **Eyeline** | The direction a character is looking, as it appears in the frame. |
| **Geography** | The audience's mental map of where people and things are in a space. |
| **Rhythm** | The pattern of shot lengths, and of events inside shots, as felt over time. |
| **ASL (average shot length)** | Running time divided by number of shots. |
| **Rupture** | The moment a scene breaks: the film suddenly stops doing something it has been doing (a sound, a camera behavior, a cutting pattern, the picture itself). |
| **Aftermath** | The stretch after a turning point or rupture, where the audience absorbs the change. |
| **Information ledger** | This file's table of who knows what, and when: the audience and each character. |
| **Plant / payoff** | A plant is a detail shown early; its payoff is the later moment that gives it meaning. |
| **Landing face** | (From A1.) The face on screen when a line's key word or a revealed fact lands. |
| **Diegetic / non-diegetic sound** | Sound inside the story world, which characters could hear (a pump, a radio) / sound they cannot hear (score, an outside narrator). |
| **On-screen / off-screen sound** | Diegetic sound whose source is / is not in the frame at that moment. |
| **Room tone** | The quiet background sound of a particular space, so that "silence" is not dead digital nothing. |
| **Ambience bed** | A continuous background layer for a location (rain, hum, traffic) that runs under several shots. |
| **Sound motif** | A recurring sound that gathers meaning each time, like a musical theme. |
| **Split edit** | A transition where sound and picture change at different moments: a **J-cut** (the next shot's sound starts before its picture) or an **L-cut** (the previous shot's sound carries on over the next picture). A **sound bridge** is a split edit across a scene change. |
| **Handles** | Extra frames before and after the part of a shot you plan to use, so the cut point can move. |
| **Frame** | One still image. This file assumes 24 frames per second: 12 frames = 0.5 seconds. |
| **Single / two-shot / three-shot** | A shot with one / two / three people in it. A **clean single** shows only that person; a **dirty single** keeps a sliver of the other person's shoulder or head at the frame edge. |
| **Over-the-shoulder (OTS)** | A shot from just behind one person's shoulder toward the person they face; the near shoulder stays in frame. |
| **Shot/reverse shot** | The standard way to cut a conversation: a shot of A, then the reverse of B, alternating. |
| **Macro** | An extreme close shot of a tiny detail, as if through a magnifying lens (a bead of blood, a fingertip on a button). |
| **Picture lock** | The point in editing when shot order and lengths are final; music and the final sound mix are fitted after it. |
| **Grade** | The adjustment of color and brightness of shots in the editing program so they match and carry mood (B2). |
| **Score / source music** | Score is music composed for the film that only the audience hears (non-diegetic). Source music comes from something in the story world, such as a radio or a band (diegetic). |
| **Cue / sting** | A cue is one continuous piece of music in the film, with an in-point and an out-point. A sting is a short, sharp musical accent on a single moment. |
| **Foley** | Everyday synchronized sounds (footsteps, cloth, hands on objects) recorded or generated to match the picture; named after the sound editor Jack Foley. |
| **O.S. / V.O. / PRE-LAP** | Screenplay marks. (O.S.), off-screen: the speaker is physically in the scene but out of frame. (V.O.), voice-over: the voice is not physically in the scene (a narrator, a thought, a radio, a phone, a recording). PRE-LAP: a line or sound from the next scene that starts before the cut, which is a J-cut. |
| **Stems** | Separate finished audio tracks for dialogue, music and effects, handed over so levels can be changed later without remixing everything. |

---

## 2. Core principles

- **P1. Meaning is made between shots.** Kuleshov showed that a neutral face reads differently depending on the shot beside it, and that shots from different places, cut together, read as one place (Section 4.2). For AI production this is the method: every shot is generated separately, and only the edit makes them one room, one moment, one feeling.
- **P2. Emotion comes first.** Murch weights emotion at 51 percent of what makes a cut right (Section 4.1). When rules conflict, keep the feeling.
- **P3. Cut when the thought changes.** A cut works like a blink: it falls where one idea has been taken in and the next is wanted.
- **P4. Continuity keeps the audience oriented.** Break it only when you want them lost, and then break it clearly.
- **P5. Rhythm is contrast.** A 2-second shot is fast only next to 5-second shots. A scene's peak is its shortest or longest shot, never its average one.
- **P6. Suspense comes from giving information** (Hitchcock's bomb, Section 6.5).
- **P7. A rupture is a broken pattern.** Teach a pattern (steady sound, steady cutting, a stable camera), then break it on the turning point.
- **P8. Sound is half of every shot.** The audience credits the picture with what the sound adds (Chion's "added value", Section 7.1); off-screen sound enlarges the world; sound before its source creates dread.
- **P9. Plants and payoffs are designed as pairs,** echoing each other in framing or sound.
- **P10. Strong devices lose force with use.** Cut to black, true silence, freeze frames, smash cuts and slow motion get a budget per film; spend it on turning points.

---

## 3. Continuity editing: the grammar of joining shots

**Continuity editing** is the system, standard in Hollywood by the 1920s, that makes separate shots feel like one continuous action in one coherent space (Bordwell and Thompson, *Film Art*).

### 3.1 The axis (the 180-degree rule)

Draw a line through two characters who face each other and keep every camera on one side of it. Then A stays on frame left, B on frame right, and their eyelines meet across every cut. Jump to the other side and they swap sides, and the audience feels turned around. The same applies to movement: a character who exits frame right should enter the next shot from frame left (Wikipedia, "180-degree rule", checked 2026-09-27).

**Crossing without confusion:** (1) move the camera across the line within one shot, so the audience sees it happen; (2) cut to a shot *on* the line (Wikipedia calls it a "buffer shot"), then continue on the new side; (3) let a character walk across, carrying the axis; (4) reset with an insert or a wide re-establishing shot.

**Crossing on purpose, to disorient:** Kubrick in the bathroom scene of *The Shining* (1980); Dreyer in *The Passion of Joan of Arc* (1928); Godard in *Breathless* (1960), in a car scene in the first five minutes that jumps between the front and back seats; Ozu, Wong Kar-wai and Tati at times (all on Wikipedia, "180-degree rule"). Put the crossing on the turning point and make it obvious, so it reads as meaning, not error.

**A horizontal flip crosses the axis for everything in the shot.** Flipping a clip reverses every screen direction, eyeline, text and handedness in it. B1 flips deliberately for *The Catch*'s mirrored world (Worked Example 1); anywhere else a flip is a hidden error.

### 3.2 The 30-degree rule

Between two shots of the same subject, move the camera at least 30 degrees around it, or change the shot size by at least one full step on B1's shot-size ladder (for example medium to close-up); smaller changes look like the picture jumped. Murch: audiences struggle with displacements "that are neither subtle nor total", such as a cut from a full-figure master shot (a wide shot covering the whole action) "to a slightly tighter shot that frames the actors from the ankles up" (quoted on Wikipedia, "30-degree rule", checked 2026-09-27).

### 3.3 Eyeline match: look, object, reaction

An **eyeline match** cuts from a character looking off-screen to what they see; the audience assumes the second shot is their view. *Rear Window* (1954) is built on it. The unit is three shots: **look**, **object** (often a point-of-view shot, taken from the character's eye position), **reaction**. The meaning lands on the reaction; if one must go, keep the reaction. Matched singles in a conversation share shot size, lens and camera height (Wikipedia, "Eyeline match", checked 2026-09-27).

### 3.4 Match on action and cutting on motion

A **match on action** cuts from one view of a movement to another view of the same movement, so it starts in shot A and ends in shot B; the motion carries the eye and hides small mismatches. Kurosawa cut on action to avoid calling attention to his cuts; in *Seven Samurai* (1954) a cut falls on Shichirōji kneeling to comfort Manzo (Wikipedia, "Cutting on action", checked 2026-09-27). Dmytryk's third rule: "Whenever possible cut 'in movement'." **For AI:** generate the *whole* movement in both clips (crews call this overlapping action) and name it in the spec ("both clips contain the full elbow strike on STOP").

### 3.5 Screen direction, within and across scenes

Keep a journey's direction constant from shot to shot and scene to scene; reverse it only when the story reverses (a return, a retreat). An unmotivated reversal reads as "she turned back". **Vertical direction counts too:** *The Catch* is built on climbing, descending, falling and rising, so write it into every shaft shot ("the wall streams upward past the grid" means the cage is going down). **For AI:** a model knows nothing of the previous clip, so write direction into every prompt and check every take.

### 3.6 Establishing geography

An **establishing shot** is a wide shot, usually at a scene's start, showing where it is and where people and things are; modern films often skip or delay it (Wikipedia, "Establishing shot", checked 2026-09-27). The pipeline's rule: *before the audience must read a spatial relationship under pressure, show it once calmly.* *The Catch*'s ladder, yellow stripe and maintenance opening must be established during the climb (sc2), because in the fall (sc6) they flash past in fractions of a second. After a rupture, **re-establish** with one clear orienting shot.

**Creative geography** (Kuleshov): shots made in different places, joined by eyelines and screen direction, read as one place (Wikipedia, "Creative geography", checked 2026-09-27). Every AI-generated scene is built this way, so keep a floor plan per location with the axis drawn on it.

**Reverses, inserts and cutaways** (Section 1) complete the kit. In a film tied to one character's point of view, like *The Catch*, a cutaway to another place breaks that point of view; report the other place through sound instead (rule T6).

### 3.7 Shot/reverse shot: cutting a conversation

Most dialogue scenes are covered in over-the-shoulder shots and singles on both sides of the axis, then cut back and forth. The craft is in *when* to be on whom.

- **Match the two sides.** Matching close-ups use the same lens, a matching camera height and the same distance, so neither person looks bigger or more important by accident (Wikipedia, "Eyeline match"). Break the match only on purpose, to shift power (B1).
- **Move in as pressure rises.** Start in over-the-shoulders or dirty singles (the two are still connected); move to clean singles as the characters separate. Give the first clean close-up to the person the scene belongs to, at its turning point (A2, B1).
- **Be on the listener when the line changes the listener.** The speaker's face shows intent; the listener's face shows effect. If a line lands on someone (A1's landing face), cut to them during the line and let the rest of it run over their face (an L-cut).
- **Cut on the thought, not the sentence.** A cut exactly at the end of each line produces the "tennis match" (Section 13). Better cut points: a look, an intake of breath, a word that hits, the first frame of a reaction.
- **Overlap the words in coverage.** In live action, each setup films the whole exchange so the editor can cut anywhere. The AI equivalent is rule AI7: generate listener clips as silent listening and lay the speaker's audio over them, so every cut point stays movable.
- **Silent beats count as beats.** A2 found that sc13's B6, with no dialogue ("Jude watches her watch it"), explains the later turn at B12; a shot list built from lines alone would drop it.

### 3.8 Continuity of detail across clips

Continuity also means that what is *in* the picture matches from shot to shot: props, wardrobe, wounds, which hand holds what, light direction, weather. Live-action crews keep a script supervisor's log for this. AI clips break it constantly, because each clip is generated fresh. Keep a **continuity log** per scene and check every clip against it before cutting. *The Catch* examples: Eli wears one shoe after sc4 ("She gives Eli one shoe. He leaves the other."); Jude's wound is in his shoulder from sc6 on ("a hole through his shoulder"); Iona presses "what is left of her shirt sleeve" into it in sc7, so from then on one sleeve is gone (and it returns as a key prop in sc21: "The sleeve of her shirt, stiff with Jude's blood."); her palm is skinned from the sill ("Her palm drags across the bright steel", sc6; "her skinned palm opens", sc9); after the turn, rings and handedness are mirrored ("Saye's wedding ring. On her right hand.", sc10). Audiences forgive small mismatches on a cut in movement (Section 3.4), and Murch ranks continuity of space last of his six criteria (Section 4.1); they rarely forgive a wound that changes shoulder.

---

## 4. Theory of the cut: Murch, Kuleshov, Eisenstein and the editors

### 4.1 Walter Murch: the Rule of Six and the blink

Walter Murch edited *The Conversation* (1974), *Apocalypse Now* (1979) and *The English Patient* (1996), was the first person credited as "Sound Designer" (*Apocalypse Now*), and is the only person to win Academy Awards for both editing and sound mixing (Wikipedia, "Walter Murch", checked 2026-09-27). *In the Blink of an Eye* (Silman-James Press; first edition 1995 in most sources, 1992 on Wikipedia; revised 2001) is based on a 1988 lecture.

**The Rule of Six.** An ideal cut "is the one that satisfies all the following six criteria at once". List and weights as quoted from pp. 17–20 of the 1995 edition on a UC Berkeley course page (checked 2026-09-27):

| # | Criterion | Weight | Question to ask of each cut |
|---|---|---|---|
| 1 | "true to the emotion of the moment" | 51% | Does the next shot deliver the feeling this beat needs now? |
| 2 | "it advances the story" | 23% | What does the audience learn from the new shot? |
| 3 | "rhythmically interesting and 'right'" | 10% | Does the duration fit the scene's rhythm plan? |
| 4 | "eye-trace" | 7% | Where is the viewer looking at the last frame, and is the next shot's key subject near there? |
| 5 | "planarity" (the flat screen: axis, stage-line) | 5% | Are left/right relationships consistent? |
| 6 | "three-dimensional continuity of the actual space" | 4% | Would anyone be confused about where people are? |

Emotion "is the thing that you should try to preserve at all costs"; if something must go, "sacrifice your way up, item by item, from the bottom." An emotionally right cut with a small continuity error beats a perfectly matched cut that is emotionally wrong. **Eye-trace** in practice: if the next shot's subject sits where the eye already rests, the cut feels smooth; far away, the eye must search, which costs time and can be used to jolt.

**The blink.** Murch reports that his cut points in *The Conversation* kept falling where Gene Hackman blinked, and argues that a blink marks the end of one thought, as a cut does. He credits the idea to John Huston, who compared looking from one object to another across a room, and blinking between them, to a cut. Treat this as a working metaphor: *cut when the character, or the viewer, has finished taking something in.* **Practical test [judgment, built on Murch's idea]:** play the take and note the frame where you would naturally blink or look away; that frame, or a few frames after a character's own blink, is the first cut point to try. An actor (or an AI face) that blinks constantly gives no such marks; a held, unblinking look reads as intense attention. *The Catch* writes a literal blink into its fall ("Closes her eyes." / "BLACK" / "Her eyes open."), and Worked Example 1 cuts on it.

### 4.2 Kuleshov: the face and what it looks at

In accounts by Lev Kuleshov and Vsevolod Pudovkin, one shot of the actor Ivan Mosjoukine, intercut with soup, a child in a coffin and a woman on a divan, was praised as hunger, grief and desire, though the face never changed. No film of it survives. Prince and Hensley (1992) failed to replicate it; Mobbs and colleagues (2006) and Barratt and colleagues (2016) found the effect; Baranowski and Hecht (2017) found that music alone shifts how a neutral face is read (Wikipedia, "Kuleshov effect", checked 2026-09-27). Hitchcock demonstrated it on his own face in a 1964 CBC *Telescope* interview: kind when cut with a mother and baby, lecherous when cut with a woman in a bikini.

**Consequences:** the shot *before* a reaction tells the audience what the face means; ask for small, open expressions (AI faces tend to over-act); music changes faces too, so keep it off reactions whose meaning should stay open.

### 4.3 Eisenstein's five methods of montage

In Soviet film theory, **montage** means making meaning from the collision of shots. (Elsewhere in this file, "montage sequence" means something narrower: a run of short shots compressing time, Section 5.) Sergei Eisenstein's "Methods of Montage" (1929; in *Film Form*, ed. and trans. Jay Leyda, 1949) names five methods. The summaries follow Wikipedia, "Soviet montage theory" (checked 2026-09-27). Examples marked "Wikipedia" are the clips that page uses; those marked "Eisenstein" are the ones he himself discusses (well-known from the essay; not re-checked against the text in this session).

| Method | What drives the cut | Example | Use in the pipeline when |
|---|---|---|---|
| **Metric** | Shot length alone, counted in frames, whatever is in the shots | Passages in *October* (1928) (Wikipedia) | A pulse the body should feel: a machine, a countdown. |
| **Rhythmic** | Length plus movement inside the frame | The Odessa Steps, *Battleship Potemkin* (1925), where the soldiers' marching feet set the rhythm (Eisenstein); the three-way duel in *The Good, the Bad and the Ugly* (1966) (Wikipedia) | Chases and struggles: cut to feet, wheels, falling things. |
| **Tonal** | The shots' emotional tone (light, shape, mood) | The mourning after the sailor Vakulinchuk's death, *Potemkin*, opening with the harbor in fog (Wikipedia; Eisenstein) | Aftermath and grief: join by mood, not action. |
| **Overtonal** | All of the above together | *The General Line* (1929) (Eisenstein); Pudovkin's *Mother* (1926), workers marching intercut with ice breaking up (Wikipedia) | The film's largest sequences. |
| **Intellectual** | An idea formed by joining two images | *Strike* (1925): attacked workers cut with a slaughtered bull (Wikipedia) | Rarely in realistic films: it announces the director's opinion. Prefer a match cut the story motivates. |

### 4.4 Editors to learn from

- **Dede Allen** (*Bonnie and Clyde*, 1967; *Dog Day Afternoon*, 1975; *Reds*, 1981) brought overlapping sound, jump cuts and abrupt changes of pace into mainstream American film, cutting for a character's inner state; she was the first editor given a solo title card (Wikipedia, "Dede Allen", checked 2026-09-27). **Lesson:** split edits and pace changes can express what is inside a character.
- **Thelma Schoonmaker** has edited every Scorsese film since *Raging Bull* (1980) and won three editing Oscars (*Raging Bull*, *The Aviator*, *The Departed*) (Wikipedia, checked 2026-09-27); Scorsese's films use freeze frames often, *Goodfellas* (1990) among them (Wikipedia, "Freeze-frame shot"). **Lesson:** once a film has taught its grammar, it can stretch or freeze time.
- **Anne V. Coates** won the Oscar for editing *Lawrence of Arabia* (1962) (Wikipedia, checked 2026-09-27), whose famous cut goes from Lawrence blowing out a match to a desert sunrise (well-known; not re-checked). **Lesson:** one cut can join two scales, two times and a breath.
- **Edward Dmytryk**, *On Film Editing* (1984): "Never make a cut without a positive reason" and "When undecided about the exact frame to cut on, cut long rather than short" (chapter 5, checked 2026-09-27); his third is "Whenever possible cut 'in movement'" (Section 3.4). The remaining four, as widely reproduced (wording not re-checked against the book): the "fresh" is preferable to the "stale"; all scenes should begin and end with continuing action; cut for proper values rather than proper "matches" (the meaning of the moment beats a perfect physical match, as with Murch); and substance first, then form. **Lesson for AI:** generate long, cut short; start and end clips inside movement, not on frozen poses.

---

## 5. The transition catalogue

Every transition tells the audience something about time, space or meaning; choose the one whose meaning you want. "Make it" assumes AI clips joined in an editing program. Wikipedia pages cited were checked 2026-09-27; examples marked "well-known" were not re-checked in this session.

| Transition | What it is | What it tells the audience | Use when | Avoid when | Make it |
|---|---|---|---|---|---|
| **Cut** | Shot A stops, shot B starts. | "Same flow of time; look here now." | The default: nearly every join. | Never; just give each a reason (Dmytryk). | Trim. |
| **Match cut: graphic** | Joined because shapes, positions or motions match: the bone that becomes an orbiting satellite in *2001: A Space Odyssey* (1968). Done as a dissolve instead of a cut, it is a **match dissolve**: the drain that dissolves into Marion's eye in *Psycho* (1960) (Wikipedia, "Match cut"). | "These are connected." Often leaps time or scale. | A real object or shape the story gives you. | The link is only clever. | Generate shot B from a start frame composed to match shot A's last frame (C1). |
| **Match cut: action** | A movement begun in one shot ends in another, possibly elsewhere: Cary Grant pulls Eva Marie Saint up Mount Rushmore and, on the cut, into a train berth in *North by Northwest* (1959) (Wikipedia, "Match cut"). | Continuity, or a time leap carried by one gesture. | Invisible joins; elegant ellipses. | Speeds or directions differ. | Both clips contain the full motion. |
| **Match cut: sound** | A sound becomes a similar sound in the next scene: a scream becomes a train whistle in *The 39 Steps* (1935); rotors become a ceiling fan in *Apocalypse Now* (1979) (well-known). | "Connected", or "inside his head". | Carrying a state across scenes. | The sounds are not alike. | Align the sounds; the cut sits on the change. |
| **Jump cut** | Same subject, nearly same position, time skipped. Popularized by *Breathless* (1960), edited with Cécile Decugis (Wikipedia, "Jump cut"). | "Time skipped", "this mind is fractured". | Waiting, nervous searching, breakdown. | You wanted continuity (Section 3.2). | Same framing, different moments. |
| **Smash cut** | An abrupt cut at an unexpected moment to a sharply different scene; its comic form, the "Gilligan cut", goes from a boast to its failure (Wikipedia, "Smash cut"). | Shock, or a joke. | Waking from a nightmare; hard tonal turns. | More than once or twice outside comedy. | Cut on the peak frame with a big level change. |
| **Cross-cutting** | Alternating between actions in different places at the same time. Griffith, its most famous early practitioner, cut rich speculators against a bread line in *A Corner in Wheat* (1909) (Wikipedia, "Cross-cutting"); *The Godfather* (1972) cuts a baptism against murders; *The Silence of the Lambs* (1991) makes two houses seem one (well-known). Many writers use **parallel editing** for the looser case where the alternated threads need not be simultaneous (the past and present stories of *The Godfather Part II*, 1974; well-known); Wikipedia uses the terms interchangeably. | "Meanwhile", "compare", a race. | Threads converging; rescues; irony. | The film is tied to one point of view (rule T6). | Plan both threads; alternate faster as they converge. |
| **Insert / cutaway** | See Section 1. | "Look at this detail" / "something else matters too". | Story-critical objects; a watcher; hiding a gap in time. | The detail is already readable; a cutaway would break a tight point of view. | A separate close clip (macro words in the prompt) / a separate clip. |
| **J-cut** | The next shot's sound starts before its picture. | "Listen: something is coming." | Entering scenes; off-screen threats. | Confusion helps nothing. | Extend B's audio earlier. |
| **L-cut** | The previous shot's sound continues over the next picture. | "The moment isn't over." | Aftermath; listeners; ending on a sound. | A scene needs a clean start. | Extend A's audio later. |
| **Dissolve** | A fades out as B fades in. Usually 1–2 s (24–48 frames); 6–12 frames softens a cut (Wikipedia, "Dissolve"). | Time passed; memory; two things become one. | Long ellipses; dreams. | Inside a continuous scene; in an all-cut film. | Editor effect; match compositions. |
| **Fade out / in** | To black (or white), then up. | A chapter ends; rest. | Act breaks; the end. | Mid-tension (it releases it). | Editor effect; length in frames. |
| **Cut to black** | Instant black, no fade. *The Sopranos*' finale, "Made in America" (2007) (well-known). | Something cut off: consciousness, an ending refused. | Ruptures and hard endings. | Routine scene changes. | Black frames; state frames and what sound does. |
| **Whip pan** | A pan so fast it blurs, used as a join; Chazelle, Edgar Wright and Wes Anderson use it (Wikipedia, "Whip pan"). *Citizen Kane* (1941) passes years of a marriage through breakfasts joined by fast pans (well-known). | Energy; time rushing. | Kinetic scenes; linked places. | Solemn scenes. | Two clips with blur at the join; cut inside the blur. |
| **Wipe** | B pushes A off along a line or shape; Lucas used many in *Star Wars*, after Kurosawa (Wikipedia, "Wipe"). | Storybook; "elsewhere". | Playful, serial tone. | Realistic drama. | Editor effect. |
| **Iris** | Image shrinks to or grows from a circle; silent-era, now mostly homage (non-ironic in Scorsese's "Life Lessons", *New York Stories*, 1989) (Wikipedia, "Iris shot"). | Old cinema; "look at this". | Pastiche; a keyhole or lens. | Realistic drama. | Editor effect. |
| **Freeze frame** | One frame held. Endings of *The 400 Blows* (1959) and *Butch Cassidy and the Sundance Kid* (1969) (Wikipedia, "Freeze-frame shot"). | Time stops: a verdict, a fixed memory. | Endings; a narrator's comment; an in-story pause. | Casually. | Hold a frame. In *The Catch* every freeze is a character pausing a screen in the story (sc13, sc16, sc17); add none of your own. |
| **Montage sequence** | Short shots compressing time, often over music (Wikipedia, "Montage (filmmaking)"); *Up* (2009) compresses a marriage (well-known). | "A lot happened; here is its shape." | Work over days, travel, training. | A turning point is inside it (that needs a scene). | Short clips over one sound or music bed. |
| **Intercut screen / call / recording** | Alternating a character and a screen, the other end of a call, or a recording; or split screen, as in *Pillow Talk* (1959) (well-known). | Two places joined by a device; watching as an act. | Calls, recordings, surveillance (*The Catch* sc13, sc15–16). | The screen can simply be shown in the room. | Generate screen content as its own clip, shape and grade (B1 Section 10). |
| **Time cut** | Leaves out part of a continuous action. | "Nothing important happened in between." | Most scene entrances and exits. | The gap held a beat. | Start clips late, end them early. *The Catch* sc7 to sc8: "Two streets away. Her car, where she left it." |
| **Hidden cut (stitched long take)** | A cut disguised so that two shots read as one unbroken take: the camera passes through a dark foreground, a body crosses the lens, a whip pan blurs, or the frame fills with a wall. *Rope* (1948) hides its cuts in the dark backs of jackets; *Birdman* (2014) and *1917* (2019) stitch many takes into what plays as one or two continuous shots (well-known). | "This is happening in one breath; no time is skipped." | Long unbroken moments that no model can generate in one clip (most clips are 4 to 15 s). | The join object is unmotivated, or the stitched clips drift in face, light or wardrobe. | End clip A on a frame filled by the join object; generate clip B from that frame as its start image (rule AI6); cut inside the fill. |

**Scene-to-scene rule.** Join scenes with a cut, often with a split edit. A dissolve, fade or cut to black is a sentence of its own: use it only where the story has a paragraph break. *The Catch* writes FADE IN once and CUT TO BLACK twice: after Saye's "Nobody leave this room." (just before the title card) and at the very end. These are its only non-cut scene transitions, and the breakdown should not add more.

### 5.1 Reading the text's own editing and sound cues

Screenplays write few transitions: modern practice leaves a plain cut unmarked, so **no transition written means a cut**. Every mark that *is* written is a deliberate instruction. Prose has no marks at all; A2 Step 0 sorts scene from summary, and the table's last rows cover prose.

| In the text | What it means for the breakdown | Spec field |
|---|---|---|
| FADE IN: / FADE OUT. | Picture from / to black over a length you choose (default 24 to 48 frames). | `transition_in` / `transition_out` |
| CUT TO: | A cut the writer wants noticed, often a jump in place or time. Treat as a cut with emphasis (a hard sound change). | `transition_out` |
| SMASH CUT TO: / MATCH CUT TO: / DISSOLVE TO: | The named transition (Section 5). Keep it. | `transition_out` |
| CUT TO BLACK. | Instant black; decide frames and what sound does. | `transition_out` |
| "BLACK." inside action lines | An in-scene black, not a scene change (*The Catch* sc6, sc27). A rupture candidate. | `rupture`, shot row |
| INTERCUT / INTERCUT WITH | Alternate the two places freely (usually a call); plan both sides. | `transition_out: intercut` |
| MONTAGE / SERIES OF SHOTS | A montage sequence; each item is one short shot. | shots list |
| FLASHBACK / BACK TO PRESENT | Time jump; pick a transition whose meaning is "memory" only if the film's grammar allows (T5). | `transition_in/out` |
| (O.S.) | Speaker present, out of frame: off-screen diegetic sound, often de-acousmatized when they enter. *The Catch* sc1: IONA (O.S.), "They all say that.", before she "comes round the cage". | `dialogue.perspective: off-screen` |
| (V.O.) with a parenthetical such as "(in her ear)" or "(over the radio)"; or an extension such as (RECORDED) | A voice not physically present. Read the parenthetical or extension: it gives the perspective (earpiece, radio, playback). | `dialogue.perspective` |
| (PRE-LAP) | The line or sound starts before the cut into its scene: a J-cut. | `split: {type: J}` |
| (beat), "a long moment", "Silence." | A pause; rank and budget them (A1's rule R15; this file's R9). | `duration_s`, `silence` |
| A sound word in CAPITALS in an action line ("METAL SHRIEK", "CLACK", "GUNSHOT", "HUM") | A sound the writer insists on. Capitals also mark a character's first appearance (ELI, THE FIGURE), key props (FLASK, PUCK, ENGINE, VESSEL), text or labels seen on screen (STOP, RECEIVING) and emphasis ("The cage is going UP."): classify each capitalized word as sound, character, prop, on-screen text or emphasis before using it. | `sync_fx` / `offscreen` / `motif` |
| Prose: a line break, section break or "Later" | Usually a scene change; choose a cut or time cut unless the story has a paragraph break (Section 5). | `transition_in` |
| Prose: a summary of repeated or extended time ("For three days...") | A montage sequence or a time cut, not a scene (Worked Example 4). | shots list |
| Prose: a simile or metaphor for an image ("the picture closed like an eye") | Information about feeling, not an instruction to show the compared thing (A1). | none |

---

## 6. Rhythm, suspense, reveals and ruptures: how moments build and break

### 6.1 Shot length and intensity

Shorter shots raise pace; longer shots let the audience settle, search the frame, or squirm (Wikipedia, "Shot (filmmaking)", checked 2026-09-27). For scale: David Bordwell ("Intensified Continuity", *Film Quarterly* 55:3, Spring 2002) reports that between 1930 and 1960 most Hollywood features had 300 to 700 shots and an ASL of "around eight to eleven seconds"; by the 1980s most ordinary films ran five to seven seconds, many four to five; by the late 1990s some films averaged under 3 seconds (exact per-film figures not re-verified in this pass). For comparison, *The Mist* (2007) averages 5.4 seconds, and *Russian Ark* (2002) is a single 96-minute take (Wikipedia, "Shot (filmmaking)").

**House starting values [judgment, not from a source]** for mapping A2's beat intensity (1 to 5) to shot duration in a live-action register. Adjust per film.

| Beat intensity | Typical shot duration | Notes |
|---|---|---|
| 1 (setup, breather) | 5 to 8 s | Room to look; establishing and re-establishing shots live here. |
| 2 | 3.5 to 6 s | Ordinary dialogue coverage. |
| 3 | 2.5 to 4 s | Pressure rising. |
| 4 | 1 to 3 s | Action, or cutting between faces on short lines. |
| 5 (turning point, rupture) | **Either the shortest shot in the scene (under 1 s) or the longest (6 s or more in an ordinary scene; in a fast sequence, at least three times the scene's ASL)** | A peak is an extreme. Action peaks go short; revelation peaks go long (R4). |

A shot must stay up long enough for a first-time viewer to read what it is for. **Minimums [judgment]:** a simple object insert, about 1 second; a face whose expression must be read, about 1.5 seconds; on-screen text the audience must read, about 1 second plus the time to read it at no more than 12 to 15 characters per second (subtitle guidelines allow somewhat faster, but subtitles sit where the eye expects them); mirrored or backwards text, at least double that, because the audience decodes it as the character does (*The Catch* sc7: "Every letter is backwards. / Iona looks at it. Looks again. Says nothing."). Test durations in an **animatic** (storyboard frames or rough clips timed to sound, see C2) by watching once without pausing: if you had to pause to understand a shot, it is too short or its composition is wrong.

### 6.2 Acceleration, deceleration and the scene's rhythm plan

A scene's rhythm is the curve of its shot lengths over time. Three shapes cover most scenes:

1. **Build and cut out:** shots shorten toward the turning point; the scene ends on or just after it. Momentum carries into the next scene.
2. **Build, rupture, aftermath:** shots shorten; at the turning point the pattern breaks (a hold, silence, black); then long shots while the audience absorbs the change.
3. **Slow burn:** long holds throughout, with one short, sharp cut at the turning point (the cut itself is the rupture).

**Choosing the shape.** Use shape 1 if the turning point launches action that continues into the next scene (an escape, a chase, a decision acted on at once). Use shape 2 if the turning point is a loss, a shock or a revelation the characters must absorb before they can act. Use shape 3 if the scene is mostly talk, waiting or watching and its turn is a single line, look or discovery. *The Catch*: sc6 is shape 2 (build, the black, aftermath on faces); sc13 plays mostly as shape 3 (long holds on the recording; the short insert of her thumb on the remote and the freeze are the break); sc5, the corridor fight that runs straight into the cage, is shape 1.

Write the plan before choosing individual durations, for example: "build 4 s to 1.5 s over B1 to B6; rupture at B7 (0.4 s black); aftermath 5 s or more." Physical action can set the curve: in *The Catch* the cage's speed *is* the rhythm (Worked Example 1).

### 6.3 Holding past comfort

A hold past the expected cut turns watching into waiting, and waiting into pressure: *12 Years a Slave* (2013) holds for a very long time on Solomon hanging on tiptoe while life goes on behind him (well-known). McKee (*Dialogue*, ch. 5): "There are no free rests: A pause must be earned." He separates two uses. Before a turning point, a pause "tightens tension" and "dams emotion momentum"; after it, a pause "allows the reader/audience time to absorb the meaning of the change and savor its aftermath." In editing terms: a **pre-turn hold** sits on the person about to act or learn, and ends on the turn; a **post-turn hold** sits on the person the turn has changed (the landing face). And from the same chapter, for screen work: "Silence invites the camera in." Hold only on a face or situation that is still changing, or whose stillness is the point; give it room tone and one small real sound (A1 rule R17).

### 6.4 The reaction shot

The reaction shot is where the audience learns what an event means. Choose the **landing face** (A1) for every turning point: usually whoever the event costs most. Cut to it *after* the event is fully seen, unless the event is being withheld (Section 6.6). A witness reacting to a reaction ("Jude watches her watch it", *The Catch* sc13) makes the moment land twice.

### 6.5 Suspense versus surprise, and the information ledger

Hitchcock to Truffaut (Truffaut, *Hitchcock*, 1967; revised 1984): if a bomb under the table suddenly explodes, "we have given the public fifteen seconds of surprise"; if the public knows the bomb is there and when it will go off, "we have provided them with fifteen minutes of suspense." "The conclusion is that whenever possible the public must be informed", except when the surprise is itself the point of the ending. (Quotation checked against several sources reproducing the revised edition, 2026-09-27.) Hitchcock also said he regretted letting the bomb kill the boy in *Sabotage* (1936), because suspense built that long must be released, not punished (Wikipedia, "Sabotage (1936 film)", checked 2026-09-27).

The pipeline controls suspense with an **information ledger**: for each key fact, who knows it, and when.

| Audience vs character | Effect | Editing consequence |
|---|---|---|
| Audience knows **more** than the character | Suspense (in *Rear Window*, Lisa searches Thorwald's apartment while Jeff, and the audience, watch Thorwald return; well-known) | Show the danger early and clearly; cut between danger and the unaware character; **hold longer**, do not cut faster. |
| Audience knows **the same** | Identification, mystery | Stay with the character's point of view; withhold what they cannot see; reveal with them. |
| Audience knows **less** | Surprise | Withhold; use once, at a big turn; make sure it reads as fair when replayed. |

Editing can also **mislead**, as in *The Silence of the Lambs*' cross-cut raid. Use this only if the payoff rewards the audience rather than cheating them.

**Ticking clocks.** A stated time limit ("Cage is coming. Thirty seconds." in *The Catch* sc4) is an instant suspense device. Decide whether screen time honors it (roughly thirty seconds of screen time until the cage arrives) or stretches it; stretching is legitimate but must be a choice.

### 6.6 Reveals: what to withhold from the frame

A reveal is designed backwards: decide what the audience will finally see, then how each earlier shot keeps it out of view. Tools, mildest first:
1. **Frame edge:** the thing is just outside the frame ("He has one hand she cannot see."). B1 rule: never tilt down to find it.
2. **Focus or darkness:** it is in frame but unreadable.
3. **Obstruction:** a body, a door, the grid.
4. **Timing:** the cut comes a moment before the thing is seen.
5. **Sound first:** the audience hears it before it is shown (acousmatic sound, Section 7.1).
6. **Recorded evidence:** the truth is in a recording watched later (*The Catch* sc13; compare *Blow-Up*, 1966, and the replayed tape in *The Conversation*, 1974; well-known).

At the reveal itself, give a clean, well-lit, well-timed view, then the landing face.

### 6.7 Setup and payoff, planted in picture and sound

Rules for plants:
- **Seen once calmly.** The plant needs one shot where it is clearly visible (or audible) and nothing more urgent competes (eye-trace).
- **Not underlined.** No musical sting, no push-in, unless the film wants the audience to anticipate (suspense).
- **Rhymed at the payoff.** Reuse the plant's framing, lens or sound, so the audience's memory is triggered without dialogue. *The Catch*: the arm on the bright sill in sc2 ("Her arm settles into the shape of the steel") and sc6 ("Her arm knows it before she does"); the tooth that makes no sound in sc2 ("Does not hear it land") and the cage that does in sc6 ("This time they hear it land").
- **Tracked in the spec** under `plants` and `pays_off` (A2 template), with the exact frame or sound to be reused.

### 6.8 How a scene breaks: the rupture

A **rupture** is the film breaking its own current pattern at the moment the story turns. It is a change in *how the film is told* (its cutting, camera, sound treatment or picture), not a loud event *in* the story. A gunshot, a shriek or a crash is action: it gets a synchronized sound and a cut. It becomes a rupture only if the telling also breaks (the sound drops out, the picture goes black, the camera stops shaking). So sc6 contains many violent events but one rupture. The catalogue:

| Rupture device | What breaks | Example |
|---|---|---|
| **Sound drop-out** | Constant sound suddenly thins to muffled or nothing | The Omaha Beach sequence of *Saving Private Ryan* (1998) goes muffled when Miller is stunned (well-known example). *The Catch* sc26: "Her boots on the deck. The sick motor through them. / Then not." |
| **True silence** | Even room tone goes | *The Catch* sc6: "BLACK. A dark with nothing in it. One instant." |
| **Change of camera behavior** | Handheld to still, still to floating (B1's "break") | *The Catch*: the camera is completely still on the ship's ledge when danger is greatest (B1 Section 9.2). |
| **Change of cutting pattern** | Fast cutting stops for a long hold, or a long take is cut by one sharp cut | *The Catch* sc13: the recording stopped on a freeze. |
| **Cut to black** | Picture itself | *The Catch* sc6 and the ending. |
| **Music stops** | Score that has run for a while cuts out mid-phrase | Works only if the film has used score. |
| **Change of point of view** | We leave the character we were tied to | The tablet feed in *The Catch* sc15. |
| **Scale jump** | From wide to extreme close (or reverse) with no step in between | The macro inserts reserved in B1. |

Rules: **one rupture per scene**, placed on the turning point (or on the beat that causes it); **teach the pattern first**, so the break is felt; **follow a rupture with a re-establishing shot** so the audience finds its footing; and **never use two rupture devices at the same moment unless it is the film's biggest moment** (*The Catch* sc6 combines a cut to black and true silence once, for the inversion; that is its budget. The crossings in sc27 rhyme with it but keep her lit gloves in frame, so they are near-black, not a cut to black).

### 6.9 Rhythm across scenes

A film has a rhythm of scenes as well as of shots. Rules [judgment, from common editing practice]:
- **Alternate pressure and release.** After a scene of intensity 5, the next scene should be quieter (a longer ASL, fewer sounds), so the audience can absorb it; two maximum-intensity scenes back to back blur into one.
- **Contrast adjacent ASLs.** The cut between scenes is felt most when the rhythm changes across it: *The Catch* goes from sc6 (ASL about 1.4 s) to sc7, which should open on held shots and "Tell me that was the brake."
- **Let quiet scenes carry dread, not just rest.** sc8 and sc9 (the backwards street and the car) are slow but not relaxed: long holds on wrong details, with ambience that is subtly off (traffic on the wrong side), keep the pressure while the pace drops.
- **Save the film's longest holds and its only true silences for its largest turns** (P10), and check the whole film's list of ruptures before locking any single scene.

---

## 7. Sound as part of the breakdown

### 7.1 Chion's working concepts

Michel Chion, *Audio-Vision: Sound on Screen* (French 1990; English ed. and trans. Claudia Gorbman, foreword by Walter Murch, Columbia University Press 1994; second edition 2019 with a glossary). The acousmêtre comes from his *The Voice in Cinema* (English 1999). Definitions below are paraphrased, not quoted; the last five rows (vococentrism, temporalization, on-the-air sound, materializing sound indices, rendering) are Chion's *Audio-Vision* terms summarized from general knowledge of the book, not re-checked against its text in this session.

| Concept | Meaning | Pipeline use |
|---|---|---|
| **Added value** | Sound changes what we think we see, and we credit the change to the image. | Decide what each key shot's sound must *add* (weight, danger, tenderness). A punch with a heavy thud looks heavier. |
| **Synchresis** | A sound and an image that happen at the same instant fuse, even if unrelated. | Any sound placed exactly on a visual event becomes that event's sound. Use it to give a cut, a flap, a light the sound you want. |
| **Point of synchronization** | A salient instant where sound and image hit together. | Mark one or two per scene: they punctuate like stressed syllables. |
| **Acousmatic sound** | Heard, source unseen. | The strongest suspense tool: the audience imagines the source. |
| **De-acousmatization** | The hidden source is shown, and the sound loses its mystery (and often its power). | Time it as a reveal. Know that showing the source *reduces* fear and can *increase* sympathy. |
| **Acousmêtre** | A character who is a voice without a visible body, credited with seeing all, knowing all and acting anywhere (the powers Chion names). | Use for villains or guardians who should feel omnipresent; strip the powers by showing the body. |
| **Empathetic / anempathetic sound** | Sound or music that matches a scene's emotion / that carries on indifferent to it (a radio playing, a machine running through a tragedy). | Anempathetic sound is often more chilling than a sad score. |
| **Vococentrism** | Film sound is centered on the voice: when a voice is present, the audience attends to it first and hears everything else as background. | Dialogue is the top layer unless it is deliberately masked (Worked Example 4's "You knock loudly"). Never put a key sound effect under an important line. |
| **Temporalization** | Sound gives time to the image: it can make a still or slow shot feel tense, or give an image a sense of heading somewhere. | A static AI shot can be made to feel like it is building by a rising or ticking sound; this is cheaper than camera motion. |
| **On-the-air sound** | Sound in the scene that is transmitted electronically (radio, phone, playback), and so can cross between on-screen, off-screen and the room freely. | Label radio, phone and recorded voices as on-the-air and give them a device perspective: Jude "(in her ear)", Eli "(over the radio)", "SAYE (RECORDED)". |
| **Materializing sound indices** | Small sound details that make the physical source concrete: breath, friction, creaks, a voice's mouth sounds. Many such details make a sound feel bodily; few make it abstract. | Add them where the film wants the body felt (Iona's palm "drags across the bright steel"); strip them where it wants distance (the silent security footage). |
| **Rendering** | Film sound is judged by whether it conveys the *feeling* of the event (weight, speed, danger), not by whether it is a faithful recording. | Specify the sensation a sound must render ("the cage lands far below, late, heavy, final"), not only its source. |

### 7.2 Diegetic and non-diegetic, on-screen and off-screen

Every sound in the spec gets two labels: **diegetic or non-diegetic**, and, if diegetic, **on-screen or off-screen**. A third label, **perspective**, says where the listener is: close, far, through a wall, through a radio, inside a helmet. *The Catch* has an in-between case: "JUDE (V.O.) (in her ear)" is diegetic (a radio earpiece) but heard as Iona hears it: close, narrow in frequency, dry. Write that, not just "V.O.".

**Off-screen sound widens the world.** *The Catch* sc2: "Gates go by with lines of light under them. Behind one, a radio, far off. Behind the next, nothing." The radio makes a whole building of unseen people; the "nothing" behind the next gate makes it empty again. Sc3: "Far below, a motor wakes." tells the audience Jude has started the cage without a cut to him. Off-screen sound is also cheap: it adds space without adding shots to generate. McKee makes the same point about the camera (*Dialogue*, ch. 16): as it moves through a scene "we become aware of life offscreen as well as onscreen. As a result, we often imagine actions and reactions we do not in fact see."

### 7.3 Layers, room tone and sound bridges

Build every scene's sound in four layers: **dialogue**, **synchronized effects** (sounds tied to on-screen actions), **ambience bed**, **music**. Murch's essay "Dense Clarity, Clear Density" (Transom, 1 April 2005, checked 2026-09-27) sets two limits. First, audiences follow "not quite three layers" of *similar* sounds at once, his "Law of Two-and-a-half". He found it syncing robot footsteps for *THX 1138*: one or two robots' steps had to be in sync, but with three "*nothing* had to be in sync". Practical use: sounds from three or more similar sources, such as a crowd's footsteps, need no frame-accurate sync, which saves AI sound work. Second, at most five layers can be heard clearly in any five-second moment, and only when they spread across the spectrum from "encoded" sound (speech, carrying meaning) to "embodied" sound (music, carrying feeling). The same essay describes **worldizing**: re-recording a sound through a speaker in a real space so it takes on that space's acoustics. **Rule:** at every moment, name the one sound the audience must hear and keep the rest below it.

**Room tone is never optional.** Where a scene is "silent", specify its room tone (rain in the brickwork, hospital air handling, ship hum). **Ambience across cuts:** run one bed under all the shots of a location, so cuts do not make the background jump; change it only when the location or the story's state changes.

**Sound bridges** do three jobs: a J-cut into a scene pulls the audience forward; an L-cut out of a scene lets a moment resonate; a matched sound (Section 5) links two places. Dede Allen made overlapping sound a signature (Section 4.4); Barry Salt's count of 33 American films found J-cuts rising in recent decades to roughly equal L-cuts, though he cautions that the sample is too small to prove a trend (Wikipedia, "Split edit", checked 2026-09-27). Screenplays mark a scripted J-cut as (PRE-LAP).

### 7.4 Sound motifs

A **sound motif** keeps its identity (rhythm, basic timbre) while its perspective, level, context and synchronization change with the story. John Williams's two-note theme in *Jaws* (1975) is the classic audible sign of an unseen threat (well-known). To build one:
1. **Find it in the text.** Screenplays repeat exact phrases or capitals: *The Catch* has "three strokes, not quite even" / "Three uneven strokes", the engine's "CLICK" and "CLACK", the ship's "HUM".
2. **Fix its signature** so every statement is the same sound, for example "stroke, 0.45 s, stroke, 0.6 s, stroke, 1.2 s rest" (a judgment; any fixed uneven pattern works). One asset file, reused, beats regenerating it.
3. **State it clearly the first time,** so later muffled or partial statements are recognized.
4. **Map every occurrence** (scene, perspective, source visible or not, meaning now), as in Worked Example 3.
5. **Ration it,** or it becomes wallpaper.

### 7.5 Silence

Silence is relative: it is heard because of what came before. Three grades: **quiet** (room tone plus one small sound), **drop-out** (the bed suddenly thins: a rupture), **true silence** (digital zero: the break of breaks, once or twice a film). *The Birds* (1963) has no conventional score, and *No Country for Old Men* (2007) a famously sparse one; both make ordinary sounds loud with dread (well-known).

### 7.6 Music and spotting

**Spotting** is deciding, against the edited picture, where each music cue starts and stops and what it must do. Per cue write: ID, in-point, out-point, function, and a "must not" line (usually: must not state the subtext, meaning what a character feels or means but does not say; A1). Rules: enter on a motion or cut, not mid-line; exit before or exactly on a rupture (music that stops suddenly *is* a rupture); no music under reveals whose meaning should stay open (Section 4.2); set the film's music policy once (full score, sparse, source music only, or none); spot after picture lock, except for sequences cut to music. *The Catch*'s sound world of pump, hum and click suggests sparse score or none, so the pump can be the film's heartbeat.

### 7.7 Voice-over

**Voice-over** is speech laid over the picture by a voice not speaking in the scene: a narrator looking back, inner thoughts, a letter read aloud, or a device (radio, recording). In prose adaptations it is the obvious way to keep the narrator and usually the wrong one when it describes what the picture already shows. McKee (*Dialogue*, ch. 2) warns that voice-over "cannot mete out exposition with the intellectual power and emotional impact of fully dramatized dialogue", except rarely. Use it where the words add what the picture cannot. McKee (ch. 1) names the two screen modes for a character speaking outside a dramatized scene: voice-over over images, or speaking direct to camera. His example of the second is a letter in Bergman's *Winter Light* (1963): as the ex-lover picks it up to read, "Bergman cuts to her face in close-up as she speaks the letter, eyes direct to camera, for six uninterrupted minutes." So a letter has three options: the reader's voice over the reader's images, the writer's voice over the reader's images, or the writer speaking it to camera. *The Long Places* opens each chapter with an italic letter ("*To the one who keeps the lamps after me:*"): a strong candidate for voice-over over lamp-keeping images, because it speaks across time to someone absent. Keep it off the investigation scenes, so the two registers stay distinct.

### 7.8 Writing sound so a model or a sound designer can use it

**Audio-capable models.** Native audio is now standard in hosted video models (C1). Google's Veo documentation ("Generate videos with Veo 3.1 in Gemini API", https://ai.google.dev/gemini-api/docs/veo, checked 2026-09-27), under "Prompting for audio": "Use quotes for specific speech"; for sound effects, "Explicitly describe sounds"; for ambient noise, "Describe the environment's soundscape". Its example puts speaker and delivery before quoted lines ("Man: (Hand on his hunting knife) "That's no ordinary bear.""). It also warns that when extending a clip, "voice is not able to be effectively extended if it's not present in the last 1 second of video", and that only English is fully supported. The same page lists Veo 3.1 clip lengths of 4, 6 and 8 seconds at 24 frames per second, which sets the arithmetic below. OpenAI's Sora 2 API was removed on 24 September 2026 (C1), so write sound specs any model, or a person, can use.

**Fitting dialogue into clips.** Conversational English runs at roughly 2.5 words per second (about 150 words a minute; a common rule of thumb). An 8-second clip, less about a second of lead-in and tail, holds a line of about 15 to 17 words. **If** a line is longer, **then** split it at a phrase boundary across two clips and hide the join with a cut to the listener (the speaker's audio continues as an L-cut), **because** a clip cannot hold it and a join inside one continuous face shot shows. Voices regenerated in separate clips can drift in timbre; for a character who speaks across many clips, use one fixed voice (a voice model or recorded actor) plus lip-sync, as the table below says.

**Where each sound should come from [judgment]:**

| Element | Best source | Why |
|---|---|---|
| Lip-synced dialogue | Model native audio, or a voice model plus lip-sync (a tool that re-times a face's mouth to a given audio track) | Sync is hard to add later. |
| Tight synchronized effects | Native audio, checked; replace if weak | Aligned to the model's own picture. |
| Ambience beds | Built once per location in the edit | Native ambience differs clip to clip. |
| Sound motifs | One fixed asset; some models accept audio references (C1: Seedance 2.x, Wan 3.0, MiniMax H3), or add in the edit | Must be identical each time. |
| Off-screen and acousmatic sound | Built in the edit | Often absent from the clip's picture. |
| Music | Composed or generated after picture lock | Must fit final timing. |
| Silence, drop-outs | Made in the edit by removing native audio | Models tend to fill silence. |

**The sound line inside a prompt** follows the documentation's order: picture first; then dialogue in quotes with speaker and delivery; then "SFX:" items tied to actions; then "Ambience:"; then "No music." if none. Keep it to what happens *inside that clip*: J-cuts, L-cuts and motifs belong in the spec's edit fields, not the prompt. For a **listener clip** (a face hearing someone else's line), write "listening, does not speak" and no quoted dialogue, then strip its audio and lay the speaker's line over it in the edit (rule AI7); a model given the other person's line may make the listener mouth it or give the line to the wrong face [judgment: a common failure; check every take]. Worked sound line for *The Catch* sc6, shot 2 (the insert of the elbow on STOP): `Close on a woman's elbow driving into a steel STOP button on an old freight-lift control box. SFX: a heavy button clunk on impact; cage motor whine; loose grid rattling. Ambience: brick shaft, echo. No music. No dialogue.` The motor and rattle will be replaced by the scene's bed in the edit (AI4); asking for them keeps the model from inventing something else.

---

## 8. Translation table: story meaning to editing and sound choices

| Story meaning | Cutting and rhythm | Transition | Sound |
|---|---|---|---|
| Continuous action; nothing should feel edited | Cut on action; keep the axis and screen direction | Cut | One ambience bed across the cuts |
| A character notices something | Look, object, reaction; hold the reaction | Cut | The object's sound may lead (J-cut) |
| Rising pressure | Shorten shots; tighten sizes; alternate faster | Cut | Add a layer; raise the bed; a clock if there is one |
| Dread: audience knows the danger, the character does not | Show the danger early; **longer** holds on the unaware character | Cross-cut, if the point of view allows | An off-screen sound only the audience can place |
| Shock | Withhold, then the shortest shot in the scene | Smash cut | Loud synchronized sound on the frame, then quiet |
| A moment that must be felt fully | Hold past comfort | None: stay | Room tone and one small sound; no music |
| Realization, an inner turn | Hold on the landing face; cut when the thought completes (the blink) | Cut | Sound narrows to one element (subjective) |
| A short gap in time | Start late, end early | Time cut or jump cut | Ambience continuous or changed to mark the gap |
| A long gap in time | Montage sequence, or a single ellipsis | Dissolve or fade | Sound bridge from the earlier time |
| Two actions at once, a race | Alternate; shorten the alternation toward the meeting | Cross-cutting | Each thread keeps its own sound; merge them at the meeting |
| Comparison, theme | Pair two images by shape or motion | Match cut (graphic) | A matched sound across the cut |
| Disorientation, a world wrong | Deliberate axis crossing, reversed screen direction | Jump cut, or a cut to a repeated framing | Sound direction reversed, or sound from the wrong place |
| Momentum into the next scene | End on a question, not an answer | J-cut | Next scene's sound leads |
| Aftermath, resonance | A long hold on the listener, not the speaker | L-cut | The last sound trails over the new picture |
| Something cut off: loss of consciousness, an ending refused | Stop on the peak frame | Cut to black | Sound stops with the picture, or continues alone |
| Closure, rest | Slow the last shots | Fade out | Let the bed fade with the picture |
| An unseen threat | Keep the source out of frame; faces listening | J-cut | Acousmatic sound, placed in space (behind, above) |
| Threat revealed as vulnerable | Show the source in close detail | Cut | De-acousmatize: sync the sound to its visible source |
| Recurring meaning, theme | Repeat a framing at each occurrence | Same transition each time | Sound motif, identity fixed, perspective changing |
| Loss of control | Break the established cutting pattern | Cut | Drop-out, or the bed is torn away |
| Numbness, shock after violence | Longer holds; fewer cuts | Cut | Muffled or thinned sound; ringing |
| The world indifferent to grief | Hold wide | Cut | Anempathetic sound: a machine, a radio carries on |
| Intimacy | Fewer cuts; both people in one frame | Cut | Close perspective; breath; low ambience |
| Isolation, vastness | Wide, long holds | Cut or dissolve | Distant off-screen sounds; thin ambience |
| Truth from recorded evidence | Let the recording run in real time; freeze it; reaction | Diegetic freeze frame | The recording's own sound (or none); the room's small sounds |
| Comic deflation | Cut straight to the failure | Smash cut | A hard change of level |

---

## 9. Decision rules

Each rule reads "If ... then consider ... because ...". **"Consider" means: do this by default; if you do not, write one line in the shot's or scene's `notes` saying why.** When two rules conflict, apply them in this order: the text's own marks (Section 5.1), then emotion (R1), then the information ledger (S rules), then everything else. Rules are grouped by task; the code (C, R, S, T, SND, AI) is for cross-reference.

### Continuity (C)
- **C1.** If a scene has two characters facing each other, then consider drawing its axis on the floor plan before choosing any shot, because every single and reverse must sit on one side of it.
- **C2.** If the story needs the axis crossed, then consider a visible camera move across it, a buffer shot on it, or a character crossing it, because an unexplained crossing reads as an error.
- **C3.** If you want the audience disoriented at a turning point, then consider crossing the axis or reversing screen direction *exactly on that beat*, because the disorientation then belongs to the story.
- **C4.** If two consecutive shots show the same subject, then consider changing the angle by at least 30 degrees or the size by at least one step on B1's shot-size ladder, because smaller changes read as jump cuts.
- **C5.** If a journey spans several scenes, then consider fixing its screen direction and writing it into every prompt, because models do not carry direction from clip to clip.
- **C6.** If a spatial relationship will matter in a fast moment later, then consider showing it once calmly beforehand, because the audience cannot learn geography under pressure.
- **C7.** If a character, prop, wound or piece of wardrobe appears in more than one clip, then consider writing its exact state into the scene's continuity log and into every prompt that shows it (which hand, which shoulder, which sleeve), because each clip is generated fresh and does not remember the last one (Section 3.8).
- **C8.** If a conversation is cut between two people, then consider matching lens, camera height and distance on both sides and moving from over-the-shoulders to clean singles only as the conflict separates them, because unmatched singles make one person look bigger by accident (Section 3.7).

### Cut points and rhythm (R)
- **R1.** If two cuts both work, then consider the one that better serves the emotion of the moment, even at a small cost in continuity, because Murch weights emotion at 51 percent.
- **R2.** If you cannot decide where to cut, then consider cutting later (Dmytryk: "cut long rather than short"), because a long shot can be trimmed but a short one cannot be extended; for AI, generate with handles.
- **R3.** If a movement crosses a cut, then consider cutting in the middle of the movement and having both clips contain the whole movement, because the motion hides the join.
- **R4.** If a scene has a turning point, then consider making its shot there the scene's shortest or longest, because a peak must be an extreme. Choose which by the kind of turn: **shortest** if it is a physical event (an impact, a blow, a shot, a fall, a black); **longest** if it is a realization, a decision, a revelation or a refusal. If one turning point is both (sc6: the CLACK, then her eyes open on a wrong world), give the event the shortest shot and hold the realization after it longer than its neighbors (Worked Example 1: 10 frames of black, then "The cage is going UP." held at 1.5 s between 0.8 s and 1.2 s shots).
- **R5.** If shots have been shortening, then consider a hold on the turning point or just after it, because a hold after acceleration is the simplest rupture.
- **R6.** If a character states a time limit, then consider making screen time honor it, or stretching it on purpose and recording why, because the audience keeps count.
- **R7.** If a reaction shot follows an event, then consider cutting to it after the event is fully seen, because a reaction to something not yet seen is confusing unless the withholding is deliberate.
- **R8.** If a shot must be read (text, a small object, a face's change), then consider giving it at least the minimum duration in Section 6.1, doubled for mirrored text, because a shot the audience cannot read in one viewing has no effect.
- **R9.** If the text marks a pause (A1's ranking), then consider placing a pre-turn pause on the person about to act and a post-turn pause on the person the turn has changed, because McKee's two kinds of pause do different jobs (Section 6.3).

### Suspense and information (S)
- **S1.** If a scene could be played as surprise or as suspense, then consider suspense (inform the audience early), because "whenever possible the public must be informed" (Hitchcock).
- **S2.** If the audience knows the danger, then consider longer holds on the unaware character, not faster cutting, because suspense is waiting.
- **S3.** If a reveal comes later, then consider designing every earlier shot backwards from it and listing how each shot withholds it, because one accidental glimpse spoils it.
- **S4.** If the audience has been given clues, then consider playing the reveal as confirmation (real time, clear view, landing face) rather than as a shock, because they are waiting for it.
- **S5.** If a plant is essential, then consider one clear, calm shot of it and a matched framing or sound at the payoff, because rhymes trigger memory without dialogue.
- **S6.** If a suspense build ends, then consider releasing it in a way the audience accepts, because Hitchcock regretted punishing suspense in *Sabotage*.

### Transitions (T)
- **T1.** If the next scene continues in time and place, then consider a plain cut, often with a J- or L-cut, because effects imply gaps.
- **T2.** If time passes between scenes, then consider a time cut for minutes, a dissolve or fade for days or years, and a montage when the passage itself is the content, because each device tells the audience a different size of gap. Exception: if the script uses only cuts (T5; *The Catch*), mark even large gaps with a cut plus a clear change of light and ambience (NIGHT to BEFORE DAWN to MORNING), because the script's own grammar outranks this rule.
- **T3.** If two scenes share a shape, motion or sound that the story motivates, then consider a match cut, because it links meaning without words.
- **T4.** If a scene should end unresolved or be cut off, then consider a cut to black, stating its length in frames and what the sound does, because a cut to black stops a scene instead of closing it.
- **T5.** If a film has used only cuts, then consider not introducing wipes, irises or dissolves late, because a new device reads as a change of style.
- **T6.** If the film is tied to one character's point of view and something happens elsewhere, then consider telling it through sound (a radio, an off-screen noise) instead of cross-cutting, because cross-cutting breaks the point of view and changes the information ledger.

### Sound (SND)
- **SND1.** If a threat should grow, then consider hearing it before seeing it, placed in space (behind, above, below), because acousmatic sound lets the audience imagine the worst.
- **SND2.** If a threat should become pitiable, then consider showing its source and synchronizing the sound to it, because de-acousmatization strips a sound of its power.
- **SND3.** If a sound recurs in the text, then consider making it a motif with one fixed asset and an occurrence table, because identical statements build meaning.
- **SND4.** If a scene is "silent", then consider specifying room tone and one small sound, and reserving true silence for a rupture, because dead silence reads as a fault.
- **SND5.** If a moment's meaning should stay open, then consider no music, because music tells the audience how to read faces.
- **SND6.** If a scene should pull the audience forward, then consider a J-cut, and if a moment should resonate, an L-cut, because sound that leads makes the audience lean toward what comes next and sound that trails keeps the last moment alive.
- **SND7.** If several sounds compete, then consider naming the one the audience must hear and keeping the rest below it, because audiences follow only about two and a half similar layers (Murch).
- **SND8.** If a film ends on a sound, then consider never cutting it off mid-pattern, because an abruptly stopped heartbeat or pulse reads as a death.

### AI production (AI)
- **AI1.** If a shot will be cut, then consider generating 0.5 to 1 second of handles at each end [judgment], because cut points are found in the edit.
- **AI2.** If a transition is not a cut, then consider building it in the editing program, not asking the generator for it, because models make clips, not edits; the exception is a join prepared with start-frame control (giving the model an image to use as the clip's first frame), as for a graphic match or a hidden cut (AI6); even then the cut itself is made in the edit.
- **AI3.** If a clip is flipped horizontally, then consider its screen directions, text and handedness reversed, because flipping crosses the axis for everything in it.
- **AI4.** If sound must match across cuts, then consider replacing each clip's native ambience with one bed, because native audio differs clip to clip.
- **AI5.** If a line of dialogue will not fit in one clip with a second of lead-in and tail (about 15 to 17 words in an 8-second clip), then consider splitting it at a phrase boundary and covering the join with the listener, because a join inside one continuous face shot shows (Section 7.8).
- **AI6.** If two clips must join invisibly (a match on action, a hidden cut, a graphic match), then consider generating clip B with a frame from clip A at the cut point as its start image, where the model supports start frames (C1), because a shared frame is the most reliable way to make two independent generations meet.
- **AI7.** If a shot shows a character listening to another's line, then consider generating it with "listening, does not speak" and no quoted dialogue, stripping its audio, and laying the speaker's line over it, because that keeps every dialogue cut point movable and prevents the listener's lips from moving.

---

## 10. The spec: edit and sound fields

These fields extend A2's scene template. Scene-level fields go once per scene; shot-level fields go inside each entry of A2's `shots:` list (A2 already has `duration_s`). Fields marked `(opt)` may be blank.

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

**Filled example** (the first two rows of Worked Example 1, abridged):

```yaml
- id: sc6.S2
  duration_s: 0.6
  handles_s: 0.75
  clip_length_s: 4
  cut_in_on: action
  cut_out_on: sound hit
  overlap_action: "the full elbow strike on STOP, from wind-up to rebound"
  start_frame_from: "sc6.S1, frame where the elbow begins to move"
  screen_direction: static
  transition_out: cut
  continuity: "behind the control box: Jude shot through the shoulder, Eli's arm round his chest, Eli's other hand hidden behind Jude's back; Eli in one shoe"
  sound:
    sync_fx: [{what: "button clunk", at_s: 0.2}]
    ambience: "AMB_SHAFT_MOVING; full level"
    silence: none
    point_of_sync: "elbow hits STOP, 0.2 s"
    model_audio: strip all
    prompt_sound_line: 'SFX: a heavy button clunk on impact; cage motor whine. Ambience: brick shaft, echo. No music. No dialogue.'
```

---

## 11. Worked examples

Scene numbers follow A2 (sc1 is the loading tunnel; sc6 the freight cage; sc13 the glass partition; sc30 the last scene). Durations are judgments for a first cut, meant to be tested in an animatic.

### Worked example 1. The cage fall and inversion (*The Catch*, sc6)

**From** "Iona hits STOP with her elbow." **to** "This time they hear it land."

**What the sequence must do.** The value is life or death for all three, with a hidden question underneath (Eli's hand). Four plants pay off and one is planted: Iona's sc1 warning, "Stop it hard and there's nothing under it to catch us"; the yellow stripe (sc2: "A band of yellow paint circles the whole shaft at head height. She passes it."); the bright sill (sc2: "Her arm settles into the shape of the steel"); the tooth (sc2: "Spits into the dark. Does not hear it land."); and, for sc13, "He has one hand she cannot see." B1 fixes the camera: bolted in the cage, one dip on the stop, no shake in the fall, repeated framings across the black.

**Rhythm plan.** Build → false relief (first long hold) → fall (short shots, with its longest hold on Eli) → rupture (CLACK, 10 frames of black, true silence) → disorientation (repeated framings, reversed direction) → deceleration (shots lengthen as the rising cage slows, like a ball at the top of a throw) → escape → aftermath (the longest shot, on faces, waiting for a sound). About 36 shots in about 50 seconds (the durations below sum to 49.7 s): ASL about 1.4 seconds. Rows that hold two or three shots are numbered as ranges.

| # | Exact text | Shot and cut | s | Sound |
|---|---|---|---|---|
| 1 | "The opening reaches them." | In the cage, 24 mm; the opening's lit edge enters the gate frame. Cut on the start of the elbow strike. | 1.5 | Motor whine, grid rattle, a shot from above. |
| 2 | "Iona hits STOP with her elbow." | Insert: elbow on STOP. Both clips hold the full strike. | 0.6 | Button clunk (point of synchronization). |
| 3 | "The cage STOPS DEAD." | Wide; the image dips a hand's width, recovers (B1). | 1.2 | Bang; the motor cuts out. |
| 4 | "Iona is thrown flat on the grid." | Close: cheek on the grid. | 0.8 | Body on steel; Jude's breath. |
| 5 | "the bright sill is almost level with the floor. A passage. A way out." | Her point of view to the sill. **First long hold: false relief.** | 3.0 | Creaks; a slow tick of stressed metal above. |
| 6 | "She reaches for the latch." | Her hand toward the latch. | 1.5 | **J-cut:** the shriek starts here, from above. |
| 7 | "one long METAL SHRIEK and lets go of the wall." | Three faces turn up. The source is never shown. | 1.5 | Shriek (acousmatic); it snaps off. |
| 8 | "The cage falls." | Shot 3's framing; bodies lift; the wall streams upward, faster. | 1.8 | Mechanical sound stops (nothing touches the cage); an air roar through the grid rises. |
| 9 | "Her body floats out behind her like washing." | Medium: fingers in the grid, body trailing. | 2.0 | Roar; cloth flapping. |
| 10 | "Jude's blood lifts off the steel in round red beads ... turning." | Macro, held: a calm, almost beautiful image inside a catastrophe. | 2.0 | Nothing added. |
| 11 | "Through the grid, the opening flicks past. Going up." | Point of view through the cage's side mesh: the opening's bright edge streaks upward out of frame (it is beside and then above them, so not through the floor). | 0.6 | A whoosh. |
| 12 | "Through the grid, the yellow stripe. Coming." | Point of view down; stripe small. | 0.9 | Roar rising in pitch. |
| 13 | "Io." / "He has one hand she cannot see." | Eli close single; one arm leaves the frame bottom (B1). **Held about three times as long as the shots either side of it: the longest shot in the fall.** | 2.5 | "Io." dry and close, over the roar. |
| 14 | "Her grip begins to slip." | Insert: fingers sliding. | 0.7 | Metal squeak. |
| 15 | (the stripe) | Shot 12's framing; stripe larger. | 0.5 | Roar at its peak. |
| 16 | "Closes her eyes." | Close on her face. **Cut on the eyelids closing.** | 1.0 | Roar. |
| 17 | "A hard metal CLACK." / "BLACK. A dark with nothing in it. One instant." | Cut to black for **10 frames**; the CLACK sits on the first black frame. | 0.4 | CLACK, then **true silence**. |
| 18 | "Her eyes open." | Extreme close. | 0.7 | All sound back at once; the roar now falling in pitch. |
| 19–21 | "The floor grid is above her" / "The yellow stripe is under her boots, getting smaller." / "The brick slides past the wrong way." | Repeats of shots 8, 12 and the grid-and-wall framing; **the wall now streams downward.** | 1.3, 0.9, 0.8 | Roar. |
| 22 | "The cage is going UP." | Wide, held. From here the world is mirrored (B1's "phase B", its name for everything after the turn); the opening approaches from the other side of frame. | 1.5 | |
| 23 | "Jude lies across Eli's arms. The gate has sprung open." | Medium. | 1.2 | Gate banging loose. |
| 24–25 | "Iona sees them together ... the tall maintenance opening. Slower now." | Her look, then her point of view. **Shots lengthen from here.** | 1.0, 2.2 | Roar thinning; creaks return. |
| 26–28 | "Lets go of the grid." / "Push." / "They go sideways together." | Medium; close on "Push."; wide, cut on the push. | 2.0, 0.8, 1.4 | Grunts; the one word, clean. |
| 29–30 | "The sill comes down into reach." / "Her arm knows it before she does." | Point of view; then an insert with **the same lens and angle as the sc2 arm-on-sill shot.** | 0.9, 1.4 | Palm dragging on steel: the sharpest close sound of the sequence. |
| 31–32 | "Her body is already through." / "The cage checks. Starts down." | Medium from the passage; wide on the cage. | 1.2, 1.0 | One creak at the top; the rattle returns. |
| 33 | "Jude's boot clears the gate frame." | Insert. **Do not cut before it clears.** | 1.0 | Boot scraping the edge. |
| 34–35 | "Iona's knees hit concrete." / "Its red tag whips against the upside-down gate." | Medium; then point of view down the shaft, tag unreadable. | 1.5, 1.4 | Bodies on concrete; rattle receding downward. |
| 36 | "This time they hear it land." | Three faces in the passage, held: **the longest shot of the sequence.** | 5.0 | About 2.5 s of shaft air and breath (the audience counts, as with the tooth); then the crash, distant, late; a long decay (the sound's echoing fade after the hit). **L-cut:** the decay runs under sc7's first shot and "Tell me that was the brake." |

**Why.**
- **Two holds carry memory.** Shot 5's false relief makes the shriek hurt. Shot 13 is the longest shot in the fall (the blood macro before it is held too, but for beauty, not information), so the hidden hand is remembered when sc13 plays the recording.
- **The rupture is a blink.** Cutting on the closing eyelids and landing the CLACK on the first black frame (synchresis makes the cut itself the event) makes the audience blink with Iona. Ten frames is a judgment: long enough to register as black and silence, short enough not to read as a scene ending. It is the film's one combination of cut to black and true silence inside a scene.
- **Direction and repetition tell the turn.** Shots 19–21 repeat earlier framings with the wall's direction reversed, so the audience reads "UP" before the text says it (B1: "Across a turn, repeat the framing").
- **Physics sets the rhythm.** Cuts quicken as the cage falls faster and slow as the rising cage nears its top; the escape happens in that slow window.
- **Sound says what the cage is touching.** Motor and rattle mean guided travel; their absence means free fall; the roar's pitch means faster or slower.
- **"This time" is a sound payoff, so the picture stays on faces.** It only works if sc2 gives the tooth a clear listening hold with no impact sound.

**AI production.** One clip per shot (rows numbered as ranges hold two or three shots), with handles. The black, CLACK, shriek, roar and crash are built in the edit from fixed assets (the CLACK becomes the engine motif; Worked Example 3). Keep the *used* part of free-fall clips under 3 seconds (generate at the model's shortest length and trim), because floating bodies and hanging liquid are where current models make physics errors (C1), and strip their native audio.

### Worked example 2. The recording playback reveal (*The Catch*, sc13)

**The moment:** "And in the long second of the fall, Eli's hand comes out from behind Jude's back. / Empty. / On the floor of the cage, where his hand was, a flat black puck is clipped to the grid. / Iona pauses the recording with the remote. Looks at her brother. Not at Jude."

**Information ledger going in.**

| Fact | Where the audience got it | Who in the room knows |
|---|---|---|
| Eli's hand was hidden before and during the fall | sc6: "Behind Jude's back. Out of sight."; "He has one hand she cannot see." | Eli |
| The puck is gone from the flask | sc7: "The clip under it is empty. / Iona sees the empty clip." | Eli, Iona |
| Eli expected the mirrored world | sc9: "He looks at it the way you look at a result you expected." | Eli |
| The puck is an engine | sc12: "a small ENGINE, the same flat black as the puck. / Iona looks at it. Then at Eli. He does not look back." | Eli; Iona suspects; whether Saye knows this puck was fired is not shown |

The audience arrives *suspecting*, so the recording plays as **suspense and confirmation**, not surprise (rule S4). The question is not "what happened?" but "when will she see it, and what will she do?"

**Choices.**
1. **The footage is silent** (a judgment: plausible for an overhead security camera, and useful). In sc6 the fall was a roar; now it is mute evidence. The room carries the sound: a faint monitor hum, Jude's breathing, the remote's click.
2. **Real time.** In sc6 the fall, from "The cage falls." to the CLACK, runs about 12 seconds of screen time (subjective, expanded). The recording shows "the long second" it really took, which tells the audience how stretched sc6 was and how little time Eli had to decide.
3. **Stack the looking.** Footage (her elbow hits STOP) → Iona's face in monitor light → "Jude watches her watch it" (A2, B6). The moment lands three times without a word. Keep Iona's face small; the Kuleshov effect gives it meaning from the footage before it.
4. **Design the footage for eye-trace.** The fall pulls the eye downward; put Eli's hand and the puck in that path, the puck the darkest shape on the bright grid (B1 Section 10.4). Hold the footage full-frame through "Empty." and the puck, *then* cut to her face, so the audience finds it a fraction before she reacts. Her face is the landing face.
5. **A diegetic freeze.** Insert: thumb on the remote; the click is the point of synchronization; the footage freezes, held about 2.5 seconds full-frame in room tone only, and then stays frozen on the monitor in the background of the shots that follow, until she "Lets the recording run", so it is the scene's longest-held image. Every freeze frame in the film is one a character makes: here, again in sc16 ("Iona runs the picture back. Stops it on the hand under his arm.") and in sc17 ("Saye stops the picture."). No editor's freeze is added anywhere, so each freeze reads as that character's verdict, not a flourish.
6. **The eyeline is the beat.** "Looks at her brother. Not at Jude." One held shot, Jude soft in the foreground, her head turn visibly passing him before landing on Eli.
7. **The silent impact.** Later she "Lets the recording run. / On the screen the upside-down cage falls empty. All three of them flinch at the same moment." No crash: they flinch at a silent image because they remember the sound. Adding the sc6 crash here would be on-the-nose. Use one three-shot: simultaneity needs one frame (A2).
8. **Switch-off.** "Jude takes the remote and switches it off." The hum stops with the picture, a small drop-out that closes the scene; A2's graphic match to the lit tablet in sc14 then opens on near-silence.

**Rhythm.** Dialogue before the recording runs about 3 to 4 seconds per shot; the recording passage slows to 4 to 6; the freeze is the scene's longest-held image; the confession returns to short singles. Compare sc6's ASL of about 1.4 seconds: the same event at roughly three to four times the shot length.

### Worked example 3. The pump motif and the ending (*The Catch*, sc15 to sc30)

**The motif** (the "three uneven strokes"), traced through every occurrence. One sound asset, one fixed signature; only perspective, level and synchronization change.

| Scene | Exact text | Perspective and source | What it means now |
|---|---|---|---|
| sc15 | "From inside it, a PUMP: three strokes, not quite even." | Heard through the tablet's small speaker: thin and band-limited (lows and highs cut off, as from a small speaker). The figure is visible; the sound's source "inside it" is not. **First statement: clear and complete.** | A machine inside a monster. |
| sc16 | "Behind her: a pump. Three uneven strokes." | **Acousmatic, off-screen, behind her, full-range and in the room.** The sound arrives over her face, off-screen, before any picture of the figure; carried across the cut into the first shot of the figure it is a J-cut (B1). | The threat has left the screen and entered her room. |
| sc20 to sc24 (optional) | (not written) | If used, very low under the ship's hum whenever the figure is near. | A judgment: it keeps the association alive. Leave it out if it risks becoming wallpaper. |
| sc25 | "The pale strip she took for a face: a flap of skin in a lit loop of tube, opening and closing. The pump she heard in the dark of her room: the only heart the big body has." | **De-acousmatization.** Macro insert; the flap's opening and closing is synchronized exactly with the strokes (synchresis). | The threat is a heart. Showing the source strips its power and turns fear into pity. |
| sc27 | "Breath in the helmet. Three uneven strokes against her chest." | Inside the helmet: close, muffled through the suit, felt as low frequencies; her breath over it. She is outside the ship in open space, so the helmet is the only place any sound can exist: no ship noise, no whoosh, nothing from outside for the whole scene. | Two hearts together; the motif is now a companion. |
| sc28 | "The little pump keeps working. Three uneven strokes." | In the room, heard by others, at an ordinary level. | A sign of life others can witness. |
| sc30 | "Each stroke of the pump makes the base of the vessel tap against the metal table." | The motif plus a new, harsher layer: glass tapping on metal, locked to each stroke. | The life is there, but hard and exposed. |
| sc30 | "The tapping stops. / The pump goes on." | She slides a folded cloth under the vessel; the tap layer disappears; the soft strokes remain. | An act of care edits the sound: the harshness is removed by her hand. |
| sc30 | "CUT TO BLACK. / Three uneven strokes in the dark." | Acousmatic again, over black. | The reverse of sc16: an unseen pump in the dark now means trust, not threat. |

**The ending, specified.**
- **Last picture shot:** close-medium on the vessel resting on the cloth beside the little container, Iona's hand withdrawing, Eli asleep soft beyond the glass. Hold it through at least two full cycles *after* the tapping stops, so the audience hears the change (tap gone, pump left).
- **Sound before the cut:** lower the room's ambience slowly during that hold, so by the last frame the pump is almost alone.
- **The cut:** cut to black (not a fade: a fade is a gesture of closure; the cut makes the pump the only thing that continues). Place the cut in the rest between two cycles, so the first sound in the dark is one complete statement: "Three uneven strokes in the dark."
- **After the three strokes:** do not stop the motif abruptly (rule SND8: a stopped heartbeat reads as a death). Either let it continue at the same level into the credits, or let it recede slowly over two or three more cycles, like a listener leaving the room, not a heart stopping. Which of these to use is a director's choice (see Section 15).
- **Music:** none over the ending. A score would tell the audience how to feel about the animal and the copied name; the motif already carries it.
- **Picture fields:** `transition_out: cut to black; sound continues (L-cut into black)`.

**Also a motif: the engine's CLICK and CLACK.** "A hard metal CLACK." (sc6, the puck firing) and "A small CLICK, from nowhere." (sc15, the cup moved) are one sound family at two sizes: the engine's signature. Give every engine firing in the film (the courier pod, the carriage, "She fires." in sc24 and sc27) a member of this family, so that by sc27 the audience knows by ear what just happened. The ship's HUM is a third motif, used as a status gauge: "The hum under the floor wavers" (sc23), "The hum misses a beat" (sc24), and "The sick motor through them. / Then not." (sc26), where its disappearance is the rupture that tells Iona, and the audience, that the ship is falling.

### Worked example 4. Prose to screen: the drill and the knock (*The Long Places*, Chapter VII, "The Breach")

**The passage** compresses days, then breaks on a sound:

> "For three days the little rig argued with the hill, and the hill gave up its core in orderly lengths ... and Melek sat through all of it on a folded sack, watching the rods eat downward. "You knock loudly," she said, on the second day, over the noise, to no one in particular, and would not be asked what she meant."
>
> "On the third morning the drill's note went hollow. The bit, which had been arguing with stone, agreed with nothing; the rods fell the length of a forearm and stood."

Later, a camera lowered on the rods is lost: "the camera went down its own way, without ceremony, and the sound of its arrival came back up the hole small and final, a knuckle on wood, once."

**Choices.**
1. **Montage sequence for the three days, built on the drill.** The drill's repeating note is the sequence's metric base (Eisenstein's metric method): shots cut on its rhythm. Each day is marked by a **jump cut from the same camera position** on Melek on her folded sack, with small changes that mark the days: the stack of core laid out beside her grows "in orderly lengths". The rig stands underground, in the low room past the fourth door, so there is no daylight to change; do not invent a window. She does not move; time does. The jump cut here means time passing, not a mistake, because the framing is exactly repeated.
2. **"You knock loudly" is spoken into the noise.** Mix the line so the drill partly masks it: the others barely hear it, the audience just catches it. Its content (the drill as knocking) plants the knock motif.
3. **The rupture is a sound change.** Over a routine shot the audience expects to pass, the drill's note goes hollow; the rods drop; then the drill is switched off (a staging choice; the text does not say) and three days of noise become silence. Hold on Márton, "both hands flat on the frame like a man taking a pulse", in room tone only. The build is the montage; the break is the note.
4. **The lost camera is heard, not seen.** Stay on the faces at the hole. The clamp jumps on the burr in the rod string (one sharp metal tick; the text: "the clamp met a burr on the rod string, and jumped"); then a silence long enough to measure depth by (the same device as *The Catch*'s tooth); then **one** small knock, far below, with a little reverberation. No bounce and no roll: a cylinder that falls should clatter and roll, and the prose later reveals the camera "upright on its foot, wiped, facing the stair" (Márton: "It fell."; then "It landed," Nilay said; then Márton: "It is a cylinder. They stand, or they roll."). The single clean knock is the plant for that payoff, so the sound designer must be told not to "improve" it.
5. **A knock motif across the chapter.** The drill ("You knock loudly"), the camera ("a knuckle on wood, once"), and the ritual at the stair ("knocked ... with the flat of his hand, twice, softly, and waited out the two breaths"; Melek "did the same — two, with the flat of the hand, on the cut stone"). Three sizes of knocking: machine, accident, courtesy. Give them one family of timbres so the audience hears the humans' two soft knocks as an answer to the machine's loud ones. The next chapter's letter confirms the reading and is the motif's payoff, a strong voice-over candidate over the drill images recalled (Chapter VIII: "*They knocked loudly, with iron that ate downward, a woodpecker noise in the house's bone, for days*").
6. **Prose that describes an image with a simile ("the picture closed like an eye") is not an instruction to illustrate it** (A1). The laptop feed simply goes to black; the simile stays in the book.

---

## 12. Checklist (run on every scene; a "no" needs a fix or a written reason)

**Scene level**
- [ ] Is the scene's turning point (from A2) marked, and is its shot the scene's shortest or longest?
- [ ] Is there a written rhythm plan, and do the shot durations follow it?
- [ ] Is there at most one rupture, on or next to the turning point, breaking a pattern the scene has established?
- [ ] Is the information ledger filled, and does the editing match its mode (suspense: longer holds; mystery: point of view kept; surprise: used once, fairly)?
- [ ] Is every plant shown once clearly, and does every payoff rhyme with its plant in framing or sound?
- [ ] Are transition in and transition out chosen, and is any effect other than a cut justified by a gap in time or a paragraph break in the story?
- [ ] Does each location have one ambience bed, and does it change only for a story reason?
- [ ] Is the music policy followed, and does every cue have in, out, function and "must not"?
- [ ] If the text states a time limit, is its screen time decided?
- [ ] Are all of the text's own editing and sound marks listed in `text_cues` and honored (Section 5.1)?
- [ ] Is a rhythm shape chosen by the rule in Section 6.2, and does this scene's ASL contrast with the scene before it where the story turns (Section 6.9)?
- [ ] Is there a continuity log, and does every clip match it (Section 3.8)?

**Shot level**
- [ ] Does every cut have a named reason (`cut_in_on`, `cut_out_on`)?
- [ ] Is the axis respected, or is the crossing deliberate, on a beat, and made readable?
- [ ] Do consecutive shots of one subject differ by at least 30 degrees or a clear size step?
- [ ] Is screen direction written for every moving subject, and consistent with the previous shot?
- [ ] For a match on action, do both clips contain the whole movement?
- [ ] Is each insert on screen long enough to be read by a first-time viewer (animatic test)?
- [ ] Does the reaction shot come after the event is seen, unless withholding is the point?
- [ ] Does every shot that withholds something say what and how?
- [ ] Are handles planned?
- [ ] Is every sound labeled diegetic or non-diegetic, on- or off-screen, with a perspective?
- [ ] Is "silence" specified as room tone, drop-out or true silence?
- [ ] Is it stated which sound comes from the model and which is built in the edit?
- [ ] Is any flipped shot checked for reversed direction, text and handedness?
- [ ] Does every shot with text on screen meet the reading minimum, doubled for mirrored text (R8)?
- [ ] Is every listener shot generated silent, with the speaker's line laid over it (AI7)?
- [ ] Does every line of dialogue fit its clip, or is it split at a phrase boundary under a listener shot (AI5)?
- [ ] Is `clip_length_s` a length the chosen model can actually generate?

---

## 13. Common mistakes, and how to spot them

| Mistake | How to spot it in a breakdown | Fix |
|---|---|---|
| **Cutting on every line** | Shot count equals line count; singles alternate like a tennis match. | Cut on beat changes (A2); use L-cuts to show listeners. |
| **The average peak** | The turning point's shot has the same duration as its neighbors. | Make it the shortest or the longest (R4). |
| **Faster cutting for suspense** | Suspense scenes have the scene's lowest ASL. | Suspense is waiting: hold on the unaware character (S2). |
| **Rupture without pattern** | Silence, black or handheld appear with nothing steady before them. | Establish the pattern first, or drop the device. |
| **Device inflation** | More than two editor-made cuts to black, freezes or true silences (of each kind) in a short film. Marks the script itself writes, and freezes a character makes on a screen in the story, do not count. | Budget them (P10); keep the ones on turning points. |
| **Accidental axis jump** | Two singles have both characters looking the same way. | Draw the axis on the floor plan; regenerate or flip (checking AI3). |
| **Direction amnesia** | A journey reverses screen direction between clips with no story reason. | Write direction into every prompt (C5). |
| **Near-duplicate angles** | Two consecutive shots of one subject with almost the same framing. | 30-degree rule, or make it an intended jump cut. |
| **Reveal spoiled by coverage** | A wide or reverse shows what a close shot withholds. | List `withholds` per shot and check all coverage against it (S3). |
| **Unrhymed payoff** | The payoff shot uses a different lens and angle from its plant. | Copy the plant's framing (S5). |
| **Dead silence** | "Silence" with no room tone specified. | Room tone plus one small sound (SND4). |
| **Music stating the subtext** | A cue labeled "sad" under a line whose sadness is unspoken. | Remove it or make it anempathetic (SND5). |
| **Showing the source too early** | The monster's sound and body arrive together in the first appearance. | Sound first, source later (SND1, SND2). |
| **Motif drift** | The same motif is described differently in each scene, so it is regenerated differently. | One asset ID, one signature (SND3). |
| **Ambience jumps at cuts** | Native model audio kept on every clip. | One bed per location (AI4). |
| **Asking the generator for transitions** | Prompts say "then dissolves to..." or "cut to...". | Generate shots; make transitions in the edit (AI2). |
| **Ending that stops dead** | The last sound is cut mid-pattern. | Let it continue or recede (SND8). |
| **Continuity drift** | A wound changes shoulder, a prop changes hand, a missing sleeve returns between clips. | Continuity log per scene; write the state into every prompt (C7). |
| **Talking listener** | The listener's lips move, or the wrong face speaks the line. | Generate listener shots silent and lay the line over them (AI7). |
| **Line too long for the clip** | A quoted line of more than about 17 words in one 8-second clip. | Split at a phrase boundary under a listener shot (AI5). |
| **Unreadable text** | A label, sign or screen caption on screen for under a second, or mirrored text held no longer than normal text. | Reading minimums (R8). |
| **Invented transitions** | The breakdown adds dissolves or fades the script never wrote, in a film that otherwise cuts. | Honor the script's marks (Section 5.1, T5). |

---

## 14. Tools: where this work is actually done

- **Editing program.** DaVinci Resolve has a free version with an audio section (Fairlight) for mixing, and is already recommended for grading in B2 and C2. Free, open-source alternatives: Kdenlive and Shotcut. Adobe Premiere Pro is the common paid option (C1 notes Adobe's Firefly models inside Premiere).
- **Animatic.** Timed storyboard frames plus temporary sound in the same editing program (C2). This is where this file's durations and sound choices are first tested. If previs (previsualization: a rough 3D version of the shots, C4) is done in Blender, its Video Sequencer can cut the previs renders with sound, keeping timing next to the 3D scenes.
- **Timeline hand-off.** An LLM can write the shot list as an edit decision list (EDL, a plain-text list of clips and in/out points in the old CMX 3600 format) or as an OpenTimelineIO file (an open, JSON-based timeline format hosted by the Academy Software Foundation), which several editing programs can import. Treat this as optional; check what your editor imports before relying on it.
- **Sound.** Native model audio (C1), a sound-effects library (for example freesound.org, whose sounds carry Creative Commons licenses that must be checked one by one), text-to-speech or voice models for temporary dialogue, and music models or a composer for cues. Google's Gemini API documentation lists music (Lyria) and text-to-speech models alongside Veo (navigation of ai.google.dev, checked 2026-09-27); C1 is the file to check for current options and prices. A further category is **video-to-audio** models, which generate synchronized effects for a clip that has none (for example the open-source MMAudio); useful for clips from silent models, but check any result against the shot's `sync_fx` list.
- **Mix hand-off.** Deliver **stems** (dialogue, music, effects on separate tracks) so a sound designer or a later pass can rebalance without starting over. **Loudness** is measured in LUFS (loudness units relative to full scale; closer to zero is louder). Broadcast standards set a target: EBU R 128 in Europe, -23 LUFS; ATSC A/85 in the US, -24 LKFS (the same unit). Web platforms turn loud uploads down to their own reference level (commonly cited as about -14 LUFS for YouTube; check the platform's current figure). Mix for the platform named in Section 15, question 6.

---

## 15. Open questions for the user

1. **Music policy for *The Catch*:** none, sparse score, or full score? This file recommends none or very sparse, so the pump can be the film's heartbeat.
2. **The ending's last seconds:** does the pump continue under the credits, or recede over two or three cycles? Either works; stopping it abruptly does not.
3. **Security footage audio (sc13):** silent (this file's choice) or with tinny sound?
4. **The optional pump under the ship scenes (sc20 to sc24):** include it at a low level, or keep the motif out between sc16 and sc25?
5. **The Long Places letters:** voice-over or not, and whose voice?
6. **Target platform and length:** a short film for festival screens tolerates longer holds than a vertical social cut; the rhythm plans assume a cinema-style viewing.

---

## Sources

**Books and articles**
- Walter Murch, *In the Blink of an Eye: A Perspective on Film Editing*, Silman-James Press (first edition 1995 in most sources, 1992 per Wikipedia; 2nd ed. 2001). Rule of Six quoted from pp. 17–20 of the 1995 edition as reproduced at https://blogs.ischool.berkeley.edu/i290-viznarr-s12/the-rule-of-six-walter-murch/ (checked 2026-09-27). The Hackman blink story is as summarized in secondary sources; not re-checked against the book.
- Walter Murch, "Dense Clarity, Clear Density", Transom, 1 April 2005, https://transom.org/2005/walter-murch/ (checked 2026-09-27: Law of Two-and-a-half and the *THX 1138* footsteps; five layers per five-second moment; encoded and embodied sound; worldizing).
- Michel Chion, *Audio-Vision: Sound on Screen*, ed. and trans. Claudia Gorbman, foreword by Walter Murch, Columbia University Press, 1994; 2nd ed. 2019, https://cup.columbia.edu/book/audio-vision-sound-on-screen/9780231185899/ (checked 2026-09-27). Chion's definitions of acousmatic and visualized sound, excerpted at http://www.filmsound.org/chion/acous.htm (checked 2026-09-27).
- Michel Chion, *The Voice in Cinema*, trans. Claudia Gorbman, Columbia University Press, 1999 (acousmêtre; its powers as listed in secondary sources checked 2026-09-27).
- François Truffaut, *Hitchcock*, Simon & Schuster, 1967; revised ed. 1984 (the bomb passage; wording checked against several reproductions, 2026-09-27).
- Sergei Eisenstein, "Methods of Montage" (1929), in *Film Form: Essays in Film Theory*, ed. and trans. Jay Leyda, Harcourt, Brace, 1949.
- Edward Dmytryk, *On Film Editing*, Focal Press, 1984 (rules 1–3 checked in chapter 5 listings, 2026-09-27).
- David Bordwell, "Intensified Continuity: Visual Style in Contemporary American Film", *Film Quarterly* 55:3 (Spring 2002), 16–28 (text checked 2026-09-27).
- David Bordwell and Kristin Thompson, *Film Art: An Introduction*, McGraw-Hill (12th ed. 2019), for continuity editing.
- Karel Reisz and Gavin Millar, *The Technique of Film Editing*, Focal Press, 1953; 2nd ed. 1968 (background; not quoted).
- Robert McKee, *Dialogue: The Art of Verbal Action for Page, Stage, and Screen*, Grand Central Publishing, 2016, checked against the book text on 2026-09-27: ch. 1 (the two screen modes of narratized dialogue; *Winter Light*'s letter to camera), ch. 2 (voice-over and exposition), ch. 5 (the pause before and after a turning point; "A pause must be earned"; "Silence invites the camera in"), ch. 16 (the camera and offscreen life).

**Web pages (Wikipedia, all checked 2026-09-27):** "180-degree rule", "30-degree rule", "Screen direction", "Eyeline match", "Cutting on action", "Establishing shot", "Creative geography", "Insert (filmmaking)", "Cutaway (filmmaking)", "Match cut", "Jump cut", "Smash cut", "Cross-cutting", "Split edit" (Barry Salt's small sample of 33 films; he cautions against treating it as a firm trend), "Dissolve (filmmaking)", "Wipe (transition)", "Iris shot", "Whip pan", "Freeze-frame shot", "Montage (filmmaking)", "Soviet montage theory", "Kuleshov effect" (including Prince & Hensley 1992, Mobbs et al. 2006, Barratt et al. 2016, Baranowski & Hecht 2017, and Hitchcock's 1964 *Telescope* interview), "Shot (filmmaking)", "Walter Murch", "In the Blink of an Eye (Murch book)", "Dede Allen", "Thelma Schoonmaker", "Anne V. Coates", "Sabotage (1936 film)", "Acousmatic sound", "Michel Chion". Base URL: https://en.wikipedia.org/wiki/

**AI video documentation:** Google, "Generate videos with Veo 3.1 in Gemini API", https://ai.google.dev/gemini-api/docs/veo (checked 2026-09-27): "Prompting for audio" and its speaker-and-parenthetical example, extension note on voice, language support, clip lengths of 4, 6 and 8 seconds at 24 fps.

**Library files:** A1 (dialogue: landing face, pauses, room tone), A2 (scene template, beats, sc13 beat list), B1 (camera system, the turn, surveillance and tablet footage), B2 and C2 (grading, animatics), C1 (model landscape, native audio, Sora retirement, audio references, physics errors).

**Films named** in the text are cited with their years. Film facts attributed above to a checked page were verified on 2026-09-27; those marked "well-known" come from general film knowledge and were not re-checked in this session.

**Test stories:** *The Catch* (workshop revision, 25 September 2026); *The Long Places* (revised final), Chapter VII, "The Breach".
