# Card 24. Rights, consent and disclosure

Step 0 reads only "The rights question"; step 4 reads only "Names and likeness"; add-on C reads it whole. "D4 R7" is rule 7 in D4 §4, "D4 P3" principle 3 (§2), "D4 Rec3" recipe 3 (§5). This is a production checklist, not legal advice: for a film that will be sold, made for a client, or that uses a real person or a licensed book, suggest a lawyer before release (D4 R27).

## The job

Settle, before any work, whether the user may adapt the story; keep real faces, voices, names, brands and protected designs out of pictures and prompts; plan sensitive shots around filters without tricks; record every licence; keep the provenance marks; write one honest disclosure line (D4 §2). Step 0 hands on PROJECT `rights` (CHOICE-001) and the source's RIGHTS record; step 4, `likeness_basis`, small choices for invented names and the name checks (notes on RT-001); add-on C, RIGHTS records for voices, likeness, music, fonts, stock and tool terms, and the disclosure text in `22 Rights and credits.md`.

## Questions in order

1. **Who owns the story? Is any face or voice real? Is every invented name clear?** See the two parts below (D4 R1, R7, R17).
2. **Does the shot touch a sensitive subject?** Set `content_flags` and a `policy_route` at shot design (D4 R10): a **content flag** marks a sensitive subject (violence, blood, a minor, a real person or brand); a **policy route** says how it is made instead. A minor is never in a flagged subject (D4 R8).
3. **Was a request refused twice?** Stop, reroute to compositing, sound or restaging, and log it; wording meant to slip past a filter can end the account (D4 R11; C1 R10).
4. **Does the tool plan allow the use?** A film that will be sold, shown at festivals or earn money needs every kept take, voice and sound made on a commercial plan (D4 R13), recorded as a RIGHTS record (`subject: model_terms`, `commercial_ok`). A take resembling a protected character, logo or artwork is rejected at checkpoint E (D4 R6).
5. **Does every asset carry its licence?** One RIGHTS record per library sound, stock file or font, made when it enters (D4 P6, R15-R16).
6. **What is disclosed?** Keep Content Credentials and watermarks (**provenance marks**, proof of where a file came from) (D4 P8; D8 R26); write one wording for credits, platform AI labels and festival answers (D4 R20-R22, Rec6).
7. **Are the facts fresh?** Re-check any law, policy or terms fact older than `model_facts_max_age_days` before release or a large spend (D4 R29).

## The rights question

Example first: The Catch's title page says "= An original short screenplay" (line 3). "Original" means not adapted from another work; it does not say who wrote it (D4 §9.1). So the welcome asks once: "Is this story yours, or do you have permission to adapt it? [It's mine]". Adapting a story is its owner's right (D4 §3.1).

PROJECT `rights` takes one value; D4's finer statuses map onto it (D4 §6.1):

- `mine`: the user wrote it.
- `permission`: a licence, an **option** (a paid, time-limited right to buy the film rights later) or written permission. It must be written and allow a film made with AI tools, say where, for how long and whether it may earn money (D4 §3.1, R28). The finer kind goes in the RIGHTS record's `clearance`.
- `public_domain`: out of copyright. Check every country of showing and the exact edition or translation (D4 R3, Rec2).
- `study_only`: "not mine, no permission", and the nearest value for a fan work, since not earning money is no defence (D4 R2). Work goes on privately; every export is marked "Private study, not for publication"; packs refuse public release (GEN-14); the text never goes to tools that train on it (D4 R1).
- `unknown`: until answered.

The source's RIGHTS record (`subject: source`) names the holder by role ("the author"), never by name or contact (blueprint principle 10). A source written or revised with an AI model is said so in credits and festival answers, and awards requiring a human-written screenplay are skipped (D4 R4, R30).

## Names and likeness

Example first: "Saye opens a file. The same woman, much younger. A flight suit. Unsmiling." (line 988), then "NELL ROWAN. FLIGHT TEST." (line 990). A real pilot's photo would be a real person's **likeness** (a recognisable face, body or voice). Instead Nell is designed at "Sixty, perhaps. She looks older." (line 1135), the photograph is made by editing that face about nineteen years younger ("The date is nineteen years old.", line 998), the flight-suit patch is invented, and the name is a text graphic (D4 §9.3).

1. **Every face and voice is invented** unless a living adult has signed **consent** (written permission for that exact use); a dead person's face and voice are protected too, and a celebrity's are never used (D4 P3, R7; D3 R16). `likeness_basis` defaults to `invented` as a small choice; `self_consented` or `performer_consented` needs a RIGHTS record whose ID goes in `consent` at add-on C, the signed form kept outside every AI tool (D4 Rec4). A child's face is always designed (D4 R8).
2. **Describe, never name.** A fixed description names no real person and never says "looks like" (D4 P2, R5; WORDS-03); each approved face gets a lookalike check by eye (D4 Rec4).
3. **Voices.** `VOICE.source` defaults to `designed`; a clone only of the user's own voice or of a consenting, verified adult (D3 R16-R17).
4. **Name check** every invented character, company, product, institution and place: search it in quotes, then the national trademark databases, and give D4's verdict: clear, a low-risk coincidence (same name, unrelated field) or a conflict (D4 R17, Rec3). A conflict becomes a small choice proposing a rename, shown at checkpoint B. OSTREL ("OSTREL, stitched on it in blue.", line 496) is near a household-goods mark, and "IONA VALE." (line 1233) is an author name on colouring books: both low-risk coincidences (D4 §9.4).
5. **Real institutions**: keep the place, invent the name, crest and livery (D4 R19); "Police lights beyond frosted windows." (line 492) show no livery, so nothing is flagged.
6. **Brands and signs** are invented; any that must be read is a text graphic (D4 R18; K17).

## Translation menus with pitfalls

One `policy_route` per flagged shot, tied to its flag (D4 §3.6, Rec5):

| Flag | Route | Pitfall |
|---|---|---|
| `gunfire` | `sound_only`, plus a composited flicker | A weapon aimed at a person in frame |
| `violence_implied` | `split_cause_reaction_aftermath`, with words for the visible result (C1 R9) | Injury words in the prompt |
| `blood_small` | `composite_element`: the plate made without blood | "Blood splatter" asked of a model (C1 §4) |
| `real_brand`, `real_person` | `restated` as an invented design, or `cut` | A model-drawn real logo (D4 §3.3) |
| `drug_use`, `self_harm` | `restated`: aftermath, never method | A word a filter misreads: SC11's "needle" is a gauge (D4 §9.2) |

## Budgets and saved choices

- `model_facts_max_age_days`: the age at which law, terms and prices are re-checked (D4 R29; GEN-11).
- `fixed_description_words`: invented faces described in visible nouns only (WORDS-05).
- `licensed_data_only: yes` limits routing to models trained on licensed footage (blueprint 8.4; C1 R19).
- One disclosure wording for every place (D4 P8).

## The baseline is a strong answer

An invented face, a designed voice, an invented brand drawn as a text graphic, and the plain credit line are choices, not failures (D4 P3, R18, Rec6). Depart only with a signed consent or a written licence.

## Cliché traps

Test: would the credit line and every festival answer still be true if the project log were read aloud (D4 Rec6-Rec7)?

- **"The filter let it through"**: a filter is a floor, not permission. Fix: the rights checks still apply (D4 §3.3, P5).
- **"Looks like" an actor** in a fixed description. Fix: visible features only (D4 Rec4; WORDS-03).
- **Cropping a watermark** away. Fix: keep it in frame (D8 R26).
- **Overstating human work**: "designed" only for what a human designed (D4 Rec6).
- **"No AI" to a narrow festival question** without checking how the source was written. Fix: read the project log first (D4 Rec6).

## Reasons that fail and reasons that pass

- Fails: "Nell's photo from a real pilot archive, for realism." Passes: "Nell's photo edited from her designed face nineteen years younger (line 998); `likeness_basis: invented` (D4 R7, §9.3)."
- Fails: "Keep 'blood splatter'; the scene needs it." Passes: "SC06's beads: `blood_small`, `composite_element`; the plate is made without blood (D4 §9.2; C1 Ex2)."
- Fails: "Directed and designed by [names]" when the AI drafted the shots. Passes: "Directed and edited by [names], who chose and approved every shot planned with an AI assistant." (D4 Rec6)

## Two worked examples

### The Catch: SC06, the shot through the roof (lines 216-222)

"Someone KICKS the top gate open and FIRES down through the roof." (line 216) gets `gunfire` and `violence_implied`, route `split_cause_reaction_aftermath`: a bright flicker through the roof grid and the three looking up; the shots and the crash in the sound mix; the spark at her boot composited (D4 §9.2). "He sits down into Eli with a hole through his shoulder." (line 222) becomes "He sits down heavily against Eli, a dark stain spreading on his shoulder"; the hole is never shown.

### The Long Places: an AI-written source (lines 1-3)

The file names itself "revised by Claude, final" (line 1), and line 3 says the novella came from "GLM 5.3's novella (file 10), revised by three Claude agents". The credit uses D4's template for an AI-written source: "Based on The Long Places, a novella generated with GLM 5.3 and revised with Claude under the direction of [names]." A screenplay the pipeline drafts from it is AI-written too, so festival answers say so (D4 R30). Its real places stay ("Erciyes stood up out of the haze", line 37), while any Ministry letterhead is invented (D4 R19, §9.6).

## Self-check

- Is `rights` answered or defaulted, and every export marked when it is `study_only`?
- Does every character have `likeness_basis`, and every non-invented one a consent record?
- Is every invented name checked, with conflicts shown as small choices?
- Does every flagged shot have a policy route, and did nothing go a third time after two refusals?
- Does every kept take, sound and font have a RIGHTS record allowing its use?

## Words for AI models

Works: visible attributes instead of names ("short neat grey hair, a pale lined face"); plain physical wording for injuries ("a dark red stain spreads through his shirt"); honest genre context first ("A tense dramatic thriller scene.") (C3 §14); invented brands as plain surfaces, the graphic composited later (D4 R18).

Fails: a real person, artist, film or brand in a prompt field (WORDS-03); misspellings or code words to pass a filter (C3 §14; D4 R11); a real person's photo as a reference (D4 R25).

## Look up for more

D4 §2, §3, §4, §5, §6.1 (pipeline names), §9; D3 §3 (R16-R19), §6; D8 R26; D9 R19-R20; C1 §4, R9-R10. Print one rule: `stage.py lib D4 R11`.
