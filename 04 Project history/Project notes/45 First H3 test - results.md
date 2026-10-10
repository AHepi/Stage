# 45 First H3 test - results

Log entry 45, 10 October 2026. The first test of Stage's MiniMax H3 route (handover item W1) on a rented pod. The clips, the take log and the prompts hold story material, so they stay outside git; this note holds what was learned. No pod names, account details or story text from scenes 1 to 6.

## One example first

Scene 5's trip, made twice by H3 with the same pictures and seeds:

- **The one-line prompt** (one sentence for the whole action): Iona swings the pole up and over; the guard never falls; in one take the guard does the kicking. The story action never happens, in either take.
- **Stage's two-shot contact-cut prompt:** the low swing lands at 2 seconds; the cut comes at about 2.5 seconds (written 2.6) to a low view on the floor with the guard already down and the pistol by his hand. In one take the boot shoves the pistol out of the frame; in the other it steps on it.

The rule behind it (route rule 26: cut at the contact, open the next shot on the result) worked in both takes.

## What ran

- **14 runs,** two seeds where it mattered:
  - two start pictures made by H3 from the character pictures
  - "Not mint." (scene 10 shot 150 / clip 07, 362 frames) with Stage's old prompt, its new prompt, and the new prompt with Iona described as in her picture
  - the trip with the one-line prompt and with Stage's contact-cut prompt
  - clip 04 from the clip file with Jude described as in his picture
- **Plus one warm-up** with no story (a plain grey wall), to load the model and test the whole chain.
- **The pod:** one H200 on a machine with graphics driver 13.2.
  - Your setup was installed exactly as pinned: Torch 2.9.1 with CUDA 13.0, ComfyUI v0.36.0, the full H3 model.
  - The pod's normal startup was kept, only port 8099 was open, there was no secure shell and no Jupyter, and the RunPod key was hidden from commands.
- **Every clip passed the setup's own checks** (size, frame rate, sound, length, full decode, fingerprint) and came back with its fingerprint checked again.

## Times and money

| Step | Time |
|---|---|
| The 123.6 GB of model files downloaded | 5 minutes (about 240 MB a second; 81 minutes last time) |
| All four files checked | 2 minutes (about 500 MB a second) |
| Model loaded on the first run | about 1 minute (18 minutes last time) |
| A 124-frame run | 55 to 91 seconds |
| A 158-frame run | 76 to 86 seconds |
| A 362-frame run (15 seconds) | 261 to 271 seconds; it fits in the graphics card's memory |
| All 15 runs | 40 minutes of rendering |

The pod ran for about 62 minutes in two parts, roughly $5.50 by the hour rate (RunPod's bill lags behind), plus the deleted first pod's $0.53. At the end the pod's own switch-off timer stopped it, 25 seconds after its end time: the money cap works.

## What the takes show

From frames (one or two a second) and from where the sound is loud or quiet. Lines and voices need listening.

1. **Contact cut: confirmed by two takes** (route rules 24 and 26). The cut lands within about 0.1 second of its written time and is clean between two clearly different framings; the result shows in the second shot. The one-line prompt failed in both takes.
2. **The planning picture decides the camera, over the words.** The new "Not mint." prompt says "one continuous close-up". In all four takes H3 copied the start picture's wide framing instead, and in clip 04 it kept Jude where the start picture had him (inside the lift, not at the gate). H3 follows the picture's camera position, shot size and placement over the prompt. This is new, and it is what the Blender blocking test will use.
3. **Calm without stillness words** (supports rule 16). Stage's new prompt, written as small timed actions, gave a calm held moment in four takes. The old prompt, with "stays still", gave big expressions in both takes, and in one an unasked-for cut to a close-up.
4. **The face comes from the picture.** Describing Iona as she looks in her picture changed nothing visible (same seed, same framing, same face).
5. **H3-made start pictures are usable but imprecise:** right place and mood, but the wrong shot size and position. In one there was a blurred extra head, although the brief said she was alone (one take against rule 22).
6. **Lengths:** 124, 158 and 362 frames all work (rule 12). The fixed camera held in every take of the new prompts (rule 19).

## Not yet known

- Whether each line is said once, by the right mouth, and how it sounds (rules 7 and 17). This needs your ears.
- Whether people stay alive between the written actions at full speed.
- Where the picture breaks up near the end of the 15-second clips (rule 10).
- The rule marks in the kit are unchanged until your listening is in; then the takes go in through the take log.

## Next

The blocking test (entry 46): Stage's own grey 3D preview, rendered with Blender on this computer, as H3's planning picture, to control the camera and where people stand. Blender's Python module (5.2.2) now runs here and has rendered the kit's sample plan.
