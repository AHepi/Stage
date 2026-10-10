# B4. Turning Meaning into Things: Visual Metaphor, Motif Systems, Props, Sets and Costume

> **What this file is for**
> 1. It gives the pipeline a method for turning abstract meaning (theme, inner state, relationship) into concrete things a camera can film: objects, places, clothes, marks on bodies and repeated sounds.
> 2. It supplies the theory stated carefully, a translation table, "If ... then ... because ..." rules, a checklist, and a list of common mistakes, including cliché and heavy-handedness.
> 3. It shows how to build a motif register (every recurring thing, what it means, where it is planted, developed and paid off, and how it is framed each time), with a full register for *The Catch* and a short one for *The Long Places*.
> 4. It shows how to track the state of every prop, costume and wound from scene to scene, so storyboards, Blender previs and AI video stay consistent.
> 5. Run it after the scene breakdown (A2) exists and before shots are designed (B1) and lit (B2); its outputs feed the asset sheets in C2.

---

## 0. How to use this file

### 0.1 Order of work for an LLM running the pipeline

1. **Theme and core opposition.** Write the story's theme as a question, then name its core opposition as two nouns (Section 3.1, steps 1 and 2).
2. **Harvest.** List every concrete thing the text names more than once, or names at a turning point: objects, places, clothes, wounds, sounds, words on things (step 3).
3. **Test and rank.** Run the six tests in Section 3.3 on each thing, apply its overrides and tie-breaks, and sort it into spine motif, supporting motif, single-scene prop or plot machinery, counting spine motifs per channel (Section 3.2).
4. **Register.** Write one register entry per motif (format in Section 9.2): meaning, plant, develop, reveal if a hinge, payoff, state changes, framing, rules. Then write the shape and material family for each pole and the emphasis-3 map (both as in Section 9.1).
5. **Passes.** Run the set pass (Section 4), prop pass (Section 5) and costume pass (Section 6) for each location and character.
6. **State table.** Write the per-scene state table (Section 9.4) and hand it to C2 for asset sheets.
7. **Per shot.** In every shot spec, fill a THINGS field: which register items are in frame, in what state, at what emphasis level (Section 3.4).
8. **Check.** Run the checklist (Section 12) and the mistakes list (Section 13).
9. **Prompt.** Translate into model-friendly wording (Section 14).

### 0.2 For the non-technical user

You do not need to learn any of this. Ask the LLM: "Run the B4 motif pass on my script and show me the register." Then read only the **Meaning** line of each entry and ask yourself whether it is true to your story. Correct any meaning you disagree with in plain words ("the mint is about Saye's loneliness, not about the test"); the LLM should then re-derive the framing. If the result feels heavy or obvious, ask it to "run Section 13 and rule 25 on its own register". If it feels generic, ask: "Which of these motifs would fit any film with this theme?"

### 0.3 Words this file uses (one word per concept)

| Term | Plain definition |
|---|---|
| **Mise-en-scène** | French for "putting into the scene": everything placed and staged in front of the camera (set, props, costume, makeup, performers' positions and movement). |
| **Production design** | The department and job that designs the whole look of the film's world: sets, set dressing, props and their colors and materials. The head is the **production designer**. |
| **Set** | Any place where a scene is filmed, whether built in a studio or found and dressed on location. |
| **Set dressing** | The objects that furnish a set but are not handled in the action (furniture, pictures, clutter, signs). |
| **Prop** | Short for "property": a movable object an actor handles or the action uses. |
| **Hero prop** | The most detailed version of a prop, made for close shots; productions often also make simpler duplicates for stunts and backups. |
| **Costume** | Everything a character wears, including accessories, as designed for the story. |
| **Makeup** | Everything done to the face and body surface: age, dirt, wounds, scars, beards, and their progression. |
| **Motif** | A concrete thing (object, place, color, shape, gesture, sound) that returns during a story and gathers meaning each time it returns. |
| **Motif system** | The whole planned set of motifs for one film. Robert McKee calls this an "Image System"; this file says motif system. |
| **Leitmotif** | In music, a short recurring phrase tied to a particular person, place or idea. This file narrows it to a motif (often a sound) tied to one character or being, returning whenever they are present or implied. The word comes from nineteenth-century writing about opera (first about Weber, then, famously, about Wagner). |
| **Emblem** | An object that stands for a particular character or relationship (a character's signature object). |
| **Objective correlative** | T. S. Eliot's term: an object, situation or chain of events that, when shown, produces a specific emotion in the audience. |
| **Visual metaphor** | An image that presents one thing as, or alongside, another so that qualities pass between them. |
| **Metonymy** | Letting a thing closely associated with something stand in for it (in *The Catch*, the empty clip for the missing puck). |
| **Synecdoche** | A kind of metonymy: a part standing for the whole (a hand for a person). |
| **Subtext** | What a character thinks, feels or knows but does not say. |
| **Core opposition** | The two poles the story's theme swings between, named as two nouns. |
| **Hinge** | A motif that crosses from one pole of the core opposition to the other during the story (Section 3.1, step 4). |
| **Turning point** | A beat where a story value changes (A2's term): something the character cares about moves from positive to negative or the reverse (safe to endangered, trusted to betrayed). |
| **Reveal** | The appearance at which the audience learns what a motif has meant all along; for a hinge it can come before the final payoff. |
| **Teaching shot** | A shot whose job is to show the audience how something works (the needle kicks when something crosses), so a later payoff that depends on it is understood without explanation. |
| **Rhyme** | Repeating an earlier shot's composition (same side, height, size and light) so the audience recognizes the moment by its look. |
| **Eyeline chain** | A run of shots that follows a character's gaze from one thing to the next, so the order of what they look at shows what they are thinking. |
| **Plant** | The first appearance of a motif, which lets the audience notice it without yet knowing what it will mean. (The trade also says "setup"; this file says plant.) |
| **Develop** | A later appearance of a motif in which something has changed: its state, its owner, its surroundings, or what the audience knows. |
| **Payoff** | The appearance where a motif's gathered meaning is spent: it decides, reveals or completes something. |
| **Coda** | One quiet closing appearance after the payoff (emphasis 0 or 1) that confirms the payoff without restating it (the flask's absence in sc29). |
| **Plot machinery** | An object the plot needs in order to work (the courier pod, the key switch) that sits on neither side of the theme; it is framed only so the audience understands what it does. |
| **State** | The physical condition of a thing at a moment in the story: whole, broken, full, empty, clean, bloodied, hidden, reversed, burnt. |
| **State change** | A change of state, whether shown on screen or discovered after a cut. |
| **Emphasis level** | How loudly the camera points at a thing, from 0 (just present) to 3 (the beat is about it). Defined in Section 3.4. |
| **Insert** | A close shot of an object or detail, cut into a scene. |
| **Eyeline match** | A cut from a character looking to the thing they are looking at. |
| **Register** | The written table of all motifs and their appearances; it doubles as the continuity record for props, costume and makeup. |
| **Spine motif / supporting motif / single-scene prop** | The three ranks a harvested thing can receive (Section 3.2). |
| **Continuity** | Keeping every visible detail consistent from shot to shot and scene to scene unless the story changes it. |
| **Mirror state** | Whether an item is drawn as designed or flipped left to right in a given shot (C2's term). |
| **Era** | C2's name for the three stretches of *The Catch* with different mirror states: A before the cage turns, B from the turn until Iona's own turn beside the ship, C from her return to the end (C2, Section 7.3). |
| **Set decorator** | The person in the art department who chooses, buys and places the set dressing. |
| **Art direction** | The older name for production design; the Academy Award category was called Art Direction until 2012. |
| **Breakdown** | The costume trade's word for ageing and distressing clothes (washing, sanding, dyeing, dirtying) so they look lived in and match story events. |
| **Multiples** | Several identical copies of a costume or prop, often made at progressive stages of damage, so a torn or bloodied state can be repeated across takes and scenes. |
| **Shape language** | Building a design from one dominant simple shape (square, circle, triangle) because audiences tend to read feelings into shapes (B5). |

**Camera, light and image words used here** (B1, B2 and C2 treat them fully; these one-line versions are enough to follow this file):

| Term | Plain definition |
|---|---|
| **Wide shot** | A shot showing a whole place or a whole body with space around it. |
| **Medium close (shot)** | A shot framing a person from about mid-chest up, or an object at a similar scale. |
| **Two-shot** | A shot with two people in it; "profile" means both are seen side-on. |
| **Point-of-view shot** | A shot that shows what a character sees, from where they are. |
| **Over-the-shoulder shot** | A shot taken from behind one character's shoulder, looking at what or whom they face. |
| **Long lens / macro** | A long (telephoto) lens frames a subject tightly from far away; seen from that distance, near and far things look pressed together (the flattening comes from the camera's distance, which the long lens makes usable) and the background blurs into a soft wash. A macro lens focuses very close, for tiny details such as a fingertip in oil. |
| **Push-in, tracking, crane, tilt** | Camera moves: toward the subject; alongside it; up or down through space on an arm; pivoting up or down on the spot. |
| **Strong points of the frame** | The places the eye goes first: the center, and the four points where lines dividing the frame into thirds cross (B3). |
| **Value** | How light or dark a surface is, regardless of its color. "Contrasting value" means light against dark. |
| **Saturated / desaturated** | A saturated color is intense and pure (a new red tag); a desaturated one is greyed or faded (brick dust). |
| **Raking light** | Light skimming across a surface at a low angle, so texture and polish show. |
| **Highlight** | The brightest spot where light reflects off a surface. |
| **Practical** | A light source that is visible in the shot and exists in the story (a torch, a lamp, a screen). |
| **Rim light** | Light from behind or beside a subject that draws a bright line along its edge. |
| **Hero lighting** | Extra light aimed at one object or face to make it the brightest, cleanest thing in the frame. |
| **Negative prompt** | A separate field, in some image and video tools, that lists what the model should leave out. |
| **Mix** | The balance of sounds in the finished soundtrack: which are loud, which are quiet, which drop out. |
| **Composite** | To combine separately made images into one frame (for example, adding exact text onto a generated prop). |
| **Previs** | Previsualization: a rough 3D or drawn mock-up of shots made before final images (C4). |
| **Asset sheet** | A reference page of images showing one character, prop or set from several angles and in each state, given to image models for consistency (C2). |
| **Cross-dissolve / montage** | A cross-dissolve (older name: lap dissolve) fades one shot into the next; a montage is a fast series of shots that compresses time or builds an idea. |
| **Soundstage** | A large soundproofed studio building where sets are built. |

Color meanings for *The Catch* (red as a limit and its cost, green as fit, yellow as the line, flat black as the engines, Iona's blue shirt) are defined in B2, Section 8.4. This file uses those meanings and does not redefine them. Camera terms (shot size, lens, angle) are defined in B1. Asset sheets and the mirror-state rule for *The Catch* are in C2, Section 7.

---

## 1. Core principles

1. **Harvest before you invent.** The strongest motifs are already in the text: named, handled by characters, and needed by the plot. *The Catch* names nearly all of its own. Invent a new object only to fill a beat that has no thing in it, and flag it as an invention.
2. **A motif is built by change, not by repetition.** Each return must show something new: a new state, a new owner, a new neighbor in the frame, or new knowledge in the audience. The same object in the same state and the same framing is wallpaper.
3. **The audience should feel the meaning before they can name it.** This is the point of Eliot's objective correlative and of McKee's image system: the thing carries the feeling; nobody explains it.
4. **Every symbolic thing needs a plain, practical reason to be there.** The red tag is a real safety sign on a real freight lift; the mint is a plant on a kitchen sill. If an object makes sense only as a symbol, the audience will read it as the author's hand. McKee's warning in *Story* is the reason (wording as reproduced on one writing blog, Karen Woodward's, not checked in print): symbols move us only while we do not recognize them as symbols, and "Awareness of a symbol turns it into a neutral, intellectual curiosity, powerless and virtually meaningless."
5. **Emphasis is a budget.** Most appearances sit quietly in the set. Each motif gets at most one loud (level-3) moment (a second only when it deliberately inverts the first; Section 3.1, step 9). That moment is its payoff or, for a hinge whose meaning is revealed mid-story, that reveal; it is never the plant.
6. **The plant must be clear, not big.** The audience must see the thing once, plainly, in context, so they can recognize it later. Clarity comes from composition and light, not from size.
7. **States are story.** A thing broken, emptied, reversed, returned, burnt or given away is a turning point made visible. Track states as carefully as dialogue.
8. **The camera's attention is the author's voice.** Size in frame, position, light, focus, and whether a hand touches the thing decide how loudly it speaks.
9. **Meaning needs an opposite.** A thing means more when its opposite is also on screen: the rung that betrays her habit and the sill that rewards it; the black suit and the white suit.
10. **Sets are histories and minds made physical.** What is there, what is missing, what is worn, what is clean, what is high or low, open or shut.
11. **Costume is the arc worn on the body.** Silhouette, color, texture, fit, wear and damage change when the character changes, and not otherwise.
12. **Continuity is part of meaning.** A wound on the wrong hand or a prop in the wrong state breaks the chain a motif depends on. AI tools break continuity easily, so the register must also serve as the continuity record.

---

## 2. The theory, stated carefully

### 2.1 Mise-en-scène

David Bordwell and Kristin Thompson's textbook *Film Art: An Introduction* (first edition 1979; recent editions co-written with Jeff Smith) treats mise-en-scène as the filmmaker's control over what appears in the frame, under four headings: setting, costume and makeup, lighting, and staging (the performers' positions and movement). Framing and camera belong to cinematography in their scheme. This pipeline splits the same ground: light is in B2, camera in B1, and this file covers setting, props, costume, makeup and the handling of objects. The stance taken from *Film Art*: judge each element by what it does in the story (motivates action, characterizes, builds a motif), so every thing on screen can answer "what is your job in this scene?"

### 2.2 The objective correlative

T. S. Eliot, in the essay "Hamlet and His Problems" (1919; collected in *The Sacred Wood*, 1920), wrote: "The only way of expressing emotion in the form of art is by finding an 'objective correlative'; in other words, a set of objects, a situation, a chain of events which shall be the formula of that particular emotion." He goes on to say that when those external facts are given, the emotion is evoked. The phrase was not his invention; the American painter Washington Allston had used it earlier. Eliot's use made it a standard critical term.

Eliot's argument is also a warning. He judged *Hamlet* a failure because, in his view, Hamlet's emotion is bigger than the facts the play gives it. For this pipeline that means two tests:

- **Missing correlative.** If a beat's inner state (from the A2 breakdown) has no object, place or action carrying it, the screen will fall back on the actor's face and the music. Find or propose a thing.
- **Oversized emotion.** If the emotion is far bigger than the things shown, do not fill the gap with symbolic decoration. Fill it with action, or accept that the actor carries it.

### 2.3 Visual metaphor, metonymy and synecdoche

**Metaphor by cutting.** Sergei Eisenstein's *Strike* (1925) ends by cross-cutting the army's massacre of workers with footage of cattle being slaughtered. The cut joins the two images and the audience makes the comparison. In a narrative film this now usually reads as the director editorializing; use it only in a film whose style is already openly rhetorical.

**Metaphor inside one image.** Noël Carroll's essays on visual metaphor (1994) and film metaphor (1996) argue that the clearest visual metaphors fuse two things into one figure in one space (his term is "homospatial"); Trevor Whittock's *Metaphor and Film* (1990) catalogues many forms. Further reading, not rules.

**Metaphor inside the story world (the safest kind).** An object literally exists in the story, literally does something, and what it does also resembles the theme. The audience gets the literal meaning first, so the metaphor never has to be accepted on trust. In *Parasite* (2019), a family friend, Min-hyuk, gives the Kim family a scholar's rock that is meant to promise wealth; later the son, Ki-woo, takes it into the bunker, and Geun-sae uses it to bludgeon him. The rock is a gift, a burden and a weapon without ever leaving the plot. In *The Catch*, Saye's toy carriage and paper F are teaching models a scientist builds to explain what happened. They are also the story's metaphor for the family: a thing that has been turned cannot turn back without an engine.

**Metonymy and synecdoche.** The linguist Roman Jakobson's 1956 essay on two aspects of language (the section usually cited is "The Metaphoric and Metonymic Poles") set metaphor, which works by similarity, against metonymy, which works by nearness, and linked metonymy with realism. Film leans toward metonymy because close shots isolate parts that stand for wholes. Jakobson says as much in passing (paraphrased from online copies of the essay, not checked in print): since D. W. Griffith, cinema has used a great variety of synecdochic close-ups (a part shown for the whole) and metonymic set-ups (camera placements that show a thing through what is next to it), and Chaplin's and Eisenstein's films laid a metaphoric montage over them, whose lap dissolves he called "filmic similes" (a simile being a comparison made openly, "like" or "as"). Operationally:

- *Metonymy* in *The Catch*: "The clip under it is empty." The empty clip stands for the missing puck, and the missing puck stands for a decision Eli has made and hidden.
- *Synecdoche* in *The Catch*: the strip of Iona's sleeve kept in a labeled container. A part of her clothing stands for her, which is exactly how the collector treats it.

A realistic story like *The Catch* should prefer metonymy and in-world metaphor. Cut-based metaphor would break its plain, physical style.

### 2.4 Motif, motif system and leitmotif

*Film Art* treats repetition with variation as a basic principle of film form and uses "motif" for any significant repeated element. The two halves matter equally: repetition makes the thing recognizable; variation makes it mean something.

Robert McKee's *Story* (1997) defines an Image System as "a strategy of motifs, a category of imagery embedded in the film that repeats in sight and sound from beginning to end with persistence and great variation, but with equally great subtlety, as a subliminal communication to increase the depth and complexity of aesthetic emotion." (Wording as reproduced on Goodreads, checked 2026-09-27; not checked against a printed copy.) Note the three demands: a *category* (not one object but a family of related images), *variation*, and *subtlety* (it should work below conscious notice). He also contrasts External Imagery, which takes images that already carry a symbolic meaning outside the film (a national flag, a cross) and uses them unaltered, with Internal Imagery, which he favors: it "takes a category that outside the film may or may not have a symbolic meaning attached but brings it into the film to give it an entirely new meaning appropriate to this film and this film alone." (That sentence as reproduced on two writing blogs; the flag and cross examples are a paraphrase from memory; neither checked in print.) The practical rule: an object's meaning should come from what happens to it in this story, not from what it means in general culture.

"Leitmotif" comes from music. The Wikipedia summary (checked 2026-09-27) notes that Friedrich Wilhelm Jähns used the word in print in 1871, and that Hans von Wolzogen popularized it in 1876 in a guide to Wagner's *Ring*; John Williams's two-note shark theme in *Jaws* (1975) is a famous film example. In this file a leitmotif is a motif tied to one being. In *The Catch*, the pump's "Three uneven strokes" is the leitmotif of the figure, and later of the animal inside it.

### 2.5 Emblems

An emblem is a character's signature object. Two verified examples:

- *Citizen Kane* (1941): the sled the boy Kane was playing on in the snow the day he was taken from his mother is thrown into a furnace at the end, and only the audience sees that its trade name is "Rosebud". The glass snow globe Kane holds while saying "Rosebud" (after Susan leaves him, and again as he dies) is a second emblem of the same lost childhood.
- *Schindler's List* (1993): in a mostly black-and-white film, a small girl in a red coat is the only color during the liquidation of the Kraków ghetto; she is later seen dead, recognizable only by the coat. (The film's other color is kept to candle flames near the start and end and the color epilogue, which is why the coat reads.) Spielberg (as quoted on Wikipedia): "It was as obvious as a little girl wearing a red coat, walking down the street, and yet nothing was done to bomb the German rail lines."

Emblems need a look that is recognized instantly and never drifts: a distinct silhouette, a distinct color, a fixed size.

### 2.6 Plant and payoff, and the MacGuffin

Anton Chekhov's principle is usually cited from his letter of 1 November 1889 to A. S. Lazarev (pen name of A. S. Gruzinsky): "One must never place a loaded rifle on the stage if it isn't going to go off. It's wrong to make promises you don't mean to keep." (Translation as given on Wikipedia, checked 2026-09-27. Other versions come from memoirs by Ilia Gurliand, 1904, and Sergius Shchukin, 1911, and wording varies.) The reverse also holds: a payoff with no plant feels like a cheat.

Alfred Hitchcock described the opposite device in his interviews with François Truffaut (*Hitchcock*, 1967): the "MacGuffin", the thing the characters care about but the audience need not understand. *Notorious* (1946) shows both side by side. The MacGuffin is uranium ore hidden in wine bottles. The emblem of the heroine's danger is a key: during a party the camera starts high and wide above the entrance hall and travels all the way down to her hand, ending close on the stolen wine-cellar key she is holding. The lesson for the pipeline: spend camera emphasis on the object that carries a character's risk or choice, not on the plot device. In *The Catch*, what is inside the flask (a culture) is close to a MacGuffin: the audience never needs to see it. The flask itself is not; it is Eli's emblem and gets one loud moment, when Iona decides its fate (sc24). The puck, which is Eli's secret choice, is the other half of that emblem, so the empty clip and the puck deserve the camera's attention, and the flask's contents never do.

*Suspicion* (1941) shows emphasis by light: a bulb inside a glass of milk made it glow as it was carried upstairs, sharpening the fear that it was poisoned. Copied directly, it is now a cliché.

### 2.7 "Show, don't tell" as a conversion procedure

In *Dialogue* (2016), Robert McKee defines showing as presenting characters who pursue their desires through actions in a believable setting, and telling as making characters stop and talk about their feelings or histories. When a scene over-talks, he advises: "make image substitute for language", by two routes: paralanguage (gesture, expression) and physical action. This file adds a third route: **things** (objects, places, clothes, marks). (The popular "Don't tell me the moon is shining; show me the glint of light on broken glass" is a later condensation, not Chekhov's words. What he wrote to his brother Alexander in 1886, in the translation Wikipedia gives, was: "In descriptions of Nature one must seize on small details, grouping them so that when the reader closes his eyes he gets a picture. For instance, you'll have a moonlit night if you write that on the mill dam a piece of glass from a broken bottle glittered like a bright little star, and that the black shadow of a dog or a wolf rolled past like a ball." The real advice is the useful one for this file: a small, specific, physical detail in a precise place, not a general image.)

David Mamet's *On Directing Film* (1991) pushes the same idea into shot design: tell the story by cutting between plain, uninflected images and let the audience make the meaning from the juxtaposition, rather than loading single shots with emphasis.

**The conversion procedure (run it on any beat with an inner state):**

1. Write the subtext in one plain sentence ("Eli knows what he did and will not say it").
2. **Action:** what does the character do with a thing because of that feeling? ("He looks down at the flask in his hand for a long time.")
3. **Harvest:** which thing already in the scene sits nearest to the feeling? (the flask)
4. **State:** which state of that thing matches the feeling? (held, closed, looked at, not explained)
5. **Emphasis:** choose the lowest emphasis level at which the audience will still register it.
6. **Words:** in prose adaptations, the thing may replace a narrated sentence. In a screenplay, keep the writer's dialogue; the thing adds subtext under it.

### 2.8 Subtext carried by objects

McKee's *Dialogue* (Chapter Three) divides a character's content into the said, the unsaid (conscious thoughts kept private) and the unsayable (drives the character cannot put into words). Objects are among the best carriers of the unsaid, because an object can be looked at, held, hidden or handed over without a word.

*Rear Window* (1954) shows one object carrying three meanings to three people. Lisa signals to Jeff that she is wearing Mrs. Thorwald's wedding ring; seeing this, Thorwald realizes Jeff is watching his apartment. To Lisa the ring is proof, to Jeff it is triumph and then danger, to Thorwald it is exposure.

The Kuleshov experiment (known from Pudovkin's 1929 account; no footage survives) claims that a neutral face reads as hunger, grief or desire depending on the object cut next to it (a bowl of soup, a girl in a coffin, a woman on a divan). Tests are mixed but lean toward the effect: a 1992 recreation (Prince and Hensley) found none, while later studies (Mobbs and colleagues, 2006; Barratt and colleagues, 2016) found that context does change how a neutral face is read. The pipeline's use: an eyeline match from a face to an object tells the audience what the character is thinking without dialogue.

### 2.9 What practitioners did

Each line below states only what was verified (sources at the end). Where a designer's method could not be verified, only credits are given.

| Designer (role) | Work | What happened | What to take from it |
|---|---|---|---|
| **Ken Adam** (production designer) | *Dr. Strangelove* (1964) | The War Room: an enormous triangular concrete room (Kubrick's idea was that a triangle would best resist a blast) with a circular table under a ring of lamps, suggesting a poker table. Kubrick had the table covered in green baize (the green felt of a card table), invisible in black and white, so the actors would feel they were playing "a game of poker for the fate of the world". | A set can hold a metaphor through shape and light alone; some choices are for the performers, not the lens. |
| **Jack Fisk** (production designer) | *Days of Heaven* (1978) | Built the mansion in the wheat fields from plywood; not a facade (a front wall only, propped from behind) but complete inside and out, in period colors: brown, mahogany and dark wood inside. | A lone, complete house on open land is the object of desire, and the camera can go anywhere in it. |
| **Bo Welch** (production designer) | *Edward Scissorhands* (1990) | "a kind of generic, plain-wrap suburb, which we made even more characterless by painting all the houses in faded pastels, and reducing the window sizes to make it look a little more paranoid." | Small measurable changes (window size, faded color) change a place's psychology. |
| **Wynn Thomas** (production designer) | *Do the Right Thing* (1989) | Altered the street's color scheme with a great deal of red and orange paint to convey a heat wave. (In the same film Radio Raheem wears brass knuckle rings reading "hate" on his left hand and "love" on his right, an homage to *The Night of the Hunter*, 1955; they belong to the character's costume, which was Ruth E. Carter's department, so they are not credited to Thomas here.) | Pressure can be painted; the theme's opposition can be worn, one pole per hand. The rings work because the film is openly rhetorical and the character performs a speech about them; in a realistic register like *The Catch*, lettering that names the theme would be heavy-handed (Section 13, "The announced symbol"). |
| **Hannah Beachler** (production designer) | *Black Panther* (2018) | Wikipedia credits the director, Ryan Coogler, with "a project bible that detailed each Wakandan tribe to guide the design process". Beachler's own design bible was far larger; in a 2019 interview for the Motion Picture Association's site *The Credits* she said: "We created this bible that set the foundation for Wakanda. That was like 500 pages of reference pictures and timelines and information about traditions and tribes and vibranium and how that came to be." She "met with architects, anthropologist, geologists and physicists", and gave each tribe its own sigils (emblem marks) and architecture: the Border Tribe drawn from Lesotho, the Merchant Tribe's sigil from Nigerian writing, the Golden Tribe's sun symbol. First African American to be nominated for, and to win, the Oscar for production design. | Write the world's visual rules and their history down before designing, then give each group its own consistent marks. The register is that kind of document. |
| **Ruth E. Carter** (costume designer) | *Black Panther* (2018) | Color schemes per tribe; the Dora Milaje's neck rings and arm bands (referencing the Southern Ndebele) show rank: gold for General Okoye, silver for the others. First African American to win in costume design, later a second time. | Costume codes must be simple, consistent and legible at a glance. |
| **Sarah Greenwood** (production designer, often with set decorator Katie Spencer) | *Atonement* (2007); *Anna Karenina* (2012); *Barbie* (2023) | Joe Wright shot most of *Anna Karenina* on one soundstage representing a dilapidated theatre. For *Barbie*, Greta Gerwig's name for the look was "authentic artificiality" (a painted sky on a soundstage: "an illusion, but it's also really there"). In *Atonement* the vase Robbie accidentally breaks while arguing with Cecilia at the fountain starts the misreading that drives the story (Cecilia strips and climbs into the fountain after a broken piece while Briony watches and misreads what she sees); the vase comes from Ian McEwan's novel, so it is an example of a story object the design had to make precious and specific, not a design invention. | A whole film can be one set-metaphor if it commits openly; a single broken object can start a tragedy if it was shown whole and valued first. |
| **Rick Carter** (production designer) | *Jurassic Park* (1993); Oscars for *Avatar* (shared) and *Lincoln* (shared) | Did not want the park to have "a lot of commercialized edifices that feel shallow and overly bright and overly energetic"; it was deliberately not designed to look like Disneyland. | Restraint: a place meant to impress can still feel real. |
| **Lee Ha-jun** (production designer) | *Parasite* (2019) | The Park house was built for the film. Lee: "Each character and each team has spaces that they take over, that they can infiltrate, and also secret spaces that they don't know." He put blocking (where actors stand and move) and camera angles ahead of normal architectural logic. Bong Joon-ho called it an "upstairs/downstairs" or "stairway movie", with staircases showing the families' positions. | Design a set as a map of who controls which space and who is hidden where; vertical architecture can carry class; design for the shots, not for a real architect. |
| **Edith Head** (costume designer) | *Vertigo* (1958) | Madeleine's grey suit was chosen to be psychologically jarring, grey not being usually a blonde's color. | A costume can feel wrong on purpose, planting unease the plot later explains. |
| **Deborah Nadoolman Landis** (costume designer, historian) | *Raiders of the Lost Ark* (1981); *Thriller* (1983) | Designed Indiana Jones's fedora and jacket and Michael Jackson's red jacket; wrote *Screencraft: Costume Design* (2003) and *FilmCraft: Costume Design* (2012). In an interview with *The Talks* she put her method plainly: "Costume design, unlike what the audience may think, is more about the conversation than about clothes", and "The clothes have no meaning without the story." | Start from who the character is and what has happened to them; the clothes follow. |
| **Colleen Atwood** (costume designer) | Tim Burton's films, including *Edward Scissorhands* (1990), where her black leather-and-buckles outsider stands out against Bo Welch's pastel suburb (row above); Oscars for *Chicago*, *Memoirs of a Geisha*, *Alice in Wonderland*, *Fantastic Beasts* | To *The Talks*: "You want the costumes to resonate in a way that is real, even if it's a made up kind of real." To NPR (2016), on how her own working life helps: "when I get a job and somebody is described as a waitress and a mother, I kind of know what their life was really like and what they really looked like and how they lived." | Even an invented world's clothes must look worn by a real life; a single contrasting silhouette can carry an outsider. |
| **Dante Ferretti** (production designer) | *Gangs of New York* (2002); Pasolini, Fellini, Scorsese; three Oscars for art direction (*The Aviator*, *Sweeney Todd*, *Hugo*), shared with his wife, the set decorator Francesca Lo Schiavo | For *Gangs of New York* he rebuilt over a mile of mid-nineteenth-century New York on the outdoor stages of Cinecittà in Rome, including the Five Points slum, which he based on George Catlin's 1827 painting of it (Wikipedia). | Dressing as social history: research a real period image and build from it, so the place carries class and time before anyone speaks. |
| **William Chang Suk-ping** | *In the Mood for Love* (2000) | Credited for production design, costume and editing. Credits verified; no statement of method verified, so none is claimed. | Study material for one designer giving set and costume one voice. |
| **Pixar** (character design) | *Up* (2009) | Pete Docter: Carl's "squarish" design symbolizes "his containment within his house"; Russell is "rounded like a balloon". Near the end Carl empties the house of its contents so it can fly again. | Shape language (a design built from one dominant simple shape) for characters; a set the hero must empty to change. |

### 2.10 Two working toolkits: Van Sijll and Block

**Jennifer Van Sijll, *Cinematic Storytelling* (Michael Wiese Productions, 2005).** The book catalogues 100 film conventions in 17 chapters, which the publisher calls "17 basic building blocks" of film language, and pairs each convention with the story job it does, frame grabs and a script excerpt; the publisher stresses showing character change without dialogue. The method is what matters most here: every visual choice gets a name, a stated story function, and the exact script moment it serves. The register entries in Section 9 follow that pattern (thing, meaning, script line, framing).

Four of its chapters are this file's territory. Their convention names and film examples, from the book's contents list (as recorded in Stanford's library catalogue, checked 2026-09-27), are:

| Chapter | Conventions (film example) | What this file takes from the name (a reading of the names, not a summary of the book's text) |
|---|---|---|
| **Props** | Props (externalizing character): *Barton Fink*, *Raging Bull*; Re-purposing props: *Bound*; Contrast: *Harold and Maude* | An object can show an inner state; an object put to a second use carries a turn in the story; two objects set against each other show an opposition |
| **Wardrobe** | Wardrobe: *Ed Wood*; Re-purposing wardrobe: *Out of Africa*; Contrast of wardrobe: *Bound* | The same three moves applied to clothes |
| **Locations** | Defining character: *Hedwig and the Angry Inch*; Location as unifying element: *The Sweet Hereafter*; Location as theme: *Blue Velvet*; Moving locations: *Dead Man* | A place can define a person, hold a film together, state the theme, or travel |
| **Natural elements** | Climate: *The Sixth Sense*; Seasons and the passage of time: *Amélie*; Physical phenomena: *Dolores Claiborne* | Weather and physical events used as story, not as mood wallpaper |

Two more conventions touch motifs: "Visual foreshadowing" (*The Piano*, in the Time chapter) and "Music as a moveable prop" (*Out of Africa*, in the Music chapter). In *The Catch*, re-purposing is everywhere and is the safest kind of in-world metaphor (Section 2.3): the drip stand becomes a battering ram and then a trip bar; the oxygen cylinder becomes a weapon; Iona's shirt sleeve becomes a dressing and then the collector's specimen; the toy carriage becomes a way to ask the animal's consent. **Rule:** if the pipeline cites Van Sijll, it names one of these conventions and its film exactly as listed; it does not attribute any wording inside the chapters to her, because the chapter text was not read.

**Bruce Block, *The Visual Story* (Focal Press, 2001; later editions).** Block names the basic visual components (space, line, shape, tone, color, movement and rhythm) and states a Principle of Contrast and Affinity: the more contrast within a component, the higher the visual intensity; the more affinity (likeness), the lower. (Paraphrase; the wording is not quoted.) For motifs this is the mechanism behind emphasis levels. A thing gets louder when it contrasts with its surroundings in one component (the only saturated red in a grey tunnel; the only moving thing in a still frame) and quieter when it shares them. It also gives a way to plan a motif's arc: for each appearance, decide which one component contrasts and by how much, and save the largest contrast for the payoff. Block also teaches that a component carries the meaning the story gives it, not a fixed dictionary meaning, which is why the tables in Sections 4.2 and 5.2 say "tends to".

**Practical use of Block for shapes.** Give each pole of the core opposition a shape and material family built from the things already harvested (Section 3.1, step 8). A new object can then be sorted at a glance, and a hinge can be designed as a mix of both families.

---

## 3. The motif procedure

### 3.1 Ten steps

1. **Theme as a question.** Write the theme as a question the story tests, not as a moral. *The Catch*: "When you carry someone, do you carry them as goods (weighed, decided for, sealed away) or as a person (asked, told, touched)?"
2. **Core opposition.** Name the two poles as nouns. *The Catch*: **GOODS** against **PERSONS**. The story states it on its first prop: "Goods only. No persons." A second opposition runs beside it: **FIT** against **TURNED** (belonging to the world against no longer fitting it).
3. **Harvest.** List every concrete thing the text names more than once, or names at a turning point. Include sounds, words on things, and marks on bodies. Note each appearance with scene number and what happens to it.
4. **Sort.** Put each thing on a pole, or mark it as a **hinge**: a thing that crosses from one pole to the other during the story. Hinges are the most valuable motifs. In *The Catch*, the figure is a hinge (it treats people as goods, then turns out to be a person inside goods), and so is the strip of sleeve.
5. **Test and rank** (Sections 3.2 and 3.3).
6. **Meaning and direction.** Give each spine and supporting motif a one-line meaning in plain words and a direction of travel: how its meaning moves (the pump: threat to heartbeat).
7. **Map appearances.** For each appearance, record scene, state, owner (who holds or controls it), emphasis level, framing (size, position, light, focus, handling) and what the audience knows at that moment.
8. **Design the look.** Silhouette, color (from B2), material and size, chosen so the thing reads in a wide shot as well as a close one. Each spine motif must be distinguishable in silhouette from everything else in its scenes. Then give each pole a **shape and material family** taken from the harvested things, in one line per pole (Section 2.10). *The Catch*: GOODS = grids, rectangles, boxes, printed labels, hard flat-black shells; PERSONS = hands, cloth, curved clear glass, water. A hinge mixes the two (the vessel: a hard mount and a pump holding curved glass and water). Any object invented later must belong to one family.
9. **Check the budget.** At most one emphasis-3 moment per turning point, and at most two per scene; if a scene has two, they must sit on different turning points with at least one lower-emphasis shot between them. Most scenes have none. At most one emphasis-3 moment per motif (two only if the second is a deliberate inversion of the first). Count sound motifs on their own scale (Section 3.4).
10. **Hand off.** Write the state table (Section 9.4), give C2 one asset sheet per state of each spine motif, and put the register IDs into the shot specs.

### 3.2 How many motifs is too many

These are working rules from practice, not sourced numbers.

- **Spine motifs** carry the core opposition. Each gets a full plant, at least one develop, and a payoff with one emphasis-3 moment. Count them per channel (next bullet). Visual objects, places and colors: three to five for a short film (under about 40 script pages), five to eight for a feature. More than that and they compete for the same beats.
- **Separate channels do not compete.** There are three channels: visual (objects, sets, colors), sound, and the body (wounds, scars and other makeup marks). Allow at most one extra spine motif in the sound channel and one in the body channel on top of the visual cap. A body mark counts as its own channel only while it stays on the body; if it needs an insert of its own more than once, count it as visual.
- **Supporting motifs** add texture and clarify story logic. They never rise above emphasis level 2, except at their own single payoff if that payoff is also a plot beat. No fixed cap, but if the register has more supporting than spine motifs by more than two to one, demote the weakest to set dressing.
- **Single-scene props** are planted and paid off inside one scene (the mint). They need no register entry beyond one line.
- **If two spine motifs want the same payoff moment**, merge them (the rings become the payoff of the glass motif) or move one payoff to a neighboring beat.

### 3.3 Strong or decorative: six tests

Score one point per "yes".

1. **Source:** is it named in the text, or an obvious property of something named?
2. **Physical:** can a camera see it, or a microphone hear it, without a caption?
3. **State:** does it change state at least once?
4. **Link:** does a change in it coincide with a turning point (a story value changing, in A2's terms)?
5. **Handling:** does a character touch it, look at it, or act because of it?
6. **Removal:** if you cut it, is a beat lost, or does a payoff lose its plant?

**5 to 6:** spine candidate. **3 to 4:** supporting motif. **1 to 2:** decorative; allow it only as set dressing at emphasis level 0. Three overrides, applied in this order:
- If every appearance falls inside one scene, it is a **single-scene prop** whatever its score (the mint scores 6 but lives in sc10 only).
- If it scores high but sits on neither pole of the core opposition, it is **plot machinery**: frame it for clarity, not meaning (the courier pod, the key switch).
- If it fails test 1 (Source), it can be at most supporting and must be flagged as an invention, whatever its other scores.

**Ties.** If there are more spine candidates than Section 3.2 allows, keep first the ones that are hinges, then the ones with the most state changes, then the ones the characters handle; demote the rest to supporting.

### 3.4 Emphasis levels: how the camera builds a motif

| Level | Name | Size and position in frame | Light and focus | Handling | Use for |
|---|---|---|---|---|---|
| **0** | Present | Small, part of the set or costume, off the strong points of the frame | Scene light only; may be soft | None | Plants of supporting motifs; most returns |
| **1** | Placed | Small to medium, on a strong point of the composition or near a face or eyeline | Catches a highlight, or sits against a contrasting value | Sharp | Plants of spine motifs; quiet develops |
| **2** | Featured | Medium close or insert; centered or on a third | Clearly lit; background softened | A character handles it or looks at it (eyeline match) | Develops that change state; shots that teach a rule |
| **3** | Spent | It dominates: an insert, a held frame in which it is the only sharp or only moving thing, or a rhyme of the plant's composition | Scene light. At most one added signal (a motivated light change, a sound change, or an unmotivated camera move toward it), and none if the script already marks the beat (rule 23) | The beat turns on it | Payoff (or a hinge's reveal), once |

**Plant exception.** Plants sit at level 0 or 1 unless the plant is itself a plot event (a rung breaks, a wound is made, a sign is read aloud, a rule is taught). Then use the level the event needs, at most 2, and add nothing (a held beat, a light, a sound) that points past the present moment to the future.

**Sound motifs use their own scale**, set in the mix rather than the frame:

| Level | Name | In the mix |
|---|---|---|
| **S0** | Bed | Present under other sounds; noticed only if listened for |
| **S1** | Clear | Clearly audible, sharing the mix with dialogue and room sound |
| **S2** | Foreground | Other sounds dip under it; it leads the moment |
| **S3** | Alone | Every other sound drops away; it is the only thing heard. Once per sound motif |

**How meaning builds across appearances** (the full rules are 6 to 12 in Section 8): plant low and pay off high; or pay off by exact rhyme of the plant's composition; or, for a hinge, spend level 3 at the reveal and let the final payoff be quiet (level 1 or 2), because by then the audience's knowledge does the work; teach a rule at level 2 before any payoff that depends on it (Hitchcock's bomb under the table, from the Truffaut interviews); change the thing's neighbor in the frame between appearances, because the neighbor is how the meaning moves. **Light follows emphasis:** at levels 0 and 1 the thing gets only the scene's light (B2's location plan); at level 3 a light change is allowed if a source in the scene motivates it.

---

## 4. Sets as psychology

### 4.1 How loud should a set be?

Charles Affron and Mirella Jona Affron, in *Sets in Motion: Art Direction and Film Narrative* (Rutgers University Press, 1995; reprinted 2022), grade sets by how strongly they assert themselves in the narrative, from sets that simply establish a place up to sets that become the story's subject. Their five levels are the book's chapter titles (checked against the publisher's chapter list, 2026-09-27): set as **denotation**, **punctuation**, **embellishment**, **artifice** and **narrative**. The one-line glosses that follow are this file's working reading of those names, not the Affrons' definitions: denotation, the set simply says where and when we are; punctuation, it underlines a moment now and then; embellishment, it is noticeably designed and draws the eye; artifice, it is openly stylized and unreal; narrative, the set is itself the story's subject. The useful idea: decide, per location, how loud the set is allowed to be. Most sets in a realistic story should sit at the quiet end (denotation or punctuation), and only one or two should be allowed to "speak".

In *The Catch*, the loud sets are the collection room (it is a character's mind made into a room) and Saye's kitchen (its emptiness is the point). The loading tunnel, car and corridors should stay quiet and practical. **If** a set is marked loud, **then** it gets one establishing wide at the start of its first scene that shows its governing feature (the kitchen's bare surfaces, the collection room's order) and the rest of the scene is shot for the action; **if** it is quiet, **then** its wides show only what the audience needs to know where people are and what the danger is, and no insert or held shot exists only to show the set.

### 4.2 Space variables and what they tend to say

These readings are tendencies, not laws. Context can reverse any of them.

| Variable | One pole tends to read as | Other pole tends to read as | Watch for |
|---|---|---|---|
| **Fullness** | Clutter: accumulated history, attachment, warmth, or an inability to let go | Emptiness: loss, control, a life withheld or suspended | Clutter that contradicts the character's history; emptiness that looks merely unfinished |
| **Enclosure** | Confinement: low ceilings, near walls, bars, grids, frames within frames (doorways, windows or screens that box a character inside the shot) | Openness: horizon, sky, long sightlines | Using bars and cages for "trapped" when the story has not earned it |
| **Scale** | A room far too big for the people in it: isolation, a life dwarfed by possessions (in *Citizen Kane*, Susan does jigsaw puzzles on the floor of Xanadu's cavernous hall, before a fireplace that cannot warm it, and she and Kane talk across the room at a distance) | A room too small for them: pressure, intimacy forced on people | Giant sets with no story reason; scale that changes between scenes of the same room |
| **Height** | High places: control, overview, escape | Low places and below: the buried, the hidden, the past. Gaston Bachelard's *The Poetics of Space* (1958; English 1964) treats the house's cellar and attic as carrying different kinds of feeling. | Height used without a story reason |
| **Depth** | Deep space (Bruce Block's term in *The Visual Story* for a frame that shows strong depth, with things near and far): distance between people, freedom, choice | Flat or limited space (Block's terms for frames with no depth, or only a little): pressure, no exit | Mixing space types in one scene without a reason |
| **Surface** | Clean: institution, control, sterility | Dirt and wear: labor, time, neglect | Brand-new surfaces in an old place |
| **Order** | Symmetry: ritual, institution, stasis, mirroring | Asymmetry: life, instability | Symmetry everywhere (it stops meaning anything) |
| **Texture** | Hard and smooth (steel, glass, tile) | Soft or porous (cloth, wood, stone) | Textures that fight the light plan (B2, "surfaces times light") |
| **Barrier type** | Opaque (walls, doors): separation you cannot see across | Transparent (glass): contact that is visible but impossible, which usually hurts more | Glass used so often it stops registering |

### 4.3 Set dressing tells history

Dressing answers "who lived here, how long, and what happened". Three tools:

- **Wear patterns.** Wear shows where bodies have been. *The Catch*: the sill "worn bright by other people's sleeves". *The Long Places*: the hollow in the gallery wall "worn, not cut, the way feet wear a threshold rather than tools a door", and the soot above the lamp niches, "layer under layer under layer".
- **Absences.** What is missing tells a story if the rest of the room says something should be there. Saye's kitchen: "No photographs. No magnets on the fridge." Her house holds "nothing of anybody", and she wears a wedding ring. One reading (an interpretation to flag to the user; the script never links them) is that the bareness belongs to the woman who, nineteen years ago, sent Nell across and lost her. The set should allow that reading without stating it: no single object (a lone framed photo turned face down, an empty second chair) that points to Nell.
- **One kept living or personal thing** in a bare room becomes that room's emblem: "A pot of mint on the windowsill, and that is all."

### 4.4 Sets that change

A set can carry an arc in four ways. For each, record both states in the state table.

1. **Revisited in a new state.** *The Catch*: the treatment floor at night, then "by daylight" with "Police lights beyond frosted windows" and "The broken window of Eli's room is being boarded up".
2. **Rhymed with another set.** The ship's "three glass rooms, each with a hospital bed in it", each with a "drawer that goes through his wall", repeat the quarantine rooms and their "transfer drawer". Building the two with the same proportions makes Iona's accusation visible before she says it: the ship's rooms are first glimpsed on Saye's monitor in sc17 ("Jude, beyond it, on his own hospital bed"), a few lines before "It's collecting what turned." / "So are you."
3. **Changed by a character.** Nell asked for outside; "It made the room bigger." A set can show a misunderstanding.
4. **Emptied or destroyed.** After the fire: "Bare bolts in the wall."

**If** a set changes state, **then** shoot the second state from at least one angle that repeats a first-state composition, so the change reads as a change of this place rather than as a new place; **and** log both states in the state table with the scene where the change happens.

### 4.5 The sets of *The Catch*

| Set | What the space says | Key dressing | Change across the story |
|---|---|---|---|
| Loading tunnel | Neglect; the underside of an institution | "Rain that got in years ago and never left"; the freight cage; the red tag | Not revisited; its cage returns as a wreck (sc21) |
| Freight shaft | Vertical danger; habit and memory | Ladder, broken rung, yellow band, bright sill, "lines of light" under gates | Seen through the floor of the descending cage (sc06); from the passage (sc18) as "the dark of the shaft" |
| Treatment floor and Eli's room | Clean institutional cruelty | "Empty bed. Empty bed. Empty bed."; glass windows into every room; locked specimen cabinet | Revisited by day: police lights, Eli's broken window "being boarded up" (sc11) |
| Iona's car | Her own ordinary life, now wrong | Coffee cup "on the wrong side of the gearstick"; mirror | The one familiar place made mirror-strange |
| Saye's kitchen | A life put on hold; control | Bareness; the mint | One scene only; its emptiness may gain a reason in sc17, when Saye says of Nell, "I sent her." (a reading, not stated by the script; flag it) |
| Quarantine rooms | Care as containment | Glass partitions, transfer drawers, grey boxes, sealed meals | Final scenes: the same rooms, chairs moved closer to the glass |
| Ship: human rooms | The same architecture as quarantine | Three glass rooms, drawers through walls, Nell's shelf | Beds removed one by one; Nell's books spill across the deck |
| Ship: collection room | A non-human mind's care, like a museum or a nurse | "Found. Carried here. Sealed. Put in order."; the cage wreck; labeled containers | Burnt, emptied: "Bare bolts in the wall." |
| Receiving room | The threshold, now inside the institution | Yellow floor line; the bright sill; padded floor; the RECEIVING sign | Iona leaves from it (sc18) and returns to it (sc28) |

---

## 5. Props

### 5.1 Kinds of props

- **Emblem:** a character's signature object (Section 2.5). Eli's flask.
- **Action prop:** an object the action needs to work (the drip stand that breaks the glass; the oxygen cylinder swung at the figure; the remote).
- **Hero prop and duplicates:** any prop seen close and also used roughly needs a hero version and duplicates in every state. For AI work, "duplicates" means one reference image per state (C2, Section 6.4).
- **Set dressing that becomes a prop:** the moment a character picks up dressing, it becomes a prop and needs a register line (the mint leaf).

### 5.2 State changes and what they tend to mark

| State change | Tends to mark | Example |
|---|---|---|
| Whole to broken | A rule or safety failing; innocence ending | The rung turns; the vase in *Atonement* |
| Full to empty | Loss, a secret spent, a resource gone | "The clip under it is empty." |
| Hidden to revealed | Truth, exposure | The puck on the recording, "clipped to the grid" |
| Kept to given up | Trust, sacrifice | Iona clamps her engine to the burning cabinet: "She deletes the way home."; Emre gives Nilay the ribbon |
| Lost to returned | Recognition, an old debt closing | The red ribbon in *The Long Places* |
| Right way to reversed | Estrangement, no longer fitting | The carriage's F; the rings on opposite hands |
| Intact to burnt | An ending; a decision that cannot be undone | The puck "burnt into the grid"; the flask sent "with the fire" |
| Clean to bloodied | Cost paid for someone | The sleeve "stiff with Jude's blood" |
| Labeled | Being classified, owned or cared for | "IONA VALE", copied "stroke for stroke" |
| Put to a second use (Van Sijll's "re-purposing", Section 2.10) | A turn in the situation; a meaning moved from one side to the other | The drip stand becomes a ram, then a trip bar; the sleeve becomes a dressing, then a specimen; the teaching carriage becomes a way to ask the animal |

### 5.3 Continuity of states

A state must either change on screen or be explained by a cut the audience accepts (time has passed, someone has acted off screen). The pipeline records every spine and supporting object in the state table (Section 9.4) with one row per scene. Two rules matter most:

- **Change a state only at the beat that means it.** If the sleeve is torn in the catch, it must look torn in every shot after the catch, including wide shots where no one is looking at it.
- **Asymmetric details need a side.** Rings, wounds, torn sleeves, a half-smile: record which side, because image models get sides wrong (C2) and *The Catch* makes sides part of its plot.

### 5.4 Props in dialogue scenes

McKee's *Dialogue* (Chapter Three, "Action versus Activity") separates activity, the visible surface of behavior (playing cards, sipping wine, talking), from action, what the character is actually doing to someone beneath it (consoling, ridiculing, confessing). For McKee every activity carries an action; even silence is an action. Props are where activity becomes visible, so the pipeline's job in a dialogue scene is to choose prop business whose surface lets the audience read the action underneath. Three patterns:

- **The prop carries the unsaid.** "He looks down at the flask in his hand for a long time." / "Drive."
- **The prop passes between hands and power passes with it.** In sc13, "Iona pauses the recording with the remote" to confront Eli; at the end, "Jude takes the remote and switches it off", ending the argument no one else can end.
- **The prop tests the body instead of a question.** Saye does not ask Iona whether she has changed; she hands her a mint leaf. "What does it taste of?" / "Not mint."

---

## 6. Costume and makeup as arc

### 6.1 The variables

| Variable | What it carries | Typical change at a turning point |
|---|---|---|
| **Silhouette** (outline of the whole figure) | Role, power, strangeness | Armor or a suit added; a coat removed |
| **Color** | Group, allegiance, the character's place in the palette (B2) | A shift toward the opposite pole's color |
| **Texture** | Class, work, softness or hardness | Soft to hard (armor), or the reverse |
| **Fit** | Comfort in one's life; borrowed or imposed identity | Clothes that are someone else's (hospital blanket, oversuit) |
| **Wear** | Time, labor, poverty or care | Sudden wear from one event |
| **Damage** | A cost paid | Torn, bloodied, burnt |
| **Coverage** | Exposure, protection, containment | Hood, helmet, tent |
| **Marks on the body** (makeup) | History that cannot be taken off | A new scar, a chipped tooth, a bandage |

Costume departments plan this with a **costume plot**: a chart listing every character's costume in every scene, with each distinct outfit numbered as a "change". The pipeline's state table is the same thing, merged with props and makeup. Three more pieces of standard practice carry over directly:

- **Breakdown before the camera.** Clothes are aged and distressed to match the life and the events (glossary). For example (design choices, not script facts): Iona's work clothes washed soft and worn at the knees and cuffs before sc01; Eli's coat creased from weeks of lying in it. **If** a prompt or asset sheet describes a working character's clothes, **then** it names the wear ("faded at the seams, knees rubbed pale"), because models default to new, pressed clothes.
- **Multiples in stages.** A costume that is damaged during the story is made several times, one copy per stage (whole, torn, torn and bloodied). For AI work, each stage is one reference image (C2), named with its first scene.
- **Makeup in numbered stages.** Wounds are planned as stages (fresh, bleeding, dressed, healing, scarred) tied to story time, not shooting order. Iona's palm: raw (sc06), reopened (sc09), dressed (sc11), bandaged (sc11 on). The chipped tooth has one stage and never changes.

**Five questions to answer for every character before describing any clothes** (standard costume-design practice, stated here as a working procedure, not as any one designer's words):
1. **Choice:** what would this person choose to wear, given their taste and what they want others to think?
2. **Means and job:** what can they afford, and what do their work and the place require (Iona's work clothes; Saye "fully dressed at four in the morning")?
3. **History:** how old are the clothes, who bought them, how have they been worn, mended, washed?
4. **Events:** what has happened to the clothes in the story so far (blood, tears, a sleeve gone, a borrowed blanket)?
5. **Imposed identity:** is anything on them put there by someone else (a wristband, a printed suit, a label)? In *The Catch* this question carries the GOODS pole.
Write the answers as nouns, materials and states; the description of the outfit follows from them, never the other way round.

### 6.2 When a costume should change

Change a costume at a turning point, or because time and circumstance force it, never for variety. *Vertigo* shows the principle: Madeleine's grey suit was chosen to feel slightly wrong, and when the hero later forces another woman into the same clothes, the costume is the plot. In *Black Panther*, rank and group are coded so that a change of band or color would itself be news.

**Cluster damage on one side.** If a character is injured several times, putting the damage on one side of the body keeps the other side clean for an emblem. In *The Catch*, this is a design recommendation, not something the script states: put Iona's skinned palm and her torn sleeve on her right arm (the arm that catches the sill), so her left hand stays clean for the ring, which must read at the end.

### 6.3 Costume and makeup arcs in *The Catch*

- **Iona.** Practical work clothes with a blue shirt (B2 requires the blue from sc01, or the collection-room strip has nothing to recall). By sc07 only "what is left of her shirt sleeve" remains to press into Jude's wound; the script does not say how it tore, and this file recommends it tears on the sill in the catch. A hospital blanket stitched "OSTREL" and a wristband with "Her own name, printed backwards" (sc11): the institution names her, and the name does not fit. A white pressure suit on which "Every word printed on it reads backwards to her" (sc18): contained and labeled by the world. The vessel strapped to her chest (sc25 to sc28): she now carries a person. A clear plastic tent (sc29). Makeup: the chipped front tooth (sc02: when the rung rolls, "Her jaw shuts on the torch", and she "finds a new edge") in every later close shot of her mouth; the palm (M03).
- **Eli.** "a beard she has never seen" (captivity), one wrist strapped, a coat, one shoe ("She gives Eli one shoe. He leaves the other."; "One shoe." later sits in the collection room). Paper oversuit (sc28). Performance and makeup: "the crooked half-smile" must be established on one side in sc03 so it can appear "on the wrong side of his face" in sc28.
- **Jude.** "easy in the shoulders", then shot through the shoulder; field dressing (the sleeve); Saye's dressing; "A fresh dressing on his shoulder, neater than the last" (the figure's work, sc17); arm strapped across his chest (sc29). His ring must be established as worn on his left hand, or its reversal in sc29 cannot be seen.
- **Saye.** "grey and tidy, fully dressed at four in the morning": she has been waiting for them tonight (Eli: "She's expecting me."); whether her readiness is older than tonight is interpretation, and the costume should not insist on it. Later a protective hood. She never takes off her control.
- **Nell.** In the file photograph "A flight suit. Unsmiling." On the ship, thin wrists, a book held against her chest. A paper oversuit; she holds the wheelchair's back "but does not sit".
- **The figure.** Tall, flat black, "Its head sits low between its shoulders", with a pale strip where a face would be. It is a costume in the literal sense: "A suit." Plant the latches down its front at emphasis level 0 in sc15, sc16 and sc20 (B5's clue ledger, Section 6.4) so that "Latches let go, one after another, down the front of it" (sc25) is fair. Its damage states (cracked cover, patch, cell removed, chest open, empty) are B5's S0 to S5 (Section 10.9); the register entry is M17.
- **An optional rhyme (interpretation, flag to the user).** Iona's white pressure suit and the figure's black suit are the same kind of object: a hard shell that keeps a living thing alive inside ("This keeps air round you."). Designing both with a shared construction language (hard shell, front closures, a chest-mounted life-support unit) makes the reveal land as recognition: the monster was a person in a suit, like her.

---

## 7. Translation table: story meaning to things

**How to use this table.** It is a list of questions, not a lookup. Each row was abstracted from *The Catch* or *The Long Places*, and the generic form of almost every row is a known cliché: the lone houseplant in an empty flat, hands on glass, a wall of tally marks, an empty chair. Use a row only to ask "what is *this* story's version of that?", then answer from the harvest (Section 3.1, step 3). **Rule:** if the thing you end up with would fit any film with the same meaning, it is stock; go back to the text for a named object with a specific detail (not "a plant" but "A pot of mint on the windowsill, and that is all"; not "a tally wall" but "one line, low, beside all the other lines").

| Story meaning | Set | Prop | Costume or makeup | Framing note |
|---|---|---|---|---|
| A character's life is on hold after a loss | Bare room, nothing personal | One kept living thing | Dressed too early or too formally | Keep it wide and still; let absence register |
| A secret decision | Hands or objects out of sight | An empty holder where something was | A pocket, a closed hand | Frame the absence (empty clip) at level 2, not the secret |
| Guilt about something made | Work objects kept close | The made thing, carried everywhere | Nothing new; the character will not change until it is gone | Carry it at level 0 to 1; the payoff is its loss |
| Habit, skill, body memory | Surfaces worn by use | Tools the hand knows | Wear on the working side | Repeat the plant's composition at the payoff |
| Habit betrayed | A familiar thing that fails | Broken piece of routine equipment | A new mark from the failure (chipped tooth) | Keep the failure fast and unornamented |
| Estrangement, no longer fitting | Mirror-reversed signs; food that is wrong | Labels, letters, rings on the wrong hand | Borrowed clothes, labels that read wrong | Let the character notice, not the camera |
| Love under containment | The story's own barrier (in *The Catch*, glass partitions it has used from sc03) | Transfer drawers; chairs | Hands bare to the barrier only if the story has earned it (rule 24) | Symmetric two-shot at the glass, long lens (B1); no fog, no tears, no score swell |
| Care | Order, tidiness, repair | Tape, dressings, a cloth slid under something | Bandages done well | Let hands work in real time |
| Being treated as goods | Shelves, containers, labels | Tags, load limits, numbers | Wristbands, printed names, uniform oversuits | Frame people among objects at the same size |
| A person inside goods (the hinge) | A body that opens | Vessel, heart, pump | A suit with latches | The reveal as an opening, not a transformation |
| Rule-following as devotion (*The Long Places*) | Worn thresholds, sooted niches | A measured amount (oil to the knuckle) | Hands shaped by the work | Macro insert repeated with different hands |
| Time kept by acts, not numbers | A wall of tallies | A small knife; one new line | None | The new mark small among thousands |
| Permission from outside against duty from inside | Offices versus the place itself | A permit against an oil can | Formal clothes against work clothes | Show which object the character carries at the end |

---

## 8. Decision rules

**Choosing motifs**

1. **If** a thing appears at two or more turning points and scores 5 or 6 on the tests in Section 3.3, **then** rank it spine, subject to the per-channel caps in Section 3.2 and the tie-breaks in Section 3.3; if it appears at two or more turning points but scores 3 or 4, rank it supporting, **because** it already sits where the story changes, but only a thing that also changes state and is handled can carry a spine.
2. **If** a thing crosses from one pole of the core opposition to the other, **then** mark it a hinge; if there are several hinges, give the largest single payoff to the hinge whose change falls closest to the climax, **because** its change is the theme happening physically. "Largest" is measurable: of all the film's emphasis-3 moments it gets the longest held frame and the strongest contrast in one visual component (Section 2.10), still with no more added signals than rule 23 allows.
3. **If** the text names more spine candidates than the length can carry, **then** merge motifs that share a payoff (glass and rings), and demote the rest to supporting, **because** motifs that peak in the same beat cancel each other.
4. **If** you are tempted to add a symbol the text does not contain, **then** first look for an existing object that could carry the meaning by a change of state, **because** borrowed symbols read as the author's hand.
5. **If** an object's meaning comes from general culture (doves, clocks, crosses, caged birds), **then** avoid it unless the story rebuilds its meaning from scratch, **because** outside meanings arrive pre-labeled and feel heavy.

**Framing**

6. **If** it is a plant, **then** keep emphasis at 0 or 1 and show the object clearly in context, **because** the audience must be able to recognize it later without being told it matters. **Exception:** if the plant is itself a plot event (the rung turns, the palm is skinned, the tag is read aloud, Saye teaches the F), use the level the event needs, at most 2, and add nothing that points past the present beat (no held pause, no extra light, no sound cue).
7. **If** the payoff depends on the audience knowing how a thing works, **then** give one level-2 teaching shot before it, **because** suspense needs knowledge.
8. **If** a character's body remembers something (the sill), **then** pay it off by repeating the plant's composition exactly, **because** the audience should recognize the moment at the same instant as the body.
9. **If** the meaning is an absence (an empty clip, a missing chair), **then** frame the holder where the thing should be, with a character's look leading to it, **because** absence cannot be seen without a frame for it.
10. **If** a non-speaking character must understand something, **then** build an eyeline chain (character, object, second object), **because** the Kuleshov principle lets the audience read the thought from the sequence.
11. **If** two spine motifs appear in the same shot, **then** give only one of them emphasis above 1, **because** two loud objects split the eye.

**States and continuity**

12. **If** a motif appears again, **then** change at least one of: its state, its owner, its neighbor in the frame, or what the audience knows, **because** unchanged repetition becomes wallpaper.
13. **If** a detail has a side (rings, wounds, torn sleeves, smiles), **then** record the side in the state table and in C2's mirror-state tag for every scene, **because** models and editors flip sides easily, and in *The Catch* sides are plot.
14. **If** a character is damaged more than once and the text does not fix the sides, **then** put all the damage on one side, record it as a recommendation for the user (Section 15), and keep the other side clean, **because** the clean side stays free for an emblem.
15. **If** an object is destroyed, **then** show its last state clearly before the destruction, **because** the audience must know what is being lost.
16. **If** an object returns after a long gap, **then** keep its look identical except for the one intended state change, **because** recognition depends on sameness.

**Sets and costume**

17. **If** a set is a character's mind or history, **then** decide its loudness first (Section 4.1) and keep the other sets quieter: at most two loud sets in a short film, three in a feature, **because** a film can only have a few loud rooms.
18. **If** two institutions in the story are morally paired, **then** rhyme their architecture, **because** the audience will feel the equivalence before any character states it.
19. **If** a costume changes, **then** tie the change to a turning point or a forced circumstance, **because** unmotivated changes read as fashion, not story.
20. **If** a character's reveal is that they are not what they seemed, **then** plant the mechanism of the reveal (latches, seams) at emphasis 0, **because** a fair reveal needs evidence the audience could have seen.

**Restraint**

21. **If** a line of dialogue states what an object means or why it matters (sc13: "That flask was proof of the trial they said didn't exist."), **then** keep the object at emphasis 0 or 1 during that line, **because** saying and showing at full volume together is heavy-handed. Reading a label or sign aloud, or naming an object, is not stating its meaning: that case is governed by the plant exception (rule 6), as when Jude reads the tag in sc01.
22. **If** a character explains a metaphor, **then** make sure the explanation has a practical purpose in the scene (Saye teaching the physics), **because** a character explaining a symbol for the audience's benefit is the author speaking.
23. **If** a beat is a level-3 payoff or reveal, **then** sort what points at the object into three kinds and apply the limits: (a) **script markers**, which come from the text and are never removed: a state change on screen, a line of dialogue about the thing, a character's look or touch; (b) **framing**, which is how the pipeline reaches level 3: size, a held frame, a rhyme of the plant's composition; (c) **added signals**, which the pipeline may add: a music cue or sting, a light change, a sound change, slow motion, or a camera move toward the object that nothing in the scene motivates (a move that follows a character's walk or search is staging, not a signal). If the beat has any script marker, add no signal from (c); if it has none, add at most one. **Because** stacking signals on one object makes it melodramatic, and the text's own marker is always the strongest. (Worked example 11.1: the palm dragging on the sill is the script marker, the rhyme is the framing, and nothing is added.)
24. **If** the image is a well-known cliché (hands on glass, the lone lit window, an empty chair), **then** keep it only if all three hold: the text names it, it has a practical job in the scene, and it changes state or meaning between appearances; then play it plainly (no slow motion, no score swell, no push-in), **because** only the story's specifics can rescue a familiar image.
25. **If** the thing you chose would fit any film with the same theme (a wilting plant for grief, a ticking clock for time running out, a caged bird for a trapped life, rain for sadness), **then** it is stock: replace it with a thing only this story has, described with a detail taken from the text, **because** specificity is what separates a motif from a cliché.
26. **If** a motif has already been paid off, **then** keep every later appearance at emphasis 0 or 1, and design at most one of them as a coda, **because** a loud return after the payoff explains it a second time. **Exception:** if a later appearance carries plot information the audience must read (a display, a readout, a label that decides the next action), frame it at the level legibility needs, up to 2, but add no rhyme, held beat or signal that recalls the payoff.
27. **If** a beat's inner state has no thing carrying it and the text offers none, **then** prefer, in this order: an action with an object already in the scene; the actor's face and body alone; and only last a new object, which must have a practical job, be placed at emphasis 0 in an earlier scene, and be flagged as an invention, **because** an invented symbol arriving exactly when it is needed reads as the author's hand.

---

## 9. Motif register: *The Catch*

Scene numbers follow the script's headings in order (sc01 loading tunnel to sc30 the final night), matching A2, B1, B2 and C2.

### 9.1 Theme, poles and hinges

- **Theme question:** when you carry someone, do you carry them as goods (weighed, decided for, sealed away) or as a person (asked, told, touched)?
- **Core opposition:** GOODS against PERSONS. Secondary: FIT against TURNED.
- **GOODS side:** the red tag, engine ratings and charge bars, the puck, the flask, sealed containers, labels, wristbands.
- **PERSONS side:** hands (on glass, under an arm "As carefully as a nurse"), the practised lift, the sleeve pressed into a wound, a cup moved into someone's reach, the question asked twice.
- **Shape and material families (Section 3.1, step 8; an interpretation drawn from the harvest, flag it to the user):** GOODS = grids (the cage floor and roof "the same open steel grid", the floor the puck is clipped to), rectangles and boxes (cabinets, the grey box, sealed containers, the courier pod), printed labels, hard flat-black shells (engines, cells, the figure). PERSONS = hands, cloth (the sleeve, the blanket, the cloth Saye catches the carriage in, the cloth under the vessel), curved clear glass and water. Hinges mix the two: the vessel is a hard mount and pump holding curved glass and water; the container holding the sleeve is a sealed box whose curve reflects the figure.
- **Hinges:** the figure (it shelves people like goods, and is itself a person inside a suit; M17); the sleeve and copied name (filed like goods, kept like a person); the visor outlines (a load display that finally carries a person). The story resolves its theme when the goods side is used to carry a person: "two outlines turn green, one inside the other." Rule 2 gives the film's largest single payoff to the hinge whose change falls closest to the climax: the figure's chest opening in sc25.
- **Ranks.** Spine: M01 load limit, M02 rung and sill, M03 palm, M05 flask and puck, M10 pump (sound), M11 sleeve and name, M13 glass with M07 rings as its payoff. Supporting: M04 yellow stripe, M06 letters and F, M09 needle, M12 drawings, M14 the question, M16 the cup moved into reach. Single-scene: M08 mint. Minor props, one line each, never above L2: M15. Character hinge (tracked, not counted): M17 the figure. Counted per channel (Section 3.2): visual spine M01, M02, M05, M11, M13 (with M07 merged in) = five, the top of the short-film range; body channel M03; sound channel M10. There is no room for another visual spine motif, so any new candidate must displace one or go to supporting. M17, the figure, is a character (designed in B5), not an object motif, so it is tracked here for its evidence and its reveal but not counted against the cap.
- **Emphasis-3 map (check against Section 3.1, step 9):** sc06 M02 (sill, by rhyme); sc13 M05 (puck on the recording); sc16 M09 (needle); sc21 M11 (the copied name, the hinge's reveal); sc23 M12 (the drawing); sc24 M05 (flask); sc25 M17 (the chest opens: the film's largest payoff) and, on a later and different turning point with the tape repair and the lifting of the vessel between them, M01 (two outlines green); sc26 M06 (the F for the animal); sc29 M07 (rings). sc25 is the only scene with two, which Section 3.1, step 9 allows. Sound: M10 reaches S3 once, in the last seconds of sc30. M05 has two L3 moments (puck, flask) because it is two objects carrying two different decisions; for the per-motif L3 budget (not for the spine count), treat the flask and the puck as two motifs. Every other motif has at most one; supporting motifs M04, M14 and M16 have none.

### 9.2 Entry format

Each entry gives: **Meaning** (one line) and its direction of travel; **Plant**, **Develop**, **Reveal** (hinges only), **Payoff** with scene, exact line, and emphasis level (L0 to L3 for things seen, S0 to S3 for sounds); **States**; **Framing and rules**. Every quoted line must be copied verbatim from the script and checked against the scene it is attributed to.

### 9.3 Entries

**M01. The load limit: the red tag, "Goods only. No persons."** Spine; GOODS pole; its payoff is a hinge.
- **Meaning:** what a thing is rated to carry, and the rule that people are not goods. Direction: a rule broken, then its cost, then a way to carry a person inside the limit.
- **Plant, sc01:** "A red tag is wired to the gate." Jude "turns the tag to the light and reads it": "Goods only. No persons." L2 by the plant exception (Section 3.4): it is a plot event, the rule read aloud. Medium close on his hand turning the tag into Iona's beam; the red must read, the lettering need not, because he speaks it (rule 21). If an insert of the lettering is used at all, use one plain insert and never repeat it. Then "Hooks the tag back on the gate." L1: they put the rule back and break it anyway.
- **Develop, sc06:** "Eli reads the tag on the wire. He reads everything." / "Io. This says-" / "We know. Get in." L1, over Eli's shoulder; no second insert. At the fall: "Its red tag whips against the upside-down gate." L1 to L2 in the wide: the rule, upside down, going away.
- **Develop (the limit returns as numbers and displays):** sc12 "The small ones manage a tray. The two big ones are for moving people"; sc13 "What was it rated for?" / "One body." / "One." / "You."; sc18 teaching shot for the display language (rule 7): "On Iona's wrist, a simple display: her outline, the engine, a bar of charge." L2, one clean frame of the graphic before she tries the controls; sc23 the shell light "turns RED", then "GREEN" once the bed's legs and panel are torn off, L2; "Can you take two?" / "No." L1 (she "checks the load on her visor"; keep the graphic small); sc25 "Two outlines. Hers green. Its own red." L2.
- **After the payoff (rule 26 and its exception):** sc26 "Her projected outline turns red: far below the receiving room. Below the loading tunnel. Inside solid rock." (the path, not the load, but the same red logic) and sc27 "The whole outline clears the hull's last projection. Turns green." Both are readouts the plot needs, so frame them at L1, or L2 where the audience must read where the outline sits (the red outline inside rock), but never rhyme the sc25 visor frame or hold on them. Same graphic style as sc18 so the audience reads them without new teaching.
- **Payoff, sc25:** "On her visor: two outlines turn green, one inside the other. A little to spare." L3 (hold the visor graphic; the green change is the script's own marker, so nothing is added, rule 23). She carries a person by leaving the goods, the suit's body, behind: "It weighs no more than a bag of shopping."
- **States:** wired shut, unwound, rehung, read, whipping on the upside-down gate. The script does not mention the tag on the wreck in sc21; if it is visible there, keep it at L0.
- **Framing and rules:** the tag is the only saturated red in sc01 (B2). All later limits are displays using the same red and green logic, so the audience links them by color and by the word "rated", not by cutting back to the tag. Never cut back to the tag for irony.

**M02. The rung and the sill.** Spine; a pair: habit betrayed and habit rewarded.
- **Meaning:** the body's memory. The rung is fifteen years of habit failing; the sill is a place worn by other people's bodies, which her body learns once and trusts at the decisive moment.
- **Plant (rung), sc02:** "Her hand closes on a rung and the rung TURNS." Then "Her foot comes up after her, the way it has come up after her for fifteen years, and sets itself on the broken rung." L2 (it is action). Result: the chipped tooth. Lesson: "Now each foot goes only where a hand has already been."
- **Plant (sill), sc02:** "Its steel sill has been worn bright by other people's sleeves." / "She hooks an arm over the sill. Rests her face against the brick. Her arm settles into the shape of the steel." L1: side-on medium close, her torch raking across the polished band.
- **Develop, sc06:** "Through the grid under her boots: the ladder. The broken rung." L1, point of view through the floor grid. "Beyond the gate, the bright sill is almost level with the floor. A passage. A way out." L2: hope, then the fall.
- **Payoff, sc06:** "The sill comes down into reach." / "Her arm knows it before she does." / "She catches it. Her palm drags across the bright steel." L3 by rhyme (worked example 11.1).
- **Later:** sc18 "Through the tall opening with the bright sill: the dark of the shaft." L0 to L1.
- **States:** the sill never changes (it is the constant); the rung goes from whole to hanging in one bracket.
- **Rules:** do not return to the rung after sc06. The sill's polished band must be identical in every shot: same width, same height, same shine.

**M03. The skinned palm.** Spine (makeup); PERSONS pole: the cost of saving all three.
- **Meaning:** what the catch cost her body; later, silent evidence in her argument with Eli.
- **Plant, sc06:** the palm dragged across the steel. L2 (the injury happens in action).
- **Develop:** sc09 "She holds the wheel so hard her skinned palm opens." L2, inside the driving coverage: a close shot of both hands gripping the wheel, whose subject is the wheel on the wrong side (M06), with blood opening in the right palm as one detail of it. It is not an insert composed on the palm alone, so the palm keeps only one insert of its own (sc13) and stays in the body channel (Section 3.2). sc11 "A NURSE works through the sealed gloves of a service hatch, dressing Iona's palm." L1. sc11 "Iona raises her bandaged hand back." L1.
- **Payoff, sc13:** "She looks down at her palm, where the sill took the skin off." / "He watches her look at it." L2, not L3: her look, the palm, then his look at her looking, with no push-in. The scene's L3 has already gone to the puck on the recording, and a body mark this close to it should not compete; Eli watching her is what makes it land. It comes straight after Eli's "You'd have come up out of that shaft on your own, Io." and her silence ("She opens her mouth. Nothing in it."): the palm, the mark of the catch that brought all three out, is what she looks at instead of answering.
- **Close, sc30:** "Iona sits on the bed with her bandaged hand in her lap." L1.
- **States:** intact; raw (sc06); reopened and bleeding (sc09); dressed (sc11); bandaged (sc11 onward, hidden inside the suit glove in sc18 to sc28); bandaged, at rest (sc30).
- **Side:** recommended right hand (Section 6.2). Per C2, Iona never flips, so it stays on her right in every era.

**M04. The yellow stripe.** Supporting; "the line" (B2).
- **Meaning:** where the fall ends, and later the threshold she chooses.
- **Plant, sc02:** "A band of yellow paint circles the whole shaft at head height. She passes it." L0 to L1: the torch passes over it without stopping.
- **Develop, sc06:** "Through the grid, the yellow stripe. Coming." L2, through the grid, growing. After the turn: "The yellow stripe is under her boots, getting smaller." L2, the same shot reversed.
- **Payoff, sc18:** "A yellow line painted across the floor." / "Iona steps onto the yellow line." L1 to L2: a medium-wide in which the line runs across the whole floor and her boots are in frame as she steps onto it in the flow of the action. This time the line is her choice. No low insert of a boot crossing a line: that is the stock "threshold" shot, and the beat's weight belongs to what follows ("Saye catches her elbow.").
- **Rules:** painted only, never a light (B2). Same yellow and the same width in shaft and floor so they read as one thing.

**M05. The flask and the puck.** Spine; Eli's emblem; GOODS pole, resolved on the PERSONS side when Iona decides.
- **Meaning:** the flask is Eli's work and guilt, an ordinary coffee flask holding a danger. The puck is his secret decision for all of them. Direction: the flask passes from his hand to the institution, to the collector, to the fire, and the decision about it passes from him to Iona. The puck goes from hidden, to absent, to revealed, to a scar.
- **Plant, sc04:** "Inside: a small steel FLASK, the kind that keeps coffee hot. A flat black PUCK clipped underneath it." L1 to L2 through the broken window; the puck must read as a separate black disc. sc05: "Takes the flask and its puck." L1.
- **Develop (hidden), sc06:** "His other hand goes underneath. Behind Jude's back. Out of sight." and "He has one hand she cannot see." L1: the cue is the hand leaving the frame, not the puck.
- **Develop (absence), sc07:** "The flask is in his fist." / "The clip under it is empty." / "Iona sees the empty clip." L2 (worked example 11.2).
- **Develop (the unsaid answer):** sc09 "He looks down at the flask in his hand for a long time." L2 as a medium close on Eli looking down, the flask in his hands in frame; not an insert of the flask (its only loud moment is sc24). sc10 Saye looks "for a long moment, at the flask"; "Don't open the flask." L1 to L2. sc13 "Saye sets the flask beside the monitor." / "That flask was proof of the trial they said didn't exist." / "Saye puts it in a sealed carrier."
- **Payoff (puck), sc13:** on the recording, "Eli's hand comes out from behind Jude's back." / "Empty." / "a flat black puck is clipped to the grid." L3, held on the paused surveillance frame, not zoomed (worked example 11.2). By the time the recording runs, Saye has put the real flask "in a sealed carrier"; if the carrier is in any shot of the recording, keep it at L0 (rule 11).
- **Coda (puck), sc21:** "The puck is still there, burnt into the grid where it was clipped. A black blister on the steel." L1, the puck's one coda (rule 26): place the blister on a strong point of the wide of the wreck, sharp, with no insert, because its payoff was spent in sc13. "Her brother's flask." in the cabinet, L1 (a develop for the flask, which has not yet paid off).
- **Payoff (flask), sc24:** "She looks at the flask inside the outline. Leaves it there." L3 (the visor outline includes it; her look is the decision). The one marker is the outline drawn round the ordinary flask among the burning shelves; no music hit, no slow motion (rule 23). Then "Cabinet, canister, flask and engine vanish together."
- **Coda, sc29:** "Saye says the flask's gone." / "I sent it with the fire." / "Good." Nothing in Eli's hands; the absence is the image.
- **States:** flask: locked in the cabinet, in Eli's fist, in his hand in the car, on Saye's counter, beside the monitor, in a sealed carrier, taken by the figure off screen (reported in sc17: "Tonight, the flask."), in the collector's cabinet, gone. Puck: clipped under the flask, in Eli's hidden hand, clipped to the grid, revealed, burnt.
- **Rules:** the flask stays ordinary: no glow, no hum, no hero lighting. Keep Eli's hands visible whenever he holds it, except in sc06, when one hand must leave the frame.

**M06. Backwards letters and the F.** Supporting; FIT against TURNED; the story's world logic.
- **Meaning:** the world's verdict on whether you belong. The F is orientation made visible, and becomes a language.
- **Plant, sc07:** "Every letter is backwards." L2: one stencil, her look. After that, the exit sign (sc07), the car (sc08), the bus number (sc09), the blanket "OSTREL" and the wristband (sc11) sit at L0 to L1. The audience learns the rule once; do not insert every sign.
- **Develop, sc12 (teaching):** "a toy carriage marked F"; "Comes back going UP. Its F is backwards."; "The F faces the right way."; the paper F that "stays an F" until "She lifts it and turns it over. A backwards F." L2. "Iona puts her palm against the glass, beside the restored F." / "Do that to us." L2. The sealed meal: "The letters face the right way. She reads it again." L1 to L2.
- **Payoff 1, sc26:** "She turns the wrist screen towards the vessel. Plays the carriage once. Its F reverses." / "The animal touches the moving picture through the glass." L3. The teaching model becomes the way to ask a non-speaking being for consent: a GOODS-to-PERSONS hinge.
- **Payoff 2, sc28:** "On the wall above Saye: RECEIVING." / "Iona looks at it. Reads it again." L2: the word reads right; she is back. Coda, sc29: "The labels run opposite ways." L1.
- **Rules:** decide the F's mirror state first (C2, Section 7.4, item 1). Readable text only in teaching and payoff shots.

**M07. Rings on opposite hands.** Spine, merged into M13 at the payoff.
- **Meaning:** the vow persisting across a division that cannot be touched; the reversal made personal.
- **Plant, sc10:** "They stand facing each other across the table like a woman and her reflection, each with the wrong hand in the air." / "Saye's wedding ring. On her right hand." / "Iona looks down at her own ring, on her own left hand." L2: a stranger's ring teaches the rule.
- **Payoff, sc29:** "Lays his good hand flat on it. His wedding ring. On his right hand." / "She lifts her own left hand and lays it against his, through the glass. The two rings sit directly across from each other, like a ring and its reflection." L3 (B1 Example 6: symmetric profile two-shot, rings meeting on the center line).
- **States:** Iona's ring always on her own left hand. Jude's ring designed on his left; it reads as right in the final era (C2).
- **Rules:** show Jude's ring on his left hand at L0 in sc01, so there is something to reverse. Keep Iona's left hand free of injury and dressing.

**M08. The mint leaf.** Single-scene prop; FIT test.
- **Meaning:** the body's verdict (taste) arriving before the mind accepts it; also the one kept living thing in a life on hold.
- **Plant, sc10:** "A pot of mint on the windowsill, and that is all." L1 in the kitchen wide: placed, not inserted.
- **Payoff, sc10:** "She goes to the windowsill, tears a leaf from the pot of mint, and holds it out." / "Chew that." / "Her face changes." / "Not mint." L2: the tearing in medium shot, then Iona's face, not the leaf, carries the payoff.
- **Rules:** no insert of the pot before it is used. Its green is the one inversion of green-as-fit (B2).

**M09. The grey box with a needle.** Supporting; a rule, then a warning.
- **Meaning:** the sign of the invisible: something has crossed.
- **Plant, sc11:** "Above the bed, a grey box with a needle in it. The needle lies flat." L1.
- **Teach, sc12:** "On the wall behind them, a grey box with a needle, like the one over Iona's bed." / "It vanishes before the wood. The needle on the wall kicks." L2: vanish and kick in one frame, or cut on the kick.
- **Develop, sc14:** "Over her bed, the grey box. The needle lies flat." L1: the audience now knows what flat means.
- **Payoff, sc16:** "Above her, the needle moves." / "The needle climbs. The room is empty. She can see every corner of it." / "The needle goes on climbing." L3: alternate the needle and the empty room.
- **Close, sc29:** "The grey box on the wall, its needle quiet." L1: peace is a needle that does not move.
- **Rules:** one box design in every room; the needle must read in a medium shot.

**M10. The pump: "Three uneven strokes".** Spine; leitmotif; sound.
- **Meaning:** the figure's presence, then the heart of the person inside it, then a life Iona carries.
- **Plant, sc15:** "From inside it, a PUMP: three strokes, not quite even." Heard over the tablet image. S1, with the small, thin quality of a tablet speaker.
- **Develop, sc16:** "Behind her: a pump. Three uneven strokes." The sound arrives before the figure; she turns. S2, full-range and close, behind her in the room: the same sound, now in her space.
- **Reveal, sc25:** "The pump she heard in the dark of her room: the only heart the big body has." Seen for the first time. S1: the image carries the reveal; do not raise the sound to point at it.
- **Develop, sc27:** "Breath in the helmet. Three uneven strokes against her chest." S2, close in the helmet mix, sharing it only with her breath.
- **Develop, sc28:** "The little pump keeps working. Three uneven strokes." S1, under the voices in the receiving room.
- **Payoff, sc30:** "Each stroke of the pump makes the base of the vessel tap against the metal table." S2 with the tap. She slides a folded cloth beneath it. "The tapping stops." / "The pump goes on." / "Three uneven strokes in the dark." S3 over black: the only S3 of the film and its last sound.
- **Rules:** one recorded sound for every appearance, same rhythm and timbre; only the mix (distance, room) changes. The meaning changes because the audience's knowledge changes, not the sound. Never put score over it.

**M11. The sleeve and the copied name "IONA VALE".** Spine; the central hinge.
- **Meaning:** Iona's act of care, her own sleeve for Jude's wound, is the thing the collector keeps, labels and finally tends. The label files her like goods; the keeping treats her as a person.
- **Plant (costume):** the blue shirt from sc01, L0.
- **Plant (act), sc07:** "pressing what is left of her shirt sleeve into Jude's shoulder." L2. sc09: "holding the sleeve on him". L1.
- **Plant (name), sc11:** "Her own name, printed backwards." The wristband, L2.
- **Reveal, sc21:** "a strip of blue cloth. The sleeve of her shirt, stiff with Jude's blood." / "Above it, a label. Her name, copied from a hospital wristband stroke for stroke, the way you would copy a drawing. By someone who did not know they were letters." / "IONA VALE." / "Behind the cloth, something cloudy moves." L3, the motif's only L3: this is the hinge's reveal (worked example 11.4).
- **Develop, sc25:** in the open chest, "the container with the strip of her shirt in it. Her name." The animal "keeps the limb against the glass." / "She clips the container to the vessel." / "The outlines stay green. Just." L2: the animal asks, she carries it. Not L3, because the scene's L3 on this turning point belongs to M01's two outlines a few lines earlier; the container rides on that graphic ("stay green. Just.") rather than getting its own insert.
- **Payoff, sc30:** "The cloudy growth behind the scrap of shirt fills half the container now." / "The label still carries the marks copied from Iona's wristband." The animal "draws the container close against its own glass." L2: care shown without explanation. A quiet payoff by design (Section 3.4): the audience already knows what the container is, so volume would only explain it again.
- **States:** whole sleeve; torn and pressed into a wound; held on the wound by Eli in the car; off screen, probably taken with "Jude's dressings, from a sealed bin" (sc17; an inference, the script does not say where the sleeve went); stiff with dried blood in a sealed container under a copied label; in the chest drawer; clipped to the vessel; growth filling half the container.
- **Rules:** the label must look drawn rather than printed: shapes copied with even, careful strokes. Mirror state of the label: C2, Section 7.4, item 3.

**M12. Nell's drawings.** Supporting; home, and the only shared language.
- **Meaning:** the wish for outside; the figure reads it and understands "home".
- **Plant, sc20:** "a stack of drawings" on Nell's shelf, L0. "Nell turns over a drawing beside her bowl. A window, a tree, a small house. Beneath it, another drawing: the same tree, a much larger room around the bed." L2. "It brings what I draw, if it can find it. It won't open the door." / "She props the drawing of the house against her bowl." L1: the drawing now faces the room.
- **Payoff, sc23:** "Then it turns its head to Nell's shelf. To the drawing propped against the bowl: a window, a tree, a small house." / "It looks back at the green line on her visor." L3 (worked example 11.3).
- **Coda, sc28:** "Is there a window in my room?" / "There is. You can see the street." The drawn window becomes a real one, in words.
- **Rules:** simple lines on paper; one house shape recognizable at medium size.

**M13. Glass and hands on glass.** Spine; love under containment.
- **Meaning:** separation that can be seen through; contact without touch. Direction: breaking glass, then reaching across it, then accepting it.
- **Plant, sc03:** "He looks up. Sees her through the glass." / "The glass cracks corner to corner and holds." / "She hits it again." L2: Iona breaks barriers.
- **Develop:** sc11 "Through another window, Eli raises a hand. Iona raises her bandaged hand back." L1 to L2, hands apart. sc12 "Iona puts her palm against the glass, beside the restored F." L2, a plea. sc17 "Iona puts her hand flat on the glass, as near to the monitor as she can get." L2. sc20 the ship's glass rooms and drawers. sc23 "Eli looks through the wall at his sister." L1. sc25 "The animal presses a limb to its window." L2: another being makes her gesture.
- **Payoff, sc29:** the rings (M07) at L3, then "She brings her chair closer to the glass. He moves his to meet it." L1: the grace note after the payoff.
- **Rules:** no breath fog, no tears on the glass, no slow push-in with music at the payoff; the rings carry it. Keep the glass clean so the hands are the subject, but never invisible: let it read by one thin frame edge or a faint reflection, or the audience will think the hands touch and the payoff (contact without touch) is lost. No smears, no glare across the hands.

**M14. "Are we going to be all right?"** Supporting; a dialogue motif carried by objects and surfaces.
- **Meaning:** the family's central question, first met with evasion, then with an honest answer.
- **sc09:** "A red light. Iona finds his eyes in the mirror." / "Eli. Are we going to be all right?" / "He looks down at the flask in his hand for a long time." / "Drive." Framed through the rear-view mirror, a surface that reverses; the flask is the answer he withholds.
- **sc23:** "Eli looks through the wall at his sister. She has not reached for her way home. She is looking at the door to the collection room." / "Are we going to be all right?" / "I don't know." Framed through glass, a surface that does not reverse; she is looking toward the room where the flask is.
- **Coda, sc29:** "In the car-" / "Yes."
- **Echo (Nell's questions):** sc20 "Is it safe to go home?" is met with an evasion, Iona's "They're making a room." after she looks "At how thin the woman's wrists are". sc28 "Is there a window in my room?" is met with a plain answer, "There is. You can see the street." / "Will you take me?" / "Yes, Nell." The same pattern (evasion, then honesty) in a second relationship. Do not frame it to rhyme with the car; the words carry it. Keep the drawing (M12) out of the sc28 frame, so the echo is not underlined.
- **Rules:** the rhyme is mirror then glass, the flask then the flask's room. Play both plainly; the reversal of who asks does the work.

**M15. Minor props, one line each.**
- **One shoe:** sc04 "He leaves the other."; sc21 "One shoe." among the collected things, L0: the collector keeps even this.
- **The bread roll:** sc12 "Not that one."; sc29 "Iona breaks a bread roll. Moves half towards the transfer drawer. Sees the label on his tray. Stops." L2: a gift made impossible by fit.
- **The water bottle cap:** sc10 "It will not give. He stops. Twists it the other way." L1: Eli already understands.
- **The repair tape:** sc18 "Only one of them can be mended with tape."; sc25 "She takes the roll of repair tape from her suit and seals it." Plant L1, payoff L2.
- **The cloth:** sc12 Saye "catches it in a cloth"; sc30 Iona folds a clean cloth and slides it under the vessel. A quiet rhyme of care, L1 each.
- **The remote:** sc13, power passing between hands (Section 5.4).
- **Chairs:** sc03 a chair jammed under the stair-door handle (a chair as a barrier); sc15 "An empty chair beside the bed." / "The chair is still there." (the vigil chair nobody sits in, left behind when the bed is taken); sc29 "A chair on each side of the glass" and "She brings her chair closer to the glass. He moves his to meet it." L0 to L1 each. Never give the empty chair in sc15 an insert: an empty chair is a stock image, and here it only has to be present.
- **The air tank:** sc20 the figure "carries a metal tank"; "Someone has cut a new fitting for it, by hand, to match the coupling on a human suit." L2 on the hand-cut fitting: the first proof, before any explanation, that the collector cares for what it keeps. "She lets go of the tool." is the payoff, on her hand, L1.

**M16. The cup moved into reach.** Supporting; PERSONS pole; the evidence that makes the figure's reveal fair.
- **Meaning:** care as small, practical attention. The figure's first act is the exact act Iona performed for Jude; the audience sees the rhyme before it knows what the figure is.
- **Plant, sc13:** "Iona moves his water into reach of his good hand." L1, in the background of the recording scene, at real speed, not cut to.
- **Develop, sc14:** "A second cooling cup of tea." L0: Iona's own vigil, untouched.
- **Payoff (of the rhyme), sc15:** "Jude reaches for his water. The cup is just past the fingers of his good hand. He gives up. Lies back." / "A small CLICK, from nowhere." / "The cup slides a hand's width across the table. Into his reach." L2: frame it as a rhyme of sc13 (the same cup, on the same side of the frame, his good hand in the same place), so the viewer's body recognizes Iona's gesture done by no one. Then "Jude grabs the cup before it tips." L1.
- **Coda, sc23:** "A loose cup creeps across a shelf. It catches the cup without looking." L1: the reflex of a carer, one beat before "it moves, and it is fast".
- **States:** out of reach; moved into reach by Iona; out of reach; moved into reach by no visible hand; grabbed; creeping on a tilting ship, caught.
- **Rules:** one plain hospital cup design in sc13 and sc15. The slide is short ("a hand's width"), at real speed, with no glow, shimmer or effect on the cup; the only signal is the CLICK before it. Rule 20 applies: this, like the latches, is fair evidence the audience could have read.

**M17. The figure's suit.** Character hinge (GOODS to PERSONS); tracked for its evidence and its reveal, not counted against the visual cap. Its look, damage states S0 to S5 and clue ledger are in B5 (Sections 6.4 and 10.9); this entry only places its appearances on the emphasis budget.
- **Meaning:** the thing that files people like goods is a small person carrying itself inside goods. Direction: threat, then keeper, then an empty shell.
- **Plant, sc15:** "Something tall and black stands beside his bed." The latches down its front at L0 (also sc16, sc20), seen only in rim light (glossary).
- **Develop:** sc16 the cracked cover and "A thin WHITE JET", L2 (action); sc20 "A patch covers part of the pale strip." L1, and the hand-cut air fitting (M15), L2; sc21 its reflection "In the curve of the container", inside M11's L3 frame, not a second L3; sc23 "The pale strip dims." when it gives up its own cell, L1; sc24 "braced against its burning cabinet", L1 to L2.
- **Reveal, sc25:** "Latches let go, one after another, down the front of it." / "The chest swings open." / "No flesh. No hollow in the shape of a person." L3, the film's largest single payoff (rule 2). Framing: a held frame in which the open chest, the mount and the vessel are the only sharp things. The script already marks the beat (the latches, the opening), so add nothing (rule 23): no music hit, no light pouring out of the chest, no burst of vapor, no slow motion; the latches release one after another at real speed. The pump (M10) stays at S1.
- **After:** "The empty black body leans back against the wall." L1, once; do not return to it.
- **Rules:** the reveal is an opening, not a transformation (Section 7). Never show the animal's body before sc25, not even as a shadow inside the cover; the pale strip itself is shown from sc15, as B5 designs it.

### 9.4 State table for *The Catch* (continuity record)

Sides marked "rec." are recommendations the user must confirm (Section 15). "Era" follows C2, Section 7.3.

| Item | sc01 to sc05 | sc06 (cage) | sc07 to sc10 | sc11 to sc17 | sc18 to sc27 | sc28 to sc30 |
|---|---|---|---|---|---|---|
| Iona's shirt | Blue, whole | Right sleeve torn on the sill (rec.) | Sleeve torn off, pressed to Jude's wound | Hospital blanket, wristband | White pressure suit | Suit, then quarantine clothes in a tent |
| Iona's palm (right, rec.) | Intact | Skinned | Reopened in the car | Dressed, bandaged | Bandaged, inside glove | Bandaged |
| Iona's tooth | Chipped from sc02 | Chipped | Chipped | Chipped | Chipped | Chipped |
| Iona's ring | Own left hand | Same | Same | Same | Under glove | Own left hand |
| Jude's shoulder (left or right: decide) | Unhurt | Shot | Sleeve pressed on; Saye's work | Dressed; "neater" dressing on the ship | Dressed | Dressing bleeds through paper; arm strapped |
| Jude's ring | His left hand, L0 | Same | Same | Same | Same | Reads as his right (era C) |
| Eli | Beard, strapped wrist, then coat and one shoe | Hidden hand | Flask in fist, one shoe | Quarantine | Ship rooms | Paper oversuit; smile on the wrong side |
| Flask and puck | Flask in cabinet, then Eli's hand; puck clipped under it | Puck clipped to grid (unseen) | Clip empty; flask in Eli's hand, then Saye's counter | Puck seen on recording; flask in sealed carrier, then taken by the figure off screen ("Tonight, the flask.", sc17) | Puck a burnt blister on the wreck; flask sent away "with the fire" | Both gone |

Prop states in full are in each register entry's **States** line; this table is for the quick per-scene check of costume and makeup. The figure's damage states are B5's S0 to S5 (Section 10.9).

Note for sc28 to sc30: Iona's own turn in sc27 returns her to the world's handedness while Eli and Jude stay turned, which is why the labels "run opposite ways" between her and Eli in sc29 and why Jude's ring reads as his right (C2, era C).

---

## 10. Motif register: *The Long Places* (brief)

*The Long Places* is prose, so its motifs are carried by narration and by the keepers' letters that open each chapter. A film version must make them physical. **Theme question:** can a thing be carried forward for ever by keeping it, rather than by measuring it? **Core opposition:** MEASURING (counts, permits, instruments, the year) against KEEPING (lamps, rounds, marks, the name of the room). Nilay's arc crosses from the first to the second.

**L1. The lamps.** Spine.
- **Meaning:** "First, the lamp is not a light." / "A lamp is an errand. Someone set it for you, and you will set it for someone." Keeping, passed hand to hand across time.
- **Plant, Chapter I:** Melek "lit nine lamps and not forty, in nine niches the villagers called the grandmothers' cupboards, and over each niche the ceiling was black, and the black had depth, layer under layer under layer". The soot above the niches is set dressing that is also an archive.
- **Develop:** 1999 (Chapter II), Nilay takes "the tin lamp from the niche at the mouth without asking"; in the dark, when the flame keeps lying down, "the third time it lay down she pinched it out with her nails"; in the morning it stands "cold, its wick folded black over — pinched, or folded; a spent flame folds a wick and a keeper pinches one". Nilay's first round "from the book" (Chapter XI). Yusuf's lamp in Derinkuyu, "the first thing he had ever kept that could not be viewed" (Chapter XII).
- **Payoff, Chapter XIV:** Emre "topped the lamp to the first knuckle of his thumb and no further"; "Keepers leave you the lamp."
- **Rules:** the lamps are small and low; their light never fills a room (B2 covers the light). The 1999 wick: show Nilay pinching the flame out in the dark, because the text does. What must stay open is the morning: whether the cold wick is still the one she pinched, or was relit by someone and burned down (which would mean someone was there). Show the morning wick already folded, in a plain insert at the same angle as the night pinch; never show anyone relighting or tending it after her.

**L2. Oil to "the first knuckle of the thumb".** Spine; the measure. Full treatment in worked example 11.5; the register lines are:
- **Meaning:** a rule kept by the body, not by an instrument; the same measure on a different hand is succession. Overfilling is fear. Direction: a rule heard, broken in fear, kept, then recognized.
- **Plant, Chapter I:** the letter's rule, "The oil goes to the first knuckle of the thumb and no further", and Melek's "knuckles like burl, a burn gone silver across the back of the right one". L2 macro insert of Melek's thumb at the lip of the lamp.
- **Develop:** 1999 (Chapter II), Nilay fills the tin lamp "past any knuckle, greedily, the way the frightened do", L2, the same insert with the oil over the knuckle; Melek's verdict later in Chapter II, "You filled it badly. Past the knuckle. The greedy or the frightened." (dialogue, no insert); Márton (Chapter IX) and Yusuf (Chapter XII), L0 to L1 in wider shots; Nilay's first round (Chapter XI), "her knuckle was not Melek's knuckle", L2, the insert steady at the knuckle.
- **Payoff, Chapter XIV:** Emre "topped the lamp to the first knuckle of his thumb and no further", then "You filled the lamp badly, that night," ... "Past the knuckle. The greedy or the frightened." L3: the same insert, then his line over it.
- **States:** oil at the knuckle; oil past it (1999 only).
- **Rules:** one composition for every insert (lens, angle, light, hand position); only the hand, the lamp and the oil level change.

**L3. The day's mark.** Spine.
- **Meaning:** time kept by acts, not numbers; the self held inside something long. "When the round is finished you cut the day's mark, one line, low, beside all the other lines, and you do not go looking for yours among them. The wall is long. Looking for yourself in something long is how people get lost."
- **Plant:** the lower wall's tally lines, "short carved strokes, one beside another, thousands", which Nilay has drawn in her notebooks for six years and privately calls "the grandmothers' minutes" (Chapter I), and item 51 in the 1924 survey: "Hand print, right, red ochre, above the first marks, lower wall." A prison-cell tally wall is a stock image; what makes this one specific is the rule (one line, low, never looking for yours), the length (thousands), and the ochre hand above the first marks.
- **Develop:** "The wall is not a diary. It is a handrail." Emre's newest cuts "pale at the low end".
- **Payoff, Chapter XIV:** "She wet her right hand in the bowl and set her palm on the stone above the first marks, beside the old print, which had always been hers". Coda: in Book Zero she "scored it once with the little knife from Melek's oilcloth, one line, low, the way the wall is cut".
- **Framing:** each new mark small among thousands; a wide that shows the wall's length before any close shot of a hand cutting. The two handprints side by side as one frame, "a thing and its shadow".

**L4. "Doors go down and rooms go along".** Spine; a rule for the whole set.
- **Meaning:** two kinds of depth that must never be confused: down is time and danger ("Kırk Oda ran four doors down"; sleep above the fourth door after rain); along is the count that will not close ("Along, the rooms went forty"; one morning "forty-one").
- **Set rules:** stage every door as a vertical transition (stairs, a descent, a camera tilt or crane down) and every room as a lateral one (tracking along a gallery). Never cut from a room to "under" a room. The gallery must exist in two states, forty openings and forty-one, and the state table must log which one each shot shows; the forty-first opening appears only where the text allows.
- **Wear:** the jamb-shaped hollow "worn, not cut"; thresholds polished by feet.

**L5. The permit.** Supporting, becoming a hinge by its replacement.
- **Meaning:** permission from outside to measure and dig, against the duty from inside to keep.
- **Plant, Chapter I:** Nilay arrives with "the permit folded in her inside pocket, where it went soft with her own heat", having come "with a permit to dig at it". Costume and prop together: carried against the body, softening.
- **Develop:** the annex, countersigned in person in Valletta; her refusal to let the night of 1999 become words "in a licensed capacity, with the Ministry's stamp drying on her".
- **Payoff:** the keepership sheet goes to Valletta "its date filled in", and the chapter's last image of her before its coda (October on the Şanlıurfa side, then the winter rendering) is of her carrying something else: she "walked up through the mulberries with the oil can for the evening's round".
- **Framing:** paper in offices and pockets at the start, the oil can in her hand at the end. The object she carries tells the audience which office she holds.

**L6. The red ribbon.** Spine; this file adds it because it is the novella's clearest plant and payoff.
- **Plant, 1999:** "She bought a roll of red ribbon at the bazaar and tied a strip to everything the looking had entered". On the door's iron she tied "a strip of the red so the way back would have a color in it"; in the morning "there was nothing. Wind, or anyone."
- **Payoff, Chapter XIV:** Emre lays on the mat "A strip of red ribbon. Bazaar red gone the color of brick dust, folded on its old creases". The letter she has not yet written says "and I did not cry until the ribbon."
- **Rules:** make the ribbon the only saturated red in the film's palette, bright in the 1999 scenes and faded to brick dust at its return. The fold creases must match between its last sight on the iron and its return. The text builds a color rhyme worth keeping exact: the returned ribbon is "the color of brick dust"; the 1924 phial of pigment from the handprint is "a red between brick dust and rust" (Chapter IV); the handprint itself is "red gone brown". Use one desaturated brick red for all three, so the faded ribbon, the ochre and the first hand read as one family, and keep the 1999 ribbon the only bright red.

---

## 11. Worked examples

### 11.1 The sill: a payoff by rhyme (*The Catch*, sc02 and sc06)

**Text.** Plant: "Halfway up: a tall maintenance opening through the shaft wall, broad enough to pass a machine through. Cables run out into a passage. Its steel sill has been worn bright by other people's sleeves." / "She hooks an arm over the sill. Rests her face against the brick. Her arm settles into the shape of the steel." Payoff: "The sill comes down into reach." / "Her arm knows it before she does." / "She catches it. Her palm drags across the bright steel."

**Choice.** At the plant, a side-on medium close at the sill's height (the right arm here follows this file's side recommendation, Section 6.2): her right arm enters from frame-left and settles along the polished band; her face rests on the brick. The only light is her torch, raking across the steel so the worn band shines against the dull metal around it (emphasis level 1: it catches a highlight, but the shot is about her resting). Let the rest play at its natural length, the time it takes her to get her breath back; do not hold past it (rule 6). No insert of the sill alone. At the payoff, cut to the same framing: same side, same height, and the same low raking angle across the band, though the source is now the floor light sliding past the moving cage (sc06: "Light, brick, light, brick"; the script does not say where her torch is by then), so the band shines against the dull steel exactly as it did at the plant, and no brighter. Her arm enters the frame into the same shape before her face arrives; the palm drags along the band. Emphasis level 3 by rhyme, not by size.

**Why.** "Her arm knows it before she does" is a statement about body memory. The only way to film body memory without a flashback is to let the audience's eye remember the composition at the same instant her arm does. A bigger shot or an insert at the plant would have told the audience "this will matter" and spent the surprise (rule 6). The polished band is set dressing that tells history ("other people's sleeves"), so the plant needs no explanation. Its opposite, the rung, fails the same habit minutes earlier (principle 9), which is why the audience trusts the sill less, and feels its payoff more.

**Avoid.** A flashback to the rest on the sill; slow motion on the catch; a sound sting on the drag.

### 11.2 The empty clip, then the recording (*The Catch*, sc07 and sc13)

**Text.** sc07: "Eli is on his knees at the opening, looking down into the shaft. The flask is in his fist." / "The clip under it is empty." / "Iona sees the empty clip." / "She takes his face in both hands and turns it towards her." / "Look at me. Can you walk?" sc13: "And in the long second of the fall, Eli's hand comes out from behind Jude's back." / "Empty." / "On the floor of the cage, where his hand was, a flat black puck is clipped to the grid."

**Choice.** sc07 is built as an eyeline chain: Iona's face (medium close), her look down, then an insert of the flask in his fist from her side, the empty spring clip facing the lens, with nothing else in the insert (emphasis level 2). Then she turns his face, not the flask, toward her. In sc13, the puck on the recording is small in a high surveillance frame (B1's security-camera rules). The emphasis comes from Iona pausing the recording and from the frame holding still, not from a zoom into the footage. Then, as the script says, she "Looks at her brother. Not at Jude." and says "You did that." with the paused frame still visible on the monitor beside or behind them, so the evidence stays in shot while she accuses him.

**Why.** The empty clip is metonymy: the holder stands for the missing puck, and the missing puck for a secret decision (Section 2.3). Absence cannot be seen unless something frames it (rule 9), so the clip gets its one insert here; the flask is in that frame only as the thing the clip hangs from, and the shot is composed on the clip. The flask gets no insert composed on itself before sc24: its contents are close to a MacGuffin, and its own single loud moment is saved for Iona's decision (Section 2.6). Iona sees the clue and chooses to act on Eli's fear rather than on the clue: taking his face is the subtext. By sc13 the audience has carried the empty clip for six scenes, so the tiny puck in a surveillance frame is enough. Enlarging it would insult that memory.

**Avoid.** A glint on the empty clip; a music cue on "Iona sees the empty clip"; a digital zoom that turns the surveillance image into a clean close-up.

### 11.3 The figure reads Nell's drawing (*The Catch*, sc23)

**Text.** "Iona walks up to it. The closest she has been. She shows it Saye pointing at the collection room. Then points at the beds. At the way home on her visor." / "The figure looks from one to the other." / "Then it turns its head to Nell's shelf. To the drawing propped against the bowl: a window, a tree, a small house." / "It looks back at the green line on her visor." / "The hum under the floor wavers." ... "Then it moves, and it is fast."

**Choice.** The figure has no face, only a pale strip, so its thought must come entirely from the order of objects it looks at: a three-shot eyeline chain. Shot 1: over the figure's shoulder to Iona's visor (the green line). Shot 2: the figure's head turning, the pale strip sliding across, in profile. Shot 3: its point of view onto Nell's shelf, the drawing propped against the bowl, facing the lens (emphasis level 3, the drawing's payoff). Shot 4: back to the visor's green line, closer than shot 1. Then action. The drawing was placed at level 1 earlier in sc20 ("She props the drawing of the house against her bowl"), so it is already standing up and facing the room.

**Why.** Kuleshov's principle (Section 2.8): a blank face reads as the thought of whatever it is cut against. Visor, drawing, visor reads as "her way home is like Nell's house", and the figure's next action (sending the beds home) confirms the reading without a word. It is also a GOODS-to-PERSONS hinge: a being that collects and files understands a child-simple drawing of home.

**Avoid.** Having the pale strip "light up" or change color when it understands; the thought must come from the cutting.

### 11.4 The copied name (*The Catch*, sc21)

**Text.** "In a small clear container at the end of a shelf floats a strip of blue cloth. The sleeve of her shirt, stiff with Jude's blood." / "Above it, a label. Her name, copied from a hospital wristband stroke for stroke, the way you would copy a drawing. By someone who did not know they were letters." / "IONA VALE." / "She turns the container in her glove. Behind the cloth, something cloudy moves." / "In the curve of the container: the room behind her, and the figure standing in it. Close enough to touch."

**Choice.** The room first, wide, at its full order ("Found. Carried here. Sealed. Put in order."), with the cage wreck in the middle and shelves of containers at the same size as the wreck's details, so people's traces and objects are filed alike (GOODS). Then Iona's search along the shelf: the camera moves only as fast as she walks and stops when she stops (staging, not an added signal, rule 23), ending on the container at emphasis level 3: the blue strip (the only blue in this dark room, B2), the label above it drawn in careful, even strokes like a copied picture. She turns it; the cloudy movement. Then the figure's reflection in the curved plastic: the reveal is placed inside the emblem.

**Why.** The strip is synecdoche (part of Iona standing for her), and it was planted twice (the blue shirt from sc01 at level 0; the sleeve pressed into the wound in sc07 at level 2). This is its develop at full volume because it is the story's hinge: the collector filed her like goods, but chose her. The handmade label makes the collector's mind visible (it does not read; it copies). Putting the figure's reflection in the container ties the object to its keeper before the story explains the keeper.

**Avoid.** Printed, font-perfect lettering; a light inside the container; an ominous music sting (the figure here is straightening, not threatening: "Straightens a container she has knocked a finger's width out of line").

### 11.5 The knuckle and the ribbon (*The Long Places*)

**Text.** Chapter I: "The oil goes to the first knuckle of the thumb and no further. Oil past the knuckle is for the greedy or the frightened, and the lamp can tell the two apart, though I never managed it." Melek, with "knuckles like burl, a burn gone silver across the back of the right one". 1999 (Chapter II): Nilay "filled it herself, past any knuckle, greedily, the way the frightened do." Later in Chapter II, when she once told Melek about the lamp, Melek said: "You filled it badly. Past the knuckle. The greedy or the frightened." Márton (Chapter IX) and Yusuf (Chapter XII) also fill "to the first knuckle of his thumb and no further". Chapter XI: "The oil went to the first knuckle of her own thumb and no further, and her knuckle was not Melek's knuckle, and the difference was millimeters, and the difference was everything." Chapter XIV: Emre "topped the lamp to the first knuckle of his thumb and no further", and says: "You filled the lamp badly, that night," ... "Past the knuckle. The greedy or the frightened."

**Choice.** One repeated macro insert, identical in lens, angle, light and hand position: a thumb at the lip of a small lamp, the oil's surface meeting the first knuckle, lit only by the neighboring niche's flame. The lamp itself follows the text rather than the composition: small niche lamps for Melek, the tin lamp in 1999, and in Chapter XIV "a bowl on a tall stem", the lamp that "is not your lamp", which quietly tells the audience she is somewhere else. Only four hands get the insert: Melek's burled knuckle with the silver burn scar; eighteen-year-old Nilay's hand in 1999, the oil over the knuckle and trembling; Nilay's hand on her first round from the book (Chapter XI), steady at the knuckle; Emre's hand. Márton's and Yusuf's fillings are shown at level 0 to 1 in wider shots, so the insert stays rare (rule 12). Emphasis level 2 each time; the last (Emre's) is level 3 because his line turns it into recognition: he knows how she filled the lamp that night because he was there, and his words are Melek's words from Chapter II. Keep Melek's line audible in its own scene so that Emre's repetition lands as an echo without any flashback. The red ribbon he then lays on the mat is the scene's second payoff; keep it at level 2, since the lamp insert has just spent the level-3 moment, and let her face carry the rest.

**Why.** The rule is constant and the body is personal: "her knuckle was not Melek's knuckle". A fixed composition makes the constancy visible, and the changing hands make the succession visible. This is the objective correlative for "a road that's long instead of far" without any time-travel imagery. The 1999 overfill is the only variant in the composition's content, so it reads as fear without a word.

**Avoid.** A montage of hands with music; a cross-dissolve between hands (the novella's point is succession, not merging); showing anyone but Nilay touching the 1999 lamp, or showing it relit (Section 10, L1); a flashback to Melek when Emre repeats her line.

---

## 12. Checklist

A "no" needs a fix or a written reason.

**Once per film**
- [ ] Is the theme written as a question and the core opposition as two nouns?
- [ ] Does every spine motif sit on a pole of the core opposition, or cross between them?
- [ ] Is there at least one hinge, and does it get the film's largest single payoff?
- [ ] Counted per channel (visual, sound, body), is the number of spine motifs within Section 3.2's caps?
- [ ] Does each pole have a one-line shape and material family, and does every invented object belong to one of them?
- [ ] Is there a written emphasis-3 map (one line per scene that has an L3), as in Section 9.1?
- [ ] Was every motif harvested from the text, and is every invention flagged as one?
- [ ] Does each motif have a one-line meaning that the user has approved?

**Per motif (register entry)**
- [ ] Is there a plant, at least one develop, and a payoff, each with scene, line and emphasis level?
- [ ] Is the plant at level 0 or 1, or, if it is a plot event, at no more than level 2 with nothing pointing forward (Section 3.4, plant exception)?
- [ ] Is the payoff louder than the plant, or an exact rhyme of it, or (for a hinge) a deliberately quiet payoff after a level-3 reveal?
- [ ] After the payoff, do all later appearances stay at level 0 or 1 (up to 2 only for a readout the plot needs, with nothing recalling the payoff), with at most one coda (rule 26)?
- [ ] Would this thing fit any film with the same theme? If yes, it is stock (rule 25).
- [ ] Does each return change state, owner, neighbor or audience knowledge?
- [ ] If the payoff depends on a rule, is there a teaching shot before it?
- [ ] Is its look (silhouette, color, material, size) fixed and distinguishable from everything near it?
- [ ] Does it have one emphasis-3 moment at most (two only for a deliberate inversion)?

**Per scene**
- [ ] Does each beat with an inner state (from A2) have a thing carrying it, or a note that the actor carries it alone?
- [ ] Is there at most one emphasis-3 moment per turning point, at most two in the scene, and never two in consecutive shots? For sound motifs, is S3 used at most once per motif?
- [ ] Does every symbolic thing have a practical reason to be here?
- [ ] Is the set's loudness decided (Section 4.1), and does the dressing tell the right history (wear, absences)?
- [ ] Is every costume and makeup state correct against the state table, including sides?
- [ ] Where the dialogue states a meaning, is the object kept at emphasis 0 or 1 during that line?

**Per shot**
- [ ] Does the THINGS field list every register item in frame, with state and emphasis level?
- [ ] Is every item with a side (ring, wound, sleeve, smile) on the recorded side and in the right mirror state (C2)?
- [ ] Is anything important too small to survive the output resolution? If so, give it its own shot or move it closer.
- [ ] At every level-3 beat, count the added signals (music, light change, sound change, slow motion, unmotivated camera move). Is the count zero where the script already marks the beat, and at most one elsewhere (rule 23)? Script markers (a state change, a line, a look or touch) are never removed.
- [ ] Does the prompt for this shot contain any meaning word or mood adjective (Section 14.3)? Replace it with nouns, materials, positions and sizes.

---

## 13. Common mistakes and how to spot them

| Mistake | What it looks like | How to spot it | Fix |
|---|---|---|---|
| **The announced symbol** | An object whose only reason to exist is to mean something (a caged bird for a trapped wife) | Ask "why is this object here, practically?" If the only answer is its meaning, it fails | Replace with an object the story already uses, or give it a practical job |
| **Borrowed meaning** | Doves, crosses, clocks, ravens, broken mirrors, chess pieces | The meaning would be the same in any film | Build meaning inside the story (Section 2.4) |
| **Insert overkill** | Every motif gets a close insert, often at the plant | Count inserts per scene; more than one or two is a warning | Drop plants to level 0 or 1; keep inserts for develops that change state and for payoffs |
| **Stacked signals** | Object insert plus music sting plus light change plus a line of dialogue about it | More than one added signal, or any added signal on a beat the script already marks | Keep the script's marker and the framing; drop the added signals (rule 23) |
| **Telegraphing** | The plant is framed bigger than the payoff | Compare emphasis levels in the register | Lower the plant; raise or rhyme the payoff |
| **Wallpaper** | The motif appears in nearly every scene unchanged | Count appearances; check each for a change | Ration it; every return must change something |
| **Motif drift** | The same object means different things with no design reason | Compare its meaning line against each appearance | Rewrite the meaning line, or cut the stray appearance |
| **Orphan plant or payoff** | A shown gun that never fires; a payoff with no plant | The register has an entry with no payoff, or a payoff with no plant | Add the missing appearance or cut the other |
| **Explained metaphor** | A character describes the symbol for the audience | A line of dialogue names what an object "means" | Cut the line, or give it a practical in-scene purpose |
| **Everything is symbolic** | Every set is loud and allegorical | More than two loud sets in a realistic film | Decide loudness per set; quiet most of them |
| **Dressing that lies** | Clutter that does not match the character's history; brand-new objects in an old place | Ask "who bought this, when, and why is it still here?" | Dress from the character's history outward |
| **Costume as fashion** | Clean, pressed, new clothes on working people; changes with no story reason | Check wear and damage against events; check each change against a turning point | Age and damage costumes to events; tie changes to beats |
| **Continuity break** | Wound on the other hand; torn sleeve whole again; ring on the wrong hand | Run the state table against every shot | Fix the shot or regenerate with the correct reference |
| **Cliché played big** | Hands on glass with breath fog, slow push-in and strings | Familiar image plus maximum emphasis | Play it plainly and let the story's specifics carry it (rule 24) |
| **Symbol replaces action** | A meaningful object shown instead of a character choosing something | The beat has no choice, only an image | Put the object in the character's hands at the moment of choice |
| **Stock shorthand** | Rain for sadness, a ticking clock for pressure, a wilting or lone houseplant for grief, a cracked mirror for a split self, a chess game for strategy, a caged bird, candles for memory, an empty chair for the dead, a prison-style tally wall | Apply rule 25: would it fit any film with this theme? Search the register for things with no quoted line from the text | Replace with a harvested thing, or keep only if the text names it and gives it a practical job and a state change (the mint, the tally wall of *The Long Places*), then play it at the lowest emphasis that works |
| **Glowing object** | The important thing is lit from within, rim-lit, or hums; the model makes it the brightest thing in frame | The object is brighter than the faces or has a light source the scene lacks | Light it with the scene's own light (B2); if it must read, raise contrast in one component only (Section 2.10) |
| **Loud after the payoff** | A paid-off motif keeps returning at full size (the flask shown in close-up again in the final scene) | The register has L2 or L3 entries after the payoff | Drop them to L0 or L1, or cut them (rule 26); in *The Catch* the flask's absence after sc24 is the image |

---

## 14. How to say this to an AI image or video model

Image and video models draw nouns, materials, colors, positions and visible damage. They do not know what your motifs mean, and they cannot remember a prop from one generation to the next unless you give them a reference image. Everything below is based on vendor prompting guides and common practitioner experience (see C1 and C2), not on controlled tests; models change fast, so test before relying on any of it.

### 14.1 What models tend to follow

- **Concrete nouns with material, color and size:** "a small brushed-steel vacuum flask", "a flat matte-black disc the size of a hockey puck, no markings, clipped under it with a metal spring clip".
- **Visible wear and damage described physically:** "a grey steel sill with one bright polished band along its edge where arms have rubbed it for years; the rest dull"; "a torn-off strip of blue cotton shirt sleeve, stiff and dark brown with dried blood".
- **Position and size in frame:** "in the lower left of the frame, small", "on the shelf behind her, out of focus". This is how to set an emphasis level.
- **A single saturated accent against a muted scene:** "the only bright color is a small red plastic safety tag wired to the gate".

### 14.2 What models follow only partly

- **Short, correctly spelled text on a prop** in recent image models; much less reliably in video. For anything that must be exact ("Goods only. No persons.", "IONA VALE"), make the text as a separate graphic and composite it (C2).
- **States across shots.** A model will not keep the sleeve torn or the palm bandaged unless every shot gets the reference image for that state. Make one prop or costume reference per state (C2, prop sheets).
- **Hands doing fine work** (a thumb in oil to the first knuckle; tape sealing a crack). Stills are more reliable than video; for the key inserts, consider a Blender animation, real footage of hands, or a video model driven by a start and end frame.
- **Sound.** Video models with native audio can produce "a slow mechanical pump sound", but the same exact rhythm repeated across clips is unlikely. Record or design the pump once and lay it in during editing.

### 14.3 What models ignore or misread

- **Meaning words:** "symbolizes", "represents", "a metaphor for", "motif", "foreshadowing", "Chekhov's gun", "objective correlative". At best they are ignored; at worst they pull in stock imagery.
- **Mood adjectives on objects:** "ominous", "mysterious", "important", "symbolic" tend to produce glowing, centered, hero-lit objects, the opposite of a quiet plant.
- **Absence:** "an empty clip", "no photographs on the walls". Models tend to add the thing you name. Describe what is there instead: "a bare metal spring clip closed on nothing"; "a bare, clean kitchen; bare white fridge door; the only object is a pot of mint on the windowsill". Use a negative prompt field where the tool has one.
- **Left and right on bodies:** rings, wounds, the side of a half-smile. Expect errors; check every frame, fix by inpainting (repainting one area of an image) or compositing, and follow C2's mirror-state rules.
- **Mirror-reversed writing:** usually "corrected" or garbled; use a flipped insert graphic (C2).

### 14.4 Phrasebook: breakdown term to model phrase

| Breakdown says | Say to the model instead |
|---|---|
| "M02 sill, plant, L1" | "Side view, medium close: a woman's forearm resting along a steel ledge that has one bright polished band worn along its edge; her cheek against wet brick; lit only by a flashlight held in her mouth" |
| "M05 empty clip, L2 insert" | "Extreme close-up: a man's fist gripping a small steel vacuum flask; beneath it a bare metal spring clip, closed on nothing; dark background" |
| "M11 label drawn, not printed" | "A small clear plastic container on a metal shelf; inside, a stiff strip of blue cloth stained dark brown; above it a handwritten label, letters drawn slowly and evenly like a careful copy of a picture" (then composite the exact letters) |
| "M01 red is the only accent" | "Muted grey-black wet brick tunnel; the only bright color is a small red plastic safety tag wired to the cage gate" |
| "Emphasis 0" | "in the background, small, slightly out of focus" |
| "Emphasis 3" | Pick one, as the register entry says: "fills the frame" or "extreme close-up"; or "held still, centered, the only sharp thing in the frame"; or the exact composition of the plant shot (for a rhyme). Use a camera instruction such as "slow push in to the object" only if the entry calls for a move, and never together with music on the same beat (rule 23) |
| "Sound S3" | Not a prompt: an editing note. Drop all other sound; the motif sound alone |
| "M17 reveal, L3, no added signal" | "Medium close, camera still: the chest plates of a tall matte-black machine body swung open like two doors; inside, clear tubes, a small metal mount and a forearm-length glass vessel of dark water; the mount and vessel are the only sharp things; lit only by the same dim light as the rest of the room, no light coming from inside" |
| "L5 permit, softened by body heat" | "a folded official paper, creased soft and slightly curved, taken from the inside pocket of a linen jacket" |

---

## 15. Open questions for the user

1. **Which hand is injured, and which sleeve is torn?** This file recommends Iona's right hand and right sleeve so her left (ring) hand stays clean. Confirm or change.
2. **Which shoulder is Jude shot in, and which side does Eli's half-smile lift?** Needed before any asset sheet (C2 asks the same).
3. **The suit rhyme.** Should Iona's white pressure suit and the figure's black suit share a construction language (Section 6.3)? This is interpretation, not text.
4. **The red tag in the wreck.** The script does not say whether the tag survives on the wrecked cage in sc21. Show it at emphasis 0, or leave it out?
5. **The ribbon in *The Long Places*.** Adopt it as a spine motif and reserve saturated red for it alone?
6. **Loud sets.** This file makes Saye's kitchen and the collection room the two loud sets in *The Catch*. Agree?
7. **The cup (M16) and shape families.** This file adds the cup moved into reach (sc13, sc15, sc23) as a supporting motif, and proposes shape and material families for GOODS and PERSONS (Section 9.1). Both are readings of the text, not stated by it. Keep, change or drop?
8. **The lamp in *The Long Places*, Chapter XIV.** The text gives Emre's lamp as "a bowl on a tall stem", unlike the village's small niche lamps. This file keeps the knuckle insert's framing constant but lets the lamp change with the text. Agree?
9. **The largest payoff.** This file gives the film's largest single payoff (longest hold, strongest contrast) to the figure's chest opening in sc25 (M17), not to the copied name in sc21 or the rings in sc29. Agree?
10. **Saye's bare kitchen.** Should the set be read as the home of the woman who sent Nell across (Section 4.3), or kept neutral? Either way, no object in it should point to Nell.

---

## Sources

**Books and essays**
- Bordwell, David, Kristin Thompson (and Jeff Smith in recent editions). *Film Art: An Introduction.* First edition Addison-Wesley, 1979; later editions McGraw-Hill. Mise-en-scène; motif; similarity and repetition, difference and variation.
- Van Sijll, Jennifer. *Cinematic Storytelling: The 100 Most Powerful Film Conventions Every Filmmaker Must Know.* Michael Wiese Productions, 2005. (Publisher's page describes "17 basic building blocks" and showing character change without dialogue; the 17 chapters and each convention's name and film example checked against the contents note in Stanford's library catalogue; the chapter text itself was not read.)
- Block, Bruce. *The Visual Story: Creating the Visual Structure of Film, TV and Digital Media.* Focal Press, 2001; later editions. The basic visual components; deep, flat and limited space; the Principle of Contrast and Affinity (paraphrased from memory, not quoted).
- Eliot, T. S. "Hamlet and His Problems" (1919), in *The Sacred Wood* (1920).
- McKee, Robert. *Story.* ReganBooks, 1997 (the "Image System" definition as reproduced on Goodreads and Quotefancy; the Internal Imagery sentence and the "Awareness of a symbol" sentence as reproduced on Karen Woodward's blog; the flag and cross examples paraphrased from memory). *Dialogue: The Art of Verbal Action for Page, Stage, and Screen.* Twelve / Grand Central Publishing, 2016 (the said, the unsaid and the unsayable, and "Action versus Activity", Chapter Three; showing versus telling, Chapter Two; "make image substitute for language", paralanguage and physical action, Chapter Five; read directly in the user's copy).
- Chekhov, Anton. Letter to A. S. Lazarev (Gruzinsky), 1 November 1889 (as quoted on Wikipedia; see below).
- Truffaut, François. *Hitchcock.* Simon & Schuster, 1967 (the MacGuffin; the bomb under the table).
- Mamet, David. *On Directing Film.* Viking, 1991.
- Jakobson, Roman. "Two Aspects of Language and Two Types of Aphasic Disturbances" (1956), including "The Metaphoric and Metonymic Poles" (the passing remark on Griffith, Chaplin, Eisenstein and "filmic similes" paraphrased from online copies, not checked in print).
- Carroll, Noël. "Visual Metaphor", in *Aspects of Metaphor* (Springer, 1994), pp. 189-218; "A Note on Film Metaphor", *Journal of Pragmatics* 26 (1996), pp. 809-822, doi:10.1016/s0378-2166(96)00021-5 (bibliographic data checked on Crossref, 2026-09-27).
- Whittock, Trevor. *Metaphor and Film.* Cambridge University Press, 1990.
- Bachelard, Gaston. *The Poetics of Space.* Presses Universitaires de France, 1958; English translation by Maria Jolas, Orion Press, 1964.
- Affron, Charles, and Mirella Jona Affron. *Sets in Motion: Art Direction and Film Narrative.* Rutgers University Press, 1995; reprinted 2022 (the five level names are its chapter titles, checked on the publisher's chapter list; the one-line glosses in Section 4.1 are this file's reading).
- Landis, Deborah Nadoolman. *Screencraft: Costume Design* (Focal Press, 2003); *Dressed: A Century of Hollywood Costume Design* (HarperCollins, 2007); *FilmCraft: Costume Design* (Focal Press, 2012). Her two quotations in Section 2.9 are from her interview with *The Talks*.

**Web (all checked 2026-09-27)**
- Objective correlative (Eliot's definition; Washington Allston): https://en.wikipedia.org/wiki/Objective_correlative
- Chekhov's gun (1889 letter; Gurliand 1904; Shchukin 1911): https://en.wikipedia.org/wiki/Chekhov%27s_gun
- Van Sijll book page: https://mwp.com/product/cinematic-storytelling/ ; publication year via Open Library: https://openlibrary.org/search.json?q=cinematic+storytelling+van+sijll
- Affron book record: https://openlibrary.org/search.json?q=sets+in+motion+affron ; chapter titles (Set as Denotation, Punctuation, Embellishment, Artifice, Narrative): https://www.degruyterbrill.com/document/doi/10.36019/9781978813199/html
- Van Sijll contents note (chapters, conventions, film examples): https://searchworks.stanford.edu/view/10768021
- Jakobson's cinema remark (online copy): https://commons.princeton.edu/shakespeares-language/wp-content/uploads/sites/41/2017/09/Jakobson-Two-Aspects-of-Language-and-Two-Types-of-Aphasic-Disturbances.pdf
- McKee on internal imagery and on awareness of symbols (as reproduced): https://blog.karenwoodward.org/2014/10/on-using-symbols-in-your-story.html
- Carroll bibliographic record: https://api.crossref.org/works?query.bibliographic=A+Note+on+Film+Metaphor+Carroll
- Metaphor and metonymy (Jakobson 1956): https://en.wikipedia.org/wiki/Metaphor_and_metonymy
- Leitmotif (definition; Jähns 1871, Wolzogen 1876, *Jaws*): https://en.wikipedia.org/wiki/Leitmotif
- Kuleshov effect (Pudovkin 1929 account; footage lost; Prince and Hensley 1992, Mobbs 2006, Barratt 2016): https://en.wikipedia.org/wiki/Kuleshov_effect
- McKee's Image System definition (as reproduced): https://www.goodreads.com/quotes/search?q=%22image+system%22+mckee
- Chekhov's 1886 letter and the "moon" paraphrase: https://en.wikipedia.org/wiki/Show,_don%27t_tell
- Van Sijll publication data: https://books.google.com/books?vid=ISBN193290705X
- *Strike* (1925) slaughter intercut: https://en.wikipedia.org/wiki/Strike_(1925_film)
- *The Poetics of Space*: https://en.wikipedia.org/wiki/The_Poetics_of_Space
- Ken Adam: https://en.wikipedia.org/wiki/Ken_Adam ; *Dr. Strangelove* War Room: https://en.wikipedia.org/wiki/Dr._Strangelove
- Jack Fisk: https://en.wikipedia.org/wiki/Jack_Fisk ; *Days of Heaven* mansion: https://en.wikipedia.org/wiki/Days_of_Heaven
- *Edward Scissorhands* (Bo Welch quotation): https://en.wikipedia.org/wiki/Edward_Scissorhands
- *Do the Right Thing* (Wynn Thomas; love and hate rings): https://en.wikipedia.org/wiki/Do_the_Right_Thing
- Hannah Beachler: https://en.wikipedia.org/wiki/Hannah_Beachler ; *Black Panther* design and costume: https://en.wikipedia.org/wiki/Black_Panther_(film) ; Beachler on her 500-page Wakanda bible (*The Credits*, Motion Picture Association, 2019): https://www.motionpictures.org/2019/02/black-panther-production-designer-rooted-worlds-advanced-nation-african-culture-2/
- Ruth E. Carter: https://en.wikipedia.org/wiki/Ruth_E._Carter
- Sarah Greenwood: https://en.wikipedia.org/wiki/Sarah_Greenwood ; *Anna Karenina* (2012): https://en.wikipedia.org/wiki/Anna_Karenina_(2012_film) ; *Atonement* (2007): https://en.wikipedia.org/wiki/Atonement_(2007_film) ; *Barbie* (2023): https://en.wikipedia.org/wiki/Barbie_(film)
- Rick Carter: https://en.wikipedia.org/wiki/Rick_Carter ; *Jurassic Park* design: https://en.wikipedia.org/wiki/Jurassic_Park_(film)
- Dante Ferretti: https://en.wikipedia.org/wiki/Dante_Ferretti ; *Gangs of New York* sets at Cinecittà: https://en.wikipedia.org/wiki/Gangs_of_New_York
- Colleen Atwood: https://en.wikipedia.org/wiki/Colleen_Atwood ; interview, *The Talks*: https://the-talks.com/interview/colleen-atwood/ ; NPR profile (2016), via North Country Public Radio: https://www.northcountrypublicradio.org/news/npr/496119928/colleen-atwood-to-design-the-costume-understand-the-character
- Deborah Nadoolman Landis: https://en.wikipedia.org/wiki/Deborah_Nadoolman_Landis ; interview, *The Talks*: https://the-talks.com/interview/deborah-landis/
- *Parasite* (2019) house and scholar's rock: https://en.wikipedia.org/wiki/Parasite_(2019_film) ; https://en.wikipedia.org/wiki/Suseok
- *Citizen Kane* (sled, snow globe, Perry Ferguson): https://en.wikipedia.org/wiki/Citizen_Kane ; Xanadu jigsaw scene (film-study summaries found by search): https://www.sparknotes.com/film/citizenkane/quotes/page/5/
- *Schindler's List* (red coat; Spielberg's comment): https://en.wikipedia.org/wiki/Schindler%27s_List
- *Vertigo* (Edith Head's grey suit): https://en.wikipedia.org/wiki/Vertigo_(film)
- *Rear Window* (the ring): https://en.wikipedia.org/wiki/Rear_Window
- *Notorious* (the key; uranium in wine bottles): https://en.wikipedia.org/wiki/Notorious_(1946_film)
- *Suspicion* (light in the milk): https://en.wikipedia.org/wiki/Suspicion_(1941_film)
- *In the Mood for Love* (William Chang; cheongsams): https://en.wikipedia.org/wiki/In_the_Mood_for_Love
- *Up* (2009) (Docter on Carl's and Russell's shapes; the house): https://en.wikipedia.org/wiki/Up_(2009_film)

**Test texts:** *The Catch* (workshop revision, 25 September 2026), read in full; *The Long Places* (revised final), Chapters I to III and XIV read in full, other chapters searched for the motifs named here (passages in Chapters IV, IX, XI and XII re-read in the fact-check pass). Every quotation from both texts in this file was machine-checked for verbatim match, and every *Catch* quotation against the scene it is attributed to.

**Checked in the fact-check pass (2026-09-27), all on the pages listed above:** Wynn Thomas's red and orange paint and the hands on which Radio Raheem's rings sit (*Do the Right Thing*); that Wikipedia credits Ryan Coogler with a "project bible" of the tribes, while Beachler herself describes a roughly 500-page design bible her team built (MPA interview), and Beachler's tribal sigils and architecture (*Black Panther*); Ruth E. Carter as costume designer of *Do the Right Thing* and her two Oscars; Lee Ha-jun's quotation on the Park house; Rick Carter's full quotation; Colleen Atwood as costume designer of *Edward Scissorhands*; the *Notorious* crane shot ending on the wine-cellar key; the *Citizen Kane* sled wording; the *Strike* cattle intercut; the *Schindler's List* color scheme and Spielberg quotation; the *Anna Karenina* soundstage theatre and Gerwig's "authentic artificiality"; the *Up* shape quotations; the *Vertigo* grey suit; the *Days of Heaven* mansion; the *Dr. Strangelove* War Room. Second pass (also 2026-09-27): the *Atonement* vase (Robbie breaks it accidentally, per Wikipedia's plot); the *Citizen Kane* sled (the boy's age is not given on the page, so it was removed) and the Xanadu jigsaw scene (film-study sources found by search); Van Sijll's contents; the Affrons' chapter titles; Landis's and Atwood's interview quotations; Ferretti's *Gangs of New York* sets; the *Parasite* rock and house quotations; the *Up* quotation; McKee's *Dialogue* passages re-read in the local copy; every quotation from *The Catch* and *The Long Places* re-checked by script after the edits, for verbatim match and for the scene or chapter it is attributed to. McKee's *Dialogue* claims were re-read in the user's copy (Chapters Two, Three and Five).

**Stated plainly: not verified.** McKee's image-system, internal-imagery and awareness-of-symbols wording against a printed copy of *Story* (only quotation sites and a blog were available); Bruce Block's exact wording of the Principle of Contrast and Affinity; the text inside Van Sijll's chapters (only the contents list was checked); what the Affrons mean by each level name (only the names were checked); Jakobson's exact wording on cinema (paraphrased); any statement of method by William Chang. Also not used, because I could not confirm them from a source in this session: the popular reading of the oranges in *The Godfather* (1972) as deliberate omens of death, and the color progression of Nina's costumes in *Black Swan* (2010).
