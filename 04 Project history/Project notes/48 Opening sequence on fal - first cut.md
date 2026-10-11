# 48 Opening sequence on fal - first cut

Log entry 48, 11 October 2026. The first time Stage's prompts were turned into finished film: the opening of The Catch, clips 01 to 03 from your hand-made clip file, made on fal with MiniMax H3 Max and joined into one 31-second cut. The film, the pictures, the prompts and the clips hold story material, so they stay outside git; this note holds what was learned. Lines from scenes 1 to 6 are described, not quoted (the question about quoting them in this public repository is still open).

## One example first

Clip 01's prompt asks for a wide shot of Jude at the elevator gate, then a cut at 4.8 seconds to a close view of the tag in his fingers, where he reads it aloud and a woman answers from the dark.

- **What H3 Max made:** the wide shot, the cut, the close view with the tag's two printed lines spelt right, Jude's line, then the woman's line. Every word right, said once, by a man's voice and then a woman's.
- **But the cut came at 6.2 seconds, 1.4 seconds late,** so everything after it slid later. The woman's line ended at 10.8 seconds, and the clip file's planned trim at 10.1 seconds would have cut her off after her first word. I kept 11.1 seconds of that clip instead.
- **And after Jude lets the tag drop, its print breaks up:** the second line turns into nonsense letters for the last second and a half.

## What was made

Everything ran on fal, through its connection in this session, with your approval of each step (the mode was "Accept edits").

1. **Set-up pictures,** made once and used everywhere after (picture model: Nano Banana Pro):
   - a costume picture of each character (full length, in their clothes for the scene), built from your character pictures;
   - a character sheet of each (front, three-quarter, back and a close face), to check the costume holds from every side;
   - the empty tunnel set (the "master picture").
2. **A start picture per clip,** built from the empty set and the costume pictures, wide (2.4:1).
3. **Three videos** with H3 Max, Reference to Video: 11.5 seconds each, 768P (it came out 1536 by 672), the start picture as the exact first frame, the costume pictures as the character references, prompt expansion switched off, a fixed seed per clip.
4. **The cut:** each clip trimmed to its keep part (11.1, 10.1 and 10.0 seconds), joined in order with a one-second fade in from black. 31.25 seconds, checked to play through without errors.

## Times and money

| Step | Time |
|---|---|
| A picture | 20 to 50 seconds |
| A video (11.5 seconds) | about 11 seconds of making; under 5 minutes from sending to having the file |
| Start pictures, videos and the cut | about 15 minutes |

About $3.40 in all, by fal's listed prices: 11 pictures (about $1.65, including two tries I threw away) and three videos (about $1.73). No rented pod, no setup, no waiting for a graphics card.

## What the takes show

From frames (two a second), from a speech-to-text program run on this computer (so no sound left it), and from the pitch of each voice. Accents need your ears.

1. **The start picture holds the set, the camera and the costumes across clips.** All three clips open on their start pictures exactly, and the tunnel, the gate and both people match between clips. Making costume pictures first, then building every start picture from them, worked: nobody changes clothes, apart from one slip (point 6).
2. **Every line was said once, with the right words and the right voice.** Jude's line at a man's pitch (about 102 vibrations a second); the woman's two lines at about 158 and 168, the same voice in two clips. Clip 02, which has no lines, stayed silent. In the first H3 test (entry 45) H3 invented speech; with Stage's voice lines and the dialogue marks it did not.
3. **The written actions happen, in order.** Clip 02: she walks to the gate, drops to her knees and the close view under the frame shows her finger finding the bolt hole. Clip 03: she says her line, Jude's hands stop on the wire, she looks at the grease on her fingertip, his hand lets the wire hang. This is a calm, small-action clip, which H3 handles.
4. **Cuts can land late.** Clip 02's cut landed on time (4.5 seconds); clip 01's came 1.4 seconds late. The fixed keep seconds then cut a line. Trimming must follow where the speech actually ends, measured on the take.
5. **Printed words on a moving prop break up.** The tag's words were right while it was held still and turned to nonsense once it swung.
6. **One costume slip:** Jude's trousers are dark in clip 01 and light brown in clip 02. Neither the start-picture brief nor his costume picture fixed the trouser colour firmly enough.
7. **Picture briefs: "film set" and "camera" put a film crew in the picture.** The first empty tunnel showed a film crew, because the look block said "a real photograph from a film set". Dropping those words, calling the camera "the viewpoint" and saying "no other people, no equipment, no lamps or stands" fixed it.
8. **Clip 03's first start picture missed the action:** Iona pointed at a hole in the gate post instead of kneeling with her torch under the floor. The second try worked once the brief described the floor frame, the gap under it and her head below it, and added clip 02's start picture as a picture to match.
9. **Two small mismatches the video smoothed over:** clip 02's start picture is square-on, not from the elevator's corner as written, and Iona stands instead of coming round the elevator mid-stride. The video simply moved on from the picture, as H3 does.

## Not yet known

- How the voices sound: accent, clarity and acting. This needs your ears.
- Whether a second take of each clip would be better or worse (one take each so far).
- Whether 1080P is worth its higher price for this look.

## What it changes in Stage

Added to note 41, section 13 (items 78 to 82): trim by the measured end of speech, keep printed words still, fix every costume colour in the costume picture and in each brief, no "film set" or "camera" in picture briefs, and describe the geometry of close actions in start-picture briefs.

## Next

Your verdict on the cut. If it holds up, the same steps carry on to clips 04 onward, with two takes per clip and the trims set by the measured speech.
