# The Catch, scene 10: the whole-film records it uses

## What this file is

Scene 10 does not stand alone. Its shots name people, their clothes and wounds, the kitchen's floor plan, the film's camera rules, the one look of the room and the choices you made. This file gathers exactly those records, taken from the project files where they live: 00 Start here, 01 Choices, 04 Scene list, 05 Story plan, 06 World and style, 07 Characters and voices, 08 Places and things, 09 Continuity, 10 Film rules and 22 Rights and credits. Read it beside the scene file for scene 10.

## At a glance

- The film: a short of about 35 minutes, photographic and plain, in the wide 2.39 to 1 frame, set in an unnamed British city today. No music.
- The mirror world: from "Her eyes open." in scene 6 the world is reversed around Iona, Jude and Eli. In scene 10 that means Saye, her kitchen and everything in it are shown mirrored, and Iona, Jude, Eli and the flask are not.
- The four people: Iona, lean and strong, her right sleeve gone and her right palm skinned; Dr Saye, grey, upright and buttoned to the collar; Jude, big and loose, shot through the right shoulder; Eli, thin and bearded, one shoe on, the flask in his fist.
- The kitchen: 6 by 3.6 metres, a table in the middle with Jude on it, the counter and window along one side, the fridge in the far corner. One warm lamp is the only light.
- The camera: level, still, at Iona's eye height, on the normal lens; the long lens is saved for the mirrored two-shot here and the rings in scene 29.

## Where things stand

Records from other scenes (the climax, the rings at the glass in scene 29, the confession in scene 13) are named here because scene 10's records point to them. Their scenes are not part of this example, which covers scene 10 only.

Below this line: details for the AI and the checker. You never need to read them.

## From 00 Start here

### PROJECT CATCH The Catch
- title: The Catch
- source_file: The Catch - workshop revision.txt
- source_fingerprint: 3f3320594e4a11d730bfb2ae7ec938b80274a3dded2bcd719d637e4e3d36fbee
- source_kind: screenplay
- source_format: catch_dialect
- language: english
- depth: standard
- surface: claude_code
- code_execution: yes
- batch_size: 18
- training_off: confirmed
- rights: mine
- format: short
- runtime_target_s: as_written
- scope: SC10
- frame_shape: 2.39
- fps: 24
- genre: science_fiction_thriller
- tone_home: tense
- tone_range: tense, enigmatic, dread, grave, wonder, contemplative
- scene_id_digits: 2
- prompt_words: torch | use: flashlight
- schema_version: 1.0
- checker_last_run: never
- model_facts_date: none
- status: approved
- locked: yes

## From 01 Choices

### CHOICE CHOICE-001 Rights
- question: Is this story yours, or do you have permission to adapt it?
- why: Exports and packs for AI video depend on the rights.
- option: a | text: It's mine
- option: b | text: I have permission
- option: c | text: It is in the public domain
- option: d | text: It is not mine and I have no permission: private study only
- default: a | reason: most people who use this kit adapt their own work
- answer: a
- asked: yes
- checkpoint: none
- affects: PROJECT.rights, RT-001
- sets: PROJECT.rights | value: mine | when: a
- sets: PROJECT.rights | value: permission | when: b
- sets: PROJECT.rights | value: public_domain | when: c
- sets: PROJECT.rights | value: study_only | when: d
- sets: RT-001.subject | value: source | when: a
- sets: RT-001.clearance | value: the author's own work | when: a
- sets: RT-001.holder | value: the author | when: a
- based_on: D4 rights intake
- status: answered
- date: 2026-09-28
- locked: yes

### CHOICE CHOICE-002 Depth
- question: How deep should the breakdown go?
- why: Depth decides how many fields every shot carries and how long the work takes.
- option: a | text: standard
- option: b | text: quick
- option: c | text: detailed
- default: a | reason: standard gives full shots ready for pictures and video
- asked: no
- checkpoint: none
- affects: PROJECT.depth
- sets: PROJECT.depth | value: standard | when: a
- sets: PROJECT.depth | value: quick | when: b
- sets: PROJECT.depth | value: detailed | when: c
- based_on: blueprint section 4
- status: defaulted
- date: 2026-09-28
- locked: yes

### CHOICE CHOICE-003 Privacy setting
- question: Have you turned off the setting that lets the app learn from your chats?
- why: An unpublished story should not be used to train anyone's model.
- option: a | text: Yes, it is off
- option: b | text: Not yet
- default: b | reason: nobody can see your settings from here, so it counts as on until you say so
- answer: a
- asked: no
- checkpoint: none
- affects: PROJECT.training_off
- sets: PROJECT.training_off | value: confirmed | when: a
- sets: PROJECT.training_off | value: not_confirmed | when: b
- based_on: D1 privacy lines
- status: answered
- date: 2026-09-28
- locked: yes

### CHOICE CHOICE-004 Format
- question: Is this a short or a feature?
- why: The format sets budgets for scenes, shots and saved choices.
- option: a | text: a short, under 40 minutes
- option: b | text: a feature
- default: a | reason: the first estimate is about 35 minutes
- asked: no
- checkpoint: a
- affects: PROJECT.format
- sets: PROJECT.format | value: short | when: a
- sets: PROJECT.format | value: feature | when: b
- based_on: D13 first estimate
- status: defaulted
- date: 2026-09-28
- locked: yes

### CHOICE CHOICE-005 Length
- question: About 35 minutes as written (32 to 38; the page count suggests up to 44). Keep everything, or give me a target?
- why: A shorter target means a plan for what to trim, merge or cut.
- option: a | text: keep everything
- option: b | text: give a target
- default: a | reason: the story is already short and tight
- asked: yes
- checkpoint: a
- affects: PROJECT.runtime_target_s
- sets: PROJECT.runtime_target_s | value: as_written | when: a
- sets: PROJECT.runtime_target_s | value: open | when: b
- based_on: K25; D13
- status: defaulted
- date: 2026-09-28
- locked: yes

### CHOICE CHOICE-006 Scenes in this example
- question: This worked example covers one scene. Which scenes should the scene work cover?
- why: Checks, estimates and exports run only on the scenes in scope.
- option: a | text: scene 10 only
- option: b | text: all 30 scenes
- default: a | reason: this project is the kit's worked example
- answer: a
- asked: yes
- checkpoint: a
- affects: PROJECT.scope
- sets: PROJECT.scope | value: SC10 | when: a
- sets: PROJECT.scope | value: all | when: b
- based_on: blueprint section 14.2, the gold example
- status: answered
- date: 2026-09-28
- locked: yes

### CHOICE CHOICE-007 Style and frame shape
- question: Photographic, clinical and plain, in the wide 2.39 to 1 frame?
- why: The style and the frame shape shape every picture and every prompt.
- option: a | text: photographic, wide 2.39 to 1
- option: b | text: photographic, standard wide 16 to 9
- option: c | text: animated, wide 2.39 to 1
- default: a | reason: the story is grounded and clinical, and its people face each other across tables and glass
- asked: yes
- checkpoint: b
- affects: STYLE.medium, PROJECT.frame_shape
- sets: STYLE.medium | value: live_action | when: a
- sets: PROJECT.frame_shape | value: 2.39 | when: a
- sets: STYLE.medium | value: live_action | when: b
- sets: PROJECT.frame_shape | value: 16_9 | when: b
- sets: STYLE.medium | value: 3d_animation | when: c
- sets: PROJECT.frame_shape | value: 2.39 | when: c
- based_on: B1 aspect ratio; D5
- status: defaulted
- date: 2026-09-28
- locked: yes

### CHOICE CHOICE-008 Place and time
- question: The script never names a country. An unnamed British city, today, with cars on the left?
- why: Place sets the signs, accents, police lights and money.
- option: a | text: an unnamed British city, today, cars on the left
- option: b | text: a place you name
- option: c | text: a deliberately invented place
- default: a | reason: the story's own words, torch and night bus, sound British
- asked: yes
- checkpoint: b
- affects: WORLD.place, WORLD.period
- sets: WORLD.place | value: named:united_kingdom | when: a
- sets: WORLD.period | value: present day | when: a
- sets: WORLD.place | value: open | when: b
- sets: WORLD.place | value: invented | when: c
- based_on: K27; D17
- status: defaulted
- date: 2026-09-28
- locked: yes

### CHOICE CHOICE-009 Music
- question: Music in the finished film: none, a few cues, or a full score?
- why: No clip ever has music baked in; this is about the finished film.
- option: a | text: none
- option: b | text: a few cues
- option: c | text: a full score
- default: a | reason: the room sounds and the pump do music's job
- asked: yes
- checkpoint: b
- affects: SOUNDPLAN.music_policy
- sets: SOUNDPLAN.music_policy | value: none | when: a
- sets: SOUNDPLAN.music_policy | value: sparse | when: b
- sets: SOUNDPLAN.music_policy | value: scored | when: c
- based_on: K31; A4
- status: defaulted
- date: 2026-09-28
- locked: yes

### CHOICE CHOICE-010 The mirror world
- question: Normal until the cage's clack; mirrored from the moment her eyes open until Iona's own turn at the ship; after that only Eli and Jude are mirrored. Keep it as written?
- why: The mirror decides which way round every person, place and sign appears in every shot.
- option: a | text: as written
- option: b | text: tell me what to change
- default: a | reason: it follows the story's own lines
- asked: yes
- checkpoint: b
- affects: WR-MIRROR
- sets: CHOICE-010-A | when: a
- sets: WR-MIRROR | value: open | when: b
- locks: WR-MIRROR
- based_on: K03
- status: defaulted
- date: 2026-09-28
- locked: yes

### SETVALUE CHOICE-010-A
- target: WR-MIRROR
- era: a | from: 10 | to: 261 | frame: original
- era: b | from: 263 | to: 1563 | frame: original
- era: c | from: 1565 | to: 1852 | frame: reversed

### CHOICE CHOICE-011 Faces
- question: Every face is invented, never a real person's likeness. Keep it so?
- why: A real likeness needs that person's written consent.
- option: a | text: invented faces for everyone
- default: a | reason: no one has given consent, and the story needs none
- asked: no
- checkpoint: b
- affects: CH-IONA.likeness_basis, CH-SAYE.likeness_basis, CH-JUDE.likeness_basis, CH-ELI.likeness_basis
- sets: CH-IONA.likeness_basis | value: invented | when: a
- sets: CH-SAYE.likeness_basis | value: invented | when: a
- sets: CH-JUDE.likeness_basis | value: invented | when: a
- sets: CH-ELI.likeness_basis | value: invented | when: a
- based_on: D4 likeness and consent
- status: defaulted
- date: 2026-09-28
- locked: yes

### CHOICE CHOICE-012 How the voices are made
- question: Every voice is designed with a voice tool, never a copy of a real voice. Keep it so?
- why: A copied voice needs consent; a designed voice does not.
- option: a | text: designed voices
- default: a | reason: asked again when you make video
- asked: no
- checkpoint: b
- affects: VO-IONA.source, VO-SAYE.source, VO-JUDE.source, VO-ELI.source
- sets: VO-IONA.source | value: designed | when: a
- sets: VO-SAYE.source | value: designed | when: a
- sets: VO-JUDE.source | value: designed | when: a
- sets: VO-ELI.source | value: designed | when: a
- based_on: D3; decision 14
- status: defaulted
- date: 2026-09-28
- locked: yes

### CHOICE CHOICE-013 Voice rule for the film
- question: Designed voices only, no copies of anyone's voice?
- why: It sets what add-on work may do with voices.
- option: a | text: designed voices only
- option: b | text: designed voices plus a copy of my own voice
- default: a | reason: the safest rule; asked again when you make video
- asked: no
- checkpoint: c
- affects: SOUNDPLAN.voice_policy
- sets: SOUNDPLAN.voice_policy | value: designed_only | when: a
- sets: SOUNDPLAN.voice_policy | value: designed_plus_own_clone | when: b
- based_on: D3; K16
- status: defaulted
- date: 2026-09-28
- locked: yes

### CHOICE CHOICE-014 Iona's sleeve and palm
- question: The story never says which sleeve tore or which palm the sill skinned. Her own right for both?
- why: It fixes which side the damage shows on in every shot from scene 6.
- option: a | text: her own right
- option: b | text: her own left
- default: a | reason: she catches the sill with the arm that leads, and the ring stays clean on her left hand
- asked: no
- checkpoint: b
- affects: CH-IONA.S02
- sets: CHOICE-014-A | when: a
- sets: CHOICE-014-B | when: b
- based_on: K26; B5
- status: defaulted
- date: 2026-09-28
- locked: yes

### SETVALUE CHOICE-014-A
- target: CH-IONA.S02
- side: sleeve torn away | own: right | plot: no
- side: skinned palm | own: right | plot: yes

### SETVALUE CHOICE-014-B
- target: CH-IONA.S02
- side: sleeve torn away | own: left | plot: no
- side: skinned palm | own: left | plot: yes

### CHOICE CHOICE-015 Where everyone stands in the kitchen
- question: Where does the camera stand for the raised hands, and where is Eli?
- why: It sets the lens, who stands behind the women, and the first of the film's two mirrored frames.
- option: a | text: far back along the table's line on the long lens, Eli small in the middle behind the women, the bottle cap in the same frame
- option: b | text: Saye in the front of the frame, Eli behind her
- default: a | reason: tested in grey 3D, and it matches the rings shot in scene 29
- asked: no
- checkpoint: c
- affects: SC10-SU01.use, LX-01, RC-01
- sets: SC10-SU01.use | value: the far frame through the wild west wall, down the table's line: the reflection two-shot, then Eli's cap, then Iona standing in the line | when: a
- sets: SC10-SU01.use | value: Saye in the front of the frame with Eli behind her | when: b
- based_on: K22; B3 Ex1; A2 worked example A
- status: defaulted
- date: 2026-09-28
- locked: yes

### CHOICE CHOICE-016 The lamp set down
- question: Keep Iona setting the lamp back on the table before the raised hands?
- why: The story only says she holds the lamp; setting it down frees her right hand and lights both women alike.
- option: a | text: keep it
- option: b | text: cut it
- default: a | reason: without it she raises her hand holding a lamp, and the two women are lit differently
- asked: yes
- checkpoint: c
- affects: SC10-SH070.additions, SC10
- sets: SC10-SH070.additions | value: Iona sets the lamp back on the table between them | when: a
- sets: SC10-SH070.additions | value: none | when: b
- based_on: K22; B2 Ex2; B3 Ex1
- status: defaulted
- date: 2026-09-28
- locked: yes

## From 04 Scene list

### SCENE SC10 Saye's kitchen
- heading: INT. SAYE'S HOUSE - KITCHEN - BEFORE DAWN
- int_ext: int
- place_text: SAYE'S HOUSE - KITCHEN
- time_text: BEFORE DAWN
- lines: 397-489
- characters: CH-SAYE, CH-IONA, CH-JUDE, CH-ELI
- speaking: CH-SAYE | cues: 10
- speaking: CH-IONA | cues: 4
- speaking: CH-JUDE | cues: 1
- speaking: CH-ELI | cues: 1
- transition_in: cut
- transition_out: cut_to_black
- presentation: normal
- origin: story
- event: Saye proved to Iona with a mint leaf that the three of them had turned and the world had not, and kept them all in her kitchen for the hospital and the police.
- sequence: SQ03
- scene_intensity: 6
- whose_scene: CH-IONA
- story_day: N1
- rhythm_class: dialogue
- tone: tense
- tone_undercurrent: enigmatic
- tags: three_or_more, glass_and_reflection, handedness
- target_duration_s: 110
- status: approved
- locked: yes

## From 05 Story plan

### PLAN
- logline: A lift engineer breaks her brother out of a medical trial, is turned with him into a mirror of the world, and gets them home only after she gives up her own way back to stop a fire.
- theme_question: When you carry someone, do you carry them as goods, weighed and decided for, or as a person, asked and told?
- core_value: home | positive: home | negative: stranded
- core_opposition: goods against persons
- crisis: SC24 "She deletes the way home."
- climax: SC26..SC27
- act: act one | scenes: SC01..SC10 | turn: SC10 "Nobody leave this room." = SC10-B11
- act: act two | scenes: SC11..SC23 | turn: SC23 "They vanish together."
- act: act three | scenes: SC24..SC30 | turn: SC27 "The engine crosses."
- peak: story | scene: SC27 | reason: the core value turns for good at the climax
- peak: crisis_choice | scene: SC24 | reason: the decision that forces the climax
- peak: colour | scene: SC24 | reason: the fire is the one saturated peak, where she gives up her way home
- peak: contrast | scene: SC24 | reason: light and dark are already extreme in the shaft, so red against green at the fire is the contrast saved for this peak
- peak: tightest_size | scene: SC13 | reason: the confession's turn lands inside Iona; the climax is played wide and still, in counterpoint
- peak: longest_hold | scene: SC30 | reason: the last shot holds on the pump over black
- peak: loudest_sound | scene: SC30 | reason: the pump is the one sound to reach sound emphasis 3
- peak: motif_payoff | scene: SC25 | reason: the chest opens, the film's largest single payoff
- peak: camera_break | scene: SC26 | reason: the camera floats free by her choice for the first time
- peak: sound_rupture | scene: SC26 | reason: the ship's hum drops out
- pov_plan: default: CH-IONA | breaks: none planned; scene 15 is seen only on Iona's tablet, so her point of view holds
- genre: science_fiction_thriller
- tone_home: tense
- tone_range: tense, enigmatic, dread, grave, wonder, contemplative
- tone_mix_rule: jokes stay in Jude's mouth and never reach the camera; wonder is kept for the crossing and grave for the fire
- runtime_estimate: 2118
- scene_budget: 30
- shot_budget: 480
- status: approved
- locked: yes

### SEQUENCE SQ03 The wrong world
- title: the wrong world
- scenes: SC07..SC10
- story_job: shows the three of them that everything reads backwards, then proves the change is in them
- value_change: they believe the world has turned; Saye proves that they have
- act: act one
- scene_intensity: 5-6
- travel: left_to_right
- status: approved
- locked: yes

### PLANT PL-07 The rings
- what: the rings on opposite hands: Saye's on the hand that looks like her right, Iona's on her own left
- planted_at: SC10 "Saye's wedding ring. On her right hand." = SC10-B04
- paid_off_at: SC29 "like a ring and its reflection"
- plant_emphasis: 2
- plot_event: yes
- payoff_emphasis: 3
- rhyme: yes | framing: the symmetrical profile two-shot along the dividing plane, on the 85 from far back (RC-01)
- motif: MO-RINGS
- status: approved
- locked: yes

### PLANT PL-08 The mint
- what: the pot of mint on Saye's sill, the one living thing in her kitchen
- planted_at: SC10 "A pot of mint on the windowsill" = SC10-B02
- paid_off_at: SC10 "Her face changes." = SC10-B07
- plant_emphasis: 1
- plot_event: no
- payoff_emphasis: 2
- rhyme: no
- motif: MO-MINT
- status: approved
- locked: yes

### PLANT PL-09 Don't open the flask
- what: Eli's one line in the kitchen, forbidding Saye to open the flask; Iona throws it back at him in scene 13
- planted_at: SC10 "Don't open the flask." = SC10-B06
- paid_off_at: SC13 "Don't open the flask. You could say that."
- plant_emphasis: 2
- plot_event: yes
- payoff_emphasis: 2
- rhyme: no
- motif: MO-FLASK
- status: approved
- locked: yes

### FACT FT-01 Turned, not the world
- what: Iona, Jude and Eli were turned; the world was not
- element: MO-RINGS
- audience_knows_from: SC10 "each with the wrong hand in the air" = SC10-B04
- known_by: CH-ELI | from: SC09 "the way you look at a result you expected"
- known_by: CH-SAYE | from: SC10 "Listens there a long time." = SC10-B03
- known_by: CH-IONA | from: SC10 "Her face changes." = SC10-B07
- mode: dramatic_irony
- status: approved
- locked: yes

## From 06 World and style

### STYLE
- medium: live_action
- style_words: photographic; real, lived-in rooms; practical light from lamps, windows and screens; muted colour; deep shadows that stay readable; fine even grain; clean spherical lenses; a level, steady camera; plain working clothes
- texture: grain | as: fine and even, like a quiet film stock
- texture: halation | as: none, except a faint glow round bare lamps
- texture: lens_character | as: clean spherical lenses, no flares or streaks
- texture: softness | as: none; faces stay sharp
- texture: cadence | as: 24 frames a second with a normal shutter
- named_reference_policy: describe_qualities_only
- words_to_avoid: cinematic, epic, futuristic, moody, glowing
- provisional: yes
- status: approved
- locked: yes

### WORLD
- place: named:united_kingdom
- period: present day
- drives_on: left
- language: english
- accents: British English, from more than one region
- signage: British road, shop and building signs, all reading backwards to the three of them from scene 6
- emergency_lights: blue flashing lights only
- institutions: a medical company's factory, a public hospital, the police
- money: pounds
- evidence: 12 | quote: "Torchlight on wet brick."
- evidence: 370 | quote: "A night bus comes at them"
- evidence: 59 | quote: "I know how a lift works, Io."
- origin: inferred
- status: approved
- locked: yes

### RULE WR-MIRROR The turned world
- kind: mirror
- statement: From "Her eyes open." the world is reversed around Iona, Jude and Eli and everything that turned with them; from "The ship is gone. The stars are gone." Iona is turned back, and only Jude, Eli and their things stay reversed to her.
- governs: LOC-SAYE-KITCHEN, CH-SAYE, PR-MINT, PR-LAMP, PR-BOTTLE, PR-PHONE, PR-SCISSORS, PR-STETHOSCOPE, PR-CASE
- era: a | from: 10 | to: 261 | frame: original
- era: b | from: 263 | to: 1563 | frame: original
- era: c | from: 1565 | to: 1852 | frame: reversed
- exception: none
- status: approved
- locked: yes

### RULE WR-TITLES Title cards
- kind: titles
- statement: Title cards read normally in every era; they are drawn as text graphics and never flipped.
- governs: TX-TITLE-CATCH
- exception: none
- status: approved
- locked: yes

## From 07 Characters and voices

### CHARACTER CH-IONA Iona
- names: IONA
- tier: principal
- role: a lift engineer who breaks her brother out of a medical trial and carries everyone home
- life_want: to keep the people she is responsible for alive and together
- arc: start: tests and catches everything with her own hands, and demands to be told | end: gives up her own way home and carries a stranger out; can sit with Eli without an answer | turning_scene: SC24
- thesis: a body made by work, all verticals and straight lines, whose hands know things before she does
- evidence: 53 | quote: "Lays her hand flat on the ropes, the way a vet feels along a dog's ribs."
- evidence: 24 | quote: "the way she has come round a thousand cages"
- evidence: 87 | quote: "the way it has come up after her for fifteen years"
- fixed_description: Iona, a lean, strong woman in her late thirties, with a long face and a straight, strong jaw, dark brown hair in a low knot with loose strands at the temples, straight low dark eyebrows, deep-set grey-green eyes.
- height_m: 1.68
- build: lean and strong, strong forearms and shoulders, her weight low
- colour_identity: faded mid-blue against dark brick
- tempo: steady and counted
- speech: sentences: short orders and plain questions | contractions: yes | vocabulary: practical, a lift engineer's words
- lineup: height: average | mass: average | shape: long | value: mid | colour: blue | tempo: medium
- face: straight low dark brows; deep-set pale eyes; a low knot with loose strands
- movement: home | part: hands and forearms | direction: forward, pressing flat on whatever she is judging | speed: steady | still: head
- movement: stress | part: arms and shoulders | direction: one sudden blow outward, then nothing moves | speed: fast, then stopped | still: whole body afterwards
- movement: break | part: mouth | direction: opens with nothing in it | speed: slow | still: hands
- gesture: a flat hand laid on something to feel whether it will hold | line: 53
- status_play: default: high | flips: SC13 "Tell me that's what you'd have wanted."
- distance: default_m: 1 | closest_m: 0 | changes: SC07, SC11, SC29
- voice: VO-IONA
- likeness_basis: invented
- status: approved
- locked: yes

### CHARACTER CH-SAYE Dr Saye
- names: SAYE, DR SAYE
- tier: principal
- role: the doctor who inspects the company's trials, who has sent people across and waited for them
- life_want: to be sure that nothing she sends across is lost again
- arc: start: holds every answer and times its release | end: honest, and walking Nell to a room with a window | turning_scene: SC24
- thesis: grey, vertical and fully fastened, a person who has been dressed and waiting for years; the only living thing she keeps is a pot of mint
- evidence: 399 | quote: "fully dressed at four in the morning"
- evidence: 404 | quote: "A kitchen with nothing of anybody in it."
- evidence: 436 | quote: "Saye's wedding ring. On her right hand."
- fixed_description: Dr Saye, a slim, upright woman in her fifties, short neat grey hair, a long lined face, thin straight brows, level grey eyes, a light grey cardigan buttoned to the collar over a white blouse.
- height_m: 1.65
- build: slim and upright, spine straight, shoulders level
- colour_identity: light cool grey and white, with the mint's green as her one living accent
- tempo: fast hands, slow body
- speech: sentences: complete and measured | contractions: no | vocabulary: exact and medical
- lineup: height: average | mass: slight | shape: long | value: light | colour: grey | tempo: slow
- face: short neat grey hair; a long lined face; thin straight brows
- movement: home | part: hands | direction: direct, flat onto the body she treats | speed: quick | still: head
- movement: stress | part: whole body | direction: none; she stops and looks at nothing | speed: stopped | still: whole body
- movement: break | part: head and shoulders | direction: leans in toward a screen | speed: slow | still: hands
- gesture: a flat hand raised between two people, holding them apart | line: 1702
- status_play: default: high | flips: SC17 "Leans in until her face is almost on the screen."
- distance: default_m: 2 | closest_m: 0.5 | changes: SC10, SC28
- voice: VO-SAYE
- likeness_basis: invented
- status: approved
- locked: yes

### CHARACTER CH-JUDE Jude
- names: JUDE
- tier: principal
- role: Iona's husband and partner on the job; the warmth of the three, wounded early
- life_want: to keep things light for Iona
- arc: start: the easy helper | end: the one who catches her and then lets go on purpose | turning_scene: SC28
- thesis: big, loose and warm, a body at ease in itself, so that when he is shot the ease goes out of the film and his jokes from a table read as courage
- evidence: 16 | quote: "JUDE, forties, easy in the shoulders"
- evidence: 414 | quote: "They didn't let me watch."
- evidence: 1779 | quote: "His wedding ring. On his right hand."
- fixed_description: Jude, a tall, broad man in his mid-forties with broad, loose shoulders, a broad face with laugh lines at the eyes, warm brown eyes, short brown hair flecked with grey, and a few days' stubble.
- height_m: 1.85
- build: tall, heavy but soft-edged, shoulders low and loose
- colour_identity: olive and khaki, mid value
- tempo: unhurried
- speech: sentences: short, dry jokes | contractions: yes | vocabulary: plain
- lineup: height: tall | mass: heavy | shape: round | value: mid | colour: olive | tempo: slow
- face: a broad face with laugh lines; short hair flecked with grey; stubble
- movement: home | part: chest and shoulders | direction: a loose float, leaning on things | speed: unhurried | still: feet
- movement: stress | part: his right side | direction: guarded, the arm held in | speed: slow | still: right arm
- movement: break | part: face | direction: the joke stops; the eyes go wide | speed: slow | still: whole body
- gesture: an open hand that reaches to hold someone, then opens to let go | line: 1709
- status_play: default: low | flips: SC28 "Other shoulder, Io."
- distance: default_m: 0.5 | closest_m: 0 | changes: SC06, SC28, SC29
- voice: VO-JUDE
- likeness_basis: invented
- status: approved
- locked: yes

### CHARACTER CH-ELI Eli
- names: ELI
- tier: principal
- role: Iona's brother, a scientist held in the trial, who turned them without asking
- life_want: to have done the right thing without having to explain it
- arc: start: decides for everyone and hides it | end: shares a meal with Iona without an answer | turning_scene: SC13
- thesis: a thin, watchful reader whose hands are always doing something we cannot see; the only warmth on his face is a smile that lifts on one side
- evidence: 133 | quote: "ELI, thirties, thin, a beard she has never seen"
- evidence: 224 | quote: "Behind Jude's back. Out of sight."
- evidence: 440 | quote: "Twists it the other way."
- fixed_description: Eli, a thin man in his early thirties with hollow cheeks, an untrimmed dark beard, dark hair grown over his ears, straight low dark eyebrows and grey-green eyes, slightly stooped.
- height_m: 1.78
- build: thin, narrow shoulders, the upper back curved from bench work
- colour_identity: dark charcoal grey
- tempo: a pause before every answer
- speech: sentences: short, often one word | contractions: yes | vocabulary: exact, a scientist's
- lineup: height: tall | mass: slight | shape: triangle | value: dark | colour: charcoal | tempo: slow
- face: an untrimmed dark beard; hollow cheeks; dark hair over the ears
- movement: home | part: head and eyes | direction: toward any text first | speed: slow | still: hands
- movement: stress | part: hands | direction: wringing, or drawn behind his body | speed: tight | still: head
- movement: break | part: shoulders | direction: forward, toward her | speed: sudden | still: hands
- gesture: a hand closed round something and drawn behind his body | line: 224
- status_play: default: low | flips: SC13 "She can always outwait him."
- distance: default_m: 1.5 | closest_m: 0.5 | changes: SC06, SC23, SC29
- voice: VO-ELI
- likeness_basis: invented
- status: approved
- locked: yes

### VOICE VO-IONA Iona's voice
- character: CH-IONA
- voice_description: A woman in her late thirties, low-middle pitch, British English with a working accent, clear and quick; short sentences that end flat, the voice of someone used to giving orders over noise, and quieter, not louder, when it matters most.
- pitch: low_mid
- pace_wps: 2.5
- accent: British English
- path_sound: radio | treatment: a small speaker, narrow band, a little crackle
- path_sound: helmet_inside | treatment: close and dry, with her breath under it
- source: designed
- status: approved
- locked: yes

### VOICE VO-SAYE Saye's voice
- character: CH-SAYE
- voice_description: A woman in her fifties, low and even, precise consonants, every word finished and never a contraction; unhurried, level at the end of each sentence, with warmth held back until she spends it on one person near the end.
- pitch: low_mid
- pace_wps: 2.0
- accent: British English, educated
- path_sound: recording | treatment: a small wrist speaker, thin and narrow
- source: designed
- status: approved
- locked: yes

### VOICE VO-JUDE Jude's voice
- character: CH-JUDE
- voice_description: A man in his mid-forties, warm and a little rough, easy British English; dry jokes delivered flat and a laugh held under the words, growing slower and quieter once he is wounded but never losing the joke.
- pitch: low
- pace_wps: 2.5
- accent: British English
- path_sound: earpiece | treatment: a radio earpiece in her ear, thin and close
- source: designed
- status: approved
- locked: yes

### VOICE VO-ELI Eli's voice
- character: CH-ELI
- voice_description: A man in his early thirties, soft and precise British English, a short pause before every answer, few words and never a raised voice; flat and careful even when what he says costs him most.
- pitch: mid
- pace_wps: 2.3
- accent: British English
- path_sound: radio | treatment: a small speaker, narrow band
- source: designed
- status: approved
- locked: yes

## From 08 Places and things

### LOCATION LOC-SAYE-KITCHEN Saye's kitchen
- headings: INT. SAYE'S HOUSE - KITCHEN - BEFORE DAWN
- story_job: the first room of the turned world that is not an institution: bare, controlled, and the place where the proof is made
- loudness: loud
- room_sound: a small bare kitchen before dawn: the fridge's low hum, and nothing else
- anchor: the table with Jude on it
- exit: BACK_DOOR | leads_to: the back step and the garden path
- exit: HALL_DOOR | leads_to: the dark hall and the rest of the house
- dressing: nothing of anybody: no photographs, a bare fridge door, a clean counter; one pot of mint on the windowsill; Saye's medical case
- plan_orientation: reversed
- size: [6.0, 3.6, 2.5]
- origin_corner: south-west inside corner
- axes: +x east, +y north, +z up
- wild_walls: west wall
- object: TABLE | at: [2.8, 1.8] | size: [1.8, 0.9, 0.75] | base: 0 | material: pale scrubbed wood | meaning: the line the two women stand on either side of; Jude lies on it | furniture: bed
- object: COUNTER | at: [3.0, 0.3] | size: [3.0, 0.6, 0.9] | base: 0 | material: a steel top over white cupboards | meaning: where the flask and the phone wait | furniture: none
- object: WINDOW | at: [2.8, 0.05] | size: [1.4, 0.1, 1.0] | base: 1.0 | material: clear glass, a deep blue sky before dawn | meaning: the sill with the one living thing | furniture: none
- object: FRIDGE | at: [5.7, 2.9] | size: [0.6, 0.7, 1.8] | base: 0 | material: white, its door bare | meaning: nothing of anybody, even here | furniture: none
- object: BACK_DOOR | at: [0.05, 0.9] | size: [0.1, 0.9, 2.0] | base: 0 | material: painted wood | meaning: where the three of them arrive | furniture: none
- object: HALL_DOOR | at: [0.6, 3.55] | size: [0.9, 0.1, 2.0] | base: 0 | material: an open doorway onto the dark hall | meaning: the rest of the house, never seen | furniture: none
- object: MINT | at: [2.8, 0.1] | size: [0.15, 0.15, 0.2] | base: 1.0 | material: a clay pot of green mint | meaning: the one living thing in the room | furniture: none
- object: FLASK | at: [3.6, 0.35] | size: [0.09, 0.09, 0.25] | base: 0.9 | material: dented steel | meaning: Eli's secret, set down in Saye's house | furniture: none
- object: PHONE | at: [3.3, 0.35] | size: [0.08, 0.16, 0.01] | base: 0.9 | material: a black phone, screen down | meaning: the hospital and the police | furniture: none
- object: LAMP | at: [3.6, 1.8] | size: [0.15, 0.15, 0.35] | base: 0.75 | material: a small lamp with a warm shade | meaning: the only light; Iona lifts it and sets it back here | furniture: none
- object: CASE | at: [2.2, 0.35] | size: [0.45, 0.3, 0.15] | base: 0.9 | material: worn black leather | meaning: Saye's medical case, open | furniture: none
- mark: IONA_MARK | at: [2.8, 2.55]
- mark: SAYE_MARK | at: [2.8, 1.05]
- mark: ELI_MARK | at: [5.1, 2.0]
- mark: SAYE_DOOR | at: [0.25, 0.9]
- mark: SAYE_COUNTER | at: [3.3, 0.85]
- mark: SAYE_SILL | at: [2.8, 0.7]
- mark: IONA_BETWEEN | at: [4.15, 1.4]
- mark: IONA_ASIDE | at: [3.9, 1.95]
- note: The plan is written as the audience sees the kitchen in scene 10, where the world is reversed; code derives the other orientation.
- status: approved
- locked: yes

### PROP PR-FLASK The flask
- names: flask, the flask
- category: hero_prop
- fixed_description: a small dented steel vacuum flask with a black screw cap, the kind that keeps coffee hot, about 25 centimetres tall
- real_size: [0.09, 0.09, 0.25]
- side: none
- text: none
- first_seen: 162
- motif: MO-FLASK
- origin: story
- status: approved
- locked: yes

### PROP PR-LAMP The lamp
- names: the lamp
- category: prop
- fixed_description: a small table lamp with a warm fabric shade and a heavy round base
- real_size: [0.15, 0.15, 0.35]
- side: none
- text: none
- first_seen: 406
- motif: none
- origin: story
- status: approved
- locked: yes

### PROP PR-MINT The pot of mint
- names: mint, the pot of mint
- category: prop
- fixed_description: a small clay pot of green mint with soft, bright leaves
- real_size: [0.15, 0.15, 0.2]
- side: none
- text: none
- first_seen: 404
- motif: MO-MINT
- origin: story
- status: approved
- locked: yes

### PROP PR-BOTTLE The water bottle
- names: a water bottle
- category: consumable
- fixed_description: a clear plastic water bottle with a white screw cap and no label
- real_size: [0.07, 0.07, 0.22]
- side: cap thread | own: right | plot: yes
- text: none
- first_seen: 440
- motif: none
- origin: story
- status: approved
- locked: yes

### PROP PR-PHONE Saye's phone
- names: her phone
- category: prop
- fixed_description: a plain black mobile phone in a dark rubber case, about 15 centimetres long
- real_size: [0.075, 0.155, 0.01]
- side: none
- text: none
- first_seen: 468
- motif: none
- origin: story
- status: approved
- locked: yes

### PROP PR-SCISSORS Saye's scissors
- names: her scissors
- category: prop
- fixed_description: steel medical scissors with angled blades and black grips, about 14 centimetres long
- real_size: [0.07, 0.18, 0.01]
- side: none
- text: none
- first_seen: 447
- motif: none
- origin: story
- status: approved
- locked: yes

### PROP PR-STETHOSCOPE Saye's stethoscope
- names: her stethoscope
- category: prop
- fixed_description: a black stethoscope with rubber tubing and a round steel chest piece
- real_size: [0.3, 0.1, 0.7]
- side: none
- text: none
- first_seen: 416
- motif: none
- origin: story
- status: approved
- locked: yes

### PROP PR-CASE Saye's medical case
- names: Saye's medical case
- category: prop
- fixed_description: a worn black leather doctor's case with a brass clasp, about 40 centimetres long
- real_size: [0.45, 0.3, 0.25]
- side: none
- text: none
- first_seen: 406
- motif: none
- origin: story
- status: approved
- locked: yes

### TEXT TX-TITLE-CATCH The title card
- kind: title_card
- words: THE CATCH
- on: none
- origin: story
- reader: none
- plot_critical: no
- emphasis: 2
- method: composite
- animation: none
- status: approved
- locked: yes

### MOTIF MO-RINGS The rings
- meaning: the vow that holds across a division that cannot be touched; the reversal made personal
- rank: spine
- channel: visual
- appearance: SC10 "like a woman and her reflection" = SC10-B04 | role: plant | emphasis: 1
- appearance: SC10 "Saye's wedding ring. On her right hand." = SC10-B04 | role: teach | emphasis: 2
- appearance: SC29 "like a ring and its reflection" | role: payoff | emphasis: 3 | rhyme_with: SC10-SH080
- signature: none
- status: approved
- locked: yes

### MOTIF MO-MINT The mint
- meaning: the body's verdict, arriving before the mind will accept it; the one kept living thing in a life on hold
- rank: single_scene
- channel: visual
- appearance: SC10 "A pot of mint on the windowsill" = SC10-B02 | role: plant | emphasis: 1
- appearance: SC10 "tears a leaf from the pot of mint" = SC10-B07 | role: develop | emphasis: 2
- appearance: SC10 "Her face changes." = SC10-B07 | role: payoff | emphasis: 2
- signature: none
- status: approved
- locked: yes

### MOTIF MO-FLASK The flask
- meaning: Eli's work and his guilt, an ordinary coffee flask holding a danger; the decision about it passes from him to Iona
- rank: spine
- channel: visual
- appearance: SC04 "a small steel FLASK" | role: plant | emphasis: 1
- appearance: SC07 "The clip under it is empty." | role: develop | emphasis: 2
- appearance: SC09 "He looks down at the flask in his hand for a long time." | role: develop | emphasis: 2
- appearance: SC10 "for a long moment, at the flask" = SC10-B01 | role: develop | emphasis: 1
- appearance: SC10 "Don't open the flask." = SC10-B06 | role: develop | emphasis: 2
- appearance: SC13 "Saye puts it in a sealed carrier." | role: develop | emphasis: 1
- appearance: SC24 "She looks at the flask inside the outline." | role: payoff | emphasis: 3
- appearance: SC29 "Saye says the flask's gone." | role: coda | emphasis: 1
- signature: none
- status: approved
- locked: yes

## From 09 Continuity

### STATE CH-IONA.S02 Sleeve torn, palm skinned
- element: CH-IONA
- from: SC06 | line: 286
- cause: 286 | quote: "Her palm drags across the bright steel."
- state_line: a faded mid-blue work shirt with its right sleeve torn away at the shoulder, dark grey canvas trousers, scuffed brown boots; her right palm raw, dried blood on both hands; a plain gold ring on her left hand
- changes: the palm skinned on the sill as she catches it; the right sleeve torn on the same steel, later pressed into Jude's wound
- side: sleeve torn away | own: right | plot: no
- side: skinned palm | own: right | plot: yes
- side: wedding ring | own: left | plot: yes
- handedness: original
- origin: story
- note: The sides of the sleeve and the palm are the small choice CHOICE-014; the story says only what is left of her shirt sleeve.
- status: approved
- locked: yes

### STATE CH-SAYE.S01 Dressed at four in the morning
- element: CH-SAYE
- from: SC10 | line: 399
- cause: 399 | quote: "fully dressed at four in the morning"
- state_line: dark grey trousers and flat black shoes, a stethoscope round her neck, a plain gold ring on her left hand
- changes: first seen
- side: wedding ring | own: left | plot: yes
- handedness: reversed
- origin: inferred
- note: The story says the ring is on her right hand while the world is reversed, so her own side is the left (K03); code shows it on the hand that looks like her right.
- status: approved
- locked: yes

### STATE CH-JUDE.S02 Shot through the shoulder
- element: CH-JUDE
- from: SC06 | line: 222
- cause: 222 | quote: "He sits down into Eli with a hole through his shoulder."
- state_line: an olive canvas work jacket hanging open, a grey T-shirt soaked dark red at the right shoulder, a blue cloth pressed into the wound, a plain gold ring on his left hand
- changes: shot through the right shoulder in the falling cage
- side: shoulder wound | own: right | plot: no
- side: wedding ring | own: left | plot: yes
- handedness: original
- origin: inferred
- status: approved
- locked: yes

### STATE CH-JUDE.S03 Shirt cut away
- element: CH-JUDE
- from: SC10 | line: 408
- cause: 408 | quote: "Saye cuts Jude's shirt away, cleans the wound"
- state_line: bare chest, the shirt cut away, a cleaned wound on the right shoulder, an old white scar low on the right of his belly, a plain gold ring on his left hand
- changes: shirt and jacket cut away, the wound cleaned, the old scar seen
- side: shoulder wound | own: right | plot: no
- side: appendix scar | own: right | plot: yes
- side: wedding ring | own: left | plot: yes
- handedness: original
- origin: story
- status: approved
- locked: yes

### STATE CH-ELI.S03 The flask in his fist
- element: CH-ELI
- from: SC07 | line: 310
- cause: 310 | quote: "The flask is in his fist."
- state_line: a long charcoal wool coat over a creased pale shirt, dark trousers, one brown shoe on his right foot and a sock on the other, Jude's blood dried on his coat sleeve
- changes: carrying the flask since the cage; one shoe since the treatment floor
- side: one shoe | own: right | plot: no
- side: half-smile | own: left | plot: yes
- side: hair parting | own: left | plot: no
- handedness: original
- origin: inferred
- status: approved
- locked: yes

### STATE LOC-SAYE-KITCHEN.S01 Bare before dawn
- element: LOC-SAYE-KITCHEN
- from: SC10 | line: 399
- cause: 404 | quote: "A kitchen with nothing of anybody in it."
- state_line: a bare, clean kitchen with nothing on the walls or the fridge door
- changes: first seen, through the back door
- side: none
- handedness: reversed
- origin: story
- status: approved
- locked: yes

### STATE PR-FLASK.S03 The clip empty
- element: PR-FLASK
- from: SC07 | line: 312
- cause: 312 | quote: "The clip under it is empty."
- state_line: a bare spring clip under its base, closed on nothing
- changes: the puck is gone from the clip
- side: none
- handedness: original
- origin: story
- status: approved
- locked: yes

### STATE PR-MINT.S01 On the sill
- element: PR-MINT
- from: SC10 | line: 404
- cause: 404 | quote: "A pot of mint on the windowsill"
- state_line: full and green, on the windowsill
- changes: first seen
- side: none
- handedness: reversed
- origin: story
- status: approved
- locked: yes

### STATE PR-LAMP.S01 Lit
- element: PR-LAMP
- from: SC10 | line: 399
- cause: 406 | quote: "Iona holds the lamp."
- state_line: lit, its shade warm
- changes: first seen on the table behind Saye at the door
- side: none
- handedness: reversed
- origin: inferred
- status: approved
- locked: yes

### STATE PR-BOTTLE.S01 Full, cap on
- element: PR-BOTTLE
- from: SC10 | line: 404
- cause: 440 | quote: "Eli twists the cap of a water bottle."
- state_line: full, the cap on
- changes: first seen in Eli's hand in the kitchen
- side: cap thread | own: right | plot: yes
- handedness: reversed
- origin: inferred
- status: approved
- locked: yes

### STATE PR-PHONE.S01 On the counter
- element: PR-PHONE
- from: SC10 | line: 404
- cause: 468 | quote: "She picks up her phone."
- state_line: lying on the counter, screen dark until it is picked up
- changes: first seen
- side: none
- handedness: reversed
- origin: inferred
- status: approved
- locked: yes

### STATE PR-SCISSORS.S01 In her hand
- element: PR-SCISSORS
- from: SC10 | line: 404
- cause: 447 | quote: "Saye sets her scissors down."
- state_line: clean steel, in use
- changes: first seen in Saye's hand
- side: none
- handedness: reversed
- origin: inferred
- status: approved
- locked: yes

### STATE PR-STETHOSCOPE.S01 Round her neck
- element: PR-STETHOSCOPE
- from: SC10 | line: 399
- cause: 416 | quote: "She puts her stethoscope on his chest."
- state_line: hanging round her neck until she uses it
- changes: first seen
- side: none
- handedness: reversed
- origin: inferred
- status: approved
- locked: yes

### STATE PR-CASE.S01 Open
- element: PR-CASE
- from: SC10 | line: 404
- cause: 406 | quote: "Saye's medical case open."
- state_line: open, its instruments laid out
- changes: first seen
- side: none
- handedness: reversed
- origin: story
- status: approved
- locked: yes

## From 10 Film rules

### CAMSYS
- frame_shape_why: the film's pairs face each other across tables and glass, and a very wide frame puts them at its opposite edges; rows of glass rooms and a figure taller than a door need its width
- lens_type: spherical
- lens_family: 35, 50
- normal_lens_mm: 50
- step_change: from: SC13 | family: 35, 50, 85 | why: from the confession on, the singles move to the 85, closer but private
- default_height: Iona's eye height; when she kneels, the camera kneels
- default_move: static
- banned: dolly_zoom | why: it would read as a quotation of another film
- banned: dutch | why: the film's wrongness is handedness, and a tilted horizon would blur that one clear signal
- banned: slow_motion | why: playback is always real time; the fall is played in real time
- banned: orbit | why: nothing in this story is seen from a circling view
- camera_speed: real_time
- break: SC26 "She pushes gently away from the rail." | what: the camera floats free with her for the first time, by her choice | because: stillness has meant control and floating has meant helplessness; at the climax floating becomes her choice
- time_rule: expanded time is built from overlapping real-time slices of one master grey preview, never slow motion
- note: The 24 millimetre exceptions (the cage, the ship's wides, the figure in Iona's room) are lens exceptions outside this excerpt.
- status: approved
- locked: yes

### CAMRULE CR-IONA Iona
- character: CH-IONA
- in_control: static frames, or smooth moves at her pace, at her eye height; the camera inspects what her hands inspect
- losing_control: handheld, closer, on a wider lens, only on the broken rung, in the car and with the figure in her room
- never: dutch
- closest: extreme_close_up | at: SC13 "She can always outwait him."
- limit_before: close_up
- eyeline: just off the lens on the side of the person she answers, never into it
- because: CH-IONA, PLAN, RC-02
- status: approved
- locked: yes

### CAMRULE CR-SAYE Saye
- character: CH-SAYE
- in_control: centred or on a third, static, on the 50 from farther back than anyone else, often beside screens she controls
- losing_control: off-centre and closer, only in the recorded message where she has lost her answering voice
- never: low angle, push_in
- closest: close_up | at: SC24 "Saye has lost the voice she uses for answers."
- limit_before: medium_close_up
- eyeline: level, on the person she is testing, or for a long moment on the thing of risk
- because: CH-SAYE
- status: approved
- locked: yes

### CAMRULE CR-ELI Eli
- character: CH-ELI
- in_control: partial framings, profile or three-quarter, eyes well off the lens, one hand often out of frame or behind something, static
- losing_control: his closest and most frontal framing at the confession in scene 13, then his first look near the lens
- never: push_in
- closest: close_up | at: SC13 "Now he looks at her."
- limit_before: medium_close_up
- eyeline: his near-lens look is saved for scene 13
- because: CH-ELI, PLAN, RC-03
- status: approved
- locked: yes

### CAMRULE CR-JUDE Jude
- character: CH-JUDE
- in_control: warm medium two-shots with Iona
- losing_control: static, patient framing while he is wounded
- never: handheld
- closest: close_up | at: SC15 "Jude opens his eyes."
- limit_before: medium_close_up
- eyeline: on Iona
- because: CH-JUDE
- status: approved
- locked: yes

### RESERVE RC-01 The reflection two-shot
- choice: the perfectly symmetrical profile two-shot along the dividing plane, on the 85 from well back
- match: frame_detail = symmetrical_profile
- max_uses: 2
- allowed_in: SC10-SU01, the raised hands; and scene 29, the rings at the glass
- never_on: none
- because: MO-RINGS, PL-07, LX-01
- status: approved
- locked: yes

### RESERVE RC-02 The extreme close-up
- choice: the non-insert extreme close-up (a film-level saved choice)
- match: size = extreme_close_up
- max_uses: 3
- allowed_in: main turns only; the first in scene 13
- never_on: CH-ELI
- because: PLAN, CR-IONA
- status: approved
- locked: yes

### RESERVE RC-03 The push-in
- choice: the push-in (a film-level saved choice)
- match: move = push_in
- max_uses: share | fraction: 0.25
- allowed_in: main turns that happen inside a person; the first in scene 13
- never_on: CH-ELI
- because: PLAN, CR-ELI
- status: approved
- locked: yes

### LENS LX-01 The early 85
- mm: 85
- only_in: SC10-SU01
- why: the reflection two-shot needs the camera well back through the wild wall, on the same lens and distance as the rings shot in scene 29 that it rhymes with
- because: RC-01, PL-07
- status: approved
- locked: yes

### LOOK LK-SAYE-KITCHEN-NIGHT Saye's kitchen before dawn
- for: LOC-SAYE-KITCHEN
- time: before dawn
- look_block: A bare, tidy kitchen before dawn, lit only by one small warm lamp low on the table. A faint cool blue shows in the window over the counter. Pale walls, a white fridge, pale wood and steel; the corners fall into soft shadow while every face stays readable.
- main_light: the lamp | colour: warm, about 2,700 kelvin | quality: soft | from: LAMP
- neutral_white: balanced between the lamp and the window, so the lamp reads warm and the window blue
- contrast: medium_high
- fill: low
- stays_dark: the corners, the hall doorway and the ceiling
- palette: grey, off-white and pale wood, the lamp's amber, the window's blue
- accent_allowed: the mint's green, and only once it is in the lamplight
- light_cue: SC10 "Iona holds the lamp." = SC10-B02 | change: the lamp is in Iona's hand over Jude, so the light moves when she moves | why: the story puts the only light in her hand
- light_cue: SC10 "It's where it should be." = SC10-B03 | change: Iona sets the lamp back on the table between the women and the light steadies | why: the addition that frees her hands and lights both women alike
- light_cue: SC10 "She picks up her phone." = SC10-B09 | change: the phone's screen lights Saye's hand and chin | why: the story gives her the phone
- status: approved
- locked: yes

### VISUAL VS-SQ03 The wrong world
- sequence: SQ03
- frame_value: 2
- saturation: 2
- temperature: cool
- dominant: grey
- accent: green
- main_light: mixed
- contrast: high
- exit: cut to black and the title card
- sub_row: SC10 | frame_value: 3 | saturation: 2 | temperature: mixed | dominant: grey | accent: green | contrast: medium_high
- space: limited
- component: space | plan: hold | why: the passage, the street, the car and the kitchen are all seen squarely and kept flat, so the only contrast is the reversed world itself
- component: line | plan: hold | why: horizontals and frontal planes; in the kitchen the table is the mirror's centre line
- component: colour | plan: contrast | why: after the cool streets the kitchen brings the first warm light and the one green, the mint
- component: rhythm | plan: progress | why: the cutting quickens through the tests and stops dead on the mint
- counterpoint: none
- note: The other rows of this sequence, scenes 7 to 9, are outside this excerpt.
- status: approved
- locked: yes

### SOUNDPLAN
- music_policy: none
- clip_audio: No music in any clip.
- voice_policy: designed_only
- device_budget: cut_to_black | max: 2
- device_budget: true_silence | max: 2
- device_budget: freeze | max: 2
- rupture_plan: SC26 | device: drop_out, the ship's hum
- status: approved
- locked: yes

### LADDER
- rung: SC10 "Her face changes." = SC10-B07 | size: close_up | hold: long | why: the turn happens inside her mouth, so it lands close and is held; the film's tightest size waits for scene 13 and its longest hold for the last scene
- note: The other rungs of the ladder, one for each scene with a main turn, are outside this excerpt.
- status: approved
- locked: yes

## From 22 Rights and credits

### RIGHTS RT-001 The story
- subject: source
- clearance: the author's own work
- holder: the author
- status: approved
- locked: yes

END OF FILE | The Catch, scene 10 - the whole-film records it uses | 80 records
