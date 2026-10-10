# Card 23. Finishing, captions and delivery

Add-on D and step 11 read it whole. "D8 R41" is rule D8-R41 in D8 §4 and "D8 Rec10" its recipe 10 (§5); "D6 R15" is rule 15 in D6 §4 and "D6 VC8" check 8 of its layer plan (§8); "D18 R11" is D18-R11 (§4); "D9 R4" is rule 4 in D9 §3.

## The job

Turn kept takes, voice takes, effects and records into one film that can be watched, captioned, described, translated and delivered. Code creates a FINISH record for each operation a shot needs and, at step 11, writes the timeline files (`timeline.otio`, `timeline.edl`), the caption files, the audio-description script and the text-to-translate list (blueprint 8.7, 5.9). The AI fills each FINISH record's `tool`, `inputs` and `output`, runs simple jobs (flip, crop, a still overlay, a speed change, joining) as ffmpeg commands on code surfaces, writes click-by-click steps for DaVinci Resolve's free version where hands are needed, spots MUSIC cues when the policy allows them, and hands on the assembly guide.

## Questions in order

1. **In what order?** "Time before size, size before colour, colour before grain" (D8 §2); inside a composite, tools that redraw pixels run before any exact layer (D6 P2, R6).
2. **One frame rate?** The whole film runs at `PROJECT.fps`; measure every take (D8 R9). A slower take made against a guide video of the same frame count plays at the film's rate; a free one is interpolated after picture lock (D8 R11-R12); slow generation returns to real time as a `speed` job (K30); in-story footage is never interpolated (D8 R15).
3. **Does it fit the frame shape?** Crop to `frame_shape`; where a head, hand or prop leaves the band, move the clip and log it (D8 R17-R19). Cropping away a visible watermark counts as removing it (D8 R26).
4. **How many flips?** A layer shows mirrored after an odd number of flips, normal after an even number (D6 §5, VC1). World lettering goes on normal before the whole-frame flip or mirrored after it, never both (D6 R15); a shot flipped inside its composite is not flipped again (D6 VC8).
5. **Upscale?** Only kept takes, after **picture lock** (when shot lengths stop changing): whole takes to 1080p so the edit relinks, used seconds plus handles to 4K only if delivery needs it; a precision upscaler before a diffusion one, which redraws detail and can change faces; in-story footage never (D8 R20-R23; D13 R14).
6. **Grade.** First a **normalize** step per model, removing its own colour and contrast; then each sequence graded to its style picture; motif colours stay fixed, and a light change the story writes is never graded away (D8 R28-R33). Darker skin stays rich, never grey or ashy (B2 R24). One grain for the whole film, once, after the grade (D8 R34; D6 R20).
7. **Sound.** Three **stems** (separate dialogue, music and effects mixes), so a dub swaps only dialogue (D8 R37); loudness set per deliverable over the whole film (`SOUNDPLAN.loudness_target`), a quiet film mixed to its dialogue (D8 R38-R39); each relayed voice through its path's one saved chain (D3 R24); a sound motif laid from one master file (D9 R12), never stopped dead at the end (D8 R41).
8. **Music?** Only as `SOUNDPLAN.music_policy` allows; under `none`, a drone needs a source in the story (D9 R1, R4); a cue enters on a motion or cut and leaves before a rupture (D9 §4.2). Every sound file carries a RIGHTS record, and a licence forbidding commercial use or changes keeps it out (D9 R19; D4 R15).
9. **Titles.** A card cuts in and out with no fade the script did not write, holds at least `text_floor`, uses one font under the SIL Open Font License, and stays inside the graphics-safe area (D8 R42-R45).
10. **Captions** (code times them, 5.9): the words come from the speech records, never from recognition (D8 R47); an off-screen speaker's cue starts with the name, italics only for a speaker not in the scene (D8 R52); an effect at sound emphasis 2 or more gets a sound tag, a motif always the same tag (D8 R51; D18 R7); backwards text gets no subtitle (D8 R53; D18 R22).
11. **Audio description**, a narrator's voice in the gaps telling a blind viewer what to see, covers every shot with `needs_description: yes`: what the frame shows, from `does`, never a feeling or anything kept hidden (D18 R3, R10); what a later payoff needs comes first (D18 R9); about `speech_wps_default` words per second of gap, ending before the next line (D18 R11); designed silences stay empty (D18 R4).
12. **Translation.** TEXT with `translate: yes` goes on the text-to-translate list; translators work from an annotated template, not the captions (D18 R18); a name that is a word in the target language gets a note (D18 R19); a glyph chosen for its shape is never translated (D18 R32).
13. **Delivery.** Keep a textless master, stems, caption files and raw downloads with their provenance marks, never stripped (D8 R60; D4 P8); the disclosure line is card 24's.

## Translation menus with pitfalls

One method per job, by the FINISH `operation` (blueprint 8.7):

| Operation | When | Pitfall |
|---|---|---|
| `flip` | The mirror routes "flip all" and "flip with mirrored references" | A second flip in the edit (D6 VC8) |
| `composite` | Text graphics, screens, plates with people, beads | An element sharper or cleaner than the plate (D6 R21, Rec9) |
| `speed` | Retimes; slow generation back to real time | A free slow-rate take simply played faster (D8 R12) |
| `upscale` | Below master size after the crop | A diffusion upscaler redrawing faces (D8 R22) |
| `deflicker` | Brightness pumping | Expecting it to steady crawling detail (D8 R25) |
| `grade` | Every sequence | A lookup table on raw takes (D8 R35) |
| `lip_sync` | A mouth that must be seen | A third try instead of cutting to the listener (D3 R23) |

## Budgets and saved choices

- `caption_lead_s`, `caption_min_s`, `caption_max_s` time every cue; longer speeches split at a sentence end (blueprint 5.9).
- `text_floor` holds every card and text in picture, doubled when mirrored (K09).
- `device_budget_short` caps editor-made cuts to black, true silences and freezes; a black the script writes is outside it (A4 P10; D8 §9.3).
- `handles_s`: the spare picture each side of every used part (D8 §1).
- `sound_motif_max` caps sound motifs (B4).

## The baseline is a strong answer

A hard cut, room sound under every line, one grain, one font, caption files beside the picture rather than burned in, and no music under `music_policy: none` are choices, not failures (D8 R42, R34, R44, R55; D9 R1). Depart only for what the story writes.

## Cliché traps

Tests: any-film, stacking and sound-off (card 05), plus **eyes closed** with the description track and **sound off** with the captions (D18 Rec7).

- **Fades and dissolves the script never wrote** (D8 R42; A4 T5). Fix: a cut.
- **A musical hit on a reveal the script already marks** (D9 §7; B4 R23). Fix: remove it.
- **A drone with no source** under `none` (D9 R4). Fix: a story source, or silence.
- **The generator's own colour left in**, or one "film" preset over everything (D8 R28, R35). Fix: normalize, then grade each sequence.
- **Grain asked for in prompts, or added twice** (D5 R18; D6 R20). Fix: one grain, after the grade.
- **Generic tags** such as "[music]" or "[speaking foreign language]" (D8 R54). Fix: name the sound and its pattern.
- **Description that interprets**: "she is horrified" (D18 R10). Fix: what the frame shows, from `does`.
- **A quiet film pushed loud for the web** (D8 R39). Fix: mix to the dialogue.

## Reasons that fail and reasons that pass

- Fails: "Dissolve into the morning to show time passing." Passes: "Hard cut into SC11: the story writes no transition there (D8 R42; A4 T5)."
- Fails: "[pump thumping]". Passes: "[three uneven pump strokes], the motif's one tag, because its payoff depends on the pattern (D18 R7; D8 R51)."

## Two worked examples

### The Catch: the end of SC10 (lines 484-488)

"Nobody leave this room." (line 484) is followed by "> CUT TO BLACK." (line 486) and "= THE CATCH" (line 488). The CUT record SC10-C200 is `cut_to_black`; SC10-SH990 is the title card TX-TITLE-CATCH, white on black inside the graphics-safe area, cut in and out, held beyond its `text_floor` in true silence: the kitchen's room sound stops with the picture and `music_policy` is `none` (D8 R42-R45, §9.3). The script writes this black, so it spends nothing from `device_budget_short`. In SC10-SH150's captions "Not mint." is its own cue of at least `caption_min_s`; Saye's lines begin "SAYE:" because she is off screen, but are not in italics, because she is in the room (blueprint 5.9; D8 R52). The description, in the gap before Saye's question, gives the face as behaviour: "She chews, then stops. Her eyes drift down. One more slow chew." (D18 §7.2).

### The Long Places: the knock (lines 419-421)

Melek "knocked twice, softly, and then stood in the waiting, two breaths entire" (line 419). The description speaks before the knock ("Melek lays her palm on the stone beside the niche. Knocks twice, softly.") and then nothing: the two breaths are a designed silence (D18 R4, §8). The captions name the sound, not a source the book never names: "[two soft knocks]", then "[a low, shaped sound under the knock, no words]", not D18 §8's "voice", which the sound design refuses (D18 R8). The answer, "Low. Shaped. With the fall of a sentence in it." (line 421), is built from breath and room resonance, never a generated voice, which would settle what the book leaves open (D9 §8.4). "the waiting was the rite, if it was a rite" (line 419) is the narrator's thought, never description (D18 §8).

## Self-check

- Does every derived operation have a FINISH record with tool, inputs and output, and no shot a second flip?
- Is every take at the film's frame rate, cropped to the frame shape, and upscaled only after picture lock?
- Is there one grain and one font, and a RIGHTS record for every sound file and font?
- Do captions use the script's words, and does description skip designed silences and hidden things?
- Is every watermark and provenance mark kept?

## Words for AI models

Works: ffmpeg commands the AI writes and runs for simple jobs (blueprint 8.7); for a music cue, "Instrumental only, no vocals.", a tempo, two to four instruments, a timed shape and "one sustained note that decays naturally" at the end (D9 §4.3); for an effect, its source, its action and the space around it (C3 §7E).

Fails: artist names, song titles or lyrics in a music prompt (D9 §4.3); a generated voice where the story keeps a sound unknown (D9 §8.4); speech recognition as the source of caption words (D8 R47).

## Look up for more

D8 §4, §5, §9; D6 §4, §5 (layer order), §6, §8; D18 §4, §5, §7, §8; D9 §3, §4, §8; A4 T5; blueprint 5.9, 8.7. Print one rule: `stage.py lib D8 R41`.
