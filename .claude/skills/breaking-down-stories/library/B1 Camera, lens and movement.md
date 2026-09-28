# B1. The Camera as Narrator: Shot Size, Angle, Height, Lens, Depth of Field, Aspect Ratio, Movement

> **What this file is for**
> 1. It tells the pipeline how to choose, for every shot, how big the subject is, where the lens sits, which lens is used, what is sharp, what shape the frame is, and how the camera moves, and why.
> 2. It treats the camera as a narrator with a point of view: every choice says how close we are, whose side we are on, and what we are allowed to know.
> 3. It gives a vocabulary, a lens-and-movement table, a translation table, "If... then consider... because..." rules, a checklist, and common mistakes.
> 4. It designs a camera behavior system for *The Catch*, including its impossible situations (falling cage, zero gravity, mirror world, stars under the floor, surveillance footage, a tablet feed).
> 5. It ends with plain phrasings that AI image and video models follow, and Blender settings for exact camera control.

---

## 0. How to use this file

**Order of work for an LLM running the pipeline:**

1. Before any shot is designed, write the film's **camera behavior system** (Section 9): aspect ratio, lens family, default height, and what the camera does for each main character when they are in control and when they are not.
2. For each scene, find the beats and the turning point (the beat where the scene's value changes; see the A-series files on story and dialogue). Plan a **shot-size progression** (Section 2) that arrives at its closest or most extreme framing on the turning point, not before.
3. For each shot, fill six slots in this order: shot size, angle and height, lens, depth of field and focus, movement, and (if it changes) aspect ratio. Give a one-line reason for each that names a story fact. Write the slots on one line so they can be checked and turned into prompts, for example:
   `SIZE: medium close-up | ANGLE/HEIGHT: level, at Iona's kneeling eye height | LENS: 50 mm | FOCUS: shallow, on Iona's face | MOVE: static | RATIO: 2.39:1 (film default) | WHY: she has just found the proof and does not show it; the camera stays down with her and does not dramatize.`
   A slot with no story reason gets the film's default from its camera behavior system (Section 9: default lens, default height, default movement), or, if no system has been written yet, the neutral default in rule 25 (Section 11); never an invented flourish.
4. Run the checklist (Section 13) on every shot, and the decision rules (Section 11) where a slot is uncertain.
5. Only then translate to model prompts (Section 15).

### 0.1 Words this file uses (one word per concept)

Each term is defined once here and used with only this meaning afterwards.

- **Frame**: the rectangle the audience sees; everything outside it is **offscreen**.
- **Shot**: one continuous run of the camera between two cuts.
- **Shot size**: how much of a person the frame holds, from extreme wide (tiny figure in a big space) to extreme close-up (part of a face).
- **Angle**: which way the lens tilts relative to level: up at the subject (low angle), down at it (high angle), or level.
- **Height**: where the lens physically sits above the floor, independent of angle. A camera can be low and level.
- **Sensor**: the light-sensitive chip (or, on older films, the strip of film) that records the image. Bigger sensors see a wider view through the same lens.
- **Lens**: the glass in front of the sensor. Its **focal length** (in millimetres, mm) sets how wide or narrow the view is. In this file every focal length is a **full-frame equivalent** (the 36 mm wide still-photo format that Blender uses by default), unless a film's own number is being quoted. Equivalence here is matched by frame width: a lens is "50 mm equivalent" if it shows the same width of the scene as a 50 mm lens on a 36 mm wide sensor. To convert a number quoted for another format, see the table at the end of Section 4.2.
- **Wide lens**: roughly 14 to 35 mm; sees a wide view. **Normal lens**: roughly 40 to 58 mm; sees about as a person attends. **Long lens**: 75 mm and up; sees a narrow slice (also called telephoto elsewhere; this file says "long lens"). Numbers between the ranges take the feel of the nearer range: 36 to 39 mm behaves like a slightly wide normal lens, 60 to 70 mm like a mild long lens.
- **Depth of field**: how deep the zone of acceptable sharpness is, front to back. **Shallow** means only one plane is sharp; **deep** means near and far are sharp.
- **Rack focus**: shifting sharpness from one plane to another during a shot.
- **Aspect ratio**: the frame's width divided by its height (2.39:1 is very wide; 1.33:1 is nearly square).
- **Static frame**: the camera does not move at all during the shot (prompt phrase: "locked-off camera").
- **Pan / tilt**: the camera turns left-right / up-down on a fixed spot.
- **Push-in / pull-back**: the camera body travels toward / away from the subject on wheels, rails or a stabilizer (other books say "dolly in / dolly out"; a **dolly** is the wheeled platform the camera rides on).
- **Truck**: the camera travels sideways, parallel to the scene.
- **Pedestal (or boom) up / down**: the camera rises or sinks straight up or down without tilting (some AI tools call this a "vertical" move).
- **Follow**: the camera travels with a moving character, behind, beside, or ahead of them (ahead is called **leading**).
- **Zoom**: the focal length changes during the shot while the camera stays put.
- **Handheld**: the camera is carried on the operator's body with no stabilizer, so it breathes and shakes. A **stabilizer** (such as a Steadicam) is a rig that smooths a carried camera so it glides.
- **Crane**: an arm that lifts or lowers the whole camera (a small one is a **jib**).
- **Coverage**: the set of shots filmed or generated for one scene, from which the edit is built.
- **Eye line**: where a character looks. **Near the lens line** means just beside the camera, so they seem to look almost at the viewer.
- **Motivated movement**: a camera move caused by something in the scene (a character moves, looks, or a sound draws attention). **Unmotivated movement** is the narrator acting on its own.
- **Objective / subjective / point-of-view camera** (after Joseph V. Mascelli, *The Five C's of Cinematography*, 1965): **objective** watches as an unseen observer; **subjective** makes the camera the viewer's eye inside the scene, either because a character looks straight into the lens and addresses the viewer, or because the camera takes a character's place and sees through their eyes. Mascelli's **point-of-view** angle is different from today's usage: he puts the camera right beside a character, at their eye height, almost cheek to cheek with them, and calls it "as close as an objective shot can approach a subjective shot—and still remain objective." **This file uses "POV shot" in the modern sense** (and the sense AI models understand): the frame shows what one character sees, from their eye position, which Mascelli would call a subjective shot. When the file means Mascelli's beside-the-character angle it says **near-POV**.
- **Camera behavior system**: the written rules for what the camera does for this film and each character, and when those rules break.
- **Beat**: the smallest exchange of action and reaction in a scene (Robert McKee's unit in *Story*, 1997, and *Dialogue*, 2016). **Turning point**: the beat where the scene's value flips.

---

## 1. Core principles

1. **The camera is a narrator with a body.** Where it stands, how high, how far, and through which lens are each a sentence about the story: "we are close to her," "we are below him," "we watch them from far away without their knowing." If you cannot say the sentence, the choice is arbitrary.
2. **Size equals importance at this moment.** Frame an object or face at the size its importance has right now in the story. This idea is widely attributed to Alfred Hitchcock (in the Truffaut interviews, *Hitchcock*, 1967); treat the attribution as a paraphrase, not a quote.
3. **Distance is emotional distance.** Film audiences read shot size like social distance. Edward T. Hall's zones in *The Hidden Dimension* (1966) are intimate, personal, social and public; Louis Giannetti's *Understanding Movies* maps shot sizes onto them. Close-up reads as intimate, medium as personal/social, wide as public.
4. **Change is the signal, not the setting.** A long lens, a low angle or a handheld camera means something when it differs from what the film has taught the audience to expect. Bruce Block (*The Visual Story*, 2008) calls this **contrast and affinity**: contrast is a visible difference between shots or scenes (steady then shaking, wide then tight), which raises intensity; affinity is sameness, which calms it. Set a baseline first; spend departures on turning points.
5. **Save your extremes.** Extreme close-ups, overhead shots, Dutch tilts, dolly zooms and fast pushes work by rarity. A scene that uses its strongest framing on beat one has nowhere to go on beat nine. Default budgets, unless the camera behavior system (Section 9) sets others: at most one extreme close-up per scene, and only on the turning point; at most one push-in per scene; dolly zoom, orbit, Dutch tilt and unmotivated overhead at most once or twice per film each; a crane-up or pull-back ending on at most one scene in four.
6. **Position first, lens second.** Perspective comes from where the camera stands; the lens only decides how much of it is framed (Section 4.1).
7. **What the frame withholds is as authored as what it shows.** Offscreen space, a hand kept out of frame, a head that does not turn: these are camera choices, and they create suspense and subtext.
8. **Every camera move needs a reason you can name.** Unmotivated moves are the narrator's opinion; use them rarely and on purpose.
9. **A rule held for most of a film can be broken once,** at the turning point it serves, and the break will feel like an event.
10. **Physical honesty sells the impossible.** In a scene that could not exist, the camera behaves as a real camera would if it were there: bolted to the craft, floating with the body, stuck in a corner.
11. **One emphasis device per beat.** Emphasis devices are the choices that shout: a push-in, a rack focus, an extreme close-up, a low or high angle change, a lens change, slow motion, a crane move (and, outside the camera, a music sting or a line that states the point). If a beat already carries one (the actor's face shows the change, the dialogue says it, a sound lands), the camera adds nothing; if it carries none, the camera adds one. Two or more on the same beat is the heavy-handed, trailer version of the moment.

---

## 2. Shot size: psychological distance

### 2.1 The ladder

| Shot size | What is in frame | Distance it feels like | Typical story use | Risk |
|---|---|---|---|---|
| Extreme wide (EWS) | Tiny figure, big space | Public, or no relationship at all | Isolation, scale, the world's indifference, geography | Used as a reflex "establishing shot" (a wide that only says where we are) that says nothing about the scene |
| Wide / full (WS) | Whole body, some surroundings | Social | Blocking (the planned positions and moves of the actors), body language, who is where | Faces unreadable; holding too long in an intimate scene |
| Medium wide (MWS) | Knees up | Social | Group scenes, action with context | Neither intimate nor clear; a default nobody chose |
| Medium (MS) | Waist up | Personal | Conversation, gesture, hands and props | Flatness if every shot is a medium |
| Medium close-up (MCU) | Chest up | Personal to intimate | The workhorse of dialogue | Overuse flattens a scene's build |
| Close-up (CU) | Face, top of shoulders | Intimate | Thought, decision, reaction | Loses power if it is the default size |
| Extreme close-up (ECU) | Eyes, mouth, a finger | Closer than any social distance | A single detail that carries a turning point | Melodrama; cliché eye ECUs |
| Insert | An object or hand, usually close | Attention, not intimacy | Information the audience must read (a tag, a gauge, a puck) | Inserts that tell the audience what it already knows |

Combinations: a **two-shot** holds two people in one frame (it says "these two are together in this"); an **over-the-shoulder (OTS)** looks past one person's shoulder at the other (it keeps both in the relationship while favoring one face); a **single** holds one person alone (it isolates them, and separates them from the other person by a cut); a **POV shot** shows what one character sees from their eye position. A **dirty** single or over-the-shoulder keeps a sliver of the other person (a shoulder, the back of a head) blurred in the foreground; a **clean** single has nobody else in frame. Dirty frames keep the relationship present; clean frames cut the person off from it, so switching from dirty to clean singles partway through a scene is a quiet way to show two people drifting apart. A **reverse** (reverse angle) is a shot from roughly the opposite direction, showing what the previous shot's subject was looking at; a **cutaway** is a shot of something outside the main action, cut in briefly.

**Research note.** In an online experiment (495 viewers, thirteen versions of a short animated film), Bálint, Blessing and Rooney ("Shot scale matters," *Poetics*, 2020) found that the number of close-ups changed how much viewers spontaneously talked about the character's mental states: more close-ups raised it up to a point, beyond which it fell. Take the practical lesson modestly: close-ups help the audience read minds, and too many stop helping.

### 2.2 Progression through a scene

Shot size is a dial the scene turns. Four patterns cover most scenes:

1. **The approach.** Wide to medium to close as tension or intimacy rises, arriving at the closest size on the turning point. This is the classical default; it is invisible when it matches the beats.
2. **The withdrawal.** Close to wide as a character is abandoned, defeated or left alone with a consequence. A cut to a wide after a run of close-ups is a statement of isolation.
3. **The hold.** One size held while the content inside it changes. This works when the stillness is the meaning (a character trapped, a confession that the camera refuses to dramatize).
4. **The break.** A sudden jump in size (wide straight to extreme close-up, or the reverse) at the exact beat of a shock. It only works if the scene has been stepping gradually before it.

**Pairs of shots carry relationships.** Matched singles (same size, lens, height) say "equals"; a mismatch says power has shifted. Moving from two-shots to singles separates two people; moving back to a two-shot joins them, or traps them together (rules 3 and 4 in Section 11).

---

## 3. Angle and height: power, status, and whose eyes

### 3.1 The options

| Choice | What it does | Good use | When it becomes cliché |
|---|---|---|---|
| Eye level (the subject's eye height) | Neutral, equal footing | Most dialogue; the default that makes departures readable | Never by itself; it is the baseline |
| Low angle (lens below eyes, tilted up) | Subject looms; dominance, threat, heroism | Someone gaining power; a threat entering | "Villain from below" on every appearance |
| High angle (lens above, tilted down) | Subject diminished, watched, vulnerable | Defeat, exposure, being judged | Every sad moment gets a crane-up |
| Overhead / top-down (lens straight down) | Pattern, fate, a god's or machine's view; removes the horizon | Surveillance, maps of action, bodies on a floor | Decorative top-down on every table scene |
| Worm's-eye (lens at the floor, steeply up) | Extreme scale; architecture overwhelms | Something enormous, or a child's or animal's view | The "trunk shot" (looking up at characters from inside a car boot, a Quentin Tarantino signature) as a gag |
| Dutch tilt (the horizon rolled off level) | Unease, a world out of joint | A character's mind or world coming loose | Tilting because the scene is "tense" |
| POV (from a character's eyes) | Shared perception, often shared ignorance | Discovery, dread, a character reading something | Whole scenes in POV that lose the character's face |

**Height is not angle.** Yasujirō Ozu's camera in films such as *Tokyo Story* (1953) sits low, nominally at the eye height of a person kneeling on a tatami mat and often lower still (one or two feet off the floor), and it keeps that height even in hallways where everyone stands; it tilts little, if at all. The effect is respect and calm, not dominance. *E.T. the Extra-Terrestrial* (1982, cinematographer Allen Daviau) keeps the camera largely at a child's eye height, so adults are often seen only from the waist down until late in the film. The rule: **put the lens at the eye height of the person whose experience the scene belongs to**, then tilt only if power is shifting.

**Height as a slow progression.** Sidney Lumet writes in *Making Movies* (1995) that he shot the first third of *12 Angry Men* (1957) above eye level, the second third at eye level and the last third below it, so the ceiling began to appear as the room closed in: a film-scale plan, invisible scene by scene.

**Low angles with ceilings.** *Citizen Kane* (1941, Gregg Toland) shot low angles on sets built with ceilings: the angle enlarges a man while the room presses down on him.

**Dutch tilt: the classic and the warning.** *The Third Man* (1949, Carol Reed; Robert Krasker) tilts much of post-war Vienna to make it feel wrong to an outsider. *Battlefield Earth* (2000) tilts so often that Roger Ebert wrote in his review (Chicago Sun-Times, 12 May 2000) that the director "has learned from better films that directors sometimes tilt their cameras, but he has not learned why." A Dutch tilt needs a reason tied to perception (the world or a mind is wrong right now) and a release (the frame levels when the reason ends).

**Overhead as concealment that does not look like concealment.** Hitchcock told Truffaut (*Hitchcock*, 1967) that for the attack on Arbogast at the top of the stairs in *Psycho* (1960) he put the camera very high so he could shoot down on top of the attacker without seeming to hide her face, and, mainly, to get a violent contrast between that high long shot and the sudden close-up of Arbogast's face as the knife comes down. Two lessons: a high angle can withhold a face honestly, because the audience reads the height as geography rather than a trick; and an extreme angle earns its keep when the next cut contrasts with it.

### 3.2 Objective, subjective and POV cameras

Mascelli's three positions (Section 0.1), adjusted to modern usage, are a useful switch for every scene. For each shot, record which one it is:

- **Objective**: the audience watches from outside the action; most of a film. Good for fairness, judgment, and letting the audience notice what characters do not.
- **Subjective, direct address**: a character looks straight into the lens, so the viewer is the one being looked at. Jonathan Demme and Tak Fujimoto frame Clarice Starling and Hannibal Lecter almost straight into the lens in *The Silence of the Lambs* (1991), so each seems to stare at the viewer.
- **Near-POV** (Mascelli's "point-of-view"): the camera stands just beside a character at their eye height, so the audience sees almost what they see while staying an observer. It is the everyday way to share a character's view without losing their presence.
- **POV** (modern sense; Mascelli's subjective "through the eyes" shot): exactly one character's view. *Lady in the Lake* (1947) runs almost entirely in POV and shows the cost: the audience loses the character's face. *Halloween* (1978) opens with a killer's POV to create complicity. Use POV in short doses: to show what someone reads or sees, then cut back to their face to show what it means to them.

---

## 4. Lenses: what they do to space, faces and motion

### 4.1 The physics, stated correctly

- **Perspective is set by camera position only.** How big a near thing looks compared with a far thing depends on the distances from the camera to each, nothing else. If you stand in one spot and shoot with a 24 mm and a 100 mm lens, then crop the centre of the 24 mm image to match the 100 mm framing, the perspective is identical; only resolution and blur differ.
- **The lens sets framing.** Focal length decides the field of view: how much of that fixed perspective lands in the frame.
- **"Compression" is a consequence of distance.** To frame a face at the same size with a long lens, you must stand far away. From far away, the face and the wall behind it are at similar distances, so they look similar in size and close together. That is compression.
- **"Wide-lens distortion" of faces is a consequence of closeness.** To frame a face at the same size with a wide lens, you must stand close. The nose is then much nearer than the ears, so it looks big and the face bulges. Portrait photographers usually work around 85 to 135 mm (full-frame) for that reason.
- **Motion toward or away from the camera.** Apparent size changes with the ratio of distances. A runner 200 m away closing 20 m barely grows; a runner 4 m away closing 2 m doubles in size. So from far away on a long lens a runner seems to run in place: *The Graduate* (1967, Robert Surtees) shoots Benjamin's run to the church on a very long lens (often reported as about 500 mm) so he seems to make no progress. Close on a wide lens, the same run looks fast and violent.
- **Motion across the frame.** If the subject is framed at the same size, it takes the same time to cross the frame on any lens. What changes is the background, and it depends on how the camera follows:
  - **Travelling alongside** (a truck, keeping the subject the same size): on a long lens the camera is far away, so the background is only a little farther off than the subject and streaks past almost as fast as the subject is moving; the movement feels fast and frantic. On a wide lens the camera is close, so the background is many times farther away than the subject and drifts slowly; the same movement feels calmer, with strong **parallax** (near and far things sliding past at different speeds).
  - **Panning from a fixed spot** (the camera turns to keep the subject the same size): the background sweeps across the frame at the same rate on any lens, because a turn moves near and far things equally. The long lens only makes that background bigger and softer, so its blur reads as more of a smear.
  - Anything passing between a long lens and its subject (a passer-by, a car) flashes across the frame in an instant, because it is far closer to the camera than the subject is. From the same camera position (not the same framing), a subject does cross a long lens's narrow view sooner.
- **Depth of field** depends on the aperture (the f-number: lower means a wider opening and shallower focus), how large the subject is in the frame, and the size of the sensor. For the same framing of the subject at the same f-number, the sharp zone around the subject is about the same whatever the focal length; but a long lens shows a smaller patch of background and magnifies its blur, so the background looks far softer. A larger sensor at the same framing and f-number gives shallower depth of field.

### 4.2 What each lens range feels like

| Lens (full-frame equivalent) | Space | Faces (at a close-up) | Feeling | Story use |
|---|---|---|---|---|
| 14 to 24 mm | Deep, stretched, room feels large; shapes near the edges of the frame stretch, and some wide lenses also bow straight lines outward (called **barrel distortion**) | Must be very close; features swell | Presence, unease, the environment pressing in | Character inside a world that dominates them; looming threat; chaos |
| 28 to 35 mm | Natural but generous; background stays readable | Slight fullness if close | Being in the room with them | Following, handheld drama, character plus context |
| 40 to 58 mm (normal) | Closest to attentive human sight | Natural | Honesty, neutrality | Default "truthful" lens; observational scenes |
| 75 to 135 mm | Background shrinks and softens; planes flatten | Flattering, calm | Intimacy from a respectful distance; isolation of one face | Dialogue close-ups; a person cut out of their world |
| 200 mm and up | Space collapses; crowds stack; heat haze | Must be far away | Watching, being watched, futility | Surveillance, voyeurism, a character moving but not arriving |

**Practitioner examples (focal lengths are for each film's own camera format).**

- **Stanley Kubrick** favored wide lenses and deep, geometric spaces (*A Clockwork Orange*, 1971; *The Shining*, 1980). For *Barry Lyndon* (1975, John Alcott) he used Zeiss 50 mm f/0.7 lenses developed for NASA to shoot scenes lit only by candles (Zeiss and DPReview, checked 2026-09-27).
- **Akira Kurosawa** changed his technique "drastically" from *Seven Samurai* (1954), whose final battle is fought in rain, using long lenses and several cameras rolling at once. The result is dense, flattened action; his stated reason was the actors: filmed from a distance, not knowing which camera would be used, they played more naturally (Wikipedia, "Filmmaking technique of Akira Kurosawa," checked 2026-09-27).
- **Emmanuel Lubezki** shot *The Revenant* (2015) mainly on ALEXA XT and ALEXA M cameras (Super 35-size sensors, about 24 mm wide) with Master Prime lenses (a series of **primes**, lenses with one fixed focal length, as opposed to zooms), adding the larger ALEXA 65 for selected sequences. He kept to wide lenses, "from a 12mm to a 21mm, including the equivalent field of view in 65mm" (roughly 18 to 32 mm full-frame), set very close to the actors so face and landscape share the frame (ARRI; Society of Camera Operators, checked 2026-09-27). Putting a wide lens inches from a face while the background stays readable is sometimes called **close-focus wide**.
- **Roger Deakins** shot *1917* (2019) on an ALEXA Mini LF (a sensor almost exactly full-frame width, so its numbers need no conversion) with ARRI Signature Primes; the film uses only 35, 40 and 47 mm lenses (CineD, checked 2026-09-27). Deakins told British Cinematographer that about 90 percent of the film was shot on the 40 mm, with the 35 mm inside the German bunker and the 47 mm on the river to lose the background a little more (interview text seen through search results on 2026-09-27; the page itself blocks automated reading). One lens for nearly a whole film is itself a statement: an unbroken, human-scaled witness.
- **Hoyte van Hoytema** and director Tomas Alfredson built *Tinker Tailor Soldier Spy* (2011) around very long lenses from distant positions, so scenes feel observed (16:9 filmtidsskrift, checked 2026-09-27). On *Interstellar* (2014) he mounted IMAX cameras (a very large film format) directly onto large spacecraft miniatures to mimic NASA documentary footage (Wikipedia, checked 2026-09-27).
- **Bradford Young** kept *Arrival* (2016) close to Louise's experience, largely on a single focal length. Shooting on an ALEXA XT (a Super 35-class sensor) with vintage Ultra Prime lenses (plus a set of older, faster Super Speeds), he estimated that up to 90 percent of the Ultra Prime work was done on the 28 mm, reaching for a 40 mm to push in for detail; he had first wanted a 20 mm, but screen tests showed it was too aggressive on Amy Adams's face (American Cinematographer interview, as reported through search results on 2026-09-27; the ASC page blocks automated reading). On that sensor a 28 mm frames roughly like a 35 to 42 mm full-frame lens, depending on how much of the sensor was used: a close, human-scaled witness rather than a spectacle lens, in a film about aliens.
- **Sidney Lumet**'s **lens plot** (a written plan of which focal lengths the film uses where) for *12 Angry Men*, in his words from *Making Movies* as quoted by SlashFilm (checked 2026-09-27): "Starting with the normal range (28 mm to 40 mm), we progressed to 50 mm, 75 mm, and 100 mm lenses," so the jury room seemed to close in; the final exterior went wide, "to let us finally breathe." Note that on his 35 mm film format, 28 to 40 mm counted as normal: always convert before copying numbers. Converted (x1.6), his plot runs from roughly 45-65 mm to 160 mm full-frame.
- ***Son of Saul*** (2015, László Nemes; Mátyás Erdély) used one 40 mm lens on 35 mm film in a 1.375:1 frame, shallow focus, and a pledge that the camera stays with Saul and never goes beyond what he sees, hears or is present for (press kit; Wikipedia, checked 2026-09-27). On that format a 40 mm frames roughly like a 60 to 65 mm full-frame lens, which is why the world dissolves around him.

**Converting a quoted focal length to full-frame equivalent.** Multiply the quoted number by 36 divided by the width of the format's image in millimetres. Approximate multipliers (by width):

| Format the number was quoted for | Image width | Multiply by |
|---|---|---|
| Full-frame stills, ALEXA LF / Mini LF, Blender default | about 36 mm | 1.0 |
| Super 35 digital (ALEXA XT, ALEXA Mini, most cinema cameras) in 16:9 | about 24 to 25 mm | 1.5 |
| 35 mm film, Super 35 frame | about 25 mm | 1.45 |
| 35 mm film, Academy frame (1.37:1, the classic studio frame) | about 21 to 22 mm | 1.6 |
| 35 mm film, 2x anamorphic (the squeezed image un-squeezes to about 44 mm wide) | about 44 mm effective | 0.8 (field of view only; depth of field still looks like the quoted lens) |
| ALEXA 65 digital | about 54 mm | 0.67 |
| 65 mm film, 5-perforation frame | about 52 mm | 0.7 |
| IMAX 15-perforation 70 mm film | about 70 mm | 0.5 |
| Phone cameras | quoted as full-frame equivalent already (main camera usually 24 to 26 mm) | 1.0 |

### 4.3 Lens families and lens changes

A **lens family** is the restricted set of focal lengths a film allows itself, written down as a rule. Examples of rules: "Only 35 and 50 mm in the city; 24 mm only when the threat is in the room"; "Normal lens for the heroine; long lens whenever she is being watched." The benefits: consistency across a long film, a baseline against which a change reads, and, for AI generation, prompts that repeat the same lens words shot after shot so the look holds.

**Changing lens to mark a turning point.** Two methods: a **step change** (from this scene on, the family shifts, as in Lumet's plot), or a **single exception** (one shot in the film on a lens nobody else gets). Either needs to be tied to a named story change.

### 4.4 Spherical versus anamorphic

A **spherical** lens is an ordinary round-glass lens. An **anamorphic** lens squeezes a wider horizontal view onto the sensor (usually by 2x), which is un-squeezed later to make a very wide frame (about 2.39:1). Anamorphic traits: oval out-of-focus highlights, horizontal streak flares, edges that curve and soften, and, for the same vertical framing, a longer focal length and so shallower-looking focus. Use anamorphic when the film wants a romantic, dreamlike or epic texture and wide frames with shallow focus. Use spherical when it wants clean, documentary, clinical honesty. A 2.39:1 frame can be made either way (spherical lenses and a crop).

### 4.5 Depth of field, rack focus and split diopter

- **Shallow depth of field** isolates: one person sharp in a soft world. It says "only this matters," and it hides what the character is not attending to. It turns ugly when every shot has it: the audience cannot see the world.
- **Deep focus** keeps several planes sharp, so the audience chooses where to look and relationships across depth stay visible. *Citizen Kane* is the textbook case (achieved with wide lenses, small apertures, strong light and, in some shots, compositing: combining separately photographed near and far images into one frame).
- **Numbers for the depth-of-field slot** (full-frame, subject at medium-close-up distance; use them in Blender and as a guide for prompt words):
  - "Shallow": f/1.4 to f/2.8. One face sharp, the room a wash of shape and color.
  - "Moderate" (the default for dialogue): f/4 to f/5.6. The face sharp, the room soft but readable.
  - "Deep": f/8 to f/16, usually on a wide lens (24 to 35 mm). Near and far both readable.
  - If the audience must read something behind the subject (a gauge, a sign, a second person's reaction), then the slot cannot be "shallow."
- **Rack focus** moves attention inside a shot without a cut: from a hand to the face that notices it, from the foreground object to the reflection behind it. Rack on a beat: the focus shift is the moment of noticing.
- **Split diopter**: a half-lens attachment that makes one side of the frame focus close and the other far, so two planes are sharp at once with a soft seam between. Brian De Palma uses it often, for example in *Blow Out* (1981). It says "these two things, at different depths, are connected right now." It is conspicuous; use it for one or two such connections per film.

---

## 5. Aspect ratio

| Ratio | Where it comes from | What it favors | Story use |
|---|---|---|---|
| 1.33:1 / 1.37:1 (Academy) | Silent and early sound film; old TV | A single upright figure, faces, headroom (empty space above heads), vertical spaces | Confinement, portraiture, period feel; *Son of Saul*; *Ida* (2013) places people low under large empty headroom |
| 1.66:1 | European widescreen | A gentle widescreen that still holds height | Classical, painterly |
| 1.85:1 | US "flat" widescreen (flat means shot on ordinary spherical lenses, not anamorphic) | Two people in a room; balanced height and width | The versatile default for drama |
| 1.78:1 (16:9) | TV and web standard | Same as 1.85 in practice | Streaming, most AI video output |
| 2.39:1 (scope, short for CinemaScope, the 1950s trade name that popularized it) | Anamorphic 35 mm; now also cropped | Landscapes, groups, two faces at opposite edges, negative space (deliberately empty areas of frame) | Isolation inside space, epic scale, separation across a frame |
| 9:16 (vertical) | Phones | One standing figure, faces, vertical motion (falling, climbing) | Social platforms; vertical subjects such as a shaft |

**Changing ratio as a device** works when the change carries a story fact. *The Grand Budapest Hotel* (2014, Robert Yeoman) uses 1.37:1 for 1932, 2.40:1 for 1968 and 1.85:1 for the 1985 and present-day frame story. *Mommy* (2014, Xavier Dolan, André Turpin) runs in a 1:1 square and widens to 1.85:1 at two hopeful moments, the first when the teenage son, skateboarding, pushes the frame open with his hands. *The Dark Knight* (2008) and *Interstellar* open up to taller IMAX frames for spectacle. A motivated, low-cost ratio change available to any film is **diegetic footage** (footage that exists inside the story, such as a security camera or a phone): show it in its own native shape inside the film's frame.

**Choosing the ratio (decide once, before any shot).**
- If the film's key images are single upright figures, confinement or faces, then choose 1.33:1 to 1.66:1, because the frame's height gives the figure room and its narrowness presses in from the sides.
- If most scenes are two or three people in rooms, then choose 1.85:1, because it holds a two-shot and still has height for standing figures and doors.
- If the key images are landscapes, pairs at opposite edges, rows of rooms, or a figure made small by space, then choose 2.39:1, because width is what separates and isolates.
- If the delivery is a phone feed, then choose 9:16 and plan for vertical action (falling, climbing, a figure standing), because sideways action and two-shots barely fit.
- If the generation tool only outputs 16:9 but the film is 2.39:1, then compose every shot for the central band (keep heads, hands and text out of the top and bottom eighths of the frame) and crop in the edit.
- If a ratio change is proposed, then name the story fact it marks (a period, a recording, a release); if you cannot name one, do not change it.

---

## 6. Camera movement: what moving means

The full list of moves, with effect, use and risk, is the table in Section 7. This section covers the ideas that decide between them.

**Push-in versus zoom.** A push-in moves the camera's body, so near and far things shift against each other (this shifting is called **parallax**) and the audience feels it is physically approaching. A zoom only magnifies: no parallax, the image flattens and enlarges like binoculars, and it feels like attention or scrutiny from a fixed place rather than approach. Use a push-in for a character's inner movement toward a realization; use a zoom for an observer's gaze (a watcher, a machine, a documentary eye), as in the slow zoom-outs of *Barry Lyndon* that turn people into figures in a painting.

**The dolly zoom** (push-in while zooming out, or pull-back while zooming in, so the subject stays the same size while the background stretches or collapses). Devised by Paramount second-unit cameraman Irmin Roberts for Hitchcock's *Vertigo* (1958) to render dizziness; later used on Brody's realization on the beach in *Jaws* (1975) and in the diner in *Goodfellas* (1990) (Wikipedia, "Dolly zoom," checked 2026-09-27). It means "the ground of your world has just shifted." It is famous enough to read as a quotation; use it at most once per film, and only on a perceptual shift.

**Push-in on realization.** A slow push-in during a character's silence tells the audience that something is changing inside them; the slow push-in on Michael Corleone at the restaurant table in *The Godfather* (1972, Gordon Willis) before he shoots is a standard reference. Start it before the realization and land it at the moment of decision; a push-in that starts after the realization is late. It is also the most overused move in current drama: slow creeping push-ins on every serious line make the camera look busy and tell the audience nothing. Budget one per scene at most, only on the beat that turns the scene, and none on characters whose camera rule forbids it (Eli in Section 9.2). If the performance already shows the change, hold still instead.

**Pull-back to reveal.** Pulling back (or craning up) reveals context the character is now alone in or small against. Its classic use is isolation or consequence. Time it so the reveal lands on the last beat of a scene; it is a full stop.

**Static frame as judgment or as trap.** A static frame refuses to help. As **judgment**, it makes the audience watch what was done (the fixed frames of Chantal Akerman's *Jeanne Dielman*, 1975, or Michael Haneke's *Caché*, 2005). As a **trap**, it holds a character the camera will not rescue, and the audience scans it for danger (the fixed night camera of *Paranormal Activity*, 2007). It becomes tense once the audience has learned that something might appear in it.

**Motivated versus unmotivated.** A move is motivated when a character's movement, gaze, or a sound gives it a reason; such moves are felt, not noticed. Unmotivated moves (a slow creep toward an empty doorway, a rise to a high overhead) are the narrator speaking directly. Rule of thumb: most moves motivated; unmotivated moves only when the narrator knows something the characters do not.

**Following versus leading.** A camera **following** behind a character shows what they walk into and makes us share their path while their face stays hidden (*Elephant*, 2003; *Son of Saul*; the Dardenne brothers' *Rosetta*, 1999). A camera **leading** ahead of them, walking backward, shows their face and hides the destination, so the suspense is about what they are walking toward. Beside them (**trucking** alongside) is companionship.

**Stabilized versus handheld, and speed.** A stabilizer (Garrett Brown's Steadicam, first used on a feature in *Bound for Glory*, 1976, and widely seen in *Rocky*, 1976, and *The Shining*) glides like a ghost or a dream; handheld breathes and reports a body, anxiety or documentary truth. Choose per character and state of control (Section 9), not per genre. Slow moves read as inevitability; fast moves as alarm; match speed to the beat.

**Orbit, crane and drone: the moves that announce themselves.** An **orbit** (or arc) circles the subject, so the background wheels behind them: the world spins around a person who is, for this moment, its centre (lovers, a trap closing, a mind reeling). A **crane** that rises well above head height puts the viewer where nobody in the scene stands (a crane that simply follows a character up a staircase is motivated and does not count here). A **drone** can go anywhere and so belongs to nobody. Unless motivated like that staircase, all three are the narrator speaking, not a character: use them only where the film wants a view no person in the scene could have (fate, an institution, the end of a story), and never as a default opener or a "hero moment." If an orbit is used, give it a reason tied to the axis (it deliberately carries the audience across the line) and a duration (a quarter or half circle, rarely a full 360).

**Screen direction survives only if the camera respects the axis.** The **axis of action** is the imaginary line through two characters who face each other (or along a character's path); keeping every camera on one side of it keeps each person on the same side of the frame from shot to shot. A camera move can carry the audience across the line within a shot without confusion; a cut across it swaps everyone's sides. The full rules are in A4, Section 3, and B3, Section 5.2: the **180-degree rule** (keep every camera on one side of the axis) and the **30-degree rule** (when cutting between two shots of the same subject, move the camera at least 30 degrees around it or change the shot size clearly, or the cut looks like a stutter, called a **jump cut**). For this file the point is: record each scene's axis before choosing camera positions, and treat a deliberate crossing as one of the scene's extremes. A horizontally flipped clip (Section 10.2) also swaps sides, exactly like a crossing.

### 6.1 Camera speed and shutter: how motion itself looks

- **Frame rate** is how many pictures per second the camera records; film plays at 24. **Slow motion** records more (48, 60, 120 or more) and plays them at 24, stretching time; **fast motion** records fewer. Slow motion says "this moment is being remembered, revered or dreaded"; it is also the most common way to make violence, grief or sacrifice look like a perfume advert. Budget it like an extreme (A4 treats it the same way).
- **Shutter** sets how long each picture is exposed, and so how much a moving thing blurs. The normal setting (called a 180-degree shutter: each picture exposed for half its time, 1/48 second at 24 frames) gives the soft motion blur audiences read as "film." A narrow shutter (45 or 90 degrees) removes the blur, so motion looks crisp and stuttering; *Saving Private Ryan* (1998, Janusz Kamiński) used it on the Omaha Beach landing to make the chaos feel hard and immediate. Heavy smearing reads as dream or intoxication. The classic case is **step-printing** (shooting at a low frame rate with a slow shutter, then printing each picture several times to fill out normal speed, so movement smears and stutters at once), as in the chase that opens Wong Kar-wai's *Chungking Express* (1994; that first half was shot by Andrew Lau, the second half by Christopher Doyle, who used the same effect again in Wong's *Fallen Angels*, 1995).
- **In-story cameras** often run at their own low frame rate: a security camera at 10 to 15 pictures per second stutters, which marks the image as a recording without any overlay.
- **If** a moment should feel slowed, **then** first try holding the shot longer in real time with less happening in it, **because** real time that feels long is stronger and less familiar than slow motion. Use slow motion only when a character's perception of time actually changes and the film has set that up.
- **For AI video**, most models generate at a fixed frame rate; "slow motion" in a prompt is usually honored, while shutter angle is not controllable by words. Fast action often smears; a common fix is to generate it in slow motion and speed it up in the edit (C1).

---

## 7. Full lens-and-movement table

| Choice | Effect on the audience | Story use | Risk |
|---|---|---|---|
| Wide lens, close to a face | Face swells, background stays readable; presence, unease | A character dominated by or bursting out of their world; a looming threat | Caricature; accidental comedy |
| Normal lens at eye height | Honest, neutral witness | Baseline; observational truth | Blandness if nothing ever departs from it |
| Long lens from far away | Flattened planes, soft world, observed feeling | Intimacy at a distance, surveillance, futility, isolation of a face | Emotional distance when you wanted closeness |
| Very long lens, subject moving toward camera | Runs without arriving | Futile effort, dread of arrival | Reads as a quotation of *The Graduate* if used for a run |
| Shallow depth of field | One thing matters; world dissolves | Obsession, grief, subjectivity | The world disappears from every shot; "phone portrait" look |
| Deep focus | Audience chooses where to look | Relationships across space; planted clues | Busy frames with no hierarchy |
| Rack focus | Attention shifts inside the shot | Noticing, realization, linking two things | Racking on every line |
| Split diopter | Two depths sharp at once, visible seam | A connection the scene insists on | Gimmick; the seam cuts through faces |
| Anamorphic | Oval blur, streak flares, epic width | Romance, myth, spectacle | Flares as decoration; soft edges on key action |
| Static frame | Refuses to help; judgment or trap | Confession, aftermath, dread, surveillance | Dead scenes when nothing inside the frame changes |
| Pan | Scans or connects across a fixed spot | Linking two people or a cause and effect | Constant searching pans that feel indecisive |
| Whip pan (pan so fast the image smears) | Snap, shock, energy; hides a cut | Sudden connection or comic speed; *Whiplash* (2014) between drummer and conductor | Style for its own sake |
| Tilt up / down | Reveals height; awe or weight | Up for power or scale; down for defeat or discovery at the feet | Obvious tilt-up "hero" reveals |
| Push-in | Approaching; inner change | Realization, decision, intimacy growing | Mechanical push-ins on every line |
| Pull-back | Withdrawing; context arrives | Isolation, consequence, scene endings | Using it mid-scene deflates the scene |
| Truck (sideways) | Parallax, companionship, surveying | Walk-and-talk beside a character; surveying a line of rooms or people | Aimless drift |
| Follow from behind | Shared path, shared ignorance | Entering the unknown; a character's routine | Too long without the face |
| Lead from ahead | Face visible, destination hidden | Suspense about where they are going | Reads as a trailer shot |
| Crane / jib up | Rising above; release, fate, overview | Endings, a god's or institution's view | Grandiosity on small moments |
| Crane down | Entering the world, arriving | Openings; descending into a place | Generic opener |
| Stabilized glide | Smooth, uncanny, dreamlike presence | Haunting, long continuous journeys | Floating camera with no point of view |
| Handheld | Body, panic, immediacy | Loss of control, violence, documentary truth | Nausea and illegibility; "shaky cam" as a default |
| Pedestal up / down | Rises or sinks without changing angle; calm change of vantage | Matching a character who stands or kneels; a gentle reveal over an obstacle | Unnoticed drift that muddles whose eye height the scene has |
| Drone / aerial | Free god's view, geography | Scale, pursuit, isolation in landscape | Every drone shot looks like a travel advert |
| Close-focus wide (wide lens inches from a face) | Face and world in one frame; raw, bodily presence | Survival, exhaustion, a character inseparable from a hostile place | Distorted faces; tiring over a whole film |
| Slow motion | Time stretched; memory, reverence, dread | A perception that truly slows (shock, a fall seen as endless) | Stock "tragic slow-mo"; hides the face at the key beat |
| Narrow shutter (crisp, stuttering motion) | Hard, nervous, immediate | Combat, panic, a world that has turned hostile | Looks like a video-game or sports broadcast if unmotivated |
| Orbit / arc | Circles subjects; the world spins around them | Romance, vertigo, a trap closing, a heroic moment | The spinning "hero 360" cliché |
| Zoom in / out | Scrutiny without approach | Observers, machines, 1970s documentary texture | Cheap-looking if unmotivated |
| Dolly zoom | The world's ground shifts | One perceptual shock | Famous; reads as quotation |
| Dutch tilt | The world is out of joint | A mind or world coming loose | Constant tilting (see *Battlefield Earth*) |
| POV | Shared perception | Reading, discovering, dread | Loses the character's face |
| Near-POV (camera beside the character at their eye height) | Almost their view, while they stay present | Sharing a look without losing the person | Confused with an over-the-shoulder if the character's head fills the frame |
| Dirty single / dirty over-the-shoulder | The other person is felt at the edge | Relationship kept alive in each shot | Foreground shoulder too large, blocking the face |
| Clean single | The person is alone in their frame | Isolation, separation, private thought | Used from beat one, so separation has nowhere to go |

---

## 8. Translation table: story meaning to camera choices

**Each row is a menu, not a recipe.** Pick the one or two columns the beat needs and leave the others at the film's baseline (principle 11). A vulnerable moment that gets a wider size, a high angle, deep focus and a pull-back all at once is the stock version; the same moment with only the height changed is felt, not noticed.

| Story meaning | Shot size | Angle / height | Lens and focus | Movement | Watch out for |
|---|---|---|---|---|---|
| Character in control, competent | Medium, clean singles | Eye level | Normal, moderate focus | Static or smooth moves that match their pace | Making competence look boring; let inserts show their skill |
| Losing control | Sizes jump; tighter | Angle drifts off level | Wider lens, closer | Handheld enters | Starting the shake before the loss |
| Secret or withheld information | Partial framing; objects kept out of frame | Often objective | Shallow focus that hides the thing | Static, or moves that stop short of the reveal | Hiding so obviously the audience guesses |
| Revelation | Insert or ECU on the thing, then the face | Level | Rack focus from object to face (or reverse) | Push-in landing on the beat | Revealing twice (insert plus dialogue plus music); using insert, rack and push-in together: choose one |
| Power rising | Their singles tighten | Lower angle on them, higher on the other | Longer lens on them, isolating | Their frame steadies | Low angles from the first beat |
| Vulnerability | Wider, more space around them | Higher angle | Deep focus showing the space | Pull-back | Crane-up on every sad moment |
| Intimacy | Two-shot or matched close singles | Level, same height | Long lens from far away, looking along the line between the two at a shallow angle, so the depth between them compresses | Slow, minimal | Cutting between singles when the point is togetherness |
| Separation | Singles; wide two-shot with a gap | Mismatched heights | Wide lens from close exaggerates a gap that runs toward the camera | Static | Using glass or bars as the only symbol |
| Isolation | Extreme wide or tight single against blank space | Level or high | Long lens with blank soft background, or wide with empty space | Pull-back or static | The lonely drone shot |
| Dread | Static wide with empty areas | Slightly high or at a corner | Wide, deep focus so the audience scans | Static; very slow push toward empty space | Jump-scare stingers standing in for tension |
| Being watched | Wide, off-axis | High corner | Long lens, foreground obstruction | Static or mechanical pan | Obvious "voyeur through leaves" framing |
| Awe or scale | Extreme wide with a figure for scale | Low or worm's-eye | Wide | Crane up or slow tilt | Spectacle with no human reference in frame |
| Confession or truth | Holds; one size for a long time | Eye level, near the lens line | Normal to long | Static, or one slow push-in | Coverage that cuts the truth into pieces |
| Grief | Wide or held medium | Level | Normal | Static; long takes | ECU tears |
| Disorientation | Unexpected sizes | Dutch tilt or rolled camera | Wide, close | Handheld or rotating | Tilting without a perceptual reason |
| Shared perception | POV, then reaction | The character's eye height | Normal | Motivated by their head and eye movement | POV that never returns to the face |

---

## 9. The camera behavior system

Shots chosen one at a time produce a film with no point of view: every scene "looks good" and nothing accumulates. So the pipeline writes the system once, derives each shot from it, and records every departure with a reason. It is also the most reliable way to keep AI-generated shots consistent, because the same lens, height and movement words recur in every prompt.

### 9.1 Template (fill this before shot design)

```
CAMERA SYSTEM: <film title>
Aspect ratio: <ratio>, because <story reason>
Lens family: default <mm>, <mm>; exception lens <mm> only when <condition>
Default height: <whose eye height>, because <reason>
Default movement: <static / smooth / handheld>, motivated by <what>
Per character:
  <Name> in control: <size, height, movement>
  <Name> losing control: <what changes>
Reserved choices (max 1-2 uses each): <ECU on X, overhead, dolly zoom...>
Banned choices: <moves or framings this film never uses, with the reason>
Camera speed: <real time everywhere / slow motion only when...>
Diegetic footage: <each in-story camera: position, lens, ratio, movement, frame rate, overlays>
The break: at <scene/beat>, the camera does <opposite of its rule>, because <turning point>
```

### 9.2 A system for *The Catch*

**Aspect ratio: 2.39:1.** The film's key images are pairs facing each other across glass or a table (Iona and Saye "like a woman and her reflection"; Iona and Jude's hands at the end), rows of glass rooms, and a figure the script calls "Taller than the door." A very wide frame gives the pairs room to sit at opposite edges and forces tall things out of the top of the frame. Diegetic footage (security camera, tablet, the camera sent across) is shown in its own shape inside the 2.39 frame: 4:3 for the old security camera, 16:9 for the tablet and Saye's monitors.

**Lens family (spherical, full-frame equivalents).** 35 mm and 50 mm for all human scenes; 85 mm, from the confession scene onward, for dialogue singles and for the final reflection two-shot (Example 6). 24 mm is allowed in three places only: inside the cage in the shaft (so bodies, grid and wall all fit), for wides of the ship's spaces (the service cavity, the long chamber, the collection room, the ledge; faces on the ship stay on 35 and 50 mm), and for the figure in Iona's room, the one face-to-face shot where it is a threat and she does not yet know what it is (see the per-character table). Everywhere else, 24 mm is not used. A macro lens (a lens that focuses very close) for the reserved inserts. Spherical rather than anamorphic, because the film's register is clinical and physical (hospital, freight, sealed rooms), and because flare streaks would decorate a film that should feel observed.

**Default height.** Iona's eye height, because the film is hers; when she kneels, the camera kneels.

**Per character.**

| Character | In control | Losing control / revealed |
|---|---|---|
| Iona | Static frames or smooth moves that keep pace with her; inserts that follow her torch and fingers, so the camera inspects the way she inspects. Under fire she is still acting (she disarms the guard, hauls Jude and Eli behind the control box, times the STOP), so those scenes keep her steady grammar: the shots show as sound, sparks and cuts, not shake | Handheld, closer, wider lens (35 mm where the scene has been on 50 mm; 24 mm only where the lens family allows it, which here means her room), on exactly these beats: the broken rung (from "It rolls. Her foot goes." until "She gets a foot on the rung below."; when "the rung TURNS" earlier, "She goes still", and so does the camera), the car (from "Hits the door." to the end of the drive), and the figure in her room (from "She turns." until "The figure is gone.") |
| Eli | Partial framings; profile or three-quarter view; eyes kept well off the lens; one hand often out of frame or hidden behind something; no push-ins on him | In the confession: his closest, most frontal framing yet on "You.", with his eyes still on the monitor, as the script implies; then, on "He has been looking at the screen. Now he looks at her.", his first eye-level look near the lens line in the film |
| Saye | Seen through glass, centred, static, 50 mm from farther back than anyone else; often beside monitors she controls | The recorded Saye who "has lost the voice she uses for answers" is framed off-centre and closer in her recorded image on Iona's wrist display |
| Jude | Warm medium two-shots with Iona | Static, patient framing when injured; no handheld on him |
| The figure | Never gets a camera move while it is a threat: the frame does not pan, tilt, push, pull or follow because of it, and it appears in static frames, between cuts or between video frames. (If Iona's own shot is handheld at that moment, her shake carries into her view of it, but the frame still does not travel to find it or follow it; its arm moves inside the frame.) The looming frame (low angle, 24 mm, top of its head cut off by the frame) is used in one place only: Iona's room, where it is a threat and she does not know what it is. On the tablet it is seen from the feed's high corner; on the ship, from Iona's eye height, looking up only as far as its height forces, on 35 mm with its whole head in frame. Giving it a low angle on every appearance would turn it into a stock monster and spoil the reveal | When it helps (the air tank), the frame stays at her eye height and levels as it bends to set the tank down ("It bends. Sets the tank on the deck between them."). In the outer recess the camera looks up at its head from Iona's eye height one last time; when the chest opens, the camera tilts down with her eyes, then goes high and the lens goes macro on the animal |

**Reserved choices.** Top-down: only for in-story recordings (the security camera; the two dishes "filmed from above") and for Iona's steep downward POVs (through the cage's floor grid; through the ship's low wall window). Perfectly symmetrical profile two-shot: only for the two "reflection" moments (kitchen hands, final rings). Handheld: only for loss of control, on the three passages listed in Iona's row. Eli's eyes near the lens line: once, on "Now he looks at her." The looming 24 mm low angle on the figure: once, in Iona's room.

**Banned choices.** Dolly zoom: none (it would read as a quotation of *Vertigo*). Dutch tilt: none, because the film's wrongness is handedness (left and right swapped), and a tilted horizon would blur that one clear signal. Slow motion: none; the fall is played in real time (the floating beads of blood already look like slowed time, and slowing the picture would make them decorative), and the only altered frame rate is the security camera's stutter. Orbit: none.

**Axis rule.** Within a handedness phase (Section 10.2), every shot of a space is either all flipped or all unflipped; never cut between a flipped and an unflipped shot of the same space inside one phase, because the audience will read it as a crossed axis rather than as the mirror world.

**The break.** Throughout the film, stillness means Iona is in control and shake means she is not. On the ship's ledge, when her danger is greatest, the camera is completely still, because free fall has no sensation ("There is no feeling of speed at all"); then, when "She pushes gently away from the rail," the camera floats free with her for the first time by her choice. Floating, which meant helplessness in the cage, now means control.

---

## 10. Impossible camera situations in *The Catch*

### 10.1 The falling cage and zero gravity inside it

**Decision: the camera rides in the cage, held level with the world's vertical, and never shakes during the fall.**

- Before the stop, the camera is fixed inside the cage, as if bolted to its frame: the cage looks still, and speed shows only through the grid ("Floors go by. Light, brick, light, brick."). 24 mm, so the three bodies, the grid and the shaft wall beyond all fit.
- On "The cage STOPS DEAD. Everything in it goes on moving for the width of a hand, and then doesn't," the camera, being bolted to the cage, stops dead with it: the frame itself does not travel on. What moves is everything inside the frame, which lurches down the width of a hand relative to the steel and then stops, with Iona thrown flat on the grid. The impact may add one short, hard shudder of the whole frame (a few frames long, as the steel rings). That shudder is the sequence's only shake.
- When "The cage falls," there is no shake at all. **Free fall** means falling with nothing holding or slowing you, so everything falling together, camera included, feels weightless. The honest image is therefore calm: bodies drift, "round red beads" of blood hang and turn, all in real time, and the only violent motion is the shaft wall streaking past beyond the grid, slow at first and faster every second, because a falling object keeps speeding up. *Apollo 13* (1995) filmed its weightless scenes in NASA's KC-135 aircraft (a plane that flies steep up-and-over arcs, called parabolas, so everyone inside is briefly weightless) in bursts of about 25 seconds per parabola (Wikipedia; Science and Media Museum, checked 2026-09-27); *Inception* (2010) locked its camera to a rotating corridor so the set looked still while gravity seemed to move (No Film School; MPA, checked 2026-09-27). Both convince because the camera obeys the same physics as the people.
- "Through the grid, the opening flicks past. Going up." is a level POV from wherever Iona's face is, looking sideways through the gate: the opening is in the shaft wall beside the cage, level with the gate at the moment of the stop, so as the cage drops it can only be seen sliding up past the gate and out of the top of the frame. Design the cage gate as an open steel lattice or mesh, so the audience can see through it here and earlier ("Beyond the gate, the bright sill is almost level with the floor"). "Through the grid, the yellow stripe. Coming." is a POV straight down through the floor grid; the stripe grows shot by shot and becomes the fall's clock.

### 10.2 The turn and the mirror-reversed world

**Handedness** means which way round a thing is, left or right, the way a glove is a left or a right. **The rule: the frame's handedness belongs to Iona.** Whatever went through the turn with Iona looks exactly as it did before; everything that did not looks mirrored. The film has three phases:

| Phase | From / to | What looks mirrored to the audience |
|---|---|---|
| A | Opening to the "hard metal CLACK" | Nothing |
| B | From "Her eyes open" in the cage to the black beside the ship where she turns again | The shaft, the building, all text and signs, the city and traffic, her car, Saye, the nurse, Nell, all world-made screens and suits. Not mirrored: Iona, Jude, Eli, the cage, the flask, their clothes, the turned meals, the ship's interior (its world shares their handedness: its food is "Turned, like us," says Eli) |
| C | From her second turn to the end | Nothing in the world; now Jude and Eli look mirrored ("The familiar little smile, on the wrong side of his face"; Jude's ring "On his right hand"), and so do their turned meals ("The labels run opposite ways"). Not mirrored: Iona, the vessel, the animal and everything that turned with her the second time |

This is why "RECEIVING" works as a payoff: it is the first world text in a long time that reads correctly, to her and to the audience ("Iona looks at it. Reads it again."). It rhymes with the one earlier piece of text that read correctly in phase B, the label on the turned meal Saye passes through the hatch ("The letters face the right way. She reads it again."). Shoot both the same way (the same insert size and lens on the text, then the same framing of her face reading it twice), so the audience links them without being told.

**The first cue is screen direction.** In phase B, the maintenance opening, which passed on one side of the frame on the way down, approaches from the other side on the way up. Keep all post-turn shaft shots world-vertical (up is up), so the audience reads "The floor grid is above her" and "The cage is going UP" at once. The cage came out of the turn upside down, so a camera still bolted to it would show the shaft upside down and hide the fact that the cage is rising; after the black, the camera stays in the same place relative to the shaft but stops following the cage's orientation. Avoid any readable text in the shaft after the turn (turn the red tag away).

**Across a turn, repeat the framing.** The shot before a black and the shot after it use the same size, lens and position, so the change reads as the world changing, not the camera ("The same view, from the same side. Iona already inverted.").

**Three ways to make phase B, and when to use each:**

1. **Flip and compensate** (cheapest; best for wides and shots where turned characters are small): generate or shoot the shot normally, but with every turned thing pre-reversed (ring on the other hand, bandage on the other palm, the cage's control box on the other side); then flip the whole clip horizontally. For AI generation, flip the character reference image horizontally before generating, then flip the output; the character comes back to their normal handedness while the world is mirrored.
2. **Flip the background only** (best for close-ups): composite the unflipped actor or generated character over a separately flipped background clip. Use this whenever a face's own asymmetry matters.
3. **Mirror the props** (best for text the audience must read): make mirrored signs, labels and the left-hand-drive car directly.

For phase C, flip only Eli's and Jude's singles, keeping readable text out of their backgrounds; this is the reliable way to put "The familiar little smile" on the wrong side of a face. In two-shots with Iona, give Jude his ring on the right hand directly.

**Decision table for any phase B or C shot:**

| If the shot contains... | Then use... |
|---|---|
| Mostly world, turned characters small in frame | Method 1 (flip and compensate) |
| A turned character's face large in frame | Method 2 (flip the background only) |
| World text the audience must read | Method 3 (mirrored prop), or Method 1 with the text generated normally and flipped with the clip |
| A world-made screen (monitor, tablet, wrist display) in phase B | Treat its whole picture as world: flip the picture, not just its text. If the picture shows a turned character live (Jude on the tablet feed), pre-reverse that character inside the picture before the flip (Method 1), so he still looks like himself. A recording made before the turn (the security footage) needs no compensation: nobody in it had turned yet, so everything in it flips |
| No asymmetric detail and no text at all (a blank wall, stars) | No flip needed; but if it is cut together with flipped shots of the same space, flip it too (Section 9.2, axis rule) |

**The F carriage is a known conflict.** The demonstration happens in phase B, and Saye's carriage and paper F are world objects, so by the rule they should look mirrored to Iona and the audience before any turn, and correct after one turn. The script describes the opposite ("The F is unchanged", "Its F is backwards", "The F faces the right way", and the paper F turned over becomes "A backwards F"). Obeying the rule would make the "restored F" that Iona lays her palm beside read backwards on screen. See Section 16 for the recommended resolution; whichever is chosen, the same decision applies to the recording of the carriage on her wrist in the climax ("Its F reverses").

### 10.3 The ship, where stars are below the floor

**Decision: on the ship the camera is grounded, level and bolted to the ship.** The ship has ordinary weight ("The same weight in her legs as in the room she just left"), so the camera behaves like a tripod on a floor: no roll, no float. The strangeness comes from content: a steep downward POV through the window, which is set "in the wall beside her, low down," to stars "Below her feet," then a level shot of her standing with one hand on the rail. Because the camera is attached to the ship (the *Interstellar* approach), the ship's small dips ("dips below the line by a hair," seen on Saye's diagram) appear, if shown at all, as the stars in the low window shifting slightly, not as camera shake.

**When the ship lurches** ("The hum misses a beat. The deck drops beneath her, catches itself."; "The deck shakes under her"; "The deck shakes twice"), treat it like the cage's stop: the frame, bolted to the ship, drops and catches with the deck, so what the audience sees move is everything loose (Iona's body lifting a fraction off her feet and landing, a cup, the hanging cables), plus at most one short hard shudder of the frame, a few frames long, on the catch. No sustained shake: sustained shake is Iona's loss-of-control signal, and on the ship she is in control.

**When the ship falls** (on the ledge), the camera stays bolted to the ship and completely still. Nothing in the frame shakes; the loose screw rises and hangs, her knees lift, and the only motion that tells the audience they are falling is the visor drawing of the room "going up and up the glass like a lift leaving without her." No exterior shot of the falling ship exists until she leaves it; afterwards the camera is attached to her (over her shoulder or at her helmet), and the ship shrinks in a frame that does not correct her orientation ("Nothing has set her the right way up").

### 10.4 Surveillance footage

**Decision: one fixed camera, one master take, reused.** A **master take** here means one continuous recording from which every later excerpt is cut. "a camera above the top gate, looking straight down the shaft": top-down, wide lens with straight lines bowing slightly outward near the edges (barrel distortion), 4:3, low resolution, a low frame rate that makes motion stutter slightly (about 12 to 15 pictures per second), a timestamp overlay, and a fixed **exposure** (the brightness setting the camera records at) that the cage's lights overwhelm, so they flare. It never moves and is never re-framed; the characters can only pause, rewind, and (on a monitor) digitally enlarge. Build or generate it once, as one continuous clip covering the whole incident, and cut excerpts from it, so every viewing shows identical footage.

It must be designed backwards from its reveal: from above, through the roof grid, the audience must be able to see "a flat black puck is clipped to the grid" and Eli's hand come "out from behind Jude's back. Empty." So: bright cage light, a bright grid floor, a puck that is the darkest object in the shot, and Eli's hidden hand positioned so the high camera can see what Iona could not. The same event seen by a colder, higher camera is a different truth; for tone, compare the last shot of *The Conversation* (1974, Bill Butler), where the camera pans back and forth like a security camera over its own surveillance expert. In phase B the whole recording is a world-made picture, so it is shown mirrored: the overlay text reads backwards, and the cage's layout (the control box, where Eli crouches) sits on the opposite side from the audience's memory of the cage scene. That is correct by the rule and quietly unsettling; do not "fix" it, but make sure the puck and Eli's hand are readable either way round.

### 10.5 A tablet screen showing another room

**Decision: establish the tablet in Iona's hands, then cut so the feed fills the screen, and let the film camera inherit the feed's behavior.**

- Establish: Iona on the bed, "a tablet propped on her knees." Then cut to the feed filling the screen (16:9 inside 2.39), a high corner camera, wide lens, static, desaturated (colors drained toward grey), with a small overlay. The audience is now locked into a fixed view it cannot move, like Iona. This is phase B, and the tablet is a world-made screen, so its picture is mirrored and any overlay text reads backwards (Section 10.2).
- The figure's arrival is a jump inside a static frame: in one frame the space is empty, in the next "It is simply there." No camera move, no cut to another angle; the fixed view is what makes it credible.
- Cut back to Iona's face only after "The bed, and Jude, and the cup, and the figure are gone." and the empty chair.
- In her own room, the film camera then adopts the feed's grammar (worked through in Example 4).

### 10.6 Other in-story cameras

- **The camera sent across** ("stars, slowly turning"; "A huge black thumb passes across the lens"): in-story footage shot, in effect, by a non-human carrier, seen on Saye's monitor, so 16:9 inside the 2.39 frame, with the small diagram in one corner as the script describes. It tumbles in space, lies static in the recess, then is carried; optionally the carry can bob to the figure's pump rhythm ("three strokes, not quite even"), a motion signature for a creature the audience has not yet understood.
- **The visor and the wrist display.** These are graphics on a surface, not cameras, and the script leans on them in the climax ("VISOR VIEW", "HULL CLEARANCE", "UPWARD SPEED", the green and red outlines). Rules: (a) a "VISOR VIEW" is Iona's POV through the helmet, full 2.39 frame, with the graphics drawn flat on the visor glass, so they do not shift with parallax when her head moves, while the world behind them does; (b) the wrist display is always an insert on her glove, so the audience knows its size and where she is looking; (c) the graphics are world-made, so in phase B their text reads backwards (Section 16 has the open question); (d) keep each readout to one or two words or a number, held for the reading time in rule 2, because the ledge sequence is told almost entirely through them.
- **Vanishing and arriving.** Every vanishing and arrival in the film (the carriage, the courier pod, the beds in their shells, the cabinet, the figure, Iona arriving "folded sideways in the air" in the receiving room) happens between two frames of a static shot (rule 20): no camera move, no dissolve, no flash or glow added by the camera. The only sign is the needle, where one is in the room, and the sound.
- **Iona's suit camera and the curved container**: "In the curve of the container: the room behind her, and the figure standing in it." Show the figure only in the reflection. Rack focus from the cloudy thing inside the container to the reflection on its surface; do not cut to a reverse of the real figure until after it "reaches past her shoulder."
- **The carriage demonstration**: an objective, flat, side-on static frame at the height of the ramp, even light, so the F reads and the directions of travel are unmistakable. Design it once; the same framing becomes the recording on her wrist ("Down. Turn. Up.") in the climax. Which way round the F appears is an open decision (Section 10.2, "The F carriage is a known conflict", and Section 16).

---

## 11. Decision rules

**How to apply these rules.** "Consider" means: this is the default; apply it unless a higher-priority rule or the film's camera behavior system says otherwise, and write the reason in the shot's WHY slot when you do not. When two rules point different ways in one shot, follow this order of priority:

1. Rules for in-story footage and impossible physics (22, 23), because breaking them breaks the film's logic.
2. The film's written camera behavior system (Section 9), including its banned and reserved choices.
3. Turning-point rules (1, 7, 17, 24), because they carry the scene's change.
4. All other rules.
5. The neutral fallback (25).

**Shot size**
1. If a beat is the scene's turning point, then consider giving it the scene's most extreme framing: the **closest** framing when the turn happens inside a person (a realization, a decision, a confession, a lie exposed), the **widest** when the turn leaves a person abandoned, defeated or small against a consequence (the withdrawal pattern, Section 2.2), because size is the loudest signal and must be saved for the value change.
2. If the audience must read an object (a tag, a gauge, a puck), then consider an insert held long enough to read twice: at least 2 seconds, plus about half a second per word of text, because unread information is not information.
3. If two characters are equals in a dialogue, then consider matched singles (same size, lens, height), because any mismatch will be read as a power statement.
4. If a relationship is breaking, then consider moving from two-shots to singles (or from dirty to clean singles), because the cut itself becomes the separation.
5. If a scene's emotion is private and the character is hiding it, then consider staying one shot size wider than the progression would otherwise reach (a medium where you would have gone to a close-up), because the audience leans in when the camera does not.

**Angle and height**
6. If the scene belongs to one person's experience, then consider putting the lens at their eye height and keeping it level, because height is where the audience stands in the story.
7. If power shifts during a scene, then consider changing angle only on the beat where it shifts, and changing it in both halves of the exchange: from that beat on, the camera looks slightly up at the one who gained power and slightly down at the one who lost it, in their matching reverse shots, because a single low angle from beat one is decoration.
8. If you want a Dutch tilt, then consider it only while the script states that a character's perception or world is actually wrong (drugged, concussed, a world whose rules have just broken), and level the frame when it rights itself, because a tilt without a release is a style tic. "The scene is tense" is never enough.
9. If a view belongs to a machine, an institution, or fate, then consider a top-down or high fixed frame, because it removes the human horizon.

**Lens and focus**
10. If you want a face to feel close but the moment private, then consider a long lens from farther away (85 to 135 mm, camera about 2 to 4 m from a close-up), because it gives intimacy without intrusion.
11. If you want a character to feel pressed by their surroundings, then consider a wide lens close to them (24 to 28 mm, camera within about 1 m of the face), because the environment stays sharp and large around the face.
12. If a character is running or reaching and should not arrive, then consider a long lens with the motion toward camera (200 mm or longer, subject 50 m or more away), because apparent size barely changes.
13. If two people must feel together across a physical barrier, then consider one of two set-ups: (a) a long lens from far away, looking along the line between them at a shallow angle (past one toward the other), because distance compresses the depth between them so they seem nearer each other than they are; or (b) a profile two-shot with the camera exactly in the plane of the barrier, because a glass wall seen edge-on shrinks to a thin line. A long lens does not shrink a gap that runs across the frame; compression only works on distances toward and away from the camera.
14. If the scene is about noticing, then consider a rack focus on the beat of noticing, because the focus shift performs the thought. For AI video, where rack focus is unreliable, split it into two shots (focus on the first thing, then a cut to focus on the second) unless a test generation shows the tool can do it.
15. If a film needs a turning point felt below conscious notice, then consider a step change in the lens family from that scene on, because a new baseline is felt rather than seen.

**Movement**
16. If a character is in control, then consider static or smooth movement that follows their pace, because steadiness reads as competence.
17. If control is lost, then consider switching to handheld on the exact beat, not before, because early shake gives the surprise away.
18. If the narrator knows something the characters do not, then consider one unmotivated move in that scene, no more (a slow push toward the thing nobody has noticed), because that is the narrator speaking, and a narrator who speaks constantly stops being heard.
19. If a scene ends on consequence or isolation, then consider a pull-back or a cut to a wide, because withdrawing is a full stop. Keep to the budget in Section 1, principle 5 (at most one scene ending in four), or every scene will end on the same sigh.
20. If something should appear impossibly, then consider a static frame in which it simply is there after a cut or frame jump, because a camera move would suggest it arrived by a path.
21. If a camera move could be replaced by a cut with no loss, then consider cutting, because moves cost attention (and, in AI generation, stability).

**Aspect ratio and systems**
22. If footage exists inside the story, then consider showing it in its own native ratio and with its own fixed camera behavior, because the shape tells the audience it is a recording.
23. If the film has an impossible physics event, then consider a camera that obeys the same physics as the characters (falls with them, is bolted to their vehicle), because honest camera behavior sells impossible content.
24. If a character's inner state inverts at the climax, then consider inverting the camera rule tied to them there, because breaking a taught rule is the loudest thing the camera can do.
25. If you are not sure what a choice means, then consider the normal lens at eye height, static, because the neutral baseline is never wrong and keeps the extremes available.

---

## 12. Worked examples

### Example 1. Kneeling at the cage (*The Catch*, opening)

> "Two brake brackets, empty. Four bright bolt holes in each."
> "She puts a finger into one of the holes. Feels the thread. Still sharp."
> "She stays on her knees. One breath."
> "Above her, Jude unwinds the wire from the gate."

**Choices.** (1) Camera already placed at Iona's kneeling height when the shot starts (no move down to it), level, 50 mm: a medium shot of her kneeling at the cage, the torch under the floor frame, her face lit by its bounce. (2) Macro insert: the finger entering the bolt hole, the thread catching the torchlight. (3) Back to her, held static, for "One breath." (4) Same height, a wider frame (35 mm): Iona kneeling in the lower half, Jude standing, his head and shoulders cut off by the top of the frame, his hands working the wire.

**Why.** The camera inspects the way she does (her system, Section 9). The insert gives the audience her evidence (fresh threads mean the brakes were removed recently, on purpose) without dialogue. The static hold is the turning point of the beat: she knows, he does not. Keeping the camera at her height and cutting off Jude's head shows the knowledge gap as a height gap: she is below, knowing; he is above, busy. No push-in, because she does not dramatize; the camera respects her restraint.

### Example 2. The stop, the fall, and a hand we cannot see

> "The cage STOPS DEAD."
> "The cage falls."
> "He is looking straight at her. He has one hand she cannot see."
> "A hard metal CLACK."
> "BLACK. A dark with nothing in it. One instant."

**Choices.** The single impact shudder on the stop, with the bodies lurching inside a frame that has stopped dead; then the calm, shake-free, real-time fall (Section 10.1). For Eli: a close single at 35 mm in three-quarter view, his eyes locked on Iona, who is out of frame to one side, so his eye line passes well clear of the lens (his first look near the lens line is saved for the confession, Example 3); his arm runs out of the bottom of the frame behind Jude's back. The camera never tilts down to find the hand. The CLACK is sound over the frame; then true black for a fraction of a second; then phase B begins: the frame keeps Iona's handedness, so from here the world is mirrored (Section 10.2).

**Why.** The hand is the story's secret, and the frame, not a prop, hides it; the later surveillance footage (Section 10.4) will show it from a higher, colder camera. Eli looking straight at her while withholding is the scene's subtext; the frame has to keep both true at once. The calm fall is physically honest and far more frightening than shake.

### Example 3. The confession at the glass partition

> ELI: "One body."
> IONA: "One."
> ELI: "You."
> "Silence."
> ELI: "Tell me that's what you'd have wanted."
> "She opens her mouth. Nothing in it."
> IONA: "And afterwards?"
> "He has been looking at the screen. Now he looks at her."

**Choices.** The scene opens in wider frames that include the monitor (on Saye's side of the glass, turned to face it), Saye beyond the glass, and Jude, because the recording is the scene's evidence. As Iona questions him, the coverage narrows to over-the-shoulder shots between Iona and Eli, and then to 85 mm singles, the first 85 mm singles in the film. Eli's single stays in profile or three-quarter view (face turned halfway between profile and full face). On "You." it reaches its closest and most frontal framing yet, but his eyes stay on the monitor, as the script implies ("He has been looking at the screen"): he tells the truth to the recording, not to her. "Silence." is held on Iona's single, static; no cutaway. On "She opens her mouth. Nothing in it." the shot stays the same size; then an insert of "her palm, where the sill took the skin off," the physical proof of what he saved. The payoff comes on "Now he looks at her.": the same 85 mm single, and his eyes come round to the lens line for the first time in the film.

**Why.** Shot-size progression lands the closest framing on the scene's turning point ("You."). The script then gives the camera a second, separate beat: the moment Eli stops looking at the evidence and faces his sister. Spending the camera's rule (a withholding man never meets the lens) on that look, rather than on the line, makes the system pay off exactly where the script puts the change, and keeps "You." from being over-emphasized (principle 11). Holding "Silence." instead of cutting prevents coverage from chopping up the truth. The lens change to 85 mm is a step change: from here on, the family has a longer, more isolating lens, because from here on these siblings are separated.

### Example 4. The tablet, and the room that becomes the tablet

> "Something tall and black stands beside his bed. It did not come through the door. It is simply there, in the space between one moment and the next."
> "The needle climbs. The room is empty. She can see every corner of it."
> "Behind her: a pump. Three uneven strokes."

**Choices.** The tablet feed fills the screen: a high corner, wide, static, 16:9 inside 2.39, mirrored as a world-made picture. The figure appears by a jump between two frames of the feed, never by a move. In Iona's room, the film camera takes the same high corner, wide, static position; insert of the needle climbing (same framing as every earlier needle insert); the pump sound arrives from offscreen before anything is shown; she turns; the shot breaks to handheld at 24 mm, low angle on the figure, its head cut off by the top of the frame. The handheld is Iona's (she has lost control); the frame breathes with her but never pans, pushes or follows toward the figure, and its raised arm travels inside a frame that stays put. On "The figure is gone." the frame steadies on the empty space.

**Why.** The audience learns a grammar (things appear in static corner frames) and is then placed inside it. The fixed frame is a trap: Iona "can see every corner," and so can we, which is exactly why the sound from behind her works. The rule that the figure gets no camera move while it is a threat makes its appearances feel like arrivals from nowhere.

### Example 5. The chest opens (angle and lens inversion)

> "It puts its hand flat against its own chest."
> "The chest swings open."
> "In the water: an ANIMAL. Almost clear, like a thing from the bottom of the sea. No longer than her hand."
> "A suit."

**Choices.** Until "It puts its hand flat against its own chest," the figure is seen from Iona's eye height, tilted up at its head, 35 mm, its whole head in frame: the last time the camera looks up at it. As the latches let go, the camera tilts down with Iona's eyes, from the head to the opening chest (a motivated tilt: she looks, the frame looks). The animal is shown on a macro lens from above and then level with the vessel: the first time the camera meets the creature at its own height. "A suit." plays on Iona's face, static, 50 mm.

**Why.** Power and scale reverse on this beat, so angle and lens reverse with it: the looming giant becomes a shell, and the true being is small and fragile. Changing the camera's angle and height (from looking up at the head to looking down at, then level with, the vessel) is the visual form of the revelation; a line of dialogue is not needed and the script gives none.

### Example 6. The rings at the glass (the frame's handedness pays off)

> "His wedding ring. On his right hand."
> "She lifts her own left hand and lays it against his, through the glass. The two rings sit directly across from each other, like a ring and its reflection."

**Choices.** A perfectly symmetrical profile two-shot with the camera standing in the plane of the glass and looking along it (its line of sight parallel to the glass and at right angles to the line between the two faces), eye level, long lens (85 mm) from well back, so the two hands and rings meet at the centre line. Jude's side is generated or shot with his ring on his right hand (phase C, Section 10.2). This is the second and last symmetrical profile two-shot in the film; the first is Iona and Saye in the kitchen, "each with the wrong hand in the air."

**Why.** The film's reserved symmetry is kept for the two moments the script calls reflections, so the audience links them: the first was estrangement (a stranger mirroring her), the second is love across the same fact. With the camera exactly in the plane of the glass, the glass is seen edge-on and shrinks to a thin line between the hands, so the barrier nearly disappears (rule 13b). The long lens from well back keeps both profiles the same size and free of distortion, and softens the room behind them; it does not shrink the gap between them, which runs across the frame.

### Example 7. The warmth at her shoulder (*The Long Places*, Chapter I)

> "The warmth came against her right shoulder the way a cat commits itself: suddenly, entirely, with weight. The lamp stood on her left, on the stone."
> "She did not turn her head."

**Choices.** A static medium close-up in profile from her left side, level, at Nilay's seated height, 75 mm. The lamp sits soft in the foreground; her profile is sharp; her right side, and whatever leans on it, is hidden behind her own body. No push-in, no pan, no reverse angle. Hold long enough for her breathing to settle, then cut on her decision to stay still.

**Why.** The prose's key action is a refusal to look, so the camera refuses too: from this side it physically cannot see the warmth without moving, and it does not move. If the camera pans or cuts round, it overrules her and turns tenderness into a horror reveal. The long lens and soft background keep the moment private, and keeping the warmth offscreen preserves the novella's deliberate ambiguity (homesickness, a cat, or something else). The same rule later applies to Yusuf's phone footage in Chapter VI: a diegetic camera that frames "the niches only" after Melek's look is a character decision about what may be filmed.

---

## 13. Checklist (run on every shot; a "no" needs a fix or a written reason)

**Scene level**
- [ ] Is the camera behavior system written, and does this scene follow it or record why it departs?
- [ ] Is the turning point identified, and does the shot-size progression arrive at its strongest framing there and not earlier?
- [ ] Are the extremes (ECU, overhead, Dutch tilt, dolly zoom, orbit, fast moves, pull-back endings) inside the budgets in Section 1, principle 5 (or the film's own system), and only on beats that need them?
- [ ] Does each beat carry at most one emphasis device (principle 11), counting what the performance, dialogue and sound already do?
- [ ] Do singles in a dialogue match in size, lens and height unless a power shift is intended?

**Shot level**
- [ ] Can you state in one sentence what this shot's size says about distance to the character right now?
- [ ] Is the lens at the eye height of the person whose experience this is, and is any angle away from level tied to a named power or perception change?
- [ ] Was the camera position chosen first, and the lens second, to frame it?
- [ ] Is the focal length stated as a full-frame equivalent and inside the film's lens family (or a declared exception)?
- [ ] Does the depth of field hide only what the story wants hidden, and show everything the audience must read?
- [ ] If focus shifts, does it shift on a beat of noticing?
- [ ] Does every camera move have a named motivation (character movement, gaze, sound) or a stated narrator reason?
- [ ] Is there at most one camera move in the shot (for AI generation, required)?
- [ ] Is what the script withholds (a hidden hand, an unseen presence) kept out of frame?
- [ ] If the shot contains impossible physics, does the camera obey the same physics as the characters?
- [ ] If the shot shows in-story footage, does it keep the footage's fixed position, ratio, lens, overlays and exact content across every viewing?
- [ ] For *The Catch*: which handedness phase (A, B or C) is this shot in, and is every asymmetric detail (text, rings, wheel, smile, control box) on the correct side?
- [ ] Is this shot flipped or unflipped, and does that match every other shot of the same space in the same phase?
- [ ] Is the scene's axis of action recorded, and does this camera position respect it (or is the crossing a declared extreme)?
- [ ] Is the shot in real time? If slow motion is used, does the camera behavior system allow it here, and does a character's perception of time actually change?
- [ ] Does any symbol in the frame (glass, reflection, bars) appear because this beat needs it, not because the location has it?
- [ ] Would a cut do this job as well as the move? If yes, cut.

---

## 14. Common mistakes and how to spot them

| Mistake | How to spot it | Fix |
|---|---|---|
| Default coverage (wide, then over-the-shoulders, then singles, for every scene) | Every scene's shot list has the same shape | Start from the turning point and design toward it |
| Extremes spent early | The closest shot of the scene is on beat one or two | Move it to the turning point; step toward it |
| Floating camera | Many moves with no motivation written | Delete moves you cannot justify; static is a choice |
| Tension by tilt | Dutch tilts in scenes where nobody's perception is wrong | Level the frame; use blocking or sound for tension |
| Reflex low angles on threats and heroes | Every appearance of a character is from below | Keep eye level; drop the camera only on the beat power rises |
| Shallow focus everywhere | Backgrounds unreadable in every shot; locations never registered | Deep focus in establishing and relational shots |
| Copied focal lengths | "Shot on 40 mm like *Son of Saul*" without the format (on its 35 mm film, that 40 mm frames like a 60 to 65 mm full-frame lens) | Convert to full-frame equivalents first (table in Section 4.2) |
| Lens before position | "Use a wide lens for distortion" with no distance stated | Place the camera, then choose the lens that frames it |
| Handheld as realism | Handheld in calm scenes; no contrast when chaos arrives | Tie handheld to loss of control |
| Late or constant push-ins | A push-in starts after the line that turned the scene, or on every line | Start before the realization; ration to turning points |
| Endless POV | The character's face absent for a whole beat of discovery | POV, then the face, then POV if needed |
| Heavy-handed symbolism | Every shot framed through glass, bars or reflections; the symbol is in the frame and in the dialogue and in the music | Reserve the symbolic frame for the beat where it means most (Section 9.2 reserves symmetry for two moments) |
| Showing the withheld | A "helpful" insert of the hidden thing; a reverse angle on the unseen presence | Keep it offscreen; let another camera or the plot reveal it |
| Dishonest physics | Shake during free fall; a camera floating freely outside a ship | Bind the camera to a body or vehicle and obey its physics |
| Inconsistent in-story footage | The security camera moves, changes angle, or shows different content on replay | Build one master clip and cut from it |
| Stacked moves in AI prompts | "Push in, pan left, tilt up and orbit" in one prompt | One move per generated clip; cut between clips |
| Compression claimed across the frame | "Long lens to bring the two people together" in a side-on two-shot | Compression only shortens distances toward the camera; shoot along the line between them, or put the barrier edge-on (rule 13) |
| Slow motion for importance | Slow motion on sacrifice, grief, a fall, with no change in anyone's perception | Real time, held longer, with less happening (Section 6.1) |
| Low angle as the monster's signature | A creature or villain seen from below in every shot | Low angle only where the viewer character is face to face with it and afraid; eye level elsewhere, so the angle can change when the truth does |
| Stacked emphasis | One beat gets a push-in, a rack focus, an extreme close-up and a music swell together; or the line already states the point and the camera states it again | Keep one device, the one the beat most needs, and return the others to the film's baseline (principle 11) |
| A rule's payoff spent early | The look into the lens, the first close-up, the first handheld shot or the first long lens a character's system saves for one moment appears in an earlier scene | Search the shot list for each reserved choice before approving a scene; move early uses back to the baseline |

---

## 15. How to say this to an AI image or video model

Claims here are modest: model behavior changes with versions, and the only reliable test is to generate and look.

**What official guides document (checked 2026-09-27).**
- Google's Veo 3.1 guide (Google Cloud blog, 16 Oct 2025) recommends ordering a prompt as cinematography, then subject, action, context, style and ambiance, and lists terms including medium shot, two-shot, low angle, dolly, tracking, crane, aerial, slow pan, POV, 180-degree arc, shallow depth of field, wide-angle lens, macro lens and deep focus.
- OpenAI's Sora 2 prompting guide (OpenAI Cookbook) advises describing a shot as if sketching a storyboard, naming framing, lens and depth of field, and keeping to one clear camera move and one clear subject action per shot; it notes the model follows instructions more reliably in shorter clips.
- Runway's Gen-4 guidance says negative phrasing is not supported and can produce the opposite; for example, instead of "no camera movement," write "camera holds completely static." It favors short, simple, verb-led motion descriptions ("camera pushes slowly forward").
- Kling documents slider camera controls (horizontal, vertical, zoom, pan, tilt, roll) that are more exact than words. Availability differs between Kling model versions and modes, and its labels do not always match film usage ("vertical" is a pedestal move; check which of its "pan" and "tilt" turns left-right), so test one short clip per control before relying on it.

**Terms that usually work** (named in the guides above, and in common use): shot sizes (wide, medium, close-up, extreme close-up), two-shot, over-the-shoulder, low angle, high angle, top-down, eye level, POV, handheld, static, slow push-in / dolly in, tracking (the model word for a follow), pan, tilt, crane up, aerial, shallow depth of field, deep focus, wide-angle lens, macro. Focal lengths such as 24 mm, 35 mm, 50 mm and 85 mm work as style hints (wider or tighter look) rather than precise optics.

**Terms often ignored or misread** (from practice, not from the guides; test before relying on them): rack focus (inconsistent), split diopter (usually ignored), dolly zoom or "Vertigo effect" (unreliable), "truck" (can be read as the vehicle), zoom versus push-in (often rendered as the same forward drift), "objective" or "subjective camera" (meaningless to the model), exact aspect ratios written in the prompt (set the ratio in the tool instead), "anamorphic" (tends to add flares and a look, not a true squeeze), and anything that depends on a thing staying out of frame. Mirror-reversed text is not reliably generated; make it by flipping in the edit (Section 10.2).

**Plain phrasings that work better:**

| Instead of | Write |
|---|---|
| "Rack focus from the container to the reflection" | "Focus starts on the cloudy shape inside the clear container, then shifts to the reflection on its curved surface." |
| "Static frame" | "The camera holds completely still for the whole shot." |
| "Truck left" | "The camera slides sideways to the left, parallel to the wall." |
| "Push-in on realization" | "The camera moves slowly closer to her face while she stays still." |
| "Hide his hand" | "Close-up of his face and shoulder in three-quarter view, his eyes fixed on someone just out of frame to the left; his right arm runs down behind the other man's back, out of the bottom of the frame." |
| "Low angle, figure too tall for frame" | "Camera near the floor looking up; the tall black figure's head is cut off by the top of the frame." |
| "Zero-g, no shake" | "Everyone floats slowly, in real time; the camera is perfectly steady; only the brick wall beyond the steel grid streaks upward, faster and faster." |
| "Slow motion" (when the system allows it) | "Slow motion" usually works as written; say which action is slowed ("in slow motion, the cup tips and falls"), because models otherwise slow the whole scene |

**Example shot prompt (Example 1, the insert):** "Extreme close-up, macro lens, torchlight from the left: a woman's fingertip slides into a bright, empty bolt hole in greasy steel; the fresh, sharp thread glints. Shallow depth of field. The camera holds completely still. Cold, wet, dark brick tunnel."

**Image models (storyboards).** A still image has no movement, so describe the frame at the move's most important moment (usually where it lands) and keep the move in the breakdown text. Where a video tool accepts a start frame (and, in some tools, an end frame), generate the two storyboard frames first and let the video model travel between them; this is the most dependable way to get a specific push-in or reveal.

**When words fail, use Blender.** For exact control, build the shot as a simple previs (a rough 3D version) and feed a rendered frame or clip to the model as the start image, or as a motion guide (a video whose movement the model is told to copy), where the tool supports it. Useful Blender camera facts (Blender 5.2 manual, checked 2026-09-27): focal length is set in millimetres (default 50 mm) against a sensor whose default width is 36 mm, which matches this file's full-frame equivalents; Depth of Field has a Focus Object or Focus Distance and an F-Stop (lower means shallower); a Ratio setting simulates anamorphic out-of-focus shapes; and the manual notes that decreasing focal length while moving the camera toward an object produces a dolly zoom. Blender's Sensor Fit setting defaults to Auto, which applies the 36 mm to whichever side of the picture is longer; for a vertical 9:16 frame that is the height, so set Sensor Fit to Horizontal with a width of 36 mm if the file's focal lengths must mean the same horizontal view in every ratio. "Bolt the camera to the cage" is literal in Blender: parent the camera to the cage object (make the cage its parent, so the camera moves with it), and it will fall, stop and turn with it; for the post-turn shots in Section 10.2, clear the parent at the black so the camera stays world-vertical. For the mirror phases, flip clips horizontally in any editor.

---

## 16. Open questions for the user

- **Phase B screen text.** By the handedness rule, world-made screens (Saye's monitors, "NELL ROWAN. FLIGHT TEST.", the visor and wrist display) read backwards in phase B. Recommended: keep them backwards, few words, large, held about twice the normal reading time, with icons and color carrying the meaning; then the visor text snapping to readable after her final turn becomes an extra cue. The alternative (the technician set her display mirrored) keeps the climax legible but breaks the rule once.
- **The F carriage** (Section 10.2). Strictly, Saye's world-made F should look backwards to the audience before any turn and correct after one, the reverse of the script's wording. Recommended: follow the script's wording by making the two Fs (the carriage's and the paper one) exception props. Every shot in the demonstration room stays flipped like every other phase B shot, so the room's geometry and the axis rule hold, but the Fs are built or generated pre-reversed, the same compensation method 1 uses for rings and bandages, so after the flip they read exactly as the script describes: correct, then backwards after one turn, then correct again. The cost is that the F is the one world object in phase B that breaks the handedness rule; the gain is that the demonstration teaches the simplest possible lesson (a turn mirrors a thing, a second turn restores it) and Iona's palm beside "the restored F" with "Do that to us." reads at once. Alternative: obey the rule and let the audience see a backwards F first, which matches the turned meals' logic but makes the restored F read backwards on screen. Confirm.
- **The copied name label** ("IONA VALE," copied "stroke for stroke") was made on the ship from a world-printed wristband; this file assumes it reads backwards to Iona, as the wristband does. Confirm.
- **Aspect ratio for delivery.** 2.39:1 is recommended; most AI video tools output 16:9, so either compose for a 2.39 crop (keep heads, hands and text out of the top and bottom eighths of every generated frame; Section 5) or choose 1.85:1 to avoid cropping.

---

## Sources

**Books**
- Mascelli, Joseph V. *The Five C's of Cinematography.* Cine/Grafic Publications, 1965 (objective, subjective and point-of-view camera; camera angles).
- Katz, Steven D. *Film Directing Shot by Shot: Visualizing from Concept to Screen.* Michael Wiese Productions, 1991.
- Block, Bruce. *The Visual Story.* 2nd ed., Focal Press, 2008 (contrast and affinity).
- Lumet, Sidney. *Making Movies.* Knopf, 1995 (lens plot and camera heights for *12 Angry Men*).
- Giannetti, Louis. *Understanding Movies.* Pearson, multiple editions (shot size and proxemics).
- Hall, Edward T. *The Hidden Dimension.* Doubleday, 1966.
- Truffaut, François. *Hitchcock.* Simon & Schuster, 1967 (size and importance; the high camera over Arbogast in *Psycho*).
- Brown, Blain. *Cinematography: Theory and Practice.* 3rd ed., Routledge, 2016.
- McKee, Robert. *Story.* ReganBooks, 1997; *Dialogue: The Art of Verbal Action for Page, Stage, and Screen.* Twelve, 2016 (beats and turning points).

**Research**
- Bálint, K. E., Blessing, J. N., and Rooney, B. "Shot scale matters: The effect of close-up frequency on mental state attribution in film viewers." *Poetics*, 2020. https://www.sciencedirect.com/science/article/pii/S0304422X20302175 (abstract read via the Semantic Scholar and OpenAlex records for DOI 10.1016/j.poetic.2020.101480, checked 2026-09-27; N = 495 and thirteen film versions re-confirmed against the abstract, 2026-09-27).

**Web (all checked 2026-09-27)**
- Deakins lens use on *1917*: British Cinematographer, https://britishcinematographer.co.uk/exclusive-interview-roger-deakins-cbe-bsc-asc-on-1917-bc97/ (blocks automated fetch; its statement that about 90 percent was shot on the 40 mm, the 47 mm on the river and the 35 mm in the bunker was read through search-result text on 2026-09-27) ; CineD, https://www.cined.com/1917-dp-roger-deakins/ (confirms ALEXA Mini LF, Signature Primes, 35, 40 and 47 mm)
- *Interstellar* cameras mounted on miniatures and handheld IMAX: https://en.wikipedia.org/wiki/Interstellar_(film)
- *Inception* rotating corridor: https://nofilmschool.com/how-inception-faked-zero-gravity ; https://www.motionpictures.org/2015/08/heres-how-they-made-the-incredible-inception-hallway-fight-scene/
- *Apollo 13* weightless filming: https://en.wikipedia.org/wiki/Apollo_13_(film) ; https://blog.scienceandmediamuseum.org.uk/how-apollo-13-was-made/
- Dolly zoom and Irmin Roberts: https://en.wikipedia.org/wiki/Dolly_zoom
- Dutch angle, *The Third Man*, Ebert on *Battlefield Earth*: https://en.wikipedia.org/wiki/Dutch_angle ; https://www.rogerebert.com/reviews/battlefield-earth-2000
- Lumet's lens plot (quoting *Making Movies*): https://www.slashfilm.com/793246/how-sidney-lumet-used-different-eye-levels-to-create-tension-in-12-angry-men/
- *The Revenant* cameras and lenses (ALEXA XT and M as main cameras, ALEXA 65 for selected sequences; lenses "from a 12mm to a 21mm"): https://www.arri.com/news-en/alexa-xt-and-alexa-65-on-the-revenant- ; https://soc.org/project/the-revenant-shooting-in-the-elements/
- *Son of Saul* lens, ratio and camera pledge: https://en.wikipedia.org/wiki/Son_of_Saul ; https://www.sonyclassics.com/sonofsaul/sonofsaul_presskit.pdf
- *The Grand Budapest Hotel* ratios: https://www.indiewire.com/features/craft/wes-andersons-dp-robert-yeoman-on-bringing-the-grand-budapest-hotel-to-life-66637/ ; https://en.wikipedia.org/wiki/The_Grand_Budapest_Hotel
- *Mommy* 1:1 ratio: https://www.hollywoodreporter.com/movies/movie-news/why-xavier-dolans-mommy-was-756857/ ; https://en.wikipedia.org/wiki/Mommy_(2014_film) (the widening to 1.85:1 at two hopeful moments is from the Hollywood Reporter article as summarized in search results; Wikipedia confirms only the 1:1 frame)
- *Barry Lyndon* f/0.7 lenses: https://www.zeiss.com/photonics-and-optics/en/home/content/newsroom/news-overview/2022/zeiss-planar-07-50.html ; https://www.dpreview.com/news/8390711699/
- *Tinker Tailor Soldier Spy* long-lens design: http://www.16-9.dk/2014/10/tinker-tailor-soldier-spy/
- Kurosawa's long lenses and multiple cameras: https://en.wikipedia.org/wiki/Filmmaking_technique_of_Akira_Kurosawa
- Ozu's low camera (tatami shot, often one or two feet off the floor): https://en.wikipedia.org/wiki/Yasujir%C5%8D_Ozu
- Mascelli's point-of-view angle ("as close as an objective shot can approach a subjective shot") and *Lady in the Lake*: https://en.wikipedia.org/wiki/Point-of-view_shot
- *E.T.* child-height camera: https://en.wikipedia.org/wiki/E.T._the_Extra-Terrestrial ; https://theconversation.com/e-t-the-extra-terrestrial-at-40-a-deep-meditation-on-loneliness-and-spielbergs-most-exhilarating-film-183985
- *The Graduate* long-lens run: https://cinemashock.org/2012/03/08/telephoto-lens-in-the-graduate/ (focal length "about 500 mm" is widely repeated but not confirmed from a primary source)
- *The Conversation* final surveillance-style pan: https://www.saturdayeveningpost.com/2024/08/review-the-conversation-movies-for-the-rest-of-us-with-bill-newcott/
- *Arrival* and Bradford Young (ALEXA XT; vintage Ultra Primes; up to 90 percent of that work on the 28 mm, a 40 mm for detail; a 20 mm rejected after tests): https://theasc.com/article/arrival-cinematography-bradford-young/ (blocks automated fetch; read through search-result text on 2026-09-27) ; https://britishcinematographer.co.uk/bradford-young-asc-arrival/
- Veo 3.1 prompting guide: https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1
- Sora 2 prompting guide: https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide
- *The Godfather* restaurant scene, camera moving closer to Michael: https://nofilmschool.com/2017/01/watch-4-filmmkaing-lessons-godfather-restaurant-scene-coppola ; https://screenrant.com/godfather-pacino-restaurant-scene-saved-movie-reason/
- Runway Gen-4 video prompting guide: https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide (page blocked automated fetch; content confirmed through search summaries)
- Kling camera control guide: https://kling.ai/quickstart/ai-camera-control-guide
- *Psycho* high camera over Arbogast (Hitchcock to Truffaut): https://www.thebluegrassspecial.com/archive/2010/june10/hitchcock-truffaut-interview.html
- *Chungking Express* cinematographers (Andrew Lau shot the first half, including the step-printed opening; Christopher Doyle the second): https://en.wikipedia.org/wiki/Andrew_Lau ; https://en.wikipedia.org/wiki/Chungking_Express
- *Fallen Angels* step-printing (Christopher Doyle): https://en.wikipedia.org/wiki/Fallen_Angels_(1995_film)
- Blender manual, Cameras: https://docs.blender.org/manual/en/latest/render/cameras.html

**Films** are cited in the text with year and, where it matters, director and cinematographer; claims about them come from the web sources above or from widely documented production history (for example: *Bound for Glory* as the first feature to use the Steadicam; the narrow shutter on *Saving Private Ryan*'s Omaha Beach landing; step-printed motion in *Chungking Express* and *Fallen Angels*), and none of the scene descriptions quotes dialogue.
