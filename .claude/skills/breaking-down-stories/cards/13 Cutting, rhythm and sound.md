# Card 13. Cutting, rhythm and sound

Step 6 reads "Sound plan"; step 7 (Standard) reads "Scene rhythm"; step 8 reads "Cut points and sound"; chat apps read it whole. "A4 R4" and "A4 SND7" are rules in A4 §9; "D9 R3" is rule 3 in D9 §3.

## The job

In The Catch the fall ends on "A hard metal CLACK." and "BLACK. A dark with nothing in it. One instant." (lines 259-261): the CLACK lands on the first black frame, true silence follows, and "Her eyes open." brings every sound back (A4 WE1). This card decides where cuts fall, how long shots run, how shots join and what is heard (A4 §0), handing on SOUNDPLAN (step 6), scene rhythm (step 7) and shot timing, cuts and sound (step 8). A **turn** is the beat where a value changes for good (card 03).

## Questions in order

1. What editing and sound marks does the text write? They outrank every other rule (A4 §5.1, §9).
2. What is the music policy; where are the planned ruptures (D9 P4; K12)?
3. Is the turn an event or a realization (A4 R4)?
4. Who knows what (A4 S2)?
5. What pattern does the scene teach; where does it break, once (A4 P7)?
6. Why does each cut fall where it does (A4 P3)?
7. Which one sound must be heard now (A4 SND7)?

## Sound plan

Example: The Catch defaults to `music_policy: none` (K31), so the pump, "three strokes, not quite even" (line 852), is its sound motif, at sound emphasis 3 only over black at the end (K12; B4 M10). The planned sound rupture is scene 26, where the ship's hum stops: "The sick motor through them." / "Then not." (lines 1508-1510).

- The **music policy**: `none`, `sparse`, `scored`, or `source_only`, music the characters hear (D9 §5).
- A **rupture** is the film breaking its own pattern at a turn: a change in the telling, not a loud event (A4 §6.8).
- The **device budget** caps the editor-made cut to black, true silence and freeze (A4 P10).
- A **sound motif** is a returning sound with one rhythm and timbre; only its path and loudness change (A4 §7.4).

Rules:
- `music_policy` is the user's (checkpoint B): propose, never set. Every clip stays music-free (`clip_audio`; D9 P1, P4).
- Propose `none` when the story gives no reason for score (D9 R1). `sparse`: few cues, each at a paragraph break (title, act change, end), never under an open reveal (D9 R3; A4 SND5). Under `none` a drone needs a source in the world, such as the ship's hum (D9 R4); a radio the story names plays murmured speech, never a tune (D9 R4a).
- A MUSIC cue has `in`, `out`, `function`, `must_not` and `licence`; it enters on a motion or a cut and leaves before or on a rupture (A4 §7.6; D9 §4.2).
- `device_budget`: one item per device, `max` from `device_budget_short`. Marks the story writes, and freezes a character makes on a screen, do not count (A4 §13; CRAFT-12).
- `rupture_plan`: one line per planned rupture, from PLAN's `peak` items; two devices at one moment only at the film's largest turn (A4 §6.8, §6.9).
- At most `sound_motif_max` sound motif, recorded once as a master sound, its rhythm in the MOTIF's `signature`; each appearance is a copy with its own path and `sound_emphasis`, emphasis 3 once per motif (D9 P2, R12; B4 §3.4).

## Scene rhythm

Example: The Catch scene 13 is a slow burn, long holds on the recording broken by her thumb on the remote and the freeze; scene 6 builds, breaks and lets the aftermath sit; scene 5 builds and cuts out into the cage (A4 §6.2).

The **rhythm shape** is the curve of shot lengths across a scene; the **average shot length** (`target_asl_s`) is screen time divided by the number of shots.

1. **`rhythm_shape`** (A4 §6.2): `build_and_cut_out` when the turn launches action into the next scene; `build_rupture_aftermath` when the turn is a loss, shock or revelation to absorb; `slow_burn` for talk, waiting or watching that turns on one line, look or discovery; `steady` only for a scene with no turn. Plan the curve before any duration: "build 4 s to 1.5 s over B1-B6; rupture B7; aftermath 5 s+" (A4 §10).
2. **`target_asl_s`**: speech shots from their time floors (the least time their words need), others from `non_dialogue_seconds_by_intensity` (K10; A4 §6.1), times the tone's `shot_length_factor` in `tone_defaults.json` (D10 §2.2); never from `rhythm_class_asl_s`, which feeds only the estimate (D13 §5). After a scene at `high_intensity_scene_min` or more, the next target is longer (FILM-07; A4 §6.9); the film stays inside `film_asl_range_s` (TIME-07).
3. **The main turn gets an extreme** (A4 R4, P5; TIME-10): the scene's shortest shot for a physical event (an impact, a fall, a black), its longest for a realization, a choice made, a revelation or a refusal. A turn that is both: the event gets the shortest shot, the realization after it a hold longer than its neighbours.
4. **Suspense**, the audience knowing a danger a character does not, holds longer on the unaware and never cuts faster (A4 S2; TIME-09).
5. **`rupture`** on the main turn or the beat causing it: a `device` (`hold`, `drop_out`, `true_silence`, `cut_to_black`, `camera_change`, `pov_change`) and `breaks`, the pattern taught first; one re-orienting shot follows. A gunshot is action, not a rupture, unless the telling breaks too (A4 §6.8).
6. **`room_sound: as_place`** unless the story changes the place's sound; in the dial (the per-beat plan) `sound` stays `room_sound` except at the rupture or a story source, never on a beat the script marks (blueprint step 7; B4 R23; CRAFT-10).

## Cut points and sound

Example: in The Catch scene 6, "Closes her eyes." is cut on the eyelids closing, and "This time they hear it land." (line 298) is the sequence's longest shot, its decay running under scene 7's "Tell me that was the brake." (line 305) as an L-cut (A4 WE1).

A **split edit** changes sound and picture at different moments: a **J-cut** starts the next shot's sound early; an **L-cut** lets this shot's sound run on. **Room sound** is a place's steady background, so no silence is dead (A4 §1, §7.3).

- `cut_out_on` (`thought_complete`, `action_midpoint`, `line_end`, `sound_hit`, `rhythm`, `withholding`; at Detailed also `cut_in_on`): cut when the thought changes (a look, a breath, a word that hits), not at every line end (A4 P3, §3.7). Unsure: cut later (A4 R2).
- An action crossing a cut: cut mid-action, the whole action in both clips (A4 R3); cutting away: let the motion rest first (D11 R9). A reaction follows the event fully seen, unless hiding it is the point, `cut_out_on: withholding` (A4 R7).
- `screen_time` never under the time floor code derives, the least time its speech, text and pauses need (TIME-01; K09, K10). Consecutive shots of one subject change a size step or at least `geometry_angle_change_min_deg`, unless it is a jump cut (A4 C4; GEOM-02).
- A CUT only where the join is not a plain cut: `j_cut`, `l_cut` (with `split_s`, `sound_across`) are free (A4 SND6); `match_cut` names the shared shape, motion or sound in its `why` (A4 T3); `dissolve`, `fade`, `cut_to_black`, `freeze`, `smash_cut` only where the story writes them (A4 T5; CRAFT-13), `cut_to_black` with `black_frames` and what the sound does (A4 T4).
- `hear` each speech (`speaker: on_screen`, `off_screen`, `hidden`); a listener shot hears it off screen (A4 AI7); a speech over `clip_speech_rule` splits at a phrase under a listener shot (A4 AI5).
- `effect` items (`at`, `sound_emphasis`) for sounds tied to actions; every sound the script writes in capitals becomes an effect, the room sound or a MOTIF appearance (COVER-07).
- `silence`: `none`; `room_sound_only`, room sound plus one small real sound; `drop_out`, the background suddenly thins, a rupture; `true_silence`, nothing, from the budget (A4 §7.5, SND4).
- `music: none` under an open reveal or a beat with an `unsaid`, a thought not spoken (A4 SND5; FILM-09).

## Translation menus with pitfalls

Pick at most one per beat; tie it to a line, object or action in this story (A4 §8):
- Rising pressure: shorter shots, one more sound layer. Pitfall: music.
- Dread: longer holds on the unaware, one off-screen sound. Pitfall: faster cutting.
- Shock: the shortest shot, a loud sound, then quiet. Pitfall: a sting where the script marks the beat (B4 R23).
- The world indifferent: a machine carries on (A4 §7.1).

## Budgets and saved choices

- `device_budget_short` (CRAFT-12); `pause_tiers`, `long_pauses_per_scene_max`; a `hold` beyond the long tier needs a saved choice (K10; TIME-04, TIME-08).
- `turn_reaction_min_s` after every turn (TIME-05); `sound_motif_max` (FILM-10).
- A sound change counts toward `signals_changing_per_beat_max` (CRAFT-19); `added_emphasis_per_beat_max` (CRAFT-10); `named_sounds_per_prompt_max` (GEN-17).

## The baseline is a strong answer

A plain cut, room sound, `silence: none` and `music: none` are choices, not failures, and need no `why` (blueprint 5.4 rule 11). Depart only for a reason you can cite: a written mark, the turn, the rupture plan (A4 T1, SND4, SND5).

## Cliché traps

- **Cutting on every line.** Test: shot count equals line count. Fix: cut on beat changes, L-cuts to the listener (A4 §13).
- **The average peak.** Test: the turn shot as long as its neighbours. Fix: make it the scene's shortest or longest (A4 R4).
- **A sad cue under unspoken sadness.** Test: does the frame tell the beat with the music off? Fix: remove it (A4 SND5).
- **Dissolves the script never wrote.** Fix: a cut; light and room sound carry the gap (A4 T2, T5).
- **Dead silence; room sound jumping at cuts; a last sound cut mid-pattern.** Fix: room sound under every silence, even across cuts; let the last sound finish (A4 SND4, AI4, SND8).

## Reasons that fail and reasons that pass

- Fails `music: MU-01` "to build tension" (REASON-04). Passes `music: none` (K31): the pressure has a story source, "The hum under the floor wavers." (line 1311) (D9 R4).
- Fails a dissolve into scene 8 "to show time passing". Passes a plain cut: the script only cuts, and "Two streets away. Her car, where she left it." (line 335) carries the gap (A4 T2, T5).
- Fails scene 10's turn shot at average length. Passes SC10-SH150 as its longest: "Her face changes." (line 456) is a realization (A4 R4).

## Two worked examples

### The Catch, scene 30 (the pump over black)

Hold the vessel on the cloth through two pump cycles after "The tapping stops.", lowering the room sound. The story writes "CUT TO BLACK." (line 1848): a CUT with `black_frames` in the rest between cycles and `sound_across: MO-PUMP`, so the dark opens on one whole "Three uneven strokes in the dark." (line 1850). No music; the pump goes on or recedes, never stops dead (A4 WE3, SND8).

### The Long Places, chapter VII (contemplative)

"For three days the little rig argued with the hill" (line 573): a montage, short shots compressing time, cut on the drill's note, each day a jump cut in one repeated framing of Melek. The rupture is "the drill's note went hollow" (line 575), `device: drop_out`, then a hold on Márton in room sound only. The lost camera is heard, not seen, "a knuckle on wood, once." (line 581): one small knock, no bounce, because it plants "It is a cylinder. They stand, or they roll." (line 593) (A4 WE4; D9 §8.4).

## Self-check

1. Every written mark honoured, no join added?
2. Each main turn's shot the scene's shortest or longest, by the kind of turn?
3. At most one rupture per scene, on the turn, after a taught pattern?
4. Cut reasons, room sound and silence grade on every shot?
5. Every clip music-free, every cue inside the policy?

## Words for AI models

Works: only what happens inside the clip: speech with its speaker, sounds tied to visible actions, the room sound, "No music." (A4 §7.8); for a listener, "listens, does not speak" (A4 AI7). Fails: "then cuts to" (A4 AI2); split edits or motifs, which live in CUT and MOTIF records; asking for silence, which models fill; make it in the edit (A4 §7.8); feelings or artist names in a music prompt (D9 §4.3).

## Look up for more

`stage.py lib A4 §9`, `A4 §6`, `A4 §7`, `A4 §11`; `D9 §3`, `D9 §4.2`, `D9 §8`. `D10 §2.2`, `D13 §5`; K10, K12, K31.
