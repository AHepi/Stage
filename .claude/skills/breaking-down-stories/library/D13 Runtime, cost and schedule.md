# D13. Runtime, Cost and Schedule Estimator

*Library file D13. Written 2026-09-27. Test sources: "The Catch" (screenplay, workshop revision of 25 September 2026) and "The Long Places" (prose, 14 chapters).*

> **What this file is for**
> 1. It turns a breakdown (or, before shots exist, the source's word counts) into runtime, shot counts, generated seconds, money across every tool and subscription, and hours of the user's own time.
> 2. It spreads those hours over a calendar, week by week, around checkpoints M and A to E.
> 3. It gives the formulas a script (the validator, never the LLM) runs to write an estimate block for each scene and for the film.
> 4. It re-forecasts during generation from measured costs and says what to cut when money or time runs short.
> 5. It applies all of this to *The Catch* (three price tiers, full length and 20 minutes) and to *The Long Places* (D2's Plans A, B and C).

**Evidence labels.** [V] verified at the named source on 2026-09-27; [U] unverified; [J] this file's judgment, including all arithmetic on the test sources and every default that no source gives. Nearly every per-shot minute and take count below is [J]: they are starting values to be replaced by the user's own measured values after the first sequence (rule R16).

**Staleness.** Prices change monthly. More than 30 days after the price table's date, re-check it before quoting money (C1 §0; rule R7).

**Fact-check note (2026-09-27).** An adversarial re-check opened every web source in the list below and the Suno terms, the Eleven Music terms and Anthropic's API price page, re-counted *The Catch* by script (30 scenes, 221 speeches, 1,579 dialogue words, 7,091 action words, 7,657 spoken characters) and re-ran the arithmetic of §15. Corrections: **ElevenLabs music may not be used in a film on any self-serve plan** (§6.6, R19); Topaz Video's Personal plan has only "Limited commercial use" (§3); credit roll-over is now verified for Runway, ElevenLabs and Suno (§3); 1080p upscaling now covers whole kept takes, as D8-R20 requires (§6.7, R14); voice credits use counted characters (D3), not words × 5.7 (§6.5); the asset-bible scale now matches C2's image counts (§6.4); §15.4's clip lengths now follow §6.2's rounding rule; wrong cross-references fixed (C5 R15, not R26; C1 Recipes 1 and 10, not "P1" and "P10"; C1's `kept_take`); the phase share of P0 and the *Air Head* comparison re-stated. Added: Follows' page ratio by script length (§4.1), `text` and `screen` needs, multi-need shots, slow generation and previs by level (§6), D6/D14/D17 time rows (§7.1), rules R20 to R25, Recipe 0 (build and test the estimator), a film-level estimate block (§11.2), and conflicts with D3, D6, D8, D9, D10 and D18 (§16). The money tables in §15 moved by under 4%.

**Place in the pipeline.** Runs four times, each sharper than the last: v0 at checkpoint M (D2's macro pass), v1 at checkpoint C (shot lists), v2 when the animatic (storyboard frames timed to scratch sound) exists, and v3 after each generation batch at checkpoint E. It reads C5's records, C1's cost fields and D2's `adaptation_plan.json`; it writes only `derived` fields (C5's authority mark for script-computed values).

**What it builds on and does not repeat.** D2 §6 already estimates *The Catch*'s natural runtime (about 35 minutes, range 32 to 44) and cuts it to 20 minutes; D2 §8 sizes *The Long Places* three ways. C1 §10 gives the top-down video cost formula; C2 the image costs; C3 §17A takes per shot; C4 §9 to §10 previs minutes; C5 the checkpoints and the validator. This file joins them into one method and adds what was missing: per-shot cost classes, the non-video money, the user's hours, and the calendar.

---

## 1. Words this file uses (one word per concept)

| Word | Plain meaning |
|---|---|
| **Runtime** | The finished length in seconds, titles and credits included (D2's `runtime_target_s`). |
| **Used length** | The seconds of a shot that appear in the film (C5's `duration_s`). |
| **Clip length** | The seconds of video a model makes for one take; you pay for all of it (`clip_s`, the blueprint's name; A4 calls the same number `clip_length_s`, and C1's batch file sends it as `duration_s`). |
| **Handles** | Extra seconds generated before and after the used part, so the editor can move the cut (C5: 0.5 to 1 s). |
| **Take** | One clip made for one shot (C1). A **draft take** is a cheap, low-resolution test; a **final take** is made on the chosen model at delivery quality. |
| **Generated seconds** | All video seconds billed, kept or not (C1). |
| **Generation factor** | Generated seconds divided by runtime. C1 writes it as overshoot × retake ratio; this file uses the product. |
| **Tier** | The price level of final takes: `budget` (about $0.07 a second), `mid` (about $0.17), `premium` (about $0.45) (C1 §10). |
| **Price table** | A dated file listing every price the estimate uses, each with its web address. |
| **Cost class** | The kind of work a shot needs, which sets its takes, images and minutes (§6.1). |
| **Rhythm class** | A scene's pace, which sets its average shot length (§5). |
| **ASL** | Average shot length: screen time (runtime less titles and credits) divided by number of shots (A4). |
| **Hours** | The user's own working time. The LLM's thinking time and overnight batch runs are not counted. |
| **Novice factor** | A multiplier on hours for a first film (§7.2). |
| **Contingency** | Money added for the unknown, as a percentage. |
| **Spend cap** | The most a batch script may spend before it stops (`spend_cap_usd`: the C1 digest's field for C1 Recipe 10's "Stop if the total cost passes $X"). |
| **Estimate** | The derived block holding runtime, shots, generated seconds, cost and hours for a scene or the film. |
| **Re-forecast** | A new estimate made from money and hours already spent plus the remaining work at measured rates. |
| **Subscription month** | One billing month of a monthly plan, paid whether used or not. |
| **Credits** | A platform's own money unit (Runway, ElevenLabs, Suno, Topaz): the plan buys a number of credits a month, and each job spends some. |
| **Validator** | The pipeline's checking script (C5). It reads the records, does every sum, and writes the `derived` fields. The LLM never writes a total. |
| **Keyframe** | A still picture made first (C2) that a video model animates or must pass through (image-to-video, start or end frame). |
| **Previs** | A rough 3D rehearsal of a shot in Blender, used to fix camera and movement before generating (C4). |
| **Plate / compositing** | A plate is a background clip made so that something else can be laid over it; compositing is the laying-over, done in post (D6). |
| **Animatic** | Storyboard frames cut together in time with scratch voices and sound: a rough film before any video exists. |
| **Picture lock** | The point after which no shot changes length or order; sound, music, grade and upscaling start from it (D8). |
| **Upscaling** | Enlarging a finished clip to a bigger picture size by software (Topaz); 720p, 1080p and 4K are picture heights of 720, 1,080 and about 2,160 lines. |

---

## 2. Core principles

- **P1. One source of numbers.** The LLM proposes classes and durations; a script does every sum (C5 R23, R27). An LLM-written total is ignored.
- **P2. Estimates get sharper in versions.** v0 from words, v1 from the shot list, v2 from the animatic, v3 from actual spending. Each replaces the one before; none is skipped.
- **P3. Ranges, not points.** Report low, central and high for runtime and hours; three tiers for money (D2 P2).
- **P4. You pay per clip, not per used second.** A 1.4-second shot costs the same as a 5-second shot, because most models' shortest clip is 3 to 5 seconds (a few go down to 1 or 2; C1 §3A). Fast cutting is expensive.
- **P5. Video takes dominate the money; post and review dominate the hours.** In the worked examples below, video is about half to two-thirds of the money, and post-production plus take review are about half to three-fifths of the hours [J].
- **P6. Reuse is free.** A refrain, a repeated framing or a recap built from approved clips costs no takes (D2 R18).
- **P7. Measure early.** The first finished sequence gives real minutes per shot and dollars per kept shot. From then on the defaults in this file are retired.
- **P8. Prices are dated.** Every money figure carries the price table's date; a table older than 30 days blocks money output.

---

## 3. The price table (checked 2026-09-27)

These are the prices the formulas use. The validator reads them from `prices.json` (template in §11.3); the LLM refreshes them by Recipe 1.

| Item | Price | Source (checked 2026-09-27) |
|---|---|---|
| Draft takes: Veo 3.1 Lite 720p | $0.05 per second (1080p $0.08; Lite has no 4K; Fast 720p $0.10, 1080p $0.12, 4K $0.30; Standard 720p/1080p $0.40, 4K $0.60) | https://ai.google.dev/gemini-api/docs/pricing [V] |
| Kling 3.0 Pro image-to-video on fal | $0.112 a second audio off, $0.168 audio on, $0.196 with voice control; clips 3 to 15 s | https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video [V] |
| Tier prices for final takes | budget ≈ $0.07, mid ≈ $0.17, premium ≈ $0.45 a second | C1 §10 (its sources checked 2026-09-27) |
| Runway plans | Standard $15 a month ($12 billed yearly), 625 credits; Pro $35 ($28), 2,250; Max $95 ($76), 9,500. Gen-4.5 "60 credits/5s". Roll-over: "On the Standard and Pro plans, monthly credits don't roll over"; on Max "up to one month of unused credits rolls over"; bought credits "never expire" | https://runway.com/pricing [V]. Arithmetic [J]: on Max, Gen-4.5 costs $95 ÷ (9,500 ÷ 12) ≈ $0.12 a second, matching C1. |
| Storyboard image | $0.0168 (Nano Banana 2 Lite, batch) | C2 [V there] |
| Keyframe image | $0.134 (Nano Banana Pro 2K) to about $0.17 (GPT Image 2.5 high) | C2 [V/U there] |
| Upscaling on fal (Topaz) | $0.01 a second up to 720p, $0.02 from 720p to 1080p, $0.08 above 1080p; "Price doubles for 60fps output" | https://fal.ai/models/fal-ai/topaz/upscale/video [V] |
| Topaz Video (desktop) | Personal $59 a month or $299 a year, "Unlimited local rendering", 25 cloud credits a month, **"Limited commercial use"**; Pro $699 a year (or $74 a month on a yearly commitment), "Full commercial use"; extra cloud credits $0.10 each; "Monthly credits expire at the end of each month and do not roll over" | https://www.topazlabs.com/pricing [V]. What "limited" allows is not spelled out on that page [U]: for a film you will show or sell, use fal's per-second Topaz route or read Topaz's licence first. |
| ElevenLabs (voice, effects) | Starter $6 a month, 30,000 credits; Creator $22 ($11 the first month), 121,000; Pro $99, 600,000; Free (10,000) has no commercial use. Yearly billing costs ten months' price. Speech 1 credit a character (Multilingual v2; Flash and Turbo 0.5 to 1). "Unused credits roll over for up to two months" on paid plans; they expire on cancelling or downgrading | https://elevenlabs.io/pricing [V] |
| ElevenLabs music (Eleven Music) | 900 credits a minute, but every self-serve plan, Free to Business, allows commercial use "except film, TV, radio, & Studio Games"; only Enterprise Music allows all media (terms of 26 May 2026). **Not usable for a film's score on a normal plan.** | https://elevenlabs.io/eleven-music-model-specific-terms [V]; https://elevenlabs.io/pricing [V] |
| ElevenLabs sound effects | "40 credits per second when duration is specified"; up to 30 s per effect. Film-use terms for effects not found in the docs [U] (D9 §2.2) | https://elevenlabs.io/docs/overview/capabilities/sound-effects [V] |
| Suno (music) | Pro $8 a month ($76.80 a year), 2,500 credits, 20 song downloads a month; Premier $24 ($230.40 a year), 10,000 credits, 60 downloads; Free: "lawful, personal and non-commercial purposes" only. Terms: you "may commercially exploit Output ... provided you have obtained a permitted download"; Suno "makes no representation or warranty ... that any copyright will vest in any Output"; subscription credits "do not carry over" | https://suno.com/pricing [V]; https://suno.com/terms (revised 10 Aug 2026, effective 3 Sep 2026) [V] |
| Freesound (effects library) | Free; each sound is CC0, CC BY (credit the author), CC BY-NC ("you can't earn any money with the piece of work you create") or the old Sampling+ (no commercial use) | https://freesound.org/help/faq/ [V] |
| DaVinci Resolve | Free version edits and finishes up to UHD at 60 fps; Studio $295 once | https://www.blackmagicdesign.com/products/davinciresolve/studio [V] |
| Blender | Free | C4 [V there] |
| Claude | Pro $20 a month ($17 billed yearly); Max from $100 a month (5× or 20× Pro usage) | https://claude.com/pricing [V]. API alternative for *The Catch*: about $17 on Opus 5.5 at $4 / $20 per million input / output tokens (D1 §7.2; price re-read at https://platform.claude.com/docs/en/about-claude/pricing [V]). |

---

## 4. The runtime model

### 4.1 v0: from words, before any shot exists

For a screenplay, per scene [J method, D2 §6]:

- **Dialogue seconds** = dialogue words ÷ 2.5 + 0.5 per speech + 1 per `(beat)` (A2 Step 9).
- **Action seconds** = action words × 0.166 (low) to 0.220 (high), the range D2 measured on SC06, SC10 and SC13.
- **Scene seconds** = dialogue + action; central = the midpoint.
- **Film** = Σ scenes + titles and credits (40 to 60 s for a short, about 3 minutes for a feature [J]).

For prose: D2 R3 (candidate scenes × 2 to 2.5 minutes), then the step outline's `target_duration` values.

**Cross-check.** Pages ÷ 1.1 gives minutes (Stephen Follows, 30 March 2026: 2,520 US Letter and 351 A4 feature scripts; one page "equals about 55 seconds"; the ratio is pages per minute of released runtime, end credits included) [V]. If v0 central differs from it by more than 25%, check the parse before going on (R3). Two refinements from the same study [V]: A4-paper scripts average 1.02 pages a minute (US Letter 1.1), and the ratio falls with script length: 60 to 89 pages averaged 0.798, 90 to 109 pages 1.0, 110 to 130 pages 1.093, over 150 pages 1.361. No bucket covers scripts under 60 pages, so for a short script the page check is an extrapolation (R22).

*The Catch*, reproduced by script [J]: 30 scenes, 221 speeches, 1,579 dialogue words, 7,091 action words give **1,926 to 2,309 s, central 2,118 s**, exactly D2's figures (the fact-check re-ran the count and got the same). At 41.7 pages (A3's line model at 55 lines a US Letter page), pages ÷ 1.1 gives 2,275 s; v0 central is 7% under it. Pass. But at the shortest bucket's 0.8 pages a minute the same pages would play about 3,130 s (52 minutes), well above v0 high; nothing in the scene-level timing (A2, A4 Worked Example 1) supports that figure, so it is shown as a warning, not used [J]. Measure the animatic (v2) before trusting either.

### 4.2 v1: from the shot list

Runtime = Σ `duration_s` of every shot not `OMITTED` + cards + titles and credits. Each duration comes from A2's defaults (spoken line: words ÷ 2.5 + 0.5 s; small act 1 to 2 s; whole-body move 2 to 4 s; "(beat)" 1 s; "Silence." 2 to 3 s; a turning-point reaction held at least 2 s) and A4's rhythm plan and minimum reading times (insert about 1 s; a face to be read 1.5 s; text 1 s plus 12 to 15 characters a second; mirrored text double). The validator compares each scene with its `target_duration` (the blueprint's `target_duration_s`; ±10%, C5 R27) and the film with `runtime_target_s` (±10%, D2 R9).

**Which duration wins** (the library's recommended resolution of the A1/A2/A4 hold-length conflict): for a shot carrying speech, A2's line formula is a floor, never shortened by A4's intensity table; A4's intensity-to-length table sets non-dialogue shots and where cuts fall; pauses use the blueprint's tiers (short under 1.0 s, medium 1.0 to 2.5 s, long 2.5 to 4.0 s; longer is a deliberate "hold"); handles default to 0.75 s.

### 4.3 v2: from the animatic

Once storyboard frames are cut to scratch voices and sound (A4, C2), the timeline's real durations replace the estimates. This is **runtime lock**: from here, a change in runtime is a story decision logged at a checkpoint, not a revised estimate.

---

## 5. The shot-count model

**Shots = scene seconds ÷ (the ASL of the scene's rhythm class × the scene's `asl_factor`).** Before shot design the LLM assigns a rhythm class; after shot design the shots are counted. `asl_factor` comes from the scene's tone in D10 §2.2 (default 1.0; for example `tense` 0.9, `romantic` 1.2, `kinetic` 0.5 at peaks, and D10's `contemplative` tone 2.5 or more, which is not the same thing as this file's `contemplative` rhythm class, §16); titles and credits carry no shots, so the film count uses runtime less titles and credits.

| `rhythm_class` | ASL (s) | Where the number comes from |
|---|---|---|
| `action_peak` | 2.0 | A4 Worked Example 1: *The Catch*'s fall, 36 shots in 49.7 s (ASL about 1.4); lead-ins run slower [J] |
| `suspense` | 3.5 | [J] between action and dialogue |
| `mixed` | 4.0 | [J] |
| `dialogue` | 4.5 | A4 Worked Example 2: dialogue 3 to 4 s a shot, the recording passage 4 to 6 |
| `contemplative` | 6.0 | [J]; A4: long holds are the scene's extremes |

**Calibration.** In Cinemetrics data summarized by Stephen Follows (films of 1997 to 2016), "the average number of shots in a movie is 1,045"; action films average 1,913 shots at an ASL of 4 seconds, science fiction 6.2 seconds (https://stephenfollows.com/p/many-shots-average-movie, 3 July 2017, checked 2026-09-27) [V; crowd-sourced data, which the article calls "inexact science"]. A4 adds Bordwell: most 1980s films ran 5 to 7 seconds, many 4 to 5. If a film-level ASL comes out under 3 or over 7 seconds for a drama or thriller, re-check the rhythm classes (R3); for other tones the band moves with D10's `asl_factor` (R23).

Results [J]: *The Catch* full length, 583 shots at an ASL of 3.6 s; at 20 minutes, 329 shots at 3.5 s (C1 assumed about 300, D2 about 300 at 4 s). *The Long Places* Plan A, 1,274 shots at 4.6 s (D2: 1,200 to 1,500 at 4 to 5 s).

---

## 6. The cost model

### 6.1 Cost classes

Each shot gets one `cost_class`, chosen from its `shot_need` list (the C1 digest's field, one or more of: dialogue, performance, establishing, exact_start_end, timed_beats, exact_camera, recurring_asset, zero_gravity, long_take, stylised, edit, text, screen, fire, animatic, scope, silent). When a shot has several needs, it takes the most expensive class among them (R20). Final takes follow C3 §17A (3 to 4 for easy shots, 6 to 8 for hard ones); draft takes are extra, cheap tests on a $0.05 route (C1 R13); C1 expects about four takes made per take kept and stops a shot at 10.

| `cost_class` | Covers (C1 `shot_need`) | Draft takes | Final takes | Keyframe | Other time |
|---|---|---|---|---|---|
| `graphic` | Title cards, black, insert graphics made as SVG (C2), editor-made freezes | 0 | 0 | none | 10 min to make |
| `reuse` | An approved clip used again: refrain, repeated framing, recap, flipped or trimmed copy | 0 | 0 | none | 2 min check |
| `still_move` | Still plus a slow push-in made in the editor; `animatic`; near-still shots (C1: "a still is a valid shot") | 0 | 0 | 1 | 2 min review |
| `easy` | `silent`, `establishing`, `recurring_asset`, `exact_start_end` (plus an end frame), `long_take`, `stylised`, `edit`, `fire`, `scope`; `text` and `screen` (each adds one plate, below) | 2 | 3 | 1 | 5 min review |
| `dialogue` | `dialogue`: on-screen speech, voice recorded first (C1 R1) | 2 | 4 | 1 | 8 min review |
| `hard` | `zero_gravity`, `exact_camera`, `timed_beats`, `performance`, creatures, violence split into cause and effect | 4 | 7 | 1 | 10 min review; previs 15 to 30 min (C4 Recipe 3) when `previs_level` is 2 or 3; a phone performance, about 20 min, when it is 4 (C1 R12) |

Separately, `composite_plates` (a whole number, any class) counts extra elements made for compositing, such as an empty room, blood beads, screen content or a sign's text (C1 rules 6 and 8, Recipe 9, Example 2; D6). Each plate adds one final take and a comp job. Minutes per comp job come from D6 §7 once the comp plan exists (its `est_hours`; D6's "later" times run from 10 minutes for a static screen to 1 to 2 hours for a video comp of a person); before that, use 40 minutes a plate [J]. D6's helper tools (mattes, removal, inpainting) add about $0.04 to $0.70 per composited 5-second shot; at most about $70 for *The Catch*'s 96 plates, so it is left inside contingency [J].

Before shot design (v0), each rhythm class carries default shares [J]:

| `rhythm_class` | still or graphic | easy | dialogue | hard | shots with a plate |
|---|---|---|---|---|---|
| `action_peak` | 10% | 40% | 5% | 45% | 25% |
| `suspense` | 15% | 55% | 10% | 20% | 20% |
| `mixed` | 15% | 55% | 20% | 10% | 15% |
| `dialogue` | 10% | 35% | 50% | 5% | 10% |
| `contemplative` | 25% | 60% | 10% | 5% | 10% |

### 6.2 Clip length

**`clip_s` = the larger of the model's shortest clip and (used length + 2 × handle), rounded up to a length the model accepts** (C1 §3A: Veo 4, 6 or 8 s; Kling 3 to 15 s in whole seconds; Seedance 2.5 4 to 30 s; Wan 3.0 2 to 30 s). Defaults [J]: handle 0.75 s; shortest clip 5 s; round up to the next whole second when the model is not yet chosen; hard shots in an action peak, 7 s. So a 1.4-second fall shot bills 5 seconds per take, and a 12-second locked-off hold bills 14 (13.5 rounded up; on Veo it cannot be made in one clip, since Veo stops at 8 s).

- **In v0** (no shots yet), the used length is the rhythm class's ASL, so `clip_s` is 5 s for `action_peak` (7 s for its hard shots) and `suspense`, 6 s for `mixed` and `dialogue`, and 8 s for `contemplative`.
- **Slow generation.** If a shot is generated in slow motion and sped up in the edit to real time (the library's allowed use of slow motion, logged in `post_ops`), then the used length inside the clip is the screen length × the slowdown (`gen_slowdown`, for example 2 for half speed), before handles are added (R21).

### 6.3 Video money per shot

**Video cost = `clip_s` × (draft takes × draft price + final takes × tier price) + plates × `clip_s` × tier price.** Draft price $0.05 (Veo 3.1 Lite 720p [V]; Wan 3.0 480p, C1).

**Top-down cross-check (C1 §10).** Generated seconds = runtime × generation factor; C1's lean case is 4.5, typical 8, heavy 12. The bottom-up method gives 9.7 to 9.9 for *The Catch* (many hard shots, a 1.4-second fall) and 7.2 for *The Long Places* (quieter). The validator warns when the film's factor falls outside 5 to 15.

### 6.4 Images (C2)

- **Asset bible**: $100 to 135 for *The Catch* (C2 §3.7 and Recipe R2: about 7 characters × 30 kept images, 3 locations × 20, 15 props × 4 and 8 style frames, about 330 kept images at three tries each). Scale for another work [J, from C2's counts at about $0.12 a try]: add about $10 per character above seven and $7 per location above three. (*The Catch*'s headings name about 20 distinct settings; C2 groups them into three sets. If each setting gets its own sheet, add about $120; see §16.)
- **Storyboard**: two tries per shot at $0.0168 = $0.034 a shot.
- **Keyframes**: about $0.55 per keyframed shot (about three tries at $0.134 to 0.17; C2's $50 to 80 for about 120 video shots).

### 6.5 Voice and sound effects (D3 and D9 now exist; their figures are used here)

ElevenLabs credits needed [J] = spoken characters × 5 tries + generated effect seconds × 40 × 2 tries. Count the characters by script (*The Catch*: 7,666 in D3's count, 7,657 in this check; about 4.9 characters a word). If they are not yet counted, use words × 4.9. Assume one 3-second generated effect for 30% of shots; the rest come from Freesound (check each licence) or a library. Choose the smallest plan whose monthly credits cover it; commercial use starts at Starter. *The Catch* needs about 38,000 credits for voices and 42,000 for effects, so one month of Creator ($22; $11 if it is the account's first month). D3 plans only three takes plus alternates (about 26,000 characters); this file keeps five tries as the budget case. Paid-plan credits roll over for up to two months but are lost on cancelling, so cancel only after the last effect is made (R13).

- **Own voice:** voice money is $0, but add 1 to 2 minutes a line (R19).
- **Lip sync in post** (D3's route for silent-model or performance-transfer pictures): add D3 §12's figure, about $90 for *The Catch* at full length if 45% of line-seconds still show mouths [J, D3].
- **Cheaper effects route:** a video-to-audio pass over the whole film on fal (Sonilo, $0.009 a second of output per sample; D9 §2.3) costs about $20 for *The Catch* at full length; fal's page says "for commercial use" (D9 [V]).

### 6.6 Music (D9 now exists; its music policy sets the count)

Read D9's `music_policy` first (set by the user at checkpoint B). If `none` (D9's recommended start for *The Catch*), music money and cue hours are 0. If `sparse` or `end_credits_only`, cues = D9's `cue_budget` (3 or fewer in a short). If `scored`, cues ≈ runtime ÷ 120 s [J]. Downloads ≈ cues × 1.5 [J]. Suno Pro gives 20 downloads a month, Premier 60; only downloaded songs may be used commercially (Suno terms). **Do not budget ElevenLabs music for a film:** its self-serve terms exclude "film, TV, radio, & Studio Games" (R19). Lyria 3.5 on the Gemini API, $0.08 a song (D9 §2.1), is another route; read its terms before use.

### 6.7 Upscaling

Only kept takes, only after picture lock (fal Topaz [V]: $0.01 a second up to 720p, $0.02 from 720p to 1080p, $0.08 above 1080p; double for 60 fps):

- **To 1080p:** upscale whole kept takes, so that file names and frame counts stay the same and the edit relinks (D8-R20). Seconds = Σ `clip_s` of kept takes and plates; in v0 use runtime × 1.5 [J; the model's clips average about 1.4 to 1.6 times the used length. D8's "2 to 3 times" assumes 8-second clips].
- **To 4K:** upscale only the used seconds plus handles, runtime × 1.3, at $0.08 (D8-R20; R14). The *Air Head* team "did all of Air Head at 480 for speed and then upr[e]s[ed] using Topaz" (fxguide [V]), which is the same idea: draft cheap, upscale only what is kept.

### 6.8 Software and LLM

Blender free; DaVinci Resolve free (edits and finishes up to Ultra HD at 60 fps; Studio $295 once, used here only in the premium tier); Claude Pro $20 a month for every month of the calendar (premium: Max, $100). No aggregator subscription is assumed: fal and Replicate bill per second (C1 §7). Topaz's desktop app is not assumed either: its Personal plan carries only "Limited commercial use" (§3), so the tables price fal's per-second Topaz route.

### 6.9 Contingency and storage

Contingency is 20% of money for a first film, falling to 10% once v3 actuals cover half the shots [J]. Storage is not priced: count takes × 5 to 15 MB per 5-second 1080p take [J] and make sure the space exists before the first batch.

### 6.10 Optional lines (added only when the user asks for them)

- **Other languages** (D18): about 38,000 ElevenLabs credits per dubbed language for *The Catch* at five tries (7,666 characters; D18 used 6 characters a word and got about 47,000), inside one Creator month; plus D18 Recipe 5's 3 to 6 hours of dubbing work per language, Recipe 4's 1 to 2 hours of translation, and Recipe 6's 10 minutes per translated graphic.
- **Audio description** (D18): priced per language once D18's script exists; D18 notes that scenes played in another language with subtitles roughly double the description work.
- **Festival fees, music licences, insurance, legal review** (D4): not priced here.

---

## 7. The time model

### 7.1 Minutes per task (a novice with an LLM doing the technical work)

| Task | Unit | Minutes | Source |
|---|---|---|---|
| Accounts, connectors, price table, first test | once | 240 | C1 Recipe 1 (15 min), C2 Recipe R1 (30 to 60 min), C4 Recipe 1 (30 min), Recipe 0 and 1 here; [J] total |
| Intake of a scanned or messy source | once | 0 for a clean text file; 30 to 90 for OCR of a 40 to 120 page scan | D14 Recipe I5 |
| Macro pass and checkpoint M | once | 60 (screenplay), 180 (novel) | D2 §5 |
| World and locale research | locale | 30 to 90 per locale; 20 per anachronism sweep; 2 per frame checked | D17 Recipes 3, 5, 7 (not in §15's totals; add for period or foreign settings such as *The Long Places*) |
| Checkpoints A and B | once | 35 | C5 (A 5 min; B 15 to 30 min) |
| Stages 0 to 5 per scene, with validator fixes | scene | 25 | [J]; D1 plans stages 0 to 5 for chapter I of *The Long Places* in about 2 hours |
| Checkpoint C | sequence of about 6 scenes | 10 | C5 |
| Asset bible | main character / location / prop | 60 / 30 / 6 | [J] from C2 Recipe R2's image counts (30 images a character, 20 a location, 4 a prop) |
| Storyboard pick | shot | 0.5 | C2 (about 10 s a pick, plus layout and drift checks) |
| Keyframe | keyframed shot | 4 | [J] (about 3 tries, check, local fix) |
| Previs | hard shot; location master set | 22; 30 | C4 Recipes 2 and 3 (15 to 30; 20 to 40). v0 counts every hard shot; v1 counts only shots with `previs_level` 2 or 3, and 20 min of phone acting for level 4 |
| Job preparation | video shot | 1 | [J] (batch script, C1 Recipe 10) |
| Take review | easy / dialogue / hard / still or reuse | 5 / 8 / 10 / 2 | C1 §10 (5 to 10 min a shot) |
| Compositing | plate | 40 until D6's comp plan exists, then its `est_hours` | [J]; D6 §7 gives 10 min to 2 h per job once practised, up to 4 h the first time |
| Voice | speaking character; line | 20; 1.5 | [J]; D3's voice-design recipe takes about 20 min a voice |
| Music | cue | 45 | [J]; 0 when D9's `music_policy` is `none` |
| Post: edit, sound design and mix, grade and conform | finished minute | 90 + 120 + 45 | [J]; D8 gives procedures but no times |
| Delivery: exports, captions, checks | once | 240 | [J] |

### 7.2 Novice factor and ranges

Base hours = Σ tasks. **Central = base × 1.3; high = base × 2** [J]. After sequence 1, replace both with measured minutes per shot by cost class (R16).

### 7.3 Calibration against published accounts

- ***Air Head*** (Shy Kids, Sora, 2024): "a minute and a half of footage", "a team of just 3 people", "in around 1.5 to 2 weeks", "probably 300:1 in terms of the amount of source material to what ended up in the final", plus a full grade, Topaz upscaling and rotoscoping in After Effects (https://www.fxguide.com/fxfeatured/actually-using-sora/, checked 2026-09-27) [V]. At 40-hour weeks [J], that is about 180 to 240 hours, or 2 to 2.7 hours per finished second.
- **Runway Gen:48**: entrants make "a 1-4 minute video" in about 48 hours (August 2025 rules, https://runway.com/gen48/terms, checked 2026-09-27) [V].
- **This model**: *The Catch* at 20 minutes costs 0.22 hours per finished second at base, 0.28 central, 0.43 high [J]. That is roughly 5 to 12 times faster per second than *Air Head* (7 to 10 times at the central case), because 2026 models take start and end frames and references and keep about one take in four (C1), where *Air Head* kept one second in 300. Against that, *Air Head*'s team were professionals and this model assumes a novice. This is the model's largest uncertainty; hence R15.
- Vendor blog claims of "2 to 5 days" per AI short (for example on invideo.io; seen in search results only [U]) are not first-hand production accounts, so they are excluded [J].

---

## 8. From hours to a calendar

### 8.1 Phases and checkpoints

| Phase | Work | Ends at | Share of hours [J] |
|---|---|---|---|
| P0 | Accounts, price table, constraints, macro pass | Checkpoint M (D2) | 1 to 4% |
| P1 | Stages 0 to 5: scene list, analysis, bible text, ledger, scenes, shots | Checkpoints A, B, C | 3 to 4% |
| P2 | Asset bible images, storyboard frames | Bible approved; v1 estimate | 4 to 7% |
| P3 | Voices (scratch, then final), animatic, previs of hard shots | Runtime lock (v2); checkpoint D | 7 to 13% |
| P4 | Keyframes, draft and final takes, review, by sequence | Checkpoint E per sequence; v3 after each | 21 to 25% |
| P5 | Compositing | Every plate placed | 10 to 15% |
| P6 | Edit to picture lock, upscaling, sound, music, grade, delivery | Delivered film | 37 to 50% |

**Weeks per phase = phase hours ÷ `hours_per_week`.** Phases overlap by sequence: while sequence 2 is in P4, sequence 1 can be in P5. Overlap shortens the calendar a little; it never reduces the hours.

### 8.2 Week-by-week template (a short of about 20 minutes, 20 hours a week, central case)

| Week | Work | Gate | Money leaving |
|---|---|---|---|
| 1 | P0 and P1: Recipe 1 price table; D2 macro pass; scene list; stages 1 to 3; v0 shown beside D2's options | M, A | LLM month 1 |
| 2 | Bible text and identity keys; asset bible images (C2 Recipe R2); shot lists per sequence; storyboard frames; v1 estimate | B, C (each sequence) | Images |
| 3 to 4 | Scratch voices, animatic, runtime lock (v2); final voices; previs of hard shots | D | Voice month 1 |
| 5 to 8 | Generation, one sequence a week: keyframes, drafts, finals, review; re-forecast after each | E (each sequence) | Video; LLM months 2 to 3 |
| 9 to 10 | Compositing (sequence 1 can start in week 7) | All plates placed | Plates |
| 11 to 12 | Edit to picture lock; upscale kept takes (R14) | Picture lock | Upscaling |
| 13 to 15 | Sound design, effects, music, mix | Mix approved | Voice or effects month 2; music month |
| 16 to 17 | Grade, captions, exports, full-length check viewing | Delivered | LLM month 4 |

For other runtimes or weekly hours, scale each row by that film's phase hours (§15 gives them for every worked example).

---

## 9. Decision rules

A plain "then" is firm; "then consider" is a default, broken only with a one-line reason in the estimate's `notes` (A2 convention).

**Versions and checks**

- **R1.** If no shots exist yet, then run v0 from word counts and show low, central and high beside D2's format options at checkpoint M, because format and runtime fix every later budget (D2 P1) and a single number hides a spread of about 20%.
- **R2.** If a sequence's shot list passes checkpoint C, then replace v0 for its scenes with v1 computed from the shot records, because counts by cost class beat default shares.
- **R3.** If v1 runtime differs from pages ÷ 1.1 by more than 25%, or the film's ASL falls outside 3 to 7 seconds, (or outside the band moved by R23), then look for missing scenes, dialogue counted twice, durations below A4's minimums, or wrong rhythm classes before approving, because on *The Catch* v0 and the page rule agree within 7%.
- **R4.** If an LLM states a total, then ignore it and run the validator, because only the script's arithmetic counts (C5 R23).

**Shots and takes**

- **R5.** If a shot's used length is shorter than the model's shortest clip, then bill the shortest clip; and if consecutive shots share one camera setup and one continuous action, then consider making one clip and cutting it into those shots, because each 1.4-second shot otherwise pays for 5 seconds on every take. This is still one shot per request (C5 R15): the cut is made in the edit. Different angles remain separate requests.
- **R6.** If a framing repeats (a refrain, A4's "repeat the framing" across a turn, a recap), then mark it `reuse` and name the approved shot in `reuse_of`, because reuse costs no takes (D2 R18). If the reused copy is reversed or flipped, then check it plays correctly before relying on it; if the new scene's time of day, light or character state differs (a night shot cannot stand in for first light), then reuse the saved setup, not the clip, and cost a new take.
- **R7.** If the price table is more than 30 days old, then the validator prints no money until Recipe 1 has run again, because prices and routes change monthly (C1 §0).
- **R8.** If a shot's `shot_need` is `zero_gravity`, `exact_camera`, `timed_beats` or `performance`, or it shows a creature, then cost it `hard`, because these fail most often (C1 R8: 83 to 94% of clips from five late-2025 models had visible physics glitches).

**Money**

- **R9.** If the user has not chosen a tier, then show all three and the mixed option "drafts at $0.05, finals at mid, dialogue close-ups at premium" [J], because the choice is theirs.
- **R10.** If the v1 total exceeds the budget, then cut in this order, re-running after each step: (1) near-still shots become `still_move`; (2) non-dialogue finals move to the budget tier; (3) 4K upscaling becomes 1080p; (4) composite plates are designed out where the story allows; (5) D2 R10's runtime cuts; (6) C1's animatic film (only dialogue close-ups and key images generated); because each step costs the story more than the one before.
- **R11.** If spending passes 50% of the video budget before 50% of shots are kept, then move the remaining non-dialogue shots to the budget tier and re-forecast (C1 §10).
- **R12.** If one shot's spending passes three times its estimate, or it reaches 10 final takes, or 4 takes in a row have failed on one route, then stop and change method (C1 §10: start and end frames, previs, compositing, or still with push-in), because more takes on a failing route rarely rescue it (C3 §17A rule 2 stops at 4 failed takes on one model). The `hard` default (4 drafts + 7 finals) stays inside these limits only if the drafts run on a cheap route.
- **R13.** If a monthly plan is used, then book only the months the schedule needs and cancel after the last job that spends its credits (ElevenLabs credits are lost on cancelling or downgrading); if its credits expire monthly (Topaz: "do not roll over"; Runway Standard and Pro; Suno), then batch that work into one month, because an unused month still bills.
- **R14.** If upscaling, then do it only after picture lock and only on kept takes: to 1080p, whole kept takes (D8-R20, so the edit relinks); to 4K, only the used seconds plus handles, and only if 4K delivery is required, because 4K costs four times as much ($0.08 against $0.02 a second) and trimmed files break relinking at 1080p where the saving is small.

**Hours and calendar**

- **R15.** If a date matters (a festival deadline), then schedule on the high case until sequence 1's actuals exist, because the one first-hand published account ran several times slower per second than this model's central case (§7.3).
- **R16.** If sequence 1 is finished, then replace the novice factor and default takes with measured values (minutes per shot by cost class, takes per kept shot, dollars per kept shot), because measured rates beat defaults.
- **R17.** If central hours ÷ `hours_per_week` exceeds 26 weeks for a short or 52 for anything else, then offer a shorter runtime or a pilot before checkpoint M [J], because a long solo project is likely to stall before it is finished.
- **R18.** If the format is a series, then estimate and make episode 1 to picture lock before generating episode 2, because episode 1's actuals correct the forecast for the rest.
- **R19.** If the user records their own lines, then voice money is $0 but add 1 to 2 minutes a line; if the voices are synthetic, then choose the smallest plan with commercial use whose credits cover the lines at five tries, because free plans exclude commercial use (ElevenLabs, Suno). If a tool's terms exclude film (ElevenLabs music on every self-serve plan: "except film, TV, radio, & Studio Games"), then do not budget it for the film at all; and if a tool licenses only downloaded output (Suno), then budget downloads, not credits.

**Added in the fact-check**

- **R20.** If a shot has more than one `shot_need`, then give it the most expensive class among them (`hard` over `dialogue` over `easy`), and add one plate for each of `text` and `screen`, because the shot must survive its hardest part and text and screens are composited (C1 rule 6, Recipe 9).
- **R21.** If a shot is generated slowed down and played back at real time (`gen_slowdown` above 1), then bill `clip_s` on the screen length × `gen_slowdown` plus handles, because the model makes every slowed second (the library allows slow generation only when playback is real time).
- **R22.** If the source is a screenplay under 90 pages, then show the page check as a range (pages ÷ 1.1 to pages ÷ 0.8) beside v0 and mark it "extrapolated" under 60 pages, because Follows' 60 to 89 page scripts ran 0.8 pages a minute and no data exist below 60 pages (§4.1).
- **R23.** If a scene has a D10 tone with an `asl_factor` other than 1, then multiply the rhythm class's ASL by it and move the E4 warning band by the same factor, because a slow-cinema or kinetic film is meant to fall outside the drama band (D10 §13).
- **R24.** If D9's `music_policy` is `none`, then music money and cue hours are 0; if `sparse` or `end_credits_only`, then cues = `cue_budget`; only `scored` uses runtime ÷ 120 s, because the music policy, not the runtime, decides how much music exists.
- **R25.** If the validator is new or has been changed, then run it on §15.1's SC06 inputs before any other use and accept it only if it reproduces 1,250 generated seconds, $78 / $157 / $377 and 14.0 base hours, because a wrong formula corrupts every later estimate silently (Recipe 0).

---

## 10. Recipes (the user pastes the prompt; the LLM and its scripts do the work)

You need an LLM app that can run small programs on your files (Claude Code, Cowork, or claude.ai with code execution switched on; D1). You never read the code or the JSON; you read the tables the LLM shows you.

**Recipe 0. Build and test the estimator (20 to 40 minutes, once; free).** *Prompt:* "Write `estimate.py` that implements D13 §11.1, formulas E1 to E12, reading prices from `prices.json` (D13 §11.3) and task minutes from D13 §7.1. It must write only the `estimate` blocks and never change any other field. Then test it on D13 §15.1's SC06 v1 inputs (36 shots: 1 graphic, 3 reuse, 16 easy with 15 clips of 5 s and one of 7 s, 2 dialogue, 14 hard, 2 plates of 5 s; previs 120 minutes for C4 Example A's three plans and master set; used length 49.7 s) and show me whether it gives 1,250 generated seconds, $78 / $157 / $377 and 14.0 base hours. If any number differs, fix the script, not the numbers." Accept it only when all four match (R25). In the pipeline the same code runs as `stage.py estimate` (blueprint Step 10).

**Recipe 1. Price table (20 to 30 minutes, once a month).** *Prompt:* "Open each page in the `url` fields of `prices.json`. For each item, read today's price and write it with today's date. List every price that changed by more than 10% and every page you could not open. Do not guess a price; mark unreadable ones `unverified`." Then: "Run a 4-second draft take and one keyframe; compare the charge with the table (C1 Recipe 10: stop if it differs by more than 20%)."

**Recipe 2. v0 at checkpoint M (10 minutes).** *Prompt:* "For each scene in `scenes_index.json`, propose a `rhythm_class` with a one-line reason. Do not compute anything. Then run `estimate.py --version v0` and show me the film estimate for each D2 option, all three tiers, and weeks at my hours per week." The user answers the constraints once, by filling in and pasting this block (any line may say "not sure"; the LLM then shows every option):

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

**Recipe 3. v1 after each checkpoint C (5 minutes a sequence).** *Prompt:* "For each shot in this sequence, set `cost_class` from its `shot_need` using D13 §6.1, set `composite_plates`, and mark `reuse_of` where a framing repeats an approved shot. Then run `estimate.py --version v1 --sequence N` and show the sequence and film totals against the budget." If the film total exceeds the budget, run Recipe 6.

**Recipe 4. Schedule (10 minutes).** *Prompt:* "Using the film estimate's phase hours and my hours per week, write `schedule.json` week by week in D13 §8.2's form: work, gate, money leaving. Put each subscription only in the weeks that use it. Mark the high-case end date as well."

**Recipe 5. Re-forecast after each generation batch (5 minutes).** *Prompt:* "Read the generation jobs' `cost_usd`, `kept_take` and `review_min`. Run `estimate.py --version v3`. Show: money spent, video money left, dollars per kept shot by cost class, forecast at completion, and any shot past rule R12. If the forecast exceeds the spend cap, list rule R10's steps with the money each saves."

**Recipe 6. Over budget or over time (15 minutes).** *Prompt:* "Apply D13 rule R10 one step at a time. After each step, re-run the estimate and show what changed on screen (which shots, which scenes). Stop when the total fits. Do not touch shots that carry a cardinal function (D2) without asking me." The user approves each step.

---

## 11. The validator's arithmetic and the estimate block

### 11.1 Formulas (script only; C5 R27)

- **E1 Scene runtime** = Σ `duration_s` of active shots + cards (v1) or the v0 word model. Warn if outside `target_duration` ±10%.
- **E2 Film runtime** = Σ scenes + titles and credits. Warn if outside `runtime_target_s` ±10%.
- **E3 Page check**: |E2 − pages ÷ 1.1 × 60| ÷ (pages ÷ 1.1 × 60) > 0.25 → warn (screenplays only). Under 90 pages, also print pages ÷ 0.8 × 60 as the high reference (R22).
- **E4 ASL** = (E2 − titles and credits) ÷ shots; warn outside 3 to 7 s for dramas and thrillers, or outside (3 to 7) × the film's runtime-weighted `asl_factor` for other tones (R23).
- **E5 Clip length** per shot as in §6.2, using the shot's `model` lengths from the price table, and `gen_slowdown` (R21).
- **E6 Generated seconds** = Σ `clip_s` × (draft takes + final takes) + Σ plates × `clip_s`. Generation factor = E6 ÷ E2; warn outside 5 to 15.
- **E7 Video money** = Σ `clip_s` × (draft takes × draft price + final takes × tier price) + plates × `clip_s` × tier price.
- **E8 Other money**: images (§6.4), voice and effects (§6.5), music (§6.6, after `music_policy`, R24), upscaling (§6.7), software and LLM months (§6.8), optional lines the user asked for (§6.10), then contingency (§6.9) on the sum.
- **E9 Hours** = Σ task minutes (§7.1) ÷ 60; central × 1.3, high × 2 (or the measured factor).
- **E10 Calendar**: weeks = hours ÷ `hours_per_week`; subscription months from `schedule.json`.
- **E11 Staleness**: `price_date` more than 30 days before today → no money output.
- **E12 Re-forecast (v3)**: forecast = money spent + Σ remaining shots × measured dollars per kept shot of their cost class; the same for hours. Rule R11 and R12 checks.

### 11.2 Estimate block (scene level; film level has the same keys plus `by_tier`, `subscriptions` and `calendar`)

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

Film level (*The Catch*, D2 Option 3, v0, mid tier; figures from §15.2):

```json
"estimate": {
  "version": "v0_words",
  "price_date": "2026-09-27",
  "tier": "mid",
  "runtime_s": {"low": 1094, "central": 1200, "high": 1305, "target": 1200},
  "shots": {"total": 329, "still_or_graphic": 41, "easy": 149, "dialogue": 73, "hard": 67, "composite_plates": 57},
  "asl_s": 3.5,
  "generated_s": {"draft": 4140, "final": 7356, "factor": 9.9},
  "money_usd": {"video": 1458, "images": 292, "upscale": 36, "voice_effects": 44, "music": 24, "llm": 80, "software": 0, "contingency": 387, "total": 2321},
  "by_tier": {"budget": 1402, "mid": 2321, "premium": 5850},
  "hours": {"base": 261, "central": 339, "high": 521},
  "subscriptions": [{"plan": "claude_pro", "months": 4}, {"plan": "elevenlabs_creator", "months": 2}, {"plan": "suno_premier", "months": 1}],
  "calendar": {"hours_per_week": 20, "weeks_central": 17, "weeks_high": 26, "schedule": "schedule.json"},
  "warnings": ["page check extrapolated: script under 60 pages (R22)", "music line assumes music_policy scored; D9 default is none (R24)"],
  "authority": "derived"
}
```

The runtime low and high here apply the spread of *The Catch*'s v0 word model (1,926 to 2,309 s around 2,118, about ±9%) to the cut's 1,160 story seconds, plus 40 s of titles [J].

### 11.3 `prices.json` (shape)

```json
{"price_date": "2026-09-27", "currency": "USD",
 "video": {"draft": {"per_s": 0.05, "model": "Veo 3.1 Lite 720p", "url": "https://ai.google.dev/gemini-api/docs/pricing"},
           "budget": {"per_s": 0.07}, "mid": {"per_s": 0.17}, "premium": {"per_s": 0.45},
           "min_clip_s": 5, "handle_s": 0.75},
 "image": {"storyboard_try": 0.0168, "keyframe_shot": 0.55, "bible_base": 100,
           "bible_per_character_above_7": 10, "bible_per_location_above_3": 7},
 "upscale": {"to_1080p_per_s": 0.02, "above_1080p_per_s": 0.08, "whole_take_factor_v0": 1.5, "handles_factor": 1.3,
             "url": "https://fal.ai/models/fal-ai/topaz/upscale/video"},
 "plans": {"claude_pro": 20, "claude_max": 100, "elevenlabs_starter": 6, "elevenlabs_creator": 22,
           "elevenlabs_pro": 99, "suno_pro": 8, "suno_premier": 24, "resolve_studio_once": 295},
 "credits": {"elevenlabs_creator_month": 121000, "tts_per_char": 1, "sfx_per_s": 40},
 "licence_flags": {"elevenlabs_music": "no_film_use_on_self_serve", "suno": "commercial_only_for_downloads",
                   "topaz_personal": "limited_commercial_use", "free_plans": "no_commercial_use"}}
```

---

## 12. Fields this subject adds

Enums are lowercase `snake_case`; empty is `"none"`. Every field below is `derived` unless marked `authored`.

| Level | Field | Meaning | Allowed values / example |
|---|---|---|---|
| film | `tier` (authored) | Price level of final takes | `budget` \| `mid` \| `premium` \| `mixed` |
| film | `hours_per_week` (authored) | User's available hours | `20` |
| film | `deadline` (authored) | Date that must be met, or none | `2027-03-01` \| `"none"` |
| film | `voice_source` (authored) | Who voices the lines | `own_voice` \| `synthetic` \| `mixed` |
| film | `delivery_size` (authored) | Finished picture size; decides the upscale route | `1080p` \| `4k` |
| film | `budget_usd`, `spend_cap_usd` (authored) | Total money allowed; most any one batch may spend (the blueprint and C1 digest already hold `spend_cap_usd`) | `2500`, `400` |
| film | `music_policy` (read, owned by D9) | Sets the music line (R24) | `none` \| `source_only` \| `sparse` \| `end_credits_only` \| `scored` |
| film | `price_table` | Path and date of the prices used | `prices.json`, `2026-09-27` |
| film | `novice_factor` | Hours multiplier | `1.3` until measured |
| film | `contingency_pct` | Money margin | `20` \| `10` |
| film | `estimate` | Film block (§11.2) with `by_tier`, `subscriptions`, `calendar` | versions `v0_words` \| `v1_shot_list` \| `v2_animatic` \| `v3_actuals` |
| film | `schedule` | Weeks with work, gate, money | file `schedule.json` |
| sequence | `estimate` | Same block per sequence | used at checkpoints C and E |
| scene | `rhythm_class` (authored) | Scene pace | `action_peak` \| `suspense` \| `mixed` \| `dialogue` \| `contemplative` |
| scene | `asl_factor` (read, owned by D10) | Tone multiplier on the class ASL | `1.0`, `0.9`, `2.5` |
| scene | `target_asl_s` | ASL from the class × `asl_factor`, or overridden | `2.0` |
| scene | `estimate` | Scene block | §11.2 |
| shot | `cost_class` (authored) | Work the shot needs | `graphic` \| `reuse` \| `still_move` \| `easy` \| `dialogue` \| `hard` |
| shot | `reuse_of` (authored) | Approved shot reused | `SC06-SH080` \| `"none"` |
| shot | `composite_plates` (authored) | Extra elements for compositing | `0`, `1`, `2` |
| shot | `clip_s` | Billed clip length (A4's `clip_length_s`) | `5` |
| shot | `gen_slowdown` | How much slower than real time the clip is generated (from `post_ops`) | `1` (default), `2` |
| shot | `draft_takes`, `final_takes` | Planned takes (defaults from class) | `4`, `7` |
| shot | `est_cost_usd`, `est_minutes` | Shot's money and hours | `4.20`, `38` |
| generation job | `review_min` | Minutes the user spent reviewing (C1's `cost_usd` and `kept_take` already exist) | `9` |
| film (log) | `forecast_history[]` | Each re-forecast: date, spent, forecast, action taken | `{"date": "...", "spent": 610, "forecast": 2480, "action": "R11"}` |

---

## 13. Checklists

**Before checkpoint M (v0):** Recipe 0 test passed (R25) • price table under 30 days old • every scene has a rhythm class (and D10's `asl_factor` if the tone is set) • three tiers shown • runtime low, central and high • pages ÷ 1.1 check passed (screenplays; range shown under 90 pages, R22) • hours at the user's weekly hours, central and high • R17 checked • the user's limits block (Recipe 2) answered.

**After each checkpoint C (v1):** every shot has a cost class • reused framings marked with `reuse_of` • plates counted • sequence within its scene targets ±10% • film total against budget; Recipe 6 if over.

**Before the first generation batch:** v2 runtime locked • spend cap set in the batch script (C1 Recipe 10) • three-shot price test within 20% (C1 Recipe 10) • storage space checked • voice lines final for dialogue shots • every paid plan in use allows commercial and film use (R19; `licence_flags` in `prices.json`).

**After every batch (v3):** costs and review minutes logged • rules R11 and R12 checked • forecast history updated • after sequence 1, measured rates replace defaults (R16).

**Before post:** picture locked • only kept takes upscaled, whole takes at 1080p and used seconds plus handles at 4K (R14) • `music_policy` read before any music plan is bought (R24) • no ElevenLabs music in the film (R19) • subscriptions for sound and music booked for the weeks the schedule gives • old subscriptions cancelled only after their last job (credits are lost on cancelling).

---

## 14. Failure modes

| Failure | Sign | Fix |
|---|---|---|
| Costing used seconds instead of clips | Fast sequences look cheap; the bill is two to three times the estimate | E5 clip lengths (P4, R5) |
| LLM arithmetic | Totals in prose that do not match the records | R4; only the validator writes `estimate` |
| Stale prices | Test take costs more than 20% over the table | Recipe 1; E11 blocks money output |
| Runtime creep | Scenes grow at shot design; film 15% over target | E1 and E2 warnings; D2 R10 cuts before generation |
| Takes spiral on one shot | One shot at 12 takes | R12: change method |
| Budget spent before half the shots are kept | 50% spent, 30% kept | R11: budget tier for non-dialogue shots |
| Hours underestimated | Sequence 1 took twice the central case | R16: replace defaults; move the deadline or cut scope (R10, R17) |
| Paying for idle months | Three subscriptions running during compositing | R13; subscriptions only in the weeks the schedule gives |
| Upscaling rejects | Upscale bill is several times the estimate | R14: after picture lock, kept takes only |
| Series drift | Six episodes estimated, none finished | R18: pilot first |
| Free-plan licence | Music or voice made on a free plan used in a public film | R19: commercial-use plans only |
| Licence excludes film | A score made with ElevenLabs music on a self-serve plan; Suno songs used without a permitted download | R19: check `licence_flags` before booking; budget Suno downloads |
| Upscaled files will not relink | The edit cannot find trimmed, upscaled clips | R14 and D8-R20: whole takes at 1080p |
| Wrong estimator | Totals change when nothing in the records changed, or differ from §15.1 on the test inputs | R25: Recipe 0 test before use |

---

## 15. Worked examples

### 15.1 *The Catch*, SC06 FREIGHT CAGE: a scene block, v0 and v1

The scene holds "Another shot sparks off the grid beside her boot.", "Iona hits STOP with her elbow." and "The cage falls." Rhythm class `action_peak` (A4 Worked Example 1).

**v0 (whole scene, words)** [J]: 10 dialogue words in 5 speeches and 513 action words give 92 to 119 s, central 106 s; at an ASL of 2.0, **53 shots**; default shares give about 5 still or graphic, 21 easy, 3 dialogue, 24 hard and 13 plates. Generated seconds: 906 draft + 1,606 final = 2,512 (factor 24). Video money: **$158 budget, $318 mid, $768 premium**; images about $31; about 36 base hours (47 central), led by compositing (about 9 hours), previs (about 9) and post (about 7.5).

**v1 (the fall only, from A4's 36 shots, 49.7 s)** [J]. Classes read from A4's rows: shot 17, the 10 frames of black under the CLACK, is `graphic`; shots 19 to 21 ("Repeats of shots 8, 12 and the grid-and-wall framing; the wall now streams downward") are `reuse` candidates (R6: check that the reversed copies play correctly; if not, they become `easy` and add about $3 each at mid, $9 for all three, plus about 9 minutes each). Shot 19 is the weakest candidate: after the black the grid is above her and she hangs from it, so a reversed copy of shot 8, where bodies lift off the floor, shows the wrong bodies; plan it as a new take and keep 20 and 21 (stripe and wall only) as reuse [J]; shots 13 ("Io.") and 27 ("Push.") are `dialogue`; 14 are `hard` (the dip, the lift, the floating body, the blood macro, the streak, the slipping fingers, the push sideways and the rising cage); 16 are `easy`, including the final 5-second hold on three faces. Two plates: the blood beads (C1 Ex2: generate without blood, composite the beads) and the spark. All clips are 5 s except the final hold (7 s).

- Generated: 464 s draft + 786 s final = **1,250 s for 49.7 s of screen, factor 25**.
- Video money: **$78 budget, $157 mid, $377 premium**.
- Hours: storyboard 16 min, keyframes 128, previs 120 (C4 Example A's three plans, `plan_cage_fall`, `plan_grid_pov` and `plan_inversion_reveal`, at about 30 minutes each, plus the master set), jobs 32, review 242, compositing 90, post share 211: **14 hours base, 18 central, 28 high**.

The lesson: at a 1.4-second ASL, each second of the fall costs about 25 generated seconds, two and a half times the film's average. Rule R5 applies to shots 12 and 15 (A4: shot 15 is "Shot 12's framing; stripe larger"): one continuous point-of-view clip of the stripe approaching, cut in two, halves their takes.

**A small scene as a contrast (SC14, `contemplative`):** "Over her bed, the grey box. The needle lies flat." About 9 s; two shots, both `still_move` from approved keyframes: about $1 in images and 15 minutes before post [J]. In SC15, "The chair is still there." can reuse the clean plate of the room without the bed that the vanish needs ("The bed, and Jude, and the cup, and the figure are gone." is made by hard cut or D6's appear/vanish comp, as C1 Ex5 makes the Figure's arrival), so that shot is `reuse` [J].

### 15.2 *The Catch*, film estimate: three tiers × two runtimes

"Full" is the script as written (v0 central 2,118 s plus 60 s of titles, D2 Option 1). "20 min" is D2's Option 3 (1,160 s plus 40 s). Figures are v0 [J]; LLM months assume 20 hours a week.

| | Full, 2,178 s | 20 min, 1,200 s |
|---|---|---|
| Shots (ASL) | 583 (3.6 s) | 329 (3.5 s) |
| By class: still or graphic / easy / dialogue / hard; plates | 71 / 257 / 147 / 109; 96 | 41 / 149 / 73 / 67; 57 |
| Generated seconds (draft + final; factor) | 20,582 (7,399 + 13,183; 9.7) | 11,496 (4,140 + 7,356; 9.9) |
| Speech credits + effect credits | about 80,000 (38,000 + 42,000; Creator, 1 month) | about 48,000 (Creator, 1 month) |

Money in dollars (video / images / upscaling / voice and effects / music / LLM / editor + 20% contingency = total):

| Tier | Full | 20 min |
|---|---|---|
| Budget | 1,293 / 441 / 65 / 22 / 16 / 140 / 0 + 395 = **2,372** | 722 / 292 / 36 / 22 / 16 / 80 / 0 + 234 = **1,402** |
| Mid | 2,611 / 441 / 65 / 44 / 24 / 140 / 0 + 665 = **3,990** | 1,458 / 292 / 36 / 44 / 24 / 80 / 0 + 387 = **2,321** |
| Premium (4K upscaling, Claude Max, ElevenLabs Pro, Resolve Studio) | 6,302 / 441 / 227 / 198 / 48 / 700 / 295 + 1,642 = **9,853** | 3,517 / 292 / 125 / 198 / 48 / 400 / 295 + 975 = **5,850** |

Budget batches voices and effects into one ElevenLabs month (R13: effects generated in weeks 3 to 4, ahead of the mix); mid and premium book two months, as in §8.2. Music: Suno Pro for two months (budget) or Premier for one (mid) or two (premium). The music line assumes a `scored` film; under D9's default `music_policy: none` for *The Catch*, subtract it (and about 14 hours base at full length, 7.5 at 20 minutes) (R24). Upscaling: budget and mid upscale whole kept takes to 1080p (runtime × 1.5 × $0.02, R14); premium upscales used seconds plus handles to 4K (runtime × 1.3 × $0.08). Not included: lip sync in post (about $90 at full length, §6.5), extra location sheets (about $120, §6.4), other languages (§6.10).

Hours and calendar:

| | Full | 20 min |
|---|---|---|
| Hours: base / central / high | 435 / 565 / 869 | 261 / 339 / 521 |
| Weeks, central, at 10 / 20 / 40 hours a week | 57 / 28 / 14 | 34 / 17 / 8.5 |
| Weeks, high, at 20 hours a week | 43 | 26 |
| Phase hours, central: P0 / P1 / P2 / P3 / P4 / P5 / P6 | 6.5 / 18 / 24 / 67 / 142 / 83 / 224 | 6.5 / 11 / 21 / 45 / 80 / 50 / 126 |

**Reading it.** C1 gave $1,500 to 4,500 for a 20-minute film's generation; this estimate, with every other line added, gives $1,400 to 5,850. D2 scaled C1's figures to $2,600 to 7,900 for the full script; this gives $2,370 to 9,850. The 20-minute cut saves about 40% of money and hours, not the 45% its runtime suggests, because the bible, setup and fixed post work do not shrink. At 20 hours a week the 20-minute film fits the template in §8.2; the full script at 10 hours a week runs over a year (R17: offer D2 Option 2, about 25 minutes). The full script at 2,178 s stays under the Academy's 40-minute short limit and D2 R4's 2,280 s margin, but only if v2 confirms v0: at the page rule's high reference (R22) it would not.

### 15.3 *The Long Places*: the three macro plans

Rhythm mix [J] for this quiet, interior book (D2: McKee's "The purer the novel... the worse the film"; heavy externalization): 35% contemplative, 35% dialogue, 20% mixed, 8% suspense, 2% action peak (the breach in chapter VII). Casts from D2's strands [J]: Plan A 8 main characters, 20 locations; Plan B 12 and 30; Plan C 5 and 6 (bible money by §6.4's scale: $229, $339 and $121). Not included: D17's locale research for a Turkish village and cave setting (§7.1), about 2 to 6 hours for a few locales.

| | Plan A, feature | Plan B, six episodes | Plan C, 15-minute bookend |
|---|---|---|---|
| Runtime | 6,000 s | 17,300 s | 900 s |
| Shots (ASL) | 1,274 (4.6 s) | 3,709 (4.6 s) | 192 (4.6 s) |
| Hard shots; plates | 122; 164 | 354; 477 | 18; 25 |
| Generated seconds (factor) | 41,872 (7.2) | 121,874 (7.2) | 6,295 (7.2) |
| Money: budget / mid / premium | $4,963 / $8,181 / $19,553 | $14,028 / $23,348 / $55,227 | $882 / $1,399 / $3,681 |
| Hours: base / central / high | 932 / 1,211 / 1,863 | 2,620 / 3,406 / 5,240 | 161 / 210 / 323 |
| Weeks, central, at 10 / 20 / 40 h | 121 / 61 / 30 | 341 / 170 / 85 | 21 / 10.5 / 5 |

**Against D2.** D2 put Plan A's video at $3,400 to 21,600 using C1's flat 8× factor at tier prices. This file gives video of $2,627 to 12,756, lower because drafts are costed at $0.05 and a quiet film's generation factor is 7.2, not 8. D2's 100 to 250 review hours compare with 123 base hours of review here.

**Decisions this forces.** Plan B is about 3.3 years at 20 hours a week: R17 and R18 say make episode 1 first. Episode 1 alone (chapters I to II, about 2,883 s, 618 shots) estimates at $2,710 / $4,298 / $10,234 and 630 central hours, about 31 weeks at 20 hours a week [J], with the whole series' bible front-loaded. Plan A is over a year at 20 hours a week (R17 applies). Plan C, at 10.5 weeks and $880 to $3,680, is the only plan that fits a first film.

### 15.4 *The Long Places*, Plan C step 03: a scene block, v1

D2 step 03: "INT./EXT. KIRK ODA - MOUTH - NIGHT", 80 s, "Refrain (18, watch insert); warmth at her right shoulder". The source: "At the mouth of Kırk Oda the air shaft breathed." and "The warmth came against her right shoulder the way a cat commits itself: suddenly, entirely, with weight." A3 Ex5's treatment gives the carriers: the lamp flame leaning out, standing still and leaning in; a watch insert; a frontal locked-off medium shot with empty space at her right shoulder; "She did not turn her head."

Twelve shots [J], 80 s (ASL 6.7): (1) the mouth at night, 7 s, easy; (2) Nilay sits, lamp on her left, 6 s, easy; (3) the watch insert, 4 s, `graphic` with one plate (exact numbers are made as a graphic, C2); (4) the flame leans out, 5 s, hard (timed to the breath); (5) stillness, 6 s, easy; (6) the flame leans in, 5 s, hard; (7) frontal locked-off medium, empty space at her right shoulder, 12 s, easy (14-second clip: Kling 3.0, Seedance 2.5 or Wan 3.0; Veo cannot make it in one clip); (8) her shoulder settles "with weight", 5 s, hard (C1 R12: acted on a phone and transferred); (9) her eyes close, 6 s, easy; (10) the climb out, 8 s, easy; (11) one look back down, 5 s, easy; (12) the dark shaft held, 11 s, `still_move`.

- Clip lengths by §6.2 (used length + 1.5 s, rounded up to a whole second, at least 5): easy clips 9, 8, 8, 14, 8, 10 and 7 s; hard clips 7 s each; the watch plate 6 s.
- Generated: 212 s draft + 345 s final = **557 s (factor 7.0)**. (The first draft of this file rounded clips up to even lengths and got 607 s; the rule in §6.2 governs.)
- Video money: **$35 budget, $69 mid, $166 premium**; images about $6.
- Hours: storyboard 6 min, keyframes 44, phone performance 20, jobs 10, review 77 (including 10 min to make the graphic), compositing 40, post share 340: **9 hours base, 12 central**. No Blender previs is counted: shots 4 and 6 are timing problems solved by prompt beats and shot 8 by phone acting (`previs_level` 4); if the validator's v0 default of 22 minutes per hard shot were applied, add 66 minutes.
- Reuse: D2's series rule makes the refrain a `template_refrain` (one saved setup and sound; only the figure on the watch changes). Step 10's return ("refrain (18)") is at FIRST LIGHT, not night, so the exterior mouth shot (1) must be remade in dawn light from the same saved setup; the lamp-lit interior shots 4, 5 and 6 can be reused if the cave interior reads the same [J]. Three shots at no video cost, one remake, plus the watch graphic.

---

## 16. Conflicts and open questions

- **Keyframes for all shots or some.** C2 costs keyframes for about 120 of 300 shots, the rest staying as storyboard frames; this file assumes nearly every shot becomes video or a still with a move. For an animatic-tier film (R10 step 6), use C2's proportion.
- **Clip lengths.** A4's spec uses Veo's 4, 6 and 8 s; C1 routes many shots to models that accept 3 to 30 s. The validator must read each shot's `model` lengths, not a film-wide default.
- **Single ASL versus rhythm classes.** D2's shot budget uses one film-wide ASL; this file counts per scene. They agree within 10% on the worked examples.
- **D3, D6, D8 and D9 now exist** (they were placeholders when this file was drafted). Taken in: D3's counted characters and lip-sync cost (§6.5), D6's comp times and helper costs (§6.1, §7.1), D8-R20's upscaling unit (§6.7, R14), D9's music policy and the Eleven Music film exclusion (§6.6, R19, R24). Still [J]: post minutes per finished minute (D8 gives no times).
- **D3 takes versus this file.** D3 budgets voices at three takes plus alternates (about 26,000 characters); this file at five tries (about 38,000). Both fit one Creator month; keep five as the budget case until sequence 1's measured tries replace it.
- **D18 characters per word.** D18 §5 Recipe 5 (step 6) uses about 6 characters a word (about 47,000 credits per dubbed language); the counted figure is about 4.9 (7,666 characters for 1,579 words), so about 38,000. D18 should use the count.
- **D8 upscaling factor.** D8 says whole takes are "2 to 3 times" the used seconds; this model's clips are about 1.4 to 1.6 times (5 to 8 s clips around 3.5 to 6 s shots). The validator should sum real `clip_s`, which settles it.
- **D10's `asl_factor` and the word `contemplative`.** D10 multiplies this file's class ASL by a tone factor (R23), and D10 also has a *tone* called `contemplative` (factor 2.5 or more, never under 10 s ASL), which is not this file's `contemplative` *rhythm class* (6 s). A contemplative-tone scene in the contemplative class would run 15 s a shot. The pipeline should rename one of them (suggestion: D13's class becomes `still_pace`) [J; needs the builder's decision].
- **Field names.** This file's `target_duration` is the blueprint's `target_duration_s`; `clip_s` is A4's `clip_length_s`; the blueprint's `stage.py estimate` is the same code as `estimate.py` here. Use the blueprint's names.
- **C2's location count.** C2 budgets *The Catch*'s asset bible with 3 location sheets; the screenplay's headings name about 20 distinct settings (the factory, the quarantine rooms, the ship's rooms, the car, the street, the kitchen). If each gets a sheet, add about $120 and, at 30 minutes a location, about 8.5 hours base [J].
- **Page rule for short scripts.** Follows' data stop at 60 pages; the 60 to 89 page bucket (0.8 pages a minute) would put *The Catch* near 52 minutes, far above every scene-level estimate (32 to 44 minutes). Treat as unresolved until the animatic (v2) measures it (R22).
- **The hours model is untested.** Post (4.25 hours a finished minute) and the novice factor (1.3) are judgments; the one published first-hand account runs slower (§7.3). Measure sequence 1 (R16).
- **Now verified** (this fact-check): credit roll-over (Runway Standard and Pro none, Max one month; ElevenLabs paid plans two months, lost on cancelling; Suno none); Suno's commercial use (downloads only; no copyright warranty); Eleven Music's film exclusion; Topaz Personal's "Limited commercial use".
- **Still unverified:** what Topaz's "Limited commercial use" permits; ElevenLabs sound-effect terms for film; storage prices; whether the reversed copies in SC06 (shots 20 and 21) play correctly (§15.1).
- **For the user:** tier; total budget and spend cap; hours per week; deadline, if any; own voice or synthetic; 4K or 1080p delivery; music policy (D9); for *The Catch*, which D2 option (and whether Academy or festival eligibility matters, D2 R4); for *The Long Places*, Plan C, a pilot of Plan B, or Plan A.

---

## Sources

Web (all checked 2026-09-27):

1. Google, Gemini API pricing (Veo 3.1 Standard, Fast and Lite). https://ai.google.dev/gemini-api/docs/pricing [V]
2. fal, Kling 3.0 Pro image-to-video. https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video [V]
3. fal, Topaz video upscaler. https://fal.ai/models/fal-ai/topaz/upscale/video [V]
4. Runway, pricing. https://runway.com/pricing [V]
5. Topaz Labs, pricing (Topaz Video). https://www.topazlabs.com/pricing [V]
6. ElevenLabs, pricing. https://elevenlabs.io/pricing [V]
7. ElevenLabs, sound effects documentation. https://elevenlabs.io/docs/overview/capabilities/sound-effects [V]
8. Suno, pricing. https://suno.com/pricing [V]
9. Freesound, FAQ (licences). https://freesound.org/help/faq/ [V]
10. Blackmagic Design, DaVinci Resolve Studio. https://www.blackmagicdesign.com/products/davinciresolve/studio [V]
11. Anthropic, Claude pricing. https://claude.com/pricing [V]
12. Stephen Follows, "How many shots are in the average movie?" (3 July 2017; Cinemetrics data, 1997 to 2016). https://stephenfollows.com/p/many-shots-average-movie [V]
13. Stephen Follows, "Is the page-per-minute rule correct?" (30 March 2026; 2,520 US Letter and 351 A4 scripts; ratios by genre, length and paper). https://stephenfollows.com/p/is-the-page-per-minute-rule-correct [V; re-read in this fact-check]
14. fxguide, "Actually using SORA" (*Air Head*, 14 April 2024). https://www.fxguide.com/fxfeatured/actually-using-sora/ [V]
15. Runway, Gen:48 official rules (August 2025 edition). https://runway.com/gen48/terms [V]
16. Suno, Terms of Service (revised 10 August 2026, effective 3 September 2026). https://suno.com/terms [V]
17. ElevenLabs, Eleven Music model-specific terms (26 May 2026). https://elevenlabs.io/eleven-music-model-specific-terms [V]
18. Anthropic, API pricing (Opus 5.5 $4 / $20 per million tokens). https://platform.claude.com/docs/en/about-claude/pricing [V]

Library files: A2 (Step 9 duration defaults); A3 (§5.2 eighths and the line-count page estimate; Ex5 carriers); A4 (§6.1 minimum reading times; Worked Examples 1 and 2, rhythm plans and ASLs; Bordwell's ASLs); C1 (§3A model limits, §10 cost arithmetic and budget rules, rules 1, 6, 8, 12, 13, Recipes 1, 9, 10, Examples 2, 5, 8) and the C1 digest (`shot_need`, `spend_cap_usd`, `kept_take`); C2 (§3.7 costs, Recipes R1 and R2, rule 2, the 10-second pick); C3 (§17A takes, take costs and budget rule 2); C4 (§9 ladder, Recipes 1 to 3, Example A, `previs_level`); C5 (R15, R23, R27, stages and checkpoints, authority marks); D1 (§7.2 LLM costs); D2 (§3.2, §6 runtime of *The Catch*, §7 Option 3 targets, §8 Plans A to C, R4, R9, R10, R17, R18); D3 (§12 voice budget and lip sync); D6 (§7 comp times and helper costs); D8 (R20 upscaling unit); D9 (§2 tools and licences, §4.1 music policy, §5 `cue_budget`); D10 (§2.2 `asl_factor`, §13); D14 (Recipe I5); D17 (Recipes 3, 5, 7); D18 (Recipes 4 to 6); the blueprint (field names, pause tiers, `stage.py estimate`).

Test sources: `/root/.claude/uploads/fbbb0203-69e3-5f8e-b675-32d722ec580d/1edae70d-35_The_Catch_-_workshop_revision_of_Final4.txt` (quoted lines 226, 228, 240, 836, 864, 866); `/root/.claude/uploads/fbbb0203-69e3-5f8e-b675-32d722ec580d/5dcd8176-19_The_Long_Places_-_revised_by_Claude_final.md` (quoted lines 75 and 79). Word counts and all estimates were computed by script on 2026-09-27 [J].
