# Word list

One plain word for each thing. Write "turn shot", never "key shot"; in a record that is `- role: turn`. Use the middle column in every record, card, step file and message, and never the retired words in the last column. Where the AI's word and the user's word differ, the user's word is the only one allowed above a file's divider and in messages ("group 3", never "SQ03"). The same list, as data the checker reads, is `_config/rules/words.json`; the user's plainer version is `06 Word list.md`.

## The words and the fields they map to

| Thing | The one word, and its field | Retired |
|---|---|---|
| Story state of a person or thing in a mirror story | **reversed** / **original** (`STATE.handedness`); never "turned", which belongs to value turns | phase, frame reversed, turned (as a mirror state), handedness_phase, mirror true |
| A stretch of the film under one frame handedness | **era** a, b, c (`RULE.era`) | phase |
| How an element appears in a shot | **mirrored** / **normal** (`mirror_state`, code) | MIRRORED, mirror_state capitals |
| The edit operation | **flip** (`SHOT.flip`, `FINISH.operation`) | mirror_flip |
| The fixed words pasted into every prompt | **fixed description** (`CHARACTER.fixed_description`, `PROP.fixed_description`) | identity key, look line |
| Costume, injury and condition at a point | **state** ("Iona, state 2", STATE records) and its **state line** (`STATE.state_line`) | look ID, costume phase C1-C6, states S1-S6 |
| Light, colour and texture of a place at a time | **look** (LOOK, `SCENE.look`); its pasted text is the **look block** (`LOOK.look_block`); "look" means nothing else | look key, lighting block, global look key |
| How the film appears / how a character appears | **style** with its **style words** (`STYLE.style_words`) / **appearance** | look (for either), style key, "the film's look", "her look" |
| The main light | **main light** (`LOOK.main_light`) | key light |
| The shot where a scene turns | **turn shot** (`SHOT.role: turn`) | key shot |
| The frame a turn must show, written before shots | **turn picture** (`SCENE.turn_picture`) | key frame (as a written frame) |
| Stills a video starts or ends on | **start picture**, **end picture**, **pinned picture** (`PIC.use`) | keyframe, first frame, start frame |
| A grey still that fixes composition | **layout picture** (`PIC.use: layout`) | structure image, layout guide |
| A grey 3D video a model copies | **guide video**, made from a **grey render** (`PREVIS.route`) | control video, clay render, greybox, motion guide |
| Reference pictures of one element state | **reference pictures**; one film-look still: **style picture** (`PIC.use`, `STYLE.style_picture`) | reference pack, asset sheet, stack, model sheet, style frame |
| McKee's action and reaction | **beat** (BEAT) | bit |
| A timed visible change inside a shot | **moment** (`SHOT.moment`) | BEATS (in prompts), timeline events, C4 beats |
| "(beat)" in a script | **pause** (`BEAT.pause_after`) | beat |
| A part of a scene with its own turn | **part** (PART) | movement |
| One reply's share of a scene's shots | **batch** (`PROJECT.batch_size`) | part (for replies) |
| A group of scenes | AI: **sequence** (SEQUENCE, `SCENE.sequence`); user: **group of scenes** ("group 3") | stretch, colour-script sequence, journey unit |
| Camera movement / a character's move on the floor plan / Block's motion component | **camera move** (`SHOT.move`) / **floor-plan move** (MOVE) / **motion** (`VISUAL.component`) | movement, "move" alone in user text |
| Whose point of view a scene holds / a shot through someone's eyes | **whose scene** (`SCENE.whose_scene`) / **point-of-view shot** (`SHOT.frame: pov`) | POV for both |
| What a character wants in a scene / in life | **want** (`SCENE.want`) / **life want** (`CHARACTER.life_want`) | objective, intention, super-intention, spine, scene desire |
| What a line or act does to the other person | **tactic**, an -ing word (`tactic` sub-parts of BEAT and SHOT) | action gerund, playable action, infinitives |
| What the hands do | **task** (`BEAT.task`) | activity, physical task |
| What we see the body do | **does** (`SHOT.subject` sub-part) | emotion words, behaviour as a plan field |
| How openly a body shows a feeling | **display** 1-3 (`SHOT.subject` sub-part); the old sub-part **still** is no longer written or sent to a model | performance scale, intensity (for display) |
| A held moment, filled | **held moment** (a moment of `hold_action_every_s` or more, or a pause held on picture) filled with **small timed actions**: a breath, a blink, a swallow, a glance, a hand that adjusts something | stillness, "stays still", a list of still parts |
| Words that ask a model to freeze | **stillness words** (`_config/rules/words.json`); never in a record a model reads | none |
| Which way a subject crosses the frame | **travel** (`SHOT.subject`, `SEQUENCE.travel`) | screen direction (as a field name) |
| A moment in a scene named before its beats exist | **story point** (kind story_point) | beat reference (before step 7) |
| The feeling a film or scene is played in | **tone**: **home tone** (`PLAN.tone_home`), a scene's **tone**, **undercurrent**, **tone shift** (`SCENE` fields) | mood (as a field), genre (for tone) |
| The record of changing states | **continuity** (`09 Continuity.md`, STATE) | continuity bible, ledger, state table, damage ledger |
| A thing that returns and gathers meaning | **motif** (MOTIF) with **plant**, **payoff** (PLANT, `SHOT.thing` sub-parts) and **rhyme** (`PLANT.rhyme`) | carrier log, thread, emblem, hinge, reserved framing |
| A choice saved for special moments | **saved choice** (RESERVE, RC IDs) | reserved choice, reserved framing |
| Kept out of frame for later | **keep hidden** (`SHOT.keep_hidden`) | withhold, withheld |
| Readable words inside the picture | **text in picture** (TEXT, `SHOT.text`); the drawn file is the **text graphic** | on-screen text, insert graphic, text spec |
| A character's voice / a place's steady background | **voice** with its **voice description** (VOICE) / **room sound** (`room_sound` fields) | sound key, voice key, room tone key, bed, ambience |
| How a voice reaches us | **path** (`SPEECH.path`, `hear` path, `VOICE.path_sound`) | channel, voice_source, perspective |
| Where the camera stands in a scene | **setup**, "camera A" to the user (SETUP, `SHOT.setup`) | camera position S1-S8 |
| Left and right | **frame-left**, **frame-right** (`frame_left` values); **own left**, **own right** (`side` items); **hand nearest the camera** | screen left, image-left, camera left |
| The imaginary line between two people | **the line**, line of action (`SETUP.side`) | axis, 180° line |
| Shot sizes | **extreme wide, wide, medium wide, medium, medium close-up, close-up, extreme close-up, insert** (`SHOT.size`) | big close-up, EWS, WS, MCU, CU, ECU, OTS and every abbreviation |
| Tilt / eye height | **angle** / **height** (`SHOT.angle`, `SHOT.height`) | angle_height |
| Where a fact comes from | **origin**: story, inferred, invented (`origin` fields) | fact, extracted, authored, added, [design choice] |
| Who may write a field | **writer**: story, ai, user, code_state, code_derived (schema) | extracted, authored, derived, human |
| Used length / length to generate | **screen time** (`SHOT.screen_time`) / **clip length** (code) | duration_s, clip_s |
| Why a shot exists | **purpose** (`SHOT.purpose`) | PURPOSE, purpose (as picture job kind) |
| The kind of picture job | **use** (`PIC.use`) | purpose |
| A departure's reason | the record's **why** (`why` fields) | override:, WHY slot, story_reason |
| How loud a thing is / a sound is | **emphasis** 0-3 / **sound emphasis** 0-3 (`thing`, `effect`, `BEAT.emphasis`) | L0-L3, S0-S3, emphasis device |
| An extra signal on a beat | **added emphasis**, 0 or 1 (`BEAT.added_emphasis`) | emphasis device, added signal |
| Pressure inside a scene / across the film | **beat intensity** 1-5 / **scene intensity** 1-10 | intensity, story intensity |
| Whole-film facts | the **whole-film files** (05-10) and their **whole-film summary** (file 02) | bible, visual bible, asset bible, register, core facts |
| A question to the user with a default | **choice**; one grouped without asking: **small choice** (CHOICE, `CHOICE.asked: no`) | decision card, question record, small call, decision (for a choice), question (for a choice) |
| A place where the user answers | AI: **checkpoint** A, P, B, C, D, E (`CHOICE.checkpoint`); user: named by what it is | checkpoint letters in user text |
| How deep the breakdown goes | **quick**, **standard**, **detailed** (`PROJECT.depth`, `SCENE.depth`) | full (as a depth) |
| A problem found, with its fix | **finding** (FINDING) | issue |
| One step of the pipeline | **step**, counted from 1 for the user ("step 8 of 12") | stage (except "Stage", capitalised, the product's name, and `stage.py`) |
| A piece of AI work that fits one reply | **unit** (`steps.json` units) | task, call |
| The file the AI reads for a unit | **handout** on code surfaces; the attached **step file** and **whole-film summary** in chat | context pack |
| Grey 3D stand-in renders of shots | AI: **previs** (PREVIS, `SHOT.previs_level`); user: **grey previews** | clay preview, greybox (for the user) |
| Runtime and cost estimates | AI: v0, v1 (D13); user: **the first estimate**, **the estimate from the shots** | v0, v1 in user text |
| Where a take is kept or rejected | **take** (TAKE) | generation job |
| A video model plus the place it runs | **route** (`PROJECT.video_route`; route entries in `_config/adapters/video_models.json`), such as "MiniMax H3 in ComfyUI, Reference to Video" | platform, pipeline (for a route) |
| One run of a video model | **clip**: on a route, one to three shots of one scene or one part of a long shot (`SC10-CL01`); elsewhere a piece of one shot (`SC10-SH150.1`) | generation, job |
| All of a route's clip pages, with its settings, pictures, shot map and take log | **clip book** (`20 Prompts for AI video/MiniMax H3 in ComfyUI/`) | prompt file (for a route) |
| The end of a clip made to be thrown away / where the kept part ends | **tail** / **keep point** | handle (for the tail), buffer |
| The number typed into the template's Duration box | **seconds to type** | duration |
| Ending a shot as one thing reaches another, the next shot opening on the result | **contact cut** | impact shot |
| An empty picture of a place, made once, that start pictures are built from | **master picture** (M1, M2 ...) | plate (for this), set still |
| The paragraph pasted first in every picture prompt on a route | **picture style block**; never "look block", which is a place's light and colour words | look block (for this) |
| The line giving each person in a clip breathing, eye movements, weight shifts and blink times | **"alive" sentence** | none |
| Which clip holds each shot, and its seconds | **shot map** | edit list |
| A run's seed, settings, result and verdict, and what it showed about a route's rules | **take log** (TAKE records with `rule` lines); each rule's **mark**: verified, confirmed, wrong or unclear | none |
| A question the checker asks when a body is asked to do something impossible | **physical sense check** (PHYS) | none |
| The flashlight in prompts | **flashlight** (`PROJECT.prompt_words`); "torch" only inside quotes of the script | torch in prompts |
| Model names | the exact name in `video_models.json`, with aliases ("Kling O3" = kling-3.0-omni) | informal names |

## What the user reads instead

Only the user's words go above a file's divider, into reports and into messages:

| The AI's word | The user's word |
|---|---|
| sequence, SQ03 | group of scenes, "group 3" |
| checkpoint A, P, B, C | the scene list; how the book becomes a film; the big choices; each group of shots |
| acceptance, checkpoint D, checkpoint E | the finished check; the grey previews; keeping takes |
| previs | grey previews |
| v0, v1 | the first estimate, the estimate from the shots |
| step 7 (counted from 0) | step 8 of 12 (counted from 1) |
| SC10-SH150 | shot 150 (scene 10) |

## Where the checker looks

WORDS-02 warns on a retired word in a field value or in user-facing text, read in its retired sense ("camera movement", "a sound bed"; "his movement" is plain English). Each entry in `_config/rules/words.json` says where: everywhere, only in user text, only in named fields, only as a field name (FORM-03), only in prompts (GEN-12), or nowhere (`emblem` as a PROP kind, `spine` as a MOTIF rank).

Always allowed: "Stage" as the product's name and `stage.py`; story words inside double quotes (a script's "torch" stays); the field names `CHARACTER.movement` (label "How they move") and `SETUP.look_at` (label "Aimed at"); research codes in AI-facing files. Mood-only reasons, emotion words and banned prompt words have their own lists (REASON-04, WORDS-01, GEN-12).
