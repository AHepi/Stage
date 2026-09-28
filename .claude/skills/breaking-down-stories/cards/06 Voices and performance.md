# Card 06. Voices and performance

Step 4 reads only "Voices"; steps 7 (Detailed) and 8 read only "Display and stillness"; add-on C reads only "Lip sync and voice takes". "D3 R13" names rule 13 in D3's numbered rules (§3); D15 and A1 rules are cited the same way.

## The job

Give every speaking character one voice that can be made the same way every time, and every acting body a performance a model can follow: what it does to the other person, what we see, how much shows, what stays still, where the eyes go (D3 §1; D15 §1). Step 4 hands on VOICE records. Steps 7 and 8 hand on `tactic`, `does`, `display`, `still`, `eyeline`, `dwell_s` and `must_not` on every subject. Add-on C hands on voice takes and a lip-sync route for every shot with a speaking mouth.

## Questions in order

1. Does the character speak in more than one scene? Then one VOICE record, locked before any picture shows their speaking mouth (D3 R1; K16).
2. What does the line do to the other person? Write the tactic as an -ing word and `does` as visible steps, never the feeling (D15 R1; A3 R2; WORDS-01).
3. Who carries the line? Where the listener's face can, the speaker is heard off screen (A1 R1; D3 R20).
4. What do the hands do? Frame a named task with the face; a task that stops is a reaction shot; where the script gives none in a talk scene, propose one marked `invented` (A1 R8-R10).
5. Is this look spent later? Then it goes in `must_not` on every earlier shot (D15 R9).
6. Does the shot continue the last one? Its subject starts where the last one ended (D15 R11).

## Voices

A VOICE record holds the fixed words for a voice (`voice_description`, `voice_description_words` long, frozen word order), its pitch band, pace, accent and path treatments (D3 §4.1).

1. **Build the voice from the character:** the age it reads as, pitch band, timbre in a few words, accent from `WORLD.accents`, pace, and status in the voice: high status is level, with falling ends and no fillers; low status adds rising ends and hesitation sounds (D3 §4.1; B5 §5.3). Saye's: "A woman in her fifties with a clear mid-pitched voice and crisp consonants; {accent}, formal; slow, even, complete sentences with firm falling ends; very still, no filler sounds; close, clean studio recording." (D3 §4.2; her age in the story's word, K26).
2. **Never name a real person** or write "sounds like" anyone, because a recognisable imitation is that person's voice in law (D3 R18).
3. **Pace is timing.** `pace_wps` defaults to `speech_wps_default`; a formal, weighted speaker is slower (K08 sets Saye slower). Code builds time floors from it (`speech_floor_extra_s`) and caps speech per clip with `clip_speech_rule`.
4. **Keep voices apart:** two voices that share three or more of age band, pitch band, timbre, pace, accent and status blur on small speakers; change pitch band or pace first (D3 R7, §4.3).
5. **Accent undecided** (`WORLD.accents` not set): every VOICE stays `draft` (D3 R6; blueprint 5.4 rule 10).
6. **Paths are sound, not acting.** A **path** is how a voice reaches us: direct, earpiece, radio, intercom, recording, through glass. A parenthetical naming a place or device ("in her ear", "over the radio") is a path (D3 R11). Each path gets one `path_sound` treatment, added after a clean take (D3 §1, R24); a line heard from both sides of a cut is treated per shot (D3 R25). Decide speech through glass once, as a story-world rule: intercom for speech, "through glass" only for knocks and breath (D3 §8.1).
7. **Speech habits go in `speech`** and in the edit: a speaker who never contracts keeps it in every take (D3 R8); "Eli thinks before he answers. He always does." (line 1142) is a silence placed in the edit (D3 R9).
8. **`source` defaults to `designed`,** a small choice. Cloning is only for the user's own voice or a consenting, verified adult with a RIGHTS record; never a celebrity, a minor, a dead person, or from films and recordings (D3 R16-R17; card 24).

## Display and stillness

**Display** is how openly the body shows the pressure: 1 contained (one or two small changes, the rest still), 2 visible (two or three changes nobody can miss), 3 open (whole body, audible) (D15 §2.2).

1. **The closer the shot, the lower the display.** Display 3 in a close-up reads as melodrama; `display: 3` at `display_3_needs_why_at_or_tighter` or tighter needs a `why` (D15 §2.2; A1 P10, R36; CRAFT-25).
2. **Beat intensity is not display.** A beat of the highest intensity often plays best at display 1 (D15 §0; K14).
3. **If the line, the eyeline or the cut already carries the beat,** use display 1: still, or one small action (D15 R3).
4. **On a turn,** write the five steps as timed behaviour: the want as an eyeline, seeing the obstacle, the choice as a held moment, the action, and the face before the line (D15 R2, §1).
5. **Write stillness.** A moment of `hold_needs_still_s` or more, or a pause held on picture, names every still part in `still`, because models fill empty time with nods and drift (D15 R6, §1; CRAFT-26). Lips that part in silence need "No dialogue." and "closes it without a sound" (D15 R7).
6. **Eyes carry thought.** `eyeline` names a target and `dwell_s` how long; never "looks around". Singles made separately look past the lens on opposite sides and never into it (D15 R10; A1 R40, R44).
7. **Energy changes inside a shot, never at a cut;** breath not seen (a helmet, a back) is carried in sound (D15 R12-R13).
8. **Pauses:** tiers come from `pause_tiers`, with at most `long_pauses_per_scene_max` long pauses per scene (A1 R15; D15 R8); a turn's reaction lasts at least `turn_reaction_min_s` (TIME-05).

## Lip sync and voice takes

1. **Voices first.** No clip with a visible speaking mouth before the VOICE is locked; a model's own voices only for drafts and one-line parts (K16; D3 §1).
2. **Route order:** where the listener can carry the line, play it off screen; where the mouth must be seen, a video model that takes the line's audio as input first, lip sync after generation second, a cutaway third (D3 R20-R21; blueprint 8.5).
3. **Code derives `lip_sync`** from face height; a speaking face at `lip_sync_tight_face_height` or larger needs tight sync.
4. **A visor, glass, a hand or a prop over the mouth:** avoid on-screen sync; play the line from behind, in profile or on the listener. When lip sync fails twice on one shot, cut to the listener or an insert (D3 R22-R23).
5. **One speaker on screen per clip** (`on_screen_speakers_per_clip_max`, GEN-13), and at most `acting_characters_per_clip_max` acting.
6. **Takes:** three per line; for delivery parentheticals and turning lines, two alternates of three takes each; transcribe each take, reject wrong words, pick by ear (D3 §5.3, R10, R15). A VOICETAKE (one take of one line) keeps its `delivery` within `voice_delivery_words_max` words; `tts_text` keeps the story's exact words (D3 R14). "(beat)" splits a line into two files; very short lines are made inside their exchange (D3 R12-R13).
7. **Seat every line** in continuous room sound (D3 R27).

## Translation menus with pitfalls

Pick one behaviour, primary first, tied to this line; the rows are untested until D15 §4.4's test is run (D15 §4.2):

| Script word | Behaviour | Pitfall |
|---|---|---|
| shock | stops moving completely; eyes fix on Saye | a gasp, a hand to the mouth |
| holding back | eyes go to the flask, not to her; does not answer | shifty eyes |
| speechless | opens her mouth, holds it, closes it without a sound | generated speech: add "No dialogue." |

Delivery words come from the tactic: pressing becomes "level, quiet, unhurried, no rise" (D3 §5.2).

## Budgets and saved choices

`long_pauses_per_scene_max`; `display_3_needs_why_at_or_tighter`; `hold_needs_still_s`; `on_screen_speakers_per_clip_max`; `acting_characters_per_clip_max`; `voice_description_words`; `voice_delivery_words_max`. One display peak per scene, at or after the main turn (D15 §8).

## The baseline is a strong answer

Display 1, a still head, eyes on the other person, room sound and a clean designed voice at `speech_wps_default` are choices, not failures. Most reactions to a turn are contained: the camera magnifies (D15 §2.2; A1 P10).

## Cliché traps

Tests: any-film, mood-word, stacking, sound-off (card 05).

- "Looks sad" in `does` fails the mood-word test. Fix: two or three timed behaviours (D15 R1; WORDS-01).
- Sobbing in a close-up: display 3 where 1 would land (A1 R36; CRAFT-25).
- A hold with stillness unwritten comes back nodding and swaying (D15 §9).
- An early glance spends the later look (D15 R9).
- Stacking: a sad face, a sad line and music under it (A1 P10).

## Reasons that fail and reasons that pass

- Fails: "Close-up so we feel her shock." Passes: "SC10-B07, 'Her face changes.': display 1; she stops chewing, brows draw together, eyes drift down, and the line comes after the face (D15 Ex1, R2)."
- Fails: "Saye sounds cold." Passes: "VO-SAYE speaks in complete sentences with falling ends and no contractions until 'Saye has lost the voice she uses for answers.' (line 1383) (D3 §4.2, R8)."

## Two worked examples

### The Catch: SC10, "Not mint." (SC10-D11)

The scene's closest frame holds Iona through the line. Her subject item at step 8, built from D15 Ex1:

```
- subject: CH-IONA.S02 | at: left_third | faces: camera | eyeline: CH-SAYE | does: chews steadily; chewing slows and stops; brows draw together slightly; eyes drift down; chews once more, very slowly | tactic: discovering | energy: held | display: 1 | still: head, hands, torso | must_not: looking at Eli
```

The glance at Eli is saved for "Iona moves between her and Eli." (line 476). A raised upper lip reads as disgust, but the taste is familiar and wrong, so it goes on the take review's list with tears (D15 Ex1, §8). The take's delivery is "breath caught, quiet"; Saye's reply stays in her answers voice for contrast (D3 §11.1).

### The Long Places: "two breaths entire" (line 419)

Prose gives time in breaths: Melek "stood in the waiting, two breaths entire". Two calm breaths run longer than the long tier of `pause_tiers`, so the shot is a hold that needs a saved choice (K10; TIME-08). Breath is visible: the shoulders rise and fall twice and nothing else moves, so `still: head, hands` and `energy: held` (D15 Ex6). The knock passes to Yusuf and Nilay: record it once, as a MOTIF with `channel: body`, and keep its timing each time it returns (D15 Ex6).

## Self-check

- Does every recurring speaker have a VOICE with a description of `voice_description_words`, no real name, a pitch band, a pace and an accent from WORLD?
- Does every subject have a tactic, a `does` with no emotion words and a display that fits the size?
- Does every hold of `hold_needs_still_s` or more name its still parts?
- Does every `eyeline` have a dwell, and every saved look sit in earlier `must_not` items?
- Is the listener used wherever it can carry the line?

## Words for AI models

Works: behaviour steps joined by "then"; named body parts ("her lower lip"); stillness with its length ("her head and hands stay completely still; only her eyes move"); "The camera does not move." on a hold; "No dialogue." for silent lips (D15 §4.3, R6; C3 L14). Tone words only for the voice ("says quietly and unsteadily") (C3 §6). In a draft whose voice the video model makes, name the path: "his voice, heard only in her earpiece, thin; he is not visible" (C3 §7F).

Fails: emotion labels; `must_not` written as "no X" in a prompt (D15 §0); a one-sided expression's side in words (flip an approved still, D15 R19); long acting notes to a voice tool, which make the voice drift (D3 §2A).

## Look up for more

D3 §1, §3 (R1-R27), §4 (voice design), §5 (delivery), §8 (paths), §11; D15 §2 (display), §3 (R1-R24), §4.2 (behaviour words), §6, §10 (Ex1-Ex6); A1 R1, R8-R10, R15; C3 §6; K08, K10, K16. Print one rule with `stage.py lib D15 R9`.
