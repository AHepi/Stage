# Digest D13: Runtime, cost and schedule estimator (27 Sept 2026)

Source: `research/D13_runtime_budget_schedule.md` (fact-checked 27 Sept 2026). Brackets: R*n* = D13 decision rule; E*n* = validator formula (§11.1); § = section. Evidence: **[V]** read at the maker's page on 27 Sept 2026, **[U]** unverified, **[J]** judgment or arithmetic on the test sources. Prices go stale monthly: a price table older than 30 days blocks all money output (R7, E11).

## 1. Scope

1. Turns a breakdown (or, before shots exist, word counts) into runtime, shot counts, generated seconds, money for every tool and subscription, and the user's own hours, in four versions: v0 words (checkpoint M), v1 shot list (checkpoint C), v2 animatic (runtime lock), v3 actual spending (after each batch at checkpoint E).
2. A script (`estimate.py`, run in the pipeline as `stage.py estimate`) does every sum and writes only `derived` `estimate` blocks per scene, sequence and film; the LLM proposes classes and durations only (P1, R4).
3. Spreads hours over a week-by-week calendar, re-forecasts from measured costs, says what to cut, and prices *The Catch* (3 tiers × full and 20 minutes) and *The Long Places* (D2 Plans A, B, C).

**Terms** [§1]: *used length* = seconds on screen (`duration_s`); *clip length* = seconds a model makes and bills per take (`clip_s`); *handles* = 0.75 s spare each side; *draft take* = $0.05/s test; *final take* = delivery take at the tier price (`budget` ≈ $0.07/s, `mid` ≈ $0.17, `premium` ≈ $0.45); *generation factor* = generated seconds ÷ runtime; *ASL* = screen time ÷ shots; *novice factor* = hours × 1.3 central, × 2 high; *contingency* = 20% (10% once actuals cover half the shots); *plate* = background clip for compositing; *picture lock* = no shot changes length or order after it.

## 2. Rules

**Versions and checks**
1. [R1] If no shots exist yet, then run v0 from word counts and show low, central and high beside D2's format options at checkpoint M, because format and runtime fix every later budget and a single number hides a spread of about 20%.
2. [R2] If a sequence's shot list passes checkpoint C, then replace v0 for its scenes with v1 from the shot records, because counts by cost class beat default shares.
3. [R3] If v1 runtime differs from pages ÷ 1.1 by more than 25%, or the film ASL falls outside 3–7 s (or the band moved by R23), then look for missing scenes, double-counted dialogue, durations under A4's minimums, or wrong rhythm classes before approving, because on *The Catch* v0 and the page rule agree within 7%.
4. [R4] If an LLM states a total, then ignore it and run the validator, because only script arithmetic counts (C5 R23).
5. [R22] If the screenplay is under 90 pages, then show the page check as a range (pages ÷ 1.1 to pages ÷ 0.8) and mark it "extrapolated" under 60 pages, because Follows' 60–89-page scripts ran 0.8 pages a minute and no data exist below 60 pages [V].
6. [R25] If the validator is new or changed, then accept it only when Recipe 0's SC06 test matches, because a wrong formula silently corrupts every estimate.

**Shots and takes**
7. [R5] If a shot's used length is below the model's shortest clip, then bill the shortest clip; if consecutive shots share one camera setup and one continuous action, then consider one clip cut into those shots in the edit (still one shot per request, C5 R15), because a 1.4 s shot otherwise pays for 5 s on every take.
8. [R6] If a framing repeats (refrain, "repeat the framing" across a turn, recap), then mark it `reuse` with `reuse_of`, because reuse costs no takes (D2 R18); if the copy is reversed or flipped, then check it plays; if time of day, light or character state differs, then reuse the saved setup, not the clip, and cost a new take.
9. [R8] If `shot_need` is `zero_gravity`, `exact_camera`, `timed_beats` or `performance`, or the shot shows a creature, then cost it `hard`, because these fail most (83–94% of clips from five late-2025 models had visible physics glitches, C1 R8).
10. [R20] If a shot has several `shot_need` values, then take the most expensive class (`hard` > `dialogue` > `easy`) and add one plate each for `text` and `screen`, because the shot must survive its hardest part and text and screens are composited.
11. [R21] If a shot is generated slowed and played back at real time (`gen_slowdown` > 1), then bill `clip_s` on screen length × `gen_slowdown` plus handles, because the model makes every slowed second.
12. [R23] If a scene's D10 tone has `asl_factor` ≠ 1, then multiply the class ASL by it and move the E4 band likewise, because slow-cinema or kinetic films are meant to fall outside the drama band.

**Money**
13. [R7] If the price table is over 30 days old, then print no money until Recipe 1 has run, because prices and routes change monthly.
14. [R9] If the user has not chosen a tier, then show all three and the mix "drafts at $0.05, finals at mid, dialogue close-ups at premium", because the choice is theirs.
15. [R10] If v1 exceeds the budget, then cut in this order, re-running after each: (1) near-stills → `still_move`; (2) non-dialogue finals → budget tier; (3) 4K → 1080p; (4) design out plates; (5) D2 R10 runtime cuts; (6) C1's animatic film, because each step costs the story more than the last.
16. [R11] If spending passes 50% of the video budget before 50% of shots are kept, then move remaining non-dialogue shots to the budget tier and re-forecast (C1 §10).
17. [R12] If one shot passes 3× its estimate, 10 final takes, or 4 failed takes in a row on one route, then stop and change method (start/end frames, previs, compositing, still with push-in), because more takes on a failing route rarely rescue it (C3 §17A rule 2); the `hard` default (4 drafts + 7 finals) fits only with drafts on a cheap route.
18. [R13] If a monthly plan is used, then book only the months the schedule needs and cancel after the last job that spends its credits (ElevenLabs credits are lost on cancelling); if credits expire monthly (Topaz, Runway Standard/Pro, Suno), then batch that work into one month, because an unused month still bills.
19. [R14] If upscaling, then only after picture lock and only kept takes: to 1080p whole kept takes (D8-R20, so the edit relinks); to 4K only used seconds plus handles and only if 4K delivery is required, because 4K costs 4× ($0.08 vs $0.02/s).
20. [R19] If the user voices the lines, then voice money is $0 plus 1–2 min a line; if synthetic, then the smallest commercial plan covering five tries; if a tool's terms exclude film (ElevenLabs music on every self-serve plan), then never budget it; if a tool licenses only downloaded output (Suno), then budget downloads, because free plans and excluded uses make the film unshowable.
21. [R24] If D9's `music_policy` is `none`, then music money and cue hours are 0; if `sparse` or `end_credits_only`, then cues = `cue_budget`; only `scored` uses runtime ÷ 120 s, because policy, not runtime, decides how much music exists.

**Hours and calendar**
22. [R15] If a date matters, then schedule on the high case until sequence 1's actuals exist, because the only first-hand published account ran several times slower per second than the central case.
23. [R16] If sequence 1 is finished, then replace the novice factor and default takes with measured minutes per shot by class, takes per kept shot and dollars per kept shot.
24. [R17] If central hours ÷ `hours_per_week` exceeds 26 weeks (short) or 52 (anything else), then offer a shorter runtime or a pilot before checkpoint M [J], because long solo projects stall.
25. [R18] If the format is a series, then make episode 1 to picture lock before generating episode 2, because its actuals correct the rest.

## 3. Breakdown fields

Enums lowercase `snake_case`; empty = `"none"`. All `derived` (script-written) unless marked authored or read.

| Level | field_name | Meaning | Allowed values / example |
|---|---|---|---|
| film | `tier` (authored) | Price level of final takes | `budget` \| `mid` \| `premium` \| `mixed` |
| film | `hours_per_week` (authored) | User's available hours | `20` |
| film | `deadline` (authored) | Date to meet | `2027-03-01` \| `"none"` |
| film | `voice_source` (authored) | Who voices lines | `own_voice` \| `synthetic` \| `mixed` |
| film | `delivery_size` (authored) | Finished picture size | `1080p` \| `4k` |
| film | `budget_usd`, `spend_cap_usd` (authored) | Total allowed; most per batch | `2500`, `400` |
| film | `music_policy` (read, D9) | Sets music line (R24) | `none` \| `source_only` \| `sparse` \| `end_credits_only` \| `scored` |
| film | `price_table` | Path and date of prices | `prices.json`, `2026-09-27` |
| film | `novice_factor` | Hours multiplier | `1.3` until measured |
| film | `contingency_pct` | Money margin | `20` \| `10` |
| film | `estimate` | Film block with `by_tier`, `subscriptions`, `calendar` | `v0_words` \| `v1_shot_list` \| `v2_animatic` \| `v3_actuals` |
| film | `schedule` | Weeks: work, gate, money | file `schedule.json` |
| film (log) | `forecast_history[]` | Each re-forecast | `{"date": "...", "spent": 610, "forecast": 2480, "action": "R11"}` |
| sequence | `estimate` | Same block per sequence | checkpoints C and E |
| scene | `rhythm_class` (authored) | Scene pace | `action_peak` \| `suspense` \| `mixed` \| `dialogue` \| `contemplative` |
| scene | `asl_factor` (read, D10) | Tone multiplier on class ASL | `1.0`, `0.9`, `2.5` |
| scene | `target_asl_s` | Class ASL × `asl_factor`, or override | `2.0` |
| scene | `estimate` | Scene block (§11.2) | see §4 below |
| shot | `cost_class` (authored) | Work the shot needs | `graphic` \| `reuse` \| `still_move` \| `easy` \| `dialogue` \| `hard` |
| shot | `reuse_of` (authored) | Approved shot reused | `SC06-SH080` \| `"none"` |
| shot | `composite_plates` (authored) | Extra elements for compositing | `0`, `1`, `2` |
| shot | `clip_s` | Billed clip length | `5` |
| shot | `gen_slowdown` | Slow-generation factor from `post_ops` | `1` (default), `2` |
| shot | `draft_takes`, `final_takes` | Planned takes (class defaults) | `4`, `7` |
| shot | `est_cost_usd`, `est_minutes` | Shot money and minutes | `4.20`, `38` |
| generation job | `review_min` | User's review minutes (C1 has `cost_usd`, `kept_take`) | `9` |

**Class ASL** [§5, J]: `action_peak` 2.0 s, `suspense` 3.5, `mixed` 4.0, `dialogue` 4.5, `contemplative` 6.0.
**Cost classes** [§6.1] (draft / final takes; minutes): `graphic` 0/0, 10 min to make; `reuse` 0/0, 2 min; `still_move` 0/0, 1 keyframe, 2 min; `easy` 2/3, 5 min review; `dialogue` 2/4, 8 min; `hard` 4/7, 10 min review plus previs 22 min (`previs_level` 2–3) or 20 min phone acting (level 4). Each plate: +1 final take + a comp job (40 min until D6's `est_hours` exist).
**v0 class shares** [§6.1, J] (still-or-graphic / easy / dialogue / hard / plated): action_peak 10/40/5/45/25%; suspense 15/55/10/20/20; mixed 15/55/20/10/15; dialogue 10/35/50/5/10; contemplative 25/60/10/5/10.

## 4. Procedures

**Formulas the validator runs** [§11.1]:
- E1 scene runtime = Σ `duration_s` of active shots + cards (v1), or v0 words: dialogue words ÷ 2.5 + 0.5 s per speech + 1 s per `(beat)`, plus action words × 0.166–0.220 s; warn outside `target_duration` ±10%. Speech durations are floors (A2); A4's intensity table sets non-dialogue shots.
- E2 film = Σ scenes + titles/credits (40–60 s short, ~3 min feature); warn outside `runtime_target_s` ±10%. E3 page check (R3, R22). E4 ASL.
- E5 `clip_s` = max(shortest clip, used + 2 × 0.75 s), rounded up to a length the model accepts (whole seconds if unchosen; minimum 5; hard action-peak shots 7). v0 uses class ASL as used length: 5 s action_peak/suspense, 6 s mixed/dialogue, 8 s contemplative.
- E6 generated s = Σ `clip_s` × (drafts + finals) + Σ plates × `clip_s`; factor warn outside 5–15. E7 video $ = Σ `clip_s` × (drafts × $0.05 + finals × tier) + plates × `clip_s` × tier.
- E8 other money: bible $100–135 (+$10 per character above 7, +$7 per location above 3); storyboard $0.034/shot; keyframes $0.55/shot; ElevenLabs credits = spoken characters × 5 + effect seconds × 40 × 2 (30% of shots get a 3 s effect); music per R24; upscaling (1080p: runtime × 1.5 × $0.02 in v0; 4K: runtime × 1.3 × $0.08); Claude Pro $20 or Max $100 per calendar month; Resolve Studio $295 (premium); then contingency.
- E9 hours = Σ task minutes ÷ 60 (setup 240; macro pass 60/180; checkpoints A+B 35; 25 per scene; 10 per checkpoint C; bible 60/30/6 per character/location/prop; storyboard 0.5; keyframe 4; job 1; review 5/8/10/2; comp 40/plate; voice 20/character + 1.5/line; music 45/cue; post 255/finished minute; delivery 240); central × 1.3, high × 2. E10 weeks = hours ÷ `hours_per_week`. E11 staleness. E12 v3 forecast = spent + remaining shots × measured $ per kept shot by class.

**Recipes** (prompts reproduced exactly) [§10]. Needs an LLM app that runs programs on your files (Claude Code, Cowork, or claude.ai with code execution).
1. **Recipe 0, build and test (once, 20–40 min):** "Write `estimate.py` that implements D13 §11.1, formulas E1 to E12, reading prices from `prices.json` (D13 §11.3) and task minutes from D13 §7.1. It must write only the `estimate` blocks and never change any other field. Then test it on D13 §15.1's SC06 v1 inputs (36 shots: 1 graphic, 3 reuse, 16 easy with 15 clips of 5 s and one of 7 s, 2 dialogue, 14 hard, 2 plates of 5 s; previs 120 minutes for C4 Example A's three plans and master set; used length 49.7 s) and show me whether it gives 1,250 generated seconds, $78 / $157 / $377 and 14.0 base hours. If any number differs, fix the script, not the numbers."
2. **Recipe 1, price table (monthly, 20–30 min):** "Open each page in the `url` fields of `prices.json`. For each item, read today's price and write it with today's date. List every price that changed by more than 10% and every page you could not open. Do not guess a price; mark unreadable ones `unverified`." Then: "Run a 4-second draft take and one keyframe; compare the charge with the table (C1 Recipe 10: stop if it differs by more than 20%)."
3. **Recipe 2, v0 at checkpoint M (10 min):** "For each scene in `scenes_index.json`, propose a `rhythm_class` with a one-line reason. Do not compute anything. Then run `estimate.py --version v0` and show me the film estimate for each D2 option, all three tiers, and weeks at my hours per week." The user fills in and pastes:
```
My limits for this film:
- Most money I will spend in total (US dollars): ____
- Hours a week I can really give it: ____
- A date it must be finished by (or "none"): ____
- Price level of final takes: budget / mid / premium / mixed / not sure
- Voices: my own recordings / made by AI / some of each
- Finished picture size: 1080p / 4K
- Music (D9): none / a few cues / end credits only / fully scored / not sure
```
4. **Recipe 3, v1 per sequence (5 min):** "For each shot in this sequence, set `cost_class` from its `shot_need` using D13 §6.1, set `composite_plates`, and mark `reuse_of` where a framing repeats an approved shot. Then run `estimate.py --version v1 --sequence N` and show the sequence and film totals against the budget." Over budget → Recipe 6.
5. **Recipe 4, schedule (10 min):** "Using the film estimate's phase hours and my hours per week, write `schedule.json` week by week in D13 §8.2's form: work, gate, money leaving. Put each subscription only in the weeks that use it. Mark the high-case end date as well."
6. **Recipe 5, re-forecast after each batch (5 min):** "Read the generation jobs' `cost_usd`, `kept_take` and `review_min`. Run `estimate.py --version v3`. Show: money spent, video money left, dollars per kept shot by cost class, forecast at completion, and any shot past rule R12. If the forecast exceeds the spend cap, list rule R10's steps with the money each saves."
7. **Recipe 6, over budget or time (15 min):** "Apply D13 rule R10 one step at a time. After each step, re-run the estimate and show what changed on screen (which shots, which scenes). Stop when the total fits. Do not touch shots that carry a cardinal function (D2) without asking me." The user approves each step.

**Scene estimate block** [§11.2] (film block adds `by_tier`, `subscriptions`, `calendar`):
```json
"estimate": {
  "version": "v1_shot_list",
  "price_date": "2026-09-27",
  "tier": "mid",
  "runtime_s": 49.7,
  "shots": {"total": 36, "graphic": 1, "reuse": 3, "still_move": 0, "easy": 16, "dialogue": 2, "hard": 14, "composite_plates": 2},
  "asl_s": 1.38,
  "generated_s": {"draft": 464, "final": 786, "factor": 25.2},
  "money_usd": {"video": 157, "images": 19, "other": "film level"},
  "hours": {"base": 14.0, "central": 18.2, "high": 28.0},
  "warnings": ["factor above 15: action peak, expected"],
  "authority": "derived"
}
```

**Calendar** [§8]: P0 setup (1–4% of hours, gate M); P1 stages 0–5 (3–4%, A B C); P2 bible images, storyboards (4–7%); P3 voices, animatic, previs (7–13%, runtime lock, D); P4 takes and review (21–25%, E); P5 compositing (10–15%); P6 post and delivery (37–50%). Weeks = phase hours ÷ `hours_per_week`. A 20-minute short at 20 h/week: weeks 1 P0–P1; 2 bible, shot lists, v1; 3–4 voices, animatic; 5–8 generation; 9–10 comp; 11–12 lock, upscale; 13–15 sound; 16–17 grade, delivery.

## 5. Checklists

- **Before checkpoint M (v0):** Recipe 0 test passed (R25) • prices under 30 days • every scene has a rhythm class (and `asl_factor`) • three tiers shown • runtime low/central/high • page check passed (range under 90 pages) • hours at the user's weekly hours, central and high • R17 checked • limits block answered.
- **After each checkpoint C (v1):** every shot has a cost class • `reuse_of` marked • plates counted • sequence within scene targets ±10% • film total against budget; Recipe 6 if over.
- **Before the first batch:** v2 runtime locked • spend cap in the batch script (C1 Recipe 10) • three-shot price test within 20% • storage checked • voice lines final • every paid plan allows commercial and film use (`licence_flags`).
- **After every batch (v3):** costs and review minutes logged • R11 and R12 checked • forecast history updated • after sequence 1, measured rates replace defaults (R16).
- **Before post:** picture locked • only kept takes upscaled (whole at 1080p, used + handles at 4K) • `music_policy` read before buying music • no ElevenLabs music • sound and music plans booked for scheduled weeks • old plans cancelled after their last job.

## 6. Saying it to AI models

- Ask for classes with one-line reasons, never numbers ("Do not compute anything."), then "run `estimate.py`" with the version and scope (`--version v1 --sequence N`) (P1, R4).
- For prices, forbid guessing: "Do not guess a price; mark unreadable ones `unverified`."
- For cuts, one R10 step at a time and "Do not touch shots that carry a cardinal function (D2) without asking me."
- Paste the limits block once; later prompts refer to "my limits" rather than restating numbers.

## 7. The Catch

**Decisions made** [§4.1, §15, J]:
- Counts re-run by script: 30 scenes, 221 speeches, 1,579 dialogue words, 7,091 action words, 7,657 spoken characters. v0: **1,926–2,309 s, central 2,118 s** (35 min) plus 60 s titles = 2,178 s; 41.7 pages ÷ 1.1 = 2,275 s (7% above v0 central: pass).
- SC06 FREIGHT CAGE (l.198–299; "Another shot sparks off the grid beside her boot." l.226, "Iona hits STOP with her elbow." l.228, "The cage falls." l.240): `action_peak`. v0 whole scene: 92–119 s, 53 shots, 2,512 generated s, video $158 / $318 / $768. v1 fall only (A4's 36 shots, 49.7 s, ASL 1.4): 1,250 generated s (factor 25), $78 / $157 / $377, 14 h base / 18 central / 28 high. Shots 12 and 15 share one POV clip (R5). Shot 19 is a new take (after the black the grid is above her; a reversed shot 8 shows the wrong bodies); shots 20–21 stay reuse candidates, each +$3 if not.
- SC14 ("Over her bed, the grey box. The needle lies flat." l.836): about 9 s, two `still_move` shots. SC15 "The chair is still there." (l.866) reuses the clean room plate that "The bed, and Jude, and the cup, and the figure are gone." (l.864) needs.
- Film (v0): full 583 shots (ASL 3.6), 20,582 generated s (factor 9.7); 20 minutes 329 shots (3.5), 11,496 s (9.9). Money budget / mid / premium: **full $2,372 / $3,990 / $9,853; 20 min $1,402 / $2,321 / $5,850**. Hours base / central / high: full 435 / 565 / 869 (28 weeks at 20 h); 20 min 261 / 339 / 521 (17 weeks). The 20-minute cut saves about 40%, not 45%.
- Voices ≈ 38,000 credits + effects ≈ 42,000 → one ElevenLabs Creator month ($22).

**Flagged for the user**:
- Which D2 option (full ~36 min, Option 2 ~25 min, Option 3 20 min); at 10 h/week the full script runs over a year (R17).
- Tier, total budget and spend cap, hours per week, deadline, own voice or AI, 1080p or 4K.
- Music policy: D9 recommends `none`; the tables assume `scored` (subtract $16–48 and 7.5–14 h if `none`).
- Academy/festival eligibility (D2 R4): 2,178 s is under 2,280 s only if the animatic confirms v0; Follows' short-script ratio would put it near 52 minutes.
- Not in the totals: lip sync in post (~$90), a location sheet per setting (~$120, ~8.5 h), other languages (§6.10).

## 8. Conflicts and open questions

- **ElevenLabs music (corrected here):** every self-serve plan excludes "film, TV, radio, & Studio Games" [V]; the earlier draft of D13 budgeted it. Suno: commercial use only for permitted downloads, no copyright warranty [V].
- **Topaz desktop:** Personal plan is "Limited commercial use" [V]; what that permits [U]. Tables price fal's Topaz route instead.
- **D8 upscaling unit:** D8-R20 adopted (whole takes at 1080p). D8 says whole takes are 2–3× used seconds; this model's clips are about 1.4–1.6×; the validator should sum real `clip_s`.
- **D3 takes:** D3 budgets 3 takes plus alternates (~26,000 characters); D13 keeps 5 tries (~38,000). Both one Creator month.
- **D18:** uses 6 characters a word (~47,000 credits per dubbed language); counted figure is ~4.9 (~38,000). D18 should use the count.
- **D10:** `asl_factor` adopted (R23). Name clash: D10's `contemplative` *tone* (factor ≥ 2.5, ASL never under 10 s) vs D13's `contemplative` *rhythm class* (6 s); combined, 15 s a shot. Builder should rename one (suggestion `still_pace`).
- **D9:** music policy decides music money (R24); SFX film-use terms on ElevenLabs [U].
- **Field names:** D13 `target_duration` = blueprint `target_duration_s`; `clip_s` = A4 `clip_length_s` = C1 batch `duration_s`; `estimate.py` = blueprint `stage.py estimate`. Use the blueprint's names.
- **C2 location count:** C2 budgets 3 location sheets; *The Catch*'s headings name about 20 settings.
- **C2** keyframes 120 of 300 shots vs D13 nearly all (use C2's share only for an animatic film). **A4** assumes Veo's 4/6/8 s clips; the validator reads each shot's `model`. **D2**'s single ASL agrees with rhythm classes within 10%; its 2,100 s vs D13's 2,118 s is rounding.
- **Hold lengths (A1/A2/A4):** A2's speech formula is a floor; A4's table for non-dialogue shots; handles 0.75 s. **Slow motion:** slow generation at real-time playback only (R21). **Short-script page rule:** unresolved until v2.
- **Untested hours model:** post 4.25 h per finished minute and novice factor 1.3 are [J]; *Air Head* ran 2–2.7 h per finished second [V] vs 0.22–0.43 here. Still [U]: Topaz "limited" terms, ElevenLabs SFX film terms, storage prices, SC06 reversed copies.

## 9. Section map

- **Header** labels, fact-check note • **§1** terms • **§2** principles P1–P8 • **§3** dated price table (URLs, roll-over, licence limits) • **§4** runtime v0/v1/v2, Follows page ratios • **§5** shot count, class ASLs • **§6** cost: classes and shares, clip length, video, images, voice, music, upscaling, software, contingency, optional lines • **§7** task minutes, novice factor, *Air Head* calibration • **§8** phases, weekly template • **§9** R1–R25 • **§10** Recipes 0–6 • **§11** E1–E12, estimate blocks, `prices.json` • **§12** fields • **§13** checklists • **§14** failure modes • **§15** examples: SC06, SC14, SC15; *The Catch* tiers × runtimes; *The Long Places* A ($4,963 / $8,181 / $19,553; 61 weeks at 20 h), B ($14,028–55,227; 170 weeks), C ($882 / $1,399 / $3,681; 10.5 weeks); Plan C step 03 (557 generated s, $35 / $69 / $166) • **§16** conflicts • **Sources** 18 web.
