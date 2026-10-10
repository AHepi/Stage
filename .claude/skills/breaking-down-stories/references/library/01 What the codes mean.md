# What the codes mean

**Example first.** C3 calls a shot "13-04"; that shot happens in the treatment-floor scene, which this pipeline calls SC11. B5 calls Iona's torn-sleeve costume "C2"; that is not the research file C2 but Iona's second state, which the pipeline writes `CH-IONA.S02`. This page turns every such label in the research into the pipeline's own name, so a card or a unit never copies an old number by mistake (K01, K26).

## The research files

| Code | Plain title (file in `library/`) | Code | Plain title |
|---|---|---|---|
| A1 | Dialogue as action and subtext | D1 | Running the pipeline in chat apps |
| A2 | Scene design, values and beats | D2 | Adapting a whole work |
| A3 | Script breakdown, directing and adaptation | D3 | Voices and dialogue audio |
| A4 | Editing, transitions, rhythm and sound | D4 | Rights, consent and disclosure |
| B1 | Camera, lens and movement | D5 | Choosing the visual style |
| B2 | Light and colour | D6 | Compositing and visual effects |
| B3 | Composition, visual structure and staging | D7 | Judging a breakdown |
| B4 | Symbols, motifs, sets, props and costume | D8 | Assembly, conform and colour grade |
| B5 | Character design for story | D9 | Music and sound effects |
| C1 | AI video models (September 2026) | D10 | Genre and tone |
| C2 | AI pictures, storyboards and consistency | D11 | Action and stunts |
| C3 | Writing prompts for video models | D12 | On-screen graphics and screens |
| C4 | Blender previs and camera control | D13 | Runtime, cost and schedule |
| C5 | Earlier systems, formats and pipeline practice | D14 | Reading any story format |
| | | D15 | Directing performance |
| | | D16 | Film-level structure |
| | | D17 | World and place research |
| | | D18 | Captions, audio description and translation |

Each file has a digest in `library/digests/` with the same name plus " - digest".

## How to read a citation

- **"B1 R14"** is rule 14 in the file's decision rules (B1 §11 here). Where a file numbers its rules without an R, the number is still written with R ("C5 R29" is rule 29 of C5 §5).
- **"§10.2"** is a section, **"Ex1"** a worked example, **"P5"** a principle from the file's first sections.
- **Digests number their rules again from 1** and give the full-file source in square brackets: B4 digest rule 17 is "[R23]", so it is B4 R23. Older notes that say "rule N" (for example "B4 rule 17" or "A3 rule 33") mean the digest's number; `library/02 Errata.md` lists the ones found. Always cite the full file.
- **Square brackets inside the research** are sources and evidence labels, not rules: [S12] and [P45] are numbered sources, [V] verified, [V-sec] verified at a secondary source, [U] unverified, [J] judgement.
- **Labels that belong to one file:**

| File | Labels |
|---|---|
| A1 | R1 to R44 (§6); principles P1 to P10; the checklist in §8 |
| A2 | rules 1 to 31 (§7); turning points TP1, TP2; beats B1 to B16 inside its worked scenes |
| A4 | rules grouped by letter in §9: C (continuity), R (cuts and rhythm), S (suspense), T (transitions), SND (sound), AI (production); "WE1" is Worked example 1 in §11 |
| B4 | motifs M01 to M17 (§9); emphasis L0 to L3 and sound levels S0 to S3 (§3.4) |
| B5 | "B5 M14" is item 14 of §13 (common mistakes), as the cards cite it |
| C1 | Recipe 1 to 11 (§8); Example 1 to 8 (§11) |
| C2 | R1 to R7 are recipes (§8), not rules; decision rules are cited "C2 §5, rule 9"; W1 to W5 are worked examples (§10) |
| C3 | L01 to L31 are linter items (§21); P1 to P55 are sources; Example 1 to 6 (§22) |
| C4 | Route 1 to 5 (§6); Example A to C (§12); previs levels 0 to 5 and 1b (§9) |
| C5 | E1 to E4 worked examples (§9); validator checks 1 to 13 (§6.6) |
| D6 | Rec1 to Rec9 recipes; VC1 to VC8 checks; W1 to W6 worked examples |
| D10 | TN, CM, HR, GW and SG rule families (SG1 to SG8 were once MU1 to MU8) |
| D11 | R1 to R28; WE1 to WE6 |
| D12 | Recipe 1 to 5; W1 to W7 |

## C3's shot numbers

C3 numbered its example shots on scene numbers that do not match the story's headings. Read them as:

| C3 shot | Scene | What it shows |
|---|---|---|
| 13-04 | SC11 | Treatment floor, morning: Iona and Saye through the glass (C3 Example 1) |
| 09-22, 09-15 | SC06 | The freight cage: zero gravity (Example 2) and the shot through the roof (Example 6) |
| 11-07A, 11-07B, 11-08 | SC07 | The maintenance passage: backwards text (Example 3) |
| 14-05A, 14-05B | SC15 | Jude's room on the tablet (Example 5; D10 uses the same numbers) |
| 18-31, 18-32, 18-33 | SC25 | The outer recess: the chest opens and the animal (Example 4) |

The part after the hyphen is C3's own shot count, not a shot ID. The pipeline issues shot IDs in tens from each scene's list.

## Other example IDs in the research

| Research label | Pipeline form |
|---|---|
| A1 §7: `scene_id: 07`, beat `7.4` | SC13 (the recording scene); its beats are `SC13-Bnn` |
| A2: `sc10.B7.b`, "B15" in sc13 | beat SC10-B07 and SC13-B15 (A2's beat numbers carry over); the letter is A2's shot option, which has no pipeline ID |
| A2 and B3: `sc10`, B4: `sc01` | SC10, SC01 |
| A3 §5.9: setup `6C`; A3 Ex3: `6-SEC` | scene 6, camera C (`SC06-SU03`, lettered in order); the security camera is a CAMERA record (`CAM-SHAFT-TOP`) |
| C1 Recipe 10: `S07_03`; C2 §6.6 and §5 rule 29: `SC014_SH03`, `SC012_SH03_start.png` | made-up names for a format; the pipeline writes `SC14-SH030` and a start-picture job `PIC-SC14-SH030-START-01` |
| C4 kit plans: `CATCH_SC06_SH14`, `_SH15`, `_SH16`, `_SH22` | SC06-SH140, SH150, SH160, SH220 (the kit's shot 14 is shot 140) |
| C4 kit plan: `CATCH_SC23_SH09_chest_opens` | the chest opens in SC25 (line 1448); the kit's scene number is wrong |
| C5 E3: `SC06-SH140`, label "6P" | kept; the crew letter label is worked out by code |
| D2 §7: `CF01` to `CF11`; D14 and D2: `ch01.p034`, `L0224` | cardinal events are CARDINAL records `CF-nn`; lines are cited by the numbered story's line numbers |

## Retired labels

| Retired label | Where | Now |
|---|---|---|
| looks `IONA-L1` to `IONA-L5` | A3 §5.4 | states: `CH-IONA.S01` and on, with boundaries from continuity (step 5) |
| costume phases C0 to C6 | B5 §10 | states, as above; beware, "C1" to "C5" there are not the research files |
| states S1 to S6 (and `CHR_IONA_S1_front.png`) | C2 §8 R2 and §6.1 | states, and reference pictures made per state |
| phases A, B, C; eras A, B, C | B1 §10.2; C2 §7.3, B4, B5 | eras a, b, c in `WR-MIRROR` (K03) |
| setups S1 to S8 | A2 §12 | setups `SC13-SU01` and on, shown as "camera A" |
| movements M1, M2 | A2 §11, §12 | parts `SC10-P1`, `SC10-P2` (an M ID is now a floor-plan move, `SC10-M04`) |
| TP1, TP2 | A2 | BEAT `turn` |
| emphasis L0 to L3; sound levels S0 to S3 | B4 §3.4 | `emphasis` 0 to 3; `sound_emphasis` 0 to 3 |
| motifs M01 to M17 | B4 §9 | MOTIF records named `MO-` and a word, chosen at step 4; the cards write M05 flask and puck `MO-FLASK`, M07 rings `MO-RINGS`, M08 mint leaf `MO-MINT`, M10 pump `MO-PUMP` |
| colour-script rows 1 to 23 ("sequence 18") | B2 §8.5 | `sub_row` items of VISUAL records; row 18 is the SC24 fire |
| nine stretches | B3 §2.7 | sequences SQ01 to SQ09 (K13) |
| "big close-up"; EWS, WS, MCU, CU, ECU | A2; B1 | `extreme_close_up` and the full size words |
| identity key, look line; look key; sound key | C3, C2, C5 | fixed description; look block; voice description and room sound |
| key shot | A2, A3, B1 | turn shot (`role: turn`) |
| `SFX-`, `AMB-`, `TH-`, SOUND record | D9 | proposals only; the schema has `effect` items, room sound and MUSIC (`MU-nn`) |
| checkpoint M; T; F, G, H | D2; D14; D8 | checkpoint P (the story plan, step 2); part of step 1; the stops inside add-on D |

The full list of retired words with their replacements is in `rules/words.json` and `reference/02 Word list.md`.
