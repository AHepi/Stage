# A3. Reading a Script for Production: Directing Analysis, the Production Breakdown, Continuity, and Adapting Prose

*Library file A3. Written 2026-09-27. Test sources: "The Catch" (screenplay, workshop revision of 25 September 2026) and "The Long Places" (prose novella). Web facts checked on 2026-09-27.*

> **What this file is for**
> 1. It teaches an LLM, or a person with no film training, to read a script the way a director does: what each character wants, what changes, and what the audience must see.
> 2. It turns that reading into the standard production paperwork: breakdown sheet, shot list, floor plan, storyboard, continuity notes, lined script.
> 3. It shows how to parse screenplay text reliably, including Fountain and the variant markup used in *The Catch*.
> 4. It shows how to adapt prose into scenes: what becomes a scene, how thought becomes behavior, how letters and time jumps are handled.
> 5. It ends with an element-extraction checklist that builds the asset lists (people, places, props, costumes, states) that image, previs and video tools need.

**How to use it.** Run the passes in this order: parse (section 4), director's pass (section 3), breakdown (section 5), continuity (section 6). For prose, run the adaptation pass (section 7) first; its output is a list of scenes in screenplay form, and the other passes then run on that. Library files A1 (dialogue) and A2 (scene design and beats) go deeper on beats and dialogue; B1 (camera) and B2 (light and color) decide how shots look. This file decides what must be planned and tracked.

---

## 1. Words this file uses (one word per concept)

| Term | Plain definition |
|---|---|
| **Source** | The text being turned into film: a screenplay or a piece of prose. |
| **Scene** | In this file, the unit of text that begins at a scene heading and ends at the next one. This is the production unit: it is numbered, measured, scheduled. |
| **Sequence** | Several consecutive scenes that play as one continuous dramatic action (in *The Catch*, scenes 1 to 7 are one rescue). A2 defines a scene dramatically; when a scene and a dramatic unit differ, record the sequence. |
| **Scene heading** | The capitalized line that starts a scene: interior or exterior, place, time (`INT. SAYE'S HOUSE - KITCHEN - BEFORE DAWN`). Other books call it a slugline. |
| **Action line** | Present-tense description of what is seen and heard. |
| **Character cue** | The capitalized name above a speech. |
| **Extension** | A tag after a cue that says how the voice is heard: (V.O.) voice-over, heard but not spoken in the scene's space, which covers both narration and a voice through a device such as a radio earpiece or phone; (O.S.) off-screen, spoken in the space but outside the frame. The parenthetical under the cue tells you which kind of V.O. it is (4.3, step 4). |
| **Parenthetical** | A short direction in parentheses under a cue: `(quite softly)`. |
| **Transition** | An editing instruction on its own line: `CUT TO BLACK.`, `DISSOLVE TO:`. |
| **Event** | The one change a scene exists to deliver, written as a past-tense sentence ("Iona learned the brakes were gone and went anyway"). Judith Weston writes of a script's "emotional events". |
| **Beat** | One action plus the reaction it provokes (A2's definition). |
| **Turning point** | The beat in which the event happens. |
| **Objective** | What a character wants from another character in this scene. A2 calls this the *scene intention*; it is the same thing. |
| **Obstacle** | Whatever stands between the character and the objective. |
| **Playable action** | A transitive verb (one that takes an object) the character does *to* someone to get the objective: to warn, to test, to soothe. An actor can play it; a camera can photograph its effect. A2 calls a change of playable action a new *tactic*. |
| **Spine** | A character's want across the whole story, phrased as a verb ("to get her brother home"). Stanislavski's word is super-objective; A2 says super-intention. |
| **Fact / inference / invention** | Labels for every item in the breakdown. A *fact* is stated in the source. An *inference* is strongly implied and the evidence is cited. An *invention* is a production choice. |
| **Breakdown** | The process of reading a script scene by scene and listing every element the production must supply. |
| **Breakdown sheet** | One page per scene listing its elements by category. |
| **Element** | Anything a department must supply: a cast member, a prop, a costume, a sound, an effect. |
| **Eighth** | One-eighth of a script page, the unit of scene length used in scheduling. |
| **Story day** | Which day of the story a scene takes place on (D1, N1, D2...), used to track costume and injuries. |
| **Set** | A place as the production builds, dresses or generates it. One set can serve several scene headings. |
| **Stripboard** | The schedule: one strip per scene, reordered so scenes on the same set shoot together. |
| **Shot list** | A table of every planned shot, scene by scene. |
| **Camera setup** | One camera position with one lens. On a set each new setup costs time; in AI video each costs at least one generation. |
| **Storyboard** | Drawings (or generated stills) of the planned shots, in order. |
| **Floor plan** | A drawing from directly above showing the set, where each character stands and moves, and where each camera setup sits. Also called an overhead. |
| **Continuity** | The practice of keeping everything that should match between shots and scenes consistent. |
| **State** | The condition of a changeable element at a given moment: a sleeve torn or whole, a flask with its puck or without. |
| **Continuity bible** | The master list of every element and its state in every scene. |
| **Lined script** | The script supervisor's copy with vertical lines showing which part of each scene each setup covers. |
| **Coverage** | All the shots taken of one scene, from all setups. |
| **Screen direction** | Which way, left or right in the frame, a character moves or looks. |
| **Eyeline** | Where a character is looking, including toward which side of the frame. |
| **Line of action** | The imaginary line between two characters (or along a movement). Keeping all setups on one side of it keeps screen direction consistent (the 180-degree rule). |
| **Hero prop** | A prop that the story depends on and the camera sees closely. |
| **Plant / payoff** | A detail placed early (plant) that pays off later. |
| **Key shot** | The shot a scene cannot lose: the frame in which its event is seen (A2's term). |
| **Insert** | A close shot of an object or a hand. |
| **Externalize** | To turn something inside a character (a thought, a memory, a feeling) into something the audience can see or hear. |
| **Iterative passage** | Prose that tells once what happened many times ("Every time the old woman came up..."). The term is Gérard Genette's. |
| **Summary passage** | Prose that compresses a stretch of time into a few sentences, without a moment-by-moment scene. |
| **Composite scene** | One screen scene built from material that the source spreads over several moments or places. |
| **Transitive verb** | A verb that takes a direct object: "to warn *him*". Only transitive verbs pass the playable-action test. |
| **Juxtaposition** | Placing two things side by side; in film, one shot directly after another so the viewer compares them. |
| **Cast number** | A fixed ID number given to each role in the breakdown, usually in order of size (1 = lead). Strips and schedules use the number, not the name. |
| **Look** | One complete appearance of a character at one point in the story: costume, hair, makeup and injuries together. Each look gets an ID (IONA-L2) that every shot and prompt cites. |
| **Blocking** | Where the actors stand and how they move during a scene. |
| **Previs** | Short for previsualization: a rough 3D or animated version of the shots, made before the final images, here usually in Blender. |
| **Practical** | A light or effect that physically exists in the scene and can be seen or used by the characters (a torch, a desk lamp, sparks), as opposed to one added later. |
| **Compositing** | Layering separately made images into one frame (a graphic over a shot, a screen image into a monitor). |
| **Image-to-video** | A video generator mode that starts from a supplied still image as the first frame. |
| **Reference asset** | An approved image (or model) of a character, prop or set that every later generation copies from, so it looks the same each time. |
| **Diegetic sound** | Sound that exists in the story world and the characters could hear (a radio, a gunshot). Non-diegetic sound (score, narration) is heard only by the audience. |
| **Intercut** | Cutting back and forth between two places where action happens at the same time (two ends of a phone call). |
| **Master shot** | A wide shot that covers a whole scene, or a large part of it, in one take; closer shots are then cut into it. |
| **Single / two-shot** | A shot framing one person / two people. **Over-the-shoulder (OTS):** a shot past the back of one person's head and shoulder onto the other's face. |
| **Push-in** | A camera move toward the subject that makes it grow in the frame; it tells the audience "this matters". |
| **Locked-off shot** | A shot in which the camera does not move at all. |
| **Establishing shot** | A wide shot that shows where a scene takes place before the action begins. |
| **Dissolve** | A transition in which one shot fades out while the next fades in over it; it usually signals time passing. |
| **Match cut** | A cut between two shots whose shapes, movements or objects line up, linking the two moments. |
| **Sound bridge** | Sound from the next scene that starts before the cut (or sound from the last scene that continues after it), joining the two. |
| **Frame-left / frame-right** | Left and right as the viewer sees the screen, not as the character sees the world. |
| **Epistolary** | Told through letters or other documents written by a character. |
| **Free indirect style** | Third-person narration that slips into a character's own thoughts and words without saying "she thought" ("It was homesickness"). |
| **Dramatic irony** | The audience knows something a character does not. |

---

## 2. Core principles

**P1. Read for change, not for content.** A scene is on the page to deliver one event. Before you plan a single shot, write the event as one sentence. If you cannot, the scene is either a transition (it moves people between places) or it is doing work you have not found yet.

**P2. Keep facts apart from choices.** Weston tells directors to list the facts the script states and, separately, the questions it leaves open. In a pipeline this becomes a rule: every item in the breakdown is labelled fact, inference or invention. Inventions are allowed. Unlabelled inventions are how a breakdown quietly rewrites the story.

**P3. Plan behavior, not results.** "Result direction is inaccurate direction," Weston writes: asking for the look of an emotion ("more worried") instead of what the character is doing. Elia Kazan's note to himself while preparing *A Streetcar Named Desire* (1947) says the same thing from the other side: "Directing finally consists of turning Psychology into Behavior." Every performance field in the breakdown holds a playable action or a physical task, never an adjective.

**P4. The shot is a word; the cut makes the sentence.** David Mamet's *On Directing Film* (1991) argues that "the job of the film director is to tell the story through the juxtaposition of uninflected images". An uninflected shot shows one plain thing (a hand, a hole, a face) without editorializing; meaning comes from what it is cut against. The Kuleshov effect (section 3.1) is the lab version of the same idea.

**P5. Size equals importance.** The rule attributed to Hitchcock: an object's size in the frame should match its importance to the story at that moment. The breakdown uses it to decide which objects get inserts, and how big.

**P6. Plan in three dimensions before two.** Weston: "Consider the physical movement in the camera frame not just in the two dimensions of the view-finder, but in the three dimensions of the characters' world." The floor plan comes before the storyboard, because the storyboard is only a set of views into the floor plan.

**P7. Everything that can change is a state.** Blood, sleeves, shoes, charge bars, which way letters face. The continuity bible records each state per scene, and a scene marked `CONTINUOUS` inherits every state exactly.

**P8. Each document answers one question.** Breakdown sheet: what must we supply? Shot list: what do we shoot? Floor plan: where is everyone? Storyboard: what will it look like? Continuity bible: what must match? Lined script: what did we get? Do not merge them into one blob; downstream tools need each answer separately.

**P9. For prose, film cannot assert; it can only show.** The literary critic Seymour Chatman's 1980 essay "What Novels Can Do That Films Can't (and Vice Versa)" makes the case that film has no easy way to state a property or a judgment the way a narrator's sentence does. Every sentence of narration must become something seen or heard, or be cut on purpose.

**P10. When unsure, ask.** A question in the open-questions list costs nothing. A confident wrong guess costs every downstream generation that depends on it.

---

## 3. Part A: the director's script analysis

### 3.1 The sources and what each one contributes

**Konstantin Stanislavski.** The acting system behind almost all modern script analysis. Elizabeth Reynolds Hapgood's translation (*An Actor Prepares*, 1936) divides a role into *units*, each with an *objective*, joined by a *through line of action* (the unbroken chain of one objective after another) toward a *super-objective* (the want behind the whole role). Jean Benedetti's translation (*An Actor's Work*, 2008) restores closer renderings of Stanislavski's words, *bits* (*kusok*) and *tasks* (*zadacha*). A task is framed as a problem to solve ("What do I need to make the other person do?"), and the action is what the character does to solve it; keep the two apart in the breakdown (objective field versus playable-action field). The popular story that "beat" came from Americans hearing "bit" in a heavy Russian accent is repeated by Wikipedia and many teachers but has no primary source; do not repeat it as fact. The word *obstacle* belongs to the American teaching that grew from Stanislavski. Uta Hagen's questions for the actor (six steps in *Respect for Acting*, 1973, expanded to nine questions in *A Challenge for the Actor*, 1991) include "What do I want?", "What's in my way?" and "What do I do to get what I want?", which is the objective / obstacle / action triad in plain words.

**Harold Clurman and Elia Kazan: the spine.** Clurman's *On Directing* (1972) asks the director to state the spine of the play and of each character as an action verb phrase. Kazan's production notebook for *Streetcar*, published in Toby Cole and Helen Krich Chinoy's anthology *Directors on Directing* (revised edition, 1963) and again in *Kazan on Directing* (2009), gives each principal character a one-line spine (Blanche's is to find protection) and then tests every scene against it. The method to take from Kazan is the notebook itself: one page per character, a spine at the top, and underneath it the behavior (what they do with their hands, where they sit, what they reach for) that makes the spine visible.

**Judith Weston.** *Directing Actors* (1996) and *The Film Director's Intuition* (2003). Her working tools for a director are verbs (playable actions), facts (the situation and backstory the script states), images (personal pictures that make a fact vivid to an actor), events, and physical tasks. Her script-analysis method in *Directing Actors* starts from a list of facts and a list of questions, and she warns against result direction (asking for the look of an emotion). Before each take she suggests asking the actor: "Do you know what your character wants from the other character?" She tells directors to use "through-line, beats, and story subtext to understand the structure of a script, and thus be able to create its emotional events." (Subtext is what a character means or wants underneath the words; through-line is the character's want carried across the whole script.) (The quotations in this file are from her *MovieMaker* article, reprinted at actioncutprint.com and checked against its text on 2026-09-27; the facts-and-questions method and the list of tools are from the books.)

**David Mamet.** *On Directing Film* (1991), from his classes at Columbia University's film school. Three ideas matter here. First, the uninflected image and the juxtaposition (P4). Second, the question he puts to every scene, "What does the protagonist want?", "Because the scene ends when the protagonist gets it." (McKee says the same in *Dialogue*: "If the writer were to grant the character his scene intention, the scene would stop.") Third, entering a scene late and leaving early: "To get into the scene late and to get out early is to demonstrate respect for your audience." His memo to the writers of the CBS series *The Unit* (dated 19 October 2005, widely circulated online from about 2010) boils this down to three questions for every scene: "Who wants what? What happens if they don't get it? Why now?" The same memo: "If you pretend the characters can't speak and write a silent movie, you will be writing great drama." That sentence is the best single test for a visual breakdown.

**Steven D. Katz.** *Film Directing Shot by Shot: Visualizing from Concept to Screen* (Michael Wiese Productions, 1991). The practical manual for turning a scene into setups: storyboarding, production design, staging actors in depth, and overhead staging diagrams paired with the frames they produce. Use it as the model for the floor plan plus storyboard pairing in section 5. Its most transferable habit: for every staging idea, draw the overhead first, then the frames each camera position would produce, and choose between staging options by comparing those frames, not by imagining them.

**Alfred Hitchcock and François Truffaut.** *Hitchcock* (French 1966, English 1967; revised 1984), the book-length interview. Two tools. (1) Size equals importance. The wording "the size of an object in the frame should equal its importance in the story" is widely attributed to these conversations; I could not confirm the exact sentence in the book, so treat it as a paraphrase. The practice is visible in *Notorious* (1946), where the camera cranes down from a wide view of a party to the key in Ingrid Bergman's hand, and in *Young and Innocent* (1937), where a crane travels across a ballroom to the drummer's twitching eyes. (2) Suspense versus surprise: if the audience knows the bomb is under the table, a dull conversation becomes unbearable. The breakdown consequence: decide, per scene, what the audience knows that a character does not, and make sure a shot delivers that knowledge in time.

**The Kuleshov effect.** In Soviet film experiments of the late 1910s and early 1920s, Lev Kuleshov is reported to have cut the same shot of the actor Ivan Mozzhukhin's face against a bowl of soup, a dead child in a coffin, and a woman on a divan; audiences praised the actor's hunger, grief and desire. The main account is Vsevolod Pudovkin's; the footage is lost. Replications disagree: Stephen Prince and Wayne Hensley (*Cinema Journal*, 1992) found little effect, while Daniel Barratt and colleagues (*Perception* 45(8), 2016) found a real but modest one. Hitchcock demonstrated his own version on the CBC programme *Telescope* in 1964. Pipeline consequence: the shot before a face shapes how the face is read, so the breakdown decides what the face is cut against. It does not license a blank face; the effect is modest, so the performance must still be compatible with the reading.

**Walter Murch.** *In the Blink of an Eye* (1995; 2nd ed. 2001) ranks what a cut must preserve: emotion 51%, story 23%, rhythm 10%, eye-trace (where the viewer's eye is on the screen at the moment of the cut) 7%, the two-dimensional plane of the screen 5%, three-dimensional space 4%. Audiences forgive a spatial mismatch far sooner than a false emotion: track continuity strictly, and break it only on purpose, for emotion.

### 3.2 The director's pass, step by step

Run this on every scene after parsing. It produces the "analysis" block of the scene record.

1. **Read the whole source twice before writing anything.** Plants in scene 1 often only make sense from scene 30.
2. **Facts list and questions list** (Weston). Facts are quoted or pointed to by line. Questions are anything the text leaves open that a department will have to decide ("Does Iona still have her torch in the cage?").
3. **Spines.** One verb phrase per principal character for the whole story.
4. **Per scene:** the event (one past-tense sentence); the driver (who makes the scene happen); and for each character present, objective, obstacle and playable action. Answer Mamet's three questions.
5. **Beats and turning point.** Use A2's method. Mark which beat is the turning point.
6. **Translate each beat into playable actions**, one verb per beat per character. Test (full version after the output block): can you do it *to* the other person, and would they notice? "To warn" passes. "To be scared" fails; convert it ("to hide it from him").
7. **What must be seen.** The key shot; every insert the story depends on (size equals importance); every reaction the audience needs, and what it is cut against (Kuleshov).
8. **What the audience knows.** Note any gap between audience knowledge and character knowledge (Hitchcock's bomb), and which shot creates it.
9. **Physical tasks and activity.** What the hands are busy with while the scene happens. Weston treats a physical task as an actor's tool; for AI video it is the most reliable way to give a figure believable motion.
10. **Entry and exit.** Where the scene can start late and end early without losing the event.

Output fields (one block per scene):

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

A starter list of playable actions (this list is mine, not Weston's): to warn, to test, to probe, to dismiss, to reassure, to soothe, to needle, to challenge, to accuse, to confide in, to plead with, to bargain with, to stall, to deflect, to shut down, to command, to protect, to recruit, to comfort, to punish, to disarm, to tease, to corner, to rebuff, to release.

**The playable test, two parts.** (1) The verb fits "I ___ you"; a particle or preposition that belongs to the verb is allowed ("I shut you down", "I plead with you"). (2) It aims to change what the other person does or feels. "To bristle" fails part 2: it is a reaction, not an attempt on the other person; the attempt behind it might be "to rebuff". "To inspect" fails part 1: it is a physical task, so it goes in the `physical_task` field, not the verb list. A beat in which a character is alone, or acts only on objects, gets a physical task and no playable action.

---
## 4. Part B: parsing screenplay format reliably

### 4.1 The standard elements and what each means for production

| Element | Looks like | What it tells production |
|---|---|---|
| Scene heading | `INT. FREIGHT SHAFT - CONTINUOUS` | Interior or exterior (`INT.`, `EXT.`, `INT./EXT.` for a scene that moves between, `I/E`); the place, often narrowing from building to room with dashes; the time. |
| Time word | `DAY`, `NIGHT`, `MORNING`, `DAWN`, `BEFORE DAWN`, `LATER`, `MOMENTS LATER`, `CONTINUOUS`, `SAME` | `CONTINUOUS` means no time passes: the camera follows action from one place into the next and every state carries over. `LATER` / `MOMENTS LATER` mean a small gap (ellipsis) in which states may change. `SAME` usually marks the same moment in a different place (for intercutting). |
| Action line | Present tense, short paragraphs | What is seen and heard. By convention each new paragraph often implies a new shot or a new beat, but that is a writer's habit, not a rule. |
| Capitals in action | `JUDE, forties`, `A GUNSHOT`, `FLASK` | Capitals are overloaded. They mark a character's first appearance, an important sound, a key prop, emphasis, and on-screen text. Classify each capitalized token; never treat all capitals as one category. |
| Character cue | `IONA` | Speaker. Strip the extension before counting characters. |
| Extension | `(V.O.)`, `(O.S.)`, `(O.C.)`, `(CONT'D)`, custom tags such as `(RECORDED)` | How the voice is heard. `(O.C.)`, off camera, means the same as `(O.S.)`. `(CONT'D)` means the same speaker continues after action; it is not a new speech. Custom tags need a note in the sound column. |
| Parenthetical | `(through the torch)`, `(beat)`, `(taps the right dish)` | A delivery note, an addressee, a pause, or a small action inside a speech. `(beat)` is a pause, not a McKee beat. |
| Transition | `CUT TO:`, `DISSOLVE TO:`, `MATCH CUT TO:`, `SMASH CUT TO:`, `FADE IN:`, `FADE OUT.`, `CUT TO BLACK.` | Editing intent. Most scripts only mark unusual transitions; the default between scenes is a cut. |
| Special headings | `INSERT`, `POV`, `BACK TO SCENE`, `INTERCUT`, `MONTAGE`, `SERIES OF SHOTS`, `SUPER:`, `TITLE CARD` | Shot-level instructions inside a scene. `POV` is a point-of-view shot (the camera sees what a character sees). `SUPER:` means text superimposed on the picture. `INTERCUT` means cut back and forth between two places for the rest of the passage. |
| Secondary headings | `ANGLE ON JUDE`, `CLOSE ON THE FLASK`, `WIDER`, `ON THE MONITOR`, a bare `LATER` | A new shot or a small time skip **inside** the current scene. Never start a new scene record at one; record it as a shot request (or an ellipsis) within the scene. |
| Time-frame markers | `FLASHBACK`, `BACK TO PRESENT`, `END FLASHBACK`, `DREAM SEQUENCE`, `(PRESENT DAY)` | The story time changes. Add a `time_frame` field (present, past, dream) to every scene until the closing marker; continuity states in a flashback belong to the earlier story day, not the current one. |

Page length: a correctly formatted page (12-point Courier, standard margins) runs about a minute of screen time on average. That is a rule of thumb for the whole script, not a measure of any one scene: an assistant director writing in *MovieMaker* puts it as "Equal ink, but not equal time on the screen."

### 4.2 Fountain

Fountain is a plain-text screenplay markup created by John August and Stu Maschwitz (specification at https://fountain.io/syntax, checked 2026-09-27). The rules a parser needs:

- **Scene heading:** a line beginning `INT`, `EXT`, `EST`, `INT./EXT`, `INT/EXT` or `I/E` (any case), followed by a dot or a space, with a blank line before it and a blank line after it. Force any line to be a heading with a leading period (`.SNIPER NEST`). Scene numbers go between hash marks at the end: `INT. HOUSE - DAY #1#`.
- **Character:** a line entirely in capitals, with a blank line before it and none after. Force with `@` (keeps mixed case: `@McClane`). Extensions follow the name: `MOM (O.S.)`.
- **Dialogue:** the lines after a character or parenthetical. **Parenthetical:** a line in parentheses inside a dialogue block.
- **Transition:** capitals ending in `TO:` surrounded by blank lines, or forced with `>`.
- **Centered text:** `>THE END<` (a `>` line that also ends in `<` is centered action, not a transition).
- **Title page:** `Key: value` pairs at the very top.
- **Sections:** lines starting with `#`, `##`, `###` mark acts and sequences for the writer's outline. They are **not printed**.
- **Synopses:** lines starting with `=`. **Not printed.**
- **Notes** `[[...]]`, **boneyard** (ignored text) `/* ... */`, **page break** `===`, **dual dialogue** (two characters speaking at once, printed side by side) `^` after the second name, **lyrics** `~`, emphasis `*italic*`, `**bold**`, `_underline_`.

### 4.3 The variant markup in *The Catch* (and why a Fountain parser will break on it)

| Marker in *The Catch* | Meaning in *The Catch* | Meaning in Fountain | Risk |
|---|---|---|---|
| `## ` at line start | Scene heading | Section (outline, not printed) | A Fountain tool would delete all 30 scene headings. |
| `@` | Character cue | Forced character | Same. Safe. |
| `>` | Transition (`> FADE IN:`, `> CUT TO BLACK.`) | Forced transition | Same. Safe. |
| `=` | Title-page lines at the top; on-screen title cards later (`= THE CATCH` after the first `CUT TO BLACK.`, `= THE END` at the close) | Synopsis (not printed) | A Fountain tool would hide the mid-film title card and the end card. |
| Parenthetical on its own line under a cue | Delivery note | Same | Safe. |

Counts from the file (computed 2026-09-27, rechecked in review): 30 scene headings; 221 character cues (IONA 94, SAYE 57 plus 5 as SAYE (RECORDED), ELI 37 plus 2 as ELI (V.O.), JUDE 15 plus 2 as JUDE (V.O.), NELL 8, IONA (O.S.) 1); 3 transitions (`> FADE IN:`, two `> CUT TO BLACK.`); 18 parenthetical lines; 8 `=` lines (6 title-page lines, then the two cards `= THE CATCH` and `= THE END`).

**Parsing procedure (any screenplay text):**

1. Detect the dialect. If any line starts with `## INT` or `## EXT`, the file is in the *Catch* dialect: every line starting `## ` is a scene heading, every line starting `@` is a character cue, and **no other line is a cue**, however capitalized it is (`IONA VALE.` and `NELL ROWAN. FLIGHT TEST.` stand alone in capitals but are on-screen text inside action). If lines start with `=` at the very top, treat the leading block as the title page; treat any later `=` line as an on-screen title card. Otherwise parse as Fountain (4.2), and if the file has no markup at all, as standard screenplay text (4.1).
2. Split into scenes at scene headings only, never at secondary headings (4.1). Number them in order (1, 2, 3...) unless the source already carries numbers, in which case keep the source's numbers exactly.
3. Split each heading into `int_ext` (the `INT.`, `EXT.`, `INT./EXT.` or `I/E` prefix), `place` (everything after the prefix and before the last ` - `, space-hyphen-space, so hyphenated names survive), `time`, and any trailing modifier in parentheses (`(ON THE TABLET)`, `(RECEIVING ROOM)`). A modifier after the time is a presentation note; a modifier inside the place is an alias.
4. Inside a scene, classify each block: cue (plus extension), parenthetical, dialogue, action, transition, title card. For each `(V.O.)` cue, read the parenthetical under it to fix how the voice is heard: *The Catch* uses `(in her ear)` and `(over the radio)`, so JUDE (V.O.) and ELI (V.O.) are radio voices heard by Iona in the scene's time, not narration; `SAYE (RECORDED)` is a playback on Iona's wrist display. A later V.O. from the same speaker in the same sequence with no parenthetical inherits the earlier one's source (JUDE's "Cage is coming. Thirty seconds." in scene 4 is the same earpiece as his "Was that you?" in scene 2; ELI's second line in scene 21 is the same radio). Record this in a `voice_source` field: narration, radio or phone, recording, thought.
5. Tag capitalized tokens in action lines as one of: character introduction, sound cue, prop introduction, on-screen text, emphasis. On-screen text is anything a character reads (`IONA VALE.`, `NELL ROWAN. FLIGHT TEST.`, `RECEIVING`). Apply these tests in order and stop at the first that fits:
   1. A name or role followed by a description, or a role's first appearance (`JUDE, forties`, `A GUARD`, `A NURSE`, `THE FIGURE`) → character introduction.
   2. Printed, displayed or read by someone (`STOP`, `RECEIVING`, `PASSAGE FLOOR`, `HULL CLEARANCE`) → on-screen text.
   3. A noise, or an action whose point is its noise (`A GUNSHOT`, `CLACK`, `METAL SHRIEK`, `CLICK`, `PUMP`, `HUM`, `ALARM`, `FIRES`) → sound cue (and, for an action, also an action beat).
   4. An object's first mention (`FLASK`, `PUCK`, `ENGINE`, `CELL`, `VESSEL`, `ANIMAL`) → prop or creature introduction.
   5. Anything else (`UP`, `STOPS DEAD`, `RED`, `GREEN`) → emphasis; then check whether it marks a state change (the shell's light turning `RED` then `GREEN` is a state row).
6. Flag inline shot instructions inside action: `VISOR VIEW:` (a point-of-view shot with a display overlay), `BLACK.` (a black frame inside the scene), `(ON THE TABLET)` (the whole scene is seen on a screen within the frame).
7. Normalize characters: `DR SAYE` in the introduction and `SAYE` in cues are one person; `THE FIGURE` is a character even though it never speaks.
8. Normalize sets (4.4).
9. Output one record per scene and a list of open questions for anything ambiguous.
10. Check the parse against counts before going on: number of scene records equals number of heading lines; every cue name after stripping extensions is in the cast list; every `=` line after the title page appears as a title card. For *The Catch* the expected figures are in the counts line above; any mismatch means the dialect was misread.

### 4.4 Normalizing sets: many headings, few places

Writers name the same place in different ways. The breakdown needs one canonical set name per place, or the schedule and the reference images will fork.

| Headings as written in *The Catch* | Canonical set | Evidence (fact / inference) |
|---|---|---|
| `MEDICAL FACTORY - LOADING TUNNEL` (1) | FACTORY: LOADING TUNNEL | Fact. |
| `FREIGHT SHAFT` (2), `FREIGHT CAGE` (6) | FACTORY: FREIGHT SHAFT, with the CAGE as a movable set piece | Fact: the cage runs in the shaft. |
| `MEDICAL FACTORY - TREATMENT FLOOR` (3, 11), `TREATMENT FLOOR - CORRIDOR` (5), `ELI'S ROOM` (4) | FACTORY: TREATMENT FLOOR (corridor, Eli's room, other rooms) | Fact. |
| `QUARANTINE - IONA'S ROOM` (14, 16, 29, 30), `JUDE'S ROOM` (15), `GLASS PARTITION` (13), `DEMONSTRATION ROOM` (12), `OBSERVATION ROOM` (17) | Same TREATMENT FLOOR rooms, now sealed | Inference: Saye says "The sealed rooms are here" (11), and the grey box whose "needle lies flat" is over Iona's bed in both 11 and 14. |
| `MAINTENANCE PASSAGE` (7), `THE PASSAGE (RECEIVING ROOM)` (18), `RECEIVING ROOM` (28) | FACTORY: PASSAGE, later dressed as RECEIVING ROOM | Fact: scene 18 says "The same concrete where she knelt with Jude." |
| `SHIP - SERVICE CAVITY / HUMAN ROOMS / COLLECTION ROOM / OUTER RECESS (THE DIP)`, `EXT. SHIP - LEDGE`, `EXT. BESIDE THE SHIP` | SHIP sets | Fact. |
| `EXT. STREET`, `INT. IONA'S CAR`, `INT. SAYE'S HOUSE - KITCHEN` | STREET, CAR, SAYE'S KITCHEN | Fact. |

---

## 5. Part C: the production breakdown

### 5.1 Lock and number the scenes

Scene numbers are fixed when the script is locked for production. Scenes added later take letter suffixes (a new scene between 12 and 13 becomes 12A); cut scenes stay in the script as `OMITTED` so numbers never shift. Revised pages are issued in a sequence of paper colors so everyone can see which version they hold. For the pipeline: number once, never renumber, and give every shot an ID that includes its scene number.

### 5.2 Measure in eighths

Each page is divided into eight parts of about one inch; a scene's length is written as whole pages plus eighths (`2 3/8`). Very short scenes are still written as at least 1/8. The *MovieMaker* piece on eighths (https://www.moviemaker.com/whats-in-an-eighth-assistant-director/, checked 2026-09-27) also notes that a single-camera feature aims for roughly 20 to 30 camera setups in a 12-hour day. Eighths are for scheduling effort, not for timing the cut.

For *The Catch*, a line-count model (61 characters per action line, 35 per dialogue line, 55 lines per page) gives about 42 to 44 pages. Treat per-scene figures as estimates; only a correctly formatted PDF gives true eighths. Estimated examples: scene 8 (`EXT. STREET`) 2/8; scene 6 (`FREIGHT CAGE`) 2 2/8; scene 13 (`GLASS PARTITION`) 3 5/8.

### 5.3 The breakdown sheet

**Header fields:** sheet number; scene number; scene heading; INT/EXT; day or night; story day; page length in eighths; set; location (real place or generated environment); one-line synopsis (what happens, not how it feels).

**Element categories.** Traditionally, a first assistant director (the person who runs the schedule and the set) marks each element in the script with a color or symbol. The widely used code (Wikipedia, "Script breakdown", citing Bastian Cleve's *Film Production Management*, 2012 edition, p. 25, checked 2026-09-27; productions vary):

| Category | Mark | What goes here |
|---|---|---|
| Cast | Red | Every speaking character (Cleve's definition: "any speaking actor"). In practice also any named role played by a performer even if silent; *The Catch*'s THE FIGURE goes here as well as under visual effects. Each cast entry gets a cast number. |
| Stunts | Orange | Any action needing a stunt performer or coordinator. |
| Extras, silent | Yellow | Non-speaking people who do something specific. |
| Extras, atmosphere | Green | Background people. |
| Special effects | Blue | Practical effects done on set: sparks, breaking glass, smoke. |
| Props | Purple | Objects important to the script or handled by an actor. |
| Vehicles and animals | Pink | Any vehicle; any animal. |
| Sound effects and music | Brown | Sound or music that must exist on set (playback, a radio a character switches off). |
| Wardrobe | Circle | Specific costumes, including damaged or dirtied versions. |
| Makeup and hair | Asterisk | Wounds, scars, blood, aging, beards. |
| Special equipment | Box | Unusual gear: crane, underwater housing, wire rig. |
| Production notes | Underline | Anything unclear about how something happens. |

Most modern sheets add **set dressing** (objects in the set that nobody handles: the empty beds on the treatment floor, the bare fridge in Saye's kitchen; the mint pot is *not* set dressing, because Saye tears a leaf from it and the taste test turns on it, so it is a prop), **visual effects** (anything finished in the computer), and **greenery** (plants and trees supplied for the set) where relevant. **For an AI pipeline, add four more:** *on-screen text and graphics* (exact wording and whether it reads normally or mirrored), *screens within the frame* (what each monitor, tablet, visor or wrist display shows), *states* (section 6), and *reference assets needed* (which character, prop or set needs a reference image for consistency). Keep two more categories from live-action practice even for AI: **weapons** (on a set they carry safety rules; in generation the same gun must appear in every shot, so it needs a reference) and **consumables and breakables** (anything eaten, broken, burned or spilled on camera; a set needs multiples, and each generated shot needs the item's state: roll whole, roll halved, half eaten).

**Filling a sheet from action lines, rule by rule.** If a character names or handles an object, then it is a prop. If an object is only described as part of the room, then it is set dressing. If an object changes state on screen (breaks, burns, is eaten), then it is a prop and it also gets a continuity row. If something moves, flies, vanishes or changes in a way no real object could, then it is visual effects. If it happens physically on the set (sparks, smoke, rain), then it is special effects, and if it cannot be filmed, also visual effects. If a person falls, is thrown, fights or is carried, then it is a stunt.

### 5.4 Story days

Number the story's days in order: D1, N1, D2... Every costume and injury is tracked against story days, not against shooting order. *The Catch*: scenes 1 to 10 are night 1 (10 is `BEFORE DAWN`); 11 to 13 are day 2 (Saye's "Yesterday" in 11 places Eli's message on the day before night 1); 14 to 16 night 2; 17 to 28 day 3 (17 is `DAWN`, "Neither of them has slept"); 29 (`DAY`) and 30 (`NIGHT`) could be later on day 3 or days afterwards; the script does not say. That is an open question: the healing of Iona's hand ("her bandaged hand" in 30) and Jude's shoulder ("his arm strapped across his chest" in 29) depends on it.

**Looks.** Give each character a numbered look for every change of costume, hair, makeup or injury, and record which scenes use it. *The Catch*, Iona: L1 (scenes 1 to 6: blue shirt with both sleeves, an inference from scene 21; tooth chipped from scene 2 on; palm skinned at the end of 6), L2 (scenes 7 to 10: one sleeve gone, palm skinned, Jude's blood on her hands), L3 (scenes 11 to 17: bandaged palm, printed wristband, Jude's blood still "under her nails" in 12; her clothes are not stated, so any change is an invention to be labelled), L4 (scenes 18 to 28: white pressure suit, engine harness, helmet in 28), L5 (scenes 29 and 30: inside the plastic tent, hand still bandaged in 30). A look change inside a scene (the sleeve torn off during 6 or 7) is a state change, logged in the continuity bible with its anchor line. The list of looks per character, with their scenes, is the AI equivalent of the "day out of days" report (a table of which cast member works on which day): it tells you which reference images to make and how often each is reused.

### 5.5 Stripboard

One strip per scene, carrying number, set, INT/EXT, day or night, eighths and cast numbers. The traditional strip colors: white for interior day, yellow for exterior day, blue for interior night, green for exterior night. Strips are reordered so all scenes on one set shoot together. The AI equivalent is batching: generate all shots that share a set, a character look and a lighting state together, from the same reference assets, so they match.

### 5.6 The shot list

Standard columns: scene number; shot number (a letter or number within the scene, often with I and O skipped because they look like 1 and 0); camera setup number; description (who does what, in one line); shot size; angle and height; lens; movement; subject and eyeline; characters in shot; dialogue or action covered (first and last words); sound notes; special equipment; estimated duration; notes. For the pipeline add: key shot yes/no; states in play (from the continuity bible); references to use; on-screen text in frame.

**Shot sizes, in plain words** (B1 goes deeper): extreme wide (the place dominates, people small); wide or long shot (whole bodies with room around them); full shot (head to feet); medium long (knees up); medium (waist up); medium close-up (chest up); close-up (the face); extreme close-up (part of the face, or a small object filling the frame); insert (a close shot of an object or hand).

**Coverage or designed shots.** On a set, a scene is usually covered: a master shot of the whole action, then closer shots (singles, over-the-shoulders, inserts, reactions) of the same action from several setups, so the editor can choose later. In AI video every setup is a separate generation and the performance will not repeat exactly between generations, so matching several angles of one action is the hardest thing to get. Rules: If a stretch of action depends on continuous physical cause and effect (the cage stops, Iona is thrown flat), then plan it as one designed shot or a short chain of shots that each start where the last ended, not as master-plus-coverage. If a dialogue scene needs cutting between faces, then plan singles whose content does not have to match frame-for-frame (each line generated as its own shot), and hold the wide for the start and the turning point only. Plan the edit order now (which shot follows which), because with AI there is no spare footage to rescue a missing angle.

**Two cutting checks for each pair of consecutive shots of the same subject:** change the shot size clearly or move the camera angle by at least about 30 degrees (the "30-degree rule"; otherwise the cut looks like a skip in the film, a *jump cut*), and keep the camera on the same side of the line of action unless the crossing is planned.

### 5.7 The storyboard (optional)

Frames in order, each tied to a shot-list row, with arrows for movement and a caption for sound and dialogue. Katz's book is the model: a storyboard frame is always paired with a position on the floor plan. In this pipeline storyboarding is optional; a shot list plus floor plan is enough to drive previs or prompts, and boards are generated from them only when the user wants them.

### 5.8 The floor plan

Draw the set from above, to rough scale. Mark walls, doors, windows, furniture, light sources. Mark each character's start position and every move as an arrow with a number (IONA 1 to IONA 2). Tie every move to a beat: if a character moves, the move should start on a new beat or a change of tactic and be listed against that beat; if a move has no beat behind it, cut it, because unmotivated movement reads as noise and costs a generation. Moves the text gives (Iona "moves between her and Eli" in scene 10) are facts; moves you add are inventions. Mark each camera setup as a small camera with its lens and a wedge for its field of view (the area the lens can see). Draw the line of action. Write left and right only as **frame-left** and **frame-right** for a named setup: prose and action lines give left and right relative to a character, and the two are opposite whenever the camera faces the character. Katz and Daniel Arijon's *Grammar of the Film Language* (1976) are the standard references. Tools: paper, Shot Designer (Hollywood Camera Work), StudioBinder, or Blender's top orthographic view (a flat view from directly above, without perspective), which becomes previs directly.

### 5.9 The script supervisor: continuity notes and the lined script

The script supervisor watches every take for what must match. Their notes (Pat P. Miller, *Script Supervising and Film Continuity*, 3rd ed. 1999; Avril Rowlands, *The Continuity Supervisor*, 4th ed. 2000; Mary Cybulski, *Beyond Continuity*, 2013) cover:

- **Screen direction and eyelines:** who exits frame-left enters the next shot from frame-right if the movement continues; in a conversation one person looks frame-left and the other frame-right, and the line of action is not crossed without a motivated move. The same applies across a whole sequence: a journey toward a goal keeps one direction of travel (always frame-right to frame-left, say) until the story turns it. In *The Catch* the travel is vertical: Iona climbs toward frame-top in scene 2, the cage descends toward frame-bottom in scene 6, and the story's reversal is written as a reversal of screen direction ("The brick slides past the wrong way", "The cage is going UP"). So keep "up the shaft" as frame-top in every setup of scenes 1 to 7, and let the reversal be the one planned break.
- **Matching action:** a movement that runs across a cut (a hand reaching for the latch) must be at the same stage and speed on both sides; cutting in the middle of a movement hides the join.
- **Prop handling and states:** which hand holds the cup, on which word it is lifted, how full it is.
- **Wardrobe, hair, makeup and injuries:** sleeves, dirt, wet or dry; where the wound is and how it progresses by story day.
- **Time of day and weather:** light direction and quality must match within a scene.
- **Dialogue as spoken and takes:** changes from the page; each take's length, problems, and the takes the director wants printed (circled).

**The lined script.** On a copy of the script, the supervisor draws one vertical line per setup through the portion of the scene that setup covered, labelled at the top with the scene and setup (`6C`). A straight line means the speaker is on camera for that stretch; a wavy line means the speaker is off camera while the text runs. The facing page (the left-hand page opposite each script page) logs each setup and take: lens, description, timing, circled takes, notes. For the pipeline, the lined script becomes the **coverage map**: for every line of dialogue and every action beat, which planned shots show it, and whose face is on screen. Checking it reveals beats nobody planned to show.

### 5.10 What each document becomes downstream

| Document | Feeds |
|---|---|
| Breakdown sheet | Asset lists: character, costume, prop and set references to design or generate once and reuse. |
| Story days, looks and continuity bible | Per-shot state fields in every prompt ("look IONA-L2: one shirt sleeve missing, palm skinned"; the side comes from the bible, and stays an open question until decided). |
| Stripboard | Generation batches grouped by set, look and light. |
| Shot list | The generation queue: one row, one clip or still. |
| Floor plan | Blender blocking: character marks, camera positions, lens. |
| Storyboard | Optional first frames for image-to-video tools. |
| Lined script / coverage map | Edit plan; a check that every beat has a shot. |

---
## 6. Part D: continuity as state tracking

A continuity bible is a table: rows are changeable elements, columns are scenes, cells are states. Build it during the breakdown, not after. An element gets a row the moment anything about it can change (a sleeve, a tooth, a bandage, a charge bar, a needle on a dial). Every state change is anchored to a source line ("scene 7, line 302: *pressing what is left of her shirt sleeve*"); if the source never says when a change happens (a bandage simply appears), log it as an inference at the scene where it is first visible. Story-specific rules that change how things look get a row too. Decision rules 7 to 9 and 12 cover `CONTINUOUS`, replays and story rules; worked examples 2 and 4 sketch the *Catch* bible.

**Row format** (one row per element per scene):

```yaml
- element: IONA_PALM          # canonical name; side recorded once decided
  scene: 7
  enter: skinned              # must equal previous scene's exit
  exit: skinned
  changes: []                 # none here; in scene 11 it becomes [{to: "bandaged", anchor: "line 498: dressing Iona's palm", label: fact}]
  label: fact                 # fact | inference | invention
  anchor: "line 286: Her palm drags across the bright steel."
```

**The state-diff procedure, run after each scene is broken down:**

1. For every row, copy the previous scene's `exit` into this scene's `enter`. If the heading is `CONTINUOUS`, this copy is binding, and so are the characters' positions and what they hold at the end of the previous scene.
2. Walk the scene's lines. Each line that changes a state adds an item to `changes` with its line number. `exit` is the last state reached.
3. If this scene is not `CONTINUOUS` (time has passed since the last one) and a state differs from what the previous exit implies (a fresh dressing, clean hands), log the change at the scene where it first shows, labelled inference, and name the time gap that allows it.
4. Flag any row whose `enter` differs from the previous `exit` with no change item and no ellipsis. That is a continuity error, in the source or in the breakdown; ask rather than guess.
5. For elements that must match inside a scene (which hand holds the flask, how full the cup is), add a per-shot state column in the shot list, not only a per-scene one.

---

## 7. Part E: adapting prose to the screen

### 7.1 What prose does that film cannot, and the reverse

A narrator can state a judgment ("she had met stranger sponsors"), summarize years in a clause, enter any mind, and tell once what happened a hundred times. Film shows one moment at a time, from one place, with more visual detail than any sentence could list, but, as Chatman argues, with no built-in way to assert. Of the standard studies (George Bluestone's *Novels into Film*, 1957; Brian McFarlane's *Novel to Film*, 1996), McFarlane's distinction is the useful one for a pipeline: some story material **transfers** directly (the events and their order, the hinge events he calls *cardinal functions* after Roland Barthes), and some needs **adaptation proper** (the narrator's voice, tone, and interior life), which must be rebuilt in film's own means. Linda Seger's *The Art of Adaptation* (1992) is the practical handbook.

### 7.2 The externalization ladder

When the prose puts something inside a character, try each rung in order and stop at the first that works. A rung "works" when a viewer who has not read the source could say what the character is thinking or feeling from picture and sound alone, at least as clearly as the source says it; if the source is itself ambiguous, the rung works when it keeps the same ambiguity. Record the rung used in the adaptation log. Voice-over is near the bottom on purpose.

1. **Behavior.** What would the body do? Kazan's "turning Psychology into Behavior". Prose often supplies it already: Nilay's mother shows gladness by "assigning you a bed and a towel within four minutes".
2. **Object.** A thing the character handles, keeps, avoids or reads: a letter, a form, a photograph. Objects also carry backstory without anyone explaining it.
3. **Juxtaposition.** Cut the face against the thing it is thinking about (Kuleshov; Mamet). The cut does the narrator's job.
4. **Framing and light.** Isolation, empty space in a frame, a light that does not reach someone (B1, B2).
5. **Sound.** A sound the character attends to, or one that carries memory.
6. **Dialogue.** Give the thought to a line spoken to someone, under pressure, in a scene. Prose habits and rules often become lines addressed to a newcomer.
7. **Voice-over.** Use it when the words themselves are the point (a letter, a document, a distinctive voice), and set them against images that do not repeat them. Sarah Kozloff's *Invisible Storytellers* (1988) defends voice-over as a legitimate tool; the pipeline's rule is only that it must add something the picture cannot.
8. **On-screen text.** Dates, places, documents. Keep it rare, exact and legible.
9. **Cut it.** Some interior material is lost in any adaptation. Say so in the notes rather than smuggling it in as description the camera cannot film.

### 7.3 Point of view

Decide for each scene whose scene it is. In a close third-person novel, the camera stays with the point-of-view character: it enters rooms when she does, sees what she sees, and does not show what she cannot know, unless the adaptation chooses dramatic irony on purpose and records the choice. (Chatman's essay works through these questions by comparing Maupassant's story with Jean Renoir's film of it, *Une partie de campagne*, shot 1936, released 1946.) A camera position is a point of view whether you mean it or not.

Concrete rules for the POV field of each scene record:

- If the source is close third person on one character, then set `pov: <that character>` and forbid any shot showing something she cannot see or know at that moment, unless the scene record carries `pov_break: <reason>`.
- If the camera must show what the POV character sees, then plan a POV shot (the camera at her eye position, looking where she looks) followed by her reaction, or an over-the-shoulder that keeps her in frame; the second is safer in AI video because it keeps the character's reference in the shot.
- If the source is first person, then the narrator is the POV character and her voice is the first candidate for any voice-over (still subject to the ladder in 7.2).
- If the source is omniscient, then choose the POV per scene and record it; do not switch POV inside a scene without a shot that carries the switch (a look that hands attention from one person to another).

### 7.4 Finding scenes inside summary

Genette's *Narrative Discourse* (1972; English 1980) names the speeds prose moves at: **scene** (story time roughly equals reading time, usually with dialogue), **summary** (much story in little text), **ellipsis** (story time skipped), and **pause** (description while story time stops). He also separates **singulative** telling (once, of something that happened once) from **iterative** telling (once, of something that happened many times). Film is almost always singulative scene. So:

- A **scene** passage becomes a scene.
- A **summary** passage becomes one of: a short scene that stands for the whole stretch; a montage (a series of short shots showing time passing); a single image that implies it; or nothing, if its information is carried elsewhere.
- An **iterative** passage ("In the evenings she entered the 1924 survey") becomes one dramatized instance chosen to carry the most, or a montage of three or four instances with visible variation. Never film the same action identically several times.
- A **pause** (description) becomes set design, light and one or two establishing images, not a held shot of nothing.

Look for buried scenes: any sentence in summary that contains a place, a time, two people, and a change is a scene in disguise ("In the second week of June the muhtar called the village to the room above the co-op").

### 7.5 Compression and composites

A feature cannot hold a novel. Keep the cardinal functions (the events the plot cannot lose) and compress the rest. Techniques: **composite scene** (two moments in different places merged into one, keeping both events); **composite character** (two minor figures merged); **moving a line** (a reported remark placed in a scene where it can be spoken); **deleting a strand** (Steven Spielberg's *Jaws*, 1975, dropped the novel's affair between Hooper and Ellen Brody). Record every compression in an adaptation log with the source lines it draws on, so later passes know what is invented.

Replace what cannot be filmed well with something that can and that serves the same meaning. Stanley Kubrick's *The Shining* (1980) replaced the novel's topiary animals with a hedge maze. For an AI pipeline this matters doubly: prefer images the tools can render consistently.

### 7.6 Dialogue from reported speech

Reported speech ("Some remembered a clipboard... One man remembered a scarf; his wife remembered no scarf") becomes dialogue by giving each report to a named speaker and letting them contradict each other in the room. Keep the source's actual words wherever it gives them, mark new lines as inventions, and keep inventions short: one line that makes the reported exchange happen is usually enough.

### 7.7 Letters and other embedded texts

Options, from most dramatic to least:

1. **Dramatize what the letter reports.** If a letter describes an event, stage the event and let a few lines of the letter play over it as voice-over.
2. **Voice-over frame.** The letter is read over images of the reader or of the past. Max Ophüls's *Letter from an Unknown Woman* (1948) is built on this: a man reads a letter and the film becomes its story.
3. **Insert.** Show the page in close-up and let the audience read a short, exact phrase.
4. **The act of writing or reading as a scene.** Who writes, where, and how they react.
5. **On-screen text** for short documents.
6. **Cut,** keeping only the information.

A close parallel to *The Long Places*: Cormac McCarthy's novel *No Country for Old Men* (2005) opens its chapters with Sheriff Bell's italic monologues. Joel and Ethan Coen's film (2007) uses Bell's voice-over once, over empty landscape at the opening, and turns the final monologue into a scene in which Bell tells his wife two dreams across a kitchen table. A recurring italic frame does not have to recur on screen; it can open the film, return at the end, and otherwise live in the images. *The Long Places* has exactly this shape: chapters I to XIII each open with an italic letter headed "*To the one who keeps the lamps after me:*"; chapter XIV has none at its head, and the book instead ends by repeating the first letter whole.

**Choosing among the options:**

- If the letter reports an event that can be staged, then use option 1, with at most four to six of the letter's own lines as voice-over.
- If the letter's value is its voice or its rules rather than an event, then use option 2 or 4, and cut the letter to the lines that the images do not already say.
- If the plot depends on the exact words (a date, a name, a signature), then add option 3, an insert of those words only, specified letter for letter.
- If the same framing text recurs through the source, then decide once how often it appears on screen (open only; open and close; every return) and record it as a series rule, not scene by scene.
- If the letter's writer is deliberately unidentified, then show hands, a room, or a page, never a face, and give the voice no feature (accent, age) the source does not.

### 7.8 Time jumps

A cut to a new scene already implies time may have passed. The question is whether the audience must know *how much*. If yes, choose a carrier that belongs to the story world before reaching for a title card: a date written on a document, a change of light or season, a costume or injury change, an object in a new state (a cup of tea gone cold). Jumps backward (flashbacks) need a clearer carrier than jumps forward: a match cut on an object, a sound bridge, or a consistent visual treatment for the past.

### 7.9 Deciding what becomes a scene

Score each passage against five tests: (1) it contains a cardinal function; (2) a value changes in it (A2); (3) it plants something paid off later; (4) it can be shown by behavior and objects rather than explained; (5) it gives a character a first appearance that defines them. Then apply these rules in order and stop at the first that fits:

1. If it passes (1), then it is kept: as its own scene if it also passes (2) or (4), otherwise folded into the nearest scene with the same place or people. A cardinal function is never cut.
2. If it passes two or more tests, then it becomes its own scene.
3. If it passes exactly one test, then fold it into a neighboring scene as a shot, a line or a prop (a plant becomes an insert; a first appearance becomes an entrance in another scene).
4. If it passes none, then cut it, and if it carries information the plot needs, move that information into another scene and log the move.

Record the score and the rule used in the adaptation log, so a reviewer can see why each passage became what it did.

---
## 8. Translation table: story meaning to screen choices and breakdown fields

| Story meaning in the source | Where to find it | Screen choice | Breakdown field |
|---|---|---|---|
| A character discovers something the plot depends on | Action lines naming an object after a look or a search | Insert sized to its importance, then the face that read it | Key shot; hero prop; reaction shot with its "cut against" |
| A character hides something | "out of sight", "she cannot see" | Floor plan places an occluder (a body, a box) between the hidden thing and the other character's eyeline; a later setup reveals it | Floor plan; eyelines; audience-knows note |
| A silent decision | "One breath.", "She nods. Once." | Hold on the face or hands; the next action shows the decision | Shot duration; physical task |
| An offscreen threat | `(O.S.)`, sounds in capitals | Sound first, reaction second, source shown late or never | Sound cue; reaction shot |
| The same place renamed | Scene-heading variants | One canonical set with dressing states | Set; set-dressing states |
| No time passes | `CONTINUOUS` | Match every state; motion can carry across the cut | Continuity: copy states forward |
| A small gap | `LATER`, `MOMENTS LATER` | A visible change carries the ellipsis (a cooled cup, a new bandage) | Continuity: allowed changes |
| Something seen on a screen | `(ON THE TABLET)`, "on the monitor" | Two layers: the inner picture (its own shot spec) and the outer frame | Screens-in-frame field |
| Recurring motif | A repeated object or line | Same framing each time it returns, so the audience compares | Plant/payoff registry |
| A plant that must not be noticed | A detail the source buries in a list | Give it legible screen time equal to its neighbors, no push-in | Plant registry with "do not emphasize" flag |
| A thought (prose) | Free indirect style, "she decided" | Externalization ladder (7.2) | Adaptation log: rung used |
| A habit (prose) | "every", "would", "in the evenings" | One dramatized instance or a varied montage | Adaptation log: iterative to singulative |
| Backstory (prose) | Summary of years | Object or document in the set; a line under pressure; or cut | Prop; insert; adaptation log |
| A letter or document | Italics, epistolary frame | Dramatize the event it reports; sparse voice-over; insert | Sound (V.O.); on-screen text; insert |
| A change in how the world looks to a character | A rule the story sets up | A per-scene frame-of-reference flag that art, makeup and graphics obey | States: story rule row |
| Power between characters | Who stands, sits, gives orders | Blocking: height, distance, who crosses to whom | Floor plan moves |

---

## 9. Decision rules

Each rule reads **If** … **then** (or **then consider**) … **because** …. A plain "then" rule is firm: follow it. A "then consider" rule is a default: follow it unless you write a one-line reason in the scene record's `notes`. When a firm rule and a default clash, the firm rule wins. (Library file A2 uses the same convention.)

**Analysis**

1. If you cannot state the scene's event in one sentence, then list the beats first (A2), find the first beat after which a value or a relationship is different, and write the event from that beat; if no beat changes anything, set `event: none` and flag the scene as a transition or for review, because the event is usually hidden in a reaction, not in a line.
2. If a performance note is an adjective of emotion ("angry", "sad"), then replace it with a playable action that passes the test in 3.2 or with a physical task, and move the adjective to a `notes` field if you want to keep it, because a result cannot be played or prompted reliably (Weston: "Result direction is inaccurate direction").
3. If a character's objective is granted mid-scene, then consider ending the scene within one or two beats of that moment and record `exit_point: beat N`, because the scene is over when the protagonist gets what they want (Mamet; McKee: granting the scene intention stops the scene).
4. If the audience needs to know something a character does not, then plan the shot that tells them, place it at least one beat before the moment it matters, and record it in `audience_knows_more`, because suspense needs the knowledge in advance (Hitchcock's bomb).
5. If a face must carry an unspoken thought, then record in the shot list the shot placed immediately before the face (`cut_against: <shot id>`) and give the face a physical task compatible with that reading, never a blank stare, because the preceding shot shapes the reading (Kuleshov) but the effect is modest.

**Breakdown and continuity**

6. If two scene headings may name the same place, then merge them into one canonical set only when there is evidence (a line saying so, matching objects, or movement that runs straight from one to the other), and record that evidence with its fact/inference label; if there is none, keep them apart and add an open question, because separate sets fork every reference image downstream and a wrong merge is just as costly.
7. If an element's state can change, then give it a row in the continuity bible now, because a state discovered late means regenerating earlier shots.
8. If a scene is `CONTINUOUS`, then copy every state, every character's position and every held object forward unchanged; only a line inside the scene may change one, because the audience reads it as the same moment.
9. If a later scene replays an earlier one on a screen, then put that camera position, and what it sees, into the earlier scene's floor plan as a named setup, because the replay is a shot of the earlier scene.
10. If the source gives left or right relative to a character, then convert it to frame-left or frame-right for each setup, because the two are opposite when the camera faces the character.
11. If on-screen text must be read, then specify its exact wording, letter case, orientation (normal or mirrored) and the surface it sits on, and set `method: composite` (added as a graphic after generation); use `method: generate` only when the text is too small to read at the planned shot size, because image and video models still render text unreliably.
12. If a story rule changes how things look (a mirror reversal, a colour shift), then add a per-scene flag and a list of which elements obey it, because every department must apply it the same way.
13. If an object is handled or seen closely, then list it as a prop, not set dressing, with a reference asset, because hero objects must match shot to shot.
14. If a feature's side matters to the story (which hand wears the ring, which side the scar is on, which palm is injured), then record the side in the character's look as fact, inference or open question, and state it in every prompt that shows it, because generators choose sides at random and mirror images freely.
15. If a `(V.O.)` cue has a parenthetical naming a device or a way of hearing (`(in her ear)`, `(over the radio)`, `(on the phone)`), then set `voice_source` to that device and treat the line as sound inside the scene's time; if there is no such parenthetical, then inherit the source of the same speaker's previous V.O. in the same sequence; only if there is none and the speaker is not in the scene, treat it as narration and flag it for review, because the two need different sound and picture.
16. If a continuous physical action must be seen from more than one angle, then consider one designed shot or a chain of shots that each start where the last ended, instead of master-plus-coverage (5.6), because matched angles of one action are the hardest thing to generate.

**Adaptation**

17. If a passage is interior (thought, memory, judgment), then consider the externalization ladder from behavior downward, stopping at the first rung that works, and record the rung in the adaptation log, because voice-over and text weaken the image when used first.
18. If a passage is iterative, then consider one dramatized instance, chosen in this order: the instance that contains a change or a plant; else the first; or a montage of three or four instances that each differ visibly (light, season, object state), because film shows one moment at a time.
19. If a summary sentence contains a place, a time, two people and a change, then consider treating it as a buried scene, because it can be dramatized.
20. If a letter reports an event, then consider staging the event with four to six lines of the letter over it (7.7), because the letter then earns its voice and the image carries the rest.
21. If a physical mark would identify an anonymous figure (a scar, a ring, a burn), then leave it off unless the source makes that identification, because costume and makeup make claims the text may be withholding.
22. If a plant is deliberately buried in the source, then keep it legible but unemphasized: the same shot size, duration and framing as its neighbors, no push-in, no music cue, no isolating light, and on screen long enough to read (about one second per three words, never under two seconds), because pushing in on it announces the ending.
23. If a scene, passage or image recurs in the source (a bookend or a refrain), then save the first occurrence's setups (camera position, lens, framing, light, blocking) as a named template and build every repeat from it, because the repeat must match to be recognized.
24. If you must invent a line, a location or an action to make an adaptation playable, then use the smallest invention that works and label it `invention` in the adaptation log with the source lines it serves, because every invention is a claim the source did not make.

---

## 10. Element-extraction checklist (building the asset lists)

Run on every scene. Each item gets: name (canonical), category, scenes, fact/inference/invention, first appearance line, states by scene, reference asset needed (yes/no), notes.

**How to run it without missing things.** Do two passes per scene. Pass 1 walks the scene line by line and, for every noun, asks: is this a person, a place, an object, a sound, a text, a light, a substance? Pass 2 walks this list top to bottom and asks of the scene: is there any item of this kind? An element found by only one pass is still listed. Then merge across scenes by canonical name, so each asset appears once with all its scenes.

1. **Speaking characters.** From cues (extension stripped) and first-appearance capitals. Merge aliases (`DR SAYE` = `SAYE`). Assign a cast number. Record the look the text gives (age, build, distinguishing marks: Eli's "beard she has never seen"), side-specific features (ring hand, scar side, a crooked "half-smile" and which corner lifts), handedness where the text shows it, and what the voice must be (age, accent, texture) for voice generation. List each numbered look (5.4).
2. **Non-speaking characters and creatures.** GUARD, NURSE, TECHNICIAN, THE FIGURE, the ANIMAL. Creatures get both a character entry and a visual effects (VFX) entry.
3. **Extras.** Silent featured people and background ("Police lights beyond frosted windows" implies police).
4. **Stunts and physical action.** Falls, fights, being thrown, weightlessness, carrying a person.
5. **Sets.** Canonical name, sub-areas, INT/EXT, time of day, weather, period or era (write `unstated` if the source does not fix it), practical light sources named in the text (torch, lamps, monitors), and the set's dressing states (the treatment floor at night, then by daylight with a boarded window).
6. **Set dressing.** Objects in the set nobody handles closely; note any that change state.
7. **Hero props and props.** Every handled or closely seen object, with its states. Separate out: weapons; consumables and breakables (bread rolls, sealed meals, the mint leaf, the smashed window), which need a state per shot; documents and paper props, whose text goes to item 15.
8. **Wardrobe.** Each character's costume per story day, with damage states.
9. **Makeup, hair, injuries.** Wounds and their progression, blood, dirt, beards, aging.
10. **Vehicles and animals.** Include vehicle details the story depends on (which side the wheel is on).
11. **Practical special effects.** Sparks, breaking glass, smoke, liquids.
12. **Visual effects.** Vanishing, floating, transformation, environments that cannot be built.
13. **Sound.** Diegetic sounds named in the text, off-screen voices, radio and recorded voices (with how they are heard), silences, sound plants and payoffs.
14. **Music.** Only if the source specifies it or a character plays it.
15. **On-screen text and graphics.** Exact wording, where it appears, orientation (normal or mirrored), and who reads it.
16. **Screens in frame.** For each monitor, tablet, visor or wrist display: what it shows, shot by shot.
17. **Special technique or equipment.** For live action: crane, wire rig, underwater housing. For AI: Blender previs, compositing, motion reference (video of a real movement used to guide a generated one), a black frame or other picture instruction written into the action (`BLACK.`).
18. **States and story rules.** Every changeable element and every story-specific rule, per scene.
19. **Time.** Story day, time of day, ellipses, and the carrier for any time jump.
20. **Plants and payoffs.** Each plant with its payoff scene and an emphasis flag.
21. **Open questions.** Anything a department must decide that the source does not settle.

---

## 11. Scene checklist (an LLM runs this against each scene record)

- [ ] The scene heading is parsed into INT/EXT, canonical set, time, and modifier.
- [ ] The event is one past-tense sentence.
- [ ] The driver is named; every character present has objective, obstacle and playable actions.
- [ ] No performance field contains an adjective of emotion.
- [ ] Mamet's three questions are answered.
- [ ] The key shot is named and exists in the shot list.
- [ ] Every insert the plot depends on is in the shot list, sized to its importance.
- [ ] Every important reaction names the shot it is cut against.
- [ ] Any audience-knows-more moment has a shot that delivers the knowledge in time.
- [ ] Every line of dialogue and every action beat appears in at least one shot (coverage map).
- [ ] The floor plan shows start positions, moves, camera setups, and the line of action.
- [ ] All left/right references are converted to frame-left/frame-right per setup.
- [ ] Every element is listed in the breakdown categories, including the four AI additions.
- [ ] States entering the scene match the previous scene's exit states (exactly, if `CONTINUOUS`).
- [ ] Every state change inside the scene is anchored to a source line or marked inference.
- [ ] On-screen text is specified word for word with orientation.
- [ ] Screens in frame have content specs.
- [ ] Plants in this scene are in the registry with their payoff and emphasis flag.
- [ ] Inventions are labelled and minimal.
- [ ] Open questions are listed rather than guessed.
- [ ] Eighths and story day are filled in.
- [ ] If this scene is replayed later, the replay camera is in this floor plan.
- [ ] Every `(V.O.)` line has a `voice_source` (narration, radio or phone, recording, thought).
- [ ] The scene has a `pov` (whose scene it is), and any shot outside that POV carries a reason.
- [ ] Every character present cites a look ID, and every side-specific feature in shot (ring hand, scar side, injured palm) is stated or listed as an open question.
- [ ] Every plant flagged "do not emphasize" has the same size and duration as its neighbors and is readable on screen.

---

## 12. Common mistakes and how to spot them

| Mistake | How to spot it | Fix |
|---|---|---|
| Parsing *The Catch* with a stock Fountain tool | Output has no scene headings, or the mid-film title card is missing | Detect the dialect first (4.3). |
| Counting `SAYE (RECORDED)` as a second character | Cast list longer than the story's people | Strip extensions before counting; log the extension in sound. |
| Treating all capitals as one thing | `STOP` (a button label) tagged as a sound; `GUNSHOT` tagged as a prop | Classify each capitalized token (4.3 step 5). |
| One set per heading | The same concrete passage generated three different ways | Normalize sets (4.4). |
| Emotions in the performance field | Words like "worried", "devastated", "tense" | Replace with playable actions and physical tasks. |
| States lost across `CONTINUOUS` | A sleeve whole in one scene, torn in the next, with no line causing it | Diff exit states against entry states. |
| Character-relative left used as frame-left | Lamp on the wrong side in the board | Convert per setup (rule 10). |
| Unlabelled inventions | The breakdown contains facts you cannot find in the source | Every item carries fact/inference/invention. |
| Over-emphasized plants | Push-ins and music stings on details the source buries | Emphasis flag in the plant registry (rule 22). |
| Voice-over used first | V.O. lines that describe what the picture shows | Climb the externalization ladder; keep V.O. only if it adds. |
| Iterative prose filmed as repeated identical scenes | Several scenes with the same action and no change | One instance or a varied montage. |
| Eighths used as screen time | Scene durations copied from page lengths | Estimate duration from beats and action separately. |
| Text left to the video model | Garbled signs and labels in generated shots | Specify text as graphics or composites. |
| A replay that cannot match | The playback shows a camera angle the original never had | Rule 9. |
| Radio voices treated as narration | `JUDE (V.O.)` given a narrator's sound and no earpiece in picture | Read the parenthetical under the cue (rule 15). |
| New scene records at secondary headings | Scene count higher than the heading count; `CLOSE ON` or `LATER` records with no heading | Split only at real scene headings (4.1, 4.3 step 2). |
| Sides left to the generator | The ring or scar changes hands between shots; the mirror story stops making sense | Record the side in the look and in every prompt (rule 14). |
| Coverage planned as if on a set | Five angles of one continuous action that do not match when cut | Designed shots or chained shots (5.6, rule 16). |

---
## 13. Worked examples

### Example 1. Director's pass on scene 1, the loading tunnel (*The Catch*)

**Facts.** "Two brake brackets, empty. Four bright bolt holes in each. Nothing between the brackets and the guide rail." "She puts a finger into one of the holes. Feels the thread. Still sharp." "She stays on her knees. One breath." **Inference:** "still sharp" means the brakes were removed recently and on purpose. **Question:** does anyone else ever learn who removed them? (The script does not say; do not invent an answer on screen.)

**Event:** Iona found the safety brakes gone and committed the three of them to the cage anyway, on one condition: stop it gently.

**Mamet's questions.** Who wants what: Iona wants a way to bring out a brother who cannot climb. If not: Eli stays strapped to a bed. Why now: Eli has sent her "a photograph of your wrist" (scene 4), and with a "Guard on each door" the cage is the only way up tonight.

**Beats and playable actions.**

| Line | Iona | Jude |
|---|---|---|
| "Goods only. No persons." / "They all say that." | to dismiss | to test (is she sure?) |
| Discovery under the floor frame | task only: torch under the frame, finger in the hole, one breath | task only: unwinds the wire, unaware |
| "The safety brakes are gone." | to warn | task: stops unwinding |
| "Stairs?" / "Guard on each door." / "Can he climb?" / "Not when I last saw him." | to shut down (each way out he offers) | to probe |
| "Ropes are sound. Take it gentle. Stop it hard and there's nothing under it to catch us." | to instruct | (listens; no line) |
| "I know how a lift works, Io." / "I know you know." | to soothe (without backing down) | to rebuff |
| "Get in when I call it. Hold it till we're in." | to command | task: hooks the tag back on the gate |

**Turning point:** the discovery beat, and it is silent. That makes the key shot an insert of the finger in the bolt hole, followed by Iona's face held for "One breath." By size equals importance, the empty bracket gets a full-frame insert; the whole climax hangs on "nothing under it to catch us". By Kuleshov, her held face is read through the insert before it, so the performance note is a physical task ("keeps her finger in the hole, breathes once, takes it out"), not "she is afraid".

**Floor plan note.** The text gives the vertical composition: "Above her, Jude unwinds the wire from the gate." Camera low at Iona's kneeling height, Jude standing above her in frame: the one who knows is lowest in the frame. **Plants logged:** "Stop it hard" pays off in scene 6 ("Iona hits STOP with her elbow. The cage STOPS DEAD."); the red tag pays off as "Its red tag whips against the upside-down gate." **Exit early:** end on her hands on the ladder, torch in her teeth.

### Example 2. Breakdown sheet and continuity slice for scene 6, the freight cage (*The Catch*)

**Header.** Scene 6. `INT. FREIGHT CAGE - CONTINUOUS`. Set: FACTORY: FREIGHT SHAFT (cage). Night 1. About 2 2/8 pages (estimate). Synopsis: The cage descends; a shot from above wounds Jude; Iona stops the cage at the maintenance opening; the cage falls; after a CLACK and an instant of black the cage is rising, and they push out sideways into the opening. (That Eli clipped and fired the puck is an inference here and a fact only from scene 13; the synopsis for scene 6 must not state it, or the breakdown gives away the reveal.)

| Category | Elements (fact unless marked) |
|---|---|
| Cast | IONA, ELI, JUDE |
| Extras / silent | Shooter above: "Someone KICKS the top gate open and FIRES down through the roof" (offscreen; a silhouette at most is an invention) |
| Stunts | Iona "thrown flat on the grid"; bodies floating during the fall; the sideways push through the opening; "Iona's knees hit concrete" |
| Props | Red tag on the gate; control box with STOP; FLASK with PUCK (hero); pistol (offscreen) |
| Wardrobe | Iona's blue shirt, sleeves whole (inference: the colour comes from "a strip of blue cloth", scene 21); Eli's coat, one shoe |
| Makeup | Jude's shoulder wound ("a hole through his shoulder"); Iona's chipped tooth (from scene 2); Iona's palm skinned ("Her palm drags across the bright steel") |
| Special effects | Sparks: "Another shot sparks off the grid beside her boot" |
| Visual effects | "Jude's blood lifts off the steel in round red beads and hangs in the air"; weightless bodies; the reversal after the CLACK; the cage falling away |
| Sound | Motor; gunshots; "METAL SHRIEK"; "A hard metal CLACK"; silence under the black frame ("BLACK. A dark with nothing in it. One instant."; the black frame itself is a picture instruction, logged under special technique); the far landing: "This time they hear it land" (payoff of scene 2's "Does not hear it land") |
| On-screen text | STOP label; the red tag (inference: its wording is what Jude reads aloud in scene 1, "Goods only. No persons."; Eli reads it again here, "Io. This says-") |
| Special technique | Blender previs of the shaft with the cage moving down, stopping, falling, then rising |
| Open questions | Does Iona still carry the torch? Where is the puck when it fires? (Answered later: scene 13, "a flat black puck is clipped to the grid"; scene 21, "burnt into the grid where it was clipped". Scene 6's floor plan must place it there.) |

**Continuity bible, rows that change here (exit states of scene 6):**

| Element | Entering 6 | Leaving 6 | Anchor |
|---|---|---|---|
| Jude | unhurt | shoulder wound, bleeding | "He sits down into Eli with a hole through his shoulder." |
| Iona's palm (which hand: open question) | whole | skinned | "Her palm drags across the bright steel." |
| Iona's shirt | whole | not stated; the sleeve is gone by scene 7 (inference) | Scene 7: "what is left of her shirt sleeve" |
| Flask and puck | puck clipped under flask | clip empty; puck on the cage grid | Scene 7: "The clip under it is empty."; scene 13 |
| Eli's shoes | one | one | Scene 4: "He leaves the other." |
| Story rule: frame of reference | normal | the three people and what they carry are reversed; the world now reads backwards to them | Scene 7: "Every letter is backwards." |

The last row drives Example 4.

### Example 3. A floor plan dictated by a later scene (*The Catch*, scenes 6 and 13)

Scene 6 hides an action from Iona: "Eli gets one arm round Jude's chest. His other hand goes underneath. Behind Jude's back. Out of sight." And: "He is looking straight at her. He has one hand she cannot see." Scene 13 reveals it on a recording from "a camera above the top gate, looking straight down the shaft": "And in the long second of the fall, Eli's hand comes out from behind Jude's back. / Empty. / On the floor of the cage, where his hand was, a flat black puck is clipped to the grid."

**Rule 9 applies.** The floor plan for scene 6 must satisfy two eyelines at once. The text puts all three in the shelter of the control box ("Iona hauls them both behind the control box"), with Iona within reach of the STOP button. From Iona's eye position, Jude's body must block Eli's hand; from directly overhead, looking down through the open roof grid, the hand and the patch of floor grid under it must be visible and not hidden by the control box. So the plan places Eli seated against the wall beside the box with Jude sitting back into him ("He sits down into Eli"), Jude's front toward Iona so his body stands between her eyeline and Eli's hand behind Jude's back, Eli's face above Jude's shoulder so he can look "straight at her", the hand's spot on the floor clear of the box when seen from above, and the security camera at the top of the shaft as a named setup (6-SEC) even though scene 6 itself never cuts to it. Scene 13's playback shots are then generated or rendered from 6-SEC, with every scene 6 state: the wound, the floating blood, the flask.

**Coverage map.** In scene 6 the line "He has one hand she cannot see" is covered by an Iona-side setup (hand hidden) and is not covered by any overhead shot, so the audience shares Iona's ignorance. In scene 13 the reveal line is covered by the playback on the monitor, and the reaction is covered by the next action: "Iona pauses the recording with the remote. Looks at her brother. Not at Jude." Then "You did that." / "Yes." Two setups carry that exchange: Iona's single, looking frame-left toward Eli, and Eli's single, looking frame-right; Jude stays in the edge of Iona's frame, deliberately not looked at.

### Example 4. A story rule as a continuity state (*The Catch*, scenes 7 to 30)

After the fall, the script writes the world from the turned characters' side: "Every letter is backwards."; "The wheel is on the other side."; "OSTREL, stitched on it in blue. Backwards."; and in Saye's kitchen: "Saye's wedding ring. On her right hand. / Iona looks down at her own ring, on her own left hand." Then: "That is your left." / "It's my right." At the end, after Iona has turned a second time and the men have not, the rule shows from the other side: Jude's "wedding ring. On his right hand"; "The two rings sit directly across from each other, like a ring and its reflection"; Eli's smile "on the wrong side of his face"; "The labels run opposite ways."

**Inference:** the camera shares Iona's frame of reference. From the CLACK in scene 6 until her own turn in scene 27, the unturned world is shown mirrored. After that turn it is shown normally and Eli, Jude and their things are mirrored; the first proof on screen is scene 28, where she reads `RECEIVING` twice.

**The breakdown adds a per-scene flag** `frame: normal | reversed` and a list of what obeys it: all world text; the car (wheel on the other side); Saye's ring hand; Jude's appendix scar ("Was your appendix on the left?"); the side of Eli's half-smile; meal labels ("The letters face the right way" on the turned meal in scene 12). **Two production methods**, recorded as a choice, not a fact: build the world mirrored (reversed signage printed, ring worn on the other hand), or shoot normally and flip the whole image, while physically mirroring whatever must read normally after the flip. For AI generation the first is safer: text is composited anyway (rule 11), and a ring or scar side can be named in the prompt. **Open question:** the visor display (`HULL CLEARANCE`, `UPWARD SPEED`) is equipment from the normal world, and the pressure suit's printing "reads backwards to her" in scene 18, but the script never says the visor reads backwards. Ask; do not guess.

### Example 5. Adapting chapter I of *The Long Places*, "The Lamps Are Old"

**What the chapter is.** An italic letter, "*To the one who keeps the lamps after me*", in which an unnamed keeper records teaching a child to light the lamps. Then close third-person prose following Nilay Arat, an archaeologist of forty-four, through June: arrival, the lamp keeper Melek, a village meeting, a miscount of rooms, evenings of paperwork, the team's arrival, and a night on the threshold. Most of it is summary and iterative telling; only a few passages are scenes. The letter is the first of a series: chapters I to XIII each open with one.

**Whole-book knowledge that changes chapter-I choices** (from reading the whole novel): the threshold paragraph ("At the mouth of Kırk Oda the air shaft breathed...") is a refrain, returning word for word in chapters VI, XI and XIV, and the novel closes with it and then the whole opening letter; item 51 in the survey list, "Hand print, right, red ochre", turns out to be Nilay's own hand ("*The print is mine*"); the brother in the permit file is Emre (named in chapter II), and the last dated letter reads "Emre Arat kept here, from the fourth of September 1999"; and the last chapter finds the letter's teaching scene in the wall's tally lines, which Nilay has been rendering for six years ("a keeper, teaching a child to tend a lamp"). So the letter scene and the threshold scene must be designed to repeat exactly (rule 23), and the hand print, the brother line and the tally wall are plants that must be legible but not emphasized (rule 22).

**Candidate scenes.**

| # | Scene heading | Source | Decision | What is externalized, and how |
|---|---|---|---|---|
| 1 | `INT. KIRK ODA - FIRST GALLERY - BEFORE DAWN (PERIOD UNSTATED)` (time is an inference from "*every morning there has ever been*"; the gallery is an invention) | The letter | Dramatize what the letter reports ("*I taught the child today*"), with 4 to 6 letter lines as voice-over (option 1 in 7.7) | Hands only, faces withheld, because the letter never names either person (the child is a girl: "*I told her*"). Letter rules become inserts: oil "*to the first knuckle of the thumb*", the wick "*pinched, never cut*", the flame "*cupped and low*". The letter's own progression is the scene's beats: "*At the third lamp her hands shook, and at the fourth they did not, and at the ninth she yawned*": nine lamps, the room lit one pool at a time. Last action: a hand cuts "*the day's mark, one line, low, beside all the other lines*" on a wall of thousands of such lines (the tally wall, planted here and seen again in Nilay's renderings). Last voice-over word, "*begin*", lands on the cut to scene 2. Record every setup for the bookend. |
| 2 | `EXT. ROAD'S END BY THE MULBERRIES - DAY (JUNE)` | Arrival paragraph | Short scene | "two bags, a tube of rolled plans"; her hand checks the inside pocket where the permit "went soft with her own heat" (invention: a gesture that plants the permit). Erciyes "with snow on it" in the establishing view. The 26 years away are not narrated; scene 3 carries them. |
| 3 | `INT. MOTHER'S HOUSE - DAY` | Mother; the Trust letter (a March backstory) | Short scene plus insert (composite; the rereading is an invention, since the letter arrived in March) | Behavior given by the text: a bed and a towel "within four minutes". The avoided subject is played as avoidance, not named. Unpacking, Nilay rereads the hand-copied letter: insert on "*in advance*" and "*A. Halden, Registrar*" in the sloping hand; a small smile; she sets it aside (the text: she "liked the letter's manners, and forgot it"). |
| 4 | `INT. KIRK ODA - GRANDMOTHERS' CUPBOARDS - EVENING` | "Why nine?" exchange | Dramatize with the source's own dialogue | Melek's hands repeat the letter's actions in the same insert framing as scene 1, so the cut, not a narrator, links her to the old rule. Tilt (the camera pivots upward) from flame to the soot ceiling: "the black had depth". Her hands are hero hands: "a burn gone silver across the back of the right one". Keep two lines that plant later chapters: "You shouted in the middle gallery when you were small. Once... Don't shout." and, at the fourth door, "When the rains come you sleep above this. Water pushes the old air up and the old air doesn't know you." The second repeats a rule from the letter, so Melek speaks it with no emphasis and the cut does the linking. |
| 5 | `INT. MELEK'S HOUSE - NIGHT` | Clock story | Keep as dialogue while she trims wicks (the source says "at her table"; that it is Melek's house is an inference); may merge into 4 if runtime is short | Plant: the clock "an hour behind" after nights below; keep her grandmother's saying, "*a clock is a donkey, you beat it and it walks*", which returns almost word for word in the Trust founder's 1924 notes that Nilay reads in chapter XIII ("*a clock is a donkey, she says; you beat it and it walks*"). Do not add a clock to her wall unless chosen and logged (it is her grandmother's clock). |
| 6 | `INT. CO-OP - UPSTAIRS ROOM - DAY (SECOND WEEK OF JUNE)` and `EXT. CO-OP STAIRS - CONTINUOUS` | Muhtar meeting | Buried scene (rule 19); reported speech to dialogue | Insert: forty consents "signed and stamped — dated in April". Scarf/no-scarf becomes a husband and wife contradicting each other. Keep the two lines as the source gives them to an unnamed villager at the back, "People here sign in April for what they decide in June," and "It saves June.", and the laugh, with Nilay laughing too. Her later realization ("only afterward, walking down, did she notice") becomes behavior on the stairs: she stops, looks back up at the upstairs window. A look carries unease, not the specific thought (no meeting ever explained the signatures); if the plot later needs that thought, give her one invented question to Selami Bey on the stairs, labelled invention. |
| 7 | `INT. KIRK ODA - MIDDLE GALLERY - EARLY MORNING` | The count | Dramatize | Smoke hanging "in shelves" in still air; the candle flame that "lay down at knee height and stood up again" (a key shot, practical effect or VFX, and a plant: in chapter II a flame that "lay down and would not stand" marks "the bad breath the rule was about", the rain rule of the letter and of Melek); she writes *ventilation*, pleased. Counting whispered: forty-one going in, forty coming out. Insert: the form with a crossed-out forty-one and forty above. Melek's line "Forty is the polite number..." is moved to Melek at the mouth as Nilay comes up (composite; logged). |
| 8 | `INT. MOTHER'S HOUSE - NIGHT (LATE JUNE)` | "In the evenings" survey entry; the permit file | Iterative to one evening; composite of two passages; location is an invention (the text does not say where she works) | Laptop screen (inference: the text says she was "typing"), items 47 to 53, typed at one steady pace: "Item fifty-one took her no longer than item fifty." Hold long enough to read all seven; no push-in on 51 (rule 22). Then the pre-filled file, filled "in the same sloping hand as the March letter" (the match is the visual plant: frame the handwriting large enough to compare with scene 3's insert), insert on "*Brother — missing, earthquake, September 1999 — province.*" The simile "as you press a bruise" becomes a literal action: her thumb pressed on the line, then the folder closed. |
| 9 | `EXT. VILLAGE LANE - DAY (END OF JUNE)` | Team arrival | Scene of introductions | Each newcomer is one prop and one behavior from the text: Kállai's crates "with their Swedish customs stickers" and the padded case he carries himself, "scolding the tractor"; Vogel's steel boxes stencilled with a Zürich university and a handshake "like a thesis defense"; Yusuf, nineteen, with his phone tripod. Composite: Nilay's field rule ("*doors are vertical... never tell me a room is under anything*"), which the text calls a habit she beats into every student, is spoken to Yusuf. It echoes the letter's "*Doors go down and rooms go along*". |
| 10 | `INT./EXT. KIRK ODA - MOUTH (FIRST DOOR) - NIGHT (LAST NIGHT OF JUNE)` | The breathing shaft; the warmth | Dramatize; bookend setups recorded | The eighteen-minute breath becomes visible and audible (inventions, logged: the text gives the breath and its timing but not these carriers): the borrowed lamp's flame leans out, stands still, leans in, with a low air sound; an insert of her watch, and a dissolve for the elapsed cycle (ellipsis). The warmth: "She did not turn her head." Frontal locked-off medium shot with empty space at her right shoulder inside the frame, composed like a two-shot with one person missing; her shoulder settles a fraction as if taking weight (the text: "with weight"; "you go still, and go careful"); she closes her eyes (invention). Show no figure, no shadow, no child: the text shows none. Continuity: the lamp is on her left, the warmth on her right; in the frontal setup that puts the lamp frame-right and the empty space frame-left. The closing interpretation ("It was homesickness, she decided") is cut; the climb out, with one look back down into the dark (invention: the behavior that replaces the interpretation), ends the chapter. |

**Voice-over budget:** one scene (1) only. Everything else is carried by behavior, objects, inserts and juxtaposition.

**Cut or deferred, and logged:** the Göbekli Tepe argument (deferred until a colleague can challenge it in dialogue); the twenty-six years of absence as narration; the judgments "Old money liked a letterhead" and "the least mysterious practice in the province"; the remark on the 1924 surveyor as "a lister, not a describer".

**Rule 21 in action.** Scene 1's keeper must not have Melek's silver burn. Chapter I never says who the keeper is, and the novel's ending, in which the hand print proves to be Nilay's own and she writes a dated letter "before she lived it", keeps the question open; a scar would close it for the book. The child's hands get the same treatment: the book leaves open who the child is, so no ring, scar or mark. Log it: `keeper_hands: aged (inference from "*as long as my knuckles hold out*"), no identifying marks (deliberate)`; `child_hands: no identifying marks (deliberate)`.

**Open questions for the user:** Should the letter's voice be one voice across the whole film, or a new voice each time it returns? Where does Nilay stay and work (scene 8 assumes her mother's house)? Should the clock appear on screen? Should the letter return at the head of each later chapter's material, or only open and close the film (7.7)?

---
## 14. Confidence notes

- The Hitchcock size rule is quoted everywhere as a paraphrase; I could not confirm its exact wording in *Hitchcock/Truffaut*.
- Mamet's book quotations are taken as reproduced in a published review (zigzorg.com, below, which gives pp. 10, 60 and 63), not checked against a printed copy. The *Unit* memo wording and date (19 October 2005) are from the isegoria.net transcription.
- Weston's quotations were checked against the text of her *MovieMaker* article on 2026-09-27. The facts-and-questions method and the list of actor's tools are attributed to *Directing Actors* from general knowledge of the book, not from a checked page.
- Uta Hagen: the attribution of the questions to *Respect for Acting* (six steps, 1973) and *A Challenge for the Actor* (nine questions, 1991) is from knowledge of the books; the web search budget was exhausted before it could be rechecked online.
- An earlier draft said Chatman used *Une partie de campagne* to show Renoir keeping the camera out of the watching men's eyes. That specific claim could not be verified against the essay and was removed; only the fact that the essay compares Maupassant's story with Renoir's film is kept.
- An earlier draft said Benedetti accused Hapgood of blurring task and action; that could not be verified and was removed.
- Kazan's "Directing finally consists of turning Psychology into Behavior" was confirmed through a publisher page for *Kazan on Directing*; the character spines are described, not quoted.
- Breakdown colors and stripboard colors are conventions, not a standard every production follows.
- The skipping of I and O in shot letters is a common practice I could not tie to a single authority.
- Eighths for *The Catch* are estimates from a line-count model, not from a formatted PDF.
- The mirror-reversal reading of *The Catch* (Example 4) is an inference from the script's wording, labelled as such.

---

## Sources

**Books and articles**

- Arijon, Daniel. *Grammar of the Film Language*. Focal Press, 1976.
- Barratt, Daniel, Anna Cabak Rédei, Åse Innes-Ker and Joost van de Weijer. "Does the Kuleshov Effect Really Exist? Revisiting a Classic Film Experiment on Facial Expressions and Emotional Contexts." *Perception* 45(8), 2016, pp. 847–874. https://journals.sagepub.com/doi/10.1177/0301006616638595 (checked 2026-09-27).
- Bluestone, George. *Novels into Film*. Johns Hopkins Press, 1957.
- Chatman, Seymour. "What Novels Can Do That Films Can't (and Vice Versa)." *Critical Inquiry* 7(1), Autumn 1980, pp. 121–140. https://www.journals.uchicago.edu/doi/10.1086/448091 (checked 2026-09-27).
- Cleve, Bastian. *Film Production Management*. Focal Press (2012 edition, p. 25, cited via Wikipedia for the breakdown color code).
- Clurman, Harold. *On Directing*. Macmillan, 1972.
- Cole, Toby, and Helen Krich Chinoy, eds. *Directors on Directing*. Revised edition, Bobbs-Merrill, 1963 (contains Elia Kazan, "Notebook for *A Streetcar Named Desire*").
- Cybulski, Mary. *Beyond Continuity: Script Supervision for the Modern Filmmaker*. Focal Press, 2013.
- Genette, Gérard. *Narrative Discourse: An Essay in Method*. Trans. Jane E. Lewin. Cornell University Press, 1980 (French original 1972).
- Hagen, Uta. *Respect for Acting*. Macmillan, 1973; *A Challenge for the Actor*. Scribner, 1991.
- Kazan, Elia. *Kazan on Directing*. Ed. Robert Cornfield. Knopf, 2009. Publisher page: https://penguinrandomhousehighereducation.com/book/?isbn=9780307277046 (checked 2026-09-27).
- Katz, Steven D. *Film Directing Shot by Shot: Visualizing from Concept to Screen*. Michael Wiese Productions, 1991.
- Kozloff, Sarah. *Invisible Storytellers: Voice-Over Narration in American Fiction Film*. University of California Press, 1988.
- Mamet, David. *On Directing Film*. Viking, 1991. Quotations as reproduced at https://zigzorg.com/?p=1028 (checked 2026-09-27).
- Mamet, David. Memo to the writers of *The Unit*, dated 19 October 2005. Text at https://www.isegoria.net/2013/08/david-mamets-master-class-memo-to-the-writers-of-the-unit/ (checked 2026-09-27).
- McCarthy, Cormac. *No Country for Old Men*. Knopf, 2005.
- McFarlane, Brian. *Novel to Film: An Introduction to the Theory of Adaptation*. Clarendon Press, 1996.
- McKee, Robert. *Dialogue: The Art of Verbal Action for Page, Stage, and Screen*. Grand Central Publishing, 2016 (the scene-intention sentence in 3.1 is quoted from the book's text; other McKee material comes via library files A1 and A2).
- Miller, Pat P. *Script Supervising and Film Continuity*. 3rd ed. Focal Press, 1999.
- Murch, Walter. *In the Blink of an Eye*. Silman-James Press, 1995; 2nd ed. 2001.
- Prince, Stephen, and Wayne E. Hensley. "The Kuleshov Effect: Recreating the Classic Experiment." *Cinema Journal* 31(2), 1992.
- Rowlands, Avril. *The Continuity Supervisor*. 4th ed. Focal Press, 2000.
- Seger, Linda. *The Art of Adaptation: Turning Fact and Fiction into Film*. Henry Holt, 1992.
- Stanislavski, Konstantin. *An Actor Prepares*. Trans. Elizabeth Reynolds Hapgood. Theatre Arts Books, 1936.
- Stanislavski, Konstantin. *An Actor's Work: A Student's Diary*. Trans. and ed. Jean Benedetti. Routledge, 2008.
- Truffaut, François, with Helen G. Scott. *Hitchcock*. Simon & Schuster, 1967; revised edition 1984.
- Weston, Judith. *Directing Actors: Creating Memorable Performances for Film and Television*. Michael Wiese Productions, 1996; *The Film Director's Intuition: Script Analysis and Rehearsal Techniques*. Michael Wiese Productions, 2003.
- Weston, Judith. "Directing the Actor" (reprinted from *MovieMaker*). https://actioncutprint.com/files/DirectingActor-JudithWeston.pdf (checked 2026-09-27; source of the Weston quotations in this file).

**Web references (all checked 2026-09-27)**

- Fountain syntax: https://fountain.io/syntax
- Script breakdown and color code: https://en.wikipedia.org/wiki/Script_breakdown
- Stanislavski terminology and translations: https://en.wikipedia.org/wiki/Stanislavski%27s_system
- Kuleshov effect history and replications: https://en.wikipedia.org/wiki/Kuleshov_effect
- Eighths and setups per day (Jon C. Scheide, *MovieMaker*): https://www.moviemaker.com/whats-in-an-eighth-assistant-director/
- Lining a script: https://www.studiobinder.com/blog/how-to-line-a-film-script/
- Stripboard colors: https://storiara.com/blog/stripboard-colors-explained
- Hitchcock's rule as usually paraphrased: https://www.filmmakersacademy.com/glossary/hitchcocks-rule/

**Films cited**

*Young and Innocent* (Alfred Hitchcock, 1937); *Notorious* (Alfred Hitchcock, 1946); *Letter from an Unknown Woman* (Max Ophüls, 1948); *Une partie de campagne* (Jean Renoir, shot 1936, released 1946); *Jaws* (Steven Spielberg, 1975); *The Shining* (Stanley Kubrick, 1980); *No Country for Old Men* (Joel and Ethan Coen, 2007). Stage: *A Streetcar Named Desire* (Tennessee Williams, directed by Elia Kazan, 1947).

**Test sources**

- *The Catch*, original short screenplay, workshop revision 25 September 2026: `/root/.claude/uploads/fbbb0203-69e3-5f8e-b675-32d722ec580d/1edae70d-35_The_Catch_-_workshop_revision_of_Final4.txt`
- *The Long Places*, prose novella: `/root/.claude/uploads/fbbb0203-69e3-5f8e-b675-32d722ec580d/5dcd8176-19_The_Long_Places_-_revised_by_Claude_final.md`
