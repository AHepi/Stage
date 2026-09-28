# Choices

## Waiting for you

Nothing is waiting: every choice for scene 10 is answered or taken by default.

## Small choices I made

- Iona sets the lamp back on the table before the raised hands.
- Her torn sleeve and skinned palm are on her own right side.
- The far camera down the table is the staging for the raised hands.

Below this line: details for the AI and the checker. You never need to read them.

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
- era: a | from: "INT. MEDICAL FACTORY - LOADING TUNNEL - NIGHT" | to: "A dark with nothing in it." | frame: original
- era: b | from: "Her eyes open." | to: "The whole outline clears the hull's last projection." | frame: original
- era: c | from: "The ship is gone." | to: "Three uneven strokes in the dark." | frame: reversed

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

---

Checked in words: 14 of 14 passed.

| Check | What it checks | Result |
|---|---|---|
| FORM-05 | every field needed at this depth is present | PASS |
| FORM-06 | the file ends with its END line | PASS |
| FORM-07 | the END line's count matches the records | PASS |
| FORM-08 | no shortening marker inside a record | PASS |
| FORM-12 | sub-parts are named, and no text holds a space, bar, space | PASS |
| ID-01 | no ID is used twice | PASS |
| ID-03 | shot numbers go in tens; cards and black from 990 | PASS (no beats or shots in this file) |
| ID-06 | every new ID is inside the numbers given for this step | PASS |
| ID-07 | every shot is in the scene's shot list | PASS (no beats or shots in this file) |
| ID-08 | each shot's beats, role and size match its list item | PASS (no beats or shots in this file) |
| COVER-01 | every story line of the scene is in a beat | PASS (no beats or shots in this file) |
| COVER-02 | every story line of the scene is in a shot | PASS (no beats or shots in this file) |
| COVER-03 | every speech is heard in a shot | PASS (no beats or shots in this file) |
| COVER-04 | every beat has a shot | PASS (no beats or shots in this file) |

END OF FILE | Choices | 19 records
