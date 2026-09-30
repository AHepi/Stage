# Field guide

Every record type and every field of `schema/schema.json`, in plain words. This file is made by `stage.py build-kit` from the schema (version 1.0); edit the schema, never this file. Record grammar: `reference/01 Record format.md`. Words: `reference/02 Word list.md`.

Example first. The SHOT field `size` reads, in the table for SHOT:

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `size` | Shot size. | extreme_wide, wide, medium_wide, medium, medium_close_up, close_up, extreme_close_up, insert | quick | ai | step 8 | `close_up` |

So a shot record carries the line `- size: close_up`: the AI writes it at step 8 (the user's step 9 of 12), from quick depth, choosing one of the eight sizes.

## How to read the tables

- **Depth**: quick (q): Required from quick depth (and at standard and detailed); standard (s): Required from standard depth (and at detailed); detailed (f): Required only at detailed depth (the user's word is detailed; 'f' is the stored letter); add-on (m): Required only when its module (add-on) is on; `module` names it; optional (o): Optional at every depth.
- **Writer**: `story`: Code, copying from the numbered story. Never typed by the AI (FORM-10); `ai`: The AI. Within the allowed values; references must exist; a departure from a default needs a why; `user`: Only through a CHOICE whose status is answered or defaulted; the field locks when set. An AI-written value without such a CHOICE is FORM-10; `code_state`: Code, stored in the record file (locks, status, resolved story points, counts). The AI may not change it (FORM-10), except a field with chat_writer ai in a project marked code_execution: no; `code_derived`: stage.py build only. Computed on every build and never stored in record files; an AI-typed value is dropped with a warning (FORM-10, W). FORM-05 never asks for these fields.
- **Filled at**: the step that fills the field, counted from 0 as in the step files (step 8 is the user's step 9 of 12); a letter is a checkpoint; add-ons come after step 11.
- **Values**: the kind first when it is not a single word, then the allowed values, the sub-parts (`key: kind (values)`), other values allowed, the default, and "one line each" for a field written once per item. Syntax of every kind is in the table below.

## Kinds of value

| Kind | Syntax | Example |
|---|---|---|
| `text` | Any words to the end of the line. The three characters space, bar, space ( \| ) are not allowed inside, because they separate sub-parts. | `Iona's body admits what her words denied.` |
| `word` | One allowed value in lowercase snake_case. Compared ignoring case; spaces and hyphens are read as underscores, so 'medium close-up' is medium_close_up. The field's `values` list the allowed words; a field of kind word without a list takes any one lowercase word. | `medium_close_up` |
| `word_list` | Allowed words separated by commas. | `tense, enigmatic, dread, grave` |
| `number` | A number written with digits and an optional decimal point, with no unit letters (units live in the field name). A field with `range` takes only values inside it; `whole: true` means no decimal point. | `2.5` |
| `seconds` | A number of seconds (field names end in _s, or the meaning says seconds). | `15` |
| `metres` | A number of metres (field names end in _m). | `1.72` |
| `millimetres` | A number of millimetres of lens focal length on a full-frame camera (field names end in _mm). | `50` |
| `dollars` | A number of US dollars (field names end in _usd). | `12.40` |
| `words_per_second` | A number of spoken words per second (field names end in _wps). | `2.0` |
| `number_list` | Numbers separated by commas. | `25, 35, 50, 85` |
| `yes_no` | yes or no. | `yes` |
| `id` | One ID whose record type is listed in `id_types` (patterns in section 5.3 and in each record type's id_pattern). | `CH-IONA` |
| `id_list` | IDs separated by commas. A comma inside double quotes does not split the list. | `SC10-B07, SC10-V1, MO-MINT, CR-IONA` |
| `id_range` | A first and last ID joined by two full stops (SC01..SC05), or one ID, or IDs separated by commas. The same form the compile command takes. | `SC01..SC05` |
| `lines` | Line numbers of the numbered story, single or as ranges, separated by commas (402, 449-463); or a quote anchor: one quoted string for one line ("Her eyes open."), or a pair joined by 'to' for a range ("Iona chews it." to "street signs either."). Each quoted string has at least 3 words and must match exactly once in its scope (CITE-02). In chat without a numbered story, anchors are required; stage.py adopt turns them into numbers. | `454-466` |
| `quote` | One double-quoted string of exact story words, found in the story (G12, CITE-03). | `"Kitchen."` |
| `story_point` | A moment inside a scene named before its beats exist: the scene ID, a space and a quote anchor (SC24 "She deletes the way home."). From step 7 a beat ID is also accepted. When code resolves a story point at step 7 it appends ' = ' and the beat ID (SC24 "She deletes the way home." = SC24-B05); that ending is code_state, never typed or changed by the AI. | `SC24 "She deletes the way home."` |
| `story_point_list` | Story points separated by commas (commas inside quotes do not split). | `SC10 "Her face changes.", SC13 "You did that."` |
| `charge` | A value's charge: ---, --, -, 0, +, ++ or +++. The sign is the direction; the count is the strength. | `---` |
| `point` | [x, y] or [x, y, z] in metres, in set-plan coordinates (5.4 rule 7). | `[2.8, 2.55]` |
| `size` | [w, d, h]: width, depth and height of a box in metres. | `[6.0, 3.6, 2.5]` |
| `span` | t0-t1: a stretch of time inside a shot, in seconds from the shot's start. | `0-4` |
| `date` | A date written year-month-day. | `2026-10-02` |
| `file` | A file name or a path inside the project folder, as plain text. | `18 Storyboard/Scene 10 - shot 150 - frame 01.png` |
| `text_list` | Names or short phrases separated by commas. | `IONA, IO` |
| `sub_parts` | An item (G6): a first part (the item's main value, usually an ID) followed by named sub-parts, each ' \| key: value'. Sub-part keys come from the field's `sub_parts` list, in any order. A field whose `first_part` is null has no first part: its value starts with its first named sub-part. Positional (unnamed) sub-parts are never allowed. | `CH-IONA.S02 \| at: left_third \| faces: camera \| does: chews, stops, frowns` |
| `because_list` | Items separated by commas: the ID of any story record (a scene, value, part, beat, speech, move, setup, sequence, plan, plant, fact, chapter, character, voice, place, thing, text, motif, in-story camera, state, world, style, rule, camera system, camera rule, saved choice, lens exception, look, visual plan, sound plan or ladder: the kind's id_types), line:NNN, or line: "<quote anchor>"; or the single word default, allowed only on a normal shot where REASON-02 finds no departure. The same set in every record (fix list C14). A comma inside double quotes does not split the list. | `SC10-B07, SC10-V1, MO-MINT, PR-FLASK, LOC-SAYE-KITCHEN, CR-IONA, line:456` |
| `reference_list` | IDs and field paths separated by commas. A field path is <ID>.<field> (SC10-SU01.lens_mm); a singleton record and the project are named by their type (PLAN.crisis, PROJECT.frame_shape). | `PROJECT.frame_shape, WR-MIRROR, SC10-SU01.lens_mm` |
| `scene_or_story_point` | A scene ID alone for the whole scene (SC26), or a story point (SC26 "She pushes gently away from the rail."); from step 7 a beat ID is also accepted, and code resolves a story point as for the kind story_point. A field's id_types may add other IDs (MOTIF appearance also takes a shot ID from step 8). | `SC26` |
| `element_list` | IDs of the record types in id_types, separated by commas; until step 4 designs the things, a story point (SC10 "the flask") may stand for an element that has no record yet. From step 5 on every item must be an ID. | `PR-RING, MO-MINT` |

## Fields every record takes

Every record type also takes these three fields (5.5). A record type that lists its own status field (CHOICE, FINDING) uses its own list; status_values on each record type gives the allowed statuses.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `status` | Where the record stands: draft, approved, stale (an input changed) or omitted (cut, keeps its ID). | draft, approved, stale, omitted | quick | code_state; in a chat without code: ai | step 0 | `approved` |
| `locked` | Set when the user approves the record; a locked record gains fields but never silently changes (5.4 rule 5). | yes_no | quick | code_state; in a chat without code: ai | step 0 | `yes` |
| `note` | A free note on the record, for people. | text; one line each | optional | ai | step 0 | `Staging assumed: the story does not say where Eli stands.` |

## PROJECT: the project

One per project: the story, the app, the depth, the rights and the big settings. ID: 3 to 8 capital letters (`CATCH`); the user sees it as the title. Lives in: 00 Start here.md. Designed at step 0; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `title` | The story's title, from the first title-page line or title heading; the AI may propose a clean title as a small choice. | text | quick | story; in a chat without code: ai | step 1 | `The Catch` |
| `source_file` | The original file name of the story. | text | quick | code_state; in a chat without code: ai | step 0 | `The Catch - workshop revision.txt` |
| `source_fingerprint` | SHA-256 fingerprint of the original story file, proving it has not changed. | text | quick | code_state; in a chat without code: ai | step 0 | `3f5a9c0e1b7d4a2e9f6c8b1a0d3e5f7a9c2b4d6e8f0a1c3e5b7d9f1a3c5e7b9d1f` |
| `source_kind` | What kind of story it is (code detects it; the AI confirms at the odd-lines report). | screenplay, prose, stage_play, treatment, comic_script, game_script, mixed | quick | code_state; in a chat without code: ai | step 1 | `screenplay` |
| `source_format` | The file format found. | catch_dialect, fountain, fdx, docx, epub, pdf_text, markdown, plain_text | quick | code_state; in a chat without code: ai | step 1 | `catch_dialect` |
| `language` | The story's language. | word | quick | code_state; in a chat without code: ai | step 1 | `english` |
| `depth` | How deep the breakdown goes (CHOICE-002, stated at step 0, default standard). | quick, standard, detailed | quick | user | step 0 | `standard` |
| `surface` | The app the pipeline runs in (set by the self-test). | claude_code, claude_cowork, claude_web, chatgpt, gemini, other | quick | code_state; in a chat without code: ai | step 0 | `claude_code` |
| `code_execution` | Whether Python runs in this app (set by the self-test). | yes_no | quick | code_state; in a chat without code: ai | step 0 | `yes` |
| `batch_size` | Most shots written in one reply at step 8: 12, or 18 once the self-test passes (constant batch_size). | number; 12, 18 | quick | code_state; in a chat without code: ai | step 0 | `18` |
| `training_off` | Whether the user confirmed the app's privacy setting (training on your chats) is off (CHOICE-003). | confirmed, not_confirmed | quick | user | step 0 | `not_confirmed` |
| `rights` | The right to adapt the story (CHOICE-001). study_only marks every export 'Private study, not for publication'. | mine, permission, public_domain, study_only, unknown | quick | user | step 0 | `mine` |
| `intended_use` | Where the finished film goes. | personal, festival, online_free, online_monetised, commercial | add-on (C) | user | add-on C (prompts for AI video) | `festival` |
| `licensed_data_only` | Route only to models the adapter marks licensed_data (8.4). | yes_no; default no | add-on (C) | user | add-on C (prompts for AI video) | `no` |
| `format` | The kind of finished work (CHOICE-004, asked: no; short under 40 minutes by the first estimate, feature otherwise). | short, feature, limited_series | quick | user | step 1 | `short` |
| `runtime_target_s` | Target length with credits, in seconds, or as_written. | seconds; also as_written | quick | user | checkpoint A | `as_written` |
| `scope` | The scenes the scene work, checks, film pass, estimates and exports cover; all by default (for prose, the scenes of chapter I). | id_list; IDs of SCENE; also all | quick | user | checkpoint P | `all` |
| `frame_shape` | The delivery frame shape (aspect ratio), chosen once at checkpoint B (default 2.39). | 2.39, 1.85, 16_9, 4_3, 9_16 | quick | user | checkpoint B | `2.39` |
| `fps` | Frames per second of the finished film. | number; 24, 25, 30 | quick | ai | step 6 | `24` |
| `genre` | The named genre, copied from PLAN by code. | word | quick | code_state; in a chat without code: ai | step 2 | `thriller` |
| `tone_home` | The film's home tone (D10 §2.1), copied from PLAN. | grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative | quick | code_state; in a chat without code: ai | step 2 | `tense` |
| `tone_range` | The tones allowed anywhere in the film, copied from PLAN. | word_list; grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative | quick | code_state; in a chat without code: ai | step 2 | `tense, enigmatic, dread, grave` |
| `scene_id_digits` | Width of scene numbers: 3 when the project has more than 99 scenes (fixed per project). | number; 2, 3 | quick | code_state; in a chat without code: ai | step 1 | `2` |
| `prompt_words` | Word swaps applied in compiled prompts (K19); script quotes keep the story's word. | sub_parts; first part: text; use: text; one line each | standard | ai | step 3 | `torch \| use: flashlight` |
| `previs_colours` | The flat colour of each character's grey stand-in, assigned once. | sub_parts; first part: id (CHARACTER); rgb: point; one line each | add-on (B) | code_state | add-on B (grey previews) | `CH-IONA \| rgb: [0.80, 0.35, 0.30]` |
| `spend_cap_usd` | Most that any batch may spend; nothing is spent until it is set (8.8). | dollars; also none | add-on (C) | user | add-on C (prompts for AI video) | `50` |
| `hours_per_week` | Hours the user can give each week, for the schedule. | number; also none | add-on (C) | user | add-on C (prompts for AI video) | `6` |
| `schema_version` | The schema version the records were written against. | text | quick | code_state; in a chat without code: ai | step 0 | `1.0` |
| `checker_last_run` | When the checker last ran on this project, or never. | text | quick | code_state; in a chat without code: ai | step 0 | `never` |
| `model_facts_date` | The date of the model facts the estimate and packs used (adapters checked_on). | date; also none | quick | code_state; in a chat without code: ai | step 10 | `2026-09-27` |

Status values: draft, approved, stale, omitted.

## CHOICE: choice

A question for the user with a default; a small choice (asked: no) is grouped under 'small choices I made'. ID: CHOICE- and 3 digits (`CHOICE-021`); the user sees it as choice 21. Lives in: 01 Choices.md. Designed at step 0; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `question` | The question in plain words. | text | quick | ai | step 0 | `Is this story yours, or do you have permission to adapt it?` |
| `why` | Why it matters, one line. | text | quick | ai | step 0 | `Exports and generation packs depend on the rights.` |
| `option` | One possible answer, lettered a, b, c. | sub_parts; first part: word; text: text; one line each | quick | ai | step 0 | `a \| text: It's mine` |
| `default` | The answer used if the user says 'defaults', and its reason. | sub_parts; first part: word; reason: text | quick | ai | step 0 | `a \| reason: most users adapt their own work` |
| `answer` | The user's answer: an option letter or their own words. | text | quick | user | step 0 | `a` |
| `asked` | yes: shown as its own question; no: a small choice, grouped under 'small choices I made' and defaulted when made. | yes_no | quick | ai | step 0 | `yes` |
| `checkpoint` | Where the choice is shown. | a, p, b, c, acceptance, d, e, none | quick | ai | step 0 | `b` |
| `affects` | IDs or field paths the answer changes (used to mark the three choices that matter most at B). | reference_list; IDs of * | quick | ai | step 0 | `PROJECT.frame_shape, SC10-SU01.lens_mm` |
| `sets` | What each option writes: a single word or number as <ID>.<field> \| value: ... \| when: a; a structured value as <SETVALUE id> \| when: a. | sub_parts; first part: text; value: text; when: word; one line each | quick | ai | step 0 | `PROJECT.frame_shape \| value: 2.39 \| when: a` |
| `locks` | Records locked when the choice is answered. | id_list; IDs of * | optional | ai | step 0 | `WR-MIRROR` |
| `based_on` | Research references behind the choice. | text | standard | ai | step 0 | `K22; B3 Ex1` |
| `status` | open, answered or defaulted. | open, answered, defaulted | quick | code_state; in a chat without code: ai | step 0 | `defaulted` |
| `date` | When it was answered or defaulted (an open choice has none). | date; also none | quick | code_state; in a chat without code: ai | step 0 | `2026-10-02` |

Status values: open, answered, defaulted.

## SETVALUE: set value

The full value one option of a CHOICE writes, for answers a sets line cannot hold; code copies its field lines into the target and locks them when that option is chosen. ID: the choice ID, a hyphen and the option letter in capitals (`CHOICE-014-A`); the user sees it as not shown (its choice is). Lives in: 01 Choices.md. Designed at step 0; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `target` | The record the lines are copied into; every other field line is checked against the target's record type. | id; IDs of * | quick | ai | step 0 | `WR-MIRROR` |

Status values: draft, approved, stale, omitted.

## SCENE: scene

One scene: its list and plan fields live in 04 Scene list.md, its design fields in its scene file; the copies merge by ID (G10). ID: SC and 2 digits (3 when the project has more than 99 scenes; fixed per project), plus an optional capital letter for an inserted scene (`SC10`); the user sees it as Scene 10. Lives in: 04 Scene list.md, 11 Scenes/Scene NN - <place>.md. Designed at step 7; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `heading` | The scene heading as the story writes it (prose: written by the AI for the step outline). | text | quick | story (when source_is_screenplay); ai (when source_not_screenplay); in a chat without code: ai | step 1 | `INT. SAYE'S HOUSE - KITCHEN - BEFORE DAWN` |
| `int_ext` | Inside, outside, or both. | int, ext, int_ext | quick | story (when source_is_screenplay); ai (when source_not_screenplay); in a chat without code: ai | step 1 | `int` |
| `place_text` | The place as the heading names it. | text | quick | story (when source_is_screenplay); ai (when source_not_screenplay); in a chat without code: ai | step 1 | `SAYE'S HOUSE - KITCHEN` |
| `time_text` | The time as the heading names it. | text | quick | story (when source_is_screenplay); ai (when source_not_screenplay); in a chat without code: ai | step 1 | `BEFORE DAWN` |
| `lines` | The scene's line range in the numbered story (in chat, a quote anchor pair). | lines | quick | story (when source_is_screenplay); code_state (when source_not_screenplay); in a chat without code: ai | step 1 | `397-489` |
| `characters` | Who is present in the scene. | id_list; IDs of CHARACTER | quick | code_state; in a chat without code: ai | step 1 | `CH-SAYE, CH-IONA, CH-JUDE, CH-ELI` |
| `speaking` | Cue counts: how many times each character speaks. | sub_parts; first part: id (CHARACTER); cues: number; one line each | quick | code_state; in a chat without code: ai | step 1 | `CH-SAYE \| cues: 10` |
| `transition_in` | The join into the scene as the story writes it; a plain cut otherwise. | cut, cut_to_black, fade_in, fade_out, dissolve, smash_cut, match_cut, continuous | quick | story; in a chat without code: ai | step 1 | `cut` |
| `transition_out` | The join out of the scene as the story writes it; a plain cut otherwise. | cut, cut_to_black, fade_in, fade_out, dissolve, smash_cut, match_cut, continuous | quick | story; in a chat without code: ai | step 1 | `cut_to_black` |
| `presentation` | How the scene is shown. | normal, on_screen, recording, flashback, dream, montage, letter | quick | ai | step 1 | `normal` |
| `host` | The device showing the scene when it is on a screen or a recording; written at step 4 by the unit that designs the in-story cameras (fix list C21). | id; IDs of PROP, CAMERA; also none | quick | ai | step 4 | `PR-TABLET` |
| `event` | What changes in the scene, one past-tense sentence with no psychology. | text | quick | ai | step 2 | `Saye proved to Iona with a mint leaf that the three of them had turned and the world had not, and kept them all in her kitchen.` |
| `sequence` | The group of scenes it belongs to. | id; IDs of SEQUENCE | quick | ai | step 2 | `SQ03` |
| `scene_intensity` | Pressure across the whole film, 1 to 10; exactly one 10 (or one 10 range) on the climax. | number; from 1 to 10 | quick | ai | step 2 | `7` |
| `whose_scene` | Whose point of view the scene holds. | id; IDs of CHARACTER | standard | ai | step 2 | `CH-IONA` |
| `story_day` | Which day or night of the story (D1, N1 ...). | text; pattern `^[DN]\d+$` | standard | ai | step 2 | `N2` |
| `rhythm_class` | The scene's pace class, used only by the estimate, never as a design target. | action_peak, suspense, mixed, dialogue, contemplative | standard | ai | step 2 | `dialogue` |
| `tone` | The scene's main tone (D10 §2.1). | grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative | standard | ai | step 2 | `tense` |
| `tone_undercurrent` | An optional second tone carried by lines and acting, never by the camera (D10 TN1). | grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative, none | standard | ai | step 2 | `comic_dark` |
| `tags` | Situations that load situation cards. | word_list; dialogue_duel, three_or_more, action, glass_and_reflection, handedness, screens_and_text, in_story_footage, suspense_and_reveal, darkness, prose_interior, montage_and_time, creature, violence; also none | quick | ai | step 2 | `glass_and_reflection, handedness` |
| `depth` | A depth for this scene above the project's ('Go deeper on scene 13'), logged as a CHOICE. | quick, standard, detailed, none | optional | user | step 7 | `detailed` |
| `target_duration_s` | Planned seconds: the first estimate, then the plan. | seconds | standard | code_state; in a chat without code: ai | step 2 | `96` |
| `keep` | Compression decision for the scene. | keep, trim, merge, fold, cut | standard | ai | step 2 | `keep` |
| `merged_into` | Where a merged or folded scene went. | id; IDs of SCENE; also none | standard | ai | step 2 | `SC05` |
| `from_lines` | Prose: the source passage the scene is drawn from. | lines | quick | ai | step 2 | `112-160` |
| `five_test` | Prose: A3's five tests as five digits 0 or 1. | text; pattern `^[01] [01] [01] [01] [01]$` | quick | ai | step 2 | `1 1 0 1 1` |
| `cardinal` | Prose: cardinal events the scene carries. | id_list; IDs of CARDINAL; also none | quick | ai | step 2 | `CF-02` |
| `strands` | Prose: strands the scene carries. | id_list; IDs of STRAND; also none | quick | ai | step 2 | `ST-01, ST-03` |
| `origin` | Whether the scene is in the story, inferred from it, or invented (authoring mode). | story, inferred, invented | quick | ai | step 1 | `story` |
| `location` | The place. | id; IDs of LOCATION | quick | ai | step 7 | `LOC-SAYE-KITCHEN` |
| `sub_area` | The part of the place used. | text | detailed | ai | step 7 | `the table end by the window` |
| `look` | The place-and-time look. | id; IDs of LOOK | standard | ai | step 7 | `LK-SAYE-KITCHEN-NIGHT` |
| `value` | A value the scene turns; the first part declares the value ID. | sub_parts; first part: id (VALUE); name: text; core: yes_no; open: charge; close: charge; turns_at: id; kind: word (action, revelation, none); one line each | quick | ai | step 7 | `SC10-V1 \| name: normal or altered \| core: yes \| open: + \| close: --- \| turns_at: SC10-B07 \| kind: revelation` |
| `want` | What each character wants here, and what they hide or hold back. | sub_parts; first part: id (CHARACTER); want: text; hidden: text; holds_back: text; one line each | standard | ai | step 7 | `CH-SAYE \| want: to prove the world is mirrored \| hidden: she has waited years \| holds_back: her own fear` |
| `driver` | Who drives the scene. | id; IDs of CHARACTER | standard | ai | step 7 | `CH-SAYE` |
| `conflict` | The kind of conflict (A2). | balanced, asymmetric, indirect, comic, minimal, reflexive | standard | ai | step 7 | `asymmetric` |
| `third_thing` | What the characters fight through. | text | standard | ai | step 7 | `the mint leaf` |
| `staging` | One line placing everyone, with 2 to 4 named stations in a scene over 8 beats; 'staging assumed' when the story is silent. | text | standard | ai | step 7 | `Saye at the stove end, Iona across the table at her mark, Eli deep by the back door; stations: door, table, stove.` |
| `start` | Where each character stands at the scene's start. | sub_parts; first part: id (CHARACTER); at: text; faces: text; posture: word (standing, seated, lying, kneeling); one line each | standard | ai | step 7 | `CH-IONA \| at: IONA_MARK \| faces: CH-SAYE \| posture: standing` |
| `scene_idea` | The scene in one sentence as a director sees it, naming the at most two departments that change at the main turn. | text | standard | ai | step 7 | `A kitchen that is almost right; at the turn only the camera (the scene's closest frame) and the sound (room sound only) change.` |
| `department_idea` | One idea for each department; holding the baseline is a full answer. | sub_parts; first part: word (camera, light, staging, sound, design); idea: text; holds_baseline: yes_no; because: because_list; one line each | standard | ai | step 7 | `light \| idea: Iona's lamp is the only warm source; it goes down on the table before the hands \| because: LK-SAYE-KITCHEN-NIGHT` |
| `turn_picture` | The frame each turn must show, written as one sentence before any shot. | sub_parts; first part: id (BEAT); picture: text; one line each | quick | ai | step 7 | `SC10-B07 \| picture: Iona close, eyes on Saye just off the lens, her mouth stopped mid-chew` |
| `dial` | Per beat, how close and how loud: planned size, distance and height, drawn toward the turn. | sub_parts; first part: id (BEAT); size: word (extreme_wide, wide, medium_wide, medium, medium_close_up, close_up, extreme_close_up, insert); distance_m: metres; height: text; light: text; sound: text; one line each | standard | ai | step 7 | `SC10-B07 \| size: close_up \| distance_m: 1.2 \| height: eye:CH-IONA \| light: as_look \| sound: room_sound` |
| `coverage` | How the scene is covered. | designed, chained, master_and_coverage, oner | standard | ai | step 7 | `designed` |
| `rhythm_shape` | The shape of the cutting. | build_and_cut_out, build_rupture_aftermath, slow_burn, steady | standard | ai | step 7 | `build_rupture_aftermath` |
| `target_asl_s` | Target average shot length, set from the rhythm shape, the tone and card 13, never from rhythm_class. | seconds | standard | ai | step 7 | `5.5` |
| `rupture` | The one break in the scene's pattern. | sub_parts; first part: id (BEAT); device: word (hold, drop_out, true_silence, cut_to_black, camera_change, pov_change); breaks: text | standard | ai | step 7 | `SC10-B07 \| device: hold \| breaks: the cutting between singles` |
| `tone_shift` | A change of tone inside the scene, on a turn or a drop (D10 TN2), or none. | sub_parts; first part: id (BEAT); from: word (grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative); to: word (grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative); device: word (size_ladder, light_cue, music_in, music_out, camera_behaviour); also none | standard | ai | step 7 | `none` |
| `room_sound` | The steady background sound here. | text; also as_place | standard | ai | step 7 | `as_place` |
| `geography` | Action scenes: where everything is (card 15, D11). | text | standard | ai | step 7 | `the shaft runs north-south; the cage hangs at the third landing` |
| `cause_chain` | Action scenes: each cause and its effect. | text | standard | ai | step 7 | `the brake bolts are gone; the cage drops; the cable snaps taut` |
| `escalation` | Action scenes: how the danger grows. | text | standard | ai | step 7 | `from a slip, to a fall, to a shot` |
| `reversal` | Action scenes: the beats where the advantage changes hands. | id_list; IDs of BEAT | standard | ai | step 7 | `SC06-B05, SC06-B09` |
| `action_score` | Action scenes: a text block, one row per count, one column per body, the set and the camera. | text | standard | ai | step 7 | `see the table above the divider` |
| `time_treatment` | Action scenes: how screen time relates to story time (slow_motion only where the camera system allows it). | real_time_continuous, held_real_time, overlapping_slices, elliptical, slow_motion | standard | ai | step 7 | `overlapping_slices` |
| `departure` | A scene-level break from a film rule. | sub_parts; first part: id (CAMSYS, CAMRULE, RESERVE, LENS, LOOK, VISUAL, SOUNDPLAN, LADDER, RULE); what: text; why: text; also none; one line each | standard | ai | step 7 | `CAMSYS \| what: one handheld shot as Iona loses control of the car \| why: "A night bus comes at them with its number written backwards." is the beat control is lost (B1 R17)` |
| `additions` | Inventions awaiting keep or cut, each marked whether it changes what the scene means. | sub_parts; first part: text; changes_meaning: yes_no; also none; one line each | standard | ai | step 7 | `Iona sets the lamp down before the raised hands \| changes_meaning: yes` |
| `lines_not_shown` | Story lines of the scene that no shot (no list item at quick) shows on purpose, each with its reason, so COVER-02 is silent for them. | sub_parts; first part: lines; why: text; also none; one line each | optional | ai | step 7 | `486 \| why: the transition "CUT TO BLACK." is the cut SC10-C200, not a shot` |
| `flags` | Scene-level faults found, never fixed (line-level faults are BEAT flag). | word_list; nonevent, splintered, turn_too_soon, turn_too_late, continuity; also none | standard | ai | step 7 | `none` |
| `era` | The mirror era the scene is in (from the mirror RULE's era lines). | word | quick, worked out by code | code_derived | step 7 | `b` |
| `frame_handedness` | Whether the scene's frame is original or reversed. | original, reversed | quick, worked out by code | code_derived | step 7 | `original` |
| `switch_at` | The line where the era switches inside the scene. | lines | quick, worked out by code | code_derived | step 7 | `263` |
| `states_in_play` | The element states valid in the scene. | id_list; IDs of STATE | quick, worked out by code | code_derived | step 7 | `CH-IONA.S02, CH-SAYE.S01` |
| `duration_est_s` | Estimated scene length from its shots. | seconds | quick, worked out by code | code_derived | step 7 | `96` |
| `label` | The scene's plain name in views (Scene 10 - Saye's kitchen). | text | quick, worked out by code | code_derived | step 7 | `Scene 10 - Saye's kitchen` |
| `eighths` | The scene's length on the page in eighths (5.6 labels and counts). | number | quick, worked out by code | code_derived | step 1 | `12` |

Status values: draft, approved, stale, omitted.

## PART: part

A part of a scene with its own turn. ID: scene ID, -P and one digit (`SC10-P2`); the user sees it as part 2. Lives in: 11 Scenes/Scene NN - <place>.md. Designed at step 7; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `beats` | The beats in the part. | id_range; IDs of BEAT | standard | ai | step 7 | `SC10-B09..SC10-B11` |
| `turn` | The part's turn beat. | id; IDs of BEAT; also none | standard | ai | step 7 | `SC10-B11` |
| `starts` | How the part starts. | scene_start, after_drop, without_drop | standard | ai | step 7 | `after_drop` |

Status values: draft, approved, stale, omitted.

## BEAT: beat

One action and reaction (McKee's beat). ID: scene ID, -B and 2 digits (`SC10-B07`); the user sees it as beat 7. Lives in: 11 Scenes/Scene NN - <place>.md. Designed at step 7; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `lines` | The story lines the beat covers. | lines | quick | ai | step 7 | `454-463` |
| `action` | Who does what, as a tactic (an -ing word). | sub_parts; first part: id (CHARACTER); tactic: word | standard | ai | step 7 | `CH-SAYE \| tactic: proving` |
| `reaction` | Who reacts, as a tactic. | sub_parts; first part: id (CHARACTER); tactic: word | standard | ai | step 7 | `CH-IONA \| tactic: testing` |
| `task` | What the hands do. | sub_parts; first part: id (CHARACTER); does: text; one line each | standard | ai | step 7 | `CH-IONA \| does: chews the leaf` |
| `beat_intensity` | Pressure inside the scene, 1 to 5 (at most two 5s per part). | number; from 1 to 5 | standard | ai | step 7 | `5` |
| `turn` | Whether a value turns here. | none, turn, main_turn | quick | ai | step 7 | `main_turn` |
| `turn_kind` | How the value turns. | action, revelation | quick | ai | step 7 | `revelation` |
| `charge` | Each value's charge after the beat. | sub_parts; first part: id (VALUE); charge: charge; one line each | standard | ai | step 7 | `SC10-V1 \| charge: ---` |
| `flag` | A flaw in one line, flagged, never fixed (A1). | sub_parts; first part: word (on_the_nose, melodrama, forced_exposition, monologue, repetitious, can_play_silent, interrupted); line: id; one line each | standard | ai | step 7 | `can_play_silent \| line: SC10-D05` |
| `engaged_pair` | In a three-person scene, the two engaged (B3 R25, A1 R5). | id_list; IDs of CHARACTER | standard | ai | step 7 | `CH-SAYE, CH-IONA` |
| `silent_third` | In a three-person scene, the witness. | id; IDs of CHARACTER | standard | ai | step 7 | `CH-ELI` |
| `five_steps` | Desire, obstacle, choice, action, expression as visible moments (five items). | sub_parts; first part: word (desire, obstacle, choice, action, expression); shows: text; one line each | standard | ai | step 7 | `choice \| shows: she takes the leaf from Saye's fingers` |
| `landing_face` | Who the audience watches when the line lands. | id; pattern `^(CH-[A-Z0-9-]+\|insert:\S+\|wide)$`; IDs of CHARACTER; also wide | standard | ai | step 7 | `CH-IONA` |
| `unsaid` | What a character thinks and does not say. | sub_parts; first part: id (CHARACTER); thought: text | standard | ai | step 7 | `CH-IONA \| thought: then we are not home` |
| `carrier` | What makes the unsaid seen or heard (an ID, or words). | text | standard | ai | step 7 | `MO-MINT` |
| `pause_after` | The pause after the beat, by tier (constant pause_tiers); a hold above 4.0 s needs a saved choice. | sub_parts; first part: word (none, short, medium, long, hold); seconds: seconds; picture: word (hold, push_in, cut, cut_wide); sound: text | standard | ai | step 7 | `long \| seconds: 3 \| picture: hold \| sound: room sound only` |
| `emphasis` | How loud each motif or thing is on this beat, 0 to 3. | sub_parts; first part: id (MOTIF, PROP, TEXT, STATE); level: number; also none; one line each | standard | ai | step 7 | `MO-MINT \| level: 2` |
| `added_emphasis` | An extra signal on this beat: 0 or 1, and what it is (0 where the script marks the beat). | sub_parts; first part: number (0, 1); what: text | standard | ai | step 7 | `0` |
| `change` | The configuration change on a turn. | text | standard | ai | step 7 | `Iona steps back from the table; Saye does not move.` |
| `distance` | Detailed staging: the distance and zone between two characters. | sub_parts; first part: id_list (CHARACTER); metres: metres; zone: word (intimate, personal, social, public); one line each | detailed | ai | step 7 | `CH-IONA, CH-SAYE \| metres: 1.5 \| zone: personal` |
| `core_word` | Detailed dialogue: the word carrying the line's meaning. | text | detailed | ai | step 7 | `mint` |
| `cut_rule` | Detailed dialogue: how the cut treats the line. | cut_on_core_word, cut_early_split, hold, no_cut_two_shot | detailed | ai | step 7 | `hold` |
| `fact` | Detailed: facts revealed or protected on this beat. | id_list; IDs of FACT; also none | detailed | ai | step 7 | `FT-03` |
| `script_marked` | yes when the beat's lines already mark it: a capitalised sound, emphasis or text token, or a light, colour or darkness word that stage.py read found and that is light in its sentence, not a person's colour (B1 P11, B4 R17). CRAFT-10 and added_emphasis_per_beat_max read it. | yes_no | quick, worked out by code | code_derived | step 7 | `yes` |

Status values: draft, approved, stale, omitted.

## SPEECH: speech

One spoken line. Screenplay speeches are read by code into speeches.json; prose speeches are written by the AI in the scene file. ID: scene ID, -D and 2 digits (3 if a scene has more than 99), numbered in cue order within the scene (`SC10-D11`); the user sees it as the words. Lives in: 11 Scenes/Scene NN - <place>.md, For machines - do not edit/speeches.json. Designed at step 7; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `speaker` | Who speaks. | id; IDs of CHARACTER | quick | story (when source_is_screenplay); ai (when source_not_screenplay) | step 7 | `CH-IONA` |
| `line` | The line number of the cue (a quote anchor in chat). | lines | quick | story (when source_is_screenplay); ai (when source_not_screenplay) | step 7 | `463` |
| `text` | The exact words spoken. | text | quick | story (when source_is_screenplay); ai (when source_not_screenplay) | step 7 | `Not mint.` |
| `parenthetical` | The parenthetical, if any. | text; also none | quick | story (when source_is_screenplay); ai (when source_not_screenplay) | step 7 | `none` |
| `extension` | The cue extension, if any ((V.O.), (O.S.)). | text; also none | quick | story (when source_is_screenplay); ai (when source_not_screenplay) | step 7 | `none` |
| `path` | How the voice reaches us. | direct, off_screen, earpiece, radio, intercom, phone, device_speaker, recording, helmet_inside, helmet_outside, through_glass, voice_over, thought | quick | story (when source_is_screenplay); ai (when source_not_screenplay) | step 7 | `direct` |
| `origin` | Whether the words are the story's, adapted, or invented. | story, adapted, invented | quick | story (when source_is_screenplay); ai (when source_not_screenplay) | step 7 | `story` |
| `word_count` | The number of words in the speech, read by the time floor and the captions (5.6). | number | quick, worked out by code | code_derived | step 1 | `19` |

Status values: draft, approved, stale, omitted.

## MOVE: floor-plan move

A character's move on the set plan (never a camera move). ID: scene ID, -M and 2 digits (`SC10-M04`); the user sees it as move 4. Lives in: 11 Scenes/Scene NN - <place>.md. Designed at step 7; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `beat` | The beat it happens in. | id; IDs of BEAT | standard | ai | step 7 | `SC10-B05` |
| `who` | The character who moves. | id; IDs of CHARACTER | standard | ai | step 7 | `CH-IONA` |
| `from` | Where the move starts: a mark or a point. | text | standard | ai | step 7 | `IONA_MARK` |
| `to` | Where the move ends: a mark or a point. | text | standard | ai | step 7 | `[2.8, 2.2]` |
| `via` | A point the path passes through, or none when the move goes straight. | point; also none | standard | ai | step 7 | `[3.4, 2.4]` |
| `start_s` | When it starts, counted from the start of the first shot that shows its beat. | seconds | standard | ai | step 7 | `1.5` |
| `dur_s` | How long the move takes. | seconds | standard | ai | step 7 | `2` |
| `faces` | What the character faces at the end: an ID or a point. | text | standard | ai | step 7 | `CH-SAYE` |
| `posture` | The posture at the end. | standing, seated, lying, kneeling | standard | ai | step 7 | `standing` |
| `why` | The want or task behind the move (toward the door = escape). | text | standard | ai | step 7 | `to set the lamp down where Saye can see her hands` |
| `origin` | Whether the move is in the story, inferred, or invented. | story, inferred, invented | standard | ai | step 7 | `invented` |

Status values: draft, approved, stale, omitted.

## SETUP: setup

A camera position in a scene (shown to the user as camera A, B, C ... in order). ID: scene ID, -SU and 2 digits (`SC10-SU02`); the user sees it as camera B. Lives in: 11 Scenes/Scene NN - <place>.md. Designed at step 7; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `at` | The camera position as a point (with a set plan). | point | standard | ai | step 7 | `[-3.5, 1.8, 1.45]` |
| `at_words` | The camera position in words (without a set plan). | text | standard | ai | step 7 | `beside Saye's shoulder` |
| `look_at` | The point the camera aims at. | point | standard | ai | step 7 | `[2.8, 1.8, 1.4]` |
| `look_at_words` | Where the camera aims, in words (without a set plan). | text | standard | ai | step 7 | `Iona's hands on the gate` |
| `lens_mm` | The lens (full-frame). | millimetres | standard | ai | step 7 | `85` |
| `use` | What the setup is for. | text | standard | ai | step 7 | `the reflection two-shot through the wild wall` |
| `side` | Which side of the line the camera is on. | a, b | standard | ai | step 7 | `a` |
| `mount` | What the camera is fixed to: the world, or an ID of a moving thing. | text | standard | ai | step 7 | `world` |

Status values: draft, approved, stale, omitted.

## SHOTLIST: shot list

The one-line shot list that fixes the shot IDs and count before detail is written. ID: scene ID and -LIST (`SC10-LIST`); the user sees it as the shot list. Lives in: 11 Scenes/Scene NN - <place>.md. Designed at step 7; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `item` | One planned shot; the first part declares the shot ID. At quick the items are the final shots. | sub_parts; first part: id (SHOT); beats: id_list; role: word (turn, must_keep, normal); size: word (extreme_wide, wide, medium_wide, medium, medium_close_up, close_up, extreme_close_up, insert); frame: word (single, two_shot, three_shot, group, over_shoulder, pov, near_pov, empty); subject: id_list; time: seconds; shows: text; one line each | quick | ai | step 7 | `SC10-SH150 \| beats: SC10-B07, SC10-B08 \| role: turn \| size: close_up \| frame: single \| subject: CH-IONA \| time: 15 \| shows: Iona chews, stops, chews once more; "Not mint."; we stay on her through Saye's answer` |
| `approved` | The user passed checkpoint C, or it was reported without changes. | yes_no | quick | code_state; in a chat without code: ai | checkpoint C | `yes` |

Status values: draft, approved, stale, omitted.

## SHOT: shot

One shot, written from its list item at standard and detailed, reason-first (purpose and because before camera values). ID: scene ID, -SH and 3 digits in steps of 10; an insert takes a number between (SH155); 990-999 for end cards and black (`SC10-SH150`); the user sees it as shot 150. Lives in: 11 Scenes/Scene NN - <place>.md, 11 Scenes/Scene NN - <place> - shots NNN-NNN.md. Designed at step 8; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `beats` | The beats the shot shows. | id_list; IDs of BEAT | quick | ai | step 8 | `SC10-B07, SC10-B08` |
| `lines` | The story lines the shot shows (a quote anchor pair in chat). | lines | quick | ai | step 8 | `454-466` |
| `purpose` | What the audience must get from the shot, one sentence. | text | quick | ai | step 8 | `Iona's body admits what her words denied; Saye's proof lands on her face.` |
| `because` | The records that justify the shot (5.4 rule 3), or default on a normal shot with no departure. | because_list; IDs of SCENE, VALUE, PART, BEAT, SPEECH, MOVE, SETUP, SEQUENCE, PLAN, PLANT, FACT, CARDINAL, STRAND, CHAPTER, CHARACTER, VOICE, LOCATION, PROP, TEXT, MOTIF, CAMERA, STATE, WORLD, STYLE, RULE, CAMSYS, CAMRULE, RESERVE, LENS, LOOK, VISUAL, SOUNDPLAN, LADDER; also default | quick | ai | step 8 | `SC10-B07, SC10-V1, MO-MINT, CR-IONA` |
| `role` | How much the scene depends on the shot. | turn, must_keep, normal | quick | ai | step 8 | `turn` |
| `kind` | The kind of shot: live (filmed in the scene), insert (a thing close), pov (what a character sees with their own eyes), screen (the picture an in-story camera or device makes, at that camera's own lens; CRAFT-07), card (a title) or black. | live, insert, pov, screen, card, black | quick | ai | step 8 | `live` |
| `why` | The story reason for any value on the list in 5.4 rule 11 that departs from its default, or for any departure from the camera system; always on turn shots. One sentence quoting a line, naming an object or action, or citing an ID. | text | standard | ai | step 8 | `"Her face changes." puts the turn inside her mouth, so the scene's closest frame is spent here and held while Saye's proof lands off screen.` |
| `origin` | Where the shot's content comes from. | story, inferred, invented | quick | ai | step 8 | `story` |
| `additions` | Inventions in frame (each also listed in the scene's additions). | text; also none | standard | ai | step 8 | `none` |
| `pov_break` | Why the shot leaves the whose-scene character's place or knowledge (A3 rule 37). | text | standard | ai | step 8 | `the audience sees the figure's hand before Iona does` |
| `setup` | The camera position. | id; IDs of SETUP | standard | ai | step 8 | `SC10-SU02` |
| `frame` | Who is framed. | single, two_shot, three_shot, group, over_shoulder, pov, near_pov, empty | quick | ai | step 8 | `single` |
| `frame_detail` | Framing variant (standard when the framing is a saved choice; every shot at detailed). | clean, dirty, symmetrical_profile, none | standard | ai | step 8 | `symmetrical_profile` |
| `size` | Shot size. | extreme_wide, wide, medium_wide, medium, medium_close_up, close_up, extreme_close_up, insert | quick | ai | step 8 | `close_up` |
| `angle` | Tilt of the camera (dutch only when a saved choice allows it). | eye_level, low, high, top_down, worms_eye, dutch; default eye_level | quick | ai | step 8 | `eye_level` |
| `height` | Whose eye height the camera is at, or a height in metres. | text; pattern `^((eye\|seated\|kneeling):CH-[A-Z0-9]+(-[A-Z0-9]+)*\|floor\|\d+(\.\d+)?)$`; default the eye of the whose_scene character, or of the subject | standard | ai | step 8 | `eye:CH-IONA` |
| `lens_mm` | The lens (full-frame). | millimetres; default CAMSYS.normal_lens_mm | standard | ai | step 8 | `50` |
| `focus` | Depth of field. | deep, moderate, shallow; default moderate | standard | ai | step 8 | `moderate` |
| `focus_on` | What is sharp. | id; IDs of CHARACTER, STATE, PROP, TEXT, MOTIF, LOCATION | standard | ai | step 8 | `CH-IONA` |
| `move` | The one camera move (orbit, zoom, whip_pan, dolly_zoom and drone only when a saved choice allows them). | static, pan, tilt, push_in, pull_back, sideways, rise, lower, follow, lead, handheld, crane, orbit, zoom, whip_pan, dolly_zoom, drone; default static | quick | ai | step 8 | `static` |
| `move_reason` | What causes the camera move. | text; also none | standard | ai | step 8 | `none` |
| `mount` | What the camera is fixed to. | text | detailed | ai | step 8 | `world` |
| `stance` | The camera's stance. | objective, pov, near_pov, direct_address | detailed | ai | step 8 | `objective` |
| `dominant` | What is seen first. At detailed the AI writes it; at standard code derives it from focus_on, role and the first subject. | text | detailed | ai (when depth_detailed); code_derived (when depth_below_detailed) | step 8 | `Iona's mouth` |
| `placement` | Where the dominant sits. | thirds, centre, edge | detailed | ai | step 8 | `thirds` |
| `layers` | Foreground, middle and background. | text | detailed | ai | step 8 | `foreground: table edge; middle: Iona; background: dark window` |
| `frame_in_frame` | A frame within the frame. | text; also none | detailed | ai | step 8 | `none` |
| `device` | At most one expressive device. | text; also none | detailed | ai | step 8 | `none` |
| `glass` | Every glass surface in frame. | sub_parts; first part: text; state: word (clear, marked, reflecting, screen, broken_open); camera: word (through, along, angled); one line each | standard | ai | step 8 | `window \| state: reflecting \| camera: angled` |
| `subject` | Who is in frame, where, facing, doing. | sub_parts; first part: id (STATE, CHARACTER); at: word (left_edge, left_third, centre, right_third, right_edge); faces: word (frame_left, frame_right, camera, away, up, down); does: text; tactic: word; energy: word (still, held, rising, breaking, spent); display: number (1, 2, 3); still: word_list (head, eyes, mouth, hands, torso, whole_body); eyeline: text; dwell_s: seconds; travel: word (frame_left, frame_right, up, down, toward_camera, away, none); must_not: text; continues: id; recorded: text; also none; one line each | quick | ai | step 8 | `CH-IONA.S02 \| at: left_third \| faces: camera \| eyeline: CH-SAYE \| dwell_s: 15 \| does: chews slowly; stops chewing; a small frown \| tactic: discovering \| energy: held \| display: 1 \| still: head, hands, torso \| travel: none` |
| `thing` | Register items in frame and how loud they are; plant or payoff on the shot that plants or pays off a PLANT. | sub_parts; first part: id (PROP, STATE, MOTIF, TEXT); emphasis: number; at: text; plant: id; payoff: id; recorded: text; also none; one line each | standard | ai | step 8 | `MO-MINT \| emphasis: 2` |
| `text` | Text in picture in frame. | id_list; IDs of TEXT; also none | standard | ai | step 8 | `TX-GOODS-ONLY` |
| `keep_hidden` | What stays out of view, the fact it protects, and how. | sub_parts; first part: id (FACT); how: word (frame_edge, focus, dark, obstruction, timing, sound_first); one line each | standard | ai | step 8 | `FT-03 \| how: frame_edge` |
| `must_show` | What must appear. | id_list; IDs of CHARACTER, STATE, PROP, TEXT, MOTIF, LOCATION, CAMERA; also none | standard | ai | step 8 | `PR-FLASK` |
| `must_not_show` | What must not appear. | id_list; IDs of CHARACTER, STATE, PROP, TEXT, MOTIF, LOCATION, CAMERA; also none | standard | ai | step 8 | `none` |
| `physics_note` | Deliberately wrong physics as visible evidence (words for prompts). | text | standard | ai | step 8 | `hair, cloth and straps drift up; nothing settles` |
| `motion` | Structured physical motion the free-fall helper reads. | sub_parts; first part: word (free_fall); object: id; from_z: metres; to_z: metres; start_frame: number; one line each | standard | ai | step 8 | `free_fall \| object: PR-CAGE \| from_z: 9.2 \| to_z: 2.53 \| start_frame: 1` |
| `light` | Light, if different from the look. | text; also as_look; default as_look | standard | ai | step 8 | `as_look` |
| `light_cue` | A light change during the shot. | sub_parts; first part: text; when: seconds; why: text; also none | standard | ai | step 8 | `the beam stops moving \| when: 3 \| why: "She stays on her knees. One breath."` |
| `dark` | What stays dark. | text | detailed | ai | step 8 | `the far corner behind Saye` |
| `eye_light` | A catchlight in the eyes. | yes_no | detailed | ai | step 8 | `yes` |
| `hear` | A speech heard in the shot. | sub_parts; first part: id (SPEECH); speaker: word (on_screen, off_screen, hidden); path: word (direct, off_screen, earpiece, radio, intercom, phone, device_speaker, recording, helmet_inside, helmet_outside, through_glass, voice_over, thought); at: seconds; words: quote; also none; one line each | quick | ai | step 8 | `SC10-D11 \| speaker: on_screen` |
| `effect` | A sound tied to an action. | sub_parts; first part: text; at: seconds; sound_emphasis: number; also none; one line each | standard | ai | step 8 | `the pump \| at: 2 \| sound_emphasis: 1` |
| `room_sound` | The background. | text; also as_place; default as_place | standard | ai | step 8 | `as_place` |
| `silence` | The silence grade. | none, room_sound_only, drop_out, true_silence; default none | standard | ai | step 8 | `room_sound_only` |
| `music` | Music under the shot. | id; IDs of MUSIC; also none; default none | standard | ai | step 8 | `none` |
| `needs_description` | The beat carries story with no sound (audio description). | yes_no | standard | ai | step 8 | `yes` |
| `screen_time` | Used length on screen, at or above the floor code derives. | seconds | quick | ai | step 8 | `15` |
| `moment` | A timed visible change inside the shot. | sub_parts; first part: span; shows: text; one line each | standard | ai | step 8 | `4-6 \| shows: stops chewing; a small frown` |
| `compound` | yes when the shot deliberately holds more than one main action per main_actions_per_seconds (5.8, C3 R2); TIME-06 is then silent, and the shot's why says why the actions cannot be split. | yes_no; default no | optional | ai | step 8 | `no` |
| `start` | How the shot opens, from the previous shot. | text | detailed | ai | step 8 | `from_end_of: SC10-SH140` |
| `end` | The last picture. | text | standard | ai | step 8 | `still, mouth closed, eyes on Saye` |
| `cut_in_on` | Why the cut into the shot falls here. | action, look, line, sound, rhythm, reveal | detailed | ai | step 8 | `look` |
| `cut_out_on` | Why the cut out of the shot falls here. | thought_complete, action_midpoint, line_end, sound_hit, rhythm, keep_hidden | standard | ai | step 8 | `thought_complete` |
| `time_slice` | Frames of a master previs this shot covers (overlapping slices); code creates the PREVIS stub if missing. | sub_parts; first part: id (PREVIS); frames: text | standard | ai | step 8 | `PV-SC06-MASTER-V01 \| frames: 12-40` |
| `held` | The meaning depends on not cutting inside this shot, so it is never split into chained clips (8.4). Turn shots and shots in a oner scene count as held. | yes_no; default no | standard | ai | step 8 | `no` |
| `previs_level` | The grey preview rung (C4): 0 simple, 2 layout check, 3 guide video, 4 performance capture. | number; from 0 to 5 | standard | ai | step 8 | `0` |
| `storyboard` | Make a storyboard frame. | yes_no | standard | ai | step 8 | `yes` |
| `framing_critical` | The meaning depends on exact framing. | yes_no | standard | ai | step 8 | `no` |
| `pose_critical` | A declared pose is needed. | yes_no | detailed | ai | step 8 | `no` |
| `route` | How to make it. | auto, text, start_picture, start_end_pictures, references, guide_video, performance_transfer, still_with_move, composite_only; default auto | standard | ai | step 8 | `auto` |
| `model` | An override of the scene model, with its reason. | sub_parts; first part: text; why: text; also none | optional | ai | step 8 | `none` |
| `flip` | Author override of the mirror route. | auto, never | standard | ai | step 8 | `auto` |
| `content_flags` | Sensitive content (D4). | word_list; violence_implied, violence_onscreen, weapon_visible, gunfire, blood_small, gore, nudity, minor_present, self_harm, drug_use, real_person, real_brand, fire, none | standard | ai | step 8 | `none` |
| `policy_route` | How sensitive content is made. | as_written, restated, split_cause_reaction_aftermath, composite_element, sound_only, cut | standard | ai | step 8 | `as_written` |
| `cost_class` | The work the shot needs (D13). | graphic, reuse, still_move, easy, dialogue, hard | standard | ai | step 8 | `dialogue` |
| `reuse_of` | An approved shot it reuses. | id; IDs of SHOT; also none | standard | ai | step 8 | `none` |
| `departure` | A change forced by a tool, with the meaning it keeps. | sub_parts; first part: text; from: text; to: text; because: word (feasibility); meaning_kept: text; one line each | standard | ai | step 8 | `move \| from: push_in \| to: static \| because: feasibility \| meaning_kept: the scene's closest frame stays on the turn` |
| `gen_note` | An instruction to the prompt compiler the fields cannot express. | text | optional | ai | step 8 | `keep the leaf in her right hand's fingers throughout` |
| `label` | The crew label used only in the shot-list spreadsheet (10Q: letters from A at SH010, skipping I and O). | text | quick, worked out by code | code_derived | step 8 | `10Q` |
| `min_screen_time_s` | The time floor, max(speech_floor, text_floor) + pause_owed, printed with its reasons (5.6). | seconds | quick, worked out by code | code_derived | step 8 | `13.8` |
| `clips` | Clip lengths per model and handles (8.4). | text | quick, worked out by code | code_derived | step 8 | `SC10-SH150.1 17 s seedance-2.5` |
| `era` | The mirror era. | word | quick, worked out by code | code_derived | step 8 | `b` |
| `mirror_state` | Per element in frame: mirrored or normal. | text | quick, worked out by code | code_derived | step 8 | `CH-SAYE.S01 mirrored` |
| `mirror_route` | The mirror route (8.5). | word | quick, worked out by code | code_derived | step 8 | `plate` |
| `post_ops` | Finishing operations the shot needs. | text | quick, worked out by code | code_derived | step 8 | `flip, composite` |
| `image_sides` | Image side and prompt side of every sided feature in frame. | text | quick, worked out by code | code_derived | step 8 | `Saye's ring: frame-right` |
| `main_light_side` | The frame side of the look's main light for this shot's setup and era, or open when the look places it on no set-plan object or compass wall (5.6). | text | quick, worked out by code | code_derived | step 8 | `frame_right` |
| `eyeline_sides` | The eyeline side of every single. | text | quick, worked out by code | code_derived | step 8 | `Iona looks frame-right` |
| `projected_placement` | Frame placement and facing projected from the set plan (when one exists). | text | quick, worked out by code | code_derived | step 8 | `Iona left_third, faces frame_right` |
| `size_check` | The size computed from lens and distance (5.6). | word | quick, worked out by code | code_derived | step 8 | `medium` |
| `face_height` | Face height as a fraction of frame height. | number | quick, worked out by code | code_derived | step 8 | `0.4` |
| `lip_sync` | How closely mouths must match speech. | none, loose, tight | quick, worked out by code | code_derived | step 8 | `tight` |
| `needs` | Generation needs tags for routing. | word_list | quick, worked out by code | code_derived | step 8 | `recurring_dialogue, single_take_over_15_s` |
| `scene_model` | The scene's chosen video model. | text | quick, worked out by code | code_derived | step 8 | `kling-3.0-omni` |
| `suggested_model` | The model routing suggests for this shot. | text | quick, worked out by code | code_derived | step 8 | `seedance-2.5` |
| `generation_spec` | The model-neutral generation spec, prompts, lint result, resolution, safe band and cost. | text | quick, worked out by code | code_derived | step 8 | `see 20 Prompts for AI video` |

Status values: draft, approved, stale, omitted.

## CUT: cut

A join between shots, only where it is not a plain cut. ID: scene ID, -C and the number of the shot it follows (`SC10-C200`); the user sees it as the cut after shot 200. Lives in: 11 Scenes/Scene NN - <place>.md, 11 Scenes/Scene NN - <place> - shots NNN-NNN.md. Designed at step 8; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `to` | The next shot. | id; IDs of SHOT | standard | ai | step 8 | `SC10-SH990` |
| `type` | The kind of join. | j_cut, l_cut, match_cut, jump_cut, smash_cut, dissolve, fade, cut_to_black, freeze, continue | standard | ai | step 8 | `cut_to_black` |
| `split_s` | The sound lead or lag of a split edit. | seconds | standard | ai | step 8 | `0.5` |
| `black_frames` | Frames of black. | number | standard | ai | step 8 | `12` |
| `sound_across` | What sound carries over the cut. | text | standard | ai | step 8 | `the pump` |
| `shared_geometry` | The previs both shots are built from (match cuts); code creates the PREVIS stub if missing. | id; IDs of PREVIS | standard | ai | step 8 | `PV-SC06-MASTER-V01` |
| `why` | The reason for the join. | text | standard | ai | step 8 | `the story writes CUT TO BLACK after "Nobody leave this room."` |

Status values: draft, approved, stale, omitted.

## PLAN: story plan

The film-level plan every later choice keys to. ID: None (`None`); the user sees it as None. Lives in: 05 Story plan.md. Designed at step 2; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `logline` | The story in one sentence. | text | quick | ai | step 2 | `A night nurse finds that her newest patient is her missing brother and has to decide whether to report him.` |
| `theme_question` | The question the film asks. | text | quick | ai | step 2 | `What do we owe the people we cannot save?` |
| `core_value` | The value at stake, with its two poles. | sub_parts; first part: text; positive: text; negative: text | quick | ai | step 2 | `loyalty \| positive: faithful \| negative: betrayed` |
| `core_opposition` | Two nouns in opposition. | text | standard | ai | step 2 | `family against duty` |
| `crisis` | The decision that forces the climax, as a story point. | story_point | quick | ai | step 2 | `SC24 "She deletes the way home."` |
| `climax` | The scene or scenes where the core value turns for the last time. | id_range; IDs of SCENE | quick | ai | step 2 | `SC26..SC27` |
| `act` | The acts, each with its scenes and its turn. | sub_parts; first part: text; scenes: id_range; turn: story_point; one line each | standard | ai | step 2 | `act one \| scenes: SC01..SC06 \| turn: SC06 "Her eyes open."` |
| `peak` | Where each component peaks, with a reason when away from the climax. | sub_parts; first part: word (story, crisis_choice, colour, contrast, tightest_size, longest_hold, loudest_sound, motif_payoff, camera_break, sound_rupture); scene: id; reason: text; one line each | standard | ai | step 2 | `tightest_size \| scene: SC13 \| reason: the confession's turn lands inside Iona; the climax is played wide and still, in counterpoint` |
| `pov_plan` | The default point of view and its declared breaks. | sub_parts; default: id; breaks: text | standard | ai | step 2 | `default: CH-IONA \| breaks: none` |
| `genre` | The named genre (copied to PROJECT). | word | quick | ai | step 2 | `thriller` |
| `tone_home` | The film's home tone (D10 §2.1). | grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative | quick | ai | step 2 | `tense` |
| `tone_range` | The tones allowed anywhere. | word_list; grave, tense, dread, enigmatic, comic_light, comic_dark, romantic, kinetic, lyric, wonder, contemplative | standard | ai | step 2 | `tense, enigmatic, dread, grave` |
| `tone_mix_rule` | How tones mix (D10 §9). | text | standard | ai | step 2 | `comic_dark only in Jude's lines and physical business; never in camera` |
| `plan_option` | Prose: a macro plan shown at checkpoint P. | sub_parts; first part: word; format: word (short, feature, limited_series); runtime_s: seconds; scenes: number; shots: number; keeps: text; cuts: text; loses: text; one line each | quick | ai | step 2 | `A \| format: feature \| runtime_s: 6000 \| scenes: 48 \| shots: 1300 \| keeps: Nilay and Emre whole \| cuts: Malta \| loses: much of the village's grief` |
| `loses` | What the audience loses in the chosen plan. | text | standard | ai | step 2 | `a secondary strand and its ending` |
| `op` | Each adaptation operation. | sub_parts; first part: word (trim, merge_scenes, fold_into, composite_character, move_line, move_plant, delete_strand, reorder, invention, replace, flashback_import, lost_resonance); what: text; from: text; to: text; why: text; one line each | standard | ai | step 2 | `merge_scenes \| what: two visits to the same room \| from: SC08, SC09 \| to: SC08 \| why: the second visit repeats the first visit's turn` |
| `runtime_estimate` | The runtime estimate in seconds (D13 v0, then the plan). | seconds | quick | code_state; in a chat without code: ai | step 2 | `2118` |
| `scene_budget` | The scene budget (D2 R7). | number | quick | code_state; in a chat without code: ai | step 2 | `30` |
| `shot_budget` | The shot budget (D13). | number | quick | code_state; in a chat without code: ai | step 2 | `480` |

Status values: draft, approved, stale, omitted.

## SEQUENCE: sequence (group of scenes)

One group of scenes; colour and visual plans are written at step 6 against these IDs. ID: SQ and 2 digits (`SQ03`); the user sees it as group of scenes 3: the wrong world (short: group 3). Lives in: 05 Story plan.md. Designed at step 2; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `title` | The group's plain name. | text | quick | ai | step 2 | `the wrong world` |
| `scenes` | Its scenes. | id_range; IDs of SCENE | quick | ai | step 2 | `SC07..SC10` |
| `story_job` | What the group does in the story. | text | standard | ai | step 2 | `teaches Iona that the world is mirrored` |
| `value_change` | How the core value changes across it. | text | quick | ai | step 2 | `hope of help to proof of wrongness` |
| `act` | The act it belongs to. | text | standard | ai | step 2 | `act two` |
| `scene_intensity` | The range of scene intensity across it. | text; pattern `^\d{1,2}(-\d{1,2})?$` | standard | ai | step 2 | `5-7` |
| `travel` | The default direction of travel across the frame. | left_to_right, right_to_left, up, down, none | standard | ai | step 2 | `left_to_right` |

Status values: draft, approved, stale, omitted.

## PLANT: plant

A plant and its payoff; the shots that plant and pay off name it on their thing items (plant:, payoff:). ID: PL- and 2 digits (`PL-07`); the user sees it as plain name. Lives in: 05 Story plan.md. Designed at step 2; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `what` | What is planted. | text | standard | ai | step 2 | `the mint growing in Saye's kitchen` |
| `planted_at` | Where it is planted, as a story point. | story_point | standard | ai | step 2 | `SC10 "A pot of mint on the windowsill"` |
| `paid_off_at` | Where it pays off, as a story point. | story_point | standard | ai | step 2 | `SC10 "Her face changes."` |
| `plant_emphasis` | How loud the plant is, 0 to 3 (constant plant_emphasis_max). | number; from 0 to 3 | standard | ai | step 2 | `1` |
| `plot_event` | yes when the plant is itself a plot event (A1 R20): its planting shot may reach emphasis 2, with nothing pointing forward (K11, plant_emphasis_max, CRAFT-08). | yes_no; default no | optional | ai | step 2 | `no` |
| `payoff_emphasis` | How loud the payoff is, 0 to 3. | number; from 0 to 3 | standard | ai | step 2 | `2` |
| `rhyme` | Whether plant and payoff rhyme in framing. | sub_parts; first part: yes_no; framing: text; side: word (same, reversed); also no | standard | ai | step 2 | `yes \| framing: the same profile two-shot` |
| `motif` | The motif it belongs to. | id; IDs of MOTIF; also none | standard | ai | step 2 | `MO-MINT` |

Status values: draft, approved, stale, omitted.

## FACT: fact

Who knows what, from when; element names what would give the fact away in frame. ID: FT- and 2 digits (`FT-03`); the user sees it as plain name. Lives in: 05 Story plan.md. Designed at step 2; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `what` | The fact. | text | standard | ai | step 2 | `the world is mirrored` |
| `element` | What would give the fact away in frame: IDs; before step 4 designs the things, a story point naming where it is seen, which step 4's things unit re-points to IDs (fix list C23). | element_list; IDs of CHARACTER, STATE, PROP, TEXT, MOTIF, LOCATION, CAMERA | standard | ai | step 2 | `PR-RING, MO-MINT` |
| `audience_knows_from` | When the audience learns it, as a story point. | story_point | standard | ai | step 2 | `SC10 "Her face changes."` |
| `known_by` | Each character who knows it, and from when. | sub_parts; first part: id (CHARACTER); from: story_point; one line each | standard | ai | step 2 | `CH-SAYE \| from: SC10 "Nothing has happened to the mint."` |
| `mode` | How the fact works on the audience. | suspense, mystery, surprise, dramatic_irony | standard | ai | step 2 | `dramatic_irony` |

Status values: draft, approved, stale, omitted.

## CHAPTER: chapter

A prose chapter: its stub from step 1, its digest from step 2. ID: CP and 2 digits (`CP01`); the user sees it as chapter I. Lives in: 05 Story plan.md. Designed at step 2; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `title` | The chapter's heading. | text | quick | story; in a chat without code: ai | step 1 | `I. The Lamps Are Old` |
| `lines` | Its line range (an anchor pair in chat). | lines | quick | story; in a chat without code: ai | step 1 | `5-83` |
| `words` | Its word count. | number | quick | story; in a chat without code: ai | step 1 | `3512` |
| `first_line` | Its first line quoted, as proof it was read. The quote is matched within the chapter's lines, as a scene field is within its scene's lines. | quote | quick | ai | step 1 | `"To the one who keeps the lamps after me:"` |
| `last_line` | Its last line quoted, as proof it was read. The quote is matched within the chapter's lines, as a scene field is within its scene's lines. | quote | quick | ai | step 1 | `"nothing under any of it but the kept dark."` |
| `digest` | The chapter in at most 350 words (constant chapter_digest_words_max). | text | quick | ai | step 2 | `Nilay climbs to Kırk Oda and sits on the threshold at night to learn the air shaft's breathing; a warmth leans its weight on her shoulder.` |
| `people` | Characters in the chapter. | id_list; IDs of CHARACTER | quick | ai | step 2 | `CH-NILAY` |
| `places` | Places in the chapter. | text | quick | ai | step 2 | `Kırk Oda; the threshold` |
| `time_markers` | Words that fix time. | text | quick | ai | step 2 | `the climb up; night` |
| `pov` | Whose point of view the chapter holds. | id; IDs of CHARACTER | quick | ai | step 2 | `CH-NILAY` |
| `candidate` | A candidate scene with A3's five tests and a decision. | sub_parts; first part: text; lines: lines; kind: word (dramatized, narratized, inner, summary, iterative, letter, description); tests: text; decision: word (own_scene, fold, montage, voice_over, cut); becomes: id; one line each | quick | ai | step 2 | `the threshold at night \| lines: 73-81 \| kind: dramatized \| tests: 1 1 1 1 0 \| decision: own_scene \| becomes: SC05` |

Status values: draft, approved, stale, omitted.

## STRAND: strand

A line of events through a prose work. ID: ST- and 2 digits (`ST-01`); the user sees it as plain name. Lives in: 05 Story plan.md. Designed at step 2; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `name` | The strand's plain name. | text | quick | ai | step 2 | `the keeper's lamps` |
| `chapters` | The chapters it runs through. | id_list; IDs of CHAPTER | quick | ai | step 2 | `CP01, CP02, CP14` |
| `carries` | The cardinal events it carries. | id_list; IDs of CARDINAL | quick | ai | step 2 | `CF-01, CF-05` |
| `feeds` | What it feeds. | text | quick | ai | step 2 | `the ending` |
| `decision` | What the plan does with it. | keep, compress, composite, fold, cut | quick | ai | step 2 | `keep` |
| `reason` | Why. | text | quick | ai | step 2 | `it carries the ending` |
| `seconds` | Its planned screen seconds. | seconds | quick | ai | step 2 | `900` |

Status values: draft, approved, stale, omitted.

## CARDINAL: cardinal event

An event the story cannot lose (the deletion test). ID: CF- and 2 digits (`CF-05`); the user sees it as plain name. Lives in: 05 Story plan.md. Designed at step 2; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `event` | The event, one past-tense sentence. | text | quick | ai | step 2 | `Iona deleted the way home.` |
| `lines` | Its lines (or an anchor pair). | lines | quick | ai | step 2 | `1412` |
| `depends` | The cardinal events it depends on. | id_list; IDs of CARDINAL; also none | quick | ai | step 2 | `CF-02` |

Status values: draft, approved, stale, omitted.

## STYLE: style

How the whole film is made to appear. ID: None (`None`); the user sees it as None. Lives in: 06 World and style.md. Designed at step 3; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `medium` | What the film is made to look like. | live_action, 3d_animation, 2d_animation, stop_motion_look, painted, mixed | quick | user | checkpoint B | `live_action` |
| `style_words` | 8 to 15 plain descriptors pasted into every prompt (constant style_words_count). | text | quick | ai | step 3 | `photographic; clean, sharp highlights; plain practical light; muted colour; fine grain` |
| `texture` | Film texture. | sub_parts; first part: word (grain, halation, lens_character, softness, cadence); as: text; one line each | standard | ai | step 3 | `grain \| as: fine, even` |
| `named_reference_policy` | Never name films, directors or living artists in prompts (fixed). | describe_qualities_only | quick | code_state; in a chat without code: ai | step 3 | `describe_qualities_only` |
| `words_to_avoid` | Words this film's prompts never use. | text | quick | ai | step 3 | `cinematic, epic, futuristic` |
| `style_picture` | A picture fixing the style (chosen by D5's three-direction test). | file | add-on (A or C) | ai | add-on A (storyboards) | `18 Storyboard/Style test - A.png` |
| `provisional` | The style was chosen from words only and awaits D5's picture test. | yes_no; default yes | quick | code_state; in a chat without code: ai | step 3 | `yes` |

Status values: draft, approved, stale, omitted.

## WORLD: world

Where and when the story happens, and its local signals. ID: None (`None`); the user sees it as None. Lives in: 06 World and style.md. Designed at step 3; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `place` | The country, an invented place, or unstated. | text; pattern `^(named:[a-z_]+\|invented\|unstated)$` | quick | user | checkpoint B | `unstated` |
| `period` | When. | text | quick | user | checkpoint B | `present day` |
| `drives_on` | Which side of the road traffic drives on. | left, right, none | quick | ai | step 3 | `left` |
| `language` | The language spoken. | word | quick | ai | step 3 | `english` |
| `accents` | Accents heard (D17, B2 R19). | text | standard | ai | step 3 | `British English` |
| `signage` | What signs look like. | text | standard | ai | step 3 | `British road and building signs` |
| `emergency_lights` | Emergency vehicle lights. | text | standard | ai | step 3 | `blue flashing lights only` |
| `institutions` | Institutions seen or named. | text | standard | ai | step 3 | `a public hospital` |
| `money` | Money seen or named. | text | standard | ai | step 3 | `pounds` |
| `evidence` | Lines that point to the locale. | sub_parts; first part: lines; quote: quote; one line each | standard | ai | step 3 | `69 \| quote: "torch"` |
| `origin` | Whether the world is stated, inferred or invented. | story, inferred, invented | standard | ai | step 3 | `inferred` |

Status values: draft, approved, stale, omitted.

## RULE: story-world rule

A story-world rule and what it governs (mirror rules, text rules, titles, recurring devices). ID: WR- and capitals and hyphens (`WR-MIRROR`); the user sees it as plain name. Lives in: 06 World and style.md. Designed at step 3; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `kind` | What kind of rule. | world, mirror, text, titles, device, other | quick | ai | step 3 | `mirror` |
| `statement` | The rule in one sentence. | text | quick | ai | step 3 | `From "Her eyes open." the world is mirrored around Iona, Jude and Eli.` |
| `governs` | What the rule governs. | id_list; IDs of * | quick | ai | step 3 | `LOC-SAYE-KITCHEN, TX-GOODS-ONLY` |
| `era` | A stretch under one frame handedness (set through a CHOICE and its SETVALUE records). | sub_parts; first part: word; from: lines; to: lines; frame: word (original, reversed); one line each | quick | user | checkpoint B | `b \| from: 263 \| to: 1563 \| frame: original` |
| `exception` | An element that breaks the rule. | sub_parts; first part: id (*); reads: word (normal, mirrored); why: text; also none; one line each | standard | ai | step 3 | `PR-TOY-CARRIAGE \| reads: normal \| why: its Fs read as scripted` |
| `occurrences` | Recurring devices: where it occurs. | lines | quick | ai | step 3 | `60-83, 1400-1420` |
| `policy` | Recurring devices: how returns are handled. | open_only, open_and_close, every_return, episode_cold_open, template_refrain | quick | ai | step 3 | `open_and_close` |
| `template_setup` | Recurring devices: the shot used as the template. | id; IDs of SHOT; also none | quick | ai | step 3 | `SC05-SH010` |
| `varies` | Recurring devices: what varies on each return. | text | quick | ai | step 3 | `only the minutes change` |

Status values: draft, approved, stale, omitted.

## CHARACTER: character

A person or being the film shows more than once, with the design every prompt keeps. ID: CH- and capitals and hyphens (`CH-IONA`); the user sees it as plain name. Lives in: 07 Characters and voices.md. Designed at step 4; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `names` | Aliases: every name the story uses for the character. | text_list | quick | story (when character_has_cue); ai (when otherwise); in a chat without code: ai | step 1 | `DR SAYE, SAYE` |
| `tier` | How big the part is. | principal, minor, extra, non_human | quick | ai | step 4 | `principal` |
| `role` | The character's role in the story. | text | quick | ai | step 4 | `the doctor who has waited for them` |
| `life_want` | What they want in life. | text | standard | ai | step 4 | `to be believed` |
| `arc` | Where they start and end, and the turning scene. | sub_parts; start: text; end: text; turning_scene: id | standard | ai | step 4 | `start: certain \| end: shaken \| turning_scene: SC13` |
| `thesis` | The design idea in one sentence. | text | standard | ai | step 4 | `tidy grey control with one living thing that becomes her proof` |
| `evidence` | Lines the design rests on. | sub_parts; first part: lines; quote: quote; one line each | standard | ai | step 4 | `436 \| quote: "Saye's wedding ring. On her right hand."` |
| `fixed_description` | The words pasted into every prompt with them: 25-40 words for principals, 20-30 for minor characters (constant fixed_description_words); visible nouns only; no expression words; no real person. Locked once approved. | text | quick | ai | step 4 | `Dr Saye, a slight, upright woman in her fifties, short neat grey hair, a pale lined face, a charcoal wool cardigan over a white collared blouse, dark trousers, flat black shoes.` |
| `height_m` | Height. | metres | standard | ai | step 4 | `1.62` |
| `build` | Body build. | text | standard | ai | step 4 | `slight, upright` |
| `colour_identity` | The character's colour. | text | standard | ai | step 4 | `charcoal and white` |
| `tempo` | How fast they move and speak, in words. | text | standard | ai | step 4 | `slow and exact` |
| `speech` | How they talk. | sub_parts; sentences: text; contractions: yes_no; vocabulary: text | standard | ai | step 4 | `sentences: short \| contractions: no \| vocabulary: exact, clinical` |
| `lineup` | The six lineup columns as words, so code can compare principals (B5 R3; CRAFT-20). | sub_parts; height: word (short, average, tall); mass: word (slight, average, heavy); shape: word (round, square, triangle, long); value: word (dark, mid, light); colour: word; tempo: word (slow, medium, fast) | standard | ai | step 4 | `height: short \| mass: slight \| shape: long \| value: light \| colour: grey \| tempo: slow` |
| `face` | The face's three largest distinguishers (B5 R21). | text | standard | ai | step 4 | `deep lines beside the mouth; very straight brows; a narrow nose` |
| `movement` | Home, stress and break effort, each as body part, direction, speed and what stays still (B5 §5.1-5.4). | sub_parts; first part: word (home, stress, break); part: text; direction: text; speed: text; still: text; one line each | standard | ai | step 4 | `stress \| part: hands \| direction: inward \| speed: slow \| still: head` |
| `gesture` | One signature gesture with its script line (B5 R17). | sub_parts; first part: text; line: lines | standard | ai | step 4 | `a flat hand laid on things to test whether they will hold \| line: 69` |
| `status_play` | The status the character plays by default, and the beats where it flips (B5 R15-R16). Named status_play because every record already has a status field. | sub_parts; default: word (high, equal, low); flips: story_point_list | standard | ai | step 4 | `default: high \| flips: SC13 "You."` |
| `distance` | Default and closest distance to others, in metres, with the scenes that change them (B5 §5.5). | sub_parts; default_m: metres; closest_m: metres; changes: id_list | standard | ai | step 4 | `default_m: 1.5 \| closest_m: 0.5 \| changes: SC13` |
| `one_image` | The one image that sums the character up. | text | detailed | ai | step 4 | `a hand flat on a steel rail` |
| `expression` | The character's expression range, as movement, never bare emotion words. | text | detailed | ai | step 4 | `SC10-B07: jaw stops, brows draw together, eyes stay on Saye` |
| `skin_light` | How their skin is lit and named in prompts, written when casting is chosen (B2 R24); added to the look block of every LOOK with contrast high or extreme. | text | add-on (C) | ai | add-on C (prompts for AI video) | `a soft fill from the lamp side keeps her face readable in the dark room` |
| `voice` | Their voice (none for a character who never speaks). | id; IDs of VOICE; also none | standard | ai | step 4 | `VO-SAYE` |
| `likeness_basis` | The source of face and voice: invented by default (a small choice at step 4). | invented, self_consented, performer_consented; default invented | quick | user | step 4 | `invented` |
| `consent` | The consent record for a real face or voice. | id; IDs of RIGHTS; also none | add-on (C) | user | add-on C (prompts for AI video) | `none` |

Status values: draft, approved, stale, omitted.

## VOICE: voice

One character's voice: the fixed words for it, pitch, pace and how it is made (D3). ID: VO- and capitals and hyphens (`VO-SAYE`); the user sees it as plain name. Lives in: 07 Characters and voices.md. Designed at step 4; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `character` | Whose voice. | id; IDs of CHARACTER | standard | ai | step 4 | `CH-SAYE` |
| `voice_description` | The fixed words for the voice, 30-50 words (constant voice_description_words). | text | standard | ai | step 4 | `A low, even woman's voice in her fifties, British English, precise consonants, no contractions, unhurried, rarely rising at the end of a sentence; warmth held back until the last line.` |
| `pitch` | Pitch band. | low, low_mid, mid, mid_high, high | standard | ai | step 4 | `low_mid` |
| `pace_wps` | Words per second (default 2.5, constant speech_wps_default; weighted speakers slower). | words_per_second; default 2.5 | standard | ai | step 4 | `2.0` |
| `accent` | Accent, from WORLD. | text | standard | ai | step 4 | `British English` |
| `path_sound` | How each path sounds. | sub_parts; first part: word (earpiece, radio, intercom, recording, helmet_inside, phone, through_glass); treatment: text; also none; one line each | standard | ai | step 4 | `intercom \| treatment: small speaker, narrow band, slight crackle` |
| `source` | How the voice is made (D3): designed by default, a small choice at step 4, asked again at add-on C. | designed, user_recorded, actor_recorded, own_clone, consented_clone, native_draft; default designed | standard | user | step 4 | `designed` |
| `consent` | The consent record for a recorded or cloned voice. | id; IDs of RIGHTS; also none | add-on (C) | ai | add-on C (prompts for AI video) | `RT-004` |
| `tool` | The voice tool. | text | add-on (C) | ai | add-on C (prompts for AI video) | `a voice-design tool named in audio_models.json` |
| `provider_voice` | The tool's voice name or number. | text | add-on (C) | ai | add-on C (prompts for AI video) | `none` |
| `texture` | Voice texture. | text | add-on (C) | ai | add-on C (prompts for AI video) | `slightly dry, close` |
| `habits` | Voice habits. | text | add-on (C) | ai | add-on C (prompts for AI video) | `a short breath before answers` |

Status values: draft, approved, stale, omitted.

## LOCATION: place

A place, with a set plan in metres when step 4's rule needs one. ID: LOC- and capitals and hyphens (`LOC-SAYE-KITCHEN`); the user sees it as plain name. Lives in: 08 Places and things.md. Designed at step 4; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `headings` | The scene headings that use this place. | text | standard | story (when source_is_screenplay); ai (when source_not_screenplay); in a chat without code: ai | step 4 | `INT. SAYE'S HOUSE - KITCHEN - BEFORE DAWN` |
| `story_job` | What the place does in the story. | text | standard | ai | step 4 | `the first room of the mirrored world that is not a hospital` |
| `loudness` | A loud set (at most loud_sets_max) or a quiet one. | loud, quiet | standard | ai | step 4 | `quiet` |
| `room_sound` | The steady background sound here. | text | standard | ai | step 4 | `a fridge hum; a clock in the hall` |
| `anchor` | The place's anchor object or feature. | text | standard | ai | step 4 | `the kitchen table` |
| `exit` | An exit and where it leads. | sub_parts; first part: text; leads_to: text; one line each | standard | ai | step 4 | `back door \| leads_to: the garden` |
| `dressing` | What dresses the place. | text | standard | ai | step 4 | `a pot of mint on the windowsill and nothing else personal` |
| `plan_orientation` | The orientation the set plan is written in (default: that of the place's first appearance on screen). | original, reversed | standard | ai | step 4 | `original` |
| `size` | The room's size. | size | standard | ai | step 4 | `[6.0, 3.6, 2.5]` |
| `origin_corner` | The corner the plan measures from. | text | standard | ai | step 4 | `south-west inside corner` |
| `axes` | The plan's axes. | text | standard | ai | step 4 | `+x east, +y north` |
| `wild_walls` | Walls the camera may pass through. | text | standard | ai | step 4 | `west wall` |
| `object` | An object in the set plan. | sub_parts; first part: word; at: point; size: size; base: metres; material: text; meaning: text; furniture: word (seat, bed, none); one line each | standard | ai | step 4 | `TABLE \| at: [2.8, 1.8] \| size: [1.6, 0.9, 0.75] \| base: 0 \| material: wood \| meaning: the third thing \| furniture: none` |
| `mark` | A named mark where people stand. | sub_parts; first part: word; at: point; one line each | standard | ai | step 4 | `IONA_MARK \| at: [2.8, 2.55]` |
| `orientation` | Whether the place is seen in one mirror state only or both (5.6). | single, both | quick, worked out by code | code_derived | step 4 | `single` |

Status values: draft, approved, stale, omitted.

## PROP: thing

A thing the film shows more than once or at a turn. ID: PR- and capitals and hyphens (`PR-FLASK`); the user sees it as plain name. Lives in: 08 Places and things.md. Designed at step 4; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `names` | Names the story uses for the thing (each found in the story). | text_list | quick | ai | step 4 | `flask, the flask` |
| `category` | What kind of thing. | hero_prop, prop, set_dressing, vehicle, animal, weapon, consumable, document, wardrobe, practical_effect, visual_effect | quick | ai | step 4 | `hero_prop` |
| `kind` | The thing's job in the story. | emblem, action, plot_machinery, dressing | detailed | ai | step 4 | `plot_machinery` |
| `fixed_description` | The words pasted into every prompt with it. | text | standard | ai | step 4 | `a dented steel vacuum flask with a black screw cap, about 30 centimetres tall` |
| `real_size` | Its real size. | size | standard | ai | step 4 | `[0.09, 0.09, 0.30]` |
| `surface` | How its surface reads on camera. | ordinary, matte_black, clear, shiny, very_bright | detailed | ai | step 4 | `shiny` |
| `side` | Sided features of the thing. | sub_parts; first part: text; own: word (left, right); plot: yes_no; also none; one line each | standard | ai | step 4 | `dent \| own: left \| plot: no` |
| `text` | Text in picture on the thing. | id_list; IDs of TEXT; also none | standard | ai | step 4 | `none` |
| `first_seen` | Where it is first seen. | lines | standard | ai | step 4 | `398` |
| `motif` | The motif it carries. | id; IDs of MOTIF; also none | standard | ai | step 4 | `none` |
| `origin` | Whether the thing is in the story, inferred from it, or invented; an invented thing in frame must be listed in the scene's additions (5.2 origin, CRAFT-14). | story, inferred, invented | quick | ai | step 4 | `story` |

Status values: draft, approved, stale, omitted.

## TEXT: text in picture

Readable words inside the picture; never generated, always composited from a text graphic (K17). ID: TX- and capitals and hyphens (`TX-GOODS-ONLY`); the user sees it as plain name. Lives in: 08 Places and things.md. Designed at step 4; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `kind` | What kind of text. | sign, label, stencil, screen, visor, wrist, monitor, document, title_card, caption, timestamp | quick | ai | step 4 | `label` |
| `words` | The exact words. | text | quick | story (when text_in_story); ai (when otherwise); in a chat without code: ai | step 4 | `Goods only. No persons.` |
| `on` | What the text is on (none for a title card or caption laid over black or over the picture). | id; IDs of PROP, LOCATION, CAMERA, CHARACTER; also none | quick | ai | step 4 | `PR-CAGE` |
| `origin` | Whether the words are the story's or invented (needed by the words writer rule). | story, inferred, invented | quick | ai | step 4 | `story` |
| `words_from` | Origin story: the story line that writes the words, with the exact words quoted when the line holds more than the text; code copies the words from it into words (not needed when words is already there, as in a project adopted from a chat). | sub_parts; first part: lines; quote: quote; one line each | quick | ai | step 4 | `608 \| quote: "CONTROL"` |
| `reader` | Who reads it in the story. | id; IDs of CHARACTER; also none | standard | ai | step 4 | `CH-JUDE` |
| `plot_critical` | The audience must read it. | yes_no | standard | ai | step 4 | `yes` |
| `emphasis` | How loud it is, 0 to 3. | number; from 0 to 3 | standard | ai | step 4 | `2` |
| `method` | How it gets into the picture: composite (a text graphic laid in after, the default), background_blur (never read), or model_drawn (the video model draws it: only a single large letter or mark the shot is about, such as the toy carriage's F, checked in the take; GEN-06 allows it). | composite, background_blur, model_drawn | standard | ai | step 4 | `composite` |
| `lettering` | How the letters look (font style, colour, size). Named lettering because 'look' belongs to LOOK records. | text | detailed | ai | step 4 | `red stencil capitals on a white tag` |
| `animation` | How it moves, if it does. | text; also none | standard | ai | step 4 | `none` |
| `translate` | Whether it goes on the text-to-translate list. | yes_no | detailed | ai | step 4 | `yes` |

Status values: draft, approved, stale, omitted.

## MOTIF: motif

A thing that returns and gathers meaning. ID: MO- and capitals and hyphens (`MO-MINT`); the user sees it as plain name. Lives in: 08 Places and things.md. Designed at step 4; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `meaning` | What it comes to mean. | text | standard | ai | step 4 | `proof that the world is not the one she left` |
| `rank` | How much it carries (constant motif_spines_max). | spine, supporting, single_scene, minor, plot_machinery | standard | ai | step 4 | `supporting` |
| `channel` | Seen, heard or in the body. | visual, sound, body | standard | ai | step 4 | `visual` |
| `appearance` | Each appearance: a scene or story point (a shot from step 8). | sub_parts; first part: scene_or_story_point (SHOT); role: word (plant, develop, teach, reveal, payoff, coda); emphasis: number; sound_emphasis: number; rhyme_with: id; side: word (same, reversed); one line each | standard | ai | step 4 | `SC10 "Her face changes." \| role: payoff \| emphasis: 2` |
| `signature` | A sound motif's rhythm. | text; also none | standard | ai | step 4 | `none` |
| `direction` | Detailed register (B4): how the motif develops. | text | detailed | ai | step 4 | `from ordinary herb to proof` |
| `pole` | Detailed register: the pole of the core opposition it serves. | text | detailed | ai | step 4 | `the lost world` |
| `test_score` | Detailed register: B4's six tests passed, 0 to 6. | number; from 0 to 6 | detailed | ai | step 4 | `5` |
| `rule` | Detailed register: a rule for how it is shown. | text; one line each | detailed | ai | step 4 | `never lit as a symbol; always an ordinary plant` |
| `largest_payoff` | Detailed register: whether this is the film's largest payoff. | yes_no | detailed | ai | step 4 | `no` |

Status values: draft, approved, stale, omitted.

## CAMERA: in-story camera

A camera inside the story (security feeds, recordings). ID: CAM- and capitals and hyphens (`CAM-SHAFT-TOP`); the user sees it as plain name. Lives in: 08 Places and things.md. Designed at step 4; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `at` | Where it is. | text | standard | ai | step 4 | `high in the corner above the shaft` |
| `lens_mm` | Its lens. | millimetres | standard | ai | step 4 | `14` |
| `ratio` | Its frame shape. | text | standard | ai | step 4 | `4:3` |
| `fps` | Its frames per second. | number | standard | ai | step 4 | `15` |
| `overlays` | What its picture shows over the image. | text | standard | ai | step 4 | `a timestamp in the top corner` |
| `moves` | How it moves. | never, pan_only, operator | standard | ai | step 4 | `never` |
| `master_clip` | The shot or previs its footage comes from. | id; IDs of SHOT, PREVIS; also none | standard | ai | step 4 | `PV-SC06-MASTER-V01` |

Status values: draft, approved, stale, omitted.

## STATE: state

The state of a changeable person, thing or place from one line to the next state: costume, injury, condition, handedness. ID: the element's ID, .S and 2 digits (`CH-IONA.S02`); the user sees it as Iona, state 2: sleeve torn, palm skinned. Lives in: 09 Continuity.md. Designed at step 5; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `element` | Whose state. | id; IDs of CHARACTER, PROP, LOCATION | quick | ai | step 5 | `CH-IONA` |
| `from` | Where the state starts: a scene and a line (a quote anchor in chat). | sub_parts; first part: id (SCENE); line: lines | quick | ai | step 5 | `SC06 \| line: 263` |
| `cause` | The line that causes it. | sub_parts; first part: lines; quote: quote | standard | ai | step 5 | `263 \| quote: "Her eyes open."` |
| `state_line` | Words appended after the fixed description in prompts; no image-side words (SIDE-02). | text | quick | ai | step 5 | `sleeve torn at the elbow, palm skinned and dirty` |
| `changes` | What differs from the last state. | text | standard | ai | step 5 | `the sleeve tore in the fall` |
| `side` | Sided features in this state, in own terms. | sub_parts; first part: text; own: word (left, right); plot: yes_no; also none; one line each | standard | ai | step 5 | `palm graze \| own: right \| plot: yes` |
| `handedness` | In a mirror story: the element's story state. | original, reversed | standard | ai | step 5 | `original` |
| `pictures_needed` | Reference views needed for this state. | text | add-on (A or C) | ai | step 5 | `front, three-quarter, right hand close` |
| `origin` | Whether the state is stated, inferred or invented. | story, inferred, invented | quick | ai | step 5 | `story` |
| `until` | Where the state ends (the next state's start). | text | quick, worked out by code | code_derived | step 5 | `SC22 \| line: 1265` |

Status values: draft, approved, stale, omitted.

## CAMSYS: camera system

The film's camera system: frame shape reason, lenses, baseline, banned choices, the one break. ID: None (`None`); the user sees it as None. Lives in: 10 Film rules.md. Designed at step 6; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `frame_shape_why` | The story reason for the frame shape (B1 P3). | text | standard | ai | step 6 | `people face each other across glass and tables` |
| `lens_type` | Lens type. | spherical, anamorphic | standard | ai | step 6 | `spherical` |
| `lens_family` | The lenses allowed. | number_list | standard | ai | step 6 | `25, 35, 50, 85` |
| `normal_lens_mm` | The normal lens, the default for lens_mm (5.4 rule 11). | millimetres | standard | ai | step 6 | `50` |
| `step_change` | When the lens family changes. | sub_parts; from: id; family: number_list; why: text; also none; one line each | standard | ai | step 6 | `from: SC26 \| family: 18, 25 \| why: the crossing is played wide` |
| `default_height` | The baseline camera height. | text | quick | ai | step 6 | `the eye height of the person the scene belongs to` |
| `default_move` | The baseline camera move. | static | quick | ai | step 6 | `static` |
| `banned` | Choices this film never makes. | sub_parts; first part: text; why: text; also none; one line each | quick | ai | step 6 | `slow_motion \| why: playback is always real time (K30)` |
| `camera_speed` | Playback speed. | real_time | quick | ai | step 6 | `real_time` |
| `break` | The camera's one break. | sub_parts; first part: scene_or_story_point; what: text; because: text | standard | ai | step 6 | `SC26 "She pushes gently away from the rail." \| what: the camera floats free for the first time \| because: PLAN` |
| `time_rule` | How expanded action is built. | text | standard | ai | step 6 | `expanded time from overlapping real-time slices of one master previs, never slow motion (K20)` |

Status values: draft, approved, stale, omitted.

## CAMRULE: character camera rule

How the camera treats one character. ID: CR- and capitals and hyphens (`CR-ELI`); the user sees it as plain name. Lives in: 10 Film rules.md. Designed at step 6; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `character` | The character. | id; IDs of CHARACTER | standard | ai | step 6 | `CH-ELI` |
| `in_control` | How the camera treats them when in control. | text | standard | ai | step 6 | `static, level, at his eye height` |
| `losing_control` | How the camera treats them when losing control. | text | standard | ai | step 6 | `wider, held longer` |
| `never` | What the camera never does to them. | text_list | standard | ai | step 6 | `push_in` |
| `closest` | Their closest size and where it is spent. | sub_parts; first part: word (extreme_wide, wide, medium_wide, medium, medium_close_up, close_up, extreme_close_up, insert); at: story_point | standard | ai | step 6 | `close_up \| at: SC13 "Now he looks at her."` |
| `limit_before` | The closest size allowed before closest is spent. | extreme_wide, wide, medium_wide, medium, medium_close_up, close_up, extreme_close_up, insert | standard | ai | step 6 | `medium_close_up` |
| `eyeline` | Their eyeline rule. | text | standard | ai | step 6 | `his near-lens look is saved for SC13` |
| `because` | The records behind the rule. | id_list; IDs of * | standard | ai | step 6 | `CH-ELI, PLAN` |

Status values: draft, approved, stale, omitted.

## RESERVE: saved choice

A choice saved for special moments, with its uses rationed. Always includes the two film-level reserves: the non-insert extreme close-up and the push-in. ID: RC- and 2 digits (`RC-01`); the user sees it as saved choice 1. Lives in: 10 Film rules.md. Designed at step 6; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `choice` | The saved choice. | text | quick | ai | step 6 | `the non-insert extreme close-up (a film-level saved choice)` |
| `match` | How code recognises a use: <field> = <value>, or manual. | text; pattern `^([a-z_]+ = [a-z0-9_.]+\|manual)$` | quick | ai | step 6 | `size = extreme_close_up` |
| `max_uses` | Most uses: a whole number, 1_per_scene, or share with a fraction of scenes. | sub_parts; first part: text; fraction: number | quick | ai | step 6 | `3` |
| `allowed_in` | Where it may be used. The checker reads only scene IDs here (SC13); words are for people. | text | quick | ai | step 6 | `main turns only; the first in SC13 (K05)` |
| `never_on` | Where it may never be used. | id_list; IDs of *; also none | quick | ai | step 6 | `CH-ELI` |
| `because` | The records behind it. | id_list; IDs of * | quick | ai | step 6 | `PLAN, LADDER, CR-ELI` |

Status values: draft, approved, stale, omitted.

## LENS: lens exception

A lens outside the family and where it is allowed. ID: LX- and 2 digits (`LX-01`); the user sees it as lens exception 1. Lives in: 10 Film rules.md. Designed at step 6; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `mm` | The lens. | millimetres | standard | ai | step 6 | `85` |
| `only_in` | Where it is allowed: setups or scenes. | id_list; IDs of SETUP, SCENE | standard | ai | step 6 | `SC10-SU01` |
| `why` | Why. | text | standard | ai | step 6 | `the reflection two-shot needs the camera well back through the wild wall` |
| `because` | The records behind it. | id_list; IDs of * | standard | ai | step 6 | `RC-01` |

Status values: draft, approved, stale, omitted.

## LOOK: look

The light, colour and texture of a place at a time; its look block is pasted word for word into every prompt there. ID: LK- and capitals and hyphens (`LK-SAYE-KITCHEN-NIGHT`); the user sees it as plain name. Lives in: 10 Film rules.md. Designed at step 6; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `for` | The place. | id; IDs of LOCATION | standard | ai | step 6 | `LOC-SAYE-KITCHEN` |
| `time` | The time. | text | standard | ai | step 6 | `before dawn` |
| `look_block` | The 2-3 sentences (at most look_block_words_max words) pasted into every prompt there. | text | standard | ai | step 6 | `A bare kitchen before dawn. The only warm light is a small lamp; blue dark stands in the window. Pale walls, one green plant.` |
| `main_light` | The main light, placed in the room so its frame side is derived per shot and era. | sub_parts; first part: text; colour: text; quality: word (hard, soft); from: text | standard | ai | step 6 | `Iona's lamp \| colour: warm \| quality: soft \| from: TABLE` |
| `neutral_white` | What reads as white. | text | standard | ai | step 6 | `the lamp` |
| `contrast` | The contrast band. | low, medium, medium_high, high, extreme | standard | ai | step 6 | `medium_high` |
| `fill` | How much fill. | none, low, medium, high | standard | ai | step 6 | `low` |
| `stays_dark` | What stays dark. | text | standard | ai | step 6 | `the hall door and the ceiling` |
| `palette` | The colours. | text | standard | ai | step 6 | `grey, white, one green` |
| `accent_allowed` | The one accent allowed. | text | standard | ai | step 6 | `the mint's green` |
| `light_cue` | A light change at a story point. | sub_parts; first part: story_point; change: text; why: text; also none; one line each | standard | ai | step 6 | `SC10 "She picks up her phone." \| change: the phone's screen lights Saye's hand \| why: the story writes the phone` |
| `style_picture` | A picture fixing this look. | file | add-on (A or C) | ai | add-on A (storyboards) | `18 Storyboard/Look - kitchen.png` |

Status values: draft, approved, stale, omitted.

## VISUAL: visual plan

The colour-script row and visual-structure plan for a sequence. ID: VS- and the sequence ID (`VS-SQ03`); the user sees it as plain name. Lives in: 10 Film rules.md. Designed at step 6; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `sequence` | The group of scenes. | id; IDs of SEQUENCE | standard | ai | step 6 | `SQ03` |
| `frame_value` | How bright the frames are, 1 to 5. | number; from 1 to 5 | standard | ai | step 6 | `3` |
| `saturation` | Colour strength, 1 to 5. | number; from 1 to 5 | standard | ai | step 6 | `2` |
| `temperature` | Warm or cool. | warm, neutral, cool, mixed | standard | ai | step 6 | `mixed` |
| `dominant` | The main colour. | word | standard | ai | step 6 | `grey` |
| `accent` | The accent colour. | also none | standard | ai | step 6 | `green` |
| `main_light` | Hard or soft light. | hard, soft, mixed | standard | ai | step 6 | `soft` |
| `contrast` | The contrast band. | low, medium, medium_high, high, extreme | standard | ai | step 6 | `medium_high` |
| `exit` | How the group hands on to the next. | text | standard | ai | step 6 | `cut to black and the title card` |
| `sub_row` | A scene-level colour row inside the group. | sub_parts; first part: id (SCENE); frame_value: number; saturation: number; temperature: word (warm, neutral, cool, mixed); dominant: word; accent: word; contrast: word (low, medium, medium_high, high, extreme); one line each | detailed | ai | step 6 | `SC10 \| frame_value: 3 \| saturation: 2 \| temperature: mixed \| dominant: grey \| accent: green \| contrast: medium_high` |
| `space` | The kind of space (visual structure). | deep, flat, limited, ambiguous | standard | ai | step 6 | `limited` |
| `component` | The visual-structure plan per component. motion replaces the research's 'movement' (word list 5.7). | sub_parts; first part: word (space, line, shape, tone, colour, motion, rhythm); plan: word (hold, progress, contrast); why: text; one line each | standard | ai | step 6 | `space \| plan: contrast \| why: the kitchen is flat until the reflection two-shot opens it` |
| `counterpoint` | A counterpoint to the scene's feeling, or none. | text; also none | standard | ai | step 6 | `none` |

Status values: draft, approved, stale, omitted.

## SOUNDPLAN: sound plan

The film's music policy, voice policy, device budget and planned ruptures. ID: None (`None`); the user sees it as None. Lives in: 10 Film rules.md. Designed at step 6; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `music_policy` | Music in the finished film (checkpoint B, default none for The Catch). | none, sparse, scored, source_only | quick | user | checkpoint B | `none` |
| `clip_audio` | No music in any clip (fixed). | text | quick | code_state; in a chat without code: ai | step 6 | `No music in any clip.` |
| `voice_policy` | How voices may be made (a small choice at step 6; asked again at add-on C). | designed_only, designed_plus_own_clone, designed_plus_consented_clones; default designed_only | quick | user | step 6 | `designed_only` |
| `device_budget` | Editor-made devices allowed (constant device_budget_short). | sub_parts; first part: word (cut_to_black, true_silence, freeze); max: number; one line each | standard | ai | step 6 | `cut_to_black \| max: 2` |
| `rupture_plan` | Planned ruptures. | sub_parts; first part: id (SCENE); device: text; also none; one line each | standard | ai | step 6 | `SC26 \| device: drop_out` |
| `loudness_target` | Delivery loudness. | text | detailed | ai | step 6 | `-23 loudness units full scale, integrated, for broadcast` |

Status values: draft, approved, stale, omitted.

## LADDER: ladder

Each scene's main turn with planned size and hold; the ladder escalates by size and hold together. ID: None (`None`); the user sees it as None. Lives in: 10 Film rules.md. Designed at step 6; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `rung` | One scene's main turn: a story point (code adds the resolved beat at step 7), planned size and hold. | sub_parts; first part: story_point; size: word (extreme_wide, wide, medium_wide, medium, medium_close_up, close_up, extreme_close_up, insert); hold: word (short, medium, long, hold); why: text; one line each | standard | ai | step 6 | `SC10 "Her face changes." \| size: close_up \| hold: long \| why: the turn happens inside her mouth` |

Status values: draft, approved, stale, omitted.

## FINDING: finding

A problem found, with its fix. ID: FIND- and 3 digits (`FIND-004`); the user sees it as plain words. Lives in: 12 Whole-film check.md, 13 Health check.md. Designed at step 9; needed from quick depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `record` | The record with the problem. | id; IDs of * | quick | code_state (when checker_finding); ai (when otherwise) | step 9 | `SC10-SH160` |
| `rule` | The check ID or the question. | text | quick | code_state (when checker_finding); ai (when otherwise) | step 9 | `CRAFT-19` |
| `evidence` | What shows the problem. | text | quick | code_state (when checker_finding); ai (when otherwise) | step 9 | `size, light and sound all change on SC10-B07` |
| `fix` | The fix. | text | quick | code_state (when checker_finding); ai (when otherwise) | step 9 | `keep the light as_look on B07` |
| `source` | Who found it. | checker, film_pass, review, user | quick | code_state (when checker_finding); ai (when otherwise) | step 9 | `checker` |
| `status` | open, fixed or accepted. | open, fixed, accepted | quick | ai | step 9 | `fixed` |
| `reason` | Why it was accepted, or how it was fixed. | text | quick | ai | step 9 | `fixed by keeping the light as_look` |

Status values: open, fixed, accepted.

## REVIEW: review

Judge answers and rubric scores for a scene or the film. ID: RV- and a scene ID, or RV-FILM (`RV-SC10`); the user sees it as plain words. Lives in: 13 Health check.md. Designed at step 10; needed from standard depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `scope` | A scene or the film. | text | standard | ai | step 10 | `SC10` |
| `answer` | One yes/no question answered against the story. | sub_parts; first part: text; answer: yes_no; evidence: text; one line each | standard | ai | step 10 | `Does Iona's face change before she says 'Not mint.' (l.454-463)? \| answer: yes \| evidence: SH150 moment 4-6` |
| `score` | A rubric criterion's score (reference/05). | sub_parts; first part: number; score: number; evidence: text; one line each | standard | ai | step 10 | `3 \| score: 2 \| evidence: one turn shot per turn` |

Status values: draft, approved, stale, omitted.

## PIC: picture job

One picture job: the shot or element state it is for. ID: PIC-, the shot or element state, -, the use in capitals, - and 2 digits (`PIC-SC10-SH150-START-01`); the user sees it as plain words. Lives in: 18 Storyboard/Storyboard frames.md, 20 Prompts for AI video/Pictures.md. Designed at add-on A (storyboards); needed from add-on depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `for` | The shot or element state it is for. | id; IDs of SHOT, STATE, CHARACTER, PROP, LOCATION | add-on | ai | add-on A (storyboards) | `SC10-SH150` |
| `use` | The kind of picture job. | storyboard, start, end, pinned, reference, plate, style, layout | add-on | ai | add-on A (storyboards) | `start` |
| `moment` | Which instant of the shot. | start, middle, end | add-on | ai | add-on A (storyboards) | `start` |
| `model` | The exact model name. | text | add-on | ai | add-on A (storyboards) | `the exact name in image_models.json` |
| `references` | Reference pictures attached, each with its job. | sub_parts; first part: file; job: word (identity, costume, set, prop, layout); one line each | add-on | ai | add-on A (storyboards) | `Reference pictures/Iona - state 2 - front.png \| job: identity` |
| `file` | The picture file. | file | add-on | ai | add-on A (storyboards) | `20 Prompts for AI video/Reference pictures/Scene 10 - shot 150 - start 01.png` |
| `checks` | Yes/no checks on the picture. | sub_parts; first part: text; answer: yes_no; one line each | add-on | ai | add-on A (storyboards) | `Is the ring on the hand that looks like her right? \| answer: yes` |
| `approved` | Approved: the AI sets storyboard frames approved when every check passes; the user approves the rest. | yes_no | add-on | ai (when storyboard_frame); user (when otherwise) | add-on A (storyboards) | `yes` |
| `cost_usd` | What it cost. | dollars | add-on | ai | add-on A (storyboards) | `0.04` |

Status values: draft, approved, stale, omitted.

## PREVIS: grey preview job

One previs job: its shot, a master (PV-SC06-MASTER) or a location. ID: PV-, the shot (or SCNN-MASTER, or a location), -V and 2 digits (`PV-SC10-SH080-V01`); the user sees it as try 1. Lives in: 19 Grey previews/Grey preview jobs.md. Designed at add-on B (grey previews); needed from add-on depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `for` | Its shot, master or location. | id; IDs of SHOT, LOCATION; also <scene>-MASTER | add-on | code_state (when previs_stub); ai (when otherwise) | add-on B (grey previews) | `SC10-SH080` |
| `level` | The C4 level, 0 to 5. | number; from 0 to 5 | add-on | code_state (when previs_stub); ai (when otherwise) | add-on B (grey previews) | `2` |
| `standin_level` | Stand-in detail, 1 to 5. | number; from 1 to 5 | add-on | ai | add-on B (grey previews) | `1` |
| `route` | The route into video (C4 §6): 1 start and end pictures from grey stills, 2 depth guide video, 3 grey reference video, 5 layers composited. | number; 1, 2, 3, 5 | add-on | ai | add-on B (grey previews) | `1` |
| `extras` | The fragment the AI writes for what is not automatic. | file; also none | add-on | ai | add-on B (grey previews) | `19 Grey previews/extras/SC10-SH080.json` |
| `stills` | Frames saved as stills. | number_list | add-on | ai | add-on B (grey previews) | `1, 97, 216` |
| `approved` | yes, no, or auto (not framing-critical, BLOCKING OK and facings within facing_tolerance_deg). | yes, no, auto | add-on | user (when framing_critical); code_state (when otherwise) | add-on B (grey previews) | `auto` |
| `plan_file` | The compiled plan file. | file | add-on, worked out by code | code_derived | add-on B (grey previews) | `For machines - do not edit/previs plans/SC10-SH080.json` |
| `blocking` | The blocking check result. | text | add-on, worked out by code | code_derived | add-on B (grey previews) | `BLOCKING OK` |

Status values: draft, approved, stale, omitted, planned.

## TAKE: take

One generated take. ID: TK-, the clip ID, -T and 2 digits (`TK-SC10-SH150.1-T03`); the user sees it as take 3. Lives in: 20 Prompts for AI video/Takes.md. Designed at add-on C (prompts for AI video); needed from add-on depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `clip` | The clip. | id; IDs of CLIP | add-on | ai | add-on C (prompts for AI video) | `SC10-SH150.1` |
| `model` | The exact model name with its date. | text | add-on | ai | add-on C (prompts for AI video) | `seedance-2.5 (model facts 2026-09-27)` |
| `route` | How it was made. | text | add-on | ai | add-on C (prompts for AI video) | `start picture and prompt` |
| `inputs` | The files sent. | text_list | add-on | ai | add-on C (prompts for AI video) | `Scene 10 - shot 150 - start 01.png` |
| `seed` | The seed. | number; also none | add-on | ai | add-on C (prompts for AI video) | `41877` |
| `settings` | The settings. | text | add-on | ai | add-on C (prompts for AI video) | `17 s, 720p, 21:9` |
| `cost_usd` | What it cost. | dollars | add-on | ai | add-on C (prompts for AI video) | `5.10` |
| `file` | The take file. | file | add-on | ai | add-on C (prompts for AI video) | `Scene 10 - shot 150 - take 03.mp4` |
| `review` | Yes/no questions on the take. | sub_parts; first part: text; answer: yes_no; evidence: text; one line each | add-on | ai | add-on C (prompts for AI video) | `Only her mouth moves, and only at 6-8 s? \| answer: yes \| evidence: watched twice` |
| `kept` | Whether the user keeps the take (checkpoint E). | yes_no | add-on | user | add-on C (prompts for AI video) | `yes` |
| `refusals` | How many times the model refused. | number | add-on | ai | add-on C (prompts for AI video) | `0` |

Status values: draft, approved, stale, omitted.

## VOICETAKE: voice take

One voice take for one speech. ID: VT-, the speech ID, -T and 2 digits (`VT-SC10-D11-T01`); the user sees it as take 1. Lives in: 20 Prompts for AI video/Voices.md. Designed at add-on C (prompts for AI video); needed from add-on depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `speech` | The speech. | id; IDs of SPEECH | add-on | ai | add-on C (prompts for AI video) | `SC10-D11` |
| `voice` | The voice. | id; IDs of VOICE | add-on | ai | add-on C (prompts for AI video) | `VO-IONA` |
| `delivery` | Delivery in up to 8 words. | text | add-on | ai | add-on C (prompts for AI video) | `unsteady, quiet, testing the word` |
| `tts_text` | The same words with the voice tool's tags. | text | add-on | ai | add-on C (prompts for AI video) | `[unsteady] Not mint.` |
| `tool` | The voice tool. | text | add-on | ai | add-on C (prompts for AI video) | `the exact name in audio_models.json` |
| `file` | The audio file. | file | add-on | ai | add-on C (prompts for AI video) | `Voices/Scene 10 - speech 11 - take 01.wav` |
| `verdict` | The user's verdict. | pick, keep, reject | add-on | user | add-on C (prompts for AI video) | `pick` |
| `cost_usd` | What it cost. | dollars | add-on | ai | add-on C (prompts for AI video) | `0.02` |
| `words_match` | Whether the transcript matches the speech's words. | yes_no | add-on, worked out by code | code_derived | add-on C (prompts for AI video) | `yes` |

Status values: draft, approved, stale, omitted.

## FINISH: finishing job

One finishing job, created from shots by code and edited by the AI. ID: FX-, the shot ID, - and 2 digits (`FX-SC10-SH080-01`); the user sees it as plain words. Lives in: 21 Edit and finishing/Finishing jobs.md. Designed at add-on D (edit and finishing); needed from add-on depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `shot` | The shot. | id; IDs of SHOT | add-on | code_state; in a chat without code: ai | add-on D (edit and finishing) | `SC10-SH080` |
| `operation` | The operation. | flip, composite, crop, speed, upscale, deflicker, grain, grade, title, lip_sync, voice_path | add-on | code_state; in a chat without code: ai | add-on D (edit and finishing) | `flip` |
| `tool` | The tool. | text | add-on | ai | add-on D (edit and finishing) | `ffmpeg` |
| `inputs` | The input files. | text_list | add-on | ai | add-on D (edit and finishing) | `Scene 10 - shot 080 - take 02.mp4` |
| `output` | The output file. | file | add-on | ai | add-on D (edit and finishing) | `Scene 10 - shot 080 - flipped.mp4` |
| `done` | Whether it is done. | yes_no | add-on | ai | add-on D (edit and finishing) | `no` |

Status values: draft, approved, stale, omitted.

## MUSIC: music cue

A music cue (only if the policy is sparse or scored). ID: MU- and 2 digits (`MU-01`); the user sees it as plain words. Lives in: 21 Edit and finishing/Finishing jobs.md. Designed at add-on D (edit and finishing); needed from add-on depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `in` | Where it starts: a shot or beat. | id; IDs of SHOT, BEAT | add-on | ai | add-on D (edit and finishing) | `SC26-SH040` |
| `out` | Where it ends: a shot or beat. | id; IDs of SHOT, BEAT | add-on | ai | add-on D (edit and finishing) | `SC27-SH120` |
| `function` | What the cue does. | text | add-on | ai | add-on D (edit and finishing) | `carries the crossing without stating the feeling` |
| `must_not` | What it must not do. | text | add-on | ai | add-on D (edit and finishing) | `state the subtext; sit under dialogue` |
| `source` | Where the music comes from. | score, library, ai | add-on | ai | add-on D (edit and finishing) | `score` |
| `licence` | Its rights record. | id; IDs of RIGHTS | add-on | ai | add-on D (edit and finishing) | `RT-006` |

Status values: draft, approved, stale, omitted.

## RIGHTS: rights record

A rights or licence record (D4). ID: RT- and 3 digits (`RT-001`); the user sees it as plain words. Lives in: 22 Rights and credits.md. Designed at step 0; needed from add-on depth.

| Field | Meaning | Values | Depth | Writer | Filled at | Example |
|---|---|---|---|---|---|---|
| `subject` | What the rights cover. | source, voice, likeness, music, font, stock, model_terms | add-on | user | step 0 | `source` |
| `clearance` | What state the rights are in. Named clearance because every record already has a status field. | text | add-on | user | step 0 | `the author's own work` |
| `holder` | Who holds the rights (kept locally, never uploaded). | text | add-on | user | step 0 | `the author` |
| `licence` | The licence file. | file; also none | add-on | user | add-on C (prompts for AI video) | `none` |
| `evidence` | What shows the rights. | text | add-on | ai | add-on C (prompts for AI video) | `the user said: It's mine` |
| `commercial_ok` | Whether commercial use is allowed. | yes, no, check | add-on | user | add-on C (prompts for AI video) | `check` |
| `attribution` | The credit line required. | text | add-on | ai | add-on C (prompts for AI video) | `none` |
| `disclosure` | The disclosure line for AI-made pictures. | text | add-on | ai | add-on C (prompts for AI video) | `Made with the help of AI picture and video tools.` |

Status values: draft, approved, stale, omitted.

## Conditions

The names used in "when" above.

| Condition | Meaning |
|---|---|
| `source_is_screenplay` | PROJECT.source_kind is screenplay. |
| `source_not_screenplay` | PROJECT.source_kind is not screenplay (prose, stage play, treatment, comic or game script, mixed): scenes come from the step outline. |
| `compressing` | The user set a runtime target shorter than the story as written, or the source is prose (step 2 compression plan). |
| `character_has_cue` | The character speaks: code found a cue for it in the story. |
| `set_plan_exists` | The scene's location has a set plan (LOCATION size, object and mark items). |
| `set_plan_needed` | Step 4's rule: the place is used by a shot likely to need previs level 2 or more, a reflection or glass shot, or three or more people in one space. |
| `action_scene` | The scene is tagged action. |
| `tag_three_or_more` | The scene is tagged three_or_more. |
| `turn_beat` | The beat's turn is not none. |
| `turn_or_intense_beat` | The beat's turn is not none, or its beat_intensity is 4 or more. |
| `dialogue_pass_beat` | At standard: a turn beat, a beat with a flagged line, a beat where a fact is revealed, a refusal, or a line the plan names. At detailed: every beat. |
| `principal` | CHARACTER.tier is principal. |
| `mirror_rule_exists` | The project has a RULE whose kind is mirror. |
| `mirror_rule` | This RULE's kind is mirror. |
| `device_rule` | This RULE's kind is device (a recurring device in prose). |
| `fact_mode_needs_record` | FACT.mode is suspense, mystery or dramatic_irony (about 5-15 in a film); every fact at detailed. |
| `fact_element_before_reveal` | A FACT's element is in the scene before its reveal (audience_knows_from). |
| `glass_in_frame` | A glass surface is in frame. |
| `eyeline_set` | The subject item has an eyeline. |
| `subject_moves` | The subject moves in the frame. |
| `later_beat_saves_behaviour` | A later beat saves a visible behaviour (for example SC13's "Now he looks at her."). |
| `overlapping_slices` | The scene's time_treatment is overlapping_slices. |
| `match_cut_or_continuous_action` | The join is a match cut or the scene is continuous action. |
| `cut_is_split` | The CUT type is j_cut or l_cut. |
| `cut_has_black` | The CUT type is cut_to_black, fade or freeze. |
| `cut_is_match` | The CUT type is match_cut. |
| `reserved_choice` | The value is used under a saved choice (RESERVE). |
| `presentation_on_device` | SCENE.presentation is on_screen or recording. |
| `choice_answered` | CHOICE.status is answered. |
| `rights_subject_source` | RIGHTS.subject is source (the story itself). |
| `storyboard_frame` | PIC.use is storyboard. |
| `framing_critical` | The PREVIS record's shot has framing_critical: yes. |
| `previs_stub` | The PREVIS record is a stub code created (status: planned). |
| `checker_finding` | FINDING.source is checker. |
| `text_in_story` | The TEXT words are written in the story. |
| `depth_detailed` | The project's (or the scene's) depth is detailed. |
| `depth_below_detailed` | The project's (or the scene's) depth is quick or standard. |
| `otherwise` | None of the other conditions in the same writer_when list holds. |
| `when_used` | Written only when the thing it records exists (a departure, a flaw, a pov break); the checker never asks for it. |
| `casting_chosen` | Casting (the appearance of the people who play the characters) has been chosen in add-on C. |
| `music_policy_allows_cues` | SOUNDPLAN.music_policy is sparse or scored. |
| `filmed_shot` | The SHOT kind is not card or black: a camera films it (a title card or black has no setup, height, lens or focus). |
| `choice_settled` | CHOICE.status is answered or defaulted. |
