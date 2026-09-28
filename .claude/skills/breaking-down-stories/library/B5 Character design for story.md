# B5. Designing Characters for Story: Face, Body, Silhouette, Costume, Color, Movement and Body Language

> **What this file is for**
> 1. It tells the pipeline how to decide what each character looks like and how each one moves, so that every visible choice serves the story's theme, the character's role and the character's arc.
> 2. It gives principles, a translation table, "If ... then consider ... because ..." rules, a checklist, common mistakes, and a written format (the character bible entry) that a performer, an animator or an AI model can follow.
> 3. It covers faces without pseudoscience, costume as biography and continuity, movement systems (Laban, Chekhov, Johnstone, Lecoq), and non-human characters that must frighten first and earn pity later.
> 4. It ends with full design entries for all ten characters in *The Catch*, including an AI identity key for each.
> 5. Run it after the scene breakdown (A2, A3) and the motif register (B4), and before shot design (B1, B3), lighting (B2) and asset sheets (C2, C3).

---

## 0. How to use this file

### 0.1 Order of work for an LLM running the pipeline

1. **Read for evidence.** For each character, collect every line the text gives about face, body, clothes, marks, gestures and movement. Quote them; do not paraphrase yet.
2. **Role and arc.** Write the character's narrative role and arc in one line each (Section 1, principle 1).
3. **Design thesis.** Write one sentence saying what the design must make an audience feel and know before anyone speaks (Section 2.6).
4. **Whole figure.** Decide silhouette, shape language, proportion, posture and value against the rest of the cast (Section 2).
5. **Face.** Fill the face specification (Section 3.2), then the expression range tied to real beats (Section 3.3).
6. **Costume.** Fill costume states by story phase and the damage ledger (Section 4).
7. **Movement.** Write the movement signature (Section 5.7).
8. **Non-human characters.** Run Section 6, including the clue ledger.
9. **Bible entry.** Assemble the character bible entry and identity key (Section 7).
10. **Check.** Run the checklist (Section 12) and the mistakes list (Section 13). Hand the entries to C2 for asset sheets.

Mark every choice the text does not state as **[design choice]**. Mark every choice derived by logic from the text as **[inferred]**, with the reason.

### 0.2 For the non-technical user

Say to the LLM: "Run file B5 on my script and give me the character bible entries." Then read only two lines of each entry: the **design thesis** and the **identity key**. If a thesis feels untrue to the person you imagined, say so in plain words ("Saye is not cold, she is frightened"), and ask the LLM to redo that entry. You decide anything marked [design choice], especially casting-type choices such as ethnicity, which the script of *The Catch* never states for anyone.

### 0.3 Words this file uses (one word per concept)

| Term | Plain definition |
|---|---|
| **Design thesis** | One sentence stating what a character's look and movement must communicate, and why. |
| **Silhouette** | The shape of the whole figure filled in solid black, with no inner detail. (The script of *The Catch* uses "outline" for the visor display; this file keeps "outline" for that display only.) |
| **Shape language** | The habit of building a figure from one dominant simple shape (circle, square, triangle) because audiences tend to read feelings into those shapes. |
| **Proportion** | The size of body parts relative to each other, for example head to body height. |
| **Value** | How light or dark something is, ignoring hue. |
| **Hue** | The color family of something (blue, green, red), as distinct from how light it is or how strong it is. |
| **Saturation** | How strong or pure a color is, from grey (no saturation) to vivid (full saturation). |
| **Characterization** | In Robert McKee's usage, everything visible on the surface of a character (see Principle 1). |
| **True character** | McKee's term for who a character really is, shown only by choices under pressure. |
| **Dimension** | McKee's term for a consistent contradiction inside a character (see Principle 2). |
| **Distinguisher** | One of the three face or body features that make a character unlike everyone else in the cast (Section 3.2). |
| **Costume state** | One numbered version of a character's clothes, marks and injuries at one point in the story. |
| **Costume plot** | A chart of every costume state for every character in every scene. |
| **Damage ledger** | A list of every injury, stain, tear or loss on a character, with the scene it starts, its side of the body, and each change after. |
| **Color identity** | The one hue (and value) that belongs to a character across the film. |
| **Movement signature** | A short written description of how a character habitually moves, precise enough to reproduce. |
| **Signature gesture** | One habitual gesture the audience learns to recognise as belonging to one character (Section 5.6). |
| **Effort** | Rudolf Laban's term for the quality of a movement, described by four factors: weight, time, space and flow (Section 5.1). |
| **Psychological gesture** | Michael Chekhov's term for one large whole-body gesture that sums up what a character wants (Section 5.2). |
| **Status** | Keith Johnstone's term for the moment-to-moment behavior by which people raise or lower themselves relative to others (Section 5.3). |
| **Proxemics** | How close characters stand to each other and what that distance means; the distance zones are in B3, Section 4.2. |
| **Tempo** | The speed at which a character habitually moves and reacts. |
| **Expression range** | The set of named facial states a character must reach in the story, each tied to a beat. |
| **Micro-expression** | A facial movement so brief (well under half a second) that viewers may register it without noticing it. |
| **Eyeline** | The direction a character is looking, which tells the audience what they are looking at. |
| **Clue** | A visible or audible detail planted early that the audience can recognise on a second viewing as pointing to a later reveal. |
| **Clue ledger** | A table listing every clue, where it is first shown, how strongly, and what it means on a second viewing (Section 6.4). |
| **Emphasis level** | How strongly the camera presents a thing, from L0 (in frame, not pointed at) to L3 (the shot is about it); defined in B4, Section 3.4. |
| **Mirror state** | Whether a character appears as designed (NORMAL) or left-right flipped (MIRRORED) in a given part of *The Catch*; defined in C2, Section 7.3. |
| **Era** | One of C2's three mirror periods of *The Catch* (A, B, C); boundaries are given at the start of Section 10. |
| **Character bible entry** | The complete written design for one character, in the format of Section 7.1. |
| **Identity key** | A fixed block of 25 to 40 words (20 to 30 for minor characters) describing a character, pasted unchanged into every AI prompt where the character appears. C2 calls the same thing a "look line". |
| **State line** | A short phrase added after the identity key to give the character's costume state in that scene. |
| **Turnaround** | The same character drawn or generated from front, three-quarter, side and back, in the same pose and light. |
| **Expression sheet** | A set of head-and-shoulders images of one character, each showing one entry from the expression range. |
| **Drift** | A character's look changing slowly and wrongly from shot to shot, especially in AI generation. |
| **Hero portrait** | The one approved head-and-shoulders image of a character that every other image of them is checked against. |
| **Hero costume and multiples** | The main, best-finished copy of a costume (the hero) and the identical copies made for stunts, blood and damage stages (the multiples). |
| **Insert** | A short close shot of a detail (a hand, a mark, an object) cut into a scene. |
| **Rim light (edge light)** | Light from behind or beside a subject that draws a thin bright line along its outline. |
| **Image-to-video** | Making a video clip by animating a supplied still image, so the still fixes how the first frame looks. |
| **Previs** | Rough 3D versions or moving storyboards of shots, made before production to plan staging and movement (C4). |
| **Control video** | A rough guide clip (a 3D blocking render or a filmed stand-in) that an AI video model follows for movement and framing. |
| **LoRA** | A small add-on file, trained on a few dozen images, that teaches an image or video model one specific look (C2, Section 3.4). |
| **Placeholder** | A value the pipeline fills in so generation can start (for example a skin tone or a gender), marked so the user can replace it. |

---

## 1. Core principles

1. **Design the surface so the story can crack it.** In *Dialogue* (2016, Chapter 2), McKee writes: "Writers, therefore, design characters around two corresponding parts known as true character and characterization." He defines characterization as "a character's total appearance, the sum of all surface traits and behaviors," with three functions: "to intrigue, to individualize, to convince." Everything in this file is characterization. Its job is to set up an appearance that a later choice can confirm or contradict. Iona's competent hands are characterization; her choice to delete her way home is true character.
2. **Design the contradiction, not just the trait.** McKee (Chapter 11) defines a dimension as "a contradiction that underpins a character's nature." A design with one note (all hard, all soft) is a poster. Put one visible element against the dominant one: Saye's grey control and her pot of mint; the figure's huge hands and the care with which it lifts an arm "As carefully as a nurse."
3. **Faces do not reveal character, but audiences read them anyway.** Judging character from facial features (physiognomy) is a pseudoscience. People still form trait impressions from a face within a fraction of a second, and those impressions are often wrong (Section 3.1). Design uses these readings as conventions, knowingly, and never as truth.
4. **One read first.** A character must be recognisable as a silhouette and as a value pattern before any detail. Detail is for close-ups.
5. **Contrast within the ensemble.** Characters who share a scene must differ in at least three of: height, mass, dominant shape, value, color, tempo. This helps the audience and, separately, it reduces AI identity mixing (Section 7.5).
6. **Costume is biography plus present state.** Clothes say who the person was before the story (work, class, habits) and what the story has done to them since (wear, damage, loss). The damage must be tracked like props (Section 4.4).
7. **Movement is the most specific thing a character has.** Two people in identical clothes are told apart by how they move. Write movement as verbs with qualities, not adjectives.
8. **Specific and visible beats general and inner.** "Knuckles like burl, a burn gone silver across the back of the right one" can be drawn; "a hard life" cannot.
9. **Plant everything the ending needs.** If a late scene depends on a side (a ring, a smile, a wound), the early design must fix that side and show it at emphasis level L0 or L1.
10. **Consistency is designed, not hoped for.** Especially with AI models, the design must be written as fixed words and fixed images before production (Section 7).

---

## 2. The whole figure: silhouette, shape, proportion, ensemble

### 2.1 Silhouette readability

Animators test a pose by filling it in black: if the action or attitude still reads, the pose works. Frank Thomas and Ollie Johnston's *The Illusion of Life: Disney Animation* (Abbeville, 1981) sets out the twelve principles of animation; its principle of **staging** is "the presentation of any idea so that it is completely and unmistakably clear" (as summarised on Wikipedia's page on the twelve principles, checked 2026-09-27). Silhouette testing is the standard working method for this, taught widely in animation; I could not re-check the book's own wording on silhouettes in this session.

In games, where players must identify characters at distance, Valve "designed each character, team, and equipped weapon to be visually distinct, even at range" for *Team Fortress 2* (2007) (Wikipedia, checked 2026-09-27), and documented the approach in the paper "Illustrative Rendering in Team Fortress 2" by Jason Mitchell, Moby Francke and Dhabih Eng (NPAR 2007, a conference on non-photorealistic rendering). The paper describes "designing characters with distinct silhouettes that can be easily identified" (as quoted on the Official TF2 Wiki's page for the paper, checked 2026-09-27).

For live-action and AI film, the silhouette test asks three things:
- **Who is it?** Can you tell each principal apart as a black shape at wide-shot size (the whole body small in the frame)?
- **What are they doing?** Does the pose read without the face?
- **What has changed?** Does a new costume state change the silhouette when the story needs it to (a suit, a strapped arm, a vessel on the chest)?

### 2.2 Shape language, and its limits

Tom Bancroft, a Disney animator who was supervising animator of Mushu in *Mulan* (1998) and was nominated for an Annie Award (the animation industry's main awards) for that work, wrote *Creating Characters with Personality* (Watson-Guptill, 2006, introduction by Glen Keane). (Do not confuse him with his twin brother Tony Bancroft, the film's co-director.) The publisher's description reads: "From Snow White to Shrek, from Fred Flintstone to SpongeBob SquarePants, the design of a character conveys personality before a single word of dialogue is spoken" (Penguin Random House listing, checked 2026-09-27). Character-design teaching, including Bancroft's book as I recall it, works from three base shapes:

| Shape | What audiences tend to read | Typical risk |
|---|---|---|
| **Circle** (round masses, curves) | Softness, warmth, approachability, youth, comedy | Reads as weak or childish |
| **Square** (blocks, verticals, right angles) | Stability, stubbornness, reliability, being fixed in place | Reads as dull or immovable |
| **Triangle** (points, wedges, diagonals) | Energy, danger, instability, cunning; a downward-pointing triangle (broad shoulders, narrow hips) reads as power | Reads as villainous by default |

A verified production example: for *Up* (2009), Wikipedia's production section reports director Pete Docter explaining that Carl "has a squarish appearance to symbolize his containment within his house, while Russell is rounded like a balloon," and that Carl was caricatured further than usual, "only at least three heads high" (checked 2026-09-27). A second, widely reported Pixar example: the five emotions of *Inside Out* (2015) were built on simple objects, Joy on a star, Sadness on a teardrop, Anger on a brick, Fear on a nerve and Disgust on a stalk of broccoli (reported in 2015 press coverage such as Creative Bloq and Screen Daily; not checked against a primary Pixar source in this session). Note what both examples do: the shape comes from the character's situation or feeling, not from a moral label.

Bancroft also sorts designs along a scale from iconic (very simple, symbolic) to realistic, which he calls a design hierarchy. Reviews of the book confirm the first four levels as iconic, simple, broad and comedy relief; the last two, as I recall them, are lead character and realistic. As I recall the book's examples, the hierarchy places characters within one production (a lead usually sits nearer the realistic end than a comedy-relief sidekick) while all of them must still look as if they belong to the same world. The useful point for this pipeline: live-action and realistic AI video sit at the realistic end, where shape language has to live in **build, posture, costume cut and hair**, not in drawn exaggeration.

**Limits.** These readings are conventions learned from media, not laws of perception. They vary by culture and they break when a story sets them up to break. Used lazily they become stereotype: the triangle-shaped villain with sharp cheekbones, the round comic sidekick. Use shape language for contrast and for arc (a shape that changes), and never as the only clue to morality.

**Restraint rules for realistic (live-action or AI) design.**
- If a character's dominant shape can only be seen by exaggerating the body, then carry it in one place only (the cut of the coat, the set of the shoulders, the hair), and keep the body a real human body.
- If the story will overturn a character (the figure), then give them the shape of the first impression and hide the overturning in the details (Section 6.4), never the other way round.
- If two principals would land on the same shape, then separate them by height or mass first; shape is the weakest of the lineup columns in realistic footage.

### 2.3 Proportion and body structure

- **Head heights.** Adults in realistic design are about seven to eight heads tall. Stylised characters shrink this (Carl's three heads). In realistic AI video, proportion variety comes from real body variety: height, limb length, shoulder width, neck length, weight distribution.
- **The body as history.** A realistic body records what a life has done to it. Climbing work builds forearms and shoulders; desk and lab work rounds the upper back; captivity and illness thin the wrists and weaken the knees; nineteen years of the wrong food thin everything. Choose the build the character's history would produce, then check it serves the design thesis.
- **Signature parts.** Give each principal one body part the camera can return to: Iona's hands, Eli's hidden hand, Saye's "quick flat hands", Nell's thin wrists, the figure's "huge black thumb".

### 2.4 Age, weight and posture

- **Age** shows in skin, hair, the set of the neck and shoulders, and speed of rising. Write the age the audience should read, and whether the character looks older or younger than they are, and why ("Sixty, perhaps. She looks older."). Choose the age markers, do not pile them on: for *Up*, Pixar gave Carl "wrinkles, pockmarks on his nose, a hearing aid, and a cane to make him appear elderly" but deliberately not "liver spots or hair in his ears", to keep him appealing (Wikipedia, "Up (2009 film)", checked 2026-09-27). Rule: pick two or three age markers that the story uses (Nell's thin wrists, her slowness) and leave the rest out.
- **Weight** means both body mass and how heavily the character seems to press into the ground. A slight person can move heavily; a large person can move lightly (Jude is "easy in the shoulders").
- **Posture** is the fastest arc tool. The same costume with a different spine tells a different chapter. Decide each character's default posture and the one or two scenes where it changes.

### 2.5 Ensemble contrast: the lineup

Character designers put the whole cast side by side at the same scale, as a lineup, to check contrast. Do this in writing for every story:

| Character | Height | Mass | Dominant shape | Value | Color identity | Tempo |
|---|---|---|---|---|---|---|
| (one row each) | | | | | | |

If two principals share four or more columns, change one. Siblings are the exception worth designing on purpose: give them one or two shared facial features (brow line, eye color) so kinship reads, and make everything else differ.

### 2.6 The one-image test and the design thesis

Before details, write the **design thesis**: one sentence of the form "*[Character] must read as [first impression], and carry [the contradiction or clue] that the story will later [confirm / overturn], because [theme or arc reason].*" Then test it: if you could show only one image of this character (a poster, a thumbnail), what pose, costume state and expression would carry the thesis? If you cannot name that image, the design is not finished.

### 2.7 Avoiding stereotype

- **Design from the role's specifics, not from a type.** Casting practice offers the model. The documentary *Casting By* (2012) is about Marion Dougherty, who, in Wikipedia's words, chose actors "based on their acting abilities, as opposed to type casting based on appearance" (checked 2026-09-27). The pipeline's equivalent: derive looks from work, history and circumstance in the text, not from the stock image of "scientist", "nurse" or "guard".
- **Do not code morality into ethnicity, body size, disability or facial difference.** The UK charity Changing Faces launched its "I Am Not Your Villain" campaign in 2018 against the film habit of marking villains with scars and facial difference (Wikipedia, checked 2026-09-27). This matters for *The Catch*: Iona's chipped tooth and skinned palm are marks of cost on the protagonist, which is the healthy direction; the figure's frightening quality must come from its behavior and its unknown nature, never from "deformity".
- **Leave casting-type choices to the user.** Where the text is silent on ethnicity, the entry states that it is open, gives a placeholder for AI generation, and marks it [design choice].
- **Hold a casting session for the AI performer.** A casting director sees many people for one part and chooses the one whose face and presence carry the role. The AI equivalent: generate six to twelve candidate portraits from the identity key alone, in neutral light, and have the user choose one against the design thesis. The chosen image becomes the hero portrait. If none fits, change the key's words, not the chosen face. Choose for what the face does at rest, not for attractiveness; AI candidates skew young and glossy, so reject any that erase the age, weathering or thinness the text gives.

---
## 3. Faces

### 3.1 What faces carry, and what they do not

- **Faces do not reveal character.** Physiognomy "meets the contemporary definition of pseudoscience" (Wikipedia, "Physiognomy", checked 2026-09-27). No bone structure means honesty, cruelty or intelligence.
- **Audiences read faces anyway, fast.** Alexander Todorov's *Face Value: The Irresistible Influence of First Impressions* (Princeton University Press, 2017) reviews the research, including Willis and Todorov (2006), "First impressions: Making up your mind after a 100-ms exposure to a face" (*Psychological Science*). The book's argument is that these impressions are fast, widely shared, and often inaccurate. For design, that means: audiences will assign warmth, dominance or trustworthiness to a face whether you intend it or not, so choose on purpose.
- **Common readings (conventions, not truths).** Rounder faces, larger eyes and softer features tend to read as younger, warmer and more naive (Leslie Zebrowitz's "babyface" research, summarised in her *Reading Faces*, 1997, not re-checked here). Strong brows, a heavy jaw and narrowed eyes tend to read as dominant. Wikipedia's summary of the animation principle of appeal (the quality that makes a character compelling to watch, which is not the same as being likable) notes that for likable characters "a symmetrical or particularly baby-like face tends to be effective."
- **Context does much of the work.** In the Kuleshov experiment (1910s to 1920s), the same neutral shot of actor Ivan Mozzhukhin was read as hungry, grieving or desiring depending on the shot it was cut against (a bowl of soup, a girl in a coffin, a woman on a divan). Prince and Hensley (1992) failed to replicate it; Mobbs and colleagues (2006) and Barratt and colleagues (2016) found the effect (Wikipedia, "Kuleshov effect", checked 2026-09-27). The practical rule: a face's meaning in film comes from face plus eyeline plus cut. Do not overload the face with "acting" when the cut will do it.
- **Expressions are not a fixed code.** Paul Ekman and Wallace Friesen's Facial Action Coding System (FACS, 1978) describes faces as numbered **action units**, each the movement of one or more muscles (for example AU1 inner brow raiser, AU4 brow lowerer, AU6 cheek raiser, AU12 lip corner puller, AU15 lip corner depressor, AU24 lip pressor; Wikipedia, checked 2026-09-27). That muscle vocabulary is reliable and useful. The claim that each emotion has one universal face is contested: Barrett, Adolphs, Marsella, Martinez and Pollak, "Emotional Expressions Reconsidered" (*Psychological Science in the Public Interest*, 2019) argue that people do not reliably make or read one configuration per emotion. Describe the movement; let context supply the emotion.
- **Micro-expressions: keep claims small.** Very brief expressions were first described by Haggard and Isaacs (1966). Their use for lie detection has weak support: Porter and ten Brinke (2008) coded 700 high-stakes genuine and falsified emotional expressions and found only 2% were microexpressions, and Wikipedia's summary adds that they appeared equally for truth-tellers and liars (Wikipedia, "Microexpression", checked 2026-09-27). So never design a micro-expression as a lie detector the audience is meant to "catch"; design it as a visible crack in composure that the story then explains. McKee writes that "The eye of the audience reads these microexpressions at up to one twenty-fifth of a second" (*Dialogue*, Chapter 5), citing Malcolm Gladwell's popular book *Blink* (2005), not a study. On screen, a flicker is real and useful; plan it at roughly a quarter to half a second (about 6 to 12 frames at 24 frames per second), long enough to register.

### 3.2 Specifying a face so it is distinctive and consistent

Write the face as a list in this fixed order, so every entry can be compared field by field:

1. **Age read** (and whether older or younger than actual age, with the reason).
2. **Head and face shape**: long, broad, oval, square; forehead height; cheekbone prominence.
3. **Bone structure**: brow ridge, cheekbones, jaw width and angle, chin.
4. **Eyes**: shape (deep-set, hooded, wide), set (close, wide), color, lid weight.
5. **Brows**: thickness, shape (straight, arched), height above the eye, how mobile.
6. **Nose**: bridge, length, width, any break or bend.
7. **Mouth**: width, lip fullness, resting set (closed, parted, pressed), teeth if seen.
8. **Skin**: tone [often a casting choice], texture, weathering, lines, pallor.
9. **Hair**: color, texture, length, how it is worn, hairline, parting side.
10. **Facial hair**, if any.
11. **Marks**: scars, chips, moles, freckles, with **side** and position.
12. **Asymmetries**: anything that differs left from right (a smile, a parting, a scar). Each must be stated in the character's own left or right.
13. **Distinguishers**: the three features, from the list above, that make this face unlike every other face in the cast. These three go into the identity key.

**Rules for distinctiveness.** Faces in AI generation drift toward an average attractive face. Features that survive drift are large and simple: hair color and style, facial hair, age lines, face width, brow shape. Features that do not survive are small and subtle: exact eye shape, a small chip, a faint scar. Put the large features in the identity key; carry the small ones through reference images and close-up checks.

### 3.3 Expressions: describe movement, tie to beats

An expression range is a list of five to eight named states for a principal (two or three for a minor character), each tied to a scene beat and each described as muscle movement plus eyes plus head, never as a bare emotion word.

| Instead of | Write |
|---|---|
| "shocked" | "brows lift (AU1 and AU2), upper lids rise (AU5), jaw drops slightly (AU26), head stops moving"; add "brows draw together (AU4)" only if the shock is fearful, because raised-and-drawn brows read as fear rather than surprise |
| "hurt" | "inner brows lift (AU1), lip corners pull down slightly (AU15), eyes drop to her hand" |
| "cold" | "face still, lips closed and relaxed, eyes level, no head movement while speaking" |
| "tries to smile" | "one lip corner pulls up (AU12, one side only), cheeks do not rise (no AU6), eyes stay flat" |

The last row is useful: a smile without the cheek raiser (AU6) is commonly read as polite or forced. Treat this as a viewing convention, not a truth test: research such as Krumhuber and Manstead (2009, *Emotion*) found that people can produce the cheek raiser deliberately, so its absence means "reads as forced", not "is false". Eli's "tries to smile" in sc28 can be written this way.

**Restraint rule.** If a beat's meaning is already carried by the line, the eyeline or the cut, then write the face as "still" or give it one movement only. Save two-or-more-movement expressions for the turning points listed in the expression range.

**Micro-expressions on screen.** Write them as a two-part beat: a flicker (a named movement lasting roughly a quarter to half a second) and a cover (the face resetting). Example for sc03: "the new beard makes his face strange; then one lip corner lifts (the crooked half-smile); the face holds it."

---

## 4. Costume for character

### 4.1 What costume carries

Deborah Nadoolman Landis designed Indiana Jones's fedora and jacket for *Raiders of the Lost Ark* (1981) and Michael Jackson's red jacket for *Thriller* (1983), and wrote *Screencraft: Costume Design* (Focal Press, 2003), *Dressed: A Century of Hollywood Costume Design* (HarperCollins, 2007) and *FilmCraft: Costume Design* (Focal Press, 2012). The running theme of her writing is that costume designers design characters, not fashion: the clothes belong to a person with a history. Two checked quotations: she has written that "a costume designer's job is to discover who the people are in the screenplay" (as quoted by the Berkeley Art Museum and Pacific Film Archive's program note, checked 2026-09-27), and she told the *Daily Bruin* in 2024, "Costume designers don't need to know how to sew, we need to know how to read." For this pipeline that means: every costume choice starts from a line of the text, not from a mood board. B4, Section 6.1, lists the costume variables (silhouette, color, texture, fit, wear, damage, coverage, marks on the body). This file adds the questions to ask of each variable:

- **Role and work.** What does their job put on their body? (Iona's work clothes, torch, knife; Saye's medical case; the guard's lanyard.)
- **Class and means.** What could they afford, and do they care?
- **History.** How old is each garment, and what has it been through?
- **Choice or imposition.** Did the character choose this, or did an institution put it on them? *The Catch* moves its principals from chosen clothes to imposed ones: hospital blanket, wristband, pressure suit, paper oversuits, a plastic tent.
- **Climate and task.** Is it right for the weather and the job? Wrongness should be a story fact, not an accident.

### 4.2 Color identity

Give each principal one color identity: a hue and a value that belongs to them, held scarce elsewhere in the frame so it keeps its meaning. B2 (Section 8) holds the film-wide color script; this file assigns people to it. Rules:
- The protagonist's color appears on nobody else in the same scene at the same saturation.
- Value separation first: in a dark scene, color identity is read through value (light shirt against dark brick) before hue.
- A color identity may pass to an object when the object carries the character (Iona's blue shirt strip in the collection room).
- Keep it to one garment or one area of the body. If the character's color covers them head to toe, then it stops being an identity and becomes a costume gimmick; mute the rest of the outfit toward neutral.
- The color must have a practical reason inside the story (a work shirt faded by washing, a flight suit in the standard color). If you cannot name one, then choose a different garment to carry the color.

### 4.3 Costume states and the costume plot

Film costume departments track clothes in a **costume plot**, numbering every change (B4, Section 6.1). For each character, list costume states (C1, C2, C3 ...) by story phase, and for each state note: garments, condition, color, marks, what the silhouette does, and the scenes it covers. On real productions, a hero costume is usually backed by several identical multiples, some pre-aged or pre-damaged in stages, so that stunts, blood and reshoots match; this is standard practice rather than a sourced claim here. The AI equivalent is one approved reference image per costume state (Section 7.3).

### 4.4 Continuity of damage

Damage is story. It must start where the text starts it, keep its side of the body, and change only when an event changes it. Write one **damage ledger** row per item, with the columns below. The ledger for *The Catch* follows (sides marked "rec." are recommendations; see Section 15):

| Item | Side | Starts | Changes | Ends |
|---|---|---|---|---|
| Iona's chipped tooth | upper left front (rec.) | sc02 "Runs her tongue over a front tooth and finds a new edge." | none | never; present in every later close shot of her mouth, at L0 (there, never pointed at; rule 24) |
| Iona's shirt sleeve | right (rec.) | sc06, torn on the sill as she catches it (B4 recommendation; the script says only, in sc07, "what is left of her shirt sleeve") | sc07 "pressing what is left of her shirt sleeve into Jude's shoulder"; sc09 "Eli twisted round, holding the sleeve on him"; sc10 comes off when "Saye cuts Jude's shirt away" [inferred]; sc17 leaves with "Jude's dressings, from a sealed bin" [inferred: this is how a strip that was never in the cage reaches the ship]; sc21 "a strip of blue cloth. The sleeve of her shirt, stiff with Jude's blood" in a container; sc25 clipped to the vessel | sc30 "The cloudy growth behind the scrap of shirt fills half the container now." |
| Jude's blood on Iona | both hands | sc06 to sc07 | sc12 "Iona looks at Jude's blood under her nails." | cleaned by sc18 (suit) [inferred] |
| Iona's palm | right (rec.) | sc06 "Her palm drags across the bright steel." | sc09 "her skinned palm opens"; sc11 dressed; bandaged; inside the glove sc18 to sc28 | sc30 bandaged, "in her lap" |
| Jude's shoulder | right [inferred, Section 10.2] | sc06 "a hole through his shoulder" | sc07 sleeve; sc10 Saye's dressing; sc17 "neater than the last"; sc28 "Blood comes through the paper" | sc29 "his arm strapped across his chest" |
| Jude's appendix scar | his own right, low on the belly (fixed by the script: "That's his right. The scar. It's where it should be.") | always there | seen only in sc10 | never changes; appears on his left in any era C shot (C2) |
| Jude's dressings | right shoulder | sc10 Saye's dressing | sc17 "Then Jude's dressings, from a sealed bin." (collected by the figure); sc21 "Bloody cloth." on the collection-room walls [inferred: the same dressings] | the collection room burns in sc24; not seen again |
| Eli's strapped wrist | side is a design choice | sc03 "one wrist strapped to the rail"; sc04 "You sent me a photograph of your wrist." | a red strap mark [inferred], fading | gone by sc20 [design choice] |
| Eli's feet | shoe on right (rec.) | sc04 "She gives Eli one shoe. He leaves the other." | sc06 shoe lost in the cage (rec.); sc21 "One shoe." in the collection room, among "The things from the cage. Found. Carried here." | socks, then hospital wear |
| Eli's beard | whole face | sc03 "a beard she has never seen" | none shown | to the end |
| White pressure suit | lettering | sc18 "Every word printed on it reads backwards to her." | engine, spare, vessel added | sc28 arrival |
| Paper oversuits | Eli, Jude, Nell | sc28 "Paper oversuits cover Eli, Jude and Nell." | blood through Jude's | sc28 |
| Figure's face cover | front | sc16 cracked, "A thin WHITE JET" | sc20 patched; sc23 strip dims | sc25 the "crescent dent", patch failing, sealed with tape |

### 4.5 Imposed costume as arc

When the story strips a character of chosen clothes, the silhouette usually loses the marks of identity (tools, work wear) and gains marks of institution (bands, labels, coverings). Design the loss visibly: keep one chosen element (Iona's ring; Nell's book) through the imposed states so the person is still findable inside them.

---

## 5. Body language and movement

### 5.1 Laban's effort factors

Rudolf Laban (1879 to 1958), a dancer, choreographer and movement theorist, described movement quality through four **effort** factors, each with two poles (Laban and F. C. Lawrence, *Effort*, Macdonald and Evans, 1947; Laban, *The Mastery of Movement on the Stage*, Macdonald and Evans, 1950, later revised by Lisa Ullmann as *The Mastery of Movement*):

| Factor | Question it answers | Poles |
|---|---|---|
| **Weight** | How much force? | strong / light |
| **Time** | How urgent? | sudden / sustained |
| **Space** | How focused is the attention? | direct / indirect |
| **Flow** | How controlled? | bound (held, could stop at any moment) / free (released, hard to stop) |

Combining weight, time and space gives the eight basic effort actions:

| Action | Weight | Time | Space | Screen use |
|---|---|---|---|---|
| **Punch** (also called thrust) | strong | sudden | direct | Iona swinging the drip stand; the oxygen cylinder |
| **Press** | strong | sustained | direct | Pressing the sleeve into a wound; holding a helmet still |
| **Slash** | strong | sudden | indirect | The figure throwing aside bed legs |
| **Wring** | strong | sustained | indirect | Eli twisting the stuck bottle cap |
| **Dab** | light | sudden | direct | Tapping the vessel's outline on the screen |
| **Glide** | light | sustained | direct | Iona's hand along the ropes; Saye's finger down the screen |
| **Flick** | light | sudden | indirect | The red tag whipping on the falling gate |
| **Float** | light | sustained | indirect | Iona's body "out behind her like washing"; the animal at rest |

**How to use it.** Give each character a home effort (their default), a stress effort (what they shift to under pressure), and a break effort (what they do when their defences fail). Change of effort across a scene is a beat you can see.

**Worked conversion (effort to instruction).** An effort name is for the designer; the performer or model needs the physical version. Iona's glide on the ropes becomes: "palm flat, hand slides slowly along the rope, even pressure, no pauses except where she checks, eyes ahead." Her punch with the drip stand becomes: "one fast, hard swing from the shoulders, straight at the glass, stops dead on impact." Every home, stress and break effort in Section 10 should be convertible this way; if it is not, it is too vague.

### 5.2 Chekhov's psychological gesture and imaginary centre

Michael Chekhov's *To the Actor: On the Technique of Acting* (Harper and Brothers, 1953) teaches the **psychological gesture**: "the actor physicalizes a character's need or internal dynamic in the form of an external gesture" (Wikipedia's summary, checked 2026-09-27). The actor rehearses one large, whole-body version of the gesture, then keeps only its inner pressure in performance. Chekhov also taught movement qualities, "molding, floating, flying, and radiating", used "to find the physical core of a character" (Wikipedia, checked 2026-09-27), and an **imaginary centre** (described in *To the Actor*; not re-checked against the text in this session): a point in or outside the body from which movement seems to start (in common teaching use, a centre in the chest reads open, one in the head reads cerebral, one low in the belly reads grounded).

For design, write one psychological gesture per principal as a single verb phrase. The small everyday gestures in the script should then look like shrunk versions of it. *The Catch* already does this; Section 10 names them.

### 5.3 Johnstone's status

Keith Johnstone's *Impro: Improvisation and the Theatre* (Faber and Faber, 1979) argues that every interaction contains small status moves, that status is something a person plays rather than a rank they hold, and that when one person raises their status the other is lowered, like a see-saw. His examples of high-status behavior include keeping the head still while speaking, holding eye contact comfortably, moving smoothly and taking up space; low-status behavior includes small head movements, touching the face, breaking eye contact and glancing back, and hesitation sounds before speaking (paraphrase from memory; not re-checked against the text in this session).

Design use:
- Status is not power. A captive (Eli, strapped to a bed) can play high status through knowledge; an authority (Saye) can drop status in one beat ("Saye has lost the voice she uses for answers").
- Give each principal a **status default** and mark the beats where it flips. The flip is often the scene's turning point.
- Self-lowering can be generous: Jude lowers himself with jokes ("Look at that idiot." / "I mean me.") to lift the others.

### 5.4 Lecoq: neutral, economy and tempo

Jacques Lecoq's teaching (*Le Corps poétique*; English edition *The Moving Body*, translated by David Bradby, Methuen, 2000) begins with the **neutral mask**, which "is symmetrical, the brows are soft, and the mouth is made to look ready to perform any action" (Wikipedia, checked 2026-09-27). The mask trains a body with no habits, calm, economical and present, so that everything a character adds can be seen as a choice. The "seven levels of tension", a scale from collapsed to rigid, is widely taught in the Lecoq tradition, but I could not confirm it in Lecoq's own book in this session.

Design use:
- Write each character's movement as **departures from neutral**: what they add (a lean, a held breath, a habitual hand) and what they never do.
- **Tempo** is a character trait. Decide each character's resting tempo and let scenes push it. When everyone speeds up and one person stays slow, that person holds the scene.

### 5.5 Proxemics per character

B3 (Section 4.2) gives Edward T. Hall's distance zones from *The Hidden Dimension* (1966), with the warning that they were drawn from North American adults and vary by culture. At character level, write two numbers: the **default distance** the character keeps in conversation, and the **closest distance** they allow, with the scene where that changes. Iona handles bodies at touching distance (lifting Eli, taking his face in both hands) but argues across glass; at the end she "brings her chair closer to the glass. He moves his to meet it."

### 5.6 Signature gestures

A signature gesture is a gesture the audience learns to recognise as belonging to one person, so that its repetition, change or **transfer** to another character carries meaning without words. Signatures can be repeated (Iona's flat hand on ropes, then on glass), moved (Eli's half-smile to "the wrong side of his face"), or handed on (the figure "puts its hand flat against its own chest"; Jude "Lays his good hand flat on it"). Rules: one signature gesture per principal that the camera is allowed to point at (other habits, such as Iona's counting or Eli's reading, are recorded under Hands and Eyes in the movement signature and played at L0); minor characters get none; and a signature is shown at most once per scene except in a payoff scene (Mistake 6). Others in *The Catch*: "Eli reads the tag on the wire. He reads everything."; "His other hand goes underneath. Behind Jude's back. Out of sight."; "Her lips move around the torch: counting."; "She can always outwait him." Each is assigned to its owner in Section 10, and Examples 1 and 2 (Section 11) show two of them designed in full.

*The Long Places* has its own: Melek "laid the flat of her hand on the sounding stone, and knocked twice, softly, and then stood in the waiting, two breaths entire"; Márton over the drill, "both hands flat on the frame like a man taking a pulse."

### 5.7 Writing a movement signature someone can reproduce

A movement signature has eight fields. Keep each to one line.

1. **Centre**: where movement starts (chest, hands, head, belly).
2. **Home effort** (Laban), plus **stress effort** and **break effort**.
3. **Tempo**: resting speed, in plain terms ("pauses about a second before answering").
4. **Default posture**: spine, shoulders, head, weight on which foot.
5. **Hands**: where they rest, what they do when idle.
6. **Eyes**: where they go first when entering a space.
7. **Signature gesture**: the habitual gesture, with the exact script line.
8. **What never moves**: the stillness that defines them.

Then add the **arc of movement**: how the signature changes, with scene numbers.

Write every line as observable instructions: body part, direction, speed, force, duration, and what stays still. "Iona moves confidently" is unusable. "Iona places each hand before shifting weight; hands flat and slow on surfaces she is judging; head still while working" can be performed, animated, keyframed in Blender (free 3D animation software; keyframing means setting a pose at chosen moments and letting the software fill the motion between), or prompted.

---
## 6. Non-human characters: frightening first, pitiable after, fair throughout

### 6.1 Precedents, stated only as far as checked

- ***Alien* (1979).** The creature's design is credited to H. R. Giger, from his lithograph *Necronom IV*; Carlo Rambaldi designed and built the mechanical head; the suit was worn by Bolaji Badejo, a "6 ft 10 in (2.08 m), rail-thin graphic designer", who "went to tai chi and mime classes to learn how to slow down his movements"; circus performers and several actors sharing one costume were tried first, but "neither proved scary"; Ridley Scott kept the creature largely unseen (Wikipedia, checked 2026-09-27). Lessons: a performer's real proportions (very tall, very thin) make a suit read as not-human; slowed, trained movement matters as much as sculpture; withholding the full view sustains fear.
- **The Daleks (*Doctor Who*, 1963).** Casings designed by BBC designer Raymond Cusick for Terry Nation's serial; in the fiction a mutant creature lives inside the armoured casing. Cusick "sought to create a design that made sure that viewers never saw how the Dalek moved". More of the mutant was planned to be shown, but this was dropped over cost and "concerns the mutant would be too terrifying"; as broadcast, it "was only seen briefly as a jelly-like substance" (Wikipedia, "Dalek", checked 2026-09-27). Lessons: a hard, frightening shell with a soft occupant is an established design pattern; hiding how a thing moves is itself frightening; and how much of the occupant to show is a deliberate choice.
- ***Men in Black* (1997).** Rick Baker's creature work included a reveal that "went from a man with a light under his neck's skin to a small alien hidden inside a human head" (Wikipedia, checked 2026-09-27). Lesson: the small-pilot-in-a-large-body reveal exists in comedy too; *The Catch* must play it for pity and awe, which means slower and more intimate staging.
- ***Pan's Labyrinth* (2006).** Guillermo del Toro's Pale Man, played by Doug Jones (who also played the Faun), has eyes in his palms, a feature shared with the Tenome (a creature from Japanese folklore whose name means "hand eyes"); "A bout of weight loss on del Toro's part inspired the physical appearance of the saggy-skinned Pale Man"; to see while performing, Jones "had to look out of the character's nostrils"; the film's creature makeup and animatronics involved DDT Efectos Especiales (Wikipedia, checked 2026-09-27). Lessons: the most frightening feature is often a human feature relocated or removed, and a design can grow from a real bodily observation (sagging skin after weight loss) rather than from other monsters. The figure's face, replaced by a moving pale strip, works the same way.
- ***Arrival* (2016).** The heptapods are "cephalopod-like, seven-limbed aliens" (cephalopods are the octopus and squid family; Wikipedia, checked 2026-09-27). Correction to a common shorthand: the heptapods were not designed by production designer Patrice Vermette. They were "designed by Carlos Huante" (Gizmodo, checked 2026-09-27), a creature designer who, as reported, handed clay maquettes (small sculpted models) to Denis Villeneuve and visual effects (VFX) supervisor Louis Morin before the effects company Hybride built them in computer graphics (CG); concept artist Peter Konig produced earlier alien designs from Villeneuve's reference photos of "cuttle fish, squids, microscopic organisms" (Gizmodo). Vermette designed the spaces, citing James Turrell's light works as a big influence on the meeting room aboard the craft; Rodeo FX, one of several effects vendors, "completed 60 visual shots" (Wikipedia). The film shows the heptapods almost always through a transparent barrier, in haze. Lessons: real animals (cephalopods) are better sources than other films' aliens; a barrier and a medium (haze, water, glass) let an audience look at something alien for a long time without the design breaking. *The Catch* has both: the animal is seen through glass and dark water.
- ***The Elephant Man* (1980).** David Lynch withholds Merrick's appearance (hooded, obscured) before the full view; Christopher Tucker's makeup took "seven to eight hours to apply each day"; the Academy's failure to honour it led to a separate makeup category (Wikipedia, checked 2026-09-27). Lesson: the sequence withhold, shock, then humanity turns fear into pity, and the shame belongs to the audience's first reaction. Note the ethical difference from *The Catch*: Merrick was a real disabled man; the figure is a machine, and its fear must not borrow from disability imagery.
- **Nature, for the animal [design reference].** Real deep-sea animals already look like the script's "Almost clear, like a thing from the bottom of the sea." Examples: comb jellies (jelly-like animals that swim with rows of beating hairs), glass octopuses, salps (see-through, barrel-shaped drifting animals), and the amphipod *Phronima* (a small crustacean), which lives inside the hollowed body of a salp or similar gelatinous animal. *Phronima* is the closest natural model for the story's idea: a small animal living inside, and moving, a much larger hollow body. These are references for texture and motion, not for copying. Caution for AI: comb jellies are known for rainbow shimmer along their comb rows and jellyfish pull in glowing bells and trailing tentacles; if you use these names in prompts rather than only in reference images, expect those features and check for them.

### 6.2 Rules for frightening first

1. **Silhouette before surface.** Show it first as a dark shape against something lighter (B2, rule 25: matte black reads only by its edges).
2. **Wrong proportions in a human plan.** Keep the human plan (two arms, two legs, upright) and make two or three proportions wrong: no neck, head sunk low, height above the door frame, hands too large.
3. **Remove or relocate one face feature.** No eyes; a pale strip that moves where eyes would be.
4. **Sound before sight.** "Behind her: a pump. Three uneven strokes." The ear finds it before the eye.
5. **Arrival without travel, in human rooms.** "It did not come through the door. It is simply there." In sc15 and sc16, cut it in; never show it walking in. On its own ship it does walk ("At the end of the chamber, something black comes into the light."; "Goes back the way it came.", sc20), and letting it walk there is part of making it familiar. So: if the scene is in the human world and the figure has not yet been seen to care, then no travel; if it is on the ship, then normal entrances.
6. **Scale against human objects.** Frame it with a door, a bed, a chair.
7. **Avoid the stock machine-monster.** If a design element would fit a famous robot or alien (a scanning light bar across the face, glowing eyes, chrome, exposed pistons, a skull-like head), then remove it. The pale strip in particular must not become a sweeping light bar: it is soft, pale matter behind glass, it moves with a pause, and it is never red.

### 6.3 Rules for pitiable after

1. **Show damage it suffers, not damage it causes.** The cracked cover, the white jet, the patch, the fluid gathering beneath it.
2. **Show care before explanation.** It lifts Jude's arm "As carefully as a nurse"; brings a tank of air for which "Someone has cut a new fitting for it, by hand"; straightens a container "a finger's width out of line"; catches a cup "without looking".
3. **Show it paying a cost.** It gives up its own cell ("The pale strip dims"); it braces against its burning cabinet.
4. **Invert the scale at the reveal.** Huge becomes "No longer than her hand"; opaque becomes "Almost clear"; hard becomes "a glass VESSEL of dark water".
5. **Give the small being a human-readable gesture.** "The animal presses a limb to its window. Pointing back."

### 6.4 Playing fair: the clue ledger

A fair reveal is one whose clues were visible the first time. Write a ledger, one row per clue:

| Clue | First shown | How to show it (emphasis level) | What it means on rewatch |
|---|---|---|---|
| Head "low between its shoulders" | sc15 | Silhouette, L1 | There is no head: the top houses a tube loop |
| Pale strip slides across, vanishes, returns | sc15 | L2, behind a clear cover | A flap of skin in a lit tube, not eyes; it moves on a cycle, not toward things |
| Pump, "three strokes, not quite even" | sc15 | Sound, L2 | "the only heart the big body has" |
| White jet; crust "turns to slush on the warm tile" | sc16 | L2 insert | Very cold water inside; "so cold it whitens" (sc25) |
| Faint frost at the edge of the cover [design choice] | sc15 onward | L0 | Same cold; visible only in rim light |
| A row of small flush latches down the centre front [design choice for how they look] | sc15, sc16, sc20 | L0 in rim light | "Latches let go, one after another, down the front of it" |
| A faint seam running from the edge of the face cover down into the chest [design choice] | sc15 onward | L0 | "The cracked cover lifts with the chest": the "face" is a window in the body's front hatch, not a head |
| It "raises one arm towards her" | sc16 | L2 (read as attack) | It was reaching to collect her, as it had just collected Jude (and, moments later, Eli's bed is gone) |
| Black cell "between its shoulders" | sc20 | L1 | It is a machine with a power socket, like Iona's harness |
| Catches a cup "without looking" | sc23 | L1 | [interpretation] The strip is not how it sees; its senses are somewhere we are not shown |
| Hands settle a fraction late after each move [design choice] | sc15 onward | L0, performance | A small operator works the big body |
| "The pale strip dims" when it removes its cell | sc23 | L1 | The strip is powered and lit, part of a system |
| Handmade air fitting | sc20 | L2 | It knows what a suit needs because it wears one |

Rule: every clue must be something a first-time viewer registers as strange, not something hidden. Strangeness now, sense later.

### 6.5 Moving a machine worked by a small body

The figure's big body is operated by the animal's limbs in sockets ("One fine limb draws itself out of a socket in the wall of the vessel. Far above, the enormous black hand goes dead and hangs."). So:
- **Two tempos.** Care tempo: glide and press, sustained and direct. Task tempo: "Then it moves, and it is fast": sudden and strong, and direct (punch) for every reach, lift and pull. Its only indirect movement is flinging things aside once they are dealt with ("Throws them aside."), which is a slash. Otherwise it never wanders or fidgets; its attention is always direct.
- **Hands are the expressive organ.** With no face, its thought shows in what its hands do and in the order of things its head turns toward (B4, Section 11.3).
- **Dead-weight tells.** When a limb withdraws, the corresponding part hangs by gravity. Use a small version of this early, once (a hand drops a few centimetres when it stands still) [design choice], as a fair clue.
- **Performer or previs.** Following the *Alien* lesson, if the figure is ever performed live or blocked with a stand-in for a control video, then use one very tall, thin performer moving slowly and deliberately, never two people or a bulky costume; the body should look carried, not inhabited.

---

## 7. Designing for AI consistency: the character bible entry

### 7.1 Entry format

Every character gets one entry with these fields, in this order:

```
NAME / ROLE:          narrative role in one line
ARC:                  start state -> end state, with the turning scene
DESIGN THESIS:        one sentence (Section 2.6)
ONE IMAGE:            the single frame that carries the thesis (Section 2.6)
EVIDENCE:             quoted lines from the text about look and movement
FACE:                 the 13-field face specification (Section 3.2)
BODY / SILHOUETTE:    height, build, proportion, posture, dominant shape
COSTUME BY PHASE:     C1, C2 ... with scenes, garments, condition, color
DAMAGE LEDGER:        rows (Section 4.4)
COLOR IDENTITY:       hue + value, and where it must not appear
MOVEMENT SIGNATURE:   the 8 fields (Section 5.7) + arc of movement
PSYCHOLOGICAL GESTURE: one verb phrase
STATUS:               default, and the beats where it flips
PROXEMICS:            default and closest distance, with the scenes where they change (Section 5.5)
EXPRESSION RANGE:     5 to 8 states (minor characters 2 to 3), each tied to a scene
MIRROR STATE:         NORMAL/MIRRORED by era (C2, Section 7.3), with every left/right feature
IDENTITY KEY:         25 to 40 words, fixed
STATE LINES:          one short phrase per costume state
REFERENCES:           list of approved images: portrait, turnaround, expressions, hands/marks, states
```

### 7.2 Identity key rules

1. **25 to 40 words** (minor characters may use 20 to 30). Suggested order: name, age read, build, skin placeholder, hair, face distinguishers, one costume anchor if constant, one mark if large enough to survive. Once a key is approved, its word order is frozen too.
2. **Only visible nouns and adjectives.** No meaning words ("symbolic", "haunted"), no backstory, no movement systems, and **no expression words** ("composed", "neutral expression", "smiling"): expression changes shot by shot and belongs in the shot prompt, so a fixed expression in the key fights every beat that needs a different one.
3. **Pasted unchanged** into every prompt. C3 quotes Google Cloud's video guidance: "Copy and paste the entire, unchanged character description into your prompt for every new scene or action." (as quoted in C3; my own fetch of that page on 2026-09-27 did not return its body text). A synonym is drift in word form.
4. **State lines change; the key does not.** Append the scene's state line after the key ("... right palm bandaged in white gauze").
5. **Sides: record in the body's terms, prompt in the frame's terms, fix by editing.** In the bible, every side is the character's own left or right in their designed (NORMAL) state; the state lines in Section 10 use this form unless marked otherwise. When a shot prompt needs a side, convert it: if the character faces the camera, their own right appears on the left of the frame; if their back is to the camera, their own right is on the right of the frame; if the character is MIRRORED in that era, swap sides first, then convert. Models are unreliable with sides either way (Section 14), so the dependable fix is to generate the character as designed and flip or edit the image, then check by eye.
6. **Distinct keys across the cast.** No two keys share hair color plus age band plus build. Designed kinship is the one exception (Iona and Eli share dark hair, the thirties and a slight build); then at least two large features must separate them (here Eli's beard and his hair over the ears against her low knot), and they must never be generated in one image without both references attached.
7. **Fix apparent sex and age band in every key, even where the script is silent.** A key that leaves them open lets the model choose again in every shot, which is drift by design. Put the placeholder in the key, and record outside the quotation marks that it is a placeholder for the user to confirm.
8. **Say what is there, not what is absent.** Write "a low domed head sunk deep between high shoulders", not "no neck"; negative words can add the thing they name (Section 14).

### 7.3 Sheets to make

Animation studios have long solved the same problem with the **model sheet**, a document "used to help standardize the appearance, poses, and gestures of a character" so that many artists' drawings do not go "off-model", the studio term for a drawing that departs from the approved design (Wikipedia, "Model sheet", checked 2026-09-27). Studios also sculpt maquettes (small statues of the character) so every artist can see the form from any angle; the AI-era equivalent is a simple 3D model turned in Blender (C4). An AI pipeline needs the same thing, because every generation is a new artist. Following C2, Section 6.2: a hero portrait (the identity anchor), a turnaround (front, three-quarter, side, back), an expression sheet tied to the expression range, a **hands and marks** sheet for every left/right feature (rings, the palm, the tooth, the smile), and one full-body image per costume state. For non-human characters, add a **scale sheet** (the figure beside a standard door, bed and Iona) and one image for each costume state.

**How to make each sheet so it is usable as a reference** [working practice, not a sourced standard]:
- **Turnaround.** One image per view (front, three-quarter, side, back), not one crowded sheet, because models copy crowded sheets badly. Same neutral standing pose (arms slightly away from the body so the waist and hands read), same flat, even, low-shadow lighting, plain mid-grey background, camera at chest height with a normal lens (about 50 mm full-frame equivalent), whole figure in frame with a little space above the head and below the feet. Costume: the character's first costume state. For the figure, add one view in rim light only, because that is how the audience first sees it.
- **Expression sheet.** Head and shoulders, front and three-quarter, same light as the hero portrait, one image per expression-range entry, each labelled with its scene number and its written movement description (Section 3.3), never with an emotion word alone.
- **Hands and marks sheet.** Close images of each side-dependent feature on the correct side of the NORMAL design, labelled "own left" or "own right": Iona's ring hand and skinned palm, her chipped tooth, Eli's half-smile and parting, Jude's ring hand and appendix scar.
- **Costume-state images.** Full body, front, same pose and light as the turnaround, one per state; for damage states, edit the previous approved image rather than generating fresh (Section 7.4).
- **Approve before use.** An image becomes a reference only after the user or the checklist (Section 12) has passed it; unapproved images are never attached to shots.

### 7.4 Reference-image strategy

- Attach the hero portrait to every shot where the face is readable; attach the relevant costume-state image for full-body shots.
- For mirrored eras, make the MIRRORED references by flipping approved NORMAL images in an editor, never by prompting "mirrored"; then fix any text that must still read correctly (C2, Section 7.2).
- For damage, edit the base image ("same person, same pose, now with ..."), so the face stays anchored while the state changes.
- Keep the references model-neutral (images plus words), so they survive a change of tool.
- If the tool accepts only one reference image, then attach the hero portrait when the face will be larger than about a tenth of the frame height, and the costume-state image otherwise.
- If two characters share a shot and the tool accepts several references, then attach one reference per character and name each character in the prompt in the same order as the references; if it accepts only one, then generate the characters separately and composite them (combine them into one image in an editor), or generate the shot and repair the second face by editing.
- If the character has no face (the figure) or no human face (the animal), then its hero reference is the silhouette and scale sheet, not a portrait.
- If a reference image contains text, a ring, or any side-dependent feature, then check it after every flip, because a flipped reference carries its errors into every shot.

### 7.5 Honest limits

- **Faces drift** across separate generations, even with references; C2 (Recipe R7) sets a drift check after every batch.
- **Small asymmetries flip or vanish**: a one-sided smile may render on either side or as a full smile; a ring may jump hands. Check every shot that depends on a side.
- **Similar characters merge.** Two men of similar age and build in one frame can swap features. Strong ensemble contrast (Section 2.5) is also a technical defence.
- **Hands, teeth and fine marks** are weak points; plan inserts from edited stills instead of hoping the video model keeps them.
- **Non-human designs regress to the familiar**: an original creature tends to become a generic robot, a diver, or a glowing jellyfish. Strong references and material words help; a LoRA (a small add-on trained on a few dozen approved images of the design; C2 Section 3.4) may be needed for the figure.
- **Identity keys do not guarantee identity.** A pasted key reduces variation; it does not stop it. Expect to reject a share of generations and budget for it; C2's drift check decides which.

---

## 8. Translation table: story meaning to design choices

| Story meaning | Face | Body and silhouette | Costume and color | Movement |
|---|---|---|---|---|
| Competence, craft | Attentive, still eyes; little facial motion while working | Built by the work (forearms, calluses) | Worn, fitted work clothes; tools on the body | Economical; hands arrive before eyes finish; direct, sustained |
| Hidden knowledge, a secret | Eyes go to text and objects first; a pause before speech | One limb often out of sight | Pockets, a coat that covers the hands | Bound flow; the hidden hand; stillness while others move |
| Warmth that deflects pain | Laugh lines; mobile brows | Rounded, heavy, loose | Soft, earth-colored fabrics | Free flow, light; self-lowering status with jokes |
| Control over grief | Unmoving face; level eyes | Vertical, narrow, upright | Grey, closed, everything fastened, dressed at 4 a.m. | Direct, quick hands; head still; the break is a lean |
| Captivity, time lost | New beard, pallor, thinness | Knees fold; wrists thin | Clothes from before, now wrong; one shoe | Slow to rise; careful with weight |
| Institution takes over a person | Hair covered, face partly hidden | Silhouette smoothed out | Blanket, wristband, oversuit, tent; names printed on them | Moved by others; told where to sit |
| Cost paid | A mark that stays (chipped tooth) | A limb out of use | Torn, bloodied, bandaged; damage on one side | Guarding the hurt side |
| Dread of the unknown | No face, or a face feature replaced | Human plan, wrong proportions | Uniform matte black; seams so fine they read only in rim light | Arrives without travel; purposeful, never idle |
| Pity for the feared | The replaced feature revealed as fragile tissue | Scale inverted: small inside big | Clear, wet, cold instead of black, hard, dry | Shrinking, winding, holding on |
| Kinship | Shared brow line or eye color | Different builds | Different color identities | One shared gesture |
| Mirror, estrangement | A one-sided smile on the wrong side | A ring on the wrong hand | Text on clothes that reads backwards | Hands reaching the wrong way (gearstick, bottle cap) |
| Reconnection | Faces at the same height | Bodies level, facing | The same imposed clothing on both | Chairs moved closer; hands flat on the same glass |

**How to use the table without producing stock images.** Each row is a menu of conventions, not a recipe. Rules:
1. For any one character, let at most one column carry a row's meaning strongly and keep the other columns ordinary. Grey clothes plus an unmoving face plus a rigid spine plus a buttoned collar is a poster of "control"; pick the two the text supports (for Saye, "grey and tidy" and "fully dressed at four in the morning") and let the rest be a normal woman in her fifties.
2. Every choice taken from the table must be traceable to a line of the text or marked [design choice] with a practical reason.
3. If a row's convention would make the character's moral role readable at first sight (villain, victim, saint), then drop it unless the story wants that first read and later overturns it.

---
## 9. Decision rules

1. **If** the text gives one physical detail for a character, **then consider** building the design outward from that detail, **because** the writer chose it as the handle (Jude "easy in the shoulders"; Melek "built like a doorpost").
2. **If** a late scene depends on a left/right feature, **then** fix the side in the earliest scene and show it at L0 or L1, **because** a change cannot be seen without a baseline (Jude's ring; Eli's smile).
3. **If** two principals share most of their scenes, **then** make them differ in at least three lineup columns, **because** audiences and models both confuse similar figures.
4. **If** characters are blood relatives, **then consider** one or two shared face features with different builds and color identities, **because** kinship should read without dialogue.
5. **If** a character withholds, **then** give the withholding a place in the body (a hidden hand, sleeves over the hands, a pause before speech), **because** subtext needs something visible to sit in.
6. **If** a character's arc is loss of control, **then** start them fully composed and let one element break at the turning point, **because** one change reads louder than general disorder.
7. **If** the story imposes clothing, **then** keep one chosen element visible through it (a ring, a book), **because** the person must stay findable inside the institution's costume.
8. **If** a character is injured more than once, **then** keep the damage on one side and a clean side for emblems, **because** continuity and emblem legibility both depend on it (B4, 6.2).
9. **If** a costume item later becomes a prop (the sleeve strip, the shoe), **then** design it once, as the same object in the same state, **because** the audience recognises it by color and shape.
10. **If** a character must frighten and later earn pity, **then** build fear from silhouette, sound, scale and arrival, and pity from damage suffered, care shown and cost paid, **because** fear built on cruelty cannot be reversed.
11. **If** a reveal is coming, **then** list every clue with its scene and make each strange rather than hidden, **because** a fair reveal rewards the second viewing.
12. **If** a character has no face, **then** give its thinking to head direction, hands and the order of its looks, **because** the audience still needs to see it decide.
13. **If** a small creature must become a person to us, **then consider** a gesture that echoes a human gesture already in the film, **because** the echo does the work a face would do.
14. **If** the text says a character looks older or younger than their age, **then** design the gap from a cause the story names (captivity, no sun, the wrong food), **because** unexplained ageing reads as makeup.
15. **If** a character holds high status by stillness, **then** make their break a single movement toward something, **because** the audience measures change against the baseline (Saye leaning to the screen).
16. **If** a character jokes under pain, **then** keep the face loose and the body guarded, **because** that contradiction is the character (Jude).
17. **If** a signature gesture recurs, **then** keep its hand shape and framing constant and change one thing each time (who does it, what it touches), **because** recognition must come before the change can be felt.
18. **If** prose describes a person by metaphor, **then** convert the metaphor into shape, proportion and posture, and keep the metaphor in the design thesis only, **because** models draw metaphors literally.
19. **If** the text is silent on ethnicity, skin tone or body type, **then** leave it open, use a marked placeholder, and ask the user, **because** these are casting decisions with consequences.
20. **If** a minor character exists as a function, **then** design one read and one key prop, **because** detail spends attention the story has not given them.
21. **If** a character will be generated across many AI shots, **then** put the three largest distinguishers in the identity key and carry small features through references and inserts, **because** small features do not survive drift.
22. **If** a movement must be exact (a puppeteered hand, a slow fall, a mirrored reach), **then** plan it as Blender previs or a control video (C4) rather than words, **because** words control movement quality weakly.
23. **If** the text states a feature, **then** never contradict or "improve" it; **if** it states nothing, **then** keep the invented feature ordinary unless it serves the design thesis, **because** every invented distinctive feature competes with the ones the writer chose.
24. **If** a detail can be read only when the camera points at it (a chipped tooth, a small scar), **then** keep it out of the identity key, carry it by reference image and insert, and show it at L0 after its first appearance, **because** pointing at a mark repeatedly turns cost into decoration.
25. **If** a design element exists only to symbolise (a white suit as purity, black as villainy), **then** give it a practical reason inside the story or drop it, **because** audiences read unexplained symbolism as the film talking down to them.
26. **If** a character is non-human and must frighten, **then** check the design against famous creatures and robots and remove anything that matches (Section 6.2, rule 7), **because** a familiar monster is frightening only as a quotation.

---

## 10. Character design entries for *The Catch*

Scene numbers sc01 to sc30 follow the script's headings in order, as in A2, B1 to B4 and C2. Eras A, B and C are C2's mirror eras: A runs to the black after the cage's "CLACK" in sc06; B runs to Iona's own turn in sc27; C is sc28 to sc30. Casting-type choices (ethnicity, skin tone) are open everywhere; skin tones in identity keys, where given, are placeholders taken from C3, Section 22.0, so the library stays consistent until the user decides. These entries supersede C3's illustrative keys.

### 10.1 IONA VALE (late thirties)

- **Role.** Protagonist. A lift engineer [inferred: "the way she has come round a thousand cages"; "the way it has come up after her for fifteen years"]. Eli's sister; Jude's wife [inferred from the matching rings in sc29].
- **Arc.** From the one who tests and catches everything with her own hands, and demands to be told, to one who deletes her way home to contain the fire and carries a stranger out; ending able to sit with Eli without an answer. Turning scene: sc24 ("She deletes the way home.").
- **Design thesis.** Iona must read as a body made by work, all verticals and straight lines, whose hands know things before she does; the story strips away her tools and clothes until only the hands and the choice are left.
- **One image (Section 2.6).** sc01: standing at the cage in the faded blue shirt, her hand laid flat on the ropes, her eyes not on the hand but up the dark shaft.
- **Face.** Reads her age. Long face, defined cheekbones, straight strong jaw. Deep-set grey-green eyes, level; straight, low, dark brows (shared with Eli) [design choice]. Straight nose. Wide mouth, thin lips, resting closed. Weathered skin. Dark brown hair in a low knot, loose strands at the temples; no make-up. Mark: chipped front tooth from sc02 [side: upper left central incisor, design choice]. **Distinguishers:** straight low brows, deep-set pale eyes, low knot with loose strands.
- **Body and silhouette.** Medium height (about 1.68 m) [design choice], lean, strong forearms and shoulders; knees soft, weight low; "A practised lift": she lifts with her legs. Dominant shape: vertical rectangle. From sc18 the engine "between Iona's shoulders" makes her top-heavy, echoing the figure's "second black cell locked between its shoulders" (sc20) [inferred rhyme; design both blocks alike]. From sc25 the vessel on her chest.
- **Costume by phase.** **C1** (sc01 to sc06): faded mid-blue cotton work shirt, sleeves rolled to the elbow [design choice], dark grey canvas work trousers, scuffed brown work boots, belt with folding knife ["She cuts the strap": inferred] and pouch, radio earpiece in the left ear ["in her ear": side is a design choice], plain gold ring on her left hand, hand torch. **C2** (sc06 to sc10): right sleeve torn away (B4 recommendation), right palm skinned, Jude's blood on both hands and under the nails. **C3** (sc11 to sc17): pale grey hospital pyjamas [design choice], blanket stitched "OSTREL" (backwards), wristband with her name backwards, right palm dressed then bandaged; blood still under her nails in sc12. **C4** (sc18 to sc27): white pressure suit whose lettering reads backwards to her, harness and black engine between the shoulders, wrist display, suit camera with red light, visored helmet, roll of repair tape; spare engine on the hip (sc23), then on the back (sc25); the vessel strapped to her chest (sc25 onward). **C5** (sc28): same, helmet on ("Leave it on."). **C6** (sc29, sc30): clear plastic tent; pyjamas; bandaged right hand.
- **Color identity.** Faded mid-blue, mid-light value against dark brick; then suit white. No other character wears that blue; stitch the blanket's "OSTREL" in dark navy so it reads as the institution's, not hers [design choice].
- **Movement signature.** Centre: hands and forearms. Home effort: glide and press (direct, sustained, bound). Stress effort: punch (drip stand, cylinder), then sudden stillness ("She goes still."). Break: loss of words ("She opens her mouth. Nothing in it."). Tempo: steady, counted ("Her lips move around the torch: counting."). Posture: upright, even weight. Hands: flat on whatever she is judging; never in pockets. Eyes: structure first (rails, ropes, gate, brackets), then people. Signature: "Lays her hand flat on the ropes, the way a vet feels along a dog's ribs." Never moves: her head while she works. Arc: hands that test (sc01), hands that hold people (sc07, "takes his face in both hands"), hands that wait (sc25 "keeps her hand where it is until the thread stops"; sc30 "Folds it. Waits").
- **Psychological gesture.** Pressing a flat hand onto something to feel whether it will hold.
- **Status.** High in her work (still head, short orders: "Get in when I call it."). Drops once, with Eli (sc13). Level at the end.
- **Proxemics.** Default about 1 m in talk [design choice]; touching distance whenever a body needs handling ("She takes his weight with her legs, not her back."; "She takes his face in both hands", sc07). From sc11 she is kept behind glass, so her closeness becomes hands on glass (sc12, sc17). Closest chosen approach to the figure: "Iona walks up to it. The closest she has been." (sc23). End: "She brings her chair closer to the glass. He moves his to meet it." (sc29).
- **Expression range.** (1) sc02 pain held: "Her jaw shuts on the torch", eyes squeeze shut [design choice], no sound; then the tongue moves behind the lip, finding the tooth. (2) sc03 recognition: eyes fix, no smile, then action. (3) sc10 the mint, "Her face changes.": chewing stops, upper lip lifts slightly, brows draw together. (4) sc13 "Nothing in it.": lips parted, no sound, eyes drop to her palm. (5) sc24 the choice: face still, eyes on the flask inside the outline. (6) sc28 "Nothing but breath": mouth open, eyes on the sign, reading it again. (7) sc29 "Cannot quite look at him while she swallows."
- **Mirror state.** Never flips (C2).
- **Identity key (32 words).** "Iona, a lean, strong woman in her late thirties, weathered fair skin, dark brown hair in a low knot with loose strands at the temples, straight low dark eyebrows, deep-set grey-green eyes." ("fair" is the C3 skin placeholder, for the user to confirm. The ring goes in the state lines, because it is hidden under a glove in C4 and C5. The chipped tooth stays out of the key by rule 24 and is carried by the hands-and-marks sheet.)
- **State lines.** C1 "faded blue work shirt with sleeves rolled to the elbow, dark grey canvas work trousers, scuffed brown boots, plain gold ring on her left hand". C2 "right shirt sleeve torn away, right palm raw, dried blood on both hands, plain gold ring on her left hand". C3 "pale grey hospital pyjamas, right palm bandaged in white gauze, plastic wristband, plain gold ring on her left hand". C4 "white pressure suit, clear-visored helmet, a black box-shaped engine on a harness between her shoulders" (+ "a glass vessel of dark water strapped to her chest" from sc25).

### 10.2 JUDE (forties)

- **Role.** Iona's husband [inferred] and partner on the job; the group's warmth and wit; the wounded body that raises the stakes and is taken by the figure.
- **Arc.** From easy helper, to wounded and carried, to the one who catches her in sc28 ("He catches her by the harness. His bad shoulder gives.") and then lets go on purpose ("He takes it away."), leaving Iona and Eli facing each other.
- **Design thesis.** Jude must read as big, loose and warm, a body at ease in itself, so that when he is shot the ease goes out of the film, and his jokes from a stretcher read as courage.
- **One image (Section 2.6).** sc01: turning the red tag to the torchlight, weight on one hip, olive jacket open, the ease that the next hour takes from him.
- **Face.** Broad face, full cheeks, laugh lines at the eyes, warm brown eyes, mobile brows [design choices]; short brown hair greying at the temples; a few days' stubble. Mark: "an old white scar low on his belly", on his right side [inferred: "That's his right. The scar. It's where it should be."]. **Distinguishers:** broad face with laugh lines, grey-flecked short hair, stubble.
- **Body and silhouette.** Tall and broad (about 1.85 m) [design choice], heavy but soft-edged, shoulders low and loose. Dominant shape: rounded rectangle (circle family), wider and rounder than Iona. After sc06, one arm held in; from sc29 strapped across the chest.
- **Wound side [inferred].** In sc29 he lays "his good hand" on the glass and it carries his wedding ring. With the ring on his own left hand (B4 rule), his good hand is his left, so he is shot through the **right** shoulder. In era C he is MIRRORED: on screen the ring shows on his right hand and the strapped arm is his apparent left.
- **Costume by phase.** **C1** (sc01 to sc06): olive canvas work jacket over a grey T-shirt, dark jeans, work boots, ring on the left hand [jacket and T-shirt from C3; jeans a design choice]. **C2** (sc06 to sc09): jacket open, T-shirt soaked at the right shoulder, Iona's blue sleeve pressed into the wound (her color in his wound). **C3** (sc10): shirt cut away, the scar visible, Saye's dressing. **C4** (sc11 to sc23): hospital pyjamas; dressing; on the ship "A fresh dressing on his shoulder, neater than the last." (sc17), and in sc20 "Jude lifts his bandaged arm an inch off the blanket." / "Whatever it is, it stitches better than she does." **C5** (sc28): paper oversuit, blood coming through at the shoulder. **C6** (sc29, sc30): arm strapped across the chest.
- **Color identity.** Olive and khaki, mid value; blood reads dark red against it.
- **Movement signature.** Centre: chest and shoulders. Home effort: free flow, light, indirect (a loose float). Stress: collapse ("He sits down into Eli"), then bound guarding of the right side. Break: the humor stops (sc15, "(a whisper) Iona?"). Tempo: unhurried; lets others go first ("At the shaft, Jude holds the cage gate open with his foot."). Posture: weight back, leaning on things. Hands: loose and open; after the wound the good hand does everything. Eyes: on Iona ("Beside her, Jude watches her watch it."). Signature: the joke delivered lying down. Never: hurries. Arc: loose, then one-armed, then steady (sc29, "Lays his good hand flat on it.").
- **Psychological gesture.** An open hand reaching to hold someone, then opening to let them go.
- **Status.** Lowers himself to lift others ("Look at that idiot." / "I mean me."). One high beat in sc28: "Other shoulder, Io."
- **Proxemics.** Close and physical by default, leaning on things and people [design choice from "easy in the shoulders"]; wounded, he is handled at touching distance by everyone. His one chosen distance is the end of sc28: "He takes it away." Then his hand on the glass in sc29.
- **Expression range.** (1) sc01 "I know how a lift works, Io.": brows up, a small closed-mouth smile, even on both sides (the one-sided smile belongs to Eli alone). (2) sc06 "(quite softly) Oh.": face slackens, no fear yet. (3) sc10 "They didn't let me watch.": dry, pale. (4) sc13 watching Iona, not the screen. (5) sc15 whisper: eyes wide, searching. (6) sc28 looks at his hand on her harness, then removes it: a decision.
- **Mirror state.** A: NORMAL. B: NORMAL (turned with Iona). C: MIRRORED.
- **Identity key (32 words).** "Jude, a tall, broad man in his mid-forties with loose, relaxed shoulders, a broad face with laugh lines, warm brown eyes, short brown hair flecked with grey, and a few days' stubble." (Ring side goes in the state line, because it changes on screen in era C.)
- **State lines.** C1 "olive canvas work jacket over a grey T-shirt, dark jeans, plain gold ring on his left hand". C2 "grey T-shirt soaked dark red at the right shoulder, a blue cloth pressed into the wound". C5 "white paper oversuit, a red stain spreading at the shoulder". C6 (era C) "his left arm strapped across his chest, plain gold ring on his right hand" (as the audience sees him, MIRRORED; this is the one state line written in on-screen terms, matching the script's "On his right hand"). Frame check when he faces the camera: the ring hand is on the left of the frame and the strapped arm on the right of the frame. Safest route (rule 5): generate him as designed (ring on his left hand, right arm strapped) and flip the image, then check by eye. For the profile two-shot (one frame holding both people, here seen side-on) through the glass that B1 (Example 6) proposes, the ring hand is the hand he lays flat on the glass, meeting Iona's ringed left hand.

### 10.3 ELI (thirties)

- **Role.** Iona's brother [stated: "Your brother sent me enough to stop this one."; probably younger, by the ages given]. A scientist who made a medicine from a culture, refused to "turn" it, and was held in the factory. He keeps the story's secret (the puck) and makes its key choice for others.
- **Arc.** From the man who decides for everyone and hides it ("His other hand goes underneath. Behind Jude's back. Out of sight."; "Drive.") to confession ("You did that." / "Yes.") to obedience ("Go." / "He stops.") to sharing a meal without an answer.
- **Design thesis.** Eli must read as a thin, watchful reader whose hands are always doing something we cannot see; captivity is written on his body, and the only warmth on his face is a smile that lifts on one side, which the ending moves to the wrong side.
- **One image (Section 2.6).** sc03 through the glass: on the bed with the beard, the strapped hand lifted as far as the strap allows, the smile lifting one corner of his mouth.
- **Face.** Early thirties, looks older from captivity; long narrow face, hollow cheeks, pale. The script gives "a beard she has never seen": untrimmed, dark, a few weeks old. Dark hair grown over the ears, parted on his own left [design choice: a second left/right check]. Grey-green eyes and straight low brows like Iona's [design choice], more mobile than hers. Thin mouth, resting slightly pressed. The crooked half-smile lifts the corner on his own left [design choice]. **Distinguishers:** untrimmed dark beard, hollow cheeks, hair over the ears.
- **Body and silhouette.** About 1.78 m, thin, narrow shoulders, slight forward curve of the upper back (reading and bench work) [design choice]; weak knees in sc04 ("His knees fold."). Dominant shape: thin angular lines, all elbows and knees; used for instability, never as villain coding.
- **Costume by phase.** **C1** (sc03, sc04): his own clothes worn for days [design choice; the script gives him a coat: "Iona hauls him up by the back of his coat"]: creased pale shirt, dark trousers, long charcoal wool coat, socks; a red strap mark on the strapped wrist [inferred from "one wrist strapped to the rail" and "You sent me a photograph of your wrist."]. **C2** (sc04 to sc06): one shoe ("She gives Eli one shoe. He leaves the other."). **C3** (sc07 to sc10): the flask in his fist, Jude's blood on his coat sleeve; one shoe or none (see Section 11, Example 4). **C4** (sc11 to sc23): hospital pyjamas. **C5** (sc28): paper oversuit. **C6** (sc29, sc30): pyjamas.
- **Color identity.** Dark charcoal grey. Saye's grey is deliberately related but lighter: the two keepers of secrets share a hue and differ in value [design choice].
- **Movement signature.** Centre: head and eyes. Home effort: bound flow; light and indirect while thinking, direct when he acts (he "crawls to the cabinet"). Stress: wring (the stuck bottle cap) and the hidden hand. Break: sc13, "Tell me that's what you'd have wanted." Tempo: a pause of about a second before answering, eyes down ("Eli thinks before he answers. He always does."). Posture: head slightly ahead of the shoulders. Hands: holding something (flask, cap, tray) or out of view. Eyes: to text first ("He reads everything."). Signature: the crooked half-smile. Never: explains unasked. Arc: from the hidden hand (sc06) to hands in view that he looks at (sc29, "He looks down at his hands.").
- **Psychological gesture.** Closing a hand around something and drawing it behind the body.
- **Status.** Low body status (strapped, crawling, carried), high information status. Flips when Iona outwaits him ("She can always outwait him.").
- **Proxemics.** Keeps back and watches, about 1.5 m, reading rather than approaching [design choice]; closest in action, not affection (his arm round Jude in sc06). Closest in feeling: "He steps into Nell's room. She makes space for him on the bed." (sc23); "He takes a step towards her too." before Saye's hand stops him (sc28); the chairs meeting at the glass (sc29).
- **Expression range.** (1) sc03 the half-smile through glass. (2) sc09 "the way you look at a result you expected": eyes track the signs, no surprise. (3) sc09 "He looks down at the flask in his hand for a long time." (4) sc13 "Yes.": no flinch. (5) sc23 asks her question back: "Are we going to be all right?" (6) sc28 tries to smile: one lip corner lifts, cheeks do not rise, on the wrong side. (7) sc29 "He takes that in."
- **Mirror state.** A: NORMAL. B: NORMAL. C: MIRRORED (smile and parting both appear on his right).
- **Identity key (31 words).** "Eli, a thin man in his early thirties, pale, with hollow cheeks, an untrimmed dark beard, dark hair grown over his ears, straight low dark eyebrows and grey-green eyes, slightly stooped."
- **State lines.** C1 "long charcoal wool coat over a creased pale shirt, dark trousers, socks, one wrist strapped to a bed rail". C2 "one brown shoe on his right foot, a sock on the other" [side: design choice]. C4 "pale grey hospital pyjamas". C5 "white paper oversuit".

### 10.4 DR SAYE (fifties)

- **Role.** "I inspect their trials." She has also "sent people across", including Nell ("I sent her."). Mentor, gatekeeper, the voice of containment; an antagonist by necessity (she burns the collection room while Iona is aboard).
- **Arc.** From the woman who holds answers and times their release, to cracked ("Saye has lost the voice she uses for answers."), to honest ("You knew I was still there." / "Yes."), to taking Nell's hand toward a window.
- **Design thesis.** Saye must read as grey, vertical and fully fastened, a person who has been dressed and waiting for years; the only living thing she keeps is a pot of mint, and the only time her body leans is toward Nell.
- **One image (Section 2.6).** sc10: in her doorway at four in the morning, buttoned to the collar, looking past the three bloodied people at the flask.
- **Face.** Late fifties [design choice within the script's "fifties"]; long oval face, fine lines, pale; grey eyes, level; thin straight brows; short neat grey hair parted on her own right [design choice; "grey and tidy" may describe her hair, her clothes or both]; mouth closed and relaxed at rest. Wedding ring on her own left hand (so it shows on her right in era B: "Saye's wedding ring. On her right hand."). **Distinguishers:** short neat grey hair, long pale lined face, thin straight brows. (Her composure is performance, not a face feature: it goes in the movement signature and the shot prompts, never in the key.)
- **Body and silhouette.** Slim, upright, about 1.65 m; spine straight, shoulders level; "quick flat hands". Dominant shape: narrow vertical rectangle, smooth and closed. The protective hood (sc18, sc28) enlarges and softens the head.
- **Costume by phase.** **C1** (sc10): "fully dressed at four in the morning": light grey cardigan buttoned to the collar over a white blouse, dark grey trousers, flat black shoes [design choices]; medical case, stethoscope. **C2** (sc11 to sc17): the same palette, same fastening, facility badge [design choice]. **C3** (sc18, sc28): protective hood and gown over the same clothes. Her clothes never loosen; her change is in movement [design choice].
- **Color identity.** Light cool grey and white; mint green as her single living accent (sc10).
- **Movement signature.** Centre: hands. Home effort: direct; quick and light when working ("works down his chest with quick flat hands"), otherwise still and bound. Stress: stillness, "looking at nothing." Break: the lean, "Leans in until her face is almost on the screen." Tempo: fast hands, slow body. Posture: upright, head still while speaking. Hands: flat, used to stop or hold (catches Iona's elbow; holds the tray; "puts her free hand between them"). Eyes: on the thing of risk (the flask, "for a long moment"). Signature: "She waits until Iona steps aside." Never: explains before she must.
- **Psychological gesture.** A flat hand raised between two people, holding them apart.
- **Status.** High by default; drops once, visibly, for Nell.
- **Proxemics.** Social distance, across a table or glass ("Saye stands outside the glass.", sc11). She touches only to treat or to stop: Jude's wound (sc10), "Saye catches her elbow." (sc18), "Saye takes her helmet in both hands and holds it still." (sc28), "puts her free hand between them" (sc28). The one touch that is neither: taking Nell's hand (sc28).
- **Expression range.** (1) sc10 the long look at the flask. (2) sc10 "Nothing has happened to the mint.": calm certainty. (3) sc13 "(quietly) No. It is not.": eyes unfocused. (4) sc17 the lean toward Nell's image. (5) sc24 recorded, voice gone: "They're here. Nell is here." (6) sc28 "Yes.": plain, eyes on Iona. (7) sc28 "Yes, Nell.": softened.
- **Mirror state.** B: MIRRORED (ring appears on her right). C: NORMAL.
- **Identity key (37 words).** "Dr Saye, a slim, upright woman in her late fifties, short neat grey hair, a long pale lined face, thin straight brows, level grey eyes, a light grey cardigan buttoned to the collar over a white blouse." (Revised from an earlier draft that fixed "a composed, unreadable expression" in the key; that phrase would have fought her sc17 lean and her sc28 "Yes, Nell.")
- **State lines.** C1 "a stethoscope round her neck, an open medical case beside her" (sc10). C3 "a clear protective hood and a pale gown over her clothes". In era B shots, generate her as designed and flip (her ring must then appear on her right hand).

### 10.5 NELL ROWAN ("Sixty, perhaps. She looks older.")

- **Role.** A flight-test pilot sent across by Saye nineteen years ago ("Engine failed. I was falling. Woke up in this bed."). The story's warning of what staying across means, and Saye's debt made visible.
- **Arc.** From waiting in one room with a book to walking to a room with a window, on her own feet, holding Saye's hand.
- **Design thesis.** Nell must read as a test pilot's straight spine inside a body the years and the wrong food have thinned, with everything she owns on one shelf; her dignity is her refusal to be carried.
- **One image (Section 2.6).** sc20: upright on her bed, the book closed on one finger, the old harness with its empty socket on the shelf behind her.
- **Face.** Looks older than sixty; thin, fine-boned face, deep lines; very pale [inferred: nineteen years without sun]; clear, steady light eyes; short uneven white hair, as if cut by her own hand [design choice]. The file photograph (sc17) shows the same bones younger: "A flight suit. Unsmiling." **Distinguishers:** fine bones, short uneven white hair, extreme pallor.
- **Body and silhouette.** Small and very thin ("how thin the woman's wrists are"); upright spine [design choice], slowed by weakness. Dominant shape: thin vertical.
- **Costume by phase.** **C0** (photo): flight suit, sage green [color is a design choice]. **C1** (sc17 on screen, sc20 to sc23): the remains of that flight suit, faded and soft, sleeves rolled, under a found cardigan [design choice: found human clothes, clean and oddly folded, because "It brings what I draw, if it can find it"]. On her shelf: the old engine harness "with its socket empty" and a tag dated nineteen years ago. **C2** (sc28): paper oversuit, book under one arm.
- **Color identity.** Faded sage green, light value; the photograph shows the same green at full strength, so the fading is the nineteen years.
- **Movement signature.** Centre: chest (the book held against it). Home effort: glide, light and sustained. Stress: holds onto edges ("Holds the frame with her free hand"; "She holds its back but does not sit."). Tempo: slow, each action once. Eyes: to windows and doors. Signature: "Nell closes the book on one finger." Never: sits when she can stand.
- **Psychological gesture.** Holding something precious to the chest while reaching for a handhold.
- **Status.** Quiet high status on the ship: she knows it, and her "Wait." as Iona reaches for a tool is the voice of experience. She lowers herself only to ask ("Will you take me?").
- **Proxemics.** Nineteen years behind a door; she opens her space twice: "She makes space for him on the bed." (sc23) and "Nell puts her book under one arm. Holds her other hand out." (sc28).
- **Expression range.** (1) sc20 "Nell looks up from her page.": eyes lift first, head follows. (2) sc20 "Is it safe to go home?": hope held flat, the face barely moves. (3) sc23 looking at the open doorway: eyes on it, no step yet. (4) sc28 "Is there a window in my room?": the first question she asks for herself. (5) sc28 steadying herself on Saye's hand: a breath, the grip, then upright.
- **Mirror state.** She never turned: MIRRORED on the ship in era B; NORMAL in era C (C2).
- **Identity key (28 words).** "Nell, a very thin, pale woman who looks older than sixty, a fine-boned face with deep lines, short uneven white hair, clear light eyes, straight-backed, very thin wrists."
- **State lines.** C1 "a faded sage-green flight suit, sleeves rolled, under a loose grey cardigan, a book held against her chest". C2 "white paper oversuit, a book under one arm".

### 10.6 THE GUARD

Minor characters get every field, kept to one line each (rule 20).

- **Role and arc.** Obstacle, then consequence: armed in sc05, "led down the stairs in handcuffs" in sc11. No inner arc.
- **Design thesis.** A uniform, a lanyard and a pistol: his face need not be remembered, but the card on his lanyard must read at a glance, because Eli takes it.
- **Face.** Forties, clean-shaven, short dark hair, ordinary features [design choices].
- **Body and silhouette.** Average height, solid; the silhouette's only accents are the holster and the hanging card.
- **Costume by phase.** C1 (sc05): dark navy private-security uniform, near black; black lanyard with a white access card; holster; boots. C2 (sc11): same, card gone, hands cuffed behind him. The other guards ("Guard on each door"; the shooter above) wear the same uniform and stay faceless.
- **Color identity.** Near-black navy, low saturation, so it never competes with Iona's blue; the white card is the brightest thing on him.
- **Movement signature.** Comes out "pistol half drawn, eyes on the stairs": attention direct but pointed the wrong way, so the blow comes from his blind side.
- **Expression range.** (1) alert, eyes on the stairs; (2) sc11 head down, led.
- **Mirror state.** A: NORMAL. sc11 (B): MIRRORED.
- **Identity key (28 words).** "A stocky security guard in his forties, clean-shaven, short dark hair, in a dark navy security uniform with a black lanyard and a pistol holster on his belt." (The access card moved out of the key into the state lines, because it is gone by sc11.)
- **State lines.** C1 "a white access card hanging from the lanyard, pistol half drawn". C2 "the lanyard empty, hands cuffed behind his back, head down".

### 10.7 THE NURSE

- **Role and arc.** The institution's care, delivered at a distance; dresses the palm, snaps on the wristband, offers the oxygen mask again after Iona has pulled it off ("The nurse offers the mask again."); "A hooded nurse takes over beside Jude" in sc28. No inner arc.
- **Design thesis.** Care through a barrier: we remember the gloves, not the face.
- **Face.** Mostly hidden by cap and mask; tired, kind eyes. Gender is not given by the script [design choice: a woman in her forties].
- **Body and silhouette.** Average; in sc11 the silhouette is the hatch and the two long gloves reaching through it ("works through the sealed gloves of a service hatch"; black is a design choice).
- **Costume by phase.** C1 (sc11, sc16): pale grey-green scrubs, cap, mask. C2 (sc28): protective hood and gown.
- **Color identity.** Pale grey-green, B2's quarantine palette; the black gloves are the accent.
- **Movement signature.** Practised, gentle, quick (dab and glide); every movement slightly slowed by the gloves.
- **Expression range.** (1) eyes attentive over the mask; (2) patient, offering the mask again after a refusal.
- **Mirror state.** B: MIRRORED. C: NORMAL.
- **Identity key (30 words).** "A nurse in her forties in pale grey-green scrubs, a pale surgical cap and mask covering her hair and lower face, only her eyes visible, with tired lines around them." (State line for sc11: "working through long black rubber gloves fixed in a sealed hatch in the glass".)

### 10.8 THE TECHNICIAN

- **Role and arc.** The procedure's hands and a witness: waits beside the second suit, starts the suit camera (sc18), brings Nell the wheelchair (sc28). No inner arc.
- **Design thesis.** Neutral competence; the only color near them is the red light of the suit camera they start.
- **Face.** About thirty, plain, narrow face, short cropped dark hair, clean-shaven [design choices]. Gender is not given by the script; the key uses a man as a **placeholder** (rule 7 of Section 7.2: a key that leaves gender open lets the model change it between sc18 and sc28), chosen to contrast with the nurse. The user may change it.
- **Body and silhouette.** Average, compact; in sc28 the hood makes them anonymous among the hooded staff.
- **Costume by phase.** C1 (sc18): pale grey coveralls with facility lettering (backwards to Iona) [design choice]. C2 (sc28): protective hood over the same.
- **Color identity.** Pale grey; the suit camera's red light is the accent.
- **Movement signature.** Economical and silent: waits still, acts only on instruction.
- **Expression range.** (1) neutral attention; (2) sc28 care, steadying the wheelchair while Nell refuses to sit.
- **Mirror state.** sc18 (B): MIRRORED. sc28 (C): NORMAL.
- **Identity key (28 words).** "A technician, a man of about thirty, in pale grey coveralls with a small facility logo on the chest, short cropped dark hair, clean-shaven, a narrow plain face." ("a man" is a placeholder; "neutral expression" was removed from an earlier draft under rule 2.)

### 10.9 THE FIGURE

- **Role.** Apparent monster and abductor, revealed as a suit worn by the animal: a keeper and collector that rescues what turned. The story's second catcher.
- **Arc.** From darkness to glass: opaque, faceless, huge; then damaged, patched, generous; then opened and empty, leaning on a wall.
- **Design thesis.** A human-shaped machine built by something that is not human-shaped: it gets the plan of a person right and three proportions wrong, and every wrong proportion is a clue to what is inside.
- **One image (Section 2.6).** sc15: a black shape against the lighter sealed door, taller than the door frame [design choice; the script says "tall" here and "Taller than the door" in sc16], bent over Jude's bed, the pale strip mid-slide, its huge hand under his arm.
- **Face.** None. A clear curved cover where a face would be; behind it, in a lit loop of tube, a pale flap of skin "slides across, vanishes, slides across again." Make the flap the same pale translucent tissue as the animal [design choice] so the reveal clicks by material (see 10.10, Face). The strip moves on a steady cycle, never toward objects. It is soft, matte and pale, lit from inside its tube; it must not read as a scanning light bar (Section 6.2, rule 7). Placement: "The cracked cover lifts with the chest" (sc25), so the face cover is set into the top of the body's single front hatch, low between the shoulders, not on a separate head [inferred].
- **Body and silhouette.** About 2.4 m ("Taller than the door"; the number is a design choice). No neck: a low dome sunk between high, broad shoulders. Deep barrel chest (it must hold a forearm-length vessel, tubes and a mount). Long arms; hands too large ("A huge black thumb"). Long shins [design choice]. Dominant shape: a heavy block with a sunken dome; no points, spikes or claws, so it reads as large and unknown, not aggressive. Silhouette test: for half a second, a tall person in a coat; then wrong.
- **Surface.** Matte flat black, the same material family as the puck, the engines and the cells [inferred: Saye's engine is "the same flat black as the puck"]. A row of small flush latches down the centre front and one fine seam round the edge of the front hatch, from the face cover to the belly, both visible only in rim light [design choice, needed for "Latches let go, one after another, down the front of it"]. A socket between the shoulders for a black cell. No chrome, no glowing eyes, no teeth.
- **Costume states (damage).** **S0** intact (sc15, sc16). **S1** cover cracked, "A thin WHITE JET", strip "jerks and stops moving" (sc16); crescent dent from the cylinder. **S2** "A patch covers part of the pale strip. A little fluid gathers beneath it." (sc20 onward); black cell between the shoulders. **S3** cell removed, "The pale strip dims." (sc23). **S4** chest open: "Tubes, and a small mount" (sc25). **S5** "The empty black body leans back against the wall."
- **Color identity.** Matte black; its only light is the pale strip, which dims from sc23. Its arc in color, as in B2, runs from silhouette to translucency.
- **Sound.** The pump, "three strokes, not quite even": sc15, sc16, sc25, sc27, sc28 and the last line.
- **Movement signature.** Two tempos (Section 6.5): care (glide, press: "As carefully as a nurse") and task (punch, slash: "Then it moves, and it is fast."). Never idle; indirect only when it flings something aside. Head turns to point the strip; hands settle a fraction late [design choice]. Kneels to work ("The figure kneels."). Arrives without travel in human rooms (sc15, sc16); walks on its own ship (sc20 onward).
- **Psychological gesture.** A flat hand laid on its own chest: "It puts its hand flat against its own chest." (sc25).
- **Proxemics.** Its frightening distance and its caring distance are the same distance, within arm's reach: it bends over Jude to lift his arm (sc15) and raises an arm toward Iona (sc16). On the ship it stands "Close enough to touch." and "reaches past her shoulder" to straighten a container (sc21). Stage the sc16 approach and the sc21 approach at the same distance and height so the rewatch reads the first as the second.
- **Expression range (no face).** (1) the head turning to point the strip at something; (2) the lifting hand, "As carefully as a nurse"; (3) the raised arm toward Iona (sc16), read as threat, later understood as reaching; (4) looking from Iona's visor to Nell's drawing and back (sc23); (5) braced against the burning cabinet (sc24); (6) the hand flat on its own chest (sc25); (7) empty, leaning.
- **Mirror state.** Turned (by inference): NORMAL in era B with the ship; MIRRORED on world screens (sc17) (C2).
- **Identity key (37 words).** "A towering matte-black machine shaped like a person, taller than a doorway, a low domed head sunk deep between high broad shoulders, a clear curved face cover with a soft pale strip behind it, very large hands." (Revised from an earlier draft that used "humanoid", which pulls in stock robots, "no neck", which is negative phrasing, and "a narrow band of pale light", which pulls in the scanning-light-bar cliché.)
- **State lines.** S1 "the clear face cover cracked, a thin white jet spraying from the crack". S2 "a dull grey patch over part of the face cover, clear fluid beneath it, a black box-shaped cell fixed between its shoulders". S3 "the socket between its shoulders empty, the pale strip dimmer". S4 "its whole front, face cover included, swung open as one hinged panel, tubes and a small mount inside" (the script: "The chest swings open." / "The cracked cover lifts with the chest."). S5 "empty, leaning back against a wall, arms hanging".

### 10.10 THE ANIMAL (and its vessel)

- **Role.** The figure's true operator; a small, fragile collector and tender; the being Iona chooses to carry home.
- **Arc.** Hidden, then exposed and afraid ("shrinks from her fingers to the far side of its water"), then trusting enough to point and to turn with her ("Winds it round a fitting."), then tending its container beside Iona's bed.
- **Design thesis.** Everything the suit was not: small, clear, soft, cold and slow; its only expressions are limb movements, and each one should echo a human hand gesture already in the film.
- **One image (Section 2.6).** sc25: the vessel strapped to the chest of Iona's white suit, the animal almost invisible in the dark water except for one fine limb pressed to the glass, "Pointing back. At the open chest."
- **Face.** None visible [design choice: it keeps the animal alien and avoids the cute reveal (Mistake 11)]. It must still see somehow, since it copied Iona's name "stroke for stroke, the way you would copy a drawing"; if the sense organs are shown at all, make them faint, darker specks in the body, not eyes with lids or pupils [design choice]. One reading of "a flap of skin in a lit loop of tube" is that the flap is the animal's own tissue reaching up into the suit's head [interpretation; confirm with the user]; if accepted, show the same pale tissue faintly at one end of its body.
- **Body and silhouette.** "No longer than her hand": about 15 cm [design choice within the text]. Soft rounded body, "Almost clear", with faint pale inner shapes, one slightly denser so it reads against dark water [design choice]. Several thread-fine limbs longer than the body, which fit into sockets in the vessel wall ("One fine limb draws itself out of a socket in the wall of the vessel."). No big eyes, no mouth, nothing toy-like.
- **Vessel.** Glass, "dark water", "about as long as her forearm"; small mount; clear tubes; the pump and battery come with it; a soft sealed sleeve in its wall (sc30). Its water is "so cold it whitens" where it escapes; a thin frost or condensation on the glass in warm rooms [design choice]. The container with the blue sleeve strip is clipped to it from sc25.
- **Color identity.** Near-clear, cool milky white; no blue, to keep Iona's color free [design choice].
- **Movement signature.** Home: float (light, sustained, indirect). Fear: bound; "folded itself small round the fittings", a limb "wound tight round its socket" [design choice: stage this to echo Iona's grip in the fall, "She hooks her fingers deeper into the grid"]. Communication: "presses a limb to its window" (echo of Iona's palm on glass). Care: "draws the container close against its own glass." Tempo: slow; it never darts.
- **Expression range (limb states).** Shrink; fold small; press to the glass (point); touch the moving picture; draw back and wait; uncurl; tend.
- **Mirror state.** Turned with the ship and again with Iona: NORMAL in eras B and C.
- **Identity key (32 words).** "A small, glass-clear, soft-bodied sea creature no longer than a hand, faint milky shapes inside it, several thread-thin limbs longer than its body, floating in a forearm-length glass vessel of dark water." (Revised from an earlier draft that said "deep-sea animal ... like a comb jelly": "deep-sea" tends to pull in anglerfish teeth and lures, and "comb jelly" pulls in rainbow shimmer and glow, which would also break the no-blue rule above. Keep comb jellies, glass octopuses, salps and *Phronima* as reference images, where you can choose what to borrow.)
- **State lines.** V1 (sc25) "held in a small mount inside the open black chest, clear tubes running into the vessel". V2 (sc25 to sc28) "the vessel strapped to the front of a white pressure suit, a small sealed container clipped to its side". V3 (sc28) "in a shallow padded tray, a small pump attached". V4 (sc29, and sc30 until the cloth) "standing on a metal bedside table inside a clear plastic tent, a small pump and a sealed container attached". V5 (end of sc30) "resting on a folded cloth on the metal table, the container beside it half full of cloudy growth" ("The cloudy growth behind the scrap of shirt fills half the container now.").

### 10.11 Lineup check

| Character | Height | Mass | Dominant shape | Value | Color identity | Tempo |
|---|---|---|---|---|---|---|
| Iona | medium | lean | vertical rectangle | mid-light | faded blue, then white | steady, counted |
| Jude | tall | heavy, soft | rounded rectangle | mid | olive | unhurried |
| Eli | medium-tall | thin | angular lines | dark | charcoal | pause, then act |
| Saye | medium | slim | narrow rectangle | light | light grey, mint accent | fast hands, still body |
| Nell | small | very thin | thin vertical | light | faded sage | slow |
| Figure | very tall | massive | block, sunken dome | black | matte black | care or sudden |
| Animal | hand-sized | tiny | soft round, threads | clear | milky white | slow float |

Eli and Saye share grey on purpose and differ in height, mass, shape, value and tempo. Iona and Eli share brows and eyes on purpose and differ in shape, color, value and tempo. Saye and Nell, who leave the film hand in hand, are the closest pair (both light in value, both narrow verticals, both slight); they stay legal under the four-column rule by height, color and tempo, and the design should widen the gap further through posture (Saye's level shoulders against Nell's effortful straightness) and white hair against grey.

---
## 11. Worked examples

### Example 1. The flat hand (sc01, then sc12, sc17, sc25, sc29)

> "She gets up. Lays her hand flat on the ropes, the way a vet feels along a dog's ribs."

**Choice.** Make this Iona's signature gesture and film its first instance as an insert at emphasis level L2: right hand [design choice], palm flat, fingers slightly spread, gliding slowly down the rope (about 30 cm in 2 seconds), pausing twice where it "feels"; her eyes are not on her hand but on the middle distance, head still. Later flat hands copy the exact hand shape and a similar framing: her palm on the glass beside the restored F (sc12), her hand flat on the glass toward Jude's image (sc17). The same shape then **transfers**: the figure "puts its hand flat against its own chest" (sc25), and Jude "Lays his good hand flat on it" (sc29).

**Why.** The simile says two things at once: diagnosis (she reads the machine through touch) and care (a vet's hand is gentle with an animal). That is Iona's psychological gesture: pressing a flat hand to feel whether something will hold. Eyes off the hand show that the knowledge is in the hand ("Her arm knows it before she does," sc06). Because the hand shape is fixed, the audience can recognise its transfer to a non-human body without dialogue: the figure uses the gesture of care that defined her. Laban: glide (light, sustained, direct), bound flow. For AI: generate the sc01 insert from a still of the hand on the rope with image-to-video; prompt the motion as "the flat hand slides slowly down the rope, pauses, slides again; the head does not move."

### Example 2. The half-smile and its wrong side (sc03 and sc28)

> "For a moment the beard belongs to somebody else. Then one corner of his mouth lifts, the crooked half-smile she knows." (sc03)
> "Eli has got to his feet. He lifts one hand and tries to smile. The familiar little smile, on the wrong side of his face." (sc28)

**Choice.** Fix the smile on Eli's own left (it appears on frame right when he faces the camera). Describe it as movement: the left lip corner pulls up (AU12, one side only), a slight cheek rise on that side, eyes softening. In sc03 play it as a two-part beat: strangeness (the beard), then the smile arriving. In sc28, because Eli is MIRRORED in era C, the same smile appears on his apparent right, and "tries to smile" is played weaker: lip corner up, no cheek rise, eyes flat. Add his hair parting (own left) as a second, quieter cue that flips with it. For AI, generate and approve the sc03 expression still, then make the sc28 reference by **flipping** that approved still in an editor, not by prompting "smile on the wrong side".

**Why.** The line pays off only if the audience saw which side it was on, and the audience saw it only if the design fixed it. The half-smile is the one warm thing in Eli's guarded face, so its wrongness at the end hurts: he is himself and not quite himself to her. Flipping a real still gives an exact mirror; prompting gives a random side.

### Example 3. The figure's first appearance (sc15)

> "Something tall and black stands beside his bed. It did not come through the door. It is simply there ... THE FIGURE. Its head sits low between its shoulders. Where a face would be, a pale strip slides across, vanishes, slides across again. From inside it, a PUMP: three strokes, not quite even."

**Choice.** Fear rules: cut it in without travel; first frame shows it as a silhouette against the lighter sealed door, taller than the frame; the pump is heard on the cut, before the strip moves [design choice: the script describes the strip first and the pump second, but sound first obeys rule 4 of Section 6.2 and costs nothing]. Clues at L0 to L1: the head flush with the shoulders (no neck); the strip moving on a steady cycle while the head points at Jude (it does not track like eyes); faint frost at the edge of the face cover in the tablet's cold light; fine latch lines on the chest caught by edge light. Then the care: "Its hand goes under his wounded arm and lifts it clear of the mattress. As carefully as a nurse." Played as press into glide, slow; after the lift the huge hand settles a fraction late. Because this scene is seen "ON THE TABLET", render it with C3's security-footage look and treat its mirror state per C2, Section 7.4.

**Why.** The audience must be afraid now and fair-minded later. Fear comes from scale, arrival, a face feature removed and a sound with no visible source. Fairness comes from clues that register as strange: a missing neck, a strip that does not look, frost, latches, the late settling hand. The nurse-like care is the dimension (Principle 2) planted in the first ten seconds, so the pity in sc25 is recognised, not imposed.

### Example 4. One shoe (sc04, sc21)

> "She gives Eli one shoe. He leaves the other." (sc04)
> "Round the walls: sealed containers. Bloody cloth. Brick dust. One shoe." (sc21)

**Choice.** Design Eli's shoes once: plain brown leather lace-ups [design choice]; he wears the right one [design choice]. The collection room holds things "off the cage", and the figure collects "what turned", so the shoe on its wall is most economically the one he wore, lost in the fall. Recommend: in sc06, as the cage stops dead, his shod foot slips against the control box and the shoe comes off, at L0; from sc07 he is in socks, shown at L0 on the concrete. The sc21 shoe is the same right shoe, turned with the cage (so NORMAL to the camera in era B). Flag as an open question (Section 15).

**Why.** A costume item that returns as a prop must be the same object, or the collection room's inventory loses its meaning: "Found. Carried here. Sealed. Put in order." It also marks Eli's arc in costume terms: he leaves the factory without his footing, literally, and the story makes him walk the rest of it on someone else's terms.

### Example 5. Melek's hands (*The Long Places*, prose)

> "Melek Yılmaz was at the mouth before her, because Melek was always somewhere before her. Seventy-eight, built like a doorpost, with the site's other register in her hands: knuckles like burl, a burn gone silver across the back of the right one, nails trimmed to nothing so the wicks could be pinched."
> Later: "Melek rose, laid the flat of her hand on the sounding stone, and knocked twice, softly, and then stood in the waiting, two breaths entire."

**Choice.** Convert each metaphor to a design fact. "Built like a doorpost": tall for her generation, straight-backed, square-shouldered, not stooped at seventy-eight; a vertical rectangle that stands at a threshold. "The site's other register in her hands": the hands are her face, so the camera's close-ups go to hands, and the entry needs a hands sheet more than an expression sheet. "Knuckles like burl": enlarged, knotted knuckles. "A burn gone silver across the back of the right one": an old healed burn scar, pale and shiny, on the back of the right hand (a left/right mark: record it). "Nails trimmed to nothing": very short nails, a work fact. Movement signature: glide and press, light and sustained; the knock is two soft knocks with the flat of the hand, then about two breaths (roughly six to eight seconds) of stillness, which the edit must hold.

**Why.** Prose gives character through metaphor, and models draw metaphors literally ("a doorpost" becomes wood). The metaphors belong in the design thesis ("a keeper who stands at the threshold, whose history is in her hands"), and only their visible translation goes into the identity key: "an upright, square-shouldered woman in her late seventies, very short nails, large knotted knuckles, a pale shiny burn scar across the back of her right hand." (The text says "Seventy-eight"; write the age band, not a rounded-up one.) Note the rhyme across the library: Melek's flat hand on the stone and Iona's flat hand on the ropes are the same gesture of listening through touch.

---

## 12. Checklist (run per character, then per shot)

**Per character**
- [ ] Role, arc and design thesis written, one line each; the one image named (principals).
- [ ] Every line of the text about look or movement is quoted under EVIDENCE.
- [ ] Every choice not in the text is marked [design choice] or [inferred], with the reason.
- [ ] Silhouette is distinct from every other principal at wide-shot size.
- [ ] Lineup: no two principals share four or more columns (Section 10.11).
- [ ] Face specification complete; three distinguishers named.
- [ ] Every left/right feature listed with its own side and its on-screen side in each mirror era.
- [ ] Expression range tied to named beats and written as movement, not emotion words.
- [ ] Costume states numbered, with scenes covered; damage ledger complete.
- [ ] Color identity assigned and not repeated at the same saturation on another character in the same scene.
- [ ] Movement signature has all eight fields, a quoted signature gesture, and an arc.
- [ ] Psychological gesture and status default written; status flips mapped to beats; proxemics (default and closest distance) written for principals.
- [ ] Stereotype check passed (Section 2.7): no morality coded in ethnicity, body size, disability or facial difference; no stock "type" costume.
- [ ] Casting-type placeholders marked open.
- [ ] Non-human: clue ledger written; fear rules and pity rules both met.
- [ ] Identity key 25 to 40 words (minor: 20 to 30), visible features only, unique across the cast; state lines written.
- [ ] The key contains no expression words, no negative phrasing, no famous names, and no item that changes during the story; it fixes apparent gender and age band (placeholders marked outside the quotation marks).
- [ ] Every side is recorded as the character's own left or right in the NORMAL design, with a note of how it appears on screen in each era.
- [ ] Reference list includes a hands-and-marks sheet (and a scale sheet for non-humans).

**Per shot**
- [ ] The costume state and damage in the shot match the ledger for that scene.
- [ ] Any side-dependent feature in frame is correct for the era.
- [ ] The movement in the shot uses the character's home, stress or break effort as the beat requires.
- [ ] The identity key is pasted unchanged; the state line is the current one.

---

## 13. Common mistakes and how to spot them

1. **Adjective design.** "Mysterious, tough, kind." *Spot:* nothing in the entry could be drawn. *Fix:* fill the face specification and movement signature.
2. **Costume as job label.** Lab coat for a scientist, trench coat for a detective. *Spot:* the costume would fit any story. *Fix:* ask what this person's work, means and history put on them, and what the story has done to it since.
3. **Villain coding by face or body.** Scars, sharp features, darker skin or fatness on the antagonist. *Spot:* remove the moral role; is the design still justified? *Fix:* Section 2.7.
4. **Clone cast.** Everyone the same age, build and attractiveness (the AI default). *Spot:* lineup table. *Fix:* vary height, mass, shape, value, color and tempo.
5. **Continuity breaks in damage.** The wound on the wrong side, a bandage before the injury, blood that vanishes. *Spot:* compare shot list to ledger. *Fix:* the ledger and state lines.
6. **The overused signature.** The flat hand in every scene until it is a tic. *Spot:* more than one instance per scene outside a payoff. *Fix:* ration it to beats that change something.
7. **Heavy-handed symbolic costume.** Dressing Saye in black to say "villain", or giving Iona an "angelic" glow in the white suit. *Spot:* a garment the character would not choose or be issued. *Fix:* every symbolic choice must also have a practical reason (the pressure suit is white because the script says so, and real spacewalk suits are white to reflect sunlight; so light it as equipment, with no halo or bloom).
8. **Over-acted faces.** An emotion word on every line. *Spot:* no still faces anywhere in the scene. *Fix:* let eyeline and cut do the work (Section 3.1); save large expressions for turning points.
9. **Monster clichés.** Glowing red eyes, teeth, drool, spikes, chrome, a famous creature's head shape. *Spot:* it resembles a known creature. *Fix:* remove or relocate one human feature and build from the story's own materials.
10. **Unfair reveal.** Latches, cell socket or cold first appear at the reveal. *Spot:* a clue ledger row with no earlier scene. *Fix:* plant at L0 or L1.
11. **The cute reveal.** The animal designed with big eyes like a toy. *Spot:* it would sell as a plush. *Fix:* keep it alien; get pity from behavior, not from a baby face.
12. **Paraphrased identity keys.** *Spot:* compare the key text across prompts. *Fix:* paste, never retype.
13. **Metaphor fed to a model.** "Built like a doorpost" returns a wooden post. *Fix:* rule 18.
14. **Movement written as feeling.** "Moves sadly." *Fix:* body part, direction, speed, force, what stays still.
15. **Heroic posing.** The protagonist in a wide stance, chin up, shot from below, hair in the wind. *Spot:* the pose would fit a film poster for any action film. *Fix:* show competence the way the text does, in small economies ("Her light goes onto each rung before her hand does."; "She takes his weight with her legs, not her back.").
16. **Suffering make-up.** Captivity and illness shown by dark eye circles, grime and sweat on every face. *Spot:* every hurt character looks the same. *Fix:* use the specific marks the text gives (Eli's beard, Nell's wrists, Iona's palm) and leave the rest clean.
17. **The stock machine-monster.** The pale strip rendered as a sweeping light bar, glowing eyes, chrome or pistons. *Spot:* the figure resembles a famous robot. *Fix:* Section 6.2, rule 7; describe soft pale matter behind glass.
18. **Fixed expression in an identity key.** "Composed", "neutral expression", "kind eyes" in the key. *Spot:* the same face in every beat. *Fix:* rule 2 of Section 7.2; expression goes in the shot prompt.

---

## 14. How to say this to an AI image or video model

These notes are judgment from how current models tend to behave; C2 and C3 hold the tested tool details. Keep claims modest and test on your own tool.

**Tends to work.** Age in decades ("in her late thirties"); build words (thin, lean, broad, stooped, upright); hair color, length and style; facial hair; named garments with colors and condition ("faded blue work shirt, sleeves rolled to the elbow"); simple accessories; materials ("matte black", "glass", "translucent"); framing and light words.

**Works partly.** Specific facial geometry (deep-set eyes, hollow cheeks) is often averaged away without a reference image. Subtle expressions: movement descriptions work better than emotion words, but a one-sided smile often becomes a full smile. Scale ("taller than a doorway") works better when a door is in the frame. Costume states, including damage, hold only if restated in every prompt.

**Often ignored or misread.** Left and right (ring hand, smile side, wound side): expect errors; fix by flipping or editing stills and checking by eye. Text on costumes (C2, Section 7). "Faceless" tends to produce a mask, a hood or a face anyway; describe what is there instead. Negative phrasing ("no eyes") can add the thing it names. Theory terms (Laban, Chekhov, Johnstone, "shape language", "design thesis", "arc", "symbolizes") are ignored or pull in stock imagery. Famous names ("like the xenomorph") pull in the famous design.

**Plain phrasings that work better**

| Design term | Say instead |
|---|---|
| Glide | "moves slowly and smoothly, her hand sliding along the surface" |
| Punch | "one fast, hard swing" |
| Bound flow | "tight, controlled movements that stop sharply" |
| Float | "drifts slowly, limbs loose, as if underwater" |
| High status | "stands still, head level, looks straight at her, does not fidget" |
| Low status | "glances away and back, small nods, touches his face" |
| Hidden hand (Eli) | "one hand stays behind the other man's back, out of view" |
| Half-smile | "a small lopsided smile, only one corner of his mouth lifts" (then check the side) |
| Pale strip | "behind the clear face cover, a soft pale strip like wet tissue slides slowly across, disappears, and slides across again" (check it has not become a glowing scanner bar) |
| Head low between shoulders | "its domed head sits deep between high shoulders; the top of the head is level with the tops of the shoulders" |
| Frightening | describe light and framing: "seen from low, lit only along its edges, filling the doorway" |
| Pitiable | describe behavior: "it shrinks to the far side of the glass" |
| Almost clear | "glass-clear and soft, faint milky shapes inside, dim, lit only where light passes through it" (a comb-jelly comparison adds rainbow shimmer; use it only in reference images) |
| Built like a doorpost | "tall, straight-backed, square-shouldered, standing very upright" |

---

## 15. Open questions for the user

1. **Casting types.** Ethnicity and skin tone for every character. The placeholders in the identity keys come from C3 and are not decisions.
2. **Jude and Iona.** The matching rings imply marriage; confirm.
3. **Sides.** Confirm the recommended sides: Iona's torn sleeve and skinned palm on the right, chipped upper left front tooth, earpiece left; Jude's wound in the right shoulder (derived from the ring and "good hand"); Eli's smile and parting on his own left; Eli's shoe on the right foot.
4. **Eli's shoe.** Does he lose his one shoe in the cage, so it is the "One shoe" in the collection room (recommended)?
5. **Nell's clothes on the ship.** Remains of her flight suit plus found clothes (recommended), or something the ship made?
6. **The animal.** How much to show, and whether it has eyes (recommended: none visible).
7. **The figure's height.** About 2.4 m is recommended; taller makes interiors harder to stage.
8. **Eli and Saye's shared grey.** Keep the link, or separate them further?
9. **The sleeve's route to the ship.** The script never says how Iona's sleeve reaches the collection room. Recommended: it is part of "Jude's dressings, from a sealed bin" (sc17), taken off Jude when "Saye cuts Jude's shirt away" (sc10). Confirm, because it decides whether Saye's kitchen scene shows the sleeve being bagged.
10. **Unstated genders of minor characters.** The nurse (placeholder: a woman) and the technician (placeholder: a man). Confirm or change before any image is made; the key must fix one.
11. **The face cover's position.** "The cracked cover lifts with the chest" is read here as: the face cover is set into the top of the figure's one front hatch. Confirm, because it changes the figure's silhouette and the reveal staging.

---

## Sources

**Books**
- McKee, Robert. *Dialogue: The Art of Verbal Action for Page, Stage, and Screen*. Twelve / Grand Central Publishing, 2016. Quoted from the user-supplied edition: Chapter 2 (true character and characterization; gestures), Chapter 5 (paralanguage; microexpression claim, endnote citing Gladwell's *Blink*), Chapter 11 (dimension).
- Bancroft, Tom. *Creating Characters with Personality: For Film, TV, Animation, Video Games, and Graphic Novels*. Introduction by Glen Keane. Watson-Guptill, 2006.
- Thomas, Frank, and Ollie Johnston. *The Illusion of Life: Disney Animation*. Abbeville Press, 1981.
- Landis, Deborah Nadoolman. *Screencraft: Costume Design* (Focal Press, 2003); *Dressed: A Century of Hollywood Costume Design* (HarperCollins, 2007); *FilmCraft: Costume Design* (Focal Press, 2012); ed., *Hollywood Costume* (V&A Publishing, 2012).
- Laban, Rudolf, and F. C. Lawrence. *Effort*. Macdonald and Evans, 1947. Laban, Rudolf. *The Mastery of Movement on the Stage*. Macdonald and Evans, 1950 (later editions revised by Lisa Ullmann as *The Mastery of Movement*).
- Chekhov, Michael. *To the Actor: On the Technique of Acting*. Harper and Brothers, 1953 (Routledge edition 2002).
- Johnstone, Keith. *Impro: Improvisation and the Theatre*. Faber and Faber, 1979.
- Lecoq, Jacques. *The Moving Body (Le Corps poétique)*. Trans. David Bradby. Methuen, 2000.
- Hall, Edward T. *The Hidden Dimension*. Doubleday, 1966.
- Todorov, Alexander. *Face Value: The Irresistible Influence of First Impressions*. Princeton University Press, 2017.
- Zebrowitz, Leslie A. *Reading Faces: Window to the Soul?* Westview Press, 1997 (not re-checked in this session).
- Ekman, Paul, and Wallace V. Friesen. *Facial Action Coding System*. Consulting Psychologists Press, 1978.

**Papers**
- Willis, J., and A. Todorov. "First impressions: Making up your mind after a 100-ms exposure to a face." *Psychological Science*, 2006.
- Barrett, L. F., R. Adolphs, S. Marsella, A. M. Martinez, and S. D. Pollak. "Emotional Expressions Reconsidered: Challenges to Inferring Emotion From Human Facial Movements." *Psychological Science in the Public Interest*, 2019.
- Prince, S., and W. E. Hensley. "The Kuleshov Effect: Recreating the Classic Experiment." *Cinema Journal*, 1992. Mobbs, D., et al., *Social Cognitive and Affective Neuroscience*, 2006. Barratt, D., et al., *i-Perception*, 2016 (as summarised on Wikipedia).
- Mitchell, J., M. Francke, and D. Eng. "Illustrative Rendering in Team Fortress 2." *Proceedings of the 5th International Symposium on Non-Photorealistic Animation and Rendering* (NPAR), 2007 (authors and venue confirmed via the ACM Digital Library listing and Valve's PDF).
- Krumhuber, E. G., and A. S. R. Manstead. "Can Duchenne Smiles Be Feigned? New Evidence on Felt and False Smiles." *Emotion* 9 (6), 2009, 807 to 820.
- Porter, S., and L. ten Brinke. "Reading Between the Lies: Identifying Concealed and Falsified Emotions in Universal Facial Expressions." *Psychological Science*, 2008 (as summarised on Wikipedia; title from memory).

**Films and series cited**
*Alien* (1979, Ridley Scott); *Doctor Who*, "The Daleks" (1963); *The Elephant Man* (1980, David Lynch); *Raiders of the Lost Ark* (1981); *Thriller* (1983); *Men in Black* (1997, Barry Sonnenfeld); *Mulan* (1998, Barry Cook and Tony Bancroft); *Pan's Labyrinth* (2006, Guillermo del Toro); *Up* (2009, Pete Docter); *Inside Out* (2015, Pete Docter); *Casting By* (2012, Tom Donahue); *Arrival* (2016, Denis Villeneuve); *Team Fortress 2* (2007, Valve).

**Web pages (all checked 2026-09-27)**
- Arrival (film): https://en.wikipedia.org/wiki/Arrival_(film)
- Xenomorph design (Giger, Rambaldi, Badejo): https://en.wikipedia.org/wiki/Alien_(creature_in_Alien_franchise)
- Dalek (Cusick, Nation, mutant inside): https://en.wikipedia.org/wiki/Dalek
- Men in Black (Rick Baker; Arquillian reveal): https://en.wikipedia.org/wiki/Men_in_Black_(1997_film)
- Pan's Labyrinth (Pale Man, Doug Jones, DDT): https://en.wikipedia.org/wiki/Pan%27s_Labyrinth
- The Elephant Man (Tucker makeup; makeup award): https://en.wikipedia.org/wiki/The_Elephant_Man_(1980_film)
- Up (Docter on Carl and Russell): https://en.wikipedia.org/wiki/Up_(2009_film)
- Annie Award for character animation in a feature (Tom Bancroft's 1998 nomination for Mushu): https://en.wikipedia.org/wiki/Annie_Award_for_Outstanding_Achievement_for_Character_Animation_in_a_Feature_Production (via search summary; Mulan's own page names Tony Bancroft as co-director: https://en.wikipedia.org/wiki/Mulan_(1998_film))
- Penguin Random House listing, *Creating Characters with Personality* (publisher's description): https://www.penguinrandomhouse.com/books/8114/creating-characters-with-personality-by-tom-bancroft-introduction-by-glen-keane/9780823023493/
- Gizmodo, "The Aliens of Arrival Nearly Looked a Lot Weirder" (Carlos Huante; Peter Konig): https://gizmodo.com/what-the-aliens-of-arrival-could-have-looked-like-1789475263
- fxguide/fxphd, "ARRIVAL: anti-gravity and aliens" (Huante's maquettes; Hybride; seen only via search summary, page blocked): https://www.fxphd.com/fxblog/arrival/
- BAMPFA program note on Deborah Nadoolman Landis ("discover who the people are in the screenplay"): https://bampfa.org/program/costume-designer-deborah-nadoolman-landis-behind-scenes-art-and-craft-cinema
- *Daily Bruin* Q&A with Landis, 5 December 2024 ("we need to know how to read"): https://dailybruin.com/2024/12/05/qa-costume-designer-deborah-nadoolman-landis-talks-career-impact-of-work
- Official TF2 Wiki, "Illustrative Rendering in Team Fortress 2" (quotation on silhouettes): https://wiki.teamfortress.com/wiki/Illustrative_Rendering_in_Team_Fortress_2
- Valve, NPAR 2007 paper PDF: https://steamcdn-a.akamaihd.net/apps/valve/2007/NPAR07_IllustrativeRenderingInTeamFortress2.pdf
- Krumhuber and Manstead 2009 (PubMed record): https://pubmed.ncbi.nlm.nih.gov/20001124/
- Creative Bloq, "5 surprising facts about Inside Out's character design" (emotion shapes; article body not retrievable, claim seen in search summary): https://www.creativebloq.com/animation/inside-out-character-design-111517644
- Twelve basic principles of animation (staging, appeal): https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation
- Model sheet: https://en.wikipedia.org/wiki/Model_sheet
- Team Fortress 2 (visual distinctness at range): https://en.wikipedia.org/wiki/Team_Fortress_2
- Deborah Nadoolman Landis: https://en.wikipedia.org/wiki/Deborah_Nadoolman_Landis
- Marion Dougherty and *Casting By*: https://en.wikipedia.org/wiki/Marion_Dougherty
- Changing Faces, "I Am Not Your Villain": https://en.wikipedia.org/wiki/Changing_Faces_(charity)
- Laban movement analysis: https://en.wikipedia.org/wiki/Laban_movement_analysis
- Michael Chekhov: https://en.wikipedia.org/wiki/Michael_Chekhov
- Jacques Lecoq: https://en.wikipedia.org/wiki/Jacques_Lecoq
- Keith Johnstone: https://en.wikipedia.org/wiki/Keith_Johnstone
- Proxemics: https://en.wikipedia.org/wiki/Proxemics
- Physiognomy: https://en.wikipedia.org/wiki/Physiognomy
- Alexander Todorov: https://en.wikipedia.org/wiki/Alexander_Todorov
- Kuleshov effect: https://en.wikipedia.org/wiki/Kuleshov_effect
- Facial Action Coding System: https://en.wikipedia.org/wiki/Facial_Action_Coding_System
- Microexpression: https://en.wikipedia.org/wiki/Microexpression
- Open Library record, *Creating Characters with Personality* (2006): https://openlibrary.org/search.json?q=creating+characters+with+personality+bancroft

**Library cross-references**: A2 and A3 (scene breakdown), B2 (color script; matte-black lighting rule 25), B3 (Hall's zones, Section 4.2), B4 (costume variables 6.1, emphasis levels 3.4, state table 9.4), C2 (character sheets 6.2, mirror states 7.3 and 7.4, drift check R7), C3 (identity keys 11 and 22.0, including its quotation of Google Cloud's "Best practices for generating videos"), C4 (Blender previs).

**Stated plainly: not verified in this session.** The last two levels of Bancroft's design hierarchy (lead character, realistic) and the book's own wording on shapes; any direct quotation from Johnstone or Lecoq (paraphrased; the Landis quotations are checked but secondhand, via BAMPFA and the *Daily Bruin*); whether "seven levels of tension" appears in Lecoq's own book; the wording of *The Illusion of Life* on silhouettes; Chekhov's "imaginary centre" wording in *To the Actor*; the *Inside Out* emotion shapes (press reports only); Hybride's role on the heptapods (search summary of fxguide/fxphd, page not fetched); the Porter and ten Brinke paper title; Zebrowitz's book details; the BFI's reported 2018 funding pledge on facial difference (not used as a fact above). All quotations from *The Catch*, *The Long Places* and McKee's *Dialogue* were checked verbatim against the user-supplied files.

**Verified in the fact-check pass (2026-09-27).** Heptapod designer (Carlos Huante, not Patrice Vermette); TF2 paper authors; Tom Bancroft's Annie nomination (and that Mulan's co-director is his twin, Tony); the publisher's Bancroft quotation; the Badejo, Dalek, Pale Man, Elephant Man and *Up* quotations; Porter and ten Brinke's 2% finding; the Lecoq neutral-mask and Chekhov psychological-gesture wording on Wikipedia.
