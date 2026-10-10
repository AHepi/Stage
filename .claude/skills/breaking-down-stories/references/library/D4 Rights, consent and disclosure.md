# D4. Rights, likeness, consent, style imitation, content policy and AI disclosure

Library file D4. Written 2026-09-27; fact-checked the same day (second pass: 30+ sources re-read, corrections to the US public-domain terms, Kling's label duty, the New York advertising exemption, the NO FAKES committee date, YouTube's "AI use" setting, the EU guidelines date and the Freesound credit format; blueprint record names mapped in §6.1). Test sources: *The Catch* (screenplay) and *The Long Places* (prose novella).

> **What this file is for**
> 1. Before any work starts, it decides whether the user may adapt the story at all, and records who owns it and on what terms (stage 0, checkpoint A).
> 2. It keeps real people's faces and voices, other people's characters, brands and artwork out of prompts and references, and plans violent or sensitive moments around model filters without tricks.
> 3. It records the licence behind every generated clip, sound, font and 3D asset, so the film can be shown, sold or entered at festivals.
> 4. It keeps the decision log that shows the human authorship in the film, and keeps the provenance marks that show the AI part.
> 5. It produces the disclosure package (platform labels, festival answers, a standard AI-use credit line), worked through on *The Catch* and *The Long Places*.

**Not legal advice.** This is a production checklist written by an LLM from public sources; laws differ by country and change monthly. For a sold, monetised or client film, or one using a real person or a licensed book, a media lawyer should read the `rights_and_compliance` record before release [J].

**Evidence labels.** [V] = read at the primary source, or two agreeing independent secondary sources; [U] = one secondary source only, or the primary page refused automated reading; [J] = this file's judgment. [S#] = Sources list, all checked 2026-09-27. **Staleness rule:** re-check any law, policy or terms fact older than 30 days before release or a large spend (as C1 §0).

**Place in the pipeline.** D4 adds one record and five gates to C5's stages:

| C5 stage | What D4 adds | Gate |
|---|---|---|
| 0 Intake | `rights_and_compliance` record: who owns the story, the licence, intended use, territories, authorship | **Checkpoint A** (rights confirmed before the scene list is approved) |
| 2 Bible | Likeness basis for every character; name, brand and insignia checks | **Checkpoint B** |
| 5 Shot design | `content_flags` and a `policy_route` per shot | **Checkpoint C** (flag summary per sequence) |
| 8 Generation | Terms snapshot and provenance per job; licence per asset | **Checkpoint E** (clearance check on each kept take) |
| 9 Export | Disclosure package, credit line, licence and attribution list | Release check (§7.5) |

Not repeated here: C1 §4, R9, R10, R19 (filters, violence split, refusals, licensed-data models); C2 R21, §3.6, R6 (open image weights, ShotDeck, insert graphics); C5 R21; A4 §14; D1 §8 (LLM app privacy). Voice cloning practice is D3, style references D5, music licences D9.

---

## 1. Words this file uses (one word per concept)

| Word | Plain meaning |
|---|---|
| **Rights holder** | The person or company that owns the copyright in a story, picture, sound or font. |
| **Adaptation** | Making a new work (here, a film) from an existing one; US law calls it a *derivative work*, and only the rights holder may authorise it [S6]. |
| **Licence** | Written permission to use something someone else owns, on stated terms (media, territory, time, money). Tool and asset terms of use are licences too. |
| **Option** | A paid, time-limited exclusive right to buy a story's film rights later [J]. |
| **Public domain** | Works whose copyright has expired or never existed; anyone may adapt them. |
| **Likeness** | A recognisable face, body or voice of a real person. |
| **Digital replica** | A computer-made copy of a real person's likeness, such as a face swap or a voice clone. |
| **Consent** | A real person's permission to use their likeness or voice. A **consent form** (in film jargon, a "release") is the signed document that records it. In this file, *release* alone means making the film public. |
| **Clearance** | Checking before release that nothing in the film uses someone else's rights without permission [J]. |
| **Trademark** | A registered or used name, logo or design that identifies a company's goods. |
| **Content policy** | A tool's banned subjects. A **filter** enforces it automatically; a **refusal** is one blocked request. |
| **Content flag** | A breakdown tag that marks a shot as touching a sensitive subject (§6). |
| **Open weights** | A model whose files you can download and run yourself; its licence still applies. |
| **Commercial use** | Any use meant to earn money: sales, monetised streaming, paid screenings, client work, adverts [S44]. |
| **Attribution** | The credit a licence requires ("sound by X, licensed CC BY 4.0"). |
| **Provenance** | Machine-readable proof of a file's origin. **Content Credentials** are C2PA's provenance records inside a file [S30]; a **watermark** such as SynthID is an invisible mark in the pixels or sound [S31]. |
| **Disclosure** | Telling viewers that AI was used. A **label** is a platform's own marker (YouTube, TikTok, Meta). |
| **Deep fake** | In EU law: AI-made or AI-altered image, audio or video "that resembles existing persons, objects, places, entities or events and would falsely appear to a person to be authentic or truthful" [S17]. |
| **Authorship evidence** | Records showing which creative choices a human made (C5's log and `decided_by: human` fields). |

---

## 2. Core principles

1. **Permission before craft.** No scene is broken down until the rights status is recorded and confirmed at checkpoint A [J].
2. **Describe, never name.** Prompts describe visible attributes; names of films, directors, cinematographers, living artists, franchises, actors and brands live only in `human_notes` (extends B2 and C5 R21) [J].
3. **Invent every face and voice** unless a living adult has signed a consent form for that exact use; this includes dead historical figures [J].
4. **Plan around filters, never through them.** Split violence (C1 R9), move blood, sparks and gunfire into compositing and sound, stop after two refusals (C1 R10). Tricking a filter breaks the terms and can end the account [S32][S35].
5. **Owning an output is not being free to use it.** A tool gives you its rights, not anyone else's: a frame copying a character, logo or artwork still infringes [S34][S41][J].
6. **Every asset carries its licence**, recorded when it enters the project, not at release [J].
7. **Human authorship is shown, not claimed.** The human-decided breakdown, shot choices, edit and composites are the copyrightable part of an AI film; the log is the evidence [S1][J].
8. **Keep the marks, disclose plainly.** Never strip C2PA or SynthID; use one wording in credits, platform labels and festival forms [J].
9. **Private material stays private.** Upload only what the user owns or may upload, in no-training settings (D1 §8) [J].

---

## 3. What the law, the tools and the platforms say (as of 27 September 2026)

### 3.1 The right to adapt a story

- **Adaptation is the owner's right.** The US Copyright Office lists "motion picture versions of literary material or plays" as derivative works, which only the rights holder may authorise [U, S6]; the UK and EU are the same [J].
- **Public domain, US** (Cornell chart [V, S7]). Works published before 1931 are free. Works published 1931–1963 with a copyright notice are free unless the copyright was renewed; renewed ones run 95 years from publication. Works published 1964–1977 run 95 years from publication. Works created from 1978 on run the author's life plus 70 years (95 years from publication for company-owned works). Works from 1930 entered the public domain on 1 January 2026 [V, S7][S8]; works from 1931 follow on 1 January 2027 [J].
- **Public domain, UK and EU.** UK: written, dramatic and artistic works last "70 years after the author's death"; films "70 years after the death of the director, screenplay author and composer" [V, S57]. EU: the same life plus 70 years (Term Directive) [U]. So a book can be free in the US and still protected in Europe, or the other way round.
- **Traps** [J]: a modern translation, edition, illustration or later character version can be protected when the original is free.
- **Fan works.** "Non-commercial" is not a defence in itself [J]. Some owners publish rules: Star Trek fan films must run "less than 15 minutes for a single self-contained story, or no more than 2 segments … not to exceed 30 minutes total", be shown free, use amateurs who "cannot be compensated", and carry a fixed disclaimer [V, S9].
- **Options, in plain words** [J]. An option is a small payment (the option fee) for the exclusive right, for a fixed period (often 12–18 months, sometimes extendable), to buy the film rights later at a price agreed now (the purchase price). The option agreement also lists the rights granted (film, series, sequels), rights the author keeps (stage, audio, print), credit wording and approvals. For this pipeline the licence or option must also say, in writing: film made with AI tools permitted; which territories; for how long; whether it may earn money. A handshake, a verbal yes or silence is not enough for a public film; an email can serve as written permission only if it names those points.

### 3.2 Who owns AI output, and what copyright covers

- **United States.** The Copyright Office's Part 2 report (29 January 2025): "Copyright does not extend to purely AI-generated material, or material where there is insufficient human control over the expressive elements"; "prompts do not alone provide sufficient control"; humans own "their works of authorship that are perceptible in AI-generated outputs, as well as the creative selection, coordination, or arrangement of material in the outputs, or creative modifications of the outputs" [V, S1][S2]. For films: "a film that includes AI-generated special effects or background artwork is copyrightable, even if the AI effects and artwork separately are not" [V, S1]. Registrations must disclose more than a trivial ("de minimis") amount of AI material and describe the human contribution [V, S1]. The Supreme Court declined *Thaler v. Perlmutter* on 2 March 2026, leaving the human-author rule intact [V, S3].
- **United Kingdom.** Section 9(3) of the Copyright, Designs and Patents Act 1988 still protects "computer-generated" works with no human author. The *Report on Copyright and Artificial Intelligence* (18 March 2026) proposes that "this specific type of protection should be removed, while copyright should continue to protect works created with AI assistance"; the government will first "continue to monitor the use and impact" of that protection, so the law has not changed yet [V, S4].
- **European Union.** EU copyright protects only "original" works, the "expression of free and creative choices reflecting the personality of its author"; the Court of Justice restated this in *Mio/konektra* (4 December 2025, a furniture case, not an AI case) [V, S5]. No EU court has yet ruled on the copyright status of AI output [J]. The first generative-AI copyright case, *Like Company v Google* (C-250/25, about Gemini and press content), was heard by the Grand Chamber on 10 March 2026; an Advocate General's opinion was scheduled for 3 September 2026 and the judgment is pending [U, S5].
- **What this means here** [J]: the screenplay (if human-written), the approved breakdown, shot choices, edit, composites and sound design are human authorship. Single generated clips may be unprotected; the film as a whole remains protected. Keep the log.

### 3.3 Style, characters and brands

- **Style.** Copyright protects expression, not a general style; but naming a film or artist pulls the model toward specific protected frames, characters and designs, and imitating a living artist competes with them [J].
- **Characters and designs.** In February 2026 Disney, Paramount and the Motion Picture Association sent ByteDance cease-and-desist letters over Seedance 2.0 outputs of their characters; ByteDance said it was "taking steps to strengthen current safeguards" against "unauthorised use of intellectual property and likeness" [V, S10]. Disney and Universal's case against Midjourney was consolidated with Warner Bros.' on 4 November 2025 and was in discovery in July 2026, with no trial date [U, S11]. Protected designs are not only characters: costumes, insignia, vehicles, creature designs and signature props are often protected too [J].
- **Model rules, as testers report them.** Seedance 2.0 rejects reference images containing a detectable real human face and refuses prompts that name well-known characters or costumes [U, S60]. OpenAI's Sora app lets a real person's face appear only through that person's own opt-in "cameo" and blocks "third-party likeness" requests [U, S33]. Treat these filters as a floor, not as permission: a prompt that passes a filter can still infringe [J].
- **Brands.** Kling's terms forbid material "which does or may infringe any copyright, trademark or other intellectual property" [V, S34]. A real product in passing is often lawful, but a model-drawn real logo is usually distorted and can suggest endorsement [J]. Invent brands and check the names (Recipe 3).

### 3.4 Faces and voices of real people

| Where | What applies | Status on 2026-09-27 |
|---|---|---|
| Tennessee | ELVIS Act: property right in name, image, likeness and voice, including a voice "simulation" | In force since 1 July 2024 [U, S12] |
| California | AB 1836: no digital replica of a *deceased* personality in an audiovisual work or sound recording without consent; "the greater of ten thousand dollars ($10,000) or the actual damages"; exceptions for news, comment, criticism, satire, parody, documentary or biographical work, and fleeting or incidental use. AB 2602: contract terms allowing replicas without a specific description of the uses are unenforceable | AB 1836 signed 17 Sept 2024, Chapter 258 [V, S13]; AB 2602 [U, S13] |
| New York | (1) Advertisers must "conspicuously disclose" AI "synthetic performers"; $1,000 first violation, $5,000 after. **Exempt:** ads for films, TV, streaming and games where the synthetic performer is used "consistent with its use in the expressive work", and audio-only ads. (2) A second law requires the rights holders' consent for commercial use of a *deceased* performer's digital replica | (1) Signed 11 Dec 2025, in force 9 June 2026 [V, S14][S61]; (2) in force on signing, Dec 2025 [U, S61] |
| US federal | NO FAKES Act of 2026 (S.4591): federal right over digital replicas of voice and visual likeness, lasting after death; exceptions for news, parody, criticism and similar speech; platforms liable if they knowingly host unauthorised replicas | Advanced by the Senate Judiciary Committee by unanimous voice vote on 18 June 2026; not law [V, S15][S62] |
| US federal | TAKE IT DOWN Act: platforms remove non-consensual intimate images, AI "digital forgeries" included, "within 48 hours" of a valid request | FTC enforcement from 19 May 2026 [V, S16] |
| EU | The AI Omnibus (a 2026 law amending the AI Act) bans AI systems generating child sexual abuse material and non-consensual intimate material | Applies from 2 Dec 2026 [V, S19] |
| UK | No general personality right; government will consider "whether it would be beneficial to introduce a new digital replica or personality right" | Under review [V, S4] |
| Denmark | Copyright-style right over one's own face, voice and body | Proposed mid-2025; the European Commission objected in March 2026 that a member state cannot put likeness inside copyright alone; adoption not confirmed on 27 Sept 2026 [U, S21][S58] |
| Unions, awards | SAG-AFTRA 2026 TV/Theatrical contract: builds on the 2023 consent rules for digital replicas and adds limits on "synthetic" performers and on replicas of minors [U, S22]; 99th Oscars acting awards only for roles "demonstrably performed by humans with their consent" [V, S26] | Ratified June 2026 (91.4% yes), effective 1 July 2026 [U, S22]; Oscars rules announced 1 May 2026 |

Tools agree: Google bans "Impersonating an individual (living or dead) without explicit disclosure, in order to deceive" [V, S32]; ElevenLabs bans using its output "to intentionally replicate the voice of another person: without consent or legal right" [V, S38]; OpenAI bans likeness use without consent [U, S33].

**What this means for a fiction film** [J]: the dead are covered too (California, New York and the proposed federal law all reach deceased performers), public figures are the riskiest (they are recognisable and their estates enforce), and minors add a second layer (child-safety rules on top of likeness rules). The only safe default is an invented face and voice.

### 3.5 Disclosure: marks, laws, platforms, festivals

**Marks.** C2PA's latest specification is 2.4 [V, S30]. Gemini checks files for SynthID and Content Credentials (video under 90 seconds); a negative result only means Google AI did not make it [V, S31]. Some re-encoders drop Content Credentials, so keep the original clips [J].

**EU AI Act, Article 50** [V, S17]:
- Providers must mark outputs "in a machine-readable format and detectable as artificially generated or manipulated" (50(2)).
- Deployers of a deep fake "shall disclose that the content has been artificially generated or manipulated" (50(4)); for "evidently artistic, creative, satirical, fictional or analogous" work, only "in an appropriate manner that does not hamper the display or enjoyment of the work".
- A deployer is anyone using an AI system "except where the AI system is used in the course of a personal non-professional activity" (Article 3(4)).
- Dates: the rules apply from 2 August 2026; for generative AI systems placed on the market before 2 August 2026, the 50(2) marking duty has a grace period to 2 December 2026 (AI Omnibus, published in the Official Journal on 24 July 2026) [V, S18][S19]. The Code of Practice on Transparency of AI-generated Content was published in June 2026 [V, S18]; the Commission's Guidelines on Article 50 were published on 20 July 2026 [V, S19] (drafts circulated in May [U, S20]). Deepfakes made before 2 August 2026 need no retroactive label, though one is "encouraged" [V, S18].
- Judgment [J]: invented people in real-looking places may "resemble existing … places, entities or events". Treat every photoreal film as in scope and use the light artistic disclosure: end-credit line, platform label, description.

**Platforms.**
- **YouTube.** Disclose realistic content that is AI-generated or meaningfully altered, including content that "Generates a realistic scene that didn't actually occur"; animation, fantastical scenes, special effects and production help (scripts, captions) are exempt. The switch is in YouTube Studio's upload flow: "In the Attributes section, under 'AI use,' tap **Yes**" (older guides, and earlier library files, call it "altered or synthetic content"). Creators who "consistently choose not to disclose" risk a label applied for them, "removal of content or suspension from the YouTube Partner Program" [V, S23]. Since 27 May 2026 YouTube also labels automatically when "our systems detect significant photorealistic AI use", and labels on content whose C2PA data says it is "fully generative AI" cannot be changed by the creator [V, S23].
- **TikTok.** TikTok has "required creators to label realistic AIGC" (AI-generated content) and reads Content Credentials to "instantly recognize and label AIGC" [V, S24].
- **Meta.** Disclosure is required for "photorealistic video or realistic-sounding audio that was digitally created or altered", with possible penalties [V, S25].

**Festivals and awards.** For the 99th Oscars, acting needs roles "demonstrably performed by humans with their consent", "screenplays must be human-authored to be eligible", and the Academy "reserves the right to request more information about the nature of the use and human authorship" [V, S26]. Cannes (79th festival, announced 9 April 2026) made films in which generative AI drives the script, the pictures or the principal performances ineligible for the Official Competition; restoration and ordinary VFX on shot footage are unaffected [V: two secondary sources, festival text not read, S27][S59]. The Berlinale's 2026 entry form asked "Have you used AI in any way in the making of this?", as research rather than a rule [U, S28]. The shared Nonfiction Core Application used by Sundance's documentary fund added optional AI questions (13 June 2025), including "how do you plan to disclose it to your audience?" [V, S29]. Every call for entries has its own AI clause [J].

**Tool-imposed labels.** Kling: "without our written permission", users must show the "Kling AI" brand on outputs or "prominently indicate that the Output is generated by 'Kling AI'"; paying members get the right to remove the brand watermark and unrestricted commercial use [V, S34]. So the label duty binds free (non-member) outputs; crediting Kling on member outputs is courtesy, not duty [J]. Tencent's HunyuanVideo licence bans placing generated content in public "without expressly and conspicuously identifying that the information and/or content is machine generated" [V, S43].

### 3.6 Content policy by topic (extends C1 §4)

| Topic | Policy evidence | Planning pattern [J] |
|---|---|---|
| Violence, injury | Google bans "Violence or the incitement of violence" but "may make exceptions … based on educational, documentary, scientific, or artistic considerations" [V, S32]; filters do not reliably apply the exception (C1 §4) | C1 R9 split into cause, reaction, aftermath; words for the visible result ("a dark stain spreads") |
| Weapons, gunfire | One tester found weapon plus fast motion plus contact refused (C1 §4) [U] | Weapon partial, soft, never aimed at a person in frame; gunfire in the mix; muzzle flash as composited flicker |
| Blood, gore | "Blood splatter" reported blocked on Kling (C1 §4) [U] | Small composited blood or a stain; no open wounds |
| Sex, nudity | Google bans "Sexually explicit content" [V, S32]; Kling bans "pornographic" material [V, S34]; EU ban on non-consensual intimate material [V, S19] | Imply by cutting away; never a real person or a minor |
| Minors | Google bans content that "Relates to child sexual abuse or exploitation" [V, S32]; Veo and Omni Flash limit minors (C1 §4) | Designed faces; no child-in-danger close-ups |
| Self-harm | Google bans content that "Facilitates self-harm" [V, S32]; so does Kling [V, S34] | Emotion and aftermath, never method |
| Drugs, medicine | Policies target instructions more than depiction [J] | No method detail; watch ambiguous words (§9.2) |
| Hate symbols | Google bans "Hatred or hate speech" [V, S32] | Invent insignia; composite any historical symbol and check the showing country's law [J] |
| Real people, brands, characters | §3.3, §3.4; Kling bans trademark infringement [V, S34] | Designed faces; invented brands as insert graphics; attributes, not names |

**Account risk.** Google bans "Circumvention of abuse protections or safety filters" [V, S32]; Runway may "immediately terminate your license" and forbids re-registering [V, S35]. A lost account takes its clips and credits with it [J]; hence C1 R10's two-refusal stop and D1's `refusals[]` log.

**Open weights are acceptable** [J] when (1) the licence allows your use and country (HunyuanVideo 1.5 excludes the EU, UK and South Korea; Wan 2.2 is Apache 2.0 [V, S43]; LTX and H3 in C1 §3C; image weights in C2 R21), (2) the content would pass a reasonable human censor, and (3) the output is still disclosed. They remove the filter, not the law.

**Per-tool summary** (what each tool's own terms or testers say; ✗ = banned or refused, ~ = limited, blank = not checked). Read with C1 §4, which has the filter observations per model.

| Tool | Real faces or voices | Named characters, brands | Violence, blood | Sexual content | Minors | Label or duty on output |
|---|---|---|---|---|---|---|
| Google (Veo, Imagen, Gemini) | ✗ impersonation to deceive [V, S32] | | ✗ "Violence", exceptions "may" be made for artistic work [V, S32] | ✗ [V, S32] | ✗ abuse; users 18+ [V, S32][S39] | SynthID watermark, detectable by Gemini [V, S31] |
| Kling | | ✗ IP and trademark infringement [V, S34] | ~ "blood splatter" reported blocked (C1 §4) [U] | ✗ "pornographic" [V, S34] | | "Kling AI" label unless member or written permission [V, S34] |
| Seedance 2.0 | ✗ real-face references rejected [U, S60] | ✗ named characters refused [U, S60] | see C1 §4 | | | |
| Runway | | | | | | Bans bypassing "safety or security controls"; licence can end "immediately" [V, S35] |
| OpenAI (Sora, image) | ~ only through the person's own "cameo" [U, S33] | ~ "third-party content" blocked [U, S33] | | | | |
| ElevenLabs (voice) | ✗ without "consent or legal right" [V, S38] | | | ✗ with minors [V, S38] | ✗ material that threatens child safety [V, S38] | Commercial use from Starter ($6/month) [V, S38] |
| HunyuanVideo (open weights) | | | none built in | | | Must identify output as "machine generated"; no EU, UK, South Korea [V, S43] |
| Wan 2.2 (open weights) | | | none built in | | | Apache 2.0; "We claim no rights" over outputs [V, S43] |

### 3.7 Licences for outputs and assets

| Tool or asset | Ownership and commercial use | Duties |
|---|---|---|
| Claude (consumer) | Anthropic assigns "all of our right, title, and interest—if any—in Outputs" [V, S40] | — |
| GLM (Z.ai) | User retains rights in outputs; third-party rights unaffected [U, S41] | — |
| Gemini API, Veo | "Google won't claim ownership", and "may generate the same or similar content for others"; users 18+ [V, S39] | SynthID stays in clips |
| Runway | No ownership claim; "does not restrict your commercial use"; you license inputs and outputs to Runway, including for training [V, S35] | — |
| Kling | Users own output IP; non-members need written permission for commercial use; members' commercial use "is not restricted" [V, S34] | "Kling AI" label on non-member outputs; members may remove the watermark [V, S34] |
| Luma | Free and Lite: "personal use only", permanent watermark, used for training; Plus and up: commercial, no watermark, no training [V, S36] | — |
| Midjourney | Companies over $1 million a year need Pro or Mega to own outputs [U, S37] | — |
| ElevenLabs | Free plan has no commercial licence; Starter ($6/month) does [V, S38] | Voice consent |
| Adobe Firefly, Marey | Trained on licensed (and, for Firefly, public-domain) material; Firefly enterprise indemnity (a promise to cover intellectual-property claims) [U, S42][S55] | — |
| Creative Commons | CC0 no conditions; BY credit; SA same licence for your version; NC non-commercial only; ND no changes [V, S44] | Credit per file |
| Freesound | CC0, CC BY, CC BY-NC or the retired Sampling+; Freesound's example credit: *This [video] uses these sounds from freesound: "[sound name]" by [user] ( http://freesound.org/s/[sound ID]/ ) licensed under [licence]*; a long list may go on a linked credits page [V, S45] | Check each file (A4 §14) |
| Fonts (OFL) | Allowed for "video titling"; "You remain the author and copyright holder" of the graphic; credit is "not required" [V, S46] | Commercial fonts: read the video clause [J] |
| Mixamo | Royalty-free for films, commercial included, no credit needed; no redistributing raw character or animation files [U, S47] | — |
| MPFB (MakeHuman) | Core assets (base mesh, targets, skins) CC0, so characters made from them may be sold; "if you use a third party asset shared under a different license it is your responsibility to fulfill the obligations of that license" [V, S48]. The add-on's code is under a software licence that does not reach exported characters [U] | Third-party assets keep their licences |

### 3.8 Privacy of manuscripts and reference photos

D1 §8 covers the LLM apps. Generation services add three risks:
- **Public file addresses.** fal serves uploads and outputs as CDN URLs (addresses on a content delivery network, which anyone with the link can open); request payloads are kept 30 days by default; retention can be shortened; and "CDN files found in the **input** of a request are not deleted" [V, S49].
- **Training on uploads.** Runway licenses inputs and outputs for training [V, S35]; Luma trains on Free and Lite content [V, S36]; Google's unpaid API tier says "Do not submit sensitive, confidential, or personal information" [V, S39]; the Gemini app warns against entering "confidential information that you wouldn't want a reviewer to see" [V, S50].
- **Other people's material** [J]: another person's unpublished manuscript or photo needs permission to upload. Photos also carry hidden location data (EXIF metadata).

---

## 4. Decision rules

1. **If** the user did not write the story and it is not public domain, **then** ask for a licence or written permission covering a film made with AI tools; without one, either stop or (the blueprint's route) continue as `study_only`: private study, every export marked "Private study, not for publication", no public-release generation packs, no upload of the text to tools that train on it, **because** adaptation is the rights holder's exclusive right [S6] and even a private adaptation is a copy; the risk is low only while nothing is shared [J].
2. **If** the user says the film is "just for fun", **then** record `fan_noncommercial` and follow the owner's published fan rules exactly, or keep it private, **because** non-commercial use is no defence in itself [J][S9].
3. **If** the source is claimed to be public domain, **then** check every showing country and the exact edition or translation, **because** US and UK/EU terms differ and modern translations can be protected [S7][J].
4. **If** the source was written wholly or mostly by an AI model, **then** record `authorship_mode` and the revision history, and warn that copyright in the text may be thin, **because** purely AI-generated material is unprotected in the US [S1] and the UK plans the same [S4].
5. **If** a prompt or reference would name a film, director, cinematographer, living artist, franchise, actor or brand, **then** rewrite it as visible attributes and keep the name in `human_notes`, **because** names pull models toward protected material and trigger filters [S10][J].
6. **If** a take resembles a protected character, logo, costume or artwork, **then** reject it at checkpoint E, **because** tool terms give you only the tool's rights, never a third party's [S34][S41].
7. **If** a character would be based on a real person, living or dead, **then** design an invented face; use a real adult only with a signed consent form, never a celebrity, **because** likeness laws cover the living and, in California and New York, the dead [S12][S13][S61], a federal right is advancing [S15], and every major tool restricts it [S32][S38].
8. **If** a character is a child, **then** design the face, never upload a real child's photo, and keep the child out of sexual or graphic violent content, **because** every policy bans it and several tools refuse minors outright (C1 §4) [S32].
9. **If** the user wants to use their own face or voice, **then** record `self_consented` with the date and keep the source files private, **because** it creates a biometric asset (a body or voice record that identifies a person) others could misuse [J].
10. **If** a shot touches any topic in §3.6, **then** set `content_flags` and a `policy_route` at shot design, **because** planning composites is cheaper than paying for refused takes [J].
11. **If** a model refuses the same request twice, **then** stop, reroute (composite, sound, restaging or open weights) and log it; never add jailbreak wording, **because** circumvention is itself banned [S32] and can end the account for good [S35].
12. **If** open weights are considered, **then** check territory, revenue and commercial terms first, keep the content non-graphic, and still disclose, **because** the licence travels with the model (HunyuanVideo excludes the EU, UK and South Korea) [S43].
13. **If** the film will be sold, monetised, shown at festivals or made for a client, **then** generate every kept asset on a plan allowing commercial use, **because** the free tiers of Kling, Luma and ElevenLabs are non-commercial [S34][S36][S38], and Luma's free-tier watermark stays even after upgrading [S36].
14. **If** a kept Kling clip was made on a free (non-member) account, **then** keep the "Kling AI" mark or state "generated by Kling AI" in the credits; **if** it was made on a paid membership, **then** credit Kling in the tool list as for any tool, **because** the label duty applies "without our written permission" and members may remove the watermark [S34] (and a commercial film needs member clips anyway, rule 13).
15. **If** a sound, music cue or image comes from a library, **then** record its licence per file, and reject NC files for commercial projects and ND files you will edit, **because** NC forbids commercial use and ND forbids changes [S44][S45].
16. **If** a font appears in an insert graphic, **then** prefer an OFL font and record it, **because** OFL allows video titling without credit [S46] while commercial font licences vary [J].
17. **If** a character, company, product or place name is invented, **then** run Recipe 3's name check at checkpoint B, **because** an exact match with a real person or brand invites defamation or trademark complaints [J].
18. **If** an invented brand, label or sign must be readable, **then** make it an insert graphic (C2 R6), **because** models redraw text each time and sometimes copy real logos [J].
19. **If** a real institution would be identifiable (a named hospital, police force or air force), **then** invent its name, crest and livery, **because** real institutions in invented events invite complaints and official insignia are often restricted [J].
20. **If** the film has photoreal AI pictures or voices, **then** keep provenance, add the credit line (Recipe 6) and set every platform's AI label, **because** YouTube (Studio, Attributes, "AI use": Yes), TikTok and Meta require it [S23][S24][S25] and EU Article 50 requires deep-fake disclosure [S17].
21. **If** the film is shown in the EU by someone acting professionally, **then** use the artistic-work form (end-credit line, description, marks intact), **because** Article 50(4) asks for disclosure "that does not hamper the display or enjoyment of the work" [S17].
22. **If** the film is entered for a festival or award, **then** read that call's AI rules and answer every AI question fully, **because** rules differ (Oscars: human-authored screenplay, human acting [S26]; Cannes: generative films out of the Official Competition [S27][S59]) and late discovery can mean disqualification [J].
23. **If** an advert shown in New York contains AI-made people, **then** add a conspicuous synthetic-performer disclosure, unless it is a trailer or promo for the film that shows those people as they appear in the film (and audio-only ads are exempt), **because** New York law requires the notice from 9 June 2026 but exempts ads for expressive works where the use is "consistent with its use in the expressive work" [S14][S61]. A trailer with new, made-for-the-ad AI people, or client advertising work, needs the notice.
24. **If** a manuscript is someone else's and unpublished, **then** get written permission before uploading it, in D1 §8's no-training settings, **because** uploads may be kept, reviewed or trained on [S39][S50].
25. **If** a reference image goes to an aggregator, **then** upload only invented or owned images, location data removed, with the shortest retention, **because** input files become CDN addresses that are not auto-deleted [S49].
26. **If** you register the film's copyright in the US, **then** disclose the AI material and describe the human contribution from the log, **because** the Copyright Office requires it [S1].
27. **If** the release is commercial, or involves a licensed book, a real person or a union performer, **then** set `counsel_review: recommended` and hold release until the user confirms, **because** this file cannot replace a lawyer [J].
28. **If** a book licence is silent on AI tools, **then** ask the rights holder to confirm AI-assisted production in writing, **because** silence invites a later dispute [J].
29. **If** any law, policy or terms fact in the record is older than 30 days at release, **then** re-check it, **because** the rules in §3 changed repeatedly during 2026 [S15][S19][S23].
30. **If** the source text or the screenplay was written or revised by an AI model (as *The Long Places* was, and as every LLM-drafted adaptation here is), **then** say so in the credit line and festival answers, and do not enter it for awards that require a human-authored screenplay, **because** the 99th Oscars rules state "screenplays must be human-authored to be eligible" [S26] and an undisclosed AI source is the kind of late discovery rule 22 warns about [J].

---

## 5. Recipes (an LLM does the work; the user answers and approves)

### Recipe 1: Rights intake (stage 0, before checkpoint A, about 10 minutes)

1. Paste to the LLM: *"Before breaking down this story, interview me for D4's rights record, one question at a time: who wrote it; whether any AI wrote or revised it; who owns it; whether it is published; what licence, option or permission I hold and what it covers (film, AI tools, territories, end date); where the film will be shown; whether it will earn money; whether it quotes other works. Then fill `rights_and_compliance` and list blockers."*
2. Answer in plain words. The LLM records the licence file's name, not its contents.
3. The LLM applies rules 1–4 and 28 and prints one line: `rights_status`, `commercial_project`, blockers.
4. At checkpoint A (for prose, before D2's checkpoint M), approve only if `rights_status` is not `unknown` or `blocked`. In the built pipeline this is the blueprint's single rights question (CHOICE-001, PROJECT `rights`: `mine` | `permission` | `public_domain` | `study_only` | `unknown`); map D4's finer values with §6.1.
5. If the answer is "not mine, no permission", set `study_only` (rule 1): the work may continue privately, but every export carries "Private study, not for publication".

### Recipe 2: Public-domain check (15 minutes per source)

1. Ask the LLM: *"Find this text's first publication year and country, the author's death year (and the translator's or illustrator's, if the edition has one), and the exact edition or translation I hold. Apply the Cornell chart for the US (published before 1931: free; 1931–1963: free unless renewed; 1964–1977: 95 years from publication; 1978 on: life plus 70) and life plus 70 for the UK and EU. List every assumption and every source."*
2. Open its sources and confirm the years yourself; for a US work published 1931–1963, ask the LLM to search renewal records (the US Copyright Office's online public records, or a renewal database for books) and show you the result [J].
3. Decide per country with this table [J]: US free and UK/EU free → `public_domain`; US free but UK/EU protected (or the reverse) → `public_domain` only for the free territories, and set `release_territories[]` to match; any doubt → `unknown`.
4. Record `public_domain_evidence`. If you hold a modern translation, find a public-domain one (often a pre-1931 translation) or license the modern one.

### Recipe 3: Clearance pass at the bible (stage 2, before checkpoint B, 20–40 minutes)

1. Ask the LLM: *"List every proper name in the bible (characters, companies, products, institutions, places), every readable text, logo, crest, livery, patch and artwork; mark each invented or real."*
2. For invented names: search the web in quotes, then the USPTO, EUIPO TMview and UK IPO registers [S52]. Record `clear`, `coincidence_low_risk` (same name, unrelated field) or `conflict` (same or similar name in a related field, or a real person in a similar role).
3. Real institutions: keep the place, invent the name and insignia (rule 19).
4. Set every character's `likeness_basis`; anything but `invented` needs a consent form.
5. Show the table at checkpoint B with renames proposed for every `conflict`.

### Recipe 4: An original face, and a real person's consent

1. Write the identity key from the script and B5; no actor names, no "looks like" (C5 R21).
2. Generate candidate faces from text only, no photo references; pick one; build the turnaround (C2).
3. Lookalike check: ask the LLM *"Does this face strongly resemble any well-known person?"* and regenerate on a confident match [J]; add a human glance, since the LLM can be wrong either way.
4. Derive older or younger versions from the approved face with an edit model, never from a real photo.
5. If a real adult performs (the user, a friend), get a one-page consent form signed before any upload: project, uses (LoRA training, a small add-on model taught one face; voice clone; performance transfer), territories, term, how to withdraw. Store it outside the AI tools; record only its file name.

### Recipe 5: Content-flag pass at shot design (stage 5, per scene)

1. Ask the LLM: *"For each shot, set `content_flags` from D4 §6's list and a `policy_route`. Rewrite any prompt words that name injury, weapons fire, blood, drugs or real people into visible, neutral description. Move gunfire into `sound_mix_elements`, and blood, sparks and flashes into `composite_elements` (C1 §6)."*
2. At checkpoint C, read the one-line flag summary per sequence and approve or change routes.
3. During generation, log every refusal (D1 `refusals[]`). After two refusals of one request, switch route; never reword a third time.

### Recipe 6: Licence log and disclosure package

1. Per generation job, the script copies `model_terms` from a per-tool table the user re-checks monthly.
2. Per imported asset (sound, font, 3D, stock), the LLM fills `asset_licence` from the download page.
3. At export, the LLM builds:
   - **Credit line** (template): *"Made with generative AI. Written by [writer]. Directed, designed and edited by [human names], who chose and approved every shot. Images and video generated with [tools]; voices with [tool]; sound effects from [libraries]. No real person's face or voice was used without consent. Content Credentials are kept where the tools provide them."* Add "Generated with Kling AI" if rule 14 applies, and list the attributions rule 15 requires.
   - **Honesty check on the credit** [J]: "designed" is true only for what a human designed. In this pipeline the LLM drafts shot plans and a human approves them, so if the user did not redesign the shots, write "Directed and edited by [names], who chose and approved every shot planned with an AI assistant." Overstating human work is the misstatement festivals and the Copyright Office (rule 26) care about.
   - **Credit line, AI-written source** (template, replaces the second sentence when `authorship_mode` is not `human_written`): *"Based on [title], a [novella / screenplay] generated with [model] and revised with [model] under the direction of [human names]."*
   - **Platform settings**: YouTube Studio upload, Attributes section, "AI use" = **Yes** for photoreal films (animation-only films may answer No, but Yes costs nothing); TikTok: turn on the AI-generated content label when posting; Meta (Facebook, Instagram): use the AI disclosure ("AI info") label tool when posting [J on menu names; S23–S25 for the duty].
   - **Description text**: the credit line's first two sentences.
   - **Festival answer** (template): *"Generative AI tools ([tools]) made the pictures[, voices] and [other]. [Writer / 'An AI model, directed by [names],'] wrote the [screenplay / source]. Humans [designed / approved or changed] every shot [an AI assistant planned], selected all takes, and did the edit, compositing and sound. No real person's face or voice was used without consent. A log of [n] recorded human decisions is available on request."* Answer each form question separately with the relevant sentence; never answer "no AI" to a narrow question (for example "AI in the script?") without checking `authorship_mode`.
4. Check the master for SynthID and Content Credentials (S31); record the result.

### Recipe 7: Authorship evidence pack (at release, 10 minutes)

1. Ask the LLM: *"From the log, every answered CHOICE record and all fields with `decided_by: human` (authority `user`), list the human creative decisions (story changes, design theses, shot lists, selected takes, edits, composites, sound), count them per stage, and quote three with record IDs."*
2. Save it with the source hashes (C5 `manifest.json`) as `authorship_evidence.md`, for registration (rule 26), festivals and disputes.

---

## 6. Fields this subject adds to the breakdown

Enums are lowercase `snake_case`; empty is `"none"`. Authority follows C5: **A** = authored by a human (`decided_by: human`), **L** = drafted by the LLM for human approval, **D** = derived by script.

| Level | Field | Meaning | Allowed values |
|---|---|---|---|
| film | `rights_and_compliance` | Holds the film fields below | object |
| film | `rights_status` (A) | Right to adapt the source | `own_original` \| `public_domain` \| `licensed` \| `option_held` \| `written_permission` \| `fan_noncommercial` \| `study_only` \| `unknown` \| `blocked` |
| film | `rights_holder` (A) | Owner's name as the user gives it; stored locally only | text |
| film | `licence_ref`, `licence_scope` (A) | Licence file name; what it covers | file name; object: `media`, `ai_tools_permitted` (`yes` \| `no` \| `silent`), `territories[]`, `term_end`, `commercial` (`yes` \| `no`) |
| film | `underlying_works[]` (L) | Quoted songs, poems, translations, artworks | objects: `title`, `status` (as `rights_status`), `evidence` |
| film | `public_domain_evidence` (L) | Proof for Recipe 2 | object: `first_published`, `country`, `author_death_year`, `edition`, `jurisdictions_checked[]` |
| film | `authorship_mode` (A) | How the source text was written | `human_written` \| `ai_assisted` \| `ai_generated_human_directed` \| `ai_generated` \| `unknown` |
| film | `source_versions[]` (L) | Revision history of the source | objects: `version_id`, `label`, `made_by` (`human` \| model name \| `unknown`), `human_role`, `file_hash` |
| film | `intended_use` (A) | Where the film goes | `personal` \| `festival` \| `online_free` \| `online_monetised` \| `commercial_sale` \| `client_work` |
| film | `release_territories[]` (A) | Countries or blocs | e.g. `us`, `eu`, `uk` |
| film | `commercial_project` (D) | From `intended_use` | `yes` \| `no` |
| film | `counsel_review` (A) | Lawyer involvement | `not_needed` \| `recommended` \| `done` |
| film | `disclosure_plan` (L) | Credit line, platform labels, festival answers | object: `credit_line`, `platform_labels{}`, `festival_answers[]`, `eu_article50` (`in_scope` \| `out_of_scope`) |
| film | `facts_checked_on` (D) | Date of the last §3 re-check | ISO date |
| character | `likeness_basis` (A) | Where the face and voice come from | `invented` \| `self_consented` \| `performer_consented` \| `blocked_real_person` |
| character | `consent_record` (A) | Pointer to the consent form | RIGHTS record ID `RT-` + 3 digits (the RIGHTS record holds the form's file name, kept offline) \| `none` |
| character, prop, location | `name_check` (L) | Recipe 3 result | object: `searched_on`, `registers[]`, `result` (`clear` \| `coincidence_low_risk` \| `conflict`), `note` |
| prop, graphic | `trademark_risk` (L) | Real or similar marks in frame | `none` \| `invented_checked` \| `real_incidental` \| `real_needs_clearance` |
| shot | `content_flags[]` (L) | Sensitive topics | `violence_implied` \| `violence_onscreen` \| `weapon_visible` \| `gunfire` \| `blood_small` \| `gore` \| `nudity` \| `sexual_content` \| `minor_present` \| `self_harm` \| `drug_use` \| `hate_symbol` \| `real_person` \| `real_brand` \| `real_institution` \| `fire` \| `none` |
| shot | `policy_route` (L, approved at C) | How the flagged content is made | `as_written` \| `restated` \| `split_cause_reaction_aftermath` \| `composite_element` \| `sound_only` \| `open_weights` \| `cut` |
| shot | `human_notes` (A) | Where film, artist or brand names may live; never compiled into prompts | text |
| generation job | `model_terms` (D) | Terms snapshot at generation | object: `plan_tier`, `commercial_ok` (`yes` \| `no` \| `check`), `label_required` (text \| `none`), `terms_url`, `checked_on` |
| generation job | `provenance` (D) | Marks found on the output | object: `c2pa` (`present` \| `absent` \| `unknown`), `synthid` (`present` \| `absent` \| `unknown`), `visible_watermark` (`yes` \| `no`) |
| generation job | `inputs_personal_data` (L) | Real person's image or voice in inputs | `none` \| `self_consented` \| `performer_consented` |
| asset (sound, music, font, 3D, stock) | `asset_licence` (L) | Licence per file | object: `source` (`generated` \| `library` \| `original` \| `public_domain`), `provider`, `licence_id` (`cc0` \| `cc_by_4_0` \| `cc_by_sa_4_0` \| `cc_by_nc_4_0` \| `ofl_1_1` \| `apache_2_0` \| `provider_terms` \| `other`), `attribution_text`, `commercial_ok`, `url`, `obtained_on` |

**New validator checks** (numbered after D1's): **D4-V17** no compiled prompt contains a name listed in any `human_notes` or in a banned-names list (films, artists, actors, brands); **D4-V18** every kept take has `model_terms.commercial_ok: yes` when `commercial_project: yes`; **D4-V19** every character has `likeness_basis`, and any value other than `invented` has a `consent_record`; **D4-V20** every asset has `asset_licence`, with no `cc_by_nc_*` in a commercial project; **D4-V21** every `content_flags` value other than `none` has a `policy_route`.

### 6.1 Mapping to the design blueprint's records

The blueprint (`design/blueprint.md`) already turned this file into records, sometimes with other names. Where they differ, **the blueprint's names win** for the built pipeline; this file's extra values are proposals to add [J].

| This file | Blueprint | Action |
|---|---|---|
| `rights_status`: `own_original` | PROJECT `rights`: `mine` | Use `mine` |
| `licensed`, `option_held`, `written_permission` | `permission` | Use `permission`; keep the finer value in the RIGHTS record's `status` text |
| `public_domain` | `public_domain` | Same |
| `fan_noncommercial` | `study_only` (closest) | Propose adding `fan_noncommercial`, or record it as `study_only` with the owner's fan rules in `evidence` |
| `unknown`, `blocked` | `unknown`; `study_only` | `blocked` = `study_only` or stop |
| `licence_ref`, `licence_scope`, `underlying_works[]`, music, font and stock `asset_licence` | RIGHTS records (`subject`: source \| voice \| likeness \| music \| font \| stock \| model_terms; `status`, `holder`, `licence`, `evidence`, `commercial_ok`, `attribution`, `disclosure`) | One RIGHTS record per item, ID `RT-001` etc.; this file's object fields become the record's text parts |
| `consent_record` (file name) | CHARACTER `consent` = RT id; VOICE `consent` = RT id (D3) | Use `RT-` IDs |
| `likeness_basis` | CHARACTER `likeness_basis`: `invented` \| `self_consented` \| `performer_consented` | Same; `blocked_real_person` is a proposal (else the character is simply not approved at B) |
| `content_flags[]` | Shot `content_flags` (no `sexual_content`, `hate_symbol`, `real_institution`) | Propose adding the three; until then write them in the shot's `policy_route` note |
| `policy_route` | Same name | Same |
| `disclosure_plan` | `22 Rights and credits.md` disclosure line; FINISH disclosure text | Same content, blueprint location |
| `decided_by: human` as authorship evidence (Recipe 7) | Fields with authority `user`, set only through answered CHOICE records | Recipe 7 counts CHOICE records and `user`-authority fields |
| `human_notes` | Not in the blueprint list; D5 uses film-level `style_human_notes` | Propose a shot- and bible-level `human_notes`; D4-V17 scans both |

---

## 7. Checklists

### 7.1 Checkpoint A (intake)
- [ ] `rights_status` set and not `unknown` or `blocked` (or `study_only`, with the private-study mark on every export); licence file stored if needed.
- [ ] `licence_scope.ai_tools_permitted` is `yes`, or the rights holder has confirmed in writing (rule 28).
- [ ] `authorship_mode` and `source_versions[]` recorded.
- [ ] `intended_use`, `release_territories[]` and `commercial_project` set.
- [ ] D1 `training_optout: confirmed` before the full text is uploaded.

### 7.2 Checkpoint B (bible)
- [ ] Every character `likeness_basis` set; consent forms on file for any non-invented one.
- [ ] Name check table done; every `conflict` renamed or accepted in writing.
- [ ] No identity key names a real person; no reference image shows one.
- [ ] Invented brands, labels and insignia have insert-graphic specs with licensed fonts.
- [ ] Style notes use attributes; names live only in `human_notes`.

### 7.3 Checkpoint C (shot lists)
- [ ] Every flagged shot has a `policy_route`; violence shots are split per C1 R9.
- [ ] Gunfire, blood and sparks are in `sound_mix_elements` or `composite_elements`.
- [ ] No shot needs a minor in a flagged topic.

### 7.4 Checkpoint E (takes)
- [ ] No recognisable real person, logo, protected character or artwork in the take.
- [ ] The job's plan allows commercial use if needed; required labels noted.
- [ ] Provenance recorded; no mark removed or cropped deliberately.
- [ ] No take came from a jailbreak prompt or a third attempt after two refusals.

### 7.5 Release (stage 9)
- [ ] Facts in §3 re-checked if older than 30 days (rule 29).
- [ ] Credit line, attributions and "Kling AI" line (if needed) in end credits.
- [ ] Platform AI labels set; description text added.
- [ ] Festival forms answered from the disclosure plan; authorship evidence pack saved.
- [ ] `counsel_review` is `done` for any commercial release.

---

## 8. Failure modes and fixes

| Failure | Cause | Fix |
|---|---|---|
| Author objects after the film is made | Rights not checked at intake | Recipe 1; checkpoint A gate |
| A character looks like a famous actor | "Looks like" wording, photo reference, model bias | Identity key only; lookalike check |
| Model copies a franchise character | Film or franchise name in the prompt | D4-V17 blocks names; attributes only |
| Account suspended mid-project | Rewording around a filter | Two-refusal stop; local copies of kept clips |
| Free-tier take in a commercial film | Plan not recorded per job | `model_terms` per job; D4-V18 |
| Library sound turns out NC | Licence not recorded at import | `asset_licence` at import; D4-V20 |
| Invented brand is a real company | No name check | Recipe 3 at checkpoint B |
| Festival disqualifies after selection | AI use not disclosed or rules not read | Recipe 6 festival answer; rule 22 |
| Content Credentials lost | Re-encoder stripped them | Keep original clips; record provenance |
| Friend's photo on a public CDN address | Real reference uploaded to an aggregator | Invented references only; short retention (rule 25) |

---

## 9. Worked examples

### 9.1 *The Catch*: the rights record at intake

The title page reads "= An original short screenplay" (l.3) and "= Workshop revision — 25 September 2026" (l.6). "Original" means not adapted from another work; it does not say who wrote or revised it. Until the user answers, the record reads:

```
rights_and_compliance:
  rights_status: unknown            # user to confirm own_original
  rights_holder: none              # to ask
  authorship_mode: unknown          # ask: who wrote Final4; who ran the workshop revision; any AI?
  underlying_works: none            # a search for songs, poems and lyrics found none
  intended_use: none               # to ask
  release_territories: []           # to ask
  counsel_review: not_needed        # becomes recommended if commercial_sale
```

List any workshop or AI contributions in `source_versions[]`: they matter for the Oscars' screenplay rule [S26] and copyright (§3.2). In the built pipeline the same state is PROJECT `rights: unknown` until CHOICE-001 is answered; "It's mine" sets `mine` (§6.1). If the workshop revision was made with an LLM, `authorship_mode` becomes `ai_assisted` and rule 30 applies to award entries.

### 9.2 SC06: the gunshot and the floating blood

The script: "Far above, the stair door gives with a crash. Someone KICKS the top gate open and FIRES down through the roof." (l.216); "He sits down into Eli with a hole through his shoulder." (l.222); "Another shot sparks off the grid beside her boot." (l.226); "Jude's blood lifts off the steel in round red beads and hangs in the air between them, turning." (l.244).

| Moment | `content_flags` | `policy_route` | Prompt wording (visible result) | Moved out of the model |
|---|---|---|---|---|
| Gate kicked, shots (l.216) | `gunfire`, `violence_implied` | `split_cause_reaction_aftermath` | "A bright flicker through the roof grid; the three look up" | Gunfire, crash to `sound_mix_elements`; flicker composited |
| Jude hit (l.222) | `violence_implied`, `blood_small` | `split_cause_reaction_aftermath` | "He sits down heavily against Eli, a dark stain spreading on his shoulder" (C1 §4 wording) | No wound entering; the hole is never shown |
| Spark at her boot (l.226) | `gunfire` | `composite_element` | "She flinches; her boot jerks back on the grid" | Sparks composited; ricochet in the mix |
| Blood beads (l.244) | `blood_small` | `composite_element` | Plate: "the cage interior falling, two figures floating" | 20–30 beads simulated in Blender and composited (C1 Ex2) |

Two more checks. The guard's "pistol half drawn" (l.183) and "The pistol skids away." (l.185) get `weapon_visible`: partial, never pointed at a person in frame. SC11's "a grey box with a needle in it. The needle lies flat." (l.498) is a gauge, not a syringe; write "a grey meter, its pointer lying flat at zero" so no filter reads it as a drug needle [J].

### 9.3 Nell's photograph

"Saye opens a file. The same woman, much younger. A flight suit. Unsmiling." (l.988), then "NELL ROWAN. FLIGHT TEST." (l.990), and later "Saye glances towards the photograph of Nell on the desk." (l.1016). A real archive photo of a woman test pilot would be a real person's likeness (rule 7). Instead:
1. Design Nell at sixty from the script ("Sixty, perhaps. She looks older.", l.1135) with an identity key and turnaround (Recipe 4); `likeness_basis: invented`.
2. Derive the photograph with an edit model: the same face about nineteen years younger ("The date is nineteen years old.", l.998), flight suit, flat light, print grain.
3. Invent the flight-suit patch: no real air force roundel or space agency emblem (rule 19).
4. Make "NELL ROWAN. FLIGHT TEST." an insert graphic with an OFL typeface (rule 16, C2 R6).
5. Name check: a web search found no well-known "Nell Rowan" [U, S56]; record the result after the registers.

### 9.4 The OSTREL blanket, the IONA VALE wristband and the police lights

- **OSTREL** ("OSTREL, stitched on it in blue. Backwards.", l.496) is an invented linen brand. A web search found no exact match; a similar US mark, OSTRIL, is reported for household utensils [U, S53]: `coincidence_low_risk` pending Recipe 3's registers. Make it a mirrored insert graphic (C2 R6) and record the font's licence.
- **IONA VALE** ("Her own name, printed backwards.", l.500; "a label. Her name, copied from a hospital wristband stroke for stroke" and "IONA VALE.", l.1231–1233). "Iona Vale" is used as an author name for colouring books and journals [U, S54]: unrelated field, sympathetic character, so `coincidence_low_risk`, for the user to accept or rename at checkpoint B. The wristband carries no real hospital's name or logo; if the locale becomes the UK, no NHS logo (rule 19) [J].
- **Police lights** ("Police lights beyond frosted windows.", l.492 and l.1004) show only coloured light through frosted glass; no livery is readable, so `real_institution` is not set. If a later design shows a car, invent markings and force name once the locale is chosen [J].

### 9.5 A festival-ready disclosure for *The Catch*

Assuming photoreal style, a human writer, paid Seedance and Kling plans, designed voices and Freesound effects:
- **End credit:** "Made with generative AI. Written by [writer]. Directed, designed and edited by [director], who chose and approved every shot. Images and video generated with Seedance 2.x and Kling 3.0 (Kling AI; members' clips need no watermark, rule 14); voices designed with [tool]; sound effects from freesound.org (each CC BY sound credited in Freesound's format [S45]). No real person's face or voice was used. Content Credentials are kept where the tools provide them."
- **Festival form:** "Generative AI made the pictures and voices, and an AI assistant drafted the shot plans. Humans wrote the screenplay, approved or changed every planned shot, selected all takes, and did the edit, compositing and sound; a log of [n] recorded human decisions is available." Skip competitions that bar generative films (Cannes Official Competition [S27][S59]); no Oscar acting eligibility [S26].
- **Online:** YouTube Studio, Attributes, "AI use" = Yes, since the film shows "a realistic scene that didn't actually occur" [S23]; TikTok and Meta labels on [S24][S25]. Expect YouTube to label it anyway: C2PA data marking clips "fully generative AI" makes the label permanent [S23].
- **Trailer:** a trailer cut from the film's own shots is exempt from New York's synthetic-performer notice; a trailer with new AI people is not (rule 23) [S61].
- **EU:** `eu_article50: in_scope`; the end credit and description satisfy the artistic-work form [S17].

### 9.6 *The Long Places*: authorship and revision history

The file opens: "# 19 The Long Places - revised by Claude, final" (l.1) and "*GLM 5.3's novella (file 10), revised by three Claude agents from an independent reading (13) and a shared plan (16), then checked by a fresh reader (18), with every finding applied. What changed, and why, is in 17's change logs.*" (l.3). The source is AI-written and AI-revised:

```
authorship_mode: ai_generated_human_directed   # confirm the human role with the user
source_versions:
  - {version_id: "10", label: "novella", made_by: "GLM 5.3", human_role: "to ask: prompts, brief"}
  - {version_id: "13", label: "independent reading", made_by: unknown}
  - {version_id: "16", label: "shared plan", made_by: unknown}
  - {version_id: "17", label: "change logs", made_by: unknown}   # probably the revising agents
  - {version_id: "18", label: "fresh reader check", made_by: unknown}
  - {version_id: "19", label: "revised by Claude, final", made_by: "three Claude agents"}
rights_status: own_original      # if the user ran these models
counsel_review: recommended      # if commercial_sale
```

Consequences:
1. The tools pass on whatever rights exist: Z.ai says users retain output rights [U, S41]; Anthropic assigns its rights "if any" [V, S40].
2. In the US the text may be unprotected except for human selection, arrangement or edits [S1]; the UK is moving the same way [S4]. Others could copy its words; the film is still protected by its human authorship (§3.2).
3. Ask the user for files 10–18, their own prompts and approvals; store hashes in `source_versions[]` as evidence.
4. Credit (Recipe 6, AI-written-source template): "Based on *The Long Places*, a novella generated with GLM 5.3 and revised with Claude under the direction of [names]." Any screenplay drafted from it by the pipeline's LLM is also AI-written: say so in festival answers and skip awards that require a human-authored screenplay (rule 30) [S26].
5. The novella uses real places ("Erciyes stood up out of the haze to the east", l.37; "the last hospital winter in Kayseri", l.39) and a "Ministry" in Ankara ("The Ministry's fax came in two days", l.451). Keep the places; invent any crest or letterhead for the Ministry and the "Trust"; depict no real official (rule 19).

---

## 10. Open questions for the user, and links to other files

- *The Catch*'s authorship and the workshop's role (§9.1); intended use and territories.
- Accept or rename "IONA VALE" and "OSTREL" after the register checks.
- *The Long Places*: the human role in files 10–18; whether any version is to be sold.
- Locale (critic conflict): it decides police livery, hospital identity and which likeness laws matter most.
- Links: D3 writes `consent_record` for cloned voices; D5 keeps named references in `human_notes`; D9 and D12 fill `asset_licence` for music and fonts (as RIGHTS records, §6.1); D8 puts the credit line on the last credit card (D8-R46); D18 (captions, when written) carries it into subtitle files; D17 applies rule 19 to locale research; D2 R4 flags award-category fit.
- Vocabulary to settle (critic list): D9's `licence` values (`cc0`, `cc_by`, `cc_by_nc`, `royalty_free`, `plan_terms`, `open_weights`, `own_recording`, `unknown`) versus this file's `licence_id` (`cc0`, `cc_by_4_0`, ...). Proposal: one list in the RIGHTS record, D9's short names plus a version suffix only where a licence has versions.

---

## Sources

All checked 2026-09-27.

- [S1] US Copyright Office, AI report Part 2, Copyrightability (Jan 2025): https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf
- [S2] US Copyright Office, NewsNet 1060: https://www.copyright.gov/newsnet/2025/1060.html
- [S3] SCOTUSblog, *Thaler v. Perlmutter*, No. 25-449: https://www.scotusblog.com/cases/thaler-v-perlmutter/
- [S4] UK Government, Report on Copyright and AI (18 Mar 2026): https://assets.publishing.service.gov.uk/media/69ba692226909a14239612e4/CP2602959_-_Report_on_Copyright_and_Artificial_Intelligence_web.pdf
- [S5] IPKat on *Mio/konektra* (C-580/23 and C-795/23): https://ipkitten.blogspot.com/2025/12/cjeu-broadly-follows-ag-and.html ; Lydian on the originality test: https://www.lydian.be/en/news-insights/cjeu-clarifies-copyright-protection-applied-art-insights-miokonektra-judgment ; Servola on the scheduled Advocate General opinion (search summary): https://servola.de/journal/the-case-that-prices-ai-training/ ; Bird & Bird on *Like Company*: https://www.twobirds.com/en/insights/2026/like-company-v-google-cjeu-holds-first-ever-hearing-on-generative-ai-and-copyright-on-10-march-2026
- [S6] US Copyright Office, Circular 14, derivative works: https://www.copyright.gov/circs/circ14.pdf
- [S7] Cornell, Copyright term and the public domain: https://guides.library.cornell.edu/copyright/publicdomain
- [S8] Duke CSPD, Public Domain Day 2026: https://web.law.duke.edu/cspd/publicdomainday/2026/
- [S9] StarTrek.com, fan film guidelines: https://www.startrek.com/fan-films
- [S10] Axios, Disney letter to ByteDance: https://www.axios.com/2026/02/13/disney-bytedance-seedance ; CNBC, ByteDance safeguards: https://www.cnbc.com/2026/02/16/bytedance-safegaurds-seedance-ai-copyright-disney-mpa-netflix-paramount-sony-universal.html
- [S11] CourtListener docket, *Disney Enterprises v. Midjourney*, 2:25-cv-05275 (page refused automated reading): https://www.courtlistener.com/docket/70513159/disney-enterprises-inc-v-midjourney-inc/ ; Variety on discovery (July 2026, search summary): https://variety.com/2026/film/news/midjourney-studios-ai-copyright-discovery-1236800902/
- [S12] Holland & Knight on the Tennessee ELVIS Act: https://www.hklaw.com/en/insights/publications/2024/04/first-of-its-kind-ai-law-addresses-deep-fakes-and-voice-clones
- [S13] California AB 1836 (Chapter 258, 2024): https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202320240AB1836 ; AB 2602: https://calmatters.digitaldemocracy.org/bills/ca_202320240ab2602
- [S14] New York Governor, synthetic performer law: https://www.governor.ny.gov/news/governor-hochul-announces-first-nation-law-requiring-disclosure-when-advertisements-include-ai
- [S15] Congress.gov, S.4591 NO FAKES Act of 2026 (page refused automated reading; committee date from S62): https://www.congress.gov/bill/119th-congress/senate-bill/4591 ; Byte Back (20 August 2026): https://www.bytebacklaw.com/2026/08/a-federal-shift-in-ai-and-the-right-of-publicity-no-fakes-act-advances-in-congress/
- [S16] FTC, Take It Down Act enforcement: https://www.ftc.gov/business-guidance/blog/2026/05/take-it-down-act-enforcement-starts-now-what-know-about-ftc-tida
- [S17] EU AI Act, Article 50: https://artificialintelligenceact.eu/article/50/ ; Article 3 definitions (4) and (60): https://artificialintelligenceact.eu/article/3/
- [S18] European Commission, Quick facts on transparency rules: https://digital-strategy.ec.europa.eu/en/factpages/quick-facts-transparency-rules-ai-systems
- [S19] Future of Privacy Forum, AI Act timeline under the AI Omnibus: https://fpf.org/blog/the-ai-act-implementation-timeline-what-changes-under-the-ai-omnibus/
- [S20] Greenberg Traurig on Article 50 guidelines: https://www.gtlaw.com/en/insights/2026/6/deepfakes-chatbots-ai-generated-text-european-commission-details-transparency-obligations-under-the-ai-act
- [S21] Schjødt, Denmark's copyright approach to deepfakes: https://schjodt.com/news/owning-the-self-denmarks-copyright-turn-against-deepfakes
- [S22] SAG-AFTRA, 2026 TV/theatrical agreement (page refused automated reading; vote figures and dates from search summaries of it and Deadline): https://www.sagaftra.org/sag-aftra-members-approve-2026-tvtheatrical-contracts-tentative-agreement ; https://deadline.com/2026/06/sag-aftra-members-approve-amptp-deal-2026-1236941651/
- [S23] YouTube Help, GenAI disclosure: https://support.google.com/youtube/answer/14328491 ; YouTube Blog (27 May 2026): https://blog.youtube/news-and-events/improving-ai-labels-viewers-creators/
- [S24] TikTok Newsroom, AI transparency: https://newsroom.tiktok.com/en-us/partnering-with-our-industry-to-advance-ai-transparency-and-literacy
- [S25] Meta, AI labels (6 Feb 2024): https://about.fb.com/news/2024/02/labeling-ai-generated-images-on-facebook-instagram-and-threads/
- [S26] Academy, 99th Oscars rules (1 May 2026): https://press.oscars.org/news/awards-rules-and-campaign-promotional-regulations-approved-99th-oscarsr
- [S27] AIFilms blog, Cannes 2026 AI rule (secondary): https://studio.aifilms.ai/blog/cannes-2026-ai-ban-official-selection (festival regulation text not read; agrees with S59)
- [S28] Screen Daily, Berlinale asks about AI (page refused automated reading): https://www.screendaily.com/news/berlinale-asking-have-you-used-ai-of-submitted-films/5211259.article
- [S29] Sundance, Nonfiction Core Application 3.1: https://www.sundance.org/blogs/an-update-to-the-nonfiction-core-application-3-1-adding-optional-genai-questions-and-field-resources/
- [S30] C2PA specifications (2.4 listed as latest): https://spec.c2pa.org/specifications/specifications/2.2/index.html
- [S31] Gemini Help, verifying AI content: https://support.google.com/gemini/answer/16722517
- [S32] Google, Generative AI Prohibited Use Policy (17 Dec 2024): https://policies.google.com/terms/generative-ai/use-policy
- [S33] OpenAI, Usage policies (effective 29 October 2025; page refused automated reading): https://openai.com/policies/usage-policies/ ; NBC News on Sora 2 likeness guardrails and cameos (search summary): https://www.nbcnews.com/tech/tech-news/openai-sora-2-guardrails-sag-aftra-bryan-cranston-rcna238715
- [S34] Kling AI Terms of Service (21 Apr 2026): https://kling.ai/docs/user-policy ; Paid Service terms: https://kling.ai/docs/payment-policy
- [S35] Runway Terms of Use (15 September 2026): https://runway.com/terms-of-use
- [S36] Luma, Dream Machine licensing (28 May 2025): https://lumalabs.ai/learning-hub/licensing
- [S37] Midjourney Terms of Service (page refused automated reading): https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service
- [S38] ElevenLabs Prohibited Use Policy (17 August 2026): https://elevenlabs.io/use-policy ; pricing: https://elevenlabs.io/pricing
- [S39] Gemini API Additional Terms (28 Apr 2026): https://ai.google.dev/gemini-api/terms
- [S40] Anthropic Consumer Terms (8 Oct 2025): https://www.anthropic.com/legal/consumer-terms ; update notice: https://www.anthropic.com/news/updates-to-our-consumer-terms
- [S41] Z.ai Terms of Use (via search summary): https://docs.z.ai/legal-agreement/terms-of-use
- [S42] Adobe, Firefly approach and indemnity (via search summary): https://business.adobe.com/products/firefly-business/firefly-ai-approach.html
- [S43] Hugging Face, Wan2.2: https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B ; HunyuanVideo 1.5 licence: https://huggingface.co/tencent/HunyuanVideo-1.5/blob/main/LICENSE
- [S44] Creative Commons, About CC licenses: https://creativecommons.org/share-your-work/cclicenses/
- [S45] Freesound FAQ: https://freesound.org/help/faq/
- [S46] OFL FAQ: https://openfontlicense.org/ofl-faq/
- [S47] Adobe, Mixamo FAQ (via search summary): https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html
- [S48] MakeHuman Community, MPFB FAQ (via search summary): https://static.makehumancommunity.org/mpfb/faq/can_i_sell_models.html
- [S49] fal, Data retention and storage: https://fal.ai/docs/documentation/model-apis/media-expiration
- [S50] Gemini Apps Privacy Hub: https://support.google.com/gemini/answer/13594961
- [S52] Trademark registers: USPTO https://tmsearch.uspto.gov/ ; EUIPO TMview https://www.tmdn.org/tmview/ ; UK IPO https://www.gov.uk/search-for-trademark
- [S53] Justia, OSTRIL trademark (via search result): https://trademark.justia.com/881/09/ostril-88109476.html
- [S54] Amazon UK, "Iona Vale" author page (via search result): https://www.amazon.co.uk/stores/author/B0D1MH51KQ
- [S55] Moonvalley, Marey trained on licensed data: https://www.moonvalley.com/beyondtheframe/moonvalley-s-marey-is-trained-on-fully-licensed-data
- [S56] Web search for "Nell Rowan" (not a register search).
- [S57] GOV.UK, How long copyright lasts: https://www.gov.uk/copyright/how-long-copyright-lasts
- [S58] ICTRecht, the European Commission's objection to Denmark's proposal (19 March 2026): https://www.ictrecht.nl/en/blog/de-ec-fluit-denemarken-terug-toch-geen-copyright-op-je-eigen-gezicht
- [S59] Film Stories, Cannes 2026 and AI (15 May 2026): https://filmstories.co.uk/news/cannes-2026-and-the-unanswered-question-about-ai-in-cinema/
- [S60] Tester reports on Seedance 2.0 face and IP filters (third-party blogs, April 2026; search summaries): https://thesource.com/2026/04/15/seedance/ ; https://seedance2pro.io/blog/seedance-2-0-visual-restrictions-guide
- [S61] Skadden, two New York AI laws (January 2026): https://www.skadden.com/insights/publications/2026/01/two-newly-enacted-new-york-laws-will-regulate ; NY Senate, S8420A: https://www.nysenate.gov/legislation/bills/2025/S8420/amendment/A
- [S62] Holland & Knight, Senate Judiciary Committee advances NO FAKES (June 2026): https://www.hklaw.com/en/insights/publications/2026/06/senate-judiciary-committee-advances-legislation-to-protect-name
