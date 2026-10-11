# Errata

**Example first.** B1's example prompt for the bolt-hole insert in SC01 says "torchlight from the left". Read it as "a flashlight beam entering low from frame-right": B2 Ex1 placed the main light, K19 chose B2's side, and every compiled prompt says "flashlight". The research files themselves are kept as they were written; this page lists the sentences in them that the pipeline no longer follows, and what to read instead.

**How to use this page.** Before acting on a library section, check this page for its code. Each entry starts with an "Applies to" line in the same form as a citation ("B1 §15", "B1 Ex1"); `stage.py lib` prints the entries whose "Applies to" line names the section or rule it prints. Where a correction comes from a resolved conflict, the K row in `references/library/00 Resolved conflicts.md` gives the full reasoning. Corrections that each research file already made to its own text during its fact-check are listed in that file's own fact-check note and need no action here (C3 §0; C1 §13; C5 §12; D1, D4, D11, D12, D13, D14 and D15 at the top of the file; D17 marks them "(corrected: ...)").

---

## Corrections the build plan names

### 1. The bolt-hole insert: light side and "torch" (K19)

- **Applies to**: B1 §15, B1 Ex1; C3 §22.0; C1 Recipe 1, C1 Recipe 10, C1 §11.
- **The research says**: B1 §15's example prompt for Example 1's insert reads "Extreme close-up, macro lens, torchlight from the left". C3 §22.0's look block for the cage says "a torch lying on the grid", and C1's test and batch prompts use "torch" and "torchlight" too.
- **Read instead**: the flashlight enters low from frame-right and rakes across the bracket (B2 Ex1's lighting spec). In any prompt the word is "flashlight"; "torch" stays only inside quotes of the script (B2 §0.1; `prompt_words`; check GEN-12).

### 2. C3's example descriptions (K26)

- **Applies to**: C3 §22.0, C3 Ex1, C3 Ex4.
- **The research says**: C3 §22.0 marks its descriptions as illustrative, and several differ from the story or from B5: the figure is "about two and a half metres tall, built like an armoured deep-sea diving suit"; Saye is "in her late fifties"; C3 Ex1 gives Iona "a grey blanket".
- **Read instead**: B5 §10 is the source of fixed descriptions, regenerated for each project at step 4: the figure is 2.4 metres (B5 §10.9, C2 and C4 agree), and B5 §7.5 names the diving-suit description as the regression to avoid (D5 §15); Saye is "fifties" (the story's word); the blanket is "OSTREL, stitched on it in blue" (the story), made dark navy (a design choice); rings and wounds go in state lines, never in fixed descriptions. Style words in C3's look blocks move to the film's style words (D5 §15).

### 3. The refrain in The Long Places is not word for word (D2 §8.2)

- **Applies to**: A3 Ex5.
- **The research says**: the threshold paragraph ("At the mouth of Kırk Oda the air shaft breathed...") "is a refrain, returning word for word in chapters VI, XI and XIV".
- **Read instead**: it is word for word except its figure: "eighteen minutes" in chapter I, then "nineteen", "twenty", and "eighteen" again (D2 §8.2, checked by script against the story). In chapter XI the same paragraph opens with a lead-in sentence, "She came up at full dark with the oil smell on her hands.", which belongs to the scene before the refrain. Build every return from one saved setup (A3 R23), show the changed figure with a watch or notebook insert, and change nothing else (D2 R15).

---

## Research sentences overruled by the resolved conflicts

### 4. Scene numbers in examples (K01)

- **Applies to**: C3 §22, C3 Ex1, C3 Ex2, C3 Ex3, C3 Ex4, C3 Ex5, C3 Ex6; C4 §12; A1 §7.
- **The research says**: C3's shot labels ("13-04", "09-22", "11-07A", "14-05A", "18-31") and C4's kit plan `CATCH_SC23_SH09_chest_opens` use scene numbers that do not match the story's headings; A1 §7 calls the recording scene "07".
- **Read instead**: the map in `references/library/01 What the codes mean.md`: "13-04" is SC11, the chest opens in SC25, A1's "07" is SC13.

### 5. "Build the world mirrored" (K02)

- **Applies to**: A3 Ex4.
- **The research says**: of two production methods for the mirror world, "For AI generation the first [build the world mirrored] is safer".
- **Read instead**: code works out a route per shot (text graphic, plate, direct, flip with mirrored references, flip all) from the element's mirror state; nothing is built mirrored for generation. B3's rule for deriving a mirrored plan stays for previs plans.

### 6. Where the eras begin and end, and the one-time light flip (K03)

- **Applies to**: B1 §10.2; C2 §7.3; A3 Ex4; B2 R21.
- **The research says**: C2 §7.3 starts era C at "RECEIVING ... Reads it again." in SC28, which leaves the lines from Iona's turn to SC28 in no era; B1 §10.2 starts phase C "from her second turn"; B2 R21 flips one lighting convention once and never back.
- **Read instead**: era b ends at line 1563 ("She fires."); era c starts at line 1565 ("The ship is gone. The stars are gone."), with Iona `reversed` from line 1563 and the frame `reversed` in era c. The main light is written in room terms and its frame side is worked out per era, so it flips with the picture at both boundaries; B2 R21's single flip is dropped.

### 7. The suit and visor text after Iona's last turn (K04; D12 §12; D6 §12)

- **Applies to**: B1 §16, B1 §10.6; C2 §7.3.
- **The research says**: B1 recommends that the visor text "snap readable" after her final turn; C2 §7.3's era C table leaves the suit out.
- **Read instead**: the suit turns with her, so its words stay backwards in era c ("It draws the turn round everything inside her outline. Herself. The suit.", line 1536); D12 §12 and D6 §12 follow this, and the first forward world word of era c is SC28's wall sign. K04 itself decides only era b (`WR-SCREEN-TEXT-B`); D6 §12 lists the era c choice as a question for the user, with D12's reading as the default.

### 8. SC13's tightest size and Eli's close shots (K05)

- **Applies to**: A2 §12; B1 Ex3; A1 Ex3; D16 §12; A2 §11.
- **The research says**: A2 §12 pushes in to a "big close-up" at beat 15 and pushes in on the recording at beat 7 ("B7 a"); B1 Ex3 gives Eli his closest, most frontal framing on "You."; D16 §12 item 2 recommends that SC13 stop at a close-up; A2 §11 gives Eli "his first close single of the scene" in SC10 on "Don't open the flask." (beat 6 b).
- **Read instead**: the main turn SC13-B15 gets the scene's one push-in, on Iona, landing at `extreme_close_up`, declared as a peak (K12); on "You." the cut lands on Iona; Eli's closest single is `close_up`, and `CR-ELI` keeps him at `medium_close_up` or wider before SC13, so in SC10 "Don't open the flask." plays with Eli off screen. The recording is never re-framed by the camera (B1 §10.4; D7 §14 item 2).

### 9. SC13 eyelines written in words (K06)

- **Applies to**: A1 Ex3, A1 R39; A2 §12; A3 Ex3.
- **The research says**: three different left-right arrangements of Iona, Jude and Eli.
- **Read instead**: every eyeline is worked out from B3's tested floor plan (B3 §8.6); where a card or file gives sides in words, the set plan wins (check GEOM-01).

### 10. Rings, reflection shots and image sides in state lines (K07)

- **Applies to**: B5 §10.2; A2 §11; C2 §8 R4.
- **The research says**: B5 §10.2 writes Jude's era c state line in picture terms ("plain gold ring on his right hand", "as the audience sees him"); C2's recipe says "State every left-right fact in image terms"; A2 §11 asks SC10's ring inserts to match the SC29 hands "in lens and angle".
- **Read instead**: state lines use own sides only ("ring on his own left hand"); "hand nearest the camera" goes in behaviour text; image sides are worked out by code per shot (check SIDE-02). The rhyme is carried by the two reflection two-shots under `RC-01`; the SC29 hands insert follows B3 §8.3.

### 11. Numbers retired by the constants (K08, K09, K10)

- **Applies to**: A1 §11, A1 R15, A1 R20; A3 R22; A4 R8; B1 R2; D15 §11.
- **The research says**: A1 §11 fits 16 to 24 spoken words in an 8-second clip; A1 R15 and D15 §11 item 12 start a long pause at 3 seconds; A1 R20, A3 R22, A4 R8 and B1 R2 give four different reading times.
- **Read instead**: `clip_speech_rule` with `speech_wps_default` and each voice's `pace_wps`; the tiers of `pause_tiers`, whose long tier starts where "Silence." starts; one reading floor, `text_floor`.

### 12. How loud a plant may be (K11)

- **Applies to**: A1 R20; A4 S5.
- **The research says**: a planted fact gets "one insert or one readable single".
- **Read instead**: a quiet plant (emphasis 0 or 1) matches its neighbours (A3 R22, B4 R6); an insert (emphasis 2) is allowed only for a plant that is itself a plot event (`plant_emphasis_max`, check CRAFT-08).

### 13. "The climax" in B2 and the peaks (K12; D16 §12)

- **Applies to**: B2 §4.4, B2 §8.5, B2 R9; D2 §7; D16 §12.
- **The research says**: B2 calls the SC24 fire "the climax" and "the film's visual climax"; D2's cardinal event list labels one row "The climax choice"; D16 §12 item 3 puts the film's longest shot in SQ08.
- **Read instead**: SC24 is the crisis; the climax is SC26 to SC27, played in counterpoint; B2's values stand as the crisis peak. The longest hold is SC30's last shot (the pump over black), as K12 sets it.

### 14. Readable text generated by the model (K17)

- **Applies to**: C3 R11, C3 Ex3.
- **The research says**: a sign of three words or fewer may be generated forwards and then flipped.
- **Read instead**: all readable text is composited from text graphics; models draw only background text nobody can read (check GEN-06). D6 §12 generates the lettering on soft surfaces such as the OSTREL blanket and fixes it on the still; K17 makes no such exception, so it holds here too.

### 15. Negation and speech syntax in prompts (K15, K18)

- **Applies to**: C2 §6.3; A1 §11; A4 §7.8.
- **The research says**: C2's location prompts end "No people, no text"; A1 §11 and A4 §7.8 put Veo speech in quotation marks.
- **Read instead**: exclusions go to a model's negative field or to the documented "No ..." lines only (check GEN-07); Veo and Omni speech is written in colon form without quotes (check GEN-09).

### 16. The fall's timing (K20; D11 §10)

- **Applies to**: A4 WE1; B1 §10.1; C4 §12.
- **The research says**: A4 Worked example 1 times the fall as about 12 seconds of subjective screen time; B1 plays it in real time; C4 keys one real fall of about 1.2 seconds.
- **Read instead**: expanded screen time built from overlapping real-time slices of one master previs (`PV-SC06-MASTER`), never slow motion; D11 §10 item 1 re-times A4's rows against the kit's frames.

### 17. The chest-opens plan (K21)

- **Applies to**: C4 §12.
- **The research says**: C4's kit plan pushes in slowly from 35 to 50 millimetres over Iona's shoulder; its file name says scene 23.
- **Read instead**: static 35 millimetres looking up, a motivated tilt down, the vessel by a macro insert, then a static 50 on Iona, no push-in (B1 Ex5; B4 R23); the scene is SC25.

### 18. The SC10 kitchen frame (gold example; K22)

- **Applies to**: B3 Ex1; A2 §11.
- **The research says**: the bottle-cap beat plays in camera A's frame "focus pulled from the women to Eli" (B3 Ex1; A2 §11 beat 5 a).
- **Read instead**: the focus pull is split into its own shot of Eli and the cap in camera A's deep frame (SC10-SH110), because pulled focus is unreliable in generated video (B1 R14).

### 19. Formats, sizes and page counts (K23, K24, K25)

- **Applies to**: B3 §6.4; C4 §5; C3 §22; A3 §5.2; C1 §10.
- **The research says**: B3's `plan_to_blender.py` builds previs; C4 renders at 1280 × 720 by default; C3's examples are 16:9; A3's 42 to 44 pages suggest 40 minutes or more; C1 costs a 20-minute film.
- **Read instead**: B3's script is retired and its plan becomes the LOCATION set plan; every size follows the chosen frame shape; the first estimate is about 35 minutes (the 44 is a page count, not an estimate), so C1's costs scale by about 1.75.

### 20. Sides and rings in example phrases (K26)

- **Applies to**: C2 §8 R2, C2 §8 R4, C2 §9, C2 §10; A3 §5.4; B5 §10.
- **The research says**: C2's example phrases say "left sleeve torn off at the shoulder", "Iona's left sleeve gone", "wound on his left shoulder", and put "simple gold wedding ring on her left hand" in the look line; A3, B5 and C2 use their own state labels (L1 to L5, C1 to C6, S1 to S6).
- **Read instead**: Iona's torn sleeve and skinned palm are on her own right, Jude's wound on his own right shoulder (small choices at checkpoint B); rings live in state lines; states are `CH-IONA.S01` and on.

### 21. Data words (K28)

- **Applies to**: A3 §1, A3 §3.2; C1 Recipe 10; C2 §6.6; A2 §11; D7 §14.
- **The research says**: A3 writes playable actions as infinitives ("to warn"); C1 and C2 use `null`; A2 writes `must-keep`.
- **Read instead**: one -ing word in `tactic`; `none` for empty; lowercase snake_case values (`must_keep`).

### 22. Slow motion as a fix (K30)

- **Applies to**: C1 §9; B1 §6.1.
- **The research says**: C1 fixes smeared fast motion with "Slow-motion in prompt then speed up in edit".
- **Read instead**: allowed only as a way of generating whose playback is real time, logged as a `speed` finishing job; slow playback is banned in The Catch (check CRAFT-16; D11 R15).


---

## Corrections from the H3 handover (10 October 2026; Project notes 42 and 43)

These come from testers' notes and from a clip file made by hand for MiniMax H3, not from runs on the user's own setup, so the rules they bring stay judgements (J) until the take log confirms them.

### 23. Stillness written as a list of still parts (D15 R6)

- **Applies to**: D15 R3, D15 R6, D15 R8, D15 §1, D15 §2.2, D15 §4.3, D15 §8, D15 §9; D15 Ex1, D15 Ex2, D15 Ex6; C3 §6; card 10's camera example; B1 §15's "Push-in on realization" phrasing and the same line in the B1 digest's Rephrase list.
- **The research says**: D15 rule 6 (item 8 of the digest, which Project notes 42 calls "rule 8"): "If a hold is 2 s or longer, then name every still part and the one moving part, and add 'The camera does not move.', because models fill empty time [J]." Its examples and checklists write stillness the same way ("her head and hands stay completely still"; "stillness held"), and rule 3 asks for display level 1 "with 'still' or one movement".
- **Read instead**: a hold of `hold_action_every_s` or more is written as small timed actions, one at least every 2 seconds (a breath, a blink, a swallow, a glance, a hand that adjusts something), and the camera gets one plain sentence. Testers found that models read a list of still parts as an order to freeze (a strong "do not move" line spreads over the whole shot, so a face looks like a photo with moving lips), and that time with nothing happening in it is squeezed out or frozen (the h3-storyboard testing notes, checked 10 October 2026). "Less display, more time" stays: the time is filled with small actions. The subject's `still` part is no longer asked for or sent to a model (checks CRAFT-26 and CRAFT-27). D15 R6 and R3 are rewritten in place, dated: display level 1 is one small action, with breath and blinks going on. The prompts of D15 Ex1, Ex2 and Ex6 are marked withdrawn where they stand (added 10 October 2026 after the cross-examination of Project notes 43). B1 §15's push-in phrasing now ends "while she breathes and blinks", as card 10 does (added 10 October 2026 after the second cross-examination of Project notes 43).

### 24. Motion only with a start picture, on MiniMax H3 in reference mode (C3 R1)

- **Applies to**: C3 R1, C3 §9A, C3 §3C; card 21's "motion only" fix.
- **The research says**: "If the shot starts from an image, then write motion only and call people 'the woman', 'the man', because Google says re-describing the image confuses the model."
- **Read instead**: C3 R1 (motion only with a start picture) does not apply to MiniMax H3's reference mode, where each person's description is repeated word for word next to their picture label (`<Subject 2> ... comes from <Picture 2>`); rewording a description there re-rolls the face (MiniMax's reference-mode prompt guide; Project notes 42). For other image-to-video models R1 still holds. The route is described in C3 §25.

### 25. H3's camera line (C3 §4; the adapter entries for MiniMax H3)

- **Applies to**: C3 §4's H3 row; `camera_static` of `minimax-h3` and `minimax-h3-max` in `_config/adapters/video_models.json`; the phrasebook's `hold` line.
- **The research says**: H3's static camera is written "holds a perfectly static shot [static]", and Stage added "The camera does not move." after it.
- **Read instead**: for both H3 entries (the hosted service and the ComfyUI route) the camera gets one sentence, "The shot is static, on a tripod, with no camera movement whatsoever." Testers found that extra camera lines ("no push in, no zoom ...") made cuts drift and the camera move, and that this one line holds (the h3-storyboard testing notes, section 7.2, checked 10 October 2026). Marked J until the take log confirms it.

### 26. The stillness example for shot 150 (card 21; step 14)

- **Applies to**: card 21's worked examples (The Catch, shot 150; The Long Places, scene 5) and step 14's purpose paragraph, as written before 10 October 2026.
- **The research says**: the prompt for shot 150 ends "Her head and hands stay still; only her eyes move. The camera does not move. No background music.", quoted as good practice.
- **Read instead**: that ending is withdrawn (entry 23): a held moment is written as small timed actions, the camera gets one sentence, and for a model with no negative side music with none is written "N/A". Card 21 and step 14 now quote the new form.

### 27. A listener written as "listening, does not speak" (A4 AI7)

- **Applies to**: A4 AI7 (rule 55 of the A4 digest, and its "Listener clips" line); the D3 digest's listener line; card 14's listener example (A1 §11).
- **The research says**: "If a shot shows listening, then prompt 'listening, does not speak', strip the audio and lay the line over it, because lips stay still and cuts stay movable."
- **Read instead**: write what the listener does, as small timed actions with the lips closed ("her lips closed; she breathes in; at about two seconds she blinks; her eyes stay on him"), then strip the audio and lay the line over it as before. "Listening" is no action (CRAFT-26 counts it as none), and "does not speak" names what is absent, which a model with no negative side adds to the picture instead (ComfyUI's MiniMax H3 prompt guide; the h3-storyboard testing notes, both checked 10 October 2026; Project notes 42 and 43). Marked J until the take log confirms it.

---

## Corrections later research files make to earlier ones

| Applies to | The earlier file says | Read instead | Source |
|---|---|---|---|
| C5 §6.11 | skills do not sync between Claude surfaces | they sync when signed in, from Claude Code 2.1.273 | D1 §13 |
| C5 §10.1 | scene IDs are `SC` and two digits | three digits for works with more than 99 scenes, fixed per project | D1 §13; K01 |
| C1 Recipe 1 | "Claude's settings → Connectors → Add custom connector" | Customize > Connectors > "+" > "Add custom connector" | D1 §13 |
| C1 Recipe 7 | keep a Kling driving clip 2 to 5 seconds | the official minimum is 3 seconds | D15 §11 |
| C4 §3E | Kling 3.0 Motion Control runs "up to 15 s" | 10 seconds for a picture, 30 for a video, driving clip 3 to 30 seconds | D15 §11 |
| A4 §7.4 | the pump's signature in seconds | 11, 14 and 29 frames at 24 frames a second | D9 §10 |
| C5 E3 | Eli's hidden hand is his "right hand" | the script says only "His other hand" (line 224); keep only that it is hidden | D7 §14 |
| A4 §6.8 | two rupture devices at once only at "the film's biggest moment", used in SC06 | SC06 is the inciting incident, a planted rhyme for SC27 | D16 §12 |
| A3 §1 | "scenes 1 to 7 are one rescue" | SQ01 is SC01 to SC05 and SQ02 is SC06; the direction of travel still holds over scenes 1 to 7 | D16 §12; K13 |
| D13 §7.1 | checkpoint C covers a sequence of about 6 scenes | read the count from the sequence list (about 3 in The Catch) | D16 §12 |
| C5 §10 | `runtime_target` with no unit | PROJECT `runtime_target_s` | D2 §12 |
| D3 §9 | loudness in one `loudnorm` pass | D8's two-pass linear method (keep D3's 48,000 samples a second) | D8 §10 |
| D3 §10.5 | D9 presets `earpiece_radio`, `small_speaker` | D9's names: `earpiece`, `radio`, `device_speaker` | D9 §10; D10 §13 |
| D8 §9.4 | translations may add a forced narrative for RECEIVING (line 1620) | none | D18 §11 |
| D5 §10 | `post_chain` flips before compositing | for shots whose world lettering goes on before the flip, the flip happens inside the composite | D6 §12 |

---

## Citations given under the wrong number

These slips are in the build plan, in early notes or in the schema's wording. The rule meant is the one in the right-hand column; cards already cite it.

| Written | Meant | Why |
|---|---|---|
| "A1 R2" for landing off the speaker at least once per scene (card 04's list; check CRAFT-23) | A1 R1 and A1 §8 checklist item 5 | A1 R2 holds on the speaker |
| "B4 rule 17" for "a beat the script already marks gets nothing added" (department card anatomy; step 7) | B4 R23 | digest rule 17 is B4 R23; B4 R17 is about loud sets |
| "R25" for the engaged pair and the silent third (card 12's list; the schema's meaning of `engaged_pair`) | B3 §4.4 and B3 R5 | B3 R25 is the one-expressive-device rule |
| "B1 P6" for in-story footage (card 17's list) | B1 §10.4 | the B1 digest's procedure P6; B1's principle 6 is "position first, lens second" |
| "A3 rule 9" (card 18's list) | A3 R4 | digest numbering |
| "A3 rule 33" (check GEOM-07) | A3 §5.9 | digest numbering |
| "A3 rule 37" (check REASON-09) | A3 §7.3 | digest numbering |
| "C1 R25-R27" (card 20's list) | C1 R9, C1 §4 and C1 R10 | digest numbering |
| "C2 rule 31", "C2 rule 33" | C2 P4, §5 rule 9 and §7.1; C2 §5 rule 11 and §8 R5 | digest numbering |
| "C5 P8" (D14) | C5 §9 E1 and C5 Recipe 2 | the C5 digest's procedure P8; C5 has no P8 |
| "C3 §7A (languages)" | C3 §7B; keeping words off the screen is C3 §7G | D18 §11 |
| A2 R4 as "close-up or a deliberate wide" (step 6) | A2 R4: the scene's tightest size, or a deliberate wide | A2 R4's own words |
| "D15 rule 8" for the stillness rule (Project notes 42) | D15 R6 (entry 23 above) | digest numbering: the digest's item 8 is §3 rule 6 |
