### CHARACTER CH-MARA Mara Voss
- tier: principal
- fixed_description: A small woman of sixty in a grey wool coat, soot on both hands, short white hair.
- names: MARA
- note: first note
- status: approved
- locked: yes

### PROJECT LANTERN The Lantern
- frame_shape: 1.85
- status: approved
- locked: yes

### CHOICE CHOICE-009 Frame shape
- default: a | reason: the shed is narrow and tall
- answer: b
- sets: PROJECT.frame_shape | value: 1.85 | when: a
- sets: PROJECT.frame_shape | value: 2.39 | when: b
- status: answered

### BEAT SC03-B01 Not locked
- lines: 20-24
- locked: no

END OF FILE | Locked records | 4 records
