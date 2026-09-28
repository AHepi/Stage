# Scene 01 - Mara's workshop

Oskar asks for the old key; Mara holds it up.

Below this line: details for the AI and the checker. You never need to read them.

### SCENE SC01 Mara's workshop
- location: LOC-WORKSHOP
- value: SC01-V1 | name: kept or lost, in whether the old key still opens the shop | core: yes | open: + | close: - | turns_at: SC01-B02 | kind: revelation
- driver: CH-OSKAR

### BEAT SC01-B01 The old key
- lines: 5-12
- action: CH-OSKAR | tactic: testing
- reaction: CH-MARA | tactic: deflecting
- charge: SC01-V1 | charge: +
- status: draft
- locked: no

### BEAT SC01-B02 The red thread
- lines: 14-17
- action: CH-MARA | tactic: revealing
- reaction: CH-OSKAR | tactic: demanding
- turn: main_turn
- charge: SC01-V1 | charge: -
- status: draft
- locked: no

### SHOTLIST SC01-LIST The shot list
- item: SC01-SH010 | beats: SC01-B01 | role: must_keep | size: wide | frame: group | subject: CH-MARA, CH-OSKAR | time: 4 | shows: Mara at her tin of keys; Oskar at the door
- item: SC01-SH020 | beats: SC01-B01 | role: normal | size: medium_close_up | frame: single | subject: CH-MARA | time: 3 | shows: she answers without looking up
- item: SC01-SH030 | beats: SC01-B02 | role: turn | size: close_up | frame: single | subject: CH-MARA | time: 5 | shows: the key held up by its red thread
- approved: yes
- status: approved
- locked: no

### SHOT SC01-SH010 Mara at her tin
- beats: SC01-B01
- lines: 5-8
- purpose: Mara at work, and the key Oskar asks about.
- because: SC01-B01, CH-MARA, line:5
- role: must_keep
- kind: live
- size: wide
- subject: CH-MARA
- hear: SC01-D01 | speaker: off_screen
- why: She works "under one bare bulb", so the wide frame holds the whole bench.
- status: draft
- locked: no

### SHOT SC01-SH020 Every key
- beats: SC01-B01
- lines: 10-12
- purpose: Her answer, without looking up.
- because: SC01-B01, CH-MARA
- role: normal
- kind: live
- size: medium_close_up
- subject: CH-MARA
- hear: SC01-D02 | speaker: on_screen | words: "I keep every key."
- status: draft
- locked: no

### SHOT SC01-SH030 The red thread
- beats: SC01-B02
- lines: 14-17
- purpose: The key Oskar wants, held up.
- because: SC01-B02, SC01-V1, MO-KEY, line: "small brass key with the red thread"
- role: turn
- kind: insert
- size: close_up
- subject: CH-MARA
- thing: PR-KEY.S01
- hear: SC01-D03 | speaker: off_screen
- why: The story ties "the red thread" through its bow, so the frame holds the thread.
- status: draft
- locked: no

END OF FILE | Scene 01 - Mara's workshop | 7 records
