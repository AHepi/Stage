# D17. World and locale research: country, period, institutions, signage, vehicles, uniforms

*Library file D17. Written 2026-09-27. Test sources: "The Catch" (screenplay, workshop revision of 25 September 2026) and "The Long Places" (prose novella). Web facts checked 2026-09-27; editor's re-check 2026-09-28 (corrections marked "(corrected: …)"). Labels: **[V]** verified (primary source, or two agreeing sources), **[U]** unverified, **[J]** this file's judgment.*

> **What this file is for**
> 1. Decide where and when a story happens, even when the source never says, and record it once in the WORLD record that every later stage reads.
> 2. Research the everyday conventions the camera sees and the ear hears: driving side, signs, traffic lights, vehicles, uniforms, institutions, money, period objects.
> 3. Give an LLM recipes, sources and checks, so a non-technical user gets locale right, or invents a deliberate non-place, without models filling gaps with American defaults.
> 4. Worked on *The Catch* (SC08–SC09 under UK, US and invented options, with effects on B3 staging and C1/C2 mirror plates) and *The Long Places* (central Anatolia, 1999 and 2025–26).

---

## 0. How to use this file

**Where it runs.** Step 3 of the pipeline ("World and style"), after the scene list and plan, before characters, voices, places, light, staging and prompts. Output: the WORLD record, one locale sheet per place, a negative list per period, and one CHOICE for checkpoint B (the user's big-decision stop). D3 reads accents from it, B2 R19 signal colours, B3 driving side, C1 and C2 plate content.

**What it does not repeat.** Streetlight colours and the emergency-light example (B2 §5.4, R19); set dressing as history (B4 §4.3); the flip method and text inserts (C2 §7, R5, R6; C1 Recipe 8); name checks and invented institutions (D4 R17–R19); voice briefs (D3). This file decides the facts those files apply.

### 0.1 Words this file uses

| Word | Plain meaning |
|---|---|
| **Locale** | The real or invented place and time a story happens in, with its everyday habits. |
| **Convention** | One visible or audible habit of a locale: the side cars drive on, the colour of police lights. |
| **Cue** | A word or detail in the source that points to a locale ("torch", "night bus", "muhtar"). |
| **Anchor country** | The real country whose conventions an invented place borrows. |
| **Non-place** | A deliberately invented locale whose conventions are designed, not researched. |
| **Period layer** | One stretch of story time with its own objects, such as 1999 and 2025 in *The Long Places*. |
| **Anachronism** | An object or practice shown in a period when it did not exist, or no longer existed. |
| **Locale sheet** | A short list, per place and period layer, of every convention the camera will see there. |
| **Negative list** | Things that must not appear in a layer, pasted into prompts as exclusions. |
| **Plate** | A background image or clip without the characters, made so they can be composited in later. |
| **Home handedness** | Which way round the everyday world is before a mirror story's turn (for example, traffic keeps left). |
| **Primary source** | The body that makes the rule or runs the thing: a law, an official manual, an institution's own page. |
| **Flip** | Mirroring a finished picture left-to-right in editing software, so everything in it swaps sides and all text reads backwards. |
| **Insert graphic** | Text or a sign made as a separate, exact image (not by the video model) and laid into the shot afterwards (C2 R6). |
| **Near side / kerb side** | The side of the road next to the pavement: the left in a left-driving country, the right in a right-driving one. |
| **Primary signal head** | The traffic light a driver is meant to obey first; where it stands differs by country (§5). |
| **Custom** | An everyday body habit the story uses as a cue, such as which hand wears a wedding ring. |
| **Checkpoint B / CHOICE** | The pipeline's one stop where the user answers the big decisions; a CHOICE record is one such question with its options and a default (blueprint). |

The pipeline's `origin` field (blueprint §5.2) carries A3's labels: `story` = A3 `fact`, `inferred` = `inference`, `invented` = `invention`.

---

## 1. Core principles

1. **Unstated is a decision waiting to be made.** When the source names no country or year, record `unstated`, list the cues, and ask the user once at checkpoint B. The library already shows what silent guessing does: C3 gives every character a British voice, B3 assumes right-hand-drive cars, A3 records the period as unstated.
2. **A locale is a bundle.** Choosing a country sets twenty or more conventions at once: driving side, plates, signs, lights, uniforms, units, money, spelling, sirens. Mixing bundles by accident (British speech, American police lights) reads as error to anyone who knows either country.
3. **Models default to America.** For underspecified prompts, DALL-E 2 and Stable Diffusion produced images that "most reflect the surroundings of the United States followed by India" [V, S15]. Naming the country helped but did not fix it: scores rose by 1.44 points (DALL-E 2) and 0.75 (Stable Diffusion) on a 5-point scale, and "the overall scores for many countries still remain low" [V, S15]. Newer models were not tested there; assume the same pull until your checks show otherwise [J].
4. **Research follows screen time.** A bus seen for two seconds at night needs its shape, colour and number right; its engine does not matter [J].
5. **Period belongs to scenes.** A story can hold several period layers; each gets its own locale sheet and negative list.
6. **An invented place still needs conventions.** Left blank, it does not become neutral; it becomes American (principle 3).
7. **The locale decides what "wrong" looks like.** In a mirror story, a reversed street looks wrong only to viewers who know the home convention; reversed text and a character's wrong reach look wrong to everyone [J].
8. **LLM memory is a lead, not a source.** LLMs state conventions fluently and sometimes mix countries. Anything seen gets a source, or stays [U] and flagged.
9. **Grammar, not names.** Audiences recognise an institution by colours, shapes and layout. Keep the researched grammar; invent names and crests (D4 R19).

---

## 2. Fields this subject adds to the breakdown

The blueprint's WORLD record already has `place, period, drives_on, language, accents, signage, emergency_lights, institutions, money, evidence, origin`. This file fixes their values and adds the rows marked **new**. Records use the blueprint's `- field: value` lines.

| Level | Field | Meaning | Allowed values |
|---|---|---|---|
| film (WORLD) | `place` | Where the story happens | `named:<country>` \| `invented` \| `unstated` |
| film | `anchor` **new** | Country whose conventions an invented place borrows | `named:<country>` \| `own` (all designed) \| `none` |
| film | `region` **new** | Part of the country, if it shows | text \| `unstated` |
| film | `period` | Main story time | year or range and season \| `present` \| `near_future` \| `unstated` |
| film | `period_layers` **new** | Each stretch of time with its own objects | repeat: `P<id> \| span \| scenes \| origin` |
| film | `drives_on` | Home driving side | `left` \| `right` \| `none` |
| film | `language`, `accents` | Language in the world and in the film; accent set | text (`undecided` blocks voice locking, D3 R6) |
| film | `writing` **new** | Alphabet, special letters, spelling, date and time formats | text |
| film | `units` **new** | Units on signs and dashboards | `metric` \| `imperial` \| `mixed:<how>` |
| film | `signage` | Road, street-name and safety-sign style | text: shapes, colours, typeface family, language |
| film | `traffic_signals` **new** | Signal sequence and where heads stand | text |
| film | `emergency_lights` | Light colours and siren family per service | text |
| film | `vehicles`, `uniforms` **new** | Typical vehicles and plates; service dress per layer | text |
| film | `institutions` | Who polices, treats, governs, inspects | repeat: `role \| shown_as \| real_or_invented \| grammar` |
| film | `money`, `tech` **new** | Currency and devices per layer | text |
| film | `customs` **new** | Body habits the story uses as cues | repeat: `item \| convention \| lines \| fact` (The Catch: `wedding ring \| left hand \| l.436–438, l.1779–1783 \| S35`) |
| film | `audience_region` **new** | Main audience, whose conventions decide what looks "wrong" | text \| `mixed` |
| film | `facts` **new** | Each researched convention with its source | repeat: `field \| value \| source: URL \| checked: date \| label: V/U/J` |
| place (LOC) | `real_basis` **new** | Real places or types the set is modelled on | `none` \| text |
| place | `locale_sheet` **new** | Conventions visible here, per layer | repeat: `P<id> \| item \| convention \| fact` |
| scene | `period_layer` **new** | The scene's layer | `P<id>` \| `TIMELESS` |
| scene | `locale_check` **new** | Every locale item here has a sheet entry | `pending` \| `done` \| `n/a` |
| thing (PR, TX) | `period_check` **new** | The object existed in its layer | `ok` \| `anachronism` \| `unchecked` |
| shot | `locale_negatives` **new** | Exclusions compiled into the prompt | list |
| generation job | `handed_check` **new** | Mirror plate checked in home handedness before any flip | `yes` \| `no` \| `n/a` |

**Reconciliation.** D3's `world_accent_rule` expects a `WR-` ID, but the blueprint keeps locale in the WORLD singleton. Point D3's field at `WORLD.accents`; keep `WR-` IDs for story-world rules such as `WR-MIRROR` [J].

---

## 3. Decision rules

*"Then" is firm; "then consider" is a default, broken only with a one-line reason in `notes` (A3's convention).*

**Deciding the world**

- **R1.** If the source names no country or year, then set `place` and `period` to `unstated`, harvest cues (Recipe 1), and write one CHOICE with a default and an alternative for checkpoint B, because accents, plates, signs and lights all depend on it.
- **R2.** If one cue conflicts with the rest, then list it as a question with both readings, because the conflict may be the story's point or a slip.
- **R3.** If a real region holds an invented site, then set `named:<country>`, `region` and the site's `real_basis`, modelled on several real analogues rather than one identifiable place, because copying one site misrepresents it and its community (D4).
- **R4.** If the user wants no real country, then choose `anchor: named:<country>` (borrow conventions, invent names) or `anchor: own` (design everything), because a half-designed place drifts to the model's default.
- **R5.** If the story spans several times, then define `period_layers` and give every scene one, because objects differ by layer.
- **R6.** If a scene should feel outside time (a letter, a ritual), then set `TIMELESS` and use only objects that existed across the whole span implied, with no print, plastic or electric light unless named, because one modern object dates the scene.

**Researching**

- **R7.** If a convention is seen for more than about two seconds in total or in more than one shot, is read, or is heard clearly, then research it from a primary source and record it in `facts`; else a labelled [J] is enough, because research time should follow screen time. (corrected: threshold aligned with the §8 checklist)
- **R8.** If the LLM answers from memory, then mark the answer [U] until a source confirms it, because LLMs mix countries fluently.
- **R9.** If a rule, currency, banknote, institution or uniform has a start date, then check that exact item's date against every layer, not just its series, because what is true today may not have existed in 1999 (Turkey's 10,000,000-lira note is from the same series as 1999's notes but was issued on 5 November 1999, after the story's September [V, S19]).
- **R10.** If a date carries a weekday, age or interval, then compute it; if it names a real event, then check the event, because locals notice a Saturday that was a Tuesday.
- **R11.** If a landmark is visible, then record its bearing from the chosen viewpoint and keep it on that side in every shot, because a mountain on the wrong side reverses the geography.
- **R12.** If an institution is real and identifiable, then invent its name, crest and livery but keep its researched grammar, because audiences read grammar and D4 R19 bars real insignia.

**Generating**

- **R13.** If a prompt shows a street, vehicle, sign, uniform, emergency service or shopfront, then name the conventions in plain words and add the layer's `locale_negatives`, because underspecified prompts drift American.
- **R14.** If readable text uses special letters (Turkish ı, İ, ş, ğ), then make it an insert graphic (C2 R6) and check each letter, because models drop letters they rarely saw.
- **R15.** If a sound belongs to the locale (siren pattern, church bell, call to prayer), then record it in WORLD and pass it to D9, because sound places a film as fast as picture.

**Mirror stories**

- **R16.** If the story mirrors the world, then record home handedness in WORLD, generate every mirror plate in home handedness, check it (`handed_check: yes`), and only then flip, because a plate that drifted to the other driving side flips into a normal-looking street.
- **R17.** If a mirror effect depends on the audience knowing the home convention, then carry it with a universal cue too (reversed text, a wrong reach), because driving side looks wrong only to viewers who share it.
- **R18.** If a number or word must visibly read backwards, then use characters that change when mirrored (for example B, C, D, E, F, G, J, K, L, N, P, R, S, Z, 2, 3, 4, 5, 6, 7, 9), not ones that barely do (A, H, I, M, O, T, U, V, W, X, Y, 0, 1, 8), because a mirrored symmetric character looks unchanged.
- **R19.** If no street appears before the mirror turn, then consider one added establishing shot in home handedness, logged `origin: invented`, because otherwise each viewer's own country is the only reference.
- **R20.** If the locale changes staging (driver's seat, reaching hand), then redraw the floor plan from WORLD before writing shots, because every frame-left/right in the scene flips with the driving side.
- **R21.** If the story uses a sided body custom as a cue (which hand wears a wedding ring), then record the home convention in WORLD `customs` and check it against the chosen country or anchor, because customs differ: the wedding ring is worn on the left hand in the UK and the US [U, S35: secondary sources agree] but placed on the right hand at the wedding in Germany, Austria, Bulgaria, Poland and Russia [V, S35]; in Turkey it is usually worn on the right during the engagement and moved to the left at marriage [U, S35], so the wrong anchor makes the cue read backwards.
- **R22.** If a mirrored sign has an official mirror-image twin (ISO 7010 has both "Emergency exit (left hand)" E001 and "(right hand)" E002 [V, S31]), then do not count on it to look wrong by itself: carry the wrongness with reversed text or the character's reaction, because a reversed running man is still a valid sign.

---

## 4. Recipes

Paste each prompt into your LLM; replace the bracketed parts.

### Recipe 1. Harvest locale cues (10 minutes)

1. Give the LLM the numbered source.
2. Paste: *"List every word or detail that points to a country, region, period or social world: spelling, vocabulary (torch/flashlight, lift/elevator), institutions, uniforms, vehicles, signs, units, money, technology, food, weather, landmarks, and body customs (which hand wears a ring, greetings). For each: line number, exact quote, what it points to, strong or weak. Then list anything that conflicts with the majority. Do not decide the country."*
3. Check three quotes against the source yourself; if any is not word for word, ask for a redo.
4. The list goes into WORLD `evidence`, each item `origin: inferred`.

### Recipe 2. Choose the world (15 minutes)

1. Paste: *"From the cue list, propose a default world and one alternative: place (named country, invented with an anchor country, or invented with its own conventions), period, driving side, language, accents. For each, list what it forces us to change in the source, the extra reference images it costs, and what it does to any story-world rule such as a mirror. Recommend one, with a reason."*
2. The LLM writes one CHOICE record (`checkpoint: b`, `asked: yes`, `affects` naming voices, places, rules and staged scenes).
3. The user's answer at checkpoint B sets `place`, `anchor`, `period`, `drives_on`, `language`.

### Recipe 3. Research each convention (30–90 minutes per locale)

1. Paste: *"For the world [answer], list the conventions the camera or ear will meet in these scenes: [scene IDs with one-line summaries]. For each: what it looks or sounds like, which scenes, how long it is seen, and the best primary source (law, official manual, the institution's own site). Order by screen time. Mark anything stated from memory [U]."*
2. Have the LLM search the web for the top items, using §5. Each checked item becomes a `facts` line.
3. For how things look, collect two real photographs per item (Street View for the present; Wikimedia Commons or newspaper archives for the past) as reference images. In Google Maps, drag the little person onto a street to enter Street View, then click "See more dates" and scroll the thumbnails to go back in time; "Historic imagery isn't available for every place that has Street View" [V, S27]. Save each photo with its place and date in the file name.
4. Stop when every item seen for more than about two seconds, or read, has a source or a flagged [U]/[J].

### Recipe 4. Locale sheets and negative lists (20 minutes)

Paste: *"For each place and each period layer, write a locale sheet: every convention visible there, each pointing to a `facts` line. Then write a negative list per layer: things a model is likely to add wrongly (other countries' police lights, school buses, modern phones in the past, wrong script on signs)."* Copy each negative list into the matching shots' `locale_negatives`.

### Recipe 5. Anachronism sweep (20 minutes per layer)

Paste: *"For layer [P1999], go through every scene in it and list every object, vehicle, garment, light source, device, sign and sound. For each, say whether it existed and was ordinary in [place] in [year]; give a source for anything doubtful. Flag anything common in recent photos of this place that did not exist then."* Set each `period_check`; any `anachronism` goes back to the scene as a replacement or a question.

### Recipe 6. Design a non-place (45 minutes)

1. Decide `anchor`: borrow one country (fast; reads as that country with names filed off) or `own` (slow; reads as nowhere).
2. For `own`, paste: *"Design a locale bible for an invented city: driving side, plates, street-name and road signs, traffic signals, police and ambulance colours and sirens, buses, taxis, safety signs, money, spelling, units, one typeface family for public signs, and every body custom the story uses as a cue (for The Catch: wedding rings on the left hand). Keep it simple, consistent, and unlike any single country's full set. Avoid combinations that already mean something (amber beacons read as tow trucks in many countries)."*
3. Make one reference image per convention (C2); no model knows the design.
4. Run D4's name check on every invented name.

### Recipe 7. Check frames for locale (2 minutes per frame)

Ask an LLM that can see images: *"Check this frame against the locale sheet [paste]: driving side, steering-wheel side, plate colours, sign shapes and colours, light colours, uniforms, vehicle types, alphabet and spelling, landmarks and their side, which hand wears a ring. List every mismatch."* Fix by inpainting or regeneration (C2). For a mirror plate, run it **before** flipping.

---

## 5. Research sources and checks for each field

| Field | Best sources (examples checked) | Check | Common trap |
|---|---|---|---|
| place, region | The source's cues (Recipe 1) | Two strong cues agree; conflicts listed | Accent chosen before place |
| period, layers | The source; a calendar | Ages, weekdays, intervals add up (R10) | Present-day objects in past layers |
| drives_on | Traffic law. UK Highway Code rule 160: "keep to the left" [V, S1]. California Vehicle Code 21650: "driven upon the right half of the roadway" [V, S10]. Turkish Law 2918 art. 46: "Karayollarında trafik sağdan akar" (on roads, traffic flows on the right) [V, S16] | Wheel side, bus doors and overtaking side agree | Model generates the other side |
| traffic_signals | UK: RED, RED AND AMBER, GREEN, AMBER [V, S2]; primary head "beyond the stop line… normally on the near side", "at least 1.5 m from the stop line, although 2.5 m is preferable", secondary "usually placed on the far side of the junction" [V, S3]. US: primary faces "No less than 40 feet beyond the stop line" and no more than 180 feet unless a near-side supplemental face is added (MUTCD §4D.08) [V, S13] | Where the red spills from in a car | Overhead American signals in a British street |
| emergency_lights | UK: no vehicle "other than an emergency vehicle or a vehicle used for special forces purposes" may be fitted with a blue warning beacon [V, S4]. California: "at least one steady burning red warning lamp visible from at least 1,000 feet to the front" is required [V, S11]; flashing blue is allowed on peace officers' emergency vehicles (§25258) [V, S11] (corrected: was [U]) | Lights match service | Red-and-blue bars outside North America |
| signage | UK escape signs: "rectangular or square shape", "white pictogram on a green background" [V, S5]; ISO 7010 E001 "Emergency exit (left hand)" and E002 "(right hand)" are mirror twins [V, S31] (corrected: was [U]). US exits need "the word 'Exit'" at least six inches high [V, S12] | The exact words the script names | A running-man sign in a US building unremarked |
| workplace safety signs (factory, lab, plant) | UK Sch. 1: prohibition "round", red edging and diagonal; warning "triangular", black on yellow; mandatory "round", white on blue; fire-fighting equipment white on red [V, S5] | Shape and colour pair match the meaning | A yellow sign used for an instruction |
| hospital | The institution's own site for signage and uniforms; D4 R19 for names and logos [J] | Invent the trust or hospital name; keep colours and layout | A real NHS logo or trust name [J] |
| units | UK roads: speed limits in mph (Highway Code rule 124) [V, S36]; science, medicine and most labels metric [J]. US: imperial on roads and most labels [J]. Turkey: metric (§7) | Road signs and dashboards agree with WORLD `units` | km/h signs in a British street; metres on a UK road sign |
| customs | Ethnographic and reference sources; two agreeing sources before [V] (S35) | The script's own lines win over any general custom | Anchor country with the opposite ring hand (R21) |
| vehicles, plates | UK: front plates black on white, rear black on yellow; current format since 2001 [V, S7]. Turkey: plates begin with a province code, 06 Ankara, 38 Kayseri, 50 Nevşehir [V, S32] | Plates unreadable or invented | Real registrations, real liveries |
| buses | London night routes carry an N prefix [V, S8] (the TfL map refused automated access on re-check; route pages such as N29 confirm the prefix); TfL's answer on bus blinds says new buses use white lettering on black [U, S9: search summary only]. San Francisco's late-night network is "Owl", running "every half hour between 12 a.m. and 5 a.m."; "Every Muni bus is equipped with two or three bike racks on the front" [V, S14] (corrected: was [U]) | Door side follows driving side | Yellow school buses in any night street |
| institutions | Founding laws, own sites. Jandarma's area is outside the police's: places beyond provincial and district municipal limits, or with no police organisation; since 2015–2016 amendments parts of a municipality or a whole district can be assigned either way [V, S17]; AFAD founded by Law 5902, accepted 29 May 2009, Official Gazette 17 June 2009 [V, S18] | Start dates against layers (R9) | Today's agencies in 1999 |
| uniforms | Clothing regulations; dated press photos. Turkey's current Jandarma dress regulation was published in the Official Gazette of 31 March 2020, no. 31085 [V, S30] (corrected: "redesigned in the 2010s" was unsupported); what the 1999 dress looked like needs dated photos [U] | Layer dates | Current uniforms in past layers |
| weapons | Firearms law. UK Firearms Act 1968 s.5(1)(aba) prohibits "any firearm which either has a barrel less than 30 centimetres in length or is less than 60 centimetres in length overall" (air weapons, muzzle-loaders and signalling devices excepted), which covers ordinary pistols [V, S6] | Does the carrier make sense? | Armed private guards in Britain |
| money | Central banks. Turkey's 7th banknote series (E7) ran to 20,000,000 lira and was withdrawn on 1 January 2006 [V, S19]. Issue dates matter within a series: 5,000,000 on 6 January 1997; 10,000,000 on 5 November 1999; 20,000,000 on 5 November 2001 [V, S19]. Law 5083 (Official Gazette 31 January 2004) set 1,000,000 old lira = 1 new lira, with old notes circulating alongside through 2005 [V, S20] (corrected: was [U]) | Prices and notes fit the layer's exact dates | New notes in old layers |
| tech | Operators' histories. Turkcell began Turkey's GSM service in February 1994 [V, S22] | Rural coverage [U] | Smartphones in 1999 |
| landmarks | National survey bodies. Erciyes: MTA's own page gives 3,864 m in its data box and 3,916 m in its text; Wikipedia gives 3,864, 3,917 or 3,918 m [V, S24: the sources disagree, even within MTA] (corrected: the first version credited MTA with one figure). Kayseri lies 15–25 km north of the volcano [U, S24] | Side of frame per viewpoint | Mountain swaps sides |
| look of the present | Google Street View; "See more dates", though "Historic imagery isn't available for every place" [V, S27] | Two photos per item | One photo taken as the rule |
| look of the past | Wikimedia Commons by year and place; newspaper archives; museum collections [J] | Photo date and place stated | Films and reconstructions as evidence |

---

## 6. The Catch: SC08–SC09 under UK, US and invented options

### 6.1 The cues

The script never names a country. Cues from Recipe 1 (all `origin: inferred`):

| Line | Quote | Points to | Strength |
|---|---|---|---|
| 59 | "I know how a lift works, Io." | British "lift" | strong |
| 69 | "She puts the torch between her teeth" | British "torch" (flashlight; B2's prompt warning) | strong |
| 149, 325 | "A practised lift."; "Stencilled on the wall in big letters" | British spelling | medium |
| 331 | "the green sign is backwards too. The little running man is running the other way." | Green running-man exit sign: UK and ISO practice, not US "Exit" wording | strong |
| 341 | "on the wrong side of the gearstick" | British "gearstick"; a lever on the centre console | medium |
| 370 | "A night bus comes at them with its number written backwards." | British "night bus" (some US cities say "owl") | medium |
| 1587 | "UPWARD SPEED, in metres per second." | Metric, British spelling | medium |
| 214, 399 | "the grey maintenance opening"; "DR SAYE, fifties, grey and tidy" | British "grey"; "DR" without a full stop is British style | medium |
| 24, 834 | "comes round the cage"; "A second cooling cup of tea." | British "round"; tea | weak |
| 436–438 | "Saye's wedding ring. On her right hand." / "Iona looks down at her own ring, on her own left hand." | Home convention: wedding ring on the left hand (UK, US), not a right-hand-ring country such as Germany or Poland (R21) | strong, for `customs` |
| 183 | "A GUARD comes out of a side room, pistol half drawn" | Armed private guard: normal in the US, a serious crime in the UK | **conflict** |
| 492, 1004 | "Police lights beyond frosted windows." | Colour not given | none |

**Period.** No year. Wrist displays, tablets, security feeds and a courier that vanishes point to present day or near future [J]; the title-page date is the writing date. Set `period: near_future`, `origin: inferred`, and let D5 decide how far from today. (The blueprint's K27 default says "present day"; see §11 Q5. Tablets, security feeds and wrist displays exist today, and the ship is not human technology, so `present` is an equally defensible default; the visor's live readouts are the strongest near-future cue [J].)

**The ring (R21).** The script shows both hands at once: Saye's ring "On her right hand", Iona's "on her own left hand" (l.436–438), and at the end Jude's "On his right hand" beside Iona's left (l.1779–1783). The cue works inside the film for every viewer because the right way is shown next to the wrong one. It fixes WORLD `customs: wedding ring | left hand`. Options A and B already use the left hand; option C must design it as left; an anchor country that puts the ring on the right hand at the wedding (Germany, Poland, Russia [V, S35]) would make the home convention look mirrored.

**The exit sign (R22).** "The little running man is running the other way" (l.331) works because Iona knows which way this door's sign ran, not because the reversed figure is unofficial: ISO 7010 has left-hand and right-hand versions (E001, E002) [V, S31]. Keep the stencil's reversed letters in the same scene (C2 W2) so the audience sees the wrongness before she names it.

**The conflict (R2).** In the UK a guard's pistol is a prohibited weapon under Firearms Act 1968 s.5(1)(aba) [V, S6]. Either the operation is criminal and the pistol is part of the proof (it fits Saye's "The men who kept him are not."), or the world is not the UK. Ask the writer; never quietly swap the pistol for a baton. Option A's `invented` place softens the conflict without removing it: the invented city's law may allow armed guards, but a viewer who reads the streets as British will still read the pistol as exceptional, so the film should treat it as exceptional either way [J]. (The blueprint's K27 wording, "an unnamed British city", is closer to `named:UK` with `region: unstated`, which keeps real UK law and makes the conflict sharp; §6.5's CHOICE decides which.)

### 6.2 Three world options

| Field | A: invented city, UK anchor (default) | B: unnamed US city | C: non-place, own conventions |
|---|---|---|---|
| `place`, `anchor` | `invented`, `named:UK` | `named:US` | `invented`, `own` |
| `drives_on` | left | right | chosen; left keeps the script's cues coherent |
| `accents` | British set (D3 locks) | American set; every C3 sound key changes | Designed, non-regional |
| `signage` | Green running-man signs [V, S5]; British-style road signs, invented names | Red or green signs with the word "Exit" [V, S12]: the running-man line needs the writer, or an international sign logged as a choice | Designed; all composited |
| `traffic_signals` | Red, red+amber, green, amber [V, S2]; primary head at the stop line, near side [V, S3] | Heads 40–180 ft beyond the stop line [V, S13], often overhead [U]; no red+amber [U] | Designed |
| `emergency_lights` | Blue only [V, S4] | California: steady red required to the front [V, S11]; blue allowed on peace officers' vehicles [V, S11] | Designed; avoid amber |
| `vehicles` | Right-hand drive; manual gearstick common [J]; double-deck night bus with an N-prefixed number [V, S8] | Left-hand drive; single-deck bus, front bike rack [V, S14] | Designed |
| `customs` | Wedding ring on the left hand (script l.436–438) | Same | Design as left; never borrow a right-hand-ring anchor (R21) |
| `units` | Mixed: mph on road signs [V, S36]; metric on the visor (l.1587) | Imperial on roads; a technical visor in metric still fits a US science setting, but the insert must spell it "meters" [J] | Designed; metric keeps l.1587 |
| `institutions` | Invented trials inspectorate, hospital and police crest (D4 R19) | Invented federal agency and county police | All invented |
| Guard's pistol | Conflict: ask | Normal | As designed |
| Reference burden | Low, but check for American drift | Lowest: the models' default | Highest: about a dozen extra reference images |

**Default [J]: option A.** It fits every cue but the pistol, keeps C3's voices as proposals and B2's and B3's assumptions as written. Option B rewrites the exit-sign line and flips every side in SC09. Option C buys a world no viewer can call wrong, at the price of designing it.

### 6.3 Effect on B3's SC09 staging

B3 §8.5 works SC09 out for a left-driving home. The camera shares Iona's frame, in which the world is mirrored (A3 Ex4):

| Staging item | A: UK anchor (B3 as written) | B: US | C: non-place |
|---|---|---|---|
| Her own car | Wheel on the right; gearstick at her left hand | Wheel on the left; selector at her right hand | Follows `drives_on` |
| "Iona walks to the driver's door. Opens it." / "The passenger seat." | By habit she goes to the car's right-hand side; on screen that door opens on the passenger seat | Left-hand side; same result, mirrored | Follows |
| On screen | Car looks left-hand drive, driving on the right | Looks right-hand drive, driving on the left | Opposite of home |
| Frontal two-shot through the windscreen | Iona frame-right, Eli frame-left | Iona frame-left, Eli frame-right | Follows |
| "Reaches for the gearstick. / Hits the door." | Left hand, toward the frame-right edge | Right hand, toward the frame-left edge | Follows |
| "Everything in her wants to be on the other side of the road." | In her forward view, her pull is to screen-left, into the oncoming lane | Pull to screen-right | Follows |
| "A night bus comes at them" | In her forward view, the oncoming bus is in the screen-left lane as she drifts (inference) | Screen-right lane | Follows |
| "A red light." | Nearest red: the primary head on a pole 1.5–2.5 m past the stop line on the kerb side [V, S3], so when the car stops at the line it stands a few metres ahead of the front corner on Eli's side, seen through the windscreen and his side window (the mirrored world keeps right, so the kerb is on the car's right: Eli's side, frame-left in the frontal two-shot), plus a far-side secondary [S3] (corrected: side wording clarified) | Red ahead across the junction, farther and higher [S13]: a weaker, even wash on both faces [J] | Designed |
| "The dashboard clock, which she has to work out like a child." | An analogue dial suits the line best [J] | Same | Same |

Two things hold in every option. The rear-view mirror is central, so B3's key shot, Eli's eyes in the mirror, stands. And "Hits the door." needs a gear lever on the centre console: a column stalk, rotary dial or buttons would kill the beat, so the locale sheet says `vehicles: gear lever on centre console, cup holder beside it` (the cup holder serves SC08's "on the wrong side of the gearstick") [J].

**Light (B2 Example 3).** In option A the red comes close, from a pole lower than an overhead signal, and from the kerb side, reaching Eli first, which suits B2's plan to put red on the side of his face toward the windscreen. In option B it comes from ahead and above; the plan still works with a weaker wash [J].

### 6.4 Effect on C1 and C2 mirror plates

C1 Recipe 8 and C2 R5 generate the world the right way round, then flip it. WORLD decides what "the right way round" is:

| Plate before the flip | A: UK anchor | B: US | C: non-place |
|---|---|---|---|
| Traffic | Keeps left | Keeps right | As designed |
| Cars | Wheel on the right; plates white front, yellow rear [V, S7], left blank for inserts | Wheel on the left; state plates, blank | Designed plates |
| Night bus | Double-deck, entrance at front left [J]; blank display, then an `N29` insert | Single-deck, entrance front right, bike rack | Designed |
| Signals | Near-side heads at stop lines | Far-side and overhead heads | Designed |
| Street names, shop signs | Blank, then British-style inserts with invented names | Blank, then US-style inserts | Designed inserts |
| After the flip | Looks left-hand drive, on the right, text reversed | Looks right-hand drive, on the left, text reversed | Mirror of design |

**The bus number (R18).** Flipped, `N29` shows a reversed 9, 2 and N in reverse order; the reversed N looks like the Cyrillic "И" and reads as wrong at a glance. Numbers built from 0, 1 and 8 barely change. Make the display an insert graphic before the flip (C2 R6), as C2 W2 does for the stencil [J]. N29 is a real, busy London night route (Trafalgar Square to Enfield) [U, S8]; under option A, where the city is invented, any N-number will match or nearly match some London route, which is harmless (a route number identifies no person) but points viewers at London; choose a number with no London association if that matters [J].

**The handedness check (R16).** Before flipping, run Recipe 7 on the unflipped plate: "Is traffic keeping left? Is every wheel on the right?" If the model drifted to American traffic, the flipped plate shows traffic keeping left with right-hand-drive cars: a normal British street with backwards text. Half the scene's effect vanishes, and nobody notices until the edit. Set `handed_check: yes` only after this check.

**Who sees the wrong side (R17, R19).** SC01–SC07 show no street and no car in home handedness, so the audience has no in-film reference. Under option A a British viewer sees a foreign-looking street; an American viewer sees a normal one. The reversed text, "Io. Your dashboard's on backwards.", and the reach that "Hits the door." carry the effect for everyone. If the traffic side must read for all viewers, consider one invented shot of Iona's car arriving in home handedness before SC01, logged `origin: invented`, costing about one generation [J].

### 6.5 The CHOICE record for checkpoint B

```
### CHOICE CHOICE-0NN Where and when The Catch happens
- question: Where and when does the story happen?
- why: accents, signs, police lights, the car and night-bus shots, and every left/right in SC08–SC09 depend on it
- option: a | text: an unnamed British-style city, near future; drives on the left; invented institutions
- option: b | text: an unnamed US city, near future; drives on the right; the exit-sign line needs the writer
- option: c | text: an invented place with designed conventions; about a dozen extra reference images
- default: a | reason: every cue but the pistol is British; keeps C3 voices, B2 light and B3 staging
- asked: yes
- checkpoint: b
- affects: WORLD, VO-IONA, VO-JUDE, VO-ELI, VO-SAYE, VO-NELL, LOC-STREET, LOC-IONA-CAR, SC07, SC08, SC09, SC11, SC18, WR-MIRROR
- sets: WORLD.place | value: invented | when: a
- sets: WORLD.anchor | value: named:UK | when: a
- sets: WORLD.drives_on | value: left | when: a
- sets: WORLD.place | value: named:US | when: b
- sets: WORLD.drives_on | value: right | when: b
- based_on: D17 §6; B3 §8.5; B2 R19; C3 §7B; D3 R6
```

A second, small CHOICE asks about the pistol (R2). The options above say "near future"; the blueprint's K27 says "present day". Put that as one line inside this CHOICE's answer ("present or near future?") rather than a separate stop, since checkpoint B holds at most seven items [J]. The ring hand (R21) needs no question: all three options keep it on the left.

---

## 7. The Long Places: Kırk Oda and Erciyes, 1999 and the present

### 7.1 Cues and the WORLD record

Here the country is fixed by the text, though the word "Turkey" never appears: real places (Kayseri, Ankara, Derinkuyu, Cappadocia) and the village's language ("in Turkish a plainer thing", l.419) settle it, so `place` is `origin: story`. (corrected: the first version said "stated") The risk is getting a real place wrong.

| Line | Quote | Points to |
|---|---|---|
| 37 | "The road gave up two villages before hers, and the minibus gave up with it" | Village at the end of a minibus route |
| 37 | "Erciyes stood up out of the haze to the east with snow on it" | Village west of Erciyes; snow in June |
| 41 | "excavation and survey, Kırk Oda, 2025 season" | Present layer: 2025 |
| 63 | "In the second week of June the muhtar called the village to the room above the co-op to discuss the dig." | Muhtar (the elected village headman); a co-op with an upstairs room |
| 71 | "from the near side of Derinkuyu, who introduced himself and his phone tripod in the same breath" | Nevşehir province nearby; smartphones |
| 130 | "By noon there were gendarmes, and dogs from Kayseri" | 1999 layer; Jandarma in a village; Kayseri the nearest city |
| 61 | "Every time, she set it by the church bell" | A church bell in the grandmother's time |
| 419 | "The answering niche, the village called it, in Turkish a plainer thing." | The village speaks Turkish |
| 625 | "Cappadocia kept hermits in its caves into living memory" | Region named |
| 805, 1181 | "Frost took the hill in the second week of November"; "The dig closed the way the season closed in that country: by letter, in the last week of August." | The present layer runs through a winter into a second season |
| 1289 | "the village kept it the way it had kept it for twenty-seven years"; "He would be forty." | Chapter XIV is 4 September 2026 |

```
### WORLD
- place: named:Turkey
- region: central Anatolia between Kayseri and Nevşehir (inferred: Erciyes to the east, Derinkuyu near, hospital in Kayseri)
- anchor: none
- period: June 2025 to October 2026
- period_layers: P2025 | span: June 2025 – Oct 2026 (two dig seasons and the winter between; ch. XIV is 4 Sept 2026) | scenes: most | origin: story
- period_layers: P1999 | span: late Aug–Sept 1999 | scenes: ch. I–II flashback | origin: story
- period_layers: P1924 | span: 1924 | scenes: only if the founder's notes are shown | origin: story
- period_layers: TIMELESS | span: the letter scenes | origin: invented (A3 Ex5 "PERIOD UNSTATED")
- drives_on: right
- language: Turkish in the world; film language is a user choice
- writing: Latin alphabet with ı İ ş ğ ç ö ü; dd.mm.yyyy; 24-hour
- units: metric
- institutions: village government | shown_as: muhtar and stamp | real | grammar: round office stamp, a file
- institutions: rural police | shown_as: Jandarma | real | grammar: military-style uniform per layer
- institutions: heritage permits | shown_as: "the Ministry" | real | grammar: folders, stamps, the Ministry's representative on site [V, S25]
- institutions: the Trust | shown_as: Anchorhold Trust, Valletta | invented | grammar: hand-copied letters
- money: 2025–26 lira; 1999 old lira in millions (largest note then: 5,000,000)
- audience_region: mixed
```

(corrected: the first version ended the present layer in September 2025; the book runs through the winter to a second season closing "in the last week of August" and a report "In October" (l.1407), and chapter XIV's "twenty-seven years" puts it on 4 September 2026.)

**Site (R3).** A search found no real site called Kırk Oda [U, S33]; treat the complex and village as invented in a real region. `real_basis`: Cappadocian underground complexes such as Derinkuyu, where, per Nevşehir's governorate, the 8 levels open to visitors reach 50 m, the full complex is estimated at 85 m and 12–13 levels, and the name comes from 52 wells 60–70 m deep [V, S26] (corrected: the first version gave 60–70 m as the depth of the open levels); no single site copied.

**The mountain (R11).** Erciyes is "to the east". Every exterior looking east shows it; no shot looking west may. Sources disagree on its height (§5); on screen it is one high, snow-patched volcanic cone, constant in size between shots [J].

### 7.2 Checks the text passes, and one it raises

| Claim | Check | Result |
|---|---|---|
| "The fourth of September was a Saturday" (l.130) | Calendar | 4 September 1999 was a Saturday [V, computed] |
| Nilay 18 in 1999, 44 now; "Twenty-six years" | Arithmetic | Consistent with 2025 [V, computed] |
| "That was the Thursday. It was the fourth of September." (l.583, 2025) | Calendar | 4 September 2025 was a Thursday [V, computed] |
| "twenty-seven years"; "He would be forty." (l.1289) | Arithmetic: missing at 13 in 1999 | 13 + 27 = 40, so chapter XIV is 4 September 2026 [V, computed] |
| "The shaking that year had all belonged to the northwest" (l.126) | 17 August 1999 İzmit earthquake | USGS gives M7.4 in a paper and M7.6 on its event page [V, S23]; northwest either way |
| Gendarmes, not police, search a village | Law 2803 art. 10 | Rural areas are Jandarma's [V, S17] |
| No disaster agency in 1999 | AFAD: Law 5902, Official Gazette 17 June 2009 [V, S18] | Consistent; and a prompt warning (§7.4) |
| "she set it by the church bell", repeated in the 1924 notes | Lausanne Convention VI, signed 30 January 1923; compulsory exchange of Orthodox Christians from 1 May 1923 [V, S29] | The remaining Cappadocian Orthodox communities were sent to Greece in 1924 [V, S34], so a church bell rung in a village in the region in early 1924 is plausible, and the notes may record one of its last years. A question for the writer (was there a Christian quarter, and did the 1924 survey come before it left?), not an error [J] (corrected: the first version called 1924 "tight") |

### 7.3 Period sheet: the lamps, the co-op and the muhtar meeting

| Item | TIMELESS (letter) | P1999 | P2025 | Source or label |
|---|---|---|---|---|
| Keeper's lamps | Small open oil lamps in niches; wick pinched by hand; no can, no plastic, no label | Same lamps; Nilay takes "the tin lamp from the niche" (l.136) | Filled "from a tin can that smelled of the press" (l.47) | Story. Linseed oil (*bezir*) fits "the press": rock-cut and masonry *bezirhane* oil presses survive in Nevşehir, Kayseri, Niğde, Kırşehir and Aksaray, and the oil was used in Anatolia "kandil yağı olarak aydınlatmada" (as lamp oil for lighting) until recent times [V, S28] (corrected: was [U]) |
| Other light | None | Gendarmes' "electric torches" (l.132): incandescent, yellowish, weak [J] | Headlamps (l.601), phone lights, a generator (l.116): white LED [J] | A light-colour marker between layers for B2 |
| The co-op | — | Not shown in ch. I; if shown, a counter, scales, a ledger [J] | "the room above the co-op" (l.63); "the drawer under the ledger weights" (l.118); still sells "the green soap, the one in the green paper" (l.427) | Story |
| The muhtar | — | Newly in office: local elections were held on 18 April 1999 [V, S21], with headmen elected the same day [U: search summaries only] | In office since 31 March 2024, when village voters cast ballots for "Muhtarlık ve İhtiyar Meclisi" (headman and elders' council) alongside the provincial assembly [V, S21] (corrected: was U) | Office stamp on the consents, "forty of them, signed and stamped" (l.63) [J] |
| Meeting room | — | — | Plain upstairs room, chairs, a table for the file, tea; a flag and a portrait of the republic's founder are common in official rooms [J] | The portrait is a real person: set dressing only, checked with D4 |
| Paperwork | A hand-written letter | Gendarmerie file, read "in a room smelling of paraffin and gun oil" (l.122) | Ministry folder (l.41); registered post held at the co-op (l.118) | Story |
| Phones | None | GSM existed from February 1994 [V, S22]; village coverage [U]; a landline if any | Smartphones, livestreams, "the dig-house number" (l.354) | Story; layer rule |
| Money | None | Old lira in millions; the largest note in August–September 1999 was 5,000,000 (issued 6 January 1997); no 10,000,000 (5 November 1999) or 20,000,000 (5 November 2001) [V, S19] | Current lira; six zeros removed on 1 January 2005 [V, S20] | Only if bought on screen ("red ribbon at the bazaar", l.134; Melek "knew the price list to the lira", l.969) |
| Vehicles | None | Minibus, tractor, gendarmerie vehicle: dated photos needed [U] | Minibus (l.37), "Kemal's tractor" (l.71), "two cars from Ankara" (l.583) on 06 plates [V, S32]; local cars on 38 or 50 | Invent the characters after the code |
| Uniforms | None | Gendarmerie dress of the period: dated photos needed [U] | Current dress regulation dated 31 March 2020 [V, S30]; match recent dated photos (corrected: "redesigned in the 2010s" removed as unsupported) | Crests and ranks unreadable (R12) |

### 7.4 Negative lists

- **TIMELESS:** no electric light, metal cans, print, plastic, wristwatches, zips or modern fabric sheen [J].
- **P1999:** no smartphones, LED light, drones or new-style lira, and no 10- or 20-million-lira notes (issued after September 1999 [V, S19]); no AFAD orange-and-navy rescue uniforms, since the agency did not exist until 2009 [V, S18] and recent Turkish earthquake photographs are full of them [J].
- **P2025:** no American-style police cars or school buses; Turkish text only, with correct ı and İ (R14); Erciyes keeps snow in June unless the user chooses otherwise [J]. The layer includes a winter (frost from November, l.805) and a second summer, so its locale sheet needs snow-and-frost variants of the hill and the mouth [J].

### 7.5 Worked locale sheet: the muhtar meeting (A3 Ex5, scene 6)

```
### LOC LOC-COOP-UPSTAIRS The room above the co-op
- real_basis: a village co-operative building in central Anatolia; no single real building
- locale_sheet: P2025 | item: forty consent forms | convention: muhtar's round office stamp | fact: S21, J
- locale_sheet: P2025 | item: tea in small glasses on saucers | convention: village hospitality | fact: J
- locale_sheet: P2025 | item: men and women present | convention: the scene needs a couple who contradict each other ("One man remembered a scarf; his wife remembered no scarf.") | fact: story
- locale_sheet: P2025 | item: window over the lane | convention: Nilay looks back up at it from the stairs | fact: invented (A3 Ex5)
- locale_negatives: no suits and ties on villagers, no microphones, no projector, no English signs
```

---

## 8. Checklists

**Before checkpoint B**
- [ ] Cue list with exact quotes and line numbers; conflicts listed as questions.
- [ ] One CHOICE with default, alternative, cost and `affects`.
- [ ] Period layers defined; every scene has `period_layer`.
- [ ] D3 told whether accents are decided.

**After checkpoint B**
- [ ] Every WORLD field filled, or `unstated` with a reason.
- [ ] Every convention seen for more than about two seconds, read, or heard clearly has a `facts` line with URL, date and label.
- [ ] Start dates checked per layer (R9), down to each banknote's issue date; weekdays, ages and events checked (R10).
- [ ] Real institutions renamed, grammar kept (R12); negative list per layer copied into shots.
- [ ] `customs` filled for every sided body cue the story uses, and checked against the anchor (R21).
- [ ] `units` agree between road signs, dashboards and on-screen instruments.

**Per place**
- [ ] `real_basis` recorded; no single real site copied.
- [ ] Landmarks on the right side for each camera direction (R11); two reference photos per major item.

**Per generated frame**
- [ ] Recipe 7 run: driving side, wheel side, plates, lights, signs, uniforms, alphabet.
- [ ] Mirror plates: `handed_check: yes` before the flip; reversed characters chosen by R18.

---

## 9. Failure modes

| Failure | How it shows | Fix |
|---|---|---|
| American default | School bus, red-and-blue bar, overhead signals in a British street | R13; Recipe 7 |
| Mixed bundle | British voices, American exit signs | R1: one WORLD record read by all |
| Flipped the wrong way | Mirrored street looks normal | R16: check before flipping |
| Invisible reversal | Bus number looks the same backwards | R18 |
| Present in the past | AFAD vests, smartphones, LED light in 1999 | Recipe 5; P1999 negatives |
| Timeless scene dated | A tin can or print in the letter scene | R6 |
| Garbled local letters | "Kirk Oda" without ı; wrong İ | R14 |
| Real institution shown | NHS logo, real police crest | R12; D4 R19 |
| Swapped landmark | Erciyes in the west in one shot | R11 |
| Confident wrong fact | LLM gives a country a sign it does not use | R8 |
| Staging on the wrong side | Iona frame-left in one shot, frame-right in the next | R20 |
| Real registration | A readable plate that belongs to someone | Keep plates unreadable, or invent and check (D4) |
| Custom reversed by the anchor | Wedding rings on the "wrong" hand in the home world | R21: record `customs`; pick an anchor with the same ring hand |
| Mirror sign that looks normal | A reversed running man read as an ordinary exit sign | R22: pair it with reversed text or a reaction |
| Note from the future | A 10,000,000-lira note in September 1999 | R9: check each note's issue date |

---

## 10. Saying it to image and video models

Name conventions, not only countries; city and brand names pull in landmarks and logos (D4). Put locale early in the prompt and attach reference photos for anything that must match [J].

| Breakdown term | Model phrase |
|---|---|
| `drives_on: left` | "traffic keeps to the left; right-hand-drive cars, steering wheels on the right" |
| UK emergency lights | "only blue flashing lights, no red" |
| UK exit sign | "a small green rectangular sign with a white running-figure pictogram above the door, no words" |
| UK night bus (before flip) | "a double-deck bus at night, entrance door at the front left, blank black destination display" |
| US signals | "traffic lights hanging over the far side of the intersection" |
| UK signal at the stop line | "a traffic light on a short pole at the kerb, just past the stop line, level with the car's front" |
| Home ring hand (before any flip) | "a plain gold wedding ring on the ring finger of her left hand" (C1 Recipe 8 decides which hand to prompt for a flipped shot) |
| P1999 village | "a small central Anatolian village in 1999: flat-roofed stone houses, a dusty lane, an old minibus" |
| TIMELESS lamp | "a small clay oil lamp in a rock niche, a hand-pinched wick, no metal, no labels" |
| P1999 negatives | "no smartphones, no LED lights, no orange rescue uniforms, no text" |

---

## 11. Open questions for the user

**The Catch**
1. Where and when does the story happen: option A, B or C (§6.5)?
2. The guard's pistol: proof of a criminal operation, or a sign the world is not the UK?
3. Should the audience see Iona's car the right way round before the turn (R19), at the cost of one invented shot?
4. Analogue or digital dashboard clock?
5. Present day (blueprint K27) or near future (§6.1)? Only the visor readouts argue for the future.

**The Long Places**
6. Film language: English with Turkish forms of address (kızım, Hanım, Bey), or Turkish with subtitles?
7. Does the village have a disused church, and did the 1924 survey come before its Christians left that year (§7.2)?
8. Should the 1999 scenes differ in light (incandescent against LED) and texture?
9. May a portrait of a real historical figure hang in the co-op room?

---

## Sources

All web sources checked 2026-09-27; re-checked 2026-09-28 where marked.

- **S1** GOV.UK, The Highway Code, rules 159–203 (rule 160): https://www.gov.uk/guidance/the-highway-code/using-the-road-159-to-203
- **S2** GOV.UK, The Highway Code, "Light signals controlling traffic": https://www.gov.uk/guidance/the-highway-code/light-signals-controlling-traffic
- **S3** Department for Transport, *Traffic Signs Manual* ch. 6 (2019), §3.1.2–3.1.3: https://assets.publishing.service.gov.uk/media/5df0e29fed915d15f42c4820/dft-traffic-signs-manual-chapter-6.pdf
- **S4** Road Vehicles Lighting Regulations 1989, reg. 16: https://www.legislation.gov.uk/uksi/1989/1796/regulation/16
- **S5** Health and Safety (Safety Signs and Signals) Regulations 1996, Sch. 1: https://www.legislation.gov.uk/uksi/1996/341/schedule/1
- **S6** Firearms Act 1968, s. 5: https://www.legislation.gov.uk/ukpga/1968/27/section/5
- **S7** GOV.UK, "Rules for number plates"; "Displaying number plates": https://www.gov.uk/displaying-number-plates/rules-number-plates ; https://www.gov.uk/displaying-number-plates
- **S8** Transport for London, night bus maps (N routes): https://tfl.gov.uk/cdn/static/cms/documents/bus-route-maps/kings-cross-night-a4-0622.pdf (refused automated access on 2026-09-28); route page: https://tfl.gov.uk/bus/route/n29/ ; N29's route history from search summaries only
- **S9** Greater London Authority, Mayor's answer "Bus blinds" (refused automated access; search summary only): https://www.london.gov.uk/who-we-are/what-london-assembly-does/questions-mayor/find-an-answer/bus-blinds
- **S10** California Vehicle Code §21650: https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=VEH&sectionNum=21650
- **S11** California Vehicle Code §25252 and §25258 (both read 2026-09-28): https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=VEH&sectionNum=25252 ; https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=VEH&sectionNum=25258
- **S12** OSHA, 29 CFR 1910.37(b)(7): https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.37
- **S13** FHWA, *MUTCD* 11th ed. (Dec 2023), Part 4, §4D.08 "Longitudinal Positioning of Signal Faces": https://mutcd.fhwa.dot.gov/pdfs/11th_Edition/part4.pdf
- **S14** SFMTA, "Muni Owl" service page; "Bikes on Muni" (both read 2026-09-28): https://www.sfmta.com/getting-around/muni/routes-stops/muni-owl-service-late-night-transportation ; https://www.sfmta.com/getting-around/bike/bikes-muni
- **S15** Basu, Babu, Pruthi, "Inspecting the Geographical Representativeness of Images from Text-to-Image Models", ICCV 2023, pp. 5113–5124: https://arxiv.org/abs/2305.11080 ; https://openaccess.thecvf.com/content/ICCV2023/html/Basu_Inspecting_the_Geographical_Representativeness_of_Images_from_Text-to-Image_Models_ICCV_2023_paper.html
- **S16** Karayolları Trafik Kanunu (Law 2918), art. 46: https://mevzuat.gov.tr/mevzuatmetin/1.5.2918.pdf
- **S17** Jandarma Teşkilat, Görev ve Yetkileri Kanunu (Law 2803), art. 10: https://www.icisleri.gov.tr/kurumlar/icisleri.gov.tr/IcSite/illeridaresi/Secim_Mevzuati/46-2803-Sayili-Jandarma-Teskilat-Gorev-ve-Yetkileri-Kanunu.pdf
- **S18** Law 5902 (AFAD), Resmî Gazete 17 June 2009: https://resmigazete.gov.tr/eskiler/2009/06/20090617-1.htm
- **S19** Central Bank of the Republic of Türkiye, banknote emission groups: https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Banknotlar/Cumhuriyet+Donemi+Banknotlari/Emisyon+Gruplari/ ; E7 note pages for 5,000,000 (emisyon34), 10,000,000 (emisyon35) and 20,000,000 (emisyon36) under .../Emisyon+Gruplari/7+Emisyon+Grubu/
- **S20** Law 5083 on the currency, Resmî Gazete 31 January 2004, no. 25363 (text read 2026-09-28): https://www.mevzuat.gov.tr/MevzuatMetin/1.5.5083.pdf
- **S21** Yüksek Seçim Kurulu, 18 April 1999 local elections: https://www.ysk.gov.tr/tr/18-nisan-1999-mahalli-idareler-genel-secimi/2805 ; 31 March 2024 calendar: https://www.ysk.gov.tr/doc/dosyalar/docs/31Mart2024/SEC%C4%B0M_TAKVIMI.pdf ; Presidency of Communications, voting in villages on 31 March 2024: https://www.iletisim.gov.tr/turkce/haberler/detay/31-mart-mahalli-idareler-genel-secimlerine-iliskin-bilgilendirme (the YSK 1999 page renders no text to automated readers)
- **S22** Turkcell, "History": https://www.turkcell.com.tr/en-en/about-us/company-overview/history/detail
- **S23** USGS event page (M 7.6): https://earthquake.usgs.gov/earthquakes/eventpage/usp0009d4z ; USGS paper (M 7.4): https://www.usgs.gov/publications/surface-rupture-and-slip-distribution-17-august-1999-izmit-earthquake-m-74-north
- **S24** MTA, "Erciyes Dağı" (gives 3,864 m and 3,916 m): https://www.mta.gov.tr/turkvolc/en/erciyes ; Wikipedia, "Mount Erciyes" (3,864, 3,917 or 3,918 m): https://en.wikipedia.org/wiki/Mount_Erciyes
- **S25** Law 2863, art. 35 (search summary: the Ministry alone holds the right to excavate; excavation permits by Presidential decree); the directive names a "Bakanlık Yetkili Uzmanı/Temsilcisi" (the Ministry's authorised expert or representative) on site (read 2026-09-28): https://www.mevzuat.gov.tr/mevzuatmetin/1.5.2863.pdf ; Ministry of Culture and Tourism excavation directive: https://teftis.ktb.gov.tr/TR-251757/kultur-ve-tabiat-varliklariyla-ilgili-yapilacak-yuzey-arastirmasi-sondaj-ve-kazi-calismalarinin-yurutulmesi-hakkinda-yonerge.html
- **S26** Nevşehir Valiliği, "Derinkuyu Yeraltı Şehri": https://nevsehir.gov.tr/derinkuyu-yeralti-sehri
- **S27** Google Maps Help, "Use Street View in Google Maps": https://support.google.com/maps/answer/3093484
- **S28** Nevşehir Hacı Bektaş Veli University, Art History, "Kapadokya Bezirhaneleri" (read 2026-09-28): https://sanattarihi.nevsehir.edu.tr/tr/27258
- **S29** Türkiye Ministry of Foreign Affairs, Lausanne Convention VI on the exchange of populations: https://www.mfa.gov.tr/lausanne-peace-treaty-vi_-convention-concerning-the-exchange-of-greek-and-turkish-populations-signed-at-lausanne_.en.mfa
- **S30** Jandarma Genel Komutanlığı Kıyafet Yönetmeliği, RG 31.03.2020/31085: https://www.lexpera.com.tr/mevzuat/yonetmelikler/jandarma-genel-komutanligi-kiyafet-yonetmeligi
- **S31** ISO 7010 E001 registry entry (not read): https://www.iso.org/obp/ui#iso:grs:7010:E001 ; Wikipedia, "ISO 7010" (E001 "Emergency exit (left hand)", E002 "Emergency exit (right hand)"): https://en.wikipedia.org/wiki/ISO_7010 ; sign makers list the same codes (e.g. Brady A270/E001)
- **S32** Turkish province plate codes, two agreeing lists: https://www.continental-tires.com/tr/tr/tire-knowledge/license-plate-codes/ ; https://www.arabam.com/blog/genel/araclarin-il-plaka-kodlari/
- **S33** Web search for "Kırk Oda" with Kayseri and Nevşehir underground terms: no site of that name found (negative result; repeated 2026-09-28 with the same result).
- **S34** Cappadocia's Orthodox Christians sent to Greece in 1924: Wikipedia, "Cappadocian Greeks": https://en.wikipedia.org/wiki/Cappadocian_Greeks ; Duke University Libraries blog, "Cappadocia and the 1923 Population Exchange" (21 March 2025): https://blogs.library.duke.edu/blog/2025/03/21/cappadocia-and-the-1923-population-exchange-mubadele-%E1%BC%80%CE%BD%CF%84%CE%B1%CE%BB%CE%BB%CE%B1%CE%B3%CE%AE
- **S35** Wedding-ring hand: Wikipedia, "Wedding ring" (Germany and Austria: engagement ring left, wedding ring right; right hand also in Bulgaria, Poland, Russia): https://en.wikipedia.org/wiki/Wedding_ring ; UK/US left hand and Turkish engagement-right, marriage-left practice from search summaries of secondary sources only [U]
- **S36** GOV.UK, The Highway Code, rule 124 speed limits table (mph): https://www.gov.uk/guidance/the-highway-code/general-rules-techniques-and-advice-for-all-drivers-and-riders-103-to-158

**Library files used:** A3 (§4.4, Ex4, Ex5), B2 (R19, §5.4, Example 3), B3 (§8.5), B4 (§4.3–4.5), C1 (R7, Recipe 8), C2 (§7, R5, R6, W2), C3 (§7B), D3 (R6), D4 (R17–R19, §9.4), design blueprint (WORLD, CHOICE, IDs).

**Test sources:** *The Catch*: `/root/.claude/uploads/fbbb0203-69e3-5f8e-b675-32d722ec580d/1edae70d-35_The_Catch_-_workshop_revision_of_Final4.txt`; *The Long Places*: `/root/.claude/uploads/fbbb0203-69e3-5f8e-b675-32d722ec580d/5dcd8176-19_The_Long_Places_-_revised_by_Claude_final.md`.
