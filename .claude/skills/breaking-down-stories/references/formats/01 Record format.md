# Record format

Every numbered file in a project stores its records in "record text": plain lines that people can read and code can check. This page is the whole grammar (rules G1 to G13), three examples, and the ten mistakes that come up most, with their fixes. Field names, kinds and allowed values live in `_config/schema/schema.json`; `references/formats/03 Field guide.md` lists them in words.

## What you most often need

This short list was the section "Records: what you most often need" of `SKILL.md`.

- The grammar is on this page (G1 to G13): `### TYPE ID title`; `- field: value`; named sub-parts after ` | `; `none` empty, `open` undecided, `auto` code's choice; `> ` a note; one END line, `END OF FILE | <what the file holds> | <n> records`.
- Never put a shortening marker ("...", "etc.", "same as above") inside a record (G11), or split a record across replies.
- Field names and values come only from `_config/schema/schema.json`; words from `references/formats/02 Word list.md`; numbers by name from `_config/rules/constants.json` (without code, the last table of `references/formats/06`).
- Code issues scene, chapter and speech IDs, and a block for the rest (beats SC10-B01 to SC10-B30; shots SC10-SH010 to SC10-SH400 in tens).
- Before step 7, a moment inside a scene is a story point: the scene ID and a quote anchor (`SC24 "She deletes the way home."`).
- When two rules disagree, the higher in `references/formats/04 Rule order.md` wins; the `why` says which.

## Example 1: one record

```
### STATE CH-IONA.S02 Sleeve torn, palm skinned
- element: CH-IONA
- from: SC07 | line: 302
- cause: 302 | quote: "what is left of her shirt sleeve"
- state_line: one shirt sleeve torn away, palm skinned
- changes: the sleeve is gone, first seen here; the palm was skinned on the sill in scene 6
- side: skinned palm | own: right | plot: yes
- handedness: original
- origin: story
> Own right is a default (K26): the story does not say which hand.
```

A heading line names the record type, its ID and a plain title. Each field is one line: a dash, the field name, a colon, the value. A field with several parts (`side`) has a main value first and then named parts, each after ` | `. The `> ` line is a note (G8).

## The grammar

**G1. What counts.** A record file is UTF-8 Markdown. Only record headings, field lines inside a record, and the END line mean anything to the parser. Every other line (the plain part, titles, tables, paragraphs, the check table after a `---` line) is free text, kept and ignored.

**G2. Headings.** A record starts `### <TYPE> <ID> <optional plain title>`. TYPE is an upper-case word from the schema. The ID matches its type's pattern (`SC10-SH150`, `CH-IONA`, `CHOICE-021`). Singleton types (PLAN, STYLE, WORLD, CAMSYS, SOUNDPLAN, LADDER) have no ID: `### PLAN`. The title is free text after the ID.

**G3. Where a record ends.** At the next line starting with `#`, at a line `---`, or at the END line.

**G4. Field lines.** A field is one line: `- <field>: <value>`. Field names are lowercase snake_case plain words from the schema. Names are read in lower case, spaces and hyphens as underscores (`- Screen time: 15` is `screen_time`, a logged tidy fix).

**G5. Values.** A value is one line. Its kind comes from the schema:

| Kind | How to write it | Example |
|---|---|---|
| text | words to the end of the line; ` \| ` is not allowed inside | `Iona's body admits what her words denied.` |
| word | one allowed value, lowercase snake_case; case, spaces and hyphens are forgiven | `medium_close_up` ("medium close-up" is read the same) |
| number | digits; the unit is in the field name (`_s` seconds, `_m` metres, `_mm` millimetres, `_usd` dollars, `_wps` words per second) | `15` |
| yes_no | yes or no | `yes` |
| id, id_list | one ID; IDs separated by commas (a comma inside double quotes does not split) | `SC10-B07, SC10-V1, MO-MINT` |
| id_range | first and last joined by two full stops | `SC07..SC10` |
| lines | line numbers and ranges, or a quote anchor: one quoted string for one line, or two joined by `to` | `402, 449-463` or `"Iona chews it." to "street signs either."` |
| story_point | a moment inside a scene before its beats exist: scene ID and a quote anchor; from step 7 a beat ID also works | `SC24 "She deletes the way home."` |
| charge | a value's charge: `---` `--` `-` `0` `+` `++` `+++`; the sign is the direction | `---` |
| point, size | `[x, y]` or `[x, y, z]` in metres; a box `[w, d, h]` | `[2.8, 2.55]` |
| span | `t0-t1` seconds inside a shot | `0-4` |
| because_list | the ID of any story record (scene, beat, value, character, state, place, prop, text, motif, rule, plan, camera rule, saved choice, look, fact, plant), `line:NNN` or `line: "<quote anchor>"`, separated by commas, the same set in every record; or `default` on a normal shot | `SC10-B07, MO-MINT, line:456` |
| reference_list | IDs and field paths `<ID>.<field>`; a singleton record or the project is named by its type | `PROJECT.frame_shape, SC10-SU01.lens_mm` |
| scene_or_story_point | a scene ID alone for the whole scene, or a story point | `SC26` |

Quote anchors are allowed wherever a line number is: `line:` in `because`, STATE `from` and `cause`, RULE `era`, `evidence` items and CARDINAL `lines`. In chat without a numbered story they are required there. Each quoted string has at least 3 words and must match exactly once in its scope: the scene's lines for a story point or a scene field, the whole story otherwise (CITE-02). When code resolves a story point at step 7 it adds ` = ` and the beat: `SC24 "She deletes the way home." = SC24-B05`. That ending belongs to code; never type or change it.

**G6. Items.** A repeatable field appears once per item. An item is a first part followed by named sub-parts: `- subject: CH-IONA.S02 | at: left_third | faces: camera | does: chews, stops, frowns`. The first part is the item's main value, usually an ID. Sub-part keys are schema words in any order; an unknown key is an error. Positional (unnamed) sub-parts are never allowed. A few fields have no first part (the schema marks them `first_part: null`); their value starts with the first named sub-part: `- lineup: height: short | mass: slight | shape: long | value: light | colour: grey | tempo: slow`.

**G7. Empty and undecided.** Empty is `none`: a field the depth asks for with nothing to hold is written `none` (`- effect: none`), never left out (FORM-05). Undecided is `open` (listed as a question for the user). `auto` means code decides. `null`, `N/A`, `-` and a blank read as missing. Elsewhere, `- at: none` in an inbox clears a stored field you wrote (a wrong `at` once `at_words` is there).

**G8. Notes.** A line inside a record starting `> ` is a note attached to it, kept and not parsed.

**G9. The END line.** Every file ends with exactly one END line: `END OF FILE | <what the file holds> | <n> records`, for example `END OF FILE | Scene 10 shots 130-200 | 8 records`. `n` counts the file's `###` records. A missing END line or a wrong count means a cut-off reply or a dropped record.

**G10. Merging.** Records with the same TYPE and ID in several files merge field by field: a scene's list fields in `04 Scene list.md` and its design fields in its scene file; a scene's shots across batch files. The same field with two different values is an error. Items of a repeatable field are combined and exact duplicates removed. On a code surface, `apply` replaces each field you send whole, except a review's answers and a side choice's sides, which it merges by their first part.

**G11. No shortening.** Shortening markers inside a record ("...", "…", "etc.", "and so on", "same as above", "as before", "remaining shots", "omitted for brevity", a line starting `//`) are errors, unless inside double quotes that match the story.

**G12. Quotes are the story's.** Anything inside double quotes in a field value is a quotation from the story and must be found in the record's cited lines (or the scene's lines). Story words otherwise appear only in `TEXT.words` and prose `SPEECH.text`.

**G13. Headings in free text.** Free-text headings use `#` or `##` only. Any line starting `###` is a record heading, and an unknown TYPE after it is FORM-01.

## Who writes what

Every field has one writer (schema `writer`): `story` (code copies it from the story), `ai` (you), `user` (only through an answered or defaulted CHOICE), `code_state` (code keeps it: status, locks, resolved story points) or `code_derived` (computed on every build, never stored: labels, time floors, clip lengths, sides, prompts, prices). Write only `ai` fields, plus the fields marked `chat_writer: ai` when you work in chat without code; on a code surface `apply` refuses a `user` or code field from you (FORM-10). A few fields change writer with the record: TEXT `words` is copied by code from `words_from` when the story writes the text, and is yours only for invented or inferred text.

## Example 2: a whole file saved from chat

```
# Continuity

## At a glance
Iona skins her palm on the sill in scene 6; from scene 7 her shirt sleeve is gone, pressed into Jude's wound.

Below this line: details for the AI and the checker. You never need to read them.

### STATE CH-IONA.S02 Sleeve torn, palm skinned
- element: CH-IONA
- from: SC07 | line: "pressing what is left of her shirt sleeve"
- cause: "pressing what is left of her shirt sleeve" | quote: "what is left of her shirt sleeve"
- state_line: one shirt sleeve torn away, palm skinned
- changes: the sleeve is gone, first seen here; the palm was skinned on the sill in scene 6
- side: skinned palm | own: right | plot: yes
- handedness: original
- origin: story
> Own right is a default (K26): the story does not say which hand.

---
| Check | Result |
|---|---|
| FORM-06 END line present | PASS |

END OF FILE | Continuity, scene 7 | 1 records
```

This is Example 1 as it is saved from a chat app. The plain part comes first, then the fixed divider line, then the records, then the checks-in-words table after a `---` line, then the END line. The real table has a row for each of the 14 checks (`references/formats/06` part 1). In chat every line reference is a quote anchor; `stage.py adopt` turns anchors into numbers later.

## Example 3: the turn shot of scene 10, and one scene item

```
### SHOT SC10-SH150 Not mint
- beats: SC10-B07, SC10-B08
- lines: 454-466
- purpose: Iona's body admits what her words denied; Saye's proof lands on her face.
- because: SC10-B07, SC10-V1, MO-MINT, CR-IONA
- role: turn
- frame: single
- size: close_up
- move: static
- subject: CH-IONA.S02 | at: left_third | faces: camera | eyeline: CH-SAYE | dwell_s: 15 | does: chews slowly; stops chewing; a small frown | still: head, hands, torso
- hear: SC10-D11 | speaker: on_screen
- screen_time: 15
- moment: 4-6 | shows: stops chewing; a small frown; chews once more, slowly
- why: "Her face changes." puts the turn inside her mouth, so the scene's closest frame is spent here.
```

The lines above are some of the shot's fields, in their order; the whole record, with every Standard field, is in `references/examples/01 The Catch - scene 10.md`. In the same scene file the turn picture, written before any shot, reads `- turn_picture: SC10-B07 | picture: Iona close, eyes on Saye just off the lens, her mouth stopped mid-chew`.

## The ten most common mistakes

1. **Unnamed sub-parts.** Wrong: `- subject: CH-IONA.S02 | left_third | camera`. Right: `- subject: CH-IONA.S02 | at: left_third | faces: camera` (G6, FORM-12).
2. **Shortening a long list.** Wrong: `- moment: 8-15 | shows: as before`. Right: write every record in full; if the reply is getting long, stop at a whole record and the next batch continues (G11, FORM-08).
3. **A missing or wrong END line.** Count the `###` records in the file, not the shots you meant to write. `END OF FILE | Scene 10 shots 130-200 | 8 records` (G9, FORM-06, FORM-07).
4. **`###` on a free-text heading.** Wrong: `### At a glance`. Right: `## At a glance` (G13, FORM-01).
5. **A bar inside text.** Wrong: `- purpose: Iona tests the leaf | Saye waits`. Right: `- purpose: Iona tests the leaf; Saye waits` (G5, FORM-12).
6. **Typing what code works out.** Leave out labels ("10Q"), time floors, clip lengths, image sides, mirror states and prices; code computes them and drops typed values with a warning (FORM-10).
7. **Abbreviations and values off the list.** Wrong: `- size: MCU`, `- move: dolly in`. Right: `- size: medium_close_up`, `- move: push_in`. Known spellings are tidied and logged (FORM-13); others are FORM-04.
8. **Wrong ID shapes.** Wrong: `SC10-SH15`, `SC10-B7`, an ID outside the handout's block. Right: `SC10-SH150`, `SC10-B07`, IDs copied from the issued block, shots in tens (FORM-02, ID-03, ID-06).
9. **Quotes that are not exact, or anchors that are too short.** `"She fires."` has two words and appears twice in The Catch. Quote at least three words that occur once in their scope, copied exactly with the story's punctuation (G5, G12, CITE-02, CITE-03).
10. **`null`, `N/A` or a blank for "nothing".** These read as missing (FORM-05). Write `none` for empty and `open` for a question the user must answer (G7).
