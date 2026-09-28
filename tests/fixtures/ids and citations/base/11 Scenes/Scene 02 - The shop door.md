# Scene 02 - The shop door

The key turns the wrong way, and the door opens anyway.

Below this line: details for the AI and the checker. You never need to read them.

### SCENE SC02 The shop door
- location: LOC-SHOP-DOOR
- driver: CH-MARA

### BEAT SC02-B01 The wrong way
- lines: 21-28
- action: CH-MARA | tactic: trying
- status: draft
- locked: no

### SHOTLIST SC02-LIST The shot list
- item: SC02-SH010 | beats: SC02-B01 | role: must_keep | size: medium | frame: single | subject: CH-MARA | time: 6 | shows: the key turns the wrong way and the door opens
- item: SC02-SH990 | beats: SC02-B01 | role: normal | size: wide | frame: empty | subject: none | time: 1 | shows: black
- approved: yes
- status: approved
- locked: no

### SHOT SC02-SH010 The wrong way
- beats: SC02-B01
- lines: 21-26
- purpose: The key turns the wrong way and the door opens anyway.
- because: SC02-B01, PL-01, PR-KEY.S01
- role: must_keep
- kind: live
- size: medium
- subject: CH-MARA
- thing: PR-KEY.S01 | payoff: PL-01
- hear: SC02-D01 | speaker: on_screen
- status: draft
- locked: no

### SHOT SC02-SH990 Black
- beats: SC02-B01
- lines: 28
- purpose: The story cuts to black.
- because: SC02-B01, line:28
- role: normal
- kind: black
- size: wide
- subject: none
- status: draft
- locked: no

END OF FILE | Scene 02 - The shop door | 5 records
