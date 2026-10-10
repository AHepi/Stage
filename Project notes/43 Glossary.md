# 43 Glossary

Log entry 43 started this file. The terms the authority documents use for making video with MiniMax H3, each with a plain meaning and where to find it. Stage's own words are in `reference/02 Word list.md`; this list is for the words that come from outside Stage.

The authority documents, checked on 10 October 2026:
- **MiniMax's reference-mode guide:** huggingface.co/MiniMaxAI/MiniMax-H3, file `docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md`.
- **MiniMax's base-mode guide:** the same place, `docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md`.
- **MiniMax's model page:** huggingface.co/MiniMaxAI/MiniMax-H3.
- **ComfyUI's H3 templates page:** docs.comfy.org/tutorials/video/minimax/minimax-h3-native.
- **ComfyUI's H3 prompt guide:** docs.comfy.org/tutorials/video/minimax/minimax-h3-prompt-guide.
- **The testers' notes:** github.com/phileiny/h3-storyboard-skill, file `skills/h3-storyboard/SKILL.md` (in Chinese).
- **The handover:** `Project notes/42 Handover - what Stage should make and why.md`.

| Term | Plain meaning | Where |
|---|---|---|
| H3 | MiniMax's video model that makes picture and sound together. | MiniMax's model page |
| H3-Context-IR (the rewriting step) | A program on MiniMax's own service that turns a short request into a long, structured prompt before H3 sees it. It is not in the open version that ComfyUI runs. | MiniMax's model page |
| Reference mode (Ref2VA, R2V) | H3 making video from pictures you give it. ComfyUI's template for it is "MiniMax H3 Reference to Video (R2V)". | MiniMax's reference guide; ComfyUI's templates page |
| `subject_definitions`, `summary`, `retention_analysis`, `detailed_description`, `overall_soundscape`, `non_diegetic_music` | The six sections of a reference-mode prompt, in this order. | MiniMax's reference guide |
| `<Subject N>` | A label for something seen that H3 must keep or change: the place, or a person. | MiniMax's reference guide |
| `<Picture N>` | A label for a picture you connect, numbered in the order you connect them. | MiniMax's reference guide; ComfyUI's templates page |
| `fully_preserved`, `partially_preserved`, `attribute_transfer`, `weak_reference` | How closely H3 should keep something from a picture: exactly, in part, only one feature, loosely. | MiniMax's reference guide |
| `[Shot 1]`, `[Shot N] At MM:SS.mmm` | Shot markers inside one clip: the first has no time; each later one opens with the time of its cut. | MiniMax's reference guide |
| `(S1)`, `(S2)` | Speaker numbers, in the order voices first speak in a clip. | MiniMax's reference guide |
| `<d>[English] ... </d>` | How a spoken line is written, with its language. | MiniMax's reference guide |
| N/A | What a section says when it is empty (no music). | MiniMax's reference guide; ComfyUI's prompt guide |
| 17 × k + 5 | The frame counts H3 accepts (5, 22, 39 ... 124 ... 362). ComfyUI rounds a length up to the next one. | ComfyUI's templates and prompt guides |
| Lightning LoRA | A speed-up add-on in the ComfyUI template (4 steps instead of 20). ComfyUI says it lowers motion and sound quality a little; leave it off. | ComfyUI's templates page |
| Steps | How many passes H3 makes to clean up a clip; 20 by default. | ComfyUI's templates page |
| ref_image_size | How large your pictures stay when H3 reads them: "match" (faster) or "max" (up to 2048 pixels on the short side). | ComfyUI's templates page |
| Negative branch (negative side) | A second, "avoid this" prompt. ComfyUI's H3 templates have none, so naming a thing adds it. | ComfyUI's prompt guide |
| Tail | The last 1.3 to 1.5 seconds of a clip, made to be thrown away, because H3 often breaks into noise 1.2 to 1.7 seconds before the end. | The testers' notes, section 7 |
| Lead-in (for shot and reverse shot) | A shot showing both people, which H3 needs before it can find the opposite angle. | The testers' notes, section 7.2 |
| Contact cut | Ending a shot as one thing reaches another and starting the next with the result already there, because H3 can't time one thing making another happen. | The testers' notes, section 2.1; the handover, W9 |
| Seed | The number that makes each run different. The testers found speech rhythm follows the seed, not the words. | ComfyUI's templates page; the testers' notes, section 6.2 |
| Route | A model plus the place it runs, such as "MiniMax H3 in ComfyUI, Reference to Video". | The handover, section 4 |
| Clip book | All the clip pages for one route, with its settings page, master pictures and shot map. | The handover, section 4 |
| Start picture | The still made for a clip's first moment; the prompt calls it `<Picture 1>`. | The handover, section 9 |
| Master picture | An empty set picture made once per place; start pictures are built from it. | The handover, section 9 |
| Take log | The record of every run: seed, settings, result, verdict. On the H3 route it also says which rules each take confirmed or showed wrong. | The handover, W11 |
