# The settings the code reads, the same for every story

These files tell `stage.py` what a record may hold, what each step does, which numbers and words apply, and what the AI video models can do. Code reads them on every run; the AI reads them only through a handout, a check message or `references/formats/03 Field guide.md`, which is made from the schema.

Example: the checker says a shot's time is too short by comparing it with `turn_reaction_min_s` in `rules/constants.json`, and the shot 150 floor (11.8 seconds of speech plus 2.0 seconds to react, 13.8 seconds) comes from that number, never from a number typed into a record.

| Folder | File | What it holds |
|---|---|---|
| `schema/` | `schema.json` | Every record type and field: its kind, allowed values, depth, and who writes it (the AI, code, the user, the story) |
| `schema/` | `steps.json` | Every step: its step file (`stages/<step>/CONTEXT.md`), its units, the card parts each unit reads (`references/cards/...`), the records it writes, its checks and its checkpoint. `stage.py next` and `stage.py handout` are built on it |
| `rules/` | `constants.json` | The named numbers, each with its meaning and source (`repair_rounds_max`, `batch_size`, `turn_reaction_min_s` and the rest) |
| `rules/` | `words.json` | The word list in code form: retired words, abbreviations and codes the checker flags, the stillness words |
| `rules/` | `limits.json` | Sizes: handout ceilings for each app, the chat kit's lengths, tokens for each word |
| `rules/` | `tone_defaults.json` | For each home tone, how much longer or shorter its shots run |
| `adapters/` | `video_models.json`, `image_models.json`, `audio_models.json`, `routing.json`, `phrasebook.json`, `prices.json` | The dated facts about AI picture, video and voice models and their prices, each file with the date it was checked (`checked_on`); `stage.py refresh-models` proposes new facts and keeps the old ones |

Who may change these, and how:

- Only the maintainers, and only with a test. Every file here is checked by the tests in `tests/` (the schema and the rules by `wp1_schema_acceptance.py`); change the file and the test together, run the tests, then run `stage.py build-kit`, which remakes the field guide and the kits from them.
- `adapters/` holds dated facts, not rules: they go out of date. Above `model_facts_max_age_days` no prompt pack is marked ready to spend and no money is printed. Refresh them with `stage.py refresh-models --propose`, and apply a price change only once the user approves it (`--apply`).
- Never put a user's story, name or account details here: these files ship in every kit.
