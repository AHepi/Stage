# Digest D4: Rights, likeness, consent, style imitation, content policy and AI disclosure (27 Sept 2026)

Source: `research/D4_legal_ethics_disclosure.md` (fact-checked 27 Sept 2026, second pass). Brackets: R*n* = the file's decision rule *n* (§4); P*n* = core principle *n* (§2); Rec*n* = Recipe *n* (§5); §x = section. Evidence: **[V]** verified, **[U]** one secondary source, **[J]** judgment. Not legal advice; re-check law and terms facts older than 30 days (R29).

## 1. Scope

1. Decides at intake whether the user may adapt the story (own work, public domain, licensed, fan use, or private `study_only`) and records owner, licence, intended use, territories and how the source was written, including AI authorship.
2. Keeps real faces, voices, characters, brands and artwork out of prompts and references; plans violence and sensitive content around model filters, never through them; logs every tool's terms and every asset's licence.
3. Builds the authorship evidence (human decisions) and the disclosure package (credit line, platform labels, festival answers, EU Article 50 form), worked through on *The Catch* and *The Long Places*.

## 2. Rules

**Rights to the story**
1. [R1] If the user did not write the story and it is not public domain, then get a licence or written permission covering a film made with AI tools, or else stop or continue as `study_only` (private; every export marked "Private study, not for publication"; no public-release packs; no upload to tools that train on it), because adaptation is the rights holder's exclusive right [V] and even a private adaptation is a copy [J].
2. [R2] If the user says "just for fun", then record `fan_noncommercial` and follow the owner's published fan rules exactly (Star Trek: under 15 minutes, or two parts up to 30; free; unpaid amateurs; fixed disclaimer [V]) or keep it private, because non-commercial use is no defence in itself [J].
3. [R3] If the source is claimed to be public domain, then check every showing country and the exact edition or translation, because US terms differ from UK/EU life + 70 [V] and modern translations can be protected [J].
4. [R4] If the source was written wholly or mostly by an AI model, then record `authorship_mode` and `source_versions[]` and warn that copyright in the text may be thin, because "Copyright does not extend to purely AI-generated material" (US Copyright Office) and the UK proposes the same [V].
5. [R28] If a book licence is silent on AI tools, then get AI-assisted production confirmed in writing, because silence invites a later dispute [J].

**Names, styles, characters, brands**
6. [R5, P2] If a prompt or reference would name a film, director, cinematographer, living artist, franchise, actor or brand, then rewrite it as visible attributes and keep the name in `human_notes`, because names pull models toward protected material and trigger filters [J].
7. [R6] If a take resembles a protected character, logo, costume or artwork, then reject it at checkpoint E, because tool terms pass on only the tool's rights, never a third party's [V].
8. [R17] If a character, company, product or place name is invented, then run the name check (Rec3) at checkpoint B, because an exact match with a real person or brand invites defamation or trademark complaints [J].
9. [R18] If an invented brand, label or sign must be readable, then make it an insert graphic (C2 R6), because models redraw text each time and sometimes copy real logos [J].
10. [R19] If a real institution would be identifiable (hospital, police force, air force, ministry), then keep the place but invent its name, crest and livery, because real institutions in invented events invite complaints and official insignia are often restricted [J].

**Faces and voices**
11. [R7, P3] If a character would be based on a real person, living or dead, then design an invented face; use a real adult only with a signed consent form, never a celebrity, because state laws cover the living and (CA, NY) the dead, federal NO FAKES cleared committee 18 June 2026, and every major tool bans it [V].
12. [R8] If a character is a child, then design the face, never upload a real child's photo, and keep the child out of sexual or graphic violent content, because every policy bans it and several tools refuse minors outright [V].
13. [R9] If the user wants to use their own face or voice, then record `self_consented` with the date and keep source files private, because it creates a biometric asset others could misuse [J].

**Content policy and filters**
14. [R10] If a shot touches violence, weapons, blood, sex, minors, self-harm, drugs, hate symbols or real people or brands, then set `content_flags` and a `policy_route` at shot design, because planning composites is cheaper than paying for refused takes [J].
15. [R11, P4] If a model refuses the same request twice, then stop, reroute (composite, sound, restaging or open weights) and log it; never add jailbreak wording, because circumvention is banned (Google) and can end the account (Runway) [V].
16. [R12] If open weights are considered, then check territory, revenue and commercial terms first, keep the content non-graphic and still disclose, because the licence travels with the model (HunyuanVideo excludes the EU, UK and South Korea) [V].

**Licences**
17. [R13] If the film will be sold, monetised, shown at festivals or made for a client, then generate every kept asset on a plan allowing commercial use, because the free tiers of Kling, Luma and ElevenLabs are non-commercial and Luma's free-tier watermark stays after upgrading [V].
18. [R14] If a kept Kling clip came from a free (non-member) account, then keep the "Kling AI" mark or state "generated by Kling AI"; if from a paid membership, credit Kling in the tool list only, because the label duty applies "without our written permission" [V].
19. [R15] If a sound, music cue or image comes from a library, then record its licence per file and reject NC files for commercial projects and ND files you will edit, because NC forbids commercial use and ND forbids changes [V].
20. [R16] If a font appears in an insert graphic, then prefer an OFL font and record it, because OFL allows "video titling" and credit is "not required" [V].

**Disclosure**
21. [R20, P8] If the film has photoreal AI pictures or voices, then keep provenance (C2PA, SynthID), add the credit line and set every platform's AI label (YouTube Studio: Attributes, "AI use" = Yes), because YouTube, TikTok and Meta require it and EU Article 50 requires deepfake disclosure [V].
22. [R21] If the film is shown in the EU by someone acting professionally, then use the artistic-work form (end-credit line, description, marks intact), because Article 50(4) limits fictional works to disclosure "that does not hamper the display or enjoyment of the work" [V].
23. [R22] If the film is entered for a festival or award, then read that call's AI rules and answer every AI question fully, because rules differ (Oscars; Cannes) [V] and late discovery can disqualify [J].
24. [R30] If the source or screenplay was written or revised by an AI model, then say so in the credit and festival answers and skip awards requiring a human-authored screenplay, because the 99th Oscars state "screenplays must be human-authored to be eligible" [V].
25. [R23] If an advert shown in New York contains AI-made people, then add a conspicuous synthetic-performer notice unless it is a trailer or promo showing them as they appear in the film (or audio-only), because the law (from 9 June 2026) exempts only ads for expressive works used "consistent with its use in the expressive work" [V].
26. [R26] If the film's copyright is registered in the US, then disclose more than de minimis AI material and describe the human contribution from the log, because the Copyright Office requires it [V].

**Privacy, counsel, staleness**
27. [R24, P9] If a manuscript is someone else's and unpublished, then get written permission before uploading it, in D1 §8's no-training settings, because uploads may be kept, reviewed or trained on [V].
28. [R25] If a reference image goes to an aggregator such as fal, then upload only invented or owned images with location data removed and the shortest retention, because "CDN files found in the input of a request are not deleted" [V].
29. [R27] If the release is commercial, or involves a licensed book, a real person or a union performer, then set `counsel_review: recommended` and hold release until the user confirms, because this file cannot replace a lawyer [J].
30. [R29] If any law, policy or terms fact is older than 30 days at release, then re-check it, because §3 changed repeatedly during 2026 [V].

## 3. Breakdown fields

Enums lowercase `snake_case`; empty `"none"`. Authority: A = human (`decided_by: human`), L = LLM drafts for approval, D = derived by script. **The blueprint's names win** in the built pipeline (§6.1; see section 8).

| Level | field_name | Meaning | Allowed values / example |
|---|---|---|---|
| film | `rights_and_compliance` | Container for the film fields | object |
| film | `rights_status` (A) | Right to adapt the source | `own_original` \| `public_domain` \| `licensed` \| `option_held` \| `written_permission` \| `fan_noncommercial` \| `study_only` \| `unknown` \| `blocked` (blueprint: `mine` \| `permission` \| `public_domain` \| `study_only` \| `unknown`) |
| film | `rights_holder` (A) | Owner's name, stored locally only | text |
| film | `licence_ref`, `licence_scope` (A) | Licence file name; coverage | file name; `media`, `ai_tools_permitted` (`yes`\|`no`\|`silent`), `territories[]`, `term_end`, `commercial` (`yes`\|`no`) |
| film | `underlying_works[]` (L) | Quoted songs, poems, translations, artworks | `title`, `status`, `evidence` |
| film | `public_domain_evidence` (L) | Proof from Rec2 | `first_published`, `country`, `author_death_year`, `edition`, `jurisdictions_checked[]` |
| film | `authorship_mode` (A) | How the source was written | `human_written` \| `ai_assisted` \| `ai_generated_human_directed` \| `ai_generated` \| `unknown` |
| film | `source_versions[]` (L) | Revision history | `version_id`, `label`, `made_by` (`human` \| model \| `unknown`), `human_role`, `file_hash` |
| film | `intended_use` (A) | Where the film goes | `personal` \| `festival` \| `online_free` \| `online_monetised` \| `commercial_sale` \| `client_work` |
| film | `release_territories[]` (A) | Countries or blocs | `us`, `eu`, `uk` |
| film | `commercial_project` (D) | From `intended_use` | `yes` \| `no` |
| film | `counsel_review` (A) | Lawyer involvement | `not_needed` \| `recommended` \| `done` |
| film | `disclosure_plan` (L) | Credit, labels, festival answers | `credit_line`, `platform_labels{}`, `festival_answers[]`, `eu_article50` (`in_scope`\|`out_of_scope`) |
| film | `facts_checked_on` (D) | Last §3 re-check | ISO date |
| character | `likeness_basis` (A) | Source of face and voice | `invented` \| `self_consented` \| `performer_consented` \| `blocked_real_person` (last is a proposal) |
| character | `consent_record` (A) | Pointer to the offline consent form | `RT-001` \| `none` |
| character, prop, location | `name_check` (L) | Rec3 result | `searched_on`, `registers[]`, `result` (`clear` \| `coincidence_low_risk` \| `conflict`), `note` |
| prop, graphic | `trademark_risk` (L) | Real or similar marks in frame | `none` \| `invented_checked` \| `real_incidental` \| `real_needs_clearance` |
| shot | `content_flags[]` (L) | Sensitive topics | `violence_implied` \| `violence_onscreen` \| `weapon_visible` \| `gunfire` \| `blood_small` \| `gore` \| `nudity` \| `sexual_content` \| `minor_present` \| `self_harm` \| `drug_use` \| `hate_symbol` \| `real_person` \| `real_brand` \| `real_institution` \| `fire` \| `none` |
| shot | `policy_route` (L, approved at C) | How flagged content is made | `as_written` \| `restated` \| `split_cause_reaction_aftermath` \| `composite_element` \| `sound_only` \| `open_weights` \| `cut` |
| shot | `human_notes` (A) | Only place names may live; never compiled | text |
| generation job | `model_terms` (D) | Terms snapshot | `plan_tier`, `commercial_ok` (`yes`\|`no`\|`check`), `label_required`, `terms_url`, `checked_on` |
| generation job | `provenance` (D) | Marks on output | `c2pa`, `synthid` (`present`\|`absent`\|`unknown`), `visible_watermark` (`yes`\|`no`) |
| generation job | `inputs_personal_data` (L) | Real likeness in inputs | `none` \| `self_consented` \| `performer_consented` |
| asset | `asset_licence` (L) | Licence per file (a RIGHTS record in the blueprint) | `source`, `provider`, `licence_id` (`cc0` \| `cc_by_4_0` \| `cc_by_sa_4_0` \| `cc_by_nc_4_0` \| `ofl_1_1` \| `apache_2_0` \| `provider_terms` \| `other`), `attribution_text`, `commercial_ok`, `url`, `obtained_on` |

**Validator checks.** D4-V17 no compiled prompt contains a name from any `human_notes` or the banned-names list; D4-V18 every kept take has `commercial_ok: yes` when `commercial_project: yes`; D4-V19 every character has `likeness_basis`, and non-`invented` ones have `consent_record`; D4-V20 every asset has a licence, no `cc_by_nc_*` in a commercial project; D4-V21 every non-`none` flag has a `policy_route`.

## 4. Procedures

**Rec1 Rights intake** (stage 0, before checkpoint A, about 10 minutes)
1. Paste: *"Before breaking down this story, interview me for D4's rights record, one question at a time: who wrote it; whether any AI wrote or revised it; who owns it; whether it is published; what licence, option or permission I hold and what it covers (film, AI tools, territories, end date); where the film will be shown; whether it will earn money; whether it quotes other works. Then fill `rights_and_compliance` and list blockers."*
2. Answer plainly; the LLM applies R1–R4 and R28 and prints `rights_status`, `commercial_project`, blockers.
3. Approve at checkpoint A (prose: before D2's M) only if not `unknown` or `blocked` (blueprint: CHOICE-001). "Not mine, no permission" → `study_only`, every export marked "Private study, not for publication".

**Rec2 Public-domain check** (15 minutes per source)
1. Ask: *"Find this text's first publication year and country, the author's death year (and the translator's or illustrator's, if the edition has one), and the exact edition or translation I hold. Apply the Cornell chart for the US (published before 1931: free; 1931–1963: free unless renewed; 1964–1977: 95 years from publication; 1978 on: life plus 70) and life plus 70 for the UK and EU. List every assumption and every source."*
2. Confirm the years yourself; for US 1931–1963 works, have the LLM search renewal records and show the result.
3. Both free → `public_domain`; free in one only → `public_domain` for those territories and set `release_territories[]` to match; doubt → `unknown`.
4. Record `public_domain_evidence`; replace a modern translation with a public-domain one or license it.

**Rec3 Clearance pass** (stage 2, before checkpoint B, 20–40 minutes)
1. Ask: *"List every proper name in the bible (characters, companies, products, institutions, places), every readable text, logo, crest, livery, patch and artwork; mark each invented or real."*
2. Invented names: web search in quotes, then USPTO, EUIPO TMview, UK IPO. Result `clear`, `coincidence_low_risk` (same name, unrelated field) or `conflict` (related field, or a real person in a similar role).
3. Real institutions: keep the place, invent name and insignia.
4. Set every `likeness_basis`; anything but `invented` needs a consent form.
5. Show the table at B with renames for every `conflict`.

**Rec4 Original face; real person's consent**
1. Identity key from script and B5; no actor names, no "looks like".
2. Candidate faces from text only; pick; build turnaround (C2).
3. Lookalike check: *"Does this face strongly resemble any well-known person?"*; regenerate on a confident match; add a human glance.
4. Age variants from the approved face with an edit model, never a real photo.
5. Real adult performer: one-page consent form signed before any upload (project; uses: LoRA training, voice clone, performance transfer; territories; term; how to withdraw). Store offline; record only its RIGHTS ID.

**Rec5 Content-flag pass** (stage 5, per scene)
1. Ask: *"For each shot, set `content_flags` from D4 §6's list and a `policy_route`. Rewrite any prompt words that name injury, weapons fire, blood, drugs or real people into visible, neutral description. Move gunfire into `sound_mix_elements`, and blood, sparks and flashes into `composite_elements` (C1 §6)."*
2. At checkpoint C approve the one-line flag summary per sequence.
3. Log every refusal (D1 `refusals[]`); after two refusals switch route; never reword a third time.

**Rec6 Licence log and disclosure package**
1. Per job, the script copies `model_terms` from a per-tool table re-checked monthly. Per imported asset, the LLM fills `asset_licence` from the download page.
2. At export, the LLM builds:
   - **Credit line:** *"Made with generative AI. Written by [writer]. Directed, designed and edited by [human names], who chose and approved every shot. Images and video generated with [tools]; voices with [tool]; sound effects from [libraries]. No real person's face or voice was used without consent. Content Credentials are kept where the tools provide them."* Add "Generated with Kling AI" if R14 applies, plus R15 attributions.
   - **Honesty variant** (LLM drafted the shot plans): "Directed and edited by [names], who chose and approved every shot planned with an AI assistant."
   - **AI-written source** (replaces sentence 2): *"Based on [title], a [novella / screenplay] generated with [model] and revised with [model] under the direction of [human names]."*
   - **Freesound credit:** *This [video] uses these sounds from freesound: "[sound name]" by [user] ( http://freesound.org/s/[sound ID]/ ) licensed under [licence]*.
   - **Platforms:** YouTube Studio, Attributes, "AI use" = Yes for photoreal; TikTok AI-generated label on; Meta AI disclosure label on.
   - **Festival answer:** *"Generative AI tools ([tools]) made the pictures[, voices] and [other]. [Writer / 'An AI model, directed by [names],'] wrote the [screenplay / source]. Humans [designed / approved or changed] every shot [an AI assistant planned], selected all takes, and did the edit, compositing and sound. No real person's face or voice was used without consent. A log of [n] recorded human decisions is available on request."*
3. Check the master for SynthID and Content Credentials (Gemini; clips under 90 s) and record the result.

**Rec7 Authorship evidence pack** (release, 10 minutes)
1. Ask: *"From the log, every answered CHOICE record and all fields with `decided_by: human` (authority `user`), list the human creative decisions (story changes, design theses, shot lists, selected takes, edits, composites, sound), count them per stage, and quote three with record IDs."*
2. Save with source hashes (C5 `manifest.json`) as `authorship_evidence.md`.

## 5. Checklists

**A (intake):** `rights_status` set, not `unknown`/`blocked` (or `study_only` with the mark); `ai_tools_permitted: yes` or written confirmation; `authorship_mode` and `source_versions[]`; `intended_use`, territories, `commercial_project`; D1 `training_optout: confirmed` before upload.
**B (bible):** every `likeness_basis` set, consent on file for non-invented; name-check table done, every `conflict` renamed or accepted in writing; no real person in identity keys or references; invented brands and insignia as insert graphics with licensed fonts; names only in `human_notes`.
**C (shots):** every flag has a route; violence split per C1 R9; gunfire, blood and sparks in sound or composite elements; no minor in a flagged topic.
**E (takes):** no real person, logo, protected character or artwork; plan allows commercial use if needed, labels noted; provenance recorded, no mark removed; no jailbreak or third-attempt take.
**Release:** §3 facts re-checked if over 30 days; credits, attributions, Kling line if needed; platform labels; festival forms; evidence pack; `counsel_review: done` if commercial.

## 6. Saying it to AI models

- **Image and video prompts** carry only visible attributes: never a film, director, cinematographer, living artist, franchise, actor, brand or real institution name (D4-V17 scans compiled prompts). Write "a dark stain spreads on his shoulder", not "gunshot wound"; "a bright flicker through the roof grid", not "gunfire".
- **No real faces as references.** Seedance 2.0 reportedly rejects real-face references and named characters; Sora admits a real face only via that person's cameo [U]. Filters are a floor, not permission.
- **Refusals:** after two, change route and log it; never disguise the content.
- **Text LLMs** get the manuscript only with training off (D1 §8); tell them "record the licence file's name, not its contents".
- **Voice tools:** clone only with a consent record (D3); ElevenLabs bans replicating a voice "without consent or legal right" [V].

## 7. The Catch

**Decisions made in the file**
- **Rights (§9.1):** "= An original short screenplay" (l.3), "= Workshop revision — 25 September 2026" (l.6): `rights_status: unknown` until the user confirms `own_original` (blueprint `mine`); no quoted songs or poems.
- **SC06 gunshot and blood (§9.2):** l.216 kick and fire → `gunfire`, `violence_implied`, `split_cause_reaction_aftermath`, prompt "A bright flicker through the roof grid; the three look up", gunfire and crash in the mix. l.222 "a hole through his shoulder" → never shown; "He sits down heavily against Eli, a dark stain spreading on his shoulder". l.226 spark → `composite_element`, "She flinches; her boot jerks back on the grid". l.244 blood beads → plate "the cage interior falling, two figures floating" plus 20–30 simulated beads composited. The guard's "pistol half drawn" (l.183) and "The pistol skids away." (l.185) → `weapon_visible`, never aimed at a person in frame. SC11's needle gauge (l.498) → "a grey meter, its pointer lying flat at zero".
- **Nell's photograph (§9.3):** l.988, l.990, l.1016. Design Nell at sixty (l.1135), derive the younger photo with an edit model ("The date is nineteen years old.", l.998), invent the flight-suit patch, make "NELL ROWAN. FLIGHT TEST." an OFL insert graphic; never a real archive photo.
- **Marks (§9.4):** OSTREL (l.496): no exact match found, similar US mark OSTRIL for utensils → `coincidence_low_risk` pending registers; mirrored insert graphic. IONA VALE (l.500, l.1231–1233): used as an author name for colouring books → `coincidence_low_risk`; wristband without any real hospital's name or logo (no NHS logo if the locale is UK). Police lights (l.492, l.1004): light only, no livery, `real_institution` not set.
- **Disclosure (§9.5):** Rec6 credit naming Seedance 2.x and Kling 3.0; festival form admitting AI-drafted shot plans; YouTube "AI use" = Yes; trailer from the film's own shots exempt in New York; `eu_article50: in_scope`; skip Cannes Official Competition.

**Flagged for the user**
1. Who wrote Final4, who ran the workshop revision, and whether an LLM was involved (if so, `ai_assisted` and R30).
2. Intended use and territories (decide commercial terms, counsel review, EU scope).
3. Accept or rename OSTREL and IONA VALE after register searches; "Nell Rowan" found no well-known match in a web search only [U].
4. Locale (open critic conflict): decides police livery, hospital identity and which likeness laws matter.
5. *The Long Places* is AI-written and AI-revised (l.1, l.3): `ai_generated_human_directed`; collect files 10–18 and the user's prompts; use the AI-source credit; invent the Ministry's and the Trust's crests.

## 8. Conflicts and open questions

- **Blueprint versus D4 names (blueprint wins, §6.1):** PROJECT `rights` has five values against D4's nine; map `own_original`→`mine`, `licensed`/`option_held`/`written_permission`→`permission`, `blocked`→`study_only` or stop. `fan_noncommercial` has no blueprint value (proposal). Licences, consent and model terms become RIGHTS records `RT-001`; `consent_record` holds the RT ID, not a file name.
- **R1 versus blueprint step 0:** D4 formerly said "stop at intake"; the blueprint allows `study_only`. Resolved in favour of the blueprint, with a warning that a private adaptation still carries low but non-zero risk [J].
- **`content_flags`:** blueprint list lacks `sexual_content`, `hate_symbol`, `real_institution`; proposed additions.
- **`human_notes`:** not in the blueprint; D5 uses film-level `style_human_notes`. Proposal: shot- and bible-level `human_notes`, with D4-V17 scanning both.
- **D9 licence enum** (`cc0`, `cc_by`, `cc_by_nc`, `royalty_free`, `plan_terms`, `open_weights`, `own_recording`, `unknown`) versus D4 `licence_id` (`cc_by_4_0` etc.): settle one list in the RIGHTS record.
- **D3 vs D4 on EU scope:** D3: a designed voice is "probably not a 'deepfake'"; D4: every photoreal film in scope. Both [J]; the credit line satisfies both.
- **YouTube wording:** older text says "altered or synthetic content"; Studio now says "AI use" (D8 agrees). D18 (captions) is not yet written; D8 carries the credit line meanwhile.
- **Unverified or pending [U]:** SAG-AFTRA contract details; Denmark's likeness right (Commission objected; adoption unconfirmed); *Like Company v Google* (AG opinion due 3 Sept 2026, unchecked); Midjourney case status; Seedance and Sora filters; Mixamo, Z.ai, Firefly, OpenAI terms; Meta and TikTok menu names.

## 9. Section map

| § | Content |
|---|---|
| Header, 1, 2 | Purpose, evidence labels, pipeline gates; terms; principles P1–P9 |
| 3.1–3.2 | Right to adapt (public domain, fan rules, options); copyright in AI output (US, UK, EU) |
| 3.3–3.4 | Style, characters, brands, model filters; likeness and voice laws table |
| 3.5 | Marks, Article 50 dates, platform labels, festivals, tool labels |
| 3.6–3.8 | Content policy by topic and per tool; licences; privacy |
| 4, 5 | Rules R1–R30; Recipes Rec1–Rec7 |
| 6, 6.1, 7, 8 | Fields and D4-V17–V21; blueprint mapping; checklists; failure modes |
| 9, 10 | Worked examples (*The Catch*, *The Long Places*); open questions and links |
| Sources | S1–S62 |
