# Digest D17: World and locale research (28 Sept 2026)

Source: `research/D17_world_locale_research.md` (fact-checked 28 Sept 2026; 16 corrections marked there). Brackets: R*n* = decision rule (§3); §1.*n* = principle. **[V]** primary page or two agreeing sources read 27–28 Sept 2026; **[U]** unverified; **[J]** judgment. Re-check TfL, SFMTA and Street View pages after 28 Oct 2026.

## 1. Scope

1. Decides once, in the WORLD record, where and when a story happens: a named country, an invented place borrowing an **anchor country's** conventions, or a designed **non-place**, plus period layers, one locale sheet per place and one negative list per layer.
2. Gives sources, checks and paste-in LLM recipes for every convention the camera or ear meets (driving side, signals, emergency lights, signs, plates, buses, institutions, uniforms, weapons, money, units, customs, landmarks), so models do not fill gaps with American defaults.
3. Worked on *The Catch* SC08–SC09 (UK, US and non-place options, with effects on B3 staging and C1/C2 mirror plates) and on *The Long Places* (central Anatolia: 1999, 2025–26, a 1924 layer and TIMELESS letter scenes).

## 2. Rules

**Principles** [§1]
1. [§1.1; R1] If the source names no country or year, then record `unstated`, list the cues and ask once at checkpoint B, because silent guessing already split the library (C3 British voices, B3 right-hand drive, A3 "period unstated").
2. [§1.2] If you choose a country, then take its whole bundle (driving side, plates, signs, lights, uniforms, units, money, spelling, sirens), because mixed bundles read as error.
3. [§1.3, §1.6; R13] If a prompt shows a street, vehicle, sign, uniform, emergency service or shopfront, then name each convention in plain words and add the layer's `locale_negatives`, because DALL-E 2 and Stable Diffusion images "most reflect the surroundings of the United States followed by India", and naming the country raised scores only 1.44 and 0.75 points out of 5 [V].
4. [§1.4; R7] If a convention is seen for more than about two seconds in total or in more than one shot, is read, or is heard clearly, then research it from a primary source into `facts`; otherwise a labelled [J] is enough, because research follows screen time.
5. [§1.8; R8] If the LLM answers from memory, then mark it [U] until a source confirms it, because LLMs mix countries fluently.
6. [§1.9; R12] If an institution is real and identifiable, then invent its name, crest and livery but keep its grammar (colours, shapes, layout), because audiences read grammar and D4 R19 bars real insignia.

**Deciding the world** [§3]
7. [R2] If one cue conflicts with the rest, then list it as a question with both readings, because it may be the story's point or a slip.
8. [R3] If a real region holds an invented site, then set `named:<country>`, `region` and a `real_basis` drawn from several analogues, because copying one site misrepresents it (D4).
9. [R4] If the user wants no real country, then choose `anchor: named:<country>` or `anchor: own`, because a half-designed place drifts to the model's default.
10. [R5] If the story spans several times, then define `period_layers` and give every scene one, because objects differ by layer.
11. [R6] If a scene should feel outside time, then set `TIMELESS` and allow only objects that existed across the whole span (no print, plastic or electric light unless named), because one modern object dates it.

**Researching** [§3]
12. [R9] If a rule, currency, banknote, institution or uniform has a start date, then check that exact item against every layer, not just its series, because Turkey's 10,000,000-lira note was issued on 5 November 1999, after the story's September [V].
13. [R10] If a date carries a weekday, age or interval, then compute it, and check any real event it names, because locals notice a Saturday that was a Tuesday.
14. [R11] If a landmark is visible, then record its bearing and keep it on that side in every shot, because a mountain on the wrong side reverses the geography.
15. [R14] If readable text uses special letters (Turkish ı, İ, ş, ğ), then make it an insert graphic (C2 R6) and check each letter, because models drop rare letters.
16. [R15] If a sound belongs to the locale (siren, church bell, call to prayer), then record it in WORLD for D9, because sound places a film as fast as picture.

**Mirror stories** [§3]
17. [R16] If the story mirrors the world, then generate every mirror plate in home handedness, check it (`handed_check: yes`), and only then flip, because a plate that drifted to the other driving side flips into a normal street.
18. [R17] If a mirror effect depends on knowing the home convention, then add a universal cue (reversed text, a wrong reach), because driving side looks wrong only to viewers who share it.
19. [R18] If a number or word must visibly read backwards, then use characters that change when mirrored (N, R, S, 2–7, 9), not A, H, I, M, O, T, U, V, W, X, Y, 0, 1, 8, because symmetric characters look unchanged.
20. [R19] If no street appears before the mirror turn, then consider one added establishing shot in home handedness, logged `origin: invented`, because otherwise each viewer's own country is the only reference.
21. [R20] If the locale changes staging, then redraw the floor plan from WORLD before writing shots, because every frame-left/right flips with the driving side.
22. [R21] If the story uses a sided body custom as a cue (the wedding-ring hand), then record it in `customs` and check it against the anchor, because the ring goes on the right hand at the wedding in Germany, Austria, Bulgaria, Poland and Russia [V] but the left in the UK and US [U].
23. [R22] If a mirrored sign has an official twin (ISO 7010 E001 "Emergency exit (left hand)", E002 "(right hand)" [V]), then carry the wrongness with reversed text or a reaction, because a reversed running man is still a valid sign.

## 3. Breakdown fields

The blueprint's WORLD record already has `place, period, drives_on, language, accents, signage, emergency_lights, institutions, money, evidence, origin`; D17 fixes their values and adds the rest (new) [§2].

| Level | field_name | Meaning | Allowed values / example |
|---|---|---|---|
| film (WORLD) | `place` | Where the story happens | `named:<country>` \| `invented` \| `unstated` |
| film | `anchor` (new) | Country an invented place borrows from | `named:<country>` \| `own` \| `none` |
| film | `region` (new) | Part of the country, if it shows | text \| `unstated` |
| film | `period` | Main story time | year/range and season \| `present` \| `near_future` \| `unstated` |
| film | `period_layers` (new) | Each stretch of time with its own objects | repeat `P<id> \| span \| scenes \| origin` |
| film | `drives_on` | Home driving side | `left` \| `right` \| `none` |
| film | `language`, `accents` | Language in world and film; accent set | text; `undecided` blocks voice locking (D3 R6) |
| film | `writing` (new) | Alphabet, letters, spelling, date/time format | "Latin alphabet with ı İ ş ğ ç ö ü; dd.mm.yyyy; 24-hour" |
| film | `units` (new) | Units on signs and dashboards | `metric` \| `imperial` \| `mixed:<how>` (UK: mph on roads) |
| film | `signage`, `traffic_signals` (new) | Sign style; signal sequence and where heads stand | text |
| film | `emergency_lights` | Colours and siren family per service | text ("blue only") |
| film | `vehicles`, `uniforms` (new) | Vehicles and plates; service dress per layer | text |
| film | `institutions` | Who polices, treats, governs, inspects | repeat `role \| shown_as \| real_or_invented \| grammar` |
| film | `money`, `tech` (new) | Currency and devices per layer | text |
| film | `customs` (new) | Body habits used as cues | repeat `item \| convention \| lines \| fact` ("wedding ring \| left hand \| l.436–438, l.1779–1783 \| S35") |
| film | `audience_region` (new) | Whose conventions decide "wrong" | text \| `mixed` |
| film | `facts` (new) | Each researched convention | repeat `field \| value \| source: URL \| checked: date \| label: V/U/J` |
| place (LOC) | `real_basis` (new) | Real places the set is modelled on | `none` \| text |
| place | `locale_sheet` (new) | Conventions visible here, per layer | repeat `P<id> \| item \| convention \| fact` |
| scene | `period_layer` (new) | The scene's layer | `P<id>` \| `TIMELESS` |
| scene | `locale_check` (new) | Every locale item has a sheet entry | `pending` \| `done` \| `n/a` |
| thing (PR, TX) | `period_check` (new) | The object existed in its layer | `ok` \| `anachronism` \| `unchecked` |
| shot | `locale_negatives` (new) | Exclusions compiled into the prompt | list |
| generation job | `handed_check` (new) | Mirror plate checked before any flip | `yes` \| `no` \| `n/a` |

D3's `world_accent_rule` points at `WORLD.accents`; `WR-` IDs stay for story-world rules such as `WR-MIRROR` [§2, J].

## 4. Procedures

Paste each prompt into your LLM; replace the bracketed parts [§4].

**Recipe 1. Harvest locale cues (10 minutes)**
1. Give the LLM the numbered source.
2. Paste: *"List every word or detail that points to a country, region, period or social world: spelling, vocabulary (torch/flashlight, lift/elevator), institutions, uniforms, vehicles, signs, units, money, technology, food, weather, landmarks, and body customs (which hand wears a ring, greetings). For each: line number, exact quote, what it points to, strong or weak. Then list anything that conflicts with the majority. Do not decide the country."*
3. Check three quotes against the source yourself; if any is not word for word, ask for a redo.
4. The list goes into WORLD `evidence`, each item `origin: inferred`.

**Recipe 2. Choose the world (15 minutes)**
1. Paste: *"From the cue list, propose a default world and one alternative: place (named country, invented with an anchor country, or invented with its own conventions), period, driving side, language, accents. For each, list what it forces us to change in the source, the extra reference images it costs, and what it does to any story-world rule such as a mirror. Recommend one, with a reason."*
2. The LLM writes one CHOICE record (`checkpoint: b`, `asked: yes`, `affects` naming voices, places, rules and staged scenes).
3. The user's answer at checkpoint B sets `place`, `anchor`, `period`, `drives_on`, `language`.

**Recipe 3. Research each convention (30–90 minutes per locale)**
1. Paste: *"For the world [answer], list the conventions the camera or ear will meet in these scenes: [scene IDs with one-line summaries]. For each: what it looks or sounds like, which scenes, how long it is seen, and the best primary source (law, official manual, the institution's own site). Order by screen time. Mark anything stated from memory [U]."*
2. Have the LLM search the web for the top items, using §5 of the file. Each checked item becomes a `facts` line.
3. Collect two real photographs per item. Present: Google Maps Street View, "See more dates" (not every place has history) [V]. Past: Wikimedia Commons, newspaper archives, museums; never films. Name each file with place and date.
4. Stop when every item seen for more than about two seconds, or read, has a source or a flagged [U]/[J].

**Recipe 4. Locale sheets and negative lists (20 minutes)**
Paste: *"For each place and each period layer, write a locale sheet: every convention visible there, each pointing to a `facts` line. Then write a negative list per layer: things a model is likely to add wrongly (other countries' police lights, school buses, modern phones in the past, wrong script on signs)."* Copy each negative list into the matching shots' `locale_negatives`.

**Recipe 5. Anachronism sweep (20 minutes per layer)**
Paste: *"For layer [P1999], go through every scene in it and list every object, vehicle, garment, light source, device, sign and sound. For each, say whether it existed and was ordinary in [place] in [year]; give a source for anything doubtful. Flag anything common in recent photos of this place that did not exist then."* Set each `period_check`; any `anachronism` goes back to the scene as a replacement or a question.

**Recipe 6. Design a non-place (45 minutes)**
1. Decide `anchor`: borrow one country (fast; reads as that country with names filed off) or `own` (slow; reads as nowhere).
2. For `own`, paste: *"Design a locale bible for an invented city: driving side, plates, street-name and road signs, traffic signals, police and ambulance colours and sirens, buses, taxis, safety signs, money, spelling, units, one typeface family for public signs, and every body custom the story uses as a cue (for The Catch: wedding rings on the left hand). Keep it simple, consistent, and unlike any single country's full set. Avoid combinations that already mean something (amber beacons read as tow trucks in many countries)."*
3. Make one reference image per convention (C2); no model knows the design.
4. Run D4's name check on every invented name.

**Recipe 7. Check frames for locale (2 minutes per frame)**
Ask an LLM that can see images: *"Check this frame against the locale sheet [paste]: driving side, steering-wheel side, plate colours, sign shapes and colours, light colours, uniforms, vehicle types, alphabet and spelling, landmarks and their side, which hand wears a ring. List every mismatch."* Fix by inpainting or regeneration (C2). For a mirror plate, run it **before** flipping.

**Key verified facts** [§5, all V]: UK keeps left (Highway Code r.160); California and Turkey keep right (VC 21650; Law 2918 art. 46). UK signals RED, RED AND AMBER, GREEN, AMBER, primary head near side 1.5–2.5 m past the stop line; US primary faces 40–180 ft beyond it (MUTCD §4D.08). UK blue beacons only on emergency vehicles; California a steady red lamp to the front, blue for peace officers. UK exit signs white on green; US signs say "Exit" in letters at least six inches high. UK plates white front, yellow rear; Turkey 06 Ankara, 38 Kayseri, 50 Nevşehir. UK prohibits firearms with barrels under 30 cm, which covers ordinary pistols (Firearms Act s.5(1)(aba)). Turkey: Jandarma outside municipal limits; AFAD from 2009; 5, 10, 20 million-lira notes issued 1997, Nov 1999, Nov 2001; six zeros removed 2005; GSM from 1994.

**Templates** [§6.5, §7.5], reproduced exactly:

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

```
### LOC LOC-COOP-UPSTAIRS The room above the co-op
- real_basis: a village co-operative building in central Anatolia; no single real building
- locale_sheet: P2025 | item: forty consent forms | convention: muhtar's round office stamp | fact: S21, J
- locale_sheet: P2025 | item: tea in small glasses on saucers | convention: village hospitality | fact: J
- locale_sheet: P2025 | item: men and women present | convention: the scene needs a couple who contradict each other ("One man remembered a scarf; his wife remembered no scarf.") | fact: story
- locale_sheet: P2025 | item: window over the lane | convention: Nilay looks back up at it from the stairs | fact: invented (A3 Ex5)
- locale_negatives: no suits and ties on villagers, no microphones, no projector, no English signs
```

## 5. Checklists

**Before checkpoint B** [§8]
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
- [ ] Recipe 7 run: driving side, wheel side, plates, lights, signs, uniforms, alphabet, ring hand.
- [ ] Mirror plates: `handed_check: yes` before the flip; reversed characters chosen by R18.

**Failure modes** [§9]: American defaults; mixed bundles; a plate flipped from the wrong handedness; a reversal nobody can see; present objects in the past; garbled Turkish letters; real logos or registrations; Erciyes swapping sides; staging on the wrong side; a ring hand reversed by the anchor.

## 6. Saying it to AI models

Name conventions, not only countries; city and brand names pull in landmarks and logos (D4). Put locale early in the prompt and attach reference photos for anything that must match [§10, J].

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

Readable text never comes from the model: blank it and add an insert graphic (C2 R6).

## 7. The Catch

**Decisions made** [§6]
- **Cues** (quotes checked verbatim): "lift" (l.59), "torch" (l.69), "practised", "Stencilled" (l.149, l.325), the green running-man sign (l.331), "gearstick" (l.341), "night bus" (l.370), "metres" (l.1587), "grey" and "DR SAYE" with no full stop (l.214, l.399). One conflict: "A GUARD comes out of a side room, pistol half drawn" (l.183). Police-light colour is never given.
- **Default: option A**, an invented city with a UK anchor: drives on the left, British accents (D3 locks after B), blue emergency lights, near-side signal heads, a double-deck night bus with an N number, invented institutions (D4 R19). Option B (unnamed US city) rewrites the exit-sign line and flips every side in SC09; option C (non-place) costs about a dozen extra reference images.
- **Period**: `near_future`, `origin: inferred`, read as D5's `near_future_subtle` (today's world, story devices advanced).
- **Ring (R21)**: `customs: wedding ring | left hand`, from "Saye's wedding ring. On her right hand." / "Iona looks down at her own ring, on her own left hand." (l.436–438) and "His wedding ring. On his right hand." (l.1779). It reads for every viewer because the wrong hand is shown beside the right one; all three options keep the left.
- **Exit sign (R22)**: "The little running man is running the other way" (l.331) depends on Iona knowing this door; keep the reversed stencil letters in the same scene (C2 W2).
- **SC09 staging, option A** (matches B3 §8.5): her own car has the wheel on the right, so she opens the right-hand door on "The passenger seat."; on screen the car looks left-hand drive on the right. Frontal two-shot: Iona frame-right, Eli frame-left; "Hits the door." is her left hand toward the frame-right edge. "Everything in her wants to be on the other side of the road." pulls her screen-left, into the lane where "A night bus comes at them". "A red light.": the UK primary head stands 1.5–2.5 m past the stop line on the kerb [V], which in the mirrored world is Eli's side (frame-left), so the red reaches him first, as B2 plans. Option B swaps every side, and its red comes from ahead and above, a weaker wash [J].
- **Every option**: the central rear-view mirror keeps B3's key shot; the car needs `vehicles: gear lever on centre console, cup holder beside it` [J]; an analogue clock suits "which she has to work out like a child" [J].
- **Mirror plates (C1 Recipe 8, C2 R5)**: generate in home handedness (traffic left, wheels right, blank plates, bus door front left, near-side signals), ask "Is traffic keeping left? Is every wheel on the right?", set `handed_check: yes`, then flip. The bus number is an insert graphic made before the flip; `N29` flipped shows a reversed 9, 2 and an "И".
- **The Long Places** (country fixed by real places and "in Turkish", l.419): layers P2025 (June 2025 – Oct 2026; ch. XIV is 4 Sept 2026), P1999 (late Aug–Sept 1999), P1924, TIMELESS. Dates and ages check out (4 Sept 1999 a Saturday; "He would be forty" = 13 + 27). Kırk Oda is invented, modelled on complexes such as Derinkuyu; Erciyes appears only in east-facing exteriors; lamps burn linseed oil (*bezir*) [V]; no AFAD and no 10- or 20-million-lira notes in 1999.

**Flagged for the user**
1. Where and when: option A, B or C, and present day or near future (one CHOICE).
2. The guard's pistol is prohibited under UK law [V]: proof of a criminal operation (fits "The men who kept him are not.") or a sign the world is not the UK? Never swap it for a baton silently.
3. One invented shot of Iona's car in home handedness before the turn (R19, about one generation)?
4. Analogue or digital dashboard clock?
5. `N29` is a real London night route [U]: keep it, or pick a number with no London association?
6. *The Long Places*: film language; whether a Christian quarter existed and the 1924 survey came before it left; incandescent against LED between layers; a portrait of the republic's founder in the co-op (D4).

## 8. Conflicts and open questions

1. **Blueprint K27 vs D17 on period**: "present day" against `near_future`; D5's digest offers `near_future_subtle`. Proposal: `period: near_future` with `period_distance: near_future_subtle`, confirmed in the place-and-time CHOICE.
2. **Blueprint K27 "an unnamed British city" vs option A "invented, anchor named:UK"**: the blueprint has no `anchor` field. `named:UK` keeps real UK law, which makes the pistol conflict sharp. Add `anchor` to the blueprint, or record option A as `named:UK`, `region: unstated`.
3. **D9 vs D17 on *The Long Places***: D9 says only "the characters' names suggest Turkey"; D17 finds Turkey fixed by Kayseri, Ankara, Derinkuyu, Cappadocia and "in Turkish" (l.419), though the word "Turkey" never appears. The lullaby's own origin ("the one from the dark") stays D9's call.
4. **C3 sound keys** give everyone "a British accent"; they stay proposals until checkpoint B (the D3 digest agrees).
5. **Ring sides**: blueprint K03 (rings as own left) and C1 Recipe 8 (turned characters prompted right-handed before a flip) both assume `customs: left hand`; a right-hand-ring anchor breaks both.
6. **Corrected in D17 on 28 Sept**: the present layer (was "June to September 2025"), Derinkuyu's depth, Erciyes' height as a single MTA figure, the Jandarma "2010s redesign", and the 1924 church bell (was "tight"). Update anything copied from the first draft.
7. **Still unverified**: headmen elected on 18 April 1999; London bus blinds white on black; UK/US left-hand rings; 1999 Jandarma dress and vehicles; rural GSM in 1999; Erciyes' height (3,864 to 3,918 m by source).
8. **Newer models untested**: the US-default study covers DALL-E 2 and Stable Diffusion only.

## 9. Section map

| Need | File section |
|---|---|
| Purpose, where it runs, what it leaves to other files | header, §0 |
| Plain definitions of terms | §0.1 |
| Principles | §1 |
| Fields added to WORLD, LOC, scene, thing, shot, job | §2 |
| Decision rules R1–R22 | §3 |
| Recipes 1–7 (cues, choice, research, sheets, anachronisms, non-place, frame check) | §4 |
| Sources and checks per field | §5 |
| The Catch: cues, three options, SC09 staging, mirror plates, CHOICE | §6.1–6.5 |
| The Long Places: WORLD record, checks, period sheet, negatives, locale sheet | §7.1–7.5 |
| Checklists | §8 |
| Failure modes | §9 |
| Model phrases | §10 |
| Open questions for the user | §11 |
| Sources S1–S36 | end |
