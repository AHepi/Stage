# B3. Composition, Visual Structure, and Staging Bodies in Space

> **What this file is for**
> 1. It tells the pipeline how to build each frame (what goes where, and where the eye lands first) and how the look of the whole film rises and falls with the story (Bruce Block's visual structure).
> 2. It tells the pipeline where people stand, how far apart, and when and why they move (staging and blocking), and how to keep the audience oriented (geography and screen direction).
> 3. It gives a translation table, "If ... then consider ... because ..." rules plus firm restraint and glass-physics rules, a per-shot composition checklist, a per-scene staging checklist, and common mistakes.
> 4. It designs the glass-barrier and mirroring system for *The Catch*, and gives a text floor-plan format plus a tested Blender script that turns it into a grey 3D blocking scene.
> 5. Read it after the scene's beats and turning point exist (A-series files) and alongside B1 (camera and lens) and B2 (light and color).

---

## 0. How to use this file

**Order of work for an LLM running the pipeline:**

1. Once per film: write the **visual structure plan** (Section 2.6): chart story intensity scene by scene, then decide how each visual component will track it.
2. Once per location: write a **floor plan** in text (Section 6) with fixed objects, an **anchor** for orientation, and the entrances, in the orientation the audience will see (Section 5.4); for a world location seen in more than one mirror phase, write the world plan first and derive the others. Sections 6.3, 8.6, 8.7 and 8.8 give four worked plans.
3. Per scene: plan the **blocking** beat by beat (Section 4): start marks, moves, and the configuration change at the turning point. Draw the **line of action** for each part of the scene and choose which side the camera stays on (Section 5).
4. Per shot: fill the composition slots (Section 3): dominant element, placement, balance, headroom, lead room and eyeline, layers, frames within the frame, glass state (for *The Catch*, including the visor). Give a one-line story reason for each non-default choice, naming an object, line or action from the script (Rule 23).
5. Run the per-shot and per-scene checklists (Section 10). Then translate to prompts (Section 12) or to Blender (Section 6.4 for the scene; C4 for per-shot previs).

**For the non-technical user:** paste your scene and say, "Using file B3, write the floor plan, the blocking by beat, and a composition line for each shot. Mark every choice with the story reason." Then check by eye that each reason names something that happens in the scene.

### 0.1 Words this file uses (one word per concept)

Camera words (shot size, lens, height, push-in and so on) are defined in file B1 and mean the same here. Story words (beat, turning point, value, scene intention) are defined in file A2.

| Term | Plain definition |
|---|---|
| **Composition** | The arrangement of everything inside one frame at one moment. |
| **Frame-left / frame-right** | The left or right of the picture as the audience sees it (not the character's left or right). |
| **Picture plane** | The flat surface of the screen itself. |
| **Frontal plane** | A surface that faces the camera squarely, parallel to the picture plane (a wall seen straight on, a sheet of glass seen straight on). |
| **Longitudinal plane** | A surface that runs away from the camera into depth (a corridor wall seen along its length). The terms are Block's. |
| **Layer** | A band of depth in the frame: **foreground** (nearest), **midground**, **background** (farthest). |
| **Depth cue** | Anything in a flat picture that tells the eye one thing is farther away than another (overlap, size, converging lines, haze, focus). |
| **Visual component** | One of Block's seven building blocks of every picture: space, line, shape, tone, color, movement, rhythm. |
| **Contrast / affinity** | Block's words: **contrast** is difference within a component (big and small, bright and dark); **affinity** is similarity. |
| **Visual intensity** | How agitated or calm a stretch of picture feels. More contrast raises it; more affinity lowers it. |
| **Story intensity** | How much pressure the story carries at a moment. This file scores it 1 to 10 per scene (A2 scores beats 1 to 5). |
| **Space type** | Block's four kinds of screen space: **deep**, **flat**, **limited**, **ambiguous** (Section 2.3). |
| **Point of attention** | Block's term for the spot in the frame the audience is looking at right now. |
| **Eye-trace** | Walter Murch's term for the path the point of attention travels across a cut. |
| **Dominant** | The element the eye goes to first in a frame. |
| **Balance** | How visual weight is spread across the frame. **Symmetrical**: mirrored halves. **Asymmetrical**: unequal elements that still feel settled. **Imbalance**: weight piled to one side so the frame feels unsettled. |
| **Headroom** | Space between the top of a head and the top of the frame. |
| **Lead room** | Space in front of a face or a moving body, in the direction it looks or moves (for a look, some books say "nose room"; this file says lead room). |
| **Short-siding** | Placing a character so they face the near edge of the frame, with the larger empty area behind them. |
| **Negative space** | Empty or near-empty area of the frame that is left empty on purpose. |
| **Frame within a frame** | A doorway, window, mirror, screen or glass pane inside the shot that frames part of the picture a second time. |
| **Leading line** | A line in the picture (a wall edge, a table, a floor stripe, a gesture) that carries the eye to something. |
| **Open form / closed form** | **Closed form** keeps everything important inside the frame and feels complete; **open form** lets people and objects be cut by the edges, so the world seems to continue offscreen. |
| **Planimetric** | A frame where the camera faces a back wall squarely and people are strung across it side by side. David Bordwell took the word from the art historian Heinrich Wölfflin and made it standard in film writing. |
| **Vanishing point** | The point in the picture where lines that are parallel in the real world (corridor walls, rails) appear to meet. |
| **Aspect ratio** | The frame's width divided by its height; 2.39:1 means the picture is 2.39 times as wide as it is tall. |
| **Progression** | Block's word for a planned, gradual change in one visual component across a scene or film (for example, space getting flatter scene by scene). |
| **Staging** | The overall strategy for placing bodies in space relative to the camera (for example, staging in depth). |
| **Blocking** | The exact marks and moves of each person, beat by beat, that carry out the staging. |
| **Mark** | A position where a person stands, sits or lies at a given beat. |
| **Move** | A change from one mark to another. |
| **Staging in depth** | People placed at different distances from the camera, so the frame reads front to back. |
| **Lateral staging** | People placed side by side across the frame, at about the same distance from the camera. |
| **Line of action** | The imaginary line through the two people (or the person and the thing) at the centre of a moment. Keeping the camera on one side of it keeps left and right consistent (the 180-degree rule). Daniel Arijon calls it the "line of interest"; this file says line of action. |
| **Screen direction** | Which way a person moves or looks relative to the frame (toward frame-left or frame-right, up or down). |
| **Geography** | The audience's mental map of a place: where the doors, people and key objects are. |
| **Anchor** | A fixed, recognizable object used to keep geography clear across shots (a window, a monitor, a yellow line on the floor). |
| **Master shot** | A wide shot that shows the whole action of a scene and everyone in it. |
| **Coverage** | The full set of shots made of one scene (master, two-shots, singles, inserts) so it can be cut together. |
| **Single** | A shot of one person. A **clean single** has no one else in it; a **dirty single** includes a soft edge of the other person (a shoulder, an ear) in the foreground. |
| **Two-shot** | A shot that holds two people. |
| **Insert** | A close shot of an object or a detail (a hand, a ring, a label) cut into the scene. |
| **Reverse (reverse angle)** | The shot from roughly the opposite direction to the previous one, usually showing the other person in a conversation. |
| **Cutaway** | A shot of something else in the scene (an object, a bystander) cut in between shots of the main action. |
| **Re-establishing shot** | A wider shot, later in a scene, that shows where everyone now is after people have moved. |
| **Eyeline** | The direction and height of a character's look. In a single, the eyeline tells the audience where the person they are looking at stands. |
| **Cheat** | To turn a person or object slightly toward the camera, more than real life would, so the face or object reads, while the audience still believes the original facing. |
| **Truck** | A sideways camera move, parallel to the subject (defined fully in B1). |
| **Shallow focus** | Only a thin slice of depth is sharp; everything nearer or farther is blurred. **Deep focus** keeps near and far sharp together. |
| **Composite** | A single frame made by layering separately made images (a person over a background, a screen image into a monitor). |
| **Plate** | A background image or clip made on its own so that people or objects can be composited over it later. |
| **Focus pull** | Shifting sharp focus during a shot from one distance to another (from a near person to a far one), so the audience's attention moves without a cut. |
| **Dissolve** | A transition in which one shot fades out while the next fades in over it; it usually tells the audience that time has passed (defined fully in A4). |
| **Slugline** | A screenplay's scene heading (for example "INT. SAYE'S HOUSE - KITCHEN - BEFORE DAWN"); this file numbers scenes by counting them. |
| **Grazing angle** | A line of sight that almost skims along a surface instead of meeting it head-on; glass seen at a grazing angle behaves almost like a mirror. |
| **Start frame** | A still image given to a video model as the first frame of a clip (C2 calls it a keyframe). |
| **Proxemics** | Edward T. Hall's study of how people use distance; his four zones are in Section 4.2. |
| **Barrier** | Anything between two people that stops touch or passage: glass, a table, a door, another body. |
| **Threshold** | A doorway, sill or painted line that marks the passage from one space into another. |
| **Floor plan** | A top-down map of a location with every mark, move and camera position written in coordinates. |
| **JSON** | A plain-text format for structured data (names, numbers, lists) that both people and programs can read; used here for the machine floor plan. |
| **Wild wall** | A set wall that can be removed so the camera can stand where the wall would be. In Blender or AI generation, every wall is wild. |
| **Glass state** | Pipeline term for how visible a pane of glass is in a shot (Section 8.1). It applies to every transparent surface, including a helmet visor and a plastic tent. |
| **Mirror state** | Whether an asset appears as itself (NORMAL) or mirrored (MIRRORED); defined in C2 (Section 7.3, where the phases are called eras A, B, C), with the three mirror phases of *The Catch* defined in B1 Section 10.2. |

---

## 1. Core principles

1. **The frame is an argument about importance.** Every composition ranks what is in it. If the ranking does not match the beat (who wants what, who is winning), the shot is wrong even if it is beautiful.
2. **Distance is relationship.** How far apart two people are, and who closed the gap, is the most readable fact in any two-person frame. Change it only on beats that change the relationship.
3. **Movement is a decision.** A person moves because they want something. A move with no desire behind it is noise; a move on the turning point is the turning point made visible.
4. **Structure beats single frames.** Block's central idea: visual intensity has to be planned across the whole film so it can rise with the story. A film where every scene has maximum contrast has nowhere to go.
5. **Hold everything constant except the thing that matters.** When most components stay in affinity, the one that changes is loud. This is how quiet scenes land hard.
6. **Geography is a promise.** The audience must always know where people are relative to each other and to the exits, unless the story wants them lost. Losing them by accident destroys tension.
7. **Barriers do the talking.** Doors, glass, tables and other bodies show separation without a word. Decide for each barrier when it is visible and when it disappears.
8. **Rhyme, do not repeat.** A composition that returns later with one thing changed (the same frame, a different person in it) carries meaning. The identical frame repeated without change is just repetition.
9. **Break a rule once, on purpose.** Short-siding, crossing the line, and dead-centre framing are strong because the rest of the film follows the rules. Record every break and its reason.
10. **Prose gives feelings, not coordinates.** When adapting a story, convert every spatial phrase into a measured mark, and keep the phrase as the reason.

---

## 2. Bruce Block's visual structure

Source: Bruce Block, *The Visual Story: Creating the Visual Structure of Film, TV and Digital Media*, 2nd edition (Focal Press, 2008; a 3rd edition followed from Routledge/Focal Press, dated 2021 on the publisher's page, with the same chapter order: the basic visual components, contrast and affinity, space, line and shape, tone, color, movement, rhythm, story and visual structures, practice). What follows paraphrases his system; quotation marks mark only the short terms he uses.

### 2.1 The seven visual components

Block says every picture, moving or still, is built from the same seven components: **space, line, shape, tone, color, movement, rhythm**. The job is to decide, component by component, how each one will behave across the film. Color and tone are handled in depth by file B2; this file covers the other five and uses tone and color only where composition depends on them.

### 2.2 The principle of contrast and affinity

In paraphrase: the greater the contrast within a visual component, the more the visual intensity increases; the greater the affinity, the more the visual intensity decreases. Contrast is difference (a black silhouette on a white wall; a close-up cut against an extreme wide). Affinity is similarity (a grey figure on a grey wall; two shots of the same size).

Block applies the principle at three levels, and the pipeline should score all three:

- **Within the shot**: is there contrast inside this one frame (deep against flat, big against small, bright against dark)?
- **From shot to shot**: does the cut jump (contrast) or flow (affinity)?
- **From sequence to sequence**: does this sequence as a whole feel different from the one before?

Neither is good or bad. A film needs both: without contrast the audience tires of sameness; without affinity every moment shouts and nothing stands out.

### 2.3 Space: deep, flat, limited, ambiguous

A screen is flat; depth is an illusion made with **depth cues**. The cues Block lists include: perspective (lines converging toward vanishing points), size difference (near things big, far things small), movement toward or away from the camera, textural diffusion (texture detail fades with distance), aerial diffusion (haze), shape change, tonal separation (near and far differ in brightness), color separation (warm and cool), up-and-down position in the frame, overlap, and focus.

- **Deep space** uses many depth cues at once: longitudinal planes, converging lines, big size differences, movement toward and away from the lens, usually a wider lens. Deep space has more built-in contrast, so it tends to feel more intense.
- **Flat space** suppresses depth cues: frontal planes, no converging lines, movement across the frame rather than toward the camera, the camera moving parallel to the planes, often a long lens that compresses distance.
- **Limited space** is Block's middle term: a combination of flat and deep, best pictured as a succession of flat, frontal planes at different depths. Overlap and size difference give some depth, but there are no longitudinal planes running into the distance, and nothing moves toward or away from the lens (people and camera move parallel to the planes, as summaries of Block put it: objects in limited space do not show depth by moving toward or away from the camera). A row of glass rooms seen straight on is limited space. **Consequence:** the moment someone walks toward the lens in a limited-space scene, the space turns deep; save that for a beat that should feel like an intrusion (the figure coming down the ship's chamber, Section 8.7).
- **Ambiguous space** occurs when the viewer cannot work out the size of the place, how objects relate in space, or where the camera is. Block names causes such as a lack of movement (movement is itself a depth cue, so a still frame gives fewer clues), unfamiliar shapes and objects of unknown size, tonal and texture patterns that camouflage edges, mirrors and reflections, and disorienting camera angles. He also notes it is hard to sustain, because audiences quickly find enough clues to make sense of a space. **Practical consequence:** to keep a space ambiguous for more than a few seconds, remove size references (no doors, chairs or people of known height near the unknown thing) and hold the camera still; one known-size object restores the scale at once, which is the tool for ending the ambiguity on purpose.

Block also discusses **surface divisions**: the lines (door edges, window frames, the horizon) that cut the frame into areas. Summaries of the book list their uses: to show similarity or difference between the things in each area, to direct attention to one area, to change the apparent shape of the frame (a doorway turns a wide frame into a tall one), and to add a visual rhythm (a row of window mullions). Their placement is part of composition: a vertical glass edge splitting the frame in half is a surface division that separates two people before anyone speaks.

### 2.4 Line, shape, movement, rhythm (and a note on tone)

- **Line.** Real lines (edges, contours) and implied lines (a look, a pointing hand, the path a moving object traces). Block describes common associations: straight lines feel direct and rigid, curves softer and more organic; in intensity, diagonals are strongest, verticals next, horizontals calmest.
- **Shape.** The circle, square and triangle are the basic two-dimensional shapes (sphere, cube and pyramid in three dimensions); Block treats circle and triangle as the most contrasting pair. What a shape means is set by how the film uses it. It is not fixed: a film can teach its audience that circles mean the bond between two people.
- **Tone.** The brightness of things, independent of color. Block notes that the viewer's eye is drawn to the brightest area of the frame, and also that movement is what captures attention. So: in a still frame, tone is usually the strongest tool for choosing the dominant (see B2); as soon as anything moves, the moving thing tends to win, even if it is darker. If the dominant must be a still object, keep everything else in the frame still.
- **Movement.** Block separates object movement, camera movement, and the movement of the audience's **point of attention**. Across a cut, if the point of attention stays in roughly the same area of the frame, the cut feels smooth (affinity of what Block calls the continuum of movement); if it has to jump, the cut feels harsh (contrast). Use the jump when the story wants a jolt.
- **Rhythm.** Alternation, repetition and tempo, found in stationary objects (a row of windows), in moving objects (footsteps, the three uneven strokes of a pump), and in editing.

### 2.5 The story structure graph and the visual structure graph

Block charts a story as a line over time: exposition, rising conflict, climax, resolution, with **story intensity** on the vertical axis. He then charts each visual component (for example, contrast of space, or contrast of movement) on graphs lined up under the story graph, so the visual intensity can be planned to rise and fall with the story. The usual plan is **parallel**: visual intensity climbs toward the climax. This file also allows deliberate **counterpoint** (visual calm under a story peak, as in the ledge scene of *The Catch*). A review quoted on the publisher's page says the book gives filmmakers tools "to create harmony and counterpoint between the story structure and its visual realization", so counterpoint sits inside Block's framework; but the exact form his examples take was not checked, so treat each counterpoint scene as a pipeline choice that must be justified in one sentence (step 4 below), not as a rule quoted from Block.

Block calls a planned gradual change in a component a **progression** ("visual progression"): for example, space moving from deep to flat across the film, or lines moving from horizontals to diagonals toward the climax. For each component, a plan picks one of three behaviours per stretch of story: **hold it constant** (affinity, so it stays quiet), **progress it** (a slow build the audience feels rather than notices), or **contrast it** (a sudden change on a story event). Summaries of the book report that Block's examples (his "Story Sequence List" and story graphs) show a story's order need not be textbook: exposition can come after a conflict, and a resolution can be very short (*North by Northwest*'s ending is the example cited). So draw the graph from the actual script, not from a template.

A classic worked case of planned progression, from outside Block: Sidney Lumet describes in *Making Movies* (Knopf, 1995) how he made the jury room of *12 Angry Men* (1957, cinematographer Boris Kaufman) feel smaller as the film went on, by moving to progressively longer lenses and by lowering the camera from above eye level, to eye level, to below eye level, so the ceiling came into view. That is a visual structure graph for space, executed.

### 2.6 How to build a visual structure plan (procedure)

1. List the scenes. Score each 1 to 10 for **story intensity across the whole film**. Do not derive this from A2's beat scores: A2 scores beats relative to their own scene, so every scene's turning point scores 5 there. Use this decision list instead; go from the top, and the first row that is true sets the score:
   - **10**: the climax, the scene where the protagonist's main value turns for good. Exactly one scene (or one continuous sequence) gets 10.
   - **8–9**: a life at stake on screen, or a reversal or revelation that changes the whole plan (9 only for the one or two biggest such events before the climax).
   - **6–7**: a turning point that changes a relationship or the protagonist's plan.
   - **4–5**: a scene that turns a minor value, tests someone, or delivers information the audience needs.
   - **2–3**: set-up, travel, aftermath, rest.
   - **1**: nothing at stake (rare; usually cut in the edit).
   Use A2's beat scores only to shape intensity *inside* a scene.
2. Mark the film's peaks and its quietest point. There must be one highest peak (the climax); if two scenes both look like a 10, give the earlier one 9.
3. For each of space, line, shape, movement and rhythm, write one sentence: what it does in the quiet stretches, what it does at the peaks, and what it does at the end, and say whether it is held constant, progressed, or contrasted in each stretch.
4. Name any **counterpoint** scenes and why.
5. Name **reserved** choices: things used only at the peaks (a space type, a line direction, a shape).
6. Write it as a table the shot designer can look up per scene.

### 2.7 A visual structure plan for *The Catch*

Scene numbers count the sluglines of the 25 September 2026 workshop revision (sc1 to sc30), as in A2 and B1.

| Sequence (scenes) | Story intensity | Space type | Line and shape | Movement and rhythm |
|---|---|---|---|---|
| Break-in (sc1–5) | 3 → 7 | Deep: tunnel, the vertical shaft, the corridor seen along its length | Verticals of the shaft; rungs as horizontals; first diagonals on violence (the drip stand) | Iona climbs up the frame; a lateral truck (sideways camera move) along the windows ("Empty bed. Empty bed. Empty bed.") |
| The fall (sc6) | 9 (first peak; the climax keeps the only 10) | Deepest space in the film: looking down the shaft through the grid | Diagonals; the yellow stripe as a horizontal that grows | Maximum object movement against a calm camera (B1 10.1): contrast between camera and bodies |
| The wrong world (sc7–10) | 5 → 6 | Limited and flat: car, street, kitchen seen squarely | Horizontals and frontal planes; the kitchen table as a centre line | Affinity in camera and space, so the only contrast is the reversed world itself (Principle 5) |
| Quarantine and truth (sc11–13) | 4 → 7 | Limited: glass planes stacked in depth, planimetric rows | Rectangles (rooms, monitors, cabinets); the vertical glass edge as a surface division | Stillness; shot size tightens toward "You." (B1 Example 3) |
| The figure (sc14–17) | 3 → 8 → 5 (sc14 is set-up; sc15–16 peak) | Ambiguous: a room where "She can see every corner of it" yet something stands behind her; turning stars on a monitor | A tall black vertical "Taller than the door" | Arrivals with no movement at all (B1: the figure gets no camera move) |
| Receiving room and the ship (sc18–22) | 5 → 6 | sc18 flat and frontal (the yellow line as a threshold across the frame); then ambiguous (no scale, stars below the floor) with one limited-space room (the human rooms) | Curves of the ship against the rectangles of the glass rooms | The chamber's length is the only deep axis; the figure comes down it |
| Sacrifice and fire (sc23–25) | 8 → 9 | From limited to deep as doors open; the chest opening is a scale reversal | The black giant against a small curved vessel: triangle and rectangle give way to circle | Fast movement for the figure only once ("Then it moves, and it is fast.") |
| Ledge and crossing (sc26–27) | 10 (climax) | Ambiguous at its extreme: black, no up, then the visor's wire-frame room as the only reference | One line: the arrow and the room coming down | Counterpoint: a still camera and slow drift at the highest story intensity |
| Return and rest (sc28–30) | 6 → 2 | Flat: planimetric, frontal glass, symmetry | Horizontals; circles (the two rings, the vessel) inside rectangles | Near stillness; the last move between people is two chairs closing the gap (sc29); the last move of all is a folded cloth slid under the vessel (sc30); rhythm of "Three uneven strokes" |

**Reserved choices.** Deep space looking straight down the shaft: sc6 and the security footage of it only. Fully ambiguous space: the ship and the black of the crossing. Perfect symmetry: the two reflection two-shots (Section 8.2, and B1's reserved list). Circles as the frame's dominant: only in the ring inserts of sc10 (which plant the ending) and from sc25 on (the vessel, the rings at the glass).

---

## 3. Composition of a single frame

Two practitioner references sit behind this section. Gustavo Mercado's *The Filmmaker's Eye: Learning (and Breaking) the Rules of Cinematic Composition* (Focal Press, 2010, dated 2011 in some catalogues; 2nd edition, Focal Press/Routledge, 2022; not to be confused with his 2019 companion, *The Filmmaker's Eye: The Language of the Lens*) goes shot type by shot type (sizes from extreme close-up to extreme long shot; conventions such as the over-the-shoulder, establishing, two-shot, group and canted shots; moving shots), giving each one's conventional job and then a film example where the convention is broken for a story reason; use it to check what a framing normally says before choosing to break it. Three of his points are used directly in this file: a film should have an **image system** (visual choices tied to the story's core ideas and motifs, and applied consistently enough that the audience can recognize it; Section 2.6 is this file's version); a subject looking frame-right normally has the eyes near the upper-left crossing of the thirds grid (and the mirror of that when looking left), which gives **looking room** that balances the "weight" of the gaze, while centring a subject who looks sideways, with no looking room, makes the frame feel static and without visual tension, which can be exactly what a scene wants; and **headroom scales with shot size**, so a close-up crops the top of the head while a long shot leaves a lot of space above it (Section 3.5).

Jennifer Van Sijll's *Cinematic Storytelling: The 100 Most Powerful Film Conventions Every Filmmaker Must Know* (Michael Wiese Productions, 2005) catalogues visual conventions in chapters on space, frame, shape, editing, time, sound, transitions, lenses, camera position and motion, lighting, color, props, wardrobe and locations, each convention tied to the story job it does and shown through film examples; use it as a lookup when a beat needs a device and none comes to mind. Her space chapter treats screen direction on three axes: the **X-axis** (left and right across the frame), the **Y-axis** (up and down) and the **Z-axis** (toward and away from the camera, into depth). Her X-axis example is the opening of Hitchcock's *Strangers on a Train* (1951), where the two men are introduced by their feet walking in opposite screen directions toward a meeting they do not know is coming (Section 5.2 turns this into a rule). Neither book is a system for a whole film; Block (Section 2) supplies that.

### 3.1 Where the eye goes first

As a working rule of thumb (not a measured order), the eye is pulled by: a face (especially eyes), movement in a still frame, the brightest area or strongest tonal contrast, a saturated color among muted ones, a figure isolated by negative space, the point where leading lines converge, sharp focus against blur, and the place other characters are looking. Bordwell and Thompson's *Film Art* discusses staging cues of this kind (movement, frontality, centrality, contrast, and characters' glances). When cues disagree, the frame feels confused. **Rule: name the dominant for every shot, and check that at least three cues agree on it and that none of the four strongest cues (movement, the brightest area, the sharpest focus, a face) points at something else.** If a shot is meant to split attention (a speaker in front, a reaction behind), say so and give each of the two exactly one strong cue.

Bordwell's writing on Hou Hsiao-hsien ("Early Hou Hsiao-hsien", davidbordwell.net, first posted 6 June 2016 and reposted 26 February 2024, checked 2026-09-27) describes **blocking and revealing**: small changes of position that hide and then uncover a key figure, steering attention without a cut. It is the most useful staging tool for long takes and for AI clips, where cutting is costly.

### 3.2 The rule of thirds, and its limits

The rule of thirds divides the frame into a three-by-three grid and places key elements on the lines or where they cross. The term was first written down by John Thomas Smith in *Remarks on Rural Scenery* (1797) (Wikipedia, "Rule of thirds", checked 2026-09-27). It is a safe default that produces balanced, slightly dynamic frames, especially for singles with lead room.

Its limits: it says nothing about story. Applied everywhere it makes every frame feel the same, which is exactly the objection George Field raised in 1845: the rule "universalises a particular, the invariable observance of which would produce a uniform and monotonous practice" (quoted on the same Wikipedia page). Use thirds as the neutral baseline so that departures from it (centre, extreme edge, short-siding) register.

**Default placements, as rules** (the baseline every departure is measured against):

- If a single looks or moves toward frame-right, then put the eyes near the upper-left crossing of the grid (about 1/3 of the width from the left, 1/3 of the height from the top); if toward frame-left, the upper-right crossing.
- If two singles are cut together as a conversation, then give them mirrored placements (one on the left third looking right, the other on the right third looking left) at the same shot size and eye height, unless one of them is meant to be cut off (Section 3.5, short-siding).
- If a shot has a horizon or a strong horizontal (a table edge, a sill, the yellow line), then put it on a third line, not across the middle, unless the shot is a reserved symmetrical one.
- If you choose centre or an extreme edge instead, then write the story reason in the shot line (Rule 23).

### 3.3 Centre framing and symmetry

Centre framing puts the subject on the vertical midline. Symmetry mirrors the two halves. Both feel formal, deliberate, and controlled, and in a film that otherwise uses thirds they announce that the image has been arranged.

- **Stanley Kubrick** used one-point perspective (a single vanishing point at frame centre) for corridors and rooms in *Paths of Glory* (1957), *2001: A Space Odyssey* (1968) and *The Shining* (1980). The symmetry reads as order that is cold, or about to break. The video essay "Kubrick // One-Point Perspective" by kogonada (2012; listed on kogonada's own site) collects examples from *Paths of Glory* to *Eyes Wide Shut* (Vimeo, https://vimeo.com/48425421, checked 2026-09-27).
- **Wes Anderson** (cinematographer Robert Yeoman; for example *Moonrise Kingdom*, 2012, *The Grand Budapest Hotel*, 2014) centres people in planimetric frames. Bordwell's definition: "The camera stands perpendicular to a rear surface, usually a wall. The characters are strung across the frame like clothes on a line." He links its rise to long lenses, names Antonioni, Godard, Kitano, Hou and Angelopoulos as other users, and ties Anderson's use to deadpan comedy ("Shot-consciousness", https://www.davidbordwell.net/blog/2007/01/16/shot-consciousness/, checked 2026-09-27).

**When to use it:** for control, ritual, confrontation head-on, a character trapped in a system, or a mirror. **When not to:** as a default style for a naturalistic drama, where it makes the film feel like a diorama.

### 3.4 Balance and imbalance

A symmetrical frame is stable. An asymmetrical frame can still feel settled if a large light area on one side is weighed against a small dark or high-contrast element on the other. Imbalance (everything heavy on one side, a large empty area on the other) makes the audience feel that something is missing or coming. Use imbalance when a character is waiting for, or dreading, the person who is not in the frame.

**Visual weight, as a working order** (heavier first): a face or a figure looking at the camera; anything moving; the brightest or highest-contrast area; a saturated color among muted ones; a large mass; something isolated in empty space; an object in the upper half of the frame (it reads as heavier than the same object lower down). To balance a frame, set a heavier element near the centre against a lighter one farther out, like a seesaw. **Rule:** if the beat is settled, then balance the frame by this list; if the beat is waiting or dread, then pile the weight on one side and leave the empty side facing the door, the glass or the direction the absent person would come from.

### 3.5 Headroom, lead room, short-siding

- **Headroom**: in a close-up or medium shot, a little space above the head reads as normal. Too much makes a person look small and sunk in the frame (useful for defeat); cutting into the top of the head in a close-up is normal and brings intensity. **Working default:** put the eyes on or just above the upper third line of the frame in any single from a medium shot to a close-up; that one number sets headroom automatically and keeps singles matched. Headroom grows with distance (Mercado): in a close-up the frame top crops the top of the head, in a medium shot a small gap remains, and in a full or long shot there is a large space above the head. If a wide shot is meant to make someone look small, then add headroom beyond this default and say why.
- **Lead room**: give space in the direction someone looks or moves, so the look has somewhere to go. In a two-person conversation cut as singles, each single normally gives lead room toward the other person. **Working default:** in a profile or three-quarter single, place the face on the third line on the side opposite the look, so about two-thirds of the frame width is in front of the face.
- **Eyeline**: in dialogue singles, the listener looks just past the lens, on the side where the other person stands. The closer the look passes to the lens, the more intimate the shot; a look straight into the lens addresses the audience and should be reserved (B1 gives Eli his closest, most frontal framing on "You." with his eyes still on the monitor, and saves his first near-lens eyeline for "He has been looking at the screen. Now he looks at her."). Eyeline height must match the bodies: a standing person looks down at a seated one, and the seated one looks up, in both singles.
- **Cheating**: in a profile, a face shows only one eye and half its expression. Unless the reserved profile two-shots need true profile, cheat people about 20 to 30 degrees toward the camera (a three-quarter view) while keeping their eyeline on the other person. Record the true facing in the floor plan and the cheat in the shot line, so both are known.
- **Short-siding**: face the character toward the near edge, with the larger empty area behind them. It creates unease, as if something is behind them or they are cut off from whoever they are addressing. *Mr. Robot* (2015–2019, created by Sam Esmail, cinematographer Tod Campbell) built its visual identity on short-sided, low-in-frame singles with large areas of wall. Use it for one character at a time, on the beats where they are isolated or hiding something.

### 3.6 Negative space

Large empty areas isolate a figure and give weight to what is absent. Negative space must be motivated: an empty chair, an unlit doorway, a bare wall where a photograph would be ("A kitchen with nothing of anybody in it"). In a wide aspect ratio (2.39:1, the ratio chosen for *The Catch* in B1) negative space is always available; the question is which side it is on.

**Which side, as rules:**

- If the empty area is lead room (the look goes into it), then it reads as attention, longing or waiting: use it when the character is looking toward someone or something.
- If the empty area is behind the character (short-siding), then it reads as threat or cut-off: use it only on beats where something is, or might be, behind them.
- If the empty area is above the character (extra headroom in a wide), then it reads as smallness or weight pressing down: use it for defeat or for a place much bigger than the person.
- If the empty area contains a specific thing from the script (the empty chair beside Jude's bed in sc15, "A clean square on the floor where Eli's bed stood" in sc16), then that thing is the point of the shot; keep it in sharp focus and keep everything else in the empty area plain. Empty space with nothing specific in it is only a mood (Rule 23).
- If more than about two-thirds of the frame width is empty, then it is a statement; allow it at most once per scene.

### 3.7 Frame within a frame

Doorways, windows, mirrors, screens and glass panes frame a character a second time. The effect is observation (we are watching them), containment (they are boxed in), or exclusion (they are outside the frame we are in). Two classic uses: the doorway that opens and closes *The Searchers* (1956, John Ford, cinematographer Winton C. Hoch), where Ethan is framed outside the home he cannot enter; and the last shot of *The Godfather* (1972, Francis Ford Coppola, cinematographer Gordon Willis), where a door closes on Kay as Michael becomes the Don. *Rear Window* (1954, Alfred Hitchcock, cinematographer Robert Burks) is built entirely of framed windows, and its climax is the moment the watched man crosses into the watcher's frame. *In the Mood for Love* (2000, Wong Kar-wai, cinematographers Christopher Doyle and Mark Lee Ping-bing) repeatedly frames the lovers through doorways, corridors and curtains, so they are often half-hidden.

**Rule for frames within frames:** one per shot. If a shot already has a frame within the frame (a doorway, a window, a screen), do not add a second framing device (a mirror, bars of shadow) unless the script names both. Framing devices stack into decoration fast.

### 3.8 Leading lines

Edges of tables, walls, floor stripes, rails, cables, a pointing arm, and gaze all carry the eye. Two rules: the lines should arrive at the dominant, not at an empty corner; and a character's gesture can draw a line that the next shot continues (Saye "draws one finger straight down the screen. Then sideways, into the concrete of the wall.").

### 3.9 Layers and depth

Foreground, midground and background let one frame hold two actions: the key action and the reaction to it, or the scene and the thing threatening it. Orson Welles and cinematographer Gregg Toland made this famous in *Citizen Kane* (1941): the boy Charles plays in the snow, seen through the window in the background, while in the foreground his future is signed away. Toland did the same for William Wyler in *The Best Years of Our Lives* (1946), where a phone call ending a love affair happens small in a far booth while a piano duet fills the foreground; André Bazin's essay on Wyler ("William Wyler, or the Jansenist of Mise en Scène") praises this kind of depth staging. Rule: foreground objects must mean something or frame something; random objects placed near the lens for "depth" are clutter.

### 3.10 Open and closed form

The terms go back to the art historian Heinrich Wölfflin (*Principles of Art History*, 1915), and Leo Braudy applied the idea to films in *The World in a Frame* (1976). Closed form suits control and fate (everything the character needs is here, and so is the trap). Open form suits freedom, chaos, or a world larger than the characters. A film can move from one to the other as its hero loses or gains control.

How to write each so a model or an operator can reproduce it:

- **Closed form:** every important person and object fully inside the frame with a clear margin; frame edges fall on walls, door frames or dark areas; people look at things inside the frame; nobody enters or leaves during the shot. Prompt words: "the whole figure within the frame", "framed by the doorway on both sides".
- **Open form:** at least one person or object cut by a frame edge; a look or a movement aimed at something offscreen; people entering or leaving through the frame edges. Prompt words: "cropped by the left edge of the image", "looking off to the right, out of frame".

If a scene is about someone trapped, controlled or observed, then default to closed form; if it is about escape, chaos, or a world that continues beyond the characters, then default to open form; switch on the turning point where control is lost or gained.

### 3.11 Eye-trace across cuts

Walter Murch, in *In the Blink of an Eye* (2nd edition, Silman-James, 2001), ranks six criteria for a cut: emotion (51%), story (23%), rhythm (10%), eye-trace (7%), the two-dimensional plane of the screen (5%), and three-dimensional space of the action (4%). Eye-trace ranks low, but in fast sequences it decides whether the audience can follow. For *Mad Max: Fury Road* (2015), director George Miller reportedly told the camera team to keep the key subject on the centre crosshairs so that editor Margaret Sixel could cut fast without viewers searching for where to look (Vashi Nedomansky, "The Editing of Mad Max: Fury Road", https://vashivisuals.com/the-editing-of-mad-max-fury-road/, checked 2026-09-27). Rule 14 (Section 7.2) turns this into an instruction.

---

## 4. Staging and blocking

### 4.1 Staging in depth versus lateral staging

**Lateral staging** spreads people across the frame at similar distances, like actors on a stage facing the audience. It is clear, flat and formal, and it suits planimetric frames, rows of people facing the same thing (an audience, a jury, a family watching a screen), and comedy of manners.

**Staging in depth** places people at different distances, so the frame has a near actor and a far one. It lets one shot hold an action and a reaction, a speaker and an eavesdropper, a character and the threat approaching. Bordwell's *Figures Traced in Light: On Cinematic Staging* (University of California Press, 2005) studies it in Feuillade, Mizoguchi, Angelopoulos and Hou Hsiao-hsien, and his blog post "Early Hou Hsiao-hsien" shows how Hou, working with long lenses (Bordwell says usually 75 to 150 mm) in films such as *Cute Girl* (1980), *Green, Green Grass of Home* (1982) and *The Boys from Fengkuei* (1983), strings people in rows perpendicular to the camera ("clothesline") or stacks several faces along a diagonal, and moves passers-by across the foreground to block and reveal the main figures (davidbordwell.net, category "Film technique: Staging", checked 2026-09-27).

Bordwell's essay "Intensified Continuity" (*Film Quarterly* 55, no. 3, 2002) describes the modern Hollywood tendency toward fast cutting, extreme lens lengths, close framings in dialogue, and a free-roaming camera. The staging cost is people standing still and talking in close singles, with the camera doing the moving. The pipeline should not default to this: singles are cheap to generate but carry no relationship, and one well-staged wide can do the work of six singles. Two alternatives: the **walk-and-talk** (a conversation carried along a route, as in *The West Wing*, 1999–2006, director Thomas Schlamme), for pressure and momentum; and the **"oner"** (one shot in which the actors' moves create the close, wide and two-shot without a cut; Tony Zhou's video essay "The Spielberg Oner", Every Frame a Painting, 2014), which in AI video works only in short versions, such as one move that turns a wide into a two-shot.

### 4.2 Distance and position show relationship and power

Edward T. Hall, in *The Hidden Dimension* (1966), described four distance zones for North American adults: **intimate** (up to about 45 cm), **personal** (about 45 cm to 1.2 m), **social** (about 1.2 to 3.6 m), and **public** (beyond about 3.6 m). The zones vary by culture, but they give the pipeline numbers to write on a floor plan. A move from social into personal distance is an event; a move into intimate distance is a claim.

Power and relationship cues, in the order they read most clearly:

1. **Who moves and who holds still.** The one who holds still while the other approaches usually has the power (or is refusing the relationship).
2. **Who closes or opens the gap**, and whether the other allows it.
3. **Height**: standing over someone sitting or lying; the person who stands up on a turning point takes the scene. (Camera height is B1's subject; body height is this file's.)
4. **Territory**: who is in their own space, who holds the doorway, who is behind a desk or a table or a glass wall they control.
5. **Facing**: squared up (confrontation or intimacy), side by side (alliance, or avoidance, as in a car), one turned away (withholding), one behind the other (protection or threat).
6. **Interposition**: stepping between two people is the plainest staging act there is. It protects one and challenges the other.
7. **Touch and objects**: handing over, taking, or setting down an object between two people marks the middle of the relationship.

### 4.3 Two people

Daniel Arijon's *Grammar of the Film Language* (Focal Press, 1976; reprinted by Silman-James, 1991) organizes dialogue coverage around the **triangle principle**: with two people on a line of action, camera positions sit at the corners of a triangle whose base runs parallel to that line, all on one side of it. The variations Arijon works through include **external reverse angles** (each person seen over the other's shoulder), **internal reverse angles** (singles from between them, without the other's shoulder), **parallel positions** (two cameras side by side, each seeing one person), **right-angle positions**, and moving in along a **common visual axis** (a closer shot on the same line as the wider one). His firm rule: choose one side of the line and keep to it.

Arrangements for two bodies, and what each says:

| Arrangement | Reads as | Coverage notes |
|---|---|---|
| Face to face, social distance | Negotiation, confrontation | The standard triangle; external reverses |
| Face to face, intimate | Love or threat | Profile two-shot; singles become near-identical close-ups |
| Side by side, both facing the same way (car, bench, window) | Alliance, or avoidance of eye contact | The frontal two-shot through the windshield or window; a mirror or reflection is the only route to eye contact |
| One behind the other, both facing camera | One watches or protects the other, who cannot see them | Staging in depth; focus choice decides whose scene it is |
| L-shape (one turned 90 degrees away) | Partial withdrawal | Lets one face the camera while the other speaks to their profile |
| Separated by a barrier (table, glass, bed) | Relationship through an obstacle | Decide the camera's side of the barrier per beat (Section 8.1) |

### 4.4 Three people

Arijon works through three-person arrangements such as a straight line, an L-shape and a triangle. The practical point for the pipeline: in a three-person scene, the line of action is not fixed. It runs between whichever two people are engaged at that moment, and it swings when the person in the middle turns their head from one partner to the other. That middle person is the **pivot**: whoever stands between the other two controls the scene's eye-lines and is physically "caught between." Before shot design, write down for each beat which pair is engaged and where the line runs.

Common patterns:

- **Triangle** (all three facing inward): balanced, a group decision; the master shot sees all three from outside one side.
- **Line of three facing a shared object** (a screen, a grave, a window): lateral, planimetric, the three as a unit; the object is the "third thing" A2 describes, and it can be filmed from behind them or from the object's side looking back at their faces.
- **Two and one**: two share a side (of a table, of a glass wall), one stands apart. Whoever is alone is either the outsider or the one with power.

**Coverage rule for three.** Write the scene as a sequence of pairs: for each beat, name the engaged pair and the silent third. Then: if the engaged pair changes, the line of action changes, so either show the change in a wider shot (the pivot's head turn inside a held frame) or cut to a shot that re-establishes all three before the new pair's singles. Keep the silent third visible in the engaged pair's shots (soft in a foreground or background) whenever their reaction matters, because a three-hander cut entirely as clean singles loses the third person.

### 4.5 Four or more

Divide the group into subgroups, and give each beat one dominant subgroup. Use staging in depth to rank them (the engaged pair near camera, the others behind), and let a person crossing from one subgroup to another be the beat. In a crowd, one person's stillness against others' movement makes them the dominant.

**Procedure for four or more:**

1. List the people and group them into two to four subgroups by where they are and what they are doing (not by who they are).
2. For each beat, name the dominant subgroup and, inside it, the engaged pair. The line of action for that beat runs through that pair only (Section 4.4).
3. Choose one **master side** for the whole scene: a side of the room from which every subgroup can be seen. Keep every wide on that side; singles obey the line of the beat's engaged pair (Section 4.4), and when that line would put a single on the far side of the room, cut back to a master-side wide first.
4. A person moving from one subgroup to another is a beat. Show the move whole, in a wide or in a shot that follows it, never split across a cut.
5. People outside the dominant subgroup stay still and, where possible, soft in the background, so the eye is not split (Section 3.1). If a background person reacts, give that reaction its own cut or a focus pull, not a second action in the same frame.
6. Around a table, draw the line through the two people who are talking and treat the others as background for those beats; when the talk passes across the table to a new pair, re-establish from the master side before the new singles.

**Worked case: *The Catch*, sc28, the receiving room (seven people).** Subgroups: the mat (Iona, Jude, the vessel; Saye joins it with the padded tray (she "sets it on the mat beside them"), and the hooded nurse joins it later); the wall (Nell, then the technician with the wheelchair); the transport shells (Eli, first sitting, then standing). Dominant subgroup by beat: the mat, from the arrival ("They go down together in a heap") through "You knew I was still there." / "Yes."; the wall, for one reaction cut ("At the wall, Nell sits with her book in her lap. She has heard them."); then the wall again for "Is there a window in my room?", which pulls Saye out of the mat subgroup and across to Nell: that crossing is a beat, so show it whole. Then Saye and Nell walk to the door "passing between Iona and the open transport shells": their bodies block Eli from Iona's side, and as they clear, "Iona looks beyond her. / Eli has got to his feet." This is blocking and revealing (Section 3.1) written into the script: stage Eli so that the passing pair covers him from the master side until they have passed, and do not show him earlier in that stretch. The last beat reduces the room to the Iona–Eli pair with Saye's hand between them (Example 4).

### 4.6 Entrances and exits

- An **entrance** into frame (from an edge) says "arrives from somewhere"; an entrance through a door in the background says "arrives into this place" and gives the door its power. Choosing which door, and whether the entrant is seen first as a shadow, a sound, or a reflection, is a story choice.
- An **exit** that clears the frame completely ends a character's presence; an exit that leaves the door open leaves the question open.
- A character who **appears without entering** breaks the audience's trust in the space. Reserve it for the uncanny.
- A person who **passes between** two others on the way out divides them for a moment; use it when the exit is also a separation.

### 4.7 Moving a scene through a space

For a scene longer than a few beats, give it **stations**: two to four marks, each tied to a movement of the scene (A2's term for a section with its own turning point). The route between stations is part of the story: toward the door (escape), toward the window (longing or looking out), toward the other person (appeal), toward an object (the thing at stake). Every move needs a desire behind it; write it on the floor plan as the move's "why."

### 4.8 Doors, windows, glass and barriers

- A **closed door** is a decision waiting to happen; a door held open is an invitation or a trap.
- A **window** turns the outside into a picture and the inside into a container.
- **Glass** allows sight and forbids touch: the purest barrier on screen, because it removes the excuse of not seeing (Section 8.1).
- A **one-way mirror** separates seeing from being seen. Physically it is a pane with a thin, partly reflective metal coating, and it works only because one side is lit and the other is dark: the lit side sees its own reflection, the dark side sees through. Swap the light and the barrier reverses. *Paris, Texas* (1984, Wim Wenders, cinematographer Robby Müller) stages its climax across a peep-show booth's one-way glass, with the two talking by an intercom phone; in the last conversation Jane turns off the light on her side and can finally see Travis (Wikipedia, "Paris, Texas (film)", checked 2026-09-27; Nastassja Kinski has said she saw only a mirror while shooting). The lesson for this file: in any glass scene, who can see whom is a lighting decision, and a change in who can see whom is a turning point that the light makes (Rules 28 and 29). Watch the film for how glass, phone and reflections carry a two-hander before borrowing specific shots.
- A **table** or **bed** between two people is a softer barrier: it can be crossed, and crossing it is an event.
- A **third body** can be a barrier: the person who "moves between" two others.

### 4.9 How blocking changes at turning points

A turning point should change the physical configuration: someone stands, sits, turns away, turns back, steps in, steps between, steps aside, crosses a threshold, touches, or lets go. After the turning point the line of action has usually moved, so the coverage resets (A2's shot plans reset size at a new movement for the same reason). Test: **if the blocking before and after the turning point is identical, either the scene has no turning point or the staging has missed it.** Stillness can be the change only if the scene before it was full of movement.

---

## 5. Geography and orientation

### 5.1 Establish the space

Before the audience can feel where people are relative to each other, they need a map. Give each new location, early in its first scene:

1. A **master shot** or an establishing view that shows the room's shape, its doors, and everyone's position.
2. At least one **anchor** that appears in most shots (a window, a monitor, a yellow line on the floor, a bed). Anchors let singles and inserts stay oriented without a wide.
3. The **exits**: where people can leave, and which exit matters.

A location can be introduced in pieces (a detail first, the wide later) when the story wants disorientation, but the pieces must add up before the first important move.

### 5.2 Screen direction and the 180-degree rule

If the camera stays on one side of the line of action, a person looking frame-right in their single will be answered by the other looking frame-left, and a person walking frame-right keeps walking frame-right from shot to shot. Crossing the line flips these, which reads as a reversal of direction or a change of side. Ways to cross legitimately: move the camera across the line within a shot; cut to a shot directly on the line (the person walks straight toward or away from camera); cut to an insert or cutaway; or let a character's move create a new line. A related convention, often called the 30-degree rule, says a cut between two shots of the same subject should change the camera angle by at least about 30 degrees (or change size clearly), or the cut looks like a jump.

The rule can be broken as a system: Bordwell and Kristin Thompson documented Yasujiro Ozu's "360-degree space," in which Ozu regularly cut across the line (for example in *Tokyo Story*, 1953). It works because it is consistent. An accidental line cross in one shot of an otherwise classical scene reads as an error.

**Movement across cuts, as rules:**

- If a person leaves a shot through frame-right, then they enter the next shot from frame-left (or walk toward or away from the camera), because the audience reads a person who exits right and enters right as someone who turned back.
- If a person must change direction on screen (turning back, fleeing the other way), then show the turn inside a shot, not across a cut.
- If people have moved to new marks since the last wide, then give a re-establishing shot (a wider frame showing everyone's new positions) before the next singles, or let the singles' anchors show the change.
- If two characters approach each other in separate shots (a meeting), then one moves toward frame-right and the other toward frame-left, because two people moving the same way in consecutive shots read as one following the other. (Van Sijll's X-axis example: in the opening of *Strangers on a Train* the two men's feet travel in opposite screen directions in alternating shots, so the audience expects them to collide before they meet.)

### 5.3 Direction as meaning

Consistent screen direction can carry story. A common convention holds that in cultures that read left to right, movement toward frame-right reads as going forward and toward frame-left as returning or resisting. Treat this as a weak default, not a law; what matters more is that each film keeps its own directions consistent (the pursuer always moves one way, home is always the other way). Vertical direction (up and down the frame) is tied to gravity rather than to reading direction, so it travels across cultures more reliably: rising commonly reads as effort, escape or hope, falling as loss of control or danger. This is still a tendency, and the film's own story decides (in *The Catch*, going UP after the turn is at first the strangest thing in the film).

### 5.4 Geography in *The Catch*

- **Vertical is the film's main axis.** Up means survival ("The cage is going UP," "Iona is going UP"); down means the fall. Keep the world's vertical true in every shaft and ledge shot (B1 10.1 and 10.3).
- **Horizontal rescue direction.** In sc3 Iona moves frame-left to frame-right along the corridor windows to "the last room." In sc20 she moves frame-left to frame-right along the ship's three glass rooms to the same brother. The rhyme tells the audience it is the same errand.
- **Mirror phases change geography.** In phase B (B1 10.2) the world is shown mirrored, so a doorway that was frame-left in phase A appears frame-right. State all screen directions as they appear in the final picture, after any flip, and flag any shot that must show a place seen earlier in another phase. The places seen in both phase A and phase B are the treatment-floor corridor, Eli's room and the maintenance passage (C2 7.3): in phase B, Eli's "last room" is at the other end of the corridor. That is correct, not a continuity error. **The flip also runs the other way, from phase B to phase C**, because in phase C the world is shown as itself again (B1 10.2; C2 7.3). Two world locations are seen in both: the passage, which is the receiving room (sc7 and sc18 in phase B, sc28 in phase C: the tall opening, the yellow line and the RECEIVING wall all swap sides), and Iona's quarantine room ("The same bed" in sc29 and sc30, seen mirrored in sc14 and sc16; the glass to the next room swaps sides). Also correct, and also to be flagged in the shot list so nobody "fixes" it.
- **Floor plans across phases.** Write each scene's floor plan in the orientation the audience will see (the final picture). For a world location that appears in more than one phase, write its **world plan** first: the room as it really is, which is also how it appears in phases A and C. Derive the phase-B plan from it by mirroring east–west: every x becomes (room width − x), and every facing angle θ becomes 180° − θ (for C4's `facing_deg`, the mirrored value is 360° − `facing_deg`). Cameras mirror the same way (position and aim point). Never hand-edit a derived plan, or the phases will drift apart. The ship appears only in phase B and shares the travellers' handedness (C2 7.3), so its plans need no derivation.
- **Anchors per location**: the red tag on the cage gate (sc1–6); the bright sill (shaft); the table with Jude on it (kitchen); the monitor turned toward the glass (sc13); the grey needle box over each bed (quarantine); the rack of six sockets (ship human rooms); the glass-fronted cabinet (collection room); the painted yellow line (receiving room); the word RECEIVING on the wall (sc28).

---

## 6. Floor plans in text

A floor plan in text lets an LLM, a human, and a Blender script share one exact picture of the staging. Write two versions: a short human-readable plan (6.1, with an optional sketch, 6.2) and a machine plan (6.3) that the script in 6.4 turns into a grey 3D scene.

### 6.1 The readable plan (fill this in)

```
FLOOR PLAN: <scene id and slugline>
Units: metres. Origin: <named corner>. +x = <compass direction>, +y = <direction>.
Room: <width> x <depth>, ceiling <height>. Wild walls: <which>.
Fixed objects: <id> at <x,y>, size <w x d x h>, <what it means in the story>
Anchor: <id>, seen in <which shots>
Exits: <door id>, <where it leads>
Start marks: <PERSON> at <x,y>, facing <person/object>, <standing/seated/lying>
Moves (one line each):
  <beat id> <PERSON> from <mark> to <x,y> via <x,y>, ends facing <target>. Why: <desire>
Lines of action: <beats>: <A>-<B>; camera stays on the <side> side
Cameras: <id> at <x,y,height> looking at <x,y,height>, <lens mm>, use: <shot purpose>
Distances at key beats: <A>-<B> <metres> (<Hall zone>)
```

### 6.2 Optional ASCII sketch (0.5 m per cell)

The sketch is for eyes only; the coordinates in 6.3 are authoritative. Here is sc10, Saye's kitchen, at beat B4 (the raised hands). North is up; each cell is 0.5 m; each row is labelled with its lower edge.

```
        x (m): 0     1     2     3     4     5     6
              +------------------------------------+
  y 3.5       | .  .  .  .  .  .  .  .  .  .  .  . |
  y 3.0       | .  .  .  .  .  .  .  .  .  .  . ###|
  y 2.5       | .  .  .  .  .  I  .  .  .  .  . ###|
  y 2.0       | .  .  .  . ============ .  .  E  . |
  y 1.5 A >>> | .  .  .  . ====J=====L= .  .  .  . |
  y 1.0       | .  .  .  .  .  S  .  .  .  .  .  . |
  y 0.5       | .  .  .  .  .  .  .  .  .  .  .  . |
  y 0.0       | .  .  . ____p__m_____f____ .  .  . |
              +------------------------------------+
  I Iona   S Saye   E Eli   J Jude lying on the table (=), head west   L lamp
  ### fridge   ___ counter under the window: p phone, m mint on the sill, f flask
  A >>> camera A, 3.5 m outside the west (wild) wall, looking east along the table
```

### 6.3 The machine plan (JSON)

JSON is used because Blender's built-in Python reads it without extra installs. Every move carries its beat and its reason.

```json
{
 "scene": "sc10 KITCHEN, Saye's house, before dawn",
 "units": "metres", "origin": "south-west inside corner", "axes": "+x east, +y north, +z up",
 "fps": 24, "resolution": [1920, 804],
 "room": {"size": [6.0, 3.6], "height": 2.5, "wild_walls": ["west"]},
 "fixed": [
  {"id": "TABLE",   "centre": [2.8, 1.8],  "size": [1.8, 0.9, 0.75]},
  {"id": "COUNTER", "centre": [3.0, 0.3],  "size": [3.0, 0.6, 0.9]},
  {"id": "FRIDGE",  "centre": [5.7, 2.9],  "size": [0.6, 0.7, 1.8]},
  {"id": "MINT",    "centre": [2.8, 0.1],  "size": [0.15, 0.15, 0.2], "z": 1.0},
  {"id": "FLASK",   "centre": [3.6, 0.35], "size": [0.08, 0.08, 0.25], "z": 0.9},
  {"id": "PHONE",   "centre": [2.0, 0.35], "size": [0.08, 0.15, 0.02], "z": 0.9},
  {"id": "LAMP",    "centre": [3.55, 1.8], "size": [0.2, 0.2, 0.45], "z": 0.75}
 ],
 "people": [
  {"id": "IONA", "eye": 1.60, "at": [2.8, 2.55], "faces": "SAYE"},
  {"id": "SAYE", "eye": 1.58, "at": [2.8, 1.05], "faces": "IONA"},
  {"id": "ELI",  "eye": 1.72, "at": [5.1, 2.0],  "faces": "SAYE"},
  {"id": "JUDE", "lying_on": "TABLE", "at": [2.6, 1.8], "head_toward": [1.0, 1.8]}
 ],
 "moves": [
  {"beat": "B6", "who": "SAYE", "start_s": 40, "dur_s": 1.5, "to": [3.3, 0.85], "faces": "FLASK",
   "why": "her hand goes toward the flask"},
  {"beat": "B7", "who": "SAYE", "start_s": 46, "dur_s": 2.0, "to": [2.8, 0.7], "faces": "MINT",
   "why": "she breaks the mirror pose and turns her back on Iona to fetch the test (the mint)"},
  {"beat": "B7", "who": "SAYE", "start_s": 50, "dur_s": 1.5, "to": [2.8, 1.05], "faces": "IONA"},
  {"beat": "B9", "who": "SAYE", "start_s": 70, "dur_s": 1.5, "to": [2.2, 0.9], "faces": "PHONE",
   "why": "she goes for the phone: containment begins"},
  {"beat": "B10", "who": "IONA", "start_s": 74, "dur_s": 3.0, "via": [[3.95, 2.45]], "to": [4.0, 1.8],
   "faces": "SAYE", "why": "she puts her body on the line between Saye and Eli"},
  {"beat": "B11", "who": "IONA", "start_s": 84, "dur_s": 1.5, "to": [4.2, 2.6], "faces": "JUDE",
   "why": "steps aside: yields to Jude's need"}
 ],
 "cameras": [
  {"id": "A", "pos": [-3.5, 1.8, 1.45], "look_at": [2.8, 1.8, 1.4], "lens_mm": 85,
   "use": "reserved reflection two-shot; Iona frame-left, Saye frame-right, Eli deep centre"},
  {"id": "B", "pos": [2.35, 0.55, 1.5], "look_at": [2.8, 2.55, 1.6], "lens_mm": 50, "use": "Iona over Saye's shoulder"},
  {"id": "C", "pos": [2.35, 3.2, 1.55], "look_at": [2.8, 1.05, 1.58], "lens_mm": 50, "use": "Saye over Iona's shoulder"},
  {"id": "F", "pos": [0.6, 3.5, 2.0], "look_at": [3.6, 1.5, 1.2], "lens_mm": 35,
   "use": "wide for Iona's move (new line of action: Saye-Eli)"}
 ]
}
```

Notes an LLM must follow when writing one: coordinates in metres from a named corner; every person has a start mark and a facing target (a name or a point, never "left" or "right"); every move has a beat id, a start time, a duration and a reason; moves are listed in time order (the script reads them in order, and a facing target uses the target's latest position); every camera is on the correct side of the line of action for the beats it covers. The lamp on the table at [3.55, 1.8] also settles A2's continuity flag for sc10 (Iona "holds the lamp" yet must raise her right hand): she sets it down before the raised hands. (Cameras A, B, C and F above are all on the west side of the Iona–Saye line; F is also on the same side of the Saye–Eli line that takes over at B9, as camera A.)

### 6.4 Blender script: floor plan to grey blocking scene

This script was run on 2026-09-27 with the `bpy` 5.0.1 Python module (Blender's own Python library, which can run without opening the Blender window) on the plan above, and re-run by two fact-check passes the same day: its renders from camera A put Iona frame-left facing right, Saye frame-right facing left, and Eli in the centre background (projected horizontal positions 0.22, 0.78 and 0.45 of the frame width; the first fact-check moved camera A from 50 mm at 4 m to 85 mm at 6.3 m to match B1's lens for the sc29 rings shot, and the composition held; see Example 1 for the lens-family exception this needs); camera F at 80 seconds shows Iona between Saye and Eli (projected 0.38, with Eli at 0.24 and Saye at 0.92). People appear as grey cylinders with a cone "nose" showing which way they face. The renders can go to C2's structure-control route as a **depth or layout guide** (an image model follows the shapes and distances of the grey render), or to a video model that accepts grey 3D "clay" renders for camera and blocking (C1). They cannot drive **pose control** (which follows a stick-figure skeleton): for that, replace the cylinders with posed figures, as C4 does.

**How this relates to C4.** C4's `previs_from_plan.py` is the pipeline's full shot tool (camera moves, depth and pose passes, plan views, stills). This script is the minimal scene-blocking version: use its plan as the **master plan for a location and a scene**, then have the LLM derive one C4 plan file per shot from it. Two conventions differ. C4 places figures by `loc` (feet position, the same as `at` here) and turns them by `facing_deg`, where 0 faces −y and 90 faces +x; this script uses a facing target and the angle θ = atan2(target y − y, target x − x), which is the direction from the person to the target measured counterclockwise from east (+x): 0° faces east, 90° north, 180° west, −90° south. Convert with **facing_deg = (θ in degrees + 90) mod 360**.

```python
# plan_to_blender.py: build a grey blocking scene from a JSON floor plan.
# Run:  blender --python plan_to_blender.py -- sc10_kitchen.json
import bpy, json, math, sys

path = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "plan.json"
plan = json.load(open(path))
fps = plan.get("fps", 24)
sc = bpy.context.scene
sc.render.fps = fps
sc.render.resolution_x, sc.render.resolution_y = plan.get("resolution", [1920, 804])
for ob in list(bpy.data.objects):
    bpy.data.objects.remove(ob, do_unlink=True)

def box(name, cx, cy, sx, sy, sz, z0=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, z0 + sz / 2))
    ob = bpy.context.object
    ob.name, ob.scale = name, (sx, sy, sz)
    return ob

W, D = plan["room"]["size"]
box("FLOOR", W / 2, D / 2, W, D, 0.02, -0.02)
points = {}
for f in plan["fixed"]:
    x, y = f["centre"]
    box(f["id"], x, y, *f["size"], z0=f.get("z", 0.0))
    points[f["id"]] = (x, y)
for p in plan["people"]:
    points[p["id"]] = tuple(p["at"])

def facing(frm, target):
    tx, ty = points[target] if isinstance(target, str) else target
    return math.atan2(ty - frm[1], tx - frm[0])

people = {}
for p in plan["people"]:
    x, y = p["at"]
    if "lying_on" in p:  # a body lying on a surface, head toward a point
        t = next(f for f in plan["fixed"] if f["id"] == p["lying_on"])
        z = t.get("z", 0.0) + t["size"][2] + 0.15
        bpy.ops.mesh.primitive_cylinder_add(radius=0.18, depth=1.75, location=(x, y, z))
        ob = bpy.context.object
        ob.rotation_euler = (0, math.pi / 2, facing((x, y), p["head_toward"]))
    else:
        h = p["eye"] + 0.12
        bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=h, location=(x, y, h / 2))
        ob = bpy.context.object
        bpy.ops.mesh.primitive_cone_add(radius1=0.08, depth=0.25, location=(0.3, 0, p["eye"] - h / 2),
                                        rotation=(0, math.pi / 2, 0))
        bpy.context.object.parent = ob            # the "nose" shows which way the person faces
        ob.rotation_euler.z = facing((x, y), p["faces"])
    ob.name = p["id"]
    people[p["id"]] = ob

def key(ob, frame):
    ob.keyframe_insert(data_path="location", frame=frame)
    ob.keyframe_insert(data_path="rotation_euler", frame=frame)

for ob in people.values():
    key(ob, 1)
for m in plan.get("moves", []):
    ob = people[m["who"]]
    f0 = 1 + round(m["start_s"] * fps)
    f1 = f0 + round(m["dur_s"] * fps)
    key(ob, f0)                                   # hold position until the move starts
    stops = m.get("via", []) + [m["to"]]
    for i, (x, y) in enumerate(stops, 1):
        ob.location.x, ob.location.y = x, y
        if i == len(stops):
            ob.rotation_euler.z = facing((x, y), m["faces"])
        key(ob, f0 + round((f1 - f0) * i / len(stops)))
    points[m["who"]] = tuple(m["to"])
    sc.frame_end = max(sc.frame_end, f1 + fps)

for c in plan["cameras"]:
    cam = bpy.data.objects.new("CAM_" + c["id"], bpy.data.cameras.new("CAM_" + c["id"]))
    sc.collection.objects.link(cam)
    cam.data.lens, cam.data.sensor_width = c["lens_mm"], 36.0   # full-frame equivalent
    cam.location = c["pos"]
    aim = bpy.data.objects.new("AIM_" + c["id"], None)
    sc.collection.objects.link(aim)
    aim.location = c["look_at"]
    con = cam.constraints.new(type="TRACK_TO")
    con.target, con.track_axis, con.up_axis = aim, "TRACK_NEGATIVE_Z", "UP_Y"
    sc.camera = sc.camera or cam
```

To get pictures out, append these lines to the script (tested the same day: 4 cameras × 7 moments = 28 grey stills from the sc10 plan). With the pip `bpy` module instead of the Blender app, run `python plan_to_blender.py -- sc10_kitchen.json`.

```python
# render_stills.py: append to plan_to_blender.py.
# Saves one grey still per camera at 1 s and at the end of every move, into ./stills/
import os
os.makedirs("stills", exist_ok=True)
sc.render.engine = "BLENDER_WORKBENCH"                 # fast grey shading, no lights needed
frames = sorted({1 + fps} | {1 + round((m["start_s"] + m["dur_s"]) * fps) for m in plan.get("moves", [])})
for c in plan["cameras"]:
    sc.camera = bpy.data.objects["CAM_" + c["id"]]
    for f in frames:
        sc.frame_set(f)
        sc.render.filepath = os.path.abspath(f"stills/{c['id']}_f{f:05d}.png")
        bpy.ops.render.render(write_still=True)
```

Limits: the script does not animate cameras, build walls, handle stairs, or pose bodies; a person turning in place needs a move with the same "to" point. A turn that crosses due west (from just under +180° to just over −180°) will spin the long way round; if that shows, add or subtract 360° by hand. Swap cylinders for a rigged figure when poses matter (raised hands, kneeling).

**Mirrored phases.** The plan is written in final-picture orientation (Section 5.4), so its grey render is already the layout the audience will see: use it as it is for composition checks. The flip belongs to the image-generation step. If C2's route generates a mirrored-world plate un-flipped and then flips it (C2 Recipe R5 and worked example W3), flip the grey render horizontally before using it as that plate's layout guide, and flip nothing else. Never mirror a plan's coordinates by hand; derive a second-phase plan only by the rule in Section 5.4.

---

## 7. Translation table and decision rules

### 7.1 Translation table: story meaning to composition and staging

These are starting points, not recipes. Taken together they would produce the stock version of every film (a lonely figure in a sea of empty wall, a couple split by a door frame, bars of shadow for a trapped person). Use them this way: pick **at most one** composition choice and **one** staging choice per moment; prefer the staging choice, because it comes from the characters' own wants; and tie the choice to a specific object, line or action in the script (the monitor, the drip stand, "Iona moves between her and Eli"), never to a mood word alone.

| Story meaning | Composition choices | Staging choices |
|---|---|---|
| Control, order, a system that holds people | Centre framing, symmetry, planimetric, closed form | Lateral staging; people on fixed marks; nobody crosses the frame's centre line |
| The system is about to break | Symmetry with one element out of place; one-point perspective with something at the vanishing point | One person still while the others move, or the reverse |
| Isolation | Negative space; small figure; excess headroom | Distance beyond social (over 3.6 m) from everyone; back to the others |
| Something behind / unseen threat | Short-siding; imbalance with the empty side behind the character | Character faces a wall or window; the threat's entrance is behind them |
| Being watched / studied | Frame within a frame (window, screen, glass); camera outside the barrier | The watched person in a lit box; the watcher in a darker, larger space |
| Two people united | Two-shot with shared lead room; both in one frame on one plane | Side by side facing the same thing, or the gap closing to personal distance |
| Two people divided | A surface division (door edge, glass edge) between them; separate singles with no shoulder in frame | A barrier or a third body between them; distances held |
| Power held | Dominant by height, centrality or tone | Holds still, holds the doorway, stands while the other sits |
| Power shifting | Composition tilts from one side's weight to the other's across the scene | The move on the turning point: the weaker one stands, steps in, or takes the object |
| Protection | One body in front of another in depth | Interposition: stepping between the threat and the protected |
| Secrets, withholding | Partial framing (a hand out of frame, a face half-hidden by a foreground edge) | Turned away; hands hidden; standing behind the person they deceive |
| Revelation | Blocking and revealing: a body moves and uncovers the thing | A step aside, a door opening, a turn toward camera |
| Longing across distance | Leading line from one to the other; the far one small in the background | Facing each other across a gap that does not close |
| Reconciliation | Symmetry returning; matched singles; one frame for both | The gap closing by both moving (not only one) |
| Being lost, reality unreliable | Ambiguous space; reflections; no anchor | Entrances and exits that do not connect; a person appears without entering |
| A world turned over | Frames repeated exactly with one element reversed | The same marks as an earlier scene, reversed or swapped |
| Grief, aftermath | Flat space, horizontals, stillness; affinity in everything | Few moves; people sitting or lying; the empty mark where someone was |

### 7.2 Decision rules

**How to read "consider".** Rules 1 to 22 are defaults. Apply each one whenever its "if" is true, unless you can write a one-line reason, naming something in the script, for doing otherwise; record that reason in the shot or scene line. Rules 23 to 29 have no such exception. When two defaults conflict, the one that follows from the characters' wants (staging) beats the one about the picture (composition), and a reserved choice (Section 2.7, B1 9.2) beats both.

1. **If** a scene has one turning point, **then consider** one clear change of configuration on that beat (a stand, a step, a turn, a crossing), **because** the audience reads bodies before words, and the change is the turn made visible.
2. **If** a scene's value is about closeness or distance between two people, **then consider** writing their distance in metres at every beat and changing it only on beats that change the value, **because** random drift in distance reads as meaning the scene does not intend.
3. **If** one character holds the power in a scene, **then consider** keeping them still while the other moves, **because** stillness under pressure reads as control.
4. **If** a character steps between two others, **then consider** staging it in one wide frame from a side where all three are visible, **because** interposition only reads when the viewer sees both people it separates.
5. **If** a scene has three people and one is physically between the other two, **then consider** making that person the pivot of the coverage (the one whose head turn moves the line of action), **because** the person in the middle is the one both others must look past, which makes them the hinge of every exchange.
6. **If** a scene is mostly talk with little movement, **then consider** a single "third thing" (a screen, a document, a window) that all can face, and stage laterally toward it, **because** it gives the eyes a shared target and lets the turn be a turn away from it.
7. **If** the scene is at a story peak, **then consider** raising contrast in no more than two components at once and holding the others in affinity, **because** contrast in everything at once flattens into noise.
8. **If** a scene follows a high-contrast sequence, **then consider** strong affinity (flat space, stillness, horizontals), **because** Block's sequence-to-sequence contrast needs a quiet side to be felt.
9. **If** the same place or configuration returns later in the story, **then consider** repeating the earlier composition exactly (same camera position, lens, marks) and changing one thing, **because** the one change becomes the meaning.
10. **If** a character is hiding something, **then consider** short-siding them or keeping one hand or half the face out of the frame, and give them their first open, centred frame when the truth comes out, **because** the composition then pays off the secret (B1 applies the same logic to lens and angle).
11. **If** a barrier stands between two people, **then consider** deciding per beat which side of it the camera is on, and cross to the other side only when the point of view shifts, **because** the camera's side is the audience's side.
12. **If** you use centre framing or symmetry, **then consider** reserving it for moments of ritual, confrontation, or mirroring, **because** used everywhere it stops meaning anything.
13. **If** a frame contains foreground objects, **then consider** whether each one frames, blocks, or comments on the subject, and remove the rest, **because** decorative foreground clutter competes with the dominant.
14. **If** a shot is under two seconds, **then consider** placing its dominant where the previous shot's dominant was (in the same third of the frame width, and no more than about a sixth of the frame width away), **because** the eye has no time to search (eye-trace). If the cut is meant to jolt, make the jump at least half the frame width, so it reads as intended rather than sloppy.
15. **If** a new location appears, **then consider** a master shot and a named anchor before the first important move, **because** a move means nothing if the audience does not know where it goes.
16. **If** you must cross the line of action, **then consider** doing it inside a shot (a camera move or a character's move that re-draws the line) or on a beat that reverses the relationship, **because** an unmotivated line cross reads as confusion.
17. **If** a character enters, **then consider** whether they arrive into the frame (an edge) or into the place (a background door), and choose by what the entrance means, **because** the door gives the place ownership.
18. **If** a character should feel uncanny, **then consider** letting them appear in the frame without entering it, and never showing them cross a threshold, **because** it breaks the rules the audience uses to feel safe.
19. **If** a prose source gives a distance as a feeling ("the good distance"), **then consider** converting it to a number on the floor plan, naming the mark, and reusing the same number whenever the phrase returns, **because** a named mark becomes a motif the camera can repeat.
20. **If** a gesture is a motif (a hand on glass), **then consider** shooting every occurrence with the same framing and escalating only one variable each time, **because** repetition with variation builds meaning where repeated emphasis becomes cliché.
21. **If** a shot will be generated by an AI model, **then consider** reducing its blocking to one move per clip and fixing the start composition with a start frame (a generated still or a Blender render), **because** current models handle one clear action far better than choreography (C1).
22. **If** a location is mirrored in one phase and not another (*The Catch*), **then consider** writing screen directions for the final picture only, **because** a flip done later will otherwise silently reverse your plan.

**Restraint and specificity rules** (these are firm, not "consider"):

23. **If** a shot's written reason names only a mood ("lonely", "tense", "to show isolation"), **then** rewrite it to name the scene's own object, line or action that carries that mood (the empty chair beside Jude's bed, the needle climbing), **because** mood-only reasons produce stock images that could sit in any film.
24. **If** a symbolic image is not in the source (rain on a window, a wilting plant, a ticking clock, a caged bird, bars of shadow from blinds), **then** do not add it, **because** the source's own recurring objects (in *The Catch*: glass, hands, the needle, the flask, the F) already carry the meaning, and an invented symbol competes with them.
25. **If** one expressive device is already working in a shot (a barrier, a reflection, a frame within a frame, short-siding, a tilted horizon), **then** keep every other component neutral in that shot, **because** two devices at once read as the film pointing at itself. (A stricter, single-frame version of Rule 7. Exception: the script itself stacks them, as in sc17's hand on glass beside a monitor.)
26. **If** a composition would still make sense pasted into a different film ("the any-film test"), **then** find the detail from this script that only this film has and put it in the frame, or simplify the shot to plain coverage.
27. **If** the script repeats a gesture or an image, **then** repeat the framing and change exactly one thing (Rule 20), and never add an extra occurrence the script does not have.

**Physics and geometry rules for glass and reflection** (details in Section 8.1):

28. **If** a shot needs A's reflection to lie over B, who is on the far side of a pane, **then** find A's mirror twin (A's position reflected through the glass plane, so the same distance behind the glass as A is in front of it), draw the straight line through the twin and B, extend it through the glass to A's side, and put the camera on that extension; keep B's side darker than A, **because** a reflection appears exactly where the mirror twin would be, and glass reflects only a few per cent of the light, so the reflection shows only against a dark background. The easiest case: A and B stand directly opposite each other at the same distance from the pane, and then A's reflection lands on B from any camera position on A's side. If B and A's twin are the same distance behind the glass but side by side, the line through them runs parallel to the glass and no camera can line them up: move one of them.
29. **If** a shot must look through glass with no reflection (glass state CLEAR), **then** keep the camera's side darker than the far side (dim the near room or hang black cloth behind the camera; in a prompt, "no reflections on the glass"), **because** reflections come from light on the camera's side. A polarizing filter (a filter that blocks light vibrating in one direction) removes glass reflections completely only when the camera sees the glass at about 56 degrees from straight-on (Brewster's angle for ordinary glass: at that angle all the reflected light vibrates in one direction, so the filter can block all of it), still cuts them to roughly a third or less between about 40 and 70 degrees, and does almost nothing near square-on, where most THROUGH shots are made; so for a square-on CLEAR shot, control the light, not the filter.

---

## 8. *The Catch*: the glass-and-mirror system and the key rooms

The script is built on barriers you can see through: the corridor windows, the quarantine glass, the specimen cabinets, the monitors, the tablet, the visor, the clear shell round a bed, the clear container with Iona's shirt, the plastic tent, and finally the glass vessel with the animal inside. It is also built on mirrors: the world reversed, the raised "wrong hand," the rings. The system below gives every glass and every mirror moment a small set of named choices, so they accumulate instead of repeating.

### 8.1 Glass states and the camera's side

Every shot that contains a barrier of glass gets a **glass state** and a **camera-to-glass position**.

| Glass state | What the audience sees | Use for |
|---|---|---|
| **CLEAR** | Only the frame edge of the pane; no reflections | Connection winning over the barrier |
| **MARKED** | The pane made visible: a smear, a label, a hand print, a highlight, a crack | The barrier matters in this beat |
| **REFLECTING** | A reflection overlapping the person behind the glass (two images in one plane) | Doubling, identity, the watcher seen in the watched (Block's ambiguous space) |
| **SCREEN** | Glass that shows a recorded or remote image (monitor, tablet, visor) | Distance in time or place: the truth arriving second-hand |
| **BROKEN / OPEN** | Cracked, shattered, or doors opened | The barrier breached, by force or by consent |

| Camera-to-glass position | What it does |
|---|---|
| **THROUGH** | Camera on one side, looking through at the other. It puts the audience on that side. |
| **ALONG** | Camera looking along the plane of the glass, which becomes a vertical line in the frame between two people in profile. It gives both sides equal weight. |
| **ANGLED** | Camera turned roughly 30 to 60 degrees away from square-on to the pane. It lets the camera choose what is reflected (something to the side, rather than the camera itself); past about 50 degrees it also makes reflections noticeably stronger. The usual choice for REFLECTING. |

**How glass actually behaves (so the choices above are physically possible).** Glass reflects at every angle, including square on: the pane shows whatever stands at the mirror position, where the angle of incidence equals the angle of reflection. Square on, the camera sees its own reflection, which is why THROUGH shots are usually cheated a few degrees off square. Clean glass reflects about 4 per cent of the light at each of its two surfaces when seen square on; the share stays under about 10 per cent up to 60 degrees from square-on, then climbs quickly (about a quarter at 75 degrees) toward total reflection at a grazing angle (Fresnel's equations, standard optics). Two consequences for writing shots:

- A reflection is only visible where the scene behind the glass is **darker** than the reflected thing. For REFLECTING, light the reflected person and keep the far side dim; for CLEAR, do the opposite (Rules 28 and 29).
- Looking ALONG the glass (grazing angle) makes the pane itself a strong mirror, so an ALONG shot will show reflections of both people unless the pane is very close to edge-on and dark behind. In the reserved profile two-shots this is useful: a faint doubled image in the dividing line is acceptable, but it must not cover a face.

**Every transparent surface in *The Catch* takes a glass state**, not only windows:

- **Iona's helmet visor (sc18–sc28).** From sc18 on she wears a pressure suit and helmet ("Her own two gloves in her helmet light"; "Breath in the helmet"), so on the ship every shot of her face is a shot through glass. Default the visor to CLEAR for every close-up where her face must be read, with her face lit from inside the helmet so it stays brighter than what the visor would reflect. A monster or a planet reflected in a helmet visor is one of the most worn images in space films, and the script has already given its one reflection of the figure to a curved container (sc21, below). So: no story content reflected in the visor by default; allow REFLECTING on the visor at most once in the film, on a beat where the script puts something behind her that the audience must see and no other framing can show it, and never over her eyes. Soft, unreadable room highlights on the visor are fine (they are MARKED, not REFLECTING). The visor's display is its SCREEN state; C2 composites it, and it must never cover her eyes in a close-up on a decision beat.
- **Protective hoods (sc18, sc28).** Saye "inside a protective hood" and the hooded technician and nurse: their faces are behind a second clear layer. In sc28, when "Saye takes her helmet in both hands and holds it still", two clear barriers meet face to face; keep both CLEAR, and let their reflections stay soft.
- **The plastic tent (sc29, sc30).** "Iona inside a tent of clear plastic." Soft plastic is a MARKED surface by nature (creases, highlights). Stage the tent against the partition glass so that, from the camera, Iona and Eli are separated by one visible barrier, not two; if the tent must stand away from the glass, frame the rings shot so the plastic's edge sits outside the frame or exactly on the centre line with the glass.
- **The clear shell round a bed, the specimen containers, the vessel.** Same states. The shell closing is BROKEN/OPEN in reverse (a barrier created); film it THROUGH, never ALONG, so it reads as a wall arriving.

**Default rule.** The camera is on Iona's side of the glass. It crosses to the far side only when the point of view shifts: in sc13, for the master that shows the three of them as a row of specimens from Saye's side (Example 2), and once in sc23, for a sentence the script writes from Eli's side (Example 3). In sc20 and sc23, where Iona is now the one outside the glass, staying with her puts the camera where Saye's camera stood in sc13. ALONG is reserved for the two reflection two-shots (8.2) and, in a deliberately imperfect version, for sc28 (Example 4).

**Script moments that already name a state.** "The glass cracks corner to corner and holds." (sc3, BROKEN). "In the curve of the container: the room behind her, and the figure standing in it. Close enough to touch." (sc21, REFLECTING: the figure is revealed only as a reflection in a curved container, so shoot ANGLED, with the reflection sharp and Iona's hand soft in the foreground). Physics to respect: a small convex surface (one that bulges toward the viewer, like the outside of a jar) shows a wide, shrunken, bent view of the room, and the reflected image sits just behind the surface, so focus on the container itself to make the reflection sharp. For the figure to read as "Close enough to touch" in so small a mirror, it must stand close behind her and fill a large part of the curve; a figure at the far side of the room would be a speck. The script makes this a suit-camera image ("Iona angles the suit camera towards the shelf"), so the frame belongs to her camera, not the film's. "Saye turns a monitor to face the glass." (sc12, SCREEN seen through CLEAR: two layers).

### 8.2 The mirror geometry, stated so it can be checked

**Profile rule.** A person facing frame-right shows the camera their right side, so their right hand is the one nearest the camera; a person facing frame-left shows their left side. This one fact makes the mirror moments checkable.

**The reflection two-shot** (reserved; B1 lists it among the film's reserved choices). Camera ALONG the plane between the two people (the table in sc10, the glass in sc29), level, 85 mm from well back (B1), both in profile at equal distance from the frame's centre, the centre line running through whatever divides them.

- **sc10, the kitchen.** "They stand facing each other across the table like a woman and her reflection, each with the wrong hand in the air." (The lens needs one exception to B1's lens family; see Example 1.) Iona frame-left facing right; Saye frame-right facing left. Each raises **the hand nearest the camera**: for Iona that is her right; for Saye, who is shown mirrored in phase B, it reads on screen as her left. Both raised hands on the same side of the frame is what makes it a reflection. Their rings are on the lowered, far hands, so the rings go in a separate insert (A2 sc10.B4.b). Floor plan and full staging: Section 6 and Example 1.
- **sc29, the rings.** "She lifts her own left hand and lays it against his, through the glass. The two rings sit directly across from each other, like a ring and its reflection." To make the ringed hands the ones nearest the camera, Iona is **frame-right facing left** (her left hand nearest camera) and Jude is **frame-left facing right** (his right hand nearest camera; he is shown mirrored in phase C, so his ring reads on his right hand). The composition is the kitchen's, reversed left to right. That reversal is motivated: Iona herself has been turned back, and the film's last reflection is a reflection of its first. Floor plan and camera: Section 8.8.

**The literal mirror.** The only real mirror in the script is the car's rear-view mirror in sc9: "A red light. Iona finds his eyes in the mirror." (Section 8.5.)

### 8.3 Hands on glass: an escalation ladder

A hand pressed to glass is a stock image in prison-visit and hospital scenes. The script uses it anyway, many times, and gets away with it by changing one thing each time. The composition must protect that: same insert framing each time (the pane seen THROUGH, square on, the hand filling about a third of the frame height, at 50 mm per B1's family), no push-in, no score swell, and only one new element per step.

| Step | Scene and exact text | What is new | Composition |
|---|---|---|---|
| 1 | sc3: "He lifts the strapped hand as far as the strap allows. Lets it fall." | A hand that cannot reach the glass | Wide THROUGH the window; the hand small; the glass MARKED by a highlight across the pane |
| 2 | sc11: "Through another window, Eli raises a hand. Iona raises her bandaged hand back." | Two hands, two panes, no touch | Wide; two layers of glass between them; neither hand touches |
| 3 | sc12: "Iona puts her palm against the glass, beside the restored F." | First palm on glass, toward knowledge, not a person | The standard insert, established here |
| 4 | sc17: "Iona puts her hand flat on the glass, as near to the monitor as she can get." | Toward her family, through glass and a screen | Standard insert with the monitor SCREEN behind the glass |
| 5 | sc25: "The animal presses a limb to its window." | The creature makes the human gesture | The standard insert, matched exactly: framed like the humans' hands, the gesture invites the audience to start reading the animal as a person |
| 6 | sc26: "The animal touches the moving picture through the glass." | Toward a picture, as Iona did in step 4 | Match step 4's framing |
| 7 | sc29: Jude "Lays his good hand flat on it." / Iona's left hand "against his, through the glass." | The only time two hands meet at one pane | The reflection two-shot (8.2), then the standard insert with both hands |

**Do not add** hand-on-glass moments the script does not have. Seven is already near the limit of what a short film can hold before it becomes heavy-handed.

**Keep the neighbours out of the ladder.** The script has other raised or flat hands that are not hands on glass: the raised hands of sc10 (the reflection two-shot, 8.2); "Jude has time to raise one hand" inside the closing shell (sc23); the figure that "puts its hand flat against its own chest" before it opens (sc25); Eli who "lifts one hand and tries to smile" (sc28); Saye's hand "between them" (sc28, Example 4). Do not frame any of these with the ladder's standard insert, or the ladder loses its count. Two of them deserve a quiet link instead: Jude's hand behind the shell in sc23 is the one time a raised hand is seen through glass as the glass takes the person away, so play it inside Iona's wide, small in frame, not as an insert; and the figure's flat hand on its own chest is the flat-hand gesture turned inward, just before the film shows what is behind that surface, so shoot it square-on to the chest from Iona's eye height (B1's rule for the figure), framed at the figure's scale, not the insert's.

### 8.4 Crossings: what may pass through the glass

Bodies cannot cross the glass; objects can, through a drawer, a hatch or the courier. Compose every crossing as the same kind of insert, the object passing through the plane from one side to the other: the nurse's "sealed gloves of a service hatch" (sc11); the meal passed "through the hatch" (sc12); "She puts a radio in the drawer that goes through his wall. He takes it out on his side." (sc20); the courier pod (sc18 onward); and in sc29 the crossing that does not happen: "Iona breaks a bread roll. Moves half towards the transfer drawer. / Sees the label on his tray. Stops." The last one should be framed exactly like the sc20 radio insert, with the half-roll stopping short of the drawer.

A second pair to rhyme: breaking and mending. The drip stand cracks the window "corner to corner" (sc3); Iona's cylinder cracks the figure's "transparent cover" (sc16); in sc25 she finds that "The edge of the crack has cut the tube", and seals the leak with repair tape, keeping "her hand where it is until the thread stops". Frame the taping as the sc3 crack insert was framed, so the violence and the repair sit side by side in the audience's memory.

### 8.5 The car (sc9): a two-hander that cannot face itself

**Marks.** Iona in the driver's seat (on the "wrong" side; phase B shows the car mirrored). Eli in the front passenger seat, "twisted round, holding the sleeve on him with one hand and the flask with the other." (The script does not name his seat; the front is the only place left, since Jude is "lying across the back seat.") Nobody can move, so the staging is heads, eyes and hands.

**Which side is which, worked out.** The script's English ("gearstick", "torch", "stencilled") suggests a country that drives on the left in right-hand-drive cars; confirm with the writer, because everything below flips if not. On that assumption, Iona's own car has its wheel on the right. In phase B the car is shown mirrored, so the wheel is on the car's left. In a frontal two-shot through the windshield (camera outside, in front of the car, looking back at the occupants), the car's left side is the camera's right: **Iona is frame-right, Eli frame-left.** Her beat "Reaches for the gearstick. / Hits the door." is a reach with her left hand toward where the gearstick sits in her own car, which in the mirrored car is the door. So the reach goes **away from Eli, toward the frame edge**, and ends on the door; stage it in the two-shot so the audience sees the hand miss. "Her own coffee cup in the holder, on the wrong side of the gearstick" (sc8, when she opens the door) is the insert that sets up the same flip.

**Staging logic.** Side-by-side staging means no eye contact without a turn or a mirror. Eli's body faces backward (toward Jude, toward what he did); Iona faces forward (the road she cannot read). Their only face-to-face path is the rear-view mirror. Make it physically possible: a rear-view mirror is aimed at the rear window, so it shows the driver the middle of the car behind the front seats, not a front passenger sitting upright. Stage Eli leaning back between the front seats to keep the sleeve pressed on Jude, so his head sits in the middle of the car, inside the mirror's view; when he looks up, Iona "finds his eyes in the mirror." A mirror works both ways: if she can see his eyes, he can see hers, so "He looks down at the flask in his hand for a long time" is him breaking a look he could hold.

**Coverage.** (a) Frontal two-shot THROUGH the windshield, glass MARKED by passing light; keep reflections as soft shapes with no readable text (C2 handles reversed text as insert graphics). (b) Iona's view of the road, backwards signs. (c) The key shot: the rear-view mirror as a frame within a frame, holding Eli's eyes, with Iona's cheek soft at the frame's edge and the flask low in frame. (d) Eli in profile from Iona's side, his face turned away from her. Hold (c) through "He looks down at the flask in his hand for a long time." The question "Are we going to be all right?" is asked into a mirror; in sc23 it is asked again through glass, with roles reversed (Example 3).

### 8.6 The glass partition (sc13): three on one side, one on the other

Saye outside the glass with the monitor turned toward it; inside, Jude in bed facing the glass, Iona on one side of him (she "moves his water into reach of his good hand"), Eli on the other. Jude is physically between the siblings and is the scene's pivot. The three face the monitor as a lateral row: a family as an audience, and, from Saye's side, a row of specimens behind glass. Full staging in Example 2. (The script does not say Jude is in a bed here; he is post-surgery and asleep beside Iona in sc12, so a bed with a raised back is the inference.)

```
FLOOR PLAN: sc13 INT. QUARANTINE - GLASS PARTITION - LATER
Units: metres. Origin: south-west inside corner of the family's room. +x = east, +y = north (toward the glass).
Room (family side): 5.0 x 4.0, ceiling 2.7. Glass partition along y = 4.0, full width; Saye's side y 4.0 to 7.0.
  Wild walls: south (behind the family), for the reverse.
Fixed objects: BED centre (2.5, 2.0), 0.9 x 2.0, head end at y 1.0, back raised: the pivot's place
  MONITOR (1.55, 4.45), 0.6 wide, screen facing south through the glass, centre 1.3 m high: the evidence, the third thing
  SCREEN2 (0.6, 4.45), facing south: the two dishes, "The grey, closed over the drop"
  FLASK beside the monitor (1.95, 4.5), later into a sealed carrier; WATER on the bed table (1.9, 1.4)
Anchor: MONITOR, in the master, the reverse and every wide
Exits: none used. Nobody enters or leaves; the barrier holds for the whole scene.
Start marks: JUDE in bed, head at (2.5, 1.3), eyes 1.1 m high, facing MONITOR
  IONA seated (1.6, 1.8), facing MONITOR; ELI seated (3.4, 1.8), facing MONITOR
  SAYE standing (1.05, 4.2), between the two screens and just behind the glass, facing east to the monitor
Moves:
  early  IONA leans to (1.9, 1.6) and back. Why: "moves his water into reach of his good hand"
  pause  IONA turns her head from MONITOR to ELI, no step. Why: "Looks at her brother. Not at Jude." (the scene's turn)
  mid    SAYE's finger down the screen, then sideways. Why: shows the drop, then the way out through rock
  end    JUDE takes the remote from IONA's side. Why: the pivot ends it
Lines of action: watching beats: row to MONITOR (roughly north-south); shots near that axis only
  (master from the north, reverse from the south), which also serve as the bridge whenever the line changes.
  Argument beats: IONA-ELI along y = 1.8, across Jude; singles stay on the south (bed-head) side,
  so Iona looks frame-right and Eli frame-left. Return to the master only after Iona "looks back at the screen."
Cameras: M (2.5, 6.6, 1.3) looking at (2.5, 1.8, 1.1), 50 mm: master through the glass; the monitor's east edge
    is a dark foreground edge at frame-right; Saye is out of this frame (the family as she studies them)
  R (2.5, -0.8, 1.3) looking at (2.5, 4.5, 1.3), 35 mm, south wall wild: the reverse, three heads, both screens, Saye
  S1 (3.4, -0.5, 1.2) looking at (1.5, 2.1, 1.15), 85 mm, south wall wild: Iona at about 0.42 of the frame width,
    Jude's head and shoulder soft at about 0.9, low in frame (a dirty single, Jude in her lead room)
  S2 (1.6, -0.5, 1.2) looking at (3.5, 2.1, 1.15), 85 mm: the mirror of S1 for Eli (Eli about 0.58, Jude about 0.1)
Distances: IONA-ELI 1.8 m across Jude (social, with a body between); row to glass 2.2 m; row to Saye about 3 m (social)
(All four cameras were built and rendered from this plan with the Section 6.4 script on 2026-09-27: in M the row reads
 Eli, Jude, Iona from frame-left with Saye out of frame; in S1 and S2 the nearer body does not cover the far face.)
```

### 8.7 The ship's human rooms (sc20, sc23): Iona in Saye's place

"A long dim chamber. Down one side, three glass rooms, each with a hospital bed in it. Two of the beds she knows."

**Space.** The three glass rooms seen square on are limited space: frontal planes stacked in depth, the chamber a dark band in front of them. The chamber's length is the only deep axis, and the figure uses it: "At the end of the chamber, something black comes into the light." The rack "with six sockets" against the far wall is the anchor.

**Rhymes.** Iona's walk along the three rooms repeats the sc3 corridor ("A window into every room. / Empty bed. Empty bed. Empty bed."), same direction (frame-left to frame-right), same height, same lens. And Iona now stands where Saye stood: outside the glass, delivering through a drawer, with the people she loves inside. Reuse the sc13 master's relation to the glass (square on, 50 mm, from the observer's side, a few metres back), but this time with the observer in the frame: Iona in the right-hand foreground where the monitor's edge stood in sc13 (camera O below). The audience will feel that she has taken on Saye's job before anyone says it. Iona is in her helmet throughout: her face is a visor shot (Section 8.1), so light it from inside the helmet for every beat where the audience must read her.

```
FLOOR PLAN: sc20 and sc23, INT. SHIP - HUMAN ROOMS
Units: metres. Origin: south-west corner of the chamber floor. +x = east (along the chamber, toward the
  collection room), +y = north (toward the glass rooms).
Chamber: 14.0 x 4.0 (y 0 to 4), ceiling 3.2, so the figure ("Taller than the door", about 2.6 m) stands upright.
Glass rooms on the north side, glass fronts along y = 4.0, each 3.0 wide x 3.0 deep:
  JUDE x 2-5, ELI x 5-8, NELL x 8-11. Solid walls between rooms; a door in the ELI-NELL wall at (8.0, 5.5).
  [Inference: the script gives no order. Eli must be next to Nell ("the door between her room and Eli's"),
   and "In the third glass room, NELL ROWAN" puts her last.]
Fixed objects: BEDS at (3.5, 5.8), (6.5, 5.8), (9.5, 5.8); a DRAWER through each glass front at x 3.5 / 6.5 / 9.5,
  0.9 m high; RACK of six sockets on the south wall, centre (6.5, 0.2): the anchor, "across the chamber";
  BENCH with the metal tool (10.4, 2.9), free-standing, within reach of Iona's mark at Nell's room; NELL's shelf inside her room (10.6, 5.0): bowl, drawings, old harness
Anchor: RACK (south wall) in every shot looking south; the three lit glass fronts in every shot looking north
Exits: WEST HATCH (0, 2.0) from the service cavity (Iona's entrance); EAST DOORWAY (14.0, 2.0) to the
  collection room ("Next door. On your right."), which is also where the figure comes from and goes back to
Start marks sc20: IONA enters at (0.5, 2.0); ELI rises from his bed to (6.5, 4.8); JUDE in bed;
  NELL seated on her bed with the book
Moves sc20:
  IONA (0.5, 2.0) to (6.5, 3.5) along the glass, frame-left to frame-right as in sc3. Why: to her brother
  IONA at each drawer (x 3.5, 6.5, 9.5; y 3.5, an arm's length from the glass): the radios. Why: first contact,
    through the barrier
  IONA steps back from Eli's drawer to (7.0, 3.0) while "He takes it out on his side". Why: she watches, as
    Saye watched (a staging addition: the script does not write this step; log it)
  IONA to (9.5, 3.3), facing NELL. Why: the stranger; the bowl, the thin wrists
  FIGURE enters at (14.0, 2.0), stops at (12.0, 2.0) on "Wait."; IONA reaches to the BENCH beside her for the tool.
    It sets the tank at (10.8, 2.6), halfway between them, and goes back east. Why: a gift placed in the gap
  IONA to the tank: her first move toward it; she "lets go of the tool"
Moves sc23:
  IONA from Eli's drawer (6.5, 3.5) to (11.3, 2.0), facing the FIGURE at (12.5, 2.0): 1.2 m, the edge of personal
    distance.
    Why: "The closest she has been."
  FIGURE: fast, one clip per move (Rule 21): Jude's shell, the rack, back; later Nell's bed
  ELI through the released door to (9.8, 5.4), onto the east edge of Nell's bed. Why: two rooms become one
  IONA to (11.0, 2.8), facing the EAST DOORWAY. Why: "She is looking at the door to the collection room."
Lines of action: sc20 IONA-ELI across the glass: camera on the chamber side. sc23 IONA-FIGURE along y = 2.0:
  camera on the south (rack) side, so Iona is frame-left and the figure frame-right, with the glass rooms and
  the watching family behind her.
Cameras: O (6.2, 0.6, 1.5) looking at (6.4, 5.8, 1.3), 50 mm: nearly square on to Eli's room; with Iona on her
    stepped-back mark (7.0, 3.0), Eli at about 0.55 of the frame width and Iona at about 0.9, cut by the right
    edge, back three-quarter to camera (the observer in the frame). On her drawer mark (6.5, 3.5) she would
    stand at about 0.59 and hide him: that is why the step back exists.
  F (14.3, -2.0, 1.6) looking at (11.9, 2.6, 1.9), 35 mm, south wall wild east of x = 12, camera at Iona's eye
    height and tilted up about 3 degrees: sc23, "The closest she has been": Iona at about 0.34 facing
    frame-right, the figure at about 0.56 with its whole head inside the frame (B1: on the ship the figure is
    seen from her eye height, looking up only as far as its height forces, head in frame; the cut-off head is
    reserved for Iona's room); Nell small behind the glass between them (about 0.43; Eli joins her there,
    about 0.44, once he has moved); the collection-room doorway at about 0.92, the place she will go
Distances: IONA-ELI at the drawer about 1.3 m, glass between; IONA-FIGURE 1.2 m at its closest
(Cameras O and F were rebuilt with the Section 6.4 script after a second fact-check on 2026-09-27; the first
 versions put Iona in front of Eli in O and cut the figure's head in F, against B1.)
Note: Eli's "Next door. On your right." (sc21) fits this plan if Iona is facing his glass (north) when he says
  it: her right is then east, toward the doorway.
```

**Blocking change at sc23's turning point.** The figure "releases the door between her room and Eli's," and Eli "steps into Nell's room. She makes space for him on the bed." Two glass rooms become one while the glass between Eli and Iona stays shut (Example 3).

### 8.8 The last two-hander across glass (sc29), and the room's two phases

"A chair on each side of the glass." sc29 is the film's resolution and its quietest two-hander: Iona inside the plastic tent, Eli beyond the glass with Jude behind him, a meal in front of each. The staging job is to let the gap between the chairs carry the scene: it opens at social distance and closes only at the very end, from both sides (Section 7.1, reconciliation). Everything else stays still.

```
FLOOR PLAN: sc29 INT. QUARANTINE - IONA'S ROOM - DAY (world plan; phase C shows it as it is)
Units: metres. Origin: south-west inside corner of Iona's room. +x = east (toward the glass), +y = north.
Rooms: IONA x 0-4, NEXT ROOM (Eli, Jude) x 4-8; both y 0-4, ceiling 2.7. Glass partition along x = 4.0,
  full height. Wild walls: north (for the two ALONG cameras) and south.
Fixed objects: IONA's BED (1.0, 2.0) along the west wall, the grey needle box on the wall above it (anchor);
  TENT of clear plastic x 0.3-4.0, y 0.6-3.6, its east face pressed flat against the glass (Section 8.1: one
  visible barrier, not two); METAL TABLE with the VESSEL, pump and container (1.9, 3.1), inside the tent;
  TRANSFER DRAWER through the glass at (4.0, 1.2), 0.9 m high, opening inside the tent;
  JUDE's BED (6.9, 2.0) in the next room; CHAIR_I (2.5, 2.0) and CHAIR_E (5.5, 2.0), each 1.5 m from the glass
Anchor: the glass edge; the needle box in every shot looking west
Exits: the next room's door (8.0, 0.8), used only by Eli's attempted exit; nobody uses Iona's
Start marks: IONA seated on CHAIR_I facing ELI; ELI seated on CHAIR_E facing IONA; JUDE lying on his bed
Moves:
  B1  IONA half-rises and holds the half-roll out toward the DRAWER, then sits back. Why: "Moves half towards
      the transfer drawer." / "Sees the label on his tray. Stops." (a half-move that stops: no step)
  B4  JUDE from his bed to (4.3, 2.8) at the glass, facing west. Why: "comes to the glass beside Eli"
      IONA rises and steps to (3.7, 2.8), facing east. Why: to lay her hand against his (a staging addition:
      the script does not say she stands; log it). She returns to CHAIR_I after "They stay like that."
  B5  ELI rises with his tray and turns toward the door. Why: "He begins to rise with his tray."
      ELI sits again. Why: "Can you stay a bit?" / "He sits down again."
  B6  IONA moves CHAIR_I to (3.6, 2.0); then ELI moves CHAIR_E to (4.4, 2.0). Why: "She brings her chair closer
      to the glass. He moves his to meet it." (she moves first; he answers)
Lines of action: IONA-ELI along y = 2.0; THROUGH shots stay on the south side. B4: IONA-JUDE along y = 2.8;
  the reserved shot sits north of the pair, in the plane of the glass.
Cameras: R (4.0, 9.1, 1.5) looking at (4.0, 2.8, 1.5), 85 mm, north wall wild: the reserved reflection
    two-shot, ALONG the glass. Iona at about 0.61 facing frame-left, Jude at about 0.39 facing frame-right,
    their hands meeting on the centre line; the same lens and distance as the kitchen's camera A, the layout
    reversed left to right (Section 8.2); Eli cut by the left edge.
  W (4.0, 9.1, 1.2) looking at (4.0, 2.0, 1.1), 35 mm: the same axis, wider and at seated height, for the
    payoff. Iona at about 0.71 and Eli at about 0.29 at the start, about 0.55 and 0.45 when the chairs have
    closed; Jude on his bed at about 0.07; the vessel at about 0.84, on her side.
  T1 (1.5, 1.7, 1.2) looking at (5.5, 2.1, 1.25), 50 mm: THROUGH the tent and the glass, a dirty single of Eli
    (about 0.53) past Iona's soft head (about 0.23), Jude's bed behind him (about 0.41).
  T2 (3.6, 1.0, 1.2) looking at (2.5, 2.1, 1.2), 50 mm, early beats only (her chair later moves near this
    spot): Iona's single (about 0.43), the vessel behind her (about 0.65).
Distances: chairs 3.0 m apart at the start (social), 0.8 m at the end (personal, glass between);
  at B4 the two palms meet on the glass.
(All four cameras were built and checked with the Section 6.4 script in the second fact-check,
 2026-09-27; the script cannot change a cylinder's height, so Iona standing at B4 was checked for
 position only.)
```

**Why this staging.** The chairs are the scene's only real move, so nothing else travels: the half-roll stops short of the drawer (framed like the sc20 radio insert, Section 8.4), Eli's exit is one rise undone, and Iona's rise to the glass for the rings is the one addition, needed because a seated hand cannot reach the pane from 1.5 m. The reserved two-shot uses the kitchen's lens and distance so the audience feels the rhyme; the payoff wide uses the same axis with a wider lens, so the reserved tight framing is not spent twice (Example 4). Keep the glass CLEAR in T1 and T2 (Iona's side dimmer than Eli's, Rule 29), and let the tent's creases be the only MARKED surface.

**The room's two phases.** Iona's room is also the room of sc14 and sc16, which play in phase B, when the world is shown mirrored. By the Section 5.4 rule, the phase-B plan is derived from this world plan by x → 8.0 − x: in sc14 and sc16 her bed stands against the east wall and the window to the next room is on her west. In phase C the glass is on her east again. Both are correct; flag them together in the shot list. Phase C mirrors Eli and Jude, not the room (B1 10.2): in T1, treat Eli's face by B1's method for a turned face in a world shot.

---

## 9. Worked examples

### Example 1. The kitchen: a reflection, a secret in the background, and a body in the way (*The Catch*, sc10)

> "They stand facing each other across the table like a woman and her reflection, each with the wrong hand in the air."
> "Across the room Eli twists the cap of a water bottle. It will not give. He stops. Twists it the other way. It comes off."
> "Iona moves between her and Eli."
> SAYE: "Look at Jude. I cannot finish that here."
> "She waits until Iona steps aside."

**Choices.** Floor plan in Section 6.3. Jude lies along the table; the women stand either side of him; Eli stands by the fridge at the far end, on the table's axis. Camera A looks straight down that axis (85 mm from about 6.3 m, 1.45 m high, west wall wild; the same long lens from well back that B1 sets for the sc29 rings shot and that A2's B4.a asks for, so the film's two reserved reflection two-shots share lens and angle, and the long lens draws Eli, deep in the background, closer and larger between the women. **Lens-family conflict:** B1's lens family holds 85 mm back until the confession scene (sc13). Log this shot as the one early 85 mm exception, justified by B1's own pairing of the two reflection two-shots; if the director keeps B1's rule strictly, use 50 mm from about 3.7 m instead, through the same wild wall: the women stay at 0.22 and 0.78 of the frame width, and Eli stays centred but reads about 15 per cent smaller relative to them): Iona frame-left facing right, Saye frame-right facing left, each raising the hand nearest the camera, with Jude, the lamp and Eli on the frame's centre line. Iona has set the lamp on the table before B4, so both hands are free and the low lamp lights both women alike (A2's continuity flag). The bottle-cap beat (B5) plays in the same frame, focus pulled from the women to Eli deep in the centre. This is a variant of A2's B5.a, which instead puts Saye in the foreground with Eli behind; choose one version per breakdown and record it. At B9 the coverage resets to camera F, a wide from the north-west corner holding Saye, Eli and the space between them, Jude in the foreground. At B10 Iona walks round the end of the table into that space and faces Saye; from camera A she now covers most of Eli (the tested render leaves a thin sliver of him at her side). At B11 she steps aside and Eli is visible again.

**Why.** The mirror's centre line runs through the evidence (Jude, whose heart Saye had to find on the other side) and through the man who already knows (Eli, who twists the cap "the other way" without thinking), so the body's confession happens behind the argument, where the script puts it: "Across the room." Interposition needs a frame that sees both people it separates (Rule 4), so it plays in the wide. The second turning point is pure blocking and revealing: Iona's body is the last barrier between Saye and Eli, and "She waits until Iona steps aside" is Saye winning by stillness (Rule 3). The configuration changes on both turning points (Section 4.9).

### Example 2. The row, the pivot, and the remote (*The Catch*, sc13)

> "Iona pauses the recording with the remote. Looks at her brother. Not at Jude."
> "Saye draws one finger straight down the screen. Then sideways, into the concrete of the wall."
> "He has been looking at the screen. Now he looks at her."
> "On the screen the upside-down cage falls empty. All three of them flinch at the same moment."
> "Jude takes the remote and switches it off."

**Choices.** Marks as in Section 8.6: Iona, Jude in the bed, Eli, in a row facing the glass and the monitor beyond it. The master is from Saye's side, THROUGH the glass, 50 mm, planimetric: the monitor's dark back as a foreground frame edge, three faces lit by the screen, glass CLEAR. The reverse is from behind the three, the footage seen THROUGH the glass as a SCREEN composite (C2). Saye's gesture is framed so her finger's path follows the shaft in the paused picture: a leading line drawn by a hand, down, then sideways into rock. When Iona turns to Eli, the line of action swings from the screen axis to the Iona–Eli axis, running over Jude; coverage moves to 85 mm singles (B1), each with a soft slice of Jude in the foreground, both from the bed-head side of that line (cameras S1 and S2 in the Section 8.6 plan). Eli's turn from the screen to her is a head turn inside a held single, not a cut. For the flinch, return to the master: one frame, three bodies. The insert of Jude's thumb on the remote repeats the framing of the insert of Iona's.

**Why.** The shared object turns the argument into a three-way conversation conducted through a thing (A2's "third thing"): the three begin as an audience, and the scene's turn is literally a turn away from the screen. Jude is the physical pivot because he is what the argument is about: the reason Eli's choice was right, and the man it nearly killed. The master is the first to sit on the side of the glass that studies the family, which is what Saye has just started doing: at the end of sc12 Iona demanded "I want the whole thing recorded." and "Saye reaches for a camera." Simultaneity cannot be cut together, so the flinch needs one frame. The remote passing from Iona to Jude hands control of the evidence to the pivot, who ends the scene.

### Example 3. The same question through the other glass (*The Catch*, sc23)

> "Eli looks through the wall at his sister. She has not reached for her way home. She is looking at the door to the collection room."
> ELI: "Io." / "Are we going to be all right?"
> IONA: "I don't know."
> "He starts to get up." / IONA: "Go." / "He stops." / "She nods. Once."

**Choices.** The script writes this sentence from Eli's side of the glass, so the camera crosses to it once (Rule 11): THROUGH the glass from just behind Eli's shoulder, Iona in the midground, and in the background, on her eyeline, the doorway to the collection room. Staging in depth shows her decision before she speaks: her body faces away from her way home and toward the room Saye has said she will burn. For "Are we going to be all right?" the camera returns to Iona's side, ANGLED to the pane, so her reflection lies across Eli's face (REFLECTING). Make that physically true (Rule 28): her white suit and helmet lamps lit, Nell's room kept dim, and the camera on the line through her mirror twin and Eli. Checked against the Section 8.7 plan: at her mark (11.0, 2.8) she is 1.2 m from the glass, so her twin stands at (11.0, 5.2); Eli is at (9.8, 5.4), about the same distance behind the glass but 1.2 m to the side, so the line through the two runs almost parallel to the pane and comes out on her side only far beyond the chamber's east wall: no camera in the chamber can put her reflection on his face from there. Two honest options: (a) on "Io." / "She looks at him." she turns and steps to the glass directly opposite him, to about (9.8, 2.6), so her twin coincides with Eli and the reflection lands on him from any angled camera on her side; the step toward him then makes "Go." a refusal of her own move; or (b) she stays on her mark and the line plays THROUGH, glass CLEAR. Choose (a) only if the director accepts an added move the script does not write, and log it as a staging addition. "He starts to get up" plays in the wide, a move toward the barrier; "Go." is Iona's static single, and she does not move at all; he stays half-risen through "He stops." The shell closing is framed THROUGH from Iona's side, the opened door between Nell's room and Eli's in the same frame as the closed glass in front of them.

**Why.** In sc9 Iona asked this question into a mirror and got "Drive." Now Eli asks it through glass (in option (a), with her reflection on his face): the mirror has become a barrier and the roles have reversed (A2 traces the question across four scenes). Her stillness against his half-rise is Rule 3: she holds power by not moving, and uses it to send him away. The open inner door and the closed outer glass in one frame state the cost: the barrier between the prisoners opens; the one between brother and sister does not.

### Example 4. When there is no glass, a hand becomes it (*The Catch*, sc28, with its payoff in sc29)

> "Iona starts towards him. The harness catches under her knee."
> "He takes a step towards her too."
> "Saye stops. Still holding Nell's hand, she puts her free hand between them."
> SAYE: "Wait. We need another room."
> "Beside Iona on the mat, Jude looks at his own hand, still holding her harness. He takes it away."
> "Iona and Eli stay where they are. Still looking at each other."

**Choices.** A wide, lateral frame from the side of the receiving room, 35 mm, at Iona's kneeling eye height, about 1 m (B1's default: "when she kneels, the camera kneels"), so the standing people rise out of the top half of the frame: Iona frame-left on her knees on the mat, Eli frame-right standing by the open transport shells, about 3 m apart (social distance). Saye and Nell cross the frame between them on their way to the door (Section 4.6: an exit that separates). Saye stops so that her raised hand lands on the frame's vertical centre line, the place the glass edge occupies in every quarantine two-shot. This is deliberately not the reserved reflection two-shot: the heights are unequal (kneeling, standing), the camera sits at her height rather than level between them, and a third person fills the centre. Before this, as Saye and Nell pass, their bodies hide Eli from the camera until they clear him ("Iona looks beyond her. / Eli has got to his feet."; Section 4.5). Insert: Jude's hand leaving the harness. Then hold the wide, both still. Iona's helmet stays on ("Leave it on."), and Saye, the technician and the nurse wear protective hoods, so Iona's face and every hooded face is behind a clear layer: keep all of them CLEAR (Section 8.1), so the only barrier the audience reads is Saye's hand.

**Payoff (sc29).** "A chair on each side of the glass." / "She brings her chair closer to the glass. He moves his to meet it." Use the reflection axis from 8.2 (ALONG the glass) but at a wider size that holds both rooms and Jude behind Eli, so the reserved tight framing is not repeated. The chairs start about 1.5 m from the glass on each side and end close to it. Both move. Iona is inside the clear plastic tent: build the tent against the partition (Section 8.1), so the chairs close on one barrier, not two. Floor plan and cameras (W is this shot): Section 8.8.

**Why.** The film has taught the audience that glass separates Iona from the people she loves; with no glass wall in the room, Saye's hand takes its exact place in the frame, and Jude's hand leaving the harness confirms the separation from the other side. The distance holds at social range because the story holds it there. In sc29 it closes as far as the barrier allows, from both sides (Section 7.1: reconciliation is the gap closed by both).

### Example 5. "The good distance" (*The Long Places*, Chapter II, the keeper's letter)

> "She had wedged herself where the wall gives its shoulder, the place the frightened find without being shown"
> "I set the lamp down where she could see it if she chose to see it"
> "Then I sat where the wall lets a body sit, at the good distance, which is farther than your wanting and nearer than hers"
> "Near morning she came closer by degrees, the way cold walks a body over. In the end she slept against my side"

**Choices.** Prose gives distances as feelings; the floor plan turns them into marks. The girl's start mark is a corner (the wall's "shoulder"). The keeper sets the lamp down about 1.2 m from the girl, and sits at the mark named **GOOD_DISTANCE**, set at 2.4 m from the girl: inside Hall's social zone, beyond personal. Camera: one position for the whole night, low (seated eye height, about 0.8 m), static, lamp in the midground, the keeper frame-right, the girl frame-left. The night is five shots from that one position joined by dissolves, and the only thing that changes between them is the girl's mark. Follow the letter's own timing: through the storm and "toward the small hours" she stays in her corner at 2.4 m, flinching (two shots); only "Near morning she came closer by degrees", so the last three shots carry the approach: 1.2 m, 0.6 m, then asleep against his side. The keeper never moves. Do not invent a clock (a burning-down flame, a candle, a watch): the letter supplies its own, the sound of the storm through the night and then "the grey came in at the top of the doorway and lay down along the floor", so the last shot, and only the last, has grey daylight lying across the floor from the top of the doorway.

**Why.** The phrase "farther than your wanting and nearer than hers" is a proxemic instruction: the frightened person's limit sets the distance, not the carer's wish. So the approach belongs to the girl alone, and the keeper's stillness is the kindness ("I did not touch her beyond being warm and being there"). Holding camera, the keeper and (until the last shot) the light in affinity lets the one changing component, distance, carry the scene (Principle 5); the grey at the doorway arrives only after the distance has closed, so it ends the night instead of counting it. The named mark then becomes a motif: the novella returns to it when an elder "came to the middle distance and stopped at the good distance" and Yusuf sets his headlamp "on the mat between them," and near the end ("laid it on the mat at the good distance — farther than your wanting, nearer than hers"). Reuse the same 2.4 m, the same low camera, and an object set down between the two bodies each time (Rule 19).

---

## 10. Checklists

### 10.1 Per shot: composition (a "no" needs a fix or a written reason)

1. Is the **dominant** named, and do at least three attention cues (face, tone, focus, isolation, lines, other characters' looks) agree on it?
2. Is the placement (thirds, centre, edge) chosen, with a story reason if it is not thirds?
3. Does the **balance** match the beat? Perfect mirror symmetry only in a reserved slot (centring one person is allowed where a character's camera system calls for it; B1 centres Saye behind glass); imbalanced only when a character waits for or dreads someone out of frame, with the empty side toward where that person would come from; otherwise asymmetrical, weighed by the visual-weight order in Section 3.4.
4. Is **headroom** normal (eyes on or just above the upper third line) unless there is a reason? Is there **lead room** toward the look or move (about two-thirds of the width in front of the face)? Is any **short-siding** planned rather than accidental? Is the **eyeline** on the correct side of the lens and at a height that matches the bodies?
5. Does every foreground object frame, block, or comment on the subject?
6. Does the **space type** match the visual structure plan for this scene (Section 2.7)?
7. Do the dominant lines follow the plan (diagonals kept for the peaks)?
8. If there is a **frame within a frame**, is its meaning (observation, containment, exclusion) stated?
9. (*The Catch*) Are the **glass state** and **camera-to-glass position** given, for every transparent surface in frame, including Iona's visor and the tent? If REFLECTING or CLEAR, is it physically possible (Rules 28 and 29: who is lit, which side is dark, where the camera stands)?
10. Is the **mirror state** checked, with hands described as "nearest the camera" and any text planned as an insert graphic (C2)?
11. Is **screen direction** consistent with the previous shot and the line of action, as the final picture will show it after any flip?
12. Is the **eye-trace** smooth from the previous shot, or is the jump intended?
13. Is an **anchor** visible, or is the geography otherwise clear?
14. Is any **reserved** composition used only in its reserved slot (for example: the perfectly symmetrical profile two-shot only in sc10 and sc29; the figure's head cut by the frame top only in Iona's room, sc16, per B1; deep space straight down the shaft only in sc6 and its security footage)?
15. With the sound off, does the frame still tell the beat?
16. Does the shot's written reason name an object, line or action from this script, not only a mood (Rule 23)? Does it pass the any-film test (Rule 26)? Is every symbolic object in frame one the source contains (Rule 24)?
17. Is at most one expressive device working in the frame (Rule 25)?
18. (*The Catch*) If a **helmet visor** is in frame, is it CLEAR with her face lit from inside, and is any visor reflection the film's single allowed one (Section 8.1)?

### 10.2 Per scene: staging

1. Is there a **floor plan** with fixed objects, an anchor, exits, and start marks with facing targets?
2. Does every **move** have a beat id and a reason ("why")?
3. Does the configuration change **on** each turning point, not before or after?
4. Are the **distances** at key beats written in metres with their Hall zone, and do they change only when a value changes?
5. Do stillness and movement match who holds the power?
6. Is the **line of action** written for each movement of the scene, with the camera's side chosen and any crossing motivated?
7. Is there a master shot or anchor before the first important move?
8. Is each entrance and exit chosen (edge or door)? Is anyone who appears without entering meant to be uncanny?
9. With three or more people, is the **pivot** named?
10. Are the **barriers** listed, with when each is visible and which side the camera is on?
11. Does the scene **rhyme** with an earlier configuration? If so, what one thing changes?
12. Does the staging make clear whose scene it is? Name the point-of-view character; is that person the dominant in the master and in the turning-point shot, or is there a written reason they are not?
13. For AI generation, does each clip hold at most one major move?
14. For prose, does every mark come from a quoted phrase or a stated reason, and does none contradict the text? For a screenplay, is every move the script does not write logged as a staging addition?
15. Could one staged wide replace several singles?
16. Do exits and entrances keep direction across cuts (exit frame-right, enter frame-left), and is there a re-establishing shot after people change marks?
17. In a three-hander, is the engaged pair named for each beat, and is the silent third kept visible when their reaction matters?
18. With four or more, are the subgroups listed, the dominant subgroup named per beat, one master side chosen, and every move between subgroups shown whole (Section 4.5)?
19. (*The Catch*) If the location appears in another mirror phase, is this plan derived from the location's world plan by the Section 5.4 rule, and is the swap of sides flagged in the shot list?
20. Does every staging addition (a move the script does not write) have a one-line reason, and is it logged as an addition?

---

## 11. Common mistakes and how to spot them

| Mistake | How to spot it | Fix |
|---|---|---|
| **No system**: placements chosen shot by shot | List every shot's placement; no pattern ties them to the story | Write the visual structure plan and reserved choices first |
| **Composition contradicts power** | The dominant belongs to the character losing the beat, with no reason given | Re-rank: tone, size, centrality to the winner, or state the irony |
| **Stand-and-deliver**: static singles in a scene with a turning point | Zero moves in the scene; more than half the shots are singles | Stage the turn as a move; play it in a wide |
| **Unmotivated moves** ("crosses to the window") | A move with no "why", or "for variety" | Tie each move to a desire or cut it |
| **Turn on the wrong beat** | The configuration changes on a beat other than the turning point | Move the change onto the turning point |
| **Lost geography** | No master or anchor; two consecutive singles with both people looking the same way | Add a master and an anchor; put the camera back on one side of the line |
| **Eye-trace jumps** in fast cutting | The dominant leaps across the frame between short shots | Match the dominant's position across the cut |
| **Decorative depth** | Foreground objects that neither frame, block, nor comment | Remove them or make them story objects |
| **Cliché**: the stock image announced by several channels at once | A hand on glass with a slow push-in and swelling music; rain-streaked windows for sadness; a character staring into a mirror to "reflect"; shadows of bars or blinds for "trapped"; a door edge splitting lovers; a tilted camera for madness. Test: could this frame be dropped into any film? | Keep the image only if the story earns it; state it through one channel (usually staging), and let light, lens and score stay neutral |
| **Heavy-handedness**: the barrier shown in every shot | Glass state MARKED in every shot of a scene | Keep glass CLEAR most of the time so MARKED means something |
| **Symmetry as style** | Centred, symmetrical frames outside the reserved slots | Return to thirds; reserve symmetry for ritual and mirrors |
| **Accidental short-siding or headroom** | Singles in a dialogue that do not mirror each other's lead room | Match singles unless one character is meant to be cut off |
| **Shallow focus everywhere** | The background is always blurred, so staging in depth and geography are lost | Deepen focus where the background carries story (Example 1) |
| **Mirror errors** | Hands written as "left/right"; a flipped frame that also flips a turned character; text readable in the wrong phase | Use "nearest the camera"; follow B1's phases and C2's flip recipes |
| **Prose staging invented or vague** | Marks that contradict the text, or "they stand apart" with no number | Cite a phrase for each mark and convert it to metres |
| **Impossible glass** | A reflection planned over a face with no one lit at the mirror position; a CLEAR pane with a bright room behind the camera; reflections "only at an angle" | Apply Rules 28 and 29: find the mirror twin, light the reflected side, darken the other |
| **Invented symbol** | An object or weather in the shot list that appears nowhere in the source (rain, a clock, a bird, blinds), or an invented device for time passing (a candle or lamp burning down, a clock face) | Delete it; carry the meaning with the source's own recurring objects and its own time markers (Rule 24; Example 5) |
| **Forgotten visor** | Ship close-ups of Iona written as if her face were bare | Add the visor's glass state; light her face from inside the helmet |
| **Monster in the visor** | The figure, the ship or the stars reflected across Iona's helmet visor | Remove it; the script gives the figure's reflection to the container in sc21 (Section 8.1) |
| **Phase flip "fixed"** | A shot list that keeps the treatment-floor corridor, Eli's first room, the passage and receiving room, or Iona's quarantine room the same way round in every phase they appear in | Derive each phase's plan from the world plan (Section 5.4); flag the swap so nobody corrects it |
| **Plan never rendered** | Camera positions written by hand with frame positions claimed ("Iona at the right edge") but never projected; people who should be side by side end up hiding each other | Run the plan through the Section 6.4 script and read the projected positions before writing any frame position into a shot line |

---

## 12. How to say this to an AI image or video model

The claims below are this file's judgment from how current image and video models behave, as of 2026-09-27; they are not tested benchmarks. File C1 covers specific video models and C2 specific image tools.

**Usually understood:** shot sizes ("wide shot", "close-up", "over-the-shoulder shot", "two-shot"); "centered composition" and "symmetrical composition" for one subject; "seen through a window" or "framed by a doorway"; one foreground and one background element ("in the foreground ... in the background"); "in profile"; "silhouette"; "reflection in the glass" (a reflection appears, but often not a physically correct one).

**Often ignored or misread:** "rule of thirds" (sometimes followed, often generic); film jargon such as "lead room", "nose room", "headroom", "short-sided", "planimetric", "limited space", "contrast and affinity", "180-degree rule", "screen direction"; "frame-left" (may be read as the character's left); exact distances in metres; which hand is raised; two people "looking at each other" (they often look at the camera or past each other); more than three people in specified positions; the same room geography across separately generated clips.

**Plainer phrasings that work better:**

| Instead of | Say |
|---|---|
| "Short-sided close-up" | "Close-up of a woman near the right edge of the image, in profile facing right, her face close to the edge; a large empty area of bare wall fills the left two-thirds of the image behind her." |
| "Lead room" | "She is on the left side of the image, facing right, with open space in front of her face." |
| "Reflection two-shot" (sc10) | "Wide 2.39:1 frame, long lens from far away, depth flattened. Two women in exact profile face each other across a kitchen table, one on the left side of the image facing right, one on the right side facing left, the same distance from the centre. Each raises the hand nearest the camera, palm out, at the same height. A man lies on the table between them. Far in the background, exactly in the centre, a thin bearded man stands by a fridge. Symmetrical composition." |
| "Interposition" | "She stands directly between the doctor on the left of the image and the man on the right, facing the doctor, blocking the doctor's view of him." |
| "Staging in depth" | "In the foreground, the doctor's shoulder; in the middle distance, the woman; in the far background, small and sharp, the man at the fridge." |
| "Social distance" | "About two body-lengths apart" or "the table between them". |
| "Glass state REFLECTING, ANGLED" | "Seen at an angle through a glass wall. She stands brightly lit on this side; the room behind the glass is dim. Her faint reflection lies over his face on the glass." (A model will not work out the physics; state the lighting that makes the reflection possible.) |
| "Glass state CLEAR" | "Seen through perfectly clear glass with no reflections; the room on the camera's side is dark." |
| Visor close-up (ship scenes) | "Close-up of a woman in a white pressure-suit helmet; her face clearly visible through the clear visor, lit softly from inside the helmet; no reflections over her eyes." |
| "Cheated three-quarter" | "Her face turned three-quarters toward the camera while her eyes look off to the right of the image, at the man she is talking to." |

The sc10 prompt only sets the composition. Saye's mirror state and the rings on the lowered hands are handled by C2's flip-and-composite route, and every hand is checked by eye afterwards.

**Working methods that hold up better than words:**

1. Build the blocking in Blender (Section 6.4), render the camera, and use the render as a structure image for an image model (depth or layout control, C2; pose control needs posed figures, C4) or as a start frame or reference for a video model; some video models accept grey 3D "clay" renders for camera and blocking (C1).
2. One major move per clip ("She walks from the left edge to the window and stops"). Split a scene's blocking into clips at the moves.
3. For two-person frames, generate or composite each person separately when positions, facing or hands must be exact (C2's composite route).
4. Write screen positions as parts of the image (left third, right edge, exact centre, lower half), never as film jargon.
5. Check every output against the per-shot checklist, especially hands, facing and mirror state.

---

## 13. Limits and open points

- Block's system is paraphrased here from the 2nd edition's structure and from summaries checked on 2026-09-27; quote Block only after checking the page. His definitions of limited and ambiguous space are given in the form those summaries confirm.
- Arijon's names for the triangle variations should be checked against the book before being printed in any user-facing document.
- Hall's distance zones were measured for North American adults; *The Long Places* is set in a Cappadocian village, where comfortable distances may differ. The story's own "good distance" should override the table.
- The *Paris, Texas* reference gives only the verified light switch (Jane turns off her light and sees Travis); watch the scene before relying on specific shots.
- The mirror geometry in Section 8.2 depends on B1's phase system (who is shown mirrored when). If B1's phases change, redo 8.2.
- The Blender script was tested on the sc10 plan, and the camera positions of the sc13, sc20/23 and sc29 plans (Sections 8.6 to 8.8) were built and checked with it on 2026-09-27. The second fact-check found that two cameras written earlier (sc20 camera O, sc23 camera F) did not produce the frames claimed for them, and rebuilt them; any new camera written by hand should be projected the same way before its frame positions are trusted. The script does not animate cameras, change a figure's height (sitting to standing) or pose bodies; C4's script does.
- Block's own treatment of visual counterpoint (visual intensity deliberately falling while story intensity rises) is only indirectly confirmed: a review quoted on the 3rd edition's publisher page credits the book with tools for "harmony and counterpoint" between story and visual structure, but the summaries checked do not show his examples. The file treats each counterpoint scene as a pipeline choice to justify. Check the chapter "Story & Visual Structures" before quoting Block on it.
- The kitchen reflection two-shot on 85 mm (Example 1) breaks B1's lens family (85 mm only from sc13 on). Resolve with B1's owner: either add it to B1's reserved list as the one early 85 mm shot, or shoot it on 50 mm as Example 1 describes.
- Staging additions this file proposes and that must be logged, because the script does not write them: Iona setting the lamp down in sc10; Iona's step back from Eli's drawer in sc20; option (a) of Example 3 in sc23; Iona rising to the glass for the rings in sc29.
- Three staging facts in *The Catch* are inferences, flagged where used: Eli in the car's front seat (sc9), Jude in a bed in sc13, and the order of the ship's three glass rooms (Jude, Eli, Nell). The car's side geometry (8.5) assumes a left-driving home country with right-hand-drive cars; confirm with the writer.
- The glass figures (about 4 per cent reflection per surface square on; polarizer best near 56 degrees) are standard optics for ordinary clear glass. Coated glass, visors with anti-reflective coatings, and plastic behave differently; test a real or rendered frame before relying on a reflection.

---

## Sources

**Books and articles**

- Bruce Block, *The Visual Story: Creating the Visual Structure of Film, TV and Digital Media*, 2nd ed., Focal Press, 2008 (3rd ed., Routledge/Focal Press, dated 2021 on the publisher's page, https://www.routledge.com/The-Visual-Story-Creating-the-Visual-Structure-of-Film-TV-and-Digital-Media/Block/p/book/9781138014152 , checked 2026-09-27, with its table of contents and the review line on "harmony and counterpoint").
- Gustavo Mercado, *The Filmmaker's Eye: Learning (and Breaking) the Rules of Cinematic Composition*, Focal Press, 2010 (dated 2011 in Open Library); 2nd ed., Focal Press/Routledge, 2022 (publisher's page, https://www.routledge.com/The-Filmmakers-Eye-Learning-and-Breaking-the-Rules-of-Cinematic-Composition/Mercado/p/book/9781138780316 , checked 2026-09-27, with its table of contents). Organised shot type by shot type, each with its conventional use and a film example of the rule broken for a story reason. His points on the image system, looking room and headroom were checked against quoted passages in search results on 2026-09-27, not against the printed page. Separate book: *The Filmmaker's Eye: The Language of the Lens*, Routledge, 2019.
- Jennifer Van Sijll, *Cinematic Storytelling: The 100 Most Powerful Film Conventions Every Filmmaker Must Know*, Michael Wiese Productions, 2005. A catalogue of conventions, each named with its story job and shown through film examples. Chapter list, the X/Y/Z-axis treatment of screen direction and the *Strangers on a Train* example confirmed from two independent summaries (The Story Department, https://www.thestorydepartment.com/screenwriting-cinematic-storytelling-1/ ; Mystery Man on Film, http://mysterymanonfilm.blogspot.com/2007/06/cinematic-storytelling.html ; both checked 2026-09-27).
- Daniel Arijon, *Grammar of the Film Language*, Focal Press / Hastings House, 1976; Silman-James reprint, 1991.
- David Bordwell, *Figures Traced in Light: On Cinematic Staging*, University of California Press, 2005.
- David Bordwell, "Intensified Continuity: Visual Style in Contemporary American Film", *Film Quarterly* 55, no. 3 (2002).
- David Bordwell, Kristin Thompson and Jeff Smith, *Film Art: An Introduction*, McGraw-Hill (many editions).
- David Bordwell, *Ozu and the Poetics of Cinema*, Princeton University Press, 1988.
- Steven D. Katz, *Film Directing Shot by Shot: Visualizing from Concept to Screen*, Michael Wiese Productions, 1991.
- Walter Murch, *In the Blink of an Eye*, 2nd ed., Silman-James, 2001.
- Sidney Lumet, *Making Movies*, Knopf, 1995.
- Edward T. Hall, *The Hidden Dimension*, Doubleday, 1966.
- Heinrich Wölfflin, *Principles of Art History*, 1915.
- Leo Braudy, *The World in a Frame: What We See in Films*, 1976.
- Herbert Zettl, *Sight, Sound, Motion: Applied Media Aesthetics*, Wadsworth (several editions), for headroom, lead room and vectors.
- André Bazin, "William Wyler, or the Jansenist of Mise en Scène" (1948), on depth staging.
- John Thomas Smith, *Remarks on Rural Scenery*, 1797 (first written use of "rule of thirds").
- Eugene Hecht, *Optics*, 5th ed., Pearson, 2017 (Fresnel reflection from glass; Brewster's angle, about 56 degrees for glass of refractive index 1.5). The reflectance figures in Section 8.1 were computed from Fresnel's equations for unpolarized light and n = 1.5.

**Web pages (all checked 2026-09-27)**

- David Bordwell, "Shot-consciousness", https://www.davidbordwell.net/blog/2007/01/16/shot-consciousness/ (definition of the planimetric shot; filmmakers who use it).
- David Bordwell, "Early Hou Hsiao-hsien: Film culture finally comes through (a repost)", https://www.davidbordwell.net/blog/2024/02/26/early-hou-hsiao-hsien-film-culture-finally-comes-through-a-repost/ (first posted 6 June 2016; Hou Hsiao-hsien: clothesline and stacking schemas, blocking and revealing, "a long lens (usually 75mm–150mm)"; re-checked 2026-09-27).
- Bordwell, "Shot-consciousness" (above) also credits the term "planimetric" to Heinrich Wölfflin.
- Wikipedia, "Rule of thirds", https://en.wikipedia.org/wiki/Rule_of_thirds (Smith 1797; George Field's 1845 objection).
- Vashi Nedomansky, "The Editing of Mad Max: Fury Road", https://vashivisuals.com/the-editing-of-mad-max-fury-road/ (crosshair framing and eye-trace).
- kogonada, "Kubrick // One-Point Perspective" (video essay, 2012), https://vimeo.com/48425421 ; also listed at https://kogonada.com/portfolio/kubrick-one-point-perspective (checked 2026-09-27).
- Wikipedia, "Paris, Texas (film)", https://en.wikipedia.org/wiki/Paris,_Texas_(film) (the one-way mirror booth; "Jane turns the light off on her side and finally sees Travis"; Kinski saw only a mirror; checked 2026-09-27).
- Summaries of Block's *The Visual Story* used to confirm terms: http://filmbooknotes.blogspot.com/2013/05/the-visual-story-by-bruce-block.html ; https://arthurtasquin.com/blog/visualjourney1 ; https://mediadobson.blogspot.com/2011/12/bruce-block-visual-story-chapters-1-2.html ; https://kafkasfilm.blogspot.com/2013/07/the-visual-story-by-bruce-block.html (confirms the term "Story Structure Graph", the "Story Sequence List" and the *North by Northwest* example). The filmbooknotes summary confirms "visual progression", the line-intensity order (diagonal, vertical, horizontal), circle and triangle as the greatest shape contrast, the continuum of movement, and the causes of ambiguous space including "lack of movement" (all re-checked 2026-09-27).
- Open Library search API, https://openlibrary.org/search.json (edition data for Block, Mercado, Van Sijll, Arijon, Bordwell, Katz, Zettl).

**Video essays named but not re-checked**

- Tony Zhou and Taylor Ramos, Every Frame a Painting, "The Spielberg Oner" (2014).

**Films cited** (title, year, director; cinematographer where named in the text): *Citizen Kane* (1941, Orson Welles; Gregg Toland); *The Best Years of Our Lives* (1946, William Wyler; Gregg Toland); *Tokyo Story* (1953, Yasujiro Ozu); *Rear Window* (1954, Alfred Hitchcock; Robert Burks); *The Searchers* (1956, John Ford; Winton C. Hoch); *12 Angry Men* (1957, Sidney Lumet; Boris Kaufman); *Paths of Glory* (1957), *2001: A Space Odyssey* (1968) and *The Shining* (1980), Stanley Kubrick; *The Godfather* (1972, Francis Ford Coppola; Gordon Willis); *Paris, Texas* (1984, Wim Wenders; Robby Müller); *In the Mood for Love* (2000, Wong Kar-wai; Christopher Doyle, Mark Lee Ping-bing); *Moonrise Kingdom* (2012) and *The Grand Budapest Hotel* (2014), Wes Anderson; Robert Yeoman; *Mad Max: Fury Road* (2015, George Miller; John Seale; editor Margaret Sixel); *Cute Girl* (1980), *Green, Green Grass of Home* (1982) and *The Boys from Fengkuei* (1983), Hou Hsiao-hsien; *North by Northwest* (1959, Alfred Hitchcock; Robert Burks), as Block's example of a short resolution; *Strangers on a Train* (1951, Alfred Hitchcock; Robert Burks), as Van Sijll's X-axis example; *Mr. Robot* (2015–2019, Sam Esmail; Tod Campbell); *The West Wing* (1999–2006, Thomas Schlamme).

**Test stories**

- *The Catch*, workshop revision, 25 September 2026 (`1edae70d-35_The_Catch_-_workshop_revision_of_Final4.txt`).
- *The Long Places*, revised final (`5dcd8176-19_The_Long_Places_-_revised_by_Claude_final.md`), Chapter II and the passages at "the good distance".
