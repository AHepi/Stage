# Project records as they are stored

Below this line: details for the AI and the checker. You never need to read them.

### PROJECT LANTERN The Lantern
- title: The Lantern
- source_kind: screenplay
- depth: standard
- rights: mine
- training_off: confirmed
- frame_shape: 2.39
- code_execution: yes
- status: draft
- locked: no

### CHOICE CHOICE-001 Rights
- default: a | reason: most people adapt their own work
- answer: a
- sets: PROJECT.rights | value: mine | when: a
- sets: PROJECT.rights | value: study_only | when: b
- status: answered

### CHOICE CHOICE-002 Depth
- default: a | reason: standard is enough to make pictures and video from
- answer: b
- sets: PROJECT.depth | value: standard | when: a
- sets: PROJECT.depth | value: quick | when: b
- status: answered

### SCENE SC03
- heading: INT. SHED - NIGHT
- characters: CH-MARA, CH-OSKAR
- status: draft
- locked: no

### SHOT SC03-SH140 A typed label
- label: 3A
- size: wide

END OF FILE | Project records | 5 records
